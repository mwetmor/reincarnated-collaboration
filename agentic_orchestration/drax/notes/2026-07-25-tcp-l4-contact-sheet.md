# TCP-L4 — the FOUR-CELL CONTACT SHEET (lap closeout)

**Dispatch:** `agentic_orchestration/dispatches/2026-07-25-drax-l4-contact-sheet.md`
**Executor:** drax (presentation seam) · **Conductor:** gandalf (`RUN-CONDUCTOR`) · 2026-07-25
**Status:** SHIPPED. Five rows, combined + four full-res strips. No HALT triggered.

---

## §1 — What shipped, and what is in each row

```
~/Games/mcp-lab/evidence/l4/sheet/
  L4_CONTACT_SHEET.png     3314 x 3399   all five rows, one image
  L4_ROW1_box.png          3940 x  728   full-res strip
  L4_ROW2_detail.png       3940 x  728   full-res strip
  L4_ROW3_pillars.png      2820 x 1408   full-res strip  ← the row that matters
  L4_ROW4_diff.png         3940 x  728   full-res strip
  SCENE_BEFORE_DETAIL.png  1920 x 1080   the one frame that did not exist (§2)
  compose_contact_sheet.py               the composer, reproducible
```

Both were shipped: the combined sheet is readable, and the rows are also separate because the
pillar row wants to be looked at at 1:1. **Column order is fixed in every row, left to right:**
`scene_before` · **W-MUR (L4a)** · **W-PRO (L4b)** · **H (L4c)**, labelled in-image with cell and
instrument, plus each cell's node count.

| row | what it is |
|---|---|
| **1 — `__box`** | the four whole-room frames at the standing judgment framing (TCP-12). All four banked. |
| **2 — the detail crop** | `l4_detail_shoot.gd` parameters, identical for all four. Three banked; `scene_before`'s shot once (§2). |
| **3 — ★ the pillar strip** | one identical pixel crop `x[1025,1365] y[285,895]` of ROW 2, ×2, with a computed matched-scale caliper (§3). |
| **4 — the diff strip** | `\|diff\| ×4` vs `SCENE_BEFORE__box.png` from banked `diff/` output. Annotated **0 · 30 · 59 · 32** changed px outside the mask, every one at channel delta 1. `scene_before`'s column is prep's `ZEROPOINT` self-diff. |
| **5 — node naming** | a text panel per cell, read off each saved `.tscn`, against the substrate's own grammar. |

## §2 — The one render, and its parameters

**Everything in rows 1, 3, 4 and the three instrument columns of row 2 is banked pixels.** Row 3
did **not** need a re-shoot: all three cells shot `*_DETAIL.png` on the same rig at the same
parameters, and all three put their +X dais pillar at the same world position `(2.5, ·, −5.25)`, so
**one identical pixel crop of the three banked frames is already matched framing and matched scale.**
That is the strongest available form — the pixels in row 3 are the same pixels each cell judged.

The only gap was `scene_before`, which had no detail-framed frame. Shot **once**:

```
rig      project/l4_detail_shoot.gd   UNMODIFIED   sha256 1ee8572ff79a5bb34eec18d10da84193506ee05393f53144d97b0e74b52b38ff
cmd      $GODOT_NET --rendering-driver metal --path project l4_detail_shoot.tscn --quit-after 400 \
           -- res://scene_before.tscn <abs-path-outside-project>/SCENE_BEFORE_DETAIL.png
params   aim (0.0, 1.0, -6.0)  dist 18.0  pitch -32.0  yaw 47.0  fov 20.0 (VERTICAL)
         near/far 0.02/2000   viewport 1920x1080  MSAA_4X SubViewport
echoed   eye     (11.164016, 10.538547, 4.410613)
         basis_x ( 0.681998,  0.000000, -0.731354)
         basis_y (-0.387558,  0.848048, -0.361404)
         basis_z ( 0.620223,  0.529919,  0.578367)
```

**Identical to the values L4a declared and L4b/L4c reused, digit for digit.** One scene, one process
(TCP-23). The output path is absolute and outside `project/`; **nothing was written into `project/`
at any point, so there was nothing to vacate.**

### The row-3 control column: the dispatch's specified subject is not photographable

§2 asked for the room's own corner pillar as row 3's control. **It cannot be shot at usable framing
and that is a finding, not a shortfall.** The room's pillars sit at `(±8.975, ·, ±8.975)` with the
wall inner faces at `±8.75`, so the part of a `0.671 m` pillar that is ever inside the room is a
`0.1105 × 0.1105 m` corner nub — **2.7 % of its footprint by area.** At the detail camera the nearest
one projects to `px (492, 100)` with its top at `py −258`, i.e. off the top of frame, at 25.8 m depth
against the dais pillar's 15.4 m. **There is no frame, in any of the four scenes, in which the
reference the whole ROOM-COHERENCE axis is defined against can be seen at its true size.**

**What I shipped instead, at zero render cost and full honesty:** an overlay **caliper** — the
`0.671010 m` room footprint projected through the declared camera at the dais pillar position
`(2.5, ·, −5.25)` at one declared height, `y = 2.10 m` (mid-shaft), giving screen-x `1095.3 → 1283.9`
(`188.6 px`). **The same pixels are drawn in all four tiles.** Computed geometry, not drawn by eye;
validated against the images (predicted left edge `1095.3` vs measured `1100` for W-PRO, `1129.2` vs
`1134` for W-MUR). One height rather than the whole-shaft envelope because the pillar leans ~9 px in
screen x across its height, and an envelope is tangent at two different heights and reads as slack
everywhere.

**It works.** W-PRO and H fill the caliper exactly. W-MUR sits visibly inside it with floor showing
on both sides. `scene_before` shows the caliper standing over bare floor.

## §3 — ★ What the COMPOSED sheet shows that no individual cell report caught

### ①  The three cells built the stairs in two different places, 4.000 m apart

Read off the three saved `.tscn` files, not off the reports:

| cell | step centres, Z | flight spans | arrives at |
|---|---|---|---|
| **L4a  W-MUR** | −3.35 · −3.75 · −4.15 · −4.55 | `z[−4.75, −3.15]` | the dais **FRONT** edge |
| **L4b  W-PRO** | −3.35 · −3.75 · −4.15 · −4.55 | `z[−4.75, −3.15]` | the dais **FRONT** edge |
| **L4c  H** | **−7.35 · −7.75 · −8.15 · −8.55** | **`z[−8.75, −7.15]`** | the dais **BACK** edge, hard against the far wall |

**X is identical in all three (`±3.6`). Y is identical (`0.075 / 0.15 / 0.225 / 0.3`). Only Z differs,
and by exactly 4.000 m — the platform's entire depth.** The flights are at opposite ends of the dais.

**No number in any report is contradicted.** Each cell reported its own Z correctly; L4a and L4b say
`−3.15 → −4.75`, L4c says `[−7.55,−7.15] … [−8.75,−8.35]`. **Nobody put the three numbers next to
each other.** L4c could not (blind); L4b's reconstruction compared only against L4a and found them
identical, which they are.

**Why the rubric passed both.** Clause 2 verbatim: *"Flanking stairs — one at each of the dais's +X
and −X ends, 4 steps, each 0.15 m rise × 0.40 m run, 1.2 m wide, **ascending toward −Z**."* It fixes
the rise, the run, the width, the X ends and the climb direction. **It never anchors Z.** Both builds
ascend toward −Z. Both are literally conformant. **Six clauses passed three cells and are blind to a
4 m displacement of an 8-node module.**

**And the sharpest corroboration is already in the reports, unnoticed:** *two cells filed a "spec
defect" against clause 2, and they filed two different defects.* L4b — *"a climber arrives level with
the dais top but standing off the slab in X."* L4c — *"climbing away from the room and arriving at
the dais's back corner, hard against the far wall. Whoever uses it walks up into a corner and turns
around."* **They are describing two different staircases.** Neither could see the other's.

**This is TCP-28's exact structural defect, second instance, found the same way — by composition,
not by measurement.** It is larger than the pillar finding: 4.000 m against 0.242 m.

### ②  L4a's own `CONTROL_pillar_room_vs_added.png` normalizes away the difference Matt caught

L4a §8 photographed the room's `Pillars/Pillar_0` beside its added dais pillar to settle the atlas
banding, and reported *"They are indistinguishable."* **Measured on that frame, the two pillars are
exactly the same on-screen width** — 88/88 px at y=300, 54/54 at y=350, 62/62 at y=400.

The mechanism is two lines of `prep/l4a_residue/l4a_pillar_compare.gd`:

```gdscript
var a: MeshInstance3D = room_src.duplicate()
a.transform = Transform3D(Basis.IDENTITY, Vector3(-1.2, 0.0, 0.0))
```

**`Basis.IDENTITY` discards the room pillar's `scale = (1.5639, 1.0168, 1.5639)`.** The clone is
rendered at module native — the same size as W-MUR's. For the texture question that is arguably the
*right* control (it isolates texture from scale), and **no number in L4a is wrong.** But the frame is
banked as `CONTROL_pillar_room_vs_added.png` under the sentence *"they are indistinguishable"*, and
**read as a room-vs-added control it positively certifies a size match that is 36.1 % out.** Row 3
exists precisely because that frame could not do row 3's job.

### ③  A third under-specification, minor, same class as ①

Clause 4 pins symmetry about X=0 and nothing else. The three cells placed the braziers at
`x = ±1.2` (L4a), `±1.5` (L4b), `±1.0` (L4c), at `z = −5.10 / −5.10 / −5.25`. **All three PASS.**
Visible in row 2 as three different spacings.

### ④  W-PRO's `+18` is four wrapper `Node3D`s, and it is a naming choice, not a defect

Row 5 makes the structural difference legible: 296 → **310 (+14)** for W-MUR and H, **314 (+18)** for
W-PRO. The four extra are `Dais_Pillar_L/R` and `Dais_Brazier_L/R` — a semantic wrapper `Node3D` per
prop holding the FBX-instance child. W-MUR and H both flatten. **Three instruments, three different
scene topologies for the same 13 visible meshes**, and clause 5 (non-destruction) is silent on all of
it because it only asks what was *not* changed.

## §4 — Blast radius

```
scene_before.tscn   sha256 d45db0f507f6b835e14447c9ceb7e7e6bd645e070bc1fe1241dd6e8522de1966   UNCHANGED
                    mode   -r--r--r-- (0444)                                                  PRESERVED
standing rigs       l4_shoot.gd d52975059230…  l4_detail_shoot.gd 1ee8572ff79a…
                    l4_diff.py 736ee06c2e40…                                                  UNTOUCHED
project/            71-file manifest BEFORE vs AFTER: byte-identical, nothing added or removed
reincarnated-godot  TCP-20 fingerprint L4C_AFTER vs L4SHEET_AFTER: every section IDENTICAL
                    Assets/ 98,823 files 041896a5…   dark-fortress 3,028 files 93645a4f…
                    addons/ 122 files ebd02e2e…      project.godot a76d666a…
                    .godot/ 131,796 files, mtime unchanged   tracked status b4e2f0ce…
editor_settings-4.6.tres  mtime 12:35:48 — BEFORE this session. Not written.
exit state          no Godot process, no gamedev-mcp-server process, port 27435 not listening
```

**`user://` vacated per TCP-34 ④.** `l4a_p6_roundtrip.tscn` (sha `ea31f704e032…`) was sitting in
`~/Library/Application Support/Godot/app_userdata/tcp_l3_lab/`. **Relocated, not deleted**, to
`prep/l4a_residue/` where the rest of L4a's residue lives behind its
`README_DO_NOT_PLACE_IN_PROJECT.md`. `user://` now holds only `godot-mcp-config.json` and `logs/`.

**One declared delta:** my single render rotated two Godot log files into `user://logs/`
(`godot.log`, `godot2026-07-25T13.59.47.log`, 761 B and 642 B). Benign, named rather than buried.

**No wire was opened. No addon was swapped. `scene_before.tscn` was never opened for write.**

## §5 — For the conductor

**No HALT.** Nothing contradicts a number in the three run reports; §3 ① is three correct numbers
that were never compared, and §3 ② is a frame caption that outruns its frame.

Three things worth a ruling or a ledger line:

1. **Clause 2 is Z-unanchored and the six-clause rubric is blind to a 4 m module displacement**
   (§3 ①). **Second instance of TCP-28's structural defect, and larger.** If TCP-28 stands as
   *"conformance clauses do not capture room coherence,"* this says the same defect also reaches
   **placement within the addition itself**, not just borrowed-module scale. Both instances were
   found by an eye on two pictures; neither by the rubric.
2. **A control frame's caption can outrun its control** (§3 ②). `CONTROL_pillar_room_vs_added.png` is
   a *texture* control that reads as a *size* control. Cheap fix for L5+: name diagnostic frames for
   the variable they hold constant, not for the objects in them.
3. **The reference for the ROOM-COHERENCE axis is not photographable in the room it belongs to**
   (§2). Any future coherence judgment against `scene_before` needs either a caliper overlay of the
   kind row 3 uses, or a purpose-built reference plate. Worth deciding once rather than per lap.

---

**Signed:** drax, presentation seam, 2026-07-25. One render, five rows, three divergences the rubric
passed anyway.
