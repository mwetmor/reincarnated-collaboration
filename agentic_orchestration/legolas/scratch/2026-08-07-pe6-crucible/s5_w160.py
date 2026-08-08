#!/usr/bin/env python3
"""S5 — PE6 deep dive: wave 160 (tier16 w10), the 150-160 band, and the nemesis roster. READ-ONLY."""
import sys, json, pathlib, collections
W = json.load(open("s4_waves_full.json"))
BY = {w["gwave"]: w for w in W}

def dump_wave(g, diff="gladiator", full=True):
    w = BY[g]
    print(f"\n{'='*100}\nWAVE {g}   (tier{w['tier']:02d} / w{w['wave']:02d})   spawn points = {w['npts']}   "
          f"archives={w['owners']}   classes={w['classes']}")
    for d in ("aspirant", "challenger", "gladiator"):
        s = w[d]
        print(f"   [{d:11s}] min={s['min']:.0f} max={s['max']:.0f} E={s['E']:.2f}  kinds={s['kinds']}")
    for e in sorted(w["points"], key=lambda x: x["pt"]):
        opts = e["diffs"][diff]
        fb = " (falls back to base pools — no Legendary override)" if e["fallback"][diff] else " (LEGENDARY OVERRIDE)"
        print(f"\n   -- p{e['pt']:02d}  [{e['cls']}, {e['owner']}]{fb}")
        if e.get("ambush"):
            print(f"      ambush: {e['ambush']}")
        for o in opts:
            if o.get("UNRESOLVED"):
                print(f"      !! UNRESOLVED {o['pool']}"); continue
            print(f"      w={o['w']:<5.0f} {o['pool']}  [{o['owner']}]  spawn {o['smin']:.0f}-{o['smax']:.0f}  "
                  f"champ {o['cch']:.0f}% {o['cmin']:.0f}-{o['cmax']:.0f}")
            if full:
                tot = sum(r["w"] for r in o["roster"]) or 1
                for r in o["roster"]:
                    print(f"           roster w={r['w']:<6.0f} ({100*r['w']/tot:5.1f}%) lim={r['limit']} "
                          f"minPL={r['minPL']} {r['lv'].split('/')[-1]:22s} {r['name']}   <- {r['rec']}")
                for r in o["champroster"]:
                    print(f"           CHAMP  w={r['w']:<6.0f} lim={r['limit']} minPL={r['minPL']} "
                          f"{r['lv'].split('/')[-1]:22s} {r['name']}   <- {r['rec']}")

print("#" * 100)
print("# WAVE 160 — THE KILL WAVE")
print("#" * 100)
dump_wave(160)

print("\n\n" + "#" * 100)
print("# BAND 150–160 (tier15 w10 .. tier16 w10) — every wave, Gladiator view")
print("#" * 100)
for g in range(150, 161):
    dump_wave(g)
