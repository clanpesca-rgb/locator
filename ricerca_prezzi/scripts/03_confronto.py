#!/usr/bin/env python3
"""03: Confronto a livello di FAMIGLIA (prodotto padre) con i prezzi trovati sul web.

- La disponibilita' viene registrata ma NON filtra nulla (richiesta del titolare).
- Livelli di match: esatto (nome+numeri), probabile (numeri ambigui), famiglia
  (nome senza numeri), possibile (numeri non riscontrati nell'URL).
- Prezzo concorrente: dalla pagina prodotto (JSON-LD); se la pagina espone una
  fascia (lowPrice/highPrice) viene registrata anche quella.
Output: ricerca_prezzi/dati/confronto_v2.csv
"""
import concurrent.futures as cf
import csv, json, os, re, sys, time, urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import extract_offer, fetch, norm, tokens_of

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRATCH = os.environ.get("RICERCA_SCRATCH", "/tmp/claude-0/-home-user-locator/c6da37d9-3fe5-53b8-8609-51ea49daf62e/scratchpad")
SMDIR = os.path.join(SCRATCH, "sitemaps")
OUT = os.path.join(REPO, "dati", "confronto_v2.csv")
MAX_PER_SITE = 3

def num_score(n, toks):
    cands = {n, n.replace(".", "")}
    dec = n.replace(".", " ").split() if "." in n else None
    best = 0
    for i, t in enumerate(toks):
        if dec and toks[i:i + len(dec)] == dec:
            return 2
        if t in cands:
            nxt = toks[i + 1] if i + 1 < len(toks) else ""
            prv = toks[i - 1] if i > 0 else ""
            if "." not in n and (re.fullmatch(r"[0-9]", nxt) or re.fullmatch(r"[0-9]", prv)):
                best = max(best, 1)
            else:
                return 2
    return best

def livello(words_ok, nums, toks):
    if not words_ok:
        return None
    if not nums:
        return "famiglia"
    sc = [num_score(n, toks) for n in nums]
    if any(s == 0 for s in sc):
        return "possibile"
    return "esatto" if all(s == 2 for s in sc) else "probabile"

RANK = {"esatto": 0, "famiglia": 1, "probabile": 2, "possibile": 3}

def match_pre(pre, text):
    """livello di match tra un padre pre-tokenizzato e un testo (slug o nome)."""
    words, nums, brand_toks = pre
    t = norm(text)
    toks = t.split()
    tc = t.replace(" ", "")
    if brand_toks and not all(b in tc for b in brand_toks):
        return None
    words_ok = all((f" {w} " in f" {t} ") or (len(w) >= 4 and w in tc) for w in words)
    return livello(words_ok, nums, toks)

def pre_of(padre):
    words, nums = tokens_of(padre["nome"])
    brand_toks = [b for b in padre["marca"].replace("-", " ").split() if len(b) >= 3]
    return (words, nums, brand_toks)

def match_text(padre, text):
    return match_pre(pre_of(padre), text)

def slug_of(url):
    return re.sub(r"[^a-z0-9]+", " ", norm(urllib.parse.unquote(url.split("//", 1)[-1].split("/", 1)[-1])))

def main():
    padri = [p for p in csv.DictReader(open(os.path.join(REPO, "dati", "catalogo_padri.csv"))) if p["prezzo_da"]]
    print(f"padri con prezzo: {len(padri)}")
    sitemaps = {}
    for fn in sorted(os.listdir(SMDIR)):
        if fn.startswith("sitemap_"):
            dom = fn[len("sitemap_"):-len(".txt")]
            urls = [u for u in open(os.path.join(SMDIR, fn)).read().splitlines() if u.strip()]
            sitemaps[dom] = [(u, slug_of(u)) for u in urls]
            print(f"  {dom}: {len(urls)} url")

    # --- canale sitemap (pre-indicizzato per marca: match solo sugli URL che citano la marca)
    brands = sorted({p["marca"] for p in padri})
    brand_toks_by = {b: [x for x in b.replace("-", " ").split() if len(x) >= 3] for b in brands}
    index = {}  # (dom, marca) -> [(url, slug)]
    for dom, urls in sitemaps.items():
        for u, slug in urls:
            sc = slug.replace(" ", "")
            for b, bt in brand_toks_by.items():
                if bt and all(x in sc for x in bt):
                    index.setdefault((dom, b), []).append((u, slug))
    cand = []
    for p in padri:
        pre = pre_of(p)
        for dom in sitemaps:
            hits = []
            for u, slug in index.get((dom, p["marca"]), []):
                lv = match_pre(pre, slug)
                if lv:
                    hits.append((RANK[lv], len(slug), lv, u))
            hits.sort()
            for _, _, lv, u in hits[:MAX_PER_SITE]:
                cand.append({"padre": p, "sito": dom, "livello": lv, "url": u})
    print(f"candidati sitemap: {len(cand)}")

    # --- canale megafish API
    cache = {}
    mf = 0
    for i, p in enumerate(padri):
        words, _ = tokens_of(p["nome"])
        if not words:
            continue
        q = " ".join(words[:4])
        if q not in cache:
            u = "https://www.megafish.it/module/iqitsearch/searchiqit?s=" + urllib.parse.quote_plus(q) + "&ajax=true"
            h = fetch(u)
            try:
                cache[q] = json.loads(h).get("products") or []
            except Exception:
                cache[q] = []
            time.sleep(0.2)
        for it in cache[q][:20]:
            lv = match_text(p, it.get("name", ""))
            if not lv:
                continue
            pr = it.get("price_amount")
            if pr is None:
                continue
            cand.append({"padre": p, "sito": "megafish.it", "livello": lv,
                         "url": it.get("link", ""), "prezzo": float(pr), "disp": ""})
            mf += 1
        if (i + 1) % 200 == 0:
            print(f"  megafish {i+1}/{len(padri)}")
    print(f"candidati megafish: {mf}")

    # --- fetch pagine candidate (solo quelle senza prezzo)
    to_fetch = sorted({c["url"] for c in cand if "prezzo" not in c and c["url"]})
    print(f"pagine da scaricare: {len(to_fetch)}")
    res, done = {}, 0
    def work(u):
        h = fetch(u)
        return u, (extract_offer(h) if h else (None, None, None, None))
    with cf.ThreadPoolExecutor(max_workers=10) as ex:
        for u, off in ex.map(work, to_fetch):
            res[u] = off
            done += 1
            if done % 200 == 0:
                print(f"  pagine {done}/{len(to_fetch)}")

    # --- righe finali, dedupe (padre, sito) tenendo livello migliore poi prezzo minore
    best = {}
    for c in cand:
        p = c["padre"]
        if "prezzo" in c:
            prezzo, low, high, disp = c["prezzo"], None, None, c.get("disp", "")
        else:
            prezzo, low, high, disp = res.get(c["url"], (None, None, None, None))
        pv = prezzo if prezzo is not None else low
        if pv is None:
            continue
        cp_da, cp_a = float(p["prezzo_da"]), float(p["prezzo_a"])
        mid = (cp_da + cp_a) / 2
        if not (0.25 <= mid / pv <= 4.0):
            continue
        k = (p["id"], c["sito"])
        rec = (RANK[c["livello"]], pv, c, prezzo, low, high, disp)
        if k not in best or rec[:2] < best[k][:2]:
            best[k] = rec
    rows = []
    for (pid, sito), (rk, pv, c, prezzo, low, high, disp) in sorted(best.items(), key=lambda kv: kv[0]):
        p = c["padre"]
        cp_da, cp_a = float(p["prezzo_da"]), float(p["prezzo_a"])
        if pv < cp_da:
            pos, delta = "cp_piu_caro", (cp_da - pv) / pv * 100
        elif pv > cp_a:
            pos, delta = "cp_piu_economico", (cp_a - pv) / pv * 100
        else:
            pos, delta = "in_fascia", 0.0
        rows.append({
            "id": pid, "marca": p["marca"], "prodotto": p["nome"], "categoria": p["categoria"],
            "cp_prezzo_da": f"{cp_da:.2f}", "cp_prezzo_a": f"{cp_a:.2f}",
            "sito": sito, "livello_match": c["livello"],
            "prezzo_concorrente": f"{pv:.2f}",
            "conc_da": f"{low:.2f}" if low else "", "conc_a": f"{high:.2f}" if high else "",
            "disponibilita_concorrente": disp or "", "posizione": pos,
            "delta_pct": f"{delta:+.1f}", "url_concorrente": c["url"], "url_clanpesca": p["url"],
        })
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    prodotti = len({r["id"] for r in rows})
    print(f"scritto {OUT}: {len(rows)} righe su {prodotti} prodotti padre")

if __name__ == "__main__":
    main()
