# Loadout Analytics Suite — Information Architecture (Iteration 1)

> **STATUS:** HISTORICAL-INFORMATIVE (pre-Epoch-4; consult for lineage only — not current truth) — see `canonical/00-ground-state.md` for current truth

**Authority:** gandalf (story-and-design steward), per overnight sprint Track B § 2.2 deliverable 5.
**Status:** **DRAFT-AS-AUTHORED — sufficient to unblock downstream** (star-lord, elrond, drax). Iterations 2/3 refine after first-pass impl lands.
**Pattern:** B (Matt-approval not blocking; pre-authorization matrix § 6 row 11 covers new canonical-story docs).
**Companion docs:**
- `canonical/story/substrate-identity-declarations-2026-05-17.md` — the 7 substrate identities the suite renders
- `canonical/story/mobile-feel-target-doe-2026-05-17.md` — register lock (DoE-class)
- `agentic_orchestration/galadriel/reference-images/MANIFEST.md` — visual canon reference set
- `canonical/16-project-roadmap.md` — what the engine has shipped (B-series)

---

## § 0 — TL;DR

The loadout app gets a **new narrative-first page at `/the-work`** (drax may pick a different slug — see § 2.4) that tells the story of what this engine and hive have built. Six story arcs, scrolled top-to-bottom, mobile-first. The existing `/analytics` page remains as the dev-numbers dashboard for power-users; the new page is the **value-story** view that a Matt-on-phone (or a stranger-on-pitch) reads and *gets*.

**Six arcs, Phase-1 disposition:**

| # | Arc | Phase-1? | Why |
|---|---|---|---|
| 1 | **The Substrate Journey** | ✅ SHIP | Substrate declarations exist (7 yaml-in-md); SubstrateHeatmap already built; canonical-4 → canonical-7 narrative is live |
| 2 | **The LLM Thematic Universe** | ✅ SHIP | `cosmological_vocabulary.json` per season is rich and underexposed; D1 corpus counts exist in memory + code |
| 3 | **The Catalogue** | ✅ SHIP (slim) | JSONL curation manifests + catalogue.db exist; per-vendor + per-pack tallies are computable; not all coverage data is exportable tonight |
| 4 | **The Diversity Architecture in Action** | ⚠️ PARTIAL | Archetype distribution + modifier-range exist; spirit-swap differentiation evidence is **THIN** (solo-play only, no swap-data yet) → ship the architecture-view; flag swap-evidence Phase-2 |
| 5 | **The Journey Across Seasons** | ⚠️ PARTIAL | SeasonTimelineChart + SeasonSummaryCards exist; Earth Self / Court of Forms preview is **design-only**; perception-test signal **does not yet exist** → ship timeline + cards; flag the meta-layer Phase-2 |
| 6 | **The Work Behind The Work** | ⚠️ PARTIAL | Commits + dispatches enumerable, but loadout app cannot read meta-repo today → star-lord exports a `hive-summary.json`; iterate impl carefully; if data not exportable tonight, ship a single teaser card + defer body to Phase-2 |

**Three honest "Phase-2 placeholder" cards** ship in iteration 1 so the suite *visibly admits* what isn't measured yet — spirit-swap evidence, Earth Self/Court preview, perception-test signal. Honesty beats hollow panels. Pattern: stub card with descriptive prose + "coming next iteration" footer; no fake metric.

The existing `/analytics` page is **NOT TOUCHED** by iteration-1 work (it's good; don't break it). Cross-link from `/the-work` arcs back into `/analytics` deep-dives ("see all charts →").

**Visual register:** inherit existing loadout palette (gray-950 / gray-800 / gray-100 / font-mono labels); add **substrate-coded accent colors** per § 3.2; alternating density (chart → prose → image → chart); avoid corporate-dashboard look; this is a **dev-tool that respects mystery**, not a marketing page.

---

## § 1 — Story arcs (the six)

For each arc: headline · what data backs it · visualization · phase disposition.

### § 1.1 — Arc 1: The Substrate Journey

**Headline a Matt-on-phone reads and gets:** *"From four elements to seven. Each substrate makes a promise and refuses what it isn't."*

**What it says:** Reincarnated started canonical-4 (fire/water/earth/wind + physical). Tonight it lives canonical-7 with lightning, holy, shadow added — and hybrid_mage retired this morning. Each substrate is not just a tint but a *commitment*: a mechanical signature it IS, a forbidden mechanic it REFUSES, an iconic register the LLM must speak in. The expansion isn't volume; it's identity.

**Data consumed:**
- `canonical/story/substrate-identity-declarations-2026-05-17.md` — 7 YAML identity blocks (parsed at build time OR hand-transcribed into a TS const; star-lord scopes whichever is faster)
- `output/standard-demo-regen-2026-05-17/season_0020{11..15}/manifest.json` — substrate appearances per season
- `output/standard-demo-regen-2026-05-17/season_0020{11..15}/classes/*.json` — `dominant_element` field per class
- Already-computed `analyticsSeasons` in `useAnalytics.ts` (re-use; no new fetch)

**Visualization:**
1. **Substrate identity card grid (7 cards, 1 per substrate).** Each card shows: substrate icon/glyph; substrate name in substrate-accent color; 3-5 iconic-verb chip row; combat pillar (one tag); ailment signature (one chip); paired-with / forbidden-with badge if applicable. Mobile: stack vertically; desktop: 2-3 across.
2. **Substrate heatmap (existing component — `SubstrateHeatmap.tsx`).** Move/reuse here. Title-card it as "**The expansion, season by season**."
3. **Canonical-7 narrative callout (existing in `Analytics.tsx`).** Move/reuse here as the section opener.

**Phase-1 disposition:** ✅ SHIP IN FULL.

**Honest gaps to name (small footnote, not a stub card):** *"Lightning, holy, shadow still need a grouping-vocab extension (resonance/radiance/penumbra L2 labels pending Task #4) — for now their grouping_label entries dangle. Engine ships them; suite ships them; vocabulary extension follows."*

---

### § 1.2 — Arc 2: The LLM Thematic Universe

**Headline:** *"Every season the LLM writes the world. Same substrates. Different language. The same fight feels different because the names are different."*

**What it says:** The substrates are stable. The *language for the substrates* is per-season. A coal-vein season ("The Dwarves' Empty Halls") gets *Seam Pressure / Damp Creep / Forge Remembrance / Withdrawal Soot* as its ignition/suffusion/radiance/penumbra fills. A hippodrome season ("Hippodrome of Ghosts") gets *Gallop-Surge / Pale Circuit / Dead Rein / Wheel-Break.* The LLM is the **author of the thematic surface**; the substrate identities are the **grammar it speaks within**. This is what "LLM-driven thematic universe" actually means in practice — and it's been hiding inside `cosmological_vocabulary.json` files no player has yet read.

**Data consumed:**
- `output/standard-demo-regen-2026-05-17/season_*/cosmological_vocabulary.json` — per-season slot-fills + pair-rationale prose **(THIS IS THE GOLD)**
- `output/standard-demo-regen-2026-05-17/season_*/manifest.json` — `season_theme_element`, `anchor`, `seasonal_elements`
- D1 element-name vocabulary corpus (per MEMORY.md: 81 allow-list / 40 eligible / 35 quarantine, 156 total entries; per-substrate distribution exists; star-lord locates the canonical source file — likely engine-internal config)

**Visualization:**
1. **The "Season as authored world" featured card (1 per season, carousel or stacked).** For each available season:
   - Anchor name + thematic blurb (one line)
   - The 8 slot-fills laid out as 4 pairs (thermal / position / luminance + impact + resonance), each pair with the LLM's pair-rationale prose under it. *This is the most poetic surface the project has ever shown a user.* Prose-readable on mobile; substrate-accent-coded headers.
2. **D1 vocabulary corpus bar.** Stacked bar showing allow-list (81) / eligible (40) / quarantine (35). Subtitle: *"Words the engine considers; words it ships; words it holds back."* Optional per-substrate breakdown table beneath.
3. **Iconic-verb cloud or chip-grid (per substrate).** 7 mini-rows of the substrate's iconic_verbs ("ignites · burns · scorches · engulfs · flares · consumes · kindles") in substrate-accent color. Direct visual proof of the per-substrate vocabulary register.

**Phase-1 disposition:** ✅ SHIP IN FULL. The cosmological_vocabulary surface alone justifies the whole suite.

**Honest gaps to name:** *"D1 status reflects current overrides — `pall`/`miasma`/`rime` demoted, `cloud`/`hurricane` promoted (per 2026-05-12 rounds). Counts move as the corpus evolves."* Small footnote, not a stub.

**Visual register note (CRITICAL):** the pair-rationale prose is **literary**. The page must give it breathing room — not bury it inside a chart card. Suggest a centered, larger-line-height prose block (~prose-base · max-w-prose) with substrate-accent rule lines above each pair. Drax: this is the one section where typography matters more than density. Don't squeeze it.

---

### § 1.3 — Arc 3: The Catalogue

**Headline:** *"Hundreds of assets crawled, scored, mapped. A small subset reaches the dungeon. The rest is held against future seasons."*

**What it says:** The hive has been crawling pixel-art and audio vendor catalogues (CraftPix, Chierit, Pimen, WSP, et al.); Elrond curates; Drax wires the chosen subset into the demo. Showing the **funnel** — crawled → eligible → curated → shipped — communicates the *scale of work behind any one dungeon prop* and the *intentionality of what makes it in.* This is the unglamorous infrastructure that lets the LLM thematic surface actually have visual representation.

**Data consumed:**
- `agentic_orchestration/research/curated/*.jsonl` — per-vendor curation subsets (audio-substrate, audio-atmospheric, audio-foley, audio-music, ambient-props, etc.); per-pack tallies
- `agentic_orchestration/research/curated/catalogue.db` (SQLite) — `catalogue_assets` (48 rows currently), `catalogue_packs` (3), `catalogue_sources` (3), `asset_style_tags` (461)
- `agentic_orchestration/research/curated/audio-coverage-matrix-vs2a-2026-05-17.md` — coverage rubric output
- Elrond's per-tier curation summaries (per-vendor MDs in `research/curated/`)

**Visualization:**
1. **Funnel diagram (4 stages):** Crawled → Eligible → Curated → Shipped. Numbers per stage. Stage drop-off as visual width.
2. **Per-vendor stacked bar:** vendor name on Y, asset counts stacked by status (eligible / curated / shipped). The 3-4 biggest vendors visible; long tail collapsed.
3. **Coverage matrix slice (small table or heatmap):** substrate × asset-category (sprite / audio / VFX / prop) coverage status (GREEN / YELLOW / RED) per the rubric. This is the *next acquisition decisions surfaced honestly*.
4. **Featured "tonight's curation" card:** the chierit substrate-mapping work that landed today (Lightning Ronin + Light Valkyrie → mini-boss tier; lightning + holy coverage advanced YELLOW → GREEN) as a *worked-example* card. Iteration-2 rotates featured curation; iteration-1 just freezes today's win.

**Phase-1 disposition:** ✅ SHIP, SLIM. The funnel + per-vendor bar + featured-curation card are achievable tonight. Coverage matrix is the stretch — ship if elrond's manifest cleanly surfaces it; defer to iteration-2 if not.

**Honest gaps to name:** The catalogue.db is 48 assets currently — much of the curation work lives in JSONL manifests, not the DB. Elrond is mid-migration. Card prose acknowledges *"a portion of the catalogue is still flat-file; DB rollup follows."*

---

### § 1.4 — Arc 4: The Diversity Architecture in Action

**Headline:** *"Substrate × role × kit. Different shapes by construction — not by content authoring."*

**What it says:** The engine doesn't author "fire_mage" as a hand-tuned class. It composes substrate × role × geometry × mechanical-signature and lets archetypes *emerge*. This is the **diversity architecture** the form-bias diagnosis recovered toward (file 37). Show the architecture's outputs as evidence: archetype distribution, modifier ranges, stat radars, role × substrate matrix. Don't just hand the user numbers — frame each chart with one prose sentence: *"this is what the architecture produced."*

**Data consumed:**
- All existing analytics outputs from `useAnalytics.ts`: `archetypeBySeasonRows`, `modifierRanges`, `statRadarEntries`, `winRateBins`, `allArchetypes`, `allSubstrates`
- (NEW for iteration-1 if scope allows; otherwise Phase-2) Role × substrate composition matrix — star-lord exports this; archetype tag → (role, substrate) tuple → count per season

**Visualization:**
1. **Architecture diagram (small SVG or styled HTML):** substrate × role → archetype, illustrating the *composition mechanic*. One static visual; no live data. *"This is how it works."*
2. **Role × substrate matrix.** Heatmap or table showing archetypes per cell. Phase-1 if data manifests it cleanly; else Phase-2 with a stub.
3. **Reuse existing ArchetypeStackedBar (per-season distribution).** Title-card as *"What the engine produced across the 5 canonical-7 seasons."*
4. **Reuse existing ModifierRangeChart.** Title-card as *"Balance across archetypes — narrower is more consistent. Hunter's 1.82× range is the architecture's known noise."* (Per MEMORY.md sidecar finding.)
5. **Stub card — "Spirit-swap differentiation evidence."** Prose: *"The engine's load-bearing seam — that swapping into a different substrate produces a meaningfully different fight — is verified at the level of statistics and shape (the charts above), not yet at the level of player-felt swap data (no players yet). Phase-2: ingest perception-test results; surface swap-vs-no-swap differential metrics."* Honest stub. No fake gauge.

**Phase-1 disposition:** ⚠️ PARTIAL. Ship arch-diagram + existing charts re-framed; ship role × substrate matrix if data manifests cleanly; ship spirit-swap stub explicitly.

---

### § 1.5 — Arc 5: The Journey Across Seasons

**Headline:** *"Each season inherits from the last and surrenders to the next. The Court remembers what the Earth-Self walked through."*

**What it says:** Reincarnated's frame is *seasonal*: bodies are temporary, the journey accumulates. The Phase-0 product ships single-season; the **meta-layer (Earth Self + Court of Forms + cross-season cohesion)** is in design but not yet running. Show the per-season cards + timeline as the *measurable surface* of the journey; show the meta-layer as a *preview commitment* with prose teasing what comes next. Don't lie about what's playable.

**Data consumed:**
- `useAnalytics.ts` — `seasonSummaryCards`, `seasonTimeline`
- `canonical/story/cosmology-reincarnated.md` — Earth Self + Court framing (for preview-card prose)
- `canonical/story/court-of-forms.md` — Court mechanic preview prose
- (Phase-2) perception-test infrastructure (D27) — not yet collecting data

**Visualization:**
1. **Reuse SeasonSummaryCards.** Title-card as *"Six seasons, one journey."* (Counts 5 canonical-7 + 1 Yomi; rocket's 002016 not yet stable so don't include until convergence resolves.)
2. **Reuse SeasonTimelineChart.** Title-card as *"Modifier drift across the journey — what the balance loop landed."*
3. **Cross-season cohesion strip (Phase-2 stub or thin Phase-1).** Prose card explaining what cohesion *will measure* (anchor-name continuity, vocabulary register consistency, archetype overlap across seasons). Phase-1: show this as a stub. Phase-2: implement metric.
4. **Earth Self / Court of Forms preview card (stub).** Prose: *"Reincarnated Phase 0 ships the seasonal journey. The Court of Forms — the gallery of accumulated bodies the Earth-Self has worn — is the meta-layer that frames every season as one passage in a longer arc. It is not yet playable. It is canonically authored (see [doc link]) and engine-side staging follows post-VS2a."* Optional: small mockup or design-doc-thumbnail.

**Phase-1 disposition:** ⚠️ PARTIAL. Ship timeline + summary cards + two stub-cards (cohesion + Court preview). Honest meta-layer admission is a feature, not a hole.

---

### § 1.6 — Arc 6: The Work Behind The Work (Hive at Scale)

**Headline:** *"Eight agents. Four repos. Three months. One pulse."*

**What it says:** Reincarnated is built by a synthetic engineering team operating across four repositories with structured dispatches, hive logs, and per-seam protocols. Showing the *scale and rhythm of the work* (commits per seam per day, dispatches per purpose, decisions logged, sprint pulses) communicates that this is not a hobby thrash — it is a coordinated production system. This is the *production-credibility* surface for a future pitch viewer.

**Data consumed:**
- (NEW — depends on star-lord) `agentic_orchestration/hive-mind/hive-summary.json` — commits-per-seam-per-day, dispatches-per-purpose (parsed from `dispatches/` filenames + git logs across 4 repos)
- `agentic_orchestration/CHANGELOG.md` — coarse-grained event log
- `agentic_orchestration/dispatches/` filenames — parse `<date>-<seam>-<purpose>.md` pattern; tally by seam + date
- Git log across 4 repos — `git log --oneline --all` per repo; tally commits per day per repo
- (Phase-2 nice-to-have) decisions-log entries — count + by-status

**Visualization:**
1. **Per-seam pulse chart:** day-by-day commits stacked by seam (drax/rocket/gamora/star-lord/elrond/jack-ryan/gandalf/knight-rider). Last 14 days. *"The hive moves together."*
2. **Dispatches-by-purpose donut or bar:** dispatch filenames tagged (impl / curation / advisory / sprint / etc.). Pattern-A vs Pattern-B vs hive-mind dispatches.
3. **Team manifest card:** small 1-line role descriptions for the 8 agents (gandalf, drax, rocket, gamora, star-lord, elrond, jack-ryan, knight-rider; galadriel pending Matt L3). Self-portrait of the hive.
4. **Featured sprint card:** tonight's overnight sprint (Track A + B + C) as a worked example. *"This page exists because of tonight's hive run."* Meta-reflexive; intentional.

**Phase-1 disposition:** ⚠️ PARTIAL.

- If star-lord can export `hive-summary.json` tonight → ship pulse chart + dispatches breakdown + team manifest + sprint card.
- If star-lord cannot tonight (parsing 4-repo git logs + dispatch filenames is non-trivial; depends on his data-manifest pass turning up the right shape) → ship only the team manifest card + sprint card + a "Phase-2: full hive metrics next iteration" footer. The card-only version still earns the section.

**Honest gaps to name:** *"This is the most build-time-coupled section — the loadout app does not natively read the meta-repo. Iteration 1 ships what star-lord can export tonight; later iterations may bake hive metrics into the engine's `output/` artifact stream so the suite ingests them like everything else."*

---

## § 2 — Route + page structure

### § 2.1 — New page, not overhauled `/analytics`

**Recommendation:** add a NEW route. The existing `/analytics` is **good**, battle-tested, and serves a different purpose (data-dashboard for power-users). Overhauling it tonight risks breaking what works and muddles two intents into one surface.

**Two pages, two intents:**

| Route | Intent | Reader | Density |
|---|---|---|---|
| `/the-work` (NEW; or `/story` or `/journey` — drax picks) | Narrative-first value-story; six arcs scrolled top-to-bottom | Matt-on-phone, pitch-viewer, son-on-couch, future collaborator | Mixed — prose between data; substrate accents; literary pair-rationales |
| `/analytics` (UNCHANGED tonight) | Data-first dashboard; all charts; deep-dive | Matt-debugging, gandalf-reviewing, jack-ryan-watching | Dense — all charts above the fold rotation |

**Cross-link policy:** each `/the-work` section ends with a small "see all charts →" link into the corresponding `/analytics` deep-dive. The two pages triangulate the story.

### § 2.2 — Single page, sectioned, mobile-first scroll

**Why single page:** Matt-on-phone scrolls top-to-bottom; that's the dominant read posture on mobile. Tabs require taps + cognitive switching that fragments the narrative. The DoE register canon is **vertical reading flow with dense atmospheric moments** (per `mobile-feel-target-doe-2026-05-17.md`). The page should *feel like* one long unfurling — same instinct.

### § 2.3 — Landing surface (first scroll)

Top of page = the **headline framing card** + arc-1 substrate identity grid. Reader within 2 seconds sees:

1. **Page headline + 1-sentence sub.** e.g. *"The Reincarnated Engine — what it builds, what speaks through it, what stands behind it."*
2. **Stat strip (reuse `StatBadge` from existing analytics):** Seasons · Classes · Archetypes · Substrates · Dispatches · Commits. Tabular-nums, restrained.
3. **Arc-1 substrate identity grid begins.** 7 cards. The journey starts.

### § 2.4 — URL slug — drax picks

Candidates: `/the-work`, `/story`, `/journey`, `/about`, `/inside`. My weak preference: `/the-work` — it's the most accurate (this IS the work) and doesn't romanticize. Drax may pick differently; the IA does not depend on the slug.

### § 2.5 — Navigation hooks

- Add nav entry in `Nav.tsx` between `/sample` and `/analytics`: "**The Work**" (or whichever name)
- Smooth-scroll anchors per section (`#substrates`, `#vocabulary`, `#catalogue`, `#diversity`, `#journey`, `#hive`)
- Desktop: optional sticky sidebar TOC (small; right-rail; collapses on mobile)
- Mobile: no sidebar; rely on scroll + a single "↑" back-to-top button after scroll depth > 80vh

### § 2.6 — Visual hierarchy on first scroll

```
┌─────────────────────────────────────┐
│ Nav (existing)                      │
├─────────────────────────────────────┤
│ Page headline                       │
│ Stat-strip badges                   │
├─────────────────────────────────────┤
│ § ARC 1 — The Substrate Journey     │
│   Section-opener prose (2 lines)    │
│   [Canonical-7 narrative callout]   │
│   [Substrate identity grid: 7 cards]│
│   [SubstrateHeatmap]                │
│   "see all charts →" link           │
├─────────────────────────────────────┤
│ § ARC 2 — The LLM Thematic Universe │
│   ...                                │
```

Section breaks should be **substrate-accented rule lines** (1px, accent-color of the next section's dominant substrate or a neutral gray-700) — not big spacious whitespace. DoE-register is dense; honor it.

---

## § 3 — Visual language guidance

### § 3.1 — Inheritance

**Inherit unchanged from existing loadout app:**
- Background: `bg-gray-950`
- Border: `border-gray-800`
- Body text: `text-gray-100`
- Label register: `font-mono uppercase tracking-wide text-xs text-gray-500`
- Stat numerals: `font-semibold tabular-nums`
- Card pattern: `bg-gray-900 border border-gray-800 rounded-lg px-4 py-3`
- Touch-targets: `min-h-[44px]` (mobile-readiness floor)
- Existing `StatBadge`, `ChartCard`, `Card`, `Tag`, `ClassIcon` components — reuse

### § 3.2 — Substrate accent palette (NEW; recommend drax codify)

Each substrate has an accent color used for section headers, identity-card borders, chip highlights, rule lines. Drawn from genre-canonical hues + the existing loadout's `violet-` precedent for canonical-7. Tailwind-namespaced where possible:

| Substrate | Accent (Tailwind class) | Notes |
|---|---|---|
| fire | `red-500` (text) / `red-900/40` (bg) / `red-800` (border) | Ember-glow register |
| water | `cyan-400` / `cyan-950/40` / `cyan-800` | Deep cold |
| earth | `amber-700` / `stone-900/40` / `stone-700` | Loam; not bright |
| wind | `slate-300` / `slate-900/40` / `slate-700` | Pale, kinetic |
| lightning | `yellow-300` / `yellow-950/40` / `yellow-700` | Discharge-bright |
| holy | `amber-200` / `amber-950/40` / `amber-700` | Warmer than yellow; clerical |
| shadow | `purple-400` / `gray-900/60` / `purple-900` | Penumbra; *quieter than fire's red* — restraint matters |
| physical | `gray-400` / `gray-900/40` / `gray-700` | Neutral; the un-elemental |

**Critical register note for shadow:** shadow's iconic_register is *quieter, lower-frequency, weight-of-absence*. Do not give shadow a "wow" color. The accent should feel *withdrawn*, not *malevolent-eye-grabbing*. The above purple-400 is already quieter than the impulse to make shadow electric-purple — keep it that way. (Solo Leveling precedent per gandalf-design-lineage Layer 5: shadow as *occlusion, not malice*.)

### § 3.3 — Typography rhythm

Three registers across the page:

1. **Label register** (`font-mono uppercase tracking-wide text-xs`) — for stat labels, chart axes, vendor names. Tight, technical, restrained.
2. **Stat register** (`font-semibold tabular-nums text-xl`) — for numbers. The eye lands on these. Use sparingly.
3. **Narrative register** (default sans; `text-sm leading-relaxed` for prose; `text-base` for arc-headlines; `text-lg` for the page title only) — for section openers and arc 2's literary pair-rationales. Looser line-height. Don't shrink it; this is the prose that makes the page *mean something.*

**Arc-2 special case (cosmological_vocabulary prose):** The pair-rationale text from `cosmological_vocabulary.json` is multi-clause, literary, and *the highest-value prose in the entire app*. Render it with:
- `font-serif` if the loadout has a serif option (it doesn't currently — drax decides whether to import one or stay sans)
- `text-base leading-loose max-w-prose mx-auto`
- Substrate-accent rule line above each pair (1px, opacity-50)
- Pair labels (thermal / position / luminance) in label-register as eyebrow

This is the **one section where the typography breaks the "dense dashboard" rhythm and gives the prose air.** Intentional. The pair-rationales are where the LLM's thematic-universe claim becomes legible to a human.

### § 3.4 — Iconography

- Use existing `game-icons.net` icons (CC BY 3.0; already footer-credited)
- One icon per substrate (fire-flame, water-drop, earth-mountain, wind-swirl, lightning-bolt, holy-sun, shadow-occluded-eye, physical-fist) — chosen by drax from game-icons.net library
- Avoid emoji — the existing app doesn't use them and shouldn't start
- Avoid corporate Material/Heroicons — they read SaaS; this is a fantasy-engine surface

### § 3.5 — Density rhythm

Alternate **dense → breath → dense** within each arc:

- Dense = chart card; identity grid; funnel
- Breath = section-opener prose; pair-rationale block; stub-card prose
- Dense = next chart; data table

This is DoE-compatible: DoE has *atmospheric moments inside the HUD-dense register* (the candle, the ember, the lone player walking through). Same idea: dense by default, intentional moments of prose-only breath.

### § 3.6 — What to AVOID

- **No marketing hero gradients.** Solid gray-950 background; no `bg-gradient-to-br from-violet-500 to-pink-500` energy. This is not a SaaS landing page.
- **No animated stat counters.** Numbers are present and stable; the eye lands without choreography. (Existing app respects this.)
- **No "Brought to you by" branding.** Footer stays as it is — game-icons.net + CC BY 3.0 credit; nothing else.
- **No emoji in headers or callouts.** Use icons or accent rule lines.
- **No exclamation marks.** The voice is **understated.** This is restrained, evidentiary writing. Pair-rationales are literary, but headers and callouts stay calm.
- **No "We" or "Our".** The page describes the work. Not a team-pitch. Voice is third-person observational.

### § 3.7 — Mobile-first floors

- Section padding: `px-4 py-6` minimum (matches existing pages)
- Touch targets: `min-h-[44px]` for any tappable element (matches v1.19.5 audit P0 fix)
- Max-width: `max-w-6xl mx-auto` (matches existing) — but arc-2 pair-rationale prose blocks should be `max-w-prose` (~65ch) for readable line-length
- Chart heights: 240px floor mobile / 360px desktop (matches existing recharts patterns)
- Image-heavy panels (Phase-2 featured curation): lazy-load; provide loading skeleton

---

## § 4 — Phase-2 placeholders

These belong in the suite but not in iteration 1. Each ships as a **stub card** with descriptive prose + "coming next iteration" footer. **No fake metric. No placeholder lorem-ipsum chart.**

| # | Placeholder | Why deferred | Stub-card prose hook |
|---|---|---|---|
| P2-A | **Spirit-swap differentiation evidence** | Solo-play only; no swap data yet | *"The engine's swap claim is verified in shape (modifier ranges, role-distribution diversity above). Player-felt swap evidence requires playtest data the project does not yet have."* |
| P2-B | **Perception-test signal (D27)** | D27 infrastructure under design; no measurements yet | *"The diversity claim is testable: does a player feel each substrate as different? D27 will measure this. Coming after VS2a closes."* |
| P2-C | **Earth Self / Court of Forms preview** | Meta-layer is design-only; not engine-staged | *"Reincarnated Phase 0 ships the seasonal journey. The meta-layer — Earth Self, Court of Forms, cross-season accumulation — is canonically authored; engine staging follows."* (link to cosmology/court canonical docs) |
| P2-D | **Cross-season cohesion metrics** | Requires anchor-name and vocabulary-register comparators not yet built | *"Cohesion measures whether successive seasons rhyme — anchor names, vocabulary register, archetype overlap. Iteration 2 ships the comparator."* |
| P2-E | **Hive pulse metrics (full)** | Requires meta-repo data-export pipeline (depends on star-lord scope tonight) | *"The hive's daily pulse — commits, dispatches, decisions — is enumerable from the four repos. The loadout app does not yet ingest meta-repo data; star-lord's manifest pass scopes the path."* |
| P2-F | **Audio coverage panel** | Audio-curation work exists in JSONL; rendering audio coverage in a web app is non-obvious surface | *"Audio coverage by substrate, by tier, by acquisition-status. Worth its own subsection. Iteration 2."* |
| P2-G | **VFX / sprite gallery** | A visual gallery of the geometry-VFX library (per `geometry-vfx-coverage-assessment.md`) | *"What the dungeon looks like, geometry by geometry. Worth showing once the gallery component is built."* |

**Stub-card pattern (drax to template):**

```
┌─────────────────────────────────────┐
│ ◌ Spirit-swap differentiation       │ ← icon + headline (accent color, dim)
│   The engine's swap claim is        │ ← descriptive prose (text-sm leading-relaxed)
│   verified in shape (above).        │
│   Player-felt swap evidence         │
│   requires playtest data the        │
│   project does not yet have.        │
│   ─────────────────────────────     │ ← thin rule
│   PHASE 2 · NEXT ITERATION          │ ← label-register footer
└─────────────────────────────────────┘
```

Border: `border-dashed border-gray-700` to visually distinguish stubs from live cards. Honest. Not deceptive.

---

## § 5 — Data-source manifest seed

This seeds star-lord and elrond's full data manifests (their dispatches). For each panel: which data files / fields / endpoints. Star-lord covers engine-side; elrond covers catalogue-side; if a panel needs cross-source data, both authors note it.

### § 5.1 — Engine-side (star-lord scope)

| Panel | Data source | Field(s) needed | Shape | Status |
|---|---|---|---|---|
| Substrate identity grid (Arc 1) | `canonical/story/substrate-identity-declarations-2026-05-17.md` (or transcribed TS const) | `mechanical_signature[]`, `forbidden_mechanics[]`, `combat_pillar`, `ailment_signature.name`, `iconic_verbs[]`, `iconic_register`, `paired_with`, `forbidden_hybrid_with` | 7 records (1 per substrate) | EXISTS — needs extraction (YAML in MD or TS literal) |
| Cosmological vocab cards (Arc 2) | `output/standard-demo-regen-2026-05-17/season_*/cosmological_vocabulary.json` | `season_id`, `anchor_name`, `season_theme_element`, `slot_fills` (8 keys), `pair_rationales` (3 keys), `pair_primary_rationale` | 1 per season | EXISTS — bundle into loadout `/data/seasons/cosmological_vocabulary.json` per-season or merged |
| D1 vocabulary corpus (Arc 2) | Engine config — likely `reincarnated-engine/src/reincarnated/foundation/` or `config/` | per-entry: `name`, `d1_status` (allow-list/eligible/quarantine), `primary_substrate`, `d1_total` score | ~156 records | star-lord locates canonical file; current state per MEMORY.md is 81/40/35 |
| Iconic-verb chips (Arc 2) | substrate-identity-declarations | `iconic_verbs[]` per substrate | reused from Arc 1 source | EXISTS |
| Role × substrate matrix (Arc 4) | `output/standard-demo-regen-2026-05-17/season_*/classes/*.json` | `archetype_tag`, `dominant_element`, `role` (if present; else infer from archetype name) | aggregated per (substrate, role) | EXISTS — needs aggregation pass |
| Archetype distribution (Arc 4) | already in `useAnalytics.ts:archetypeBySeasonRows` | reuse | reused | EXISTS — wired |
| Modifier ranges (Arc 4) | already in `useAnalytics.ts:modifierRanges` | reuse | reused | EXISTS — wired |
| Season cards + timeline (Arc 5) | already in `useAnalytics.ts:seasonSummaryCards`, `seasonTimeline` | reuse | reused | EXISTS — wired |
| Hive pulse — commits per seam (Arc 6) | git log across 4 repos | per-commit `author`, `date`, `seam` (parsed from commit msg prefix or branch) | aggregated per (seam, date) | NEW — needs export script; star-lord scopes feasibility tonight |
| Hive pulse — dispatches by purpose (Arc 6) | `agentic_orchestration/dispatches/*.md` filenames | parse `<date>-<seam>-<purpose>.md` | aggregated per (purpose, seam, date) | NEW — straightforward filename parse |
| Featured sprint card (Arc 6) | `agentic_orchestration/gandalf/requests/2026-05-18-knight-rider-mobile-playable-analytics-visual-benchmark-sprint.md` + this IA + galadriel docs | static prose | hand-curated | EXISTS — static authoring |

**Suggested star-lord output shape:** a single JSON bundle at `reincarnated-loadout/src/data/the-work-data.json` (or split per arc) consumed by a new `useTheWorkData()` hook mirroring `useAnalytics()`. The bundle is generated by an export script run in the engine repo and copied to the loadout repo as part of the existing sync flow.

### § 5.2 — Catalogue-side (elrond scope)

| Panel | Data source | Field(s) needed | Shape | Status |
|---|---|---|---|---|
| Funnel (Arc 3) | `research/curated/catalogue.db` + JSONL inventories | total crawled count (from `crawl_sessions`); eligible count (per source); curated count (per `*-subset-vs2a-2026-05-17.jsonl` files); shipped count (from drax wire-in inventory — coordination with drax) | 4 numbers per source, summed | PARTIAL — catalogue.db has 48 assets; JSONLs have more; "shipped" needs drax cross-ref |
| Per-vendor stacked bar (Arc 3) | `research/curated/catalogue.db:catalogue_sources` + per-vendor JSONLs | per vendor: `eligible`, `curated`, `shipped` counts | per-vendor records | PARTIAL — same as funnel |
| Coverage matrix (Arc 3) | `research/curated/audio-coverage-matrix-vs2a-2026-05-17.md` (parse) + sprite/VFX equivalents (may not all exist) | substrate × category → status (G/Y/R) | ~7 × 4 grid | PARTIAL — audio exists; sprite/VFX coverage less formalized |
| Featured curation card (Arc 3) | `elrond/v1.10` chierit-substrate-mapping notes + handoff brief | static prose | hand-curated | EXISTS — static authoring |
| Per-vendor asset gallery (P2-G stretch) | `catalogue_assets` table + thumbnail paths | asset records with image URL | TBD | EXISTS PARTIALLY — image rendering in loadout is unproven; defer to P2-G |

**Suggested elrond output shape:** `agentic_orchestration/research/curated/the-work-catalogue-summary.json` — emitted by elrond's curation pass; copied or fetched by the loadout app via the same sync pattern as engine data. Single file; avoids loadout-needs-SQLite question.

### § 5.3 — Shared / cross-source

- **Substrate accent color palette** (§ 3.2 above) is hand-authored by gandalf in this doc and consumed by drax as TS const; no engine/catalogue source needed.
- **Stub-card prose** for Phase-2 placeholders is authored in this doc (§ 4) and transcribed by drax; not data-sourced.
- **Page headline prose** is gandalf-authored (in implementation review) — drax requests final wording from gandalf when implementing, or uses the working drafts in this doc.

---

## § 6 — Iteration-1 implementation guidance for drax (lightweight; drax decides)

This is **not** a design system. It's enough register guidance to keep drax from clashing with what the demo is becoming.

- **Component reuse:** `StatBadge`, `Card`, `Tag`, `ChartCard`, all existing `analytics/*` chart components are reusable. Wrap in section-shells, don't rebuild.
- **New components to introduce:**
  - `SubstrateIdentityCard` (Arc 1)
  - `CosmologyPairBlock` (Arc 2 — the literary pair-rationale block)
  - `IconicVerbChipRow` (Arc 2)
  - `D1VocabularyBar` (Arc 2)
  - `CatalogueFunnel` (Arc 3)
  - `VendorStackedBar` (Arc 3)
  - `ArchitectureDiagram` (Arc 4 — likely static SVG)
  - `RoleSubstrateMatrix` (Arc 4)
  - `StubCard` (used 3-5 times)
  - `HivePulseChart` (Arc 6 — depends on star-lord export)
  - `TeamManifestCard` (Arc 6 — static)
  - `FeaturedSprintCard` (Arc 6 — static)
- **Routing:** add `<Route path="/the-work" element={<TheWork />} />` (or chosen slug) to `App.tsx`; add `NavItem` in `Nav.tsx`
- **Page composition:** one `TheWork.tsx` page composing six sections; each section gets its own `Section{ArcName}.tsx` for code-locality (gandalf can review one section at a time in future iterations)
- **Data hook:** `useTheWorkData()` mirroring `useAnalytics()`; consume new JSON bundles per § 5
- **Mobile breakpoints:** `md:` for desktop transitions; nothing fancier
- **Smooth-scroll anchors:** `id="substrates"`, `id="vocabulary"`, `id="catalogue"`, `id="diversity"`, `id="journey"`, `id="hive"`; `scroll-behavior: smooth` already global in modern browsers
- **Optional desktop sidebar TOC:** `hidden lg:block fixed right-8 top-24 w-48` — implement only if time permits; not iteration-1 blocking

**What drax explicitly does NOT do tonight:**
- Build a full design system (Phase-3+)
- Import a serif font (defer — current sans is fine for iteration 1; arc-2 prose is *bigger and looser* but still sans)
- Build chart components from scratch when recharts versions suffice
- Add animations beyond Tailwind defaults
- Add a "share" button or social embed

---

## § 7 — Honest scope discipline

Iteration 1 is **first-pass**, not perfection. Three principles bind:

1. **Honesty over filler.** A stub card admitting a gap beats a fake chart hiding one. The page's credibility depends on it.
2. **Reuse over re-architecture.** Don't refactor `useAnalytics` tonight; pull from it. Don't rebuild charts; wrap them.
3. **Sectioned + scrolling, not paged + tabbed.** Mobile readers scroll. The DoE register is *vertical density.* Honor it.

**If wall-clock saturates,** ship arcs in this priority order: **2 (vocabulary) → 1 (substrates) → 4 (diversity) → 3 (catalogue) → 5 (journey) → 6 (hive).** Arc 2 alone earns the suite — the cosmological pair-rationale prose is the most under-exposed asset in the project. Don't ship without it.

**If any arc cannot ship,** ship a single section-stub-card naming the gap, with a one-line plan for iteration 2. The reader sees the **shape of the future suite** even when iteration 1 doesn't fill every section.

---

## § 8 — Cross-references

- `canonical/story/substrate-identity-declarations-2026-05-17.md` — Arc 1 source-of-truth
- `output/standard-demo-regen-2026-05-17/season_*/cosmological_vocabulary.json` — Arc 2 source-of-truth (per-season files)
- `agentic_orchestration/research/curated/` — Arc 3 source-of-truth (JSONL + DB)
- `reincarnated-loadout/src/hooks/useAnalytics.ts` — Arcs 1/4/5 partial existing wiring
- `reincarnated-loadout/src/pages/Analytics.tsx` — existing dashboard (untouched)
- `canonical/story/mobile-feel-target-doe-2026-05-17.md` — register canon
- `agentic_orchestration/galadriel/reference-images/MANIFEST.md` — visual reference set (post-impl, galadriel screenshots the deployed result for register coherence review)
- `agentic_orchestration/gandalf/requests/2026-05-18-knight-rider-mobile-playable-analytics-visual-benchmark-sprint.md` — invocation

---

## § 9 — Downstream signal (the unblock)

This IA's job is to unblock three dispatches:

1. `2026-05-18-star-lord-loadout-analytics-data-manifest-engine-side.md` — star-lord enumerates the engine-side bundles per § 5.1 above; resolves the unknowns (D1 corpus file location; hive-pulse export feasibility); produces `the-work-data.json` shape spec
2. `2026-05-18-elrond-loadout-analytics-data-manifest-catalogue-side.md` — elrond enumerates the catalogue-side bundles per § 5.2; resolves the funnel-numbers gaps; produces `the-work-catalogue-summary.json` shape spec
3. `2026-05-18-drax-loadout-analytics-suite-iteration-1.md` — drax implements per § 2/3/6 above, consuming the manifests from (1) and (2)

After drax pushes, galadriel (or stand-in) captures preview-URL screenshots per Track B deliverable 8.

---

*Authored 2026-05-18 overnight-sprint window by gandalf, per Track B § 2.2 deliverable 5. Iteration 1 IA; suite is six arcs scrolled; arc 2 is the gold; honesty over filler. Mithrandir signs.*
