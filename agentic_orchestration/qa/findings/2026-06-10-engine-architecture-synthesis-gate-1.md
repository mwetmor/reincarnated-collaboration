# Finding — 2026-06-10 — engine-architecture-canonical-synthesis (Fable-5 Phase 1)

**Reviewer:** jack-ryan
**Mode:** Gate-1 critique-pair (DESIGN-MODE), adversarial read — QA half of the Fable-5 Phase-1 eval signal
**Severity:** INFO (no WARN, no BLOCK)
**Verdict:** **PASS**
**Target:** `canonical/story/2026-06-10-engine-architecture-canonical-synthesis.md` (STATUS: CURRENT pending Gate-1)
**Developer:** gandalf (story-and-design steward)
**Principles applied:** Review Principle 4 (decisions-log / source single-source-of-truth); Discipline #11 (empirical inspection over assumption); Discipline #42 (framing-audit); Discipline #51 (synthesis-draft adversarial critique pre-lock — the discipline this doc routes itself through)

---

## Method-compliance pre-check (the doc's own claim)

The header claims a canonical-source-consultation declaration committed before reads + all 33 sources read in full + per-block working notes. **Verified present:**
- Checklist `agentic_orchestration/gandalf/notes/2026-06-10-fable-5-canonical-synthesis-source-consultation-checklist.md` exists (98 lines); enumerates 33 sources (A1-6 / B1-11 / C1-3 / D1-9 / E1-4 = 6+11+3+9+4); all boxes ☑; declares ground-state-oracle as orientation-only (E4) — the explicit guard against the 2026-06-10-morning failure pattern.
- Working notes `…-fable-5-synthesis-working-notes.md` present (358 lines).
- Header cites pre-read commit `dfe168f` for the declaration. Method claim is substantiated.

---

## Charge 1 — Citation-fidelity spot-checks

**What I checked:** pulled 7 load-bearing claims and verified the cited § against source.

| Claim (synthesis §) | Cited source | Result |
|---|---|---|
| §3.6 BC axes 68,040 cells; axis factorization 6×5×3×3×3×3×4×7 | bc-axes-lock §2/§3 (lines 14, 79, 585) | ✅ exact; axis enumeration matches |
| §3.6 Profile-A operational archive 25,920 (post sim-deferral) | bc-axes-lock (line 693 `= 25,920 cells`) | ✅ exact |
| §4.4 weapon v1_scope locked **2,293**, within ~1,700–3,100 estimate, tag `v1.0-weapon-substrate-cycle-10-shipped` | roadmap §3 (line 66/109); composition-policy §1.7 (line 106); D1a=449 (line 98) | ✅ exact, incl. tag + estimate band |
| §5.1 Path-α v1 closure C1+C2+C3+C5=4/4, C4 dropped→Cycle 16+ | doc 51 §10.8.10 (lines 1365-1369); doc 50 §4.7 | ✅ exact, incl. C1 BASE-CONTEXT/DDA-off + Matt A1 election |
| §5.3 DDA = Disc #39 Mode-B scaffold w/ **explicit Cycle 15 retirement commit**, Matt D5 | doc 50 §4.7 v1.2 (line 274) | ✅ **verbatim** match |
| §5.4 T4 layered-vocabulary table (3/7/11/21/C1-C5) canonically disambiguated | doc 47 §4.6.9 (line 748); 7 = 6 + DUAL_ELEMENT_ADDITION | ✅ disambiguation point exists; 6+1=7 confirmed |
| §3.1 Architecture A: 100 rotating + 9 physical = **109** | flavor-pool-lock §0/§2.9 (lines 33, 130, 143) | ✅ exact — and uses the **post-amendment-corrected** 109 (not pre-correction 118) |

**Finding:** 7/7 verified exactly. No misattribution. Notably the §3.1 count reflects the 2026-06-01 amendment-pass correction (109 not 118) — a memory-based synthesis would likely have carried the stale number; this confirms current-source reads, not oracle one-liners. **Severity: none.** Charge 1 PASS.

---

## Charge 2 — Stress-test "Contradiction count: zero" (§9 + §0)

**What I checked:** the four named reconciliations the charge flagged, hunting for one that papers over a genuine unresolved tension.

- **§3.8 Architecture A→B.** "Substrate-agnostic" (A, convergence-input layer — mechanical convergence element-blind) vs "substrate-bound at Phase 2" (B, generation-binding layer). These are genuinely different layers; binding ≠ convergence input; A retained as R&D/dev-tool ref per doc 37 amendment. **Genuine distinction, not papering.**
- **§5.4 T4 counts.** Five counts live at five distinct layers (player-facing categories / operational registry / regime-change palette / future-expansion register / measurement vocabulary), canonically disambiguated at doc 47 §4.6.9 (verified to exist). **Layered vocabulary, confirmed.**
- **§6.1 §10 6-group vs §12 7-anchor** (the weakest-looking, checked deepest). The §10 6-group rune scaffold is canonically **DEFERRED to Pattern B** (creation-moment doc lines 557/566/594/652 — "canonical rune-group structure lock DEFERRED"); the §12 7-anchor structure is a different object (experiential INPUT cascade anchors) and §12 itself declares "Composition with prior canonical commitments: ALL preserved (… §1-§10 …)" (line 682). No lock exists at 6 to contradict. **The synthesis's reconciliation is accurate and arguably understated.**
- **§4.7 seasonal_journey flag vs season-archival.** Narrative-layer (`seasonal_journey_narrative_structure` preserved) vs release-layer (season-as-release-unit archived), reconciled via D6 §1.4 explicit. **Different axes, holds.**

**Finding:** none of the four papers over an unresolved tension; each is a legitimate layer/scope distinction with explicit source support. The "Contradiction count: zero" headline is **defensible as scoped** — it claims zero *unresolved cross-source contradictions* (each apparent divergence carrying an amendment/layer record), not architectural completeness. **Severity: INFO** — the headline phrasing could be misread as "architecture is settled"; it is not (§9 carries 22 deferred items + the 55-question hypothesis-flow register). Mitigated already by §9 and the doc's own framing ("this is itself a finding: the canon's amendment-pass discipline is holding"). No fix required.

---

## Charge 3 — Standard Gate-1 (coherence / accuracy / scope)

- **Recognition-not-supersession framing:** holds. §1 + §10 state REFERENCE-not-supersession + "source wins on divergence" + gaps DEFERRED-not-resolved. The §2 reading-rule (strategic-frame docs cited for commitments not operational snapshots) is transparent and grounded in supersession-by-refinement (working-notes Block D) — it does not silently override any source.
- **§9 deferred-register criteria are real gates,** not hand-waves: playtest stages, Pattern B sessions (~1hr scoped), Cycle-N work-units, multi-node calibration workstream, ADR-006 Matt-authorization (DB migration), Legolas glyph-corpus crawl. No bare "TBD/revisit-later" without a named empirical/process criterion.
- **Scope discipline:** the doc stays in recognition lane; authors no new design.
- **Discipline #51 self-application:** the doc correctly subjects itself to the gate rather than claiming exemption. **Severity: INFO** — see note below on gate intensity.

---

## INFO notes (no remediation required; for the record)

1. **#51 gate intensity.** #51's founding instance (Q18 flavor-pool) governed a synthesis that *became a new architectural lock*. This synthesis is a REFERENCE/recognition surface that creates no new commitment — so the #51 Matt-adversarial-Pattern-B intensity is correctly satisfiable by the critique-pair reads (gandalf design-side + this QA-side) plus Matt's ratification-as-reference. The "source wins on divergence" rule (§1/§10) is what keeps the gate light: downstream consumers must navigate-to-source, never treat the synthesis as the lock. If any consumer treats it as a lock, the gate requirement retroactively elevates to founding-instance intensity.
2. **Headline misread risk** (Charge 2) — optional one-clause guard on the §9 "Contradiction count: zero" sentence clarifying it means *cross-source consistency*, not *settled/complete*. Not required; §9 already guards.
3. **STATUS-stamp transition** — on this PASS, the header "CURRENT pending Gate-1 critique-pair review" firms to CURRENT via gandalf canonical-write; process step, not a defect.

---

## Action

- [x] jack-ryan: independent adversarial read filed (QA half of Fable-5 Phase-1 eval signal).
- [ ] gandalf: firm STATUS stamp `CURRENT pending Gate-1` → `CURRENT` (header + §10).
- [ ] Matt: confirm the #51 Pattern-B ratification-as-reference is logged (INFO note 1); on confirmation, workstream advances to Fable-5 Phase 2 (rocket) + Phase 3 (gamora) per dispatch.

## References
- Reviewed: `canonical/story/2026-06-10-engine-architecture-canonical-synthesis.md`
- Method artifacts: `agentic_orchestration/gandalf/notes/2026-06-10-fable-5-canonical-synthesis-source-consultation-checklist.md`; `…-fable-5-synthesis-working-notes.md`
- Spot-check sources: `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md`; `canonical/02-roadmap.md`; `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md`; `canonical/51-investment-scaling-6-pattern-architecture-2026-05-28.md`; `canonical/50-bounded-viability-with-specialization-design-directive-2026-05-28.md`; `canonical/47-damage-scaling-architecture-2026-05-27.md`; `canonical/story/2026-06-07-earth-avatar-cosmograph-creation-moment-architecture.md`; `canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md`
- Discipline: `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` #51 (lines 2441-2483)

**Reviewer sign-off:** jack-ryan — Gate-1 PASS. The synthesis is trustworthy as a reference surface: citation fidelity is exemplary (7/7, incl. post-amendment-corrected numbers), the zero-contradiction claim survives adversarial stress-testing as-scoped, and the recognition framing is correctly self-applied to its own gate.
