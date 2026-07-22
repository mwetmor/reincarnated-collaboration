# Tier-3 W3′ — T3-F4′ Gate Report (mechanical execution, as-measured)

**VERDICT: FAIL** (all three legs fail; no partial pass per §6). Honorable fallback fires: RD-1 does
NOT fire; W3 RF-A/RF-B + this W3′ decomposition route to the W4 review book (§7).

**Author:** gamora (named leg), 2026-07-22. Zero-discretion execution of the FROZEN amendment sheet
`2026-07-22-tier3-w3prime-prereg.md` (frozen `904f317c`, clean PASS `c47f6cc8`) + base sheet
`2026-07-22-tier3-w3-prereg.md` (`5ea56bf3`, by reference). Reported AS MEASURED (DRIFT-CRITIC posture).

## Gate legs (SEALED renormalized rule: ≥2-of-3, all 3 metrics informative)

| Leg | Metric | Value | Threshold | Pass |
|---|---|---|---|---|
| LEG1 showcase | median composite d, 16 high-fit pairs | **0.0** | ≥ +0.5 | ✗ |
| LEG2 stress | median composite d, 16 low-fit pairs | **+0.192** | ≤ −0.5 | ✗ |
| LEG3 direction | pairs sign-correct (≥2-of-3 informative) | **10/32** | ≥ 24/32 | ✗ |

LEG2 fails on SIGN (low-fit pairs, predicted to fare WORSE in their argmin geometry, average slightly
POSITIVE). LEG3 10/32 sits at/below chance (16/32 expected under the null) — fit does not predict
geometry direction at this effect size. Direction split: high 7/16 correct, low 3/16 correct.

## Degeneracy determination (§4 + §8.3; baseline cells only; SEALED before any encounter fight)

| Metric | sd_pool′ | cells-at-bound | bound | DEGENERATE |
|---|---|---|---|---|
| mobs_killed | 13.011 | 4/32 | 40 | **No** |
| total_aoe_hits | 13.011 | 0/32 | none | **No** |
| player_damage_total | 1951.69 | 0/32 | none | **No** |

**No metric degenerate.** All 3 informative → sign rule stays ≥2-of-3 (unchanged). §4 did NOT fire, so
`alpha_realized` for the direction leg = **0.0035** (identical to the base-sheet nominal — exact under
all-pairs-3-informative, §8.4 C5). This is a REPORTING obligation discharge; the gate parameter is the
≥24/32 count regardless.

**RF-B dissolution confirmed (the whole point of W3′).** In W3 the shared `open_arena` baseline held
~19,575 destructible HP (3 elite + 37 swarm @ 1.5×) vs homogeneous encounters @ 6,000 HP — mobs_killed
saturated at the 40-ceiling (the RF-B confound). W3′ composition-matched baseline (HP 150 both arms, no
1.5×): baseline mobs_killed now spreads 0-40 (mean 15.2, matching the neutral pool mean 15.28); only
4/32 baseline cell-MEANS at the ceiling (< the 29 threshold), 16/128 baseline + 26/128 encounter fights
at ceiling. The instrument now isolates geometry — and the honest geometry-only result is FAIL.

## Composition-parity HARD INVARIANT (§2; per-pair verified)

| COMMON-4 class | enc tiers | base tiers | enc HP | parity |
|---|---|---|---|---|
| swarm | swarm×40 | swarm×40 | 150×40 | **True** |
| lane | swarm×40 | swarm×40 | 150×40 | **True** |
| volley-fan | magic×40 | magic×40 | 150×40 | **True** |
| emplacement | magic×40 | magic×40 | 150×40 | **True** |

Matched baseline = encounter's EXACT mob multiset (count+tier+HP+scalars) placed at the open_arena
DEFAULT (x,y) positions; fresh scenario_id `t3w3p_base_*` + `apply_mob_hp_difficulty_multiplier=False`
so the 1.5× gate stays inert and per-mob HP is byte-identical to the encounter (resolutions M1-M3 in
`2026-07-22-tier3-w3prime-gate-math.md`). Zero parity violations.

## Selection census (eligibility redraw, §5 RF-A fix)

| Era | n cand (post-hole) | families drafted | courts | swaps |
|---|---|---|---|---|
| I | 125 | AURA·DOT·MELEE·MPV·TOTEM·TRAP | chaos-poison/cold/fire/physical (4) | 0 |
| II | 111 | AURA·CB·DOT·MPV·TOTEM·TRAP·WW | +lightning (5) | 0 |
| III | 111 | CB·DOT·MELEE·TOTEM·TRAP·WW | chaos-poison/fire/lightning/physical (4) | 0 |
| IV | 131 | AURA·DOT·MELEE·MPV·TOTEM·TRAP·WW | 5 courts | 0 |

All eras ≥3 courts (union: chaos-poison/cold/fire/lightning/physical); zero courts-swaps needed. Tier
mix of 32 scored pairs: RATIFIED 14 · DOCKET 13 · PROPAGATED 5. **The 4 W3 hole-cell red-flags are gone**
(gd-aar-spellbinder, d2-avenger, d2-auradin, poe1-frost-blades were argmin hole picks in W3; excluding
`family_present=hole` from the pool BOTH sides redraws them to next-best buildable candidates) → **full
32 pairs, 0 red-flags.**

## Per-era decomposition (descriptive, not gated)

| Era | high median d | low median d | sign-correct |
|---|---|---|---|
| I | −0.231 | +0.442 | 2/8 |
| II | +0.240 | +0.346 | 4/8 |
| III | 0.0 | 0.0 | 2/8 |
| IV | +0.346 | +0.346 | 2/8 |

Low-fit medians are POSITIVE in every era (the LEG2 sign failure is uniform, not an era outlier). Era II
is the only era where the high-side shows a mild positive tilt.

## Per-metric medians (all 3 informative)

| Metric | high median d | low median d |
|---|---|---|
| mobs_killed | 0.0 | +0.192 |
| total_aoe_hits | 0.0 | +0.192 |
| player_damage_total | 0.0 | +0.192 |

**Metric collinearity: 28/32 pairs have identical d across all three metrics** (in homogeneous-mob
clears, kills, AOE hits, and damage move together). The ≥2-of-3 rule therefore provides no independence
here — the composite ≈ the single shared d. This is not a defect of execution; it is a property of the
instrument the base sheet acknowledged (§5 "correlation within the triple is acknowledged; ≥2-of-3 is a
robustness device, not an independence claim") and W3′ now confirms empirically.

## Per-family mean composite d (scored pairs)

MPV +0.705 · TRAP-MINE +0.793 · AURA +0.589 · TOTEM +0.208 · WHIRLWIND 0.0 · CHANNELED-BEAM −0.077 ·
MELEE-STRIKE −0.103 · DOT-AILMENT −0.231. (Mixes high+low pairs per family; descriptive only.)

## Red-flags

**None.** No per-pair red-flags, no encounter-builder red-flags, no baseline-builder red-flags, no
parity violations, no seal mutation. The latent `SHAPESHIFT/IV`-unbuildable-present edge (a `present`
cell whose only Era-IV formation is strain-4 excluded) did NOT fire — it sits at fit 0.5-0.6, mid-pack,
never drafted as argmax(1.0)/argmin(0.1). The W3 red-flag machinery was retained unchanged (would stop-
and-record, never improvise) but had nothing to catch.

## Discipline compliance

- **#1 math-before-code:** the frozen preregs ARE the math note; my mechanical resolutions M1-M3/S1/D1/
  G1/E1 were written to `2026-07-22-tier3-w3prime-gate-math.md` BEFORE the runner.
- **#2 smoke:** non-passive 2-pair smoke check ran first (as W3); both non-passive; proceeded.
- **#3 no parallel regens:** all 256 fights sequential, one seed set {20260722-25}. **No memoization**
  (§8.4 C6) — every pair's baseline ran; 128 baseline + 128 encounter = 256 distinct fight records.
- **#11 empirical inspection:** parity, degeneracy, seal-md5, HEAD-invariant, corpus md5 open/close all
  verified from data, not assumed.
- **Seal (§8.2 C2):** `2026-07-22-tier3-w3prime-pregate-seal.json` written AFTER 128 baselines, BEFORE
  any encounter fight; md5 `3c2bf3742b85fb34ea644e3ef3d59ab9` embedded in the gate output; IMMUTABLE
  (no post-encounter mutation).
- **Invariants:** engine HEAD `a3671d4…` byte-identical fire→close on `simulation/spatial_gauntlet/` +
  `generation/`; corpus.db read-only, md5 `d091881d…` stable open==close; ZERO engine/telemetry writes.

## Files
- runner: `agentic_orchestration/gamora/notes/2026-07-22-tier3-w3prime-gate.py`
- seal: `agentic_orchestration/gamora/notes/2026-07-22-tier3-w3prime-pregate-seal.json`
- output: `agentic_orchestration/gamora/notes/2026-07-22-tier3-w3prime-gate-output.json`
- math note: `agentic_orchestration/gamora/notes/2026-07-22-tier3-w3prime-gate-math.md`
