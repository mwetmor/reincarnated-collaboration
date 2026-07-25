# TCP-L4b — W-PRO CELL (run report) — ⚠ **RECONSTRUCTION**

**Program:** Tool-Capability Program · lap **L4**, class **T2 EXPANSION** × mode **(i) held-constant spec**
**Charters:** `2026-07-24-tool-capability-program-charter.md` · `2026-07-25-tcp-l4-expansion-bakeoff-charter.md`
**Conductor:** gandalf (`RUN-CONDUCTOR`) · **Instrument:** W-PRO only (Godot MCP Pro 1.15.1)
**Status:** **CLOSED — PASS.** All six spec clauses PASS. P-1..P-6 each resolved to a recorded fact **or**
marked `UNRECOVERABLE`.

---

## ⚠ §0 — WHAT THIS DOCUMENT IS. READ THIS BEFORE ANY NUMBER IN IT.

**This is a RECONSTRUCTION from surviving artifacts, authored after the executing agent terminated.**

The L4b cell ran to completion and its agent session **died on the last step**. Its final logged line was
*"Now the report."* Everything upstream — the addon swap, the manifest enumeration, the scene read, three
author→look→fix cycles, all judgment, the diffs, the crops, the L-J restore, the blast-radius fingerprint
and the TCP-27 vacate — landed on disk. **Only the written report was missing.** This document is it,
written by **drax as a fresh reader of those artifacts**, per dispatch
`agentic_orchestration/dispatches/2026-07-25-drax-l4b-report-reconstruction.md`.

**No wire was touched, no addon was swapped, no Godot was opened, no instrument was re-run to produce this
document.** Every action taken was a read: file reads, `shasum`, `diff`, and arithmetic over banked JSON and
banked PNGs. Two derived images were computed for this report and are named as such in §12.

### The epistemic boundary, stated once, because the program's method rests on it

**A fresh reader of artifacts is a different object from the agent that ran them.** The executing agent
knew *why* it made each call; I know only *what* it called and *what came back*. Therefore:

| marking | meaning |
|---|---|
| a plain assertion | **sourced to a named file on disk**, and the file is cited inline |
| *quoted italic* | **the terminated agent's own words**, relayed by the conductor's dispatch §1 — a transcript fragment, **not** an artifact. Every one is checked against the artifacts below and the verdict of that check is stated |
| **`UNRECOVERABLE`** | the artifacts do not settle it. **Not inferred, not smoothed, not filled in.** Collected in one place at §15 |

**Nothing in this report is written in the first person of the run.** Where the L4a report says "I judged,"
this one says "the artifact records." Where L4a could say "I chose X because Y," this one can only say
"X was called; the reason is not banked." That distinction is the whole value of the stamp.

## §1 — Verdict, in one paragraph

**W-PRO added the dais to a scene it did not author, hit all six spec clauses on the reloaded file, and
damaged nothing — 59 changed pixels of 1,730,817 outside the addition, and not one pixel anywhere outside
the addition moved by more than a single least-significant bit.** It took **three author→look→fix cycles**
and **90 wire calls** across 10 call-plans, client-side **median 6.73 ms (n=90, no exclusions)**.
**P-2 REVERSES the conductor's pre-registered prediction** — the prediction was **W-PRO FAILS**; W-PRO
passes, and §5 says plainly why that is a *confirmation of TCP-24's corrected attribution* rather than a
surprise. **P-6's forecast fired, on Pro, exactly as written** — the four FBX props saved duplicated,
318 nodes instead of 314, four of them untextured, **every call returning `ok`** — and the thing that
caught it was **not** the rendered frame. The duplicate was pixel-for-pixel invisible (§6, proved with a
change mask). **A non-lossy route exists on Pro's wire and it is one call per prop** (§6). The lap's most
load-bearing product is **§4: L-J's exact failure mode, live** — the Pro addon banked at **44 files** on
install was **79 files** at restore, while `plugin.cfg` still read `version="1.15.1"`, and the 35-file
growth is now **fully attributed**. Second sharpest: the duplication's collision-rename produced node names
that are **other real modules in the same pack** (§7) — an artifact that reads as plausible and is wrong.
And the executing agent **found and fixed a defect in its own verifier mid-run** (§11), which is the reason
clause 5 is a real PASS and not a vacuous one.

## §2 — Rubric diff against intent (law L-I — say out loud what fell out)

This cell ran **one instrument on one frozen spec**. It says **nothing** about W-MUR or H (their cells are
separate), nothing about design quality (the spec is frozen), nothing about new-scene authoring, nothing
about UI or VFX. It answers **execution fidelity + non-destruction + iteration count, for Pro, on an
expansion task.**

Four things a reader could over-read, named before they are:

- **"Pro is safe on foreign scenes" is licensed only for this scene shape.** The substrate is *flat* by
  PREP's deliberate design — 296 plain `MeshInstance3D` with inline `ArrayMesh`, no instanced sub-scenes
  (`L4_KIT_CONSTANTS.md` §8). L2's damage mechanism needed instanced sub-scenes in the *pre-existing* tree
  to bite. **This cell did not present that condition to Pro.** P-2 passes on the scene it was given.
- **P-2's pass is not evidence that Pro's save path is clean.** It is evidence that Pro's save path did not
  disturb what it did not touch. Pro's save path **did** duplicate what it *did* touch (§6). Those are
  different claims and the pixel diff only settles the first.
- **The wall-clock comparison against L4a is not instrument-vs-instrument.** L4a reports a *server-side*
  median from a Murzak relay log; L4b has no server log at all (§9) and reports a *client-side* median.
  Different measurement points. Reading 6.73 against 6.93 as a ranking is not supported.
- **This report's confidence is bounded by §0.** Where L4a's author could vouch for intent, this report can
  only vouch for artifacts. The `UNRECOVERABLE` register at §15 is not boilerplate; it is the list of things
  a first-person run log would have quietly asserted.

## §3 — Spec conformance checklist — six clauses, each with its measurement

Measured off the **saved file, reloaded from disk**, by an independent probe
(`prep/l4b_residue/l4b_verify.gd`). Raw: `evidence/l4/l4b/logs/VERIFY_final.txt`.

| # | Clause | Measured | Verdict |
|---|---|---|---|
| **1** | Platform 6.0 × 4.0 × 0.6, centred X=0, back edge flush to far wall inner face | world `x[-3.0000, 3.0000] y[0.0000, 0.6000] z[-8.7500, -4.7500]`; size `6.0000 × 0.6000 × 4.0000`; X centre `0.0000`; **back edge z = −8.75000**, and the same verifier run measured `Wall_0_0_inner` at `z[-8.97500, -8.75000] → INNER FACE Z = -8.75000` in the same pass | **PASS** |
| **2** | Two flights, 4 steps, 0.15 rise × 0.40 run, 1.2 wide, ascending −Z | all 8 steps width `1.2000`, run `0.4000`; tops `0.1500 / 0.3000 / 0.4500 / 0.6000`; −X flight `x[-4.2000, -3.0000]`, +X flight `x[3.0000, 4.2000]`; z runs `-3.15 → -4.75`; top tread top face flush with the dais top at `0.6000` and its far edge flush with the dais front edge at `z = -4.75` | **PASS as the clause is written** — see the spec note below |
| **3** | Two pack pillars **on** the dais, front (+Z) corners, inset 0.5 m from each edge | `SM_Bld_Base_Pillar_01` ×2; centres `(±2.5000, ·, -5.2500)`; **inset measured to centre = 0.5000 from the +Z edge and 0.5000 from the X edge**; world footprint `0.6710 × 0.6710` spanning `x[2.1645, 2.8355]` and `z[-5.5855, -4.9145]` — **entirely within the platform**; height `3.0659`, base y `0.5958` against a dais top of `0.6000` = **4.2 mm seated into the slab** | **PASS** — with one number declared below |
| **4** | `SM_Prop_Brazier_04` ×2 at the dais front edge, symmetric about X=0, **measured texture presence per TCP-16 as amended by TCP-25** | `SM_Prop_Brazier_04` ×2; centres `(±1.5000, ·, -5.1000)`, **symmetric about X = 0 exactly**; **base y = 0.6000 exactly** (base-centred origin, as the constants file promised); size `0.6864 × 1.2404 × 0.6864` = native (`0.686378, 1.240413, 0.686378`) to 4 dp. **Texture:** the reload census reads the actual material off each surface and prints `StandardMaterial3D[PolygonDarkFortress_Texture_01_A.png]`, with `untextured MI : 0` across the whole 314-node scene (`logs/P6_count_cycle2.txt`, `logs/P6_dais_cycle1.txt`) | **PASS — with a declared evidentiary gap.** See below |
| **5** | **NON-DESTRUCTION** — nothing moved, deleted, renamed or re-parented | **Structural:** `before nodes: 296 after nodes: 314 (added 18)`; `checked: 296 missing/renamed/reparented: 0 moved: 0 retyped: 0 mesh-changed: 0 material-changed: 0`. **Pixel (P-2, decisive):** see §5 | **PASS** |
| **6** | Camera — `__box`, parameters verbatim from the constants file | every shoot log prints `eye=(23.123901, 39.502224, 21.687008)`, `basis_x=(0.681998, 0.000000, -0.731354)`, `fov=20.000000`, `near/far 0.02/2000` — identical to `L4_KIT_CONSTANTS.md` §7 and to L4a. **Independently proven non-perturbing:** `scene_before` re-rendered **with the Pro addon installed and live** is **byte-identical** to prep's reference — `CTRL_SCENE_BEFORE__box_underPro.png` sha `248b6b94…` = `evidence/l4/frames/SCENE_BEFORE__box.png` sha `248b6b94…` (verified by `shasum` for this report) | **PASS** |

**Clause 4's declared evidentiary gap, stated rather than papered over.** TCP-25 requires discrimination on
the **rendered MEAN** (≈206 untextured vs ≈82 atlas-mapped), because variance passes an untextured prop.
**L4b banks no region-mean sampler and no rendered-mean figures.** What it banks instead is one level *up*
from the render and one level *down* from a return code: the reload census opens the saved material,
resolves `albedo_texture`, and prints the resolved texture's **filename**, per surface, for every added node
— which cannot pass on a null material, and reports `untextured MI : 0`. Combined with the frames
(`CROP_props.png` shows two charcoal atlas-mapped braziers where prep documented raw ones render as
near-white blobs, `L4_KIT_CONSTANTS.md` §4), the clause is settled. **But the specific TCP-25 statistic is
not on disk for this cell**, and a reader comparing cells clause-for-clause should know that L4a's clause 4
carries a stronger instrument than L4b's.

**Clause 3, the one number declared:** base y = `0.5958` against a dais top of `0.6000`. The pillar is
**seated 4.2 mm into the slab, not floating** — consequence of the pillar mesh's own AABB origin
(`−0.004134` y native, `L4_KIT_CONSTANTS.md` §2) carried through the instance. L4a reports the same figure
(`0.595866`) from a different route, so it is a property of the module, not of either instrument.

**Clause 3, one thing L4b did that L4a did not, declared so it is not read as conformance or as a defect:**
the added pillars carry `scale = (1.56392431259155, 1.01681637763977, 1.56392431259155)`
(`wire/c1a/0014_Dais_Pillar_L_scl.txt`). That is **not** a derived number — it is copied **verbatim** from
the room's own `Pillars/Pillar_0`, read off the wire at `wire/read4/0019_P0.txt`, which carries the
identical float triple. So L4b's dais pillars are **the same size as the room's existing pillars**
(`0.6710 × 3.0659`), while L4a's are at module native (`0.4291 × 3.0152`). **The clause specifies neither**,
both are conformant, and the difference is an operator ruling in each cell. Worth recording because a
four-cell contact sheet will show pillars of visibly different girth and that is not a defect in either.

**One more operator ruling the spec does not cover, declared so it is not read as conformance:** the dais
and step materials were given `uv1_triplanar = true` and `uv1_scale = (0.8, 0.8, 0.8)` — a 1.25 m texture
pitch, which is the room's own measured floor-tile pitch — plus `roughness 0.9` and `cull_mode DISABLED`
(`prep/l4b_residue/l4b_c2.json`, `l4b_c1b.json`). Without it the dais rendered as smooth pale concrete in a
stone room; the cycle-1 frame shows exactly that (§12). **This is the same class of ruling L4a made by a
different mechanism** (L4a used planar `uv1_scale (4.8, 3.2)` / `(0.96, 0.32)` to reach the same 1.25 m
pitch). It is equally available to every cell and should not count for or against any of them.

**The flanking stairs — NOT a Pro defect, and not re-investigated here.** Measured: both flights sit
**entirely outside the dais X-footprint** (`x[-4.2, -3.0]` and `x[3.0, 4.2]` against a dais `x[-3, 3]`) and
their run terminates at `z = -4.75`, the dais's front edge — so a climber arrives level with the dais top
but standing off the slab in X. **This is a defect in the charter clause as written, ruled by the conductor
in dispatch `2026-07-25-drax-l4b-report-reconstruction.md` §3.2, and both cells built it faithfully and
identically** (L4a records the same `x` spans and the same `z` run). Scored against the clause as written.
**PASS.** Not fixed, not marked against Pro.

## §4 — ★ THE HEADLINE: **L-J's exact failure mode, live — and the growth is now attributed**

**L-J says: restore by file inventory, never by a version string.** This cell is the law being vindicated
empirically, on the exact procedure it governs, in a single lap.

```
banked at install   evidence/l4/l4b/swap/PRO_INVENTORY.sha256      44 files
parked at restore   ~/Games/mcp-lab/_swap/pro_addon_godot_mcp_USED/   79 files
the version string  _swap/pro_addon_godot_mcp_USED/plugin.cfg      version="1.15.1"   ← unchanged, all along
```

**The directory grew by 35 files — 80 % — while the only field a `--install-addon` integrity check reads
stayed correct.** L-J's founding evidence was a *gutted* addon reporting healthy (3 `.gd` against an
expected 36). This is the **inverse case and it is arguably worse**: a **grown** addon reporting healthy.
A count-based check would have flagged it; a version check would not; and the failure L-J was written
against is a version check.

**The 35 files, pinned.** The dispatch asked that the growth be attributed or declared unattributed. It is
attributable, exactly, and I diffed the two trees file-by-file for this report:

| | |
|---|---|
| **ADDED** at restore, absent at install | **35 — every one a `.uid` sidecar**, one per `.gd`: `command_router.gd.uid`, `plugin.gd.uid`, `websocket_server.gd.uid`, `mcp_{game_inspector,input,screenshot}_service.gd.uid`, `ui/status_panel.gd.uid`, `utils/{node_utils,property_parser}.gd.uid`, and the 26 `commands/*_commands.gd.uid` |
| **REMOVED** | **0** |
| **CONTENT-CHANGED** | **0** — all 44 banked files byte-identical at restore |
| install composition | **35 `.gd`** + 7 `.md` + 1 `.tscn` + 1 `.cfg` = 44 |
| parked composition | 35 `.gd` + **35 `.uid`** + 7 `.md` + 1 `.tscn` + 1 `.cfg` = 79 |

**35 `.gd` in, 35 `.uid` out. The mapping is exact and one-to-one.** The mechanism is **Godot's own script-UID
sidecar generation on project scan** (Godot 4.4+), not anything Pro wrote. So the honest reading, and it is
sharper than "the version string lied by 35 files":

> **Pro's own files were not touched. Godot's scan accreted a sidecar per script into a third-party addon
> directory, and the addon's self-report could not see it.** A restore predicate that compares *counts*
> would raise a false alarm here; a predicate that compares the *version string* would miss a real
> gutting; **only a per-file content inventory distinguishes the two.** That is precisely what L-J
> prescribes, and this cell is the first time both failure directions have been observed on one procedure.

**Program consequence, offered to the ledger:** L-J's restore predicate should state that the incoming
inventory is compared **by content, per path**, and that **new engine-generated sidecars are an expected,
non-corrupting delta** — otherwise the next lap that swaps will HALT on a benign `.uid` bloom.

**And the restore itself checks out.** I verified it directly for this report rather than relaying it:

```
shasum -a 256 -c evidence/l4/l4b/swap/MUR_INVENTORY.sha256
  → 361 of 361 OK, 0 FAILED         (inventory is 361 lines; Murzak addon is 361 files)
project/addons/godot_mcp                      361 files  — Murzak 0.19.1, restored
project/project.godot            vs swap/project.godot.PRE-L4B            → byte-identical
project/.mcp.json                vs swap/mcp.json.PRE-L4B                 → byte-identical, port 27435
project/.godot/global_script_class_cache.cfg  vs …PRE-L4B                 → identical (`list=[]`, 8 bytes)
```

**Two honest qualifications on the restore.**

1. **L-J residue #1 (Pro rewrites `[autoload]`) is not observable as a residue here** — `project.godot` is
   byte-identical to the PRE-L4B bank, so either Pro did not rewrite it or the rewrite was fully restored.
   **Which of those two happened is `UNRECOVERABLE`** from the artifacts.
2. **L-J residue #2 (addon removal silently empties the class-name cache) is not observable here either** —
   the cache reads `list=[]` **both before and after**, because Murzak is a C# addon and registers no
   GDScript global classes. The prescribed rescan nevertheless ran and is banked
   (`logs/rescan.log`, 12:35:48, 61 KB): a full `first_scan_filesystem` → `update_scripts_classes` over
   161 steps, ending with `[Godot-MCP] plugin loaded`, `derivedPort=27435`, `connecting (mode=Custom,
   host=http://localhost:27435)`. **The rescan is evidenced; its effect on this project is nil, and that is
   a property of the incumbent addon, not of the procedure.**

## §5 — P-2, DECISIVE: non-destruction — **PASS, against a pre-registered prediction of FAIL**

Run with **prep's already-calibrated differ, unmodified** — `prep/l4_diff.py`, mtime `11:10`, i.e. untouched
since PREP wrote it and unchanged between the L4a and L4b runs.

**`evidence/l4/l4b/diff/L4B_WPRO_DIFF.json`:**

| | final | cycle 1 |
|---|---|---|
| pixels measured **outside** the addition | **1,730,817** | 1,730,817 |
| **changed pixels outside** | **59** — `0.0034 %` | **59** |
| **max channel delta outside** | **1** | **1** |
| mean abs diff outside | `1.156 × 10⁻⁵` | `1.156 × 10⁻⁵` |
| p99.9 channel delta outside | `0.0` | `0.0` |
| whole-frame changed px | 119,338 | 121,839 |
| inside the addition (sanity) | 119,279 changed, max delta **187**, mean 7.57 | 121,780, max 187, mean 7.41 |
| mask | `masked_in_px 342,783` (16.53 %), `dilate_px 24`, hexagonal hull, envelope `x[-5,5] y[-0.1,4.2] z[-8.85,-2.35]` | identical |

**All figures above are confirmed against the conductor's dispatch §2 table. Nothing contradicts it.**
The dispatch left the cycle-1 outside column blank; the artifacts fill it in, and it is **identical**: the
de-instancing and re-texturing of cycle 2 changed **nothing at all** outside the addition.

**Verdict: PASS.** Two independent statements support it, one mask-dependent and one not:

1. **Mask-dependent (prep's differ):** 59 pixels of 1,730,817, every one at channel delta 1, p99.9 = 0.
2. **Mask-INDEPENDENT, computed for this report from the two banked PNGs:** across the entire 1920×1080
   frame, **the number of pixels outside the addition region at channel delta ≥ 2 is zero.** That statement
   does not depend on how the mask is rasterized or dilated, and it is the strongest form of the claim.

**The boundary check, because prep's §6.4 says shadow spill is the differ's one lying direction and it lies
toward false conviction.** Re-rasterizing the banked hull and dilating it recovers a **subset** of 23 of the
59 (my polygon fill and 24-px dilation are approximations of the differ's — my mask covers 362,592 px
against the differ's 342,783, so my "outside" is smaller). Of those 23: **every one is at delta exactly 1**
(histogram `{1: 23}`), **20 lie within 20 px of the mask edge, 22 within 30 px, all 23 within 43 px**, and
they cluster in `x[862, 1428] y[443, 732]` — the floor immediately below and left of the dais, where its
cast shadow ends. **This is the same signature L4a published as the empirical passing floor** (30 LSB
pixels hugging the hull) and it is well inside it.

**The picture, and I looked at it:** `evidence/l4/l4b/diff/L4B_WPRO_DIFFx4_MASKED.png` — outside the orange
hull the frame is **pure black across its whole area**. The only signal is inside the hull and it is exactly
the addition's silhouette: the slab, both stair flights as stepped wedges at lower-left and lower-right,
both pillars as bright uprights, both braziers, and the cast shadow. Nothing else in the room registers at
×4 amplification.

### Why the reversal is a confirmation, not a bolt from the blue — and it must be said plainly

The pre-registered prediction was **W-PRO FAILS P-2**, on L2's mechanism: `add_scene_instance` calls
`set_owner_recursive`, so internal nodes save owned *and* re-instance on reload, colliding and renaming.
**That mechanism fired in this cell exactly as predicted** — §6 — and it produced **zero** damage outside
the addition, because **the mechanism was already re-attributed before this cell ran.** **TCP-24** found the
duplication reproduces from a plain headless GDScript builder with no MCP server running (808 nodes in,
1320 out) and named it a property of **Godot's `PackedScene.pack()` save path**, not of Pro. PREP then
flattened the confound out of the *substrate*, so the pre-existing 296 nodes carry no instance boundaries
for the mechanism to bite on.

**So P-2's reversal confirms the corrected attribution and does not reverse a belief about Pro.** The
prediction was authored against the pre-TCP-24 picture; TCP-24 superseded that picture; the measurement
agrees with TCP-24. **Do not oversell it.** The honest one-line statement is: *the L2 finding was about
instanced sub-scenes in the tree, PREP removed them from the substrate, and Pro therefore had nothing to
damage.* A foreign scene that **does** carry instanced sub-scenes is **still untested against Pro**, and
this cell does not license the general claim.

## §6 — P-6: **the forecast fired on Pro — and the rendered frame could not see it**

**The forecast (charter §3, P-6):** *"at least one instrument ships duplicated pillars and does not notice,
because every call returned `ok` — L-K, sixth instance."*

**It fired. On this instrument. In cycle 1.** `evidence/l4/l4b/logs/P6_count_cycle1.txt`, measured by
reloading the saved file from disk and counting what the engine actually builds:

```
NODES OUT              : 318          expected 314   (+4)
MeshInstance3D         : 305          expected 301   (+4)
surface overrides OUT  : 553          correct
untextured MI          : 4            ← the four re-instanced copies, no material
```

And the per-node dump, `logs/P6_dais_cycle1.txt`, shows what those four are — **two identically-named
children under each FBX prop root, one textured, one null**:

```
Dais/Dais_Pillar_L/SM_Bld_Base_Pillar_01   mesh=ArrayMesh surf=1 mats=["null"]                       worldY=[-0.00861..3.00654]
Dais/Dais_Pillar_L/SM_Bld_Base_Pillar_01   mesh=ArrayMesh surf=1 mats=["StandardMaterial3D[...A.png]"] worldY=[-0.00861..3.00654]
Dais/Dais_Brazier_L/SM_Prop_Brazier_04     mesh=ArrayMesh surf=1 mats=["null"]                       worldY=[0.00000..1.24041]
Dais/Dais_Brazier_L/SM_Prop_Brazier_04     mesh=ArrayMesh surf=1 mats=["StandardMaterial3D[...A.png]"] worldY=[0.00000..1.24041]
```

— and both copies at **identical world Y extents**. Same mesh, same place, one dressed and one not.
**All 37 cycle-1 wire calls returned `ok`** (`wire/c1a.summary.json` 22/22, `wire/c1b.summary.json` 15/15).

### ★ The finding that is bigger than the cell: **the frame could not catch this one**

L-K's law says a rendered frame diffed against a control is the only instrument that has ever caught one of
these. **Here it is the instrument that could not.** The duplicate is exactly co-located with the original,
so it is occluded by it at every camera.

**Proved, not asserted.** I computed the pixel change mask between the cycle-1 detail frame and the cycle-2
detail frame — cycle 2's only structural act was removing the four duplicates — and looked at it:
**the two pillar shafts and both braziers appear as unchanged black silhouettes.** Every changed pixel lies
on the platform surface, the step treads and risers, or the shadows those surfaces receive — i.e. **the
whole visible delta is the triplanar-UV ruling, and the removal of four duplicated meshes is worth zero
pixels.** The `__box` numbers agree independently: whole-frame changed pixels moved 121,839 → 119,338, and
the *outside* figure did not move at all (59 → 59, §5).

> **L-A is necessary and it is not sufficient.** A frame catches what changes the picture. **A silently
> duplicated, exactly-co-located node changes nothing in the picture and doubles the draw calls, the file,
> and every later reparent.** The instrument that caught it was a **reload-from-disk structural census**,
> and the rig's own header says why it must reload rather than read the `.tscn` text
> (`prep/l4b_residue/l4b_count.gd`: *"whether Godot double-creates it is an engine behaviour, not a text
> property"*). **Two instruments, two failure modes, and they do not share one.** Offered to the ledger as
> the sharpest qualification L-A has received.

**Attribution, carefully.** Per **TCP-21**, an L-K instance requires both that the tool reported success and
that the operation was correctly invoked. Both hold. But per **TCP-24** the duplication mechanism is
**Godot's `PackedScene.pack()`**, not Pro's — so **this is not filed as an L-K instance against Pro.**
What is attributable to Pro is the *pole it sits at* in TCP-24's trilemma:

| instrument | ownership choice | consequence at save | what it costs |
|---|---|---|---|
| **W-PRO** (`add_scene_instance`) | **own-all** — internal children saved owned | **duplicates on reload**, correct materials on one copy | node-count wrong; the wrong copy is invisible |
| **W-MUR** (`node-create`, L4a §10) | **own-root-only** | correct node count, **every material silently dropped** | white blobs — which the frame *did* catch |

**The two instruments occupy opposite poles of the same trilemma, and each needed a different workaround.**
That is a genuine comparative result and neither cell could have produced it alone.

### The non-lossy route on Pro's wire — one call per prop

**Found, and it is cheaper than L4a's.** `prep/l4b_residue/l4b_c2.json`:

```
update_property  node_path "Dais/Dais_Pillar_L"  property "scene_file_path"  value ""
```

Clearing `scene_file_path` on the instance root **de-instances it in place**: the root becomes a plain
`Node3D` holder, its FBX-internal `MeshInstance3D` becomes an ordinary owned child, nothing re-instances on
load, and the material survives. The probe response
(`wire/probe/0004_pillarL_after.txt`) shows the root afterwards as `"type": "Node3D"` with only Node3D
properties, retaining its position and scale. **Four calls, one per prop.**

**Measured, on the saved file, reloaded** (`logs/P6_count_cycle2.txt`, `logs/VERIFY_final.txt`):

```
scene_before.tscn        live nodes on load    296
scene_l4b_wpro.tscn      live nodes on load    314      (+18 = 14 authored + 4 de-instanced FBX children)
MeshInstance3D                                 301
surface overrides                              553      (substrate 540 + the addition's 13)
untextured MI                                  0
type census    MeshInstance3D 301 · Node3D 9 · DirectionalLight3D 2 · OmniLight3D 1 · WorldEnvironment 1
```

**No duplication. No material loss. Both poles of TCP-24's trilemma avoided, at 4 wire calls.** Compare
L4a's route: `node-set-parent` the internal mesh out with `keepGlobalTransform`, then `node-delete` the
emptied root, then assign the material null-first — three call shapes and a mandatory delete. **Pro's route
is the cheaper of the two and it preserves the holder node**, which is why L4b's tree is 314 nodes against
L4a's 310 for the same addition: L4b keeps four `Node3D` prop roots that L4a deletes.

**One declared caveat, and it is `UNRECOVERABLE` whether the executing agent tested it:** L4a explicitly
re-packed and re-loaded its output a second time (`310 → 310, pack err=0`). **L4b's artifacts show one
reload, not a repack round-trip.** The 314 figure is a load-from-disk count on a file Pro saved; it is not
a proof that re-saving *that* file from Godot is stable. No artifact settles it.

## §7 — ★ The collision-rename produced the name of a **different real module**

**This is the defect the executing agent called *"one real defect remains"* and spent cycle 3 on, and it is
worth more attention than a rename usually gets.**

When the cycle-1 duplicate landed, the editor's live tree resolved the name collision by incrementing the
trailing digit. The broken-verifier run at 12:29:34 and the fixed one at 12:30:43 both read the saved names
(`logs/VERIFY_cycle2.txt`, `logs/VERIFY_cycle2_fixed.txt`):

```
SM_Bld_Base_Pillar_02      ← the node is SM_Bld_Base_Pillar_01
SM_Prop_Brazier_05         ← the node is SM_Prop_Brazier_04
```

**Both of those are real, distinct, shipping modules in the same pack.** Verified on disk for this report:
`Generic/FBX/Base/SM_Bld_Base_Pillar_02.fbx` exists (as do `_03`, `_04`, `_05`), and
`DarkFortress/FBX/SM_Prop_Brazier_05.fbx` exists — prep even **measured** it as a declared substitute
(`0.914421, 1.144097, 0.953050`, **2 surfaces**, `L4_KIT_CONSTANTS.md` §6). So:

> **A `+1` collision-rename inside a Synty pack does not produce a garbage name. It produces the name of a
> neighbouring module.** An auditor reading `scene_l4b_wpro.tscn` at that point would have concluded the
> cell used `SM_Prop_Brazier_05` — **a clause-4 violation of the pinned prop** — and would have been wrong.
> The geometry was `Brazier_04` the whole time; only the label lied, and the label lied *plausibly*.

**This is L-K's shape one level out from the wire:** not a call that reports success while failing, but an
**artifact that reads as valid and is wrong**, produced by an engine convention colliding with an asset
naming convention. It survived a save. It would have survived any check that reads names rather than
meshes. **The thing that caught it was the AABB table** — the fixed verifier printed a node labelled
`SM_Prop_Brazier_05` with `size=(0.6864, 1.2404, 0.6864)`, which is `Brazier_04`'s native size and **not**
`Brazier_05`'s.

**Fixed in cycle 3**, four `rename_node` calls, each response naming the old value
(`wire/c3/0002_rn_pilL.txt` … `0005_rn_brzR.txt`), then `save_scene`. `logs/VERIFY_final.txt` reads
`SM_Bld_Base_Pillar_01` and `SM_Prop_Brazier_04`. The final frames are **byte-identical** to cycle 2's
(§12) — as they must be, since a rename moves no pixel.

## §8 — P-3, the route: **per-node, purpose-built creation calls — with one escape-hatch call, forced**

**The first prompt was banked verbatim before the addon was installed, before the editor was launched and
before `tools/list` was called** — `evidence/l4/l4b/P3_FIRST_PROMPT_BANKED.md`, mtime **12:14:36**, against
`PRO_INVENTORY.sha256` (the install bank) at **12:14:47** and the `tools/list` enumeration at **12:15:48**.
**The ordering is confirmed by file mtimes, not by assertion.**

**I read the banked prompt in full and checked it for a method noun, because the dispatch made that a HALT
condition. It carries none.** It names a project path, a source scene, an output scene, five geometric
clauses, two asset filenames (`SM_Bld_Base_Pillar_01`, `SM_Prop_Brazier_04` — required by clause 4's pinning)
and two file paths to read. It contains no "script", no "batch", no "node", no "gridmap", no "instance",
no "create", no "place", no "editor script", no "one at a time". **P-3 is NOT contaminated for this cell.
No HALT.**

**What the wire actually did — the complete tool census across all 90 calls** (computed from
`evidence/l4/l4b/wire/*.jsonl` for this report):

| tool | calls | where |
|---|---|---|
| `get_node_properties` | **30** | read3 ×6, read4 ×23, probe ×1 |
| `set_material_3d` | **13** | c1b — one per added surface |
| `update_property` | **12** | c1a ×6 (positions/scales), c2 ×4 (de-instance), probe ×2 |
| `add_mesh_instance` | **9** | c1a — platform + 8 steps, `BoxMesh` with explicit `size` |
| `open_scene` | 7 | once per plan |
| `add_scene_instance` | **4** | c1a — 2 pillars + 2 braziers |
| `get_scene_tree` | 4 | read1, read2, c1a, c3 |
| `rename_node` | **4** | c3 |
| `save_scene` | **3** | c1b, c2, c3 |
| `add_node` | **1** | c1a — the `Dais` holder |
| `execute_editor_script` | **1** | c2 — the escape hatch |
| `analyze_scene_complexity` | 1 | read2 |
| `get_scene_file_content` | 1 | read5 |

**P-3 resolves: W-PRO went NODE-BY-NODE, through purpose-built typed creation tools, one node per call.**
Fourteen nodes, fourteen creation calls (`add_node` ×1 + `add_mesh_instance` ×9 + `add_scene_instance` ×4).
**It did not batch and it did not gridmap, and both were available** — `batch_add_nodes` and `add_gridmap`
are both in the 175-tool live manifest (`wire/PRO_LIVE_TOOLNAMES.txt`, lines 22 and 6) and **neither was
called once**. The charter's named GridMap prediction is therefore **not tested by this cell**.

**The escape hatch was reached for exactly once, and it was forced — with a banked blocking artifact (L-G).**
The probe plan tried to set a sub-resource property through the property wire and got a **real, honest
error**:

```
update_property  node_path "Dais/Dais_Platform"  property "surface_material_override/0:uv1_scale"
  → Godot error (-32001): Property 'surface_material_override/0:uv1_scale' on MeshInstance3D not found
    Suggestion: Available: ["process_mode", …, "material_override", "material_overlay"]
```

(`wire/probe/0003_uv_subpath_probe.txt`, `wire/probe.err`.) **Pro's property wire addresses node properties,
not sub-resource property paths.** So the UV ruling went through `execute_editor_script` — nine nodes,
`m.uv1_triplanar = true; m.uv1_scale = Vector3(0.8, 0.8, 0.8)`, one call, with the per-node result echoed
back (`wire/c2/0006_uv_triplanar.txt`). **The escape hatch is 1 call of 90. The rest of the run is the
node family.**

**The structural parallel with L4a is exact and worth the ledger line.** In L4a the *read* was forced off
the node family onto a script because Murzak's wire cannot read a transform. In L4b the *write of one
property class* was forced onto a script because Pro's wire cannot address a sub-resource path. **Both
instruments handled the bulk of an expansion node-by-node and both needed the escape hatch for exactly one
thing their wire could not express.** Two instruments, same shape, different hole. That is a stronger
statement about the *category* than either cell alone.

### The counter-example to L-K, and it deserves naming

**In a program whose central law is "in this stack, failure returns SUCCESS," Pro's property wire returned
a real failure with a real diagnosis.** One call of 90 failed; it failed *loudly*; it named the rejected
property; and it **listed the twenty properties that would have worked**. That is the single cleanest
counter-example to L-K found anywhere in this program so far, and it is the reason the escape hatch was
reached for deliberately rather than after a silent no-op. **Program consequence:** L-K is a law about
this *stack*, not a law about every tool in it — and an instrument's verdict should record **which of its
surfaces fail honestly**, because those are the surfaces an agent can iterate against cheaply.

## §9 — P-4, wall-clock — **partially `UNRECOVERABLE`, and the recoverable part is stated with its statistic**

**Wire latency — client-side, from `evidence/l4/l4b/wire/*.jsonl`, recomputed for this report:**

```
tools/call   n=90   MEDIAN=6.73 ms   q1=5.64   q3=7.67   mean=13.03   min=2.03   max=312.36
             calls > 100 ms: 1  ->  312.36 ms, read1's `open_scene` (first, cold, 296-node scene)
             EXCLUSIONS: NONE APPLIED. Every call in every plan is in the set.
             total wire time across the whole cell: 1.173 s
tools/list   n=1    12 ms  ->  175 tools
```

**The mean (13.03 ms) is 1.9× the median and is carried by one call**, named above. TCP-19's rule, applied.
Per-plan medians (`wire/*.summary.json`) run 4.96–11.55 ms and agree.

**The comparator caveat, and it is not a quibble.** L4a reports **server-side handler time** parsed from a
Murzak relay log (`median 6.93 ms, n=119`). **L4b has no server-side log** — Pro's addon *is* the server, a
WebSocket listener inside the editor on ports 6505–6514, and it emits no per-handler timing. So L4b's
figure includes client transport and L4a's does not. **6.73 vs 6.93 is not a ranking.** The
client-side totals are comparable to each other: **W-PRO 1.173 s / 90 calls** against **W-MUR 1.943 s /
117 calls**.

**Elapsed wall-clock, from the cell's own timeline stamps and artifact mtimes:**

| span | source | wall-clock |
|---|---|---|
| `L4B_RUN_START` → `L4B_AUTHORING_END` | `evidence/l4/l4b_TIMELINE.txt`, `l4b/l4b_TIMELINE.txt` | **1,271 s (21 m 11 s)** |
| `L4B_RUN_START` → `L4B_RUN_END` | same | **1,510 s (25 m 10 s)** |
| first wire call → last authoring wire call | mtimes `read1.err` 12:16:16 → `c3.err` 12:31:33 | **917 s (15 m 17 s)** |
| …including the final renders and diff | → `L4B_WPRO_DIFF.json` 12:32:18 | **962 s (16 m 02 s)** |

**Instrument time inside that span — one line of it is measured and the rest is `UNRECOVERABLE`:**

| | |
|---|---|
| wire, 90 calls | **1.173 s** — measured |
| renders, 8 processes | **`UNRECOVERABLE` except one.** Only `logs/reverify_box.log` carries a `real 1.96 / user 0.88 / sys 0.25`. The other seven shoot logs record camera parameters and `err=0` but **no timing** |
| headless script runs (2 counts, 3 verifies) | **`UNRECOVERABLE`** — no durations banked |

**What can be said:** wire time is **1.173 s of a 962 s authoring-and-render span — 0.12 %.** L4a measured
1.3 % on the same task with a fuller decomposition. **Both cells say the same thing and it is the actual
P-4 finding: at T2 task size, wall-clock is dominated by operator decision time and is not an instrument
property.** P-5 is the axis that carries the information.

## §10 — P-1 — **YES**

**Does the dais geometry come out at all?** **Yes.** 14 authored nodes + 4 de-instanced FBX children = 18,
all six clauses measured on the reloaded file (§3), all placements correct to four decimal places on the
**first authoring pass** — every world AABB in `VERIFY_final.txt` matches the spec arithmetic exactly, and
no cycle was spent moving anything. Cycles 2 and 3 fixed a save-path duplication and a name; **zero cycles
were spent on geometry.**

## §11 — The executing agent found a defect in **its own verifier**, mid-run, and it invalidated clause 5

**This is banked in the rig's own source, so it is recoverable and it is not hearsay.**
`prep/l4b_residue/l4b_verify.gd` carries a defect note written at the point of fix:

> *"`Node3D.global_transform` returned IDENTITY for every node even after `add_child` inside a SceneTree
> `_init()` — the transform cache is not built at that point. It did not error. It returned a
> plausible-looking AABB centred on the origin, and the non-destruction comparison then compared identity
> to identity and reported PASS FOR EVERY NODE. A verifier that cannot fail is not a verifier (TCP-25's
> rule, applied to my own tool)."*

**The two artifacts show it, 69 seconds apart:**

| | `VERIFY_cycle2.txt` (12:29:34, broken) | `VERIFY_cycle2_fixed.txt` (12:30:43, fixed) |
|---|---|---|
| platform | `X[-3.0000, 3.0000] Y[-0.3000, 0.3000] Z[-2.0000, 2.0000]` — **local, origin-centred** | `X[-3.0000, 3.0000] Y[0.0000, 0.6000] Z[-8.7500, -4.7500]` — **world** |
| all 8 steps | `X[-0.6000, 0.6000] Z[-0.2000, 0.2000]` — **all eight identical**, i.e. all at the origin | eight distinct world spans, L and R flights separated |
| far wall | `INNER FACE Z = 0.11250` | `INNER FACE Z = -8.75000` |
| clause 5 | **`PASS`** | **`PASS`** |

**Both reported PASS. Only one of them meant anything.** The broken run compared identity transforms to
identity transforms across all 296 nodes and could not have failed — the eight steps reading *byte-identical
AABBs* is the tell, and it is visible in the artifact. **This is TCP-25's rule ("a check that cannot fail on
the case it exists to catch is not a check") firing on the operator's own instrument**, and it is the
second time in this lap that a plausible-shaped zero was the failure mode (the first being `custom_aabb`,
§13).

**Consequence for this report's confidence, stated rather than buried:** clause 5's structural PASS
(`VERIFY_final.txt`, 12:31:50) is a **post-fix** measurement, produced by a verifier that chains local
transforms by hand and is state-independent. **Clause 5 is a real PASS.** Any reading of
`VERIFY_cycle2.txt` as evidence of anything is wrong, and it is retained in the bank only as the error
trail.

## §12 — Frames, judged with my own eyes (L-A)

**TCP-23 honoured throughout: one scene per process, every capture.** Eight capture processes, eight logs,
one frame each — every shoot log ends `complete — 1 frame(s)`.

### The wide shot — `evidence/l4/l4b/frames/L4B_WPRO__box.png` (sha `c4a04c0a…`)

A 17.5 m room seen from high to the southeast on black void. **The room is intact and I can see that it
is:** warm grey-tan brick floor tiling clean across the full span with no seam or palette artefact; four
dark blue-grey walls, the two far ones showing inner faces at full height, the two near ones as thin top
bands; wall-top void caps as a darker course along every wall top; corner pillars with toppers; the soft
warm `InteriorPool` pool near floor centre. **It is prep's reference frame with one thing added and nothing
taken away.**

Against the far (upper-right) wall: the dais, a raised slab whose top surface tiles at the room's own pitch
so it reads as part of the floor plane rather than as a pale insert; two tall pillars standing at its front
corners; two braziers between them; two small stepped wedges — the flanking flights — at each end; and a
clean shadow thrown toward +X.

### The detail crop — `evidence/l4/l4b/frames/L4B_WPRO_DETAIL.png` (sha `b266c8af…`)

Rig: `project/l4_detail_shoot.gd` — **L4a's rig, reused verbatim as its report required**, and the log
confirms parameter-for-parameter identity (`final_shoot_detail.log`):

```
CAM_FOV 20.0 (vertical)   CAM_PITCH -32.0   CAM_YAW 47.0   CAM_DIST 18.0   CAM_AIM (0, 1, -6)
eye=(11.164016, 10.538547, 4.410613)   basis_x=(0.681998, 0.000000, -0.731354)
near/far 0.02/2000   1920x1080  MSAA_4X  SubViewport
```

**What I see:** the dais slab against the far wall, its front face and the step faces reading as tiled
stone at the room's pitch. On the left, the −X flight: **four steps, individually countable, even rise,
even run**. Lower right, the +X flight, treads separable. Two pillars on the slab at its front corners,
visibly inset from both edges, **banded in the pack's atlas palette** (§13). Between them, two braziers —
dark metal tripods with a wide shallow bowl — symmetric about centre, seated flat on the dais top.
**Every clause the crop was added to adjudicate is adjudicable in it.**

### The cycle frames — the P-5 trace, and cycle 1's defect is photographed

| frame | what it shows |
|---|---|
| `C1_L4B_WPRO__box.png` / `C1_L4B_WPRO_DETAIL.png` | **cycle 1.** Geometry all correct and in place. **The dais top, its front face and all eight step faces render as smooth, featureless pale concrete** — the texture is assigned but unmapped, so it stretches across each box instead of tiling. At `__box` the dais reads as a pale grey insert against a tiled floor. **The duplicated props are NOT visible in either frame** (§6) |
| `C2_L4B_WPRO__box.png` / `C2_L4B_WPRO_DETAIL.png` | **cycle 2.** Dais and steps read as stone at the room's pitch; duplicates gone. **Byte-identical to the final frames** (`c4a04c0a…` / `b266c8af…`) — because cycle 3 was four renames and a save |
| `CTRL_SCENE_BEFORE__box_underPro.png` | `scene_before` re-rendered **with the Pro addon installed and live**. sha `248b6b94…`, **byte-identical to prep's reference frame.** The zero point does not move under the swapped addon |

### The four close-ups — shipped, with their provenance declared

`CROP_stairL.png` (849×700), `CROP_stairR.png` (900×360), `CROP_props.png` (725×700),
`CROP_pilbase.png` (679×700). **I looked at all four.**

- **`CROP_stairL`** is the clause-2 evidence and it is decisive: **four steps, countable, even rise, even
  run**, brick-textured, with the dais's dark front face at right.
- **`CROP_stairR`** is the +X flight, tightly framed; three treads are fully in frame and the fourth clips.
- **`CROP_props`** shows both braziers on the dais top: dark charcoal atlas-mapped metal, tripod legs,
  wide shallow bowls, symmetric, seated flat. **Not white blobs** — clause 4's L-A evidence.
- **`CROP_pilbase`** shows a pillar base seated on the dais with its dark plinth, and the atlas banding at
  full magnification.

**Provenance, declared:** none of the four is a byte-exact sub-rectangle of `L4B_WPRO_DETAIL.png`, and
**no rig, script, log or command for them is banked — how they were produced is `UNRECOVERABLE`.** A
multi-scale search run for this report locates each of them inside the detail frame as a **magnified crop**
(best-fit source regions: stairL 360×297 at (160,384); stairR 460×184 at (928,896); props 610×589 at
(560,288); pilbase 240×247 at (480,352); residual mean-abs-difference 4–12 counts, consistent with
upsampling). **They are consistent with magnified crops of the banked detail frame and are shipped on that
basis.** They are **not** independent captures and must not be counted as such. **They are shipped anyway
— L-A binds: the pictures are the deliverable.**

### Two images derived for THIS REPORT, marked so they are never mistaken for run artifacts

- `/tmp/l4b_c1_vs_c2_detail_changemask.png` — the §6 change mask, computed here from the two banked cycle
  frames. **Not a run artifact. Not banked. Reproducible from the two PNGs in one line.**
- The P-2 hull re-rasterization of §5 exists only as numbers in this report.

## §13 — Substrate and spec notes that are NOT this cell's, carried per the dispatch

**Both were traced and closed by the conductor before this report was written
(`2026-07-25-drax-l4b-report-reconstruction.md` §3). Neither is re-investigated here.**

1. **The quilted / rainbow pillars are substrate, not Pro's and not L4a's.**
   `MaterialList_PolygonGeneric.txt` declares `SM_Bld_Base_Pillar_01` → `Slot: Generic_Concrete (Uses custom
   shader)` — one slot, **no albedo texture**. `render_catalogue.gd` treats *"uses custom shader"* as a
   no-albedo sentinel and routes it to a neutral material, which is why the catalogue thumbnail renders
   clean; `kit_replica_level.gd:770` and `:808` apply `tex_atlas` **unconditionally** to pillars and toppers
   in all five kits. **Atlas onto never-atlas-authored UVs = the swatch bands.** The banding is visible in
   L4b's frames exactly as it is in L4a's, from a different instrument, on the same module, and its presence
   here is **corroboration of the attribution, not a second defect.** A separate product dispatch carries
   the fix. **Zero L4b cycles were spent on it** — TCP-27 ③'s propagation worked.
2. **The flanking-stair geometry is a defect in the charter clause, not in Pro's execution.** Measured in
   §3; scored against the clause as written; not fixed, not marked against the instrument.

**A third item, observed in this cell's own artifacts and belonging to neither instrument.**
`custom_aabb` — **L-K instance #4** — is visible returning its plausible-shaped lie in this cell's scene
read: **all 28 `MeshInstance3D` reads** (22 of the 23 responses in `wire/read4/` — the 23rd is `Key`,
a `DirectionalLight3D`, which has no such field — plus all 6 in `wire/read3/`) carry
`"custom_aabb": "[P: (0.0, 0.0, 0.0), S: (0.0, 0.0, 0.0)]"`, on nodes with real, non-zero meshes. **The
executing agent did not use it** — the far wall's inner face was derived from `position` and the mesh
natives instead (`wire/read4/0001_W0_0_in.txt`: `position z = -8.86250`, wall thickness `0.225`, giving the
inner face at `-8.75`, which the verifier later confirms independently). **L-K #4 is confirmed live on a
second instrument-lap and it was correctly not trusted.**

## §14 — Exit predicate, item by item

| # | Item | Status |
|---|---|---|
| 1 | Six-clause conformance checklist, PASS/FAIL, each with its measurement | **DONE** — §3, six PASS, one declared evidentiary gap |
| 2 | P-1..P-6 each resolved to a recorded fact **or** `UNRECOVERABLE` | **DONE** — §5 §6 §8 §9 §10, register at §15 |
| 3 | Wide + detail frames shipped and judged by eye | **DONE** — §12 |
| 4 | `scene_before.tscn` hash re-verified unchanged | **DONE** — `d45db0f507f6b835e14447c9ceb7e7e6bd645e070bc1fe1241dd6e8522de1966`, mode `0444`, **identical to `L4_KIT_CONSTANTS.md` §8**. Re-checked for this report. **Cell is not void** |
| 5 | Pro swap restored, **verified by inventory**, plus the class-name rescan | **DONE** — §4. 361/361 byte-identical; rescan banked at `logs/rescan.log` |
| 6 | TCP-20 fingerprint before/after incl. out-of-lab surfaces | **DONE** — below |
| 7 | TCP-27 ① vacate — cell output out of `project/` | **DONE** — below |
| 8 | No Godot / MCP server left running | **PARTIAL** — see below, and the partiality is named |

### TCP-20 blast radius — `evidence/l4/TCP20_FINGERPRINT_L4B_{BEFORE,AFTER}.txt`, diffed for this report

| surface | files | before vs after |
|---|---|---|
| `Assets/` (whole ignored value tree) | 98,823 | `041896a5…` **identical** |
| `Assets/Synty/polygon-dark-fortress` | 3,028 | `93645a4f…` **identical** — and the **3,028-file per-file manifest is byte-identical** (`cmp` clean) |
| `addons/` | 122 | `ebd02e2e…` **identical** |
| `project.godot` | — | `a76d666a…` **identical**, mtime unchanged at `00:08:22` — **the editor-open tripwire did not fire on the product repo** |
| tracked `git status` | — | `b4e2f0ce…` **identical** |
| **`editor_settings-4.6.tres`** (shared by both Godot builds) | — | **sha `f7a16c0b…` identical, size 3897 identical — but the mtime moved `10:56:04 → 12:35:48`** |
| `app_userdata/tcp_l3_lab` | — | **14 → 15 files (+1)** |

**Two deltas, named rather than rounded down.**

- **The shared editor-settings file WAS written during L4b and rewritten with identical content.** L4a
  reported it *"not written this lap"* (mtime unchanged); L4b's mtime moves by 40 minutes while the bytes
  do not. **This is the TCP-20 amendment earning its place:** had the predicate been content-only, the
  write would have been invisible; had it been mtime-only, it would have read as damage. **It is neither —
  it is a touch.** The `12:35:48` stamp coincides with the post-restore rescan launch (`rescan.log`,
  12:35:48), so the writer is a Godot editor start, consistent with L-J residue #3 (*an editor open is a
  write*) landing on the machine-global surface rather than on `project.godot`.
- **One file added inside the lab's own userdata**, removable per `UNINSTALL.md` §3. **Which file is
  `UNRECOVERABLE`** — the fingerprint records a count, not a manifest, for that directory.

**Continuity across cells, checked for this report:** `TCP20_FINGERPRINT_L4A_AFTER.txt` and
`TCP20_FINGERPRINT_L4B_BEFORE.txt` **differ only in their label and timestamp lines.** Nothing drifted in
the 13 minutes between the two cells.

### TCP-27 ① — cell vacated, and the vacate is verified

`project/` now contains **no** `scene_l4b_wpro.tscn`, **no** `l4b_verify.gd`, **no** `l4b_count.gd` and
**no** call plans. It retains only the shared capture harness (`l4_shoot.gd/.tscn`,
`l4_detail_shoot.gd/.tscn`), the frozen `scene_before.tscn` at mode `0444`, and the project scaffolding.
Everything else moved to `prep/l4b_residue/` with a closed-directory README (12:37:03).

**The README's key claim is that the banked wide shot faithfully records the vacated scene, and I verified
it independently rather than relaying it:** the pre-vacate re-render survives at
`/tmp/L4B_reverify__box.png` (12:34), and its sha256 is
`c4a04c0a64eb5bf7aa5faea6cabff0ef628bcc33987c929d1cd698b7af853070` — **byte-identical to the banked
`L4B_WPRO__box.png`.** `logs/reverify_box.log` records that render: same camera, `err=0`, `real 1.96`.

### Exit state — stated with its limitation

**No artifact records a process check at run close.** What I can state is a check run **now, at
reconstruction time**, which is a different moment and must not be presented as the run's exit predicate:

```
pgrep 'Godot|gamedev-mcp-server|dotnet'   ->  none
port 27435 (Murzak)                       ->  not listening
port 6505  (Pro)                          ->  not listening
```

**One thing the Pro editor log does record, and it is worth a line:** the L4b Pro editor session ended in a
**crash, not a clean exit** — `logs/editor-l4b-pro-headless.log` terminates with
`ERROR: Pages in use exist at exit in PagedAllocator` followed by
`libc++abi: terminating due to uncaught exception of type std::__1::system_error: mutex lock failed`, twice.
**Whether that was the harness tearing it down or an unclean shutdown is `UNRECOVERABLE`**, and it is the
class of event that produced L3's orphaned-editor hazard. Nothing is orphaned now.

### Two more defects visible in the Pro editor log

1. **`save_scene` emits an internal error while succeeding.** The log records 2 `Saving Scene` operations
   and one of them prints, at the *Creating Thumbnail* step:
   `ERROR: Parameter "t" is null. at: texture_2d_get` with a GDScript backtrace through
   `res://addons/godot_mcp/commands/scene_commands.gd:242`. **The save nevertheless completed** — the step
   reports DONE, the tool returned `{"saved": true}` (`wire/c2/0007_save.txt`), and the reloaded file is
   correct in every measurement in this report. **This is NOT an L-K instance** — the operation genuinely
   succeeded. It is a thumbnail-generation path that assumes a real rendering device and finds a dummy one.
   Noise, not damage, but it is noise that looks like damage in a log an operator is scanning.
2. **The addon and the wire disagree about how many tools exist, by one.** The plugin logs
   `[MCP] Registered 174 commands`; `tools/list` served **175** (`wire/list.err`,
   `wire/PRO_LIVE_TOOLNAMES.txt` = 175 lines). Small, but it is **L-B's exact shape** — the component's
   self-report is not the wire — and L2's 175 figure is confirmed live at this lap per **L-C**.

## §15 — `UNRECOVERABLE` register — the complete list

**Everything this reconstruction could not source to a file. Nothing here is inferred elsewhere in the
report.**

| # | Item | Why it cannot be recovered |
|---|---|---|
| 1 | ***"`timeout` isn't on macOS — RC=127 means the editor never ran. Retrying."*** | **No artifact records the failed invocation, its exit code, or the retry.** The transcript fragment exists only in the conductor's dispatch §1.8. What *is* on disk is a successful post-restore rescan (`logs/rescan.log`, 12:35:48), which is consistent with a retry having succeeded — **but the failure itself is not evidenced and is not asserted here** |
| 2 | The **route-decision procedure** for P-3 | L4a banked `ROUTE_DECISION.txt` *before execution*; **L4b banked only the first prompt.** P-3's "unprompted" claim therefore rests on the prompt's cleanliness and the call census alone — both of which are strong — but **no pre-committed decision procedure exists for this cell** |
| 3 | **Render and headless-script durations**, 7 of 8 renders and all 5 script runs | The shoot logs record camera and `err=0` but no timing; only `reverify_box.log` carries `real 1.96` |
| 4 | **Server-side handler latency** | Pro's addon is the server and emits no per-handler timing; **there is no L4b analogue of `logs/server-l4a.log`** |
| 5 | **The crop rig** for the four `CROP_*.png` | No script, no log, no command banked. Provenance reconstructed only as "consistent with magnified crops of the detail frame" (§12) |
| 6 | Whether **Pro rewrote `[autoload]`** (L-J residue #1) and it was restored, or never rewrote it | `project.godot` is byte-identical to the PRE-L4B bank. **Both histories produce that artifact** |
| 7 | **Which file** the lab `app_userdata` gained (14 → 15) | The TCP-20 fingerprint records a count for that directory, not a manifest |
| 8 | **The exit-state process check at run close** | No artifact. The check in §14 was run at reconstruction time and is labelled as such |
| 9 | **Number of Godot editor launches** during the cell, and any inherited-orphan check at session start | One Pro editor log survives; earlier launches, if any, are not preserved |
| 10 | Whether the 314-node output is stable across a **repack** (not just a reload) | L4a ran that round-trip explicitly; **L4b's artifacts show a load-from-disk count only** |
| 11 | **The TCP-25 rendered-mean figures** for the dais props | Not banked for this cell (§3, clause 4) |
| 12 | The executing agent's **reasoning** at any decision point | Out of scope of artifacts by construction. This is the §0 boundary and it is the reason this register exists |

## §16 — For the conductor

**No HALT was triggered, and the three the dispatch named were each checked:**

- **Restore verification checks out.** §4 — `MUR_INVENTORY.sha256` verifies **361/361**; the Pro install
  bank (`PRO_INVENTORY.sha256`) accounts for **44/44 unchanged** with a fully attributed +35.
- **No artifact contradicts any number in dispatch §2.** P-2, P-5 and P-3 all reproduce. Two
  **refinements** are recorded, neither a contradiction: the cycle-1 outside-pixel column is not blank —
  it is **identical** to the final (59 / delta 1); and "11 plans" resolves as **10 executed call-plans
  (90 `tools/call`) plus one `tools/list` enumeration**.
- **`P3_FIRST_PROMPT_BANKED.md` contains no method noun.** Read in full. P-3 is uncontaminated for this
  cell.

**Six things worth a ruling or a ledger line:**

1. **§4 — L-J vindicated in the direction nobody had seen, and the growth is attributed.** 44 → 79 files
   under an unchanged `1.15.1`, all 35 new files Godot's own `.uid` sidecars, 0 removed, 0 changed.
   **Proposed amendment: L-J's predicate should compare per-path content and declare engine-generated
   sidecars an expected non-corrupting delta**, or the next swap lap HALTs on a benign bloom.
2. **§6 — L-A gets its sharpest qualification yet: a rendered frame structurally cannot catch a
   co-located duplicate.** P-6 fired on Pro, 318 nodes instead of 314, four untextured copies, every call
   `ok`, and **the picture is pixel-identical before and after the fix.** The catching instrument was a
   reload-from-disk census. **L-A is necessary and not sufficient**, and the two instruments are not
   redundant.
3. **§7 — a new failure shape: a collision-rename that produces the name of a different real module.**
   `SM_Prop_Brazier_05` and `SM_Bld_Base_Pillar_02` both exist in the pack. **The artifact read as a
   clause-4 violation and was not one.** Any audit that reads node names rather than measuring meshes
   would have convicted an innocent cell.
4. **§6 — the two instruments sit at opposite poles of TCP-24's trilemma, and Pro's escape is cheaper.**
   Pro: own-all → duplicates → cleared by `scene_file_path = ""`, **4 calls**. Murzak: own-root-only →
   silent material loss → cleared by reparent-out + delete-root + null-first assign, **3 call shapes plus a
   mandatory delete**. Both routes are publishable; they are not the same route and the comparison is only
   available because both cells ran.
5. **§8 — P-3 resolves node-by-node for a SECOND instrument, on the same task, for a structurally similar
   reason.** Both wires handled the bulk on the node family and both needed the escape hatch for exactly
   one thing their wire could not express (Murzak: read a transform; Pro: address a sub-resource property
   path). **`batch_add_nodes` and `add_gridmap` were both live and neither was called**, so the charter's
   GridMap correctness prediction remains **untested**.
6. **§8 — a counter-example to L-K that should be on the record.** Pro's property wire failed **loudly**,
   named the rejected property and **listed the twenty that would have worked.** In a program built on
   "failure returns SUCCESS," an instrument's verdict should say **which of its surfaces fail honestly**,
   because those are the surfaces an agent can iterate against cheaply.

**Honorable-fallback status (L-F/L-G):** nothing needed one. **One ceiling was hit and is named with its
exact blocking artifact** per L-G: Pro's `update_property` cannot address a sub-resource property path —
`Property 'surface_material_override/0:uv1_scale' on MeshInstance3D not found`, with the tool's own
available-property list as the blocking artifact (`wire/probe/0003_uv_subpath_probe.txt`). Worked around
via `execute_editor_script`, 1 call of 90.

---

## Artifact inventory — everything under `evidence/l4/l4b/` (164 files) and `prep/l4b_residue/` (12 files)

**Report:** `agentic_orchestration/drax/notes/2026-07-25-tcp-l4b-wpro-run-report.md`

### `~/Games/mcp-lab/evidence/l4/l4b/` — 164 files, 10 MB

| group | count | contents |
|---|---|---|
| **root** | 2 | `P3_FIRST_PROMPT_BANKED.md` (P-3 evidence, banked 12:14:36 pre-install) · `l4b_TIMELINE.txt` (`AUTHORING_END`, `RUN_END`) |
| **`frames/`** | 11 | `L4B_WPRO__box.png` `c4a04c0a…` · `L4B_WPRO_DETAIL.png` `b266c8af…` · `C1_L4B_WPRO__box.png` `7134fc35…` · `C1_L4B_WPRO_DETAIL.png` `ab7a6a18…` · `C2_L4B_WPRO__box.png` (= final, `c4a04c0a…`) · `C2_L4B_WPRO_DETAIL.png` (= final, `b266c8af…`) · `CTRL_SCENE_BEFORE__box_underPro.png` `248b6b94…` (= prep reference) · `CROP_stairL.png` · `CROP_stairR.png` · `CROP_props.png` · `CROP_pilbase.png` |
| **`diff/`** | 8 | final: `L4B_WPRO_DIFF.json` · `L4B_WPRO_DIFF.png` · `L4B_WPRO_DIFFx4.png` · `L4B_WPRO_DIFFx4_MASKED.png` — cycle 1: `C1_L4B_WPRO_DIFF.json` · `.png` · `x4.png` · `x4_MASKED.png` |
| **`logs/`** | 15 | `VERIFY_final.txt` · `VERIFY_cycle2_fixed.txt` · `VERIFY_cycle2.txt` (**the broken run, retained as error trail** — §11) · `P6_count_cycle1.txt` (318) · `P6_count_cycle2.txt` (314) · `P6_dais_cycle1.txt` (the duplicate dump) · `c1_shoot_box.log` · `c1_shoot_detail.log` · `c2_shoot_box.log` · `c2_shoot_detail.log` · `ctrl_shoot_box.log` · `final_shoot_box.log` · `final_shoot_detail.log` · `reverify_box.log` (pre-vacate re-render, `real 1.96`) · `rescan.log` (post-restore class-name rescan, 61 KB) |
| **`swap/`** | 6 | `PRO_INVENTORY.sha256` (**44 files, banked at install — the §4 evidence**) · `MUR_INVENTORY.sha256` (361) · `MUR_INVENTORY_SUMMARY.txt` (361 files / 161 `.cs` / manifest sha `871663b2…`) · `project.godot.PRE-L4B` · `mcp.json.PRE-L4B` · `global_script_class_cache.cfg.PRE-L4B` |
| **`wire/` top level** | 34 | per plan (`read1..read5`, `probe`, `c1a`, `c1b`, `c2`, `c3`): `.jsonl` (per-call `seq/label/tool/ms/ok/result_bytes/error`) + `.summary.json` + `.err`; plus `read1.out`, `list.err` (**`tools/list -> 175 tools in 12 ms`**), `PRO_LIVE_MANIFEST.json` and `PRO_LIVE_TOOLNAMES.txt` (**L-C re-enumeration, 175 tools**) |
| **`wire/<plan>/`** | 88 | verbatim per-call responses, numbered and labelled: `c1a/` 22 · `c1b/` 15 · `c2/` 7 · `c3/` 7 · `probe/` 4 · `read2/` 3 · `read3/` 6 · `read4/` 23 · `read5/` 1 |
| *(also present)* | 1 | `.DS_Store` — Finder metadata, not evidence |

### `~/Games/mcp-lab/prep/l4b_residue/` — 12 files, 328 KB — **CLOSED DIRECTORY**

| file | what it is |
|---|---|
| `README_DO_NOT_PLACE_IN_PROJECT.md` | the TCP-27 ① closure note and manifest |
| `scene_l4b_wpro.tscn` | **the cell output** — 314 nodes, the solved dais. sha `da04d6c7…` |
| `l4b_verify.gd` (+ `.uid`) | spec-conformance world AABBs + structural non-destruction diff. **Carries the §11 defect note in its own source** |
| `l4b_count.gd` (+ `.uid`) | P-6 rig: reload-from-disk node count + material census. **The instrument that caught §6** |
| `l4b_c1a.json` · `l4b_c1b.json` | cycle-1 wire plans (geometry; then materials + save) |
| `l4b_c2.json` | cycle-2 plan — de-instance ×4, the `execute_editor_script` UV call verbatim, save |
| `l4b_c3.json` | cycle-3 plan — 4 renames + save |
| `l4b_probe.json` | the de-instance / UV-subpath probe |
| `l4b_read4.json` | the scene-read plan (23 `get_node_properties`) |

### Cross-referenced, outside the two directories

| artifact | path |
|---|---|
| **Run-start stamp** | `~/Games/mcp-lab/evidence/l4/l4b_TIMELINE.txt` (`L4B_RUN_START 16:12:52Z`) |
| **TCP-20 fingerprints + 3,028-file pack manifests** | `~/Games/mcp-lab/evidence/l4/TCP20_FINGERPRINT_L4B_{BEFORE,AFTER}.txt`, `TCP20_MANIFEST_darkfortress_L4B_{BEFORE,AFTER}.txt` |
| **Pro editor session log** (§14 defects) | `~/Games/mcp-lab/logs/editor-l4b-pro-headless.log` |
| **The parked Pro addon — the §4 evidence, 79 files** | `~/Games/mcp-lab/_swap/pro_addon_godot_mcp_USED/` |
| **Pro wire tooling** (outside `project/`) | `~/Games/mcp-lab/bin/pro_mcp_client.mjs`, `bin/editor_up_pro.sh` |
| **The differ, unmodified since PREP** | `~/Games/mcp-lab/prep/l4_diff.py` (mtime `11:10`) |
| **Frozen substrate** | `~/Games/mcp-lab/project/scene_before.tscn` — `d45db0f5…`, mode `0444` |
| **Shared capture harness (TCP-8), left in place for L4c** | `~/Games/mcp-lab/project/l4_shoot.gd/.tscn`, `l4_detail_shoot.gd/.tscn` |
| **Pre-vacate re-render, survives and was verified** | `/tmp/L4B_reverify__box.png` — `c4a04c0a…` |

---

**Signed:** drax, 2026-07-25 (presentation seam).
**RECONSTRUCTION — authored from surviving artifacts after the executing agent terminated.** Every claim is
sourced to a named file or marked `UNRECOVERABLE` at §15. **This report is not a run log and must not be
cited as one.**
