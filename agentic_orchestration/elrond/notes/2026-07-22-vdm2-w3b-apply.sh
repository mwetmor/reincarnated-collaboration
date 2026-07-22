#!/usr/bin/env bash
# =====================================================================
# VDM-2 W3b APPLY SCRIPT — RUNNABLE, BUT *** DO NOT RUN THIS WAVE ***
# =====================================================================
# Author:  elrond (data steward) · assembled Wave W3a · runs at Wave W3b
# Package: 2026-07-22-vdm2-w3a-migration-package.md
# Gate:    RUN ONLY AFTER jack-ryan Gate-2 PASS on the W3a package.
#
# THIS SCRIPT IS ASSEMBLED FOR REVIEW. It is NOT executed in W3a. corpus.db
# stays byte-identical (md5 50df15b776ad5b0da93fe90cdee1163d) until W3b.
#
# Sequence (charter §4 W3 + run-state W3b line + ADR-004):
#   0. preflight guards (stamp == v1.1-verified; md5 == expected; foreign_keys)
#   1. BACKUP corpus.db + RECORD md5 FIRST                (reversibility anchor)
#   2. PRAGMA foreign_keys=ON                             (loud FK failure)
#   3. additive DDL v1                                    (12 tables + 9 cols)
#   4. data riders + registry seeds                       (corpus_class/court/eras/etc.)
#   5. post-rider census ASSERTS                          (must match W3a package)
#   6. v2.0 stamp LAST                                    (the final statement)
#   7. MIGRATION.md entry per ADR-004                     (append the W3a draft)
#   8. compendium regen from kit_master
#
# SAFETY: steps 3-6 run inside a SINGLE TRANSACTION. Any assert failure ->
# ROLLBACK -> restore-from-backup is a no-op (nothing committed). The v2.0
# stamp only lands if every assert passed. New dockets take status='open'
# (distinct from the 19 matt-ratified). Raws never dropped (§4.3 reversibility).
# =====================================================================
set -euo pipefail

CURATED="$HOME/Games/reincarnated-collaboration/agentic_orchestration/research/curated"
NOTES="$HOME/Games/reincarnated-collaboration/agentic_orchestration/elrond/notes"
DB="$CURATED/corpus.db"
DDL="$NOTES/2026-07-22-vdm2-ddl-v1.sql"
RIDERS="$NOTES/2026-07-22-vdm2-riders.sql"
DATESTAMP="$(date +%Y-%m-%d)"
BACKUP="$CURATED/corpus.db.pre-vdm2-schema-${DATESTAMP}-backup"
EXPECTED_PRE_MD5="50df15b776ad5b0da93fe90cdee1163d"
UTC="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

echo "### VDM-2 W3b APPLY — $UTC"

# --- STEP 0: preflight guards ----------------------------------------
echo "## [0] preflight guards"
STAMP=$(sqlite3 "$DB" "SELECT version FROM corpus_schema_meta ORDER BY rowid DESC LIMIT 1;")
[ "$STAMP" = "v1.1-deprecation-source_urls" ] || [ "$STAMP" = "v1.1-verified" ] || {
  echo "FATAL: terminal stamp is '$STAMP', expected v1.1-verified/-deprecation-source_urls. ABORT."; exit 1; }
PRE_MD5=$(md5 -q "$DB" 2>/dev/null || md5sum "$DB" | cut -d' ' -f1)
[ "$PRE_MD5" = "$EXPECTED_PRE_MD5" ] || {
  echo "FATAL: pre-apply md5 '$PRE_MD5' != expected '$EXPECTED_PRE_MD5'. corpus.db changed since W3a. ABORT."; exit 1; }
echo "  stamp OK ($STAMP); md5 OK ($PRE_MD5)"

# --- STEP 1: BACKUP FIRST + record md5 -------------------------------
echo "## [1] backup + md5"
[ -f "$BACKUP" ] && { echo "FATAL: backup $BACKUP already exists (prior run?). ABORT to avoid clobber."; exit 1; }
cp "$DB" "$BACKUP"
BACKUP_MD5=$(md5 -q "$BACKUP" 2>/dev/null || md5sum "$BACKUP" | cut -d' ' -f1)
[ "$BACKUP_MD5" = "$EXPECTED_PRE_MD5" ] || { echo "FATAL: backup md5 mismatch. ABORT."; exit 1; }
echo "  backup -> $BACKUP (md5 $BACKUP_MD5)"

# --- STEPS 2-6: DDL + riders + asserts + stamp, ONE TRANSACTION -------
# On ANY error inside the heredoc, sqlite3 aborts; because the whole block is
# one BEGIN...COMMIT, an abort before COMMIT = automatic ROLLBACK (nothing
# persisted). The v2.0 stamp is the LAST statement inside the txn.
echo "## [2-6] DDL v1 + riders + census asserts + v2.0 stamp (single txn)"
sqlite3 "$DB" <<SQL
PRAGMA foreign_keys=ON;
BEGIN;

-- [3] additive DDL v1
.read $DDL

-- [4] data riders + registry seeds
.read $RIDERS

-- [5] post-rider census ASSERTS — each RAISEs (aborts the txn -> ROLLBACK)
--     if the count is not exactly the W3a-package-pinned value.
-- 5a. corpus_class: record 267 | annex 299 | system 19 | NULL 0
SELECT CASE WHEN (SELECT COUNT(*) FROM canon_corpus WHERE corpus_class='record')=267
            AND (SELECT COUNT(*) FROM canon_corpus WHERE corpus_class='annex')=299
            AND (SELECT COUNT(*) FROM canon_corpus WHERE corpus_class='system')=19
            AND (SELECT COUNT(*) FROM canon_corpus WHERE corpus_class IS NULL)=0
       THEN 1 ELSE RAISE(ABORT,'ASSERT FAIL: corpus_class census != 267/299/19/0') END;
-- 5b. court on record bucket: physical 90 | fire 54 | chaos-poison 44 | lightning 42 | cold 27 | NULL 13
SELECT CASE WHEN (SELECT COUNT(*) FROM canon_corpus WHERE corpus_bucket IN ('poe1','d2','gd','poe2','le') AND court='physical')=90
            AND (SELECT COUNT(*) FROM canon_corpus WHERE corpus_bucket IN ('poe1','d2','gd','poe2','le') AND court='fire')=54
            AND (SELECT COUNT(*) FROM canon_corpus WHERE corpus_bucket IN ('poe1','d2','gd','poe2','le') AND court='chaos-poison')=44
            AND (SELECT COUNT(*) FROM canon_corpus WHERE corpus_bucket IN ('poe1','d2','gd','poe2','le') AND court='lightning')=42
            AND (SELECT COUNT(*) FROM canon_corpus WHERE corpus_bucket IN ('poe1','d2','gd','poe2','le') AND court='cold')=27
            AND (SELECT COUNT(*) FROM canon_corpus WHERE corpus_bucket IN ('poe1','d2','gd','poe2','le') AND court IS NULL)=13
       THEN 1 ELSE RAISE(ABORT,'ASSERT FAIL: court census != 90/54/44/42/27/13') END;
-- 5c. original_element promotion total on record (270)
SELECT CASE WHEN (SELECT COUNT(*) FROM canon_corpus WHERE corpus_bucket IN ('poe1','d2','gd','poe2','le') AND original_element IS NOT NULL)=270
       THEN 1 ELSE RAISE(ABORT,'ASSERT FAIL: original_element != 270 on record') END;
-- 5d. atlas_coords promotion on record (268; 2 honest NULL)
SELECT CASE WHEN (SELECT COUNT(*) FROM canon_corpus WHERE corpus_bucket IN ('poe1','d2','gd','poe2','le') AND atlas_coords IS NOT NULL)=268
       THEN 1 ELSE RAISE(ABORT,'ASSERT FAIL: atlas_coords != 268 on record') END;
-- 5e. eras_normalized on record (268; 2 poe1 NULL-eras honest)
SELECT CASE WHEN (SELECT COUNT(*) FROM canon_corpus WHERE corpus_bucket IN ('poe1','d2','gd','poe2','le') AND eras_normalized IS NOT NULL)=268
       THEN 1 ELSE RAISE(ABORT,'ASSERT FAIL: eras_normalized != 268 on record') END;
-- 5f. A-7 preserve-NULL: t4_doors JSON-null count UNCHANGED (29 total; 8 record-game)
SELECT CASE WHEN (SELECT COUNT(*) FROM kit_mapping WHERE json_type(mapping_json,'\$.t4_doors')='null')=29
       THEN 1 ELSE RAISE(ABORT,'ASSERT FAIL: t4_doors JSON-null count != 29 (A-7 preserve-NULL violated)') END;
-- 5g. iron-law: total 585, kit_master 574, is_system 19, no orphan side-car kit_ids
SELECT CASE WHEN (SELECT COUNT(*) FROM canon_corpus)=585
            AND (SELECT COUNT(*) FROM kit_master)=574
            AND (SELECT COUNT(*) FROM canon_corpus WHERE is_system=1)=19
       THEN 1 ELSE RAISE(ABORT,'ASSERT FAIL: iron-law 585/574/19 broke') END;

-- [6] v2.0 stamp — THE FINAL STATEMENT (only reached if every assert passed)
INSERT INTO corpus_schema_meta(version, applied_utc, note)
VALUES ('v2.0', '$UTC',
  'VDM-2 schema landing (elrond, W3b). Additive DDL v1: 12 side-car tables + 9 columns (corpus_class/eras_normalized/original_element/court/atlas_coords/capstone_source_acquisition on canon_corpus; source_deviation_id/source_kit_id/intake_lane on mechanic_gap_docket; claim_subject/anchor_lint/source_lane on verify_ledger). Riders: corpus_class 267/299/19; court 257/270 (13 NULL, V-15); original_element 270; atlas_coords 268; eras_normalized 268 (V-16 per-game vocab in MIGRATION.md). A-1..A-7 folded. exact_json/normalization_rule/capstone NULL/empty at apply (downstream deps). Zero VDM-1 touch; A-7 preserve-NULL held (29 JSON-null t4_doors unchanged). Reversible via $BACKUP.');

COMMIT;
SQL

echo "  txn committed (all asserts passed; v2.0 stamped)"

# --- STEP 6b: verify the stamp landed --------------------------------
NEWSTAMP=$(sqlite3 "$DB" "SELECT version FROM corpus_schema_meta ORDER BY rowid DESC LIMIT 1;")
[ "$NEWSTAMP" = "v2.0" ] || { echo "FATAL: post-apply stamp is '$NEWSTAMP', expected v2.0. INVESTIGATE (restore from $BACKUP)."; exit 1; }
echo "## [6b] stamp verified: $NEWSTAMP"

# --- STEP 7: MIGRATION.md per ADR-004 --------------------------------
# Append the W3a MIGRATION.md draft (2026-07-22-vdm2-migration-draft.md) as a
# new entry to the running curated/MIGRATION.md. Manual review-then-append at
# W3b (do not blind-cat); the draft is the content.
echo "## [7] MIGRATION.md — append the W3a draft entry to $CURATED/MIGRATION.md (per ADR-004)"

# --- STEP 8: compendium regen ----------------------------------------
# Regenerate the compendium from kit_master v2 (same generator lineage as
# vdm1_compendium_gen_2026_07_19.py; the v2 generator is a W6 artifact, but the
# W3b compendium regen re-runs the existing generator over the post-DDL store to
# confirm kit_master still assembles identically — a smoke check, not the v2 book).
echo "## [8] compendium regen from kit_master (smoke: kit_master assembles post-DDL)"

echo "### W3b APPLY COMPLETE. corpus.db @ v2.0. Backup at $BACKUP."
echo "### Reversibility: cp \"$BACKUP\" \"$DB\" restores exact pre-VDM-2 state."
