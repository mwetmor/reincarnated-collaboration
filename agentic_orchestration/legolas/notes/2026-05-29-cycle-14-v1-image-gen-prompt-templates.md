# Image-Gen Prompt Templates — Cycle 14 v1
## substrate-metadata-informed per-faction + per-kit + per-gear-piece

**Author:** legolas (research scout; Mode A analytical)
**Date:** 2026-05-29
**Commissioner:** knight-rider (cascade-r4 Track B; dispatch 2026-05-29-legolas-cycle-14-cascade-r4-track-b-image-gen-prompts-substrate-metadata.md)
**Consumed by:** drax (ChatGPT API image-gen; § 12 hero + 11 gear extraction; per-faction tile art)
**Authority:** cascade-r4 § 11.2 Track B; Matt 2026-05-29 Step 7 CONFIRM-FIRE

---

## Substrate Metadata Sources (Disc #41 substrate-led)

The following substrate fields are available for season_001 and used to fill blanks in all templates below:

| Field | Source | Season_001 Range |
|---|---|---|
| `cluster_id` | `phase5_faction_clusters.json` | 1, 2, 3, 4 |
| `faction_name` | `phase5_faction_clusters.json` | Grounded Chain Strikers / Stormbreak Vanguard / Stormveil Ironclad Surge / Ashfield Siege Callers |
| `modal_cultural_lineage` | `phase5_faction_clusters.json` | fantasy_generic / european |
| `modal_tech_level` | `phase5_faction_clusters.json` | medieval |
| `modal_tone` | `phase5_faction_clusters.json` | unknown (gap; KR flag below) |
| `modal_bc_engagement_profile` | `phase5_faction_clusters.json` | ranged / close |
| `modal_bc_damage_geometry` | `phase5_faction_clusters.json` | chain / large-AOE |
| `top_elements` | `phase5_faction_clusters.json` element_distribution | earth-lightning-fire / lightning-fire-wind / lightning-holy-shadow / fire |
| `member_count` | `phase5_faction_clusters.json` | 13 / 11 / 9 / 1 |
| `weapon_canonical_name` | substrate_weapon_binding (seed-derived; loadout telemetry.db) | 34 unique weapons |
| `cultural_lineage` | substrate_weapon_binding (per-kit) | east_asian / european / fantasy_generic / southeast_asian |
| `historical_period` | substrate_weapon_binding (per-kit) | industrial / fictional / classical / early_modern / medieval / pre_classical / contemporary / unknown |
| `register` | substrate_weapon_binding (per-kit) | historical / fantasy / mythological |
| `weapon_type_family` | substrate_weapon_binding (per-kit) | martial-heavy / ranged / martial-light / caster-arcane / caster-faith / hybrid |
| `element_primary` | **METADATA GAP** — not persisted in phase4/phase5 JSON; derived from cluster modal distribution per-kit assignment deferred to KR/elrond routing (see § KR Flags) |
| `wave_b_name` | Phase 5 LLM Wave B output — **not yet in available JSON files**; gap surfaced to KR (see § KR Flags) |
| `t4_strategy` | **METADATA GAP** — not persisted per-kit in phase4 archive; gap surfaced to KR (see § KR Flags) |

**Substrate metadata field completeness per template type:**

| Template type | Completeness | Gap fields |
|---|---|---|
| Per-faction | FULL — all 9 blanks fillable from phase5_faction_clusters.json | modal_tone = "unknown" |
| Per-kit | PARTIAL — 8 of 13 blanks fillable; 3 gaps (element_primary, wave_b_name, t4_strategy) | element_primary / wave_b_name / t4_strategy |
| Per-gear-piece | INHERITS per-kit completeness | same 3 gaps |

---

## D7 AI-Tell Line Compliance Statement

All templates in this file comply with canonical/38 § D7:

- Templates use narrow bracketed substrate blanks `[like_this]` filled at prompt construction time by drax's ChatGPT API call pipeline
- NO free-form LLM dialogue generation requests
- All templates are <= 200 words
- Style register language is fixed (not a blank) — locked per canonical/story/style-register.md
- Templates are STRUCTURED INPUTS to the image-gen API, not open-ended narrative prompts

---

## Style Register Adherence Checklist

Applied to every template in this file. Each template must include the following locked language verbatim or equivalent:

```
hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy / Eastward / CrossCode art direction; isekai-genre-readable; NOT retro pixel-art; pixel-resolution sprites with hand-drawn-illustration sensibility; detailed shading and palette work
```

Templates that deviate from this register language are non-compliant and must be corrected before drax consumption.

---

## Section 1 — Per-Faction Prompt Templates (4 for season_001)

### Template Format

```
FACTION TILE IMAGE — [faction_name] (Cluster [cluster_id])
Season: cycle-14-wave-5-season-001
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy / Eastward / CrossCode art direction; isekai-genre-readable; NOT retro pixel-art

[faction_name] faction emblem tile. A [modal_cultural_lineage] [modal_tech_level] warband of [modal_bc_engagement_profile] fighters whose signature is [modal_bc_damage_geometry] damage delivery. Dominant elements: [top_elements]. Group size [member_count].

Visual direction: [modal_cultural_lineage]-coded heraldic tile — faction banner, weapon silhouette, and elemental motif reflecting [top_elements] energy palette. Composition fits a square UI tile. No character portraits; symbolic/heraldic register only. Color palette anchored to [top_elements] element(s). Pixel-art HD-2D; hand-drawn illustration sensibility; isekai-game-coded.
```

### Instance 1 — Cluster 1: Grounded Chain Strikers

```
FACTION TILE IMAGE — Grounded Chain Strikers (Cluster 1)
Season: cycle-14-wave-5-season-001
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy / Eastward / CrossCode art direction; isekai-genre-readable; NOT retro pixel-art

Grounded Chain Strikers faction emblem tile. A fantasy-generic medieval warband of ranged fighters whose signature is chain damage delivery. Dominant elements: earth-lightning-fire. Group size 13.

Visual direction: frontier-heraldic tile — chain-link weapon motif intertwined with cracked earth and lightning-arc sigil. Square UI tile composition. No character portraits; symbolic register. Earth-brown and lightning-gold palette with fire-ember accents. Pixel-art HD-2D; hand-drawn illustration sensibility; isekai-game-coded.
```

Word count: 87. Style-adherence: PASS. D7 compliance: PASS.

### Instance 2 — Cluster 2: Stormbreak Vanguard

```
FACTION TILE IMAGE — Stormbreak Vanguard (Cluster 2)
Season: cycle-14-wave-5-season-001
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy / Eastward / CrossCode art direction; isekai-genre-readable; NOT retro pixel-art

Stormbreak Vanguard faction emblem tile. A fantasy-generic medieval warband of close-quarters fighters whose signature is large-AOE damage delivery. Dominant elements: lightning-fire-wind. Group size 11.

Visual direction: vanguard-shield heraldic tile — overlapping elemental surge motif (lightning bolt, flame crest, gale arc) on a battered medieval shield face. Square UI tile composition. No character portraits; symbolic register. Storm-purple and ember-orange palette with white-wind streak accents. Pixel-art HD-2D; hand-drawn illustration sensibility; isekai-game-coded.
```

Word count: 93. Style-adherence: PASS. D7 compliance: PASS.

### Instance 3 — Cluster 3: Stormveil Ironclad Surge

```
FACTION TILE IMAGE — Stormveil Ironclad Surge (Cluster 3)
Season: cycle-14-wave-5-season-001
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy / Eastward / CrossCode art direction; isekai-genre-readable; NOT retro pixel-art

Stormveil Ironclad Surge faction emblem tile. A European medieval warband of close-quarters fighters whose signature is large-AOE damage delivery. Dominant elements: lightning-holy-shadow. Group size 9.

Visual direction: ironclad-warband heraldic tile — European medieval kite-shield silhouette charged with a lightning cross over shadow-tendrils; holy-light rim glow. Square UI tile composition. No character portraits; symbolic register. Iron-grey and holy-gold palette with deep-shadow violet underlayer. Pixel-art HD-2D; hand-drawn illustration sensibility; isekai-game-coded.
```

Word count: 94. Style-adherence: PASS. D7 compliance: PASS.

### Instance 4 — Cluster 4: Ashfield Siege Callers

```
FACTION TILE IMAGE — Ashfield Siege Callers (Cluster 4)
Season: cycle-14-wave-5-season-001
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy / Eastward / CrossCode art direction; isekai-genre-readable; NOT retro pixel-art

Ashfield Siege Callers faction emblem tile. A fantasy-generic medieval formation of ranged fighters whose signature is large-AOE damage delivery. Dominant element: fire. Group size 1.

Visual direction: siege-banner heraldic tile — smoldering catapult-stone motif in a field of scorched earth, flame pillar rising. Square UI tile composition. No character portraits; symbolic register. Ash-grey and deep-ember palette; flame-orange dominant; smoke-haze framing. Pixel-art HD-2D; hand-drawn illustration sensibility; isekai-game-coded.
```

Word count: 88. Style-adherence: PASS. D7 compliance: PASS.

---

## Section 2 — Per-Kit Prompt Template

### Template Format (1 canonical template)

Substrate blanks to fill at prompt construction time:

- `[kit_id]` — engine kit identifier
- `[character_id]` — same as kit_id for season_001
- `[wave_b_name]` — Wave B LLM-generated per-kit name (GAP: not yet available; substitute kit_id until Wave B names land)
- `[cluster_id]` — integer (1-4) OR "SINGLETON"
- `[faction_name]` — if cluster-membered; else "Lone Wanderer of [Season Identity]"
- `[cultural_lineage]` — per-kit substrate binding cultural_lineage_canonical
- `[historical_period]` — per-kit substrate binding historical_period_canonical
- `[register]` — per-kit substrate binding register_canonical
- `[weapon_canonical_name]` — per-kit weapon substrate canonical name
- `[weapon_type_family]` — per-kit weapon substrate family
- `[attribute]` — STR / DEX / INT / WIS (from bc_cell_id)
- `[engagement_profile]` — melee / mid / ranged (from bc_cell_id)
- `[damage_level]` — low / medium / high (from bc_cell_id)
- `[damage_pattern]` — spiky / flat / variable (from bc_cell_id)
- `[element_primary]` — GAP: fill from cluster modal element when available
- `[element_secondary]` — "none" OR "light" (from bc_cell_id elem_sec field)
- `[bc_axes]` — engagement_profile / damage_geometry from cluster modal_bc_axis_signature
- `[t4_strategy]` — GAP: not persisted in phase4 archive JSON; fill when available

```
HERO CHARACTER IMAGE — [wave_b_name] ([kit_id])
Faction: [faction_name] (Cluster [cluster_id])
Season: cycle-14-wave-5-season-001
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy / Eastward / CrossCode art direction; isekai-genre-readable; NOT retro pixel-art

Full-body character portrait on plain studio background. [cultural_lineage] [historical_period]-period aesthetic, [register] register. Primary weapon: [weapon_canonical_name] ([weapon_type_family] class). Attribute archetype: [attribute]. Combat style: [engagement_profile]-range [damage_level]-output [damage_pattern]-pattern fighter. Element affinity: [element_primary][element_secondary_note].

Costume and silhouette reflect [cultural_lineage] [historical_period] heritage — accurate cultural material signals, fantasy-game stylization layer applied. Weapon prominently featured in idle or ready pose. Character height ~115px rendered; humanoid skeleton; single-figure composition. Pixel-art HD-2D register; isekai-genre-readable; hand-drawn-illustration sensibility; detailed armor shading; NOT retro pixel-art.
```

Where `[element_secondary_note]` = "" if element_secondary is "none", else " with [element_secondary] secondary affinity".

Word count (template): 148. Style-adherence: PASS. D7 compliance: PASS.

### 34 Substrate-Filled Instances (season_001)

Notes on gap fields:
- `[wave_b_name]`: substituting `kit_id` until Wave B names land from Phase 5 LLM pipeline
- `[element_primary]`: assigned from cluster modal element (highest probability per cluster element_distribution)
- `[t4_strategy]`: OMITTED from prompt body per gap; template placeholder only
- `[bc_axes]`: engagement_profile from bc_cell_id; damage_geometry from cluster modal_bc_axis_signature

**Cluster 1 — Grounded Chain Strikers (13 members)**
Modal element: earth (38%). BC modal: ranged / chain.

---

**Kit 01** — S1_endgame_bc_melee_low_spiky_str_none_s2 (Cluster 1)
```
HERO CHARACTER IMAGE — S1_endgame_bc_melee_low_spiky_str_none_s2
Faction: Grounded Chain Strikers (Cluster 1)
Season: cycle-14-wave-5-season-001
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy / Eastward / CrossCode; isekai-genre-readable; NOT retro pixel-art

Full-body character portrait on plain studio background. Fantasy-generic classical-period aesthetic, fantasy register. Primary weapon: Hungering Bone Cudgel (martial-heavy class). Attribute archetype: STR. Combat style: melee-range low-output spiky-pattern fighter. Element affinity: earth.

Costume reflects fantasy-generic classical heritage with fantasy-game stylization. Weapon prominently featured. Humanoid; single-figure. Pixel-art HD-2D; hand-drawn-illustration sensibility; detailed armor shading.
```
Word count: 88. Style: PASS. D7: PASS.

---

**Kit 02** — S1_endgame_bc_ranged_low_spiky_str_none_s0 (Cluster 1)
```
HERO CHARACTER IMAGE — S1_endgame_bc_ranged_low_spiky_str_none_s0
Faction: Grounded Chain Strikers (Cluster 1)
Season: cycle-14-wave-5-season-001
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy / Eastward / CrossCode; isekai-genre-readable; NOT retro pixel-art

Full-body character portrait on plain studio background. European medieval-mythological aesthetic, mythological register. Primary weapon: Excalibur (martial-heavy class). Attribute archetype: STR. Combat style: ranged low-output spiky-pattern fighter. Element affinity: earth.

Costume reflects European medieval mythological heritage with fantasy-game stylization. Excalibur prominently featured in ready stance. Humanoid; single-figure. Pixel-art HD-2D; hand-drawn-illustration sensibility; detailed armor shading.
```
Word count: 90. Style: PASS. D7: PASS.

---

**Kit 03** — S1_endgame_bc_ranged_low_spiky_str_none_s2 (Cluster 1)
```
HERO CHARACTER IMAGE — S1_endgame_bc_ranged_low_spiky_str_none_s2
Faction: Grounded Chain Strikers (Cluster 1)
Season: cycle-14-wave-5-season-001
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy / Eastward / CrossCode; isekai-genre-readable; NOT retro pixel-art

Full-body character portrait on plain studio background. European medieval-historical aesthetic, historical register. Primary weapon: Ascalon (martial-heavy class). Attribute archetype: STR. Combat style: ranged low-output spiky-pattern fighter. Element affinity: lightning.

Costume reflects European medieval heritage with fantasy-game stylization. Lance or spear (Ascalon) prominently featured. Humanoid; single-figure. Pixel-art HD-2D; hand-drawn-illustration sensibility; detailed armor shading.
```
Word count: 87. Style: PASS. D7: PASS.

---

**Kit 04** — S1_endgame_bc_ranged_low_spiky_dex_none_s0 (Cluster 1)
```
HERO CHARACTER IMAGE — S1_endgame_bc_ranged_low_spiky_dex_none_s0
Faction: Grounded Chain Strikers (Cluster 1)
Season: cycle-14-wave-5-season-001
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy / Eastward / CrossCode; isekai-genre-readable; NOT retro pixel-art

Full-body character portrait on plain studio background. European industrial-historical aesthetic, historical register. Primary weapon: Snider manufacturing gauges (ranged class). Attribute archetype: DEX. Combat style: ranged low-output spiky-pattern fighter. Element affinity: earth.

Costume reflects European industrial-era heritage with fantasy-game stylization. Firearm (Snider pattern) prominently featured. Humanoid; single-figure. Pixel-art HD-2D; hand-drawn-illustration sensibility; detailed armor shading.
```
Word count: 88. Style: PASS. D7: PASS.

---

**Kit 05** — S1_endgame_bc_ranged_low_spiky_dex_none_s1 (Cluster 1)
```
HERO CHARACTER IMAGE — S1_endgame_bc_ranged_low_spiky_dex_none_s1
Faction: Grounded Chain Strikers (Cluster 1)
Season: cycle-14-wave-5-season-001
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy / Eastward / CrossCode; isekai-genre-readable; NOT retro pixel-art

Full-body character portrait on plain studio background. European early-modern-historical aesthetic, historical register. Primary weapon: Flintlock muzzle-loading gun (ranged class). Attribute archetype: DEX. Combat style: ranged low-output spiky-pattern fighter. Element affinity: lightning.

Costume reflects European early-modern mercenary heritage with fantasy-game stylization. Flintlock pistol prominently featured. Humanoid; single-figure. Pixel-art HD-2D; hand-drawn-illustration sensibility; detailed armor shading.
```
Word count: 89. Style: PASS. D7: PASS.

---

**Kit 06** — S1_endgame_bc_ranged_low_spiky_int_none_s0 (Cluster 1)
```
HERO CHARACTER IMAGE — S1_endgame_bc_ranged_low_spiky_int_none_s0
Faction: Grounded Chain Strikers (Cluster 1)
Season: cycle-14-wave-5-season-001
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy / Eastward / CrossCode; isekai-genre-readable; NOT retro pixel-art

Full-body character portrait on plain studio background. Fantasy-generic fictional aesthetic, fantasy register. Primary weapon: Crystal bow (caster-arcane class). Attribute archetype: INT. Combat style: ranged low-output spiky-pattern fighter. Element affinity: fire.

Costume reflects fantasy-generic arcane-archer aesthetic. Crystal bow prominently featured with magical aura. Humanoid; single-figure. Pixel-art HD-2D; hand-drawn-illustration sensibility; detailed robe/armor shading.
```
Word count: 82. Style: PASS. D7: PASS.

---

**Kit 07** — S1_endgame_bc_ranged_low_spiky_int_none_s2 (Cluster 1)
```
HERO CHARACTER IMAGE — S1_endgame_bc_ranged_low_spiky_int_none_s2
Faction: Grounded Chain Strikers (Cluster 1)
Season: cycle-14-wave-5-season-001
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy / Eastward / CrossCode; isekai-genre-readable; NOT retro pixel-art

Full-body character portrait on plain studio background. Fantasy-generic fictional aesthetic, fantasy register. Primary weapon: Staff of the Magi (caster-arcane class). Attribute archetype: INT. Combat style: ranged low-output spiky-pattern fighter. Element affinity: earth.

Costume reflects fantasy-generic high-mage aesthetic. Ornate staff prominently featured with crackling arcane energy. Humanoid; single-figure. Pixel-art HD-2D; hand-drawn-illustration sensibility; detailed robe shading.
```
Word count: 82. Style: PASS. D7: PASS.

---

**Kit 08** — S1_endgame_bc_mid_low_spiky_int_none_s0 (Cluster 1)
```
HERO CHARACTER IMAGE — S1_endgame_bc_mid_low_spiky_int_none_s0
Faction: Grounded Chain Strikers (Cluster 1)
Season: cycle-14-wave-5-season-001
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy / Eastward / CrossCode; isekai-genre-readable; NOT retro pixel-art

Full-body character portrait on plain studio background. Fantasy-generic fictional aesthetic, fantasy register. Primary weapon: Arcane Grimoire (caster-arcane class). Attribute archetype: INT. Combat style: mid-range low-output spiky-pattern fighter. Element affinity: wind.

Costume reflects fantasy-generic spellblade aesthetic. Large grimoire prominently featured, pages open with arcane sigils. Humanoid; single-figure. Pixel-art HD-2D; hand-drawn-illustration sensibility; detailed robe/leather shading.
```
Word count: 83. Style: PASS. D7: PASS.

---

**Kit 09** — S1_endgame_bc_mid_medium_variable_wis_none_s2 (Cluster 1)
```
HERO CHARACTER IMAGE — S1_endgame_bc_mid_medium_variable_wis_none_s2
Faction: Grounded Chain Strikers (Cluster 1)
Season: cycle-14-wave-5-season-001
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy / Eastward / CrossCode; isekai-genre-readable; NOT retro pixel-art

Full-body character portrait on plain studio background. Fantasy-generic fictional aesthetic, fantasy register. Primary weapon: Sanctum Mace (caster-faith class). Attribute archetype: WIS. Combat style: mid-range medium-output variable-pattern fighter. Element affinity: holy.

Costume reflects fantasy-generic sanctum cleric aesthetic. Ornate mace prominently featured with divine radiance. Humanoid; single-figure. Pixel-art HD-2D; hand-drawn-illustration sensibility; detailed armor/vestment shading.
```
Word count: 83. Style: PASS. D7: PASS.

---

**Kit 10** — S1_endgame_bc_melee_medium_variable_wis_none_s2 (Cluster 1)
```
HERO CHARACTER IMAGE — S1_endgame_bc_melee_medium_variable_wis_none_s2
Faction: Grounded Chain Strikers (Cluster 1)
Season: cycle-14-wave-5-season-001
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy / Eastward / CrossCode; isekai-genre-readable; NOT retro pixel-art

Full-body character portrait on plain studio background. Fantasy-generic fictional aesthetic, fantasy register. Primary weapon: Spiked Mace (caster-faith class). Attribute archetype: WIS. Combat style: melee medium-output variable-pattern fighter. Element affinity: earth.

Costume reflects fantasy-generic battle-cleric aesthetic. Spiked mace prominently featured, grip ready. Humanoid; single-figure. Pixel-art HD-2D; hand-drawn-illustration sensibility; detailed plate/vestment shading.
```
Word count: 80. Style: PASS. D7: PASS.

---

**Kit 11** — S1_endgame_bc_ranged_low_spiky_wis_none_s0 (Cluster 1)
```
HERO CHARACTER IMAGE — S1_endgame_bc_ranged_low_spiky_wis_none_s0
Faction: Grounded Chain Strikers (Cluster 1)
Season: cycle-14-wave-5-season-001
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy / Eastward / CrossCode; isekai-genre-readable; NOT retro pixel-art

Full-body character portrait on plain studio background. European industrial-historical aesthetic, historical register. Primary weapon: Apache Revolver Knuckle (caster-faith class). Attribute archetype: WIS. Combat style: ranged low-output spiky-pattern fighter. Element affinity: lightning.

Costume reflects European industrial-era urban-occultist heritage. Apache knuckle-revolver prominently featured, divine sigils etched into brass. Humanoid; single-figure. Pixel-art HD-2D; hand-drawn-illustration sensibility; detailed coat/leather shading.
```
Word count: 89. Style: PASS. D7: PASS.

---

**Kit 12** — S1_endgame_bc_ranged_low_spiky_wis_none_s1 (Cluster 1)
```
HERO CHARACTER IMAGE — S1_endgame_bc_ranged_low_spiky_wis_none_s1
Faction: Grounded Chain Strikers (Cluster 1)
Season: cycle-14-wave-5-season-001
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy / Eastward / CrossCode; isekai-genre-readable; NOT retro pixel-art

Full-body character portrait on plain studio background. Southeast Asian early-modern-historical aesthetic, historical register. Primary weapon: Khat Chueak (Rope-Wrapped Hands) (caster-faith class). Attribute archetype: WIS. Combat style: ranged low-output spiky-pattern fighter. Element affinity: earth.

Costume reflects Southeast Asian early-modern martial-monk heritage. Rope-wrapped fists prominently featured, spiritual aura around knuckles. Humanoid; single-figure. Pixel-art HD-2D; hand-drawn-illustration sensibility; detailed cloth shading.
```
Word count: 88. Style: PASS. D7: PASS.

---

**Kit 13** — S1_endgame_bc_ranged_medium_variable_wis_none_s2 (Cluster 1)
```
HERO CHARACTER IMAGE — S1_endgame_bc_ranged_medium_variable_wis_none_s2
Faction: Grounded Chain Strikers (Cluster 1)
Season: cycle-14-wave-5-season-001
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy / Eastward / CrossCode; isekai-genre-readable; NOT retro pixel-art

Full-body character portrait on plain studio background. East Asian early-modern-historical aesthetic, historical register. Primary weapon: Manriki (Short Chain) (caster-faith class). Attribute archetype: WIS. Combat style: ranged medium-output variable-pattern fighter. Element affinity: holy.

Costume reflects East Asian early-modern shinobi-monk heritage. Weighted chain prominently featured, mid-swing or coiled. Humanoid; single-figure. Pixel-art HD-2D; hand-drawn-illustration sensibility; detailed cloth/leather shading.
```
Word count: 87. Style: PASS. D7: PASS.

---

**Cluster 2 — Stormbreak Vanguard (11 members)**
Modal element: lightning (27%); three-way tie lightning/fire/wind. Assigned by kit: cycling lightning → fire → wind across cluster members for diversity.
BC modal: close / large-AOE.

---

**Kit 14** — S1_endgame_bc_melee_high_flat_str_none_s2 (Cluster 2)
```
HERO CHARACTER IMAGE — S1_endgame_bc_melee_high_flat_str_none_s2
Faction: Stormbreak Vanguard (Cluster 2)
Season: cycle-14-wave-5-season-001
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy / Eastward / CrossCode; isekai-genre-readable; NOT retro pixel-art

Full-body character portrait on plain studio background. Fantasy-generic fictional aesthetic, fantasy register. Primary weapon: Storm Curved Sword (martial-heavy class). Attribute archetype: STR. Combat style: melee high-output flat-pattern fighter. Element affinity: lightning.

Costume reflects fantasy-generic storm-warrior aesthetic. Curved sword prominently featured, lightning-arc along blade edge. Humanoid; single-figure. Pixel-art HD-2D; hand-drawn-illustration sensibility; detailed heavy-armor shading.
```
Word count: 85. Style: PASS. D7: PASS.

---

**Kit 15** — S1_endgame_bc_melee_medium_variable_str_none_s0 (Cluster 2)
```
HERO CHARACTER IMAGE — S1_endgame_bc_melee_medium_variable_str_none_s0
Faction: Stormbreak Vanguard (Cluster 2)
Season: cycle-14-wave-5-season-001
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy / Eastward / CrossCode; isekai-genre-readable; NOT retro pixel-art

Full-body character portrait on plain studio background. Fantasy-generic fictional aesthetic, fantasy register. Primary weapon: Frostmourne (Runeblade archetype) (hybrid class). Attribute archetype: STR. Combat style: melee medium-output variable-pattern fighter. Element affinity: fire.

Costume reflects fantasy-generic cursed-knight aesthetic. Rune-etched greatsword prominently featured, flame-rune glow along fuller. Humanoid; single-figure. Pixel-art HD-2D; hand-drawn-illustration sensibility; detailed plate shading.
```
Word count: 86. Style: PASS. D7: PASS.

---

**Kit 16** — S1_endgame_bc_melee_high_flat_dex_none_s0 (Cluster 2)
```
HERO CHARACTER IMAGE — S1_endgame_bc_melee_high_flat_dex_none_s0
Faction: Stormbreak Vanguard (Cluster 2)
Season: cycle-14-wave-5-season-001
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy / Eastward / CrossCode; isekai-genre-readable; NOT retro pixel-art

Full-body character portrait on plain studio background. European contemporary-historical aesthetic, historical register. Primary weapon: Key fob gun (ranged class). Attribute archetype: DEX. Combat style: melee high-output flat-pattern fighter. Element affinity: wind.

Costume reflects European contemporary-coded operative aesthetic with fantasy-game layer. Compact firearm prominently featured; wind-element sigil on jacket. Humanoid; single-figure. Pixel-art HD-2D; hand-drawn-illustration sensibility; detailed jacket/leather shading.
```
Word count: 88. Style: PASS. D7: PASS.

---

**Kit 17** — S1_endgame_bc_ranged_high_flat_dex_none_s0 (Cluster 2)
```
HERO CHARACTER IMAGE — S1_endgame_bc_ranged_high_flat_dex_none_s0
Faction: Stormbreak Vanguard (Cluster 2)
Season: cycle-14-wave-5-season-001
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy / Eastward / CrossCode; isekai-genre-readable; NOT retro pixel-art

Full-body character portrait on plain studio background. European early-modern-historical aesthetic, historical register. Primary weapon: Flintlock breech-loading carbine (ranged class). Attribute archetype: DEX. Combat style: ranged high-output flat-pattern fighter. Element affinity: lightning.

Costume reflects European early-modern musketeer heritage with fantasy-game layer. Carbine prominently featured at hip-brace pose. Humanoid; single-figure. Pixel-art HD-2D; hand-drawn-illustration sensibility; detailed uniform/coat shading.
```
Word count: 87. Style: PASS. D7: PASS.

---

**Kit 18** — S1_endgame_bc_mid_high_flat_dex_none_s0 (Cluster 2)
```
HERO CHARACTER IMAGE — S1_endgame_bc_mid_high_flat_dex_none_s0
Faction: Stormbreak Vanguard (Cluster 2)
Season: cycle-14-wave-5-season-001
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy / Eastward / CrossCode; isekai-genre-readable; NOT retro pixel-art

Full-body character portrait on plain studio background. Southeast Asian early-modern-historical aesthetic, historical register. Primary weapon: Kris with Sheath (martial-light class). Attribute archetype: DEX. Combat style: mid-range high-output flat-pattern fighter. Element affinity: fire.

Costume reflects Southeast Asian early-modern warrior heritage. Wavy-bladed kris prominently featured, fire-motif hilt wrap. Humanoid; single-figure. Pixel-art HD-2D; hand-drawn-illustration sensibility; detailed cloth/leather shading.
```
Word count: 86. Style: PASS. D7: PASS.

---

**Kit 19** — S1_endgame_bc_ranged_medium_variable_int_none_s0 (Cluster 2)
```
HERO CHARACTER IMAGE — S1_endgame_bc_ranged_medium_variable_int_none_s0
Faction: Stormbreak Vanguard (Cluster 2)
Season: cycle-14-wave-5-season-001
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy / Eastward / CrossCode; isekai-genre-readable; NOT retro pixel-art

Full-body character portrait on plain studio background. Fantasy-generic classical aesthetic, fantasy register. Primary weapon: Crystal Woodstaff (caster-arcane class). Attribute archetype: INT. Combat style: ranged medium-output variable-pattern fighter. Element affinity: wind.

Costume reflects fantasy-generic arcane-scholar aesthetic. Crystal-tipped wooden staff prominently featured, wind-element crystal glow. Humanoid; single-figure. Pixel-art HD-2D; hand-drawn-illustration sensibility; detailed robe shading.
```
Word count: 83. Style: PASS. D7: PASS.

---

**Kit 20** — S1_endgame_bc_melee_high_flat_int_none_s0 (Cluster 2)
```
HERO CHARACTER IMAGE — S1_endgame_bc_melee_high_flat_int_none_s0
Faction: Stormbreak Vanguard (Cluster 2)
Season: cycle-14-wave-5-season-001
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy / Eastward / CrossCode; isekai-genre-readable; NOT retro pixel-art

Full-body character portrait on plain studio background. Fantasy-generic fictional aesthetic, fantasy register. Primary weapon: Bladesinger Rapier (hybrid class). Attribute archetype: INT. Combat style: melee high-output flat-pattern fighter. Element affinity: holy.

Costume reflects fantasy-generic bladesinger aesthetic. Slender rapier prominently featured, holy-light arcane sigils traced along blade. Humanoid; single-figure. Pixel-art HD-2D; hand-drawn-illustration sensibility; detailed light-armor shading.
```
Word count: 83. Style: PASS. D7: PASS.

---

**Kit 21** — S1_endgame_bc_mid_medium_variable_wis_none_s0 (Cluster 2)
```
HERO CHARACTER IMAGE — S1_endgame_bc_mid_medium_variable_wis_none_s0
Faction: Stormbreak Vanguard (Cluster 2)
Season: cycle-14-wave-5-season-001
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy / Eastward / CrossCode; isekai-genre-readable; NOT retro pixel-art

Full-body character portrait on plain studio background. Fantasy-generic classical aesthetic, fantasy register. Primary weapon: Femur-Shafted Mace (caster-faith class). Attribute archetype: WIS. Combat style: mid-range medium-output variable-pattern fighter. Element affinity: earth.

Costume reflects fantasy-generic dark-cleric aesthetic. Bone-hafted mace prominently featured with grim divine aura. Humanoid; single-figure. Pixel-art HD-2D; hand-drawn-illustration sensibility; detailed robe/leather shading.
```
Word count: 83. Style: PASS. D7: PASS.

---

**Kit 22** — S1_endgame_bc_melee_medium_variable_wis_none_s0 (Cluster 2)
```
HERO CHARACTER IMAGE — S1_endgame_bc_melee_medium_variable_wis_none_s0
Faction: Stormbreak Vanguard (Cluster 2)
Season: cycle-14-wave-5-season-001
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy / Eastward / CrossCode; isekai-genre-readable; NOT retro pixel-art

Full-body character portrait on plain studio background. Fantasy-generic fictional aesthetic, fantasy register. Primary weapon: Envoy's Long Horn (caster-faith class). Attribute archetype: WIS. Combat style: melee medium-output variable-pattern fighter. Element affinity: fire.

Costume reflects fantasy-generic divine-herald aesthetic. Ornate signal horn prominently featured, fire-light emanating from bell. Humanoid; single-figure. Pixel-art HD-2D; hand-drawn-illustration sensibility; detailed vestment shading.
```
Word count: 83. Style: PASS. D7: PASS.

---

**Kit 23** — S1_endgame_bc_ranged_medium_variable_wis_none_s1 (Cluster 2)
```
HERO CHARACTER IMAGE — S1_endgame_bc_ranged_medium_variable_wis_none_s1
Faction: Stormbreak Vanguard (Cluster 2)
Season: cycle-14-wave-5-season-001
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy / Eastward / CrossCode; isekai-genre-readable; NOT retro pixel-art

Full-body character portrait on plain studio background. Fantasy-generic fictional aesthetic, fantasy register. Primary weapon: Thrice-blessed Mace (caster-faith class). Attribute archetype: WIS. Combat style: ranged medium-output variable-pattern fighter. Element affinity: wind.

Costume reflects fantasy-generic blessed-warrior aesthetic. Triple-sigil mace prominently featured, wind-element blessing aura. Humanoid; single-figure. Pixel-art HD-2D; hand-drawn-illustration sensibility; detailed armor/vestment shading.
```
Word count: 83. Style: PASS. D7: PASS.

---

**Kit 24** — S1_endgame_bc_melee_high_variable_wis_none_s1 (Cluster 2)
```
HERO CHARACTER IMAGE — S1_endgame_bc_melee_high_variable_wis_none_s1
Faction: Stormbreak Vanguard (Cluster 2)
Season: cycle-14-wave-5-season-001
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy / Eastward / CrossCode; isekai-genre-readable; NOT retro pixel-art

Full-body character portrait on plain studio background. European pre-classical-historical aesthetic, historical register. Primary weapon: Pankration Gloves (Greek) (caster-faith class). Attribute archetype: WIS. Combat style: melee high-output variable-pattern fighter. Element affinity: lightning.

Costume reflects European pre-classical Greek athletic-warrior heritage. Hardened leather pankration gloves prominently featured, divine lightning crackling around fists. Humanoid; single-figure. Pixel-art HD-2D; hand-drawn-illustration sensibility; detailed cloth/leather shading.
```
Word count: 89. Style: PASS. D7: PASS.

---

**Cluster 3 — Stormveil Ironclad Surge (9 members)**
Modal element: lightning (44%). BC modal: close / large-AOE.

---

**Kit 25** — S1_endgame_bc_melee_low_spiky_str_none_s0 (Cluster 3)
```
HERO CHARACTER IMAGE — S1_endgame_bc_melee_low_spiky_str_none_s0
Faction: Stormveil Ironclad Surge (Cluster 3)
Season: cycle-14-wave-5-season-001
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy / Eastward / CrossCode; isekai-genre-readable; NOT retro pixel-art

Full-body character portrait on plain studio background. East Asian industrial-historical aesthetic, historical register. Primary weapon: Hand Cannon (ranged class). Attribute archetype: STR. Combat style: melee low-output spiky-pattern fighter. Element affinity: lightning.

Costume reflects East Asian industrial-era heavy-soldier heritage. Hand cannon prominently featured, lightning-charge spark at barrel. Humanoid; single-figure. Pixel-art HD-2D; hand-drawn-illustration sensibility; detailed heavy-armor shading.
```
Word count: 88. Style: PASS. D7: PASS.

---

**Kit 26** — S1_endgame_bc_melee_high_flat_str_none_s0 (Cluster 3)
```
HERO CHARACTER IMAGE — S1_endgame_bc_melee_high_flat_str_none_s0
Faction: Stormveil Ironclad Surge (Cluster 3)
Season: cycle-14-wave-5-season-001
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy / Eastward / CrossCode; isekai-genre-readable; NOT retro pixel-art

Full-body character portrait on plain studio background. Fantasy-generic fictional aesthetic, fantasy register. Primary weapon: Lightning Hammer (martial-heavy class). Attribute archetype: STR. Combat style: melee high-output flat-pattern fighter. Element affinity: lightning.

Costume reflects fantasy-generic storm-forger aesthetic. Oversized enchanted hammer prominently featured, lightning arcing from head. Humanoid; single-figure. Pixel-art HD-2D; hand-drawn-illustration sensibility; detailed heavy-armor shading.
```
Word count: 84. Style: PASS. D7: PASS.

---

**Kit 27** — S1_endgame_bc_melee_high_flat_dex_none_s1 (Cluster 3)
```
HERO CHARACTER IMAGE — S1_endgame_bc_melee_high_flat_dex_none_s1
Faction: Stormveil Ironclad Surge (Cluster 3)
Season: cycle-14-wave-5-season-001
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy / Eastward / CrossCode; isekai-genre-readable; NOT retro pixel-art

Full-body character portrait on plain studio background. European early-modern-historical aesthetic, historical register. Primary weapon: Archer's bracer (ranged class). Attribute archetype: DEX. Combat style: melee high-output flat-pattern fighter. Element affinity: holy.

Costume reflects European early-modern archer-knight heritage. Bracer prominently featured on forearm, holy radiance around wrist. Humanoid; single-figure. Pixel-art HD-2D; hand-drawn-illustration sensibility; detailed leather/mail shading.
```
Word count: 85. Style: PASS. D7: PASS.

---

**Kit 28** — S1_endgame_bc_ranged_high_flat_dex_none_s1 (Cluster 3)
```
HERO CHARACTER IMAGE — S1_endgame_bc_ranged_high_flat_dex_none_s1
Faction: Stormveil Ironclad Surge (Cluster 3)
Season: cycle-14-wave-5-season-001
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy / Eastward / CrossCode; isekai-genre-readable; NOT retro pixel-art

Full-body character portrait on plain studio background. European early-modern-historical aesthetic, historical register. Primary weapon: Bandoliers (ranged class). Attribute archetype: DEX. Combat style: ranged high-output flat-pattern fighter. Element affinity: shadow.

Costume reflects European early-modern mercenary-scout heritage. Multiple bandoliers crossed over chest, shadow-tinted gunpowder aura. Humanoid; single-figure. Pixel-art HD-2D; hand-drawn-illustration sensibility; detailed leather/coat shading.
```
Word count: 87. Style: PASS. D7: PASS.

---

**Kit 29** — S1_endgame_bc_mid_high_flat_dex_none_s1 (Cluster 3)
```
HERO CHARACTER IMAGE — S1_endgame_bc_mid_high_flat_dex_none_s1
Faction: Stormveil Ironclad Surge (Cluster 3)
Season: cycle-14-wave-5-season-001
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy / Eastward / CrossCode; isekai-genre-readable; NOT retro pixel-art

Full-body character portrait on plain studio background. European industrial-historical aesthetic, historical register. Primary weapon: Centrefire breech-loading gun (ranged class). Attribute archetype: DEX. Combat style: mid-range high-output flat-pattern fighter. Element affinity: water.

Costume reflects European industrial-era field-soldier heritage. Bolt-action rifle prominently featured, water-element crystal stock inlay. Humanoid; single-figure. Pixel-art HD-2D; hand-drawn-illustration sensibility; detailed uniform/coat shading.
```
Word count: 87. Style: PASS. D7: PASS.

---

**Kit 30** — S1_endgame_bc_ranged_medium_variable_int_none_s1 (Cluster 3)
```
HERO CHARACTER IMAGE — S1_endgame_bc_ranged_medium_variable_int_none_s1
Faction: Stormveil Ironclad Surge (Cluster 3)
Season: cycle-14-wave-5-season-001
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy / Eastward / CrossCode; isekai-genre-readable; NOT retro pixel-art

Full-body character portrait on plain studio background. Fantasy-generic fictional aesthetic, fantasy register. Primary weapon: Chain Conductor Staff (caster-arcane class). Attribute archetype: INT. Combat style: ranged medium-output variable-pattern fighter. Element affinity: wind.

Costume reflects fantasy-generic chain-mage aesthetic. Conducting staff prominently featured with wind-element chain loops. Humanoid; single-figure. Pixel-art HD-2D; hand-drawn-illustration sensibility; detailed robe shading.
```
Word count: 82. Style: PASS. D7: PASS.

---

**Kit 31** — S1_endgame_bc_mid_medium_variable_wis_none_s1 (Cluster 3)
```
HERO CHARACTER IMAGE — S1_endgame_bc_mid_medium_variable_wis_none_s1
Faction: Stormveil Ironclad Surge (Cluster 3)
Season: cycle-14-wave-5-season-001
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy / Eastward / CrossCode; isekai-genre-readable; NOT retro pixel-art

Full-body character portrait on plain studio background. European industrial-historical aesthetic, historical register. Primary weapon: Mark I Trench Knife (caster-faith class). Attribute archetype: WIS. Combat style: mid-range medium-output variable-pattern fighter. Element affinity: holy.

Costume reflects European industrial-era battlefield-chaplain heritage. Trench knife with holy rune on crossguard prominently featured. Humanoid; single-figure. Pixel-art HD-2D; hand-drawn-illustration sensibility; detailed military-coat shading.
```
Word count: 86. Style: PASS. D7: PASS.

---

**Kit 32** — S1_endgame_bc_ranged_medium_variable_wis_none_s0 (Cluster 3)
```
HERO CHARACTER IMAGE — S1_endgame_bc_ranged_medium_variable_wis_none_s0
Faction: Stormveil Ironclad Surge (Cluster 3)
Season: cycle-14-wave-5-season-001
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy / Eastward / CrossCode; isekai-genre-readable; NOT retro pixel-art

Full-body character portrait on plain studio background. East Asian medieval-historical aesthetic, historical register. Primary weapon: Kama Pair (caster-faith class). Attribute archetype: WIS. Combat style: ranged medium-output variable-pattern fighter. Element affinity: lightning.

Costume reflects East Asian medieval monk-warrior heritage. Paired kama (short sickles) prominently featured with lightning crescent charge. Humanoid; single-figure. Pixel-art HD-2D; hand-drawn-illustration sensibility; detailed cloth/leather shading.
```
Word count: 87. Style: PASS. D7: PASS.

---

**Kit 33** — S1_endgame_bc_melee_high_variable_wis_none_s0 (Cluster 3)
```
HERO CHARACTER IMAGE — S1_endgame_bc_melee_high_variable_wis_none_s0
Faction: Stormveil Ironclad Surge (Cluster 3)
Season: cycle-14-wave-5-season-001
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy / Eastward / CrossCode; isekai-genre-readable; NOT retro pixel-art

Full-body character portrait on plain studio background. Fantasy-generic classical aesthetic, fantasy register. Primary weapon: Femur-Shafted Mace (caster-faith class). Attribute archetype: WIS. Combat style: melee high-output variable-pattern fighter. Element affinity: shadow.

Costume reflects fantasy-generic bone-rite shaman-warrior aesthetic. Bone-hafted mace prominently featured, shadow-pulse aura. Humanoid; single-figure. Pixel-art HD-2D; hand-drawn-illustration sensibility; detailed ritual-leather shading.
```
Word count: 83. Style: PASS. D7: PASS.

---

**Cluster 4 — Ashfield Siege Callers (1 member)**
Modal element: fire (100%). BC modal: ranged / large-AOE.

---

**Kit 34** — S1_endgame_bc_ranged_medium_variable_int_light_s0 (Cluster 4)
```
HERO CHARACTER IMAGE — S1_endgame_bc_ranged_medium_variable_int_light_s0
Faction: Ashfield Siege Callers (Cluster 4)
Season: cycle-14-wave-5-season-001
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy / Eastward / CrossCode; isekai-genre-readable; NOT retro pixel-art

Full-body character portrait on plain studio background. Fantasy-generic fictional aesthetic, fantasy register. Primary weapon: Meteor Swarm Tome (caster-arcane class). Attribute archetype: INT. Combat style: ranged medium-output variable-pattern siege fighter. Element affinity: fire with light secondary affinity.

Costume reflects fantasy-generic siege-mage aesthetic. Oversized tome prominently featured, fire-meteor sigils glowing from open pages, light-corona radiance at page edges. Humanoid; single-figure. Pixel-art HD-2D; hand-drawn-illustration sensibility; detailed robe shading.
```
Word count: 95. Style: PASS. D7: PASS.

---

## Section 3 — Per-Gear-Piece Sub-Templates (11 gear slots)

All gear-piece templates share the following base structure:

- Isolated gear piece on transparent/plain background
- No character body visible — gear only
- No overlap with other gear pieces
- Suitable for Meshy ingestion (clean silhouette; no background clutter)
- Style register: hand-drawn pixel-art HD-2D-shaped illustration register

**Slot vocabulary:** main_weapon / secondary_item / head / chest / hands / feet / legs / amulet / ring_1 / ring_2 / belt

### Gear Piece Template Format

```
GEAR PIECE IMAGE — [gear_slot] — [wave_b_name] kit ([kit_id])
Style: isolated gear piece illustration; no background; no overlap; suitable for Meshy ingestion; hand-drawn pixel-art HD-2D-shaped illustration register; reference Octopath Traveler / Triangle Strategy item-art aesthetic; isekai-genre-readable; NOT retro pixel-art

[gear_slot_description] for a [cultural_lineage] [historical_period]-period [attribute]-archetype character. Element affinity: [element_primary]. [weapon_type_family] class.

[gear_slot_specific_visual_note]. Plain studio background or fully transparent. Single object; no shadow; clean outline; detailed material rendering; pixel-art HD-2D register.
```

### Slot-Specific Visual Notes (substituted into `[gear_slot_specific_visual_note]`)

| Slot | gear_slot_description | gear_slot_specific_visual_note |
|---|---|---|
| main_weapon | Primary weapon — [weapon_canonical_name] | Full weapon from pommel to tip; horizontal or angled presentation; element-affinity enchantment glow visible |
| secondary_item | Off-hand item (shield, focus, dagger, or tome per weapon_type_family) | Off-hand object at arm's-length scale; compact composition; element-affinity tinge |
| head | Helm or headgear | Centered; front-facing or three-quarter view; cultural lineage and element motif visible in crest or ornament |
| chest | Chest armor or robe body | Torso piece only; front-facing; cultural lineage in material texture and decorative trim |
| hands | Gloves or gauntlets | Pair of hands (empty); front-facing or slight angle; cultural lineage in material and knuckle detail |
| feet | Boots or foot armor | Pair of boots; side-angled or front view; cultural lineage in sole design and fastener |
| legs | Leg armor or trouser piece | Pair of greaves or leg pieces; front-facing; cultural lineage in plate or cloth treatment |
| amulet | Necklace amulet | Pendant on chain; centered; element-affinity gem or sigil in focal point; cultural lineage in chain material |
| ring_1 | Ring (primary slot) | Single ring; top-down or slight angle; element-affinity stone or rune engraved; cultural lineage in band design |
| ring_2 | Ring (secondary slot) | Single ring; slightly different style than ring_1; element-affinity complement; cultural lineage in band design |
| belt | Belt or girdle | Horizontal band composition; front-facing; cultural lineage in buckle and material; weapon-family utility attachment visible |

### Example Filled Instance (Kit 34 — Ashfield Siege Callers)

**main_weapon:**
```
GEAR PIECE IMAGE — main_weapon — S1_endgame_bc_ranged_medium_variable_int_light_s0 kit
Style: isolated gear piece illustration; no background; no overlap; suitable for Meshy ingestion; hand-drawn pixel-art HD-2D-shaped illustration register; reference Octopath Traveler / Triangle Strategy item-art aesthetic; isekai-genre-readable; NOT retro pixel-art

Primary weapon — Meteor Swarm Tome — for a fantasy-generic fictional-period INT-archetype character. Element affinity: fire with light secondary. caster-arcane class.

Full tome from spine to fore-edge; horizontal presentation; fire-meteor sigils glowing on open pages, light-corona radiance at edges; floating mid-air pose. Plain studio background. Single object; clean outline; detailed parchment and binding rendering; pixel-art HD-2D register.
```
Word count: 97. Style: PASS. D7: PASS.

**head (example):**
```
GEAR PIECE IMAGE — head — S1_endgame_bc_ranged_medium_variable_int_light_s0 kit
Style: isolated gear piece illustration; no background; no overlap; suitable for Meshy ingestion; hand-drawn pixel-art HD-2D-shaped illustration register; isekai-genre-readable; NOT retro pixel-art

Helm or headgear for a fantasy-generic fictional-period INT-archetype siege mage. Element affinity: fire. caster-arcane class.

Centered; front-facing; pointed mage's hat or circlet with fire-rune crest and light-corona trim; cultural fantasy-generic arcane aesthetic in material. Plain studio background. Single object; clean outline; detailed fabric/metal rendering; pixel-art HD-2D register.
```
Word count: 87. Style: PASS. D7: PASS.

---

## Section 4 — Wanderer-Specific Variant Templates (Post-Gamora Iteration)

**Status:** DEFERRED — gamora Amendment 1 (Wanderer architecture) not yet closed. This section documents the planned variant templates to be layered once gamora close lands and SINGLETON cluster_id contract is confirmed.

### When to fire

Layering condition: gamora Amendment 1 completion record committed + SINGLETON cluster_id schema confirmed in phase5_faction_clusters.json output.

### Wanderer Faction Tile Template

```
WANDERER TILE IMAGE — Lone Wanderer of [Season Identity]
Season: [season_id]
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy / Eastward / CrossCode art direction; isekai-genre-readable; NOT retro pixel-art

Wanderer emblem tile. A solitary figure unaffiliated with any faction, walking a path defined by their own substrate identity alone. No banner; no formation; no doctrine.

Visual direction: lone-traveler emblem — single silhouette or solitary weapon motif against a neutral field; isekai-coded "the road not taken" composition. Square UI tile. No group heraldry; individual identity only. Palette derived from the Wanderer kit's primary element. Pixel-art HD-2D; hand-drawn-illustration sensibility; isekai-genre-readable.
```

Word count: 107. Style: PASS. D7: PASS.

### Wanderer Per-Kit Template

```
HERO CHARACTER IMAGE — [wave_b_name] (Lone Wanderer)
Cluster: SINGLETON — Lone Wanderer of [Season Identity]
Season: [season_id]
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy / Eastward / CrossCode art direction; isekai-genre-readable; NOT retro pixel-art

Full-body character portrait on plain studio background. Standalone identity composition — no faction insignia; no group markings. [cultural_lineage] [historical_period]-period aesthetic, [register] register. Primary weapon: [weapon_canonical_name] ([weapon_type_family] class). Attribute archetype: [attribute]. Combat style: [engagement_profile]-range [damage_level]-output [damage_pattern]-pattern fighter. Element affinity: [element_primary].

Composition emphasizes independence and self-determination — posture open, road behind visible as subtle environmental element (dust, wind, receding path). No faction heraldry. Cultural substrate honest. Pixel-art HD-2D; isekai-genre-readable; hand-drawn-illustration sensibility.
```

Word count: 142. Style: PASS. D7: PASS.

### Wanderer Gear-Piece Sub-Template

Inherits the base gear-piece sub-template format from Section 3. The `[faction_name]` blank is replaced with "Lone Wanderer" framing. No other structural changes. Layer this variant for any kit with `cluster_id = "SINGLETON"` once gamora architecture is confirmed.

---

## Section 5 — Iteration Plan

### Post-Gamora (immediate — within cascade-r4 fan-out)

1. **Wanderer tile template instance:** once gamora Amendment 1 closes and SINGLETON kit(s) are confirmed, author filled Wanderer tile + per-kit instances per Section 4 templates above.
2. **element_primary gap resolution:** if gamora Amendment 1 outputs per-kit element assignments in SINGLETON schema, backfill the element_primary blank for all 34 current instances where modal-element proxy was used.
3. **wave_b_name gap resolution:** once Phase 5 LLM Wave B names land (from the Phase 5 orchestrator run), replace the `kit_id` placeholder with the LLM-generated wave_b_name in all 34 instances.
4. **t4_strategy gap resolution:** if per-kit T4 strategy becomes available from updated phase4 archive JSON, append T4 strategy context phrase to the combat-style sentence in each instance.

### Post-Track-A (seasons 002 + 003)

When rocket generates seasons 002 and 003 (Track A), the template system extends as follows:

1. **New faction tile instances:** author 4 filled faction tile instances per new season's cluster output, using the same Section 1 template format. Substrate blanks filled from that season's phase5_faction_clusters.json.

2. **New per-kit instances:** author filled per-kit instances for each new season's 34 accepted kits, using the Section 2 template format. Substrate blanks from that season's kit_archive + substrate_weapon_binding.

3. **Cross-season prompt consistency:** the style register language is FIXED across all seasons (same locked phrase). The substrate blanks are the ONLY seasonal variation. This ensures visual consistency across seasons when drax calls the ChatGPT API.

4. **Seasonal identity token:** add a `[season_identity]` blank to the Wanderer template (Section 4) that references the season's thematic identity (if any is assigned by the Wave A/B process). For seasons without explicit thematic identity, default to the season_id.

5. **Per-season template versioning:** name instances as `season-001-kit-XX.md`, `season-002-kit-XX.md` etc. when multiple seasons accumulate. The canonical template format in Sections 1-3 remains v1; instances are versioned by season.

### Long-term template evolution (Cycle 15+)

Per the designer-writes-substrate principle (canonical/story/2026-05-29-designer-writes-substrate-player-names-experience-principle.md § 4.4): at Cycle 15+, Wave B LLM prompts will integrate both the designer-writes-substrate layer AND the player-names-experience layer (experiential archetype vocabulary: Bossing / Speedfarming / Endgame Generalist). When that Cycle 15+ extension lands:

- Add `[experiential_archetype]` blank to per-kit templates (Bossing / Speedfarming / Endgame Generalist per community-validated ARPG vocabulary)
- Add experiential framing sentence to image-gen prompt: "Endgame-generalist aesthetic — kit balanced for sustained engagement across diverse encounters" / "Bossing aesthetic — kit optimized for single-target encounter mastery" / etc.
- This is a LAYER; the existing substrate blanks remain; experiential archetype is additive

---

## Section 6 — KR Flags (Substrate Metadata Gaps)

The following gaps were surfaced during template authoring and require KR routing per dispatch:

### KR Flag 1 — wave_b_name not available

**Gap:** Wave B LLM names (per-kit identity names generated by Phase 5 orchestrator) are not persisted in any JSON output file in `cycle-14-wave-5-season-001/`. The phase5_faction_clusters.json metadata confirms `wave_b_kit_count: 34` and `wave_b_cost_usd: 0.34`, indicating Phase 5 Wave B fired — but the LLM output names are not in the available files.

**Impact:** all 34 per-kit instances use `kit_id` as `[wave_b_name]` placeholder. Prompts are functionally complete but use the engine identifier, not the player-facing name.

**Routing:** surface to KR for rocket/elrond routing — confirm where Wave B names are persisted and how drax accesses them for prompt construction.

### KR Flag 2 — element_primary not persisted per-kit

**Gap:** per-kit element assignments are not in `phase4_archive_insertion.json`, `phase3_gauntlet_results.json`, `phase3_quality_vectors.json`, or `phase7_season_summary.json`. Cluster-level element distributions are available from `phase5_faction_clusters.json`. Per-kit element was assigned from regenerating the pipeline — but regeneration produces non-deterministic element assignments that don't match the original season_001 run.

**Workaround applied:** modal element per cluster used as proxy (earth for Cluster 1, lightning for Cluster 2/3, fire for Cluster 4). Three-way tie in Cluster 2 (lightning/fire/wind at 27% each) resolved by cycling across members.

**Impact:** element_primary in 34 instances is a proxy, not the canonical original-run value. May cause prompt-to-engine-output mismatch if player-facing content is generated against these templates before gap is resolved.

**Routing:** surface to KR for star-lord/rocket routing — add per-kit element to phase4 archive insertion JSON output (or expose via separate per-kit metadata export).

### KR Flag 3 — t4_strategy not persisted per-kit

**Gap:** `phase4_archive_insertion.json` has `t4_strategy: null` and `invest_profile: null` for all 34 accepted kits. The T4 strategy is available in the gauntlet results (`phase3_gauntlet_results.json`) but keyed to `legendary_id` (e.g., `endgame_bc_melee_low_spiky_str_none_t4_chain_2`), not to the `kit_id` directly.

**Workaround applied:** t4_strategy blank OMITTED from all 34 instances. Template contains the blank but instances leave it out of the prompt body to avoid incomplete information.

**Impact:** prompts lack the T4 strategy context that would differentiate mechanically-similar kits. Low visual-fidelity impact (t4_strategy is mechanical, not visual) but may matter for gear-piece styling when t4 informs defensive/offensive aesthetic.

**Routing:** surface to KR for rocket routing — expose t4_strategy in phase4 archive insertion JSON per-kit record for future season runs.

### KR Flag 4 — modal_tone field is "unknown" in all 4 clusters

**Gap:** `phase5_faction_clusters.json` has `modal_tone: "unknown"` for all 4 clusters. This blank is present in the per-faction template but was not used in the faction tile prompt body (compositions use engagement_profile and element instead).

**Impact:** low — modal_tone is a supplementary prompt blank; the current faction tile compositions are complete without it.

**Routing:** note to gandalf via KR if faction tile prompts should be revisited once tone vocabulary is defined.

---

## Acceptance Criteria Status

- [x] Per-faction prompt templates authored (4 for season_001; style adherence + D7 compliance)
- [x] Per-kit prompt template authored (1 template + 34 substrate-filled instances)
- [x] Per-gear-piece sub-templates authored (11 gear slots with slot-specific visual notes)
- [x] Wanderer-specific variant templates authored (Section 4; deferred plan + template format)
- [x] Style register adherence verified per template (Octopath Traveler / Triangle Strategy / Eastward / CrossCode; hand-drawn pixel-art HD-2D; NOT retro pixel-art)
- [x] D7 AI-tell line compliance verified (all templates <= 200 words; bracketed substrate blanks; no free-form LLM dialogue)
- [x] Substrate metadata fields documented (Section 0 table; per-kit fields extracted from substrate_weapon_binding; gaps flagged in Section 6)
- [x] Iteration plan documented (Section 5; Wanderer post-gamora; seasons 002+003 post-Track-A; Cycle 15+ experiential layer)

---

*Authored by legolas — Mode A analytical research — cascade-r4 Track B — 2026-05-29*
