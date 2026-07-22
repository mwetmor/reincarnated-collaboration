#!/usr/bin/env bash
# =====================================================================
# VDM-2 W5b APPLY SCRIPT — the EXECUTE wave (exactly ONE ruled correction)
# =====================================================================
# Author:  elrond (data steward) · Wave W5b · gandalf RUN-CONDUCTOR lap
# Charter: 2026-07-22-vdm2-edition-next-lap-charter.md
# Ruling:  V-23(a) UPHELD (binding). Ledger rows V-18/V-22/V-23 + RB-6/RB-8.
#          Predecessor: MIGRATION.md § vdm2-w5a-verify-2026-07-22.
#
# THE MUTATION — exactly this, nothing more (V-23 net scope = 1 elem_raw + 1 court row):
#   Kit: d2-wl-blood-boil (record-class).
#   (1) canon_corpus.elem_raw : 'shadow/blood?' -> 'fire'
#         Anchor (V-23(a)/RB-8, FROZEN kit_mapping — read-only): Blood Boil +
#         Summon Tainted BOTH element_primary=fire. The '?'-marked elem_raw is
#         an UNCERTAIN folk-tag contradicting its own skill data. Correcting the
#         DERIVED field TOWARD its SOURCE = the designed W5 case (derived-toward-
#         source only; source-data edits escalate — RB-8).
#   (2) canon_corpus.court     : NULL/'' -> 'fire'
#         Bounded single-row court re-derivation (V-18 + V-15/V-20: fire -> fire
#         court). ONLY this one row's court. NOT a corpus-wide re-derivation.
#
# HARD CONSTRAINTS (do NOT):
#   * NOT poe1-spectral-throw (V-23(b): DOWNGRADED to AMBIGUOUS-HOLD — its
#     mapping_json anchor says lightning, AGREEING with elem_raw; a frozen-
#     catalogue finding for a later pass, not a W5b edit).
#   * NOT any other canon_corpus row (9 AMBIGUOUS-HOLD incl. spectral-throw,
#     7 DOCUMENTED-CROSSWALK, 3 next-lap membership, 7 CONTRADICTED geometry —
#     ALL no-mutation dispositions, documentation only).
#   * NOT kit_mapping / mapping_json (FROZEN catalogue, iron-law 574).
#   * NOT a corpus-wide court re-derivation — ONLY d2-wl-blood-boil.
#   * NOT the six side-car blocks / kit_door_arg / verify_ledger / any docket.
#
# DISCIPLINE (reuse the W3a-fix bash-gate pattern):
#   * Pre-flight md5 drift-guard: live corpus.db MUST be the expected md5 before
#     any write. Drift => STOP (someone else touched the DB).
#   * Backup first (unconditional, clobber-guarded) BEFORE any write.
#   * Apply the 2 UPDATEs in a SINGLE transaction; then ASSERT under
#     set -euo pipefail. If ANY assert fails: RESTORE from backup (reversible)
#     and exit 1 — the change is kept ONLY if every assert passes.
#   * The confirm/stamp echo is a SEPARATE terminal call, control-flow-
#     unreachable on any mismatch (a failed assert exit-1s first).
#
# NEGATIVE PATH: any assert mismatch -> restore backup -> live db byte-identical
#   to pre-W5b -> exit 1 before the confirm line. Reversible + idempotent
#   (backup clobber-guard blocks a silent second run over a mutated db).
# =====================================================================
set -euo pipefail

CURATED="$HOME/Games/reincarnated-collaboration/agentic_orchestration/research/curated"
# DB / BACKUP / EXPECTED_PRE_MD5 default to the production target. Overridable
# from the environment ONLY for throwaway-copy evidence runs; unset => live db.
DB="${DB:-$CURATED/corpus.db}"
DATESTAMP="$(date +%Y-%m-%d)"
BACKUP="${BACKUP:-$CURATED/corpus.db.pre-vdm2-w5b-${DATESTAMP}-backup}"
EXPECTED_PRE_MD5="${EXPECTED_PRE_MD5:-032c9b65d3354c3c35b05082fc3c1695}"
TARGET="d2-wl-blood-boil"
UTC="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

md5_of() { md5 -q "$1" 2>/dev/null || md5sum "$1" | cut -d' ' -f1; }

# restore_and_die <reason> : byte-for-byte restore the live db from the backup,
# verify the restore matched the pre-mutation md5, then exit 1. Used by BOTH the
# mutation-step trap AND the assert helper so EVERY failure mode (a mid-txn
# error that the sqlite3 CLI would otherwise let slip past a bare `set -e`, or a
# post-verify assert mismatch) lands the live db in its exact pre-W5b state. The
# backup is taken first (step [1]) and is the reversibility guarantee (§4.3).
restore_and_die() {
  local reason="$1"
  echo "FAILURE: $reason"
  echo "  -> RESTORING db from backup (reversible): cp \"$BACKUP\" \"$DB\""
  cp "$BACKUP" "$DB"
  local restore_md5; restore_md5=$(md5_of "$DB")
  echo "  -> restored. live md5 now $restore_md5 (must equal pre-mutation $EXPECTED_PRE_MD5)."
  [ "$restore_md5" = "$EXPECTED_PRE_MD5" ] || echo "  !! WARN: restored md5 mismatch — INVESTIGATE."
  exit 1
}

# The one-row-only differential fingerprint: every canon_corpus row EXCEPT the
# target, on the four fields any element/court edit could touch. Must be byte-
# identical between the pre-W5b backup and the post-W5b live db => exactly one
# row changed, nothing else.
diff_hash() {  # diff_hash <db>
  sqlite3 "$1" \
    "SELECT kit_id,elem_raw,court,corpus_class FROM canon_corpus WHERE kit_id != '$TARGET' ORDER BY kit_id;" \
    | md5_of /dev/stdin
}

echo "### VDM-2 W5b APPLY — $UTC — target=$TARGET"

# --- STEP 0: preflight drift-guard -----------------------------------
echo "## [0] preflight md5 drift-guard"
PRE_MD5=$(md5_of "$DB")
[ "$PRE_MD5" = "$EXPECTED_PRE_MD5" ] || {
  echo "FATAL: pre-mutation md5 '$PRE_MD5' != expected '$EXPECTED_PRE_MD5'."
  echo "  -> corpus.db changed since W5a close. DRIFT (someone else touched the DB). ABORT — NO write."; exit 1; }
echo "  md5 OK ($PRE_MD5)"

# preflight target-state guard: the row MUST be in its expected pre-state
BEFORE=$(sqlite3 "$DB" "SELECT quote(elem_raw)||'|'||quote(court) FROM canon_corpus WHERE kit_id='$TARGET';")
echo "  target BEFORE (elem_raw|court): $BEFORE"
[ "$BEFORE" = "'shadow/blood?'|''" ] || [ "$BEFORE" = "'shadow/blood?'|NULL" ] || {
  echo "FATAL: $TARGET pre-state is $BEFORE, expected elem_raw='shadow/blood?' court=''/NULL. ABORT — NO write."; exit 1; }

# --- STEP 1: BACKUP FIRST (unconditional, clobber-guarded) -----------
echo "## [1] backup first (before any write)"
[ -f "$BACKUP" ] && { echo "FATAL: backup $BACKUP already exists (prior run?). ABORT to avoid clobber."; exit 1; }
cp "$DB" "$BACKUP"
BACKUP_MD5=$(md5_of "$BACKUP")
[ "$BACKUP_MD5" = "$EXPECTED_PRE_MD5" ] || { echo "FATAL: backup md5 '$BACKUP_MD5' mismatch. ABORT."; exit 1; }
echo "  backup -> $BACKUP (md5 $BACKUP_MD5)"

# capture the pre-mutation differential fingerprint from the BACKUP (the
# frozen 584-row reference) — this is the load-bearing one-row-only proof.
BACKUP_DIFF_HASH=$(diff_hash "$BACKUP")
echo "  backup 584-row differential hash: $BACKUP_DIFF_HASH"

# --- STEP 2: THE MUTATION — 2 UPDATEs, ONE transaction ---------------
# Single BEGIN...COMMIT with `.bail on` so ANY statement error aborts the CLI
# BEFORE reaching COMMIT => the whole txn rolls back, no partial persists.
# (CRITICAL: without `.bail on` the sqlite3 CLI reports a mid-txn error but
# CONTINUES to the next line — it would run COMMIT and persist the already-
# succeeded UPDATEs as a partial. Proven on a throwaway copy: the default CLI
# committed blood-boil's two UPDATEs even though a 3rd collateral statement
# violated a CHECK. `.bail on` makes the txn truly atomic — same class of
# looks-transactional-but-isn't defect RB-1 exists to catch.)
# The mutation runs inside a subshell guarded by `if ! ...`, NOT a bare
# `set -e` death, so a non-zero sqlite3 exit routes to restore_and_die (which
# restores the pre-mutation db from backup) — the restore covers the mutation
# step too, not only the asserts. Guarded UPDATEs (WHERE fences the elem_raw
# pre-value / the NULL-or-empty court) so a re-run can't silently re-mutate a
# shifted row.
echo "## [2] mutation (2 UPDATEs, single atomic txn; .bail on)"
if ! sqlite3 "$DB" <<SQL
.bail on
PRAGMA foreign_keys=ON;
BEGIN;
UPDATE canon_corpus
   SET elem_raw = 'fire'
 WHERE kit_id = '$TARGET' AND elem_raw = 'shadow/blood?';
UPDATE canon_corpus
   SET court = 'fire'
 WHERE kit_id = '$TARGET' AND (court IS NULL OR court = '');
COMMIT;
SQL
then
  restore_and_die "mutation txn returned non-zero (aborted before COMMIT; .bail on => rolled back). db restored to pre-W5b."
fi
echo "  UPDATEs committed (db mutated; asserts next decide keep/restore)"

# --- STEP 3: POST-VERIFY ASSERTS — BASH CONTROL-FLOW -----------------
# Each expected value is a sqlite3 scalar into a shell var, then gated. On any
# mismatch: RESTORE the db byte-for-byte from the backup, then exit 1. The
# confirm line (step [4]) is unreachable on any mismatch. The change is kept
# ONLY if EVERY assert passes.
echo "## [3] post-verify asserts (bash-gated; mismatch -> RESTORE backup, exit 1)"

assert() {  # assert <name> <expected> <actual>
  local name="$1" expected="$2" actual="$3"
  if [ "$actual" = "$expected" ]; then
    echo "  ok   $name = $actual"
  else
    restore_and_die "ASSERT FAIL: $name expected [$expected] got [$actual]"
  fi
}

# 3a. TARGET post-state: exactly elem_raw=fire, court=fire
assert "target.elem_raw" "fire" "$(sqlite3 "$DB" "SELECT elem_raw FROM canon_corpus WHERE kit_id='$TARGET';")"
assert "target.court"    "fire" "$(sqlite3 "$DB" "SELECT court    FROM canon_corpus WHERE kit_id='$TARGET';")"

# 3b. iron-law unchanged: 585 / 574 / 19
assert "iron-law.canon_corpus" 585 "$(sqlite3 "$DB" "SELECT COUNT(*) FROM canon_corpus;")"
assert "iron-law.kit_master"   574 "$(sqlite3 "$DB" "SELECT COUNT(*) FROM kit_master;")"
assert "iron-law.is_system"     19 "$(sqlite3 "$DB" "SELECT COUNT(*) FROM canon_corpus WHERE is_system=1;")"

# 3c. six-block unchanged: 490 / 259 / 441 / 310 / 267 / 2
assert "six-block.skill_geometry_band"   490 "$(sqlite3 "$DB" "SELECT COUNT(*) FROM skill_geometry_band;")"
assert "six-block.kit_deviation"         259 "$(sqlite3 "$DB" "SELECT COUNT(*) FROM kit_deviation;")"
assert "six-block.recognition_hook"      441 "$(sqlite3 "$DB" "SELECT COUNT(*) FROM recognition_hook;")"
assert "six-block.kit_acceptance_assert" 310 "$(sqlite3 "$DB" "SELECT COUNT(*) FROM kit_acceptance_assert;")"
assert "six-block.kit_delta_t4"          267 "$(sqlite3 "$DB" "SELECT COUNT(*) FROM kit_delta_t4;")"
assert "six-block.kit_numeric"             2 "$(sqlite3 "$DB" "SELECT COUNT(*) FROM kit_numeric;")"

# 3d. carved-out surfaces unchanged: kit_door_arg 0, verify_ledger 2577
assert "kit_door_arg"  0    "$(sqlite3 "$DB" "SELECT COUNT(*) FROM kit_door_arg;")"
assert "verify_ledger" 2577 "$(sqlite3 "$DB" "SELECT COUNT(*) FROM verify_ledger;")"

# 3e. integrity + FK
assert "integrity_check" "ok" "$(sqlite3 "$DB" "PRAGMA integrity_check;")"
FK_ROWS=$(sqlite3 "$DB" "PRAGMA foreign_key_check;" | wc -l | tr -d ' ')
assert "foreign_key_check.rows" 0 "$FK_ROWS"

# 3f. THE ONE-ROW-ONLY PROOF: the 584-row differential hash of the LIVE db
#     (post-mutation) MUST equal the BACKUP's (pre-mutation). Equal => the
#     mutation touched EXACTLY the target row and nothing else.
LIVE_DIFF_HASH=$(diff_hash "$DB")
echo "  backup 584-row differential hash: $BACKUP_DIFF_HASH"
echo "  live   584-row differential hash: $LIVE_DIFF_HASH"
assert "one-row-only.diff_hash" "$BACKUP_DIFF_HASH" "$LIVE_DIFF_HASH"

echo "  ALL asserts passed."

# --- STEP 4: CONFIRM — SEPARATE, LAST call (unreachable on mismatch) --
# Reached ONLY because every assert above passed (any mismatch RESTORES +
# exit-1s before this line). This is the terminal confirmation; it emits the
# post-mutation md5 (which WILL differ from pre — expected, the 1-row change).
echo "## [4] confirm (separate terminal call; reached only after ALL asserts passed)"
POST_MD5=$(md5_of "$DB")
echo "  pre-mutation  md5: $EXPECTED_PRE_MD5"
echo "  post-mutation md5: $POST_MD5   (WILL differ — expected: the 1-row mutation)"
echo "  target $TARGET: elem_raw shadow/blood? -> fire ; court NULL/'' -> fire"
echo "  one-row-only differential hash (backup == live): $BACKUP_DIFF_HASH"
echo "### W5b APPLY COMPLETE. corpus.db mutated (exactly 1 row). Backup at $BACKUP."
echo "### Reversibility: cp \"$BACKUP\" \"$DB\" restores exact pre-W5b state."
