#!/usr/bin/env python3
"""Predicted GD base-attack hit size vs charLevel, under the two candidate
monsterAttributePak TDM composition readings. Read-only over the .arz corpus
via legolas's G-5a resolver. galadriel 2026-07-28."""
import importlib.util, pathlib, json
G5 = pathlib.Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
                  "legolas/scratch/2026-07-28-kitcal1-g5a/g5a_resolve.py")
spec = importlib.util.spec_from_file_location("g5a", G5); M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)
P = "records/skills/nonplayerskills/passive/"
DB = {t: M.rec(f"{P}damagebase_physical0{t}.dbr") for t in (1,2)}
AB = {t: M.rec(f"{P}armorbase0{t}.dbr") for t in (1,2)}
PAK = M.pak_vals()
PAK_TDM = PAK["offensiveTotalDamageModifier"]; DEXM = PAK["characterDexterityModifier"]
print(f"pak TDM = {PAK_TDM}%   pak DexMod = {DEXM}%")

def a(arr_, r): return arr_[min(max(int(r)-1,0), len(arr_)-1)]

def band(cl, tier=1, reading="mult"):
    pmin = a(DB[tier]["offensivePhysicalMin"], cl); pmax = a(DB[tier]["offensivePhysicalMax"], cl)
    tdm  = a(AB[tier]["offensiveTotalDamageModifier"], cl)
    if reading == "mult": m = (1+tdm/100)*(1+PAK_TDM/100)
    elif reading == "add": m = 1 + (tdm+PAK_TDM)/100
    else: raise ValueError
    dex = (cl*6.5+10)*(1+DEXM/100); dm = dex/245+1
    return pmin*m*dm, pmax*m*dm, tdm, m

def oa(cl):
    dex = (cl*6.5+10)*(1+DEXM/100)
    return ((cl*6+5) + cl*12 + dex*0.5)*(1+PAK["characterOffensiveAbility"+"Modifier"]/100)+53

def pth(OA, DA):
    return ((((OA/((DA/3.5)+OA))*300)*0.3)+(((((OA*3.25)+10000)-(DA*3.25))/100)*0.7))-50
def pthmod(p):
    T=[70,90,105,120,130,135]; Mo=[1.0,1.1,1.2,1.3,1.4,1.5]; out=1.0
    for t,mm in zip(T,Mo):
        if p>=t: out=mm
    return out

print(f"\n{'charL':>5} {'tier':>4} | {'ADDITIVE (pak summed)':>24} | {'MULTIPLICATIVE (pak sep.)':>26} | ratio | monOA  PTH@DA")
for cl in range(1,16):
    for tier in (1,2):
        alo,ahi,tdm,ma = band(cl,tier,"add"); mlo,mhi,_,mm = band(cl,tier,"mult")
        O=oa(cl)
        print(f"{cl:>5} {tier:>4} | tdm{tdm:>5.0f}% m={ma:.3f}  {alo:6.2f}-{ahi:6.2f} | "
              f"m={mm:.4f}  {mlo:6.2f}-{mhi:6.2f} | {mm/ma:5.2f} | {O:6.1f}")
    print()

# emit machine-readable
out = {"pak_tdm_pct": PAK_TDM, "pak_dex_mod_pct": DEXM, "bands": {}}
for cl in range(1,16):
    out["bands"][cl] = {t: {r: band(cl,t,r)[:2] for r in ("add","mult")} for t in (1,2)}
    out["bands"][cl]["monster_OA"] = oa(cl)
json.dump(out, open("predicted-bands.json","w"), indent=1)

# PTH damage modifier over plausible player DA
print("PTH damage modifier (monster charLevel x player DA):")
print(f"{'charL':>5} " + " ".join(f"DA{d:<5}" for d in (50,90,140,225,300,400)))
for cl in (1,2,4,6,8,10,12):
    row=[]
    for DA in (50,90,140,225,300,400):
        p=pth(oa(cl),DA); row.append(f"{p:5.0f}/{pthmod(p):.1f}")
    print(f"{cl:>5} " + " ".join(row))
