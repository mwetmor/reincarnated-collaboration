# Gate-2 submission — KPM-band spatial recalibration Stage-2d (band wire-in)

**From:** gamora (simulation seam)
**To:** jack-ryan (Gate-2, DEV-MODE, BLOCK authority)
**Date:** 2026-06-16
**Dispatch:** `agentic_orchestration/dispatches/2026-06-16-gamora-kpm-band-spatial-recalibration.md` — Stage-2d (gandalf-ruling 2c → mechanical wire-in).
**Authority:** gandalf RULED the band (2c, 2026-06-16); Matt-authorized expanded Stage-2.
**Tag intent:** `gamora/v1.1-kpm-band-spatial-recalibration` (tag `gamora/v1.1-kpm-band-spatial-recalibration-2d`).
**Commit SHA (engine):** `92c040f0c59f322d125154ab50aab822345c6cce`
**Pushed?** NO (Matt-gated).
**Interim guard:** Phase-3 season-gen output is NON-CANONICAL and stays so until THIS Gate-2 PASSES. The guard LIFTS on Gate-2 PASS, NOT before. Not self-closed.

---

## What this Gate-2 covers

A **threshold wire-in** (it changes a gate band → it gates). Combined semantic-shift + band wire-in per the gandalf-ruled expanded Stage-2. The numerator semantic shift (Stage-2a, `1032560`) and this band wire-in (Stage-2d) together close the recalibration.

### Files changed (engine `92c040f`)
1. `src/reincarnated/simulation/gauntlet_sim.py` — `ENCOUNTER_COHORT_KPM_BAND` (`:206`) VALUES replaced (legacy 1D-duel 137–836 → gandalf per-shell mobs/min band). Gate predicate (`_route_tier_1` direct range check) UNCHANGED. `SPATIAL_ENCOUNTER_KPM_BAND` (RESOLVE) UNTOUCHED.
2. `src/reincarnated/simulation/MIGRATION.md` — v1.76 wire-in entry + provenance stamp + v1.72 reconcile; v1.75 (renumbered t4-repoint); v1.73/v1.74 cross-ref updates.
3. `src/reincarnated/simulation/math/kpm-band-spatial-recalibration-2026-06-16-STAGE2D-BAND-WIREIN.md` — math note (authored before the edit, Discipline #1).

### The gandalf-APPROVED band (wired EXACTLY — gandalf ruled; NOT re-opened)
| shell | band lo/hi (mobs/min) | bracket basis |
|---|---|---|
| boss_with_adds | [2.49, 3.78] | bimodal: p25-lo / p90-hi |
| elite_pack | [5.65, 10.00] | bimodal: p25-lo / p90-hi |
| mini_boss | [0.57, 3.30] | bimodal: p25-lo / p90-hi |
| chokepoint_corridor | [11.65, 15.88] | unimodal: p10/p90 |
| magic_pack | [6.06, 11.43] | unimodal: p10/p90 |
| open_arena | [9.90, 15.53] | unimodal: p10/p90 |

Per-shell, cohort-invariant (replicated across all 4 cohort columns; gate `[shell][cohort]` lookup structurally intact). Deliberate asymmetry on bimodal shells: lo=p25 (slog cut, excludes the `MOB_HP_DIFFICULTY_MULTIPLIER=1.5` genuine-non-clear low mode), hi=p90 NOT p75 (keep the fast-clear power-fantasy tail).

---

## Two-witness expectation (what you verify)

### (a) Clean build/import
```
python3 -c "import src.reincarnated.simulation.gauntlet_sim, src.reincarnated.simulation.t4_sim_cycling"
```
PASSES — both modules import; 6-shell / 4-cohort structural asserts (`gauntlet_sim.py:370-398`) hold. RESOLVE band reads `open_arena {'balanced': (21.5, 107.5)}` (untouched); gate band reads `open_arena Balanced (9.9, 15.53)` (wired).

### (b) Healthy slice passes central mass + genuine non-clears reject
Smoke judged the Stage-2b n=3078 mobs/min distribution (`output/kpm-band-spatial-recal-full-20260616_232152.json`) through the WIRED `ENCOUNTER_COHORT_KPM_BAND` + the REAL `_route_tier_1` predicate:

| shell | band | p50 (central) | p5 (slog) | max (trivialize) | central routes | slog routes | trivialize routes |
|---|---|---|---|---|---|---|---|
| boss_with_adds | [2.49,3.78] | 2.84 IN | 0.25 | 4.36 | PROVISIONAL_PASS | REJECT | REJECT |
| elite_pack | [5.65,10.00] | 6.95 IN | 0.83 | 11.13 | PROVISIONAL_PASS | REJECT | REJECT |
| mini_boss | [0.57,3.30] | 1.55 IN | 0.00 | 3.82 | PROVISIONAL_PASS | REJECT | REJECT |
| chokepoint_corridor | [11.65,15.88] | 13.96 IN | 11.35 | 17.63 | PROVISIONAL_PASS | REJECT | REJECT |
| magic_pack | [6.06,11.43] | 8.76 IN | 5.91 | 12.24 | PROVISIONAL_PASS | REJECT | REJECT |
| open_arena | [9.90,15.53] | 13.51 IN | 9.55 | 17.61 | PROVISIONAL_PASS | REJECT | REJECT |

Central mass (p50/p25/p75) IN-band on all 6 shells. Slog low tail (p5 < lo) REJECTS on all 6. Trivialize high tail (max > hi) REJECTS on all 6. Boundaries inclusive (lo/hi edges → PROVISIONAL_PASS). Real-gate spot check on open_arena: p50=13.51 → PROVISIONAL_PASS; kpm=5.0 (slog) → REJECT; kpm=20.0 (trivialize) → REJECT.

---

## Surfaced for Gate-2 (make your verification clean)

### 1. Full `observed_kpm` consumer audit (from Stage-2a, the precondition fix)
14 consumers classified in `simulation/math/kpm-band-spatial-recalibration-2026-06-16-STAGE2A-NUMERATOR-FIX.md` §4. **Result: NO category (c) hidden rooms/min break.** Every band-comparison consumer (W4G gate, RESOLVE cert, Track-1, phase7) judges against a mobs/min-derived band, so all were silently mis-comparing under the prior rooms/min numerator and are CORRECTED by it. **RESOLVE cert (`gauntlet_sim.py:1003/1029`) is CORRECTED-by-the-numerator-fix, NOT broken** — and is NOT re-judged by this band swap (different constant: it reads `SPATIAL_ENCOUNTER_KPM_BAND`, which I did NOT touch). No interaction between the band swap and the RESOLVE cert.

### 2. Sub-gate-3 zero-damage-floor semantic interaction (`t4_sim_cycling.py:714`)
`_check_zero_damage_floor` predicate `f.kills == 0 and duration ≥ 119s`: under the corrected mobs/min numerator, `f.kills == 0` shifts from "did NOT clear the room" (win-flag FALSE-POSITIVE on near-clears that killed 7/8 mobs) to "killed LITERALLY ZERO mobs in a ≥119s fight" — which IS a true zero-damage floor (the sub-gate's named intent). **Assessment: WARN-not-BLOCK, moves TOWARD correctness.** It is a WARN sub-gate (first-cycle empirical per SC-7 §E1), so the interaction cannot harden any kit's verdict to BLOCK; it only makes the WARN fire correctly. Evidence in Stage-2a §5. This is a numerator-fix interaction (landed at `1032560`), surfaced here so you have the complete picture for the combined wire-in.

### 3. v1.72 MIGRATION numbering-collision reconcile (deferred Stage-2 housekeeping — DONE)
AOE re-home (rocket's seam, top of MIGRATION) RETAINS v1.72; t4-repoint (gamora's seam) renumbered v1.72 → v1.75 (number-only; no content change). New Stage-2d entry is v1.76. Please verify the numbering is collision-free.

### 4. Cohort-column collapse (flagged Discipline #12)
The legacy band carried 4 distinct cohort columns per shell; this wire-in replicates one per-shell band across all 4. The cohort columns become degenerate at this gate — INTENTIONAL per gandalf "per-shell, cohort-invariant; do NOT add per-cohort variation" (the 2b characterization confirmed cohort-invariance empirically, per-shell cohort means ≤0.1 mobs/min apart). Flagged so you can confirm it is the ruled behavior, not accidental flattening.

---

## On Gate-2 PASS
- The interim guard LIFTS (Phase-3 season-gen output becomes archivable as canonical for the KPM-gate dimension).
- I do NOT self-close. I do NOT push. I do NOT lift the guard myself.
- The `MOB_HP_DIFFICULTY_MULTIPLIER` workstream is SEPARATE (Matt-scheduling-pending) — the bands are documented re-fit candidates if that multiplier changes (provenance stamp, MIGRATION v1.76), but that is documentation, not a dependency of this gate.
