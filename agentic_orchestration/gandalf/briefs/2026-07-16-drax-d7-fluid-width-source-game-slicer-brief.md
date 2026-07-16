# drax charge — D7: glance `/atlas` host fluid width + SOURCE GAME slicer (ONE pass, STOP at preview)

**From:** gandalf (SPEC-AUTHOR) · **Date:** 2026-07-16 · **Authority:** Matt 2026-07-16 live-PRD report (verbatim): *"on loadout, the width of the entire app fits my browser screen, but on glance it stays at about 50% of screen width. Also, since we're doing a bit of work, could we have one more slicer/filter added to the table called 'source game'?"*
**Context:** the v1.12 port is VERIFIED + PROMOTED — glance PRD serves Edition III; loadout `/atlas` is a live redirect. This is the first live-PRD fix-pass on the new home. Contract: `agentic_orchestration/operating-procedures/glance-contract-spec-2026-07-03.md` §7.8; package spec `agentic_orchestration/gandalf/notes/2026-07-15-atlas-interactive-glance-spec.md` (read §9.7 — it binds two things on THIS pass, see D7-c).

## D7-a — host fluid width on the `/atlas` route ONLY (gandalf-diagnosed, host-level D1-f)

Root cause found: the ported instrument is internally fluid (D1-f), but the glance HOST clamps every page — `glance/app/src/App.tsx:106` `<main className="mx-auto max-w-5xl px-3 pb-24 pt-4 sm:px-4">` (1024px ≈ 50% of Matt's monitor). Loadout's shell was fluid; that's the delta Matt sees.

- Make the `<main>` width **route-conditional**: on the `/atlas` route the page goes FLUID (full browser width, sensible horizontal padding); **every other glance page keeps `max-w-5xl` exactly as-is** (D1-f law: this route only).
- The Tier-0 header band (the `max-w-5xl` container at ~`App.tsx:133`) — if a fluid main under a narrow centered header reads as two different surfaces, you may align the header band to the same route-conditional width; if the wide header tiles read sparse/bad, cap sensibly. Your call within "the atlas page reads as ONE full-width surface" — surface the choice + a screenshot.
- 375/mobile behavior unchanged (the clamp only binds ≥1024px). The error page `max-w-2xl` (~L87) untouched.

## D7-b — SOURCE GAME slicer joins the filter grammar

New filter control labeled **SOURCE GAME** alongside AXIS-X · AXIS-Y · ENTITY · LIVENESS · FAMILY:

- **Dropdown** (FAMILY precedent — cardinality 19), options = distinct `game` values from the slim JSON (`kits[].game`, coverage 506/506 — already there, ZERO data/builder changes needed; gandalf-verified: 19 slugs, no `diablo-4`/`d4` dupe) + **All** default.
- **Display names, not slugs:** options render through the SAME game display-name path the leaf rows already use for `folk_name — Game Year` (e.g. `chronicon`→Chronicon, `d2`→D2, `poe1`→whatever the existing formatter emits). If no shared formatter exists, extract ONE (leaf rows + dropdown consume it — no second mapping). Sort: alphabetical by display name (count badges optional — your call, state it).
- **Same pipeline, no special case:** composes AND with the existing filters and drives table rows AND the chart lens/halo through the existing filter→lens path (D3 law). Ghost entities carry no `game`: the slicer binds build-class rows only; with ENTITY=Ghosts it is inert — state (and test) the inert behavior; don't invent a ghost-game.
- Suite: extend for the new predicate (compose + inert cases); existing 98 stay green.

## D7-c — the probe hardening rides this pass (spec §9.7, owed)

You're re-probing anyway; fix the two §9.7 findings in `scripts/atlas/d6-verify-probe.mjs` first:
1. **Flip-wait = wait-for-CHANGE:** poll until plate fill (or skin attr) DIFFERS from pre-click, fail-loud on timeout — never break on "an svg exists" (the old skin satisfies that instantly; it silently re-measured dark as "1440-light" in the v1.12 pass).
2. **Selector by CANVAS label:** find skin controls by `Dark`/`Light` label + `aria-pressed`, never by skin name (`archive`=dark lead, `instrument`=light — inverted names, ratified 2026-07-15).

## Acceptance + return contract

- Build + full suite green; previews UP (state URLs/commands).
- **Occlusion re-verify at the NEW geometry:** fluid width moves the region/legend — the v2 occlusion law (zero in-artifact `<text>` bbox intersections ±4px, both skins) re-runs with the hardened probe at **1920 AND 2560** (the widths this pass exists for) + 1440 + 1280 + 375. Receipts JSON. If any wide placement fails: HALT-don't-shrink, surface.
- Fluid-width receipt: full-page screenshot at 2560 (or widest you can emulate) — atlas fills the browser width; plus one NON-atlas page screenshot proving `max-w-5xl` held there.
- Slicer receipts: dropdown screenshot (display names visible); a filtered receipt (e.g. SOURCE GAME=D2 → row count 59, halo follows); inert-with-Ghosts receipt.
- Diff receipt enumerated · judgment calls surfaced · auto-commit collab repo. **NO push. NO PRD deploy, NO alias move — verify gates promotion (standing chain).**

## HALT conditions

Anything server-side/LLM/parser → HALT · occlusion unsatisfiable at wide widths → HALT · route-conditional width forces non-mechanical rewrites of other pages → HALT with the finding.

**Signed:** gandalf — operationalizing Matt's live-PRD width report + slicer order; my verify gates promotion.
