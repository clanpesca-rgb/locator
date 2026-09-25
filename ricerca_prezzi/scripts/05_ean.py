#!/usr/bin/env python3
"""05: integrazione EAN dal gestionale.

  python3 05_ean.py verify  -> verifica/riassegna i match esistenti leggendo i gtin
                               dalle pagine concorrenti gia' individuate
  python3 05_ean.py search  -> ricerca per EAN sui siti interrogabili per i padri
                               ancora senza confronto

Prerequisiti: dati/figli.csv (01b), gestionale.csv nello scratchpad (upload del
titolare: MAI committare, contiene prezzi di acquisto), dati/confronto_v2.csv.
Output: dati/ean_verifica.csv, dati/ean_ricerca.csv
"""
import concurrent.futures as cf
import csv, json, os, re, sys, urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import extract_offer, fetch

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRATCH = os.environ.get("RICERCA_SCRATCH", "/tmp/claude-0/-home-user-locator/c6da37d9-3fe5-53b8-8609-51ea49daf62e/scratchpad")

GTIN_RE = re.compile(r'(?:"gtin1?[234]?"|"ean1?3?"|itemprop="gtin1?3?"[^>]*content="|EAN\s*1?3?\s*[:\s]|barcode\D{0,10})\s*"?(\d{12,14})', re.I)

def ean_maps():
    """EAN reale -> parent_id e parent_id -> [EAN]."""
    sku2parent = {}
    for r in csv.DictReader(open(os.path.join(REPO, "dati", "figli.csv"))):
        if r["sku"]:
            sku2parent[r["sku"].strip().upper()] = r["parent_id"]
    ean2parent, parent2ean = {}, {}
    for r in csv.DictReader(open(os.path.join(SCRATCH, "gestionale.csv"))):
        if r.get("tipo_ean") != "reale":
            continue
        pid = sku2parent.get(str(r["Codice"]).strip().upper())
        if not pid:
            continue
        ean = str(r["Barcode"]).strip()
        ean2parent[ean] = pid
        parent2ean.setdefault(pid, []).append(ean)
    return ean2parent, parent2ean

def gtins_of(page_html):
    out = set()
    for m in GTIN_RE.finditer(page_html):
        g = m.group(1)
        if len(g) == 14 and g.startswith("0"):
            g = g[1:]
        if len(g) in (12, 13):
            out.add(g)
    return out

def cmd_verify():
    ean2parent, parent2ean = ean_maps()
    print(f"mappa: {len(ean2parent)} EAN su {len(parent2ean)} padri")
    rows = list(csv.DictReader(open(os.path.join(REPO, "dati", "confronto_v2.csv"))))
    urls = sorted({r["url_concorrente"] for r in rows if r["url_concorrente"]})
    print(f"pagine da verificare: {len(urls)}")
    res, done = {}, 0
    def work(u):
        h = fetch(u)
        return u, (gtins_of(h) if h else set())
    with cf.ThreadPoolExecutor(max_workers=10) as ex:
        for u, gs in ex.map(work, urls):
            res[u] = gs
            done += 1
            if done % 100 == 0:
                print(f"  {done}/{len(urls)}")
    out, conf, reass, nogtin = [], 0, 0, 0
    for r in rows:
        gs = res.get(r["url_concorrente"], set())
        owners = {ean2parent[g] for g in gs if g in ean2parent}
        esito = ""
        if not gs:
            nogtin += 1
        elif r["id"] in owners:
            esito, conf = "confermato_ean", conf + 1
        elif owners:
            esito, reass = "riassegna:" + sorted(owners)[0], reass + 1
        out.append({**r, "verifica_ean": esito, "gtin_pagina": ";".join(sorted(gs)[:3])})
    with open(os.path.join(REPO, "dati", "ean_verifica.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)
    print(f"confermati via EAN: {conf} | da riassegnare: {reass} | pagine senza gtin leggibile: {nogtin}")

SEARCH_SITES = {
    "megafish.it": ("https://www.megafish.it/module/iqitsearch/searchiqit?s={q}&ajax=true", "iqit"),
    "escaepescashop.it": ("https://escaepescashop.it/?s={q}&post_type=product", "woo"),
    "webpesca.it": ("https://www.webpesca.it/?s={q}&post_type=product", "woo"),
    "propesca.it": ("https://propesca.it/?s={q}&post_type=product", "woo"),
    "fishingitalia.com": ("https://www.fishingitalia.com/?s={q}&post_type=product", "woo"),
    "marlinblue.it": ("https://www.marlinblue.it/?s={q}&post_type=product", "woo"),
    "sampey.it": ("https://www.sampey.it/ricerca?controller=search&s={q}", "presta"),
    "dimensionepesca.com": ("https://www.dimensionepesca.com/it/ricerca?controller=search&s={q}", "presta"),
}
PRODUCT_HREF = re.compile(r'href="(https?://[^"]+(?:/prodotto/|/shop/|/negozio/|\d+-[a-z0-9-]+\.html)[^"]*)"', re.I)

def cmd_search():
    ean2parent, parent2ean = ean_maps()
    have = {r["id"] for r in csv.DictReader(open(os.path.join(REPO, "dati", "confronto_v2.csv")))}
    padri = {p["id"]: p for p in csv.DictReader(open(os.path.join(REPO, "dati", "catalogo_padri.csv")))}
    targets = [(pid, eans[0]) for pid, eans in parent2ean.items() if pid not in have and pid in padri]
    print(f"padri scoperti con EAN reale: {len(targets)}")
    jobs = [(pid, ean, dom) for pid, ean in targets for dom in SEARCH_SITES]
    print(f"query di ricerca EAN: {len(jobs)}")
    def work(job):
        pid, ean, dom = job
        tmpl, kind = SEARCH_SITES[dom]
        h = fetch(tmpl.format(q=urllib.parse.quote_plus(ean)), tries=1, timeout=25)
        if not h:
            return None
        links = []
        if kind == "iqit":
            try:
                for it in (json.loads(h).get("products") or [])[:3]:
                    links.append((it.get("link", ""), it.get("price_amount")))
            except Exception:
                pass
        else:
            seen = set()
            for m in PRODUCT_HREF.finditer(h):
                u = m.group(1)
                if dom.split(".")[0] not in u:
                    continue
                if u not in seen and "?s=" not in u and "add-to-cart" not in u:
                    seen.add(u)
                    links.append((u, None))
                if len(links) >= 2:
                    break
        return (pid, ean, dom, links) if links else None
    hits, done = [], 0
    with cf.ThreadPoolExecutor(max_workers=10) as ex:
        for r in ex.map(work, jobs):
            done += 1
            if r:
                hits.append(r)
            if done % 500 == 0:
                print(f"  query {done}/{len(jobs)} (hit finora: {len(hits)})")
    print(f"hit ricerca: {len(hits)}")
    # verifica pagine trovate
    out = []
    def page(job):
        pid, ean, dom, links = job
        rows = []
        for u, pr in links:
            h = fetch(u, tries=1, timeout=30)
            if not h:
                continue
            price, low, high, avail = extract_offer(h)
            pv = price if price is not None else (low if low is not None else pr)
            if pv is None:
                continue
            gs = gtins_of(h)
            lvl = "ean" if any(ean2parent.get(g) == pid for g in gs) else "ean_ricerca"
            rows.append({"parent_id": pid, "sito": dom, "url": u, "prezzo": f"{float(pv):.2f}",
                         "conc_da": f"{low:.2f}" if low else "", "conc_a": f"{high:.2f}" if high else "",
                         "disp": avail or "", "livello": lvl, "ean_usato": ean})
            break  # basta la prima pagina valida per sito
        return rows
    with cf.ThreadPoolExecutor(max_workers=10) as ex:
        for rows in ex.map(page, hits):
            out.extend(rows)
    with open(os.path.join(REPO, "dati", "ean_ricerca.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["parent_id", "sito", "url", "prezzo", "conc_da", "conc_a", "disp", "livello", "ean_usato"])
        w.writeheader()
        w.writerows(out)
    prodotti = len({r["parent_id"] for r in out})
    print(f"scritto dati/ean_ricerca.csv: {len(out)} righe, {prodotti} padri recuperati")

if __name__ == "__main__":
    {"verify": cmd_verify, "search": cmd_search}[sys.argv[1]]()
