# TCP-L5-D — mode (ii) SEAM ARRIVAL, **Phase B report** (build)

**Cell:** L5-D · **Author:** drax (presentation seam) · **Date:** 2026-07-25
**Dispatch:** `agentic_orchestration/dispatches/2026-07-25-drax-l5d-seam-arrival-phase-b.md`
**Phase A:** `…-phase-a-report.md` + `~/Games/mcp-lab/evidence/l5/l5d/SITING_PLAN.md`
**Status: BUILT. All eight gates met. G4 walkability PASSES.**

---

## 0 — The authoring clock

| Mark | UTC | Elapsed |
|---|---|---|
| Phase A | `20:04:33Z → 20:32:19Z` | **27.8 min** |
| Phase B | `20:51:23Z → 21:14:40Z` | **23.3 min** |
| **CELL TOTAL** | | **51.1 min (0.85 h)** |

Thinking included, per TCP-32. **Method H throughout, both phases — no wire engaged, so none of
the 51.1 min is swap or transport** (Matt R-7, agreed).

**The boundary, stated so it cannot be gamed:** the clock stops where Phase A's stopped — at
deliverables-complete and substrate re-verified (Phase A: "SITING_PLAN complete, probes banked,
substrate re-verified"). For Phase B that is `21:14:40Z`, the vacate plus the closing substrate
check. Report authoring sits outside it, as in Phase A. **For completeness the un-truncated
wall-clock to the commit landing is `20:51:23Z → 21:19:00Z` = 27.6 min**, and the cell total on
that basis is 55.4 min. Both numbers are here so the smaller one is not doing any hiding.

Phase B breakdown: substrate re-read and material/basis harvesting ~5 min; builder authoring ~6 min;
three build-time defects found and fixed ~5 min; census authoring plus two check-definition
corrections ~4 min; G4 sweep including the instrument defect ~4 min; frames, diff, vacate ~4 min.

Five Godot processes, one scene each (TCP-23): build (headless) · census (headless) · sweep
(Metal) · `__box` (Metal) · money frame (Metal). Plus one repeat `__box` for the byte-identity
check and one repeat build for the determinism check.

---

## 1 — What was built

**330 nodes** (296 − 2 + 36). A 5.00 × 3.75 m side-chamber on the crypt's north axis, entered
through a 2.0042 × 1.9663 m opening in bay `0_3`, built entirely from the crypt's own modules,
materials and sub-resources.

```
REMOVED   Walls/Wall_0_3_inner, Walls/Wall_0_3_outer          (2, targeted by volume query)
ADDED     Walls/Portal_0_3                                     opening module, 3 surface overrides
          Floor/ChFloorQ_0..11                                 12 tiles, the crypt's OWN ArrayMesh
          Walls/ChWall_{far,eastside,westside}_*               12 skins, double-skinned 0.225+0.225
          Walls/ChWallCap_*                                     6 caps, BoxMesh as the substrate does
          Pillars/ChPillar_{E,W} + ChTopper_{E,W}               4, the kit's own corner piece
          ChamberPool                                           1 OmniLight3D
```

**Zero new materials and zero new shaders were authored** — the built `.tscn` carries the same
26 ShaderMaterial and 8 StandardMaterial3D sub-resources as the substrate, and the same six
`ext_resource` entries. R-4 is satisfied at the file level, not merely in intent. Only **two**
new mesh resources exist: the opening module and the half-width wall panel, the only two modules
the substrate does not already contain inline.

---

## 2 — The gates

| # | Gate | Result |
|---|---|---|
| 1 | Reload census through the engine | **PASS** — `evidence/l5/l5d/RELOAD_CENSUS.txt` |
| 2 | ★ The 0.45 m floor hole, closed | **PASS** — mechanism in §3 |
| 3 | ★ G4 capsule sweep vs the PROXY | **PASS** — walkable, clear width 1.9544 m |
| 4 | Three-surface door module | **PASS** — all 3 overridden, 0 untextured surfaces scene-wide |
| 5 | Money frame + `__box` establishment | **PASS** — 3 frames banked |
| 6 | Descriptive diff, `l4_diff.py` unmodified | **DONE** — §5 |
| 7 | Vacate | **PASS** — project dir inventory identical to cell start |
| 8 | Blast radius | **PASS** — no HALT |

### 2.1 Reload census (gate 1)

Loaded back **from disk through the engine** as a live tree, not text-parsed — a text parse
agrees with the writer about anything the writer got wrong.

- counts 296 → 330; MeshInstance3D 288 → 321; OmniLight3D 1 → 2; Floor 196 → 208, Walls 84 → 101,
  Pillars 8 → 12. All match prediction exactly.
- **removals proven absent** two ways: by path (`Wall_0_3_inner`/`_outer` resolve in the substrate,
  resolve to null after reload) **and by volume**, because absence-by-name is weak — a renamed
  survivor would pass it.
- **duplicates / TCP-31: I declare FLATTEN, not instance.** 0 nodes below the root carry a
  `scene_file_path`; 0 duplicate names within a holder; 0 pairs sharing mesh *and* transform. Every
  added node is a bare `MeshInstance3D` with an inline mesh sub-resource parented straight into the
  substrate's own role holders. No `PackedScene` is instanced and no `set_owner_recursive` runs over
  an imported sub-tree — which is the duplication mechanism TCP-31 exists for.
- **untextured survivors: zero**, checked per *surface* (override → material_override → mesh
  material) across all 321 mesh instances.

### 2.2 The orphaned-collision clause, with its reason (L-L)

**Satisfied, and the pass carries no information.** Measured: the substrate contains **0**
`CollisionObject3D`/`CollisionShape3D` of any kind; the built scene contains 0 as well. The clause
is **empty by construction, not satisfied by care** — a removal cannot orphan collision that never
existed, so on this substrate the check had no way to fail. Stating it as a pass without the reason
would have been the L-K failure mode wearing a governance hat. The question it stands proxy for —
*can the player still walk there* — is answered instead by G4, which **generates** collision at
sweep time precisely because there is none to inherit.

### 2.3 Blast radius

| Thing | Verdict |
|---|---|
| `project/scene_before.tscn` | sha `d45db0f5…de8522de1966`, mode **0444**, verified at cell START and cell END. Never opened for write. |
| `project/l4_shoot.gd` | `d5297505…` — **unmodified**, used as-is for the `__box` frame |
| `prep/l4_diff.py` | `736ee06c…` — **unmodified**, run as-is |
| `~/Games/mcp-lab/project/` | file inventory byte-for-byte identical to cell start (diff of listings) |
| `user://` | `logs/` emptied into `prep/l5d_residue/user_logs/`; nothing else touched |
| `~/Games/mcp-lab/l6prep/` | **not entered.** No `*l5d*` anywhere under it. |
| `~/Games/reincarnated-godot/` | HEAD `81eea9d` → **`398609c`** — the quilt dispatch's own three commits, exactly as the dispatch said. `kit_replica_level.gd` = `42935a35…`, git-clean. The one uncommitted tracked file, `project.godot`, carries the **identical** `mesh_lod` diff banked at Phase A cell start. **Not mine. No HALT.** |

---

## 3 — ★ THE FLOOR HOLE, AND THE RECIPE CLAUSE

**Mechanism: the new room's floor plate runs to the NEAR face of the shared wall band, not to its
far face. It passes *under* the full 0.45 m of masonry and butts the old room's last tile row.**

Concretely: the chamber plate is `z [−12.50, −8.75]`, not `z [−12.50, −9.20]`. Its near tile row
(`z` origin −10.00, covering `z [−10.00, −8.75]`) spans the entire band the removal opened. No
special threshold piece, no patch tile, no bespoke geometry — the fix is a **choice of extent**,
made three tiles deep so it lands on the grid.

**The recipe clause, for every future door in every future room:**

> A doorway's floor is owned by the room BEHIND it. Size the new room's floor plate to the shared
> wall's **near** face — the old room's floor edge — so it runs under the full band thickness.
> The old room's floor stops at its own edge and always has; the band was never floored because it
> was never walked on. Cutting the wall is what makes it walkable.

Three independent measurements bind it:

1. **Build-time, before the chamber existed:** stepping the band at 1 mm and asking whether any
   floor node's world AABB spans it → **0.4500 m uncovered of 0.4500 m**. The Phase A finding
   reproduced exactly, from the other direction.
2. **Build-time, after:** the same query → **0.0000 m uncovered**. This is an assertion in the
   builder; the build fails if it does not hold.
3. **Sweep-time, by physics:** a downward ray every 1 cm along the whole 12 m walk → **1201
   samples, 0 with no floor, floor y ∈ [0.008100, 0.008100], max step 0.000000 m.** No hole, no
   lip, no step, anywhere. That also discharges register cue #2.

The census records the two chamber tiles that live inside the portal prism (`ChFloorQ_5`,
`ChFloorQ_8`) as a *required* presence, not contamination — see §4.2.

---

## 4 — Build-time findings (the ones that changed the work)

### 4.1 ★ `.tscn` stores basis ROWS, not columns — and SITING_PLAN §3 says the opposite

**SITING_PLAN.md §3 "Transpose watch" is WRONG**, in the sentence I wrote specifically to guard
against the transpose trap:

> *".tscn `Transform3D(...)` stores **basis columns first**, origin last."*

It stores **rows**. For `Transform3D(a,b,c, d,e,f, g,h,i, ox,oy,oz)` the triples are
`rows[0..2]`, so `basis.x = (a,d,g)`, `basis.y = (b,e,h)`, `basis.z = (c,f,i)` — the basis vectors
are read **down the columns with a stride of 3**, not across. Godot's `Basis` stores `rows[3]` and
`.x/.y/.z` are *column* accessors, so the serialised triples are not the basis vectors.

Two things made this real rather than pedantic:

- **The 12-float form has no GDScript constructor at all.** `Transform3D(f × 12)` exists only in
  the serialiser. Any script that authors transforms is *forced* to translate the text, and the
  translation is exactly where the trap lives.
- **6 of my 8 transcribed bases passed a transposed reading.** `N`, `CN`, `CE`, `CW`, `P`, `T` all
  have off-diagonal terms of O(1e-7) or zero, below `is_equal_approx`'s tolerance. Only `E` and
  `W` — the two whose off-diagonals are O(1) — came back with x and z swapped and negated. **A
  transposed transcription would have shipped a mirrored chamber on six bases out of eight, and
  the two that caught it are an accident of which walls I happened to need.**

What saved the build was not care, it was structure: no basis is retyped at all. Every basis is
**read off the live substrate node it mirrors**, and the transcription exists only as a *gate*
against it. The check is in the builder and the build fails if the two disagree.

*This is the same class of failure as KIT-REPLICA lap-1 R2, which I cited in Phase A as the reason
to be careful — and being careful is what produced the wrong sentence.*

### 4.2 Two census checks were wrong, and both corrections are load-bearing

- **"the prism holds the opening module and nothing else"** returned three nodes: the portal plus
  `ChFloorQ_5` and `ChFloorQ_8`. Those two tiles are **the floor-hole repair**, and an assertion
  that forbids them forbids the fix. The correct statement splits the prism at the walking
  surface: nothing but the opening **above** it, floor **below**. The corrected check now verifies
  the removal *and* the repair in a single query.
- **"chamber far band outer face = −12.95"** returned −13.0672. That is the corner **topper**,
  whose 0.4870 footprint scaled ×1.4054898 overhangs the band by 0.117 — exactly as the crypt's
  own toppers overhang its band. The frame budget is stated for two different things and has to be
  checked as two: band face **−12.9500** ✓, outermost geometry **13.0672 < 13.538** (the Phase A
  budget *with* a corner topper) ✓.

### 4.3 ★ G4's clearance search was measuring my probe, not the doorway (L-K class)

The first form of the clearance measurement binary-searched the largest **capsule** radius that
passes the opening plane. It returned **0.8595 m** — a clean, plausible, four-decimal number.

It is a property of the probe. `CapsuleShape3D` requires `height ≥ 2·radius`, so past r = 0.8495
the probe grows *taller* as it grows wider and its own bottom sinks back into the floor. Solving:
bottom reaches the floor at r = 0.868090 − 0.0005 − 0.008100 = **0.85949**. The search reported
**0.8595**. It measured my capsule to four decimal places and I would have believed it.

A capsule cannot measure a hole wider than its own height permits. Re-asked with a probe whose
width is independent of its height — a 1.70 m box, 0.10 m deep, width bisected — the answer is
**clear width 1.9544 m**, which agrees with the independently measured proxy aperture of **1.9553 m
to 0.9 mm**. That agreement *is* the calibration: the physics world and the FBX rasteriser, two
unrelated instruments, land on the same number.

### 4.4 The G4 capsule needed a declared skin, and the first run said the floor was a wall

First sweep: **all 1064 stations blocked, including z = 0.0 in the middle of an empty room.** With
the capsule's feet exactly on the floor, `intersect_shape` counts contact as penetration, so the
floor blocks the walk. Every real character controller carries a skin width for this. Declared:
**0.01 m**. The floor is *not* excluded from the test — ground continuity is answered separately
and more strongly by the downward ray (§3), which keeps the floor in the measurement.

### 4.5 Phase A §0.3 was half wrong about *why* the near walls are dark

Phase A said runs 1 and 2 (south, east) are "deliberately made see-through". Reading the shader
sources at build time: **`occlude = 0.0` on every wall material in the substrate.** In
`walltop_occlude`, `upper_alpha = mix(1.0, ghost_floor, occlude)`, so at occlude = 0 the wall is
**fully solid** regardless of `ghost_floor`. The east run is not faded; it is *configured* to
vanish (`ghost_floor 0.0` rather than 0.18) when a runtime driver raises `occlude`, which nothing
in this static scene does. South genuinely *is* blacked out, but by `south_blackout = true` in
`walltop_void_radial`, a different mechanism entirely.

**The Phase A conclusion survives** — south and east are still the camera-*near* walls, and a
chamber beyond either would sit between the camera and the crypt. R-1's north-vs-west comparison is
untouched. Only the stated reason was wrong.

### 4.6 The builder is deterministic except for Godot's `unique_id`

Run twice from the identical substrate, the two outputs differ on exactly **72 lines = 36 added
nodes × 2**, and every one is a `unique_id=` value, which Godot randomises per session. No
transform, mesh, material or property differs. The scene banked in residue is run 1, the one every
frame and both instrument passes were made from.

### 4.7 `omni_range = 5.0` is invisible in the saved file

Godot omits properties at their default, and `OmniLight3D.omni_range` defaults to 5.0 — so the
authored range does not appear in the `.tscn` and a reader cannot tell it was set. It is read back
and printed by the census (`range=5.0000`) rather than left to the file to prove. Legibility
artifact, not a defect, but worth knowing before someone "fixes" a light that looks unauthored.

---

## 5 — Frames, and the descriptive diff

| file | what it is |
|---|---|
| `frames/L5D_MONEY_through-the-opening.png` | **the money frame.** Camera in the crypt on the room axis at eye height; opening in frame with both jambs and the lintel; chamber floor running out through it and the chamber's far wall legible beyond. |
| `frames/L5D_AFTER__box.png` | `__box` establishment, shot with `l4_shoot.gd` **unmodified**. Camera eye `(23.123901, 39.502224, 21.687008)` — identical to `l4_diff.py`'s constant, so the diff is valid. |
| `frames/DIAG_capsule-sweep_framing-held-__box.png` | G4 artifact: the swept capsule at 12 stations. Named for the variable it holds constant (TCP-36 ①): the **framing** is held at `__box` while the capsule's position varies. |

**The money frame's framing is derived, not eye-picked.** The camera stands on the room axis at
1.60 m and is dollied back until the *measured* aperture half-width fills a stated 55 % of the
frame half-width: `d = 1.0021 / (0.55 · tan(hfov/2)) = 2.8158 m` → camera `(0, 1.60, −6.1592)`,
pitch −7.09°, FOV 40° vertical. `__box` cannot take this shot and that is the point — at −50° of
pitch you look *over* the wall, never *through* the opening. All parameters are printed by the rig.

### 5.1 TCP-39 ③ — the scene has no clock in it

No tolerance is declared, because none is needed, and this was measured rather than assumed:

- **No animated occupant.** Node types in the built scene: 321 `MeshInstance3D`, 4 `Node3D`, 2
  `OmniLight3D`, 2 `DirectionalLight3D`, 1 `WorldEnvironment`. Zero `AnimationPlayer`,
  `AnimationTree`, particles, `Skeleton3D`, `CharacterBody3D`.
- **No temporal accumulator.** No TAA (absent from `project.godot`, defaults off), no SDFGI, no
  SSAO/SSIL/SSR. `fog_enabled = true` is **depth** fog (`fog_density`); Godot's temporally
  reprojected fog is `volumetric_fog_*`, which is absent.
- **Confirmed empirically:** re-rendering the same scene in a fresh process gives a
  **byte-identical** PNG, sha `4f51d447…`.

### 5.2 The numbers

Whole frame, `l4_diff.py` unmodified, noise floor 0:

```
changed_pixels     134294 of 2073600   =  6.476 %
changed bbox       x [1095, 1664]  y [0, 596]      <- ONE contiguous region
max_channel_delta  171
```

**Every changed pixel in the frame lies inside that one box, which is exactly where the opening
and the chamber are.** The other 93.5 % of the frame — the whole crypt floor, all four wall runs
but the doorway bay, the light pool, every pillar — is byte-identical. Of the 4356 changed pixels
outside a generous chamber box, the **maximum delta is 3**, i.e. the soft edge of the light spill.

**Read the mask with care.** `l4_diff.py`'s "addition envelope" is L4's frozen **dais** spec
(`x [−5, 5] y [−0.1, 4.2] z [−8.85, −2.35]`). My addition is at `z [−13.07, −8.75]` and lies almost
entirely *outside* it. So `outside_addition` in the JSON does **not** mean "outside my addition" —
it mostly *is* my addition. The differ was run unmodified as instructed and its mask is correct for
what it was frozen against; for this cell the **whole-frame** figure is the one that means anything.

### 5.3 The declared side effect, measured

R-5's chamber light spills through the opening onto the crypt floor. Predicted in §3 of the plan,
and now measured on the room axis:

| crypt floor z | before RGB | after RGB | delta |
|---|---|---|---|
| −8.60 (0.15 m inside) | 74.2 70.7 65.0 | 85.8 79.5 69.8 | **+11.5 +8.8 +4.8** |
| −8.00 | 73.8 70.6 65.0 | 81.0 75.9 67.8 | +7.2 +5.2 +2.7 |
| −7.00 | 73.9 70.3 64.7 | 75.8 72.1 65.5 | +2.0 +1.7 +0.9 |
| −6.00 and inward | — | — | **0 0 0, exactly** |

The spill is warm (ΔR > ΔG > ΔB, consistent with the copied `(1, 0.85, 0.62)`), peaks at the
threshold, and is **exactly zero from 2.75 m inside the crypt onward**. This is the addition's own
light, not damage — and it is a register cue in its own right: you see the glow before you see the
room. It is why I place it here rather than letting the diff imply the crypt was disturbed.

### 5.4 R-4 verified by pixel

The chamber's camera-near (+X) wall inherits run 2's materials. Sampled:

```
crypt  east wall, outer face   BEFORE (25.1, 29.8, 40.0)   AFTER (25.1, 29.8, 40.0)   <- identical
chamber +X wall, outer face    AFTER  (16.8, 18.7, 23.7)                              <- same family
chamber far wall, inner face   AFTER  (133.4, 119.3, 95.0)                             <- lit stone
```

The chamber's near wall reads dark-blue **because the crypt's own near wall reads dark-blue** —
these are outward faces receiving no direct light, falling to the scene's bluish ambient
`(0.1, 0.11, 0.14)`. That is R-4 delivering exactly what it claims: identical normal → identical
treatment → identical appearance. It also means the mitigation R-4 *predicted* (a faded near wall)
does not occur in a static frame, per §4.5 — the wall is solid, and it does occlude the chamber's
near side from `__box`. Logged veto-open below.

---

## 6 — Register cues: all seven, each as something checked

| # | cue | evidence |
|---|---|---|
| 1 | floor is one surface | 12 tiles of the substrate's **own** `ArrayMesh_51wnn` + `StandardMaterial3D_a4i48`; plate `x [−2.50, 2.50] z [−12.50, −8.75]`, phase-locked to 8.75 − 1.25n |
| 2 | no threshold | chamber floor top **0.008091** vs crypt **0.008090**; physics ray over 1201 samples: **max step 0.000000 m** |
| 3 | one wall-top plane | cap tops over **all 34 caps**, crypt and chamber together: `[3.169743, 3.169743]` — spread **< 1e−5** |
| 4 | one construction | 0.225 + 0.225 = 0.45 band, identical; corners left to a pillar as the crypt does; only 2 new meshes in the whole build |
| 5 | one material set | **zero** new materials, **zero** new shaders in the saved `.tscn`; inheritance by matching normal; verified by pixel in §5.4 |
| 6 | on the room's axis | portal centred `x [−1.2500, 1.2500]`; chamber centreline = crypt centreline |
| 7 | same light, own pool | colour and attenuation copied from `InteriorPool` **at runtime**, not transcribed; `InteriorPool` verified untouched (range 9.0, energy 3.4) at build and at reload |

---

## 7 — Rulings logged at build time, all veto-open

Phase A's R-1…R-7 stand as filed; Matt confirmed R-1, R-3 and R-7. New this phase:

- **R-8 — chamber nodes go in the substrate's own role holders (`Floor`/`Walls`/`Pillars`), with a
  `Ch` name prefix, not in a `Chamber` holder of their own.** The substrate's holders are typed by
  *role*, not by room. A separate holder would encode "this is a different place" in the scene tree
  — the exact thing the brief says not to do — and the name prefix already gives the census
  everything it needs to separate them. *Veto if:* a downstream consumer needs the addition to be
  detachable as a unit, in which case a holder is cheaper than a name filter.
- **R-9 — collision is generated at sweep time, not shipped in the scene.** The substrate ships
  presentation and no collision; the built scene does the same. G4 builds 320 trimesh bodies from
  the visible geometry plus one authored proxy, inside the sweep process. This measures the
  geometry *as shipped* rather than a hand-authored guess, and keeps the presentation artifact a
  presentation artifact. *Veto if:* the (i) cells are to be handed a scene that is walkable out of
  the box, in which case collision generation becomes a build step and the scene doubles in node
  count.
- **R-10 — the opening module's collision is the kit's authored proxy; its render mesh is excluded
  from the physics world entirely.** The proxy's hole is 4.9 cm narrower and 3.3 cm lower than the
  visible one. Sweeping the render would overstate clearance by that much. Confirmed by the box
  probe: measured 1.9544 vs proxy 1.9553, vs visual 2.0042.
- **R-11 — `ChamberPool` range 5.0, everything else copied.** Colour, energy and attenuation are
  read off `InteriorPool` at runtime. Range is the single authored number, chosen so the chamber's
  floor-centre illuminance matches the crypt's: Godot's omni falloff at d = 2 gives
  `(1 − (2/5)⁴)² · 2^−1.3 = 0.3856` against the crypt's `0.4042` — **95.4 %**. *Veto if:* the spill
  through the opening (§5.3) is unwanted; a smaller range removes it and darkens the chamber, and a
  larger one lights the crypt's north end. There is no range that does neither.
- **R-12 — the half-width side-wall panel goes at the FAR end of both side walls.** The kit's run
  direction is mirrored between the ±X walls, so the natural tiling puts the seam at the far end on
  one side and the near end on the other. Forced symmetric: seam at `z = −11.25` on both.

---

## 8 — Anything in the dispatch that steered me

The dispatch asked to be checked. **Two things steered, one of them productively and one worth
watching:**

1. **§2.3's "the kit's collision hole is 4.9 cm narrower than its visible one" is my own Phase A
   finding handed back to me as an instruction.** That is legitimate — it is my measurement, and
   restating it as a binding constraint is the conductor doing his job. But it is worth naming that
   **a Phase-B dispatch which quotes Phase A's findings back can make them unfalsifiable.** Had my
   Phase A proxy measurement been wrong, §2.3 would have instructed me to preserve the error. I
   re-measured it independently in Phase B — the box probe returned 1.9544 against the rasteriser's
   1.9553 — so it survives, but the survival is because I checked, not because the dispatch let me.
   **Recommendation: when a Phase-B dispatch restates a Phase-A finding as a constraint, mark it as
   "your own, re-verify" rather than as a given.**

2. **§2's numbering steered the shape of my work more than its content.** Eight numbered gates
   ordered census → floor hole → G4 → door → frames → diff → vacate → blast radius is very close to
   the order I executed in, and I did not seriously consider a different one. That is mostly fine —
   the dependencies mostly force it — but the G4 sweep would have been *better* run before the
   frames, because it is the gate most likely to fail and the most expensive to re-shoot around.
   I got lucky that it passed.

**What did NOT steer:** §0's rulings are Matt's verbatim words, and R-3's "an opening, not a door:
no leaf, no hinge, no door furniture" closed a design question rather than answering a measurement
question — that is an owner decision arriving as an owner decision, which is the correct shape.
§2.2's "how you fix it is a recipe clause" told me the *form* the answer had to take without
telling me the answer, which is the useful kind of instruction and is why §3 above is written as a
rule rather than as a description of what I did.

**Still standing from Phase A, unaddressed:** `L4_KIT_CONSTANTS.md` §6 pins L4's two-brazier
dressing decision inside the natives file. Any future arrival cell reading it for module
measurements is handed a design decision by adjacency. It should be split before that file is
handed to another (ii) cell.

---

## 9 — Where everything is

```
~/Games/mcp-lab/evidence/l5/l5d/
    SITING_PLAN.md                 Phase A — the spec (its §3 transpose note is WRONG; see §4.1)
    FIRST_INTENT_BANKED.md         Phase A
    MEASURED_DOOR_MODULES.txt      Phase A — module + proxy natives
    CONCURRENT_REPO_BASELINE.txt   Phase A
    BUILD_LOG.txt                  Phase B — every build-time assertion
    RELOAD_CENSUS.txt              Phase B — gate 1, all six sections
    G4_SWEEP.json                  Phase B — gate 3, incl. the retired capsule bisection
    frames/L5D_MONEY_through-the-opening.png       THE MONEY FRAME
    frames/L5D_AFTER__box.png                      establishment (l4_shoot.gd unmodified)
    frames/DIAG_capsule-sweep_framing-held-__box.png
    diff/L5D_DIFF.json + _DIFF.png + _DIFFx4.png + _DIFFx4_MASKED.png
    rigs/                          l5d_build, l5d_census, l5d_sweep, l5d_money (+ Phase A rigs)
    PROBE_*.png                    Phase A

~/Games/mcp-lab/prep/l5d_residue/
    README.txt                     vacate record + how to re-enter
    l5d_scene_after.tscn           THE BUILD, sha c7b9e950…
    user_logs/                     5 engine logs relocated out of user://
```

---

## 10 — For the conductor

**Nothing needs a HALT.** Nothing re-scopes the lap. Two items are worth carrying forward into the
contract the (i) cells will be handed:

1. **§4.1 is a hazard for every cell that authors transforms in GDScript.** The `.tscn` 12-float
   form has no script constructor, so translation is mandatory, and a transposed reading passes
   silently on axis-aligned bases. The mitigation that worked is cheap and mechanical: **harvest
   bases from the live node, never retype them, and keep the transcription only as a gate.** That
   belongs in `CALIBRATION.md` next to the TCP-23 latch note from Phase A.
2. **§4.3 is a second entry for the same file.** A probe whose dimensions are coupled cannot
   measure a gap on the uncoupled axis, and a bisection over a coupled probe returns a beautifully
   precise measurement of the probe. Any future clearance question should be asked with a shape
   whose measured axis is free.

**Honorable fallback was not needed.** No blocker was hit that survived the cell.

---

**Signed:** drax, presentation seam, 2026-07-25.
