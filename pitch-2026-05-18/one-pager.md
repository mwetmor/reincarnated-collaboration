# Reincarnated — Engine + Game

*Two distinct but combinable products.*

**Matt Wetmore** · mhwetmore@gmail.com · 2026-05-18

---

## The Engine

**Procedural content engine that generates and simulation-balances a full ARPG season in 41 minutes for under $1.**

Live-service ARPGs need weekly content to retain players. Content production is the genre's biggest cost — most studios run 8-12 week cycles with 30-50 person seasonal teams. The Reincarnated Engine replaces that cycle with a 1-day generation + 1-week polish loop.

**What's load-bearing:** content isn't just procedurally generated — it's *simulation-balanced* against canonical combat encounters before shipping. The simulation layer is the innovation. Existing procgen produces content that needs hand-balancing; this produces content that's already balanced.

**Evidence today:**
- Yomi season: 10 classes generated, 100% validation pass, **$0.98 cost, 41.6 min wall time**
- 1.5M+ simulated fights captured in telemetry
- 12 engineering disciplines codified, 30+ design decisions logged
- Findings the engine surfaced unsolicited: hunter archetype shows 1.82× modifier range (template consistency issue); fire over-represented at 23.6%; 85% mana homogeneity; AOE-vs-pack 8× multiplier emerging genre-correctly

**Path to commercial:** B2B middleware for live-service studios. Replace 8-week content cycles with 1-day generation. Recurring license + per-call billing.

---

## The Game

**"This Week I Was Reincarnated As…" — an isekai mobile ARPG with weekly reincarnation seasons and a persistent player-identity meta-game.**

Every week the player is reincarnated as a new class. Their seasonal progression is mortal — it ends with the season. But their **Earth Self** — the persistent player identity — accumulates *ascended spirits* (classes embodied) into a permanent gacha-style collection.

**Player problems solved:**
- "My build is obsolete after every patch" — builds are weekly; investment in the collection is permanent
- "Content drought between seasons" — weekly fresh class + season = constant novelty
- "Endgame grind fatigue" — the loop itself rotates; what's permanent is the collection

**Genre fit:** Isekai has been mainstream in anime/manga/light-novels for a decade (Slime Tensei, Reincarnated as a Sword, Re:Zero, …). Underrepresented in Western games. No native-game isekai with this design.

**Evidence today:**
- Demo1 (Pixi.js) — playable seasonal demonstration shipped 2026-05-08
- Loadout web app live at `https://reincarnated-loadout.vercel.app` (4 modes: build planner, engine baseline view, cross-season analytics, encounter visualizer)
- Yomi as worked example: 10 named classes, full kits, trial boss, balance-validated

**Path to commercial:** Mobile B2C live-service ARPG. Mobile-first, isekai-native game design.

---

## Combinable

The engine produces structured data; the game consumes it. Clean interface. Either can stand alone.

| Path | Description |
|---|---|
| **Engine-only (B2B)** | License engine to other studios. Game becomes demo, not revenue product. |
| **Game-only (B2C)** | Build out the game as standalone. Engine becomes proprietary infrastructure. |
| **Vertical integration** | Ship the game as flagship demo of the engine; license engine to non-competing genres. |

**Engine is closer to shippable than the game.** Engine-first commercialization is the safer initial bet — generates revenue sooner, de-risks the game.

---

## Trajectory

**Phase 0 (current, ~mostly complete):** Engine validates generation pipeline. Game has demo1 + loadout web app.

**Phase 1 (next, 6-12 months solo / faster with team):** Engine production hardening. Game demo2 with playable session + rooms + AOE gauntlet + non-humanoid character support. Earth Self meta-layer prototype.

**Phase 2 (medium):** Engine multi-tenant SaaS prototype + first licensing conversation. Game closed beta with Earth Self mechanics. Multi-genre extension experiments.

**Phase 3 (long):** Engine as shipped commercial middleware. Game production launch (mobile, live-service). Multiplayer rift events + social meta-layer live.

---

## What this isn't yet

- **Not production-ready** — Phase 0 prototype scope.
- **Not player-validated** — engine balance validated; player-side appeal unproven.
- **Not multiplayer** — solo combat by design; multiplayer lives in Phase 3 meta-layer.
- **Not capital-light at scale** — engine SaaS or game production launch needs team.

---

## What I'm curious about

This pitch is structured to invite feedback on three axes:

1. **Engine marketability** — does the procgen-with-simulation-balance bet read as real?
2. **Game marketability** — does isekai-native + weekly-reincarnation + Earth-Self read as a market fit?
3. **Sequencing** — engine-first or game-first or both? Where's the highest-leverage early move?

I'm not pitching for advancement, hire, or investment today. I'm pitching for honest industry read.

**Explore the live artifact:** `https://reincarnated-loadout.vercel.app`
