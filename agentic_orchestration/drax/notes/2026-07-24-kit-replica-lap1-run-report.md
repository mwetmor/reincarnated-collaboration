# KIT-REPLICA LAP-1 — run report

**Date:** 2026-07-24 · **Agent:** drax (presentation seam) · **Conductor:** gandalf
**Charter:** `agentic_orchestration/gandalf/notes/2026-07-24-kit-replica-lap1-run-charter.md`
**Interim note 1 (M1 ceiling + R1):** `2026-07-24-kit-replica-lap1-interim-r1.md`
**Status:** COMPLETE — 3 rooms shipped, 3 ceilings mapped, contact sheet produced.

---

## 0. The exit predicate — the pictures

**`~/Games/reincarnated-godot/harness_logs/kit_replica_2026-07-24/CONTACT_SHEET_box.png`**
— reference + R1 + R2 + R3, whole box, same camera, labelled. **This is the frame to judge.**

Also:
- `CONTACT_SHEET_cam.png` — the same four rooms at the bit-identical gameplay camera.
- `CONTACT_SHEET_matrix3x3.png` — the 3×3 room × occupant grid.
- `clip/` — G2 evidence (occupant driven to the interior clamp against S and E walls).
- `_dolly/` — the dolly ladder the box framing was eye-picked from.

---

## 1. Verdicts

| | R1 `polygon-dungeon-realms` | R2 `polygon-dwarven-dungeon` | R3 `polygon-ancient-egypt` |
|---|---|---|---|
| method assigned | M1 (MCP wire) | M2 (.tscn text) | M3 (generator) |
| method outcome | **M1 FAILED** → M3 fallback | **M2 PASSED** (after one silent, near-invisible defect) | **M3 PASSED** |
| **G1 geometry** | **PASS** — 17.5 m, 7 whole segments/side | **PASS** | **PASS** |
| **G2 clip** | **PASS** | **PASS** | **PASS** |
| **G3 occlusion** | **PASS (static)** — near-side ghosting present; no live approach run | **PASS (static)** | **PASS (static)** |
| **G4 collision** | **NOT TESTED** — see §6 | **NOT TESTED** | **NOT TESTED** |
| **G5 photographic identity** | **PASS with a declared substitution** (§4) | **PASS** | **PASS** |
| **G6 register** | deferred to galadriel (advisory) | " | " |

G1 was verified numerically at build (`floor 14×14 @ 1.25 m`, `wall scale`, `interior_half 8.30`
printed per build) and visually on the contact sheet. G2 was verified by driving the occupant to
the interior clamp and shooting the wall at box framing against black void — the definitive test.

---

## 2. Where each method stopped

### M1 — MCP wire (`satelliteoflove/godot-mcp` 4.1.0) — **FAILS EARLY, confirmed**

Predicted to fail because the room is runtime-built so the editor tree is empty. That is true and
was reconfirmed. It is **not the binding constraint**. The binding constraint is:

> **godot-mcp 4.1.0 has no node-creation primitive at all.**

`create_node` · `add_node` · `instantiate_scene` · `create_scene` · `add_child` · `delete_node` ·
`set_property` · `godot_gridmap_edit` · `gridmap_set_cell` — every one returns `UNKNOWN_COMMAND`,
probed over the wire. The whole node surface is `{get_node_properties, find_nodes, update_node,
reparent_node}`: property-set and re-parent on nodes that **already exist**. Nothing creates one.

Also absent: **measurement**. `get_resource_info` on an FBX returns `{resource_path,
resource_type: "PackedScene"}` — no AABB, no dims, no surfaces. And you cannot instantiate it to
measure it, because creation is absent. Since the run's core skill is *measure a new kit and
re-derive*, M1 cannot even reach the starting line.

What M1 *does* do well: introspection of **already-persisted** content —
`open_scene` + `get_scene_bounds` on `crypt_vault_node_baked.tscn` returned `node_count 724`,
`combined_aabb size (80,80,80)`. GridMap authoring exists (`set_gridmap_cell`,
`set_gridmap_cells_batch`) but is **gated**: it needs a pre-existing GridMap node *and* MeshLibrary,
and no command creates either. `exec_run` relays to the running game, not the editor, and persists
nothing.

**Setup friction (M1 cost, not R1 cost):** the installed addon was gutted — 3 `.gd` files against
36 in the package, `plugin.cfg` pointing at a non-existent `plugin.gd`. The official repair does
not repair it: `npx …--install-addon` reads the version from `plugin.cfg`, sees `4.1.0`, prints
*"Addon is already up to date"* and exits without an integrity check. **A gutted addon never
self-heals.** Restored from the npm tarball; re-applied the standing dead-`class_name` patch.

### M2 — direct `.tscn` text authoring — **PASSES, at authoring cost**, and the cost is *silence*

R2 shipped: 556 node blocks, 105 KB, ~280 instances, every `Transform3D` a baked literal.

The prediction ("passes, at authoring cost") is right, but understates *which* cost. The expensive
part was not writing 280 transforms — that is mechanical. It was that **a wrong one does not
announce itself.**

**The transpose trap.** A `.tscn` `Transform3D` literal's 9 basis floats are **row-major**; the
basis vectors you reason with (`basis.x/.y/.z`) are the **columns**. Emitting axes as consecutive
triples writes the **transpose**. For a rotation matrix the transpose is the **inverse**, so
nothing fails — every rotation is silently *mirrored*.

How well it hid:
- Godot loaded the scene with **zero errors and zero warnings**.
- A structural inspection pass reported **everything correct**: 288 `MeshInstance3D`, 2
  `DirectionalLight3D`, 1 `OmniLight3D` all visible at correct energies, correct node names,
  correct origins, correct `surface_material_override` on every instance.
- Symmetric cases (identity, 180°) are transpose-invariant, so the floor and half the walls
  looked *fine*, which actively argued against the hypothesis.

It was caught only by **measuring pixels**: a floor patch read `(12.9, 12.7, 14.5)` against the
control's `(115, 93.9, 76.8)` — 9× too dark. Diagnosis then took four discriminating experiments
(shadows off; M3 shadow-sensitivity; an sRGB hypothesis that was **falsified**; finally diffing a
light's basis against the value Godot computes for the same `rotation_degrees`). After the fix,
M2's floor patch is `(115, 93.9, 76.8)` — **identical to the M3 control**, whole-frame within 0.4.

**The M2 ceiling, stated precisely:** text authoring reproduces geometry exactly and is fully
capable — but it removes every feedback channel at once. No editor gizmo, no runtime derivation,
no parse error, and structural verification passes. The only instrument that catches a
transposed basis is a rendered frame compared against a control. **M2 without a rendered control
is not a safe authoring method**, regardless of how careful the arithmetic is.

### M3 — generator script — **PASSES cheapest, and the margin is large**

R3 was measured, dressed, built and captured in **1 min 37 s** on the established pipeline.

---

## 3. The measurement skill — what the kits actually did

Instrument: `scripts/kit_measure.gd`, **calibrated before use** — run on the reference pack it
reproduces every constant in `walltop_level.gd` to six decimals (`WALL_H 3.005743`, `FLOOR_Q 1.25`,
`PILLAR_NATIVE_W 1.082276`, topper base `0.011793`).

### The charter's difficulty ranking was inverted by measurement

§4a ranked the packs by catalogue asset **counts** (dungeon-realms 81 walls = "easiest";
dwarven-dungeon 37 = "hardest"). Measured:

| | predicted | measured | why |
|---|---|---|---|
| R1 dungeon-realms | easiest | **by far the hardest** | own `SM_Env_Dwarf_*` grid; 5 m walls and 5 m floors; **nothing** matches the reference |
| R2 dwarven-dungeon | hardest | **easiest** | ships Synty's shared `Generic/Models/Base` kit — wall measures `2.499991 × 3.005743 × 0.225`, **byte-identical to the reference** |
| R3 ancient-egypt | range-finder | easy geometry, alien register | also ships the shared base kit, byte-identical |

**Count ≠ compatibility.** Two of three packs ship the same modular kit; a kit swap between them
is nearly free (all scales `1.0`) and the register change comes entirely from textures. The one
pack with its own grid needed every constant re-derived. That is the roadmap-relevant finding.

### R1's genuine wall-run ceiling — found, then cleared without touching room geometry

- `SM_Env_Dwarf_Wall_01` = **5.000000 m** → 17.5 / 5.0 = **3.5 segments**, a broken half-segment —
  exactly the failure class `walltop_level.gd`'s *"WHY 14 and NOT 13"* comment documents.
- `SM_Env_Dwarf_Floor_01..06` = **5.0 m** → 3.5 tiles. Same.

Per charter §3 the room was **not** re-scaled. Searched the pack instead and found
`SM_Env_Dwarf_Wall_Half_02` = **2.500001 m** → **7 whole segments**, and
`SM_Env_Dwarf_Floor_Half_01` = **2.5 m** → 7×7 = 17.5 m exactly. Ceiling cleared, no HALT needed.

**Declared replica cost:** the DR wall is natively 5 m tall, so meeting `WALL_H` squashes it
**0.601 in Y** — the dwarven brick course reads ~40% squatter than the pack authored it.

### R2's *distinctive* vocabulary is unusable for this room — a real, separate ceiling

`polygon-dwarven-dungeon` ships only **4 wall meshes of its own**, all irregular cave rock
(`SM_Env_Cave_Wall_01` = 4.287868 × 4.586979 × 1.428782, off-centre origin; `_02` = 4.221344 ×
4.433870). None tiles a 2.5 m bay; there is no corner piece; they are meant to line cave corridors,
not close a rectangular room. **A modular room cannot be dressed from this pack's own content** —
R2 is only buildable because the pack also carries the shared generic kit.

### Three defects only a rendered frame could surface (all generalised into the builder)

1. **Origin convention, not just size.** The reference wall is symmetric in thickness
   (z ∈ [−0.1125, +0.1125]); the DR wall is **not** (z ∈ [−0.142392, +0.421605], origin 0.1396 off
   centre). Placed with reference math both leaves sat **5.6 cm proud** — a gap at the inner face
   and the outer leaf's top edge protruding past the void cap. Fixed by cancelling the module's own
   thickness-axis offset **in its local frame** (local +Z faces outward on N/S but inward on E/W,
   so the correction cannot be applied along `outward`).
2. **The void cap does not survive a naive kit swap.** It samples via **world-space UV tiling**,
   correct only because the reference pack ships a *separate tiling* stone texture
   (`Brick_Small_01.png`). dungeon-realms ships **none** — atlas only — and world-UV tiling across
   a 4096² atlas walks over its palette-swatch strip, painting a rainbow chunk on the cap once per
   world period. Fixed with a per-kit `cap_tex`: kits with tiling stone keep the reference material
   verbatim; atlas-only kits fall back to a solid texture at the reference brick's **measured** mean
   `(0.4076, 0.4137, 0.4218)`, so the band lands at the same value under the same `stone_tint`.
3. **`aura_tint` was a silent no-op for every pilot.** `pilot_rig._tint_aura()` sets
   `set_instance_shader_parameter("tint", …)`; the ruled Binbun variants expose **no `tint`
   uniform** — `aura_clip.gdshader` exposes `primary_color` / `secondary_color` / `tertiary_color`.
   Proven by rendering `--aura=#FF0000` and getting an unchanged white aura. Applied host-side to
   the uniforms that exist. **The rig seam was not modified** — flagged for the KT-2/KT-3 owner.

---

## 4. Two charter defects found in execution — reported, not silently resolved

**I7 is not satisfiable as written.** The reference frame Matt has been judging
(`harness_logs/walltop_void_test_v8_2026-06-21/walltop_00_player_cam.png`) was shot when
`FLOOR_TILES` was 6 — a **7.5 m** room. Matt grew the room to 17.5 m on 2026-07-07. At 17.5 m the
bit-identical `CAM_DIST 16.5` telephoto frames **floor only** — no wall enters the shot (verified;
see `CONTACT_SHEET_cam.png`, which is genuinely wall-free). A frame with no wall cannot be judged
for a wall swap.

**Substitution, applied identically to all four rooms:** each ships `__cam` (literal I7) *and*
`__box` (same pitch/yaw/FOV/aim derivation, dollied to 50 m, reproducing the v8 composition). The
naive room-growth ratio (16.5 × 17.5/7.5 = 38.5) still crops the corner columns; 50 m was eye-picked
from a dolly ladder. Only the dolly distance differs, and identically per room, so cross-room
comparison — the sheet's entire purpose — is exact.

**I4 conflates two numbers.** `interior_half = 8.30` is the occupant **movement clamp**. The
reference clips `king_clip`/`aura_clip` at the wall **inner face**, `floor_edge * 0.5 = 8.75` (what
`playshell.gd` actually passes). Implemented the reference behaviour, and exercised the box by
driving the occupant to 8.30 for the G2 frames.

---

## 5. Aura re-pick (drax reasoning-boundary call, charter §7)

| Room | KT-2 hex | Re-pick | Reason |
|---|---|---|---|
| REF | `#9AA0A6` | *unchanged* | kept as a true control |
| **R1** | `#9AA0A6` | **`#5AB4E0`** | R1 is pale sandstone; the desaturated grey rendered white-on-white and stopped reading as an aura. Steel-cyan keeps the cyclone's wind/steel identity and separates from warm sand. |
| **R2** | `#FF6A1A` | **`#FF5A0F`** | already separates against cool stone; nudged hotter for the darker room |
| **R3** | `#FF7A24` | **`#FF3D1A`** | orange sits on Egypt's sand+gold palette and would merge; hotter and redder to separate while staying a flame |

**Note on R3's aura:** the purifier's ruled VFX is `beam_vfx_04` — a *beam*, not a ground disc. At
idle it lies across the floor (visible on the sheet). Thematically correct — Flames of Ignaffar is a
channelled flame beam — but in a static idle room shot it reads as a stripe on the ground. Flagged
for Matt; the VFX-scene choice is a KT-3 ruling (KTL-4), not mine to overturn.

**Known inconsistency in the 3×3 matrix (secondary deliverable):** aura tint there is keyed to the
**room**, not the pilot, so R1's purifier wears the cyclone's cyan. The primary contact sheet pairs
each room with its assigned occupant, where tint and build line up correctly.

---

## 6. What was NOT tested — stated plainly

- **G4 collision: NOT TESTED.** Every frame is a static capture built with `with_collision = false`
  (the reference PNG-harness path). No `CharacterBody3D` was driven into a wall. The occupant was
  *placed* at the interior clamp, which tests the clip box (G2), not the collider. A G4 verdict
  needs the play-shell, not this harness.
- **G3 occlusion: static only.** Near-side ghosting materials are wired and present, but no
  camera→player approach was run, so the *transition* is unverified.
- **G6 register:** galadriel's, advisory, not run here.
- **Animation:** out of scope per Matt (lap 2). Idle only.

---

## 7. Cost ledger (KRL-2 split)

| Phase | one-time pipeline cost | per-room method cost |
|---|---|---|
| **M1 attempt (R1)** | — | **4 min 11 s** — addon repair from tarball, patch, editor launch, WS client rebuild, ~15 wire probes |
| **Pipeline construction** | **~10 min** — `kit_measure` authored + calibrated · `kit_replica_level` authored · `shoot_kit_replica` authored · contact-sheet compositor · reference smoke · dolly ladder | — |
| **R1 — M3 fallback** | 3 fixes generalised (origin re-centring · `cap_tex` · aura colour) | **8 min 37 s** — mostly the 3 fixes, which R2/R3 inherit free |
| **R2 — M2** | — | **13 min 42 s** — measure 1 s · emitter authored · emit · **~7 min diagnosing one silent transpose** |
| **R3 — M3** | — | **1 min 37 s** — measure → dress → build → capture |
| G2 clip + 3×3 matrix + sheets | — | ~4 min |

**Total run: ~48 min** (20:45 → 21:33).

**The number that matters:** on an established pipeline, a full dressing swap costs **~1.5 min**
(R3). R1's 8m37s and R2's 13m42s are pipeline-construction and defect-diagnosis, not swap cost. A
re-render of any finished room is **~3 s** of Godot wall-clock. If the content roadmap needs N
dressed rooms from packs that share Synty's base kit, the marginal cost is minutes, not hours — and
the one pack with its own grid (R1) cost ~4× more, which is the honest planning multiplier.

---

## 8. Failure register — which surface bit

| Method | Surface | What happened |
|---|---|---|
| M1 | **authoring/creation** | No node-creation primitive exists. Upstream of all four charter surfaces. |
| M1 | **introspection** | Partial: solid on persisted scenes; returns nothing dimensional for an un-instantiated asset, which is exactly what a kit swap needs. |
| M1 | import | Clean — all four packs fully imported (674/1221/434/884 sidecars). |
| M1 | persistence / skeleton-material remap | Never reached. |
| M2 | **persistence** | The transpose trap: valid-but-wrong text, zero errors, structurally verifiable, silently mirrored. |
| M2 | skeleton-and-material remap | Clean — but only after `probe_fbx_tree.gd` was written to discover child node paths an editor would show in the scene dock. |
| M3 | **skeleton-and-material remap** | The void cap's world-UV tiling assumes a separate tiling texture; atlas-only packs break it. |
| M3 | import | Module **origin conventions** differ between packs — size alone is not enough. |

**Taxonomy finding for the conductor:** the four-surface taxonomy inherited from the bake-off
assumes a creation primitive exists and asks which surface fails downstream. For M1 the answer is
upstream of all four. Recommend adding **authoring/creation** as a fifth surface for lap 2.

---

## 9. Artefacts

Code (`~/Games/reincarnated-godot/`):
- `scripts/kit_measure.gd` + `scenes/kit_measure.tscn` — measurement probe (calibrated)
- `scripts/kit_replica_level.gd` — kit-parameterised room builder (M3)
- `scripts/emit_r2_tscn.py` — M2 text emitter (carries the transpose-trap note)
- `scripts/shoot_kit_replica.gd` + `scenes/shoot_kit_replica.tscn` — capture harness
- `scripts/kit_contact_sheet.py` — sheet/crop compositor
- `scripts/probe_fbx_tree.gd` + `scenes/probe_fbx_tree.tscn` — FBX child-path probe
- `scenes/kit_replica_r2_dwarven.tscn` — the M2 room (556 node blocks)

Captures: `~/Games/reincarnated-godot/harness_logs/kit_replica_2026-07-24/` (39 MB)

Commits (local, **not pushed** — Matt-gated): `2f07ee9`, `378ce69`, + this report's commit.
