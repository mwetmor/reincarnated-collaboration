# Drax iteration 1 — connected-descent MOOD LIFT pass (lit better + looking like the theme)

**Type:** direct gandalf→drax iteration brief (autonomous; Matt away; Matt-authorized 2026-06-15 — *"all connected, lit better and looking like the …/modular_asset_idea_pictures theme"*).
**Date:** 2026-06-15
**Author:** gandalf (story-and-design steward)
**Parent:**
- `agentic_orchestration/gandalf/notes/2026-06-15-drax-brief-connected-descent-scene.md` — the original build brief (Drax DELIVERED: `scenes/arena_descent.tscn`; parity proven; 6 zones connected; per-zone color progression).
- Reference art: `~/Games/reincarnated-godot/Assets/Synty/polygon-dark-fantasy-01/modular_asset_idea_pictures/maps/` + `/theme/` — esp. `maps/Screenshot 2026-06-15 at 8.36.17 AM.png` (the calibration image).

---

## 0. What landed (Drax's build) + what this pass closes

Structure is DONE and CORRECT: 6 connected zones, descent ordering right, **spawn-position parity PROVEN** (spawns == spec across all 35 / 6 zones), per-zone color progression reads (threshold / arcane / warhall-warm-dense / oubliette / antechamber-green-soulfire / sanctum-red-bloom+magenta). That is the load-bearing half of "all connected." ✓

This pass closes the gap between the current look and the reference theme. My calibrated read (current per-zone frames vs `maps/8.36.17`):

- **Reference = DARK-with-vivid-colored-light:** a luminous GREEN atmosphere rising from the ground, golden brazier/lantern points that POP, dense gothic dressing (tombs/statues/crates/bones packed in), deep shadows.
- **Current = dim-grey-with-some-warm-points:** teal VOID background (not a glowing green atmosphere), flat grey stone floor dominating the frame, warm fires punching only in zone 2 (warhall).

## 1. Three concrete fixes (ALL presentation levers — spawn POSITIONS sacrosanct; re-verify parity after)

**Fix 1 — Remove the magenta-square artifact (sanctum / zone5 floor, foreground).** A flat saturated magenta panel sits on the sanctum floor. It reads as a placeholder / portal-pad / raw-emissive, NOT dark-fantasy (nothing in the reference looks like a flat geometric magenta square). Identify the node and either remove it or restyle it to a real dark-fantasy arcane decal at sane intensity. It must not survive as a flat saturated magenta square.

**Fix 2 — Global atmosphere lift toward vivid green + DARKEN the floor.** The reference's signature is luminous green glowing from the ground with deep shadows; the current WorldEnvironment reads as a dark teal void and the grey floor is too uniformly bright and dominates.
- Push fog/ambient toward a saturated dark-fantasy GREEN that reads as *luminous*, not a flat dark backdrop.
- Lower the floor's apparent brightness (drop ambient_light energy and/or darken the floor) so colored light POOLS on a dark floor rather than washing a flat grey one. Reference floor = dark with light pooling, not uniformly lit grey.
- KEEP the per-zone color accents (they read well) — the lift is to the GLOBAL atmosphere + contrast, layered UNDER the per-zone accents.

**Fix 3 — Density + warm-point punch in the sparse zones.** Zone 2 (warhall) is the target look — dense braziers, warm points pop. Bring zones 0 (threshold) and 1 (arcane) up toward that: more motivated fire sources (braziers / pyres / candelabra / candles from the extracted prop vocabulary), every warm point a motivated light, fires POPPING (bloom/intensity) against the now-darker atmosphere like the reference's golden lanterns. Add gothic dressing density too (gravestones / statues / bones / crates) where zones read empty.

## 2. Constraints (unchanged — do NOT re-open)

- **Parity sacrosanct.** Re-run the spawn-position parity check after changes; spawns must still equal spec `(x,0,y)` for all 35 / 6 zones. Lighting/atmosphere/dressing are presentation levers; positions are not.
- **Register-2 gates must still hold.** The body-anchored hero fire bloom (FX_Fire_Large_01 + SummonGlow) is the load-bearing HLF/bloom carrier — do NOT weaken it. Darkening the global atmosphere should make it pop MORE (good for the VFX axis). Leave `USE_RITUAL_CIRCLE_PLACEHOLDER` as-is — that decision is settled elsewhere; not in scope here.
- **One editable `.tscn`** Matt opens (`scenes/arena_descent.tscn`); regenerate via `scripts/bake_descent_scene.sh`; keep tracked-authority files (`render_descent_scene.gd`, `descent_scene.tscn`, etc.).
- **Readability holds** — combatants legible; don't drown them in fog or props.
- **Auto-commit locally** (in-scope; Matt-authorized autonomous). **Do NOT push** (Matt away; push stays gated).

## 3. Deliverable

Re-bake + re-capture the establishing + per-zone frames. Report per-fix what changed + the parity re-verification result. Then I review the lift and bring in galadriel to capture + score register-2 (gates hold) AND dark-fantasy visual-similarity vs the reference art.

---

**Signed:** gandalf, 2026-06-15
**For:** iteration-1 mood-lift directive on Drax's delivered connected-descent scene — close the gap to the reference theme via three presentation-lever fixes (remove the magenta sanctum-floor artifact; lift the global atmosphere to vivid luminous green + darken the floor so light pools; raise density + warm-point punch in the sparse threshold/arcane zones), spawn-position parity and the register-2 HLF-carrying hero bloom both held untouched, before galadriel objective scoring.
