# Faction Content-Shape — Emission Spec (which faction fields cross into the sim-ready bundle)

**STATUS:** DESIGN SPEC (gandalf-authored; gates star-lord's faction-writer plumbing, P2). Authorable-cold; ready for jack-ryan Gate-1 + Matt-lock.
**Date:** 2026-06-18
**Author:** gandalf (story-and-design steward)
**Purpose:** answer the P2 design question precisely — *does the sim/Godot consume factions **mechanically** or **narratively**, and which `ExportFactionCluster` / `ExportFactionRelationship` fields are sim-load-bearing (→ the bundle) vs pipeline-internal (→ telemetry only)?* Produces: (a) the mechanical-vs-narrative ruling, (b) a visibility ruling, (c) a field-by-field partition, (d) the concrete faction block shape embedded in the unified season bundle, (e) the writer contract for star-lord, (f) forward hooks + surfaced design questions.
**Scope discipline — what this is NOT:** NOT a re-design of faction generation/assembly/naming/relationships — that is `2026-05-27-path-iii-faction-assembly-extension.md` (Matt-ratified, implemented; the schema reflects it). This spec is **purely the emission shape** — the contract between produced faction data and the Godot-consumable bundle. It changes no generation code.
**Upstream authority inherited:** Path III (G-B primary-pair + F-C inter-faction relationships); the no-classes vocabulary lock (Discipline #41); D7 AI-tell discipline (already satisfied at generation — this spec emits, it does not author narrative).
**Couples to:** `canonical/story/2026-06-18-current-to-end-state-battlesim-and-pipeline.md` P2 (the blocker this clears); wind-down memo §7.2(2); engine `export/schemas.py:588/733/1174`; the live cycle-14 sidecar `reincarnated-loadout/data/cycle14-season-001-faction-clusters.json`.

---

## 0. The spec in one line

**For season-1, factions are an ORGANIZING + PRESENTATION layer, not a combat mechanic.** The bundle carries the *structural membership* + *thematic signature* + *player-facing identity* + *relationship edges* (so a future faction-aware encounter-composer is unblocked), and **drops the clustering/QA internals to telemetry** (roughly half the schema fields). Factions are **VISIBLE** in season-1 (reconciling a stale "v1 = invisible" schema default). The faction block is **embedded in the season bundle, not a sidecar** — that embedding IS the P2 unification.

---

## 1. Mechanical or narrative? — RULING: organizing + narrative for season-1; data carried for forward mechanical use

### 1.1 What the disk says (descriptive)

- **The fight model does not consume factions.** Verified: zero `faction` references in the fight-resolution layer — `spatial_engine.py`, `combatant.py`, `arena.py`, `damage_resolver.py`. Faction references live ONLY in the orchestration/verdict layer (`phase7_verdict.py`, `wave5_season_orchestrator.py`) — i.e. factions are produced + gated at season-assembly time; they never enter a fight. There is no faction-resistance, no faction-modifier, no faction-allied-AI in combat.
- **The balance apparatus does not compose faction-coherent encounters.** The gauntlet runs kits vs FIXED encounter cohorts (the SC-6 / `ENDGAME_ENCOUNTER_CATALOG` set), not vs faction-drawn groups. So for the headless balance half, factions are currently irrelevant.
- **The loadout app already consumes the presentation tier.** `FactionClusterTile.tsx` renders `faction_label_canonical` (:52), `faction_identity_narrative` (:65), `faction_thematic_tags` (:110); `Cycle14SeasonSection.tsx` reads `member_count` + `member_kit_ids`. Season-2 marquee renders per-faction group portraits. So the *identity* tier is proven load-bearing for a real consumer.

### 1.2 The ruling (forward judgment)

**Season-1 factions are the ORGANIZING FICTION of the season's content + the player-facing identity layer.** They group the season's kits into named, narrated cohorts and supply the structural + thematic data a future encounter-composer COULD use — but season-1 does **not** wire faction-driven encounter composition or relationship-driven combat. The bundle **carries the data for those forward capabilities without the spec mandating their use.**

This is the right scope, and it is genre-correct. In Diablo and PoE, the "faction" analogue (D2 act bestiaries; PoE monster packs / area rosters) is primarily an **organizing + thematic** layer — packs share an element/theme, areas have coherent rosters — and only *selectively* a mechanical one (faction-specific resists, allied-pack behaviours) layered in later. Season-1 lands the organizing+thematic layer; mechanical faction interactions (allied-pack AI, faction resist profiles, three-way antagonist encounters) are a deliberate season-N enrichment the carried data keeps open. Building faction-aware encounter composition now would be a large sim feature for zero current consumer — over-scope.

**Consequence:** the bundle must carry `member_kit_ids` (membership), `modal_bc_axis_signature` + `element_distribution` (thematic/combat signature), and the relationship `relationship_type` edges — because those three are exactly what a faction-aware encounter-composer needs. Everything that is purely clustering provenance or QA is telemetry.

---

## 2. Visibility — RULING: season-1 is faction-VISIBLE (resolve the stale default)

The schema docstring states `faction_label_canonical` is *"Null for Reincarnated v1 (faction_visibility = invisible per engine profile flag)"* (`export/schemas.py` ~:659). **This default is stale.** The live cycle-14 output carries fully-populated canonical labels ("Earthbound Chain Wardens", "Ashwind Vanguard", …), the cohesion-judge (Path III F-C) is live, and the loadout renders the identity layer. The project went faction-VISIBLE in practice.

**Ruling: season-1 emits faction identity VISIBLE.** The bundle carries `faction_label_canonical` + `faction_identity_narrative` + `faction_thematic_tags` as primary. `faction_label_placeholder` rides as the **fallback only** (used iff canonical is null — e.g. an LLM short-circuit). The consumer prefers canonical, falls back to placeholder, never shows both. This makes the bundle robust to a short-circuit without exposing the internal placeholder in the normal (visible) path.

> **Note for star-lord:** do not gate emission on the `faction_visibility` profile flag's stale default. Emit visible; derive "is this identity real?" from canonical-presence, not from the flag.

---

## 3. The field partition (the core deliverable)

### 3.1 `ExportFactionCluster` (`export/schemas.py:588`)

| Field | Tier | Bundle? | Rationale |
|---|---|---|---|
| `cluster_id` | structural | **BUNDLE** | stable per-season reference; relationship edges + membership key off it |
| `season_id` | structural | **BUNDLE** | record-portability join key (redundant inside a season file but cheap; keep) |
| `member_kit_ids` | structural | **BUNDLE** | THE membership — the load-bearing organizing datum + the encounter-composer hook |
| `member_count` | presentation | **BUNDLE** | loadout already renders it (`Cycle14SeasonSection.tsx`) |
| `modal_cultural_lineage` | presentation | **BUNDLE** | worldbuilding texture (group `worldbuilding` block) |
| `modal_tech_level` | presentation | **BUNDLE** | worldbuilding texture |
| `modal_tone` | presentation | **BUNDLE** | worldbuilding texture — **DATA-QUALITY FLAG:** cycle-14 emits `"unknown"` for tone (see §6) |
| `element_distribution` | thematic signature | **BUNDLE** | encounter-theming hook + presentation; load-bearing for forward composition |
| `modal_bc_axis_signature` | thematic/combat signature | **BUNDLE** | engagement_profile + damage_geometry — the faction's *mechanical flavour*; the single most encounter-composer-relevant field |
| `faction_label_canonical` | presentation | **BUNDLE** (primary) | THE name; loadout renders it |
| `faction_identity_narrative` | presentation | **BUNDLE** | THE flavour; loadout renders it |
| `faction_thematic_tags` | presentation | **BUNDLE** | tags; loadout renders them; also feeds the "monster-contrast" forward pipeline (schema :664) |
| `faction_label_placeholder` | fallback | **BUNDLE (fallback only)** | emit iff canonical is null; never shown alongside canonical (§2) |
| `primary_pair_flag` | presentation | **BUNDLE** (renamed `is_primary_pair_member`) | the player-facing "central tension" marker |
| `phase7_gate_status` | QA/gate | TELEMETRY | consumer derives visibility from canonical-presence, not this raw status |
| `pm1_algorithm` | clustering provenance | TELEMETRY | gmm_k4 etc. — analyst-only |
| `cluster_compactness` | clustering metric | TELEMETRY | analyst-only |
| `substrate_anchored_personages` | analytics-only | TELEMETRY | schema: *"analytics metadata only; NEVER LLM-exposed"* (:603/:669); null in cycle-14. **Forward flag:** this is the named-personage anchor — when companions/NPCs arrive season-2, revisit whether a *curated* personage surface emits (§7) |
| `cosine_similarity_max` | QA | TELEMETRY | schema: *"Logged to telemetry"* (:683) |
| `diversity_flag` | QA | TELEMETRY | schema: *"Logged to telemetry"* |
| `llm_call_id` | provenance | TELEMETRY | call traceability |
| `regeneration_fired` | provenance | TELEMETRY | call traceability |
| `gb_selection_rationale` | analyst | TELEMETRY | player sees the primary pair, not *why* it was selected; revisit only if UI wants a tooltip |
| `pairwise_distance_distribution` | analyst | TELEMETRY | schema: *"analyst convenience for histogram analysis"* (:717) |
| `provisional_pending_playtest_validation` | gate | **NEITHER — pre-emission check** | a *provisional* taxonomy must not ship to Godot; this gates **whether the bundle emits at all**, it is not a field IN it (§5) |

**The partition is roughly 14 bundle / 10 telemetry** — i.e. half the schema is clustering+QA provenance that the schema author already annotated as analytics/telemetry. The spec is mostly *formalizing the schema's own annotations* into an emission contract.

### 3.2 `ExportFactionRelationship` (`export/schemas.py:733`)

| Field | Tier | Bundle? | Rationale |
|---|---|---|---|
| `cluster_a_id` / `cluster_b_id` | structural | **BUNDLE** (as `between: [a, b]`) | the edge endpoints |
| `relationship_type` | presentation + forward hook | **BUNDLE** | the 6-enum (antagonist/rival/allied/neutral/mysterious/parallel); player-facing + the hook for future three-way / allied-pack composition |
| `tension_narrative` | presentation | **BUNDLE** | the flavour |
| `shared_history_hook` | presentation | **BUNDLE** (nullable) | optional flavour |
| `primary_pair_intensifier` | presentation | **BUNDLE** (nullable) | the richer narrative on the primary pair |
| `ai_tell_compliance_score` | QA self-assessment | TELEMETRY | D7 gate metric, not content |
| `cohesion_judge_confidence` | gate input | TELEMETRY | Phase-7 gate metric, not content |

---

## 4. The concrete bundle shape (embedded in the season bundle — this IS the P2 unification)

The faction block lives **inside** the unified season bundle (not the current loadout sidecar). This is the whole point of P2: stop dumping factions to a separate `loadout/data/*-faction-clusters.json` and embed them in the one Godot-consumable bundle.

```jsonc
"factions": {
  "clusters": [
    {
      "cluster_id": 1,
      "name": "Earthbound Chain Wardens",          // faction_label_canonical (else placeholder)
      "identity_narrative": "A medieval fellowship of ranged combatants whose strikes arc and chain…",
      "thematic_tags": ["chain-strike", "earth-dominant", "ranged-pragmatist"],
      "member_kit_ids": ["S1_endgame_bc_melee_low_spiky_str_none_s2", …],   // structural membership
      "member_count": 13,
      "element_distribution": {"earth": 0.385, "physical": 0.231, "fire": 0.154, …},
      "bc_axis_signature": {"engagement_profile": "ranged", "damage_geometry": "chain"},
      "worldbuilding": {"cultural_lineage": "fantasy_generic", "tech_level": "medieval", "tone": "unknown"},
      "is_primary_pair_member": true               // primary_pair_flag
    }
    // … 3–5 clusters per season
  ],
  "relationships": [
    {
      "between": [1, 2],                           // cluster_a_id, cluster_b_id
      "type": "rival",                             // relationship_type (6-enum)
      "tension_narrative": "…",
      "shared_history_hook": "…",                  // nullable
      "primary_pair_intensifier": "…"              // nullable (non-null on the primary pair)
    }
    // … k*(k-1)/2 edges
  ]
}
```

**Shape rules:**
- Field renames at emission for player-facing cleanliness: `faction_label_canonical`→`name`, `faction_identity_narrative`→`identity_narrative`, `faction_thematic_tags`→`thematic_tags`, `modal_bc_axis_signature`→`bc_axis_signature`, `primary_pair_flag`→`is_primary_pair_member`, the three `modal_*` worldbuilding fields → a nested `worldbuilding` object. (Drops the `modal_`/`faction_` prefixes the bundle doesn't need — internal-vocabulary leakage into a player-facing artifact is avoidable.)
- `name` resolution: `faction_label_canonical` if non-null else `faction_label_placeholder`. Never both.
- NO clustering/QA fields appear in this block (they go to the telemetry DB via the existing star-lord path).
- The bundle is the **validated** artifact: a season carrying any `provisional_pending_playtest_validation=true` cluster does NOT emit this block as canonical (§5).

---

## 5. The `provisional` gate (a pre-emission check, not a field)

`provisional_pending_playtest_validation` marks a cluster whose identity is provisional because its *input archive* is provisional (swift-closure path). The bundle is the ship-ready, Godot-consumable artifact — provisional taxonomy is design substrate, not validated truth (schema :722–730). **Ruling:** the faction-writer checks this flag at emit time; if any cluster is provisional, the writer either (a) refuses to emit a *canonical* faction block (emits a clearly-marked provisional bundle that Godot treats as preview-only), or (b) is gated upstream by the joint-gate that already governs season emission. It is **not** carried as a per-cluster field in the player-facing block. star-lord + jack-ryan choose (a) vs (b) at Gate-1; the design requirement is only that **provisional taxonomy never reaches Godot wearing canonical clothes.**

---

## 6. Data-quality flags surfaced (not blockers; for the planning pass)

- **`modal_tone = "unknown"` across all cycle-14 clusters.** Tone is one of three worldbuilding texture fields; "unknown" is a degenerate value (the modal-tone aggregation isn't resolving). The bundle should still carry the field, but this is a content-quality gap — a faction with no tone reads flatter. Route to the generation seam (tone aggregation) as a non-blocking follow-up; the emission spec carries whatever tone is produced.
- **Singletons / "Wanderers."** cycle-14 cluster 4 is a 1-member cluster that still received a faction name ("Ashfield Ember Wardens"). The loadout already distinguishes `integerClusters` vs `wandererClusters` (`Cycle14SeasonSection.tsx`). **Design question (surfaced, §7):** is a 1-member group a thin "faction" or a "Wanderer" (a form belonging to no coherent faction — thematically apt for the solo isekai descent)? The emission shape is the same either way (carry the cluster); the *framing* (faction vs Wanderer) is a loadout/Godot presentation call. Recommend a `min_faction_members` threshold (≥2 or ≥3) below which the cluster is emitted with a `wanderer: true` marker rather than as a named faction — but this is a small Matt/loadout-consistency call, not an emission blocker.

---

## 7. Forward hooks + surfaced design questions (NOT resolved here — they don't block emission)

1. **What do factions ORGANIZE — player selection, the enemy roster, or both?** The loadout uses factions to organize *selectable kits* (player-side browsing). The seasonal-journey frame also supports factions as the *enemy roster* (the player descends through rival forms — coherent with the trial-room boss gallery + Earth-meta form-library). Both readings are compatible with this emission shape (it carries the data regardless). But the answer sizes whether `member_kit_ids` becomes sim-load-bearing (enemy composition) in a later season. **A Matt design question for the systematic planning pass.**
2. **Faction-aware encounter composition (season-N).** The carried `member_kit_ids` + `bc_axis_signature` + `relationship_type` are exactly the inputs a composer would need to build faction-coherent packs, allied-pack encounters, or three-way antagonist fights. The bundle keeps this door open; building it is a future sim feature.
3. **Personage anchors → named NPCs (season-2).** `substrate_anchored_personages` (telemetry-only here) is the named-personage hook. When the companion/NPC layer activates season-2, revisit whether a *curated* personage surface emits to the bundle — it composes with the companion-difficulty work (`2026-06-18-companion-difficulty-inversion-…`).
4. **`relationship_type` → combat hook.** Today the 6-enum is narrative. A future season could map `antagonist`→three-way encounters, `allied`→mixed packs, etc. Carried, not wired.

---

## 8. Writer contract (what star-lord builds for P2)

- **Input:** the produced `list[ExportFactionCluster]` + `list[ExportFactionRelationship]` (Path III output; present in the schema, generated at Phase 5 — currently discarded to the loadout sidecar).
- **Output:** the `"factions"` block (§4) embedded in the unified season bundle.
- **Transform:** project each cluster/relationship to the bundle tier per §3 (drop telemetry fields; rename per §4; resolve `name` per §2; nest `worldbuilding`).
- **Telemetry-tier fields:** routed to the telemetry DB via star-lord's existing path (NOT dropped — they remain available to analysts; they just leave the bundle).
- **Pre-emission gate:** the `provisional` check per §5.
- **No generation change:** this is pure emission plumbing. If embedding factions in the bundle changes a cross-seam contract (the bundle shape Godot/loadout reads), that is an ADR-004 `MIGRATION.md` + a round-trip smoke (bundle → loader field-presence) — star-lord assesses at Gate-1 (Principle 6).
- **Sidecar retirement:** once the embedded block lands and the loadout reads it from the bundle, the standalone `*-faction-clusters.json` sidecar is retired (the de-duplication is the P2 win). Sequence the loadout cutover with drax so the app doesn't lose its faction render mid-flight.

---

## 9. Discipline composition

- **D7 (AI-tell):** inherited-satisfied. Faction names/narratives/relationships are produced as structured LLM output with narrow blanks (Path III §3.6); this spec EMITS them, it authors no narrative. No D7 re-opening.
- **#41 / #45 (no-classes / vocabulary lock):** preserved — the bundle uses faction/kit vocabulary; `relationship_type` values stay the emergent 6-enum, not a pre-authored taxonomy.
- **Substrate-led:** the partition keeps substrate-derived signal (element_distribution, bc_axis_signature, membership) in the bundle and removes only the *clustering mechanism's* provenance — substrate truth in, algorithm exhaust out.
- **#11 (empirical inspection):** the partition was drawn against the LIVE cycle-14 sidecar + the schema's own field annotations, not from assumption.
- **Principle 6 (cross-seam contract):** flagged for star-lord (the bundle-shape change is the contract surface).

---

## 10. What this unblocks

- **P2 (faction writer)** — star-lord can build the writer directly off §3 + §4 + §8. No further gandalf design input needed for the writer itself.
- **P1 (unified driver)** — the faction block is one of the legs the unified driver assembles; this defines that leg.
- **Sidecar de-duplication** — retires the standalone faction sidecar (the loadout reads factions from the one bundle).

---

**Signed:** gandalf, 2026-06-18. Factions are the season's organizing fiction and its player-facing identity — not (yet) a combat mechanic. Carry the membership, the signature, and the relationship edges so the mechanical door stays open; send the clustering exhaust to telemetry; embed the block in the one bundle Godot reads. The schema already told us which fields are content and which are analytics — this spec just makes the engine honour its own annotations. Ready for Gate-1 + Matt-lock.
