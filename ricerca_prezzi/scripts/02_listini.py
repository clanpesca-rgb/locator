#!/usr/bin/env python3
"""02: Scarica le liste prodotti (sitemap) dei concorrenti verificabili.

Un file per sito in <scratch>/sitemaps/sitemap_<dominio>.txt.
Note operative apprese nella rilevazione di agosto 2026:
- bestpesca, misterfish, pescafishingshop usano <loc> con CDATA;
- misterfish/pescafishingshop: sub-sitemap 1_it_0_sitemap.xml, URL in http:// (forzare https)
  e per misterfish dominio storico pescaecacciastore.com da riscrivere;
- mondo-pesca.it e' diventato escaepescashop.it;
- bassstore: /sitemaps/sitemap-1-it-products-1.xml.
Siti con bot-wall (non scaricabili): pescaloccasione, decathlon, marcosportshop,
amazon, trovaprezzi, idealo, free-fishing.
"""
import concurrent.futures as cf
import os, re, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import LOC_RE, fetch

SCRATCH = os.environ.get("RICERCA_SCRATCH", "/tmp/claude-0/-home-user-locator/c6da37d9-3fe5-53b8-8609-51ea49daf62e/scratchpad")
OUTDIR = os.path.join(SCRATCH, "sitemaps")

def to_https(u):
    return "https://" + u.split("://", 1)[1] if "://" in u else u

def from_robots(base):
    rob = fetch(base + "robots.txt")
    return [to_https(u) for u in re.findall(r"(?im)^sitemap:\s*(\S+)", rob)]

def expand(roots, cap_urls=60000, keep=None):
    urls, seen, queue, depth = set(), set(), list(dict.fromkeys(roots))[:10], 0
    while queue and depth < 3 and len(urls) < cap_urls:
        nxt = []
        for sm in queue:
            if sm in seen:
                continue
            seen.add(sm)
            xml = fetch(sm)
            if not xml:
                continue
            ls = [to_https(u) for u in LOC_RE.findall(xml)]
            if "<sitemapindex" in xml:
                prod = [l for l in ls if re.search(r"product|prodott", l, re.I)]
                nxt += (prod or ls)[:40]
            else:
                urls.update(ls)
            time.sleep(0.2)
        queue, depth = nxt, depth + 1
    if keep:
        urls = {u for u in urls if keep(u)}
    return sorted(urls)

def site_generic(domain):
    return expand(from_robots(f"https://www.{domain}/") or [f"https://www.{domain}/sitemap.xml"])

SPECIAL = {
    "bassstoreitaly.com": lambda: expand(["https://bassstoreitaly.com/sitemaps/sitemap-1-it-products-1.xml"]),
    "bestpesca.com": lambda: expand(["https://www.bestpesca.com/sitemap.xml"]),
    "misterfish.shop": lambda: [u.replace("pescaecacciastore.com", "misterfish.shop")
                                for u in expand(["https://www.misterfish.shop/1_it_0_sitemap.xml"])],
    "pescafishingshop.com": lambda: expand(["https://www.pescafishingshop.com/1_it_0_sitemap.xml"]),
    "escaepescashop.it": lambda: expand(from_robots("https://escaepescashop.it/") or ["https://escaepescashop.it/sitemap_index.xml"]),
}
GENERIC = ["pescapromo.it", "webpesca.it", "pescamia.eu", "fishingitalia.com", "propesca.it", "marlinblue.it"]

def main():
    os.makedirs(OUTDIR, exist_ok=True)
    jobs = {d: SPECIAL[d] for d in SPECIAL}
    for d in GENERIC:
        jobs[d] = (lambda dd: (lambda: site_generic(dd)))(d)
    def work(item):
        d, fn = item
        try:
            urls = fn()
        except Exception as e:
            return d, f"ERR {e}"
        with open(os.path.join(OUTDIR, f"sitemap_{d}.txt"), "w") as f:
            f.write("\n".join(urls))
        return d, len(urls)
    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        for d, n in ex.map(work, jobs.items()):
            print(f"{d:<24} {n}")

if __name__ == "__main__":
    main()
