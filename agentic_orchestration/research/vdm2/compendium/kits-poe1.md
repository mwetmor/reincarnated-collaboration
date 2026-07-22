# VDM-2 Compendium — poe1 (94 kits)

> **Source:** `corpus.db` `kit_master` view (574) ENRICHED live with the six VDM-2 side-car blocks + two registries (render-layer joins; DB never mutated). **v2.0** · db md5 `bebc933b0bf9bcab5988bbc16bcc55b4` · generated 2026-07-22T09:46:42Z.
> `court` is the reconciled element court (enum-checked); `original_element` carries raw provenance. Raw mobile-era descriptors (`elem_raw`) are NOT exposed (provenance-only). `kit_citations` is the sole citation authority.

| grade | n | verify (C/X/U) | dossier | cited | geom-bands | hooks |
|---|---|---|---|---|---|---|
| E 2 · C 62 · A 22 · G 8 | 94 | 412/16/64 | 564 | 94/94 | 136 | 159 |

## poe1-cleave — Cleave `[NEGATIVE, class:record]`

- **grade / terminal:** `EXACT` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** bleed
- **eras:** 1.x;2.x;3.0-3.6;3.7-3.13 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 1 · **dossier rows:** 6
- **citations (2):** [official] poedb.tw · https://poedb.tw/us/Cleave; [authored] pathofexile.com/forum · @IsneakyI · https://www.pathofexile.com/forum/view-thread/2910707
- **t4 doors:** `GEOMETRY_COLLAPSE`, `ZONE_CONTROL`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Cleave**: delivery=melee_arc, range=melee, width=wide, motion_signature=arc_sweep, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Cleave: melee arc melee_arc identity — _expressed by_ `geometry.delivery_class`
- **acceptance asserts:**
  - `primary_delivery_class == 'melee_arc'` [green]

## poe1-cyclone — Cyclone `[class:record]`

- **grade / terminal:** `EXACT` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** 2.x;3.0-3.6;3.7-3.13;3.20+ · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 0 · **dossier rows:** 6
- **citations (3):** [authored] overgear.com · @Nurseos · https://overgear.com/guides/poe/cyclone-slayer-build-guide/; [authored] poe-vault.com · https://www.poe-vault.com/guides/ultimate-cyclone-slayer-build-guide; [authored] pathofexile.com/forum · https://www.pathofexile.com/forum/view-thread/3078559
- **t4 doors:** `ZONE_CONTROL`, `MOMENTUM_CASCADE`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Cyclone**: delivery=motion, range=melee, width=wide, cadence=channel, motion_signature=orbit_fixed, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Cyclone: whirlwind motion identity — _expressed by_ `geometry.delivery_class`
- **acceptance asserts:**
  - `primary_delivery_class == 'motion'` [green]

## poe1-aegis-max-block — Aegis Max Block `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** cold · _raw_: cold
- **elements attested:** lightning
- **ailments attested:** _(none)_
- **eras:** 3.7-3.13;3.14-3.19;3.20+ · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 2 · **dossier rows:** 6
- **citations (2):** [communal] pathofexile.com/forum · @ComradeSerge#4604 · https://www.pathofexile.com/forum/view-thread/868996; [dataset] poedb.tw · https://poedb.tw/us/Aegis_Aurora
- **t4 doors:** `DEFENSIVE_TRADEOFF`, `RETRIBUTION_ENGINE`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Tempest Shield**: delivery=aura, range=self, count=1, chain=2 · conf 0.75
  - `#1` **delivery-agnostic offense (Retaliation / attached spell / totem)**: delivery=projectile, motion_signature=straight_line, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Aegis Max Block: self buff aura identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] lightning element register — _expressed by_ `element:lightning`
- **deviations:**
  - [accepted_downgrade] Block-chance stacking to a ~75% cap and 'ES recovered per block' are numeric magnitudes the engine expresses via def-bin block rider + on-block trigger, not a bespoke mechanism; · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'aura'` [green]
- **mapping deviation notes:** Block-chance stacking to a ~75% cap and 'ES recovered per block' are numeric magnitudes the engine expresses via def-bin block rider + on-block trigger, not a bespoke mechanism; identity intact, the exact 'infinite shield vs blockable damage' feel is a numeric-tuning outcome. Delivery-agnostic offense means the offensive geometry is a placeholder, not a source-fixed skill.

## poe1-arc — Arc `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** lightning · _raw_: lightning
- **elements attested:** lightning
- **ailments attested:** sunder
- **eras:** 1.x;2.x;3.0-3.6;3.7-3.13 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 1 · **dossier rows:** 6
- **citations (3):** [dataset] poedb.tw · https://poedb.tw/us/Arc; [communal] pathofexile.com/forum · https://www.pathofexile.com/forum/view-thread/3824370; [communal] pobarchives.com · https://pobarchives.com/build/iLtcmwee
- **t4 doors:** `ELEMENTAL_ECHO`, `GEOMETRY_PROPAGATION_cascade`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Arc**: delivery=beam, motion_signature=chain_hop, count=1, chain=2 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Arc: chain beam identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] lightning element register — _expressed by_ `element:lightning`
- **deviations:**
  - [accepted_downgrade] STEWARD AUDIT (DRIFT-CRITIC 25% sample): downgraded EXACT->CLOSE. · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'beam'` [green]
- **mapping deviation notes:** STEWARD AUDIT (DRIFT-CRITIC 25% sample): downgraded EXACT->CLOSE. Engine chain fan-out DECAYS per hop (_CHAIN_DEFAULT_DECAY=0.7, primary+3 arcs default); PoE Arc GROWS damage per remaining chain (+15% more) across 7-10 hops. Scaling direction inverted + hop count compressed — the player of the original would feel pack-clear invert (engine chain strongest on first target; Arc strongest deep in the pack). Identity (chaining lightning bolt + sunder) intact. Quantitative mint-candidate ledgered: per-kit chain-decay override >1.0.

## poe1-archmage — Archmage Mana Stacker `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** lightning · _raw_: lightning
- **elements attested:** lightning
- **ailments attested:** sunder
- **eras:** 3.7-3.13;3.20+ · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 0 · **dossier rows:** 6
- **citations (4):** [authored] pathofexile.com/forum · @EnkiVT#6435 · https://www.pathofexile.com/forum/view-thread/3147914; [dataset] poedb.tw · https://poedb.tw/us/Archmage_Support; [authored] mobalytics.gg · https://mobalytics.gg/poe/builds/mana-stacker-hierophant-comprehensive-leaguestart-guide; [authored] poe-vault.com · @TbXie · https://www.poe-vault.com/guides/ball-lightning-hierophant-build-guide
- **t4 doors:** `RESOURCE_CONVERSION`, `ELEMENTAL_ECHO`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Ball Lightning (+ Archmage Support)**: delivery=zone, speed=slow, motion_signature=burst_around_self, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Archmage Mana Stacker: circle zone identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] lightning element register — _expressed by_ `element:lightning`
- **deviations:**
  - [accepted_downgrade] The mana-stack resource identity (RESOURCE_CONVERSION) and MoM/Indigon economy warps land cleanly, but Ball Lightning's signature 'slow-drift + 150ms tick + inverse-velocity (slower orb = more hits = more damage)' has no matching 26-geometry; · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
- **mapping deviation notes:** The mana-stack resource identity (RESOURCE_CONVERSION) and MoM/Indigon economy warps land cleanly, but Ball Lightning's signature 'slow-drift + 150ms tick + inverse-velocity (slower orb = more hits = more damage)' has no matching 26-geometry; approximated as a circle tick-AoE. A player would keep the mana-as-weapon feel but lose the positional skill of drifting the orb through a pack for max hits.

## poe1-armageddon-brand — Armageddon Brand `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** fire · _raw_: fire
- **elements attested:** fire
- **ailments attested:** burn
- **eras:** 3.0-3.6;3.7-3.13 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 6 / 0 / 0 · **dossier rows:** 6
- **citations (3):** [dataset] poedb.tw · https://poedb.tw/us/Armageddon_Brand; [authored] odealo.com · https://odealo.com/articles/armageddon-brand-elementalist-build-odealos-crafty-guide; [communal] pathofexile.com/forum · https://www.pathofexile.com/forum/view-thread/3229636
- **t4 doors:** `GEOMETRY_PROPAGATION_cascade`, `ELEMENTAL_ECHO`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Armageddon Brand**: delivery=zone, motion_signature=ground_place, count=1 · conf 0.75
  - `#1` **Brand Recall**: delivery=motion, motion_signature=straight_line, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Armageddon Brand: ground targeted circle zone identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **deviations:**
  - [accepted_downgrade] The attach-emitter-mark + periodic meteor lands via trigger-grammar (mark_identity + burst-damage) and ground_targeted_circle, but the meteor's TIMED proc-while-attached has no exact proc_trigger_condition enum member (approximated to on-mark-apply). · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
- **mapping deviation notes:** The attach-emitter-mark + periodic meteor lands via trigger-grammar (mark_identity + burst-damage) and ground_targeted_circle, but the meteor's TIMED proc-while-attached has no exact proc_trigger_condition enum member (approximated to on-mark-apply). The distinctive 'run freely while brands auto-bombard the marked target' feel is preserved; the exact cadence-while-attached timing is a numeric property the trigger enum doesn't name.

## poe1-aurastacker — Solo Aurastacker `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** cold · _raw_: cold
- **elements attested:** water
- **ailments attested:** _(none)_
- **eras:** 3.7-3.13 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 0 · **dossier rows:** 6
- **citations (1):** [authored] pathofexile.com/forum · @Jix#7520 · https://www.pathofexile.com/forum/view-thread/2913007
- **t4 doors:** `NETWORK_AMPLIFIER`, `RESONANCE_LOOP`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **aura suite (12+ auras: Zealotry/Hatred/Determination/Grace/Discipline/Purities/etc)**: delivery=aura, range=self, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Solo Aurastacker: aura aura identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] water element register — _expressed by_ `element:water`
- **deviations:**
  - [accepted_downgrade] The self-stacking aura identity lands cleanly (NETWORK_AMPLIFIER, solo-viable unlike Aurabot), but the source reserves ~100% of the pool (via Aul's Uprising free-aura) which exceeds the engine's 0.75 LOCKED reservation cap — clamped in the map. · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'aura'` [green]
- **mapping deviation notes:** The self-stacking aura identity lands cleanly (NETWORK_AMPLIFIER, solo-viable unlike Aurabot), but the source reserves ~100% of the pool (via Aul's Uprising free-aura) which exceeds the engine's 0.75 LOCKED reservation cap — clamped in the map. A player would keep the 'walking-buff-tower who deals damage by existing' feel; the extreme near-total reservation magnitude is capped below the source's.

## poe1-ball-lightning — Ball Lightning `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** lightning · _raw_: lightning
- **elements attested:** lightning
- **ailments attested:** blind,sunder
- **eras:** 3.0-3.6;3.7-3.13 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 6 / 0 / 0 · **dossier rows:** 6
- **citations (3):** [authored] pathofexile.com/forum · @g00fy_goober#7177 · https://www.pathofexile.com/forum/view-thread/2755952; [dataset] poedb.tw · https://poedb.tw/us/Ball_Lightning; [communal] rpgstash.com · https://www.rpgstash.com/blog/ball-lightning-miner-shadow-saboteur-guide
- **t4 doors:** `GEOMETRY_PROPAGATION_cascade`, `ELEMENTAL_ECHO`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Ball Lightning (via mines)**: delivery=zone, speed=slow, motion_signature=burst_around_self, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Ball Lightning: circle zone identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] lightning element register — _expressed by_ `element:lightning`
- **deviations:**
  - [accepted_downgrade] Ball Lightning's signature 'slow drift + 150ms tick + inverse-velocity (slower = more hits)' has no matching 26-geometry — approximated as a circle tick-AoE, same as the archmage BL delivery. · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
- **mapping deviation notes:** Ball Lightning's signature 'slow drift + 150ms tick + inverse-velocity (slower = more hits)' has no matching 26-geometry — approximated as a circle tick-AoE, same as the archmage BL delivery. The mine throw/detonate chassis is modeled via trigger-grammar + activation-toggle. A player would keep the orb-zap and mine-laying feel but lose the fine positional skill of drifting the orb slowly through a pack to maximize hits.

## poe1-bane — Bane `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** chaos-poison · _raw_: chaos
- **elements attested:** shadow
- **ailments attested:** curse:amplify,curse:decrepify,curse:weaken,drain
- **eras:** 3.0-3.6;3.7-3.13 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 0 · **dossier rows:** 6
- **citations (3):** [dataset] poedb.tw · https://poedb.tw/us/Bane; [authored] odealo.com · https://odealo.com/articles/bane-occultist-starter-build; [authored] pathofexile.com/forum · @Enki#6435 · https://www.pathofexile.com/forum/view-thread/3230231
- **t4 doors:** `NETWORK_AMPLIFIER`, `PERSISTENCE_ENGINE_saturation`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Bane (+ Despair, + linked hexes)**: delivery=zone, motion_signature=ground_place, count=1, chain=2 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Bane: ground targeted circle zone identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] shadow element register — _expressed by_ `element:shadow`
- **deviations:**
  - [accepted_downgrade] The chaos-DoT-plus-curse-bundle and per-curse damage multiplier land via the drain ailment + curse: variants + NETWORK_AMPLIFIER, but the source's defining 'ONE cast applies ALL linked curses simultaneously' is expressed as the kit carrying multiple curse-ailments rather than a single bundled-cast primitive. · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
- **mapping deviation notes:** The chaos-DoT-plus-curse-bundle and per-curse damage multiplier land via the drain ailment + curse: variants + NETWORK_AMPLIFIER, but the source's defining 'ONE cast applies ALL linked curses simultaneously' is expressed as the kit carrying multiple curse-ailments rather than a single bundled-cast primitive. Outcome-faithful; a player keeps the 'cast once, everything is cursed and melting' feel, though the engine models the curses as co-applied discrete ailments.

## poe1-baron-zombies — Baron Zombies `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** 3.0-3.6;3.7-3.13 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 1 · **dossier rows:** 6
- **citations (3):** [authored] poe-vault.com · @TbXie · https://www.poe-vault.com/guides/zombiemancer-the-baron-zombies-necromancer-summoner-build-guide; [dataset] poedb.tw · https://poedb.tw/us/The_Baron; [dataset] poedb.tw · https://poedb.tw/us/Raise_Zombie
- **t4 doors:** `PROXY_ASCENSION`, `PROXY_SOVEREIGNTY`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Raise Zombie (Baron STR-stacked)**: delivery=melee_arc, range=melee, motion_signature=point_strike, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Baron Zombies: ground slam melee_arc identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] The str-stacked zombie army maps via PROXY_ASCENSION + attribute-affix scaling (Strength -> minion count/power) + TH leech, but 'a specific gear stat (STR) on your sheet becoming the army's scaling axis' is abstracted to generic attribute-stacking-of-minions rather than a bespoke Baron-helm mechanic. · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'melee_arc'` [green]
- **mapping deviation notes:** The str-stacked zombie army maps via PROXY_ASCENSION + attribute-affix scaling (Strength -> minion count/power) + TH leech, but 'a specific gear stat (STR) on your sheet becoming the army's scaling axis' is abstracted to generic attribute-stacking-of-minions rather than a bespoke Baron-helm mechanic. Outcome-faithful (stack STR, army grows); a player keeps the str-stack-summoner identity, though the flavor of one helm welding STR to zombie power is generalized.

## poe1-blade-flurry — Blade Flurry `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** bleed,poison
- **eras:** 2.x;3.0-3.6 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 1 · **dossier rows:** 6
- **citations (2):** [authored] pathofexile.com/forum · @LiftingNerdBro#1842 · https://www.pathofexile.com/forum/view-thread/1775250; [dataset] poedb.tw · https://poedb.tw/us/Blade_Flurry
- **t4 doors:** `TEMPORAL_CHARGE`, `MOMENTUM_CASCADE`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Blade Flurry**: delivery=melee_arc, range=melee, width=wide, cadence=channel, motion_signature=arc_sweep, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Blade Flurry: melee arc melee_arc identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] The channel-stack-release identity lands via PC tick-cost channel + charge-stack accumulator + TEMPORAL_CHARGE, but the frontal close-range AoE geometry ('circle in front of player') has no exact 26-type — approximated to melee_arc (neither the whirlwind-spin nor cone-breath fit). · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'melee_arc'` [green]
- **mapping deviation notes:** The channel-stack-release identity lands via PC tick-cost channel + charge-stack accumulator + TEMPORAL_CHARGE, but the frontal close-range AoE geometry ('circle in front of player') has no exact 26-type — approximated to melee_arc (neither the whirlwind-spin nor cone-breath fit). A player keeps the build-6-stages-and-detonate commitment feel; the precise frontal-circle footprint is generalized to a wide melee arc.

## poe1-blood-magic-kit — Blood Magic Life-as-Resource `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** _(unassigned)_ · _raw_: physical/chaos
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** _(unattested)_ · **tier:** — · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 1 · **dossier rows:** 6
- **citations (2):** [official] poedb.tw · https://poedb.tw/us/Blood_Magic; [communal] pathofexile.fandom.com · https://pathofexile.fandom.com/wiki/Blood_Magic
- **t4 doors:** `SACRIFICE_ASCENDANCY`, `DEFENSIVE_TRADEOFF`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Blood Magic (keystone passive — no active cast)**: delivery=aura, range=self, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Blood Magic Life-as-Resource: self buff aura identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] Life-as-resource lands on the purpose-built RS/LC lane (reservation_resource=hp + hp_cost_scale — the engine even names the guard after this kit). · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'aura'` [green]
- **mapping deviation notes:** Life-as-resource lands on the purpose-built RS/LC lane (reservation_resource=hp + hp_cost_scale — the engine even names the guard after this kit). Minor identity drift: PoE Blood Magic is TOTAL and uncapped (max mana=0, any cost can exceed your life), engine clamps to 0.30 max-HP/cast LOCKED and keeps a mana pool. The 'no safety rail, cast can kill you' danger that defines the keystone's feel is bounded by the guard. Keystone-not-active-skill => geometry is a degenerate placeholder.

## poe1-boneshatter — Boneshatter `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** stun
- **eras:** 3.14-3.19;3.20+ · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 0 · **dossier rows:** 6
- **citations (2):** [authored] maxroll.gg · @Zizaran · https://maxroll.gg/poe/build-guides/boneshatter-juggernaut-league-starter; [authored] odealo.com · https://odealo.com/articles/boneshatter-of-complex-trauma-juggernaut-build
- **t4 doors:** `TEMPORAL_CHARGE`, `SACRIFICE_ASCENDANCY`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Boneshatter**: delivery=melee_arc, range=melee, motion_signature=point_strike, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Boneshatter: ground slam melee_arc identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] Trauma maps cleanly as a charge-stack accumulator (on-hit-dealt fill, cap 9) paired with hp_cost_scale self-damage — the exact 'more damage AND more self-harm per stack' coupling, both native. · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'melee_arc'` [green]
- **mapping deviation notes:** Trauma maps cleanly as a charge-stack accumulator (on-hit-dealt fill, cap 9) paired with hp_cost_scale self-damage — the exact 'more damage AND more self-harm per stack' coupling, both native. Drift: the identity's SOUL is the reset-cliff risk-management (ride toward 9, dread the 10th-stack reset, self-damage climbing quadratically 194*(N+1)); the engine accumulator caps-and-holds rather than modelling the overflow-reset threat, and hp_cost_scale 0.30 LOCKED clamps the escalating self-hit magnitude. Damage ramp intact; the knife-edge cap-tension is approximated.

## poe1-caustic-arrow — Caustic Arrow `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** chaos-poison · _raw_: chaos
- **elements attested:** shadow
- **ailments attested:** poison
- **eras:** 1.x;2.x;3.7-3.13 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 0 · **dossier rows:** 6
- **citations (3):** [authored] pathofexile.com/forum · @Scottoria · https://www.pathofexile.com/forum/view-thread/2974902 (archive: http://web.archive.org/web/20201027013531/https://www.pathofexile.com/forum/view-thread/2974902); [authored] poe-vault.com · @Moon · https://www.poe-vault.com/guides/caustic-arrow-occultist-build-guide; [authored] odealo.com · https://odealo.com/articles/caustic-arrow-shadow-trickster-build-odealos-crafty-guide
- **t4 doors:** `PERSISTENCE_ENGINE_uptime`, `ZONE_CONTROL`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Caustic Arrow**: delivery=zone, motion_signature=ground_place, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Caustic Arrow: ground targeted circle zone identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] shadow element register — _expressed by_ `element:shadow`
- **deviations:**
  - [accepted_downgrade] Clean map to ground_targeted_circle + poison (crosswalk-mandated chaos->shadow+poison home); · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
  - [accepted_downgrade] Minor drift: PoE Caustic Arrow is a fixed-tick chaos DAMAGE-OVER-TIME cloud, while the engine `poison` ailment is stack-additive (cap 5-10); · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
- **mapping deviation notes:** Clean map to ground_targeted_circle + poison (crosswalk-mandated chaos->shadow+poison home); the hit-independent 'only the ground cloud matters' identity is native to a zone-occupancy DoT. Minor drift: PoE Caustic Arrow is a fixed-tick chaos DAMAGE-OVER-TIME cloud, while the engine `poison` ailment is stack-additive (cap 5-10); the DoT-cloud-vs-stacking-ailment nuance is smoothed by the mandated lane. Wither-totem chaos-taken amp routed as ailment-scaling debuff, noted.

## poe1-coc-ice-nova — CoC Ice Nova `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** cold · _raw_: cold
- **elements attested:** water
- **ailments attested:** chill,freeze
- **eras:** 3.0-3.6;3.7-3.13;3.20+ · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 0 · **dossier rows:** 6
- **citations (3):** [authored] poe-vault.com · https://www.poe-vault.com/guides/cyclone-cast-on-critical-ice-nova-assassin-gear-jewels-flasks; [authored] odealo.com · https://odealo.com/articles/cospris-coc-ice-nova-glacial-cascade-assassin-build-odealos-crafty-guide; [communal] pathofexileclub.wordpress.com · https://pathofexileclub.wordpress.com/2019/07/26/most-popular-poe-37-assassin-build/
- **t4 doors:** `ELEMENTAL_ECHO`, `GEOMETRY_COLLAPSE`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Cyclone (trigger host)**: delivery=motion, range=melee, speed=fast, cadence=channel, motion_signature=orbit_fixed, count=1 · conf 0.75
  - `#1` **Ice Nova (triggered payload)**: delivery=zone, range=screen, motion_signature=burst_around_self, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] CoC Ice Nova: whirlwind motion identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] water element register — _expressed by_ `element:water`
- **deviations:**
  - [accepted_downgrade] on-crit -> linked-cast is native and IS the CoC identity (Cyclone crit machine-guns Ice Nova). · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'motion'` [green]
- **mapping deviation notes:** on-crit -> linked-cast is native and IS the CoC identity (Cyclone crit machine-guns Ice Nova). Two smoothings: (1) Cospri's Malice is a SECOND parallel on-crit trigger (socketed spells fire too) — parallel depth-1 fan-out, but only one proc_trigger_condition primitive is modelled, so the double-trigger is a noted parallel not a chain; (2) 'attack-rate BECOMES cast-rate' via CDR breakpoints (14% CDR = ~one trigger/server-tick) is carried as cadence_scale, an approximation of a precise server-tick timing mechanic. Identity intact.

## poe1-cold-dot-occ — Cold DoT Occultist `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** cold · _raw_: cold
- **elements attested:** water
- **ailments attested:** chill
- **eras:** 3.0-3.6;3.7-3.13;3.14-3.19 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 0 · **dossier rows:** 6
- **citations (2):** [authored] poe-vault.com · @TbXie · https://www.poe-vault.com/guides/cold-dot-vortex-occultist-build-guide; [authored] odealo.com · https://odealo.com/articles/vortex-cold-snap-es-ci-occultist-build-odealos-crafty-guide
- **t4 doors:** `PERSISTENCE_ENGINE_uptime`, `ZONE_CONTROL`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Vortex**: delivery=zone, speed=instant, motion_signature=ground_place, count=1 · conf 0.75
  - `#1` **Creeping Frost**: delivery=zone, motion_signature=ground_place, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Cold DoT Occultist: ground targeted circle zone identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] water element register — _expressed by_ `element:water`
- **deviations:**
  - [accepted_downgrade] Twin structure to caustic-arrow: two ground_targeted_circle cold-DoT pools + chill (water family), self-anchored Vortex-at-feet. · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
- **mapping deviation notes:** Twin structure to caustic-arrow: two ground_targeted_circle cold-DoT pools + chill (water family), self-anchored Vortex-at-feet. Drift: PoE cold DoT is a fixed-tick DAMAGE-OVER-TIME pool scaled by DoT-multiplier with reapply-not-spam cadence; the engine carries 'cold DoT' via water + chill ailment + ground_targeted_circle, but the pure-DoT-uptime damage model is approximated (PERSISTENCE_ENGINE_uptime at capstone). The CI/ES-facetank safety identity is a def-bin/trait rider, not a geometry.

## poe1-deaths-oath — Death's Oath `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** chaos-poison · _raw_: chaos
- **elements attested:** shadow
- **ailments attested:** drain
- **eras:** 1.x;3.0-3.6;3.7-3.13 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 2 / 1 / 1 · **dossier rows:** 6
- **citations (5):** [communal] poe-vault.com · https://www.poe-vault.com/guides/deaths-oath-occultist-build; [communal] pathofexile.com · https://www.pathofexile.com/forum/view-thread/1974718/page/1; [communal] pathofexile.com · http://www.pathofexile.com/forum/view-thread/651516; [communal] odealo.com · https://odealo.com/articles/death-aura-occultist; [communal] poedb.tw · @communal · https://poedb.tw/us/Death_Aura
- **t4 doors:** `PERSISTENCE_ENGINE_uptime`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Death Aura (item-granted)**: delivery=aura, range=self, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Death's Oath: aura aura identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] shadow element register — _expressed by_ `element:shadow`
- **deviations:**
  - [accepted_downgrade] The reserved-aura constant-chaos-DoT identity + zero-button uptime lands cleanly via aura geometry + drain ailment + PERSISTENCE_ENGINE_uptime + reservation economy. · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
  - [accepted_downgrade] Minor drift: the item's signature 'chaos-damage-to-wearer-per-kill' self-harm loop (which forces the chaos-res investment that defines gearing) is expressed as a defensive-tax trait rather than a bespoke self-damage primitive; · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'aura'` [green]
- **mapping deviation notes:** The reserved-aura constant-chaos-DoT identity + zero-button uptime lands cleanly via aura geometry + drain ailment + PERSISTENCE_ENGINE_uptime + reservation economy. Minor drift: the item's signature 'chaos-damage-to-wearer-per-kill' self-harm loop (which forces the chaos-res investment that defines gearing) is expressed as a defensive-tax trait rather than a bespoke self-damage primitive; and the probe-attested 'wither' amp-debuff has no clean ailment lane. A player keeps the walk-and-melt feel; the self-damage-gearing-tension is generalized.

## poe1-discharge — Discharge `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** fire · _raw_: fire
- **elements attested:** fire,lightning
- **ailments attested:** burn
- **eras:** 1.x;2.x;3.0-3.6 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 2 · **dossier rows:** 6
- **citations (3):** [communal] odealo.com · https://odealo.com/articles/discharge-assassin-build; [communal] pathofexile.com · https://www.pathofexile.com/forum/view-thread/2680909; [communal] poedb.tw · https://poedb.tw/us/Discharge
- **t4 doors:** `TEMPORAL_CHARGE`, `MOMENTUM_CASCADE`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Discharge**: delivery=zone, motion_signature=burst_around_self, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Discharge: ring zone identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **deviations:**
  - [accepted_downgrade] The 'build the stack, dump the stack' charge-consume-all identity lands NATIVELY via accumulator + discharge_threshold, and ring nova is exact. · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
  - [accepted_downgrade] Minor drift: Discharge is intrinsically TRI-element (lightning-per-power / fire-per-endurance / cold-per-frenzy, each charge-count scaling its own damage type simultaneously) — the engine's 2 element slots keep the top-2 (fire+lightning), dropping the cold-per-frenzy contribution. · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
- **mapping deviation notes:** The 'build the stack, dump the stack' charge-consume-all identity lands NATIVELY via accumulator + discharge_threshold, and ring nova is exact. Minor drift: Discharge is intrinsically TRI-element (lightning-per-power / fire-per-endurance / cold-per-frenzy, each charge-count scaling its own damage type simultaneously) — the engine's 2 element slots keep the top-2 (fire+lightning), dropping the cold-per-frenzy contribution. A player keeps the charge-dump nova feel; the three-elements-at-once-partitioned-by-charge-type flavor is compressed to a dual-element nova.

## poe1-divine-ire — Divine Ire `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** lightning · _raw_: lightning
- **elements attested:** lightning
- **ailments attested:** sunder
- **eras:** 3.0-3.6;3.7-3.13 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 0 · **dossier rows:** 6
- **citations (3):** [communal] odealo.com · https://odealo.com/articles/divine-ire-templar-inquisitor-build; [communal] pathofexile.com · @Bergerbrush · https://www.pathofexile.com/forum/view-thread/2925066; [communal] poedb.tw · https://poedb.tw/us/Divine_Ire
- **t4 doors:** `TEMPORAL_CHARGE`, `ELEMENTAL_ECHO`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Divine Ire**: delivery=beam, range=screen, cadence=channel, motion_signature=straight_line, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Divine Ire: beam channel beam identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] lightning element register — _expressed by_ `element:lightning`
- **deviations:**
  - [accepted_downgrade] The channel-gather-then-release-beam identity lands cleanly: beam_channel geometry + native accumulator-discharge (stage-build via on-hit-dealt, fire at 10-stage cap) + tick-cost channel + shock->sunder. · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
  - [accepted_downgrade] Minor drift: the beam's fixed-length-immune-to-area-mods property and the secondary on-release damage-bubble are behavioral details the geometry enum doesn't separately model. · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'beam'` [green]
- **mapping deviation notes:** The channel-gather-then-release-beam identity lands cleanly: beam_channel geometry + native accumulator-discharge (stage-build via on-hit-dealt, fire at 10-stage cap) + tick-cost channel + shock->sunder. Minor drift: the beam's fixed-length-immune-to-area-mods property and the secondary on-release damage-bubble are behavioral details the geometry enum doesn't separately model. A player keeps the full gather-then-lance rhythm; only the beam's area-scaling-immunity nuance is generalized.

## poe1-ea-ballista — Explosive Arrow Ballista `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** fire · _raw_: fire
- **elements attested:** fire
- **ailments attested:** burn
- **eras:** 3.14-3.19;3.20+ · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 1 · **dossier rows:** 6
- **citations (5):** [communal] maxroll.gg · @Palsteron · https://maxroll.gg/poe/build-guides/explosive-arrow-ballista-elementalist; [communal] poe-vault.com · @TbXie · https://www.poe-vault.com/guides/explosive-arrow-ballista-champion-build-guide; [communal] poedb.tw · https://poedb.tw/us/Explosive_Arrow; [communal] odealo.com · https://odealo.com/articles/explosive-arrow-ballista-totem-elementalist-starter-build; [communal] poedb.tw · @communal · https://poedb.tw/us/Siege_Ballista
- **t4 doors:** `PROXY_ASCENSION`, `PERSISTENCE_ENGINE_saturation`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Explosive Arrow (via Ballista Totem)**: delivery=summon_delegate, cadence=cooldown, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Explosive Arrow Ballista: totem summon_delegate identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **deviations:**
  - [accepted_downgrade] The totem-delivered fuse-stack-then-detonate identity lands well: totem geometry (dominant loop) + native accumulator (20-fuse cap, fill-per-arrow, detonate-at-cap-or-on-death) + ground_targeted_circle burst + fire/burn. · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
  - [accepted_downgrade] Minor drift: the fuse-stack accumulates on the TARGET from MULTIPLE autonomous totems' arrows (a shared on-defender accumulator fed by proxies), which the engine models as a single-target accumulator filled by hit-events rather than a bespoke multi-totem-shared-fuse primitive; · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'summon_delegate'` [green]
- **mapping deviation notes:** The totem-delivered fuse-stack-then-detonate identity lands well: totem geometry (dominant loop) + native accumulator (20-fuse cap, fill-per-arrow, detonate-at-cap-or-on-death) + ground_targeted_circle burst + fire/burn. Minor drift: the fuse-stack accumulates on the TARGET from MULTIPLE autonomous totems' arrows (a shared on-defender accumulator fed by proxies), which the engine models as a single-target accumulator filled by hit-events rather than a bespoke multi-totem-shared-fuse primitive; and the 'detonate instantly the moment the target dies' is one accumulator discharge condition among the cap. A player keeps the place-totems-and-watch-it-erupt feel; the multi-totem-shared-fuse bookkeeping is generalized.

## poe1-earthquake — Earthquake `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** stun
- **eras:** 2.x;3.0-3.6 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 1 · **dossier rows:** 6
- **citations (4):** [communal] poe-vault.com · https://www.poe-vault.com/guides/earthquake-juggernaut-build-guide; [communal] odealo.com · https://odealo.com/articles/earthquake-juggernaut-starter-build-odealos-crafty-guide; [communal] poedb.tw · https://poedb.tw/us/Earthquake; [communal] pathofexile.com · https://www.pathofexile.com/forum/view-thread/2149501
- **t4 doors:** `GEOMETRY_COLLAPSE`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Earthquake**: delivery=melee_arc, range=melee, motion_signature=point_strike, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Earthquake: ground slam melee_arc identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] The plant-and-payoff delayed-aftershock slam lands well: ground_slam + native `delayed` timing (delay_seconds, engine-verified) whose non-stacking single-delayed-hit matches EQ's one-aftershock-per-slam exactly + physical-neutral + stun. · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
  - [accepted_downgrade] Minor drift: the aftershock's LARGER radius than the initial hit is a behavioral property carried by the geometry+timing note rather than a separate scaled-geometry field; · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'melee_arc'` [green]
- **mapping deviation notes:** The plant-and-payoff delayed-aftershock slam lands well: ground_slam + native `delayed` timing (delay_seconds, engine-verified) whose non-stacking single-delayed-hit matches EQ's one-aftershock-per-slam exactly + physical-neutral + stun. Minor drift: the aftershock's LARGER radius than the initial hit is a behavioral property carried by the geometry+timing note rather than a separate scaled-geometry field; and physical is element-neutral (flavor only) per the physical rule. A player keeps the slam-then-delayed-bigger-boom rhythm faithfully.

## poe1-earthshatter — Earthshatter `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** stun
- **eras:** 3.7-3.13;3.20+ · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 0 · **dossier rows:** 6
- **citations (6):** [communal] odealo.com · https://odealo.com/articles/earthshatter-berserker-build; [communal] pathofexile.com · https://www.pathofexile.com/forum/view-thread/2887937; [communal] poedb.tw · https://poedb.tw/us/Earthshatter; [dataset] poe.ninja · https://poe.ninja/poe1/builds/keepers?class=Berserker&skills=Earthshatter; [communal] poedb.tw · @communal · https://poedb.tw/us/Earthshatter_of_Fragility; [communal] poedb.tw · @communal · https://poedb.tw/us/Earthshatter_of_Prominence
- **t4 doors:** `GEOMETRY_PROPAGATION_cascade`, `GEOMETRY_COLLAPSE`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Earthshatter**: delivery=melee_arc, range=melee, motion_signature=point_strike, count=1 · conf 0.75
  - `#1` **Warcry (War Bringer)**: delivery=aura, range=self, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Earthshatter: ground slam melee_arc identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] The plant-then-detonate identity lands via ground_slam + apply-consume-pair trigger grammar (spikes = mark:consumption applied by slam, consumed by warcry for burst-damage) + spike-count accumulator, at chain-depth 1. · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
  - [accepted_downgrade] Minor drift: the source has TWO valid detonators (warcry OR a follow-up slam) — the map fixes on the warcry-cast trigger (on-cast-linked), the dominant Berserker loop; · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'melee_arc'` [green]
- **mapping deviation notes:** The plant-then-detonate identity lands via ground_slam + apply-consume-pair trigger grammar (spikes = mark:consumption applied by slam, consumed by warcry for burst-damage) + spike-count accumulator, at chain-depth 1. Minor drift: the source has TWO valid detonators (warcry OR a follow-up slam) — the map fixes on the warcry-cast trigger (on-cast-linked), the dominant Berserker loop; and physical is element-neutral. [D-7.6 / poe1-REVIEW-1 STRUCK 2026-07-19: the phantom alias 'Foulborn Ghostwrithe zerker(3.28)' is STRICKEN as a confabulated alias (no source fact); REVIEW-1 resolved.] A player keeps the raise-spikes-then-shatter payoff rhythm.

## poe1-facebreaker — Facebreaker Unarmed `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** stun
- **eras:** 1.x;2.x;3.0-3.6 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 1 · **dossier rows:** 6
- **citations (3):** [communal] pathofexile.com · @KorgothBG#4084 · https://www.pathofexile.com/forum/view-thread/445390; [communal] poedb.tw · https://poedb.tw/us/Facebreaker; [dataset] poe.ninja · https://poe.ninja/poe1/builds/keepers?items=Facebreaker
- **t4 doors:** `ELEMENT_CONVERSION_PHYSICAL`, `GEOMETRY_PROPAGATION_cascade`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Infernal Blow**: delivery=melee_arc, range=melee, motion_signature=point_strike, count=1 · conf 0.75
  - `#1` **Ancestral Warchief**: delivery=summon_delegate, cadence=cooldown, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Facebreaker Unarmed: melee strike melee_arc identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] The unarmed physical-punch identity lands via melee_strike + physical-neutral (physical rule) + ELEMENT_CONVERSION_PHYSICAL, with the Facebreaker 600-1000%-more-unarmed multiplier expressed as the dominant unarmed-physical gear-affix/trait scaler. · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
  - [accepted_downgrade] Minor drift: 'no weapon equipped, the gloves ARE the weapon' is abstracted to a large unarmed-damage affix rather than a bespoke empty-weapon-slot primitive; · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'melee_arc'` [green]
- **mapping deviation notes:** The unarmed physical-punch identity lands via melee_strike + physical-neutral (physical rule) + ELEMENT_CONVERSION_PHYSICAL, with the Facebreaker 600-1000%-more-unarmed multiplier expressed as the dominant unarmed-physical gear-affix/trait scaler. Minor drift: 'no weapon equipped, the gloves ARE the weapon' is abstracted to a large unarmed-damage affix rather than a bespoke empty-weapon-slot primitive; and physical is element-neutral. A player keeps the bare-fisted-bruiser feel and the item-defines-everything scaling, though the empty-weapon-slot flavor is generalized to an affix.

## poe1-flameblast — Flameblast `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** fire · _raw_: fire
- **elements attested:** fire
- **ailments attested:** burn
- **eras:** 1.x;2.x;3.0-3.6 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 0 · **dossier rows:** 6
- **citations (3):** [communal] pathofexile.com · https://www.pathofexile.com/forum/view-thread/3262997; [communal] odealo.com · https://odealo.com/articles/3-0-starter-flameblast-totem-build-odealos-crafty-guide; [communal] poedb.tw · https://poedb.tw/us/Flameblast
- **t4 doors:** `TEMPORAL_CHARGE`, `GEOMETRY_COLLAPSE`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Flameblast**: delivery=zone, cadence=channel, motion_signature=burst_around_self, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Flameblast: circle zone identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **deviations:**
  - [accepted_downgrade] Flameblast maps nearly losslessly — the purest charge-and-detonate: circle expanding-nova geometry + native accumulator-discharge (10-stage build via on-passive-tick, release at cap, and native sub-threshold release = the 'earlier release = weaker' behavior) + tick-cost rooted channel + fire/burn. · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
- **mapping deviation notes:** Flameblast maps nearly losslessly — the purest charge-and-detonate: circle expanding-nova geometry + native accumulator-discharge (10-stage build via on-passive-tick, release at cap, and native sub-threshold release = the 'earlier release = weaker' behavior) + tick-cost rooted channel + fire/burn. Only minor flavor drift: the exact +0.3m-per-stage radius growth and 165%-more-per-stage magnitude are numeric tuning the geometry/accumulator carry as scaling rather than named fields; and 'circle' (filled expanding disc) is chosen over 'ring' for the self-origin grow-out. A player keeps the full channel-grow-release commitment faithfully.

## poe1-flicker — Flicker Strike `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** 1.x;2.x;3.0-3.6;3.7-3.13;3.20+ · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 0 · **dossier rows:** 6
- **citations (3):** [dataset] poedb.tw · https://poedb.tw/us/Flicker_Strike; [communal] pathofexile.com · @Spacefight0r#5392 · https://www.pathofexile.com/forum/view-thread/2731202; [communal] pathofexile.com · @ACGIFT#1167 · https://www.pathofexile.com/forum/view-thread/3325373
- **t4 doors:** `TEMPORAL_CHARGE`, `PHASE_MOMENTUM`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Flicker Strike**: delivery=motion, motion_signature=straight_line, count=1, chain=2 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Flicker Strike: dash attack motion identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] The teleport-strike + charge-fuelled auto-chaining lands via dash_attack + charge-cycle economy + TEMPORAL_CHARGE, but two behavioral signatures generalize: (a) Flicker teleports to a RANDOM nearby enemy each hop (dash_attack models a directed reposition, not random target-hop selection); · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'motion'` [green]
- **mapping deviation notes:** The teleport-strike + charge-fuelled auto-chaining lands via dash_attack + charge-cycle economy + TEMPORAL_CHARGE, but two behavioral signatures generalize: (a) Flicker teleports to a RANDOM nearby enemy each hop (dash_attack models a directed reposition, not random target-hop selection); (b) the hard dependency where running out of charges STOPS the build cold is a numeric-sustain property, not a bespoke mechanism. A player keeps the 'blink-strike a screen while holding one button' feel; the frantic random-hop chaos and the charge-starvation failure state are approximated.

## poe1-freezing-pulse — Freezing Pulse `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** cold · _raw_: cold
- **elements attested:** water
- **ailments attested:** chill,freeze
- **eras:** 1.x;2.x;3.0-3.6 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 1 · **dossier rows:** 6
- **citations (2):** [dataset] poedb.tw · https://poedb.tw/us/Freezing_Pulse; [communal] pathofexile.com · @Fyregrass#7297 · https://www.pathofexile.com/forum/view-thread/3145014
- **t4 doors:** `ELEMENTAL_ECHO`, `ZONE_CONTROL`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Freezing Pulse**: delivery=projectile, motion_signature=straight_line, count=1, pierce=all · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Freezing Pulse: line projectile identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] water element register — _expressed by_ `element:water`
- **deviations:**
  - [accepted_downgrade] The piercing cold bolt + chill/freeze lands via line geometry + water + the freeze/shatter pair, but Freezing Pulse's defining 'damage and freeze-chance DECAY with distance -- stand close for max output' has no matching 26-geometry (distance-falloff is a numeric projectile property the enum does not carry). · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]
- **mapping deviation notes:** The piercing cold bolt + chill/freeze lands via line geometry + water + the freeze/shatter pair, but Freezing Pulse's defining 'damage and freeze-chance DECAY with distance -- stand close for max output' has no matching 26-geometry (distance-falloff is a numeric projectile property the enum does not carry). A player keeps the piercing-cold-caster feel but loses the core positional discipline of hugging targets to hit the damage/freeze breakpoints before the pulse fades.

## poe1-frost-blades — Frost Blades `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** cold · _raw_: cold
- **elements attested:** water
- **ailments attested:** chill,freeze
- **eras:** 2.x;3.7-3.13;3.20+ · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 1 / 0 · **dossier rows:** 6
- **citations (4):** [dataset] poedb.tw · https://poedb.tw/us/Frost_Blades; [communal] pathofexile.com · @bashtart#2403 · https://www.pathofexile.com/forum/view-thread/2077486; [communal] pathofexile.com · @Timmytimmy123#6879 · https://www.pathofexile.com/forum/view-thread/2919061; [communal] maxroll.gg · @FuzzyDuckzy · https://maxroll.gg/poe/build-guides/frost-blades-slayer-league-starter
- **t4 doors:** `GEOMETRY_PROPAGATION_cascade`, `ELEMENTAL_ECHO`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Frost Blades (melee strike)**: delivery=melee_arc, range=melee, motion_signature=point_strike, count=1 · conf 0.75
  - `#1` **Frost Blades (projectile release)**: delivery=projectile, motion_signature=fan_spread, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Frost Blades: melee strike melee_arc identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] water element register — _expressed by_ `element:water`
- **deviations:**
  - [accepted_downgrade] The melee-strike-spawns-icy-projectiles identity lands as a two-geometry composite (melee_strike + multi_projectile) with GEOMETRY_PROPAGATION_cascade for the hit-to-fan propagation, but the engine expresses it as two discrete geometries rather than a single unified 'strike that emits a projectile fan' primitive. · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'melee_arc'` [green]
- **mapping deviation notes:** The melee-strike-spawns-icy-projectiles identity lands as a two-geometry composite (melee_strike + multi_projectile) with GEOMETRY_PROPAGATION_cascade for the hit-to-fan propagation, but the engine expresses it as two discrete geometries rather than a single unified 'strike that emits a projectile fan' primitive. The 30%-less-damage fan and the exact 'behind the first target' spawn geometry are behavioral properties. A player keeps the engage-in-melee / damage-projects-behind feel; the tight coupling of one attack producing both hits is generalized to two linked geometries.

## poe1-generals-cry — General's Cry `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** bleed
- **eras:** 3.11-3.13;3.20+ · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 1 / 0 · **dossier rows:** 6
- **citations (2):** [dataset] poedb.tw · https://poedb.tw/us/Generals_Cry; [communal] pathofexile.com · @wishdropper#0634 · https://www.pathofexile.com/forum/view-thread/2998167
- **t4 doors:** `PROXY_FISSION`, `PROXY_ASCENSION`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **General's Cry (warcry)**: delivery=aura, range=self, cadence=cooldown, count=1 · conf 0.75
  - `#1` **Mirage Warrior (linked strike executor)**: delivery=melee_arc, range=melee, width=wide, motion_signature=arc_sweep, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] General's Cry: self buff aura identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] The corpse-summon -> transient-proxies-execute-your-linked-strike identity lands via PROXY_FISSION + on-cast-linked/linked-cast trigger-grammar at depth-1, but two properties generalize: (a) the mirages perform an EXERTED (warcry-boosted) copy of the player's SPECIFIC linked skill -- the engine models a generic linked-cast, not a faithful clone of an arbitrary chosen strike; · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'aura'` [green]
- **mapping deviation notes:** The corpse-summon -> transient-proxies-execute-your-linked-strike identity lands via PROXY_FISSION + on-cast-linked/linked-cast trigger-grammar at depth-1, but two properties generalize: (a) the mirages perform an EXERTED (warcry-boosted) copy of the player's SPECIFIC linked skill -- the engine models a generic linked-cast, not a faithful clone of an arbitrary chosen strike; (b) the corpse-consumption gate (no corpses = no warriors) is a resource dependency the economy lane approximates rather than a hard summon-fuel primitive. A player keeps the 'warcry erupts a mirage squad that all attack at once' feel; the exact skill-cloning and corpse-gating are abstracted.

## poe1-glacial-cascade-mines — Glacial Cascade Mines `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** cold · _raw_: cold
- **elements attested:** water
- **ailments attested:** chill,freeze,knockback
- **eras:** 3.0-3.6;3.7-3.13 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 3 / 1 / 0 · **dossier rows:** 6
- **citations (2):** [dataset] poedb.tw · https://poedb.tw/us/Glacial_Cascade; [communal] maxroll.gg · @aer0 · https://maxroll.gg/poe/build-guides/glacial-cascade-elementalist-league-starter
- **t4 doors:** `GEOMETRY_PROPAGATION_cascade`, `ELEMENTAL_ECHO`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Glacial Cascade (via High-Impact Mine)**: delivery=projectile, motion_signature=straight_line, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Glacial Cascade Mines: line projectile identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] water element register — _expressed by_ `element:water`
- **deviations:**
  - [accepted_downgrade] The marching 4-burst ice cascade + knockback + freeze/shatter lands via line + GEOMETRY_PROPAGATION_cascade + the mine trigger-chassis, but two properties generalize: (a) the precise '4 discrete sequential bursts each bigger/final-burst-double-radius' cadence is a numeric multi-hit property line geometry doesn't enumerate; · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]
- **mapping deviation notes:** The marching 4-burst ice cascade + knockback + freeze/shatter lands via line + GEOMETRY_PROPAGATION_cascade + the mine trigger-chassis, but two properties generalize: (a) the precise '4 discrete sequential bursts each bigger/final-burst-double-radius' cadence is a numeric multi-hit property line geometry doesn't enumerate; (b) the mine throw/detonate delivery is approximated via trigger-grammar + activation-toggle rather than a native mine primitive. A player keeps the 'lay mines, erupt a shoving line of ice that shatters the pack' feel; the exact burst-count/overlap-tuning and mine cadence are abstracted.

## poe1-glacial-hammer — Glacial Hammer `[NEGATIVE, class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** cold · _raw_: cold
- **elements attested:** water
- **ailments attested:** chill,freeze
- **eras:** 1.x;2.x;3.0-3.6 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 6 / 0 / 0 · **dossier rows:** 6
- **citations (2):** [dataset] poedb.tw · https://poedb.tw/us/Glacial_Hammer; [communal] pathofexile.com · @mantol456#0648 · https://www.pathofexile.com/forum/view-thread/3332780
- **t4 doors:** `ELEMENT_CONVERSION_PHYSICAL`, `ELEMENTAL_ECHO`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Glacial Hammer**: delivery=melee_arc, range=melee, motion_signature=point_strike, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Glacial Hammer: melee strike melee_arc identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] water element register — _expressed by_ `element:water`
- **deviations:**
  - [accepted_downgrade] The phys->cold single-target striker + freeze/shatter lands cleanly via melee_strike + ELEMENT_CONVERSION_PHYSICAL + the engine's NATIVE shatter (a direct match to shatter-frozen-low-life), but the 'every 3rd successive hit deals 200-390% more damage' cadence-counter has no enum carrier -- it is a behavioral property noted in traits, not modeled as a mechanism. · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'melee_arc'` [green]
- **numerics:**
  - `more_damage_390` = 390.0 (poe1_more_damage)
- **mapping deviation notes:** The phys->cold single-target striker + freeze/shatter lands cleanly via melee_strike + ELEMENT_CONVERSION_PHYSICAL + the engine's NATIVE shatter (a direct match to shatter-frozen-low-life), but the 'every 3rd successive hit deals 200-390% more damage' cadence-counter has no enum carrier -- it is a behavioral property noted in traits, not modeled as a mechanism. A player keeps the freeze-a-target-then-shatter-it cold-mace identity; the rhythmic every-3rd-hit power-stroke pacing is generalized to flat strike output.

## poe1-golementalist — Golementalist `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** fire · _raw_: fire
- **elements attested:** fire
- **ailments attested:** burn
- **eras:** 2.x;3.0-3.6;3.7-3.13 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 1 · **dossier rows:** 6
- **citations (2):** [communal] pathofexile.com · @Angry_Roleplayer#6657 · https://www.pathofexile.com/forum/view-thread/2146515; [dataset] poedb.tw · https://poedb.tw/us/Summon_Flame_Golem
- **t4 doors:** `PROXY_ASCENSION`, `PROXY_CONVERGENCE`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Summon Flame Golem (primary damage proxy, x4)**: delivery=summon_delegate, cadence=cooldown, count=1 · conf 0.75
  - `#1` **Summon Ice/Lightning/Stone/Chaos Golem (support menagerie)**: delivery=summon_delegate, cadence=cooldown, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Golementalist: totem summon_delegate identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **deviations:**
  - [accepted_downgrade] The 8-golem menagerie (flame golems kill, other golem types buff the squad via jewels) maps via PROXY_ASCENSION + PROXY_CONVERGENCE + two proxy skill-entries, but the SPECIFIC engine of it -- Primordial Harmony cooldown-resets as the flame-golem DPS multiplier and Primordial Eminence as a per-golem-type effectiveness aura -- is abstracted to minion-cast-speed + golem-effectiveness affixes rather t · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'summon_delegate'` [green]
- **mapping deviation notes:** The 8-golem menagerie (flame golems kill, other golem types buff the squad via jewels) maps via PROXY_ASCENSION + PROXY_CONVERGENCE + two proxy skill-entries, but the SPECIFIC engine of it -- Primordial Harmony cooldown-resets as the flame-golem DPS multiplier and Primordial Eminence as a per-golem-type effectiveness aura -- is abstracted to minion-cast-speed + golem-effectiveness affixes rather than a bespoke 'jewel-driven cooldown-reset + menagerie-buff' primitive. A player keeps the 'command a diverse golem squad where support-golems empower the killers' identity; the exact Primordial-jewel scaling loop is generalized to proxy traits.

## poe1-hexblast-mines — Hexblast Mines `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** chaos-poison · _raw_: chaos
- **elements attested:** shadow
- **ailments attested:** curse:amplify
- **eras:** 3.12-3.13;3.20+ · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 3 / 1 / 0 · **dossier rows:** 6
- **citations (3):** [dataset] poedb.tw · https://poedb.tw/us/Hexblast; [official] pathofexile.com · https://www.pathofexile.com/forum/view-thread/2935777; [communal] poe-vault.com · @TbXie · https://www.poe-vault.com/guides/hexblast-miner-saboteur-build-guide
- **t4 doors:** `NETWORK_AMPLIFIER`, `ELEMENTAL_ECHO`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Hexblast (via mines)**: delivery=zone, motion_signature=burst_around_self, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Hexblast Mines: circle zone identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] shadow element register — _expressed by_ `element:shadow`
- **deviations:**
  - [accepted_downgrade] The consume-a-hex-for-amplified-chaos identity lands cleanly via on-mark-consume/consume-mark trigger-grammar + curse:amplify + NETWORK_AMPLIFIER + circle, but the full loop depends on an EXTERNAL curse-automation source (Impending Doom / hex-on-hit / Asenath's Mark) continuously re-applying the hex that Hexblast then consumes -- the apply half sits outside the kit's own skill and is captured in t · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
- **mapping deviation notes:** The consume-a-hex-for-amplified-chaos identity lands cleanly via on-mark-consume/consume-mark trigger-grammar + curse:amplify + NETWORK_AMPLIFIER + circle, but the full loop depends on an EXTERNAL curse-automation source (Impending Doom / hex-on-hit / Asenath's Mark) continuously re-applying the hex that Hexblast then consumes -- the apply half sits outside the kit's own skill and is captured in the economy lane rather than as a self-contained apply-consume primitive (MAX_CHAIN_DEPTH=1 keeps the consume as the modeled step). A player keeps the 'blast the curse off for a huge hit' feel; the automated re-cursing that sustains the loop is noted, not mechanized.

## poe1-hoag — Herald of Agony `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** chaos-poison · _raw_: chaos
- **elements attested:** shadow
- **ailments attested:** poison
- **eras:** 3.0-3.6;3.7-3.13 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 0 · **dossier rows:** 6
- **citations (5):** [dataset] poedb.tw · https://poedb.tw/us/Herald_of_Agony; [official] poe-vault.com · https://www.poe-vault.com/dev-tracker/content-update-340-path-of-exile-delve; [communal] poe-vault.com · @TbXie · https://www.poe-vault.com/guides/herald-of-agony-juggernaut-build-guide; [communal] poedb.tw · @communal · https://poedb.tw/us/Plague_Bearer; [communal] poedb.tw · @communal · https://poedb.tw/us/Cyclone
- **t4 doors:** `PROXY_ASCENSION`, `PROXY_SOVEREIGNTY`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Herald of Agony (Agony Crawler proxy)**: delivery=summon_delegate, cadence=cooldown, count=1 · conf 0.75
  - `#1` **Cyclone (Virulence feeder)**: delivery=motion, range=melee, cadence=channel, motion_signature=orbit_fixed, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Herald of Agony: totem summon_delegate identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] shadow element register — _expressed by_ `element:shadow`
- **deviations:**
  - [accepted_downgrade] The your-hits-only-feed-a-pet-that-does-everything identity lands via PROXY_ASCENSION/PROXY_SOVEREIGNTY + the Virulence accumulator + two skill-entries (crawler proxy + Cyclone feeder), but the specific coupling -- the Agony Crawler's attack-speed/damage scaling CONTINUOUSLY off the live Virulence count, and the crawler DYING the instant Virulence hits 0 -- is a behavioral property of the accumula · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'summon_delegate'` [green]
- **mapping deviation notes:** The your-hits-only-feed-a-pet-that-does-everything identity lands via PROXY_ASCENSION/PROXY_SOVEREIGNTY + the Virulence accumulator + two skill-entries (crawler proxy + Cyclone feeder), but the specific coupling -- the Agony Crawler's attack-speed/damage scaling CONTINUOUSLY off the live Virulence count, and the crawler DYING the instant Virulence hits 0 -- is a behavioral property of the accumulator noted in economy rather than a bespoke 'stack-count-drives-proxy-power-and-lifespan' primitive. A player keeps the feed-the-scorpion identity; the exact stack-to-proxy-power curve and the death-at-empty failure state are abstracted.

## poe1-ice-shot — Ice Shot `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** cold · _raw_: cold
- **elements attested:** water
- **ailments attested:** chill,freeze
- **eras:** 3.7-3.13;3.20+ · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 0 · **dossier rows:** 6
- **citations (3):** [dataset] poedb.tw · https://poedb.tw/us/Ice_Shot; [communal] poe-vault.com · @PoEVault · https://www.poe-vault.com/guides/ice-shot-deadeye-build-guide; [communal] maxroll.gg · @aer0 · https://maxroll.gg/poe/build-guides/ice-shot-of-penetration-miner-deadeye-league-starter
- **t4 doors:** `ELEMENT_CONVERSION_PHYSICAL`, `ELEMENTAL_ECHO`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Ice Shot**: delivery=zone, motion_signature=fan_spread, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Ice Shot: cone zone identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] water element register — _expressed by_ `element:water`
- **deviations:**
  - [accepted_downgrade] The cold-arrow-with-cone-splash-behind-target identity lands cleanly via cone geometry + water + ELEMENT_CONVERSION_PHYSICAL + freeze/shatter, with only · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
  - [accepted_downgrade] Minor drift: the skill is a two-part hit (partial phys->cold ON the target, then TOTAL phys->cold in the cone behind it) and the engine expresses the dominant cone while the on-target partial-conversion hit is folded into the cone-delivery note rather than modeled as a separate strike. · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
- **mapping deviation notes:** The cold-arrow-with-cone-splash-behind-target identity lands cleanly via cone geometry + water + ELEMENT_CONVERSION_PHYSICAL + freeze/shatter, with only minor drift: the skill is a two-part hit (partial phys->cold ON the target, then TOTAL phys->cold in the cone behind it) and the engine expresses the dominant cone while the on-target partial-conversion hit is folded into the cone-delivery note rather than modeled as a separate strike. A player keeps the aim-the-cone-through-the-pack cold-archer feel; the exact split between the single-target arrow hit and the full-conversion cone is generalized to the cone as the identity footprint.

## poe1-icicle-mines — Icicle Mines `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** cold · _raw_: cold
- **elements attested:** water
- **ailments attested:** chill,freeze
- **eras:** 3.8-3.13 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 2 / 1 / 1 · **dossier rows:** 6
- **citations (2):** [communal] poedb.tw · https://poedb.tw/us/Icicle_Mine; [communal] pathofexile.com · @Memoria · https://www.pathofexile.com/forum/view-thread/2638570
- **t4 doors:** `GEOMETRY_PROPAGATION_cascade`, `ELEMENTAL_ECHO`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Icicle Mine (via Detonate Mines)**: delivery=projectile, speed=fast, motion_signature=fan_spread, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Icicle Mines: multi projectile projectile identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] water element register — _expressed by_ `element:water`
- **deviations:**
  - [accepted_downgrade] Mine throw/detonate chassis is approximated via trigger-grammar + activation-toggle (engine has no mine primitive -- b04-established approximation, not re-docketed); · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]
- **mapping deviation notes:** Mine throw/detonate chassis is approximated via trigger-grammar + activation-toggle (engine has no mine primitive -- b04-established approximation, not re-docketed); the detonation-sequence projectile-count growth and the quick-dissipate range falloff are behavioral/numeric properties multi_projectile does not enumerate; the converge-from-multiple-points field generalizes toward a single volley origin. Player keeps throw-then-detonate cold volleys with shatter.

## poe1-incinerate — Incinerate `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** fire · _raw_: fire
- **elements attested:** fire
- **ailments attested:** burn
- **eras:** 1.x;2.x · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 0 · **dossier rows:** 6
- **citations (1):** [communal] poedb.tw · https://poedb.tw/us/Incinerate
- **t4 doors:** `MOMENTUM_CASCADE`, `ELEMENTAL_ECHO`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Incinerate**: delivery=beam, width=wide, cadence=channel, motion_signature=straight_line, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Incinerate: beam channel beam identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **deviations:**
  - [accepted_downgrade] Cone-vs-beam: the stage-expanding cone footprint is folded into beam_channel (channel dominance per s7.2) -- a player would see a straighter stream than the source's widening fan. · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'beam'` [green]
- **mapping deviation notes:** Cone-vs-beam: the stage-expanding cone footprint is folded into beam_channel (channel dominance per s7.2) -- a player would see a straighter stream than the source's widening fan. Stage count, per-stage cone-angle growth, and the release-wave multiplier are numeric properties with no enum carriers. 1.x-era 3-stage vs modern 8-stage numeric drift noted (mechanism identical).

## poe1-kinetic-fusillade — Kinetic Fusillade `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** 3.20+ · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 0 · **dossier rows:** 6
- **citations (3):** [communal] poedb.tw · https://poedb.tw/us/Kinetic_Fusillade; [communal] pathofexile.com · https://www.pathofexile.com/forum/view-thread/3876136; [communal] maxroll.gg · https://maxroll.gg/poe/build-guides/kinetic-fusillade-ballista-hierophant-league-starter
- **t4 doors:** `MOMENTUM_CASCADE`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Kinetic Fusillade**: delivery=projectile, motion_signature=fan_spread, count=12, chain=2 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Kinetic Fusillade: multi projectile projectile identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] The hovering-projectile halo visual, the 0.05s sequential-release rhythm, and the per-impact explosion AoE generalize to a standard multi-projectile volley with accumulator economy; · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]
- **mapping deviation notes:** The hovering-projectile halo visual, the 0.05s sequential-release rhythm, and the per-impact explosion AoE generalize to a standard multi-projectile volley with accumulator economy; the per-prior-projectile damage crescendo rides the door, not a per-projectile carrier. Source data is post-cutoff thin (delivery conf 0.3, econ 'unknown') -- re-check if a deeper dossier lands.

## poe1-lacerate-glad — Bleed Gladiator `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** bleed
- **eras:** 3.0-3.6;3.7-3.13;3.20+ · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 2 · **dossier rows:** 6
- **citations (2):** [communal] poedb.tw · https://poedb.tw/us/Lacerate; [communal] poe-vault.com · https://www.poe-vault.com/guides/lacerate-gladiator-build-guide
- **t4 doors:** `PERSISTENCE_ENGINE_uptime`, `GEOMETRY_PROPAGATION_cascade`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Lacerate (dual slash)**: delivery=melee_arc, range=melee, width=wide, motion_signature=arc_sweep, count=1 · conf 0.75
  - `#1` **Blood and Sand (stance toggle)**: delivery=aura, range=self, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Bleed Gladiator: melee arc melee_arc identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] The left-right double-slash choreography and its overlap double-hit zone generalize to a single melee_arc footprint (a Lacerate player would miss the positioning-for-overlap micro-game); · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'melee_arc'` [green]
- **mapping deviation notes:** The left-right double-slash choreography and its overlap double-hit zone generalize to a single melee_arc footprint (a Lacerate player would miss the positioning-for-overlap micro-game); the stance pair carries as a generic activation-toggle (mode re-tuning is behavioral); Gladiator max-block lives in the def-bin, not the mapping.

## poe1-lightning-arrow — Lightning Arrow `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** lightning · _raw_: lightning
- **elements attested:** lightning
- **ailments attested:** sunder
- **eras:** 1.x;3.20+ · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 1 · **dossier rows:** 6
- **citations (1):** [communal] poedb.tw · https://poedb.tw/us/Lightning_Arrow
- **t4 doors:** `ELEMENT_CONVERSION_PHYSICAL`, `ELEMENTAL_ECHO`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Lightning Arrow**: delivery=beam, motion_signature=chain_hop, count=1, chain=2 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Lightning Arrow: chain beam identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] lightning element register — _expressed by_ `element:lightning`
- **deviations:**
  - [accepted_downgrade] Simultaneous-splash-to-3 vs sequential decaying chain hops is the visible drift (pack-clear cadence, not per-target damage, is what a LA player would notice); · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'beam'` [green]
- **mapping deviation notes:** Simultaneous-splash-to-3 vs sequential decaying chain hops is the visible drift (pack-clear cadence, not per-target damage, is what a LA player would notice); the 18u fixed splash radius and up-to-3 cap are numeric properties chain does not enumerate.

## poe1-lightning-conduit — Lightning Conduit `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** lightning · _raw_: lightning
- **elements attested:** lightning
- **ailments attested:** sunder
- **eras:** 3.19;3.20+ · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 3 / 1 / 1 · **dossier rows:** 6
- **citations (3):** [communal] poedb.tw · https://poedb.tw/us/Lightning_Conduit; [communal] poe-vault.com · https://www.poe-vault.com/guides/lightning-conduit-elementalist-build-guide; [official] poe-vault.com · https://www.poe-vault.com/guides/lake-of-kalandra-league-new-skill-gems
- **t4 doors:** `RESONANCE_LOOP`, `ELEMENTAL_ECHO`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Lightning Conduit**: delivery=zone, motion_signature=burst_around_self, count=1 · conf 0.75
  - `#1` **Orb of Storms (shocker)**: delivery=summon_delegate, cadence=cooldown, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Lightning Conduit: circle zone identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] lightning element register — _expressed by_ `element:lightning`
- **deviations:**
  - [accepted_downgrade] The consumed-magnitude coupling (damage read off the shock's effect value at consume time) generalizes -- engine consume-mark fires a burst but does not read the cleared ailment's magnitude; · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
- **mapping deviation notes:** The consumed-magnitude coupling (damage read off the shock's effect value at consume time) generalizes -- engine consume-mark fires a burst but does not read the cleared ailment's magnitude; and Orb of Storms' periodic-zap cadence generalizes to totem behavior. The apply-then-cash-in loop, the sunder amp window, and the removal-on-consume all land.

## poe1-lightning-strike — Lightning Strike `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** lightning · _raw_: lightning
- **elements attested:** lightning
- **ailments attested:** sunder
- **eras:** 1.x;3.20+ · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 1 / 0 · **dossier rows:** 6
- **citations (1):** [communal] poedb.tw · https://poedb.tw/us/Lightning_Strike
- **t4 doors:** `GEOMETRY_PROPAGATION_cascade`, `ELEMENT_CONVERSION_PHYSICAL`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Lightning Strike (melee hit)**: delivery=melee_arc, range=melee, motion_signature=point_strike, count=1 · conf 0.75
  - `#1` **Lightning Strike (projectile fan)**: delivery=projectile, width=medium, motion_signature=fan_spread, count=3 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Lightning Strike: melee strike melee_arc identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] lightning element register — _expressed by_ `element:lightning`
- **deviations:**
  - [accepted_downgrade] The strike-spawns-fan identity lands as a two-geometry composite, but the engine expresses two discrete geometries rather than a unified strike-that-emits primitive (same generalization as b04 frost-blades); · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'melee_arc'` [green]
- **mapping deviation notes:** The strike-spawns-fan identity lands as a two-geometry composite, but the engine expresses two discrete geometries rather than a unified strike-that-emits primitive (same generalization as b04 frost-blades); the ~85-degree forward arc, the fan's 50%-less ratio, and the cannot-miss coupling are un-enumerated properties. A LS player keeps melee-and-ranged-in-one-button.

## poe1-low-life-shavs — Low-Life Shavronne's `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** fire · _raw_: fire
- **elements attested:** fire
- **ailments attested:** burn
- **eras:** 1.x;2.x;3.0-3.6 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 0 · **dossier rows:** 6
- **citations (2):** [communal] pathofexile.com · https://www.pathofexile.com/forum/view-thread/537555/page/2; [communal] poedb.tw · https://poedb.tw/us/Pain_Attunement
- **t4 doors:** `DEFENSIVE_TRADEOFF`, `SACRIFICE_ASCENDANCY`, `NETWORK_AMPLIFIER`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **auras on life (reservation frame)**: delivery=aura, range=self, count=1 · conf 0.75
  - `#1` **era-variable damage spell (LL RF / LL Spark)**: delivery=zone, motion_signature=burst_around_self, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Low-Life Shavronne's: aura aura identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **deviations:**
  - [accepted_downgrade] The reservation warp, the sacrifice-for-power trade, and the aura-stack payload all land on literal engine keys/doors; · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'aura'` [green]
- **mapping deviation notes:** The reservation warp, the sacrifice-for-power trade, and the aura-stack payload all land on literal engine keys/doors; what generalizes: (a) the ES-pool-substitution survival texture (living on a second pool while life is floored) -- engine defense bins differ, the near-death-but-safe FEEL is approximated by the tradeoff doors; (b) the below-35%-threshold CONDITIONAL structure flattens to a permanent static trade (faithful to lived play, since reservation pins the state); (c) the era-variable damage slot is mapped representatively (fire/RF register), not as a specific spell. A LL-Shavs player would say 'low-life auras, worse' -- the frame holds.

## poe1-mjolner — Mjölner `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** lightning · _raw_: lightning
- **elements attested:** lightning
- **ailments attested:** sunder
- **eras:** 2.x;3.0-3.6 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 1 · **dossier rows:** 6
- **citations (4):** [communal] poedb.tw · https://poedb.tw/us/Mj%C3%B6lner; [communal] pathofexile.com · @Funsy · https://www.pathofexile.com/forum/view-thread/1104996; [communal] poedb.tw · @communal · https://poedb.tw/us/Cast_On_Critical_Strike_Support; [communal] poedb.tw · @communal · https://poedb.tw/unique.php?n=Mjölner
- **t4 doors:** `RESONANCE_LOOP`, `ELEMENTAL_ECHO`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Mjolner trigger (melee swing)**: delivery=melee_arc, range=melee, cadence=cooldown, motion_signature=point_strike, count=1 · conf 0.75
  - `#1` **Arc (triggered payload; Ball Lightning alt)**: delivery=beam, motion_signature=chain_hop, count=1, chain=2 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Mjölner: melee strike melee_arc identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] lightning element register — _expressed by_ `element:lightning`
- **deviations:**
  - [accepted_downgrade] The swings-pour-out-spells identity lands via on-hit-threshold/linked-cast + proc-loop at depth-1; · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'melee_arc'` [green]
- **mapping deviation notes:** The swings-pour-out-spells identity lands via on-hit-threshold/linked-cast + proc-loop at depth-1; what generalizes: (a) the 0.25s internal cooldown (trigger-rate cap) has no engine carrier -- engine trigger cadence follows the host's hit rate uncapped; (b) the triggered-payload-costs-0 economy has no per-payload cost knob; (c) socket-order rotation between TWO socketed spells (Arc + Ball Lightning alternating) collapses to one modeled payload. Inherits the arc-b01 chain-decay drift on the payload.

## poe1-molten-strike — Molten Strike `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** fire · _raw_: fire
- **elements attested:** fire
- **ailments attested:** burn
- **eras:** 3.0-3.6 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 0 · **dossier rows:** 6
- **citations (1):** [communal] poedb.tw · https://poedb.tw/us/Molten_Strike
- **t4 doors:** `GEOMETRY_PROPAGATION_cascade`, `ELEMENT_CONVERSION_PHYSICAL`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Molten Strike (melee hit)**: delivery=melee_arc, range=melee, motion_signature=point_strike, count=1 · conf 0.75
  - `#1` **Molten Strike (magma-ball rain)**: delivery=projectile, motion_signature=fan_spread, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Molten Strike: melee strike melee_arc identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **deviations:**
  - [accepted_downgrade] Two-geometry composite generalization (as frost-blades/lightning-strike): no unified strike-emits-projectiles primitive. · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'melee_arc'` [green]
- **mapping deviation notes:** Two-geometry composite generalization (as frost-blades/lightning-strike): no unified strike-emits-projectiles primitive. The ball-overlap boss-shotgun (the identity payoff) is an emergent splash-overlap behavior the engine's multi_projectile does not guarantee; the 2-25-unit variable scatter and 60%-less ball ratio are un-enumerated numerics. A Molten Strike player keeps hammer-the-boss-under-a-magma-fountain.

## poe1-pconc — Poisonous Concoction `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** chaos-poison · _raw_: chaos
- **elements attested:** earth
- **ailments attested:** poison
- **eras:** 3.16-3.19;3.20+ · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 3 / 1 / 0 · **dossier rows:** 6
- **citations (2):** [communal] poedb.tw · https://poedb.tw/us/Poisonous_Concoction; [communal] maxroll.gg · https://maxroll.gg/poe/build-guides/poisonous-concoction-pathfinder-league-starter-guide
- **t4 doors:** `RESOURCE_CONVERSION`, `PERSISTENCE_ENGINE_saturation`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Poisonous Concoction**: delivery=zone, motion_signature=ground_place, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Poisonous Concoction: ground targeted circle zone identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] earth element register — _expressed by_ `element:earth`
- **deviations:**
  - [accepted_downgrade] The flask-charge ammo economy and poison payload land on literal engine carriers (charge cycle + native stacking poison); · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
- **mapping deviation notes:** The flask-charge ammo economy and poison payload land on literal engine carriers (charge cycle + native stacking poison); what generalizes: (a) the FLASK-item coupling -- damage read off a gear-consumable's recovery stat becomes a generic resource-conversion door, losing the 'my healing potion is my weapon' flavor; (b) the unarmed weapon-slot requirement has no lane (flavor only); (c) charge_max=10/recharge=time are representative values for an unattested exact charge pool. A PConc player keeps sprint-and-lob poison-blast rhythm with charges gating throws.

## poe1-pizza-sticks — Pizza Sticks `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** fire · _raw_: fire
- **elements attested:** fire
- **ailments attested:** burn
- **eras:** 3.0-3.6 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 6 / 0 / 0 · **dossier rows:** 6
- **citations (5):** [communal] pathofexile.com · @unknown · https://www.pathofexile.com/forum/view-thread/1730745/page/1; [dataset] poedb.tw · https://poedb.tw/us/Flameblast; [communal] youtube.com · @unknown · https://www.youtube.com/watch?v=6rfRecXbIM4; [communal] poedb.tw · @communal · https://poedb.tw/us/Ancestral_Bond; [communal] poedb.tw · @communal · https://poedb.tw/us/Spell_Totem_Support
- **t4 doors:** `PROXY_ASCENSION`, `PROXY_CONVERGENCE`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Flameblast**: delivery=zone, cadence=channel, motion_signature=burst_around_self, count=1 · conf 0.75
  - `#1` **Spell Totem**: delivery=summon_delegate, cadence=cooldown, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Pizza Sticks: circle zone identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **deviations:**
  - [accepted_downgrade] The per-stage EXPANDING blast radius (the circle visibly grows 3m per stage as the totem channels, and early detonation at partial stages trades size for cadence) has no live stack->geometry carrier — folded into circle + accumulator with notes; · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
- **mapping deviation notes:** The per-stage EXPANDING blast radius (the circle visibly grows 3m per stage as the totem channels, and early detonation at partial stages trades size for cadence) has no live stack->geometry carrier — folded into circle + accumulator with notes; a player of the original loses watching the pizza slices grow and the partial-stage detonation texture. Place-totems-they-nuke identity fully intact.

## poe1-poets-pen-vd — Poet's Pen Volatile Dead `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** fire · _raw_: fire
- **elements attested:** fire
- **ailments attested:** burn
- **eras:** 3.0-3.6 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 2 · **dossier rows:** 6
- **citations (4):** [communal] odealo.com · @odealo · https://odealo.com/articles/poets-pen-volatile-dead-berserker-marauder-odealos-crafty-guide; [dataset] poedb.tw · https://poedb.tw/us/Volatile_Dead; [communal] pathofexile.com · @unknown · https://www.pathofexile.com/forum/view-thread/2586778; [communal] poedb.tw · @communal · https://poedb.tw/us/The_Poets_Pen
- **t4 doors:** `TEMPORAL_CHARGE`, `RESOURCE_CONVERSION`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Volatile Dead**: delivery=projectile, motion_signature=fan_spread, count=1 · conf 0.75
  - `#1` **Unearth**: delivery=projectile, motion_signature=straight_line, count=1 · conf 0.75
  - `#2` **Frenzy (trigger driver)**: delivery=projectile, motion_signature=straight_line, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Poet's Pen Volatile Dead: multi projectile projectile identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **deviations:**
  - [accepted_downgrade] Two spells triggered from ONE attack (dual-wand simultaneity) generalizes to the engine's one-trigger -> linked-cast shape — mapped as the spell pair sharing the attack trigger at depth-1; · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]
- **mapping deviation notes:** Two spells triggered from ONE attack (dual-wand simultaneity) generalizes to the engine's one-trigger -> linked-cast shape — mapped as the spell pair sharing the attack trigger at depth-1; a purist loses the strict both-wands-fire-together texture. The 0.25s hard trigger-cooldown is carried as an economy note, not an enum. Corpse-seeking orb locomotion is behavioral.

## poe1-poison-bv — Poison Blade Vortex `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** chaos-poison · _raw_: chaos
- **elements attested:** shadow
- **ailments attested:** poison
- **eras:** 2.x;3.0-3.6;3.7-3.13;3.14-3.19 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 7 / 0 / 1 · **dossier rows:** 6
- **citations (6):** [dataset] poedb.tw · https://poedb.tw/us/Blade_Vortex; [communal] poe-vault.com · @TbXie · https://www.poe-vault.com/guides/poison-blade-vortex-assassin-build-guide; [communal] odealo.com · @odealo · https://odealo.com/articles/blade-vortex-poison-assassin-build; [communal] pathofexile.com · @unknown · https://www.pathofexile.com/forum/view-thread/2723275; [communal] pathofexile.com · @unknown · https://www.pathofexile.com/forum/view-thread/3168707; [dataset] poedb.tw · https://poedb.tw/us/Plague_Bearer
- **t4 doors:** `PERSISTENCE_ENGINE_saturation`, `RESOURCE_CONVERSION`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Blade Vortex**: delivery=motion, motion_signature=orbit_fixed, count=1 · conf 0.75
  - `#1` **Plague Bearer**: delivery=aura, range=self, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Poison Blade Vortex: orbit motion identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] shadow element register — _expressed by_ `element:shadow`
- **deviations:**
  - [accepted_downgrade] Blade-COUNT-scales-HIT-FREQUENCY (each added blade makes everyone in radius get hit FASTER, not harder) is a bespoke cadence coupling the engine orbit does not carry — landed as accumulator + notes. · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'motion'` [green]
- **mapping deviation notes:** Blade-COUNT-scales-HIT-FREQUENCY (each added blade makes everyone in radius get hit FASTER, not harder) is a bespoke cadence coupling the engine orbit does not carry — landed as accumulator + notes. Plague Bearer's store-fraction-then-release pool is approximated as accumulator-spend into an aura (the incubate/release toggle rhythm noted). Walk-the-blender identity intact.

## poe1-righteous-fire — Righteous Fire `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** fire · _raw_: fire
- **elements attested:** fire
- **ailments attested:** burn
- **eras:** 1.x;3.0-3.6;3.7-3.13;3.14-3.19;3.20+ · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 10 / 0 / 0 · **dossier rows:** 6
- **citations (3):** [dataset] poedb.tw · https://poedb.tw/us/Righteous_Fire; [communal] poe-vault.com · @Pohx · https://www.poe-vault.com/guides/righteous-fire-juggernaut-build-guide; [communal] poe-vault.com · @unknown · https://www.poe-vault.com/guides/the-burning-man-righteous-fire-juggernaut-build-guide
- **t4 doors:** `PERSISTENCE_ENGINE_uptime`, `DEFENSIVE_TRADEOFF`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Righteous Fire**: delivery=aura, range=self, count=1 · conf 0.75
  - `#1` **Fire Trap**: delivery=zone, motion_signature=ground_place, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Righteous Fire: aura aura identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **deviations:**
  - [accepted_downgrade] Self-burn intensity clamped by the LOCKED 0.30 hp-cost ceiling: the source's knife-edge 'your own skill is actively killing you and one gear mistake means you burn to death' tension softens to a strong-but-survivable tick. · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'aura'` [green]
- **mapping deviation notes:** Self-burn intensity clamped by the LOCKED 0.30 hp-cost ceiling: the source's knife-edge 'your own skill is actively killing you and one gear mistake means you burn to death' tension softens to a strong-but-survivable tick. Walk-forward burning-aura identity, zero-button loop, and the regen race itself are intact.

## poe1-skeleton-mages — Skeleton Mages `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** cold · _raw_: cold
- **elements attested:** water
- **ailments attested:** chill,freeze
- **eras:** 3.7-3.13;3.14-3.19 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 0 · **dossier rows:** 6
- **citations (4):** [communal] maxroll.gg · @unknown · https://maxroll.gg/poe/build-guides/skeleton-mages-necromancer; [communal] buildofexile.com · @unknown · https://www.buildofexile.com/builds/5410; [communal] pathofexilegems.com · @unknown · https://pathofexilegems.com/builds/3-18-summon-skeletons-mages-necromancer-full-build/; [dataset] poedb.tw · https://poedb.tw/us/Summon_Skeletons
- **t4 doors:** `PROXY_ASCENSION`, `PROXY_FISSION`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Summon Skeletons (Dead Reckoning mage conversion)**: delivery=projectile, motion_signature=straight_line, count=1, pierce=all · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Skeleton Mages: single target projectile identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] water element register — _expressed by_ `element:water`
- **deviations:**
  - [engine_inexpressible] Per-mage random element (fire/cold/lightning roulette) flattened to the mono-cold meta endpoint — the pre-conversion rainbow-squad texture is lost (docket accrual filed, kit graded un-minted). → _fix_ `new_door_rfc`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]
  - `expresses: Per-mage random element (fire/cold/lightning roulette) flattened to the mono-col` [red] · expected: RED until engine lane exists (routed to docket)
- **mapping deviation notes:** Per-mage random element (fire/cold/lightning roulette) flattened to the mono-cold meta endpoint — the pre-conversion rainbow-squad texture is lost (docket accrual filed, kit graded un-minted). Squad-formation multi-point delivery carried by the proxy frame around single_target bolts.

## poe1-soulrend — Soulrend `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** chaos-poison · _raw_: chaos
- **elements attested:** shadow
- **ailments attested:** drain
- **eras:** 3.0-3.6;3.7-3.13 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 1 · **dossier rows:** 6
- **citations (1):** [dataset] poedb.tw · https://poedb.tw/us/Soulrend
- **t4 doors:** `PERSISTENCE_ENGINE_uptime`, `RESOURCE_CONVERSION`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Soulrend**: delivery=projectile, motion_signature=straight_line, count=1, pierce=all · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Soulrend: line projectile identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] shadow element register — _expressed by_ `element:shadow`
- **deviations:**
  - [accepted_downgrade] The damage-FEEDS-defense loop (per-hit spell-leech -> energy shield) has no resource_economy key — the TH lane converts damage TAKEN, not dealt; · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]
- **mapping deviation notes:** The damage-FEEDS-defense loop (per-hit spell-leech -> energy shield) has no resource_economy key — the TH lane converts damage TAKEN, not dealt; carried via the defense probe (ES primary), trait lane, and the RESOURCE_CONVERSION door. A player of the original misses the mechanical per-pack shield-refill pulse; homing-turn and the DoT-area-around-the-projectile are behavioral notes on the line pierce.

## poe1-spark — Spark `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** lightning · _raw_: lightning
- **elements attested:** lightning
- **ailments attested:** sunder
- **eras:** 1.x;2.x;3.14-3.19;3.20+ · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 7 / 0 / 0 · **dossier rows:** 6
- **citations (3):** [dataset] poedb.tw · https://poedb.tw/us/Spark; [communal] rpgstash.com · @unknown · https://www.rpgstash.com/blog/326-spark-inquisitor-build-poe-secrets-of-the-atlas; [communal] poe-vault.com · @unknown · https://www.poe-vault.com/guides/spark-inquisitor-build-guide
- **t4 doors:** `ZONE_CONTROL`, `PERSISTENCE_ENGINE_saturation`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Spark**: delivery=projectile, motion_signature=fan_spread, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Spark: multi projectile projectile identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] lightning element register — _expressed by_ `element:lightning`
- **deviations:**
  - [accepted_downgrade] Terrain-aware bouncing + stochastic wander — the properties that make ROOM GEOMETRY the build's real damage variable (corridors strong, open fields weak) — are behavioral with no 26-type carrier; · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]
- **mapping deviation notes:** Terrain-aware bouncing + stochastic wander — the properties that make ROOM GEOMETRY the build's real damage variable (corridors strong, open fields weak) — are behavioral with no 26-type carrier; a player keeps the spark-flood but loses the walls mattering. Duration/150-unit travel caps are numeric notes.

## poe1-spectral-helix — Spectral Helix `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** bleed
- **eras:** 3.14-3.19;3.20+ · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 0 · **dossier rows:** 6
- **citations (1):** [dataset] poedb.tw · https://poedb.tw/us/Spectral_Helix
- **t4 doors:** `TEMPORAL_CHARGE`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Spectral Helix**: delivery=projectile, width=wide, motion_signature=straight_line, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Spectral Helix: line projectile identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] The corkscrew signature — the literal helix path, hits distributed along ~4.25 rotations, and the density-at-spiral-crossings texture (near-origin overlap shotgunning) — collapses to a line + wide-swath note; · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]
- **mapping deviation notes:** The corkscrew signature — the literal helix path, hits distributed along ~4.25 rotations, and the density-at-spiral-crossings texture (near-origin overlap shotgunning) — collapses to a line + wide-swath note; the player keeps 'throw spinning blades that grind through packs at attack speed', loses the helix choreography itself. Wall-bounce behavioral.

## poe1-split-arrow-bleed — Split Arrow Bleed `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** bleed
- **eras:** 3.0-3.6;3.7-3.13 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 2 · **dossier rows:** 6
- **citations (2):** [dataset] poedb.tw · https://poedb.tw/us/Split_Arrow; [communal] odealo.com · https://odealo.com/articles/bleeding-split-arrow-puncture-gladiator-build
- **t4 doors:** `GEOMETRY_PROPAGATION_cascade`, `PERSISTENCE_ENGINE_uptime`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Split Arrow**: delivery=projectile, motion_signature=fan_spread, count=1 · conf 0.75
  - `#1` **Puncture**: delivery=projectile, motion_signature=straight_line, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Split Arrow Bleed: multi projectile projectile identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] Minor drift: 5-9 arrow count scaling, the no-double-hit-per-attack rule, and explosion magnitude tuning are behavioral; · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]
- **mapping deviation notes:** Minor drift: 5-9 arrow count scaling, the no-double-hit-per-attack rule, and explosion magnitude tuning are behavioral; bleed, fan, swap-rotation, and on-kill pops all land on native lanes.

## poe1-sst — Spectral Shield Throw `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** bleed
- **eras:** 3.0-3.6;3.20+ · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 0 · **dossier rows:** 6
- **citations (3):** [dataset] poedb.tw · https://poedb.tw/us/Spectral_Shield_Throw; [communal] odealo.com · https://odealo.com/articles/spectral-shield-throw-pure-physical-gladiator-odealos-crafty-guide; [communal] odealo.com · https://odealo.com/articles/elemental-spectral-shield-throw-raider
- **t4 doors:** `GEOMETRY_PROPAGATION`, `RESOURCE_CONVERSION`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Spectral Shield Throw**: delivery=projectile, motion_signature=fan_spread, count=1, pierce=all, chain=2 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Spectral Shield Throw: multi projectile projectile identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] Minor drift: primary-vs-secondary pierce split and shard-count patch history are behavioral; · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]
- **mapping deviation notes:** Minor drift: primary-vs-secondary pierce split and shard-count patch history are behavioral; defence-scaling approximated via door + affix lane. The throw-and-shatter loop itself lands cleanly.

## poe1-storm-brand — Storm Brand `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** lightning · _raw_: lightning
- **elements attested:** lightning
- **ailments attested:** sunder
- **eras:** 3.0-3.6;3.7-3.13 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 1 · **dossier rows:** 6
- **citations (4):** [dataset] poedb.tw · https://poedb.tw/us/Storm_Brand; [communal] odealo.com · https://odealo.com/articles/storm-brand-inquisitor; [communal] odealo.com · https://odealo.com/articles/storm-brand-hierophant-build-odealos-crafty-guide; [authored] maxroll.gg · https://maxroll.gg/poe/build-guides/storm-brand-inquisitor-league-starter
- **t4 doors:** `PERSISTENCE_ENGINE_uptime`, `ZONE_CONTROL`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Storm Brand**: delivery=beam, motion_signature=chain_hop, count=1, chain=2 · conf 0.75
  - `#1` **Brand Recall**: delivery=aura, range=self, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Storm Brand: chain beam identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] lightning element register — _expressed by_ `element:lightning`
- **deviations:**
  - [accepted_downgrade] Minor drift: 80%-more-to-branded-target split, 0.5s activation cadence, and multi-brand juggling are behavioral; · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'beam'` [green]
- **mapping deviation notes:** Minor drift: 80%-more-to-branded-target split, 0.5s activation cadence, and multi-brand juggling are behavioral; the set-and-forget chained-lightning-while-you-move identity lands on chain + proc-loop + full-move chassis (mine/brand-chassis-via-trigger-grammar per b04 precedent).

## poe1-sweep — Sweep `[NEGATIVE, class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** knockback
- **eras:** 1.x;2.x;3.0-3.6 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 0 · **dossier rows:** 6
- **citations (4):** [dataset] poedb.tw · https://poedb.tw/us/Sweep; [communal] pathofexile.com/forum · @Blackdepp · https://www.pathofexile.com/forum/view-thread/1583197; [communal] pathofexile.com/forum · https://www.pathofexile.com/forum/view-thread/3143065; [communal] pathofexile.com/forum · https://www.pathofexile.com/forum/view-thread/1490076
- **t4 doors:** `ZONE_CONTROL`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Sweep**: delivery=melee_arc, range=melee, width=wide, motion_signature=arc_sweep, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Sweep: melee arc melee_arc identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] Minor drift: 360-degree full circle rendered as wide melee arc (nearest member, noted); · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'melee_arc'` [green]
- **mapping deviation notes:** Minor drift: 360-degree full circle rendered as wide melee arc (nearest member, noted); hit-cap and leveling-skill register are flavor. The stand-and-sweep knockback loop lands.

## poe1-tectonic-slam — Tectonic Slam `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** fire · _raw_: fire
- **elements attested:** fire
- **ailments attested:** burn
- **eras:** 3.2-3.6 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 1 · **dossier rows:** 6
- **citations (3):** [dataset] poedb.tw · https://poedb.tw/us/Tectonic_Slam; [communal] odealo.com · https://odealo.com/articles/tectonic-slam-chieftain-build; [authored] poe-vault.com · https://www.poe-vault.com/guides/tectonic-slam-juggernaut-build-guide
- **t4 doors:** `ELEMENT_CONVERSION_PHYSICAL`, `TEMPORAL_CHARGE`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Tectonic Slam**: delivery=melee_arc, range=melee, motion_signature=point_strike, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Tectonic Slam: ground slam melee_arc identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **deviations:**
  - [accepted_downgrade] Minor drift: every-3rd-slam charge cadence and the random branch-fissure spray are behavioral; · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'melee_arc'` [green]
- **mapping deviation notes:** Minor drift: every-3rd-slam charge cadence and the random branch-fissure spray are behavioral; charge-fed converted fire slam lands on native slam + charge-cycle + conversion lanes.

## poe1-tornado-shot — Tornado Shot `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** 1.x;3.0-3.6;3.7-3.13;3.20+ · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 2 · **dossier rows:** 6
- **citations (2):** [dataset] poedb.tw · https://poedb.tw/us/Tornado_Shot; [authored] poe-vault.com · @Manni · https://www.poe-vault.com/guides/manni-tornado-shot-deadeye-build-guide
- **t4 doors:** `GEOMETRY_PROPAGATION`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Tornado Shot**: delivery=projectile, motion_signature=fan_spread, count=1, pierce=all · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Tornado Shot: multi projectile projectile identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] Minor drift: no-double-hit-per-burst and secondary-range-from-projectile-speed are behavioral; · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]
- **mapping deviation notes:** Minor drift: no-double-hit-per-burst and secondary-range-from-projectile-speed are behavioral; the fire-at-point-then-radial-burst clear identity lands as multi_projectile propagation.

## poe1-toxic-rain — Toxic Rain `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** chaos-poison · _raw_: chaos
- **elements attested:** earth
- **ailments attested:** chill,poison
- **eras:** 3.4-3.6;3.7-3.13;3.14-3.19;3.20+ · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 6 / 0 / 1 · **dossier rows:** 6
- **citations (3):** [dataset] poedb.tw · https://poedb.tw/us/Toxic_Rain; [authored] poe-vault.com · @PathofEvening · https://www.poe-vault.com/guides/toxic-rain-pathfinder-build-guide; [authored] maxroll.gg · https://maxroll.gg/poe/build-guides/toxic-rain-ballista-pathfinder
- **t4 doors:** `PERSISTENCE_ENGINE_saturation`, `ZONE_CONTROL`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Toxic Rain**: delivery=zone, motion_signature=ground_place, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Toxic Rain: ground targeted circle zone identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] earth element register — _expressed by_ `element:earth`
- **deviations:**
  - [accepted_downgrade] Minor drift: per-pod stacking-slow cap, the 5-pod overlap breakpoint, and pod-burst timing are behavioral density parameters on one ground-DoT zone lane; · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
- **mapping deviation notes:** Minor drift: per-pod stacking-slow cap, the 5-pod overlap breakpoint, and pod-burst timing are behavioral density parameters on one ground-DoT zone lane; the rain-pods-blanket-and-run identity lands (saturation door carries stack-density).

## poe1-viper-poison — Poison Assassin (Viper/Pestilent) `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** chaos-poison · _raw_: chaos
- **elements attested:** earth
- **ailments attested:** poison
- **eras:** 3.7-3.13 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 1 / 2 · **dossier rows:** 6
- **citations (3):** [communal] pathofexile.com/forum · @tylam6746 · https://www.pathofexile.com/forum/view-thread/2646990; [dataset] poedb.tw · https://poedb.tw/us/Pestilent_Strike; [dataset] poedb.tw · https://poedb.tw/us/Viper_Strike
- **t4 doors:** `GEOMETRY_PROPAGATION_cascade`, `PERSISTENCE_ENGINE_saturation`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Pestilent Strike**: delivery=melee_arc, range=melee, speed=fast, motion_signature=point_strike, count=1 · conf 0.75
  - `#1` **Viper Strike**: delivery=melee_arc, range=melee, motion_signature=point_strike, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Poison Assassin (Viper/Pestilent): melee strike melee_arc identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] earth element register — _expressed by_ `element:earth`
- **deviations:**
  - [accepted_downgrade] Minor drift only: Pestilent's kill-burst consumes-remaining-poison math simplified to on-kill cascade; · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'melee_arc'` [green]
- **mapping deviation notes:** Minor drift only: Pestilent's kill-burst consumes-remaining-poison math simplified to on-kill cascade; poison instance bookkeeping approximated by native stack cap. Identity (stack poison fast, kills pop the pack) intact.

## poe1-warchief — Ancestral Warchief `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** 2.x;3.0-3.6 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 1 · **dossier rows:** 6
- **citations (3):** [communal] pathofexile.com/forum · @guggelhupf#2310 · https://www.pathofexile.com/forum/view-thread/1694250; [dataset] poedb.tw · https://poedb.tw/us/Ancestral_Warchief; [communal] odealo.com · @Odealo · https://odealo.com/articles/3-0-anc-warchief-berseker-starter-and-uber-farmer-odealos-crafty-guide
- **t4 doors:** `PROXY_ASCENSION`, `ELEMENT_CONVERSION_PHYSICAL`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Ancestral Warchief**: delivery=summon_delegate, cadence=cooldown, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Ancestral Warchief: totem summon_delegate identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] Minor drift: the proximity-coaching buff becomes flavor (engine has no player-adjacency-buffs-proxy primitive); · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'summon_delegate'` [green]
- **mapping deviation notes:** Minor drift: the proximity-coaching buff becomes flavor (engine has no player-adjacency-buffs-proxy primitive); multi-totem count rides the proxy door rather than an Ancestral Bond analog. A Warchief player still recognizes plant-stand-slam.

## poe1-winter-orb — Winter Orb `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** cold · _raw_: cold
- **elements attested:** water
- **ailments attested:** chill,freeze
- **eras:** 3.5-3.6 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 2 / 1 / 1 · **dossier rows:** 6
- **citations (4):** [dataset] poedb.tw · https://poedb.tw/us/Winter_Orb; [communal] pathofexile.com/forum · @Angry_Roleplayer#6657 · https://www.pathofexile.com/forum/view-thread/2320561; [communal] odealo.com · @Odealo · https://odealo.com/articles/winter-orb-elementalist-non-crit-poe-build; [communal] requnix.com · https://requnix.com/path-of-exile-3-5-betrayal-best-builds/
- **t4 doors:** `TEMPORAL_CHARGE`, `PERSISTENCE_ENGINE_uptime`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Winter Orb**: delivery=motion, cadence=channel, motion_signature=orbit_fixed, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Winter Orb: orbit motion identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] water element register — _expressed by_ `element:water`
- **deviations:**
  - [accepted_downgrade] Minor drift: turret-projectile behavior vs orbit contact presence (noted, R-M6-spirit nearest-geometry call); · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'motion'` [green]
- **mapping deviation notes:** Minor drift: turret-projectile behavior vs orbit contact presence (noted, R-M6-spirit nearest-geometry call); decay pacing approximated. A Winter Orb player still recognizes channel-charge, run, personal blizzard turret.

## poe1-woc-ignite — Wave of Conviction Ignite `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** fire · _raw_: fire
- **elements attested:** fire
- **ailments attested:** burn,sunder
- **eras:** 3.7-3.13;3.14-3.19 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 2 · **dossier rows:** 6
- **citations (3):** [dataset] poedb.tw · https://poedb.tw/us/Wave_of_Conviction; [authored] poe-vault.com · @TbXie · https://www.poe-vault.com/guides/wave-of-conviction-ignite-elementalist-build-guide; [communal] pathofexile.com/forum · https://www.pathofexile.com/forum/view-thread/3324120
- **t4 doors:** `PERSISTENCE_ENGINE`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Wave of Conviction**: delivery=zone, width=wide, motion_signature=fan_spread, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Wave of Conviction Ignite: cone zone identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **deviations:**
  - [accepted_downgrade] Minor drift: the one-touch-per-wave rule and the single-giant-ignite cap are simplified against engine burn application; · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
- **mapping deviation notes:** Minor drift: the one-touch-per-wave rule and the single-giant-ignite cap are simplified against engine burn application; exposure timing window approximated by sunder duration band. Identity (walk, cast one wave, one huge burn per body) intact.

## poe1-animate-weapon — Animate Weapon `[class:record]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** shadow
- **ailments attested:** poison
- **eras:** 1.x;3.7-3.13;3.20+ · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 0 · **dossier rows:** 6
- **citations (4):** [authored] maxroll.gg · @Helm Breaker · https://maxroll.gg/poe/build-guides/poison-ranged-animate-weapons-league-starter; [dataset] poedb.tw · https://poedb.tw/us/Animate_Weapon; [communal] pathofexile.com/forum · @Hoffen#2482 · https://www.pathofexile.com/forum/view-thread/3788773; [authored] poe-vault.com · @GhazzyTV · https://www.poe-vault.com/guides/animate-weapon-necromancer-build-guide
- **t4 doors:** `PROXY_FISSION`, `PROXY_ASCENSION`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Bladefall of Trarthus (blade-drop feeder)**: delivery=projectile, motion_signature=fan_spread, count=1 · conf 0.75
  - `#1` **Animate Weapon of Ranged Arms**: delivery=summon_delegate, cadence=cooldown, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Animate Weapon: multi projectile projectile identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] shadow element register — _expressed by_ `element:shadow`
- **deviations:**
  - [engine_inexpressible] The 'ground-lying weapons ARE the summon ammunition; → _fix_ `new_door_rfc`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]
  - `expresses: The 'ground-lying weapons ARE the summon ammunition;` [red] · expected: RED until engine lane exists (routed to docket)
- **mapping deviation notes:** The 'ground-lying weapons ARE the summon ammunition; the loot drop-stream is the resource pool' is the kit's signature identity and has no engine lane — engine proxies draw from mana/corpses, not consumed ground-item entities. Mapped as a standard transient poison-proxy swarm (PROXY_FISSION) which captures the combat feel but LOSES the loot-becomes-ammo resource-substrate. A player of the original would miss that their army's size and cadence were fed by what dropped on the floor. Docket candidate filed.

## poe1-autobomber — Autobomber `[class:record]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** cold · _raw_: cold
- **elements attested:** lightning,water
- **ailments attested:** freeze,sunder
- **eras:** 3.0-3.6;3.7-3.13 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 1 · **dossier rows:** 6
- **citations (3):** [communal] pobarchives.com · https://pobarchives.com/build/3cgUfRhq; [dataset] poedb.tw · https://poedb.tw/us/Herald_of_Ice; [communal] poecurrency.com · https://www.poecurrency.com/news/hot-autobomber-elementalist-poe-3-20
- **t4 doors:** `GEOMETRY_PROPAGATION_cascade`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Shield Charge (movement / freeze-trigger)**: delivery=motion, motion_signature=straight_line, count=1 · conf 0.75
  - `#1` **Herald of Ice + Inpulsa's Broken Heart (on-kill explosion chain)**: delivery=zone, motion_signature=burst_around_self, count=1, chain=2 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Autobomber: dash attack motion identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] water element register — _expressed by_ `element:water`
- **deviations:**
  - [accepted_downgrade] The kit's signature is an UNBOUNDED cascading kill-chain (each explosion-kill triggers the next explosion across the whole pack). · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'motion'` [green]
- **mapping deviation notes:** The kit's signature is an UNBOUNDED cascading kill-chain (each explosion-kill triggers the next explosion across the whole pack). Engine MAX_CHAIN_DEPTH=1 is LOCKED, so the map expresses a single on-kill->burst step via GEOMETRY_PROPAGATION_cascade — the chain-reaction is truncated to one hop, never minted deeper per charter law. A player of the original would notice the screen-wide auto-chain becomes a bounded single-propagation; the 'zero-input movement clears everything' identity is intact but its unlimited-cascade magnitude is capped.

## poe1-bladefall-bladeblast — Bladefall + Blade Blast `[class:record]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** 3.7-3.13 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 1 · **dossier rows:** 6
- **citations (4):** [authored] maxroll.gg · @Tripolarbear · https://maxroll.gg/poe/build-guides/bladefall-bladeblast-occultist-league-starter-guide; [communal] pathofexile.com/forum · https://www.pathofexile.com/forum/view-thread/2919618 (archive: http://web.archive.org/web/20200921172755/https://www.pathofexile.com/forum/view-thread/2919618); [authored] pathofexile.com/forum · @TraviiGrinds · https://www.pathofexile.com/forum/view-thread/3009876; [authored] poe-vault.com · @TbXie · https://www.poe-vault.com/guides/blade-blast-chieftain-build-guide
- **t4 doors:** `GEOMETRY_PROPAGATION_cascade`, `GEOMETRY_COLLAPSE`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Bladefall**: delivery=projectile, motion_signature=fan_spread, count=1 · conf 0.75
  - `#1` **Blade Blast**: delivery=zone, motion_signature=burst_around_self, count=1, chain=2 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Bladefall + Blade Blast: multi projectile projectile identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [engine_inexpressible] The signature is a TWO-STAGE coupling: Bladefall PLANTS a lingering-blade field; → _fix_ `new_door_rfc`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]
  - `expresses: The signature is a TWO-STAGE coupling: Bladefall PLANTS a lingering-blade field;` [red] · expected: RED until engine lane exists (routed to docket)
- **mapping deviation notes:** The signature is a TWO-STAGE coupling: Bladefall PLANTS a lingering-blade field; Blade Blast CONSUMES that field as detonation fuel (blade count = damage budget, up to 30 detonations/s). No engine lane represents 'a placed-entity field that a second skill spends as a consumable ammunition queue' — engine placed entities are autonomous, not spend-by-detonation. Mapped as multi_projectile seed feeding a ring explosion-cascade (GEOMETRY_PROPAGATION_cascade), which lands the plant-then-explode combat feel but loses the shared field-resource substrate that COUPLES the two buttons. A player of the original would miss that Bladefall's job is to stock the ammo Blade Blast burns. Docket candidate filed (field-resource-consume, shared with animate-weapon).

## poe1-charged-dash — Charged Dash `[NEGATIVE, class:record]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** lightning · _raw_: lightning
- **elements attested:** lightning
- **ailments attested:** _(none)_
- **eras:** 3.0-3.6;3.7-3.13 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 0 · **dossier rows:** 6
- **citations (3):** [official] poedb.tw · https://poedb.tw/us/Charged_Dash; [authored] odealo.com · https://odealo.com/articles/charged-dash-raider; [authored] pathofexile.com/forum · https://www.pathofexile.com/forum/view-thread/2605098
- **t4 doors:** `PHASE_MOMENTUM`, `TEMPORAL_CHARGE`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Charged Dash**: delivery=motion, cadence=channel, motion_signature=straight_line, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Charged Dash: dash attack motion identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] lightning element register — _expressed by_ `element:lightning`
- **deviations:**
  - [accepted_downgrade] The identity is a compound the base geometry flattens: a cursor-STEERED illusion-phantom (not the player) that emits NON-OVERLAPPING lane-pulses (the single-target flaw) then teleports the player to its endpoint UNCANCELLABLY (the danger flaw). · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'motion'` [green]
- **mapping deviation notes:** The identity is a compound the base geometry flattens: a cursor-STEERED illusion-phantom (not the player) that emits NON-OVERLAPPING lane-pulses (the single-target flaw) then teleports the player to its endpoint UNCANCELLABLY (the danger flaw). Engine dash_attack lands the reposition-as-strike but loses the piloted-phantom feel, the along-path pulse emission, and both flaw-mechanics that make this a NEGATIVE kit. A player of the original would miss the steerable illusion and the exact clunk. Deliberately NOT minted: reproducing a known-bad skill's bespoke awkwardness violates parsimony; the negative-canon value is the record, not a build target.

## poe1-crackling-lance — Crackling Lance `[class:record]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** lightning · _raw_: lightning
- **elements attested:** lightning
- **ailments attested:** sunder
- **eras:** 3.12-3.13 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 3 / 1 / 0 · **dossier rows:** 6
- **citations (3):** [official] poedb.tw · https://poedb.tw/us/Crackling_Lance; [authored] odealo.com · https://odealo.com/articles/crackling-lance-elementalist-build; [communal] mmogah.com · https://www.mmogah.com/news/poe/poe-3-12-builds-crackling-lance-build-guide
- **t4 doors:** `ELEMENTAL_ECHO`, `TEMPORAL_CHARGE`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Crackling Lance**: delivery=beam, width=narrow, cadence=channel, motion_signature=straight_line, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Crackling Lance: beam channel beam identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] lightning element register — _expressed by_ `element:lightning`
- **deviations:**
  - [accepted_downgrade] beam_channel + lightning + sunder lands the base skill, but the IDENTITY is Intensity — a stand-still stack ramp (max 3, +35% dmg/stack) that SIMULTANEOUSLY morphs the geometry: each stack widens the beam +0.3m AND narrows branching 33%, transforming a wide frontal fan into a focused lance. · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'beam'` [green]
- **mapping deviation notes:** beam_channel + lightning + sunder lands the base skill, but the IDENTITY is Intensity — a stand-still stack ramp (max 3, +35% dmg/stack) that SIMULTANEOUSLY morphs the geometry: each stack widens the beam +0.3m AND narrows branching 33%, transforming a wide frontal fan into a focused lance. The engine carries the damage-ramp (accumulator) OR the beam, but no lane represents 'stack count continuously reshapes beam width + branching.' A player would lose the signature beam-tightening-as-you-hold-ground AoE-vs-damage trade. Not minted (geometry-morph-by-stacks is an evidence-gated qualitative mechanism; flagged if it recurs). Era 3.12-3.13 per verify_ledger errata, respected.

## poe1-cwdt-loop — CWDT Self-Hit Loop `[class:record]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** chaos-poison · _raw_: chaos
- **elements attested:** shadow
- **ailments attested:** _(none)_
- **eras:** 3.14-3.19;3.20+ · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 0 · **dossier rows:** 6
- **citations (3):** [communal] reddit.com/r/pathofexile (via libredd.it) · https://libredd.it/r/pathofexile/comments/ou2jej/new_cwdt_loop_with_forbidden_rite_and_petrified/; [authored] odealo.com · https://odealo.com/articles/heartbound-loop-autobomber-scion-build; [authored] pathofexile.com/forum · https://www.pathofexile.com/forum/view-thread/3261066
- **t4 doors:** `RETRIBUTION_ENGINE`, `SACRIFICE_ASCENDANCY`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Cast when Damage Taken (trigger)**: delivery=aura, range=self, count=1 · conf 0.75
  - `#1` **Forbidden Rite / VD (triggered self-damage payload)**: delivery=zone, motion_signature=burst_around_self, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] CWDT Self-Hit Loop: self buff aura identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] shadow element register — _expressed by_ `element:shadow`
- **deviations:**
  - [accepted_downgrade] on-damage-taken -> linked-cast is native at depth 1, but the IDENTITY is a CLOSED SELF-FEEDING CIRCUIT: the triggered spell's own self-damage re-crosses the CwDT threshold and re-triggers CwDT indefinitely — the consequence re-triggering its cause = trigger-chain DEPTH >1. · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'aura'` [green]
- **mapping deviation notes:** on-damage-taken -> linked-cast is native at depth 1, but the IDENTITY is a CLOSED SELF-FEEDING CIRCUIT: the triggered spell's own self-damage re-crosses the CwDT threshold and re-triggers CwDT indefinitely — the consequence re-triggering its cause = trigger-chain DEPTH >1. MAX_CHAIN_DEPTH=1 is LOCKED (template law): deeper chains APPROX + note, NEVER a depth mint. Engine models one hop and stops; the self-perpetuating automation-circuit (a build that plays itself) cannot be represented or minted. A player would get one cast per external hit, not the autonomous loop that IS the kit. Not a missing-lane docket — a deliberate engine LOCK; recorded as the canonical MAX_CHAIN_DEPTH exemplar.

## poe1-dark-pact — Dark Pact `[class:record]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** chaos-poison · _raw_: chaos
- **elements attested:** shadow
- **ailments attested:** drain
- **eras:** 3.0-3.6 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 1 · **dossier rows:** 6
- **citations (2):** [authored] pathofexile.com/forum · @poetech#3681 · https://www.pathofexile.com/forum/view-thread/1954194 (archive: http://web.archive.org/web/20170817003830/http://www.pathofexile.com:80/forum/view-thread/1954194); [authored] poe-vault.com · @GhazzyTV · https://www.poe-vault.com/guides/dark-pact-necromancer-build-guide
- **t4 doors:** `PROXY_FISSION`, `SACRIFICE_ASCENDANCY`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Dark Pact**: delivery=beam, motion_signature=chain_hop, count=1, chain=2 · conf 0.75
  - `#1` **Summon Skeletons (fuel/proxy source)**: delivery=summon_delegate, cadence=cooldown, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Dark Pact: chain beam identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] shadow element register — _expressed by_ `element:shadow`
- **deviations:**
  - [engine_inexpressible] chain + shadow(chaos) + drain lands the chaining sacrifice-nova, but the SIGNATURE is an INVERSION of the proxy pattern: skeletons are CONSUMABLE BATTERIES whose MAX LIFE is the ammo Dark Pact spends — Minion Life supports scale YOUR damage by inflating the battery. → _fix_ `new_door_rfc`
- **acceptance asserts:**
  - `primary_delivery_class == 'beam'` [green]
  - `expresses: chain + shadow(chaos) + drain lands the chaining sacrifice-nova, but the SIGNATU` [red] · expected: RED until engine lane exists (routed to docket)
- **mapping deviation notes:** chain + shadow(chaos) + drain lands the chaining sacrifice-nova, but the SIGNATURE is an INVERSION of the proxy pattern: skeletons are CONSUMABLE BATTERIES whose MAX LIFE is the ammo Dark Pact spends — Minion Life supports scale YOUR damage by inflating the battery. No engine lane represents 'proxy max-life as a consumable per-cast ammo pool'; the PROXY family models proxies that attack + are sustained, not consumed as fuel. Mapped as chain-nova + totem-battery-field + minion-life-consume note + hp_cost_scale no-skeleton fallback (native); captures the chain-chaos feel but loses the battery-inversion substrate. Docket filed (proxy-max-life-as-ammo, shared with animate-weapon + this batch's bladefall field-consume). Engine chain decays 0.7x/hop (arc precedent) — acceptable since Dark Pact propagates not grows, hop-count capped vs PoE noted.

## poe1-edc — Essence Drain + Contagion `[class:record]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** chaos-poison · _raw_: chaos
- **elements attested:** shadow
- **ailments attested:** drain
- **eras:** 2.x;3.0-3.6;3.7-3.13;3.14-3.19 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 6 / 0 / 0 · **dossier rows:** 6
- **citations (4):** [communal] poe-vault.com · @TbXie · https://www.poe-vault.com/guides/essence-drain-contagion-trickster-build-guide; [communal] odealo.com · https://odealo.com/articles/3-1-essence-drain-occultist-starter-build-odealos-crafty-guide; [communal] poedb.tw · https://poedb.tw/us/Essence_Drain; [communal] pathofexile.com · https://www.pathofexile.com/forum/view-thread/2333065
- **t4 doors:** `GEOMETRY_PROPAGATION_cascade`, `PERSISTENCE_ENGINE_saturation`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Essence Drain**: delivery=projectile, motion_signature=fan_spread, count=1 · conf 0.75
  - `#1` **Contagion**: delivery=zone, motion_signature=ground_place, count=1, chain=2 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Essence Drain + Contagion: multi projectile projectile identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] shadow element register — _expressed by_ `element:shadow`
- **deviations:**
  - [accepted_downgrade] The two-button DoT-plague maps via drain ailment + on-defender-death trigger (native) + GEOMETRY_PROPAGATION_cascade, but the SIGNATURE is an UNBOUNDED cascading room-clear — each death spreads the ED DoT, those spread-DoTs kill, which spread again, rippling across the whole pack. · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]
- **mapping deviation notes:** The two-button DoT-plague maps via drain ailment + on-defender-death trigger (native) + GEOMETRY_PROPAGATION_cascade, but the SIGNATURE is an UNBOUNDED cascading room-clear — each death spreads the ED DoT, those spread-DoTs kill, which spread again, rippling across the whole pack. Engine MAX_CHAIN_DEPTH=1 is LOCKED, so the map expresses a single on-death->spread hop — the chain-reaction is truncated to one propagation, never minted deeper per charter law. A player of the original would notice the screen-wide spreading plague becomes a bounded single-hop spread; the 'cast twice and watch the room dissolve in ripples' identity is intact but its unlimited-cascade magnitude is capped.

## poe1-elemental-hit — Elemental Hit `[class:record]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** fire · _raw_: fire
- **elements attested:** fire
- **ailments attested:** burn
- **eras:** 3.0-3.6 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 0 · **dossier rows:** 6
- **citations (4):** [communal] poe-vault.com · https://www.poe-vault.com/guides/elemental-hit-deadeye-build-guide; [official] pathofexile.com · https://www.pathofexile.com/forum/view-thread/2148537; [communal] odealo.com · https://odealo.com/articles/fire-elemental-hit-deadeye-starter-build-odealos-crafty-guide; [communal] poedb.tw · @communal · https://poedb.tw/us/Elemental_Hit
- **t4 doors:** `ELEMENT_CONVERSION_MONO`, `ELEMENTAL_ECHO`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Elemental Hit**: delivery=projectile, motion_signature=fan_spread, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Elemental Hit: multi projectile projectile identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **deviations:**
  - [engine_inexpressible] The defining mechanic — each attack rolls a RANDOM element from {fire,cold,lightning}, and build-defining Combat Focus jewels PRUNE that pool to force a single element — has no engine lane: engine fixes one element per skill at generation, with no per-attack-RNG-element-roll and no element-pool-pruning primitive. → _fix_ `new_door_rfc`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]
  - `expresses: The defining mechanic — each attack rolls a RANDOM element from {fire,cold,light` [red] · expected: RED until engine lane exists (routed to docket)
- **mapping deviation notes:** The defining mechanic — each attack rolls a RANDOM element from {fire,cold,lightning}, and build-defining Combat Focus jewels PRUNE that pool to force a single element — has no engine lane: engine fixes one element per skill at generation, with no per-attack-RNG-element-roll and no element-pool-pruning primitive. Mapped to the meta ENDPOINT (forced mono-fire bow burst via ELEMENT_CONVERSION_MONO), which captures where the build lands but LOSES the random-roll-then-sculpt-the-pool identity that makes Combat Focus jewels the signature item. A player would miss that their element came from a pool they curated.

## poe1-fire-trap — Fire Trap `[class:record]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** fire · _raw_: fire
- **elements attested:** fire
- **ailments attested:** burn
- **eras:** 1.x;2.x;3.7-3.13 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 1 · **dossier rows:** 6
- **citations (3):** [communal] pathofexile.com · https://www.pathofexile.com/forum/view-thread/1872594/page/1; [communal] odealo.com · https://odealo.com/articles/fire-trap-elementalist-build; [communal] poedb.tw · https://poedb.tw/us/Fire_Trap
- **t4 doors:** `ZONE_CONTROL`, `PERSISTENCE_ENGINE_uptime`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Fire Trap**: delivery=zone, motion_signature=ground_place, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Fire Trap: ground targeted circle zone identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **deviations:**
  - [accepted_downgrade] The deploy-and-bait trap identity approximates across trigger-grammar (trap = placed mark, proximity-detonation = consume -> burst-damage) + activation-toggle throw rhythm + ground_targeted_circle burning-ground, but the engine has no dedicated TRAP primitive: 'throw to ground -> arm as a dormant device -> detonate when an enemy STEPS NEAR (proximity-enter)' is mapped to on-hit-threshold (the near · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
- **mapping deviation notes:** The deploy-and-bait trap identity approximates across trigger-grammar (trap = placed mark, proximity-detonation = consume -> burst-damage) + activation-toggle throw rhythm + ground_targeted_circle burning-ground, but the engine has no dedicated TRAP primitive: 'throw to ground -> arm as a dormant device -> detonate when an enemy STEPS NEAR (proximity-enter)' is mapped to on-hit-threshold (the nearest proc; there is no on-proximity-enter condition). A player of Fire Trap would notice the pre-arm-and-bait positional game (place traps, lure enemies onto them) becomes a more generic placed-hazard-that-fires-on-contact; the burning-ground DoT and deploy-a-zone feel are intact, but the distinctive dormant-trap-armed-in-advance mechanic is approximated.

## poe1-minion-pact-bv — Minion Pact Blade Vortex `[class:record]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** 3.20+ · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 2 · **dossier rows:** 6
- **citations (2):** [communal] poedb.tw · https://poedb.tw/us/Blade_Vortex; [communal] poedb.tw · https://poedb.tw/us/Minion_Pact_Support
- **t4 doors:** `SACRIFICE_ASCENDANCY`, `RESOURCE_CONVERSION`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Blade Vortex (with Minion Pact Support)**: delivery=motion, motion_signature=orbit_fixed, count=1 · conf 0.75
  - `#1` **Raise Spectre (sacrifice feedstock)**: delivery=summon_delegate, cadence=cooldown, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Minion Pact Blade Vortex: orbit motion identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] What the player of the original would miss: (a) the literal slaughter -- engine has no primitive for consuming a proxy entity and reading its LIFE POOL into a spell's damage; · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'motion'` [green]
- **mapping deviation notes:** What the player of the original would miss: (a) the literal slaughter -- engine has no primitive for consuming a proxy entity and reading its LIFE POOL into a spell's damage; the trigger-grammar + cycle-economy + doors model the rhythm and the trade, not the mechanism; (b) the SNAPSHOT (sacrificed-minion life locked into blade damage for their duration) has no carrier; (c) minion-life as an OFFENSIVE scaling stat inverts the trait lane (approximated in scaffold traits). The blade-orbit shell, the raise/sacrifice treadmill, and the sacrifice-for-power identity read through -- 'that build, worse', hence APPROX not GAPPED (R-M7 player test; b02 dark-pact precedent).

## poe1-reaper — Summon Reaper `[NEGATIVE, class:record]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** 3.14-3.19 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 1 · **dossier rows:** 6
- **citations (4):** [dataset] poedb.tw · https://poedb.tw/us/Summon_Reaper; [communal] pathofexile.com · @cheapbunny · https://www.pathofexile.com/forum/view-thread/3155821; [communal] odealo.com · @odealo · https://odealo.com/articles/reaper-summoner-necromancer-build; [communal] pathofexile.com · @community · https://www.pathofexile.com/forum/view-thread/3157877
- **t4 doors:** `PROXY_SOVEREIGNTY`, `PROXY_ASCENSION`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Summon Reaper**: delivery=melee_arc, range=melee, motion_signature=arc_sweep, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Summon Reaper: melee arc melee_arc identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [engine_inexpressible] The signature sustain — the Reaper passively weakens and CONSUMES YOUR OTHER MINIONS to heal and temporarily empower itself (+30% AoE when fed) — has no engine lane: proxy sustain draws from resummon/upkeep, never from eating sibling entities (entity-as-consumable-resource-pool family, 4th accrual; → _fix_ `new_door_rfc`
- **acceptance asserts:**
  - `primary_delivery_class == 'melee_arc'` [green]
  - `expresses: The signature sustain — the Reaper passively weakens and CONSUMES YOUR OTHER MIN` [red] · expected: RED until engine lane exists (routed to docket)
- **mapping deviation notes:** The signature sustain — the Reaper passively weakens and CONSUMES YOUR OTHER MINIONS to heal and temporarily empower itself (+30% AoE when fed) — has no engine lane: proxy sustain draws from resummon/upkeep, never from eating sibling entities (entity-as-consumable-resource-pool family, 4th accrual; docket filed). A player of the original keeps the sovereign commanded pet; loses the feed-it-minions husbandry AND its starvation failure state — which is precisely the trap-canon signal the corpus negative flag records.

## poe1-scourge-arrow — Scourge Arrow `[class:record]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** chaos-poison · _raw_: chaos
- **elements attested:** earth
- **ailments attested:** poison
- **eras:** 3.0-3.6;3.7-3.13 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 0 · **dossier rows:** 6
- **citations (2):** [dataset] poedb.tw · https://poedb.tw/us/Scourge_Arrow; [communal] pathofexileclub.wordpress.com · @unknown · https://pathofexileclub.wordpress.com/2019/10/06/poe-3-8-popular-scourge-arrow-pathfinder-build-fast-tanky-easy-friendly-guide/
- **t4 doors:** `PERSISTENCE_ENGINE_saturation`, `MOMENTUM_CASCADE`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Scourge Arrow**: delivery=projectile, cadence=channel, motion_signature=fan_spread, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Scourge Arrow: multi projectile projectile identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] earth element register — _expressed by_ `element:earth`
- **deviations:**
  - [accepted_downgrade] MANDATORY: the TWO-STAGE emission chain — arrow first (laying pods along its wake), pods THEN blooming delayed 9-arrow fans — is flattened to a single multi_projectile volley. · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]
- **mapping deviation notes:** MANDATORY: the TWO-STAGE emission chain — arrow first (laying pods along its wake), pods THEN blooming delayed 9-arrow fans — is flattened to a single multi_projectile volley. The player of the original loses pod-line PLACEMENT (painting a lane of delayed bloomers through/behind the pack) and the stage-dependent pod-count texture; the channel-charge rhythm and the close-range poison-shotgun payoff are intact — 'that build, worse', not 'not that build'.

## poe1-seismic-trap — Seismic Trap `[class:record]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** 3.14-3.19 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 3 / 1 / 2 · **dossier rows:** 6
- **citations (4):** [dataset] poedb.tw · https://poedb.tw/us/Seismic_Trap; [communal] maxroll.gg · @unknown · https://maxroll.gg/poe/build-guides/seismic-trap-saboteur-league-starter-guide; [communal] pathofexile.com · @unknown · https://www.pathofexile.com/forum/view-thread/3179858; [communal] pathofexilegems.com · @unknown · https://pathofexilegems.com/builds/3-17-seismic-trap-exsanguinate-saboteur-full-build-guide/
- **t4 doors:** `ZONE_CONTROL`, `PERSISTENCE_ENGINE_saturation`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Seismic Trap**: delivery=melee_arc, range=melee, motion_signature=point_strike, count=1 · conf 0.75
  - `#1` **Exsanguinate (trap pair)**: delivery=zone, motion_signature=ground_place, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Seismic Trap: ground slam melee_arc identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] MANDATORY: two approximations stack. · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'melee_arc'` [green]
- **mapping deviation notes:** MANDATORY: two approximations stack. (a) The trap-arm-then-proximity-fire device is carried by trigger grammar, not a native placed-dormant-device primitive (fire-trap b03 precedent). (b) The SEQUENCED 5-wave timer emission — the overlapping pulse GRID that converts sustained AoE into 32-64-hit boss burst when traps stack — collapses to a single consume-burst (TIMED-WHILE-ACTIVE-APPROX); the player of the original loses the 3.5-second hammering rhythm and the stack-traps-for-overlap optimization. The throw-traps-and-kite zone-hammer identity survives.

## poe1-siege-ballista — Iron Commander Siege Ballista `[class:record]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** 2.x;3.0-3.6 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 1 · **dossier rows:** 6
- **citations (2):** [dataset] poedb.tw · https://poedb.tw/us/Siege_Ballista; [dataset] poedb.tw · https://poedb.tw/us/Iron_Commander
- **t4 doors:** `PROXY_ASCENSION`, `PROXY_FISSION`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Siege Ballista**: delivery=summon_delegate, cadence=cooldown, count=1, pierce=all · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Iron Commander Siege Ballista: totem summon_delegate identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] MANDATORY: the central scaling loop — every 200 DEX is literally another ballista, so every gear/attribute decision COUNTS the army — is severed; · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'summon_delegate'` [green]
- **mapping deviation notes:** MANDATORY: the central scaling loop — every 200 DEX is literally another ballista, so every gear/attribute decision COUNTS the army — is severed; the player keeps the turret-battery archetype but attribute-stacking regresses to ordinary stat scaling instead of visible army growth. Graded as-if-un-minted per the parsimony ladder; docket candidate filed (attribute-value -> proxy-count coupling).

## poe1-spectral-throw — Spectral Throw `[class:record]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** lightning · _raw_: lightning
- **elements attested:** lightning,water
- **ailments attested:** sunder
- **eras:** 1.x;2.x · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 1 / 0 · **dossier rows:** 6
- **citations (3):** [dataset] poedb.tw · https://poedb.tw/us/Spectral_Throw; [communal] pathofexile.com/forum · @g00fy_goober · https://www.pathofexile.com/forum/view-thread/1839087; [communal] pathofexile.com/forum · https://www.pathofexile.com/forum/view-thread/1531912
- **t4 doors:** `ELEMENTAL_ECHO`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Spectral Throw**: delivery=projectile, cadence=cooldown, motion_signature=straight_line, count=1, pierce=all · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Spectral Throw: line projectile identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] lightning element register — _expressed by_ `element:lightning`
- **deviations:**
  - [accepted_downgrade] What the Ele Buzzsaw player would miss: the return pass — hitting enemies BEHIND you on the way back, the double-hit overlap zone at the deceleration point, and the stutter-step rhythm of standing inside overlapping out-and-return copies. · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]
- **mapping deviation notes:** What the Ele Buzzsaw player would miss: the return pass — hitting enemies BEHIND you on the way back, the double-hit overlap zone at the deceleration point, and the stutter-step rhythm of standing inside overlapping out-and-return copies. Engine expresses a one-way piercing line only.

## poe1-srs — Summon Raging Spirits `[class:record]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** fire · _raw_: fire
- **elements attested:** fire
- **ailments attested:** burn
- **eras:** 1.x;2.x;3.0-3.6;3.7-3.13;3.20+ · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 6 / 0 / 2 · **dossier rows:** 6
- **citations (5):** [dataset] poedb.tw · https://poedb.tw/us/Summon_Raging_Spirit; [communal] pathofexile.com/forum · https://www.pathofexile.com/forum/view-thread/1427765; [communal] pathofexile.com/forum · https://www.pathofexile.com/forum/view-thread/2983747; [authored] maxroll.gg · https://maxroll.gg/poe/build-guides/summon-raging-spirit-guardian-league-starter; [communal] poedb.tw · @communal · https://poedb.tw/us/Minion_Instability
- **t4 doors:** `PROXY_FISSION`, `ELEMENT_CONVERSION_MONO`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Summon Raging Spirit**: delivery=summon_delegate, cadence=cooldown, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Summon Raging Spirits: totem summon_delegate identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **deviations:**
  - [accepted_downgrade] What the SRS player would miss: the 20-skull machine-gun swarm scale, the flight/homing delivery, and minion untargetability. · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'summon_delegate'` [green]
- **mapping deviation notes:** What the SRS player would miss: the 20-skull machine-gun swarm scale, the flight/homing delivery, and minion untargetability. On engine lanes this lands as a small persistent proxy set — 'SRS, worse' but recognizably the summon-spam loop.

## poe1-totem-hierophant — Totem Hierophant `[class:record]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** _(unattested)_ · **tier:** — · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 1 · **dossier rows:** 6
- **citations (3):** [communal] odealo.com · https://odealo.com/articles/arc-hexa-spell-totem-hierophant-build-odealos-crafty-guide; [dataset] poedb.tw · https://poedb.tw/us/Spell_Totem_Support; [communal] poedb.tw · @communal · https://poedb.tw/us/Hierophant
- **t4 doors:** `PROXY_ASCENSION`, `PROXY_CONVERGENCE`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Spell Totem (linked spell)**: delivery=summon_delegate, cadence=cooldown, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Totem Hierophant: totem summon_delegate identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] What the Hierophant would miss: six simultaneous totems (engine proxy counts are lower), the hard you-cannot-deal-damage keystone contract, and the 40%-slower proxy-cast tax as an explicit chassis parameter. · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'summon_delegate'` [green]
- **mapping deviation notes:** What the Hierophant would miss: six simultaneous totems (engine proxy counts are lower), the hard you-cannot-deal-damage keystone contract, and the 40%-slower proxy-cast tax as an explicit chassis parameter. Place-totems-and-kite with fewer proxies reads 'totem hiero, worse' — identity approximated, not absent.

## poe1-vaal-blade-vortex — Vaal Blade Vortex `[class:record]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** 3.0-3.6;3.7-3.13 · **tier:** — · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 0 · **dossier rows:** 6
- **citations (4):** [dataset] poedb.tw · https://poedb.tw/us/Vaal_Blade_Vortex; [communal] pathofexile.com/forum · https://www.pathofexile.com/forum/view-thread/2144834; [communal] pathofexile.com/forum · https://www.pathofexile.com/forum/view-thread/2091072; [communal] poedb.tw · @communal · https://poedb.tw/us/Blade_Vortex
- **t4 doors:** `TEMPORAL_CHARGE`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Vaal Blade Vortex**: delivery=zone, motion_signature=burst_around_self, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Vaal Blade Vortex: circle zone identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] What the VBV player would miss: the vortex HUNTING — it chases fresh enemies across the screen for its 5s life. · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
- **mapping deviation notes:** What the VBV player would miss: the vortex HUNTING — it chases fresh enemies across the screen for its 5s life. Engine circle is a stationary/drifting tick-AoE (R-M6 class); a non-seeking blade storm reads 'Vaal BV, worse' but the pursuit is the load-bearing geometry delta (batch flag a).

## poe1-venom-gyre — Venom Gyre `[class:record]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** chaos-poison · _raw_: chaos
- **elements attested:** earth
- **ailments attested:** poison
- **eras:** 3.8-3.13;3.20+ · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 1 / 1 · **dossier rows:** 6
- **citations (5):** [communal] pathofexile.com/forum · @ezyanfarihin#5882 · https://www.pathofexile.com/forum/view-thread/2634104; [communal] odealo.com · @Odealo · https://odealo.com/articles/venom-gyre-deadeye-build; [dataset] poedb.tw · https://poedb.tw/us/Venom_Gyre; [communal] pathofexile.com/forum · @loczek123 · https://www.pathofexile.com/forum/view-thread/2626271; [communal] pathofexile.com/forum · https://www.pathofexile.com/forum/view-thread/3343381
- **t4 doors:** `TEMPORAL_CHARGE`, `PERSISTENCE_ENGINE_saturation`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Venom Gyre**: delivery=projectile, motion_signature=straight_line, count=1, pierce=all · conf 0.75
  - `#1` **Whirling Blades**: delivery=motion, motion_signature=straight_line, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Venom Gyre: line projectile identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] earth element register — _expressed by_ `element:earth`
- **deviations:**
  - [accepted_downgrade] Player of the original would miss: the literal caught-projectile MAGAZINE (burst size equals number caught; · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]
- **mapping deviation notes:** Player of the original would miss: the literal caught-projectile MAGAZINE (burst size equals number caught; engine accumulator carries damage ramp instead) and the out-and-back catch geometry (line + note). Whirling-Blades-as-release-valve approximated as dash_attack with burst note; the two-button couple (thrower feeds, dash spends) survives as accumulator fill/spend.

## poe1-wander — Wander (Kinetic Blast) `[class:record]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** execute
- **eras:** 2.x;3.0-3.6;3.20+ · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 6 / 0 / 1 · **dossier rows:** 6
- **citations (4):** [communal] pathofexile.com/forum · http://www.pathofexile.com/forum/view-thread/1144534; [dataset] poedb.tw · https://poedb.tw/us/Kinetic_Blast; [communal] odealo.com · @Odealo · https://odealo.com/articles/the-fastest-poe-build-kinetic-blast-pathfinder-odealos-crafty-guide; [communal] maxroll.gg · https://maxroll.gg/poe/build-guides/league-starter/kinetic-blast-deadeye-league-starter
- **t4 doors:** `ELEMENT_CONVERSION_PHYSICAL`, `TEMPORAL_CHARGE`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Kinetic Blast**: delivery=projectile, motion_signature=fan_spread, count=1 · conf 0.75
  - `#1` **Power Siphon**: delivery=projectile, motion_signature=straight_line, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Wander (Kinetic Blast): multi projectile projectile identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] Player of the original would miss blast-OVERLAP tech — point-blank wall/corner shotgunning where multiple explosions stack on one target — and the AoE-spacing scaling knob. · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]
- **mapping deviation notes:** Player of the original would miss blast-OVERLAP tech — point-blank wall/corner shotgunning where multiple explosions stack on one target — and the AoE-spacing scaling knob. The volley approximation spreads damage points but cannot anchor them around an impact.

## poe1-whispering-ice — Whispering Ice `[class:record]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** cold · _raw_: cold
- **elements attested:** water
- **ailments attested:** chill,freeze
- **eras:** 2.x;3.0-3.6;3.7-3.13;3.20+ · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 8 / 0 / 0 · **dossier rows:** 6
- **citations (3):** [dataset] poedb.tw · https://poedb.tw/us/The_Whispering_Ice; [communal] odealo.com · @Odealo · https://odealo.com/articles/whispering-ice-icestorm-trickster-build; [communal] pathofexile.com/forum · https://www.pathofexile.com/forum/view-thread/2936012/page/2
- **t4 doors:** `RESOURCE_CONVERSION`, `PERSISTENCE_ENGINE_saturation`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Icestorm (item-granted)**: delivery=zone, motion_signature=ground_place, count=1 · conf 0.75
  - `#1` **Cyclone (CwC variant)**: delivery=motion, range=melee, cadence=channel, motion_signature=orbit_fixed, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Whispering Ice: ground targeted circle zone identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] water element register — _expressed by_ `element:water`
- **deviations:**
  - [accepted_downgrade] Player of the original would miss storms growing LONGER as INT climbs (duration side of the scaling pact) and the staff-as-whole-build item romance; · downgrade-owner `elrond (W4 tranche; W1 GAP-annotation lineage)`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
- **mapping deviation notes:** Player of the original would miss storms growing LONGER as INT climbs (duration side of the scaling pact) and the staff-as-whole-build item romance; the damage side of stat-stacking survives natively. TIMED-WHILE-ACTIVE-APPROX does not apply (storm duration is skill-native, not a proc window).

## poe1-aurabot — Aurabot `[class:record]`

- **grade / terminal:** `GAPPED` / `MAPPED_DOCKET`
- **element (court):** _(unassigned)_ · _raw_: n/a
- **elements attested:** lightning
- **ailments attested:** _(none)_
- **eras:** 2.x;3.0-3.6;3.7-3.13;3.14-3.19;3.20+ · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 1 · **dossier rows:** 6
- **citations (3):** [authored] pathofexile.com/forum · @cutiechuchu#6132 · https://www.pathofexile.com/forum/view-thread/3179545; [communal] pathofexile.com/forum · https://www.pathofexile.com/forum/view-thread/1664893; [authored] poe-vault.com · https://www.poe-vault.com/guides/necromancer-aurabot-support-build-guide
- **t4 doors:** `NETWORK_AMPLIFIER`, `RESONANCE_LOOP`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **aura suite (Wrath/Anger/Hatred/Malevolence/Determination/Grace/Haste/Purities)**: delivery=aura, range=self, count=1 · conf 0.75
  - `#1` **Smite (token personal skill)**: delivery=melee_arc, range=melee, motion_signature=point_strike, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Aurabot: aura aura identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] lightning element register — _expressed by_ `element:lightning`
- **deviations:**
  - [engine_inexpressible] Aurabot's identity is a party-support buff-projector — zero personal damage, output = ALLIES' amplified power — and it is explicitly useless solo. → _fix_ `new_door_rfc`
- **acceptance asserts:**
  - `primary_delivery_class == 'aura'` [green]
  - `expresses: Aurabot's identity is a party-support buff-projector — zero personal damage, out` [red] · expected: RED until engine lane exists (routed to docket)
- **mapping deviation notes:** Aurabot's identity is a party-support buff-projector — zero personal damage, output = ALLIES' amplified power — and it is explicitly useless solo. The engine is solo-scope, so the kit's entire purpose has no lane: there are no allies to buff. Additionally the ~100% reservation exceeds the engine's 0.75 LOCKED reservation cap. Mapped the aura shell + clamped reserve, but a player of the original would find the build does literally nothing in solo — the ally-projection that IS the kit cannot be expressed. Docketed as out-of-solo-scope.

## poe1-detonate-dead — Detonate Dead `[class:record]`

- **grade / terminal:** `GAPPED` / `MAPPED_DOCKET`
- **element (court):** fire · _raw_: fire
- **elements attested:** fire,shadow
- **ailments attested:** burn
- **eras:** 1.x;3.7-3.13;3.14-3.19 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 1 · **dossier rows:** 6
- **citations (3):** [communal] poe-vault.com · @TbXie · https://www.poe-vault.com/guides/unkillable-necro-detonate-dead-necromancer-build-guide; [communal] poedb.tw · https://poedb.tw/us/Detonate_Dead; [communal] pathofexile.com · https://www.pathofexile.com/forum/view-thread/2041296
- **t4 doors:** `GEOMETRY_PROPAGATION_cascade`, `ELEMENTAL_ECHO`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Detonate Dead**: delivery=zone, motion_signature=ground_place, count=1 · conf 0.75
  - `#1` **Desecrate**: delivery=zone, motion_signature=ground_place, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Detonate Dead: ground targeted circle zone identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **deviations:**
  - [engine_inexpressible] The corpse-as-ammunition economy lands NATIVELY (on-corpse-consume accumulator), but Detonate Dead's DEFINING mechanic — explosion damage scales as a percentage of the CORPSE's/victim's maximum life (boss corpses = huge blasts, red-map monster HP = bigger explosions) — has no engine lane: engine damage scales off caster stats, never target HP. → _fix_ `new_door_rfc`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
  - `expresses: The corpse-as-ammunition economy lands NATIVELY (on-corpse-consume accumulator),` [red] · expected: RED until engine lane exists (routed to docket)
- **mapping deviation notes:** The corpse-as-ammunition economy lands NATIVELY (on-corpse-consume accumulator), but Detonate Dead's DEFINING mechanic — explosion damage scales as a percentage of the CORPSE's/victim's maximum life (boss corpses = huge blasts, red-map monster HP = bigger explosions) — has no engine lane: engine damage scales off caster stats, never target HP. Mapped as a standard fire-AoE detonation, which LOSES the victim-HP-scaling that makes the skill iconic (a DD player would notice their blast no longer grows with the corpse's health pool). Docket candidate filed. GRADE=GAPPED (not APPROX): the victim-max-HP-fraction damage IS 'an identity-bearing mechanism with no engine lane' per the grade definition; terminal MAPPED_DOCKET follows.

## poe1-forbidden-rite — Forbidden Rite `[class:record]`

- **grade / terminal:** `GAPPED` / `MAPPED_DOCKET`
- **element (court):** chaos-poison · _raw_: chaos
- **elements attested:** shadow
- **ailments attested:** _(none)_
- **eras:** 3.14-3.19;3.20+ · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 0 · **dossier rows:** 6
- **citations (4):** [dataset] poedb.tw · https://poedb.tw/us/Forbidden_Rite; [communal] pathofexile.com · @ShamefulPenguin#7799 · https://www.pathofexile.com/forum/view-thread/3164444; [communal] odealo.com · https://odealo.com/articles/forbidden-rite-totem-hierophant-build; [communal] poe-vault.com · @GhazzyTV · https://www.poe-vault.com/guides/forbidden-rite-hierophant-build-guide
- **t4 doors:** `PROXY_ASCENSION`, `SACRIFICE_ASCENDANCY`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Forbidden Rite (via Spell Totem)**: delivery=projectile, motion_signature=fan_spread, count=1 · conf 0.75
  - `#1` **Spell Totem (delivery chassis)**: delivery=summon_delegate, cadence=cooldown, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Forbidden Rite: multi projectile projectile identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] shadow element register — _expressed by_ `element:shadow`
- **deviations:**
  - [engine_inexpressible] The kit's defining twist -- Forbidden Rite normally COSTS THE CASTER LIFE (can kill you), but routed through totems the LIFE-COST IS PAID BY THE TOTEM ENTITIES, not the player -- has no engine lane: the engine can model an hp-cost on a skill (hp_cost_scale) but cannot REDIRECT that self-damage-cost onto a proxy entity's life pool. → _fix_ `new_door_rfc`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]
  - `expresses: The kit's defining twist -- Forbidden Rite normally COSTS THE CASTER LIFE (can k` [red] · expected: RED until engine lane exists (routed to docket)
- **mapping deviation notes:** The kit's defining twist -- Forbidden Rite normally COSTS THE CASTER LIFE (can kill you), but routed through totems the LIFE-COST IS PAID BY THE TOTEM ENTITIES, not the player -- has no engine lane: the engine can model an hp-cost on a skill (hp_cost_scale) but cannot REDIRECT that self-damage-cost onto a proxy entity's life pool. Mapped as totem-proxy delivery (PROXY_ASCENSION) + a capped hp-cost on the chassis, which loses the 'the totems bleed so you don't' outsourcing that IS the build's safety identity. A player of the original would notice the life-price now lands on them rather than being laundered through disposable totems. Docket candidate filed. | [STEWARD-AUDIT R-M7 2026-07-18] Re-graded APPROX->GAPPED: the identity IS the self-damage economy (the skill hits the caster; the build routes self-chaos-damage into safety scaffolding). Engine has no self-hit lane (hp_cost_scale 0.30 LOCKED is a cast COST, not a hit event) — the player of the original would say 'this is not that build.' Terminal MAPPED_DOCKET unchanged; docket row stands.

## poe1-heavy-strike-stun — Heavy Strike Stun Berserker `[class:record]`

- **grade / terminal:** `GAPPED` / `MAPPED_DOCKET`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** chill,stun
- **eras:** 3.20+ · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 0 · **dossier rows:** 6
- **citations (2):** [dataset] poedb.tw · https://poedb.tw/us/Heavy_Strike; [communal] pathofexile.com · @mantol456#0648 · https://www.pathofexile.com/forum/view-thread/3421600
- **t4 doors:** `MOMENTUM_CASCADE`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Heavy Strike**: delivery=melee_arc, range=melee, motion_signature=point_strike, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Heavy Strike Stun Berserker: melee strike melee_arc identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [engine_inexpressible] Heavy Strike Stun's identity -- STUN IS THE DAMAGE: ~75% reduced-enemy-stun-threshold to relentlessly stun-lock, with damage scaling off the stun model -- has no engine lane. → _fix_ `new_door_rfc`
- **acceptance asserts:**
  - `primary_delivery_class == 'melee_arc'` [green]
  - `expresses: Heavy Strike Stun's identity -- STUN IS THE DAMAGE: ~75% reduced-enemy-stun-thre` [red] · expected: RED until engine lane exists (routed to docket)
- **mapping deviation notes:** Heavy Strike Stun's identity -- STUN IS THE DAMAGE: ~75% reduced-enemy-stun-threshold to relentlessly stun-lock, with damage scaling off the stun model -- has no engine lane. The engine's stun ailment is a hard-CC primitive with a deliberate anti-stunlock immunity floor + boss resistance, and it is NOT a damage source; there is no T4 strategy for 'convert stun buildup into damage'. Mapped as a melee_strike + stun ailment + the nearest (MOMENTUM_CASCADE) door, which captures 'a heavy melee that stuns' but LOSES both the perma-stunlock feel (engine prevents it) and the stun-as-damage-scaling model that IS the build. A player of the original would find stun is now crowd-control flavor on their hits rather than the damage engine. Docket candidate filed. (Low source confidence compounds the gap.) | [STEWARD-AUDIT R-M7 2026-07-18] Re-graded APPROX->GAPPED: stun-as-kill-plan (threshold stunlock as the damage mechanism) has no engine lane; without it this is generic single-target melee — 'not that build.' Terminal MAPPED_DOCKET unchanged; docket row stands.

## poe1-spectres — Spectre Necromancer `[class:record]`

- **grade / terminal:** `GAPPED` / `MAPPED_DOCKET`
- **element (court):** fire · _raw_: fire
- **elements attested:** fire,shadow
- **ailments attested:** burn
- **eras:** 3.0-3.6;3.7-3.13;3.14-3.19 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 2 · **dossier rows:** 6
- **citations (5):** [dataset] poedb.tw · https://poedb.tw/us/Raise_Spectre; [communal] pathofexile.com/forum · https://www.pathofexile.com/forum/view-thread/2094035; [communal] pathofexile.com/forum · https://www.pathofexile.com/forum/view-thread/2989420; [authored] poe-vault.com · @GhazzyTV · https://www.poe-vault.com/guides/the-spectre-summoner-build-guide; [communal] odealo.com · https://odealo.com/articles/3-1-starter-spectre-summoner-necromancer-odealos-crafty-guide
- **t4 doors:** `PROXY_ASCENSION`, `PROXY_SOVEREIGNTY`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Raise Spectre**: delivery=summon_delegate, cadence=cooldown, count=1 · conf 0.75
  - `#1` **Desecrate**: delivery=zone, motion_signature=ground_place, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Spectre Necromancer: totem summon_delegate identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **deviations:**
  - [engine_inexpressible] Player test fails: hand a Spectre Necromancer a fixed generic minion squad and they say 'this is a summoner, but this is not Spectres.' The defining identity — choosing WHICH world monster to enslave (Solar Guards vs Slave Drivers vs Syndicate Operatives) and inheriting its ability kit — has no engine mechanism class. → _fix_ `new_door_rfc`
- **acceptance asserts:**
  - `primary_delivery_class == 'summon_delegate'` [green]
  - `expresses: Player test fails: hand a Spectre Necromancer a fixed generic minion squad and t` [red] · expected: RED until engine lane exists (routed to docket)
- **mapping deviation notes:** Player test fails: hand a Spectre Necromancer a fixed generic minion squad and they say 'this is a summoner, but this is not Spectres.' The defining identity — choosing WHICH world monster to enslave (Solar Guards vs Slave Drivers vs Syndicate Operatives) and inheriting its ability kit — has no engine mechanism class.

## poe1-ward-loop — Ward Loop `[class:record]`

- **grade / terminal:** `GAPPED` / `MAPPED_DOCKET`
- **element (court):** chaos-poison · _raw_: chaos
- **elements attested:** shadow
- **ailments attested:** _(none)_
- **eras:** 3.15-3.19;3.20+ · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 1 / 1 · **dossier rows:** 6
- **citations (4):** [communal] pathofexile.com/forum · https://www.pathofexile.com/forum/view-thread/3261066; [communal] odealo.com · @Odealo · https://odealo.com/articles/heartbound-loop-autobomber-scion-build; [communal] vhpg.com · http://www.vhpg.com/poe-ward/; [communal] poecurrency.com · https://www.poecurrency.com/news/poe-3-21-how-to-fix-the-problems-in-ward-loop-build
- **t4 doors:** `RETRIBUTION_ENGINE`, `SACRIFICE_ASCENDANCY`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **CWDT (loop motor)**: delivery=aura, range=self, count=1 · conf 0.75
  - `#1` **Summon Skeletons**: delivery=summon_delegate, speed=instant, cadence=cooldown, count=1 · conf 0.75
  - `#2` **Forbidden Rite (triggered payload)**: delivery=projectile, motion_signature=fan_spread, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Ward Loop: self buff aura identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] shadow element register — _expressed by_ `element:shadow`
- **deviations:**
  - [engine_inexpressible] R-M7 player test FAILS: without the self-sustaining loop this is a reactive CWDT build that needs enemies to hit the player; → _fix_ `new_door_rfc`
- **acceptance asserts:**
  - `primary_delivery_class == 'aura'` [green]
  - `expresses: R-M7 player test FAILS: without the self-sustaining loop this is a reactive CWDT` [red] · expected: RED until engine lane exists (routed to docket)
- **mapping deviation notes:** R-M7 player test FAILS: without the self-sustaining loop this is a reactive CWDT build that needs enemies to hit the player; the original runs at full cast throughput in an EMPTY ROOM — perpetual motion is the identity, not a scaling detail. 'This is not that build.' Docket candidate filed (closed-loop self-damage trigger economy).

## poe1-wild-strike — Wild Strike `[NEGATIVE, class:record]`

- **grade / terminal:** `GAPPED` / `MAPPED_DOCKET`
- **element (court):** fire · _raw_: fire
- **elements attested:** fire
- **ailments attested:** burn
- **eras:** 2.x;3.0-3.6;3.7-3.13 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 4 · **dossier rows:** 6
- **citations (3):** [communal] pathofexile.com/forum · https://www.pathofexile.com/forum/view-thread/1478404; [communal] pathofexile.com/forum · @mamburu#3286 · https://www.pathofexile.com/forum/view-thread/3039099; [dataset] poedb.tw · https://poedb.tw/us/Wild_Strike
- **t4 doors:** `PHASE_MOMENTUM`, `ELEMENT_CONVERSION_MONO`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Wild Strike**: delivery=melee_arc, range=melee, motion_signature=point_strike, count=1, pierce=all, chain=2 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Wild Strike: melee strike melee_arc identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **deviations:**
  - [engine_inexpressible] R-M7 player test FAILS: a fixed-element strike with one fixed secondary shape is 'not that build' — the gimmick (random element + random payoff geometry every hit) is the entire identity, and unlike elemental-hit there is no meta endpoint where the build itself deletes the randomness. → _fix_ `new_door_rfc`
- **acceptance asserts:**
  - `primary_delivery_class == 'melee_arc'` [green]
  - `expresses: R-M7 player test FAILS: a fixed-element strike with one fixed secondary shape is` [red] · expected: RED until engine lane exists (routed to docket)
- **mapping deviation notes:** R-M7 player test FAILS: a fixed-element strike with one fixed secondary shape is 'not that build' — the gimmick (random element + random payoff geometry every hit) is the entire identity, and unlike elemental-hit there is no meta endpoint where the build itself deletes the randomness. Docket accrual filed to the RNG-element-pool family.

## poe1-wormblaster — Wormblaster `[class:record]`

- **grade / terminal:** `GAPPED` / `MAPPED_DOCKET`
- **element (court):** fire · _raw_: fire
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** 3.0-3.6;3.7-3.13 · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 2 · **dossier rows:** 6
- **citations (3):** [communal] pathofexile.com/forum · @Bramux#0742 · https://www.pathofexile.com/forum/view-thread/2130484; [communal] poecurrency.com · https://www.poecurrency.com/news/suzu520-s-herald-of-ice-wormblaster-build-for-poe-3-22; [communal] poedb.tw · @communal · https://poedb.tw/us/Cast_On_Critical_Strike_Support
- **t4 doors:** `PROXY_INVERSION`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Cast On Critical Strike (chassis)**: delivery=aura, range=self, count=1 · conf 0.75
  - `#1` **Barrage**: delivery=projectile, cadence=builder_spender, motion_signature=fan_spread, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Wormblaster: self buff aura identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [engine_inexpressible] R-M7 player test FAILS on the attested invariant: a CoC spellslinger without the worm supply 'is not Wormblaster' — the name IS the worms, and the boss-context fodder guarantee is the kit's stated point (mech_note). → _fix_ `new_door_rfc`
- **acceptance asserts:**
  - `primary_delivery_class == 'aura'` [green]
  - `expresses: R-M7 player test FAILS on the attested invariant: a CoC spellslinger without the` [red] · expected: RED until engine lane exists (routed to docket)
- **mapping deviation notes:** R-M7 player test FAILS on the attested invariant: a CoC spellslinger without the worm supply 'is not Wormblaster' — the name IS the worms, and the boss-context fodder guarantee is the kit's stated point (mech_note). Graded on the attested worm-fodder identity, not the unsupported skill pairing. Docket filed WITH the confidence caveat (heavy-strike-stun precedent: re-check the gap if a deeper dossier lands).

