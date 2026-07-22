# VDM-1 Compendium — mcd (5 kits)

> **Source:** `corpus.db` `kit_master` view (live-computed; cannot drift). **v1.1-verified** · db md5 `c7886250e92d80c9014890a58b0b0cc3` · generated 2026-07-19T20:04:46Z.
> Supersedes the four review rosters (which carry no citations). `kit_citations` is the sole citation authority; raw mobile-era descriptors are NOT exposed (provenance-only).

| grade | n | | verify (C/X/U total) | dossier rows | cited kits |
|---|---|---|---|---|---|
| E 0 · C 3 · A 1 · G 1 | 5 | | 15/0/0 | 30 | 5/5 |

## mcd-dynamo-torment — Dynamo Roll-Shoot (Standstill/Rolling Torment)

- **grade / terminal:** `CLOSE` / `MAPPED`
- **elements attested:** _(silent)_
- **ailments attested:** knockback
- **eras:** mcd-2022-final-v1.17 · **tier:** — · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 0 · **dossier rows:** 6
- **citations (3):** [communal] minecraft.wiki · https://minecraft.wiki/w/Dungeons:Dynamo; [official] minecraft.wiki · https://minecraft.wiki/w/Dungeons:1.4.3.0; [communal] minecraftdungeons.wiki.fextralife.com · https://minecraftdungeons.wiki.fextralife.com/Dynamo
- **deviations:** MCD enchantment-loadout identity lacks mastery/ascendancy layer; stack-unload approximates TEMPORAL_CHARGE but MCD has no on-kill propagation, chain, or node-tree depth. A player familiar with PoE Seismic Trap or D4 charge builders would recognize the core pattern but miss the enchantment-slot granularity.

## mcd-fireworks — Fireworks Arrow Artillery

- **grade / terminal:** `CLOSE` / `MAPPED`
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** mcd-2020-launch;mcd-2022-final-v1.17 · **tier:** — · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 0 · **dossier rows:** 6
- **citations (2):** [communal] minecraft.wiki · https://minecraft.wiki/w/Dungeons:Fireworks_Arrow; [communal] game8.co · https://game8.co/games/Minecraft-Dungeons/archives/289200
- **deviations:** No direct 'cooldown-as-resource' engine lane; CD reduction via armor enchant approximates resource_economy cadence_scale. Explosion AoE radius is not quantified in fetched text, so circle footprint is directionally correct but unscaled. Player familiar with ARPGs would recognize trap/artillery loop.

## mcd-soul — Soul Build (Corrupted Beacon economy)

- **grade / terminal:** `CLOSE` / `MAPPED`
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** mcd-2020-launch;mcd-2022-final-v1.17 · **tier:** — · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 0 · **dossier rows:** 6
- **citations (5):** [authored] windowscentral.com · https://www.windowscentral.com/minecraft-dungeons-soul-guide; [communal] minecraft.wiki · https://minecraft.wiki/w/Dungeons:Soul_Siphon; [communal] minecraft.wiki · https://minecraft.wiki/w/Dungeons:Soul; [communal] minecraft.wiki · https://minecraft.wiki/w/Dungeons:Corrupted_Beacon; [communal] minecraft.wiki · https://minecraft.wiki/w/Dungeons:Enigma_Resonator
- **deviations:** Soul resource has an accumulate-then-spend duality not captured by tick-cost alone; the beam is the drain and killing is the fill — the engine's PERSISTENCE_ENGINE_uptime approximates this but the two-phase loop (gather vs burn) is richer than a simple toggle. Player would feel the core beam+soul-economy identity.

## mcd-speed — Speed Build (Speedy Steve / Speedy Assassin)

- **grade / terminal:** `APPROX` / `MAPPED`
- **elements attested:** _(silent)_
- **ailments attested:** knockback
- **eras:** mcd-2020-launch;mcd-2022-final-v1.17 · **tier:** — · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 0 · **dossier rows:** 6
- **citations (3):** [authored] gamepur.com · https://www.gamepur.com/guides/best-minecraft-dungeons-builds; [authored] gamingscan.com · https://www.gamingscan.com/minecraft-dungeons-best-builds/; [communal] minecraft.wiki · https://minecraft.wiki/w/Dungeons:Boots_of_Swiftness
- **deviations:** Engine has no first-class movement-speed-as-identity lane: movement speed is a stat not a geometry or economy key in the engine. PHASE_MOMENTUM approximates the shape/phase-cycling identity but movement doubling + near-permanent uptime via CD cycling is a distinct pattern not native to the engine. A player familiar with this build would recognize the dash+melee combo but the core movement-speed experience has no engine analog.

## mcd-summoner — Companion / Beast Master Build

- **grade / terminal:** `GAPPED` / `MAPPED_DOCKET`
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** mcd-2020-launch;mcd-2022-final-v1.17 · **tier:** — · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 0 · **dossier rows:** 6
- **citations (5):** [communal] minecraft.wiki · https://minecraft.wiki/w/Dungeons:Golem_Kit; [communal] minecraft.wiki · https://minecraft.wiki/w/Dungeons:Tasty_Bone; [communal] minecraft.wiki · https://minecraft.wiki/w/Dungeons:Hunter%27s_Promise; [authored] windowscentral.com · https://www.windowscentral.com/minecraft-dungeons-guide-how-summon-all-companions-and-pets; [authored] thegamer.com · https://www.thegamer.com/minecraft-dungeons-best-builds/
- **deviations:** Pet-CORE: companions are the entire damage loop; player role is target marking and cooldown maintenance only. Engine has no companion-army-as-primary-damage lane at current scope. The skill shapes are individually mappable but the IDENTITY (zero player rotation, 3 cooldown-gated companions doing all damage) has no engine equivalent. Summoner-deferral docket class applies.

