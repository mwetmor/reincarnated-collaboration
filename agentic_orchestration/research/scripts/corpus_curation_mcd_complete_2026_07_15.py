#!/usr/bin/env python3
"""
corpus_curation_mcd_complete_2026_07_15.py

COMPLETE the MCD Mode-B curation that corpus_ingest_mcd_2026_07_15.py started.
The prior elrond run ingested all 120 mcd rows (canon_tier=shallow, cell_keys for the
94 keyable, flags carrying the annotations) but its API stream timed out mid-run before
the ANNOTATIONS were promoted from the flags JSON blob to first-class queryable columns.

Gandalf mapped the exact residual state (post-WAL-checkpoint, DB consistent). This script
finishes ONLY the remaining first-class-column promotion. It is:

  ADDITIVE   — two new columns, populated on mcd rows only. No survivor row touched.
  IDEMPOTENT — re-run -> columns already exist (guarded), values re-set to identical.
  MCD-SCOPED — every UPDATE is `WHERE game='mcd'` (or the explicit 6-kit pull set).

WHAT THIS SCRIPT DOES (the 2 landings the timeout skipped):

  1. architecture='notable'  as a FIRST-CLASS COLUMN on all 120 mcd rows.
     WHY a column, not just the flags token: the INGEST was granted on 3 architectural
     grains (classless gear-only kit architecture, unconstrained pull economy,
     closed-feedback-loop power curve). Consumers MUST be able to find these rows.
     The annotation currently lives ONLY inside the flags JSON array
     (["depth:shallow","architecture:notable",...]) — a fragile substring match that
     gandalf's named-column search (correctly) did not see. Discipline #14 (tagged, not
     encoded): explicit tag column over meaning packed in a blob. This gives
     `WHERE architecture='notable'` the same first-class status `canon_tier='shallow'`
     already has. The flags token is LEFT in place (redundant provenance, non-destructive).

  2. pull_pending_vocab  as a FIRST-CLASS INTEGER column (1 on the 6 pull kits, 0 else).
     WHY: a consumer must distinguish "unresolved because pull vocabulary is pending the
     Edition-II pass" from "unresolved because the artifact note is a thin category-page
     one-liner". Both are unresolved=1 today. The distinction lived only in the flags blob
     (pull_pending_vocab:true + unmapped_pending_curation:pull_pending_vocab). Promote it
     so `WHERE unresolved=1 AND pull_pending_vocab=1` = the 6 frozen-basis pull kits, and
     `WHERE unresolved=1 AND pull_pending_vocab=0` = the 20 thin artifacts.

WHAT THIS SCRIPT DELIBERATELY DOES NOT DO:

  - NO re-ingest. The 120 rows + 94 cell_keys already exist. Re-running the ingest would
    duplicate/churn; this script only promotes annotations.
  - NO lattice_coord population (the "rekey pass"). DEFERRED — see the curation log. The
    displacement/ghost field emitters read canon_engine_key.cell_key (which MCD ALREADY
    has, survivor-compatible, 94 well-formed 14-field keys satisfying the emitter
    predicate), NOT lattice_coord. lattice_coord is consumed by nothing today. Firing it
    now would be off-critical-path materialization risking divergence from the
    authoritative cell_key. Queued for the next atlas-derivation batch.
  - NO change to the 2 kc=4 rows' coords. Both (mcd-mechanized-sawblade, mcd-voidcaller)
    are honest NULLs: attr_val is NULL on ALL 120 mcd (classless game, no STR/DEX/INT/WIS
    grain) so the mcd ceiling is kc=5; these two additionally lack a numeric `speed` stat
    in prose ("Power unspecified") -> tempo_val NULL -> kc=4. Nothing to complete; there is
    no data to key without inventing it (never-invent discipline).
  - NO change to suffix_rekey_status. MCD carries no geo_raw/ctrl_raw/def_raw/econ_raw
    suffix descriptors (it was keyed from prose, not a suffix-descriptor harvest), so the
    field's literal meaning (raw-descriptor rekey pending) is inapplicable; the default
    'awaiting-rekey' is harmless and correctly signals "not yet promoted to the survivors'
    keyed-v1 lattice standard." Left as-is.

BACKUP: corpus.db.pre-mcd-2026-07-15-backup already exists (pre-ingest). This script makes
  NO destructive change (two additive columns, mcd-only writes), so per the dispatch a
  re-backup is not required.
"""

import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent  # -> reincarnated-collaboration
DB = ROOT / "agentic_orchestration/research/curated/corpus.db"

PULL_KITS = (
    "mcd-hammer-of-gravity", "mcd-encrusted-anchor", "mcd-echo-of-the-valley",
    "mcd-burst-gale-bow", "mcd-imploding-crossbow", "mcd-voidcaller",
)


def column_exists(conn, table, col):
    return any(r[1] == col for r in conn.execute(f"PRAGMA table_info({table})"))


def main():
    if not DB.exists():
        sys.exit(f"corpus.db not found at {DB}")
    conn = sqlite3.connect(str(DB))
    conn.row_factory = sqlite3.Row

    # -- hard-constraint baseline: survivor cell_keys must be byte-identical after run --
    def survivor_sha():
        rows = conn.execute(
            "SELECT k.kit_id||'|'||COALESCE(k.cell_key,'') "
            "FROM canon_engine_key k JOIN canon_corpus c ON c.kit_id=k.kit_id "
            "WHERE k.row_class='combat-kit' AND c.negative=0 AND c.game!='mcd' "
            "ORDER BY k.kit_id"
        ).fetchall()
        import hashlib
        h = hashlib.sha256()
        for r in rows:
            h.update((r[0] + "\n").encode())
        return h.hexdigest()

    sha_before = survivor_sha()

    # ---- 1. architecture (first-class) ----
    if not column_exists(conn, "canon_corpus", "architecture"):
        conn.execute("ALTER TABLE canon_corpus ADD COLUMN architecture TEXT")
    # Landing: all 120 mcd rows carry the INGEST-granting architectural grain label.
    n_arch = conn.execute(
        "UPDATE canon_corpus SET architecture='notable' WHERE game='mcd'"
    ).rowcount

    # ---- 2. pull_pending_vocab (first-class) ----
    if not column_exists(conn, "canon_corpus", "pull_pending_vocab"):
        conn.execute(
            "ALTER TABLE canon_corpus ADD COLUMN pull_pending_vocab INTEGER NOT NULL DEFAULT 0"
        )
    # default 0 covers every existing row (incl. non-mcd); set 1 on the 6 pull kits only.
    conn.execute("UPDATE canon_corpus SET pull_pending_vocab=0 WHERE game='mcd'")
    qmarks = ",".join("?" * len(PULL_KITS))
    n_pull = conn.execute(
        f"UPDATE canon_corpus SET pull_pending_vocab=1 WHERE kit_id IN ({qmarks})",
        PULL_KITS,
    ).rowcount

    conn.commit()

    # ---- schema_meta marker (idempotent) ----
    conn.execute("DELETE FROM corpus_schema_meta WHERE version='mcd-curation-complete-2026-07-15'")
    conn.execute(
        "INSERT INTO corpus_schema_meta (version, applied_utc, note) VALUES (?,?,?)",
        (
            "mcd-curation-complete-2026-07-15",
            "2026-07-15T00:00:00Z",
            "MCD curation completion (elrond) — finishes the timed-out ingest run. Promotes "
            "two annotations from the flags JSON blob to FIRST-CLASS queryable columns on the "
            "120 mcd rows: architecture='notable' (INGEST-granting 3-grain label; "
            "WHERE architecture='notable' now returns the 120) and pull_pending_vocab INTEGER "
            "(1 on the 6 frozen-basis pull kits, 0 else; distinguishes pending-pull-vocab from "
            "thin-artifact among unresolved=1). Additive, mcd-scoped, survivors byte-identical. "
            "lattice_coord rekey DEFERRED (off critical path; displacement/ghost emitters read "
            "cell_key, which MCD already has). No re-ingest.",
        ),
    )
    conn.commit()

    # ---- verification ----
    sha_after = survivor_sha()
    assert sha_after == sha_before, (
        f"SURVIVOR CELL_KEYS CHANGED — abort. before={sha_before} after={sha_after}"
    )

    integ = conn.execute("PRAGMA integrity_check").fetchone()[0]

    # queryability proofs
    q_arch = conn.execute(
        "SELECT COUNT(*) FROM canon_corpus WHERE architecture='notable'"
    ).fetchone()[0]
    q_arch_mcd = conn.execute(
        "SELECT COUNT(*) FROM canon_corpus WHERE architecture='notable' AND game='mcd'"
    ).fetchone()[0]
    q_pull = conn.execute(
        "SELECT COUNT(*) FROM canon_corpus WHERE unresolved=1 AND pull_pending_vocab=1"
    ).fetchone()[0]
    q_thin = conn.execute(
        "SELECT COUNT(*) FROM canon_corpus WHERE unresolved=1 AND pull_pending_vocab=0 AND game='mcd'"
    ).fetchone()[0]
    q_pull_nonmcd = conn.execute(
        "SELECT COUNT(*) FROM canon_corpus WHERE pull_pending_vocab=1 AND game!='mcd'"
    ).fetchone()[0]

    conn.close()

    print("== MCD CURATION COMPLETION ==")
    print(f"  architecture column set on mcd rows: {n_arch}")
    print(f"  pull_pending_vocab=1 set on kits:    {n_pull}")
    print(f"  --- queryability proofs ---")
    print(f"  WHERE architecture='notable'                       -> {q_arch}  (all mcd={q_arch_mcd})")
    print(f"  WHERE unresolved=1 AND pull_pending_vocab=1         -> {q_pull}  (expect 6)")
    print(f"  WHERE unresolved=1 AND pull_pending_vocab=0 (mcd)   -> {q_thin}  (expect 20)")
    print(f"  pull_pending_vocab=1 leaked to non-mcd             -> {q_pull_nonmcd}  (expect 0)")
    print(f"  survivor cell_keys byte-identical:  YES  (sha {sha_after[:12]}…)")
    print(f"  integrity: {integ}")

    ok = (n_arch == 120 and n_pull == 6 and q_arch_mcd == 120 and q_pull == 6
          and q_thin == 20 and q_pull_nonmcd == 0 and integ == "ok")
    if not ok:
        sys.exit("VERIFICATION FAILED — inspect counts above")
    print("  ALL CHECKS PASS")


if __name__ == "__main__":
    main()
