# Cosmograph Substrate-Trace Packet — README

**Status:** PHASES 0+2+3+4 COMPLETE — full delivery packet for drax ingestion.
**Owner:** elrond (catalogue DB + abstraction-analysis seam)
**Dispatch:** `agentic_orchestration/dispatches/2026-06-06-elrond-cosmograph-substrate-trace-extraction.md`
**Verdict (load-bearing):** `agentic_orchestration/gandalf/notes/2026-06-06-pattern-a-verdict-cosmograph-weapon-form-ratio.md`
**Authored:** elrond 2026-06-06

---

## What this packet is

The substrate-trace data that feeds the cosmograph rendered at `/forge`. The cosmograph is FORWARD-LOOKING per Option B amendment 2026-06-06 — it renders the future-engine substrate vocabulary as ALL simulated PROVISIONAL constellations. Cycle 14 named-bearer corpus (Duskweaver et al.) STAYS at `/loadout` as the empirical-current-state showcase.

---

## Deliverable manifest

| Artifact | Status | Contents |
|---|---|---|
| `primitive_registry_v0.json` | DELIVERED (Phase 0) | 570 atomic substrate primitives flat-enumerated across 17 families with per-primitive substrate_fingerprint + provenance_tag + canonical_source; phys/mag classification for weapon-form tokens. Inspectable/diagnostic JSON form. |
| `primitive_registry.parquet` | DELIVERED (Phase 4 final) | Same 570 primitives + `bdi_weight` ∈ [0.10, 1.00] populated per § 5.1 weighting + `embedding_x`, `embedding_y` from UMAP. Parquet form for drax ingestion. |
| `region_labels_v0.json` | DELIVERED (Phase 0) | BC bin labels (34 across 8 axes) + skill-tree tier labels (4) + scaling-pattern labels (4) + chain architecture labels (2). |
| `region_labels.json` | DELIVERED (Phase 4 final) | Phase 0 v0 + emergent_mechanic_family_labels populated (6 substrate-led clusters; mean purity 0.95) + methodology record. |
| `kit_constellations.parquet` | DELIVERED (Phase 4) | 1000 simulated PROVISIONAL constellations per Option B amendment; per-kit primitive_set + centroid_x/y in UMAP space + Surface B element classification. ALL rows: `is_simulated=true`, `cell_status=PROVISIONAL`, `q_scores=null`, `kit_name == kit_id` (bc_cell_NNNN_simulated placeholder per D7). |
| `flag_enum_attachments.parquet` | DELIVERED (Phase 4) | Per-kit attachment of hypothesis-flow § 4 flag families. 14-20 flags per kit (mean 15.6) drawn from § 4.1 (Target-Pattern), § 4.3 (Investment-Tier), § 4.4 (Variant-axis), § 4.5 (Coupling-architecture), § 4.6 (Substrate-signature), § 4.7 (T4 strategy), § 4.10 (Power-plane), § 4.11 (Validation-status), § 4.13 (Kit architecture), § 4.16 (Cell shape), § 4.1 (Emergent archetype). |
| `faction_overlays.json` | DELIVERED (Phase 4) | 7 emergent faction overlays via kmeans-k=7 on kit centroids in UMAP space. PROVISIONAL_PRE_LLM labels (substrate-honest until Phase 5+ LLM naming fires post-Pareto on ~30 kits per Option A iter 5 lock). Each faction carries convex-hull polygon vertices for cosmograph halo rendering. |
| `cosmograph_phase0_notes.md` | DELIVERED (Phase 0) | Framing-audit Q1-Q3 + per-family enumeration summary + Surface A substrate-coverage honesty + verdict-binding checklist. |
| `AGENT_STATE.md` | DELIVERED | Multi-session continuity state file. |

---

## Substrate-coverage honesty

### Weapon-form-token region (Surface A — per Pattern-A verdict § 2.1)

Weapon-form-token region renders **~88.84% physical / ~11.16% magical at classified-token level** (215 phys / 27 mag / 35 unclassified out of 277 tokens). Reflects substrate composition under cycle-10 source mix. Per Discipline #41 + #59, the substrate is the truth at this surface; no manufacturing.

**Substrate-enrichment workstream (queued; not blocking Phase A):** magical-implement diversity — wand / orb / focus / staff / tome / censer / grimoire — target v2 substrate-snapshot ramp toward 70/30 phys/mag at token level per verdict § 2.1.

### Kit-roster element-axis-coverage (Surface B — per Pattern-A verdict § 2.2)

Phase 2 sim-kit element selection honors Discipline #58 genre-aligned distribution. Empirical:
- **Physical-primary kits: 42.80%** (target 40-45% — PASS)
- **Caster-primary kits: 57.20%** (target 55-60% — PASS)
- **Per-caster element: 7.5%-8.9% each** (target ~7-9% — PASS)
- QDX-5 anchor 43.2/56.8 alignment achieved.

### Element-attribute coupling (Surface C — per Pattern-A verdict § 2.3)

Element-attribute coupling honored throughout sim-kit generation per `element_biases.py:28`:
- STR ← physical (kit_attribute=STR for all physical-primary kits)
- INT ← fire, water, lightning, shadow
- WIS ← earth, wind, holy
- DEX is uncoupled to canonical-7+1 elements; surfaces only via T4 ELEMENT_CONVERSION (rare in sim sample; per Architecture A asymmetry, cosmograph renders DEX with distinct visual encoding).

### Faction-overlay structure honesty (emergent finding, Phase 4)

The 7 emergent faction overlays cluster **primarily by attribute group** (STR / INT / WIS) rather than per-element identity. Reason: the BDI-weighted kit centroid in UMAP space is dominated by element-coupling + T4 capstone + chain architecture dimensions, and these correlate strongly with the kit's attribute. Per Discipline #41 substrate-led: this is the structure the substrate actually has. Per-element factional identity is expected to surface more cleanly post-Phase 5+ LLM cohesion clustering on the Pareto-reduced ~30-kit population (Option A iter 5 lock) where LLM judge can attend to sub-element-flavor + cultural-tradition + weapon-form signal that the BDI-weighted centroid currently averages over.

---

## Design-history visibility — cosmograph property

Per Pattern-A verdict § 6: the cosmograph renders design-history evolution visibly via `provenance_tag` + distinct visual encoding. Substrate has temporal layers — what was retired, what was added at B11, what was added at B13, what the v1.13 two-layer T4 architecture introduced, what Architecture A physical-opts-out-of-flavor commits to.

Provenance tags in `primitive_registry.parquet` carry this design history:

| Family | Provenance tags present |
|---|---|
| T4_strategy | `active-v1.13` (7 active) / `retired-but-preserved` (1 — DEFENSIVE_TRADEOFF; brightness_hint 0.20 → render at ~5% sample frequency in sim) |
| skill_geometry | `CORE_14` (14) / `CORE_MARGINAL_2` (2) / `B11_EXPANSION` (9) / `B13_DEFENSIVE_MOBILITY` (3) |
| sub_element_flavor | `rotating_flavor_pool_v1_2026-06-01` (100) / `architecture_A_taxonomy_sibling_v1_2026-06-01` (9 — load-bearing asymmetry) |
| investment_scaling_pattern | `investment_pattern_v1.2_load-bearing` (2) / `investment_pattern_v1.2_canonical_locked_stub` (4) |
| attribute | `primary_attribute_v1` (4) / `deferred_placeholder_v1_2026-05-24` (1 — VIT, render as faint outline) |
| race_primitive | `race_set_tolkien_s1_illustrative_schema_only` (5 — Phase A default; rotates per season) |

Drax rendering should honor these tags so the **expansion history is legible in the cosmograph** — turns the artifact from flat snapshot into journey-captured.

---

## Drax ingestion contract

This section documents how drax should read each artifact.

### `primitive_registry.parquet` — Layer 0 stars

Schema:

| Column | Type | Purpose |
|---|---|---|
| `primitive_id` | str | Unique identifier; join key |
| `primitive_family` | str | One of 17 families (see Phase 0 notes § 2 enumeration table) |
| `primitive_label` | str | Player-facing label |
| `substrate_fingerprint_json` | str (JSON) | Per-family substrate signature; parse into dict on consumption |
| `element_coupling_json` | str (JSON) | List of canonical-7+1 element ids this primitive couples to |
| `attribute_coupling_json` | str (JSON) | List of {STR, DEX, INT, WIS} this primitive couples to (VIT excluded — deferred) |
| `canonical_source` | str | Path to authoritative source doc / engine file |
| `provenance_tag` | str | Design-history layer marker (see Design-history visibility above) |
| `bdi_weight` | float | ∈ [0.10, 1.00] — drives `star_brightness = bdi_weight × normalized_visual_scale` |
| `embedding_x`, `embedding_y` | float | 2D UMAP coordinate; drax uses for star positioning |
| `visibility_at_default_zoom` | bool | True → first-class star; False → drillable zoom-in |
| `is_simulated` | bool | All False here (substrate is engine-canonical, not simulated) |
| `notes` | str | Free-form notes |

**Drax rendering rules:**
- Default zoom shows 77 first-class stars (visibility_at_default_zoom=True): 8 elements + 5 attributes + 8 T4 strategies + 28 skill geometries + 6 skill-tree positions + 4 scaling patterns + 2 chain architectures + 6 investment patterns + 5 resource models + 5 illustrative race primitives.
- Drill zoom shows additional 493 stars: 277 weapon-form tokens + 109 sub-element flavors + 71 mechanics + 14 cultural traditions + 9 historical periods + 6 registers + 7 off-hand substrates.
- Star brightness ∝ `bdi_weight`. T4 primary universal (1.00) is brightest; deferred VIT attribute (0.20) is faintest; retired DEFENSIVE_TRADEOFF (0.20) is faint-ghost.
- Provenance-tag visual encoding distinguishes design-history layers (e.g., B11_EXPANSION geometries render with a distinguishing chromatic shift from CORE_14).
- Element-coupling drives spatial-color of element stars; attribute-coupling drives second-axis chromatic encoding.

### `region_labels.json` — Lock #4 sky-neighborhoods

Schema:

```json
{
  "_meta": { "version": "1.0.0", "phase": "Phase 3 final" },
  "bc_bin_labels": {
    "source": "qd-engine-bc-axes-lock-2026-05-20 § 2",
    "total_bins": 34,
    "axes": { "axis_1_engagement_profile": [...], ... }
  },
  "skill_tree_tier_labels": { "tiers": ["T1_rotation", "T2_beta_pair", "T3_build_defining", "T4_capstone"] },
  "scaling_pattern_per_tier_labels": { ... },
  "chain_architecture_labels": { ... },
  "emergent_mechanic_family_labels": {
    "status": "POPULATED",
    "methodology": { "algorithm": "KMeans", "k": 6, ... },
    "cluster_count": 6,
    "clusters": [ { "cluster_id": 0, "label": "emergent::damage|close|high", "centroid_x": ..., ... }, ... ]
  }
}
```

**Drax rendering rules:**
- Region labels are AMBIENT NAVIGATION OVERLAYS — not first-class stars.
- BC bin labels render as labeled "sky regions" with subtle bounding-box outlines; cells contain primitives whose substrate_fingerprint maps to that BC tuple.
- Tier + scaling-pattern + chain-architecture labels render as horizontal "skill-tree-depth bands" overlaying the canvas.
- Emergent mechanic-family labels render at the centroid (centroid_x, centroid_y) of each cluster's member primitives — small text "emergent::{effect}|{range}|{tempo}" so the player sees what the substrate said about the mechanic neighborhood.

### `kit_constellations.parquet` — constellation lines + status visual encoding

Schema (key columns):

| Column | Type | Purpose |
|---|---|---|
| `kit_id` | str | bc_cell_NNNN_simulated placeholder per D7 |
| `kit_name` | str | SAME as kit_id (NO LLM-derived name per D7) |
| `kit_identity_narrative` | str | Literal: `"PROVISIONAL — engine has not yet composed this pattern."` |
| `cell_status` | str | All `"PROVISIONAL"` per Option B amendment |
| `is_simulated` | bool | All True |
| `q_scores`, `gauntlet_pass_rate`, `pareto_rank`, `archive_status` | null | All sim kits null |
| `primary_element` | str | Single primary; one of canonical-7+1 |
| `kit_attribute` | str | One of STR/DEX/INT/WIS (derived from primary element coupling) |
| `is_hybrid` | bool | True if kit has 2 primary elements |
| `surface_B_element_class` | str | "physical" or "caster" per Surface B verdict § 2.2 |
| `primitive_set_json` | str (JSON) | List of all primitive_ids this kit composes; join to primitive_registry for rendering constellation lines |
| `centroid_x`, `centroid_y` | float | BDI-weighted mean of kit's primitive embedding coordinates |

**Drax rendering rules:**
- Each kit constellation renders as a SET OF LINES connecting its constituent primitive stars. Use `primitive_set_json` to compute the spanning lines.
- Cell status PROVISIONAL → render constellation in DIM / DASHED line-style (visually distinct from a future CONFIRMED state when cycle 15+ generates real kits against the substrate).
- Kit centroid (centroid_x, centroid_y) is the constellation's "anchor point" for label placement.
- DO NOT render `kit_name` (it's just the bc_cell_NNNN_simulated placeholder); DO render `kit_identity_narrative` on hover ("PROVISIONAL — engine has not yet composed this pattern.").
- DO NOT display q-scores (all null; per § 1.2 of dispatch, cosmograph never displays q-scores).

### `flag_enum_attachments.parquet` — side-panel flag visualization

Schema:

| Column | Type | Purpose |
|---|---|---|
| `kit_id` | str | Join key to kit_constellations |
| `flag_set_json` | str (JSON) | List of flag enum strings from hypothesis-flow § 4 |
| `flag_count` | int | Count of flags attached (mean 15.6, range 14-20) |

**Drax rendering rules:**
- On kit-constellation hover or selection, drax renders the kit's flag set in a side panel grouped by flag family:
  - Substrate flags (4.6): SUBSTRATE_ELEMENT_*, SUBSTRATE_ATTRIBUTE_*, SUBSTRATE_CULTURAL_*
  - T4 flags (4.7): T4_* strategy names + T4_BUILD_DEFINING_HIGH/MEDIUM
  - Kit architecture (4.13): KIT_SINGLE_ELEMENT / KIT_HYBRID_2_ELEMENT
  - Validation (4.11): VALIDATION_PROVISIONAL (all sim kits)
  - Coupling (4.5): COUPLING_LIGHT_3_LAYER / COUPLING_MEDIUM_4_5_LAYER
  - Variant (4.4): VARIANT_PUSH / VARIANT_SPEEDFARM / VARIANT_BALANCED
  - Investment (4.3): INVESTMENT_MEDIUM (sim default)
  - Power-plane (4.10): PLANE_HOLDS_ACROSS_ALL (sim default)
  - Target-pattern (4.1): TARGET_PATTERN_BOSSING / TARGET_PATTERN_SPEEDFARMING / TARGET_PATTERN_BALANCED
  - Cell-shape (4.16): CELL_SHAPE_SPECIALIZED (sim default)
  - Emergent label (4.1): EMERGENT_LABEL_AMBIGUOUS (sim default — pending Phase 5+ LLM naming)
- For sim kits, most flags are HEURISTIC-DERIVED from primitive set; they will become EMPIRICAL-DERIVED when cycle 15+ runs real kits through math validation + gauntlet + Phase 5 cohesion judge.

### `faction_overlays.json` — constellation-grouping halos

Schema:

```json
{
  "_meta": {
    "algorithm": "kmeans_k7_on_kit_centroids_in_umap_space",
    "cluster_count": 7,
    "kit_count": 1000,
    "label_status_all": "PROVISIONAL_PRE_LLM"
  },
  "factions": [
    {
      "faction_id": "faction_emergent_NN",
      "faction_label_placeholder": "emergent::{primary}|{attr}|hyb{NN}",
      "member_count": int,
      "member_kit_ids": [...],
      "centroid": { "x": float, "y": float },
      "spread": { "std_x": float, "std_y": float },
      "polygon_convex_hull": [[x, y], ...],
      "element_distribution": { "physical": 0.5, "fire": 0.1, ... },
      "modal_primary_element": str,
      "modal_attribute": str,
      "hybrid_fraction": float,
      "label_status": "PROVISIONAL_PRE_LLM"
    },
    ...
  ]
}
```

**Drax rendering rules:**
- Each faction renders as a translucent HALO polygon around its kit centroids (use `polygon_convex_hull` vertices directly).
- Halo color encoded by modal_primary_element + modal_attribute combination.
- Faction label uses `faction_label_placeholder` until Phase 5+ LLM cohesion clustering names them; on display, prefix with "[Emergent] " so the player understands these are pre-LLM placeholders.
- Halos may overlap (factions are not strictly partitioning; kmeans partition is one valid view of the density structure).

### Lasso-resolution algorithm input contract

When the player draws a lasso on the cosmograph, drax needs to resolve the lasso polygon to a SET OF KITS. The input contract:

- **Lasso polygon** in cosmograph coordinate space (matching `centroid_x`, `centroid_y` of kit_constellations + `embedding_x`, `embedding_y` of primitive_registry).
- **Drax computes** point-in-polygon for each kit's `(centroid_x, centroid_y)`.
- **Output**: list of `kit_id` whose centroid falls inside the lasso polygon.
- **Optional**: drax may additionally include kits whose constellation spans the lasso (any constituent primitive's embedding coordinates inside polygon) — gives "kits passing through this region" semantics.

The lasso-resolution output is the input to subsequent player-side workflows (loadout-side filtering, comparison, save-as-set).

---

## Verdict bindings honored — full audit

| Verdict binding | Honored at |
|---|---|
| Surface A — weapon-form-token ~89/11 rendered honestly | Phase 0 enumeration; `_meta.weapon_form_token_substrate_honesty` block in v0 registry |
| Surface B — kit-roster element distribution 40-45/55-60 phys/caster | Phase 2 sim-kit element selection; empirical 42.80/57.20 + per-caster element 7.5-8.9% |
| Surface C — element-attribute coupling matrix rendered per element_biases.py:28 | Phase 0 element.attribute_coupling + Phase 2 kit_attribute derivation |
| T4 strategies = 8 with provenance (active-v1.13 + retired-but-preserved); DEFENSIVE_TRADEOFF brightness 0.20 | Phase 0 enumeration; Phase 2 sim sampling rate ~5% for retired entries |
| Skill geometry = 28 with provenance (CORE_14 / CORE_MARGINAL_2 / B11_EXPANSION / B13_DEFENSIVE_MOBILITY) | Phase 0 enumeration via engine VALID_GEOMETRIES ground truth |
| Attributes = 4 active + VIT deferred-placeholder (faint outline; bdi_weight 0.20) | Phase 0 enumeration + Phase 3 BDI weighting |
| Sub-element flavors = 100 rotating + 9 Architecture A asymmetry | Phase 0 enumeration + Phase 2 single-element kits draw from primary's pool only |
| Resource models = 5 with cycle13/foundation provenance | Phase 0 enumeration; Phase 2 STR-kit→stamina + INT/WIS-kit→mana with 30% flavor secondary |
| Design-history visibility via provenance tags | Phase 0 enumeration on every relevant family + rendered into final parquet |
| UMAP defaults n_neighbors=15, min_dist=0.1, n_components=2 stand | Phase 3 (cosine metric for one-hot vectors; documented choice) |
| BDI ω+τ correlation in sim kit composition | Phase 2 element-pair sampling honors ELEMENT_TAU table; element-weapon-form affinity honors BDI § 2; element-mechanic effect-category coherence honors BDI v1 patterns |
| No LLM-named identities (D7) | Phase 2 — all kit_name == kit_id; identity_narrative is fixed PROVISIONAL string |
| Plausibility QA ≥95% | Phase 2 — 100% pass rate; no regeneration needed |
| Emergent mechanic-family labels read from clustering, not pre-imposed | Phase 3 — 6 substrate-led clusters labeled by dominant (effect|range|tempo); mean purity 0.95 |
| Substrate-led discipline #41 | Throughout — no taxonomy imposition; substrate spoke at every choice |
| Framing-audit Q1-Q3 fired at Phase 0 start | Phase 0 — captured in cosmograph_phase0_notes.md § 1 |
| Substrate-coverage honesty per #59 | Phase 0 + Phase 2 — Surface A reported truthfully at 89/11; substrate-enrichment workstream queued |

---

## Cross-references

- `canonical/story/2026-06-06-atomic-substrate-registry.md` — Layer 0 + Layer 0.5 + derivation chains + Naming Layer N1-N4
- `canonical/story/2026-05-31-hypothesis-flow-pattern-library-architecture.md` — cell schema § 3 + flag enum § 4 + Phase A-E roadmap (CANONICAL)
- `canonical/story/2026-06-05-cosmograph-pivot.md` § 9 — primitive-as-star + kit-as-constellation architectural lock + Option B amendment
- `canonical/story/bdi-omega-tau-tables-v1-2026-05-22.md` — BDI ω+τ reference tables for kit-composition sampling
- `agentic_orchestration/gandalf/notes/2026-06-06-pattern-a-verdict-cosmograph-weapon-form-ratio.md` — load-bearing verdict for this work
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § 11 + § 18 + § 41 + § 42 + § 58 + § 59 — disciplines applied throughout
- `agentic_orchestration/research/scripts/cosmograph_phase0_enumerate_2026_06_06.py` — Phase 0 reproducibility
- `agentic_orchestration/research/scripts/cosmograph_phase2_3_4_2026_06_06.py` — Phase 2/3/4 reproducibility

---

## Commission close protocol

Per dispatch § 9:

1. **Acceptance criteria met** (Phase 4 § 6.3): all packet files delivered; this README documents full drax ingestion contract; AGENT_STATE.md updated.
2. **Notification** — elrond reports completion to knight-rider; knight-rider triggers gandalf for downstream drax commission authoring (per dispatch § 9.3).
3. **No push to remote** required from elrond (gandalf + drax handle push-pattern coordination).

**End of cosmograph_README.** Commission CLOSED 2026-06-06.
