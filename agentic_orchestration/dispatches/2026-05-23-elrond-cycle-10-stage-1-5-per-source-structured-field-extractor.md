# Cycle 10 Stage 1.5 — Per-Source Structured-Field Extractor (elrond + gandalf)

**Cycle:** 10 — Substrate Curation Multi-Stage Dispatch
**Stage:** 1.5 of 4 (parallel with Stage 1)
**Owners:** elrond (lead — extractor authoring + DB write) + gandalf (named-historical-figure seed list curation + 30-row spot-check)
**Author:** knight-rider (orchestrator)
**Date:** 2026-05-23
**Status:** **DRAFT — fire-ready on Stage 0 transcription landing.** GATED on Matt + gandalf Stage 0 design call completion.
**Routing source:** `agentic_orchestration/gandalf/requests/2026-05-23-knight-rider-substrate-curation-multi-stage-dispatch.md` § Stage 1.5
**State file:** `agentic_orchestration/weapon-substrate-curation-cycle-10-state.md`

---

## 0. TL;DR

Mine the rich-structured-field sources (~50% of substrate; ~32K rows) for **named-bearer attribution + materials + provenance + dimensions + historical-use**. Cross-purpose: feeds Stage 2 cross-tab refinement, Stage 2.5 quality scoring, AND Track M1 substrate-spine bearer mining (cost reduction on future M1 web-crawl scope).

**Empirical criterion for completion:** extractor script lands; rich-source rows have populated extraction columns; gandalf 30-row spot-check pass validates extraction sanity; `extracted_named_bearer` column populated for ≥500 rows (Track M1 mining floor per dispatch § 3 Stage 1.5).

**Parallelism:** fires in parallel with Stage 1 (cheap proxy mechanical fingerprint). Both gate on Stage 0.

---

## 1. Required reading

1. `canonical/00-ground-state.md` § 1 (current truth)
2. `agentic_orchestration/gandalf/requests/2026-05-23-knight-rider-substrate-curation-multi-stage-dispatch.md` § Stage 1.5 + § 5 (cross-cutting disciplines)
3. `agentic_orchestration/elrond/research/phase-D-cleaning-pipeline-2026-05-23/` + `phase-D-bis-step-6-6-2026-05-23/` — Phase D + D-bis cleaning provenance (existing per-source schema understanding)
4. **`canonical/story/v1-bc-target-intent-2026-05-24.md` (Stage 0 transcription — LANDED 2026-05-24)** — Sketch D cultural-tradition distribution + Sketch F named/unnamed form ratio target (~32% named-personage / ~68% engine-named-original; ~12 named forms across ~37). **Sketch F § 6.1 enumerates 12 named-bearer anchor candidates** for v1: Arthur, Roland, Hattori Hanzō, Lu Bu, Thor, Achilles, Cú Chulainn, Moctezuma+Quetzalcoatl-nested, Cleopatra, Karna, Baba Yaga, Gilgamesh. **Seed list scope should explicitly include these 12 + tradition-coherent surrounds; remaining 488-1988 entries fill broadly-fictionalized traditions per Sketch D distribution.**
5. **`canonical/story/marginal-lineage-tagging-pattern-2026-05-23.md`** — Mode A/B/C/D tagging-vocabulary collapse pattern; informs the named-bearer extraction discipline (Mode A cultural-tradition matches preferred; Mode B/C/D filtered with rep-audit per Discipline #25)

---

## 2. Inputs

- Per-source `structured_properties` JSON schemas for 6-8 rich-source libraries:
  - Met Museum (~870 char avg structured_properties)
  - Odin Army Tradoc (military-modern; 4000+ char descriptions)
  - OSRSbox (Old School RuneScape; game-data structured)
  - Wikipedia (infobox-derived; varies per article)
  - royal_armouries (museum-curated; ~350 char structured_properties)
  - Soulslike fextralife (game-data; Dark Souls family, Elden Ring, Demon's Souls)
  - WoW Classic (game-data structured)
  - Cataclysm DDA (post-apocalyptic TRPG structured)
- Per-source curation notes from elrond Phase D documentation
- **gandalf-curated seed list of 500-2000 named-historical-figures** spanning broadly-fictionalized traditions (Arthurian / Norse / Greek / Celtic / Finnish / Vedic / Mesopotamian / Egyptian / Chinese / Japanese folklore / Slavic / Mesoamerican / etc.) — file at `agentic_orchestration/gandalf/notes/2026-05-23-named-historical-figure-seed-list.md` (gandalf authors at Stage 1.5 prep)

---

## 3. Outputs

**Schema extension on `weapon_knowledge_entries`:**

```sql
ALTER TABLE weapon_knowledge_entries ADD COLUMN extracted_length_value REAL;
ALTER TABLE weapon_knowledge_entries ADD COLUMN extracted_length_unit TEXT;
ALTER TABLE weapon_knowledge_entries ADD COLUMN extracted_weight_value REAL;
ALTER TABLE weapon_knowledge_entries ADD COLUMN extracted_weight_unit TEXT;
ALTER TABLE weapon_knowledge_entries ADD COLUMN extracted_materials TEXT;       -- JSON array or comma-separated
ALTER TABLE weapon_knowledge_entries ADD COLUMN extracted_named_bearer TEXT;    -- preserves source phrasing
ALTER TABLE weapon_knowledge_entries ADD COLUMN extracted_provenance_richness REAL;  -- 0.0-1.0
ALTER TABLE weapon_knowledge_entries ADD COLUMN extracted_historical_use TEXT;  -- NULL where absent
```

**Artifact deliverables:**
- Extractor script: `agentic_orchestration/elrond/research/cycle-10-stage-1-5-2026-05-XX/extract_structured_fields.py` (per-source branch logic; background execution per Discipline #19)
- Per-source schema mapping document: `cycle-10-stage-1-5-2026-05-XX/per-source-schema-mapping.md`
- Named-bearer match log: `cycle-10-stage-1-5-2026-05-XX/named-bearer-matches.json` (every match with regex + source phrasing + entry_id)
- gandalf 30-row spot-check artifact across sources: `cycle-10-stage-1-5-2026-05-XX/spot-check-gandalf-2026-05-XX.md`
- Track M1 cost-reduction estimate memo: `cycle-10-stage-1-5-2026-05-XX/track-m1-mining-dividend.md` (estimated mineable-bearer-attribution candidates count for future M1 web-crawl scope reduction)

---

## 4. Method notes

- **Per-source schema mapping is the unavoidable upfront cost.** Each rich source has different field names + structures. Build a per-source extractor in a single elrond script with per-source branch logic. Concentrate on rich sources first (~32K rows covered). Sparse sources (Wikidata, most TRPG) get NULL extractions cheaply.
- **Named-bearer extraction is the highest-value signal.**
  - Regex patterns + structured-field lookup
  - Met Museum: `object_history` field; Wikipedia infobox often `associated_persons` or `used_by`
  - Match against curated 500-2000-entry named-historical-figure list (gandalf authors seed list)
  - Preserve source phrasing (e.g., "Saladin", "Charlemagne", "attributed to Masamune") — downstream curation decides canonical form
  - Multi-match acceptable (list separator); single-match preferred
- **Materials extraction:**
  - Met Museum `medium` field; royal_armouries `materials`; Soulslike `crafting_materials`
  - Comma-separated string OR JSON array (decide per source consistency); rare/exotic materials (rhino-horn ivory, jade, mithril, obsidian) flagged for Stage 2.5 quality bonus
- **Provenance richness:** composite metric measuring source-attribution field density (`object_history`, `provenance`, `cultural_context`, `archaeological_context` fields). Range 0.0-1.0; museum sources typically 0.6+; community-scraped 0.0-0.3.
- **Historical use:** prose extraction (e.g., "Battle of Hastings 1066", "exhibited at Royal Tournament 1850"). NULL acceptable for most rows.

---

## 5. Cross-seam impact

- **Substrate DB schema change** (8 new columns on `weapon_knowledge_entries`) — same MIGRATION.md check as Stage 1 (per ADR-004).
- **No row deletion or destructive curation** — additive only.
- **Cross-purpose value for Track M1:** bearer-attribution column directly feeds future M1 substrate-spine work without re-crawling. Track M1 future dispatch can reference this output via DB query rather than independent web crawl. Estimated cost reduction logged in Track M1 mining dividend memo.

---

## 6. Out of scope (explicit)

- NOT damage-amplitude / damage-spread axis — Stage 4 territory
- NOT Stage 1 proxy mechanical fingerprint — separate parallel dispatch
- NOT methodology consultation per Discipline #18 — Stage 1.5 is per-source schema extraction; NOT a methodology hotspot
- NOT v1_scope flag population — Stage 3 territory
- NOT canonical_name modification or country-title cleanup — Recognition 2 v1.1+ deferred; this dispatch flags candidates via `extracted_provenance` columns without modifying canonical_name
- NOT Track M1 firing — Track M1 dispatch remains 02-roadmap § 3.6 deferred; Stage 1.5 produces mining dividend ONLY
- NOT cohesion-judge / LLM-judge calls on extraction quality — extractor is regex + structured-field-lookup only

---

## 7. Tag intent

`elrond/v0.0-cycle-10-stage-1-5-structured-field-extraction` after acceptance criterion met + gandalf 30-row spot-check pass + named-bearer ≥500 rows.

---

## 8. Smoke-test expectation

Per Discipline #2:
- Pre-execution smoke: 50-row dry-run on Met Museum sample; verify extractor produces non-empty columns where expected; verify named-bearer regex catches obvious candidates (e.g., "Halberd of Archduke Ferdinand II" → `extracted_named_bearer="Archduke Ferdinand II"`)
- Post-execution smoke: per-source coverage histogram — Met Museum should populate 80%+ of length/weight/materials columns; community-scraped sources should populate 10-30%

Per Discipline #2.1 resource-bounds projection:
- 32K rich-source rows × per-row regex scan + structured-properties JSON parse + named-bearer match against 500-2000-entry seed list = ~5-10 minutes total (Python single-process; manageable)
- Background execution per Discipline #19 — `nohup python extract_structured_fields.py > log.out 2>&1 &`
- DB write cost: 32K × 8-column UPDATE = ~1-2 min batched; acceptable

---

## 9. Gate routing

- **No Gate-1 review required for this dispatch** — Stage 1.5 is per-source schema extraction with no methodology hotspot, no architectural commitment. Cross-purpose Track M1 dividend is documented but does NOT trigger M1 firing.
- **No Gate-2 review at Stage 1.5 boundary** — output consumed by Stage 2 + 2.5 which fold into Stage 3 design-call review.
- **gandalf 30-row spot-check** + **named-bearer ≥500 rows floor check** serve as cheapest-refuting-tests per Discipline #19.1.

---

## 10. Cycle context

- This is one of 9 stages in Cycle 10. Fires AFTER Stage 0 design call (Matt scheduling). Fires in PARALLEL with Stage 1.
- Stages 2 + 2.5 gate on Stage 1 + 1.5 completion.
- Gandalf named-historical-figure seed list authoring is a prep task BEFORE Stage 1.5 fires; can be authored during Stage 0 design-call window in parallel.

---

## 11. Cross-references

- Dispatch source: `agentic_orchestration/gandalf/requests/2026-05-23-knight-rider-substrate-curation-multi-stage-dispatch.md` § Stage 1.5
- State file: `agentic_orchestration/weapon-substrate-curation-cycle-10-state.md`
- Phase D cleaning provenance: `agentic_orchestration/elrond/research/phase-D-cleaning-pipeline-2026-05-23/` + `phase-D-bis-step-6-6-2026-05-23/`
- Substrate DB: `/Users/admin/Games/reincarnated-loadout/data/telemetry.db`
- Engineering disciplines: `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#2, #2.1, #19, #19.1, #21, #22)
- Future Track M1 cost-reduction beneficiary: `canonical/02-roadmap.md` § 3.6

---

## 12. Sign-off

**Author:** knight-rider (orchestrator)
**Date:** 2026-05-23
**Authority:** Matt 2026-05-23 — direct authorization of parent dispatch
**Status:** **DRAFT — FIRE-READY** pending Stage 0 transcription + gandalf named-historical-figure seed list authoring
**Owners:** elrond (lead) + gandalf (seed list + 30-row spot-check)
