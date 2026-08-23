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

---

# §9 Addendum — SyntyPass subscription: termination, survival, drift, seats — 2026-08-23

**Trigger:** Matt confirmed his packs are held via the **SyntyPass subscription**, not one-time purchase. §6's SyntyPass row noted "rights are subscription-contingent, not perpetual" but never read the termination/survival clauses. This addendum reads them.
**Hypothesis under test (H-Matt-2):** *assets used in a game are effectively "purchased as of the date the game is published" — a game published while subscribed retains its rights even if the subscription later lapses.*
**Retrieval date:** 2026-08-23 (all sources re-fetched fresh this pass; §1–§8 above unchanged).
**Sources added this pass:** S16 SyntyPass product page `https://syntystore.com/products/syntypass`; S17 Subscription Licence 6 March 2025 `https://syntystore.com/pages/standard-subscription-licence-march-6-2025`; S18 Subscription Licence 11 September 2024 `https://syntystore.com/pages/archive-standard-subscription-licence-11-september-2024`. S2, S4/S9, S1, S10, S11 re-retrieved.

## H-Matt-2 verdict: **PARTIAL**

Matt's *operational conclusion* is close to right; his *mechanism* is not in the document. **There is no "purchase" event anywhere in the subscription licence.** Nothing converts, nothing vests, no date pins anything. What clause 12 actually creates is a **development freeze** — you may keep and minimally maintain what you shipped, and you must stop building. The gap between "purchased as of publication date" and "frozen as of lapse date" is small in the happy case and material in three specific ones (below).

The single sharpest structural fact: the subscription licence **grants no affirmative right to publish, distribute or sell anything**, at any time — subscribed or not. Verified by keyword sweep (below). What the shipped game rests on post-lapse is the *absence of a prohibition*, not the *presence of a grant*.

---

## §9.1 — Q1: Survival on cancellation/lapse

### The controlling grant is expressly time-bounded

> "**6.1** **While you have an active Subscription**, we grant you and your Authorised Users a non-exclusive right to use our Assets for the Authorised Purpose (**which may be suspended or revoked in accordance with this Agreement**). This right cannot be passed on or transferred to any other person…" — S2 §6.1

And critically — **clause 6 is not in the survival list**:

> "**13.11** **Survival**: Clauses **8 to 12** will survive the termination or expiry of this Agreement." — S2 §13.11

The Asset Licence clause (6) is outside 8–12. The grant itself does not survive; only the IP, confidentiality, consumer-law, liability and termination clauses do. Post-termination conduct is therefore governed entirely by **clause 12**, which is inside the surviving set (§12.9 also self-survives).

### The operative post-termination clauses

> "**12.2** Upon termination of this Agreement in accordance with this clause 12, or expiry of the Subscription Period, you must **cease using our Assets in any new Intellectual Property (including Your Materials or New Materials) created following the date of termination or expiry**. **You reserve the right to make minor bug fixes such as maintenance updates to the Product if:** (a) the Product is not substantially developed, modified or improved after the date of termination or expiry; or (b) you are removing the use of our Assets from the Product." — S2 §12.2

> "**12.3** For the avoidance of doubt, If the Product is substantially developed, modified or improved **you are required to have an active Subscription**." — S2 §12.3

> "**12.4** Upon termination … you **must not create or share any new promotional or marketing material** (including social media posts) containing our Assets. **You reserve the right to leave live any promotional or marketing materials created and shared prior to the date of termination or expiry** of the Agreement." — S2 §12.4

> "**6.2** Where your Subscription expires or is terminated, you must cease using our Assets in **any new Intellectual Property created following the date of expiry or termination**, in accordance with clauses 12.2 and 12.4." — S2 §6.2

### Verdicts by sub-case

| Sub-case | Verdict | Grade | Basis |
|---|---|---|---|
| **(a) Game ALREADY PUBLISHED while subscribed** | **SURVIVES** — by implication and by carve-out, **not** by express grant | **B/C** | §12.2's restriction reaches only *new IP created after* termination; and its bug-fix proviso ("minor bug fixes such as maintenance updates to the Product") **presupposes a Product that continues to exist and be maintained post-termination**. §12.4's parallel "leave live" permission for pre-existing marketing shows the drafters knew how to preserve a pre-termination artefact. Corroborated Grade **B** by S16 (below). **But no clause says the shipped Product's licence continues**, and §6.1 is subscription-conditioned. |
| **(b) Game IN DEVELOPMENT at lapse** | **TERMINATES** | **A** | §12.2 + §12.3 are unambiguous and mutually reinforcing: cease using Assets in new IP; substantial development *requires* an active Subscription. Only two permitted activities remain — minor bug fixes to a frozen Product, or stripping the Assets out. **Development must stop.** |
| **(c) Continued SALE / distribution after lapse** | **AMBIGUOUS — leaning survives** | **C** | Nothing prohibits it: §12.2 is scoped to *creating new IP*, §12.4 to *new marketing material*; neither reaches distribution of an already-built binary. The §12.2 bug-fix carve-out is hard to make sense of unless the Product stays live. **But the subscription confers no distribution right to survive** — see the zero-hit sweep below. |

### The zero-hit sweep — the finding under the finding

Keyword sweep of the **entire** 9 Jul 2026 subscription licence body for an affirmative distribution entitlement (`publish` / `distribute` / `sell` / `sale` / `broadcast` / `incorporate` / `embed`) returns **no grant**. Every hit is a *prohibition* (§6.3(f), §6.3(h), §1.4(a)), a *tax* clause (§5.8), a *definition* (Asset Marketplace), or *dispute-resolution* boilerplate.

Compare the one-time licence, re-verified today:

> "…your licence entitles you: to incorporate the Asset into Products produced under your direct control… **to publish, distribute, transmit, broadcast, communicate, show and play the Asset as incorporated into those Products** and promotional materials…" — S1
> "**Your licence is perpetual, and cannot be terminated except as stated in this EULA.**" — S1

**The subscription has neither sentence.** Synty's own overview page states the distinction in exactly these terms:

> "[One Time Purchase] Under this licence, you will have **perpetual rights** to use the specific pack(s) you have purchased directly." … "[Standard Subscription] You are **licensed for development** using any assets available to you **while your subscription plan is active**." — S11

Note the word Synty chose for the subscription: **development**. That matches §1.3's Authorised Purpose, which enumerates creation/development and promotional materials — and does not enumerate publication or sale.

### The Grade-B evidence that supports Matt

Synty's own SyntyPass product page markets precisely Matt's model:

> "**Flexible Terms** — Flexible licensing terms mean you **stay subscribed during development, choose to cancel once your project is complete**." — S16

This is the strongest support for H-Matt-2 located anywhere, and it is marketing copy on the product page for the exact SKU Matt holds. It is **Grade B, not A** — it is not clause text and it does not appear in the Agreement. It is, however, close to unusable-if-false: it describes the intended lifecycle of the product being sold.

**Net read:** the happy path (ship it, then cancel, then keep selling the frozen build) is what Synty *sells* and what §12.2's bug-fix proviso *assumes*. The clause text supports it by omission rather than by grant. The three places the gap bites are (b) — development must stop, hard, Grade A — plus the two edge cases below.

### Two edge cases the clauses do not cleanly resolve

1. **Built-but-not-yet-published at lapse.** §12.2 restricts *creating new IP*; releasing an already-built binary is arguably not creation. But §12.4 flatly prohibits *creating or sharing any new promotional or marketing material* — so the game could not be marketed, store-paged or announced. A launch is not practically available post-lapse even if distribution technically is.
2. **Post-launch content updates.** §12.3 is the sharp edge for a live-service or seasonal shape: "If the Product is substantially developed, modified or improved you are required to have an active Subscription." A patch cadence that adds content is "substantially developed" on any natural reading. **For RDR's serial-content-emission direction this is the clause that matters most** — it means the subscription is not a development-phase cost that ends at launch, it is an ongoing cost for as long as the game receives content. Factual note; scoping is Matt's and gandalf's call.

---

## §9.2 — Q2: Terms drift — **no ratchet; current terms govern; renewal-time re-check is a REAL watch item**

### There is no rights-preserving clause

Keyword sweep of the full subscription body for `already purchased` / `will not affect your rights` / `new version available` / `licences that you have` / `perpetual` / `in perpetuity` / `irrevocable`: **zero hits.** The OTP's ratchet —

> "We can change this EULA at any time, by making a new version available through the relevant Store. However, **our changes will not affect your rights under any licences that you have already purchased**." — S1

— **has no subscription analogue.** The subscriber's only remedy against an adverse change is exit:

> "**1.8** We may change the scope of the Authorised Purpose (as set out in clause 1.3) from time to time and with **30 days prior written notice**. Where you reject any change to the scope of the Authorised Purpose, you reserve the right to **terminate** this Agreement in accordance with clause 12.6(c)." — S2 §1.8

> "**1.14** …you agree that **we may vary our Services or the Subscription Fees at any time**, by providing 30 days' written notice to you (*Variation Notice Period*). If you do not agree to any amendment… you may, before the end of the Variation Notice Period, **terminate** this Agreement…" — S2 §1.14

> "**13.1 Amendment**: Subject to clauses 1.13 and 1.14, this Agreement may only be amended if **we and you agree in writing**." — S2 §13.1

### An amendment-authority gap (flagged, not relied on)

§1.8's unilateral-change power is scoped by its own words to **clause 1.3** (the *Authorised Purpose* — the permitted list). §1.13/1.14 are scoped to *Services* and *Subscription Fees*. §13.1 otherwise requires mutual written agreement. But **both 2026 revisions edited clause 1.4 — the *prohibited* list** — which none of those three clauses plainly authorises Synty to change unilaterally. This is an arguable point, not a plank to stand on, and it is not a basis for acting against current terms. Recording it because it is cheap to raise in the T18 letter and it is the only leverage the subscription document contains.

### Drift is real, and it is *narrowly and exclusively* an AI watch

Full machine diff of the subscription licence body across **all four** published versions:

| Transition | Changes |
|---|---|
| 11 Sep 2024 → 6 Mar 2025 | **none** (byte-identical body) |
| 6 Mar 2025 → 3 Jun 2026 | **§1.4(a) only** — "development of or in connection with generative AI (**including as input for generative AI**), stock images…" **→** "In datasets utilised by Generative AI Programs; or in the development of Generative AI Programs; stock images…" |
| 3 Jun 2026 → 9 Jul 2026 | **§1.4(b) added** — "Generation of 3D models utilising Generative AI Programs." (former (b)→(c), (c)→(d)) |

**In ~22 months, clause 1.4 is the only clause Synty has ever edited, and both edits are AI clauses.** Everything else is byte-identical across all four versions — including the entire termination/survival regime (§6.1, §6.2, §12.1–12.9, §13.11), seats (§2, §3), amendment (§1.8, §1.13, §1.14, §13.1) and IP (§8, §14.1 definitions).

Two consequences:

- **The survival mechanics in §9.1 are the settled part of this document.** Two years of stability. They are not a moving target and can be banked with more confidence than the AI clauses.
- **The renewal-time re-check is a real watch item, and it is specifically a §1.4 AI-clause watch.** One clause, twice touched in five months. This is a cheap, targeted, automatable check — diff §1.4 against the pinned 9 Jul 2026 text at each renewal — not a general terms review.

### Downstream consequence: **T18 letter Q1 is MOOT for this channel**

§5 Tier-1 Q1 asks whether packs bought before 3 June 2026 may rely on the current EULA. **For the subscription channel that question does not arise** — there is no purchase-date pin, no version-pinning mechanism, and no rights-preserving clause. The current published version governs, full stop. The June-2026 relaxation (removal of the blanket "as inputs to Generative AI Programs" ban) therefore **applies to Matt now**, without needing Synty's confirmation. Recommend Q1 be retired or re-scoped to the OTP-held packs only (see caveat in §9.5).

---

## §9.3 — Q3: Seats

**Tier structure** (S16, retrieved 2026-08-23) — a single SyntyPass tier, two billing shapes:

| Plan | Price | Term | Seats |
|---|---|---|---|
| SyntyPass, monthly | **$40 USD/mo** | 3-month pre-paid minimum | **5 seats per licence** |
| SyntyPass, annual | **$30 USD/mo** billed annually | 12-month pre-paid (save 25%) | **5 seats per licence** |

> "**Licences - 5 seats per licence**" — S16
> "Please be aware there is a **3 month pre-paid minimum term** for our monthly SyntyPass subscription plan… your SyntyPass licensing will end after your 3 month pre-paid minimum term concludes." — S10

Same 5-seat allocation as an OTP purchase. **Seat headroom is a non-issue at Matt's scale** (1 human). Scaling is by whole subscriptions, not incremental seats: "**2.2** Where you require additional Seats, you must purchase an **additional Subscription**…" (S2 §2.2).

**Authorised User, verbatim** (§3.1; the §14.1 definition is identically worded):

> "**3.1** An Authorised User is **any, employee, contractor, or individual engaged by you to interact with our Assets or the Product in some capacity within the last 30 days**." — S2 §3.1 *(comma placement is Synty's)*

> "**Seats** means the maximum number of Authorised Users you may authorise to interact with our Assets, Product and access your Account." — S2 §14.1

### Does automated / AI tooling count as a seat?

**Verdict: NO on plain text — the actor categories are exhaustively human.** Grade **C** (inference), but strongly supported: all three enumerated categories — *employee*, *contractor*, *individual* — are natural persons, and each is qualified by "**engaged by you**," language of human engagement. An MCP agent or a CI job is none of the three. The human who directs the tooling is the Authorised User; the tooling is an instrument, not a user. This is the same answer §5 Q12 asks Synty to confirm, and the text leans clearly our way.

**The real seat exposure is the activity limb, not the actor limb.** Note "interact with our Assets **or the Product**" — and *Product* is defined expansively:

> "**Product** means **anything created, developed, modified or improved in the course of using our Services and Assets**." — S2 §14.1

So any person engaged who touches *the game*, even if they never open a Synty file, is an Authorised User consuming a seat. Immaterial at 1 human; flagged because it is broader than it reads at first pass and would bite on any future collaborator or contractor.

**One oddity, recorded not relied on:** §4.2 — "Each of your Authorised Users **will require your login**, to access your Account" — a shared-credential model, paired with §4.4's suspension power for "unauthorised or **excessive sharing of login details**." Internally awkward; no exposure at single-seat scale.

---

## §9.4 — Q4: Modifications-IP after termination — **no clause on point; asymmetry runs against us**

**Verdict: AMBIGUOUS / silent.** No clause addresses rights to modifications after termination. What *can* be established from text:

**(i) Synty owns your edits, and that ownership survives.**

> "**Our Materials** means our Assets and all Intellectual Property which is owned by or licensed to us and any improvements, modifications or enhancements of such Intellectual Property… **For the avoidance of doubt, where you edit or alter our Assets, such edits form part of Our Materials and are our Intellectual Property.**" — S2 §14.1

> "**8.4** As between the Parties, ownership of all Intellectual Property Rights in any New Materials created by you in the course of the Agreement (**excluding the use, modification, or improvement of Our Materials**) will at all times vest, or remain vested, in you upon creation." — S2 §8.4

Your ownership of New Materials is expressly carved to *exclude* modifications of Synty assets. **8.6** and **13.11** put clause 8 in the surviving set — so §8.1/§8.4 ownership survives termination.

**(ii) Your only right in those modifications is a *revocable* licence.**

> "**8.3** We grant you a non-exclusive, **revocable**, royalty-free, worldwide, non-sublicensable and non-transferable right and licence, to use Our Materials that we provide to you, **solely for your use and enjoyment of the Services for the Authorised Purpose**, as contemplated by this Agreement." — S2 §8.3

Because edits *are* Our Materials, §8.3 is the clause governing your use of your own modifications. It is expressly **revocable**; it is tethered to "the Services," which §6.1 conditions on an active Subscription; and it is nowhere made perpetual.

**(iii) The interaction with lapse is genuinely unresolved.** §8.3 nominally survives (it is in clause 8, and 13.11 preserves 8–12), but it is tied to Services access that ends at lapse — a circularity the document does not resolve. Meanwhile §12.2's freeze does **not** distinguish modified from unmodified assets, so on clause 12 alone modified assets sit in the same position as unmodified ones.

**The asymmetry, stated plainly:** for unmodified assets, lapse leaves you holding a frozen build of material Synty licensed you. For **modified** assets, lapse leaves you holding a frozen build of material **Synty owns**, under a licence Synty may **revoke**, with no clause preserving your position. That is a strictly worse footing, and it is the one place where "purchased as of publication date" is most clearly not what the document says.

**Design-level mitigation, noted factually — Matt/gandalf decide.** The exposure scales with how much we *edit* Synty meshes as opposed to *composing* them. Scene assembly, parenting, transforms, material/shader swaps and LOD config do not obviously "edit or alter our Assets" in the §14.1 sense; mesh edits, re-topology and baked-down derivatives plainly do. Keeping the presentation seam compose-first rather than edit-first keeps the §8.3 revocable-licence surface small. This is a finding, not a recommendation.

---

## §9.5 — Surfaced unprompted: **Synty sells a generative-AI custom licence**

Not in the commission frame; material enough to record. The SyntyPass product page lists, immediately beside the Standard Subscription Licence:

> "**Custom Licence** — For custom licensing to cover the use of **generative AI**, commercial printing, reselling, agency work and more" — S16

This is the first evidence located in either probe that Synty operates a **paid tier that permits generative-AI use**. §5's escape-hatch note only found the NFT-&-Metaverse tier and the §5.4 Content-Creation-System route. It changes the posture of the T18 letter on the AI surfaces (§3 rows 4, 5(i), 5(ii)) from *"is this permitted?"* — where the answer for image→3D is a flat no under §1.4(b) — to *"what does the generative-AI custom tier cover and cost?"* Recommend adding that as a Tier-1 letter item; it converts a hard block into a priced option.

**Purchase-channel caveat.** SyntyPass returns "$10 USD per month back in Synty Store credit **which can be utilised on one time purchase licences**" (S16). Matt may therefore hold packs under **both** regimes — subscription-licensed library access *plus* OTP-licensed, perpetually-held packs bought with accrued credit. The two regimes differ on every question in this addendum. Worth Matt confirming whether any credit has been spent; if so, §6's OTP row and this §9 both apply, to different packs.

---

## §9.6 — Knowledge gaps not resolved (this pass)

- **No official statement, anywhere, on what happens to a published game after cancellation.** The FAQ's "SyntyPass Billing" section (S10) is billing-only — cancellation mechanics, minimum terms, refunds. Swept the full FAQ for post-cancellation licence guidance: nothing. The §9.1(a) verdict therefore rests on clause implication plus one line of marketing copy, with no interpretive layer behind it.
- **SyntyPass product-page Q&A accordions ("General" / "Team / Studio" tabs) are JS-rendered** and did not appear in static fetch. A human browser session could surface additional official Q&A. Expected yield low but non-zero — and the "Team / Studio" tab is the likeliest place a seat-counting or post-cancellation answer would live.
- **Subscription plan detail is deferred to the website by clause** ("Subscription Features… as set out on our website" — §14.1), meaning the licence's own terms are partly defined by an undated, mutable page. S16 has no version stamp. Pinned by retrieval date only.
- **Epic/FAB Content EULA (S15)** remains HTTP 403 to agent fetch — unchanged from §7, and irrelevant if SyntyPass is the sole channel.

---

## §9.7 — Addendum source list

All retrieved 2026-08-23, read-only, no authentication.

- **S2** Synty Standard Subscription Licence & EULA (current, last updated 9 July 2026) — https://syntystore.com/pages/standard-subscription-licence
- **S9** Synty Standard Subscription Licence, 3 June 2026 — https://syntystore.com/pages/standard-subscription-licence-june-3-2026
- **S17** Synty Standard Subscription Licence, 6 March 2025 — https://syntystore.com/pages/standard-subscription-licence-march-6-2025
- **S18** Synty Standard Subscription Licence, 11 September 2024 — https://syntystore.com/pages/archive-standard-subscription-licence-11-september-2024
- **S16** SyntyPass product page (pricing, seats, Flexible Terms, Custom Licence) — https://syntystore.com/products/syntypass
- **S1** Synty One-Time Purchase Licence & EULA (current, 9 July 2026) — https://syntystore.com/pages/one-time-purchase-licence *(re-retrieved for the perpetual/distribution contrast)*
- **S10** Synty FAQ — https://syntystore.com/community/faq
- **S11** Synty Licences Overview — https://syntystore.com/pages/licences-overview
- **S3** Synty EULA Versions History — https://syntystore.com/pages/eula-versions-history

**Method note.** All four subscription versions were stripped to plain text, whitespace-normalised with U+00A0→space (per the §1 method note — the same non-breaking-space trap applies to these pages), sliced to the licence body ("1. Our Services" → end of definitions) and machine-diffed pairwise. The three transitions in §9.2 are complete diffs, not samples: no changes exist outside the rows shown.

---

**Addendum filed by:** legolas (UNKNOWN-RESEARCHER), 2026-08-23. Evidentiary; research findings, not legal advice. Not committed — gandalf handles commit and curation.
