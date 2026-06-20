# Dispatch — 2026-06-19 — gamora — clean boss numbers measurement harness

**From:** knight-rider
**To:** gamora (simulation seam)
**Approved by:** Matt 2026-06-19 ("let's run real boss numbers" — live gandalf Pattern-B measurement-doctrine session)
**Estimated effort:** multi-hour (math-note-first → harness build → full tier_2 run across 2 shells × 4 cohorts × full season-001 faithful-power population → aggregate → emit). Pattern B (own session memory).
**Acceptance:** clean single-regime JSON + gandalf-consumable summary table (survive+kill rate + termination breakdown + TTK + KPM, by attribute and archetype), with V1–V4 confirmed in the math note BEFORE the table is read as data. jack-ryan Gate-2 PASS on harness correctness.

---

## Context (why this run exists — read the brief, this is the short version)

gandalf is re-architecting the battle-sim's combat-efficacy MEASUREMENT layer. A Gate-1 code trace overturned three claims and surfaced the blocker that makes the existing data unusable for boss claims: **boss shells are tier_1-KPM-REJECTED, and a REJECT short-circuits tier_2 (`t4_sim_cycling.py:1452`). So the survive+kill simulation NEVER RUNS on boss shells.** The "STR boss-crater" (`survival=0.0`) in `phase3_gauntlet_results.json` is a tier_2-never-ran DEFAULT, not a measured death. The artifact is also REGIME-MIXED (old-scale KPM rows + current mobs/min metadata; row `in_band` 427 vs metadata 3285, 8× disagreement).

The design session needs clean boss numbers to settle ONE empirical question: **at faithful power, on boss shells, which archetypes actually survive-and-kill the boss within the enrage timer — and is the STR boss-crater real, or an artifact of the KPM gate rejecting STR before survive+kill is ever measured?**

This is a **measurement harness, NOT a gate change.** It drives the existing tier_2 sim directly on boss shells, bypassing the tier_1 KPM-reject caller-gate, so survive+kill is actually observed. It MUST NOT modify the production ship gate.

## Required reading before starting

1. **The run brief (READ FULLY — it is the spec):** `agentic_orchestration/gandalf/requests/2026-06-19-kr-clean-boss-numbers-run-prompt.md`
2. The Gate-1 addendum + corrected §5/§6 it depends on: `agentic_orchestration/gandalf/notes/2026-06-19-encounter-measurement-doctrine-spine.md`
3. Engine anchors (KR has already read these — confirm first-hand, do not take on report):
   - `t4_sim_cycling.py:1199` — `w4g2_tier_2_full_sim` (the instrument; standalone, does NOT require tier_1 to have passed)
   - `t4_sim_cycling.py:1452` — the `tier_1_outcome != TIER_1_REJECT` short-circuit (the caller-gate the harness bypasses)
   - `t4_sim_cycling.py:1073-1099` — `_run_spatial_w4g_batch` winner→termination mapping (`_term_for = {"player":"b_dead","monster":"a_dead","timeout":"timeout"}`; `kills = fr.mobs_killed`)
   - `t4_sim_cycling.py:225-260` — `StratumFightBatch` properties (`survival_rate = wins/n_fights`; `wins = sum(f.player_won)`; `observed_kpm`)
   - `spatial_engine.py:1742-1771` — winner resolution for `boss_killed` / `mini_boss_killed`
   - `arena.py:472-523` (`SCENARIO_BOSS_WITH_ADDS`) + `arena.py:~755-771` (`SCENARIO_MINI_BOSS`)
4. Engineering disciplines #1 (math-before-code), #2 (smoke-test), #3 (distinct seeds, no parallel regens), #12 (semantic-shift declaration), #19.1 (cheapest-refuting-test-per-claim)

## Math-before-code — Discipline #1 (THE GATE; do this FIRST, before any harness code)

Author a math note (`simulation/math/clean-boss-numbers-harness-2026-06-19.md`) that confirms the FOUR verify-gates BEFORE the numbers are trusted. **KR has pre-traced these from code to de-risk you; confirm each first-hand and record the line you read it at. V1 is load-bearing — if it fails, survival_rate ≠ survive+kill and the whole table is invalid: STOP and report, do not hand back a table built on a false signal.**

- **V1 (winner = survive AND kill) — LOAD-BEARING.** Confirm `run_spatial_fight` resolves `fr.winner=="player"` ONLY when (a) the boss/mini-boss entity is DEAD **and** (b) the player is ALIVE — a player death before the boss dies must yield `winner!="player"`.
  - KR pre-trace (confirm, don't assume): `spatial_engine.py:1742-1753` (`boss_killed`) and `:1755-1771` (`mini_boss_killed`) both check `if not self.player.is_alive:` FIRST → `winner="monster"`; `winner="player"` is reached ONLY in the `elif ... not boss_alive` branch, which by control-flow requires the player-alive check above to have passed. So `winner=="player"` ⇒ boss dead AND player alive, by construction across both branches.
  - **THEN confirm the chain holds end-to-end to `survival_rate`:** `survival_rate = wins/n_fights` (`:230-233`), `wins = sum(f.player_won)` (`:226-227`), `player_won = (fr.winner=="player")` (`:1078`). Therefore on boss shells `survival_rate` IS the survive+kill rate. **Assert this self-consistency in the harness:** the `b_dead` termination count MUST equal `wins` MUST equal the `winner=="player"` count, per cell. If they ever diverge, the harness is wrong — fail loud.
- **V2 (enrage cap):** report the ACTUAL hard time-cap per boss shell from the `ArenaScenario`, NOT the stale `120s` docstring at `t4_sim_cycling.py:252` (that comment is on the generic `fights_resolving_under_max` property, unrelated to the boss cap).
  - KR pre-trace (confirm): `boss_with_adds` `max_duration_s=240.0` (`arena.py:522`); `mini_boss` `max_duration_s=240.0` hard + `soft_timeout_s=150.0` (`arena.py` mini-boss block). The 240s hard cap IS the doctrine's enrage timer; `timeout` terminations = "didn't kill before enrage."
- **V3 (faithful power):** confirm the run executes at max-profile investment (current default post flip-#3 `apply_max_profile_investment` ON), NOT the stripped ablation floor. "Real boss numbers" = geared/faithful kits. Document HOW faithful power is applied to the kits you drive (see Open Questions — population provenance).
- **V4 (proxy-inclusive kills, Matt #5):** confirm `fr.mobs_killed` counts a mob killed regardless of final-blow source (player / summon / totem / DoT).
  - KR pre-trace (confirm): `kills = fr.mobs_killed` (`t4_sim_cycling.py:1090`); `mobs_killed` is a dead-mob count (`spatial_engine.py:1740` `sum(1 for m in self.mobs if not m.is_alive)`). Dead-mob count is attribution-agnostic by construction.

**DPS (Matt #8) is SCOPED OUT.** The spatial result drops per-fight damage (`player_damage_dealt=0.0`, `t4_sim_cycling.py:1096-1098`). Do NOT block on it; note it in the hand-back as the Tier-B follow-on (surfacing player + all-proxy damage from `SpatialFightResult` is engine instrumentation, a separate build).

## Cross-seam contract change? (Principle 6 gate — KR completes this at authoring time)

Does this dispatch add/modify/rename/remove any field on a telemetry schema table, fight_log dict key, loadout dict key, export packet, or inter-seam fixture?

**NO — Round-trip: not applicable.** This is a read-only diagnostic harness. It DRIVES the existing `w4g2_tier_2_full_sim` and READS existing `StratumFightBatch`/`SpatialFightResult` fields. It writes a standalone diagnostic JSON to the cycle-14 season-001 folder. It does NOT touch any cross-seam schema, the production ship gate, `gauntlet_sim.py`, `ENCOUNTER_COHORT_KPM_BAND`, or any persisted telemetry table. (jack-ryan confirms no gate regression at Gate-2.)

## Scope
- [ ] Math note FIRST (`simulation/math/clean-boss-numbers-harness-2026-06-19.md`) — V1–V4 confirmed with line citations; V1 self-consistency assertion specified; population-provenance decision documented; seed base recorded (distinct from prior harnesses, Disc #3)
- [ ] Harness (standalone script/module — measurement-only; does NOT modify production gate code): loads the season-001 faithful-power kit population, drives `w4g2_tier_2_full_sim(...)` per kit × {`boss_with_adds`, `mini_boss`} × {all 4 cohorts} at full tier_2 `n_fights`, BYPASSING the tier_1 KPM-reject caller-gate
- [ ] Per kit × shell × cohort, record: `survival_rate` (= survive+kill rate, V1-confirmed), termination breakdown (`a_dead`/`b_dead`/`timeout` counts), TTK (`elapsed_s` / `duration_s` on `winner=="player"`/`b_dead` fights only), proxy-inclusive KPM (`observed_kpm`)
- [ ] Aggregate by attribute (int/wis/dex/str, parsed from `legendary_id` as §5 did) AND by archetype, with n per cell
- [ ] V1 self-consistency check ASSERTED in harness (b_dead count == wins == winner-player count per cell; fail loud on divergence)
- [ ] Single-regime fingerprint verified: current `run_spatial_fight` + current mobs/min + faithful power; NO old-scale KPM mixed in
- [ ] n per attribute cell ≥ §5 cell sizes (str/dex/int n≈144, wis n≈360) — confirm not underpowered
- [ ] Smoke-test pass (Disc #2): a tiny n_fights dry-run of the harness on ONE kit × ONE shell × ONE cohort confirming the path runs end-to-end, tier_2 actually fires on the boss shell (the whole point), and the termination/KPM fields populate — BEFORE the full run. Include resource-scaling sanity (Disc #2.1): peak memory of the full 2×4×~population run is bounded.
- [ ] Clean JSON output + gandalf-consumable summary table written to `agentic_orchestration/cycle-14-wave-5-season-001/` (suggested: `clean-boss-numbers-harness-2026-06-19.json`)
- [ ] MIGRATION.md: not applicable (no cross-seam contract change; note this explicitly)
- [ ] Round-trip smoke: not applicable — no cross-seam contract change (read-only diagnostic)
- [ ] AGENT_STATE.md updated at session end
- [ ] AUTO-COMMIT harness + math note + output per team commit discipline (in-scope cycle work). DO NOT PUSH — leave the stack clean on disk; record the unpushed commit list in the completion record.

## Acceptance criteria
- [ ] V1–V4 all confirmed in the math note WITH line citations, BEFORE the table is read as data. V1 especially (the load-bearing semantic).
- [ ] **If V1 fails (winner can be "player" without boss-dead OR while player-dead): STOP, do not emit the table, report the failure.** That is the exact failure mode this run exists to avoid.
- [ ] tier_2 demonstrably RUNS on boss shells in the smoke-test (the production-path failure was tier_2-never-ran; the smoke must show it firing)
- [ ] tier_1 bypass is measurement-only — production ship gate (`gauntlet_sim.py`, `ENCOUNTER_COHORT_KPM_BAND`, `eligible_encounters_passed`) untouched
- [ ] termination_reason recorded so death (`a_dead`) is distinguishable from enrage-timeout (`timeout`) is distinguishable from clean kill (`b_dead`) — the single most valuable new column
- [ ] faithful power (max-profile investment) applied; documented how
- [ ] proxy-inclusive kills confirmed (V4)
- [ ] n per attribute cell ≥ §5 cell sizes
- [ ] Round-trip smoke: not applicable — read-only diagnostic, no cross-seam contract change

## Out of scope (explicit non-goals)
- **DO NOT modify the production ship gate** — no edits to `gauntlet_sim.py`, `ENCOUNTER_COHORT_KPM_BAND`, the tier_1 routing, `eligible_encounters_passed`, or any persisted telemetry schema. This is read-only measurement.
- **DO NOT implement the doctrine** (don't wire survive+kill as a gate, don't remove the boss KPM ceiling). This run MEASURES; the design session DECIDES; a later dispatch IMPLEMENTS.
- **DO NOT measure DPS** — scoped out (engine instrumentation, Tier-B follow-on). Note it; don't build it.
- **DO NOT run the clear-room shells** — `boss_with_adds` and `mini_boss` ONLY (the two `*_killed` win-condition shells).
- **DO NOT re-fit or re-tune kits** — measure the season-001 faithful-power population as-is.
- **DO NOT push to remote.**

## Open questions for the agent to resolve (document the decision in the math note)
- **Population provenance (load-bearing — get this right).** The brief wants "the season-001 faithful-power kit population (the same kits behind §5)." `phase3_gauntlet_results.json` has **66 `kit_results`** (each with a `legendary_id`), but `phase2_kit_candidates.json` has **54 kits** (with full reconstruction substrate: `bc_tuple`, `element`, `chain_composition`, `gear_representative`, `skills`). Resolve the 54-vs-66 provenance and choose the kit-loading path that gives you `PlayerClass` objects at faithful power that match §5's population:
  - Option (a): re-materialize the exact season-001 gauntlet kits by driving the SAME generation entry point that produced them, with `apply_max_profile_investment` ON (faithful default). Cleanest if it reproduces the §5 population bit-for-bit.
  - Option (b): reconstruct `PlayerClass` from the phase2 candidate records (+ whatever the gauntlet caller adds to reach 66). Document any reconstruction assumptions.
  - Whichever path: confirm faithful power is applied (V3) and the resulting n per attribute cell ≥ §5 sizes. State the provenance decision and the 54→66 reconciliation explicitly.
- **`survival_rate` vs `b_dead` equivalence on boss shells.** KR's trace says they're identical by construction (both = `winner=="player"` count). Confirm and ASSERT it in the harness. If your read shows `survival_rate` counting anything other than `winner=="player"` (e.g. a survive-but-didn't-kill path leaking in), STOP — that would be V1-adjacent and would mean survive+kill ≠ survival_rate.
- **TTK basis.** Compute TTK from `elapsed_s`/`duration_s` on `winner=="player"`/`b_dead` fights ONLY (kill-time distribution). Decide and document central-tendency (median recommended; report distribution shape — min/median/p90 — since boss-melt tails matter to the DPS-measure design downstream).
- **Termination vocabulary in the output.** The live spatial path uses `winner` ∈ {player, monster, timeout}, mapped to `termination_reason` ∈ {b_dead, a_dead, timeout} (`_term_for`, line 1074). gandalf's table wants `a_dead`/`b_dead`/`timeout`. Use the `termination_reason` values directly; label them in the output for a non-engine reader (e.g. `b_dead = clean survive+kill`, `a_dead = player died, defensive failure`, `timeout = survived but did not kill before enrage`).

## Hand-back (what KR needs to return to gandalf)
On completion, append a completion record with:
- The clean boss table: survive+kill rate + termination breakdown (`a_dead`/`b_dead`/`timeout`) + TTK (median + shape) + KPM, **by attribute (int/wis/dex/str) AND by archetype**, with n per cell.
- V1–V4 verify status (each PASS/FAIL with the line cited).
- The output artifact path.
- The unpushed commit list (harness + math note + output).
- **THE HEADLINE:** does STR actually survive+kill bosses at faithful power, or is the crater real? (i.e. when tier_2 actually runs on STR boss shells — bypassing the KPM-reject that previously prevented it — what is STR's `b_dead` rate vs `a_dead` rate? `a_dead`-dominant = real defensive crater; `timeout`-dominant = too-slow-but-survivable, exactly the legitimate slow-kill the KPM ceiling wrongly condemns; `b_dead`-healthy = the crater was a pure KPM-reject artifact.)
- Any surprise vs the regime-mixed §5 expectation. Flag anything that changes the doctrine.

## References
- Run brief: `agentic_orchestration/gandalf/requests/2026-06-19-kr-clean-boss-numbers-run-prompt.md`
- Doctrine spine + Gate-1 addendum: `agentic_orchestration/gandalf/notes/2026-06-19-encounter-measurement-doctrine-spine.md`
- §5 population artifact: `agentic_orchestration/cycle-14-wave-5-season-001/phase3_gauntlet_results.json` (66 kit_results)
- Reconstruction substrate: `agentic_orchestration/cycle-14-wave-5-season-001/phase2_kit_candidates.json` (54 kits)
- Instrument: `t4_sim_cycling.py:1199` (`w4g2_tier_2_full_sim`); caller-gate bypassed: `:1452`
- Winner semantics: `spatial_engine.py:1742-1771`; enrage caps: `arena.py:522` + mini-boss block
