# Corpus curation log — Edition-II Stage 3 pull re-keys (existing kits, narrowed)

> **STATUS:** CURRENT (record of a completed re-key batch). Edition-II Stage 3.
> **Author:** elrond (data steward) · **Date:** 2026-07-15
> **Store:** `agentic_orchestration/research/curated/corpus.db` (elrond-owned, gitignored — this log is the committed record)
> **Batch class:** RE-KEY (evidence-judged, C3-style reversible). NO new rows. NO treatment=hybrid keys.
> **Script:** `agentic_orchestration/research/scripts/corpus_rekey_pull_stage3_2026_07_15.py`
> **Backup-before-batch:** `corpus.db.pre-stage3-rekey-2026-07-15-backup` (644 rows).

---

## 0. Ruling context (census freeze)

Under Matt's census freeze (2026-07-15), Edition-II admits the pull VOCABULARY (register v1.2)
but NO new corpus rows. The pull slice lights ONLY where EXISTING kits re-key on intrinsic
evidence — **corrections, not additions** (C3 precedent). This batch is that narrowed set.

## 1. The two engine-key re-keys (FIRED)

| kit_id | from function | to function | treatment | evidence | door |
|---|---|---|---|---|---|
| `d3-zbarb` | `none` | **`pull`** | `damage` (unchanged) | Ground Stomp **Wrenching Smash** is a RUNE (intrinsic, no gear-assembly) — 24y radial-nova pull-to-self, instant (30-frame), rooted during cast, triggers 40% CC-res. The kit's density mechanic IS the rune pull. | intrinsic rune → `function=pull` rider; `ctrl_treatment=damage` (corpus row keyed damage-primary; pull is the rider). Ancient Spear Rage Flip (outward throw) is NOT pull — knockback geometry, excluded. |
| `di-cyclone-monk-pvp` | `knockback` | **`pull`** | `control` (unchanged) | Base Cyclone Strike pull is INTRINSIC (no Legendary/essence). The existing `knockback` value is the DI engine's **force-direction-blind label**; Cyclone Strike's inward vortex IS pull (register v1.2 boundary rule: force DIRECTION inward = pull, not the engine tag). | force-direction correction; `ctrl_treatment=control` (this PvP row's identity is control-centric CC disruption per its existing mech_note). |

**cell_key change (positional splice, #5b only — every other slot byte-preserved):**

```
d3-zbarb
  old: full-move|at-target|flat|vortex_pull|damage|none|tank|cooldown|solo|melee|med|instant|active|one-shot
  new: full-move|at-target|flat|vortex_pull|damage|pull|tank|cooldown|solo|melee|med|instant|active|one-shot

di-cyclone-monk-pvp
  old: walk|self-origin|flat|vortex_pull|control|knockback|evade|cooldown|solo|melee|med|instant|active|one-shot
  new: walk|self-origin|flat|vortex_pull|control|pull|evade|cooldown|solo|melee|med|instant|active|one-shot
```

Both re-keys append a reversible-verdict token to `canon_engine_key.flags`:
`edition2-stage3-rekey:function <from>->pull (intrinsic pull evidence; reversible C3)`.

## 2. DECLINED (prior ruling stands)

- **`d3-dmo-twister`** — do NOT re-key. Asserted untouched (function stays `none`). Prior ruling.

## 3. The 6 MCD pull kits — flag-resolution key-hygiene (NOT plane admission)

`mcd-hammer-of-gravity`, `mcd-imploding-crossbow`, `mcd-voidcaller`, `mcd-encrusted-anchor`,
`mcd-echo-of-the-valley`, `mcd-burst-gale-bow`.

These carry `pull_pending_vocab=1` and have **NO `canon_engine_key` row** (MCD unresolved subset —
classless-gear architecture; the deferred docket keeps MCD atlas-invisible, spec §10.0). There is
no engine-key `ctrl_function` to re-key. Per spec §10.1.6 + register v1.2 §6.1 ("re-key to
`function=pull`; flag resolves; data honest; REMAIN off-plane"):
- **Resolved** the pending-vocab marker (pull vocabulary landed at Edition-II) and recorded
  `function=pull` at the **descriptor level** — `flags` token `edition2-pull-vocab-resolved:function-descriptor=pull`
  + a mech_note key-hygiene line.
- **NO engine-key row created** (that would be a census addition under the freeze). **NO cell_key.
  NO plane admission.** `movement=blank` keeps them off-plane regardless.

## 4. Proofs (in-script, all PASS)

| proof | result |
|---|---|
| survivor-integrity | 467 of 469 survivors byte-identical; ONLY d3-zbarb + di-cyclone-monk-pvp changed, each ONLY at cell_key #5b → `pull` |
| declined-untouched | `d3-dmo-twister` full engine-key snapshot byte-identical (function=none) |
| lattice_coord | unchanged for re-keyed rows (d3-zbarb=SMMFSI, di-cyclone-monk-pvp=DMMFSI) — function ∉ the BC6 prefix, so the "lattice_coord batch update" is vacuous for function re-keys (asserted, not skipped) |
| mcd-off-plane | all 6 MCD pull kits still have NO engine-key row (off-plane preserved; freeze honored) |
| counts | `canon_corpus`=644, `canon_engine_key`=618 (unchanged — re-keys only) |

WAL checkpointed; integrity_check = ok.

## 5. Consequence (lit measurement)

The 2 fired re-keys light **2 pull meso cells** on the Edition-II ghost field (the pull slice's
on-plane lights): d3-zbarb `[FREE-MOVE, ZONE, damage, pull, solo, active, one-shot]` +
di-cyclone-monk-pvp `[WALK, NOVA, control, pull, solo, active, one-shot]`. ZERO mcd-lit pull
cells (acceptance 25). The pull slice lights only where existing intrinsic-evidence kits reach it —
census freeze honored, vocabulary admitted clean.

## 6. Reversibility

Every re-key is a stated verdict on stated evidence; the from-value is recorded (flags token + this
log + the re-key script). The MCD flag-resolution is a descriptor annotation; the rows stay
unresolved/off-plane for the independent classless-gear-grain reason. Backup
`corpus.db.pre-stage3-rekey-2026-07-15-backup` preserves the pre-re-key state.

---

**Signed:** elrond (data steward) — the pull slice lights by correction, not addition: two existing
kits already reached inward-force ground; Edition-II gives that ground its name.
