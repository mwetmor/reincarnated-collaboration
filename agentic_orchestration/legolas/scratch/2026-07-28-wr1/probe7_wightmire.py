#!/usr/bin/env python3
"""probe7 (WR1 E-1) — is slith_h01 (igrixx_frigidring carrier) reachable in Act-1 Wightmire?
Scan all proxy pools for references; report area + level-variance equation. Read-only."""
import sys, pathlib, re
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ARZS = [ROOT/"database/database.arz", ROOT/"gdx1/database/GDX1.arz",
        ROOT/"gdx2/database/GDX2.arz", ROOT/"gdx3/database/GDX3.arz"]
TARGET = "records/creatures/enemies/hero/slith_h01.dbr"
archives = [(p.name, ArzArchive(p)) for p in ARZS]
for name, a in archives:
    for rp in a.records:
        if 'proxies' not in rp: continue
        rec = a.read_record(rp)
        for k, v in rec.items():
            if isinstance(v, str) and v == TARGET:
                idx = re.sub(r'^name', '', k)
                print(f"[{name}] {rp}")
                print(f"      {k}={v}")
                for kk in (f"weight{idx}", f"levelVarianceEquation{idx}", f"alwaysSpawn{idx}",
                           f"limit{idx}", "spawnMin", "spawnMax", "championChance"):
                    if kk in rec: print(f"        {kk:26s} {rec[kk]!r}")
# the hero record itself
print("\n### slith_h01 record — cadence + wiring")
for name, a in archives:
    if TARGET in a.records:
        rec = a.read_record(TARGET)
        for k in sorted(rec):
            if re.search(r'^charLevel$|monsterClassification|characterAttackSpeed|^skillName\d|^skillLevel\d|specialAttack|numAttackSlots|chanceToEquip(Right|Left)Hand$|characterAttributeEquations|^controller$|^description$|hitThreshold', k):
                print(f"  {k:34s} {rec[k]!r}")
        break
