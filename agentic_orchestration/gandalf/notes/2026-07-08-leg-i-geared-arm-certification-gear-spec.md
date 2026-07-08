# Leg-i Geared Arm — certification_gear Instrument Spec (Matt-Ruled 2026-07-08)

**From:** gandalf → **Consumed by:** knight-rider (transmission addendum) + gamora (wire)
**Date:** 2026-07-08
**Authority:** Matt ruled Option 3 same-session ("Ok, I agree with #3") with a binding condition:
*"assuming we have a plan to develop gear for Leg i which will be very similar to what soulbound
will eventually be."* This note IS that plan.
**Context anchors:** `2026-07-08-kr-commissioning-transmission-pilot-preconditions.md` (the two-leg
pilot this arm extends); `canonical/reap-die-rise-engine/design-decisions-session.md` §7 (the
soul-bound gear model); `canonical/reap-die-rise-story/agnostic-loot-story-spec.md` (cementing =
the loot-flow sense of "soul-bound"; NOT this instrument's concern).

---

## 1. The gap this arm measures (why it exists)

- **Ruled spec:** design-decisions-session.md §7 — *"[DECISION] Gear is pushed into the battle
  sim — so kits are validated as geared units, and gear is a treatment variable."*
- **Build state:** the certification gauntlet fights STRIPPED kits. Chain:
  `w5g1_gauntlet_execution` → `w4g1/w4g2` → `_run_spatial_w4g_batch` → `run_spatial_fight(...)`
  with no `measured_gear_stats` (t4_sim_cycling.py:1222-1238); adapter contract: *"None = no gear
  (stripped baseline)"* (spatial_resolver_adapter.py:149).
- **Lineage:** Cycle-13 W4G (commit `10a6193`) fought geared via
  `from_player_class(with_gear_stats=<cohort gear>)`. The 1D-sim-deletion repoint (`de09d8b`,
  2026-06-16, "no CombatantState pre-build") silently dropped the cohort gear; balance_loop lost
  per-percentile gear sampling in the same commit ("gear-variance forward-work is a separate
  dispatch" — balance_loop.py:2000-2005; never fired). The four cohorts have since differentiated
  ONLY the judging band — four verdicts on one identical stripped fight.
- **Classification:** spec-conflicting deferral → GAP-TO-CLOSE (OP §3.7 FLIP), not accepted state.
- **All live KPM bands are fit to stripped distributions** (W-α6 empirical, R2, R3a-D1 26,500-HP
  regime — all post-repoint). Gearing the fights without re-fitting bands mis-bands wholesale;
  re-fit-at-declared-baseline is the existing instrument discipline (MOB_HP-multiplier precedent).

## 2. Scope rulings (Matt, 2026-07-08, this session)

- **Player kits ONLY.** Gauntlet mobs are synthetic stat-blocks (endgame_mob_stat_profile budget +
  typed skills); no mob gear concept exists, and gearing mobs against player gear would violate the
  §7 sawtooth guard [DECISION/CRITICAL] (content fixed by depth; Oblivion treadmill forbidden).
  Geared player vs depth-fixed mob budgets is the ruled shape; the difficulty ladder (§4-A ruling,
  WR-gradient's home) is where geared power meets resistance.
- **Not the shipped gear systems.** Neither the legacy 110-instance bundle emission nor the
  soul-bound modular system (whose sim function `express_gear(power_level, kit)` is spec'd §7 but
  UNBUILT — verified absent from the engine). Waiting for soul-bound deadlocks: the
  agnostic-loot-engine-spec build is itself gated on "the redesigned gauntlet instrument."
- **Certification measures declared investment STATES, not RNG-rolled items** — deterministic,
  population-uniform, archetypal. That holds long-term, not just for the pilot.

## 3. The instrument — `certification_gear(cohort, power_level)`

Compose two existing, already-ruled instruments (both currently dormant on the gauntlet path):

| Dimension | Arm instrument (v0) | Soul-bound end-state (§7) |
|---|---|---|
| Structure | Legendary-T1 weapon shell + set 2pc/4pc (keystone 6b reference set, combatant.py:441-475) | Two tiers each legendary + set |
| Magnitudes | 4pc +35% dmg = chain-T4 band [25%,50%] MIDPOINT (Matt §6 ruling 2026-06-16); +18% armor / +12% hp = Legendary-T1 stat band | Same ruled anchors; §7 affixes validate against them |
| Function shape | `certification_gear(cohort, power_level=endgame_node)` | `express_gear(power_level, kit)` — signature-compatible; succession = function swap |
| Investment styles | Four cohort tilts (stat_preference_vector offense/defense/utility, `_build_cohort_combatant_stats` t4_sim_cycling.py:927, doc 41 §3 endgame T1+T2) | "Invested character dominates" living in gear/build |

- The 6b 4pc magnitude was CONSTRUCTED as chain-T4-band midpoint so bands don't move when real 6a
  sets swap in (six-profile §9 invariant) — the same invariant now underwrites the
  stripped→geared→soul-bound succession.
- **Composition detail (gamora's implementation call under these anchors):** 6b is single-neutral,
  not profile-keyed; the arm layers the cohort tilt (offense/defense/utility split) over the 6b
  skeleton. Weapon-shell handling: a fixed representative Legendary-T1 shell (per the keystone
  archive-remeasure harness pattern) — NOT per-kit real weapons (couples certification to
  kit-specific rolls). Power-level scaling may follow the `compute_balance_gear_stats` L50
  base_mag × scalar pattern (gear_catalog.py:196).
- **Declared non-goals (effect-layer, measured later by the loot campaign's
  generate→sim→check-in-band loop):** legendary specific effects (§7 crux [OPEN] A/B/C), gems,
  per-kit idiom expression, affix RNG distributions. The arm measures the STAT-POWER layer —
  the layer that moves WR/KPM.
- **F4 honesty property:** the gear stat surface carries NO mobility/exit-window stat — gear
  cannot rescue F4 martial fails. The escape test stays honest under gear; the F4-martial
  disposition fork (queued post-Leg-ii) is untouched by this arm.

## 4. Arm shape + riders

- **Leg i runs twice at the same seed (57000000), same ~20-70 post-dedup configs:** arm S
  (stripped, current instrument — the pilot's PIPE/YIELD verdicts on the instrument as-built) +
  arm G (certification_gear v0, all four cohorts — the disjunction finally measured as designed).
- **Deliverable:** per-family (F1-F4) WR/KPM deltas stripped-vs-geared, per cohort. These deltas
  are the band re-fit's input AND the empirical answer to "does gear saturate the surface."
- **#2-FF rider for arm G:** instrument identity = "certification_gear v0" named in the run
  start-banner; pre-fire verification = one grep proving `measured_gear_stats` is threaded on the
  gauntlet path (`grep -n measured_gear_stats simulation/t4_sim_cycling.py` → non-empty) + first-log
  expectation naming both arms; pilot citation = this note + the ruled transmission.
- **Wire seam:** entirely gamora (t4_sim_cycling.py, combatant.py hers;
  `run_spatial_fight` already accepts `measured_gear_stats` at spatial_engine.py:3351). Joins her
  commissioned precondition session as an added beat (hours-scale). Pilot preconditions otherwise
  unchanged; F3 is now VERIFY not fix (jack-ryan Gate-1, 2026-07-08 — my transmission carried the
  F3 STOP stale; resolved 2026-07-07, bds=48.0 locked).
- **KR:** the geared arm belongs INSIDE the `pilot_policy` decisions-log entry (repilot_driver:69
  latent gate) so the policy names both arms before the pilot fires.

## 5. Succession clause (the declared-baseline discipline, applied twice)

1. **Now:** certification baseline = stripped (as-built) — arm S certifies the pilot's
   instrument-validation verdicts (PIPE/YIELD) on the current state.
2. **At emission re-fire:** baseline moves to `certification_gear v0`; bands re-fit from arm-G
   distributions; cohort-geared becomes the declared certification state (restores the Cycle-13
   designed state + closes the §7 spec gap at the stat-power layer).
3. **When `express_gear` lands** (loot-engine campaign, gated on this instrument): function swap,
   bands re-fit again. Two band-fits over the project's life is the acknowledged, correct price.

---

**Sign-off:** gandalf, 2026-07-08. Companion rulings this session: §4 acceptance-layer reframe =
Option A (KPM measurement / WR validity screen / gradient→ladder; jack-ryan independent review leg
owed); gear-gap = Option 3 with the soul-bound-similarity condition satisfied by §3 above.
