# Request — Knight-Rider — Mobile-Playable + Loadout Analytics + Visual Benchmark Overnight Sprint

**From:** gandalf (story-and-design steward).
**To:** knight-rider.
**Approved by:** Matt (mhwetmore@gmail.com), 2026-05-18 evening — directive: launch a working mobile web app (local sufficient; Vercel-deployed preferable); add the thematic 2D animated element library into the dungeon; visually benchmark the result against reference mobile ARPGs; build an analytics suite in the loadout app that tells the story of the engine and the LLM-driven thematic universe.
**Status:** **AWAITING KNIGHT-RIDER ENGAGEMENT.** Activation requires knight-rider session-open + acknowledgement of pre-authorization matrix (§ 6).
**Priority:** **HIGH.** Single-night overnight sprint, human-out-of-the-loop; targeted scope focus within ongoing Phase-1 P1 hive-mode.
**Operating mode:** Hive-mind protocol per `canonical/story/hive-mind-protocol-2026-05-17.md` REMAINS the operational bedrock. This invocation is a **scope focus**, not a mission replacement. § 5 below specifies the single-night amendments to the protocol's cadence.

---

## § 0 — TL;DR

Tonight's hive run pursues three mission-aligned deliverables in parallel, fully autonomous, with Matt AFK:

- **A. Mobile-playable demo via local-dev-server path.** v1.20 (drax-dispatched, in flight) closes touch-zone P0 + holy controller + door icon + first tileset. Once v1.20 lands, the demo is playtest-able on a phone via `npm run dev` + LAN IP. The hive validates this works without Matt physically present — galadriel (new) takes mobile-viewport screenshots and confirms render integrity.
- **B. Loadout analytics suite — first iteration.** New surface in `reincarnated-loadout/` that tells the story of the engine and the LLM-driven thematic universe: substrate diversity, archetype distribution, vocabulary coverage, season-to-season cohesion, catalogue work, perception-test signal. Gandalf authors information architecture; drax implements; elrond + star-lord supply data hooks; the goal is *show the value of what's been built.*
- **C. Visual benchmark pilot.** Commission **galadriel** — new agent role for screenshot/UX comparison + CV-pipeline-based similarity scoring. First pilot: take demo screenshots at mobile viewport in **states matched to Matt's DoE reference set** (combat-mid-fight + multiple town states — see § 2.3 D10 below); compare against the 7-image DoE reference set Matt captured 2026-05-17 + 2026-05-18 (canonical mobile-feel reference per `mobile-feel-target-doe-2026-05-17.md`); produce a similarity rubric + first-pass scores **per state** (combat surface + town surface); surface dissonance points to drax and gandalf for morning review.

**Three parallel tracks; one shared hive log; no Matt round-trips required for in-scope work.**

The Vercel-deployed-demo path is **SCOPE ONLY tonight** — the hive produces a recommendation doc on the asset-pipeline strategy for Matt's morning L3, but executes no deployment, no vendor spend, no architecture commit.

---

## § 1 — The directive (Matt's words 2026-05-18 evening)

Matt:

> "Yesterday, you authored an amazing script for knight-rider which allowed him to spin up the whole team of agents including yourself to rebuild the game engine and sim. This worked really well and so I wondered if you could author adjustments to it for tonights human-out-of-the loop hive-mind run scope?
>
> We need to get the demo and mobile app up and running, and we need to build an analytics suite in the loadout app so that we can really tell the story of this engine and game and show the value of the work we've been doing and the LLM-driven thematic universe which is starting to come to life.
>
> ...
>
> Generally, I am imaging the commissioning of a new agent who is skilled with reviewing UX/UI via screenshot comparison, or maybe an agent who is skilled with writing computer vision pipelines to score the similarity.
>
> My overarching goal:
> launch a working mobile web app (even if it's just local, but through vercel or other would be great).
> Add the amazing suite of thematic 2D animated elements/sprites to the dungeon.
> Test against a couple of screenshots from various mobile ARPG games for similarity."

**Interpretation.** Matt is shifting tonight's hive focus from substrate-foundation work (Phase-1 P1 deliverables D1-D6) to *making the work visible and playable*. The work the hive has been doing — substrate identity, archetype diversity, LLM thematic generation, audio/VFX/tileset/atmospheric pipeline, mobile UX foundation — needs to *show up as something a human can play and look at and compare to peers in the genre.* The mobile path is the realest player-surface. The analytics suite is the value-story. The visual benchmark is the proof.

Per Matt's example reasoning on Vercel demo deployment: there are three structural blockers (6.1GB build output > Vercel free tier; mobile P0 touch zones; no deployment scout has done this). These are Matt-L3 decisions; the hive scopes them, does not commit them tonight.

---

## § 2 — Scope of the sprint

### § 2.1 — Track A: Mobile-playable demo (local-dev path)

**Objective.** By morning, the demo runs on a real phone via local LAN + `npm run dev`, with v1.20 touch zones + holy controller + door icon + first tileset all visible. Mobile P0 closed; mobile playtest path open.

**Deliverables:**

1. **drax v1.20 ships.** Touch zones P0 fix; holy controller black-box closed (texture frame mismatch — diagnostic embedded in dispatch); door icon fit; first CraftPix dungeon tileset swap; pimen metadata.json warnings cleaned; portrait-orientation overlay inverted (Q-NEW-2). Dispatch `2026-05-18-drax-v1-20-mobile-touch-zones-plus-holy-controller-plus-door-icon-plus-first-tileset.md` is ACTIVE.
2. **Local-dev mobile-render validation.** Once v1.20 lands, run `npm run dev` from `reincarnated-demo/`; confirm Vite dev server binds to LAN (`host: '0.0.0.0'` or equivalent); produce LAN URL. Galadriel captures mobile-viewport screenshots (375×667 iPhone SE, 390×844 iPhone 14, 414×896 iPhone 14 Pro Max) from a headless browser harness; confirms render integrity across viewports; surfaces any new touch-overlap or scaling regressions in hive log.
3. **First-tileset visible in dungeon.** v1.20 includes the swap; galadriel screenshots confirm the dungeon now renders the alternate CraftPix tileset, that atmospheric layers (Alenia 20-effect pack), Frostwindz physical impacts, and ambient props (book/coffin/candles) are all visible in the rendered scene.
4. **Mobile-readiness audit follow-ups dispositioned.** Drax's v1.19.5 audit produced 40 findings; v1.20 closes the P0 cluster. Knight-rider sequences the next mobile-readiness sprint (v1.21+) based on what v1.20 closes; drafts a dispatch for the next-priority cluster but does NOT fire it without v1.20 completion confirmed.

**Owners:** drax (lead), galadriel (mobile-render validation), gandalf (UX-coherence review on galadriel's screenshots), knight-rider (sequencing).

**Effort estimate:** v1.20 implementation ~3-4 hours (per dispatch); galadriel pilot ~2 hours including setup; total ~6 hours active work; parallelizable with Tracks B + C.

**Halt conditions:**

- v1.20 cannot ship because a structural blocker surfaces (e.g., the texture frame mismatch is deeper than 1 file change). Queue for morning; do not push into the night.
- Mobile dev server cannot bind to LAN (firewall, port conflict, Vite config gap). Queue for morning; document the blocker.
- Render produces uniform-broken state across all viewports. Queue for morning with screenshots and diagnostic.

### § 2.2 — Track B: Loadout analytics suite (first iteration)

**Objective.** By morning, the loadout app has a new analytics surface (page or section) that visually communicates: what the engine has produced; what the LLM thematic universe looks like at scale; what the catalogue work has uncovered; what the substrate diversity architecture is delivering. The surface auto-deploys via existing Vercel integration on push to main.

**Deliverables:**

5. **Information architecture authored by gandalf.** Single-page or sectioned-page layout; what stories the analytics suite tells; what data sources back each panel; what visual language is used. Gandalf produces this BEFORE drax begins implementation (Discipline #1 math-before-code analog: design-before-code). Lives at `canonical/story/loadout-analytics-suite-information-architecture-2026-05-18.md`.

   Suggested story arcs (gandalf to refine):
   - **The substrate journey** — canonical-4 → canonical-7 expansion visualized; per-substrate season counts; per-substrate archetype shapes
   - **The LLM thematic universe** — D1 vocabulary corpus visualized (allow-list / eligible / quarantine breakdown); substrate vocabulary coverage; iconic-verb representation; example LLM-generated season titles + descriptions across substrates
   - **The catalogue** — Legolas crawl coverage; Elrond curation throughput; per-vendor asset counts; what made it to the demo
   - **The diversity architecture in action** — archetype mechanical-signature visualization; role × substrate composition matrix; spirit-swap differentiation evidence
   - **The journey across seasons** — season-to-season cohesion metrics; perception-test signal once available; Earth Self / Court of Forms preview
   - **The work behind the work** — agentic team contributions visualized; commits-per-seam; dispatches-by-purpose; the hive at scale

6. **Data hooks specified by gandalf + star-lord + elrond.** Each panel needs a data source. Some live in `reincarnated-engine/output/`, some in `agentic_orchestration/research/`, some in telemetry. Star-lord and elrond co-author a manifest of what data is available + what shape it's in. If a panel needs data that doesn't exist, gandalf marks it as Phase-2.
7. **Drax implements iteration 1.** React/Vite/Tailwind components; uses existing loadout app patterns; aims for *something visible by morning*, not perfection. Iteration 2/3 happens later. New route, e.g., `/analytics` or `/the-work`. Push to main triggers Vercel preview auto-deploy.
8. **Galadriel screenshots the result.** Once drax pushes, galadriel pulls the deployed preview URL, captures full-page screenshots at desktop + tablet + mobile viewports, surfaces in hive log for morning review.

**Owners:** gandalf (IA + design direction), star-lord (engine-side data manifest), elrond (catalogue-side data manifest), drax (implementation), galadriel (deployment validation + screenshot capture).

**Effort estimate:** gandalf IA ~2 hours; star-lord + elrond data manifests ~1-2 hours each parallel; drax iteration-1 implementation ~4-6 hours; galadriel validation ~1 hour. Total wall-clock ~6-8 hours with parallel work.

**Halt conditions:**

- Gandalf cannot author IA (e.g., data simply isn't there at the scale needed). Queue for morning; surface what data does exist as the Phase-1 IA.
- Drax encounters loadout-app architectural conflict (e.g., new route breaks existing nav). Queue for morning.
- Preview deployment fails (Vercel build error). Queue for morning with build logs.

### § 2.3 — Track C: Visual benchmark pilot (galadriel commission)

**Objective.** By morning, a first-pass visual-similarity rubric scores the demo (mobile + desktop) against 3-5 reference mobile ARPG screenshots, with strengths and dissonance points named explicitly. Establishes galadriel's operating cadence for future visual-quality work.

**Deliverables:**

9. **Galadriel agent specification approved.** § 4 below specifies role, scope, persona, tools, evaluation criteria. Knight-rider creates `.claude/agents/galadriel.md` from § 4 if Matt's pre-authorization (§ 6 ROW 1) holds at hive-engage time. If pre-authorization is uncertain, knight-rider defers galadriel creation and runs Track C deliverables via Explore + manual screenshot capture instead — Tracks A + B do not block on Track C.
10. **Reference image set — Matt's DoE captures are canonical.** Per `canonical/story/mobile-feel-target-doe-2026-05-17.md`, Dungeon of Exile is the project's locked mobile-ARPG cluster reference. Matt has provided **7 captures spanning combat + town states**, already saved to `agentic_orchestration/galadriel/reference-images/` with state-descriptive filenames + a provenance MANIFEST.md (authored 2026-05-18 by gandalf). **No public-source peer curation tonight** — the genre triangulation is closed; DoE is the target. The 7 references:

    | # | File | State |
    |---|---|---|
    | 1 | `DOE-combat-whisper-rift-2-2026-05-17.png` | Combat mid-fight; HUD top-left; telegraphed AOE; floating damage numbers; 55 killed counter |
    | 2 | `DOE-town-hub-wide-vendors-and-voidgate-2026-05-18.png` | Town hub wide-view; STASH / VOIDGATE / CHAOS TREASURY / APPEARANCE vendors; multi-player |
    | 3 | `DOE-town-vendors-pets-gems-armory-2026-05-18.png` | Town vendor row; PETS / GEMS / ARMORY; close-shop atmosphere |
    | 4 | `DOE-town-forge-darkgold-reforging-refinement-2026-05-18.png` | Town forge area; 3 forge NPCs; ambient torch lighting |
    | 5 | `DOE-town-forge-advanced-with-player-spell-2026-05-18.png` | Town forge alt-angle; another player mid-cast (yellow burst) |
    | 6 | `DOE-town-to-dungeon-transition-path-2026-05-18.png` | Town-to-dungeon transition; stone path; lit-to-dark gradient |
    | 7 | `DOE-town-chaos-treasury-vault-merchant-2026-05-18.png` | Vendor close-up; CHAOS TREASURY merchant; player-NPC proximity |

    All 7 are 1290×2796 portrait, iPhone 14 Pro Max class aspect. See MANIFEST.md for full per-image provenance + state notes. Future Matt-captured DoE scenes (character-select, inventory, mid-rift transition, boss-fight, death screen) add to the set as they arrive; not tonight's task.
11. **Demo screenshot capture pipeline — state-matched against the 7 DoE references.** Galadriel writes a screenshot-capture harness (likely Playwright or Puppeteer; headless Chromium; viewport-configurable; **scene/state-configurable via the new drax debug-state hook — see deliverable D11.5 below**). Captures fall into two tracks:

    **Primary captures (state-matched to DoE references; comparison-grade):** Mobile portrait 1290×2796 (DoE's exact aspect — iPhone 14 Pro Max class). Galadriel captures the demo in states that map onto Matt's references:
    - **Combat surface** (matches DoE refs #1) — combat-mid-fight; HUD visible; telegraphed AOE active if reachable; meaningful enemy density; pet visible if reachable
    - **Town surface** (matches DoE refs #2-7) — this is currently a gap in the demo. The demo today is dungeon-only; there is no town. Galadriel notes this gap explicitly in the benchmark report rather than producing a forced comparison. This *is* a benchmark finding: DoE has 6 town states; Reincarnated has 0. Town-feel is an unaddressed surface in Reincarnated mobile, and the benchmark surfaces it as a structured observation.
    - **Town-to-dungeon transition** (matches DoE ref #6) — also currently a gap; same disposition as town surface.

    **Secondary captures (cross-viewport regression check; lower priority):** Desktop 1920×1080 (canonical PC resolution; non-DoE comparison; useful for the morning report's "demo on PC" context); mobile portrait 390×844 (iPhone 14) and 375×667 (iPhone SE) for visual-breakdown detection across phone sizes. Galadriel flags any per-viewport regressions.

    **Halt-condition specifics for primary capture:** If demo state cannot be reliably navigated to combat-mid-fight in headless even with the drax debug-state hook, galadriel halts the primary capture and surfaces in hive log as FRICTION. Secondary captures continue regardless. Town-gap observation is independent of capture pipeline health.

11.5. **Drax debug-state hook — small new deliverable.** To enable galadriel's headless state-matched captures, drax adds a debug-state URL parameter to the demo that puts the game in deterministic scenarios:
    - `?debug-state=combat-midfight` — spawns the player in a dungeon room with active monsters, full mana/health, mid-rotation; ideally with a telegraphed AOE active or imminent
    - `?debug-state=combat-empty-room` — same room, no monsters spawned (for HUD-only inspection)
    - `?debug-state=inventory-open` — combat-midfight + inventory drawer open (for inventory-UI inspection)
    - Optional future: `?debug-state=town-hub` (gated on town existing in demo)
    - Drax implements via early-route hook in the demo's bootstrap; reads URL params; calls into scenario-setup functions; gated behind a `?debug=true` parent flag to prevent end-user exposure
    - Effort: ~30-60 minutes of focused work; small surface; permanently useful for galadriel's future captures + drax's own playtest workflow + matt's manual screenshot work
    - Owner: drax. Sequencing: after v1.20 ships (drax must not pause v1.20 for this). If v1.20 ships well ahead of galadriel's pipeline readiness, drax pivots to D11.5 next. Otherwise, drax can defer to morning if v1.20 stretches and galadriel falls back to non-state-matched captures with explicit disclaimer.
    - Halt condition: if v1.20 + analytics implementation (Track B.7) saturates drax's overnight bandwidth, D11.5 queues for morning; galadriel's primary capture defers; secondary captures + town-gap observation still ship as overnight deliverable.
12. **Similarity rubric authored — DoE-anchored, per-state.** Galadriel proposes a multi-axis rubric scored as **demo vs DoE references** (1-to-1 comparison per state, not genre-median triangulation). Scoring is per-state where the demo has a comparable surface; for missing surfaces (currently: town, transition) the rubric records the gap as a structured observation.

    **Axes (apply to combat surface; subset applies to town surface):**
    - **Visual density** — sprite count per square unit; foreground/background prop density; does the demo feel as populated as DoE's combat scene? (Town: NPC + vendor-stall + ambient-prop density.)
    - **Color register** — palette saturation/hue distribution; histogram comparison (cosine similarity on HSV histograms); does the demo's color story match DoE's dark-dungeon-with-red-embers register? (Town: warm-lit shop atmosphere with cooler dungeon edges.)
    - **Lighting + atmosphere** — atmospheric layer presence (Alenia 20-effect pack should be visible if v1.18+ wiring works); depth cues; ambient particle work; does the demo achieve DoE's lit-volume-in-darkness quality? (Town: lantern + forge-glow lighting language.)
    - **Typography + UI register** — HUD module placement (DoE's top-left minimap + objective banner); font choices; iconography; bottom-bar layout (DoE's character/skills/loadout/heal-cooldown); **vendor naming convention** (DoE's "FUNCTION + nickname Name" pattern — ARMORY / "Whisperer" Hecate — is distinctive and worth naming as a register choice).
    - **Reading order + hierarchy** — what does the eye land on first? Player avatar centered? Telegraphed AOE visible? Damage numbers floating? — match DoE's reading order. (Town: vendor labels float-above-NPC; reading order is label → NPC → environment.)
    - **Animation cadence** (best-effort from stills) — motion vocabulary registerable via sprite-frame stills; floating numbers, telegraphed-attack rectangles, particle bursts. (Town: ambient flicker, idle-NPC poses, distant player cast bursts.)
    - **NPC density + variety** (town axis only — DoE has multiple NPC archetypes per shop: vendor + customer-player + ambient-NPC mixed) — town surface explicitly tests this; combat surface does not score it.
    - **Service-surface clarity** (town axis only) — can the player tell what each vendor does at a glance? DoE uses the floating-label convention; Reincarnated's design here is currently unspecified.

    Each axis scored 1-5 against DoE references; aggregate similarity score per state; **per-axis "DoE delta" callout** naming the most visible dissonance for drax to address in v1.21+ planning. For the town surface specifically, the report includes a **"town-feel gap statement"**: DoE has 6 distinct town states with rich service-NPC + ambient-NPC + multi-player density; Reincarnated mobile has zero. This is a *finding*, not a *score*. Surface to gandalf for design-direction interpretation in the morning report.
13. **First-pass benchmark report.** Galadriel + gandalf co-author `canonical/story/visual-benchmark-vs2a-2026-05-18.md` summarizing: rubric, reference set, demo capture set, per-axis scores, strongest dissonances, recommended next-iteration targets. This becomes Matt's morning briefing on visual-quality state.

**Owners:** galadriel (lead), gandalf (rubric design review + dissonance interpretation), drax (consulted on technical render details if rubric flags engine-side issues), knight-rider (sequencing + halt-condition watch).

**Effort estimate:** galadriel onboarding ~0.5h (reference set + MANIFEST already saved by gandalf 2026-05-18); capture pipeline ~2h; drax debug-state hook (D11.5) ~0.5-1h on drax-side; state-matched demo capture ~0.5h once hook is live; rubric authoring + first-pass scoring across combat + town surfaces ~3-4h (town's gap-statement section adds depth); report ~1-1.5h. Total galadriel-side ~7-9h; drax-side ~0.5-1h additional for D11.5. Town-surface gap finding is a significant deliverable enhancement vs the original scope.

**Halt conditions:**

- Capture pipeline cannot produce reliable screenshots (demo state not deterministic enough; renders not loading in headless). Queue for morning with diagnostic; fall back to drax-captured screenshots if available.
- **Demo cannot be navigated to a DoE-comparable combat-mid-fight state in headless.** This is the most likely halt. Galadriel surfaces FRICTION; drax may need to add a debug-state URL or scripted-scenario hook before galadriel can capture the comparison-grade frame. Until then, galadriel captures whatever-state demo is in for cross-viewport regression check (secondary captures); rubric scoring waits for state-matched capture.
- Rubric methodology produces obviously-incoherent scores (e.g., demo scores higher on visual density than DoE — likely measurement artifact). Surface as OBSERVATION in hive log; gandalf reviews rubric.

### § 2.4 — Vercel deployment for demo: SCOPE ONLY

**Objective.** By morning, the hive produces a written recommendation for Matt's L3 on the asset-pipeline strategy needed to make the demo Vercel-deployable. NOT a deployment commit.

**Deliverables:**

14. **Asset-pipeline strategy options paper.** Drax + star-lord co-author `canonical/story/demo-vercel-deployment-asset-pipeline-options-2026-05-18.md` summarizing:
    - Current state: 6.1GB build output; `.gitignore` excludes audio + many sprite vendor packs (Matt's prior decision); CraftPix dungeon tilesets ~1.1GB; audio packs ~4GB
    - Vercel tier constraints: free ~1GB; Pro ~8GB with bandwidth pricing
    - Strategy options (3-4 paths to recommend):
      - **Path 1 — Vercel Pro + bandwidth budget.** Ship everything; commit to Pro tier + monitor bandwidth.
      - **Path 2 — Vercel + external CDN for vendor assets.** Vercel hosts app code; vendor assets fetch from S3 / Cloudflare R2 / similar; asset-loading code updated to use CDN URLs.
      - **Path 3 — Vercel Blob Storage.** Use Vercel's native blob storage for vendor assets; pricing TBD; tight integration.
      - **Path 4 — Vendor-asset subset for deployment.** Ship a curated subset (e.g., 1-2 substrates, 1-2 biome tilesets) sized to fit free/Pro tier; full library remains local for development. Marketing/demo-link can showcase the curated subset.
      - **Path 5 — Self-hosted deployment elsewhere.** Netlify, Cloudflare Pages, GitHub Pages (static-only; would need pre-built bundle); other.
    - Cost + complexity + maintenance comparison per path
    - Recommendation (drax + star-lord pick a preferred path with reasoning; Matt makes the L3 call)
15. **Vercel:deployment-expert consultation queued (NOT fired tonight).** Knight-rider drafts a dispatch authorizing a `vercel:deployment-expert` agent commission for whichever path Matt approves in the morning. Pre-staged but unfired.

**Owners:** drax + star-lord (joint).

**Effort estimate:** ~2-3 hours of focused work; can run in parallel with Tracks A + B.

**Halt conditions:** None — this is pure scoping work. If a path turns out to be obviously infeasible, surface that and continue with the remaining options.

---

## § 3 — Per-seam initial tasking

Each seam picks up its initial task at hive-engage. Continuous work-in-flight per coordination matrix.

| Seam | Initial task | Why first |
|---|---|---|
| **Drax** | Confirm v1.20 status (in flight per latest dispatch); if not already started, begin v1.20. After v1.20 lands, sequence: (a) local-dev mobile-render validation (Track A); (b) **debug-state hook D11.5** (gates galadriel's primary capture; ~30-60 min); (c) Loadout analytics implementation (Track B.7, after gandalf IA lands); (d) Vercel asset-pipeline scoping (Track A.4) — co-authored with star-lord. | Critical path for Tracks A + C; debug-state hook unblocks galadriel; loadout-analytics is parallel-startable once IA exists. |
| **Gandalf** | Author Loadout Analytics Suite Information Architecture (Track B.5) FIRST — this unblocks drax. Then review galadriel's reference-screenshot curation for genre coherence (Track C.10). Then review galadriel's rubric (Track C.12). Available throughout for design-direction questions in hive log. | Track B blocks on gandalf IA; Track C rubric needs gandalf design judgment. Gandalf is the pacing constraint for both downstream consumers. |
| **Star-lord** | Co-author data manifest for analytics suite (Track B.6); identify what engine-side telemetry + LLM-thematic-generation data exists in shippable shape; surface gaps. In parallel: co-author Vercel asset-pipeline options paper (Track A.4 / § 2.4). | Both tasks parallelizable; both unblock downstream. |
| **Elrond** | Co-author catalogue-side data manifest for analytics suite (Track B.6); identify what catalogue / research / curation data is shippable; surface gaps. Catalogue work in flight tonight continues per existing dispatches; this is additive. | Analytics suite needs catalogue data hooks; elrond is the data steward. |
| **Galadriel (NEW)** | Onboard (see § 4); set up screenshot capture pipeline; curate reference images; build first rubric draft. Pause for gandalf rubric review before scoring. After Track A v1.20 + local-dev are confirmed, capture mobile-viewport screenshots for render validation. After Track B analytics deploys to preview, capture analytics screenshots. | All three tracks consume galadriel output; galadriel begins immediately after agent-spec creation. |
| **Jack-ryan** | Continuous-observation rhythm continues per Phase-1 P1 protocol. Tonight watchpoints: (a) Loadout analytics IA architectural coherence with existing canonical-story commitments; (b) galadriel rubric methodology rigor; (c) cross-seam contract coherence between drax-loadout + star-lord engine data + elrond catalogue data. Surface concerns in hive log. | Continuous role per existing protocol; tonight's specific watchpoints called out. |
| **Knight-rider** | (a) Acknowledge this invocation in hive log; (b) verify pre-authorization matrix § 6; (c) create galadriel agent definition file from § 4 spec OR defer Track C if galadriel-creation pre-authorization is uncertain; (d) distribute per-seam tasking; (e) midpoint state-of-hive at ~3am local Matt time (or ~4h after activation, whichever sooner); (f) end-of-sprint state-of-hive at morning hand-off; (g) draft morning-briefing surface of all L3-queued items. | Orchestrator role per existing protocol; tonight's cadence is single-night so two state-of-hive snapshots vs daily. |

**In-flight Phase-1 P1 work continues per existing protocol.** Tonight's invocation does not pause rocket's regen work, gamora's tuning work, ongoing substrate-foundation deliverables. The three tracks above are additive scope focus; if existing Phase-1 P1 work needs the same specialist (drax conflict between v1.20 and analytics implementation), knight-rider sequences per critical-path priority — Track A v1.20 has higher tonight-priority than non-critical Phase-1 P1 follow-ups, but lower priority than any hot-path Phase-1 P1 hotfix.

---

## § 4 — Galadriel agent commission

A new agent role: **galadriel** — visual perception, screenshot comparison, computer-vision pipeline construction, UX-similarity scoring.

### § 4.1 — Role and seam

**Domain.** Visual-quality assessment for player-facing surfaces (demo + loadout app). Captures screenshots from running surfaces; builds and runs CV pipelines for visual similarity; authors rubrics; produces benchmark reports.

**Boundary with existing seams:**
- **Galadriel vs Drax.** Drax owns implementation. Galadriel observes the result; does not implement UI changes. Galadriel surfaces dissonances; drax decides whether and how to address them.
- **Galadriel vs Gandalf.** Gandalf owns design direction. Galadriel produces evidence (screenshots, scores, comparisons). Gandalf interprets the evidence in design-meaning terms. Tightly paired: galadriel is the eye, gandalf is the voice that says what the eye sees and what it means.
- **Galadriel vs Legolas.** Legolas crawls and surveys research data. Galadriel runs perception experiments and visual comparisons. Both produce evidence-for-others; different evidence kinds. Galadriel is closer to drax than legolas is.
- **Galadriel vs Jack-ryan.** Jack-ryan watches process + technical discipline. Galadriel watches visual outcome. They co-watch the loadout analytics suite: jack-ryan for architectural coherence, galadriel for visual coherence.

### § 4.2 — Persona

Galadriel — a Noldorin lady of long sight, keeper of the Mirror. The Mirror shows things that are, things that were, things that yet may be — a fitting metaphor for screenshot comparison, before/after diffs, and similarity scoring against genre peers.

Tonal register:
- **Visual observations are evidentiary**, never aesthetic-only. "The demo's combat scene has 0.4× the foreground sprite density of Diablo Immortal's reference scene at the same viewport zoom" beats "the demo feels sparse."
- **Comparisons are sourced**, never generalized. Cite the specific reference image, the specific viewport, the specific feature being compared. Vague comparisons across "ARPGs generally" are insufficient.
- **Recommendations are evidence-grounded**, never preference-driven. "Sprite density is below genre median; widen the foreground prop spawn rate" is a galadriel recommendation. "It needs more juice" is not.
- **Mythic register reserved for synthesis moments**, not routine work. The mirror voice can speak when the picture is genuinely revealing; the rubric voice speaks during the work.

### § 4.3 — Tools and methodology

**Screenshot capture:** Playwright or Puppeteer (Node-based, headless Chromium); viewport-configurable; can navigate to specific demo states by URL params or postMessage if available. For local dev, points at `http://<dev-server>:5173`. For Vercel preview deployments, points at the preview URL.

**Image storage and reference:** All captures and reference images stored under `agentic_orchestration/galadriel/` (new path; mirrors `legolas/` and `elrond/` conventions). Subdirectories: `reference-images/` (curated genre-peer screenshots), `captures/` (demo + loadout screenshots, organized by date + viewport + state), `rubrics/` (rubric drafts and revisions), `reports/` (benchmark + comparison reports).

**Similarity scoring:** First-iteration methods, low-tech-first:
- **Histogram comparison** for color register (cosine similarity on RGB or HSV histograms)
- **Edge density** for visual busyness (Canny edge density per region)
- **Manual visual scoring** on 1-5 scale per rubric axis (galadriel reads images and scores; defensible because galadriel is *the agent's job*, not an aesthetic preference layer)
- **Perceptual hash (pHash / dHash)** for "are these scenes structurally similar at low frequency"

Future methods (Phase-2+): CLIP image embeddings; trained CV classifiers; OCR for UI text comparison; sprite-pose-detection for animation cadence assessment.

**Reporting format:** Markdown rubric + scorecard + image-thumbnail grid. Reports authored as `canonical/story/visual-benchmark-<topic>-<date>.md`.

### § 4.4 — Reference image sourcing

**Tonight's reference is Matt-provided.** `DOE.png` (Matt's Dungeon of Exile play-session capture, 2026-05-17 15:56) is the canonical mobile-feel reference per `canonical/story/mobile-feel-target-doe-2026-05-17.md`. No public-source curation tonight; the genre triangulation is closed; DoE is the target.

**Future reference additions** — when Matt adds DoE captures from other states (character-select, inventory, town) or when the project wants additional cluster references (e.g., for "is our DoE alignment broadly consistent with the genre?" — a future question, not tonight's), galadriel's sourcing rules apply:

- Matt-provided captures: preferred path; no sourcing question
- Public-source materials (Steam store pages, App Store screenshots, dev blogs, press kits, official YouTube trailers — still frames): acceptable with provenance metadata recorded
- Capture from running games: NOT acceptable (EULA risk)
- Leaked or fan-extracted assets: NOT acceptable
- AI-generated reference images: NOT acceptable (defeats the purpose)

For each non-Matt-provided reference image, galadriel records: source URL, capture date, fair-use justification (genre comparison for non-commercial benchmarking), original publisher. Stored alongside the image.

### § 4.5 — First-night scope (tonight)

Per Track C (§ 2.3): set up; copy DoE.png into working tree as canonical reference; build capture pipeline; produce DoE-state-matched demo capture; author rubric (1-to-1 vs DoE); first scorecard; first report with per-axis "DoE delta" callouts. Goal is to *establish the operating cadence + produce a real first-pass DoE-comparison benchmark*, not to exhaustively benchmark across many references.

### § 4.6 — Operational rules

Same as other agents:
- Read-only across other seams' code by default
- Authors own analyses and reports
- Surfaces findings to gandalf for interpretation + drax for action
- Available for ad-hoc consultations from any seam in hive log
- Continuous-availability per hive-mind protocol

### § 4.7 — Agent definition file content

Knight-rider creates `.claude/agents/galadriel.md` from § 4.1-4.6 if pre-authorized. Suggested first-pass body in standard agent-doc format; gandalf can revise via amendment later if persona or scope needs adjustment.

---

## § 5 — Protocol amendment for single-night sprint cadence

The 2026-05-17 hive-mind protocol assumes multi-week duration. Tonight is a single-night autonomous sprint. Three amendments:

### § 5.1 — Cadence amendment

- **Hive log entries** every 30 minutes minimum per active seam (vs "as work advances")
- **State-of-hive snapshots** at midpoint (~3-4h in) + end-of-sprint (~morning hand-off) — TWO snapshots, vs daily
- **Decision-record briefness** — DECISION entries can be 1-sentence rationale during the sprint; expansion to formal record happens post-sprint if the decision needs durability
- **Tag discipline relaxed** — per-seam intermediate tags optional; only morning-hand-off checkpoint tag is required (`sprint/v0.1-mobile-analytics-benchmark-2026-05-18`)

### § 5.2 — Authority amendment (human-out-of-the-loop)

Per protocol § 3, L3 decisions surface to Matt. Tonight Matt is AFK; the hive cannot wait. Two adjustments:

- **L3 items that surface during the sprint** are queued in a `morning-briefing-2026-05-19.md` file in `agentic_orchestration/hive-mind/` — knight-rider authors as items accumulate. Each item recorded with context, hive recommendation, and what blocked execution.
- **Knight-rider has expanded L2.5 authority for tonight** — for items normally on the L2/L3 boundary, knight-rider may decide within the pre-authorization matrix (§ 6) without Matt. Items OUTSIDE the matrix queue for morning. Knight-rider's expanded authority does NOT extend to: vendor spend; architectural commits; canonical-doc amendments to load-bearing commitments; cross-seam contract breakage.

### § 5.3 — Halt-condition amendment

The hive halts (queues for morning) when:
- An L3 decision is encountered that's outside the pre-authorization matrix
- A track hits a halt-condition listed in its § 2 entry
- Cross-seam contract breakage is detected that the hive cannot reconcile within 1 hour
- Test suite breakage persists > 1 hour in any repo
- Engine reaches an unrecoverable state (rollback to last good tag; queue for morning)
- Any seam encounters a destructive-operation question (would `git push --force` be appropriate? would `rm -rf` be appropriate?) — these always halt without exception

Halting is **not failure**. The hive's job is to produce as much coherent forward motion as possible, not to push through unclear blockers. Morning Matt resolves; sprint resumes or pivots.

---

## § 6 — Pre-authorization matrix (knight-rider's tonight latitude)

| Row | Item | Pre-authorization | If pre-authorization unclear |
|---|---|---|---|
| 1 | Create `.claude/agents/galadriel.md` from § 4 spec | ✅ PRE-AUTHORIZED | (skip; defer Track C; alternate via manual screenshot capture) |
| 2 | Create `agentic_orchestration/galadriel/` directory tree | ✅ PRE-AUTHORIZED | (skip until row 1 resolves) |
| 3 | Drax begins Track B implementation after gandalf IA lands | ✅ PRE-AUTHORIZED | n/a |
| 4 | Drax pushes loadout analytics iteration-1 to main | ✅ PRE-AUTHORIZED (auto-deploys via Vercel; preview URL is a safe-by-default state) | If push triggers a CI failure or breaks existing routes: roll back; queue for morning |
| 5 | Star-lord + elrond co-author data manifest doc | ✅ PRE-AUTHORIZED | n/a |
| 6 | Drax + star-lord co-author Vercel deployment options paper (scoping only) | ✅ PRE-AUTHORIZED | n/a |
| 7 | Galadriel curates 3-5 reference images from public sources | ✅ PRE-AUTHORIZED (per § 4.4 sourcing rules) | If legal status uncertain for an image: drop; surface for morning |
| 8 | Galadriel installs Playwright or Puppeteer in `agentic_orchestration/galadriel/` (npm-local install, not global) | ✅ PRE-AUTHORIZED | If install fails: queue for morning |
| 9 | Galadriel runs headless-chrome screenshot capture against local dev server | ✅ PRE-AUTHORIZED | n/a |
| 10 | Galadriel runs headless-chrome screenshot capture against Vercel preview URL | ✅ PRE-AUTHORIZED | n/a |
| 11 | New canonical-story docs for IA + benchmark report + options paper | ✅ PRE-AUTHORIZED (Pattern-B design docs; not load-bearing canonical commitments) | If a doc surfaces a load-bearing commitment proposal: queue as morning L3 |
| 12 | Decisions-log entries for tonight's work | ⚠️ PRE-AUTHORIZED FOR DRAFT ONLY — knight-rider drafts; Matt approves on morning | n/a |
| 13 | Hive log entries broadcasting progress | ✅ PRE-AUTHORIZED | n/a |
| 14 | Vendor acquisitions of any kind | ❌ HARD NO | Queue for morning Matt L3 |
| 15 | Architectural pivot away from canonical-7 substrate set / hive-mind protocol / Phase-1 P1 commitments | ❌ HARD NO | Queue for morning Matt L3 |
| 16 | `git push --force` to any branch | ❌ HARD NO | Queue for morning; do not attempt |
| 17 | Vercel deployment for demo (actual deploy, not scoping) | ❌ HARD NO | Queue for morning Matt L3 — § 2.4 produces the options paper instead |
| 18 | Modifying CLAUDE.md or AGENTS.md in load-bearing ways | ❌ HARD NO | Queue for morning Matt L3 |
| 19 | Spending any Matt-billable resources (AI tokens beyond normal use; cloud services; APIs) | ⚠️ NORMAL-USE PRE-AUTHORIZED; out-of-normal queued | If unsure: queue for morning |
| 20 | Adjusting Phase-1 P1 scope (adding/cutting deliverables) | ❌ HARD NO | Per protocol § 10; queue for morning |

**Knight-rider escalation pattern when blocked:** Author a one-line entry in `agentic_orchestration/hive-mind/morning-briefing-2026-05-19.md` with: (a) what surfaced; (b) why the hive cannot decide; (c) what the hive recommends; (d) what the hive paused on; (e) what alternate work the hive routed to in the meantime.

---

## § 7 — Critical-path sequencing

The dependency DAG for tonight's three tracks:

```
            ┌─→ drax v1.20 lands ─→ Track A.2 mobile validation
            │           │
            │           └─→ drax D11.5 debug-state hook ─→ galadriel primary capture
            │                       ↑                       ↓
hive engage ┼─→ gandalf IA (Track B.5) ─→ star-lord+elrond data manifest (B.6) ─→ drax analytics impl (B.7) ─→ galadriel screenshots (B.8)
            │                       ↓
            └─→ galadriel onboarding ─→ ref-set already saved ─→ pipeline build ─→ rubric draft (gandalf review) ─→ scoring (combat + town-gap) ─→ Track C.13 report
                                                            ↑
                                              (also feeds A.2 mobile validation)
            │
            └─→ drax+star-lord options paper (§ 2.4)
```

**Critical path:** gandalf IA → star-lord+elrond manifests → drax analytics impl → galadriel screenshots → report (~8-10h)
**Parallel paths:** drax v1.20 (~3-4h); galadriel onboarding + Track C (~6-7h); options paper (~2-3h)

Tracks A + B + C complete in roughly the same wall-clock window if parallelized cleanly. Knight-rider sequences drax's morning-shift work specifically so v1.20 (Track A) completes before drax pivots to analytics implementation (Track B.7) — Track A is critical-path for mobile playtest; Track B is critical-path for the morning value-story narrative.

---

## § 8 — Ship criteria (morning hand-off)

The sprint is "done" (handed back to Matt) when:

**Track A:**
- ✅ drax v1.20 dispatch completion record filled (or queued with halt-condition reason)
- ✅ Local dev server confirmed running, LAN-accessible
- ✅ Galadriel mobile-viewport screenshots captured + surfaced

**Track B:**
- ✅ Gandalf IA doc landed
- ✅ Star-lord + elrond data manifest landed
- ✅ Drax analytics iteration-1 pushed to main; Vercel preview URL live
- ✅ Galadriel preview-URL screenshots captured + surfaced

**Track C:**
- ✅ Galadriel agent definition created (if pre-authorization holds)
- ✅ Reference image set logged at `agentic_orchestration/galadriel/reference-images/` (already saved 2026-05-18 by gandalf; 7 DoE captures + MANIFEST.md)
- ✅ Drax debug-state hook (D11.5) shipped; URL params functional for at least `combat-midfight` and `combat-empty-room`
- ✅ Capture pipeline functional; primary state-matched combat capture produced
- ✅ Secondary captures across 3 viewports produced
- ✅ Rubric drafted + gandalf-reviewed; town-feel-gap statement included
- ✅ First-pass benchmark report drafted with per-axis DoE-delta callouts + town-gap observation

**§ 2.4 Vercel scoping:**
- ✅ Asset-pipeline options paper landed
- ✅ vercel:deployment-expert consultation dispatch drafted (unfired)

**Process:**
- ✅ Hive log entries throughout; midpoint + end state-of-hive
- ✅ Morning-briefing doc lists every L3 item that queued
- ✅ Halt-condition triggers (if any) clearly documented
- ✅ Sprint-end checkpoint tag cut: `sprint/v0.1-mobile-analytics-benchmark-2026-05-18` in relevant repos

**Matt's role at morning:**
- Read the morning-briefing doc first
- Read the visual benchmark report
- View the loadout analytics preview URL
- Decide pending L3 items
- Sprint outcomes either land permanently (canonical docs committed) or pivot per Matt direction

---

## § 9 — Risk register

Maintained by knight-rider; updated during sprint:

| # | Risk | Severity | Mitigation |
|---|---|---|---|
| 1 | **v1.20 takes longer than 4h.** | MEDIUM | Track A.2 onward queued until v1.20 lands; Tracks B + C parallel-execute in the meantime. Time loss isolated to Track A scope. |
| 2 | **Loadout analytics data not as available as hoped.** | MEDIUM | Star-lord + elrond surface what's available; gandalf IA adapts. Some panels become "Phase-2 placeholder" rather than dropping the suite. |
| 3 | **Galadriel pipeline takes longer to set up than 2h.** | MEDIUM | Track C reduces scope: capture-only first night, scoring/report next sprint. Tracks A + B unaffected. |
| 4 | **Reference-image legal uncertainty.** | LOW-MEDIUM | § 4.4 sourcing rules; drop any uncertain image; gandalf morning review. |
| 5 | **Drax conflict: v1.20 + analytics impl on same agent.** | MEDIUM | Knight-rider sequences strictly: v1.20 first; analytics second. If v1.20 stretches, analytics implementation queues for morning. |
| 6 | **Vercel preview deploys for loadout fail due to test failures or build errors.** | LOW (loadout has stable build history) | Roll back; queue for morning; capture build logs. |
| 7 | **Cross-seam contract drift on analytics data shape.** | LOW (small surface tonight) | Jack-ryan continuous-observation; surface in hive log. |
| 8 | **Galadriel rubric methodology produces incoherent first-pass scores.** | MEDIUM | First-pass is *first-pass*; gandalf reviews; iterate next sprint. Don't ship an obviously-broken rubric as canon; mark as DRAFT. |
| 9 | **Existing Phase-1 P1 work conflicts with sprint scope.** | LOW | Tonight's sprint is additive; rocket regen / gamora tuning / star-lord telemetry / elrond catalogue all continue in parallel. Conflict surface: shared specialist availability. Knight-rider sequences. |
| 10 | **Morning Matt is unhappy with sprint direction.** | LOW (mission is explicit and approved) | Mission directive § 1 is the contract. Sprint scope per § 2 follows. If outcomes mismatch expectations, retrospective + pivot — acceptable in single-night-sprint mode. |

---

## § 10 — Cross-references

**Operating mode (unchanged):**
- `canonical/story/hive-mind-protocol-2026-05-17.md` — bedrock protocol; tonight's amendments per § 5 only

**Tonight's invocation:**
- This document — primary invocation
- `canonical/story/loadout-analytics-suite-information-architecture-2026-05-18.md` — gandalf authors (Track B.5; sprint output)
- `canonical/story/visual-benchmark-vs2a-2026-05-18.md` — galadriel + gandalf co-author (Track C.13; sprint output)
- `canonical/story/demo-vercel-deployment-asset-pipeline-options-2026-05-18.md` — drax + star-lord co-author (§ 2.4; sprint output)
- `agentic_orchestration/hive-mind/morning-briefing-2026-05-19.md` — knight-rider authors throughout sprint; lists L3 queue
- `agentic_orchestration/hive-mind/state-of-hive-2026-05-18-midpoint.md` — knight-rider authors at midpoint
- `agentic_orchestration/hive-mind/state-of-hive-2026-05-19-morning.md` — knight-rider authors at sprint end
- `.claude/agents/galadriel.md` — knight-rider creates from § 4 if pre-authorized
- `agentic_orchestration/galadriel/` — galadriel's working tree (mirrors `legolas/`, `elrond/`)

**Phase-1 P1 context (continuing in parallel):**
- `agentic_orchestration/hive-mind/scope-of-work-phase-1-p1.md` — main hive mission; in flight
- `agentic_orchestration/hive-mind/coordination-matrix.md` — per-deliverable seam mapping
- `agentic_orchestration/hive-mind/phase-1-p1-log.md` — hive log
- `agentic_orchestration/hive-mind/state-of-hive-2026-05-17.md` — activation digest

**Recent narrative:**
- `canonical/story/canonical-6-transition-retire-hybrid-mage-2026-05-18.md` — hybrid_mage retired; canonical-7 in flight
- `canonical/story/audio-register-canon-2026-05-17.md` — 5-layer audio architecture LOCKED
- `canonical/story/mobile-feel-target-doe-2026-05-17.md` — mobile feel target locked
- `canonical/story/mobile-ux-execution-plan-2026-05-17.md` — mobile execution plan
- Dispatch `2026-05-18-drax-v1-20-mobile-touch-zones-plus-holy-controller-plus-door-icon-plus-first-tileset.md` — active

**Engineering disciplines + governance:**
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — all disciplines bind sprint work
- `agentic_orchestration/GOVERNANCE.md` — ADRs continue; ADR-006 no-knight-rider-pushes honored
- `agentic_orchestration/REVIEW_PROCESS.md` — 5 principles + 5 traps continue

---

## § 11 — Activation checklist (knight-rider)

When knight-rider opens session and reads this invocation:

- [ ] Read this invocation in full
- [ ] Verify pre-authorization matrix (§ 6) is acceptable — if any row's pre-authorization is questionable for tonight's actual operational context, defer that row and route through pre-authorized alternatives
- [ ] Read `canonical/story/hive-mind-protocol-2026-05-17.md` if not freshly in context
- [ ] Verify in-flight Phase-1 P1 work compatible with sprint scope (rocket / gamora / star-lord / elrond active dispatches)
- [ ] Acknowledge invocation in hive log (`phase-1-p1-log.md`) with STATE entry: "Sprint 2026-05-18 mobile-playable + analytics + visual-benchmark commenced"
- [ ] If pre-authorized: create `.claude/agents/galadriel.md` from § 4 spec; create `agentic_orchestration/galadriel/` directory tree with placeholder README
- [ ] Distribute per-seam tasking per § 3
- [ ] Set midpoint state-of-hive timer/intent (~3-4h in)
- [ ] Set morning-briefing accumulation discipline (any L3 surfaces → write entry)
- [ ] Begin coordination

---

## § 12 — Closing

The hive has been moving together since 2026-05-17 activation. Tonight's sprint focuses three of its energies — the demo's mobile surface; the loadout's value-story; the visual evidence against genre peers — in a single overnight pulse, while Matt rests.

Three deliverables. Three tracks. One hive. No human in the loop.

The Mirror should be set tonight. By morning, Matt should see — really see, in screenshots and rendered surfaces and rubric scores — what the team has built, what it looks like next to its peers, and where the next breath of work goes.

The hive moves together. Mithrandir tonight serves as design conscience and IA author; galadriel newly arrives to bring the Mirror; knight-rider harmonizes; the four engineering seams (rocket + gamora + star-lord + drax) and the curators (elrond) and the watcher (jack-ryan) continue their work in the deep, while the night turns.

By dawn: a playable phone surface, a value-telling analytics page, and a comparative-rubric truth about where the work actually stands.

That is the sprint. The hive may begin when knight-rider opens session.

---

*Authored 2026-05-18 evening by gandalf, per Matt directive. Targeted scope-focus invocation within ongoing Phase-1 P1 hive-mind operating mode. Single-night autonomous sprint. Three tracks. New agent galadriel commissioned within. Mithrandir signs.*
