# Analisi linea Pro Tackles — agosto 2026

Analisi dei prodotti a marchio distribuito da **Pro Tackles** (Marco Rossi,
rossi@protackles.com): Molix, Skirmjan, Major Craft, OMTD, Fioretto.

## Fonte dei dati

Tutto viene dai report automatici "Confronto Prezzi Clan Pesca" inviati a
clanpesca@gmail.com:

| Report | Data | Cosa contiene |
|---|---|---|
| Confronto Molix (4 esecuzioni) | 08/08 e 22/08/2026 | 458 famiglie, nostro prezzo vs minimo di mercato su 24-25 negozi |
| Confronto Prezzi Sito | 06/08/2026 | 504 prodotti su 6400, **con costo da 2bit e margine** |

Il report del 22/08 ore 18:08 e' l'unico con matching stretto ("SOLO i confronti
certi: stessa famiglia, misura e variante"). E' quello inviato a Marco ed e'
quello su cui si basa la tabella A dello script.

## Il calcolo

Nei report Molix il costo d'acquisto non c'e'. L'unico ancoraggio di costo
disponibile e' nel Confronto Prezzi Sito del 06/08:

    Molix Hyper Split Ring 9 — nostro 6,90 € — allineare a 3,25 € — margine se allineo: -33,6%

Da cui si ricava il costo:

    (3,25 - C) / 3,25 = -0,336   =>   C = 4,34 €

Cioe' **costo = 62,9% del nostro prezzo al pubblico**, margine attuale **37,1%**,
contro un **pareggio dichiarato del 39,3%**.

Applicando quel rapporto a tutta la linea si ottiene la soglia critica:

> **delta >= +59% => il concorrente vende sotto il nostro costo d'acquisto.**

## Limite da tenere presente

Il rapporto costo/prezzo e' calibrato su **un solo prodotto**, e il report stesso
avverte che "alcuni costi in anagrafica sono vecchi o errati". I numeri per singola
famiglia vanno confermati con l'ultima fattura Pro Tackles. La **direzione** del
risultato invece e' solida: regge anche ipotizzando uno sconto d'acquisto molto
piu' generoso.

## Uso

    python3 analisi_margini.py

L'output completo e' in `output_analisi.txt`.

## Cosa manca per chiudere l'analisi

Lo script non risponde a "quali prodotti non vendono" e "quali rendere": servono
**giacenze e venduto**, che il report del 06/08 segnala come "giacenze: non trovate".
Export necessario da 2bit, per articolo della linea Pro Tackles:

- codice, descrizione, giacenza attuale
- pezzi venduti negli ultimi 12 e negli ultimi 24 mesi
- data primo carico e data ultima vendita
- ultimo costo d'acquisto reale

Con quelle cinque colonne i cassetti "da eliminare" e "da rendere" si compilano da soli.
