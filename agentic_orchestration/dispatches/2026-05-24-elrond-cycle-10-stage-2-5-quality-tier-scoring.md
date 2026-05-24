# Cycle 10 Stage 2.5 — Per-Row Quality / Uniqueness / Flavor Composite Scoring + Tier S/A/B/C (elrond + gandalf)

**Cycle:** 10 — Substrate Curation Multi-Stage Dispatch
**Stage:** 2.5 of 4 (post-Wave-2 gate; fires parallel with Stage 2)
**Owners:** elrond (substrate seam — scoring script + DB write) + gandalf (source-library reputation tier curation + named-mythological-match logic + 100-row spot-check)
**Author:** knight-rider (orchestrator)
**Date:** 2026-05-24
**Status:** **DRAFT — fire-ready post-Matt-commit-tag (Option B).** Gates on Wave 2 combined commit + tag landing.
**Routing source:** `agentic_orchestration/gandalf/requests/2026-05-23-knight-rider-substrate-curation-multi-stage-dispatch.md` § Stage 2.5
**State file:** `agentic_orchestration/weapon-substrate-curation-cycle-10-state.md`

---

## 0. TL;DR

Produce per-row composite quality / uniqueness / flavor score + tier assignment (S / A / B / C) so Stage 3 sampling can protect exceptional items via tier-pre-commit. Composite signal sources: source-library reputation + description richness + Stage 1.5 extracted-properties signals + cluster centrality + named-mythological-match (using gandalf seed list — already authored). Tier S auto-includes via named-mythological-corpus match OR top-1% composite score.

**Empirical criterion for completion:** scoring script lands; all 69,137 rows scored; tier assignments distributed roughly per proposed defaults (Tier S ~1-3% / Tier A ~7-10% / Tier B ~50-70% / Tier C ~20-30%); gandalf 100-row review across tiers validates score sanity (especially Tier S — does the auto-include list look right; do obvious flavor-load items land in Tier C wrongly).

**Parallelism:** fires in parallel with Stage 2 (cross-tab surfacing).

**Gandalf prep dependency:** source-library reputation tier lookup needs gandalf authorship before scoring fires; can author during Stage 2 execution window (~1 hr task; non-blocking on Stage 2.5 start IF elrond can run reputation-tier-as-NULL first then fill once gandalf lands).

---

## 1. Required reading

1. `canonical/00-ground-state.md` § 1 (current truth)
2. `agentic_orchestration/gandalf/requests/2026-05-23-knight-rider-substrate-curation-multi-stage-dispatch.md` § Stage 2.5 (the spec — including cultural-sensitivity stratification reference)
3. `canonical/story/v1-bc-target-intent-2026-05-24.md` § 6 Sketch F (named/unnamed form ratio + 12 anchor candidates + Tier 1/2/3 cultural-sensitivity stratification per § 6.3)
4. `agentic_orchestration/gandalf/notes/2026-05-24-named-historical-figure-seed-list.md` (680-entry seed list — Tier S auto-include match source; Sketch F 12 anchors enumerated)
5. `canonical/story/marginal-lineage-tagging-pattern-2026-05-23.md` (Discipline #25 semantic-layer rep-audit applies at Tier S auto-include match)
6. `agentic_orchestration/elrond/research/cycle-10-stage-1-2026-05-24/` (Stage 1 + v1.1 fingerprint — confidence + bin distribution)
7. `agentic_orchestration/elrond/research/cycle-10-stage-1-5-2026-05-24/` (Stage 1.5 extraction — provenance richness + named_bearer + materials)
8. `agentic_orchestration/elrond/research/phase-E-pattern-6-2026-05-23/` (Phase E cluster_id + within-cluster centrality)
9. `agentic_orchestration/operating-procedures/critique-pair-gate-protocol.md` (Q-B verdict § 3.2 cultural-sensitivity stratification — Tier S/A auto-inclusion must respect Tier 1/2/3 boundaries per `canonical-doc-format` spec)

---

## 2. Inputs (signal sources for composite score)

| Signal | Source | Weight (proposed default; design-call may adjust) |
|---|---|---|
| Source-library reputation tier | gandalf-curated lookup (museum-curated > designer-curated > community-scraped > game-data-dump) | 0.20 |
| Description richness | `description_text` length + structured-property field density | 0.15 |
| Extracted provenance richness | Stage 1.5 `extracted_provenance_richness` REAL 0.0-1.0 | 0.10 |
| Extracted named-bearer signal | Stage 1.5 `extracted_named_bearer` (non-NULL = bonus) | 0.15 |
| Extracted materials rarity | Stage 1.5 `extracted_materials` (multi-material / rare exotics like jade/obsidian/mithril) | 0.10 |
| Cultural-lineage depth | `cultural_lineage_tags` array depth + `genre_appearances` length + `related_entries` count | 0.10 |
| Image presence | `knowledge_entry_reference_images` JOIN count | 0.05 |
| Cluster centrality | Phase E-1 within-cluster distance to centroid (lower distance = higher centrality) | 0.10 |
| Cultural-tradition weight (Fate-genre rubric) | gandalf-curated lookup mapping cultural_lineage → Fate-genre weight | 0.05 |
| **TOTAL** | | **1.00** |

---

## 3. Outputs

**Schema extension on `weapon_knowledge_entries`:**

```sql
ALTER TABLE weapon_knowledge_entries ADD COLUMN quality_composite_score REAL;
ALTER TABLE weapon_knowledge_entries ADD COLUMN quality_tier TEXT CHECK (quality_tier IN ('S', 'A', 'B', 'C') OR quality_tier IS NULL);
ALTER TABLE weapon_knowledge_entries ADD COLUMN named_mythological_match TEXT;
```

**Tier assignment logic (proposed defaults; design call may adjust):**

| Tier | Inclusion logic | Estimated % |
|---|---|---|
| **S — Auto-include** | Named-mythological-corpus match (via gandalf seed list — broadly-fictionalized Tier 1 OR Tier 2 soft-attribution per Sketch F § 6.3) OR top 1% composite score | ~1-3% |
| **A — Preferred-include** | Top 10% composite score (excluding S) | ~7-10% |
| **B — Standard pool** | Standard composite range | ~50-70% |
| **C — Eligible but low priority** | Bottom composite quartile | ~20-30% |

**Cultural-sensitivity gate at Tier S/A:** apply Q-B verdict § 3.2 stratification — broadly-fictionalized traditions OK to name explicitly; marginalized-culture traditions (Tier 3 per Sketch F § 6.3) excluded; living-religious traditions excluded. **Stage 1.5 bearer-match seed list already enforces this at extraction time** (Tier 3 excluded from seed list); Stage 2.5 verifies no Tier 3 contamination at Tier S/A assignment.

**Discipline #25 rep-audit at Tier S auto-include:** for every named-mythological-match candidate, spot-check that the row's actual content matches the named entity (e.g., "Mjolnir" row content = mythological hammer, not Soviet missile codename). Stage 1.5 Mode-C contamination flags (72 rows) ALREADY identified — these rows do NOT get Tier S auto-include via named-mythological-match path (must qualify via top-1% composite score instead).

**Artifact deliverables:**
- Scoring script at `agentic_orchestration/elrond/research/cycle-10-stage-2-5-2026-05-24/score_quality_composite.py`
- Source-library reputation tier lookup at `agentic_orchestration/gandalf/notes/2026-05-24-source-library-reputation-tier.md` (gandalf authors as prep)
- Cultural-tradition weight lookup at `agentic_orchestration/gandalf/notes/2026-05-24-cultural-tradition-weight-lookup.md` (gandalf authors as prep; small ~30 entries)
- Per-tier count summary at `cycle-10-stage-2-5-2026-05-24/per-tier-counts.md`
- 100-row spot-check artifact for gandalf at `cycle-10-stage-2-5-2026-05-24/spot-check-gandalf-request.md` (sampled across tiers)

---

## 4. Method notes

- **Score normalization:** each signal normalized to 0.0-1.0 BEFORE weighted combination; weight sums to 1.0; final score 0.0-1.0
- **Tier threshold lookup:** computed empirically AFTER scoring (top 1% / top 10% / bottom quartile) rather than fixed absolute thresholds — adapts to substrate score distribution
- **Named-mythological-match:** uses Stage 1.5 `extracted_named_bearer` column directly (no re-regex pass — Stage 1.5 already did the work) + cross-check against gandalf seed list `tier` field (Tier 1/2 → eligible for Tier S; Tier 3 → blocked per cultural-sensitivity)
- **Mode-C contamination filter:** rows with Stage 1.5 `rep_audit_mode_c_naming_allusion_suspected` flag → NOT auto-include via named-mythological-match path; must qualify via composite score
- **Composite scoring weight curation:** gandalf curates initial weights; design-call may adjust at Stage 3
- **Methodology consult per Discipline #18 (OPTIONAL):** if design call surfaces uncertainty on weights, knight-rider routes ~30-60 min legolas Mode A literature scan on library-curation composite-scoring patterns BEFORE Stage 2.5 execution. Default: gandalf-authored weights, design-call review pass.

---

## 5. Cross-seam impact

- Substrate DB schema change (3 new columns on `weapon_knowledge_entries`) — same additive ADR-004 pattern as Stages 1 + 1.5; verify cross-seam consumers; MIGRATION.md if applicable
- No row deletion or destructive curation — additive only

---

## 6. Out of scope (explicit)

- NOT v1_scope flag population — Stage 3 territory
- NOT composition policy lock — Stage 3 design call
- NOT cross-tab + thin-cell surfacing — Stage 2 (parallel)
- NOT engine-authored gap-fills — Stage 3.5 territory
- NOT methodology consultation per Discipline #18 — SOFT hotspot (composite scoring weights); OPTIONAL legolas Mode A consult only if design-call surfaces uncertainty
- NOT new named-historical-figure seed-list authoring — gandalf already authored at Wave 2 prep; Stage 2.5 consumes
- NOT changes to existing Stage 1 fingerprint or Stage 1.5 extraction columns — additive only

---

## 7. Tag intent

`elrond/v0.0-cycle-10-stage-2-5-quality-tier-scoring` after acceptance criterion met + gandalf 100-row spot-check pass.

---

## 8. Smoke-test expectation

Per Discipline #2:
- Pre-scoring smoke: SELECT 100 random rows + manually estimate composite score for ~10 (high-richness museum-curated should score higher than community-scraped game-data-dump); run scoring on those 100; verify ~7/10 match estimate
- Post-scoring smoke: per-tier count distribution matches proposed defaults within ~5% (Tier S 1-3%; Tier A 7-10%; Tier B 50-70%; Tier C 20-30%); Tier S named-mythological-match list visually scannable by gandalf

Per Discipline #2.1 resource-bounds: 69K rows × ~10 signal computations + composite math = ~1-2 min single-process Python; trivial.

---

## 9. Gate routing

- **No Gate-1 review required** — Stage 2.5 is composite scoring + tier assignment; weights are gandalf-curated; design-call ratifies at Stage 3
- **gandalf 100-row spot-check** + per-tier count distribution check serve as cheapest-refuting-tests per Discipline #19.1
- Stage 3 design call IS the formal gate for composition policy + Stage 2.5 + Stage 2 outputs together

---

## 10. Cycle context

- Wave 3 — fires AFTER Wave 2 combined commit + tag (Option B) lands
- Parallel with Stage 2
- Output feeds Stage 3 design call (Wave 4)

---

## 11. Cross-references

- Dispatch source: `agentic_orchestration/gandalf/requests/2026-05-23-knight-rider-substrate-curation-multi-stage-dispatch.md` § Stage 2.5
- Stage 0 transcription: `canonical/story/v1-bc-target-intent-2026-05-24.md` § 6
- Marginal-lineage rep-audit: `canonical/story/marginal-lineage-tagging-pattern-2026-05-23.md`
- Seed list: `agentic_orchestration/gandalf/notes/2026-05-24-named-historical-figure-seed-list.md`
- State file: `agentic_orchestration/weapon-substrate-curation-cycle-10-state.md`
- Substrate DB: `/Users/admin/Games/reincarnated-loadout/data/telemetry.db`
- Engineering disciplines: `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#2, #2.1, #11, #18 [optional soft], #19, #19.1, #21, #22, #25)

---

## 12. Sign-off

**Author:** knight-rider (orchestrator)
**Date:** 2026-05-24
**Authority:** Matt 2026-05-23 — parent dispatch authorization
**Status:** **DRAFT — FIRE-READY post-Wave-2-commit-tag**
**Owners:** elrond (lead — scoring + DB write) + gandalf (reputation-tier + cultural-tradition-weight + 100-row spot-check)
