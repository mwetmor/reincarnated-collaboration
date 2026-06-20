# Dispatch — 2026-06-19 — gamora — STR 9-pass-floor all-18 clear-room measurement harness

**From:** knight-rider
**To:** gamora (simulation seam)
**Approved by:** Matt 2026-06-19 ("agreed, route it" — gandalf routing handoff, settling STR's combat-efficacy disposition)
**Estimated effort:** multi-hour (math-note-first → EXTEND the existing boss harness from 2 boss shells to all 18 reference-gauntlet shells → smoke → full tier_2 run across 18 shells × 4 cohorts × full season-001 faithful-power population → aggregate with band-fit classification + two-lens pass tally → emit). Pattern B (own session memory).
**Acceptance:** clean single-regime JSON + gandalf-consumable summary table whose **headline is STR's clear-room pass count of 14, per cohort + per clear-type** (open_arena / chokepoint_corridor / magic_pack / elite_pack), each cell classified below-floor / in-band / above-ceiling; plus the free boss-shell re-run reconfirming the 4 auto-fails. V1–V6 confirmed in the math note BEFORE any number is read as data (V1 especially). jack-ryan Gate-2 PASS on harness correctness.

---

## Context (why this run exists — read the brief, this is the short version)

The combat-efficacy measurement layer adopted a **win-condition split doctrine** (Matt 2026-06-19): clear rooms judge on a cohort-relative KPM band (floor+ceiling); boss rooms judge on binary survive-and-kill within the 240s enrage, with DPS measured but never gating. Two runs already landed and passed jack-ryan Gate-2:

- **The clean boss-numbers run** (commit `2f9c5c8`, harness `clean_boss_numbers_harness_2026_06_19.py`): STR fails ALL 4 boss encounters by **timeout** (survive+kill 0.000, a_dead 0.000 — it SURVIVES, it can't KILL in time).
- **The DPS instrumentation** (engine `26a6f27`, tag `gamora/v-dps-instrument-1`): STR deals ~1,300 DPS (~314k total — would kill the boss 1.1–1.36× over IF focused) but sinks 73–96% of it into the ADDS. Diagnosis: a **melee target-allocation failure**, NOT degenerate, NOT pure-throughput, NOT out-healed. DEX (same physical→bleed ailment, also inert in the spatial sim) succeeds where STR fails → the differentiator is melee-vs-ranged allocation.

The ship gate is `gauntlet_pass(cohort)` = `eligible_encounters_passed(cohort) >= 9` over **18 encounters = 4 boss + 14 clear** (`gauntlet_sim.py:158` floor `GAUNTLET_ELIGIBLE_PASS_FLOOR_W_ALPHA_6 = 9`). STR auto-fails the 4 boss (timeout, doctrine survive+kill = 0.000). So the ONE remaining empirical question this run settles:

> **Does STR pass ≥ 9 of the 14 clear-room shells?** If yes → ship STR as a clear-room specialist (the solo enrage-boss is the intended gap). If no → a kit fix (target-priority mechanic / single-target option) is load-bearing.

This is a **measurement harness, NOT a gate change.** It drives the existing tier_2 sim directly on ALL 18 shells, bypassing the tier_1 KPM-reject caller-gate, so STR's clear-room KPM is actually MEASURED — never defaulted to 0.0. It MUST NOT modify the production ship gate.

## THE TRAP — do not re-walk it (generalized from the boss run; verified on disk by KR)

The production path short-circuits tier_2 whenever tier_1 routes REJECT. KR confirmed this first-hand at **`gauntlet_sim.py:1019`**: `if t1_routing == TIER_1_REJECT:` sets `enc_result.in_band = False` / `sg_overall = SUBGATE_BLOCK`, then `continue` at `:1029` — **skipping the tier_2 call at `:1032` entirely. `enc_result.tier_2_kpm` is NEVER assigned, so it defaults to 0.0.** A low-DPS archetype's clear shells could tier_1-reject, leaving `tier_2_kpm` **defaulted to 0.0** masquerading as a measured "STR fails all clears" — exactly the way the boss artifact fabricated `survival=0.0`. **This run MUST drive tier_2 on ALL 18 shells unconditionally, bypassing the tier_1 verdict, so STR's clear-room KPM is MEASURED.** Your existing boss harness already does this (it calls `w4g2_tier_2_full_sim(...)` directly at harness `:132`, never executing the caller `continue`) — this dispatch EXTENDS that same bypass from the 2 boss shells to all 18.

> **NOTE — the prior dispatch's cited gate line was corrected at Gate-2 (carry this forward, Discipline #11/#1.2):** the runtime short-circuit is `gauntlet_sim.py:1019` (→ `continue` at `:1029`, skipping the tier_2 call at `:1032`), NOT `t4_sim_cycling.py:1452` (jack-ryan confirmed `:1452` is a fight-COUNT tally expression inside quality-report finalization, not the runtime gate). Cite `gauntlet_sim.py:1019` in your math note.

## The build = EXTEND the existing harness (do NOT rewrite from scratch)

KR has read the existing harness end-to-end. The extension is surgical. **Reuse everything that already passed jack-ryan Gate-2; widen only the shell set and add band-fit classification + the two-lens pass tally.**

**REUSE UNCHANGED (already Gate-2-confirmed on commit `2f9c5c8`):**
- The tier_1-bypass mechanism: direct `w4g2_tier_2_full_sim(...)` call at harness `:132` (never the caller-gate `continue`). This IS the bypass; it works identically for clear shells.
- `build_population()` (harness `:66-93`) — the 66-config season-001 faithful-power population (22 legendary_ids × 3 samples). jack-ryan confirmed V3 faithful power applies by construction (no `apply_max_profile_investment` override; flip #3 default ON). KEEP this population path.
- The **V1 self-consistency assertion** (harness `:158-165`: `b_dead == wins == winner_player` per cell, fail loud, no table emitted on divergence). This stays — it gates the boss-shell re-run. (On clear shells the win condition is `all_mobs_killed`, not `*_killed`; see V4 below — the assertion's boss-semantics apply only to the 4 boss shells.)
- `attr_of(legendary_id)` (harness `:58-64`) — the `_str_/_dex_/_int_/_wis_` token parse.
- `observed_kpm` recording (harness `:216`, proxy-inclusive) and the production `in_band` verdict capture (harness `:221`, recorded-NOT-gated).
- The seed namespace approach (record a base **distinct** from the boss harness's `619000`, Discipline #3).

**WIDEN (the one structural change):**
- `BOSS_SHELLS = ("boss_with_adds", "mini_boss")` (harness `:43`) → drive ALL 18 catalog encounters. Replace the boss-only filter (harness `:103`, `if ... scenario_shell_id in BOSS_SHELLS`) with the full `ENDGAME_ENCOUNTER_CATALOG` (all 18). KR verified the composition first-hand (grep-counted, not asserted): **open_arena ×4, chokepoint_corridor ×3, magic_pack ×3, elite_pack ×4 (= 14 clear) + boss_with_adds ×3, mini_boss ×1 (= 4 boss) = 18.**

**ADD (the genuinely new logic the boss harness did not need):**
- **Band-fit classification per cell.** Look up `ENCOUNTER_COHORT_KPM_BAND[scenario_shell_id][cohort]` (`gauntlet_sim.py:316-322`) and classify each cell's `observed_kpm` as **below-floor** (< lo) / **in-band** (lo ≤ kpm ≤ hi) / **above-ceiling** (> hi). This is the clear-room pass signal. NOT just pass/fail — record the **failure SIDE** (gandalf reads below-floor and above-ceiling as OPPOSITE design meanings; see §What to record). The bands KR confirmed live: open_arena `(9.90, 15.53)`, chokepoint_corridor `(11.65, 15.88)`, magic_pack `(6.06, 11.43)`, elite_pack `(5.65, 10.00)`, boss_with_adds `(2.49, 3.78)`, mini_boss `(0.57, 3.30)` — all **cohort-invariant** (`gauntlet_sim.py:298-302` "Do NOT add per-cohort variation").
- **Per-cohort clear-room pass count (of 14)** = count of clear shells where `observed_kpm` is in-band, per cohort. THE HEADLINE.
- **Two-lens `eligible_encounters_passed` per cohort:** (a) **current-code lens** — KPM-band in-band across all 18; (b) **doctrine lens** — KPM-band in-band on the 14 clear + survive+kill (`b_dead`, the V1-confirmed boss survival_rate) on the 4 boss. Report both; gandalf reads the doctrine lens against the pre-registered table.
- The boss-shell survive+kill re-run is FREE (the 4 boss shells flow through the same loop) — reconfirm STR's 4 auto-fails (survive+kill 0.000, timeout-dominant) as the doctrine-lens denominator in the same artifact.

## Required reading before starting

1. **The run brief (READ FULLY — it is the spec):** `agentic_orchestration/gandalf/requests/2026-06-19-str-9pass-floor-clear-room-run-brief.md`
2. **The pre-registered interpretation (for awareness — gandalf binds his read before your data; you do NOT need to satisfy it, but it tells you exactly what texture gandalf needs intact):** `agentic_orchestration/gandalf/notes/2026-06-19-str-9pass-floor-pre-registered-interpretation.md` — note especially: cohort-agreement-within-~1-encounter is gandalf's pre-committed EXPECTATION (divergence = surprise to flag); the per-clear-type breakdown distinguishes "broad clear-competent" from "swarm-only specialist"; below-floor-on-swarm is gandalf's FALSIFIER signal.
3. The doctrine spine: `agentic_orchestration/gandalf/notes/2026-06-19-encounter-measurement-doctrine-spine.md`
4. **The two prior Gate-2 findings (your own work, blessed — reuse their confirmed anchors, do NOT re-derive):**
   - `agentic_orchestration/qa/findings/2026-06-19-gamora-clean-boss-numbers-harness-gate2.md` (V1 source + the 1,056-cell invariant; the `gauntlet_sim.py:1019` gate correction)
   - `agentic_orchestration/qa/findings/2026-06-19-gamora-dps-instrumentation-gate2.md` (V3/V4/V5 + the `spatial_gauntlet/` subdir path note — INFO-1, fix it this time)
5. The prior dispatch (the harness you are extending): `agentic_orchestration/dispatches/2026-06-19-gamora-clean-boss-numbers-harness.md`
6. Engine anchors (KR has read these; confirm first-hand, do not take on report):
   - `gauntlet_sim.py:1019` — the `if t1_routing == TIER_1_REJECT:` short-circuit (→ `continue` at `:1029`, skipping the tier_2 call at `:1032`). THE TRAP.
   - `gauntlet_sim.py:316-322` — `ENCOUNTER_COHORT_KPM_BAND` (the clear-room bands; cohort-invariant per `:298-302`).
   - `gauntlet_sim.py:158` — `GAUNTLET_ELIGIBLE_PASS_FLOOR_W_ALPHA_6 = 9` (the floor over 18).
   - `generation/endgame_encounter_catalog.py:161` — `ENDGAME_ENCOUNTER_CATALOG` (the 18; `_validate_catalog()` asserts `len == 18` at `:50`). `get_encounters_for_scenario()` at `:1007` if useful.
   - `t4_sim_cycling.py:1199` — `w4g2_tier_2_full_sim` (the instrument; standalone, does NOT require tier_1 to have passed).
   - `clean_boss_numbers_harness_2026_06_19.py` (the harness you extend; the V1 assertion at `:158-165`, the population at `:66-93`, the drive loop at `:505-525`).
7. Engineering disciplines #1 (math-before-code), #2 + #2.1 (smoke-test + resource-scaling rehearsal), #3 (distinct seeds, no parallel regens), #11 (capture decision telemetry / citation correction), #12 (semantic-shift declaration if any), #19.1 (cheapest-refuting-test-per-claim).

## Math-before-code — Discipline #1 (THE GATE; do this FIRST, before any harness code)

Author a math note (`simulation/math/str-9pass-floor-all18-clearroom-harness-2026-06-19.md`) that confirms the SIX verify-gates BEFORE the numbers are trusted. **V1 is load-bearing for the boss-shell re-run; V4 is load-bearing for the clear-shell win-condition; confirm each first-hand and record the line you read it at. Correct the prior path imprecision: cite the `spatial_gauntlet/` subdir (e.g. `simulation/spatial_gauntlet/spatial_engine.py`), not the bare `simulation/` path (DPS-instrument Gate-2 INFO-1).**

- **V1 (tier_2 actually ran on all 18) — LOAD-BEARING, THE TRAP GENERALIZED.** Confirm the harness drove `w4g2_tier_2_full_sim` on EVERY one of the 18 shells (× 4 cohorts × population), with NO defaulted-0.0 KPM masquerading as a measured miss. The harness does this by calling tier_2 directly (harness `:132`), never the caller-gate `continue` at `gauntlet_sim.py:1019`/`:1029`. **ASSERT in the harness:** every cell carries an `observed_kpm` that came from an executed batch (e.g., `batch.n_fights == expected_n` per cell; a cell with `n_fights == 0` or a KPM never set from a batch is a FAIL — fail loud, do NOT emit). Read it, do not assert on faith.
- **V2 (faithful power):** max-profile investment is the current default (flip #3, `apply_max_profile_investment` ON across the 4-site chain, decisions-log 2026-06-18). Confirm the harness drives the default chain without overriding it (jack-ryan confirmed this holds by construction in the boss harness — re-confirm it for the widened run). Faithful, NOT the stripped ablation floor.
- **V3 (proxy-inclusive KPM, Matt #5):** `observed_kpm` = `mobs_killed`/min where `mobs_killed = sum(1 for m in self.mobs if not m.is_alive)` (`spatial_gauntlet/spatial_engine.py:1740`) — attribution-agnostic by construction (proxy/summon/DoT kills count regardless of final-blow source). STR is melee/solo → proxy term ≈ 0, but confirm the RULE holds (it does, by construction).
- **V4 (clear-shell win condition) — LOAD-BEARING for the 14 clear shells.** The 14 clear encounters resolve on `all_mobs_killed` (clear the pack) and KPM = `mobs_killed`/min on the pack-clear — NOT a boss shell mislabeled. Confirm the clear shells' win condition + that `observed_kpm` is the pack-clear rate. **Note the V1 self-consistency assertion (boss-semantics: `b_dead == wins == winner_player`) applies to the 4 BOSS shells; for the 14 clear shells the analogous integrity check is `Σ termination_counts == n_fights` + `observed_kpm` populated from an executed batch.** Keep the boss assertion scoped to boss shells; add the clear-shell integrity check.
- **V5 (single regime):** current spatial sim only (`run_spatial_fight` / `w4g2_tier_2_full_sim`), current mobs/min, faithful power. NO old-scale KPM mixed in (the regime-mix that made phase3 useless — old-scale rows + current metadata, 8× `in_band` disagreement). Fingerprint the regime in the output metadata.
- **V6 (measurement-only):** production ship gate untouched — NO edits to `gauntlet_sim.py`, `ENCOUNTER_COHORT_KPM_BAND`, the tier_1 routing, `gauntlet_pass`/`eligible_encounters_passed`, or any persisted telemetry schema. This is a read-only diagnostic of the existing tier_2. The harness writes only its own diagnostic JSON/TXT to the cycle-14 season-001 folder. (jack-ryan confirms no gate regression at Gate-2.)

## Cross-seam contract change? (Principle 6 gate — KR completes this at authoring time)

Does this dispatch add/modify/rename/remove any field on a telemetry schema table, fight_log dict key, loadout dict key, export packet, or inter-seam fixture?

**NO — Round-trip: not applicable.** This is a read-only diagnostic harness extension. It DRIVES the existing `w4g2_tier_2_full_sim`, READS existing `StratumFightBatch` fields + the existing `ENCOUNTER_COHORT_KPM_BAND` constant, and writes a standalone diagnostic JSON to the cycle-14 season-001 folder. It does NOT touch any cross-seam schema, the production ship gate, `gauntlet_sim.py` (read-only), the bands, the tier_1 routing, or any persisted telemetry table. No MIGRATION.md required (note this explicitly). jack-ryan confirms no gate regression at Gate-2 (V6).

## Scope
- [ ] Math note FIRST (`simulation/math/str-9pass-floor-all18-clearroom-harness-2026-06-19.md`) — V1–V6 confirmed with line citations (use `spatial_gauntlet/` subdir paths); V1 + V4 integrity assertions specified; band-fit classification rule documented (below-floor / in-band / above-ceiling vs `ENCOUNTER_COHORT_KPM_BAND`); two-lens `eligible_encounters_passed` definitions documented; seed base recorded (distinct from the boss harness's `619000`, Disc #3); cite `gauntlet_sim.py:1019` (not `t4_sim_cycling.py:1452`) for the gate.
- [ ] EXTEND the existing harness (measurement-only; does NOT modify production gate code): widen the shell set from `BOSS_SHELLS` to all 18 `ENDGAME_ENCOUNTER_CATALOG` encounters, driving `w4g2_tier_2_full_sim(...)` per kit × {all 18 shells} × {all 4 cohorts} at full tier_2 `n_fights`, BYPASSING the tier_1 KPM-reject caller-gate (reuse the direct-call mechanism at harness `:132`).
- [ ] Per kit × shell × cohort, record: `observed_kpm` (proxy-inclusive), the cohort band `[lo, hi]`, the band-fit classification (**below-floor / in-band / above-ceiling**), the enc_type tag + clear-vs-boss flag, and (boss shells only) the survive+kill + termination split (`a_dead`/`b_dead`/`timeout`, the V1-confirmed boss result).
- [ ] V1 integrity ASSERTED in harness (every cell's KPM came from an executed batch — `batch.n_fights == expected_n`; fail loud on any defaulted/empty cell). V4 clear-shell integrity ASSERTED (`Σ termination_counts == n_fights`). Boss-shell V1 self-consistency (`b_dead == wins == winner_player`) RETAINED for the 4 boss shells.
- [ ] Aggregate by attribute (int/wis/dex/str, parsed from `legendary_id`) AND **the headline: STR clear-room pass count of 14, per cohort + per clear-type** (open_arena / chokepoint_corridor / magic_pack / elite_pack), with the failure-SIDE breakdown per clear-type. Plus two-lens `eligible_encounters_passed` per cohort (current-code 18-wide vs doctrine 14-clear+4-boss).
- [ ] Single-regime fingerprint verified + recorded in output metadata: current `run_spatial_fight` + current mobs/min + faithful power; NO old-scale KPM mixed in (V5).
- [ ] n per attribute cell ≥ the boss-harness cell sizes (the boss run drove all 4 cohorts unconditionally → str/dex/int n≈3,840, wis n≈9,600 per attribute across shells; per-cell n_fights = 20). Confirm not underpowered (brief endorse-criterion 5: n per cell ≥ boss-harness cell sizes).
- [ ] Smoke-test pass (Disc #2): a tiny n_fights dry-run on ONE kit × a HANDFUL of representative shells (at minimum one of EACH clear type: open_arena / chokepoint_corridor / magic_pack / elite_pack, + one boss) × ONE cohort confirming the path runs end-to-end, **tier_2 actually fires on the CLEAR shells** (the whole point — the trap is a clear shell defaulting to 0.0), the band-fit classification populates, and the clear-shell integrity check passes — BEFORE the full run. Include resource-scaling sanity (Disc #2.1): peak memory of the full 18×4×66 run is bounded vs host RAM (the run is 9× the boss run's shell breadth — 18 shells vs 2 — so project the scaling explicitly).
- [ ] Clean JSON output + gandalf-consumable summary table written to `agentic_orchestration/cycle-14-wave-5-season-001/` (suggested: `str-9pass-floor-all18-clearroom-2026-06-19.json` + `.txt`).
- [ ] MIGRATION.md: not applicable (no cross-seam contract change; note this explicitly).
- [ ] Round-trip smoke: not applicable — no cross-seam contract change (read-only diagnostic).
- [ ] Fix the DPS-instrument Gate-2 INFO-1 carryover: cite `spatial_gauntlet/` subdir paths in the math note (not bare `simulation/`).
- [ ] AGENT_STATE.md updated at session end.
- [ ] AUTO-COMMIT harness + math note + output per team commit discipline (in-scope cycle work). DO NOT PUSH — leave the stack clean on disk; record the unpushed commit list in the completion record.

## Acceptance criteria
- [ ] V1–V6 all confirmed in the math note WITH line citations (subdir-correct), BEFORE the table is read as data. V1 (tier_2 ran on all 18, no defaulted zeros) + V4 (clear-shell win condition) especially.
- [ ] **If V1 fails (any clear-shell cell carries a KPM that did NOT come from an executed tier_2 batch — a defaulted 0.0): STOP, do not emit the table, report the failure.** That is the exact failure mode this run exists to avoid.
- [ ] tier_2 demonstrably RUNS on the CLEAR shells in the smoke-test (the trap is a clear shell short-circuiting to 0.0; the smoke must show tier_2 firing on at least one of each clear type).
- [ ] tier_1 bypass is measurement-only — production ship gate (`gauntlet_sim.py`, `ENCOUNTER_COHORT_KPM_BAND`, `gauntlet_pass`/`eligible_encounters_passed`, tier_1 routing) untouched (V6).
- [ ] Band-fit classification recorded per cell with the failure SIDE (below-floor vs in-band vs above-ceiling) — the single most valuable new column for gandalf (he reads below-floor and above-ceiling as opposite design meanings).
- [ ] THE HEADLINE answerable: STR's clear-room pass count of 14, per cohort + per clear-type, distinguishing "passes spread across both groups" (broad clear-competent) from "passes concentrated in no-anchor swarm" (swarm-only specialist) from "<9 with failures concentrated in anchored" (allocation pervasive) from "<9 with failures on no-anchor swarm" (gandalf's FALSIFIER).
- [ ] Cohort agreement legible (gandalf pre-commits cohorts agree within ~1 encounter, given cohort-invariant bands; if cohorts DIVERGE by >1 encounter, FLAG it prominently — that is a surprise, not a disposition input).
- [ ] Free boss-shell re-run reconfirms STR's 4 auto-fails (survive+kill 0.000, timeout-dominant) — consistency rail.
- [ ] faithful power (max-profile investment) applied (V2); proxy-inclusive KPM confirmed (V3); single regime (V5).
- [ ] n per attribute cell ≥ boss-harness cell sizes.
- [ ] Round-trip smoke: not applicable — read-only diagnostic, no cross-seam contract change.

## Out of scope (explicit non-goals)
- **DO NOT modify the production ship gate** — no edits to `gauntlet_sim.py`, `ENCOUNTER_COHORT_KPM_BAND`, the tier_1 routing, `gauntlet_pass`/`eligible_encounters_passed`, or any persisted telemetry schema. This is read-only measurement (V6).
- **DO NOT implement the doctrine** (don't wire survive+kill or band-fit as a NEW gate, don't change the floor, don't remove any ceiling). This run MEASURES; gandalf RULES on the data; a later dispatch IMPLEMENTS if needed.
- **DO NOT re-fit or re-tune the KPM bands** — read `ENCOUNTER_COHORT_KPM_BAND` as-is. (The swarm-ceiling-for-melee-cleavers question is PARKED on gandalf's side unless his above-ceiling-swarm edge case fires; you measure, you don't re-band.)
- **DO NOT re-fit or re-tune kits** — measure the season-001 faithful-power population as-is (the same `build_population()` the boss harness used).
- **DO NOT rewrite the harness from scratch** — EXTEND the existing `clean_boss_numbers_harness_2026_06_19.py` (or a clearly-derived sibling that imports its reusable pieces). Reuse the Gate-2-blessed bypass, population, and V1 assertion.
- **DO NOT measure DPS as a verdict** — DPS is measured-never-gated (already instrumented; this run is clear-room KPM band-fit, not a DPS verdict). You may surface DPS as sanity telemetry but it is NOT the headline.
- **DO NOT push to remote.**

## Open questions for the agent to resolve (document the decision in the math note)
- **Extend-in-place vs derived sibling.** Decide whether to widen `BOSS_SHELLS` in the existing harness (and gate boss-only logic behind a shell-type check) OR author a clearly-derived sibling (`str_9pass_floor_all18_harness_2026_06_19.py`) that imports `build_population` / `attr_of` / `run_one_cell` / the V1 assertion from the boss harness. Either is fine — state which and why. The constraint: the bypass + population + V1 assertion must be the SAME Gate-2-blessed code, not re-derived.
- **Band-fit edge handling.** Define the in-band predicate at the boundaries explicitly (lo ≤ kpm ≤ hi, inclusive both ends — match the production `_route_tier_1` direct-range-check semantics; confirm the production predicate's inclusivity at `gauntlet_sim.py` and mirror it so your band-fit lens matches the live gate's). Document it.
- **Above-ceiling on clear shells = NOT in-band but NOT incompetence.** gandalf reads above-ceiling-on-swarm as the cleaver-fantasy CONFIRMED (too fast), opposite of below-floor (too slow). Make sure the classification records the SIDE so a pass-count of "X in-band" is not silently conflated with "14 − X incompetent." Report in-band / below-floor / above-ceiling as three distinct counts per clear-type.
- **TTK / termination on clear shells.** Clear shells end on `all_mobs_killed`; capture the clear-time distribution if cheap (informs whether a below-floor result is a slow-slog vs a near-miss), but it is secondary to the band-fit headline. Decide and document.

## Hand-back (what KR needs to return to gandalf)
On completion, append a completion record with:
- **THE HEADLINE:** STR's clear-room pass count of 14, **per cohort** AND **per clear-type** (open_arena / chokepoint_corridor / magic_pack / elite_pack), each with the in-band / below-floor / above-ceiling split. This is the single fact gandalf maps to his pre-registered disposition table.
- The two-lens `eligible_encounters_passed` per cohort (current-code 18-wide vs doctrine 14-clear + 4-boss survive+kill).
- The free boss-shell re-run result (STR survive+kill 0.000 / timeout-dominant reconfirmed — the consistency rail).
- The dex/int/wis CONTROL clear-room pass counts (corroboration that known-competent archetypes clear broadly — if a control craters, the harness is suspect, not STR).
- Cohort-agreement read: do STR's per-cohort pass counts agree within ~1 encounter (expected, given cohort-invariant bands)? FLAG any >1-encounter divergence prominently.
- V1–V6 verify status (each PASS/FAIL with the line cited).
- The output artifact path + the unpushed commit list (harness/extension + math note + output).
- Any surprise vs the pre-registered expectation. Flag anything that changes the disposition read.

## References
- Run brief: `agentic_orchestration/gandalf/requests/2026-06-19-str-9pass-floor-clear-room-run-brief.md`
- Pre-registered interpretation: `agentic_orchestration/gandalf/notes/2026-06-19-str-9pass-floor-pre-registered-interpretation.md`
- Doctrine spine: `agentic_orchestration/gandalf/notes/2026-06-19-encounter-measurement-doctrine-spine.md`
- Prior boss harness (EXTEND this): `~/Games/reincarnated-engine/src/reincarnated/simulation/clean_boss_numbers_harness_2026_06_19.py`
- Prior boss dispatch: `agentic_orchestration/dispatches/2026-06-19-gamora-clean-boss-numbers-harness.md`
- Prior Gate-2 findings (reuse confirmed anchors): `agentic_orchestration/qa/findings/2026-06-19-gamora-clean-boss-numbers-harness-gate2.md` + `2026-06-19-gamora-dps-instrumentation-gate2.md`
- THE TRAP (verified): `gauntlet_sim.py:1019` (`if t1_routing == TIER_1_REJECT:` → `continue` at `:1029`, skipping tier_2 call at `:1032`)
- Clear-room bands: `gauntlet_sim.py:316-322` (`ENCOUNTER_COHORT_KPM_BAND`, cohort-invariant per `:298-302`); floor `:158` (`= 9`)
- The 18-catalog: `generation/endgame_encounter_catalog.py:161` (`ENDGAME_ENCOUNTER_CATALOG`; `len==18` asserted `:50`) — KR-verified composition: open_arena ×4, chokepoint ×3, magic_pack ×3, elite_pack ×4, boss_with_adds ×3, mini_boss ×1
- Instrument: `t4_sim_cycling.py:1199` (`w4g2_tier_2_full_sim`); proxy-inclusive KPM `spatial_gauntlet/spatial_engine.py:1740`
- Faithful-power default: decisions-log 2026-06-18 (flip #3, `apply_max_profile_investment` ON, 4-site chain)
