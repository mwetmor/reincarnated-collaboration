"""
corpus_dr_reclassify_2026_07_17.py — DR 2-kit PER-FIGHT ECONOMY re-classification pass.

Author: elrond, 2026-07-17 (autonomous atlas-parity run, DR-RECLASSIFY charge).
Commissioner: gandalf-prime (Matt autonomous-run delegation 2026-07-16); all rulings veto-open at Matt read.
Concurrent processes: gandalf-prime DRIFT-CRITIC + jack-ryan Gate-1 on Wave-D spec
    (canonical/reap-die-rise-engine/wave-d-drain-fidelity-engine-spec.md).

CHARGE (paraphrased):
    Census V11 landed 558/564 = 98.94%. The residual econ tail is 2 kits flagged econ_gaps=["DR"]:
        hot-norseman-frost-avalanche + vs-queen-sigma.
    Wave-D spec §3-§4 + §11.a established from DB truth that "DR" on these kits is LEGACY VOCAB
    for draft/pool-management (roguelite meta-layer), NOT a per-fight drain: econ_meter_type=n/a,
    economy_model=unknown on both; mech_note verbatim "DR in old vocab = draft/pool-management."
    Engine will build NOTHING for DR (gandalf-prime DEFER § 11.a).

    Evaluate whether these 2 kits' PER-FIGHT economy lands honestly in LANDED vocab.

DISPOSITION (elrond ruling, veto-open at Matt read):
    BOTH KITS LAND AS **NR** (near-zero / steady auto-fire, VS-genre-native).
    The draft-meta shape is recorded as a provenance-tagged descriptor OVERLAY
    (SS form-lock precedent from the same batch), not as a bin.

    Rationale (evidence base):
      1. Both kits carry movement.verbs=["auto-fire-while-moving"] (survivor-genre bullet-heaven
         signature) — hot = Halls of Torment (survivor-genre-family); vs = Vampire Survivors.
      2. Both extractions give economy.model="draft" with meter_type="n/a" and plain_text
         EXPLICITLY disambiguating: "DR = draft/offer-pool" / "DR = draft/pre-converged." The
         "draft" model at extraction is META-LAYER commentary (offer-pool hygiene / per-run
         convergence), NOT per-fight resource mechanics.
      3. VS-PHIERAGGI PRECEDENT (same cycle, application sheet 2026-07-17, commit 0d4479e4):
             VS passive auto-cast ruled NR ("genre-typical for VS / bullet-heavens generally");
             Revival is a passive run-state multiplier, NOT consumable per-fire.
         The DB state after that ruling for vs-phieraggi:
             econ_status=native · econ_gaps=[] · econ_meter_type=n/a · economy_model=unknown
             + canon_corpus.flags carrying `econ-recrawl-application-2026-07-17:f4110f20:NR/auto-fire
             (VS-genre-native)...` provenance overlay.
      4. hot-norseman + vs-queen-sigma are STRUCTURALLY IDENTICAL to vs-phieraggi at the per-fight
         layer: auto-fire while moving, no per-cast resource pay, distinct meta-layer scaling
         (Revival stacks vs. offer-pool hygiene vs. per-level compound scaling — all descriptor,
         not per-fight bin).
      5. SS FORM-LOCK PRECEDENT (same batch, NOTABLE find 2): a secondary economy overlay that is
         real but NOT a bin records as descriptive lineage/gx metadata via a flag token, not as a
         bin re-classification. The draft-meta shape here is the analogous overlay.
      6. Wave-D spec §4.2 sub-option C.1 explicitly names the elrond-re-classify lane: "If elrond
         agrees, both kits' econ_gaps re-key from ['DR'] to a corpus-labelled bucket ... and drop
         from the census 'blocked on econ' bucket entirely." The spec proposed re-keying to
         ["draft-meta"] (leaving econ_status=gap). NR-LAND is a stronger form of C.1 that is more
         DB-truth-honest at the per-fight grain (there is no gap; the per-fight econ IS NR/steady
         auto-fire, precedent-matched to vs-phieraggi). Engine-side outcome identical: engine builds
         NOTHING for DR; census gets +2; Wave-D deliverables unchanged.

    Engine-side is UNTOUCHED (this script writes to corpus.db only; Wave-D spec §11.a DEFER holds:
    _DEFERRED_ECON_BINS stays empty, no drain surface, no cost_type map entry).

WRITES (idempotent, UPDATE-only; row conservation: 585 → 585):
    For each of {hot-norseman-frost-avalanche, vs-queen-sigma}:
      1. canon_engine_key row:
           econ_status: 'gap' -> 'native'
           econ_gaps: '["DR"]' -> '[]'
           econ_meter_type: 'n/a' -> 'n/a'                (unchanged)
           economy_model: 'unknown' -> 'unknown'          (unchanged)
      2. canon_corpus.flags (comma-separated token append; house style per econ-recrawl-apply):
           APPEND: `dr-reclassify-2026-07-17:elrond-ruling:NR/auto-fire (survivor-genre-native).
                    Per-fight econ = auto-fire-while-moving; no per-cast resource pay; meter n/a.
                    ELROND classification; Matt veto-open. Precedent: vs-phieraggi
                    (econ-recrawl-application-2026-07-17). Wave-D §4.2 sub-option C.1 stronger form.`
           APPEND: `draft-meta-overlay-2026-07-17:<offer-pool-hygiene | pre-converged-draft>`
                   (descriptor overlay; real-but-not-a-bin; SS form-lock precedent from same batch)

    NO writes to: canon_corpus.mech_note (already carries the draft-management verbatim + folk-story;
        the overlay flag makes the descriptor explicit at the flag layer, mech_note stays as-is).
    NO writes to: canon_engine_key.cell_key, resource_verbatim (extraction-source verbatim preserved).
    NO writes to: canon_engine_key.raw_json (raw fidelity preserved).
    NO writes to: canon_corpus.source_urls (extraction from megaprobe-2026-07-12; no fresh URLs added).

REVERSAL SQL (per-kit; documented in dr-reclassify-2026-07-17.md artifact §5):
    UPDATE canon_engine_key
      SET econ_status='gap', econ_gaps='["DR"]'
      WHERE kit_id IN ('hot-norseman-frost-avalanche','vs-queen-sigma');
    UPDATE canon_corpus
      SET flags = NULL
      WHERE kit_id IN ('hot-norseman-frost-avalanche','vs-queen-sigma');
    DELETE FROM corpus_schema_meta WHERE version='dr-reclassify-2026-07-17';
    (Pre-write flags were both empty-string / NULL-equivalent per PRE inspection; setting to NULL
    is the clean reversal. If Matt vetoes only one kit, apply reversal per-kit as above.)

IRON LAWS:
    1. Backup-first: ../curated/corpus.db.pre-dr-reclassify-2026-07-17-backup
    2. Asserts PRE + POST invariants identical: total=585 · engine_key=585 · orphans 0+0 ·
       dossier_owed=4 (LA-Wildsoul + LA-Valkyrie pairs; unchanged).
    3. Write scope limited to 2 canon_engine_key rows + 2 canon_corpus rows.
    4. Idempotent — re-run = ledger hit → no-op.
    5. HALT on any assert fail; rollback; exit non-zero.
    6. No new schema minted. No new bin. No new column. Uses EXISTING landed NR-shape convention
       (econ_status=native, econ_gaps=[], econ_meter_type=n/a, economy_model=unknown; 8 rows
       precedent → 10 after this write).
    7. Auto-commit collab repo (Discipline #62 pathspec-only staging); NO push (gandalf pushes).

DELTA (post-write):
    - econ_status: gap→native (2 rows)
    - econ_gaps: ["DR"]→[] (2 rows)
    - econ:DR blocked bucket: 2 kits → 0 kits (bucket disappears)
    - blocked-6 → blocked-4 (shapeshift 3 + unknown-ailment 1)
    - Projected census V12 (fires post-Wave-D Gate-2, NOT authored here): 560/564 = 99.29%
      (elrond does NOT write V12 in this script)

REGISTERED CENSUS-HYGIENE DEBT (carry into V12 authoring):
    Census V11 §1 "of which dossier_owed held-out 4" sub-row under Blocked=6 is misplaced.
    DB truth: 4 dossier_owed = 2 LA Wildsoul (in blocked-6, under shapeshift bucket) + 2 LA Valkyrie
    (NOT blocked; expressible-now despite dossier_owed=1). Only 2 of the 4 sit in blocked-6.
    V12 §1 should split the dossier_owed row into "in-pool total (4)" vs "of-which-in-blocked (2)".

CONCURRENT-PROCESS NOTE:
    gandalf-prime Wave-D DRIFT-CRITIC + jack-ryan Gate-1 are in flight in parallel with this write.
    Wave-D spec §11.a DEFER ruling and this NR-LAND ruling are compatible: engine builds NOTHING
    for DR (spec §11.a), corpus per-fight econ lands as NR (this ruling). No conflict; no rebase.
"""

import json
import pathlib
import shutil
import sqlite3
import sys
from datetime import datetime, timezone

BASE = pathlib.Path("/Users/admin/Games/reincarnated-collaboration")
DB_PATH = BASE / "agentic_orchestration/research/curated/corpus.db"
BACKUP_PATH = BASE / "agentic_orchestration/research/curated/corpus.db.pre-dr-reclassify-2026-07-17-backup"

MIGRATION_VERSION = "dr-reclassify-2026-07-17"
RULING_FLAG_PREFIX = "dr-reclassify-2026-07-17"
OVERLAY_FLAG_PREFIX = "draft-meta-overlay-2026-07-17"

# Iron-law invariants (identical PRE + POST for row-conservation UPDATE-only pass).
EXPECTED = {
    "total_corpus": 585,
    "total_engine_key": 585,
    "orphans_engine": 0,
    "orphans_corpus": 0,
    "dossier_owed": 4,
}

# Per-kit spec — verified against DB pre-write.
TARGETS = {
    "hot-norseman-frost-avalanche": {
        "pre_econ_status": "gap",
        "pre_econ_gaps": '["DR"]',
        "pre_econ_meter_type": "n/a",
        "pre_economy_model": "unknown",
        "pre_flags": "",  # None or empty in DB
        "post_econ_status": "native",
        "post_econ_gaps": "[]",
        # meter_type + economy_model UNCHANGED (n/a + unknown; matches vs-phieraggi NR-shape).
        "ruling_note": (
            "elrond-ruling:NR/auto-fire (survivor-genre-native). Per-fight econ = "
            "auto-fire-while-moving; no per-cast resource pay; meter n/a. hot = Halls of Torment; "
            "structurally identical to vs-phieraggi at per-fight layer. Draft/offer-pool is "
            "META-LAYER descriptor (see draft-meta-overlay flag). ELROND classification; "
            "Matt veto-open. Wave-D spec §4.2 C.1 stronger form (NR-land vs re-key to draft-meta)."
        ),
        "overlay_note": "offer-pool-hygiene",
    },
    "vs-queen-sigma": {
        "pre_econ_status": "gap",
        "pre_econ_gaps": '["DR"]',
        "pre_econ_meter_type": "n/a",
        "pre_economy_model": "unknown",
        "pre_flags": "",
        "post_econ_status": "native",
        "post_econ_gaps": "[]",
        "ruling_note": (
            "elrond-ruling:NR/auto-fire (VS-genre-native). Per-fight econ = auto-fire-while-moving "
            "(Victory Sword); no per-cast resource pay; meter n/a. Precedent-matched to vs-phieraggi. "
            "Pre-converged-draft + per-level +1% Might/+1% Growth compound scaling is META-LAYER "
            "(see draft-meta-overlay flag). ELROND classification; Matt veto-open. "
            "Wave-D spec §4.2 C.1 stronger form (NR-land vs re-key to draft-meta)."
        ),
        "overlay_note": "pre-converged-draft",
    },
}


def run_asserts(conn, label):
    actual = {
        "total_corpus": conn.execute("SELECT COUNT(*) FROM canon_corpus").fetchone()[0],
        "total_engine_key": conn.execute("SELECT COUNT(*) FROM canon_engine_key").fetchone()[0],
        "orphans_engine": conn.execute(
            "SELECT COUNT(*) FROM canon_engine_key ek "
            "WHERE NOT EXISTS (SELECT 1 FROM canon_corpus c WHERE c.kit_id=ek.kit_id)"
        ).fetchone()[0],
        "orphans_corpus": conn.execute(
            "SELECT COUNT(*) FROM canon_corpus c "
            "WHERE NOT EXISTS (SELECT 1 FROM canon_engine_key ek WHERE ek.kit_id=c.kit_id)"
        ).fetchone()[0],
        "dossier_owed": conn.execute("SELECT COUNT(*) FROM canon_corpus WHERE dossier_owed=1").fetchone()[0],
    }
    print(f"\n[{label}] iron-law asserts:")
    breach = False
    for k, exp in EXPECTED.items():
        act = actual[k]
        ok = act == exp
        if not ok:
            breach = True
        print(f"    {k:22s} expected={exp:>4d}  actual={act:>4d}  {'OK' if ok else 'BREACH'}")
    return actual, breach


def append_flag_token(conn, kit_id, token):
    """Append a comma-separated flag token to canon_corpus.flags. Idempotent by exact-token match."""
    existing = conn.execute("SELECT flags FROM canon_corpus WHERE kit_id=?", (kit_id,)).fetchone()[0]
    toks = [t for t in (existing.split(",") if existing else []) if t]
    if token in toks:
        return False, existing
    toks.append(token)
    new_flags = ",".join(toks)
    conn.execute("UPDATE canon_corpus SET flags=? WHERE kit_id=?", (new_flags, kit_id))
    return True, new_flags


def apply_econ_reclassify(conn, kit_id, status, gaps_json):
    """Update econ_status + econ_gaps on canon_engine_key. meter_type + economy_model UNCHANGED."""
    row = conn.execute(
        "SELECT econ_status, econ_gaps, econ_meter_type, economy_model FROM canon_engine_key WHERE kit_id=?",
        (kit_id,),
    ).fetchone()
    if not row:
        raise RuntimeError(f"target missing from canon_engine_key: {kit_id}")
    old_status, old_gaps, meter, model = row
    conn.execute(
        "UPDATE canon_engine_key SET econ_status=?, econ_gaps=? WHERE kit_id=?",
        (status, gaps_json, kit_id),
    )
    return old_status, status, old_gaps, gaps_json, meter, model


def main():
    if not DB_PATH.exists():
        print(f"ERROR: corpus.db not found at {DB_PATH}", file=sys.stderr)
        sys.exit(1)

    # Backup-first (idempotent — overwrite prior backup from this pass only if same md5).
    if not BACKUP_PATH.exists():
        shutil.copy2(str(DB_PATH), str(BACKUP_PATH))
        print(f"[BACKUP] created {BACKUP_PATH.name}")
    else:
        print(f"[BACKUP] exists (re-run) — leaving in place: {BACKUP_PATH.name}")

    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys = ON")

    try:
        _, pre_breach = run_asserts(conn, "PRE")
        if pre_breach:
            print("HALT: PRE-state assert breach (iron law). No writes.", file=sys.stderr)
            sys.exit(2)

        # Idempotency: ledger check.
        already = conn.execute(
            "SELECT COUNT(*) FROM corpus_schema_meta WHERE version=?", (MIGRATION_VERSION,)
        ).fetchone()[0]
        if already:
            # Verify the expected post-state and exit clean.
            for kit_id, spec in TARGETS.items():
                r = conn.execute(
                    "SELECT econ_status, econ_gaps FROM canon_engine_key WHERE kit_id=?",
                    (kit_id,),
                ).fetchone()
                assert r == (spec["post_econ_status"], spec["post_econ_gaps"]), (
                    f"idempotent re-run: {kit_id} not at post-state {r}"
                )
                fl = conn.execute("SELECT flags FROM canon_corpus WHERE kit_id=?", (kit_id,)).fetchone()[0]
                assert fl and RULING_FLAG_PREFIX in fl and OVERLAY_FLAG_PREFIX in fl, (
                    f"idempotent re-run: {kit_id} flags missing tokens: {fl!r}"
                )
            conn.rollback()
            print("\nAlready applied (ledger hit). Post-state verified. No-op — DB unchanged.")
            return

        # PRE row verification (targets are exactly what we expect).
        print("\n[PRE-verify] target rows match expected pre-state:")
        for kit_id, spec in TARGETS.items():
            r = conn.execute(
                "SELECT econ_status, econ_gaps, econ_meter_type, economy_model FROM canon_engine_key WHERE kit_id=?",
                (kit_id,),
            ).fetchone()
            assert r[0] == spec["pre_econ_status"], f"{kit_id}: pre econ_status {r[0]!r} != {spec['pre_econ_status']!r}"
            assert r[1] == spec["pre_econ_gaps"], f"{kit_id}: pre econ_gaps {r[1]!r} != {spec['pre_econ_gaps']!r}"
            assert r[2] == spec["pre_econ_meter_type"], f"{kit_id}: pre meter {r[2]!r}"
            assert r[3] == spec["pre_economy_model"], f"{kit_id}: pre model {r[3]!r}"
            fl = conn.execute("SELECT flags FROM canon_corpus WHERE kit_id=?", (kit_id,)).fetchone()[0]
            assert (fl or "") == spec["pre_flags"], f"{kit_id}: pre flags {fl!r} != {spec['pre_flags']!r}"
            print(f"    {kit_id:32s} OK  ({r[0]} / {r[1]} / meter={r[2]} / model={r[3]} / flags={fl!r})")

        # Apply.
        print(f"\n[APPLY] {len(TARGETS)} DR->NR reclassifies:")
        for kit_id, spec in TARGETS.items():
            old_s, new_s, old_g, new_g, meter, model = apply_econ_reclassify(
                conn, kit_id, spec["post_econ_status"], spec["post_econ_gaps"]
            )
            print(f"    {kit_id}:")
            print(f"        econ_status: {old_s!r} -> {new_s!r}")
            print(f"        econ_gaps:   {old_g!r} -> {new_g!r}")
            print(f"        meter_type:  {meter!r} (unchanged)")
            print(f"        economy_model: {model!r} (unchanged)")
            # Ruling flag.
            ruling_token = f"{RULING_FLAG_PREFIX}:{spec['ruling_note']}"
            added_r, _ = append_flag_token(conn, kit_id, ruling_token)
            # Overlay flag.
            overlay_token = f"{OVERLAY_FLAG_PREFIX}:{spec['overlay_note']}"
            added_o, new_flags = append_flag_token(conn, kit_id, overlay_token)
            print(f"        flags append: ruling={added_r}  overlay={added_o}")
            print(f"        flags now: {new_flags!r}")

        # POST verification.
        print("\n[POST-verify] target rows now at expected post-state:")
        for kit_id, spec in TARGETS.items():
            r = conn.execute(
                "SELECT econ_status, econ_gaps FROM canon_engine_key WHERE kit_id=?", (kit_id,)
            ).fetchone()
            assert r == (spec["post_econ_status"], spec["post_econ_gaps"]), (
                f"{kit_id}: post {r} != expected {(spec['post_econ_status'], spec['post_econ_gaps'])}"
            )
            print(f"    {kit_id}: OK  ({r[0]} / {r[1]})")

        # DR-blocked-bucket check: should now be empty.
        remaining_dr = conn.execute(
            "SELECT COUNT(*) FROM canon_engine_key ce JOIN canon_corpus c ON c.kit_id=ce.kit_id "
            "WHERE c.grain='kit' AND c.negative=0 AND ce.econ_gaps LIKE '%\"DR\"%'"
        ).fetchone()[0]
        print(f"\n[BUCKET] econ:DR blocked count (post): {remaining_dr} (expected 0)")
        assert remaining_dr == 0, f"DR bucket residue: {remaining_dr}"

        # NR-shape family (native/[]/n/a/unknown) should now be 10 (was 8 pre-run).
        nr_shape = conn.execute(
            "SELECT COUNT(*) FROM canon_engine_key WHERE econ_status='native' AND econ_gaps='[]' "
            "AND econ_meter_type='n/a' AND economy_model='unknown'"
        ).fetchone()[0]
        print(f"[FAMILY] NR-shape (native/[]/n/a/unknown) row count: {nr_shape} (expected 10 = 8+2)")
        assert nr_shape == 10, f"NR-shape family {nr_shape} != expected 10"

        # POST iron-law asserts.
        _, post_breach = run_asserts(conn, "POST")
        if post_breach:
            print("HALT: POST-state assert breach. Rolling back.", file=sys.stderr)
            conn.rollback()
            sys.exit(3)

        # Schema-meta ledger bump.
        now_utc = datetime.now(timezone.utc).isoformat()
        conn.execute(
            "INSERT INTO corpus_schema_meta (version, applied_utc, note) VALUES (?, ?, ?)",
            (
                MIGRATION_VERSION,
                now_utc,
                (
                    "Elrond DR 2-kit per-fight economy re-classification (2026-07-17, gandalf-prime "
                    "commissioner; Matt veto-open). Ruling: both hot-norseman-frost-avalanche + "
                    "vs-queen-sigma land as NR (near-zero / steady auto-fire, survivor-genre-native). "
                    "Precedent: vs-phieraggi (econ-recrawl-application-2026-07-17, commit 0d4479e4). "
                    "Wave-D spec §4.2 sub-option C.1 stronger form: engine builds NOTHING for DR "
                    "(§11.a DEFER holds; _DEFERRED_ECON_BINS stays empty), corpus per-fight econ lands "
                    "as NR, draft-meta shape recorded as descriptor overlay via canon_corpus.flags "
                    "(SS form-lock precedent). Writes: 2 canon_engine_key rows (econ_status gap->native, "
                    "econ_gaps ['DR']->[]; meter_type + economy_model unchanged) + 2 canon_corpus.flags "
                    "(dr-reclassify + draft-meta-overlay tokens). Row conservation: 585 unchanged. "
                    "econ:DR blocked bucket: 2->0 kits. Projected census V12 (NOT authored here): "
                    "560/564 = 99.29%. Census-hygiene debt registered for V12 authoring: V11 §1 "
                    "'dossier_owed held-out 4' misplaced under Blocked=6 (DB truth: only 2 of the 4 "
                    "dossier_owed sit in blocked-6; the '4' is the full in-pool dossier total)."
                ),
            ),
        )

        conn.commit()
        print(f"\nDR reclassify complete. Committed at {now_utc}.")

    except Exception as e:
        conn.rollback()
        print(f"\nHALT: exception during run — rolled back. {type(e).__name__}: {e}", file=sys.stderr)
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
