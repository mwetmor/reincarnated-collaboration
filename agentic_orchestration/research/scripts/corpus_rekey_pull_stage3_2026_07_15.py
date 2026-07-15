#!/usr/bin/env python3
"""
corpus_rekey_pull_stage3_2026_07_15.py  — EDITION-II STAGE 3 (existing-kit pull re-keys, NARROWED)

Under Matt's census freeze (2026-07-15), Edition-II admits the pull VOCABULARY (register v1.2)
but NO new corpus rows. The pull slice lights ONLY where EXISTING kits re-key on intrinsic
evidence — corrections, not additions (C3 precedent). This script is that narrowed batch.

RE-KEYS (evidence-judged, C3-style reversible; ctrl_function → `pull`):
  1. d3-zbarb              : function none      -> pull   (FIRES)
       Evidence (pull tranche b7f773d3 enrichment): Ground Stomp WRENCHING SMASH is a RUNE
       (intrinsic, no gear-assembly), 24y radial-nova pull-to-self, instant, triggers 40% CC-res.
       The kit's density mechanic IS the rune pull. Treatment stays `damage` (the corpus row is
       keyed damage-primary; the pull is the rune rider). Likely the pull slice's first on-plane
       light (mob=full-move, delivery=at-target -> maps to a lit meso cell).
  2. di-cyclone-monk-pvp   : function knockback -> pull   (FIRES)
       Evidence (pull tranche): base Cyclone Strike pull is INTRINSIC (no Legendary/essence
       required; all essence variants are gear-assembled overlays). The existing `knockback`
       value is the DI engine's force-direction-BLIND label; Cyclone Strike's inward vortex IS
       pull (register v1.2 boundary rule: force DIRECTION inward = pull, not the engine's
       knockback tag). Treatment stays `control` (this PvP row's identity is control-centric CC
       disruption per its existing mech_note).

DECLINED (prior ruling stands):
  3. d3-dmo-twister        : do NOT re-key. Asserted untouched.

MCD 6 pull kits (mcd- prefix) — FLAG-RESOLUTION key-hygiene, NOT plane admission:
  mcd-hammer-of-gravity, mcd-imploding-crossbow, mcd-voidcaller, mcd-encrusted-anchor,
  mcd-echo-of-the-valley, mcd-burst-gale-bow.
  These carry pull_pending_vocab=1 and have NO canon_engine_key row (MCD unresolved subset —
  classless-gear architecture; deferred docket keeps MCD atlas-invisible, spec §10.0). There is
  no engine-key ctrl_function to re-key. Per spec §10.1.6 + register v1.2 §6.1 ("re-key to
  function=pull; flag resolves; data honest; REMAIN off-plane"): we RESOLVE the pending-vocab
  marker (pull vocabulary landed at Edition-II) and record function=pull at the DESCRIPTOR level
  (flags JSON + mech_note). NO engine-key row is created (that would be a census addition under
  the freeze), NO cell_key, NO plane admission. movement=blank keeps them off-plane regardless.

lattice_coord: encodes [attr, range, tempo, amp, proxy, commit] (BC6 prefix) — NOT function.
  A function-only re-key produces ZERO lattice_coord change. The brief's "lattice_coord batch
  update for every re-keyed row" is therefore satisfied vacuously for these function re-keys;
  we RE-ASSERT lattice_coord unchanged per re-keyed row as the proof (fail loud on any change).

NO new rows. NO treatment=hybrid keys (both hybrid candidates are DEFERRED rows this edition).

DISCIPLINE: backup-before-batch (caller: corpus.db.pre-stage3-rekey-2026-07-15-backup);
  survivor-integrity proof asserted in-script (the 469-survivor cell_key set changes on EXACTLY
  the 2 re-keyed rows, and ONLY at cell_key position #5b none/knockback -> pull; all 467 others
  byte-identical); WAL checkpoint; curation log per batch. IDEMPOTENT (converges).
"""

import json
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from corpus_cell_key_materialize_2026_07_13 import CELL_KEY_ORDER  # noqa: E402

# cell_key position of ctrl_function (#5b) — verified against CELL_KEY_ORDER at runtime below.
FUNCTION_SLOT_IDX = CELL_KEY_ORDER.index("ctrl_function")  # == 5

CURATED = Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated")
DB = CURATED / "corpus.db"
BACKUP = CURATED / "corpus.db.pre-stage3-rekey-2026-07-15-backup"

# The two evidence-judged engine-key re-keys: (kit_id, from_function, to_function)
ENGINE_KEY_REKEYS = [
    ("d3-zbarb", "none", "pull"),
    ("di-cyclone-monk-pvp", "knockback", "pull"),
]
DECLINED = ["d3-dmo-twister"]  # asserted untouched
MCD_PULL_KITS = [
    "mcd-hammer-of-gravity", "mcd-imploding-crossbow", "mcd-voidcaller",
    "mcd-encrusted-anchor", "mcd-echo-of-the-valley", "mcd-burst-gale-bow",
]


def engine_key_snapshot(cur, kit_id):
    """Full canon_engine_key row snapshot for a kit (for untouched-proof on the declined row)."""
    row = cur.execute(
        "SELECT ctrl_treatment, ctrl_function, geometry_value, delivery_value, "
        "def_bin, economy_model, activation_val, dependency_val, mob_policy_while_casting, cell_key "
        "FROM canon_engine_key WHERE kit_id=?", (kit_id,)).fetchone()
    return row


def splice_function(cell_key: str, new_fn: str) -> str:
    """Replace ONLY cell_key position #5b (ctrl_function) — a positional splice on the stored
    string, so no other slot can drift. Fails loud if the key is not the expected 14-slot shape."""
    parts = cell_key.split("|")
    assert len(parts) == len(CELL_KEY_ORDER), (
        f"cell_key has {len(parts)} slots, expected {len(CELL_KEY_ORDER)}: {cell_key}")
    parts[FUNCTION_SLOT_IDX] = new_fn
    return "|".join(parts)


def survivor_cellkeys(cur):
    """The 469-survivor kit_id -> cell_key map (non-mcd, non-negative combat-kits)."""
    rows = cur.execute(
        "SELECT k.kit_id, k.cell_key FROM canon_engine_key k "
        "JOIN canon_corpus c ON c.kit_id=k.kit_id "
        "WHERE k.row_class='combat-kit' AND c.negative=0 AND c.game!='mcd'"
    ).fetchall()
    return {kid: ck for kid, ck in rows}


def main():
    assert BACKUP.exists(), f"pre-stage3 backup missing: {BACKUP}"
    con = sqlite3.connect(DB)
    cur = con.cursor()

    print("== STAGE 3: existing-kit pull re-keys (census-freeze narrowed) ==")

    # -------- capture pre-state survivor cell_keys + declined-row snapshot --------
    pre_surv = survivor_cellkeys(cur)
    declined_pre = {k: engine_key_snapshot(cur, k) for k in DECLINED}
    lattice_pre = {}
    for kid, _, _ in ENGINE_KEY_REKEYS:
        lattice_pre[kid] = cur.execute(
            "SELECT lattice_coord FROM canon_corpus WHERE kit_id=?", (kid,)).fetchone()[0]

    # ============ (A) the two engine-key re-keys (positional cell_key splice) ============
    rekey_record = []
    for kit_id, from_fn, to_fn in ENGINE_KEY_REKEYS:
        row = cur.execute(
            "SELECT ctrl_function, cell_key FROM canon_engine_key WHERE kit_id=?", (kit_id,)).fetchone()
        assert row is not None, f"{kit_id}: no engine-key row to re-key"
        cur_fn, old_cell_key = row
        if cur_fn == to_fn:
            print(f"  = {kit_id:22s} already function={to_fn} (idempotent no-op)")
            rekey_record.append((kit_id, to_fn, to_fn, old_cell_key, old_cell_key))
            continue
        assert cur_fn == from_fn, (
            f"{kit_id}: expected function={from_fn} before re-key, found {cur_fn} "
            f"(evidence-judged re-key aborted — state mismatch)")
        # confirm the stored cell_key's #5b matches the current function (integrity of the splice)
        assert old_cell_key.split("|")[FUNCTION_SLOT_IDX] == from_fn, (
            f"{kit_id}: cell_key #5b ({old_cell_key.split('|')[FUNCTION_SLOT_IDX]}) != "
            f"ctrl_function ({from_fn}) — stored key inconsistent, aborting")
        # positional splice: ONLY #5b changes; every other slot byte-preserved
        new_cell_key = splice_function(old_cell_key, to_fn)
        cur.execute("UPDATE canon_engine_key SET ctrl_function=?, cell_key=? WHERE kit_id=?",
                    (to_fn, new_cell_key, kit_id))
        # append a reversible-verdict note to flags (never destroy the from-value record)
        flags = cur.execute("SELECT flags FROM canon_engine_key WHERE kit_id=?", (kit_id,)).fetchone()[0]
        flags_list = json.loads(flags) if flags else []
        flags_list.append(f"edition2-stage3-rekey:function {from_fn}->pull (intrinsic pull evidence; reversible C3)")
        cur.execute("UPDATE canon_engine_key SET flags=? WHERE kit_id=?",
                    (json.dumps(flags_list), kit_id))
        rekey_record.append((kit_id, from_fn, to_fn, old_cell_key, new_cell_key))
        print(f"  ~ {kit_id:22s} function {from_fn:9s} -> {to_fn}   cell_key #5b updated")

    # ============ (B) MCD 6 pull kits — flag-resolution key-hygiene (NO engine-key row) ============
    for kit_id in MCD_PULL_KITS:
        # confirm still no engine-key row (must NOT create one under the freeze)
        has_key = cur.execute("SELECT COUNT(*) FROM canon_engine_key WHERE kit_id=?", (kit_id,)).fetchone()[0]
        assert has_key == 0, f"{kit_id}: unexpectedly has an engine-key row — freeze violated upstream"
        # resolve the pending marker: pull vocabulary now exists (v1.2). Record function=pull at
        # the descriptor level in flags; keep pull_pending_vocab column as a RESOLVED audit marker
        # by rewriting the flags token pull_pending_vocab:true -> function-descriptor:pull + resolved.
        flags = cur.execute("SELECT flags FROM canon_corpus WHERE kit_id=?", (kit_id,)).fetchone()[0]
        flags_list = json.loads(flags) if flags else []
        if any(f.startswith("edition2-pull-vocab-resolved") for f in flags_list):
            print(f"  = {kit_id:22s} pull-vocab already resolved (idempotent no-op)")
            continue
        flags_list.append("edition2-pull-vocab-resolved:function-descriptor=pull "
                          "(pull vocabulary landed v1.2; OFF-PLANE — classless-gear, movement=blank, no engine-key row)")
        cur.execute("UPDATE canon_corpus SET flags=? WHERE kit_id=?", (json.dumps(flags_list), kit_id))
        # append a mech_note key-hygiene line (idempotent guard on the marker string)
        cur.execute(
            "UPDATE canon_corpus SET mech_note = COALESCE(mech_note,'') || ? "
            "WHERE kit_id=? AND mech_note NOT LIKE '%EDITION-II PULL-VOCAB RESOLVED%'",
            (" [EDITION-II PULL-VOCAB RESOLVED 2026-07-15]: `pull` is now canonical (register v1.2); "
             "this weapon's intrinsic Gravity-enchant inward force is function=pull at the descriptor "
             "level. Kit REMAINS OFF-PLANE: MCD classless-gear architecture (gear-assembled per "
             "four-probe test), movement=blank, no engine-key row -> fails the fit2reg_movement gate. "
             "Key-hygiene only, not plane admission (spec §10.1.6). Full curation deferred post-Edition-II.",
             kit_id))
        print(f"  ~ {kit_id:22s} pull-vocab resolved (descriptor=pull; OFF-PLANE, no engine-key row)")

    con.commit()

    # ============ PROOFS ============
    # (P1) declined row untouched (full snapshot byte-identical; ctrl_function stays 'none')
    for k in DECLINED:
        now = engine_key_snapshot(cur, k)
        assert now == declined_pre[k], f"DECLINED row {k} was modified — must be untouched!"
        assert now[1] == "none", f"{k}: ctrl_function drifted from 'none' (got {now[1]})"
    print(f"\n  PROOF declined-untouched: {DECLINED} unchanged (function=none) OK")

    # (P2) survivor set changes on EXACTLY the 2 re-keyed rows, ONLY at position #5b
    post_surv = survivor_cellkeys(cur)
    assert set(pre_surv) == set(post_surv), "survivor kit_id SET changed — no adds/drops allowed!"
    changed = {kid for kid in pre_surv if pre_surv[kid] != post_surv[kid]}
    expected_changed = {kid for kid, _, _ in ENGINE_KEY_REKEYS}
    assert changed == expected_changed, (
        f"survivor cell_key changes != the 2 re-keyed rows.\n"
        f"  changed: {sorted(changed)}\n  expected: {sorted(expected_changed)}")
    # verify each change is ONLY at position #5b (ctrl_function), from-> pull
    for kid in changed:
        old_parts = pre_surv[kid].split("|")
        new_parts = post_surv[kid].split("|")
        diff_pos = [i for i in range(len(old_parts)) if old_parts[i] != new_parts[i]]
        assert diff_pos == [5], f"{kid}: cell_key changed at positions {diff_pos}, expected only [5] (#5b function)"
        assert new_parts[5] == "pull", f"{kid}: #5b is {new_parts[5]}, expected 'pull'"
    n_unchanged = len([k for k in pre_surv if pre_surv[k] == post_surv[k]])
    print(f"  PROOF survivor-integrity: {len(changed)} rows changed (exactly {sorted(changed)}), "
          f"each ONLY at cell_key #5b -> 'pull'; {n_unchanged} survivors byte-identical OK")

    # (P3) lattice_coord unchanged for re-keyed rows (function not encoded in BC6 prefix)
    for kid, _, _ in ENGINE_KEY_REKEYS:
        now = cur.execute("SELECT lattice_coord FROM canon_corpus WHERE kit_id=?", (kid,)).fetchone()[0]
        assert now == lattice_pre[kid], (
            f"{kid}: lattice_coord changed {lattice_pre[kid]} -> {now} — function must NOT touch BC6 prefix!")
    print(f"  PROOF lattice_coord: unchanged for re-keyed rows "
          f"({', '.join(f'{k}={lattice_pre[k]}' for k, _, _ in ENGINE_KEY_REKEYS)}) — "
          f"vacuous update (function ∉ lattice_coord) OK")

    # (P4) MCD 6 still have no engine-key row (freeze: no census addition)
    for kit_id in MCD_PULL_KITS:
        has_key = cur.execute("SELECT COUNT(*) FROM canon_engine_key WHERE kit_id=?", (kit_id,)).fetchone()[0]
        assert has_key == 0, f"{kit_id}: engine-key row created — census-freeze violated!"
    print(f"  PROOF mcd-off-plane: all 6 MCD pull kits still have NO engine-key row (off-plane preserved) OK")

    # (P5) corpus + engine_key counts unchanged (no adds/drops)
    n_corpus = cur.execute("SELECT COUNT(*) FROM canon_corpus").fetchone()[0]
    n_key = cur.execute("SELECT COUNT(*) FROM canon_engine_key").fetchone()[0]
    assert n_corpus == 644 and n_key == 618, f"counts drifted: corpus={n_corpus} key={n_key}"
    print(f"  PROOF counts: canon_corpus=644, canon_engine_key=618 (unchanged — re-keys only) OK")

    con.execute("PRAGMA wal_checkpoint(TRUNCATE)")
    con.commit()
    con.close()

    # ---- summary of re-key records (for the log) ----
    print("\n  RE-KEY RECORD (old cell_key -> new cell_key):")
    for kid, from_fn, to_fn, old_ck, new_ck in rekey_record:
        print(f"    {kid}:  function {from_fn} -> {to_fn}")
        print(f"      old: {old_ck}")
        print(f"      new: {new_ck}")

    print("\nSTAGE 3 COMPLETE — 2 evidence-judged pull re-keys fired (d3-zbarb, di-cyclone-monk-pvp); "
          "d3-dmo-twister declined; 6 MCD pull kits flag-resolved off-plane. No new rows, no hybrid keys.")


if __name__ == "__main__":
    main()
