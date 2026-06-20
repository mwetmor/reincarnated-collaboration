# Build brief — DPS measurement instrumentation (boss MEASURE + STR classification)

**Type:** gandalf-authored measurement-BUILD brief → knight-rider to sequence (gamora build + jack-ryan Gate-2). This is a PRODUCTION instrumentation change in gamora's simulation seam, NOT a read-only harness.
**Author:** gandalf
**Matt-declared 2026-06-19:** "Let's build the DPS measurement ASAP" — fast-tracking PAST the rocket kit-well-formedness cheap-step (Matt explicitly skipped it to inspect STR's cause directly via measured damage).
**Composes with:** the encounter-measurement doctrine ADOPTED by Matt 2026-06-19 (`agentic_orchestration/gandalf/notes/2026-06-19-encounter-measurement-doctrine-spine.md` §1, §3, RULINGS).

---

## 0. Why this build exists — TWO payoffs, one instrument

1. **Permanent (doctrine-mandated):** the adopted doctrine makes **DPS/TTK the boss-room MEASURE** — recorded telemetry that informs encounter tuning, **NEVER a gate** (Matt #8, anti-homogenization). The sim currently CANNOT measure it: `SpatialFightResult` drops per-fight damage (`player_damage_dealt = 0.0`, `t4_sim_cycling.py:1096-1098` — "SpatialFightResult carries no per-fight damage field"). This build adds the field the doctrine requires.
2. **Immediate (STR classification):** the clean boss run (spine §5) proved STR fails the boss gate by **timeout** (`timeout = 1.000`, `a_dead = 0.000`) — but could NOT distinguish *slow-but-real* (chips the boss, just misses the 240s enrage → real throughput shortfall) from *degenerate* (barely scratches the boss → kit/structural problem). The disambiguating signal is **boss-HP-removed-in-240s** = exactly the dropped damage field. This build inspects STR directly.

## 1. What's missing today
The spatial sim resolves damage internally (it must, to run fights) but does NOT surface it. `run_spatial_fight` → `SpatialFightResult` exposes winner / elapsed_s / mobs_killed / termination_reason, but `player_damage_dealt` is hardcoded `0.0` (`t4_sim_cycling.py:1096-1098`). No DPS is computable downstream.

## 2. What to build
Surface per-fight damage from `run_spatial_fight` / `SpatialFightResult`:
- **Minimum viable (deliver for certain):** total damage dealt by the player **+ ALL proxies** (minions, summons, totems, DoT, ailments) per fight. `DPS = total_damage / elapsed_s`.
- **Diagnostic ideal (for STR — deliver if reachable in one pass):** damage attributed to the **BOSS ENTITY** specifically (the `win_condition` target), so damage sunk into adds does NOT mask a boss-damage shortfall. `boss_HP_removed = damage_to_boss / boss_max_hp`.
- gamora assesses which is feasible in one pass; deliver minimum-viable for certain, diagnostic-ideal if reachable, FLAG the gap explicitly.

**Proxy-inclusive (Matt #5, the mirror of the kills rule):** damage by a summoned skeleton / totem / DoT IS the player's damage. Count ALL proxy sources — the same attribution rule that makes a proxy kill the player's kill.

## 3. The STR classification this build must answer (immediate deliverable)
Re-run the clean boss harness (`clean_boss_numbers_harness_2026_06_19.py`) with DPS now captured. For STR on both boss shells, report `boss_HP_removed`-in-240s (or `DPS × 240s` vs `boss_max_hp`):
- **STR removes ≈most of the boss HP, misses the timer** → **SLOW-BUT-REAL.** A real throughput-vs-enrage shortfall. Disposition: kit-efficacy fix OR encounter-tuning (enrage length) OR route-via-the-9-pass-floor. The doctrine stands; STR is a tuning/kit question.
- **STR removes a small fraction of boss HP** → **DEGENERATE.** A structural/kit problem (e.g. STR kits lack a real damage skill — mirror of the BC-cutover caster build-path deletion). Disposition: fix the population, not the doctrine.

The output MUST let gandalf rule which. This is the question Matt fast-tracked the build to answer.

## 4. Verify-gates — GATES, math-note-first (Discipline #1). Confirm BEFORE numbers are trusted.
- **V1 (proxy-inclusive damage):** the damage sum includes player + ALL proxy sources, not just player direct attacks. Mirror of #5 for damage. CONFIRM by reading how damage is accumulated in the spatial engine — read it, do not assert (the Gate-1 lesson).
- **V2 (no double-count):** each damage instance counted once — DoT ticks not double-summed; shared-source not double-attributed; overkill not inflating the total beyond delivered damage.
- **V3 (faithful power):** runs at max-profile investment (current default, post flip-#3), NOT the stripped ablation floor.
- **V4 (MEASURE not GATE — LOAD-BEARING, Matt #8):** the new DPS field is recorded telemetry ONLY. It does NOT enter `eligible_encounters_passed`, `gauntlet_pass`, `in_band`, or any ship/reject criterion. CONFIRM no gate reads it. A DPS *gate* would re-homogenize builds toward whatever maximizes the number — the exact monoculture the doctrine forbids.
- **V5 (boss-entity attribution, if the diagnostic-ideal is delivered):** confirm per-target damage attributes to the `win_condition` target (boss / mini-boss entity) correctly.

## 5. Endorse criteria (gandalf checks before consuming)
1. **Single-regime** (current `run_spatial_fight`, faithful power).
2. **V1–V5 confirmed** in the gamora math note before any number is read as data.
3. **DPS recorded-not-gated** (V4) — no gate regression (jack-ryan confirms).
4. **STR classification answerable** from the output — slow-but-real vs degenerate is distinguishable, not ambiguous.
5. **n per cell** matches/exceeds the boss harness cell sizes.

## 6. Hand-back
gamora → instrumented `SpatialFightResult` (new damage field) + re-run boss harness JSON with DPS / TTK / boss_HP_removed columns + math note. jack-ryan Gate-2: instrumentation correctness (V1–V5), **semantic-shift declaration** for the new field (decisions-log — this is a real schema addition), no gate regression (V4). gandalf consumes → STR classification ruling → spine §5 STR disposition + the boss MEASURE columns become permanent.

---

**Signed:** gandalf, 2026-06-19. The instrument the doctrine requires and the STR question demands — surface player + all-proxy damage so the boss MEASURE finally exists and STR's failure can finally be classified. Measured, never gated.
