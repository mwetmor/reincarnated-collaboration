# galadriel charge — E2.2 plate relabel: "Build Horizon — Edition II" (Matt-ordered, presentation-text-only)

**From:** gandalf (SPEC-AUTHOR) · **Date:** 2026-07-15 · **Authority:** Matt 2026-07-15 ninth message (verbatim): *"the Atlas' name should be Build Horizon - Edition II (not Atlas of Kits)"* — this fires the E2.2 plate-vocabulary relabel that was registered at D1 (interactive spec Tracker-delta v1.2) and un-gates it NOW at Edition-II (it had been parked behind the Edition-III freeze; Matt's order supersedes the park — he is looking at the Edition-II PRD surface today).

## Scope — ONE change class, frozen everything else

Re-render the Edition-II atlas (BOTH skins) with the plate title changed:

- **Old:** `The Atlas of Kits — Edition-II`
- **New:** `Build Horizon — Edition II`

(Matt typed `Build Horizon - Edition II`; house style keeps the em-dash the artifact family already uses. "Edition II" unhyphenated in the TITLE exactly as Matt typed it; the hyphenated `Edition-II` machine-form stays untouched in the provenance strip, footer line, and JSON fields.)

This is the **E2.1 fix-pass class**: presentation text on frozen data. Positions, geometry, dot classes, condensation key, axis poles, provenance DATA, denominators — all byte-logic untouched. Renderer: `agentic_orchestration/galadriel/pipeline/atlas-edition2-r7-render.mjs` lineage (amend the title constant; re-run; if the E2.1 pass layered on r7, use whichever script is your current head for the vendored artifacts — the vendored footer says `emitted 2026-07-15T19:20:12` / `skin=instrument`, so match THAT pipeline head).

## Deliverables

1. `atlas-edition2-instrument.svg` + `atlas-edition2-archive.svg` + provenance JSON re-emitted to your capture home (`agentic_orchestration/galadriel/captures/2026-07-15-atlas-edition2-e22/` or your convention) — with sha256 receipts in the return summary.
2. Verify in-artifact: title reads `Build Horizon — Edition II` on both skins; diff-class receipt that ONLY title text (+ emission timestamp/provenance fields) changed vs the current vendored copies at `~/Games/reincarnated-loadout/public/atlas/` — e.g., a normalized diff or element-count/geometry-hash comparison. Fail-loud if anything beyond the title + emission metadata moved.
3. Auto-commit to collab repo (in-scope render artifacts). NO push. NO vendoring into loadout — that is drax's D6-d step; your return summary names the exact paths for drax.

## Return contract

Summary names: the two SVG paths + provenance path, sha256s, the diff-class receipt (title-only change), and both title renders eyeballed (attach or name your check crops). Any surprise (renderer head mismatch, data drift since the vendored emission, >title diffs) → HALT and surface, do not improvise.

**Signed:** gandalf — operationalizing Matt's 2026-07-15 relabel order; drax D6-d consumes your output (interactive spec §9.6).
