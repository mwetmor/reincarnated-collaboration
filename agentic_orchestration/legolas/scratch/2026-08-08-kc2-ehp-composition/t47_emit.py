#!/usr/bin/env python3
"""EMIT t21_wave160_board_ehp_r2.csv -- corrected per-record eHP for Crucible wave 160, Gladiator.
   Chain:  eHP = floor( characterLife(bio, L) * M ),  M = 1 + 5.80 + G/100 + armorbase[L-1]/100
   WINNER-ONLY overlay semantics (whole-record replacement) throughout."""
import sys, pathlib, csv, math, json, re
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from t0_lib import read, owners
TAGS=json.load(open("t23_tags.json"))
OUT=pathlib.Path(__file__).parent/"t21_wave160_board_ehp_r2.csv"

ULT = read("records/game/balancingadjustment_mp+difficulty_enemies01.dbr")[0]["characterLifeModifier"][8]  # 580
GIDX = 159
G = read("records/game/balancingadjustment_survivalmode_enemies03.dbr")[0]["characterLifeModifier"][GIDX]  # 324
AB={}
def ab(path):
    if path not in AB: AB[path]=read(path)[0]["characterLifeModifier"]
    return AB[path]

def life(eq, L):
    e = eq.replace("charLevel", f"({L})").replace("^","**")
    return eval(e, {"__builtins__":{}}, {})

def armorbase_of(rec):
    for i in range(1,40):
        s=rec.get(f"skillName{i}")
        if s and "armorbase" in s: return s, rec.get(f"skillLevel{i}")
    return None, None

MEAS = {"Zantarin, the Immortal":3722896,"Archmage Aleksander":3722896,
        "Kubacabra, the Endless Menace":2955796,"Galakros, the Mountain":2295755,
        "Aetherial Bileeater":484095,"Death Revenant":468504,
        "Aleksander's Shard":103912,"Skeletal Archer":41237}

# ---- roster: (pool_slot, record, spawn_source, proxy, proxy_min, proxy_max, level_offset, level_grade, note)
POOL=[("p01.name%d"%i,p,"pool","lv8_boss+",106,106) for i,p in enumerate([
 "records/creatures/enemies/nemesis/nemesis_aetherial_01.dbr",
 "records/creatures/enemies/nemesis/nemesis_chthonian_02.dbr",
 "records/creatures/enemies/nemesis/nemesis_orderdeathsvigil_01.dbr",
 "records/creatures/enemies/nemesis/nemesis_outlaw_01.dbr",
 "records/creatures/enemies/nemesis/nemesis_undead_02b.dbr",
 "records/creatures/enemies/nemesis/nemesis_kymon_02.dbr",
 "records/creatures/enemies/nemesis/nemesis_undead_01.dbr",
 "records/creatures/enemies/nemesis/nemesis_kymon_01.dbr",
 "records/creatures/enemies/nemesis/nemesis_orderdeathsvigil_02.dbr",
 "records/creatures/enemies/nemesis/nemesis_outlaw_02.dbr"],1)]
POOL+=[("p02.name%d"%i,p,"pool","lv8_boss+",106,106) for i,p in enumerate([
 "records/creatures/enemies/nemesis/nemesis_beast_01_p1.dbr",
 "records/creatures/enemies/nemesis/nemesis_chthonianvoidborn_01.dbr",
 "records/creatures/enemies/nemesis/nemesis_wendigo_01.dbr",
 "records/creatures/enemies/nemesis/nemesis_beast_02.dbr",
 "records/creatures/enemies/nemesis/nemesis_wendigo_02.dbr"],1)]
POOL+=[("p03.name%d"%i,p,"pool","lv8_boss+",106,106) for i,p in enumerate([
 "records/creatures/enemies/nemesis/nemesis_aetherialvanguard_01.dbr",
 "records/creatures/enemies/nemesis/nemesis_wendigo_01.dbr"],1)]
POOL+=[("p04a.name1","records/creatures/enemies/boss&quest/aetherialcolossus_galakros.dbr","pool","lv7_uber hero",103,105),
       ("p04b.name1","records/creatures/enemies/boss&quest/statue_korvaaktombguardian.dbr","pool","lv7_uber hero",103,105)]
POOL+=[("p06.nameChampion%d"%i,p,"pool","lv6_hero",104,105) for i,p in enumerate([
 "records/creatures/enemies/hero/wendigocannibal_h01.dbr","records/creatures/enemies/hero/wendigocannibal_h02.dbr",
 "records/creatures/enemies/hero/wendigocannibal_h03.dbr","records/creatures/enemies/hero/wendigocannibal_h04.dbr",
 "records/creatures/enemies/hero/wendigocannibal_h05.dbr"],1)]
SUMMON=[("Zantarin.skill6","records/creatures/enemies/nemesis/nemesis_orderdeathsvigil_01_revenantsummon.dbr","summon-of-Zantarin",109,109),
 ("Zantarin.skill13","records/creatures/enemies/faction/skeleton_a02_summon.dbr","summon-of-Zantarin",109,109),
 ("Aleksander.skill9","records/skills/nonplayerskillsgdx1/bossskills/nemesis/aetherialvanguard_crystal.dbr","summon-of-Aleksander",109,109),
 ("Galakros.skill12","records/creatures/enemies/aetherialbloater_b01_summon.dbr","summon-of-Galakros",112,112),
 ("Galakros.skill12b","records/creatures/enemies/aetherialbloater_c01_summon.dbr","summon-of-Galakros",112,112)]
PHASE=[("Kubacabra.deathspawn(P2) UNMANIFESTED","records/creatures/enemies/nemesis/nemesis_beast_01_p2a.dbr","phase-UNWIRED-in-crucible",109,109),
 ("Kubacabra.deathspawn(P2b) UNMANIFESTED","records/creatures/enemies/nemesis/nemesis_beast_01_p2b.dbr","phase-UNWIRED-in-crucible",109,109),
 ("Kubacabra.deathspawn(P3a) UNMANIFESTED","records/creatures/enemies/nemesis/nemesis_beast_01_p3a.dbr","phase-UNWIRED-in-crucible",109,109)]

rows=[]
PROXY_BAND={"lv8_boss+":(106,106),"lv7_uber hero":(103,105),"lv6_hero":(104,105)}
def emit(slot, path, src, proxy, lo, hi, grade, note):
    rec,arch = read(path)
    if not rec: print("MISSING", path); return
    tag=rec.get("description",""); nm=TAGS.get(tag,tag)
    bio=rec.get("characterAttributeEquations")
    brec,barch=read(bio); eq=brec["characterLife"]
    abp,ablv=armorbase_of(rec); arr=ab(abp)
    for L in range(lo,hi+1):
        a=arr[L-1]; M=1+ULT/100+G/100+a/100
        base=life(eq,L); ehp=math.floor(base*M)
        meas=MEAS.get(nm) if (grade=="MEASURED-CAMERA") else None
        rows.append(dict(
          body=nm, name_tag=tag, record=path, winner_archive=arch, pool_slot=slot, spawn_source=src,
          monster_class=rec.get("monsterClassification"), proxy=proxy,
          proxy_lv_min=PROXY_BAND.get(proxy,("",""))[0] if src=="pool" else "",
          proxy_lv_max=PROXY_BAND.get(proxy,("",""))[1] if src=="pool" else "",
          level_offset_vs_proxy=(L-PROXY_BAND[proxy][0]) if (src=="pool" and proxy in PROXY_BAND) else "",
          charLevel=L, charLevel_grade=grade,
          bio_record=bio, bio_archive=barch, life_equation=eq,
          armorbase_record=abp, armorbase_skill_level_eq=ablv, armorbase_index=L-1, armorbase_pct=a,
          ultimate_pct=ULT, gladiator_index=GIDX, gladiator_pct=G,
          own_characterLifeModifier=rec.get("characterLifeModifier") or 0.0, own_applied="NO (falsified: Bileeater +50 -> +4.41%)",
          M=round(M,4), base_life=round(base,4), eHP=ehp,
          measured=meas if meas else "",
          residual_abs=(ehp-meas) if meas else "", residual_pct=(round((ehp-meas)/meas*100,6) if meas else ""),
          verdict=("EXACT" if meas and ehp==meas else ("MISMATCH" if meas else "PREDICTION-uncorroborated")),
          note=note))

CAM={"Zantarin, the Immortal","Archmage Aleksander","Kubacabra, the Endless Menace","Galakros, the Mountain"}
for slot,path,src,proxy,lo,hi in POOL:
    rec,_=read(path); nm=TAGS.get(rec.get("description",""),"?")
    if nm in CAM:
        L=109 if proxy=="lv8_boss+" else 106
        emit(slot,path,src,proxy,L,L,"MEASURED-CAMERA","camera nameplate level; on the filmed board")
    else:
        emit(slot,path,src,proxy,lo+3,hi+3,"DERIVED (proxy band + 3; the +3 is MEASURED, DB-source NAMED-ABSENT)",
             "not drawn on the filmed board; level band carries the +3 offset measured on the two drawn pool bodies")
for slot,path,src,lo,hi in SUMMON:
    rec,_=read(path); nm=TAGS.get(rec.get("description",""),"?")
    g="MEASURED-CAMERA" if nm in MEAS else "DERIVED (sibling of a measured summon)"
    emit(slot,path,src,"(none - skill-spawned pet)",lo,hi,g,
         "summon level MEASURED per body; general summon-level rule NAMED-ABSENT (no petLevel field on any summon skill)")
for slot,path,src,lo,hi in PHASE:
    emit(slot,path,src,"(none - deathspawn pool)",lo,hi,"N/A - does not spawn in the Crucible",
         "sm1 record omits poolToSpawnOnDeath + chanceToSpawnOnDeath that gdx1 carries; overlay is whole-record replacement -> phase chain UNWIRED. Camera confirms. Row retained for provenance only; eHP is the CAMPAIGN value and must NOT be summed into the Crucible board.")

cols=list(rows[0].keys())
with open(OUT,"w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=cols); w.writeheader(); w.writerows(rows)
print(f"wrote {OUT}  ({len(rows)} rows)")
print("\nMEASURED-row audit:")
for r in rows:
    if r["measured"]: print(f"  {r['body']:32s} L={r['charLevel']} eHP={r['eHP']:>9,d} meas={r['measured']:>9,d} resid={r['residual_abs']} -> {r['verdict']}")
tot=sum(r["eHP"] for r in rows if r["verdict"]=="EXACT")
print(f"\n  measured-board eHP floor (8 bodies, distinct: F1 counted twice, F6 x2, F7 x3) = see note")
