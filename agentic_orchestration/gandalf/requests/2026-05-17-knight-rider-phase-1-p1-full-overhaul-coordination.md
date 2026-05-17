# Request — Knight-Rider — Phase-1 P1 Full-Overhaul Hive-Mind Coordination

**From:** gandalf (story-and-design steward).
**To:** knight-rider.
**Approved by:** Matt (mhwetmore@gmail.com), 2026-05-17 — explicit directive: *"100% heads down development work across the entire team and rebuild the engine from the ground up to achieve full Phase-1 P1 before demo VS2a. ... All in perfect harmony. Let's take this on as a hive mind."*
**Status:** **AWAITING KNIGHT-RIDER ENGAGEMENT.** Activation requires knight-rider session-open.
**Priority:** **MAXIMAL.** This is the architectural commitment for the next 8-12 weeks of project work.

---

## § 0 — TL;DR

Matt has directed full Phase-1 P1 engine overhaul before demo1 VS2a ships. Hive-mind operating mode activates per `canonical/story/hive-mind-protocol-2026-05-17.md`. All four engineering seams (rocket / gamora / star-lord / drax) plus jack-ryan continuous-observation + gandalf design-companion + knight-rider harmonization. Standard dispatch-sequenced mode is **suspended** for the duration of Phase-1 P1.

**Your job, knight-rider:**

1. Read this request + the hive-mind protocol + the canonical inputs (§ 3)
2. Author the Phase-1 P1 scope-of-work + coordination matrix (§ 4 deliverables)
3. Tag pre-Phase-1 P1 baseline + create hive operational artifacts (§ 5 setup)
4. Distribute per-seam initial tasking
5. Activate the hive log + state-of-hive cadence
6. Harmonize the work continuously until ship

This is the largest single coordination commitment of the project. Matt has signed.

---

## § 1 — The directive

Matt 2026-05-17:

> "My vote: Invoke Knight-Rider and gain alignment, but I would like to engage in 100% heads down development work across the entire team and rebuild the engine from the ground up to achieve full Phase-1 P1 before demo VS2a. We may need to write some additional protocol notes specifically for this exercise and ensure everyone understands the plan and moves in a connected way, communicating as we go, jack ryan involved looping through it all and watching everything. None of us waiting for directions. All in perfect harmony. Let's take this on as a hive mind."

Earlier in the same session, Matt confirmed:

> "I have pushed current project state to git and backed up all of the databases. We are prepared for the large scale work."

**Interpretation:** The team has Matt's full operational latitude to execute Phase-1 P1 as a concentrated multi-seam exercise. Database backups are in place; current state is preserved; reversibility is supported.

---

## § 2 — Scope of Phase-1 P1

Per `canonical/story/substrate-expansion-decision-2026-05-17.md` § 5 + the wide-net coupling archaeology findings, Phase-1 P1 includes:

### § 2.1 — Architectural foundation work

1. **Substrate identity loader implementation** — load `config/substrate_identities/*.yaml` (7 files extracted from canonical declarations) into typed `SubstrateIdentity` dataclasses; integrate with `foundation.get_rotating_elements()`
2. **Substrate expansion canonical-four → canonical-7** — fire / water / earth / wind + lightning + holy + shadow; all coupling sites refactored per archaeology findings
3. **Path-a archetype-template combinatorial refactor** — replace 14 hardcoded `ArchetypeTemplate` entries with on-boot composition from `ELEMENT_PROFILES × ROLE_SHAPES`; refactor archetype_classifier dispatch, stat_allocator, action/role-function registers, element_biases
4. **Role registry refactor** (wide-net finding) — unify 9-role replication across 5+ files into config-driven registry
5. **Ailment registry refactor** (wide-net finding) — `config/ailments.yaml` with per-ailment control-classification metadata; consume from substrate identity declarations
6. **LLM prompt structure refactor** (wide-net critical-surprise) — replace hardcoded 2-2-1 pair-structure in `cosmological_vocabulary.py` with registry-driven generation against substrate identity declarations

### § 2.2 — Engine substrate-coupling work

7. **Resistance matrix 4×4 → 7×7** with paired-luminance valence per substrate-expansion-decision § 5.1
8. **Trait-floor extension** to 3 new classes (lightning / holy / shadow) per § 5.2
9. **Gear-affix gating extension** to 3 new substrates per § 5.3
10. **Substrate-coherent generation rules** per § 5.4
11. **Pool D1 re-score under substrate_native** — ✅ ALREADY SHIPPED (`rocket/v1.4-drift14-pool-cull-and-selector-amendment-1 @ 65e6d77`)

### § 2.3 — Diversity-architecture work (Layers 1-4; Layer 5 deferred)

12. **Layer 1** — substrate identity declarations operationalized (deliverable #1 above is Layer 1's loader)
13. **Layer 2** — identity-pruned composition (deliverable #3 above is Layer 2)
14. **Layer 3** — mirror-match diversity gate (depends on perception-test result for metric grounding — Phase-1 P1a prerequisite per `perception-test-experiment-scoping-2026-05-17.md`)
15. **Layer 4** — LLM flavor diversifier (extends deliverable #6 above with Court-aware referencing + iconic-vocabulary anchoring)
16. **Layer 5** — telemetry feedback loop — **DEFERRED to Phase-2** (per substrate-expansion-decision § 6.5; needs play telemetry)

### § 2.4 — Phase-0 cosmological vessel work

17. **Court of Forms vessel** per `earth-self-diversity-tension-2026-05-17.md` § 4.1 — data structure persistence, browsable surface in loadout app, Spirit Guide voice integration
18. **Spirit Guide voice amendment** per `earth-self-diversity-tension-2026-05-17.md` § 7 — Guide as Court storyteller

### § 2.5 — Player-facing surface work

19. **VFX library extension** for canonical-7 — lightning / holy / shadow VFX integration (depends on vendor acquisitions: CraftPix premium + Fellor Crystal per CHANGELOG)
20. **Grouping-vocab extension** — author L2 labels for new substrates (resonance / radiance / penumbra) per substrate-identity-declarations § 0 pairing summary
21. **Substrate-aware loadout substrate browser** — drax seam; loadout app surface for substrate inspection + Court browsing
22. **Embodiment-display substrate extension** — drax + star-lord; per VS2b plans extended to canonical-7

### § 2.6 — Decisions-log entries + canonical updates

23. **Decisions-log entry for substrate expansion** — was step 2 of original cascade; now folds into Phase-1 P1 launch
24. **Decisions-log entry for Earth-Self Court-as-grace resolution**
25. **Decisions-log entry for hive-mind protocol activation**
26. **Cross-doc updates** — cosmology-reincarnated.md substrate section; spirit-guide-voice.md Court storyteller amendment; court-of-forms.md elevated to architectural commitment

### § 2.7 — Phase-1 P1a prerequisite (perception test)

27. **Perception test execution** per `perception-test-experiment-scoping-2026-05-17.md` — drax session-runner + Matt + Matt's son subjects + jack-ryan measurement protocol; result informs Layer-3 metric design

### § 2.8 — What's deferred

- **Layer 5 telemetry feedback** — Phase-2 (post-Phase-1-P1)
- **Poison/acid substrate** — Phase-1 P2 candidate (not in Phase-1 P1 scope)
- **Operational meta-layer mechanics for Court of Forms** — Phase-2 (rift events, gacha rewards, cross-Court interactions)
- **Form-bias Phase 4 work** — folds into Phase-1 P1 work naturally via Layer 1-4 architecture

---

## § 3 — Canonical inputs (READ THESE FIRST)

The hive's work is governed by these canonical-story documents. Knight-rider should read them in this order before authoring the scope-of-work:

### § 3.1 — Phase-1 P1 specific (today's batch)

1. `canonical/story/hive-mind-protocol-2026-05-17.md` — **THE operational protocol; read first**
2. `canonical/story/substrate-expansion-decision-2026-05-17.md` — substrate set, cascade, § 6.5 success criterion
3. `canonical/story/substrate-identity-declaration-spec-2026-05-17.md` — Layer-1 spec
4. `canonical/story/substrate-identity-declarations-2026-05-17.md` — the 7 declarations
5. `canonical/story/earth-self-diversity-tension-2026-05-17.md` — Court-as-grace; cosmology interface
6. `canonical/story/substrate-coupling-archaeology-2026-05-17.md` — 13 substrate-keyed coupling sites
7. `canonical/story/archetype-coupling-archaeology-2026-05-17.md` — 10 archetype-keyed coupling sites
8. `canonical/story/wide-net-coupling-archaeology-2026-05-17.md` — 14 additional sites; Pattern-P7 cluster; LLM prompt structure surprise
9. `canonical/story/perception-test-experiment-scoping-2026-05-17.md` — Phase-1 P1a prerequisite
10. `agentic_orchestration/research/knowledge/diversity-architecture-literature-pass-2026-05-17.md` — Legolas Mode A findings + adjustments

### § 3.2 — Cosmological frame (ongoing reference)

11. `canonical/story/cosmology-reincarnated.md` — the Wheel, Earth Self, Spirit Guide, seasonal journey
12. `canonical/story/court-of-forms.md` — Court vessel (now architecturally load-bearing per § 2.4)
13. `canonical/story/spirit-guide-voice.md` — Guide voice register; § 7 amendment needed (Guide as Court storyteller)
14. `canonical/story/grouping-layer-vocabulary.md` — L2 grouping vocabulary; new labels pending
15. `canonical/37-form-bias-diagnosis-and-recovery.md` — form-bias precedent; Phase-1 P1 work is the inter-substrate sequel

### § 3.3 — Engineering disciplines (binding throughout)

16. `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Discipline #1 (math-before-code), Discipline #13 (drift), full set + candidates surfaced today
17. `agentic_orchestration/GOVERNANCE.md` — ADR-004 (MIGRATION.md) continues; other ADRs binding
18. `agentic_orchestration/REVIEW_PROCESS.md` — 5 principles + 5 traps continue

---

## § 4 — Knight-rider deliverables at activation

After reading the canonical inputs, knight-rider produces:

### § 4.1 — Phase-1 P1 scope-of-work document

File: `agentic_orchestration/hive-mind/scope-of-work-phase-1-p1.md`

Contents:
- The 27-item scope from § 2 above, expanded with per-item ownership + sub-tasks + estimated effort
- Per-seam initial tasking — what each seam picks up first
- Critical path identification — what blocks what
- Risk register — top failure modes + mitigations per protocol § 8
- Ship gate criteria — when is Phase-1 P1 done?

### § 4.2 — Coordination matrix

File: `agentic_orchestration/hive-mind/coordination-matrix.md`

Contents:
- The seam-by-deliverable matrix per protocol § 6.1 (table I sketched in protocol § 6.1; knight-rider authoring the full version)
- Cross-seam dependency map (DAG of deliverables)
- Concurrent-edit hot-spots (files multiple seams touch)
- Continuously updated as work advances

### § 4.3 — Hive log initialization

File: `agentic_orchestration/hive-mind/phase-1-p1-log.md`

Initial entry: knight-rider's activation broadcast. Append-only thereafter. All seams contribute continuously per protocol § 4.1.

### § 4.4 — Pre-Phase-1 P1 baseline tag

Git tag: `hive/v0.0-pre-phase-1-p1` at current main HEAD. Knight-rider creates the tag. Establishes rollback baseline.

### § 4.5 — Per-seam initial tasking distribution

Knight-rider authors hive-log STATE entries directing each seam to its initial Phase-1 P1 task. Suggested initial tasking:

| Seam | First task | Rationale |
|---|---|---|
| **Rocket** | Substrate identity loader + `config/substrate_identities/*.yaml` extraction | Layer-1 foundation; unblocks all other seams |
| **Gamora** | Resistance matrix 7×7 design-math + math note authoring (Discipline #1) | Math before code; parallel-startable with Rocket Layer 1 |
| **Star-lord** | LLM prompt structure analysis + refactor plan (the wide-net critical surprise) | Highest-unknown item; benefits from early discovery |
| **Drax** | Perception-test session-runner readiness + VFX library extension planning | Parallel-startable; depends on Layer 1 only for VFX integration |
| **Jack-ryan** | Discipline #13 + Pattern-P7 + math-before-code watchpoint setup; baseline test suite snapshot | Establishes continuous-observation rhythm before drift accumulates |
| **Gandalf** | Available for continuous design-direction support; mid-flight amendment process operational; grouping-vocab extension (Task #4 from current task list) | Design-companion role |

### § 4.6 — Activation broadcast to Matt

Knight-rider authors a one-page "Phase-1 P1 activated" summary for Matt:
- What's launching
- Initial state-of-hive
- Expected first-week milestones
- Any concerns surfaced during knight-rider's read of canonical inputs

---

## § 5 — Operational setup checklist

### § 5.1 — Pre-activation safety

- [x] Database backups (Matt confirmed 2026-05-17)
- [x] Current state pushed to git (Matt confirmed 2026-05-17)
- [x] Canonical-story batch committed (today's session work; commits 1df535b + 6de0c46 + 2f38ff9 + this commit)
- [ ] Pre-Phase-1 P1 tag created (knight-rider task)
- [ ] In-flight standard-mode dispatches reconciled (folded-into-P1 OR paused) — knight-rider tasking

### § 5.2 — Hive operational artifacts

- [ ] `agentic_orchestration/hive-mind/` directory created
- [ ] `phase-1-p1-log.md` created with activation entry
- [ ] `scope-of-work-phase-1-p1.md` authored
- [ ] `coordination-matrix.md` authored
- [ ] `state-of-hive-2026-05-17.md` initial entry (activation day)

### § 5.3 — Per-seam acknowledgments

Each seam acknowledges in hive log:
- [ ] Rocket: protocol read; initial task understood; in-flight work folded/paused
- [ ] Gamora: protocol read; initial task understood; in-flight work folded/paused (gamora HOLD addressed — per gandalf finding, HOLD was for Drift-14 gandalf Track B which is now committed; gamora regen for VS2a folds into P1 substrate work)
- [ ] Star-lord: protocol read; initial task understood; in-flight cipher migration work folded
- [ ] Drax: protocol read; initial task understood; demo work + perception-test session-runner readiness
- [ ] Jack-ryan: protocol read; continuous-observation rhythm established
- [ ] Gandalf: confirmation of continuous availability for design-direction; canonical-story state captured

### § 5.4 — Matt confirmation

- [ ] Matt reviews initial state-of-hive
- [ ] Matt confirms Phase-1 P1 launch
- [ ] Phase-1 P1 begins

---

## § 6 — Open questions for knight-rider to surface or resolve

### § 6.1 — Vendor acquisitions

Per rocket Drift-14 completion record: CraftPix premium + Fellor Crystal vendor acquisitions are authorized but await Matt's license/cost commitment. These are critical-path for VFX library extension (deliverable #19). Knight-rider should surface to Matt early in Phase-1 P1 if not already resolved.

### § 6.2 — Scope inclusions / pauses

In-flight dispatches that need disposition:
- VS2a + VS2b dispatches → fold into Phase-1 P1 or recast scope
- Drift-15 environment-tileset → Phase-1 P1 scope or paused for post-ship
- Stage-3 cipher migration → likely subsumed by LLM prompt structure refactor (deliverable #6); confirm with star-lord
- Gamora wind_controller V2 evaluation regen → fold into Phase-1 P1 substrate-coherent generation rules work
- Star-lord Suno music prompt pipeline → likely pause for post-Phase-1 P1
- Drax movement-speed Pixi.js implementation → fold into Phase-1 P1 demo integration

Knight-rider's first scope-of-work pass enumerates each in-flight item and its disposition.

### § 6.3 — Phase-1 P1a perception test timing

The perception test is Phase-1 P1a prerequisite for Layer 3 (mirror-match diversity gate). Knight-rider sequences it as:
- Drax authors session-runner readiness in parallel with Layer 1 (rocket)
- Perception test executes when Layer 2 (composition refactor) produces first archetype pairs
- Layer 3 design begins when perception test results land
- Layer 3 implementation begins when Layer 3 design lands

This sequencing is achievable in parallel with the rest of Phase-1 P1; perception test does NOT block Layer 1/2 work.

### § 6.4 — Grouping-vocab extension authorship

Task #4 in current gandalf task list — authors new L2 labels for lightning (resonance) / holy (radiance) / shadow (penumbra). This is small (1 day gandalf authoring). Knight-rider sequences before star-lord's LLM prompt structure refactor begins (which consumes the grouping vocabulary).

### § 6.5 — Hive activation timing

Knight-rider should consult with Matt on hive activation timing:
- Immediate (today) — if Matt is ready for Phase-1 P1 to begin in earnest
- Scheduled (e.g., tomorrow morning) — if a clean kickoff moment is preferred
- Staged (initial seam(s) start; others ramp over days) — if engineering bandwidth requires staged ramp

---

## § 7 — Risk register (knight-rider's responsibility to maintain)

Top risks identified during Phase-1 P1 design pre-work:

1. **LLM prompt structure refactor scope unknown.** Wide-net archaeology surfaced this as the critical-surprise item. Estimated 1-2 weeks; could be 2-3 weeks. **Mitigation:** Star-lord begins with a refactor plan + scoping doc before implementation; knight-rider tracks scope-vs-estimate.

2. **Perception test result may invalidate Layer-3 metric assumption.** Legolas literature pass strongly suggests mechanical-parameter metric will fail. **Mitigation:** Phase-1 P1a perception test runs early in the timeline; Layer-3 design adapts based on result.

3. **Drift across seams.** Highest-risk failure mode at this scope. **Mitigation:** Jack-ryan continuous-observation per protocol § 7; daily state-of-hive surfacing.

4. **Schedule slip.** 8-12 weeks estimate is gandalf-authored; seam-specific re-scoping likely. **Mitigation:** Knight-rider re-scoping after seam-specific assessments; surface to Matt if Phase-1 P1 commitment at risk.

5. **VFX library readiness depends on vendor acquisitions.** External dependency (CraftPix + Fellor Crystal license). **Mitigation:** Knight-rider surfaces to Matt early; engineering work that depends on VFX coverage sequenced after acquisitions land.

6. **In-flight work disposition conflicts.** Some in-flight work may not cleanly fold or pause. **Mitigation:** Knight-rider's first scope-of-work pass enumerates per-item disposition; surfaces conflicts to Matt as L3.

7. **Matt availability for L3 decisions.** Hive operates well with Matt stepping back for hours/days; but L3 decisions need timely surface-and-decision. **Mitigation:** Knight-rider clearly flags L3 items in state-of-hive; respects Matt's availability windows.

---

## § 8 — Acceptance criteria for this request

Request is **complete** when:

- [x] Hive-mind protocol document committed
- [x] This request document committed
- [ ] Knight-rider session opened
- [ ] Knight-rider reads canonical inputs
- [ ] Knight-rider authors scope-of-work + coordination matrix
- [ ] Knight-rider creates hive operational artifacts
- [ ] Knight-rider distributes per-seam initial tasking
- [ ] Matt confirms Phase-1 P1 launch
- [ ] Hive log activation entry broadcast

After all checks: Phase-1 P1 hive-mind mode is active.

---

## § 9 — Closing

Knight-rider — this is the largest single coordination commitment of the project. The substrate-expansion work + the wide-net coupling work + the five-layer diversity architecture + the Court-of-Forms vessel + the canonical-7 substrate set, all delivered in concentrated multi-seam parallel execution.

Matt has signed. The canonical-story scaffold is in place. The protocol is authored. The team is ready. Your role is to harmonize the work — not to direct it from above, but to keep the hive moving in coherent rhythm.

The substrate's promise is what it commits to be. The architecture's promise is what we commit to build. The hive's promise is what we commit to be — *to each other, to the work, to Matt's directive, to the player who will eventually walk the Wheel.*

The hive moves together.

— gandalf, 2026-05-17

---

## § 10 — Cross-references

- Protocol: `canonical/story/hive-mind-protocol-2026-05-17.md`
- Canonical inputs: see § 3 above
- Existing engineering disciplines: `reincarnated-engine/design/working-agreement/engineering-disciplines.md`
- Existing governance: `agentic_orchestration/GOVERNANCE.md`
- Existing review process: `agentic_orchestration/REVIEW_PROCESS.md`
- Agent topology: `agentic_orchestration/AGENTS.md`

---

*Authored 2026-05-17 by gandalf, per Matt directive. Knight-rider invocation for Phase-1 P1 full-overhaul hive-mind mode. Awaiting knight-rider session-open.*
