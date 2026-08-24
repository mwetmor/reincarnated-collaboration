# KC2 MODEL-COMPLETION RUN · Wave 1 · piece **D-5b** — THE `.msh` DECODE + BOUNDARY DERIVATION

**Date:** 2026-08-24 · **Agent:** legolas (UNKNOWN-RESEARCHER) · **Conductor:** gandalf (RUN-CONDUCTOR)
**Commission:** charter `agentic_orchestration/gandalf/notes/2026-08-24-kc2-model-completion-run-charter.md`, ledger **L-19**
**Predecessor:** `agentic_orchestration/legolas/notes/2026-08-24-kc2-mc-lap-d5-arena-boundary-decode/README.md`
**Discipline:** GL-12 DECODE-NEVER-ESTIMATE · Law 3 PARSE-DON'T-GUESS · READ-ONLY on every source · FULL sha256 on every input
**Instrument:** `agentic_orchestration/research/scripts/mcd5b_msh_boundary_2026_08_24.py` — every number below is emitted by that file, none retyped
**Evidence:** `evidence/` (`decode.log`, `d5b_findings.json`, `msh_mesh_table.csv`, `composition_sweep.csv`, `anchor_diagnosis.csv`, four `.npy` rasters)

---

## 0 · VERDICT — split, because the commission had two halves and they came out differently

> ### (A) THE FORMAT TARGET: **MET.** `MSH\x03` is DECODED, and further than the commission asked.
>
> Seven chunk ids, the whole chain, **self-validating**: chunk 10's AABB is **bit-exact equal to the
> chunk-4 vertex extremes on 27/27 blocking meshes and 399/400 randomly-sampled Level-Art meshes**,
> and chunk 5's maximum index equals `n_vert − 1` on the same populations. The parse proves itself
> against the file rather than against my expectations.
>
> **⚑ And the commission's hedge — "or the collision-relevant sub-block if the format carries one" —
> lands. It carries one.** **Chunk 8 is a hitbox OBB array**: `[u32 n]` then n × 96 B of
> `(32 B name | 3 f32 half-extents | 3×3 f32 rotation | 3 f32 centre | u32 0xFFFFFFFF)`. That is
> exactly the object `Entity::GetHitBox(int)` hands `NavMeshBuilder::AddBox`. 453 OBBs across the
> 341 blocking placements (37 distinct OBBs across 25 of the 27 meshes). **And it cross-validates
> against a chunk decoded independently:** over the 15 single-hitbox meshes, `stalagmite_single01`'s
> OBB centre reproduces its chunk-10 AABB centre with a y-delta of **exactly 0.000000** m.
>
> ### (B) THE GEOMETRY TARGET: **NOT MET — `UNDERIVABLE-WITH-PATH-NAMED`.**
>
> All the inputs are now in hand — 620,182 triangles, 453 hitbox OBBs, 27 mesh AABBs, 341 placement
> rotations, the terrain heightfield, the engine's own nav cell size. **I composed them 24 ways and
> every one fails.** Not "looks wrong" — *fails a test D-5 itself pre-registered* (§ 5 step 4:
> emitters, patrol points and the player spawn must be inside; the region must be closed).
>
> **⚑ NO CELL IN THE 24-CELL SWEEP IS BOTH CLOSED AND ANCHOR-COMPLETE**, and the failure is not
> marginal. At the most engine-faithful cell, **three anchors the shipped game demonstrably uses —
> including `tier16spawnpoint01`, THE tier-16 emitter — land inside blocking geometry.** A monster
> emitter cannot be inside a wall. The composition is **falsified by the game's own data**, not by
> my judgement. **No boundary is offered. No polygon. No radial profile. Nothing was published that
> could not survive its own acceptance test.**

> **⚑ THE FINDING UNDER THE FINDING — and it retires the whole D-5b hypothesis, not just this lap.**
> D-5 said: *what closes the arena is entity collision.* **Measured, that is false.** The 341
> blocking placements are not a wall ring; they are a **field**. Distance from the arena centroid:
> min 4.7 m · p10 21.6 m · **median 48.0 m** · p90 76.4 m · max 100.7 m, with a 10 m-bin histogram
> of `[10, 24, 29, 72, 44, 55, 44, 42, 19, 1, 1]` — no annulus holds a dominant share; there are
> ten blockers inside 10 m of the arena centre. **They are scenery scattered through a cave, and
> the Crucible fight happens among them.** D-5's residual pointed at a wall that does not exist.

**Consequence for facet (h):** D-5's HALT-deferral condition ("while a bounded derivation path
remains") is now **discharged and exhausted**. The bounded path was taken, the format fell, and the
boundary still did not follow. **The L-13-batched Matt brief should fire**, now with a complete
search record: no bounds field, no blocker entity, no Lua leash, no stored nav map, no baked
impassable array, no wall ring, and no composition of the real geometry that survives validation.

---

## 1 · Inputs — re-hashed before use, HALT-on-mismatch

| input | sha256 | verdict |
|---|---|---|
| `vendor/grim-dawn/Engine.dll` | `7141b51ae61b396fd0743da9e51471043329c51b3bb61d0037b2ce934864c87c` | **PIN MATCH** (D-5) |
| `vendor/grim-dawn/resources/Level Art.arc` | `e33e3b93b89c4f4d1bfdbf6fbd3223e097ebea7941a45a0b16a86f173a4a8f33` | **PIN MATCH** (D-5) |
| `…edition-III/survivalmode1/resources/Maps.arc` | `2f5b34fe914e26d6fadda88aebd4080d172dc92b8d66ac990c3e108e05821237` | **PIN MATCH** (D-5) |
| `…edition-III/mods/survivalmode/resources/Creatures.arc` | recorded in `d5b_findings.json` | new this lap |
| `…edition-III/database/database.arz` | recorded | recorded |

⚑ **A depot D-5 did not name.** `defense_floorgrate01a.msh` — the mesh behind the 9 `chestmarker_*` /
`defensemarker_01` blockers — is **absent from every base-game archive** and lives only in
`mods/survivalmode/resources/Creatures.arc`. Any future mesh lap needs both trees, not just
`Level Art.arc`.

---

## 2 · `MSH\x03` — the format, decoded

```
+0    b'MSH\x03'
+4    flat chunk chain, closing EXACTLY at EOF:   [u32 chunk_id][u32 size][payload]

 id  4  VERTEX BUFFER  [u32 n_stream][u32 stride][u32 n_vert][u32 stream_type × n_stream]
                       then n_vert × stride bytes.  POSITION = the first 3 f32 of each vertex.
                       (observed stride 56 = pos 12 + uv 8 + three 12-byte vectors; stream_type
                        codes 0,4,1,2,3)
 id  5  INDEX BUFFER   [u32 n_tri][u32 n_submesh][u16 index × 3·n_tri][44 B × n_submesh tail]
 id  7  MATERIAL LIST  [u32 n] then len-prefixed shader path + typed named properties
 id  8  HITBOX OBB ARRAY   [u32 n] then n × 96 B:
                       [32 B NUL-padded name][3 f32 half-extents][3×3 f32 rotation]
                       [3 f32 centre][u32 0xFFFFFFFF]
 id 10  AABB           [6 f32] = min.xyz, max.xyz  — the EXACT vertex extremes
 id 13  [u32][u32]     id  6  [u32]      id  2 / id 3 / id 0  (present on some meshes, not opened)
```

### 2.1 The parse validates itself — three independent falsifiers, all survived

| check | blocking meshes (27) | random Level-Art control (400 of 3,360) |
|---|---|---|
| chunk chain closes exactly at EOF | **27/27** | **400/400** |
| chunk-10 AABB == chunk-4 vertex extremes, **bit-exact, 6/6 floats** | **27/27** | **399/400** |
| chunk-5 max index == `n_vert − 1` | **27/27** | **399/400** |

The AABB test is the strong one: it is a *cross-chunk* identity. If the vertex stride, the stream
header, the position offset, the AABB offset **or** the chunk walk were wrong, it would not hold —
and it holds to the bit on 426 of 427 files. (The single control miss is one mesh out of 400; not
chased, recorded.)

### 2.2 A scale falsifier, because "is this metres?" was a live risk

`creatures/pc/hero01.msh` — the player character — has AABB y `−0.019 … 2.537`, i.e. **2.556 m**,
against a decoded `agentHeight` of **2.0 m** (§ 3). Mesh units are world metres. The rocks really
are that big; the over-blocking in § 5 is not a unit error.

---

## 3 · The engine chain — **D-5 § 5 step 2 CORRECTED**

D-5 named `Entity::OccludesPathing → ImpassableData::AddEntity → ImpassableData::AddBox(int, const
OBBox&, bool)` and concluded "the engine blocks with oriented bounding boxes, not triangle soup."
**In this shipped build all of those are ICF-folded empty stubs:**

| symbol | RVA | first bytes | meaning |
|---|---|---|---|
| `ImpassableData::AddEntity` | `0xa0a0` | `c2 08 00` | `ret 8` — **empty** (12 export names fold here) |
| `ImpassableData::AddBox` | `0x10be0` | `c2 0c 00` | `ret 0xc` — **empty**, and **0 callers in `.text`** |
| `Entity::GetCollisionBox` | `0xaab0` | `32 c0 c2 04 00` | `xor al,al; ret 4` — returns false |
| `Entity::OccludesPathing` | `0xa6a0` | `32 c0 c3` | `xor al,al; ret` — **returns FALSE** |
| `Actor::OccludesPathing` | `0x22e90` | `b0 01 c3` | `mov al,1; ret` — returns true |

**The live chain, traced by caller scan:**

```
Level::CreatePathMesh          (Engine.dll — the ONLY caller of either NavMeshBuilder::Create)
  ├─ World::GetRegionsInBox → Region::LoadLevel/PostLoadLevel
  ├─ NavMeshBuilder::Create(const Level*)   @0xe8d80   ×2
  │     └─ GridRegion::GetCellMeshesInBox(ABBox, vector<const GraphicsMeshInstance*>&)
  │        then, per instance, a per-VERTEX transform loop and an index copy.
  │        ⚑ STATIC LEVEL GEOMETRY ENTERS AS TRIANGLES, NOT AS BOXES.
  ├─ World::GetEntitiesInBox → NavMeshBuilder::Create(const Entity*) @0xe9720
  │     └─ loop i: vtbl[+0x80](retbuf, i)  [an OBBox-returning getter] → NavMeshBuilder::AddBox
  │        ⚑ ENTITIES ENTER AS HITBOX OBBs — i.e. as chunk 8.
  ├─ NavMeshBuilder::CreateNavMesh → NavMesh::Set{Vertex,Index,Face}Data
  └─ NavManager::AddData(Region*) → NavManager::CreateNavigationData(...)
```

**⚑ D-5's structural conclusion survives in spirit but not in mechanism**, and the difference is
load-bearing: the AABB-is-enough shortcut that made D-5b look like a one-lap job **does not hold**,
because static level meshes are rasterised as real triangles.

### 3.1 `allowPathing` — what it actually means, decoded

The DBR key string lives at Game.dll VA `0x10540b7c` with **exactly one code reference**, inside
`Decoration::Load` (+0x18b), which stores the byte at `Decoration + 0x428`. That byte has **exactly
one reader in the whole module**:

```
?IsStatic@Decoration@GAME@@UBE_NXZ   RVA 0x1a53a0
    cmp  byte ptr [ecx + 0x428], 0x0
    sete al
    ret
```

**`allowPathing == 0` ⇔ `Decoration::IsStatic() == true`.** And there is **no
`Decoration::OccludesPathing` override**, so decorations inherit the base `Entity::OccludesPathing`
— which returns **false**.

> **⚑ So `allowPathing = False` is not "blocks pathing". It is "bake me into static level
> geometry".** The blocking is real but indirect: static decorations are what
> `GridRegion::GetCellMeshesInBox` hands the nav builder. D-5's 341-placement population is the
> right population; its *label* was wrong, and the wrong label is what made an OBB shortcut look
> licensed.

### 3.2 `NavManager::SetDefaultConfig` — 13 navigation parameters, read from the immediates

`?SetDefaultConfig@NavManager@GAME@@AAEXXZ`, RVA `0x126d70`, thirteen `mov dword ptr [ecx+off], imm`:

| offset | u32 | f32 | grade |
|---|---:|---:|---|
| `+0x0c` | **32** | — | integer (tile size) |
| `+0x10` | | **0.25** | **the nav cell size** — used as this lap's raster pitch |
| `+0x14` | | **0.2** | cell height |
| `+0x18` | | **2.0** | **agent height** — cross-checked against the 2.556 m player mesh (§ 2.2) |
| `+0x1c` | | **0.8** | agent radius |
| `+0x20` | | **0.5** | agent max climb |
| `+0x24` | | 16.0 | ORDER-AMBIGUOUS |
| `+0x28` | | 1.5 | ORDER-AMBIGUOUS |
| `+0x2c` | | 20.0 | ORDER-AMBIGUOUS |
| `+0x30` | | 50.0 | ORDER-AMBIGUOUS |
| `+0x34` | **6** | — | integer |
| `+0x38` | | 6.0 | — |
| `+0x3c` | | 1.0 | — |

**Grading, out loud.** The *values* are decoded — they are immediate operands in shipped code. The
*names* for the first six are asserted on structural position, and I checked the obvious way to be
wrong: **Recast/Detour is NOT in this binary** (zero occurrences of `dtNavMesh`, `Recast`,
`rcAlloc`, `dtCrowd`, `DT_`, `rcConfig`; the `CROWD` namespace is Crate's own —
`crowdmanager.cpp` / `crowdpath.cpp` / `crowdthread.cpp`). So I did **not** import Recast's field
order as truth. The six named fields are named because 0.25/0.2/2.0/0.8/0.5 in that order, plus a
`tileSize` integer of 32, is a coherent agent description and because 2.0 is independently
corroborated by the character-mesh height. **The middle four are left unnamed rather than guessed.**

These six numbers are **baton-critical regardless of how facet (h) is ruled**: a Godot rebuild needs
an agent radius and height, and these are the shipped game's, not an estimate.

### 3.3 The placement transform convention — read, not assumed

Inside `NavMeshBuilder::Create(const Level*)` @ `0x100e94b0` the per-vertex transform reads the
instance matrix at float indices **0,3,6 → out.x**, **1,4,7 → out.y**, **2,5,8 → out.z**. That is
the **row-vector convention: `world = local @ M`, M row-major** — which is exactly the 9 floats at
`.lvl` placement offset +0. Two supporting facts, measured: all 341 blocking placement matrices have
**row norms in [0.999997, 1.000000]** and **determinants in [0.999994, 1.000000]** — pure rotations,
**unit scale, no hidden scale factor**. (And because the observed rotations leave the y axis alone,
the `M` vs `Mᵀ` ambiguity mirrors each footprint about its own centre and **cannot change any area
or height result below** — recorded so the negative is not blamed on it.)

---

## 4 · The composition sweep — 24 cells, three rules, and what each one costs

Raster: 512 × 512 at the engine's own **0.25 m** cell, over A001's 128 × 128 m. Terrain height by
bilinear interpolation of the D-5 heightfield (mapping `world_x = col − 4.00`, `world_z = row +
0.00`, validated by D-5 to 3.92 mm and re-used unchanged). Terrain impassability from D-5's decoded
`Terrain::SlopeImpassable` (K = 0.25, T = 0.600000023841858, both re-read from `.rdata` this lap).
A column is blocked when a geometry sample falls in the walkable band `[terrain + lo, terrain + hi]`.

| rule | what it is | samples in region |
|---|---|---:|
| `triangles` | the 620,182 real mesh triangles, barycentrically sampled at ≤ 0.125 m — **the engine's own static-geometry source** | 28,987,859 |
| `hitboxOBB` | the 453 chunk-8 OBBs — the engine's **entity** primitive | 48,524,899 |
| `renderAABB` | the 27 chunk-10 AABBs — **the commission's original ask** | 96,497,757 |

| rule | lo | hi | geo blocked | reach m² | closed? | anchors |
|---|---:|---:|---:|---:|---|---|
| triangles | 0.0 | 1.0 | 19.7 % | 2,063 | no | 14/18 |
| triangles | 0.0 | **2.0** | 28.9 % | 1,743 | no | 14/18 |
| triangles | 0.0 | 3.0 | 37.1 % | **39** | yes | **0/18** |
| triangles | **0.5** | 1.0 | 15.6 % | 7,086 | no | 14/18 |
| triangles | **0.5** | **2.0** | 26.1 % | 5,688 | no | 14/18 |
| triangles | 0.5 | 3.0 | 34.8 % | 40 | yes | 0/18 |
| triangles | 1.0 | 2.0 | 22.5 % | 6,485 | no | 14/18 |
| triangles | 1.0 | 3.0 | 32.1 % | 41 | yes | 0/18 |
| hitboxOBB | any of 8 | | 42.5–48.9 % | **0** | — | **0/18** |
| renderAABB | any of 8 | | 55.4–64.5 % | **0** | — | **0/18** |

**Read the last two rows carefully: reach = 0 means the arena-centroid cell is ITSELF blocked.**
Both box rules bury the sim's own frame origin. The commission's fallback — per-mesh AABB — is the
worst of the three by a wide margin, and the hitbox OBB, though the engine's genuine entity
primitive, is barely better. **Only the triangle rule leaves the centroid standing, and it still
fails.**

The three `hi = 3.0` cells are the only "closed" cells in the sweep, and they close by **collapsing
to a 40 m² pocket containing none of the 18 anchors** — the degenerate closure, not a boundary.

> **⚑ NO CELL IS BOTH CLOSED AND ANCHOR-COMPLETE.** The best cell on anchors is `triangles | 0.0 |
> 2.0` at 14/18, not closed.

### 4.1 Terrain alone, extended well past D-5's sweep — still open, 17 thresholds out of 17

D-5 swept one terrain rule over 0.30–2.00 m and found the flood always reaches the region edge. I
added two more rules that a nav build would plausibly use, and pushed the first one below D-5's
floor:

| rule | thresholds tried | closed at any? |
|---|---|---|
| `SlopeImpassable` corner deviation (m) | 0.15 · 0.30 · **0.600 (decoded)** · 1.20 · 2.00 | **no, 0/5** |
| surface slope (deg) | 8 · 10 · 12 · 16 · 20 · 30 · 45 | **no, 0/7** |
| max step per cell (m) | 0.2 · 0.3 · 0.5 · 0.8 · 1.5 | **no, 0/5** |

At slope 8° the region is 69.6 % impassable and the arena centroid is itself blocked (reach 0).
**There is no terrain threshold at which the arena closes and remains usable.** D-5's negative is
confirmed and widened by a factor of three in rule-space.

---

## 5 · The falsification, stated precisely

At the most engine-faithful cell — `triangles`, band `[terrain + 0.5, terrain + 2.0]`, i.e. the
decoded climb and the decoded agent height — the free space fragments into **770 components**, the
largest being **5,688 m²**, and the 18 shipped anchors resolve as:

| anchor | sim (x, y) | status |
|---|---|---|
| `emitter:tier16spawnpoint01` | (−34.45, +9.59) | **INSIDE BLOCKING GEOMETRY** |
| `emitter:spawnpoint05` | (−6.82, +2.18) | **INSIDE BLOCKING GEOMETRY** |
| `patrolpoint_attack_03` | (−14.86, −11.36) | **INSIDE BLOCKING GEOMETRY** |
| `emitter:spawnpoint02` | (+9.34, −31.46) | DISCONNECTED (a 4 m² island) |
| the other 14 | | reachable |

`tier16spawnpoint01` is **the** emitter for the wave band this whole run exists to model. A monster
emitter is a place the game spawns bodies. **It cannot be inside a wall.** Therefore the composition
over-blocks, and it over-blocks by a margin that no threshold in the sweep closes.

**Why, in one sentence, and it is the named path for any successor lap:** the engine does not decide
walkability by projecting geometry onto the ground plane — it accumulates triangles, quads and boxes
and hands them to `NavManager::CreateNavigationData`, which resolves *3-D span* questions a 2-D
projection cannot express (walking **on top of** a low rock, walking **under** an overhang, eroding
by agent radius, then culling small regions). I read `NavMeshBuilder::Create(const Level*)` to its
end and **there is no slope or normal filter in the accumulation loop** — every vertex and every
index of every static instance is appended verbatim. The filtering lives behind
`CreateNavigationData`. **Reimplementing it would be inventing a rule, which Law 3 forbids.**

---

## 6 · Clearance vs the occupancy hull — the commission's last question, answered as far as it can be

With no earned boundary, "distance from the derived boundary to the occupancy hull" is unanswerable
as posed, and I will not answer it with a boundary that fails its own test. What **is** measurable:

| quantity | sim x | sim y |
|---|---|---|
| occupancy hull (C-1 / drax A1b, 86.915 × 85.303 centred (−1.819, 0.244)) | [−45.28, +41.64] | [−42.41, +42.90] |
| **A001 region tile** | [−85.26, +42.74] | [−64.36, +63.64] |
| terrain-passable from the centroid, decoded T | [−85.14, +42.61] | [−64.24, +63.51] |

**Hull edge → region-tile edge: east +1.10 m · west +39.98 m · north +20.74 m · south +21.95 m.**
**1,452 of 1,600** hull-perimeter samples sit on terrain-passable ground.

> **⚑ The east number is the one to carry.** The recorded occupancy hull reaches to within **1.10 m
> of the eastern edge of the arena's own region tile** — and terrain-passable ground runs right up
> to that tile edge, so the sim's actors are walking to the limit of the only region that contains
> the arena. That is not "plenty of room beyond the recording"; on that side there is **essentially
> none**, and what stops the flood-fill there is a *file boundary*, not a wall. Whether the arena
> genuinely ends at that seam or continues into a neighbouring region is **not resolved by this
> lap** (the seven `.lvl` region origins are recorded in `d5b_findings.json`; their tiling does not
> read as a contiguous 128 m grid and I did not chase it). On the other three sides the hull has
> 20–40 m of terrain-passable ground beyond it, so the hull is **not** a proxy for the arena there
> either — it is, as C-1 said, a box drawn around some paths.

---

## 7 · Residuals opened or closed by this lap

| id | item | state |
|---|---|---|
| **D-5 R-5** | the seven 262,188 B `.map`-head blobs "presumed minimap textures" | **CONFIRMED, one look, then dropped.** `7 × 262,188 + 4,655 = 1,839,971` vs the A001 blob offset `1,839,979` (Δ 8 B). **`262,188 − 44 = 262,144`, which is simultaneously `512 × 512 × 1` and `256 × 256 × 4`** — and the 0.25 m nav cell decoded in § 3.2 makes 512 × 512 over 128 m *exactly* a per-region pathing bitmap, which is why this was worth opening at all. It isn't one: the payload reads as 4-byte pixel runs. **A 256 × 256 RGBA image.** |
| **new** | the `.lvl` property list between the entity section and the terrain block | **OPENED, not bounds.** Entity section ends `0x8643`, heightfield marker at `0xdede`, declared property-section size 22,659 B → **392 `[u32 key][u32 size][payload]` entries**, payload-size histogram `{12: 390, 5048: 1, 9795: 1}`. The 390 twelve-byte payloads decode as RGB float triples — a colour/lighting table. The two large entries were not opened. |
| **new** | the `.map` head's named-object table | **ENUMERATED, 12 objects**: `PatrolPoint_Attack` · `Patrol Points` · `SurvivalMode_Tomb` · `tagSurvivalArena_01` · `SurvivalMode_Deeps` · `tagSurvivalArena_02` · `BossMusic` · `Spawn Area` · `Spawn Area 02` · `Survival Mode 01` · `NoRiftgates` · `NoPVP`. Each carries a GUID and **two editor RGBA colours — no geometry payload.** ⚑ **`survivalworld_a.map` names TWO survival arenas**, which the run has been treating as one; not resolved here. |
| **new** | `NavManager::CreateNavigationData` | **THE named target for any successor lap.** `NavMeshBuilder::CreateNavMesh` (~0x1e0 B, and it only packages the accumulated soup into `NavMesh::Set{Vertex,Index,Face}Data`) plus whatever `CreateNavigationData` dispatches to. Until it is read, the walkability rule is not decoded and any boundary is invented. |
| **new** | region tiling | The seven region entries (offset, size, trailing grid/origin words) are recorded in `d5b_findings.json` under `residuals.regions`. They do **not** read as a contiguous 128 m tiling and were not reconciled. Matters only if the arena crosses the east seam (§ 6). |
| **D-5 R-1..R-4** | untouched | still open, still not load-bearing for this verdict |

---

## 8 · What this lap did NOT do

- Did **not** publish a boundary, a polygon, a radial profile, a rectangle or a hull. The two files
  from a superseded first pass that contained a polygon were **deleted, not shipped**.
- Did **not** reimplement the engine's navmesh builder, and did **not** import Recast's parameter
  semantics as truth after confirming Recast is not in the binary.
- Did **not** name the four ORDER-AMBIGUOUS nav-config fields.
- Did **not** open MSH chunks 0, 2, 3 (present on some meshes), the chunk-5 44-byte per-submesh
  tail, or the vertex streams past position.
- Did **not** resolve which of the two named survival arenas A001 hosts, nor the region tiling.
- Did **not** touch the sim, the checkpoint, the baton, or any engine file. The only read outside
  the two vendor trees was D-5's own `A001_dbr_pathing.json`.

---

*KC2-MC Wave 1 · piece D-5b · legolas · 2026-08-24. Commit prefix `legolas(KC2-MC D-5b):`. Committed, not pushed.*
