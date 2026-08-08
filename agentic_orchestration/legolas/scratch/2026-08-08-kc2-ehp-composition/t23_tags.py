#!/usr/bin/env python3
"""Q1/Q3: resolve monster description tags -> display names from Edition-II Text_EN.arc (READ-ONLY)."""
import sys, pathlib, json, re
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arc_reader_2026_07_26 import ArcArchive
ROOT=pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ARCS=[("base",ROOT/"resources/Text_EN.arc"),("gdx1",ROOT/"gdx1/resources/Text_EN.arc"),
      ("gdx2",ROOT/"gdx2/resources/Text_EN.arc"),("gdx3",ROOT/"gdx3/resources/Text_EN.arc"),
      ("sm_mod",ROOT/"mods/survivalmode/resources/Text_EN.arc"),
      ("sm1",ROOT/"survivalmode1/resources/Text_EN.arc"),
      ("sm2",ROOT/"survivalmode2/resources/text_en.arc"),
      ("sm3",ROOT/"survivalmode3/resources/Text_EN.arc")]
TAGS={}   # key -> (val, archive, file)
for k,p in ARCS:
    if not p.exists(): print(f"  (missing {k})"); continue
    a=ArcArchive(p)
    names=a.names()
    for n in names:
        if not n.lower().endswith(".txt"): continue
        try: raw=a.read_file(n)
        except Exception as e: continue
        try: txt=raw.decode("utf-8-sig")
        except Exception: txt=raw.decode("latin-1")
        for line in txt.splitlines():
            if "=" not in line: continue
            kk,_,vv=line.partition("=")
            kk=kk.strip()
            if kk: TAGS[kk]=(vv.strip(),k,n)
print(f"banked {len(TAGS)} tag keys across {len(ARCS)} archives")
json.dump({k:v[0] for k,v in TAGS.items()}, open("t23_tags.json","w"))
WANT=["tagNemesis_Aetherial01","tagNemesis_Chthonian02","tagNemesis_OrderDeathsVigil01",
 "tagNemesis_Outlaw01","tagNemesis_Undead02","tagNemesis_Kymon02","tagGDX3Nemesis_Undead02",
 "tagGDX3Nemesis_Zealot02","tagGDX3Nemesis_Necro02","tagGDX3Nemesis_Outlaw02",
 "tagGDX1Nemesis_Beast01","tagGDX1Nemesis_Chthonian01","tagGDX1Nemesis_Wendigo01",
 "tagGDX3Nemesis_Beast02","tagGDX3Nemesis_Wendigo02","tagGDX1Nemesis_Aetherial01",
 "tagGDX1MiniBoss_Aetherial02","tagGDX2Boss_TombGuardian_01",
 "tagGDX1HeroWendigoCannibal_H01","tagGDX1HeroWendigoCannibal_H02","tagGDX1HeroWendigoCannibal_H03",
 "tagGDX1HeroWendigoCannibal_H04","tagGDX3HeroWendigoCannibal_H01"]
print("\n== ROSTER TAGS ==")
for w in WANT:
    v=TAGS.get(w); print(f"  {w:38s} -> {v[0]!r}   [{v[1]}/{v[2]}]" if v else f"  {w:38s} -> ***MISSING***")
print("\n== reverse lookup: which tag keys hold these display strings? ==")
for target in ("Zantarin","Aleksander","Kubacabra","Bileeater","Death Revenant","Skeletal Archer",
               "Galakros","Grava'Thul","Valdaran","Fabius","Iron Maiden","Moosilauke","Reaper","Benn'Jahr",
               "Shriek","Ignus","Vinn Ozmald","Raddoth","Underking","Shard"):
    hits=[(k,v[0],v[1],v[2]) for k,v in TAGS.items() if target.lower() in v[0].lower()]
    print(f"\n  '{target}' -> {len(hits)} tags")
    for k,val,ar,f in sorted(hits)[:14]:
        print(f"      {k:46s} = {val!r}  [{ar}/{f}]")
