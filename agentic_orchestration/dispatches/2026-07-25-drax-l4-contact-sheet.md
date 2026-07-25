# DISPATCH — TCP-L4: the FOUR-CELL CONTACT SHEET (lap closeout)

**From:** gandalf (`RUN-CONDUCTOR`) · **To:** drax (presentation seam) · **Date:** 2026-07-25
**Program:** `agentic_orchestration/gandalf/notes/2026-07-24-tool-capability-program-charter.md`
**Lap charter:** `agentic_orchestration/gandalf/notes/2026-07-25-tcp-l4-expansion-bakeoff-charter.md` §5.1
**Cells closed:** L4a (W-MUR) PASS · L4b (W-PRO) PASS · L4c (H control) PASS

---

## §0 — Why this is a separate dispatch, and why you are no longer blind

Lap charter §5.1 assigned this sheet to **the H dispatch** — the one cell forbidden by its own §1 to
read `evidence/l4/l4a/**` and `evidence/l4/l4b/**`. **You escalated the conflict rather than
resolving it by reading, which was the right call and is now recorded as TCP-34 ③.**

**The blind period is CLOSED.** L4c is built, judged, reported and signed. Every forbidden path in
that dispatch is **now open to you** — reading a solved scene cannot retroactively contaminate a
control that has already shipped. Read whatever you need.

**Nothing is re-rendered.** TCP-27 ① rules this sheet is assembled from **banked frames**, and TCP-23
forces one scene per process so the cells were never shot together anyway. **This is image
composition over PNGs already on disk. Do not open Godot. Do not touch the wire. Do not touch
`scene_before.tscn`.**

## §1 — What the sheet is FOR, and it is not decoration

**Matt's judgment is the instrument this lap discovered.** Shown L4a and L4b side by side he said, in
ten seconds: *"The only differences I can see are stair texture and pillar size. The PRO pillars are
wider."* **Both were true, both were measurable, and neither was in the six clauses that PASSED both
cells.** That observation became TCP-28 and the standing ROOM-COHERENCE axis.

**So build the sheet that lets him do that again, harder, across four columns instead of two.** If
the sheet requires a table to interpret, it has failed (L-A corollary 2).

## §2 — The composition

**Column order, left to right, always:** `scene_before` · **W-MUR (L4a)** · **W-PRO (L4b)** ·
**H (L4c)**. Label every column with cell + instrument, legibly, in the image.

**Row 1 — `__box`, the standing judgment framing (TCP-12).** The four whole-room frames.

**Row 2 — the detail crop.** `l4_detail_shoot.gd` parameters (aim `(0,1,-6)` dist 18 pitch −32 yaw 47
fov 20), which all three cells shot. `scene_before` has no dais, so its cell in this row is the empty
substrate at the same camera — **that is informative, not a gap; do not blank it.**

**Row 3 — ★ THE PILLAR STRIP, and this row is the reason the sheet is worth building.** A close-up of
the added pillars, one column per cell, **at matched framing and matched scale so the sizes are
directly comparable by eye.** This is the row that makes TCP-28's central number visible without
arithmetic: W-MUR shipped a **0.4291 m** footprint against the room's own **0.6710 m**; W-PRO and H
both landed **0.671010** exactly. **The `scene_before` column here is the CONTROL — the room's own
corner pillar, which is what "correct" looks like.**
- Prefer banked close-ups where a cell shot one at usable framing. Where none exists at matched
  framing, **you may re-shoot close-ups from the three residue scenes** (`prep/l4{a,b,c}_residue/`) —
  that is a permitted exception to §0's no-render rule, **on the strict conditions** that all four
  columns use **identical camera parameters**, each is **one scene in one process** (TCP-23), the
  parameters are **declared in the report**, and **nothing is written into `project/`** that is not
  vacated after (TCP-27 ①, **extended to `user://` per TCP-34 ④ — check it and clean it**).

**Row 4 — the diff strip.** Each cell's `|diff| ×4` against `SCENE_BEFORE__box.png`, from banked
`diff/` output. `scene_before`'s column is its self-diff (the calibrated zero). Annotate each with
its outside-mask number: **30 · 59 · 32 changed px, every one at channel delta 1.**

**Optional row 5, only if it costs you little — node naming.** A text panel per cell, same order:
W-MUR's `_MeshInstance3D_27179` / `_MeshInstance3D_27180` against W-PRO's `Dais_Pillar_L` and H's
`Dais/Pillar_0`. Matt did not need to see this to be right about the others; it is the third leg of
the coherence axis and it is free.

## §3 — Inputs (all banked, all on disk)

```
~/Games/mcp-lab/evidence/l4/frames/SCENE_BEFORE__box.png      the substrate
~/Games/mcp-lab/evidence/l4/l4a/**                            W-MUR frames + diff   (now open)
~/Games/mcp-lab/evidence/l4/l4b/**                            W-PRO frames + diff   (now open)
~/Games/mcp-lab/evidence/l4/l4c/frames/, .../diff/            H frames + diff
~/Games/mcp-lab/prep/l4{a,b,c}_residue/                       the three saved scenes (now open)
```

The three run reports are also open to you now and carry each cell's measured numbers for
annotation: `drax/notes/2026-07-25-tcp-l4{a-wmur,b-wpro,c-h-control}-run-report.md`.

## §4 — Exit predicate

1. **The sheet exists as one image** at `~/Games/mcp-lab/evidence/l4/L4_CONTACT_SHEET.png`, plus the
   per-row strips as separate images if the combined one gets unreadably large. **Readability beats
   completeness — if four rows at full width is a mess, ship the rows separately and say so.**
2. **Every column labelled in-image.** Every camera parameter for any re-shot close-up declared.
3. **Blast radius** — `scene_before.tscn` still `d45db0f507f6b835e14447c9ceb7e7e6bd645e070bc1fe1241dd6e8522de1966`
   and mode 0444; `reincarnated-godot` byte-unmodified by TCP-20 fingerprint if you render anything;
   `project/` and `user://` vacated (**TCP-34 ④ — `l4a_p6_roundtrip.tscn` is sitting in
   `~/Library/Application Support/Godot/app_userdata/tcp_l3_lab/` right now; clean it**).
4. **A short note** — `drax/notes/2026-07-25-tcp-l4-contact-sheet.md`, ≤1 page: what's in each row,
   any re-shoot parameters, anything you saw in the composed sheet that no individual cell report
   caught. **That last one is the point of compositing.**

**Honorable fallback (L-F):** if a row cannot be built honestly at matched framing, **ship the sheet
without it and say why.** A three-row honest sheet beats a four-row sheet with one row's scale faked.

## §5 — Conductor interface

- **Yours to rule, logged:** layout, resolution, label styling, whether rows ship combined or
  separate, close-up camera parameters, montage tooling.
- **HALT to gandalf:** any need to modify `scene_before.tscn`, `l4_shoot.gd`, `l4_detail_shoot.gd` or
  `l4_diff.py`; any finding that contradicts a number in the three run reports.
- **HALT to Matt:** nothing anticipated.

---

**Signed:** gandalf, 2026-07-25 (`RUN-CONDUCTOR`). This dispatch exists because you refused to build
a deliverable your own charter forbade you to build. **Four cells found four charter defects in a
row; every one was found by the executor, not the conductor.** Keep doing that.

---

## Completion record

**Executed:** drax (presentation seam), 2026-07-25. **Status: SHIPPED. No HALT triggered.**
**Report:** `agentic_orchestration/drax/notes/2026-07-25-tcp-l4-contact-sheet.md`

### Exit predicate, item by item

| # | Item | Status |
|---|---|---|
| 1 | The sheet exists as one image, plus per-row strips | **DONE — both.** `evidence/l4/sheet/L4_CONTACT_SHEET.png` (3314×3399, 5 rows) + `L4_ROW{1,2,3,4}_*.png` full-res. Rows shipped separately as well because ROW 3 wants 1:1. |
| 2 | Every column labelled in-image; every re-shoot parameter declared | **DONE** — cell + instrument + node count per column, every row. One render only (below). |
| 3 | Blast radius | **DONE** — `scene_before.tscn` `d45db0f5…` / 0444 unchanged; `project/` 71-file manifest byte-identical; `reincarnated-godot` TCP-20 fingerprint identical to `L4C_AFTER` in every section; `editor_settings-4.6.tres` not written; **`user://` vacated (TCP-34 ④)**; no processes, port 27435 closed. |
| 4 | A short note, ≤1 page, incl. what compositing caught | **DONE** — three findings, §3 of the note. |

### Rows

`scene_before` · **W-MUR (L4a)** · **W-PRO (L4b)** · **H (L4c)**, fixed left-to-right in all five rows.
**1** `__box` · **2** the detail crop · **3 ★** the pillar strip · **4** the diff strip (0 · 30 · 59 · 32)
· **5** node naming (built — it was free, as predicted).

### The one render

Row 3 needed **no** re-shoot: all three cells shot `*_DETAIL.png` on the same rig and placed the +X
pillar at the same world point, so **one identical pixel crop of the banked frames is already matched
framing and matched scale.** Only `scene_before` had no detail frame. Shot once, `l4_detail_shoot.gd`
**UNMODIFIED** (`1ee8572ff79a…`), at the parameters that rig declares — aim `(0,1,−6)` dist 18 pitch
−32 yaw 47 fov 20, echoed eye `(11.164016, 10.538547, 4.410613)`, identical to L4a's declaration.
One scene, one process. **Output written to an absolute path outside `project/`; nothing entered
`project/`, so nothing needed vacating.**

**§2's specified control subject was not buildable (L-F, applied to one cell, not the row).** The
room's own corner pillars are 97.3 % buried in the wall corners — a `0.11 × 0.11 m` nub of a
`0.671 m` pillar — and the nearest projects off the top of the detail frame at 25.8 m against the
dais pillar's 15.4 m. **There is no frame in any of the four scenes showing the coherence axis's own
reference at true size.** Substituted, at zero render cost: a computed **caliper** — the room's
`0.671010 m` footprint projected at `(2.5, ·, −5.25)` at `y = 2.10 m`, screen-x `1095.3 → 1283.9`,
**the same pixels in all four tiles.** W-PRO and H fill it exactly; W-MUR sits visibly inside it.

### What the composition caught that no cell report did

1. **★ The three cells built the stairs 4.000 m apart in Z.** L4a and L4b: step centres
   `−3.35/−3.75/−4.15/−4.55`, arriving at the dais **front** edge. L4c: `−7.35/−7.75/−8.15/−8.55`,
   arriving at the **back** edge against the wall. **X and Y identical; only Z differs, by exactly the
   platform's full depth.** Clause 2 fixes rise, run, width, X ends and climb direction and **never
   anchors Z** — both builds satisfy *"ascending toward −Z"* and **all six clauses passed both.**
   Corroboration already latent in the reports: **L4b and L4c each filed a "spec defect" against
   clause 2 and filed two different defects, because they had built two different staircases.**
   **This is TCP-28's structural defect, second instance, and 16× larger (4.000 m vs 0.242 m).**
2. **L4a's `CONTROL_pillar_room_vs_added.png` divides out the very difference Matt caught.**
   `l4a_pillar_compare.gd` assigns `Transform3D(Basis.IDENTITY, …)` to both clones, discarding the
   room pillar's `scale (1.5639, 1.0168, 1.5639)`. Measured on the banked frame the two pillars are
   **the same on-screen width to the pixel** (88/88, 54/54, 62/62). Correct for the texture question
   it was built for; **no L4a number is wrong**; but read as a room-vs-added control it certifies a
   size match that is 36.1 % out.
3. **Two lesser divergences the rubric also passed:** braziers at `x = ±1.2 / ±1.5 / ±1.0`
   (clause 4 pins symmetry and nothing else), and three different scene topologies — W-PRO's `+18`
   against W-MUR's and H's `+14` is four semantic wrapper `Node3D`s per prop where the other two
   flatten.

### For the conductor

**No HALT: nothing contradicts a number in the three run reports.** Finding 1 is three correct
numbers that were never compared; finding 2 is a caption that outruns its frame. Three items offered
to the ledger: (a) **clause 2 is Z-unanchored and the six-clause rubric is blind to a 4 m module
displacement — TCP-28's defect reaches placement *within* the addition, not just borrowed-module
scale**; (b) diagnostic frames should be named for the variable they hold constant, not the objects
in them; (c) the ROOM-COHERENCE reference is not photographable in its own room — decide once
whether future coherence judgments use a caliper overlay or a purpose-built reference plate.

**Artifacts:** `~/Games/mcp-lab/evidence/l4/sheet/` — `L4_CONTACT_SHEET.png` `289b7889…`,
`L4_ROW1_box.png` `f1f79ed8…`, `L4_ROW2_detail.png` `a3590417…`, `L4_ROW3_pillars.png` `32324133…`,
`L4_ROW4_diff.png` `2c6e1785…`, `SCENE_BEFORE_DETAIL.png` `798c6ff5…`, plus
`compose_contact_sheet.py` (the composer, reproducible, camera math inline).

**Signed:** drax, presentation seam, 2026-07-25.
