# Dispatch — 2026-05-26 — jack-ryan — Cycle 13 SC-2 + SC-3 Discipline Canonical Work

**From:** knight-rider
**To:** jack-ryan
**Approved by:** Matt 2026-05-26 (via Cycle 13 framing brief Q4 ratification — sidecar list + KR autonomous scope per § 4.1 + skip-confirmation per Q11)
**Estimated effort:** 3-6 hrs canonical authoring
**Acceptance:** 5 new disciplines (#26-#30 or appropriate numbering) landed in `engineering-disciplines.md` + Discipline #23 amendment with 3rd operational instance; tagged commit

## Context

Doc 40 (Cycle 13 architectural foundation, 2026-05-26) surfaced 5 engineering-discipline candidates in § 12.1 awaiting jack-ryan ratification. These are async / non-blocking — they don't gate any Cycle 13 wave fire, but their adoption is needed before they can be cited downstream. Bundling SC-2 (5 candidates) + SC-3 (Discipline #23 amendment) into a single jack-ryan dispatch reduces context-load overhead.

This is canonical-authoring work — jack-ryan's seam per ground-state § 4 first-reads. No production code; pure canonical text.

## Required reading before starting

1. `canonical/00-ground-state.md` (current epoch + canon-status table)
2. `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (current authoritative source; 25 disciplines + amendments; adopt format / numbering / when-to-cite trigger / R-prescriptions pattern)
3. `canonical/40-gear-balance-guide-architecture-2026-05-26.md` § 12.1 (5 candidate disciplines source) + § 1.4 (3rd operational instance for Discipline #23)
4. `canonical/40-gear-balance-guide-architecture-2026-05-26.md` § 8 (D61 playability) + § 8.9 (D76 dual-effect + D78 spirit-guide-pacing + D79 commitment-to-consequence) + § 8.11 (D84 sim methodology naming)
5. `agentic_orchestration/operating-procedures/jack-ryan.md` (DESIGN-MODE for canonical-write decisions)
6. `agentic_orchestration/operating-procedures/engineering-disciplines.md` (cross-cutting reference skill wrapping the 25 disciplines)
7. `agentic_orchestration/operating-procedures/decision-log-format.md` (composition reference; disciplines compose with decisions-log via cross-citation)

## Math-before-code (canonical-authoring; no code)

NOT applicable — canonical-doc work only.

## Cross-seam contract change? (Principle 6 gate)

**Round-trip: not applicable — no cross-seam contract change in this dispatch.** Disciplines are referenced by other agents at execution time; no schema / fixture / boundary mutation.

## Scope

### SC-2: 5 candidate disciplines from doc 40 § 12.1

For each, author canonical entry per existing format (summary + when-to-cite + named patterns + R-prescriptions cross-reference where applicable + source-of-record):

- [ ] **D61 Playability discipline** — PLAYABLE-AND-IN-BAND as the validation criterion (KPM in band + coherent rotation + resource flow + uptime + non-degenerate + cognitive load manageable). Source: doc 40 § 8.10. Composes with #18 methodology-before-execution at Phase 3 sim. Affects Cycle 13 Wave 4-5 sim cycling.
- [ ] **D76 Dual-effect capstone discipline** — T4 capstones MUST produce dual mechanical impact (character-wide effect + within-chain or parallel-chain effect). Source: doc 40 § 8.9 + § 8 D81. Composes with #20 row-duplication prohibition (similar "no degenerate single-effect" pattern). Affects Cycle 13 Wave 2-3 T4 algorithm implementation.
- [ ] **D78 Spirit-guide-pacing discipline** — spirit-guide voice = NEUTRAL OBSERVATION / data-oracle, NOT counselor (D28); language = "projected to / typically / estimated" (D31 honesty). Source: doc 40 § 8.9 + § 5. Affects Cycle 14 Phase 5 spirit-guide data-oracle integration.
- [ ] **D79 Commitment-to-consequence discipline** — decisions land with consequence; no free reversibility. Compose with substrate-led discipline + balance-as-property (D1). Source: doc 40 § 8.9. Apply throughout Cycle 13+ wave decisions.
- [ ] **D84 Sim methodology naming discipline** — when authoring sim methodology for multi-T4 / multi-cohort / multi-progression-node validation, name the methodology pattern explicitly (e.g., "hybrid cohort + edge-case sampling with per-legendary cohort anchoring"). Source: doc 40 § 8.11. Composes with #18 methodology-before-execution. Affects Cycle 13 Wave 4 gamora methodology consultation.

### SC-3: Discipline #23 amendment

- [ ] Amend `engineering-disciplines.md` Discipline #23 (framing-audit checklist Pattern A-deep three-question protocol) with 3rd operational instance:
  - **3rd instance source:** doc 40 § 1.4 — auto-combat correction caught during canonization (Matt 2026-05-26 surfaced "auto-combat is mobile-variant deferred option only; PRIMARY game retains conventional execution mechanics"; canonical framing in doc 40 § 1 corrected mid-authoring before drift propagated)
  - **Pattern:** load-bearing framing assumption (auto-combat as primary execution) surfaced via Matt-applied framing-audit during doc 40 authoring; correction landed in same authoring session
  - **Lesson:** framing-audit during canonical authoring (not just at Pattern A-deep verdicts) catches load-bearing assumptions before they ossify in canon
  - **Existing 1st + 2nd instances:** verify existing entries cite their sources correctly; add 3rd as continuation of pattern

### Discipline numbering protocol

- Assign next available numbers (#26 onward) in order: D61 → #26 Playability; D76 → #27 Dual-effect capstone; D78 → #28 Spirit-guide-pacing; D79 → #29 Commitment-to-consequence; D84 → #30 Sim methodology naming.
- If numbering collision with concurrent jack-ryan work, adjust + flag in completion record.
- Update agentic_orchestration/operating-procedures/engineering-disciplines.md wrapper skill to reflect new disciplines (one-line summary + when-to-cite trigger).

## Acceptance criteria

- [ ] All 5 candidate disciplines authored in `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` per existing format
- [ ] Discipline #23 amended with 3rd operational instance
- [ ] `agentic_orchestration/operating-procedures/engineering-disciplines.md` updated with new discipline entries (one-line summary + when-to-cite trigger)
- [ ] `canonical/00-ground-state.md` § 1 row for engineering-disciplines.md updated to reflect new disciplines + amendment (e.g., "25 → 30 + #23 3rd-instance amendment")
- [ ] Each new discipline references its source decision (D61 / D76 / D78 / D79 / D84)
- [ ] Tagged commit per jack-ryan convention (`jack-ryan: engineering-disciplines amendment — Cycle 13 SC-2 + SC-3 candidates landed`)
- [ ] Round-trip: not applicable — no cross-seam contract change

## Out of scope (explicit non-goals)

- Authoring NEW disciplines beyond the 5 candidates + #23 amendment (any additional candidates surfaced during read should be FLAGGED, not authored, this dispatch)
- Modifying existing disciplines #1-#22, #24-#25 (only #23 amendment + new #26-#30 additions)
- decisions-log entries (separate jack-ryan work; if surfaced, capture as flag only)
- Production code modifications

## Open questions for the agent to resolve

- Numbering — confirm #26-#30 is appropriate, OR if concurrent jack-ryan work has consumed those numbers, adjust + note
- Format — current disciplines vary slightly in format depth; pick consistent depth for new entries matching the closest analogue (D61 mirrors discipline-as-validation-criterion pattern of #1.2 code-citation; D84 mirrors named-pattern-with-when-to-cite trigger pattern)
- R-prescription cross-references — identify which (if any) of the new disciplines deserves R-prescription association; if none, skip cleanly

## References

- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` § 12.1 (5 candidates source) + § 1.4 (3rd instance source) + § 8.9-8.11 (substantive decisions)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (current state; 25 disciplines + amendments)
- `agentic_orchestration/gandalf/notes/2026-05-26-cycle-13-framing-brief.md` § 5 SC-2 + SC-3 (this dispatch's authority basis)
- `agentic_orchestration/operating-procedures/jack-ryan.md` (DESIGN-MODE canonical-write authority)

---

**Cycle:** 13
**Wave:** 0 / Sidecar
**Gates:** none (async / non-blocking)
**Priority:** P2 — fire parallel with SC-4

---

## Completion record

**Completed:** 2026-05-26
**Agent:** jack-ryan
**Commit:** see tag `jack-ryan: engineering-disciplines amendment — Cycle 13 SC-2 + SC-3 candidates landed`

### Disciplines landed

**SC-2 — 5 new disciplines (#26-#30):**
- **#26 — Playability discipline (D61):** PLAYABLE-AND-IN-BAND as the sim validation criterion; 6-gate checklist (KPM + rotation coherence + resource flow + defensive uptime + no-degenerate-states + cognitive-load); composes with Discipline #18 at Phase 3/4 gamora consultation
- **#27 — Dual-effect capstone discipline (D76):** T4 capstones MUST produce dual mechanical impact (character-wide effect AND within-chain or parallel-chain effect); BLOCK trigger at Gate-1 for any single-effect capstone definition
- **#28 — Spirit-guide-pacing discipline (D78):** NEUTRAL OBSERVATION / data-oracle voice pattern with three required language markers (projected to / typically / estimated); WARN trigger for counselor-voice violations; composes with D65 respec-offer pacing mechanism
- **#29 — Commitment-to-consequence discipline (D79):** no free reversibility on commitment-class decisions; escape valves (standard revert cost) permitted but free reversibility prohibited; WARN trigger for free-revert implementations; composes with #28
- **#30 — Sim methodology naming discipline (D84):** methodology patterns must be named explicitly at math hotspots (four-axis naming: node-population + edge-case + cohort + compute-burden); composes with #18; WARN trigger for structurally-described-but-unnamed methodology

**SC-3 — Discipline #23 amendment:**
- Added **3rd operational instance:** auto-combat framing inherited from `skills_and_gear_discussion` source conversation; Matt corrected at line 2420; framing-audit caught DURING canonization of doc 40 § 1 (not post-hoc); lesson: framing-audit applies to canonical-doc authoring from external-conversation source material
- Added **2nd operational instance** inline (previously only cited in first-canonical-example note; now explicit as numbered instance): drax "requires no work" understatement caught during SO-3 Pattern A-deep verdict authoring 2026-05-25
- Added **1st operational instance** inline (previously described in main discipline statement; now explicit as numbered instance): Phase E-1 kernel-panic / gandalf ratification failure (Pattern-A query refuted H1-H5 availability assumption in ~120 sec)
- Extended "when to cite" to include: "canonical-doc authoring that inherits framing from external-conversation source material"

### Cross-updates made

- `agentic_orchestration/operating-procedures/engineering-disciplines.md` wrapper skill: updated IS-statement from 20 to 30 disciplines; updated § 1 table from 20 to 30 rows (new rows #20-#30 with correct names — prior table showed 20 but was missing #21-#25 which had been added 2026-05-23)
- `canonical/00-ground-state.md` § 1 row for engineering-disciplines.md: count updated 25 → 30; #26-#30 names listed; #23 3rd-instance amendment noted; CURRENT status updated with commit reference placeholder

### Numbering confirmation

No collision found. #26-#30 were unoccupied. Assignment order matches dispatch spec: D61→#26, D76→#27, D78→#28, D79→#29, D84→#30.

### R-prescription check

No new R-prescriptions authored in this dispatch. Disciplines #26-#30 carry Gate-1 trigger questions but operate within the existing R-prescription framework (R11(b) cross-seam round-trip covers any schema changes these disciplines would flag).

### Key citations

- Source: `canonical/40-gear-balance-guide-architecture-2026-05-26.md` § 8.8/#8.10 (D61 → #26), § 8.9 (D76 → #27, D78 → #28, D79 → #29), § 8.11 (D84 → #30), § 1.4 (D47 → #23 3rd instance)
- Authority: Matt 2026-05-26 (via doc 40 session + Cycle 13 framing brief Q4 ratification)
- Acceptance criteria: all 5 checked; #23 amendment checked; wrapper skill updated; ground-state row updated
