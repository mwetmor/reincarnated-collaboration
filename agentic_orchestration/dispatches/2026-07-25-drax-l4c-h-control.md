# DISPATCH — TCP-L4c: the **H control** (headless GDScript builder)

**From:** gandalf (`RUN-CONDUCTOR`) · **To:** drax (presentation seam) · **Date:** 2026-07-25
**Program:** `agentic_orchestration/gandalf/notes/2026-07-24-tool-capability-program-charter.md`
**Lap charter (six clauses, P-1..P-6):** `agentic_orchestration/gandalf/notes/2026-07-25-tcp-l4-expansion-bakeoff-charter.md`
**Cells already closed:** L4a (W-MUR) PASS · L4b (W-PRO) PASS

---

## §0 — What this cell is, and the honest limit on what it can prove

**H = a plain GDScript file run under `godot --headless --script`.** No MCP server, no addon swap, no
wire. It opens the frozen substrate, adds the dais, saves to its own output path. That is the whole
method, and it is the control the other two cells are measured against.

**Rubric diff (law L-I — say out loud what falls out).** This cell measures **what the H route costs
and produces on an expansion task with the answer already specified in numbers.** It says **nothing**
about design arrival — H requires a human or agent who already knows the geometry to write it down.
That is mode (ii) and it is not this lap. **Do not let an H win here be read as "H is the production
route."** It is evidence about execution cost, not about authoring.

## §1 — ★ THE BLIND-CONTROL PROTOCOL — the load-bearing section, read it twice

You are a **fresh spawn with no memory of L4a or L4b.** That is not an accident, it is the control.
Two solved scenes sit on disk containing **every placement the spec asks for, already correct.**
Reading either one turns this cell from *authoring* into *transcription* and destroys the comparison.

**FORBIDDEN — do not open, grep, or read these, and do not read anything that quotes them:**

| | |
|---|---|
| `~/Games/mcp-lab/prep/l4a_residue/scene_l4a_wmur.tscn` | W-MUR's solved scene |
| `~/Games/mcp-lab/prep/l4b_residue/scene_l4b_wpro.tscn` | W-PRO's solved scene |
| everything else under `prep/l4a_residue/` and `prep/l4b_residue/` | verifiers, probes, `.tres` meshes carrying the spec's arithmetic |
| `agentic_orchestration/drax/notes/2026-07-25-tcp-l4a-wmur-run-report.md` | **your own prior note — carries the solved numbers** |
| `agentic_orchestration/drax/notes/2026-07-25-tcp-l4b-wpro-run-report.md` | **same** |
| `~/Games/mcp-lab/evidence/l4/l4a/**` and `evidence/l4/l4b/**` | frames, plans, censuses |

**That fifth and sixth row are the real trap.** Your session-start discipline says read your own
recent notes. **Here it would hand you both answers.** Skip that step for this cell and say in your
report that you skipped it.

**PERMITTED, and these are H's legitimate advantages — use them freely:**

- `~/Games/reincarnated-godot/scripts/kit_replica_level.gd` — the production room builder. Its
  constants and conventions are H's ancestry and reading it is exactly what a real H author would do.
- `~/Games/mcp-lab/evidence/L4_KIT_CONSTANTS.md` — handed to all three cells.
- `~/Games/mcp-lab/project/scene_before.tscn` — the substrate. **Read it to derive what was NOT
  handed:** where the far (−Z) wall sits, its inner-face Z, floor extent, node names. All three cells
  had to do this.
- The shoot rigs already in `project/`: `l4_shoot.gd` (TCP-23 — refuses a second scene per process),
  `l4_detail_shoot.gd`, and `prep/l4_diff.py` (the calibrated differ, **unmodified**).

**Bank your first prompt-to-self before any build work**, verbatim, to
`~/Games/mcp-lab/evidence/l4/l4c/FIRST_INTENT_BANKED.md`, and **declare every file you read** in the
report. Both other cells did this; it is what makes the comparison legible.

## §2 — The spec: unchanged, held constant, and one clause you must NOT fix

**Charter §2, all six clauses, identical to L4a and L4b.** Platform 6.0×4.0×0.6 m centred X=0, back
edge flush to the far wall's inner face; four steps 0.15 rise × 0.40 run, 1.2 m wide; two pillars
inset 0.5 m at the front corners; two props symmetric about X=0; **NON-DESTRUCTION**; `__box` camera.

**⚠ Clause 2 places the two stair flights at the dais's +X and −X ends, ascending −Z — i.e. entirely
OUTSIDE the platform footprint, arriving at its back corner.** That is architecturally poor and it is
**gandalf's spec defect, already recorded.** Both other cells built it as written. **Build it as
written.** Do not improve it. A control that silently corrects the spec is not a control. Note the
defect in your report if you like; do not act on it.

## §3 — Three things that are new since the other two cells ran

1. **★ A RELOAD-FROM-DISK STRUCTURAL CENSUS IS NOW MANDATORY, not optional.** L4b shipped **four
   exactly-co-located duplicate meshes** — 318 nodes against 314 expected, 4 untextured — and **a
   rendered frame was structurally incapable of catching it** (the duplicate hides behind its own
   original; the C1→C2 change mask showed the props as unchanged black silhouettes). Frames catch what
   changes the picture; a census catches what changes the file. **Run both.** The census must **reload
   the saved scene through the engine**, not parse the `.tscn` text — whether Godot double-creates a
   node is an engine behaviour, not a text property.
2. **P-2's passing floor is ~30 LSB pixels, NOT zero** (TCP-27 ②). PREP's calibrated zero is a
   calibration figure. A legitimate addition moves shadow at the mask edge. L4a measured 30 px at
   delta 1; L4b measured 59. **Publishing prep's 0 as the bar would convict an honest cell.**
3. **★ SCORE THE ROOM-COHERENCE AXIS (TCP-28), and report it per module.** Does your addition adopt
   the conventions of the room it joins — **module scaling, material/texture density, node naming**?
   This axis exists because the six clauses passed both cells while being blind to the differences
   Matt named in ten seconds. For reference, and this is a *measurement to reproduce or diverge from,
   not an answer to copy*: the room's own corner pillars stand at `PILLAR_WORLD_FOOT = 1.082276 × 0.62
   = 0.671011 m`, and `PILLAR_WORLD_H = WALL_H × 1.02`. **Whether H adopts that is the finding.**

## §4 — Pre-registered predictions (pinned before the cell runs; it cannot move its own goalposts)

- **P-C1 — H completes in ONE cycle.** Both wires needed **three**. *High confidence.* If H needs two
  or more, that is a large finding and the reason must be attributed.
- **P-C2 — H passes P-2 trivially**, because it never mutates existing nodes. A FAIL here would be
  very interesting.
- **P-C3 — DECISIVE. The duplication hazard FIRES ON H TOO.** TCP-24 established the mechanism is
  **Godot's `PackedScene.pack()`**, not any tool's. If H instances FBX sub-scenes and saves a `.tscn`,
  it should duplicate exactly as Pro did. **If H duplicates, the hazard is universal and both wires
  were partly exonerated. If H avoids it, HOW it avoids it is the single most transferable thing this
  lap produces.** Note that our production idiom sidesteps this entirely by building at runtime and
  never saving a `.tscn` — if you take that route, say so, because it changes what the cell measures.
- **P-C4 — H scores highest on ROOM-COHERENCE**, because it can import the constants directly rather
  than infer them. Predict it lands `PILLAR_WORLD_FOOT` exactly, as W-PRO did and W-MUR did not.
- **P-C5 — wall-clock under one tenth of either wire.** Record it honestly, including authoring time,
  not just execution time. **Authoring time is the number that matters** and it is the one a wire
  comparison usually hides.

**Every prediction resolves to a recorded fact. A FAIL is a finding, not a terminal event (L-G).**

## §5 — Exit predicate

1. Six clauses measured, each with the number that resolves it.
2. **Frames at `__box` + the detail crop**, plus the four conformance close-ups. L-A binds.
3. **The reload census**, with expected-vs-actual node counts and any untextured survivors.
4. P-C1..P-C5 each resolved to a recorded fact, or marked `UNRECOVERABLE`.
5. **ROOM-COHERENCE scored per module** with measurements.
6. P-2 via `prep/l4_diff.py`, **unmodified**, against `evidence/l4/frames/SCENE_BEFORE__box.png`.
7. **TCP-27 ① vacate** — bank frames + diff, verify a byte-identical re-render, then move outputs to
   `prep/l4c_residue/`. The project dir ends as clean as you found it.
8. **Blast radius** — `scene_before.tscn` still `d45db0f507f6b835e14447c9ceb7e7e6bd645e070bc1fe1241dd6e8522de1966`,
   still mode 0444. `reincarnated-godot` byte-unmodified, verified by TCP-20 fingerprint (not by
   `git status`, which is structurally blind to the ignored tree).
9. **Your declared read-list** per §1.

**Honorable fallback (L-F):** if H cannot satisfy a clause, ship the attributed blocking artifact and
the frame anyway. An attributed failure is a PASS; only an unattributed one fails.

## §6 — Conductor interface

- **Yours to rule, logged, veto-open:** how the builder is structured; whether to instance FBX or
  flatten (**declare which, it determines P-C3**); mesh-vs-module choice for platform and steps;
  which two props; census implementation.
- **HALT to gandalf:** any need to modify `scene_before.tscn`, `l4_shoot.gd` or `l4_diff.py`; any
  finding that changes what L5–L7 can attempt; **any accidental read of a §1-forbidden file — declare
  it immediately rather than continuing, a contaminated control declared is worth more than a clean
  one asserted.**
- **HALT to Matt:** nothing anticipated.

**Report to:** `agentic_orchestration/drax/notes/2026-07-25-tcp-l4c-h-control-run-report.md`

---

**Signed:** gandalf, 2026-07-25 (`RUN-CONDUCTOR`). Three consecutive cells have had charter defects
found by the executor and reported rather than worked around — L4's own scratch-clone premise, the
unsatisfiable zero-diff bar, the props-vs-modules naming trap. **This charter's most likely defect is
§1: I may have failed to name a file that leaks the answer.** If you find one, say so before you read
it.
