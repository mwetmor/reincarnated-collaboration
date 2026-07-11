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

---

## 10. THE STEAM CONSTELLATION PLAN

**The structural insight:** Steam's power law punishes single-ticket launches; the engine makes tickets cheap. A satellite = packets + the arcade runtime, and each Steam app carries its own tags, its own New & Trending shot, its own review pool, and — decisively — **its own Next Fest token** (one fest per title, ever; three fests/year: Feb/June/Oct). App fees are trivial ($100, recoupable). Convert content-cheapness into repeated launch-moment lottery tickets.

### 10.1 Two mechanisms that DO NOT EXIST (never plan around them)
1. **Pages do not merge.** Wishlists are per-app and non-transferable; there is no folding mechanism. A retired page's wishlists are stranded forever.
2. **There is no negotiating placement with Valve.** Visibility is algorithmic (New & Trending = launch *revenue* velocity; Popular Upcoming = *total* wishlists) or Valve-curated and earned (e.g., official Next Fest trailer consideration — Steam pulls trailers and notifies you; ~40K+ entering wishlists is what gets considered).

### 10.2 Architecture: mothership + satellites
- **Mothership** (Reap. Die. Rise.) page goes live early and is the ONLY wishlist jar for the paid game.
- **2–4 satellites:** permanently free standalone arcade apps, each targeting a **distinct tag-audience** (selection test: a separate page is justified only if it reaches an audience the mothership's page can't — horde-survival tags, TD/strategy tags, etc.). If satellites court one audience, the constellation fragments itself.
- **Satellites collect players, reviews, and followers — attention, which transfers. They do not collect mothership wishlists directly.** The funnel: in-game one-click wishlist prompts (overlay opens the mothership page) at victory/session-end screens; demo end-screens; the franchise/developer page (followers get notified of every release); devlog hub; page copy framing ("a free arcade mode from the Reap. Die. Rise. engine").
- **Both wishlist buttons stay live.** Satellite wishlists are not leakage — they are (a) fest ammunition (fest named-lists sort by the app's own totals) and (b) **deferred fuel**: on free release they fire as "a game you wishlisted is now available — free" notifications, delivering players directly into the in-game mothership prompt.

### 10.3 Satellite lifecycle (order is mandatory — fest rules force it)
Coming Soon page + demo → smaller genre festivals (unlimited) → its **one** Next Fest → **release free weeks after its own fest** (while its wishlists are warm; never held to the mothership's launch window) → permanent funnel duty.
Verified rules: fest = *unreleased* titles only (Early Access counts as released; a live free game is ineligible); demo publicly playable by fest start (top performers launch demos 1+ month early); release only after the fest ends; registration ~7–8 weeks prior.
**The perpetual-demo/shutdown path is forbidden:** demos earn no review score, their wishlists never fire, and deleting pages at launch destroys funnel infrastructure at the exact moment it matters while staining the shared engine reputation.

### 10.4 Fest-token sequencing: strictly sequential
One satellite per fest, one full outreach campaign per fest (top fest earners run multi-channel campaigns; bottom earners run none). Sequencing compounds: each fest grows the following the next launches from, and each teaches capsule/tag/hook lessons. **The mothership's token is sacred and goes LAST** — the last Next Fest before EA launch. Next Fest is a multiplier, not a generator.

### 10.5 Wishlist math (recalibrated)
"100K during one fest" is ~6× the observed all-time record (single-fest breakouts: ~15–16K; in Feb 2026, <4% of ~3,500 entrants held even ~40–50K *total*). Corrected target: **100K cumulative by EA launch.** Path: satellites + devlog accumulate 12–18 months → mothership enters its fest with 40–60K banked (Popular Upcoming placement; first ~48h of fest visibility is randomized-equal, then the algorithm amplifies performers; trailer-consideration territory) → fest adds a breakout-tier 10–20K → launch weeks later on hot velocity → New & Trending.
**Page craft rule:** 68–88% of fest wishlists come from people who never play the demo. The demo unlocks entry; **the capsule, tags, and page do the converting.** All five pages get the same craft investment.

### 10.6 Conversion realism & instrumentation
Devlog-following is the enthusiast tail (low single digits) — retention layer, not the funnel. The funnel is the in-game prompt (single-digit to low-teens conversion for well-executed cross-app prompts). Expect a satellite wave of tens of thousands of free players to yield low-thousands of mothership wishlists — meaningful and compounding, not the whole engine; the satellites' bulk value is fest tokens + review-proof + followers + the pivot option. **Instrument from satellite one:** UTM links + wishlist-source analytics; satellite→mothership conversion is a measured KPI and the constellation updates on data.

### 10.7 The substitution test (why free satellites can't undercut the mothership)
ARPG value is progression — the treadmill, the loot chase, permanence — not access to combat (PoE gives the whole game away and prints money). The membrane already strips satellites of the power economy; formalize the test: **a satellite ships free only if it does NOT satisfy the mothership's core promise — no persistent progression, no loot economy, and no full reap verb** (the title mechanic is mothership-exclusive; at most a teased taste). Satellites stay deliberately narrow (one template each) so their boredom horizon ends at the mothership prompt. Residual free-parkers were never buyers; in this market **obscurity costs more than cannibalization** by an order of magnitude. WC3 precedent: the free custom scene sold the box.

### 10.8 Pricing doctrine
- **Satellites: free, forever.** NEVER $5-then-free — paid→free triggers refunds and review-bombs that attach to the shared engine reputation across all five pages. Revenue valve if wanted: a cosmetic supporter pack (membrane-compliant).
- **Paid inversion rule (write the trigger in advance):** a satellite converts to paid ONLY via full inversion — its organic pull exceeds the mothership's, it *becomes* the flagship with a real price, roadmap, and support promise, and RDR ships into it as the content spine. Its non-transferable wishlists/reviews/velocity now work in our favor. Mechanical decision, not emotional.
- **Mothership: premium + cosmetics (the D4 shape, not PoE F2P).** Four grounds: F2P converts ~2–5% and needs six-figure day-one volume; New & Trending is revenue-ranked, so premium monetizes the wishlist-notification burst in the exact window the algorithm watches; a real price is a quality signal against the slop prior (52% dev-negativity climate + AI disclosure on the page); premium→F2P later is a celebrated second act, the reverse is impossible. F2P is a **gated future option** revisited only on proven massive volume + strong cosmetic attach.
- **The constellation-wide cosmetic registry:** one cosmetic entitlement (soul-weapon skin, banner, announcer pack) renders across mothership + all satellites + the eventual editor — unusually high perceived value per item, membrane-compliant by construction. Net shape: **F2P at the edges, premium at the core, one registry spanning all of it.**

### 10.9 Post-launch inversion
Satellites never close. After the mothership ships they invert into permanent acquisition infrastructure — the free top-of-funnel for the paid game ("liked this? the full engine is $X") — and become the natural home of the arcade's anomaly-slice previews, keeping them alive at near-zero cost since their content *is* pipeline output. Maintenance bill: the standing certification bar + occasional packet refreshes — for this engine, the cheapest maintenance in indie games.

**Verified sources for §10:** Steamworks Next Fest documentation (partner.steamgames.com/doc/marketing/upcoming_events/nextfest + 2026 editions) · presskit.gg Next Fest scheduling & prep guides (one-fest-ever rule, 68–88% page-conversion stat, demo-timing data) · tech-insider.org June 2026 fest analysis (record hauls, <4% threshold stat).
