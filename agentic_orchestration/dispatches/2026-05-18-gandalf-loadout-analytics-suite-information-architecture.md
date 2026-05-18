# 2026-05-18 — gandalf — Loadout analytics suite information architecture (Track B.5; sprint critical-path BLOCKER)

**Authority:** Overnight sprint invocation `agentic_orchestration/gandalf/requests/2026-05-18-knight-rider-mobile-playable-analytics-visual-benchmark-sprint.md` Track B § 2.2 deliverable 5; pre-authorization matrix § 6 row 11.
**Type:** Pattern B; ~2 hours estimated.
**Status:** 🟢 **ACTIVE — first work item of the sprint; downstream consumers (star-lord, elrond, drax) blocked until this lands.**
**Tag intent:** none (canonical-story doc; gandalf authorship).

---

## Why this is the critical path

The loadout analytics suite (Track B) is the *value-story* deliverable of tonight's sprint. Three downstream consumers wait on the IA:
- **star-lord** and **elrond** co-author the data manifest — they need to know which panels they're sourcing data for before they survey what exists
- **drax** implements iteration-1 components — needs IA to know route structure, panel layout, visual register
- **galadriel** (deferred-agent-creation; work happening via knight-rider orchestration) screenshots the result — needs to know what to look at

Without gandalf IA first, the other three seams produce work that misaligns. With gandalf IA first, the three downstream seams parallelize cleanly.

---

## Required reading

1. The full invocation (above) — especially § 2.2 (Track B deliverables) + § 0 TL;DR (B context)
2. `canonical/story/canonical-elements-one-pool-2026-05-17.md` — substrate set; D1 vocabulary distribution
3. `canonical/story/substrate-identity-declarations-2026-05-17.md` — the 7 declarations the suite visualizes
4. `canonical/16-project-roadmap.md` — B-series roadmap; what the engine has actually shipped
5. `agentic_orchestration/research/curated/` — quick listing to know what catalogue work has produced
6. Loadout app structure: `~/Games/reincarnated-loadout/src/` — existing routes, components, design language; the analytics suite extends this idiom
7. Engine output: `~/Games/reincarnated-engine/output/` — what season artifacts exist; this is the source of substrate / archetype / vocabulary data
8. `canonical/story/mobile-feel-target-doe-2026-05-17.md` § for typography + register direction hints
9. `agentic_orchestration/galadriel/reference-images/MANIFEST.md` — DoE register canon (the analytics suite typography should not clash with the demo's emerging visual identity)

---

## Deliverable

A new canonical-story doc at `canonical/story/loadout-analytics-suite-information-architecture-2026-05-18.md`.

### Required sections

**1. Story arcs the suite tells.** Per invocation § 2.2 suggested arcs (refine, prune, or add):
- The substrate journey — canonical-4 → canonical-7 expansion visualized; per-substrate season counts; per-substrate archetype shapes
- The LLM thematic universe — D1 vocabulary corpus (allow-list / eligible / quarantine; ~156 entries); per-substrate vocabulary coverage; iconic-verb representation; example LLM-generated season titles + descriptions
- The catalogue — Legolas crawl coverage; Elrond curation throughput; per-vendor asset counts; what made it to the demo
- The diversity architecture in action — archetype mechanical-signature visualization; role × substrate composition matrix; spirit-swap differentiation evidence
- The journey across seasons — season-to-season cohesion metrics; perception-test signal once available; Earth Self / Court of Forms preview
- The work behind the work — agentic team contributions visualized; commits-per-seam; dispatches-by-purpose; the hive at scale

For each arc gandalf retains, name:
- **What the panel says** (one-sentence headline that a Matt-on-his-phone reads and gets)
- **What data it consumes** (which engine files / research artifacts / dispatches / commits)
- **What visualization carries it** (chart type — bar / radar / chord / table / image-grid / etc.; gandalf can keep this loose, drax will pick implementations)
- **Phase-1 vs Phase-2** disposition — first-night iteration-1 includes a subset; the rest queue. Be honest about which arcs lack the data tonight.

**2. Route + page structure.** Single-page or sectioned. If sectioned, what is the navigation? What is the landing surface? What is the visual hierarchy on first scroll?

**3. Visual language guidance.** Typography register, color palette pointers, density (DoE's HUD-busy register vs. analytics-page-readable register), iconography. Drax doesn't need a full design system; he needs enough register guidance to not clash with what the demo is becoming.

**4. Phase-2 placeholders.** Panels that should exist but for which data isn't there tonight. Mark them and recommend a backlog disposition.

**5. Data-source manifest seed.** Per panel, one line on what data star-lord and elrond should look for. Star-lord and elrond will produce the full manifest; gandalf seeds it.

---

## Out of scope

- Drax implementation guidance beyond visual register (drax picks components)
- Full design-system authorship (this is iteration-1; full system is later)
- Engine-side telemetry schema authorship (star-lord's job; gandalf only requests fields)
- Catalogue-DB schema authorship (elrond's job)
- Vercel deployment specifics (drax + star-lord § 2.4 work)
- Track A or Track C scope
- Modifying any canonical-story doc OTHER than authoring the new IA doc

## Out-of-scope (pre-authorization HARD NOs honored)

- No load-bearing canonical-doc amendments (this is a new doc; new docs are pre-authorized per § 6 row 11; amendments to existing load-bearing docs are L3-queue)
- No Phase-1 P1 scope changes
- No vendor acquisitions

---

## Completion criteria

- Doc lives at `canonical/story/loadout-analytics-suite-information-architecture-2026-05-18.md`
- All 5 required sections present
- Hive-log STATE entry (§ 14.1.1 PRE-SIGNAL discipline) announcing IA landed with link to the doc
- The 5 story arcs Phase-1/Phase-2 disposition is honest — if the data isn't there, gandalf says so; iteration-1 ships what IS there

## Downstream signal

Once this lands, knight-rider fires:
- `2026-05-18-star-lord-loadout-analytics-data-manifest-engine-side.md`
- `2026-05-18-elrond-loadout-analytics-data-manifest-catalogue-side.md`

And once those land, knight-rider fires:
- `2026-05-18-drax-loadout-analytics-suite-iteration-1.md`

The critical-path DAG is per invocation § 7.

---

*Dispatched 2026-05-18 evening by knight-rider per overnight sprint invocation Track B § 2.2 deliverable 5. Single-night sprint cadence; § 14.1.1 PRE-SIGNAL discipline applies to all hive-log commits.*
