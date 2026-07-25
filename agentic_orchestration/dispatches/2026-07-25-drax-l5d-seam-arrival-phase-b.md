# DISPATCH — TCP-L5-D: mode (ii) SEAM ARRIVAL, **Phase B** (build)

**From:** gandalf (`RUN-CONDUCTOR`) · **To:** drax (presentation seam) · **Date:** 2026-07-25
**Phase A:** `drax/notes/2026-07-25-tcp-l5d-seam-arrival-phase-a-report.md` + `SITING_PLAN.md`
**Gate cleared:** **OWNER-EYE ① — Matt ruled all three flagged calls.** Build.

## §0 — Matt's rulings, verbatim

- **R-1 — the wall.** *"Chosen wall works for me. Regarding camera angle, let's continue to use this
  one for now. It could be that we adopt grim dawn's later but for now let's use this one unless
  there is a specific reason not to."* → **north wall bay `0_3` CONFIRMED, and `__box` is the
  judging framing for Phase B and for every (i) cell.** Your R-1 veto condition is therefore closed:
  the camera the design was optimized against is the camera it will be judged in. (A future
  Grim-Dawn-register camera is queued as a program item, not this lap's business.)
- **R-3 — the portal.** *"an opening is fine."* → **an opening, not a door.** No leaf, no hinge, no
  door furniture. Continuity over boundary.
- **R-7 — method.** *"agreed."* → **H, no wire.** Your authoring clock continues from 27.8 min.

## §1 — Build the plan you filed

`SITING_PLAN.md` §1 is the spec now, in your own measured numbers. Ship all seven register cues as
stated. R-4 (inherit materials by matching wall normal) and R-5 (own `OmniLight3D`, `InteriorPool`'s
colour and attenuation, its own range) stand un-vetoed — build them.

**Substrate:** unchanged and unchangeable — sha `d45db0f5…de8522de1966`, mode 0444; verify at start
and end. Save to your own output path.

## §2 — The gates, with the amendments your Phase A forced

1. **RELOAD CENSUS** — through the engine, not a text parse. Expected-vs-actual node counts;
   **removals proven absent**; duplicates (TCP-31 flatten idiom binds — declare instance-vs-flatten);
   untextured survivors. **The orphaned-collision clause is satisfied WITH ITS REASON STATED** —
   empty by construction because the substrate has none. A check that cannot fail is not allowed to
   pass silently (L-L).
2. **★ THE FLOOR HOLE — close it.** Your §2.4: the removal exposes a 0.45 m gap in the walking
   surface. Fixing it is part of the build, and **how you fix it is a recipe clause** — every door in
   every future room inherits this. State the mechanism.
3. **★ G4 WALKABILITY** — 0.4 m radius × 1.7 m capsule, room-A centre → chamber centre, through the
   opening, no penetration. **The substrate has zero collision, so generate it** (trimesh from
   visible geometry) or use the kit's proxies where they exist — and **measure against the PROXY,
   never the render: the kit's collision hole is 4.9 cm narrower than its visible one.** The sweep
   artifact ships. This is the program's first gate about play rather than picture; if it fails,
   that is a finding, not a defect.
4. **THE THREE-SURFACE DOOR MODULE** — your finding, not the constants file's: override all three,
   or the architrave ships as an untextured blob at eye level.
5. **FRAMES (L-A)** — the **through-the-opening money frame** (camera in the crypt, opening in
   frame, chamber legible through it) + `__box` establishment. Diagnostic frames are named for **the
   variable they hold constant** (TCP-36 ①).
6. **DESCRIPTIVE DIFF** vs `SCENE_BEFORE__box.png` using `prep/l4_diff.py` **unmodified** — evidence,
   no pass/fail bar this cell. **TCP-39 ③ binds: the diffed scene contains no animated occupant and
   no temporal accumulator, or you declare a tolerance.** Equality diffing requires a scene with no
   clock in it.
7. **VACATE** — TCP-27 ① + TCP-34 ④: bank frames, verify a byte-identical re-render, relocate
   outputs to `prep/l5d_residue/`, `user://` included. Project dir as clean as you found it.
8. **BLAST RADIUS** — substrate sha + 0444; `reincarnated-godot` by **git attribution** (the
   quilt-fix dispatch has now CLOSED with commits `ce1c1af`/`188fd27`/`398609c`; the uncommitted
   `project.godot` `mesh_lod` line predates all of this and is not yours). A concurrent L6-PREP cell
   runs in `~/Games/mcp-lab/l6prep/` — **not your floor, no interaction.**

## §3 — Report

Close the authoring clock (total, thinking included — TCP-32 says this is the number that matters).
Log every build-time ruling veto-open. **Name anything in this dispatch that steered you** — that
sentence has caught a conductor defect in six consecutive cells and I would rather it caught a
seventh.

**Report to:** `agentic_orchestration/drax/notes/2026-07-25-tcp-l5d-seam-arrival-phase-b-report.md`
**HALT to gandalf:** any need to modify substrate, shoot rigs, or differ; any finding that re-scopes
the lap or the contract the (i) cells will be handed.
**Honorable fallback (L-F):** ship the attributed blocker and the frame anyway.

**Signed:** gandalf, 2026-07-25 (`RUN-CONDUCTOR`).
