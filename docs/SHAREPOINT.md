# Lägga kalkylatorn på en SharePoint-sida

`docs/kalkylator.html` är hela kalkylatorn i en enda fil: modellen, gränssnittet och
diagrammen. Ingen server, inga externa bibliotek, inga nätverksanrop — allt räknas i
webbläsaren. Det gör den enkel att bädda in, och det gör den lätt att svara på när någon
frågar vart lönesiffrorna tar vägen: ingenstans, de lämnar aldrig datorn.

Fyra vägar in i SharePoint. Väg A ger den inbäddad på sidan, väg D är den enklaste av
allihop om man kan leva med att folk laddar ner den.

---

## A. GitHub Pages + webbdelen Bädda in (snabbast, ~10 min)

Filen hostas av GitHub Pages och visas i en `iframe` på SharePoint-sidan.

**1. Slå på Pages.** I repot: **Settings → Pages → Build and deployment**. Välj
*Deploy from a branch*, branch = den branch som filen ligger på, mapp = **`/docs`**. Spara.

**2. Vänta ~1 minut** och öppna adressen som dyker upp:

```
https://antonalin.github.io/automation-value-model/kalkylator.html
```

Testa att den funkar i en vanlig flik först.

**3. Lägg in den på sidan.** Redigera SharePoint-sidan → **+** → sök upp webbdelen
**Bädda in** (*Embed*) → klistra in antingen adressen ovan, eller den här koden om du vill
styra höjden:

```html
<iframe src="https://antonalin.github.io/automation-value-model/kalkylator.html"
        width="100%" height="1500" style="border:0"
        title="Automatiseringskalkyl"></iframe>
```

Kalkylatorn är responsiv, så den fungerar både i en full sidbredd och i en smal kolumn —
men den blir mycket trevligare i en enkolumnssektion i full bredd.

**4. Om det står "refused to connect" eller att domänen inte är tillåten.** SharePoint
har en tillåtelselista för iframes per webbplatssamling. En administratör för
webbplatssamlingen går till **Webbplatsinställningar → HTML-fältsäkerhet**
(*Site Settings → HTML Field Security*) och lägger till:

```
antonalin.github.io
```

Alternativet *Tillåt iframes från alla domäner* fungerar också men är onödigt brett.
GitHub Pages i sig blockerar inte inbäddning, så sitter det still efter det här är det
något annat i tenanten som stoppar det — då är väg B eller C rätt.

---

## B. Hosta filen inne i SharePoint (inget externt beroende)

Vill man inte peka utanför tenanten kan filen ligga i SharePoint själv.

1. Ladda upp `kalkylator.html` till biblioteket **Webbplatstillgångar** (*Site Assets*)
   på webbplatsen.
2. Modern SharePoint laddar som standard **ner** HTML-filer istället för att visa dem.
   Det styrs av *browser file handling*, som en SharePoint-administratör ändrar per
   webbplats med PowerShell:

   ```powershell
   Set-SPOSite -Identity https://<tenant>.sharepoint.com/sites/<webbplats> `
               -BrowserFileHandling Permissive
   ```

3. Bädda sedan in filens URL med webbdelen **Bädda in**, precis som i steg A3.

Fördelen är att inget lämnar tenanten och att åtkomsten följer webbplatsens behörigheter.
Nackdelen är att uppdateringar blir en manuell filuppladdning istället för en push, och
att `Permissive` gäller hela webbplatsen — därför är det värt att fråga IT innan.

---

## C. SPFx-webbdel (rätt sätt om det ska användas brett)

Ska kalkylatorn bli en riktig, valbar webbdel som vem som helst kan lägga på sin sida är
SharePoint Framework vägen: `yo @microsoft/sharepoint`, klistra in modellen och
gränssnittet i webbdelen, `gulp bundle --ship && gulp package-solution --ship`, och ladda
upp `.sppkg` till **appkatalogen**. Det kräver Node, ett byggsteg och att någon får
publicera till appkatalogen, men ger paketering, versionshantering och inställningar
(t.ex. förifyllda löner) direkt i webbdelens egenskapsruta.

Lönt bara om många ska använda den återkommande. För ett beslutsunderlag som används
någon gång i månaden räcker väg A.

---

## D. Bara ladda upp filen och låta folk hämta hem den (enklast)

Lägg `kalkylator.html` i ett vanligt dokumentbibliotek och länka till den från sidan.
SharePoint laddar ner filen istället för att visa den, och användaren öppnar den i sin
webbläsare. Eftersom filen är självständig fungerar den lika bra från hårddisken:
inga nätverksanrop, diagram och beräkningar körs som vanligt, och både
*Kopiera sammanfattning* och *Kopiera länk till caset* fungerar från `file://`.

Ingen administratör behövs, ingen tillåtelselista, inget externt beroende. Två saker att
väga in ändå:

**Versionsdrift är den verkliga kostnaden.** Varje nedladdning är en kopia som aldrig
uppdateras. Rättar man en parameter om ett halvår sitter halva avdelningen kvar på den
gamla filen, och två personer får olika svar på samma case utan att förstå varför.
Datumstämpla filnamnet (`kalkylator-2026-08.html`) så syns det åtminstone.

**Friktionen avgör om den används.** Klicka, ladda ner, leta i Hämtade filer, öppna — mot
noll steg för en inbäddad sida. Ska kalkylen faktiskt användas i beslut och inte bara
finnas är väg A värd de tio minuterna.

Edge och Chrome frågar ibland "Behåll?" på nedladdade HTML-filer. Det är ofarligt men ser
skumt ut för den som inte väntat sig det, så det är värt en rad i texten på sidan.

---

## Förifylla ett case

Parametrarna hamnar i adressens hash, så ett specifikt case kan länkas eller bäddas in
förifyllt. Knappen **Kopiera länk till caset** ger adressen direkt, och den kan klistras
in i `iframe`-koden:

```
kalkylator.html#manual_minutes_per_run=25&runs_per_year=250&build_hours=60&monthly_salary_sek=42000
```

Allt som inte anges faller tillbaka på standardvärdena.

---

## Vad som inte fungerar

**Webbdelen Textblock.** Den kör ingen JavaScript, så det går inte att klistra in
kalkylatorn som text.

**Skriptredigeraren.** Den är borttagen ur moderna sidor. Finns den kvar på en klassisk
sida fungerar den, men bygg inget nytt på den.

**Power Apps eller Excel istället.** Den deterministiska delen går att bygga i båda, men
Monte Carlo med 50 000 scenarier gör det inte — i Excel blir det segt och i Power Fx blir
det värre. Det är också där det mesta av värdet i modellen ligger, så det är fel sak att
kompromissa bort.
