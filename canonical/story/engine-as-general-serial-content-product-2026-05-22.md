# Engine as General Serial-Content Product — Strategic Reframe + Variant C Architecture

> **STATUS:** CURRENT (load-bearing as of 2026-05-23) — see `canonical/00-ground-state.md`

**Date:** 2026-05-22 (evening session, post-P0-close)
**Author:** gandalf (story-and-design steward; senior designer)
**Authority:** Matt 2026-05-22 (this session) — explicit strategic reframe: "the engine's use cases have grown far beyond reincarnated-game, and we need to expand the capability of the engine to produce coherence and distinctness for serial content production. We can then add flags/gates to produce the reincarnated-game variant."
**Status:** v1 canonical lock — strategic reframe + Variant C scope adopted; per-profile overlay architecture committed; engine-flag vs profile-overlay-flag separation locked. Implementation specifics carry forward into companion canonical docs (forthcoming tomorrow morning: legacy-categorical-cleanup-audit, stat-derivation-from-bc-convergence, gear-heavy-promotion).

---

## 0. TL;DR

The QD-engine rebuild's value extends beyond shipping Reincarnated Phase 0. The engine is a **general serial-content production system** capable of producing coherent + distinct content across multiple downstream use cases. Reincarnated is one of those use cases — specifically Profile A in the protocol § 6.7 profile architecture that was always part of the canonical commitment.

This is a strategic clarification, not a pivot. The QD-engine has always been general; Reincarnated is one profile of four (Profile A Reincarnated + Profile B B2B SaaS + Profile C mod-pack + Profile D solo-dev). What changes today: profile work moves from "spec-only deferred" to "first-class product surface from launch."

**Three architectural pillars locked under this reframe:**

1. **Variant C engine scope.** The full multi-aesthetic substrate + faction-coalescence + monster-contrast + pairing algorithm pipeline becomes a *general engine capability*, not a Reincarnated-specific add. Substrate-as-cohesion architectural commitment is preserved and strengthened.

2. **Engine-flag vs profile-overlay-flag separation.** General engine reads engine-flags (per-profile configuration); profile overlays add profile-specific flags. Reincarnated's distinctive properties (Earth Self meta-layer; spirit-form library accumulation; reincarnation framing; seasonal-journey narrative structure) live in the Reincarnated profile overlay, not in the general engine.

3. **Pre-convergence substrate vs post-convergence overlay architecture.** What enters the gauntlet sim convergence loop (element substrate + mechanical BC axes + weapon substrate with aesthetic tuples) is mechanically load-bearing. What gets themed after convergence (armor; monster contrast; visual coordinate; element-derived VFX) is aesthetic-only overlay. This category distinction sharpens substrate-as-cohesion's "only mechanically-bearing properties enter convergence" principle.

The strategic risk worth naming: over-generalizing the engine could dilute Reincarnated's distinctive feel. The mitigation: **the Reincarnated profile overlay must be substantive design work, not configuration defaults.** Earth Self framing + spirit-form library + reincarnation narrative structure are authored design, not YAML.

---

## 1. Strategic context — why this reframe, what changed

### 1.1 What was already canonical

The QD-engine rebuild architecture committed to multi-profile output from the beginning:

| Profile | Use case | Per protocol § 6.7 (committed v1.3) |
|---|---|---|
| **A** | Reincarnated Phase 0 ship | Full integration in v1; player-facing demo |
| **B** | B2B SaaS | Spec-only in v1; API surface defined |
| **C** | Mod-pack exporter | Spec-only in v1 |
| **D** | Solo-dev tooling | Spec-only in v1 |

The 8 BC axes + MAP-Elites archive + substrate-as-cohesion commitment + LUCB1 theme-discovery + joint-gate (mechanical + cohesion + visual) — every architectural component is profile-agnostic engine machinery. Profiles operate as output filters + integration paths.

### 1.2 What Matt clarified today

Matt's 2026-05-22 reframe: "the engine's use cases have grown far beyond reincarnated-game ... expand the capability of the engine ... then add flags/gates to produce the reincarnated-game variant."

**Operationally this means:**
- Profile B/C/D move from "spec-only deferred" to "first-class product surface from launch"
- The general engine capability (substrate × convergence × archive × joint-gate × profiles) is the canonical product
- Reincarnated profile is one demonstration of that capability, not the singular target

### 1.3 Why this is clarification, not pivot

The original protocol's profile structure (committed v1.3 § 6.7) anticipated this exact shape. The reframe makes explicit what was always implicit: **the engine's value is general; profiles are how that value reaches specific consumers.** No architectural commitment is being reversed. Phase commitments (P0-P7) are unchanged in structure. The protocol amendments needed are scoping (P6 work substantively in v1) and naming (LITE→HEAVY for gear-substrate), not architectural reversal.

This connects to substrate-as-cohesion's deepest commitment: identity should emerge from substrate-agnostic generation. A general engine that produces "coherent + distinct content" without pre-imposing identity is the architectural form of that commitment.

---

## 2. Variant C engine architecture — pre-convergence substrate vs post-convergence overlay

### 2.1 The category distinction (Matt's framing)

Per the 2026-05-22 evening conversation, the architectural cleanup that distinguishes engine-level from profile-level is:

| Layer | What lives here | Examples | Why |
|---|---|---|---|
| **Pre-convergence substrate (enters balance sim)** | Element substrate; mechanical BC axes; weapons (with aesthetic tuples) | fire/water/etc.; range × geometry × timing × charge × accuracy × rhythm; weapon library with mechanical+aesthetic properties | These have mechanical properties that drive convergence; they participate in the gauntlet sim |
| **Post-convergence overlay (themed after kit cements)** | Armor; monster contrast; visual coordinate (Meshy rendering); element-derived VFX | armor pieces; faction-derived monster themes; per-kit Meshy character generation; flames/lightning/holy-glow effects | These don't affect mechanical convergence; they apply faction/archetype/season identity to an already-cemented kit |

**Decision criterion for any new feature:** does this thing have mechanical effects that should drive balance convergence, OR does it follow from the kit's already-determined identity? First category enters convergence; second category is post-convergence overlay.

This sharpens substrate-as-cohesion's "only mechanically-bearing properties enter convergence" principle. Aesthetic identity that doesn't drive mechanics (armor visual tier; monster cultural-coding; VFX color/style) lives downstream of the convergence loop, not as substrate input.

### 2.2 Engine-level multi-aesthetic substrate architecture

Under Variant C scope, the engine commits to:

| Engine capability | What it does |
|---|---|
| **Weapon substrate with aesthetic tuples** | Each weapon in the library carries `(tech_level, tone, cultural_lineage)` aesthetic tuple + mechanical properties (range, geometry, timing, charge, etc.). Weapon selection during balance sim convergence tags the hero with the aesthetic the selected weapons collectively express. |
| **Substrate-agnostic generation** | Kit generation is element + BC-mechanical-signature driven; no archetype categorical pre-imposition; no role_orientation tag input; stats are derived projection of convergence state (per forthcoming `stat-derivation-from-bc-convergence` canonical doc) |
| **Faction-coalescence on clustered kits** | Multimodal clustering identifies natural groupings in the cemented kit population; faction labels are post-hoc cluster identities, not generation inputs. Optional surface for player-facing display per profile flag. |
| **Monster contrast pipeline (P5b)** | Post-faction-coalescence stage that designs monster rosters contrastively against emerged factions (shadow-self, incomprehensible-ancient, playful-mocker, primitive-tribal, existential-threat vocabulary) |
| **Pairing algorithm (P6/P7 boundary)** | Season-launch faction-configuration selector (unified / disjoint / mixed-triangulated); takes season-brief inputs and selects opening configurations |
| **Density-routed asset pipeline** | Substrate-vector queries against the weapon library; high-density regions resolve from imported assets; sparse regions route to Meshy gap-fill; the density map evolves as catalogue grows |

All six are general-engine commitments under Variant C, not Reincarnated-profile-specific.

### 2.3 What enters the gauntlet sim under this architecture

```
GAUNTLET SIM (mechanical convergence):
  Element substrate (fire/water/earth/wind/lightning/holy/shadow)
    × Mechanical BC axes (range/mobility, geometry, proxy density, control,
                          damage tempo, amplitude variance, defense, resource)
    × Weapon substrate (queried from library; carries aesthetic tuple + sim properties)
    × Skill substrate (substrate-agnostic per W0.2)
  → Kit converges to mechanical signature + element scaling
  → Stats are derived projection (element_scaling_attribute × per-axis magnitude)

POST-CONVERGENCE COHESION JUDGING:
  Cohesion-judge reads converged kit + weapon aesthetic tuples
  → Assigns thematic identity (canonical Reincarnated spirit names / faction labels)

CLUSTERING:
  Multi-distribution clustering of cemented kits
  → Multimodal cohesive clusters emerge

POST-CLUSTERING OVERLAY:
  Faction-coalescence (assign cluster identities)
  Monster-contrast pipeline (per faction)
  Armor visual application (per faction/archetype identity; baked)
  Visual coordinate (Meshy generation w/ aesthetic tuple input)
  VFX layer (element-derived effects added at Unity assembly)

PROFILE ASSEMBLY:
  Pairing algorithm (per season-brief)
  Per-profile filtering + output formatting
```

The engine never reasons about aesthetic identity during convergence; aesthetic emerges from weapon selection + cluster identity + profile overlay.

---

## 3. Engine-flag vs profile-overlay-flag architecture

### 3.1 The separation

The general engine reads **engine-level flags** that configure its behavior across profiles. Each profile then adds **overlay flags** that add profile-specific features.

This separation is what lets Reincarnated be Reincarnated while the engine stays general.

### 3.2 Engine-level flags (proposed)

| Flag | Values | What it controls |
|---|---|---|
| `cultural_lineage_register` | List of `(tech_level × tone × cultural_lineage)` tuples enabled | Which aesthetic substrates the engine considers during convergence + clustering |
| `faction_count_target_per_season` | Integer (default 3-5) | Drives cluster-spread tuning; clustering targets this faction count and adjusts spread to hit target |
| `faction_visibility` | `visible` / `invisible` | Whether faction labels surface to the player; Reincarnated = `invisible` (clusters emerge but aren't shown as factions); other profiles may = `visible` |
| `pairing_mode` | `unified` / `disjoint` / `mixed_triangulated` | Season-launch faction configuration selector |
| `monster_contrast_vocabulary` | Subset of `{shadow-self, incomprehensible-ancient, playful-mocker, primitive-tribal, existential-threat}` | Which contrast types are valid for this profile |
| `style_register_lock` | Reference to canonical style register; or `null` for profile-custom | Per-profile visual register |
| `gear_armor_decoupling` | `baked` / `decoupled` | Default baked (one mesh per spirit); profiles needing equip-swap set `decoupled` to also emit per-tier-per-slot armor assets (per legolas Unity catalogue findings) |
| `tier_hierarchy_depth` | Integer (default 1 for v1; 3 for D2-style v1.1+) | Number of tier variants per gear/armor; v1 ships with 1 tier (no within-spirit progression) |
| `aesthetic_tuple_resolution_mode` | `dominant_weapon` / `weighted_aggregation` / `disjoint_allowed` | How multi-weapon kits resolve their aesthetic-tuple at the kit level (Q1 design call) |
| `player_faction_choice` | `engine_assigns` / `player_selects` | Whether players pre-commit to faction at character creation (standard ARPG) or get assigned via emergence (Reincarnated) |

### 3.3 Profile-overlay flags (Reincarnated; proposed)

| Flag | Values | What it controls |
|---|---|---|
| `earth_self_meta_layer_enabled` | `true` (Reincarnated) / `false` | Whether the player has a persistent meta-identity above factions; spirit-form library accumulates across seasons |
| `spirit_form_library_persistence` | `true` / `false` | Whether cemented kits persist into the player's accumulator across seasons |
| `seasonal_journey_narrative_structure` | `seasonal-cycle` (Reincarnated) / `campaign` / `episodic` / `null` | How seasons relate to each other narratively |
| `reincarnation_framing` | `true` (Reincarnated) / `false` | Whether kits are framed as "past lives" / "spirit-forms" in player-facing surfaces |
| `spirit_swap_mechanic_enabled` | `true` (Reincarnated; load-bearing differentiator) / `false` | In-season spirit-form swapping mechanic |
| `monster_contrast_per_spirit` | `true` (Reincarnated) / `false` | Whether monster contrast is per-spirit-context (Reincarnated, since player swaps spirits) or per-season (default) |

### 3.4 Reincarnated profile flag configuration (locked v1)

```
# Reincarnated Profile A — flag configuration v1
ENGINE FLAGS:
  cultural_lineage_register = [medieval × {heroic, grim, mystical} × {European, East-Asian, South-Asian},
                                primitive × {heroic, mystical} × {African, fictional-hybrid},
                                medieval × grim × fictional-hybrid]
                              # Sci-fi / post-singularity registers deferred to v1.1+
  faction_count_target_per_season = 3-5 (adaptive)
  faction_visibility = invisible          # multimodal clusters emerge; player sees variety, not factions
  pairing_mode = mixed_triangulated       # Reincarnated wants narrative tension at season launch
  monster_contrast_vocabulary = {shadow-self, incomprehensible-ancient, existential-threat}
                              # Reincarnated leans dark + cosmic; mocker/primitive sparingly used
  style_register_lock = canonical/story/style-register.md (HD-2D Octopath-coded)
  gear_armor_decoupling = baked           # v1; decoupled comes back with v1.1+ loot system
  tier_hierarchy_depth = 1                # v1; D2-style 3-tier expansion is v1.1+
  aesthetic_tuple_resolution_mode = disjoint_allowed   # mixed-aesthetic spirits become first-class library entries
  player_faction_choice = engine_assigns  # Reincarnated forecloses faction-pick by design

REINCARNATED OVERLAY FLAGS:
  earth_self_meta_layer_enabled = true
  spirit_form_library_persistence = true
  seasonal_journey_narrative_structure = seasonal-cycle
  reincarnation_framing = true
  spirit_swap_mechanic_enabled = true     # load-bearing differentiator
  monster_contrast_per_spirit = true      # spirit-context-driven, not season-fixed
```

Other profiles (B/C/D) carry different flag configurations; specified per profile when those profiles become substantive (P6 work).

---

## 4. Reincarnated profile overlay — the distinctive design surface

### 4.1 What makes Reincarnated distinctive

Under the engine-as-general-product framing, the question becomes: **what makes Reincarnated *not* feel like a generic ARPG output of the engine?** The answer is the overlay — and the overlay must be substantive design work, not configuration defaults.

The Reincarnated overlay carries:

1. **Earth Self meta-layer.** The player is the cosmological collector who has lived across many forms in many cultures across many lives. Each spirit-form in the library is a past life manifested. Earth Self is the persistent player identity that owns the library across seasons.

2. **Spirit-form library accumulation.** Cemented kits persist across seasons. The library grows in count and variety; this is the dominant progression surface (horizontal-collection-progression, not vertical-tier-progression).

3. **Reincarnation framing.** Each spirit-form has a story — where it lived, what it became, how it ended. The canonical Canary of the Drowned Seam exemplifies this: a fire-mage in a flooded coal mine, soot-stained robes with canary-yellow trim, the canary as companion-warning, the mine as the spirit's gauntlet.

4. **Seasonal-journey narrative structure.** Each season is one chapter of the Earth Self's accumulating reincarnation arc. Trial-room boss-gallery framing; spirit-emergence-from-trial as the season's core beat; the form library grows by one or more spirits per season.

5. **Invisible factions, visible diversity.** Multimodal clustering produces aesthetically + mechanically coherent groups. The player experiences variety in the library (industrial-grim spirit next to ancient-Asian-mystical spirit next to medieval-heroic spirit), but no "faction" label is surfaced. The collection IS the world; faction-as-concept stays in the engine's invisible scaffolding.

6. **Spirit-swap as the differentiating mechanic.** In-season, the player swaps among accumulated spirits; the active spirit's mechanical signature + visual identity + companion + element-VFX changes. Spirit-swap operates on the library; the library is the player's expressive surface.

### 4.2 Pipeline overlay implications

**Asset pipeline per profile-A spec (forthcoming `asset-pipeline-meshy-swap-2026-05-22.md` finalization):**

- Source images: T-pose body + outfit + rigid accessories only; NO companions in source; NO element-derived VFX in source (per galadriel § 8 canonical lesson)
- Unity layer: companions parented to shoulder bone via Animation Rigging; element VFX added per spirit's converged element substrate; flowing cloth via Unity Cloth; spirit-guide manifestations as separate-root entities
- Armor: baked into character mesh; one tier per spirit per aesthetic tuple; no runtime equip-swap
- Asset sources: Asset Store Tier 1 ($140-180; medieval-European register; per legolas Unity catalogue findings) + Meshy gap-fill for non-Asset-Store-covered aesthetic regions (per legolas Meshy pipeline findings)

**Catalogue strategy under vast-library framing (per just-fired legolas commission):**

- Gear-substrate populates from imported vast library (loadout DB `/Users/admin/Games/reincarnated-loadout/data/telemetry.db`; empty greenfield 2026-05-22)
- Substrate-vector queries return candidate weapon sets from library
- Density-routing: empty regions route to Meshy gap-fill
- 15-gear catalogue (current `gear-substrate-rule-table-v1-2026-05-22.md`) likely emerges as natural clusters in imported library data rather than being pre-imposed

### 4.3 v1 aesthetic register commitment (medieval-spanning)

Per legolas Unity catalogue findings + Q1 aesthetic-tuple matrix proposal (pending Matt confirmation):

| Tech level | v1 coverage |
|---|---|
| Primitive | Secondary tuples on warhammer, caster-staff (shaman), war-horn (tribal) |
| Medieval | **Dominant** — 13 of 15 gear catalogue primaries |
| Industrial | Limited (blunderbuss; crossbow Van Helsing era) |
| Advanced/sci-fi | **Deferred to v1.1+** (catalogue expansion + Meshy gap-fill) |
| Post-singularity | **Deferred to v1.1+** |

| Cultural lineage | v1 coverage |
|---|---|
| European | Dominant (11 of 15 primaries) |
| East-Asian | Strong (multiple primaries + secondaries) |
| South-Asian | Limited (chakram primary; censer secondary) |
| Mesoamerican | Minimal (secondary only) |
| African | Minimal (secondary only) |
| Fictional-hybrid | Limited (twin-daggers rogue primary) |

**v1 is multi-aesthetic but medieval-spanning. Sci-fi + post-singularity gear catalogue expansion lands in v1.1+ alongside G-PROMOTE-v1.1 full gear-substrate promotion.**

---

## 5. Other profile overlays (B/C/D) — sketches

### 5.1 Profile B (B2B SaaS)

Customer-curated archive subsets; per-customer BC weighting + joint-gate; customer-deliverable season packs; API surface specification.

**Distinctive flag-points (proposed):**
- `player_faction_choice = player_selects` (standard ARPG; most B2B customers want pre-commit-faction shape)
- `faction_visibility = visible` (factions surfaced to player; standard ARPG framing)
- `cultural_lineage_register` per customer specification (some want medieval-only; some want sci-fi; some want full multi-aesthetic)
- `tier_hierarchy_depth = 3` (D2-style; matches mainstream ARPG expectation)
- `gear_armor_decoupling = decoupled` (runtime equip-swap; loot system)
- Reincarnated overlay flags all `false` / `null`

Profile B specifies real customer integration paths in v1 (not just spec-only); actual customer onboarding follows v1.1+.

### 5.2 Profile C (mod-pack exporter)

Target-game/genre customization parameters; customer-genre-aligned BC subsets; mod-pack deliverables.

**Distinctive flag-points:**
- Per-target-game flag configuration (D2-style; PoE-style; Last-Epoch-style)
- `cultural_lineage_register` set to target game's canon
- Export format matches target game's mod system

### 5.3 Profile D (solo-dev tooling)

Solo-developer customization interface; per-dev BC subset preferences; dev-friendly artifact bundles.

**Distinctive flag-points:**
- Maximum flag flexibility (every flag exposed; dev tunes for project)
- Lightweight integration paths (CLI tooling; JSON exports)

---

## 6. Empirical validation — substrate-as-cohesion at multi-genre scale

### 6.1 The validation gate sharpens under Variant C

Per protocol § 6.6.1 v1.2 epistemic correction (Matt 2026-05-21 catch): P5 is the first empirical test of substrate-as-cohesion. Under Variant C with multi-aesthetic substrate, P5 validation is sharpened into a **two-stage gate**:

| Stage | Test | Pass criterion |
|---|---|---|
| **Stage 1 — single-aesthetic cohesion judging** | Substrate-agnostic kits prompted through cohesion-judge produce coherent thematic identity (current planned P5 W5.2 work) | Cohesion-judge identifies recognizable thematic identities; score ≥ threshold per Discipline #17 calibration |
| **Stage 2 — multi-aesthetic cohesion judging** | Same substrate signature with different weapon-aesthetic tuples produces correctly-different thematic identities (Reincarnated-coherent for one tuple; sci-fi-coherent for another) | Cohesion-judge distinguishes thematic identity per aesthetic tuple; cross-tuple variance is meaningful |

**If Stage 1 passes but Stage 2 fails:** multi-aesthetic deferred; v1 ships medieval-spanning only; sci-fi/etc. catalogue work waits on cohesion-judge architecture sharpening.

**If both pass:** Variant C is empirically validated; v1.1+ expansion proceeds.

### 6.2 Pre-P5 probe recommendation

Run a pre-P5 cheap multi-genre probe (similar to the substrate-as-cohesion probe at 4.35 supportive that legolas executed 2026-05-21) but explicitly testing multi-aesthetic. If Stage 2 fails pre-P5, the architecture risk surfaces before committing P5 implementation cycles. Cost: ~1 day of legolas probe work.

This is now a **mandatory pre-P5 gate** under Variant C, not nice-to-have.

---

## 7. What's deferred to v1.1+

Under Variant C v1 scope, the following are explicitly v1.1+ work:

| Item | Reason |
|---|---|
| **G3-LITE** — gear-instance generation constrained by archetype | Deferred to v1.1+; v1 uses density-routed library queries |
| **G7-LITE** — 4-substrate empirical validation gate | Deferred; v1 ships 3-substrate empirical test (substrate-as-cohesion); 4-substrate (with gear) lands at G-PROMOTE-v1.1 |
| **G-PROMOTE-v1.1** — full gear-substrate generative promotion | v1.1+; v1 ships derived-tag-plus-tier-hierarchy gear |
| **Equippable armor decoupling** | v1 ships baked-armor only; decoupled mode comes with v1.1+ loot system |
| **Sci-fi gear catalogue expansion** | Asset Store coverage is zero; full Meshy gap-fill required; deferred to v1.1+ catalogue work |
| **Tier hierarchy depth > 1** | v1 ships one tier; D2-style 3-tier (or finer) expands in v1.1+ |
| **Pet system mechanical detail** | Form library accumulation lands; richer pet mechanics (loot pickup, combat assistance) deferred |
| **Profile B/C/D actual customer integration** | v1 ships specs; integration follows v1.1+ |
| **Cross-season faction continuity** | v1 ships per-season faction emergence; cross-season faction persistence deferred |

---

## 8. The risk worth naming honestly

**Over-generalizing the engine could dilute Reincarnated's distinctive feel.** The same architecture serving D&D module generation + B2B customer rosters + Reincarnated tends toward *generic competence* — the engine gets good at "produce coherent thematic identity" in the abstract, which can land as "produce thematic identity that doesn't feel rooted in any particular cultural-creative voice." Solo Leveling is what it is because Chugong's voice + Korean cultural register pervade it. Generic engines don't have voices.

**The mitigation:** the Reincarnated profile overlay (Earth Self framing + spirit-form library + seasonal-journey + locked style register + curated cultural-lineage choices + Matt's authorial voice) is what gives Reincarnated its distinctive voice. As long as that overlay is real, distinctive, and curated — not just configuration defaults — Reincarnated stays Reincarnated.

**Design discipline this commits to:** Reincarnated's profile overlay is design work, not configuration work. It needs gandalf + Matt design-call cycles, woven into P1-P7. Earth Self mechanical detail + spirit-form library rules + reincarnation narrative structure + per-spirit narrative authoring + canonical visual register curation all land as substantive v1 deliverables.

If overlay design work doesn't get the bandwidth, Variant C dies — engine ships generic; Reincarnated profile is thin.

---

## 9. Open questions (carry-forward to subsequent canonical authoring)

| # | Question | Resolution path |
|---|---|---|
| Q1 | Aesthetic-tuple matrix per gear catalogue entry | Matt confirmation of gandalf-proposed primary + secondary tuples (15 entries); locked tomorrow morning |
| Q2 | Stat-derivation per BC-axis mapping | `canonical/story/stat-derivation-from-bc-convergence-2026-05-22.md` authoring tomorrow morning |
| Q3 | Multi-weapon kit aesthetic-tuple resolution mode | Lean: `disjoint_allowed` for Reincarnated; player choice for other profiles |
| Q4 | Viable-tuple space restriction (full Cartesian 120-tuple vs. canonical-only ~30-50) | Resolution depends on legolas weapon library findings (Tuesday/Wednesday return) |
| Q5 | Cross-season faction continuity | Deferred to v1.1+ |
| Q6 | Tier hierarchy re-introduction threshold for v1.1+ | Deferred; gameplay feedback informs |
| Q7 | Trait system role under stat-BC-derivation framework | Traits may exist as optional identity modulators v1.1+; not load-bearing for stats; revisited post-v1 ship |

---

## 10. Implementation phasing under this reframe

The P0-P7 critical path is **unchanged in structure** under Variant C. What changes is scope per phase:

| Phase | Variant C scope addition |
|---|---|
| P1 substrate enrichment | Add: G1 gear-substrate rule-table + W1.15 derivation + vast library import + selection-pattern infrastructure |
| P2 BC measurement | Unchanged (mechanically agnostic to aesthetic substrate) |
| P3 archive | Unchanged (multimodal clustering already on path) |
| P4 sim extensions | Unchanged (mechanical extensions; aesthetic-agnostic) |
| P5 cohesion + visual BC | Add: faction-coalescence stage; monster-contrast pipeline (P5b); multi-aesthetic cohesion-judge validation (Stage 2) |
| P6 profile assembly | Add: substantive Profile A overlay implementation; pairing algorithm; Profile B/C/D spec authoring |
| P7 validation + cutover | Add: per-profile validation gauntlets; reference-build certification across aesthetic registers |

Per phase, the effort estimate grows ~30-50% over the pre-reframe baseline. Total v1 timeline expands ~5-7 weeks. Reincarnated overlay design work + legolas vast-library import + multi-aesthetic cohesion-judge prompt authoring are the three biggest scope expansions.

---

## 11. Cross-references

### 11.1 Canonical foundation
- `canonical/story/hive-mind-protocol-qd-engine-rebuild-2026-05-21.md` v1.3 — protocol; § 6.7 profiles A/B/C/D; § 6.6.1 P5 empirical-validation framing
- `canonical/story/historical/engine-architecture-vision-qd-profile-2026-05-19.md` § 4 — profile architecture original commitment
- `canonical/story/qd-engine-end-to-end-workflow-2026-05-21.md` — touchpoint architecture across phases
- `canonical/story/substrate-design-supplement-2026-05-21.md` — substrate-as-cohesion architectural commitment

### 11.2 This session's canonical work
- `canonical/story/asset-pipeline-meshy-swap-2026-05-22.md` — Profile A asset pipeline (skeleton; finalization pending legolas vast-library findings)
- `canonical/story/gear-substrate-rule-table-v1-2026-05-22.md` — gear-substrate rule-table (surface-cleaned; full restructure to 21-vector v1 + library-emergent-clusters pending)
- `canonical/story/bdi-omega-tau-tables-v1-2026-05-22.md` — BDI ω/τ formalism (pending recalibration under role_orientation drop + stat-BC-derivation reframe)
- `canonical/story/tier-4-architecture-defaults-2026-05-22.md` — T4 keystone architecture defaults

### 11.3 Forthcoming canonical work (tomorrow morning)
- `canonical/story/legacy-categorical-cleanup-audit-2026-05-22.md` — vestigial-pattern audit + per-surface cleanup checklist (covers archetype + role_orientation + "traits carry stats" + stat_distribution_signature input + reference-archetypes naming)
- `canonical/story/stat-derivation-from-bc-convergence-2026-05-22.md` — BC-axis-derived stats canonical replacement for trait-based stat assignment
- `canonical/story/gear-heavy-promotion-2026-05-22.md` — LITE→HEAVY rename + tier-hierarchy + WR-bracket sequencing

### 11.4 In-flight research
- `agentic_orchestration/dispatches/2026-05-22-legolas-weapon-library-import-discovery.md` — legolas commission running (~3 days; returns Tuesday/Wednesday); will inform gear-heavy-promotion + asset-pipeline-meshy-swap finalization
- `agentic_orchestration/legolas/research/unity-catalogue-armor-meshy-2026-05-22/` — completed Unity catalogue + Meshy armor capability findings (5 files)
- `agentic_orchestration/legolas/research/meshy-pipeline-2026-05-22/findings.md` — completed Meshy pipeline capability research

### 11.5 Discipline ratifications + process
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § 19 — RATIFIED 2026-05-22 (engine commit `0d1ad63`)
- `~/Games/reincarnated-engine/design/decisions/decisions-log.md` 2026-05-22 entry — Discipline #19 ratification entry
- `agentic_orchestration/galadriel/notes/2026-05-22-canary-meshy-regen.md` § 8 — companions/VFX canonical pipeline pattern (rigid-attachment vs independent-life categorization)

### 11.6 Memory references (to be updated under legacy-categorical-cleanup-audit)
- `memory/project_role_orientation_taxonomy.md` — to be marked historical/diagnostic-only
- `memory/project_trait_architecture.md` — to be marked legacy / borderline vestigial under BC-axis-derived stats framework
- `memory/project_earth_meta_layer.md` — captures Earth Self framing; load-bearing for Reincarnated overlay
- `memory/project_pet_system.md` — companion creatures architecture; pulls forward into Reincarnated overlay v1

---

**Signed:** gandalf (story-and-design steward; senior designer)
**Authority:** Matt 2026-05-22 — explicit strategic reframe + Variant C scope adoption + per-profile overlay architecture + engine-flag/profile-overlay-flag separation
**For:** canonical lock of the strategic reframe; Variant C engine scope commitment; Reincarnated profile overlay architectural definition; foundation for tomorrow's three companion canonical docs (legacy-categorical-cleanup-audit; stat-derivation-from-bc-convergence; gear-heavy-promotion).
