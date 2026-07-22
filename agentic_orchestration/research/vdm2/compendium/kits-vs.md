# VDM-2 Compendium — vs (23 kits)

> **Source:** `corpus.db` `kit_master` view (574) ENRICHED live with the six VDM-2 side-car blocks + two registries (render-layer joins; DB never mutated). **v2.0** · db md5 `bebc933b0bf9bcab5988bbc16bcc55b4` · generated 2026-07-22T09:46:42Z.
> `court` is the reconciled element court (enum-checked); `original_element` carries raw provenance. Raw mobile-era descriptors (`elem_raw`) are NOT exposed (provenance-only). `kit_citations` is the sole citation authority.

| grade | n | verify (C/X/U) | dossier | cited | geom-bands | hooks |
|---|---|---|---|---|---|---|
| E 2 · C 12 · A 2 · G 7 | 23 | 64/3/3 | 138 | 23/23 | 0 | 0 |

## vs-thousand-edge — Thousand Edge (Knife evo) `[class:annex]`

- **grade / terminal:** `EXACT` / `MAPPED`
- **element (court):** _(unassigned)_ · _raw_: n/a
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** vs-1.0-2022;vs-1.13-14-2025+ · **tier:** T3 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 0 · **dossier rows:** 6
- **citations (1):** [communal] vampire.survivors.wiki · https://vampire.survivors.wiki/w/Thousand_Edge
- **t4 doors:** `GEOMETRY_INVERSION`

## vs-unholy-vespers — Unholy Vespers (King Bible evo) `[class:annex]`

- **grade / terminal:** `EXACT` / `MAPPED`
- **element (court):** _(unassigned)_ · _raw_: n/a
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** vs-1.0-2022;vs-1.13-14-2025+ · **tier:** T3 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 0 · **dossier rows:** 6
- **citations (1):** [communal] vampire.survivors.wiki · https://vampire.survivors.wiki/w/Unholy_Vespers
- **t4 doors:** `PERSISTENCE_ENGINE_uptime`

## vs-bloody-tear — Bloody Tear (Whip evo) `[class:annex]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** _(unassigned)_ · _raw_: n/a
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** vs-1.0-2022;vs-dlc-era;vs-1.13-14-2025+ · **tier:** T3 · **lineage:** genre/whip
- **verify (C/X/U):** 3 / 0 / 0 · **dossier rows:** 6
- **citations (1):** [communal] vampire.survivors.wiki · https://vampire.survivors.wiki/w/Bloody_Tear
- **t4 doors:** `PERSISTENCE_ENGINE_uptime`
- **mapping deviation notes:** Engine lacks the precise 'heal-on-crit' trigger chain natively; mapped as on-crit resource-fill which captures intent. Crit system approximated via proc_trigger_condition. No ailments in VS roguelite context.

## vs-death-spiral — Death Spiral (Axe evo) `[class:annex]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** _(unassigned)_ · _raw_: n/a
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** vs-1.0-2022;vs-1.13-14-2025+ · **tier:** T3 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 0 · **dossier rows:** 6
- **citations (1):** [communal] vampire.survivors.wiki · https://vampire.survivors.wiki/w/Death_Spiral
- **t4 doors:** `ZONE_CONTROL`, `PERSISTENCE_ENGINE_saturation`
- **mapping deviation notes:** Engine orbit geometry maps the delivery well. Pool-limit saturation mechanic (50 active persistent projectiles) approximated via PERSISTENCE_ENGINE_saturation — engine has no direct pool-limit analog; fidelity note required.

## vs-fuwalafuwaloo — Fuwalafuwaloo (Vento Sacro+Bloody Tear union) `[class:annex]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** _(unassigned)_ · _raw_: n/a
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** vs-base;vs-1.13-14-2025+ · **tier:** T3 · **lineage:** —
- **verify (C/X/U):** 2 / 1 / 0 · **dossier rows:** 6
- **citations (2):** [communal] vampire.survivors.wiki · https://vampire.survivors.wiki/w/Fuwalafuwaloo; [communal] vampire.survivors.wiki · https://vampire.survivors.wiki/w/Vento_Sacro
- **t4 doors:** `MOMENTUM_CASCADE`, `PERSISTENCE_ENGINE_uptime`
- **mapping deviation notes:** Dual geometry (melee_arc + orbit simultaneously) is non-standard; engine skill chains are sequential not simultaneous — approximated as two skill entries. Movement-damage ramp approximated via MOMENTUM_CASCADE.

## vs-heaven-sword — Heaven Sword (Cross evo) `[class:annex]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** _(unassigned)_ · _raw_: n/a
- **elements attested:** _(silent)_
- **ailments attested:** knockback
- **eras:** vs-1.0-2022;vs-1.13-14-2025+ · **tier:** T3 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 0 · **dossier rows:** 6
- **citations (1):** [communal] vampire.survivors.wiki · https://vampire.survivors.wiki/w/Heaven_Sword
- **t4 doors:** `GEOMETRY_INVERSION`
- **mapping deviation notes:** out-and-return boomerang double-pierce is approximated via placed_lane — engine does not natively distinguish outbound vs return-path pierce. Extreme knockback is attested and emitted. Minor fidelity loss on the double-traversal nuance.

## vs-hellfire — Hellfire (Fire Wand evo) `[class:annex]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** _(unassigned)_ · _raw_: n/a
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** vs-1.0-2022 · **tier:** T3 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 0 · **dossier rows:** 6
- **citations (1):** [communal] vampire.survivors.wiki · https://vampire.survivors.wiki/w/Hellfire
- **t4 doors:** `ZONE_CONTROL`
- **mapping deviation notes:** Identity maps well to placed_lane large-projectile delivery. Primary fidelity loss: fire+burn theme is visible to players but structurally absent from mapping per law. Engine representation is geometry-pure, missing the expected elemental feel.

## vs-holy-wand — Holy Wand (Magic Wand evo) `[class:annex]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** _(unassigned)_ · _raw_: n/a
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** vs-1.0-2022;vs-1.13-14-2025+ · **tier:** T3 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 0 · **dossier rows:** 6
- **citations (1):** [communal] vampire.survivors.wiki · https://vampire.survivors.wiki/w/Holy_Wand
- **t4 doors:** `PERSISTENCE_ENGINE_saturation`
- **mapping deviation notes:** single_target maps the non-pierce nearest-enemy delivery. No ailments, no element. Primary fidelity loss: holy name registers as holy-identity to players but is structurally absent per law.

## vs-la-borra — La Borra (Santa Water evo) `[class:annex]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** _(unassigned)_ · _raw_: n/a
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** vs-1.0-2022;vs-1.13-14-2025+ · **tier:** T3 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 0 · **dossier rows:** 6
- **citations (1):** [communal] vampire.survivors.wiki · https://vampire.survivors.wiki/w/La_Borra
- **t4 doors:** `ZONE_CONTROL`, `PERSISTENCE_ENGINE_uptime`
- **mapping deviation notes:** Mobile growing puddle behavior (follow player, grow in travel) is approximated by ground_targeted_circle — engine has static circles, not self-relocating ones. Minor fidelity loss on the 'follows player' component.

## vs-phieraggi — Phieraggi (guns union) `[class:annex]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** _(unassigned)_ · _raw_: n/a
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** vs-1.0-2022;vs-1.13-14-2025+ · **tier:** T3 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 0 · **dossier rows:** 6
- **citations (1):** [communal] vampire.survivors.wiki · https://vampire.survivors.wiki/w/Phieraggi
- **t4 doors:** `RESOURCE_CONVERSION`
- **mapping deviation notes:** CLOSE: engine orbit geometry captures rotating laser ring well. What source player misses: the revive-stock-as-power economy has no direct engine analog — the nearest T4 (RESOURCE_CONVERSION) approximates the conversion shape but not the stock-as-amplitude escalation.

## vs-runetracer-no-future — No Future (Runetracer evo) `[class:annex]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** _(unassigned)_ · _raw_: n/a
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** vs-1.0-2022 · **tier:** T3 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 0 · **dossier rows:** 6
- **citations (1):** [communal] vampire.survivors.wiki · https://vampire.survivors.wiki/w/No_Future
- **t4 doors:** `GEOMETRY_PROPAGATION_cascade`
- **mapping deviation notes:** CLOSE: ricochet_bounce geometry and cascade T4 door capture the identity. What source player misses: the dual explosion trigger (wall bounce AND enemy hit) creates a richer cascade geometry than single-condition ricochet; Armor-as-explosion-scalar is an atypical stat routing not in the engine economy.

## vs-soul-eater — Soul Eater (Garlic evo) `[class:annex]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** _(unassigned)_ · _raw_: n/a
- **elements attested:** _(silent)_
- **ailments attested:** drain
- **eras:** vs-1.0-2022 · **tier:** T3 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 0 · **dossier rows:** 6
- **citations (1):** [communal] vampire.survivors.wiki · https://vampire.survivors.wiki/w/Soul_Eater
- **t4 doors:** `PERSISTENCE_ENGINE_saturation`
- **mapping deviation notes:** CLOSE: circle aura geometry and drain ailment capture the identity. What source player misses: the lifesteal-to-damage ramp mechanic (HP-healed as damage accumulator) has no direct engine analog; the cap-gated ramp shape (60 HP per +1 damage, cap +60) is more nuanced than the engine's ramp_per_s key.

## vs-thunder-loop — Thunder Loop (Lightning Ring evo) `[class:annex]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** _(unassigned)_ · _raw_: n/a
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** vs-1.0-2022 · **tier:** T3 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 0 · **dossier rows:** 6
- **citations (1):** [communal] vampire.survivors.wiki · https://vampire.survivors.wiki/w/Thunder_Loop
- **mapping deviation notes:** CLOSE: single_target geometry captures at-target random-strike delivery. What source player misses: the double-hit 'loop' mechanic (second strike same location with delay) has no engine analog — it reads as doubled hit-count, but the spatial lingering creates a zone-presence effect the engine cannot represent.

## vs-vandalier — Vandalier (Peachone+Ebony Wings union) `[class:annex]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** _(unassigned)_ · _raw_: n/a
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** vs-1.0-2022 · **tier:** T3 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 0 · **dossier rows:** 6
- **citations (1):** [communal] vampire.survivors.wiki · https://vampire.survivors.wiki/w/Vandalier
- **t4 doors:** `DUAL_PROXY`
- **mapping deviation notes:** CLOSE: orbit + companion geometry captures the flying-bird-with-bomb-zones identity. What source player misses: slot liberation (freeing a weapon slot by fusing two weapons into one) is a VS-specific loadout-economy mechanic with no engine analog; the dual CW/CCW bomb zones create a symmetric orbit pattern the engine orbit geometry does not distinguish.

## vs-gorgeous-moon — Gorgeous Moon (Pentagram evo) `[class:annex]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** _(unassigned)_ · _raw_: n/a
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** vs-1.0-2022;vs-1.13-14-2025+ · **tier:** T3 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 0 · **dossier rows:** 6
- **citations (1):** [communal] vampire.survivors.wiki · https://vampire.survivors.wiki/w/Gorgeous_Moon
- **t4 doors:** `GEOMETRY_PROPAGATION_cascade`
- **mapping deviation notes:** Global-screen erasure with max-HP damage scalar and gem-vacuum combo has no close engine analog. ring geometry approximates the outward pulse shape but misses the 'global' scale and the harvest-integration vacuum mechanic. Player would miss the one-button screen-wipe + instant-harvest fusion identity.

## vs-je-ne-viv — Je-Ne-Viv (Insatiable) `[class:annex]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** _(unassigned)_ · _raw_: n/a
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** vs-dlc-era;vs-1.13-14-2025+ · **tier:** T3 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 0 · **dossier rows:** 6
- **citations (1):** [communal] vampire.survivors.wiki · https://vampire.survivors.wiki/w/Je-Ne-Viv
- **t4 doors:** `NETWORK_AMPLIFIER`, `RESOURCE_CONVERSION`
- **mapping deviation notes:** Utility-stat-as-damage (Greed→damage, Magnet→range) has no engine analog for non-damage stats becoming damage scalars. World-eater transformation every 6th level has no engine lane. Player would miss the stat-conversion identity specifics.

## vs-big-trouser — Big Trouser (gold-farm archetype) `[class:annex]`

- **grade / terminal:** `GAPPED` / `MAPPED_DOCKET`
- **element (court):** _(unassigned)_ · _raw_: n/a
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** vs-base;vs-1.13-14-2025+ · **tier:** T3 · **lineage:** —
- **verify (C/X/U):** 1 / 2 / 0 · **dossier rows:** 6
- **citations (2):** [communal] vampire.survivors.wiki · https://vampire.survivors.wiki/w/Big_Trouser; [communal] rogueranker.com · https://rogueranker.com/trouser-vampire-survivors/
- **mapping deviation notes:** No fixed skill loop or weapon identity — the build IS the Greed economy; no geometry, ailment, or element to map. Player experience = economy archetype, not a damage loadout. 'Not that build' criterion fully met.

## vs-gatti-amari — Gatti Amari (as drafted) `[NEGATIVE, class:annex]`

- **grade / terminal:** `GAPPED` / `MAPPED_DOCKET`
- **element (court):** _(unassigned)_ · _raw_: n/a
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** vs-1.0-2022 · **tier:** T3 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 1 · **dossier rows:** 6
- **citations (1):** [communal] vampire.survivors.wiki · https://vampire.survivors.wiki/w/Gatti_Amari
- **mapping deviation notes:** Pickup-consumption anti-harvest economy has no engine lane; friendly-fire mechanic has no engine lane. Wandering-proxy delivery differs from fixed-totem engine model. 'Not that build' criterion for the anti-harvest identity. Map the attested delivery shape; negative-canon story rides review book.

## vs-infinite-corridor-crimson-shroud — Infinite Corridor + Crimson Shroud (Death-kill tech) `[class:annex]`

- **grade / terminal:** `GAPPED` / `MAPPED_DOCKET`
- **element (court):** _(unassigned)_ · _raw_: n/a
- **elements attested:** _(silent)_
- **ailments attested:** freeze
- **eras:** vs-1.0-2022;vs-1.13-14-2025+ · **tier:** T3 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 0 · **dossier rows:** 6
- **citations (2):** [communal] vampire.survivors.wiki · https://vampire.survivors.wiki/w/Infinite_Corridor; [communal] vampire.survivors.wiki · https://vampire.survivors.wiki/w/Crimson_Shroud
- **t4 doors:** `DEFENSIVE_TRADEOFF`, `RETRIBUTION_ENGINE`
- **mapping deviation notes:** HP-halving screen effect and 10-damage-cap mechanic have no engine analogs. The dual-weapon Reaper-kill tech is a structural gap — 'not that build.' freeze emission is correct and grounded. DEFENSIVE_TRADEOFF + RETRIBUTION_ENGINE T4 doors approximate the identity direction.

## vs-out-of-bounds-freeze — Out of Bounds freeze build `[class:annex]`

- **grade / terminal:** `GAPPED` / `MAPPED_DOCKET`
- **element (court):** _(unassigned)_ · _raw_: n/a
- **elements attested:** _(silent)_
- **ailments attested:** freeze
- **eras:** vs-0.6.1-arcana-2022;vs-1.13-14-2025+ · **tier:** T3 · **lineage:** —
- **verify (C/X/U):** 2 / 0 / 1 · **dossier rows:** 6
- **citations (1):** [communal] vampire.survivors.wiki · https://vampire.survivors.wiki/w/Out_of_Bounds
- **t4 doors:** `PERSISTENCE_ENGINE_saturation`
- **mapping deviation notes:** GAPPED: the identity is a passive arcana modifier reshaping a freeze-weapon loadout — no player rotation exists. Engine cannot represent arcana-slot investment + weapon-loadout fusion. 'Not that build.'

## vs-queen-sigma — Queen Sigma `[class:annex]`

- **grade / terminal:** `GAPPED` / `MAPPED_DOCKET`
- **element (court):** _(unassigned)_ · _raw_: n/a
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** vs-0.11.0-2022;vs-dlc-era;vs-1.13-14-2025+ · **tier:** T3 · **lineage:** —
- **verify (C/X/U):** 2 / 0 / 1 · **dossier rows:** 6
- **citations (1):** [communal] vampire.survivors.wiki · https://vampire.survivors.wiki/w/Queen_Sigma
- **t4 doors:** `MOMENTUM_CASCADE`
- **mapping deviation notes:** GAPPED: the identity is a collection-completion gate + infinite per-level compounding character — no rotation, no skill sequence. Engine cannot represent collection-completion unlock or unbounded per-level Might/Growth escalation. 'Not that build.'

## vs-red-death — Red Death / Mask of the Red Death `[class:annex]`

- **grade / terminal:** `GAPPED` / `MAPPED_DOCKET`
- **element (court):** _(unassigned)_ · _raw_: n/a
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** vs-1.0-2022;vs-1.13-14-2025+ · **tier:** T3 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 0 · **dossier rows:** 6
- **citations (1):** [communal] vampire.survivors.wiki · https://vampire.survivors.wiki/w/Red_Death
- **t4 doors:** `PHASE_MOMENTUM`
- **mapping deviation notes:** GAPPED: identity is a movement-speed + orbit-weapon character with no skill rotation. Engine cannot represent the loadout-identity structure. 'Not that build.'

## vs-vlad-dracula — Vlad Tepes Dracula `[class:annex]`

- **grade / terminal:** `GAPPED` / `MAPPED_DOCKET`
- **element (court):** _(unassigned)_ · _raw_: n/a
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** vs-dlc-era;vs-1.13-14-2025+ · **tier:** T3 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 0 · **dossier rows:** 6
- **citations (1):** [communal] vampire.survivors.wiki · https://vampire.survivors.wiki/w/Vlad_Tepes_Dracula
- **t4 doors:** `DEFENSIVE_TRADEOFF`
- **mapping deviation notes:** GAPPED: character identity is a damage-cap survivability + Curse-inversion-as-Might economy — no rotation; engine cannot represent damage-cap-at-10 mechanic or the Curse-as-Might inversion. Wine Glass delivery geometry unattested in fetched text. 'Not that build.'

