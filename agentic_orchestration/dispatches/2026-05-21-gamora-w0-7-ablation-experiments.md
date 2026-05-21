# Dispatch — 2026-05-21 — gamora — W0.7: LC-002 + LC-009 + LC-011 ablation experiments

**From:** knight-rider
**To:** gamora (simulation seam); jack-ryan reviews ablation experiment design before each fires
**Approved by:** gandalf attestation 2026-05-21 § 5 (six autonomous workstreams cleared); per activation dispatch § 4 Step 4 W0.7 + protocol § 6.1.2 W0.7
**Status:** PENDING — ACTIVE (gamora may execute when launched)
**Estimated effort:** ~1-2 days per ablation (3 ablations total; ~4-6 days)
**Acceptance:** 3 ablation experiments designed + run + analyzed; per-LC attribution data documented; tag `qd-rebuild/v0.7-ablation-complete`.

**AMENDMENT 2026-05-21 (knight-rider autonomous per Matt directive; surfacing to Matt at session close per ADR-002):** Per jack-ryan Gate-1 LC-009 disposition (APPROVE-OPTION-C 2026-05-21):
> Where Discipline #11 empirical inspection refutes the precondition for ablation (signal is a data quality artifact, not a current-era structural signal), the LC may close with empirical inspection + math note + structural reinterpretation as the deliverable. This constitutes meta-attribution under Discipline #13b and satisfies the LC's closure requirement. Ablation runs are not required.

Decision tree for Discipline #11 outcomes:
- **Signal confirmed present:** design/revise ablation to attribute it (LC-002 path — runs executed)
- **Signal shrunk but non-zero:** design ablation for actual signal (path not yet exemplified)
- **Signal refuted as artifact:** no ablation; close with empirical note (LC-009 Option C path)

All three branches are valid Discipline #11 outcomes. Filed at `agentic_orchestration/jack-ryan/qa/w0-7-lc-009-ablation-design-gate-1-2026-05-21.md` § ARP-7.

---

## Context — Discipline #13b ablation framework

Per Discipline #13b (Outcome attribution opacity): per-variable contribution to observed convergence shapes is UNKNOWN without ablation. Three LCs from jack-ryan's audit carry EMPIRICALLY-SURFACED findings that require ablation to attribute cause:

- **LC-002** — Fire element bias (23.6% over-represented vs 20% uniform expected; per B14.5 sidecar finding #4)
- **LC-009** — Hunter modifier range 1.82 (the least consistent shape across seeds; per B14.5 sidecar finding #2)
- **LC-011** — Convergence iterations highest for controllers/mages, lowest for rogue/hunter (per B14.5 sidecar finding #1)

Each ablation isolates one variable at a time per Discipline #13b. The output is attribution data — what fraction of the observed shape is attributable to which variable.

**Track C synthesis 2026-05-21 reinforces** that calibration-uniform Pattern-A is the dominant pathology; per-substrate / per-archetype patterns observed in LC-002/LC-009/LC-011 are second-order effects layered on top. The ablations characterize those second-order effects.

## Per-LC ablation design

### LC-002 — Fire element bias ablation

**Variable to isolate:** D1 pool weighting + `element/selector.py` rotation logic that produces fire selection.

**Ablation experiment:**
- Run 1: baseline — current D1 weighting + selector logic
- Run 2: fire weight halved
- Run 3: fire weight zeroed (forced equal across other elements)
- Compare element distribution across 10-20 seasons per run

**Predicted shape:** under Run 2, fire over-representation should drop to ~12-15%; under Run 3, fire should be uniform with others. Magnitude of the drop attributes the over-representation to the weighting variable.

**Discipline #13b output:** attribute observed 23.6% to (a) D1 pool weighting fraction X% + (b) selector rotation logic fraction Y% + (c) residual structural presupposition fraction (100-X-Y)%.

### LC-009 — Hunter modifier range ablation

**Variable to isolate:** hunter template variables — `range_profile=long`, `geometry_bias`, `kit_size`, interaction with `ARCHETYPES_FORBIDDEN_CLOSE_RANGE`.

**Ablation experiment:**
- Run 1: baseline — current hunter template
- Run 2: hunter `range_profile` flat to medium (test range-profile contribution)
- Run 3: hunter `geometry_bias` removed (test geometry contribution)
- Run 4: hunter `kit_size` reduced to match other archetypes (test kit-size contribution)
- Measure modifier range across 10-20 seasons per run

**Predicted shape:** hunter's 1.82 range reduces toward typical ~0.5 range under one or more of the ablations. The ablation that reduces variance most attributes the variance to that variable.

**Discipline #13b output:** attribute 1.82 range to (a) range_profile contribution + (b) geometry_bias contribution + (c) kit_size contribution + (d) constraint-interaction contribution.

**Track C OQ-6 surface:** if hunter is physical-tagged and physical hunter hits modifier=1.000 ceiling (per Track C synthesis § 3 OQ-6), the ablation results inform whether the W0.1 B14.5 V2 energy-type lever fix interacts with the hunter range pathology. Cross-reference findings to W0.1 math note.

### LC-011 — Controller/mage iteration overhead ablation

**Variable to isolate:** which constraint(s) cause controller/mage classes to require 3-5× more recompose iterations per kit.

**Ablation experiment:**
- Run 1: baseline — current convergence iteration counts per archetype
- Run 2: control-pure archetypes with mage-template constraints removed (test mage-constraint contribution)
- Run 3: simplified constraint sets — minimum constraint set retained per archetype
- Measure iterations per archetype per run

**Predicted shape:** under Run 2 (mage-constraint removal), controller iterations drop toward median. Under Run 3, all archetypes converge in similar iteration counts.

**Discipline #13b output:** attribute iteration overhead to (a) mage-specific constraints + (b) control-pure mechanic constraints + (c) substrate-X-role-shape interaction.

**Forward implication:** if controller/mage classes converge slowly in QD-archive filling (per LC-011 framing), the QD generation loop may underrepresent them in the archive. Surface findings as input to W0.4 specialist code audit (broader convergence-cost-awareness question) + P3 archive maintenance design.

## Coordination + sequencing

**Sequence ablations one at a time** to avoid telemetry-DB write conflicts (per Discipline #3: no parallel regens of same seed). Each ablation:
1. Design experiment per template above
2. **Jack-ryan Gate-1 review of experiment design** before running (per activation dispatch § 4.2 critique-pair structure: "W0.7: jack-ryan reviews ablation experiment design before fires")
3. Run experiment (smoke-test mode per Discipline #2 where feasible)
4. Analyze + document attribution
5. Tag intermediate: `qd-rebuild/v0.7-ablation-lc-XXX`

After all 3 complete: hive tag `qd-rebuild/v0.7-ablation-complete`.

## Required reading before starting

- `agentic_orchestration/jack-ryan/research/legacy-constraint-audit-2026-05-21/constraint-inventory.md` (LC-002, LC-009, LC-011 full entries)
- `~/.claude/projects/-Users-admin-Games-reincarnated-collaboration/memory/project_b14_5_sidecar_analyses.md` (the B14.5 sidecar findings that surfaced these)
- `canonical/story/substrate-generalization-track-c-synthesis-2026-05-21.md` § 1.2 + § 3 OQ-6 (modifier-range substrate data; physical hunter ceiling)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` § 13b (Outcome attribution opacity; the authoritative spec)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` § 11.1 (state-space conditioning — apply to ablation telemetry)
- `reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md` (prior records)
- `reincarnated-engine/element/selector.py` + `b6_archetype_templates.py` + `simulation/balance_loop.py` (target files for ablation)

## Math-before-code (if applicable)

Each ablation requires a math-before-code prediction (Discipline #1). Author predictions BEFORE running each ablation; verify post-run. If measured ≠ predicted, re-diagnose mechanism BEFORE adjusting parameters or hypothesis.

## Cross-seam contract change? (Principle 6 gate)

**Round-trip: not applicable — ablation experiments are read-only-against-current-code; they modify configuration parameters for the duration of the experiment but do NOT add/modify/rename/remove fields on cross-seam contracts. Code changes from ablation findings (if any) become follow-on workstreams with their own round-trip clauses.**

## Scope

- [ ] LC-002 fire-bias ablation: experiment designed + jack-ryan Gate-1 review + run + analyzed
- [ ] LC-009 hunter modifier range ablation: experiment designed + jack-ryan Gate-1 review + run + analyzed
- [ ] LC-011 controller/mage iteration overhead ablation: experiment designed + jack-ryan Gate-1 review + run + analyzed
- [ ] Per-LC attribution data documented in AGENT_STATE.md + a per-LC math note
- [ ] Cross-reference to W0.1 (LC-009 hunter feeds into B14.5 V2 lever) + W0.4 (LC-011 informs convergence-cost-awareness in archive)
- [ ] Tag: `qd-rebuild/v0.7-ablation-complete`

## Acceptance criteria

- [ ] Each ablation: math-before-code prediction + measurement + attribution conclusion
- [ ] Discipline #13b output (per-variable contribution attribution) documented per LC
- [ ] No regressions to current sim behavior (ablations are configuration-level; restore original config after each run)
- [ ] Jack-ryan Gate-1 reviews documented (experiment design valid before run)
- [ ] Round-trip: not applicable — ablation workstream

## Out of scope

- Implementing fixes to the variables identified (those are follow-on workstreams)
- Re-running B14.5 sidecar analyses (those are LIVE; this dispatch attributes their findings via ablation)
- Cross-LC interaction analysis (each ablation isolates one LC at a time per Discipline #13b)
- New constraint discovery (focus on the 3 named LCs)

## Open questions for the agent to resolve

- **Smoke-test vs full regen for ablation runs**: per Discipline #2 + Track C precedent (~3-5 seeds per substrate), smoke-test mode is appropriate for first-pass attribution; full regen as needed for confidence intervals. Document choice per ablation.
- **Run count per ablation**: 10-20 seasons per run gives reasonable confidence; document choice with reasoning.
- **LC-002 + LC-009 + LC-011 cross-interactions**: if Run 2 of one ablation reveals an interaction with another LC (e.g., fire-bias ablation reveals hunter modifier variance changes), document as a finding but do NOT chase the interaction in this dispatch — surface for follow-on.

## Critique-pair structure

Per activation dispatch § 4.2:
- **jack-ryan** reviews ablation experiment design BEFORE each run (measurement validity)
- **gandalf** reviews findings post-run for design-judgment implications (e.g., does LC-002 fire-bias attribution inform substrate-as-cohesion theme-library design?)
- **knight-rider** folds verdicts into state-of-hive + cross-references to W0.1 + W0.4

## References

- `agentic_orchestration/dispatches/2026-05-21-knight-rider-qd-rebuild-hive-activation.md` § 4 Step 4 W0.7 + § 4.2 critique-pair
- `canonical/story/hive-mind-protocol-qd-engine-rebuild-2026-05-21.md` § 6.1.2 W0.7 + § 6.1.3 critique-pair structure
- `agentic_orchestration/jack-ryan/research/legacy-constraint-audit-2026-05-21/constraint-inventory.md` LC-002, LC-009, LC-011
- `canonical/story/substrate-generalization-track-c-synthesis-2026-05-21.md` § 1.2 + § 3 OQ-6
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` § 1, § 11.1, § 13b
- `~/.claude/projects/-Users-admin-Games-reincarnated-collaboration/memory/project_b14_5_sidecar_analyses.md`
