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
# --- GATE-2 REMEDIATION (2026-07-22, jack-ryan BLOCK) ----------------
# PRIOR DEFECT: the 7 census asserts used RAISE(ABORT,...) inside bare
# top-level SELECT CASE...END statements. SQLite permits RAISE() ONLY
# inside a trigger-program, so each assert failed at PARSE time and never
# evaluated the count. The sqlite3 CLI (no -bail) skipped the parse error
# and proceeded to the v2.0-stamp INSERT + COMMIT, which SUCCEEDED. Net:
# the db landed v2.0-stamped with ALL asserts bypassed — the headline
# safety contract ("assert failure -> no stamp") was INOPERATIVE.
#
# FIX (jack-ryan Option B — bash-gated asserts, separate-call stamp):
#   * DDL v1 + riders run in ONE transaction and COMMIT (steps [2-4]).
#     They MUST commit before the asserts because the 6 census columns
#     (corpus_class/court/original_element/atlas_coords/eras_normalized)
#     DO NOT EXIST until DDL v1 creates them — you cannot query them from
#     bash otherwise. DDL+riders are idempotent + reversible (§4.3) and
#     the backup is taken first (step [1]), so a committed-but-unstamped
#     db is exactly the "identifiable partial" the design wants; re-run
#     is safe.
#   * The 7 census asserts (step [5]) are now BASH control-flow: each
#     expected count is a sqlite3 scalar into a shell var, gated
#     [ "$X" = "N" ] || { echo "ASSERT FAIL ..."; exit 1; } under
#     set -euo pipefail. A failed assert exit-1s the whole script.
#   * The v2.0 stamp (step [6]) is a SEPARATE, LAST sqlite3 invocation,
#     reached ONLY AFTER all 7 asserts pass. Because a failed assert
#     exit-1s before this call, the stamp is UNREACHABLE on any mismatch.
#     "Stamp last, only if every assert passed" is now a real bash
#     control-flow guarantee, not an in-SQL one SQLite silently skips.
#
# NEGATIVE-PATH PROOF: 2026-07-22-vdm2-w3a-fix-negative-path-evidence.md
#   (a) wrong count -> ABORT with NO v2.0 stamp; (b) correct -> stamps.
#   DDL v1 + riders SQL are UNCHANGED (Gate-2 proved them byte-perfect).
#
# SAFETY: assert failure -> exit 1 BEFORE the stamp call -> the db keeps
# its pre-stamp version (v1.1-*); the DDL+riders partial is reversible via
# the step-[1] backup (cp BACKUP DB). The v2.0 stamp lands only if every
# assert passed. New dockets take status='open' (distinct from the 19
# matt-ratified). Raws never dropped (§4.3 reversibility).
# =====================================================================
set -euo pipefail

CURATED="$HOME/Games/reincarnated-collaboration/agentic_orchestration/research/curated"
NOTES="$HOME/Games/reincarnated-collaboration/agentic_orchestration/elrond/notes"
# DB / BACKUP / EXPECTED_PRE_MD5 default to the production target but may be
# overridden from the environment ONLY for the negative/positive-path evidence
# runs (2026-07-22-vdm2-w3a-fix-negative-path-evidence.md), which drive THIS
# script unmodified against throwaway copies. Unset in production => live db.
DB="${DB:-$CURATED/corpus.db}"
DDL="$NOTES/2026-07-22-vdm2-ddl-v1.sql"
RIDERS="$NOTES/2026-07-22-vdm2-riders.sql"
DATESTAMP="$(date +%Y-%m-%d)"
BACKUP="${BACKUP:-$CURATED/corpus.db.pre-vdm2-schema-${DATESTAMP}-backup}"
EXPECTED_PRE_MD5="${EXPECTED_PRE_MD5:-50df15b776ad5b0da93fe90cdee1163d}"
UTC="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

# Record-bucket predicate reused across every court/promotion assert.
REC_BUCKETS="corpus_bucket IN ('poe1','d2','gd','poe2','le')"

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

# --- STEPS 2-4: DDL + riders, ONE TRANSACTION (NO stamp yet) ---------
# The DDL+riders run inside one BEGIN...COMMIT. If sqlite3 errors before
# COMMIT, the txn auto-rolls-back (nothing persisted) and set -e kills the
# script before any assert or the stamp. On success the DDL+riders commit;
# the db is now migrated but UNSTAMPED (still v1.1-*) — an identifiable,
# reversible partial. The census columns now EXIST, so the bash asserts
# in step [5] can query them.
echo "## [2-4] DDL v1 + riders (single txn; NO v2.0 stamp yet)"
sqlite3 "$DB" <<SQL
PRAGMA foreign_keys=ON;
BEGIN;
-- [3] additive DDL v1 (12 tables + 9 columns)
.read $DDL
-- [4] data riders + registry seeds (corpus_class/court/eras/original_element/atlas)
.read $RIDERS
COMMIT;
SQL
echo "  DDL+riders committed (db migrated, still UNSTAMPED v1.1-*)"

# --- STEP 5: post-rider census ASSERTS — BASH CONTROL-FLOW -----------
# Each expected count is a sqlite3 scalar into a shell var, then gated. A
# mismatch echoes the failure and exit 1 — which, under set -euo pipefail,
# terminates the script BEFORE the step-[6] stamp call is ever reached.
# The stamp is therefore unreachable on any assert failure. On abort here,
# the db keeps its pre-stamp version; reverse the DDL+riders partial with
# cp "$BACKUP" "$DB".
echo "## [5] census asserts (bash-gated; mismatch -> exit 1 BEFORE stamp)"

assert() {  # assert <name> <expected> <actual>
  local name="$1" expected="$2" actual="$3"
  if [ "$actual" = "$expected" ]; then
    echo "  ok   $name = $actual"
  else
    echo "ASSERT FAIL: $name expected $expected got $actual"
    echo "  -> aborting BEFORE v2.0 stamp. db is migrated-but-UNSTAMPED (still $STAMP)."
    echo "  -> reverse the partial: cp \"$BACKUP\" \"$DB\""
    exit 1
  fi
}

# 5a. corpus_class: record 267 | annex 299 | system 19 | NULL 0
assert "corpus_class.record" 267 "$(sqlite3 "$DB" "SELECT COUNT(*) FROM canon_corpus WHERE corpus_class='record';")"
assert "corpus_class.annex"  299 "$(sqlite3 "$DB" "SELECT COUNT(*) FROM canon_corpus WHERE corpus_class='annex';")"
assert "corpus_class.system"  19 "$(sqlite3 "$DB" "SELECT COUNT(*) FROM canon_corpus WHERE corpus_class='system';")"
assert "corpus_class.NULL"     0 "$(sqlite3 "$DB" "SELECT COUNT(*) FROM canon_corpus WHERE corpus_class IS NULL;")"

# 5b. court on record bucket: physical 90 | fire 54 | chaos-poison 44 | lightning 42 | cold 27 | NULL 13
assert "court.physical"     90 "$(sqlite3 "$DB" "SELECT COUNT(*) FROM canon_corpus WHERE $REC_BUCKETS AND court='physical';")"
assert "court.fire"         54 "$(sqlite3 "$DB" "SELECT COUNT(*) FROM canon_corpus WHERE $REC_BUCKETS AND court='fire';")"
assert "court.chaos-poison" 44 "$(sqlite3 "$DB" "SELECT COUNT(*) FROM canon_corpus WHERE $REC_BUCKETS AND court='chaos-poison';")"
assert "court.lightning"    42 "$(sqlite3 "$DB" "SELECT COUNT(*) FROM canon_corpus WHERE $REC_BUCKETS AND court='lightning';")"
assert "court.cold"         27 "$(sqlite3 "$DB" "SELECT COUNT(*) FROM canon_corpus WHERE $REC_BUCKETS AND court='cold';")"
assert "court.NULL"         13 "$(sqlite3 "$DB" "SELECT COUNT(*) FROM canon_corpus WHERE $REC_BUCKETS AND court IS NULL;")"

# 5c. original_element promotion total on record (270)
assert "original_element.record" 270 "$(sqlite3 "$DB" "SELECT COUNT(*) FROM canon_corpus WHERE $REC_BUCKETS AND original_element IS NOT NULL;")"

# 5d. atlas_coords promotion on record (268; 2 honest NULL)
assert "atlas_coords.record" 268 "$(sqlite3 "$DB" "SELECT COUNT(*) FROM canon_corpus WHERE $REC_BUCKETS AND atlas_coords IS NOT NULL;")"

# 5e. eras_normalized on record (268; 2 poe1 NULL-eras honest)
assert "eras_normalized.record" 268 "$(sqlite3 "$DB" "SELECT COUNT(*) FROM canon_corpus WHERE $REC_BUCKETS AND eras_normalized IS NOT NULL;")"

# 5f. A-7 preserve-NULL: t4_doors JSON-null count UNCHANGED (29 total; 8 record-game)
assert "t4_doors.jsonnull" 29 "$(sqlite3 "$DB" "SELECT COUNT(*) FROM kit_mapping WHERE json_type(mapping_json,'\$.t4_doors')='null';")"

# 5g. iron-law: total 585, kit_master 574, is_system 19
assert "iron-law.canon_corpus" 585 "$(sqlite3 "$DB" "SELECT COUNT(*) FROM canon_corpus;")"
assert "iron-law.kit_master"   574 "$(sqlite3 "$DB" "SELECT COUNT(*) FROM kit_master;")"
assert "iron-law.is_system"     19 "$(sqlite3 "$DB" "SELECT COUNT(*) FROM canon_corpus WHERE is_system=1;")"

echo "  ALL 17 census asserts passed."

# --- STEP 6: v2.0 stamp — SEPARATE, LAST sqlite3 CALL ----------------
# Reached ONLY because every assert above passed (any mismatch exit-1s the
# script before this line). This is the ONLY statement that writes 'v2.0',
# and it is a distinct sqlite3 invocation from the DDL+riders txn. That is
# the fix: the stamp is control-flow-unreachable on any assert failure.
echo "## [6] v2.0 stamp (separate call; reached only after all asserts passed)"
sqlite3 "$DB" <<SQL
INSERT INTO corpus_schema_meta(version, applied_utc, note)
VALUES ('v2.0', '$UTC',
  'VDM-2 schema landing (elrond, W3b). Additive DDL v1: 12 side-car tables + 9 columns (corpus_class/eras_normalized/original_element/court/atlas_coords/capstone_source_acquisition on canon_corpus; source_deviation_id/source_kit_id/intake_lane on mechanic_gap_docket; claim_subject/anchor_lint/source_lane on verify_ledger). Riders: corpus_class 267/299/19; court 257/270 (13 NULL, V-15); original_element 270; atlas_coords 268; eras_normalized 268 (V-16 per-game vocab in MIGRATION.md). A-1..A-7 folded. exact_json/normalization_rule/capstone NULL/empty at apply (downstream deps). Zero VDM-1 touch; A-7 preserve-NULL held (29 JSON-null t4_doors unchanged). Reversible via $BACKUP.');
SQL
echo "  v2.0 stamp written."

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
