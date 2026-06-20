# Boss-gate implementation spec — §6 of the encounter-measurement doctrine, now build-ratified

**Type:** gandalf-authored implementation spec → **knight-rider sequences** (gamora implements + runs; jack-ryan Gate-2 with BLOCK authority; gandalf design-fit on disposition).
**Author:** gandalf
**Date:** 2026-06-20
**Composes with / read IN FULL first:**
- `gandalf/notes/2026-06-19-encounter-measurement-doctrine-spine.md` §1 (win-condition split, Matt-ADOPTED), §5 (clean-boss numbers), §5a (STR-via-floor ruling), **§6 (the boss-gate, AGREED — this spec builds it)**, and the **GATE-1 VERIFICATION ADDENDUM** (the first-hand code trace — touch points below come from it).
- `gandalf/notes/2026-06-20-composed-rebaseline-three-fork-ruling.md` (the STOP that ratified building §6 now).
- `gandalf/requests/2026-06-20-instrument-validity-workstream-KR-brief.md` (parent workstream; measure-isolated + one-refit disciplines).

---

## 0. Why this exists (one paragraph)
The win-condition doctrine is Matt-ADOPTED (§1): clear rooms gate on a KPM band (floor + ceiling); **boss rooms gate on survive-and-kill within the 240s enrage timer, with DPS/TTK MEASURED but never gating and NO over-performance ceiling.** §6 established — by first-hand code trace — that this central move is **UNBUILT**: boss shells are KPM-gated *right now* by a narrow per-boss band, and the survival signal (sg2) is computed but wired to gate **nothing**. The composed re-baseline STOP (the three-fork ruling) ratified building §6 now: the boss rows' 72×/cratered KPM spread is not a band problem to solve — it is the band being applied where the doctrine says it must not be. This spec wires the boss-gate so boss shells **leave the KPM band entirely.** This is the **boss-shell half of the workstream's single tail-refit** (the clear-shell half is deferred behind the magnitude pass).

## 1. The work (recompose-first — REWIRE existing-but-disconnected machinery; invent NOTHING)
The intent already exists in code (oracle comment `gauntlet_sim.py:357` "boss/mini: SURV-judged, KPM a wide sanity rail"); sg2 is already computed; the survival floor already exists. The defect is that they are not wired to gate. Three moves, **all verify-first-hand** (line refs from §6/GATE-1 addendum; may have drifted):
- **(a) Stop KPM-REJECTing boss shells at tier_1.** Boss rooms (`boss_with_adds`, `mini_boss`) must route to tier_2 unconditionally (or on a wide sanity rail) so survive+kill is actually simulated. Today a tier_1 REJECT short-circuits tier_2 (`gauntlet_sim.py:1019`), which is what manufactures the fake STR boss-crater (it refuses to test the thing that would clear or condemn it).
- **(b) Make the boss-shell ship gate read sg2 (survive within 240s + target killed), NOT the narrow KPM band.** Today `eligible_encounters_passed` counts `tier_2_kpm` inside `ENCOUNTER_COHORT_KPM_BAND[boss_with_adds]=(2.49,3.78)` / `[mini_boss]=(0.57,3.30)` (`gauntlet_sim.py:582-592,636`); sg2 is excluded from `in_band`/`gauntlet_pass` (`:1069` comment "Only sg1… is enriched"; `:1080-1081` counter; `t4_sim_cycling.py:811-815` `SURVIVAL_FLOOR_BY_COHORT`). Wire sg2 as the **gate** for boss shells.
- **(c) DPS/TTK becomes recorded telemetry on boss shells (measure-only, never gates).** The DPS instrument from the Matt #8 build already exists and drove the §5 clean-boss run — **verify it records on this path; wire only if absent.** If the field crosses the simulation→telemetry seam, coordinate with star-lord + write `MIGRATION.md` (Principle 6 / ADR-004).

## 2. Math-before-code (Discipline #1 — REQUIRED FIRST)
Author a math-note BEFORE the change stating the **expected boss-shell pass-population shift**: how many kits flip from KPM-rejected → survive-and-kill pass/fail, and the expected disposition by attribute (casters pass ~0.99 per §5; STR fails timeout=1.000 per §5/§5a). The note makes the gate change falsifiable against the already-measured clean-boss table.

## 3. CRITICAL — this is the FIRST production-gate change in the workstream
Phases 1–4 + R were measure-ISOLATED (bands + production gate untouched). **This changes `eligible_encounters_passed` for boss shells** — what actually ships. Therefore:
- **jack-ryan structural Gate-2 with BLOCK authority** (mechanism correctness, V-gates, seed hygiene, no *clear-shell* gate regression).
- **Semantic-shift declaration (Discipline #12):** the meaning of "passed" changes for boss shells (KPM-in-band → survive-and-kill). Declare it across the boundary.
- **Decisions-log entry:** this implements the §1/§6-AGREED doctrine decision (Matt 2026-06-19). KR drafts / jack-ryan reviews. The implementation is authorized by the prior adoption; the *resulting* boss-shell disposition lands at a Matt approval halt (§6 below).
- **EXPECTED, already-ruled outcome — do NOT "fix" it:** under the wired gate, **STR fails boss shells (timeout=1.000).** This is the §5a-RULED texture (STR ships via the clear-room floor *without* boss shells). It is the instrument now *measuring* STR's boss failure instead of refusing to test it — it is the input to Phase 6's lever read, NOT a regression and NOT a Gate-2 BLOCK.

## 4. Scope boundaries (hard)
- **Boss shells ONLY** (`boss_with_adds`, `mini_boss`). The **clear-shell KPM gate is UNTOUCHED** (open_arena, chokepoint, magic_pack, elite_pack stay on their KPM band).
- **NO magnitude work** (no SPATIAL_DAMAGE_SCALE / mob-HP). The boss rows are long single-target grinds — the 600@0.3s timing-floor artifact never touches them, so zero magnitude is needed to resolve them.
- **NO clear-room re-band** (deferred behind the scheduled magnitude pass; empirical gate: caster sub-second cells calibrated).
- **NO anchor-predicate work** (that is the separate Phase-6-internal gamora item per the G3b ruling §2.4).
- The **240s hard cap IS the enrage timer** — do not invent a new timer; use the existing cap.

## 5. Measure / verify (first-hand, affirmative)
- Boss shells route to tier_2 with no KPM-reject; sg2 gates; DPS/TTK recorded.
- The §5 clean-boss survive+kill table reproduces under the *wired* gate (int ≈0.992, wis ≈0.984, dex ≈0.786, **str 0.000 timeout 1.000**) — i.e. the gate change does not alter the underlying fight outcomes, only what gates on them.
- **Discipline #3:** if a verification run is needed, fresh disjoint seed base (consult the workstream's used bases; population seed_base=14001, Phase-5 fight_seed_base=40000000 are taken).

## 6. Hand-back chain
1. gamora: math-note → recompose-first rewire (a/b/c) → boss-shell verification (affirmative, by-attribute) → semantic-shift declaration. → **jack-ryan structural Gate-2 (BLOCK authority — production-gate change).**
2. KR drafts the decisions-log entry (implements §1/§6 doctrine); jack-ryan reviews.
3. **Matt approval halt:** the boss-shell gate disposition (survive-and-kill replaces the boss KPM band) — this is the **boss-half of the Phase-5 band-approval halt.** Clear-half stays deferred.
4. On Matt approval → **Phase 6 Read-1 unblocks** (STR encounter-segregated read — honest with the lever as it fires today). Read-2 (mixed-pack focus-fire — the definitive (A)-vs-(B) read) follows gamora's anchor-predicate rescale per the G3b ruling §2.4.

## Out of scope
Clear-room re-band (magnitude-gated). Anchor-predicate rescale (Phase-6-internal). Any magnitude re-tune. Any clear-shell gate change. Phases 1–4 + R (landed).

---
**Signed:** gandalf, 2026-06-20. Wire the gate the doctrine already ruled and the code already named — un-reject the boss, let survive-and-kill judge it, record DPS/TTK and never let it gate. Boss shells leave the band; the band stops lying on the rows it never fit.
