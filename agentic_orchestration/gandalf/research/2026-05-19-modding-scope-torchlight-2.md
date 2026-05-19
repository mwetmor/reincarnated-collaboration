# Research — Torchlight 2 Modding Scope & Developer Permissions — 2026-05-19

**Mode:** A (analytical)
**Commissioner:** Gandalf (Pattern-B mod-target analysis)
**Scope:** Six axes — IP ownership, moddable surface, monetization, SynergiesMOD legal, distribution enforcement, engine lifespan

---

## TL;DR

Torchlight 2's modding surface is broad and technically stable: GUTS covers classes, skills, combat data, AI parameters, UI layout files, custom 3D models, and level chunks, with only the procedural dungeon generation logic itself and compiled C++ internals locked. The IP chain is now Runic Games (dissolved 2017) → Perfect World → Gearbox Publishing SF → Arc Games (April 2024), all within Embracer Group's umbrella; no new mod policy has been issued at any transition. The operative legal text remains Runic's original ToU (Section 6.4), which explicitly prohibits commercial exploitation of mods — meaning Patreon-funded mods are in a gray zone at best, and selling mods is clearly prohibited. SynergiesMOD (last update February 2020, author Salan last publicly active circa 2020) carries no published license and no documented permission for third-party builds — add-ons exist in practice because enforcement is absent, not because permission was granted. Engine v1.25 (last patched 2017) is frozen, which is a stability asset for modding: no patch-break risk. Steam Workshop and Nexus remain active; no enforcement actions documented against any mod distribution method. Community is small but functional (~250 daily concurrent, active Discord, torchlightfansite/ModDrop archive preserved). The operative risk for Reincarnated is not technical moddability — it is the absence of any explicit mod-rights grant covering commercial or redistributable builds, and the orphaned SynergiesMOD legal situation.

---

## 1. EULA / Official Policy — Who Owns It Now?

**Status: PARTIALLY DOCUMENTED — IP chain documented; post-transition mod policy is UNKNOWN/UNPUBLISHED**

**IP chain:**
- Runic Games was majority-acquired by Perfect World Entertainment in 2010; Runic dissolved November 2017 (source: [Runic Games — Wikipedia](https://en.wikipedia.org/wiki/Runic_Games), [Indie Game Website](https://www.indiegamewebsite.com/2017/11/06/runic-games-dissolved-by-parent-company-perfect-world-entertainment/)).
- Perfect World retained the Torchlight IP and continued selling TL2 post-shutdown (confirmed in PWE statement at dissolution).
- Echtra Games (founded by ex-Runic co-founder Max Schaefer) was contracted by PWE to develop Torchlight 3/Frontiers, but PWE retained IP ownership — Echtra was never the IP holder (source: [The Gamer](https://www.thegamer.com/echtra-games-zynga-torchlight-3-perfect-world/)).
- Zynga acquired Echtra Games in March 2021, but TL3's IP remained with Perfect World; Echtra handed back TL3 development and Zynga closed Echtra in June 2025 (source: [Massively Overpowered, June 2025](https://massivelyop.com/2025/06/03/og-torchlight-frontiers-aka-torchlight-3-studio-echtra-games-has-been-shuttered-by-zynga/)).
- Embracer Group acquired Perfect World Entertainment in December 2021 for $125M; PWE was absorbed as a subsidiary of Gearbox Entertainment Company and rebranded as Gearbox Publishing San Francisco (source: [Embracer Group press release](https://embracer.com/releases/embracer-group-enters-into-agreement-to-acquire-perfect-world-entertainment/), [GameSpot](https://www.gamespot.com/articles/embracer-group-acquires-torchlight-publisher-perfect-world-entertainment-in-125-million-deal/1100-6499200/)).
- In April 2024, Gearbox Publishing SF was retained by Embracer (after Gearbox Entertainment was sold to Take-Two) and rebranded as **Arc Games** (source: [PC Gamer](https://www.pcgamer.com/hyper-light-breaker-publisher-perfect-world-is-now-gearbox-publishing/), [Game Developer](https://www.gamedeveloper.com/business/perfect-world-rebrands-as-gearbox-publishing-after-embracer-purchase)).

**Current IP owner: Arc Games (Embracer Group subsidiary), as of April 2024.** Arc Games publishes TL2 on Steam and provides support at support.arcgames.com.

**Operative EULA:** The Runic Games Terms of Use ([torchlight2game.com/legal/terms-of-use](https://www.torchlight2game.com/legal/terms-of-use)) remains the operative agreement. Key modding-relevant language:
- Section 6.4: "selling, licensing, or otherwise commercially exploiting 'mods' of the Game" is explicitly prohibited.
- Section 3.5: creating derivative works from game content without written consent is prohibited.
- Section 7: no works of authorship or derivative works based on the site or game except as expressly permitted by Runic.
- Exception: non-commercial fan sites are permitted under specific attribution conditions.

**Post-transition changes: UNKNOWN/UNPUBLISHED.** No new mod policy statement has been issued by Perfect World, Gearbox Publishing SF, or Arc Games since Runic's dissolution. No Wayback Machine captures of a more permissive Runic-era mod policy (distinct from the ToU) were located. The original Runic mod-friendliness was expressed through providing the GUTS tool — not a separate written mod rights grant. The commercial prohibition in the ToU has never been explicitly relaxed or superseded by any successor owner. Arc Games has a TL2 modding support section ([Modding Issues](https://support.arcgames.com/hc/en-us/sections/360003275973-Modding-Issues-Torchlight-II)) but no independently published mod rights document was found.

---

## 2. What Is Moddable vs. Locked

**Status: DOCUMENTED (GUTS scope); PARTIALLY UNKNOWN (compiled internals)**

**Class system:** DOCUMENTED — fully moddable via GUTS data editor. Custom classes are created by cloning vanilla class base files and editing DAT properties. All four stock classes were built with GUTS; there is no class slot cap enforced by the engine — classes are data-registered. The single conflict point is the character-select screen layout file, which all class mods write to simultaneously, requiring manual merging when combining multiple class mods (source: [Steam PCGamingWiki](https://www.pcgamingwiki.com/wiki/Torchlight_II), [TorchlightFansite class guide](https://www.torchlightfansite.com/torchlight-2-forums/torchlight-2-modding/torchlight-2-modding-guide-threads/6723-create-custom-class-guts-images-stuff.html)). The 40+ class injection precedents (Classes Reborn, TL2-ACE, etc.) confirm no hard architectural ceiling.

**Combat math:** PARTIALLY DOCUMENTED — the majority of balance parameters live in DAT files and are freely editable (stat formulas, damage multipliers, skill values, armor reduction ranges). Community modders have confirmed editing DAT files for balance changes. However, certain low-level formulas (precise dodge/crit calculation functions) appear to be compiled — community discussions note searching the executable when DAT files didn't expose the exact coefficient (source: [Runic Forums defense thread](https://forums.runicgames.com/discussion/55943/how-stuff-works-defense), [Steam mechanics guide](https://steamcommunity.com/sharedfiles/filedetails/?id=251337108)). The split is: balance tuning parameters = DAT/data-driven and fully moddable; core combat resolution logic = likely compiled C++ and inaccessible. This is meaningful — Reincarnated's LLM-driven balance loop would operate on the data-driven tier, which is accessible.

**AI behavior:** DOCUMENTED as limited. "Enemy AI in Torch2 is fairly primitive and not very moddable" — community consensus. AI has data-driven patrol/aggro parameters (approach range, attack timing) that GUTS can edit, but behavior trees or pathfinding logic are not scriptable by modders. No modding wiki entry for custom AI scripting was located (source: [Steam GUTS discussion](https://steamcommunity.com/app/200710/discussions/0/810921274004811810/)).

**Asset pipeline (3D, sound, particles):** DOCUMENTED — custom 3D models are supported via Ogre mesh format (.OMD static, .OSM skinned). Runic released 3DSMax 2009 plugins (ExportOMD, ExportOSM, ExportOSA) as part of the GUTS Tools and Assets package, plus raw character/NPC/monster MAX files for reference. Particle effects support embedded 3D meshes. **Sound: NOT SUPPORTED through GUTS tools** — no audio pipeline tools were included in the GUTS package; the official blog post explicitly lists music/sound creation as outside GUTS scope. Sound replacement may be possible via direct file replacement in .pak but is not officially tooled (source: [Runic GUTS blog 2013](https://www.runicgames.com/blog/2013/04/01/guts/), [GUTS Tools and Assets wiki](https://docs.runicgames.com/wiki/GUTS_Tools_and_Assets)).

**World structure (dungeon/map system):** DOCUMENTED as hybrid. Maps use a chunk-based procedural system — pre-authored tile chunks are assembled randomly at runtime. GUTS supports authoring new level chunks and editing existing layouts. The procedural assembly parameters (seed logic, chunk weighting) are not documented as moddable and are likely compiled. Fixed maps (towns, named dungeons) are fully hand-authored and GUTS-editable. MapWorks (endgame portals) = procedural, parameters UNKNOWN/UNPUBLISHED for moddability (source: [Steam map generation discussion](https://steamcommunity.com/app/200710/discussions/0/1742216642525930331/)).

**UI / HUD:** DOCUMENTED — fully replaceable via .layout and .imageset files. GUTS has a dedicated UI layout editor tab. The GUTS Tools package includes raw UI assets and a texture sheet generator. Modding community norm: create unique texture sheets to avoid inter-mod conflicts with the UI layer (source: [GUTS Tools and Assets wiki](https://docs.runicgames.com/wiki/GUTS_Tools_and_Assets), [YouTube GUTS UI tutorial](https://www.youtube.com/watch?v=XnHuBO8mC-I)).

**Multiplayer / anti-cheat:** DOCUMENTED. TL2 does not use VAC. Mods require all players in a session to have the same mods active (mod state is session-matched). Modded characters can join vanilla MP games — the engine relies on a soft flagging system (character sheet tags cheated chars) rather than hard exclusion. No gameplay restrictions apply to mods in MP beyond mutual-possession requirement. This means: a Reincarnated class mod functions in co-op without additional unlocking friction (source: [Steam cheating discussion](https://steamcommunity.com/app/200710/discussions/0/864948856885377625/), [TorchlightFansite MP discussion](https://www.torchlightfansite.com/torchlight-2-forums/torchlight-2-general/5125-torchlight-2-questions-cheaters-multiplayer.html)).

---

## 3. Monetization Rights

**Status: DOCUMENTED prohibition; commercial gray zone for Patreon/donations**

The Runic ToU Section 6.4 explicitly prohibits "selling, licensing, or otherwise commercially exploiting 'mods' of the Game." This is unambiguous on direct mod sales. Downstream derivative works without written consent are also prohibited (Section 3.5).

**Patreon / donation model:** UNKNOWN/UNPUBLISHED as explicit policy. A Runic Games forum thread titled "Making money for creating mods" existed and was accessible in search index ([forums.runicgames.com/discussion/69774/](https://forums.runicgames.com/discussion/69774/making-money-for-creating-mods)) but the forum itself returned ECONNREFUSED — Runic's servers are dead or access-gated. Based on the search result snippet, community members discussed Patreon and donation links as possible revenue paths for modders, but no Runic staff response confirming this was acceptable was captured.

**SynergiesMOD Patreon:** No Patreon or donation link was found on either the SynergiesMOD Steam Workshop page or its Nexus page. Salan does not appear to have attempted to monetize the mod.

**Successor owner stance on monetization:** UNKNOWN/UNPUBLISHED. No statement from Perfect World, Gearbox Publishing, or Arc Games extending or narrowing the commercial prohibition has been located. The prohibitory Runic ToU language remains operative by default.

**Practical community norm:** Mods are distributed free. No precedent for TL2 mod monetization was found — not on Steam Workshop (which prohibits paid mods on most games anyway), not on Nexus (which allows optional donations but not paywalled mods), not on itch.io. The commercial prohibition appears respected in practice, though unenforced rather than enforced.

---

## 4. SynergiesMOD Legal Status

**Status: UNDOCUMENTED permission; no documented refusals; add-ons exist by tolerance, not grant**

**Author status:** Salan's last SynergiesMOD update was February 26, 2020 (v.1375, on Steam Workshop). The gap before that was May 2017 → January 2020 — a 2.5-year hiatus followed by a brief Paladin rework sprint then silence. No public posts or activity since early 2020 have been located (source: [SynergiesMOD changelog](https://steamcommunity.com/sharedfiles/filedetails/changelog/136232408)).

**License on Steam Workshop page:** None published. No Creative Commons, MIT, or any other license declaration appears on the mod's Steam Workshop page or its Nexus page (source: WebFetch of Steam Workshop page 136232408).

**License on Nexus page:** The Nexus page returned 403, preventing direct inspection of the mod description's license field. The ModDB entry for SynergiesMOD similarly contains no documented license.

**Third-party add-on posture:** Add-on mods compatible with SynergiesMOD exist on Steam Workshop (e.g., "SynergiesALL Addons" compilation, [id 377067621](https://steamcommunity.com/sharedfiles/filedetails/?id=377067621), the LowPop framerate mod). A Steam guide for "Creating a Mod Support for Synergy" exists ([id 1195636111](https://steamcommunity.com/sharedfiles/filedetails/?id=1195636111)) and advises: "You should not include any content from the actual mod unless you have permission from the creator" — indicating the modding community itself acknowledges Salan's permission is required but does not claim it has been granted. No record of Salan explicitly granting or refusing third-party build permission was found.

**Has anyone been told no?** No documented case of Salan objecting to an add-on or asking a modder to take down a SynergiesMOD-dependent add-on was found. The absence of objection over 5+ years of inactivity suggests tolerance, but tolerance from an absent author is not a license.

**Summary for Reincarnated:** Building a Reincarnated class mod as a SynergiesMOD add-on (the "nest" option) is legally ambiguous — the game's ToU prohibits derivative works without written consent, SynergiesMOD itself has no license, and Salan is unreachable. This confirms the previous finding that the SynergiesMOD-nest option is the highest-risk path. Building a standalone class mod (outside SynergiesMOD) avoids the Salan layer but still operates under the Runic ToU's derivative-works constraint.

---

## 5. Distribution Restrictions

**Status: DOCUMENTED norms; no active enforcement documented**

**Steam Workshop:** The standard mechanism for TL2 mods. .sch scheme files enable auto-sync. Workshop active as of May 2026 — new compilation mods posted as recently as 2025 (source: [Steam Workshop TL2 2025 collection](https://steamcommunity.com/sharedfiles/filedetails/?id=3424812391)). No sign of Workshop deprecation for TL2 — Steam continues hosting Workshop for games with far smaller communities.

**Nexus Mods:** Active with 1,400+ mods listed. TL2 has a Nexus community Discord ([Nexus TL2 Discord announcement](https://www.nexusmods.com/torchlight2/news/12870/)). Some larger mods are Nexus-exclusive due to Steam Workshop file-size limits ("too big for steam so now Nexus Exclusive" — multiple search result snippets). No takedown activity or enforcement actions against any Nexus-hosted TL2 mod were found.

**ModDrop / TorchlightFansite:** ModDrop backs the TorchlightFansite archive — mods are preserved against link rot. This is the community's archival layer.

**Direct .pak / .mod distribution:** No known enforcement against direct file distribution. The format is transparent (DAT plain text inside the .mod container) and widely shared.

**Community norms:** The modding community operates openly. No documented case of Arc Games / Gearbox / Perfect World issuing a DMCA takedown or cease-and-desist against any TL2 mod was located across forums, Reddit, ModDB, Nexus, or Steam. Passive tolerance has been consistent across all IP transitions since 2017.

**Arc Games support:** Arc Games maintains a Torchlight II support section and "Official Torchlight II Mods" page, suggesting active IP administration — but no enforcement activity against third-party mods.

---

## 6. Engine Lifespan / Fragility

**Status: DOCUMENTED stability; UNKNOWN for Arc Games future plans**

**Last patch:** v1.25.5.5, released 2017 (Runic's final patch before dissolution). No engine updates since. The version history wiki page returned 403, but Arc Games' own version history page at arcgames.com confirms the v1.25 lineage (source: [Arc Games version history](https://www.arcgames.com/en/arc-news/detail/5002923-torchlight-ii-version-history)).

**Stability for modders:** Frozen engine = zero patch-break risk. All mods built for v1.25 in 2013 still function in 2026. This is a significant modding advantage over active-development games. The community explicitly relies on this stability.

**Player population:** ~250 daily concurrent as of May 2026 (from commission brief). Peak 808 in August 2025 (Steam Charts). The player base is small but stable — consistent with a game that peaked at 88,000 concurrent at 2012 launch and has settled into a maintenance community.

**Steam Workshop infrastructure:** No signs of deprecation. Steam supports Workshop for games with far smaller concurrent counts than TL2's ~250. The Workshop infrastructure is maintained by Valve, not by Arc Games — Arc Games going dark would not affect Workshop availability.

**Arc Games / Embracer future plans for TL2:** UNKNOWN/UNPUBLISHED. Torchlight 3 is at <30 concurrent players and commercially dead. Torchlight Infinite (mobile GaaS) is the active franchise entry and is managed separately. No statement from Arc Games about a TL2 sequel, remaster, or any activity has been found. The IP appears parked. The risk is not active interference — it is complete IP abandonment, which paradoxically leaves the modding ecosystem as the game's de facto living layer.

**Fragility risk surface:**
- No patch-break risk (engine frozen) — LOW
- Workshop deprecation risk — LOW (Valve-managed, not IP-owner-managed)
- Community collapse risk — LOW-MODERATE (small but stable, 13-year persistence)
- IP-owner hostile action risk — LOW (no enforcement history across 4 ownership transitions)
- IP-owner beneficial action (e.g., SDK update, new modding rights grant) — VERY LOW (effectively zero chance)

---

## Open Questions

1. **Arc Games ToU — current operative text.** The fetched ToU is from torchlight2game.com (original Runic-era URL). Whether Arc Games has issued an updated ToU governing TL2 was not confirmed — the support.arcgames.com mod page returned 403. A direct check of the current Steam EULA (via Steam client, not web) could resolve whether the prohibitions in Section 6.4 are still verbatim operative under Arc Games.

2. **Runic forum monetization thread content.** The forums.runicgames.com server is dead or connection-refused, meaning the "Making money for creating mods" thread content was not retrieved. A Wayback Machine crawl of that specific thread URL could recover whether Runic staff made any informal permission statement regarding Patreon/donations.

3. **Salan contact viability.** Salan's last online activity has not been dated precisely — the last mod update was February 2020 but no profile activity date was confirmed. If the SynergiesMOD nest option is being considered, a direct Steam message to Salan is the only path to explicit permission; given 5+ years of silence, a response cannot be assumed.

4. **Combat formula compiled scope.** The exact boundary between DAT-editable balance parameters and compiled C++ combat math was not fully mapped. A practical test (editing specific DAT balance curves and measuring behavior) could confirm Reincarnated's LLM balance loop can operate on the accessible tier without needing compiled access.

5. **Procedural dungeon parameters.** Whether MapWorks portal generation parameters (chunk pool, tier weights) are DAT-exposed or compiled was not confirmed. For a spirit-swap mod integrating trial rooms, this could matter.

---

## Source List

- Runic Games Wikipedia: https://en.wikipedia.org/wiki/Runic_Games
- Torchlight Wikipedia: https://en.wikipedia.org/wiki/Torchlight
- Runic Games dissolution — Indie Game Website: https://www.indiegamewebsite.com/2017/11/06/runic-games-dissolved-by-parent-company-perfect-world-entertainment/
- Echtra Games and TL IP — The Gamer: https://www.thegamer.com/echtra-games-zynga-torchlight-3-perfect-world/
- Echtra Games closure June 2025 — Massively Overpowered: https://massivelyop.com/2025/06/03/og-torchlight-frontiers-aka-torchlight-3-studio-echtra-games-has-been-shuttered-by-zynga/
- Embracer acquires Perfect World — Embracer Group press release: https://embracer.com/releases/embracer-group-enters-into-agreement-to-acquire-perfect-world-entertainment/
- Embracer acquires Perfect World — GameSpot: https://www.gamespot.com/articles/embracer-group-acquires-torchlight-publisher-perfect-world-entertainment-in-125-million-deal/1100-6499200/
- Perfect World rebrands as Gearbox Publishing — Game Developer: https://www.gamedeveloper.com/business/perfect-world-rebrands-as-gearbox-publishing-after-embracer-purchase
- Perfect World / Arc Games rename — PC Gamer: https://www.pcgamer.com/hyper-light-breaker-publisher-perfect-world-is-now-gearbox-publishing/
- Runic Games Terms of Use (operative): https://www.torchlight2game.com/legal/terms-of-use
- Runic GUTS blog post (April 2013): https://www.runicgames.com/blog/2013/04/01/guts/
- GUTS modding overview: https://docs.runicgames.com/wiki/Modding_Overview.html
- GUTS Tools and Assets wiki: https://docs.runicgames.com/wiki/GUTS_Tools_and_Assets
- SynergiesMOD Steam Workshop page (v.1375): https://steamcommunity.com/sharedfiles/filedetails/?id=136232408
- SynergiesMOD changelog: https://steamcommunity.com/sharedfiles/filedetails/changelog/136232408
- SynergiesMOD Nexus page: https://www.nexusmods.com/torchlight2/mods/1
- SynergiesMOD ModDB: https://www.moddb.com/mods/synergiesmod
- Creating Mod Support for Synergy guide: https://steamcommunity.com/sharedfiles/filedetails/?id=1195636111
- SynergiesALL Addons: https://steamcommunity.com/sharedfiles/filedetails/?id=377067621
- Mod merging guide: https://steamcommunity.com/sharedfiles/filedetails/?id=2658349053
- TL2 multiplayer cheating discussion: https://steamcommunity.com/app/200710/discussions/0/864948856885377625/
- TL2 map generation discussion: https://steamcommunity.com/app/200710/discussions/0/1742216642525930331/
- TL2 Runic monetization forum thread (server dead, index only): https://forums.runicgames.com/discussion/69774/making-money-for-creating-mods
- TL2 Steam mechanics guide: https://steamcommunity.com/sharedfiles/filedetails/?id=251337108
- Arc Games TL2 modding support: https://support.arcgames.com/hc/en-us/sections/360003275973-Modding-Issues-Torchlight-II
- Arc Games official TL2 mods article: https://support.arcgames.com/hc/en-us/articles/360017720153-Official-Torchlight-II-Mods
- Nexus TL2 Discord announcement: https://www.nexusmods.com/torchlight2/news/12870/
- PCGamingWiki Torchlight II: https://www.pcgamingwiki.com/wiki/Torchlight_II
- TorchlightFansite: https://www.torchlightfansite.com/
- Arc Games version history: https://www.arcgames.com/en/arc-news/detail/5002923-torchlight-ii-version-history
