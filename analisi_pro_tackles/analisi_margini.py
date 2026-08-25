# -*- coding: utf-8 -*-
"""Analisi linea Pro Tackles (Molix/Skirmjan/Major Craft/OMTD) dai report Confronto Prezzi."""

# --- ANCORAGGIO COSTO -------------------------------------------------------
# Unico dato di costo certo disponibile: report Confronto Prezzi Sito 06/08/2026
#   Molix Hyper Split Ring 9: nostro 6,90 -> allineare a 3,25 => margine -33,6%
# (M - C)/M = -0.336  =>  C = M * 1.336
C_split = 3.25 * 1.336
ratio_costo = C_split / 6.90          # costo / nostro prezzo al pubblico
pareggio = 0.393                       # margine di pareggio dichiarato nel report

print(f"Costo Molix Hyper Split Ring 9      = {C_split:.2f} EUR (su 6,90 al pubblico)")
print(f"=> costo/prezzo linea Pro Tackles   = {ratio_costo:.3f}  (margine attuale {1-ratio_costo:.1%})")
print(f"Margine di pareggio negozio         = {pareggio:.1%}")
print(f"=> gia' SOTTO il pareggio di {pareggio-(1-ratio_costo):+.1%} prima ancora di scontare\n")

# Soglia: sotto quale % del nostro prezzo il mercato scende sotto il NOSTRO costo
soglia_delta = 1/ratio_costo - 1
print(f"SOGLIA CRITICA: delta >= +{soglia_delta:.0%} => il mercato vende SOTTO il nostro costo d'acquisto\n")

# --- DATI: report 22/08/2026 18:08, run 'SOLO confronti certi' (il piu' affidabile)
certi = [
 ("MOLIX SNEAKY WORM 5\"",                             7.10,   3.00, "Pesca Piu"),
 ("MOLIX WALLET LURE CASE",                           16.90,   9.90, "Esseci Sport"),
 ("MOLIX SB CRANK 55 SILENT",                         13.60,   8.10, "Boscolo Sport"),
 ("CANNA SKIRMJAN PREDATOR HUNTER 7.9 SPINNING 2PZ", 179.00, 110.00, "Il Maestrale"),
 ("MOLIX ELITE AREA SPOON 2.5 GR",                     6.50,   4.10, "Boscolo Sport"),
 ("OMTD DOUBLE EYELET SERIE OJ1500",                   7.98,   5.40, "WebPesca"),
 ("CANNA SKIRMJAN EVO PIKE 6.8\" CASTING",            219.00, 150.00, "Il Maestrale"),
 ("CANNA SKIRMJAN PREDATOR HUNTER 6.6 SPINNING 2PZ", 160.00, 110.00, "Il Maestrale"),
 ("MOLIX LOVER AREA SPOON GR. 2.4",                    6.98,   4.80, "Il Maestrale"),
 ("CANNA FIORETTO ESSENCE ALL ROUND 7.6 3/8-1",      259.00, 178.90, "5Five Fishing"),
 ("MOLIX ELITE AREA SPOON 1.5 GR",                     6.50,   4.50, "Il Maestrale"),
 ("CANNA FIORETTO ESSENCE ALL ROUND 7.6 3/16-7",     249.00, 178.90, "5Five Fishing"),
 ("MOLIX TACTICAL BAG",                               48.00,  34.90, "Esseci Sport"),
 ("CANNA FIORETTO ESSENCE ALL ROUND 7.2 1/4-1",      245.00, 178.90, "5Five Fishing"),
 ("CANNA SKIRMJAN 66M",                              150.00, 110.00, "Il Maestrale"),
 ("MAJOR CRAFT CEANA 7.6\" 5-15 GR FAST",            115.00,  86.10, "WebPesca"),
 ("CANNA SKIRMJAN PREDATOR HUNTER 7.9 SPINNING 2PZ (b)",145.00,110.00,"Il Maestrale"),
 ("MOLIX HYBRID SWIMMER 165",                         17.99,  13.90, "Esseci Sport"),
 ("MAJOR CRAFT CEANA ITALY ED. 7.9\" 20-80",         155.00, 119.89, "Marco Sport"),
 ("CANNA FIORETTO ESSENCE ALL ROUND 7.1 3/16-1/2",   229.00, 178.90, "5Five Fishing"),
]

# --- DATI: famiglie viste solo nei run a matching largo (08/08 e 22/08 13:53-15:26)
#     da riverificare, ma tutte con delta enorme
larghi = [
 ("MOLIX CRAW FLEX 3\"",              6.98,  3.00, "Pesca Piu"),
 ("OMTD ROUND GUARD SERIE OJ1300",    8.98,  4.49, "Tuttospinning"),
 ("MOLIX RA SHAD 3.5",                7.18,  4.19, "Tuttospinning"),
 ("MOLIX RA SHAD 3",                  7.18,  4.19, "Tuttospinning"),
 ("MOLIX RA SHAD 2",                  6.95,  4.19, "Tuttospinning"),
 ("MOLIX RT FORK FLEX 4\"",           8.98,  5.20, "Boscolo Sport"),
 ("MOLIX RT FORK FLEX 6\"",          10.78,  6.30, "Boscolo Sport"),
 ("MOLIX RT FORK FLEX 3\"",           7.18,  4.86, "WebPesca"),
 ("MOLIX SUPERNATO BEETLE BABY",     13.90,  8.30, "Boscolo Sport"),
 ("MOLIX JUGULO HEAD 64 GR",         14.98,  8.99, "WebPesca"),
 ("MOLIX REAL THING SHAD 3.5",        9.50,  5.80, "Boscolo Sport"),
 ("GLIDE BAIT 178 FLOATING BARONI",  89.98, 49.99, "Bass Store/Boscolo"),
 ("OMTD BIG SWIMBAIT HOOK WEIGTHED",  8.10,  5.40, "4Fishing"),
 ("MAJOR CRAFT CEANA ITALY ED. 7.7\" 10-42", 145.00, 86.70, "Extra Fishing"),
 ("MAJOR CRAFT CEANA ITALY ED. 7.3\" 7-21",  135.00, 86.10, "WebPesca"),
 ("MAJOR CRAFT CEANA ITALY ED. 7.5\" 7-35",  135.00, 86.10, "WebPesca"),
 ("MAJOR CRAFT CEANA ITALY ED. 7.1\" 5-18",  135.00, 86.70, "Extra Fishing"),
 ("MAJOR CRAFT CEANA ITALY ED. 7.9\" 15-60", 145.00, 89.25, "Extra Fishing"),
 ("CANNA MAJOR CRAFT TROUTINO 4.10 GR 1-8",  235.00, 79.00, "Marco Sport"),
 ("CANNA MAJOR CRAFT TROUTINO 5.6\" GR 2-10",235.00, 99.00, "Extra Fishing"),
]

def analizza(righe, titolo):
    print("="*104)
    print(titolo)
    print("="*104)
    print(f"{'Famiglia':<46}{'Noi':>8}{'Min mkt':>9}{'Delta':>8}{'Costo st.':>10}{'Marg. se allineo':>18}")
    print("-"*104)
    out = []
    for nome, nostro, minimo, chi in righe:
        costo = nostro * ratio_costo
        delta = nostro/minimo - 1
        marg  = (minimo - costo)/minimo
        out.append((nome, nostro, minimo, delta, costo, marg, chi))
    out.sort(key=lambda r: r[5])
    for nome, nostro, minimo, delta, costo, marg, chi in out:
        flag = "SOTTO COSTO" if marg < 0 else ("sotto pareggio" if marg < pareggio else "ok")
        print(f"{nome[:45]:<46}{nostro:>8.2f}{minimo:>9.2f}{delta:>+7.0%}{costo:>10.2f}{marg:>15.1%}  {flag}")
    return out

a = analizza(certi,  "A. CONFRONTI CERTI  (run 22/08/2026 18:08 - stessa famiglia, misura e variante)")
print()
b = analizza(larghi, "B. SOLO NEI RUN A MATCHING LARGO  (08/08 e 22/08 13:53) - DA RIVERIFICARE")

tutti = a + b
sotto_costo = [r for r in tutti if r[5] < 0]
sotto_par   = [r for r in tutti if 0 <= r[5] < pareggio]
print()
print("="*104)
print("SINTESI")
print("="*104)
print(f"Famiglie analizzate                                : {len(tutti)}")
print(f"Il mercato vende SOTTO il nostro costo d'acquisto  : {len(sotto_costo)}  ({len(sotto_costo)/len(tutti):.0%})")
print(f"Allinearsi = margine sotto il pareggio 39,3%       : {len(sotto_par)}  ({len(sotto_par)/len(tutti):.0%})")
print(f"Allinearsi resta sostenibile                       : {len(tutti)-len(sotto_costo)-len(sotto_par)}")
