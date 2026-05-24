# Off-Hand Items — Reincarnated v1 Operational Definition

> **STATUS:** CURRENT — PROPOSED operational definition for off-hand items as substrate sub-category in v1 pipeline. Authored as Cycle 10 Sidecar B canonical reference per Matt 2026-05-24 Stage 0 design dialogue (Custer-with-Art-of-War scenario surfacing).

**Date:** 2026-05-24
**Author:** gandalf (story-and-design steward)
**Status:** ACTIVE — locks off-hand items inclusion in v1 pipeline; 6 categories enumerated; schema-extension approach (Approach B single-table); Phase 5 two-item cohesion-coalescence discipline extends existing 3-tier named-bearer pattern
**Authority:** Matt 2026-05-24 — Cycle 10 Sidecar B inclusion confirmation ("include and amend now")
**Companion docs:**
- `canonical/story/attribute-system-2026-05-24.md` (4-attribute system; off-hand items respect attribute coupling)
- `canonical/story/skill-system-2026-05-24.md` (Phase 2 skill composition; § 12.3 named-bearer discipline extends to two-item case per § 6 below)
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` (BC axes; off-hand items have distinct mechanical-axis profile from weapons)
- `canonical/story/qd-engine-end-to-end-workflow-2026-05-21.md` (Phase 2 generation pulls off-hand items alongside weapons; Phase 5 cohesion handles two-item alignment)
- `canonical/story/v1-bc-target-intent-2026-05-24.md` (Stage 0 transcription; cells using off-hand items identified)
- `agentic_orchestration/gandalf/requests/2026-05-23-knight-rider-substrate-curation-multi-stage-dispatch.md` § Sidecar B (Cycle 10 substrate-curation execution territory)
- `~/Games/reincarnated-loadout/data/telemetry.db` (`weapon_knowledge_entries` schema extension target)

---

## 0. TL;DR

Reincarnated v1 includes **off-hand items** as a substrate sub-category alongside main weapons. Six categories enumerated:

1. **Shield** — defensive-stance + block-mechanic; cardinal off-hand for tank/paladin/warrior forms
2. **Tome** — tactical-buff + aura-effect + spell-amp; for caster/spellsword/strategist forms
3. **Banner / Standard** — proxy-buff + faction-aura + leadership-amp; for proxy-heavy + faction-anchored forms
4. **Focus / Orb / Talisman** — element-amp + cast-amp + ritual-amp; for caster + ritualist + channel forms
5. **Horn / Signaling-implement** — proxy-call + tempo-shift + war-cry-amp; for proxy + buff-leaning forms
6. **Off-hand weapon** — second weapon for dual-wield; uses main-weapon schema with off-hand slot tag

Schema approach: **Approach B (single-table)** — extend `weapon_knowledge_entries.weapon_kind` enum to include off-hand categories; same schema; off-hand items get tagged differently but use same row structure as weapons.

Two-item cohesion-coalescence discipline at Phase 5 extends existing 3-tier named-bearer pattern (per skill-system § 12.3) with cross-item alignment scoring. Cross-cultural bifurcation accepted as feature when genre-coherent (Custer + Sun Tzu Art of War); rejected as bug when nonsensical (cohesion judge drops to engine-named-original).

Substrate-sourcing via Cycle 10 Sidecar B: ~1,400-5,500 off-hand items estimated (mostly existing-source mining from royal_armouries + Met Museum + Wikipedia + Wikidata; targeted Mode B crawl supplements gaps).

---

## 1. The six off-hand item categories

### 1.1 Shield

- **Mechanical profile:** defensive-stance + block-probability + damage-mitigation; some shields add offensive contribution (shield-bash; spike-shield)
- **Typical attribute coupling:** STR (heavy shields — tower, kite, heater) / DEX (light shields — buckler, parma, targe) / WIS (sacred shields — Aegis, paladin holy-shield)
- **Genre exemplars:** D2 Paladin holy-shield (Hammerdin signature); D3 Crusader Phalanx-shield; PoE Bone Offering shield; Last Epoch Sentinel-shield builds
- **Substrate-source coverage:** RICH — royal_armouries + Met Museum + Wikipedia carry ~500-2,000 historical/cultural shields
- **Tier-S/A named exemplars (per cultural tradition):**
  - European: Aegis (Greek; goatskin shield of Athena/Zeus); Pridwen (Arthur's shield)
  - Norse: Svalin (Sun's shield); Skjold (Viking shield)
  - Greek: Aegis (canonical); Pelta (light cavalry shield)
  - Japanese: Tate (samurai shield — though uncommon in Japanese-folklore)
  - Various cultural-tradition shields with named-bearer attribution

### 1.2 Tome / Book / Treatise

- **Mechanical profile:** tactical-buff (battle-knowledge); spell-amplification (arcane-tome); aura-effect (knowledge-aura); information-passive (treatise-passive)
- **Typical attribute coupling:** INT (arcane tomes — grimoires, spellbooks) / WIS (ritual texts — holy books, scriptures) / DEX or STR (tactical treatises — Art of War, military manuals)
- **Genre exemplars:** D2 Necromancer wand-and-tome; D3 Wizard source; PoE Witch tome-and-wand; D&D wizard spellbook
- **Substrate-source coverage:** RICH — Wikipedia + Wikidata + targeted crawl carry ~500-1,500 tactical/magical/sacred texts
- **Tier-S/A named exemplars:**
  - Tactical: The Art of War (Sun Tzu); De Re Militari (Vegetius); On War (Clausewitz); Hagakure (Yamamoto)
  - Arcane: Necronomicon (Lovecraftian fictional but broadly recognized); Liber AL vel Legis; Lemegeton (Lesser Key of Solomon — careful with religious sensitivity)
  - Sacred: various sacred texts (TIER 3 — broadly excluded per Q-B § 3.2 cultural-sensitivity discipline; substrate carries for reference, not for player-facing form naming)
  - Historical philosophical: Meditations (Marcus Aurelius); The Prince (Machiavelli)

### 1.3 Banner / Standard / Flag

- **Mechanical profile:** proxy-buff (rally-aura for minions/summons); faction-aura (faction-identity-broadcast); leadership-amp (multi-actor coordination boost)
- **Typical attribute coupling:** STR (military banners) / WIS (sacred standards) / Generic (faction emblems)
- **Genre exemplars:** PoE Spirit Banner / War Banner (totem-like proxy-buff); D3 Crusader Phalanx-banner (proxy-buff); D4 Necromancer banner; many strategy games' standard-bearer-units
- **Substrate-source coverage:** SMALL — military museums + heraldry sources carry ~100-500 named historical banners; gap area for v1
- **Tier-S/A named exemplars:**
  - European: Oriflamme (French royal banner); Raven Banner (Viking); Roman Aquila (legion eagle standard)
  - Japanese: Sashimono (clan banners); Hata-jirushi (samurai standards); Nobori (war-banner)
  - Mongol: Tugh (horsetail standard)
  - Various clan/family heraldic banners

### 1.4 Focus / Orb / Talisman

- **Mechanical profile:** element-amplification (per-element cast-bonus); cast-amp (general spell-speed/damage); ritual-amp (channel-stability + duration-extension)
- **Typical attribute coupling:** INT (arcane focuses) / WIS (ritual talismans) / Cross-attribute (cultural-tradition talismans)
- **Genre exemplars:** D2 Sorceress orb; D3 Wizard source; PoE focus-and-wand combos; LE Acolyte catalyst; D&D wizard arcane focus
- **Substrate-source coverage:** MEDIUM — Wikipedia + Wikidata + ritual-object substrate carry ~200-1,000 named focuses/talismans
- **Tier-S/A named exemplars:**
  - European: Philosopher's Stone (alchemical fictional but iconic); Holy Grail (Tier 1 mythological but careful with religious sensitivity); various crystal-orb traditions
  - East Asian: Magatama (Japanese sacred jewel — careful with religious sensitivity); various jade artifacts
  - Greek/Mediterranean: Hand of Sabazios; various amulets
  - Various cultural-tradition focuses with named-bearer attribution

### 1.5 Horn / Signaling-implement

- **Mechanical profile:** proxy-call (summon-trigger or proxy-buff-pulse); tempo-shift (speed-boost cycles); war-cry-amp (battle-cry / damage-buff aura)
- **Typical attribute coupling:** STR (war-horns) / WIS (ritual-horns) / Cross-attribute (cultural-tradition horns)
- **Genre exemplars:** D2 Barbarian war-cries (no explicit horn item but mechanism similar); PoE Berserker call-of-battle; LE Primalist howl-passives; Diablo 3 Crusader battle-shout
- **Substrate-source coverage:** SMALL — military + ceremonial substrate carry ~100-500 named historical horns
- **Tier-S/A named exemplars:**
  - European: Gjallarhorn (Heimdall's horn; Tier 1 mythological); Oliphant (Roland's horn; per Song of Roland); Olifant (medieval war-horn)
  - Mesoamerican: Pututu (Andean conch-trumpet)
  - Various Bronze Age battle-horns; Roman cornu; Greek salpinx

### 1.6 Off-hand weapon (dual-wield secondary)

- **Mechanical profile:** secondary weapon for dual-wield builds; same mechanical schema as main weapon (range / tempo / amplitude / geometry / attribute)
- **Typical attribute coupling:** matches main-weapon attribute (DEX-DEX dual-dagger; STR-STR dual-sword; INT-INT dual-wand)
- **Genre exemplars:** D2 Assassin twin-claws; D3 Crusader sword-and-sword; PoE Slayer dual-wield; D4 Rogue dual-blades
- **Substrate-source coverage:** RICH (uses existing weapon substrate; just tagged with off-hand slot capability)
- **Tier-S/A named exemplars:**
  - Dyrnwyn (Welsh sword, sometimes paired with off-hand)
  - Various paired/twin-weapon traditions
  - Most dual-wield comes from PAIR-PATTERN (player carries two of same weapon-family) rather than from named-pair canon

---

## 2. Schema integration — Approach B (single-table extension)

### 2.1 Schema change

```sql
ALTER TABLE weapon_knowledge_entries
DROP CONSTRAINT IF EXISTS check_weapon_kind;
ALTER TABLE weapon_knowledge_entries
ADD CONSTRAINT check_weapon_kind CHECK (
  weapon_kind IN (
    -- Original categories
    'category', 'unique', 'named_template', 'ammo_or_consumable',
    -- Off-hand item categories (added 2026-05-24 per Cycle 10 Sidecar B)
    'shield', 'tome', 'banner', 'focus', 'horn', 'talisman',
    -- Unknown
    'unknown'
  )
);
```

(Elrond seam executes ALTER as part of Cycle 10 Sidecar B.)

### 2.2 Off-hand slot tagging

Add new column to indicate slot-eligibility:

```sql
ALTER TABLE weapon_knowledge_entries
ADD COLUMN slot_eligibility TEXT DEFAULT 'main_only' CHECK (
  slot_eligibility IN ('main_only', 'off_hand_only', 'either', 'unknown')
);
```

- `main_only` — most weapons; cannot be equipped in off-hand slot
- `off_hand_only` — shields, banners, large tomes that can ONLY be off-hand
- `either` — daggers, small focuses, light weapons that can be either main or off-hand (dual-wield friendly)
- `unknown` — substrate-curation pending classification

### 2.3 Off-hand mechanical-axis profile (Cycle 10 Stage 4 schema gap closure)

Off-hand items have different mechanical-axis profile than main weapons. Extend `weapon_sim_props` or add `off_hand_sim_props`:

```sql
ALTER TABLE weapon_sim_props
ADD COLUMN off_hand_buff_geometry TEXT, -- 'aura' / 'self_buff' / 'target_buff' / 'zone_buff' / 'none'
ADD COLUMN off_hand_aura_tempo TEXT,    -- 'constant' / 'cycled' / 'triggered' / 'none'
ADD COLUMN off_hand_defensive_stance REAL, -- 0.0-1.0 defensive contribution (shields)
ADD COLUMN off_hand_focus_element_affinity TEXT; -- 'fire' / 'water' / 'all_elements' / 'none'
```

These axes are populated at Cycle 10 Stage 4 per Discipline #18 methodology consult (legolas Mode A ~30-60 min on off-hand-mechanical-profile patterns).

---

## 3. Per-cell off-hand usage (from Stage 0 transcription)

Per `canonical/story/v1-bc-target-intent-2026-05-24.md` cell roster, cells that USE off-hand items in v1:

| Cell | Off-hand type | Example form |
|---|---|---|
| `(melee, medium, variable, STR, none)` Polearm Soldier | shield (occasionally) | Roman legionary with scutum |
| `(melee, high, flat, STR, none)` Light Fighter | shield (commonly) | Hoplite with aspis |
| `(melee, medium, variable, WIS, none)` Holy Knight / Paladin | shield (commonly); holy-symbol/horn (occasionally) | Hammerdin with holy-shield; Crusader with banner |
| `(melee, high, flat, DEX, none)` Dagger Assassin | off-hand dagger (dual-wield); buckler (occasionally) | D2 Assassin twin-claws; PoE dual-dagger Slayer |
| `(mid, high, flat, DEX, none)` Twin-Blade Fencer | off-hand weapon (dual-wield) | D2 Bowazon variant; KonoSuba light-fencer |
| `(ranged, medium, variable, INT, none)` Standard Wizard | focus/orb (commonly); tome (occasionally) | D2 Sorc with orb; D3 Wizard source |
| `(ranged, low, spiky, INT, none)` Artillery Mage | focus/orb; tome | D2 Sorc Frozen Orb with magic-find orb |
| `(melee, high, flat, INT, none)` Red Mage / Spellsword | focus + dagger (dual-wield-mage); tome + sword | Eldritch Knight with arcane focus + sword |
| `(mid, low, spiky, INT, heavy)` Necromancer Summoner | tome (necromancy-tome); banner (proxy-buff) | D2 Necro with bone-shield + wand+tome combo |
| `(mid, medium, variable, INT, heavy)` Totem Hierophant | totem-focus | PoE Hierophant with totem-focus |
| `(mid, medium, variable, WIS, none)` Channeling Cleric | holy-symbol; focus | D3 Witch Doctor with mojo; D2 Druid pelt |
| `(ranged, low, spiky, WIS, none)` Ritual Mage / Oracle | ritual-focus; tome | D2 Druid pelt; oracle-implement |
| `(ranged, medium, variable, WIS, none)` Storm Caller / Druid | focus; horn (occasional) | Druid with pelt + horn |
| `(mid, low, variable, WIS, heavy)` Druid Beastmaster | horn (animal-call); banner | LE Primalist Beastmaster with horn |
| `(mid, medium, variable, WIS, heavy)` Witch Doctor Petmaster | mojo (focus); banner (proxy-buff) | D3 WD with mojo |

Cells NOT typically using off-hand:
- `(melee, low, spiky, STR, none)` Heavy Barbarian — two-handed weapon
- `(ranged, low, spiky, STR, none)` Thrown-Heavy — thrown weapon set
- `(ranged, high, flat, DEX, none)` Archer — bow (two-handed)
- `(ranged, low, spiky, DEX, none)` Crossbow Sniper — crossbow (two-handed for heavy crossbows)
- `(melee, high, variable, WIS, none)` Monk-archetype — unarmed or staff (two-handed)
- `(mid, low, spiky, DEX, heavy)` Trap Assassin — traps/mines (no off-hand needed)
- `(melee, low, spiky, STR, light)` Ancestor-Warrior — two-handed weapon
- `(ranged, high, flat, DEX, light)` Falconer — bow + falcon (falcon as proxy, no off-hand)
- `(ranged, medium, variable, INT, light)` Arcane-Familiar Mage — staff (two-handed)

**Approximate v1 cell coverage using off-hand:** ~15 cells of 22 = ~68% of cells use off-hand items. Estimated ~25-30 forms with off-hand support.

---

## 4. Cycle 10 Sidecar B execution

### 4.1 Substrate-sourcing approach

| Step | Description | Owner | Cost |
|---|---|---|---|
| 1 | Existing-source mining (royal_armouries + Met Museum + Wikipedia + Wikidata) for shield + tome + banner + focus + talisman + horn | elrond | ~half-day |
| 2 | Schema extension (ALTER TABLE per § 2) | elrond | ~30 min |
| 3 | Reclassify mined items per weapon_kind enum extension | elrond | ~2-4 hrs |
| 4 | Targeted legolas Mode B crawl for category-coverage gaps (tactical-treatises; ritual-implements; named-mythological focuses) | legolas | ~1 day |
| 5 | Mechanical-axis tagging (off-hand-specific axes; Discipline #18 consult) | rocket + gamora + jack-ryan Gate-2 | Folds into Cycle 10 Stage 4 |
| 6 | Tier S/A/B/C assignment (composite quality scoring) | elrond + gandalf | Folds into Cycle 10 Stage 2.5 |

### 4.2 Substrate-coverage targets

| Category | Estimated v1_scope rows | Source notes |
|---|---|---|
| Shield | 200-400 | Mostly from royal_armouries + Met Museum mining |
| Tome | 150-300 | Mix of mining + targeted crawl for tactical-treatises |
| Banner | 50-150 | Gap area; needs targeted crawl |
| Focus / Talisman | 100-200 | Mining + targeted crawl |
| Horn | 50-100 | Gap area; needs targeted crawl |
| Off-hand weapon (dual-wield secondary) | (uses main weapon substrate; tagged via slot_eligibility) | N/A new substrate |
| **TOTAL** | **~550-1,150 unique off-hand items in v1_scope** | |

---

## 5. Two-item Phase 5 cohesion-coalescence discipline (extension of skill-system § 12.3)

### 5.1 Extension of existing 3-tier named-bearer discipline

Per skill-system § 12.3 + Matt 2026-05-23 bi-modal revision (covered in skill-system doc), the existing named-bearer discipline extends naturally to two-item case:

```
Phase 5 cohesion coalescence (two-item case):
1. Score kit-MAIN-weapon alignment (cultural-tradition × kit element/skill)
2. Score kit-OFF-HAND alignment (cultural-tradition × kit element/skill)
3. Score CROSS-ITEM coherence (do both items' cultural-traditions co-occur in genre canon?)
4. If all three scores HIGH → name explicitly (Tier 1) or soft-attribution (Tier 2):
     - Both items' cultural-influences acknowledged in form-name + lore
     - Example: Custer + Sun Tzu Art of War + American Cavalry kit
       → "The Tactical Cavalryman of the Western Plains" (both cultural-influences acknowledged; named-person soft-attributed)
5. If primary HIGH, off-hand LOW → keep primary cultural-attribution, drop off-hand item-cultural-attribution
6. If both items LOW alignment with kit → engine-name from kit-shape alone (per bi-modal original-form pattern)
7. Cross-cultural bifurcation accepted when historically/genre-coherent
   (Custer + Sun Tzu; Caesar + Greek philosophy; Cleopatra + Roman amulet)
8. Cross-cultural bifurcation REJECTED when nonsensical
   (Custer + Mongol scimitar + scattered elements → cohesion judge drops both signals;
    engine-names form per kit-shape; per bi-modal pattern)
```

### 5.2 Cross-cultural bifurcation as feature when meaningful

Per Matt 2026-05-24 design dialogue + Fate-genre canon precedent:

| Example | Verdict | Reasoning |
|---|---|---|
| Custer (American Cavalry saber) + Art of War (Chinese tactical-tome) | FEATURE | Historically attested (Custer studied military classics); genre-coherent; bi-modal anchor for "Tactical Cavalryman" identity |
| Caesar (Roman gladius) + Greek philosophical-tome | FEATURE | Historically attested (Caesar was literate in Greek); genre-coherent |
| Saber Lily (Avalon Faerie scabbard) + Excalibur (Arthurian sword) | FEATURE | Fate-canon canonical-cross-tradition |
| Gilgamesh (Sumerian gate-of-weapons) + many cultural weapons | FEATURE | Fate-canon collection of cross-cultural weapons |
| Cleopatra (Egyptian uraeus) + Roman amulet | FEATURE | Historically attested cross-cultural fusion (Ptolemaic-Roman) |
| Random Custer + Mongol scimitar + Aztec drum | BUG | Nonsensical cross-cultural collision; no historical or genre-canon basis; cohesion judge drops to engine-named-original |

### 5.3 Algorithm § 8 extension for off-hand items

Algorithm at skill-system § 8 (algorithmic mechanic-alteration) extends to consider off-hand-item selection during Phase 2:

```
algorithm_output_for_kit_with_off_hand:
  alteration_type: (per § 7 palette)
  alteration_specific: (per algorithm output)
  manifestation: "T4_active_skill" | "rank2_passive" | "rank3_passive"
  bind_axis: (kit-specific)
  estimated_eta: (high-η candidate)
  thematic_anchor: (cultural-tradition-coherent)
  off_hand_selection: (substrate-resident off-hand item matching cell + cultural-tradition alignment)
  llm_naming_template: (Phase 5 templated naming)
```

Off-hand-item selection at Phase 2 respects cell-coverage floor per `canonical/story/v1-bc-target-intent-2026-05-24.md` Sketch B (~+30-50 off-hand items per cell using off-hand).

---

## 6. Decisions deferred to subsequent design calls

1. **Single off-hand slot vs two off-hand slots** — currently assumed single off-hand; dual-wield uses off-hand-slot for second weapon. Could expand to two off-hand slots (e.g., focus + talisman + main staff) but not v1 scope
2. **Per-category mechanical-axis-binning depth** — Cycle 10 Stage 4 work + Discipline #18 consult will refine bin granularity
3. **Named-mythological off-hand item seed list** — gandalf authors as part of Stage 2.5 quality scoring + Track M1-equivalent for off-hand items
4. **Per-form off-hand-item-required vs off-hand-item-optional** — some forms (Holy Knight) might MANDATE shield; others (Standard Wizard) might allow focus-or-tome flexibility. Stage 3 composition policy locks per-form

---

## 7. What this doc does NOT do

- NOT a substrate-curation execution doc — that's Cycle 10 Sidecar B (elrond + legolas) territory
- NOT a finalized off-hand-item mechanical-axis schema — Cycle 10 Stage 4 + Discipline #18 consult refine
- NOT an exhaustive substrate enumeration — substrate-source mining executes per Sidecar B
- NOT a player-facing UI spec — slot-display + equipping UI is downstream design work
- NOT a final lock — Cycle 10 Stage 3 composition policy may amend per-cell off-hand usage
- NOT a complete cohesion-judge spec — § 5 sketches the two-item discipline; full spec authored when cohesion-judge calibration (P5) fires
- NOT a Tier 3 sacred-object policy doc — Tier 3 discipline per Q-B § 3.2 applies; sacred-object substrate-curation review remains v1.1+ work

---

## 8. Cross-references

### Active project canon this doc grounds in
- `canonical/00-ground-state.md` § 1 (current truth oracle)
- `canonical/story/attribute-system-2026-05-24.md` (attribute coupling)
- `canonical/story/skill-system-2026-05-24.md` (§ 12.3 named-bearer discipline; § 8 algorithm extension)
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` (BC axes; off-hand mechanical-axis profile)
- `canonical/story/qd-engine-end-to-end-workflow-2026-05-21.md` (Phase 2 + Phase 5)
- `canonical/story/v1-bc-target-intent-2026-05-24.md` (Stage 0 transcription; cell-usage table)
- `agentic_orchestration/gandalf/requests/2026-05-23-knight-rider-substrate-curation-multi-stage-dispatch.md` § Sidecar B

### Live state references
- `~/Games/reincarnated-loadout/data/telemetry.db` (`weapon_knowledge_entries` + `weapon_sim_props` schema)

### Downstream artifacts this doc anchors
- Cycle 10 Sidecar B execution (substrate-sourcing + schema extension + mining)
- Cycle 10 Stage 4 mechanical-tagging (off-hand-axis tagging)
- T4-B v1 catalogue authoring (consumes off-hand-cell-usage table for per-T4-node off-hand spec)
- Future cohesion-judge spec (Phase 5 two-item alignment)
- Future Track M1-equivalent for named-mythological off-hand items

---

## 9. Sign-off

**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-05-24 — Cycle 10 Sidecar B inclusion confirmation
**Status:** CURRENT — PROPOSED operational definition; Cycle 10 Sidecar B execution + Stage 3 composition policy may amend
**Re-engagement gate:** Sidecar B execution lands → schema extension + initial substrate population; Cycle 10 Stage 3 design call locks per-cell off-hand usage policy

---

**Signed:** gandalf
**For:** the canonical operational definition of off-hand items as substrate sub-category in v1 pipeline. Six categories enumerated (shield + tome + banner + focus + horn + talisman + off-hand-weapon-for-dual-wield). Schema extension via Approach B (single-table). Two-item Phase 5 cohesion-coalescence discipline extends existing 3-tier named-bearer pattern. Cycle 10 Sidecar B execution reference.
