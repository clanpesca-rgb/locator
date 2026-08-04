# Ricerca prezzi — Clan Pesca vs concorrenti online

Confronto dei prezzi dei prodotti venduti su [clanpesca.com](https://clanpesca.com)
con i principali negozi online di pesca sportiva in Italia.

**Stato: prima rilevazione completata (4 agosto 2026)** — risultati in
[`REPORT.md`](REPORT.md), tabella in [`confronto_prezzi.csv`](confronto_prezzi.csv),
fonti in [`dati_grezzi.md`](dati_grezzi.md).

La rete dell'ambiente è ancora bloccata (vedi in fondo): la rilevazione è stata
fatta **via snippet dei motori di ricerca** (la ricerca web funziona anche con la
policy restrittiva). Limiti: prezzi affidabili come ordine di grandezza ma non
garantiti "live"; il prezzo Clan Pesca è emerso solo per 11 righe su 33 — per le
altre la colonna è da completare dal gestionale (benchmark concorrenti già pronti).

## Obiettivo

- Campione di **30+ prodotti di marca** (Daiwa, Shimano, Trabucco, Rapala, Colmic, ...)
  scelti tra i ~6.000 del catalogo, dando priorità ai prodotti **disponibili**.
- Confronto prezzo per prezzo con **~20 siti concorrenti** (lista sotto).
- Output: tabella CSV (`confronto_prezzi.csv`) + report leggibile (`REPORT.md`)
  con le conclusioni: dove Clan Pesca è più caro, dove è competitivo, dove conviene ritoccare.

Nota: un report precedente (fatto da Claude Code sul computer del titolare)
copriva solo 4 prodotti; questa ricerca lo sostituisce con un campione ampio.

## Siti concorrenti da confrontare

| # | Sito | Note |
|---|------|------|
| 1 | pescaloccasione.it | >15.000 prodotti, storico |
| 2 | megafish.it | outlet, leader dal 2015 |
| 3 | bassstoreitaly.com | >50.000 prodotti, spinning/bass |
| 4 | sampey.it | Shimano/Daiwa/Trabucco |
| 5 | bestpesca.com | prezzi aggressivi |
| 6 | fishingitalia.com | feeder e colpo |
| 7 | mondo-pesca.it | Trabucco/Daiwa/Italcanna |
| 8 | pescafishingshop.com | outlet multi-marca |
| 9 | marlinblue.it | mulinelli e mare |
| 10 | pescapromo.it | promozioni |
| 11 | misterfish.shop | Toscana, outlet |
| 12 | free-fishing.it | generalista |
| 13 | decathlon.it | grande distribuzione (Caperlan) |
| 14 | marcosportshop.com | Lonigo (VI), segnalato dal titolare |
| 15 | webpesca.it | segnalato dal titolare |
| 16 | propesca.it | attivo dal 1995 |
| 17 | dimensionepesca.com | pesca e nautica |
| 18 | pescamia.eu | generalista |
| 19 | amazon.it | marketplace, prezzo di riferimento |
| 20 | trovaprezzi.it / idealo.it | aggregatori, per i minimi di mercato |

Esclusi: piscor.com (chiuso, segnalazione del titolare), pescanet.it (non verificato).
La lista verrà rifinita in base ai marchi effettivi del catalogo Clan Pesca:
per ogni prodotto contano i siti che lo trattano davvero.

## Metodo

1. Lettura del catalogo clanpesca.com (categorie, marchi, prezzi, disponibilità).
2. Selezione del campione: bestseller e prodotti rappresentativi per categoria
   (mulinelli, canne, artificiali, fili, minuteria), solo articoli identificabili
   con marca+modello (i prodotti "generici" non sono confrontabili).
3. Per ogni prodotto: ricerca del prezzo sui siti concorrenti (stesso modello,
   stessa taglia/misura), annotando prezzo, disponibilità e data di rilevazione.
4. Sintesi: posizionamento medio di Clan Pesca, prodotti fuori mercato,
   opportunità di prezzo.

## Vincolo tecnico (ancora aperto)

L'ambiente Claude Code remoto ha la policy di rete "solo domini fidati":
`clanpesca.com` e i siti concorrenti sono bloccati (HTTP 403 sia da terminale
sia dal fetcher; anche web.archive.org è bloccato). La prima rilevazione ha
aggirato il blocco usando gli snippet dei motori di ricerca, che però non
danno prezzi live né disponibilità.

Per la **seconda passata** (prezzi live, copertura sistematica dei ~20 siti,
monitoraggio periodico) serve impostare l'accesso di rete dell'ambiente su
"tutti i domini" da claude.ai/code → impostazioni ambiente.
Documentazione: https://code.claude.com/docs/en/claude-code-on-the-web
