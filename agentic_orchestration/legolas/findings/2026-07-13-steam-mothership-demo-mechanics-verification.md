# Steam Mothership + Standalone Demo Mechanics — Verification

**STATUS:** CURRENT
**Commissioned-by:** gandalf, per wind-down doc § 7.2 (fired at Matt's direct order 2026-07-13)
**Mode:** A (analytical research; read-only external sources)
**Date:** 2026-07-13
**Source document under verification:** `matt_notes_handoff_docs/gemini-steam-mothership-research-and-kit-naming-advice-for-devlog` (Gemini-authored, undated)

Verdict enum: **CONFIRMED / PARTIAL / REFUTED / UNVERIFIED**.
Rule: a claim scores PARTIAL when its main thrust holds but a load-bearing sub-claim is inaccurate or mis-stated in a way that would mislead a GTM decision.

---

## Per-claim verdict table

| # | Claim (paraphrased) | Verdict | Load-bearing correction |
|---|---|---|---|
| 1 | Demos have their own store page, library slot, reviews, and **community hub** | **PARTIAL** | Store page, library slot, and reviews CONFIRMED (post-July-2024). **Community hub REFUTED — Valve doc explicitly states demos do NOT have their own community hub.** |
| 2 | Valve auto-embeds native "Wishlist / Buy" UI on demo page and in-client; non-blockable, default | **CONFIRMED** | Automatic prominent link back to full game is Valve-authored default. In-game overlay via ISteamFriends is dev-implemented, not automatic. |
| 3 | "100% of demo player volume + downloads + reviews directly elevate the main premium page's discovery index" | **REFUTED (as stated); PARTIAL if softened** | Demo activity does NOT auto-aggregate into the main app's discovery ranking. Demo reviews stay on the demo page and do NOT roll into main-app review score. What IS confirmed: demo-launch is an event trigger (wishlist email, "New & Trending" chart entry, notify-followers button — one-shot), and demos are marketed as a top discovery mechanism. Load-bearing folklore, not policy. |
| 4 | Demo remains live indefinitely — before, during, after paid launch | **CONFIRMED** | No mandatory sunset or removal in Valve doc. Deactivation is dev-optional. |
| 5 | Packing ~10 mini-game modes inside one demo is compliant with current Valve demo policy | **PARTIAL / UNVERIFIED** | No explicit prohibition. Valve doc says demo content should be "specific to the demo" not the full game, and demo is intended for **purchase decision-making**. No stated one-demo-per-App-ID limit; language is singular ("your demo"). Precedent games doing "persistent multi-mode free portal" via demo App ID: none surfaced in this pass. Compliance is a Valve-review judgment call — likely to pass if framed as demo content, but no ex-ante guarantee. |
| 5b | Valve deprecated separate-free-prologue App IDs, making single-demo funnel more favorable | **CONFIRMED** | Valve directly said "changes to demos should make it unnecessary for developers to purchase a separate appID to use for prologues." (Aug 2024). Prologues not banned; demos are the Valve-preferred path. |
| 6 | Demos can be freely updated (e.g., bi-weekly new modes) without per-update review friction | **CONFIRMED** | Standard build-upload process. Initial demo release is reviewed (3–5 biz days); subsequent build updates follow same free-update model as any Steam game. Enabling a separate demo store page post-release doesn't require Valve review. |
| 7 | Current AI disclosure has two categories: Pre-Generated + Live-Generated | **CONFIRMED (with January 2026 update)** | Two-tier framework confirmed. Form rewritten **Jan 16-17, 2026** to focus on content "consumed by players." |
| 8 | AI-assisted CODE (GDScript via LLM) is exempt from disclosure | **CONFIRMED** (as of Jan 2026 update) | **Under the Jan-2026 rewrite: code assistants like Claude Code / Cursor / GitHub Copilot are OUT of scope.** Valve now explicitly excludes "efficiency gains through the use of AI-powered [dev] tools." Prior to Jan 2026, the form did list "code" in-scope; the claim would have been WRONG in 2024–2025 but is now CORRECT. Time-sensitive. |
| 9 | Proposed disclosure statement suffices under current rules | **PARTIAL** | The proposed statement covers pre-generated in-game text (safe). **Gap: if any LLM-generated content ships in MARKETING / STORE-PAGE assets (screenshots, capsule art copy, trailer text, "About This Game" section, community-hub posts), those ALSO require Tier-1 disclosure per Jan-2026 form.** The dev must audit the full ship-to-Steam surface, not just the game binary. Also: the word "seasonal" in the current draft is Reap-Die-Rise-internal jargon — Valve reviewers may not parse it; recommend "periodic" or "per-content-update." No adult-content AI attestation surfaced as relevant. |

**Headline verdict:** 5 CONFIRMED, 3 PARTIAL, 1 REFUTED (as stated), 0 UNVERIFIED. **The single load-bearing REFUTATION is the "100% elevates the main premium page's discovery index" claim (#3), which the Gemini doc leans on structurally.**

---

## Evidence sections

### Claim 1 — Demo store page / library / reviews / community hub

**Valve Steamworks documentation** (`partner.steamgames.com/doc/store/application/demos`, current):

- **Store page:** "You can choose to configure an entire store page for your demo, or just provide some assets for your demo to appear on your base game's store page." CONFIRMED.
- **Library slot:** Demos appear as distinct library entries with prominent link to full game's store page. CONFIRMED.
- **Reviews:** "Your demo will let players of the demo leave user reviews." CONFIRMED (per demo App ID with separate store page).
- **Community hub — LOAD-BEARING CORRECTION:** Valve's own doc states verbatim: **"Regardless of whether you create a separate store page or not, demos do not have their own community hub."** REFUTED.

The July 2024 overhaul ("The Great Steam Demo Update," announced 25 July 2024) added: separate store pages, user reviews on demo, add-to-library button, chart appearances in "New & Trending," and dev-triggered wishlist emails on demo release. Sources: TechRaptor 26-Jul-2024; Neowin 26-Jul-2024; Game World Observer 26-Jul-2024. The community-hub gap is documented, not a bug.

**GTM implication for the Simulation Hub concept:** community discussion + player conversation must live on the **main App ID's** community hub, not the demo's. The strategy doc's "separate community hub" bullet is wrong and any messaging built on it needs rewiring.

### Claim 2 — Wishlist / Buy embedding

Valve doc: **"Steam will automatically include a prominent link from your demo store page back to your full game, making it easy for players to wishlist or purchase your game."** Confirmed automatic and non-blockable at the platform level.

In-client overlay upsell during gameplay requires developer-side implementation via `ISteamFriends::ActivateGameOverlayToStore`. Not automatic — but trivial and standard.

### Claim 3 — "100% elevates the main premium page's discovery index"

**This is the single most consequential claim in the Gemini doc and it does NOT hold as stated.**

**Valve-official (from the demos doc):** demos can appear "anywhere in Steam that a free game could appear. This includes lists such as the 'New & Trending' as well as lists within store hubs, tag pages, genre pages." Valve makes NO claim of automatic algorithmic transfer from demo activity to main-app discovery.

**Reviews are NOT aggregated.** Reviews on a separate demo App ID show on the demo page only. They do not roll into the main app's Positive/Mixed/Negative score. Source: Game World Observer 26-Jul-2024 + Valve community forum discussion of "demos and reviews" (long-standing, "by design"). If demo reviews land Mostly Negative, the demo can get filtered from views by Steam's own low-review-score gate — a downside, not a boost.

**Credible empirical (Chris Zukowski, howtomarketagame.com):**
- Article 31-Jul-2024, "What Steam's big demo update means for your marketing strategy": the demo boost is **event-triggered** — a one-time wishlist notification email + "New & Trending" chart appearance at demo launch. He explicitly notes this is "essentially a button you can push that says 'more visibility.'" One shot, per demo.
- Article 31-Mar-2025, "Want to know the best way to gain attention on Steam? Add a demo": mechanisms named are concurrent-player thresholds (~100 CCU as an alleged algorithm signal), front-page featuring at demo launch, streamer amplification (streamers need something playable), and playtest priming. Zukowski does NOT argue continuous demo downloads/reviews boost main-app discovery.

**Empirical adjacent:** GameDiscoverCo (Simon Carless) "State of Steam wishlist conversions 2024-2025" — wishlists convert on median at 0.10-0.25x depending on volume + price band. Discovery Queue is ~half of first-two-weeks impressions but is triggered by wishlist volume and user-page conversion rate (Q2 2026: pages converting 4% visits→wishlists get re-recommended vs. 1.5% throttled). None of these attribute uplift to demo download volume as such.

**What IS true:** having a demo dramatically outperforms not having one for wishlist accumulation because (a) the free-download surface creates a low-friction entry funnel, (b) streamers can play it, (c) it triggers Steam's demo-launch email + chart placement, (d) Next Fest participation requires one. The mechanism is FUNNEL EFFECTS, not algorithmic transfer.

**REFUTATION-level summary:** the doc's "100% directly elevate" phrasing overclaims a mechanism that is real-but-indirect. A GTM plan that load-bears on continuous demo-review-count → main-app-discovery is building on folklore.

### Claim 4 — Permanent lifecycle

Valve doc: no mandatory sunset. Demo can pre-release ("release your demo's store page presence ahead of the release of your demo"), remain live through paid launch, and remain live indefinitely after. Deactivation is developer-optional. CONFIRMED.

**Caveat (surfaced by Zukowski 31-Jul-2024 as an open question but not resolved):** some developers speculated separate demo pages might be pulled at paid launch; Valve has issued no such rule. Current empirical: many post-launch games retain live demo pages (standard practice).

### Claim 5 — Multi-mode demo package + one demo per App ID

**Not explicitly addressed in Valve doc either way.** Language is singular ("your demo"). Valve doc guidance is that demo content should give players enough to make a **purchase decision** ("Balance giving the customer enough content to get them excited, without giving away so much that they feel like they've experienced everything the game has to offer") and if there's a separate store page, "ensure that the content is specific to the demo and not the full game."

**Compliance risk profile:** the Simulation Hub design is a marketing/funnel structure Valve reviewers haven't formally blessed but also haven't forbidden. A demo packaging 10 distinct mini-game modes as "Tactical Soul Simulations" would likely pass review IF the modes are framed as demo content (each mode uses the game's characters/kits/loot), IF the store page describes what's in the demo accurately, and IF the demo doesn't attempt to be a wholly separate service unrelated to the paid game. Valve retains discretion.

**Precedent scan (this pass):** no clear precedent found for a demo intentionally operating as a persistent multi-mode free portal. Absence of precedent ≠ prohibition, but it does mean the strategy is stepping into policy grey area. Recommend an explicit early Steamworks support ticket clarifying intent, or a small-mode initial demo release that Valve reviews before the full 10-mode expansion.

**Sub-claim 5b (Prologue-App-ID deprecation):** CONFIRMED. Valve stated verbatim (Aug 2024, via game industry press): "The changes already made to demos should make it unnecessary for developers to purchase a separate appID to use for prologues, and can instead use the demo appID that is already associated with their game." Prologues are not banned but Valve has signalled demos are the preferred path.

### Claim 6 — Update cadence

Standard Steam build submission. Post-initial-release, developers freely update demo builds without per-patch Valve gating. Initial demo build gets 3–5 business day review, then updates flow. Enabling a separate demo store page post-hoc requires no review. Bi-weekly mode drops are operationally viable. CONFIRMED.

### Claim 7 — AI disclosure categories

Original Steamworks AI content survey introduced **January 2024**. Two categories:

- **Pre-Generated:** "any kind of content (art/code/sound/etc) created with the help of AI tools during development" — as originally worded.
- **Live-Generated:** "any kind of content created with the help of AI tools while the game is running," with additional guardrail-description requirement.

**Form rewritten 16–17 January 2026** to focus on content "consumed by players" and to explicitly carve out efficiency-only tools. CONFIRMED with 2026 update.

Sources: original policy — Valve news post via Steamworks Development group (Jan 2024, Steam news app 4145017/view/3862463747997849618); 2026 rewrite — PC Gamer + StraySpark + BigGo News (17-18 Jan 2026).

### Claim 8 — Code exempt

**Confirmed under the January 2026 form rewrite.** Valve now specifies that AI-powered dev tools used for efficiency gains are not the focus of this section. Reporting cites specific examples: "If you use Claude Code, Cursor, GitHub Copilot, or similar tools to write game code, that code is not considered AI-generated content" (StraySpark 17-Jan-2026 summary of the revised form).

**Historical time-sensitivity note:** this was NOT the clear read of the form pre-January 2026 (the original text listed "code" in-scope alongside art/sound). The strategy doc is correct today; would have been wrong in 2024–2025.

### Claim 9 — Proposed disclosure statement

The Gemini-drafted disclosure text:

> "We utilize an LLM tool in our pre-runtime content pipeline to generate periodic variations of character names, item titles, and flavor/lore text fields. This data is fully baked into static JSON files prior to the game compiling and shipping. The game client itself does not make any live external network calls to AI services during active gameplay."

**Assessment:** covers the in-game pre-generated text case correctly. Two gaps:

1. **Marketing / store-page assets:** Under the Jan-2026 rewrite, AI-generated assets that appear in Steam Store marketing (capsule art, screenshots, About This Game text, trailer captions) or on the Steam Community page also require Tier-1 disclosure. If any marketing surface uses LLM-generated copy, that must be disclosed separately or the statement must broaden. Confirm with dev pipeline: are store-page descriptions, capsule art copy, trailer text ever LLM-drafted?
2. **Word choice:** "seasonal" is Reap-Die-Rise-internal (Phase-0 seasonal-journey framing). Valve reviewers won't know that. Use "periodic" / "per-content-update" / "prior to each content patch" to keep it plain-language.

No adult-content AI attestation is needed for this project as scoped. No other current disclosure regime encroaches.

### Bonus — 2025–2026 changes affecting the strategy

- **Popular Upcoming threshold:** raised from ~7K wishlists to ~100K wishlists in June 2024 (Zukowski data). Popular Upcoming is materially harder to reach; the Simulation Hub's job of accumulating wishlists is bigger than it would have been pre-2024.
- **Discovery Queue page-conversion signal:** Q2 2026, Steam started weighting page visit→wishlist conversion rate materially; well-converting pages (>4%) get re-recommended, poorly-converting (<1.5%) throttled. The main premium page's on-page conversion matters distinctly from the demo's traffic volume.
- **Wishlist-email cooldown:** 2-week cooldown between the four trigger emails (launch / EA-to-1.0 / 20%+ discount / demo release). Each demo can push notify only once. Bi-weekly mode drops therefore cannot leverage new notify emails per drop — the notify-button is a per-demo-instance shot, not per-update.
- **Next Fest one-per-game:** each game can participate in Next Fest exactly ONCE, ever. The Simulation Hub cannot leverage recurring Next Fest visibility events for the main game — only one Next Fest window is available.
- **Store-page-description rule tightening (Sep 2024):** no external links, no cross-promotion imagery mimicking Steam UI, no store pages that are "effectively advertisements for other store pages." Affects how the demo page links can be structured.
- **Review-bombing protections for demos:** no separate demo-specific policy surfaced; general review-bombing detection applies. Since demo reviews don't aggregate into the main app, a demo review-bomb hurts the demo page's filtering but not the main app's score.

---

## GTM consequences (neutrally stated — findings only; design read is gandalf's)

**Stands as-is:**

- Standalone Demo with separate store page as the "Simulation Hub" surface. Feature set (page, library, reviews, chart appearances, wishlist emails, add-to-library, dev-updatable) is Valve-supported.
- Permanent lifecycle (pre-launch → live-launch → post-launch, indefinitely). No policy forcing removal.
- Native Wishlist / Buy upsell link on the demo store page (automatic, non-blockable).
- AI-disclosure story for pre-generated in-game text under the Jan-2026 rewrite.
- Code-gen exemption for GDScript / Godot script work.
- Prologue-vs-demo positioning: demos are the Valve-preferred funnel; the strategy's choice to avoid separate prologue App IDs aligns with Valve's stated preference.
- Bi-weekly update cadence for demo builds is operationally viable.

**Needs reshaping:**

- **Discovery-index claim (#3):** the doc's "100% elevates the main premium page's discovery index" phrasing is folklore-shaped. Demo activity does NOT auto-aggregate into main-app discovery ranking; demo reviews do NOT roll into the main app's score. The real funnel effects are (a) demo-launch email + New-and-Trending event, (b) streamer accessibility, (c) main-page traffic driven by "wishlist the full game" link. GTM messaging and roadmap KPIs need to be rewritten to target those real levers, not the folkloric aggregate-boost.
- **Community-hub claim (#1):** demos do not have their own community hub. Player conversation lives on the main App ID's community hub. Community-strategy planning around a "demo community hub" needs to redirect.
- **Multi-mode demo compliance (#5):** grey area, not confirmed. Recommend an explicit early Steamworks support ticket clarifying the intent before all 10 modes ship. Consider starting with 2–3 modes and expanding, so Valve's initial review pass is over a familiar-shaped demo.
- **AI-disclosure statement (#9):** broaden to explicitly address marketing / store-page assets (or confirm none are LLM-authored). Replace "seasonal" with plain-language phrasing.
- **Wishlist-notify one-shot:** the "notify wishlisters when demo launches" button fires ONCE per demo. Bi-weekly mode-drop cadence cannot rely on notify-email as its comms surface; alternative comms (Steam news posts, community hub posts on the main App ID, external channels) must carry the recurring drops. This affects the "high-velocity bi-weekly deployment cycle" section's assumed leverage.
- **Next Fest one-per-game:** the Simulation Hub cannot leverage recurring Next Fest events. Pick one Next Fest window strategically; do not plan around recurring appearances.

**Compliance-flag-worthy:**

- Multi-mode demo may not survive strict "specific to the demo and representative of full game" reading in Valve review. Mitigation: frame each mode as a "Tactical Soul Simulation" that showcases character kits + combat mechanics from the paid game (which the strategy doc already proposes) so each mode is provably a slice of the paid game's core loop, not an independent product.

---

## Source list

**Valve-official:**
- Steamworks Documentation, "Demos": https://partner.steamgames.com/doc/store/application/demos (fetched 2026-07-13)
- Steamworks Documentation, "Content Survey": https://partner.steamgames.com/doc/gettingstarted/contentsurvey (fetched 2026-07-13)
- Steamworks Documentation, "Steam Next Fest" + child pages (2026 editions): https://partner.steamgames.com/doc/marketing/upcoming_events/nextfest (fetched 2026-07-13)
- Steamworks Development news, "AI Content on Steam": https://store.steampowered.com/news/group/4145017/view/3862463747997849618 (published Jan 2024; fetched 2026-07-13)

**Empirical / industry press (dated):**
- TechRaptor, "Valve Overhauls Steam Demos with Separate Store Pages and More," 26-Jul-2024: https://techraptor.net/gaming/news/valve-overhauls-steam-demos
- Neowin, "Valve makes major changes to Steam game demos, offering store pages, reviews, and more," 26-Jul-2024: https://www.neowin.net/news/valve-makes-major-changes-to-steam-game-demos-offering-store-pages-reviews-and-more/
- Game World Observer, "Steam revamps game demos with separate store pages, user reviews, and other features," 26-Jul-2024: https://gameworldobserver.com/2024/07/26/steam-game-demos-update-reviews-store-pages-charts
- GamesRadar, "Valve overhauls Steam demos to act more like full games," 2024: https://www.gamesradar.com/games/valve-overhauls-steam-demos-to-act-more-like-full-games-complete-with-user-reviews-and-chart-positions/
- Chris Zukowski / How To Market A Game, "What Steam's big demo update means for your marketing strategy," 31-Jul-2024: https://howtomarketagame.com/2024/07/31/what-steams-big-demo-update-means-for-your-marketing-strategy/
- Chris Zukowski, "Want to know the best way to gain attention on Steam? Add a demo," 31-Mar-2025 (via Game Developer): https://www.gamedeveloper.com/marketing/want-to-know-the-best-way-to-gain-attention-on-steam-add-a-demo-
- Game Developer, "Valve implementing new rules to 'refine' Steam store page written descriptions," 14-Aug-2024: https://www.gamedeveloper.com/marketing/valve-implementing-new-rules-to-refine-steam-store-page-written-descriptions
- PC Gamer, "Valve issues new rules outlawing links in Steam page descriptions... prologue games," Aug 2024 (referenced): https://www.pcgamer.com/games/valve-issues-new-rules-outlawing-links-in-steam-page-descriptions-hopefully-bringing-an-end-to-the-plague-of-demos-pretending-theyre-prologue-games/
- PC Gamer, "Steam updates AI disclosure form to specify that it's focused on AI-generated content that is 'consumed by players'," Jan 2026 (referenced): https://www.pcgamer.com/software/ai/steam-updates-ai-disclosure-form-to-specify-that-its-focused-on-ai-generated-content-that-is-consumed-by-players-not-efficiency-tools-used-behind-the-scenes/
- StraySpark, "Steam's 2026 AI Disclosure Rules: What Indie Developers Actually Need to Know," ~17-Jan-2026: https://www.strayspark.studio/blog/steam-ai-disclosure-rules-2026-indie-developer-guide
- BigGo News, "Valve Clarifies Steam's AI Disclosure Rules: Focus Shifts to Player-Facing Content, Not Dev Tools," 17-Jan-2026: https://biggo.com/news/202601171220_Steam_AI_Disclosure_Update_Focuses_on_Player_Content
- freethoughtblogs / A Trivial Knot, "On Steam AI disclosures," 04-Dec-2025: https://freethoughtblogs.com/atrivialknot/2025/12/04/on-steam-ai-disclosures/
- presskit.gg, "Steam Next Fest Dates & Registration Deadlines (2026-2027)": https://presskit.gg/field-guides/next-fest-scheduling-registration
- presskit.gg, "How Steam Wishlists Work" + "Steam Page Optimization Guide 2026": https://presskit.gg/field-guides/how-steam-wishlists-work
- GameDiscoverCo (Simon Carless), "The state of Steam wishlist conversions: 2024-2025": https://newsletter.gamediscover.co/p/the-state-of-steam-wishlist-conversions
- StraySpark, "Steam Algorithm Decoded 2026": https://www.strayspark.studio/blog/steam-algorithm-decoded-wishlists-visibility

**Access date for all URLs: 2026-07-13.**

## Knowledge gaps not resolved this pass

- **Precedent for a persistent multi-mode free demo portal on Steam.** No named precedent surfaced. Worth a targeted pass through recent Simulation Hub-shaped launches (Vampire Survivors → separate free game not a demo; Warhammer Skulls-style event demos are different pattern). If a precedent exists, it would materially reduce Claim 5's compliance risk.
- **Whether Valve reviewers have accepted or rejected multi-mode demo builds under the 2024 overhaul.** No dev postmortems located this pass. Steamworks support ticket is the direct-source path.
- **How Valve internally weights demo-page metrics into main-app discovery ranking.** Valve does not publish algorithm internals; Zukowski, GameDiscoverCo, and StraySpark speculate but cannot prove specific weights. My conclusion (no automatic aggregate transfer) is grounded in absence of Valve claim + empirical funnel-mechanism naming, not in a Valve-authored refutation.
- **Whether demo reviews with a separate App ID have EVER been used as an indirect signal (e.g., filter threshold) that affects main-app placement.** No evidence surfaced either way; assumed no per absence.
