# Ricerca prezzi — Clan Pesca vs concorrenti online

Confronto dei prezzi dei prodotti venduti su [clanpesca.com](https://clanpesca.com)
con i principali negozi online di pesca sportiva in Italia.

**Stato: completata (prima rilevazione, 5 agosto 2026).**
Risultati e raccomandazioni: **[REPORT.md](REPORT.md)** · dati completi:
[`confronto_prezzi.csv`](confronto_prezzi.csv) (777 rilevazioni con URL) ·
campione: [`campione.csv`](campione.csv).

## In sintesi

- Campione di **37 prodotti di marca disponibili** (7 mulinelli, 6 canne, 12 artificiali,
  5 fili, 4 minuteria, 3 accessori) scelti tra i bestseller identificabili con
  marca+modello, con variante esatta e SKU.
- **18 prodotti confrontati** con almeno un concorrente a parità di modello/taglia:
  Clan Pesca è in mediana **+4,4% sopra la mediana** dei concorrenti (11 sopra, 2 in
  linea, 5 sotto). **19 prodotti non sono trattati da nessun concorrente verificato**
  (distribuzione di fatto esclusiva).
- Il concorrente più sovrapposto è **bassstoreitaly.com** (20 prodotti su 37).

## Nota sui marchi (correzione rispetto all'impostazione)

Il catalogo reale di clanpesca.com è centrato su **Molix, Carson, Mikado, Tubertini,
Owner, BKK, Heron, Golden Catch, Tamura, Fladen, Shimano** (+ nicchie JDM: Nories,
Smith, Major Craft, Keitech, Gary Yamamoto...). Daiwa, Rapala e Colmic — ipotizzati
all'avvio — **non sono nel catalogo**; Trabucco è marginale (3 articoli).

## Siti concorrenti — esito verifica

| # | Sito | Esito |
|---|------|-------|
| 1 | pescaloccasione.it | ⛔ non verificabile (bot-wall 403/503) |
| 2 | megafish.it | ✅ verificato (API di ricerca) |
| 3 | bassstoreitaly.com | ✅ verificato (sitemap + pagine prodotto) — **concorrente principale** |
| 4 | sampey.it | ✅ verificato — nessuna sovrapposizione sul campione |
| 5 | bestpesca.com | ✅ verificato (sitemap) — nessuna sovrapposizione |
| 6 | fishingitalia.com | ✅ verificato |
| 7 | mondo-pesca.it | ✅ verificato — **è diventato escaepescashop.it** (redirect) |
| 8 | pescafishingshop.com | ✅ verificato — nessuna sovrapposizione |
| 9 | marlinblue.it | ✅ verificato — nessuna sovrapposizione |
| 10 | pescapromo.it | ✅ verificato — 2° per sovrapposizione |
| 11 | misterfish.shop | ⚠️ parziale (ricerca interna via JS; sitemap ridotta) |
| 12 | free-fishing.it | ⛔ irraggiungibile |
| 13 | decathlon.it | ⛔ non verificabile (bot-wall) |
| 14 | marcosportshop.com | ⛔ non verificabile (bot-wall) |
| 15 | webpesca.it | ✅ verificato (molti articoli però esauriti) |
| 16 | propesca.it | ✅ verificato — nessuna sovrapposizione |
| 17 | dimensionepesca.com | ✅ verificato |
| 18 | pescamia.eu | ✅ verificato (sitemap) — nessuna sovrapposizione |
| 19 | amazon.it | ⛔ non verificabile (bot-wall) |
| 20 | trovaprezzi.it / idealo.it | ⛔ non verificabili (bot-wall) |

Esclusi: piscor.com (chiuso, segnalazione del titolare), pescanet.it (non verificato).
I 7 siti bloccati richiedono una rilevazione manuale (o un accesso browser reale):
sono il principale punto aperto, insieme al re-check periodico dei 18 confrontabili.

## Metodo (com'è stata fatta)

1. Lettura del catalogo clanpesca.com dalle pagine marca (1.177 prodotti di marca, tutti
   con prezzo/disponibilità) e dai bestseller per categoria (ordinamento per popolarità).
2. Selezione del campione con variante esatta (taglia/misura/diametro) e SKU.
3. Per ogni prodotto, ricerca su ogni concorrente con tre canali: ricerca interna del
   sito, API di ricerca dove esiste, sitemap prodotti con matching degli slug. Prezzo e
   disponibilità letti dalla pagina prodotto (JSON-LD/microdati). Nessun prezzo stimato:
   ogni rilevazione nel CSV ha l'URL di provenienza.
4. Confronto solo a parità di modello e taglia; le somiglianze sono registrate come
   `variante_diversa` ed escluse dalle statistiche.

Nota storica: un report precedente (fatto sul computer del titolare) copriva solo
4 prodotti; questa ricerca lo sostituisce.
