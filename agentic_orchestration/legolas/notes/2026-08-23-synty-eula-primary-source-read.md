# Research — Synty EULA primary-source read (U-9(a)) — 2026-08-23

**Mode:** A (analytical / primary-source probe)
**Commissioner:** gandalf (fired by Matt)
**Agent:** legolas (UNKNOWN-RESEARCHER)
**Retrieval date for all sources:** 2026-08-23
**Access method:** read-only HTTP GET, public pages, no authentication.
**Status of this note:** evidentiary. Verdicts below are research findings, not legal advice.

---

## Summary

The July-2026 Synty EULA revision claim is **CONFIRMED**, and it is narrower and sharper than the Codex flag implied. Both Synty licences carry a version stamped **9 July 2026**, and a machine-diff against the immediately-prior 3 June 2026 versions shows the revision added **exactly two AI clauses and nothing else** — a prohibition on "Generation of 3D models utilising Generative AI Programs," and a ban on uploading source files or models to third-party services for 3D-model generation. Both land directly on the ensemble pipeline's Stage-4 image→3D (Tripo-class) slot. The revision was **not** editor-related: the editor restriction ("Game Creation Software") has been in the EULA continuously since 11 October 2022 and is unchanged.

The single most consequential finding is one nobody asked for: the **3 June 2026** revision *removed* a blanket prohibition on using Assets "**as inputs to Generative AI Programs**" that had been in force since at least October 2022. Combined with the OTP's "changes will not affect your rights under any licences that you have already purchased," this means **which EULA version governs depends on when Matt bought the packs** — and packs bought before June 2026 may still sit under a blanket AI-input ban that would prohibit not only the Tripo path but also cloud vision-LLM screenshot judging. That is the highest-value question in the T18 letter.

**H-Matt is CONFIRMED on its conclusion and only partially on its reasoning.** Shipped game and minigames are cleanly permitted; the player-facing editor is the out-of-bounds surface. But the extractability carve-out Matt hypothesised is *not* granted by the text — the embedded-runtime/data-contract design addresses Synty's stated *rationale* while the owner-side prohibition as written is flat and unconditioned.

---

## 1. Pinned source register

| # | Document | URL | Version / effective date | Grade |
|---|---|---|---|---|
| S1 | **One-Time Purchase Licence & EULA** (current) | `https://syntystore.com/pages/one-time-purchase-licence` | Self-labelled **"One Time Purchase Licence [Current] / As at 9 July 2026"** | Primary |
| S2 | **Standard Subscription Licence & EULA** (current) | `https://syntystore.com/pages/standard-subscription-licence` | Self-labelled **"[Current]"**; body: *"These Terms were last updated on 9 July 2026"* | Primary |
| S3 | **EULA Versions History** (index) | `https://syntystore.com/pages/eula-versions-history` | Undated index page | Primary |
| S4 | OTP Licence — prior version | `https://syntystore.com/pages/one-time-purchase-licence-3-june-2026` | Self-labelled **"As at 3 June 2026 - 9 Jul 2026"** | Primary |
| S5 | OTP Licence — prior version | `https://syntystore.com/pages/one-time-purchase-licence-13-november-2025` | "As at 13th November 2025" | Primary |
| S6 | OTP / EULA archive | `https://syntystore.com/pages/archive-end-user-licence-agreement-4th-april-2024` | "As at 4th April 2024" | Primary |
| S7 | OTP / EULA archive | `https://syntystore.com/pages/archive-end-user-licence-agreement-11-october-2022` | 11 October 2022 | Primary |
| S8 | OTP / EULA archive | `https://syntystore.com/pages/archive-end-user-licence-agreement-7th-october-2019` | 7 October 2019 | Primary |
| S9 | Subscription Licence — prior version | `https://syntystore.com/pages/standard-subscription-licence-june-3-2026` | "current 3 June - 9 July 2026" | Primary |
| S10 | **Synty FAQ** (official) | `https://syntystore.com/community/faq` | No date stamp on page | Primary (official, undated) |
| S11 | Licences Overview | `https://syntystore.com/pages/licences-overview` | No date stamp | Primary |
| S12 | Custom Licencing plans | `https://www.syntystudios.com/licencing-plans` | No date stamp | Primary |
| S13 | **Unity Asset Store Terms of Service and EULA** | `https://unity.com/legal/as-terms` | **"Last updated: December 4, 2024"** | Primary (other channel) |
| S14 | Synty Godot asset-pack collection | `https://syntystore.com/collections/godot-asset-packs` | Live catalogue, **19 products** | Primary |
| S15 | Epic / FAB Content EULA | `https://www.fab.com/eula`, `https://www.unrealengine.com/eula/content` | **NOT RETRIEVED — HTTP 403** to agent fetch (both URLs, two user-agents) | **UNRESOLVED** |

Also confirmed: `https://syntystore.com/pages/end-user-licence-agreement` (the site-footer "Licensing Terms" link) is **byte-identical** to S1 — it is an alias, not a third licence.

**Method note.** Clause-presence checks were run on whitespace-normalised text. An initial pass produced a *false negative* on the 2022/2024/Nov-2025 archives because those pages encode `&nbsp;` between words, which does not match a literal-space pattern. All lineage claims in §3 were re-verified after normalising U+00A0 → space. Flagging this because the first-pass result would have produced a confidently wrong lineage table.

---

## 2. July-2026 revision claim: **CONFIRMED**

Both current licences are stamped **9 July 2026**. Machine-diff of the licence body against the immediately-prior versions isolates the change set exactly.

### One-Time Purchase Licence — 3 June 2026 → 9 July 2026

Two additions, nothing else changed (no deletions, no other edits):

**(a)** New bullet in the prohibited-products list:
> "Generation of 3D models utilising Generative AI Programs." — S1

**(b)** New final sentence under the **Source files** heading:
> "You may not upload source files or models to third party services for the purpose of 3D model generation." — S1

### Standard Subscription Licence — 3 June 2026 → 9 July 2026

One substantive addition — a new clause 1.4(b), re-lettering the former (b)→(c) and (c)→(d):
> "1.4 You may not use our Assets for the following purposes: … (b) Generation of 3D models utilising Generative AI Programs." — S2

### What the revision was NOT

The Codex flag was "AI/editor use." The **editor half is not part of the July revision.** The clause
> "Creation of content for Metaverse-related and/or Game Creation Software and products." — S1

has been present continuously since **11 October 2022** (S7) and is textually unchanged through the current version. The editor exposure is real but it is ~4 years old, not new.

### Clause lineage (verified, whitespace-normalised)

| Clause | 7 Oct 2019 | 11 Oct 2022 | 4 Apr 2024 | 13 Nov 2025 | 3 Jun 2026 | **9 Jul 2026** |
|---|---|---|---|---|---|---|
| GenAI dataset / development ban | absent | present **incl. "or as inputs to"** | present **incl. "as inputs to"** | present **incl. "as inputs to"** | present — **"as inputs to" REMOVED** | present (same as Jun) |
| "Generation of 3D models utilising Generative AI Programs" | absent | absent | absent | absent | absent | **ADDED** |
| "may not upload source files or models to third party services for … 3D model generation" | absent | absent | absent | absent | absent | **ADDED** |
| Metaverse / Game Creation Software ban | absent | present | present | present | present | present |

### The June-2026 deletion — the finding under the finding

13 Nov 2025 text:
> "Inclusion in datasets utilised by Generative AI Programs; in the development of Generative AI Programs; **or as inputs to Generative AI Programs**." — S5

3 Jun 2026 text (and current):
> "Inclusion in datasets utilised by Generative AI Programs; or in the development of Generative AI Programs." — S4, S1

The blanket **AI-input** prohibition was deleted in June 2026 and then, in July 2026, replaced by a **narrower, activity-specific** ban aimed at 3D-model generation. Read as a trajectory: Synty relaxed the general AI-input position and simultaneously hardened the specific one that threatens their business (asset generation).

This matters because of the OTP's change clause:
> "We can change this EULA at any time, by making a new version available through the relevant Store. However, **our changes will not affect your rights under any licences that you have already purchased**." — S1

That is a **rights-preserving ratchet pinned to purchase date**. It plainly protects a licensee from *new* restrictions. It is silent — and therefore ambiguous — on whether a licensee *benefits* from *relaxations*. If Matt's packs were bought before 3 June 2026, the pre-June blanket "as inputs to Generative AI Programs" ban may still be the operative term for those packs.

---

## 3. Use-surface verdict table

Evidence grades: **A** = explicit clause; **B** = official FAQ / staff statement; **C** = inference from clause language (marked honestly).

| # | Surface | Verdict | Grade | Governing clause |
|---|---|---|---|---|
| 1 | **Shipped ARPG** (Synty meshes embedded in Godot build, sold) | **PERMITTED** | **A** | "your licence entitles you: to incorporate the Asset into Products produced under your direct control… to publish, distribute… the Asset as incorporated into those Products"; *"Product means any videogame (which will always be covered by your licence)"* (S1). Engine scope: *"The licence is worldwide, and is not limited by game engine, OS, platform or device"* (S1). Corroborated (B): FAQ *"Yes, you can use Synty assets for your commercial game"* (S10). |
| 2 | **Minigames** (same embedding, same product family) | **PERMITTED** | **A** | Same clause; "Products" is plural and unrestricted as to count, qualified only by "produced under your direct control" (S1). No per-title licence limit found. |
| 3a | **Internal dev editor** (Matt-only, never distributed) | **PERMITTED** *(inference)* | **C** | No clause squarely reaches it. Subscription defines Content Creation System as software "which enables **end users** to create commercialised content" (S2 §14.1) — an internal tool has no end users. FAQ's owner-side prohibition is framed around "distribute our assets to users in the platform" (S10) — no distribution here. **Caveat:** the OTP's bare phrase "Game Creation Software" is *undefined in the OTP* and a literal reading could reach any editor. Low risk, but it is inference, not text. |
| 3b | **Product-grade player-facing editor** (UGC; data contracts through shipped runtime) | **PROHIBITED without custom licence** | **A** (subscription) / **B** (one-time) | Subscription, explicit: *"1.6 You may not use our Assets for the creation and development of Content Creation Systems."* and *"1.7 …provided that you are **not the developer or owner** of the Content Creation System"* (S2). One-time route is via FAQ: *"As a Metaverse **Owner** you can not create software that allows a user to create a project (e.g. a game) for other users to experience. You must have a custom license to distribute our assets to users in the platform."* (S10). Escape hatch exists: S2 §5.4 directs Content Creation System licensing to `licencing@syntystudios.com`; S12 lists "User Created Content" under the NFT & Metaverse tier. |
| 4 | **Editor-time AI-agent use** (Claude/Codex via MCP placing Synty assets during dev) | **AMBIGUOUS** — leans permitted under current text | **C** | Current text prohibits four enumerated activities only: dataset inclusion, GenAI development, 3D-model generation, and GenAI-related promo (S1). Agentic scene assembly generates no 3D model and develops no GenAI program. **But** the definition is very broad — *"Generative AI Programs means artificial intelligence, machine learning… designed to automate the generation of or **aid in the creation of** new content"* (S1) — and an MCP agent reading mesh/scene files into a model context is arguably supplying Assets *to* such a program. Squarely prohibited under **pre-June-2026** text ("as inputs to"). Version-pinning (§2) is decisive here. **No FAQ guidance exists** (see negative finding below). |
| 5(i) | **Image→3D generation** (Tripo-class, on Synty-derived captures) | **PROHIBITED** | **A** | Two independent clauses, both added 9 Jul 2026: *"Generation of 3D models utilising Generative AI Programs."* and *"You may not upload source files or models to third party services for the purpose of 3D model generation."* (S1); subscription equivalent at §1.4(b) (S2). **Note the render-instead-of-mesh workaround does not escape:** the second clause is input-scoped ("source files or models"), but the first is *activity*-scoped and prohibits the generation outcome regardless of input form. |
| 5(ii) | **Cloud vision-LLM judging** of Synty screenshots (Anthropic API) | **AMBIGUOUS** — leans permitted under current text | **C** | Under 9 Jul 2026 text no clause squarely reaches it: not dataset inclusion (no training), not GenAI development, not 3D-model generation, not GenAI promo (S1). **But** squarely prohibited under pre-June-2026 "as inputs to Generative AI Programs" (S5/S6/S7). Also **prohibited outright** if any pack came from the Unity Asset Store (see §5). FAQ *"it is prohibited to resell our assets rendered as image files"* (S10) concerns resale, not evaluation, and does not bite. |
| 6 | **Marketing surfaces** (trailers, screenshots, Steam page) | **PERMITTED for own-made materials — with one live risk** | **A** + **B** caveats + **C** risk | Entitlement: *"to incorporate the Asset into Products… and into promotional materials (graphics, videos or print media) for those Products"* and to "publish, distribute… broadcast" them (S1). **Caveat 1 (B):** you may not use *Synty's own* media — *"No, you can not use our media for the promotion of your game, for example on Steam or Kickstarter"* (S10). **Caveat 2 (B):** *"it is prohibited to resell our assets rendered as image files"* (S10). **RISK (C) — see §4.1 below.** |
| 7 | **Asset-protection obligation** in distributed builds (Godot `.pck` extractability) | **NO OBLIGATION FOUND** | **A (negative)** | Keyword sweep of both current licences for *decompile / reverse engineer / extract / reasonable measures / protect / redistribute* returns **no** affirmative technical-protection duty. Nearest clause is conduct-scoped, not technical: *"you must not distribute our Assets as stock images or stock art (2D or 3D) or otherwise share them for re-use by third parties"* (S1). **Compliance-action candidate, not prescribed:** Godot supports PCK encryption; this becomes materially more load-bearing if surface 3b ever ships, since asset egress is precisely Synty's stated concern (§4). |

### Negative finding worth recording

**The Synty FAQ contains zero AI guidance.** A case-insensitive sweep of S10 for *generative / artificial intelligence / machine learning / " AI "* returns **0 hits**. Every AI verdict above therefore rests on licence text alone, with **no Grade-B corroboration available**. That absence is itself the argument for the T18 letter: on the AI surfaces there is no published interpretive layer to lean on, only clause text that changed twice in five weeks.

### Engine scope — resolved clean

Godot is fine. The licence is **explicitly engine-agnostic**: *"The licence is worldwide, and is not limited by game engine, OS, platform or device"* (S1). Synty now sells a **dedicated Godot line — 19 products** (S14). The FAQ's older, more cautious line — *"we currently only provide official support for Unity and Unreal Engine"* (S10) — is about **support**, not licence permission, and is superseded on the catalogue side by S14. No engine restriction exists.

---

## 4. H-Matt verdict: **CONFIRMED on the conclusion; PARTIALLY on the reasoning**

**H-Matt:** *shipped game and minigames permitted; "the editor" potentially out of bounds — with the load-bearing question being whether embedded-runtime UGC is distinguished from exposing assets in extractable/reusable form.*

**Confirmed:** surfaces 1 and 2 are permitted at Grade A. Surface 3b is the out-of-bounds surface, and it is out of bounds by a clause that has nothing to do with AI and predates the July revision by ~4 years. Matt's instinct correctly located the risk.

**Partially confirmed — the seam, head-on.** The distinction Matt hypothesised is *visible in Synty's reasoning but absent from Synty's operative text.*

**Synty's rationale is exactly asset-egress.** The FAQ's user-side examples are all about assets escaping the licensee's control:
> "as a player of VR Chat you are able to make a world for other players to visit but **they are not allowed to take any assets with them to other worlds not under your direct control**." — S10
> "as a Roblox Player you are able to make your own Roblox game but **assets are not allowed to be shared with other users for projects outside of your product**." — S10
> "…as long as they remain **under your direct control and are not sublicensed in any way**." — S10

The RDR editor design — scenario data edited through the shipped runtime, assets never exported, never downloadable, never usable outside the build — **satisfies every one of those conditions.** On rationale, the design is aligned.

**But the owner-side prohibition is stated flatly and is not conditioned on extractability:**
> "As a Metaverse Owner **you can not create software that allows a user to create a project (e.g. a game) for other users to experience.**" — S10

That sentence contains no carve-out for embedded assets, no reference to extraction, and no commercialisation qualifier. A deferred player-facing scenario editor does precisely what it describes.

**Two textual seams could still carry the carve-out — both genuinely open:**

1. **The commercialisation hinge.** The subscription definition reads: *"Content Creation System means any software… which enables end users to create **commercialised** content with our Assets, including without limitation, for the creation of game mods, user-generated content, standalone products, **or where user-generated content is the primary purpose of the Product**."* (S2 §14.1). If "commercialised" qualifies the whole definition, a non-commercial creator editor may fall outside. But the trailing limb carries **no commercialisation qualifier** and could stand alone. Unresolvable from the text.

2. **The OTP's directional ambiguity.** The one-time licence prohibits *"Creation of content **for** … Game Creation Software"* (S1) — grammatically the *user* side (making content for someone else's tool), not the *owner* side (building the tool). The subscription licence is the one that explicitly prohibits *"the creation and development **of** Content Creation Systems"* (S2 §1.6). **The two licences are not equivalent on the editor question**, and a one-time-purchase licensee's owner-side prohibition rests on FAQ interpretation (Grade B) rather than clause text.

**Operational read:** treat surface 3b as **requiring written clearance before any build work**, not as settled either way. The escape hatch is well-signposted and cheap to ask for: S2 §5.4 routes Content Creation System licensing to `licencing@syntystudios.com`, and S12 lists "User Created Content" as a feature of the NFT & Metaverse custom tier. Surface 3a (internal tooling) is low-risk and need not wait.

### 4.1 Unprompted risk surfaced — the AI-marketing clause vs. RDR's own AI feature

This was not in the commission's frame and is flagged because it is live and non-obvious.

A prohibition present since 2022 and **unchanged** in the current text reads:
> "Use in promotional, marketing, social media, blog posts, articles, images, videos or other materials **related to any Generative AI Programs or Products**." — S1

RDR's business strategy makes a runtime LLM feature a headline marketing beat (`business-platform-strategy.md` §4, "describe a mode, play it with bots" — constrained LLM parse → packet). A trailer or Steam page that shows **Synty assets** while presenting **that AI feature** is arguably "materials related to a Generative AI Program." Note also that "Product" is a **defined term** in the EULA meaning "any videogame" (S1) — so "Generative AI … Products" plausibly denotes *videogames that are generative-AI products*, which raises a second-order question about whether an LLM-driven game is itself such a Product.

Grade **C** (inference), but with high salience: it touches the launch marketing surface, it is cheap to clarify in writing, and it would be expensive to discover late. Two letter items (§5, Q8/Q9) cover it.

---

## 5. The ambiguity list — letter-ready (T18)

Each item is one sentence, answerable yes/no by Synty licensing. Ordered by decision value. **12 items.**

**Tier 1 — blocks pipeline or build decisions**

1. **Version pinning.** For packs we purchased before 3 June 2026, may we rely on the current 9 July 2026 EULA in its entirety — including the removal of the former "or as inputs to Generative AI Programs" restriction?
2. **Vision-model evaluation.** May we send screenshots or renders of scenes built with Synty assets to a third-party multimodal AI service solely for automated visual-quality evaluation, where no 3D model or derivative asset is produced and no data is retained for training?
3. **Image→3D confirmation.** Do we correctly understand that generating 3D models from Synty-derived images or meshes via any third-party generative-AI service is prohibited under the 9 July 2026 terms, with no exception for internal or non-distributed use?
4. **Embedded-runtime UGC editor.** If our shipped game includes an in-game editor where players arrange pre-authored scenes using Synty assets, and those assets remain embedded in our build — never exported, downloadable, or usable outside our game — does that require a custom licence?

**Tier 2 — scopes near-term development**

5. **AI coding agents in-editor.** May AI coding assistants (e.g. Claude, Codex) operating inside our development environment read, place, and configure Synty asset files during development of our own game?
6. **Internal tooling.** Does an internal-only level/scenario editor, used solely by our own team and never distributed, fall outside the "Game Creation Software" and "Content Creation System" restrictions?
7. **Non-commercial UGC.** Does the "Content Creation System" definition apply where end users cannot commercialise their creations?

**Tier 3 — launch-surface and compliance**

8. **AI-feature marketing.** Our game uses a language model at runtime to interpret player text into game modes; does the prohibition on Assets in "materials related to any Generative AI Programs or Products" prevent us from showing Synty assets in trailers or screenshots that also present this feature?
9. **Product classification.** Does a game that uses a language model at runtime to configure gameplay from player text count as a "Generative AI Program or Product" under the EULA?
10. **Asset protection.** Does the EULA require us to take technical measures (such as package encryption) to prevent extraction of Synty assets from our distributed game build?
11. **Custom-tier fit.** Would the "NFT & Metaverse" custom licence tier cover an in-game player-facing scenario editor of the kind described in Q4?
12. **Seat counting.** Do the licence seat limits count only natural persons, or must automated/AI tooling acting on the assets be counted as seats?

### Explicitly NOT ambiguous — do not spend letter goodwill on these

Shipped commercial game use (A); minigames (A); Godot/engine-agnosticism (A, explicit clause + a live 19-product Godot catalogue); own-authored promotional materials for own Products (A); NFT/blockchain (A, flat prohibition, no custom licence offered — S10).

---

## 6. Channel-dependence table

Matt's purchase channel is **not known** to this probe and was not guessed. The row that applies is the row to read.

| Channel | Governing licence | Seats | AI-input regime | Notes |
|---|---|---|---|---|
| **Synty Store (direct)** | Synty **One-Time Purchase Licence**, at the version in force **on purchase date** | **5 seats per licence purchase**; buy more if Team exceeds | Current: no blanket AI-input ban; 3D-model generation prohibited | Baseline case. "Store" expressly includes the Synty Store (S1). |
| **Humble Bundle** — 'The Best of Synty' #1–#5; 'Best of Polygon Game Dev Bundle' (2020) | **Same One-Time Purchase Licence**, with one delta | **ONE seat only** | Same as Synty Store | *"The EULA for all HUMBLE BUNDLES is mostly the same as the below One Time Purchase Licence, but; Products purchased via Humble Bundle are limited to **one seat only**"*; *"Assets from the Humble Bundle may be used in commercial games and projects, as long as they follow the terms of the One Time Purchase Licence"* (S1). Non-transferable to any other store or person. **Good news: Humble does not carry separate bundle-specific terms — it inherits the Synty OTP.** |
| **Unreal Marketplace / FAB** | Synty OTP applies — *"Store means the Synty Store, **Unreal Marketplace**, or any other store…"* (S1). Epic/FAB platform terms layer on top: **UNRESOLVED** | 5 (per OTP) | Synty terms; Epic layer unknown | FAQ routes buyers to separate "Unreal Marketplace" and "FAB" EULA documents (S10), implying a platform layer, but **Epic returns HTTP 403 to agent fetch** (S15). Requires human retrieval if this is the channel. |
| **Unity Asset Store** | **NOT the Synty EULA.** Synty's Store definition reads *"…or any other store where we offer Assets for purchase or download (**excluding the Unity Asset Store**)"* (S1). Unity Asset Store ToS & EULA governs (S13, last updated 4 Dec 2024) | Per Unity terms | ⚠️ **MATERIALLY STRICTER** | *"use the Unity Asset Store or Assets for purposes such as training an artificial intelligence or machine learning model without the express consent… This restriction includes… using such Assets… for data sets, in the creation process, **or as inputs for artificial intelligence or machine learning model programs, whether for commercial or non-commercial purposes**."* (S13). This is the language Synty *deleted* in June 2026, still live at Unity. **Under this channel, surface 5(ii) vision-LLM judging is prohibited, not ambiguous.** Corroborated by FAQ: *"Unity (UAS) and Unreal (FAB) are their own completely separate asset stores"* (S10). |
| **SyntyPass subscription** | **Standard Subscription Licence** (9 Jul 2026) | Per Subscription seats; Authorised User = anyone interacting with Assets in last 30 days (S2 §3.1) | Same 3D-gen ban | Adds explicit UGC handling absent from OTP: §1.3(b) permits *"creation and development of user generated content within a game, platform, engine, or middleware"*, §1.6 prohibits *"creation and development of Content Creation Systems"*. Also note §14.1 *Our Materials*: *"where you edit or alter our Assets, such edits form part of Our Materials and are our Intellectual Property"* — Synty claims IP in your modifications. Rights are subscription-contingent, not perpetual. |

**Channel triage, one line:** if any pack came from the **Unity Asset Store**, the AI questions are already answered *against* us and no letter changes that; if packs came from **Synty Store or Humble**, the OTP governs and the version-pinning question (Q1) is what decides the pipeline.

---

## 7. Knowledge gaps not resolved

- **Epic/FAB Content EULA (S15)** — HTTP 403 to agent fetch on both `fab.com/eula` and `unrealengine.com/eula/content`, across two user-agents. Agent-unfetchable; needs a human browser session. Only material if FAB/Unreal Marketplace is a purchase channel.
- **Synty FAQ has no date stamp** — cannot pin when the Metaverse/Game-Creation-Software answers were written, so cannot confirm they post-date the 9 July 2026 revision. They are consistent with current clause text, but their currency is assumed, not established.
- **No Synty staff statement located on AI tooling during development** (surface 4). Searched; the FAQ has zero AI content. Community sources were not used as a verdict basis per commission rigor.
- **Matt's actual purchase channel(s) and dates** — deliberately not guessed. Q1 and the channel table both hinge on this; it is the cheapest input Matt can supply and it collapses several ambiguities at once.
- **Subscription-licence prior versions (6 Mar 2025, 11 Sep 2024)** were indexed but not diffed — the June→July subscription diff was sufficient to characterise the revision claim, and no downstream verdict depended on the older subscription lineage.

---

## 8. Source list

All retrieved 2026-08-23, read-only.

- Synty One-Time Purchase Licence & EULA (current, as at 9 July 2026) — https://syntystore.com/pages/one-time-purchase-licence
- Synty Standard Subscription Licence & EULA (current, last updated 9 July 2026) — https://syntystore.com/pages/standard-subscription-licence
- Synty EULA Versions History — https://syntystore.com/pages/eula-versions-history
- Synty OTP Licence, 3 June 2026 — https://syntystore.com/pages/one-time-purchase-licence-3-june-2026
- Synty OTP Licence, 13 November 2025 — https://syntystore.com/pages/one-time-purchase-licence-13-november-2025
- Synty EULA archive, 4 April 2024 — https://syntystore.com/pages/archive-end-user-licence-agreement-4th-april-2024
- Synty EULA archive, 11 October 2022 — https://syntystore.com/pages/archive-end-user-licence-agreement-11-october-2022
- Synty EULA archive, 7 October 2019 — https://syntystore.com/pages/archive-end-user-licence-agreement-7th-october-2019
- Synty Standard Subscription Licence, 3 June 2026 — https://syntystore.com/pages/standard-subscription-licence-june-3-2026
- Synty Frequently Asked Questions — https://syntystore.com/community/faq
- Synty Licences Overview — https://syntystore.com/pages/licences-overview
- Synty Asset Custom Licencing plans — https://www.syntystudios.com/licencing-plans
- Synty Godot Asset Packs collection (19 products) — https://syntystore.com/collections/godot-asset-packs
- Unity Asset Store Terms of Service and EULA (last updated 4 December 2024) — https://unity.com/legal/as-terms
- Epic / FAB Content EULA — https://www.fab.com/eula and https://www.unrealengine.com/eula/content — **HTTP 403, not retrieved**

Licensing contact of record for T18: `licencing@syntystudios.com` (S2 §5.4, S12).

---

**Filed by:** legolas (UNKNOWN-RESEARCHER), 2026-08-23. Not committed — gandalf handles commit and downstream curation (U-9 status, T18 letter scope).
