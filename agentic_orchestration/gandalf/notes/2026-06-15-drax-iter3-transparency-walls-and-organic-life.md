# Drax iteration 3 — TRANSPARENCY WALLS (camera-agnostic) + ORGANIC LIFE (columns/arches/moss/vines) + golden-point top-up

**Type:** direct gandalf→drax iteration brief (Matt present + directing; continues the authorized connected-descent build).
**Date:** 2026-06-15
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-06-15 — (1) the multi-camera wall-occlusion problem (*"in many pictures the wrong two walls are larger"*) + the transparency proposal (*"making the wall transparent when the camera needs to see the floor underneath"*) — gandalf RULED: adopt it; (2) reference #61's columns/arches + *"tons of mosses, vines and wall plants which give it a real feeling."*
**Parent:**
- `agentic_orchestration/gandalf/notes/2026-06-15-drax-iter2fix-single-wall-ring-ruling.md` — iter2fix (DELIVERED `a137014`: single outer wall ring, pit unwalled, continuous floor).
- `agentic_orchestration/galadriel/reports/2026-06-15-descent-iter2fix-register2-and-similarity-rescore.md` — iter2fix VALIDATED (register-2 6/6, composite 3.96; gold-over-green inverted to gold-dominant; dressing +39%; "the board became a place"). READ §watch-cell (light-point redistribution).
- Reference: `~/Games/reincarnated-godot/Assets/Synty/polygon-dark-fantasy-01/modular_asset_idea_pictures/` — image #61, the gold-lit gothic crypt (arches, columns, heavy moss/vines).
- Canon: `canonical/story/battle-room-presentation-decoupling-2026-06-15.md` — the decoupling principle this iteration's transparency move EXTENDS (Layer-3 geometry-vs-render).

---

## 0. What landed (iter2fix) + what this iteration adds

iter2fix is VALIDATED and is the new baseline — single outer wall ring, unwalled pit, continuous floor, gold-over-green (now gold-dominant), 369-piece annulus, register-2 6/6. KEEP ALL of it. Three additions:

## 1. Change A — TRANSPARENCY WALLS (replaces the per-zone wall-HEIGHT logic)

**The problem (Matt-flagged):** we view shared rooms from MULTIPLE camera angles (establishing spine-shot + per-zone). A wall that's "far" for one camera is "near" for another — so the iter2 "raise the two far walls" per-camera approach makes the WRONG walls tall for some angles. You can't bake a single wall both tall and short.

**The fix — camera-relative wall fade (the genre-standard "wall cutaway"):**
- **Build ALL perimeter walls at full multi-level height — UNIFORM.** Drop the per-zone "which two walls are far" height branching (`_side_levels` / `FAR_LEVELS` per-camera selection). Every wall in the single outer ring is now a tall castle-section wall.
- **Apply camera-relative transparency:** fade out whichever walls sit BETWEEN the active camera and the playable floor. Technique is your seam — either (a) a Godot spatial shader keyed on camera position (fade walls on the camera-near side of room-center), or (b) since the capture cameras are deterministic, per-camera material assignment. **Recommend smooth alpha-fade over hard dither** for screenshot cleanliness.
- **Faded walls still EXIST for lighting** — they cast/receive light and contribute grandeur; only their camera-facing RENDER fades. (If a wall sits between camera and a brazier, fading it lets the glow through — net-positive for the lighting gate.)
- **Why this is better, not just different:** kills the fragile per-camera height logic; works for EVERY camera (establishing, per-zone, eventual gameplay follow-cam, any future angle) with zero per-camera tuning; and grandeur goes UP because every wall is now full-height (the old approach kept near walls stubby at 1-level, sacrificing grandeur — fade gives you full height AND floor readability).
- **Genre:** the wall cutaway is universal — Diablo III/IV, Divinity: Original Sin, Baldur's Gate 3, Pillars of Eternity, Last Epoch.

**PRESERVE the single-wall-ring invariant:** still exactly ONE wall ring at the outer/visual-footprint edge; the playable pit stays UNWALLED; floor flows continuously pit → annulus → outer ring. Do NOT re-introduce an inner ring. iter3 changes the ring's walls from low-near/tall-far to **uniform-tall + camera-faded** — that's the only wall change.

## 2. Change B — ORGANIC LIFE (columns, arches, moss, vines, wall-plants)

Reference #61's "real feeling" layer — the single biggest remaining gap to the reference:
- **Gothic arches** (pointed, traceried) + **columns/pillars** (structural + broken/standalone) — the vertical-variety architecture. → annulus, `nonpassable_dressing`.
- **Moss / vines / wall-plants** — moss patches on stone; vines climbing columns + walls; ferns/foliage at wall-bases and between rubble; hanging vines. This is what makes it read as a LIVING, reclaimed crypt instead of clean geometry. → big vine-walls + wall-climbing growth in the annulus (`nonpassable_dressing`); **LOW passable foliage** (ferns, small plants, moss decals) on the playable floor as floor-art.
- Confirm exact asset names from the POLYGON Dark Fantasy pack (your prop vocabulary). **Go dense** — the reference is overgrown.

## 3. Change C — GOLDEN-POINT TOP-UP (Galadriel's watch-cell)

iter2fix's gold-over-green rotation CUT green points → total light-point density went flat-to-down (`r_lightpoint 0.366→0.330`); zone4's green soulfire dropped 4.09→1.49. **Fix: add MORE golden braziers/lanterns/candelabra in the warm-SPARSE upper chambers — arcane, oubliette, establishing — NOT a green re-add.** Bring total motivated-light density up while staying gold-dominant. Do NOT touch the sanctum hero bloom (load-bearing VFX carrier).

## 4. Constraints (do NOT violate)
- **PARITY SACROSANCT** — re-run `check_descent_parity.py`; 35/35 spawns == spec `(x,0,y)` across 6/6. Transparency + dressing + lights move zero spawn.
- **READABILITY non-negotiable** — the fade must clear the playable floor + combatants for EVERY capture camera (that's the whole point of the change). If a camera angle fights the fade, re-frame the camera (your seam).
- **Register-2 gates HOLD** (lighting ≥4 AND VFX ≥4; composite ≥3.6). Transparency + golden top-up should HELP lighting; organic dressing helps similarity. Sanctum hero bloom (FX_Fire_Large_01 + SummonGlow ×6) + `USE_RITUAL_CIRCLE_PLACEHOLDER` untouched.
- **Single outer wall ring + unwalled pit + continuous floor** preserved. `nonpassable_dressing` grouping preserved + extended to the new arches/columns/vines.
- **One editable `.tscn`** via `bash scripts/bake_descent_scene.sh`; keep tracked-authority files. **Auto-commit locally; do NOT push** (gated).

## 5. Prediction (recognition → validate → commit)
- **Transparency:** EVERY camera angle now shows the correct floor (no "wrong walls larger"); grandeur UP (all walls full-height).
- **Organic dressing:** similarity dressing-density closes more of the gap; "real feeling" up.
- **Golden top-up:** `r_lightpoint` recovers toward/above iter1's 0.366 while staying gold-dominant.
- **Register-2 HOLDS or IMPROVES.**
- **Falsifier:** if transparency hurts readability (faded walls leave combatants/floor ambiguous) OR register-2 DROPS OR parity breaks → the iteration is wrong; surface it, don't ship it.

## 6. Deliverable
Re-bake + re-capture from **MULTIPLE angles** (the whole point of Change A — verify NO angle shows wrong-walls-larger / occluded floor) + the per-zone frames. Parity re-verify. Report per-change (A/B/C) what changed + the parity result + the frame paths. Then Galadriel re-scores iter3 (register-2 gates + similarity + the light-point watch-cell recovery).

---

**Signed:** gandalf, 2026-06-15
**For:** iteration-3 on the connected-descent scene — replace the fragile per-camera wall-height logic with camera-relative transparency (the genre-standard wall cutaway; uniform full-height walls, fade whatever occludes the play space, correct from every angle, grandeur up); add the reference's organic-life layer (gothic arches + columns in the annulus, dense moss/vines/wall-plants for the "real feeling," low passable foliage on the playable floor); and top up golden braziers/lanterns in the warm-sparse upper chambers to recover the light-point density the gold-over-green rotation redistributed — single-wall-ring topology, spawn parity, and the sanctum hero bloom all preserved untouched, readability non-negotiable across every camera angle.
