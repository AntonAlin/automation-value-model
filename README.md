# Automatiseringsbeslut: en riskjusterad kalkyl

En modell för att avgöra om en manuell rutin är värd att automatisera — i kronor,
med osäkerheten kvantifierad istället för bortgissad.

Istället för "sparad tid > byggtid, alltså kör" svarar modellen på:
hur sannolikt är det att vi tjänar på det, hur mycket i snitt, och hur mycket
riskerar vi om det går snett.

## Innehåll

- **`projektautomatisering.ipynb`** — hela modellen:
  - deterministisk kalkyl (diskontering, överlevnad, sannolikhet att bygget når prod)
  - Monte Carlo över 50 000 scenarier → fördelning istället för en punktskattning
  - känslighetsanalys (tornado) över vilka parametrar som faktiskt styr utfallet
  - KPI-vy för uppföljning av automationer i drift

## Grundidéer

- **Timpriset härleds, gissas inte.** Månadslön → fullt belastad timkostnad
  (arbetsgivaravgift + overhead, fördelat på effektiva timmar/år).
- **Sparad tid blir inte automatiskt pengar.** `capacity_realization` skalar ner
  besparingen till den andel som faktiskt omsätts i värde.
- **Byggtimmen prissätts separat från den sparade timmen**, så att en dyr
  specialist som ersätter en billig process syns i kalkylen.
- **Byggtidsestimat lutar mot underskattning**, så byggtiden modelleras
  lognormalt med fet svans uppåt snarare än symmetriskt.

## Köra

```bash
pip install numpy pandas matplotlib
jupyter lab projektautomatisering.ipynb
```

Modulen kör även fristående (`python`-koden i cell 2) och skriver då ut en
full rapport för exempel-caset.

## Känd förenkling

Alla osäkra parametrar dras oberoende av varandra. I verkligheten hänger ett
struligt bygge ihop med både mer underhåll och högre risk att det aldrig når
produktion, vilket gör den verkliga svansen något tjockare än siffrorna visar.
