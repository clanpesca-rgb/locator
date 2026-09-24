#!/usr/bin/env python3
"""Libreria condivisa per la ricerca prezzi Clan Pesca."""
import html as H
import json, re, time, unicodedata, urllib.request

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36",
      "Accept-Language": "it-IT,it;q=0.9,en;q=0.6"}
GTM_RE = re.compile(r'data-gtm4wp_product_data="([^"]+)"')
LOC_RE = re.compile(r"<loc>\s*(?:<!\[CDATA\[)?\s*([^<\]\s]+)\s*(?:\]\]>)?\s*</loc>")

def fetch(url, tries=3, timeout=40):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read().decode("utf-8", "ignore")
        except Exception:
            if i == tries - 1:
                return ""
            time.sleep(1.5 * (i + 1))
    return ""

def gtm_products(page_html):
    out = []
    for m in GTM_RE.finditer(page_html):
        try:
            out.append(json.loads(H.unescape(m.group(1))))
        except json.JSONDecodeError:
            continue
    return out

def norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = s.lower().replace('"', " ").replace("'", " ")
    return re.sub(r"[^a-z0-9.]+", " ", s).strip()

STOP = {"mulinello", "mulinelli", "canna", "canne", "artificiale", "artificiali", "amo", "ami",
        "girella", "girelle", "trecciato", "filo", "fili", "nylon", "scatola", "valigetta",
        "borsa", "esca", "esche", "col", "colore", "mis", "misura", "taglia", "gr", "mm", "cm",
        "mt", "lb", "lbs", "pz", "pcs", "kg", "spinning", "casting", "per", "con", "the", "di",
        "da", "e", "in", "x"}

def tokens_of(name):
    words, nums = [], []
    for t in norm(name).split():
        t = t.strip(".")
        if not t or t in STOP:
            continue
        (nums if re.fullmatch(r"[0-9.]+", t) else words).append(t)
    return [w for w in words if len(w) >= 2], nums

def extract_offer(page_html):
    """(price, low, high, availability) dal JSON-LD/microdati di una pagina prodotto."""
    price = low = high = avail = None
    for m in re.finditer(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', page_html, re.S | re.I):
        try:
            data = json.loads(m.group(1).strip())
        except Exception:
            continue
        for d in (data if isinstance(data, list) else [data]):
            if not isinstance(d, dict):
                continue
            for g in (d.get("@graph") or [d]):
                if not isinstance(g, dict):
                    continue
                ty = g.get("@type")
                if ty == "Product" or (isinstance(ty, list) and "Product" in ty):
                    off = g.get("offers") or {}
                    if isinstance(off, list):
                        off = off[0] if off else {}
                    if isinstance(off.get("offers"), list) and off["offers"]:
                        off = off["offers"][0]
                    def f(x):
                        try:
                            return float(str(x).replace(",", "."))
                        except (TypeError, ValueError):
                            return None
                    price = f(off.get("price")) or price
                    low = f(off.get("lowPrice")) or low
                    high = f(off.get("highPrice")) or high
                    av = str(off.get("availability", ""))
                    if av:
                        avail = ("disponibile" if ("InStock" in av or "LimitedAvailability" in av)
                                 else "esaurito" if "OutOfStock" in av else "preordine" if "PreOrder" in av else None)
        if price or low:
            break
    if price is None and low is None:
        m = (re.search(r'itemprop="price"[^>]*content="([\d.,]+)"', page_html)
             or re.search(r'property="product:price:amount"[^>]*content="([\d.,]+)"', page_html)
             or re.search(r'"price"\s*:\s*"?([\d.]+)"?', page_html))
        if m:
            try:
                price = float(m.group(1).replace(",", "."))
            except ValueError:
                pass
    if avail is None:
        lowh = page_html.lower()
        if "outofstock" in lowh or "non disponibile" in lowh or "esaurito" in lowh:
            avail = "esaurito"
        elif "instock" in lowh or "aggiungi al carrello" in lowh:
            avail = "disponibile"
    return price, low, high, avail
