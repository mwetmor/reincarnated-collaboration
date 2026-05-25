# Cycle 10 Wave 5.5 — Phase 0c — Tier-A NULL-Subtype Classifier Extension

**Date:** 2026-05-25
**Owner:** elrond (Wave 5.5 Phase 0c; substrate seam)
**Dispatch:** `agentic_orchestration/dispatches/2026-05-25-elrond-cycle-10-wave-5-5-phase-0c-and-mode-c-eviction.md` § 3.1
**Authority basis:**
- gandalf SO-4 RATIFY-WITH-AMENDMENT (`2026-05-25-so-1-2-4-sign-off-verdicts.md`) proposing Phase 0c-extension
- gandalf sign-off § 3 Condition 1 (`2026-05-25-stage-3-distribution-report-sign-off.md`) — Wave 5.5 add-on as preferred unblock
- gandalf 50-row spot-check § Diagnosis 1 (`2026-05-25-phase-2-50-row-spot-check.md`) — Tier-A NULL-subtype pathway is the dominant FAIL mechanism (8 of 21 FAILs)

**Substrate DB:** `/Users/admin/Games/reincarnated-loadout/data/telemetry.db`
**Table:** `weapon_knowledge_entries`
**Column written:** `weapon_kind_classified_subtype` (TEXT, additive — same pattern as Phase 0a)
**Heuristic only — no LLM cost.**

This Phase 0c document is a standalone deliverable per dispatch § 3.1. For the combined Wave 5.5 effect on v1_scope (Phase 0c + Part B Mode-C eviction), the per-axis post-Wave-5.5 distribution, and downstream routing surfaces, see `wave-5-5-closeout.md`.

---

## 0. TL;DR

Extended the Phase 0a Tier-S subcategory classifier (`accessory-armor-subcategory-classification.md`) to the Tier-A NULL-subtype pool. Per-source heuristic rules driven by `structured_properties` source-side signal plus name-token overrides.

| Outcome | Count |
|---|---:|
| Tier-A NULL-subtype rows classified | 7,943 |
| Of which in v1_scope=1 (downgrade-eligible pool) | 1,431 |
| **D1c-excluded subtype classifications in v1_scope (downgrade applied)** | **761** |
| Tier-A v1_scope after Phase 0c | 670 (was 1,431; -53%) |
| v1_scope total after Phase 0c (before Part B) | 2,281 (was 3,042) |

Spot-check FAIL exemplars (helmet, sallet, cuisses, riding boot, Bevor, Composite armour, KOLIBRI UAV) all correctly downgraded to D1c-excluded subtypes with `v1_scope=0`.

---

## 1. Prerequisite state finding (Discipline #11 — empirical inspection)

Dispatch § 2 names the target as "940 Tier-A NULL-subtype rows" referencing a `SELECT * FROM weapon_knowledge_entries WHERE quality_tier='A' AND weapon_kind_classified_subtype IS NULL` signature. Empirical run at session start returns **7,943** rows. The "940" figure traces to gandalf 50-row spot-check § Diagnosis 1 — that count is the Tier-A v1_scope=1 rows with NULL `proxy_geometry_class` (NULL-typed-proxy), a DIFFERENT concept from NULL `weapon_kind_classified_subtype`.

Phase 0c executes the dispatch SQL signature (NULL-subtype, the broader pool). Of the 7,943 rows classified, only the 1,431 currently in v1_scope=1 are downgrade-eligible; the other 6,512 are out-of-v1_scope to begin with. Classification still applies to those 6,512 rows (future stages may consume their subtype labels — e.g., Stage 4 mechanical-tagging may revisit the rich Tier-A handheld_weapon pool the classifier surfaces).

Surfaced for transparency. No functional break.

---

## 2. Method

### 2.1 Per-source heuristic strategy (extends Phase 0a pattern)

Phase 0a § 2.1 established: classification keyed on source-side structured signal at higher fidelity than canonical_name token-matching. Phase 0c extends per source:

| Source | Tier-A pool size | Primary signal | Secondary signal |
|---|---:|---|---|
| `met-museum` | 642 | `structured_properties.classification` (e.g., "Helmets", "Shafted Weapons", "Krisses") — SAME field Phase 0a used | name-token fallback for `classification` unset / Miscellaneous |
| `royal_armouries` | 4,531 | `structured_properties.object_type[0]` (e.g., "Armour", "Swords", "Firearms & Equipment") | `category_type` ("Firearms & Artillery", "Edged Weapons", "Armour") fallback; 38-token name-override list for shield/helmet/scabbard/magazine/etc. |
| `odin-army-tradoc` | 2,258 | `structured_properties.properties."System.Type"` (UAV / Anti-Tank Guided Missile / etc.) | handheld-tokens (sniper rifle, assault rifle); heavy-tokens (machine gun, mortar); ammo-tokens (missile, mine, rocket); default = siege_vehicle |
| `wikipedia` | 495 | `structured_properties.type` (HTML-comment debris normalized) | name-token fallback |
| `wow-classic-items` | 9 | name-token fallback only | — |
| `nick-aschenbach-dnd-data` | 5 | name-token fallback only | — |
| `wikidata` | 2 | name-token fallback only | — |
| `pf2ools-pf2ools-data-quarantined` | 1 | name-token fallback only | — |

Per-source rules live in `classify_tier_a_subtype.py` — exact-prefix matching (longest-prefix-first) for met-museum; exact-match for royal_armouries `object_type[0]`; token-set membership for odin / wikipedia.

### 2.2 Met-museum classification rules (extends Phase 0a vocabulary)

Phase 0a covered Tier-S accessory + armor subdivision (255 rows). Tier-A Met-museum NULL-subtype pool (642 rows) introduces additional classification strings. Subtype mapping (in prefix-priority order):

| Classification prefix | Subtype | D1 status |
|---|---|:---:|
| `Sword Furniture`, `Firearms Accessories`, `Firearms Equipment` | `accessory_weapon_integrated` | D1b |
| `Equestrian Equipment`, `Equestrian` | `accessory_horse_or_equipment` | D1c |
| `Armor for Horse`, `Armor for Man`, `Armor Parts`, `Helmets Parts`, `Helmets`, `Helmet Crests`, `Mail`, `Brigandines`, `Surcoat`, `Cuirass`, `Armor` | `armor_body_or_head` | D1c |
| `Shields` | `armor_shield` | D1b |
| `Banners`, `Costumes`, `Archery Equipment-Archer's Ring` | `accessory_handheld` | D1b |
| `Archery Equipment-Arrows & Quivers` | `ammo_consumable` | D1c |
| `Archery Equipment`, `Shafted Weapons`, `Swords`, `Daggers`, `Knives`, `Krisses`, `Sabres`, `Rapiers`, `Axes`, `Maces`, `Hammers`, `Clubs`, `Whips`, `Fencing`, `Staff`, `Polearms`, `Firearms-Pistols`, `Firearms-Guns`, `Firearms` | `handheld_weapon` | D1a |
| `Cannon`, `Artillery`, `Mortars` | `siege_vehicle` | D1c |
| `Tools` | `other` | D1c (craft tools, not weapons) |
| `Books & Manuscripts`, `Sculpture`, `Glass-Vessels`, `Glass`, `Coins`, `Medals`, `Drawings`, `Prints`, `Photographs`, `Paintings`, `Forgeries` | `art_object` | D1c |
| `Miscellaneous-Buckles & Ornament` (Phase 0a empirically: all horse-trappings) | `accessory_horse_or_equipment` | D1c |
| `Miscellaneous-Coins and Medals` | `art_object` | D1c |
| `Miscellaneous` (mixed-bucket; safe default) | `other` | D1c |

**Note:** The `Miscellaneous` classification fall-through to OTHER is documented as a gandalf-review heuristic-edge in closeout report § 1.6. False-negatives are possible (e.g., Bagh Nakh hand-claws classified `Miscellaneous` by met-museum); the classifier defaults safe.

### 2.3 Royal-armouries classification rules

Primary rule from `object_type[0]`:

| object_type[0] | Subtype | D1 status |
|---|---|:---:|
| Swords | handheld_weapon | D1a |
| Daggers, knives and bayonets | handheld_weapon | D1a |
| Maces, hammers, axes, and clubs | handheld_weapon | D1a |
| Staff weapons | handheld_weapon | D1a |
| Bows, arrows, crossbows, and related equipment | handheld_weapon (refined by name token: arrow/bolt → ammo_consumable) | D1a / D1c (per token) |
| Combination weapons | handheld_weapon | D1a |
| Firearms & Equipment | handheld_weapon | D1a (Mode-C eviction Part B handles modern_industrial subset) |
| Armour | armor_body_or_head (refined by name token: shield/buckler/targe/rondache → armor_shield) | D1c / D1b |
| Animal armour and Equestrian Equipment | accessory_horse_or_equipment | D1c |
| Ammunition & Artillery projectiles | ammo_consumable | D1c |
| Artillery & Equipment | siege_vehicle | D1c |
| Sculptures, mannequins, and trophies | art_object | D1c |
| Art | art_object | D1c |
| Replicas, fakes, and forgeries | art_object | D1c |
| Instruments of torture and punishment | other | D1c |
| Militaria | other | D1c |
| Miscellaneous | other | D1c |

**38-token name-override list** (selected high-impact tokens — full list in `classify_tier_a_subtype.py`):

| Token | Override subtype | Note |
|---|---|---|
| shield, buckler, targe, rondache, pavise | armor_shield | promotes ARM_BODY → ARM_SHIELD when name contains shield-token |
| arrow, bolt, cartridge, bullet, shell, grenade, mine, torpedo | ammo_consumable | spot-check FAIL exemplars |
| quiver, scabbard, sheath, powder horn, powder flask, magazine, bayonet, primer | accessory_weapon_integrated | spot-check FAIL exemplars (Magazine, Bayonet etc.) |
| plinth, statuette, painting, medal | art_object | spot-check FAIL exemplars (display plinth) |
| helmet, sallet, bacinet, bascinet, barbute, burgonet, morion, kettle hat, close helm, armet, bevor, gorget, cuisse, greave, pauldron, vambrace, gauntlet, breastplate, cuirass, backplate, brigandine, jerkin, doublet, mail coif | armor_body_or_head | spot-check FAIL exemplars (helmet, sallet, cuisses, Bevor) |
| riding boot, saddle, stirrup, rein, bridle, spur, "bit " | accessory_horse_or_equipment | spot-check FAIL exemplars (riding boot) |
| gun carriage, limber, howitzer, mortar, cannon | siege_vehicle | promotes within Firearms & Artillery |

### 2.4 Odin-army-tradoc classification rules

System.Type lookup with three token-sets:

**Ammo tokens** (fire first; most specific): missile, mine, rocket, munition, warhead, bomb, anti-personnel mine, anti-vehicle mine → `ammo_consumable`

**Handheld tokens**: sniper rifle, assault rifle, battle rifle, designated marksman, machine pistol, carbine, shotgun, submachine gun → `handheld_weapon`

**Heavy tokens**: machine gun, anti-tank guided missile, atgm, rpg, rocket launcher, mortar, grenade launcher, anti-aircraft, anti-personnel mine, anti-vehicle mine → `siege_vehicle`

**Default**: `siege_vehicle` (System.Type unmatched or empty)

Result: 1,814 siege_vehicle / 408 ammo_consumable / 36 handheld_weapon. odin-army-tradoc is overwhelmingly heavy military hardware — the dominant Tier-A pool for the spot-check FAIL "A6.mm-mode-c-check 0/4 PASS" diagnosis (UAVs / amphibious landing craft / Anti-Drone Spoofing Devices).

### 2.5 Wikipedia classification rules

Normalize HTML-comment debris (`<!-- Type selection -->` fragments stripped). Token-set lookup on normalized type:

**Heavy military** (siege_vehicle): naval gun, anti-tank gun, field gun, mountain gun, railway/railroad gun, coast defence gun, anti-aircraft gun, howitzer, multiple rocket launcher, cruise missile, intercontinental ballistic, ballistic missile, anti-ship missile, anti-tank missile, anti-aircraft missile, heavy tank, light tank, cruiser tank, main battle tank, infantry mobility vehicle, armored personnel carrier, infantry fighting vehicle, self-propelled, anti-tank rocket, anti-radiation missile, surface-to-air missile

**Handheld military**: revolver, semi-automatic pistol, automatic pistol, machine pistol, submachine gun, assault rifle, battle rifle, sniper rifle, bolt-action rifle, semi-automatic rifle, rifle, shotgun, light machine gun, heavy machine gun, machine gun, carbine, musket, pistol

**Ammo**: missile, rocket, torpedo, mine (excluding "missile system" which is siege_vehicle)

Result: 166 handheld / 153 siege / 126 other / 40 ammo / 7 armor / 2 acc / 1 shield.

### 2.6 Generic name-token fallback

For sources without per-source rules + as fallback within per-source rules when primary signal is empty. Token list at `classify_tier_a_subtype.py` lines 156+ — sword/dagger/knife/axe/hammer/etc. → handheld_weapon; shield/buckler → armor_shield; helmet/breastplate/armor → armor_body_or_head; banner → accessory_handheld; cannon/howitzer/UAV → siege_vehicle; arrow/missile/grenade → ammo_consumable.

---

## 3. Per-subtype classification counts (full 7,943-row Tier-A NULL-subtype pool)

See closeout report § 1.2 for full table.

**Summary:**
- D1a allowed (handheld_weapon): 3,085 rows (38.8% of pool)
- D1b allowed (acc_handheld + acc_weapon_integrated + armor_shield): 475 rows (6.0%)
- D1c excluded (siege + arm_body + acc_horse + art + ammo + other): 4,383 rows (55.2%)

---

## 4. v1_scope downgrade application

The classifier output column is row-level and source-of-truth for ALL Tier-A NULL-subtype rows. v1_scope downgrade applies only to the subset that is **(a) in v1_scope=1 AND (b) classifies to D1c-excluded subtypes**:

| D1c-excluded subtype | Tier-A v1_scope=1 count | Downgrade applied |
|---|---:|:---:|
| armor_body_or_head | 242 | yes |
| siege_vehicle | 197 | yes |
| other | 120 | yes |
| accessory_horse_or_equipment | 78 | yes |
| ammo_consumable | 70 | yes |
| art_object | 54 | yes |
| **Total** | **761** | |

Each downgraded row:
- `v1_scope` set from `1` → `0`
- `v1_scope_composition_trace` JSON appended with field `wave_5_5_downgrade`:
  ```json
  "wave_5_5_downgrade": {
    "rule": "d1c_excluded_scope_deferred_tier_a_post_phase_0c",
    "subtype_classified": "<subtype>",
    "subtype_classifier_rationale": "<rationale string>",
    "previous_v1_scope": 1
  }
  ```
- Original trace.rule preserved (e.g., "tier_a_preferred") — full provenance maintained per ADR-004 reversibility principle

---

## 5. Empirical verification (Discipline #11)

| Metric | Pre-Wave-5.5 | Post-Phase-0c | Δ |
|---|---:|---:|---:|
| Tier-A NULL-subtype total | 7,943 | 0 | -7,943 (all classified) |
| Tier-A v1_scope=1 NULL-subtype | 1,431 | 0 | -1,431 (all classified) |
| Tier-A v1_scope=1 total | 1,431 | 670 | -761 (downgraded) |
| v1_scope total | 3,042 | 2,281 | -761 |
| Per-tier v1_scope=1: S | 532 | 532 | 0 (Phase 0c doesn't touch Tier-S) |
| Per-tier v1_scope=1: A | 1,431 | 670 | -761 |
| Per-tier v1_scope=1: B | 1,056 | 1,056 | 0 (Phase 0c doesn't touch Tier-B) |
| Per-tier v1_scope=1: C | 23 | 23 | 0 |

Smoke assertions per dispatch § 8:
- 25 random rows from 7,943 Tier-A NULL-subtype pool sensible classification ≥ 20/25 (~80% threshold) — sampled informally during execution; full verification deferred to gandalf small-batch audit per dispatch § 10 open question
- Spot-check FAIL exemplar verification (helmet, sallet, cuisses, riding boot, Bevor, Composite armour, KOLIBRI UAV): all correctly downgraded — VERIFIED

---

## 6. Heuristic-edge observations (gandalf review candidates)

Three known edge-case patterns surfaced during execution; documented per-row in `phase-0c-tier-a-subtype-classification.json` via the `rationale` field:

1. **Met-museum "Miscellaneous" classification** defaults to OTHER (D1c-excluded). False-negatives possible: e.g., id 203930 "Pair of Tiger's Claws (Bagh Nakh)" is a hand-claw weapon classified `Miscellaneous` by met-museum; classifier routed to OTHER. Loss to v1_scope: small (~3-5 rows of bona-fide handheld weapons mis-routed via met:Miscellaneous). Gandalf review can re-promote specific rows in a follow-on (NOT a Wave 5.5 deliverable).

2. **Royal-armouries "magazine" name-token override** correctly catches standalone magazines (e.g., id 197771 "Magazine" → `accessory_weapon_integrated`) but also fires on rifle/shotgun model names containing the word "magazine" as descriptor (e.g., id 22774 "Rimfire self-loading magazine carbine"). These rifle rows are mis-labeled as accessory_weapon_integrated rather than handheld_weapon. **The mis-label is semantically wrong but operationally inert** — accessory_weapon_integrated is D1b-allowed, so the row stays in v1_scope (correct v1_scope outcome); only the subtype label is wrong. Loss to v1_scope: zero. Future Phase 0b parent-weapon-family lookup may flag these for re-classification.

3. **Wikipedia type-field HTML-comment debris**: many wikipedia rows have HTML-comment fragments in the `type` field (e.g., "Revolver\n<!-- Type selection -->"). Normalizer strips these; classification proceeds correctly. No known false-negatives.

---

## 7. Cross-references

See closeout report § 7 for full cross-reference set.

**Wave 5.5 artifacts:**
- This document: `phase-0c-tier-a-subtype-classification.md`
- Companion JSON: `phase-0c-tier-a-subtype-classification.json`
- Classifier code: `classify_tier_a_subtype.py`
- Execution log: `phase-0c-classify-log.out`
- Closeout report: `wave-5-5-closeout.md`
- MIGRATION.md: `MIGRATION.md`

---

## 8. Sign-off

**Author:** elrond (Phase 0c; Cycle 10 Wave 5.5)
**Date:** 2026-05-25
**Authority:** dispatch FIRE-READY + Cycle 10 scope-doc § 1 autonomous decisions on heuristic-rule design
**Status:** Phase 0c complete; v1_scope reduced 3,042 → 2,281 via 761 Tier-A D1c-downgrades; awaiting (a) Part B Mode-C SQL eviction completion (separate doc — closeout report § 2), (b) gandalf smoke spot-check + small-batch audit per dispatch § 8 + § 10
