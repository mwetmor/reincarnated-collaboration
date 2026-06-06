# Cosmograph Substrate-Trace Packet — README

**Status:** Phase 0 PARTIAL — primitive vocabulary enumerated; Phase 2-4 outputs pending.
**Owner:** elrond (catalogue DB + abstraction-analysis seam)
**Dispatch:** `agentic_orchestration/dispatches/2026-06-06-elrond-cosmograph-substrate-trace-extraction.md`
**Verdict (load-bearing):** `agentic_orchestration/gandalf/notes/2026-06-06-pattern-a-verdict-cosmograph-weapon-form-ratio.md`

---

## What this packet is

The substrate-trace data that feeds the cosmograph rendered at `/forge`. The cosmograph is FORWARD-LOOKING per Option B amendment 2026-06-06 — it renders the future-engine substrate vocabulary as ALL simulated PROVISIONAL constellations. Cycle 14 named-bearer corpus (Duskweaver et al.) STAYS at `/loadout` as the empirical-current-state showcase.

---

## Packet artifacts (Phase 0)

| Artifact | Status | Contents |
|---|---|---|
| `primitive_registry_v0.json` | DELIVERED | 570 atomic substrate primitives flat-enumerated across 17 families; per-primitive substrate_fingerprint + provenance_tag + canonical_source; phys/mag classification for weapon-form tokens |
| `region_labels_v0.json` | DELIVERED | BC bin labels (34 across 8 axes) + skill-tree tier labels (4) + scaling-pattern labels (4) + chain architecture labels (2); emergent mechanic-family labels DEFERRED to Phase 3 |
| `cosmograph_phase0_notes.md` | DELIVERED | Framing-audit Q1-Q3 + per-family enumeration summary + Surface A substrate-coverage honesty + verdict-binding checklist |
| `AGENT_STATE.md` | DELIVERED | Multi-session continuity state file |

## Packet artifacts (Phase 2-4 — pending)

| Artifact | Status | Description |
|---|---|---|
| `kit_constellations.parquet` | PENDING (Phase 2) | ~1000 simulated PROVISIONAL constellations per Option B amendment; element distribution honors Discipline #58 genre-aligned (40-45% physical / 55-60% caster per Pattern-A verdict § 2.2) |
| `primitive_registry.parquet` | PENDING (Phase 3 final) | Phase 0 v0 registry + embedding_x/y from UMAP + bdi_weight from BDI ω+τ priors |
| `region_labels.json` (final) | PENDING (Phase 3) | Phase 0 v0 + emergent_mechanic_family_labels populated from Phase 3 clustering |
| `flag_enum_attachments.parquet` | PENDING (Phase 4) | Per-kit attachment of hypothesis-flow § 4 flag families (17 family enums) |
| `faction_overlays.json` | PENDING (Phase 4) | ~9 faction-grouping polygon definitions per phase5_faction_clusters |

---

## Substrate-coverage honesty

### Weapon-form-token region (Surface A — per Pattern-A verdict § 2.1)

Weapon-form-token region renders **~88.84% physical / ~11.16% magical at classified-token level** (215 phys / 27 mag / 35 unclassified out of 277 tokens). Reflects substrate composition under cycle-10 source mix (museum + community game-data + Wikidata weighted toward physical-implement diversity). Per Discipline #41 + #59, the pipeline is sound; the substrate is thin on the magical-implement axis.

**Substrate-enrichment workstream (queued; not blocking Phase A):** magical-implement diversity — wand / orb / focus / staff / tome / censer / grimoire — target v2 substrate-snapshot ramp toward 70/30 phys/mag at token level. Source candidates per verdict § 2.1: PoE wand/sceptre catalogues, D2/D3/D4 caster-weapon enumerations, Lost Ark/PoE2 focus-class data, JRPG magical-implement vocabularies (FF rod/staff lineage, Tales-of franchise focus-weapon tradition).

### Kit-roster element-axis-coverage (Surface B — per Pattern-A verdict § 2.2)

The 40-45% physical / 55-60% caster genre-aligned distribution per Discipline #58 + Matt 2026-06-02 verbatim QDX-5 ratification governs at Phase 2 sim-kit element selection (NOT at the weapon-form-token layer). Empirical QDX-5 anchor: 43.2% / 56.8% PASS.

### Element-attribute coupling (Surface C — per Pattern-A verdict § 2.3)

4 attribute stars × 8 elements with the coupling matrix from `element_biases.py:28`:
- STR ← physical (1)
- INT ← fire, water, lightning, shadow (4 elements)
- WIS ← earth, wind, holy (3 elements)
- DEX ← (uncoupled to any canonical-7+1 element; cross-attribute access via T4 ELEMENT_CONVERSION)

DEX renders with distinct visual encoding (uncoupled-node asymmetry) per verdict § 2.3.

---

## Design-history visibility — cosmograph property

Per Pattern-A verdict § 6: the cosmograph renders design-history evolution visibly via provenance_tag + distinct visual encoding. Substrate has temporal layers — what was retired, what was added at B11, what was added at B13, what the v1.13 two-layer T4 architecture introduced, what Architecture A physical-opts-out-of-flavor commits to.

Provenance tags in `primitive_registry_v0.json` carry this design history:

| Family | Provenance tags present |
|---|---|
| T4_strategy | active-pre-v1.13 / **active-v1.13** / **retired-but-preserved** (DEFENSIVE_TRADEOFF brightness 0.20) |
| skill_geometry | **CORE_14** (14) / **CORE_MARGINAL_2** (2) / **B11_EXPANSION** (9) / **B13_DEFENSIVE_MOBILITY** (3) |
| sub_element_flavor | rotating_flavor_pool_v1_2026-06-01 (100) / **architecture_A_taxonomy_sibling_v1_2026-06-01** (9 — load-bearing asymmetry) |
| investment_scaling_pattern | load-bearing C14 (2) / canonical_locked_stub C15+ (4) |
| attribute | primary_attribute_v1 (4) / deferred_placeholder_v1_2026-05-24 (1 — VIT, faint outline) |
| race_primitive | race_set_tolkien_s1_illustrative_schema_only (5 — Phase A default; rotates per season) |

Drax rendering should honor these tags so the **expansion history is legible in the cosmograph** — turns the artifact from flat-snapshot into journey-captured.

---

## Drax ingestion contract — Phase 0 read paths

Drax may read `primitive_registry_v0.json` for early-prototyping of star vocabulary rendering. Phase 0 schema:

```
primitive_registry_v0.json:
  _meta:
    version, phase, total_primitives, by_family (Counter)
    weapon_form_token_substrate_honesty:
      phys_count, mag_count, unclassified_count
      phys_ratio_at_classified, phys_ratio_at_token_level_pct, mag_ratio_at_token_level_pct
      note (substrate-led discipline citation)
  primitives: [
    {
      primitive_id: str  (unique)
      primitive_family: str  (one of 17 families)
      primitive_label: str  (player-facing label)
      substrate_fingerprint: dict  (per-family: geometry-tag / tempo / range / resource-interaction / effect-category / element-coupling / etc.)
      element_coupling: list[str]
      attribute_coupling: list[str]
      canonical_source: str
      provenance_tag: str  (design-history visibility)
      bdi_weight: null  (populated Phase 3)
      embedding_x: null  (populated Phase 3 via UMAP)
      embedding_y: null  (populated Phase 3 via UMAP)
      visibility_at_default_zoom: bool
      is_simulated: false
      notes: str
    },
    ...
  ]
```

Phase 4 will deliver this as `primitive_registry.parquet` (final form) with embedding_x/y + bdi_weight populated; current JSON v0 is the inspectable/diagnostic form for in-flight Phase 0 → Phase 3 work.

---

## Cross-references

- `canonical/story/2026-06-06-atomic-substrate-registry.md` — Layer 0 + Layer 0.5 + derivation chains
- `canonical/story/2026-05-31-hypothesis-flow-pattern-library-architecture.md` — cell schema + flag enum + Phase A-E roadmap (CANONICAL)
- `canonical/story/2026-06-05-cosmograph-pivot.md` § 9 — primitive-as-star + kit-as-constellation architectural lock + Option B amendment
- `agentic_orchestration/gandalf/notes/2026-06-06-cosmograph-star-granularity-verdict.md` — Pattern A-deep verdict on star granularity
- `agentic_orchestration/gandalf/notes/2026-06-06-pattern-a-verdict-cosmograph-weapon-form-ratio.md` — load-bearing verdict for this Phase 0 work
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § 18 + § 41 + § 42 + § 58 + § 59 — disciplines applied throughout

---

**End of cosmograph_README — Phase 0 partial.** Phase 4 will issue the full delivery README upon commission close.
