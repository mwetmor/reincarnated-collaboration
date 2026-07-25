# TCP-L4c — the H CONTROL (headless GDScript builder): run report

**Cell:** L4c, the control · **Instrument:** H = plain GDScript under `godot --headless --script`
**Executor:** drax (presentation seam) · **Date:** 2026-07-25 · **Conductor:** gandalf (`RUN-CONDUCTOR`)
**Dispatch:** `agentic_orchestration/dispatches/2026-07-25-drax-l4c-h-control.md`
**Lap charter:** `…/gandalf/notes/2026-07-25-tcp-l4-expansion-bakeoff-charter.md`
**Verdict:** **PASS** — six clauses met, non-destruction proven two independent ways, P-C3
resolved decisively against the wires' prosecution. **Two of five pre-registered predictions
FALSIFIED, and both falsifications are the cell's most useful output.**

---

## §0 — The one-paragraph answer

**H built the dais in 5 build attempts and 13 minutes, and the wire did not lose by the margin
anyone predicted.** Execution is effectively free — 282 ms of script time to open a 296-node
scene, derive the wall it had never been told about, add 14 nodes and save. **Authoring is not
free, and authoring is the whole cost.** The decisive finding is P-C3: the save-duplication
hazard that L4b shipped **fires on H too, identically, with no MCP server anywhere in the
process** — 9 nodes in, 13 out, +1 duplicate per instanced FBX. Both wires are exonerated. The
route that avoids it is flattening, and it is written down in §6 so it transfers.

---

## §1 — DECLARED READ-LIST (dispatch §1 / exit item 9)

### Read

| # | Path | Extent |
|---|---|---|
| 1 | `agentic_orchestration/dispatches/2026-07-25-drax-l4c-h-control.md` | full |
| 2 | `…/gandalf/notes/2026-07-25-tcp-l4-expansion-bakeoff-charter.md` | full |
| 3 | `…/gandalf/notes/2026-07-24-tool-capability-program-charter.md` | full |
| 4 | `~/Games/mcp-lab/evidence/L4_KIT_CONSTANTS.md` | full |
| 5 | `~/Games/mcp-lab/project/scene_before.tscn` | structure via `grep`/`awk`: node headers, name histogram, `ext_resource` list, `sub_resource` type histogram, the `Pillars` / `Walls` / `WallCap` / `FloorQ` / `StandardMaterial3D` / `ShaderMaterial` blocks |
| 6 | `~/Games/mcp-lab/project/l4_shoot.gd` | full |
| 7 | `~/Games/mcp-lab/project/l4_detail_shoot.gd` | full |
| 8 | `~/Games/mcp-lab/prep/l4_diff.py` | lines 1–110 (header, CLI, camera + mask constants) |
| 9 | `~/Games/mcp-lab/prep/fingerprint_product_repo.sh` | header |
| 10 | `~/Games/reincarnated-godot/scripts/kit_replica_level.gd` | constants block, `_derive`, `_build_pillars`, `_build_topper`, `_load_inst`, `_apply_single_tex` |
| 11 | `~/Games/reincarnated-godot/scripts/walltop_occlude.gdshader` | UV-handling lines only (`grep`) |
| 12 | `~/Games/mcp-lab/project/project.godot`, `~/Games/mcp-lab/env.sh` | full |
| 13 | `evidence/l4/TCP20_FINGERPRINT_L4{A,B,C}_{BEFORE,AFTER}.txt` | **line 2 + file mtimes only**, for P-C5's bracket. These files carry blast-radius bookkeeping and no geometry. |
| 14 | Directory **listings** (names only, no contents) | `mcp-lab/`, `project/`, `project/scripts/`, `evidence/`, `evidence/l4/`, `evidence/frames/`, `prep/` |

### ★ NOT read — deliberately, and this is the control

- **The session-start step "read your own recent notes" was SKIPPED for this cell.** It is the
  step that would have handed me both answers. Stated here because the dispatch required it to
  be stated.
- `drax/notes/2026-07-25-tcp-l4a-wmur-run-report.md` — not opened.
- `drax/notes/2026-07-25-tcp-l4b-wpro-run-report.md` — not opened.
- `prep/l4a_residue/**`, `prep/l4b_residue/**` — not opened **and not listed**.
- `evidence/l4/l4a/**`, `evidence/l4/l4b/**` — not opened **and not listed**.
- `evidence/l4/l4b_TIMELINE.txt` — **outside §1's letter** (it sits at `evidence/l4/` root, not
  under `l4b/`) and deliberately not opened anyway. P-C5's bracket came from the TCP-20
  fingerprint timestamps instead, which is a stricter route to the same number.
- `~/Library/Application Support/Godot/app_userdata/tcp_l3_lab/l4a_p6_roundtrip.tscn` — an L4a
  artifact that §1 does not name and that lies outside every vacate path. **Not opened.** See
  charter defect 4.
- `evidence/l4/CALIBRATION.md` — not needed, not read.

### ⚠ CONTAMINATION, declared at banking time rather than at report time

Banked verbatim before any build work to
`~/Games/mcp-lab/evidence/l4/l4c/FIRST_INTENT_BANKED.md` (13:17:56 EDT), including this
declaration. **Two facts entered my intent from the MANDATED reading, not from a forbidden
file** — see charter defect 1. They are: the room's pillar sizing convention (handed twice, once
with W-PRO's solved triple), and the semantic node-naming idea. **P-C4 is measuring something
considerably weaker than it reads, and I am the one saying so.**

---

## §2 — THE SIX CLAUSES, each with the number that resolves it

Every figure below is printed by the builder or by an instrument, not transcribed.
Derivation is name-free: the far wall is found by scanning world AABBs, not by trusting a node
name, and is then **cross-checked against a second, independent derivation**.

**Derived from `scene_before.tscn` (not handed):**

```
floor          x[-8.750000, 8.749943]  z[-8.750000, 8.749947]  top_y = 0.008091  edge = 17.4999 m
far (-Z) wall  14 segments (7 inner + 7 outer), outer_z = -9.200000, thickness = 0.450000
               INNER FACE Z = -8.750000
CROSS-CHECK    |wall inner face - floor -Z edge| = 0.000000000 m   AGREE
room tile pitch 1.249996 m  ->  room floor texture density 0.8000 repeats/m
```

| # | Clause | Measurement | Verdict |
|---|---|---|---|
| **1** | Platform 6.0×4.0×0.6, centred X=0, back edge flush to far wall inner face | `BoxMesh size (6.00, 0.60, 4.00)`, pos `(0, 0.3, -6.75)`; occupies X`[-3.000, 3.000]` Z`[-8.750, -4.750]` Y`[0.000, 0.600]`. Back edge = **-8.750000** = the derived inner face, to 0 dp of float. | **PASS** |
| **2** | 2 flights × 4 steps, 0.15 rise × 0.40 run, 1.2 m wide, ascending −Z | Treads at y = 0.1500 / 0.3000 / 0.4500 / 0.6000. Runs `[-7.55,-7.15] [-7.95,-7.55] [-8.35,-7.95] [-8.75,-8.35]`. Width 1.20, flights at x = **±3.6000**. Total rise 0.60 = platform height exactly; top tread's back face flush at −8.750 with the platform and the wall. | **PASS** |
| **3** | 2 pillars from the pack, on the dais, inset 0.5 m from each edge | pos `(±2.5000, 0.6000, -5.2500)`; **inset_x = 0.50, inset_z = 0.50**; world foot **0.671010 m**, height **3.065857 m**; base_y 0.595796 — i.e. seated on the 0.600 dais top with the same 4.2 mm FBX-internal sink the room gives its own pillars. | **PASS** |
| **4** | 2 dressing props at the dais front edge, symmetric about X=0, **measured** texture presence | `SM_Prop_Brazier_04` ×2 (pinned by `L4_KIT_CONSTANTS` §6, no substitution) at `(±1.0000, 0.6000, -5.2500)`, size `0.686378 × 1.240413 × 0.686378`, base_y **0.600000** exactly (base-at-y=0 origin convention used as handed). Texture verified by the census resolving the **effective** material per surface to a real `Texture2D` resource: **0 untextured surfaces**. | **PASS** |
| **5** | **NON-DESTRUCTION** | Two independent instruments, §3 and §4. Structural: **296 pre-existing paths, 0 missing, 0 changed** across class / world transform / mesh content / surface-override count / material fingerprint. Pixel: **32 changed of 1,730,817 outside the mask, max channel delta 1.** | **PASS** |
| **6** | `__box` camera (TCP-12) | `l4_shoot.gd` **unmodified** (sha256 `d529750592…`), camera printed by the running rig: eye `(23.123901, 39.502224, 21.687008)`, fov 20, basis rows exactly the published constants. | **PASS** |

### ⚠ Clause 2's spec defect — NOTED, NOT ACTED ON

Clause 2 places both flights **entirely outside the platform footprint** (|x| 3.00…4.20 against
a platform ending at |x| 3.00) climbing **away** from the room and **arriving at the dais's back
corner**, hard against the far wall. Whoever uses it walks up into a corner and turns around.
Recorded by the builder itself at build time and visible in
`CLAUSE2_stairs_plusX.png`. **Built as written. A control that silently corrects the spec is not
a control.**

---

## §3 — THE RELOAD-FROM-DISK STRUCTURAL CENSUS (dispatch §3.1, mandatory)

`prep/l4c_residue/l4c_census.gd`. **It reloads both scenes through the engine and instantiates
them; it does not parse `.tscn` text** — whether Godot double-creates a node is an engine
behaviour and a text scan is the wrong instrument for it.

```
scene_before  reloaded: 296 nodes
scene_l4c_h   reloaded: 310 nodes
EXPECTED      296 + 14 = 310    ACTUAL 310    -> MATCH

CLASS HISTOGRAM        before   after   delta
  MeshInstance3D          288     301      +13
  Node3D                    4       5       +1
  DirectionalLight3D        2       2       +0
  OmniLight3D               1       1       +0
  WorldEnvironment          1       1       +0

CLAUSE 5   pre-existing paths 296 | missing 0 | renamed/reparented 0 | changed 0 | added 14
           VERDICT: PASS — additions only

CO-LOCATED DUPLICATE SCAN (the L4b failure class)
  scene_before   duplicate survivors: 0
  scene_l4c_h    duplicate survivors: 0

TEXTURE PRESENCE PER SURFACE (TCP-16)
  scene_before   untextured surfaces: 0
  scene_l4c_h    untextured surfaces: 0
```

### Did the census find anything a frame could not? — the honest answer

**On this cell it found a NEGATIVE, and the negative is the point.** There were no duplicates
and no untextured survivors, so the census convicted nothing. But *"there are zero co-located
duplicates"* is a proposition **no rendered frame can ever establish**, because the duplicate
hides behind its own original — which is exactly how L4b's four got through. A frame can only
ever fail to see them. **The census is the only instrument in the stack that can return that
negative, and a lap that ships without one is asserting the absence rather than measuring it.**

It also proves clause 5 at a resolution the pixel diff structurally cannot reach: **296 paths ×
5 properties = 1,480 assertions**, including nodes fully occluded at `__box` (every outer wall,
every far-side cap). A rename, a re-parent, or a silent material swap on an occluded node moves
**zero pixels** and would pass P-2 unnoticed. It does not pass the census.

### One positive finding, from file comparison rather than the census

Cycles 2 and 3 produced **geometrically identical** scenes whose `.tscn` files **differ by 56
lines**: Godot assigns a fresh random `unique_id` to every newly-created node on each `pack()`.
**A `.tscn` is not byte-reproducible across builds even when the geometry is bit-identical.** The
rendered frame *is* byte-reproducible (verified below). TCP-27 ① already phrases its
reproducibility predicate on the **re-render** rather than the file — that was the right call and
this is corroboration, not a defect.

---

## §4 — P-2, via `prep/l4_diff.py` UNMODIFIED (exit item 6)

`prep/l4_diff.py` sha256 `736ee06c2e4012f66cd5261d27b64faa93cb8ec87e9b651428acb23c57cb56ea`,
mtime 11:10 — **before this cell existed. Not touched.**

```
OUTSIDE THE ADDITION   changed 32 of 1,730,817 px   max channel delta 1
                       bbox [1441, 433, 1601, 626]  mean_abs_diff 5.39e-06
INSIDE  THE ADDITION   changed 103,679 of 342,783   max channel delta 187
```

**Every changed pixel outside the mask is at channel delta exactly 1** — LSB, no exceptions.
Independent check against the raw (undilated) hull: **143 raw-hull-outside pixels, all at delta
1, 143/143 within 80 px of the hull, max distance 66.8 px**, clustered on the +X / −Z side — the
shadow-throw direction the differ's own header declares as expected spill. **Zero changed pixels
anywhere else in the room.**

Against TCP-27 ②'s floor (~30 LSB px, not prep's calibration zero): **PASS.** For the record,
L4a measured 30 and L4b 59; **H is 32** — squarely inside the honest-addition band, and the
lowest but one.

---

## §5 — CYCLE COUNT (P-5 is this lap's headline metric, so it is reported two ways)

**BUILD ATTEMPTS: 5. LOOK-DRIVEN FIXES: 2. FRAMES INSPECTED: 3.**

| # | Started | Outcome | **How it was caught** |
|---|---|---|---|
| 1 | 13:25:08 | **CRASH.** `DERIVATION FAILED: wall_n=0` | The builder's own guard |
| 2 | 13:25:48 | Built. Two derivation *reports* wrong; the cross-check printed `DISAGREE` **and shipped anyway** | The builder's own cross-check |
| 3 | 13:26:47 | Built. All derivations correct. Geometry byte-identical to cycle 2 (only `unique_id` churn) | — |
| 4 | 13:31:28 | `uv1_scale` per piece | **The detail FRAME** (look 2) |
| 5 | 13:32:34 | World-triplanar. **FINAL** | **The detail FRAME** (look 3), accepted |

**Attribution of each fix, because an unattributed failure is the only real failure (L-G):**

1. **Cycle 1 — `get_global_transform()` returns IDENTITY out of tree.** Inside
   `SceneTree._initialize()` a freshly instantiated subtree is not inside the tree, so every
   world-transform read came back as a value **shaped exactly like the answer**. The floor
   derivation then "succeeded" against LOCAL AABBs and reported a **1.25 m room**. Only the
   second, independent wall derivation failed loudly. *This is L-K's exact signature wearing
   engine clothes — except Godot did print 13 errors, so it is not an L-K instance under
   TCP-21's two-clause test (the operation was also incorrectly invoked). Fix: never ask the
   tree for a world transform; compose it from the node chain.*
2. **Cycle 2 — "flat" is not "floor."** The room's 28 `WallCap` boxes are 2.5 × 0.16 × 0.45,
   also under 0.2 m tall, sitting at y ≈ 3.09 out to |x|,|z| = 9.2. Merging them reported an
   **18.4 m room with its floor top at y = 3.169743**. Caught by the cross-check, which then
   **printed `DISAGREE` and let the build proceed** — a verification that reports and does not
   gate is decoration. It is now a hard gate. *No geometry was ever affected: the contaminated
   value fed only a log line, which is why cycles 2 and 3 are geometrically identical.*
3. **Cycles 4/5 — texture density; see §7.** Both fixes came from looking at a picture.

**The transferable asymmetry, stated only about H because the other cells' detection modes are
behind the forbidden wall:** **3 of H's 5 attempts, and 2 of its 3 fixes, were caught by
assertions inside the authoring instrument before any frame existed, at 0.60–1.10 s per
attempt.** The instrument that authors is also the instrument that checks, in the same process,
for free. Whether that asymmetry holds against the wires is gandalf's comparison to make.

---

## §6 — P-C1 … P-C5, each resolved to a recorded fact

### P-C1 — "H completes in ONE cycle" → **FALSIFIED**

**5 build attempts, 3 of them fixes.** Both wires needed 3. H is not obviously fewer, and the
prediction was made with *high confidence*. Attribution is in §5, cycle by cycle. **The
prediction's error was assuming that a cell whose answer is fully specified in numbers has
nothing left to discover — but three of H's five attempts were spent discovering things about
the SUBSTRATE and the ENGINE (out-of-tree transforms, wallcaps masquerading as floor, BoxMesh
UV generation), none of which the spec could have contained.**

### P-C2 — "H passes P-2 trivially" → **CONFIRMED**

32 px at delta 1, plus 0 changed of 296 paths structurally. And the mechanism is worth naming
because it is the transferable part: **non-destruction here is a property of what the builder
does not call.** The builder holds a reference to a pre-existing node **only to read from it**;
there is no code path that writes a property, transform, name, parent or material on anything
that came out of `scene_before`. That is checkable by grep, which is a stronger guarantee than
any post-hoc diff.

### P-C3 — DECISIVE: "the duplication hazard fires on H too" → **CONFIRMED, and it exonerates both wires**

Route declared per dispatch §6: **the deliverable FLATTENS.** That means the hazard structurally
cannot touch it — which is a real answer to the spec and **not** an answer to P-C3. So the cell
ran the experiment it had declined: `l4c_dupprobe.gd` instances the same four FBX the dais needs
(2 pillars + 2 braziers), saves, reloads and counts. **No MCP server, no addon, plain GDScript
under `--headless`.**

```
FBX instance shape:  SM_Bld_Base_Pillar_01 (Node3D)
                       SM_Bld_Base_Pillar_01 (MeshInstance3D)

A  own-all, GEN_EDIT_STATE_DISABLED   nodes  9 -> 13 (+4)   textured surfaces 4 -> 4   LOSSY
B  own-all, GEN_EDIT_STATE_INSTANCE   nodes  9 -> 13 (+4)   textured surfaces 4 -> 4   LOSSY
C  own-root-only                      nodes  9 ->  9 (+0)   textured surfaces 4 -> 0   LOSSY
```

Every instanced FBX comes back carrying **two** identical `MeshInstance3D` children where it
went in with one. This **reproduces TCP-24's three-route result exactly, at addition scale,
with nothing on the wire.** No route gives both a correct node count and surviving materials.

**Consequences, stated plainly:**

- **The hazard is Godot's `PackedScene.pack()`. It is universal. W-PRO is exonerated for L4b's
  four duplicates and W-MUR is exonerated pre-emptively.** The `+4` signature is not a
  coincidence: four instanced FBX produce exactly four duplicates, which is the number L4b
  shipped from the same four pieces.
- **This is TCP-30's conviction bias firing a fourth time, and this time it was caught before
  the conviction was filed.**

**HOW H AVOIDS IT — the transferable part, and the single most portable thing this cell
produced:**

> Instantiate the FBX **in memory**, lift `MeshInstance3D.mesh` off it, compose the FBX-internal
> transform **on the right**, and emit **one plain `MeshInstance3D`**. Free the temporary. No
> sub-scene boundary reaches the save path, so `pack()` has nothing to double.
>
> ```gdscript
> out.transform = Transform3D(Basis().scaled(scale), placement) * internal
> ```
>
> The right-composition is not optional. The pillar FBX carries a **+0.004478 m Y** offset on its
> internal mesh node; instancing applies it for you and extraction does not. Composed, it
> reproduces the substrate's own seat exactly: `0.6 + 1.0168164 × 0.004478 = 0.6045533`.

**And the honest limit, per dispatch §6:** our production idiom sidesteps this entirely by
building at runtime and never saving a `.tscn`. This cell **does** save one, so it is measuring
the hazard rather than dodging the measurement — but every scene-authoring tool must face it and
the flatten route is what lets a `.tscn`-saving tool survive it.

### P-C4 — "H scores highest on ROOM-COHERENCE and lands `PILLAR_WORLD_FOOT` exactly" → **CONFIRMED on the number; the prediction is weaker than it reads**

```
room  Pillars/Pillar_0   scale (1.5639243, 1.0168164, 1.5639243)  foot 0.671011 m  h 3.065858 m
dais  Dais/Pillar_0      scale (1.5639243, 1.0168164, 1.5639243)  foot 0.671010 m  h 3.065857 m
|scale delta| = (0.000000000, 0.000000000, 0.000000000)     footprint ratio = 0.999999
NATIVE-SCALE COUNTERFACTUAL: shipping the FBX at scale 1 gives a 0.429056 m foot = 63.9% of the room's
```

Exact to nine decimals. **But `PILLAR_WORLD_FOOT` was handed to me twice** — dispatch §3.3 states
it, and the program charter's **TCP-28** states it *with W-PRO's solved scale triple and its full
derivation*. The prediction claims H "can import the constants directly rather than infer them,"
and that is true — but the cell was also simply told the answer. **P-C4 measures transcription
fidelity here, not derivation.** I did independently re-derive it from the natives
(`0.671011 / 0.429056`) and assert equality against the room's own node, which is the strongest
form available under the contamination; it is not the same as having derived it blind.
Declared at banking time. See charter defect 1.

### P-C5 — "wall-clock under one tenth of either wire" → **FALSIFIED**

Identical method for all three cells: the TCP-20 blast-radius bracket (BEFORE fingerprint →
AFTER fingerprint), read off file timestamps at `evidence/l4/` root. **No forbidden file was
opened to obtain these.**

| cell | bracket | duration | vs H |
|---|---|---|---|
| L4a (W-MUR) | 11:27:27 → 12:00:11 | **32 min 44 s** | 2.52× |
| L4b (W-PRO) | 12:13:17 → 12:36:15 | **22 min 58 s** | 1.77× |
| **L4c (H)** | 13:24:59 → 13:37:58 | **12 min 59 s** | — |

**H is 0.40× W-MUR and 0.57× W-PRO. The prediction was 0.10×. Falsified by a factor of four to
six.**

**Authoring time, which the dispatch correctly names as the number that matters**, and which the
bracket above *understates* because my builder was written before the first fingerprint:

```
13:14        first tool call (dispatch)
13:17:56     first intent BANKED, before any substrate read
13:24:45     builder written                    ->  ~11 min reading + authoring
13:25:08     cycle 1
13:32:34     cycle 5 (final)                    ->  ~8 min of build/look/fix
13:37:58     all instruments, frames, diff done ->  ~24 min total session
```

**Pure execution is where the thousandfold lives: 0.60 s per full run, of which 282.5 ms is the
script's own build-and-save** — opening a 296-node scene, deriving a wall it was never told
about, adding 14 nodes and writing a 310-node `.tscn`. **Execution is free. Authoring is the
entire cost, and it does not shrink because the answer was handed over in numbers.** That is
dispatch §0's warning, measured.

**Caveat, declared:** L4c's bracket also contains four instruments the other two cells did not
have to build — the reload census, the duplication probe, the coherence measurement and the
close-up rig, together roughly half the elapsed time. Netting them out puts H nearer 6–7 min,
which is still **0.20×–0.30×**, not 0.10×. **P-C5 falsifies either way.**

---

## §7 — ROOM-COHERENCE (TCP-28), SCORED PER MODULE

Measured by `l4c_coherence.gd`, comparing every added module against the room's **own** nearest
precedent read out of `scene_before` in the same process. Full log:
`evidence/l4/l4c/logs/coherence.txt`.

| module | module scaling | texture density | naming | verdict |
|---|---|---|---|---|
| `Dais/Platform` | primitive — no scale concept | **0.8000 rep/m on every face** vs room floor **0.8000** | `Platform` | **ADOPTED** |
| `Dais/Step_{L,R}_0..3` ×8 | primitive | **0.8000 rep/m on every face** | `Step_L_0` … `Step_R_3` | **ADOPTED** |
| `Dais/Pillar_0..1` ×2 | scale delta **(0, 0, 0)** to 9 dp; foot 0.671010 vs room 0.671011 | atlas, `uv1_scale` 1, **1.4903 rep/m** = the room's pillar exactly | `Pillar_0`, `Pillar_1` | **ADOPTED** |
| `Dais/Brazier_0..1` ×2 | native — **no room precedent exists**, `scene_before` carries zero props | atlas, `uv1_scale` 1, 1.4569 rep/m | `Brazier_0`, `Brazier_1` | **ADOPTED** (nothing to adopt on scale) |

**Materials.** 2 added, shared across all 13 added meshes — the room's own idiom (2 textured
materials across 288 meshes). Parameter-identical to the substrate's own:
`cull_mode = 2 (CULL_DISABLED)`, `roughness = 0.9000`, `metallic = 0.0000`, albedo loaded through
`load()` so the imported resource carries the sRGB flag (colour-space parity, per
`L4_KIT_CONSTANTS` §5).

**Naming.** The room's grammar, read off the substrate: a type-plural `Node3D` holder at root
(`Floor` / `Walls` / `Pillars`) with `<Type>_<index>` children — `FloorQ_0..195`,
`Wall_<side>_<seg>_<inner|outer>`, `WallCap_<side>_<n>`, `Pillar_0..3`, `Topper_0..3`. Adopted
verbatim: holder `Dais` at root, 13 semantically named children, **0 auto-generated or debris
names out of 14 added nodes.** Note the addition follows **the room's** grammar rather than a
flat `Dais_Pillar_L`-style scheme — `Dais/Pillar_0` is unambiguous because it is scoped by its
holder, exactly as `Pillars/Pillar_0` is.

### The texture-density call, and the two cycles it cost — this is the finding

**Cycle 3 shipped NO `uv1_scale`, on the literal reading**: the substrate carries **zero**
`uv1_scale` across 296 nodes and 34 materials, and its shaders sample stone through the module's
**authored** UV channel and explicitly never reproject (`walltop_occlude.gdshader` :27–:29,
:95–:96). Adopting that verbatim looked obviously right.

**The detail frame falsified it in one look.** A 6 × 4 m `BoxMesh` has **generated** UVs, not
authored ones — one texture set per face — so at `uv1_scale` 1 the dais top rendered as a **blank
grey slab at 0.167 repeats/m, two metres from a room floor running at 0.800.** The convention
TCP-28 names is **texture density**; *"`uv1_scale` is absent"* is a **consequence** of every room
module carrying authored UVs, **not the convention itself**. Adopting the flag and losing the
density is cargo-cult coherence.

**Cycle 4 over-corrected** with a per-piece `uv1_scale` and the frame falsified that too, for a
reason the arithmetic hid: a `BoxMesh` face maps U to one world axis and V to another, so **one
scalar pair cannot serve a 6.0 × 4.0 top and a 6.0 × 0.6 riser off the same material.** The top
landed at 0.800; the 0.6 m riser took V = 3.2 across 0.6 m and rendered as dense horizontal
banding. Cycle 4 fixed the large face by breaking the small one.

**Cycle 5 — world triplanar.** `uv1_scale` becomes repeats-per-world-metre and is therefore
independent of face dimensions: **every surface of every dais piece lands on exactly 0.8000
rep/m, the room's own floor density**, off **one** shared material. This does **not** contradict
the room's shader comment — that prohibition exists because the wall and pillar meshes are
**atlas**-mapped and reprojection would pick the wrong swatch out of a palette sheet.
`FloorTiles_Texture_01` is measured **genuine tiling** stone (`L4_KIT_CONSTANTS` §5). The
prohibition is about atlases; it does not reach a tiling texture on a primitive. The dais's atlas
material keeps `uv1_scale` 1 and no triplanar, exactly as the room does.

### Room conventions the addition did NOT adopt — declared, not hidden

1. **Toppers.** All 4 of the room's pillars carry a `Topper` cap; the dais's two do not. Clause 3
   says *"two pillars"*, and a topper is a **third module type the spec does not license.**
   Coherence loss recorded; **spec obeyed.** This is the same discipline as clause 2.
2. **Occlusion shaders.** The room's camera-side pillars and walls carry `walltop_occlude` /
   `walltop_void` `ShaderMaterial`s so near geometry fades. The dais uses plain
   `StandardMaterial3D`. Correct — the dais is interior geometry, not a camera-side occluder —
   but it **is** a divergence from the room's material mix and is named as one.
3. **`uv1_scale` as a flag.** Diverged in the flag; adopted in the density. See above.

**Inherited, not caused (TCP-27 ③):** the dais pillars read as rainbow atlas bands. Same mesh,
same UVs, same scale, same texture as the room's own — this is the substrate defect gandalf
propagated so no cell would burn a cycle on it. **Zero cycles burned.** The propagation worked.

---

## §8 — CHARTER DEFECTS

gandalf predicted his most likely defect was §1 failing to name a file that leaks the answer.
**The leak is not an unnamed file. It is the named ones.**

### DEFECT 1 — ★ §1's forbidden list does not cover the documents §1 orders you to read

The dispatch mandates the **program charter**. That charter's ruling ledger publishes:

- **TCP-28**: W-PRO's solved pillar scale `(1.56392, 1.01682, 1.56392)` **with its full
  derivation**; W-PRO's node-naming scheme verbatim (`Dais_Pillar_L`, `Dais_Step_L1`,
  `Dais_Brazier_R`); W-PRO's `uv1_scale (0.8,0.8,0.8)` and its material count; and the **prop
  identity** (brazier), which is clause 4's answer.
- **TCP-27 ①**: `mesh_platform.tres` is *"literally `size = Vector3(6, 0.6, 4)`"* — clause 1's
  arithmetic, quoted in the document explaining why that arithmetic must be hidden.
- **Dispatch §3.1**: L4b's expected node count (314) and its duplicate count (4).

**A large fraction of the answer is delivered by the two documents that forbid the answer.**
Some of this is deliberate (§3.3 re-publishes `PILLAR_WORLD_FOOT` as *"a measurement to reproduce
or diverge from"*); TCP-28's solved triple and naming scheme are not, and they arrive before the
blind control has formed an intent. **Fix for L5+: give blind cells a redacted charter, or move
per-cell results out of the ruling ledger into cell-scoped notes the ledger cites by reference.**

### DEFECT 2 — the four conformance close-ups are REQUIRED but UNDEFINED, and their only prior definition is behind the forbidden wall

Dispatch §5.2 requires *"the four conformance close-ups"* as though they were a defined artifact.
Neither charter defines their parameters. The only place L4a/L4b's parameters could exist is
`evidence/l4/l4a/**` and `l4b/**` — **§1-forbidden.** The requirement is **unsatisfiable as
written by a blind control.**

Resolved per **L-F**: four close-ups defined **here**, one per measurable clause, every parameter
declared on the command line and echoed by the rig (`l4c_closeup.gd`, a **new** file — the
standing rigs are HALT-listed or self-declared "reused verbatim" and were left byte-unmodified).
**They are not claimed to match L4a/L4b's crops.**

### DEFECT 3 — ★ the lap charter assigns the H dispatch a deliverable §1 forbids it to build

Lap charter §5.1: the **four-cell contact sheet** (`scene_before | W-MUR | W-PRO | H`, plus a
`|diff| ×4` strip per cell) is *"Assembled by the H dispatch"*. Assembling it **requires reading
`evidence/l4/l4a/**` and `evidence/l4/l4b/**`** — both §1-FORBIDDEN to this cell. The L4c
dispatch's own §5 exit predicate silently drops the item.

**NOT BUILT. The conflict is escalated rather than resolved by reading.** Every input for the H
column is banked at `evidence/l4/l4c/frames/` and `evidence/l4/l4c/diff/`. **Recommendation:
gandalf assembles the sheet from the three cells' banked frames, or a non-blind pass does, after
the blind period closes.** The two requirements cannot both be met by the party that is blind.

### DEFECT 4 — the vacate predicate does not cover `user://`

TCP-27 ① requires the cell to vacate the **project directory**. It does not reach Godot's
`user://`, and an L4a artifact is sitting there right now:
`~/Library/Application Support/Godot/app_userdata/tcp_l3_lab/l4a_p6_roundtrip.tscn`. It is
**outside `prep/l4a_residue/`, outside `evidence/l4/l4a/`, and therefore outside §1's forbidden
list** — a solved-scene-shaped file a blind cell could open without breaking any stated rule.
**I did not open it.** This is the same error class as TCP-20's two amendments: *a predicate that
does not cover the surface being written.* **Fix: extend the vacate predicate to `user://`, and
have `l4_shoot.gd`-class rigs write nowhere but the declared output path.**

---

## §9 — EXIT PREDICATE (dispatch §5)

| # | Item | Status |
|---|---|---|
| 1 | Six clauses measured, each with its resolving number | ✅ §2 |
| 2 | Frames at `__box` + detail crop + four conformance close-ups | ✅ §10 (close-ups per defect 2) |
| 3 | Reload census, expected vs actual, untextured survivors | ✅ §3 — 310/310, 0 duplicates, 0 untextured |
| 4 | P-C1..P-C5 each resolved to a recorded fact | ✅ §6 — 3 confirmed, **2 falsified** |
| 5 | ROOM-COHERENCE scored per module with measurements | ✅ §7 |
| 6 | P-2 via `l4_diff.py` **unmodified** | ✅ §4 — sha `736ee06c…`, mtime 11:10, untouched |
| 7 | TCP-27 ① vacate — bank, verify byte-identical re-render, move outputs | ✅ §10 |
| 8 | Blast radius | ✅ §10 |
| 9 | Declared read-list | ✅ §1 |

---

## §10 — ARTIFACTS, VACATE AND BLAST RADIUS

### Frames (L-A binds — every one judgeable by eye, unaided)

```
evidence/l4/l4c/frames/L4C_H__box.png              the standing __box judgment framing (TCP-12)
evidence/l4/l4c/frames/L4C_H_detail.png            the §5.2b detail crop, parameters verbatim from
                                                   l4_detail_shoot.gd (aim (0,1,-6) dist 18 pitch -32
                                                   yaw 47 fov 20) — unmodified, reused as declared
evidence/l4/l4c/frames/CLAUSE1_platform_backedge.png  aim (0, 0.60, -7.40) dist 13 pitch -30 yaw 47 fov 26
evidence/l4/l4c/frames/CLAUSE2_stairs_plusX.png       aim (3.6, 0.35, -7.90) dist 10 pitch -30 yaw 20 fov 16
evidence/l4/l4c/frames/CLAUSE3_pillar_inset.png       aim (2.5, 0.60, -5.40) dist 10 pitch -40 yaw 47 fov 22
evidence/l4/l4c/frames/CLAUSE4_props_symmetry.png     aim (0, 1.10, -5.25) dist  8 pitch -10 yaw  0 fov 24
evidence/l4/l4c/diff/L4C_H_DIFF.json / .png / DIFFx4.png / DIFFx4_MASKED.png
```

Each frame is one scene in one process — **TCP-23, enforced by the rigs, not trusted to the
operator.**

### TCP-27 ① vacate

Byte-identical re-render verified **before** moving anything: `L4C_H__box.png` re-shot in a fresh
process, both sha256 `7d85414fbb6bc677273f8186e1204367043485bb596c501120a258c3a6b12e7c` —
**BYTE-IDENTICAL.** Outputs then moved to `prep/l4c_residue/`:

```
prep/l4c_residue/scene_l4c_h.tscn      sha256 8c3d336d3e74bce49268d0090c19dad66c82591fb816102d05ebc0e68f72c212
prep/l4c_residue/l4c_build.gd          the builder
prep/l4c_residue/l4c_census.gd         the reload census
prep/l4c_residue/l4c_dupprobe.gd       the P-C3 probe  (+ its 3 output .tscn)
prep/l4c_residue/l4c_coherence.gd      the TCP-28 measurement
prep/l4c_residue/l4c_closeup.gd/.tscn  the close-up rig
```

**`project/` ends exactly as found** — `addons Assets icon.svg icon.svg.import l4_detail_shoot.gd(+uid)
l4_detail_shoot.tscn l4_shoot.gd(+uid) l4_shoot.tscn project.godot scene_before.tscn scripts
tcp_l3_lab.csproj`. No `l4c_*` file, no stray `.uid`, no stray `.import`.

### Blast radius

```
scene_before.tscn   sha256 d45db0f507f6b835e14447c9ceb7e7e6bd645e070bc1fe1241dd6e8522de1966   UNCHANGED
                    mode   -r--r--r-- (0444)                                                  PRESERVED
reincarnated-godot  2494-file dark-fortress manifest BEFORE vs AFTER: BYTE-IDENTICAL (TCP-20, not git status)
standing rigs       l4_shoot.gd d52975059230…  l4_detail_shoot.gd 1ee8572ff79a…  l4_diff.py 736ee06c2e40…
                    all mtimes 11:03–11:44, before this cell began at 13:17 — UNTOUCHED
editor_settings-4.6.tres  mtime 12:35:48, BEFORE this cell — the TCP-20-amended shared surface was not written
exit state          no Godot process, no gamedev-mcp-server process, no listening port
```

**One declared delta:** lab `app_userdata` files 15 → 16. Attributed: a single rotated Godot run
log, `logs/godot2026-07-25T13.37.24.log`, generated by my own runs. Benign, named rather than
buried.

### Bookkeeping gap, declared

Build cycles 1–3 were tee'd to full logs; **cycles 4 and 5 were run through a grep filter and
their full stdout was not tee'd.** The captured console output is banked as an explicitly
labelled excerpt at `evidence/l4/l4c/logs/build_cycle4_5_EXCERPT.txt`, and both cycles are
re-derivable by re-running `prep/l4c_residue/l4c_build.gd`.

---

## §11 — WHAT THIS CELL DOES AND DOES NOT LICENSE

Repeating dispatch §0 because the result invites exactly the misreading it warns about.

**It measured:** what the H route costs and produces on an expansion task **whose answer was
already specified in numbers**, and whether a universally-blamed save hazard belongs to the
tools. **It says nothing about design arrival.** H requires a human or agent who already knows
the geometry to write it down — that is mode (ii) and it is not this lap. **An H win here is
evidence about execution cost, not about authoring.**

And the sharpest single number in the cell argues *against* the easy reading: **execution was
0.60 s; the cell took 24 minutes.** Nearly all of H's cost is the part this lap held constant.

---

**Signed:** drax, presentation seam, 2026-07-25. Two predictions falsified, four charter defects
filed, one prosecution withdrawn on the tools' behalf, and the answer never read.
