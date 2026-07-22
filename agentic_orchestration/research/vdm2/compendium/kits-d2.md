# VDM-2 Compendium — d2 (60 kits)

> **Source:** `corpus.db` `kit_master` view (574) ENRICHED live with the six VDM-2 side-car blocks + two registries (render-layer joins; DB never mutated). **v2.0** · db md5 `bebc933b0bf9bcab5988bbc16bcc55b4` · generated 2026-07-22T09:46:42Z.
> `court` is the reconciled element court (enum-checked); `original_element` carries raw provenance. Raw mobile-era descriptors (`elem_raw`) are NOT exposed (provenance-only). `kit_citations` is the sole citation authority.

| grade | n | verify (C/X/U) | dossier | cited | geom-bands | hooks |
|---|---|---|---|---|---|---|
| E 9 · C 33 · A 9 · G 9 | 60 | 330/3/63 | 360 | 60/60 | 144 | 92 |

## d2-blizzard-sorc — Blizzard Sorceress `[class:record]`

- **grade / terminal:** `EXACT` / `MAPPED`
- **element (court):** cold · _raw_: cold
- **elements attested:** water
- **ailments attested:** freeze
- **eras:** lod-1.10+;d2r;rotw-s13+ · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 9 / 0 / 0 · **dossier rows:** 6
- **citations (4):** [authored] maxroll.gg · @Teo1904; BTNeandertha1 (orig); MacroBioBoi (reviewer) · https://maxroll.gg/d2/guides/blizzard-sorceress; [authored] wowhead.com · @CinereousStyx · https://www.wowhead.com/diablo-2/guide/blizzard-sorc-sorceress-build-skills-gear; [authored] icy-veins.com · @MrLlamaSC · https://www.icy-veins.com/d2/blizzard-sorceress-build; [communal] diablo.fandom.com · https://diablo.fandom.com/wiki/Patch_1.10_(Diablo_II)
- **t4 doors:** `ZONE_CONTROL`, `PERSISTENCE_ENGINE_uptime`, `ELEMENT_CONVERSION_MONO`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Blizzard**: delivery=zone, cadence=cooldown, motion_signature=ground_place, count=1 · conf 0.75
  - `#1` **Glacial Spike**: delivery=projectile, motion_signature=straight_line, count=1 · conf 0.75
  - `#2` **Ice Blast**: delivery=projectile, motion_signature=straight_line, count=1 · conf 0.75
  - `#3` **Teleport**: delivery=motion, motion_signature=blink_translate, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Blizzard Sorceress: ground targeted circle zone identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] water element register — _expressed by_ `element:water`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]

## d2-fire-sorc — Fire Sorceress `[class:record]`

- **grade / terminal:** `EXACT` / `MAPPED`
- **element (court):** fire · _raw_: fire
- **elements attested:** fire
- **ailments attested:** _(none)_
- **eras:** lod;d2r;rotw-s14 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 6 / 0 / 1 · **dossier rows:** 6
- **citations (2):** [authored] icy-veins.com · @MrLlamaSC · https://www.icy-veins.com/d2/fireball-sorceress-build; [authored] maxroll.gg · @Teo1904 · https://maxroll.gg/d2/guides/meteor-sorceress
- **t4 doors:** `ZONE_CONTROL`, `PERSISTENCE_ENGINE_saturation`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Fire Ball**: delivery=projectile, cadence=spam, motion_signature=straight_line, count=1 · conf 0.75
  - `#1` **Meteor**: delivery=zone, motion_signature=ground_place, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Fire Sorceress: single target projectile identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]

## d2-firewall-sorc — Firewall Sorceress `[class:record]`

- **grade / terminal:** `EXACT` / `MAPPED`
- **element (court):** fire · _raw_: fire
- **elements attested:** fire
- **ailments attested:** _(none)_
- **eras:** lod-1.09 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 3 / 1 / 0 · **dossier rows:** 6
- **citations (3):** [authored] maxroll.gg · https://maxroll.gg/d2/guides/fire-wall-sorceress-guide; [communal] themovingcaravan.com · https://themovingcaravan.com/threads/1-09-leveling-guide-lod-and-classic.256/; [official] classic.battle.net (Arreat Summit via Wayback) · @Blizzard Entertainment (official) · http://web.archive.org/web/20090324044015/http://classic.battle.net:80/diablo2exp/skills/sorceress-fire.shtml (archive: http://web.archive.org/web/20090324044015/http://classic.battle.net:80/diablo2exp/skills/sorceress-fire.shtml)
- **t4 doors:** `ZONE_CONTROL`, `PERSISTENCE_ENGINE_saturation`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Fire Wall**: delivery=zone, cadence=cooldown, motion_signature=lane_place, count=1, chain=2 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Firewall Sorceress: placed lane zone identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]

## d2-fury-wolf — Fury Werewolf `[class:record]`

- **grade / terminal:** `EXACT` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** lod;d2r · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 6 / 0 / 0 · **dossier rows:** 6
- **citations (3):** [authored] maxroll.gg · @Teo1904 · https://maxroll.gg/d2/guides/werewolf-fury-druid; [authored] icy-veins.com · @MrLlamaSC · https://www.icy-veins.com/d2/fury-druid-build; [communal] wikipedia.org · https://en.wikipedia.org/wiki/Diablo_II:_Lord_of_Destruction
- **t4 doors:** `MOMENTUM_CASCADE`, `PHASE_MOMENTUM`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Fury**: delivery=melee_arc, range=melee, motion_signature=point_strike, count=1 · conf 0.75
  - `#1` **Feral Rage (pre-buff ramp)**: delivery=aura, range=self, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Fury Werewolf: melee strike melee_arc identity — _expressed by_ `geometry.delivery_class`
- **acceptance asserts:**
  - `primary_delivery_class == 'melee_arc'` [green]

## d2-javazon — Javazon `[class:record]`

- **grade / terminal:** `EXACT` / `MAPPED`
- **element (court):** lightning · _raw_: lightning
- **elements attested:** lightning
- **ailments attested:** _(none)_
- **eras:** lod-1.09+;d2r;rotw-s13+ · **tier:** T1 · **lineage:** d2/javazon
- **verify (C/X/U):** 6 / 0 / 1 · **dossier rows:** 6
- **citations (2):** [authored] icy-veins.com · https://www.icy-veins.com/d2/lightning-fury-charged-strike-amazon-javazon-build; [authored] purediablo.com · https://www.purediablo.com/strategy/pvm-lf-pj-javazon-guide-for-v1-10
- **t4 doors:** `GEOMETRY_PROPAGATION_cascade`, `ELEMENT_CONVERSION_PHYSICAL`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Lightning Fury**: delivery=projectile, motion_signature=fork_split, count=1, pierce=all · conf 0.75
  - `#1` **Charged Strike**: delivery=melee_arc, range=melee, motion_signature=point_strike, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Javazon: fork projectile identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] lightning element register — _expressed by_ `element:lightning`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]

## d2-lightning-sorc — Lightning Sorceress `[class:record]`

- **grade / terminal:** `EXACT` / `MAPPED`
- **element (court):** lightning · _raw_: lightning
- **elements attested:** lightning
- **ailments attested:** _(none)_
- **eras:** lod-infinity+;d2r;rotw · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 6 / 0 / 2 · **dossier rows:** 6
- **citations (1):** [authored] icy-veins.com · https://www.icy-veins.com/d2/lightning-sorceress-build
- **t4 doors:** `ELEMENT_CONVERSION_MONO`, `GEOMETRY_PROPAGATION_cascade`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Lightning**: delivery=projectile, motion_signature=straight_line, count=1 · conf 0.75
  - `#1` **Chain Lightning**: delivery=beam, motion_signature=chain_hop, count=1, chain=2 · conf 0.75
  - `#2` **Teleport**: delivery=motion, motion_signature=blink_translate, count=1, chain=2 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Lightning Sorceress: line projectile identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] lightning element register — _expressed by_ `element:lightning`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]

## d2-maul-bear — Maul Werebear `[class:record]`

- **grade / terminal:** `EXACT` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** stun
- **eras:** lod;d2r · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 6 / 0 / 1 · **dossier rows:** 6
- **citations (1):** [authored] maxroll.gg · https://maxroll.gg/d2/guides/maul-druid
- **t4 doors:** `MOMENTUM_CASCADE`, `PHASE_MOMENTUM`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Maul**: delivery=melee_arc, range=melee, motion_signature=point_strike, count=1 · conf 0.75
  - `#1` **Shockwave**: delivery=zone, motion_signature=fan_spread, count=1 · conf 0.75
  - `#2` **Werebear (form transform)**: delivery=aura, range=self, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Maul Werebear: melee strike melee_arc identity — _expressed by_ `geometry.delivery_class`
- **acceptance asserts:**
  - `primary_delivery_class == 'melee_arc'` [green]

## d2-wl-fire — Fire Warlock `[class:record]`

- **grade / terminal:** `EXACT` / `MAPPED`
- **element (court):** fire · _raw_: fire
- **elements attested:** fire
- **ailments attested:** _(none)_
- **eras:** rotw-s13+ · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 6 / 0 / 0 · **dossier rows:** 6
- **citations (2):** [authored] icy-veins.com · https://www.icy-veins.com/d2/fire-warlock-build; [authored] maxroll.gg · https://maxroll.gg/d2/guides/fire-warlock-guide
- **t4 doors:** `ZONE_CONTROL`, `PERSISTENCE_ENGINE_saturation`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Ring of Fire**: delivery=zone, width=wide, motion_signature=burst_around_self, count=1 · conf 0.75
  - `#1` **Flame Wave**: delivery=zone, motion_signature=fan_spread, count=1 · conf 0.75
  - `#2` **Apocalypse**: delivery=zone, range=screen, width=wide, motion_signature=ground_place, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Fire Warlock: ring zone identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]

## d2-ww-barb — Whirlwind Barbarian `[class:record]`

- **grade / terminal:** `EXACT` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** classic;lod;d2r;rotw-s14 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 7 / 0 / 1 · **dossier rows:** 6
- **citations (3):** [authored] maxroll.gg · https://maxroll.gg/d2/guides/whirlwind-barbarian-guide; [official] classic.battle.net · https://classic.battle.net/diablo2exp/skills/barbarian-combatskills.shtml; [communal] diablobytes.com · https://diablobytes.com/d2-resurrected/builds/whirlwind-barb/
- **t4 doors:** `ELEMENT_CONVERSION_PHYSICAL`, `MOMENTUM_CASCADE`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Whirlwind**: delivery=motion, range=melee, cadence=channel, motion_signature=orbit_fixed, count=1 · conf 0.75
  - `#1` **Battle Orders**: delivery=aura, range=self, width=wide, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Whirlwind Barbarian: whirlwind motion identity — _expressed by_ `geometry.delivery_class`
- **acceptance asserts:**
  - `primary_delivery_class == 'motion'` [green]

## d2-auradin — Auradin `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** lightning · _raw_: lightning
- **elements attested:** fire,lightning
- **ailments attested:** curse:sap
- **eras:** lod-1.11+;d2r · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 6 / 0 / 2 · **dossier rows:** 6
- **citations (2):** [communal] diablo2.io · @Blindfire187; Schnorki (mod) · https://diablo2.io/forums/auradin-questions-t1209183.html; [communal] diablo2.io · @Nate; Queegon; Schnorki (mod) · https://diablo2.io/forums/max-auradin-build-t1237207.html
- **t4 doors:** `NETWORK_AMPLIFIER`, `ELEMENT_CONVERSION_HYBRID`, `PERSISTENCE_ENGINE_uptime`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Zeal**: delivery=melee_arc, range=melee, motion_signature=point_strike, count=1 · conf 0.75
  - `#1` **Conviction aura**: delivery=aura, range=self, count=1 · conf 0.75
  - `#2` **Dream Holy Shock aura-pulse (item-defined)**: delivery=zone, range=screen, motion_signature=burst_around_self, count=1 · conf 0.75
  - `#3` **Dragon Holy Fire aura-pulse (item-defined)**: delivery=zone, motion_signature=burst_around_self, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Auradin: melee strike melee_arc identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] lightning element register — _expressed by_ `element:lightning`
- **deviations:**
  - [accepted_downgrade] Player would miss: dual-aura stack identity texture and the no-reservation free-aura economy feel; · downgrade-owner `elrond (W4 D2 tranche; internal-consistency reconcile, no W1 evidence — W5 is D2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'melee_arc'` [green]
- **mapping deviation notes:** Player would miss: dual-aura stack identity texture and the no-reservation free-aura economy feel; engine aura-pulse approximates but stack-doubling flavor is absent. Physical Zeal layer fully approximated. Item-dependence noted.

## d2-avenger — Avenger `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** fire · _raw_: fire
- **elements attested:** fire,lightning,water
- **ailments attested:** curse:sap
- **eras:** lod;d2r · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 6 / 0 / 0 · **dossier rows:** 6
- **citations (2):** [official] diablo2.io · @Stormlash (data contributor) · https://diablo2.io/skills/vengeance-t4185.html; [communal] diablo2.io · https://diablo2.io/forums/vengeance-pally-advice-please-t1463261.html
- **t4 doors:** `ELEMENT_CONVERSION_HYBRID`, `NETWORK_AMPLIFIER`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Vengeance**: delivery=melee_arc, range=melee, motion_signature=point_strike, count=1 · conf 0.75
  - `#1` **Conviction aura**: delivery=aura, range=self, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Avenger: melee strike melee_arc identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **deviations:**
  - [accepted_downgrade] Player would miss: cold as third simultaneous element (mapped fire+lightning only); · downgrade-owner `elrond (W4 D2 tranche; internal-consistency reconcile, no W1 evidence — W5 is D2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'melee_arc'` [green]
- **mapping deviation notes:** Player would miss: cold as third simultaneous element (mapped fire+lightning only); engine 7×7 covers two; tri-ele simultaneous feel is approximated.

## d2-berserker — Berserker `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** _(unassigned)_ · _raw_: magic
- **elements attested:** _(silent)_
- **ailments attested:** fear
- **eras:** lod;d2r · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 1 · **dossier rows:** 6
- **citations (2):** [authored] maxroll.gg · @MacroBioBoi; DarkHumility (orig) · https://maxroll.gg/d2/guides/berserk-barbarian; [communal] diablo2.io · @Nate · https://diablo2.io/forums/best-berserk-barb-mf-off-hand-t1037414.html
- **t4 doors:** `DEFENSIVE_TRADEOFF`, `GEOMETRY_COLLAPSE`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Berserk**: delivery=melee_arc, range=melee, motion_signature=point_strike, count=1 · conf 0.75
  - `#1` **Howl**: delivery=zone, motion_signature=fan_spread, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Berserker: melee strike melee_arc identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] Player would miss: magic damage conversion (engine has no magic element family; · downgrade-owner `elrond (W4 D2 tranche; internal-consistency reconcile, no W1 evidence — W5 is D2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'melee_arc'` [green]
- **mapping deviation notes:** Player would miss: magic damage conversion (engine has no magic element family; approximated as element-neutral physical with DEFENSIVE_TRADEOFF trade); Hork loot-economy identity loop not capturable in engine scope.

## d2-bonemancer — Bonemancer `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** _(unassigned)_ · _raw_: magic
- **elements attested:** shadow
- **ailments attested:** root
- **eras:** lod-1.10+;d2r · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 8 / 0 / 0 · **dossier rows:** 6
- **citations (2):** [communal] diablo2.io · @Johny82PL; Schnorki (mod); Necrarch (mod) · https://diablo2.io/forums/bonemancer-questions-t1471582.html; [communal] diablo2.io · @rgp151 · https://diablo2.io/forums/bonemancer-necro-success-in-hell-t809922.html
- **t4 doors:** `ZONE_CONTROL`, `PERSISTENCE_ENGINE_uptime`, `GEOMETRY_PROPAGATION_cascade`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Bone Spear**: delivery=projectile, motion_signature=straight_line, count=1, pierce=all · conf 0.75
  - `#1` **Bone Spirit**: delivery=projectile, motion_signature=straight_line, count=1 · conf 0.75
  - `#2` **Bone Prison**: delivery=zone, motion_signature=burst_around_self, count=1 · conf 0.75
  - `#3` **Bone Armor**: delivery=aura, range=self, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Bonemancer: line projectile identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] shadow element register — _expressed by_ `element:shadow`
- **deviations:**
  - [accepted_downgrade] Player would miss: Bone Spirit seeking feel (engine delivers seeking via delivery_notes only; · downgrade-owner `elrond (W4 D2 tranche; internal-consistency reconcile, no W1 evidence — W5 is D2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]
- **mapping deviation notes:** Player would miss: Bone Spirit seeking feel (engine delivers seeking via delivery_notes only; no native seeking geometry in 26-enum); Bone Prison cage shape (mapped circle; cage-wall feel partially approximated).

## d2-bowazon — Bowazon `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** classic;lod;d2r · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 7 / 0 / 1 · **dossier rows:** 6
- **citations (1):** [communal] diablo2.io · @louner; undertow; mhlg; Janet the Java · https://diablo2.io/forums/general-thoughts-and-tips-on-physical-bowazon-t1111426.html
- **t4 doors:** `GEOMETRY_PROPAGATION_overkill`, `TEMPORAL_CHARGE`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Multiple Shot**: delivery=projectile, motion_signature=fan_spread, count=1 · conf 0.75
  - `#1` **Strafe**: delivery=projectile, cadence=channel, motion_signature=fan_spread, count=1 · conf 0.75
  - `#2` **Guided Arrow**: delivery=projectile, motion_signature=straight_line, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Bowazon: multi projectile projectile identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] Player would miss: IAS breakpoint identity (weapon-speed-as-identity not directly mappable; · downgrade-owner `elrond (W4 D2 tranche; internal-consistency reconcile, no W1 evidence — W5 is D2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]
- **mapping deviation notes:** Player would miss: IAS breakpoint identity (weapon-speed-as-identity not directly mappable; approximated via cadence_scale economy note); Strafe animation-lock feel; Valkyrie companion pet layer (GAP-noted but rider not core loop).

## d2-bvc — BvC `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** knockback
- **eras:** lod-pvp;d2r-pvp · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 6 / 0 / 1 · **dossier rows:** 6
- **citations (3):** [authored] purediablo.com · @Yuqing · https://www.purediablo.com/forums/threads/pvp-bvc-guide-by-yuqing-co.1065/; [authored] purediablo.com · @Ling · https://www.purediablo.com/forums/threads/pvp-barb-vs-caster-guide-bvc-by-ling.1064/; [authored] maxroll.gg · https://maxroll.gg/d2/guides/whirlwind-barbarian-guide
- **t4 doors:** `MOMENTUM_CASCADE`, `DEFENSIVE_TRADEOFF`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Whirlwind**: delivery=motion, range=melee, cadence=channel, motion_signature=orbit_fixed, count=1 · conf 0.75
  - `#1` **Leap**: delivery=motion, range=melee, cadence=cooldown, motion_signature=leap_arc, count=1 · conf 0.75
  - `#2` **Battle Orders**: delivery=aura, range=self, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] BvC: whirlwind motion identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] Player would miss: PvP context (engine is solo PvE — WW mechanics map but caster-hunting purpose is context); · downgrade-owner `elrond (W4 D2 tranche; internal-consistency reconcile, no W1 evidence — W5 is D2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'motion'` [green]
- **mapping deviation notes:** Player would miss: PvP context (engine is solo PvE — WW mechanics map but caster-hunting purpose is context); Enigma teleport repositioning layer (item-dependent mobility).

## d2-charger — Charger `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** lod-pvp · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 0 · **dossier rows:** 6
- **citations (2):** [authored] purediablo.com · https://www.purediablo.com/forums/threads/pvp-charger-guide-ver-5.22670/; [communal] eu.forums.blizzard.com · https://eu.forums.blizzard.com/en/d2r/t/how-to-build-highest-damage-charge-paladin/11238
- **t4 doors:** `MOMENTUM_CASCADE`, `GEOMETRY_COLLAPSE`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Charge**: delivery=motion, motion_signature=straight_line, count=1 · conf 0.75
  - `#1` **Fanaticism aura**: delivery=aura, range=self, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Charger: dash attack motion identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] Player would miss: must-create-separation-before-recharge constraint (loop-pacing texture unique to Charge; · downgrade-owner `elrond (W4 D2 tranche; internal-consistency reconcile, no W1 evidence — W5 is D2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'motion'` [green]
- **mapping deviation notes:** Player would miss: must-create-separation-before-recharge constraint (loop-pacing texture unique to Charge; engine dash_attack approximates but lacks re-trigger gate); Fanaticism IAS non-interaction detail.

## d2-conc-barb — Concentrate Barbarian `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** lod;d2r · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 6 / 0 / 0 · **dossier rows:** 6
- **citations (1):** [authored] diablo2.io · @LuckyAce · https://diablo2.io/forums/guide-to-playing-a-mf-concentrate-barbarian-t899635.html
- **t4 doors:** `DEFENSIVE_TRADEOFF`, `PERSISTENCE_ENGINE_uptime`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Concentrate**: delivery=melee_arc, range=melee, motion_signature=point_strike, count=1 · conf 0.75
  - `#1` **Shout**: delivery=aura, range=self, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Concentrate Barbarian: melee strike melee_arc identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] Player would miss: uninterruptible swing feel — engine melee_strike approximates but no native 'cannot be interrupted' mechanic; · downgrade-owner `elrond (W4 D2 tranche; internal-consistency reconcile, no W1 evidence — W5 is D2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'melee_arc'` [green]
- **mapping deviation notes:** Player would miss: uninterruptible swing feel — engine melee_strike approximates but no native 'cannot be interrupted' mechanic; the safety-vs-damage identity is approximated via DEFENSIVE_TRADEOFF T4.

## d2-daggermancer — Daggermancer `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** chaos-poison · _raw_: poison
- **elements attested:** earth
- **ailments attested:** curse:amplify,poison
- **eras:** d2r-2.4+ · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 2 · **dossier rows:** 6
- **citations (2):** [official] diablo2.io · @Stormlash (data contributor) · https://diablo2.io/skills/poison-dagger-t4133.html; [communal] diablo2.io · @basicnecromancy; Necrarch (mod) · https://diablo2.io/forums/poison-necro-build-style-what-about-daggermancer-t1049069.html
- **t4 doors:** `PERSISTENCE_ENGINE_saturation`, `ELEMENT_CONVERSION_PHYSICAL`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Poison Dagger**: delivery=melee_arc, range=melee, motion_signature=point_strike, count=1 · conf 0.75
  - `#1` **Amplify Damage curse**: delivery=projectile, motion_signature=straight_line, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Daggermancer: melee strike melee_arc identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] earth element register — _expressed by_ `element:earth`
- **deviations:**
  - [accepted_downgrade] Player would miss: Crushing Blow identity layer (on-kill threshold mechanic; · downgrade-owner `elrond (W4 D2 tranche; internal-consistency reconcile, no W1 evidence — W5 is D2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'melee_arc'` [green]
- **mapping deviation notes:** Player would miss: Crushing Blow identity layer (on-kill threshold mechanic; approximated via execute T4 door note but not mapped as ailment — no fetched 'execute' language); adjacency-only melee range constraint (approximated by melee_strike geometry).

## d2-enchantress — Enchantress `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** fire · _raw_: fire
- **elements attested:** fire
- **ailments attested:** _(none)_
- **eras:** lod;d2r · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 1 · **dossier rows:** 6
- **citations (2):** [authored] icy-veins.com · @MrLlamaSC · https://www.icy-veins.com/d2/enchantress-sorceress-build; [authored] purediablo.com · @MongoJerry · https://www.purediablo.com/strategy/mongojerrys-1-10-enchantress-guide
- **t4 doors:** `PERSISTENCE_ENGINE_uptime`, `ELEMENT_CONVERSION_MONO`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Enchant**: delivery=aura, range=self, count=1 · conf 0.75
  - `#1` **Zeal (Passion oskill)**: delivery=melee_arc, range=melee, motion_signature=point_strike, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Enchantress: self buff aura identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **deviations:**
  - [accepted_downgrade] Source Enchantress wraps a buff-economy into a melee kit via oskill — the buff-recast loop and melee-strike delivery are both present, but the double-Fire-Mastery application trigger and the prebuff window are minor texture losses. · downgrade-owner `elrond (W4 D2 tranche; internal-consistency reconcile, no W1 evidence — W5 is D2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'aura'` [green]
- **mapping deviation notes:** Source Enchantress wraps a buff-economy into a melee kit via oskill — the buff-recast loop and melee-strike delivery are both present, but the double-Fire-Mastery application trigger and the prebuff window are minor texture losses. Player feels 'fire melee with big buff' — that build, slightly worse.

## d2-fire-druid — Fire Druid `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** fire · _raw_: fire
- **elements attested:** fire
- **ailments attested:** _(none)_
- **eras:** lod;d2r-2.4+ · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 7 / 0 / 0 · **dossier rows:** 6
- **citations (2):** [authored] icy-veins.com · @MrLlamaSC · https://www.icy-veins.com/d2/fire-druid-build; [communal] wikipedia.org · https://en.wikipedia.org/wiki/Diablo_II:_Lord_of_Destruction
- **t4 doors:** `ZONE_CONTROL`, `PERSISTENCE_ENGINE_uptime`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Fissure**: delivery=zone, motion_signature=ground_place, count=1 · conf 0.75
  - `#1` **Armageddon**: delivery=zone, motion_signature=burst_around_self, count=1 · conf 0.75
  - `#2` **Molten Boulder**: delivery=projectile, motion_signature=straight_line, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Fire Druid: ground targeted circle zone identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **deviations:**
  - [accepted_downgrade] Body-attached Armageddon (meteor shower that moves with caster) has no direct engine analog; · downgrade-owner `elrond (W4 D2 tranche; internal-consistency reconcile, no W1 evidence — W5 is D2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
- **mapping deviation notes:** Body-attached Armageddon (meteor shower that moves with caster) has no direct engine analog; circle+moving-emitter note carries it as texture rather than a distinct geometry. Player feels 'zone fire caster who walks into packs' — that build, slight delivery texture loss on the moving meteor rain.

## d2-fireclaw-wolf — Fireclaws Wolf `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** fire · _raw_: fire
- **elements attested:** fire
- **ailments attested:** _(none)_
- **eras:** lod;d2r · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 6 / 0 / 1 · **dossier rows:** 6
- **citations (2):** [authored] maxroll.gg · @Teo1904 · https://maxroll.gg/d2/guides/fire-claws-druid; [communal] wikipedia.org · https://en.wikipedia.org/wiki/Diablo_II:_Lord_of_Destruction
- **t4 doors:** `ELEMENT_CONVERSION_MONO`, `PHASE_MOMENTUM`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Fire Claws**: delivery=melee_arc, range=melee, motion_signature=point_strike, count=1 · conf 0.75
  - `#1` **Armageddon**: delivery=zone, motion_signature=burst_around_self, count=1 · conf 0.75
  - `#2` **Feral Rage (pre-buff)**: delivery=aura, range=self, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Fireclaws Wolf: melee strike melee_arc identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **deviations:**
  - [accepted_downgrade] Body-attached Armageddon (moving meteor circle) and form-lock are texture losses. · downgrade-owner `elrond (W4 D2 tranche; internal-consistency reconcile, no W1 evidence — W5 is D2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'melee_arc'` [green]
- **mapping deviation notes:** Body-attached Armageddon (moving meteor circle) and form-lock are texture losses. Feral Rage→Fire Claws switch pattern approximated as self_buff prelude. Player feels 'fire melee werewolf' — that build, slight delivery texture loss on moving Armageddon.

## d2-fishyzon — Fishyzon `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** lightning,water
- **ailments attested:** _(none)_
- **eras:** lod-1.09 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 3 / 1 / 2 · **dossier rows:** 6
- **citations (3):** [communal] blogspot.com · @Silverbolt · https://silverboltsplayground.blogspot.com/2009/05/diablo-ii-fishyzon-skill-layout.html; [communal] diablo2.io · https://diablo2.io/forums/plan-for-first-build-mavs-mf-zon-t8575.html; [official] classic.battle.net (Arreat Summit via Wayback) · @Blizzard Entertainment (official) · http://web.archive.org/web/20090324044010/http://classic.battle.net:80/diablo2exp/skills/amazon-javelin.shtml (archive: http://web.archive.org/web/20090324044010/http://classic.battle.net:80/diablo2exp/skills/amazon-javelin.shtml)
- **t4 doors:** `ELEMENT_CONVERSION_HYBRID`, `ZONE_CONTROL`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Lightning Fury**: delivery=projectile, motion_signature=fork_split, count=1, chain=2 · conf 0.75
  - `#1` **Charged Strike**: delivery=melee_arc, range=melee, motion_signature=point_strike, count=1 · conf 0.75
  - `#2` **Freezing Arrow**: delivery=projectile, motion_signature=straight_line, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Fishyzon: fork projectile identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] lightning element register — _expressed by_ `element:lightning`
- **deviations:**
  - [accepted_downgrade] The javelin-lightning-arc shape of Lightning Fury (thrown javelin that spawns radiating lightning bolts) approximates as fork geometry — no exact 'thrown-projectile-spawns-radial-bolts' token. · downgrade-owner `elrond (W4 D2 tranche; internal-consistency reconcile, no W1 evidence — W5 is D2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]
- **mapping deviation notes:** The javelin-lightning-arc shape of Lightning Fury (thrown javelin that spawns radiating lightning bolts) approximates as fork geometry — no exact 'thrown-projectile-spawns-radial-bolts' token. The physical javelin delivery vehicle is minor texture. Player feels 'lightning javelin thrower who freezes immunes' — that build, slight lightning-arc-spawn texture loss.

## d2-fohdin — FoHdin `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** lightning · _raw_: lightning
- **elements attested:** holy,lightning
- **ailments attested:** curse:sap
- **eras:** lod-pvp;d2r-2.4+ · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 1 · **dossier rows:** 6
- **citations (1):** [authored] icy-veins.com · @MrLlamaSC · https://www.icy-veins.com/d2/fist-of-the-heavens-foh-paladin-build
- **t4 doors:** `NETWORK_AMPLIFIER`, `ZONE_CONTROL`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Fist of the Heavens**: delivery=projectile, motion_signature=straight_line, count=1 · conf 0.75
  - `#1` **Conviction (aura)**: delivery=aura, range=self, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] FoHdin: single target projectile identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] lightning element register — _expressed by_ `element:lightning`
- **deviations:**
  - [accepted_downgrade] Holy bolt shrapnel spray as a secondary AoE element from the same cast is approximated as dual-element delivery note. · downgrade-owner `elrond (W4 D2 tranche; internal-consistency reconcile, no W1 evidence — W5 is D2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]
- **mapping deviation notes:** Holy bolt shrapnel spray as a secondary AoE element from the same cast is approximated as dual-element delivery note. Engine single_target geometry doesn't natively carry 'lightning bolt + radial shrapnel' dual-shape without delivery_notes. Player feels 'holy lightning cursor-caster with resist-shred aura' — that build, minor shrapnel-shape texture loss.

## d2-frenzy-barb — Frenzy Barbarian `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** lod;d2r · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 1 · **dossier rows:** 6
- **citations (1):** [authored] icy-veins.com · @MrLlamaSC · https://www.icy-veins.com/d2/frenzy-barbarian-build
- **t4 doors:** `MOMENTUM_CASCADE`, `TEMPORAL_CHARGE`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Frenzy**: delivery=melee_arc, range=melee, motion_signature=point_strike, count=1 · conf 0.75
  - `#1` **Double Swing**: delivery=melee_arc, range=melee, motion_signature=point_strike, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Frenzy Barbarian: melee strike melee_arc identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] Physical melee with speed-ramp self-buff is well-covered; · downgrade-owner `elrond (W4 D2 tranche; internal-consistency reconcile, no W1 evidence — W5 is D2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'melee_arc'` [green]
- **mapping deviation notes:** Physical melee with speed-ramp self-buff is well-covered; minor texture loss on the dual-weapon alternating-hit feel and the 'frenzy state' escalating intensity. No ailment attestation means the on-hit bleed possibility from Gore Rider (item-layer) doesn't enter mapping_json. Player feels 'fast physical dual-wield melee brawler' — that build, slight intensity-escalation texture loss.

## d2-frost-bowazon — Frostmaiden `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** cold · _raw_: cold
- **elements attested:** water
- **ailments attested:** freeze
- **eras:** lod;d2r · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 1 · **dossier rows:** 6
- **citations (1):** [authored] icy-veins.com · @MrLlamaSC · https://www.icy-veins.com/d2/freezing-arrow-frostmaiden-amazon-build
- **t4 doors:** `ZONE_CONTROL`, `MOMENTUM_CASCADE`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Freezing Arrow**: delivery=projectile, motion_signature=straight_line, count=1, pierce=all · conf 0.75
  - `#1` **Cold Arrow**: delivery=projectile, motion_signature=straight_line, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Frostmaiden: single target projectile identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] water element register — _expressed by_ `element:water`
- **deviations:**
  - [accepted_downgrade] Pierce-enabled chain detonation (each pierced enemy independently detonates the AoE) is a geometry-multiply texture with no direct engine token; · downgrade-owner `elrond (W4 D2 tranche; internal-consistency reconcile, no W1 evidence — W5 is D2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]
- **mapping deviation notes:** Pierce-enabled chain detonation (each pierced enemy independently detonates the AoE) is a geometry-multiply texture with no direct engine token; carried in delivery_notes. Player feels 'freeze-and-shatter ranged cold controller' — that build, minor pierce-chain texture loss.

## d2-frozen-orb-sorc — Frozen Orb Sorceress `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** cold · _raw_: cold
- **elements attested:** water
- **ailments attested:** _(none)_
- **eras:** lod;d2r;rotw-s14 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 6 / 0 / 1 · **dossier rows:** 6
- **citations (1):** [authored] maxroll.gg · @Jymnasium · https://maxroll.gg/d2/guides/frozen-orb-sorceress
- **t4 doors:** `GEOMETRY_PROPAGATION_overkill`, `PERSISTENCE_ENGINE_saturation`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Frozen Orb**: delivery=motion, width=wide, motion_signature=orbit_fixed, count=1 · conf 0.75
  - `#1` **Teleport**: delivery=motion, motion_signature=blink_translate, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Frozen Orb Sorceress: orbit motion identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] water element register — _expressed by_ `element:water`
- **deviations:**
  - [accepted_downgrade] The traveling-orb-that-emits-radially is approximated as orbit — the kit's defining shape (advancing emitter, not stationary orbit) is a delivery texture loss. · downgrade-owner `elrond (W4 D2 tranche; internal-consistency reconcile, no W1 evidence — W5 is D2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'motion'` [green]
- **mapping deviation notes:** The traveling-orb-that-emits-radially is approximated as orbit — the kit's defining shape (advancing emitter, not stationary orbit) is a delivery texture loss. Player feels 'cold orb sorceress who blankets areas with ice' — that build, slight advancing-vs-stationary orbit texture loss.

## d2-ghost-pvp — Ghost Assassin (WW/Trap) `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** lightning
- **ailments attested:** stun
- **eras:** lod-1.10+ · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 3 · **dossier rows:** 6
- **citations (3):** [communal] mbaker2307.wixsite.com · https://mbaker2307.wixsite.com/diablo2hardcore/pvp-lightning-sentry-whirlwind-assassin; [authored] purediablo.com · @TienJe · https://www.purediablo.com/forums/threads/pvp-ww-ghost-assassin-guide-v2-0-by-tienje.1070/; [communal] wikipedia.org · https://en.wikipedia.org/wiki/Diablo_II:_Lord_of_Destruction
- **t4 doors:** `ZONE_CONTROL`, `PROXY_ASCENSION`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Lightning Sentry**: delivery=summon_delegate, cadence=cooldown, count=1 · conf 0.75
  - `#1` **Mind Blast**: delivery=projectile, motion_signature=straight_line, count=1 · conf 0.75
  - `#2` **Whirlwind**: delivery=motion, range=melee, cadence=channel, motion_signature=orbit_fixed, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Ghost Assassin (WW/Trap): totem summon_delegate identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] lightning element register — _expressed by_ `element:lightning`
- **deviations:**
  - [accepted_downgrade] Ghost Assassin's identity fuses trap-zone control + mobility burst + CC-chain in PvP — the PvP meta-context (CC-lock dueling) is texture in fidelity_notes per engine solo-PvE scope. · downgrade-owner `elrond (W4 D2 tranche; internal-consistency reconcile, no W1 evidence — W5 is D2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'summon_delegate'` [green]
- **mapping deviation notes:** Ghost Assassin's identity fuses trap-zone control + mobility burst + CC-chain in PvP — the PvP meta-context (CC-lock dueling) is texture in fidelity_notes per engine solo-PvE scope. WW + trap combo is well-captured; minor loss on the precision positioning game of PvP dueling. Player feels 'trap-layer who teleports in and CC-bursts' — that build, PvP context excluded.

## d2-hammerdin — Hammerdin `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** _(unassigned)_ · _raw_: magic
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** lod-1.10+;d2r;rotw-s13+ · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 7 / 0 / 1 · **dossier rows:** 6
- **citations (3):** [authored] icy-veins.com · https://www.icy-veins.com/d2/blessed-hammer-paladin-hammerdin-build; [authored] purediablo.com · https://www.purediablo.com/strategy/diablo-2-guide-paladin-hammerdin-v1-10; [authored] maxroll.gg · https://maxroll.gg/d2/guides/blessed-hammer-paladin
- **t4 doors:** `PERSISTENCE_ENGINE_uptime`, `ZONE_CONTROL`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Blessed Hammer**: delivery=motion, motion_signature=orbit_fixed, count=1 · conf 0.75
  - `#1` **Teleport (Enigma runeword)**: delivery=motion, motion_signature=blink_translate, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Hammerdin: orbit motion identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] Source player would miss: (1) hammers travel in fixed spiral paths — coverage is position-dependent, not true ring/orbit; · downgrade-owner `elrond (W4 D2 tranche; internal-consistency reconcile, no W1 evidence — W5 is D2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'motion'` [green]
- **mapping deviation notes:** Source player would miss: (1) hammers travel in fixed spiral paths — coverage is position-dependent, not true ring/orbit; the spiral-arc placement puzzle is mechanically distinct from a maintained orbital. Orbit token is the best available approximation.

## d2-hydra-sorc — Hydra Sorceress `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** fire · _raw_: fire
- **elements attested:** fire
- **ailments attested:** _(none)_
- **eras:** d2r-2.4+;rotw-s14 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 1 · **dossier rows:** 6
- **citations (2):** [authored] maxroll.gg · https://maxroll.gg/d2/guides/hydra-sorceress; [authored] icy-veins.com · https://www.icy-veins.com/d2/hydra-orb-sorceress-build
- **t4 doors:** `PROXY_SOVEREIGNTY`, `PERSISTENCE_ENGINE_uptime`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Hydra**: delivery=summon_delegate, cadence=cooldown, count=1 · conf 0.75
  - `#1` **Teleport**: delivery=motion, motion_signature=blink_translate, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Hydra Sorceress: totem summon_delegate identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **deviations:**
  - [accepted_downgrade] Source player would miss: the 6-turret simultaneous stacking density is the build's power multiplier; · downgrade-owner `elrond (W4 D2 tranche; internal-consistency reconcile, no W1 evidence — W5 is D2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'summon_delegate'` [green]
- **mapping deviation notes:** Source player would miss: the 6-turret simultaneous stacking density is the build's power multiplier; mapping captures placed-turret identity but not the specific up-to-6 count scaling texture.

## d2-kicksin — Kicksin `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** bleed
- **eras:** lod;d2r · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 2 · **dossier rows:** 6
- **citations (2):** [authored] icy-veins.com · https://www.icy-veins.com/d2/dragon-talon-assassin-kicksin-build; [communal] diablo.fandom.com · https://diablo.fandom.com/wiki/Dragon_Talon_Kicksin
- **t4 doors:** `TEMPORAL_CHARGE`, `MOMENTUM_CASCADE`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Dragon Talon**: delivery=melee_arc, range=melee, speed=fast, motion_signature=point_strike, count=1 · conf 0.75
  - `#1` **Fade**: delivery=aura, range=self, count=1 · conf 0.75
  - `#2` **Cobra Strike**: delivery=melee_arc, range=melee, motion_signature=point_strike, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Kicksin: melee strike melee_arc identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] Source player would miss: (1) Crushing Blow percent-HP shred is the boss-kill engine — approximated via melee_strike but the percent-HP damage mechanic has no ailment analog; · downgrade-owner `elrond (W4 D2 tranche; internal-consistency reconcile, no W1 evidence — W5 is D2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'melee_arc'` [green]
- **mapping deviation notes:** Source player would miss: (1) Crushing Blow percent-HP shred is the boss-kill engine — approximated via melee_strike but the percent-HP damage mechanic has no ailment analog; (2) Mosaic runeword charge-maintenance shifts the kit from LoD to D2R identity significantly.

## d2-meteorb — Meteorb `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** fire · _raw_: fire
- **elements attested:** fire,water
- **ailments attested:** _(none)_
- **eras:** lod-1.10+;d2r;rotw-s14 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 7 / 0 / 1 · **dossier rows:** 6
- **citations (2):** [communal] purediablo.com · https://www.purediablo.com/strategy/meteorb-sorceress-guide; [communal] purediablo.com · https://www.purediablo.com/forums/threads/d2r-frozen-orb-sorceress-guide.20353/
- **t4 doors:** `ELEMENT_CONVERSION_HYBRID`, `GEOMETRY_COLLAPSE`, `PERSISTENCE_ENGINE_uptime`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Meteor**: delivery=zone, motion_signature=ground_place, count=1 · conf 0.75
  - `#1` **Fire Ball**: delivery=projectile, speed=fast, cadence=spam, motion_signature=straight_line, count=1 · conf 0.75
  - `#2` **Frozen Orb**: delivery=projectile, motion_signature=fan_spread, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Meteorb: ground targeted circle zone identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **deviations:**
  - [engine_inexpressible] Immunity-driven tree-partition motive has no engine lane. → _fix_ `new_door_rfc`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
  - `expresses: Immunity-driven tree-partition motive has no engine lane.` [red] · expected: RED until engine lane exists (routed to docket)
- **mapping deviation notes:** Immunity-driven tree-partition motive has no engine lane. Fireball is primary spam; Meteor is secondary burst-on-stationary — skill relative weight noted. Engine loses the 'which element do I cast now?' immunity-check loop that defined meteorb gameplay every 3 seconds.

## d2-nova-sorc — Nova Sorceress `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** lightning · _raw_: lightning
- **elements attested:** lightning
- **ailments attested:** stun
- **eras:** lod;d2r;rotw-s14 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 3 · **dossier rows:** 6
- **citations (2):** [communal] diablo2.io · @saggytits · https://diablo2.io/forums/hc-nova-sorc-guide-for-2-5-t1133963.html; [communal] diablo2.io · @APKefka · https://diablo2.io/forums/season-starter-es-nova-sorc-guide-fast-and-easy-runes-and-keys-t359249.html
- **t4 doors:** `ZONE_CONTROL`, `GEOMETRY_COLLAPSE`, `PERSISTENCE_ENGINE_uptime`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Nova**: delivery=zone, range=short, cadence=spam, motion_signature=burst_around_self, count=1 · conf 0.75
  - `#1` **Static Field**: delivery=zone, motion_signature=burst_around_self, count=1 · conf 0.75
  - `#2` **Teleport**: delivery=motion, motion_signature=blink_translate, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Nova Sorceress: ring zone identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] lightning element register — _expressed by_ `element:lightning`
- **deviations:**
  - [accepted_downgrade] Source player lived inside melee range by design — proximity requirement for ring center has no engine enforcement. · downgrade-owner `elrond (W4 D2 tranche; internal-consistency reconcile, no W1 evidence — W5 is D2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
- **mapping deviation notes:** Source player lived inside melee range by design — proximity requirement for ring center has no engine enforcement. Stun cadence at spell speed (not melee speed) = unusual delivery feel preserved via ring geometry. Static Field percent-HP shred loses precision mapping.

## d2-poison-javazon — Poison Javazon `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** chaos-poison · _raw_: poison
- **elements attested:** earth
- **ailments attested:** poison
- **eras:** lod · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 1 · **dossier rows:** 6
- **citations (2):** [communal] purediablo.com · https://www.purediablo.com/strategy/pvm-lf-pj-javazon-guide-for-v1-10; [communal] purediablo.com · https://www.purediablo.com/forums/threads/gitos-poison-javazon-guide.30058/
- **t4 doors:** `PERSISTENCE_ENGINE_saturation`, `ZONE_CONTROL`, `GEOMETRY_PROPAGATION_cascade`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Plague Javelin**: delivery=zone, motion_signature=ground_place, count=1 · conf 0.75
  - `#1` **Poison Javelin**: delivery=projectile, motion_signature=straight_line, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Poison Javazon: ground targeted circle zone identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] earth element register — _expressed by_ `element:earth`
- **deviations:**
  - [accepted_downgrade] Overlapping-zone stacking identity (throw to two sides simultaneously) has no engine enforcement — player spatial tactic, not a mechanic. · downgrade-owner `elrond (W4 D2 tranche; internal-consistency reconcile, no W1 evidence — W5 is D2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
- **mapping deviation notes:** Overlapping-zone stacking identity (throw to two sides simultaneously) has no engine enforcement — player spatial tactic, not a mechanic. Patient kill-confirmation loop (DoT, wait, confirm) is mood/pacing that engine captures only via DoT uptime, not timing UI.

## d2-poison-nova-necro — Poison Nova Necromancer `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** chaos-poison · _raw_: poison
- **elements attested:** shadow
- **ailments attested:** curse:sap,poison
- **eras:** lod-1.10+;d2r · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 7 / 0 / 0 · **dossier rows:** 6
- **citations (2):** [communal] diablo2.io · @ghostpos · https://diablo2.io/forums/necro-build-poison-nova-t1503529.html; [communal] diablo2.io · @xigua · https://diablo2.io/forums/gearing-a-poison-nova-necro-t1459573.html
- **t4 doors:** `PERSISTENCE_ENGINE_saturation`, `ZONE_CONTROL`, `NETWORK_AMPLIFIER`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Poison Nova**: delivery=zone, range=screen, width=wide, speed=slow, motion_signature=burst_around_self, count=1 · conf 0.75
  - `#1` **Lower Resist**: delivery=aura, range=self, count=1 · conf 0.75
  - `#2` **Corpse Explosion**: delivery=zone, motion_signature=ground_place, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Poison Nova Necromancer: ring zone identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] shadow element register — _expressed by_ `element:shadow`
- **deviations:**
  - [engine_inexpressible] Corpse Explosion's corpse-consumer identity loses fidelity — corpse_nodes rider note captures the gap. → _fix_ `new_door_rfc`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
  - `expresses: Corpse Explosion's corpse-consumer identity loses fidelity — corpse_nodes rider ` [red] · expected: RED until engine lane exists (routed to docket)
- **mapping deviation notes:** Corpse Explosion's corpse-consumer identity loses fidelity — corpse_nodes rider note captures the gap. Immune cleanup via CE has no engine corpse-resource analogue. Engine ring geometry + DoT correctly captures Nova identity. Lower Resist → curse:sap loses the poison-resistance-specific flavor.

## d2-singer — Singer `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** stun
- **eras:** lod;d2r;rotw-s14 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 7 / 0 / 1 · **dossier rows:** 6
- **citations (2):** [communal] diablo2.io · @Blubbalutsch · https://diablo2.io/forums/the-worker-a-war-cry-horker-barbarian-build-t1277155.html; [official] diablo2.io · https://diablo2.io/skills/war-cry-t4191.html
- **t4 doors:** `ZONE_CONTROL`, `NETWORK_AMPLIFIER`, `PERSISTENCE_ENGINE_uptime`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **War Cry**: delivery=zone, motion_signature=burst_around_self, count=1 · conf 0.75
  - `#1` **Battle Orders**: delivery=aura, range=self, count=1 · conf 0.75
  - `#2` **Battle Cry**: delivery=aura, range=self, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Singer: circle zone identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] Small-radius constraint (notably smaller than other War Cries) has no engine enforcement. · downgrade-owner `elrond (W4 D2 tranche; internal-consistency reconcile, no W1 evidence — W5 is D2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
- **mapping deviation notes:** Small-radius constraint (notably smaller than other War Cries) has no engine enforcement. The inversion pleasure (barbarian as caster) is player-experience texture the engine cannot encode. Engine stun + circle geometry captures the loop correctly.

## d2-smiter — Smiter `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** lod-1.10+;d2r · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 6 / 0 / 1 · **dossier rows:** 6
- **citations (2):** [communal] diablo2.io · @azeroti · https://diablo2.io/forums/found-my-favorite-uber-smiter-build-t1509613.html; [communal] purediablo.com · https://www.purediablo.com/forums/threads/the-1pt-smiter-guide-to-uber-tristram-v-1-0.86756/
- **t4 doors:** `SACRIFICE_ASCENDANCY`, `PROXY_ASCENSION`, `PERSISTENCE_ENGINE_uptime`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Smite**: delivery=melee_arc, range=melee, motion_signature=point_strike, count=1 · conf 0.75
  - `#1` **Fanaticism**: delivery=aura, range=self, count=1 · conf 0.75
  - `#2` **Holy Shield**: delivery=aura, range=self, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Smiter: melee strike melee_arc identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] Auto-hit guarantee (no miss chance) has no engine encoding — engine has standard accuracy model. · downgrade-owner `elrond (W4 D2 tranche; internal-consistency reconcile, no W1 evidence — W5 is D2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'melee_arc'` [green]
- **mapping deviation notes:** Auto-hit guarantee (no miss chance) has no engine encoding — engine has standard accuracy model. Crushing blow percent-HP shred maps to execute threshold only approximately (execute is kill-threshold, not damage-as-percent-HP). What the source smiter player felt was the reliable-hit certainty vs uber bosses; engine misses the 'no matter what, this lands' feel.

## d2-throw-barb — Throw Barbarian `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** lod;d2r-2.4+ · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 6 / 0 / 0 · **dossier rows:** 6
- **citations (2):** [authored] icy-veins.com · @MrLlamaSC · https://www.icy-veins.com/d2/throw-barbarian-build; [authored] maxroll.gg · https://maxroll.gg/d2/guides/double-throw-barbarian-guide
- **t4 doors:** `ELEMENT_CONVERSION_PHYSICAL`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Double Throw**: delivery=projectile, motion_signature=fan_spread, count=1 · conf 0.75
  - `#1` **Throwing Mastery**: delivery=aura, range=self, count=1, pierce=all · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Throw Barbarian: multi projectile projectile identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] Source player gets ranged dual-throw weapon feel with Amplify Damage on-hit as a core tactical layer (weapon choice IS the kit); · downgrade-owner `elrond (W4 D2 tranche; internal-consistency reconcile, no W1 evidence — W5 is D2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]
- **mapping deviation notes:** Source player gets ranged dual-throw weapon feel with Amplify Damage on-hit as a core tactical layer (weapon choice IS the kit); engine approximates via on-hit trigger rider. Mana leech (gear-sourced) is not a native resource key — noted as gear-mediated sustain.

## d2-wind-druid — Wind Druid `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** water
- **ailments attested:** chill
- **eras:** lod-1.10+;d2r · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 8 / 0 / 0 · **dossier rows:** 6
- **citations (2):** [authored] icy-veins.com · @MrLlamaSC · https://www.icy-veins.com/d2/wind-druid-build; [authored] maxroll.gg · https://maxroll.gg/d2/guides/tornado-hurricane-druid
- **t4 doors:** `PERSISTENCE_ENGINE_uptime`, `ZONE_CONTROL`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Tornado**: delivery=zone, motion_signature=burst_around_self, count=1 · conf 0.75
  - `#1` **Hurricane**: delivery=aura, range=self, count=1 · conf 0.75
  - `#2` **Cyclone Armor**: delivery=aura, range=self, count=1 · conf 0.75
  - `#3` **Oak Sage**: delivery=aura, range=self, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Wind Druid: circle zone identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] water element register — _expressed by_ `element:water`
- **deviations:**
  - [accepted_downgrade] Tornado's erratic wandering path is a player-skill expression unique to d2; · downgrade-owner `elrond (W4 D2 tranche; internal-consistency reconcile, no W1 evidence — W5 is D2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
- **mapping deviation notes:** Tornado's erratic wandering path is a player-skill expression unique to d2; engine circle/zone + drift note approximates the wander but loses the manual aim challenge that is the skill expression of this build.

## d2-wl-abyss — Abyss Warlock `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** _(unassigned)_ · _raw_: magic
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** rotw-s13+ · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 6 / 0 / 1 · **dossier rows:** 6
- **citations (3):** [authored] maxroll.gg · https://maxroll.gg/d2/guides/abyss-warlock-build-guide; [official] icy-veins.com · https://www.icy-veins.com/d2/reign-of-the-warlock-overview-for-diablo-ii-resurrected; [communal] rpgstash.com · https://www.rpgstash.com/blog/d2r-season-13-tier-list-best-builds-in-reign-of-the-warlock
- **t4 doors:** `ZONE_CONTROL`, `GEOMETRY_COLLAPSE`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Abyss**: delivery=zone, motion_signature=inward_pull, count=1 · conf 0.75
  - `#1` **Miasma Chains**: delivery=zone, motion_signature=ground_place, count=1 · conf 0.75
  - `#2` **Miasma Bolt**: delivery=projectile, motion_signature=straight_line, count=1 · conf 0.75
  - `#3` **Sigil: Death**: delivery=zone, motion_signature=ground_place, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Abyss Warlock: vortex pull zone identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] Abyss pull-detonate is a composite mechanic (pull + DoT + detonate) that maps to vortex_pull but loses the DoT phase between pull and detonate. · downgrade-owner `elrond (W4 D2 tranche; internal-consistency reconcile, no W1 evidence — W5 is D2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
- **mapping deviation notes:** Abyss pull-detonate is a composite mechanic (pull + DoT + detonate) that maps to vortex_pull but loses the DoT phase between pull and detonate. Engine vortex_pull is a CC delivery; the damage-DoT-then-explode texture is fidelity loss.

## d2-wl-echoing-strike — Echoing Strike Warlock `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** physical · _raw_: physical?
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** rotw-s13+ · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 2 · **dossier rows:** 6
- **citations (2):** [authored] icy-veins.com · https://www.icy-veins.com/d2/echoing-strike-warlock-build; [authored] maxroll.gg · https://maxroll.gg/d2/guides/echoing-strike-warlock-guide
- **t4 doors:** `ELEMENT_CONVERSION_PHYSICAL`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Echoing Strike**: delivery=projectile, motion_signature=straight_line, count=1, pierce=all · conf 0.75
  - `#1` **Mirrored Blades**: delivery=projectile, speed=fast, motion_signature=fan_spread, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Echoing Strike Warlock: line projectile identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] Echoing out-and-return path is a unique mechanical feel (double-hit line) that the engine's line geometry approximates but loses the return-pass damage texture. · downgrade-owner `elrond (W4 D2 tranche; internal-consistency reconcile, no W1 evidence — W5 is D2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]
- **mapping deviation notes:** Echoing out-and-return path is a unique mechanical feel (double-hit line) that the engine's line geometry approximates but loses the return-pass damage texture. FCR-gated attack rate (not mana cost) as primary cadence gate is partially absorbed into economy note.

## d2-ww-sin — Whirlwind Assassin `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** lod-1.10+;d2r · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 6 / 0 / 0 · **dossier rows:** 6
- **citations (2):** [authored] icy-veins.com · https://www.icy-veins.com/d2/whirlwind-assassin-whirlwindsin-build; [authored] maxroll.gg · https://maxroll.gg/d2/guides/whirlwind-assassin
- **t4 doors:** `ELEMENT_CONVERSION_PHYSICAL`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Whirlwind (Chaos oskill)**: delivery=motion, range=melee, cadence=channel, motion_signature=orbit_fixed, count=1 · conf 0.75
  - `#1` **Fade**: delivery=aura, range=self, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Whirlwind Assassin: whirlwind motion identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] Claw-speed weapon-math produces different WW feel than barb version (faster claw ticks vs slower weapon pool); · downgrade-owner `elrond (W4 D2 tranche; internal-consistency reconcile, no W1 evidence — W5 is D2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'motion'` [green]
- **mapping deviation notes:** Claw-speed weapon-math produces different WW feel than barb version (faster claw ticks vs slower weapon pool); source player experiences this speed-math difference. Engine whirlwind geometry does not differentiate weapon-speed-math — noted as fidelity delta.

## d2-zealot — Zealot `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** lod;d2r;rotw-s13 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 7 / 0 / 1 · **dossier rows:** 6
- **citations (3):** [authored] icy-veins.com · https://www.icy-veins.com/d2/zealot-paladin-build; [authored] maxroll.gg · https://maxroll.gg/d2/guides/zeal-paladin; [authored] purediablo.com · https://www.purediablo.com/strategy/diablo-2-paladin-guide-zealot
- **t4 doors:** `TEMPORAL_CHARGE`, `MOMENTUM_CASCADE`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Zeal**: delivery=melee_arc, range=melee, motion_signature=point_strike, count=1 · conf 0.75
  - `#1` **Fanaticism**: delivery=aura, range=self, width=wide, count=1 · conf 0.75
  - `#2` **Holy Shield**: delivery=aura, range=self, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Zealot: melee strike melee_arc identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] Commitment-lock animation (cannot cancel mid-Zeal) is the build's defining mechanical feel; · downgrade-owner `elrond (W4 D2 tranche; internal-consistency reconcile, no W1 evidence — W5 is D2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'melee_arc'` [green]
- **mapping deviation notes:** Commitment-lock animation (cannot cancel mid-Zeal) is the build's defining mechanical feel; engine melee_strike does not carry an animation-lock mechanic. Source player experiences this as a tactical trade; engine approximates the 5-hit flurry output without the lock consequence.

## d2-blade-sin — Blade Fury sin `[NEGATIVE, class:record]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** lod · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 1 · **dossier rows:** 6
- **citations (2):** [official] diablo2.io · @Stormlash (data contributor) · https://diablo2.io/skills/blade-fury-t4001.html; [authored] purediablo.com · https://www.purediablo.com/strategy/diablo-2-guide-the-furysin-blade-fury
- **t4 doors:** `PERSISTENCE_ENGINE_uptime`, `TEMPORAL_CHARGE`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Blade Fury**: delivery=projectile, motion_signature=straight_line, count=1 · conf 0.75
  - `#1` **Blade Sentinel**: delivery=zone, cadence=cooldown, motion_signature=lane_place, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Blade Fury sin: line projectile identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] Player would miss: fixed-6fps IAS-immune cadence feel — engine cadence_scale approximates but lacks the hard-cap IAS-ignore mechanic; · downgrade-owner `elrond (W4 D2 tranche; internal-consistency reconcile, no W1 evidence — W5 is D2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]
- **mapping deviation notes:** Player would miss: fixed-6fps IAS-immune cadence feel — engine cadence_scale approximates but lacks the hard-cap IAS-ignore mechanic; blade-sentinel dual role (placed lane + synergy scalar) partially approximated.

## d2-blaze-sorc — Blaze Sorceress `[NEGATIVE, class:record]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** fire · _raw_: fire
- **elements attested:** fire
- **ailments attested:** _(none)_
- **eras:** lod · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 0 · **dossier rows:** 6
- **citations (2):** [official] classic.battle.net · https://classic.battle.net/diablo2exp/skills/sorceress-fire.shtml; [authored] maxroll.gg · @DarkHumility; MacroBioBoi (reviewer) · https://maxroll.gg/d2/guides/blaze-sorceress
- **t4 doors:** `PERSISTENCE_ENGINE_uptime`, `ZONE_CONTROL`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Blaze**: delivery=zone, cadence=channel, motion_signature=ground_place, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Blaze Sorceress: ground targeted circle zone identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **deviations:**
  - [accepted_downgrade] Player would miss: movement-paint ground trail delivery — engine has no 26-enum for 'movement-scribes-damage-path'; · downgrade-owner `elrond (W4 D2 tranche; internal-consistency reconcile, no W1 evidence — W5 is D2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
- **mapping deviation notes:** Player would miss: movement-paint ground trail delivery — engine has no 26-enum for 'movement-scribes-damage-path'; ground_targeted_circle approximates a placed ground DoT but misses the movement-as-painter feel; PERSISTENCE_ENGINE_uptime captures duration emphasis.

## d2-impale-zon — Impale Amazon `[NEGATIVE, class:record]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** classic;lod · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 6 / 0 / 0 · **dossier rows:** 6
- **citations (3):** [authored] diablo2.diablowiki.net · @Celine · https://diablo2.diablowiki.net/Guide:Amazon_Subclasses_v1.09,_by_Celine; [communal] us.forums.blizzard.com · @multiple community posters · https://us.forums.blizzard.com/en/d2r/t/impalefend-amazon-is-in-a-bad-state/101915; [official] classic.battle.net (Arreat Summit via Wayback) · @Blizzard Entertainment (official) · http://web.archive.org/web/20090324044010/http://classic.battle.net:80/diablo2exp/skills/amazon-javelin.shtml (archive: http://web.archive.org/web/20090324044010/http://classic.battle.net:80/diablo2exp/skills/amazon-javelin.shtml)
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Impale**: delivery=melee_arc, range=melee, motion_signature=point_strike, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Impale Amazon: melee strike melee_arc identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] Source player would miss: weapon durability drain penalty per hit (which IS the build's design tension and negative identity marker) has no engine economy lane. · downgrade-owner `elrond (W4 D2 tranche; internal-consistency reconcile, no W1 evidence — W5 is D2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'melee_arc'` [green]
- **mapping deviation notes:** Source player would miss: weapon durability drain penalty per hit (which IS the build's design tension and negative identity marker) has no engine economy lane. Mapping approximates the single-strike delivery but cannot express the item-degradation economy.

## d2-inferno-sorc — Inferno Sorceress `[NEGATIVE, class:record]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** fire · _raw_: fire
- **elements attested:** fire
- **ailments attested:** _(none)_
- **eras:** classic;lod · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 6 / 0 / 0 · **dossier rows:** 6
- **citations (4):** [communal] diablo2.wiki.fextralife.com · https://diablo2.wiki.fextralife.com/Inferno; [communal] diablo2.io · https://diablo2.io/skills/inferno-t4099.html; [authored] maxroll.gg · https://maxroll.gg/d2/guides/blaze-sorceress; [official] classic.battle.net (Arreat Summit via Wayback) · @Blizzard Entertainment (official) · http://web.archive.org/web/20090324044015/http://classic.battle.net:80/diablo2exp/skills/sorceress-fire.shtml (archive: http://web.archive.org/web/20090324044015/http://classic.battle.net:80/diablo2exp/skills/sorceress-fire.shtml)
- **t4 doors:** `PERSISTENCE_ENGINE_uptime`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Inferno**: delivery=beam, width=narrow, cadence=channel, motion_signature=straight_line, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Inferno Sorceress: beam channel beam identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **deviations:**
  - [accepted_downgrade] Source player would miss: (1) rooted-during-channel creates total positional vulnerability — a design texture approximated by delivery_notes but not an engine constraint; · downgrade-owner `elrond (W4 D2 tranche; internal-consistency reconcile, no W1 evidence — W5 is D2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'beam'` [green]
- **mapping deviation notes:** Source player would miss: (1) rooted-during-channel creates total positional vulnerability — a design texture approximated by delivery_notes but not an engine constraint; (2) fire immune hard-stop creates a secondary-skill requirement that has no engine analog in this mapping.

## d2-leap-attack-barb — Leap Attack Barbarian `[NEGATIVE, class:record]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** classic;lod · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 2 · **dossier rows:** 6
- **citations (2):** [communal] diablo2.io · @multiple community posters · https://diablo2.io/forums/my-thoughts-on-leap-attack-t929427.html; [official] classic.battle.net (Arreat Summit via Wayback) · @Blizzard Entertainment (official) · http://web.archive.org/web/20090326043850/http://classic.battle.net:80/diablo2exp/skills/barbarian-combatskills.shtml (archive: http://web.archive.org/web/20090326043850/http://classic.battle.net:80/diablo2exp/skills/barbarian-combatskills.shtml)
- **t4 doors:** `GEOMETRY_COLLAPSE`, `PHASE_MOMENTUM`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Leap Attack**: delivery=motion, range=melee, cadence=cooldown, motion_signature=leap_arc, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Leap Attack Barbarian: leap strike motion identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] Source player would miss: the classic/lod era Leap Attack (movement only, no meaningful damage) is genuinely a different kit; · downgrade-owner `elrond (W4 D2 tranche; internal-consistency reconcile, no W1 evidence — W5 is D2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'motion'` [green]
- **mapping deviation notes:** Source player would miss: the classic/lod era Leap Attack (movement only, no meaningful damage) is genuinely a different kit; mapping captures the D2R 2.4+ damage form. The 'movement IS the skill' texture is approximated by leap_strike but the distinction between movement-verb and damage-verb is a design dimension the engine geometry can't fully carry.

## d2-mosaic-sin — Mosaic Assassin `[class:record]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** lightning · _raw_: lightning
- **elements attested:** fire,lightning
- **ailments attested:** _(none)_
- **eras:** rotw-s13+;d2r-2.6+ · **tier:** T1 · **lineage:** d2/phoenix-strike
- **verify (C/X/U):** 5 / 0 / 2 · **dossier rows:** 6
- **citations (2):** [communal] diablo2.io · @Teebling · https://diablo2.io/runewords/mosaic-t1282119.html; [communal] diablo2.io · @Schnorki · https://diablo2.io/forums/mosaic-for-beginners-t1453557.html
- **t4 doors:** `TEMPORAL_CHARGE`, `ELEMENT_CONVERSION_HYBRID`, `MOMENTUM_CASCADE`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Phoenix Strike**: delivery=projectile, motion_signature=fan_spread, count=1 · conf 0.75
  - `#1` **Claws of Thunder**: delivery=beam, motion_signature=chain_hop, count=1, chain=2 · conf 0.75
  - `#2` **Dragon Claw**: delivery=melee_arc, range=melee, motion_signature=point_strike, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Mosaic Assassin: multi projectile projectile identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **deviations:**
  - [accepted_downgrade] Source player felt: build charges, finisher persists them, never deplete = sustained power ramp with no resource valley. · downgrade-owner `elrond (W4 D2 tranche; internal-consistency reconcile, no W1 evidence — W5 is D2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]
- **mapping deviation notes:** Source player felt: build charges, finisher persists them, never deplete = sustained power ramp with no resource valley. Engine has no charge-persistence-on-finisher mechanic — the Mosaic identity (charges never consumed = always-on elemental burst) cannot fully map. Closest: TEMPORAL_CHARGE + cycle shape. 'That build, worse' — the perpetual-charge feel is the identity.

## d2-rabies-wolf — Rabies Wolf `[class:record]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** chaos-poison · _raw_: poison
- **elements attested:** earth
- **ailments attested:** poison
- **eras:** lod;d2r · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 1 · **dossier rows:** 6
- **citations (2):** [communal] diablo2.io · @Deleted User 632 · https://diablo2.io/forums/mld-rabies-druid-t1063773.html; [communal] purediablo.com · https://www.purediablo.com/strategy/diablo-2-guide-druid-rabies-wolf-v1-10
- **t4 doors:** `GEOMETRY_PROPAGATION_cascade`, `PERSISTENCE_ENGINE_saturation`, `PHASE_MOMENTUM`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Werewolf**: delivery=aura, range=self, count=1 · conf 0.75
  - `#1` **Rabies**: delivery=melee_arc, range=melee, motion_signature=point_strike, count=1, chain=2 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Rabies Wolf: self buff aura identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] earth element register — _expressed by_ `element:earth`
- **deviations:**
  - [accepted_downgrade] Contagious spread mechanic (poison hops via target contact) has no engine geometry analogue — melee_strike + delivery note is 'that build, worse.' The defining loop feel (bite one, poison cascades through touching pack) cannot map without a chain-hop spread geometry or mechanic. · downgrade-owner `elrond (W4 D2 tranche; internal-consistency reconcile, no W1 evidence — W5 is D2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'aura'` [green]
- **mapping deviation notes:** Contagious spread mechanic (poison hops via target contact) has no engine geometry analogue — melee_strike + delivery note is 'that build, worse.' The defining loop feel (bite one, poison cascades through touching pack) cannot map without a chain-hop spread geometry or mechanic. Docket candidate filed for contact-propagation-DoT. GX-02 form-swap docket also relevant.

## d2-trapsin — Trapsin `[class:record]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** lightning · _raw_: lightning
- **elements attested:** lightning
- **ailments attested:** _(none)_
- **eras:** lod-1.10+;d2r;rotw-s13+ · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 6 / 0 / 2 · **dossier rows:** 6
- **citations (3):** [authored] maxroll.gg · https://maxroll.gg/d2/guides/lightning-sentry-assassin; [authored] icy-veins.com · https://www.icy-veins.com/d2/lightning-death-sentry-assassin-trapsin-build; [authored] icy-veins.com · https://www.icy-veins.com/d2/lightning-death-sentry-trapsin-build-skills
- **t4 doors:** `PROXY_ASCENSION`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Lightning Sentry**: delivery=summon_delegate, cadence=cooldown, count=10, pierce=all · conf 0.75
  - `#1` **Death Sentry**: delivery=summon_delegate, cadence=cooldown, count=1, chain=2 · conf 0.75
  - `#2` **Shadow Master**: delivery=summon_delegate, cadence=cooldown, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Trapsin: totem summon_delegate identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] lightning element register — _expressed by_ `element:lightning`
- **deviations:**
  - [engine_inexpressible] Shadow Master autonomous combatant maps as placed-proxy approximation (summoner-GAP). → _fix_ `new_door_rfc`
- **acceptance asserts:**
  - `primary_delivery_class == 'summon_delegate'` [green]
  - `expresses: Shadow Master autonomous combatant maps as placed-proxy approximation (summoner-` [red] · expected: RED until engine lane exists (routed to docket)
- **mapping deviation notes:** Shadow Master autonomous combatant maps as placed-proxy approximation (summoner-GAP). Source player gets a fully autonomous Assassin copy; engine gives a stationary placed emitter. The trap-placement core maps well; SM is the miss.

## d2-wl-blood-boil — Blood Boil Warlock `[class:record]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** fire · _raw_: shadow/blood?
- **elements attested:** fire
- **ailments attested:** _(none)_
- **eras:** rotw-s13+ · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 1 / 1 · **dossier rows:** 6
- **citations (2):** [authored] maxroll.gg · https://maxroll.gg/d2/guides/blood-boil-warlock-guide; [authored] icy-veins.com · https://www.icy-veins.com/d2/blood-boil-warlock-build
- **t4 doors:** `PROXY_FISSION`, `PERSISTENCE_ENGINE_uptime`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Blood Boil**: delivery=zone, motion_signature=ground_place, count=1 · conf 0.75
  - `#1` **Summon Tainted**: delivery=summon_delegate, cadence=cooldown, count=1 · conf 0.75
  - `#2` **Bind Demon**: delivery=projectile, motion_signature=straight_line, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Blood Boil Warlock: ground targeted circle zone identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **deviations:**
  - [engine_inexpressible] Summon Tainted is an autonomous fireball combatant — summoner-GAP means the engine loses the autonomous-attacker feel. → _fix_ `new_door_rfc`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
  - `expresses: Summon Tainted is an autonomous fireball combatant — summoner-GAP means the engi` [red] · expected: RED until engine lane exists (routed to docket)
- **mapping deviation notes:** Summon Tainted is an autonomous fireball combatant — summoner-GAP means the engine loses the autonomous-attacker feel. Blood Boil detonation of proxy demons maps via PROXY_FISSION but source player places actual autonomous demons then explodes them; engine gives proxies that explode. 'Not that build' only at the autonomous-combatant layer; detonation core approximates well.

## d2-golemancer — Golemancer `[NEGATIVE, class:record]`

- **grade / terminal:** `GAPPED` / `MAPPED_DOCKET`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** lod · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 0 · **dossier rows:** 6
- **citations (4):** [communal] alt.games.diablo2.narkive.com · @Buck Naked; Cernovog (multiple posters) · https://alt.games.diablo2.narkive.com/iHCyHN5J/golemancer-build; [communal] diablo2.io · @Asha; Schnorki; Conspirator (multiple posters) · https://diablo2.io/forums/iron-golem-survivability-t1330383.html; [communal] diablofans.com · @multiple community posters · https://www.diablofans.com/forums/read-only-diablo-forums/diablo-legacy-forums/diablo-ii/71381-summonancer-golems-or-skeletons; [official] classic.battle.net (Arreat Summit via Wayback) · @Blizzard Entertainment (official) · http://web.archive.org/web/20090324043656/http://classic.battle.net:80/diablo2exp/skills/necromancer-summoning.shtml (archive: http://web.archive.org/web/20090324043656/http://classic.battle.net:80/diablo2exp/skills/necromancer-summoning.shtml)
- **t4 doors:** `PROXY_SOVEREIGNTY`, `PROXY_ASCENSION`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Iron Golem**: delivery=summon_delegate, cadence=cooldown, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Golemancer: totem summon_delegate identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [engine_inexpressible] Not that build: autonomous combatant pet army engine has no engine lane. → _fix_ `new_door_rfc`
- **acceptance asserts:**
  - `primary_delivery_class == 'summon_delegate'` [green]
  - `expresses: Not that build: autonomous combatant pet army engine has no engine lane.` [red] · expected: RED until engine lane exists (routed to docket)
- **mapping deviation notes:** Not that build: autonomous combatant pet army engine has no engine lane. T4 doors reflect proxy-family shape; combat loop is genuinely un-mappable pending summoner-deferral resolution.

## d2-grim-ward-barb — Grim Ward Barbarian `[NEGATIVE, class:record]`

- **grade / terminal:** `GAPPED` / `MAPPED_DOCKET`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** fear
- **eras:** lod · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 3 · **dossier rows:** 6
- **citations (3):** [communal] diablo2.wiki.fextralife.com · https://diablo2.wiki.fextralife.com/Grim+Ward; [communal] diablo.fandom.com · https://diablo.fandom.com/wiki/Grim_Ward; [official] classic.battle.net (Arreat Summit via Wayback) · @Blizzard Entertainment (official) · http://web.archive.org/web/20090325112811/http://classic.battle.net:80/diablo2exp/skills/barbarian-warcries.shtml (archive: http://web.archive.org/web/20090325112811/http://classic.battle.net:80/diablo2exp/skills/barbarian-warcries.shtml)
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Grim Ward**: delivery=summon_delegate, cadence=cooldown, count=1 · conf 0.75
  - `#1` **Combat (implied primary — Grim Ward presupposes a kill verb)**: delivery=melee_arc, range=melee, motion_signature=point_strike, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Grim Ward Barbarian: totem summon_delegate identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [engine_inexpressible] Not that build: Grim Ward Barbarian as a named archetype is unattested; → _fix_ `new_door_rfc`
- **acceptance asserts:**
  - `primary_delivery_class == 'summon_delegate'` [green]
  - `expresses: Not that build: Grim Ward Barbarian as a named archetype is unattested;` [red] · expected: RED until engine lane exists (routed to docket)
- **mapping deviation notes:** Not that build: Grim Ward Barbarian as a named archetype is unattested; kit identity is partial-recovery only. Even if identity were confirmed, the combat loop (area-denial only, zero damage engine) has no engine lane mapping. Fear is attested and emitted correctly.

## d2-horker — Horker `[class:record]`

- **grade / terminal:** `GAPPED` / `MAPPED_DOCKET`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** lod;d2r · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 2 · **dossier rows:** 6
- **citations (1):** [authored] yesgamers.com · https://www.yesgamers.com/diablo-2/horker-build
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Whirlwind**: delivery=motion, range=melee, cadence=channel, motion_signature=orbit_fixed, count=1 · conf 0.75
  - `#1` **Berserk**: delivery=melee_arc, range=melee, motion_signature=point_strike, count=1 · conf 0.75
  - `#2` **Find Item**: delivery=projectile, motion_signature=straight_line, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Horker: whirlwind motion identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [engine_inexpressible] Not that build: the Horker's defining loop-verb is Find Item corpse re-rolls for loot economy — there is no engine lane for meta-game loot re-roll identity. → _fix_ `new_door_rfc`
- **acceptance asserts:**
  - `primary_delivery_class == 'motion'` [green]
  - `expresses: Not that build: the Horker's defining loop-verb is Find Item corpse re-rolls for` [red] · expected: RED until engine lane exists (routed to docket)
- **mapping deviation notes:** Not that build: the Horker's defining loop-verb is Find Item corpse re-rolls for loot economy — there is no engine lane for meta-game loot re-roll identity. Combat verbs (Whirlwind/Berserk) map but don't constitute the build.

## d2-sacrifice — Sacrifice (Paladin) `[NEGATIVE, class:record]`

- **grade / terminal:** `GAPPED` / `MAPPED_DOCKET`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** lod · **tier:** — · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 0 · **dossier rows:** 6
- **citations (5):** [official] diablo2.io · https://diablo2.io/skills/sacrifice-t4149.html; [communal] diablo2.io · @Maldoror · https://diablo2.io/forums/sacrifice-paladin-t1456874.html; [communal] purediablo.com · https://www.purediablo.com/forums/threads/sacrifice-and-self-damage.171072/; [official] web.archive.org · http://archive.org/wayback/available?url=classic.battle.net/diablo2exp/skills/paladin/combatskills.shtml&timestamp=20050101; [official] classic.battle.net (Arreat Summit via Wayback) · @Blizzard Entertainment (official) · http://web.archive.org/web/20090325132146/http://classic.battle.net:80/diablo2exp/skills/paladin-combat.shtml (archive: http://web.archive.org/web/20090325132146/http://classic.battle.net:80/diablo2exp/skills/paladin-combat.shtml)
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Sacrifice**: delivery=melee_arc, range=melee, motion_signature=point_strike, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Sacrifice (Paladin): melee strike melee_arc identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [engine_inexpressible] Self-damage-on-hit primary attack has no engine lane as a build identity. → _fix_ `new_door_rfc`
- **acceptance asserts:**
  - `primary_delivery_class == 'melee_arc'` [green]
  - `expresses: Self-damage-on-hit primary attack has no engine lane as a build identity.` [red] · expected: RED until engine lane exists (routed to docket)
- **mapping deviation notes:** Self-damage-on-hit primary attack has no engine lane as a build identity. SACRIFICE_ASCENDANCY T4 exists but requires a functioning damage loop to capstone — Sacrifice has no viable primary loop. The kit's verified identity is self-damage curiosity / Smite synergy ingredient, not a playable primary build. 'Not that build' → GAPPED.

## d2-summon-druid — Summon Druid `[class:record]`

- **grade / terminal:** `GAPPED` / `MAPPED_DOCKET`
- **element (court):** physical · _raw_: physical
- **elements attested:** earth
- **ailments attested:** _(none)_
- **eras:** lod;rotw;d2r-2.4+ · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 7 / 0 / 1 · **dossier rows:** 6
- **citations (2):** [communal] diablo2.io · @tmGrunty · https://diablo2.io/forums/2-7-summon-druid-guide-t903558.html; [communal] purediablo.com · https://www.purediablo.com/strategy/diablo-2-guide-druid-summoner
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Summon Grizzly**: delivery=summon_delegate, cadence=cooldown, count=1 · conf 0.75
  - `#1` **Dire Wolves**: delivery=summon_delegate, cadence=cooldown, count=1 · conf 0.75
  - `#2` **Ravens**: delivery=summon_delegate, cadence=cooldown, count=1 · conf 0.75
  - `#3` **Oak Sage**: delivery=aura, range=self, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Summon Druid: totem summon_delegate identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] earth element register — _expressed by_ `element:earth`
- **deviations:**
  - [engine_inexpressible] Kit identity is full autonomous-pet menagerie command — the player's loop is 'summon, reposition, maintain.' No engine lane for autonomous combatants. → _fix_ `new_door_rfc`
- **acceptance asserts:**
  - `primary_delivery_class == 'summon_delegate'` [green]
  - `expresses: Kit identity is full autonomous-pet menagerie command — the player's loop is 'su` [red] · expected: RED until engine lane exists (routed to docket)
- **mapping deviation notes:** Kit identity is full autonomous-pet menagerie command — the player's loop is 'summon, reposition, maintain.' No engine lane for autonomous combatants. Oak Sage aura maps as stand-alone but the kit without its summoned army is not the kit.

## d2-summonmancer — Summonmancer `[class:record]`

- **grade / terminal:** `GAPPED` / `MAPPED_DOCKET`
- **element (court):** physical · _raw_: physical
- **elements attested:** earth,shadow
- **ailments attested:** curse:amplify
- **eras:** classic;lod-1.10+;d2r;rotw-s14 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 9 / 0 / 1 · **dossier rows:** 6
- **citations (3):** [communal] purediablo.com · https://www.purediablo.com/forums/threads/meet-tartarus-the-summoner-necromancer.15049/; [communal] purediablo.com · https://www.purediablo.com/strategy/bone-summon-v-2-0; [communal] diablo2.io · @DopamineJunky · https://diablo2.io/forums/summon-build-t1459264.html
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Raise Skeleton**: delivery=summon_delegate, cadence=cooldown, count=1 · conf 0.75
  - `#1` **Corpse Explosion**: delivery=zone, motion_signature=ground_place, count=1 · conf 0.75
  - `#2` **Amplify Damage**: delivery=aura, range=self, count=1 · conf 0.75
  - `#3` **Clay Golem**: delivery=summon_delegate, cadence=cooldown, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Summonmancer: totem summon_delegate identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] shadow element register — _expressed by_ `element:shadow`
- **deviations:**
  - [engine_inexpressible] Core loop (kill → corpse → raise skeleton + corpse explode → kill → repeat) is the engine's most complex missing mechanic — both summoner GAP and spatial-consumable-resource-node gap simultaneously. → _fix_ `new_door_rfc`
- **acceptance asserts:**
  - `primary_delivery_class == 'summon_delegate'` [green]
  - `expresses: Core loop (kill → corpse → raise skeleton + corpse explode → kill → repeat) is t` [red] · expected: RED until engine lane exists (routed to docket)
- **mapping deviation notes:** Core loop (kill → corpse → raise skeleton + corpse explode → kill → repeat) is the engine's most complex missing mechanic — both summoner GAP and spatial-consumable-resource-node gap simultaneously. Amp Damage maps cleanly; CE and skeletons do not.

## d2-teleport-sorc — Teleport Sorceress `[class:record]`

- **grade / terminal:** `GAPPED` / `MAPPED_DOCKET`
- **element (court):** _(unassigned)_ · _raw_: n/a
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** lod;d2r-2.4+ · **tier:** — · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 1 · **dossier rows:** 6
- **citations (2):** [official] diablo2.io · https://diablo2.io/skills/teleport-t4176.html; [communal] purediablo.com · https://www.purediablo.com/forums/threads/build-idea-defensive-8-person-baal-teleporter-for-exp-runs-der-0.130063/
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Teleport**: delivery=motion, speed=instant, motion_signature=blink_translate, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Teleport Sorceress: teleport motion identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [engine_inexpressible] No combat loop attested — the kit's identity is metagame transport service. → _fix_ `new_door_rfc`
- **acceptance asserts:**
  - `primary_delivery_class == 'motion'` [green]
  - `expresses: No combat loop attested — the kit's identity is metagame transport service.` [red] · expected: RED until engine lane exists (routed to docket)
- **mapping deviation notes:** No combat loop attested — the kit's identity is metagame transport service. Any combat mapping would be fabrication. Engine teleport geometry exists but the kit has no damage output to attach it to. First purely-utility non-combat kit in basin-3.

## d2-wl-tainted-summoner — Tainted Summoner Warlock `[class:record]`

- **grade / terminal:** `GAPPED` / `MAPPED_DOCKET`
- **element (court):** _(unassigned)_ · _raw_: shadow?
- **elements attested:** fire
- **ailments attested:** _(none)_
- **eras:** rotw-s13+ · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 3 · **dossier rows:** 6
- **citations (2):** [authored] maxroll.gg · https://maxroll.gg/d2/guides/summoner-warlock-guide; [authored] maxroll.gg · https://maxroll.gg/d2/guides/blood-boil-warlock-guide
- **t4 doors:** `PROXY_ASCENSION`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Bind Demon**: delivery=projectile, motion_signature=straight_line, count=1 · conf 0.75
  - `#1` **Summon Tainted**: delivery=summon_delegate, cadence=cooldown, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Tainted Summoner Warlock: single target projectile identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **deviations:**
  - [engine_inexpressible] Kit identity is autonomous-demon-army summoner (Bind Demon accumulate + Summon Tainted autonomous combatants). → _fix_ `new_door_rfc`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]
  - `expresses: Kit identity is autonomous-demon-army summoner (Bind Demon accumulate + Summon T` [red] · expected: RED until engine lane exists (routed to docket)
- **mapping deviation notes:** Kit identity is autonomous-demon-army summoner (Bind Demon accumulate + Summon Tainted autonomous combatants). Both are summoner-GAP territory. ERRATA-55 unattested folk-name adds identity uncertainty. The kit as described is 'not that build' in engine without autonomous-combatant support.

## d2-wl-void-rift — Void Rift Warlock `[NEGATIVE, class:record]`

- **grade / terminal:** `GAPPED` / `MAPPED_DOCKET`
- **element (court):** chaos-poison · _raw_: void?
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** rotw-s13+ · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 0 / 0 / 4 · **dossier rows:** 6
- **citations (3):** [authored] icy-veins.com · https://www.icy-veins.com/d2/warlock-class-and-builds; [authored] maxroll.gg · https://maxroll.gg/d2/resources/warlock-overview; [communal] gurugamer.com · https://gurugamer.com/pc-console/complete-list-of-warlock-skills-in-diablo-2-resurrected-26393
- **t4 delta:** shape `step` (signoff: unvalidated)
- **deviations:**
  - [engine_inexpressible] No attested mechanics, no attested identity, no attested skills. → _fix_ `new_door_rfc`
- **acceptance asserts:**
  - `kit_identity_present == true` [green]
  - `expresses: No attested mechanics, no attested identity, no attested skills.` [red] · expected: RED until engine lane exists (routed to docket)
- **mapping deviation notes:** No attested mechanics, no attested identity, no attested skills. Kit is a probable spec-error / phantom entry. All mapping surfaces empty per honest-evidence-only discipline. 'Not that build' is an understatement — no verified build exists. [D-7.1 keep-as-ghost 2026-07-19: kb-hallucination-class ghost; harvest FAILED all four families (honest-negative); retained as a DOCUMENTED NEGATIVE, not excised (deletion is Matt-tier). Registered ghost, not a live kit.]

