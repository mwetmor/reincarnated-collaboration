> **SUPERSEDED-BY-CANON (2026-07-10):** canonized verbatim + annex at
> `canonical/reap-die-rise-game/business-platform-strategy.md` — read/edit THERE. This handoff
> original is retained as mobile-session lineage only.

# Reap. Die. Rise. — Business Model & Platform Strategy

**Audience:** Hale + the build team. Strategy companion to `reap-die-rise-minigame-template-taxonomy.md` and the pipeline docs. This is positioning and sequencing, not engineering spec.
**One-line verdict:** platform play, no; product with a uniquely cheap content engine, yes (power-law odds stated honestly); pipeline expertise as the professional floor; nostalgic-cohort niche, not "the masses."

---

## 1. The Three Businesses (verdict table)

| Business | Verdict | Evidence / reasoning |
|---|---|---|
| **UGC platform** ("Roblox for RPG minigames") | **NO — do not build toward it** | Valve's Dota 2 Arcade languished with a giant installed base; SC2 Arcade = 5% primary interest by Blizzard's own poll; Reforged cratered on nostalgia; prompt-to-game platforms are a funded-startup knife fight (Verse8 et al); Roblox/Fortnite own the mass UGC network. Distribution, not tooling, was always the moat — a solo dev cannot win a network war giants lost. |
| **Product** (RDR + machine-run arcade) | **YES** | Best-fit commercial indie niche (ARPG/roguelite/horde). Structural edge: a certified content season costs tokens + curation, not months of labor — one of very few solo devs who can honestly sustain live cadence. Cadence = retention = the modern indie business. Odds are power-law; genre/hook/streamability move the percentile, nothing removes the distribution. |
| **Pipeline expertise** (the hedge) | **The floor** | Sim-certified content generation is rare and demonstrable. Devlogging the factory builds wishlists AND professional optionality (talks, consulting, licensing, VP-track leverage). Median game outcome still leaves market-valued expertise. |

## 2. Positioning

The market is not the masses. It is the **ex-Battle.net custom-games cohort, now ~35–45**: time-poor, employed, underserved (Roblox is their kids' scene). Pitch: *the custom-game lobby, resurrected — the mapmaker is a machine, every mode is certified balanced, and bots mean it works at 11pm with no friends online.* Niche-first is the winning solo position, not the compromise.

## 3. Monetization Ladder

1. **Paid base game** (Steam premium).
2. **FREE seasonal kit tranches** — the retention engine. They are nearly free to produce; that is the structural edge. Never paywall your own advantage.
3. **Cosmetics / supporter DLC** — only after an audience exists. (Law 4 membrane already keeps these power-free.)

**Never:**
- **Content hidden behind prompt discovery.** Retention runs on *visible* novelty: seasons land as new kits in the world, new reap targets, new arcade rotation, patch notes, trailer beats.
- **Paid asset packs for creators.** Three stacked reasons: (a) economically, creators are a second content factory, not a customer segment — maximize their inputs, don't tax them; (b) structurally, ownership-fragmented assets shatter the shared vocabulary that makes modes instantly learnable; (c) legally, asset-store licenses (Synty included) permit shipped-game use, not asset redistribution.

**LAW — Content visibility:** *The agent is a fast hand over a browsable catalog, never the only door.* Prompts arrange content into modes; they never unlock content. Kits are nouns, modes are sentences; every noun is visible in the catalog. Each season feeds both surfaces from one emission: new kits for players, new vocabulary for creators, announced together.

## 4. The 60-Second Demo ("describe a mode, play it with bots")

**Feasible — because a mode is a packet, not code.** Templates are pre-implemented; kits pre-certified; bots free via the shared player/AI pool.

- Runtime path: constrained LLM parse → packet (~5–10s) → schema validation (instant) → runtime load (~5–15s). **15–30s in-lattice; 60s has margin.**
- **Range certification (the required move):** the sim pre-validates each template's *parameter space* offline ("wave scaling X–Y in-band for composition class Z"). Runtime packets **clamped to certified ranges are certified by construction** — instant AND Law-6-compliant. Same architecture as gear fairness bands, one level up.
- **Lattice edge, graceful:** parameter fills succeed in seconds; new primitives are engine work — the tool must say "not in the vocabulary yet; closest I can do is X."
- Why it's a moat: shallow at runtime *because* deep at build time. The demo is uncopyable without the substrate — a marketing beat, not a feature war.

## 5. The Creator Editor — the World Editor path, not the Roblox path

**Game-first.** WC3's editor was a feature in a shipped RTS riding the game's distribution; Roblox is platform-first. The open lane: RDR ships as a game, the arcade is a mode, the **editor is the creator endgame** — for the cohort who were 2003 mapmakers, i.e., the target audience anyway.

Editor = packet authoring over the lattice (no code exposed):
- Template picker → kit slicer → parameter forms → one twist
- **Agent copilot** in the sidebar ("gentler early waves, brutal bosses" → parameter patch) — dissolves the JASS learning curve
- **Preview-with-bots** button — the 60-second demo *is* the playtest loop
- **Submit-to-certification** — async sim pass, minutes

Two properties that make it new, not nostalgic:
1. **Certification as a platform property** — the first UGC surface where every published mode is certified balanced before anyone plays it (the WC3 zoo was beloved AND broken).
2. **The registry flywheel** — community modes are packets in *our* registry, in *our* game; the best curate into the official seasonal rotation. The DotA lesson from the platform owner's side: **own the registry.** Blizzard shipped the editor and captured none of DotA's value; this architecture captures it by construction.

Boundaries: creators **compose** primitives; authoring new primitives stays internal (GUI triggers vs. JASS, reborn). Assets travel as **registry references, never raw files** — the game client owns assets; licensing dissolves permanently.

## 6. Build-As-You-Go Tooling (answer to Q1: yes)

You already are — the Mac team + packet schemas *is* the editor wearing a conversational UI. Formalize in thin layers over the packet contract, each pulled forward only when the manual version hurts:

packet-validation CLI → crude local form per template → preview-with-bots button → cert-submit command

**RULE OF THREE:** no tool until the manual version has been done painfully three times. **Zero creator-grade polish** (undo stacks, pretty panels, onboarding docs) before the Stage-4 demand signal. Every layer must pay for itself inside the current milestone; by launch, the creator editor is battle-tested internal workflow plus onboarding, not speculative software.

## 7. Mod Tools (answer to Q2: tiered)

| Tier | What | Verdict |
|---|---|---|
| **1 — Mode/packet creation** | the editor above | Build for self continuously; expose at Stage 4 |
| **2 — Content modding** (community kits, custom assets) | interesting *because the sim could certify community kits like anything else*; but art breaks style cohesion + licensing | **Stage 5 question**, not now |
| **3 — Code-level modding** (the JASS tier) | arbitrary scripts break certification by definition; moderating executable UGC is Roblox-scale cost | **Never promise.** Primitives stay authored — standing architecture law |

**Mod-enablement-by-architecture NOW (free):** versioned + documented packet contract; registry-ID indirection everywhere; certification callable as a service; no hardcoding. Preserves every future option at zero present cost. Precedent: Rimworld and Factorio matured mod ecosystems *after* earning audiences; the World Editor shipped inside a finished RTS.

## 8. The One Principle

**Build platform capabilities as internal capabilities; expose them as products only on demand signals.** The packet contract IS the platform. Editor UI, mod SDK, and the prompt front-end are skins over it. Every skin waits for either your own pain or players asking. The ship date stays sacred.

## 9. Decision Gates

| Stage | Surface | Gate to advance |
|---|---|---|
| 1–3 | In-game activities → arcade surface (taxonomy rungs 1–3) | as already defined in the taxonomy doc |
| **4** | **Creator editor exposed** | arcade retention healthy AND players *asking* to make modes |
| **4.5** | **Prompt front-end exposed** (the 60s demo, public) | editor proven internally; used as a marketing beat |
| **5** | Tier-2 content modding | active creator scene AND mature style-certification pipeline |

**Devlog/wishlist plan:** devlog the factory itself (the pipeline is the story nobody else can tell) → wishlists + the expertise hedge in one motion.

**Risks on file:** AI-content reception on Steam (disclosure checkbox per ensemble doc §12; mitigation narrative is true and strong: build-time generation, human-directed, sim-certified, stylized); crowded survivor-like field (differentiation = reap-anything + kit depth — protect it); **scope remains the existential risk** — this document exists to protect the ship date, not to grow the project.
