# Dispatch — legolas: Weapon Library Import Discovery + SQL Schema Proposal

**Date:** 2026-05-22 (evening)
**Author:** gandalf (commissioning research; design-side)
**Recipient:** legolas (Mode A + Mode B mixed; web library enumeration + metadata analysis + schema design)
**Authority:** Matt 2026-05-22 (this session) — explicit fire authorization following architectural pivot from "15-entry hand-authored gear catalogue" to "vast queryable weapon library populating a greenfield SQLite DB"
**Priority:** HIGH — load-bearing for tomorrow's canonical doc authoring (engine-as-general-product + gear-heavy promotion) + P1 substrate-enrichment scoping + W1.15 rocket implementation
**Estimated effort:** 3-3.5 days bounded scope (social-media sweep deferred to second commission)
**Mode:** A + B mixed — analytical research on library landscape + catalogue crawl for scale/metadata + design-grade schema authoring
**Fire condition:** none; pre-authorized; Matt direct fire 2026-05-22 evening

---

## 0. TL;DR

Matt has pivoted gear-substrate architecture from "15-entry hand-authored catalogue" to **"vast queryable weapon library populating a greenfield SQLite DB at `/Users/admin/Games/reincarnated-loadout/data/telemetry.db`."** The DB is confirmed empty (0 bytes, no schema, no React/Vite cross-references) — true greenfield import target.

The architectural elegance: gear becomes a real substrate space (queryable; substrate-vector-matching predicates pull candidate weapons; density-routing fills empty regions via Meshy gap-fill) rather than a controlled-space proxy (15 hand-picked categories). More substrate-as-cohesion-coherent.

**Five-priority commission:**

| # | Priority | Effort |
|---|---|---|
| 1 | Web library enumeration (Sketchfab, OGA, Smithsonian, TurboSquid, CGTrader, Free3D, Clara.io, BlendSwap, itch.io, Wikidata, Wikipedia taxonomy) | ~1 day |
| 2 | Metadata field analysis (per-library tag normalization plan) | ~0.5 day |
| 3 | SQL DDL proposal for the empty DB (core weapon entity + tag tables + source provenance + sim-property fields + aesthetic-tuple fields + indexing) | ~0.5-1 day |
| 4 | Selection-pattern design (parameterized queries; substrate-vector → candidate-weapon-set; density-routing-to-Meshy-on-empty) | ~0.5 day |
| 5 | Import strategy recommendation (which libraries first; what scale; license-tier prioritization; phased plan) | ~0.5 day |

**Out of scope (deferred to second commission):**
- Social-media sweep (ArtStation, DeviantArt, Twitter, Discord) — yields reference images for Meshy gap-fill input pipeline, not direct DB import targets; second commission after core import is operational
- Actual import execution — this dispatch is discovery + schema design only; execution dispatch follows once schema is approved

---

## 1. Priority 1 — Web library enumeration

### 1.1 Target libraries

Enumerate weapon coverage across each, with for-each: **scale** (approx model count for weapons), **licensing** (CC0 / CC-BY / commercial / mixed; how license breakdowns work), **downloadability** (free API? per-asset download? bulk download permitted?), **format support** (FBX / GLB / OBJ / USD / STL), **metadata fields exposed** (tags / categories / descriptions / authorship).

Major candidates:

| Library | Why it's a target |
|---|---|
| **Sketchfab** | ~10M total models; large weapon coverage; CC0/CC-BY subset substantial; API available |
| **Open Game Art (OGA)** | Game-focused; CC0/CC-BY licensing; free; smaller catalogue but high signal |
| **Smithsonian Open Access** | Historical real weapons; CC0; museum-grade; cultural authenticity for non-Western registers |
| **TurboSquid** | Commercial; large weapon coverage; per-asset licensing terms vary |
| **CGTrader** | Commercial + free mix; large coverage |
| **Free3D** | Free models; smaller catalogue; mixed quality |
| **Clara.io** | Free models; CC licensing options |
| **BlendSwap** | Blender community; CC0/CC-BY; smaller but quality |
| **itch.io 3D bundles** | Indie game-asset packs; bundle pricing |
| **Wikidata Q-items** | Semantic web — weapon taxonomy by Q-item; NOT models but ontology for tag schemas |
| **Wikipedia weapons categories** | Taxonomy reference for cultural / temporal / mechanical classification |

Other libraries you encounter during the sweep — add them with confidence flags.

### 1.2 Library scoring framework

For each library, produce a one-paragraph summary + a structured row:

```
Library: <name>
Total models (weapon-tagged or estimated): <count>
Licensing breakdown: <CC0 X% | CC-BY Y% | commercial Z%>
Downloadability: <API | per-asset | bulk-permitted | manual-only>
Format support: <FBX | GLB | OBJ | etc.>
Metadata fields exposed: <tags | category | description | era | material | etc.>
Aesthetic register coverage:
  - medieval-European: <strong | moderate | thin | empty>
  - medieval-East-Asian: <...>
  - medieval-South-Asian: <...>
  - industrial: <...>
  - advanced/sci-fi: <...>
  - primitive: <...>
  - other cultural lineages: <...>
Confidence: <HIGH | MEDIUM | LOW> with rationale
Priority tier for import: <Tier 1 | Tier 2 | Tier 3 | defer>
```

---

## 2. Priority 2 — Metadata field analysis

### 2.1 The normalization problem

Each library exposes different metadata. Sketchfab uses free-text tags + categories; Smithsonian uses formal museum cataloguing; Wikidata uses semantic-web Q-items. To populate ONE DB with weapons from multiple libraries, we need a **canonical tag schema** that all sources map into.

### 2.2 Research questions

1. **What tags/properties does each library expose?** (Document per Priority 1 entry.)
2. **What canonical tag schema unifies them?** Propose a canonical schema with:
   - Mechanical properties (range, geometry, timing-class, charge-class, accuracy-class, rhythm-class) — these drive sim-viability and substrate-vector matching
   - Aesthetic tuple (tech_level × tone × cultural_lineage) — these drive cohesion-judge thematic-identity assignment
   - Source provenance (library origin, asset ID, license, download URL, preview image URL, license-compliance notes)
   - Asset-readiness flags (ready-to-import | needs-conversion | needs-Meshy-regenerate | sim-viability-unverified)
3. **Per-library tag normalization plan** — how does each library's native taxonomy map into the canonical schema? Where are mappings clean? Where are mappings lossy?
4. **Ontology reference** — does Wikidata's weapon Q-tree give us a backbone taxonomy? Where does it fall short?

### 2.3 Deliverable structure

`metadata-normalization.md` containing:
- Canonical tag schema specification (field-by-field)
- Per-library normalization mapping table
- Gaps and lossy mappings flagged explicitly

---

## 3. Priority 3 — SQL DDL proposal for the empty DB

### 3.1 Greenfield context

The target DB is **empty** (`/Users/admin/Games/reincarnated-loadout/data/telemetry.db`; 0 bytes; verified 2026-05-22 evening). No migration concerns. No existing React/Vite cross-references.

Design the schema from scratch with these constraints:
- SQLite (lives in loadout repo)
- Performant for substrate-vector-matching queries (likely 10-100K weapons after import; indexing matters)
- Supports many-to-many tag relationships (a weapon can have many tags; a tag applies to many weapons)
- Supports per-library source provenance + license tracking
- Supports sim-property fields directly (range / geometry / timing) plus aesthetic-tuple fields directly (tech × tone × culture)
- Supports asset-readiness flags + Meshy-regenerate flag

### 3.2 Deliverable structure

`sql-ddl-proposal.md` containing:
- Entity-relationship diagram (text-art or markdown table)
- Full CREATE TABLE statements with column types + constraints + indexes
- Justification per non-obvious decision
- Migration considerations (in case the DB gets re-populated later)

PLUS `schema.sql` — the actual DDL ready to run against the empty DB once approved.

### 3.3 Core table candidates (proposed; refine in your research)

```
weapons              -- core entity; one row per imported weapon
weapon_tags          -- many-to-many; arbitrary metadata tags
weapon_sources       -- per-weapon source provenance (library, asset_id, license, URLs)
weapon_sim_props     -- range/geometry/timing/charge/accuracy/rhythm
weapon_aesthetic     -- tech_level/tone/cultural_lineage tuple per weapon
weapon_readiness     -- asset-readiness state machine
libraries            -- library registry with API metadata
licenses             -- license-tier registry
tag_taxonomy         -- canonical tag schema (controlled vocabulary)
```

Adjust as your analysis surfaces better structure.

---

## 4. Priority 4 — Selection-pattern design

### 4.1 What the engine queries against

The substrate-as-cohesion architecture means: given a kit's converged identity (dominant_element + range_profile + stat_distribution_signature + emergent BC signature), the gear-substrate derivation queries the library for candidate weapons matching the substrate-vector.

### 4.2 Research questions

1. **What does a substrate-vector-to-candidate-weapon-set query look like?**
   - Input: substrate-vector (e.g., `(fire, ranged, INT-dominant)` plus aesthetic preference `(medieval, heroic, European)`)
   - Output: ordered candidate weapon set with match-scores
   - Query structure: parameterized SQL with substrate-property filters + aesthetic-tuple filters + sim-property compatibility filters + license-tier filters

2. **What does density-routing look like in this schema?**
   - If candidate-set is empty (N=0), route to Meshy gap-fill
   - If candidate-set is sparse (N<3), flag low-density region for prioritized Meshy gap-fill
   - If candidate-set is dense (N>10), use ranking/scoring to pick from top candidates
   - Engine consumes this routing decision deterministically

3. **What scoring/ranking sits inside the query?**
   - Mechanical-property fit (does the weapon's range/geometry/timing match the substrate-vector?)
   - Aesthetic-tuple fit (does the aesthetic match? exact | secondary | cross-aesthetic-allowed?)
   - License-tier preference (CC0 preferred; CC-BY accepted; commercial gated)
   - Asset-readiness preference (ready-to-import preferred over needs-Meshy-regenerate)

4. **What's the BDI ω/τ formalism interaction?**
   - The BDI ω-table predicts mechanical-overlap β-magnitude per gear × element pair
   - Selection queries should respect ω predictions (high-ω pairs are canonical matches; low-ω pairs are novel-but-valid)
   - Per the BDI v1 doc at `canonical/story/bdi-omega-tau-tables-v1-2026-05-22.md`

### 4.3 Deliverable structure

`selection-patterns.md` containing:
- ~5-10 example parameterized queries (substrate-vector → candidate-weapon-set)
- Density-routing rules
- Scoring/ranking framework
- BDI ω/τ integration sketch
- Query-performance considerations (indexing implications for the DDL)

---

## 5. Priority 5 — Import strategy recommendation

### 5.1 Research questions

1. **Which libraries first?**
   - Tier 1 import: highest signal-to-noise; cleanest licensing; covers dominant aesthetic register (medieval-European)
   - Tier 2 import: adds aesthetic diversity (East-Asian; grim; South-Asian)
   - Tier 3 import: completeness sweeps (Smithsonian for cultural authenticity; Wikidata for ontology)

2. **What scale per library?**
   - Full crawl (everything available)?
   - Curated subset (top-N by quality / license-fitness)?
   - Tag-filtered (only weapon-tagged assets)?

3. **License-tier prioritization?**
   - CC0 (no attribution required; ideal for inclusion in shipping product)
   - CC-BY (attribution required; manageable for indie distribution)
   - Commercial (per-asset license fees; only for high-value weapons that can't be sourced free)
   - Reject: GPL (incompatible with closed-source distribution), CC-NC (non-commercial), no-license-declared

4. **What's the import phasing?**
   - Phase A: schema lock + Tier 1 library import (proof of pipeline)
   - Phase B: Tier 2 libraries (aesthetic expansion)
   - Phase C: Tier 3 libraries (completeness)
   - Phase D: Meshy gap-fill against the density map

### 5.2 Deliverable structure

`import-strategy.md` containing:
- Recommended Tier 1/2/3 library assignments with rationale
- Per-tier scale targets
- License-tier policy
- Four-phase import sequence (A-D)
- Estimated import compute + time per phase

---

## 6. Deliverable summary

Single directory: `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/`

| File | Content |
|---|---|
| `library-enumeration.md` | Priority 1 findings; library inventory with scale/license/format/metadata per library |
| `metadata-normalization.md` | Priority 2 canonical tag schema + per-library normalization mappings |
| `sql-ddl-proposal.md` | Priority 3 schema rationale + ERD + table structure justification |
| `schema.sql` | Priority 3 DDL ready to run against the empty DB |
| `selection-patterns.md` | Priority 4 query templates + density-routing rules + scoring framework |
| `import-strategy.md` | Priority 5 phased import plan + license-tier policy |
| `findings-summary.md` | Headline conclusions + cross-references |

Length budget per file: ~1000-3000 words depending on coverage. Total: 8000-15000 words.

---

## 7. Out of scope (for this dispatch)

- **Social-media sweep.** ArtStation / DeviantArt / Twitter / Discord yield *reference images* for Meshy gap-fill input pipeline, not direct DB import targets. Treat as second commission after this one closes.
- **Actual import execution.** This dispatch is discovery + schema design only. Import dispatches follow once schema is reviewed + approved.
- **Engine-side query implementation.** Implementation is rocket / drax territory; this dispatch produces specifications they consume, not the implementation itself.
- **Meshy gap-fill infrastructure.** Per legolas's prior commission findings, Meshy gap-fill is the density-routing destination; this dispatch sketches the integration point but doesn't build the infrastructure.

---

## 8. Downstream consumers

1. **gandalf** — folds findings into tomorrow's canonical authoring (engine-as-general-product doc + gear-heavy promotion doc); updates the asset-pipeline-meshy-swap doc with vast-library framing
2. **Matt** — reviews schema proposal + license-tier policy + import strategy; approves before any execution commissions fire
3. **rocket** — consumes the SQL schema + selection-pattern specs when W1.15 implementation begins
4. **drax** — consumes the schema for any loadout-app-side queries (since the DB lives in the loadout repo)
5. **knight-rider** — relays import execution commissions (one per phase) once strategy is approved
6. **Future commission (legolas Mode B social-media sweep)** — second commission after this one's findings inform what Meshy gap-fill targets need

---

## 9. Critical context

**Architectural framing:**
- Substrate-as-cohesion architectural commitment (post-W0.2)
- Gear is a real substrate space; library populates the substrate space
- Density-routing pattern (catalogue density determines library vs. Meshy gap-fill)
- 7-element substrate (fire / water / earth / wind / lightning / holy / shadow)
- Aesthetic tuple (tech_level × tone × cultural_lineage)
- Mechanical properties (range / geometry / timing / charge / accuracy / rhythm) drive sim-viability
- Gear-heavy v1 (gear-LITE framing retired; gear as real mechanical substrate)
- Variant C engine architecture (general engine with profile-overlay flags)

**Build on, don't re-derive:**
- `agentic_orchestration/legolas/research/unity-catalogue-armor-meshy-2026-05-22/` — your prior Unity Asset Store crawl (covers one library; this commission expands to many libraries)
- `agentic_orchestration/legolas/research/meshy-pipeline-2026-05-22/findings.md` — Meshy pipeline confirmation (Meshy gap-fill is the density-routing destination)
- `canonical/story/gear-substrate-rule-table-v1-2026-05-22.md` — the 15-gear catalogue; under vast-library framing, these likely emerge as natural clusters in the imported data rather than being pre-imposed

**Discipline #19 RATIFIED 2026-05-22 (engine commit `0d1ad63`):**
- You run as a bounded sub-agent with explicit deliverable directory
- No babysit pattern; no Agent invocations of your own for waiting
- If you need long-running web fetches, run them directly via WebFetch or Bash
- Cross-session continuity is your findings directory at the canonical path

---

## 10. Cross-references

- `/Users/admin/Games/reincarnated-loadout/data/telemetry.db` — target DB (confirmed empty greenfield 2026-05-22)
- `agentic_orchestration/legolas/research/unity-catalogue-armor-meshy-2026-05-22/findings-summary.md` — Unity catalogue prior findings
- `agentic_orchestration/legolas/research/meshy-pipeline-2026-05-22/findings.md` — Meshy pipeline capability research
- `canonical/story/gear-substrate-rule-table-v1-2026-05-22.md` — 15-gear catalogue (pre-vast-library framing)
- `canonical/story/gear-as-substrate-2026-05-21.md` — original substrate commitment
- `canonical/story/bdi-omega-tau-tables-v1-2026-05-22.md` — BDI ω/τ tables (Priority 4 selection-pattern integration)
- `canonical/story/multi-dim-convergence-algorithm-2026-05-21.md` — math note (substrate-vector definitions)
- `~/Games/reincarnated-engine/src/reincarnated/generation/element_biases.py:28` — ELEMENT_SCALING_ATTRIBUTE canonical
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § 19 — RATIFIED 2026-05-22

---

**Signed:** gandalf (story-and-design steward; research commissioner)
**For:** vast-weapon-library import discovery + greenfield SQL schema design + selection-pattern specification — load-bearing for gear-heavy v1 substrate architecture under Matt's 2026-05-22 pivot to vast queryable substrate space.
