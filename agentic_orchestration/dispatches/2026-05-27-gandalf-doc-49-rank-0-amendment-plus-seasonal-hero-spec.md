# Dispatch — 2026-05-27 — gandalf — Bundled: doc 49 rank-0 amendment + seasonal_hero_candidates design spec (Pattern-A; ~0.5-1 day combined)

**From:** knight-rider
**To:** gandalf (design-side canonical-write owner; doc 49 + seasonal-hero design steward)
**Approved by:** Matt 2026-05-27 (Design call #3 ratification: "Rank 0 (true empty)... gandalf to author doc 49 amendment" + Design call #1 ratification: "H-5 hybrid (substrate produces top-3; gandalf curates 1 from top-3)")
**Estimated effort:** ~0.5-1 day combined (doc 49 amendment ~15 min; seasonal_hero_candidates design spec ~0.5-1 day)
**Acceptance:** (1) doc 49 amendment clarifying "rank 0 (zero points per node); not rank 1 default" + cross-references to PoE PoB pattern; (2) seasonal_hero_candidates design spec at canonical path specifying Phase 4+5 metadata emission + gandalf design-call workflow + drax surfacing semantics

## Quality criterion (Move 1)

**Game-quality goal this dispatch serves:** lock two ratified design calls into canonical text before downstream impl fires. Design call #3 (rank 0 empty-state) gates Dispatch B (drax Loadout Phase A); Design call #1 (H-5 hybrid seasonal hero) gates Summary tab redesign at Dispatch C + Phase 4+5 emission integration.

**Refutation conditions:**
- Doc 49 rank-0 amendment site mismatch (no § 1.1 (a) currently exists; gandalf judgment on placement)
- Seasonal_hero_candidates emission schema conflicts with existing Phase 4 + 5 schemas (ExportFactionCluster gandalf check)
- H-5 hybrid workflow ambiguity (substrate top-3 selection algorithm; gandalf judgment surface)

## Context

**Matt design call #3 verbatim (rank 0 empty-state):**
"Rank 0 (true empty). All nodes uninvested at startup; matches doc 49 § 1.1 (a) + Matt verbatim "empty" + PoE PoB pattern. gandalf to author doc 49 amendment explicitly noting 'rank 0 (zero points per node); not rank 1 default.'"

**Matt design call #1 verbatim (H-5 hybrid seasonal hero):**
"Seasonal hero: H-5 hybrid (substrate produces top-3; gandalf curates 1 from top-3). Implementation: Phase 4 + 5 emit seasonal_hero_candidates metadata post Wave 5; gandalf design-call selects season_hero_id; drax surfaces in Summary tab."

**Composition with current state:**
- Doc 49 at `canonical/49-loadout-sample-player-surface-design-2026-05-27.md` (gandalf `67b22d7`; player-facing design-spec; CURRENT canonical)
- Phase 4 mechanical archive at engine `749d5aa` (gamora; kit_archive output)
- Phase 5 ExportFactionCluster at engine `bf7f659` + `94f8c88` (star-lord; PM1Cluster + G-B telemetry fields)
- Drax Cycle 14 tab integration response at `a0a449e` (Summary tab redesign scope at Dispatch C; gates on seasonal_hero_candidates emission)

## Required reading

- `canonical/49-loadout-sample-player-surface-design-2026-05-27.md` (target for amendment; current canonical)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/phase4_db.py` (kit_archive schema — Phase 4 output)
- `~/Games/reincarnated-engine/src/reincarnated/export/schemas.py` ExportFactionCluster + ExportFactionRelationship (Phase 5 output)
- `agentic_orchestration/drax/notes/2026-05-27-cycle-14-tab-integration-pattern-a-response.md` (Summary tab scope; seasonal_hero gate)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § Discipline #41 (substrate-led; H-5 hybrid must keep substrate-emergent top-3 NOT pre-authored shortlist)

## Discipline #46 compliance

- N/A — canonical authoring; no DB queries

## Discipline #42 framing-audit

- **Q1:** (1) doc 49 § 1.1 (a) exists OR amendment can place clarification adjacent; (2) seasonal_hero_candidates emission fits Phase 4 + 5 schema architecture; (3) H-5 hybrid workflow is substrate-led (no pre-authored shortlist)
- **Q2:** verify doc 49 § structure pre-amendment; verify Phase 4 + 5 emission feasibility (gamora + star-lord coordination at later impl dispatch); verify substrate-led top-3 selection algorithm doesn't reimpose taxonomy
- **Q3:** if doc 49 amendment site mismatch OR H-5 substrate-led semantics ambiguous, invoke #44 framing-refusal + surface back to KR

## Scope

### Part 1 — doc 49 rank-0 amendment (~15 min)

- [ ] Read `canonical/49-loadout-sample-player-surface-design-2026-05-27.md` § 1.1 (a) — verify current empty-state spec text
- [ ] Apply amendment clarifying: "rank 0 (zero points per node); NOT rank 1 default"
- [ ] Cross-reference Matt verbatim 2026-05-27 design call #3
- [ ] Cross-reference PoE PoB (Path of Exile Path of Building) empty-state pattern
- [ ] Add brief rationale (matches Matt verbatim "empty" + composes with substrate-emergent identity)

### Part 2 — seasonal_hero_candidates design spec (~0.5-1 day)

- [ ] Author seasonal_hero_candidates design spec at `canonical/story/seasonal-hero-h-5-hybrid-spec-2026-05-27.md` (or your judgment on canonical path; could land as doc 49 amendment OR companion spec)
- [ ] **Phase 4 emission spec** — kit_archive seasonal_hero_candidates field semantics; top-3 selection algorithm (substrate-led; e.g., top-3 by Mahalanobis distance from cohort mean OR substrate-coverage-richness OR composite metric); gandalf judgment + Discipline #41 compliance
- [ ] **Phase 5 PM-2 amendment** — composition with cluster-level identity; seasonal_hero_candidates flow from kit-level → cluster-level
- [ ] **Gandalf design-call workflow** — selecting season_hero_id from top-3 candidates at Wave 5 close (post audit-gate PASS); audit log structure for #43
- [ ] **Drax surfacing semantics** — Summary tab consumption of season_hero_id; D-Sharpened invariance applies (substrate-anchored named-personage hidden at engine; player sees uniform Phase 5 LLM naming)
- [ ] **Cross-seam consumption surfaces** — drax loadout summary metadata + star-lord telemetry (per D-Sharpened pattern)
- [ ] Discipline #41 substrate-led verification (top-3 selection MUST be substrate-emergent algorithm; gandalf curation pick from top-3 is design-judgment NOT pre-authored taxonomy reimposition)
- [ ] Risks + Watch Items per failure-modes register § 5 (D-2 faction pre-authored watch; D-4 LLM as oracle watch)

### Closure

- [ ] Append completion record to this dispatch
- [ ] Commit + push per Matt's per-cycle push pattern
- [ ] Signal KR: doc 49 amendment LANDED + seasonal_hero_candidates spec READY for downstream impl (Phase 4 emission impl + Phase 5 amendment + drax Dispatch C surface)

## Acceptance criteria

- [ ] doc 49 § 1.1 (a) rank-0 clarification landed
- [ ] seasonal_hero_candidates design spec authored at canonical path
- [ ] Phase 4 emission spec + Phase 5 amendment + gandalf design-call workflow + drax surfacing semantics specified
- [ ] Discipline #41 substrate-led verified at H-5 hybrid top-3 selection
- [ ] D-Sharpened invariance preserved at seasonal hero surface
- [ ] Risks + Watch Items embedded
- [ ] Completion record + commit + push

## Out of scope

- Do NOT execute Phase 4 + 5 impl for seasonal_hero_candidates emission (separate downstream dispatch post this spec landing)
- Do NOT touch Dispatch C Summary tab impl (drax seam; gated on this spec landing)
- Do NOT touch Dispatch B Loadout Phase A impl (drax seam; doc 49 amendment unblocks)

## Open questions for gandalf

- **Q-Bundle-1:** Seasonal_hero_candidates top-3 selection algorithm — Mahalanobis distance from cohort mean vs substrate-coverage-richness vs composite? Your judgment under Discipline #41
- **Q-Bundle-2:** Canonical path for seasonal_hero spec — doc 49 amendment OR companion spec at `canonical/story/`? Your judgment
- **Q-Bundle-3:** Gandalf design-call workflow at Wave 5 close — Pattern-B Matt design-call vs gandalf-autonomous selection within design-quality audit Discipline #43 authority? Your judgment

## References

- Matt 2026-05-27 design call #1 + #3 verbatim ratifications
- Doc 49 at gandalf `67b22d7`
- Drax Cycle 14 tab integration Pattern-A response at `a0a449e`
- Engineering-disciplines.md § Discipline #41 + #43 + #45

---

## Completion record

(append on completion)
