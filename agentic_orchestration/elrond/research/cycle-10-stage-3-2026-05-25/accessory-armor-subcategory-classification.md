# Cycle 10 Stage 3 — Phase 0a — Accessory + Armor Subcategory Classification

**Date:** 2026-05-25
**Owner:** elrond (lead — Phase 0a; Tier-S 255-row substrate subdivision)
**Dispatch:** `agentic_orchestration/dispatches/2026-05-24-elrond-cycle-10-stage-3-v1-scope-materialization.md` § 3.2 + § 4.1
**Composition policy:** `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` § 1.1 (D1a / D1b / D1c)
**Substrate DB:** `/Users/admin/Games/reincarnated-loadout/data/telemetry.db`
**Table:** `weapon_knowledge_entries`
**Column:** `weapon_kind_classified_subtype` (TEXT, nullable, no CHECK — populated only on Tier-S rows)
**Heuristic only — no LLM cost.**

---

## 0. TL;DR

Subdivided the 255 Tier-S `accessory` (130) + `armor` (125) rows per composition policy § 1.1 sub-enum schema. Final distribution:

| Subcategory | Count | Policy fate |
|---|---:|---|
| `accessory_handheld` | **8** | D1b allowed (auto-promote candidate; subject to Phase 0b parent-fit gate for `accessory_weapon_integrated` only — this bucket flows through unchanged) |
| `accessory_weapon_integrated` | **77** | D1b allowed (auto-promote candidate; subject to Phase 0b parent-weapon-family compatibility gate) |
| `accessory_horse_or_equipment` | **45** | D1c excluded (mounted-combat scope-creep; deferred to v1.1+) |
| `armor_shield` | **10** | D1b allowed (auto-promote) |
| `armor_body_or_head` | **115** | D1c excluded (character-armor-slot deferred to v1.1+) |
| **TOTAL** | **255** | |

D1b-allowed sum (`accessory_handheld` + `accessory_weapon_integrated` + `armor_shield`): **95** rows. Composition policy § 1.1 estimate was ~100-160; the empirical 95 sits just below the lower bound. **Implication for downstream v1_scope size:** D1b auto-promote contribution is ~95 not the ~130 midpoint the policy assumed. The ~1,700-3,100 v1_scope envelope is unaffected (single-digit-percentage shift); flagged for Phase 3 distribution report.

D1c-excluded sum (`accessory_horse_or_equipment` + `armor_body_or_head`): **160** rows. Policy estimate was ~105-145; empirical 160 is slightly above. **Implication:** more aggressive D1c routing than expected (driven by the `met:classification=Miscellaneous-Buckles & Ornament` cluster all being "Ornament of Horse Trapping" rows — see § 4.1).

---

## 1. Prerequisite state finding (Discipline #11 — empirical inspection)

The dispatch describes column `weapon_kind_classified_subtype` as "already populated on 1,126 Tier-S rows with parent categories `accessory`/`armor`/`handheld_weapon`/etc." Empirical check at session start: **the column does NOT exist in the DB.** The Stage 2.5 classifier wrote ONLY to JSON artifact `tier-s-classification.json`; no `ALTER TABLE` landed at Stage 2.5 (verified by reading `cycle-10-stage-2-5-2026-05-24/MIGRATION.md` § 1 — three columns added but none named `weapon_kind_classified_subtype`).

**Operational decision (autonomous, per Cycle 10 scope-doc § 1):** Phase 0a is now a three-step operation, not single UPDATE-in-place:

1. `ALTER TABLE weapon_knowledge_entries ADD COLUMN weapon_kind_classified_subtype TEXT` (nullable, no CHECK constraint)
2. Populate parent category for all 1,126 Tier-S rows from Stage 2.5 JSON (handheld_weapon / accessory / armor / siege_vehicle / art_object / other / ammo_consumable) — so the D1a auto-include rule (`weapon_kind_classified_subtype = 'handheld_weapon'`) referenced by Phase 2 sampler has a column to query
3. Subdivide the 255 accessory + armor rows per composition policy § 1.1 sub-enum

Three-step approach is the only way to honor (a) the dispatch's UPDATE-in-place language for the 255 rows AND (b) Phase 2's downstream dependency on `weapon_kind_classified_subtype = 'handheld_weapon'` covering all 449 Tier-S handheld_weapon rows. The alternative — leaving non-accessory/non-armor parent values un-materialized — would break Phase 2 sampler queries.

**Cross-seam impact unchanged:** still an additive column on `weapon_knowledge_entries`; same ADR-004 additive pattern as Stages 1 + 1.5 + 2.5. MIGRATION.md drafted at `cycle-10-stage-3-2026-05-25/MIGRATION.md`.

**Surfaced back via dispatch completion record** (§ 7) so knight-rider can amend Phase 2 dispatch language accordingly.

---

## 2. Method

### 2.1 Heuristic input — Stage 2.5 classifier `method` field

The Stage 2.5 classifier preserved its source-side structured signal in a per-row `method` field (e.g., `met:classification=Sword Furniture-Menuki`, `ra:cv=animal armour & equestrian equipment`). These method strings capture the original museum/library vocabulary at higher fidelity than canonical_name token-matching could. Phase 0a subdivision is keyed on this method string — same upstream signal that drove the parent classification, now extended into the sub-enum.

### 2.2 Sub-enum mapping rules (full enumeration)

**Accessory rules** (deterministic exact-match on Stage 2.5 method):

| Method string | Subcategory | Rationale | Rows |
|---|---|---|---:|
| `met:classification=Sword Furniture` | `accessory_weapon_integrated` | Sword Furniture is mounted directly on a sword (kozuka set, mitokoromono) | 5 |
| `met:classification=Sword Furniture-Menuki` | `accessory_weapon_integrated` | Menuki = sword-grip ornaments, integrated to hilt | 64 |
| `met:classification=Sword Furniture-Tsuba` | `accessory_weapon_integrated` | Tsuba = sword guard, integrated between hilt + blade | 4 |
| `met:classification=Firearms Accessories-Powder Horns` | `accessory_weapon_integrated` | Powder horn paired to a specific firearm | 2 |
| `ra:cv=bayonets+name` | `accessory_weapon_integrated` | Bayonet sheath (parent weapon: rifle/musket) | 1 |
| `ra:cv=firearms & related objects+name:powder flask` | `accessory_weapon_integrated` | Powder flask, paired to firearm | 1 |
| `met:classification=Equestrian Equipment-Spurs` | `accessory_horse_or_equipment` | Mounted-combat scope | 16 |
| `met:classification=Equestrian Equipment-Bits` | `accessory_horse_or_equipment` | Mounted-combat scope | 7 |
| `met:classification=Equestrian Equipment-Shaffrons` | `accessory_horse_or_equipment` | Horse-head defense | 3 |
| `met:classification=Equestrian Equipment-Horse Trappings` | `accessory_horse_or_equipment` | Horse caparison | 1 |
| `ra:cv=animal armour & equestrian equipment` | `accessory_horse_or_equipment` | Royal Armouries umbrella for horse gear | 12 |
| `met:classification=Miscellaneous-Buckles & Ornament` | `accessory_horse_or_equipment` | All 6 rows inspected = "Ornament of Horse Trapping" — empirically all horse-tack | 6 |
| `met:classification=Banners` | `accessory_handheld` | Hand-carried standards (banner with shaft, regal banners) | 3 |
| `met:classification=Costumes` | `accessory_handheld` | Sandals, ceremonial habits — character-equippable hand/body items | 2 |
| `met:classification=Archery Equipment-Archer's Ring` | `accessory_handheld` | Thumb-ring for archery (worn on hand) | 1 |
| `ra:cv=militaria` | `accessory_handheld` (ambiguous; flagged) | 2 rows: Forsyth Primer display board + officer's helmet storage tin — neither is combat gear; closest sub-fit but warrants gandalf review | 2 |
| **Subtotal accessory** | | | **130** |

**Armor rules** (deterministic exact-match on Stage 2.5 method):

| Method string | Subcategory | Rationale | Rows |
|---|---|---|---:|
| `wd:weapon_type=shield` | `armor_shield` | Wikidata shield typing | 3 |
| `met:classification=Shields` | `armor_shield` | Met-museum Shields classification | 3 |
| `ra:cv=shields` | `armor_shield` | Royal Armouries shields | 2 |
| `name:tok=shield` | `armor_shield` | Wikipedia name-token fallback caught shield | 2 |
| `ra:cv=complete armours` | `armor_body_or_head` | Full body-armor sets | 56 |
| `met:classification=Helmets` | `armor_body_or_head` | Head defense | 10 |
| `met:classification=Armor Parts-Thigh and Leg Defense` | `armor_body_or_head` | Limb armor | 9 |
| `met:classification=Armor Parts` | `armor_body_or_head` | Limb/torso armor parts | 5 |
| `met:classification=Armor for Man` | `armor_body_or_head` | Full body-armor | 5 |
| `met:classification=Armor Parts-Knee Defenses` | `armor_body_or_head` | Knee plates | 4 |
| `ra:cv=helmets` | `armor_body_or_head` | Head defense | 3 |
| `ra:cv=armour pieces` | `armor_body_or_head` | Body-armor pieces | 3 |
| `met:classification=Armor for Man-1/2 Armor` | `armor_body_or_head` | Half-armor (torso + head) | 2 |
| `met:classification=Armor Parts-Masks` | `armor_body_or_head` | Face masks (Tengu-bo / Tengu-bu) | 2 |
| `met:classification=Armor Parts-Gauntlets` | `armor_body_or_head` | Hand armor | 2 |
| `met:classification=Armor for Horse and Man` | `armor_body_or_head` | Body-armor (note: includes horse companion) | 2 |
| `met:classification=Armor` | `armor_body_or_head` | Generic armor | 2 |
| `met:classification=Armor Parts-Cuirasses` | `armor_body_or_head` | Torso plates / set of mirrors | 2 |
| `met:classification=Armor Parts-Arms & Shoulders` | `armor_body_or_head` | Sodē | 1 |
| `met:classification=Armor Parts-Sollerets` | `armor_body_or_head` | Foot armor | 1 |
| `met:classification=Armor for Horse` | `armor_body_or_head` | Horse armor (D1c-excluded regardless) | 1 |
| `met:classification=Armor Parts-Colletins` | `armor_body_or_head` | Gorget | 1 |
| `met:classification=Helmets Parts` | `armor_body_or_head` | Helmet collar plate | 1 |
| `met:classification=Mail` | `armor_body_or_head` | Chain mail | 1 |
| `name:tok=armour` | `armor_body_or_head` (ambiguous; flagged) | Timoney APC — out-of-genre vehicle; gandalf may re-route at later stage | 1 |
| `name:tok=plate armor` | `armor_body_or_head` (ambiguous; flagged) | Statuette of Knight — art object; gandalf may re-route at later stage | 1 |
| **Subtotal armor** | | | **125** |

### 2.3 Default-fallthrough rules

If a method string is not in the enumerated table above, the row defaults to:
- Accessory parent → `accessory_handheld` with explicit `subdivision_note = "unenumerated_method=...; defaulted to accessory_handheld; gandalf review"`
- Armor parent → `armor_body_or_head` with explicit `subdivision_note = "unenumerated_method=...; defaulted to armor_body_or_head; gandalf review"`

Default-fallthrough was NOT triggered in this run (every Stage 2.5 method string was enumerated). No silent transformations.

### 2.4 Ambiguous-row flagging

Four rows carry `subdivision_note` flagging them as ambiguous routing for gandalf review:

| id | canonical_name | sub-routed to | flag note |
|---|---|---|---|
| 203443 | Forsyth Primer display board | `accessory_handheld` | display object, not combat gear; closest sub-fit but gandalf-review candidate |
| 209488 | Storage tin for officer's helmet | `accessory_handheld` | storage object, not combat gear; closest sub-fit but gandalf-review candidate |
| 193249 | Timoney (armoured personnel carrier) | `armor_body_or_head` | military vehicle, out-of-genre; D1c-excluded regardless |
| 206917 | Statuette of Knight Wearing Chain-mail and Plate Armor | `armor_body_or_head` | art object, not combat armor; D1c-excluded regardless |

The latter two are **D1c-excluded regardless of subcategorization**, so their classification has zero downstream effect on v1_scope. The first two are `accessory_handheld` and D1b-allowed; gandalf spot-check may flag for removal (rerouting to a parent-category re-classification at later stage would be substrate-outside-Phase-0a scope per dispatch § 6: "NOT changes to existing Stage 1+1.5+2+2.5 column values").

---

## 3. Per-subcategory representative samples

### 3.1 `accessory_handheld` (8 rows)

| id | source | name | method |
|---|---|---|---|
| 192725 | met-museum | Pair of Straw Hemp Sandals | `met:classification=Costumes` |
| 198725 | met-museum | Banner with Shaft | `met:classification=Banners` |
| 198732 | met-museum | Banner of Louis XIV, King of France (r. 1643–1715) | `met:classification=Banners` |
| 198738 | met-museum | Banner of Pope Alexander VIII (reigned 1689–91) | `met:classification=Banners` |
| 203443 | royal_armouries | Forsyth Primer display board *(flagged)* | `ra:cv=militaria` |
| 203948 | met-museum | Very Thin Archer's Ring of Mottled Stone | `met:classification=Archery Equipment-Archer's Ring` |
| 209015 | met-museum | French Academician's Habit of Julian Green and René de Obaldia | `met:classification=Costumes` |
| 209488 | royal_armouries | Storage tin for officer's helmet *(flagged)* | `ra:cv=militaria` |

### 3.2 `accessory_weapon_integrated` (sample 10 of 77)

| id | source | name | method |
|---|---|---|---|
| 195229 | met-museum | Sword guard (Tsuba) Depicting Skanda (韋駄天図鐔) | `met:classification=Sword Furniture-Tsuba` |
| 195230 | met-museum | Sword guard (Tsuba) Depicting God of Longevity Jurōjin (寿老人図鐔) | `met:classification=Sword Furniture-Tsuba` |
| 197598 | met-museum | Pair of Sword-Grip Ornaments (Menuki) | `met:classification=Sword Furniture-Menuki` |
| 201254 | royal_armouries | Sheath *(bayonet)* | `ra:cv=bayonets+name` |
| 205391 | royal_armouries | Powder flask | `ra:cv=firearms & related objects+name:powder flask` |
| 206629 | met-museum | Powder Flask of Jacques de Silly (1513–1571) | `met:classification=Firearms Accessories-Powder Horns` |
| 207261 | met-museum | Set of Sword Fittings (Mitokoromono) with Two Additional Knife Handles (Kozuka) | `met:classification=Sword Furniture` |
| 207439 | met-museum | Set of Sword Fittings (Mitokoromono) with Two Additional Knife Handles (Kozuka) | `met:classification=Sword Furniture` |
| 207447 | met-museum | Set of Sword Fittings (Mitokoromono) with Two Additional Knife Handles (Kozuka) and a Pair | `met:classification=Sword Furniture` |
| 209857 | met-museum | Powder Horn of John Mahard | `met:classification=Firearms Accessories-Powder Horns` |

### 3.3 `accessory_horse_or_equipment` (sample 10 of 45)

| id | source | name | method |
|---|---|---|---|
| 187506 | met-museum | Two Ear Guards from a Shaffron (Horse's Head Defense) of Emperor Charles V | `met:classification=Equestrian Equipment-Shaffrons` |
| 196085 | met-museum | Pair of Ear Guards from a Shaffron (Horse's Head Defense) | `met:classification=Equestrian Equipment-Shaffrons` |
| 197351 | met-museum | Pair of Rowel Spurs | `met:classification=Equestrian Equipment-Spurs` |
| 198572 | met-museum | Pair of Hussar Rowel Spurs | `met:classification=Equestrian Equipment-Spurs` |
| 200265 | met-museum | Bit Boss with Hercules and Diomedes | `met:classification=Equestrian Equipment-Bits` |
| 200270 | met-museum | Bit Boss with Hercules Fighting the Monster Cacus | `met:classification=Equestrian Equipment-Bits` |
| 206763 | royal_armouries | Saddle steel | `ra:cv=animal armour & equestrian equipment` |
| 206765 | royal_armouries | Saddle steel | `ra:cv=animal armour & equestrian equipment` |
| 207207 | met-museum | Ornament of Horse Trapping | `met:classification=Miscellaneous-Buckles & Ornament` |
| 207209 | met-museum | Ornament of Horse Trapping | `met:classification=Miscellaneous-Buckles & Ornament` |

### 3.4 `armor_shield` (10 rows)

| id | source | name | method |
|---|---|---|---|
| 11 | wikidata | shield of Achilles | `wd:weapon_type=shield` |
| 46 | wikidata | Shield Depicting Saint George Slaying the Dragon | `wd:weapon_type=shield` |
| 77 | wikidata | Q88199410 | `wd:weapon_type=shield` |
| 174333 | wikipedia | Battersea Shield | `name:tok=shield` |
| 180526 | met-museum | Shield Depicting Saint George Slaying the Dragon | `met:classification=Shields` |
| 189836 | met-museum | Shield of Henry II of France (reigned 1547–59) | `met:classification=Shields` |
| 193224 | wikipedia | Rhos Rydd Shield | `name:tok=shield` |
| 193566 | met-museum | Shield (Pavise) | `met:classification=Shields` |
| 199565 | royal_armouries | Shield | `ra:cv=shields` |
| 205550 | royal_armouries | Rondache | `ra:cv=shields` |

### 3.5 `armor_body_or_head` (sample 10 of 115)

| id | source | name | method |
|---|---|---|---|
| 24024 | royal_armouries | Tilting visor | `ra:cv=helmets` |
| 27932 | royal_armouries | Left cuisse and poleyn | `ra:cv=armour pieces` |
| 167927 | met-museum | Half Armor attributed to Don Gonzalo Fernández de Córdoba | `met:classification=Armor for Man-1/2 Armor` |
| 167928 | met-museum | Foot-Combat Helm of Sir Giles Capel (1485–1556) | `met:classification=Helmets` |
| 174863 | met-museum | Pair of Shoulder Guards (Sodē) | `met:classification=Armor Parts-Arms & Shoulders` |
| 174882 | met-museum | Mask (Tengu-bo) of Mountain God Face with Gorget | `met:classification=Armor Parts-Masks` |
| 193249 | wikipedia | Timoney (armoured personnel carrier) *(flagged — out-of-genre vehicle)* | `name:tok=armour` |
| 195176 | met-museum | Jousting Sallet (Rennhut) Made for Louis II, King of Hungary | `met:classification=Helmets` |
| 206917 | wikipedia | Statuette of Knight Wearing Chain-mail and Plate Armor *(flagged — art object)* | `name:tok=plate armor` |
| 210606 | met-museum | Shirt of Mail and Plate of Al-Ashraf Sayf ad-Din Qaitbay (ca. 1416/18–1496) | `met:classification=Mail` |

---

## 4. Subcategory boundary observations

### 4.1 `accessory_horse_or_equipment` reconciliation surprise

The `met:classification=Miscellaneous-Buckles & Ornament` cluster (6 rows) all turned out to be "Ornament of Horse Trapping" upon inspection. Routed to `accessory_horse_or_equipment` consistent with their actual semantic meaning. **Downstream effect:** D1c-excluded count nudges from policy estimate ~105-145 up to empirical 160 partly because of this cluster. This is correct routing per the substrate — the policy estimate was based on an assumption that "Miscellaneous-Buckles" would split between handheld and horse, but empirically all 6 are horse-trapping ornaments.

### 4.2 `accessory_weapon_integrated` Japanese-sword skew

77 rows in this subcategory, but **73 of 77 are Japanese sword-furniture** (Menuki 64 + Tsuba 4 + Sword Furniture umbrella 5). Only 4 rows are non-Japanese-sword (1 bayonet sheath, 1 royal-armouries powder flask, 2 met-museum powder horns). **Implication for Phase 0b (gandalf substrate-fit lookup):** the parent-weapon-family compatibility lookup needs to handle Japanese sword sub-families (katana/wakizashi/tanto) specifically — Menuki + Tsuba are not compatible with European broadswords. Powder horns + bayonets need separate lookup for firearm parent-family.

### 4.3 `armor_shield` distribution

10 shields total: 3 from Wikidata, 3 from met-museum, 2 from Royal Armouries, 2 from Wikipedia. Geographically European/Greek-mythological-heavy (Achilles, Saint George, Battersea, Henry II of France, Rondache, Pavise). No East Asian shields surfaced at Tier S — flagged as substrate gap for Sidecar B (the dispatch § 6 routes thin-tradition + thin-cell-enrichment to Sidecar B; East Asian shield could be a thin-substrate area worth surfacing).

### 4.4 No `mythological` `armor_shield` substrate rows present beyond the shield of Achilles

Sketch F anchor coverage observation: shield of Achilles (id=11) is the only mythological armor_shield row in Tier S. Other mythological-register Sketch F anchor armor (e.g., Aegis of Athena) was not surfaced by the Stage 1 mythological-NULL pipeline; Stage 4 mythological rescue (~30 rows) may surface additional candidates. Not a Phase 0a deliverable — noted for the Phase 3 distribution report.

---

## 5. Spot-check sample (25 rows for gandalf review)

Stratified by `(subcategory, method)` to give gandalf breadth — avoids the Menuki-monopoly problem (Menuki is 64 of 77 in `accessory_weapon_integrated`). Companion JSON at `spot-sample-25.json`.

| # | Subcategory | id | source | canonical_name | method |
|---:|---|---:|---|---|---|
| 1 | `accessory_handheld` | 192725 | met-museum | Pair of Straw Hemp Sandals | `met:classification=Costumes` |
| 2 | `accessory_handheld` | 198738 | met-museum | Banner of Pope Alexander VIII (reigned 1689–91) | `met:classification=Banners` |
| 3 | `accessory_handheld` | 203443 | royal_armouries | Forsyth Primer display board *(flagged)* | `ra:cv=militaria` |
| 4 | `accessory_handheld` | 203948 | met-museum | Very Thin Archer's Ring of Mottled Stone | `met:classification=Archery Equipment-Archer's Ring` |
| 5 | `accessory_weapon_integrated` | 196635 | met-museum | Sword Guard (Tsuba) With the Motif of Autumnal Vegetation | `met:classification=Sword Furniture-Tsuba` |
| 6 | `accessory_weapon_integrated` | 200761 | met-museum | Pair of Sword-Grip Ornaments (Menuki) | `met:classification=Sword Furniture-Menuki` |
| 7 | `accessory_weapon_integrated` | 201254 | royal_armouries | Sheath *(bayonet)* | `ra:cv=bayonets+name` |
| 8 | `accessory_weapon_integrated` | 205391 | royal_armouries | Powder flask | `ra:cv=firearms & related objects+name:powder flask` |
| 9 | `accessory_weapon_integrated` | 206629 | met-museum | Powder Flask of Jacques de Silly (1513–1571) | `met:classification=Firearms Accessories-Powder Horns` |
| 10 | `accessory_weapon_integrated` | 207447 | met-museum | Set of Sword Fittings (Mitokoromono) | `met:classification=Sword Furniture` |
| 11 | `accessory_horse_or_equipment` | 187506 | met-museum | Two Ear Guards from a Shaffron of Emperor Charles V | `met:classification=Equestrian Equipment-Shaffrons` |
| 12 | `accessory_horse_or_equipment` | 197351 | met-museum | Pair of Rowel Spurs | `met:classification=Equestrian Equipment-Spurs` |
| 13 | `accessory_horse_or_equipment` | 204213 | met-museum | Pair of Bit Bosses | `met:classification=Equestrian Equipment-Bits` |
| 14 | `accessory_horse_or_equipment` | 206778 | royal_armouries | Saddle steels | `ra:cv=animal armour & equestrian equipment` |
| 15 | `accessory_horse_or_equipment` | 207210 | met-museum | Ornament of Horse Trapping | `met:classification=Miscellaneous-Buckles & Ornament` |
| 16 | `armor_shield` | 77 | wikidata | Q88199410 | `wd:weapon_type=shield` |
| 17 | `armor_shield` | 193224 | wikipedia | Rhos Rydd Shield | `name:tok=shield` |
| 18 | `armor_shield` | 193566 | met-museum | Shield (Pavise) | `met:classification=Shields` |
| 19 | `armor_shield` | 205550 | royal_armouries | Rondache | `ra:cv=shields` |
| 20 | `armor_body_or_head` | 167927 | met-museum | Half Armor attributed to Don Gonzalo Fernández de Córdoba | `met:classification=Armor for Man-1/2 Armor` |
| 21 | `armor_body_or_head` | 174863 | met-museum | Pair of Shoulder Guards (Sodē) | `met:classification=Armor Parts-Arms & Shoulders` |
| 22 | `armor_body_or_head` | 180561 | met-museum | Face Mask of Mountain God (Tengu-bu) | `met:classification=Armor Parts-Masks` |
| 23 | `armor_body_or_head` | 195176 | met-museum | Jousting Sallet (Rennhut) Made for Louis II of Hungary | `met:classification=Helmets` |
| 24 | `armor_body_or_head` | 203247 | royal_armouries | Close helmet | `ra:cv=helmets` |
| 25 | `armor_body_or_head` | 211171 | royal_armouries | Mitten gauntlet | `ra:cv=armour pieces` |

**Acceptance threshold (per dispatch § 8 Phase 0a smoke):** ≥20/25 sensible (~80%). Flagged rows (3 and 17 — `Q88199410` is a stub-named Wikidata row; 17 = `Rhos Rydd Shield`, an obscure shield) may be on the boundary; verifying-as-sensible is at gandalf's discretion.

---

## 6. Empirical verification (post-execution)

DB queries post-UPDATE:

```
SELECT weapon_kind_classified_subtype, COUNT(*)
FROM weapon_knowledge_entries WHERE quality_tier='S'
GROUP BY weapon_kind_classified_subtype ORDER BY 2 DESC;
```

| subcategory | count |
|---|---:|
| `handheld_weapon` | 449 |
| `siege_vehicle` | 316 |
| `armor_body_or_head` | 115 |
| `accessory_weapon_integrated` | 77 |
| `art_object` | 52 |
| `accessory_horse_or_equipment` | 45 |
| `other` | 31 |
| `ammo_consumable` | 23 |
| `armor_shield` | 10 |
| `accessory_handheld` | 8 |
| **Sum** | **1,126** |

D1a auto-include verification: `weapon_kind_classified_subtype = 'handheld_weapon'` returns 449 — matches dispatch § 2 binding count exactly.

D1b auto-include verification: `weapon_kind_classified_subtype IN ('armor_shield', 'accessory_handheld', 'accessory_weapon_integrated')` returns 95 — composition-policy estimate ~100-160; empirical 95 just below lower bound (see TL;DR for downstream-implication note).

D1c excluded verification: `weapon_kind_classified_subtype IN ('siege_vehicle', 'art_object', 'other', 'ammo_consumable', 'accessory_horse_or_equipment', 'armor_body_or_head')` returns 582 — these are the Tier-S rows blocked from v1_scope per § 4.1 of dispatch.

Non-Tier-S leakage: 0 rows outside Tier-S have `weapon_kind_classified_subtype` populated. Phase 2 may extend population to non-Tier-S rows in future stages (currently Phase 0a touches only Tier-S per scope).

---

## 7. Open items / follow-ups (surfaced for Phase 2 + dispatch completion record)

1. **State-finding clarification:** Phase 0a was a three-step operation (ALTER + populate-1126 + subdivide-255), not single UPDATE-in-place. Dispatch § 3.1 + § 5 language presupposed column existed. Knight-rider should consider light amendment for Phase 2 dispatch references. No functional break; flagged for transparency.
2. **D1b empirical 95 vs policy estimate ~100-160:** ~5-65-row shortfall in auto-promote secondaries. v1_scope envelope (1,700-3,100) is unaffected (the D1b range was a small fraction of total). gandalf may want to acknowledge this in Phase 3 distribution report sign-off.
3. **`accessory_weapon_integrated` Japanese-sword skew (73 of 77):** Phase 0b parent-weapon-family lookup must handle Japanese-sword sub-families (katana/wakizashi/tanto). Surfaced to gandalf for Phase 0b authoring.
4. **Four ambiguous rows flagged** (§ 2.4) — gandalf may request rerouting; routing changes deferred to a separate dispatch per dispatch § 6 ("NOT changes to existing Stage 1+1.5+2+2.5 column values").
5. **Substrate gap surfaced:** no Tier-S East Asian shield; no Tier-S mythological armor beyond shield of Achilles. Routes to Sidecar B (off-hand items + thin-tradition boost) per dispatch § 1.6.

---

## 8. Acceptance criteria coverage (per dispatch § 5.5 Phase 0a subset)

- [x] All 255 rows have `weapon_kind_classified_subtype` updated to a subcategory enum value
- [x] Markdown artifact at `agentic_orchestration/elrond/research/cycle-10-stage-3-2026-05-25/accessory-armor-subcategory-classification.md` with per-subcategory counts (§ 0), per-subcategory representative 5-10 row sample (§ 3), heuristic rules documented (§ 2)
- [x] Companion JSON at same dir with full row-level details for downstream consumption (`accessory-armor-subcategory-classification.json`)
- [x] Pre-update DB backup created at `cycle-10-stage-3-2026-05-25/backups/telemetry.db.pre-phase-0a` (gitignored per per-directory `.gitignore` pattern per Stage 1.5 precedent)
- [x] 25-row spot-check block clearly marked in markdown (§ 5) for gandalf review
- [ ] gandalf 25-row spot-check ≥20/25 sensible (post-hoc; not blocked by this artifact)

---

## 9. Cross-references

- Dispatch: `agentic_orchestration/dispatches/2026-05-24-elrond-cycle-10-stage-3-v1-scope-materialization.md`
- Composition policy v1: `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` § 1.1
- Stage 2.5 source artifact: `agentic_orchestration/elrond/research/cycle-10-stage-2-5-2026-05-24/tier-s-classification.json` + `tier-s-weapon-kind-classification.md`
- Stage 2.5 classifier script: `agentic_orchestration/elrond/research/cycle-10-stage-2-5-2026-05-24/classify_tier_s_weapon_kind.py` (Phase 0a is its direct extension)
- Population script: `classify_accessory_armor_subcategory.py` (this dir)
- Execution log: `classify_log.out` (this dir)
- Pre-phase-0a backup: `backups/telemetry.db.pre-phase-0a` (gitignored)
- Phase 0a MIGRATION: `MIGRATION.md` (this dir)
- Cycle 10 state file: `agentic_orchestration/weapon-substrate-curation-cycle-10-state.md`

---

## 10. Sign-off

**Author:** elrond (Phase 0a; Cycle 10 Stage 3)
**Date:** 2026-05-25
**Authority:** dispatch FIRE-READY (Gate-1 cleared; commit `04509ad`) + Cycle 10 scope-doc § 1 autonomous decisions on heuristic-rule choice
**Status:** Phase 0a complete; awaiting (a) gandalf 25-row spot-check (post-hoc) and (b) Phase 2 re-invocation by knight-rider after Phase 0b + Phase 1 land.
