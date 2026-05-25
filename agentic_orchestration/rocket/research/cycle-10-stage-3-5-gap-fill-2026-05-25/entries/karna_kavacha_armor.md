# Entry: Karna — Kavacha Celestial Armor

## Anchor identity
- **Anchor:** GF-6* Karna
- **Cultural tradition:** south_asian (Vedic/Hindu; Mahabharata)
- **Tier discipline:** Tier S; Tier 1 broadly-fictionalized + heightened Vedic-Hindu curation awareness
- **Register:** mythological

## Heightened curation awareness notes
- Kavacha-kundala are the divine armor and earrings Karna was born with in the Mahabharata (gifts from his divine father Surya); they represent his divine birthright and the central moral tragedy of his character (he gave them away, exposing himself to mortality)
- Treatment here: kavacha as a secondary armor item in the epic-heroic tradition — armor pieces are documented game items in isekai/ARPG genres; Fate Grand Order depicts Karna wearing kavacha-kundala as a core part of his visual identity and Noble Phantasm defense
- Heightened curation applied: the kavacha-kundala are depicted respectfully as armor of divine birthright in epic-heroic context, NOT as a sacred religious ritual object to be used/discarded carelessly; the narrative of Karna giving them away is not replicated in-game mechanics in a way that demeans the sacrifice
- This item is armor_body_or_head subtype: per D1c, body/head armor is excluded from v1_scope auto-include; HOWEVER, as a Sketch F Tier S named anchor item it enters via D1b spirit (named-bearer anchor protection); note: weapon_kind_classified_subtype may need jack-ryan Gate-2 clarification on D1c armor exclusion vs named-bearer anchor override

## Cohesion-judge naming-space partitioning
- Pattern family: kavacha / kundala / vijaya / vasavi-shakti / suryaputra / radheya / sun-hero
- This entry: `karna_kavacha_armor` — kavacha (divine armor) as secondary armor item
- Player-facing: "Kavacha of the Sun-Hero" — Tier 1 with respectful depiction
- Discipline #25 rep-audit: kavacha-kundala is a broadly-fictionalized item in Mahabharata tradition; Fate Grand Order depicts it explicitly; south_asian representation is a stated gap (2.6% vs target 3-4%); this entry helps close that gap; no Mode-C contamination

## Mechanical profile rationale
- BC-axes cell: secondary armor item for Karna anchor
- proxy_attribute_class: STR (martial armor; STR-scaling defense)
- Pairs with Vijaya bow (armor + bow = the canonical Karna loadout before the sacrifice)
- Legendary-pair candidate: kavacha + Vijaya = Karna's divine birthright before Indra's exchange; composition policy § 6.4 legendary-pair set-bonus potential
- D1c note: flagged for jack-ryan Gate-2 review — body armor is normally D1c-excluded, but kavacha is a named Sketch F anchor item; per dispatch § 3.2 "Stage 4 mechanical-tagging fields" this item's subtype classification can be ratified at Wave 7; recommended: weapon_kind_classified_subtype = 'accessory_handheld' or a noted exception
- Sim-viability: secondary armor item; passes within BC envelope per Architecture B secondary slot

## D7 AI-tell compliance
- Templated: [kavacha armor noun] + [sun-hero divine birthright vocabulary] + [secondary defensive pairing] + [Mahabharata mythological period]
- Heightened curation: heroic-epic divine-armor framing; respectful; no demeaning use

## gandalf curation pass
- PASS — kavacha is core Karna identity; south_asian representation gap-fill value high; D1c subtype note flagged for jack-ryan Gate-2; heightened Vedic-Hindu curation applied correctly (divine armor depicted respectfully as heroic birthright, not sacred ritual object for casual use); Discipline #25 clean; no Tier 3 leak

## Wave 6 amendment 2026-05-25

**Authority:** jack-ryan Gate-2 PASS-WITH-AMENDMENTS verdict (Flag 1 WARN) — `agentic_orchestration/qa/findings/2026-05-25-gate2-stage-3-5-gap-fill.md`

**Amendment applied:**
- `weapon_kind_classified_subtype`: `accessory_handheld` -> `armor_body_or_head` (corrects D1c boundary per composition policy v1 § 1.1; kavacha is wearable body armor, not a hand-carriable accessory per off-hand-items doc § 1.4)
- `v1_scope`: `1` -> `0` (D1c excludes armor_body_or_head from v1_scope auto-include)
- `v1_scope_composition_trace.rule`: updated to `d1c_excluded_scope_deferred_karna_kavacha_named_bearer_rescue_candidate`

**Rationale:** The original `accessory_handheld` classification was a workaround to keep the entry in v1_scope via D1b; the off-hand-items doc § 1.4 defines `accessory_handheld` as focuses/talismans/hand-carriable ornaments — not wearable armor pieces. Kavacha is definitionally body armor (Karna born wearing it per Mahabharata; Fate Grand Order treats it as a wearable Noble Phantasm defense layer). The D1c exclusion is correct.

**Sidecar B / v1.1+ rescue-candidate status:** Entry preserved in substrate with full naming-space partition record (kavacha / kundala vocabulary slot). Flagged as a v1.1+ named-bearer anchor rescue candidate per Roland Durendal precedent — if composition policy v1 is amended to include `armor_hero_named` as a D1b subtype (or equivalent named-bearer armor override), this entry is the first rescue target. No data lost; no DB row deleted.

**Post-amendment Karna anchor profile:** 4 entries at v1_scope=1 (vijaya_bow, vasavi_shakti_spear, surya_sun_sword, mahabharata_chariot_lance) + 1 entry at v1_scope=0 (kavacha_armor, rescue-candidate). Consistent with dispatch § 3.2 named-bearer anchor protection intent.
