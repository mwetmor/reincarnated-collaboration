# VDM-2 Compendium — gd (41 kits)

> **Source:** `corpus.db` `kit_master` view (574) ENRICHED live with the six VDM-2 side-car blocks + two registries (render-layer joins; DB never mutated). **v2.0** · db md5 `bebc933b0bf9bcab5988bbc16bcc55b4` · generated 2026-07-22T09:46:42Z.
> `court` is the reconciled element court (enum-checked); `original_element` carries raw provenance. Raw mobile-era descriptors (`elem_raw`) are NOT exposed (provenance-only). `kit_citations` is the sole citation authority.

| grade | n | verify (C/X/U) | dossier | cited | geom-bands | hooks |
|---|---|---|---|---|---|---|
| E 9 · C 23 · A 3 · G 6 | 41 | 164/13/33 | 246 | 41/41 | 73 | 70 |

## gd-blade-arc-warder — Blade Arc Warder `[class:record]`

- **grade / terminal:** `EXACT` / `MAPPED`
- **element (court):** physical · _raw_: bleed
- **elements attested:** _(silent)_
- **ailments attested:** bleed
- **eras:** base-2016;patch-1.1-1.2 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 0 · **dossier rows:** 6
- **citations (2):** [authored] forums.crateentertainment.com · @Allan_Ashcroft · https://forums.crateentertainment.com/t/1-2-0-3-big-bleed-easy-blade-arc-warder-ravager-callagadra-sr90/133802; [authored] forums.crateentertainment.com · @The_Coyote · https://forums.crateentertainment.com/t/1-1-9-7-1-1-9-8-budget-physical-blade-arc-s-b-warder-sr80-ravager-of-minds/127745
- **t4 doors:** `PERSISTENCE_ENGINE_saturation`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Blade Arc**: delivery=melee_arc, range=melee, width=wide, motion_signature=arc_sweep, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Blade Arc Warder: melee arc melee_arc identity — _expressed by_ `geometry.delivery_class`
- **acceptance asserts:**
  - `primary_delivery_class == 'melee_arc'` [green]

## gd-drain-essence-spellbinder — Drain Essence Spellbinder `[class:record]`

- **grade / terminal:** `EXACT` / `MAPPED`
- **element (court):** chaos-poison · _raw_: vitality
- **elements attested:** shadow
- **ailments attested:** drain
- **eras:** aom-2017;patch-1.1-1.2 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 1 · **dossier rows:** 6
- **citations (3):** [communal] forums.crateentertainment.com · @unknown · https://forums.crateentertainment.com/t/1-1-4-2-aether-drain-essence-spellbinder/89110; [communal] forums.crateentertainment.com · @unknown · https://forums.crateentertainment.com/t/1-1-7-1-bro-do-you-even-leech-drain-essence-spellbinder-facetank-all-ravagers-sr80/100976; [authored] gametyrant.com · @unknown · https://gametyrant.com/news/grim-dawn-ashes-of-malmouth-is-a-necromancers-dream
- **t4 doors:** `PERSISTENCE_ENGINE_uptime`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Drain Essence**: delivery=beam, cadence=channel, motion_signature=straight_line, count=1, chain=2 · conf 0.75
  - `#1` **Mark of Torment**: delivery=aura, range=self, cadence=cooldown, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Drain Essence Spellbinder: beam channel beam identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] shadow element register — _expressed by_ `element:shadow`
- **acceptance asserts:**
  - `primary_delivery_class == 'beam'` [green]

## gd-flames-of-ignaffar-purifier — Flames of Ignaffar Purifier `[class:record]`

- **grade / terminal:** `EXACT` / `MAPPED`
- **element (court):** fire · _raw_: fire
- **elements attested:** fire
- **ailments attested:** burn
- **eras:** aom-2017;patch-1.1-1.2 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 2 · **dossier rows:** 6
- **citations (2):** [communal] forums.crateentertainment.com · @unknown · https://forums.crateentertainment.com/t/1-1-7-2-the-fire-coneman-fire-flames-of-ignaffar-purifier-focused-on-conversion/102294; [authored] mmos.com · @unknown · https://mmos.com/news/grim-dawn-ashes-of-malmouth-october-11
- **t4 doors:** `PERSISTENCE_ENGINE_uptime`, `ELEMENT_CONVERSION_MONO`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Flames of Ignaffar**: delivery=zone, width=wide, cadence=channel, motion_signature=fan_spread, count=1 · conf 0.75
  - `#1` **Inquisitor Seal**: delivery=zone, motion_signature=ground_place, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Flames of Ignaffar Purifier: cone zone identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]

## gd-phantasmal-blades-witch-hunter — Phantasmal Blades Witch Hunter `[class:record]`

- **grade / terminal:** `EXACT` / `MAPPED`
- **element (court):** chaos-poison · _raw_: vitality
- **elements attested:** earth,shadow
- **ailments attested:** _(none)_
- **eras:** base-2016;patch-1.1-1.2 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 0 · **dossier rows:** 6
- **citations (1):** [communal] forums.crateentertainment.com · @unknown · https://forums.crateentertainment.com/t/1-2-1-6-green-knives-galore-acid-poison-phantasmal-blades-witch-hunter/151949
- **t4 doors:** `ELEMENT_CONVERSION_MONO`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Phantasmal Blades**: delivery=projectile, range=long, cadence=spam, motion_signature=fan_spread, count=1, pierce=all · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Phantasmal Blades Witch Hunter: multi projectile projectile identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] shadow element register — _expressed by_ `element:shadow`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]

## gd-ravenous-earth-oppressor — Ravenous Earth Oppressor `[class:record]`

- **grade / terminal:** `EXACT` / `MAPPED`
- **element (court):** chaos-poison · _raw_: vitality
- **elements attested:** shadow
- **ailments attested:** curse:sap,drain
- **eras:** fg-2019;patch-1.1-1.2 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 0 · **dossier rows:** 6
- **citations (1):** [communal] forums.crateentertainment.com · @Nery · https://forums.crateentertainment.com/t/1-1-1-2-1-1-6-2-beginners-vitality-ravenous-earth-oppressor-with-leveling-guide/50493
- **t4 doors:** `ZONE_CONTROL`, `PERSISTENCE_ENGINE_saturation`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Ravenous Earth**: delivery=zone, cadence=cooldown, motion_signature=ground_place, count=1 · conf 0.75
  - `#1` **Celestial Presence + Spectral Wrath (mastery RR passives)**: delivery=aura, range=self, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Ravenous Earth Oppressor: ground targeted circle zone identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] shadow element register — _expressed by_ `element:shadow`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]

## gd-righteous-fervor-dervish — Righteous Fervor Dervish `[class:record]`

- **grade / terminal:** `EXACT` / `MAPPED`
- **element (court):** chaos-poison · _raw_: acid
- **elements attested:** earth
- **ailments attested:** curse:sap
- **eras:** fg-2019;patch-1.1-1.2 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 1 · **dossier rows:** 6
- **citations (2):** [communal] forums.crateentertainment.com · @unknown · https://forums.crateentertainment.com/t/1-1-8-1-edgyswingsetacid-dw-righteous-fervor-dervish-sr-90-4-50-crucible-avatar-ravager-crate/99684; [communal] steamcommunity.com · @unknown · https://steamcommunity.com/sharedfiles/filedetails/?l=german&id=1781921985
- **t4 doors:** `ELEMENT_CONVERSION_MONO`, `MOMENTUM_CASCADE`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Righteous Fervor**: delivery=melee_arc, range=melee, speed=fast, motion_signature=point_strike, count=1 · conf 0.75
  - `#1` **Night's Chill (aura)**: delivery=aura, range=self, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Righteous Fervor Dervish: melee strike melee_arc identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] earth element register — _expressed by_ `element:earth`
- **acceptance asserts:**
  - `primary_delivery_class == 'melee_arc'` [green]

## gd-savagery-warder — Savagery Warder `[class:record]`

- **grade / terminal:** `EXACT` / `MAPPED`
- **element (court):** lightning · _raw_: lightning
- **elements attested:** lightning
- **ailments attested:** _(none)_
- **eras:** base-2016;patch-1.1-1.2 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 1 · **dossier rows:** 6
- **citations (1):** [communal] forums.crateentertainment.com · @Archangel2245 · https://forums.crateentertainment.com/t/warder-soldier-shaman/46257
- **t4 doors:** `TEMPORAL_CHARGE`, `MOMENTUM_CASCADE`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Savagery**: delivery=melee_arc, range=melee, motion_signature=point_strike, count=1 · conf 0.75
  - `#1` **Wendigo Totem**: delivery=summon_delegate, cadence=cooldown, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Savagery Warder: melee strike melee_arc identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] lightning element register — _expressed by_ `element:lightning`
- **acceptance asserts:**
  - `primary_delivery_class == 'melee_arc'` [green]

## gd-stun-jacks — Stun Jacks (launch era) `[NEGATIVE, class:record]`

- **grade / terminal:** `EXACT` / `MAPPED`
- **element (court):** lightning · _raw_: lightning
- **elements attested:** lightning
- **ailments attested:** _(none)_
- **eras:** base-2016;aom-2017 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 1 · **dossier rows:** 6
- **citations (3):** [communal] forums.crateentertainment.com · @x1x1x1x2 · https://forums.crateentertainment.com/t/1-0-3-2-cdr-stun-jacks-sorcerer-a-gladiator-viable-build/43274; [communal] forums.crateentertainment.com · @afanasenkov26 · https://forums.crateentertainment.com/t/1-1-4-2-1-1-6-2-caster-electrify-my-life-stun-jacks-purifier-c-sr/89028; [communal] forums.crateentertainment.com · @unknown · https://forums.crateentertainment.com/t/caster-1-0-6-1-stun-jacks-purifier-lokarr-30-seconds/46116 (archive: http://web.archive.org/web/20220519085600/https://forums.crateentertainment.com/t/caster-1-0-6-1-stun-jacks-purifier-lokarr-30-seconds/46116)
- **t4 doors:** `GEOMETRY_COLLAPSE`, `ELEMENT_CONVERSION_MONO`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Stun Jacks**: delivery=projectile, range=short, width=wide, cadence=spam, motion_signature=fan_spread, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Stun Jacks (launch era): multi projectile projectile identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] lightning element register — _expressed by_ `element:lightning`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]

## gd-vires-might-shieldbreaker — Vire's Might Shieldbreaker `[class:record]`

- **grade / terminal:** `EXACT` / `MAPPED`
- **element (court):** fire · _raw_: fire
- **elements attested:** fire
- **ailments attested:** burn
- **eras:** fg-2019;patch-1.1-1.2 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 1 · **dossier rows:** 6
- **citations (2):** [communal] forums.crateentertainment.com · @unknown · https://forums.crateentertainment.com/t/1-1-2-5-zigzag-shieldbreaker/50323; [official] forums.crateentertainment.com · @unknown · https://forums.crateentertainment.com/t/forgotten-gods-what-we-know-about-the-oathkeeper-skills/47953
- **t4 doors:** `PERSISTENCE_ENGINE_uptime`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Vire's Might**: delivery=motion, cadence=spam, motion_signature=straight_line, count=1 · conf 0.75
  - `#1` **Thermite Mines**: delivery=zone, motion_signature=ground_place, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Vire's Might Shieldbreaker: dash attack motion identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **acceptance asserts:**
  - `primary_delivery_class == 'motion'` [green]

## gd-aar-spellbinder — Albrecht's Aether Ray Spellbinder `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** lightning · _raw_: aether
- **elements attested:** lightning
- **ailments attested:** _(none)_
- **eras:** aom-2017;fg-2019;patch-1.1-1.2 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 1 / 0 · **dossier rows:** 6
- **citations (2):** [authored] forums.crateentertainment.com · @Nery · https://forums.crateentertainment.com/t/1-1-9-3-beginners-albrechts-aether-ray-spellbinder/112241; [authored] forums.crateentertainment.com · https://forums.crateentertainment.com/t/all-of-my-friends-are-dead-and-i-have-a-laser-spellbinder-1-0-2-1/41696
- **t4 doors:** `PERSISTENCE_ENGINE_uptime`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Albrecht's Aether Ray**: delivery=beam, cadence=channel, motion_signature=straight_line, count=1, pierce=all · conf 0.75
  - `#1` **Mirror of Ereoctes**: delivery=aura, range=self, cadence=cooldown, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Albrecht's Aether Ray Spellbinder: beam channel beam identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] lightning element register — _expressed by_ `element:lightning`
- **deviations:**
  - [accepted_downgrade] minor drift: the source player experiences a hard energy-management pressure and a rooted-while-channeling commitment; · downgrade-owner `elrond (W4 GD tranche; internal-consistency reconcile, no W1 evidence — W5 is GD's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'beam'` [green]
- **mapping deviation notes:** minor drift: the source player experiences a hard energy-management pressure and a rooted-while-channeling commitment; PERSISTENCE_ENGINE_uptime approximates the sustained-beam identity but the engine has no literal aether-ray, so the beam is mapped as a channeled piercing line. No status lost (none attested).

## gd-aegis-paladin — Aegis of Menhir Paladin `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** fire · _raw_: fire
- **elements attested:** fire
- **ailments attested:** _(none)_
- **eras:** fg-2019;patch-1.1-1.2 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 1 · **dossier rows:** 6
- **citations (2):** [authored] forums.crateentertainment.com · @Ulvar1 · https://forums.crateentertainment.com/t/1-1-8-1-fire-shield-throw-paladin-from-scratch-build-journal-and-guide/105073; [communal] forums.crateentertainment.com · https://forums.crateentertainment.com/t/forgotten-gods-what-we-know-about-the-new-mastery/46822
- **t4 doors:** `GEOMETRY_PROPAGATION_overkill`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Aegis of Menhir**: delivery=projectile, motion_signature=ricochet_return, count=1 · conf 0.75
  - `#1` **Inquisitor Seal**: delivery=aura, range=self, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Aegis of Menhir Paladin: ricochet bounce projectile identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **deviations:**
  - [accepted_downgrade] minor drift: the out-and-return boomerang leg is a signature the source player feels (shield comes back) but the engine ricochet_bounce geometry does not model the return path -- filed as out-and-return accrual, geometry approximates the outbound hop only. · downgrade-owner `elrond (W4 GD tranche; internal-consistency reconcile, no W1 evidence — W5 is GD's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]
- **mapping deviation notes:** minor drift: the out-and-return boomerang leg is a signature the source player feels (shield comes back) but the engine ricochet_bounce geometry does not model the return path -- filed as out-and-return accrual, geometry approximates the outbound hop only. No status lost (none attested).

## gd-belgothian-blademaster — Belgothian Blademaster `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** physical · _raw_: pierce
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** aom-2017;fg-2019;patch-1.1-1.2 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 1 / 0 · **dossier rows:** 6
- **citations (2):** [authored] forums.crateentertainment.com · @lMarcusl · https://forums.crateentertainment.com/t/1-1-9-8-1-2-0-2-build-overview-belgothian-blademaster-sr75-80/127760; [communal] forums.crateentertainment.com · @Stupid_Dragon · https://forums.crateentertainment.com/t/build-compendium-ix-ashes-of-malmouth/47681
- **t4 doors:** `ELEMENT_CONVERSION_PHYSICAL`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Cadence (default) / WPS suite**: delivery=melee_arc, range=melee, motion_signature=point_strike, count=1, pierce=all · conf 0.75
  - `#1` **Blade Spirit**: delivery=motion, motion_signature=orbit_fixed, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Belgothian Blademaster: melee strike melee_arc identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] minor drift: the WPS suite is the source player's core texture (a rotating pool of weapon procs firing every swing) but the engine models it as a single on-hit-threshold burst rider rather than a named pool of distinct procs, since no individual WPS payload was fetched. · downgrade-owner `elrond (W4 GD tranche; internal-consistency reconcile, no W1 evidence — W5 is GD's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'melee_arc'` [green]
- **mapping deviation notes:** minor drift: the WPS suite is the source player's core texture (a rotating pool of weapon procs firing every swing) but the engine models it as a single on-hit-threshold burst rider rather than a named pool of distinct procs, since no individual WPS payload was fetched. Blade Spirit's autonomy is under-attested, mapped as orbit rather than pet. No status lost.

## gd-bloody-pox-conjurer — Bloody Pox Conjurer `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** chaos-poison · _raw_: vitality
- **elements attested:** shadow
- **ailments attested:** _(none)_
- **eras:** base-2016;patch-1.1-1.2 · **tier:** T1 · **lineage:** genre/rabies
- **verify (C/X/U):** 3 / 0 / 2 · **dossier rows:** 6
- **citations (2):** [authored] forums.crateentertainment.com · @MergosWetNurse · https://forums.crateentertainment.com/t/1-1-7-0-bloody-madness-fevered-rage-bloody-pox-conjurer-sr-80-gladiator-150-170/100806; [official] grimdawn.com · https://www.grimdawn.com/guide/character/masteries/occultist/
- **t4 doors:** `PERSISTENCE_ENGINE_saturation`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Bloody Pox**: delivery=projectile, motion_signature=straight_line, count=1 · conf 0.75
  - `#1` **Wendigo Totem**: delivery=summon_delegate, cadence=cooldown, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Bloody Pox Conjurer: single target projectile identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] shadow element register — _expressed by_ `element:shadow`
- **deviations:**
  - [accepted_downgrade] minor drift: the signature the source player feels is the plague JUMPING through a dense pack (contagion), which the engine single_target geometry does not model -- mapped as single-cast + spread note per precedent. · downgrade-owner `elrond (W4 GD tranche; internal-consistency reconcile, no W1 evidence — W5 is GD's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]
- **mapping deviation notes:** minor drift: the signature the source player feels is the plague JUMPING through a dense pack (contagion), which the engine single_target geometry does not model -- mapped as single-cast + spread note per precedent. Two near-misses withheld (no forcing): a vitality-decay DoT status (not named in fetched -- theme != status) and Curse of Frailty's RR token (application shape unanchored). No status emitted.

## gd-bwc-demolitionist — Blackwater Cocktail Demolitionist `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** fire · _raw_: fire
- **elements attested:** fire
- **ailments attested:** blind,burn
- **eras:** base-2016;patch-1.1-1.2 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 0 · **dossier rows:** 6
- **citations (2):** [communal] forums.crateentertainment.com · https://forums.crateentertainment.com/t/blackwater-cocktail-or-thermite-mines/33838; [authored] forums.crateentertainment.com · https://forums.crateentertainment.com/t/1-1-8-1-watch-cairn-burn-infernal-knight-blackwater-cocktail-thermite-mines-canister-bombs-grenade-purifier-celestial-killer-crate-ravager-mogdrogen-calla-cruci-150-170-sr-75-76/106390
- **t4 doors:** `PERSISTENCE_ENGINE_saturation`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Blackwater Cocktail**: delivery=zone, width=wide, motion_signature=ground_place, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Blackwater Cocktail Demolitionist: ground targeted circle zone identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **deviations:**
  - [accepted_downgrade] minor drift: the source player lays overlapping burning ground carpets and debuffs with fumble + RR -- blind (fumble) is captured, but the fire-DoT's 'burn' flavor is withheld (not named as a status) and Thermite's RR token is withheld (application shape unanchored). · downgrade-owner `elrond (W4 GD tranche; internal-consistency reconcile, no W1 evidence — W5 is GD's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
- **mapping deviation notes:** minor drift: the source player lays overlapping burning ground carpets and debuffs with fumble + RR -- blind (fumble) is captured, but the fire-DoT's 'burn' flavor is withheld (not named as a status) and Thermite's RR token is withheld (application shape unanchored). The molotov-carpet ground zone maps cleanly to ground_targeted_circle; the two withholds are near-misses, not silent drops.

## gd-cadence-witchblade — Cadence Witchblade `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** base-2016;patch-1.1-1.2 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 0 · **dossier rows:** 6
- **citations (2):** [authored] forums.crateentertainment.com · @jajaja · https://forums.crateentertainment.com/t/1-0-0-4-cadence-witchblade-100-unkillable-100-faceroll-build/33398; [authored] forums.crateentertainment.com · https://forums.crateentertainment.com/t/1-1-9-1-budget-physical-cadence-blitz-s-b-witchblade/111542
- **t4 doors:** `MOMENTUM_CASCADE`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Cadence**: delivery=melee_arc, range=melee, motion_signature=point_strike, count=1 · conf 0.75
  - `#1` **Blitz**: delivery=motion, motion_signature=straight_line, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Cadence Witchblade: melee strike melee_arc identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] minor drift: the source player feels the swing-count rhythm building to a periodic detonation (every 3rd swing) -- the engine has no native every-Nth-swing accumulator, so it is filed as a two-tier-accumulator family accrual and approximated via trigger_grammar, not delivered natively. · downgrade-owner `elrond (W4 GD tranche; internal-consistency reconcile, no W1 evidence — W5 is GD's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'melee_arc'` [green]
- **mapping deviation notes:** minor drift: the source player feels the swing-count rhythm building to a periodic detonation (every 3rd swing) -- the engine has no native every-Nth-swing accumulator, so it is filed as a two-tier-accumulator family accrual and approximated via trigger_grammar, not delivered natively. Curse of Frailty's RR token is withheld (shape unanchored). No status emitted. Stays terminal MAPPED (CLOSE with a family-accrual candidate) per R-M7.

## gd-callidors-tempest-templar — Callidor's Tempest Templar `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** lightning · _raw_: aether
- **elements attested:** fire,lightning
- **ailments attested:** burn
- **eras:** fg-2019;patch-1.1-1.2 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 3 / 1 / 0 · **dossier rows:** 6
- **citations (3):** [authored] forums.crateentertainment.com · @WyreZ · https://forums.crateentertainment.com/t/1-1-9-8-callidors-holy-hammer-1-14m-callidors-tempest-crucible-150-sr-76/127806; [communal] forums.crateentertainment.com · https://forums.crateentertainment.com/t/forgotten-gods-what-we-know-about-the-new-mastery/46822; [communal] steamcommunity.com · https://steamcommunity.com/app/219990/discussions/0/451850213950176826/
- **t4 doors:** `GEOMETRY_COLLAPSE`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Callidor's Tempest**: delivery=zone, range=short, motion_signature=burst_around_self, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Callidor's Tempest Templar: ring zone identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **deviations:**
  - [accepted_downgrade] minor drift: the source player accepts a hard range/target-size restriction (must be point-blank; · downgrade-owner `elrond (W4 GD tranche; internal-consistency reconcile, no W1 evidence — W5 is GD's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
- **mapping deviation notes:** minor drift: the source player accepts a hard range/target-size restriction (must be point-blank; only hits human-sized mobs) as the cost of a strong pulse -- the engine ring geometry delivers the point-blank burst but does not model the human-size gate. The aether-fire composite is compressed to fire-primary + lightning-secondary. burn is captured (named). Minor composite-element drift.

## gd-canister-saboteur — Canister Bomb Saboteur `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** fire · _raw_: fire
- **elements attested:** fire
- **ailments attested:** bleed
- **eras:** base-2016;patch-1.1-1.2 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 0 · **dossier rows:** 6
- **citations (2):** [authored] forums.crateentertainment.com · @chillstepbbc · https://forums.crateentertainment.com/t/1-0-0-9-saboteur-the-grenado-gunslinger-caster-gunslinger/38302; [authored] forums.crateentertainment.com · @Torzini · https://forums.crateentertainment.com/t/1-1-9-3-the-sparkle-bomber-cold-canister-bomb-pb-saboteur-sr75/112102
- **t4 doors:** `GEOMETRY_COLLAPSE`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Canister Bomb**: delivery=projectile, motion_signature=fan_spread, count=1, pierce=all · conf 0.75
  - `#1` **Flashbang**: delivery=zone, motion_signature=ground_place, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Canister Bomb Saboteur: multi projectile projectile identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **deviations:**
  - [accepted_downgrade] minor drift: the source player uses Flashbang as a hard CC/debuff (community calls it 'Insane') and stun-locks packs -- but the engine emits NO CC token for it because the fetched anchor names only 'debuff' (stun/blind live in probe/claim-paraphrase, both inadmissible). · downgrade-owner `elrond (W4 GD tranche; internal-consistency reconcile, no W1 evidence — W5 is GD's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]
- **mapping deviation notes:** minor drift: the source player uses Flashbang as a hard CC/debuff (community calls it 'Insane') and stun-locks packs -- but the engine emits NO CC token for it because the fetched anchor names only 'debuff' (stun/blind live in probe/claim-paraphrase, both inadmissible). Canister's cluster-scatter maps to multi_projectile and internal-trauma to bleed cleanly. The withheld Flashbang CC + Thermite RR are near-misses, not silent drops.

## gd-dee-witch-hunter — Dreeg's Evil Eye Witch Hunter `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** chaos-poison · _raw_: acid
- **elements attested:** earth
- **ailments attested:** poison
- **eras:** base-2016;fg-2019;patch-1.1-1.2 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 1 · **dossier rows:** 6
- **citations (2):** [communal] forums.crateentertainment.com · @unknown · https://forums.crateentertainment.com/t/1-0-0-7-dreegs-champion/36230; [communal] forums.crateentertainment.com · @unknown · https://forums.crateentertainment.com/t/1-2-0-3-witch-hunter-w-embers-calling-set-fire-burn-dreegs-evil-eye-75-fire-rr/133677
- **t4 doors:** `PERSISTENCE_ENGINE_saturation`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Dreeg's Evil Eye**: delivery=zone, cadence=spam, motion_signature=ground_place, count=1 · conf 0.75
  - `#1` **Bloody Pox**: delivery=projectile, motion_signature=straight_line, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Dreeg's Evil Eye Witch Hunter: ground targeted circle zone identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] earth element register — _expressed by_ `element:earth`
- **deviations:**
  - [accepted_downgrade] minor drift: the two-stage projectile-then-pool delivery is compressed to the pool geometry with the bolt as delivery flavor; · downgrade-owner `elrond (W4 GD tranche; internal-consistency reconcile, no W1 evidence — W5 is GD's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
- **mapping deviation notes:** minor drift: the two-stage projectile-then-pool delivery is compressed to the pool geometry with the bolt as delivery flavor; the fumble-curse accuracy layer and confusion layer are withheld pending steward rows (near-misses, not silent drops).

## gd-devastation-sorcerer — Devastation Sorcerer `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** lightning · _raw_: aether
- **elements attested:** fire,lightning
- **ailments attested:** curse:sap
- **eras:** base-2016;patch-1.1-1.2 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 1 · **dossier rows:** 6
- **citations (2):** [communal] forums.crateentertainment.com · @unknown · https://forums.crateentertainment.com/t/1-1-7-0-the-tiny-devastation-sorcerer-sr75/100740; [communal] forums.crateentertainment.com · @unknown · https://forums.crateentertainment.com/t/1-1-9-7-sorcerer-devastation-mortar-build-pyran-set-sr80/126856
- **t4 doors:** `ZONE_CONTROL`, `GEOMETRY_COLLAPSE`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Devastation**: delivery=zone, range=screen, width=wide, cadence=cooldown, motion_signature=ground_place, count=1 · conf 0.75
  - `#1` **Blackwater Cocktail (support)**: delivery=zone, motion_signature=ground_place, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Devastation Sorcerer: ground targeted circle zone identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] lightning element register — _expressed by_ `element:lightning`
- **deviations:**
  - [accepted_downgrade] minor drift: discrete falling-meteor impacts homogenize to zone-tick damage in ground_targeted_circle; · downgrade-owner `elrond (W4 GD tranche; internal-consistency reconcile, no W1 evidence — W5 is GD's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
- **mapping deviation notes:** minor drift: discrete falling-meteor impacts homogenize to zone-tick damage in ground_targeted_circle; the devotion-proc layer is empty (payloads unfetched).

## gd-doom-bolt-sentinel — Doom Bolt Sentinel `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** chaos-poison · _raw_: chaos
- **elements attested:** fire
- **ailments attested:** curse:sap
- **eras:** fg-2019;patch-1.1-1.2 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 1 · **dossier rows:** 6
- **citations (2):** [communal] forums.crateentertainment.com · @unknown · https://forums.crateentertainment.com/t/1-1-4-0-judgment-of-doom-bolt-fire-sentinel/50808; [authored] massivelyop.com · @unknown · https://massivelyop.com/2019/03/29/grim-dawns-forgotten-gods-expansion-has-launched-with-new-story-chapter-and-oathkeeper-mastery/
- **t4 doors:** `ELEMENT_CONVERSION_MONO`, `PERSISTENCE_ENGINE_uptime`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Doom Bolt**: delivery=projectile, cadence=cooldown, motion_signature=straight_line, count=1 · conf 0.75
  - `#1` **Sigil of Consumption + Curse of Frailty (between-nuke fill)**: delivery=zone, motion_signature=ground_place, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Doom Bolt Sentinel: single target projectile identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **deviations:**
  - [accepted_downgrade] minor drift: hard-cooldown nuke rhythm + timer-based CDR pulse ride on cadence keys rather than a native cooldown primitive; · downgrade-owner `elrond (W4 GD tranche; internal-consistency reconcile, no W1 evidence — W5 is GD's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]
- **mapping deviation notes:** minor drift: hard-cooldown nuke rhythm + timer-based CDR pulse ride on cadence keys rather than a native cooldown primitive; the acid/chaos DoT carry is element-flavor only (no statuses named -> no tokens).

## gd-fire-strike-purifier — Fire Strike Purifier `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** fire · _raw_: fire
- **elements attested:** fire
- **ailments attested:** _(none)_
- **eras:** aom-2017;patch-1.1-1.2 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 3 / 2 / 0 · **dossier rows:** 6
- **citations (3):** [communal] forums.crateentertainment.com · @unknown · https://forums.crateentertainment.com/t/1-0-7-1-the-burning-devil-full-set-ulzuin-fire-strike-purifier/48352; [communal] forums.crateentertainment.com · @unknown · https://forums.crateentertainment.com/t/1-1-9-1-budget-2-handed-ranged-the-desolator-fire-strike-fire-purifier/111014; [authored] mmos.com · @unknown · https://mmos.com/news/grim-dawn-ashes-of-malmouth-october-11
- **t4 doors:** `ELEMENT_CONVERSION_MONO`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Fire Strike**: delivery=projectile, motion_signature=straight_line, count=1 · conf 0.75
  - `#1` **Inquisitor Seal**: delivery=zone, motion_signature=ground_place, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Fire Strike Purifier: line projectile identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **deviations:**
  - [accepted_downgrade] minor drift: the WPS attack-variety layer is structurally present but payload-thin (unfetched); · downgrade-owner `elrond (W4 GD tranche; internal-consistency reconcile, no W1 evidence — W5 is GD's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]
- **mapping deviation notes:** minor drift: the WPS attack-variety layer is structurally present but payload-thin (unfetched); line compresses shot-plus-burst into the attested explosive-line footprint.

## gd-forcewave-warlord — Forcewave Warlord `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** bleed
- **eras:** fg-2019;patch-1.1-1.2 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 2 / 1 / 1 · **dossier rows:** 6
- **citations (2):** [communal] forums.crateentertainment.com · @unknown · https://forums.crateentertainment.com/t/1-1-8-0-budget-physical-forcewave-warlord/104493; [authored] massivelyop.com · @unknown · https://massivelyop.com/2019/03/29/grim-dawns-forgotten-gods-expansion-has-launched-with-new-story-chapter-and-oathkeeper-mastery/
- **t4 doors:** `ZONE_CONTROL`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Forcewave**: delivery=projectile, width=wide, cadence=spam, motion_signature=straight_line, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Forcewave Warlord: line projectile identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] Lane-wave spam loop, cast-root rhythm, casting-speed tempo land natively; · downgrade-owner `elrond (W4 GD tranche; internal-consistency reconcile, no W1 evidence — W5 is GD's external check)`
  - [accepted_downgrade] [STEWARD AUDIT 2026-07-18: regraded APPROX->CLOSE in-place; · downgrade-owner `elrond (W4 GD tranche; internal-consistency reconcile, no W1 evidence — W5 is GD's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]
- **mapping deviation notes:** Lane-wave spam loop, cast-root rhythm, casting-speed tempo land natively; Internal Trauma DoT layer now ROUTED (bleed) under the m02-audit steward ruling (GD trauma -> bleed, phys-DoT lineage). Residual drift: bleed-vs-trauma flavor register + ZONE_CONTROL door weak fit (accepted-weak at audit). [STEWARD AUDIT 2026-07-18: regraded APPROX->CLOSE in-place; the sole stated deviation was the pending row ruling, now resolved.]

## gd-krieg-death-knight — Krieg Death Knight `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** lightning · _raw_: aether
- **elements attested:** shadow
- **ailments attested:** _(none)_
- **eras:** aom-2017;patch-1.1-1.2 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 0 · **dossier rows:** 6
- **citations (2):** [communal] forums.crateentertainment.com · @unknown · https://forums.crateentertainment.com/t/1-0-6-1-warpblade-krieg-dw-aether-cadence-death-knight-gladiator-farmer-9-minutes/46973; [authored] gametyrant.com · @unknown · https://gametyrant.com/news/grim-dawn-ashes-of-malmouth-is-a-necromancers-dream
- **t4 doors:** `ELEMENT_CONVERSION_MONO`, `TEMPORAL_CHARGE`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Cadence**: delivery=melee_arc, range=melee, motion_signature=point_strike, count=1 · conf 0.75
  - `#1` **Bone Harvest**: delivery=melee_arc, range=melee, cadence=cooldown, motion_signature=arc_sweep, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Krieg Death Knight: melee strike melee_arc identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] shadow element register — _expressed by_ `element:shadow`
- **deviations:**
  - [accepted_downgrade] minor drift: the counted every-3rd-hit texture is approximated by the native cycle + threshold surfaces (accrual filed for the exact two-tier shape); · downgrade-owner `elrond (W4 GD tranche; internal-consistency reconcile, no W1 evidence — W5 is GD's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'melee_arc'` [green]
- **mapping deviation notes:** minor drift: the counted every-3rd-hit texture is approximated by the native cycle + threshold surfaces (accrual filed for the exact two-tier shape); Krieg's Wrath set-proc layer is empty (name-only).

## gd-mortar-purifier — Mortar Trap Purifier `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** fire · _raw_: fire
- **elements attested:** fire
- **ailments attested:** _(none)_
- **eras:** aom-2017;patch-1.1-1.2 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 3 / 1 / 1 · **dossier rows:** 6
- **citations (2):** [communal] forums.crateentertainment.com · @unknown · https://forums.crateentertainment.com/t/1-0-4-1-tears-of-fire-mortar-trap-immortal-purifier-170-cruicible/44138; [authored] mmos.com · @unknown · https://mmos.com/news/grim-dawn-ashes-of-malmouth-october-11
- **t4 doors:** `PROXY_ASCENSION`, `ZONE_CONTROL`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Mortar Trap**: delivery=summon_delegate, cadence=cooldown, count=1 · conf 0.75
  - `#1` **Inquisitor Seal**: delivery=zone, motion_signature=ground_place, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Mortar Trap Purifier: totem summon_delegate identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **deviations:**
  - [accepted_downgrade] minor drift: turret aggro-targeting autonomy and overlap-count multiplication are softened onto the native placed-emitter; · downgrade-owner `elrond (W4 GD tranche; internal-consistency reconcile, no W1 evidence — W5 is GD's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'summon_delegate'` [green]
- **mapping deviation notes:** minor drift: turret aggro-targeting autonomy and overlap-count multiplication are softened onto the native placed-emitter; the exact count-stacking shape lives in the filed accrual.

## gd-panettis-mage-hunter — Panetti's Missile Mage Hunter `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** _(unassigned)_ · _raw_: mixed(fire/cold/lightning)
- **elements attested:** fire,lightning
- **ailments attested:** _(none)_
- **eras:** aom-2017;patch-1.1-1.2 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 3 / 2 / 1 · **dossier rows:** 6
- **citations (2):** [communal] forums.crateentertainment.com · @unknown · https://forums.crateentertainment.com/t/1-1-8-1-shaper-of-elements-elemental-prm-mage-hunter/106609; [authored] mmos.com · @unknown · https://mmos.com/news/grim-dawn-ashes-of-malmouth-october-11
- **t4 doors:** `ELEMENT_CONVERSION_HYBRID`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Panetti's Replicating Missile**: delivery=projectile, speed=fast, cadence=spam, motion_signature=fork_split, count=1 · conf 0.75
  - `#1` **Inquisitor Seal**: delivery=zone, motion_signature=ground_place, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Panetti's Missile Mage Hunter: fork projectile identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **deviations:**
  - [accepted_downgrade] minor drift: equal-thirds tri-elemental compresses to a 2-slot hybrid (cold dropped per hybrid law -- the source player would see one-third of the rainbow missing its color, damage carried but flavor narrowed). · downgrade-owner `elrond (W4 GD tranche; internal-consistency reconcile, no W1 evidence — W5 is GD's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]
- **mapping deviation notes:** minor drift: equal-thirds tri-elemental compresses to a 2-slot hybrid (cold dropped per hybrid law -- the source player would see one-third of the rainbow missing its color, damage carried but flavor narrowed).

## gd-primal-strike-vindicator — Primal Strike Vindicator `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** lightning · _raw_: lightning
- **elements attested:** lightning
- **ailments attested:** curse:sap
- **eras:** aom-2017;patch-1.1-1.2 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 3 / 1 / 2 · **dossier rows:** 6
- **citations (2):** [communal] forums.crateentertainment.com · @unknown · https://forums.crateentertainment.com/t/1-2-1-6-beginner-primal-strike-vindicator-unleash-the-thunderbuss-sr-and-lokarr-viable/143897; [official] store.steampowered.com · @Crate Entertainment · https://store.steampowered.com/app/642280/Grim_Dawn__Ashes_of_Malmouth_Expansion/
- **t4 doors:** `ELEMENT_CONVERSION_MONO`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Primal Strike**: delivery=melee_arc, range=melee, motion_signature=point_strike, count=1 · conf 0.75
  - `#1` **Wind Devil**: delivery=summon_delegate, cadence=cooldown, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Primal Strike Vindicator: melee strike melee_arc identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] lightning element register — _expressed by_ `element:lightning`
- **deviations:**
  - [accepted_downgrade] Wind Devil wanders; · downgrade-owner `elrond (W4 GD tranche; internal-consistency reconcile, no W1 evidence — W5 is GD's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'melee_arc'` [green]
- **mapping deviation notes:** Wind Devil wanders; engine totem is stationary (R-M8-adjacent mobile-emitter drift; qual mint-candidate filed). Storm Totem unfetched — omitted rather than memory-supplemented.

## gd-roh-infiltrator — Rune of Hagarrad Infiltrator `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** cold · _raw_: cold
- **elements attested:** water
- **ailments attested:** _(none)_
- **eras:** aom-2017;patch-1.1-1.2 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 0 · **dossier rows:** 6
- **citations (2):** [communal] forums.crateentertainment.com · @unknown · https://forums.crateentertainment.com/t/1-1-9-7-dw-melee-cold-abb-rune-of-hagarrad-infiltrator-sr-90/124166; [official] store.steampowered.com · @Crate Entertainment · https://store.steampowered.com/app/642280/Grim_Dawn__Ashes_of_Malmouth_Expansion/
- **t4 doors:** `ZONE_CONTROL`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Rune of Hagarrad**: delivery=zone, cadence=cooldown, motion_signature=ground_place, count=1 · conf 0.75
  - `#1` **Word of Renewal**: delivery=aura, range=self, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Rune of Hagarrad Infiltrator: ground targeted circle zone identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] water element register — _expressed by_ `element:water`
- **deviations:**
  - [accepted_downgrade] Trap arms on enemy contact; · downgrade-owner `elrond (W4 GD tranche; internal-consistency reconcile, no W1 evidence — W5 is GD's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
- **mapping deviation notes:** Trap arms on enemy contact; engine ground-circle bursts/ticks on placement — the arm-and-lure timing texture is lost (qual mint-candidate filed). Still that build, slightly worse: place-under-enemies loop survives.

## gd-shadow-strike-infiltrator — Shadow Strike Infiltrator `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** cold · _raw_: cold
- **elements attested:** water
- **ailments attested:** _(none)_
- **eras:** aom-2017;patch-1.1-1.2 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 1 / 0 · **dossier rows:** 6
- **citations (2):** [communal] forums.crateentertainment.com · @unknown · https://forums.crateentertainment.com/t/1-1-5-1-demorgogoneth-2h-dw-cold-shadow-strike-infiltrator/93574; [official] store.steampowered.com · @Crate Entertainment · https://store.steampowered.com/app/642280/Grim_Dawn__Ashes_of_Malmouth_Expansion/
- **t4 doors:** `ELEMENT_CONVERSION_MONO`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Shadow Strike (+Nightfall)**: delivery=motion, motion_signature=blink_translate, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Shadow Strike Infiltrator: teleport motion identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] water element register — _expressed by_ `element:water`
- **deviations:**
  - [accepted_downgrade] Movement and nuke are fused in one button; · downgrade-owner `elrond (W4 GD tranche; internal-consistency reconcile, no W1 evidence — W5 is GD's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'motion'` [green]
- **mapping deviation notes:** Movement and nuke are fused in one button; engine teleport is an offensive reposition whose strike payload on arrival is noted, not asserted native (arc-b01 discipline). Fusion texture may render as reposition-then-hit.

## gd-trozan-druid — Trozan's Sky Shard Druid `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** cold · _raw_: cold
- **elements attested:** lightning,water
- **ailments attested:** _(none)_
- **eras:** base-2016;aom-2017;patch-1.1-1.2 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 3 · **dossier rows:** 6
- **citations (3):** [communal] forums.crateentertainment.com · @unknown · https://forums.crateentertainment.com/t/trozan-sky-shard-druid-cold-lightning-hybrid-beginner-guide-1-2-1-6/150132; [communal] forums.crateentertainment.com · @mad_lee · https://forums.crateentertainment.com/t/1-2-1-6-king-trozan-4-00-crucible-gladiator-150-170-shard-36-all-celestials-cold-caster-druid-by-mad-lee-vid-g4-everything/109750; [communal] forums.crateentertainment.com · @unknown · https://forums.crateentertainment.com/t/1-1-4-0-the-whole-trozan-lightning-skybreach-warlock-druid/86267
- **t4 doors:** `ELEMENT_CONVERSION_HYBRID`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Trozan's Sky Shard**: delivery=zone, cadence=cooldown, motion_signature=ground_place, count=1 · conf 0.75
  - `#1` **Wind Devil**: count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Trozan's Sky Shard Druid: ground targeted circle zone identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] water element register — _expressed by_ `element:water`
- **deviations:**
  - [accepted_downgrade] Cold/lightning HYBRID collapsed to element_primary water + secondary lightning per §1 top-2 rule; · downgrade-owner `elrond (W4 GD tranche; internal-consistency reconcile, no W1 evidence — W5 is GD's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
- **mapping deviation notes:** Cold/lightning HYBRID collapsed to element_primary water + secondary lightning per §1 top-2 rule; the Codex hybrid's cold->lightning conversion identity carried by ELEMENT_CONVERSION_HYBRID door. Source player of the pure-cold Skybreach variant loses the lightning slot — noted as variant, dominant published loop is the cold caster.

## gd-vitality-conjurer — Vitality Conjurer `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** chaos-poison · _raw_: vitality
- **elements attested:** shadow
- **ailments attested:** _(none)_
- **eras:** base-2016;aom-2017;fg-2019;patch-1.1-1.2 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 6 / 1 / 1 · **dossier rows:** 6
- **citations (2):** [communal] forums.crateentertainment.com · @unknown · https://forums.crateentertainment.com/t/1-1-6-2-beginners-vitality-caster-conjurer-guide-how-to-build-monster-build-from-the-scratch-suitable-for-first-character/99959; [communal] forums.crateentertainment.com · @unknown · https://forums.crateentertainment.com/t/1-2-1-4-bloody-plague-vitality-dot-2h-caster-conjurer-rominds-mog-calla-sr-31-bloody-pox-focus/142712
- **t4 doors:** `PERSISTENCE_ENGINE_saturation`, `PROXY_ASCENSION`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Sigil of Consumption**: delivery=zone, motion_signature=ground_place, count=1 · conf 0.75
  - `#1` **Bloody Pox**: delivery=zone, motion_signature=burst_around_self, count=1 · conf 0.75
  - `#2` **Wendigo Totem**: delivery=summon_delegate, cadence=cooldown, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Vitality Conjurer: ground targeted circle zone identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] shadow element register — _expressed by_ `element:shadow`
- **deviations:**
  - [accepted_downgrade] The build's POST-PATCH dominant form is the Dark One's Gift totem-sigil hybrid (weak-Sigil-to-dominant-totem transformation is explicit in fetched text) — mapped as the totem-forward form. · downgrade-owner `elrond (W4 GD tranche; internal-consistency reconcile, no W1 evidence — W5 is GD's external check)`
  - [accepted_downgrade] [STEWARD AUDIT 2026-07-18: blind token struck (anchor-splice; · downgrade-owner `elrond (W4 GD tranche; internal-consistency reconcile, no W1 evidence — W5 is GD's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
- **mapping deviation notes:** The build's POST-PATCH dominant form is the Dark One's Gift totem-sigil hybrid (weak-Sigil-to-dominant-totem transformation is explicit in fetched text) — mapped as the totem-forward form. Source player loses: the RR-curse (Curse of Frailty) mapped as un-tokened support (shape-silent withhold), and the totem's leech-sustain flavor is economy-noted not ailment-tokened. [STEWARD AUDIT 2026-07-18: blind token struck (anchor-splice; OA-reduction unattested) — debuff-texture understatement now includes the OA-tax flavor.]

## gd-wendigo-totem-ritualist — Wendigo Totem Ritualist `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** physical · _raw_: bleed
- **elements attested:** shadow
- **ailments attested:** _(none)_
- **eras:** aom-2017;patch-1.1-1.2 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 2 · **dossier rows:** 6
- **citations (2):** [communal] forums.crateentertainment.com · @unknown · https://forums.crateentertainment.com/t/1-2-0-0-1-2-1-the-wendigos-hunger-dw-4-wendigo-totem-vitality-dark-ones-gift-ritualist/133196; [authored] massivelyop.com · @unknown · https://massivelyop.com/2017/10/02/grim-dawns-massive-ashes-of-malmouth-expansion-arrives-october-11th/
- **t4 doors:** `PROXY_ASCENSION`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Wendigo Totem**: delivery=summon_delegate, range=screen, width=wide, cadence=cooldown, count=1 · conf 0.75
  - `#1` **Devouring Swarm**: delivery=zone, motion_signature=burst_around_self, count=1 · conf 0.75
  - `#2` **Grasping Vines**: delivery=zone, motion_signature=ground_place, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Wendigo Totem Ritualist: totem summon_delegate identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] shadow element register — _expressed by_ `element:shadow`
- **deviations:**
  - [accepted_downgrade] Totem-army is a placed-proxy delivery that engine supports as `totem` — but the AUTONOMY of the leech-totems (they tick independently while player kites) is a mild summoner-deferral flavor; · downgrade-owner `elrond (W4 GD tranche; internal-consistency reconcile, no W1 evidence — W5 is GD's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'summon_delegate'` [green]
- **mapping deviation notes:** Totem-army is a placed-proxy delivery that engine supports as `totem` — but the AUTONOMY of the leech-totems (they tick independently while player kites) is a mild summoner-deferral flavor; here the totems are PLACED emitters (map cleanly), not autonomous combatants (no pet GAP). Source player loses the RR/control ailment tokens (both withheld on attestation grounds), which understates the debuff-stacking texture.

## gd-word-of-pain-tactician — Word of Pain Tactician `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** fire · _raw_: fire
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** aom-2017;patch-1.1-1.2 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 6 / 0 / 0 · **dossier rows:** 6
- **citations (3):** [communal] forums.crateentertainment.com · @unknown · https://forums.crateentertainment.com/t/1-1-9-0-blade-arc-word-of-pain-pierce-tactician-cr-5-00-sr75/87715; [communal] forums.crateentertainment.com · @unknown · https://forums.crateentertainment.com/t/1-2-1-6-ranged-beginner-ssf-unconvetional-chaos-word-of-pain-vampirris-build/154912; [authored] massivelyop.com · @unknown · https://massivelyop.com/2017/10/02/grim-dawns-massive-ashes-of-malmouth-expansion-arrives-october-11th/
- **t4 doors:** `ELEMENT_CONVERSION_PHYSICAL`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Word of Pain**: delivery=zone, range=screen, width=wide, motion_signature=ground_place, count=1, pierce=all · conf 0.75
  - `#1` **Inquisitor Seal**: delivery=zone, range=screen, width=wide, motion_signature=ground_place, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Word of Pain Tactician: ground targeted circle zone identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] Multi-variant element identity (chaos/lightning/pierce) collapsed to the dominant PIERCE build -> element-neutral. · downgrade-owner `elrond (W4 GD tranche; internal-consistency reconcile, no W1 evidence — W5 is GD's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
- **mapping deviation notes:** Multi-variant element identity (chaos/lightning/pierce) collapsed to the dominant PIERCE build -> element-neutral. Source player of the chaos (shadow) WoP Vampirris variant loses their element slot. The devotion-proc payloads (Flame Torrent etc.) are the kit's real damage flavor but map to nothing — names only, no fetched behavior — so the mapping understates proc-driven output. 'Elemental agony' brand has no tokenable status.

## gd-blade-trap — Blade Trap `[NEGATIVE, class:record]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** physical · _raw_: pierce
- **elements attested:** _(silent)_
- **ailments attested:** root
- **eras:** base-2016;aom-2017 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 2 · **dossier rows:** 6
- **citations (2):** [communal] forums.crateentertainment.com · https://forums.crateentertainment.com/t/blade-trap-no-seriously-we-need-to-talk-about-this/38411?page=2 (archive: http://web.archive.org/web/20230328093307/https://forums.crateentertainment.com/t/blade-trap-no-seriously-we-need-to-talk-about-this/38411); [communal] forums.crateentertainment.com · https://forums.crateentertainment.com/t/blade-trap/41508
- **t4 doors:** `ZONE_CONTROL`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Blade Trap**: delivery=projectile, cadence=cooldown, motion_signature=straight_line, count=1, pierce=all · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Blade Trap: single target projectile identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] MANDATORY (APPROX): the source player experiences a targeted CC trap that both immobilizes AND emits blade-hits in a small radius -- the engine single_target + root captures the immobilize and cast-on-enemy delivery but flattens the blade-proc-in-radius payload (which is neither a clean single-target hit nor a placed zone). · downgrade-owner `elrond (W4 GD tranche; internal-consistency reconcile, no W1 evidence — W5 is GD's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]
- **mapping deviation notes:** MANDATORY (APPROX): the source player experiences a targeted CC trap that both immobilizes AND emits blade-hits in a small radius -- the engine single_target + root captures the immobilize and cast-on-enemy delivery but flattens the blade-proc-in-radius payload (which is neither a clean single-target hit nor a placed zone). The 24-point cost, 4s cooldown, and boss-immunity are texture the engine does not encode. This stays terminal MAPPED (APPROX, not GAPPED) per R-M7: it is 'that build, worse', not 'not that build'.

## gd-eor-warlord — Eye of Reckoning Warlord `[class:record]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** fire · _raw_: fire
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** fg-2019;patch-1.1-1.2 · **tier:** T1 · **lineage:** genre/spin
- **verify (C/X/U):** 5 / 0 / 0 · **dossier rows:** 6
- **citations (2):** [communal] forums.crateentertainment.com · @unknown · https://forums.crateentertainment.com/t/1-1-9-7-ssf-physical-eye-of-reckoning-warlord-leveling-and-beginner-build-hc-friendly/124405; [authored] massivelyop.com · @unknown · https://massivelyop.com/2019/03/29/grim-dawns-forgotten-gods-expansion-has-launched-with-new-story-chapter-and-oathkeeper-mastery/
- **t4 doors:** `ELEMENT_CONVERSION_PHYSICAL`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Eye of Reckoning**: delivery=motion, range=melee, cadence=channel, motion_signature=orbit_fixed, count=1 · conf 0.75
  - `#1` **Judgment**: delivery=zone, motion_signature=burst_around_self, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Eye of Reckoning Warlord: whirlwind motion identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] A GD EoR Warlord keeps the spin loop, movement-while-channel, the conversion identity, and the Judgment tap rhythm -- but every devotion-proc payload (Maul and the whole bound-devotion damage layer that Judgment exists to fire) is EMPTY under 0.3: names fetched, payloads not. · downgrade-owner `elrond (W4 GD tranche; internal-consistency reconcile, no W1 evidence — W5 is GD's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'motion'` [green]
- **mapping deviation notes:** A GD EoR Warlord keeps the spin loop, movement-while-channel, the conversion identity, and the Judgment tap rhythm -- but every devotion-proc payload (Maul and the whole bound-devotion damage layer that Judgment exists to fire) is EMPTY under 0.3: names fetched, payloads not. The source player would miss the proc-damage layer that motivates casting Judgment at all; its consequence slot is lawfully null. That build, worse (R-M7: still that build -- spin + convert + tap remains playable) -> APPROX, un-minted.

## gd-stormbox-elementalist — Storm Box Elementalist `[class:record]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** lightning · _raw_: lightning
- **elements attested:** lightning
- **ailments attested:** _(none)_
- **eras:** aom-2017;patch-1.1-1.2 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 2 / 0 / 2 · **dossier rows:** 6
- **citations (2):** [communal] steamcommunity.com · @unknown · https://steamcommunity.com/app/219990/discussions/0/1678063648170859096/; [communal] forums.crateentertainment.com · @russell_timmerman · https://forums.crateentertainment.com/t/my-best-character-so-far-elementalist-stun-jacks/93990
- **t4 doors:** `PERSISTENCE_ENGINE_uptime`, `RESONANCE_LOOP`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Storm Box of Elgoloth**: delivery=beam, motion_signature=chain_hop, count=1, chain=2 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Storm Box Elementalist: chain beam identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] lightning element register — _expressed by_ `element:lightning`
- **deviations:**
  - [accepted_downgrade] MANDATORY (§7.3): the source player would miss the persistent enemy-attached tether — Storm Box rides the tagged enemy and re-arcs continuously over its duration; · downgrade-owner `elrond (W4 GD tranche; internal-consistency reconcile, no W1 evidence — W5 is GD's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'beam'` [green]
- **mapping deviation notes:** MANDATORY (§7.3): the source player would miss the persistent enemy-attached tether — Storm Box rides the tagged enemy and re-arcs continuously over its duration; engine chain renders as cooldown-cadenced arc casts from the target, losing the set-and-forget tag-and-wait texture. Player test: that build, worse — the tag-then-arcs loop survives at chain + cooldown cadence.

## gd-berserker-wereforms — Berserker (FoA mastery) `[class:record]`

- **grade / terminal:** `GAPPED` / `MAPPED_DOCKET`
- **element (court):** cold · _raw_: cold
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** foa-pending · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 1 / 0 / 2 · **dossier rows:** 6
- **citations (2):** [official] grimdawn.com · https://www.grimdawn.com/guide/about/fangs-of-asterkarn/; [communal] wccftech.com · https://wccftech.com/grim-dawn-fangs-of-asterkarn-release-date-july-2026/
- **t4 delta:** shape `step` (signoff: unvalidated)
- **deviations:**
  - [engine_inexpressible] MANDATORY (GAPPED): the entire kit is unmappable because the source content does not yet exist -- Fangs of Asterkarn is unshipped and every dossier family abstained. → _fix_ `new_door_rfc`
- **acceptance asserts:**
  - `kit_identity_present == true` [green]
  - `expresses: MANDATORY (GAPPED): the entire kit is unmappable because the source content does` [red] · expected: RED until engine lane exists (routed to docket)
- **mapping deviation notes:** MANDATORY (GAPPED): the entire kit is unmappable because the source content does not yet exist -- Fangs of Asterkarn is unshipped and every dossier family abstained. The source player would experience a wereform/transformation ARPG loop (per folk-name aliases) but zero mechanics are attested, so nothing beyond the identity placeholder can be translated. This is a content-availability gap, NOT an engine-capability gap. See docket: unshipped-content class.

## gd-blight-fiend-ritualist — Blight Fiend Ritualist `[class:record]`

- **grade / terminal:** `GAPPED` / `MAPPED_DOCKET`
- **element (court):** chaos-poison · _raw_: acid
- **elements attested:** shadow
- **ailments attested:** _(none)_
- **eras:** aom-2017;patch-1.1-1.2 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 1 · **dossier rows:** 6
- **citations (2):** [authored] forums.crateentertainment.com · @Duskdeep86 · https://forums.crateentertainment.com/t/1-1-5-2-vid-ghol-set-unstable-blight-fiend-vitality-pet-ritualist-sr-100/95760; [official] grimdawn.com · https://www.grimdawn.com/guide/about/ashes-of-malmouth/
- **t4 doors:** `PROXY_FISSION`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Summon Blight Fiend**: count=1 · conf 0.75
  - `#1` **Unstable Anomaly (explosion-on-death)**: delivery=zone, motion_signature=burst_around_self, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Blight Fiend Ritualist: ring zone identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] shadow element register — _expressed by_ `element:shadow`
- **deviations:**
  - [engine_inexpressible] MANDATORY (GAPPED): the source player summons autonomous pets and shoves them into packs as walking bombs -- the ENTIRE delivery (an independently-acting summoned combatant) is the engine's deferred summoner-gap, so the loop cannot be delivered as-is. → _fix_ `new_door_rfc`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
  - `expresses: MANDATORY (GAPPED): the source player summons autonomous pets and shoves them in` [red] · expected: RED until engine lane exists (routed to docket)
- **mapping deviation notes:** MANDATORY (GAPPED): the source player summons autonomous pets and shoves them into packs as walking bombs -- the ENTIRE delivery (an independently-acting summoned combatant) is the engine's deferred summoner-gap, so the loop cannot be delivered as-is. The engine can model the death-explosion burst (ring, on-defender-death) but NOT the autonomous pet that carries it there. Ghol acid-conversion, pet positioning, and resummon-cadence are all pet-substrate the engine does not yet host. terminal MAPPED_DOCKET per R-M7: this is 'not that build' (no pet = no kit), not merely 'that build, worse'.

## gd-pet-conjurer — Pet Conjurer `[class:record]`

- **grade / terminal:** `GAPPED` / `MAPPED_DOCKET`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** base-2016;fg-2019;patch-1.1-1.2 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 3 / 1 / 1 · **dossier rows:** 6
- **citations (3):** [communal] forums.crateentertainment.com · @unknown · https://forums.crateentertainment.com/t/birbbringer-pet-conjurer/93504; [communal] forums.crateentertainment.com · @unknown · https://forums.crateentertainment.com/t/atomic-emu-pet-conjurer-callagadra-facetank-edition/122714; [communal] steamcommunity.com · @unknown · https://steamcommunity.com/sharedfiles/filedetails/?id=473961455
- **t4 doors:** `DUAL_PROXY`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Summon Briarthorn + Summon Familiar (pet core)**: count=1 · conf 0.75
  - `#1` **Blood of Dreeg**: delivery=aura, range=self, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Pet Conjurer: self buff aura identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [engine_inexpressible] Not that build (R-M7): the entire damage layer is autonomous pets scaled by pet-only stats; → _fix_ `new_door_rfc`
- **acceptance asserts:**
  - `primary_delivery_class == 'aura'` [green]
  - `expresses: Not that build (R-M7): the entire damage layer is autonomous pets scaled by pet-` [red] · expected: RED until engine lane exists (routed to docket)
- **mapping deviation notes:** Not that build (R-M7): the entire damage layer is autonomous pets scaled by pet-only stats; the engine's player-delivery surface would leave only the buff/debuff shell with nobody fighting for you.

## gd-reap-spirit — Reap Spirit (as primary) `[NEGATIVE, class:record]`

- **grade / terminal:** `GAPPED` / `MAPPED_DOCKET`
- **element (court):** chaos-poison · _raw_: vitality
- **elements attested:** shadow
- **ailments attested:** _(none)_
- **eras:** aom-2017;fg-2019;patch-1.1-1.2 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 0 · **dossier rows:** 6
- **citations (3):** [communal] steamcommunity.com · @unknown · https://steamcommunity.com/app/219990/discussions/0/3182216552781692959/; [communal] forums.crateentertainment.com · @Squib · https://forums.crateentertainment.com/t/reap-spirit-super-underwhelming-or/41989; [communal] forums.crateentertainment.com · @TheFuentes5551 · https://forums.crateentertainment.com/t/spellbinder-that-uses-reap-spirit-as-main-attack/107054
- **t4 doors:** `PROXY_ASCENSION`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Reap Spirit**: delivery=summon_delegate, cadence=cooldown, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Reap Spirit (as primary): totem summon_delegate identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] shadow element register — _expressed by_ `element:shadow`
- **deviations:**
  - [engine_inexpressible] Autonomous temporary pet combatants are the entire loop; → _fix_ `new_door_rfc`
- **acceptance asserts:**
  - `primary_delivery_class == 'summon_delegate'` [green]
  - `expresses: Autonomous temporary pet combatants are the entire loop;` [red] · expected: RED until engine lane exists (routed to docket)
- **mapping deviation notes:** Autonomous temporary pet combatants are the entire loop; engine has no autonomous-combatant delivery (summoner-deferral, §A pet row). Player test: not that build.

## gd-retaliation-warlord — Retaliation Warlord `[class:record]`

- **grade / terminal:** `GAPPED` / `MAPPED_DOCKET`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** fg-2019;patch-1.1-1.2 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 1 · **dossier rows:** 6
- **citations (2):** [communal] forums.crateentertainment.com · @unknown · https://forums.crateentertainment.com/t/1-1-9-6-just-another-physical-retaliation-s-b-warlord-sr85-ravager-of-souls-callagadra/115298; [communal] forums.crateentertainment.com · @unknown · https://forums.crateentertainment.com/t/drunken-fwuffy-lazy-retaliation-warlord/83654
- **t4 doors:** `RETRIBUTION_ENGINE`, `DEFENSIVE_TRADEOFF`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Eye of Reckoning (retaliation-added-to-attack)**: delivery=motion, range=melee, cadence=channel, motion_signature=orbit_fixed, count=1 · conf 0.75
  - `#1` **Counter Strike**: delivery=melee_arc, range=melee, motion_signature=point_strike, count=1, chain=2 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Retaliation Warlord: whirlwind motion identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [engine_inexpressible] The loop-verb is stand-and-tank-return: passive per-attacker damage return with stat-stacked magnitude has no player-initiated delivery token (§A row — the absence IS the gap). → _fix_ `new_door_rfc`
- **acceptance asserts:**
  - `primary_delivery_class == 'motion'` [green]
  - `expresses: The loop-verb is stand-and-tank-return: passive per-attacker damage return with ` [red] · expected: RED until engine lane exists (routed to docket)
- **mapping deviation notes:** The loop-verb is stand-and-tank-return: passive per-attacker damage return with stat-stacked magnitude has no player-initiated delivery token (§A row — the absence IS the gap). Player test: not that build. EoR spin + Counter Strike trigger + TH reflect economy map as riders only.

## gd-skeleton-ritualist — Skeleton Ritualist `[class:record]`

- **grade / terminal:** `GAPPED` / `MAPPED_DOCKET`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** bleed
- **eras:** aom-2017;patch-1.1-1.2 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 6 / 0 / 0 · **dossier rows:** 6
- **citations (1):** [communal] forums.crateentertainment.com · @jhillman87 · https://forums.crateentertainment.com/t/ritualist-pet-summoner-shaman-necro/41572
- **t4 doors:** `PROXY_ASCENSION`, `PROXY_SOVEREIGNTY`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Raise Skeletons**: delivery=summon_delegate, cadence=cooldown, count=1 · conf 0.75
  - `#1` **Primal Spirit**: delivery=summon_delegate, cadence=cooldown, count=1 · conf 0.75
  - `#2` **Wendigo Totem**: delivery=summon_delegate, cadence=cooldown, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Skeleton Ritualist: totem summon_delegate identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [engine_inexpressible] The damage identity is an autonomous pet army (summoner-deferral gap, §A pet row); → _fix_ `new_door_rfc`
- **acceptance asserts:**
  - `primary_delivery_class == 'summon_delegate'` [green]
  - `expresses: The damage identity is an autonomous pet army (summoner-deferral gap, §A pet row` [red] · expected: RED until engine lane exists (routed to docket)
- **mapping deviation notes:** The damage identity is an autonomous pet army (summoner-deferral gap, §A pet row); maintenance-reservation economy and pet-stat scaling lane compound the distance. Player test: not that build. Wendigo Totem is the only native-mapping component.

