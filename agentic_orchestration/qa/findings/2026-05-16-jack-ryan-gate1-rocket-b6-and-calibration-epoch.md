# Finding — 2026-05-16 — Gate 1: rocket B6 pre-work + calibration epoch declaration

**Reviewer:** jack-ryan
**Severity:** PASS WITH FLAGS — INFO (x2), WARN (x1)
**Target:** PENDING dispatch + PENDING decisions-log entry (held on this review + Matt approval)
**Developer:** knight-rider (dispatch author), rocket (implementer)
**Principles applied:** Review Principles 1, 2, 4; Disciplines #1, #2, #11, #12; ADR-002, ADR-004

---

## VERDICT: PASS WITH FLAGS

Both artifacts are structurally sound and internally consistent. No blocking issues. Three flags below — one WARN (math arithmetic gap), two INFOs (hunter partial-shift framing, star-lord cascade underspecification). Matt approval can proceed.

---

## Artifact 1 — Rocket dispatch (B6 pre-work: energy-type-aware tier assignment)

### Flag 1 — WARN: 1.7× multiplier derivation has an arithmetic gap

**What I found:** The dispatch cites gamora's §4.3 combined factor as ~2.4–3.3× (from three factors: startup ~1.5–2.0× + miss ~1.18× + armor ~1.23×). But the math note §4.3 actually computes: `1.5–2.0 × 1.18 × 1.23 ≈ 2.2–3.0×` — not 2.4–3.3×. The dispatch also notes the observed ratio is 5.5× but generation can only address the structural portion, not the gauntlet-distribution residual. The 1.7× working multiplier is offered without an explicit derivation from these numbers. The dispatch says it "targets the sim-mechanical portion only" but doesn't state the reasoning: i.e., the gen-controllable lever is tier magnitude (not startup or miss rate), so the 1.7× is not the full 2.2–3.0× factor but a partial correction sized to move the epoch in the right direction without overcorrecting.

**Issue:** Step 0 instructs rocket to "verify gamora's 1.7× compensation factor." But gamora's math note does NOT derive 1.7× explicitly — it proposes it as an approximate target in the findings narrative ("Rage/physical archetypes need ~1.5–2× higher skill tier baseline… Approximate targets: rage/physical tier 38–65 (proposed; ~1.7× higher)"). The math note §4.3 table shows factors that yield 2.2–3.0×. Rocket will not find a clean derivation of 1.7× in §4.3 — and Step 0 asks rocket to "confirm the 1.7× factor" from that section specifically.

**Risk:** Rocket reads §4.3, finds 2.2–3.0×, and concludes 1.7× is unsupported — then either (a) proposes 2.5× which may overcorrect, or (b) flags and waits, costing a round-trip.

**Recommendation:** Add a clarifying sentence to Step 0 (or the math instruction in Step 1.1) explaining the derivation gap: the 2.2–3.0× combined sim-mechanical factor cannot be fully corrected at the generation tier level because rage startup and miss rate are not tier-addressable; tier magnitude only affects damage output per hit, not hit frequency or startup timing. Therefore the generation-controllable compensation is a partial correction; 1.7× is a reasoned lower-bound estimate leaving deliberate headroom for B14.5 V2 to close the remainder. Rocket's math note should explicitly document this rationale as part of Step 1 (factor → multiplier mapping).

**Cite:** Discipline #1 (math-before-code — the math note must be derivable, not just assertable).

---

### Flag 2 — INFO: Hunter partial-shift framing is open, not pre-answered

**What I found:** The dispatch correctly identifies hunter as "partial shift" territory (miss-rate only, no rage startup or melee positioning) and leaves the recommendation to rocket. This is appropriate. However, the dispatch frames it as an open question without giving rocket the key datum to anchor the answer: hunter's avg modifier across 7 seasons is 0.594 — the closest archetype to the 0.85–1.15 band — and it carries only the ~1.18× miss-rate factor. A naive application of 1.7× to hunter would likely overshoot. The data is in the findings file but is not foregrounded in the hunter question paragraph of the dispatch.

**Risk:** Low. Rocket reads the required reading (gamora findings file) and will see the 0.594 figure. But the dispatch could save a diagnostic step by surfacing it.

**Recommendation:** In the Open Questions section, Question 1 (hunter shift), add the datum parenthetically: "hunter avg modifier 0.594 across 7 seasons (closest to target band); only the miss-rate factor (~1.18×) applies — partial shift or none may be appropriate."

**Cite:** Discipline #11 (attribution clarity — relevant context should be present where the decision is being made).

---

### Cross-seam boundary and MIGRATION.md guidance — PASS

The dispatch's MIGRATION.md guidance is correct: required only if simulation-side consumers read tier values directly via schema (schema-visible change), not required if values shift within existing field semantics. This is the right application of ADR-004. No issue.

### Discipline #12 (energy_type as a new semantic axis) — PASS

Attribution is clean. The dispatch explicitly names energy_type as a "meaningful generation axis" after this change and cites Discipline #12 in required reading. Step 2 adds energy_type as a parameter on the archetype template structure — this is a semantic expansion, not a silent semantic shift. The framing is correct.

### Math-before-code application (Discipline #1) — PASS with the WARN above

Step 0 + Step 1 correctly gate code on a math note. The structure is right; the WARN above addresses a derivation gap inside that gate.

### Experimental archetype exclusion — PASS

Excluding experimental from the tier shift is correct per `project_trait_architecture.md` (experimental classes don't roll trait affixes; outlier territory is intentional). The dispatch explains the exclusion. No issue.

---

## Artifact 2 — Decisions-log entry (calibration epoch declaration)

### Distinct-entry justification — CONFIRMED

Knight-rider's read is correct: this deserves its own entry. The View A lock + divergence framework entry addresses fight-outcome philosophy and the multi-dimensional monitoring framework. This entry addresses the CALIBRATION BASELINE that framework reads against — specifically, that the operational anchor is mean |mod-1.0| ≈ 0.82 at the B10.4 Option 2 epoch, NOT the aspirational 0.85–1.15 band. These are separable concerns. The baseline declaration also sets up rocket's cascade explicitly, which would be awkwardly co-mingled in the stewardship entry. Confirmed: distinct entry, correct structure.

### Discipline #12 compliance — PASS

The entry cleanly separates two semantics throughout: (a) B10.4 Option 2 convergence semantic (non-pack WR = 50%, CONVERGED non-experimental classes, mean |mod-1.0| ≈ 0.82) vs (b) the file 29 aspirational band (0.85–1.15, pre-gauntlet, pre-B14.5, no specific convergence semantic). The metric is locked correctly as `mean |modifier - 1.0|` per the defined convergence semantic. I find no conflation in the entry body.

One observation: the entry states the tracking metric at non-pack WR = 50% "per convergence semantic." The reader needs to know this is the B10.4 Option 2 semantic specifically. The entry does state this in the decision heading and table. No action needed — this is belt-and-suspenders language and is already correct.

### Alternatives section — PASS, with one minor gap noted (INFO)

The four alternatives are well-reasoned and the rejection logic is sound. One minor gap:

**Flag 3 — INFO: Alternative (d) rejection missing the "both needed" rationale**

The entry says convergence WR and modifier range are "orthogonal information." This is correct but the sentence reads as an assertion without grounding it. A reader unfamiliar with the divergence framework might ask: "why orthogonal?" The entry could add one phrase: "convergence WR tells you whether balance landed; modifier range tells you WHERE it landed and how the current energy-system mechanical gap expresses across archetypes — two independent dimensions of the same balance state." This makes the rejection crisp rather than asserted.

**Cite:** Discipline #12 (semantic-shifting — the orthogonality claim is a semantic claim; brief grounding helps).

---

### Cross-seam cascades — PASS with one addition

The cascade list is complete for the confirmed work. One observation: the list omits gamora's CURRENT seam work. If a gamora task is active during the period between this entry landing and B6 pre-work landing, gamora's smoke-test output would show modifier values in the 0.09–0.52 range — and a future gamora session should know that the B10.4 calibration epoch is the active reference, not the 0.85–1.15 band. This isn't missing from the entry (the jack-ryan cascade entry covers it implicitly), but if a gamora self-validation step checks modifiers, the gamora seam prompt should reference this entry.

This is an INFO for future gamora dispatch wiring, not a gap in this entry.

---

## Summary of flags

| # | Severity | Artifact | Issue |
|---|---|---|---|
| 1 | WARN | Dispatch Step 0 | 1.7× multiplier lacks explicit derivation from §4.3; dispatch asks rocket to "verify" a number gamora derived narratively, not from the §4.3 table |
| 2 | INFO | Dispatch Open Q1 | Hunter question missing the 0.594 anchor datum; minor friction for rocket |
| 3 | INFO | Decisions-log Alt (d) | Orthogonality claim asserted, not grounded; one phrase would make it crisp |

## Action required before dispatch activation

- [ ] Knight-rider: Address Flag 1 — add derivation-gap note to dispatch Step 0 / Step 1 explaining why 1.7× is a partial correction (not the full 2.2–3.0× sim factor) and why that is intentional. Rocket's math note documents the full chain.
- [ ] Knight-rider (optional but recommended): Address Flags 2 and 3 — small wording additions.
- [ ] Matt: Review and approve both artifacts for execution.

No BLOCK issues. Both artifacts ready for Matt approval after Flag 1 is addressed.

---

## References

- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/dispatches/2026-05-16-rocket-b6-pre-work-energy-type-aware-tiers.md`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/qa/pending/2026-05-16-decisions-log-calibration-epoch.md`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/qa/findings/2026-05-16-gamora-modifier-range-rootcause.md`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/math/modifier-range-root-cause.md`
- `/Users/admin/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/GOVERNANCE.md`
