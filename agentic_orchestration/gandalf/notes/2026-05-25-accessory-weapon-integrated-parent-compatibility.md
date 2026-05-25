# Substrate-Fit Lookup — `accessory_weapon_integrated` → Parent Weapon Family Compatibility

**Date:** 2026-05-25
**Author:** gandalf (story-and-design steward)
**Status:** ACTIVE — Cycle 10 Stage 3 Phase 0b output; consumed by Phase 2 elrond sampler
**Authority:** Stage 3 execution dispatch (`agentic_orchestration/dispatches/2026-05-24-elrond-cycle-10-stage-3-v1-scope-materialization.md` § 3.3) FIRE-READY post-Gate-1 (commit `04509ad`)
**Companion docs:**
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` § 1.1 D1b (Main/Secondary auto-promote; subcategory `accessory_weapon_integrated`)
- `canonical/story/off-hand-items-2026-05-24.md` (Main/Secondary architecture)
- `agentic_orchestration/dispatches/2026-05-24-elrond-cycle-10-stage-3-v1-scope-materialization.md` § 4.1 D1b (parent-family fit gate)

---

## 0. TL;DR

Lookup mapping representative `accessory_weapon_integrated` candidates → compatible parent weapon families, used by Phase 2 elrond sampler to gate Tier-S `accessory_weapon_integrated` auto-promote against retained parent weapon families in `v1_scope`. Covers ~40 representative entries across ~10 weapon-family clusters (Japanese sword fittings, bow/crossbow accessories, historical firearm furniture, modern firearm furniture trimmed per Sketch D, universal sword/dagger fittings, polearm accessories, axe/haft fittings, sling/cord attachments). Remainder (~50% expected; D1b estimates ~30-50 `accessory_weapon_integrated` Tier-S rows total) handled by Phase 2 sampler default-disposition rule (§ 3 below).

**Composition policy § 1.1 D1b reference:** auto-promote rule `quality_tier = 'S' AND weapon_kind_classified_subtype = 'accessory_weapon_integrated'` is conditional on parent-family retention — i.e., a tsuba auto-promotes ONLY if at least one katana/wakizashi/tanto remains in v1_scope post-sampling. Sampler enforces via this lookup at v1_scope materialization.

---

## 1. Lookup table — structured data block (YAML)

```yaml
# Schema:
#   accessory_token: canonical name (lowercase; matches extraction patterns + likely substring matches against entry.canonical_name or description_text)
#   aliases: alternate names / spellings the sampler should match-against
#   parent_families: list of weapon-family tokens that, IF PRESENT in v1_scope, qualify the accessory for inclusion
#   parent_match_mode: 'any' (default — any single parent-family hit qualifies) | 'genre_filter_strict' (parent must also pass current genre filter)
#   genre_disposition: 'universal' (passes any era) | 'historical_pre_modern' | 'military_modern_deferred' (D1c-adjacent — flag but exclude unless military_modern lane retained)
#   rationale: 1-line design-rationale for the mapping
#   cultural_anchor: optional — primary cultural-tradition signal for the accessory (used by Phase 5 cohesion-judge sub-element flavor binding, not Phase 2 gating)

accessory_weapon_integrated_parent_compatibility:

  # === JAPANESE SWORD FITTINGS (East Asian Japanese tradition) ===
  # Cluster 1: Japanese sword furniture. Tight family — all bind to the katana/wakizashi/tanto/odachi cluster.
  - accessory_token: tsuba
    aliases: [sword_guard_japanese, japanese_hand_guard]
    parent_families: [katana, wakizashi, tanto, odachi, nodachi, uchigatana]
    parent_match_mode: any
    genre_disposition: universal
    rationale: Japanese-sword hand-guard; structurally bound to the nihonto family; legendary tsuba (e.g., Goto-school) anchor East Asian Japanese cultural-tradition Sketch F coverage.
    cultural_anchor: east_asian_japanese

  - accessory_token: menuki
    aliases: [hilt_ornament_japanese]
    parent_families: [katana, wakizashi, tanto, odachi, nodachi, uchigatana]
    parent_match_mode: any
    genre_disposition: universal
    rationale: Decorative hilt-ornament under tsukamaki binding on Japanese swords; substrate-resident named examples likely tied to Goto/Mino schools.
    cultural_anchor: east_asian_japanese

  - accessory_token: fuchi
    aliases: [fuchi_kashira, hilt_collar_japanese]
    parent_families: [katana, wakizashi, tanto, odachi, nodachi]
    parent_match_mode: any
    genre_disposition: universal
    rationale: Hilt-collar fitting paired with kashira on Japanese sword mountings; same family-binding as tsuba.
    cultural_anchor: east_asian_japanese

  - accessory_token: kashira
    aliases: [pommel_cap_japanese, hilt_butt_japanese]
    parent_families: [katana, wakizashi, tanto, odachi, nodachi]
    parent_match_mode: any
    genre_disposition: universal
    rationale: Pommel-cap on Japanese sword hilt; pairs with fuchi.
    cultural_anchor: east_asian_japanese

  - accessory_token: habaki
    aliases: [blade_collar_japanese]
    parent_families: [katana, wakizashi, tanto, odachi, nodachi]
    parent_match_mode: any
    genre_disposition: universal
    rationale: Blade-collar wedge fitting against saya; strictly bound to Japanese sword construction.
    cultural_anchor: east_asian_japanese

  - accessory_token: kozuka
    aliases: [utility_knife_japanese, kozuka_handle]
    parent_families: [katana, wakizashi, tanto]
    parent_match_mode: any
    genre_disposition: universal
    rationale: Small utility-knife slot integrated into saya; substrate-resident decorative kozuka are named-art objects bound to the sword they accompany.
    cultural_anchor: east_asian_japanese

  - accessory_token: sageo
    aliases: [sword_cord_japanese, saya_cord]
    parent_families: [katana, wakizashi, tanto, odachi]
    parent_match_mode: any
    genre_disposition: universal
    rationale: Cord lashing the saya to the obi; integral to Japanese sword wear; less commonly Tier-S but covered for completeness.
    cultural_anchor: east_asian_japanese

  # === BOW + CROSSBOW ACCESSORIES (Cell 7 Archer / Cell 10 Falconer + crossbow lineage) ===
  # Cluster 2: Ranged-DEX accessories. Quiver is the dominant Tier-S candidate (e.g., heroic-quiver named in mythological registers).
  - accessory_token: quiver
    aliases: [arrow_quiver, bolt_quiver]
    parent_families: [bow, longbow, recurve_bow, composite_bow, shortbow, crossbow, arbalest]
    parent_match_mode: any
    genre_disposition: universal
    rationale: Universal arrow/bolt-holder; substrate-resident named quivers (e.g., heroic-archer mythological quivers) bind directly to bow OR crossbow parent families.
    cultural_anchor: cross_cultural

  - accessory_token: bracer
    aliases: [arm_guard_archery, archer_bracer]
    parent_families: [bow, longbow, recurve_bow, composite_bow, shortbow]
    parent_match_mode: any
    genre_disposition: universal
    rationale: Archer's forearm guard against string-slap; functionally weapon-integrated though borderline armor — included per D1b boundary-call.
    cultural_anchor: cross_cultural

  - accessory_token: bowstring
    aliases: [string_bow]
    parent_families: [bow, longbow, recurve_bow, composite_bow, shortbow, crossbow]
    parent_match_mode: any
    genre_disposition: universal
    rationale: Integral component; named-mythological bowstrings (e.g., Heracles-bow string lore) qualify as substrate-resident.
    cultural_anchor: cross_cultural

  - accessory_token: windlass
    aliases: [crossbow_windlass, cranequin]
    parent_families: [crossbow, arbalest]
    parent_match_mode: any
    genre_disposition: historical_pre_modern
    rationale: Mechanical-spanning device for heavy crossbows; strictly crossbow-family-bound; European medieval / early-modern era.
    cultural_anchor: european_medieval

  - accessory_token: goats_foot_lever
    aliases: [goats_foot, spanning_lever_crossbow]
    parent_families: [crossbow]
    parent_match_mode: any
    genre_disposition: historical_pre_modern
    rationale: Lighter spanning-lever for crossbows; crossbow-only parent-binding.
    cultural_anchor: european_medieval

  - accessory_token: stirrup_crossbow
    aliases: [crossbow_stirrup]
    parent_families: [crossbow, arbalest]
    parent_match_mode: any
    genre_disposition: historical_pre_modern
    rationale: Foot-loop at crossbow prod for spanning leverage; crossbow-only.
    cultural_anchor: european_medieval

  # === HISTORICAL FIREARM FURNITURE (matchlock / wheellock / flintlock era — passes register=historical filter) ===
  # Cluster 3: Pre-percussion-cap firearm furniture. These ride the historical-register lane (~50-55% v1_scope share per § 2.1) and qualify when their parent firearm is retained.
  - accessory_token: powder_horn
    aliases: [powder_flask, priming_horn]
    parent_families: [matchlock, wheellock, flintlock, musket, arquebus, blunderbuss, pistol_historical]
    parent_match_mode: any
    genre_disposition: historical_pre_modern
    rationale: Black-powder priming/charge vessel; named historical powder-horns (named-bearer + provenance) are substrate-resident Tier-S candidates; binds to matchlock/wheellock/flintlock parents.
    cultural_anchor: european_early_modern

  - accessory_token: ramrod
    aliases: [scouring_stick, loading_rod]
    parent_families: [matchlock, wheellock, flintlock, musket, arquebus, rifle_muzzleloader, pistol_historical]
    parent_match_mode: any
    genre_disposition: historical_pre_modern
    rationale: Muzzleloader charging tool; intrinsic to pre-breechloader firearms.
    cultural_anchor: european_early_modern

  - accessory_token: flint
    aliases: [gun_flint, flint_lock_stone]
    parent_families: [flintlock, snaphance, miquelet, pistol_historical]
    parent_match_mode: any
    genre_disposition: historical_pre_modern
    rationale: Ignition-flint; flintlock-mechanism-only parent-binding.
    cultural_anchor: european_early_modern

  - accessory_token: matchcord
    aliases: [slow_match, match_cord]
    parent_families: [matchlock, arquebus]
    parent_match_mode: any
    genre_disposition: historical_pre_modern
    rationale: Smoldering cord for matchlock ignition; strictly matchlock-era.
    cultural_anchor: european_early_modern

  - accessory_token: bayonet
    aliases: [socket_bayonet, plug_bayonet, sword_bayonet]
    parent_families: [musket, arquebus, rifle_muzzleloader, rifle_historical, flintlock]
    parent_match_mode: any
    genre_disposition: historical_pre_modern
    rationale: Blade fitted to muzzle for thrust-defense; historical-era bayonets (e.g., Brown Bess socket bayonet) ride historical lane; military_modern bayonets are D1c-deferred.
    cultural_anchor: european_early_modern

  - accessory_token: bayonet_lug
    aliases: [bayonet_mount, lug_bayonet]
    parent_families: [rifle_historical, musket, rifle_muzzleloader]
    parent_match_mode: any
    genre_disposition: historical_pre_modern
    rationale: Mounting-fitting for bayonet attachment; same parent-family scope as bayonet itself.
    cultural_anchor: european_early_modern

  # === MODERN FIREARM FURNITURE (Sketch D D1b-trim — genre-disposition='military_modern_deferred' flags) ===
  # Cluster 4: Modern firearm accessories. These ride the military_modern lane (~5-8% v1_scope share per § 2.1) which is significantly trimmed. Sampler should DEFER unless military_modern parents are retained AND share-floor hasn't blown.
  - accessory_token: magazine
    aliases: [clip, ammo_magazine, detachable_magazine]
    parent_families: [rifle_modern, pistol_modern, submachine_gun, assault_rifle, military_modern]
    parent_match_mode: any
    genre_disposition: military_modern_deferred
    rationale: Modern-firearm ammo-feed; rides the military_modern lane (D1b trim); excluded unless military_modern parents retained per § 2.1 ~5-8% share.
    cultural_anchor: military_modern

  - accessory_token: scope
    aliases: [telescopic_sight, optical_sight, gun_scope, riflescope]
    parent_families: [rifle_modern, sniper_rifle, rifle_historical, military_modern]
    parent_match_mode: any
    genre_disposition: military_modern_deferred
    rationale: Magnified-optics sighting; primarily military_modern; pre-modern rifle scopes (early 1900s) edge-case may pass historical lane.
    cultural_anchor: military_modern

  - accessory_token: sling
    aliases: [rifle_sling, weapon_sling, gun_strap]
    parent_families: [rifle_modern, rifle_historical, musket, pole_arm, two_handed_weapon, military_modern]
    parent_match_mode: any
    genre_disposition: universal
    rationale: Carry-strap; spans modern AND historical firearm-carrying + two-handed-polearm carriage; universal disposition because it appears across eras.
    cultural_anchor: cross_cultural

  - accessory_token: suppressor
    aliases: [silencer, sound_suppressor]
    parent_families: [pistol_modern, rifle_modern, submachine_gun, military_modern]
    parent_match_mode: any
    genre_disposition: military_modern_deferred
    rationale: Modern muzzle-device; deferred per Sketch D military_modern trim.
    cultural_anchor: military_modern

  # === UNIVERSAL SWORD + DAGGER FITTINGS (Cell 1/3/4 melee STR + Cell 8/9 melee DEX) ===
  # Cluster 5: Generic sword/dagger furniture spanning European medieval + cross-cultural + Pan-Fantasy. Broadest parent-family scope.
  - accessory_token: pommel
    aliases: [sword_pommel, hilt_pommel, pommel_cap]
    parent_families: [sword, longsword, shortsword, arming_sword, broadsword, sabre, rapier, scimitar, dagger, falchion, claymore, zweihander, gladius]
    parent_match_mode: any
    genre_disposition: universal
    rationale: Counterweight + grip-cap at sword/dagger butt; named pommels (e.g., Pommel of the Sword of St. Maurice) are substrate-resident Tier-S; broad parent scope across all sword families.
    cultural_anchor: cross_cultural

  - accessory_token: crossguard
    aliases: [quillon, sword_guard, cross_guard]
    parent_families: [sword, longsword, shortsword, arming_sword, broadsword, claymore, zweihander, gladius, dagger, rapier_swept_hilt, sabre]
    parent_match_mode: any
    genre_disposition: universal
    rationale: Transverse hand-protection bar on European-style swords; ubiquitous across sword families.
    cultural_anchor: european_medieval

  - accessory_token: grip
    aliases: [hilt_grip, handle_wrap, sword_grip]
    parent_families: [sword, longsword, shortsword, dagger, sabre, rapier, scimitar, mace, axe, hammer]
    parent_match_mode: any
    genre_disposition: universal
    rationale: Wrapped handle-section on hafted/hilted weapons; broadest universal-parent scope.
    cultural_anchor: cross_cultural

  - accessory_token: scabbard
    aliases: [sheath, sword_scabbard]
    parent_families: [sword, longsword, shortsword, dagger, sabre, rapier, scimitar, katana, wakizashi, tanto, falchion]
    parent_match_mode: any
    genre_disposition: universal
    rationale: Blade-carrier; named scabbards (e.g., Avalon scabbard per legendary canonical-pair § 6.4) qualify as substrate-resident Tier-S AND seed canonical-pair set-bonus pairings.
    cultural_anchor: cross_cultural

  - accessory_token: chape
    aliases: [scabbard_tip, scabbard_chape]
    parent_families: [sword, longsword, shortsword, sabre, rapier, dagger]
    parent_match_mode: any
    genre_disposition: universal
    rationale: Metal tip-fitting on European scabbard; named historical examples may be substrate-resident.
    cultural_anchor: european_medieval

  - accessory_token: ricasso
    aliases: [ricasso_guard, blade_ricasso]
    parent_families: [longsword, zweihander, claymore, two_handed_sword, rapier]
    parent_match_mode: any
    genre_disposition: universal
    rationale: Unsharpened blade-section for half-swording grip; binds to longer European swords; edge-case Tier-S inclusion.
    cultural_anchor: european_medieval

  # === POLEARM ACCESSORIES (Cell 2 Light Fighter / Cell 6 Heavy Spearman) ===
  # Cluster 6: Polearm furniture.
  - accessory_token: langet
    aliases: [polearm_langet, side_strap]
    parent_families: [polearm, spear, halberd, pike, glaive, naginata, pollaxe, bardiche, voulge]
    parent_match_mode: any
    genre_disposition: historical_pre_modern
    rationale: Side-straps reinforcing head-to-haft junction on polearms; prevents shearing; substrate-resident on European medieval polearms.
    cultural_anchor: european_medieval

  - accessory_token: ferrule
    aliases: [butt_cap, polearm_butt]
    parent_families: [polearm, spear, halberd, pike, glaive, naginata, quarterstaff]
    parent_match_mode: any
    genre_disposition: universal
    rationale: Metal cap at non-bladed haft end; structural reinforcement.
    cultural_anchor: cross_cultural

  - accessory_token: butt_spike
    aliases: [haft_spike, polearm_spike]
    parent_families: [polearm, spear, halberd, pike, naginata]
    parent_match_mode: any
    genre_disposition: historical_pre_modern
    rationale: Pointed butt-end for opportunistic offensive use; pikes and spears especially.
    cultural_anchor: european_medieval

  # === AXE + HAFT-WEAPON FITTINGS (Cell 1 Heavy Barbarian / Cell 4 Defender) ===
  # Cluster 7: Axe + mace haft furniture.
  - accessory_token: haft_wrap
    aliases: [axe_grip_wrap, haft_binding]
    parent_families: [axe, battle_axe, dane_axe, war_hammer, mace, club]
    parent_match_mode: any
    genre_disposition: universal
    rationale: Wrapped grip-section on axe/mace haft for traction; universal across two-handed haft weapons.
    cultural_anchor: cross_cultural

  - accessory_token: axe_head_langet
    aliases: [axe_langet]
    parent_families: [axe, battle_axe, dane_axe, pollaxe]
    parent_match_mode: any
    genre_disposition: historical_pre_modern
    rationale: Reinforcement straps from axe-head down the haft; analogous to polearm langet but axe-specific.
    cultural_anchor: european_medieval

  # === WHIP + FLAIL ATTACHMENTS (Cell 24/25 WIS pet-master + Cell 8 DEX hybrid) ===
  # Cluster 8: Flexible-weapon hardware. Sparse substrate but covered for completeness.
  - accessory_token: flail_head
    aliases: [morning_star_head, flail_ball, flail_weight]
    parent_families: [flail, military_flail, chain_flail, morning_star_flail]
    parent_match_mode: any
    genre_disposition: historical_pre_modern
    rationale: Striking-head on chain-end of flail; integral; substrate-resident edge-case.
    cultural_anchor: european_medieval

  - accessory_token: chain_link
    aliases: [flail_chain, nunchaku_chain]
    parent_families: [flail, nunchaku, kusarigama, manriki_gusari]
    parent_match_mode: any
    genre_disposition: universal
    rationale: Linking-chain on flail-family weapons; East Asian (nunchaku/kusarigama) + European (flail) cross-cultural span.
    cultural_anchor: cross_cultural

  # === SLINGS + STRAPS (universal carriage) ===
  # Cluster 9: Already covered under sling above (cluster 4) for firearms; this entry covers polearm/two-handed cross-binding.
  # (Sling is handled above; no separate entry needed.)

  # === SPECIALTY / NAMED-MYTHOLOGICAL ANCHORS ===
  # Cluster 10: Catch-all for named-mythological accessories whose parent is itself a named mythological weapon.
  - accessory_token: mythological_bowstring_named
    aliases: [heracles_bowstring, named_bowstring]
    parent_families: [bow_mythological, named_bow]
    parent_match_mode: any
    genre_disposition: universal
    rationale: Named mythological bowstrings (e.g., Heracles-bow string lore); parent must be substrate-resident named mythological bow.
    cultural_anchor: greek_mythological

  - accessory_token: named_scabbard_paired_legendary
    aliases: [avalon_scabbard, legendary_scabbard]
    parent_families: [sword_named_legendary, excalibur, kusanagi, durendal, joyeuse]
    parent_match_mode: any
    genre_disposition: universal
    rationale: Per composition policy § 6.4 legendary canonical-pair set-bonus — named scabbards pair with named legendary swords; parent-binding to specific named-sword Tier-S rows.
    cultural_anchor: cross_cultural

  - accessory_token: named_pommel_paired_legendary
    aliases: [pommel_relic, legendary_pommel]
    parent_families: [sword_named_legendary, longsword_named, named_sword]
    parent_match_mode: any
    genre_disposition: universal
    rationale: Edge-case relic-pommels (e.g., Pommel of the Sword of St. Maurice) bind to specific named legendary swords; rare but substrate-resident.
    cultural_anchor: european_medieval
```

---

## 2. Coverage estimate

| Cluster | Entries | Expected substrate-Tier-S coverage |
|---|---|---|
| 1. Japanese sword fittings | 7 | High — Goto/Mino schools well-attested; ~5-10 substrate rows likely |
| 2. Bow + crossbow accessories | 6 | Mid — quiver + bowstring + bracer common; crossbow-spanning gear rarer |
| 3. Historical firearm furniture | 6 | High — powder-horn / ramrod / flint / bayonet common in royal_armouries + Met substrate |
| 4. Modern firearm furniture (D1b-deferred) | 4 | Mid but mostly excluded — military_modern lane trimmed per § 2.1 |
| 5. Universal sword + dagger fittings | 6 | High — pommel + crossguard + scabbard especially; ~10-15 substrate rows likely |
| 6. Polearm accessories | 3 | Mid — langet + ferrule + butt-spike |
| 7. Axe + haft fittings | 2 | Low-mid — haft-wrap + langet |
| 8. Whip + flail attachments | 2 | Low — flail-head + chain-link sparse |
| 10. Specialty / named-mythological anchors | 3 | Low but high-value — paired-legendary set-bonus seeds per § 6.4 |
| **Total entries** | **~40** | **~30-50 substrate Tier-S rows expected** (matches composition policy D1b § 1.1 estimate of 30-50 `accessory_weapon_integrated` rows) |

---

## 3. Phase 2 sampler integration

### 3.1 Default disposition for unmatched accessories

For `accessory_weapon_integrated` rows whose extracted_canonical_name OR description_text does NOT match any `accessory_token` or `aliases` in this lookup:

- **Default rule:** include in v1_scope ONLY if `quality_tier = 'S'` AND at least one sword OR bow OR polearm OR axe OR firearm parent-family is retained in v1_scope (broadest weapon-family-presence check)
- **Rationale:** ~50% of `accessory_weapon_integrated` Tier-S rows are expected to be enumerable via this lookup; remaining ~50% (idiosyncratic / Pan-Fantasy / catch-all) ride the broad-presence default
- **Composition trace:** `composition_trace.notes = "accessory_weapon_integrated default-disposition; no specific parent-token match"`

### 3.2 Match mechanics

- **String matching:** case-insensitive substring match against (a) `canonical_name`, (b) `description_text`, (c) `extracted_named_bearer` (Stage 1.5 column) — token + aliases scored together; first hit wins
- **Parent retention check:** for matched accessory, query v1_scope state for ANY `weapon_kind_classified_subtype = 'handheld_weapon'` row whose family-signal matches `parent_families`; family-signal source is Stage 1 proxy_attribute_class + canonical_name substring match (e.g., "katana" in canonical_name → katana family)
- **Genre-disposition gate:** if `genre_disposition = 'military_modern_deferred'`, accessory enters v1_scope ONLY if per-axis military_modern share is below § 2.1 ~5-8% floor AND parent military_modern weapon is retained
- **Cultural-anchor signal:** NOT a Phase 2 gate; passed to Phase 5 cohesion-judge for sub-element flavor binding per composition policy § 6.5

### 3.3 Edge cases

- **Cross-family universal accessories (pommel, grip, scabbard, sling):** any single sword/dagger/firearm parent retention qualifies — no per-family gating
- **Strictly-bound accessories (tsuba, habaki, windlass, matchcord, flint):** parent-family list is exhaustive — if NO listed parent is retained, exclude from v1_scope
- **Named-mythological-paired accessories (Avalon scabbard, etc.):** parent must be the SPECIFIC named legendary weapon — not generic family. These compose into legendary canonical-pair set-bonus pairings per composition policy § 6.4 and feed downstream loot-architecture canonical doc

### 3.4 Spot-check guidance for gandalf Gate-2 / Matt sign-off

When reviewing the Phase 3 distribution report, audit:

1. **Tsuba / menuki / habaki count vs katana family count:** if any of these auto-promoted but katana family is empty in v1_scope, that's a BLOCK (lookup-fit violation)
2. **Powder-horn / ramrod count vs flintlock/musket family count:** same parent-retention sanity
3. **Modern accessories (magazine / scope / suppressor) count vs military_modern lane share:** if military_modern share is at floor (~5-8%) but modern-accessory count is disproportionate, sampler trim weight needs adjustment
4. **Named legendary scabbard/pommel count vs named-legendary-sword count:** check legendary canonical-pair coverage seeds for downstream loot-architecture

---

## 4. Open questions parked for downstream phases (not blocking Phase 2)

| Question | Routing |
|---|---|
| Does Stage 4 mythological-NULL rescue add accessory_weapon_integrated rows? | rocket + gamora + jack-ryan Stage 4 dispatch — re-run this lookup against rescued rows post-Stage-4 |
| How does Phase 5 cohesion-judge bind cultural_anchor signal here to sub-element flavor? | Phase 5 cohesion-judge calibration spec (post-Cycle-10 canonical authoring queue per dispatch § 6 out-of-scope) |
| Should the lookup grow into a substrate column at v1.1+? | v1.1+ queue item — accessory_token + parent_families could become extracted_* columns on weapon_knowledge_entries for sampler determinism |
| Do paired-legendary entries (Avalon scabbard, etc.) need a separate `paired_legendary_with_substrate_entry_id` column? | Loot-architecture canonical doc (post-Cycle-10 queue per dispatch § 6) — set-bonus regime-change is gameplay-layer concern beyond v1_scope |

---

## 5. Cross-references

- Composition policy v1: `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` § 1.1 D1b (Main/Secondary auto-promote), § 2.1 (register share targets), § 6.4 (legendary canonical-pair set-bonuses), § 6.5 (sub-element flavor at LLM-runtime)
- Stage 3 execution dispatch: `agentic_orchestration/dispatches/2026-05-24-elrond-cycle-10-stage-3-v1-scope-materialization.md` § 3.3 (Phase 0b output spec), § 4.1 D1b (parent-family fit gate)
- Off-hand items architecture: `canonical/story/off-hand-items-2026-05-24.md` (Main/Secondary; weapon-integrated accessory category)
- Sketch F anchors: `canonical/story/v1-bc-target-intent-2026-05-24.md` § 5 + composition policy § 5.2
- Cycle 10 state: `agentic_orchestration/weapon-substrate-curation-cycle-10-state.md`
- Cycle 10 scope: `agentic_orchestration/cycles/cycle-10-hive-mind-scope.md`

---

## 6. Sign-off

**Author:** gandalf (story-and-design steward)
**Authority:** Stage 3 execution dispatch FIRE-READY § 3.3 + composition policy v1 § 1.1 D1b
**Status:** ACTIVE — Phase 2 elrond sampler consumes this artifact at v1_scope materialization
**Re-engagement gate:** Phase 3 distribution report; if accessory_weapon_integrated coverage materially deviates (>±20% from D1b § 1.1 estimate of 30-50 rows), this lookup re-engages for amendment; Stage 4 mythological-NULL rescue may add accessory rows requiring re-lookup
