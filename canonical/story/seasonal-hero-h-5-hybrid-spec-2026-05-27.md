# Seasonal Hero — H-5 Hybrid Design Spec

> **STATUS:** CURRENT (load-bearing as of 2026-05-27) — canonical spec for the seasonal_hero surface across Phase 4 emission, Phase 5 cluster-level composition, gandalf design-call workflow, and drax Summary tab consumption. Authored per Matt 2026-05-27 design call #1 ratification: "Seasonal hero: H-5 hybrid (substrate produces top-3; gandalf curates 1 from top-3)."

**Date:** 2026-05-27 evening
**Author:** gandalf (story-and-design steward)
**Status:** CANONICAL — load-bearing for Phase 4 emission impl + Phase 5 PM-2 amendment + drax Dispatch C (Summary tab redesign) + star-lord telemetry consumption
**Authority:** Matt 2026-05-27 verbatim design call #1: "Seasonal hero: H-5 hybrid (substrate produces top-3; gandalf curates 1 from top-3). Implementation: Phase 4 + 5 emit seasonal_hero_candidates metadata post Wave 5; gandalf design-call selects season_hero_id; drax surfaces in Summary tab."
**Companion docs:**
- `canonical/49-loadout-sample-player-surface-design-2026-05-27.md` — player-surface architecture; Summary tab dependency (§ 4.3); seasonal hero surfaces alongside primary_faction_pair narrative
- `canonical/41-progression-framework-2026-05-27.md` — endgame anchor + composition framework
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` — kit shape architecture (chain_count + T4 candidates + supporting chain emit)
- `agentic_orchestration/gandalf/notes/2026-05-27-path-iii-faction-assembly-extension.md` — Path (III) faction-assembly extension; primary_faction_pair + inter-faction narratives at Summary tab
- `agentic_orchestration/drax/notes/2026-05-27-cycle-14-tab-integration-pattern-a-response.md` — Summary tab scope; gate on this spec
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Discipline #41 (substrate-led; LOAD-BEARING for top-3 selection algorithm); Discipline #43 (design-quality audit at wave-close; LOAD-BEARING for gandalf design-call authority); Discipline #45 (vocabulary lock at player surface)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/phase4_db.py` — kit_archive schema (Phase 4 output)
- `~/Games/reincarnated-engine/src/reincarnated/export/schemas.py` — ExportFactionCluster + ExportFactionRelationship (Phase 5 output)

---

## 0. TL;DR

**Decision (Matt 2026-05-27):** H-5 hybrid pattern — substrate produces a top-3 seasonal-hero candidate list per season; gandalf curates 1 from the top-3 as the canonical `season_hero_id`; drax surfaces the curated hero in the Summary tab.

**Composition pattern:**

```
[Phase 4 — gamora]                  [Phase 5 — star-lord]               [Wave 5 close — gandalf]              [Dispatch C — drax]
kit_archive →                       cluster-level aggregation →         design-call selection from top-3 →    Summary tab consumption
SUBSTRATE METRIC scoring →          ExportFactionCluster +              audit-log entry under #43 →            season_hero_id displayed
top-3 emission per season           ExportSeasonHeroCandidates           season_hero_id finalized               D-Sharpened invariance held
                                    list emission
```

**Discipline #41 substrate-led discipline LOAD-BEARING:** the top-3 MUST be derived from a substrate-emergent metric (composite of Q-vector quality + cohort-distinctiveness + substrate-anchor-richness, defined § 3 below). It MUST NOT be a pre-authored personality archetype shortlist, named-personage roster, or canonical-archetype-register filter. **Gandalf curation pick from top-3 is design-judgment within Discipline #43 audit authority — NOT pre-authored taxonomy reimposition.**

**D-Sharpened invariance preserved:** the seasonal hero's substrate_anchored_personage (if any) remains engine-internal analytics only; player-facing surface uses Phase 5 cohesion-judge LLM canonical name uniformly across all kits regardless of substrate anchor.

---

## 1. Player-experience intent

### 1.1 What "seasonal hero" means to the player

In ARPG genre composition, "the season's hero" is the canonical face of the season — the character that defines what THIS season was about. This is genre-conventional across the lineage:

- **Diablo III seasons:** each season has a thematic class focus and signature build (e.g., "Necromancer-driven blood-mage season"). The "hero" of the season is informal but recognizable.
- **PoE league characters:** each league surfaces a defining build that captures the league's mechanic identity.
- **Last Epoch seasonal cycles:** each cycle has a signature playstyle the meta crystallizes around.
- **Isekai genre convention (Mushoku Tensei, Slime, Solo Leveling):** each major arc surfaces a "protagonist of THIS arc" — the form/spirit that carries the season's narrative weight.

The seasonal hero answers the player's recognition question: "When I look back at season N, what character do I REMEMBER?"

### 1.2 Player consequence

Without a seasonal hero surface, the season is a flat cohort of survivors — N kits with no narrative emphasis. The player can identify factions (per Path III F-C) and explore individual kits (Loadout + Sample tabs), but no single character carries the season's identity.

WITH a seasonal hero surface, the season has a face. The Summary tab opens to this face. The Court of Forms (Cycle 15+) accumulates this face as the season's signature ascended-form. Narrative recognition lands.

### 1.3 What "H-5 hybrid" preserves vs what it discards

**Pure substrate-led (H-1):** algorithm picks the top kit; gandalf has no input. Risk: substrate picks a kit that scores well mechanically but lacks narrative weight (e.g., the most-optimized kit may not be the most THEMATICALLY interesting).

**Pure design-curation (H-9):** gandalf picks freely from the full cohort. Risk: violates Discipline #41 — gandalf pre-imposes design judgment that the substrate hasn't earned; reintroduces taxonomy bias.

**H-5 hybrid (Matt 2026-05-27):** substrate produces top-3 via substrate-emergent metric; gandalf selects 1 from the 3 as design-judgment within Discipline #43 audit authority. **Both the substrate-led discipline AND the narrative-curation contribution land.** This is the load-bearing path.

---

## 2. Architectural composition

### 2.1 Where the metadata lives — emission flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ Phase 4 (gamora)                                                            │
│  • Per-season kit_archive populated (gauntlet-passed survivors)             │
│  • SUBSTRATE METRIC scoring per kit (§ 3 below)                             │
│  • Per-season seasonal_hero_candidates emission: top-3 kit_ids + scores     │
│  • Field: kit_archive.seasonal_hero_candidates_json (NEW; § 4.1 below)      │
└─────────────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│ Phase 5 (star-lord)                                                         │
│  • PM-1 clustering → emergent clusters                                      │
│  • PM-2 D-Hybrid faction-label LLM (ExportFactionCluster)                   │
│  • G-B primary_faction_pair selection                                       │
│  • F-C inter-faction relationship narratives (ExportFactionRelationship)    │
│  • PM-2 amendment: emit ExportSeasonHeroCandidates (§ 4.2 below)            │
│       composes Phase 4 top-3 with cluster-membership context                │
└─────────────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│ Wave 5 close (gandalf)                                                      │
│  • Post audit-gate PASS                                                     │
│  • Gandalf reviews top-3 candidates + cluster context + cohesion-judge      │
│    canonical names                                                          │
│  • Gandalf selects season_hero_id from top-3 (autonomous per § 5 below)     │
│  • Audit log entry per Discipline #43 audit record                          │
│  • Emit ExportSeasonHero (§ 4.3 below) with finalized season_hero_id        │
└─────────────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│ Dispatch C (drax) + star-lord telemetry                                     │
│  • Summary tab consumes ExportSeasonHero                                    │
│  • Displays canonical kit name + faction context + 1-2 sentence flavor      │
│  • D-Sharpened invariance: substrate_anchored_personage metadata HIDDEN     │
│  • Star-lord telemetry: season_hero_id logged for cross-season analysis     │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Single source of truth (composes with doc 49 § 2.3)

The seasonal_hero surface composes with doc 49's single-source-of-truth pattern: engine emits canonical state; drax/star-lord consume read-only. The seasonal_hero is NOT a separately curated runtime object — it is a derived selection from the gauntlet-passed survivor cohort, with the selection persisted in the engine emission.

---

## 3. Substrate metric — top-3 selection algorithm (Discipline #41 LOAD-BEARING)

### 3.1 Q-Bundle-1 decision (gandalf judgment under Discipline #41)

**Algorithm:** **Composite substrate metric** combining three substrate-emergent signals:

1. **Q-vector quality** (kit_archive Q1-Q5 normalized) — combat-validated kit quality
2. **Cohort distinctiveness** (Mahalanobis distance from cohort mean in 8-axis BC space) — substrate-emergent uniqueness within THIS season
3. **Substrate-anchor richness** (substrate_anchored_personage presence; D-Sharpened metadata) — narrative depth substrate contributes

Each signal is substrate-emergent (NOT a pre-authored archetype shortlist). The composite is computed per kit; top-3 emitted per season.

### 3.2 Composite formula

```
seasonal_hero_score(kit_i) = 
    w_quality   · Q_norm(kit_i)
  + w_distinct  · D_mahalanobis(kit_i, cohort_mean) / D_max_in_season
  + w_anchor    · anchor_signal(kit_i)

where:
  Q_norm(kit_i) = (Q1 + Q2 + Q3 + Q4 + Q5) / 5     # already 0-1 normalized per Q-axis
  
  D_mahalanobis(kit_i, cohort_mean) = computed over 8-axis BC space using
    cohort covariance estimated from this season's kit_archive (Discipline #46
    bounded query; cohort size ~28-32 per season → trivial compute)
  
  D_max_in_season = max(D_mahalanobis(kit_j, cohort_mean)) for kit_j in season
                    (normalizes distinctiveness to [0, 1] within-season)
  
  anchor_signal(kit_i) = 1.0 if substrate_named_personage_anchor != null
                         (Sketch F D-Sharpened anchor present)
                       = 0.0 otherwise
  
weights (Cycle 14 initial):
  w_quality  = 0.5
  w_distinct = 0.3
  w_anchor   = 0.2

(weights sum to 1.0; gandalf may revise via amendment after first 3 seasons of
empirical observation; revision is design-judgment within #43 audit authority)
```

### 3.3 Why each signal is substrate-led

- **Q-vector quality:** Q1-Q5 are emergent from gauntlet-sim outcomes. Not pre-authored. Reflects substrate combat response.
- **Mahalanobis distinctiveness:** computed over 8-axis BC space (engagement_profile, damage_geometry, proxy_density, control_density, damage_tempo, damage_amplitude_variance, defensive_profile, resource_economy — per `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md`). BC axes are substrate dimensions. Distinctiveness within-season is substrate-emergent.
- **Anchor signal:** substrate_named_personage_anchor is a D-Sharpened metadata field (Sketch F substrate-anchored personage; ~32% of kits per PM-2 § 2.7). Anchor allocation is substrate-driven (not pre-authored per-kit). The signal indicates "this kit carries substrate-anchored narrative depth"; it does NOT impose what that depth means.

### 3.4 Why this is NOT a pre-authored taxonomy

The composite metric:
- Does NOT name personality archetypes or filter to a fixed shortlist (e.g., "hero / villain / antihero")
- Does NOT filter by anchor LINEAGE (e.g., "European anchors only"); the signal is presence/absence binary
- Does NOT name "classes" or class-equivalents (Discipline #45 vocabulary lock holds)
- Does NOT rank by pre-authored thematic categories (e.g., "fire kits preferred")

The metric is purely substrate-statistical. Top-3 candidates emerge from the substrate; gandalf's curation pick (§ 5) is design-judgment over the SUBSTRATE-EMERGENT top-3, not pre-imposed pre-filtering.

### 3.5 Tiebreaks

If two or more kits tie within ε = 0.01:
1. Higher Mahalanobis distinctiveness wins (more distinctive within-season carries more narrative weight)
2. If still tied, anchor-present wins over anchor-absent
3. If still tied, lower kit_id wins (deterministic; reproducible)

### 3.6 Edge cases

- **Season with < 3 surviving kits:** top-N emitted (N = cohort size); gandalf curates from the actual cohort
- **Season with all-anchor-absent kits:** anchor_signal contributes 0 to all; ranking driven entirely by quality + distinctiveness (still substrate-led; no fallback to pre-authored taxonomy)
- **Highly degenerate season (all kits in one tight cluster):** D_max_in_season may be small; distinctiveness contribution flattens; ranking driven mostly by Q-quality. Acceptable degeneracy — preserves substrate-led semantics.

---

## 4. Emission schemas (cross-seam consumption)

### 4.1 Phase 4 emission — kit_archive amendment (gamora ownership)

**Approach:** seasonal_hero candidate scoring computed per-season at Phase 4 close (after all kits inserted into kit_archive); emitted as a new per-season metadata record (NOT a per-kit field on kit_archive — composite is season-scoped).

**New table (proposed):**

```sql
CREATE TABLE IF NOT EXISTS seasonal_hero_candidates (
    season_id              INTEGER NOT NULL PRIMARY KEY,
    candidate_kit_ids      TEXT NOT NULL,                -- JSON list of top-3 kit_ids in rank order
    candidate_scores       TEXT NOT NULL,                -- JSON list of top-3 composite scores
    candidate_breakdown    TEXT NOT NULL,                -- JSON list of per-candidate (q_norm, d_mahalanobis_norm, anchor_signal) triples
    selection_metadata     TEXT NOT NULL,                -- JSON: {w_quality, w_distinct, w_anchor, algorithm_version}
    inserted_at            TEXT NOT NULL,                -- ISO8601
    notes                  TEXT
);

CREATE INDEX IF NOT EXISTS idx_seasonal_hero_candidates_season
    ON seasonal_hero_candidates (season_id);
```

**Discipline #46 § 7 compliance:** per-season scoping; cohort size ~28-32; computation O(N) ranking + O(N) Mahalanobis (cohort covariance estimated once per season). No unbounded scan.

**Discipline #41 compliance:** algorithm IS the substrate-emergent metric per § 3. No pre-authored taxonomy filter. Algorithm-version field allows future amendment under audit trail.

**Composition with kit_archive:** seasonal_hero_candidates references kit_archive.kit_id via candidate_kit_ids. Joinable for downstream analysis. kit_archive itself is not amended (preserves cell-level addressability per Discipline #46 § 7).

**Phase 4 IMPL trigger:** new module `simulation/spatial_gauntlet/seasonal_hero_scorer.py` (or co-located in `phase4_db.py` per gamora seam preference); fires once per season at Phase 4 close after all kits archived.

### 4.2 Phase 5 PM-2 amendment — ExportSeasonHeroCandidates (star-lord ownership)

**Approach:** Phase 5 reads Phase 4 seasonal_hero_candidates table; composes with cluster-membership context; emits ExportSeasonHeroCandidates record per season.

**New Pydantic schema (proposed; star-lord seam):**

```python
class ExportSeasonHeroCandidates(BaseModel):
    """Top-3 seasonal-hero candidate list per season — Wave 5 H-5 hybrid output.
    
    Composes Phase 4 substrate-metric ranking with Phase 5 cluster-membership
    context. Consumed by gandalf at Wave 5 close for design-call curation.
    Written to exports/<season_id>/season_hero_candidates.json.
    
    Discipline #41 LOAD-BEARING: top-3 selection is substrate-emergent metric
    per gandalf spec § 3 — NOT pre-authored personality archetype shortlist.
    """
    season_id: str
    
    # Top-3 in rank order (highest composite score first)
    candidate_kit_ids: list[str]
    candidate_scores: list[float]
    
    # Per-candidate signal breakdown (analyst transparency + audit trail)
    candidate_breakdowns: list[dict[str, float]]
    # each dict: {q_norm, d_mahalanobis_norm, anchor_signal}
    
    # Cluster context per candidate (composes with PM-2 ExportFactionCluster)
    candidate_cluster_ids: list[int]
    candidate_faction_label_canonicals: list[str | None]
    
    # Anchor metadata per candidate (D-Sharpened analytics; NEVER LLM-prompt-exposed)
    candidate_substrate_anchors: list[str | None]
    # ↑ substrate_named_personage_anchor when present; null otherwise
    
    # Cohesion-judge canonical names per candidate (Phase 5 LLM output)
    candidate_kit_name_canonicals: list[str | None]
    # ↑ e.g., "Crimson Reaver" from cohesion-judge; null if LLM short-circuited
    
    # Algorithm provenance
    selection_algorithm_version: str   # e.g., "v1.0_composite_2026-05-27"
    selection_weights: dict[str, float]  # {w_quality, w_distinct, w_anchor}
    
    # Audit hooks
    inserted_at: str
```

**Composition with ExportFactionCluster:** ExportSeasonHeroCandidates.candidate_cluster_ids joins to ExportFactionCluster.cluster_id. Allows gandalf to consider faction context at curation time.

**Composition with cohesion-judge:** candidate_kit_name_canonicals derives from Phase 5 cohesion-judge LLM output (kit-level canonical naming). Provides player-facing name for each candidate.

### 4.3 Wave 5 close — ExportSeasonHero (gandalf curation output)

**Approach:** after gandalf's design-call selection (§ 5 below), emit a single ExportSeasonHero record per season — the finalized canonical hero.

**New Pydantic schema (proposed):**

```python
class ExportSeasonHero(BaseModel):
    """Finalized seasonal hero per season — gandalf curation output.
    
    Selected from ExportSeasonHeroCandidates top-3 by gandalf at Wave 5 close.
    Selection is design-judgment within Discipline #43 audit authority;
    audit-log entry MUST be present.
    
    Written to exports/<season_id>/season_hero.json.
    Consumed by drax Summary tab + star-lord telemetry.
    
    D-Sharpened invariance preserved: substrate_named_personage_anchor is
    analytics metadata only; player-facing surface uses kit_name_canonical
    uniformly per cohesion-judge output.
    """
    season_id: str
    
    # The chosen kit
    season_hero_kit_id: str
    
    # Player-facing surface (cohesion-judge canonical; uniform per D-Sharpened)
    season_hero_kit_name_canonical: str | None
    # ↑ e.g., "Crimson Reaver"; null only if cohesion-judge short-circuited
    
    # Faction context
    season_hero_cluster_id: int
    season_hero_faction_label_canonical: str | None
    
    # Composite score from substrate-emergent metric
    season_hero_composite_score: float
    season_hero_signal_breakdown: dict[str, float]
    # ↑ {q_norm, d_mahalanobis_norm, anchor_signal}
    
    # Gandalf curation provenance (Discipline #43 audit hook)
    selection_rationale: str
    # ↑ 1-3 sentences; gandalf cites which substrate signal(s) drove the pick
    #   among the 3 candidates. Stored verbatim for audit transparency.
    # ↑ MUST cite substrate-emergent rationale; pre-authored taxonomy rationale
    #   is a Discipline #41 violation and #43 audit FAIL.
    
    selection_audit_log_ref: str
    # ↑ pointer to wave-close audit-log entry per Discipline #43
    
    # D-Sharpened analytics (NEVER displayed to player; star-lord telemetry only)
    substrate_anchored_personage_internal: str | None = None
    # ↑ e.g., "Lu Bu"; engine-internal analytics anchor; D-Sharp-1 invariance held
    
    # Provenance
    selected_at: str
    selected_by: str = "gandalf"
    candidate_pool_ref: str  # path to ExportSeasonHeroCandidates JSON for this season
```

**D-Sharpened invariance:** ExportSeasonHero.substrate_anchored_personage_internal is engine-internal analytics ONLY. Drax MUST NOT surface this field at the player surface. Player sees season_hero_kit_name_canonical (Phase 5 cohesion-judge uniform LLM naming) — same surface as any other kit. This preserves the D-Sharpened pattern across the entire emission chain.

### 4.4 Cross-seam emission summary

| Stage | Owner | Emission | Consumer |
|---|---|---|---|
| Phase 4 close | gamora | `seasonal_hero_candidates` table | star-lord (Phase 5 input) |
| Phase 5 PM-2 amendment | star-lord | `ExportSeasonHeroCandidates` JSON | gandalf (Wave 5 close input) |
| Wave 5 close | gandalf | `ExportSeasonHero` JSON | drax (Summary tab) + star-lord (telemetry) |
| Drax consumption | drax | Summary tab display | player |
| Star-lord telemetry | star-lord | cross-season aggregation | analytics; sidecar; Cycle 15+ Court mechanics |

---

## 5. Gandalf design-call workflow (Q-Bundle-3)

### 5.1 Q-Bundle-3 decision (gandalf judgment)

**Workflow:** **gandalf-autonomous selection within Discipline #43 audit authority** — NOT Pattern-B Matt design-call by default.

**Rationale:**

- Discipline #43 (design-quality audit at wave-close) explicitly grants gandalf the authority to make design judgments at wave-close as part of the design-quality audit. The seasonal hero selection IS a design-quality call: which of the top-3 substrate-emergent candidates best serves narrative recognition?
- Pattern-B Matt design-call default would surface a routine selection to Matt for ratification — over-asking pattern (per CLAUDE.md addendum 2026-05-25 retiring knight-rider over-asking).
- The top-3 are ALREADY substrate-bounded; gandalf is choosing among substrate-equivalent options at the metric level. The choice is design-curation, not architectural commitment.

**Escalation to Pattern-B Matt design-call (rare exceptions only):**

Gandalf escalates to Matt design-call IF:

1. **Top-3 has near-tied composite scores** (max gap < 0.05) — the substrate hasn't strongly preferred any candidate; gandalf surfaces to Matt rather than make a flat curation call
2. **Discipline #41 substrate-led check fails** — gandalf cannot honestly cite a substrate-emergent rationale for any of the 3 picks; surface to Matt with the discipline concern raised explicitly
3. **Cross-season continuity concern** — selecting this season's hero appears to reimpose a thematic taxonomy across seasons (e.g., "every season I'm picking the fire-anchor kit"); surface to Matt for cross-season pattern review (defends against drift per Discipline #18 implicit-pillar-drift composition)
4. **Selection would conflict with Path III primary_faction_pair narrative emphasis** (e.g., season hero NOT in primary_pair faction, breaking the season's narrative center) — surface to Matt for narrative-architecture call

**Default path:** gandalf-autonomous; no escalation; audit-log entry per Discipline #43.

### 5.2 Audit log entry format (Discipline #43 wave-close audit record)

Gandalf appends a per-season entry to the wave-close design-quality audit record:

```markdown
## Seasonal hero selection — season_id <N>

**Top-3 candidates (substrate-emergent ranking):**
1. kit_id=<A>; composite_score=<X.XX>; breakdown=(q=<>, d=<>, anchor=<>)
   cohesion-judge name=<canonical>; cluster=<id>; faction=<label>
2. kit_id=<B>; ... [same fields]
3. kit_id=<C>; ... [same fields]

**Gandalf selection:** season_hero_id = <kit_id>

**Selection rationale (Discipline #41 substrate-led; Discipline #43 audit-eligible):**
<1-3 sentences citing the substrate-emergent reason. MUST reference at least
 one of: (a) which signal in the composite metric drove the pick, (b) which
 cluster/faction context supports this candidate as season-defining, (c)
 which substrate anchor (if present) contributes narrative depth.>

<MUST NOT cite: pre-authored personality taxonomy, fixed-class roster
 thinking, named-personage curation outside substrate emergence,
 Discipline #45 prohibited vocabulary.>

**Escalation triggered?** [No | Yes — reason: <one of § 5.1 triggers>]
```

### 5.3 Discipline #43 audit gate composition

Wave 5 close audit-gate PASS (gandalf design-quality audit) is the precondition for seasonal_hero selection. If the wave-close audit returns DRIFT-DETECTED (e.g., A2 pre-authored taxonomy introduction at any wave output; A4 substrate-led architectural drift), gandalf MUST resolve the drift BEFORE finalizing season_hero_id. The seasonal_hero surface inherits the wave's discipline status.

---

## 6. Drax surfacing semantics (Dispatch C Summary tab)

### 6.1 Summary tab — seasonal hero card

**Surface intent:** the Summary tab opens with a seasonal_hero card highlighting THIS season's signature character. This is the player's narrative anchor for the season.

**Card content:**

| Field | Source | Notes |
|---|---|---|
| Hero name (large) | `ExportSeasonHero.season_hero_kit_name_canonical` | Phase 5 cohesion-judge LLM output; D-Sharpened uniform naming |
| Faction line | `ExportSeasonHero.season_hero_faction_label_canonical` | Cluster identity; "of the <faction>" framing |
| 1-2 sentence flavor | Composed by drax from `selection_rationale` + cluster narrative + (optional) cohesion-judge flavor text | Player-facing; substrate-grounded |
| Visual element | Drax design decision (TBD per drax seam); could be kit primary-stat icon + element glyph | Visual treatment per `reincarnated-loadout/` style |
| "View details" CTA | Drax routing | Routes player to this kit's Sample tab |

**D-Sharpened invariance (LOAD-BEARING):** the card MUST NOT display `substrate_anchored_personage_internal`. The hero's substrate anchor (if any) is engine-internal analytics. Player sees only the cohesion-judge canonical name + cluster faction context.

**Discipline #45 vocabulary lock:** the seasonal_hero card MUST NOT use "class" vocabulary. Acceptable framings:
- "Season N's signature Spirit" ✓
- "The face of Season N" ✓
- "Season Hero" ✓
- "<Hero Name>, of the <Faction Name>" ✓
- "Season N's hero class" ✗ (Discipline #45 violation)
- "The N-class champion" ✗ (Discipline #45 violation)

### 6.2 Composition with Summary tab — other surfaces

The seasonal_hero card sits ALONGSIDE (not replacing) the Path III F-C surfaces per drax Cycle 14 tab integration response:

- **primary_faction_pair narrative** (per ExportFactionRelationship.primary_pair_intensifier; Path III)
- **per-faction member listings** (per ExportFactionCluster.member_kit_ids)
- **inter-faction relationship narratives** (per ExportFactionRelationship; Path III F-C)

The seasonal_hero card is the **first surface** the player sees (top of Summary tab); other narrative surfaces compose below.

### 6.3 Cycle 15+ extension — Court of Forms accumulation

Per doc 49 § 7.2 (Sample drives narrative recognition + Court accumulation), the seasonal_hero is the canonical Spirit-archetype the Court of Forms accumulates for this season. Drax Court tab (Cycle 15+) would show the lineage of seasonal heroes across seasons — narrative continuity that the per-season seasonal_hero emission creates.

### 6.4 Star-lord telemetry consumption

Star-lord logs `season_hero_id` to telemetry for cross-season analytics:

- `season_id → season_hero_kit_id` mapping (cross-season analyst query)
- Per-season `selection_rationale` corpus (cross-season pattern detection; drift watch — same gandalf rationale phrases repeating across seasons may indicate implicit-pillar drift per Discipline #18)
- Per-season composite score distribution (substrate-metric calibration; rebalance candidate signal)

---

## 7. Discipline composition

### 7.1 Discipline #41 (substrate-led; pre-authored taxonomy interrogation) — LOAD-BEARING

The top-3 selection algorithm (§ 3) is substrate-emergent. The composite metric uses:
- Q-vector quality (substrate combat output)
- Mahalanobis distinctiveness on 8-axis BC space (substrate dimensions)
- Substrate-anchor presence (substrate-driven D-Sharpened allocation)

No pre-authored personality archetype, fixed-class roster, named-personage curation, or thematic-category filter is introduced. Gandalf's pick (§ 5) is design-judgment OVER substrate-emergent candidates — NOT pre-imposed pre-filtering.

### 7.2 Discipline #43 (design-quality audit at wave-close) — LOAD-BEARING

Gandalf's selection authority derives from Discipline #43. The selection is logged into the wave-close audit record with substrate-emergent rationale. Wave 5 audit-gate PASS is precondition.

### 7.3 Discipline #45 (vocabulary lock at player surface)

Drax MUST NOT use "class" vocabulary in the seasonal_hero card. Substrate-anchored vocabulary only.

### 7.4 D-Sharpened invariance

Substrate_anchored_personage metadata flows through Phase 4 → Phase 5 → ExportSeasonHero as engine-internal analytics ONLY. Player-facing surface uses Phase 5 cohesion-judge uniform LLM naming. This pattern matches PM-2 § 2.7 D-Sharpened invariance for ExportFactionCluster and extends it to the seasonal_hero surface.

### 7.5 Discipline #46 § 7 (per-cell bounding)

Substrate metric computation is per-season (cohort ~28-32 kits); O(N) ranking + O(N) Mahalanobis. Trivial compute. Bounded by season cohort size, not by archive-wide scan.

### 7.6 Discipline #42 (framing-audit) — applied at this dispatch

**Q1 verified:** dispatch presupposes no pre-authored taxonomy. Substrate metric is substrate-emergent.
**Q2 verified:** substrate-led discipline implies substrate produces top-3; gandalf curates within constraint.
**Q3:** no framing-refusal triggered.

---

## 8. Risks + Watch Items (per failure-modes register § 5)

### 8.1 D-2 watch — faction pre-authored taxonomy creep

**Risk:** if gandalf's selection_rationale repeatedly cites cluster/faction membership AS the reason for the pick across seasons, the selection may de facto introduce a pre-authored thematic faction-as-classification taxonomy. Drift toward "every season the most heroic-faction kit becomes hero" reimposes a pre-authored heroism taxonomy.

**Watch trigger:** star-lord cross-season telemetry — if 3+ consecutive seasons cite "faction X = season hero" or substantially similar phrasing, gandalf MUST surface the pattern at the next Wave 5 close audit and consider Pattern-B Matt design-call escalation per § 5.1 trigger (3).

**Detection:** automated cross-season `selection_rationale` lexical overlap check by star-lord telemetry; threshold > 0.5 Jaccard similarity across 3 consecutive seasons → WARN flag.

### 8.2 D-4 watch — LLM-as-oracle creep

**Risk:** if the seasonal hero selection becomes driven by `candidate_kit_name_canonical` (Phase 5 cohesion-judge output) — i.e., gandalf picks based on which LLM-generated name sounds most compelling — the substrate-led discipline weakens. The LLM becomes the de facto curator.

**Watch trigger:** gandalf selection_rationale that primarily references the cohesion-judge name ("I picked Crimson Reaver because the name is the most evocative") rather than the substrate signal breakdown. This is a Discipline #41 violation pattern.

**Mitigation:** § 5.2 audit-log format REQUIRES substrate-emergent rationale (cites which signal in composite metric drove pick, OR substrate cluster context, OR substrate anchor depth). Cohesion-judge name is FLAVOR — not RATIONALE. Wave-close audit catches drift.

### 8.3 D-? watch — narrative-coherence vs substrate-emergence tension

**Risk:** the season's narrative center (primary_faction_pair per Path III F-C; e.g., "Pyre-Knights vs Stone-Wardens central tension") may not include the substrate-metric-top kit. If gandalf consistently picks the season hero outside the primary_faction_pair narrative, the Summary tab fragments: hero card and inter-faction narrative point in different directions.

**Mitigation:** § 5.1 escalation trigger (4) — gandalf escalates to Pattern-B Matt design-call if selection would conflict with Path III narrative emphasis. Allows Matt to ratify narrative-architecture call at the rare seasons where this tension surfaces.

### 8.4 D-? watch — implicit-pillar drift in weights

**Risk:** the composite weights (w_quality=0.5, w_distinct=0.3, w_anchor=0.2) are Cycle 14 initial. If gandalf adjusts these without empirical justification, weights become an implicit pillar — encoding gandalf's drift toward whatever signal currently feels right.

**Mitigation:** weight revision requires empirical justification per Discipline #18 (substrate-led methodology). Weights MAY be revised after 3 seasons of empirical observation, with the rationale citing observed substrate signal behavior. Revision is design-judgment within #43 authority; weight changes are logged in audit-log with revision rationale.

---

## 9. Cross-references

### 9.1 Canonical docs (composes with)

- `canonical/49-loadout-sample-player-surface-design-2026-05-27.md` — player-surface architecture; Summary tab gates on this spec; § 4.3 dependency
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` — kit shape emit (chain_count + T4 candidates + supporting chain)
- `canonical/41-progression-framework-2026-05-27.md` — endgame anchor; composition framework
- `canonical/46-concentration-architecture-2026-05-27.md` — concentration discipline at kit + cluster + faction layers (seasonal_hero composes at kit layer)
- `canonical/47-damage-scaling-architecture-2026-05-27.md` — damage scaling (composes for Q-vector quality interpretation)
- `canonical/00-ground-state.md` — needs § 1 amendment (this doc registers as new CURRENT entry; cross-references doc 49 + Phase 4 + Phase 5 + drax Dispatch C)
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` — 8-axis BC space; Mahalanobis distinctiveness operates over this space

### 9.2 Operational + agent docs

- `agentic_orchestration/gandalf/notes/2026-05-27-no-classes-architectural-recommitment.md` — vocabulary lock at seasonal_hero card
- `agentic_orchestration/gandalf/notes/2026-05-27-path-1-phase-4-5-7-cycle-14-scope-expansion.md` — Phase 4 + 5 architecture
- `agentic_orchestration/gandalf/notes/2026-05-27-path-iii-faction-assembly-extension.md` — primary_faction_pair narrative composition
- `agentic_orchestration/drax/notes/2026-05-27-cycle-14-tab-integration-pattern-a-response.md` — Summary tab redesign scope; gates on this spec

### 9.3 Engine code references

- `~/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/phase4_db.py` — kit_archive DDL (Phase 4); seasonal_hero_candidates DDL added per § 4.1
- `~/Games/reincarnated-engine/src/reincarnated/export/schemas.py` — ExportFactionCluster + ExportFactionRelationship; ExportSeasonHeroCandidates + ExportSeasonHero added per § 4.2 + § 4.3

### 9.4 Discipline composition

- Discipline #41 (substrate-led) — § 3 algorithm composition; § 5.2 audit-log rationale requirement
- Discipline #42 (framing-audit at dispatch consumption) — this dispatch's framing-audit (§ 7.6)
- Discipline #43 (design-quality audit at wave-close) — § 5 gandalf selection authority; § 5.2 audit-log entry format
- Discipline #44 (framing-refusal authority) — not triggered for this spec; framing audit PASS
- Discipline #45 (vocabulary lock) — § 6.1 player-surface labels
- Discipline #46 § 7 (per-cell bounding) — § 4.1 + § 7.5 compute bounds
- Discipline #18 (substrate-led methodology) — § 8.4 weight revision discipline

---

## 10. Open items (deferred to downstream impl)

### 10.1 Phase 4 emission impl (gamora dispatch)

- [ ] `simulation/spatial_gauntlet/seasonal_hero_scorer.py` module (or co-locate)
- [ ] DDL for `seasonal_hero_candidates` table (per § 4.1)
- [ ] Computation: cohort covariance estimation + Mahalanobis distinctiveness per kit + composite score
- [ ] Top-3 selection + tiebreak per § 3.5
- [ ] Phase 4 close hook firing seasonal_hero_scorer
- [ ] MIGRATION.md entry

### 10.2 Phase 5 PM-2 amendment (star-lord dispatch)

- [ ] Pydantic schema for `ExportSeasonHeroCandidates` (per § 4.2)
- [ ] Join with `ExportFactionCluster` (cluster_id + faction_label_canonical) and cohesion-judge (kit_name_canonical)
- [ ] Emission to `exports/<season_id>/season_hero_candidates.json`
- [ ] MIGRATION.md entry

### 10.3 Wave 5 close gandalf workflow (this seam)

- [ ] Operational procedure update: gandalf OP § 4 — add seasonal_hero selection workflow per § 5
- [ ] Audit-log entry template (per § 5.2) embedded into Discipline #43 wave-close audit record format
- [ ] Pattern-B escalation criteria checklist (per § 5.1)

### 10.4 Drax Summary tab (drax Dispatch C)

- [ ] Consume `ExportSeasonHero` for Summary tab
- [ ] Seasonal hero card layout per § 6.1
- [ ] Composition with primary_faction_pair narrative + per-faction listings per § 6.2
- [ ] Discipline #45 vocabulary review of all surface strings
- [ ] D-Sharpened invariance verification — substrate_anchored_personage_internal NEVER surfaced

### 10.5 Star-lord telemetry (star-lord seam)

- [ ] Cross-season `season_hero_id` aggregation
- [ ] `selection_rationale` corpus lexical-overlap watch per § 8.1
- [ ] Composite score distribution analytics per § 6.4

### 10.6 Ground-state oracle amendment

- [ ] `canonical/00-ground-state.md` § 1 — register this spec as new CURRENT entry; cross-reference Phase 4 + 5 + drax Dispatch C dependencies

---

## 11. Sign-off

**Author:** gandalf (story-and-design steward)
**Status:** CANONICAL — load-bearing design spec for seasonal_hero surface across Phase 4 + Phase 5 + Wave 5 + drax Dispatch C + star-lord telemetry
**Authority:** Matt 2026-05-27 verbatim design call #1 ratification (H-5 hybrid pattern)
**Composition:** with doc 49 (player-surface architecture) + Path III F-C (faction-assembly extension; primary_faction_pair narrative) + Discipline #41 (substrate-led; LOAD-BEARING for top-3 selection) + Discipline #43 (design-quality audit at wave-close; LOAD-BEARING for gandalf curation authority) + Discipline #45 (vocabulary lock at player surface) + D-Sharpened invariance (substrate_anchored_personage analytics-only across emission chain)

**For:** the canonical lock of H-5 hybrid seasonal_hero design (substrate-emergent top-3 per season; gandalf design-judgment curation pick within Discipline #43 audit authority; drax Summary tab consumption with D-Sharpened invariance; star-lord telemetry for cross-season analytics + drift watch). Composes with player-experience intent (recognition + Court of Forms accumulation Cycle 15+), genre conventions (Diablo/PoE/Last Epoch seasonal-character pattern; isekai arc-protagonist pattern), substrate-led architectural commitment (no pre-authored personality taxonomy), and Cycle 14 Wave 5 close cadence (audit-gate PASS precondition).

**Signed:** gandalf (story-and-design steward)
