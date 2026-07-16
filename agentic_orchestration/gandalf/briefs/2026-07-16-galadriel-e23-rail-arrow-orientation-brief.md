# galadriel charge — E2.3 rail-arrow orientation: DEPLOY/PERFORM arrows point OUTWARD on screen (Matt-ordered, presentation-text-only)

**From:** gandalf (SPEC-AUTHOR) · **Date:** 2026-07-16 · **Authority:** Matt 2026-07-16 (verbatim): *"Please just make the arrows next to the axes of Perform and Deploy point outwards, rather than up and down."*

## Ground truth (gandalf probe of the vendored artifacts)

Both west/east pole labels are ROTATED text: `<text transform="rotate(-90 54.00 618.00)" …>← DEPLOY</text>` and `<text transform="rotate(-90 1546.00 618.00)" …>PERFORM →</text>`. Under `rotate(-90)` (SVG y-down), a local `←` renders screen-DOWN and a local `→` renders screen-UP — Matt's "up and down" report, exactly. The glyphs are right in the string, wrong on screen.

## Scope — ONE change class (E2.1 fix-pass lineage), frozen everything else

Re-render the Edition-II atlas (BOTH skins) with the two rotated rail-label arrow glyphs swapped so the ON-SCREEN arrows point OUTWARD:

- West rail: arrow must READ `←` on screen (pointing left, away from the plane). Under rotate(-90) the glyph that does this is `↑` → string becomes `↑ DEPLOY`.
- East rail: arrow must READ `→` on screen (pointing right, away). Under rotate(-90) that glyph is `↓` → string becomes `PERFORM ↓`.

The math is my derivation — **your EYES are the acceptance**: check crops of both rails, both skins, must show arrows pointing outward (left on the left rail, right on the right rail). If the glyph-under-rotation approach reads badly (font renders the vertical arrows poorly, spacing off), you MAY instead split the arrow into its own small non-rotated `<text>` sibling positioned beside the rotated word — that is a structure change, so surface it as a judgment call in the return. Add a one-line comment in the renderer explaining WHY the source glyph differs from the on-screen direction (the rotate(-90) mapping) so no future pass "fixes" it backwards.

**Untouched:** `↑ LAUNCH` / `EMBODY ↓` (north/south, horizontal, already outward). Positions, rotations, geometry, dot classes, condensation key, footer/provenance DATA, denominators — all byte-logic frozen. Renderer: your current E2.2 head (the one that emitted the vendored `Build Horizon — Edition II` artifacts).

## Deliverables

1. Both SVGs + provenance JSON re-emitted to your capture home (`agentic_orchestration/galadriel/captures/2026-07-16-atlas-edition2-e23/` or your convention) with sha256s in the return.
2. Diff-class receipt vs the vendored copies at `~/Games/reincarnated-loadout/public/atlas/`: ONLY the two rail-label text elements (+ emission timestamp/provenance metadata) changed per skin — element-count/geometry-hash comparison; fail-loud on anything else.
3. Check crops: both rails, both skins, arrows visibly outward.
4. Auto-commit to collab repo. NO push. NO vendoring into loadout — drax consumes; your return names the exact paths.

## Return contract

Paths + sha256s + diff-class receipt + crop paths + on-screen-direction confirmation per rail per skin. Any surprise (renderer head mismatch, more-than-two-element diff, ambiguous arrow rendering) → HALT and surface.

**Signed:** gandalf — operationalizing Matt's 2026-07-16 rail-arrow order; drax's next pass consumes your output.
