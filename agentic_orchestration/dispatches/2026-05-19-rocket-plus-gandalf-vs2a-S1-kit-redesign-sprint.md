# Dispatch — 2026-05-19 — rocket + gandalf consult — VS2a S1 kit-redesign sprint (path per F2)

**From:** knight-rider
**To:** rocket (generation seam — catalogue OWNER under chosen path) + gandalf (design consult — criteria + first-batch class selection input + validation gate)
**Approved by:** PRE-APPROVED in batch (Matt 2026-05-19); fires when F2 decision lands + F1 schema field operational
**Estimated effort:** Path-dependent — 4–6 weeks hand-redesign (a) / 2–3 weeks R8-inversion (b) / 3–5 weeks hybrid (c)
**Acceptance:** Per § Acceptance below + R1 sprint re-run as canonical metric (70–85% pass rate threshold per kit-redesign queue § 5.1). Tag fires: `vs2a/v0.7-kit-redesign-sprint-complete`.
**Hive context:** VS2a hive ACTIVE; F2 (gandalf approach decision) + F1 (`geometry_type` schema field) are upstream gates. S1 is the **central catalogue workstream** for VS2a — gates S2 (B6 main work) and L1 (demo regen ship).

---

## TL;DR — three-branch dispatch

This dispatch is **pre-authored for all three F2 paths.** Rocket consumes the branch gandalf's F2 disposition selects. Branches differ on effort + sequencing + per-class methodology + first-batch class selection rationale. **Common to all branches:** R1 sprint re-run is the canonical validation metric; 70–85% pass rate is the success threshold; gandalf consult cadence is invocation-on-need; rocket has L1 within seam.

---

## Context

Per `canonical/story/r1-kit-redesign-queue-2026-05-19.md` (gandalf-authored 2026-05-19; the catalogue pathology surface that motivates S1) + F2 disposition (`canonical/story/vs2a-kit-redesign-approach-2026-05-19.md` once authored):

- 51 of 51 shipped classes failed the per-tier gate under disposition-1 + disposition-3 calibration
- Failure pattern is kit-architectural (range-collapse for "mages"; single-vector defensive layers; energy-cycling pathology; archetype-tag mismatch)
- Forecast: ~5–10 kit-acceptable / ~20–30 kit-mediocre / ~10–15 kit-broken
- S1 is the operational closure: redesign the broken/mediocre subset, re-run R1 sprint, validate against 70–85% threshold

---

## Required reading (all branches)

In order:
1. F2 decision doc: `canonical/story/vs2a-kit-redesign-approach-2026-05-19.md` (gandalf-authored; defines branch)
2. `canonical/story/r1-kit-redesign-queue-2026-05-19.md` § 3 redesign criteria (range diversity / defensive layer / burst window / archetype alignment / energy cycling) + § 5 roadmap integration
3. `reincarnated-engine/design/working-agreement/R1-blocker-3-disposition-2026-05-19.md` (encounter recalibration)
4. F1 dispatch + completion record (`agentic_orchestration/dispatches/2026-05-19-rocket-plus-star-lord-vs2a-geometry-type-schema.md`)
5. `canonical/story/r8-disposition-2026-05-19.md` (R8 disposition — substrate-identity invariance + `inverted` committed)
6. `canonical/story/substrate-identity-declarations-2026-05-17.md` § 9.5 (R8 surface-readability amendment)
7. `canonical/story/engine-rebuild-2026-05-19-gap-solutions-and-tests.md` § 2 (R1 spec) + § 8 (R8 spec)
8. R1 sprint v2 + v3 outputs: `reincarnated-engine/output/R1-class-retune-2026-05-19/`
9. `reincarnated-engine/src/reincarnated/generation/AGENT_STATE.md` (rocket checkpoint)
10. `agentic_orchestration/hive-mind/scope-of-work-vs2a.md` § 2.2 (S1)
11. `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 + § 4.9

---

## Branch (a) — Hand-redesign sprint

**Scope per F2 path (a):**

- [ ] Audit the 51 shipped classes against criteria § 3.1–§ 3.5 of `r1-kit-redesign-queue-2026-05-19.md` (range diversity / defensive layer / burst window / archetype alignment / energy cycling)
- [ ] Categorize per sprint v3 telemetry + rocket's design read: kit-acceptable / kit-mediocre / kit-broken
- [ ] **First-batch selection** (per F2 disposition's first-batch class selection criteria): typically kit-broken first (shadow_mage 0018/0045; class_0008 physical_grappler at modifier 4.0; class_0016 lightning_mage range-collapse — the most-extreme pathologies; representative archetype coverage)
- [ ] Per-class hand-redesign with gandalf consult cadence (rocket invokes when archetype convention is in question or when criteria conflict)
- [ ] Each redesigned class: write redesign rationale at `reincarnated-engine/output/S1-kit-redesign/class_<NNNN>-redesign.md` capturing pathology pattern + redesign moves + criteria satisfied
- [ ] Skill JSON regenerated for redesigned classes; `geometry_type` field (F1) carried through explicitly
- [ ] Re-run R1 sprint against redesigned catalogue (gamora consumer; surface re-run request via hive log)
- [ ] Tag: `vs2a/v0.7-kit-redesign-sprint-complete` when R1 sprint re-run achieves 70–85% pass rate (or per F2 revised threshold)
- [ ] MIGRATION.md appended at `reincarnated-engine/src/reincarnated/generation/MIGRATION.md` (per-class redesign batch is a content-change set; consumer obligation note for star-lord telemetry + gamora sim)

**Effort:** 4–6 weeks rocket; gandalf consult ~0.5 day per week.

---

## Branch (b) — R8-inversion regeneration

**Scope per F2 path (b):**

- [ ] Regenerate all 51 classes (or subset per F2 disposition § 3) under R8 `inverted` pipeline (coalescence-first + per-entity LLM naming)
- [ ] Generation-time prompt-augmentation MAY incorporate criteria § 3.1–§ 3.5 (range diversity / defensive layer / archetype alignment) as prompt-input — OR rocket runs pure-mechanical-first and validates post-hoc against criteria. Per F2 disposition (which path F2 picks within (b)).
- [ ] Seed strategy per F2: re-roll (new seeds) OR preserve seeds (mode-only diff). Default per F2: re-roll for fresh emergent archetypes.
- [ ] Manifest continuity for 5 shipped seasons: per F2 — do shipped seasons re-converge (replaced) or do new seasons supplement (additive)? Default per F2: new seasons supplement; shipped seasons preserved with `geometry_type` backfilled per F1
- [ ] `geometry_type` field (F1) emitted as generation-time field (not post-derived)
- [ ] Re-run R1 sprint against regenerated catalogue
- [ ] Substrate-identity Test 4-style post-hoc validation: do emergent archetypes preserve substrate-mode-of-action per R8 disposition § 9.5? Surface in completion record
- [ ] Cohesion sanity-check: gandalf judges 3+ regenerated seasons against R8 cohesion-judging protocol (`agentic_orchestration/hive-mind/R8-cohesion-judging-protocol-2026-05-19.md`); ensure cohesion + 0.5 from baseline
- [ ] Tag: `vs2a/v0.7-kit-redesign-sprint-complete` when R1 sprint re-run achieves 70–85% pass rate AND cohesion gate satisfied
- [ ] MIGRATION.md updated for catalogue replacement (rocket appends to `reincarnated-engine/src/reincarnated/generation/MIGRATION.md` + star-lord telemetry continuity note)
- [ ] LLM cost telemetry: per-season regen cost captured (~$3.20/season × N seasons regenerated; star-lord captures)

**Effort:** 2–3 weeks rocket; gandalf consult on cohesion judging ~1 day; star-lord LLM orchestration ~0.5 wk.

---

## Branch (c) — Hybrid

**Scope per F2 path (c):**

- [ ] Partition rule per F2 disposition: kit-broken classes → R8-inversion regeneration (where curation has nothing to preserve); kit-mediocre classes → hand-redesign (where curated kits have salvageable identity); kit-acceptable preserved
- [ ] Execute branch (b) tasks on the kit-broken subset (~10–15 classes)
- [ ] Execute branch (a) tasks on the kit-mediocre subset (~20–30 classes)
- [ ] Sequencing per F2: R8-inversion sub-batch first then hand-redesign, OR reverse, OR parallel
- [ ] Re-run R1 sprint against final hybrid catalogue
- [ ] Tag: `vs2a/v0.7-kit-redesign-sprint-complete` when R1 sprint re-run achieves 70–85% pass rate
- [ ] MIGRATION.md captures both methodology shifts

**Effort:** 3–5 weeks rocket; gandalf consult equivalent to (a) + (b) combined per-class.

---

## Common to all branches

### Per-redesign / per-regenerated-class verification

- [ ] All five criteria of `r1-kit-redesign-queue-2026-05-19.md` § 3 satisfied (range diversity / defensive layer / burst window / archetype alignment / energy cycling)
- [ ] `geometry_type` per skill explicit (F1 field)
- [ ] Validator passes (engine schema)
- [ ] Smoke-test GREEN

### Cross-seam coordination

- gamora consumer (R1 sprint re-run as validation gate; surface re-run request via hive log when each batch lands)
- star-lord consumer (telemetry continuity; `class_balance_results` table extension may surface)
- drax consumer (no breaking change; S2 main work + L1 demo regen consume the new catalogue)
- elrond consumer (no backfill needed beyond F1 backfill; new content is generation-time)
- jack-ryan continuous observation: Discipline #13 drift watch; Pattern P7 silent-default check; Discipline #17 semantic-shifting if archetype-tags shift meaning

### Gandalf design consult cadence

- gandalf invocation cost is real (per AGENTS.md); rocket invokes when:
  - Archetype convention is in question (e.g., "should `lightning_mage` mean ranged-int-mana per § 3.4 OR should the kit's actual composition reset the tag?")
  - Criteria conflict surfaces (e.g., burst-window vs energy-cycling trade-off where the kit can satisfy one but not both)
  - First-batch class selection reveals catalogue-wide pattern beyond § 3 criteria
  - Cohesion gate (branch b/c only): post-regeneration judging
- gandalf otherwise OBSERVES (the F2 disposition is the design-input; per-class decisions are rocket L1)

---

## Cross-seam contract change? (Principle 6 gate)

**YES** — catalogue content changes at scale. MIGRATION.md required:

- Rocket appends to `reincarnated-engine/src/reincarnated/generation/MIGRATION.md` (per-class redesign batch OR catalogue regen depending on branch)
- Star-lord appends to `reincarnated-engine/src/reincarnated/export/MIGRATION.md` if telemetry surface changes (class_balance_results may extend; surface as it arises)

**Round-trip smoke REQUIRED.** End-to-end fixture: redesigned/regenerated class → schema validator → fight engine simulation → telemetry recorder → export packet → loadout consumer (if loadout consumes new content). Field-presence + integrity checks at each boundary. **R1 sprint re-run IS the round-trip smoke at scale** (51 classes × 5 tiers × N fights through the full pipeline).

---

## Acceptance criteria

- [ ] F2-selected branch scope executed (a / b / c per F2 disposition)
- [ ] Per-class redesign / regeneration verification: all criteria § 3 satisfied; `geometry_type` explicit; validator passes; smoke GREEN
- [ ] R1 sprint re-run executed (gamora; via hive log re-run request) achieving 70–85% pass rate threshold (or revised threshold per F2 disposition)
- [ ] MIGRATION.md appended at generation seam + export seam (if telemetry surface changes)
- [ ] Round-trip smoke per Principle 6
- [ ] Cohesion sanity-check (branch b/c only): R8 cohesion judging protocol applied; cohesion within 0.5 of baseline
- [ ] AGENT_STATE.md updated for rocket; gandalf canonical-doc amendments authored where the redesign work prompts archetype convention amendments
- [ ] Hive log: STATE on sprint start + STATE on each batch handoff + STATE on R1 sprint re-run handoff to gamora + HANDOFF on completion
- [ ] Tag fire request: `vs2a/v0.7-kit-redesign-sprint-complete`

---

## Out of scope

- B6 main work (S2 — gamora-authored; separate dispatch; consumes S1 redesigned catalogue)
- B6 skill-tree UI (F4 — drax; separate dispatch)
- R2 H1 re-validation (R2-RT — gamora; separate dispatch; gated on F1)
- Spatial boss recalibration (R2 H1 disposition § 3.4 forward-flagged; potentially VS2b)
- Substrate identity declaration further amendments (gandalf scope; ad-hoc if surfaces)
- Per-encounter recalibration beyond R1 disposition-3 envelope
- Class additions beyond 51-class catalogue (VS2b/VS2c+ scope)
- chierit per-archetype mapping (gandalf decision; parallel; not gating S1)

---

## Open questions for the agents

- **First-batch class selection** — per F2 disposition; if F2 doesn't enumerate specifically, rocket selects: shadow_mage 0018/0045 + class_0008 + class_0016 + 1 each archetype-tag representative (typically 7–10 first-batch classes)
- **R1 sprint re-run cardinality** — per first batch or per full sprint completion? L1 rocket + gamora coordination. Recommendation: per-batch R1 sprint re-run as canary; full re-run at sprint completion
- **MIGRATION.md granularity** — per-class entries or batch entries? L1 rocket. Recommendation: batch entries with class-level enumeration in appendix
- **Archetype convention amendments** — if redesign work prompts archetype convention amendments (e.g., "lightning_mage" semantic is amended to permit close-range chain-lightning at 4m), gandalf authors canonical-doc amendment. Surface to gandalf via hive log if hand-redesign work surfaces convention questions
- **Cohesion gate threshold (branch b/c only)** — within 0.5 of baseline per R8 protocol; document choice; if cohesion regresses, surface to gandalf for re-disposition per R8 partial-commit precedent
- **`inverted_no_naming` deferred opt-in usage** — explicitly OUT OF SCOPE per R8 disposition § 5a; do NOT use deferred opt-in path. Document.
- **R1 sprint re-run threshold edge cases** — if achieves 65–69%, is that PARTIAL PASS or FAIL? L1 gandalf consult; document in completion record

---

## References

- `canonical/story/vs2a-kit-redesign-approach-2026-05-19.md` (F2 disposition; upstream branch)
- `canonical/story/r1-kit-redesign-queue-2026-05-19.md` § 3 + § 5
- `reincarnated-engine/design/working-agreement/R1-blocker-3-disposition-2026-05-19.md`
- `canonical/story/r8-disposition-2026-05-19.md` + R8 cohesion-judging protocol
- `canonical/story/substrate-identity-declarations-2026-05-17.md` § 9.5
- F1 dispatch + completion record
- `reincarnated-engine/output/R1-class-retune-2026-05-19/` (v2 + v3 outputs)
- `agentic_orchestration/hive-mind/scope-of-work-vs2a.md` § 2.2 (S1)
- `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 + § 4.9 + § 4.4 + § 4.5

---

## Autonomous-operation authority + activation gate

**Activation gate:** F2 disposition lands + F1 schema field operational (acceptance complete on both).

**Post-activation:** rocket L1 within seam; gandalf L2-equivalent consult on archetype convention + cohesion gate. R1 sprint re-run is gamora consumer (via hive log re-run request). No Matt-wait either branch.

---

*Authored 2026-05-19 by knight-rider under pre-approval-batch authority. S1 is the central VS2a catalogue workstream; F2 picks the path; rocket builds; gamora validates; the 51-class catalogue becomes a catalogue you can ship.*

---

## Completion record

**Branch executed:** (b) R8-inversion regeneration — first-batch (1 season)
**Author:** rocket
**Date:** 2026-05-19
**Status:** FIRST-BATCH COMPLETE — awaiting gamora R1 sprint re-run + gandalf cohesion judgment for full gate determination

### Deliverables

1. Season_100001 generated under R8 `inverted` pipeline — `reincarnated-engine/output/S1-first-batch-2026-05-19/season_100001/`
2. `spatial_geometry_type` emitted at generation time (F1 field — 100% present on 124 class skills; not post-derived heuristic)
3. B6 archetype_tag-based tier assignment honored (no class_id hard-coding; confirmed via B6 pre-work parameterization audit)
4. MIGRATION.md appended — `reincarnated-engine/src/reincarnated/generation/MIGRATION.md`
5. AGENT_STATE.md updated — `reincarnated-engine/src/reincarnated/generation/AGENT_STATE.md`
6. Hive log STATE + HANDOFF entries filed — `agentic_orchestration/hive-mind/engine-rebuild-log.md`
7. Tag fired: `rocket/v1.22-s1-first-batch-regen` (intermediate seam tag; engine repo)

### First-batch validation gate results

| Criterion | Target | Observed | Status |
|---|---|---|---|
| 1. boss_kr >= 0.10 on >= 1 class | >= 1 | class_0002: 0.130 / class_0007: 0.240 | **PASS** |
| 2. mini_kr >= 0.15 on >= 2 classes | >= 2 | 5/11 classes pass | **PASS** |
| 3. cohesion >= 4.0 (gandalf judges) | >= 4.0 | PENDING | SURFACE TO GANDALF |
| 4. no template debris | zero | 0 unknown/template names | **PASS** |
| 5. substrate-identity invariant | invariant | 5-element preserved; seasonal_dom=char | **PASS** |

4/5 confirmed PASS. Full gate determination awaits criterion 3 (cohesion judgment from gandalf).

### Season identity

- season_id: season_100001
- anchor: "The Battlefield Where Nothing Grew Back" (ruins_and_forgotten_places)
- element: char (fire-derived battlefield conflagration substrate)
- manifest_version: 1.8
- LLM calls: ~400; estimated cost: ~$3.20

### Gamora handoff note (SMOKE_CLASS_IDS)

`scripts/r1_class_retune_sprint.py::SMOKE_CLASS_IDS` is hardcoded to shipped-catalogue class_ids that don't exist in season_100001. Gamora must switch to metadata-based sampling (one class per archetype_tag group) before running R1 against the regenerated catalogue. Filed in hive log HANDOFF entry.

### Next step

If cohesion criterion PASS: rocket regenerates 4 more seasons (separate follow-on). Seeds 100002-100005.
If cohesion criterion FAIL: gandalf authors follow-on disposition per R2 H1 / R1 Blocker 3 precedent.
