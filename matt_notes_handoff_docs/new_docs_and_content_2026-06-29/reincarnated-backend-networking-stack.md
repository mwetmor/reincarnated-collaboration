# Reap. Die. Rise. — Backend, Networking & Server Stack (Technical Reference)

**Project:** Reap. Die. Rise. (ARPG)
**Document:** Backend architecture for PVE and PVP — server topology, netcode, data persistence, hosting/cost models, and the decision structure
**Status:** Technical reference — companion to the gameplay-loop design doc and the performance/target-specs doc
**Audience:** Claude implementation team
**Engine:** Godot 4.x · **Platform:** Steam (Windows primary)

> **Sourcing caveat:** backend tooling, hosting prices, and Godot's netcode maturity change fast. Figures here reflect 2025–2026 sources and are *order-of-magnitude* planning numbers, **not** quotes. Re-run vendor pricing calculators before committing budget, and re-check Godot's multiplayer feature set against the current stable version. This is the area of the project most sensitive to staleness — verify before spending.

---

## 0. The principle: the real fork is "single-player/local" vs. "server-authoritative online" — NOT "PVE vs PVP"

What drives backend cost and complexity is not the PVE/PVP label. It is two questions:

1. **Is it online-multiplayer at all?**
2. **Does a server need to be *authoritative* (arbitrate truth to prevent cheating and resolve conflicts)?**

Those determine the stack. For Reap. Die. Rise., the modes sort cleanly:

- **PVE (the core descent loop): single-player → essentially NO game servers.** Backend reduces to *managed services* (auth, save sync, content delivery), which is cheap, boring, and low-risk.
- **PVP (the proposed CTF/battleground): online + authoritative → a full dedicated-server stack**, which is a permanent engineering *and* operational *and* cost commitment, and is the single largest hidden scope item in the project.

The gap between these two is enormous. Treat them as separate programs.

---

## 1. PVE backend — clientless gameplay, managed services only

**The core realization: if PVE is single-player (which the entire design implies — your spirit, your descent, your grimoire), the game runs entirely on the player's machine. There are NO game servers for PVE gameplay.** Combat, generation, loot, the sawtooth — all local. This is the cheap, safe path, and it should stay that way.

What PVE *does* need is **backend services** (a different, far cheaper thing than game servers):

**1.1 Save data / progression / the grimoire.**
The permanent grimoire (became-it pages), collection, and progression need to persist. Two viable approaches:
- **Steam Cloud (recommended default).** Free, built into Steam, designed exactly for single-player save persistence and cross-device sync. Many shipped single-player ARPGs use only this. For a single-player game, **this is very likely sufficient and is the lowest-risk, lowest-cost option.** Start here.
- **A managed database / BaaS** (only if you need server-side validation of progression, cross-platform identity beyond Steam, or online leaderboards tied to progression). Adds cost and complexity; only adopt if Steam Cloud's limits bite.

**1.2 Account / identity.**
If the game is Steam-only and single-player, **Steam identity is enough** (the player is their Steam account). No separate auth system needed. A separate auth layer is only required if you go cross-platform (Steam + Epic + console) and need unified identity.

**1.3 Seasonal content delivery (the JSON kit-packs).**
New kits/seasons ship as **data packets** — this is *patching / file distribution*, which **Steam handles natively** (depot updates). No custom infrastructure. If you ever want to push content *without* a client patch (live content drops), a lightweight remote-config / CDN service (or a BaaS "live config" feature) covers it, but it is optional.

**1.4 Leaderboards / telemetry (optional).**
- Leaderboards: **Steam provides these free.** Sufficient for most needs.
- Telemetry (balance data, player behavior — useful for tuning the §experimental pipeline): a modest analytics pipeline or a BaaS analytics feature. Optional, additive, low-cost at indie scale.

**PVE backend cost summary: at indie scale, plausibly $0–low-tens/month** (Steam Cloud + Steam leaderboards + Steam patching = $0 beyond the Steamworks fee; a small DB/analytics layer adds little). **PVE has no scaling-cost cliff** because there are no game servers — player count drives Steam's infrastructure, not yours.

**PVE backend = managed services, not servers. Default to Steam-native (Cloud + leaderboards + depot patching), add a BaaS only if a specific need forces it.**

---

## 2. PVP backend — the authoritative-server stack (a second program)

This is where the cost, complexity, and risk live. PVP that lets players affect each other's outcomes **must be server-authoritative** (the alternative — trusting clients — is an open invitation to cheating, fatal for a game whose stakes are "keep what you kill"). Authoritative multiplayer in Godot is a **three-layer architecture**:

1. **Game Client** — the player's Godot executable: rendering, input, interpolating server state.
2. **Dedicated Server (headless Godot)** — a Godot build exported headless (`dedicated_server` feature, run with `--headless`), running on a Linux VM/container in the cloud, running the *authoritative* simulation and validating inputs. **This is the piece that costs compute and must be operated.**
3. **Platform Backend (API + database)** — an external web service for accounts, matchmaking, lobbies, persistence, leaderboards (PlayFab / Nakama / similar). The dedicated server talks to this over HTTP; **the client must never talk directly to the database.**

### 2.1 Godot's netcode reality — capable, but you build more yourself, and there are hard limits

Godot 4's high-level multiplayer API (ENet/UDP transport, `MultiplayerSpawner`, `MultiplayerSynchronizer`, `@rpc`) is **real and shippable** — there is now a production case study (Dome Keeper, a Godot game with multi-million Steam revenue, shipped online co-op and competitive modes). But the honest constraints, which matter enormously for *this* game:

- **No built-in client-side prediction or rollback.** Input goes to the server, the server processes, the result comes back — you *build* prediction/reconciliation yourself, or players feel input latency. For a fast ARPG, prediction is effectively mandatory, which is **significant netcode engineering**.
- **No built-in matchmaking, lobbies, or friend lists.** All of that is your problem (or a platform SDK's — see GodotSteam below).
- **No NAT traversal.** ENet over UDP is blocked by most home routers; you need a relay (Steam Networking, or a relay server). Godot ships neither — **GodotSteam** (wrapping Steamworks) provides Steam Networking Sockets (relay + NAT traversal) plus lobbies/matchmaking/friends, and is the standard way Godot games on Steam solve this.
- **No built-in anti-cheat.** Authoritative architecture stops the *worst* cheats (teleport, infinite health), but not all; mitigation is server-side validation you write, possibly plus third-party anti-cheat.
- **Weaker debugging tools** than Unreal's network profiler — expect heavy reliance on logging and controlled latency testing.
- **Unreal comparison (relevant because it quantifies the gap):** Unreal ships property replication, built-in movement prediction, network relevancy, and the Online Subsystem — *weeks of networking work you'd do manually in Godot.* Godot's netcode is **simpler and more explicit (you understand it) but you write all of it** (prediction, reconciliation, interest management, bandwidth optimization). For a solo dev, this is a *large* time cost.

### 2.2 The hard scalability ceiling — ~40 concurrent players per server instance

**This is a critical, possibly decisive constraint, and it shapes the entire PVP design.** Documented Godot benchmarks show **connection-stability issues above roughly 40 concurrent users per server instance** (one set of tests; another framework exceeded 100 CCU, so it is implementation-dependent — but ~40 is the conservative planning number for Godot's high-level API). Practical reading:

- **Small-session PVP (your CTF/battleground for, say, 5v5–8v8 = 10–16 players) is comfortably within Godot's wheelhouse.** This is the *good* news: your bounded-battleground design (a contained match, modest player count) is *exactly* the shape Godot handles well. **Do not design PVP modes that need more than a few dozen players in one instance.**
- A "shipping on Steam, small sessions (2–8, up to a few dozen), can live without rollback" profile is explicitly where Godot multiplayer *fits*. Co-op and small competitive modes are the sweet spot.
- Modes needing >40 in one instance, or twitch-competitive rollback netcode, are where Godot strains — **avoid that scope.**

**Design consequence:** the bounded-battleground PVP (§design doc) must be *capped at a few dozen players per match*, which it naturally is. This is a *fit*, not a fight — but it forecloses any "massive battle" PVP ambition.

### 2.3 Platform backend (accounts, matchmaking, persistence) — buy, don't build

You do **not** hand-roll accounts/matchmaking/persistence. Options fall into categories:

- **Managed backend suites (PlayFab, etc.):** all-in-one (auth, matchmaking, lobbies, leaderboards, economy, dedicated-server orchestration), **usage-based pricing**, free entry tiers. Lowest ops burden; you trade money + vendor dependence for not running infrastructure. **Best fit if your strength is game dev, not DevOps** (i.e., the solo-dev default).
- **Self-hostable server frameworks (Nakama, open-source):** free software, **but high *indirect* cost** — you run, monitor, scale, secure, and back up it yourself. Powerful and sovereign; **only worth it if you have real DevOps capacity** (a solo dev at launch generally does not). Managed Nakama (Heroic Cloud) removes the ops burden for a fee.
- **Lightweight/flat-fee BaaS (various indie-targeted options):** predictable flat monthly pricing, free starter tiers (e.g. free up to a few thousand MAU), REST-first so any engine integrates. Attractive for *predictable* cost vs. usage-based surprises.
- **GodotSteam (the Steam-native shortcut):** for a Steam-first game, GodotSteam's lobbies + Steam Networking can handle matchmaking, relay/NAT, and friends **without a separate backend service at all** for the *networking/lobby* layer — a major simplification. Persistence still needs Steam Cloud or a DB. **For a solo Steam launch, GodotSteam is likely the lowest-friction matchmaking/relay path.**

### 2.4 Dedicated-server hosting — the recurring cost, and why it never sleeps

The headless-Godot dedicated servers are the part that **costs money continuously and must be operated forever.** The model and its cost structure:

- **Session-based, autoscaling hosting** (e.g. Amazon GameLift and similar orchestrators): you pay for **server compute by duration of use**, scaling instances up/down with player demand. Spot instances cut 50–85% for short (<30-min) sessions — *which your bounded matches are*, a genuine fit.
- **Order-of-magnitude cost:** large-scale modeled examples land near **~$0.80–$1.00 per peak-concurrent-player per month** for a session-based multiplayer game on managed hosting (this figure is remarkably stable across 10k / 100k / 1M CCU in AWS's own modeling). At indie PVP scale (hundreds to low-thousands of peak CCU), that implies **roughly hundreds to low-thousands of dollars/month** while players are active — *and it scales with players, so a hit costs more to run.* (Re-run the calculator; on-demand rates shift.)
- **Free tiers exist** (e.g. thousands of game sessions + hundreds of thousands of server-minutes/month for the first year), which covers *early/small* PVP populations — useful for launch, not for sustained scale.
- **The operational reality:** dedicated servers require fleet orchestration, monitoring, patching, regional deployment (latency!), and **live balance/anti-cheat tuning that is never "done."** PVP is a *permanent live-ops commitment*, not a ship-and-forget feature. This is a *team* responsibility, not a solo-at-launch one.

### 2.5 PVP cost/effort summary

- **Engineering:** authoritative netcode + client-side prediction + interest management + anti-cheat validation + matchmaking integration — **weeks-to-months of specialized work** Godot does *not* give you for free (unlike Unreal). For a solo dev, this is a major diversion from game-building.
- **Hosting:** **recurring, player-scaling** dedicated-server compute (~$1/peak-CCU/month order of magnitude), plus backend-service fees — **a perpetual operating cost that grows with success.**
- **Operations:** permanent live-ops (balance, anti-cheat, server fleet, regional latency) — **a team commitment.**
- **Ceiling:** ~40 players/instance (Godot) — fine for bounded battlegrounds, fatal for "massive battle" ambitions.

---

## 3. Side-by-side

| Dimension | PVE (single-player) | PVP (authoritative online) |
|---|---|---|
| Game servers | **None** (runs on player's machine) | **Required** (headless Godot, cloud-hosted) |
| Authoritative logic | N/A (local) | **Mandatory** (anti-cheat) |
| Netcode work | None | **Large** (prediction/reconciliation hand-built in Godot) |
| Matchmaking | None | Required (GodotSteam or BaaS) |
| Persistence | **Steam Cloud** (default) | DB/BaaS (server-validated) |
| Content delivery | **Steam depot patching** | Same |
| Monthly cost @ indie scale | **~$0–low-tens** | **~hundreds–low-thousands, player-scaling** |
| Cost behavior with success | Flat (Steam's problem) | **Rises with players** |
| Operational burden | Minimal | **Permanent live-ops (team)** |
| Player ceiling | N/A | **~40/instance (Godot)** |
| Risk to solo launch | Low | **High (largest scope item in the project)** |

---

## 4. Recommendations & decision structure

**4.1 PVE: build now, keep it server-light.**
Single-player, local gameplay; **Steam Cloud for saves, Steam for identity/leaderboards, Steam depot patching for seasonal content.** Add a BaaS/DB only if a concrete need (cross-platform identity, server-validated progression, online leaderboards beyond Steam's) forces it. This is cheap, low-risk, and has no scaling cliff. **No game-server infrastructure for PVE, period.**

**4.2 PVP: do NOT build at launch. Architect the door; ship through it later, if at all.**
The research makes the case clearly:
- PVP is a **second program** — large netcode engineering Godot doesn't give you free, perpetual player-scaling hosting cost, permanent live-ops, and a ~40-player ceiling.
- It collides head-on with the project's two anchors: **solo-dev capacity** and **deliberate commercial-risk reduction**. Adding the genre's most resource-hungry, never-finished, cost-scaling system is the **single most likely thing to sink a solo launch.**
- **Therefore: ship PVE. Treat PVP as post-launch, team-gated, opt-in, and bounded** — exactly the "build cheap, architect expensive" discipline applied to the riskiest feature.

**4.3 What "architect the door" means concretely (do this during PVE build, cheaply):**
- Keep **combat resolution clean and deterministic-friendly** (a combat layer that *could* run server-authoritatively later — server-validatable state, no logic that assumes a trusting client). This is good PVE architecture anyway.
- Separate **simulation from presentation** (so a headless server build is feasible without untangling rendering from game logic).
- Keep **game state serializable** (needed for both save-sync and, later, network replication).
- Do **not** build netcode, matchmaking, or servers now. Just don't *foreclose* them.

**4.4 If/when PVP is built (post-launch, with a team):**
- **Scope it small:** bounded battlegrounds, ≤ a few dozen players/match (within Godot's ~40 ceiling), short sessions (Spot-instance-friendly).
- **Use GodotSteam** for lobbies/matchmaking/relay/NAT (Steam-native, lowest friction) — avoid hand-rolling matchmaking.
- **Use a managed backend** (PlayFab-tier or managed Nakama) for persistence/orchestration rather than self-hosting, unless a DevOps hire exists.
- **Use session-based autoscaling hosting with Spot instances** for the dedicated servers (matches the short-bounded-match profile; 50–85% cheaper).
- **Budget perpetual cost and perpetual live-ops** — PVP is a standing commitment, not a feature you finish.
- **Keep "keep what you kill" aimed at objectives (generals), not players** (per design doc) — this *also* reduces backend stakes (less need to server-arbitrate permanent player-identity loss) and toxicity simultaneously.

---

## 5. Decisions to lock

1. **PVE ships server-light:** Steam Cloud + Steam identity/leaderboards + Steam depot patching; BaaS only if forced. (§1, §4.1)
2. **PVE has no game servers.** Gameplay is local. (§0, §1)
3. **PVP is post-launch, team-gated, opt-in, bounded — NOT a launch feature.** (§2, §4.2)
4. **Architect the combat/state layer to *permit* future authoritative PVP** (deterministic-friendly, sim/presentation split, serializable state) **without building netcode now.** (§4.3)
5. **Any future PVP stays ≤ a few dozen players/match** (Godot's ~40-CCU/instance reality) and uses **GodotSteam + managed backend + Spot-instance session hosting.** (§2.2, §4.4)
6. **Re-verify all netcode capabilities and all hosting/BaaS pricing against current sources before any PVP commitment** — this domain moves fast and these figures are planning-grade, not quotes. (sourcing caveat)

---

*End of backend/networking reference. The headline: PVE is cheap and server-light (Steam-native); PVP is a separate, perpetual, player-scaling, live-ops-heavy program with a ~40-player Godot ceiling — architect for it, but ship PVE first and add PVP only post-launch with a team, scoped small and opt-in.*
