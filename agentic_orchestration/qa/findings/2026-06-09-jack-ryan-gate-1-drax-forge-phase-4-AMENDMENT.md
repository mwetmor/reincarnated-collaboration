# Finding — 2026-06-09 — drax forge-phase-4-AMENDMENT (Gate-1 DESIGN-MODE)

**Reviewer:** jack-ryan
**Severity:** PASS-WITH-AMENDMENTS (0 BLOCK; 2 WARN; 3 INFO)
**Target:** dispatch `agentic_orchestration/dispatches/2026-06-09-drax-forge-phase-4-AMENDMENT-rune-per-group-two-tier.md`
**Developer:** drax (executor); gandalf (dispatch author)
**Principles applied:** Principle 1 (math-before-code), Principle 2 (smoke-gate), Principle 3 (design-consistency), Principle 4 (cross-seam impact), Principle 5 (scope-honesty)

---

## Verdict: PASS-WITH-AMENDMENTS

Dispatch is well-structured. Architecture is coherent. Discipline citations (#18/#18.2, #25, #40, #41) are present and substantively correct. All Phase 3 baselines are explicitly preserved. Scope supersession is cleanly drawn (original § 1.3, § 1.4, criteria #3/#5/#6 superseded; everything else carried forward).

Two WARNs surface — neither is a BLOCK, but both should be resolved before drax fires. Three INFOs are for the record.

---

## Per-Finding

### WARN-1 — Quality Criterion § 4.5: Phase-4-amended-specific refutation condition is structurally sound but under-specified

**Severity:** WARN
**Location:** § 4.5 (Quality criterion), final bullet of refutation conditions

**Finding:** The amended-specific refutation condition reads: "Phase 4 amendment results do NOT inform canonical Branch A commitment because two-tier complexity at 2D web is structurally insufficient to be predictive of iPad UE-port ergonomic; surface if Phase 4 cannot validate enough of the rune-per-group + two-tier pattern."

This is the right concern. However, it does not name what "enough" means. The original Phase 4 dispatch had a parallel condition ("Phase 4 results do NOT inform canonical Branch A commitment because they are structurally insufficient") and it was similarly thin. In Gate-2 the acceptance criteria carried the weight — but here Tier 2 is scoped to "at least 2-3 groups (Elements + Movement minimum)" (criterion 6 / § 3.3), meaning Phase 4 could GREEN with Tier 2 only partially realized. A reviewer reading § 4.5 needs a falsifiable threshold: under what conditions does drax surface this refutation condition?

**Suggested remediation:** Add one sentence to the refutation condition naming the minimum Tier-2 coverage for the empirical-validation claim to hold. Example: "If Tier 2 functional for fewer than 2 groups at Phase 4 close, or if rune-selection mechanism is tap-only alpha (never prototyped gesture), surface this condition — two-tier pattern is under-validated for canonical Branch A commitment." The threshold can be low; it just needs to be stated.

**Cite:** Discipline #18 (math-before-code, applies to quality-criterion empirical-sufficiency as well as algorithm choice); Principle 5 (scope-honesty).

---

### WARN-2 — Criterion 11 carries YELLOW 3 re-validation scope, but rune-anchor geometry change is materially larger than glyph-anchor geometry change

**Severity:** WARN
**Location:** Acceptance criterion 11; § 1.1 visual register spec

**Finding:** Criterion 11 ("classifyLasso() scaffold thresholds re-validated against rune-anchor geometry") carries forward Phase 3 YELLOW Observation 3 correctly. However, the rune-per-group amendment changes the anchor geometry more substantially than the original Phase 4 would have. Original Phase 4 had 8 anchors (per-primitive); amended Phase 4 has 6 group-runes (per-group). The "large + atmospheric behind primitive cluster" visual register means the rune does NOT occupy a bounded canvas at a distinct anchor position the way a figurative nebula or compact glyph would — it looms as a background presence framing the cluster region. This is a spatial footprint change that `classifyLasso()`'s `within_anchor_centroid_threshold`, `nearby_anchor_threshold`, and `cross_buffer_min_lasso_radius` constants were NOT calibrated against.

The dispatch names this in criterion 11 ("re-validated against rune-anchor geometry") but does not flag it as a YELLOW carry-in at higher-than-original severity. The spatial change from "bounded glyph" (original Phase 4) to "atmospheric background rune" (amended Phase 4) could produce lasso threshold misclassification that bounded-canvas geometry would not.

**Suggested remediation:** Drax should flag in the Phase 4.1 close-report subsection that `classifyLasso()` re-validation priority is elevated vs Phase 3 YELLOW 3 framing, because the rune's diffuse spatial footprint is architecturally different from a bounded-canvas anchor. If the spatial footprint is actually bounded (i.e., rune render stays within a bounded region despite the "atmospheric" descriptor), drax should document the bounding box at Phase 4.1. This is a WARN, not a BLOCK — drax can address at Phase 4 close report as long as the elevation is flagged going in.

**Cite:** Discipline #11 (empirical inspection over assumption); Discipline #40 (scaffold-value honesty — threshold values were calibrated against specific geometry; geometry change triggers re-audit).

---

### INFO-1 — Discipline #41 rationale in § 5.2: tight enough, but weakened by absence of substrate-emergence-insufficiency argument

**Severity:** INFO
**Location:** § 5.2 (Discipline #41 rationale)

**Finding:** § 5.2 correctly states that the 6-group scaffold is "drax-discretion-substitutable" and that canonical group lock is DEFERRED to Pattern B. However, Discipline #41 (pre-authored taxonomy interrogation) asks not just "is this scaffold-flagged?" but "is there a substrate-emergence-insufficiency justification for the scaffold?" The dispatch does not explain WHY the atomic-substrate-registry (20 primitive families + Layer 0.5 operator) cannot directly supply the group taxonomy, requiring gandalf to pre-offer 6 groups. The § 1.2 table offers groups (Elements / Movement / Combat geometry / Resource / Attributes / Mechanic-altering) without saying whether those emerged from substrate analysis or were pre-authored by gandalf for prototype convenience.

For a Gate-1 INFO, not a WARN, because: (a) the scaffold is correctly flagged; (b) the canonical lock is correctly deferred; (c) Matt's verbatim refinement itself named examples that land naturally in the 6-group taxonomy (water drop, lightning bolt for Elements; jumping man, teleport man for Movement). The groups are reasonably substrate-adjacent. But the dispatch would be stronger if § 5.2 added one sentence: "6-group scaffold is a prototype convenience grouping of the 20-primitive-family atomic-substrate-registry; substrate cannot directly supply the group taxonomy pre-Phase-4 because canonical primitive-curation (which 12-20 of 20 primitives are visible) is itself deferred; groups are authoring convenience at drax-implementation granularity."

**Cite:** Discipline #41 (pre-authored taxonomy interrogation — substrate-emergence-insufficiency justification). INFO only.

---

### INFO-2 — § 6 out-of-scope is comprehensive; one minor gap noted

**Severity:** INFO
**Location:** § 6

**Finding:** The out-of-scope list is thorough and preserves the original Phase 4's items cleanly. One scope-creep gap worth noting: the dispatch introduces `visual_render_spec` as a new field in the per-rune data structure (§ 2.2) without stating whether this field's canonical contents (light-edge brush-stroke render parameters) are scaffold-with-pending-decision or locked. Given the dispatch correctly defers canonical rune-per-group lock to Pattern B, `visual_render_spec` contents are implicitly also scaffold — but this is not made explicit. A reader might interpret the § 1.1 visual register spec as canonical lock on render parameters when it is Matt's design direction, not a canonical lock.

**Suggested remediation:** One line in § 6 suffices: "Canonical `visual_render_spec` render parameter values (brush-stroke weight, light-edge intensity, atmospheric scale) — scaffold per drax discretion at Phase 4; Pattern B session." Or add to § 5.4 Discipline #40 list.

**Cite:** Discipline #40 (scaffold-with-pending-decision flagging).

---

### INFO-3 — MIGRATION.md: correctly not triggered; confirm

**Severity:** INFO
**Location:** cross-seam scope

**Finding:** Phase 4 AMENDMENT is loadout-seam-only. No engine seam touch. No telemetry interface change. No cross-seam schema change. ADR-004 MIGRATION.md trigger does NOT fire. This is the correct call and matches the Phase 3 precedent (Gate-2 verified no cross-seam impact at `c757964`). Noting for the record only.

**Cite:** ADR-004 (cross-seam MIGRATION.md requirement). Confirmed not triggered.

---

## Specific concern audit (A through J per briefing)

| Concern | Verdict |
|---|---|
| A) § 4.5 Quality Criterion — standard + amended-specific refutation conditions | WARN-1 — condition present but threshold unstated |
| B) 12 acceptance criteria refit — adequate Gate-2 surface? Criterion 11 carry-forward | WARN-2 — criteria are adequate in count; WARN on lasso re-validation elevation |
| C) Discipline #40 scaffold-values in § 5.4 — all 5 flagged? | PASS — all 5 present; INFO-2 adds 6th (visual_render_spec) |
| D) Discipline #41 § 1.2 group-scaffold substrate-led rationale tightness | INFO-1 — rationale present; substrate-emergence-insufficiency argument thin |
| E) Discipline #25 § 5.3 per-rune semantic match responsibility | PASS — gandalf semantic review at Vercel preview milestones named; audit responsibility clear |
| F) Discipline #18.2 hotspot timing — § 5.1 Tier 1 gesture-recognition | PASS — post-baseline consultation timing correctly stated |
| G) Out-of-scope § 6 — rune-per-group scope-creep gaps | INFO-2 — visual_render_spec parameter lock not explicitly deferred; minor |
| H) Phase 3 baseline composition (§ 1.4 + criterion 7) | PASS — all Phase 3 GREEN patterns explicitly preserved in § 1.4 and criterion 7 |
| I) Elrond Hotspot A composition — force-directed as production default | PASS — § 7 composition table names this correctly; aligns with elrond recommendation |
| J) MIGRATION.md for Phase 4 AMENDMENT | PASS — INFO-3 for record; correctly not triggered |

---

## Severity matrix

| Severity | Count |
|---|---|
| BLOCK | 0 |
| WARN | 2 |
| INFO | 3 |

---

## Actions

- [ ] **gandalf (WARN-1):** Add falsifiable minimum-Tier-2-coverage threshold to § 4.5 amended-specific refutation condition before drax fires. One sentence; low-effort.
- [ ] **gandalf or drax (WARN-2):** Add note in Phase 4.1 sub-phase (§ 3.1) or criterion 11 that `classifyLasso()` re-validation priority is elevated due to rune's diffuse/atmospheric spatial footprint vs bounded-canvas anchor; drax to document bounding box at Phase 4.1 close.
- [ ] **gandalf (INFO-1):** Optional — one sentence in § 5.2 explaining substrate-emergence-insufficiency for the 6-group scaffold. Not blocking; strengthens discipline compliance.
- [ ] **gandalf (INFO-2):** Add `visual_render_spec` render parameter values to § 5.4 Discipline #40 scaffold list OR add one line to § 6. Not blocking.
- [ ] **jack-ryan:** Decisions-log entry for two-layer + buffer-space validated architecture fired in Item B this session.

---

## References

- `agentic_orchestration/dispatches/2026-06-09-drax-forge-phase-4-AMENDMENT-rune-per-group-two-tier.md` — primary review target
- `agentic_orchestration/dispatches/2026-06-09-drax-forge-phase-4-substrate-led-glyph-anchor-prototype.md` — original Phase 4 (superseded scope)
- `canonical/story/2026-06-09-tal-rasha-glyphic-primitive-anchor-architecture-recognition.md` — Branch A architecture authority; § 4 commitments
- `agentic_orchestration/qa/findings/2026-06-09-jack-ryan-gate-2-drax-forge-phase-3-close.md` — Phase 3 Gate-2 PASS-WITH-INFO (INFO-1 residual `outer_glow_radius` + decisions-log recommendation)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Disciplines #11, #18, #18.2, #25, #40, #41 cited
