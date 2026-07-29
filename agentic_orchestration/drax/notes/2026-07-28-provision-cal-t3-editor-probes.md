# PROVISION-CAL · cell PC-T3 — Tier 3: EDITOR-ONLY plugins

**Run:** PROVISION-CAL (`2026-07-28-provision-cal-run-charter.md`) · **Conductor:** gandalf (RUN-CONDUCTOR)
**Cell:** PC-T3 · **Executor:** drax (presentation seam, `reincarnated-godot`) · **Date:** 2026-07-28

**Boundary observed:** LOADS?/REACHES?, never BETTER. Scope frozen to menu rows; discoveries are logged
findings (§F), never acted on.
**Law L-H (all-or-none):** every verdict below is **arm-agnostic**. Editor tooling is available to
W-MUR, W-PRO and H alike, or to none. No result here is any one arm's private capability.
**R-PC-5 network fence:** menu row 4 is installed and probed **outside** every other row's work, at the
end of the cell, in its own project, with the network activity named.

**Method notes carried in (my own PC-T12 standing notes + PC-W1-A instrument findings):**
- **F8** — `godot --headless --import` rewrites `project.godot` and prunes settings equal to engine
  defaults. `git diff project.godot` after **every** pass; restore by hand.
- **F9** — deleting `.md5` does NOT force reimport on 4.6.3; only deleting the dest artifact does.
- **G6 (standing)** — a scene can report `load: OK` while its script is **silently dropped** by a
  `class_name` collision. Scene-instantiation success is NOT evidence a GDScript row works. Assert
  script compilation directly, and run a `class_name`-collision check before trusting any script row.
- **PROCESS_MODE_ALWAYS propagation** — a test rig that sets `PROCESS_MODE_ALWAYS` propagates it into
  targets, so nothing actually pauses. Rigs in this cell do not set it.

**Stack:** Godot `4.6.3.stable.official.7d41c59c4`, Forward+/Metal, macOS arm64 (Apple M2).
**Projects:** `/Users/admin/Games/reincarnated-godot` (install + boot + presence) ·
`/Users/admin/Games/mcp-lab/pct3/` (checks 5 + 6 functional probes; a copy of my own L6-PREP lab so the
known-failing baseline is reproducible) · `/Users/admin/Games/mcp-lab/pct3_net/` (row 4, fenced).

**Write discipline:** written incrementally, one section per row, so a timeout loses at most one row.

---

## §0 — Verdict tally

**14 rows carry a verdict — every editor-only (`EW=WIRE`) row on the menu. Tier-3 coverage is complete.**
Both named §6 checks are answered with measurements. **All verdicts are arm-agnostic (L-H).**

| Verdict | N | Rows |
|---|---:|---|
| **LOADS-CLEAN** | **10** | 8 Shader Previewer · 9 Shader-Lib · 13 vkaParticleTool · 15 Advanced Model Import · 16 Animation Library Unique-ifier · 22 godot-synty-tools · 23 Import Replacer · 24 Mixamo Animation Batcher · 25 Modifier Animation Baker · 29 Unused Bone Track Remover |
| **LOADS-DIRTY** | **4** | 4 Godot Shaders Library `(network-by-design)` · 17 Anim Property Tracks Batch `(zh-CN-only UI)` · 26 Skeleton Poser 3D `(ships its own UID duplicate)` · 28 Unidot Importer `(deps-not-shipped-installed)` |
| **FAILS-LOAD** | **0** | — |
| **EXCLUDED(licence)** | 0 *new* | the editor-adjacent unlicensed rows (20, 27) were already excluded in PC-T12 |

**Reach verdicts, on the second axis:**

| Row | Reach |
|---|---|
| 24 Mixamo Animation Batcher | **`REACHES`** — check 5: the stock patch **fails**, the amended patch **passes** |
| 29 Unused Bone Track Remover | **`REACHES`** — 46 / 46 unmapped-bone tracks removed from a real Synty clip |
| 25 Modifier Animation Baker | **`REACHES`** *(with prerequisite)* — declines FBX-imported libraries by design |
| 22 godot-synty-tools | **`REACHES-NOT`** — check 6: the Base-Locomotion fixer does not resolve the inversion |
| 17 Anim Property Tracks Batch | **`REACHES-PARTIAL`** — per-animation yes; per-track reaches **0** tracks in our corpus |

### The two named checks, in one line each

- **CHECK 5 — does row 24's stock `.import` patch survive R4?** **NO.** Its shipped bone map matches
  **0 / 34** Synty bone names, so the retarget binds nothing and its own `remove_tracks/unmapped_bones`
  then deletes **every track** (91 → 0, 122 → 0). Amended, it passes. And **only the bone-map swap is
  load-bearing** — `fix_silhouette` is not required for the gate (§3.5).
- **CHECK 6 — does godot-synty-tools' Base-Locomotion fixer fix the 121-bone inversion?** **NO.** It
  runs clean in 0.4 s and emits its full library, and its output gates at **head y −1.615 … −1.319**
  against a **−1.628 … −1.315** baseline — a 0.013 m difference on a 1.6 m inversion. Measured on both
  the baseline character and the addon's own character convention.

### ★ The finding the conductor needs before Tier 4

**The 121-bone inversion is already solved, by a key row 24 was carrying all along.** Adding
`"retarget/remove_tracks/unmapped_bones": true` to the exact `.import` block that produced the charter's
−1.628 baseline flips it to **+1.612 … 1.649, upright** (§3.6). Neither my R4 recipe nor row 22 sets it.
And the inversion turns out to live in the **glTF round-trip**, not the Godot import (§4bis) — which is
where the L6 pipeline's front door is.

---

## §1 — Pre-flight: version re-read (L-C) + `class_name`-collision check

### 1.1 — L-C re-read, 2026-07-28: **one row has drifted, and it is row 4**

Every Asset-Library `download_commit` re-read from `godotengine.org/asset-library/api/asset/<id>` today.
**10 of 11 match the menu's 2026-07-26 read character-for-character.** The eleventh:

| # | Row | menu pin (2026-07-26) | AL serves 2026-07-28 | drift |
|---|---|---|---|---|
| 4 | Godot Shaders Library (Kelpekk, AL 4890) | **`v1.5` (rel 2026-07-20)** | **`1.4`**, commit `94cecbbf1e6b793241c1262c708d41117deef982` | **YES — the Asset Library is two releases behind the repo.** The menu pinned the GitHub release; the AL entry has not been updated to it |

The other ten, all identical: 5079 `965fea4b…` · 4785 `137c897d…` · 4331 `ecb13e0f…` · 4338 `66c49eef…` ·
4719 `39d00449…` · 4263 `6677ca55…` · 4844 `358743c5…` · 5119 `aa1c5239…` · 4833 `ec60afda…` ·
2503 `c1c786f3…` · 2654 `7b4f638e…` · 2427 `bb5b72fe…`.
**godot-synty-tools** (row 22, no tags) — `HEAD` re-read today = `c664ba3b46a3cf0bc38fe2c470e4348661d152f2`
@ **2026-05-08T02:42:33Z**, matching the menu's "`HEAD` @ 2026-05-08". No drift.

Every row installed from **the menu's pin**, fetched as a GitHub archive of the pinned SHA — not from
`HEAD`, and not through the in-editor Asset Library dock (which for row 4 would have silently installed
the older 1.4).

### 1.2 — `class_name`-collision check (PC-T12 standing method note, run BEFORE any verdict)

Every global `class_name` declared by every candidate row, diffed against the 155 already registered in
`reincarnated-godot` (`scripts/ scenes/ addons/`). Evidence: `tmp/pct3/presence_boot.log`.

**Result: ZERO collisions.** No row's script is silently dropped. The G6 false-CLEAN hazard did not fire
in Tier 3 — but it was checked, not assumed, and §2 asserts script compilation directly anyway.

**One landgrab logged, not acted on (finding T3-F1).** `godot-synty-tools` (row 22) publishes four
extremely generic global class names into the project namespace:

```
class_name FileUtils        class_name PopupManager
class_name BaseMenu         class_name BoneMapUtils
```

Nothing in `reincarnated-godot` currently claims those names, so no collision *today*. `FileUtils` and
`PopupManager` are the exact shape of the row-7/row-10 `Point` collision PC-T12 measured (G3) — a
third-party addon claiming a name the project would naturally want.

Row 9 (`Shader-Lib`) declares **41** global classes, but all but one are `VisualShaderNode*`-prefixed
and namespaced by construction; the bare one is `ShaderLib`.

### 1.3 — Instrument defect caught and corrected before it contaminated anything

My first staging directory was `reincarnated-godot/tmp/pct3/dl/` — **inside the project**. Godot imported
the extracted archives as project content and the import pass produced **69 UID duplicates** (every asset
existing twice: once under `addons/`, once under `tmp/pct3/dl/`). That is my instrument's dirt, not any
row's. Staging was moved to `/Users/admin/Games/mcp-lab/pct3/dl/` (outside the project) and the pass
re-run: **UID duplicates fall to 6**, of which 4 are the pre-existing `PolygonDarkFantasy` pairs PC-W1-A
logged as F7 and 1 is row 2's own (PC-T12 G12). **The 6th is new and belongs to a Tier-3 row** — see §3
row 26.

Named because a cell that had not re-run the control would have attributed 63 of its own duplicates to
the rows under test.

### 1.4 — F8 fired, deterministically, again

`godot --headless --import` pruned `[rendering] mesh_lod/lod_change/threshold_pixels=1.0` from
`project.godot` on **every** pass in this cell, as in PC-T12. Restored by hand after each.
**F8 is confirmed across two cells and ~12 passes. It is not intermittent.**

---

## §2 — Install → editor boot → presence (12 EditorPlugin rows + 1 resource-only row)

**All verdicts in this section are arm-agnostic (L-H).** Nothing here is available to one arm and not
another: an enabled `EditorPlugin` is a property of `project.godot`, which every cell shares.

### 2.1 — The instrument

`--headless --editor --script <EditorScript>` **does not work** — Godot treats `--script` as a MainLoop
and an `EditorScript` is not one; the run exits after printing the version banner with no output
(`tmp/pct3/presence_boot.log` first attempt). So presence is measured by a **temporary probe
EditorPlugin** of my own, `addons/pct3_probe/`, enabled **last** in `[editor_plugins]` so every row under
test has already run its `_enter_tree()` before the dump. It is removed at cell exit (§5).

Three assertions per row, weakest to strongest:

1. **the plugin.cfg's script compiles and `new()` yields an `EditorPlugin`** — asserted directly, per the
   G6 standing note (never infer a GDScript row works from a load that returned OK);
2. `EditorInterface.is_plugin_enabled()` → `true`;
3. **the surface the row's `_enter_tree()` claims is present in the LIVE editor tree** — the probe walks
   the whole editor window collecting every `PopupMenu` item text (947 found) and every `TabContainer`
   tab title (70 found), then checks the row's own claimed string against them.

Assertion 3 is the one that matters. `add_tool_menu_item()` returning without error is L-B's "manifest";
finding the item *in the menu* is the wire.

### 2.2 — Results

| # | Row | compiles | enabled | live surface found | Verdict |
|---|---|:---:|:---:|---|---|
| 24 | Mixamo Animation Batcher | ✓ | ✓ | tool-menu item **`Mixamo Animation Batcher...`** | **LOADS-CLEAN** (probe → §3) |
| 22 | godot-synty-tools | ✓ | ✓ | tool-menu item **`Godot Synty Tools`** | **LOADS-CLEAN** (probe → §4) |
| 25 | Modifier Animation Baker | ✓ | ✓ | tool-menu item **`Modifier Animation Baker...`** | **LOADS-CLEAN** |
| 28 | Unidot Importer | ✓ | ✓ | **3/3** live tool-menu items | **LOADS-DIRTY(deps-not-shipped-installed)** — §2.4 |
| 15 | Advanced Model Import (4.6) | ✓ | ✓ | dock tab **`Advanced Model Import`** + control `BulkImporterDock` | **LOADS-CLEAN** |
| 17 | Anim Property Tracks Batch | ✓ | ✓ | dock tab **`动画属性轨道批量修改`** | **LOADS-DIRTY(zh-CN-only UI)** — §2.5 |
| 13 | vkaParticleTool | ✓ | ✓ | control **`ParticleControlPanel`** in `CONTAINER_INSPECTOR_BOTTOM` | **LOADS-CLEAN** |
| 8 | Shader Previewer | ✓ | ✓ | control **`ShaderPreviewer`** (4.6 `EditorDock` API) | **LOADS-CLEAN** |
| 26 | Skeleton Poser (3D) | ✓ | ✓ | controls `Pose Save Dialog`, `pose stack`, `Add/Remove Pose Button` | **LOADS-DIRTY(ships its own UID duplicate)** — §2.6 |
| 29 | Unused Bone Track Remover | ✓ | ✓ | `add_inspector_plugin` — no tree surface; functional smoke §5 | **LOADS-CLEAN** |
| 16 | Animation Library Unique-ifier | ✓ | ✓ | `add_inspector_plugin` — no tree surface | **LOADS-CLEAN** |
| 23 | Import Replacer | ✓ | ✓ | `add_scene_post_import_plugin` — no tree surface | **LOADS-CLEAN** |
| 9 | Shader-Lib | n/a | n/a | **5/5 sampled `VisualShaderNode*` classes registered** | **LOADS-CLEAN** — §2.3 |

**12 / 12 EditorPlugins compile, enable, and boot on 4.6.3.** Not one addon-load failure in the boot log
(`grep -i "Unable to load addon\|error in the code"` → zero hits). The only errors in the boot are the
two **already-verdicted `FAILS-LOAD` GDExtensions from PC-T12** (rows 12 and 14) plus a pre-existing
`VFXLoot` parse error in the gitignored Binbun staging tree — both confirmed present in PC-T12 and
PC-W1-A logs, i.e. **not caused by any Tier-3 row** (L-N: the instrument's baseline is on the record).

### 2.3 — Row 9 has no `EditorPlugin` at all, and the menu's "editor-only" is right for the wrong reason

`Shader-Lib` ships **no `plugin.cfg`**. It is not an addon that is enabled; it is 41 `class_name
VisualShaderNode*` scripts under `addons/ShaderLib_v2_2_4/`, which Godot registers as global classes and
surfaces in the visual-shader Add-Node dialog automatically. Consequences worth stating plainly:

- **it cannot be "enabled" or "disabled"** — it is present the moment the folder is in the project;
- **its `EW` is arguably ALL, not WIRE** — a hand-authored GDScript pass can `ShaderLib.new()` and
  instantiate any of the 41 nodes without an editor. The menu lists it `WIRE`. Under L-H this is moot
  (all-or-none), but the menu's classification is measurably narrow. Logged as **T3-F2**.

### 2.4 — Row 28 · Unidot Importer — loads on 4.6.3 despite self-declaring 4.0–4.2

The menu's 4.6-evidence field is **NEGATIVE** (README: *"Currently supports Godot Editor versions 4.0
through 4.2"*). Measured: **it compiles, enables and registers its tool-menu items on 4.6.3.** All three
of its live `add_tool_menu_item` calls land; the other two the source contains are **commented out
upstream** (`plugin.gd:107,110`), so 3/3 is full presence, not a partial.

**The dirt is what it does NOT ship installed.** The repo's `addons/` carries **three more addons** —
`vrm` (2.0.1), `Godot-MToon-Shader` (3.4.0) and a nested `skeleton_merge_tool` — that the menu row does
not mention. I installed **only** `addons/unidot_importer/` (the named row). It boots without them.
Separately, it requires **FBX2glTF (row 42, macOS x86_64-only)** configured in Editor Settings before it
can translate anything — that dependency is a menu fact, re-confirmed here, not a new finding.

Verdict `LOADS-DIRTY(deps-not-shipped-installed)`: the row loads; its advertised *function* needs two
uninstalled sibling addons and an x86_64-only external binary.

### 2.5 — Row 17 · Animation Property Tracks Batch Modification — **the UI is Chinese-only**

Loads and docks cleanly. Its dock tab title is `动画属性轨道批量修改`; its console output is
`面板已收起，资源已清理` / `动画属性轨道批量修改 插件已卸载`. Grep of the addon finds **no
English string table and zero `tr()` calls** — the strings are hardcoded zh-CN.

This is a *usability* fact with a *fairness* edge under L-H, so I state it and stop: the row is equally
available to all three arms, and it is equally Chinese-only for all three. It is not a capability
difference. Logged as **T3-F3** — sibling of PC-T12's **G5** (the menu carries no *language* column,
neither programming-language nor human-language).

### 2.6 — Row 26 · Skeleton Poser (3D) — one defect, and one near-miss I nearly recorded as a defect

**The near-miss, recorded rather than smoothed.** My first read of the source found:

```gdscript
add_autoload_singleton("SkeletonManagerGlobal", "res://addons/skeleton_manager_plugin/skeleton_poser.gd", )
```

— a path (`skeleton_manager_plugin`) that does not exist in the shipped archive (the folder is
`skeleton_poser_plugin`). I had written it up as a shipped broken-autoload defect. **It is commented
out** (`skeleton_poser_plugin.gd:17`, inside an empty `_enable_plugin()`); it is Godot's own plugin
template boilerplate, left in with a stale path. **Not a defect. No verdict rests on it.** Recorded
because a grep for `add_autoload_singleton` matches commented lines, and that is a way to manufacture a
finding out of dead code.

**The actual defect:** it ships a UID duplicate inside its own example scene —
   `example_scene/pose_collection_snapshot.tres` vs `example_scene/lizbot_poses_from_rest.tres`. This is
   the 6th duplicate in §1.3 and it will warn on every project import from now on, joining row 2's
   (G12) and the four pre-existing pack duplicates (F7).

Also the only **LGPLv2** row on the menu — fine for an editor tool that never links into shipped code,
and named here so nobody has to re-derive it.


---

## §3 — Row 24 · Mixamo Animation Batcher — **§6 CHECK 5, the named probe**

> **Check 5 asks:** *"Does row 24's `.import` patch survive when `rest_fixer/fix_silhouette` is added and
> the bone map swapped to `sidekick_bone_map.tres`? The addon omits the key drax's R4 calls mandatory."*

### 3.1 — ANSWER

**The stock patch does NOT survive. It needs the amendment, and it needs it far more badly than the menu
predicted.** The menu called the omission of `fix_silhouette` the gap that would produce *"a
technically-retargeted, silhouette-wrong result."* The measurement says something worse and something
better, both:

- **Worse:** the stock patch does not produce a technically-retargeted result at all. It produces
  **animation clips with zero tracks** — the retarget binds nothing, and the addon's own
  `remove_tracks/unmapped_bones = true` then deletes every track in the clip. `swing` goes 91 tracks → 0.
  `walk` goes 122 → 0. The clips still import, still carry the right name and the right length
  (2.0333 s / 1.0333 s), and animate nothing. The pose gate cannot even be run against it, because the
  humanoid bone namespace never comes into existence.
- **Better:** of the two amendments, **only the bone-map swap is load-bearing.** `fix_silhouette` is not
  required for the gate to pass. It is not inert either — §3.5.

### 3.2 — Why the stock patch produces nothing: a bone-map census

The addon's shipped `sample_bone_map.tres` measured against the **raw, un-retargeted** 121-bone Synty
rig (`assets/anim_raw/`, `_subresources={}`):

| bone map | mapped names | **exact matches in the Synty rig** | case-insensitive matches |
|---|---:|---:|---:|
| addon `sample_bone_map.tres` | 34 | **0 / 34  (0.0%)** | 14 / 34 (41.2%) |
| ours `sidekick_bone_map.tres` | 54 | **54 / 54 (100.0%)** | 54 / 54 (100%) |

The addon maps `Root`, `Hips`, `Spine_01`, `Neck`, `Head`, `Shoulder_L`, `Elbow_L`, `Thumb_01_L` … —
Mixamo capitalisation. The Synty rig is UE-cased: `root`, `pelvis`, `spine_01`, `neck_01`, `head`,
`clavicle_l`, `lowerarm_l`, `thumb_01_l`. **Godot's bone lookup is case-sensitive**, so even the 14 that
differ only in case bind nothing. Evidence: `logs/census.log`.

*(A first census run gave 14.7% and was wrong — it loaded a scene that had already been imported through
`sidekick_bone_map`, so it was measuring the renamed rig against itself. Recorded rather than silently
replaced; the corrected census is the one above and it is the only one any verdict rests on.)*

### 3.3 — The instrument, validated against the charter's own baseline BEFORE any patch was measured (L-N)

The charter names a baseline: `walk` (`A_MOD_BL_Walk_F_Masc`) at **head y −1.628 … −1.315**. That number
was produced by TCP-L6-PREP's `pose_gate.gd` reading an **emitted `.glb`** (character + clip library),
not the imported scene. So the cell rebuilt that exact path — `pct3_emit.gd` (lineage:
`l6prep/tools/emit_final.gd::_library()`) → `verify_clean/pose_gate.gd` (my own gate, unmodified except
for the glb path) — and ran it on the untouched L6-PREP `.import` config first:

```
clip                  head y         hips y    R-hand travel    upright
swing          0.904..1.254   0.513..0.775          1.5212 m       true
walk          -1.628..-1.315 -0.988..-0.792         0.7702 m      false
```

**Character-for-character identical to the 2026-07-25 record.** The instrument is proven able to see the
failure before it is used to record any success.

**Instrument finding T3-F4, named not hidden.** A gate run on the **imported scene** instead of the glb
gives *different numbers for the same `.import` config* — control config, scene-side: `swing`
1.290…1.544 / `walk` **1.525…1.559 upright=true**. The scene-side walk **passes** where the glb-side walk
inverts. So on the control config **the inversion is introduced by the glTF round-trip, not by Godot's
import retarget.** Both readings are true of their own artifact. Every number in §3–§4 is reported on
**both** instruments, and the glb one is the instrument of record because it is the one the charter's
baseline is defined on.

### 3.4 — Five configurations, one variable at a time

The addon's own `_apply_import_settings()` was **called, not re-implemented** — `batcher.tscn` is
instantiated and the shipped method invoked on the real `.import` files. Every config starts from
`_subresources={}` (virgin), and every reimport deletes the dest `.scn` first (**F9**).

| cfg | bone map | `fix_silhouette` | `remove_tracks/unmapped_bones` | skeleton name | swing tracks | walk tracks | **walk head y (glb)** | upright | GATE |
|---|---|:---:|:---:|---|---:|---:|---|:---:|---|
| **control** — my R4 settings, the charter's baseline | sidekick | ✓ | **✗** | GeneralSkeleton | 91 | 122 | **−1.628 … −1.315** | **NO** | **FAIL** |
| **a — STOCK, as shipped** | addon (Mixamo) | ✗ | ✓ | Skeleton | **0** | **0** | *gate cannot run — no `Head`/`Hips` bone* | — | **FAIL** |
| **b — stock + BOTH amendments** | sidekick | ✓ | ✓ | Skeleton | 52 | 42 | 1.612 … 1.649 | yes | **PASS** |
| **b1 — stock + map swap ONLY** | sidekick | **✗** | ✓ | Skeleton | 56 | 25 | 1.617 … 1.654 | yes | **PASS** |
| **c — my R4 control + `remove_tracks` ONLY** | sidekick | ✓ | **✓** | GeneralSkeleton | 52 | 42 | 1.612 … 1.649 | yes | **PASS** |

Config **a**'s character imports with its raw Synty bone names intact — `root`, `pelvis`,
`hipAttachFront`, `thigh_l`, … — i.e. `rename_bones=true` renamed nothing, because the map matched
nothing. `Skeleton3D.find_bone("Head")` → **−1**.

Evidence: `/Users/admin/Games/mcp-lab/pct3/proj/logs/{patch,import,gatescene,emit,gateglb}_<cfg>.log`,
`out/gate_<cfg>.json`, `emitted/lib_<cfg>.glb`.

### 3.5 — What each amendment actually buys, measured separately

- **Amendment 1 — the bone-map swap — is necessary and sufficient for the gate.** Config **b1** carries
  it *without* `fix_silhouette` and passes on both instruments.
- **Amendment 2 — `fix_silhouette` — is NOT required for the gate, and is not inert.** Holding
  everything else fixed (b vs b1) it changes the surviving track counts (swing 52 vs 56, walk 42 vs 25)
  and it **recovers motion amplitude**: R-hand travel `swing` **1.549 m with** vs 1.396 m without;
  `walk` **0.408 m with** vs 0.245 m without. The gate is a *shape* test, not an *amplitude* test, and
  amendment 2 is an amplitude effect. My R4 statement — *"`fix_silhouette` is not optional"* — is
  **narrowed by this measurement**: it is not optional for faithful motion; it is not what keeps the
  character upright. I am correcting my own prior claim rather than defending it.

### 3.6 — ★ The finding that outruns check 5: what actually dissolves the 121-bone inversion

Config **c** is my own R4 control configuration — the exact `.import` block that produced the charter's
**−1.628** — plus **one** added key:

```
"retarget/remove_tracks/unmapped_bones": true
```

That one key is **the addon's**, and it is the one setting in row 24's patch that my R4 config never
carried. With it, the same clip on the same character through the same bone map with the same
`fix_silhouette` goes from **head y −1.628 … −1.315, upright=false** to **head y 1.612 … 1.649,
upright=true**, and `walk` drops from 122 tracks to 42.

**The 121-bone inversion is caused by the 80 unmapped leftover tracks landing on the target's bones, and
it is dissolved by a single `.import` boolean.** L6-PREP named the cause correctly (*"21 `ik_*` /
`*Proc_*` / `upperarm_proportion_*` tracks the 88-bone target cannot host"*) and did not have the fix.
Row 24 had the fix all along, buried under a bone map that made it unreachable.

**Consequence for check 6, stated before check 6 runs:** the charter frames the 121-bone inversion as
`godot-synty-tools`'s exclusive problem to solve. It is not exclusive any more. §4 measures whether
row 22 also solves it, and the pass/fail there is now a comparison against a *solved* baseline, not an
unsolved one.

### 3.7 — Two further defects in row 24, both from the menu's own gap list, both confirmed

- **`save_to_file` is keyed to `"mixamo_com"`, hardcoded** (`batcher.gd:216`). Synty clips are keyed by
  filename. The addon wrote `_subresources.animations["mixamo_com"].save_to_file.enabled = true` into all
  three files; **no `.res` was ever produced**, in any config, because no animation with that key exists.
  It fails silently — no error, no warning. Menu gap #2 confirmed exactly as written.
- **It writes the `save_to_file` block into the CHARACTER's `.import` too** if you point it at a folder
  containing one. My run passed the character deliberately (both sides must go through the same map,
  R4), and the addon happily wrote an animation-export block into a mesh file.

### 3.8 — Row 24 verdict

**`LOADS-CLEAN` · `REACHES(check-5: stock patch FAILS the pose gate; amended patch PASSES)`**

Loads clean, docks clean, and its patch mechanism is real and correct — it writes exactly the
`_subresources` block the job needs, and one of its four keys turns out to be the missing piece of my own
R4 recipe. **As shipped, pointed at Synty content, it destroys the animation it is asked to retarget.**
The menu's own recommendation — *"provision as a reference implementation, not as a tool… its 60
load-bearing lines are worth more than its dock"* — is **confirmed by measurement**, and it is more
right than it knew: the 60 lines contain a key we did not have.

Arm-agnostic per **L-H**: the patch is a `ConfigFile` write on a `.import` file. Any arm — MCP wire or
hand-authored GDScript — can perform it. Nothing here is one arm's private capability.

---

## §4 — Row 22 · godot-synty-tools — **§6 CHECK 6, the named probe**

> **Check 6 asks:** *"Does `godot-synty-tools`'s Base-Locomotion fixer actually fix the 121-bone
> inversion? Run it on `A_MOD_BL_Walk_F_Masc`, then the pose gate — drax's failing row is head y
> −1.628 … −1.315, so the pass/fail is unambiguous."*

### 4.1 — ANSWER: **NO.** Measured twice, on both character conventions.

| clip | head y | hips y | R-hand travel | upright every frame | GATE |
|---|---|---|---:|:---:|---|
| `walkbase` — the untouched baseline, **in the same glb** (L-N control) | **−1.628 … −1.315** | −0.988 … −0.792 | 0.7702 m | **NO** | **FAIL** |
| `walksynty` — **the fixer's output**, baseline character | **−1.615 … −1.319** | −0.963 … −0.784 | 0.8091 m | **NO** | **FAIL** |
| `walksynty` — the fixer's output, character imported through **the addon's own** `base_locomotion_v3_sidekick.tres` + its own naming (its best shot) | **−1.609 … −1.308** | −0.963 … −0.784 | 0.8091 m | **NO** | **FAIL** |

The fixer's output is **inverted by the same amount as the input**. The delta between the failing
baseline and the "fixed" clip is **0.013 m at the head** — 0.8 % of a 1.6 m inversion. The pass/fail is
as unambiguous as the charter promised, and it lands on FAIL.

Evidence: `logs/check6_run.log` (the fixer run), `logs/emit_check6*.log`, `logs/gateglb_check6*.log`,
`emitted/lib_check6{,b,c}.glb`.

### 4.2 — The fixer ran, and it ran successfully. This is not a load failure.

`BaseLocomotionImportGenerator.process()` was called **unmodified**, from a real editor context, on the
real pack:

```
=== PC-T3 CHECK 6 :: godot-synty-tools Base-Locomotion fixer ===
Running base_locomotion processing with folder: res://pack_slice
Finished running base_locomotion processing with folder: res://pack_slice
process() -> 0  (OK)  in 0.4s
```

It produced its full advertised output tree — per-clip `.res` Animation resources plus the packed
`Sidekick_Masculine.tres` / `Polygon_Masculine.tres` AnimationLibraries:

```
godot-synty-tools-output/base_locomotion/Sidekick/Masculine/Locomotion/Walk/A_MOD_BL_Walk_F_Masc.res   100,843 bytes
godot-synty-tools-output/base_locomotion/Sidekick_Masculine.tres                                       196,397 bytes  (1 animation: "MOD_BL_Walk_F")
```

**The row LOADS and its pipeline REACHES its own output.** What it does not do is fix the inversion.

**Input provenance (so the result is not dismissible):** the clip fed to the fixer is
`md5 7b76af530ba42014c1e5d5ec48f8ed72`, **byte-identical** to the `A_MOD_BL_Walk_F_Masc.fbx` that
produced the charter's baseline. It was extracted fresh from Matt's corpus zip
(`synty-corpus/fbx/ANIMATION_-_Base_Locomotion__1406852.zip`, 721 FBX) into a **minimal slice** carrying
exactly the structure `process()` requires: `Polygon/` + `Sidekick/` trees, both `Additive/TPose/`
sources, the four `.controller` files its cleanup step deletes, and one Walk clip per side. The slice is
a subset, not a modification — no file in it differs from the pack.

### 4.3 — Instrument defect, recorded (attempt 1)

The first run **timed out** — `Reimport timeout after 240.1 seconds`, `process() -> 1 (Failed)`. I did
not record that as the row's verdict. My driver fired `process()` from `_enter_tree()`, which races the
editor's boot scan: the addon connects to `resources_reimported` and then calls `efs.scan()`, but the
boot scan was already mid-flight, so the signal for its interim T-Pose copies never arrived and it waited
out its own timeout. **That is the driver's defect, not the row's** — the addon is designed to be clicked
by a human after the editor has settled. The driver was changed to wait for `efs.is_scanning() == false`
plus a settle, and the same call then completed in **0.4 s**. Attempt 1 is kept at
`logs/check6_attempt1_driver-defect.log`. **L-N: the instrument was cleared before the NO was recorded.**

### 4.4 — Why it fails, from its own source, and what does work

The fixer's mechanism is genuinely different from row 24's and genuinely thoughtful. Per
`base_locomotion_import_generator.gd::generate_animation_fbx_import_file()`, it writes:

```gdscript
"rest_pose/load_pose": 2,
"rest_pose/external_animation_library": anim_library,   # built from the pack's own T-Pose clip
"rest_pose/selected_animation": "RESET",
"retarget/bone_map": bone_map,                          # base_locomotion_v3_sidekick.tres
"retarget/bone_renamer/unique_node/make_unique": false,
"retarget/bone_renamer/unique_node/skeleton_name": "Skeleton3D",
```

It re-bases the rest pose from the pack's own `A_MOD_BL_TPose_Neut.fbx`. **It never sets
`retarget/remove_tracks/unmapped_bones`**, and it never sets `rest_fixer/fix_silhouette`.

Its output carries the fingerprint: **139 tracks, 93 of which resolve to a bone on the target**. The
other **46 are leftover** — the track paths are a mixture of renamed humanoid names and untouched Synty
names in the same animation:

```
Skeleton3D:Hips            <- mapped, renamed
Skeleton3D:hipAttachFront  <- unmapped, left as-is
Skeleton3D:hipAttach_l
Skeleton3D:hipAttachBack
```

§3.6 established that **`retarget/remove_tracks/unmapped_bones = true`, set at import time, dissolves
this exact inversion** on this exact clip and character (−1.628 → +1.612, upright). Row 22 does not set
it. Row 24 does.

### 4.5 — A tempting shortcut that does NOT work, measured rather than assumed

If the 46 leftover tracks are the cause, removing them from the finished animation should fix it. **It
does not.** A third clip in the same glb — the fixer's own output with all 46 unmapped-bone tracks
stripped in memory (139 → 93) — gates at **head y −1.568 … −1.530, upright=false**. Still inverted.

**So the load-bearing thing is the import-time setting, not the track list.** `remove_tracks/unmapped_bones`
acts *before* the rest-fixer composes the retargeted rest; deleting the same tracks from the finished
Animation is a different operation with a different result. I record this because it is the obvious next
move and it is wrong, and someone would otherwise spend a cycle discovering that.

### 4.6 — Row 22 verdict

**`LOADS-CLEAN` · `REACHES-NOT(check-6: Base-Locomotion fixer does not resolve the 121-bone inversion; head y −1.615 … −1.319 vs a −1.628 … −1.315 baseline, on both character conventions)`**

The menu put this row on the list because it is *"the only tool found that names that specific pack."*
It does name it, its pipeline is real, it runs clean on 4.6.3 in 0.4 s, and it emits packed animation
libraries. **On the one measurement it was put on the menu to answer, it does not move the number.**

Arm-agnostic per **L-H**: the fixer is an editor-context `RefCounted` driven by an `EditorPlugin`; its
output is plain `.res`/`.tres` any arm can load. Its failure is equally everyone's.

### 4.7 — Secondary observations on row 22, logged not acted on

- Its `base_locomotion_v3_sidekick.tres` is a **correct** Synty→humanoid map (`Root→root`,
  `Hips→pelvis`, `Spine→spine_01`, `LeftLowerArm→lowerarm_l`, …) — i.e. equivalent in kind to our own
  `sidekick_bone_map.tres`. **The bone map is not the problem.** It also ships 15 further per-pack maps
  (casino, city, farm, horror_carnival, kaiju, mech, mech_pilot, prototype, scifi_city, street_racer,
  quaternius_ual, mixamo_standard, sidekick_starter, base_locomotion_v3, base_locomotion_v3_polygon).
  Those are a genuinely valuable resource independent of the fixer's verdict.
- `process()` **hard-fails if the four `.controller` files are absent** — its cleanup step calls
  `DirAccess.remove_absolute()` on each and returns on the first error. A user pointing it at a pack
  directory that has had the Unity controllers pruned gets `FAILED` at the very end, after all the work.
- It publishes `FileUtils`, `PopupManager`, `BaseMenu`, `BoneMapUtils` globally (T3-F1, §1.2).

---

## §4bis — Where the inversion actually lives (a precision on §3.6, from the two instruments)

The scene-side gate and the glb-side gate together locate the failure more exactly than either alone.
Same character, same clip, walk row only:

| config | scene-side (imported `.tscn`) | glb-side (emitted, the baseline instrument) |
|---|---|---|
| **control** (no `remove_tracks`) | head 1.525 … 1.559 · **upright** | head **−1.628 … −1.315** · **inverted** |
| **b / c** (with `remove_tracks`) | head 1.525 … 1.559 · upright | head **1.612 … 1.649** · **upright** |

**The imported scene is upright in both configs.** The inversion appears only after
`GLTFDocument.append_from_scene()` → `write_to_filesystem()` → re-import. So:

- the 121-bone inversion is a **glTF round-trip failure**, not a Godot-import failure;
- `retarget/remove_tracks/unmapped_bones = true` is what makes the round-trip survive;
- and that matters *specifically* because **the `.glb` is the L6 pipeline's front door** — TCP-L6-PREP
  established one `.glb` per character carrying the whole clip library as the corpus's shipping shape.
  A defect that only appears at the emit is a defect exactly where the pipeline lives.

This also explains §4.5: stripping the unresolvable tracks from the finished animation before export does
not help, because the surviving tracks were already composed against a rest the export cannot reproduce.
The setting has to be present **at import**, before the rest fixer runs.

**Boundary check:** this is a LOADS/REACHES observation about two rows' `.import` output under a fixed
instrument. It ranks nothing and recommends nothing. The pipeline decision is L6's.

---

## §5 — The §2.4 dossier trio: one-touch functional smokes on real Synty content

Each row's **own shipped code** was called — no re-implementation — against real Synty animation data:
the check-6 emitted library (an 88-bone Sidekick character) plus godot-synty-tools' fixer output
(139 tracks, **46 of which address bones absent from that rig**). That combination is not incidental; it
is exactly the situation the dossier says these three tools exist for.

Evidence: `/Users/admin/Games/mcp-lab/pct3/proj/logs/smoke3.log`.

### 5.1 — Row 29 · Unused Bone Track Remover — **REACHES**, cleanly and completely

```
clip 'row29_case': 139 tracks, 46 address a bone NOT on this rig
_can_handle(AnimationPlayer) -> true
Track Skeleton3D:elbowProc_r is removed
Track Skeleton3D:upperarm_proportion_r is removed
Track Skeleton3D:clavLiftProc_l is removed          … (46 lines)
Done! Removed tracks: 46
tracks 139 -> 93  (removed 46)
```

**46 of 46, exactly the right 46.** The removed set is precisely the `*Proc_*` /
`upperarm_proportion_*` family TCP-L6-PREP named as the 121-bone pack's un-hostable leftovers. The row
does what the dossier says it does, on our content, first try.

Verdict **`LOADS-CLEAN` · `REACHES(46/46 unmapped-bone tracks removed from a real Synty clip)`**.
Its AL entry declares Godot **4.0**; it runs on **4.6.3** with no deprecation warning.

**Scope note, not a defect:** it operates on an `AnimationPlayer` in an open scene via the inspector, one
animation at a time from a dropdown. It has no batch mode. And per §4bis, removing these tracks *after*
import is **not** equivalent to `retarget/remove_tracks/unmapped_bones` at import — this row cleans a
loaded animation; it does not change how the animation was composed.

### 5.2 — Row 25 · Modifier Animation Baker — **LOADS-CLEAN**, and it declines Synty content by design

Its machinery executes without error: `_make_dialog()` builds its `ConfirmationDialog`; `_bake_keys()`
runs. But the addon enforces two hard preconditions in `_on_target_selected()`, and against a real Synty
imported clip:

| precondition (the addon's own words) | measured |
|---|---|
| *"Target AnimationMixer must have RESET animation"* | **false** — Synty FBX imports produce one clip named after the file; `animation/import_rest_as_RESET` is `false` by default |
| *"Target AnimationMixer must have editable AnimationLibrary"* (`_is_resource_editable`: false if a sibling `.import` exists) | true only because my probe fed it a runtime-built library; **an FBX-imported library is `.import`-backed and this returns false** |

So on Synty content **as imported**, this row refuses to run — correctly, and with a clear message. It
is a tool for baking modifier-IK on an *authored* scene, and it becomes usable the moment a clip is
extracted to a `.res`/`.tres` (which both row 24's `save_to_file` and row 22's generator do). Not a
defect; a **prerequisite**, and one that is invisible from the menu row.

Verdict **`LOADS-CLEAN` · `REACHES(dialog + bake kernel execute; refuses FBX-imported libraries by design — needs an extracted .res first)`**.

### 5.3 — Row 17 · Animation Property Tracks Batch Modification — **LOADS-DIRTY(zh-CN-only UI)**, and its scope is narrower than the menu implies

```
动画属性轨道批量修改 插件已加载
_find_animation_players(<real Synty scene>) -> 1 AnimationPlayer(s)
get_total_track_count_for_animation('walksynty') -> 0
get_animation_loop_mode_name(0) -> '不启用循环'
```

It loads, docks, discovers real `AnimationPlayer`s, and every call executes without error. **Two facts
the menu row does not carry:**

1. **`get_total_track_count_for_animation` returns 0 for a 95-track animation.** Not a bug — the
   function counts `Animation.TYPE_VALUE` tracks only:
   ```gdscript
   if track_type == Animation.TYPE_VALUE:
       count += 1
   ```
   Synty clips are **100 % `TYPE_POSITION_3D` / `TYPE_ROTATION_3D`** (TCP-L6-PREP §1.2: *"no scale
   tracks anywhere"*, and no value tracks either). The menu says this row hits *"bulk loop/interp/
   update-mode edits across 3,386 clips."* Its **per-track** editing reaches **zero** tracks in our
   corpus. Its **per-animation** loop-mode editing does still apply.
2. **The UI is Chinese-only** (§2.5). It ships an `_on_language_selected(index)` handler whose entire
   body is `pass` — a language selector that was wired up and never implemented.

Verdict **`LOADS-CLEAN(mechanics)` → recorded as `LOADS-DIRTY(zh-CN-only UI)` · `REACHES-PARTIAL(per-animation loop mode yes; per-track property edits reach 0 tracks in the Synty corpus — the corpus has no TYPE_VALUE tracks)`**.

### 5.4 — Instrument defects in this section, both mine, both recorded

1. **The smokes could not run in `reincarnated-godot` at all.** Three attempts died with
   `WARNING: Canceling suspended execution of "_go" due to a script reload` — the editor reloads scripts
   when it hits the project's pre-existing `VFXLoot` parse error (gitignored Binbun staging tree), which
   kills any awaiting coroutine in an `EditorPlugin`. **Any future cell that awaits inside an
   EditorPlugin in that project will hit this.** New standing method note: do editor-coroutine work in a
   small clean project, not in `reincarnated-godot`.
2. **My first row-29 run reported "removed 0" and it was my rig, not the row.** The OptionButton
   selection matched the wrong animation name, so the addon dutifully cleaned a clip that had nothing to
   clean — and *printed its own honest `Info: No tracks to remove`* while my harness printed a
   misleading `removed 0`. Fixed; the corrected run is §5.1. A row was one line away from an unearned
   REACHES-NOT.

---

## §6 — Row 4 · Godot Shaders Library — **R-PC-5 NETWORK FENCE, discharged**

**Fence honoured, stated precisely.** This row was installed and probed **after** every other row's work
in this cell was complete, in **its own project** (`/Users/admin/Games/mcp-lab/pct3_net/`), which contains
nothing else. It never ran during any measurement in §2–§5, and no measurement in §2–§5 ran while it was
installed anywhere. PC-T12 carried the fence forward unspent; this cell spends it and returns it.

### 6.1 — Verdict

**`LOADS-DIRTY(network-by-design)`** — as R-PC-5 anticipated, and it otherwise loads clean:

```
plugin.gd compiles                                              = true
is_plugin_enabled('shader_library')                             = true
ProjectSettings.has_setting('shader_library/general/shaders_folder') = true
main-screen control 'ShaderLibrary' present                     = true
```

All four assertions pass on Godot 4.6.3. It registers a `ShaderApplier` custom node, an inspector
plugin, two project settings, and a full main-screen editor control.

### 6.2 — L-C: this row **has drifted**, and the Asset Library is the stale one

| source | version | commit |
|---|---|---|
| menu pin (2026-07-26) | **v1.5** (rel 2026-07-20) | — |
| **Asset Library, re-read 2026-07-28** | **1.4** | `94cecbbf1e6b793241c1262c708d41117deef982` |
| GitHub releases, 2026-07-28 | v1.5 (2026-07-20) · v1.4 (2026-06-13) · v1.3.4 | — |
| GitHub `main` HEAD, 2026-07-28 | — | `12c587f1…` @ **2026-07-29T00:41Z** (pushed today) |

**Installing this row through the in-editor Asset Library dock would silently have given us 1.4, one
release behind the menu's own pin.** I installed the **menu pin (v1.5)** from the GitHub release tag.
This is the only drift among the 12 rows re-read (§1.1), and it is a drift in the *registry*, not the
repo. It is also the single most actively-developed row on the menu — HEAD moved during this cell.

### 6.3 — The network surface is **three hosts, not one**, and one of them is not on-demand

The menu's telemetry field reads *"it fetches from the network on demand."* Measured from source:

| host | what for | trigger |
|---|---|---|
| `raw.githubusercontent.com/Kelpekk/Godot-Shader-Library/main/data/shaders.json` | the shader database | **on demand** — `cache_manager.fetch_from_github()` from a user action, behind a 24 h cache |
| `godotshaders.com` | preview images / video / shader pages | **on demand** — per card, when browsed |
| **`api.github.com/repos/Kelpekk/Godot-Shader-Library/releases/latest`** | **self-update check** | **AUTOMATIC** — `shader_browser.gd:795`, a 2-second timer armed when the plugin loads, no user action, subject only to a 24 h cache |

```gdscript
get_tree().create_timer(2.0).timeout.connect(func(): update_checker.check_for_updates())
```

**The third host is an unprompted phone-home at plugin load.** It is benign (a public GitHub releases
endpoint, no identity payload) and it is not what the menu's FLAG described. Named so the fence rests on
the actual behaviour rather than the description. → finding **T3-F5**.

### 6.4 — Measured: in a headless editor, it is quiescent

The row was held in a live `--headless --editor` session for **12 seconds wall-clock** — six times its
own 2 s auto-timer:

```
user cache dir exists: false
```

`user://shader_library_cache/` was **never created**, meaning neither `UpdateChecker._ready()` nor
`CacheManager._ready()` ran. Its browser is a *main-screen* control, and the main-screen `_ready` chain
does not execute in a headless editor. **So in the only context this program runs Godot in, row 4 makes
no network requests at all.** The `LOADS-DIRTY(network-by-design)` annotation stands on the code, not on
observed traffic — and the fence remains the right call for any interactive session.

### 6.5 — F8, confirmed a third time, in a virgin project

Row 4's `_enter_tree()` demonstrably registered `shader_library/general/shaders_folder`
(`ProjectSettings.has_setting` → `true`), yet **`grep shader_library project.godot` finds nothing**. The
setting equals its own registered default, so Godot pruned it on write — F8, in a project created five
minutes earlier with no history. **F8 is not a `reincarnated-godot` quirk; it is engine behaviour on any
project.** Any cell that verifies a setting by reading `project.godot` will get a false negative.

---

## §7 — Exactly what changed, and what was left behind

**No commit was made in `reincarnated-godot`.** `git status --porcelain` shows **zero tracked-file
modifications**; `git diff project.godot` is **empty**.

**Created (untracked addon trees, 13 new):**
`addons/mixamo_animation_batcher/` · `addons/godot-synty-tools/` · `addons/Unused Bone Track Remover/` ·
`addons/modifier_animation_baker/` · `addons/animation_property_tracks_batch_modification/` ·
`addons/advanced_model_import/` · `addons/import_replacer/` · `addons/unique_anim_lib/` ·
`addons/skeleton_poser_plugin/` · `addons/shader-previewer/` · `addons/ShaderLib_v2_2_4/` ·
`addons/vkaParticleTool/` · `addons/unidot_importer/`

**Created then REMOVED (my temporary instruments):**
`addons/pct3_probe/` (presence probe) · `addons/pct3_smoke/` (functional smokes). Both deleted at exit;
`ls addons/` confirms neither remains.

**Touched and restored:** `project.godot` — 13 plugin entries added to `[editor_plugins]` for the
measurement and reverted; **F8 fired on every headless pass** (~6), each time pruning
`[rendering] mesh_lod/lod_change/threshold_pixels=1.0`; restored every time. Final state **byte-identical
to `HEAD`**. Baseline kept at `tmp/pct3/project.godot.baseline`.

**Left DISABLED:** no third-party `EditorPlugin` is enabled in `project.godot` at exit. Every Tier-3 row
is **installed-but-inert**, exactly as PC-T12 left the Tier-1/2 rows. Deliberate — enabling plugins is
shared `project.godot` state and, under **L-H**, an enable-decision is the conductor's, not a probe's.

**Evidence roots (all outside the project, so nothing pollutes its import pass — §1.3):**
- `/Users/admin/Games/reincarnated-godot/tmp/pct3/` — `presence_boot.log`, `presence_probe.json`,
  `import_all2.log`, `import_final.log`, `smoke.log` (the failed in-project attempt),
  `project.godot.baseline`
- `/Users/admin/Games/mcp-lab/pct3/dl/` — the 13 pinned source archives + extracted trees
- `/Users/admin/Games/mcp-lab/pct3/proj/` — the check-5/6 probe project: `tools/pct3_*.gd`,
  `verify_clean/pose_gate.gd`, `run_cfg*.sh`, `logs/*.log` (incl.
  `check6_attempt1_driver-defect.log`), `out/gate_*.json`, `emitted/lib_*.glb`, `pack_slice/`,
  `godot-synty-tools-output/`
- `/Users/admin/Games/mcp-lab/pct3_net/` — row 4, fenced, with `boot*.log`

**Not touched:** `SK_Chr_Werewolf_Undead_01.fbx` (**R-PC-1** honoured). Any Murzak/Pro row (Tier 4,
`GATED-Q46`). `~/Games/mcp-lab/project/`, `harness/`, `evidence/` (the Murzak lab). No Synty source file
was modified anywhere — the check-6 `pack_slice/` is a byte-identical extraction from Matt's corpus zip.

---

## §8 — Findings logged for the conductor (NOT acted on)

| # | Finding | Evidence |
|---|---|---|
| **T3-F1** | **`godot-synty-tools` publishes four generic global `class_name`s** — `FileUtils`, `PopupManager`, `BaseMenu`, `BoneMapUtils`. No collision today; the same landgrab shape as PC-T12's G3 (`Point`). If any project code later wants `FileUtils`, row 22 wins the name. | §1.2 |
| **T3-F2** | **Row 9 is not an EditorPlugin at all** — no `plugin.cfg`; 41 `class_name VisualShaderNode*` scripts that register the moment the folder exists. It cannot be enabled or disabled, and a headless GDScript pass can instantiate its nodes, so its menu `EW=WIRE` is measurably narrow. | §2.3 |
| **T3-F3** | **Row 17's UI is Chinese-only**, with an `_on_language_selected()` whose body is `pass`. Sibling of PC-T12's G5: the menu has no *language* column, for either programming language or human language. | §2.5, §5.3 |
| **T3-F4** | **★ The 121-bone inversion is a glTF ROUND-TRIP failure, not an import failure.** The imported scene is upright in every config measured; the inversion appears only after `append_from_scene` → `write_to_filesystem` → re-import. Since the `.glb` is the L6 pipeline's front door (TCP-L6-PREP), the defect sits exactly where the pipeline lives. | §3.3, §4bis |
| **T3-F5** | **Row 4 phones home automatically.** Three network hosts, not the one the menu names, and `api.github.com/.../releases/latest` fires on a **2-second timer at plugin load with no user action** (`shader_browser.gd:795`). Benign payload; not "on demand". | §6.3 |
| **T3-F6** | **★ `retarget/remove_tracks/unmapped_bones` is the missing key in my own R4 recipe.** Adding that one boolean to the exact `.import` block that produced the charter's −1.628 baseline flips it to +1.612 upright. Row 24 ships it; row 22 does not; my R4 never had it. | §3.6 |
| **T3-F7** | **`fix_silhouette` is an amplitude effect, not a shape effect.** It is not required for the pose gate to pass; it changes surviving track counts and recovers R-hand travel (swing 1.549 m vs 1.396 m). My own R4 line *"`fix_silhouette` is not optional"* is narrowed by measurement. | §3.5 |
| **T3-F8** | **Coroutines in an `EditorPlugin` cannot survive `reincarnated-godot`.** Three runs died on `Canceling suspended execution of "_go" due to a script reload`, triggered by the project's pre-existing `VFXLoot` parse error in the gitignored Binbun staging tree. Any future editor-context cell must use a small clean project. | §5.4 |
| **T3-F9** | **F8 is engine behaviour, not a project quirk.** It fired in `pct3_net`, a project created minutes earlier with no history, pruning a setting a plugin had just registered. Verifying a setting by grepping `project.godot` yields false negatives. | §6.5 |
| **T3-F10** | **Row 26 ships a UID duplicate in its own example scene** (`pose_collection_snapshot.tres` vs `lizbot_poses_from_rest.tres`), joining row 2's (G12) and the four pre-existing pack duplicates (F7). Running count of permanent import-warning sources: **6**. | §2.6 |
| **T3-F11** | **Row 22 ships 16 Synty per-pack BoneMaps** (base_locomotion ×3, casino, city, farm, horror_carnival, kaiju, mech, mech_pilot, prototype, scifi_city, street_racer, quaternius_ual, mixamo_standard, sidekick_starter). Correct maps, independent of the fixer's REACHES-NOT verdict — arguably the row's real value. | §4.7 |
| **T3-F12** | **Row 25 cannot run on Synty content as imported.** It requires a `RESET` animation and a non-`.import`-backed AnimationLibrary; FBX-imported clips have neither. It becomes usable only after a clip is extracted to `.res`. A prerequisite invisible from the menu row. | §5.2 |
| **T3-F13** | **Row 17's per-track editing reaches 0 tracks in our corpus.** It counts `TYPE_VALUE` tracks only; Synty clips are 100 % `TYPE_POSITION_3D` / `TYPE_ROTATION_3D`. Its per-animation loop-mode editing does apply. The menu's *"bulk edits across 3,386 clips"* is half true. | §5.3 |
| **T3-F14** | **Row 22's `process()` hard-fails if the four Unity `.controller` files are absent** — its cleanup step returns on the first `DirAccess.remove_absolute()` error, after all the work is done. | §4.7 |
| **T3-F15** | **The Asset Library is a staler pin than the repo for row 4** (AL 1.4 vs release v1.5). Installing via the in-editor AL dock silently installs behind the menu's own pin. L-C should re-read **both** surfaces, not just one. | §6.2 |

---

## §9 — Cell exit

| brief item | status |
|---|---|
| Row 24 — install, editor boot, tool-menu presence | ✅ compiles · enabled · live item `Mixamo Animation Batcher...` found in the editor's own PopupMenu tree (§2.2) |
| Row 24 — **§6 check 5**, the named probe: patch one Synty clip **both ways**, run `pose_gate.gd` | ✅ **stock FAILS, amended PASSES.** Five configs, one variable at a time; the addon's own `_apply_import_settings()` **called, not re-implemented** (§3) |
| Row 22 — install, boot, presence | ✅ compiles · enabled · live item `Godot Synty Tools` (§2.2) |
| Row 22 — **§6 check 6**: Base-Locomotion fixer on `A_MOD_BL_Walk_F_Masc`, then pose gate | ✅ **REACHES-NOT.** `process()` returned OK in 0.4 s and emitted its libraries; the output gates at −1.615…−1.319 vs a −1.628…−1.315 baseline, on **two** character conventions (§4) |
| Row 4 — **R-PC-5 network fence**: install + probe OUTSIDE any timed measurement | ✅ own project, after all other work, nothing else installed. `LOADS-DIRTY(network-by-design)`; three hosts named, one of them an unprompted phone-home; **measured quiescent in headless** (§6) |
| Rows 29 / 25 / 17 — install, boot, presence, one-touch functional smoke on a real Synty clip | ✅ all three; each row's **own shipped code** called. 29 removed **46/46**; 25 executes and declines FBX-imported libraries by design; 17 executes and reaches 0 per-track edits in our corpus (§5) |
| Remaining licence-clean editor-only Layer-1 rows — presence + verdict | ✅ rows 8, 9, 13, 15, 16, 23, 26, 28 all verdicted (§2.2). **Every `EW=WIRE` row on the menu now carries a verdict** |
| Unlicensed rows — EXCLUDED(licence), never installed | ✅ none newly arose in Tier 3; rows 20 and 27 were already excluded in PC-T12 and were **not** downloaded or installed here |
| Method — F9 reimport (dest-`.scn` delete) | ✅ every reimport in §3–§4 (`run_cfg.sh`) |
| Method — watch for F8 after every headless pass, restore by hand | ✅ fired ~6× in `reincarnated-godot` and once in a **virgin** project; restored every time; final `git diff project.godot` empty (§1.4, §6.5, §7) |
| Method — `class_name`-collision check before trusting any script-bearing row | ✅ run before any verdict; **zero collisions**; one landgrab logged (§1.2) |
| Method — PROCESS_MODE_ALWAYS propagation | ✅ no rig in this cell sets it |
| **L-H** — verdicts arm-agnostic, never framed as one arm's private capability | ✅ stated per row; §2, §3.8, §4.6 |
| **L-N** — clear the instrument before recording a NO | ✅ the glb pose gate reproduced the charter's baseline **character-for-character** before any patch was measured (§3.3); check 6's first run was thrown out as **my** driver's defect and re-run (§4.3); the row-29 smoke's first "removed 0" was **my** rig and was re-run (§5.4) |
| Boundary — LOADS?/REACHES?, never BETTER | ✅ no row ranked, no row repaired, no recommendation offered. Where a row's menu classification is measurably wrong (9, 17) or its dossier gap is confirmed (24), the measurement is reported and the menu amendment is left to legolas's seam |
| OUTPUT — incremental write; committed in the collaboration repo; nothing committed in `reincarnated-godot` | ✅ created at cell start, appended per row; §7 lists every changed file |

**Three instrument defects were caught and corrected before they became verdicts** — a staging directory
inside the project (69 phantom UID duplicates), a driver that raced the editor's boot scan (a false
240 s timeout on row 22), and an OptionButton pointed at the wrong animation (a false `removed 0` on
row 29). Each is written up where it happened rather than smoothed out, because each one was one step
away from an unearned FAILS or REACHES-NOT.

---

**Signed:** drax (presentation seam), 2026-07-28.
Evidence roots: `/Users/admin/Games/reincarnated-godot/tmp/pct3/` ·
`/Users/admin/Games/mcp-lab/pct3/` · `/Users/admin/Games/mcp-lab/pct3_net/`
