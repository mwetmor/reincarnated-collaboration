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

### 2026-05-27 — gandalf — BOTH PARTS LANDED

**Part 1 — doc 49 § 1.1.1 rank-0 amendment — LANDED at commit `35c2800`** (committed + pushed at incremental-write boundary per dispatch directive).

Amendment summary:
- Inserted explicit "rank 0 (zero points per node); NOT rank 1 default" specification in § 1.1 Loadout functional spec bullet list
- Added new § 1.1.1 dedicated amendment block citing Matt 2026-05-27 verbatim design call #3
- Three composing rationales: Matt verbatim "empty" mismatch under rank-1 default; ~70-point endgame budget infeasibility under rank-1 default; theorycraft semantics break (rank-1 default removes first-allocation choice)
- PoE Path of Building genre precedent (empty passive tree at session start)
- Composition with substrate-emergent identity (kit shape carries identity per Path (1) Wave 1.5 Stage 3 Option α; rank-0 empty preserves identity intact)
- Drax-side derivation pattern (engine emits kit_committed_state.skill_investment as gauntlet-passed map; drax zeros to rank-0 for Loadout empty starting state)
- Cross-reference to Discipline #41 + #45

**Part 2 — seasonal_hero spec — LANDED at `canonical/story/seasonal-hero-h-5-hybrid-spec-2026-05-27.md`** (this commit).

Spec summary:
- **Q-Bundle-1 (algorithm) resolved:** composite substrate metric — w_quality·Q_norm + w_distinct·D_mahalanobis_norm + w_anchor·anchor_signal — initial weights (0.5, 0.3, 0.2); Cycle 14 calibration; revision per Discipline #18 substrate-led empirical justification
- **Q-Bundle-2 (canonical path) resolved:** companion spec at `canonical/story/` (rationale: seasonal_hero is cross-cutting Phase 4 → 5 → drax surface concept; better as companion spec doc 49 cross-references than further inflating doc 49 Loadout/Sample architecture scope)
- **Q-Bundle-3 (workflow) resolved:** gandalf-autonomous selection within Discipline #43 audit authority is default; Pattern-B Matt design-call escalation reserved for 4 specific triggers (near-tied scores; #41 substrate-led check fails; cross-season continuity concern; primary_faction_pair narrative conflict)
- **Phase 4 emission spec** (§ 4.1): new `seasonal_hero_candidates` table; gamora seam
- **Phase 5 PM-2 amendment** (§ 4.2): new `ExportSeasonHeroCandidates` Pydantic schema; star-lord seam
- **Wave 5 close emission** (§ 4.3): new `ExportSeasonHero` Pydantic schema; gandalf curation output
- **Drax surfacing** (§ 6): Summary tab seasonal hero card; D-Sharpened invariance preserved; Discipline #45 vocabulary lock at player surface
- **Star-lord telemetry** (§ 6.4): cross-season aggregation + drift watch
- **Discipline #41 LOAD-BEARING verified** (§ 3.3 + § 3.4 + § 7.1): all 3 composite signals substrate-emergent; no pre-authored taxonomy
- **Risks + Watch Items** (§ 8): D-2 faction-taxonomy creep watch; D-4 LLM-as-oracle creep watch; narrative-coherence vs substrate-emergence tension; weight revision implicit-pillar drift watch

**Framing-audit (Discipline #42) — PASS:**
- Q1: dispatch presupposes no pre-authored taxonomy; substrate metric is substrate-emergent
- Q2: substrate-led discipline implies substrate produces top-3; gandalf curates within constraint
- Q3: no framing-refusal triggered

**Downstream unblocked:**
- Dispatch B drax Loadout Phase A impl (rank-0 empty-state semantics from doc 49 § 1.1.1)
- Phase 4 emission impl dispatch (gamora; seasonal_hero_scorer module + table DDL per § 4.1)
- Phase 5 PM-2 amendment dispatch (star-lord; ExportSeasonHeroCandidates schema per § 4.2)
- Dispatch C drax Summary tab redesign (seasonal hero card + composition with Path III F-C surfaces per § 6.1 + § 6.2)
- Wave 5 close gandalf OP § 4 amendment (selection workflow + audit-log entry template; queued)
- Ground-state oracle § 1 amendment (queued — knight-rider routing per canonical-doc-format skill)

**Acceptance criteria — all checked:**
- [x] doc 49 § 1.1 (a) rank-0 clarification landed
- [x] seasonal_hero_candidates design spec authored at canonical path (`canonical/story/seasonal-hero-h-5-hybrid-spec-2026-05-27.md`)
- [x] Phase 4 emission spec + Phase 5 amendment + gandalf design-call workflow + drax surfacing semantics specified
- [x] Discipline #41 substrate-led verified at H-5 hybrid top-3 selection (§ 3.3 + § 3.4 + § 7.1)
- [x] D-Sharpened invariance preserved at seasonal hero surface (§ 4.3 + § 6.1)
- [x] Risks + Watch Items embedded (§ 8)
- [x] Completion record + commit + push (2 commits / 2 pushes per incremental-write discipline)

**Signal to KR:** doc 49 § 1.1.1 amendment LANDED + seasonal_hero_candidates H-5 hybrid spec READY for downstream Phase 4 emission impl + Phase 5 PM-2 amendment + drax Dispatch C surface impl.
