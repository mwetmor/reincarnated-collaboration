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

---

## Completion record — PHASE B

**Executed by:** drax · **2026-07-25** · **Status: BUILT. All eight gates met. G4 PASSES.**

**Authoring clock: Phase A 27.8 min + Phase B 23.3 min = 51.1 min (0.85 h) for the whole cell**,
thinking included. **Method H throughout both phases — no wire, so no swap and no transport.**
Phase B ran `20:51:23Z → 21:14:40Z`, stopping where Phase A's clock stopped — deliverables complete
and substrate re-verified — with report authoring outside it, as in Phase A. **Un-truncated
wall-clock to the commit landing: 27.6 min** (cell total 55.4 min); both numbers are in the report
so the smaller one is not hiding anything. Five Godot processes, one scene each (TCP-23), plus two
repeat runs for the determinism checks.

**Report:** `agentic_orchestration/drax/notes/2026-07-25-tcp-l5d-seam-arrival-phase-b-report.md`
**Build:** `~/Games/mcp-lab/prep/l5d_residue/l5d_scene_after.tscn` (sha `c7b9e950…`), 330 nodes.
**Evidence:** `~/Games/mcp-lab/evidence/l5/l5d/` — 3 frames, diff set, `RELOAD_CENSUS.txt`,
`G4_SWEEP.json`, `BUILD_LOG.txt`, 4 rigs.

### The build

296 − 2 + 36 = **330 nodes.** Opening in north bay `0_3` per Matt R-1; an **opening, not a door**,
per R-3 — no leaf, no hinge, no furniture. Chamber 5.00 × 3.75 on the crypt's own 1.25 grid, at the
crypt's floor height, from the crypt's own modules. **Zero new materials and zero new shaders in the
saved `.tscn`** (26 ShaderMaterial / 8 StandardMaterial3D / 6 ext_resource — identical to the
substrate), and only **two** new meshes: the opening module and the half-width panel, the only two
modules the substrate does not already carry inline. R-4 and R-5 built as filed.

### The gates

1. **Census** PASS — through the engine. 296→330; MeshInstance3D 288→321; holders 196→208 /
   84→101 / 8→12, all as predicted. **Removals proven absent by path AND by volume** (name-absence
   is weak: a renamed survivor passes it). **TCP-31: FLATTEN declared** — 0 nodes below root carry
   `scene_file_path`, 0 duplicate names, 0 pairs sharing mesh+transform. **0 untextured surfaces**
   across all 321 mesh instances.
2. **★ FLOOR HOLE — CLOSED**, and the mechanism is a rule, not a patch: **the new room's floor
   plate runs to the NEAR face of the shared band — the old room's floor edge — so it passes under
   the full 0.45 m of masonry.** Plate is `z [−12.50, −8.75]`, not `[−12.50, −9.20]`. Proved three
   ways: 0.4500 m uncovered before the chamber, 0.0000 m after (both builder assertions), and
   **1201 downward physics rays over the whole walk: 0 with no floor, max step 0.000000 m.**
3. **★ G4 WALKABLE = TRUE.** 320 generated trimesh bodies + the **authored proxy** for the opening;
   the render mesh excluded from the physics world entirely. `cast_motion` safe fraction
   **1.000000**; **0 of 1064** stations blocked at 1 cm; **clear width 1.9544 m** measured, against
   the proxy's independently measured 1.9553 (agreement **0.9 mm**) and the visual 2.0042. Capsule
   needs 0.800 → margin 1.155 m. Declared 0.01 m controller skin.
4. **Three-surface door** — all three overridden; the census re-checks it per surface.
5. **Frames** — money frame (camera in the crypt, both jambs and the lintel in shot, chamber floor
   running out through the opening), `__box` establishment shot with `l4_shoot.gd` **unmodified**
   (camera eye matches `l4_diff.py`'s constant exactly), and the sweep artifact.
6. **Diff** — `l4_diff.py` unmodified. **6.476 % of pixels changed, all inside ONE contiguous box
   `x[1095,1664] y[0,596]`** — exactly where the opening and chamber are. The other 93.5 % of the
   frame is byte-identical. **TCP-39 ③ satisfied, no tolerance declared:** 0 animated nodes, no
   TAA/SDFGI/SSAO/volumetric fog (the fog present is depth fog), and a fresh-process re-render is
   **byte-identical** (`4f51d447…`).
7. **Vacate** — project dir file inventory **byte-for-byte identical to cell start** (verified by
   listing diff); `user://logs/` emptied into `prep/l5d_residue/user_logs/`.
8. **Blast radius** — substrate `d45db0f5…` / **0444** verified at start AND end; `l4_shoot.gd` and
   `l4_diff.py` unmodified; `l6prep/` never entered; `reincarnated-godot` HEAD `81eea9d`→`398609c`
   (the quilt dispatch's own commits) with `project.godot`'s `mesh_lod` diff **byte-identical to the
   Phase-A baseline**. **No HALT.**

### Findings

1. **★ `.tscn` stores basis ROWS, not columns — and SITING_PLAN §3 says the opposite.** The
   sentence I wrote to guard against the transpose trap is itself transposed. Worse: the 12-float
   `Transform3D` form **has no GDScript constructor at all**, so any script authoring transforms is
   forced to translate the text. **6 of my 8 transcribed bases passed a transposed reading** —
   their off-diagonals are O(1e-7), below tolerance — and only the two ±X wall bases caught it. A
   mirrored chamber was two bases away from shipping. The fix that worked is structural, not
   careful: **harvest bases from the live node, never retype, keep the transcription only as a gate.**
2. **★ G4's first clearance search measured my probe, not the doorway (L-K class).** Bisecting
   capsule radius returned 0.8595 m — which is exactly where a `height ≥ 2·radius` capsule's own
   bottom re-enters the floor (0.85949, to four decimals). A capsule cannot measure a hole wider
   than its height permits. Re-asked with a 1.70 m box of free width: 1.9544 m.
3. **The first G4 run declared the floor a wall** — all 1064 stations blocked including the middle
   of an empty room, because feet-on-floor counts as penetration. Needs a declared controller skin.
4. **Two census checks were wrong and both corrections are load-bearing** — "the prism holds the
   opening and nothing else" forbids the floor-hole repair; "far band face = −12.95" was measuring
   the corner topper's legitimate 0.117 overhang.
5. **Phase A §0.3 was half wrong about the near walls.** `occlude = 0.0` on every wall material, so
   the east run is *not* faded — it is configured to vanish when a runtime driver fires. South is
   blacked out by a different mechanism. The Phase A **conclusion** survives (both are camera-near);
   only the reason was wrong. Verified by pixel: the chamber's +X wall (16.8, 18.7, 23.7) reads as
   the crypt's own +X wall (25.1, 29.8, 40.0), which is byte-identical before and after.
6. **The declared light spill, measured:** +11.5 RGB at the threshold, +2.0 at 1.75 m in, **exactly
   0 from 2.75 m inward.** Warm-tinted, matching the copied colour. The addition's light, not damage.
7. **Builder is byte-deterministic** except Godot's per-session `unique_id` (72 lines = 36 nodes × 2).

### New rulings, all veto-open

R-8 chamber nodes live in the substrate's own role holders with a `Ch` prefix (a separate holder
would encode "different place" in the tree) · R-9 collision generated at sweep time, not shipped ·
R-10 the opening is measured against the kit proxy, its render excluded from physics · R-11
`ChamberPool` range 5.0, the only authored number, set so chamber floor-centre illuminance is 95.4 %
of the crypt's · R-12 half-panel seam forced symmetric at `z = −11.25` on both side walls.

### Steer-check — what in this dispatch steered me

**§2.3 hands my own Phase-A finding back as a binding constraint.** Legitimate, but it makes that
finding unfalsifiable: had my proxy measurement been wrong, §2.3 would have instructed me to
preserve the error. I re-measured independently and it survived — because I checked, not because
the dispatch allowed it. **Recommendation: mark a restated Phase-A finding as "your own, re-verify"
rather than as a given.** Second, milder: §2's numbered gate order is very close to my execution
order and I did not seriously consider another; **G4 should have run before the frames**, being the
gate most likely to fail and the most expensive to re-shoot around. What did *not* steer: §2.2's
"how you fix it is a recipe clause" specified the *form* of the answer without supplying it, which
is the useful kind of instruction and is why the floor-hole answer is written as a rule.

**Still open from Phase A:** `L4_KIT_CONSTANTS.md` §6 pins L4's brazier dressing decision inside
the natives file; it should be split before that file is handed to another (ii) cell.
