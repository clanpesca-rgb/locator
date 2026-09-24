#!/usr/bin/env python3
"""01: Catalogo Clan Pesca a livello di PRODOTTO PADRE con fascia di prezzo da-a.

Fase A: pagine marca (sitemap ts_product_brand) -> lista padri.
Fase B: pagina di ogni padre -> prezzi dei figli collegati -> fascia min-max.
Esclusioni concordate col titolare: marchio Shimano, categoria Tuning.
Output: ricerca_prezzi/dati/catalogo_padri.csv
"""
import concurrent.futures as cf
import csv, os, sys, time, urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import LOC_RE, fetch, gtm_products

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "dati", "catalogo_padri.csv")
ESCLUSI_BRAND = {"shimano"}
ESCLUSE_CAT = {"tuning"}

def fase_a():
    xml = fetch("https://clanpesca.com/product_brand-sitemap.xml")
    brand_urls = [u for u in LOC_RE.findall(xml) if "/marchio/" in u]
    padri, seen = [], set()
    for burl in brand_urls:
        slug = burl.rstrip("/").rsplit("/", 1)[-1]
        if slug in ESCLUSI_BRAND:
            continue
        page = 1
        while True:
            u = (burl if page == 1 else f"{burl}page/{page}/") + "?per_page=100"
            h = fetch(u)
            if not h:
                break
            got = 0
            for d in gtm_products(h):
                pid = d.get("id")
                if pid in seen or not d.get("productlink"):
                    continue
                got += 1
                seen.add(pid)
                padri.append({
                    "id": pid, "marca": slug, "nome": d.get("item_name", "").strip(),
                    "categoria": d.get("item_category", ""), "tipo": d.get("product_type", ""),
                    "prezzo_listing": d.get("price"), "stock_listing": d.get("stockstatus", ""),
                    "url": d.get("productlink", ""),
                })
            if not got or f"/page/{page+1}/" not in h:
                break
            page += 1
            time.sleep(0.25)
        time.sleep(0.25)
    padri = [p for p in padri if p["categoria"].strip().lower() not in ESCLUSE_CAT]
    print(f"fase A: {len(padri)} padri ({len(brand_urls)} marche, esclusi Shimano/Tuning)")
    return padri

def fase_b(padri):
    def work(p):
        h = fetch(p["url"])
        if not h:
            return p, None, []
        figli = [d for d in gtm_products(h) if d.get("item_list_name") == "Grouped Product Detail Page"]
        prezzi = []
        for d in figli:
            try:
                v = float(d.get("price"))
                if v > 0:
                    prezzi.append(v)
            except (TypeError, ValueError):
                pass
        return p, len(figli), prezzi
    rows, done = [], 0
    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        for p, nfigli, prezzi in ex.map(work, padri):
            try:
                base = float(p["prezzo_listing"])
            except (TypeError, ValueError):
                base = None
            if prezzi:
                pmin, pmax = min(prezzi), max(prezzi)
            elif base and base > 0:
                pmin = pmax = base
            else:
                pmin = pmax = None
            rows.append({
                "id": p["id"], "marca": p["marca"], "nome": p["nome"], "categoria": p["categoria"],
                "tipo": p["tipo"], "n_varianti": nfigli or 0,
                "prezzo_da": f"{pmin:.2f}" if pmin else "",
                "prezzo_a": f"{pmax:.2f}" if pmax else "",
                "url": p["url"],
            })
            done += 1
            if done % 100 == 0:
                print(f"  fase B: {done}/{len(padri)}")
    return rows

def main():
    padri = fase_a()
    rows = fase_b(padri)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    con_fascia = sum(1 for r in rows if r["prezzo_da"] and r["prezzo_da"] != r["prezzo_a"])
    print(f"scritto {OUT}: {len(rows)} padri, {con_fascia} con fascia da-a reale")

if __name__ == "__main__":
    main()
