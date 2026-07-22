# VDM-2 Compendium — poe2 (38 kits)

> **Source:** `corpus.db` `kit_master` view (574) ENRICHED live with the six VDM-2 side-car blocks + two registries (render-layer joins; DB never mutated). **v2.0** · db md5 `bebc933b0bf9bcab5988bbc16bcc55b4` · generated 2026-07-22T09:46:42Z.
> `court` is the reconciled element court (enum-checked); `original_element` carries raw provenance. Raw mobile-era descriptors (`elem_raw`) are NOT exposed (provenance-only). `kit_citations` is the sole citation authority.

| grade | n | verify (C/X/U) | dossier | cited | geom-bands | hooks |
|---|---|---|---|---|---|---|
| E 0 · C 27 · A 11 · G 0 | 38 | 167/8/26 | 228 | 38/38 | 59 | 61 |

## poe2-blood-mage — Blood Mage `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** bleed,sunder
- **eras:** 0.1;0.2-dawn;0.3-edict;0.4 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 1 · **dossier rows:** 6
- **citations (4):** [communal] maxroll.gg · https://maxroll.gg/poe2/resources/bloodmage-ascendancy; [dataset] poe2db.tw · https://poe2db.tw/us/Bonestorm; [dataset] poe.ninja · https://poe.ninja/poe2/builds/vaal?class=Blood+Mage&skills=Life+Remnants; [communal] pathofexile.com · @DrugaddictMenemist#6176 · https://www.pathofexile.com/forum/view-thread/3592603
- **t4 doors:** `SACRIFICE_ASCENDANCY`, `RETRIBUTION_ENGINE`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Bonestorm**: delivery=projectile, cadence=channel, motion_signature=fan_spread, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Blood Mage: multi projectile projectile identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [engine_inexpressible] Minor drift: the 150%-of-max-life OVERHEAL buffer (the survivability core of the build -- you bank effective HP above your bar) is not expressible as a native key, so it degrades to a note + docket-candidate; → _fix_ `new_door_rfc`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]
  - `expresses: Minor drift: the 150%-of-max-life OVERHEAL buffer (the survivability core of the` [red] · expected: RED until engine lane exists (routed to docket)
- **mapping deviation notes:** Minor drift: the 150%-of-max-life OVERHEAL buffer (the survivability core of the build -- you bank effective HP above your bar) is not expressible as a native key, so it degrades to a note + docket-candidate; the clamp of hp_cost_scale to 0.30 may under-state the source's Life pressure. Geometry+ailment+on-kill loop otherwise map cleanly, so CLOSE not APPROX.

## poe2-bonestorm — Bonestorm `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** root,sunder
- **eras:** 0.1;0.2-dawn;0.5-ancients · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 1 · **dossier rows:** 6
- **citations (3):** [dataset] poe2db.tw · https://poe2db.tw/us/Bonestorm; [communal] pathofexile.com · https://www.pathofexile.com/forum/view-thread/3852711; [communal] pathofexile.com · https://www.pathofexile.com/forum/view-thread/3706145
- **t4 doors:** `GEOMETRY_COLLAPSE`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Bone Storm**: delivery=projectile, cadence=channel, motion_signature=fan_spread, count=1 · conf 0.75
  - `#1` **Bone Cage**: delivery=zone, cadence=cooldown, motion_signature=lane_place, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Bonestorm: multi projectile projectile identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] Minor drift: Bone Cage's exact shape is under-specified in source (only 'defensive panic button'), so its placed_lane+root mapping is a reasonable-but-thin inference. · downgrade-owner `elrond (W4 PoE2 tranche; internal-consistency reconcile, no W1 evidence — W5 is PoE2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]
- **mapping deviation notes:** Minor drift: Bone Cage's exact shape is under-specified in source (only 'defensive panic button'), so its placed_lane+root mapping is a reasonable-but-thin inference. The core Bonestorm channel-release-Impale loop maps cleanly (geometry+sunder+accumulator), so CLOSE.

## poe2-cof-comet — Cast on Freeze Comet `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** cold · _raw_: cold
- **elements attested:** water
- **ailments attested:** chill,freeze
- **eras:** 0.1;0.4 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 6 / 0 / 0 · **dossier rows:** 6
- **citations (2):** [communal] maxroll.gg · https://maxroll.gg/poe2/build-guides/cast-on-freeze-comet-stormweaver-leveling-guide; [communal] pathofexile.com · https://www.pathofexile.com/forum/view-thread/3612731
- **t4 doors:** `ELEMENTAL_ECHO`, `GEOMETRY_COLLAPSE`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Cast on Freeze (meta gem)**: delivery=aura, range=self, count=1 · conf 0.75
  - `#1` **Comet (triggered)**: delivery=zone, motion_signature=ground_place, count=1 · conf 0.75
  - `#2` **Frostbolt**: delivery=projectile, motion_signature=straight_line, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Cast on Freeze Comet: self buff aura identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] water element register — _expressed by_ `element:water`
- **deviations:**
  - [accepted_downgrade] Minor drift: the two-layer trigger-ENERGY economy (freeze builds trigger energy that discharges Comet -- the exact mechanic 0.1.0d nerfed) is expressed only as 'free proc-cast', losing the energy-accumulation gate between freezes. · downgrade-owner `elrond (W4 PoE2 tranche; internal-consistency reconcile, no W1 evidence — W5 is PoE2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'aura'` [green]
- **mapping deviation notes:** Minor drift: the two-layer trigger-ENERGY economy (freeze builds trigger energy that discharges Comet -- the exact mechanic 0.1.0d nerfed) is expressed only as 'free proc-cast', losing the energy-accumulation gate between freezes. The freeze->trigger->Comet loop and shatter payoff otherwise map cleanly via R-M9, so CLOSE.

## poe2-concoction — Concoction Pathfinder `[NEGATIVE, class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** chaos-poison · _raw_: chaos
- **elements attested:** earth
- **ailments attested:** poison
- **eras:** 0.1;0.2-dawn;0.3-edict;0.4;0.5-ancients · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 3 / 1 / 1 · **dossier rows:** 6
- **citations (3):** [communal] maxroll.gg · https://maxroll.gg/poe2/build-guides/poisonous-concoction-pathfinder-build-guide; [communal] pathofexile.com · https://www.pathofexile.com/forum/view-thread/3635301; [dataset] poe.ninja · https://poe.ninja/poe2/builds/dawn?class=Pathfinder&skills=Poisonous+Concoction
- **t4 doors:** `PERSISTENCE_ENGINE`, `GEOMETRY_COLLAPSE`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Poisonous Concoction**: delivery=zone, motion_signature=ground_place, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Concoction Pathfinder: ground targeted circle zone identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] earth element register — _expressed by_ `element:earth`
- **deviations:**
  - [accepted_downgrade] Minor drift: the flask-charge-as-ammo economy (your damage skill literally spends flask charges, gated by charge-recovery mods) maps to a cycle-shape + note but loses the tight flask-sustain-vs-fire-rate tension that IS the Pathfinder identity; · downgrade-owner `elrond (W4 PoE2 tranche; internal-consistency reconcile, no W1 evidence — W5 is PoE2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
- **mapping deviation notes:** Minor drift: the flask-charge-as-ammo economy (your damage skill literally spends flask charges, gated by charge-recovery mods) maps to a cycle-shape + note but loses the tight flask-sustain-vs-fire-rate tension that IS the Pathfinder identity; the RNG element-variant framing (Poison/Fire/Ice from one Concoction chassis) is collapsed to the confirmed poison variant. Core throw-poison loop maps cleanly, so CLOSE.

## poe2-erasure-edc-lich — Erasure DoT Contagion Lich `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** chaos-poison · _raw_: chaos
- **elements attested:** shadow
- **ailments attested:** curse:amplify,drain
- **eras:** 0.2-dawn;0.3-edict;0.4;0.5-ancients · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 2 · **dossier rows:** 6
- **citations (2):** [communal] maxroll.gg · https://maxroll.gg/poe2/build-guides/essence-drain-lich-build-guide; [communal] maxroll.gg · https://maxroll.gg/poe2/resources/lich-ascendancy-overview
- **t4 doors:** `GEOMETRY_PROPAGATION`, `PERSISTENCE_ENGINE`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Essence Drain**: delivery=projectile, speed=instant, motion_signature=straight_line, count=1 · conf 0.75
  - `#1` **Contagion**: delivery=zone, motion_signature=ground_place, count=1, chain=2 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Erasure DoT Contagion Lich: single target projectile identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] shadow element register — _expressed by_ `element:shadow`
- **deviations:**
  - [accepted_downgrade] Minor drift, and it is CLEAN: with the Erasure phantom removed per binding, the kit IS classic Essence-Drain/Contagion -- a chaos-DoT projectile + on-kill AoE-spread propagation -- which maps to GEOMETRY_PROPAGATION + drain almost exactly. · downgrade-owner `elrond (W4 PoE2 tranche; internal-consistency reconcile, no W1 evidence — W5 is PoE2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]
- **mapping deviation notes:** Minor drift, and it is CLEAN: with the Erasure phantom removed per binding, the kit IS classic Essence-Drain/Contagion -- a chaos-DoT projectile + on-kill AoE-spread propagation -- which maps to GEOMETRY_PROPAGATION + drain almost exactly. The only loss is the unverifiable 'Erasure amplifies the spread chain' claim, which by ruling we grade as nonexistent. If Erasure is later confirmed real this may need revisit, but on current source CLOSE is honest. [D-7.7 2026-07-19: possible-phantom annotation KEPT; NO deletion (poe2-REVIEW-2 / b1-REVIEW-2; deletion is Matt-only). 'Erasure' remains unverified-possible-phantom; Essence Drain + Contagion are CONFIRMED real.]

## poe2-galvanic-shards — Galvanic Shards Merc `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** lightning · _raw_: lightning
- **elements attested:** lightning
- **ailments attested:** sunder
- **eras:** 0.1 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 0 · **dossier rows:** 6
- **citations (4):** [dataset] poe2db.tw · https://poe2db.tw/us/Galvanic_Shards; [dataset] poe2db.tw · https://poe2db.tw/us/Armour_Piercing_Rounds; [dataset] poe.ninja · https://poe.ninja/poe2/builds/dawn?skills=Galvanic+Shards; [communal] pathofexile.com · https://www.pathofexile.com/forum/view-thread/3705011
- **t4 doors:** `GEOMETRY_PROPAGATION`, `GEOMETRY_COLLAPSE`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Galvanic Shards**: delivery=projectile, motion_signature=fork_split, count=1, chain=2 · conf 0.75
  - `#1` **Armour Piercing Rounds**: delivery=projectile, speed=fast, motion_signature=fan_spread, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Galvanic Shards Merc: fork projectile identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] lightning element register — _expressed by_ `element:lightning`
- **deviations:**
  - [accepted_downgrade] Minor drift: the two-stage projectile->beam transformation (bolts that BECOME chaining beams mid-flight) has no single 26-geometry member that carries both the fan-out AND the beam-chain, so fork (stage 1, dominant) + a GEOMETRY_PROPAGATION door (stage 2) approximate it -- the source player loses the visual of fragments morphing into forking beams as one continuous emission. · downgrade-owner `elrond (W4 PoE2 tranche; internal-consistency reconcile, no W1 evidence — W5 is PoE2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]
- **mapping deviation notes:** Minor drift: the two-stage projectile->beam transformation (bolts that BECOME chaining beams mid-flight) has no single 26-geometry member that carries both the fan-out AND the beam-chain, so fork (stage 1, dominant) + a GEOMETRY_PROPAGATION door (stage 2) approximate it -- the source player loses the visual of fragments morphing into forking beams as one continuous emission. The shotgun fan, lightning, shock, and armour-break-sunder all map cleanly, so CLOSE.

## poe2-gas-arrow-ignite — Gas Arrow Detonation `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** fire · _raw_: fire
- **elements attested:** earth,fire
- **ailments attested:** burn,poison
- **eras:** 0.1;0.2-dawn;0.3-edict · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 0 · **dossier rows:** 6
- **citations (3):** [dataset] poe2db.tw · https://poe2db.tw/us/Gas_Arrow; [communal] maxroll.gg · https://maxroll.gg/poe2/build-guides/deadeye-gas-arrow-leveling-guide; [communal] pathofexile.com · https://www.pathofexile.com/forum/view-thread/3632515
- **t4 doors:** `GEOMETRY_PROPAGATION`, `ELEMENT_CONVERSION_PHYSICAL`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Gas Arrow (detonation)**: delivery=zone, motion_signature=ground_place, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Gas Arrow Detonation: ground targeted circle zone identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **deviations:**
  - [accepted_downgrade] Minor drift: the two-stage place-then-detonate mechanic (a cloud you plant and then must IGNITE with a second skill) maps to a single ground_targeted_circle (the detonation) + an arming-stage note -- the source player loses the deliberate two-input setup/payoff rhythm and the cloud-expansion-over-time window (1.8m growing +80%). · downgrade-owner `elrond (W4 PoE2 tranche; internal-consistency reconcile, no W1 evidence — W5 is PoE2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
- **mapping deviation notes:** Minor drift: the two-stage place-then-detonate mechanic (a cloud you plant and then must IGNITE with a second skill) maps to a single ground_targeted_circle (the detonation) + an arming-stage note -- the source player loses the deliberate two-input setup/payoff rhythm and the cloud-expansion-over-time window (1.8m growing +80%). The detonation blast, hybrid fire/poison, and conversion all map cleanly, so CLOSE.

## poe2-howa-invoker — HoWA Invoker `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** lightning · _raw_: lightning
- **elements attested:** lightning
- **ailments attested:** sunder
- **eras:** 0.1;0.2-dawn · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 0 · **dossier rows:** 6
- **citations (3):** [dataset] poe2db.tw · https://poe2db.tw/us/Hand_of_Wisdom_and_Action; [authored] maxroll.gg · https://maxroll.gg/poe2/build-guides/flicker-strike-invoker-build-guide; [authored] maxroll.gg · https://maxroll.gg/poe2/build-guides/tempest-flurry-gemling-legionnaire-build-guide
- **t4 doors:** `ELEMENTAL_ECHO`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Tempest Flurry / Ice Strike host, empowered by Hand of Wisdom and Action**: delivery=melee_arc, range=melee, motion_signature=point_strike, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] HoWA Invoker: melee strike melee_arc identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] lightning element register — _expressed by_ `element:lightning`
- **deviations:**
  - [accepted_downgrade] A HoWA player would get flat-lightning melee that scales on GEAR AFFIXES rather than on an attribute-TOTAL -- the identity 'my stat page is my weapon' (damage as a linear function of stacked INT+DEX) is softened to a static added-damage affix. · downgrade-owner `elrond (W4 PoE2 tranche; internal-consistency reconcile, no W1 evidence — W5 is PoE2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'melee_arc'` [green]
- **mapping deviation notes:** A HoWA player would get flat-lightning melee that scales on GEAR AFFIXES rather than on an attribute-TOTAL -- the identity 'my stat page is my weapon' (damage as a linear function of stacked INT+DEX) is softened to a static added-damage affix. Playable output preserved (CLOSE); the missing coupling is a qualitative mint-candidate for steward review, kit graded un-minted.

## poe2-ice-strike-invoker — Ice Strike Invoker `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** cold · _raw_: cold
- **elements attested:** lightning,water
- **ailments attested:** chill,freeze
- **eras:** 0.1;0.2-dawn · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 6 / 0 / 0 · **dossier rows:** 6
- **citations (3):** [authored] maxroll.gg · @Milkybk_ · https://maxroll.gg/poe2/build-guides/tempest-flurry-invoker-leveling-guide; [authored] odealo.com · https://odealo.com/articles/ice-strike-invoker-poe2-build; [communal] rpgstash.com · https://www.rpgstash.com/blog/poe-2-020-ice-strike-invoker-build-guide
- **t4 doors:** `TEMPORAL_CHARGE`, `GEOMETRY_COLLAPSE`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Ice Strike**: delivery=melee_arc, range=melee, speed=fast, motion_signature=point_strike, count=1 · conf 0.75
  - `#1` **Charged Staff / Herald of Ice (finisher + on-freeze-kill explosion)**: delivery=zone, cadence=builder_spender, motion_signature=burst_around_self, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Ice Strike Invoker: melee strike melee_arc identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] water element register — _expressed by_ `element:water`
- **deviations:**
  - [accepted_downgrade] A minor drift: the two distinct accumulators the source exposes (Combo Points on Ice Strike AND Power Charges spent by Charged Staff) are modeled as one builder-spender accumulator + spend-burst; · downgrade-owner `elrond (W4 PoE2 tranche; internal-consistency reconcile, no W1 evidence — W5 is PoE2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'melee_arc'` [green]
- **mapping deviation notes:** A minor drift: the two distinct accumulators the source exposes (Combo Points on Ice Strike AND Power Charges spent by Charged Staff) are modeled as one builder-spender accumulator + spend-burst; the player keeps the freeze->shatter payoff and the bank-then-dump feel, so the drift is the second charge-type's separate identity.

## poe2-infernal-legion — Infernal Legion Minions `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** fire · _raw_: fire
- **elements attested:** fire
- **ailments attested:** burn
- **eras:** 0.2-dawn;0.3-edict;0.4 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 1 · **dossier rows:** 6
- **citations (3):** [authored] maxroll.gg · @Shayd · https://maxroll.gg/poe2/build-guides/infernal-legion-lich-build-guide; [official] maxroll.gg · https://maxroll.gg/poe2/news/0-5-0-patch-notes-return-of-the-ancients; [communal] pathofexile.com · https://www.pathofexile.com/forum/view-thread/3856260
- **t4 doors:** `PROXY_ASCENSION`, `PERSISTENCE_ENGINE_uptime`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Infernal Legion (support gem on minions -> self-immolation fire aura)**: delivery=aura, range=self, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Infernal Legion Minions: aura aura identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **deviations:**
  - [accepted_downgrade] The self-immolation-as-damage-source flavor (minions burn THEMSELVES to deal damage; · downgrade-owner `elrond (W4 PoE2 tranche; internal-consistency reconcile, no W1 evidence — W5 is PoE2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'aura'` [green]
- **mapping deviation notes:** The self-immolation-as-damage-source flavor (minions burn THEMSELVES to deal damage; their deaths are the payoff) is softened -- engine minion-proxy damage is the minion's own attacks, not a self-sacrifice burn loop. Proxy identity is expressible (CLOSE); the deviation is the suicide-burn mechanism reading as ordinary proxy damage.

## poe2-lightning-arrow-deadeye — Lightning Arrow Deadeye `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** lightning · _raw_: lightning
- **elements attested:** lightning
- **ailments attested:** sunder
- **eras:** 0.1;0.2-dawn;0.3-edict;0.4;0.5-ancients · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 8 / 0 / 1 · **dossier rows:** 6
- **citations (1):** [authored] maxroll.gg · @Crouching_Tuna · https://maxroll.gg/poe2/build-guides/lightning-arrow-deadeye
- **t4 doors:** `ELEMENTAL_ECHO`, `GEOMETRY_PROPAGATION_cascade`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Lightning Arrow**: delivery=beam, speed=fast, motion_signature=chain_hop, count=1, chain=2 · conf 0.75
  - `#1` **Lightning Rod**: delivery=zone, motion_signature=ground_place, count=1, chain=2 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Lightning Arrow Deadeye: chain beam identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] lightning element register — _expressed by_ `element:lightning`
- **deviations:**
  - [accepted_downgrade] Two verified drifts noted: (1) engine chain hops sequentially and decays 0.7x/hop, whereas Lightning Arrow's beam splash is simultaneous at full damage to up to 3 targets -- a LA player's screen-clear is slightly weaker per-hop; · downgrade-owner `elrond (W4 PoE2 tranche; internal-consistency reconcile, no W1 evidence — W5 is PoE2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'beam'` [green]
- **mapping deviation notes:** Two verified drifts noted: (1) engine chain hops sequentially and decays 0.7x/hop, whereas Lightning Arrow's beam splash is simultaneous at full damage to up to 3 targets -- a LA player's screen-clear is slightly weaker per-hop; (2) Lightning Rod's placed boss-zone is approximated as ground_targeted_circle rather than a shot-empowered rod. Both preserve the run-and-gun chain identity.

## poe2-lightning-spear-amazon — Lightning Spear Amazon `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** lightning · _raw_: lightning
- **elements attested:** lightning
- **ailments attested:** sunder
- **eras:** 0.2-dawn;0.3-edict · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 6 / 0 / 0 · **dossier rows:** 6
- **citations (2):** [authored] maxroll.gg · @Crouching_Tuna · https://maxroll.gg/poe2/build-guides/lightning-spear-amazon; [communal] thegamer.com · https://www.thegamer.com/path-of-exile-2-poe2-huntress-class-ascendancies-guide/
- **t4 doors:** `GEOMETRY_PROPAGATION_overkill`, `ELEMENTAL_ECHO`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Lightning Spear**: delivery=projectile, width=wide, motion_signature=fan_spread, count=1 · conf 0.75
  - `#1` **Storm Lance / Explosive Spear (boss single-target rotation)**: delivery=projectile, motion_signature=straight_line, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Lightning Spear Amazon: multi projectile projectile identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] lightning element register — _expressed by_ `element:lightning`
- **deviations:**
  - [accepted_downgrade] Minor drift: the secondary-bolt cascade is modeled as a multi_projectile shotgun + on-hit propagation; · downgrade-owner `elrond (W4 PoE2 tranche; internal-consistency reconcile, no W1 evidence — W5 is PoE2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]
- **mapping deviation notes:** Minor drift: the secondary-bolt cascade is modeled as a multi_projectile shotgun + on-hit propagation; the source's specific crit-engine-triggers-on-fork-bolts amplification (crit density scaling off the secondaries) is carried in traits, not as a distinct mechanic -- the fanout clear identity is preserved.

## poe2-minion-infernalist — Minion Infernalist `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** fire · _raw_: fire
- **elements attested:** fire
- **ailments attested:** burn
- **eras:** 0.1;0.2-dawn;0.3-edict;0.4 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 7 / 0 / 1 · **dossier rows:** 6
- **citations (3):** [authored] maxroll.gg · @Helm Breaker · https://maxroll.gg/poe2/build-guides/minion-army-infernalist-build-guide; [authored] maxroll.gg · https://maxroll.gg/poe2/build-guides/twink-skeletal-arsonist-infernalist-leveling-guide; [communal] pathofexile.com · https://www.pathofexile.com/forum/view-thread/3644326
- **t4 doors:** `PROXY_SOVEREIGNTY`, `PROXY_ASCENSION`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Skeletal Arsonists / Summon Raging Spirits / Loyal Hellhound (persistent minion army)**: delivery=summon_delegate, cadence=cooldown, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Minion Infernalist: totem summon_delegate identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **deviations:**
  - [accepted_downgrade] Behavioral delta (R-M8-adjacent): engine totems are STATIONARY while these minions PURSUE targets across the encounter -- the roaming-army feel is delivery flavor the stationary-totem geometry cannot fully carry. · downgrade-owner `elrond (W4 PoE2 tranche; internal-consistency reconcile, no W1 evidence — W5 is PoE2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'summon_delegate'` [green]
- **mapping deviation notes:** Behavioral delta (R-M8-adjacent): engine totems are STATIONARY while these minions PURSUE targets across the encounter -- the roaming-army feel is delivery flavor the stationary-totem geometry cannot fully carry. Proxy-army identity is expressible (CLOSE); the deviation is the mobility of the proxies.

## poe2-perfect-strike-01 — Perfect Strike (launch) `[NEGATIVE, class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** fire · _raw_: fire
- **elements attested:** fire
- **ailments attested:** burn
- **eras:** 0.1 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 1 · **dossier rows:** 6
- **citations (2):** [dataset] poe2db.tw · https://poe2db.tw/us/Perfect_Strike; [communal] mmojugg.com · https://www.mmojugg.com/news/poe2-warrior-league-starter-build-perfect-strike.html
- **t4 doors:** `ELEMENT_CONVERSION_PHYSICAL`, `PERSISTENCE_ENGINE_uptime`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Perfect Strike (0.1 launch pre-nerf state)**: delivery=melee_arc, range=melee, speed=fast, cadence=channel, motion_signature=arc_sweep, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Perfect Strike (launch): melee arc melee_arc identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **deviations:**
  - [accepted_downgrade] A 0.1-launch player would 'miss' the specific pre-nerf degeneracy (always-Ignite at 45% base speed on a trivially-timed window) -- but that is a TUNING artifact, not a mappable mechanism; · downgrade-owner `elrond (W4 PoE2 tranche; internal-consistency reconcile, no W1 evidence — W5 is PoE2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'melee_arc'` [green]
- **mapping deviation notes:** A 0.1-launch player would 'miss' the specific pre-nerf degeneracy (always-Ignite at 45% base speed on a trivially-timed window) -- but that is a TUNING artifact, not a mappable mechanism; the engine has no 'trivially-timed window' anti-pattern to reproduce. The channel-charge-release fire-wave mechanism maps cleanly (CLOSE); the deviation is that the trap was balance, not a missing feature.

## poe2-poison-pathfinder — Poison Pathfinder `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** chaos-poison · _raw_: chaos
- **elements attested:** earth
- **ailments attested:** poison
- **eras:** 0.1;0.2-dawn;0.3-edict;0.4 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 8 / 0 / 0 · **dossier rows:** 6
- **citations (3):** [authored] maxroll.gg · @Crouching_Tuna · https://maxroll.gg/poe2/build-guides/poisonburst-arrow-pathfinder; [authored] odealo.com · https://odealo.com/articles/gas-arrow-pathfinder-poe2-build; [communal] mmojugg.com · https://www.mmojugg.com/news/poe2-040-build-recommendation-poisonburst-pathfinder-from-fubgun.html
- **t4 doors:** `PERSISTENCE_ENGINE_saturation`, `ZONE_CONTROL`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Poisonburst Arrow**: delivery=zone, motion_signature=ground_place, count=1 · conf 0.75
  - `#1` **Gas Arrow + Toxic Growth (boss burst combo)**: delivery=zone, motion_signature=ground_place, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Poison Pathfinder: ground targeted circle zone identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] earth element register — _expressed by_ `element:earth`
- **deviations:**
  - [accepted_downgrade] Minor drift: the Pathfinder flask-charge-on-kill engine (extra charges on kill -> near-permanent flask uptime that POWERS poison scaling) is approximated as an on_kill recovery key + flask-effect traits; · downgrade-owner `elrond (W4 PoE2 tranche; internal-consistency reconcile, no W1 evidence — W5 is PoE2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
- **mapping deviation notes:** Minor drift: the Pathfinder flask-charge-on-kill engine (extra charges on kill -> near-permanent flask uptime that POWERS poison scaling) is approximated as an on_kill recovery key + flask-effect traits; the specific flask-uptime-drives-damage coupling is softened. The one-button poison-explosion clear + place/detonate boss burst identity is preserved.

## poe2-rake-ritualist — Bleed Ritualist `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** bleed
- **eras:** 0.2-dawn;0.3-edict · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 6 / 0 / 0 · **dossier rows:** 6
- **citations (3):** [communal] akrpg.com · https://www.akrpg.com/news/910--poe-2-best-ritualist-leveling-bleed-huntress-build-in-02-dawn-of-the-hunt; [communal] pathofexile.com · https://www.pathofexile.com/forum/view-thread/3852926; [communal] mmopixel.com · https://www.mmopixel.com/news/poe-2-dawn-of-the-hunt-best-endgame-build-for-pinnacle-bosses-bleed-ritualist-build-guide
- **t4 doors:** `PERSISTENCE_ENGINE_saturation`, `MOMENTUM_CASCADE`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Rake**: delivery=motion, cadence=builder_spender, motion_signature=straight_line, count=1, chain=2 · conf 0.75
  - `#1` **Blood Hunt (single-target execution)**: delivery=melee_arc, range=melee, cadence=builder_spender, motion_signature=point_strike, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Bleed Ritualist: dash attack motion identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] Drift from the flicker precedent: dash_attack captures the delivery, but the engine has no native 'apply-then-Disengage-OUT' hit-and-run RETREAT half of the loop -- the dash is modeled as an attack-approach, the strategic dash-away (the survival core of a Ritualist Rake) is delivery flavor. · downgrade-owner `elrond (W4 PoE2 tranche; internal-consistency reconcile, no W1 evidence — W5 is PoE2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'motion'` [green]
- **mapping deviation notes:** Drift from the flicker precedent: dash_attack captures the delivery, but the engine has no native 'apply-then-Disengage-OUT' hit-and-run RETREAT half of the loop -- the dash is modeled as an attack-approach, the strategic dash-away (the survival core of a Ritualist Rake) is delivery flavor. The dash-bleed-builder + Blood Hunt execution identity is preserved.

## poe2-smith-ignite — Smith of Kitava Ignite `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** fire · _raw_: fire
- **elements attested:** fire
- **ailments attested:** burn
- **eras:** 0.2-dawn;0.3-edict;0.4;0.5-ancients · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 6 / 0 / 2 · **dossier rows:** 6
- **citations (5):** [official] maxroll.gg · https://maxroll.gg/poe2/resources/smith-of-kitava-ascendancy-overview; [authored] game8.co · https://game8.co/games/Path-of-Exile-2/archives/573471; [authored] rpgstash.com · https://www.rpgstash.com/blog/path-of-exile-2/dawn-of-the-hunt-rolling-slam-smith-of-kitava-build-guide; [communal] boostmatch.gg · https://boostmatch.gg/blog/poe-2/articles/poe2-smith-of-kitava-best-build; [communal] boostmatch.gg · https://boostmatch.gg/blog/poe-2/articles/poe2-warrior-smith-of-kitava-balrog-fire-bear-build
- **t4 doors:** `ELEMENT_CONVERSION_PHYSICAL`, `PERSISTENCE_ENGINE_saturation`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Supercharged Slam**: delivery=melee_arc, range=melee, width=wide, motion_signature=point_strike, count=1 · conf 0.75
  - `#1` **Molten Crash (fissure lines from impact)**: delivery=projectile, motion_signature=straight_line, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Smith of Kitava Ignite: ground slam melee_arc identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **deviations:**
  - [accepted_downgrade] Minor drift: Weapon Heat maps cleanly as an accumulator, but the specific 'heat is generated by CRAFTING interactions' flavor (a forge-ascendancy meta-loop OUTSIDE combat) has no engine analog -- the accumulator is fed by in-combat proxies instead. · downgrade-owner `elrond (W4 PoE2 tranche; internal-consistency reconcile, no W1 evidence — W5 is PoE2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'melee_arc'` [green]
- **mapping deviation notes:** Minor drift: Weapon Heat maps cleanly as an accumulator, but the specific 'heat is generated by CRAFTING interactions' flavor (a forge-ascendancy meta-loop OUTSIDE combat) has no engine analog -- the accumulator is fed by in-combat proxies instead. The in-combat heat->ignite-magnitude behavior and the slam-ignite identity are faithful.

## poe2-snipe-mirage-deadeye — Snipe Mirage Deadeye `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** cold · _raw_: cold
- **elements attested:** water
- **ailments attested:** freeze
- **eras:** 0.5-ancients · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 1 · **dossier rows:** 6
- **citations (3):** [authored] maxroll.gg · https://maxroll.gg/poe2/build-guides/ice-shot-deadeye-build-guide; [communal] pathofexile2.wiki.fextralife.com · https://pathofexile2.wiki.fextralife.com/Mirage+Deadeye+(Meta+Skill); [dataset] poe2db.tw · https://poe2db.tw/us/Snipe
- **t4 doors:** `GEOMETRY_COLLAPSE`, `PROXY_ASCENSION`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Snipe (channeled bow shot)**: delivery=projectile, cadence=channel, motion_signature=straight_line, count=1 · conf 0.75
  - `#1` **Ice Shot (freeze-setup projectile + shard AoE)**: delivery=projectile, motion_signature=fan_spread, count=9 · conf 0.75
  - `#2` **Mirage Deadeye (clone meta-skill)**: delivery=aura, range=self, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Snipe Mirage Deadeye: single target projectile identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] water element register — _expressed by_ `element:water`
- **deviations:**
  - [accepted_downgrade] Minor drift: the freeze->Snipe interaction is a cross-skill setup (Ice Shot freezes, Snipe cashes the frozen-target bonus) that the engine models as two independent skills + a GEOMETRY_COLLAPSE door rather than a first-class 'bonus-vs-frozen' coupling; · downgrade-owner `elrond (W4 PoE2 tranche; internal-consistency reconcile, no W1 evidence — W5 is PoE2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]
- **mapping deviation notes:** Minor drift: the freeze->Snipe interaction is a cross-skill setup (Ice Shot freezes, Snipe cashes the frozen-target bonus) that the engine models as two independent skills + a GEOMETRY_COLLAPSE door rather than a first-class 'bonus-vs-frozen' coupling; the player keeps the freeze-then-burst rhythm. Mirage Deadeye's clone-echo (repeat-my-attack) collapses to a self_buff+linked-cast trigger rather than spawned autonomous clones -- the 'my shots get doubled by ghosts' fantasy reads as a linked-cast proc. Both are recognizable-but-slightly-hollow, not identity-breaking.

## poe2-spark-stormweaver — Spark Stormweaver `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** lightning · _raw_: lightning
- **elements attested:** lightning
- **ailments attested:** sunder
- **eras:** 0.1;0.2-dawn;0.3-edict;0.4;0.5-ancients · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 0 · **dossier rows:** 6
- **citations (2):** [authored] maxroll.gg · https://maxroll.gg/poe2/build-guides/archmage-spark-stormweaver-build-guide; [authored] timesaver.gg · https://timesaver.gg/poe-2/builds/sorceress
- **t4 doors:** `RESOURCE_CONVERSION`, `GEOMETRY_PROPAGATION`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Spark (bouncing lightning projectiles)**: delivery=projectile, motion_signature=fan_spread, count=1, chain=2 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Spark Stormweaver: multi projectile projectile identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] lightning element register — _expressed by_ `element:lightning`
- **deviations:**
  - [accepted_downgrade] Minor drift: (1) poe2 shock's damage-amp identity maps to sunder, so a Stormweaver player loses the specific 'shock = more-damage-taken from a lightning ailment' flavor read (functionally preserved as sunder's damage_taken_percent, the exact PoE band). · downgrade-owner `elrond (W4 PoE2 tranche; internal-consistency reconcile, no W1 evidence — W5 is PoE2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]
- **mapping deviation notes:** Minor drift: (1) poe2 shock's damage-amp identity maps to sunder, so a Stormweaver player loses the specific 'shock = more-damage-taken from a lightning ailment' flavor read (functionally preserved as sunder's damage_taken_percent, the exact PoE band). (2) Archmage's 'my entire mana bar IS my damage number' coupling is expressed as a RESOURCE_CONVERSION door + an anti-reservation economy note rather than a bespoke mana-total->spell-damage scaler; the build's headline fantasy (stack mana, watch damage soar) is recognizable but its precise magnitude-coupling is door-level, not a first-class economy key. Kept CLOSE (not APPROX): the bouncing-projectile-flood core maps EXACT and the mana-coupling is a genuine strategy door, not an unmodelable gap.

## poe2-spiral-volley — Spiral Volley `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** 0.4;0.5-ancients · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 2 / 1 / 1 · **dossier rows:** 6
- **citations (2):** [authored] maxroll.gg · https://maxroll.gg/poe2/build-guides/spiral-volley-deadeye-build-guide; [authored] maxroll.gg · https://maxroll.gg/poe2/build-guides/spiral-volley-pathfinder-build-guide
- **t4 doors:** `TEMPORAL_CHARGE`, `GEOMETRY_PROPAGATION`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Spiral Volley (360-degree arrow burst)**: delivery=zone, range=screen, width=wide, speed=fast, motion_signature=burst_around_self, count=29, chain=2 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Spiral Volley: ring zone identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] Minor drift: the Endurance->Frenzy charge-CONVERSION (build one charge type via Armour Break, transmute it to another via a keystone, spend that on the nova) is a two-currency laundering loop the engine models as a single charge-stack cycle + consume-mark; · downgrade-owner `elrond (W4 PoE2 tranche; internal-consistency reconcile, no W1 evidence — W5 is PoE2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
- **mapping deviation notes:** Minor drift: the Endurance->Frenzy charge-CONVERSION (build one charge type via Armour Break, transmute it to another via a keystone, spend that on the nova) is a two-currency laundering loop the engine models as a single charge-stack cycle + consume-mark; the player keeps the bank-then-dump burst rhythm but loses the specific 'wrong-charge-into-right-charge' conversion identity. The ring+6x-chain coverage maps cleanly. Kept CLOSE.

## poe2-supporting-fire — Supporting Fire Tactician `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** 0.2-dawn;0.3-edict;0.4;0.5-ancients · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 1 · **dossier rows:** 6
- **citations (1):** [authored] maxroll.gg · https://maxroll.gg/poe2/build-guides/supporting-fire-tactician-build-guide
- **t4 doors:** `ZONE_CONTROL`, `PROXY_SOVEREIGNTY`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Supporting Fire (commanded arrow volley)**: delivery=zone, motion_signature=ground_place, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Supporting Fire Tactician: ground targeted circle zone identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] Minor drift: the kit's minion-mediated delivery (minions physically loose the arrows on command) is compressed into a player-cast ground_targeted_circle with a PROXY_SOVEREIGNTY door -- the player keeps the 'designate zone, arrows rain' loop but loses the visible 'my squad fires on my command' proxy texture. · downgrade-owner `elrond (W4 PoE2 tranche; internal-consistency reconcile, no W1 evidence — W5 is PoE2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
- **mapping deviation notes:** Minor drift: the kit's minion-mediated delivery (minions physically loose the arrows on command) is compressed into a player-cast ground_targeted_circle with a PROXY_SOVEREIGNTY door -- the player keeps the 'designate zone, arrows rain' loop but loses the visible 'my squad fires on my command' proxy texture. The banner/squad-tactics fantasy (corpus mech_note) is thinner than a true commanded-proxy system would render it, but the every-3-seconds ACTION (place a 14m volley) maps cleanly. Kept CLOSE.

## poe2-tempest-bell — Tempest Bell Monk `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** lightning · _raw_: lightning
- **elements attested:** lightning
- **ailments attested:** sunder
- **eras:** 0.1;0.2-dawn;0.3-edict;0.4;0.5-ancients · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 0 · **dossier rows:** 6
- **citations (2):** [authored] maxroll.gg · https://maxroll.gg/poe2/build-guides/tempest-flurry-invoker; [authored] switchbladegaming.com · https://www.switchbladegaming.com/path-of-exile-2/monk-best-build/
- **t4 doors:** `PROXY_ASCENSION`, `TEMPORAL_CHARGE`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Tempest Flurry (combo-point builder + bell striker)**: delivery=melee_arc, range=melee, cadence=builder_spender, motion_signature=arc_sweep, count=1 · conf 0.75
  - `#1` **Tempest Bell (placed pulsing proxy)**: delivery=summon_delegate, cadence=cooldown, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Tempest Bell Monk: melee arc melee_arc identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] lightning element register — _expressed by_ `element:lightning`
- **deviations:**
  - [accepted_downgrade] Minor drift: Tempest Bell's defining texture -- a placed proxy that does nothing on its own and only pulses WHEN YOUR OWN MELEE HITS IT -- collapses into a totem (placed proxy) whose proc is expressed via trigger_grammar (on-hit-threshold -> resource-fill/pulse). · downgrade-owner `elrond (W4 PoE2 tranche; internal-consistency reconcile, no W1 evidence — W5 is PoE2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'melee_arc'` [green]
- **mapping deviation notes:** Minor drift: Tempest Bell's defining texture -- a placed proxy that does nothing on its own and only pulses WHEN YOUR OWN MELEE HITS IT -- collapses into a totem (placed proxy) whose proc is expressed via trigger_grammar (on-hit-threshold -> resource-fill/pulse). The engine's totem is more autonomous than the bell's 'you must ring it yourself' dependency, so the player's 'I attack my own bell to weaponize it' loop reads as a more self-sufficient sentry. The dual-currency (Combo Points to summon + Power Charges to Falling-Thunder) is modeled as one accumulator + a charge bank. Recognizable, slightly-hollowed proxy identity -> CLOSE.

## poe2-tempest-flurry — Tempest Flurry Monk `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** lightning · _raw_: lightning
- **elements attested:** lightning
- **ailments attested:** sunder
- **eras:** 0.1;0.2-dawn;0.5-ancients · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 1 · **dossier rows:** 6
- **citations (2):** [authored] maxroll.gg · https://maxroll.gg/poe2/build-guides/tempest-flurry-invoker; [authored] switchbladegaming.com · https://www.switchbladegaming.com/path-of-exile-2/monk-best-build/
- **t4 doors:** `TEMPORAL_CHARGE`, `MOMENTUM_CASCADE`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Tempest Flurry (rhythm quarterstaff flurry)**: delivery=melee_arc, range=melee, speed=fast, motion_signature=arc_sweep, count=1 · conf 0.75
  - `#1` **Charged Staff (Power-Charge-spend buff + lightning finisher)**: delivery=aura, range=self, cadence=builder_spender, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Tempest Flurry Monk: melee arc melee_arc identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] lightning element register — _expressed by_ `element:lightning`
- **deviations:**
  - [accepted_downgrade] Minor drift: the 4-hit RHYTHM cadence (each hit in the combo escalates, the 4th erupts) is the flurry's signature feel, and while melee_arc + a MOMENTUM_CASCADE door capture 'ramping repeated swings culminating in a burst', the engine has no first-class '4th-hit-of-a-fixed-combo erupts' beat -- the eruption reads as a generic finisher rather than a metered rhythm payoff. · downgrade-owner `elrond (W4 PoE2 tranche; internal-consistency reconcile, no W1 evidence — W5 is PoE2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'melee_arc'` [green]
- **mapping deviation notes:** Minor drift: the 4-hit RHYTHM cadence (each hit in the combo escalates, the 4th erupts) is the flurry's signature feel, and while melee_arc + a MOMENTUM_CASCADE door capture 'ramping repeated swings culminating in a burst', the engine has no first-class '4th-hit-of-a-fixed-combo erupts' beat -- the eruption reads as a generic finisher rather than a metered rhythm payoff. The dual Combo/Power-Charge currencies compress to one accumulator. The core melee-flurry-into-lightning-burst maps cleanly -> CLOSE.

## poe2-titan-hotg — Hammer of the Gods Titan `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** stun,sunder
- **eras:** 0.1;0.2-dawn;0.3-edict · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 1 · **dossier rows:** 6
- **citations (1):** [authored] maxroll.gg · https://maxroll.gg/poe2/build-guides/hammer-of-the-gods-titan-build-guide
- **t4 doors:** `GEOMETRY_COLLAPSE`, `SACRIFICE_ASCENDANCY`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Hammer of the Gods (colossal falling-hammer slam)**: delivery=melee_arc, range=melee, motion_signature=point_strike, count=1 · conf 0.75
  - `#1` **Armour Breaker / warcry setup (armor-shred prerequisite)**: delivery=melee_arc, range=melee, motion_signature=arc_sweep, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Hammer of the Gods Titan: ground slam melee_arc identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] Minor drift: HotG's identity is a SETUP-GATED single nuke -- its full damage REQUIRES a fully-broken-armor + heavy-stunned target, a cross-skill prerequisite chain (Armour Breaker + Earthshatter + warcries -> then Hammer). · downgrade-owner `elrond (W4 PoE2 tranche; internal-consistency reconcile, no W1 evidence — W5 is PoE2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'melee_arc'` [green]
- **mapping deviation notes:** Minor drift: HotG's identity is a SETUP-GATED single nuke -- its full damage REQUIRES a fully-broken-armor + heavy-stunned target, a cross-skill prerequisite chain (Armour Breaker + Earthshatter + warcries -> then Hammer). The engine maps the pieces (ground_slam + sunder + stun + a GEOMETRY_COLLAPSE door) but expresses the 'HotG deals MORE into broken armor' coupling as a generic burst rather than a first-class conditional-damage gate; the player keeps the slow-wind-up-into-massive-slam feel and the break-then-hammer sequence, but the precise 'broken-armor multiplier' is door/trait-level. The colossal-slam core maps cleanly -> CLOSE.

## poe2-warbringer-totems — Ancestral Totem Warrior `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** 0.2-dawn;0.3-edict;0.4;0.5-ancients · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 2 / 1 / 2 · **dossier rows:** 6
- **citations (2):** [authored] maxroll.gg · https://maxroll.gg/poe2/build-guides/shockwave-totem-warbringer-leveling-guide; [dataset] poe2db.tw · https://poe2db.tw/us/Ancestral_Warrior_Totem
- **t4 doors:** `PROXY_SOVEREIGNTY`, `PROXY_FISSION`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Ancestral Warrior Totem (spirit-warrior slam proxy)**: delivery=summon_delegate, cadence=cooldown, count=10 · conf 0.75
  - `#1` **Shockwave Totem (secondary placed slam proxy)**: delivery=summon_delegate, cadence=cooldown, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Ancestral Totem Warrior: totem summon_delegate identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] Minor drift: (1) the ENDURANCE-CHARGE-FUELED totem economy -- each totem COSTS 3 Endurance Charges to raise, coupling a defensive charge type to proxy deployment -- is expressed as an accumulator spend + a placed-proxy-count note rather than a first-class 'charges-buy-proxies' key; · downgrade-owner `elrond (W4 PoE2 tranche; internal-consistency reconcile, no W1 evidence — W5 is PoE2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'summon_delegate'` [green]
- **mapping deviation notes:** Minor drift: (1) the ENDURANCE-CHARGE-FUELED totem economy -- each totem COSTS 3 Endurance Charges to raise, coupling a defensive charge type to proxy deployment -- is expressed as an accumulator spend + a placed-proxy-count note rather than a first-class 'charges-buy-proxies' key; the player keeps the drop-totems-and-wait loop. (2) the up-to-10-simultaneous-totem swarm is a placed-proxy-COUNT extremum (accrual candidate to the placed-proxy-count family) that PROXY_FISSION approximates. (3) Wooden Wall's 'redirect my incoming damage TO my totems' proxy-tanking is noted but not first-class. The heavy-proxy identity (totems do all the work, Warrior tanks) maps cleanly via PROXY_SOVEREIGNTY -> CLOSE (recognizable, minor economy/count compression).

## poe2-whirling-assault-ma — Whirling Assault Martial Artist `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** 0.5-ancients · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 0 · **dossier rows:** 6
- **citations (2):** [authored] maxroll.gg · @Manni · https://maxroll.gg/poe2/build-guides/hollow-form-whirling-assault-martial-artist-build-guide; [authored] maxroll.gg · https://maxroll.gg/poe2/build-guides/whirling-assault-martial-artist-build-guide
- **t4 doors:** `MOMENTUM_CASCADE`, `TEMPORAL_CHARGE`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Whirling Assault (Hollow Form clone-cast)**: delivery=motion, range=melee, cadence=channel, motion_signature=orbit_fixed, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Whirling Assault Martial Artist: whirlwind motion identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] A Hollow Form MA player gets a faithful spin-AoE with a charge-fueled proxy loop, but the CLONE MULTIPLICITY (multiple images each spinning simultaneously = output-multiplication by clone count) is softened: the engine models one whirlwind geometry + a linked-cast trigger, so the 'my clones spin for me and I just tap the button' identity lands as a single spin with a charge-accumulator feed rather · downgrade-owner `elrond (W4 PoE2 tranche; internal-consistency reconcile, no W1 evidence — W5 is PoE2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'motion'` [green]
- **mapping deviation notes:** A Hollow Form MA player gets a faithful spin-AoE with a charge-fueled proxy loop, but the CLONE MULTIPLICITY (multiple images each spinning simultaneously = output-multiplication by clone count) is softened: the engine models one whirlwind geometry + a linked-cast trigger, so the 'my clones spin for me and I just tap the button' identity lands as a single spin with a charge-accumulator feed rather than N parallel spinning bodies. That build, worse (R-M7) -> CLOSE; playable, the clone-count damage-multiplier is the fidelity loss noted.

## poe2-witchhunter-grenades — Grenadier Witchhunter `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** fire · _raw_: fire
- **elements attested:** fire
- **ailments attested:** stun,sunder
- **eras:** 0.1;0.2-dawn;0.3-edict;0.4;0.5-ancients · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 0 · **dossier rows:** 6
- **citations (3):** [authored] maxroll.gg · @Crouching_Tuna · https://maxroll.gg/poe2/build-guides/oil-grenade-witchhunter-build-guide; [communal] pathofexile.com/forum · https://www.pathofexile.com/forum/view-thread/3859536; [authored] maxroll.gg · https://maxroll.gg/poe2/build-guides/grenade-mercenary-leveling-guide
- **t4 doors:** `ZONE_CONTROL`, `GEOMETRY_COLLAPSE`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Explosive Grenade**: delivery=zone, width=wide, motion_signature=ground_place, count=1 · conf 0.75
  - `#1` **Oil Grenade**: delivery=zone, cadence=spam, motion_signature=ground_place, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Grenadier Witchhunter: ground targeted circle zone identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **deviations:**
  - [accepted_downgrade] A grenade Witchhunter gets the kill-zone loop faithfully -- lob, pre-stack, detonate -- via ground_targeted_circle + ammo economy + burst-damage trigger. · downgrade-owner `elrond (W4 PoE2 tranche; internal-consistency reconcile, no W1 evidence — W5 is PoE2's external check)`
  - [accepted_downgrade] Minor drift: the FUSE-TIMING skill expression (grenades that sit and burn down before exploding, rewarding pre-placement) is carried as a burst-damage linked-cast rather than a first-class delayed-detonation timer; · downgrade-owner `elrond (W4 PoE2 tranche; internal-consistency reconcile, no W1 evidence — W5 is PoE2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
- **mapping deviation notes:** A grenade Witchhunter gets the kill-zone loop faithfully -- lob, pre-stack, detonate -- via ground_targeted_circle + ammo economy + burst-damage trigger. Minor drift: the FUSE-TIMING skill expression (grenades that sit and burn down before exploding, rewarding pre-placement) is carried as a burst-damage linked-cast rather than a first-class delayed-detonation timer; the engine has no native fuse-delay primitive, so 'time your throws so they all pop together' is approximated. That build, worse -> CLOSE, playable.

## poe2-acolyte-darkness — Darkness Acolyte `[class:record]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** chaos-poison · _raw_: chaos
- **elements attested:** shadow
- **ailments attested:** _(none)_
- **eras:** 0.3-edict;0.4;0.5-ancients · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 1 / 1 / 2 · **dossier rows:** 6
- **citations (2):** [communal] maxroll.gg · https://maxroll.gg/poe2/resources/acolyte-of-chayula-ascendancy; [dataset] poe2db.tw · https://poe2db.tw/us/Into_the_Breach
- **t4 doors:** `RESOURCE_CONVERSION`, `SACRIFICE_ASCENDANCY`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Into the Breach chaos-converted strikes**: delivery=melee_arc, range=melee, motion_signature=arc_sweep, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Darkness Acolyte: melee arc melee_arc identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] shadow element register — _expressed by_ `element:shadow`
- **deviations:**
  - [accepted_downgrade] The source player would miss the Waking Dream Remnant economy as its OWN resource (a color-streamed pickup meter, made mono-color by Lucid Dreaming) -- we render it as reservation-swap + on-kill fill, losing the pickup-stream texture and the purple-damage-stack ramp. · downgrade-owner `elrond (W4 PoE2 tranche; internal-consistency reconcile, no W1 evidence — W5 is PoE2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'melee_arc'` [green]
- **mapping deviation notes:** The source player would miss the Waking Dream Remnant economy as its OWN resource (a color-streamed pickup meter, made mono-color by Lucid Dreaming) -- we render it as reservation-swap + on-kill fill, losing the pickup-stream texture and the purple-damage-stack ramp. Also the darkness-absorb defensive window (Embrace the Darkness) is folded into a T4 door, not modeled as an active mitigation buff. That build, worse -- not a different build -- so APPROX not GAPPED.

## poe2-archmage-totems — Archmage Totems Oracle `[class:record]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** lightning · _raw_: lightning
- **elements attested:** lightning
- **ailments attested:** _(none)_
- **eras:** 0.5-ancients · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 1 · **dossier rows:** 6
- **citations (4):** [communal] maxroll.gg · https://maxroll.gg/poe2/build-guides/grim-pillars-spell-totem-oracle-build-guide; [dataset] poe.ninja · https://poe.ninja/poe2/builds/runesofaldur?class=Oracle&skills=Spell+Totem; [dataset] poe.ninja · https://poe.ninja/poe2/builds/runesofaldur?class=Oracle&skills=Spark; [communal] maxroll.gg · https://maxroll.gg/poe2/build-guides/archmage-spark-stormweaver-build-guide
- **t4 doors:** `PROXY_ASCENSION`, `NETWORK_AMPLIFIER`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Spark (cast by Spell Totem)**: delivery=summon_delegate, cadence=cooldown, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Archmage Totems Oracle: totem summon_delegate identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] lightning element register — _expressed by_ `element:lightning`
- **deviations:**
  - [engine_inexpressible] The source player would miss that this is a mana-STACKING archmage build where max-mana IS the damage stat funneled THROUGH totems -- we express the totem proxy cleanly but the mana-as-weapon coupling degrades to a cost_scale note (no native key couples max-mana-pool to spell damage). → _fix_ `new_door_rfc`
- **acceptance asserts:**
  - `primary_delivery_class == 'summon_delegate'` [green]
  - `expresses: The source player would miss that this is a mana-STACKING archmage build where m` [red] · expected: RED until engine lane exists (routed to docket)
- **mapping deviation notes:** The source player would miss that this is a mana-STACKING archmage build where max-mana IS the damage stat funneled THROUGH totems -- we express the totem proxy cleanly but the mana-as-weapon coupling degrades to a cost_scale note (no native key couples max-mana-pool to spell damage). Joint attestation weakness means the specific Oracle+Archmage+Totem synergy is not source-confirmed as one loop; if that synergy proves phantom the kit collapses toward a plain totem-Spark build. Because a plausible weaker version of that build survives, APPROX.

## poe2-chronomancer-01 — Chronomancer (launch) `[NEGATIVE, class:record]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** cold · _raw_: cold
- **elements attested:** _(silent)_
- **ailments attested:** stun
- **eras:** 0.1;0.2-dawn;0.3-edict;0.4 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 1 · **dossier rows:** 6
- **citations (3):** [communal] maxroll.gg · https://maxroll.gg/poe2/resources/chronomancer-ascendancy; [dataset] poe2db.tw · https://poe2db.tw/us/Time_Freeze; [communal] pathofexile.com · https://www.pathofexile.com/forum/view-thread/3643825
- **t4 doors:** `TEMPORAL_CHARGE`, `ZONE_CONTROL`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Time Freeze**: delivery=zone, motion_signature=burst_around_self, count=1 · conf 0.75
  - `#1` **Time Snap**: delivery=aura, range=self, cadence=cooldown, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Chronomancer (launch): ring zone identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [engine_inexpressible] The source player would miss (1) that the CC is literal TIME-STOP -- enemies frozen mid-animation, not stunned-and-recovering -- our stun approximation loses the total-action-denial texture that made it boss-trivializing (and negative); → _fix_ `new_door_rfc`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
  - `expresses: The source player would miss (1) that the CC is literal TIME-STOP -- enemies fro` [red] · expected: RED until engine lane exists (routed to docket)
- **mapping deviation notes:** The source player would miss (1) that the CC is literal TIME-STOP -- enemies frozen mid-animation, not stunned-and-recovering -- our stun approximation loses the total-action-denial texture that made it boss-trivializing (and negative); (2) the cooldown-RESET engine (Time Snap) as a first-class mechanic -- no native key resets cooldowns, so the signature back-to-back-stasis loop degrades to a cadence note + docket. Both are IDENTITY-level losses -> APPROX bordering GAPPED; kept APPROX because a duration-capped mass-stun controller is recognizably 'that build, weaker.'

## poe2-demon-form — Demon Form Infernalist `[class:record]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** fire · _raw_: fire
- **elements attested:** fire
- **ailments attested:** burn
- **eras:** 0.1;0.2-dawn;0.4 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 2 / 0 / 2 · **dossier rows:** 6
- **citations (3):** [communal] maxroll.gg · https://maxroll.gg/poe2/resources/infernalist-ascendancy; [communal] pathofexile.com · @wishdropper#0634 · https://www.pathofexile.com/forum/view-thread/3656716; [communal] pathofexile.com · https://www.pathofexile.com/forum/view-thread/3643314
- **t4 doors:** `SACRIFICE_ASCENDANCY`, `PHASE_MOMENTUM`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **in-form spell (Spark-attested; fire per corpus)**: delivery=aura, range=self, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Demon Form Infernalist: self buff aura identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **deviations:**
  - [engine_inexpressible] The source player would miss (1) the FORM-SWAP itself as a distinct game-state (you BECOME a demon -- a body/moveset change, GX-02) -- rendered as a self_buff it loses the transformation identity; → _fix_ `new_door_rfc`
- **acceptance asserts:**
  - `primary_delivery_class == 'aura'` [green]
  - `expresses: The source player would miss (1) the FORM-SWAP itself as a distinct game-state (` [red] · expected: RED until engine lane exists (routed to docket)
- **mapping deviation notes:** The source player would miss (1) the FORM-SWAP itself as a distinct game-state (you BECOME a demon -- a body/moveset change, GX-02) -- rendered as a self_buff it loses the transformation identity; (2) the unbounded Demonflame life-drain ramp -- clamped to hp_cost_scale 0.30, the escalating 'race your own life-loss' tension is capped, losing the run-it-till-you-die brinkmanship; (3) element ambiguity (fire per corpus vs lightning/Spark per attested builds). Form-swap has no engine lane (GX-02 pending) and the drain-ramp is clamped -> APPROX; not GAPPED because a fire-spell self-buff caster with a decaying-HP cost is 'that build, weaker.'

## poe2-gemling-stacker — Gemling Attribute Stacker `[class:record]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** lightning · _raw_: lightning
- **elements attested:** lightning,water
- **ailments attested:** freeze
- **eras:** 0.1;0.2-dawn;0.3-edict;0.4;0.5-ancients · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 1 · **dossier rows:** 6
- **citations (3):** [communal] maxroll.gg · @Void241 · https://maxroll.gg/poe2/build-guides/tempest-flurry-gemling-legionnaire-build-guide; [communal] pathofexile.com · https://www.pathofexile.com/forum/view-thread/3670962; [communal] maxroll.gg · https://maxroll.gg/poe2/resources/gemling-legionnaire-ascendancy
- **t4 doors:** `RESOURCE_CONVERSION`, `GEOMETRY_PROPAGATION`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Tempest Flurry (HoWA attribute-stacked)**: delivery=melee_arc, range=melee, width=wide, speed=fast, motion_signature=arc_sweep, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Gemling Attribute Stacker: melee arc melee_arc identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] lightning element register — _expressed by_ `element:lightning`
- **deviations:**
  - [engine_inexpressible] The source player would miss the ENTIRE identity engine: attribute-stacking-AS-damage. → _fix_ `new_door_rfc`
- **acceptance asserts:**
  - `primary_delivery_class == 'melee_arc'` [green]
  - `expresses: The source player would miss the ENTIRE identity engine: attribute-stacking-AS-d` [red] · expected: RED until engine lane exists (routed to docket)
- **mapping deviation notes:** The source player would miss the ENTIRE identity engine: attribute-stacking-AS-damage. In PoE2 you pour 600+ STR / 300 DEX / 300-500 INT and Enhanced Effectiveness DOUBLES it, then Pillar + HoWA convert those raw stats into your whole damage output -- the build IS the stat-stack. The engine has no lane that couples attribute TOTALS to flat attack damage (docket #8 is the adjacent-but-distinct stat->proxy-count), so this degrades to trait/affix scaler notes + a RESOURCE_CONVERSION door + a docket-candidate. What survives (a lightning/cold melee attacker with freeze-shatter) is recognizable but hollow of the stacker fantasy -> APPROX (that build, much weaker), bordering GAPPED; kept APPROX because the melee-attack shell maps and the stat-coupling is a docket-able quantitative gap, not a wholly unmodelable mechanism.

## poe2-grim-feast — Grim Feast Overleech `[is_system, class:system]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** _(unassigned)_ · _raw_: n/a
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** 0.2-dawn · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 3 / 2 / 0 · **dossier rows:** 6
- **citations (3):** [dataset] poe2db.tw · https://poe2db.tw/us/Grim_Feast; [authored] maxroll.gg · https://maxroll.gg/poe2/build-guides/explosive-shot-deadeye-build-guide; [authored] maxroll.gg · https://maxroll.gg/poe2/build-guides/shattering-palm-invoker-build-guide
- **t4 doors:** `DEFENSIVE_TRADEOFF`, `PERSISTENCE_ENGINE_uptime`
- **mapping deviation notes:** An ES-overleech (0.2-dawn) player would get a worse version: the engine expresses the on-kill life-remnant INTAKE (recovery keys) but NOT the ABOVE-MAX overflow buffer that IS the durability identity -- ES tops off toward the cap instead of overflowing to 2x. 'That build, worse' (R-M7) -> APPROX, kit stays MAPPED (playable worse-version); the above-cap MECHANISM gap is carried in the docket-candidate for steward consolidation.

## poe2-shaman-bear — Shaman Bear `[class:record]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** fire
- **ailments attested:** burn,stun
- **eras:** 0.4;0.5-ancients · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 6 / 0 / 0 · **dossier rows:** 6
- **citations (3):** [authored] maxroll.gg · @Palsteron · https://maxroll.gg/poe2/build-guides/demon-calamity-bear-shaman-build-guide; [authored] odealo.com · https://odealo.com/articles/bear-form-shaman-poe2-build; [communal] overgear.com · https://overgear.com/guides/poe-2/shaman-bear-druid/
- **t4 doors:** `MOMENTUM_CASCADE`, `PHASE_MOMENTUM`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Maul / Furious Slam (Bear Form heavy slams)**: delivery=melee_arc, range=melee, motion_signature=point_strike, count=1 · conf 0.75
  - `#1` **Walking Calamity (Glory-triggered passive meteors)**: delivery=zone, cadence=builder_spender, motion_signature=ground_place, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Shaman Bear: ground slam melee_arc identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **deviations:**
  - [accepted_downgrade] A Shaman-Bear player would MISS the distinct two-tier economy: Rage OVERFLOW (past max) FEEDING a SEPARATE Glory meter that gates Walking Calamity. · downgrade-owner `elrond (W4 PoE2 tranche; internal-consistency reconcile, no W1 evidence — W5 is PoE2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'melee_arc'` [green]
- **mapping deviation notes:** A Shaman-Bear player would MISS the distinct two-tier economy: Rage OVERFLOW (past max) FEEDING a SEPARATE Glory meter that gates Walking Calamity. The single-accumulator + threshold-proc model collapses the two meters into one, so the 'fill Rage, then watch it spill into Glory, then Glory caps and meteors erupt' rhythm reads as a plain charge-then-proc. The compressed second tier is the deviation (a WATCH-ITEM accrual for steward mint review).

## poe2-temporalis-blink — Temporalis Blink `[is_system, class:system]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** _(unassigned)_ · _raw_: n/a
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** 0.1;0.2-dawn · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 0 · **dossier rows:** 6
- **citations (2):** [communal] pathofexile.com · https://www.pathofexile.com/forum/view-thread/3696262/page/2; [authored] mobalytics.gg · @jungroan · https://mobalytics.gg/poe-2/builds/blink-autobomber-jungroan
- **t4 doors:** `PHASE_MOMENTUM`, `TEMPORAL_CHARGE`
- **mapping deviation notes:** The Temporalis Blink player would MISS the build's entire reason to exist: a UNIQUE-ITEM-driven cooldown COLLAPSE that turns a 3-second-cooldown utility blink into a ~10-cast-per-second continuous-teleport engine, which is then weaponized by linking Cast-on-Critical bomb chains to the blink frequency. The engine maps Blink as a `blink` utility geometry + a cooldown-recovery economy note + a PHASE_MOMENTUM door, but has no first-class 'ALL cooldowns approach zero' item-warp -- the ~10x/s teleport-spam that defines the kit degrades to 'a fast-cooldown blink'. The linked-CoC-autobomber payoff (the actual damage) lives one MAX_CHAIN_DEPTH=1 hop away and can't chain deeper. What survives (a highly mobile blink build) is recognizable but hollow of the cooldown-collapse fantasy -> APPROX (that build, much weaker/slower), bordering GAPPED; kept APPROX because Blink-as-utility maps and the cooldown-collapse is a quantitative economy gap (recovery-rate extremum), not a wholly unmodelable mechanism.

## poe2-twister — Twister Spirit Walker `[class:record]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** blind
- **eras:** 0.2-dawn;0.3-edict;0.4;0.5-ancients · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 1 · **dossier rows:** 6
- **citations (2):** [authored] maxroll.gg · https://maxroll.gg/poe2/build-guides/spirit-walker-twisters; [dataset] poe2db.tw · https://poe2db.tw/us/Twister
- **t4 doors:** `GEOMETRY_PROPAGATION`, `ZONE_CONTROL`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Twister (wandering vortex projectiles)**: delivery=projectile, motion_signature=fan_spread, count=1 · conf 0.75
  - `#1` **Whirling Slash (stationary empower-zone)**: delivery=motion, range=melee, cadence=channel, motion_signature=orbit_fixed, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Twister Spirit Walker: multi projectile projectile identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] A Twister player would miss the kit's signature geometry: SELF-PROPELLED vortices that WANDER erratically across the room at 7.5m/s for 3 seconds, blinding and grinding everything they pass through, spawned in bunches by consuming a stationary whirlwind you must cast from inside. · downgrade-owner `elrond (W4 PoE2 tranche; internal-consistency reconcile, no W1 evidence — W5 is PoE2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]
- **mapping deviation notes:** A Twister player would miss the kit's signature geometry: SELF-PROPELLED vortices that WANDER erratically across the room at 7.5m/s for 3 seconds, blinding and grinding everything they pass through, spawned in bunches by consuming a stationary whirlwind you must cast from inside. The engine's multi_projectile + an R-M8 wander-note + a GEOMETRY_PROPAGATION door approximate 'many moving hits that spread', but there is no first-class 'autonomous roaming persistent AoE that pathfinds forward' member -- the erratic-wander identity (the whole reason the build feels alive) degrades to a projectile spread with a mobility note, and the 'cast-from-inside-the-whirlwind-or-lose-the-buff' positional dance compresses to an activation-toggle. What survives (a physical caster laying down multi-hit blinding area) is recognizable but hollow of the wandering-tornado fantasy -> APPROX (that build, meaningfully flatter); the roaming behavior is a documented R-M8 delta + a qualitative candidate for steward review (roaming-persistent-AoE class), not a wholly unmodelable loop, so APPROX not GAPPED.

## poe2-walking-calamity — Walking Calamity Shaman `[class:record]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** fire · _raw_: fire
- **elements attested:** fire,water
- **ailments attested:** _(none)_
- **eras:** 0.5-ancients · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 2 / 0 · **dossier rows:** 6
- **citations (2):** [authored] maxroll.gg · https://maxroll.gg/poe2/build-guides/walking-calamity-shaman-build-guide; [dataset] poe2db.tw · https://poe2db.tw/us/Walking_Calamity
- **t4 doors:** `GEOMETRY_PROPAGATION`, `MOMENTUM_CASCADE`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Walking Calamity (Glory-activated meteor rain)**: delivery=zone, motion_signature=ground_place, count=1 · conf 0.75
  - `#1` **Herald of Ice + Polcirkeln (on-freeze/on-kill propagation)**: delivery=zone, motion_signature=burst_around_self, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Walking Calamity Shaman: ground targeted circle zone identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **deviations:**
  - [accepted_downgrade] A Walking Calamity Shaman player would miss TWO things: (1) the two-tier Rage->Glory economy -- Rage OVERFLOW at max feeds a SEPARATE Glory meter that, at cap, ACTIVATES the meteor storm; · downgrade-owner `elrond (W4 PoE2 tranche; internal-consistency reconcile, no W1 evidence — W5 is PoE2's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
- **numerics:**
  - `more_frequent_200` = 200.0 (poe2_more_frequent)
- **mapping deviation notes:** A Walking Calamity Shaman player would miss TWO things: (1) the two-tier Rage->Glory economy -- Rage OVERFLOW at max feeds a SEPARATE Glory meter that, at cap, ACTIVATES the meteor storm; collapsed to one accumulator + threshold-proc, the 'fill Rage, spill into Glory, Glory caps and the sky falls' rhythm reads as a plain charge-then-proc (same WATCH-ITEM deviation as b02 shaman-bear). (2) the ENEMY-COUNT frequency scaling -- meteor cadence ramps up to 200% MORE frequent the more enemies surround you, a density-reactive output curve the engine's ground_targeted_circle + GEOMETRY_PROPAGATION door approximate as generic on-kill cascade rather than a first-class 'more targets -> faster meteors' coupling. The core (a fire meteor-field autobomber that propagates kills via Herald of Ice) maps recognizably, but the two-tier accrual + density-scaling are the deviations -> APPROX (that build, flatter economy + no density ramp); both are steward candidates, not unmodelable, so APPROX not GAPPED.

## poe2-wall-of-shields — Wall of Shields `[NEGATIVE, class:record]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** 0.3-edict;0.4 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 6 / 0 / 0 · **dossier rows:** 6
- **citations (3):** [authored] maxroll.gg · https://maxroll.gg/poe2/build-guides/shield-wall-warbringer-build-guide; [dataset] poe2db.tw · https://poe2db.tw/us/Shield_Wall; [authored] odealo.com · https://odealo.com/articles/shield-wall-warbringer-poe2-build
- **t4 doors:** `ZONE_CONTROL`, `GEOMETRY_COLLAPSE`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Shield Wall (placed detonate-able fissure wall)**: delivery=zone, range=screen, cadence=cooldown, motion_signature=lane_place, count=1 · conf 0.75
  - `#1` **Warcry / Slam detonators (Fortifying Cry, Infernal Cry, Shield Charge)**: delivery=aura, range=self, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Wall of Shields: placed lane zone identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [engine_inexpressible] A Shield Wall player would miss two coupled identities: (1) DAMAGE-FROM-SHIELD-ARMOUR -- your entire DPS is a function of your shield's raw Armour stat ('Armour on shield equals DPS'), a defensive-stat-as-offensive-source coupling the engine has no native key for (docket-candidate; → _fix_ `new_door_rfc`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
  - `expresses: A Shield Wall player would miss two coupled identities: (1) DAMAGE-FROM-SHIELD-A` [red] · expected: RED until engine lane exists (routed to docket)
- **mapping deviation notes:** A Shield Wall player would miss two coupled identities: (1) DAMAGE-FROM-SHIELD-ARMOUR -- your entire DPS is a function of your shield's raw Armour stat ('Armour on shield equals DPS'), a defensive-stat-as-offensive-source coupling the engine has no native key for (docket-candidate; distinct from tq2 armor-CONVERSION and docket #4 stun-as-damage). (2) the PLACE-then-DETONATE two-beat -- the wall is completely inert damage until a SEPARATE warcry/slam shatters it, so the loop is 'lay segments, then trigger them', mapped as placed_lane + a consume-mark detonation trigger; the engine's placed geometries are more self-sufficient, so the 'my wall does nothing until I blow it up' dependency reads thinner. What survives (a placed physical-AoE barrier detonated by warcries) is recognizable but hollow of the armour-scaling engine -> APPROX (that build, missing its damage source). NOTE: this is a corpus-flagged NEGATIVE/dead build; the APPROX grade reflects HONEST mapping of a weak kit, not an endorsement -- its non-viability is a corpus fact, not a mapping judgment.

