# Pre-registered interpretation rule — STR 9-pass-floor clear-room run

**Author:** gandalf
**Date:** 2026-06-19 (written BEFORE the gamora run returns — deliberately, the third time this discipline holds this session)
**Why pre-register:** the boss-numbers run already taught the lesson twice — gamora's headline drifted toward "degenerate," jack-ryan's framing drifted toward "lean degenerate/structural," and only the pre-registered read held STR at "melee target-allocation failure." The antidote to motivated reasoning is to fix the read BEFORE the data lands. This note binds how I will interpret the headline (STR's clear-room pass count of 14, per cohort, per clear-type) so I cannot post-hoc bend the disposition to whatever returns.
**Consumes:** output of the run brief `agentic_orchestration/gandalf/requests/2026-06-19-str-9pass-floor-clear-room-run-brief.md` (gamora harness, tier_1-bypassed on all 18; jack-ryan Gate-2 V1–V6).
**Composes with:** the boss-numbers pre-reg (`2026-06-19-boss-numbers-pre-registered-interpretation.md`, RESOLVED) and the doctrine spine §5.

---

## The single fact the run produces

The ship gate is `gauntlet_pass(cohort)` = `eligible_encounters_passed(cohort) >= 9` over the 18-encounter reference gauntlet. STR auto-fails the 4 boss encounters (survive+kill 0.000, already settled — that is the PREMISE, not the question). Therefore:

> **STR ships via the floor IFF it passes ≥ 9 of the 14 clear-room encounters.**

The 14 clear shells, verified from `generation/endgame_encounter_catalog.py` (grep-counted, not asserted):

| Group | Shells | n | Allocation exposure |
|---|---|---|---|
| **No-anchor / pure-swarm** | open_arena ×4 + chokepoint_corridor ×3 | **7** | undifferentiated mob field — NO priority target to mis-allocate against. Cleave shines. Allocation problem CANNOT manifest. |
| **Anchored / priority-structure** | magic_pack ×3 + elite_pack ×4 | **7** | tougher priority targets within a pack; elite_pack is BIMODAL (grouped with boss_with_adds + mini_boss in the gandalf deliberate-asymmetry note, `gauntlet_sim.py:303` — high-HP anchor + adds). Allocation problem CAN recur. |

Per shell I get tier_2 KPM (proxy-inclusive), the cohort band, and the **failure SIDE** (below-floor / in-band / above-ceiling). All four cohorts (the gate is per-cohort).

## Cohort-invariance — the EXPECTATION, bound in advance (the catch)

The clear-room bands are **cohort-invariant** (`gauntlet_sim.py:317-322`: open_arena `(9.90, 15.53)` is identical for all four cohorts; same for choke/magic/elite; code comment line 301-302: "cohort-invariance confirmed empirically... Do NOT add per-cohort variation"). The boss harness corroborated this — STR boss KPM 0.25 and surv+kill agreed across cohorts within 0.1. **Therefore I PRE-COMMIT: STR's clear-room pass-count should agree across all 4 cohorts within ~1 encounter.** If cohorts DIVERGE by >1 encounter, that is the SURPRISE — flag it, investigate the harness/power profile, do NOT read the disposition until reconciled. The disposition is read on the (expected-invariant) count; I am not building a cohort-dependent tree on noise <0.1 KPM.

## The allocation hypothesis → predicted KPM gradient (BOUND IN ADVANCE)

The boss disposition isolated STR's failure as melee target-allocation: it deals real damage (~1,300 DPS) but spreads it across adds instead of focusing the single kill-target. Applied to clear rooms (all-mobs-killed win condition → every mob must die), the same mechanism predicts a **descending pass-likelihood gradient**:

> open_arena (cleave shines) ≥ chokepoint_corridor (funneled swarm) > magic_pack (tougher pack) > elite_pack (bimodal anchors — allocation recurs: spread damage lets each elite linger, clear time balloons, KPM craters)

If STR's pass-pattern follows this gradient, the allocation thesis is corroborated at the clear-room layer. The gradient is the predictive backbone of every row below.

## The pre-registered disposition table

**COUNT first (ships or not), then PATTERN (what STR IS / why it failed):**

| Run result for STR | What it MEANS | Spine §5 disposition |
|---|---|---|
| **≥9/14, passes SPREAD across both groups** (passes most swarm AND most anchored) | Allocation problem is **BOSS-SPECIFIC** — only the single enrage-gated kill-target defeats it; STR clears anchored packs fine. The D2 Barbarian who clears all content but isn't the Uber-soloer. | **route-via-floor CONFIRMED.** Ship STR as broadly clear-competent; the solo enrage-boss is the ONE intended gap (class texture, not defect). Cleanest ship. |
| **≥9/14, passes CONCENTRATED in the 7 no-anchor shells** (clears swarm + just enough anchored to reach 9; fails most magic/elite) | Allocation **RECURS on any anchored target**, but STR clears enough undifferentiated swarm to clear the floor. The D2 Whirlwind Barb — swarm-melter, struggles the moment a priority target exists. | **route-via-floor CONFIRMED, with a NAMED build-identity constraint.** STR ships as the swarm-clear specialist. Load-bearing for roster/content balance: STR needs swarm content to be viable AND other archetypes must cover anchored/boss content. Document the swarm-specialist identity as intended, not a bug. |
| **<9/14, failures CONCENTRATED in anchored group** (passes swarm, fails magic+elite predominantly) | Allocation thesis **CONFIRMED and pervasive** — STR can't even clear-room past anchored packs. | **route-via-floor FAILS.** Kit fix is LOAD-BEARING — STR needs a target-priority mechanic, a single-target option, or a design that makes adds-vs-anchor allocation not matter. The clear-specialist identity is not reachable without kit work. |
| **<9/14, failures ALSO on no-anchor swarm (below-floor on open_arena/chokepoint)** | **FALSIFIER.** Allocation thesis is WRONG — pure swarm has no priority target to mis-allocate against, so a below-floor result there means STR has a raw throughput / clear-DELIVERY deficiency even against undifferentiated targets. | **Re-opens the "is STR's spatial damage delivery broken?" question** the ~1,300-DPS boss measurement seemed to close. Points structural (melee reach / attack cadence / target-acquisition). The disposition is NOT "ship as specialist" — it is "diagnose the delivery deficiency." See falsifier note below. |

## Failure-SIDE ruling — below-floor and above-ceiling mean OPPOSITE things (bound in advance)

The ≥9 count treats below-floor and above-ceiling identically (both = not in-band = not passed). The DESIGN meaning is opposite, and I bind the distinction NOW so the naive count cannot mislead me:

- **Below-floor on swarm** (open/choke KPM under 9.90/11.65) = STR too SLOW on undifferentiated packs = the FALSIFIER signal (raw deficiency, not allocation).
- **Above-ceiling on swarm** (KPM over 15.53/15.88) = STR too FAST = swarm-melter identity CONFIRMED (over-performs on undifferentiated packs — exactly the cleaver fantasy). This does NOT count toward ≥9, but it is the opposite of incompetence.
- **Edge case bound:** if STR misses ≥9 *because* of above-ceiling swarm clips (not below-floor slogs) combined with anchored below-floor, the "floor failure" is a BAND-FIT artifact, not a competence failure. Disposition: the parked question "is the swarm ceiling wrongly clipping legitimate melee-cleaver fantasy?" goes LIVE — revisit the open_arena/chokepoint ceiling, do NOT declare STR incompetent. (The purest swarm-melter signature is exactly this: above-ceiling on undifferentiated + below-floor on anchored.)

## Consistency rails (quarantine the run if these break)

1. **Boss re-run reproduces 0.000.** The free re-run of the 4 boss shells must reconfirm STR survive+kill = 0.000. If STR suddenly survives+kills bosses, the harness has drifted regime — quarantine the whole run until reconciled (mirror of the boss pre-reg's caster control).
2. **dex/int/wis controls clear competently.** dex (0.786 boss surv+kill) and casters (0.992/0.984) should pass clear rooms broadly. If a known-competent control craters on clears, the harness is suspect, not STR.
3. **Cohort agreement within ~1 encounter** (above). Divergence = investigate before reading.
4. **V1 (tier_2 actually ran on all 18).** No defaulted-0.0 KPM masquerading as a measured miss — the boss-run trap generalized. Read the math note; do not assert.

## Falsifier note (honesty check)

The cleanest way I am WRONG: STR comes back **below-floor on open_arena** (the top of the gradient, the shell where cleave should most shine). That single result breaks the allocation thesis — there is no priority target to mis-allocate against in an undifferentiated swarm, so slowness there is a raw delivery problem. I commit to reading that as a falsification of my own thesis and re-opening the spatial-damage-delivery question, NOT as STR "just needing more swarm content." A model-BREAKER (not a clean falsifier) is an INVERTED gradient — STR passes elite_pack but fails open_arena — which means my mechanism is simply wrong and the whole read must be rebuilt from the data.

## What this run does NOT settle (do not overclaim)

- **DPS** (Matt #8) — measured-only, never gated; this run is clear-room KPM band-fit, not a DPS verdict.
- **The boss disposition** — already settled; STR auto-fails 4 boss is the premise.
- **Swarm-ceiling calibration for melee cleavers** — PARKED unless the above-ceiling-swarm edge case fires.
- **The DoT-inert / DoT-scaling-int-wis-only design-debt items** — separate findings, untouched here.
- **dex/int/wis dispositions** — CONTROLS for the harness, not subjects; their clear competence is corroboration only.

---

**Signed:** gandalf, 2026-06-19 — the read, fixed before the data, so the data rules me and not the reverse. The third holding of this discipline in one session; STR's disposition will be ruled on the pre-registered table, not on whatever the headline tempts.

---

## RESOLUTION — the data landed (to fill after gamora run + jack-ryan Gate-2 PASS)

*(Stub. On return: map STR's per-cohort, per-clear-type pass-count to exactly one row of the disposition table; confirm the four consistency rails; record whether the predicted KPM gradient held; note any place the result exceeded the pre-reg as a strengthening, not a reinterpretation. Then fold into spine §5 STR-disposition. Do not read numbers as data until Gate-2 PASS.)*
