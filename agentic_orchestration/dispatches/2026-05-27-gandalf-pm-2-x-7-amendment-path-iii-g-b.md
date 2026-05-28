# Dispatch — 2026-05-27 — gandalf — PM-2 § X.7 amendment (Path III G-B primary-pair selection math spec; ~30 min mechanical apply)

**From:** knight-rider
**To:** gandalf (PM-2 canonical-write owner)
**Approved by:** Matt 2026-05-27 verbatim Path III ratification "Let's go with option (III)" + KR Path III kicker § 3 routing
**Estimated effort:** ~30 min mechanical amendment (copy-paste-ready spec from Path III kicker § 3; verify composition with existing PM-2 structure)
**Acceptance:** PM-2 § X.7 amendment landed at `~/Games/reincarnated-engine/src/reincarnated/generation/math/phase-5-pm-2-faction-label-assignment-math-2026-05-27.md` per Path III kicker § 3 spec; G-B primary-pair selection algorithm canonical; consumable by Dispatch 3B Seam 1 rocket PM-1 impl + Wave 3 F-C LLM impl

## Quality criterion (Move 1)

**Game-quality goal this dispatch serves:** lock G-B primary-pair selection algorithm canonically so Dispatch 3B Seam 1 rocket PM-1 impl + Wave 3 F-C LLM (primary_pair_intensifier slot) can integrate without re-deliberation. Composes Path III faction-assembly extension with PM-1+PM-2 Matt-ratified work.

**Refutation conditions:**
- § X.7 placement conflicts with existing PM-2 numbering (collision with § 2.7 D-Sharpened or § 3.7 algorithm invariance)
- Mahalanobis pairwise centroid distance spec at k∈{3,4} produces NaN at MIN_COV<15 edge case (composition with MG-3 Tikhonov regularization?)
- Tie-break logic non-deterministic under specific substrate patterns (verify per-seed determinism preserved)

## Context

**Source:** `agentic_orchestration/gandalf/notes/2026-05-27-path-iii-kr-amendment-kicker.md` § 3 — PM-2 § X.7 spec ready-to-copy as markdown block.

**Path III amendment scope:**
- G-B algorithmic primary-pair selection from PM-1 emergent clusters
- Mahalanobis pairwise centroid distance over cluster set
- Selects primary_faction_pair metadata
- Tie-break logic (lineage diversity / named anchor / geometry / lexicographic)
- O(k²) at k∈{3,4} = max 12 pairwise ops (trivial)
- Mahalanobis pooled-covariance reuses MG-3 infrastructure

**Composition with current state:**
- PM-2 § 2.7 + § 3.7 D-Sharpened amendments LANDED at engine `7233e0f`
- PM-2 stale-ref sweep LANDED at engine `27bfd0e` (all `class_name_*` → `kit_name_*`)
- New § X.7 = new section at end of PM-2 doc (gandalf judgment on exact section number — likely § 4 or § 7 depending on PM-2's existing structure)

## Required reading

- `agentic_orchestration/gandalf/notes/2026-05-27-path-iii-kr-amendment-kicker.md` § 3 (full § X.7 spec; ready-to-copy markdown)
- `agentic_orchestration/gandalf/notes/2026-05-27-path-iii-faction-assembly-extension.md` § 2 (G-B full spec for reference)
- `~/Games/reincarnated-engine/src/reincarnated/generation/math/phase-5-pm-2-faction-label-assignment-math-2026-05-27.md` (target)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/phase-4-mg-3-mahalanobis-distance-math-2026-05-27.md` (Mahalanobis pooled-covariance infrastructure reference)
- Engineering-disciplines.md § Discipline #45 (vocabulary lock; verify § X.7 doesn't introduce class/role/archetype-list prohibited vocabulary)

## Discipline #46 compliance

- N/A — canonical math-note amendment; no DB queries. Note: § X.7.4 already states O(k²) at k∈{3,4} = max 12 ops, no per-cell bounding concern; preserve verbatim.

## Discipline #42 framing-audit

- **Q1:** (1) § X.7 placement doesn't collide with existing PM-2 numbering; (2) Mahalanobis pooled-covariance reuses MG-3 infrastructure (which is now landed at gamora `749d5aa`); (3) tie-break logic is deterministic + complete (lexicographic final fallback per § X.7.2 # 4)
- **Q2:** verify section numbering; verify MG-3 infrastructure reference correct
- **Q3:** if section numbering collision OR MG-3 reference broken, invoke #44 framing-refusal + surface to KR

## Discipline #45 compliance

- N/A — § X.7 does NOT introduce class/role/archetype vocabulary. faction_pair_*, cluster_id, pairwise_distance, selection_rationale all permitted.
- Verify no `class`/`role`/etc. terms in copied text (pre-verified clean per kicker authoring; gandalf double-checks at apply)

## Scope

- [ ] Read Path III kicker § 3 § X.7 spec (ready-to-copy markdown)
- [ ] Identify correct section number for PM-2 (the kicker says § X.7; gandalf judgment on whether this becomes § 4, § 7, or other based on PM-2's existing structure)
- [ ] Apply § X.7 amendment to PM-2 math note (full markdown block from kicker § 3)
- [ ] Verify no section-number collision with existing § 2.7 / § 3.7 D-Sharpened content
- [ ] Verify Discipline #45 vocabulary compliance (no `class`/`role`/`archetype` non-exempt terms in copied text)
- [ ] Append completion record to this dispatch
- [ ] Commit + push per Matt 2026-05-27 per-cycle push pattern

## Acceptance criteria

- [ ] § X.7 amendment landed at PM-2 math note
- [ ] Section numbering clean (no collision)
- [ ] § X.7.1-X.7.5 sub-sections present per kicker § 3 spec
- [ ] Discipline #45 vocabulary compliance verified
- [ ] Completion record + commit + push

## Out of scope

- Do NOT modify § X.7 spec content beyond what kicker § 3 specifies (kicker spec is authoritative)
- Do NOT touch PM-2 § 2.7 / § 3.7 D-Sharpened amendments (preserve `7233e0f` content)
- Do NOT touch other math notes (parallel scopes complete)
- Do NOT enter Discipline #18 re-Gate-1 mode (jack-ryan seam; kicker § 6 notes ~15-min review can happen as part of next-fire Wave 3 or Dispatch 3B Seam 1 Gate-1)

## Open questions for gandalf

- **Q-X7-1:** PM-2 section numbering — what's the next available top-level section number in PM-2 to receive G-B as § X.7 (e.g., § 4, § 7)? Your judgment based on PM-2's current structure
- **Q-X7-2:** Mahalanobis pooled-covariance reference — cross-link to MG-3 math note (engine `749d5aa` post-gamora) at § X.7.4 or X.7.5? Your judgment

## References

- Matt 2026-05-27 Path III verbatim "Let's go with option (III)"
- Path III kicker § 3 (ready-to-copy spec)
- Path III full spec at `2026-05-27-path-iii-faction-assembly-extension.md` § 2
- MG-3 math note (gamora `749d5aa`; Mahalanobis pooled-covariance reference)
- Engineering-disciplines.md § Discipline #45 (just-landed; vocabulary compliance check)

---

## Completion record

**Completion timestamp:** 2026-05-27 (Pattern-A apply by sub-agent gandalf)
**Executor:** sub-agent gandalf (KR invocation)
**Effort actual:** ~20 min (within ~30-min estimate)

### What landed

**Target file:** `~/Games/reincarnated-engine/src/reincarnated/generation/math/phase-5-pm-2-faction-label-assignment-math-2026-05-27.md`

**Section numbering decision (resolves Q-X7-1):**
- The kicker's "§ X.7" naming was a placeholder. PM-2's existing top-level sequence runs § 1 through § 13 (Sign-off at § 13). Subsections use two-deep numbering (§ 2.1...§ 2.7, § 3.1...§ 3.7).
- **Decision:** insert new content as top-level **§ 13** between § 12 (Architectural surprises) and the old § 13 Sign-off; renumber Sign-off to **§ 14**. Subsections become § 13.1 through § 13.5.
- **Rationale:** G-B primary-pair selection is a new math layer adjacent to (not sub-of) § 3 label-assignment policy. Placing it as top-level § 13 keeps § 1-12 numbering intact (no churn on prior cross-refs to § 9 disciplines, § 11 framing-audit). Only Sign-off renumbers (§ 13 → § 14). Verified no external cross-refs to PM-2 § 13 across `reincarnated-engine/`, `canonical/`, `agentic_orchestration/` (grep returned zero matches).
- Honors the kicker's "X.7.1...X.7.5" sub-numbering intent by mapping X=13 and writing subsections as § 13.1 through § 13.5 (matches PM-2's existing two-deep convention).

**Cross-link to MG-3 (resolves Q-X7-2):**
- Cross-link placed at **§ 13.4** (Discipline #46 compliance) — the natural home given MG-3 reuse is named in the Discipline #46 line of the kicker source
- ADDITIONAL cross-link placed in the § 13 header composition note (engine commit `749d5aa` + absolute path to MG-3 spec)
- ADDITIONAL cross-link at § 13.5 closing line (notes MG-3 pooled-covariance reused at cluster-centroid scale rather than per-cell scale)
- Three cross-link placements ensures rocket Dispatch 3B Seam 1 impl + Wave 3 F-C LLM impl + jack-ryan LIGHT re-Gate-1 review all find the MG-3 reference at the expected reading location

### Content applied (per kicker § 3 spec; verbatim where applicable)

- § 13 header + composition note (gandalf addition; clarifies § 13 as new math layer composing with § 3 + § 3.7)
- § 13.1 Algorithm (verbatim from kicker; formatted as code block per house style)
- § 13.2 Tie-breaking (verbatim from kicker; 4 ordered rules)
- § 13.3 Output metadata schema (verbatim from kicker; JSON block)
- § 13.4 Discipline #46 compliance (verbatim from kicker + MG-3 cross-link expansion + Tikhonov regularization edge-case acknowledgement)
- § 13.5 Cross-seam consumption (verbatim from kicker; drax + star-lord + F-C three-seam consumption pattern preserved; MG-3 cross-link added at closing)

### Sign-off update

Updated § 14 Sign-off Status line to acknowledge Path III § 13 amendment alongside prior D-Sharpened § 2.7 + § 3.7 amendments. LIGHT re-Gate-1 verification scope noted as folding into Dispatch 3B / Wave 3 authoring per kicker § 6.

### Acceptance criteria verification

- [x] § 13 amendment landed at PM-2 math note
- [x] Section numbering clean (no collision with § 2.7 / § 3.7 D-Sharpened content; § 2.7 + § 3.7 preserved verbatim from engine `7233e0f`)
- [x] § 13.1-13.5 sub-sections present per kicker § 3 spec
- [x] Discipline #45 vocabulary compliance verified (only `proxy_geometry_class` matches in new block; exempt per Discipline #45 § 1715 — substrate field name; pre-existing infrastructure)
- [x] Completion record appended (this section)
- [ ] Commit + push per Matt 2026-05-27 per-cycle push pattern (next step)

### Refutation-conditions check (per Quality criterion)

- **§ X.7 placement conflicts with existing PM-2 numbering** — RESOLVED via § 13 placement + § 14 Sign-off renumbering; § 2.7 + § 3.7 preserved verbatim
- **Mahalanobis pairwise centroid distance at k∈{3,4} produces NaN at MIN_COV<15 edge case** — § 13.4 now explicitly notes MG-3 Tikhonov regularization handles this edge case (composition with MG-3 § 4 per-cell algorithm); no separate engine implementation required for PM-2 — reuses MG-3 infrastructure
- **Tie-break logic non-deterministic under specific substrate patterns** — § 13.2 # 4 (lexicographic final fallback) guarantees per-seed determinism; preserved verbatim from kicker

### Architectural surprises surfaced (none new; one acknowledgement)

No new architectural surprises beyond what kicker § 3 + the dispatch refutation conditions already named. One acknowledgement worth flagging for downstream jack-ryan LIGHT re-Gate-1 review:

- **MG-3 reuse pattern composition with § 13:** MG-3 was authored for per-cell Mahalanobis distance during MAP-Elites archive duplicate detection (cell-scale; cell sample count drives MIN_COV threshold). § 13 reuses the SAME distance + pooled-covariance computation at cluster-centroid scale (k∈{3,4} centroids; cluster sample counts may differ from per-cell sample counts). The Tikhonov regularization that protects per-cell MIN_COV<15 ALSO protects cluster-scale MIN_COV<15 (centroid pooled-covariance over cluster member sample counts). Cross-link at § 13.4 makes this composition explicit; rocket Dispatch 3B Seam 1 impl should reuse MG-3 pooled-covariance computation directly (no parallel implementation). No additional refutation surfaced.

### Hand-back

Per dispatch hand-back spec: KR fires next gandalf-touching work post-completion (gandalf OP amendment, then Phase 7 Seam 1, then Wave 3 Seam 1, then A/B comparison protocol). Plus rocket Dispatch 3B Seam 1 PM-1 + G-B impl fires after this lands (rocket consumes G-B spec at § 13).

**Signed:** sub-agent gandalf (story-and-design steward)

---

## INFO-1 follow-on completion record (rocket)

**Completion timestamp:** 2026-05-27 (Pattern-A apply by sub-agent rocket)
**Executor:** sub-agent rocket (INFO-1 follow-on per jack-ryan Path-III LIGHT re-Gate-1 verification note)
**Effort actual:** ~5 min (mechanical; within ~5-10 min estimate)

### What landed

**Code fix:** `~/Games/reincarnated-engine/src/reincarnated/generation/phase5_pm1_multimodal_clustering.py` — `_apply_gb_tiebreak` step 4 return value changed from `"geometry_divergence_tiebreak"` to `"lexicographic_tiebreak"` (line 1042). Step 3 return (`"geometry_divergence_tiebreak"` at line 1036) is unchanged and correct.

**Test updates** (3 call sites in `tests/test_dispatch_3b_phase5_seam1_pm1_gb.py`):
- `test_tiebreak_lineage_diversity_preferred` (line 477): added `"lexicographic_tiebreak"` to the valid-rationale tuple
- `test_tiebreak_valid_rationale_values` (line 500): added `"lexicographic_tiebreak"` to `valid_rationales` set
- `test_10_season_tiebreak_rate_under_20pct` (line 655): added `"lexicographic_tiebreak"` to tiebreak-event counting set (step 4 is a tiebreak event; correct to include in rate)

**Test run:** 50/50 PASS, 0 regressions.

### Enum string verification

PM-2 § 13.3 amendment at engine `0cf4f3a` lists `"lexicographic_tiebreak"` as the 5th permitted value verbatim. Impl now matches spec exactly.

### Caller-site grep findings

`_apply_gb_tiebreak` has one call site: `select_primary_faction_pair` line 926. No other code path emits `"geometry_divergence_tiebreak"` when step 4 is the actual resolver. Star-lord seam files `src/reincarnated/export/schemas.py` (line 672) and `src/reincarnated/export/MIGRATION.md` (line 39) still enumerate the old 4-value rationale comment — those are star-lord seam; flagged here for KR to route a star-lord follow-on if schema-comment alignment is desired.

**Signed:** sub-agent rocket
