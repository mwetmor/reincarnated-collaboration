#!/usr/bin/env python3
"""D11 — THE SOLVED LIFE MODEL. HP = base(L) x (1 + (580 + surv[w] + armorbase[L-1])/100).
Edition-II pin (fixture substrate; byte-identical in Edition-III per L-61). READ-ONLY."""
import sys, collections
sys.path.insert(0,".")
import lib2
E2=lib2.E2
def ev(e,L): return eval(str(e).replace("^","**").replace("charLevel",f"({L})"),{"__builtins__":{}},{})
SURV=E2.merged("records/game/balancingadjustment_survivalmode_enemies03.dbr")[0]["characterLifeModifier"]
DIFF=E2.merged("records/game/balancingadjustment_mp+difficulty_enemies01.dbr")[0]["characterLifeModifier"][8]  # Ultimate, players=1

def life_model(p, L, wave=152):
    r,_=E2.merged(p)
    if not r: return None
    bp=r.get("characterAttributeEquations")
    if not bp: return None
    b,_=E2.merged(bp if isinstance(bp,str) else bp[0])
    if not b or "characterLife" not in b: return None
    base=ev(b["characterLife"], L)
    extra=0.0; src=[]
    for i in range(1,30):
        sn=r.get(f"skillName{i}"); sl=r.get(f"skillLevel{i}")
        if not sn: continue
        s,_=E2.merged(sn)
        if not s: continue
        lm=s.get("characterLifeModifier")
        if lm is None: continue
        if isinstance(lm,list):
            idx=int(ev(sl,L))-1 if sl is not None else 0
            if 0<=idx<len(lm) and lm[idx]:
                extra+=lm[idx]; src.append(f"{sn.split('/')[-1]}[{idx}]={lm[idx]}")
        elif lm:
            extra+=lm; src.append(f"{sn.split('/')[-1]}={lm}")
    sigma = DIFF + SURV[wave-1] + extra
    return base*(1+sigma/100), base, sigma, src, r.get("monsterClassification")

print(f"difficulty (Ultimate, 1 player) = +{DIFF} %   survival[w152] = +{SURV[151]} %\n")
CHECK=[("swampcrab_a00_summon (crabling)","records/creatures/enemies/swampcrab_a00_summon.dbr",[105,106,107,108,109],[42798,43548]),
       ("aetherialfleshshaper_haraxis","records/creatures/enemies/boss&quest/aetherialfleshshaper_haraxis.dbr",[107,108,109],[2050807]),
       ("aetherialphantom_h01 (devotion hero)","records/creatures/enemies/devotion/aetherialphantom_h01.dbr",[107,108],[453883]),
       ("aetherialcorruption_c01_summon","records/creatures/enemies/aetherialcorruption_c01_summon.dbr",[107,108],[472732]),
       ("basilisk_h02 = Rotmouth","records/creatures/enemies/hero/basilisk_h02.dbr",[107,108],[]),
       ("swampcrab_h03 = Mudflinger","records/creatures/enemies/hero/swampcrab_h03.dbr",[107,108],[443554,453883]),
      ]
for lbl,p,Ls,targets in CHECK:
    print(f"### {lbl}")
    for L in Ls:
        hp,base,sig,src,cls=life_model(p,L)
        tag=""
        for t in targets:
            d=(hp-t)/t*100
            if abs(d)<0.05: tag+=f"   <<< EXACT match {t:,} ({d:+.4f} %)"
            elif abs(d)<1.0: tag+=f"   [near {t:,} {d:+.3f} %]"
        print(f"   L{L}  base {base:12,.4f}  Sigma {sig:7.1f} %  mult x{1+sig/100:8.5f}  HP {hp:12,.2f}{tag}")
        if L==Ls[0]: print(f"        skill life terms: {src}")
    print()
print("=== the Delta1.752 % question, resolved arithmetically ===")
h107,b107,s107,_,_=life_model("records/creatures/enemies/swampcrab_a00_summon.dbr",107)
h108,b108,s108,_,_=life_model("records/creatures/enemies/swampcrab_a00_summon.dbr",108)
print(f"   L107 -> {h107:,.3f}   (measured 42,798 ; delta {(h107-42798)/42798*100:+.4f} %)")
print(f"   L108 -> {h108:,.3f}   (measured 43,548 ; delta {(h108-43548)/43548*100:+.4f} %)")
print(f"   modelled ratio {h108/h107:.6f}  ({(h108/h107-1)*100:.4f} %)")
print(f"   measured ratio {43548/42798:.6f}  ({(43548/42798-1)*100:.4f} %)")
print(f"   pure-level part {(b108/b107-1)*100:.4f} %  +  passive-rank part {((1+s108/100)/(1+s107/100)-1)*100:.4f} %")
