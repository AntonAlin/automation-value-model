# Sidtext för SharePoint

Färdig text att klistra in på en SharePoint-sida. Rubrikerna motsvarar textblock —
klistra in styckena i ett eller flera **Textblock**, och lägg länken till filen där det
står `[länk till kalkylatorn]`. Bäddar du in kalkylatorn med webbdelen **Bädda in**
istället, stryk stycket "Så gör du" och lägg webbdelen direkt under introt.

Ersätt `[Namn]` och `[e-post]` innan du publicerar.

---

## Ska vi automatisera det här? Räkna först.

Någon har en manuell rutin, den känns tjatig, och magkänslan säger att vi borde bygga bort
den. Problemet är att magkänslan nästan alltid räknar fel. Den utgår från att bygget tar
exakt så lång tid vi gissade, att automationen funkar felfritt och att processen lever för
evigt. Inget av det stämmer.

Kalkylatorn på den här sidan svarar på något mer användbart än "sparar det tid?":
**hur sannolikt är det att vi faktiskt tjänar på det, hur mycket i snitt, och hur mycket
riskerar vi om det går snett** — allt i kronor.

Räkna innan bygget beställs, inte efter. Det tar fem minuter.

### Så gör du

1. Ladda ner kalkylatorn: [länk till kalkylatorn]
2. Öppna filen i webbläsaren. Den fungerar direkt från datorn — ingen installation, inget
   konto, ingen data lämnar din dator.
3. Fyll i rutinen du funderar på. Resultatet räknas om medan du skriver.
4. Klicka **Kopiera sammanfattning** och klistra in den i ärendet eller mejlet där beslutet
   ska fattas.

Om webbläsaren frågar "Behåll?" när du laddar ner filen är det bara den vanliga varningen
för HTML-filer. Svara ja.

### Vad du behöver veta innan du fyller i

Tre siffror avgör nästan hela utfallet, så var ärlig med dem:

**Minuter per körning.** Den verkliga tiden, inklusive avbrott, väntan och rättningar —
inte den tid rutinen tar när allt går perfekt.

**Andel sparad tid som blir värde.** Det här är den viktigaste rutan. Om ingen använder
den frigjorda tiden till något som skapar värde är besparingen mest luft. Standard är
70 procent. Sätt lägre om tiden sprids ut i småbitar över veckan, för tio minuter här och
där blir sällan något.

**Byggtid.** Utvecklingsestimat lutar systematiskt mot underskattning. Skriv din gissning
— modellen räknar redan med att det kan bli rejält mycket värre, men inte att du gissar
medvetet lågt.

Bygger någon annan än den som gör jobbet idag: fyll i båda lönerna. Samma rutin kan gå
från självklart ja till nej om en dyr specialist bygger bort en billig process.

### Vad siffrorna betyder

**Sannolikhet lönsam** — andelen scenarier där automationen går plus. Över 85 procent är
ett tydligt ja, under 50 procent ett lika tydligt nej.

**Väntevärde (EMV)** — vad vi tjänar i snitt över alla scenarier, inklusive de som
havererar.

**Nedsida om det går fel (CVaR)** — vad vi förlorar i snitt i de scenarier som går back.
Det här är siffran att titta på när någon frågar "vad är värsta fallet".

**Break-even** — hur många körningar det tar innan bygget är betalt.

**Dom** — en sammanfattning av ovanstående. Den ersätter inte omdöme, men den gör det
svårare att prata sig förbi siffrorna.

### Vad kalkylen inte gör

Den mäter tid och pengar. Den mäter inte att en manuell rutin är tråkig, att den skapar
fel som ingen upptäcker, eller att någon slutar för att jobbet är själsdödande. Ibland är
det goda skäl att automatisera ändå — men då ska det sägas rakt ut, inte gömmas i en
uppblåst tidsbesparing.

Den räknar också varje osäkerhet för sig. I verkligheten hänger ett strulande bygge ihop
med både mer underhåll och större risk att det aldrig når produktion, så den riktiga
nedsidan är något värre än den som visas.

### Frågor

Hör av dig till [Namn], [e-post]. Är du osäker på vad du ska fylla i, hör av dig i förväg
— en kalkyl med påhittade siffror är värre än ingen kalkyl alls.
