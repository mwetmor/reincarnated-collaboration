# Battle-Room Presentation — the Sim-Invariant vs Presentation Decoupling

> **STATUS:** CURRENT (load-bearing as of 2026-06-15) — see `canonical/00-ground-state.md`

**Date:** 2026-06-15 (Pattern-B battle-room-presentation dialogue with Matt)
**Author:** gandalf (story-and-design steward)
**Status:** v1.2 — canonical lock for Layers 1–3 (ALL empirically validated) + the architectural-grammar rule (§2-bis, validated by Galadriel iter4 re-score 2026-06-15, commit ffae02b). Layer 3 validated by iter3 re-score commit 8f2f52c.
**Authority:** Matt 2026-06-15 — the 3-part "peering-into-a-section" pattern + the multi-camera wall-transparency direction; validated on the connected-descent scene via Galadriel's objective re-score (iter2fix Layers 1–2; iter3 Layer 3).
**Companion docs:**
- `agentic_orchestration/gandalf/notes/2026-06-15-heading-rad-diff-ruling.md` — Layer 1 (the heading_rad presentation-lever ruling this principle generalizes)
- `agentic_orchestration/gandalf/notes/2026-06-15-drax-iter2-diorama-depth-and-gold.md` — the iteration brief that introduced the footprint decoupling
- `agentic_orchestration/gandalf/notes/2026-06-15-drax-iter2fix-single-wall-ring-ruling.md` — the single-wall-ring topology (the operational form of Layer 2)
- `agentic_orchestration/galadriel/reports/2026-06-15-descent-iter2fix-register2-and-similarity-rescore.md` — the empirical validation evidence
- `agentic_orchestration/gandalf/notes/2026-06-15-drax-iter3-transparency-walls-and-organic-life.md` — Layer 3 (camera-relative transparency; the iteration brief)
- `agentic_orchestration/galadriel/reports/2026-06-15-descent-iter3-register2-and-similarity-rescore.md` — Layer 3 empirical validation (iter3 re-score, commit 8f2f52c)
- `agentic_orchestration/gandalf/notes/2026-06-15-columns-arches-architectural-grammar-rule.md` — §2-bis (the architectural-grammar ruling — columns never stand alone, arches never float, the load-path test)
- `agentic_orchestration/galadriel/reports/2026-06-15-descent-architectural-grammar-gap.md` — the PRE-build gap review (iter3 = 18% architectural presence; arcade-first ranked residual)
- `agentic_orchestration/galadriel/reports/2026-06-15-descent-iter4-architectural-grammar-rescore.md` — §2-bis empirical validation (iter4 re-score, commit ffae02b — 18%→65%, falsifiers cleared)

---

## 0. TL;DR

The battle-room presentation rests on one principle: **separate the SIM-INVARIANT from the PRESENTATION at every layer. Build the world solid and complete; let the presentation adapt.** The sim fixes a small, sacrosanct set of facts (spawn positions, the playable tile footprint, damage geometry); everything the player *sees* — room extent, wall height, dressing, camera, lighting, even which walls render at all — is a presentation lever that can move freely as long as it never touches the invariant.

Validated on the connected-descent scene: Galadriel's iter2fix objective re-score returned **register-2 6/6, composite 3.96**, the gold-over-green hue inverted to gold-dominant, dressing density +39%, and the verdict *"the board became a place"* — the tabletop-board read replaced by a diorama you peer into. Spawn parity held **35/35** through every change.

This generalizes the 2026-06-15 `heading_rad` ruling (Layer 1) and is the governing reference for all future battle-room presentation work. The architectural-grammar refinement (§2-bis) — columns never stand alone, arches never float, grandeur is storeys not tall walls — folds in as a validated constraint on how the annulus dressing reads as a coherent built structure (iter4 re-score: architectural presence 18%→65%, all four falsifier classes cleared, register-2 improved, parity 35/35).

---

## 1. The principle, in three applied layers

The same separation, applied at progressively deeper layers of the render:

| Layer | INVARIANT (sim-fixed; sacrosanct) | PRESENTATION (free lever) | Status |
|---|---|---|---|
| **1** | Spawn POSITIONS `(x,0,y)` | Figure facing / scale / dressing / camera / lighting | Validated (heading_rad ruling) |
| **2** | Playable FOOTPRINT (sim-spec tiles; combatants never leave it) | Visual FOOTPRINT (rendered room extent — expandable outward) | **Validated (iter2fix)** |
| **3** | Wall GEOMETRY (full-height; casts light; carries grandeur) | Wall RENDER (camera-relative transparency fade) | **Validated (iter3)** |

**Layer 1 (`heading_rad` ruling):** the sim fixes WHERE combatants spawn; their facing, scale, the dressing around them, the camera, and the lighting are all presentation. The emitter carries the canonical spawn data faithfully; the loader applies presentation rules on top.

**Layer 2 (this session's core — VALIDATED):** the sim fixes the playable tile footprint (the parity contract — combatants only ever occupy these tiles). The *visual* footprint — how large the room looks — is a free lever. The room is rendered far larger than the playable tiles; the gap is filled with impassable dressing. The playable footprint is an **invisible sub-region of a larger dressed floor**, not a walled room.

**Layer 3 (transparency — VALIDATED iter3):** a wall's geometry (full multi-level height, its contribution to lighting and grandeur) is invariant; its *visibility from a given camera* is presentation. All walls are built full-height; whichever ones occlude the play space for the active camera fade out. This decouples geometry from any single camera angle — see § 3. Validated by Galadriel's iter3 re-score: readability clean across every camera angle (establishing diagonal + per-zone top-downs fade *different* walls of the same rooms, all correct, no wrong-walls-larger), grandeur up (871→1314 full-height walls), register-2 held 6/6, no falsifier fired.

## 2. The annulus rule + single-wall-ring topology (the operational form of Layer 2)

- **The annulus:** impassable dressing (tombs, statuary, columns, arches, rubble, vines) fills `[playable-footprint edge → outer wall]`, strictly OUTSIDE the playable AABB plus a small readability margin. The playable pit stays clear; the world grows around it. This is where dressing density is repaid (iter2fix: a 369-piece annulus → +39% dressing similarity).
- **Single wall ring:** there is **exactly ONE wall ring per room, at the outer/visual-footprint edge.** The playable pit is **UNWALLED** — the floor flows continuously pit → annulus → outer ring. Walling the playable pit re-couples the two footprints and re-creates the "tabletop board boxed pit" the whole move eliminates. (iter2's double-wall defect, corrected in iter2fix, was exactly this re-coupling.)
- **Optional demarcation:** if a play-space boundary aids readability, LOW see-over elements only (knee-high ruined-wall fragments / a curb / a floor-texture ring) — never a full-height inner wall.
- **Floor-tiling root cause (iter4 refinement):** the annulus floor must be tiled with the SAME material as the playable floor — and the failure mode to guard is not a darker *material* but a **missing** one. iter4 surfaced that the "darker annulus" Matt saw was bare near-black background VOID (the playable footprint was the only tiled region, so it re-drew its own boundary). Tile the FULL footprint with the playable floor material. The discipline generalizes: **the playable footprint must never be the only tiled region**, or it re-creates the boxed-pit read the whole Layer-2 move eliminates.

## 2-bis. The architectural-grammar rule — columns & arches as coherent built structure (VALIDATED iter4)

> Refines §2: it constrains HOW the annulus dressing + wall ring use columns and arches. Authored as the standalone ruling `agentic_orchestration/gandalf/notes/2026-06-15-columns-arches-architectural-grammar-rule.md` (Matt 2026-06-15 verbatim — *"the columns themselves are never standing alone unless it is rubble… arches should either be used across wall tops as windows or across columns as a separate 'wall' set… built as if it was actually made as a coherent structure"*), built by Drax (iter4, commit `ed3c1b2`), and **validated by Galadriel's iter4 re-score** (commit `ffae02b`) — folded in here per recognition→validate→commit.

The annulus dressing is not scattered decoration. Columns and arches must read as **a real building that could stand** — a coherent load path. Three locked rules + one test:

- **Columns never stand alone.** A standing column is a **pier** (carries an arch), an **arcade member** (carries an arch run in regular rhythm), an **engaged column / pilaster** (set into a wall plane), or a **baluster** (carries a rail). The ONLY free-standing-on-the-ground stone vertical allowed is **rubble** — fallen, broken, on its side. No upright orphan columns.
- **Arches never float.** An arch is a **window-in-wall** (head of an opening cut in a wall plane, masonry above + beside — this motivates the god-rays), an **arcade** (springs column-to-column in a regular rhythm — a see-through but physically-bounded screen-wall), or a **gallery/bridge span** (between two wall masses at an upper level). Every arch lands on real support at BOTH feet.
- **Grandeur is storeys, not tall walls.** A lower arcade carries an upper gallery with a balustrade edge, reached by stairs, with set-pieces (statuary / votives / banners) reading as inhabited. The gallery sits OUTSIDE the playable footprint (annulus/backdrop; combatants never go up). Tall walls give scale; a floor-above-floor gives grandeur.
- **The one test (the load-path invariant):** before placing any column or arch — *"if this were stone and gravity were on, would it stand, and is it doing a job?"* Every arch springs from a real support at both feet; every column carries a load or is rubble; no orphan verticals, no floating spans. This is the architectural analog of the sim-invariant: the load path is the invariant the dressing must respect, exactly as the playable footprint is the invariant the visual footprint must respect.

**Validation (iter4, Galadriel re-score `ffae02b`):** architectural-grammar presence **18% → 65%** (composite 0.875→3.10 / 4.75); all four falsifier classes (orphan upright columns / wall-top silhouette arches / free verticals on open floor / arch-feet on empty floor) **CLEARED to zero**; per-dimension gains arcade 0.5→3.0, storey/gallery 0.5→3.0, load-path 1.5→3.5, arch-as-window 1.0→2.8; register-2 **not regressed — improved** (warm:green 1.46→1.75, the warm masonry is gold-additive; green identity + hero bloom + magenta gateway all held); parity **35/35** sacrosanct. Build inventory: arcade piers (`SM_Bld_Buttress_Pillar`) carrying `SM_Bld_Wall_Archway_02` arches across 2-tile bays; windows-in-wall (`SM_Bld_Base_Wall_Window_01`) at the ground course; a gallery storey on tall piers with a `SM_Bld_Railing` balustrade reached by stairs; rubble = pillars laid on their side over burnt-rubble props.

**One PARTIAL, not a fold-blocker:** through-window god-rays — the windows are built + verified in the wall planes, but no captured frame yet shows a light shaft visibly passing *through* a named window arch (iter3 had no windows at all, so the god-ray-motivator intent is structurally satisfied). The cheap optional third-wave residual: place a window directly in an establishing-camera light shaft so a ray passes through it — converts the PARTIAL to PASS and closes the largest single-dimension gap. Not required for the fold.

## 3. Layer 3 — camera-relative wall transparency (the wall cutaway)

**Problem it solves:** a fixed scene viewed from multiple camera angles (establishing spine-shot + per-zone shots, and eventually a gameplay follow-cam) cannot have correct wall heights baked per-camera — a wall that is "far" (should be tall) for one camera is "near" (should be low) for another. You cannot bake a single wall both tall and short.

**Resolution:** build ALL walls full-height (uniform; no per-camera height selection), and fade out whichever walls sit between the active camera and the play space. The faded wall still exists for lighting and grandeur — only its camera-facing render fades. This is the genre-standard **wall cutaway** (Diablo III/IV, Divinity: Original Sin, Baldur's Gate 3, Pillars of Eternity, Last Epoch). It is *architecturally simpler* than per-camera height logic (it deletes the branching), correct from every angle, and increases grandeur (every wall is now a full castle-section wall, not a stubby near-wall).

## 4. Genre grounding

The diorama / open-fronted-box framing is the genre default for fixed-camera tactical/ARPG rooms: Diablo's isometric chambers, Darkest Dungeon and Divinity: Original Sin framing the fight as "peering into an open-fronted box." Combat is visually bounded by impassable architecture far larger than the playable corridor; the camera looks *into* a section of a larger world. The reference target (POLYGON Dark Fantasy gold-lit crypt) is built on exactly this: a small clear playable pit ringed by raised tombs and statuary, tall gothic architecture and god-rays behind, dense organic overgrowth giving it a lived-in "real" feel.

## 5. What it governs + forward hooks

- **Governs:** all future battle-room presentation builds. Any room renders the playable footprint as a sub-region of a larger dressed floor with a single outer wall ring; combatants never leave the sim-spec tiles; parity is re-verified after every presentation change.
- **`nonpassable_dressing` grouping:** every impassable dressing object lives in a clearly-named group so the eventual live-combat/collision pass can programmatically separate blockers from playable-floor decals. Cheap now; saves a manual sweep at the live-combat milestone.
- **Playable-floor art is passable-only:** decals/scatter/low foliage on the playable floor (pathing-collision-forward-compatible); all non-passable objects go in the annulus.
- **Live-combat milestone caveat:** when the room stops being a scored tableau and becomes a playable fight that initializes entity STATE from the spec, re-examine whether any presentation lever needs to feed sim state (e.g., spawn-instant facing). Marginal — the sim overrides spawn heading at fight-start regardless (per the heading_rad ruling) — but flagged.
- **Arcade-rhythm probe framing-tension (benchmark instrument note):** the objective arcade-rhythm periodic-peak probe (Galadriel's gap-review discriminator) registers a regular colonnade ONLY from a side-on angle; our top-down combat camera foreshortens the rhythm along the frame edge and the probe under-counts it (iter4's built arcade reads max-1 peaks where the reference's side-on shots read 2–4). This is a framing tension, not a build gap — the manual architectural-inventory close-read is the gate. If a clean objective arcade number is ever wanted, render one oblique/lower-angle benchmark-capture frame per scene (separate from the combat camera) for the probe to score.
- **Through-window god-ray (optional refinement):** see §2-bis PARTIAL — placing a window-in-wall directly in an establishing-camera light shaft is a cheap placement/lighting refinement that converts the lone architectural-grammar PARTIAL to PASS. Not required.

## 6. Validation evidence + open watch-cell

- **Validated (iter2fix, Galadriel re-score):** register-2 6/6, mean composite 3.96 (up from iter1 3.875); lighting improved on all 6 zones; VFX hero bloom marquee-strength; gold-over-green inverted to gold-dominant (the iter1 #1 gap closed); dressing +39%; contrast +20% from the diorama depth; parity 35/35. The single-wall-ring removal of the inner ring did NOT drop the lighting gate (the outer multi-level walls + annulus carry the gold rake).
- **Validated (iter3, Galadriel re-score `8f2f52c`):** Layer-3 transparency **PASS** — readability clean across **every** camera angle (the load-bearing Change-A criterion: establishing diagonal + per-zone top-downs fade *different* walls of the same rooms, all correct, no wrong-walls-larger), grandeur up (871→1314 full-height walls). Register-2 **HELD** 6/6 (composite 3.96→3.94, within noise; both gates clear color-fair every zone). Dressing density **IMPROVED** (`r_dressing` 0.693→0.853, +23%; gap to reference halved 31%→15% from the 688 organic pieces). No falsifier fired.
- **Validated (iter4, architectural-grammar fold-in, Galadriel re-score `ffae02b`):** the §2-bis columns-&-arches rule built (Drax `ed3c1b2`) + validated — architectural-grammar presence **18%→65%** (composite 0.875→3.10/4.75), all four falsifier classes cleared to zero, register-2 improved not regressed, parity 35/35. One PARTIAL (through-window god-ray; not a fold-blocker). The arcade-rhythm probe did NOT move (max-1, vs reference 2–4) — read as the top-down framing under-counting a built arcade (see §5 benchmark instrument note + §2-bis), with the manual close-read as the gate; reported plainly against the PASS.
- **RESOLVED watch-cell (was carried iter2fix→iter3 — r_lightpoint):** recovered `r_lightpoint` 0.330→**0.384** (above iter1's 0.366 target) via the golden top-up — warm% +0.327 scene-wide with green **flat** (+0.012), i.e. gold not a green re-add, exactly the specified lever.
- **New watch-cell (carried forward from iter3 — warm:green margin compression):** the gold-dominant margin **COMPRESSED 1.95→1.47** (−25% toward parity) — but the inversion **HELD** (warm:green scene-mean 1.465 >1.0; 5/7 views gold-dominant; every near-chamber view that was gold-dominant in iter2fix STAYED so; it did NOT regress past the inversion line). Cause: the uniform full-height walls now on all four sides — especially the previously-OPEN camera-side wall, now present + faded — plus cool ambient grew cool mass on the floor bed, so the floor reads cooler while the gold concentrates into point-sources / dressing-rim / walls and still wins the frame. **NOT a ship-blocker** (gates held, inversion held). If a future cool-side-geometry iteration narrows it further, the lever is a **warmer floor-material tint or floor-bed gold-bounce — NOT more point-lights** (the eye reads those as points-on-cool-floor, not a warm bed). Residual: the oubliette warm top-up was uneven (favored arcane/threshold/establish over the dark corridor). **iter4 update — IMPROVED, not compressed:** the §2-bis architecture build moved warm:green 1.46→**1.75** (every frame warmer, none cooler — the warm tan masonry is gold-additive, exactly the "warmer floor/material tint, NOT more point-lights" lever this watch-cell named). The margin recovered without a point-light re-add; watch-cell de-escalated.

---

## 7. Cross-references

- Layer 1 origin: `agentic_orchestration/gandalf/notes/2026-06-15-heading-rad-diff-ruling.md`
- Layer 2 briefs: iter2 (`...drax-iter2-diorama-depth-and-gold.md`), iter2fix ruling (`...drax-iter2fix-single-wall-ring-ruling.md`)
- Layer 3 brief: `...drax-iter3-transparency-walls-and-organic-life.md`
- Validation (Layers 1–2): `agentic_orchestration/galadriel/reports/2026-06-15-descent-iter2fix-register2-and-similarity-rescore.md`
- Validation (Layer 3): `agentic_orchestration/galadriel/reports/2026-06-15-descent-iter3-register2-and-similarity-rescore.md`
- §2-bis (architectural grammar) ruling: `agentic_orchestration/gandalf/notes/2026-06-15-columns-arches-architectural-grammar-rule.md`
- Validation (§2-bis): gap review `agentic_orchestration/galadriel/reports/2026-06-15-descent-architectural-grammar-gap.md` → iter4 re-score `agentic_orchestration/galadriel/reports/2026-06-15-descent-iter4-architectural-grammar-rescore.md` (commit ffae02b)
- Parity contract: `reincarnated-godot/scripts/check_descent_parity.py`; the editable scene `scenes/arena_descent.tscn` (baked via `scripts/bake_descent_scene.sh`)

---

**Signed:** gandalf, 2026-06-15
**For:** capturing the battle-room presentation principle — separate the sim-invariant (spawn positions, playable footprint, damage geometry) from the presentation (room extent, wall height, dressing, camera, lighting, wall render) at every layer; build the world solid and let the presentation adapt; the playable footprint is an invisible sub-region of a larger dressed floor bounded by a single outer wall ring with the pit unwalled; empirically validated on the connected-descent scene (Galadriel iter2fix re-score: register-2 6/6, composite 3.96, gold-dominant, dressing +39%, "the board became a place"), with the camera-relative wall-transparency layer (Layer 3) now validated by Galadriel's iter3 re-score (register-2 held 6/6, transparency readability clean from every camera angle, grandeur 871→1314 full-height walls, dressing +23%, no falsifier fired), and the architectural-grammar rule (§2-bis: columns never stand alone, arches never float, grandeur is storeys, governed by one load-path test) now folded in and validated by Galadriel's iter4 re-score (architectural presence 18%→65%, all four falsifier classes cleared, register-2 improved to warm:green 1.75, parity 35/35).
