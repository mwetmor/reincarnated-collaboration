# drax charge — B-2: re-vendor R8 plates + clickable legend → TOP-LEFT plane seat (D6-b v2 law, v3 seat) — ONE pass, STOP at preview

**From:** gandalf (SPEC-AUTHOR) · **Date:** 2026-07-16 · **Fires after:** galadriel B-1 (r8-furniture plates) lands.
**Authority:** Matt 2026-07-16 (verbatim): *"Lastly the clickable legend should fit inside the box on the upper-left-hand side, opposite to the 'Condensations' box (and the condensations box should be re-named to 'Build Families'."*
**Ultra-think record:** `agentic_orchestration/gandalf/notes/2026-07-16-tier3-refit-and-polish-spec.md` §4. Package spec: `agentic_orchestration/gandalf/notes/2026-07-15-atlas-interactive-glance-spec.md` (§9.6 D6-b, §9.8).

## Scope facts (gandalf recon)

- The "Condensations box" = the **in-SVG condensation key, top-right of plane** (`lx = M.left+PW−190, ly = M.top+14`). Its rename to `BUILD FAMILIES` is galadriel's B-1 (already charged). Your clickable `AtlasLegend` already says "Build Families" (D1-i vocabulary) — **no HTML rename owed**; verify the rendered R8 plate shows the renamed key and your legend vocabulary agrees.
- "Opposite" therefore = **top-LEFT of plane, INSIDE the chart region** — the mirror seat of the key.

## B2-a — re-vendor the R8 plates

Galadriel's B-1 output: `agentic_orchestration/galadriel/captures/2026-07-16-atlas-edition3-r8-furniture/` (both skins + re-emitted `render-provenance.json`). Re-vendor through your established pipeline (captures → build inputs → `public/atlas/`), and update `.vercelignore` un-ignore paths if the capture folder path changed (D7 lesson: the un-ignored build inputs currently point at `2026-07-16-atlas-edition3/` — verify the deploy context carries whatever the build actually reads; state what you did).

## B2-b — legend seat: bottom-right → top-left (v2 law, v3 seat)

`glance/app/src/components/atlas/AtlasLegend.tsx`:

- **Law unchanged (D6-b v2):** the overlay may intersect the screen-space bbox of NO in-artifact `<text>` node (±4px pad) and no drill-in dot, both skins. Only the SEAT moves.
- Top-left interior contents to clear (post-R8 geometry — probe, don't assume): the title/banner/gloss band sits ABOVE the plane in the top margin; the rotated PERFORM/DEPLOY rail titles hug the left rail edge; condensation anchor plaques + horizon labels may reach the upper-left interior. Derive the seat empirically: top offset clearing the title band, left offset clearing the rail titles — **fraction-anchored, not magic px** (the 14.5% width-cap discipline carries: the panel and the plate text both scale with the region, so fractional insets/caps hold at every width).
- Re-derive the width cap against the top-left text landscape (the old 14.5% was derived against the bottom-right points-denominator tail — that constraint no longer binds; a new one may).
- **Mobile (375):** chip starts collapsed (unchanged); the bottom-[23%] seat was tuned for bottom-right — re-derive the ONE lawful top-left chip seat at 375 by probe (44px touch-target floor is an a11y invariant, never shrunk; if no lawful top-left seat exists at 375 → HALT + surface, don't silently shrink or drop).
- Rewrite the component's seat-law comment block as v3 (top-left), preserving the v2 occlusion-law text.
- While in the probe: retire stale vocabulary in `scripts/atlas/d6-verify-probe.mjs` legend-detection regexes (`Live Kits|Condensations` → current labels `Build Families|Live Builds`) — detection must not depend on retired strings.

## Acceptance + return contract

- Build green + full suite green (extend/adjust any test asserting legend placement).
- **Occlusion re-verify at the NEW geometry** (R8 furniture + v3 seat): hardened d6 probe (wait-for-CHANGE flip, canvas-label selector) at **2560 / 1920 / 1440 / 1280 / 375 × both skins** — zero text-bbox intersections ±4px. Receipts JSON. Any failure: **HALT-don't-shrink**, surface the finding.
- Screenshots: top-left legend expanded (desktop, both skins), collapsed chip at 375, one full-page 2560 shot showing legend top-left + renamed BUILD FAMILIES key top-right reading as opposites.
- Preview deploy UP (state URL/command). Diff receipt enumerated · judgment calls surfaced · auto-commit collab repo. **NO push. NO PRD deploy, NO alias move — gandalf's verify gates promotion (standing chain).**

## HALT conditions

No lawful top-left seat at any verify width → HALT with probe evidence · R8 plates missing/failed acceptance → HALT · anything touching parser/server/LLM → HALT.

**Signed:** gandalf — my verify gates promotion.
