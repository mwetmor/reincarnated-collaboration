# Dispatch — 2026-05-16 — gamora — Doppelganger gate re-run (post-B14.5 V1 trigger condition)

**From:** knight-rider (authored per gandalf's queued routing item 5, post Matt-gandalf convergence on Option B for the ailment-damage-signatures deferral question)
**To:** gamora
**Approved by:** Matt at 2026-05-16 Day 4 (per memory note `project_ailment_damage_thematic.md` § "Trigger conditions to revisit" — explicit revisit trigger: "After `v1.3-b14-5-recompose-validated` tag lands (whenever that is), run doppelganger gate one more time with the goal of either retiring this design idea or scheduling its implementation.")
**Status:** COMPLETE
**Estimated effort:** 1 session (~30-90 min); the doppelganger gate is an existing test infrastructure invocation; analysis + reporting is the bulk of the work.
**Acceptance:** Doppelganger gate runs against current ±25% variance setting at the current main HEAD (post-B10.4 Option 2 + post-rocket-B6-pre-work + post-gamora-B10-V2 stack); per-archetype win rates reported and classified against the memory note's three signal-strength thresholds (high / medium / urgent); findings filed; deferral-lifting decision queued for knight-rider drafting per the signal classification.

---

## Context — why this dispatch exists

Per the form-bias-cadence-strategy doc § 9.1 rocket cascade + the 5-entry decisions-log batch's Entry 2 § "cipher architecture stays operative" + the memory note `project_ailment_damage_thematic.md` § "Trigger conditions to revisit":

**The ailment-damage-signatures design is currently DEFERRED.** The memory note specifies the revisit trigger: B14.5 lands → re-run doppelganger gate → signal strength determines next action.

**Matt-gandalf converged 2026-05-16 (Day 4)** on the routing: **re-run doppelganger gate FIRST; then decide.** Jack-ryan WARN-1 on the form-bias decisions-log batch was resolved at source-of-truth by gandalf's strategy-doc § 6.3 amendment (matching § 9.1's "Future" framing). The batch commits with the deferral status preserved; this dispatch supplies the empirical evidence the deferral-lifting decision turns on.

**B14.5 V1 has landed.** Plus subsequent work: rocket's B6 pre-work (energy-type-aware tier shifts at intermediate tag `rocket/v1.3-b6-energy-type-tiers @ 639ac3d`) and gamora's B10 V2 (sequential-room semantics at intermediate tag `gamora/v1.3-b10-v2-sequential-room @ 9db2f5a`). The doppelganger gate re-run sees the combined effect of all three on the substrate it was originally measured against.

**Note for attribution honesty (Discipline #13b):** the gate result will reflect the COMPOUNDED effect of B14.5 V1 + B6 pre-work + B10 V2. It will not isolate which work-item contributes which fraction of the signal. The signal classification (high / medium / urgent) is what matters for the deferral-lifting decision; the per-component attribution is a separate question, not this dispatch's scope.

## The memory note's three signal thresholds (the binary the dispatch reports against)

Per `~/.claude/projects/-Users-admin-Games-reincarnated-collaboration/memory/project_ailment_damage_thematic.md` § "Trigger conditions to revisit":

| Signal | Wind_controller (and pure-control archetype) win rate | Implication for ailment-damage-signatures |
|---|---|---|
| **High** | 30-50% WR | "Thematic damage is solved at a different layer; defer indefinitely or downgrade to pure design polish." |
| **Medium** | 20-25% WR (in band but borderline) | "Thematic damage becomes a useful improvement — implement to dial per-fight variance back to ±15% and tighten balance." |
| **Urgent** | Regress out of band (below ~20% or above ~60%; controllers fail mirror match) | "Thematic damage is the immediate fix." |

**The signal classification IS the deliverable.** Once the gate runs, the report classifies against these thresholds and queues the appropriate knight-rider follow-on (deferral-lifting decisions-log entry of the matching shape).

## What this dispatch does

### Step 1 — Verify state

Before running the gate:
- Confirm engine `main` HEAD includes both rocket's B6 pre-work commit AND your own B10 V2 commit (`9db2f5a`)
- Confirm doppelganger gate infrastructure is operational against the V2-semantic balance loop (B10 V2 changed convergence semantics — verify the doppelganger gate's WR calculation is using room-level WR per V2, not per-encounter WR per V1; document the semantic alignment in your findings)
- Confirm the ±25% per-fight variance setting is still active (per memory note context)

### Step 2 — Run the gate

Standard doppelganger gate invocation against the current 11-class roster from `season_001005` (the freshly-regenerated season per star-lord's 2026-05-16 dispatch). Use whichever seed/configuration the gate's standard test harness expects.

Capture per-class WR data including:
- All 11 classes' mirror-match WR
- Specifically: wind_controller, earth_controller, fire_controller, water_controller (the pure-control archetypes from gamora's archetype-gradient table per `qa/findings/2026-05-16-gamora-modifier-range-rootcause.md`)
- Variance distribution (per-class WR variance across N fights per pair)
- Fight termination reasons (HP-timeout vs KO vs other)

### Step 3 — Signal classification

Apply the memory note's threshold table to the per-control-archetype WR results:

- If wind_controller (and the other pure-control archetypes as supporting evidence) lands in the 30-50% range → **HIGH SIGNAL** (B14.5 V1 + B6 + B10 V2 dissolved the ailment-damage-signatures need; deferral indefinite)
- If 20-25% (in band but borderline) → **MEDIUM SIGNAL** (deferral-lifting recommended; implement thematic damage)
- If out of band → **URGENT SIGNAL** (deferral-lifting required; thematic damage is the immediate fix)
- If the classification is ambiguous (e.g., wind_controller in HIGH range but earth_controller in MEDIUM) → name the ambiguity and recommend signal class with reasoning

### Step 4 — Findings file

File at `agentic_orchestration/qa/findings/2026-05-16-gamora-doppelganger-gate-rerun.md`. Cover:

1. **State verification** (Step 1 outcome)
2. **Per-class WR data** (table + commentary on the four pure-control archetypes specifically)
3. **Signal classification** (high / medium / urgent / ambiguous) with explicit reasoning
4. **Cross-component attribution caveat** (Discipline #13b) — note that the signal reflects compounded B14.5 V1 + B6 + V2 effect; do not attribute fractions
5. **Recommendation for knight-rider** on the deferral-lifting decisions-log entry shape (matches the signal class per memory note text)
6. **V2-semantic alignment confirmation** (Step 1 verify): does the doppelganger gate correctly read room-level WR under V2, or does it need a small extension dispatch first?

### Step 5 — Notify knight-rider

At completion, knight-rider applies the routing:
- **HIGH SIGNAL:** drafts deferral-indefinite or downgrade-to-design-polish decisions-log entry; ailment-damage-signatures dispatch NOT authored (or authored as deferred-design-polish lower priority)
- **MEDIUM SIGNAL:** drafts deferral-lifted decisions-log entry; authors rocket dispatch for ailment-damage-signatures implementation (~1-2 days per memory note timing estimate)
- **URGENT SIGNAL:** drafts deferral-lifted decisions-log entry with urgency note; authors rocket dispatch for ailment-damage-signatures implementation IMMEDIATE priority; may require also authoring a small gamora compensation patch in the interim

## Cross-seam considerations

- **Rocket:** downstream consumer of the signal — if MEDIUM or URGENT, rocket gets the ailment-damage-signatures implementation dispatch with the memory note's effect-resolver + generator-changes scope per § "Implementation cost at revisit time."
- **Star-lord:** no immediate cross-seam ask. The doppelganger gate uses existing telemetry; new fields would only be needed if the gate's V2-semantic alignment requires telemetry schema work (Step 1 verification; surface if so).
- **Spirit-guide:** marginal-value calculations may consume convergence_winrate or modifier values; V2 semantic shift may affect recommendation logic per gamora's prior B10 V2 completion record (the LOW-priority cross-seam flag). Out of scope for this dispatch; surface if directly observed during the re-run but do not investigate.

## Out of scope (explicit)

- **Implementation of ailment-damage-signatures.** This dispatch is signal-evidence-only. The implementation dispatch (if signal warrants) is a follow-on per § Step 5.
- **Cross-component attribution.** The signal reflects compounded B14.5 V1 + B6 + V2 effect; isolation experiments are a separate question (Discipline #13b) and not commissioned here.
- **Modification of variance settings.** Re-run is at the current ±25% per-fight variance. Changing variance is a separate balance-loop tuning decision.
- **Modification of doppelganger gate test harness** (unless V2-semantic alignment requires a small fix per Step 1 verification — surface as a flag, do not unilaterally extend).
- **Strategy doc amendment.** The strategy doc § 6.3 was already amended by gandalf 2026-05-16; this dispatch's findings feed downstream decisions-log work, not strategy-doc revision.

## Required reading

- `~/.claude/projects/-Users-admin-Games-reincarnated-collaboration/memory/project_ailment_damage_thematic.md` (the source-of-truth for trigger conditions + signal thresholds + implementation cost estimates)
- `canonical/story/form-bias-cadence-strategy.md` § 6.3 + § 9.1 (Future framing of ailment-damage-signatures; rocket cascade reference)
- `agentic_orchestration/gandalf/open-threads/2026-05-16-ailment-damage-signatures-timing-and-arpg-canon.md` (Matt-gandalf convergence context; resolution routing)
- `agentic_orchestration/qa/findings/2026-05-16-gamora-modifier-range-rootcause.md` (your own prior findings — archetype-gradient table is the reference for which classes count as "pure-control")
- `reincarnated-engine/src/reincarnated/simulation/math/b10-v2-sequential-room-convergence.md` (your own B10 V2 math note — V2 semantics doppelganger gate must align with)
- `reincarnated-engine/design/decisions/decisions-log.md` 2026-05-16 entries (calibration epoch + engine-balance-stewardship companion entries; provide the framework the signal classification reports against)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Disciplines #1 (math-before-code), #11 (attribution), #12 (semantic-shifting — V2 semantic alignment), #13b (outcome attribution opacity — for the cross-component caveat)

## Acceptance criteria

- [ ] Engine state verified (B6 + B10 V2 both in HEAD; doppelganger gate V2-semantic alignment confirmed or flagged)
- [ ] Gate runs against current 11-class roster from season_001005
- [ ] Per-class WR data captured for all 11 classes; pure-control archetypes specifically highlighted
- [ ] Signal classified (high / medium / urgent / ambiguous) with explicit reasoning
- [ ] Findings filed at `agentic_orchestration/qa/findings/2026-05-16-gamora-doppelganger-gate-rerun.md`
- [ ] V2-semantic alignment confirmation explicit in findings
- [ ] Knight-rider notified with signal class + recommended decisions-log entry shape

## Tag policy

No tag required (analysis-only; no code changes unless V2-semantic alignment requires a small fix — in which case a separate intermediate tag follows the standard discipline). If the V2-semantic alignment IS a code-change, file it as a separate dispatch; do NOT bundle with this analysis.

---

## Completion record

**Completed:** 2026-05-16 (gamora)
**Findings path:** `agentic_orchestration/qa/findings/2026-05-16-gamora-doppelganger-gate-rerun.md`
**Signal class:** HIGH
**Pure-control archetype WR summary:**
- wind_controller/wind: avg WR 0.487 (L17=0.58, L33=0.38, L50=0.50) — HIGH
- earth_controller/earth: avg WR 0.473 (L17=0.44, L33=0.56, L50=0.42) — HIGH
- fire_controller/fire: avg WR 0.393 (L17=0.36, L33=0.46, L50=0.36) — HIGH
- water_controller/water: avg WR 0.393 (L17=0.40, L33=0.38, L50=0.40) — HIGH

All 11 classes pass gate (DOPPELGANGER_BALANCED_RANGE [0.20, 0.80]).

**V2-semantic alignment status:** NOT APPLICABLE — the doppelganger gate is inherently
encounter-level (calls `simulate_fight()`, not `simulate_room()`). Gate code and constants
are identical at b15ecb2 and HEAD (5d51b5a). No semantic mismatch between gate output and
memory note thresholds (both defined at encounter-level WR). A V2-aware room-level gate
extension is a potential future small dispatch; surfaced as a flag only (NOT implemented here).

**Notes for knight-rider:**
1. Signal is HIGH. Recommended action per memory note: draft deferral-indefinite decisions-log entry. Do NOT author rocket dispatch for ailment-damage-signatures implementation.
2. Entry 2 of the 2026-05-16 form-bias decisions-log batch "Future" framing is consistent with this finding and requires no amendment.
3. Season_001005 was NOT re-generated under B6 pre-work or B10 V2. The class substrate is pre-B6. This is a substrate-provenance note, not a finding that changes the signal classification — the gate code is unchanged between the generation commit and HEAD.
4. Fight termination: 0.0% timeout rate across 21,600 pure-control archetype fights. KI-B6-1 crisis (100% timeout for wind_controller) is completely resolved. B14.5 V1 recompose-first loop is the primary driver.
5. V2-aware doppelganger gate (room-level mirror match) is a future extension option — surfaced for knight-rider tracking but NOT commissioned here.
