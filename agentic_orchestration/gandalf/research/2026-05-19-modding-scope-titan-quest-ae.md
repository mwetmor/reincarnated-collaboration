# Research — Titan Quest Anniversary Edition: Developer-Permission Scope and Modding Envelope — 2026-05-19

**Mode:** A (analytical)
**Commissioner:** Gandalf — Pattern-B secondary mod-target analysis
**Sources consulted:** THQ Nordic EULA (privacy.thqnordic.com/eula-en), THQ Nordic Video Policy, Steam Workshop TQAE page, titanquestfans.net forum (multiple threads), Nexus Mods TQAE listings, Crate Entertainment forum (TQ ReDawn, importing threads), Wikipedia (Iron Lore Entertainment, Crate Entertainment), PCGamingWiki (TQAE), Steam Community discussions (TQAE General Discussions), Titan Quest Fandom wiki (Art Manager, Modding Main Page, World Editor, Quest Editor)

---

## TL;DR

THQ Nordic's published EULA explicitly permits non-commercial mod sharing as private use but bars any direct or indirect commercial utilization without "prior written consent" — no indie-friendly modding carve-out exists and no published exception for Patreon or tip-jar models has been located. The technical envelope is wide for data-driven content (masteries fully replaceable, combat parameters tunable via DBR, AI behavior data-tunable, world and quest authoring fully supported) but hardcoded at the engine layer for the deepest math (core damage formula is fixed in the compiled binary, not in DBR files) and partially hardcoded for UI (compass bitmap, merchant window grid, certain HUD element positions are documented as locked). DLC fragmentation carries real friction: the Atlantis update broke ARC file loading and forced tool re-pointing for all existing mods; the Eternal Embers DLC is required by at least one major mastery overhaul (Legion of Champions); and the TQ ReDawn cross-port found TQAE's recent map format incompatible with both vanilla TQ and GD. No public Crate Entertainment statement on TQ IP concerns exists; the engine license runs from Iron Lore's former owners to Crate, predating THQ Nordic's IP acquisition, and no documented conflict has surfaced.

---

## 1. THQ Nordic's Modding EULA / Official Policy

**STATUS: DOCUMENTED (EULA text retrieved; no separate modding-specific policy document found)**

THQ Nordic publishes a unified EULA at `privacy.thqnordic.com/eula-en`. Key clauses extracted verbatim from that document:

- **Permitted (non-commercial sharing):** "Storage of software data, especially maps created with included level editors or mods created with an SDK is exclusively permitted to individual persons for private use. Private use also means the provision of data via the Internet for use by other individual persons for non-commercial purposes."

- **Prohibited (commercial):** "Any other reproduction, distribution, broadcasting, provision and any indirect or direct commercial utilization...is strictly prohibited without prior written consent from THQ Nordic GmbH."

- **IP assignment clause:** "For the sake of clarity all intellectual property created with the help of the software should be owned by THQ Nordic GmbH." Users additionally grant THQ Nordic "an exclusive, perpetual, irrevocable, fully transferable and sub-licensable worldwide right and license to use your contributions in any way and for any purpose."

- **Waiver:** Users waive "moral rights of paternity, publication, reputation, or attribution" on UGC.

**Comparative posture versus indie-developer modding relationships:** This EULA posture is materially more restrictive than Crate Entertainment's stance on Grim Dawn. Crate has not formally published a paid-mods prohibition and GD modders operate under an implied permissive tolerance. THQ Nordic's EULA explicitly names commercial distribution as requiring written consent and claims ownership of all IP created with the tools. There is no published modding-specific addendum that relaxes these terms for TQAE. The Steam Workshop TQAE page (206 items as of crawl date) provides no publisher-specific rules beyond directing users to "official documentation" — which resolves back to the EULA above.

No THQ Nordic press statement specifically addressing modding policy was found in the 2024–2026 window. The Video Policy page (separate document) addresses only video content monetization, not mods.

---

## 2. What Is Modifiable vs. Locked

### 2a. Mastery System Architecture

**STATUS: DOCUMENTED — FULLY REPLACEABLE**

The mastery system is entirely data-driven via DBR files. Art Manager's primary function is editing database records that define all mastery properties. Custom masteries are well-documented with a full wiki guide ("Create Your Own Masteries") and are the basis of the most substantial mods in the ecosystem (ShadowChampions, Legion of Champions, Grim Quest lineage). Modders can: add entirely new masteries, replace existing masteries, tune all skill parameters, add multi-mastery unlocks. The mastery architecture is architecturally identical to Grim Dawn's (Iron Lore alumni carried the design forward); the DBR schema is the same family.

**Documented limit:** The number of mastery tree slots has a ceiling; modders flagged "insufficient mastery tree slots" as a requested expansion in community feedback to THQ Nordic. The specific cap is not documented as an exact number in sources found.

### 2b. Combat Math (Damage Formulas)

**STATUS: PARTIALLY DOCUMENTED — DATA-LAYER TUNABLE, FORMULA STRUCTURE HARDCODED**

DBR-accessible parameters: all skill magnitude values, damage type percentages, resistance values, armor values, weapon damage ranges, elemental conversion rates, attack speed, crit chance, dodge chance. These all live in DBR files and are freely moddable.

The underlying damage calculation loop — the order of operations (hit check → crit → mitigation → resistance → absorption) — is compiled into the engine binary and is not exposed as a DBR parameter or script. Community damage formula documentation (the "In-depth Damage mechanics" Steam guide) reverse-engineered the formula from observed outputs but describes it as a fixed engine behavior rather than a moddable field. Modders can tune all the *inputs* to the formula heavily but cannot reorder or replace the formula structure itself without binary patching (which is outside the official modding scope and would void EULA compliance).

### 2c. AI Behavior

**STATUS: DOCUMENTED — DATA-TUNABLE, NO SCRIPTING LAYER**

Monster AI behavior parameters are in DBR files: reposition behavior, aggro range, skill priority weights, pursuit duration, flight-on-hit flags. Multiple mods demonstrate this — Monster Fixes mod retunes ranged AI reposition behavior; other mods tune pet AI aggression. These are tunable data fields.

No scripting layer (Lua, Python, custom bytecode) is exposed for AI. There is no equivalent of Skyrim's Papyrus or GD's Lua-accessible behavior trees accessible to modders. The underlying AI framework (documented in the prior research database as data-driven priority lists) is the boundary: modders can adjust priority weights and flags, but cannot author new behavioral logic from first principles. The implication for Reincarnated: if custom AI-authored encounter logic (not just stat tuning) is part of the export vision, it cannot be authored within the modding system.

### 2d. Asset Pipeline (Art Manager Scope)

**STATUS: DOCUMENTED — TEXTURES/ANIMATIONS YES; NEW 3D MESHES SEVERELY CONSTRAINED**

Art Manager officially supports: texture conversion, animation import, database record creation/editing, particle effects (via built-in particle tools), sound record authoring. World Editor and Quest Editor are officially included.

**The mesh toolchain was never released publicly.** The game developers explicitly stated they did not feel it worth releasing the mesh creation tools (source: Art Manager wiki discussion). As a result: importing brand-new custom 3D models is only possible via workarounds (modifying existing TQ meshes, using attachment points to place secondary meshes). The modding community developed a custom mesh import path that does NOT use official tools — it requires model-specific workarounds and cannot produce fully new character body geometry cleanly.

ArtManager also cannot archive mesh and animation files (documented limitation from the "Missing Records" Steam thread, confirmed by a THQ Nordic developer "GrimVince" who noted a pending patch for related issues). This is a meaningful constraint for Reincarnated's visual authoring needs if new character art is part of the scope.

### 2e. World Structure / Quests

**STATUS: DOCUMENTED — FULL WORLD AND QUEST AUTHORING AVAILABLE**

The World Editor supports full map creation: terrain levels (overground) and grid levels (underground/interior), entity placement, texture painting, pathing files, minimap generation, and Layout mode for hooking quests to maps. The Quest Editor supports trigger/condition/action logic for quest scripting. This is a complete world and quest authoring stack — not locked.

**Practical DLC-induced friction noted:** each DLC update shipped a new MapCompiler.exe; modders must point Art Manager's Tools Directory to the latest DLC's directory to compile maps correctly. This caused broken builds for existing mods post-Atlantis until modders re-pointed the compiler path.

### 2f. UI / HUD

**STATUS: PARTIALLY DOCUMENTED — TEXTURE-LEVEL REPLACEABLE; LAYOUT PARTIALLY HARDCODED**

UI texture/bitmap replacement is possible. The modding tutorials include a "Modding the Titan Quest UI by Kirii" PDF, confirming UI texture work is within scope.

**Documented hardcoded elements (from community forum research):**
- Compass bitmap: certain elements are hardcoded in position and cannot be moved or deleted
- Merchant window grid: does not expand despite template options suggesting it could
- Character window: cannot overlap certain lower HUD areas
- HUD element positions: constrained — a 2016 dev response (GrimVince) to the "missing records" thread acknowledged some UI-related issues but did not claim they were resolved

UI layout structural replacement (repositioning the entire HUD, implementing a new HUD paradigm) is not achievable through official modding tools alone. Texture skinning is achievable. This aligns with the Wave-2A revision note flagging "UI authoring overhead."

### 2g. Affix Library Architecture

**STATUS: DOCUMENTED — MUST SLOT INTO EXISTING TABLE STRUCTURE; CANNOT BYPASS**

The affix system uses a library of LootRandomizer template DBR files stored in `records\item\lootmagicalaffixes\` (base game) and `records\xpack\item\lootmagicalaffixes\` (DLC variants). New affixes must be created in this structure and registered in difficulty/act-specific loot tables. The tutorial ("Add yellow/green affixes to the game" on titanquestfans.net) confirms this is the only documented authoring path.

**Bypass status:** No mechanism for bypassing the affix table system entirely was found. Mods cannot inject items with inline rolled effects outside the library structure — affixes must be authored as library entries and wired into loot tables, then procedurally selected by the loot engine at runtime. This is a meaningful structural delta from Reincarnated's approach (inline `rolled_effects` per item vs. library lookup). Translation layer required.

**Documented constraint:** LootRandomizerTable.tpl has limited slots, forcing modders to spread affix tables across multiple files for large content sets.

---

## 3. Monetization Rights

**STATUS: DOCUMENTED (EULA); EMPIRICALLY UNKNOWN (NO KNOWN VIOLATIONS OR LICENSED EXCEPTIONS)**

The EULA is explicit: commercial distribution requires prior written consent from THQ Nordic. There is no published blanket commercial permission, no "Verified Creators" program (like Bethesda's), and no Nexus Mods publisher-approved paid-modding entry for THQ Nordic found.

**Empirical survey of active mods:** No TQAE mod with active Patreon, paid Nexus, or itch.io commercial listing was found in this crawl. ShadowChampions Multimaster (1.7 GB, Mar 2025), Legion of Champions Reloaded (active May 2026), TQ-Retold — all distributed free. This is consistent with the EULA prohibition, not contradicting it. Absence of a paid mod does not confirm THQ Nordic would deny consent if asked, but no documented instance of consent being granted was found.

**THQ Nordic's broader commercial posture:** THQ Nordic is a subsidiary of Embracer Group (formerly), a multi-IP holding company. Their EULA's IP-assignment clause ("all IP created with the tools is owned by THQ Nordic GmbH") is a stronger assertion than typical indie studios make. This creates non-trivial legal exposure for any commercial use of mod-exported Reincarnated content even if distributed under the "mod for TQAE" framing.

---

## 4. DLC Fragmentation Impact

**STATUS: DOCUMENTED (with specific breakage instances)**

TQAE has three paid DLCs that compound modding surface:

- **Ragnarök** — Act 5 campaign extension; adds Rune Mastery. Modders must point Art Manager to the Ragnarök tools directory for map compilation involving Nordic content.
- **Atlantis** — Act 4.5 optional content. The Atlantis update (v2.x) broke compressed ARC file loading engine-wide, forcing all existing mods to replace `.arc` archives with uncompressed folder structures. It also shipped a new MapCompiler.exe that broke map compilation for mods still pointing to the older Immortal Throne tools directory. Multiple mods became non-functional post-Atlantis until rebuilt.
- **Eternal Embers** — Legendary-tier exclusive content; adds Neidan Mastery. Legion of Champions **requires** Eternal Embers as a hard dependency. The TQ ReDawn cross-port explicitly stated Eternal Embers map format is "not compatible with either vanilla TQ or GD" and thus untransferable.

**Worst-case mod versioning question:** Sources do not document modders shipping 4 discrete versions (base/+R/+A/+A+R+EE). The observed pattern is:
- Mods targeting base campaign typically work without DLCs
- Mods using DLC masteries (Rune, Neidan) require those DLCs
- Mods using DLC map areas require the DLC
- The Atlantis-era ARC breakage was a one-time infrastructure disruption, not an ongoing DLC-version branching requirement

The practical fragmentation concern is not 4 parallel versions but rather: (a) content authored using DLC masteries forces all users to own that DLC, and (b) any future TQAE patch could again shift the ARC format or MapCompiler binary, as has happened before. This is an ongoing maintenance risk, not a solved problem.

---

## 5. Distribution Restrictions

**STATUS: PARTIALLY DOCUMENTED**

**Steam Workshop:** TQAE Workshop is live with 206 items. The Workshop "about" page provides no TQAE-specific content policies beyond directing to "official documentation." Steam's general Workshop Terms of Service (Valve) govern, plus THQ Nordic's EULA non-commercial clause applies. Mod installation via Workshop auto-subscribes; however, Workshop mods are loaded via the Custom Maps path (`My Documents\My Games\Titan Quest Immortal Throne\CustomMaps`) — they do not inject into the base game directory, which has implications for the multiplayer restriction discussed below.

**Multiplayer distribution constraint (documented):** Mods adding new masteries, skills, or monsters do not work in multiplayer unless all players have the mod installed. The engine's `CleanseDatabase` function unloads mod data on returning to menu. Community workarounds (Cheat Engine bypass, "hardmod" DLL hex edit) exist but are outside official scope and potentially EULA-violating.

**titanquestfans.net:** Primary community forum with dedicated mod boards (Legion of Champions, Titanomachy, Deities, Enhanced Gameplay, etc.). No posted THQ Nordic policy distinguishing titanquestfans.net distribution from Workshop. THQ Nordic has an official board on titanquestfans.net for announcements but it does not address modding permissions.

**Nexus Mods:** TQAE has an active Nexus presence. No THQ Nordic-specific policy found for TQAE on Nexus. Nexus Mods' publisher-approved paid modding program (documented as existing) does not list THQ Nordic as a participating publisher in sources found.

**No documented conflict** between Steam Workshop and external site distribution was found. Mods appear on both platforms concurrently without publisher action.

---

## 6. IP / Lineage Constraints

**STATUS: PARTIALLY DOCUMENTED (ownership chain); UNDOCUMENTED (active conflict)**

**IP chain:**
- Iron Lore Entertainment created Titan Quest (published by THQ, 2006); Iron Lore closed January 2008
- THQ purchased IP rights; Nordic Games (later renamed THQ Nordic) acquired Titan Quest IP from THQ's bankruptcy estate (~2013-2014)
- THQ Nordic currently holds the Titan Quest IP and published TQAE (2016) and commissioned TQII (2025, Grimlore Games)
- Crate Entertainment was founded February 2008 by former Iron Lore lead designer Arthur Bruno; Crate licensed the *engine* (not the IP) from Iron Lore's former owners in summer 2009 — separate from the IP acquisition by Nordic Games
- Grim Dawn runs on the licensed TQ engine; Crate built GD's own IP (not TQ characters/world/lore)
- One community speculation suggests THQ Nordic may now own the engine as well (since they acquired the IP and Iron Lore's assets), but no documentation confirms whether Crate's license predates or survives THQ Nordic's ownership transfer

**Active conflict status:**
- No documented instance of THQ Nordic taking action against TQAE mods
- No documented instance of THQ Nordic taking action against Crate for GD's engine lineage
- TQ ReDawn (porting TQ world content into GD engine) runs on the Crate forum without official challenge or commentary — a significant empirical data point, though absence of action is not endorsement
- Crate Entertainment has made no public statement on TQ IP concerns in sources found
- The ASYLUM101 comment on the Crate forum ("TQ models don't transfer over easily — armor pieces must be adapted in 3dsmax") describes a technical barrier, not a legal one — no IP-chill language used

**Reincarnated-specific concern:** The scenario relevant to Reincarnated is not TQ content appearing in Reincarnated, but Reincarnated content being exported into TQAE. The EULA IP-assignment clause would technically grant THQ Nordic rights over Reincarnated-generated content distributed as a TQAE mod. This is the more pointed risk for this project.

---

## Open Questions

1. **Has any mod author ever sought and received (or been denied) written consent from THQ Nordic for commercial distribution?** No evidence found in either direction. Direct inquiry to THQ Nordic support would be the only resolution path.

2. **Does the Crate engine license survive THQ Nordic's IP acquisition, or did THQ Nordic inherit a claim over the engine Crate licensed?** Wikipedia and community sources suggest the license predated THQ Nordic's acquisition, but no primary source confirms current legal status. Relevant only if engine-level similarities between TQ/GD output trigger claims.

3. **What is the exact mastery tree slot ceiling?** Community posts request expansion but no exact integer limit is documented. Testing required.

4. **Could future TQAE patches again break the ARC pipeline or MapCompiler path?** Historically yes (Atlantis did). No forward commitment from THQ Nordic on modding stability has been found.

5. **Is there a Titan Quest II (TQII, Aug 2025 Early Access) modding policy that signals THQ Nordic's evolving posture?** TQII's Steam page references a Workshop tab but no modding policy statement found as of this crawl. TQII is on a new engine (not the Iron Lore engine); its modding stance may not carry over to TQAE.

6. **Does the IP-assignment clause in the EULA create a specific legal exposure for Reincarnated-generated content published as a TQAE mod?** Legal interpretation question outside scout scope. The clause text is documented; the legal risk assessment is Gandalf/Matt's call.

---

## Source List

- THQ Nordic EULA (English): https://privacy.thqnordic.com/eula-en (accessed 2026-05-19)
- THQ Nordic Video Policy: https://www.thqnordic.com/company/video-policy (accessed 2026-05-19)
- Steam Workshop TQAE: https://steamcommunity.com/workshop/about/?appid=475150 (accessed 2026-05-19)
- Steam Community — Guides/Tools pinned thread: https://steamcommunity.com/app/475150/discussions/0/3814032755159107467/ (accessed 2026-05-19)
- Steam Community — "Editor: Missing Records! Modding is limited!": https://steamcommunity.com/app/475150/discussions/0/343787920126333098/ (accessed 2026-05-19)
- Steam Community — "Mods and how it works": https://steamcommunity.com/app/475150/discussions/0/1742227898986186478/ (accessed 2026-05-19)
- Steam Community — In-depth Damage Mechanics Guide: https://steamcommunity.com/sharedfiles/filedetails/?id=2382433615 (accessed 2026-05-19)
- Steam Workshop — Legion of Champions: https://steamcommunity.com/sharedfiles/filedetails/?id=2912073811 (accessed 2026-05-19)
- titanquestfans.net — "Add yellow/green affixes to the game" tutorial: https://titanquestfans.net/index.php?topic=888.0 (accessed 2026-05-19)
- titanquestfans.net — "Atlantis update messes with mods": https://titanquestfans.net/index.php?topic=958.0 (accessed 2026-05-19)
- titanquestfans.net — "Mod Pathing Problems - Atlantis Expansion Issues [SOLVED]": https://titanquestfans.net/index.php?topic=994.0 (accessed 2026-05-19)
- titanquestfans.net — "[Guide] Bypassing mod restrictions in multiplayer": https://titanquestfans.net/index.php?topic=1869.0 (accessed 2026-05-19)
- titanquestfans.net — "Suggestions for expanding the modding limits": https://titanquest.4fansites.de/forum/viewtopic.php?t=12949 (accessed 2026-05-19)
- titanquestfans.net — THQ Nordic board: https://titanquestfans.net/index.php?board=269.0 (accessed 2026-05-19)
- titanquestfans.net — Modding Tutorials A-Z: https://titanquestfans.net/index.php?topic=935.0 (accessed 2026-05-19)
- Titan Quest Fandom Wiki — Art Manager: https://titanquest.fandom.com/wiki/Art_Manager (accessed 2026-05-19)
- Titan Quest Fandom Wiki — World Editor: https://titanquest.fandom.com/wiki/World_Editor (accessed 2026-05-19)
- Titan Quest Fandom Wiki — Quest Editor: https://titanquest.fandom.com/wiki/Quest_Editor (accessed 2026-05-19)
- Nexus Mods TQAE — Multi-Class Mastery Mod: https://www.nexusmods.com/titanquestanniversaryedition/mods/25 (accessed 2026-05-19)
- Nexus Mods TQAE — ShadowChampions Multimaster: https://www.nexusmods.com/titanquestanniversaryedition/mods/93 (accessed 2026-05-19)
- Nexus Mods TQAE — Legion of Champions 2024 Source: https://www.nexusmods.com/titanquestanniversaryedition/mods/64 (accessed 2026-05-19)
- Crate Entertainment Forum — TQ ReDawn Mod thread: https://forums.crateentertainment.com/t/mod-tq-redawn-mod-v1-1-0-act-2-available/141821 (accessed 2026-05-19)
- Crate Entertainment Forum — Opinions on Legion of Champions: https://forums.crateentertainment.com/t/opinions-on-legion-of-champions-mod/46809 (accessed 2026-05-19)
- Crate Entertainment Forum — Importing stuff from Titan Quest: https://forums.crateentertainment.com/t/importing-stuff-from-titan-quest/31916 (accessed 2026-05-19)
- Nexus Mods — Publisher-Approved Paid Modding Policy thread: https://forums.nexusmods.com/topic/13501488-publisher-approved-paid-modding-policy/ (accessed 2026-05-19, 403 on fetch — listed as attempted source)
- Wikipedia — Iron Lore Entertainment: https://en.wikipedia.org/wiki/Iron_Lore_Entertainment (accessed 2026-05-19)
- Wikipedia — Crate Entertainment: https://en.wikipedia.org/wiki/Crate_Entertainment (accessed 2026-05-19)
- Wikipedia — Titan Quest: https://en.wikipedia.org/wiki/Titan_Quest (accessed 2026-05-19)
- PCGamingWiki — Titan Quest Anniversary Edition: https://www.pcgamingwiki.com/wiki/Titan_Quest_Anniversary_Edition (accessed 2026-05-19)
- Titan Quest official site (THQ Nordic): https://titanquest.thqnordic.com/ (accessed 2026-05-19)
