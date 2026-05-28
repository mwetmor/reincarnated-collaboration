# Dispatch — 2026-05-27 — jack-ryan — LIGHT re-Gate-1 bundled review (6 math-notes; pre-Matt-gate)

**From:** knight-rider
**To:** jack-ryan (DESIGN-MODE Gate-1 reviewer; LIGHT scope per Matt routing)
**Approved by:** Matt 2026-05-27 verbatim "jack-ryan LIGHT re-Gate-1 verification (~1-2 hr); then surface remaining Matt-gate as 8 math-note algorithm ratifications + 1 WARN + 4 INFO per Discipline #18 math-hotspot ratification"
**Estimated effort:** ~1-2 hours bundled review across 6 math-notes
**Acceptance:** Bundled re-Gate-1 PASS / PASS-with-REVISIONS / BLOCK verdict per note; per-question ratifications surfaced (Trigger B candidate selection, reject-pool cap selection, MG-5 § 7 cap-alignment scaffold drift disposition); Matt-gate fire-ready package assembled

## Quality criterion

**Game-quality goal this dispatch serves:** verify that the bundled methodology amendments (4 from elrond + 2 from gandalf) preserve algorithmic correctness, per-cell bounding integrity (Discipline #46 § 7 LOAD-BEARING), substrate-led discipline (Discipline #41), and Move 1 quality-criterion intent BEFORE Matt-gate ratification fires. Without this LIGHT re-Gate-1, Matt-gate inherits unverified amendment composition risk — the consolidated stream is too large for direct Matt review without process-gate filtering.

**Refutation conditions** (jack-ryan surfaces if any apply):
- Any of the 4 elrond methodology amendments OR 2 gandalf amendments contradict pre-existing Gate-1 PASS conditions
- Reject pool schema violates Discipline #46 § 7 per-cell bounding (cap mis-specified OR per-cell semantics ambiguous)
- Trigger B verdict authority under Discipline #43 requires separate sub-discipline ratification (not just verdict-application)
- MG-5 § 7 cap-alignment scaffold drift (`CELL_CAPACITY_MAX=50` vs C2 30-kit) requires Matt-gate question, not jack-ryan disposition
- PM-1 algorithm commit (GMM primary k∈{3,4}) contradicts SC-3 Pattern B PRIMARY structured-output composition with PM-2

## Context

**Two parallel amendment streams converged into single re-Gate-1 bundle:**

**Stream A — Elrond bundled methodology consultation (engine `f8eb1a4`):**
- MG-1 Pareto: PROCEED-AS-AUTHORED (NO re-Gate-1 needed)
- MG-2 Crowding: minor amendment (MIN_POPULATION 6→10; NSGA-II; HVC deferred)
- **MG-3 Mahalanobis (LOAD-BEARING):** substantive — Gaussian + Tikhonov **λ=1e-3 NOT 1e-4**, MIN_COV_POPULATION 7→15, **Hotelling T² not chi-squared at small k**, HDBSCAN fallback gated on Shapiro-Wilk smoke test G-MG3-1
- **MG-4 KL:** substantive REFRAMING — **JSD primary across full k range**; **retire discrete-grid KL entirely** (KDE curse-of-dimensionality at d=5); Silverman + 0.05 floor; remove NOVELTY_CLAMP; MIN_KL_POPULATION 5→10
- **PM-1 Multimodal:** algorithm commit — **A4 GMM primary k∈{3,4} BIC-selected NOT 5**; A1 k-means n<20 fallback; Option β CONFIRMED distinct from substrate-row HDBSCAN; aesthetic-heavy sqrt-weights + PCA-whitening 95%; PM-1↔MG-5 feedback loop architecturally committed

**Stream B — Gandalf PM-2 + MG-5 amendments (engine `7233e0f` + meta `fcb7b0d`):**
- **PM-2 D-Sharpened:** new § 2.7 + § 3.7 added (substrate-anchored named-personage hidden engine-layer; metadata to drax + star-lord; Phase 5 LLM uniform player-facing); composes with D-Hybrid + D-Separate; LAYERS ON
- **MG-5 E-Dev-Phase-Aware:** reject pool retention during engine-dev phase; Trigger B switchover to E1 discard; **gandalf-recommend (a) OWN per-cell cap 30-kit mirroring archive C2** (rationale: avoids reject pool eating into archive Pareto Rank 0 protection); Trigger B candidates surfaced (T-B-α primary + T-B-γ override); Q-E-3 telemetry YES-recommend; **NEW finding surfaced:** MG-5 § 7 pre-existing `CELL_CAPACITY_MAX=50` vs C2 30-kit ratification scaffold drift (out-of-scope per gandalf dispatch; routed to this re-Gate-1)

## Required reading

- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/phase-4-mg-1-pareto-dominance-math-2026-05-27.md` (MG-1; PROCEED-AS-AUTHORED — verify per-cell bounding compliance still holds)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/phase-4-mg-2-crowding-hypervolume-math-2026-05-27.md` (MG-2; minor amendment review)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/phase-4-mg-3-mahalanobis-math-2026-05-27.md` (MG-3 LOAD-BEARING; substantive amendment review)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/phase-4-mg-4-kl-information-gain-math-2026-05-27.md` (MG-4; substantive REFRAMING review)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/phase-4-mg-5-eviction-rules-math-2026-05-27.md` (MG-5; gandalf amendment + scaffold drift finding)
- `~/Games/reincarnated-engine/src/reincarnated/generation/math/phase-5-pm-1-multimodal-clustering-math-2026-05-27.md` (PM-1; algorithm commit review)
- `~/Games/reincarnated-engine/src/reincarnated/generation/math/phase-5-pm-2-faction-label-assignment-math-2026-05-27.md` (PM-2; D-Sharpened § 2.7 + § 3.7 review)
- `agentic_orchestration/elrond/notes/2026-05-27-phase-4-5-methodology-consultation.md` (Stream A authority)
- `agentic_orchestration/dispatches/2026-05-27-gandalf-pm2-mg5-amendments-matt-ratifications.md` (Stream B authority + completion record)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § Discipline #46 § 7 (per-cell bounding LOAD-BEARING)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § Discipline #43 (design-quality audit; Trigger B verdict authority)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § Discipline #41 (pre-authored taxonomy interrogation; substrate-led discipline preservation)
- `.claude/skills/reincarnated-jack-ryan-operating-procedure`
- `.claude/skills/reincarnated-engineering-disciplines`
- Prior Gate-1 record: `7d5d585` (Gate-1 PASS-with-REVISIONS bundled review for 7 notes 2026-05-27)

## Discipline #46 compliance

- N/A — this is canonical math-note re-review; no DB queries introduced. **HOWEVER**: re-Gate-1 audit MUST verify each amendment preserves Discipline #46 § 7 per-cell bounding compliance. Particular attention to MG-5 reject pool cap selection (gandalf-recommend OWN 30-kit per-cell) and MG-5 § 7 scaffold drift (`CELL_CAPACITY_MAX=50` predates C2 ratification at 30).

## Discipline #42 framing-audit

- **Q1 load-bearing assumptions:** (1) Stream A elrond methodology amendments + Stream B gandalf amendments are independently authored against compatible canonical anchors; (2) re-Gate-1 LIGHT scope means amendment-delta review NOT full re-review of pre-Gate-1-PASS notes; (3) Trigger B verdict authority under Discipline #43 is ratifiable WITHOUT separate sub-discipline ratification
- **Q2 refutation evidence to seek:** Stream A + Stream B independence verification (do any of the 6 amendments touch the same code/note section creating composition conflict?); LIGHT-scope boundary verification (any amendment that re-opens a prior Gate-1 PASS condition warrants full review, not LIGHT); Discipline #43 authority scope verification (canonical text supports verdict-application without amendment?)
- **Q3 outcome trigger:** if any Q-MG / Q-PM-1 / Q-PM-2 / Q-MG-5 below surfaces a framing contradiction OR if MG-5 § 7 scaffold drift requires Matt-gate not jack-ryan disposition, invoke Discipline #44 framing-refusal + surface back to KR for re-routing

## Scope — per-note bundled re-Gate-1

### MG-1 Pareto (verification-only; no amendment)

- [ ] Verify MG-1 still passes prior Gate-1 PASS conditions
- [ ] Verify per-cell bounding (Discipline #46 § 7) still encoded
- [ ] Disposition: PASS / PASS-with-REVISIONS / BLOCK

### MG-2 Crowding (minor amendment)

- [ ] Verify MIN_POPULATION_FOR_DIVERSITY 6→10 (=2d) amendment landed cleanly
- [ ] Verify NSGA-II crowding distance Algorithm A correctly specified
- [ ] Verify HVC indefinite-defer rationale present
- [ ] Verify NSGA-III reference-point rejection rationale present
- [ ] Disposition

### MG-3 Mahalanobis (LOAD-BEARING; substantive amendment)

- [ ] Verify Gaussian Mahalanobis + Tikhonov regularization spec (Σ+λI; **λ=1e-3 NOT 1e-4**)
- [ ] Verify MIN_COV_POPULATION 7→15 amendment
- [ ] Verify Hotelling T² substitution for chi-squared at small k (with empirical 5% detection target)
- [ ] Verify Pareto-strict replacement of Q_scalar arbitrary weights
- [ ] Verify HDBSCAN mutual-reachability fallback module spec
- [ ] Verify Shapiro-Wilk normality smoke test G-MG3-1 trigger condition
- [ ] Verify Welford 50-insertion checkpoint (or relaxed to 500 per elrond suggestion)
- [ ] Disposition

### MG-4 KL (substantive REFRAMING)

- [ ] Verify JSD primary across full k range; verify discrete-grid KL path FULLY RETIRED (not deferred)
- [ ] Verify Silverman's rule + 0.05 bandwidth floor replaces Scott's rule
- [ ] Verify NOVELTY_CLAMP removal (JSD natural bounding documented)
- [ ] Verify MIN_KL_POPULATION 5→10 amendment
- [ ] Disposition

### MG-5 Eviction (gandalf amendment + scaffold drift finding)

- [ ] Verify E-Dev-Phase-Aware retention-policy encoding
- [ ] **Verify reject pool per-cell cap selection — pick (a) OWN 30-kit OR (b) shared 30-kit; jack-ryan ratifies under Discipline #46 § 7 authority** (gandalf-recommend (a))
- [ ] **Verify Trigger B operational definition — pick from candidates T-B-α / T-B-β / T-B-γ; jack-ryan ratifies under Discipline #43 authority** (gandalf-recommend T-B-α primary + T-B-γ override)
- [ ] **Surface scaffold drift finding** — MG-5 § 7 pre-existing `CELL_CAPACITY_MAX=50` vs C2 30-kit ratification — disposition: (a) jack-ryan amends MG-5 § 7 to align with C2 (in-scope LIGHT scope) OR (b) surface to Matt-gate as separate question (out-of-scope; requires Matt verdict)
- [ ] Verify Discipline #46 § 7 per-cell bounding compliance preserved across reject pool + archive (30 + 30 = 60 per-cell rows MAX confirmed)
- [ ] Verify Q-E-3 telemetry recommend disposition (FIFO eviction count per cell per season)
- [ ] Disposition

### PM-1 Multimodal (algorithm commit)

- [ ] Verify A4 GMM primary commit (k∈{3,4} BIC-selected NOT 5)
- [ ] Verify A1 k-means n<20 fallback
- [ ] Verify Option β CONFIRMED distinction from substrate-row HDBSCAN (Note 1 Option α composition)
- [ ] Verify aesthetic-heavy sqrt-weights pre-PCA
- [ ] Verify PCA-whitening top-95% variance normalization
- [ ] Verify revised GMM-aware sparsity thresholds (24/20/12/8)
- [ ] Verify PM-1↔MG-5 calibration feedback loop architecturally committed (5-season window)
- [ ] Verify substrate-led discipline (Discipline #41) preserved (aesthetic-heavy = design lens, NOT pre-authored faction taxonomy)
- [ ] Disposition

### PM-2 D-Sharpened (gandalf amendment)

- [ ] Verify § 2.7 D-Sharpened composition with D-Hybrid + D-Separate (LAYERS ON; does NOT replace)
- [ ] Verify § 3.7 algorithm invariance clause (faction-label assignment runs identically regardless of substrate-anchored vs synthesized lineage)
- [ ] Verify metadata-emission surfaces correctly bounded (drax loadout summary + star-lord telemetry; gating mechanism present for substrate_anchored field)
- [ ] Verify Sketch F design intent preservation (named-personage hiding compatible with identity-bestowal semantics — does layered metadata satisfy the "hidden at engine layer" criterion?)
- [ ] Verify SC-3 Pattern B PRIMARY composition still holds (Structured Output with Layer Tags; D-Sharpened doesn't break LLM call architecture)
- [ ] Disposition

## Acceptance criteria

- [ ] Per-note disposition (6 verdicts: PASS / PASS-with-REVISIONS / BLOCK)
- [ ] Trigger B candidate selection ratified (jack-ryan picks T-B-α / T-B-β / T-B-γ + override choice)
- [ ] Reject pool per-cell cap selection ratified (gandalf-recommend (a) OWN 30-kit; jack-ryan confirms or refutes)
- [ ] MG-5 § 7 cap-alignment scaffold drift dispositioned (in-scope amend OR out-of-scope Matt-gate question)
- [ ] Bundled BLOCK count (if any) surfaced with remediation path
- [ ] Matt-gate fire-ready package assembled: 8 math-note algorithm ratifications + 1 WARN + 4 INFO (per Matt routing)
- [ ] Completion record appended to this dispatch
- [ ] Commit + push per Matt 2026-05-27 per-cycle push pattern (auto-fire per CLAUDE.md addendum)

## Out of scope

- Do NOT enter DEV-MODE Gate-2 review (re-Gate-1 mode only)
- Do NOT re-review MG-1 / PM-2 unchanged sections (LIGHT scope — amendment-delta only; MG-1 verification-only; PM-2 new sections only)
- Do NOT touch THEMATIC_REGISTRY authoring (separate gandalf cross-cutting dispatch post Matt-gate)
- Do NOT touch Dispatch 3A/3B authoring (KR seam; post Matt-gate)
- Do NOT amend canonical math-notes (gandalf + elrond + gamora authorship); jack-ryan disposition only — if amendment needed, surface as BLOCK with required-change spec

## Open questions for jack-ryan

- **Q-MG-3-1:** Welford 50-insertion checkpoint OK or relax to 500 per elrond suggestion? Your judgment under Discipline #11 empirical-inspection authority
- **Q-MG-5-1:** Reject pool per-cell cap (a) OWN 30-kit vs (b) shared 30-kit — gandalf-recommend (a); your ratification under Discipline #46 § 7 authority
- **Q-MG-5-2:** Trigger B candidate selection T-B-α / T-B-β / T-B-γ — gandalf-recommend T-B-α primary + T-B-γ override; your ratification under Discipline #43 authority
- **Q-MG-5-3:** MG-5 § 7 cap-alignment scaffold drift — in-scope amend (you write MG-5 § 7 amendment) OR out-of-scope Matt-gate question?
- **Q-PM-1-1:** Does PM-1 algorithm commit retain substrate-led discipline (Discipline #41)? aesthetic-heavy weighting = design lens, NOT pre-authored faction taxonomy — verify clean separation
- **Q-PM-2-1:** Does D-Sharpened metadata-emission satisfy "hidden at engine layer" semantics? engine-internal data with controlled surfacing to drax/star-lord — is this hiding-equivalent or surfacing-equivalent under Sketch F design intent?

## References

- Stream A: `agentic_orchestration/elrond/notes/2026-05-27-phase-4-5-methodology-consultation.md` + engine `f8eb1a4`
- Stream B: `agentic_orchestration/dispatches/2026-05-27-gandalf-pm2-mg5-amendments-matt-ratifications.md` + engine `7233e0f` + meta `fcb7b0d`
- Prior Gate-1: meta `7d5d585` (PASS-with-REVISIONS 7 notes)
- Matt 2026-05-27 ratification verbatim (5 in-advance + D-Sharpened + E-Dev-Phase-Aware)
- Engineering-disciplines.md § Discipline #41 / #42 / #43 / #44 / #46 (all load-bearing in this review)

---

## Completion record

(append on completion)
