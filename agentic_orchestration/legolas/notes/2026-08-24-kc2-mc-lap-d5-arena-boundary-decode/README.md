# KC2 MODEL-COMPLETION RUN · Wave 1 · piece **D-5** — THE ARENA-BOUNDARY DECODE

**Date:** 2026-08-24 · **Agent:** legolas (UNKNOWN-RESEARCHER) · **Conductor:** gandalf (RUN-CONDUCTOR)
**Commission:** charter `agentic_orchestration/gandalf/notes/2026-08-24-kc2-model-completion-run-charter.md`, ledger **L-15**
**Discipline:** GL-12 DECODE-NEVER-ESTIMATE · Law 3 · READ-ONLY on every external source · FULL sha256 on every input
**Instrument:** `agentic_orchestration/research/scripts/mcd5_arena_boundary_2026_08_24.py` — every number below is emitted by that file, none retyped
**Evidence:** `evidence/` (`decode.log`, `d5_findings.json`, `A001_heightfield_129x129.npy`, `A001_placements.json`, `A001_dbr_pathing.json`, `slope_impassable.disasm.txt`)

---

## 0 · VERDICT

> **`UNREACHED-S8` is now PARTLY CLOSED and the residual is RE-AIMED, not merely restated.**
>
> **(a) The arena's terrain IS decoded** — 129 × 129 float32 heightfield, 1.000 m cells, located inside
> `Region_Survival_A001.lvl`, with a world-coordinate mapping *validated to 3.92 mm* against 65
> ground-anchored entity placements.
>
> **(b) The engine's terrain-impassability rule IS decoded** — `Terrain::SlopeImpassable`,
> Engine.dll RVA `0x18c120`, with both float constants read out of `.rdata`:
> `impassable(i,j) ⇔ max_k |h_k − 0.25·Σh| > 0.600000023841858 m` over the cell's four corners.
>
> **(c) Applying (b) to (a) returns a NEGATIVE, and it is threshold-independent:**
> **⚑ THE TERRAIN DOES NOT CLOSE THE CRUCIBLE ARENA.** The passable region reachable from the
> `PatrolPoint_Attack` centroid **reaches the region edge on all four sides at every threshold
> from 0.30 m to 2.00 m** — a 6.7× sweep around the decoded value. There is no terrain wall ring.
>
> **(d) What actually closes it is entity collision, and that is the residual.**
> **341 of 483** A001 placements carry `Decoration.allowPathing = False`, and **336 of those 341
> carry `actorRadius = 0.0`** — meaning their blocking extent is taken from the mesh, and `.msh`
> (magic `MSH\x03`, `Level Art.arc`) was not opened by this lap.
>
> **Therefore, for facet (h): the arena boundary is `UNDECODABLE-FROM-SUBSTRATE-IN-THIS-LAP`,
> with the path named to the file and the format (§ 5).** No boundary polygon is offered. No
> rectangle is blessed. The fallback fork **S-1 stands and is Matt's to rule.**
>
> **⚑ THE FINDING UNDER THE FINDING.** The C-1 caveat said the quoted rectangle is a construction
> rather than a decode. This lap establishes something stronger and more useful to the ruling:
> **the real boundary is not an authored object anywhere in the shipped data.** No bounds field, no
> blocker entity, no Lua leash, no stored impassable map, no navmesh on disk (§ 4.4). Even a
> successful future lap will *derive* the boundary from mesh collision, not read it. Whatever Matt
> rules, "walls as decoded truth" will always mean *walls as a reconstruction from decoded inputs* —
> and the honest baton row is therefore a derived-geometry row with its derivation pinned, not a
> quoted rectangle.

---

## 1 · Inputs — re-hashed before use, HALT-on-mismatch

| input | sha256 | verdict |
|---|---|---|
| `vendor/grim-dawn/Engine.dll` | `7141b51ae61b396fd0743da9e51471043329c51b3bb61d0037b2ce934864c87c` | **PIN MATCH** (Lap S / D-1) |
| `vendor/grim-dawn/Game.dll` | `4876d6bdb69cca71cfa987652cbd7a42cf6d5578564d02d09aaf9b55c078ab02` | **PIN MATCH** |
| `…edition-III/survivalmode1/resources/Maps.arc` | `2f5b34fe914e26d6fadda88aebd4080d172dc92b8d66ac990c3e108e05821237` | **PIN MATCH** (Lap S) |
| `…edition-III/survivalmode2/resources/Maps.arc` | `cef96030be9bdc9be64bf187389aeccec6552ba1cfde30d1c63d716d2f6dbaec` | **PIN MATCH** |
| `…edition-III/survivalmode3/resources/Maps.arc` | `94e20abadfce0f92d5187ab20bb8a9510fca9163e2b5b67b038cb55953f34911` | **PIN MATCH** |
| `…edition-III/mods/survivalmode/resources/Maps.arc` | `5377259861ad5c17a6009ae045ebc94612faca9a65bc14904b193b9c6d4fa708` | recorded |
| `…edition-III/database/database.arz` | `2ad6d379285cfb745462316949e8d59e9450cb58a13f9ffa2fdeb70193183bfd` | recorded |
| `…edition-III/survivalmode1/resources/Scripts.arc` | `27d0c258d1b6dc6017d1b0e68385a67913f73e019196aaeb7f81c28b40f52278` | recorded |
| `vendor/grim-dawn/resources/Level Art.arc` | `e33e3b93b89c4f4d1bfdbf6fbd3223e097ebea7941a45a0b16a86f173a4a8f33` | recorded — **the residual's home** |

⚑ **Provenance note for the follow-on lap.** `Level Art.arc` (848 MB, 4,215 members) exists **only in
the older full install `/Users/admin/Games/vendor/grim-dawn/` (2026-07-23 vintage)**. The pinned
Edition-III tree ships only `Creatures/Levels/Scripts/Text_EN.arc` — it has **no level-art depot**.
Any mesh-collision lap must either accept the older tree's vintage (and say so) or re-pin depot 219991.

---

## 2 · The `.lvl` region format — decoded past Lap U's header

Lap U (`pm4u_lvl_regions.json`) decoded the region **container**: the seven `Region_Survival_A00n.lvl`
blobs embedded in the `.map`, their exact tiling, and the `LVL\x0f` magic. This lap decodes the
**contents**:

```
LVL region blob
  +0    b'LVL\x0f'
  +4    6 × f32          two points, NOT the region AABB   (see R-3)
  +28   u32  flag        == 5 on every survival region seen
  +32   u32  entity_section_size     → entity section ends at 40 + this   [ARITHMETICALLY CHECKED]
  +36   u32  string_count
  +40   string table: [u32 len][ascii `.dbr` path] × string_count
        u32 placement_count | u32 (0)
        placement records — TWO VARIANTS:
           56 B  [9 × f32 row-major rotation][3 × f32 world position][u32 flags][u32 string_index]
           72 B  as above + a 16-byte GUID  ← the members of a NAMED GROUP
        [u32 key][u32 size][payload] property list
        [u32 W = 129][u32 D = 129][ W·D × f32 TERRAIN HEIGHTFIELD ]
        [ per-vertex layer bitmask bytes ][ per layer: [u32 len][terrain-texture path][opacity bytes] ]
```

`survivalmode1/survivalworld_a.map :: Region_Survival_A001.lvl` @ 1 839 979 (1 076 532 B):
117 strings · **494 declared placements, 494 parsed** (483 plain + 11 group-member) ·
heightfield at blob + `0xdee6`, range **−0.4102 … 18.2090 m**.

### 2.1 ⚑ The 72-byte variant reconciles a standing inconsistency

The 11 GUID-carrying records are the **`PatrolPoint_Attack` group members**, and they match the
sim's own patrol CSV **to 0.0000 m on all 11 points**. Their group centroid is
**(81.2601, 64.3606)** — the sim's `centroid_xz`, reproduced from the region bytes to **0.042 mm**.

This matters because the *plain* `patrolpoint_01` records in the same region are a **different
population** of 11 points with centroid **(83.5817, 63.0754)** — which is what Lap S's
`pm4s_arena_placements.csv` counted, and it is 2.65 m away. Both populations validate against the
heightfield (median |Δy| 6.0 mm and 3.7 mm), so both are real placements.

> **⚑ The sim's declared reference frame is CONFIRMED, not merely assumed.** `locomotion.py`'s
> `arena_centre` is the centroid of the *named group*, which is the set `tier16waves.lua` actually
> links packs to. Lap S's "8–11 patrol points per arena" counted the *other* set. Two different
> quantities that have been carrying one name.

---

## 3 · The heightfield's world mapping — fitted, then validated

| item | value |
|---|---|
| grid | 129 × 129 vertices, **cell = 1.000 m** |
| mapping | `world_x = col − 4.00` · `world_z = row + 0.00` (row indexes z, column indexes x) |
| **validation** | **median \|H(x,z) − y_placement\| = 3.92 mm** over **65** ground-anchored placements |
| optimum | **unique** — the runner-up offset in a ±40 m × ±40 m sweep scores 0.0678 m, 17× worse |
| independent cross-check | the sim's own 11 `PatrolPoint_Attack` rows (a *different* population): **median 3.67 mm** |

The mapping is therefore not fitted-and-asserted; it is fitted on one population and confirmed on
a second that had no part in the fit.

### 3.1 A correction owed to Lap U

Lap U graded a float array at `region0 + 0x1c000` **INFERRED-WITH-EVIDENCE — consistent with a
terrain HEIGHT field**, on the test that 0.87 of finite floats lay in [0, 40] m. **That reading is
refuted.** The bytes there are a constant `0x03030303` fill, which decodes as the denormal
`3.85e-37` — a positive float below 40, so it passes the band test vacuously. Lap U's own guard
held (it was explicitly not called a decode and no value was consumed anywhere), so nothing
downstream is contaminated; the record is corrected here for the ledger. The real heightfield sits
**53 KB further in**, at `+0xdee6`, and is contiguous f32 — not the interleaved 8-byte-per-vertex
layout that `Terrain::Load` reads (see R-1).

---

## 4 · The impassability rule — decoded from Engine.dll bytes

`?SlopeImpassable@Terrain@GAME@@AAE_NHH@Z`, RVA `0x18c120` (VA `0x1018c120`), full listing in
`evidence/slope_impassable.disasm.txt`:

```
i0 = clamp(i,0,W)  j0 = clamp(j,0,D)  i1 = clamp(i+1,0,W)  j1 = clamp(j+1,0,D)
avg  = (h(i0,j0) + h(i1,j0) + h(i0,j1) + h(i1,j1)) * K      ; mulss  [0x102e04c8]  K = 0.25f
                                                            ; andps  [0x102e0e40] = 0x7fffffff (abs)
return  ∃k : |h_k − avg| > T                                ; comiss [0x102e0538]  T = 0.600000023841858f
```

Four `comiss` / `ja` pairs, one per corner; `xor al,al` on fall-through, `mov al,1` on the taken
branch. **Both constants are read out of `.rdata` by the instrument, not typed by hand.**

### 4.1 The sweep — the negative is threshold-independent

Flood-fill (4-connected) from the arena-centre cell (64, 85):

| T (m) | impassable frac | reachable cells | sim-frame x span | sim-frame y span | reaches region edge |
|---:|---:|---:|---|---|---|
| 0.30 | 0.3060 | 8 583 | [−81.3, +42.7] | [−58.4, +63.6] | **yes** |
| 0.45 | 0.2029 | 10 010 | [−81.3, +42.7] | [−58.4, +63.6] | **yes** |
| **0.600 (decoded)** | **0.1325** | **13 516** | **[−85.3, +42.7]** | **[−64.4, +63.6]** | **yes** |
| 0.80 | 0.0879 | 14 599 | [−85.3, +42.7] | [−64.4, +63.6] | **yes** |
| 1.20 | 0.0508 | 15 517 | [−85.3, +42.7] | [−64.4, +63.6] | **yes** |
| 2.00 | 0.0214 | 16 034 | [−85.3, +42.7] | [−64.4, +63.6] | **yes** |

Sim frame = level (x, z) minus the `PatrolPoint_Attack` centroid, per `locomotion.py:350`.
At the decoded threshold **82.5 %** of the 128 × 128 m region is terrain-passable and the reachable
set is bounded only by the region's own edge. **No number in this table is a boundary and none is
offered as one.**

### 4.2 · 4.3 · 4.4 — the four negative results, each searched for and each absent

| # | what was looked for | where | result |
|---|---|---|---|
| N-1 | an arena-bounds / playable-region field | `.map` head, all 7 `.lvl` region headers, `Region`/`Level` export surface | **absent** — no such field exists |
| N-2 | an invisible-wall / blocker entity placed in the arena | all 127 distinct `.dbr` paths in `survivalworld_a.map`, regex `block\|wall\|collis\|barrier\|bound\|invis\|fence\|clip\|nav` | **absent** — the single hit, `stalagmitecluster_blockermedium01`, is a stalagmite prop |
| N-3 | a scripted leash / bounds check | all 11 + 10 Crucible Lua modules in `survivalmode{1,3}/resources/Scripts.arc`, regex `bound\|leash\|arena\|Teleport\|radius\|Distance\|Extents` | **absent** — the only `Player.Teleport` calls are the wave-start and treasure-room hops |
| N-4 | a stored impassable / nav map | scan of both A001 (arena) and A006 (near-empty control) for any 0/1 byte array ≥ 4 000, and for a (W−1)(D−1)·4 = 65 536 B u32 array | **absent in A006 entirely** ⇒ the `.map` does not carry it |

**N-4's corroboration from the code.** `Terrain::Load` (RVA `0x187740`) *allocates* `(W−1)·(D−1)`
bytes for the impassable buffer at `this+0x64` and, in its runtime-format branch, fills it by
reading one u32 per cell. `Terrain::IsImpassable` (RVA `0x18c240`) reads exactly that buffer at
`v·(W−1)+u`. But the `.map`'s terrain block is the **editor/`Save` layout** (contiguous f32
heights — proved by § 3's 3.92 mm validation, which is impossible under an 8-byte interleave), and
no such array is present in it. On the nav side, `NavMesh` has **`NavMeshBuilder::Create(const
Level*, NavMesh*&)` and no `NavMesh::Load`** — navigation is built at load, never shipped.

---

## 5 · The residual, aimed precisely

`Decoration` records carry `allowPathing` (bool) and `actorRadius` (float). Resolving **all 115**
placed `.dbr` paths across seven ARZ layers (**0 unresolved**, incl. `mods/survivalmode/database/SurvivalMode.arz`):

| quantity | value |
|---|---|
| A001 plain placements | 483 |
| **placements with `allowPathing = False`** | **341** |
| of those, `actorRadius` **> 0** (authored blocking disc) | **5** — 4 × 1.80 m (`stalagmitecluster_{blockermedium01,medium01}`), 1 × 1.00 m (`door_stepsoftorment_epicdoor_frame`) |
| of those, `actorRadius = 0.0` (extent comes from the mesh) | **336** |

So five authored discs cannot ring a 128 m chamber; the wall is 336 meshes. **The named path for a
follow-on lap, in order:**

1. **`Level Art.arc` → `<name>.msh`, magic `MSH\x03`.** Present and readable; e.g.
   `undergrounds/natural/stalagmitecluster_long03.msh` = 391 959 B. Format **not opened** — this is
   the one genuinely new container in the chain.
2. **Extract each mesh's bounding box.** `Entity::OccludesPathing` → `ImpassableData::AddEntity` →
   `ImpassableData::AddBox(int, const OBBox&, bool)` (Engine.dll). The engine blocks with **oriented
   bounding boxes, not triangle soup**, so a per-mesh AABB + the placement's 3×3 rotation is
   sufficient — full mesh geometry is *not* required. That is the single fact that makes this
   tractable in one lap.
3. **Compose.** 341 OBBs (already in hand: rotation + position + dbr, `evidence/A001_placements.json`)
   ∪ the terrain-impassable mask (already in hand, § 4) → flood-fill from the centroid → boundary polygon.
4. **Validate before publishing.** Falsifiable acceptance test available for free: all six emitters,
   all 22 patrol points and the player spawn must be *inside*; the referent's own observed footprint
   (player ≤ 22.2 m, monsters ≤ 43.6 m from the centroid, gamora C-1 § 3.1) must be inside; and the
   boundary must be *closed*, i.e. must NOT reach the region edge — which is exactly the property
   terrain alone fails.

Estimated shape of that lap: one new format (`MSH` header + bbox), no new engine-rule decode.
**Steps 1–4 are the whole of what stands between the run and a decoded facet-(h).**

---

## 6 · `NAMED-I26-1` (sm1 vs survivalmode3) — bonus, and it resolves in two directions

All three layers ship `survivalworld_a.map`. `Region_Survival_A00{2..7}` are **byte-identical**
across `sm1` / `sm3` / `mods`; only A001 and the map head differ (by ~443 and ~919 B).

| | sm1 | sm3 | sm_mod |
|---|---|---|---|
| A001 placements | 494 | 498 | 491 |
| `PatrolPoint_Attack` members | 11 | 11 | 11 |
| group centroid (= the sim's frame origin) | (81.2601, 64.3606) | (81.4449, 64.4246) | (81.2601, 64.3606) |
| **heightfield sha256** | `0b2d98fb7fcb1dd6…` | **identical** | **identical** |

**(a) For geometry and for the sim's frame, the disagreement is immaterial.** The terrain is
byte-identical; the frame origin moves **0.196 m**.

**(b) For the emitter ring, it is NOT immaterial:**

| emitter | sm1 (x, z) | sm3 (x, z) | Δ |
|---|---|---|---:|
| `tier16spawnpoint01` | (46.81, 73.95) | (47.19, 73.98) | 0.38 m |
| `spawnpoint02` | (90.60, 32.90) | (90.60, 32.90) | 0.00 m |
| `spawnpoint03` | (89.39, 96.73) | (70.76, 94.08) | **18.81 m** |
| `spawnpoint04` | (112.17, 71.51) | (112.17, 71.51) | 0.00 m |
| `spawnpoint05` | (74.44, 66.54) | (93.47, 63.60) | **19.26 m** |
| `spawnpoint06` | (112.47, 71.17) | (108.75, 88.09) | **17.33 m** |

**Three of six emitters move by 17–19 m between the layers.** `p05` in particular moves from
r = 7.16 m to r = 12.05 m from the arena centre — a 68 % change in the ambush emitter's radius, on
the emitter the sim's own `emitter_radius_m` reads.

**What this lap does NOT resolve:** which layer the *runtime* mounts. The three `survivalmode{1,2,3}/resources`
literals sit adjacent in `Engine.dll` at **file offsets** `0x2a7f88`, `0x2a7fa0`, `0x2a7fc0` — i.e.
in **string-pooling order, which is not mount order** (note it reads 2, 3, 1) — and no disassembly
of the mounting function was attempted. Two facts bear on it and are recorded rather than concluded from: `sm3` ships a
**complete** 10-map set plus `tier17..tier20` waves, while `tier16waves.lua` — the module that
governs waves 151–160 — **ships only in `sm1`**.

> **Ruling shape for the conductor.** `NAMED-I26-1` is **narrowed, not closed**: measured-immaterial
> for the arena frame and terrain (Δ ≤ 0.196 m, heightfield identical), measured-**material** for
> the emitter ring (three emitters, 17–19 m). The residual is a one-function disassembly of the
> archive-mount order in `Engine.dll` — small, and now worth doing, which it was not before this
> measurement.

---

## 7 · Residuals opened by this lap (named, so they are not silently inherited)

| id | residual | why it is open | what closes it |
|---|---|---|---|
| **R-1** | the `.map` terrain block is the `Save` layout, not the `Load` layout | `Terrain::Load` reads interleaved `(f32 height, u32 flag)` at 8 B/vertex; the file is contiguous f32 (proved by § 3). `Terrain::Save` / `SaveRunTimeFormat` were only partly read | finish `Terrain::Save` (RVA `0x187e50`) — bounded, ~0x600 B |
| **R-2** | the 72-byte placement variant's **string-index offset** is unresolved | its positions are exact (0.0000 m vs the sim's group), but reading the index at +52 or +68 both yield unrelated records | the group table in the `.map` head names the record; or finish the head-section group parse |
| **R-3** | the 6 floats at LVL `+4` are **not** the region AABB | A004's pair is degenerate in x and z, A002's in x and y — the shape of region-connection portals, not a box. Lap U published these as `header_aabb` | `Region::GetBoundingBox` / portal load path |
| **R-4** | `Terrain::SlopeImpassable` has **no direct caller** in `.text` (E8/E9 scan and abs-VA scan both empty) | so the *binding* of the decoded rule to the `.map` load path is **INFERRED-WITH-EVIDENCE**, not decoded: it is the only shipped height-based impassability predicate, and § 4.4 shows nothing is stored. Graded, not asserted | find the inlined recompute that writes `this+0x64` |
| **R-5** | the six `.map`-head `262 188`-byte per-region blobs are **presumed** minimap/aerial textures | identified by arithmetic only (7 × 262 188 + 4 655 = the head's exact size); contents not opened | irrelevant to (h) — recorded so it is not re-chased |

**None of R-1…R-5 is load-bearing for § 0's verdict.** The verdict rests on § 3's 3.92 mm
validation, § 4's read-from-`.rdata` constants, § 4.1's threshold-independent sweep, and § 5's
341/336 count — each of which is independent of every residual above.

---

## 8 · What this lap did NOT do

- Did **not** open `.msh`. No mesh geometry, no bounding boxes, no OBB composition.
- Did **not** emit a boundary, a polygon, a rectangle, a radius or a hull. Not at the decoded
  threshold, not at any other.
- Did **not** bless the 86.915 × 85.303 m rectangle, and did not replace it. It remains what C-1
  found it to be.
- Did **not** touch the sim, the checkpoint, the baton, or any engine file. The only reads outside
  the vendor trees were `data/kc2/kc2_crucible_patrolpoints.csv` and `simulation/kc2/locomotion.py`,
  both read-only, both for the § 2.1 cross-check.
- Did **not** determine the archive mount order (§ 6), and says so rather than leaning.

---

*KC2-MC Wave 1 · piece D-5 · legolas · 2026-08-24. Commit prefix `legolas(KC2-MC D-5):`. Committed, not pushed.*
