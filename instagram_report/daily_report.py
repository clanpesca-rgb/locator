"""
Report Instagram giornaliero per Clan Pesca.

Uso:
    python daily_report.py            → genera il report e lo invia via email
    python daily_report.py --check    → modalità diagnostica: testa ogni pezzo
                                        (token IG, insights, chiave Claude, SMTP)
                                        e dice esattamente cosa funziona e cosa no

Le credenziali NON stanno nel codice: vanno nel file .env accanto a questo
script (vedi .env.example).
"""

import json
import os
import smtplib
import sys
import traceback
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

import requests
import anthropic
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

IG_TOKEN = os.environ.get("IG_TOKEN", "")
IG_USER_ID = os.environ.get("IG_USER_ID", "")
CLAUDE_API_KEY = os.environ.get("CLAUDE_API_KEY", "")
EMAIL_MITTENTE = os.environ.get("EMAIL_MITTENTE", "")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD", "")  # Password per le app di Gmail, NON la password normale
EMAIL_DESTINATARIO = os.environ.get("EMAIL_DESTINATARIO", EMAIL_MITTENTE)

BASE = "https://graph.instagram.com/v21.0"

MESI_IT = ["", "gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno",
           "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre"]


def oggi_italiano():
    ora = datetime.now()
    return f"{ora.day} {MESI_IT[ora.month]} {ora.year}"


def _get(url, params):
    """GET con gestione errori: ritorna sempre un dict, mai un'eccezione di rete non spiegata."""
    try:
        r = requests.get(url, params=params, timeout=30)
        return r.json()
    except Exception as e:
        return {"error": {"message": f"Errore di rete: {e}"}}


# ---------------------------------------------------------------------------
# DATI INSTAGRAM
# ---------------------------------------------------------------------------

def get_instagram_data():
    """Metriche account. Le metriche 'total_value' e quelle a serie temporale
    NON possono stare nella stessa chiamata: per questo sono separate."""
    dati = {}

    # Serie temporali (valore per giorno)
    dati["reach_giornaliero"] = _get(f"{BASE}/{IG_USER_ID}/insights", {
        "metric": "reach",
        "period": "day",
        "access_token": IG_TOKEN,
    })

    dati["follower_count"] = _get(f"{BASE}/{IG_USER_ID}/insights", {
        "metric": "follower_count",
        "period": "day",
        "access_token": IG_TOKEN,
    })

    # Metriche che richiedono metric_type=total_value
    dati["metriche_totali"] = _get(f"{BASE}/{IG_USER_ID}/insights", {
        "metric": "profile_views,accounts_engaged,total_interactions,profile_links_taps",
        "period": "day",
        "metric_type": "total_value",
        "access_token": IG_TOKEN,
    })

    # Numero follower attuale (non insight, campo diretto del profilo)
    dati["profilo"] = _get(f"{BASE}/{IG_USER_ID}", {
        "fields": "username,followers_count,media_count",
        "access_token": IG_TOKEN,
    })

    return dati


def get_media_insights(media_id):
    """Insights del singolo post/reel. NB: la metrica si chiama 'saved', non 'saves'."""
    dati = _get(f"{BASE}/{media_id}/insights", {
        "metric": "views,reach,saved,shares,likes,comments,total_interactions",
        "access_token": IG_TOKEN,
    })
    if "error" in dati:
        # alcuni tipi di media accettano meno metriche: riprova con set ridotto
        dati = _get(f"{BASE}/{media_id}/insights", {
            "metric": "reach,saved,shares",
            "access_token": IG_TOKEN,
        })

    risultato = {}
    for m in dati.get("data", []):
        valori = m.get("values", [{}])
        risultato[m.get("name")] = valori[0].get("value") if valori else None

    if risultato:
        return risultato
    # Se anche il retry è fallito, riporta l'errore vero: il report deve
    # poterlo dire invece di mostrare N/D senza spiegazione.
    return {"errore": dati.get("error", {}).get("message", "sconosciuto")}


def get_recent_posts():
    """Ultimi 10 post con metriche complete per ciascuno."""
    dati = _get(f"{BASE}/{IG_USER_ID}/media", {
        "fields": "id,caption,like_count,comments_count,timestamp,media_type,media_product_type,permalink",
        "limit": 10,
        "access_token": IG_TOKEN,
    })
    for post in dati.get("data", []):
        post["insights"] = get_media_insights(post["id"])
    return dati


# ---------------------------------------------------------------------------
# ANALISI CON CLAUDE
# ---------------------------------------------------------------------------

def analizza_con_claude(dati_ig, post_recenti):
    client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
    oggi = oggi_italiano()
    messaggio = f"""
Sei il Social Media Manager e Data Analyst senior di Clan Pesca, negozio specializzato nella pesca sportiva.

Il tuo compito NON è descrivere i dati, ma prendere decisioni operative basate sulle evidenze.

Data di oggi: {oggi}

=========================
DATI DISPONIBILI
=========================

POST RECENTI (ultimi 10 con tutte le metriche; il campo "insights" di ogni post contiene views, reach, saved, shares)
{json.dumps(post_recenti, ensure_ascii=False, indent=2)}

METRICHE ACCOUNT
{json.dumps(dati_ig, ensure_ascii=False, indent=2)}

=========================
COME RAGIONARE
=========================

Ogni osservazione deve essere classificata mentalmente come:

• FATTO → supportato dai dati disponibili.
• IPOTESI → probabile ma non dimostrabile con i dati.
• AZIONE → decisione concreta da prendere.

Non confondere mai correlazione e causalità.

Evita frasi assolute come:

❌ "Le caption lunghe non funzionano."

Preferisci:

✅ "Nei dati disponibili i contenuti con caption più brevi hanno ottenuto performance superiori, ma non è possibile attribuire con certezza il risultato alla sola lunghezza della caption."

Se il campione di contenuti simili è inferiore a 5, specifica che la conclusione è preliminare.

Non drammatizzare variazioni di reach su una singola giornata.
Per parlare di trend servono almeno 7-14 giorni.

Confronta SEMPRE quando possibile: oggi, ieri, media ultimi 7 giorni, media ultimi 30 giorni.

Se alcuni dati non sono disponibili NON inventarli. Se un dato riporta un campo "errore", segnalalo come limite dei dati.

=========================
CONOSCENZA INSTAGRAM
=========================

REELS — importanza dei segnali:
1. Condivisioni
2. Watch Time
3. Percentuale di completamento
4. Salvataggi
5. Commenti
6. Like

Valuta quando possibile: hook dei primi 3 secondi, formato, durata, audio, testo nel video, copertina, CTA, tono.

Distribuzione:
FASE 1 → Follower
FASE 2 → Esplora / Suggeriti
FASE 3 → Distribuzione ampia / virale

Per ogni Reel prova a stimare la fase di distribuzione.

POST E CAROSELLI — segnali principali:
1. Salvataggi
2. Commenti
3. Condivisioni
4. Tempo di visualizzazione
5. Like

STORIES: strumento di retention e relazione, non indicatore principale della crescita.

=========================
OBIETTIVO DEL REPORT
=========================

Il report deve aiutare il titolare del negozio a rispondere rapidamente a tre domande:
1. Come sta andando il profilo?
2. Perché sta andando così?
3. Qual è la cosa più importante da fare oggi?

=========================
OUTPUT
=========================

Restituisci SOLO HTML, senza blocchi di codice markdown (niente ```).

Usa questo contenitore:

<div style="font-family:Arial,sans-serif;max-width:720px;margin:0 auto;color:#333;line-height:1.5;">

<div style="background:linear-gradient(135deg,#1a1a2e,#16213e);padding:30px;border-radius:12px;text-align:center;margin-bottom:25px;">
<h1 style="margin:0;color:#e94560;">📊 Report Instagram</h1>
<h2 style="margin-top:10px;color:white;">@clanpesca — {oggi}</h2>
</div>

SEZIONE 0 — 📅 PIANO OPERATIVO DEL GIORNO (la sezione più importante)

REEL DEL GIORNO: idea precisa, hook dei primi 3 secondi, caption (max 10 parole), 5-7 hashtag, orario consigliato, obiettivo (Reach/Engagement/Vendita), perché lo proponi sulla base dei dati.

STORIES: sondaggio, backstage, collegamento al Reel, domanda alla community.

AZIONE COMMERCIALE: una sola, concreta (es. Story con link diretto a un prodotto). Motiva sempre la scelta.

SEZIONE 1 — 📈 KPI DEL GIORNO
Tabella con: Reach, Interazioni, Visite profilo, Follower, Click sito. Confronto con ieri e quando possibile con media 7 giorni. Colori verde/arancione/rosso.

SEZIONE 2 — 🏆 TOP 3 CONTENUTI
Per ognuno: like, commenti, salvataggi, condivisioni. Analisi: perché probabilmente ha funzionato, elemento da replicare, elemento che NON può essere considerato automaticamente la causa del successo.

SEZIONE 3 — 🤖 ANALISI ALGORITMICA
Hook, formato, durata, CTA, audio, copertina. Stima fase di distribuzione: 🟢 in crescita / 🟡 rallentata / 🔴 terminata. Motiva.

SEZIONE 4 — 📊 PATTERN OSSERVATI
Solo elementi osservabili. Cosa accomuna i contenuti migliori. Distingui chiaramente FATTI e IPOTESI. Non attribuire mai il successo esclusivamente alla caption.

SEZIONE 5 — 💡 AZIONI PER I PROSSIMI 7 GIORNI
3 azioni misurabili, ognuna con: obiettivo, motivazione, KPI da osservare.

SEZIONE 6 — 🎣 MIX CONTENUTI CONSIGLIATO
50% intrattenimento relatable / 30% educazione con hook forte / 20% commerciale narrativo. Spiega perché.

SEZIONE 7 — ⚠️ ALERT
Solo se realmente presenti (es. 🔴 nessun Reel da tre giorni, 🟡 frequenza bassa, 🟢 nessun alert).

SEZIONE 8 — 🎯 KPI DA MONITORARE DOMANI
Massimo tre, motivati.

SEZIONE 9 — 📌 DASHBOARD DECISIONALE
Tabella riassuntiva finale: Il profilo è in salute? Serve pubblicare oggi? Quale contenuto pubblicare? Qual è il principale obiettivo? Quale errore evitare? Qual è la priorità assoluta di oggi?

SEZIONE 10 — ⭐ VALUTAZIONE
Voto 1-10 motivato con semaforo 🟢/🟡/🔴. Un profilo che genera contenuti con decine di migliaia di interazioni non dovrebbe ricevere meno di 7/10 solo per una giornata negativa.

STILE: titoli #e94560, positivo #27ae60, attenzione #f39c12, negativo #e74c3c. Ogni sezione con bordo sinistro colorato, padding, sfondo leggermente diverso, emoji nel titolo. Restituisci esclusivamente HTML valido.
"""
    response = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=16000,
        messages=[{"role": "user", "content": messaggio}],
    )
    testo = "".join(block.text for block in response.content if hasattr(block, "text"))

    # Se il modello avvolge comunque l'HTML in un blocco ```html ... ```, toglilo
    testo = testo.strip()
    if testo.startswith("```"):
        testo = testo.split("\n", 1)[1] if "\n" in testo else ""
        if testo.rstrip().endswith("```"):
            testo = testo.rstrip()[:-3]

    return testo if testo.strip() else "<p>Nessun dato disponibile</p>"


# ---------------------------------------------------------------------------
# EMAIL
# ---------------------------------------------------------------------------

def invia_email(report_html, oggetto=None):
    oggi = datetime.now().strftime("%d/%m/%Y")
    msg = MIMEMultipart("alternative")
    msg["Subject"] = oggetto or f"📊 Report Instagram Clan Pesca — {oggi}"
    msg["From"] = EMAIL_MITTENTE
    msg["To"] = EMAIL_DESTINATARIO

    html_completo = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="background-color: #f5f5f5; padding: 20px; margin: 0;">
        {report_html}
        <div style="text-align: center; margin-top: 20px; color: #999; font-size: 12px;">
            Report generato automaticamente da Claude AI per Clan Pesca
        </div>
    </body>
    </html>
    """

    msg.attach(MIMEText(html_completo, "html", "utf-8"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_MITTENTE, EMAIL_PASSWORD)
        server.send_message(msg)
    print("Report inviato!")


def invia_email_errore(errore_testo):
    """Se il report fallisce, prova comunque ad avvisarti via email:
    meglio una mail d'errore che il silenzio."""
    try:
        invia_email(
            f"<pre style='font-family:monospace'>{errore_testo}</pre>",
            oggetto="⚠️ Report Instagram Clan Pesca — ERRORE",
        )
    except Exception:
        print("Impossibile inviare anche la mail di errore (problema SMTP?).")


# ---------------------------------------------------------------------------
# MODALITÀ DIAGNOSTICA
# ---------------------------------------------------------------------------

def check():
    """Testa ogni componente separatamente e dice cosa funziona."""
    ok = True

    print("1) Variabili d'ambiente (.env)...")
    for nome in ["IG_TOKEN", "IG_USER_ID", "CLAUDE_API_KEY", "EMAIL_MITTENTE", "EMAIL_PASSWORD"]:
        if os.environ.get(nome):
            print(f"   ✅ {nome} presente")
        else:
            print(f"   ❌ {nome} MANCANTE — aggiungilo al file .env")
            ok = False

    print("\n2) Token Instagram...")
    profilo = _get(f"{BASE}/{IG_USER_ID}", {
        "fields": "username,followers_count,media_count",
        "access_token": IG_TOKEN,
    })
    if "error" in profilo:
        print(f"   ❌ Errore: {profilo['error'].get('message')}")
        print("      → Controlla che il token sia valido e non scaduto (i token durano ~60 giorni).")
        ok = False
    else:
        print(f"   ✅ Connesso come @{profilo.get('username')} "
              f"({profilo.get('followers_count')} follower, {profilo.get('media_count')} post)")

    print("\n3) Insights account...")
    dati = get_instagram_data()
    for chiave, valore in dati.items():
        if "error" in valore:
            print(f"   ❌ {chiave}: {valore['error'].get('message')}")
            ok = False
        else:
            print(f"   ✅ {chiave}: ok")

    print("\n4) Insights di un post recente...")
    media = _get(f"{BASE}/{IG_USER_ID}/media", {"fields": "id,media_type", "limit": 1, "access_token": IG_TOKEN})
    lista = media.get("data", [])
    if not lista:
        print(f"   ❌ Impossibile leggere i post: {media.get('error', {}).get('message', 'nessun post')}")
        ok = False
    else:
        ins = get_media_insights(lista[0]["id"])
        if "errore" in ins:
            print(f"   ❌ Errore insights sul post: {ins['errore']}")
            ok = False
        else:
            print(f"   ✅ Metriche disponibili: {', '.join(ins.keys())}")

    print("\n5) Chiave API Claude...")
    try:
        client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
        client.messages.create(model="claude-haiku-4-5-20251001", max_tokens=10,
                               messages=[{"role": "user", "content": "ok"}])
        print("   ✅ Chiave Claude valida")
    except Exception as e:
        print(f"   ❌ Errore Claude: {e}")
        ok = False

    print("\n6) Login SMTP Gmail...")
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_MITTENTE, EMAIL_PASSWORD)
        print("   ✅ Login Gmail riuscito")
    except smtplib.SMTPAuthenticationError:
        print("   ❌ Login Gmail RIFIUTATO.")
        print("      → Serve una 'Password per le app' (16 caratteri), NON la password normale.")
        print("      → Account Google → Sicurezza → Verifica in due passaggi → Password per le app.")
        ok = False
    except Exception as e:
        print(f"   ❌ Errore SMTP: {e}")
        ok = False

    print("\n" + ("🟢 Tutto ok: puoi lanciare il report." if ok else "🔴 Sistema i punti ❌ e rilancia --check."))
    return ok


# ---------------------------------------------------------------------------

if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(0 if check() else 1)

    try:
        print("Recupero dati Instagram...")
        dati = get_instagram_data()
        post = get_recent_posts()
        print("Dati recuperati, analisi in corso...")
        report = analizza_con_claude(dati, post)
        invia_email(report)
    except Exception:
        errore = traceback.format_exc()
        print(errore)
        invia_email_errore(errore)
        sys.exit(1)
