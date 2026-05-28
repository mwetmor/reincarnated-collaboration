# Dispatch — 2026-05-27 — gamora — Bundled transcription (Pattern-A; Phase 4+5 MG-2 + MG-3 + MG-4 + MG-5)

**From:** knight-rider
**To:** gamora (simulation-side math-note canonical-write owner)
**Approved by:** Matt 2026-05-27 (Path (1) Phase 4+5 ratification flow); jack-ryan PASS-with-REVISIONS disposition at `25af11c` constitutes revision-execution authority
**Estimated effort:** ~1-2 hours combined transcription (MG-2 ~10 min; MG-3 ~30-45 min LOAD-BEARING with 6 amendments; MG-4 ~20-30 min with 5 amendments; MG-5 ~15 min § 7 + § 2 cap annotation)
**Acceptance:** All 4 simulation-side math-notes transcribed per elrond consultation `f8eb1a4` + jack-ryan dispositions + gandalf MG-5 amendments `7233e0f`; transcription obligation, NOT new design question; hand back to KR for Matt-gate routing

## Quality criterion

**Game-quality goal this dispatch serves:** lock jack-ryan-ratified algorithm amendments into canonical simulation-side math-notes as a transcription obligation; enables Phase 4+5 Matt-gate clean ratification + Dispatch 3A (Phase 4 impl) fire-readiness. Preserves algorithm-package integrity through canonical-text persistence. Composes Move 1 quality-criterion + Discipline #18 math-hotspot ratification flow + Discipline #46 § 7 per-cell bounding LOAD-BEARING (MG-5 reject pool schema specifically).

**Refutation conditions** (gamora surfaces if any apply):
- Any elrond consultation amendment text contradicts pre-existing math-note § structure (gamora authored these; should be smoothest transcription)
- MG-5 § 7 CELL_CAPACITY_MAX 50→30 annotation conflicts with elsewhere-in-note bound assumption
- HDBSCAN fallback module spec (MG-3) requires algorithm depth gamora isn't equipped to author (would warrant gandalf or legolas methodology consult)
- KL discrete-grid retirement (MG-4) leaves orphaned reference dependencies elsewhere in note

## Context

**Source: Phase 4+5 LIGHT re-Gate-1 PASS-with-REVISIONS at `25af11c`** — jack-ryan amendment text already in place via:
- **Elrond consultation `f8eb1a4`** (Stream A authority for MG-2/MG-3/MG-4 algorithm amendments)
- **Gandalf MG-5 amendments `7233e0f`** (Stream B authority for MG-5 E-Dev-Phase-Aware + scaffold drift annotation)

**Transcription obligation, NOT new design question** per jack-ryan gating note. All algorithm decisions already ratified at Gate-1; gamora carries text into canonical math-notes.

## Required reading

- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/phase-4-mg-2-crowding-hypervolume-math-2026-05-27.md` (MG-2 transcription target)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/phase-4-mg-3-mahalanobis-distance-math-2026-05-27.md` (MG-3 LOAD-BEARING transcription target)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/phase-4-mg-4-kl-information-gain-math-2026-05-27.md` (MG-4 transcription target)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/phase-4-mg-5-eviction-rules-math-2026-05-27.md` (MG-5 transcription target; pre-existing gandalf amendments at `7233e0f` § X.3 / X.3.2 / X.7 / X.8 / X.9 STAY; this dispatch adds § 7 + § 2 cap annotation)
- `agentic_orchestration/elrond/notes/2026-05-27-phase-4-5-methodology-consultation.md` § 2 MG-2 + § 3 MG-3 + § 4 MG-4 (amendment text authority for MG-2/3/4)
- `agentic_orchestration/dispatches/2026-05-27-jack-ryan-light-re-gate-1-six-math-notes.md` completion record (jack-ryan per-note dispositions; LIGHT re-Gate-1 amendment specs)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § Discipline #46 § 7 (per-cell bounding LOAD-BEARING — MG-5 reject pool schema compliance check)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § Discipline #41 (substrate-led discipline; not violated by transcription)
- `.claude/skills/reincarnated-gamora-operating-procedure`
- `.claude/skills/reincarnated-engineering-disciplines`

## Discipline #46 compliance

- N/A — canonical math-note transcription; no DB queries introduced. **HOWEVER**: MG-5 § 7 CELL_CAPACITY_MAX 50→30 annotation MUST verify Discipline #46 § 7 per-cell bounding integrity preserved (30 archive + 30 reject pool = 60 per-cell rows MAX per gandalf amendment).

## Discipline #42 framing-audit

- **Q1 load-bearing assumptions:** (1) jack-ryan PASS-with-REVISIONS dispositions are revision-execution authority (no new design questions); (2) elrond consultation `f8eb1a4` § 2-4 amendment text encodes cleanly into MG-2/3/4 § structures (gamora authored these; structure compatible); (3) gandalf MG-5 amendments at `7233e0f` are integrated; gamora only adds § 7 + § 2 cap annotation
- **Q2 refutation evidence to seek:** verify amendment text composition does not contradict pre-existing canonical text; verify MG-5 30+30=60 cap integrity preserved post § 7 annotation; verify HDBSCAN fallback module spec is encodable (or surface as Q-T-MG3-1 if methodology depth needed)
- **Q3 outcome trigger:** if any amendment surfaces a composition contradiction OR HDBSCAN fallback spec depth exceeds gamora transcription scope, invoke Discipline #44 framing-refusal + surface back to KR for methodology consultation routing

## Scope

### Part 1 — MG-2 Crowding transcription (~10 min)

- [ ] Amend MG-2 § 4.3 (or equivalent) per elrond consultation `f8eb1a4` § 2:
  - MIN_POPULATION_FOR_DIVERSITY 6→10 (=2d at d=5)
  - Confirm NSGA-II crowding distance Algorithm A spec present (no change)
  - HVC indefinite-deferral rationale documented
  - NSGA-III reference-point variant rejected (rationale: pre-imposes preference structure)

### Part 2 — MG-3 Mahalanobis (LOAD-BEARING) transcription (~30-45 min)

- [ ] Amend MG-3 per elrond consultation `f8eb1a4` § 3 (6 amendments):
  1. Tikhonov regularization: **λ=1e-3** (NOT 1e-4 in prior draft)
  2. MIN_COV_POPULATION: 7→**15**
  3. Empirical-threshold framing: DUPLICATE_THRESHOLD calibrated to **target 5% detection rate** via Hotelling T² reference distribution (NOT chi-squared at small k)
  4. Pareto-strict replacement: REPLACES Q_scalar arbitrary weights
  5. HDBSCAN mutual-reachability fallback as standby module (gated on Shapiro-Wilk smoke test G-MG3-1 normality failure)
  6. G-MG3-1 trigger spec: Shapiro-Wilk normality test on residuals at smoke-test gate; fallback fires if normality rejected at α=0.05
- [ ] Welford 500-insertion checkpoint per Q-MG-3-1 ratification
- [ ] Cross-reference elrond consultation `f8eb1a4` as authority

### Part 3 — MG-4 KL Information Gain transcription (~20-30 min)

- [ ] Amend MG-4 per elrond consultation `f8eb1a4` § 4 (5 amendments):
  1. **Retire § 3 KL+discrete-grid path entirely** (KDE curse-of-dimensionality at d=5; h~k^(-1/9) over-smooths)
  2. JSD primary across full k range
  3. Silverman's rule + 0.05 bandwidth floor (replaces Scott's rule)
  4. Remove NOVELTY_CLAMP (JSD bounded naturally)
  5. MIN_KL_POPULATION: 5→10
- [ ] Verify no orphaned references to retired KL+grid path elsewhere in note (clean ribbon)

### Part 4 — MG-5 Eviction § 7 + § 2 cap annotation (~15 min)

- [ ] PRESERVE gandalf-authored amendments at `7233e0f` (§ X.3 OWN 30-kit reject pool cap; § X.3.2 scaffold drift surface; § X.7 30+30=60 per-cell MAX; § X.8 Trigger B candidates T-B-α + T-B-γ; § X.9 Risks + Watch Items)
- [ ] Amend MG-5 § 7 (canonical cap declaration): CELL_CAPACITY_MAX **50→30** (alignment with C2 ratification); add scaffold-drift-resolution annotation (pre-existing 50 predated C2 ratification)
- [ ] Amend MG-5 § 2 (input bundle / parameter definitions): update CELL_CAPACITY_MAX reference to 30
- [ ] Verify Discipline #46 § 7 per-cell bounding integrity: 30 archive + 30 reject pool = 60 per-cell rows MAX (no Discipline #46 violation)
- [ ] Verify Pareto Rank 0 protection rationale documented (reject pool OWN cap avoids eating into archive Rank 0)

### Closure

- [ ] Append completion record to this dispatch (per-part outcomes; HDBSCAN fallback encoding outcome; Discipline #46 § 7 integrity verification)
- [ ] Surface any framing-refusal (Discipline #44) if Q3 triggers
- [ ] Commit + push per Matt 2026-05-27 per-cycle push pattern (auto-fire per CLAUDE.md addendum)

## Acceptance criteria

- [ ] MG-2 amendment landed (MIN_POPULATION_FOR_DIVERSITY 6→10)
- [ ] MG-3 6 amendments landed (Tikhonov λ=1e-3 / MIN_COV 15 / Hotelling T² / Pareto-strict / HDBSCAN fallback / G-MG3-1 spec)
- [ ] MG-4 5 amendments landed (retire grid / JSD primary / Silverman + 0.05 / remove NOVELTY_CLAMP / MIN_KL 10)
- [ ] MG-5 § 7 + § 2 CELL_CAPACITY_MAX 50→30 annotation landed; gandalf amendments preserved
- [ ] Discipline #46 § 7 per-cell bounding integrity verified (30+30=60 MAX)
- [ ] Completion record appended; commit + push
- [ ] Hand back to KR for: (a) parallel gandalf transcription verification (Stream A PM-1 + Stream B Option α); (b) Matt-gate ratification routing for Phase 4+5 + Option α packages; (c) Dispatch 3A (Phase 4 impl) authoring post Matt-gate

## Out of scope

- Do NOT touch MG-1 (PROCEED-AS-AUTHORED; no transcription needed)
- Do NOT touch PM-1 / PM-2 (gandalf sister dispatch)
- Do NOT touch Option α notes (gandalf sister dispatch)
- Do NOT touch Dispatch 3A impl (KR seam post Matt-gate)
- Do NOT enter LIGHT re-Gate-1 mode (jack-ryan seam; if any amendment re-opens prior PASS conditions, surface as completion-record note for KR routing)

## Open questions for gamora

- **Q-T-MG2-1:** Any pre-existing MG-2 § structure that resists amendment text encoding? Your judgment under Discipline #11 empirical-inspection
- **Q-T-MG3-1:** HDBSCAN fallback module spec depth — is the elrond consultation text sufficient for transcription, or does it need methodology depth (e.g., per-parameter spec for mutual-reachability distance computation)? If the latter, surface as Discipline #44 framing-refusal + route to legolas Mode A
- **Q-T-MG4-1:** Any orphaned KL+grid references in MG-4 elsewhere (e.g., cross-references, table headers, equations) that need ribbon cleanup post-retirement? Your judgment
- **Q-T-MG5-1:** Discipline #46 § 7 per-cell bounding verification — confirm 30+30=60 cap is the canonical statement; verify no other § of MG-5 implies a different cap

## References

- jack-ryan Phase 4+5 PASS-with-REVISIONS at `25af11c`
- elrond consultation authority: `agentic_orchestration/elrond/notes/2026-05-27-phase-4-5-methodology-consultation.md`
- gandalf MG-5 amendments authority: engine `7233e0f`
- Engineering-disciplines.md § Discipline #41 / #42 / #44 / #46 § 7
- Path (1) failure-modes register § 5 (Risks + Watch Items pattern)

---

## Completion record

(append on completion)
