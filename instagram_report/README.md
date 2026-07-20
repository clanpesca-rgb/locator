# 📊 Report Instagram giornaliero — Clan Pesca

Script che ogni giorno legge le metriche di @clanpesca dall'API di Meta,
le fa analizzare a Claude e invia il report via email.

## Installazione (una volta sola)

```bash
cd instagram_report
pip install -r requirements.txt
cp .env.example .env
# apri .env e inserisci le chiavi
```

### La password email (causa più comune di mail non arrivate)

Gmail **non accetta la password normale** dell'account per l'invio da script.
Serve una **Password per le app**:

1. Vai su [myaccount.google.com](https://myaccount.google.com) → **Sicurezza**
2. Attiva la **Verifica in due passaggi** (se non è già attiva)
3. Cerca **Password per le app** → creane una (es. "report instagram")
4. Copia i 16 caratteri in `EMAIL_PASSWORD` nel file `.env`

## Prima di lanciare: diagnosi

```bash
python daily_report.py --check
```

Testa uno per uno: file `.env`, token Instagram, insights account,
insights di un post, chiave Claude, login Gmail. Ogni riga dice ✅ o ❌
con la spiegazione. Sistemare i ❌ prima di lanciare il report vero.

## Lancio del report

```bash
python daily_report.py
```

Se qualcosa va storto, lo script prova a mandarti una **mail di errore**
con il dettaglio, così non resti mai senza notizie.

## Esecuzione automatica ogni giorno

**Mac/Linux** — `crontab -e` e aggiungi (report alle 8:00):

```
0 8 * * * cd /percorso/di/locator/instagram_report && python3 daily_report.py >> report.log 2>&1
```

**Windows** — Utilità di pianificazione → Crea attività di base →
ogni giorno alle 8:00 → Avvia programma: `python` con argomento
`daily_report.py` e directory di avvio la cartella `instagram_report`.

## Note sull'API di Meta

- La metrica dei salvataggi per i post si chiama **`saved`** (non `saves`).
- Le metriche account `profile_views`, `accounts_engaged`,
  `total_interactions`, `profile_links_taps` richiedono
  `metric_type=total_value` e vanno chiamate **separatamente** da quelle a
  serie temporale (`reach`, `follower_count`).
- `website_clicks` non esiste più: i click sui link sono `profile_links_taps`.
- Il token Instagram scade dopo ~60 giorni: se `--check` segnala token non
  valido, rigeneralo da Meta for Developers.
