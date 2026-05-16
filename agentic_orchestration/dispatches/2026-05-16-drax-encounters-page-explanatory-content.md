# Dispatch — 2026-05-16 — drax — Encounters page: definitions, legends, and explanatory content

**From:** knight-rider
**To:** drax (presentation seam — reincarnated-loadout)
**Approved by:** Matt at 2026-05-16 (Day 4 open — after Matt reviewed v0.7 screenshots and asked for reader-friendly explainer content)
**Status:** COMPLETE
**Estimated effort:** 1 session (~2-3 hours; UI iteration with content authoring, no new data wiring)
**Acceptance:** Encounters page is self-explanatory to a reader who hasn't been in the design conversation — axis meanings, color semantics, ellipse semantics, view-toggle purpose, and the "what to look at" framing all surfaced inline; no scrolling-back to top legend required for individual-card interpretation.

## Context — why this exists

Matt reviewed the v0.7 encounter-analytics screenshots (in `~/Games/reincarnated-collaboration/reference_screenshots/`, 2026-05-16). His feedback summary: "some of it doesn't have legend labels so I feel a bit lost." The page is doing genuine analytical work — multi-dimensional centroid + stdev ellipse projections across (class × encounter-slot) pairs, two view orientations, divergence-ceiling flagging — but the legends are top-of-page only, and the visual encoding density requires a guided read.

Knight-rider's analytical read on the screenshots (sent to Matt inline) covered:
- Three projection axes (X = Avg Damage, Y = Win Rate, ellipse size = variance with formula `rx = σ(damage), ry = √(WR × (1−WR)) × scale`)
- Color legend semantics (Swarm / Magic / Trash / Elite / Mini-Boss / Boss + WR<25% red flag)
- The two view orientations (Per-class vs Per-encounter-slot)
- Six data-pattern findings (vertical stacking; Swarm floor failures; AOE% correlation; orange Swarm cluster top; magic/trash near 100%; boss/mini-boss spread)
- Three carry-forward signals (divergence ceiling violated almost universally; vertical stacking confirms WR-doing-the-work; class_0011 as outlier worth investigation)

This dispatch asks you to fold a substantive subset of that explanatory framing into the page itself — so future readers (Matt or anyone else) don't need a guide alongside the viz.

## What to add — explanatory content surfaces

### Surface 1 — Persistent axis + ellipse legend per card or per-row

Currently the X-axis ("Avg Damage →") and Y-axis (0%/50%/100% gridlines) are labeled per card, but **what those axes MEAN at the project level is not on the card.** Add a small legend either:

- **(a)** As a permanent compact strip immediately above each card row (one strip per row of cards), or
- **(b)** As a small hover-revealed tooltip on a `?` icon near each card's title, or
- **(c)** As a sticky mini-legend that scrolls with the user as they scroll through the small-multiples grid.

Whichever lands cleanest in your UI judgment. Pick one; don't add all three.

Required legend content per card-region:
- **X = Avg Damage dealt** (per-fight average for that (class, monster) pair across all fights run)
- **Y = Win Rate** (0–100%; fraction of fights won)
- **Each point = one (class × encounter-slot) pair in this view; ellipse shows variance**
- **Ellipse: `rx = σ(damage)` (wider = damage was inconsistent across fights); `ry = √(WR×(1−WR)) × scale` (taller = outcome was uncertain — binomial variance)**

The exact wording is yours — these are content guidelines, not copy.

### Surface 2 — Color legend made always-visible OR repeated per row

Currently the color legend (Swarm / Magic / Trash / Elite / Mini-Boss / Boss / WR<25%) lives only at top of the page. Readers scrolling past the third row lose it. Options:

- **(a)** Make the color legend sticky (CSS `position: sticky; top: 0`)
- **(b)** Repeat it at top of each row of cards (visual cost: more chrome; benefit: never lost)
- **(c)** Render color swatches on each card's points/ellipses with a small inline legend in card chrome

Pick whichever is cleanest visually — sticky is probably the lowest-effort highest-clarity option for the per-class view. **For the per-encounter-slot view (screenshot #3 at 9.37.35 AM), the coloring switches semantics: each color is a CLASS, not an encounter type.** The legend needs to update accordingly — when the user toggles to per-encounter-slot view, the legend now reads `class_0001 / class_0002 / …` with the class colors. Make sure both views' legends are clearly distinguished so the user doesn't read encounter-type colors when actually looking at class colors.

This is the **single most important fix** in the dispatch. The view-toggle changes color semantics; the page should make that switch obvious.

### Surface 3 — "How to read this" explainer at top of page

A collapsed-by-default expandable panel at the top of the Encounters page (under the title, above the view-toggle) titled something like "How to read this" or "Reading guide." Inside, a structured walkthrough:

1. **What this page shows:** Each card visualizes how one class performs against every encounter slot the simulation tested (or, in the alternative view, how every class performs against one encounter slot).
2. **The data:** Per-fight aggregates from `season_001005` telemetry. Each (class × monster) pair is one point with an ellipse showing damage and outcome variance.
3. **What "good" looks like:** Differentiated archetype shapes — points spread *across* damage values within each card, win rates clearly above the 25% floor on every encounter slot, and AOE classes showing high WR on Swarm slots while non-AOE classes still hold a playable floor.
4. **What "bad" looks like:** Vertical stacking (damage barely varies across encounters — classes win or lose without speed differentiation); horizontal red-flagged ellipses below 25% WR (a divergence-ceiling failure — that class has a helpless matchup); boss/mini-boss clusters showing zero spread across classes (high-tier encounters that brick or trivialize uniformly across the roster).
5. **Important caveats:** Tier-1 columns (duration, heals, potions) are NULL for `season_001005` rows; this is why X is currently Avg Damage rather than Damage × TTK. Pack encounters are shown for diagnostic but are excluded from the convergence binary search (per Option 2 / B10.4).
6. **View A interpretation (locked 2026-05-16):** [The existing DESIGN INTERPRETATION callout you already have. Leave that in place; it's good. Just make sure its connection to the "How to read this" panel is clear — the View A callout is the *analytic frame*; the reading guide is the *mechanical frame*.]

Style this panel as collapsible (HTML `<details>` element or a custom React expandable) so it doesn't dominate the page for repeat readers — but visible by default on first page-load.

### Surface 4 — Per-card AOE % subtitle context

The AOE % subtitle on each per-class card (e.g., `class_0001 / AOE 54%`) is informative but uncontextualized — a reader doesn't know whether 54% is high, low, or median. Add either:

- **(a)** A small inline note on the per-class view (top of card grid) — "AOE % = fraction of class's skill kit that produces area damage; roster range in `season_001005`: 18% to 54%"
- **(b)** Hover-revealed tooltip on the AOE % subtitle showing the roster distribution
- **(c)** Color-code or otherwise visually distinguish high-AOE vs low-AOE classes (e.g., subtle background tint) so the AOE→Swarm-WR correlation is visually surfaced

Pick whichever is cleanest. **Option (a) is the lowest-effort and probably sufficient.**

### Surface 5 — View-toggle labeling clarity

The current view-toggle (`Per-class` / `Per-encounter-slot` buttons) is clear in meaning but could benefit from a subline explanation:

- **Per-class view:** "Each card is one class; points show its performance across all 22 encounter slots."
- **Per-encounter-slot view:** "Each card is one monster; points show all 11 classes' performance against it."

Either inline under the buttons, or as tooltip-on-hover.

### Surface 6 — "What's pending" honesty line

The Tier-1-pending note in the page header is good but small. Consider promoting it slightly so readers understand the projection switch is a near-term change:

> *Tier-1 telemetry fields (duration, heals, potions) are pending the next Yomi regen. Once those land, the X-axis will switch from Avg Damage to a Damage × Time-to-Kill projection that better captures class efficiency. Until then, treat damage values as directional and prefer Win Rate as the primary signal.*

You can keep the existing red-tinted note styling; just expand the text slightly.

## Out of scope

- **New data wiring.** This dispatch is content/UI only — no new fields, no new telemetry queries, no JSON regeneration. If something needs new data to be fully explanatory, flag in completion record but don't ship it here.
- **Algorithmic changes to the viz.** Centroid + stdev ellipse semantics are correct as-is per gamora B10.4 Option 2 and the View A lock. Don't change the math.
- **Re-cutting tags.** The `drax/v0.7-encounter-analytics` intermediate tag stays. This dispatch produces an *additive* intermediate tag (e.g., `drax/v0.7-encounter-analytics-legends`) when complete. The milestone tag `v0.7-encounter-analytics` is currently HELD by Matt and stays held until knight-rider confirms.
- **The other analytics charts** (StatRadarChart, SeasonTimelineChart, SkillTierChart from v0.6.5). Those are separate; if Matt asks for explanatory content there in the future, that's another dispatch.

## Required reading before starting

- Your own `~/Games/reincarnated-loadout/AGENT_STATE.md` v0.7 section
- `~/Games/reincarnated-loadout/src/pages/Encounters.tsx` (your existing impl — the existing DESIGN INTERPRETATION callout shows you've already wired this kind of explanatory content; this dispatch extends that pattern)
- `~/Games/reincarnated-loadout/data/encounter_analytics.json` (the data the page renders — confirms what fields exist for tooltip content)
- `agentic_orchestration/skill_handoff_2026-05-16.md` § Day 4 open (for the milestone-tag hold context — important for tag intent)
- Knight-rider's analytical read on the screenshots (in this Day 4 session transcript — you can ask Matt to forward it if needed; it's the reference for "what reader-friendly framing looks like at the right depth")

## Acceptance criteria

- [ ] Surface 1 (axis + ellipse legend per card region) implemented
- [ ] Surface 2 (color legend made always-visible + view-toggle color-semantics switch handled clearly) implemented
- [ ] Surface 3 (How to read this expandable panel at page top) implemented
- [ ] Surface 4 (AOE % context) implemented
- [ ] Surface 5 (view-toggle subline labels) implemented
- [ ] Surface 6 (Tier-1 pending honesty line expanded) implemented
- [ ] `npm run build` clean (0 errors)
- [ ] Visual smoke: both views render correctly; legends update on view toggle; expandable panel opens/closes cleanly
- [ ] Vercel preview deployed
- [ ] Intermediate tag cut: `drax/v0.7-encounter-analytics-legends` (or similar — your call on tag-slug)
- [ ] AGENT_STATE.md updated with the new tag and surface list
- [ ] Knight-rider notified at completion with preview URL

## Open questions for drax to resolve

- Which surface-1 option lands cleanest (sticky strip vs hover icon vs scrolling mini-legend)? Your UI judgment.
- Which surface-2 option lands cleanest (sticky vs per-row repeat vs inline-on-card)? Your UI judgment.
- Is there a way to make the View A DESIGN INTERPRETATION callout's connection to the reading-guide explainer more explicit without merging them? They serve different audiences (analytic vs mechanical) — keep them distinct but cross-referenced.

## References

- `canonical/story/engine-balance-stewardship.md` (View A locked context)
- `reincarnated-engine/design/decisions/decisions-log.md` 2026-05-16 entries (View A + B10.2 supersession — the analytical frame the page is rendering against)
- `reference_screenshots/Screenshot 2026-05-16 at 9.37.10 AM.png` etc. (Matt's 2026-05-16 reference set; the visual state this dispatch is responding to)

---

## Completion record

**Completed:** 2026-05-16 (drax)
**Preview URL:** https://reincarnated-loadout-1tj6lewiv-matthew-wetmore-s-projects.vercel.app
**Intermediate tag:** `drax/v0.7-encounter-analytics-legends` (commit 3f2fca6)
**Surfaces shipped:**
- Surface 1 ✓ — `AxisLegend` component: compact strip above each card grid; X = avg damage dealt, Y = win rate, ellipse width = σ(damage) (inconsistency), ellipse height = √(WR×(1−WR)) (outcome uncertainty)
- Surface 2 ✓ — View toggle + color legend grouped in a `sticky top-0 z-10 bg-gray-950` block; legend updates on view toggle: encounter-type colors in per-class view, class colors in per-slot view; subline next to toggle makes the semantics switch explicit ("color = encounter type" vs "color = class")
- Surface 3 ✓ — `<details open>` expandable "How to read this" panel before the View A callout; 6 structured items covering what/data/good/bad/caveats/analytic-frame; references the Design Interpretation callout as the "analytic frame" to this "mechanical frame"
- Surface 4 ✓ — AOE % roster range note above per-class grid: "AOE % = fraction of class's skill kit that produces area damage · roster range in season_001005: 18% to 54%"
- Surface 5 ✓ — View-toggle subline description rendered inline next to buttons; updates reactively on toggle (class vs slot view descriptions)
- Surface 6 ✓ — Tier-1 pending note expanded from inline span to full paragraph: "treat damage values as directional and prefer Win Rate as the primary signal"
**Notes for knight-rider:** All 6 acceptance criteria met. Build clean (0 TS errors, 686 modules). Milestone tag `v0.7-encounter-analytics` was on hold per dispatch — still held; this intermediate tag covers the legend work. Recommend Matt review preview before milestone tag cut.
