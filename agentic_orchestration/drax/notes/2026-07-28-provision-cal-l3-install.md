# PC-L3-INSTALL — Layer-3 toolchain: install + positive-control probes

> **STATUS: COMPLETE** (written incrementally, tool by tool; all six rows now carry measured verdicts)

**Author:** drax (presentation seam) · **Commissioner:** gandalf (`RUN-CONDUCTOR`) · **Authorization:** Matt,
2026-07-28 (*"I definitely want the blender tools"*) · **Rider:** PROVISION-CAL post-exit, discharging
charter §8 **R-PC-10** · **Date:** 2026-07-28
**Host:** macOS 24.6.0 / Apple **M2 (arm64)** / Homebrew 6.0.12 / node v24.15.0 / npm 11.12.1

**Scope law.** This cell **installs and probes**. It does **not** edit the provisioning menu
(`legolas/notes/2026-07-26-plugin-provisioning-menu.md`) — a follow-up legolas cell adopts §9's
recommendations.

**Verdict enum (closed).** `LOADS-CLEAN` / `LOADS-DIRTY(what)` / `FAILS-LOAD(evidence)` /
`REACHES(probe)` / `REACHES-NOT(probe)`. **Boundary law: LOADS? / REACHES? — never BETTER.**
Nothing below is a quality judgement of any tool. Where a tool's output differs from its input,
that difference is recorded as a **fact about the transform**, not as an improvement or a regression.

**Corpus (read-only inputs; neither was modified — verified by leaving both directories untouched):**
- `/Users/admin/Games/mcp-lab/pct3/proj/emitted/lib_a.glb` (1,144,920 B — Godot-emitted, PC-T3)
- `/Users/admin/Games/reincarnated-godot/Assets/Synty/polygon-werewolf/SourceFiles/FBX/Unreal_Characters/SK_Chr_Werewolf_01.fbx`

**Scratch (every output):** `/Users/admin/Games/mcp-lab/pcl3/` — `bin/`, `scratch/`, `logs/`,
`npm-global/`, `row18/`

---

## §1 — Host mutations performed (the complete list)

| # | Mutation | Mechanism | Result |
|---|---|---|---|
| 1 | `/Applications/Blender.app` + `/opt/homebrew/bin/blender` | `brew install --cask blender` | **Blender 5.2.0 LTS**, hash `fbe6228777e7`, built 2026-07-14 · exit 0 |
| 2 | `@gltf-transform/cli@4.4.2` | `npm i -g`, **confined prefix** (§1.1) | installed |
| 3 | `gltfpack@1.2.0` | `npm i -g`, same confined prefix | installed |
| 4 | `gltf-validator@2.0.0-dev.3.10` (npm) | `npm i -g`, same confined prefix | installed — **and it is not a CLI** (§5) |
| 5 | Khronos `gltf_validator` 2.0.0-dev.3.10 release binary | curl + tar → `pcl3/bin/gltf_validator/` | sha256 `4751098c…10d7eef` |
| 6 | godotengine `FBX2glTF` v0.13.1 release binary | curl + unzip → `pcl3/bin/FBX2glTF-macos-x86_64/` | sha256 `336ab6bb…173cfcf3` |
| 7 | Blender user extension `fix_synty_anim_to_godot_with_autorigpro` | `blender --command extension install-file -r user_default` | installed to `~/Library/Application Support/Blender/5.2/extensions/user_default/` |

**No other host mutations.** No `sudo`. No system npm-prefix change. No Godot project files touched.
No writes anywhere under `pct3/proj/emitted/` or `reincarnated-godot/Assets/`. Mutation 7 is confined
to Blender's user extension repo, which is the row-18 definition itself.

### §1.1 — Provisioning fact: the global npm prefix on this host is root-owned

`npm config get prefix` → `/usr/local`; `/usr/local/lib/node_modules` is `root:wheel`. The literal
command in the rider **fails** here:

```
$ npm i -g @gltf-transform/cli
npm error Error: EACCES: permission denied, mkdir '/usr/local/lib/node_modules/@gltf-transform'
```

Rather than `sudo` (a larger host mutation than this rider authorises), all three npm packages were
installed with `NPM_CONFIG_PREFIX=/Users/admin/Games/mcp-lab/pcl3/npm-global`. Binaries land in
`pcl3/npm-global/bin/` and every probe below invoked them from there. **These are real installs and
real invocations.** But a future cell that types `gltf-transform` with no PATH change will get
`command not found`. Options for the next reader: export that prefix, use absolute paths, or
`sudo npm i -g` (a Matt call, not mine).

### §1.2 — Rosetta status on this host

`oahd` is running, `/Library/Apple/usr/share/rosetta` is present, `arch -x86_64 /usr/bin/true`
succeeds. **Rosetta 2 is installed and functional.** Per the rider's rule, any x86_64-only tool that
runs is therefore `LOADS-DIRTY(rosetta)` — it loads, but not natively.

---

## §2 — Row 41 · Blender 5.2.0 (headless) — **LOADS-CLEAN · REACHES(glb-import)**

**Install.** `brew install --cask blender` → exit 0. The cask served **5.2.0** — exactly the version
the menu pinned. Native arm64 build (Homebrew serves the Apple-silicon artefact on this host).

**LOADS probe** — `blender --version`:

```
Blender 5.2.0 LTS
	build date: 2026-07-14
	build commit date: 2026-07-13
	build hash: fbe6228777e7
```

**REACHES probe** — headless `blender -b -P` importing the Godot-emitted `.glb`
(`pcl3/scratch/blender_probe.py`):

```
22:56:06 | INFO: glTF import finished in 0.05s
PROBE objects=3 meshes=2 armatures=1
PROBE armature=SidekickChar bones=88
PROBE actions=0
```

Blender headless reads our own emit and reports its contents. **Verdict: `LOADS-CLEAN` +
`REACHES(headless glb import; 3 objects / 1 armature / 88 bones)`.**

**Note for the follow-up cell:** PC-T12's `Blender path is invalid or not set … Cannot configure
blender path in headless mode` (the adjacent evidence legolas correctly refused to convert into a
verdict) is a **Godot editor-setting** fact, and it remains true — installing the cask does not
populate `filesystem/import/blender/blender_path`. That is a separate, un-probed knob.

---

## §3 — Row 43 · glTF-Transform CLI — **LOADS-CLEAN · REACHES(inspect on lib_a.glb)**

**Install.** `@gltf-transform/cli@4.4.2` — **exactly the menu pin.** `gltf-transform --version` → `4.4.2`.

**REACHES probe** — `gltf-transform inspect …/pct3/proj/emitted/lib_a.glb` → exit 0, full report at
`pcl3/scratch/gltf-transform-inspect-lib_a.txt`. Verbatim extract:

```
version            2.0
generator          Godot Engine v4.6.3.stable.official@7d41c59c457bd5a245092b4e7eb2d833e3b3f8c3
extensionsUsed     GODOT_single_root
extensionsRequired none

warn: Missing optional extension, "GODOT_single_root".

SCENES   rootName SidekickChar  bbox -0.94838,-0.00298,-0.18617 → 0.94838,1.78465,0.17989
         renderVertexCount 19,884   uploadVertexCount 8,424
MESHES   SK_DMMY_BASE_01_00BODY2  TRIANGLES  8,424 vertices  u16 indices  1.12 MB
         attributes: COLOR_0:f32, JOINTS_0:u8, JOINTS_1:u8, NORMAL:f32, POSITION:f32,
                     TANGENT:f32, TEXCOORD_0..3:f32, WEIGHTS_0:f32, WEIGHTS_1:f32
MATERIALS lambert2 (OPAQUE, no textures)
TEXTURES  No textures found.
ANIMATIONS No animations found.
```

**Verdict: `LOADS-CLEAN` + `REACHES(inspect on a PC-T3 emitted .glb)`.**

---

## §4 — Row 45 · gltfpack / meshoptimizer — **LOADS-CLEAN · REACHES(pack + re-validate)**

**Install.** No brew formula exists — `brew info gltfpack`, `brew info meshoptimizer` and
`brew search gltf` all come back empty (`brew search gltf` returns only `glfw` and `gltfquicklook`).
The npm route was used: `gltfpack@1.2.0`, **exactly the menu pin.** `gltfpack -h` → `gltfpack 1.2`.

**REACHES probe** — `gltfpack -i lib_a.glb -o pcl3/scratch/lib_a.packed.glb` → exit 0,
**1,144,920 B → 231,776 B**. Re-validated with the Khronos validator (row 44's instrument):
**0 errors**, and the packed file loads.

**Transform facts recorded (facts, not judgements).** gltfpack's defaults are lossy on this asset:

| | input `lib_a.glb` | output `lib_a.packed.glb` |
|---|---|---|
| generator | Godot Engine v4.6.3.stable | gltfpack 1.2 |
| `extensionsRequired` | none | `KHR_mesh_quantization` |
| `maxUVs` | 4 | **0** |
| `maxInfluences` | 8 | **4** |
| `maxAttributes` | 12 | 5 |
| `totalVertexCount` | 8,424 | 7,150 |
| validator errors / warnings | 0 / 1 | 0 / 2 |

The extra warning is `/nodes/0: Local transforms will not affect a skinned mesh` alongside the
`NODE_SKINNED_MESH_NON_ROOT` that the input already carried.

**Verdict: `LOADS-CLEAN` + `REACHES(pack lib_a.glb → 231,776 B; output re-validates with 0 errors)`.**

---

## §5 — Row 44 · glTF-Validator (Khronos) — **LOADS-DIRTY(rosetta) · REACHES(validate lib_a.glb)**

**Install — the npm package is not a CLI.** `npm view gltf-validator` resolves (2.0.0-dev.3.10) and
installs, but its `package.json` has **`bin: null`** and only `main: index.js`. It is a dart2js
library with a JS API. There is no `gltf-validator-cli` on the registry (404). **The npm route
therefore cannot satisfy row 44's positive control.**

**Install — release binary.** Khronos release `2.0.0-dev.3.10` (published 2024-10-22) ships four
artefacts: `linux64`, `macos64`, `web`, `win64`. The macOS artefact is:

```
$ lipo -info gltf_validator
Non-fat file: gltf_validator is architecture: x86_64
```

**There is no arm64 macOS artefact in any of the 8 published releases.** It runs on this M2 host —
under Rosetta 2.

**LOADS probe** — `./gltf_validator --help` → exit 0, prints
`glTF 2.0 Validator, version 2.0.0-dev.3.10` and its 18 supported extensions.

**Menu-fact discrepancy for the follow-up cell:** the menu pins row 44 at `commit HEAD @ 2025-12-30`.
The **newest published release is 2.0.0-dev.3.10 @ 2024-10-22** — over a year older. The repo HEAD is
ahead of the last binary release; a HEAD pin would require a Dart build from source, which this cell
did not do. What is installed and probed is the **2.0.0-dev.3.10 release binary**.

**Verdict: `LOADS-DIRTY(rosetta)` + `REACHES(validate a PC-T3 emitted .glb; report read)`.**

### §5.1 — ★ What the validator says about our own emit (the high-value part)

**`lib_a.glb` — 0 errors, 1 warning, 6 infos.** Verbatim from the report
(`pcl3/scratch/lib_a.report.json`):

```
Errors: 0, Warnings: 1, Infos: 6, Hints: 0

	Warnings:
		/nodes/89: Node with a skinned mesh is not root. Parent transforms will not affect a skinned mesh.

	Infos:
		/extensionsUsed/0: Cannot validate an extension as it is not supported by the validator: 'GODOT_single_root'.
		/meshes/0/primitives/0/attributes/TANGENT: Tangents are not used because the material has no normal texture.
		/meshes/0/primitives/0/attributes/TEXCOORD_0: This object may be unused.
		/meshes/0/primitives/0/attributes/TEXCOORD_1: This object may be unused.
		/meshes/0/primitives/0/attributes/TEXCOORD_2: This object may be unused.
		/meshes/0/primitives/0/attributes/TEXCOORD_3: This object may be unused.
```

Machine codes: `NODE_SKINNED_MESH_NON_ROOT` (severity 1 = warning); `UNSUPPORTED_EXTENSION`,
`UNUSED_MESH_TANGENT`, `UNUSED_OBJECT`×4 (severity 2 = info).

Report `info` block:

```json
{"animationCount": 0, "materialCount": 1, "hasMorphTargets": false, "hasSkins": true,
 "hasTextures": false, "hasDefaultScene": true, "drawCallCount": 1,
 "totalVertexCount": 8424, "totalTriangleCount": 6628,
 "maxUVs": 4, "maxInfluences": 8, "maxAttributes": 12}
```

**Since the instrument was already loaded, all eight PC-T3 emits were validated** (read-only; reports
in `pcl3/scratch/*.report.json`). Three findings, stated as findings:

| file | errors | warnings | animationCount | anim names | nodes | skins | joints |
|---|---|---|---|---|---|---|---|
| `lib_a` | **0** | 1 | **0** | — | 90 | 1 | **88** |
| `lib_b` | 0 | 1 | 3 | `Take 001`, `swing`, `walk` | 90 | 1 | 88 |
| `lib_b1` | 0 | 1 | 3 | `Take 001`, `swing`, `walk` | 90 | 1 | 88 |
| `lib_c` | 0 | 1 | 3 | `Take 001`, `swing`, `walk` | 90 | 1 | 88 |
| `lib_check6` | 0 | 1 | 3 | `Take 001`, `walkbase`, `walksynty` | 90 | 1 | 88 |
| `lib_check6b` | 0 | 1 | 2 | `Take 001`, `walksynty` | 90 | 1 | 88 |
| `lib_check6c` | 0 | 1 | 4 | `Take 001`, `walkbase`, `walkstrip`, `walksynty` | 90 | 1 | 88 |
| `lib_control` | 0 | 1 | 3 | `Take 001`, `swing`, `walk` | 90 | 1 | 88 |

1. **★ Zero spec errors across the entire emitted corpus.** Godot 4.6.3's `GLTFDocument` writes
   conformant glTF 2.0. Whatever the L6 121-bone inversion is, **it is not a glTF spec violation** —
   an independent Khronos conformance check cannot see it. That is a genuine narrowing of the search
   space, and it is the opposite of what "located at the glTF EMIT step" might have led one to expect.
2. **★ One warning, and it is identical in all eight files:** `NODE_SKINNED_MESH_NON_ROOT` —
   *"Node with a skinned mesh is not root. Parent transforms will not affect a skinned mesh."* This is
   a systematic property of the Godot emit, not a per-file accident. It is a **structural statement
   about where the skinned mesh sits in the node hierarchy** — the closest thing in this report to a
   skeleton-topology remark. I am recording it, not interpreting it, and explicitly not proposing a fix.
3. **★ The skin carries 88 joints in every emit — not 121.** `lib_a` is additionally the only member
   of the corpus with **zero animations**; the other seven carry 2–4 named clips. Both are
   measurements; whether either is by design is a PC-T3 question, not mine.

---

## §6 — Row 42 · FBX2glTF (godotengine fork) — **LOADS-DIRTY(rosetta) · REACHES(Synty FBX → .glb)**

**Install.** No brew formula (`brew info fbx2gltf` → *"No available formula"*). Release binary route.
The menu's claim is confirmed **by measurement, not by reading the release page**:

- `godotengine/FBX2glTF` **v0.13.1** (2023-06-13) assets: `linux-x86_64.zip`, **`macos-x86_64.zip`**,
  `windows-x86_64.zip` — **no arm64 artefact.**
- `facebookincubator/FBX2glTF` (upstream, newest release **v0.9.7 @ 2019-08-10**) assets:
  `FBX2glTF-darwin-x64`, `-linux-x64`, `-windows-x64.exe` — **also no arm64.**
- ```
  $ lipo -info FBX2glTF-macos-x86_64
  Non-fat file: FBX2glTF-macos-x86_64 is architecture: x86_64
  ```

So: **a runnable macOS binary exists** — this is *not* `FAILS-LOAD(no-macos-binary)` — but it is
x86_64 only on an M2 host.

**LOADS probe** — `FBX2glTF-macos-x86_64 --version` → exit 0:
```
FBX2glTF version 0.13.1
Copyright (c) 2016-2018 Oculus VR, LLC.
```

**REACHES probe** — conversion of the real Synty asset
(`…/polygon-werewolf/SourceFiles/FBX/Unreal_Characters/SK_Chr_Werewolf_01.fbx`) to
`pcl3/scratch/werewolf01.glb`, **0.126 s wall**, exit 0:

```
Warning: could not find a image file for texture: file3221.
Warning: node /RootNode/root/pelvis uses unsupported transform inheritance type 'eInheritRrs'
     This tool will attempt to partially compensate, but glTF cannot truly express this mode.
     If this was a Maya export, consider turning off 'Segment Scale Compensate' on all joints.
     (Further warnings of this type squelched.)
Wrote 1291785 bytes of binary glTF to .../werewolf01.glb.
```

**Verdict: `LOADS-DIRTY(rosetta)` + `REACHES(SK_Chr_Werewolf_01.fbx → werewolf01.glb, 1,291,784 B)`.**

### §6.1 — What the validator says about FBX2glTF's output (banked, unprompted finding)

Running row 44's instrument on row 42's output — **1 error**:

```
Errors: 1, Warnings: 1, Infos: 6

	Errors:
		/meshes/0/primitives/0/attributes/TANGENT: Vector3 at accessor indices 40676..40678 is not of unit length: 0.0.

	Warnings:
		/nodes/1: Node with a skinned mesh is not root. Parent transforms will not affect a skinned mesh.
```

`info`: `nodes=54, skins=2, joints=[52, 52], animationCount=0, maxInfluences=8, materialCount=2`.
The `/skins/1: This object may be unused` info says one of the two identical 52-joint skins is dead
weight. Recorded as a finding about this conversion path; no action proposed.

**Two facts that sit next to each other and are worth someone's attention:** the FBX2glTF path
produces a **52-joint** skin from the werewolf source, while every Godot-emitted `lib_*.glb` carries
an **88-joint** skin. Different assets, different paths — I am not asserting a relationship, only
that both numbers were measured today by the same instrument.

---

## §7 — Row 18 · fix_synty_anim_to_godot_with_autorigpro — **LOADS-CLEAN · REACHES-NOT(arp-operator-absent)**

**What the row is.** `Vortex-Basis-LLC/fix_synty_anim_to_godot_with_autorigpro` (GPL-3.0, 16★, cold
since 2025-01-27) — a **Blender extension**, `blender_manifest.toml` schema 1.0.0, `id` matching the
row name, `blender_version_min = "4.2.0"`, no `blender_version_max`.

**Install** (in scope — the row *is* the addon; confined to Blender's user extension dir):

```
$ blender -b --command extension install-file -r user_default --enable pcl3/row18/ext.zip
STATUS Installed "fix_synty_anim_to_godot_with_autorigpro"
```

Landed at `~/Library/Application Support/Blender/5.2/extensions/user_default/fix_synty_anim_to_godot_with_autorigpro/`.

**LOADS probe** — headless enable + registration check (`pcl3/scratch/row18_probe.py`):

```
PROBE18 enable=OK
PROBE18 op_namespace_present=True
PROBE18 op_poll=True
PROBE18 panel=True
PROBE18 scene_props=True
```

The extension registers cleanly on Blender **5.2** despite declaring only `4.2.0` minimum: the
operator `fix_synty_anim_to_godot_with_autorigpro.retarget` polls `True`, the panel
`VIEW3D_PT_fix_synty_anim_to_godot_with_autorigpro` registers, and the scene properties
(`fix_synty_with_arp_import_path` etc.) are installed. **`LOADS-CLEAN`.**

**REACHES probe** — the row's actual work depends on six Auto-Rig Pro operators, which appear in the
source at `retarget_helpers.py:79,85,88,103` and `__init__.py:109,115`:

```
PROBE18 arp_namespace_present=True
PROBE18 arp.redefine_rest_pose=True   ← attribute access only; bpy.ops namespaces are lazy
PROBE18 arp.copy_bone_rest=True
PROBE18 arp.copy_raw_coordinates=True
PROBE18 arp.retarget=True
PROBE18 arp.build_bones_list=True
PROBE18 arp.import_config=True
PROBE18 arp_call=FAIL AttributeError: Calling operator "bpy.ops.arp.build_bones_list" error, could not be found
```

**Read this carefully:** `hasattr(bpy.ops.arp, …)` returns `True` for anything — `bpy.ops`
sub-namespaces are lazily constructed and never fail on attribute access. Only the **call** resolves
the operator, and the call fails: the ARP operator does not exist because **Auto-Rig Pro is a paid
Blender-Market addon and is not installed on this host.** The rider authorised a toolchain install,
not a commercial-addon purchase.

**Verdict: `LOADS-CLEAN` + `REACHES-NOT(bpy.ops.arp.* absent — Auto-Rig Pro not installed; paid dependency)`.**
Row 41 is now satisfied, so the row's *other* blocker is cleared; the paid dependency is the only
remaining one, and it is a Matt purchase decision, not a measurement gap.

---

## §8 — Reproduction commands (for the next cell)

```bash
export PATH=/Users/admin/Games/mcp-lab/pcl3/npm-global/bin:$PATH
GV=/Users/admin/Games/mcp-lab/pcl3/bin/gltf_validator/gltf_validator
FB=/Users/admin/Games/mcp-lab/pcl3/bin/FBX2glTF-macos-x86_64/FBX2glTF-macos-x86_64

blender --version
blender -b -P /Users/admin/Games/mcp-lab/pcl3/scratch/blender_probe.py
gltf-transform inspect  <file.glb>
gltfpack -i <in.glb> -o <out.glb>
"$GV" -a -p -r -o <file.glb>          # -o = report to STDOUT (NOT an output dir);
                                       # without it the report is written NEXT TO the asset
"$FB" -b -i <in.fbx> -o <out-basename>
```

`gltf_validator -o` means *print JSON to stdout*, not *output directory*. Omitting it writes
`<asset>.report.json` **beside the input** — which for our corpus would mean writing into
`pct3/proj/emitted/`. Every validation in this note used `-o` with redirection into scratch precisely
to avoid that. **Whoever runs this next: do not drop the `-o`.**

---

## §9 — Per-row verdict recommendations (for the follow-up legolas cell to adopt)

All six rows currently read `EXCLUDED(no-positive-control …)`. Each now has a measured verdict.

| # | Row | Current menu verdict | **Recommended verdict** | Evidence |
|---|---|---|---|---|
| 18 | fix_synty_anim_to_godot_with_autorigpro | `EXCLUDED(no-positive-control on the Blender-extension instrument)` | **`LOADS-CLEAN` · `REACHES-NOT(arp-operator-absent)`** | §7 — installs + enables + registers on Blender 5.2; `bpy.ops.arp.build_bones_list()` → `AttributeError: … could not be found`; Auto-Rig Pro is paid and absent |
| 41 | Blender 5.2.0 (headless) | `EXCLUDED(no-positive-control on the CLI-invocation instrument)` | **`LOADS-CLEAN` · `REACHES(headless glb import)`** | §2 — cask served the pinned 5.2.0; `-b -P` imported `lib_a.glb`, reported 3 objects / 1 armature / 88 bones |
| 42 | FBX2glTF (godotengine fork) | `EXCLUDED(no-positive-control on the binary-execution instrument)` | **`LOADS-DIRTY(rosetta)` · `REACHES(Synty FBX → .glb)`** | §6 — `lipo -info` confirms x86_64-only across **both** forks; Rosetta present; converted `SK_Chr_Werewolf_01.fbx` in 0.126 s |
| 43 | glTF-Transform CLI | `EXCLUDED(no-positive-control on the npm-CLI instrument)` | **`LOADS-CLEAN` · `REACHES(inspect on lib_a.glb)`** | §3 — installed at the exact pin 4.4.2; full inspect report captured |
| 44 | glTF-Validator (Khronos) | `EXCLUDED(no-positive-control on the npm-CLI instrument)` | **`LOADS-DIRTY(rosetta)` · `REACHES(validate lib_a.glb)`** | §5 — **npm route is not a CLI** (`bin: null`); release binary is x86_64-only in all 8 releases; validated all 8 PC-T3 emits |
| 45 | gltfpack / meshoptimizer | `EXCLUDED(no-positive-control on the npm-CLI instrument)` | **`LOADS-CLEAN` · `REACHES(pack + re-validate)`** | §4 — no brew formula; npm pin 1.2.0 exact; 1,144,920 B → 231,776 B, output re-validates at 0 errors |

**Three menu corrections the follow-up cell should also carry (facts, not verdicts):**

1. **Row 44's install mechanism is wrong as stated.** The positive-control column reads *"npm CLI
   invocation."* The npm `gltf-validator` package has **no `bin` entry** — it is a JS library. Row 44
   is a **release-binary** row, not an npm row.
2. **Row 44's pin is unreachable as a binary.** Menu says `commit HEAD @ 2025-12-30`; the newest
   *published release* is `2.0.0-dev.3.10 @ 2024-10-22`. A HEAD pin implies a Dart source build.
   What is installed and probed is the release binary.
3. **Rows 42 and 44 are both x86_64-only.** The menu flags this for row 42 (★) but not for row 44.
   Row 44 deserves the same star.

---

## §10 — What this cell did NOT do

- Did **not** edit `legolas/notes/2026-07-26-plugin-provisioning-menu.md`. §9 is a recommendation.
- Did **not** build FBX2glTF or glTF-Validator from source (explicitly out of scope for this cell).
- Did **not** purchase or install Auto-Rig Pro.
- Did **not** configure Godot's `filesystem/import/blender/blender_path` — installing the cask does
  not set it, and PC-T12's error remains live until someone does.
- Did **not** `sudo npm i -g`; the confined prefix in §1.1 is a standing consequence.
- Did **not** delete legolas's four read-only clones in
  `agentic_orchestration/legolas/research/2026-07-26-plugin-audit-scratch/` (still there; still Matt's call).
- Did **not** modify any file in `pct3/proj/emitted/` or `reincarnated-godot/Assets/`.
- Made **no BETTER/WORSE claim** about any tool. Every transform difference in §4 and §6.1 is stated
  as a measured property of the transform.

**Signed:** drax, 2026-07-28. Six EXCLUDED rows now carry measured verdicts. The Layer-3 gap is closed.
