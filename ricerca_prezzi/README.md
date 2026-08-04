# Ricerca prezzi — Clan Pesca vs concorrenti online

Confronto dei prezzi dei prodotti venduti su [clanpesca.com](https://clanpesca.com)
con i principali negozi online di pesca sportiva in Italia.

**Stato: impostazione** — in attesa dello sblocco dell'accesso di rete
dell'ambiente Claude Code per leggere i siti (vedi sotto).

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

## Vincolo tecnico da risolvere

L'ambiente Claude Code remoto ha la policy di rete "solo domini fidati":
`clanpesca.com` e i siti concorrenti sono bloccati (HTTP 403 sia da terminale
sia dal fetcher). Per eseguire la ricerca serve impostare l'accesso di rete
dell'ambiente su "tutti i domini" da claude.ai/code → impostazioni ambiente.
Documentazione: https://code.claude.com/docs/en/claude-code-on-the-web
