# Research — New ARPG Releases 2024–2026 + Modding Purpose Taxonomy — 2026-05-19

**Mode:** A (analytical)
**Commissioner:** Gandalf (Pattern-B commercial-direction analysis)
**Sources consulted:** Nexus Mods game pages, PCGamingWiki, Thunderstore, Steam community discussions, developer official sites, GameRant, VideoGamer, PC Gamer, Kotaku, Wikipedia — full list at bottom.

---

## TL;DR

**Job 1 (New releases 2024–2026):** No newly released game clears the modding-pipeline bar to challenge Grim Dawn as a PRIMARY target. The two most watch-worthy entries are **Titan Quest II** (EA Aug 2025, ARPG, official modding "in discussion") and **STALKER 2** (Nov 2024, UE5 Zone Kit released June 2025, FPS-RPG genre adjacency only). **Last Epoch** confirms NotViable: no official tools, MelonLoader-only, tiny content-mod corpus. **Elden Ring Nightreign** (May 2025, roguelike spin-off) opens a new Souls-adjacent modding surface with Mod Engine 3 but shares all the genre-fit problems of base Elden Ring. Diablo IV, Path of Exile 2, Hades II, No Rest for the Wicked, Avowed, and Throne and Liberty are all NotViable or wrong-genre for Reincarnated's purposes.

**Job 2 (Modding purpose taxonomy):** Among the top 8 existing hosts, the modding communities divide sharply. Grim Dawn and Torchlight 2 are dominated by **content addition (large) + total conversion** — the closest community analogs to Reincarnated's injection use case. Terraria and Minecraft are dominated by **content addition (large) + QoL**, with strong tolerance for novel systems. BG3 is cosmetic-heavy. Elden Ring and V Rising skew toward **balance/difficulty + mechanic injection**. Procedural/generative modding is **universally rare** across all eight hosts — Reincarnated would be a community-novel pattern on every platform, but GD and TL2 have the least friction because their communities already accept large content drops from external sources.

---

## JOB 1 — New Releases 2024–2026: Modding Survey

### Summary Table

| Title | Dev | Release | Genre Fit | Modding Pipeline | KPI | Schema | Pipeline | Community | MFS est. | Tier | Critical Caveat |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Titan Quest II | Eidos/THQ Nordic | EA Aug 2025, 1.0 ~late 2026 | STRONG — direct ARPG mastery system | Limited early-access data modding; community UE5 pak mods; official tools "under discussion" | 4 | 3 | 2 | 2 | 2.75 | Niche (watch) | Pre-launch; no confirmed official mod SDK; UE5 pak mods functional but fragile |
| STALKER 2: Heart of Chornobyl | GSC Game World | Nov 2024 (full), Zone Kit June 2025 | WEAK — FPS survival with RPG elements | Zone Kit (UE5 SDK) on Epic Launcher, Mod.io + Steam Workshop | 1 | 1 | 3 | 3 | 1.90 | NotViable | Genre mismatch (FPS/survival vs ARPG); schema incompatibility near-total |
| Last Epoch | Eleventh Hour Games | 1.0 Feb 2024 | STRONG — looter ARPG with mastery-style class system | NO official tools; MelonLoader community loader; offline mode only; no Steam Workshop | 3 | 3 | 1 | 2 | 2.25 | NotViable | Developer has never signaled mod support intent; online/offline split limits audience |
| Elden Ring Nightreign | FromSoftware | May 30, 2025 | WEAK — roguelike spin-off of Souls action-RPG | Mod Engine 3 (community, successor to ME2); Nexus Mods active; EAC = online ban if modded | 1 | 1.5 | 2.5 | 3 | 1.90 | NotViable | Same Souls audience/genre issues as base Elden Ring; EAC limits distribution; roguelike loop not ARPG |
| Hades II | Supergiant Games | EA May 2024, 1.0 Sept 25 2025 | WEAK — roguelite action; 112k peak concurrent | Hell2Modding (community, Thunderstore); no official support; Lua-based content scripts | 1 | 1 | 2 | 3 | 1.65 | NotViable | Roguelite loop fundamentally different from ARPG build-system; no dev mod tools |
| No Rest for the Wicked | Moon Studios | EA Apr 2024; still EA May 2026 (1.7M copies) | MODERATE — isometric action-RPG, dark gothic | MelonLoader community only; no official modding SDK; 1.0 not yet shipped | 2 | 2 | 1 | 2 | 1.75 | NotViable | EA limbo (1.0 not confirmed); no official tools planned; tiny mod corpus |
| Tainted Grail: The Fall of Avalon | Awaken Realms | EA → nearing 1.0 (patch 1.15 Dec 2025) | MODERATE — open-world RPG, Arthurian | BepInEx loader; ~135 Nexus mods; no Steam Workshop; one-mod-at-a-time (single res.pack) | 2 | 2 | 1.5 | 2 | 1.80 | NotViable | Same single-pack constraint as Wartales; no content-class mods observed |
| Avowed | Obsidian / Xbox | Feb 13, 2025 | MODERATE — first-person RPG; Pillars-adjacent | No official support; community Nexus mods (~142 mods); mostly QoL/perf | 1 | 1 | 1.5 | 2 | 1.35 | NotViable | FP-RPG not ARPG; no class injection precedent; no official tools planned |
| Wartales | Shiro Games | Full 2023, updates 2024 | WEAK — turn-based tactical RPG | No official tools; Nexus mods only; single res.pack constraint = one mod at a time | 1 | 1 | 1 | 2 | 1.20 | NotViable | Turn-based tactical; wrong genre entirely; single-mod constraint severe |
| Diablo IV | Blizzard | Expansion Oct 2024 (Vessel of Hatred) | STRONG genre match | Explicitly banned; Blizzard actively bans accounts for any mods | 4 | 4 | 1 | 1 | 2.45 | NotViable (policy) | Permanent ban enforcement confirmed post-2024; no change to policy |
| Path of Exile 2 | GGG | EA Dec 2024; 0.3 ~Aug 2026 | VERY STRONG genre match | No mod support; GGG has never permitted mods; live-service architecture | 5 | 4 | 1 | 1 | 2.65 | NotViable (policy) | GGG's 0.5 update (May 2026) added community build-planner API — NOT modding; live-service architecture structurally precludes client mods |
| Throne and Liberty | NCSoft / Amazon | Oct 2024 | WRONG — MMO | MMO; no mod support; wrong genre | 1 | 1 | 1 | 1 | 1.00 | NotViable | MMO; architecture precludes modding |
| Eternal Strands | Yellow Brick Games | Jan 28, 2025 | WEAK — action-RPG, magic-focused | No modding tools; no community mod scene observed; DLC/collab focus | 1 | 1 | 1 | 1 | 1.00 | NotViable | Small studio; no modding infrastructure |
| Torchlight: Infinite | XD Inc | Mobile/PC free-to-play; 2022–2025 | MODERATE game loop, WRONG model | Live-service F2P; no mod support by design | 2 | 2 | 1 | 1 | 1.55 | NotViable | F2P live-service; modding architecturally impossible |

---

### Per-Candidate Detail

#### Titan Quest II — WATCH (Niche, possible Secondary by 1.0)

- **Status:** Early Access since August 1, 2025. Full release targeted late 2026. Developed by Eidos-Sherbrooke / THQ Nordic. Built on Unreal Engine 5.
- **Genre fit:** Direct ARPG with mastery system — the closest spiritual successor to TQAE in the survey list. KPI match with Reincarnated would be strong.
- **Modding:** No official mod SDK or editor confirmed as of May 2026. Steam discussion thread titled "Why no Modding options?" from community. THQ Nordic EA FAQ states modding support is "under discussion." A Vortex Mod Manager community extension exists; UE5 pak-based mods are functioning (Nexus mods page active). ModDB has a small mods listing.
- **MFS estimate:** KPI 4 / Schema 3 / Pipeline 2 / Community 2 → ~2.75 weighted. Niche tier now, but if official tools ship with 1.0 this becomes a Secondary or better candidate. The TQAE adapter pipeline (if built in Phase 2) would substantially reduce TQ2 integration cost.
- **Caveat:** Do not commit effort until official modding tool announcement. The UE5 pak approach is fragile between patches. Recheck at 1.0 launch.

#### STALKER 2: Heart of Chornobyl — NotViable

- **Status:** Full release November 2024 (after years of delays and wartime disruption). Zone Kit (official UE5 modding SDK) released June 25, 2025 on Epic Games Launcher. Size: 700 GB of uncompressed assets. Supports Mod.io + Steam Workshop. Patch 1.5 June 2025 also shipped A-Life overhaul.
- **Genre fit:** FPS survival-RPG. Not an ARPG. No mastery/class system analogous to Reincarnated.
- **Modding pipeline:** Zone Kit is real and functional; active Nexus community (~2000+ mods as of late 2025). Top mods are total overhauls ("Better Zone"), gameplay-hardcore overhauls, A-Life fixes. Procedure: can create new locations, quests, NPCs, items, weapons. Strong precedent from classic STALKER mod communities.
- **MFS estimate:** KPI 1 / Schema 1 / Pipeline 3 / Community 3 → ~1.90 weighted. NotViable.
- **Caveat:** Pipeline is genuinely good and the community is large. If Reincarnated ever pivots toward FPS-RPG survival (unlikely), this is a reconsider. For now: wrong genre, wrong schema, no path.

#### Last Epoch — NotViable

- **Status:** 1.0 released February 21, 2024. Developed by Eleventh Hour Games. Seasonal content model ("Cycles"). Active live service. ~200k peak concurrent on 1.0 launch day.
- **Genre fit:** Extremely strong ARPG match — mastery-style monolith system, deep build system, Cycles parallel to Reincarnated's seasonal content model.
- **Modding:** Officially not supported and never signaled as planned. Offline mode enables MelonLoader-based mods for single-player only. Nexus Mods page exists but corpus is almost entirely QoL cheats (auto-loot, stash management, stat display). No class injection mods observed. Developer's "Paradox Classes" (future DLC content) suggests they view class expansion as a paid content vector, not a community modding space.
- **MFS estimate:** KPI 3 / Schema 3 / Pipeline 1 / Community 2 → ~2.25 weighted. NotViable.
- **Caveat:** This is the most painful miss on the list — the game loop is a near-perfect conceptual match for Reincarnated's content model. The pipeline gap is structural and the developer has no incentive to open it (they're selling seasons themselves). Offline-only mod scope would reach a tiny fraction of the playerbase. Do not pursue.

#### Elden Ring Nightreign — NotViable

- **Status:** Released May 30, 2025. Roguelike action-RPG spin-off; cooperative focus. 313k peak concurrent Steam; 3.5M copies in 5 days.
- **Genre fit:** Roguelike action-RPG. "Nightlord" boss rotation has some ARPG seasonal flavor but the core loop is roguelite not looter-ARPG.
- **Modding:** Mod Engine 3 (community tool, successor to ME2) supports Nightreign as of its 1.02.3 patch. Active Nexus Mods community. EAC prevents online play while modded — this hard-caps audience to offline/single-player modders only, which is a severe distribution problem.
- **MFS estimate:** KPI 1 / Schema 1.5 / Pipeline 2.5 / Community 3 → ~1.90 weighted. NotViable.
- **Note:** The roguelite structure (3-night run = one "season") has thematic resonance with Reincarnated's seasonal content, but the execution gap is large. Flag for post-Phase-3 speculative note in Gandalf's analysis only.

#### Hades II — NotViable

- **Status:** EA May 2024. 1.0 released September 25, 2025. 112k+ peak concurrent on 1.0 launch (2x original Hades record). Strong critical reception.
- **Genre fit:** Roguelite dungeon-crawler. Character and boon variety is thematically adjacent but the loop (run-based, no persistent build investment) is wrong for Reincarnated.
- **Modding:** Community Hell2Modding framework (Lua-based, ReturnOfModding base). Thunderstore distribution. No official support from Supergiant. Mods on Nexus as well. Community active but small.
- **MFS estimate:** KPI 1 / Schema 1 / Pipeline 2 / Community 3 → ~1.65 weighted. NotViable.

#### No Rest for the Wicked — NotViable (for now)

- **Status:** EA April 2024. As of May 2026, still in EA. 1.7M copies sold. Co-op update "Together" Jan 2026. Major updates Breach and Breach Refined in 2025. 1.0 release date not confirmed; price expected to rise from ~$40 to ~$60 at 1.0.
- **Genre fit:** Isometric action-RPG with pixel-art hand-crafted aesthetic. ARPG loop. Medium genre match.
- **Modding:** MelonLoader community only. No official SDK. Moon Studios focused on co-op and content completion. Small Nexus mod corpus (mostly QoL). No class injection mods.
- **Verdict:** Flag for re-evaluation at 1.0 ship. If Moon Studios adds Workshop/modding tools post-1.0, the genre fit is meaningful. SPECULATION: the studio is self-publishing indie; modding tools are unlikely in 1.0 scope.

#### Diablo IV — NotViable (policy, permanently)

Blizzard's account-ban policy for all mods, including purely cosmetic ones, was confirmed active post-2024 and has not softened after the Vessel of Hatred expansion. No change to research finding from prior survey period. Confirmed closed.

#### Path of Exile 2 — NotViable (architecture, likely permanently)

GGG released EA December 2024. As of May 2026, update 0.3 targeting August 2026, full 1.0 still unconfirmed timeline. GGG has added a community build-planner API (0.5 update May 2026) but this is a third-party data integration tool, not a modding framework. GGG has never permitted client modifications and the live-service architecture (always-online, server-authoritative) makes client-side content mods structurally impossible. Confirmed closed.

#### Throne and Liberty — NotViable

MMORPG released October 2024 by NCSoft / Amazon. Multiplayer-only architecture. Modding not applicable.

#### Tainted Grail: The Fall of Avalon — NotViable

Open-world RPG. ~135 Nexus mods. BepInEx loader. Critically: single res.pack constraint means only one mod can be loaded at a time (same problem as Wartales). No class-injection or content-addition mods observed. Genre is open-world RPG, not ARPG looter. Skip.

#### Wartales — NotViable

Turn-based tactical mercenary RPG. No official modding tools. Single-file constraint (one res.pack). Wrong genre entirely.

#### Avowed — NotViable

First-person RPG (Pillars of Eternity adjacent). Feb 2025 release. ~142 Nexus mods, almost entirely QoL and performance. No official modding tools planned. First-person exploration RPG — wrong genre for ARPG class injection.

---

### Other Candidates Checked (Brief)

- **Torchlight: Infinite** — F2P live-service mobile/PC. No mod support. Wrong architecture.
- **Eternal Strands** — Action-RPG Jan 2025 (Yellow Brick Games, ex-BioWare team). No modding infrastructure. Post-launch focused on paid DLC collaborations (Final Fantasy, Grasshopper Manufacture). Small studio, unlikely to open modding.
- **Immortals of Aveum** (Ascendant Studios, 2023) — First-person magic shooter. Poor sales, studio layoffs 2024. Not an ARPG. No modding community.
- **Pillars of Eternity 3** — Not announced as of May 2026. No data.
- **Mobile ARPG modding** — Not viable. All major mobile ARPGs (Diablo Immortal, Torchlight Infinite, etc.) are live-service with no modding provisions.
- **Roboquest** — 1.0 Nov 2023. Roguelite FPS, not ARPG. Small mod community. No relevant pipeline.
- **Contraband** (Avalanche Studios) — Not released as of May 2026; previously rumored cancelled or in indefinite hold. No data.
- **Steam Next Fest / EA ARPGs 2025–2026** — No ARPG in the EA/Next Fest window observed with both (a) strong modding pipeline AND (b) sufficient player base to matter. Most EA ARPGs use UE5 pak mods informally with no official support.

---

## JOB 2 — Modding Purpose Taxonomy for Top 8 Hosts

### Taxonomy Definitions (for this report)

1. **QoL / Bug-fix** — UI, accessibility, stash management, bug-fixes, balance tweaks
2. **Cosmetic / Art** — Skins, textures, models, visual retextures
3. **Content addition (small)** — Single new class / weapon / monster / item set
4. **Content addition (large)** — Class packs, expansion-sized additions, new acts
5. **Total conversion (TC)** — Replaces core game (Reign of Terror, Median XL)
6. **Balance / Difficulty overhaul** — Hard modes, rebalance patches, rule rewrites
7. **Lore / Worldbuilding** — Questlines, dialogue, story expansions
8. **Mechanic injection** — New systems (crafting overhaul, new combat mechanics)
9. **Multiplayer / Online** — Server features, co-op, custom modes
10. **Procedural / Generative** — Random generation, infinite content, seasonal gen

### Taxonomy Table (Top 8 Hosts)

| Host | Dominant Purpose #1 | Dominant Purpose #2 | Dominant Purpose #3 | Procedural/Generative presence? | Reincarnated fit natural or unusual? |
|---|---|---|---|---|---|
| Grim Dawn | Content addition (large) — class/mastery packs | Total conversion (TC) | QoL / Bug-fix | Rare to absent | UNUSUAL but closest analog; community accepts large new-class drops as first-class content |
| TQAE | Content addition (large) — mastery packs | Total conversion (TC) | QoL | Rare to absent | UNUSUAL — same pattern as GD; small but receptive community |
| Torchlight 2 | Content addition (large) — class packs | Content addition (small) — individual classes | QoL / Balance tweaks | Rare to absent | UNUSUAL but well-tolerated; "Classes Reborn" (40+ classes) shows appetite for high-volume content drops |
| Terraria (tModLoader) | Content addition (large) — biome/boss expansion mods | Mechanic injection | QoL | Low but present (kRPG-style item gen) | SOMEWHAT UNUSUAL — tModLoader community has the highest tolerance for novel systems; compile-time C# constraint is the real blocker |
| Minecraft (Forge/Fabric) | Content addition (large) — tech/magic modpacks | Mechanic injection | QoL / Performance | LOW but present (Vault Hunters randomized dungeon loot) | UNUSUAL but highest community openness to systemic novelty; voxel genre divergence is the problem |
| Baldur's Gate 3 | Cosmetic / Art — character creator, appearance | Content addition (small) — subclasses, spells | QoL / Bug-fix | Essentially absent | VERY UNUSUAL — BG3 community is cosmetic and narrative-first; procedural content injection is an alien concept here |
| Elden Ring | Balance / Difficulty overhaul | Content addition (large) — spells/weapons/areas | Cosmetic / Art | Essentially absent | VERY UNUSUAL — Souls community expects curated handcrafted content; procedural generation would be received with skepticism |
| V Rising | Multiplayer / Online — server tools, admin mods | Mechanic injection — new class/perk systems | QoL | Essentially absent | UNUSUAL — server-operator community is active; if Reincarnated content injected as a "server season pack" the framing could fit, but the community expects server-admin tools not content generators |

---

### Per-Host Detail

#### Grim Dawn

The Nexus Mods category breakdown (as of 2025–2026) shows Gameplay as the largest category (68+ files), followed by Miscellaneous (42). The dominant cultural gravity is **class/mastery addition** — the entire community recognizes Dawn of Masteries and Grimarillion as the apex mods. Dawn of Masteries compiles 50+ ported masteries from other game mods; it is effectively the community's "all content welcome" aggregator. Total conversions (Reign of Terror porting D2, Warhammer 40K conversion, Path of Grim Dawn 2024) represent the second major mode.

**Procedural/generative:** No observed procedural-generation mods. The GD engine's deterministic loot tables and hand-authored content are the norm. Reincarnated's seasonal-JSON-injection pattern would be **novel** but not hostile — the community is accustomed to "external source drops new mastery pack." The framing that Reincarnated produces a new mastery every season via LLM is adjacent enough to the Dawn of Masteries compilation model to be intelligible. The one-mod-at-a-time constraint remains the operational headache: Reincarnated's seasons would compete for the single active-mod slot unless nested inside a compilation mod.

**Verdict:** Most receptive host to Reincarnated's use case by cultural fit. Content drops from external tools are normalized. Procedural generation is novel but not hostile.

#### Titan Quest Anniversary Edition

Modding culture mirrors GD: mastery/class packs dominate (ShadowChampions Multimaster, Legion of Champions Reloaded, active as of May 2026). Total conversions exist (GD→TQAE direction precedents). Community smaller (~742 avg concurrent May 2026) but engaged.

**Procedural/generative:** Same absence as GD. Same cultural receptivity argument applies, slightly attenuated by smaller community.

#### Torchlight 2

Dominated by class content. SynergiesMOD (3 new classes, 661k Steam Workshop subscribers — the highest single-mod subscriber count in the survey), Classes Reborn (40+ classes), TL2-ACE (6 classes + 2 acts). The class-injection pattern is the most traveled of any host: TL2 community explicitly expects new class drops and has infrastructure to receive them (Workshop auto-sync, DAT text format).

**Procedural/generative:** Torchlight 2 already has **procedurally generated dungeons as a native game mechanic** — the game's dungeon randomizer is baked in. The modding community, however, has not extended this to content generation. No observed mods that generate class/skill content procedurally. But the native proc-gen DNA of the engine means the community has a conceptual model for it. Reincarnated's seasonal classes would read as "another new class" — the highest-frequency accepted mod type here.

**Verdict:** Best operational fit for Reincarnated's content-injection use case if the framing is "here is a new class this season." The per-season cadence maps cleanly to the Workshop subscription model (subscribe once, get the season's class).

#### Terraria (tModLoader)

Content addition (large) is king: Calamity (9.18M subscribers), Thorium, Spirit Mod. Mechanic injection is strong second: tModLoader API is C# and specifically designed to support entirely new game systems. QoL mods (Recipe Browser, Magic Storage) are third.

**Procedural/generative:** The closest analog to Reincarnated in the existing Terraria mod ecosystem is **kRPG** — a mod that adds procedurally generated items and some class-like elements. It demonstrates community appetite. However, "closest analog" still means small audience relative to content-expansion mods.

The critical issue for Reincarnated: all content must be compiled C# at build time. Per-season content drops require a full new build + Workshop push. For a weekly or monthly cadence this is operationally feasible but non-trivial. The community would accept it; the pipeline is the problem.

#### Minecraft (Forge/Fabric)

Content addition (large) via modpacks is the cultural dominant: tech packs, magic packs, kitchen-sink packs. Mechanic injection is strong second (the Create mod, Mekanism, etc. all inject full new mechanical systems). The community has the highest **conceptual tolerance** for novel systemic additions of any host — Minecraft modders expect the unexpected.

**Procedural/generative:** Vault Hunters modpack is the most relevant precedent: ARPG-style vault dungeon runs with randomized loot and seasonal updates. It demonstrates that the Minecraft community can receive an ARPG-procedural-content framing. But the voxel aesthetic conversion cost for Reincarnated is severe.

#### Baldur's Gate 3

The Nexus Mods page has 15,000+ mods. Top downloads are dominated by cosmetic character creator mods (Tav's Hair Salon is #1 by downloads), followed by the ImprovedUI system mod and subclass/spell additions (5e Spells, Fantastical Multiverse). The community's first question is "how does my Tav look?" — strongly cosmetic orientation.

**Procedural/generative:** Essentially absent. No observed procedural-generation mods. The BG3 community is narrative-immersion and cosmetic-first. A mod that generates new subclasses algorithmically would likely be received with curiosity but low uptake — the community wants authored, lore-coherent content.

**For Reincarnated specifically:** Framing this as "procedurally generated subclass with LLM-written flavor text" is the closest viable angle, and could be a brand-presence play as noted in the scoring matrix. But do not expect high community uptake based on dominant mod culture.

#### Elden Ring

~6,900 mods on Nexus. Dominant categories: balance/difficulty overhaul (Elden Ring Reforged, difficulty sliders, hitbox fixes), content addition large (The Convergence — new spells, weapons, areas), cosmetic (armor swaps, appearance changes), co-op/multiplayer (Seamless Co-op is the #1 most-downloaded mod on the entire Nexus page).

**Procedural/generative:** Essentially absent. The Souls community's core identity is engagement with authored, handcrafted content — enemy placements, boss designs, level layouts are the subject of intense community discussion and appreciation. Procedurally generated content would be antithetical to the dominant community value system.

**Note on Shadow of Erdtree:** The DLC (June 2024) broke many mods. The Convergence (the major content mod) required months of rebuilding. This compat fragility is a real operational risk.

#### V Rising

Thunderstore hosts the V Rising mod ecosystem. Dominant mod types by community mass: server-side admin and multiplayer tools (PvP leaderboards, server automation, scheduled spawning), followed by mechanic injection (Bloodcraft adds full class system, leveling, familiars, perk tree), followed by QoL.

**Procedural/generative:** Absent in the current mod corpus. The V Rising community has a meaningful contingent of **server operators** who use mods to configure custom PvP/PvE experiences. This is actually an interesting angle for Reincarnated: a "seasonal server pack" that server operators apply to generate fresh content each cycle. The community's server-operator orientation makes them more receptive to automated content tooling than most other communities. However, the audience is still small relative to GD/TL2 and Thunderstore has lower discoverability than Nexus.

**Note on Bloodcraft:** Bloodcraft (the best precedent mod) demonstrates that the community will accept comprehensive mechanic injection. No license determination yet for third-party build nesting.

---

## Cross-Cutting Insights

**Insight 1: Procedural/generative modding is a white space across all 8 hosts.** Not one host community has an established procedural-content-generation mod that has achieved significant uptake. Reincarnated's use case is novel on every platform. This is simultaneously a market-gap opportunity and a community-education challenge. The framing "LLM generates a new class this season" requires translation into host-community vocabulary ("here is a new mastery for this season" in GD; "here is a new class" in TL2).

**Insight 2: The two most culturally aligned communities (GD + TL2) are also the two with the most directly analogous existing content patterns.** Both communities treat large new-class drops as first-class content. Reincarnated can arrive as "another content source" rather than "a weird generative experiment."

**Insight 3: The BG3 and Elden Ring communities are the worst fits for Reincarnated's generative content-injection purpose** — they are cosmetic-first and curated-content-first respectively. These remain defensible as brand-presence plays but procedural seasonal content will not be a community-pull driver there.

**Insight 4: Titan Quest II is the only new-release game that could mature into a Secondary-tier host.** If THQ Nordic ships official modding tools at 1.0 (~late 2026), the TQ2 community would be culturally pre-primed (same mastery-system modding culture as TQAE) and the genre fit is strong. The TQAE adapter pipeline (Phase 2) would likely be partially reusable for TQ2. Recommend a check-in at TQ2 1.0 launch.

**Insight 5: STALKER 2 has a genuinely good modding SDK but is a genre dead-end.** The Zone Kit (700 GB, UE5, Mod.io + Steam Workshop) is one of the more capable official mod SDKs to ship in this period. The FPS-survival genre gap is unbridgeable for Reincarnated's current content schema. Log it as an irrelevant but technically impressive data point.

**Insight 6: Last Epoch is the most painful miss.** The conceptual model (seasonal cycles, deep build system, mastery classes) is a near-perfect match for Reincarnated's output. The developer's structural choice to monetize class expansion via paid DLC ("Paradox Classes") and keep the game always-online-preferred makes community modding of the type Reincarnated needs architecturally and commercially impossible.

**Insight 7: V Rising's server-operator community is an underrated procedural-content audience.** If Reincarnated produces a "season pack" that a server operator can install to refresh their server's content each cycle, the V Rising server operator community is more culturally prepared to receive this framing than any other community in the survey — they are already thinking in terms of "what configuration do I deploy this season?" The pipeline (BepInEx + Thunderstore) remains the operational constraint.

---

## Open Questions

1. **Titan Quest II 1.0 modding tools announcement** — Does THQ Nordic confirm official mod SDK before end of 2026? If yes, add to scoring matrix at that time. Check at full release.
2. **Last Epoch developer stance re-check** — Any indication from Eleventh Hour that offline modding will be expanded or official tools considered? (Current evidence: none. Paradox Classes DLC model suggests opposite direction.) Recommend a single check-in at each major expansion.
3. **Elden Ring Nightreign modding pipeline stability** — Mod Engine 3 is community-maintained. If FromSoftware patches break it (as happened with Elden Ring base game after Shadow of Erdtree), the community surface collapses. For Reincarnated this matters only if a speculative Nightreign angle is ever pursued.
4. **No Rest for the Wicked 1.0 + modding tools** — Studio has become self-publishing indie. Any chance of Workshop/official tools at 1.0? Worth a single follow-up check at 1.0 launch.
5. **V Rising Bloodcraft license check** — Confirmed outstanding in existing scoring matrix. Still needed before any V Rising nesting work begins.
6. **Procedural modding framing experiment** — Has any modder in any community attempted a "generate new content from an external tool and ship as a mod" workflow? The kRPG (Terraria) and Vault Hunters (Minecraft) precedents are closest but neither use LLM generation. Worth a targeted scan if Reincarnated wants to establish community-prior art.

---

## Source List

- [Last Epoch — PCGamingWiki](https://www.pcgamingwiki.com/wiki/Last_Epoch)
- [Last Epoch Nexus Mods](https://www.nexusmods.com/lastepoch)
- [MelonLoader Mods for Last Epoch — GitHub](https://github.com/RCInet/LastEpoch_Mods)
- [Path of Exile 2 build planner — FRVR](https://frvr.com/blog/news/path-of-exile-2-build-planner-will-never-include-official-ggg-builds/)
- [Hades II v1.0 coming Sept 25, 2025 — Supergiant](https://www.supergiantgames.com/blog/hades2-coming-sep25/)
- [Hades II 112k concurrent — GameSpot](https://www.gamespot.com/articles/hades-2-passes-110000-concurrent-players-on-steam-doubling-all-time-peak-for-original/1100-6535081/)
- [Hell2Modding — Thunderstore](https://thunderstore.io/c/hades-ii/p/Hell2Modding/Hell2Modding/)
- [Hades II Nexus Mods](https://www.nexusmods.com/games/hades2)
- [No Rest for the Wicked — Steam store page](https://store.steampowered.com/app/1371980/No_Rest_for_the_Wicked/)
- [No Rest for the Wicked progress toward 1.0 — ingamenews, Apr 2026](https://www.ingamenews.com/2026/04/no-rest-for-wicked-steam-early-access.html)
- [No Rest for the Wicked modding tools — Steam discussion](https://steamcommunity.com/app/1371980/discussions/0/695374764691402819/)
- [STALKER 2 Zone Kit — official modding page](https://www.stalker2.com/modding)
- [STALKER 2 Zone Kit 700 GB size — PC Gamer](https://www.pcgamer.com/games/fps/wanna-make-mods-for-stalker-2-thatll-be-700-gb-of-hard-drive-space-please/)
- [STALKER 2 Zone Kit + Patch 1.5 — BigGo News](https://biggo.com/news/202506261032_STALKER_2_Gets_Major_Update_and_Modding_Tools)
- [STALKER 2 Nexus Mods](https://www.nexusmods.com/games/stalker2heartofchornobyl)
- [Avowed modding — VideoGamer](https://www.videogamer.com/guides/avowed-is-there-mod-support/)
- [Avowed Nexus Mods](https://www.nexusmods.com/avowed)
- [Diablo IV modding ban — Tweaktown](https://www.tweaktown.com/news/92570/do-you-use-diablo-4-mods-blizzard-might-hit-with-the-perma-ban-stick/index.html)
- [Diablo IV modding ban — The Gamer](https://www.thegamer.com/diablo-4-will-perma-ban-players-using-any-mods/)
- [Wartales modding — Steam discussion](https://steamcommunity.com/app/1527950/discussions/0/3830916907590337146/)
- [Wartales Nexus Mods](https://www.nexusmods.com/games/wartales)
- [Tainted Grail: The Fall of Avalon — Nexus Mods](https://www.nexusmods.com/games/taintedgrailthefallofavalon)
- [Tainted Grail modding guide — dtgre.com, 2025](https://www.dtgre.com/2025/05/tainted-grail-best-mods-guide.html)
- [Titan Quest II — Nexus Mods](https://www.nexusmods.com/games/titanquest2)
- [Titan Quest II modding discussion — Steam](https://steamcommunity.com/app/1154030/discussions/0/591781816976983345/)
- [Titan Quest II Early Access Roadmap — THQ Nordic](https://thqnordic.com/news/titan-quest-ii-early-access-roadmap-and-faq)
- [Elden Ring Nightreign — Wikipedia](https://en.wikipedia.org/wiki/Elden_Ring_Nightreign)
- [Elden Ring Nightreign — Steam](https://store.steampowered.com/app/2622380/ELDEN_RING_NIGHTREIGN/)
- [Elden Ring Nightreign Nexus Mods](https://www.nexusmods.com/games/eldenringnightreign)
- [Mod Engine 3 — me3.help](https://me3.help/en/latest/)
- [Grim Dawn Nexus Mods categories](https://www.nexusmods.com/grimdawn/mods/categories)
- [Dawn of Masteries — Nexus](https://www.nexusmods.com/grimdawn/mods/82)
- [Dawn of Masteries — ModDB](https://www.moddb.com/mods/dawn-of-masteries)
- [Torchlight 2 Nexus Mods top](https://www.nexusmods.com/torchlight2/mods/top)
- [SynergiesMOD — Nexus](https://www.nexusmods.com/torchlight2/mods/1)
- [Classes Reborn Overhaul — ModDB](https://www.moddb.com/mods/classes-reborn-overhaul)
- [BG3 Nexus Mods categories](https://www.nexusmods.com/baldursgate3/mods/categories/)
- [Best BG3 mods 2025 — GameSpot](https://www.gamespot.com/gallery/best-baldurs-gate-3-mods/2900-5661/)
- [V Rising Thunderstore](https://thunderstore.io/c/v-rising/)
- [Eternal Strands — Wikipedia](https://en.wikipedia.org/wiki/Eternal_Strands)
- [Eternal Strands DLC plans — The Outerhaven](https://www.theouterhaven.net/updates-and-dlc-plans-eternal-strands/)
- [aRPG Timeline — NRFTW](https://www.arpg-timeline.com/game/nrftw)
