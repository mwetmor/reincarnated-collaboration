#!/usr/bin/env python3
"""S-1 CONTROL. Test the bio-block field mapping against a closed form built
ENTIRELY from records/creatures/pc/{malepc01,playerlevels}.dbr:

    points_X   = (stored_X - 50) / 8            (strength/dexterity/intelligenceIncrement = 8)
    health     = 250 + 20*pPHY + 8*pCUN + k*pSPI   (lifeIncrement / ...Dexterity / ...Intelligence)
    energy     = 250 + 16*pSPI                     (manaIncrement)

H1 = parser order (physique, cunning, spirit); H2 = physique/cunning SWAPPED.
A mapping that is right is right on EVERY sample. READ-ONLY."""
import sys; sys.path.insert(0,'.')
import gdcg7 as G

BASE, INC, LIFE_P, LIFE_C, MANA_S = 250.0, 8.0, 20.0, 8.0, 16.0

def pts(v): 
    p = (v - 50.0)/INC
    return p, (abs(p - round(p)) < 1e-6)

rows=[]
for path in [l.strip() for l in open("samples.txt") if l.strip()]:
    try: res = G.parse(path)
    except Exception as e:
        rows.append((path,"PARSE-FAIL",str(e))); continue
    b = res["blocks"].get("character_bio")
    if not b: rows.append((path,"NO-BIO","")); continue
    h = res["header"]
    A,B,C,HP,EN = b["physique"], b["cunning"], b["spirit"], b["health"], b["energy"]
    out={}
    for name,(P,Cu,Sp) in (("H1",(A,B,C)), ("H2-swap",(B,A,C))):
        pP,iP = pts(P); pC,iC = pts(Cu); pS,iS = pts(Sp)
        en = BASE + MANA_S*pS
        best=None
        for k in (8.0,12.0):
            hp = BASE + LIFE_P*pP + LIFE_C*pC + k*pS
            if abs(hp-HP) < 1e-3: best=k; break
        out[name] = dict(pts=(pP,pC,pS), integral=(iP and iC and iS),
                         energy_ok=abs(en-EN)<1e-3, energy_pred=en,
                         health_k=best, health_pred=BASE+LIFE_P*pP+LIFE_C*pC+12*pS)
    rows.append((path, h["name"], h["level"], (A,B,C,HP,EN), out))

print(f"{'character':20s} {'lvl':>3s} {'stored (P,C,S,HP,EN)':38s} | {'H1 energy':>10s} {'H1 health':>22s} | {'H2 energy':>10s} {'H2 health':>22s}")
for r in rows:
    if len(r)!=5: print(r); continue
    path, nm, lvl, st, out = r
    def fmt(o):
        e = "EXACT" if o["energy_ok"] else f"MISS({o['energy_pred']:.0f})"
        hk = f"EXACT k={o['health_k']:.0f}" if o["health_k"] else f"MISS(pred12={o['health_pred']:.0f})"
        return e, hk
    e1,h1 = fmt(out["H1"]); e2,h2 = fmt(out["H2-swap"])
    ptsok = "int" if out["H1"]["integral"] else "NON-INTEGRAL"
    print(f"{nm[:20]:20s} {lvl:3d} {str(st):38s} | {e1:>10s} {h1:>22s} | {e2:>10s} {h2:>22s}   pts={ptsok} P/C/S={tuple(int(x) for x in out['H1']['pts'])}")
