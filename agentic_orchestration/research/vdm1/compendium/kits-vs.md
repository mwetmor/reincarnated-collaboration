# VDM-1 Compendium — vs (23 kits)

> **Source:** `corpus.db` `kit_master` view (live-computed; cannot drift). **v1.1-verified** · db md5 `50df15b776ad5b0da93fe90cdee1163d` · generated 2026-07-19T20:04:46Z.
> Supersedes the four review rosters (which carry no citations). `kit_citations` is the sole citation authority; raw mobile-era descriptors are NOT exposed (provenance-only).

| grade | n | | verify (C/X/U total) | dossier rows | cited kits |
|---|---|---|---|---|---|
| E 2 · C 12 · A 2 · G 7 | 23 | | 64/3/3 | 138 | 23/23 |

## vs-thousand-edge — Thousand Edge (Knife evo)

- **grade / terminal:** `EXACT` / `MAPPED`
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** vs-1.0-2022;vs-1.13-14-2025+ · **tier:** T3 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 0 · **dossier rows:** 6
- **citations (1):** [communal] vampire.survivors.wiki · https://vampire.survivors.wiki/w/Thousand_Edge

## vs-unholy-vespers — Unholy Vespers (King Bible evo)

- **grade / terminal:** `EXACT` / `MAPPED`
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** vs-1.0-2022;vs-1.13-14-2025+ · **tier:** T3 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 0 · **dossier rows:** 6
- **citations (1):** [communal] vampire.survivors.wiki · https://vampire.survivors.wiki/w/Unholy_Vespers

## vs-bloody-tear — Bloody Tear (Whip evo)

- **grade / terminal:** `CLOSE` / `MAPPED`
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** vs-1.0-2022;vs-dlc-era;vs-1.13-14-2025+ · **tier:** T3 · **lineage:** genre/whip
- **verify (C/X/U):** 3 / 0 / 0 · **dossier rows:** 6
- **citations (1):** [communal] vampire.survivors.wiki · https://vampire.survivors.wiki/w/Bloody_Tear
- **deviations:** Engine lacks the precise 'heal-on-crit' trigger chain natively; mapped as on-crit resource-fill which captures intent. Crit system approximated via proc_trigger_condition. No ailments in VS roguelite context.

## vs-death-spiral — Death Spiral (Axe evo)

- **grade / terminal:** `CLOSE` / `MAPPED`
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** vs-1.0-2022;vs-1.13-14-2025+ · **tier:** T3 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 0 · **dossier rows:** 6
- **citations (1):** [communal] vampire.survivors.wiki · https://vampire.survivors.wiki/w/Death_Spiral
- **deviations:** Engine orbit geometry maps the delivery well. Pool-limit saturation mechanic (50 active persistent projectiles) approximated via PERSISTENCE_ENGINE_saturation — engine has no direct pool-limit analog; fidelity note required.

## vs-fuwalafuwaloo — Fuwalafuwaloo (Vento Sacro+Bloody Tear union)

- **grade / terminal:** `CLOSE` / `MAPPED`
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** vs-base;vs-1.13-14-2025+ · **tier:** T3 · **lineage:** —
- **verify (C/X/U):** 2 / 1 / 0 · **dossier rows:** 6
- **citations (2):** [communal] vampire.survivors.wiki · https://vampire.survivors.wiki/w/Fuwalafuwaloo; [communal] vampire.survivors.wiki · https://vampire.survivors.wiki/w/Vento_Sacro
- **deviations:** Dual geometry (melee_arc + orbit simultaneously) is non-standard; engine skill chains are sequential not simultaneous — approximated as two skill entries. Movement-damage ramp approximated via MOMENTUM_CASCADE.

## vs-heaven-sword — Heaven Sword (Cross evo)

- **grade / terminal:** `CLOSE` / `MAPPED`
- **elements attested:** _(silent)_
- **ailments attested:** knockback
- **eras:** vs-1.0-2022;vs-1.13-14-2025+ · **tier:** T3 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 0 · **dossier rows:** 6
- **citations (1):** [communal] vampire.survivors.wiki · https://vampire.survivors.wiki/w/Heaven_Sword
- **deviations:** out-and-return boomerang double-pierce is approximated via placed_lane — engine does not natively distinguish outbound vs return-path pierce. Extreme knockback is attested and emitted. Minor fidelity loss on the double-traversal nuance.

## vs-hellfire — Hellfire (Fire Wand evo)

- **grade / terminal:** `CLOSE` / `MAPPED`
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** vs-1.0-2022 · **tier:** T3 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 0 · **dossier rows:** 6
- **citations (1):** [communal] vampire.survivors.wiki · https://vampire.survivors.wiki/w/Hellfire
- **deviations:** Identity maps well to placed_lane large-projectile delivery. Primary fidelity loss: fire+burn theme is visible to players but structurally absent from mapping per law. Engine representation is geometry-pure, missing the expected elemental feel.

## vs-holy-wand — Holy Wand (Magic Wand evo)

- **grade / terminal:** `CLOSE` / `MAPPED`
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** vs-1.0-2022;vs-1.13-14-2025+ · **tier:** T3 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 0 · **dossier rows:** 6
- **citations (1):** [communal] vampire.survivors.wiki · https://vampire.survivors.wiki/w/Holy_Wand
- **deviations:** single_target maps the non-pierce nearest-enemy delivery. No ailments, no element. Primary fidelity loss: holy name registers as holy-identity to players but is structurally absent per law.

## vs-la-borra — La Borra (Santa Water evo)

- **grade / terminal:** `CLOSE` / `MAPPED`
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** vs-1.0-2022;vs-1.13-14-2025+ · **tier:** T3 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 0 · **dossier rows:** 6
- **citations (1):** [communal] vampire.survivors.wiki · https://vampire.survivors.wiki/w/La_Borra
- **deviations:** Mobile growing puddle behavior (follow player, grow in travel) is approximated by ground_targeted_circle — engine has static circles, not self-relocating ones. Minor fidelity loss on the 'follows player' component.

## vs-phieraggi — Phieraggi (guns union)

- **grade / terminal:** `CLOSE` / `MAPPED`
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** vs-1.0-2022;vs-1.13-14-2025+ · **tier:** T3 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 0 · **dossier rows:** 6
- **citations (1):** [communal] vampire.survivors.wiki · https://vampire.survivors.wiki/w/Phieraggi
- **deviations:** CLOSE: engine orbit geometry captures rotating laser ring well. What source player misses: the revive-stock-as-power economy has no direct engine analog — the nearest T4 (RESOURCE_CONVERSION) approximates the conversion shape but not the stock-as-amplitude escalation.

## vs-runetracer-no-future — No Future (Runetracer evo)

- **grade / terminal:** `CLOSE` / `MAPPED`
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** vs-1.0-2022 · **tier:** T3 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 0 · **dossier rows:** 6
- **citations (1):** [communal] vampire.survivors.wiki · https://vampire.survivors.wiki/w/No_Future
- **deviations:** CLOSE: ricochet_bounce geometry and cascade T4 door capture the identity. What source player misses: the dual explosion trigger (wall bounce AND enemy hit) creates a richer cascade geometry than single-condition ricochet; Armor-as-explosion-scalar is an atypical stat routing not in the engine economy.

## vs-soul-eater — Soul Eater (Garlic evo)

- **grade / terminal:** `CLOSE` / `MAPPED`
- **elements attested:** _(silent)_
- **ailments attested:** drain
- **eras:** vs-1.0-2022 · **tier:** T3 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 0 · **dossier rows:** 6
- **citations (1):** [communal] vampire.survivors.wiki · https://vampire.survivors.wiki/w/Soul_Eater
- **deviations:** CLOSE: circle aura geometry and drain ailment capture the identity. What source player misses: the lifesteal-to-damage ramp mechanic (HP-healed as damage accumulator) has no direct engine analog; the cap-gated ramp shape (60 HP per +1 damage, cap +60) is more nuanced than the engine's ramp_per_s key.

## vs-thunder-loop — Thunder Loop (Lightning Ring evo)

- **grade / terminal:** `CLOSE` / `MAPPED`
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** vs-1.0-2022 · **tier:** T3 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 0 · **dossier rows:** 6
- **citations (1):** [communal] vampire.survivors.wiki · https://vampire.survivors.wiki/w/Thunder_Loop
- **deviations:** CLOSE: single_target geometry captures at-target random-strike delivery. What source player misses: the double-hit 'loop' mechanic (second strike same location with delay) has no engine analog — it reads as doubled hit-count, but the spatial lingering creates a zone-presence effect the engine cannot represent.

## vs-vandalier — Vandalier (Peachone+Ebony Wings union)

- **grade / terminal:** `CLOSE` / `MAPPED`
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** vs-1.0-2022 · **tier:** T3 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 0 · **dossier rows:** 6
- **citations (1):** [communal] vampire.survivors.wiki · https://vampire.survivors.wiki/w/Vandalier
- **deviations:** CLOSE: orbit + companion geometry captures the flying-bird-with-bomb-zones identity. What source player misses: slot liberation (freeing a weapon slot by fusing two weapons into one) is a VS-specific loadout-economy mechanic with no engine analog; the dual CW/CCW bomb zones create a symmetric orbit pattern the engine orbit geometry does not distinguish.

## vs-gorgeous-moon — Gorgeous Moon (Pentagram evo)

- **grade / terminal:** `APPROX` / `MAPPED`
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** vs-1.0-2022;vs-1.13-14-2025+ · **tier:** T3 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 0 · **dossier rows:** 6
- **citations (1):** [communal] vampire.survivors.wiki · https://vampire.survivors.wiki/w/Gorgeous_Moon
- **deviations:** Global-screen erasure with max-HP damage scalar and gem-vacuum combo has no close engine analog. ring geometry approximates the outward pulse shape but misses the 'global' scale and the harvest-integration vacuum mechanic. Player would miss the one-button screen-wipe + instant-harvest fusion identity.

## vs-je-ne-viv — Je-Ne-Viv (Insatiable)

- **grade / terminal:** `APPROX` / `MAPPED`
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** vs-dlc-era;vs-1.13-14-2025+ · **tier:** T3 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 0 · **dossier rows:** 6
- **citations (1):** [communal] vampire.survivors.wiki · https://vampire.survivors.wiki/w/Je-Ne-Viv
- **deviations:** Utility-stat-as-damage (Greed→damage, Magnet→range) has no engine analog for non-damage stats becoming damage scalars. World-eater transformation every 6th level has no engine lane. Player would miss the stat-conversion identity specifics.

## vs-big-trouser — Big Trouser (gold-farm archetype)

- **grade / terminal:** `GAPPED` / `MAPPED_DOCKET`
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** vs-base;vs-1.13-14-2025+ · **tier:** T3 · **lineage:** —
- **verify (C/X/U):** 1 / 2 / 0 · **dossier rows:** 6
- **citations (2):** [communal] vampire.survivors.wiki · https://vampire.survivors.wiki/w/Big_Trouser; [communal] rogueranker.com · https://rogueranker.com/trouser-vampire-survivors/
- **deviations:** No fixed skill loop or weapon identity — the build IS the Greed economy; no geometry, ailment, or element to map. Player experience = economy archetype, not a damage loadout. 'Not that build' criterion fully met.

## vs-gatti-amari — Gatti Amari (as drafted) `[NEGATIVE]`

- **grade / terminal:** `GAPPED` / `MAPPED_DOCKET`
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** vs-1.0-2022 · **tier:** T3 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 1 · **dossier rows:** 6
- **citations (1):** [communal] vampire.survivors.wiki · https://vampire.survivors.wiki/w/Gatti_Amari
- **deviations:** Pickup-consumption anti-harvest economy has no engine lane; friendly-fire mechanic has no engine lane. Wandering-proxy delivery differs from fixed-totem engine model. 'Not that build' criterion for the anti-harvest identity. Map the attested delivery shape; negative-canon story rides review book.

## vs-infinite-corridor-crimson-shroud — Infinite Corridor + Crimson Shroud (Death-kill tech)

- **grade / terminal:** `GAPPED` / `MAPPED_DOCKET`
- **elements attested:** _(silent)_
- **ailments attested:** freeze
- **eras:** vs-1.0-2022;vs-1.13-14-2025+ · **tier:** T3 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 0 · **dossier rows:** 6
- **citations (2):** [communal] vampire.survivors.wiki · https://vampire.survivors.wiki/w/Infinite_Corridor; [communal] vampire.survivors.wiki · https://vampire.survivors.wiki/w/Crimson_Shroud
- **deviations:** HP-halving screen effect and 10-damage-cap mechanic have no engine analogs. The dual-weapon Reaper-kill tech is a structural gap — 'not that build.' freeze emission is correct and grounded. DEFENSIVE_TRADEOFF + RETRIBUTION_ENGINE T4 doors approximate the identity direction.

## vs-out-of-bounds-freeze — Out of Bounds freeze build

- **grade / terminal:** `GAPPED` / `MAPPED_DOCKET`
- **elements attested:** _(silent)_
- **ailments attested:** freeze
- **eras:** vs-0.6.1-arcana-2022;vs-1.13-14-2025+ · **tier:** T3 · **lineage:** —
- **verify (C/X/U):** 2 / 0 / 1 · **dossier rows:** 6
- **citations (1):** [communal] vampire.survivors.wiki · https://vampire.survivors.wiki/w/Out_of_Bounds
- **deviations:** GAPPED: the identity is a passive arcana modifier reshaping a freeze-weapon loadout — no player rotation exists. Engine cannot represent arcana-slot investment + weapon-loadout fusion. 'Not that build.'

## vs-queen-sigma — Queen Sigma

- **grade / terminal:** `GAPPED` / `MAPPED_DOCKET`
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** vs-0.11.0-2022;vs-dlc-era;vs-1.13-14-2025+ · **tier:** T3 · **lineage:** —
- **verify (C/X/U):** 2 / 0 / 1 · **dossier rows:** 6
- **citations (1):** [communal] vampire.survivors.wiki · https://vampire.survivors.wiki/w/Queen_Sigma
- **deviations:** GAPPED: the identity is a collection-completion gate + infinite per-level compounding character — no rotation, no skill sequence. Engine cannot represent collection-completion unlock or unbounded per-level Might/Growth escalation. 'Not that build.'

## vs-red-death — Red Death / Mask of the Red Death

- **grade / terminal:** `GAPPED` / `MAPPED_DOCKET`
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** vs-1.0-2022;vs-1.13-14-2025+ · **tier:** T3 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 0 · **dossier rows:** 6
- **citations (1):** [communal] vampire.survivors.wiki · https://vampire.survivors.wiki/w/Red_Death
- **deviations:** GAPPED: identity is a movement-speed + orbit-weapon character with no skill rotation. Engine cannot represent the loadout-identity structure. 'Not that build.'

## vs-vlad-dracula — Vlad Tepes Dracula

- **grade / terminal:** `GAPPED` / `MAPPED_DOCKET`
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** vs-dlc-era;vs-1.13-14-2025+ · **tier:** T3 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 0 · **dossier rows:** 6
- **citations (1):** [communal] vampire.survivors.wiki · https://vampire.survivors.wiki/w/Vlad_Tepes_Dracula
- **deviations:** GAPPED: character identity is a damage-cap survivability + Curse-inversion-as-Might economy — no rotation; engine cannot represent damage-cap-at-10 mechanic or the Curse-as-Might inversion. Wine Glass delivery geometry unattested in fetched text. 'Not that build.'

