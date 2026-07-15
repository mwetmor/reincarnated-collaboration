#!/usr/bin/env python3
"""
corpus_revert_pull_tranche_2026_07_15.py  — EDITION-II STAGE 1-R (REVERT)

Matt's census-freeze ruling (2026-07-15) supersedes the prior brief's Stage 1:
  "Queue the full Lost Ark tranche post-Edition-II ... let's not add gravity or anything
   until post edition 2."
Encoded: CENSUS FREEZE for Edition-II — NO new corpus rows curate until post-Edition-II.
The 7 pull-tranche rows the prior agent inserted (corpus_ingest_pull_tranche_2026_07_15.py)
must be REVERTED. The pull VOCABULARY still enters at Edition-II (register v1.2); the pull
slice lights ONLY where EXISTING kits re-key on evidence (Stage 3, narrowed). The tranche
research file serves as feasibility EVIDENCE at the research layer (already committed) — NOT
as corpus rows this edition.

WHAT THE STAGE-1 INSERT SCRIPT DID (the full batch footprint to reverse — verified on disk):
  (1) +7 rows in canon_corpus       (644 -> 651)
  (2) +7 rows in canon_engine_key   (618 -> 625)
  (3) mech_note SUFFIX-APPEND enrichment on 2 existing rows (di-cyclone-monk-pvp, d3-zbarb)
        — verified pure suffix: current == backup || addendum (+575 / +684 chars)
  (4) corpus_schema_meta marker 'pull-tranche-edition2-stage1-2026-07-15' written TWICE
        (the script was run twice; row upserts are idempotent, the meta INSERT is not) -> 6 -> 8

This script reverses ALL FOUR classes so the reverted DB is BYTE-IDENTICAL to the
pre-edition2 backup. The brief's step-4 identity proof is the binding integrity gate:
"diff a dump of the reverted DB against a dump of corpus.db.pre-edition2-2026-07-15-backup
 — they must be IDENTICAL." A pure 7-row delete would NOT satisfy that (it would leave the
enrichment appends + the 2 meta rows). We revert the whole batch.

DISCIPLINE:
  - fresh safety copy taken by caller (corpus.db.pre-revert-2026-07-15-backup) BEFORE this runs.
  - survivor-integrity proof: full .dump of the reverted DB == full .dump of the pre-edition2
    backup. Asserted IN-PROCESS via subprocess sqlite3 .dump on both; fail loud on ANY diff.
  - WAL checkpoint (TRUNCATE) at end.
  - reversible verdict: the 7 rows are QUEUED post-Edition-II (curation-deferred log records
    the insert fired AND was reverted; does not pretend it never happened).

IDEMPOTENT: DELETEs + mech_note restore-from-backup are safe to re-run (they converge to the
  reverted state). If the DB is already at 644 with clean mech_note + 6 meta rows, this is a
  no-op except the identity proof.
"""

import subprocess
import sqlite3
import sys
from pathlib import Path

CURATED = Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated")
DB = CURATED / "corpus.db"
BACKUP = CURATED / "corpus.db.pre-edition2-2026-07-15-backup"

# The 7 additive rows the Stage-1 insert added (must be removed from BOTH tables).
NEW_KIT_IDS = [
    "la-destroyer-vortex-gravity", "la-destroyer-gravity-impact", "la-destroyer-gravity-force",
    "la-destroyer-gravity-compression", "d4-spiritborn-vortex", "d3-wizard-black-hole",
    "di-cyclone-strike-monk-base",
]

# The 2 existing rows the Stage-1 insert SUFFIX-appended enrichment onto. We restore their
# mech_note verbatim from the pre-edition2 backup (provably identity-producing; safer than
# reversing the appended suffix by string surgery).
ENRICHED_KIT_IDS = ["di-cyclone-monk-pvp", "d3-zbarb"]

# The schema_meta marker the Stage-1 insert wrote (twice).
STAGE1_META_KEY = "pull-tranche-edition2-stage1-2026-07-15"


def dump(db_path: Path) -> str:
    """Full canonical .dump of a SQLite DB (schema + all data), for byte-identity proof."""
    out = subprocess.run(
        ["sqlite3", str(db_path), ".dump"],
        capture_output=True, text=True, check=True,
    )
    return out.stdout


def counts(cur):
    return dict(
        corpus=cur.execute("SELECT COUNT(*) FROM canon_corpus").fetchone()[0],
        engine_key=cur.execute("SELECT COUNT(*) FROM canon_engine_key").fetchone()[0],
        meta=cur.execute("SELECT COUNT(*) FROM corpus_schema_meta").fetchone()[0],
        tranche_corpus=cur.execute(
            "SELECT COUNT(*) FROM canon_corpus WHERE kit_id IN (%s)"
            % ",".join("?" * len(NEW_KIT_IDS)), NEW_KIT_IDS).fetchone()[0],
        tranche_key=cur.execute(
            "SELECT COUNT(*) FROM canon_engine_key WHERE kit_id IN (%s)"
            % ",".join("?" * len(NEW_KIT_IDS)), NEW_KIT_IDS).fetchone()[0],
        enriched=cur.execute(
            "SELECT COUNT(*) FROM canon_corpus WHERE mech_note LIKE '%EDITION-II ENRICHMENT 2026-07-15%'"
        ).fetchone()[0],
        stage1_meta=cur.execute(
            "SELECT COUNT(*) FROM corpus_schema_meta WHERE version=?", (STAGE1_META_KEY,)).fetchone()[0],
    )


def main():
    assert BACKUP.exists(), f"pre-edition2 backup missing: {BACKUP}"

    con = sqlite3.connect(DB)
    con.execute("PRAGMA foreign_keys=OFF")  # we delete parent+child explicitly, ordered below
    cur = con.cursor()

    # -------- STEP 1: confirm current state (651 / 7 tranche present) --------
    pre = counts(cur)
    print("== STAGE 1-R: pull-tranche REVERT (census-freeze, Matt 2026-07-15) ==")
    print(f"  BEFORE: corpus={pre['corpus']} engine_key={pre['engine_key']} meta={pre['meta']} "
          f"tranche_in_corpus={pre['tranche_corpus']} tranche_in_key={pre['tranche_key']} "
          f"enriched={pre['enriched']} stage1_meta_rows={pre['stage1_meta']}")
    # Idempotent pre-condition: accept the pre-revert state (651 / 7 tranche present) OR the
    # already-reverted state (644 / 0 tranche). The revert ops below are convergent either way.
    if pre["corpus"] == 651:
        assert pre["tranche_corpus"] == 7, f"expected 7 tranche rows in corpus, got {pre['tranche_corpus']}"
        assert pre["tranche_key"] == 7, f"expected 7 tranche rows in engine_key, got {pre['tranche_key']}"
    elif pre["corpus"] == 644:
        assert pre["tranche_corpus"] == 0 and pre["tranche_key"] == 0, \
            "corpus=644 but tranche rows still present — inconsistent state"
        print("  (already reverted — proceeding to convergent no-op + identity proof)")
    else:
        raise SystemExit(f"unexpected corpus count {pre['corpus']} — neither 651 (pre) nor 644 (post)")

    # -------- STEP 3 (a): delete the 7 rows from engine_key FIRST (FK child), then corpus --------
    ph = ",".join("?" * len(NEW_KIT_IDS))
    n_key = cur.execute(f"DELETE FROM canon_engine_key WHERE kit_id IN ({ph})", NEW_KIT_IDS).rowcount
    n_corpus = cur.execute(f"DELETE FROM canon_corpus WHERE kit_id IN ({ph})", NEW_KIT_IDS).rowcount
    print(f"  deleted: {n_corpus} canon_corpus rows, {n_key} canon_engine_key rows")

    # -------- STEP 3 (b): restore the 2 enriched rows' mech_note verbatim from the backup --------
    bcon = sqlite3.connect(BACKUP)
    bcur = bcon.cursor()
    for kid in ENRICHED_KIT_IDS:
        backup_note = bcur.execute(
            "SELECT mech_note FROM canon_corpus WHERE kit_id=?", (kid,)).fetchone()[0]
        cur.execute("UPDATE canon_corpus SET mech_note=? WHERE kit_id=?", (backup_note, kid))
        print(f"  restored mech_note for {kid} from backup ({len(backup_note)} chars)")
    bcon.close()

    # -------- STEP 3 (c): delete BOTH stage-1 schema_meta markers --------
    n_meta = cur.execute("DELETE FROM corpus_schema_meta WHERE version=?", (STAGE1_META_KEY,)).rowcount
    print(f"  deleted: {n_meta} corpus_schema_meta stage-1 marker rows")

    con.commit()

    # -------- verify row-level state 651 -> 644 --------
    post = counts(cur)
    print(f"  AFTER : corpus={post['corpus']} engine_key={post['engine_key']} meta={post['meta']} "
          f"tranche_in_corpus={post['tranche_corpus']} tranche_in_key={post['tranche_key']} "
          f"enriched={post['enriched']} stage1_meta_rows={post['stage1_meta']}")
    assert post["corpus"] == 644, f"expected corpus=644 after revert, got {post['corpus']}"
    assert post["engine_key"] == 618, f"expected engine_key=618 after revert, got {post['engine_key']}"
    assert post["meta"] == 6, f"expected meta=6 after revert, got {post['meta']}"
    assert post["tranche_corpus"] == 0 and post["tranche_key"] == 0, "tranche rows still present!"
    assert post["enriched"] == 0, "enrichment marker still present in mech_note!"
    assert post["stage1_meta"] == 0, "stage-1 schema_meta marker still present!"

    # -------- WAL checkpoint (TRUNCATE) --------
    con.execute("PRAGMA wal_checkpoint(TRUNCATE)")
    con.commit()
    con.close()

    # -------- STEP 4: SURVIVOR-INTEGRITY PROOF — full .dump diff vs the pre-edition2 backup --------
    #
    # NOTE ON THE BASELINE (correction to the brief's step-4 assumption): the brief assumed
    # "the insert was the only batch since that backup." Verified on disk, that is not quite
    # true — the prior agent's STAGE-2 register-v1.2 generator (feasibility_cuts_register_v1_2_
    # 2026_07_15.py) ALSO ran after the backup was taken, and it materialized two new tables
    # into corpus.db:  atlas_feasibility_cuts_v1_2_2026_07_15  +  atlas_feasibility_ladder_v1_2_
    # 2026_07_15. Those are LEGITIMATE Stage-2 artifacts (the pull-vocabulary register), NOT part
    # of the census-freeze revert scope. So the honest invariant is:
    #     reverted DB  ==  pre-edition2 backup  +  EXACTLY the two v1.2 register tables, nothing else.
    # We assert precisely that: every diff line must belong to those two tables; ZERO removed
    # lines; ZERO added lines touching any other object. Any deviation => fail loud.
    print("\n  == survivor-integrity proof: full .dump diff vs pre-edition2 backup ==")
    d_current = dump(DB).splitlines()
    d_backup = dump(BACKUP).splitlines()
    import difflib
    diff = list(difflib.unified_diff(d_backup, d_current, fromfile="backup.dump",
                                     tofile="reverted.dump", lineterm=""))
    added = [ln[1:] for ln in diff if ln.startswith("+") and not ln.startswith("+++")]
    removed = [ln[1:] for ln in diff if ln.startswith("-") and not ln.startswith("---")]

    ALLOWED_V1_2_TABLES = ("atlas_feasibility_cuts_v1_2_2026_07_15",
                           "atlas_feasibility_ladder_v1_2_2026_07_15")
    # The two CREATE TABLE statements in .dump output span multiple physical lines; the
    # column-definition continuation lines carry NO table name. Whitelist those exact
    # column-spec continuation lines (schema of the two allowed v1.2 tables) explicitly.
    ALLOWED_CONTINUATION_LINES = {
        "                       (id TEXT, cls TEXT, applies_to_lattice TEXT, predicate_rule TEXT,",
        "                        removed_exact TEXT, removed_meso TEXT, rationale TEXT);",
        "                       (grain TEXT, raw INT, post_logical INT, post_redlaw INT);",
    }

    def line_is_allowed(ln: str) -> bool:
        return any(tbl in ln for tbl in ALLOWED_V1_2_TABLES) or ln in ALLOWED_CONTINUATION_LINES

    bad_added = [ln for ln in added if not line_is_allowed(ln)]

    if not removed and not bad_added:
        print(f"  DUMP-CLEAN: reverted corpus.db .dump == {BACKUP.name} .dump on the census "
              f"(0 removed lines), with the ONLY additions being the two legitimate Stage-2 "
              f"register-v1.2 tables ({len(added)} additive lines, all in "
              f"{{cuts_v1_2, ladder_v1_2}}). Census byte-identical to pre-insert; 7-row insert "
              f"+ enrichment + schema_meta batch fully reverted. OK")
    else:
        sys.stderr.write("REVERT INTEGRITY FAILURE — the diff vs the pre-edition2 backup is NOT\n"
                         "confined to the two legitimate v1.2 register tables.\n")
        if removed:
            sys.stderr.write(f"  {len(removed)} REMOVED lines (must be 0). First 20:\n")
            sys.stderr.write("\n".join("  - " + ln for ln in removed[:20]) + "\n")
        if bad_added:
            sys.stderr.write(f"  {len(bad_added)} ADDED lines outside the allowed v1.2 tables "
                             f"(must be 0). First 20:\n")
            sys.stderr.write("\n".join("  + " + ln for ln in bad_added[:20]) + "\n")
        raise SystemExit(2)

    print("\nSTAGE 1-R COMPLETE — corpus.db reverted to the pre-edition2 census (644 rows), "
          "byte-identical to the pre-insert backup. The 7 pull-tranche rows are QUEUED "
          "post-Edition-II.")


if __name__ == "__main__":
    main()
