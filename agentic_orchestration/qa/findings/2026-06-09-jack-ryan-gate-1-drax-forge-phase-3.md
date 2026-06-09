# Finding — 2026-06-09 — Drax /forge Phase 3 Two-Layer + Buffer-Space Prototype

**Reviewer:** jack-ryan
**Severity:** PASS-WITH-AMENDMENTS (WARN x3, INFO x3; zero BLOCK)
**Target:** dispatch `agentic_orchestration/dispatches/2026-06-09-drax-forge-phase-3-two-layer-buffer-space-prototype.md` (pre-fire Gate-1)
**Developer:** drax (executor); gandalf (dispatch author)
**Principles applied:** Review Principles 1–5
**Companion docs read:** Phase 2 dispatch (cb2d60d Gate-2 PASS-with-INFO reference), Tal Rasha recognition record, Legolas zodiac-substrate-corpus commission, engineering-disciplines.md §§ 18/18.2/25/41/42, KR OP § 3.11, ADR-004

---

## Verdict

**PASS-WITH-AMENDMENTS**

Three WARNs, three INFOs. No BLOCKs. Dispatch is fire-ready after gandalf addresses the WARNs; drax may begin execution concurrently if gandalf confirms WARN-1 resolution is author-self-applicable (see below).

**Severity matrix:**

| Severity | Count |
|---|---|
| BLOCK | 0 |
| WARN | 3 |
| INFO | 3 |

---

## Findings

---

### WARN-1 — Missing Quality Criterion block (KR OP § 3.11 / Discipline #42)

**Location:** Dispatch top-level structure; the dispatch has § 4 (acceptance criteria) + § 5 (discipline citations) + § 9 (empirical-evidence triggers) but no `## Quality criterion` section in the KR OP § 3.11 template format.

**Concern:** KR OP § 3.11 (Move 1, Matt 2026-05-27 ratification) requires every dispatch Wave 2+ to carry TWO criterion blocks: (1) acceptance criteria and (2) a named quality-criterion section with game-quality goal + refutation conditions. The Phase 3 dispatch carries acceptance criteria and discipline citations but does not surface the named quality-criterion block drax needs for framing-audit Q1-Q3 at dispatch consumption per Discipline #42. The §§ 5 and 9 content is discipline-citation and trigger-routing, not a quality-criterion game-quality statement.

**Note on authoring lane:** This dispatch was authored by gandalf, not KR. The § 3.11 requirement is written as a KR-dispatch discipline. However the effective clause states "retroactive to all Wave 2+ dispatches" with the grandfather clause covering pre-ratification dispatches only. Gandalf-authored dispatches that substitute for KR dispatches inherit the same template requirement for sub-agent consumption discipline to function cleanly.

**Recommended remediation:** Gandalf adds a `## Quality criterion` section (after § 4) carrying:
- **Game-quality goal:** e.g., "validate two-layer + buffer-space spatial architecture in 2D web so UE-port commits rendering resources against an empirically-tested visualization pattern rather than untested design"
- **Refutation conditions:** the standard six from § 3.11 template, plus Phase-3-specific: "Phase 3 results do NOT inform Branch A vs Branch B because they are structurally independent — surface if drax finds spatial-architecture results would require Branch A to validate"

**Routing:** gandalf amendment; does not block drax execution start if gandalf confirms this is a self-serviceable add.

---

### WARN-2 — Acceptance criterion 12 wording is Gate-2-verifiable but narrow (Branch A bleed risk)

**Location:** § 4, criterion 12: "No glyph-as-primitive-anchor implementation (Branch A deferred per Tal Rasha recognition record). How validated: Code review; primitive-anchors are NOT abstract symbolic glyphs in Phase 3."

**Concern:** The criterion correctly fences against glyph-as-primitive-anchor. However, the implementation risk is not only literal-glyph rendering — it is also the INTERACTION MODEL. The Phase 3 lasso includes "sign into the iPad" gesture semantics (§ 1.3 lasso ergonomics), which is the same gesture mechanic that Branch A's Path I (drop-ingredients) surface would employ. A drax implementation of "draw the lasso as a sign gesture" could pre-commit the sign-input-gesture UX interaction model to Branch A's vocabulary even if no abstract glyph VISUAL is rendered. Criterion 12 catches the visual register; it does not catch the interaction-model pre-commitment.

**Recommended remediation:** Gandalf extends criterion 12 (or adds criterion 13) to read: "No glyph-as-primitive-anchor VISUAL implementation AND no sign-gesture-vocabulary interaction model for primitive-anchors (Branch A gesture semantics deferred). Phase 3 lasso is region-selection; the gesture is spatial-selection, not symbol-tracing."

This is a tightening, not a reversal. The §§ 1.3 and 3.2 lasso semantics are already scoped as spatial-selection; the criterion just needs to name the interaction-model constraint explicitly.

---

### WARN-3 — Primitive-anchor curated subset candidates (§ 2.2) are ambiguous on Discipline #41 standing

**Location:** § 2.2 primitive-anchor curated subset; § 5.2 discipline citation.

**Concern:** The dispatch correctly cites Discipline #41 in § 5.2 and declares the curation decision "not fixed in Phase 3." However, the three specific candidate framings offered in § 2.2 — "7 primary elements," "5-7 weapon-form-family clusters," "mixed test set" — are themselves pre-authored alternatives. The dispatch grants drax discretion to "pick one anchor framing for Phase 3 baseline test" without a substrate-emergence-insufficiency rationale for why these three framings were pre-selected over alternatives that could have emerged from the atomic-substrate-registry itself (e.g., frequency-weighted cluster extraction from 37-kit corpus Q18 data, or positional clustering from Phase 2's existing grid layout).

The § 5.2 citation says "Drax tests with curated subset per § 2.2; primitive-curation decision deferred." But "prototype-scoped test set with discretion delegation" requires at least a brief substrate-emergence-insufficiency rationale in the dispatch itself per Discipline #41: why is the candidate framing pre-offered rather than letting the substrate-vector shape the test set selection?

**Recommended remediation:** Gandalf adds a one-sentence #41 rationale to § 2.2 (or § 5.2): "Pre-offered framings are prototype-scoping heuristics, not generative-unit taxonomies; the substrate-emergence-insufficiency rationale is that a substrate-emergent test-set requires Phase B full corpus analysis (post-Legolas), which is out-of-scope for the Phase 3 2D-web visual-pattern test." This rationale is almost certainly correct — it just needs to be stated for drax's framing-audit Q1 to clear cleanly.

---

### INFO-1 — Methodology hotspot timing (#18.2) is correctly applied; no concern

**Location:** § 1.4 + § 5.1.

**Observation:** The dispatch correctly sequences: (a) drax picks baseline (force-directed) + one alternative empirically; (b) elrond methodology consultation fires AFTER Phase 3 surfaces pain per Discipline #18.2 timing refinement. This is the correct extension-hotspot pattern per #18.2. Calling elrond pre-fire would violate the "fires AFTER baseline at extension hotspots" timing refinement. The Phase 2 predecessor already validated force-directed + grid layout at full corpus; Phase 3 is extending that baseline — not starting fresh — so #18.2 timing applies correctly.

**No action required.** Cite for the record that #18.2 is correctly applied here.

---

### INFO-2 — Mobile performance target (60 FPS at 2D web) is sound; note device-variance caveat

**Location:** § 3.4 / criterion 10.

**Observation:** 60 FPS at 2D web layer is the correct performance budget inherited from Phase 2 (which confirmed 60 FPS at 1000-kit LOD architecture). The Phase 3 extension adds primitive-anchor layer nodes but is architecturally a small additional rendering cost at the centroid-dot LOD level. The target is defensible.

**Note for drax:** Phase 3 adds multi-layer rendering (primitive-anchor layer + kit-cluster layer simultaneously), not just a count increase. If the LOD threshold (currently 2.0× normalized zoom from Phase 2) needs recalibration for two-layer simultaneous rendering, that is a close-report observation not a pre-fire blocker. "iPad-class viewport" in criterion 8 should be tested on both iPad-class hardware and DevTools emulation; note that iPad Mini vs iPad Pro performance variance is meaningful at canvas-heavy rendering.

---

### INFO-3 — WS2 downstream composition is referenced but no MIGRATION.md required at Phase 3

**Location:** § 7 composition table; § 9 empirical-evidence triggers.

**Observation:** The dispatch correctly notes Phase 3 findings "inform WS2 (Niagara VFX) commission scope authoring." WS2 is a future commission, not a current consumer with an active interface contract. ADR-004 (MIGRATION.md requirement) fires when a seam change AFFECTS another seam's consumers. Phase 3 is a prototype in `reincarnated-loadout/`; WS2 is a future UE commission. There is no cross-seam API contract being changed here — the Phase 3 → WS2 relationship is informational handoff (drax findings inform a future gandalf-authored commission), not a schema or interface change.

**No MIGRATION.md required at Phase 3.** If Phase 3 produces an interface contract change (e.g., modifies the elrond substrate-trace ingestion contract), a MIGRATION.md would be required at that point. The current dispatch correctly scopes Phase 3 as read-only on elrond's existing packet (§ 2.1).

---

## What I found

The dispatch is structurally sound, architecturally coherent with prior canonical commitments (Tal Rasha recognition record DEFERRED correctly throughout; Branch A fencing is present in §§ 0, 1.4, 5.6, 6, 7, and criterion 12), and correctly applies Discipline #18.2 timing at the methodology hotspot. Phase 2 GREEN state is inherited cleanly. Sub-phase gating (5 Vercel previews at 3.1-3.5) is appropriate smoke-gate density for a 1-3 day wall-clock commission.

Three issues need gandalf attention before drax's framing-audit Q1-Q3 can complete cleanly at dispatch consumption: (1) the Quality Criterion block per KR OP § 3.11 is absent; (2) criterion 12's Branch A fence needs an interaction-model clause to cover gesture-vocabulary pre-commitment, not just visual register; (3) the § 2.2 pre-offered curated subset options need a one-sentence #41 substrate-emergence-insufficiency rationale. All three are authoring amendments — none require architectural reconsideration.

---

## Rationale

- WARN-1: KR OP § 3.11 (Move 1); Discipline #42 (framing-audit at dispatch consumption requires quality-criterion to audit against)
- WARN-2: Review Principle 5 (cross-seam round-trip); Tal Rasha recognition record § 4.4 (Branch A includes sign-gesture interaction model, not only glyph visual); Discipline #42 Q1 (load-bearing framing assumption)
- WARN-3: Discipline #41 (pre-authored taxonomy interrogation; dispatch MUST carry substrate-emergence-insufficiency rationale when pre-offering candidate framings)
- INFO-1: Discipline #18.2 (methodology-consultation timing at extension hotspots — correctly applied)
- INFO-2: D8 (mobile-friendly-from-day-one); Review Principle 2 (smoke-gate adequacy)
- INFO-3: ADR-004 (cross-seam MIGRATION.md scope — not triggered here)

---

## Action

- [ ] Gandalf: Add `## Quality criterion` section per KR OP § 3.11 template (WARN-1)
- [ ] Gandalf: Extend criterion 12 (or add criterion 13) to explicitly fence sign-gesture interaction model from Branch A vocabulary (WARN-2)
- [ ] Gandalf: Add one-sentence Discipline #41 substrate-emergence-insufficiency rationale to § 2.2 for the pre-offered curated subset framings (WARN-3)
- [ ] Matt: No escalation required; all WARNs are within gandalf amendment authority. Dispatch fires post-amendment.

---

## References

- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/dispatches/2026-06-09-drax-forge-phase-3-two-layer-buffer-space-prototype.md`
- `/Users/admin/Games/reincarnated-collaboration/canonical/story/2026-06-09-tal-rasha-glyphic-primitive-anchor-architecture-recognition.md`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/dispatches/2026-06-07-drax-cosmograph-a-b-spike.md` (Phase 2 predecessor; Gate-2 PASS-with-INFO cb2d60d)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/dispatches/2026-06-09-legolas-zodiac-substrate-corpus-mode-b.md`
- `/Users/admin/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` §§ 18, 18.2, 25, 41, 42
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/GOVERNANCE.md` ADR-002, ADR-004
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/operating-procedures/knight-rider.md` § 3.11
