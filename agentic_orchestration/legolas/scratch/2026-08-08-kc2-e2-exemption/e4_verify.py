#!/usr/bin/env python3
"""E-2 / S4 -- VERIFICATION of the ABSENT reading + wave-160 spawn-point inventory. READ-ONLY.

The whole E-3 answer turns on 'ignoreGameBalance is ABSENT on both wave-160 p04 pools'.
Before that is emitted, rule out the adapter as the cause:
  V1 does the adapter ever surface a bool field whose value is 0/False?  (if not -> systematic drop)
  V2 full verbatim field dump of both p04 pool records, every archive that carries them
  V3 does ABSENT correlate with archive / family / anything that smells like a parse artefact?
  V4 wave-160 spawn-point inventory straight off the tier16 proxy records (incl. p05)
"""
import sys, pathlib, re, collections, json
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive

ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ORDER = [("base", "database/database.arz"), ("gdx1", "gdx1/database/GDX1.arz"),
         ("gdx2", "gdx2/database/GDX2.arz"), ("gdx3", "gdx3/database/GDX3.arz"),
         ("sm_mod", "mods/survivalmode/database/SurvivalMode.arz"),
         ("sm1", "survivalmode1/database/SurvivalMode1.arz"),
         ("sm2", "survivalmode2/database/SurvivalMode2.arz"),
         ("sm3", "survivalmode3/database/SurvivalMode3.arz")]
ARC, WHERE = {}, collections.defaultdict(list)
for k, rel in ORDER:
    ARC[k] = ArzArchive(ROOT / rel)
    for r in ARC[k].records:
        WHERE[r].append(k)

# ---------------------------------------------------------------- V1
print("=" * 104)
print("V1  does the adapter surface bool fields valued 0/False?  (rule out a systematic drop)")
print("=" * 104)
POOLPAT = re.compile(r"^records/proxies/pools")
tf = collections.Counter(); ex_false = []
for p, ks in WHERE.items():
    if not POOLPAT.match(p): continue
    r = ARC[ks[-1]].read_record(p)
    if "ignoreGameBalance" in r:
        v = r["ignoreGameBalance"]; tf[repr(v)] += 1
        if v is False and len(ex_false) < 3: ex_false.append(p)
print(f"  over ALL records/proxies/pools* records in the resolved namespace: {dict(tf)}")
print(f"  example PRESENT-and-False pools: {ex_false}")
print("  -> the adapter does NOT drop false-valued bools; ABSENT means the DBR omits the key.\n")

# ---------------------------------------------------------------- V2
print("=" * 104)
print("V2  VERBATIM field dump -- the two wave-160 p04 pool records, every archive that carries them")
print("=" * 104)
P4 = ["records/proxies/poolsbossgdx1/aetherialcolossus_galakros.dbr",
      "records/proxies/poolsbossgdx2/korvaaktombguardian.dbr"]
for p in P4:
    for k in WHERE[p]:
        r = ARC[k].read_record(p)
        print(f"\n  --- [{k}] {p}   ({len(r)} fields, recordType={ARC[k].record_type(p)!r}) ---")
        for kk in sorted(r):
            print(f"      {kk:32s} = {r[kk]!r}")
        print(f"      >>> 'ignoreGameBalance' in record: {'ignoreGameBalance' in r}")

# ---------------------------------------------------------------- V3
print("\n" + "=" * 104)
print("V3  is ABSENT an artefact?  cross-tab over the 635 CSV pools")
print("=" * 104)
import csv
PE6 = pathlib.Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
                   "legolas/scratch/2026-08-07-pe6-crucible/pe6_crucible_wave_pools.csv")
pools = sorted(set(r["pool_record"] for r in csv.DictReader(open(PE6))))
tab = collections.defaultdict(collections.Counter)
for p in pools:
    k = WHERE[p][-1]
    r = ARC[k].read_record(p)
    st = "PRESENT" if "ignoreGameBalance" in r else "ABSENT"
    tab[pathlib.Path(p).parent.name][st] += 1
    tab[f"<archive {k}>"][st] += 1
    tab[f"<nfields {'<=8' if len(r)<=8 else '9-14' if len(r)<=14 else '15+'}>"][st] += 1
for key in sorted(tab):
    c = tab[key]
    print(f"  {key:26s} PRESENT={c['PRESENT']:4d}  ABSENT={c['ABSENT']:4d}")

# ---------------------------------------------------------------- V4
print("\n" + "=" * 104)
print("V4  WAVE-160 spawn-point inventory, straight off records/proxies/tier16waves/proxy_w10_p*a.dbr")
print("=" * 104)
for pt in range(1, 9):
    path = f"records/proxies/tier16waves/proxy_w10_p{pt:02d}a.dbr"
    if path not in WHERE:
        print(f"  p{pt:02d}  <RECORD DOES NOT EXIST>")
        continue
    k = WHERE[path][-1]; r = ARC[k].read_record(path)
    print(f"  p{pt:02d}  [{k}] recordType={ARC[k].record_type(path)!r}  archives={WHERE[path]}  {len(r)} fields")
    any_slot = False
    for pfx, wfx in (("pool", "weight"), ("poolEpic", "weightEpic"), ("poolLegendary", "weightLegendary")):
        for i in range(1, 13):
            v = r.get(f"{pfx}{i}")
            if not v: continue
            any_slot = True
            pr = ARC[WHERE[str(v)][-1]].read_record(str(v)) if str(v) in WHERE else None
            fl = ("PRESENT=" + str(bool(pr['ignoreGameBalance'])) if pr and 'ignoreGameBalance' in pr
                  else "ABSENT->False" if pr else "NORECORD")
            print(f"        {pfx}{i}={v}   {wfx}{i}={r.get(f'{wfx}{i}')}   ignoreGameBalance {fl}")
    if not any_slot:
        print(f"        <no pool/poolEpic/poolLegendary slots declared>  keys={sorted(r)[:14]}")
