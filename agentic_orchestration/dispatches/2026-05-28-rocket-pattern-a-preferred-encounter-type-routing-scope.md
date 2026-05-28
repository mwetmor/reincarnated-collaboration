# DISPATCH — Rocket Pattern-A Query: preferred_encounter_type Routing Scope (R2 Verification)

**Authored:** 2026-05-28 (post-freeze hive-mind re-entry; Mode A item 1)
**Author:** knight-rider (Cycle 14 Mode A hive-mind orchestrator)
**Recipient:** rocket (foundation seam; T4 catalog + mechanic_alteration + season_generation_pipeline)
**Pattern:** Pattern A-light empirical query (read-only verification + brief report)
**Expected effort:** ~30 min
**Status:** PENDING — fires on receipt
**Authority:** Matt 2026-05-28 adjudication lock (`agentic_orchestration/gandalf/notes/2026-05-28-phase-4-rerun-3-adjudication.md` § 2 R2 VERIFY-BEFORE-DECIDE)

---

## 0. CONTEXT (read first — 5 min)

Phase 4 RE-RUN-3 (telemetry `cycle-14-wave-5-season-001/w-alpha-7-plus-phase-4-rerun-3-two-layer-t4-sweep-telemetry.json` + `bounded-viability-validation-baseline-2026-05-28.json`) returned **compound_pass=FALSE** across all 7 profiles and BVV calibration anchor. T1+T3+T5 pass; **T2 zero-KPM fails 19 cells**; **T4 Secondary specialization fails 14-18/18 kits per profile**.

Matt + gandalf Pattern-A-deep adjudication this session locked the disposition:

- R1 (DDA 1.75× → 2.0×): **REJECT** (Primary universal-EXEMPT + SCAFFOLD-Cycle-15-RETIREMENT per Discipline #40)
- R2 (preferred_encounter_type assignment misalignment): **VERIFY-BEFORE-DECIDE** ← **THIS QUERY**
- R3 (T2 zero-KPM): **CYCLE 14.5 HOTFIX BLOCKING CLOSE** (gamora forensic; sequenced after this query)
- R4 (Secondary T4 cohort peaks): **CYCLE 16+ DEFERRAL** via BC axis expansion (c-hybrid § 1.1 amendment 5→10 candidate axes)
- Two-layer T4 architecture: **PRESERVE (Read B)** — no code rollback
- Close path: **Option γ-refined** — amended close-criterion T1+T2+T3+T5 (T4 dropped as gate)

**Required reading (in order):**

1. `agentic_orchestration/gandalf/notes/2026-05-28-phase-4-rerun-3-adjudication.md` § 2 (R1/R2/R3/R4 disposition) + § 4 (ranked tier table)
2. `canonical/story/c-hybrid-cell-and-curation-architecture-2026-05-28.md` § 1.1 (BC axis expansion 5→10 candidates; amendment marker) + § 1.3 (Layer 2-derived velocity granularity)
3. `agentic_orchestration/cycle-14-hive-mind-state.md` § "MATT ADJUDICATION LOCKED 2026-05-28" + § "KR MODE A HIVE-MIND CHARGE ACTIVE"

---

## 1. THE QUERY

**Question (verbatim per adjudication § 2 R2):**

> Does `preferred_encounter_type` route Secondary T4 variant SELECTION at generation time, or does it only route Primary DDA TARGETING at simulation time?

**Why this matters per adjudication § 2 R2 disposition table:**

| Routing scope | R2 disposition |
|---|---|
| Primary DDA targeting only (simulation-time) | **REJECT** — Primary is universal-EXEMPT (doc 51 § 10.8.9); R2 cannot move T4 specialization metric |
| Also Secondary T4 variant selection (generation-time) | **Cycle 14.5 hotfix candidate** — misaligned preferred_encounter_type would route the wrong Secondary T4 variants into cohort positions, suppressing cohort-relative peaks |

Under Read B (Matt-locked this session) — even if scope is generation-time-also, R2 likely reduces to REJECT because Secondary T4 specialization is dropped as Cycle 14 close-gate, so R2 becomes a Cycle 16+ refinement composing with BC axis expansion. **UNLESS rocket Pattern-A surfaces an immediate player-experience consequence we missed.**

---

## 2. EXPECTED INVESTIGATION SHAPE (Pattern A-light)

**Read-only verification of routing scope.** No code changes. Report back with:

### 2.1 Generation-time path

Trace `preferred_encounter_type` from assignment → consumption at kit generation:

- `mechanic_alteration.py:686` `_assign_preferred_encounter_type()` — assignment algorithm (per math note § 2.3)
- `mechanic_alteration.py:1170` `select_primary_t4()` — Primary T4 slot population
- `mechanic_alteration.py:1206` `get_preferred_encounter_type()` — convenience helper for `season_generation_pipeline.py`
- `mechanic_alteration.py:707` doc comment: *"The selection machinery is bypassed for Primary T4 (select_primary_t4() handles this)"* — initial-read signal that selection machinery is Primary-only

**Specifically verify:** does Secondary T4 / Tertiary T4 variant SELECTION (the per-kit ELEMENT_CONVERSION / GEOMETRY_COLLAPSE / RESOURCE_CONVERSION / TRADE_OFF_REVERSED_FRENZY assignment that lands in `kit.secondary_t4` + `kit.tertiary_t4`) read `preferred_encounter_type` to influence:

- Which variant strategy is picked? (e.g., does a kit with `preferred_encounter_type="boss_with_adds"` get a different Secondary T4 strategy than `"elite_pack"`?)
- Which variant magnitude / parameter is picked? (e.g., does ELEMENT_CONVERSION Variant A vs B vs C selection depend on preferred encounter?)
- Which sub-target / context the Secondary T4 binds to? (e.g., does a Secondary T4 also have a "preferred encounter" sub-targeting field?)

### 2.2 Simulation-time path

Trace `preferred_encounter_type` consumption in `simulation/`:

- `combatant.py:216-227` field definitions (`t4_preferred_encounter_type` + `t4_current_encounter_type`)
- `combatant.py:573-680` `from_player_class()` direct_damage_amplification handler populating `t4_preferred_encounter_type`
- `damage_resolver.py:248-256` + `:404` DDA multiplier application
- `t4_sim_cycling.py` fight-context injection of `t4_current_encounter_type = scenario_shell_id`

**Specifically verify:** at simulation time, does ANY non-DDA strategy (Secondary T4 = ELEMENT_CONVERSION / GEOMETRY_COLLAPSE / RESOURCE_CONVERSION / TRADE_OFF_REVERSED_FRENZY) read `t4_preferred_encounter_type` or `t4_current_encounter_type` to modulate its mechanic?

### 2.3 Report format

A brief markdown report (~1-2 pages) appended to this dispatch as a completion record. Cover:

1. **VERDICT** — single line: "preferred_encounter_type routes [Primary DDA targeting only / Primary DDA targeting AND Secondary T4 selection / something else]"
2. **GENERATION-TIME PATH** — file:line citations for each consumer of `preferred_encounter_type` at generation
3. **SIMULATION-TIME PATH** — file:line citations for each consumer of `t4_preferred_encounter_type` / `t4_current_encounter_type` at simulation
4. **EMPIRICAL TEST** (if uncertain) — one-line grep / pytest output demonstrating the routing scope
5. **R2 DISPOSITION RECOMMENDATION** — based on verdict, recommend REJECT vs Cycle 14.5 hotfix vs Cycle 16+ deferral
6. **DISCIPLINE #12 / #1.2 NOTE** — if any semantic-shift or code-citation surfaces, flag for the math-note record

**No code changes. No tag. No commit.** Pure read-and-report.

---

## 3. OUT OF SCOPE

- ❌ Any code change to `preferred_encounter_type` routing
- ❌ Any code change to Primary T4 or Secondary T4 selection logic
- ❌ R1 DDA multiplier tune (adjudicated REJECT)
- ❌ R3 T2 zero-KPM forensic (gamora seam; sequenced next)
- ❌ R4 BC axis expansion impl (Cycle 16+)
- ❌ Phase 4 RE-RUN-4 fire (sequenced post R3)
- ❌ Any tagging or push

---

## 4. RISKS + COMPLICATIONS

- **Edge case — preferred_encounter_type used by something other than DDA:** if `preferred_encounter_type` is consumed by an unexpected path (e.g., a sidecar telemetry attribution; gauntlet cohort assignment; some Secondary T4 variant that you haven't surfaced previously), flag it in the verdict explicitly.
- **Math-note alignment check:** the rocket v1.13 math note at `simulation/math/w-alpha-7-plus-phase-4-rerun-3-two-layer-t4-2026-05-28.md` should describe the routing-scope intent; verify the implementation matches the math-note intent. If they disagree, that's a Discipline #12 semantic-shift surface for KR to route.
- **Discipline #47 (host-RAM-aware operational concurrency) active:** rocket session uses Pattern A-light read-only; no large grep without `find -size +100M` pre-flight; no parallel I/O.

---

## 5. URGENCY + SEQUENCING

**Fires FIRST in KR Mode A dispatch sequence.** Lightest investigation; reduces R-set before the heavier R3 gamora forensic. Likely retires R2 to REJECT under Read B (architectural posture says simulation-time-only based on initial code-read; rocket attests via verification).

**Cycle 14 v1 MVP close gates on the dispatch sequence: this query → R3 gamora forensic → Phase 4 RE-RUN-4 → canonical capture → jack-ryan Gate-2 → Cycle 14 closure record.** Single sub-agent at a time per Discipline #47 R47.4.

**KR will fire R3 gamora forensic dispatch on receipt of this report.**

---

**KR signature:** authored per Matt 2026-05-28 adjudication lock + KR Mode A hive-mind charge + Discipline #47 R47.4 single-seam sequencing on 8 GB constrained host. R2 verification is the lightest cheapest-empirical-refutation test of the question "does this matter for Cycle 14 close?" — answer in ~30 min, retire or escalate.

---

## Completion record

**Completed:** 2026-05-28
**Author:** rocket
**Effort:** ~30 min read-only verification

---

### 1. VERDICT

`preferred_encounter_type` routes **Primary DDA targeting only (simulation-time)**.

It has zero routing influence over Secondary T4 variant SELECTION at generation time or simulation time. KR's initial-read signal is confirmed correct.

---

### 2. GENERATION-TIME PATH

**Assignment (generation-time, Primary T4 only):**

- `mechanic_alteration.py:686-702` — `DirectDamageAmplificationStrategy._assign_preferred_encounter_type()`: algorithmic assignment from kit `damage_geometry` + `dominant_element`. Returns one of `open_arena | chokepoint_corridor | magic_pack | elite_pack | boss_with_adds | mini_boss`.
- `mechanic_alteration.py:714-718` — `DirectDamageAmplificationStrategy.generate_alteration()`: stores the result as `strategy_params["preferred_encounter_type"]`. This is the PRIMARY T4 AlterationOutput only.
- `mechanic_alteration.py:1170-1203` — `select_primary_t4()`: Primary T4 universal assignment entrypoint. Calls `DirectDamageAmplificationStrategy.generate_alteration()`. The doc comment at `mechanic_alteration.py:707-709` (inside `opportunity_scan`) explicitly states "The selection machinery is bypassed for Primary T4 (select_primary_t4() handles this)."
- `mechanic_alteration.py:1206-1225` — `get_preferred_encounter_type()`: convenience helper used by `season_generation_pipeline` to populate `kit.preferred_encounter_type` (the per-kit schema field). This is a derivation helper, not a selection input.
- `season_generation_pipeline.py:243-248` — `KitCandidate.preferred_encounter_type` field: schema slot for the derived value. Populated from `get_preferred_encounter_type()`.
- `season_generation_pipeline.py:800-804` — `_gamora_fields_from_t4_candidate()` DIRECT_DAMAGE_AMPLIFICATION branch: places `preferred_encounter_type` into `direct_damage_amplification` combatant fields dict. This is the DDA arm of the dispatch; the other arms (ELEMENT_CONVERSION, TRADE_OFF_REVERSED_FRENZY, RESOURCE_CONVERSION, GEOMETRY_COLLAPSE) contain no `preferred_encounter_type` read.

**Secondary/Tertiary T4 selection (generation-time):**

The Layer 2 selection function `select_mechanic_alteration()` at `mechanic_alteration.py:1033-1112` calls `strategy.opportunity_scan(bc, substrate)` on each of the 6 Layer 2 strategies in `REGIME_CHANGE_STRATEGIES_V1_13_LAYER2`. None of those `opportunity_scan` implementations read `preferred_encounter_type` — they score against BC axes (`damage_geometry`, `resource_economy`, `damage_amplitude`, etc.). `preferred_encounter_type` does not appear as an input to `select_mechanic_alteration()` and is not present in `BcTargetView`. Secondary and Tertiary T4 variant selection (ELEMENT_CONVERSION variant A/B/C choice, GEOMETRY_COLLAPSE, RESOURCE_CONVERSION, TRADE_OFF, TRADE_OFF_REVERSED_FRENZY scoring) is entirely blind to `preferred_encounter_type`.

---

### 3. SIMULATION-TIME PATH

**All consumers of `t4_preferred_encounter_type` / `t4_current_encounter_type` at simulation time:**

- `combatant.py:216-230` — field definitions (`t4_preferred_encounter_type` + `t4_current_encounter_type`); both documented as DDA-only fields.
- `combatant.py:571-586` — `from_player_class()` DDA handler: reads `af["direct_damage_amplification"]["preferred_encounter_type"]` to populate `_final_t4_preferred_encounter_type`. No other strategy branch (ELEMENT_CONVERSION, TRADE_OFF_REVERSED_FRENZY, RESOURCE_CONVERSION, GEOMETRY_COLLAPSE) touches either encounter-type field.
- `combatant.py:679` — `CombatantState` constructor: sets `t4_preferred_encounter_type=_final_t4_preferred_encounter_type`; `t4_current_encounter_type` defaults to `None` (injected at fight setup).
- `damage_resolver.py:249` — comment confirming DDA application rule.
- `damage_resolver.py:403-407` — **sole live consumption site**: inside `resolve_skill()`, guarded by `t4_alteration_type == "DIRECT_DAMAGE_AMPLIFICATION"` check, then `_preferred_enc == _current_enc` equality. Multiplies `magnitude` by `DIRECT_DAMAGE_AMPLIFICATION_MULTIPLIER` (1.75) when match. No other strategy block reads either encounter-type field.
- `t4_sim_cycling.py:1032-1040` — `w4g1_tier_1_sweep()` fight-context injection: sets `player_combatant.t4_current_encounter_type = encounter.scenario_shell_id`. Commented as DDA-specific; no other T4 mechanic reads this field.
- `t4_sim_cycling.py:1128-1132` — `w4g2_tier_2_full_sim()` mirrors the Tier 1 injection pattern, same DDA-only purpose.
- `unified_calibration_loop.py:3548-3570` — `primary_dda` branch in UCL two-layer logic: calls `select_primary_t4()`, extracts `preferred_encounter_type`, builds `alteration_fields["direct_damage_amplification"]` dict. This is the calibration-loop entry point for Primary T4; it is not a Secondary T4 routing path.

**Non-DDA strategies at simulation time:** ELEMENT_CONVERSION modifies `damage_type` on skills (via `combatant.t4_element_conversion_variant`); TRADE_OFF_REVERSED_FRENZY modifies `accuracy` and `crit_chance` at `combatant.py:607-608`; RESOURCE_CONVERSION and GEOMETRY_COLLAPSE apply their own combatant fields. None of these read or write `t4_preferred_encounter_type` or `t4_current_encounter_type`.

---

### 4. EMPIRICAL TEST

Exhaustive grep across all engine Python source (`src/reincarnated/**/*.py`) for `preferred_encounter_type`, `t4_preferred_encounter_type`, and `t4_current_encounter_type` returned 32 hits total. Every hit resolves to one of three categories: (a) DDA generation-time assignment / carry-forward, (b) DDA simulation-time field definition / injection / application, (c) comments and logging. Zero hits in any Secondary/Tertiary T4 selection path, any non-DDA strategy class, or any encounter-type-routed variant-selection logic.

---

### 5. R2 DISPOSITION RECOMMENDATION

**REJECT** — under both the routing-scope finding and Read B.

The routing scope finding alone is sufficient: `preferred_encounter_type` routes Primary DDA targeting only. Primary T4 is universal-EXEMPT from the T4 specialization metric (doc 51 § 10.8.9). Therefore R2 cannot move the T4 Secondary specialization metric at all — fixing assignment misalignment would not change which Secondary T4 variants are placed into cohort positions. R2 is architecturally moot for the Secondary T4 failure.

Under Read B (Matt-locked this session), even if a future design expands `preferred_encounter_type` to influence Secondary T4 selection (a Cycle 16+ possibility per adjudication § 6, item 4), that work composes with BC axis expansion and is not a Cycle 14.5 hotfix candidate. No immediate player-experience consequence surfaces from the current routing scope that would override the REJECT disposition.

**R2 is retired: REJECT.**

---

### 6. DISCIPLINE #12 / #1.2 NOTE

No semantic-shift surfaces in the implementation vs math note. The generation math note (`generation/math/w-alpha-7-plus-two-layer-t4-architecture-implementation-2026-05-28.md`) § 2.3 describes `preferred_encounter_type` as a DDA routing signal exclusively; the simulation math note (`simulation/math/w-alpha-7-plus-phase-4-rerun-3-two-layer-t4-2026-05-28.md`) § 3.1 describes the gamora harness DDA-injection responsibility exclusively. Both notes are consistent with the implementation. No Discipline #12 flag required.

One minor observation: `mechanic_alteration.py` line 1066 references `REGIME_CHANGE_STRATEGIES_V1` (without the `_13_LAYER2` suffix) in `select_mechanic_alteration()`, while the strategy list definition at line 848 is named `REGIME_CHANGE_STRATEGIES_V1_13_LAYER2`. This warrants a brief check that the two names resolve to the same object — but this is a naming-consistency observation, not a semantic-shift surface affecting the R2 finding. Flagged for KR awareness if a follow-on tidy is desired.

---

**Signed:** rocket (foundation seam verification)
**For:** KR Mode A hive-mind R2 disposition under Cycle 14 adjudication lock 2026-05-28.
