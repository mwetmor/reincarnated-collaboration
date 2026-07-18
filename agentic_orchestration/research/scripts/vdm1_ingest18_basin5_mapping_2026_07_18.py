"""
vdm1_ingest18_basin5_mapping_2026_07_18.py
-------------------------------------------
MIGRATION-vdm1-ingest18 (basin-5 mapping INGEST — LAST mapping ingest of VDM-1 run)

Ops:
  1a. Greenfield INSERT of 125 kit_mapping rows from mapping-batch-p01..p13.jsonl
  1b. MAP-ERRATA-1: ud-lightning-vortex — element_primary null→"lightning", ailments ["shock"]→[]
  1c. Assert COUNT(grade='GAPPED') == COUNT(terminal_state='MAPPED_DOCKET') == 31

TIER 2 HOLD: mechanic_gap_docket and mint_ledger untouched.

Source spec: agentic_orchestration/research/vdm1/stage2/basin5/INGEST-BASIN5-MAPPING-MANIFEST.md
"""

import json
import glob
import sqlite3
import sys
import os

DB = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/corpus.db"
BASIN5_DIR = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/vdm1/stage2/basin5"
BATCH_GLOB = os.path.join(BASIN5_DIR, "mapping-batch-p*.jsonl")

# ---------------------------------------------------------------------------
# Load all 125 rows from batch files
# ---------------------------------------------------------------------------
rows = []
for fpath in sorted(glob.glob(BATCH_GLOB)):
    with open(fpath) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            rows.append({
                "kit_id": rec["kit_id"],
                "mapping_json": json.dumps(rec["mapping_json"], ensure_ascii=False, separators=(",", ":")),
                "grade": rec["grade"],
                "deviation_notes": rec.get("deviation_notes"),
                "terminal_state": rec["terminal_state"],
            })

print(f"Rows loaded from files: {len(rows)}")
assert len(rows) == 125, f"Expected 125 rows, got {len(rows)}"

# ---------------------------------------------------------------------------
# Pre-ingest guards (hard)
# ---------------------------------------------------------------------------
con = sqlite3.connect(DB)
cur = con.cursor()

missing_canon = []
already_mapped = []
for row in rows:
    kid = row["kit_id"]
    cur.execute("SELECT 1 FROM canon_corpus WHERE kit_id=?", (kid,))
    if not cur.fetchone():
        missing_canon.append(kid)
    cur.execute("SELECT 1 FROM kit_mapping WHERE kit_id=?", (kid,))
    if cur.fetchone():
        already_mapped.append(kid)

if missing_canon:
    print(f"ABORT: {len(missing_canon)} kit_id(s) not in canon_corpus: {missing_canon}")
    con.close()
    sys.exit(1)

if already_mapped:
    print(f"ABORT: {len(already_mapped)} kit_id(s) already in kit_mapping: {already_mapped}")
    con.close()
    sys.exit(1)

print("GUARD 1 PASS: all 125 kit_ids found in canon_corpus")
print("GUARD 2 PASS: zero kit_ids already in kit_mapping")

# ---------------------------------------------------------------------------
# 1a. Greenfield INSERT
# ---------------------------------------------------------------------------
cur.execute("SELECT COUNT(*) FROM kit_mapping")
pre_count = cur.fetchone()[0]
print(f"kit_mapping pre-insert count: {pre_count}")

insert_sql = """
INSERT INTO kit_mapping (kit_id, mapping_json, grade, deviation_notes, terminal_state)
VALUES (:kit_id, :mapping_json, :grade, :deviation_notes, :terminal_state)
"""
cur.executemany(insert_sql, rows)
con.commit()

cur.execute("SELECT COUNT(*) FROM kit_mapping")
post_count = cur.fetchone()[0]
print(f"kit_mapping post-insert count: {post_count}")
assert post_count == pre_count + 125, f"Expected {pre_count + 125}, got {post_count}"
print(f"INSERT complete: {post_count - pre_count} rows inserted")

# ---------------------------------------------------------------------------
# 1b. MAP-ERRATA-1: ud-lightning-vortex
# ---------------------------------------------------------------------------
cur.execute("SELECT mapping_json FROM kit_mapping WHERE kit_id='ud-lightning-vortex'")
row_vortex = cur.fetchone()
assert row_vortex is not None, "ABORT: ud-lightning-vortex not found in kit_mapping after insert"

mj = json.loads(row_vortex[0])

# Locate "Lightning Vortex" skill
lightning_vortex_skill = None
for skill in mj.get("skills", []):
    if skill.get("source_skill") == "Lightning Vortex":
        lightning_vortex_skill = skill
        break

assert lightning_vortex_skill is not None, "ABORT: 'Lightning Vortex' skill not found in mapping_json"

# Verify pre-errata state matches expectation
assert lightning_vortex_skill["element_primary"] is None, \
    f"Expected element_primary=null before errata, got {lightning_vortex_skill['element_primary']!r}"
assert lightning_vortex_skill["ailments"] == ["shock"], \
    f"Expected ailments=['shock'] before errata, got {lightning_vortex_skill['ailments']!r}"

# Apply errata
lightning_vortex_skill["element_primary"] = "lightning"
lightning_vortex_skill["ailments"] = []

# Verify post-errata state
assert lightning_vortex_skill["element_primary"] == "lightning"
assert lightning_vortex_skill["ailments"] == []

mj_updated = json.dumps(mj, ensure_ascii=False, separators=(",", ":"))
cur.execute(
    "UPDATE kit_mapping SET mapping_json=? WHERE kit_id='ud-lightning-vortex'",
    (mj_updated,)
)
con.commit()
print("MAP-ERRATA-1 applied: ud-lightning-vortex / Lightning Vortex — element_primary=lightning, ailments=[]")

# Verify grade and terminal_state unchanged
cur.execute("SELECT grade, terminal_state FROM kit_mapping WHERE kit_id='ud-lightning-vortex'")
grade_ts = cur.fetchone()
assert grade_ts[0] == "CLOSE", f"Expected grade=CLOSE, got {grade_ts[0]!r}"
assert grade_ts[1] == "MAPPED", f"Expected terminal_state=MAPPED, got {grade_ts[1]!r}"
print(f"MAP-ERRATA-1 guard: grade={grade_ts[0]}, terminal_state={grade_ts[1]} (unchanged — correct)")

# ---------------------------------------------------------------------------
# 1c. R-M7 biconditional assert: COUNT(GAPPED)==COUNT(MAPPED_DOCKET)==31
#     scoped to the 125 new rows
# ---------------------------------------------------------------------------
new_kit_ids = [r["kit_id"] for r in rows]
placeholders = ",".join("?" * len(new_kit_ids))

cur.execute(
    f"SELECT COUNT(*) FROM kit_mapping WHERE grade='GAPPED' AND kit_id IN ({placeholders})",
    new_kit_ids
)
gapped_count = cur.fetchone()[0]

cur.execute(
    f"SELECT COUNT(*) FROM kit_mapping WHERE terminal_state='MAPPED_DOCKET' AND kit_id IN ({placeholders})",
    new_kit_ids
)
docket_count = cur.fetchone()[0]

print(f"R-M7 assert: COUNT(grade='GAPPED')={gapped_count}, COUNT(terminal_state='MAPPED_DOCKET')={docket_count}")
assert gapped_count == 31, f"R-M7 FAIL: GAPPED={gapped_count}, expected 31"
assert docket_count == 31, f"R-M7 FAIL: MAPPED_DOCKET={docket_count}, expected 31"
assert gapped_count == docket_count, f"R-M7 FAIL: GAPPED({gapped_count}) != MAPPED_DOCKET({docket_count})"
print("R-M7 PASS: 31 == 31")

# ---------------------------------------------------------------------------
# Grade histogram (new rows only)
# ---------------------------------------------------------------------------
cur.execute(
    f"SELECT grade, COUNT(*) FROM kit_mapping WHERE kit_id IN ({placeholders}) GROUP BY grade ORDER BY grade",
    new_kit_ids
)
histogram = cur.fetchall()
print("Grade histogram (new 125 rows):")
for grade, cnt in histogram:
    print(f"  {grade}: {cnt}")

# ---------------------------------------------------------------------------
# TIER 2 HOLD: verify mechanic_gap_docket and mint_ledger unchanged
# ---------------------------------------------------------------------------
cur.execute("SELECT COUNT(*) FROM mechanic_gap_docket")
docket_total = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM mint_ledger")
mint_total = cur.fetchone()[0]
print(f"mechanic_gap_docket rows (unchanged): {docket_total}")
print(f"mint_ledger rows (unchanged): {mint_total}")
assert docket_total == 8, f"ABORT: mechanic_gap_docket expected 8, got {docket_total}"
assert mint_total == 6, f"ABORT: mint_ledger expected 6, got {mint_total}"

# ---------------------------------------------------------------------------
# Final totals
# ---------------------------------------------------------------------------
cur.execute("SELECT COUNT(*) FROM kit_mapping")
final_total = cur.fetchone()[0]
print(f"\nFinal kit_mapping total: {final_total}")
assert final_total == 574, f"Expected 574 total, got {final_total}"

con.close()
print("\nINGEST-18 COMPLETE — all assertions passed.")
