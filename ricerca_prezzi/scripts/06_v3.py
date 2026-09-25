#!/usr/bin/env python3
"""06: costruisce il confronto v3 = v2 + verifiche EAN + ricerca EAN + margini.

- dati/confronto_v3.csv: completo, con colonne margine (resta nell'area di lavoro).
- confronto_famiglie.csv (repo): versione SENZA dati di acquisto/margine.
Livelli finali: ean > esatto > ean_ricerca > famiglia > probabile > possibile.
Le righe 'ean_ricerca' senza marca nello slug diventano 'dubbio' (escluse dalle statistiche).
"""
import csv, os, statistics, sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import norm

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRATCH = os.environ.get("RICERCA_SCRATCH", "/tmp/claude-0/-home-user-locator/c6da37d9-3fe5-53b8-8609-51ea49daf62e/scratchpad")
RANK = {"ean": 0, "esatto": 1, "ean_ricerca": 2, "famiglia": 3, "probabile": 4, "possibile": 5, "dubbio": 9}

def main():
    padri = {p["id"]: p for p in csv.DictReader(open(os.path.join(REPO, "dati", "catalogo_padri.csv")))}
    # margini per padre dal gestionale (via figli)
    sku2p = {r["sku"].strip().upper(): r["parent_id"]
             for r in csv.DictReader(open(os.path.join(REPO, "dati", "figli.csv"))) if r["sku"]}
    acq, ric = defaultdict(list), defaultdict(list)
    for r in csv.DictReader(open(os.path.join(SCRATCH, "gestionale.csv"))):
        pid = sku2p.get(str(r["Codice"]).strip().upper())
        if not pid:
            continue
        try:
            a, v = float(r["Prezzo Acq."]), float(r["Prezzo Vend."])
            if a > 0 and v > 0:
                acq[pid].append(a)
                ric[pid].append((v - a) / v * 100)
        except (TypeError, ValueError):
            pass

    rows = []
    # v2 con verifiche
    for r in csv.DictReader(open(os.path.join(REPO, "dati", "ean_verifica.csv"))):
        pid, lvl = r["id"], r["livello_match"]
        ver = r.get("verifica_ean", "")
        if ver == "confermato_ean":
            lvl = "ean"
        elif ver.startswith("riassegna:"):
            pid, lvl = ver.split(":", 1)[1], "ean"
        if pid not in padri:
            continue
        rows.append({"pid": pid, "sito": r["sito"], "livello": lvl,
                     "prezzo": float(r["prezzo_concorrente"]),
                     "conc_da": r["conc_da"], "conc_a": r["conc_a"],
                     "disp": r["disponibilita_concorrente"], "url": r["url_concorrente"]})
    # ricerca EAN
    for r in csv.DictReader(open(os.path.join(REPO, "dati", "ean_ricerca.csv"))):
        pid = r["parent_id"]
        if pid not in padri:
            continue
        lvl = r["livello"]
        if lvl == "ean_ricerca":
            marca_tok = [t for t in padri[pid]["marca"].replace("-", " ").split() if len(t) >= 3]
            slug = norm(r["url"]).replace(" ", "")
            if marca_tok and not all(t in slug for t in marca_tok):
                lvl = "dubbio"
        rows.append({"pid": pid, "sito": r["sito"], "livello": lvl, "prezzo": float(r["prezzo"]),
                     "conc_da": r["conc_da"], "conc_a": r["conc_a"], "disp": r["disp"], "url": r["url"]})

    # sanity prezzo + dedupe (pid, sito)
    best = {}
    for r in rows:
        p = padri[r["pid"]]
        try:
            da, a = float(p["prezzo_da"]), float(p["prezzo_a"])
        except ValueError:
            continue
        mid = (da + a) / 2
        if r["livello"] not in ("ean",) and not (0.25 <= mid / r["prezzo"] <= 4.0):
            continue
        k = (r["pid"], r["sito"])
        key = (RANK[r["livello"]], r["prezzo"])
        if k not in best or key < (RANK[best[k]["livello"]], best[k]["prezzo"]):
            best[k] = r

    out = []
    for (pid, sito), r in sorted(best.items()):
        p = padri[pid]
        da, a, pv = float(p["prezzo_da"]), float(p["prezzo_a"]), r["prezzo"]
        if pv < da:
            pos, delta = "cp_piu_caro", (da - pv) / pv * 100
        elif pv > a:
            pos, delta = "cp_piu_economico", (a - pv) / pv * 100
        else:
            pos, delta = "in_fascia", 0.0
        am = statistics.median(acq[pid]) if acq.get(pid) else None
        rm = statistics.median(ric[pid]) if ric.get(pid) else None
        m_all = (pv - am) / pv * 100 if (am and pv) else None
        out.append({
            "id": pid, "marca": p["marca"], "prodotto": p["nome"], "categoria": p["categoria"],
            "cp_prezzo_da": f"{da:.2f}", "cp_prezzo_a": f"{a:.2f}", "sito": sito,
            "livello_match": r["livello"], "prezzo_concorrente": f"{pv:.2f}",
            "conc_da": r["conc_da"], "conc_a": r["conc_a"],
            "disponibilita_concorrente": r["disp"], "posizione": pos, "delta_pct": f"{delta:+.1f}",
            "margine_attuale_pct": f"{rm:.1f}" if rm is not None else "",
            "margine_se_allineato_pct": f"{m_all:.1f}" if m_all is not None else "",
            "url_concorrente": r["url"], "url_clanpesca": p["url"],
        })
    with open(os.path.join(REPO, "dati", "confronto_v3.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)
    # versione repo senza margini
    pub_fields = [k for k in out[0] if not k.startswith("margine_")]
    with open(os.path.join(REPO, "confronto_famiglie.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=pub_fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(out)

    valide = [r for r in out if r["livello_match"] != "dubbio"]
    fam = len({r["id"] for r in valide})
    per_lvl = defaultdict(int)
    for r in out:
        per_lvl[r["livello_match"]] += 1
    print(f"v3: {len(out)} righe totali | valide: {len(valide)} su {fam} famiglie | livelli: {dict(per_lvl)}")

if __name__ == "__main__":
    main()
