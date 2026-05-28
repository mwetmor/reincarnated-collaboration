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

(append on completion)
