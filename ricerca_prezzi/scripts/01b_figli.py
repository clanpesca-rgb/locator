#!/usr/bin/env python3
"""01b: dalle pagine dei prodotti padre estrae gli SKU e i prezzi dei figli.
Output: dati/figli.csv (parent_id, sku_figlio, prezzo_figlio, nome_figlio).
Serve ad agganciare il gestionale (Codice/Barcode) alle famiglie del sito."""
import concurrent.futures as cf
import csv, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import fetch, gtm_products

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "dati", "figli.csv")

def main():
    padri = list(csv.DictReader(open(os.path.join(REPO, "dati", "catalogo_padri.csv"))))
    def work(p):
        h = fetch(p["url"])
        rows = []
        if h:
            for d in gtm_products(h):
                if d.get("item_list_name") == "Grouped Product Detail Page":
                    rows.append((p["id"], str(d.get("sku", "")).strip(),
                                 d.get("price"), d.get("item_name", "")))
            if not rows:  # prodotto semplice: lo sku e' del padre stesso
                for d in gtm_products(h):
                    if str(d.get("id")) == str(p["id"]):
                        rows.append((p["id"], str(d.get("sku", "")).strip(),
                                     d.get("price"), d.get("item_name", "")))
                        break
        return rows
    out, done = [], 0
    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        for rows in ex.map(work, padri):
            out.extend(rows)
            done += 1
            if done % 150 == 0:
                print(f"{done}/{len(padri)}")
    with open(OUT, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["parent_id", "sku", "prezzo", "nome"])
        w.writerows(out)
    print(f"scritto {OUT}: {len(out)} figli di {len(padri)} padri")

if __name__ == "__main__":
    main()
