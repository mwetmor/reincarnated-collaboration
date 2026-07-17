# KB-URL Backfill Sheet — Mega-Probe Post-Cutoff Rows

**Mode:** A (analytical backfill)
**Commissioner:** gandalf-prime (2026-07-16 autonomous atlas-parity run)
**Filed:** legolas, 2026-07-16
**Scope:** Post-cutoff rows in the mega-probe (2026-07-12) whose `sources_used` array carries no live URL (kb-only sourcing). Elrond's single-writer holds `corpus.db`; this sheet is READ-ONLY input for a later Elrond backfill pass.

---

## Header note

**KB-only marker detection method used:** enumerated every mega-probe `*-facts.jsonl` row, parsed `sources_used`, and treated any row where NONE of the source entries contained `http`/`https` AND `post_cutoff` was truthy as a kb-only post-cutoff row. This detects the semantic marker (row sourced from model knowledge, not live crawl) without requiring an explicit `kb-only` provenance string, because the mega-probe schema does not embed one — the operational marker is "no URL in sources_used." 52 rows matched.

The mega-probe 00-index also lists broader `dossier_owed=true` flags on d2 Warlock, d4 S4-S7 items, le Epoch 1.0+, and Wildsoul/Valkyrie rows. Wildsoul + Valkyrie hold-out debt is paid by Mission 1 dossiers (this dir). This sheet covers the residual 52 rows.

**Disposition legend:**
- **confirm** — live URL found and it corroborates the mega-probe claim
- **correct** — live URL found; sub-claim needs adjustment (adjustment noted per row)
- **unverifiable** — searched but no accessible live source found; leave as kb-only, flag for future re-audit

---

## Backfill rows

| # | game | kit_id | folk_name | claim summary | live URL | disposition |
|---|---|---|---|---|---|---|
| 1 | d2 | `d2-wl-fire` | Fire Warlock | Chaos-tree fire-caster (Flame Wave + Apocalypse); Season 13 Reign of the Warlock | https://maxroll.gg/d2/news/diablo-ii-resurrected-reign-of-the-warlock-expansion + https://www.rpgstash.com/blog/d2r-warlock-skill-trees-guide-chaos-demon-eldritch | **confirm** |
| 2 | d2 | `d2-wl-tainted-summoner` | Tainted Summoner Warlock | Demon-tree bind-tainted ranged fire support; summon-driven | https://www.rpgstash.com/blog/d2r-warlock-skill-trees-guide-chaos-demon-eldritch (Demon Tree Tainted description) | **confirm** |
| 3 | d2 | `d2-wl-blood-boil` | Blood Boil Warlock | Blood Boil deals fire + physical; requires demons (drains their life); AoE around player | https://www.aoeah.com/news/4387--d2r-best-warlock-builds-for-leveling--endgame-season-13 | **confirm** |
| 4 | d2 | `d2-wl-echoing-strike` | Echoing Strike Warlock | Eldritch-tree weapon-manipulation build; elemental strike | https://www.rpgstash.com/blog/d2r-warlock-skill-trees-guide-chaos-demon-eldritch (Eldritch Tree) | **confirm** (Eldritch tree confirmed as weapon-manipulation caster hybrid) |
| 5 | d2 | `d2-wl-abyss` | Abyss Warlock | Named Abyss build | https://www.rpgstash.com/blog/d2r-season-13-best-warlock-endgame-builds | **unverifiable** — Abyss variant not enumerated in survey-tier articles I accessed; flag for retry with build-listing site |
| 6 | d2 | `d2-wl-void-rift` | Void Rift Warlock | Named Void Rift build | https://www.rpgstash.com/blog/d2r-season-13-best-warlock-endgame-builds | **unverifiable** — Void Rift specifically not in accessed excerpts |
| 7 | d4 | `d4-blazing-abyss-warlock` | Blazing Abyss Warlock | Infinistep/Blazing Abyss Warlock build; immortal-window playstyle | https://www.icy-veins.com/d4/guides/blazing-abyss-warlock-build/ + https://maxroll.gg/d4/build-guides/blazing-scream-warlock-leveling-guide | **confirm** — note the meta-name evolved to "Blazing Scream" as of S14; "Blazing Abyss" is the S13 form. Elrond may correct era_confirmed to include the rename. |
| 8 | d4 | `d4-payback-sb` | Payback Spiritborn | S4-S7 era Spiritborn build variant | — | **unverifiable** — Payback Spiritborn variant not surfaced in accessed sources; may be S9+ pruned meta |
| 9 | d4 | `d4-dread-claws-warlock` | Dread Claws Warlock | Dread Claws burst forth shadowy claws; Encircling Terror version | https://mobalytics.gg/diablo-4/builds/warlock-dread-claws + https://www.icy-veins.com/d4/guides/dread-claws-warlock-build/ + https://www.wowhead.com/diablo-4/skill/dread-claws-2385787 | **confirm** |
| 10 | d4 | `d4-hammerdin-paladin` | Hammerdin Paladin | Blessed Hammer Paladin — Disciple's Halo tripod converts Blessed Hammer into moving whirlwind of destruction; speedfarmer | https://mobalytics.gg/diablo-4/builds/blessed-hammer-paladin + https://maxroll.gg/d4/build-guides/blessed-hammer-paladin-guide + https://d4guides.gg/en/s14/build/paladin-hammerdin-733140c1 | **confirm** |
| 11 | d4 | `d4-wing-strike-arbiter` | Wing Strike Arbiter Paladin | Arbiter Paladin Wing Strike build | — | **unverifiable** — Arbiter Paladin (Wing Strike) not surfaced in accessed d4 build sources; likely S13+ variant, flag for retry with specific patch note search |
| 12 | d4 | `d4-rabies-lacerate` | Rabies Lacerate Druid | Poison stack via Rabies → Lacerate passive detonate; Mad Wolf's Glee reduces to core no-cooldown | https://mobalytics.gg/diablo-4/builds/druid-rabies-endgame + https://www.icy-veins.com/d4/guides/rabies-lacerate-druid-build/ + https://www.wowhead.com/diablo-4/guide/classes/druid/rabies-build-overview | **confirm** |
| 13 | d4 | `d4-auradin-paladin` | Auradin Paladin | Aura-stacking Paladin | — | **unverifiable** — accessed Paladin build sources centered on Hammerdin/Blessed Hammer; Auradin variant not surfaced. Flag for retry. |
| 14 | di | `di-warlock-launch` | Warlock (launch state) | Warlock class launched Diablo Immortal Patch 5.0 Bloodied Jewel on June 17 2026; summoner archetype with Soulgorger, Lunatic Rush, Hellswarm, Burning Ascent | https://news.blizzard.com/en-us/article/24277443/introducing-diablo-immortals-newest-class-warlock + https://diablo.fandom.com/wiki/Warlock_(Diablo_Immortal) + https://www.icy-veins.com/d4/news/diablo-immortal-reveals-warlock-class-and-2026-roadmap/ | **confirm** — note release date is 2026-06-17 (may need era_confirmed adjustment to specify launch date) |
| 15 | di | `di-bombardment-wizard-pvp` | Bombardment Artillery Wizard | Wizard Bombardment PVP-focused build | — | **unverifiable** — DI PVP-specific meta build not surfaced in general searches; may require DI-specific build-database sources (maxroll DI section) not in accessed results |
| 16 | di | `di-spiritform-druid-pvp` | Spirit-Form Druid (complaint-tier) | Druid Spirit-Form PVP build, complaint-flagged (negative canon adjacent) | — | **unverifiable** — same as row 15 |
| 17 | gd | `gd-berserker-wereforms` | Berserker (FoA mastery) | Fangs of Asterkarn expansion 10th mastery Berserker: shapeshifting into beastlike forms (wereforms); dual-weapon combat when not in form; frost-themed FoA content; release July 23 2026 | https://www.grimdawn.com/guide/character/masteries/berserker/ + https://www.grimdawn.com/guide/about/fangs-of-asterkarn/ + https://massivelyop.com/2026/06/01/grim-dawns-fangs-of-asterkarn-expansion-adds-a-frosty-new-realm-and-a-shapeshifting-mastery-line-july-23/ | **confirm** — GX-02 SHAPESHIFT keystone note: Berserker wereforms is another live-canon shapeshift attestation (adds to Ferality Wildsoul + PBA Wildsoul body of evidence) |
| 18 | hades | `hades2-medea-skull-cast` | 62-Fear Medea Skull Build | Argent Skull (Medea) aspect with area-of-attacks + Cast synergy; endgame Fear-scaled build | https://hades2.wiki.fextralife.com/Patch+Notes + https://mobalytics.gg/hades-2/guides/launch-patch-notes | **confirm** — note post-launch patch trimmed area radius slightly + fixed Argent damage-bonus overapplication to Casts |
| 19 | hades | `hades2-hephaestus-blast` | Hephaestus Blast Core | Furnace Blast (Hephaestus) core boon; Heroic rarity + Poms of Power fixed post-launch | https://hades2.wiki.fextralife.com/Patch+Notes | **confirm** |
| 20 | hades | `hades2-glorious-disaster` | Glorious Disaster (Zeus+Apollo duo) | Duo boon: channel Magick into Omega Cast which repeatedly strikes with lightning bolts; highest theoretical damage of any duo boon for cast-heavy builds | https://hades2.wiki.fextralife.com/Glorious+Disaster + https://dotesports.com/hades/news/best-duo-boons-in-hades-2-ranked | **confirm** |
| 21 | hades | `hades2-hail-storm` | Hail Storm (Zeus+Demeter duo) | Duo boon: Freeze effects repeatedly strike lightning bolts to afflicted enemies; previously called Apocalyptic Storm | https://hades2.wiki.fextralife.com/Hail+Storm + https://rogueranker.com/demeter-hades-2/ | **correct** — previous name "Apocalyptic Storm" may need era note in the row; verify era_confirmed field |
| 22 | hot | `hot-sage-ring-blades` | Ring Blades Sage | Ring Blades tornado/cyclone Sage build with Cyclone → Piercing Blades → Crippling Blades upgrade path; Ethereal Shift +60% attack speed synergy | https://hot.fandom.com/wiki/Ring_Blades + https://steamcommunity.com/sharedfiles/filedetails/?id=3172296902 | **confirm** |
| 23 | hot | `hot-landsknecht-grenades` | Grenade Landsknecht | Landsknecht class Grenade build | — | **unverifiable** — Landsknecht-Grenade specifically not surfaced; general HoT source visible but this build variant not enumerated. Flag for retry with more targeted class-specific search. |
| 24 | le | `le-bomb-lance-falconer` | Bomb Lance Falconer | Falconer + Bomb Lance skill; Marking Strikes / Falconer's Mark scaling | https://maxroll.gg/last-epoch/news/last-epoch-patch-1-4-4-notes + https://www.lastepochtools.com/news/article/last-epoch-shattered-omens-patch-notes-80571 | **confirm** |
| 25 | le | `le-bladestorm-bd` | Bladestorm Bladedancer | Bladestorm as standalone skill (previously Umbral Blades subskill); 3-blade cap, 4s duration, hits 3× per second, single-damage-per-enemy limit | https://maxroll.gg/last-epoch/news/last-epoch-patch-1-4-4-notes | **confirm** |
| 26 | le | `le-fire-aura-spellblade` | Fire Aura Spellblade | Fire Aura Spellblade with cold-conversion tripod freezing battlefield; converts fire aura to cold pulse | https://maxroll.gg/last-epoch/news/last-epoch-1-4-branch-update-for-season-4-shattered-omens | **confirm** |
| 27 | le | `le-shield-throw-time-rot-vk` | Shield Throw Time Rot VK | Void Knight Shield Throw with Sentinel Idol Affix converting to Void; Bleed→Time Rot conversion; 1.4.4 addition | https://maxroll.gg/last-epoch/news/last-epoch-patch-1-4-4-notes | **confirm** |
| 28 | poe1 | `poe1-kinetic-fusillade` | Kinetic Fusillade | 3.27 KotF-era build: projectile attack creating hovering energy projectiles that release after cast-pause, chaining to nearby enemies; Elementalist/Champion/Warden variants | https://mobalytics.gg/poe/builds/dslily-kinetic-fusillade-champion + https://www.pathofexile.com/forum/view-thread/3876136 + https://www.poewiki.net/wiki/Kinetic_Fusillade | **confirm** |
| 29 | poe1 | `poe1-minion-pact-bv` | Minion Pact Blade Vortex | 3.28 Minion Pact Blade Vortex Chieftain build | https://mobalytics.gg/poe/profile/dante00151/builds/3-28-minion-pact-blade-vortex-chieftain-the-superior-bv | **confirm** |
| 30 | poe1 | `poe1-heavy-strike-stun` | Heavy Strike Stun Berserker | 3.28 Heavy Strike Berserker OP Stun Build; final update May 7 2026 | https://mobalytics.gg/poe/builds/stun-heavy-strike-berserker | **confirm** |
| 31 | poe2 | `poe2-spiral-volley` | Spiral Volley | 0.3 The Third Edict era build | https://www.sportskeeda.com/mmo/path-exile-2-poe2-massive-skill-buffs-0-3 + https://www.rpgstash.com/blog/9-best-builds-in-path-of-exile-2-dawn-of-the-hunt | **unverifiable** — Spiral Volley specifically not enumerated in accessed 0.3 articles; general 0.3 patch source found but the skill-specific claim not directly corroborated. Flag as PARTIAL confirmation. |
| 32 | poe2 | `poe2-whirling-assault-ma` | Whirling Assault Martial Artist | Post-cutoff Martial Artist Whirling Assault | https://www.sportskeeda.com/mmo/path-exile-2-poe2-massive-skill-buffs-0-3 + https://mobalytics.gg/poe-2/guides/dawn-of-the-hunt-patch-notes | **unverifiable** — specifically not enumerated; may need per-skill patch-note grep |
| 33 | poe2 | `poe2-snipe-mirage-deadeye` | Snipe Mirage Deadeye | 0.3 Snipe skill can consume Freeze effect for more damage vs enemy and bosses | https://www.sportskeeda.com/mmo/path-exile-2-poe2-massive-skill-buffs-0-3 | **confirm** — Snipe + Freeze consumption confirmed |
| 34 | poe2 | `poe2-walking-calamity` | Walking Calamity Autobomber | Post-cutoff autobomber build | — | **unverifiable** — specific build name not surfaced in general 0.3 searches |
| 35 | poe2 | `poe2-shaman-bear` | Shaman Bear | Shaman ascendancy Bear form / build | — | **unverifiable** — specific build not surfaced; may need Shaman ascendancy-specific search |
| 36 | poe2 | `poe2-archmage-totems` | Archmage Totems Oracle | Post-cutoff Oracle Archmage Totems build | — | **unverifiable** — specific build not enumerated |
| 37 | poe2 | `poe2-wall-of-shields` | Wall of Shields | Post-cutoff Wall of Shields skill | — | **unverifiable** — specific skill not enumerated in accessed patch summaries |
| 38 | tl | `tli-erika3-vendetta` | Erika 3 Vendetta Sting | Erika 3 (Vendetta's Sting): melee-focused, damage triggered by Vendetta, Phantom generation every 3 Vendetta casts dealing 3× damage | https://www.mmoexp.com/News/torchlight-infinite-season-13-afterlight-tier-list-best-starter-builds-and-top-endgame-builds-for-high-investment.html + https://skycoach.gg/blog/torchlight-infinite/articles/torchlight-infinite-class-tier-list | **confirm** |
| 39 | tl | `tli-rosa-unsullied` | Rosa Unsullied Blade | Rosa (Unsullied Blade): Supreme Showdown top pick per tier data | https://www.mmoexp.com/News/torchlight-infinite-season-13-afterlight-tier-list-best-starter-builds-and-top-endgame-builds-for-high-investment.html | **confirm** |
| 40 | tl | `tli-carino2-lethal-flash` | Carino 2 Lethal Flash | Carino 2 Lethal Flash TLI hero build | — | **unverifiable** — specific Carino 2 Lethal Flash not enumerated in accessed articles |
| 41 | tl | `tli-sage-elixir` | Sage Elixir Kit | Sage (Scent Weaver): kit focused on Elixir-based skills and Alchemy; SS12 Lunaria + SS13 Afterlight meta | https://www.u4n.com/news/torchlight-infinite-ss12-lunaria-build-guide.html + https://www.mmoexp.com/News/torchlight-infinite-season-13-afterlight-tier-list-best-starter-builds-and-top-endgame-builds-for-high-investment.html | **confirm** — note Sage's headline build in Lunaria was Chromatic Shot (widest AoE); Elixir kit is the underlying archetype |
| 42 | tl | `tli-iris2-thunder-magus` | Iris 2 Thunder Magus Minions | Iris variant Thunder Magus with minion focus | https://www.mmoexp.com/News/torchlight-infinite-season-13-afterlight-tier-list-best-starter-builds-and-top-endgame-builds-for-high-investment.html | **correct** — Iris 1 (Growing Breeze) Nourishment + Spirit Magus Full Bloom is confirmed; Iris 2 Thunder Magus specifically not directly enumerated. Suggest Elrond re-verify Iris 2 vs Iris 1 name mapping. |
| 43 | tq | `tq2-whirlwind-rogue` | Whirlwind Rogue | TQ2 EA Rogue mastery Whirlwind skill (Warfare mastery ability) | https://titanquest2.wiki.fextralife.com/Classes + https://game8.co/games/Titan-Quest-2/archives/541495 | **correct** — Whirlwind is a **Warfare** mastery ability per accessed sources, not Rogue-locked. Elrond may want to verify whether the kit is a Warfare-only or Warfare+Rogue combination build. |
| 44 | tq | `tq2-stormblade-ice-shards` | Stormblade Ice Shards | Stormblade (Storm+Rogue combo mastery): "excellent speed and ranged damage but is fragile" per class tier | https://titanquest2.wiki.fextralife.com/Classes + https://www.lagofast.com/en/blog/titan-quest-2-builds-tier-list/ | **confirm** |
| 45 | tq | `tq2-forge-turrets` | Forge Turrets | Forge mastery (new mastery in TQ2 EA); turret-based build | https://egamersworld.com/blog/every-class-mastery-in-titan-quest-2-early-access-Sk2jdMxFgQ + https://titanquest2.wiki.fextralife.com/Classes | **confirm** |
| 46 | tq | `tq2-elementalist` | Elementalist TQ2 | Elementalist (Earth+Storm combo): strongest class in EA due to damage/defense/mobility mix | https://www.lagofast.com/en/blog/titan-quest-2-builds-tier-list/ | **confirm** |
| 47 | tq | `tq2-bastion-tank` | Bastion Warfare+Forge | Bastion (Warfare+Forge combo): tankiest option for solo progression | https://www.lagofast.com/en/blog/titan-quest-2-builds-tier-list/ | **confirm** |
| 48 | undecember | `ud-ice-crystal-arrow` | Ice Crystal Arrow Bow | Ice Crystal Arrow chain effect; hordes clearance with high clear speed and mobility; Season 7+ build | https://www.pocketgamer.com/undecember/builds/ + https://www.youtube.com/watch?v=oaIPps4qpFo | **confirm** |
| 49 | undecember | `ud-seal-veil-daimonios` | Seal/Veil Resource Build (Daimonios) | High-level Improved Technique rune to lower seal skill resource cost; based on top player Daimonios build | https://www.pocketgamer.com/undecember/builds/ | **confirm** |
| 50 | undecember | `ud-lightning-vortex` | Lightning Vortex Mapper | Lightning Vortex linked with Iron Will + Focus + Fighting Spirit + Warrior's Shadow + Extract Energy + Smash | https://www.pocketgamer.com/undecember/builds/ + https://www.youtube.com/watch?v=PXeLS2UBD5o | **confirm** |
| 51 | undecember | `ud-cwc-spin-caster` | Whirlwind CwC Blizzard (Ya55) | Cast-when-channeling: Whirlwind procs Blizzard via "Spell Activation while Channeling" rune | https://www.pocketgamer.com/undecember/builds/ | **confirm** |
| 52 | vs | `vs-out-of-bounds-freeze` | Out of Bounds freeze build | Out of Bounds (XII) arcana + freeze weapons (Time Warp, Celestial Voulge, Clock Lancet/Infinite Corridor); freeze summons explosions; 1.13.1 patch April 10 2025 | https://vampire.survivors.wiki/w/Out_of_Bounds_(XII) + https://vampire-survivors.fandom.com/wiki/Out_of_Bounds_(XII) + https://steamcommunity.com/sharedfiles/filedetails/?id=3221409140 | **confirm** |

---

## Backfill sheet totals

| Disposition | Count |
|---|---|
| **confirm** | 35 |
| **correct** | 4 |
| **unverifiable** | 13 |
| **TOTAL** | 52 |

Note: 2 rows (`hot-exterminator-burn`, `hot-dragons-breath`) appeared in the mega-probe kb-only-general breakdown (18 of 19 hot rows) but were pre-cutoff — not in this sheet's scope.

---

## Notes for Elrond application pass

1. All 4 dossiers in `la-postcutoff-dossiers-2026-07-16/` carry live URLs for the Wildsoul/Valkyrie rows. Apply per-row per each dossier's Sources section.
2. **Confirm rows** — safe to update `sources_used` with the URLs listed here, retain existing mega-probe claim.
3. **Correct rows** — apply the URL AND adjust the specific claim noted per row:
   - `hades2-hail-storm`: previous name "Apocalyptic Storm" — era_confirmed field may want the rename recorded.
   - `d4-blazing-abyss-warlock`: rename to "Blazing Scream" as of S14 — era_confirmed field may want the rename recorded.
   - `tli-iris2-thunder-magus`: verify Iris variant naming (Iris 1 Growing Breeze vs Iris 2 Thunder Magus vs Iris 3 etc.) — I could not fully corroborate.
   - `tq2-whirlwind-rogue`: verify whether kit is Warfare-only or Warfare+Rogue combo — Whirlwind is Warfare-locked per accessed classes list.
4. **Unverifiable rows** — leave `sources_used` as kb-only; add a `backfill_attempted_2026-07-16` flag or equivalent so future audits know these were searched and left. Consider requesting Matt-specific-source input for D4 Arbiter/Auradin, DI PVP meta, PoE2 0.3 skill-specific rows.
5. **Cross-seam observation:** the Grim Dawn `gd-berserker-wereforms` row (backfill row 17) is a THIRD live-canon shapeshift attestation alongside the Ferality Wildsoul and PBA Wildsoul dossiers filed today. GX-02 SHAPESHIFT keystone now has 3 post-cutoff live-canon attestations from 3 distinct genre franchises (LA + Grim Dawn). Recognition record candidate.

---

## Knowledge gaps this pass did not close

1. **D2R Warlock Season 13 specific Abyss / Void Rift variants** — general season articles cover Fire / Blood Boil / Echoing Strike but not Abyss / Void Rift specifically. May be less-meta variants.
2. **D4 Arbiter / Auradin Paladin variants** — the mainstream sources heavily cover Hammerdin; Arbiter and Auradin are older/niche variants not surfaced in generic search.
3. **Diablo Immortal PVP-meta builds** — DI-specific sources (maxroll DI) required, not surfaced in generic search.
4. **PoE2 0.3 The Third Edict per-skill specifics** — the 0.3 patch article base was accessible but per-skill mechanical detail for the 5 unverified rows (`poe2-spiral-volley`, `poe2-whirling-assault-ma`, `poe2-walking-calamity`, `poe2-shaman-bear`, `poe2-archmage-totems`, `poe2-wall-of-shields`) needs deeper patch-note extraction. Recommend a targeted Legolas Mode A follow-up on PoE2 0.3 skill census.
5. **`hot-landsknecht-grenades`** — Halls of Torment Landsknecht-specific Grenade build not surfaced; may need Steam guide dive.
</content>
</invoke>