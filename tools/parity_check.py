#!/usr/bin/env python3
"""
Kollar att HTML-kalkylatorn räknar likadant som notebooken.

Modellen finns på två ställen — Python i projektautomatisering.ipynb och en port
till JavaScript i docs/kalkylator.html — och två implementationer glider isär om
ingen tittar till dem. Skriptet plockar ut båda, kör samma case genom dem och
jämför.

Bara de deterministiska talen och känslighetsanalysen jämförs exakt. Monte Carlo
kan inte matchas krona för krona eftersom slumpgeneratorerna är olika, så där
kontrolleras bara att sannolikheten att det lönar sig hamnar inom en dryg
procentenhet.

Kör: python tools/parity_check.py   (kräver python med numpy/pandas samt node)
"""

from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
NOTEBOOK = ROOT / "projektautomatisering.ipynb"
CALCULATOR = ROOT / "docs" / "kalkylator.html"

# Fälten anges som i formuläret: procenttalen i procent, inte som andel.
CASES = [
    {},                                        # README-exemplet, rena defaultvärden
    {
        "manual_minutes_per_run": 25, "runs_per_year": 250, "horizon_years": 2.5,
        "build_hours": 60, "maintenance_hours_per_year": 12,
        "monthly_salary_sek": 42000, "builder_monthly_salary_sek": 75000,
        "overhead_pct": 20, "p_go_live": 80, "reliability": 90,
        "obsolescence_hazard": 15, "discount_rate": 4, "capacity_realization": 50,
    },
    {
        "manual_minutes_per_run": 240, "runs_per_year": 12, "horizon_years": 5,
        "build_hours": 8, "maintenance_hours_per_year": 0,
        "monthly_salary_sek": 38000, "overhead_pct": 0,
        "p_go_live": 100, "reliability": 100, "obsolescence_hazard": 0,
        "discount_rate": 0, "capacity_realization": 100,
    },
    {
        "manual_minutes_per_run": 5, "runs_per_year": 52, "horizon_years": 1.5,
        "build_hours": 100, "maintenance_hours_per_year": 20,
        "monthly_salary_sek": 30000, "builder_monthly_salary_sek": 90000,
        "capacity_realization": 30,
    },
]

PCT_FIELDS = ("social_fee_pct", "overhead_pct", "p_go_live", "reliability",
              "obsolescence_hazard", "discount_rate", "capacity_realization")

JS_RUNNER = r"""
import fs from 'fs';
const html = fs.readFileSync(process.argv[2], 'utf8');
const script = html.split('<script>')[1].split('</script>')[0];
const cut = script.indexOf('const $ = id =>');   // allt före detta är modellen
if (cut < 0) throw new Error('hittade inte modellen i kalkylator.html');
const model = new Function(script.slice(0, cut) +
  '\nreturn {DEFAULTS, recomputeRates, deterministic, monteCarlo, sensitivity};')();

const cases = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'));
const PCT = ["social_fee_pct","overhead_pct","p_go_live","reliability",
             "obsolescence_hazard","discount_rate","capacity_realization"];

const out = cases.map(raw => {
  const c = Object.assign({}, model.DEFAULTS, raw);
  for (const p of PCT) c[p] = c[p] / 100;
  model.recomputeRates(c);
  const det = model.deterministic(c);
  const mc = model.monteCarlo(c, 50000, 42).summary;
  const sens = model.sensitivity(c);
  return {
    hourly_value: det.hourly_value,
    build_hourly_cost: det.build_hourly_cost,
    naive_gross_saved_h: det.naive_gross_saved_h,
    risk_adjusted_net_h: det.risk_adjusted_net_h,
    build_sek: det.build_sek,
    net_sek: det.net_sek,
    roi_pct: det.roi_pct,
    breakeven_runs: Number.isFinite(det.breakeven_runs) ? det.breakeven_runs : null,
    p_profitable: mc.p_profitable,
    sens: Object.fromEntries(sens.map(r => [r.parameter, r.span])),
  };
});
process.stdout.write(JSON.stringify(out));
"""


def load_python_model():
    """Plocka ut kodcellen med modellen ur notebooken och exekvera den."""
    nb = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    for cell in nb["cells"]:
        src = "".join(cell["source"])
        if cell["cell_type"] == "code" and "def burdened_hourly_rate" in src:
            ns: dict = {}
            exec(compile(src.replace('if __name__ == "__main__":', "if False:"),
                         "<notebook>", "exec"), ns)
            return ns
    raise SystemExit("hittade ingen modellcell i notebooken")


def python_results(ns, cases):
    AutomationCase = ns["AutomationCase"]
    results = []
    for raw in cases:
        kwargs = dict(raw)
        for p in PCT_FIELDS:
            if p in kwargs:
                kwargs[p] = kwargs[p] / 100
        case = AutomationCase(**{**{"manual_minutes_per_run": 90, "runs_per_year": 52},
                                 **kwargs})
        det = ns["deterministic_analysis"](case)
        mc, _ = ns["monte_carlo"](case)
        sens = ns["sensitivity"](case)
        results.append({
            "hourly_value": case.hourly_value_sek,
            "build_hourly_cost": case.build_hourly_cost_sek,
            "naive_gross_saved_h": det["naiv_bruttobesparing_h"],
            "risk_adjusted_net_h": det["riskjusterad_nettobesparing_h"],
            "build_sek": det["byggkostnad_sek"],
            "net_sek": det["riskjusterat_nettovarde_sek"],
            "roi_pct": det["roi_pct"],
            "breakeven_runs": (det["breakeven_korningar"]
                               if det["breakeven_korningar"] != "aldrig" else None),
            "p_profitable": mc["sannolikhet_lonsam"],
            "sens": dict(zip(sens["parameter"], sens["spann_sek"])),
        })
    return results


def js_results(cases):
    with tempfile.TemporaryDirectory() as tmp:
        runner = pathlib.Path(tmp) / "runner.mjs"
        payload = pathlib.Path(tmp) / "cases.json"
        runner.write_text(JS_RUNNER, encoding="utf-8")
        payload.write_text(json.dumps(cases), encoding="utf-8")
        proc = subprocess.run(["node", str(runner), str(CALCULATOR), str(payload)],
                              capture_output=True, text=True)
        if proc.returncode != 0:
            raise SystemExit("node misslyckades:\n" + proc.stderr)
        return json.loads(proc.stdout)


# Toleranser: deterministiska tal ska matcha så när som på avrundning,
# Monte Carlo bara ungefärligt.
TOLERANCE = {
    "hourly_value": 1.0, "build_hourly_cost": 1.0,
    "naive_gross_saved_h": 0.1, "risk_adjusted_net_h": 0.1,
    "build_sek": 1.0, "net_sek": 1.0, "roi_pct": 0.1,
    "breakeven_runs": 0.1, "p_profitable": 0.015,
}


def main() -> int:
    py = python_results(load_python_model(), CASES)
    js = js_results(CASES)

    failures = []
    for i, (p, j) in enumerate(zip(py, js), start=1):
        for key, tol in TOLERANCE.items():
            a, b = p[key], j[key]
            if a is None or b is None:
                if a != b:
                    failures.append(f"case {i}: {key} — python {a}, js {b}")
                continue
            if abs(float(a) - float(b)) > tol:
                failures.append(f"case {i}: {key} — python {a}, js {b} (tol {tol})")
        for param, span in p["sens"].items():
            if param not in j["sens"]:
                failures.append(f"case {i}: känslighet saknar {param} i js")
            elif abs(float(span) - float(j["sens"][param])) > 2.0:
                failures.append(f"case {i}: känslighet {param} — "
                                f"python {span}, js {round(j['sens'][param])}")

    if failures:
        print("Modellerna har glidit isär:")
        for f in failures:
            print("  -", f)
        return 1

    print(f"OK: notebooken och docs/kalkylator.html räknar likadant "
          f"på {len(CASES)} case.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
