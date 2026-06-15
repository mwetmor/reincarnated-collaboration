# Finding — 2026-06-15 — gate1-gamora-lever-c-disambiguation

**Reviewer:** jack-ryan
**Severity:** CLEAR-WITH-AMENDMENTS
**Target:** `c35de08` — `simulation/math/lever-c-upper-tier-throughput-disambiguation-2026-06-15.md`
**Developer:** gamora (simulation seam)
**Mode:** DESIGN-MODE (Gate-1, pre-probe-code; gamora HALTed pending this clearance)
**Principles applied:** #1 (math-before-code), #3 (cross-seam impact), #4 (decisions-log as truth), #5 (severity); Disciplines #1, #11, #12; ADR-002 (within-seam measurement, my approval authority)

## What I found

The note is well-constructed: it pre-registers the interpretation rule before any probe code (Discipline #1 satisfied), correctly identifies the two separable causes gandalf located, and keeps the probe a pure MEASUREMENT (Discipline #12 N/A confirmed — `damage_modifier` is an existing knob, no schema touch). I verified the engine claims against `balance_loop.py` as it exists. Three hold cleanly, one is a measurement-plumbing gap, and one — the load-bearing interpretation rule — has a soundness hole that would let a false "architecture" verdict fire. None is fatal; all are fixable inside the seam. I clear the probe WITH the three amendments below folded in as mandatory pre-conditions on Phase-2.

**Verified TRUE:**
- M=1.0 is genuinely neutral/unscaled. `damage_modifier` defaults to 1.0 (`combatant.py:188`) and enters damage as a pure multiplicative factor in `buff_dmg_mult` (`damage_resolver.py:311`). M=0.30 is a 70% damage cut. Higher M = more player damage. The note's modifier semantics are correct.
- `_evaluate_class(player_class, gauntlet, fights_per_matchup, modifier=M)` accepts a fixed modifier and applies it with NO search around it — geared path `state.damage_modifier = _mod` (`:2968`), legacy path `combatant_a.damage_modifier = modifier` (`:2989`). The fiat-hold is real. (Line citation nit: the def is at `:2865`, not `:2855` — `:2855` is an exception handler. Cosmetic; fix in the note.)
- TIER_FLOORS (`:532-538`) and kills-only semantics (`BOSS_TIER_KILLS_ONLY`/`MINI_BOSS_TIER_KILLS_ONLY` `:505-506`; `b_dead` test `:3226`/`:3230`) match what the note states. Floors and measurement modes are correct.
- Swarm can be excluded by filtering the gauntlet — the `_is_swarm` branch (`:2899`) only fires on swarm-tier monsters, so a swarm-free gauntlet never enters the spatial slot. Sound.

## Rationale

### AMENDMENT 1 (BLOCKING on Phase-2) — the interpretation rule pivots on the WRONG modifier; this is the false-"architecture" risk

As written, **C-1 fires on `boss kills-only ≥ 0.30 at M=1.0`, "regardless of" M=0.30** (§3, primary read at M=1.0). This is the exact spurious-pass hole the probe must not have. A clear at the optimistic ceiling alone cannot distinguish "the crushed 0.0719 modifier was zeroing a capable kit" (architecture) from "1.0 is simply enough headroom to push a marginal kit over the 0.30 bar" (tells you nothing about the modifier-vs-composition question). The discriminating evidence lives at **M=0.30**, not M=1.0.

Engine-grounded: Matt's own boss calibration comment (`:516`) reads "verified killable at modifier 0.65." So M=1.0 sits *above* the modifier at which a healthy kit is already expected to clear bosses — M=1.0 is generous, not neutral-in-effect. A boss clear at M=1.0 is therefore weak evidence for "architecture." But a boss clear at **M=0.30** — a 70% damage cut, the conservative edge of the non-pathological band — proves the kit has boss tools at a genuinely modest modifier, which means only the crushed 0.0719 floor was killing it. THAT is the unambiguous architecture signal.

**Required rewrite of the rule (operative discriminator = M=0.30):**
- **C-1 (architecture):** boss kills-only ≥ 0.30 **at M=0.30**. (Clear at the conservative bound ⇒ the kit had boss tools all along; the global modifier crushed to 0.0719 was the cause.)
- **C-2 (composition):** boss craters < 0.05 **at BOTH M=1.0 AND M=0.30**. (No modifier in the healthy band rescues it.) — unchanged, already correctly two-point.
- **C-3 (partial):** any other combination — including the diagnostically important case "**clears at M=1.0 but craters/sub-floor at M=0.30**," which under the current note would have spuriously fired C-1. This is the textbook partial: modifier-modulated boss throughput that does not survive the conservative bound. Graded to Matt.

M=1.0 stays in the probe as the optimistic-ceiling corroborator (a kit that craters boss even at M=1.0 is decisively C-2-leaning), but it must NOT be the C-1 trigger. With this rewrite the rule cannot emit a false "architecture" verdict from a trivial M=1.0 pass. Cite: Principle #5, Discipline #1.

### AMENDMENT 2 (note records "boss is the pivot" — accept, but bound it explicitly)

The brief asks whether boss-as-sole-pivot is right. It is — for THIS probe's question. The probe asks "does the kit have boss tools," and boss is the cleanest discriminator. The note already reports elite/mini_boss as supporting texture. Accept the boss pivot, but fold in one guard: **if the kit clears boss at M=0.30 (C-1) yet CRATERS elite or mini_boss at the same M, the verdict is not clean architecture — flag it C-3 and report the inversion to Matt.** A kit that kills bosses but not elites is anomalous (suggests a measurement or kit-coherence artifact, not a clean architecture story) and must not be silently labeled C-1. Cite: Principle #5, survey-mode separation (description vs verdict).

### AMENDMENT 3 (BLOCKING on Phase-2) — measurement-plumbing gap: kills-only rates do NOT come off `_evaluate_class`

The note says boss/mini_boss kills-only rates are read "via existing methods (`_compute_kills_only_tier_rates`)" off the direct `_evaluate_class` call. They are NOT directly wired. `_evaluate_class` returns `(overall_winrate, win_rates, batches, loadouts)` — a per-opponent win_rates dict and BatchResult objects. But `_compute_kills_only_tier_rates` (`:3171`) consumes a different structure: a `fight_log: list[dict]` filtered on `entry["phase"] == "class"` AND `entry["iteration"] == final_iteration` (`:3214-3231`), reading per-entry `termination_reason`. A direct `_evaluate_class` call produces neither the `phase`/`iteration`-tagged fight_log nor a `final_iteration` index.

The kills-only rate (the boss-tier measurement the ENTIRE interpretation rule pivots on) must therefore be reconstructed from the `BatchResult` objects in `batches` — i.e. tally `termination_reason == "b_dead"` over each boss-tier batch's per-fight results, NOT by calling `_compute_kills_only_tier_rates` as-is. Phase-2 must confirm `BatchResult.results[*]` carries `termination_reason` (or the FightResult equivalent) in-memory. If it does NOT — i.e. the kills-only signal can only be reconstructed from the persisted fight_log — the §6 MIGRATION-HALT trigger fires: HALT, do not add a field, escalate to star-lord. The note's pre-registered HALT trigger is exactly right; this amendment just names the specific reconstruction the probe owes and the exact spot it may dead-end. Cite: Discipline #11 (empirical inspection — verify the field is in-memory before relying on it), Principle #3.

### Confirmed N/A / process
- §4 control fidelity: same floored rogue kit, genuine coords, `{def:1, mob:2, area:4, burst:1}` — apples-to-apples vs `d003f8f`. Per-matchup seed `hash(id+opp) % 100_000` (`:2888`) is deterministic given stable kit JSON. Confirmed.
- §5 determinism hygiene: stash the dirty working tree (gear/monster JSON, telemetry.db, cycle-14 noise) before the run — carries my prior Gate-2 INFO. NOTE the additional non-determinism source the note does not mention: per-fight DPS variance (`search_estimator.py:208-210`, `±15%` Prop-4 + `±20%` per-hit Prop-3) is ACTIVE in `run_batch`/`run_batch_geared` unless `enable_fight_damage_variance`/`enable_damage_variance` are disabled. It draws from `rng_dmgvar` seeded off the per-matchup seed, so it is reproducible at fixed seed — but it WIDENS the boss kills-only rate's confidence interval near the 0.30/0.05 thresholds. Use enough `fights_per_matchup` that a boss rate landing near 0.30 or 0.05 isn't a variance artifact (report n and the rate, not just the rate). INFO, not blocking.
- §6 Principle-6 N/A confirmed (existing knob held fixed, no schema write). MIGRATION-HALT pre-registration is correct and now has Amendment 3's named dead-end attached.

## Action
- [ ] gamora: rewrite §3 so C-1 pivots on **M=0.30** (not M=1.0); add the "clears 1.0 / craters 0.30" case explicitly to C-3 (Amendment 1).
- [ ] gamora: add the boss-clears-but-elite/mb-craters inversion guard to the boss-pivot rule → C-3 + report to Matt (Amendment 2).
- [ ] gamora: in Phase-2, reconstruct boss/mini_boss kills-only rate from `batches[*].results` `termination_reason == "b_dead"` (NOT `_compute_kills_only_tier_rates` as-is); verify `termination_reason` is in-memory on the batch results FIRST; if absent, fire the §6 MIGRATION-HALT to star-lord (Amendment 3).
- [ ] gamora: stash the dirty tree before the run; pick `fights_per_matchup` high enough that boss rates near 0.30/0.05 aren't Prop-3/Prop-4 variance artifacts; report n alongside rate (INFO).
- [ ] gamora: cosmetic — fix the `_evaluate_class` line cite (`:2865`, not `:2855`).
- [ ] Matt: no decision needed pre-run. The eventual C-1/C-2/C-3 verdict gates your architecture-vs-known-limitation call; C-3 returns to you graded.

## References
- Reviewed: `reincarnated-engine/src/reincarnated/simulation/math/lever-c-upper-tier-throughput-disambiguation-2026-06-15.md` (`c35de08`)
- Engine code verified: `balance_loop.py:92` (MODIFIER_LOW_THRESHOLD), `:505-506` (kills-only flags), `:516` (boss killable-at-0.65 calibration), `:532-538` (TIER_FLOORS), `:2865` (`_evaluate_class` def), `:2899` (swarm branch), `:2968`/`:2989` (modifier application), `:3171`/`:3214-3231` (kills-only rate computation)
- `damage_resolver.py:311` (damage_modifier multiplicative role); `combatant.py:188` (default 1.0); `search_estimator.py:208-210` (Prop-4 per-fight variance)
- Parent evidence: Gate-2 `0793aa2` (swarm-coverage spike PASS-WITH-INFO), refire `d003f8f`, gandalf disposition `3d727f9`
