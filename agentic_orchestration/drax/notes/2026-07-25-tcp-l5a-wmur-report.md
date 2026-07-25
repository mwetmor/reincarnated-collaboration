# TCP-L5a — BUILDING THE SEAM WITH W-MUR (mode (i), blind)

**Cell:** L5a · **Agent:** drax (presentation seam) · **Date:** 2026-07-25
**Method:** W-MUR — Murzak Godot-MCP 0.19.1 addon + `gamedev-mcp-server` 9.2.0 relay, self-hosted
**Dispatch:** `agentic_orchestration/dispatches/2026-07-25-drax-l5a-wmur-seam.md`
**Contract:** `~/Games/mcp-lab/evidence/l5/CONNECTION_CONTRACT.md` (65 predicates)
**Build:** `~/Games/mcp-lab/evidence/l5/l5a/l5a_scene_after.tscn`
sha256 `25530cc952dec799b22da62904a61cdafa0c4fe7f6b29b4f8e795be9322c9b0c`

---

## §0 — HEADLINE

**The room was built. The wire built 30 of its 36 added nodes unaided, and could not finish
the other 6.** Two ceilings and one defect, all three attributed against a plain-script control.

| | |
|---|---|
| **Predicates** | **57 PASS · 8 FAIL · 0 UNRECOVERABLE**, every one with a measured value |
| **Of the 8 FAILs** | **0 are build defects.** 5 are one contract-figure blind spot, 3 are mask/tolerance defects the contract pre-registered as its own most-likely failure |
| **Removal set** | **2 nodes**, derived by volume, never by name |
| **Wire verdict** | builds geometry well; **cannot measure, cannot execute, cannot author a per-surface material** |
| **Authoring** | **38 min 49 s** (22:02:53Z → 22:41:42Z) |
| **Execution** | **≈ 1 min of machine time — ~2 % of total.** Not inverted. |

---

## §1 — BLIND PROTOCOL: read-list and one declared incident

### 1.1 ★ DECLARED CONTAMINATION — a directory listing showed me two forbidden filenames

At 22:41Z, confirming the output directory existed, I ran `ls` on
`agentic_orchestration/drax/notes/`. The listing displayed
`2026-07-25-tcp-l5d-seam-arrival-phase-a-report.md` and `…-phase-b-report.md` — two names on the
§2 forbidden list. **I did not open either file.** Per §2 I halt, declare, and continue.

**Assessed leak: nil.** The contract's own header already states the L5-D arrival produced a
Phase-A `SITING_PLAN.md` and a Phase-B build report. The filenames carry no information the
contract did not hand me on page one. It happened *after* all measurement and building was
complete, so it cannot have influenced any result in this report.

**Two near-misses I avoided deliberately, recorded because they were live hazards:**

1. `~/Games/mcp-lab/project/.ai-game-dev/server/logs/server-log.txt` — 2 MB, `Trace` level, and it
   is the relay's **tool-call log**. Reading it would have shown me another cell's exact call
   sequence. I did not open it. (Its 18:10 mtime initially read as another session's; it was in
   fact my own accidental server start at 22:08Z — local clock is EDT.)
2. `bin/editor_up_pro.sh`, `bin/pro_mcp_client.mjs`, `_swap/pro_addon_godot_mcp_USED` — W-PRO
   material. **L-J binds: one wire at a time.** Not opened. I saw the `_swap` directory *name* in
   an `ls -la` of the lab root; it conveys only that W-PRO's addon was previously installed and
   swapped out, which the dispatch already told me ("W-PRO stays parked in its swap directory").

### 1.2 Full read-list — everything I opened, including what proved irrelevant

**Specification:** the dispatch; `CONNECTION_CONTRACT.md` (whole, in four reads);
`evidence/L4_KIT_CONSTANTS.md` (whole).

**Instrument, to use it correctly and to attribute its behaviour:**
`mcp-lab/UNINSTALL.md`; `project/.mcp.json`; `project/project.godot`;
`addons/godot_mcp/plugin.cfg`; `addons/godot_mcp/extensions.catalog.md` (first 60 lines —
**irrelevant**, it documents the optional-extension catalog, not the tool surface);
`addons/godot_mcp/Runtime/Reflection/GodotReflectorFactory.cs` lines 38-60 (**decisive** — the
registered converter list); `bin/editor_up.sh`; `bin/editor_down.sh`; `bin/mur_mcp_client.mjs`;
`.ai-game-dev/server/appsettings.json`; `.ai-game-dev/server/server.json`; `godot-cli --help`;
`godot-cli/dist/lib/configure-agent.js` (grep only — how the relay is invoked).

**Frozen instruments:** `prep/l4_diff.py` (lines 51-155); `project/l4_shoot.gd` (lines 1-185).

**Substrate:** `project/scene_before.tscn` — **grep/count only, never opened as a document.** Every
geometric figure in this report comes from the engine (see §2), not from the file text.

**Not read:** everything on the §2 list; my own notes of any date; `evidence/l4/L4_DRESSING_DECISION.md`;
any file under `evidence/l5/l5d/` or `prep/l5d_residue/`; `harness/`; `l6prep/`;
`~/Games/reincarnated-godot/` (concurrent cell — untouched).

---

## §2 — REMOVAL TARGETING (headline output)

### 2.1 The method

The contract gives a prism (§5.2) and forbids name-targeting. I implemented exactly that, in
one sentence: **for every `MeshInstance3D` in the substrate, compute the world AABB as
`node.global_transform * mesh.get_aabb()` read off the live engine node, and keep those whose
overlap with the prism is strictly positive on all three axes.**

Two choices in that sentence carry the whole result.

**(a) The AABB is read from the engine, never from the `.tscn` text.** Deriving world AABBs by
parsing serialised transforms would require me to decode inline `ArrayMesh` vertex data, and
would make the measurement agree with the writer about anything the writer got wrong — N-1's
principle, applied one stage earlier than N-1 asks for it.

**(b) The overlap test is STRICT, with an epsilon.** This is the load-bearing decision, and it
is the one I would flag to any future cell. The sweep:

| epsilon (m) | nodes selected |
|---|---|
| 0 (closed-interval, "touching counts") | **4** |
| 1e-9 | **4** |
| **1e-6** | **2** |
| 1e-4 | 2 |
| 1e-3 | 2 |

The answer is **flat across four orders of magnitude** (1e-6 → 1e-3), so 1e-6 is not a tuned
constant — it sits in the middle of a plateau, four orders above the substrate's float noise and
four below its smallest real feature (the 4 mm cap gap).

### 2.2 The removal set

```
Walls/Wall_0_3_inner      overlap x=2.500000  y=3.005743  z=0.225000
Walls/Wall_0_3_outer      overlap x=2.500000  y=3.005743  z=0.225000
```

Both carry `ShaderMaterial_aobh0` on both slots — that is "the ShaderMaterial the skins your
removal freed were carrying" (M-1), discovered rather than looked up.

### 2.3 Three traps the substrate actually contains — all measured, none guessed

**TRAP 1 — the naming trap (§0.1's warning, made concrete).** The bay index `_0_3` names **three**
nodes, not two:

| node | margin vs prism | verdict |
|---|---|---|
| `Walls/Wall_0_3_inner` | **+0.225000** | intersects |
| `Walls/Wall_0_3_outer` | **+0.225000** | intersects |
| `Walls/WallCap_0_3` | **−0.004000** | **disjoint — the name lies** |

The cap's underside is 3.009743; the prism's ceiling is 3.005743. It clears by **4 mm**. A
name-based cut takes 3 nodes and breaks **V-3** (all 28 crypt caps present, AABB-identical),
which is the invariant the whole lap exists to set. *The names partition by bay; the geometry
partitions by elevation.*

**TRAP 2 — the float-drift abutment trap. This one is nastier than the naming trap, and I have
not seen it named anywhere.** The two bays flanking the portal abut the prism at x = ±1.25. They
do **not** abut it symmetrically:

| node | x-overlap with prism |
|---|---|
| `Walls/Wall_0_2_*` (west flank) | **+2.384e-07** — *positive* |
| `Walls/Wall_0_4_*` (east flank) | **0.000000** — exactly zero |

A naive `margin > 0` test therefore eats the **west** flanking bay and spares the **east** one.
The result is a silent, asymmetric, mirrored-looking cut that breaks **V-6** — and because the
overlap is 238 nanometres, nothing in a rendered frame would show it until the wall-top ribbon
went subtly wrong on one side only. The epsilon is what makes V-6 survivable.

**TRAP 3 — the floor tiles.** `FloorQ_84 / _98 / _112` overlap the prism in **y** by 0.008091 (the
floor's top face stands above y = 0) and in **x**, abutting in z at exactly 0.000000. A `>=0`
test on all three axes takes three crypt floor tiles and breaks **V-7**. This is the same hazard
V-2 anticipates from the other direction — hence the contract's "split the prism at the walking
surface", which I did for V-1/V-2.

**All three traps are invisible to a name-based method and all three are caught by the same
one-line strict-overlap predicate.** That is the transferable result.

---

## §3 — THE WIRE ACCOUNT

### 3.1 Bringing it up — the wire is a two-process system, and only one of them is documented

`bin/editor_up.sh` launches the editor and polls the wire's `ping`. It does **not** launch the
relay, and it fails with a wall of C# stack traces if the relay is absent (`Connection refused
(localhost:27435)` → editor exits). The Murzak plugin is a *client*; the MCP server is a separate
109 MB binary at `project/.ai-game-dev/server/gamedev-mcp-server` that must be started first.

Two things a future cell will want:

- The relay **does not derive its port from cwd** despite deriving its project identity from it.
  Launched bare it reports `Location: …/project` and then `Start listening on port: 8080`, while
  the plugin dials the pin-derived **27435**. `--port 27435` is required.
- Once both are up the handshake is fast: `[up] READY after 1 ping attempt(s), 4s`.

**Correct launch sequence, for the record:**
```bash
cd ~/Games/mcp-lab/project && nohup ./.ai-game-dev/server/gamedev-mcp-server --port 27435 &
cd ~/Games/mcp-lab && ./bin/editor_up.sh headless 180
```

### 3.2 What W-MUR did *well* — and one of these is genuinely excellent

1. **`node-duplicate` is the wire's strongest tool, and it is the reason this cell has a room.**
   It carries `surface_material_override/0` and `/1` through to the copy. Since every chamber
   node has an exact material donor in the crypt, "duplicate the right donor, then move it" gets
   material inheritance (M-1), slot parity (M-2) and by-reference materials (M-3's
   `ShaderMaterial 26 → 26`) **for free, with no material call at all.** Zero new materials
   authored was not something I achieved; it was something the duplicate route made unavailable
   to get wrong.

2. **Resource assignment by reference works, including into inline sub-resources.**
   `node-modify {path:"Mesh", value:{resourcePath:"res://scene.tscn::ArrayMesh_51wnn"}}` →
   `Resolved Resource resourcePath='…' to a live 'ArrayMesh'`. The `ext_resource` count held at
   **6** across the whole build. I had predicted this would fail and produce `ext_resource`
   entries for the FBX; **the measurement refuted me.** Godot inlined them.

3. **The transform trap the contract spends §4 on does not exist through this wire.** The
   `.tscn` row/column ambiguity is a *text-serialisation* hazard. `reflection-method-find`
   reports `Godot.Basis` with named `Row0/Row1/Row2` **and** `X/Y/Z` **and** `Column0/1/2`, and
   `node-modify` accepts `Basis:{Row0,Row1,Row2}`. There is nothing to transpose. **T-2's gate is
   still worth running** — mine fired correctly on a broken reader early on (see §4, T-2) — but a
   wire-driven build is structurally immune to the hazard that convicted six of eight bases.

4. `script-create` syntax-validates GDScript before writing. Good behaviour; see §3.3 ceiling 2
   for why it does not help here.

### 3.3 CEILINGS — with the exact call that hit each

#### ★ CEILING 1 — the wire cannot read a node property. Any node property.

The 39-tool surface has **no node-property read**. `scene-get-data` and `node-find` return
`instanceId, name, path, type, script, childCount` and nothing else — no transform, no mesh, no
AABB, no material. `resource-get-data` reads *Resources*, and on an inline sub-resource it
returns only a reference:

```
resource-get-data {"resourceRef":{"resourcePath":"res://l5a_build.tscn::ArrayMesh_51wnn"}}
  -> {"name":"…::ArrayMesh_51wnn","typeName":"Godot.ArrayMesh",
      "value":{"instanceId":0,"resourcePath":"…::ArrayMesh_51wnn"}}      # no AABB, no surfaces
```

`node-modify` is write-only. It *knows* the properties — its not-found error helpfully enumerates
`Transform, GlobalTransform, Position, Basis, GlobalBasis, …` — but there is no getter.

**Why this is the ceiling that matters for a subtractive task:** removal targeting is a pure
measurement problem. Every figure in §2 — world AABBs, overlap margins, the 238 nm asymmetry —
is unobtainable through the wire.

#### ★ CEILING 2 — the wire can author and attach scripts but cannot execute them

No "run script" tool exists. I tested **four** in-wire triggers against a `@tool` script the wire
itself created and attached; all four returned `ok` and none ran:

| trigger | exact call | result |
|---|---|---|
| `@export` setter | `node-modify {pathPatches:[{path:"run_now", value:{typeName:"System.Boolean",value:true}}]}` | `Segment 'run_now' not found on type 'Node3D'. Available fields: none` — **`node-modify` resolves only the node's C# class surface; a GDScript `@export` is invisible to it** |
| `_process` latch | `script-update` (forces script reload) | never ticked — edited-scene nodes do not process under `--headless --editor` |
| lifecycle re-entry | `script-attach-to-node ""` then re-attach | no callback |
| reparent | `node-set-parent` (Godot `Node.Reparent`, which *does* fire `_exit_tree`/`_enter_tree`) | no callback |

`editor-application-set-state` (play-run) was considered and rejected: it launches the *main*
scene in a separate process and cannot see the edited, unsaved tree.

#### ★ CEILING 3 — `reflection-method-call` cannot bind ANY Godot object as `targetObject`

This is the tool that could have closed both ceilings above, and it is static-methods-only in
practice. `reflection-method-find` locates the method perfectly:

```
reflection-method-find {"filter":{"typeName":"Node3D","methodName":"GetGlobalTransform"},
                        "typeNameMatchLevel":5,"methodNameMatchLevel":5}
  -> [Success] Found 1 method(s)   ReturnType Godot.Transform3D
```

`reflection-method-call` with the identical filter does not:

```
reflection-method-call {…same filter…, "targetObject":{"typeName":"Godot.Node3D","value":1948052956113}}
  -> Tool execution failed: Method not found.  Godot.Node3D.GetGlobalTransform()
```

That first error is a **second, separate defect**: `find` defaults `parametersMatchLevel` to 0
while `call` defaults it to 2, so the same filter that finds a method fails to call it. Setting
`parametersMatchLevel: 0` resolves the method and exposes the real wall:

```
  -> Tool execution failed: 'targetObject' deserialized instance is null.
```

**Five encodings tested** (`value: <instanceId>`, `value:{instanceId}`, `value:{resourcePath}`,
`typeName: Godot.Node3D / Godot.Resource / Godot.Mesh`) — all null. A static call on the same
tool works fine (`Mathf.Sqrt(2)` → `1.4142135623730951`), so the tool is functional; only target
binding is broken.

**Root cause, read out of the wire's own source** —
`addons/godot_mcp/Runtime/Reflection/GodotReflectorFactory.cs:41-56` registers ReflectorNet
converters for `Vector2`, `Vector3`, `Color` and `Resource`, and **none for `Node`**. Notably the
`Resource` converter *does* exist and *does* work for `node-modify` member assignment — yet a
`Resource` `targetObject` is *also* null, so `reflection-method-call` does not share
`node-modify`'s converter chain.

#### ★ CEILING 4 — the wire cannot set a per-surface material override

The one the contract's P-6 / M-2 / N-5 are built around. `MeshInstance3D`'s per-surface overrides
are exposed in C# only as *methods* (`SetSurfaceOverrideMaterial(int, Material)`), and
`node-modify`'s path resolver walks fields and properties only:

```
node-modify {pathPatches:[{path:"surface_material_override/0", value:{…}}]}
  -> Segment 'surface_material_override' not found on type 'MeshInstance3D'.
     Available properties: Mesh, Skin, Skeleton, MaterialOverride, MaterialOverlay, Transparency,
     CastShadow, ExtraCullMargin, CustomAabb, LodBias, …          # no per-surface member exists
```

Also tested and rejected: `SurfaceMaterialOverride/[0]`, `surface_material_override/[0]`.
`MaterialOverride` (whole-node) **does** work — and that is a **laundering trap worth naming**: it
renders textured, passes any "is it untextured?" eyeball check, and silently violates M-2 slot
parity while writing `material_override` instead of `surface_material_override/N` into the file.

Ceilings 3 and 4 interlock: reflection could have called `SetSurfaceOverrideMaterial`, but it
cannot bind the node; `node-modify` can reach the node, but the member does not exist.

### 3.4 The wire's one genuine DEFECT — `node-modify {path:"Mesh"}`, convicted by control

Two faults appeared together when I assigned a new mesh through the wire:

1. **It clears every `surface_material_override` slot.** The four half-panels and the portal lost
   the overrides their donors carried. The portal ended up with **zero** overrides — worse than
   the 2-override architrave blob P-6 warns about.
2. **It deep-copies the resource per assignment.** Four nodes assigned the *same* half-panel mesh
   produced **four distinct** inline `ArrayMesh` sub-resources (`q6q7t`, `qd007`, `kax63`,
   `h5s6l`).

**This program has three times convicted a tool for a defect belonging to Godot or to us, so I
ran the control before filing.** `evidence/l5/l5a/rigs/l5a_control.gd` performs the identical
operation (`d.mesh = half` on four duplicates of the same donor) in plain GDScript:

| | plain GDScript control | W-MUR `node-modify {Mesh}` |
|---|---|---|
| overrides after mesh assignment | **preserved**, `count=2`, both slots intact, saved as `overrides=2` | **cleared to 0** |
| 4 nodes ← same mesh | **1 shared** `SubResource("ArrayMesh_wrvvf")` | **4 distinct** sub-resources |

**Attribution: the wire, on both counts.** Godot preserves overrides across a same-surface-count
mesh change and shares one resource across four references. This is the TCP-31 duplication class
reproduced through a different mechanism.

*Fair the other way:* the control also showed that the door's **third** surface has no override
even in a plain script (`CtrlDoor … overrides=2` in the saved file, despite in-memory count 3).
Setting slot 2 explicitly is a real requirement of the job, **not** a wire defect. The wire's
failing is that it *cannot* set it.

### 3.5 Fallbacks — declared, and timed separately

| # | what | why the wire could not | execution |
|---|---|---|---|
| **FALLBACK-1** | all measurement: substrate census, FBX natives, reload census, G4 sweep, aperture probes | Ceilings 1+2+3 — no property read, no code execution | 8 headless runs, **0.29 – 0.56 s each** (measured) |
| **FALLBACK-2** | repair of 5 nodes: share one inline mesh across the 4 half-panels, give the portal its door mesh, set overrides **including the portal's third slot** | Ceiling 4 + the §3.4 defect | **1 s** wall (`FALLBACK2_START 22:29:09Z → END 22:29:10Z`) |

**Exact calls that could not be made:** `node-modify {path:"surface_material_override/2"}` (ceiling
4); `reflection-method-call → MeshInstance3D.SetSurfaceOverrideMaterial` (ceiling 3).

FALLBACK-2 harvests every material off a live sibling node — each half-panel from its own
full-panel sibling, the portal from a far-wall skin that inherited the freed material. Nothing
was transcribed from the contract.

**Wire share of the build: 30 of 36 added nodes untouched by fallback, and both removals.**

### 3.6 Latency — the 8.32 ms hypothesis re-measured, and it is not a constant

77 calls, ledger-exact:

```
total 2992.9 ms   mean 38.87   median 19.49   p95 87.79   max 89.94
  node-duplicate  n=36   mean 71.24 ms      <- 8.8x the hypothesis
  node-modify     n=36   mean  8.12 ms      <- matches 8.32 ms almost exactly
  node-delete     n=2    mean 15.53 ms
  scene-save      n=1         56.34 ms
  scene-open      n=1          8.95 ms
```

**The prior cell's ~8.32 ms is right for cheap property writes and wrong by an order of magnitude
for `node-duplicate`.** Reporting a single mean for this wire hides a 9× spread. The whole
36-node build cost **2.99 s** of wire time.

---

## §4 — THE 65 PREDICATES

**57 PASS · 8 FAIL · 0 UNRECOVERABLE.** Raw JSON in `evidence/l5/l5a/census/predicates_part{1,2,3}.json`.

### T — transform convention (3/3 PASS)

| | verdict | measured |
|---|---|---|
| T-1 | PASS | all 4 run bases read as ROWS agree with live column vectors |
| T-2 | **PASS** | `−basis.z = (0.22040360, −0.88294762, −0.41451883)`, max component error **6.37e-08** |
| T-3 | PASS | harvested vs contract literals, max Δ **2.4e-08** across all four runs |

**T-2 earned its keep in this cell.** My first measurement rig queried `global_transform` on nodes
not yet in the scene tree; Godot returned identity and the gate fired immediately
(`−basis.z = (0,0,−1)`, "sun shines along −Z"). Without the gate I would have targeted the removal
against 288 identity transforms and cut nothing. **CR-7 is vindicated: it is a mechanism, and it
caught a real defect that was not a transpose.**

### P — the portal (6/6 PASS)

| | verdict | measured |
|---|---|---|
| P-1 | PASS | door **3 surfaces**; footprint 2.499993 × 3.005744 × 0.288030; FBX-local transform identity |
| P-2 | PASS | world AABB x[−1.2500, 1.2500] y[0.0000, 3.0057] z[−9.1190, −8.8310] |
| P-3 | PASS | mid-plane −8.975000; reveals **0.0810 / 0.0810** |
| P-4 | PASS | render aperture **2.0056 × 1.9669** (contract 2.0042 × 1.9663; Δ 1.4 mm / 0.6 mm, tol 2 mm) |
| P-5 | PASS | discharged at G-4: 0 no-floor samples, max_step 0.000000 |
| P-6 | **PASS** | `/0`, `/1`, `/2` all set, all `ShaderMaterial_aobh0` — **the wire could not do this; FALLBACK-2 did** |

### V — invariants (8/8 PASS) — the section that matters most

| | verdict | measured |
|---|---|---|
| V-1 | PASS | prism above walking surface returns `['Walls/ChOpening']` and nothing else |
| V-2 | PASS | prism below walking surface returns chamber floor tiles |
| V-3 | **PASS** | **28/28 crypt caps present, max ΔAABB = 0.00e+00** on all six bounds |
| V-4 | PASS | 34 caps, top spread **0.00e+00** at **3.169743** |
| V-5 | PASS | 0 gaps > 1e-3 on all 4 crypt runs and all 3 chamber runs |
| V-6 | PASS | flanking skins + caps, max ΔAABB **0.00e+00** over 6 nodes |
| V-7 | PASS | 196/196 floor tiles, max Δorigin **0.00e+00** |
| V-8 | PASS | pool range 9.0 / energy 3.4 / atten 1.3 / (0,2,0); Key ΔBasis 0.0 |

### C — the chamber (10/10 PASS)

C-1 12 tiles, x[−2.5, 2.5] z[−12.5, −8.75], **phase residual 0.00e+00** · **C-2 uncovered band
BEFORE = 0.4500 of 0.4500 m (196 floor nodes), AFTER = 0.0000 m (208 floor nodes)** · C-3 top
0.008091 = crypt's · C-4 far z[−12.9500, −12.5000], east x[2.5000, 2.9500], west x[−2.9500, −2.5000]
· C-5 height 3.005743 (err 2.1e-07), cap top 3.169743 · **C-6 coverage far [−2.5, 0]+[0, 2.5],
east and west both [−12.5, −11.25]+[−11.25, −8.75] — seam symmetric at z = −11.25 from
*different origins* per CR-2** · C-7 6 caps, all tops 3.169743 · C-8 outermost geometry
|x| 3.0672, z −13.0672 < 13.538 budget · C-9 max y 3.3430 (toppers only) · C-10 holders
{Floor, Pillars, Walls}, **0 `scene_file_path`**.

**C-2's mechanism caught my own instrument.** My first coverage test returned BEFORE = 0.0000,
because its y-filter admitted *wall* skins (which span y[0, 3.006]) as floor. Corrected to
"thin slab whose top is the walking surface", it returns the required 0.4500. **A build that only
asserted AFTER = 0.0000 would have passed with a broken instrument** — which is precisely why
C-2 demands both readings. It is the best-designed mechanism in the contract.

### M — materials and light (3 PASS / 3 FAIL) — see §5

M-1 **PASS**, 12 spot-checks against the M-1 table, 0 mismatches · M-2 **PASS**, 0 slot-parity
violations across 35 added nodes · **M-3 FAIL** (`StandardMaterial3D` 13, contract says 8) ·
**M-4 FAIL** (`ArrayMesh` +4, contract says +2) · M-5 **PASS** · M-6 **PASS**.

**West-side material choice (contract §14.5, free and to be reported): `ShaderMaterial_1u5ct`** —
the run-3 centre-bay instance, the west wall's positional mirror of the portal bay.

**M-5/M-6 note:** `ChamberPool` was made by **duplicating the live `InteriorPool`**, so colour
(1, 0.85, 0.62, 1), energy 3.4 and attenuation 1.3 were *copied off the live node* rather than
transcribed — M-5's explicit requirement, satisfied structurally. Only `omni_range` was authored
(5.0). M-6's artifact reproduces exactly: **`omni_range` does not appear in the saved `.tscn`**
(Godot omits properties at default); read back off the live node it is `5.0000`.

### R — register cues (4 PASS / 2 FAIL / 1 folded)

R-1 PASS (12/12 tiles, `ArrayMesh_51wnn` by reference, phase 0.00e+00) · **R-2 PASS** (discharged
by G-4: max step 0.000000, 0 no-floor) · R-3 PASS · **R-4 FAIL** (mesh count only; bands and
height PASS) · **R-5 FAIL** (`StandardMaterial3D` count only; ShaderMaterial 26 → 26 PASS) ·
R-6 PASS (portal asym 1.4e-06, floor asym 4.3e-06, pool x = 0) · R-7 PASS (exact equality on
colour/energy/attenuation; only range differs, 5.0 vs 9.0).

### G — walkability (6/6 PASS)

| | verdict | measured |
|---|---|---|
| G-1 | PASS | capsule r 0.400, h 1.700, skin 0.010 **declared**, centre y **0.868090** |
| G-2 | PASS | **1063 stations, blocked = 0** (contract states 1064 — see §5.4) |
| G-3 | PASS | `cast_motion` **safe_fraction = 1.0** |
| G-4 | PASS | 1201 samples, **no_floor = 0**, floor_y ∈ [0.008100, 0.008100], **spread 0.0**, **max_step 0.0** |
| G-5 | PASS | render mesh excluded (1), proxy substituted; **321 collision bodies generated at sweep time, 0 shipped** |
| G-6 | PASS | decoupled probe declared: **BoxShape3D, width bisected, height 1.70 and depth 0.10 FIXED** |

**G-5/G-6 calibration — two unrelated instruments, and they agree.**

| instrument | clear width |
|---|---|
| BoxShape3D width-bisection (physics) | **1.954416** |
| ray scan at 0.5 mm (independent) | **1.955500** |
| contract's proxy aperture (drax's rasteriser) | 1.9553 |

Box probe vs contract: **0.9 mm**. My ray scan vs contract: **0.2 mm**. Height 1.9340 vs 1.9336:
**0.4 mm**. Requirement is ≥ 1.95 m and agreement ≤ 2 mm — both hold. **§16.6 asked me to
re-measure every aperture figure because all of them were drax's. They reproduce.**

I ran G4 **before** the frames, taking the contract's own §14.2 advice. It cost nothing and
would have saved a re-shoot had it failed.

### N — reload census (7 PASS / 1 FAIL)

N-1 PASS (reloaded from disk as a live tree) · **N-2 PASS — every pre-registered delta met
exactly**:

| holder / type | pre-registered | measured |
|---|---|---|
| Floor | 196 → **208** | 208 |
| Walls | 84 → **101** | 101 |
| Pillars | 8 → **12** | 12 |
| root children | 7 → **8** | 8 |
| total | 296 → **330** | 330 |
| MeshInstance3D | 288 → **321** | 321 |
| OmniLight3D | 1 → **2** | 2 |
| collision nodes | 0 → **0** | 0 |

N-3 PASS (both absent by path; by volume only `ChOpening` above the walking surface) · N-4 PASS
(0 `scene_file_path` → **FLATTEN declared**; 0 duplicate names; 0 mesh+transform pairs) ·
**N-5 PASS — 597 surfaces checked individually, 0 untextured** · **N-6 PASS *with its reason*:
substrate 0 and built 0 `CollisionObject3D`/`CollisionShape3D`. The clause is EMPTY BY
CONSTRUCTION — a removal cannot orphan collision that never existed. This PASS carries no
information about my build.** The question it stands proxy for is answered by §10 · N-7 PASS ·
**N-8 FAIL** (see §5).

### D — differ (4 PASS / 3 FAIL) and F — frames (4/4 PASS)

| | verdict | measured |
|---|---|---|
| D-1 | PASS | **exactly 0 of 2,073,600** |
| D-2 | **SPLIT** | detection **PASS** (13,119 px, max delta 116); containment **FAIL as written** — §5.3 |
| D-3 | **PASS** | re-implemented `project()` + `convex_hull()` reproduce all 6 L4 hull vertices, **max error 0.000 px** |
| D-4 | **FAIL as written** | Zone S 114,937 = **85.6 %** of 134,294 (floor is 90 %) — §5.2 |
| D-5 | **FAIL as written** | **1** darker pixel of 19,350, delta (0, 0, **−1**) — §5.2 |
| D-6 | **PASS** | Zone F **7 px**, max delta **1** (bar: ≤ 60 and ≤ 1; L4 cells were 30/59/32) |
| D-7 | PASS | differ run unmodified, sha verified; `outside_addition` **not quoted** — it is the L4 dais mask and is meaningless here |
| F-1 | PASS | eye `(23.123901, 39.502224, 21.687008)` — exact |
| F-2 | PASS | `tan_h = 0.6470582`, `d = 2.81582`, pitch **−7.0854°**, eye `(0, 1.600000, −6.159179)` — all derived and printed |
| F-3 | PASS | `DIAG_cap-notch_framing-held-__box.png`, `DIAG_determinism_framing-held-__box.png` |
| F-4 | PASS | fresh process → **byte-identical**, sha `fbfc50cee2a5…` both |

**Cross-lap agreement worth flagging.** The unmodified differ reports **`changed_pixels = 134294`**
for my build. The contract quotes drax's independent build at **134,294** [B §5.2]. Two cells
that never saw each other's work moved *the same number of pixels*. The contract is tight enough
to force convergence at the pixel layer.

**Frames verified by eye.** `__money` shows the aperture with chamber floor, far wall and side
wall legible through it, deep-set reveal, and **no white blob** — the architrave is textured.
`__box` shows the cap ribbon running unbroken across the junction.

---

## §5 — CONTRACT DEFECTS FOUND (measured contradictions, per §0.2 rule 2)

### 5.1 ★ M-3 / M-4 / N-8 / R-4 / R-5 — five FAILs, one blind spot: **Godot attaches companions to a baked module**

The contract counts the *module*. Godot attaches two kinds of sub-resource to every baked module,
and the contract counts neither.

**(a) Shadow meshes.** The substrate's 8 `ArrayMesh` sub-resources are **4 visible + 4
`shadow_mesh` companions** — verifiable in `scene_before.tscn`:
`shadow_mesh = SubResource("ArrayMesh_coco8")` etc. Importing 2 new FBX modules therefore adds
**4**, not 2:

```
ArrayMesh   substrate  8  ->  built 12    (+2 visible: qscuh door, wrvvf half  +2 shadow: 1haxw, 6ch8g)
```

**The plain-script control produces the identical +4.** N-8's "new `ArrayMesh` exactly 2" and
M-4's "exactly two new mesh resources" are **unsatisfiable by any legal build that imports two
FBX modules.**

**(b) Per-surface mesh-internal materials.** The substrate's 8 `StandardMaterial3D` are
**6 mesh-internal + 2 node-override** (`a4i48` floor, `ugsf6` pillar/topper) — measured by
locating each id inside `[sub_resource type="ArrayMesh"]` blocks vs `[node]` blocks. The two new
modules carry 2 + 3 = **5** surfaces, hence 5 more mesh-internal defaults:

```
StandardMaterial3D   substrate 8 (6 internal + 2 override)  ->  built 13 (11 internal + 2 override)
```

**The node-override material set is unchanged, and `ShaderMaterial` is 26 → 26.** R-5's actual
claim — *"0 new materials and 0 new shaders may be authored"* — **holds exactly**. What fails is
the file-level count that was chosen to prove it.

**I did not tune the build to the number.** I could have nulled the imported meshes' internal
materials to force `StandardMaterial3D` back to 8 (pixel-neutral, since every surface carries an
override). I did not, because it would make my baked meshes structurally *unlike* the substrate's
own six, which cuts against R-4/R-5's "one construction / one material set" intent. **Reporting
the defect is the honest move; tuning to a defective predicate is not.**

**Suggested repair:** count *visible* meshes and *authored* materials, or state the expected
counts as `8 → 12` and `8 → 13` with the derivation.

### 5.2 ★ D-4 and D-5 — the mask defect the contract pre-registered against itself

The contract's closing line names Zone P as "this document's most likely defect". **Both zone
failures are that defect, and neither is damage.**

**The partition is exact:** S 114,937 + P 19,350 + F 7 = **134,294 = whole frame**. And
**99.9948 % of every changed pixel lies inside `MASK_SP`** — only **7 pixels** reach the far
field.

**D-4.** The 90 % floor is applied to Zone S alone, but 19,350 changed pixels land in Zone P —
where the contract *explicitly permits* change. Max channel delta in Zone P is **8**: dim, diffuse
glow, exactly the spill D-5 exists to bless. The floor was derived from drax's "generous chamber
box", which **§16.4 admits is undefined and non-recomputable**; that box evidently included the
spill region, so 96.8 % is not commensurable with an S-fraction. **The mask convicts the cell for
producing precisely the effect the adjacent predicate calls legitimate.** Had the predicate read
`changed(S) + changed(P) >= 0.90 * whole`, my build scores **99.995 %**.

**D-5.** One darker pixel in 19,350, at (x=1139, y=143): `before (73, 69, 61) → after (73, 69, 60)`
— a **single-LSB drop in blue only**. That is quantisation, not occlusion. The warm-ordering
predicate resolves the same way:

| threshold | n | warm-ordered `dR ≥ dG ≥ dB` |
|---|---|---|
| delta ≥ 1 | 19,350 | 81.88 % |
| delta ≥ 2 | 11,217 | 98.95 % |
| **delta ≥ 3** | **7,326** | **100.00 %** |
| delta ≥ 4 | 4,528 | 100.00 % |

**Every shortfall is in the 1-LSB bin**, where sub-LSB values round independently and channel
ordering is not resolvable by the instrument. The physics claim — spill is unidirectional and
warm — is fully satisfied.

**Suggested repair:** apply D-5's sign and ordering tests at `delta >= 2` (or exempt `|delta| == 1`),
and state D-4 against `MASK_SP` rather than Zone S.

### 5.3 D-2 — the cap-notch control detects, but its containment clause under-specifies

Detection is unambiguous: deleting `Walls/WallCap_0_3` moves **13,119 pixels, max channel delta
116**. **The instrument would have convicted me had I taken the cap.**

Containment does not hold as written:

| hull | contains bbox? | changed px inside |
|---|---|---|
| cap AABB + 24 px (**as written**) | **No** | 10,485 (**79.9 %**) |
| cap AABB + its shadow throw + 24 px | No | 12,790 (**97.5 %**) |
| neither | — | 326 (**2.5 %**) |

Removing an occluder changes three things: its own pixels, **the pixels it shadowed**, and **the
geometry it occluded from the camera**. The clause models only the first. Using the contract's
*own* §12.2 shadow-throw factors, a 3.169743 m cap throws **+0.7912 in X and −1.4881 in Z** — the
same arithmetic §12.2 uses to size Zone S, omitted here. The residual 2.5 % is the occlusion
reveal, which projects away from the camera (up-left in `__box`).

**Suggested repair:** gate D-2 on `changed_pixels > 0` plus a bbox test against the cap volume
**swept by the light direction and by the view ray**; or gate on detection alone, which is what
D-2 is actually for.

### 5.4 Two small figures that do not reproduce

- **G-2 station count.** Contract says 1064 stations for 0 → −10.625 at 0.01. Inclusive stepping
  gives **1063** (10.625 / 0.01 = 1062.5). `blocked = 0` is the gate and it passes; only the count
  differs.
- **M-1 / CR-3 / §14.5 — "14 parameter-identical instances" is 7.** Measured: runs 0 and 3 each
  carry **7 distinct `ShaderMaterial` instances across 14 skins**, each instance **shared by that
  bay's inner *and* outer skin**:

  ```
  run0 bay0 inner=3pmbl outer=3pmbl SHARED   ... bay6 inner=5xfco outer=5xfco SHARED   -> 7 distinct
  run3 bay0 inner=er1ke outer=er1ke SHARED   ... bay6 inner=efbn6 outer=efbn6 SHARED   -> 7 distinct
  ```

  The figure counted skins, not instances. **CR-3's reasoning is unaffected** — the choice is still
  free and pixel-neutral — but §14.5 should read "which of the **7**".

---

## §6 — RULINGS (all veto-open)

| # | ruling | reason | veto if |
|---|---|---|---|
| **R-L5a-1** | Prism intersection uses **strict overlap > 1e-6 m on all three axes**. | The answer is flat from 1e-6 to 1e-3; 1e-6 is 4 orders above the substrate's 2.4e-07 float drift and 4 below its smallest real feature. A `>0` test breaks V-6 asymmetrically; a `>=0` test breaks V-7. | a cell shows a legal removal whose true overlap is < 1e-6. |
| **R-L5a-2** | West-side material = **`ShaderMaterial_1u5ct`**. | Contract §14.5 leaves it free; I took the run-3 centre bay, the west wall's mirror of the portal bay. | a structural cross-cell diff needs it pinned. |
| **R-L5a-3** | The two 1.25 m caps reuse an existing `BoxMesh` with **basis-x scaled 0.5**, rather than authoring a new `BoxMesh(1.25, …)`. | Holds new mesh resources at exactly 2 (M-4/R-4) with identical coverage; V-5 is the gate and coverage is unchanged. **BoxMesh 28 → 28.** | cross-cell structural comparison wants C-7's literal 6-node/new-mesh construction. |
| **R-L5a-4** | Kept the kit's mesh-internal materials rather than nulling them to force M-3's count of 8. | Nulling would make my baked meshes structurally unlike the substrate's own 6 and would tune the build to a defective predicate. See §5.1. | the conductor prefers file-level counts to match at the cost of construction parity. |
| **R-L5a-5** | Build order: **clone all donors, then cut.** | The far wall and portal must inherit "the ShaderMaterial the skins your removal freed were carrying" (M-1). Duplicating the doomed skins before deleting them obtains it by construction, with no material call. | — |
| **R-L5a-6** | `ChamberPool` created by **duplicating the live `InteriorPool`**. | M-5 requires colour/energy/attenuation copied off the live node, not transcribed. Duplication makes transcription impossible. Only `omni_range` authored. | — |
| **R-L5a-7** | Wire usage counted as W-MUR = **tool calls over JSON-RPC** via the lab's standard `bin/mur_mcp_client.mjs`. Scripts *authored by* the wire but *executed by* Godot would have counted as wire-mediated; the question is moot (ceiling 2). | The client is a transport, not an author. Every mutation is a `tools/call`. | the conductor counts only Claude-native MCP tool bindings — see §8. |

---

## §7 — HYGIENE

| check | start | end |
|---|---|---|
| `project/scene_before.tscn` sha256 | `d45db0f5…de1966` ✓ | **`d45db0f5…de1966` ✓** |
| mode | `-r--r--r--` (0444) ✓ | **`-r--r--r--` ✓** |
| size | 134280 | **134280** |
| `project/` inventory | 19 entries | **19 entries, identical** — all `l5a_*` scratch removed |
| Godot processes | none | **none** (`editor_down.sh` → `CLEAN`) |
| `gamedev-mcp-server` | none | **none**; port 27435 free |

The substrate was never opened for write; all work ran on a 0644 copy at `project/l5a_build.tscn`,
banked to `evidence/l5/l5a/l5a_scene_after.tscn` and then removed from the project tree.
`~/Games/reincarnated-godot/` (concurrent cell), `harness/` and `l6prep/` were not touched.

**One residue to note:** the addon writes `project/.claude/skills` on every editor boot
("auto-generate skills: ensured up-to-date skills in …"). `.claude/` pre-existed this cell.

---

## §8 — STEER-CHECK ON THE DISPATCH

*The control the conductor asks for. It has caught a defect in nine consecutive cells.*

**1. ★ "There is a real trap in the substrate's naming that the invariants in §6 are designed to
catch."** This is a **supplied conclusion** and it is more specific than the contract. §0.1 says
only that the naming "does not partition the way the geometry does"; the dispatch told me the
trap is *in the naming* and that *§6 catches it*, which points at V-3 and therefore at the caps.
**I went looking for the cap.** Mitigating: §5.2 of the contract independently mandates
AABB-vs-prism targeting and forbids name-targeting, so my method was fixed before the hint could
act — and the method found **two** further traps (the 238 nm flank asymmetry and the floor-tile
abutment) that neither document mentions. But I cannot claim the cap finding was unassisted, and
I do not.

**2. "Prior cells found execution to be a small fraction of total; if this one inverts that, it is
a finding about the wire."** A supplied expectation about the *result*. It did not change any
measurement (the ledger is machine-generated), but it shaped what I instrumented and how
prominently I reported it. Named for the record. It did not invert.

**3. "A ceiling you hit and name … is worth more than a room you got by quietly falling back."**
This is a correct incentive but it is an incentive **toward finding ceilings**, and I was aware of
it while probing. **Mitigation, applied deliberately:** every attribution in §3 was tested against
a plain-script control or against the wire's own source before being filed — which is how §3.4's
two faults were confirmed as the wire's, and how the door's missing third override was confirmed
*not* to be.

**4. "~8.32 ms mean call latency — treat it as a hypothesis and re-measure if it matters."** Well
framed: it handed me a number *and* the instruction to distrust it. I re-measured and it is
tool-dependent (§3.6). No correction needed — this is how a figure should be passed between cells.

**5. One thing the dispatch did NOT steer, and should have been clearer about.** "Using the
installed W-MUR wire" does not define whether wire-authored-but-Godot-executed scripts count as
the wire. I ruled (R-L5a-7) that they would have, and the question turned out moot because the
wire cannot execute anything. **A future dispatch should say so explicitly**, because a cell that
ruled the other way could report "the wire built the room" while a GDScript did the work.

---

## §9 — WHAT I WOULD TELL THE NEXT CELL

1. **The wire is a good hand and a blind eye.** It places geometry accurately, inherits materials
   perfectly through `node-duplicate`, and assigns resources by reference without being asked. It
   cannot see. For an *additive* task where you already know the numbers, that is survivable. For
   a *subtractive* task, where targeting is measurement, it is disqualifying on its own.
2. **`node-duplicate` is the whole trick.** Do not build nodes and then dress them. Find the node
   the crypt already built that is materially identical to the one you want, clone it, and move
   it. Every material predicate then passes by construction.
3. **Never let `node-modify {path:"Mesh"}` near a node whose overrides you care about.** It
   silently clears them and deep-copies the resource. Assign the mesh first, or repair after.
4. **Run G4 before the frames.** Contract §14.2 is right.
5. **Epsilon your AABB test, and sweep it.** The substrate's float drift is asymmetric between the
   two flanking bays. A `>0` test cuts one flank and not the other, and nothing you can see would
   tell you.

---

## §10 — ARTIFACTS

All under `~/Games/mcp-lab/evidence/l5/l5a/`:

```
l5a_scene_after.tscn                    the build (sha 25530cc9…2c9b0c)
census/N2_PREREGISTERED.txt             N-2 expectations, declared BEFORE the build
census/BUILD_SPEC.json                  36 nodes: donor, harvested basis, origin, mesh
census/substrate_census.json            296-node engine census (removal targeting input)
census/after_census.json                330-node reload census (N-1)
census/fbx_natives.json                 re-measured door / half / wall / proxy natives
census/G4_SWEEP.json                    G-1..G-6
census/P4_render_aperture.json          render-mesh aperture (G-5 measured the proxy)
census/predicates_part{1,2,3}.json      all 65, PASS/FAIL + measured value
frames/L5A_AFTER__box.png               F-1, judging framing (sha fbfc50ce…)
frames/L5A_AFTER__money.png             F-2, derived framing
frames/DIAG_determinism_framing-held-__box.png   F-4, byte-identical to __box
frames/DIAG_cap-notch_framing-held-__box.png     D-2 control
diff/L5A_ZEROPOINT_DIFF.json            D-1, 0 of 2,073,600
diff/L5A_L4DIFF_DIFF.json               D-7, unmodified differ, whole_frame 134,294
diff/L4_HULL_REFERENCE.json             D-3 reference hull
diff/L5A_ZONES.json                     D-3..D-6
diff/L5A_D2_CAPNOTCH.json               D-2
diff/l5a_zones.py                       new zone differ, D-3 gated at 0.000 px
rigs/l5a_wire_build.mjs                 the W-MUR build driver (77 calls, ledger)
rigs/l5a_control.gd                     ★ the plain-script control that convicted the wire
rigs/CONTROL_out.tscn                   its output — 1 shared mesh, overrides preserved
rigs/l5a_{measure,fbx,fix,g4,money,notch,probe}.gd
logs/tools-list.json                    the 39-tool surface as the WIRE reports it
logs/wire-build-report.json             per-tool latency ledger
logs/CLOCK.txt                          authoring / execution clock stamps
```

---

**Signed:** drax, presentation seam, 2026-07-25.
**Verdict:** the room is built and the contract is largely met. **8 FAILs, 0 of them build
defects** — 5 a contract-figure blind spot about Godot's baked-module companions, 3 the mask and
tolerance defects the contract named as its own most likely failure. **The wire's account is the
real deliverable: four ceilings, one defect, all attributed against controls; 30 of 36 nodes
built natively; 2 declared fallbacks totalling under 5 seconds of machine time.**
