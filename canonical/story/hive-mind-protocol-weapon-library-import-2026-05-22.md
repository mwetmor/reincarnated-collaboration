# Hive-Mind Protocol — Weapon Library Import + Pattern-6 Axis Discovery + Emergent Clustering

> **STATUS:** CURRENT (load-bearing as of 2026-05-23) — see `canonical/00-ground-state.md`

**Date:** 2026-05-22 (evening session; canonical lock — elevated from operational plan to hive-mind-protocol status)
**Author:** gandalf (story-and-design steward; senior designer; planner — not orchestrator)
**Status:** v1 hive-mind-protocol — operationalizes the vast-library substrate pivot (Patterns 4-5-6 of six vestigial-pattern retirements) as a multi-phase coordinated hive workstream
**Authority:** Matt 2026-05-22 evening — "tee up for knight-rider and the hive mind. This is structural work."
**Estimated duration:** 1-3 weeks across phases; longer if Meshy bulk path requires partner outreach + onboarding
**Discipline:** #19 RATIFIED 2026-05-22 — all long-running phases as background processes; no Agent-tool monitoring; status via direct Bash + DB queries; JSON summary artifacts as cross-session continuity

**Parent protocol:** `canonical/story/hive-mind-protocol-qd-engine-rebuild-2026-05-21.md` v1.3 § 6.2 P1 substrate enrichment — this protocol is the substrate-enrichment workstream operationalized at hive-mind scale

**Companion docs:**
- `canonical/story/legacy-categorical-cleanup-audit-2026-05-22.md` — Patterns 4-5-6 audit (the architectural why)
- `canonical/story/gear-heavy-promotion-2026-05-22.md` — vast-library substrate architecture (the substrate-design what)
- `canonical/story/engine-as-general-serial-content-product-2026-05-22.md` — Variant C strategic lock (the strategic frame)
- `canonical/story/stat-derivation-from-bc-convergence-2026-05-22.md` — stat-derivation (downstream consumer of substrate)
- `canonical/story/asset-pipeline-meshy-swap-2026-05-22.md` — Phase D Meshy gap-fill canonical pipeline

**Source operational plan:** `agentic_orchestration/weapon-library-import-orchestration-plan-2026-05-22.md` (RE-PLAN section authoritative; this protocol elevates + structures the plan)

---

## 0. TL;DR

This protocol operationalizes the **vast-library substrate pivot** (Patterns 4-5-6 retirements per `legacy-categorical-cleanup-audit-2026-05-22.md`) as a coordinated hive-mind workstream spanning ~1-3 weeks.

The work is structured in two layers:

- **Vision layer:** substrate-as-cohesion knowledge-first — the substrate is a vast queryable weapon-knowledge library (~15,000-30,000 entries) with rich textual + structured + cultural-lineage + visual data; the engine queries against the library via substrate-vectors; emergent clusters and discovered axes replace pre-imposed categorical taxonomies (Patterns 4-5-6).

- **Operational layer:** phased crawl (Phase 1) + feature extraction (Phase 1.5) + statistical axis discovery + BDI ω-seeding (Phase 2) + multimodal clustering (Phase 3) + cluster semantic labeling (Phase 4) + validation + substrate-density precomputation (Phase 5) + Meshy gap-fill (Phase D, post-density-map).

**Phase architecture (eight phases):**

| Phase | Owner(s) | Scope | Duration |
|---|---|---|---|
| **P0** | knight-rider | Schema lock + cluster-table amendment + DB greenfield init | ~5 min |
| **P1** | legolas (primarily) | Knowledge-source crawls + 3D-model imports (Tracks A + B parallel) | 4-8 hours wall; up to several days for Meshy bulk |
| **P1.5** | rocket / legolas | Feature extraction per weapon — wide feature vectors | 1-2 hours |
| **P2** | rocket (with legolas Mode A on methodology) | Statistical axis discovery (PCA / factor analysis; Pattern 6 operationalization) + BDI ω-table seeding | 1-3 days |
| **P3** | legolas Mode A or rocket | Multi-dimensional clustering analysis | 1-2 days |
| **P4** | gandalf + Matt | Cluster semantic labeling design call | 2-3 hours focused (could span days) |
| **P5** | galadriel + rocket parallel | Visual coherence validation + substrate-density precomputation | 4-8 hours parallel |
| **PD** | knight-rider orchestrating; legolas + galadriel executing | Meshy generation gap-fill for sparse-region substrate-vectors | Operational ongoing |

**Critique-pair structure per phase** specified (jack-ryan technical critique; gandalf design critique).

**Math gates per phase** specified (Discipline #1 application points).

**Risk register** with 15 risks identified + mitigation per risk.

**Engineering-disciplines compliance matrix** covers all 19 disciplines.

**Decision gates** (G1-G4) hold dispatches pending Matt input.

**Acceptance criterion (whole protocol):** ~15,000-30,000 weapon knowledge entries indexed; ~4,000-6,500 3D model attachments; 50-150 semantically-labeled emergent clusters; BDI ω-scores populated; substrate-density precomputed; Phase D operational; Profile A asset pipeline ready for spirit-form-library generation.

---

## 1. Provenance, scope, dependencies

### 1.1 How this protocol came to be

The 2026-05-22 evening session executed a substantial architectural cleanup pass (six vestigial-pattern retirements per `legacy-categorical-cleanup-audit-2026-05-22.md`). Three of those retirements (Patterns 4-5-6) require operational substrate work to land:

- **Pattern 4 retirement** (pre-imposed aesthetic-tuple dimensions) → emergent aesthetic clusters from data
- **Pattern 5 retirement** (15-entry gear catalogue) → emergent gear-form clusters from data
- **Pattern 6 retirement** (the axes themselves) → discovered axes from statistical analysis on data

All three require *the data to exist*. Without a vast-enough weapon corpus, axis discovery is statistically underpowered; without statistical axis discovery, the canonical-axis taxonomies stay pre-imposed; without emergent clustering, the 15-entry catalogue cannot be replaced.

This protocol structures the substrate-acquisition + analysis work as a coordinated hive workstream. It is the operationalization of the vast-library substrate pivot committed canonically in `gear-heavy-promotion-2026-05-22.md` and architecturally in `engine-as-general-serial-content-product-2026-05-22.md`.

### 1.2 Two-layer architecture (vision + operational)

Mirror the QD-rebuild protocol's two-layer structure:

**Vision layer — substrate-as-cohesion knowledge-first:**

- The substrate is a vast queryable weapon-knowledge library
- Primary substrate: rich text + structured properties + cultural-lineage + reference images per weapon knowledge entry
- Secondary substrate: 3D model attachments (many-to-many with knowledge entries)
- Substrate-vector queries: the engine asks the library "give me weapons matching (element substrate ω-affinity, range_profile, [discovered-axis vector])"
- Cluster identity: emergent from multimodal clustering of the imported corpus
- Axes: discovered from PCA / factor analysis on extracted feature vectors (Pattern 6)
- Per Variant C scope: this is general engine capability, not Reincarnated-specific

**Operational layer — phased crawl + axis discovery + clustering + cluster labeling:**

- Phase 0 schema lock
- Phase 1 Tracks A (knowledge) + B (3D models) parallel
- Phase 1.5 feature extraction
- Phase 2 statistical axis discovery + BDI ω-seeding (Pattern 6 operationalization)
- Phase 3 multimodal clustering
- Phase 4 cluster semantic labeling (gandalf + Matt design call)
- Phase 5 validation + substrate-density precomputation
- Phase D Meshy generation gap-fill

The vision-layer is the architectural commitment; the operational-layer is how the architectural commitment becomes engine reality.

### 1.3 Scope and exclusions

**In scope:**
- Knowledge-source crawls (Wikipedia + Wikidata + game wikis + SRD + museums + anime/manga wikis)
- 3D model imports (Sketchfab + Kenney + OGA + Smithsonian + Meshy where applicable)
- Reference-image capture for Meshy validation loop
- Schema + DB infrastructure (SQLite at `/Users/admin/Games/reincarnated-loadout/data/telemetry.db`)
- Feature extraction methodology
- Statistical axis discovery (PCA / factor analysis / NMF candidates)
- BDI ω/τ table seeding
- Multimodal clustering
- Cluster semantic labeling
- Visual coherence validation
- Substrate-density precomputation
- Phase D Meshy gap-fill pipeline operationalization

**Out of scope (deferred to v1.1+ or other workstreams):**
- Engine code refactor to consume library queries (lands in P1 W1.15 of the parent QD-rebuild protocol; this protocol provides the substrate, that protocol consumes it)
- Cohesion-judge prompt authoring against discovered axes + clusters (lands in P5 of parent protocol)
- Profile B/C/D actual integration (per Variant C deferrals)
- Sci-fi + post-singularity catalogue expansion (v1.1+)
- Full generative gear-substrate (G-PROMOTE-v1.1)
- Multi-tier hierarchy (v1.1+ per gear-heavy-promotion § 3.4)

### 1.4 Dependencies entering P0

| Dependency | Status |
|---|---|
| Variant C canonical lock | DONE — `engine-as-general-serial-content-product-2026-05-22.md` (`f72690f`) |
| Gear-HEAVY canonical lock | DONE — `gear-heavy-promotion-2026-05-22.md` |
| Vestigial-pattern audit | DONE — `legacy-categorical-cleanup-audit-2026-05-22.md` |
| Stat-derivation canonical | DONE — `stat-derivation-from-bc-convergence-2026-05-22.md` |
| Legolas weapon library import findings | DONE — `weapon-library-import-2026-05-22/` (7 files; ~2,900 lines) |
| Legolas Unity catalogue + Meshy armor findings | DONE — `unity-catalogue-armor-meshy-2026-05-22/` (5 files) |
| Legolas Meshy pipeline findings | DONE — `meshy-pipeline-2026-05-22/findings.md` |
| Galadriel canary v1 + v2 Meshy tests | DONE — empirical pipeline rule canonized (`06e91e9`) |
| Greenfield SQLite DB | DONE — empty as of 2026-05-22 evening (`/Users/admin/Games/reincarnated-loadout/data/telemetry.db`) |
| `schema.sql` ready-to-run | DONE — 562 lines; needs cluster-table amendment per P0 |
| Discipline #19 ratification | DONE — engine commit `0d1ad63`; applies throughout |

**Pending operational items (resolve before P1 fires):**
- C1 `MESHY_API_KEY` persisted to `~/.zshrc` (per skill_handoff § 5)
- C2 Meshy API probe (per skill_handoff § 5)
- P0.5 Smithsonian `api.data.gov` API key registration (gates Phase 1 Source D6)
- Per-source robots.txt verification (P0.8 + jack-ryan Discipline #20 robots.txt authoring)
- Per-source TOS check (P0.9)

---

## 2. The two-layer architecture (vision + operational)

### 2.1 Vision layer

Captured in `gear-heavy-promotion-2026-05-22.md` § 2 (vast-library substrate architecture). Summary:

- Substrate is knowledge-first (text + properties + reference images PRIMARY; 3D models SECONDARY visual references)
- Substrate scale: 15,000-30,000 knowledge entries; 4,000-6,500 model attachments
- Substrate is queryable via substrate-vectors (element substrate ω-affinity, range, [discovered-axis vector])
- Cluster identity emerges from data; designer labels post-hoc
- Axes themselves discovered from PCA / factor analysis on extracted feature vectors (Pattern 6)

The vision-layer is the architectural commitment under substrate-as-cohesion + Variant C.

### 2.2 Operational layer

This protocol's eight-phase structure (§ 6 per-phase detail) is the operational layer. Each phase has owner(s), scope, math gates (where applicable), critique-pair structure, acceptance criteria, decision gates within the phase, and Discipline #19 compliance pattern.

### 2.3 Parent protocol cross-reference

This protocol is the substrate-enrichment workstream of `canonical/story/hive-mind-protocol-qd-engine-rebuild-2026-05-21.md` v1.3 § 6.2 (Phase P1 Substrate Enrichment). The parent protocol's P1 workstreams (W1.1-W1.15) consume the substrate this protocol produces:

- W1.1-W1.6 schema + telemetry + skill substrate enrichment → unaffected by this protocol; runs in parallel
- W1.7-W1.12 Mixamo/Meshy/VFX integration → uses outputs from this protocol's Phase 1 + Phase D
- W1.13 LC-011 floor-lock work → unaffected; runs in parallel
- **W1.15** signature_gear derivation → **DIRECTLY CONSUMES this protocol's outputs** (substrate-vector queries against the library)

Sequencing: this protocol's Phase 0-Phase 4 must complete before W1.15 implementation lands. Phase 5 + Phase D operate in parallel with W1.15 onward.

---

## 3. Pre-flight checks (P0 prerequisites)

Knight-rider runs these FIRST thing tomorrow before authoring any per-phase dispatches. Per the source operational plan § 1 + the orchestration plan's RE-PLAN P0.8 + P0.9 additions:

| # | Check | How | Resolution path if failing |
|---|---|---|---|
| **P0.1** | `MESHY_API_KEY` env var persists across shell sessions | `echo "${MESHY_API_KEY:0:4}"` in a fresh terminal | Matt adds `export MESHY_API_KEY="..."` to `~/.zshrc`; re-source |
| **P0.2** | Meshy API probe — verify key auth + library endpoint availability | Probe script per skill_handoff § 6.1 | If library endpoints all 404: pivot Phase 1 D2 to skip Meshy bulk; if some 200s: API-driven enumeration |
| **P0.3** | DB greenfield state confirmed | `sqlite3 /Users/admin/Games/reincarnated-loadout/data/telemetry.db ".tables"` returns empty | If non-empty: matt-briefing — schema migration plan needed |
| **P0.4** | `schema.sql` ready at canonical path | Already verified 562 lines 2026-05-22 evening | None — DONE |
| **P0.5** | Smithsonian `api.data.gov` API key registered | Matt confirms; key in `SMITHSONIAN_API_KEY` env var | Matt registers at https://api.data.gov/signup/ (free; takes ~5 min); blocks Phase 1 Source D6 only |
| **P0.6** | CC-BY-SA legal review status | Matt confirms commercial compatibility status | If unclear: matt-briefing — `game_approved` flag stays `0` for CC-BY-SA pending; doesn't block Phase 1 |
| **P0.7** | Meshy partner-tier outreach status | Matt confirms whether outreach email has been sent | Non-blocking; if response comes back during Phase 1, pivot D2 scope |
| **P0.8** | Per-source robots.txt verification | For EACH crawl target: fetch `robots.txt`; verify `User-agent: ClaudeBot` and `User-agent: anthropic-ai` NOT Disallow-listed | If blocked, source routes to non-Claude implementation OR skips |
| **P0.9** | Per-source TOS check | For each source: fetch ToS; verify automated-research-access compatible | Wikipedia/Wikidata explicit OK; museum APIs explicit OK; TVTropes/IMFDB worth checking |

**P0.1 + P0.2 are blocking for Phase 1 D2 (Meshy bulk import).** Other P0 items have specific blocking scopes; resolve in parallel.

**P0.8 + P0.9 are blocking for Phase 1 across all crawl-based sources** — Discipline #20 (jack-ryan's parallel authoring per session) is the canonical framework for this.

---

## 4. Decision gates

Knight-rider holds dispatches at these gates pending Matt input.

| Gate | When | What blocks | Resolution |
|---|---|---|---|
| **G1** — Meshy API probe outcome | Before D2 fires | Phase 1 D2 scope | P0.2 probe + Matt confirmation of which D2 variant fires |
| **G2** — CC-BY-SA legal review | Before any commercial-publish use of imported assets | `game_approved` flag policy | Matt confirms CC-BY-SA commercial-compatible OR keeps `game_approved=0` for those assets |
| **G3** — Cluster semantic labeling kickoff | After Phase 3 completes | Phase 4 design call timing | Matt schedules ~2-3 hours with gandalf for the labeling session |
| **G4** — Phase D Meshy generation gap-fill priority | Mid-Phase-5 once density map populated | Priority ranking for Meshy generation targets | Matt + gandalf review density map; identify priority targets; knight-rider authors Phase D dispatches |

---

## 5. Phase architecture overview

Eight phases total (P0 through P5 in sequence; PD operates post-density-map per gate G4):

```
P0 Schema Lock (~5 min)
   ↓
P1 Library Imports — Track A Knowledge + Track B 3D Models PARALLEL (4-8 hrs wall)
   ↓ (≥80% imports complete)
P1.5 Feature Extraction (1-2 hrs)
   ↓
P2 Axis Discovery + BDI ω-Seeding (1-3 days)
   ↓
P3 Clustering Analysis (1-2 days)
   ↓
P4 Cluster Semantic Labeling — gandalf + Matt design call (2-3 hrs focused)
   ↓
P5 Validation + Substrate-Density Precomputation PARALLEL (4-8 hrs)
   ↓
PD Meshy Generation Gap-Fill (operational ongoing per density-map sparse regions)
```

**Total wall time: ~1-2 weeks** with ~3-4 hours active Matt time (pre-flight resolution + cluster labeling + decision gates).

---

## 6. Per-phase detail

### 6.1 Phase P0 — Schema Lock + Cluster Table Amendment

**Owner:** knight-rider (direct; operational)
**Dependencies:** P0.3, P0.4
**Duration:** ~5 min
**Discipline:** N/A (foreground operational)

#### 6.1.1 Scope

Amend `schema.sql` with cluster + knowledge-entry tables; run DDL; verify; commit.

#### 6.1.2 Workstreams

**W0.1 — Schema amendment.** Amend `schema.sql` to add:
- `weapon_knowledge_entries` (PRIMARY substrate table)
- `knowledge_model_attachments` (many-to-many join)
- `knowledge_entry_canonical_merge` (canonical entry merging)
- `knowledge_entry_reference_images` (reference-image attachments)
- `clusters` + `cluster_membership` (Pattern 5 cluster-table amendment per source plan)
- ALTER `weapons` to add `cluster_id` FK

**W0.2 — DDL execution.** `sqlite3 /Users/admin/Games/reincarnated-loadout/data/telemetry.db < schema.sql`

**W0.3 — Verification.** Run `.schema` query; confirm all tables present; confirm indexes present.

**W0.4 — Commit.** `schema.sql` amendments committed to repo; CHANGELOG entry filed.

#### 6.1.3 Critique-pair structure

- **Pattern B (Spec + Review):** legolas reviews schema amendments before W0.2 execution (structural review on cluster-table additions); rocket reviews ω-affinity column placements
- **No design critique needed** — operational schema work

#### 6.1.4 Success / failure criteria

**Success:**
- All tables present per `.schema` query
- Compound indexes present per legolas's `schema.sql` specification
- `substrate_density` precomputed table empty but ready
- `clusters` + `cluster_membership` tables empty but ready
- Commit hash recorded in CHANGELOG

**Failure modes:**
- Schema syntax errors → re-author + re-test before W0.2
- DDL execution fails → debug + retry
- Compound index missing → re-author DDL

#### 6.1.5 Math gates

None — operational only.

#### 6.1.6 Discipline #19 compliance

Foreground operational; single `sqlite3` invocation. No babysit needed.

---

### 6.2 Phase P1 — Library Imports (Tracks A + B PARALLEL)

**Owner:** legolas (primarily; possibly split across legolas + rocket for parallelism)
**Dependencies:** Phase 0 complete; P0.1 + P0.2 + P0.5 + P0.8 + P0.9 resolved per source needs
**Duration:** Variable per source (hours to days)
**Discipline:** #19 — ALL long-running imports are background processes; status via DB COUNT queries; JSON summary artifacts as final-act

#### 6.2.1 Scope

**Track A — Knowledge crawls (PRIMARY):** Wikipedia + Wikidata + game wikis + SRD + museums + TVTropes + IMFDB + anime/manga wikis. Target: ~15,000-30,000 knowledge entries with rich text + structured properties + reference images.

**Track B — 3D model imports (SECONDARY):** Sketchfab + Kenney + OGA + Smithsonian + Meshy (per G1 outcome). Target: ~4,000-6,500 model entries attached to knowledge entries via name-match where possible.

#### 6.2.2 Workstreams

**Track A — Knowledge crawls:**

| WS | Source | Estimated entries | Duration |
|---|---|---|---|
| **W1.A.1** | Wikipedia weapons categories | ~5,000-15,000 | 4-8 hours |
| **W1.A.2** | Wikidata weapon Q-items | ~2,000-5,000 | 2-4 hours |
| **W1.A.3** | Game wikis (PoE/D3/D4/Last Epoch/Dark Souls/Monster Hunter/WoW/Bleach/SAO Fandom-hosted) | ~2,000-10,000 | 4-8 hours |
| **W1.A.4** | D&D / Pathfinder SRD | ~100-200 | 30 min |
| **W1.A.5** | Royal Armouries / Met Museum / Smithsonian | ~5,000-10,000 | 4-8 hours (gated on P0.5) |
| **W1.A.6** | TVTropes weapon tropes | Genre taxonomy enrichment | 2-4 hours |
| **W1.A.7** | IMFDB | Movies/TV weapon canon | 1-2 hours |
| **W1.A.8** | Anime/manga weapon wikis | Isekai substrate enrichment | 2-4 hours |

Each WS runs as background process; checkpoints to DB; resumable on failure; JSON summary artifact on completion.

**Track B — 3D model imports:**

| WS | Source | Estimated entries | Duration |
|---|---|---|---|
| **W1.B.1 (D2)** | Meshy library bulk import | Variable per G1 outcome | Hours to deferred entirely |
| **W1.B.2 (D3)** | Sketchfab Data API v3 crawl | ~1,177 CC0+CC-BY weapons | 1-4 hours |
| **W1.B.3 (D4)** | Kenney static downloads | ~200-400 CC0 weapons | 30-60 min |
| **W1.B.4 (D5)** | Open Game Art crawl | ~389 weapons (mixed licenses) | 1-2 hours |
| **W1.B.5 (D6)** | Smithsonian Open Access | ~100-400 weapons (gated on P0.5) | 1-2 hours after key reg |

Same Discipline #19 pattern: background processes; DB checkpoints; resumable; JSON summary artifacts.

**Reference image acceptance criterion (per orchestration plan MEMO FOR LEGOLAS):** ≥70% of knowledge entries with at least one reference image; ≥30% with canonical (primary) image marked; license metadata captured per image.

#### 6.2.3 Critique-pair structure

- **Pattern A (Design + Implementation):**
  - gandalf reviews knowledge-source prioritization (which sources first; what cultural-lineage coverage does the prioritization produce)
  - legolas implements crawls
- **Pattern B (Spec + Review):**
  - jack-ryan reviews per-source TOS + robots.txt compliance (Discipline #20)
  - rocket reviews per-source metadata-normalization conformance to canonical schema

#### 6.2.4 Success / failure criteria

**Success:**
- ≥15,000 knowledge entries imported across Track A (target lower bound)
- ≥4,000 model attachments imported across Track B (target lower bound)
- ≥70% knowledge entries with reference images
- All sources comply with TOS + robots.txt verification
- License metadata captured per record (CC0 / CC-BY / CC-BY-SA / PD / etc.)
- Per-source JSON summary artifacts at known paths

**Failure modes:**
- Source robots.txt blocks Claude-agent → route to non-Claude implementation OR skip
- API rate-limiting → exponential backoff; resume from DB checkpoint
- License unclear → mark `license_class = "unknown"`; flag for post-hoc review
- Reference-image coverage <70% → Phase D Meshy gap-fill priority increases

#### 6.2.5 Math gates

None directly — empirical import work. Math gates land at P2.

#### 6.2.6 Discipline #19 compliance

ALL workstreams as `nohup` background processes. Status via:
```bash
sqlite3 /Users/admin/Games/reincarnated-loadout/data/telemetry.db \
  "SELECT source_library, COUNT(*) FROM weapon_knowledge_entries GROUP BY source_library;"
```
No Agent invocations for monitoring. JSON summary artifacts at:
- `agentic_orchestration/logs/wikipedia_crawl_summary.json`
- `agentic_orchestration/logs/wikidata_crawl_summary.json`
- `agentic_orchestration/logs/game_wikis_crawl_summary.json`
- (etc., per workstream)

---

### 6.3 Phase P1.5 — Feature Extraction Per Weapon

**Owner:** rocket (primary) or legolas Mode A
**Dependencies:** Phase 1 imports ≥80% complete
**Duration:** 1-2 hours
**Discipline:** #1 (math-before-code on feature-extraction methodology) + #11 (empirical inspection on sample before full run)

#### 6.3.1 Scope

For each imported weapon (knowledge entry + attached models), extract a wide feature vector with NO pre-imposed axes — extract everything measurable. Pattern 6 axis discovery operates on these extracted features.

#### 6.3.2 Workstreams

**W1.5.1 — Methodology spec.** Per Discipline #1: spec the feature-extraction methodology before coding. Feature classes:

| Feature class | Examples |
|---|---|
| **Text features** | description text embedding (sentence-transformer); tag co-occurrence vector; subcategory one-hot |
| **Structured features** | length, weight, period, country, two-handed-bool, range-type, all structured infobox fields as numeric/categorical |
| **Cultural-lineage features** | culture tags (Smithsonian + Wikidata structured); period tags; genre appearances |
| **Geometric features (model side)** | poly count, dimensions (x/y/z), bounding-box aspect ratio, curvature estimates, ornamentation density, symmetry score |
| **Visual features (model side)** | preview image embedding (CLIP-style vision-language model); color palette histogram |
| **Source metadata** | library origin, author, license_class |
| **Computed mechanical estimates** | range estimate from geometry; two-handed-likely vs one-handed; weight-class estimate |

**W1.5.2 — Sample pass.** Per Discipline #11: extract features on ~50-100 sample weapons; inspect for anomalies; calibrate methodology.

**W1.5.3 — Full pass.** Run feature extraction across full imported corpus. Output: wide feature matrix per weapon row.

**W1.5.4 — Storage.** Feature matrix stored as JSON blob on `weapons` rows OR in a separate `weapon_features` table (decide per schema review).

#### 6.3.3 Critique-pair structure

- **Pattern B:** rocket implements; legolas Mode A reviews methodology spec (statistical rigor); gandalf reviews feature-class coverage (does this capture the cultural-lineage substrate Reincarnated needs?)

#### 6.3.4 Success / failure criteria

**Success:**
- Feature vectors populated for ≥99% of imported weapons
- Sample inspection on 20 random weapons: features feel right (katana has curved-blade signature; greatsword has straight-blade-two-handed signature)
- Feature matrix size + storage layout documented

**Failure modes:**
- Feature extraction blows up on edge cases → handle gracefully; tag failed rows for re-pass
- Storage layout too large for DB → migrate to separate `weapon_features` table OR external file storage

#### 6.3.5 Math gates

Discipline #1 application: feature-extraction methodology specified mathematically before implementation.

#### 6.3.6 Discipline #19 compliance

Background process if >1 hour; foreground if smaller. Status via row update count queries.

---

### 6.4 Phase P2 — Axis Discovery + BDI ω-Seeding (Pattern 6 operationalization)

**Owner:** rocket (with legolas Mode A on statistical methodology)
**Dependencies:** Phase 1.5 complete
**Duration:** 1-3 days
**Discipline:** #1 (math-before-code on statistical methodology) + #11 (empirical inspection on derived axes) + Pattern 6 honored (no axis pre-imposition)

#### 6.4.1 Scope (Pattern 6 operationalization)

**This is where Pattern 6 lands operationally.** Per the audit doc § 3.6 and `gear-heavy-promotion-2026-05-22.md` § 2: the aesthetic axes and the geometrical/mathematical mechanical variables must be DERIVED from a statistically significant sample, NOT pre-imposed.

Two sub-phases:

#### 6.4.2 Workstreams

**W2.1 — Statistical axis discovery (Pattern 6 implementation).**

Per Discipline #1: spec the statistical methodology before running. Candidates:
- **PCA** — linear; orthogonal axes explaining variance
- **Factor Analysis** — latent factors; more interpretable for semantic axes
- **UMAP / t-SNE** — non-linear; visualization + cluster prep
- **Sparse PCA / NMF** — sparse loadings; interpretable axis-definitions
- **Mixed-effects: PCA on geometric+mechanical features + Factor Analysis on semantic+visual features** — separates axis-discovery for the two substrate halves

**Sample-size guidance** (per source plan):
- PCA: minimum 5-10× sample per feature; for ~50 features → 250-500 weapons minimum
- Factor analysis: minimum 200-300 for stable factor loadings
- **Recommended sample for stable axis discovery: 1,000-2,000 weapons** (achievable from Track A alone; doesn't require D2 Meshy bulk success)

**Output of W2.1:**
- Discovered aesthetic axes (4-8 principal components from visual+semantic feature analysis)
- Discovered mechanical axes (4-8 principal components from geometric+source-metadata feature analysis)
- Per-axis interpretation (gandalf + Matt review axis loadings; assign semantic labels)
- **Replaces** the pre-imposed `(tech_level / tone / cultural_lineage)` + `(range / geometry / timing / charge / accuracy / rhythm)` taxonomies with data-derived axis-sets

**W2.2 — BDI ω-table seeding.**

Operates against the **derived axes** from W2.1, not pre-imposed dimensions. Each weapon's ω-score per element is computed against the derived-axis basis vectors.

Per-weapon: identify top-3 element affinities + record best ω-magnitude. Serialized into `dominant_element_affinities` JSON column.

**Why this matters now (not later):** clustering (P3) uses the discovered axes + ω-scores as feature inputs. Without W2.1, clustering operates on raw features (less interpretable) OR on pre-imposed axes (vestigial pattern survives).

#### 6.4.3 Critique-pair structure

- **Pattern A:** rocket implements; legolas Mode A reviews statistical methodology rigor
- **Pattern B:** gandalf reviews discovered-axis interpretations (do the axes carry semantic meaning the design can use?); jack-ryan reviews math methodology compliance (Discipline #1 #11)

#### 6.4.4 Success / failure criteria

**Success:**
- ≥1,000 weapons in sample (achievable from Track A)
- Discovered axes have ≥80% cumulative variance explained at top-8 components
- Axis interpretations gandalf + Matt-reviewed for soundness
- ω-scores populated for ≥99% of weapon rows
- Sample inspection on ~20 random weapons: ω-scores feel right (canonical pairings like holy+censer score high; novel pairings like holy+blunderbuss score low-but-positive)

**Failure modes:**
- Sample too small for stable axis discovery → defer until Track A nears full completion
- Axes don't carry interpretable semantic meaning → try alternative methodology (Factor Analysis vs PCA vs NMF)
- ω-score sample inspection surfaces calibration issues → recalibrate BDI table per element

#### 6.4.5 Math gates

**Discipline #1:** statistical methodology spec'd before run.
**Discipline #11:** empirical inspection on derived axes for soundness.
**Discipline #17:** axis-interpretation calibration sweep.

#### 6.4.6 Discipline #19 compliance

Background process (Mode A analytical + ML can run multi-hour). Status via algorithm version in `clusters` table + JSON summary as final-act.

---

### 6.5 Phase P3 — Clustering Analysis

**Owner:** legolas (Mode A analytical) OR rocket (decide at dispatch time per ML library access)
**Dependencies:** Phase 2 complete
**Duration:** 1-2 days
**Discipline:** #1 (math-before-code on clustering algorithm choice) + #11 (empirical inspection on cluster outputs before lock)

#### 6.5.1 Scope

Multi-dimensional clustering on imported weapons. Feature space:
- Discovered axes from W2.1
- BDI ω-scores per element (7 dimensions, per W2.2)
- Raw geometric features (poly count, dimensions, ornamentation density)
- Raw semantic features (text + image embeddings)

#### 6.5.2 Workstreams

**W3.1 — Algorithm evaluation.** Run multiple clustering algorithms; benchmark:
- Hierarchical clustering (cluster tree; multi-granularity)
- HDBSCAN (density-based; produces noise-points; good for catalogues with outliers)
- k-means with multiple k values (k=15, 30, 50, 100, 150)
- Hybrid (semantic + geometric features fused)

**W3.2 — Cluster output population.** Per algorithm pass:
- Cluster assignments per weapon → `cluster_id` on `weapons` table (single dominant cluster)
- Multi-cluster membership → `cluster_membership` table with confidence scores
- Cluster registry → `clusters` table with dominant_axes_description

#### 6.5.3 Critique-pair structure

- **Pattern A:** legolas/rocket implements; gandalf reviews cluster gestalt-recognition (do the emergent clusters carry recognizable thematic identity?)
- **Pattern B:** jack-ryan reviews algorithm methodology (Discipline #1 #11); rocket reviews multi-algorithm comparison

#### 6.5.4 Success / failure criteria

**Success:**
- ≥3 algorithm passes complete with comparable cluster structures
- Inter-rater reliability check: hierarchical + HDBSCAN agree on dominant cluster centroids
- Cluster count in target range (50-150 clusters at recommended granularity)
- Per-cluster JSON summary with sample weapons + dominant-axes

**Failure modes:**
- Algorithms produce wildly different clusterings → indicates noisy substrate; iterate on W2.1 axis discovery
- Cluster count outside range → re-tune k or HDBSCAN params
- Clusters lack gestalt coherence (random weapons grouped together) → revisit feature extraction (P1.5)

#### 6.5.5 Math gates

**Discipline #1:** algorithm choice specified mathematically.
**Discipline #11:** empirical inspection on cluster outputs.

#### 6.5.6 Discipline #19 compliance

Background (Mode A + ML clustering multi-hour). Status via algorithm version in `clusters` table.

---

### 6.6 Phase P4 — Cluster Semantic Labeling

**Owner:** gandalf + Matt design call
**Dependencies:** Phase 3 complete
**Duration:** 2-3 hours focused (could span multiple sittings)
**Discipline:** Pattern recognition design work; not automatable

#### 6.6.1 Scope

Review top-N clusters (by size + distinctness) from Phase 3. For each: inspect sample weapons (5-10 representatives); identify cluster gestalt; assign semantic label; note hypothesis match against 15-entry catalogue predictions.

#### 6.6.2 Workstreams

**W4.1 — Cluster review.** gandalf + Matt sit for cluster review session:
- Per cluster: inspect 5-10 sample weapons
- Identify the cluster's gestalt — what makes weapons in this cluster feel like a coherent family?
- Assign a semantic label ("Eastern-curved-blade-family", "Industrial-firearm-family", "Ornate-ceremonial-staff-family")
- Optionally assign secondary tags (aesthetic-tuple vocabulary: tech_level / tone / cultural_lineage as descriptive language per Pattern 4 surviving vocabulary)
- Note whether this cluster matches a 15-entry catalogue prediction (per `gear-heavy-promotion-2026-05-22.md` § 6.4 prediction table)

**W4.2 — Cluster registry population.** Updates to `clusters.label` + `clusters.dominant_axes_description` per reviewed cluster.

**W4.3 — Canonical emergent-cluster catalogue authoring.** Authors `canonical/story/emergent-cluster-catalogue-2026-05-XX.md` capturing the labeled clusters as canonical Reincarnated gear-substrate vocabulary.

#### 6.6.3 Critique-pair structure

- **Pattern C (Critique-pair memo):** gandalf + Matt design call; jack-ryan reviews artifact post-session

#### 6.6.4 Success / failure criteria

**Success:**
- ≥80% of weapons (by row count) are members of a labeled cluster
- Cluster labels are player-meaningful (designer-test: would a player understand "katana-family" vs "obscure-cluster-17")
- Cross-references back to original 15-entry catalogue (which entries emerged as clusters? which didn't?)
- Emergent-cluster catalogue doc authored + committed

**Failure modes:**
- Designer cannot identify gestalt for many clusters → indicates clustering issue; revisit P3
- Clusters split fine-grained that don't carry meaningful designer-identifiable difference → revisit clustering granularity

#### 6.6.5 Math gates

None — design call.

#### 6.6.6 Discipline #19 compliance

Foreground interactive (design call; not automatable).

---

### 6.7 Phase P5 — Validation + Substrate-Density Precomputation (PARALLEL)

**Owner:** galadriel (visual validation) + rocket (density precompute)
**Dependencies:** Phase 4 complete (cluster labels assigned)
**Duration:** 4-8 hours parallel
**Discipline:** #1 (math-before-code on density-aggregation) + #11 (empirical inspection on visual coherence)

#### 6.7.1 Scope

Two parallel workstreams:

**Sub-phase A — Galadriel visual coherence validation.** Visual-similarity scoring across cluster members. Outputs: per-cluster visual cohesion score; outlier flagging; cross-cluster confusion analysis.

**Sub-phase B — Rocket substrate-density precomputation.** Populate `substrate_density` precomputed table per legolas's `selection-patterns.md` schema design.

#### 6.7.2 Workstreams

**W5.A.1 — Visual coherence validation (galadriel).**

Computer-vision similarity scoring on preview images of weapons within each labeled cluster. Outputs:
- Per-cluster visual cohesion score (do members look like they belong together?)
- Outlier flagging (weapons assigned to cluster but visually distinct — candidate misclassifications)
- Cross-cluster confusion analysis (which cluster pairs have weapons that could plausibly belong to either?)

**W5.B.1 — Density precomputation (rocket).**

Populate `substrate_density` table. For each substrate-vector tuple (element × range × cluster_id):
- Count of weapons matching the tuple
- Best-ω-score for the tuple
- Aesthetic-coverage map (which descriptive tags are represented)
- Density classification: dense / medium / sparse / empty (with thresholds calibrated per Discipline #17)

Output: `substrate_density` table populated; engine queries return O(1) density check + routing decision.

#### 6.7.3 Critique-pair structure

- **Pattern A:** galadriel implements W5.A.1; gandalf reviews per-cluster visual cohesion outputs
- **Pattern A:** rocket implements W5.B.1; legolas Mode A reviews density-aggregation formula
- **Pattern B:** jack-ryan reviews both for Discipline #17 calibration compliance

#### 6.7.4 Success / failure criteria

**Sub-phase A success:**
- ≥75% of clusters have visual cohesion score above threshold (per Discipline #17 calibration)
- Outlier weapons flagged with confidence scores; ≤5% require reassignment

**Sub-phase B success:**
- All non-empty substrate-vector tuples have density entries
- Sample inspection on 20 random tuples: density classifications feel right
- Engine queries return O(1) routing decision

**Failure modes:**
- Visual cohesion <75% → cluster needs re-review or splitting (back to P3 or P4)
- Outlier rate >5% → indicates misclassifications; back to P3 algorithm tuning

#### 6.7.5 Math gates

**Discipline #1:** density-aggregation formula specified mathematically.
**Discipline #11:** empirical inspection on density classifications.
**Discipline #17:** visual-cohesion threshold + density-bucket threshold calibration.

#### 6.7.6 Discipline #19 compliance

Background each. Status via summary file existence:
- `agentic_orchestration/galadriel/logs/cluster_validation_summary.json`
- `~/Games/reincarnated-engine/logs/substrate_density_summary.json`

---

### 6.8 Phase PD — Meshy Generation Gap-Fill (operational ongoing)

**Owner:** knight-rider orchestrating; legolas + galadriel executing
**Dependencies:** Phase 5 complete (density map populated); G4 gate resolution
**Duration:** Operational ongoing
**Discipline:** #19 (background generation; checkpoint per asset)

#### 6.8.1 Scope

For sparse regions of the density map (substrate-vector tuples lacking adequate library coverage), run the Phase D Meshy generation gap-fill pipeline per `gear-heavy-promotion-2026-05-22.md` § 7 canonical pipeline.

#### 6.8.2 Workstreams

**WD.1 — Sparse-region prioritization.** gandalf + Matt review density map; identify priority targets (typically: clusters with low entry counts in important substrate-vector regions).

**WD.2 — Per-target pipeline runs.** For each priority target:
- Identify representative knowledge entry from the sparse cluster
- ChatGPT image-gen synthetic weapon image
- Validate against reference images (galadriel visual-similarity scoring)
- Meshy image-to-3D
- Validate against reference images again
- Unity assembly

**WD.3 — Density-map update.** Newly-generated assets attached to knowledge entries; density-density-map regenerates.

#### 6.8.3 Critique-pair structure

- **Pattern A:** gandalf + Matt prioritize WD.1; galadriel validates WD.2; jack-ryan reviews Discipline #19 compliance per generation run
- **Pattern C:** galadriel's per-cluster generation summary surfaces calibration lessons (per § 8 canonical rule on rigid vs independent-life)

#### 6.8.4 Success / failure criteria

**Success:**
- Sparse-region count decreases per PD iteration
- Density classification improves (sparse → medium; medium → dense) for priority regions
- Generated assets pass reference-image validation loop
- Generated assets respect canonical pipeline rule (rigid-static vs independent-life per galadriel § 8)

**Failure modes:**
- ChatGPT fails to produce reference-compatible image → re-prompt with adjusted parameters
- Meshy produces structurally broken mesh → route to alternative source
- Generated asset breaks animation usability (per Canary v2 lesson) → re-author with companions/VFX in Unity-layer instead of source

#### 6.8.5 Math gates

None directly — pipeline-execution-driven.

#### 6.8.6 Discipline #19 compliance

Background generation runs. Checkpoint per asset. JSON summary artifact per PD iteration.

---

## 7. Critique-pair structure (consolidated)

Mirror the QD-rebuild protocol's three patterns:

### 7.1 Pattern A — Design + Implementation critique

One specialist implements; another (or gandalf for design dimension) critiques. Used in: P1.5 (rocket implements, gandalf reviews coverage); P2 (rocket implements, legolas reviews methodology); P3 (legolas/rocket implements, gandalf reviews gestalt); P5 (each sub-phase).

### 7.2 Pattern B — Spec + Review critique

Specifier authors spec; reviewer reviews before implementation fires. Used in: P0 (legolas reviews schema before DDL fires); P1 (jack-ryan reviews TOS/robots.txt per source); P2 (jack-ryan reviews methodology Discipline #1 #11); P5 (jack-ryan reviews Discipline #17 calibration).

### 7.3 Pattern C — Critique-pair memo

Sustained design dialogue captured as memo. Used in: P4 (gandalf + Matt design call); PD (per-iteration galadriel summary).

### 7.4 Per-phase critique requirements

| Phase | Pattern A | Pattern B | Pattern C |
|---|---|---|---|
| P0 | N/A | legolas schema review | N/A |
| P1 | N/A | jack-ryan TOS + robots.txt review; rocket schema-conformance | N/A |
| P1.5 | rocket impl, gandalf coverage | legolas Mode A methodology | N/A |
| P2 | rocket impl, gandalf interpretations | jack-ryan Discipline #1 #11 | N/A |
| P3 | legolas/rocket impl, gandalf gestalt | jack-ryan algorithm methodology | N/A |
| P4 | N/A | N/A | gandalf + Matt design call |
| P5 | per sub-phase | jack-ryan Discipline #17 | N/A |
| PD | gandalf+Matt prioritize, galadriel validate | jack-ryan Discipline #19 | galadriel per-iteration summary |

---

## 8. Tag conventions

Per QD-rebuild protocol § 9 pattern, applied to this workstream:

### 8.1 Intermediate tags

`wlib-import/v<PHASE>.<WORKSTREAM>-<DESCRIPTOR>[-<ITERATION>]`

Examples:
- `wlib-import/v0.1-schema-amendment`
- `wlib-import/v1.A.1-wikipedia-crawl-checkpoint`
- `wlib-import/v2.1-axis-discovery-pca`
- `wlib-import/v3.1-clustering-hdbscan-pass-1`
- `wlib-import/v4.1-cluster-labels-draft`
- `wlib-import/v5.B.1-density-precompute`

### 8.2 Milestone tags (Matt-approved)

`wlib-v<PHASE>.0-<phase-name>-shipped`

Examples:
- `wlib-v0.0-schema-locked`
- `wlib-v1.0-imports-complete`
- `wlib-v2.0-axes-discovered`
- `wlib-v3.0-clustering-complete`
- `wlib-v4.0-labels-canonical`
- `wlib-v5.0-density-ready`

### 8.3 Final tag

`wlib-v6.0-substrate-ready` — substrate ready for parent QD-rebuild protocol's W1.15 consumption; Phase D operational ongoing.

### 8.4 Rollback tags

Each milestone tag preserves the DB state at that point. Rollback via:
1. Restore SQLite DB from milestone-tagged backup
2. Revert schema.sql to milestone version
3. Resume from milestone phase

---

## 9. Risk register

### 9.1 Risks identified

| ID | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| **W1** | Meshy API library endpoints don't exist (all 404) | MED | LOW-MED | Phase 1 D2 deferred; sources from D3-D6 only; Phase shrinks to ~1,700-2,400 weapons but ships |
| **W2** | Per-source robots.txt blocks Claude-agent crawling | MED | MED | Discipline #20 (jack-ryan parallel authoring); per-source non-Claude implementation path OR skip source |
| **W3** | CC-BY-SA license commercial-compatibility unclear | LOW-MED | LOW (game_approved gates) | `game_approved=0` for CC-BY-SA pending review; doesn't block import; revisit pre-cutover |
| **W4** | Reference-image coverage <70% threshold | LOW | MED | Phase D Meshy gap-fill priority increases; mitigation runs naturally |
| **W5** | Axis discovery (W2.1) produces uninterpretable axes | MED | HIGH | Try alternative methodology (PCA vs FA vs NMF vs sparse); gandalf+Matt review for interpretation soundness |
| **W6** | Clustering algorithms produce wildly different clusterings | LOW-MED | MED | Indicates noisy substrate; iterate on W2.1 axis discovery; expand sample if needed |
| **W7** | Cluster gestalt-recognition fails (designer cannot identify what makes cluster coherent) | LOW | MED | Revisit clustering granularity (k tuning); revisit feature extraction (P1.5 coverage gaps) |
| **W8** | Sample too small for stable axis discovery (<1,000 weapons after Phase 1) | LOW | HIGH | Defer P2 until Track A nears full completion; expand crawl scope if needed |
| **W9** | Smithsonian API key registration blocks (P0.5) | LOW | LOW | Source D6 deferred; Track A Sources A.1-A.4 + A.6-A.8 continue |
| **W10** | Meshy partner-tier outreach fails | LOW | LOW | Phase D Meshy generation uses generation API (not library); operational as long as API key works |
| **W11** | Schema migration needed mid-import (DB not greenfield) | LOW | MED | Pre-flight P0.3 catches; migration plan authored by legolas before P0 fires |
| **W12** | Discovered axes meaningfully contradict pre-imposed taxonomies (e.g., range/geometry/timing collapse to 3 axes) | LOW-MED | LOW-MED (this is Pattern 6 working as intended) | gandalf+Matt design call to ratify the discovered axes as canonical replacement |
| **W13** | Density map shows large sparse regions in priority substrate-vectors | MED | LOW (Phase D mitigates) | Phase D Meshy gap-fill addresses; mitigation runs naturally |
| **W14** | Visual cohesion validation flags many clusters as incoherent | LOW | MED | Re-cluster with adjusted parameters; gandalf reviews labels |
| **W15** | Discipline #19 compliance violation during background imports (specialist accidentally babysits via Agent) | LOW | LOW (caught in review) | jack-ryan reviews per-phase compliance |

### 9.2 Risk monitoring

- Per-phase risk review at phase boundary
- Per-workstream risk identification by specialist
- Cross-cutting risk register maintained by knight-rider
- Risk re-assessment at every Matt session-open

---

## 10. Math gates per phase

Per Discipline #1 + #11 + #17, math gates land where statistical or empirical calibration applies:

| Math gate | Implementation phase | Specialist | Key threshold |
|---|---|---|---|
| Feature-extraction methodology spec | P1.5 W1.5.1 | rocket | Discipline #1 mathematical spec before code |
| Sample inspection on feature extraction | P1.5 W1.5.2 | rocket + gandalf | Discipline #11 empirical inspection on ~50-100 weapons |
| Axis-discovery methodology spec | P2 W2.1 | rocket + legolas Mode A | Discipline #1 mathematical spec; PCA vs FA vs NMF justified |
| Axis-loadings interpretation review | P2 W2.1 | gandalf + Matt | Discipline #11 empirical interpretation soundness |
| Axis variance-explained threshold | P2 W2.1 | rocket | ≥80% cumulative variance at top-8 components |
| BDI ω-score sample inspection | P2 W2.2 | gandalf | Discipline #11 empirical on ~20 random weapons |
| Clustering algorithm choice | P3 W3.1 | rocket / legolas | Discipline #1 mathematical justification |
| Cluster output empirical inspection | P3 W3.2 | gandalf + rocket | Discipline #11 gestalt-recognition check |
| Inter-rater reliability check on clustering | P3 W3.2 | rocket | Hierarchical + HDBSCAN agreement |
| Visual cohesion threshold calibration | P5 W5.A.1 | galadriel | Discipline #17 calibration sweep |
| Density classification thresholds | P5 W5.B.1 | rocket | Discipline #17 calibration sweep on dense/medium/sparse buckets |
| Density-aggregation formula spec | P5 W5.B.1 | rocket | Discipline #1 mathematical spec |

All gates land in their respective phase; cumulative compliance reviewed by jack-ryan at phase boundary.

---

## 11. Engineering disciplines compliance matrix

| Discipline | Application throughout this protocol |
|---|---|
| **#1 Math-before-code** | Every algorithmic surface specified mathematically before implementation (feature extraction, axis discovery, clustering, density aggregation) |
| **#2 Smoke-test vs full-regen** | Per P1.5 W1.5.2 sample pass before full feature extraction; P3 algorithm benchmark on subset before full run |
| **#3 No parallel regens of same seed** | Per-phase; specialist tags state before regen; no parallel runs against same DB without explicit coordination |
| **#4 Right tool for validation question** | Per-phase tooling specified; statistical analysis in Python/R; visual validation via galadriel; structural review via legolas |
| **#5 Triage discipline** | Per-phase critique pair pattern (§ 7) |
| **#6 Tag intermediate states** | § 8 tag conventions; intermediate tags per workstream checkpoint |
| **#7 Capture decision telemetry** | Per-phase JSON summary artifacts at known paths (per § 12 cross-session continuity) |
| **#8 Schema validation at boundaries** | P0 schema lock validates; P1 imports validate per-record against schema |
| **#9 Attribution clarity** | Per-source tagging on every imported record; license-class capture per record |
| **#10 Empirical inspection over assumption** | Discipline #17 calibration sweeps; sample-inspection passes at every phase |
| **#11 Live-state verification** | Per-phase critique pairs include live-state checks (DB queries) |
| **#12 Semantic shift** | Pre-imposed-vocabulary → discovered-vocabulary migration is itself a semantic shift; gandalf + Matt review labels |
| **#13a Drift detection** | Jack-ryan audits per-phase compliance; risk register monitored at phase boundaries |
| **#13b Per-variable attribution** | Per-feature provenance tracking on extracted feature vectors |
| **#14 Terminology lock** | Per `legacy-categorical-cleanup-audit-2026-05-22.md` § 7 canonical replacement language |
| **#15 UI scope decomposition** | N/A — no UI surface in this protocol; Profile A demo integration is separate workstream |
| **#16 Tuning-drift constants** | Cluster count target (50-150); reference-image coverage (≥70%); axis variance threshold (≥80%); calibration thresholds explicit |
| **#17 Empirical calibration smoke** | P2 axis-interpretation calibration; P5 visual-cohesion + density-bucket calibration |
| **#18 Joint-gate ship criterion** | Substrate ready for W1.15 consumption requires: ≥80% labeled clusters + density map populated + reference-image coverage ≥70% |
| **#19 Agent tool not for waiting** | RATIFIED 2026-05-22; ALL long-running phases as background processes; status via direct Bash + DB queries |
| **#20 robots.txt + Claude-agent directive respect** | Jack-ryan parallel authoring per session; pre-flight P0.8 verification per crawl source |

---

## 12. Cross-session continuity

Per Discipline #19, every dispatch produces a JSON summary at a known path. Summaries act as cross-session continuity if orchestrator session ends mid-phase:

| Phase | Summary artifact path |
|---|---|
| P0 | `agentic_orchestration/logs/schema_lock_summary.json` |
| P1 Track A per-source | `agentic_orchestration/logs/<source>_crawl_summary.json` |
| P1 Track B per-source | `~/Games/reincarnated-engine/logs/<source>_import_summary.json` |
| P1.5 | `~/Games/reincarnated-engine/logs/feature_extraction_summary.json` |
| P2 W2.1 | `~/Games/reincarnated-engine/logs/axis_discovery_summary.json` |
| P2 W2.2 | `~/Games/reincarnated-engine/logs/bdi_seeding_summary.json` |
| P3 | `~/Games/reincarnated-engine/logs/clustering_analysis_summary.json` |
| P4 | `canonical/story/emergent-cluster-catalogue-2026-05-XX.md` (canonical doc IS the artifact) |
| P5 sub-A | `agentic_orchestration/galadriel/logs/cluster_validation_summary.json` |
| P5 sub-B | `~/Games/reincarnated-engine/logs/substrate_density_summary.json` |
| PD per iteration | `agentic_orchestration/logs/meshy_gapfill_iteration_<N>_summary.json` |

Next-session orchestrator recovers state by reading these files + querying DB row counts.

---

## 13. Autonomous operation protocol

### 13.1 Default mode

Knight-rider orchestrates dispatches per phase sequencing. Specialists execute per dispatch. No specialist needs Matt input mid-phase unless gate G1/G2/G3/G4 surfaces.

### 13.2 Escalation paths

- **Per-phase issues** → knight-rider triages; routes to appropriate specialist or escalates to Matt
- **Design issues** (cluster labeling, axis interpretation) → gandalf reviews; escalates to Matt for design call
- **Technical issues** (algorithm choice, methodology) → jack-ryan reviews; escalates to Matt for engineering call
- **Hard blockers** (license review, partner outreach, schema migration) → direct Matt escalation

### 13.3 Communication protocol

- Per-phase status: DB queries + summary file existence
- Per-phase completion: CHANGELOG entry + tag
- Cross-session: this protocol doc + JSON summaries
- Matt session-open: knight-rider posts state-of-phase summary

### 13.4 Emergency protocols

- Mid-phase failure: capture state in JSON; tag intermediate state; pause; surface to knight-rider; resolve via Matt input or specialist iteration
- Data corruption: restore from last milestone tag; re-run affected phase
- Resource exhaustion (DB size, processing time): scope reduction; defer non-blocking sources

---

## 14. Recommended knight-rider kickoff sequence

**Tomorrow morning's first knight-rider session (per source plan § 6):**

1. **Read** this protocol + the source operational plan + `skill_handoff_2026-05-22-evening.md` for full context
2. **Resolve P0.1 + P0.2** with Matt (env var persist + probe; ~5 min Matt time)
3. **Resolve P0.5** with Matt (Smithsonian API key registration; non-blocking but unblocks Source D6)
4. **Fire Phase 0 (W0.1-W0.4)** — schema lock; ~5 min
5. **Author and fire Phase 1 parallel dispatches:**
   - Track A: Wikipedia + Wikidata + game wikis + SRD + museums + TVTropes + IMFDB + anime/manga wikis
   - Track B (per G1 outcome): Meshy + Sketchfab + Kenney + OGA + Smithsonian
6. **Monitor Phase 1 via direct DB COUNT queries** (Discipline #19-compliant; no babysit)
7. **When Phase 1 ≥80% complete:** fire P1.5 (feature extraction)
8. **When P1.5 completes:** fire P2 (axis discovery + BDI ω seeding)
9. **When P2 completes:** fire P3 (clustering analysis)
10. **When P3 completes:** schedule G3 (cluster labeling design call) with Matt
11. **After P4 lands:** fire P5 sub-A + sub-B in parallel
12. **Post-P5:** G4 — review density map with gandalf + Matt; identify priority Phase D targets
13. **PD onwards:** operational ongoing; per-iteration galadriel summary
14. **On phase completion:** CHANGELOG entry; mark phase done; tag milestone

---

## 15. Open questions for Matt (review before kickoff)

Per source plan § 7 (carried forward):

| # | Question | Default if no response |
|---|---|---|
| Q1 | If Meshy API library-browse endpoints exist under partner-tier (not Pro): partner-tier outreach + wait, OR start with D3-D6 + Meshy-generation-only Phase D? | Start with D3-D6 in parallel; partner outreach runs in background; pivot Phase 1 Track B if outreach succeeds |
| Q2 | CC-BY-SA legal review completion timing? Blocks game_approved=1 but doesn't block import. | `game_approved=0` for CC-BY-SA assets pending review; revisit at pre-cutover |
| Q3 | Clustering algorithm preference (hierarchical / HDBSCAN / k-means / hybrid)? | gandalf-recommended **hybrid (semantic + geometric)** with hierarchical output for multi-granularity |
| Q4 | Cluster count target (50 / 100 / 150)? | Default 75-100 (gandalf intuition; refinable post-P3) |
| Q5 | Phase 4 design call format — single 2-3 hour session, or split across days? | Default: split across days for designer-craft reasons; clusters benefit from sleep between reviews |
| Q6 | Galadriel visual validation (P5 sub-A) — full population or sampled? | Sampled (50-100 weapons per cluster) for time efficiency; full only if outlier flagging surfaces concerns |
| Q7 | Statistical axis discovery methodology preference (PCA / FA / NMF / sparse / mixed)? | Default: mixed-effects (PCA on geometric+mechanical; FA on semantic+visual); rocket + legolas Mode A justify choice in W2.1 spec |
| Q8 | Reference-image coverage <70% — accept and proceed to P2, or pause for additional source crawls? | Default: accept and proceed; PD prioritizes gap-fill on sparse-reference-image regions |

---

## 16. Estimated timeline

Per source plan § 8:

| Phase | Duration (wall) | Active Matt time |
|---|---|---|
| P0 (schema lock) | 5 min | 0 |
| P1 (imports parallel) | 4-8 hours wall time; up to several days if Meshy bulk path engaged | ~30 min for P0 checks + dispatch authoring review |
| P1.5 (feature extraction) | 1-2 hours | 0 (rocket-owned) |
| P2 (axis discovery + ω seeding) | 1-3 days | ~30 min for axis-loadings interpretation review |
| P3 (clustering analysis) | 1-2 days | 0 (legolas/rocket-owned) |
| P4 (cluster labeling) | 2-3 hours focused (could span days) | **2-3 hours active Matt time** |
| P5 (validation + density) | 4-8 hours parallel | 0 (galadriel + rocket-owned) |
| PD (ongoing) | Operational | ~30 min per iteration for prioritization |
| **Total wall time** | **~1-2 weeks** | **~3-4 hours active Matt time** |

---

## 17. What this delivers

When all phases complete:

| Deliverable | What it enables |
|---|---|
| **~15,000-30,000 knowledge entries** in DB | Engine-side substrate-vector queries return rich knowledge-based candidate sets |
| **~4,000-6,500 model attachments** in DB | Visual realization for queried knowledge entries |
| **≥70% knowledge entries with reference images** | Meshy validation loop operational |
| **Discovered axes from PCA / factor analysis** (Pattern 6 operationalization) | Pre-imposed taxonomies replaced by data-derived axes |
| **50-150 semantically-labeled emergent clusters** | Cohesion-judge reads cluster identity; profile flags reference cluster labels |
| **BDI ω-scores populated** | Density-routing-by-element functional; cohesion-judge prompts grounded |
| **Substrate-density precomputed** | O(1) density-check + routing-decision per generation cycle |
| **Phase D canonical pipeline operational** | Knight-rider fires Meshy generation gap-fill dispatches against sparse regions |
| **Profile A asset pipeline ready** | Reincarnated v1 spirit-form library generation has real substrate to query |

This is the **structural work** that turns gear-substrate from a hand-authored 15-entry sketch into a substrate-as-cohesion-coherent emergent system. It is what Patterns 4-5-6 require operationally to land.

---

## 18. Maintenance and revision protocol

### 18.1 When to revise this protocol

- Phase completion changes scope estimate → update § 5 + § 16
- New crawl source surfaces → add to § 6.2 Track A workstreams
- Statistical methodology shifts → update § 6.4 W2.1
- Cluster algorithm choice locks → update § 6.5 W3.1
- Risk realized → add mitigation outcome to § 9 risk register

### 18.2 Who revises

- gandalf (planner; protocol author) for structural revisions
- knight-rider (orchestrator) for operational sequencing updates
- jack-ryan for discipline-compliance updates
- specialists (legolas, rocket, galadriel, drax) for per-workstream revisions

### 18.3 Versioning

v1 = this protocol (initial). v1.1 = post-P3 clustering results inform refinements. v2 = post-PD operational learnings inform refinements (likely +6 months out).

---

## 19. Cross-references

### 19.1 This session's canonical foundations
- `canonical/story/legacy-categorical-cleanup-audit-2026-05-22.md` — Patterns 4-5-6 architectural detail (the why)
- `canonical/story/gear-heavy-promotion-2026-05-22.md` — vast-library substrate architecture (the what)
- `canonical/story/engine-as-general-serial-content-product-2026-05-22.md` — Variant C strategic lock (the strategic frame)
- `canonical/story/stat-derivation-from-bc-convergence-2026-05-22.md` — stat-derivation (downstream consumer)
- `canonical/story/asset-pipeline-meshy-swap-2026-05-22.md` — Phase D Meshy gap-fill pipeline (companion)

### 19.2 Parent protocol
- `canonical/story/hive-mind-protocol-qd-engine-rebuild-2026-05-21.md` v1.3 — parent protocol; § 6.2 P1 substrate enrichment is the workstream this protocol operationalizes
- `canonical/story/engine-architecture-vision-qd-profile-2026-05-19.md` — vision document foundation
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` — BC axes canonical definitions

### 19.3 Source operational plan
- `agentic_orchestration/weapon-library-import-orchestration-plan-2026-05-22.md` — operational plan (RE-PLAN section authoritative); this protocol elevates + structures

### 19.4 Research foundations
- `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/` — 7 files; weapon library import discovery + schema (562-line `schema.sql`)
- `agentic_orchestration/legolas/research/unity-catalogue-armor-meshy-2026-05-22/` — Unity catalogue + Meshy armor capability research
- `agentic_orchestration/legolas/research/meshy-pipeline-2026-05-22/findings.md` — Meshy pipeline capability research
- `agentic_orchestration/galadriel/notes/2026-05-22-canary-meshy-regen.md` § 8 — canonical pipeline rule

### 19.5 Discipline + governance
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — all 19 disciplines (Discipline #20 forthcoming per jack-ryan parallel authoring)
- `~/Games/reincarnated-engine/design/decisions/decisions-log.md` — Discipline #19 ratification entry; future entries for vestigial-pattern retirements
- `agentic_orchestration/CHANGELOG.md` — phase milestone records

### 19.6 Schema + DB
- `/Users/admin/Games/reincarnated-loadout/data/telemetry.db` — greenfield SQLite DB (empty as of 2026-05-22 evening)
- `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/schema.sql` — ready-to-run DDL; needs cluster + knowledge-entry table amendments per P0

### 19.7 Memory references (Matt manual update per audit § 6.3)
- `memory/project_role_orientation_taxonomy.md` — Pattern 2 historical/diagnostic-only
- `memory/project_trait_architecture.md` — Pattern 3 legacy / borderline vestigial
- `memory/project_earth_meta_layer.md` — Reincarnated overlay design (load-bearing; no change)
- `memory/project_pet_system.md` — companion architecture pulls forward (no change)

---

## 20. Closing — what this protocol commits

This protocol commits the hive to a coordinated multi-phase substrate-acquisition + analysis workstream that operationalizes three vestigial-pattern retirements (Patterns 4-5-6 per the audit). The substrate-as-cohesion architectural commitment requires that the data exist for emergent clustering + statistical axis discovery to land; this protocol acquires that data and processes it through the analysis pipeline.

What's at stake:

- **Without this protocol's outputs, the substrate-as-cohesion commitment is performative at the gear-substrate layer.** The 15-entry catalogue stays as vestigial pre-imposition; the pre-imposed axes stay as designer-authored coordinates; the engine claims substrate-as-cohesion architecturally while carrying categorical pre-imposition operationally.

- **With this protocol's outputs, Patterns 4-5-6 land for real.** The vast library is the substrate; emergent clusters carry gear-form identity; discovered axes replace pre-imposed taxonomies; the engine queries against the library via substrate-vectors; Profile A's asset pipeline draws from the substrate the engine knows about.

The Reincarnated profile overlay benefits directly: the spirit-form library accumulates from a substrate that spans multiple cultural lineages + multiple aesthetic registers, not from a 15-entry Eurocentric medieval list. Earth Self's collection grows in variety + cultural depth.

The general engine (per Variant C) benefits: Profile B/C/D customers can target their own substrate-vectors against the library; cultural-lineage diversity is real data, not configuration defaults.

The road continues. The Mirror is ready to see what emerges from 15,000-30,000 weapon knowledge entries.

---

**Signed:** gandalf (planner; not orchestrator)
**Authority:** Matt 2026-05-22 evening — "tee up for knight-rider and the hive mind. This is structural work."
**For:** canonical lock of the weapon library import + Pattern-6 axis discovery + emergent clustering workstream at hive-mind-protocol status; knight-rider's tomorrow-morning session takes ownership of execution sequencing per § 14 kickoff sequence; hive specialists (legolas / rocket / galadriel / drax / jack-ryan) consume per-phase dispatches when authored; Matt holds gates G1-G4 + ~3-4 hours active time across the workstream's ~1-2 weeks.

**Knight-rider:** when you pick this up, read § 3 pre-flight checks first; resolve P0.1 + P0.2 + P0.5 with Matt; then sequence dispatches per § 14 kickoff sequence. This protocol is the spine; you author the per-phase dispatches against it. Hold gates G1-G4 for Matt input.

**Matt:** your ~3-4 hours of active time concentrate at:
- Pre-flight check resolution (~30 min)
- P2 axis-loadings interpretation review (~30 min)
- P4 cluster semantic labeling design call (~2-3 hours)
- Decision-gate inputs (G1-G4; ~30 min spread)

The hobbits sleep. The work begins again at dawn.
