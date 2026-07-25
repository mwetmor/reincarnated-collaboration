# TCP-L4-PREP — SUBSTRATE + DIFF CALIBRATION (run report)

**Program:** Tool-Capability Program · lap **L4**, **prep dispatch** (control cell — runs no instrument)
**Charters:** `2026-07-24-tool-capability-program-charter.md` · `2026-07-25-tcp-l4-expansion-bakeoff-charter.md`
**Conductor:** gandalf (`RUN-CONDUCTOR`) · **Executor:** drax (presentation seam)
**Status:** **CLOSED — PASS.** All eight exit-predicate items met.

---

## §0 — Verdict, in one paragraph

**The substrate is built, frozen, hashed and photographed; the differ is calibrated at both
points; the product repo is provably untouched.** `scene_before.tscn` is the L2 room — 17.5 m
square, polygon-dark-fortress, environment, lighting, void caps and occlusion-split shaders all
ported — 296 nodes, sha256 `d45db0f5…`, mode 0444. The differ's zero point is **exactly zero,
not "small"**, and its non-zero point detects a 5 cm nudge with the bright pixels on the nudged
node. Against that: **three defects found, two of them in this dispatch's own instructions and
one in my own predicate.** (1) The "exactly zero" requirement was *unsatisfiable as written* —
the renderer drifts with every capture inside a process — and became satisfiable only after I
found the rule that makes it deterministic; the fix is now structurally enforced. (2) Building
`scene_before` the way the reference builder does **reproduces L2's `set_owner_recursive`
duplication from a plain GDScript builder with no wire involved**, which would have made all
three cells fail P-2 for reasons that are Godot's, not the instruments'. (3) My own TCP-20
predicate did not cover a config surface both Godot builds share, and that surface was written.
**gandalf's constants table is correct on all four modules to six decimals** — the first thing
in this program I have re-measured and found already right.

## §1 — Rubric diff against intent (law L-I — name what falls out, out loud)

This dispatch builds the substrate and **runs no instrument**. It therefore says **nothing** about
W-MUR, W-PRO or H. It cannot: that is its design. Two things it *does* settle that a reader
might over-read:

- **The FBX-instance duplication (§4) is NOT evidence against Pro.** It is evidence that L2's
  mechanism is a property of Godot's scene serialization. It neither convicts nor exonerates
  Pro on P-2 — it removes the mechanism from the substrate so P-2 can measure the instruments.
- **A calibrated differ is not a correct verdict.** It is a differ that has been shown to detect
  a change it was handed. §6 names the one direction in which it can still lie.

## §2 — Exit predicate, item by item

| # | Item | Status |
|---|---|---|
| 1 | Pack copied + imported; **median** with n and exclusions | **DONE** — §3 |
| 2 | `scene_before.tscn` built, frozen, SHA-256 published | **DONE** — `d45db0f5…`, mode 0444 |
| 3 | Builder relocated out of the project dir | **DONE** — §5 |
| 4 | `L4_KIT_CONSTANTS.md` published; natives measured; props verified; camera exact; **no placements** | **DONE** — §7 |
| 5 | Rendered at `__box`; **ship the picture**; judge with my own eyes | **DONE** — §8 |
| 6 | Differ built and calibrated at **both** points, with both strips | **DONE** — §6 |
| 7 | TCP-20 fingerprint before and after; they match | **DONE** — §9 |
| 8 | No Godot / `gamedev-mcp-server` processes left | **DONE** — §9 |

## §3 — The pack (exit 1)

`polygon-dark-fortress` copied — **never symlinked** — from `reincarnated-godot` to the mirrored
path `project/Assets/Synty/polygon-dark-fortress/`, so `res://` paths match and `.import`
sidecars stay valid. A symlink lets Godot's importer rewrite sidecars *through* the link into
the product tree, invisibly to git (L3 §5.2 / TCP-20).

| Measurement | Result |
|---|---|
| Copy (338 MB, **3028** files) | **2.27 s** |
| **Cold import**, `--headless --import` | **68.68 s**, RC=0 — **n=1, and this is NOT a median** |
| **Warm re-import median** | **2.67 s** — **n=5**, sorted 2.36 / 2.67 / **2.67** / 2.68 / 2.89, **no exclusions** |
| Imported artifacts | 2530 → 5556 (+3026) |
| Cold-import error lines | 3906, all one benign class |
| Warm-import error lines | **0** |

**On the statistic (TCP-19).** A cache can only be cold once, so the cold figure is a single
observation and is reported as one rather than dressed up as a median. Nothing was excluded from
the warm set — all five runs are in the sorted list above.

**The 3906 cold error lines are the same benign class L3 documented**, confirmed here rather than
assumed: `.psd` and Dropbox authoring paths baked into Synty's FBX material slots
(`res://Assets/Dropbox/SyntyStudios/PolygonDarkFortress/_Working/_Textures/…psd`). No `.psd`
ships in any pack. They are noise, they vanish on warm import, and they will drown an L4 log —
filter them, do not triage them.

## §4 — CHARTER-ADJACENT DEFECT: building the room the reference way reproduces L2's failure — with no wire anywhere near it

The reference builder (`kit_replica_level.gd`) does `load(fbx).instantiate()` and adds the
sub-scene. **Packing that to a `.tscn` from a headless SceneTree is broken**, and I measured it
three ways before changing anything:

| route | nodes in → out | surface overrides in → out |
|---|---|---|
| own-all, `GEN_EDIT_STATE_DISABLED` | 4 → **6** | 2 → 2 |
| own-all, `GEN_EDIT_STATE_INSTANCE` | 4 → **6** | 2 → 2 |
| own **root only** | 4 → 4 | 2 → **0** |

The first two write the instance's internal child with `type="MeshInstance3D"`, so on reload the
FBX instance creates it **and** the explicit entry creates it again — collision and rename. The
third is clean on nodes and **silently drops every material**. Edit state only removes `type=`
from the instance *root* line, not from the child. The `[node … index="0"]` modify-in-place form
that the R1/R2 rooms carry on disk was emitted by hand-written Python (L1's M2 path), not by
`PackedScene.pack()`. At full room scale the naive route gave **808 nodes in, 1320 out**.

**This is the mechanism L2 attributed to Pro** — `add_scene_instance` calling
`set_owner_recursive`, internal nodes saving owned *and* re-instancing. **Reproduced here from a
plain GDScript builder, headless, with no MCP server running.** So it is a property of Godot's
scene serialization, not a Pro defect. L2's observation stands; its **attribution** should be
widened.

**Why the fix is a fix and not a workaround.** Had the frozen substrate carried that fragility,
every instrument that re-saved it would be damaged **by Godot**, P-2 would return FAIL for all
three cells, and the lap would have measured the engine while reporting on the instruments. That
is the confound-removal an experimental control exists to do.

**The fix:** flatten each module to a plain `MeshInstance3D` with the FBX-internal transform
composed on the right (`world = placement ∘ internal`). Round-trip is now clean — **296 nodes and
540 surface overrides in, 296 and 540 out** — and every piece of geometry is directly addressable
by node path, which is *fairer to the wire instruments* than burying it behind an instance
boundary.

**Declared losses:** the FBX's own `AnimationPlayer` child (a Synty import artifact on static
architecture) and the FBX-as-`ExtResource` reference for geometry; the four module meshes inline
as 8 deduped `ArrayMesh` sub-resources. Textures and shaders remain `ExtResource`s.

**A nearly-silent 4.5 mm bug the flattener surfaced:** the pillar FBX's internal mesh node is
offset **+0.004478 m in Y**. Instancing applies it for you; extracting the mesh does not.
Composed correctly, and published in the constants file so no cell rediscovers it.

**What was ported, and what was not.** Ported verbatim: invariants, environment, lighting, floor
tiling, wall placement + origin re-centring, **void caps**, **occlusion-split ShaderMaterials**,
south dissolve, pillars + toppers, the imported-texture colour-space rule. The shaders cost three
self-contained file copies (388 lines, no includes), so "port cheaply" was satisfied and I took
them. **Deliberately omitted, because it changes what the diff sees:** *collision* (TCP-14 — owed
by rooms intended to be walked, not photographed; invisible to a pixel differ) and *the occupant
+ hero-fill light rig* (the spec has no occupant, and the pilot rigs are character assets in
`reincarnated-godot` — dragging them into the lab widens the blast radius for nothing).
Consequently **lighting is the room's own rig only, baked into the scene**, so every cell
inherits it from the substrate and the shooter contributes only a camera. The L2 `env_kit` fixup
cannot be needed here.

## §5 — The forbidden artifact, and a second contamination source the dispatch did not anticipate

`l4prep_build_scene_before.gd` was moved to
`~/Games/mcp-lab/prep/FORBIDDEN_do_not_place_in_project/` the moment it had run, with the
prohibition in its own header. The measure probe, the pack probe and the prop-proof rig went with
it. **The line the dispatch drew is intact: instruments may read `scene_before.tscn` by any means;
they may not read the builder that produced it.**

**Found while doing it — and I am flagging it rather than quietly fixing it, because it bears
directly on a prediction.** L3 left `tcp_l3b_builder.gd` sitting in the project directory. That is
**a worked, wire-authored GDScript room builder** — the W→H proof artifact. **P-3 asks whether
Murzak *naturally* routes through W→H or goes node-by-node.** An agent that opens the project and
finds a Murzak-authored builder already there is not answering that question freely. Moved to
`prep/l3_residue/`, with the rest of the L3 scratch scenes.

**Amendment owed to the L3 report's artifact index:** `project/tcp_l3b_builder.gd` and its
siblings are now at `prep/l3_residue/`. Nothing was deleted.

**One thing I moved and had to put back**, recorded because a silent restore is how a real break
hides: the glob `project/tcp_l3*` also caught **`tcp_l3_lab.csproj`**, the lab's .NET project file
that Murzak requires. Restored immediately; `project/` verified afterward.

**Also disabled for this lap:** the `godot_mcp` editor plugin in the lab's `project.godot`. Prep
runs no instrument, and the addon's compiled-in default connection mode is **Cloud** (L3 §4.1 /
Q46) — merely loading it transmits machine name and project identity before any tool call, and it
writes 39 `SKILL.md` files uninvited. **L4a must restore the line verbatim**; it is quoted in a
comment at the edit site and the original file is banked at `evidence/l4/project.godot.PRE-L4PREP`.

## §6 — THE DIFF INSTRUMENT, and the dispatch defect its calibration exposed

Instrument: `~/Games/mcp-lab/prep/l4_diff.py`. Full evidence: `~/Games/mcp-lab/evidence/l4/CALIBRATION.md`.

### 6.1 The "exactly zero" requirement was unsatisfiable as written

The dispatch is explicit: *"Not 'small'. Zero."* On first measurement it was not zero — two
renders of the same scene differed in 2 pixels. **That is not noise, and calling it noise would
have been the easy wrong answer.** Six renders across three processes showed the pattern:

- all three **position-1** frames byte-identical, sha `248b6b94…`
- all three **position-2** frames byte-identical, sha `c74a1a50…`

Capture **order** was leaking into the pixels. Three captures of the same scene in one process
then gave **q1 ≠ q2 ≠ q3**, and the drift **grows and spreads**: q1↔q2 is 2 px in a 5×2 bbox;
q2↔q3 is 7 px in a **507×217** bbox. So it is not warm-up either — discarding a first frame would
not have fixed it.

**One capture per process is byte-identical across processes, and equals q1 exactly.** With that
rule the zero point is **exactly zero: max channel delta 0, changed pixels 0 of 2,073,600.**

**This threatens the lap's own exit predicate.** Charter §5.1 asks the H dispatch to assemble a
four-cell contact sheet. Shot in one process, three of four cells are photographed under drifted
state and every P-2 number carries an undeclared contaminant. It is 2–7 px *here*; nothing bounds
it for a scene with more shadow casters or a brazier bright enough to cross the glow threshold.

**Fixed structurally, not documented:** `l4_shoot.gd` now **refuses** more than one scene per
invocation and exits non-zero. Same principle as L3's `editor_up.sh` — make the failure impossible
rather than trusting the operator to remember. Verified: it refuses.

### 6.2 The projection was calibrated before the mask was trusted

A mask derived from an unverified projection is the same trap in new clothes, so seven world
anchors were projected through the exact `__box` camera and drawn on the frame. Floor corners
land on floor corners; `Pillar_1 top` lands on the pillar cap; the far-wall inner top lands on the
wall's top edge. **The useful one is the falsifiable one:** the near floor corner projects to
y = 1298.7, *below the 1080-px frame* — and it is indeed cut off in the picture.

### 6.3 Both calibration points

| | result |
|---|---|
| **ZERO POINT** | max Δ **0**, changed px **0** / 2,073,600, mean 0.0 |
| **NON-ZERO POINT** — `Pillar_1` origin.x 8.9750000 → 9.0250000 (+5 cm) | changed px **4264**, max Δ **82**, mean 0.0206 |
| — inside the masked-out region | **0** |
| — intensity centroid | **(1769.3, 588.0)** |
| — `Pillar_1` projects | base (1737.0, 627.9) → top (1775.0, 506.5), mid (1755.5, 568.8) |

**The bright pixels land on the nudged node** — centroid 13.8 px in X and 19.2 px in Y from the
pillar's mid-height, changed bbox `[1667, 448, 1828, 656]` bracketing its full screen extent. The
bbox is wider than the pillar because the pillar's **shadow** moved with it, which is correct.
Both strips shipped; `_nonzero_crop.png` puts the room beside the `|diff| ×4` and shows a bright
pillar-shaped sliver at exactly the pillar's position, everything else black.

**`Pillar_1` was chosen because it is OUTSIDE the mask.** The calibration must prove the differ
detects a change in the region it is *responsible for*. A nudge inside the mask would be correctly
ignored and would have proved nothing. The nudge was made by **text edit, no Godot script**, so
the frozen original is provably never opened for write — its hash re-read after the edit is
unchanged.

### 6.4 The mask, stated — and the one direction it can lie

Defined in **world space from the frozen spec** (never from any cell's output, or it is not a
held-constant instrument), projected and filled as a convex hull:

```
spec platform  x [-3.0, 3.0]  z [-8.75, -4.75]  y [0, 0.6]
spec stairs    1.2 m wide, 4 x 0.40 m run  -> x to ±4.2, z to -3.15
spec pillars   on the dais, ~3.07 m        -> y to ~3.67
ENVELOPE       x [-5.00, 5.00]  y [-0.10, 4.20]  z [-8.85, -2.35]   + 24 px dilation
```

Covers **342,783 px = 16.53 %** of frame; **1,730,817 px** are measured for P-2.

**Shadow analysis, because a dais legitimately changes light outside its own footprint.** Only the
Key `DirectionalLight3D` casts shadows (Fill and InteriorPool do not). Its direction is
**(0.2204, −0.8829, −0.4145)** — toward **+X and −Z**, i.e. *toward the far wall*. A 3.67 m dais
pillar throws 0.92 m in +X and 1.72 m in −Z; the 1.84 m brazier throws 0.46 / 0.86 m. Both land
inside the envelope. No GI is enabled, so there is no bounce term.

**RESIDUAL RISK, declared:** a cell whose addition **exceeds** the spec envelope will throw shadow
outside the mask, and that reads as destruction when it is physics. **If a cell's diff shows bright
pixels hugging the mask boundary on the +X / −Z side, suspect shadow spill before declaring damage.**
This is the one place the instrument can lie, and it lies toward **false conviction**, not false
acquittal — which, given L-G makes mis-attribution the only real failure, is the direction that
matters.

## §7 — Constants file (exit 4)

`~/Games/mcp-lab/evidence/L4_KIT_CONSTANTS.md`. **Module natives only. No scene placements** — the
far wall's inner-face Z, the floor extent, the tile pitch, the node names and the room dimensions
are all readable from `scene_before.tscn` and are deliberately absent, because that is what P-4
measures.

**gandalf's table is correct.** Re-measured, not copied — all four modules agree **exactly**:

| | dispatch table | measured |
|---|---|---|
| wall | `2.499991 × 3.005743 × 0.225`, origin z `−0.112500` | identical |
| floor | `1.249996`, top face `+0.008090` | identical (`−0.092517 + 0.100607`) |
| pillar | w `0.429056`, h `3.015154` | identical |
| topper | w `0.486970`, base y `−0.013555` | identical |

**No disagreement to report.** Two footnotes the table does not carry: the floor tile is
anisotropic by 4 µm (x `1.249996`, z `1.250000`), and the pillar's internal +4.478 mm Y offset
(§4).

**Three things published that the dispatch did not ask for and the cells need:**

1. **Surface counts.** `wall` and `floor` carry **2** surfaces; `pillar`, `topper` and the prop
   carry **1**. TCP-16 one level down: `set_material_3d` is single-surface, no tool reports the
   count, and a single-slot assignment leaves surface 1 untextured — R2's cream floor.
2. **Every module in this pack ships `albedo_texture = NULL`**, `albedo_color ≈ (0.906, 0.906,
   0.906, 0.8)`. A module placed with no override is a **translucent near-white blob**. This is
   the L2 white-floor failure available by default, to every cell, on every module.
3. **The `__box` camera read off the running rig**, not transcribed: eye
   `(23.123901, 39.502224, 21.687008)`, the three basis rows, fov 20.0 (vertical — Godot defaults
   to `KEEP_HEIGHT`), near/far 0.02/2000, 1920×1080 MSAA_4X.

### 7.1 The dais props — VERIFIED, no substitution

**`DarkFortress/FBX/SM_Prop_Brazier_04.fbx` ×2 passes both checks.** gandalf's proposal holds.

| property | measured |
|---|---|
| size | `0.686378, 1.240413, 0.686378` |
| origin convention | **centred in X/Z, base at y = 0** |
| meshes / surfaces | 1 / **1** |
| own material | `albedo_texture=NULL`, `albedo_color=(0.9063,…,0.8)` |
| texture presence, **rendered** | raw mean `(206.0, 206.8, 210.1)` → atlas-mapped `(81.8, 85.2, 89.2)` |

Evidence is a picture, not a return code: `evidence/l4/frames/PROP_brazier04_raw_vs_textured.png`
— left, the raw white blob; right, atlas-mapped charcoal. **Single-surface**, so the two-surface
trap does not apply to *it* — but does to the walls and floor, which means a cell can get the
brazier right and the walls wrong with the same call shape. Its base-centred origin means
`position = (x, dais_top_y, z)` stands it on the dais with no offset arithmetic. All four siblings
were measured too, so a substitute is pre-costed if a cell hits a blocker.

**A defect in my own instrument, recorded.** The prop rig's automated "is it textured" test
measured **rendered pixel variance** and returned **TEXTURED for the untextured white brazier** —
shading creates variance on a flat material. Worse for this pack: Synty assets UV-map onto solid
palette patches, so a *correctly* atlas-mapped prop also reads flat. **The discriminating signal
is the MEAN (≈206 vs ≈82), not the variance.** Any cell that checks its dressing with a variance
test will pass a white blob. Had I trusted my own check instead of looking at the picture, I would
have filed a green tick on a broken test.

**And a live L-K near-instance in my own harness, caught by L-A.** The prop rig's first run
returned `err=0`, `surfaces=1`, `overridden=1`, `saved …` — and rendered an **empty frame**. Every
counter said success. The log named the cause on one line (`Node not inside tree. Use
look_at_from_position()` — `look_at` called before `add_child`, leaving the camera at identity
basis aimed at nothing). **I read the log rather than guessing**, per TCP-21: an L-K instance
requires both that the tool reported success *and* that the operation was correctly invoked. This
was operator error, so it is not an L-K instance — it is a reminder that the picture is the
predicate.

## §8 — The frame, and what I see in it (exit 5, L-A)

`~/Games/mcp-lab/evidence/l4/frames/SCENE_BEFORE__box.png` — 1920×1080, `__box`, MSAA_4X.

**Judged by eye, not merely produced.** A 17.5 m square room seen from high to the southeast on
black void: warm grey-tan brick floor tiling reading cleanly across the full span with no seam or
palette artefact; four dark blue-grey brick walls, the two far ones showing their inner faces at
full height, the two near ones seen from above as thin top bands — the 50° camera looks *over*
them, which is why the occlusion-split shaders are not load-bearing at this framing even though
they are present; wall-top void caps reading as a distinct darker course along every wall top,
correctly seated and not rainbowed (the pack ships genuine tiling stone, so L1's cap defect does
not recur); pale-tan corner pillars with their caps at three visible corners; and a soft warm pool
on the floor near centre from the `InteriorPool` omni.

**It matches the L2 M3 reference frame** (`reincarnated-godot/harness_logs/tcp_l2_2026-07-24/M3_dark-fortress__box.png`)
minus the occupant and aura — which is exactly the declared difference. **The far (−Z) wall the
dais goes against is the upper-right wall in frame**; the projected mask hull sits on the
upper-right quadrant of the floor, which is where the dais belongs.

Also shipped: `PROP_brazier04_raw_vs_textured.png`, `ZEROPOINT_PROJECTION_CHECK.png`,
`NONZEROPOINT_DIFFx4.png`, `NONZEROPOINT_DIFFx4_MASKED.png`, `_nonzero_crop.png`.

## §9 — Blast radius (exit 7) and exit state (exit 8)

**TCP-20 fingerprint, BEFORE and AFTER — IDENTICAL on every surface.** `git status` alone does not
satisfy this and was never relied on: 2.67 MiB is tracked against **10 GB / 98,823 files** of
gitignored `Assets/`.

| surface | files | sha256 | before vs after |
|---|---|---|---|
| `Assets/` (whole ignored value tree) | 98,823 | `041896a5…` | **identical** |
| `Assets/Synty/polygon-dark-fortress` | 3,028 | `93645a4f…` | **identical** — and the **per-file manifest diffs byte-for-byte clean** |
| `addons/` | 122 | `ebd02e2e…` | **identical** |
| `project.godot` | — | `a76d666a…` | **identical** (and equal to L3's baseline) |
| `.godot/` mtime + count | 131,796 | — | **identical** |
| tracked `git status` | — | `b4e2f0ce…` | **identical** |

The pre-existing uncommitted `M project.godot` (L-J residue #3, mtime 2026-07-25 00:08 — before
this lap and before L3's lab existed) was left exactly as found.

**Exit state:** `pgrep 'Godot|gamedev-mcp-server|dotnet'` → none. Port 27435 → not listening. **The
inherited orphan L3 found did not recur** — checked at session start and at close.

### 9.1 Residue outside the lab — a defect in MY OWN predicate

**`~/.dotnet` and `~/.nuget`: ZERO files touched.** L3's §7 escape did not recur; no `dotnet` was
invoked.

**But `~/Library/Application Support/Godot/` was written, and my fingerprint did not cover it.**
It is pre-existing (2026-06-14, 1.7 GB) and **SHARED by both Godot builds** — the lab's
`Godot_mono.app` 4.6.3 and `/Applications/Godot.app` 4.6.3 write the same paths.

1. **`editor_settings-4.6.tres` rewritten at 10:56:04 by a plain `--script` run.** No `--editor`
   was used anywhere. This is **L-J residue #3 in a new location**: a tools-build run is a WRITE,
   and it reports nothing. The file carries no reference to the lab, so it is most likely a no-op
   resave — **but I had no baseline to diff against, which is the defect.** TCP-18 constraint 2
   protects `/Applications/Godot.app`; its *configuration* is a different object and was not
   covered. Baseline now banked (`f7a16c0b…`, size 3897) and
   `prep/fingerprint_product_repo.sh` §6 covers it for L4a/b/c.
2. **`app_userdata/tcp_l3_lab/` — 12 files, 888 KB** (run logs + Metal shader cache). Ours,
   removable; command in `UNINSTALL.md` §3.

Named rather than rounded down, because TCP-18 constraint 1 says *everything* lands in the lab and
13 filesystem entries did not.

## §10 — Defects found (the dispatch said to assume there were more; there were three)

1. **"Exactly zero" was unsatisfiable as written** (§6.1). Not a wrong instruction — a *right*
   instruction whose precondition did not hold and had never been checked. It became satisfiable
   only after finding the one-scene-per-process rule, which is now enforced in code. **The
   requirement was worth more than an easier one would have been**: had the dispatch said "small",
   I would have accepted 2 px as noise and never found the order-dependent drift, which is the
   larger finding.
2. **The reference build path reproduces L2's duplication with no wire present** (§4). Fixed by
   flattening, with the confound removed from the experiment rather than papered over.
3. **My own TCP-20 predicate had a hole** (§9.1) — same *class* of error the L3 charter made:
   a verification predicate that does not cover the surface being written. Fixed for the
   downstream dispatches.

**Plus one contamination source the dispatch did not anticipate** (§5): L3's wire-authored builder
sitting in the project directory, directly bearing on P-3.

## §11 — For the conductor

**No HALT was triggered.** Nothing was written into any product repo; no `sudo`; no machine-wide
install; `/Applications/Godot.app` never invoked.

**Four things the L4 cells must inherit, and one ruling I would like:**

1. **One scene per process.** Enforced in `l4_shoot.gd`. The H dispatch owns the four-cell contact
   sheet — **it must shoot four processes, not one**, or its own P-2 numbers are contaminated.
2. **L4a must restore the `godot_mcp` plugin line** in the lab `project.godot` (verbatim text in
   a comment at the edit site; original at `evidence/l4/project.godot.PRE-L4PREP`), and must set
   the four `GODOT_MCP_*` env vars or the addon dials `ai-game.dev` before any tool call.
3. **Shadow spill is the differ's one lying direction** (§6.4), and it lies toward false
   conviction. Any cell reporting P-2 damage should check the mask boundary first.
4. **The L3 artifact index needs amending** — `project/tcp_l3b_*` are now at `prep/l3_residue/`.

**The ruling I would like: whether §4 amends L2's P-2 finding.** L2 recorded "a Pro-authored scene
does not round-trip through Pro" and attributed it to `add_scene_instance`/`set_owner_recursive`.
I have now produced the same duplication from a plain headless GDScript builder with no MCP server
running. **The observation stands; the attribution looks too narrow.** That matters for how P-2 is
read in three days' time: if Pro damages `scene_before`, the question "is this Pro, or is this
Godot?" now has a measured prior, and it is not the one the program is carrying. That is above my
seam.

**Honorable-fallback status (L-F/L-G):** nothing hit a ceiling needing one. The three defects are
named with their exact blocking artifacts — the pack-probe table (§4), the six-render sha pattern
(§6.1) and the `editor_settings` mtime (§9.1) — and each was routed around rather than worked
around.

---

## Artifact index

**Report:** `agentic_orchestration/drax/notes/2026-07-25-tcp-l4-prep-report.md`

| Artifact | Path |
|---|---|
| **THE CONSTANTS FILE — all three cells read this** | `~/Games/mcp-lab/evidence/L4_KIT_CONSTANTS.md` |
| **THE FROZEN SUBSTRATE** (sha `d45db0f5…`, mode 0444) | `~/Games/mcp-lab/project/scene_before.tscn` |
| **Calibration evidence** | `~/Games/mcp-lab/evidence/l4/CALIBRATION.md` |
| Diff instrument | `~/Games/mcp-lab/prep/l4_diff.py` |
| Capture rig (shared, TCP-8) | `~/Games/mcp-lab/project/l4_shoot.gd`, `l4_shoot.tscn` |
| **`scene_before` at `__box`** | `~/Games/mcp-lab/evidence/l4/frames/SCENE_BEFORE__box.png` |
| Prop verification (raw vs textured) | `~/Games/mcp-lab/evidence/l4/frames/PROP_brazier04_raw_vs_textured.png` |
| Projection check | `~/Games/mcp-lab/evidence/l4/calib/ZEROPOINT_PROJECTION_CHECK.png`, `_projcheck_exact.png` |
| Zero point | `~/Games/mcp-lab/evidence/l4/calib/ZEROPOINT_DIFF.json`, `ZEROPOINT_DIFFx4*.png` |
| Non-zero point | `~/Games/mcp-lab/evidence/l4/calib/NONZEROPOINT_DIFF.json`, `NONZEROPOINT_DIFFx4*.png`, `_nonzero_crop.png` |
| Determinism evidence (6 + 6 renders) | `~/Games/mcp-lab/evidence/l4/calib/noise_p*.png`, `calib2/q*.png`, `calib2/solo*.png` |
| Measured natives | `~/Games/mcp-lab/evidence/l4/MEASURED_NATIVES.txt` |
| Build log + round-trip proof | `~/Games/mcp-lab/evidence/l4/BUILD_scene_before.txt` |
| **TCP-20 fingerprints** | `~/Games/mcp-lab/evidence/l4/TCP20_FINGERPRINT_{BEFORE,AFTER}.txt` + `TCP20_MANIFEST_darkfortress_{BEFORE,AFTER}.txt` |
| Fingerprint tool (reusable, now covers the shared Godot config) | `~/Games/mcp-lab/prep/fingerprint_product_repo.sh` |
| Lab `project.godot` original | `~/Games/mcp-lab/evidence/l4/project.godot.PRE-L4PREP` |
| **FORBIDDEN — the builder + prep tooling** | `~/Games/mcp-lab/prep/FORBIDDEN_do_not_place_in_project/` |
| L3 residue relocated out of the project | `~/Games/mcp-lab/prep/l3_residue/` |
| Nudge script (recreates the non-zero calibration scene) | `~/Games/mcp-lab/prep/make_nudged_calibration_scene.py` |
| Uninstall procedure (updated) | `~/Games/mcp-lab/UNINSTALL.md` |
| Import logs | `~/Games/mcp-lab/logs/l4/` |

**Signed:** drax, 2026-07-25 (presentation seam).
