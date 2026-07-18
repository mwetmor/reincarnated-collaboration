#!/usr/bin/env python3
"""
VDM-1 ingest wave 5 — SECOND kit_mapping wave (PoE1 mapping batches 05-08).

Elrond (data steward, SINGLE WRITER of corpus.db).

SCOPE — one job this ingest: land the second kit_mapping wave (46 rows) from
stage2/poe1/mapping-batch-0{5,6,7,8}.jsonl. Steward-audited, ZERO re-grades — the
committed files ARE the audited state. NO stage-1 batches, NO errata, NO backfill,
NO promotions this wave (those all landed at ingest-4). Follows the ingest-4
kit_mapping path (corpus_vdm1_ingest4_2026_07_18.py part 5) exactly, with the same
serialization + provenance-default convention.

Row shape (matches wave-1 / ingest-4):
  kit_id, mapping_json (nested dict -> json.dumps text), grade, deviation_notes,
  terminal_state. mapping_provenance defaults to 'authored-vdm1' (the kit_mapping
  run-tag convention — the table has no run_tag column; provenance IS the tag).
  authored_date defaults to date('now').

  batch-05 = 12 rows, batch-06 = 12, batch-07 = 12, batch-08 = 10  -> 46 rows.

GUARD — INSERT ONLY (dispatch LAW): if ANY of the 46 kit_ids already has a
kit_mapping row, HALT and report (NO upsert). Enforced as a pre-write assert against
the live DB (existing kit_mapping kit set) BEFORE the write txn opens.

Post-ingest asserts (dispatch):
  - kit_mapping total = 94 (48 wave-1 + 46 wave-2), one row per PoE1 kit, 0 collisions
  - grade histogram over ALL 94 = EXACT 2 / CLOSE 62 / APPROX 22 / GAPPED 8
  - R-M7 1:1 in DB: terminal_state='MAPPED_DOCKET' <=> grade='GAPPED', count 8, kit
    set exactly {aurabot, detonate-dead, forbidden-rite, heavy-strike-stun, spectres,
    ward-loop, wild-strike, wormblaster}
  - mint_ledger and mechanic_gap_docket REMAIN 0 rows (candidate side-files are NOT
    ingested this wave — steward ratification lands at ingest-6)
  - journal_mode still DELETE

Charter laws honored:
  - No silent transformation: no re-grades; the audited file state is truth. Every
    row loaded verbatim (mapping_json serialized 1:1, no field drop/rewrite).
  - Reversible: raw JSONL inputs committed + static; reproducible against the
    pre-ingest5 backup.
  - journal_mode stays DELETE (readonly crawlers run concurrently between sessions;
    NEVER flipped to WAL).
  - Short write txn: all validation before the single BEGIN IMMEDIATE..COMMIT;
    index.lock retry on the write handle (wait 30s, retry 3x) per dispatch LAW.

Usage:
  python3 corpus_vdm1_ingest5_2026_07_18.py           # dry-run (validate + report, no writes)
  python3 corpus_vdm1_ingest5_2026_07_18.py --apply   # execute the single write txn
"""
import argparse
import json
import sqlite3
import sys
import time
from pathlib import Path

REPO = Path("/Users/admin/Games/reincarnated-collaboration")
DB = REPO / "agentic_orchestration/research/curated/corpus.db"
S2 = REPO / "agentic_orchestration/research/vdm1/stage2/poe1"
MAP_BATCHES = ["05", "06", "07", "08"]

# ---- CHECK enums mirrored from schema (validate before insert) ----
MAP_GRADE = {"EXACT", "CLOSE", "APPROX", "GAPPED"}
MAP_TERMINAL = {"MAPPED", "MAPPED_DOCKET"}

# ---- dispatch file-truth constants (whole-DB post-wave-2) ----
EXPECT_TOTAL = 94                      # 48 wave-1 + 46 wave-2
EXPECT_WAVE2 = 46
EXPECT_GRADE_HIST = {"EXACT": 2, "CLOSE": 62, "APPROX": 22, "GAPPED": 8}
EXPECT_DOCKET = 8
EXPECT_GAPPED_SET = {
    "poe1-aurabot", "poe1-detonate-dead", "poe1-forbidden-rite",
    "poe1-heavy-strike-stun", "poe1-spectres", "poe1-ward-loop",
    "poe1-wild-strike", "poe1-wormblaster",
}
# per-batch expected line counts (guards mis-split / truncated inputs)
EXPECT_BATCH = {"05": 12, "06": 12, "07": 12, "08": 10}


def load_jsonl(path):
    rows = []
    for ln, line in enumerate(path.read_text().splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        rows.append((ln, json.loads(line)))   # raises on any malformed line
    return rows


def connect_with_retry(path, attempts=3, wait=30):
    """Open the write connection; on a locked DB (index.lock / database is locked)
    wait `wait`s and retry up to `attempts` times per dispatch LAW."""
    last = None
    for i in range(1, attempts + 1):
        try:
            con = sqlite3.connect(str(path), timeout=wait)
            con.execute("PRAGMA foreign_keys=ON;")
            con.execute("BEGIN IMMEDIATE;")   # probe the lock early, then release
            con.execute("COMMIT;")
            return con
        except sqlite3.OperationalError as e:
            last = e
            if "lock" in str(e).lower() and i < attempts:
                print(f"   [lock] attempt {i}/{attempts}: {e} -> wait {wait}s, retry")
                time.sleep(wait)
                continue
            raise
    raise last


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="execute writes (default: dry-run)")
    args = ap.parse_args()

    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    con.execute("PRAGMA foreign_keys=ON;")

    # ground truth snapshots
    dbkits = set(r[0] for r in con.execute("SELECT kit_id FROM canon_corpus"))
    existing_km = set(r[0] for r in con.execute("SELECT kit_id FROM kit_mapping"))
    pre_km = con.execute("SELECT COUNT(*) FROM kit_mapping").fetchone()[0]
    pre_mint = con.execute("SELECT COUNT(*) FROM mint_ledger").fetchone()[0]
    pre_docket = con.execute("SELECT COUNT(*) FROM mechanic_gap_docket").fetchone()[0]
    jm_pre = con.execute("PRAGMA journal_mode;").fetchone()[0]

    log = {"mapping": 0, "rejects": [], "collisions": []}

    # ---------- VALIDATE + STAGE kit_mapping inserts (second wave) ----------
    map_ins = []
    grade_hist = {g: 0 for g in MAP_GRADE}
    term_hist = {t: 0 for t in MAP_TERMINAL}
    gapped_kits, docket_kits, map_kits = [], [], []
    per_batch = {}
    for b in MAP_BATCHES:
        rows = load_jsonl(S2 / f"mapping-batch-{b}.jsonl")
        per_batch[b] = len(rows)
        for ln, r in rows:
            kit = r.get("kit_id"); grade = r.get("grade"); term = r.get("terminal_state")
            if kit not in dbkits or grade not in MAP_GRADE or term not in MAP_TERMINAL:
                log["rejects"].append(("mapping", b, ln, "enum/FK", r)); continue
            # INSERT-ONLY guard (dispatch LAW): no upsert. Collision => record; HALT below.
            if kit in existing_km:
                log["collisions"].append((b, ln, kit)); continue
            mj = r.get("mapping_json")
            mj_str = None if mj is None else json.dumps(mj, ensure_ascii=False)
            map_ins.append((kit, mj_str, grade, r.get("deviation_notes"), term))
            grade_hist[grade] += 1
            term_hist[term] += 1
            map_kits.append(kit)
            if grade == "GAPPED":
                gapped_kits.append(kit)
            if term == "MAPPED_DOCKET":
                docket_kits.append(kit)
    log["mapping"] = len(map_ins)

    # in-file dup guard (defensive; wave uses PK anyway)
    infile_dupes = sorted({k for k in map_kits if map_kits.count(k) > 1})

    # ---------- report ----------
    print("=== VDM-1 ingest wave 5 (%s) ===" % ("APPLY" if args.apply else "DRY-RUN"))
    print("journal_mode (pre):", jm_pre)
    print("per-batch line counts:", per_batch, "(expect", EXPECT_BATCH, ")")
    print("kit_mapping wave-2 staged for insert:", log["mapping"])
    print("  wave-2 grade histogram:", grade_hist)
    print("  wave-2 terminal histogram:", term_hist)
    print("  wave-2 GAPPED kits:", sorted(gapped_kits))
    print("  wave-2 MAPPED_DOCKET kits:", sorted(docket_kits))
    print("  wave-2 distinct kit_ids:", len(set(map_kits)))
    print("pre-ingest kit_mapping total:", pre_km,
          "| mint_ledger:", pre_mint, "| mechanic_gap_docket:", pre_docket)
    print("rejects (malformed enum/FK):", len(log["rejects"]))
    for rj in log["rejects"]:
        print("   REJECT", rj[:4])
    print("PK collisions vs live kit_mapping (INSERT-only guard):", len(log["collisions"]))
    for c in log["collisions"]:
        print("   COLLISION", c)

    # ---------- pre-write asserts (staged / file-truth) ----------
    # HALT hard on any collision (dispatch LAW: INSERT only, no upsert).
    assert not log["collisions"], (
        "INSERT-ONLY GUARD TRIPPED — one or more wave-2 kit_ids already have a "
        "kit_mapping row. HALT (no upsert). Collisions: %s" % log["collisions"])
    assert not log["rejects"], f"rejects present: {log['rejects']}"
    assert not infile_dupes, f"in-file duplicate kit_ids: {infile_dupes}"
    for b in MAP_BATCHES:
        assert per_batch[b] == EXPECT_BATCH[b], \
            f"batch-{b} line count {per_batch[b]} != {EXPECT_BATCH[b]}"
    assert log["mapping"] == EXPECT_WAVE2, f"staged {log['mapping']} != {EXPECT_WAVE2}"
    assert len(set(map_kits)) == EXPECT_WAVE2, \
        f"distinct wave-2 kits {len(set(map_kits))} != {EXPECT_WAVE2}"
    # wave-2 in-file R-M7 1:1
    assert sorted(docket_kits) == sorted(gapped_kits), \
        "wave-2 R-M7 1:1: MAPPED_DOCKET rows must equal GAPPED rows exactly (in-file)"

    if not args.apply:
        # projected whole-DB post-state (in-memory; no write)
        proj_total = pre_km + log["mapping"]
        print("\nprojected post-wave kit_mapping total:", proj_total, "(expect", EXPECT_TOTAL, ")")
        assert proj_total == EXPECT_TOTAL, f"projected total {proj_total} != {EXPECT_TOTAL}"
        print("DRY-RUN complete. Re-run with --apply to write.")
        con.close()
        return

    con.close()  # close readonly handle before opening write handle

    # ---------- single short write txn (write handle with index.lock retry) ----------
    wcon = connect_with_retry(DB)
    try:
        wcon.execute("BEGIN IMMEDIATE;")
        wcon.executemany(
            "INSERT INTO kit_mapping "
            "(kit_id, mapping_json, grade, deviation_notes, terminal_state) "
            "VALUES (?,?,?,?,?)", map_ins)
        wcon.commit()
    except Exception:
        wcon.rollback()
        raise

    # ---------- POST-write asserts (whole-DB, dispatch file-truths) ----------
    post_km = wcon.execute("SELECT COUNT(*) FROM kit_mapping").fetchone()[0]
    post_distinct = wcon.execute("SELECT COUNT(DISTINCT kit_id) FROM kit_mapping").fetchone()[0]
    post_mint = wcon.execute("SELECT COUNT(*) FROM mint_ledger").fetchone()[0]
    post_docket_tbl = wcon.execute("SELECT COUNT(*) FROM mechanic_gap_docket").fetchone()[0]
    # whole-DB grade histogram
    db_grade_hist = {g: 0 for g in MAP_GRADE}
    for g, c in wcon.execute("SELECT grade, COUNT(*) FROM kit_mapping GROUP BY grade"):
        db_grade_hist[g] = c
    # R-M7 1:1: MAPPED_DOCKET set vs GAPPED set (whole-DB)
    db_docket = set(r[0] for r in wcon.execute(
        "SELECT kit_id FROM kit_mapping WHERE terminal_state='MAPPED_DOCKET'"))
    db_gapped = set(r[0] for r in wcon.execute(
        "SELECT kit_id FROM kit_mapping WHERE grade='GAPPED'"))
    # cross-check: no row where GAPPED xor MAPPED_DOCKET (grade<->terminal coherence)
    incoherent = wcon.execute(
        "SELECT COUNT(*) FROM kit_mapping "
        "WHERE (grade='GAPPED') <> (terminal_state='MAPPED_DOCKET')").fetchone()[0]
    orph_km = wcon.execute(
        "SELECT COUNT(*) FROM kit_mapping m WHERE NOT EXISTS "
        "(SELECT 1 FROM canon_corpus c WHERE c.kit_id=m.kit_id)").fetchone()[0]
    # provenance default landed on the new rows
    prov_bad = wcon.execute(
        "SELECT COUNT(*) FROM kit_mapping WHERE mapping_provenance != 'authored-vdm1'"
    ).fetchone()[0]
    jm = wcon.execute("PRAGMA journal_mode;").fetchone()[0]
    ic = wcon.execute("PRAGMA integrity_check;").fetchone()[0]
    fk = wcon.execute("PRAGMA foreign_key_check;").fetchall()

    assert post_km == pre_km + EXPECT_WAVE2 == EXPECT_TOTAL, \
        f"kit_mapping {post_km} != {pre_km}+{EXPECT_WAVE2} (expect {EXPECT_TOTAL})"
    assert post_distinct == EXPECT_TOTAL, \
        f"distinct kit_ids {post_distinct} != {EXPECT_TOTAL} (one row per PoE1 kit)"
    assert db_grade_hist == EXPECT_GRADE_HIST, \
        f"whole-DB grade histogram {db_grade_hist} != {EXPECT_GRADE_HIST}"
    assert len(db_docket) == EXPECT_DOCKET, \
        f"MAPPED_DOCKET count {len(db_docket)} != {EXPECT_DOCKET}"
    assert db_docket == db_gapped == EXPECT_GAPPED_SET, (
        "R-M7 1:1 law: MAPPED_DOCKET set == GAPPED set == expected 8-kit set. "
        f"docket={sorted(db_docket)} gapped={sorted(db_gapped)}")
    assert incoherent == 0, f"{incoherent} rows violate grade<->terminal coherence"
    assert orph_km == 0, f"{orph_km} kit_mapping orphans (FK to canon_corpus)"
    assert prov_bad == 0, f"{prov_bad} rows lack mapping_provenance='authored-vdm1'"
    # side-files NOT ingested this wave — mint_ledger + mechanic_gap_docket stay 0
    assert post_mint == pre_mint == 0, f"mint_ledger changed {pre_mint}->{post_mint} (must stay 0)"
    assert post_docket_tbl == pre_docket == 0, \
        f"mechanic_gap_docket changed {pre_docket}->{post_docket_tbl} (must stay 0)"
    assert jm == "delete", f"journal_mode {jm} != delete"
    assert ic == "ok", f"integrity_check {ic}"
    assert fk == [], f"foreign_key_check {fk}"

    print("\n=== APPLIED ===")
    print(f"kit_mapping    {pre_km} -> {post_km}  (+{post_km-pre_km})")
    print("whole-DB grade histogram:", db_grade_hist)
    print("MAPPED_DOCKET == GAPPED == 8-kit set:", sorted(db_docket))
    print("grade<->terminal incoherent rows:", incoherent)
    print("mint_ledger:", post_mint, "| mechanic_gap_docket:", post_docket_tbl, "(both stay 0)")
    print("journal_mode:", jm, "| integrity_check:", ic, "| foreign_key_check:", fk)
    wcon.close()


if __name__ == "__main__":
    sys.exit(main())
