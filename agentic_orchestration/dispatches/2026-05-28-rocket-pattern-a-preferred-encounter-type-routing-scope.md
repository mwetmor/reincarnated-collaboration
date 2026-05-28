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

(rocket appends here)
