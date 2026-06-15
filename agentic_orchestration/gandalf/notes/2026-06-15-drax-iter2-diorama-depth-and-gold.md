# Drax iteration 2 — DIORAMA DEPTH + GOLD-OVER-GREEN (Matt's 3-part pattern × Galadriel's CV signal converge)

**Type:** direct gandalf→drax iteration brief (Matt present + authorizing; continues the authorized connected-descent build).
**Date:** 2026-06-15
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-06-15 — the 3-part "peering-into-a-section" pattern + reference image (POLYGON Dark Fantasy gold-lit crypt hero shot). This brief synthesizes Matt's pattern with Galadriel's objective scorecard, which independently found the same target.
**Parent:**
- `agentic_orchestration/gandalf/notes/2026-06-15-drax-iter1-descent-mood-lift.md` — iter1 (DELIVERED: green atmosphere + darker floor + density; magenta artifact removed; parity proven 35/35).
- `agentic_orchestration/galadriel/reports/2026-06-15-descent-connected-register2-and-similarity-scorecard.md` — Galadriel's objective re-score (READ THE NUMBERS in §2C).
- Reference art: `~/Games/reincarnated-godot/Assets/Synty/polygon-dark-fantasy-01/modular_asset_idea_pictures/` — the new hero image Matt cited is the gold-lit gothic crypt (gold LIGHT pouring through green SHADOW; multi-level walls; small playable pit ringed by raised tombs/statuary).

---

## 0. The convergence (why this iteration is high-confidence)

Matt's design intuition and Galadriel's CV instrument independently point at the SAME target:

| Matt's pattern | Galadriel's measured gap | One move |
|---|---|---|
| #1 multi-level far walls ("peering into a section, not a tabletop board") | lighting-drama headroom + light-point density 63% below | raise far walls → more vertical surface for gold-rake + deeper shadow drama |
| #2 extend room beyond sim-spec, pad with impassable dressing | dressing density 50% below; "green-black void reads empty" | the annulus between playable edge and far walls is WHERE the dense gothic clutter goes |
| Matt's reference = GOLD light in GREEN shadow | hue inverted: demo went GREEN-dominant; ref is WARM-over-green (warm% 1.70 vs ref 5.46) | gold-dominant LIGHT, green only as the shadow/atmosphere bed |

iter1's "vivid green" was directionally incomplete — I over-rotated the green. The reference (and Matt's image) is **gold-dominant LIGHT in a green SHADOW bed**, not a green flood. This iteration corrects that AND adds the depth Matt's pattern calls for.

## 1. Governing principle — playable-footprint vs visual-footprint DECOUPLING

The load-bearing insight in Matt's pattern. Two footprints, now explicitly separate:

- **Playable footprint** = the sim-spec tile space from `data/arena_scenarios.json`. The combatants ONLY ever occupy this. **PARITY CONTRACT — unchanged, sacrosanct.**
- **Visual footprint** = the rendered room extent. **PRESENTATION LEVER — expandable outward.**

This extends the 2026-06-15 `heading_rad` ruling ("spawn POSITIONS sacrosanct; facing/scale/dressing/camera are presentation levers") by adding ROOM EXTENT + WALL HEIGHT to the presentation-lever side. Genre-standard: Diablo 2/3/4 visually bound combat with impassable ruins/architecture far larger than the playable corridor; Darkest Dungeon / Divinity: Original Sin frame the fight as "peering into an open-fronted box." (Canon-worthy — I capture it after this iteration + Galadriel re-score validate the predicted register lift.)

## 2. Three composed changes

### A. Multi-level far walls (Matt #1)
- We have a FIXED 2.5D per-zone camera, so "which walls are far" is DETERMINISTIC per zone. The two walls AWAY from the camera rise **2–4 levels**; the camera-side wall + the connected-corner wall (where the player spawns) stay **1 level** (or low/open so the camera sees in over them — see the reference's foreground crenellations).
- **Connector openings stay** (the corridors between rooms are sacrosanct passage). Raise the OUTER non-connector far walls.
- **Re-frame the per-zone + establishing cameras** as needed so the taller far walls do NOT occlude the playable floor — readability of combatants is non-negotiable (§3).
- Bonus: tall far walls give Galadriel's LIGHTING gate more to work with (vertical surface for gold-rake, deeper cast shadows = more drama) and are the natural carrier for the gold god-rays.

### B. Extend visual footprint + impassable annulus dressing (Matt #2)
- Push the OUTER walls outward so the room is visibly larger than the playable tile space. Grow **laterally + on the far-wall side**; do NOT let adjacent rooms' visual extents collide along the spine (corridors stay the spine connection).
- **The annulus rule:** dense impassable gothic dressing fills `[playable-footprint edge → far wall]`, STRICTLY outside the playable AABB plus a small readability margin. Tombs, sarcophagi, broken pillars, statuary, rubble, skull-piles, pyres, banners — this annulus is where Galadriel's 50%-below dressing density gets repaid. The playable pit stays clear; the world extends around it.
- Net effect: the room FEELS larger/grander and adheres 100% to the sim spec (combatants never leave the playable footprint).

### C. Gold-over-green + playable floor-art (Matt #3 + Galadriel #1/#2)
- **Hue correction (Galadriel's #1 gap, ~65% off):** make WARM GOLD the dominant LIGHT (braziers, lanterns, candelabra, god-rays, glowing treasure/fire) and let GREEN recede to the SHADOW/atmosphere bed. Not a green flood — gold POPS, green is the dark. Re-read Galadriel's report for the warm% target (ref 5.46 vs current 1.70 ≈ need ~3× the warm-light presence).
- **Light-point density (Galadriel's #2 gap, ~63% below):** ~3× the golden point-lights, concentrated in the annulus + far-wall rake, so the upper chambers stop reading warm-starved.
- **Playable floor-art (Matt #3):** on the PLAYABLE floor prefer PASSABLE decals/scatter — rocks, plants, torn book-pages, bone-scatter, a red rug/runner — texture without collision risk. Keep NON-passable objects OFF the playable floor (they go in the annulus). Rationale Matt named: we don't yet know how pathing interacts with live-combat collision; keep the playable floor clear-of-blockers and forward-compatible.
- **Forward-compat hook (gandalf add):** put every non-passable dressing object in a clearly-named group (e.g., `nonpassable_dressing`) so the eventual live-combat/collision pass can programmatically find blockers vs playable-floor decals. Cheap now; saves a manual sweep later. (This operationalizes Matt's "we can easily delete the non-passable objects later as needed.")

## 3. Constraints (do NOT violate)
- **PARITY SACROSANCT.** The playable footprint + all 35 spawn positions are unchanged. Re-run `check_descent_parity.py`; spawns must still equal spec `(x,0,y)` across 6/6 zones. Extending the visual extent + raising walls must NOT move any spawn.
- **Register-2 gates HOLD.** The body-anchored hero bloom (FX_Fire_Large_01 + SummonGlow ×6) stays untouched (load-bearing VFX carrier). `USE_RITUAL_CIRCLE_PLACEHOLDER` untouched.
- **READABILITY is non-negotiable.** Taller far walls must NOT occlude the playable floor or the combatants from the capture cameras. If a wall height fights the camera, re-frame the camera (your seam) — do not sacrifice combatant legibility for grandeur.
- **One editable `.tscn`** (`scenes/arena_descent.tscn`) via `bash scripts/bake_descent_scene.sh`; keep tracked-authority files.
- **Auto-commit locally** (in-scope autonomous); **do NOT push** (gated).

## 4. Prediction (register; recognition → validate → commit)
- Subjective grandeur UP ("peering into a section of the castle," not a tabletop board).
- Galadriel similarity UP on all three measured gaps: hue (gold-over-green), light-point density, dressing density.
- Register-2 HOLDS or IMPROVES (taller walls + gold-rake = more lighting drama = more gate headroom; annulus dressing + floor-art don't touch playable spawns).
- **Falsifier:** if register-2 gates DROP (e.g., walls over-shadow the lighting gate, or occlude the floor hurting readability) OR parity breaks (any spawn moves) — the iteration is wrong; surface it, don't ship it.

## 5. Deliverable
Re-bake + re-capture establishing + per-zone frames. Report per-change (A/B/C) what changed + the parity re-verification result + the frame paths. Then I review, and Galadriel re-scores register-2 + similarity-vs-reference to validate the §4 prediction.

---

**Signed:** gandalf, 2026-06-15
**For:** iteration-2 on Drax's connected-descent scene — synthesizing Matt's 3-part "peering-into-a-section" pattern (multi-level far walls; extend visual footprint + impassable annulus dressing; passable floor-art on the playable area) with Galadriel's converging objective scorecard (correct the green-over-gold hue inversion to gold-light-in-green-shadow; +3× warm light-point density; +dressing density in the now-larger annulus), under the governing playable-footprint-vs-visual-footprint decoupling principle, with spawn-position parity and the register-2 hero bloom held untouched and readability non-negotiable.
