# galadriel charge — B-1: Edition-III plate FURNITURE re-scale for fluid-width display + key rename (data geometry byte-frozen)

**From:** gandalf (SPEC-AUTHOR) · **Date:** 2026-07-16 · **Authority:** Matt 2026-07-16 (verbatim): *"Currently the app fits screen size and the "box" is zoomed appropriately, but the legends/descriptive sections/title/axis-title/axis itself are all still set to fill the "box" that has now grown. So, they need to fit the box as it is now."* + *"(and the condensations box should be re-named to "Build Families")"*.
**Ultra-think record:** `agentic_orchestration/gandalf/notes/2026-07-16-tier3-refit-and-polish-spec.md` §4.

## Context (why)

D7 made the glance `/atlas` route fluid: the plate that used to display at ≤1024px now displays at ~2528px on Matt's monitor — the SVG (1600×1200 viewBox) renders at scale ≈1.58 instead of ≈0.62. Every furniture element scales with it: the title (internal 26px) renders ~41px, pole titles (15) ~24px, key rows (11) ~17px. Matt approved the box growth; the furniture must now be re-proportioned for the plate at its new displayed size. This head also renders the upcoming Refit-Candidate-1 plates (workstream A) — both comparison plates must carry IDENTICAL furniture, so get this right once.

## The law: FURNITURE ONLY — data geometry byte-frozen

Fork `agentic_orchestration/galadriel/pipeline/atlas-edition3-render.mjs` → `atlas-edition3-r8-furniture-render.mjs` (series convention). Byte-frozen (identical output bytes): every data mark — live/condensation/graveyard point `cx/cy/r` + fills + hooks + `<title>` nodes, the **† tombstones at font-size 16** (the acceptance regexes at ~L1763/L2387 key on `font-size="16"` — do not touch), ring accents, hull polyline geometry, KDE terrain, drill-in dots, ghost speckle, zero-axis lines, frame rect geometry. The script's own FIT/acceptance blocks must still PASS.

Re-scaled (the furniture set — Matt's list):
- **Title block:** title 26 → target; RIDER banner text 13 + its band rect (y58 h30); derivation gloss 11.
- **Axis furniture:** pole titles (15) + glosses (~9.5) on all four poles incl. the two rotated rail titles; horizon labels; any tick/pole annotation text. Rail/zero-axis stroke-widths: your judgment — re-weight only if crops read heavy.
- **Condensation key (top-right of plane, ~L1380):** header + rows (11) + gloss rows (9.5) + swatch radii + the box rect (196w) hugging the shrunken content. **RENAME header `CONDENSATIONS` → `BUILD FAMILIES`.** Sweep for other USER-VISIBLE "condensation" strings in plate chrome (hover `<title>`/`<desc>` machine metadata may keep machine vocab; visible chrome renames).
- **Ghost plaque (420w), below-plane ledger, footer honesty block, points-denominator line, condensation anchor plaques (font 12 + rects; anchor/connector POSITIONS stay).**
- Boxes hug their shrunken text (Matt: "descriptive sections… fit the box") — plaque/band/key rect dims re-derive from content, positions stay in their bands.

## Target scale

At a 2560-wide viewport (display scale ≈1.58): title ≈24–30px rendered; key/ledger/legend/footer rows ≈12–14px; pole titles ≈14–18px; glosses/footnotes ≈10–12px. That's a global furniture factor ≈0.6–0.65 with per-class judgment — tune by eye with crops, don't apply blindly. Floor: still legible at a 1440 viewport (scale ≈0.88). Mobile relies on pinch-zoom (unchanged). The plate must also remain readable as a STANDALONE artifact at native 1600px.

## Acceptance + return contract

- Render BOTH skins (`archive`=dark lead, `instrument`=light — names inverted, ratified 2026-07-15) → new capture folder `2026-07-16-atlas-edition3-r8-furniture/` + re-emitted `render-provenance.json` (render stamp notes r8-furniture; skin_canvas_map unchanged).
- **Byte-frozen proof:** a diff receipt showing data-mark bytes identical old→new (your acceptance machinery already compares coord+title tuples — extend/report it), furniture-only deltas enumerated.
- Crop receipts at simulated display scales (2560 + 1440): title band, key (renamed visible), poles/rails, footer/ledger, plaque — both skins. Full-plate PNGs both skins.
- Do NOT touch glance/app (drax re-vendors in B-2). Do NOT touch any edition3 JSON. Auto-commit the collab repo. **NO push.**
- HALT: any data-mark byte diff you cannot eliminate · acceptance block failure · a furniture change that forces data-geometry movement.
