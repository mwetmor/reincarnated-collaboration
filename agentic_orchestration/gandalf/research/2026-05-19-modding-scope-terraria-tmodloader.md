# Research — Terraria / tModLoader Developer-Permission Scope — 2026-05-19

**Mode:** A (analytical)
**Commissioner:** Gandalf (Pattern-B analysis — Phase 3 Option B mod-export target)
**Sources consulted:** See Source List. Primary: Re-Logic official wiki, tModLoader GitHub (docs, wiki, issues), tModLoader Steam TOS, Steam patch notes. Secondary: PC Gamer, GamesRadar, TechRaptor, PCGamesN. Tertiary: Steam community forums, Fargo's Mods wiki.

---

## TL;DR

Re-Logic is genuinely one of the most modder-friendly major studios in the industry: tModLoader ships as a free official Steam DLC, two tModLoader community developers have been hired to Re-Logic's payroll (2022 and 2024), and the EULA explicitly permits decompilation for compatibility. The hard constraint for Reincarnated is not permission — it is architecture. tModLoader has no runtime JSON content path: all new items, damage classes, and NPC types must be registered at mod-load time in compiled C#. The kRPG mod demonstrates that a pre-allocated slot approach (a fixed pool of C#-registered "placeholder" items whose stats are overwritten at runtime via ModConfig/ServerConfig JSON) is a functioning workaround, but it caps procedural variety at the size of the pre-allocated pool and introduces a CI/compile-rebuild discipline. A second structural risk is patch fragility: Terraria 1.4.5 ("Bigger and Boulder") launched late 2024 and full tModLoader compatibility is still in progress as of May 2026 — the 1.4.4 precedent took nine months. Mods targeting the stable 1.4.4 tModLoader branch continue to work during the gap, but any major new Terraria release creates a multi-month dead zone for mods relying on cutting-edge base-game content.

---

## 1. Re-Logic + tModLoader Official Policy

**Status: DOCUMENTED**

tModLoader is distributed as a free Steam DLC alongside the base game (Steam App ID 1281930), which constitutes an explicit Re-Logic endorsement. The tModLoader Terms of Service (Steam EULA) confirm that tModLoader software is released under the **MIT License**, permitting use, modification, distribution, and sublicensing. Re-Logic's own modding policy (recorded in community forum EULA posts) allows modification of Terraria PC within bounds: decompilation for compatibility is permitted; bypassing Steam DRM is prohibited; distribution of unmodified source is prohibited.

The "officially endorsed but community maintained" framing is accurate but should be sharpened: as of 2024, Re-Logic has actively integrated tModLoader into its own payroll. Two tModLoader developers now work at Re-Logic:

- **Chicken Bones (David Jakes)** — hired May 2022 as Systems Programmer, tModLoader team
- **jopojelly (Javid Pack)** — hired May 2024 as tModLoader Developer, announced in the May 2024 Terraria State of the Game; per the announcement, he "will continue to work on collaborating with the tModLoader community on adding new features and bug fixes"

This is not contractor-level involvement — these are full employees. The practical effect: tModLoader is increasingly an internal Re-Logic product for maintenance and roadmap purposes, even if the community TML Team continues to drive the majority of development. The May 2024 announcement also represents Re-Logic's most recent explicit public statement on tModLoader support, and it is strongly affirmative.

The tModLoader TOS includes one important disclaimer for Reincarnated: "Although tModLoader is endorsed by Re-Logic, none of the mods downloadable via it are officially endorsed." Individual mods remain third-party software — Re-Logic's endorsement extends to the platform, not to any particular mod's content or fitness.

---

## 2. What's Modifiable vs Locked

### 2a. Class equivalent (DamageClass injection)

**Status: DOCUMENTED — full injection, compile-time registration required**

`DamageClass` is a fully hookable abstract class. Mods subclass it and register custom damage classes with full control over:
- `GetEffectInheritance` — which armor/accessory bonuses the class inherits
- `GetStatInheritance` — which stat bonuses (damage%, crit%) it benefits from
- `GetPrefixInheritance` — prefix behavior

Thorium Mod's pattern (`thoriumMod.TryFind("BardDamage", out DamageClass damageClass)`) is now partially superseded — tModLoader 1.4 added native `ModContent.TryFind` as the ecosystem standard. Both approaches are documented and functional. Cross-mod DamageClass consumption is well-trodden territory.

Constraint: DamageClass types must be registered at mod load. You cannot create a new named damage class at runtime from a JSON payload.

### 2b. Combat math (damage calculation, armor, crit)

**Status: DOCUMENTED — modifier-stack model, not full formula replacement**

tModLoader exposes combat math through a layered hook system rather than a replaceable formula function. Key hooks:

- `GlobalNPC.ModifyIncomingHit` — custom damage formula for all incoming NPC damage; allows rewriting defense calculation and crit multiplier logic
- `GlobalNPC.ModifyHitByItem/Projectile` — per-source damage modifier injection
- `GlobalItem.ModifyWeaponDamage` — temporary weapon damage modification based on buffs
- `ModPlayer.PostUpdateEquips` — post-equipment stat modification

**Assessment:** You can achieve functional equivalence to Reincarnated's damage formula chain by layering these hooks, but you cannot replace Terraria's underlying combat loop wholesale. Armor mitigation, hit registration, and projectile physics are Terraria-native. This means the translation overhead is real — Reincarnated's formula (attribute scaling, substrate matrix, pack proxy multiplier, per-hit variance bands) must each be mapped to a tModLoader hook injection point. Some elements (e.g., pack proxy) have no direct analog and require NPC AI workarounds.

### 2c. AI behavior (ModNPC AI hooks)

**Status: DOCUMENTED — full custom AI available**

`GlobalNPC` exposes:
- `PreAI` — returning `false` stops all vanilla AI execution; full replacement is possible
- `AI` — runs only if `PreAI` returns true
- `PostAI` — always runs

This is full override capability. Mods like Calamity implement entirely novel boss AI patterns with no vanilla AI involvement. No locked engine AI that cannot be bypassed.

### 2d. Asset pipeline

**Status: DOCUMENTED — full custom**

Terraria and tModLoader are fully open to custom pixel art, audio, and shader replacement within mod assemblies. Assets are bundled in `.tmod` files. Re-Logic has never restricted custom asset authoring. The constraint is presentation: Terraria is 2D side-scrolling with a fixed camera and tile grid, requiring 16-64px native pixel art re-authoring of any Reincarnated visual assets.

### 2e. World generation

**Status: DOCUMENTED — full custom, additive**

`ModSystem` (formerly `ModWorld`) provides hooks for adding custom world generation passes. Mods can inject biomes, structures, and terrain features that generate in new worlds. Custom procedural world generation is well-documented and widely used. The "Advanced World Generation" Steam Workshop mod demonstrates sophisticated procedural structure placement. Constraint: world gen passes that are computationally expensive freeze gameplay during execution in both singleplayer and multiplayer — relevant for any Reincarnated "trial room" or substrate-specific zone generation.

### 2f. UI / HUD

**Status: DOCUMENTED — full custom via ModSystem + UIState**

`ModSystem.ModifyInterfaceLayers` is the current standard hook for adding or replacing HUD elements. Custom `UIState` instances can be drawn at any screen position. Full HUD replacement is achievable — mods like "Fancy UI" and "Better Game UI" on Workshop demonstrate wide scope. Some vanilla HUD elements (hearts, mana stars) can be hidden or replaced via resource draw hooks in `ModPlayer`.

### 2g. Multiplayer — sync requirements

**Status: DOCUMENTED — strict mod-version matching, no built-in anti-cheat flexibility**

All players in a tModLoader session must have identical mod sets, identical versions, and identical load order. Server-side `ModConfig` (`ConfigScope.ServerSide`) is automatically synchronized to connecting clients — this is the mechanism the pre-allocated slot workaround relies on for distributing procedurally generated content data at session join. There is no Steam-level anti-cheat layer for mods; trust is purely mod-list matching. A Reincarnated season mod would require all players in a session to have the same season build installed — feasible for the Workshop auto-update model, but the version-sync requirement means a season update mid-session is not possible.

---

## 3. Monetization Rights

**Status: DOCUMENTED with nuance on Patreon pattern**

Re-Logic's EULA policy (community forum statement): "You are allowed to make modifications to Terraria PC, but you are not allowed to sell mods for profit." Direct paid mods — Steam paid workshop items or separate storefronts charging for a mod — are prohibited.

**Patreon model:** Multiple major mods operate Patreon pages without known Re-Logic enforcement action:

- **Calamity Mod** — active Patreon; the team was publicly invited by Redigit in June 2024 ("which of you wants to work for Re-Logic and get paid for your work?"), indicating Re-Logic's posture toward the team is supportive, not adversarial. The mod itself remains free; Patreon supports development costs.
- **jopojelly** — maintained a personal Patreon for his tModLoader utility mods before his 2024 hiring; Re-Logic hired him from that position.
- **Fargo's Mods** — has a Patreon with named "Patreon content" items, but per their wiki, these items are accessible to all players regardless of donation status; the Patreon names are tribute items, not paywalled gameplay.

**Pattern:** The de facto standard is Patreon-for-development-support with the mod itself remaining free and fully functional for all users. Re-Logic has never publicly moved against a Patreon-supported mod. Exclusive gameplay content behind a paywall would be a different and untested case — no documented precedent exists for Re-Logic tolerating actual gameplay gating.

**For Reincarnated:** A subscription or per-season charge for the mod would almost certainly violate the spirit of Re-Logic's "no profit" policy. A free mod with optional Patreon development support is the documented viable model. No direct revenue from the Terraria distribution channel.

---

## 4. Runtime JSON Workaround Precedents

**Status: DOCUMENTED (ModConfig mechanism); kRPG implementation details PARTIALLY DOCUMENTED**

This is the dealbreaker axis. tModLoader's content registration is compile-time only — items, NPCs, damage classes, and buffs must be registered in C# at mod load. There is no runtime content injection API. However, two workaround vectors exist:

### Vector A: Pre-allocated slot + ServerConfig/ModConfig JSON (kRPG pattern)

kRPG (Kalciphoz's RPG Mod) implements procedurally generated weapons as follows: the mod compiles a fixed pool of `ModItem` subclasses with placeholder identifiers. At runtime, item stats (damage, modifiers, procedural name, element assignments) are not stored in the C# class — they are generated procedurally and written into persistent world/player data structures or driven by `ModConfig` ServerSide JSON. When a player receives a "procedurally generated weapon," they receive one of the pre-allocated item types with stats read from the runtime data layer.

This pattern works but has a hard ceiling: the variety of simultaneously-existing procedural items is bounded by the number of pre-allocated slots compiled into the mod. kRPG gets away with this because most procedural variation is stat-level (magnitude, element, prefix), not type-level (new geometry, new projectile shape). For Reincarnated's season model — which generates new classes, skills, and monster types per season — the slot requirement scales with season complexity, not just stat variation.

**tModLoader ModConfig capabilities confirmed:**
- `ConfigScope.ServerSide` configs are automatically synced to all connecting clients in multiplayer
- Supports arbitrary JSON-serializable C# types (reference types with `Clone()` override, nested objects, arrays)
- Files persist at `Terraria/tModLoader/ModConfigs/<ModName>_<ConfigName>.json`
- No documented size limit, though large configs have not been benchmarked in community discussions

### Vector B: CI/compile-and-republish pipeline

GitHub Actions tooling exists for automated tModLoader mod builds (`ModLoaderTools` GitHub Marketplace action). The Workshop publishing pipeline supports automated updates triggered by `build.txt` version increments — the tModLoader Workshop wiki explicitly notes "modders can also use GitHub Actions to publish a mod update whenever build.txt is updated." No documented frequency cap on Workshop updates. Calamity publishes roughly monthly updates; more frequent publishing has no known prohibition.

A Reincarnated seasonal CI pipeline — Reincarnated engine generates season content as JSON → a transpiler converts to C# mod source → GitHub Actions builds and publishes to Workshop — is technically constructible. The rebuild-and-republish cycle would be the season cadence clock. Players would receive the update via Workshop auto-update. The constraint is: session participants must all be on the same mod version, so seasons cannot update mid-session, and there would be a window between publish and all-players-updated.

**Assessment of viability ceiling:** The CI pipeline approach has no technical blocker other than the transpiler build (JSON → C# class generation is straightforward). The operational cost is the compile-and-publish cycle time (likely 5-15 minutes for a well-optimized pipeline) and the player update latency. This is workable for a season-cadence model (weekly or monthly season drops) but not for real-time procedural generation per fight or per player.

---

## 5. Distribution Restrictions

**Status: DOCUMENTED**

**Workshop as primary channel:** Steam Workshop is the canonical distribution path. The tModLoader in-game Mod Browser draws from Workshop and a tModLoader-operated mirror (`mirror.sgkoi.dev`). The Mod Browser is a Re-Logic-blessed component of the tModLoader product — it is not a separate third-party tool; it ships with tModLoader.

**Mod size:** No documented hard size limit. The tModLoader GitHub has flagged that large `.tmod` files should be audited for accidentally included source files. Calamity Mod is among the largest Terraria mods (assets, audio, textures) and publishes without issue, establishing practical proof that multi-hundred-MB mods are supported. The `buildIgnore` directive in `build.txt` is the tool for controlling what gets packaged.

**Publishing pipeline:** `build.txt` version increment → in-game build → Workshop publish (or GitHub Actions automation). Players auto-update via Steam Workshop subscription. No documented review approval delay for updates to existing published mods, though as of 2024 new mod submissions go through a moderation queue for code review before first publication.

**Cross-mod compatibility:** Three patterns in use — `ModContent.TryFind` (ecosystem standard as of 1.4), `ModLoader.TryGetMod` + null check (for optional dependencies), and `Mod.Call` (cooperative messaging for mods that publish explicit call specifications). Thorium's TryFind pattern is widely referenced as a reference implementation but is not the only approach. No mandatory cross-mod compatibility standard exists; these are documented conventions.

**Mod Browser / third-party:** The primary discovery surface is the Steam Workshop page and the in-game Mod Browser (Workshop-backed). No significant independent third-party Terraria mod host exists at the scale of, say, Nexus Mods for Bethesda games — Workshop + in-game browser is the ecosystem.

---

## 6. Engine Fragility / Cadence

**Status: DOCUMENTED**

**Monthly tModLoader release cycle:** tModLoader follows a three-stage monthly cadence — Development month → Preview/freeze → Stable release at month start. Modders receive advance notice of breaking changes through Discord `#preview-update-log`. Breaking changes are classified as Runtime Breakage (requires immediate mod update) or Source-code Breakage (update after stable). Backwards compatibility is not guaranteed between monthly releases, but well-maintained mods track the Preview branch.

**Terraria major patch fragility — current live case:**

Terraria 1.4.5 ("Bigger and Boulder") released late 2024. As of the March 2026 tModLoader stable patch notes, full 1.4.5 compatibility is still in progress. The tModLoader team's public statement: "Updating tModLoader to major Terraria releases is a huge undertaking" and "will take many months yet." Historical precedent: the 1.4.4 update took nine months for full tModLoader compatibility.

The mitigation: tModLoader 1.4.4 (stable) continues to receive maintenance updates and is fully functional. Mods targeting 1.4.4-stable continue to work. Players can opt into the 1.4.4 tModLoader branch while 1.4.5 support matures. This means there is no hard "all mods break" event — rather, a gradual migration window in which new players on vanilla 1.4.5 cannot use mods until tModLoader catches up.

**Has Re-Logic ever broken modding intentionally?** No documented instance. Community discussions (Steam forum threads framing tModLoader 1.4 as adversarial) reflect frustration with patch lag rather than intentional sabotage. Re-Logic's hiring of Chicken Bones and jopojelly demonstrates active investment in keeping the modding pipeline functional.

**Long-term Re-Logic commitment:** The hiring trajectory (2022, 2024) and the free DLC distribution model are the strongest available signals. There is no public commitment document, but structural evidence (two employees, official Steam product, monthly blog coverage) is consistent with a multi-year commitment horizon. The absence of a paid DLC monetization model for tModLoader itself means Re-Logic has no financial incentive to abandon it.

---

## Open Questions

1. **Pre-allocated slot ceiling for a Reincarnated season:** kRPG's exact slot count and the stat-variation ceiling achieved within it are not publicly documented. The kRPG GitHub README describes the capability but not the implementation cardinality. Directly reading the kRPG C# source (`/Content` directory) would resolve this. **Relevance:** determines whether the pre-allocated pattern can support a full Reincarnated season (N classes × M skills × P monster types) or only stat-level variation.

2. **ModConfig ServerSide sync size limits in practice:** No community benchmarks on ModConfig payload size vs sync performance. A Reincarnated season's JSON content could be 50-500KB depending on depth. Whether this causes noticeable MP session-join latency is unknown. **Relevance:** direct operational risk for MP viability.

3. **Workshop moderation queue timing for new mod initial submission:** The 2024 moderation queue introduction is documented but queue duration is not. Subsequent updates to existing mods appear to bypass the queue. **Relevance:** one-time onboarding friction, not ongoing.

4. **Explicit Re-Logic policy statement on Patreon early-access gameplay gating:** No public document exists. The current Patreon practice across major mods is free-mod-plus-development-support. Whether Re-Logic would tolerate a Reincarnated subscription model for season content is unknown — the EULA's "no selling mods for profit" language would likely cover it, but enforcement is undocumented. **Relevance:** if Reincarnated's commercial model requires per-season revenue from Terraria players, this is an unresolved blocker.

5. **CI pipeline build time for a full season mod:** No published benchmark for tModLoader mod compilation time at Calamity-scale. A transpiler pipeline (Reincarnated JSON → C# → tmod) would need profiling. **Relevance:** determines season cadence ceiling for the compile-and-publish workaround.

---

## Source List

1. tModLoader Steam TOS/EULA: https://store.steampowered.com/eula/1281930_eula_0
2. tModLoader official site: https://www.tmodloader.net/
3. tModLoader on Steam: https://store.steampowered.com/app/1281930/tModLoader/
4. Re-Logic official wiki: https://terraria.wiki.gg/wiki/Re-Logic
5. tModLoader official wiki: https://terraria.wiki.gg/wiki/TModLoader
6. tModLoader DamageClass API docs: https://docs.tmodloader.net/docs/preview/class_damage_class.html
7. tModLoader ModNPC API docs: https://docs.tmodloader.net/docs/stable/class_mod_n_p_c.html
8. tModLoader GlobalNPC API docs: https://docs.tmodloader.net/docs/stable/class_global_n_p_c.html
9. tModLoader ModConfig API docs: https://docs.tmodloader.net/docs/stable/class_mod_config.html
10. tModLoader ModSystem API docs: https://docs.tmodloader.net/docs/stable/class_mod_system.html
11. tModLoader Basic JSON & ModConfigs wiki: https://github.com/tModLoader/tModLoader/wiki/Basic-JSON-&-ModConfigs
12. tModLoader Expert Cross-Mod Content wiki: https://github.com/tModLoader/tModLoader/wiki/Expert-Cross-Mod-Content
13. tModLoader Workshop wiki: https://github.com/tModLoader/tModLoader/wiki/Workshop
14. tModLoader Release Cycle wiki: https://github.com/tModLoader/tModLoader/wiki/tModLoader-Release-Cycle
15. tModLoader 1.4.5 update issue tracker: https://github.com/tModLoader/tModLoader/issues/5070
16. tModLoader Advanced UI guide: https://github.com/tModLoader/tModLoader/wiki/Advanced-guide-to-custom-UI
17. tModLoader World Generation wiki: https://github.com/tModLoader/tModLoader/wiki/World-Generation
18. tModLoader August 2024 Stable Update (Steam): https://steamcommunity.com/games/1281930/announcements/detail/4329732329530362391
19. PC Gamer — tModLoader 1.4.5 compatibility article: https://www.pcgamer.com/games/survival-crafting/terrarias-biggest-mod-manager-will-require-months-before-its-fully-compatible-with-the-1-4-5-patch-updating-tmodloader-to-major-terraria-releases-is-a-huge-undertaking/
20. GamesRadar — Redigit Calamity job offer: https://www.gamesradar.com/games/action/terraria-creator-has-a-simple-question-for-the-team-behind-one-of-the-games-best-mods-which-of-you-wants-to-work-for-re-logic-and-get-paid-for-your-work/
21. TechRaptor — Re-Logic hires Minecraft modder (jopojelly): https://techraptor.net/gaming/news/re-logic-hires-minecraft-modder-to-work-on-terraria-mod-tools
22. PCGamesN — Ex-Minecraft modder hired by Re-Logic: https://www.pcgamesn.com/terraria/minecraft-modder-hired-by-re-logic
23. Calamity Mod Patreon: https://www.patreon.com/CalamityMod
24. Fargo's Mods Patreon content wiki: https://fargosmods.wiki.gg/wiki/Patreon_content
25. kRPG GitHub: https://github.com/Kalciphoz/kRPG
26. Thorium Mod Calls wiki: https://thoriummod.wiki.gg/wiki/Mod_Calls
27. ModLoaderTools GitHub Actions: https://github.com/marketplace/actions/modloadertools
28. tModLoader Multiplayer debugging wiki: https://github.com/tModLoader/tModLoader/wiki/Debugging-Multiplayer-Usage-Issues
