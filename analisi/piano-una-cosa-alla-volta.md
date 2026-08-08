# Una cosa alla volta — la scala dei fix, dal più semplice

*Deriva dal piano 90 giorni dell'analisi competitiva, riordinato per **sforzo crescente**: si parte da ciò che si chiude in 5 minuti e si sale. Regole del gioco: (1) una voce alla volta, in ordine; (2) una voce è chiusa solo quando passa la sua verifica "fatto quando"; (3) non si apre la successiva prima. Le voci marcate 🔧 richiedono chi vi gestisce il sito (o 15 minuti di un tecnico); tutte le altre si fanno dal pannello WordPress/WooCommerce senza toccare codice.*

---

## Livello 1 — Il primo pomeriggio (tutte insieme fanno ~1 ora)

- [x] **1. Togliere Skype** — ✅ **CHIUSA l'8/8/2026**: la riga "Skype: CLAN_Pesca" è stata rimossa dalla pagina [Contatti](https://clanpesca.com/contatti/), che ora mostra solo telefono, email, indirizzo e orari (verificato live).
- [x] **2. Spegnere "Clan Usato"** — ✅ **CHIUSA l'8/8/2026**: voce rimossa dai menu; verificato live che nella navigazione non restano link morti (`href="#"`). La riattivazione dell'usato come servizio vero resta al livello 4 (voce 16).
- [ ] **3. Nascondere gli esauriti dal catalogo** — oggi 1 scheda su 8 è "Esaurito" ma resta in vetrina. Dove: WooCommerce → Impostazioni → Prodotti → Inventario → spunta "Nascondi gli articoli esauriti dal catalogo". ⏱ 2 min. **Fatto quando:** sfogliando 3 categorie a caso non compaiono più esauriti.
- [ ] **4. P.IVA e venditore coerente** — la P.IVA non è esposta e il bonifico è intestato a Carson Srl mentre le condizioni dicono Clan Pesca srl: per un nuovo cliente che deve bonificare 400€ è un freno. Dove: footer + pagina Condizioni + istruzioni bonifico; decidete la dicitura corretta (se il conto è di Carson Srl, va scritto lì il perché, es. "Carson Srl — società del gruppo Clan Pesca"). ⏱ 30 min. **Fatto quando:** ragione sociale e P.IVA identiche in footer, condizioni e pagina di pagamento.
- [ ] **5. Link recensioni Google, versione manuale** — la raccolta parte oggi, l'automazione arriva al livello 3. Dove: dalla scheda Google Business prendete il link breve "Chiedi recensioni" e mettetelo in firma email, nel messaggio WhatsApp post-vendita e su un cartoncino nel pacco ("Ti sei trovato bene? 30 secondi: lascia una recensione"). ⏱ 30 min. **Fatto quando:** il link parte con ogni ordine e ogni scontrino.

## Livello 2 — Una sera ciascuna

- [ ] **6. 🔧 Sbloccare lo zoom su mobile** — il viewport ha `maximum-scale=1`: chi vuole ingrandire una foto prodotto dal telefono non può. Dove: header del tema (chi vi gestisce il sito lo fa in 15 min). **Fatto quando:** dal telefono si ingrandisce una scheda con due dita.
- [ ] **7. Unificare i marchi doppi** — fiish/fiiish, mehio/meiho, iviline/ivyline spezzano i prodotti su pagine diverse: metà catalogo diventa introvabile. Dove: WooCommerce → Prodotti → attributi/brand: spostare i prodotti sulla grafia giusta e cancellare (o reindirizzare) la doppia. ⏱ 1–2 ore di clic. **Fatto quando:** ogni marchio ha una sola pagina con dentro tutti i suoi prodotti.
- [ ] **8. Aggiornare la scheda Google Business** — orari, foto recenti, link al sito, e rispondere alle ultime recensioni (anche solo "grazie"): è la vostra vetrina più vista e spesso è ferma. ⏱ 1 ora. **Fatto quando:** foto e info sono del 2026 e le ultime 10 recensioni hanno risposta.

## Livello 3 — Mezza giornata ciascuna (qui inizia il ritorno grosso)

- [ ] **9. 🔧 Riparare la ricerca interna** — oggi "metanium" dà 0 risultati e "shimano" trova 18 prodotti su 61: per un catalogo di nicchia la ricerca *è* il commesso. Dove: plugin di ricerca dedicato (es. FiboSearch, gratuito nella versione base) al posto della ricerca standard. **Fatto quando:** "metanium", "shimano" e un refuso tipo "metanum" trovano tutti i prodotti giusti.
- [ ] **10. Soglia spedizione gratuita da 75€ a 59€** — unica voce che è prima una decisione di margine e poi 5 minuti di setting (WooCommerce → Spedizione). I concorrenti diretti sono a 50€; 59€ chiude quasi tutto il gap costando poco. **Fatto quando:** il banner del sito dice "gratis da 59€".
- [ ] **11. 🔧 Redirect 301 dalle vecchie pagine e dai vecchi domini** — l'anzianità di clanpesca.it/clanvergiate.it oggi finisce in 404 e non passa autorevolezza al sito nuovo. Dove: plugin Redirection per le pagine; regola di redirect sui vecchi domini (hosting). **Fatto quando:** aprendo 5 vecchi URL a caso si atterra sulla pagina giusta del sito nuovo.
- [ ] **12. Recensioni automatiche post-ordine** — l'abitudine manuale del punto 5 diventa sistema: email automatica X giorni dopo la consegna con il link. Dove: plugin (es. Customer Reviews for WooCommerce) o l'automazione della piattaforma email. **Fatto quando:** ogni ordine genera la richiesta senza che nessuno se ne ricordi.

## Livello 4 — Progetti (uno al mese, non "fix")

- [ ] **13. La prima scheda "eroe"** — 1 prodotto di nicchia: reel parlato incorporato nella scheda, foto complete, riga "Perché lo teniamo". Poi una a settimana. È l'inizio della leva contenuti, quella che crea domanda per i prodotti a margine.
- [ ] **14. Primi 3 kit per tecnica/lago** e riattivazione del blog (1 guida al mese).
- [ ] **15. Fedeltà minima** (buoni a scaglioni nel pacco) **+ BNPL** (Scalapay/Klarna: nessun concorrente diretto lo ha).
- [ ] **16. "Clan Usato" vero** — regole di permuta pubblicate, valore vincolato a spesa su kit/nicchia.
- [ ] **17. Esclusive e polo tuning** — trattativa ZPI/ZELOS (checklist nel dossier dedicato), canale B2B Hedgehog per Avail, primi contatti Fishman/Issei.

---

*Il criterio dell'ordine: prima ciò che toglie frizioni ed errori visibili (costa quasi zero e smette di perdere clienti), poi ciò che fa trovare i prodotti, poi ciò che costruisce domanda e margine. I riferimenti completi di ogni voce sono nell'[analisi competitiva](analisi-competitiva-clanpesca.md) (§4 criticità e §8 piano 90 giorni) e nel [dossier esclusive](esclusive-jdm-zpi.md).*
