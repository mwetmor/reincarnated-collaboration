# Reap. Die. Rise. — Build Architecture & Agent-Team Topology (Canonical)

**Project:** Reap. Die. Rise. (ARPG / roguelite, Godot 4.7, deterministic procedural-generation engine, multi-agent Claude dev team)
**Scope:** How the multi-agent Claude team builds the game in **one shared Godot project** that exports to **PC/Steam + iOS/Android**, fed by **JSON emitted from the serial content engine**.
**Status:** Feasibility confirmed (Godot 4.7 + 2026 Claude Code orchestration + JSON/Resource pipeline). This doc records the load-bearing decisions, the cleaned-up team topology, and the work-decomposition map. Where it conflicts with earlier ad-hoc build notes, this wins.

---

## 0. How to read this document

Sections 1–3 are **decisions** (don't relitigate). Section 4 is the **team topology** (the cleanup). Sections 5–7 are the **work map and seams** (the operational core). Sections 8–11 are **execution, performance, mapping, and risk**. The non-negotiable core for a new agent is **§1, §3, §4, §6**.

Tags: **[DECISION]** = settled. **[RECOMMENDATION]** = proposed cleanup, adopt unless overridden. **[OPEN]** = unresolved, tracked.

---

## 1. Architecture Decision Record (the load-bearing commitments)

- **[DECISION] One shared Godot project, not parallel codebases.** PC and mobile are **export presets off a single codebase**, never separately-developed builds. "Build PC and mobile in parallel" means *parallel export targets from one source*, with platform differences handled as thin adaptive layers — NOT parallel codebases (the anti-pattern: divergence + double merge surface + tightly-coupled work split across agents).
- **[DECISION] Mobile-first as the binding constraint.** Design and budget to the mobile floor (renderer tier, VFX density, draw calls); the PC build scales *up* from that baseline. Designing mobile-first and scaling up is far cheaper than the reverse.
- **[DECISION] JSON is the import boundary; typed Resources are the runtime form.** The serial content engine emits JSON; an import layer converts it to typed Godot `Resource` objects at build/load time. Game code consumes Resources, not raw JSON. (See §3.)
- **[DECISION] Solo PvE ships complete and cross-platform at launch. PvP/CTF is a post-launch reuse layer, PC-first.** (See §10, and gameplay-loop §23.6.) This is both a design de-risking decision and a technical necessity (Steam networking is PC-only).
- **[DECISION] Godot 4.7 is the pinned engine version.** Export templates are version-locked (4.7.0 templates do not work with 4.7.1, etc.); the editor, templates, and JDK must all match. Pin the exact patch version in the repo and upgrade deliberately via the migration guide.

---

## 2. Target & Platform Matrix

| Target | Renderer | Networking | Store plumbing | Notes |
|---|---|---|---|---|
| Windows / macOS / Linux (Steam) | Forward+ or Mobile (can scale up) | GodotSteam + SteamMultiplayerPeer (PvP, post-launch) | Steamworks | Steam overlay works in exported builds; Forward+ overlay-in-editor caveat is irrelevant to shipping. |
| iOS | Mobile / Compatibility | (no Steam; PvP deferred) | StoreKit 2 plugin (Foundation-maintained) | Xcode signing; export presets auto-flag unreliable-device configs (4.6+). |
| Android | Mobile / Compatibility | (no Steam; PvP deferred) | Google Play Billing + Play Games Services (Foundation-maintained) | JDK 17 + Android SDK; AAB for Play Store, APK for sideload/itch. **Never lose the release keystore — updates are impossible without it.** |

- **[DECISION] Renderer tier = Mobile/Compatibility as the floor.** Mobile GPU/driver variance is extreme (Android spans 12,000+ devices); the engine itself drove crash rates from ~4% to <1% via 4.6 mobile-hardening. Budget to that floor.
- **[DECISION] Steam networking is PC-only.** GodotSteam/SteamMultiplayerPeer cover Windows/Linux/Mac only. This walls PvP to PC unless/until a platform-neutral netcode path is added for mobile (deferred — see §10).

---

## 3. The Content Pipeline (serial engine → game)

**[DECISION] The JSON schema is the contract** between the serial content engine and the game. It is owned, versioned, and validated at the import boundary. Both teams (content-engine and build) treat it as the single source of truth for content shape.

**The import boundary (build/load time):**
- Content engine emits JSON packets (character/monster archetypes, gear, VFX slots, conduits, etc. — the StyleProfile/seasonal-coherence output).
- An **importer** parses JSON → instantiates **typed Custom Resources** (`MonsterData`, `GearData`, `ConduitData`, `EncounterData`, …, each `extends Resource` with `@export` fields).
- Game systems consume the **Resources** (type-safe, Inspector-visible, validated), never the raw JSON.

**[DECISION] Rules at the boundary:**
- **Cast numbers explicitly.** JSON has only floats, not ints — the importer must cast HP/damage/counts to int per the schema. Encode int-vs-float in the schema.
- **Validate on import, fail loud.** Schema-validate every packet; reject/flag malformed content at build time, not at runtime in front of a player.
- **Resources for authored content (we control it) — JSON for save data and anything networked (we don't).** A `.tres` can embed a script (a security hole if a player or remote source can edit it). So: authored/build-time content = Resources (fine); **save files and all networked/PvP payloads = plain JSON containing only values (ids, quantities, state).** This is a hard line, especially once PvP exists.

---

## 4. Agent-Team Topology (the cleanup)

### 4.1 What exists today (recorded, not redesigned)
- A **synthetic engineering team** for the build: an **Orchestrator** (tech-lead: plans, decomposes, reconciles), an **Analyst** (always-on QA/correctness watcher at the seams — catches divergence as it happens, not post-hoc), and **dev agents with mutually-exclusive folder/repo scopes** (so each can only break things inside its own scope; the Analyst watches the seams).
- A **separate, upstream content-engine team** (**Orchestrator / Designer / Judge**) that produces the JSON. This is NOT part of the build team.
- This foundation is sound. The cleanup adapts it to the cross-platform Godot build and fixes one scoping risk.

### 4.2 [RECOMMENDATION] The cleaned-up topology

**Principle 1 — Keep the two teams distinct, joined only by the JSON contract.** The content-engine team (Orchestrator/Designer/Judge) and the build team are separate org units. Their *only* interface is the versioned JSON schema (§3). Neither reaches into the other's repo. This is the cleanest seam in the whole system — protect it.

**Principle 2 — Scope dev agents by GAME SYSTEM, never by PLATFORM.** The biggest cleanup. Do **not** create a "PC agent / iOS agent / Android agent" split — that re-creates the parallel-codebases anti-pattern. Platform is **export configuration**, owned centrally, not a team axis. Dev agents own *systems* (which are platform-agnostic by construction, thanks to the abstraction layers in §5).

**Principle 3 — Cap at ~3–4 active dev agents.** Beyond that, the Orchestrator and Analyst become bottlenecks and parallelism stops paying. Fan out to the ceiling only when there's genuinely independent work; collapse to fewer when work is coupled.

**The roles:**

1. **Orchestrator (lead / integrator).** Holds the plan and the decision record; owns project conventions and the Resource class hierarchy; decomposes work; reconciles branches into one reviewable change set. **Owns the tightly-coupled core loop directly** (combat / possession / procgen / conduit economy) rather than splitting it — because it's a dependency chain where a single agent reasoning end-to-end beats a team (see §6).
2. **Analyst (always-on QA at the seams).** Keep this — it's the standout strength of the current setup. Continuous correctness watching across the seams between dev agents and at the JSON import boundary; catches procedural-generation divergence at emergence (where post-hoc diagnosis fails). In Godot terms, also owns the test harness (GUT/headless test runs) and the crash/perf watch against the mobile floor.
3. **Content-Pipeline dev agent.** Owns the JSON→Resource importer, schema validation, and the Resource class hierarchy. This is the build-side terminus of the content-engine seam. Mutually-exclusive scope: `/import`, `/data` (Resource definitions).
4. **Systems dev agent(s) (1–2, fan-out).** Owns the **parallelizable periphery**: individual enemy/champion kits, VFX slot implementations, UI screens, save/load, meta-progression, the hub. Mutually-exclusive folder scopes per agent. This is where you add a second worker when there's independent work, and where subagent fan-out lives.
5. **Platform/Release function (mostly automated, not a creative agent).** Owns export presets, headless CLI export, signing/keystore, and the build pipeline (§7). Implements the cross-platform abstraction layers (§5) **once**, to specs from the Orchestrator. This is config + CI, not a parallel development track.

**Principle 4 — Isolation via git worktrees; coordination via the right primitive.**
- Each dev agent works in its **own git worktree on its own branch** (mutually-exclusive scopes mean concurrent edits never collide; isolated test runs mean one agent's failing build can't corrupt another's).
- **Subagents** (report-back only) for independent periphery fan-out (e.g., "implement these 6 enemy kits in parallel").
- **Agent Teams** (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`; shared task list, peer messaging, **file locking**) when teammates must coordinate on adjacent code — file locking is the mitigation for the rare case where periphery work touches shared files.
- The Orchestrator reconciles; the Analyst watches. Humans approve anything reaching the main branch.

---

## 5. Cross-Platform Abstraction Layers (built once, by Platform/Release)

These three thin layers make "one codebase, two form factors" real. Gameplay code must be **platform-agnostic** — it never branches on platform; it talks to these layers.

1. **[DECISION] Input abstraction.** A logical-action layer: gameplay reads abstract actions (move, reap, possess, dash, interact) bound per-platform to mouse/keyboard (PC) or touch/virtual-stick (mobile). Decide the input model *early* (action-RPG with possession/reaping is touch-heavy). Use Godot's input-action map; lean on the 4.7 VirtualJoystick node and the "Emulate Touch from Mouse / Mouse from Touch" proxies during development. Gameplay code never knows which device it's on.
2. **[DECISION] UI / resolution / DPI scaling.** Anchor-based Control layouts (relative Anchor + Margin, never absolute pixels); set Stretch Mode/Aspect for the base resolution; rely on 4.5+ text/SVG DPI scaling. One UI that adapts to phone and desktop aspect ratios.
3. **[DECISION] Graphics / performance tier.** A quality tier driven by platform: mobile floor (no/limited heavy VFX, capped GPUParticles3D, Mobile/Compatibility renderer) → PC scales up. The VFX slot model (cast→travel→impact→residual) must have a mobile-budget tier per slot. (See §8.)

---

## 6. The Work-Decomposition Map (what parallelizes vs. what doesn't)

**The governing rule:** multi-agent parallelism wins on **genuinely independent** work and *loses* on tightly-coupled chains (coordination overhead + merge conflicts outweigh speed; a single agent reasoning end-to-end is cheaper and more reliable). A game's core systems interlock; its periphery does not. **Parallelize the periphery; single-thread the core.**

**Single-thread (Orchestrator owns directly — coupled dependency chain):**
- The core loop: combat ↔ possession/reincarnation ↔ procgen (graph-grammar/prefab/WFC) ↔ conduit economy ↔ the three-beat descent + escape. These touch each other constantly; splitting them across agents thrashes.

**Parallelize (Systems agents / subagent fan-out — independent slices):**
- The JSON→Resource import pipeline (Content-Pipeline agent).
- Individual enemy/champion **kits** (each self-contained — ideal fan-out).
- Individual **VFX slot** implementations.
- **UI screens** (hub, inventory/grimoire, vendor, run-summary).
- **Save/load** (JSON), meta-progression, cult-standing economy.
- The **platform-adaptation layers** (§5) — built once, independently of gameplay.
- Cosmetic/data-driven content that flows from the engine.

**Decomposition heuristic for the Orchestrator:** if a task needs the output of another in-flight task, keep it single-threaded; if it has explicit, non-overlapping file boundaries and clear success criteria, fan it out. Route high-volume, well-scoped slices (e.g., N enemy kits) to cheaper models; reserve frontier reasoning for the coupled core and the integration.

---

## 7. Build & CI Pipeline (as-built reference)

*The team has run a build/CI split for months; this records the mechanics so the doc is self-contained. Not a redesign.*
- **Headless export per target:** `godot --headless --export-release "<PresetName>" <output>` — one automated pipeline produces all platform artifacts. Preset names must exactly match Project → Export; matching export templates (+ JDK 17 + Android SDK for Android) must be installed on the build machine.
- **Templates pinned to the exact Godot patch version** (§1).
- **Signing:** Android keystore (guard like a password — loss = no future updates); iOS via Xcode signing.
- **Outputs:** AAB (Play Store) / APK (sideload, itch) for Android; Xcode build for iOS; Steam depot for PC.

---

## 8. Performance Budget (mobile floor as the design constraint)

- **[DECISION] Target sub-1% crash rate on mobile** (the bar the engine's own mobile-hardening hit). Native debug symbols (Android) + crash monitoring via Play Console.
- **Renderer:** Mobile/Compatibility floor; Forward+ only as a PC scale-up.
- **VFX density:** the composable VFX slot model needs a per-slot mobile tier; cap GPUParticles3D counts; reuse the harvested-flipbook/texture-driven approach (cheap) over heavy simulation on mobile.
- **Draw calls / instancing:** GPU instancing (HISM-equivalent / MultiMesh) for the militant-sameness soldier mass; this is also a content/art constraint, not just code.
- This section is the runtime companion to the existing performance-target-specs doc — keep them aligned.

---

## 9. Mapping to the §23 Run Model

How the architecture serves the actual game (gameplay-loop §23):
- **Procgen generators** (graph-grammar = macro beats; prefab meta-tiles = architectural structures; WFC = biome fields) are code modules the Orchestrator owns (coupled core).
- **The three-beat descent + escape** = scene structure assembled by the generators at runtime from Resource-defined content pools.
- **The conduit economy** (harvest, hand-in-vs-keep, cult-standing tax) = Resource-driven systems + JSON save state.
- **Engine-generated content** (kits, gear, conduits, VFX) flows in via the JSON→Resource boundary (§3) and is consumed by the parallelizable periphery (§6).

---

## 10. Post-Launch / PvP Addendum (walled off; PC-first)

- **PvP = bounded 8v8 CTF**, NPC giants as the victory engine (gameplay-loop §23.6). **Post-launch reuse layer, not a launch dependency.**
- **PC-first by technical necessity:** GodotSteam/SteamMultiplayerPeer (RPC + MultiplayerSynchronizer + MultiplayerSpawner over Steam sockets, Steam lobbies for matchmaking) are **PC-only**. Mobile PvP, if ever pursued, needs a platform-neutral netcode path (dedicated server / relay) decided later.
- **Reuses existing systems** (possession, the commander-domination loop, the conduit) — additive, cheap-by-reuse, deferrable. The conduit's dormant combat dimension (PvE-normal / giant-exceptional) activates here as a *balance* feature.
- **All networked payloads = JSON, never Resources** (§3 security line).
- **Deferred PvP-balance questions** (decide with real player data): conduit permanent-vs-consumable; giant possession gate-vs-edge.

---

## 11. Risk Register & Open Questions

- **[RISK] Whole-game multi-agent coupling.** The "refactor 40 independent files" success stories are *more* parallel than a game's interlocking systems. Expect strong parallelism gains on the periphery (§6) and *little* on the coupled core — plan decomposition around that seam; resist over-fanning the core.
- **[RISK] Integration thrash.** Parallel work on a single game's systems can conflict at shared files. Mitigations: mutually-exclusive folder scopes, git worktrees, Agent-Team file locking, the always-on Analyst at the seams, and a strict reconciling Orchestrator.
- **[RISK] Mobile GPU/driver variance.** 12,000+ Android devices; budget to the floor, monitor crash rates, use instrumented tests (Firebase Test Lab) where possible.
- **[FRAGILE] Fast-moving externals.** Godot version (now 4.7), plugin compatibility (GodotSteam ↔ Steamworks SDK breaks occasionally), and Foundation-maintained store plugins all move. Pin versions; re-verify before upgrades.
- **[OPEN]** Whether the existing content-engine team's `Designer`/`Judge` should emit Godot-native Resources directly (via MCP into Godot) vs. continue emitting JSON consumed at the import boundary. Current decision: **JSON boundary** (clean seam, validatable, decouples the teams). Revisit only if the boundary becomes a bottleneck.
- **[OPEN]** Cheap-model routing thresholds for periphery fan-out — tune in practice.

---

## 12. The one-paragraph summary

Build **one Godot 4.7 project, mobile-first**, exporting to PC/Steam + iOS/Android via separate presets. The serial content engine feeds it through a **JSON→typed-Resource import boundary** (the clean seam between the two teams). The build team keeps its proven shape — **Orchestrator (lead/integrator) + always-on Analyst (QA at the seams) + dev agents in mutually-exclusive worktree scopes** — but **scoped by game system, never by platform**, capped at ~3–4 active agents. The Orchestrator **single-threads the coupled core** (combat/possession/procgen/conduit) and **fans out the independent periphery** (kits, VFX, UI, save, the platform layers). Platform is export config, owned by a mostly-automated release function. **Solo PvE ships cross-platform at launch; PvP/CTF is a PC-first, post-launch reuse layer** — a call that's right for both design and the PC-only Steam networking reality.
