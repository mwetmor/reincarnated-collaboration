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
