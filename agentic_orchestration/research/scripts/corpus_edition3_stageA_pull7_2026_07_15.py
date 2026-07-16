#!/usr/bin/env python3
"""
corpus_edition3_stageA_pull7_2026_07_15.py — EDITION-III STAGE A

Re-insert + complete keying for the 7-row pull-intrinsic class-kit tranche that was
INSERTED-then-REVERTED under the Edition-II census freeze (revert log:
research/curated/corpus-curation-pull-tranche-deferred-2026-07-15-log.md). Matt lifted the
freeze 2026-07-15 ("Edition 3: one batch"); gandalf's ONE-BATCH commission
(gandalf/briefs/2026-07-15-elrond-edition3-one-batch-commission.md §1) is the authority.

WHY A NEW SCRIPT (not a re-run of corpus_ingest_pull_tranche_2026_07_15.py):
  The Stage-1 insert script carries a hard-coded SURVIVOR_SHA_BASELINE = ce67bfba... that is
  the PRE-Stage-3 survivor state. Since that script was written, the Edition-II Stage-3 pull
  re-keys FIRED (d3-zbarb none->pull, di-cyclone-monk-pvp knockback->pull) — both are survivor
  rows, so the 469-survivor digest legitimately moved to fdd7fbfa... . The old script's guard
  therefore fails BEFORE (correctly — its baseline predates Stage-3). Rather than mutate the
  committed reverted-batch artifact, this Edition-III script:
    - reuses the SAME 7-row manifest + enrichment from the insert module (single source of truth
      for the row data — no drift),
    - guards against the CURRENT (post-Stage-3) survivor baseline,
    - additionally proves that the current survivor state == pre-edition2 survivor state EXCEPT
      the two documented Stage-3 re-keys (so the baseline shift is fully accounted, not blind),
    - asserts each of the 7 intended cell_keys explicitly (the keying is COMPLETED, not deferred).

FOUR LIVE FLAGS (brief §1) — re-verified against source this stage:
  (a) la-destroyer-gravity-compression pull is INFERRED. Re-verified against the tranche source
      row (2026-07-15-pull-intrinsic-classkit-tranche.md line 24): the row's own treatment field
      says "damage-primary (no explicit pull on living enemies in base description)"; the mech_note
      says the pull is "implicit ... rather than an explicit 'enemies moved toward caster'
      description." NEVER-INVENT governs -> function=none, pull_pending_vocab=0, pull-implicit
      annotation. The d4-spiritborn-vortex movement is likewise source-silent ("unknown (not
      documented in available sources)", line 25) -> mob=blank honest-NULL (cell won't light on the
      movement gate). CONFIRMED.
  (c) Destroyer cell-distinctness ACROSS GRAINS: the 4 pull-tranche Destroyer rows are SKILL grain
      (individual skills: Vortex Gravity / Gravity Impact / Gravity Force / Gravity Compression);
      the LA-tranche la-destroyer-rage-hammer + la-destroyer-gravity-training are ENGRAVING/identity
      grain (Stage B). DIFFERENT grains of the same class — both are legitimate rows measuring
      different objects (a skill vs an identity path). GRAIN-OF-RECORD adjudication (this script
      asserts it): the 4 skill-grain rows carry atlas cell placement here; the 2 engraving-grain
      rows carry atlas placement in Stage B; they do NOT collide because their cell_keys differ
      (Stage B keys the identity paths from their own prefix_claims). Among the 4 skill-grain rows,
      all cell_keys are DISTINCT (asserted below): they differ on {geometry, commit, dependency,
      amp}. No two collapse.
  (d) di-cyclone-strike-monk-base vs di-cyclone-monk-pvp land in DIFFERENT cells (asserted below):
      movement rooted vs walk, delivery melee vs self-origin, commit wind-up vs instant.
  (e) Undecember Illusion Hook bounded re-check: the tranche's empty-verdict line (line 102) rules
      it EMPTY per the intrinsic bar (classless rune-assembled, not class-intrinsic). In-corpus
      evidence is decisive: ud-illusion-family already carries the HOOK as a weapon-type variant of
      an ECHO-COPY skill (geometry=multi_projectile, damage x none), NOT a grappling pull. AFFIRM
      EXCLUSION; no new ud- row. (No new crawl — bounded to existing evidence, per brief.)

IDEMPOTENT: additive; the 7 rows upsert from the shared manifest each run; the 469 survivor
  cell_keys (post-Stage-3) are guarded byte-identical before + after. Backup taken by caller
  (corpus.db.pre-edition3-2026-07-15-backup).
"""

import hashlib
import importlib.util
import json
import sqlite3
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))
from corpus_cell_key_materialize_2026_07_13 import serialize_cell_key  # noqa: E402

DB = Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/corpus.db")
PRE_E2_BACKUP = DB.parent / "corpus.db.pre-edition2-2026-07-15-backup"

# ---- import the Stage-1 insert module to REUSE its manifest (NEW, ENRICH, upsert fns) ----
_spec = importlib.util.spec_from_file_location(
    "pull_insert", SCRIPTS / "corpus_ingest_pull_tranche_2026_07_15.py")
pins = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pins)

NEW_KIT_IDS = pins.NEW_KIT_IDS   # the 7 additive kit_ids (excluded from survivor digest)

# The two documented Edition-II Stage-3 pull re-keys — the ONLY survivor rows that changed
# since pre-edition2. Used to PROVE the baseline shift is fully accounted (not blind drift).
STAGE3_REKEYS = {
    "d3-zbarb": ("none", "pull"),
    "di-cyclone-monk-pvp": ("knockback", "pull"),
}

# The 7 intended cell_keys (serialized from the shared manifest — asserted, keying COMPLETED).
INTENDED_CELL_KEYS = {
    "la-destroyer-vortex-gravity":
        "rooted|melee|spiky|vortex_pull|damage|pull|tank|cooldown|solo|melee|high|instant|active|one-shot",
    "la-destroyer-gravity-impact":
        "rooted|melee|flat|vortex_pull|damage|pull|tank|generator-spender|solo|melee|med|channel|active|build→spend",
    "la-destroyer-gravity-force":
        "walk|melee|flat|line|damage|pull|mitigate|generator-spender|solo|melee|med|wind-up|active|build→spend",
    "la-destroyer-gravity-compression":
        "rooted|melee|spiky|ground_targeted_circle|damage|none|mitigate|generator-spender|solo|melee|med|channel|active|build→spend",
    "d4-spiritborn-vortex":
        "blank|at-target|spiky|vortex_pull|damage|pull|evade|generator-spender|solo|mid|med|instant|active|build→spend",
    "d3-wizard-black-hole":
        "rooted|at-target|spiky|vortex_pull|damage|pull|glass|spend|solo|ranged|med|instant|active|one-shot",
    "di-cyclone-strike-monk-base":
        "rooted|melee|flat|vortex_pull|damage|pull|evade|cooldown|solo|melee|med|wind-up|active|one-shot",
}


def survivor_rows(cur):
    """The 469 PRE-EXISTING survivor rows (non-mcd active combat-kit), EXCLUDING the 7 additive
    new kit_ids. kit_id|cell_key strings, ordered."""
    rows = cur.execute(
        "SELECT k.kit_id||'|'||k.cell_key FROM canon_engine_key k "
        "JOIN canon_corpus c ON c.kit_id=k.kit_id "
        "WHERE k.row_class='combat-kit' AND c.negative=0 AND c.game!='mcd' "
        "ORDER BY k.kit_id"
    ).fetchall()
    return [r[0] for r in rows if r[0].split("|", 1)[0] not in NEW_KIT_IDS]


def digest(rows):
    return hashlib.sha256("\n".join(rows).encode()).hexdigest()


def prove_baseline_shift_accounted(cur):
    """Prove: current survivor state == pre-edition2 survivor state EXCEPT exactly the two
    documented Stage-3 re-keys. Fail loud on any UNaccounted difference."""
    cur_rows = survivor_rows(cur)
    con2 = sqlite3.connect(PRE_E2_BACKUP)
    pre_rows = survivor_rows(con2.cursor())
    con2.close()
    cur_d = dict(x.split("|", 1) for x in cur_rows)
    pre_d = dict(x.split("|", 1) for x in pre_rows)
    assert set(cur_d) == set(pre_d), (
        f"survivor kit_id SET differs vs pre-edition2 (unexpected add/remove): "
        f"added {set(cur_d)-set(pre_d)}, removed {set(pre_d)-set(cur_d)}")
    diffs = {k for k in cur_d if cur_d[k] != pre_d[k]}
    assert diffs == set(STAGE3_REKEYS), (
        f"survivor rows changed vs pre-edition2 are NOT exactly the two Stage-3 re-keys.\n"
        f"  changed: {sorted(diffs)}\n  expected: {sorted(STAGE3_REKEYS)}")
    # and prove each change is #5b only (from-fn -> to-fn), every other slot byte-identical
    for k, (from_fn, to_fn) in STAGE3_REKEYS.items():
        pre_slots = pre_d[k].split("|")
        cur_slots = cur_d[k].split("|")
        changed = [i for i in range(len(pre_slots)) if pre_slots[i] != cur_slots[i]]
        assert changed == [5], f"{k}: expected ONLY slot #5b (index 5) changed, got {changed}"
        assert pre_slots[5] == from_fn and cur_slots[5] == to_fn, (
            f"{k}: expected {from_fn}->{to_fn} at #5b, got {pre_slots[5]}->{cur_slots[5]}")
    print("  [baseline-accounted] current survivor state == pre-edition2 EXCEPT the 2 documented "
          "Stage-3 re-keys (d3-zbarb none->pull, di-cyclone-monk-pvp knockback->pull), #5b only. OK")
    return digest(cur_rows)


def assert_cell_distinctness(cur):
    """Flag (c) + (d): the 4 skill-grain Destroyer rows are mutually distinct cells; di-base and
    di-pvp are distinct cells. Read from the DB after insert (the source of truth)."""
    destroyer_skill = ["la-destroyer-vortex-gravity", "la-destroyer-gravity-impact",
                       "la-destroyer-gravity-force", "la-destroyer-gravity-compression"]
    keys = {}
    for kid in destroyer_skill + ["di-cyclone-strike-monk-base", "di-cyclone-monk-pvp"]:
        row = cur.execute("SELECT cell_key FROM canon_engine_key WHERE kit_id=?", (kid,)).fetchone()
        assert row is not None, f"{kid} has no engine-key row"
        keys[kid] = row[0]
    # 4 Destroyer skill-grain cell_keys all distinct
    dk = [keys[k] for k in destroyer_skill]
    assert len(set(dk)) == 4, f"Destroyer skill-grain cells NOT all distinct: {dk}"
    print(f"  [flag c] 4 Destroyer skill-grain rows -> 4 distinct cells OK")
    # di-base vs di-pvp distinct
    assert keys["di-cyclone-strike-monk-base"] != keys["di-cyclone-monk-pvp"], (
        f"di-base and di-pvp collapse to one cell:\n"
        f"  base: {keys['di-cyclone-strike-monk-base']}\n  pvp : {keys['di-cyclone-monk-pvp']}")
    print(f"  [flag d] di-cyclone-strike-monk-base != di-cyclone-monk-pvp (distinct cells) OK")


def main():
    con = sqlite3.connect(DB)
    cur = con.cursor()

    n_corpus_pre = cur.execute("SELECT COUNT(*) FROM canon_corpus").fetchone()[0]
    n_key_pre = cur.execute("SELECT COUNT(*) FROM canon_engine_key").fetchone()[0]
    print(f"== EDITION-III STAGE A: pull-7 re-insertion + keying completion ==")
    print(f"  pre-state: corpus={n_corpus_pre}, engine_key={n_key_pre}")

    # ---- GUARD 1: prove the (post-Stage-3) survivor baseline is fully accounted ----
    pre_digest = prove_baseline_shift_accounted(cur)

    # ---- re-insert the 7 rows + enrichment (reuse the shared manifest) ----
    print("  inserting 7 pull-tranche rows (idempotent upsert from shared manifest)...")
    keyed = {}
    for r in pins.NEW:
        pins.upsert_corpus_row(cur, r)
        ck = pins.upsert_engine_key(cur, r)
        keyed[r["kit_id"]] = ck
        print(f"    + {r['kit_id']:34s} t={r['treatment']:7s} f={r['function']:6s} ck-ok")
    for kid, addendum in pins.ENRICH.items():
        cur.execute("UPDATE canon_corpus SET mech_note = COALESCE(mech_note,'') || ? "
                    "WHERE kit_id=? AND mech_note NOT LIKE '%EDITION-II ENRICHMENT 2026-07-15%'",
                    (addendum, kid))
        print(f"    ~ enriched {kid} (mech_note fact-append; cell_key untouched)")

    # ---- ASSERT: each of the 7 cell_keys is the intended key (keying COMPLETED) ----
    for kid, want in INTENDED_CELL_KEYS.items():
        got = cur.execute("SELECT cell_key FROM canon_engine_key WHERE kit_id=?", (kid,)).fetchone()[0]
        assert got == want, f"cell_key mismatch {kid}:\n  want {want}\n  got  {got}"
    print(f"  [keying] all 7 intended cell_keys asserted byte-exact OK")

    # ---- ASSERT: flag (c) + (d) cell-distinctness ----
    assert_cell_distinctness(cur)

    # ---- schema marker (Edition-III Stage A) ----
    cur.execute("INSERT INTO corpus_schema_meta VALUES (?,?,?)", (
        "edition3-stageA-pull7-2026-07-15", "2026-07-15T00:00:00Z",
        "Edition-III Stage A (elrond): pull-7 re-insertion + keying COMPLETION post-freeze. The 7 "
        "pull-tranche rows (4 la-Destroyer skill-grain + d4-spiritborn-vortex + d3-wizard-black-hole "
        "+ di-cyclone-strike-monk-base) re-inserted (Matt 'Edition 3: one batch'), keyed at full "
        "completeness with function=pull (register v1.2). Both proposed hybrids -> damage+pull rider "
        "(hybrid-assignment-criteria memo §4; gandalf-adopted). Flag(a): gravity-compression pull "
        "INFERRED per source -> function=none (never-invent); d4-spiritborn movement source-silent -> "
        "mob=blank. Flag(c): 4 Destroyer SKILL-grain rows distinct + separate grain from the 2 LA "
        "engraving-grain rows (Stage B). Flag(d): di-base != di-pvp. Flag(e): Illusion Hook affirmed "
        "EXCLUDED (echo-copy, not pull). Enrichment re-applied on di-cyclone-monk-pvp + d3-zbarb. "
        "Survivor baseline is the POST-Stage-3 digest (2 documented re-keys accounted); 469 survivors "
        "byte-identical before+after this stage.",
    ))

    # ---- GUARD 2: survivor digest byte-identical before + after (new rows must not perturb) ----
    post_digest = digest(survivor_rows(cur))
    assert post_digest == pre_digest, (
        f"SURVIVOR DIGEST CHANGED during Stage A (must not happen — additive only)!\n"
        f"  before: {pre_digest}\n  after : {post_digest}")
    print(f"  [survivor-guard] 469 survivors byte-identical before+after: {post_digest[:16]}... OK")

    con.commit()

    # ---- report ----
    n_corpus = cur.execute("SELECT COUNT(*) FROM canon_corpus").fetchone()[0]
    n_key = cur.execute("SELECT COUNT(*) FROM canon_engine_key").fetchone()[0]
    n_la = cur.execute("SELECT COUNT(*) FROM canon_corpus WHERE kit_id LIKE 'la-%'").fetchone()[0]
    n_pull = cur.execute("SELECT COUNT(*) FROM canon_engine_key WHERE ctrl_function='pull'").fetchone()[0]
    n_hybrid = cur.execute("SELECT COUNT(*) FROM canon_engine_key WHERE ctrl_treatment='hybrid'").fetchone()[0]
    print(f"\n  post-state: corpus={n_corpus} (+{n_corpus-n_corpus_pre}), engine_key={n_key} "
          f"(+{n_key-n_key_pre})")
    print(f"  la- rows: {n_la} | ctrl_function='pull' rows: {n_pull} | hybrid rows: {n_hybrid} "
          f"(frontier stays empty)")
    con.close()
    print("STAGE A COMPLETE.")


if __name__ == "__main__":
    main()
