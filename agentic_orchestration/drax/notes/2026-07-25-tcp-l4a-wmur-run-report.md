# TCP-L4a — W-MUR CELL (run report)

**Program:** Tool-Capability Program · lap **L4**, class **T2 EXPANSION** × mode **(i) held-constant spec**
**Charters:** `2026-07-24-tool-capability-program-charter.md` · `2026-07-25-tcp-l4-expansion-bakeoff-charter.md`
**Conductor:** gandalf (`RUN-CONDUCTOR`) · **Executor:** drax (presentation seam) · **Instrument:** W-MUR only
**Status:** **CLOSED — PASS.** All six spec clauses PASS. P-1..P-6 each resolved to a recorded fact.

---

## §0 — Verdict, in one paragraph

**W-MUR added the dais to a scene it did not author, hit all six spec clauses to five decimal
places, and damaged nothing — 30 changed pixels of 1,730,817 outside the addition, every one of
them at a channel delta of exactly 1, 29 of 30 within 20 px of the mask boundary.** It took
**three author→look→fix cycles** and **117 wire calls**, server-side **median 6.93 ms** (n=119).
**P-3 resolved AGAINST the program's central prediction: the route was node-by-node, not W→H** —
and the reason is a manifest fact, not a preference. Against that: **P-6's duplication hazard did
not fire, but its sibling did** — `node-create` owns only the instance root, so the four FBX props
saved with **their materials silently dropped**, every call returning `Success`. **A non-lossy path
exists and I found it** (`node-set-parent` the FBX-internal mesh out, delete the empty instance
root): 296 nodes in → 310 out → **310 after repack+reload, 553 material assignments in and out**.
And a **sixth L-K instance, sharp enough to be worth the lap on its own: `node-modify` on a
resource-valued property that is ALREADY SET builds a blank default resource and reports
`Type: Success`. The identical call on a NULL property works.** Two failure modes, same call
shape, no error either time. Finally, **the detail crop found a defect in the SUBSTRATE, not in any
instrument** — and prep, L4b and L4c all needed to know.

## §1 — Rubric diff against intent (law L-I — say out loud what fell out)

This cell ran **one instrument on one frozen spec**. It says **nothing** about W-PRO or H, nothing
about design quality (the spec is frozen), nothing about new-scene authoring, nothing about UI or
VFX. It answers **execution fidelity + non-destruction + iteration count, for Murzak, on an
expansion task.**

Three things a reader could over-read, named before they are:

- **"Murzak is the best tool" is not licensed by this cell.** No comparison was run. Its wall-clock
  number (§6) is dominated by operator decision time, not instrument time, so even the speed
  reading is not what it looks like.
- **The P-3 result is about a manifest, not about intelligence.** Murzak did not "choose" node-by-node
  over W→H. Its read surface has a hole (§4) that forced the *reading* onto a script and left the
  *writing* on the node family. A different task shape could route differently.
- **The pillar banding (§8) is the substrate's, and I nearly filed it as my own defect.** It is in
  `scene_before.tscn`, it predates every instrument, and it will appear in L4b and L4c identically.

## §2 — Spec conformance checklist — six clauses, each with its measurement

Measured off the **saved file**, reloaded, by an independent probe. Raw: `evidence/l4/l4a/logs/VERIFY.txt`.

| # | Clause | Measured | Verdict |
|---|---|---|---|
| **1** | Platform 6.0 × 4.0 × 0.6, centred X=0, back edge flush to far wall inner face | world `x[-3.00000, 3.00000] y[0.00000, 0.60000] z[-8.75000, -4.75000]`; size `6.00000 × 0.60000 × 4.00000`; X centre `0.000000`; **back edge z = −8.750000 = the far wall's measured inner face** | **PASS** |
| **2** | Two flights, 4 steps, 0.15 rise × 0.40 run, 1.2 wide, ascending −Z | all 8 steps: width `1.2000`, run `0.4000`, rise `0.1500`; tops `0.1500 / 0.3000 / 0.4500 / 0.6000`; +X flight `x[3.0000, 4.2000]`, −X flight `x[-4.2000, -3.0000]`; z runs `-3.15 → -4.75`, top tread flush with the dais top **and** its front edge | **PASS** |
| **3** | Two pack pillars **on** the dais, front (+Z) corners, inset 0.5 m from each edge | `SM_Bld_Base_Pillar_01`, height `3.01515` (native `3.015154`); centres `(±2.50000, ·, −5.25000)`; **inset from the +Z edge = 0.50000, from the X edge = 0.50000**; footprint entirely within the platform | **PASS** — with one number declared: base y = `0.595866` against a dais top of `0.600000`, i.e. **4.13 mm seated into the slab**. Consequence of the pillar mesh's own AABB origin (`−0.008612` y) plus the FBX's `+0.004478` internal offset, both preserved by `keepGlobalTransform`. Seated, not floating |
| **4** | `SM_Prop_Brazier_04` ×2 at the dais front edge, symmetric about X=0, **measured texture presence per TCP-16 as amended by TCP-25 (MEAN, never variance)** | centres `(±1.20000, ·, −5.10000)`, **base y = 0.600000 exactly** (base-centred origin, as the constants file promised); size `0.6864 × 1.2404 × 0.6864` = native to 4 dp. **Rendered mean, untextured → atlas-mapped: R `(157.4, 152.8, 145.1)` → `(87.5, 84.2, 78.2)`; L `(133.2, 128.9, 122.9)` → `(66.1, 63.8, 60.1)`.** Prep's independent figure for the same prop is `(206.0, 206.8, 210.1)` raw → `(81.8, 85.2, 89.2)` atlas-mapped — **my textured number reproduces prep's to within a few counts, from a different frame and a different rig** | **PASS** |
| **5** | **NON-DESTRUCTION** — nothing moved, deleted, renamed or re-parented | **Structural:** 294 original `Node3D` paths; **missing 0, moved 0**, added 14; `Key`, `Fill`, `InteriorPool`, `WorldEnvironment` all present. **Pixel (P-2, decisive):** see §5 | **PASS** |
| **6** | Camera — `__box`, parameters verbatim from the constants file | rig printed `eye=(23.123901, 39.502224, 21.687008)`, `basis_x=(0.681998, 0.000000, -0.731354)`, `fov=20.000000`, `near/far 0.02/2000` — identical to `L4_KIT_CONSTANTS.md` §7. Independently proven non-perturbing: `scene_before` re-rendered **after** restoring the `godot_mcp` plugin line is **byte-identical** to prep's reference, sha `248b6b94…` | **PASS** |

**One thing the spec does not cover and I did anyway, declared so it is not read as conformance:**
the dais and step materials were given `uv1_scale` (platform `4.8, 3.2`; steps `0.96, 0.32`) so the
floor texture tiles at the room's measured 1.25 m pitch, and `cull_mode=2` / `roughness=0.9` to
match the room's own materials exactly. Without it the dais rendered as smooth pale concrete in a
stone room. **This is an operator ruling, not a spec clause, and it is equally available to L4b and
L4c** — it should not count for or against any cell.

## §3 — P-3, the prediction this cell was designed to protect: **NODE-BY-NODE, not W→H**

**The first prompt was written to disk before any wire call and before the manifest was
re-enumerated** — `evidence/l4/l4a/FIRST_PROMPT_VERBATIM.txt`. It contains **no method noun**: not
"script", not "builder", not "headless", not "node", not "create", not "place", not "instance". It
states geometry and a save. The **decision procedure** was then fixed in writing, also before
execution — `evidence/l4/l4a/ROUTE_DECISION.txt` — and it was written to be able to return
"node-by-node", with three pinned conditions that would license leaving the node family.

**Declared contamination, because pretending otherwise is worth less than naming it:** I ran L3, in
which Murzak authored a builder via `script-create` and it ran headless in 0.30 s. That cannot be
unlearned. The guards were (a) no method noun in the prompt, (b) start on the *other* surface, (c)
require a quoted blocking artifact to leave it. **The claim the evidence supports is not that the
operator was naive — it is that the choice was made against the manifest with the reasoning fixed
in advance.**

**What actually happened, and it was not a preference:**

- **Budget did not decide it.** Node-by-node costs ~60–70 calls at 8 ms — under a second of wire.
  I wrote that down before starting.
- **The task's first demand is a READ** ("back edge flush to the far wall's inner face"), and
  **Murzak's wire cannot read a transform** (§4). That forced *the read* onto `script-create`.
- **The write stayed on the node family for the whole run.** 13 nodes + 7 resources authored through
  `node-create` / `node-modify` / `resource-create` / `resource-modify` / `node-set-parent` /
  `node-delete`. **No builder script was ever authored.** Every `.gd` this cell created is a
  read-only probe or a verifier.

**So P-3 resolves: W-MUR went NODE-BY-NODE.** The charter said *"if it instead goes node-by-node,
record that — it means the W→H path needs deliberate prompting rather than being the natural
groove."* **Recorded. That is what happened, and the program's central bet is weaker for it** —
W→H is a real capability (L3 proved it end to end) but it is **not** where the tool's shape points
you for a bounded expansion. For 13 nodes the node family is the obvious surface and the manifest
makes it the obvious surface.

**The honest qualifier:** this is one task at one size. At 300 nodes the arithmetic would likely
push the other way. What this cell falsifies is *"W→H is the natural groove"* stated without a size
qualifier — the fifth time in this program a one-condition measurement was generalized to a class.

## §4 — The finding that shaped the run: **Murzak's wire cannot read a transform**

Checked across **all 39 live tools** (re-enumerated this lap per L-C: 39 tools / 11 families,
byte-identical name set to L3 — `evidence/l4/l4a/MUR_LIVE_MANIFEST_L4A.json`).

| surface | what it returns | transform? |
|---|---|---|
| `scene-get-data` | `instanceId, name, path, type, childCount` | **no** |
| `node-find` | the same field set — **verified empirically, not inferred** | **no** |
| `resource-get-data` on `res://scene_l4a_wmur.tscn` | `{"name":"…","typeName":"Godot.PackedScene","value":{"instanceId":0,"resourcePath":"…"}}` — the ref, nothing else | **no** |
| `script-read` | *"Must end in '.cs' or '.gd'."* | cannot open a `.tscn` |
| `filesystem-list` | directory entries + importer type + uid, *"no resource is loaded"* | **no** |
| `reflection-method-call` | see below | **no** |

There is **no `node-get-properties` tool in the 39.** Pro ships `get_node_properties`; Murzak does not.

**The reflection escape hatch — the thing that closed the "can it measure AND create" question on
paper — cannot reach a Node.** `reflection-method-find` finds `Godot.Node3D.GetGlobalPosition()`
cleanly and returns its schema. Calling it fails at the target:

```
Tool execution failed for 'Method C# / Call': One or more errors occurred.
  ('targetObject' deserialized instance is null. Please specify 'targetObject' properly.)
```

**Root cause read from source, not guessed** — `Runtime/Reflection/GodotReflectorFactory.cs`
`RegisterGodotConverters` registers exactly five: `Godot_Vector2_`, `Godot_Vector3_`,
`Godot_Color_`, `Godot_Resource_ReflectionConverter`, and `GodotNodePathJsonConverter`. **There is
no Godot *Node* reflection converter.** A live scene Node cannot cross the MCP boundary as a target
object, so every Node instance method is unreachable by reflection. That is a structural ceiling and
it is named (L-G).

**Consequence for the program's picture of this tool.** The manifest audit's decisive claim was that
*"Murzak closes both — measure and create."* **For Resources, yes. For Nodes, it creates and cannot
measure.** That is the exact inverse of W-INC (*"the wire inspects, it does not build"*) and it is
worth a ledger line, because the audit's phrasing does not survive contact.

**Two schema disagreements found on the way, both L-B:**

1. `reflection-method-call`'s own description documents `targetObject` as `{ type, value }`. The wire
   rejects `type` and names the truth in the error body: *"Did you want to use 'name', 'typeName',
   'value', 'fields' or 'props'?"* **The tool's description contradicts the tool.**
2. `parametersMatchLevel` defaults to **2 (equals)** on `call` but **0 (ignore)** on `find`. A filter
   that finds a method will not call it. Fixed by passing `parametersMatchLevel: 0`.

**What I did instead (forced, per pinned condition (c)):** authored a read probe via `script-create`
and ran it headless. It returned the far wall's inner face at **z = −8.75000**, floor top
**y = +0.008091**, floor extent `x[−8.750000, 8.749944] z[−8.750000, 8.749948]`, the four wall rows,
the node naming scheme, and the room's actual materials. Full record:
`evidence/l4/l4a/SCENE_READ.txt`.

**A cross-check worth stating, because neither side was fitted to the other.** Prep's diff mask was
written from the frozen spec **before any cell ran**, and its comment derives *"stairs → x to ±4.2,
z to −3.15"*. My arithmetic, computed from the scene read, lands on **±4.2 and −3.15 independently**.
Two derivations, one answer.

## §5 — P-2, DECISIVE: non-destruction

Run with **prep's already-calibrated differ, unmodified** (`prep/l4_diff.py`).

| | |
|---|---|
| pixels measured (outside the addition) | **1,730,817** (mask covers 342,783 px = 16.53 %) |
| **changed pixels** | **30** — `0.0017 %` |
| **max channel delta** | **1** — and the per-pixel histogram is `{1: 30}`, i.e. **every one of the 30 is a single least-significant bit** |
| mean abs diff | `5.78 × 10⁻⁶` |
| p99.9 channel delta | `0.0` |
| inside the addition (sanity) | 106,161 changed px, max delta 174, mean 5.53 — **the addition is plainly there** |

**Prep's instruction was to check the mask boundary before attributing damage** (its §6.4: shadow
spill is the differ's one lying direction, and it lies toward *false conviction*). I checked it
rather than asserting it: **29 of the 30 pixels lie within 20 px of the mask hull, 27 within 15 px,
8 within 2 px.** One lies beyond 25 px. Located and pictured:
`evidence/l4/l4a/diff/P2_OUTSIDE_PIXELS_LOCATED.png`.

**Verdict: PASS.** Thirty LSB flips hugging the mask edge is the dais's shadow penumbra shifting by
less than one quantization step. It is not damage, and the structural check agrees independently:
**0 missing, 0 moved, 0 renamed, 0 re-parented** across 294 original `Node3D` paths.

**A number L4b and L4c should have before they run, and prep could not have supplied it.** Prep's
zero point was `scene_before` against *itself* — necessarily 0. **A cell that legitimately adds
geometry perturbs the shadow at the mask edge, so the passing floor is not 0; for this addition it
is ~30 LSB pixels.** A cell reporting a few dozen delta-1 pixels at the boundary has passed. A cell
reporting delta >1, or pixels far from the hull, has not.

**The picture, and I judged it with my eyes:** `evidence/l4/l4a/diff/L4A_WMUR_DIFFx4_MASKED.png` —
outside the orange hull the frame is **pure black across its whole area**. The only signal is inside
the hull, and it is exactly the addition's silhouette: the slab, both stair flights, both pillars,
both braziers and the cast shadow. Nothing else in the room registers at ×4 amplification.

## §6 — P-4, wall-clock — with statistic, n and exclusions (TCP-19)

**Server-side handler times, parsed from `logs/server-l4a.log`:**

```
tools/call   n=119   MEDIAN=6.93 ms   q1=6.20   q3=17.96   p95=35.24   mean=49.89   max=4061.90
             calls > 100 ms: 3  ->  164.3, 304.5, 4061.90
             EXCLUSIONS: NONE APPLIED. Every tools/call the server handled is in the set.
tools/list   n=1     56.97 ms
initialize   n=26    median 0.09 ms
```

**The mean (49.89 ms) is 7× the median and is meaningless** — it is three calls, named above: the
4061.9 ms one is the readiness `ping` fired by `editor_up.sh` while the plugin was still connecting;
304.5 ms is `scene-open` on a 296-node scene; 164.3 ms is the first `reflection-method-find` (an
all-assembly scan). **This is TCP-19's rule doing exactly the work it was written for.** Client-side
ledgers agree: **117 plan calls, 1.943 s total.**

**The elapsed-time decomposition, and it is the actual P-4 finding:**

| span | wall-clock |
|---|---|
| cycle 1 — read + author + save | 518.6 s |
| cycles 2–3 — fixes | 581.8 s |
| **all authoring and fixing** | **1100.4 s (18m 20s)** |
| including final renders | 1297.6 s (21m 37s) |

| instrument time inside that span | |
|---|---|
| wire, 117 calls | **1.943 s** |
| headless script runs, 7 | ~4.1 s (**median 0.58 s, n=5**, sorted 0.57/0.58/0.58/0.58/0.74, no exclusions) |
| renders, 8 | ~11.1 s (**median 1.39 s, n=3**, 1.37/1.39/1.59) |
| **total** | **~17.1 s = 1.3 % of elapsed** |

**98.7 % of this cell's wall-clock was the operator deciding what to call.** The charter's P-4
("H wins wall-clock, but by a narrower margin") is framed as an instrument comparison; **at this
task size wall-clock is not an instrument property at all.** TCP-15 corrected the latency constant
and TCP-19 corrected its statistic; this cell says the metric itself is measuring the wrong thing
for T2. **P-5 is the axis that carries the information, and the charter was right to add it.**

## §7 — P-5, ITERATION COUNT — 3 cycles, and what each one was for

An **author→look→fix cycle** = authoring, then a **rendered frame judged by eye**, then fixes driven
by what the frame showed.

| # | Authored | The look showed | Fixed |
|---|---|---|---|
| **1** | The whole dais: 7 resources, 13 nodes, materials, save | `CYCLE1_wide` + `CYCLE1_detail`: geometry all correct and in place — **and the two pillars and two braziers rendering as bright white blobs.** Dais reading as smooth pale concrete | The **instrument defect** (§9): reparent the FBX-internal meshes out with `node-set-parent`, delete the emptied instance roots, re-assign materials **null-first**. Plus the declared `uv1_scale` ruling |
| **2** | The above | `CYCLE2_detail`: braziers correct. Pillars textured but **palette-banded** → investigated, **substrate property, no fix owed** (§8). **Step faces showing a fine grid** — a side effect of my own uv ruling. Materials differing from the room in `cull_mode` and `roughness` | `cull_mode=2`, `roughness=0.9` to match the room; a step-scaled material at `uv1_scale (0.96, 0.32)` |
| **3** | The above | `L4A_WMUR__box` + `L4A_WMUR_DETAIL`: steps read as stone, materials match the room, all six clauses hold | — |

**3 cycles.** Decomposition, because the bare number would mislead:

- **1 of 3 was caused by the instrument** (the silent material drop). Cycle 1's fix was entirely
  instrument-workaround.
- **2 of 3 were presentation fidelity the frozen spec never demanded** — my own `uv1_scale` ruling
  and its side effect, plus matching the room's `cull_mode`/`roughness`. A cell that shipped after
  cycle 1's fix would still have passed all six clauses.
- **0 were spent on geometry.** Every placement was correct on the first authoring pass, to five
  decimal places, first try. The spec arithmetic never needed a look to correct it.

**Two more iterations that were NOT render-gated, reported separately so the count is not flattered:**
the reparent probe (`p15`) and the null-first probe (`p18`) were each a one-node experiment verified
by reading the `.tscn` off disk. **Counting looks-at-a-file as cycles would give 5.** I report 3 by
the render-gated definition and name the other 2 rather than hiding them, because L4b and L4c must
count the same way or the number is not comparable.

**A finer count that may be the most useful of the three: wire *aim* failures — 6.** Three
`targetObject` shapes tried before abandoning reflection; two `Name`-set shapes tried before naming
it a ceiling; one silent `MaterialOverride` failure. **Aim, not latency, is what the wire costs.**

## §8 — What the DETAIL CROP found, and it is in the SUBSTRATE

The charter added the detail crop after the conductor looked at prep's reference frame and judged
the dais unjudgeable at `__box`. It was right, and it caught more than it was aimed at.

**At `__box` the added pillars read as small dark uprights. At the detail framing they read as
strongly banded in atlas-palette colours** — green, red, blue, pink. My first reaction was that I
had produced the L1 void-cap rainbow.

**Measured instead of assumed.** The added pillar and the room's own `Pillars/Pillar_0`:

```
mesh        SM_Bld_Base_Pillar_01   identical, 1 surface, 96 vertices, both
UVs         u[0.00648, 0.58454]  v[-0.14026, 0.99763]   IDENTICAL to five decimals
texture     PolygonDarkFortress_Texture_01_A.png        identical
uv1_scale   (1.0, 1.0, 1.0)                             identical
```

Then, because L-A says an argument from numbers is not a frame, **a control picture**:
`evidence/l4/l4a/frames/CONTROL_pillar_room_vs_added.png` — the room's own `Pillar_0` and my added
pillar, cloned into open floor **in memory only** (the scene on disk was never written; its hash is
unchanged), photographed side by side under the room's own lights. **They are indistinguishable.**
Same shaft, same fern motif, same banding.

**So the banding is the pack's own atlas mapping for `SM_Bld_Base_Pillar_01`. It is in
`scene_before.tscn`. It predates every instrument in this lap.** It was invisible to prep only
because the room's corner pillars sit at `x,z = ±8.975` while the wall inner faces are at `±8.75` —
**they poke 0.11 m into the room and are ~89 % buried in the wall corners**, and at `__box` they are
about 50 px of heavily-mipmapped tan.

**Why this matters beyond aesthetics.** L4b and L4c will place the same module in the same open
position and see the same banding. **Without this note, one of them spends a cycle "fixing" a
substrate property** — and P-5 is the lap's headline metric. **The crop earned its place before any
cell was compared.**

## §9 — L-K, SIXTH INSTANCE: `node-modify` on a non-null resource property builds a blank

**Both clauses of TCP-21 are satisfied, so this is a genuine instance and not a mis-attribution.**
The tool reported success **and** the operation was correctly invoked — correct node path, real C#
property name, `scene-save` called in the same plan.

**The failure.** Setting `MaterialOverride` to `{"instanceId":0,"resourcePath":"res://l4a/mat_atlas.tres"}`:

*When the property is **null**:*
```
[Success] Resolved Resource resourcePath='res://l4a/mat_atlas.tres' to a live 'Material'.
[Success] Object 'null' modified with type 'Godot.Material'.
```
→ saves as `material_override = ExtResource("13_t3yuh")`. **Correct.**

*When the property **already holds a material** — same tool, same argument shape:*
```
[Success] Set value
  was: type='Godot.StandardMaterial3D', value='<StandardMaterial3D#...428>'
  new: type='Godot.StandardMaterial3D', value='<StandardMaterial3D#...126>'.
[Success] Value '<...126>' modified to  {"instanceId": 0, "resourcePath": "res://l4a/mat_atlas.tres"}
[Info]    No fields modified.
[Info]    No properties modified.
```
→ saves as `[sub_resource type="StandardMaterial3D" id="…"]` **with zero properties. A blank white
default. The texture is gone.**

**Mechanism.** `Godot_Resource_ReflectionConverter` resolves the ref only on the *assign* path. On
the *modify-in-place* path ReflectorNet constructs a fresh default of the declared type and tries to
populate it **from the ref object treated as fields** — `instanceId` and `resourcePath` are not
`StandardMaterial3D` members, so *"No properties modified"*, and you are left holding a blank.

**Both report `Type: Success`. `isError` is `false` in both. The only tell is the message text**, and
you have to already know what the two shapes mean. This is L-K's most dangerous form yet: not a tool
that always lies, but **a tool that tells the truth on one code path and not the other, with no
signal at the boundary.**

**Workaround, verified end to end:** null the property first, then assign.
```
node-modify  jsonPatch {"MaterialOverride": null}
node-modify  jsonPatch {"MaterialOverride": {"instanceId":0,"resourcePath":"res://…tres"}}
```
Applied to all four props and later to all eight steps (where the trap fired a **second** time —
it is standing, not a one-off).

**This was caught by a rendered frame.** Twelve `Success` returns, a clean `scene-save`, a
310-node file — and two white pillars and two white braziers in the picture. **L-K's law holds
exactly as written.**

## §10 — P-6, the save-duplication hazard: **a non-lossy path exists, and here it is**

The charter handed over no known-good route and asked each cell to find one or name its ceiling.
Prep measured three routes and none gave both correct node count and surviving materials.

**What Murzak does by default.** `node-create`'s own description: *"The new Node's owner is set to
the edited scene root so it is saved with the scene."* **Singular — the instance root only.** So the
four FBX props saved as `instance=ExtResource(...)` carrying **only a transform**, and the
`material_override` I had set on their internal `MeshInstance3D` children **was not in the file at
all.** That is TCP-24's *own-root-only* pole exactly: **correct node count, every material silently
dropped.**

**Worse than prep's version, and worth stating:** the empty instance roots would have **re-instanced
their internal children on reload** — so the file would have shipped a correct node count that
reloaded into geometry with no overrides, and any later reparenting would have produced the
duplication too.

**The non-lossy path, all on the node family:**

1. `node-set-parent` the FBX-internal `MeshInstance3D` up to the addition's holder, with
   `keepGlobalTransform: true` — it becomes a real owned node.
2. `node-delete` the now-empty FBX instance root — **this step is not optional**; leave it and Godot
   re-instances the FBX on load and you have both copies.
3. `node-modify` the material **null-first** (§9).

**Measured, on the saved file, reloaded:**

```
scene_before.tscn          live nodes on load          296
scene_l4a_wmur.tscn        live nodes on load          310      (+14, exactly the addition)
REPACK + RELOAD            live nodes                  310      pack err=0
MeshInstance3D             before 301  ->  after 301
material assignments       before 553  ->  after 553
```

**No duplication. No material loss. Both poles of TCP-24's trilemma avoided.** The cost is that the
FBX geometry is **inlined** into the scene as `SubResource("ArrayMesh_…")` rather than referenced
from the `.fbx` — the mesh is copied, deduped against the substrate's existing pillar mesh. Declared,
because it changes the file's relationship to the asset: **the addition no longer tracks the FBX if
the FBX is reimported.** For a photographed lap scene that is free; for a production pipeline it is
a real trade and it should be on the record before anyone copies this recipe.

**The forecast in P-6 was: "at least one instrument ships duplicated pillars and does not notice,
because every call returned `ok`."** For this cell, **half of it happened.** Nothing duplicated —
but the materials vanished with every call returning `ok`, and **only the rendered frame noticed.**

## §11 — Frames, judged with my own eyes (L-A)

**TCP-23 honoured throughout: one scene per process, every capture.** Eight renders, eight processes.

### The wide shot — `evidence/l4/l4a/frames/L4A_WMUR__box.png` (sha `42eacc66…`)

A 17.5 m room from high to the southeast on black void. **The room is intact and I can see that it
is:** warm grey-tan brick floor tiling clean across the full span with no seam or palette artefact;
four dark blue-grey walls, the two far ones showing inner faces at full height, the two near ones as
thin top bands; wall-top void caps reading as a darker course along every wall top; corner pillars
with toppers at three visible corners; the soft warm `InteriorPool` pool near floor centre. **It is
prep's reference frame with one thing added and nothing taken away.**

Against the far (upper-right) wall: the dais, a raised slab reading marginally darker than the floor,
its two stair flights visible as small stepped wedges at each end, two pillars standing at its front
corners, two braziers between them, and a clean shadow thrown toward +X — consistent with the Key
light's measured direction `(0.2204, −0.8829, −0.4145)`. It sits in the upper-right quadrant,
exactly where prep said the mask hull lands.

### The detail crop — `evidence/l4/l4a/frames/L4A_WMUR_DETAIL.png` (sha `416c897d…`)

**Declared once here. L4b and L4c reuse these verbatim.** Rig: `project/l4_detail_shoot.gd`
(drax-authored, TCP-8; one scene per process, enforced).

```
CAM_FOV     20.0    (VERTICAL — Godot Camera3D keep_aspect defaults to KEEP_HEIGHT)
CAM_PITCH  -32.0
CAM_YAW     47.0    IDENTICAL to __box
CAM_DIST    18.0
CAM_AIM    (0.0, 1.0, -6.0)
near/far    0.02 / 2000.0      viewport 1920x1080  MSAA_4X  SubViewport
resolved:   eye=(11.164016, 10.538547, 4.410613)
            basis_x=( 0.681998,  0.000000, -0.731354)
            basis_y=(-0.387558,  0.848048, -0.361404)
            basis_z=( 0.620223,  0.529919,  0.578367)
```

**Why pitch −32 and not `__box`'s −50, since the choice binds two other cells.** The two things this
frame must settle pull opposite ways: **the 0.5 m pillar inset is a plan measurement** and wants a
steep look-down; **the 0.15 m step rise is an elevation measurement** and a steep look-down
foreshortens it to nothing. −32 keeps the dais top open enough to read the inset while giving the
four risers real screen height. **Yaw is left at `__box`'s 47** so the crop is the same room dollied
and tilted, not a different view — and so no cell can be advantaged by a flattering framing.

**What I see:** the dais slab against the far wall, front and side faces reading as tiled stone at
the room's pitch. On the left, the −X flight: **four steps, individually countable, even rise, even
run**. On the right, the +X flight in shadow, its treads still separable. Two pillars on the slab at
its front corners, visibly inset from both edges, banded in the pack's atlas palette (§8). Between
them, two braziers — dark metal tripods with a bowl — symmetric about centre, seated flat on the
dais. **Every clause the crop was added to adjudicate is adjudicable in it.**

### Also shipped

| frame | what it is for |
|---|---|
| `CYCLE1_wide.png`, `CYCLE1_detail.png` | the P-5 trace, cycle 1 — **the white-blob failure, photographed** |
| `CYCLE2_wide.png`, `CYCLE2_detail.png` | the P-5 trace, cycle 2 |
| `CONTROL_pillar_room_vs_added.png` | §8's control — the room's pillar beside mine |
| `diff/L4A_WMUR_DIFFx4_MASKED.png` | P-2, the ×4 masked strip |
| `diff/P2_OUTSIDE_PIXELS_LOCATED.png` | the 30 outside pixels ringed against the mask hull |

## §12 — Exit predicate, item by item

| # | Item | Status |
|---|---|---|
| 1 | Six-clause conformance checklist, PASS/FAIL, each with its measurement | **DONE** — §2, six PASS |
| 2 | P-1..P-6 each resolved to a recorded fact with evidence | **DONE** — §3–§10 |
| 3 | Both frames shipped and judged by eye | **DONE** — §11 |
| 4 | `scene_before.tscn` hash re-verified unchanged | **DONE** — `d45db0f507f6b835e14447c9ceb7e7e6bd645e070bc1fe1241dd6e8522de1966`, mode `0444`, identical to prep. **Cell is not void** |
| 5 | TCP-20 fingerprint before/after incl. out-of-lab surfaces | **DONE** — below |
| 6 | No Godot / `gamedev-mcp-server` left running; check for inherited orphans | **DONE** — below |
| 7 | No other cell's output touched | **DONE** — L4b/L4c do not exist |

**P-1 — does the dais geometry come out at all?** **YES.** 13 nodes, all six clauses, first authoring
pass correct on every placement.

### TCP-20 blast radius — identical on every product surface

| surface | files | before vs after |
|---|---|---|
| `Assets/` (whole ignored value tree) | 98,823 | `041896a5…` **identical** |
| `Assets/Synty/polygon-dark-fortress` | 3,028 | `93645a4f…` **identical** — and the **3,028-file per-file manifest diffs byte-for-byte clean** |
| `addons/` | 122 | `ebd02e2e…` **identical** |
| `project.godot` | — | `a76d666a…` **identical** |
| `.godot/` mtime + count | 131,796 | **identical** |
| tracked `git status` | — | `b4e2f0ce…` **identical** |
| **`editor_settings-4.6.tres`** (the shared surface prep found written, and added to the predicate) | — | `f7a16c0b…` **identical — not written this lap** |

**One delta, named rather than rounded down:** `app_userdata/tcp_l3_lab` went **12 → 14 files**. Mine:
`user://l4a_p6_roundtrip.tscn` from the P-6 repack test plus a log. Inside the lab's own userdata,
removable per `UNINSTALL.md` §3.

### Exit state

```
pgrep 'Godot|gamedev-mcp-server|dotnet'   ->  NONE
port 27435                                ->  not listening
```

**Inherited orphans checked at session start** (L3 found one that outlived a prior cleanup): none
present. Editor launches this cell: **one**, headless, reaped by `editor_down.sh`. Server: one,
started fresh, killed at close.

### Q45 / Q46 — self-hosting held, and it held because we made it

```
[Godot-MCP] connecting (mode=Custom, host=http://localhost:27435) ...
[Godot-MCP] connected.
```
**Zero occurrences of `ai-game.dev` in this launch's log.** The four `GODOT_MCP_*` vars are the only
thing that did that. **Q46 stands unchanged and is not mitigated by this cell** — the compiled-in
default is still Cloud. Two related observations:

- The plugin logs `derivedPort=27435 (portOverridden=False)` — it **derives** a per-project port from
  the project-path hash. **The server does not: its default is `MCP_PLUGIN_PORT=8080`.** Launched by
  L3's §8 procedure verbatim, the relay comes up on 8080 and the plugin dials 27435, and **the wire
  never connects** — with no error that names the cause. See §13.
- The addon again wrote **39 `SKILL.md` files** into `project/.claude/skills/` uninvited on plugin
  load (L3 §4.12). Expected, recorded, harmless in a lab.

## §13 — Defects found (the dispatch said to assume more; there were four)

1. **L3 §8's executable launch procedure is incomplete and fails silently.** It starts the relay with
   no `MCP_PLUGIN_PORT`, so the server binds **8080** while the plugin derives **27435** from the
   project hash and dials that. Nothing errors; the tool list is simply empty. Fixed here by
   exporting `MCP_PLUGIN_PORT=27435` before launch. **L4b and L4c inherit the broken procedure unless
   this is propagated.** The vendor's own defaults disagree with each other — the plugin derives a
   port, the server does not.

2. **My own capture rig is now two rigs, and only one of them was standing.** The charter asked for a
   detail crop after prep had already frozen `l4_shoot.gd`. I did **not** modify the standing rig —
   the wide shot must stay bit-identical across cells — and wrote a sibling instead. **Recorded
   because the natural move was to add a second mode to `l4_shoot.gd`, and that would have silently
   changed the instrument the other two cells are measured with.**

3. **Prep's P-2 zero point is not the passing floor for a cell** (§5). Prep calibrated
   `scene_before` against itself, which is necessarily 0. Any cell that adds geometry moves the
   shadow at the mask edge. **A cell told "the zero point is exactly zero" and finding 30 pixels
   could reasonably report damage.** The empirical floor is published here.

4. **The detail crop found a substrate property that prep's framing hid** (§8), and it is the kind
   that costs a cycle if a cell meets it cold.

**And one contamination hazard I could only half-close** — full note at
`~/Games/mcp-lab/prep/l4a_residue/README_DO_NOT_PLACE_IN_PROJECT.md`. I relocated my probe and
verifier scripts out of `project/` (prep's `l3_residue` precedent), **because `l4a_probe_read.gd` is
a worked answer to "how do I read the far wall out of a scene I did not author" — which is P-4's
substance.** Verified afterwards: the scene re-renders **byte-identical** to the shipped frame.

**What I could not relocate, and it is a conductor call:** `res://scene_l4a_wmur.tscn` carries every
solved placement, and `res://l4a/mesh_platform.tres` is literally `size = Vector3(6, 0.6, 4)` — **the
spec's arithmetic, on disk, in the directory L4b and L4c will work in.** They must stay renderable
because charter §5.1 has the H dispatch build a four-cell contact sheet from them. The dispatch
already makes peeking a HALT; what is new is that the risk is **passive** — `filesystem-list` of
`res://` returns `l4a/`, and Pro enumerates the project tree by default. Two cheap options are in the
README; I did not take the stronger one unilaterally because moving a cell's output before the
contact sheet exists risks the exit predicate.

## §14 — For the conductor

**No HALT was triggered.** Nothing written into any product repo; no `sudo`; no machine-wide install;
`/Applications/Godot.app` never invoked; the frozen substrate never opened for write and its hash
re-verified; Murzak never launched without the full self-hosted env block; the FORBIDDEN and
`l3_residue` directories were never read, opened or referenced.

**Five things worth a ruling or a ledger line:**

1. **P-3 resolved against the program's central bet, on a manifest fact.** *"W→H is the single most
   likely winner of the whole program"* was asserted from a tool list. This cell says W→H is a real
   capability that is **not the natural groove for a bounded expansion** — 13 nodes goes node-by-node
   because the manifest makes that the obvious surface. **The claim needs a size qualifier or it is
   the same one-condition generalization the program has now made five times.**

2. **The Murzak audit's "closes both — measure and create" does not survive contact.** For Resources,
   yes. **For Nodes it creates and cannot measure** — no `node-get-properties`, and no Node reflection
   converter, verified in source. That is the exact inverse of W-INC and it belongs in the ledger
   before Murzak is scored.

3. **L-K instance #6 (§9) is a new shape and I think it is the most dangerous one yet** — the same
   call, same arguments, succeeds on a null property and silently produces a blank on a non-null one.
   Prior instances were tools that lied consistently. This one is correct half the time.

4. **P-6 has a non-lossy route and it is publishable** (§10) — reparent-out, delete the instance root,
   assign null-first. 296 → 310 → 310, 553 materials in and out. **The declared cost is that FBX
   geometry inlines into the scene and stops tracking the asset.** Whether that is acceptable as a
   *pattern* rather than a lap workaround is above my seam.

5. **P-4 is measuring the wrong thing for T2** (§6). 1.3 % of this cell's wall-clock was instrument
   time. TCP-15 fixed the number and TCP-19 fixed the statistic; this says the **metric** does not
   carry information at this task size, and **P-5 does.**

**Honorable-fallback status (L-F/L-G):** nothing needed one — but two ceilings were hit and are
**named with their exact blocking artifacts**, per L-G: (a) `reflection-method-call` cannot resolve a
live Node as `targetObject`, attributed to the absent converter in
`GodotReflectorFactory.RegisterGodotConverters`; (b) `Name` cannot be set through `node-modify` by
either surface — *"The JSON value could not be converted to Godot.StringName"* via `jsonPatch` and
via `pathPatches` with an explicit `Godot.StringName` typeName. Consequence: **two added nodes carry
Godot's auto-generated names** (`_MeshInstance3D_27179`, `_MeshInstance3D_27180`). Cosmetic, visible
in the `.tscn`, unfixable on this wire.

---

## Artifact index

**Report:** `agentic_orchestration/drax/notes/2026-07-25-tcp-l4a-wmur-run-report.md`

| Artifact | Path |
|---|---|
| **THE CELL'S SCENE** (sha `13b671e8…`, 310 nodes) | `~/Games/mcp-lab/project/scene_l4a_wmur.tscn` |
| **WIDE SHOT** — `__box`, proves non-destruction | `~/Games/mcp-lab/evidence/l4/l4a/frames/L4A_WMUR__box.png` |
| **DETAIL CROP** — proves conformance; params declared §11 | `~/Games/mcp-lab/evidence/l4/l4a/frames/L4A_WMUR_DETAIL.png` |
| **DETAIL RIG — L4b/L4c reuse verbatim** | `~/Games/mcp-lab/project/l4_detail_shoot.gd`, `l4_detail_shoot.tscn` |
| **P-3 evidence — first prompt, written before any wire call** | `~/Games/mcp-lab/evidence/l4/l4a/FIRST_PROMPT_VERBATIM.txt` |
| **P-3 evidence — route procedure, fixed before execution** | `~/Games/mcp-lab/evidence/l4/l4a/ROUTE_DECISION.txt` |
| **P-4 evidence — what was read out of the scene** | `~/Games/mcp-lab/evidence/l4/l4a/SCENE_READ.txt` |
| **P-2 diff** (JSON + ×4 strips + located pixels) | `~/Games/mcp-lab/evidence/l4/l4a/diff/` |
| **Six-clause + P-6 verification, raw** | `~/Games/mcp-lab/evidence/l4/l4a/logs/VERIFY.txt` |
| §8 control — room pillar vs added pillar | `~/Games/mcp-lab/evidence/l4/l4a/frames/CONTROL_pillar_room_vs_added.png` |
| P-5 trace frames (cycles 1 and 2) | `~/Games/mcp-lab/evidence/l4/l4a/frames/CYCLE{1,2}_{wide,detail}.png` |
| Live manifest, re-enumerated this lap (39 tools) | `~/Games/mcp-lab/evidence/l4/l4a/MUR_LIVE_MANIFEST_L4A.json` |
| **All 24 wire plans, verbatim** | `~/Games/mcp-lab/evidence/l4/l4a/plans/` |
| **All 23 raw wire responses + ledgers** | `~/Games/mcp-lab/evidence/l4/l4a/logs/p*_raw.json` |
| Mesh/UV/material comparison, material dump | `~/Games/mcp-lab/evidence/l4/l4a/logs/PROBE_CMP.txt`, `PROBE_MAT.txt` |
| Region-mean sampler (TCP-25 instrument) | `~/Games/mcp-lab/evidence/l4/l4a/measure_regions.py` |
| Latency: server log / headless + render timings | `~/Games/mcp-lab/logs/server-l4a.log`, `evidence/l4/l4a/logs/headless_script_timing.txt` |
| Zero-point re-check under the restored plugin line | `~/Games/mcp-lab/evidence/l4/l4a/logs/ZEROCHECK_scene_before_pluginON.png` |
| **TCP-20 fingerprints** | `~/Games/mcp-lab/evidence/l4/TCP20_FINGERPRINT_L4A_{BEFORE,AFTER}.txt` + manifests |
| **L4a residue — DO NOT return to `project/`** | `~/Games/mcp-lab/prep/l4a_residue/` (+ its README, which carries the §13 contamination flag) |

**Signed:** drax, 2026-07-25 (presentation seam).
