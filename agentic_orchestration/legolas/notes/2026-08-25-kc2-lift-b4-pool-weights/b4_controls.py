#!/usr/bin/env python3
"""KC2 LIFT · Lap B4 — the POSITIVE CONTROLS, as a runnable file.

A lap that only emits rows has proved that a reader ran, not that it read correctly. These four
controls each compare this lap's per-slot decomposition against an INDEPENDENTLY-PRODUCED artifact
that already exists in the run's lineage. They are written to be re-runnable by anyone who doubts
a row.

  C-1  ROSTER IDENTITY  — the ordered `member_record` list per (pool, family) must equal, element
       for element, the pinned `pe6_crucible_wave_pools_v2.csv`'s flattened `roster_records` /
       `champ_records`. This is what proves the INDEX PAIRING and the overlay WINNER choice: a
       wrong archive or a mis-paired index would reorder or re-populate the list.
  C-2  CAPACITY DECOMPOSITION — the per-slot `limit<i>` values must SUM to Lap V's independently
       decoded `regular_capacity` / `champion_capacity` (`pm4v_roster_arithmetic.csv`), with an
       ABSENT limit mapping to `inf` exactly as Lap V's decode did. This is the lift's whole
       thesis in one assertion: the sum that was the only available grain decomposes into parts,
       and the parts add back to the sum.
  C-3  L-53 SPOT ANCHOR — the run ledger's own hand-quoted slot must reproduce byte-for-byte:
       `skeletonrevenant_t3` slot 4 = `skeleton_d01.dbr`, weight 75, minPlayerLevel 45, limit 2.
  C-4  DANGLING REFERENCES — every `member_record` must resolve to a record in some archive
       (the G-7 class). A dangling name is a finding; a silently-kept dangling name is a defect.

Author: legolas (UNKNOWN-RESEARCHER), 2026-08-25.
"""
from __future__ import annotations

import collections
import csv
import math
import pathlib
import sys

ENGINE = pathlib.Path("/Users/admin/Games/reincarnated-engine")
META = pathlib.Path("/Users/admin/Games/reincarnated-collaboration")
LAP = META / "agentic_orchestration/legolas/notes/2026-08-25-kc2-lift-b4-pool-weights"
LAPV = META / "agentic_orchestration/legolas/notes/2026-08-15-kc2-pm4-lap-v-roster-decode"

sys.path.insert(0, str(ENGINE / "src" / "reincarnated" / "simulation" / "scripts"))
sys.path.insert(0, str(META / "agentic_orchestration" / "research" / "scripts"))
sys.path.insert(0, str(ENGINE / "src"))

from gamora_kc2_c1_closure_ed3_2026_08_08 import E3  # noqa: E402

MINE = list(csv.DictReader(open(LAP / "b4_pool_members_w150_160.csv")))
PE6 = list(csv.DictReader(open(ENGINE / "data/kc2/pe6_crucible_wave_pools_v2.csv")))
SEL = [r for r in PE6 if 150 <= int(r["global_wave"]) <= 160]

fails = 0


def report(tag, ok, detail=""):
    global fails
    print(f"  {'PASS' if ok else 'FAIL'}  {tag}  {detail}")
    if not ok:
        fails += 1


# ─────────────────────────────────────────────────────────────── C-1 roster identity
mine_n, mine_c = collections.defaultdict(list), collections.defaultdict(list)
for r in MINE:
    (mine_n if r["family"] == "normal" else mine_c)[r["pool_record"]].append(r["member_record"])

bad_n, bad_c, seen = [], [], set()
for r in SEL:
    p = r["pool_record"]
    if p in seen:
        continue
    seen.add(p)
    lst = [x.strip().lower() for x in r["roster_records"].split("|") if x.strip()]
    if lst != mine_n[p]:
        bad_n.append(p)
    lst = [x.strip().lower() for x in r["champ_records"].split("|") if x.strip()]
    if lst != mine_c[p]:
        bad_c.append(p)
report("C-1 roster identity vs pinned pe6 CSV", not (bad_n or bad_c),
       f"{len(seen)} pools; normal-mismatch={len(bad_n)} champion-mismatch={len(bad_c)}")

# ─────────────────────────────────────────────────────────────── C-2 capacity decomposition
cap = {("normal", ""): collections.defaultdict(lambda: [0, False]),
       ("champion", ""): collections.defaultdict(lambda: [0, False])}
for r in MINE:
    d = cap[(r["family"], "")][r["pool_record"]]
    if r["limit_state"] == "ABSENT":
        d[1] = True
    else:
        d[0] += int(r["limit"])


def cap_of(fam, p):
    s, anyabs = cap[(fam, "")][p]
    return math.inf if anyabs else s


lapv = list(csv.DictReader(open(LAPV / "pm4v_roster_arithmetic.csv")))
n_cmp, bad = 0, []
seen = set()
for r in lapv:
    p = r["pool_record"]
    if not (151 <= int(r["global_wave"]) <= 160) or p in seen or p not in mine_n and p not in mine_c:
        continue
    seen.add(p)
    n_cmp += 1
    if cap_of("normal", p) != float(r["regular_capacity"]) or \
       cap_of("champion", p) != float(r["champion_capacity"]):
        bad.append((p, cap_of("normal", p), r["regular_capacity"],
                    cap_of("champion", p), r["champion_capacity"]))
report("C-2 per-slot limits SUM to Lap-V decoded capacity", not bad,
       f"{n_cmp} pools compared (Lap V's band is 151-170, so wave-150-only pools are out of "
       f"its scope and out of this control); mismatches={len(bad)} {bad[:3]}")

# ─────────────────────────────────────────────────────────────── C-3 L-53 spot anchor
hit = [r for r in MINE if r["pool_record"].endswith("skeletonrevenant_t3.dbr")
       and r["family"] == "normal" and r["slot_index"] == "4"]
ok = (len(hit) == 1 and hit[0]["member_record"].endswith("skeleton_d01.dbr")
      and hit[0]["weight"] == "75" and hit[0]["min_player_level"] == "45"
      and hit[0]["limit"] == "2")
report("C-3 L-53 hand-quoted slot reproduces", ok, str(hit[0] if hit else "NOT FOUND")[:160])

# ─────────────────────────────────────────────────────────────── C-4 dangling references
dang = [r for r in MINE if r["member_record"] and r["member_record"] not in E3.idx]
report("C-4 no dangling member records (G-7 class)", not dang,
       f"{len(MINE)} slots; dangling={len(dang)} {[d['member_record'] for d in dang][:3]}")

print(f"\n{4 - fails}/4 controls pass.")
sys.exit(1 if fails else 0)
