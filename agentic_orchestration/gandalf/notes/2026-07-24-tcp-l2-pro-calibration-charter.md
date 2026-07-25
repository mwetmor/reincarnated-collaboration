# TCP-L2 — PRO CALIBRATION (run charter)

**Program:** `2026-07-24-tool-capability-program-charter.md` — lap **L2**, class **T1 REPLICA** × mode **(i) held-constant spec**
**Conductor:** gandalf (`RUN-CONDUCTOR`) · **Executor:** drax (presentation seam) · **Status:** CHARTERED + DISPATCHED 2026-07-24
**Matt gate:** none. This is the only lap in the program with no open commitment-boundary.

---

## §0 — Intent, in one sentence

**Does Godot MCP Pro 1.15.1 measure a kit it has never seen, or only execute constants derived
elsewhere?** — and, secondarily, exercise the lap machinery once on the cheap instrument before we
spend the expensive one.

**Rubric diff against §0 (law L-I).** What falls out of the exit predicate: this lap says nothing
about *design* quality, nothing about iteration throughput, nothing about Pro on non-replica tasks.
It answers **one** question — author or executor — and produces one judgeable frame. Do not let a
PASS here be read as "Pro is good at building rooms."

## §1 — Why calibration, not competition (TCP-4)

L1 already told us the wire loses a replica race on latency arithmetic alone: ~280 instances ×
114–180 ms = **32–50 s of pure wire time** before a single decision, against M3's **1m37s for an
entire room including dressing and capture.** Running L2 to discover that again would be a wasted lap.

So L2 is reframed on the same logic that made drax calibrate `kit_measure.gd` against the reference
pack before trusting a single number out of it: **if Pro cannot reproduce a room we already have a
control for, nothing it does in L4–L7 can be trusted.** A FAIL here is not "Pro loses the race" — it
is "Pro's later results are uninterpretable." That is what makes this lap worth the time.

## §2 — Target and control

**One room. One new pack. The control is built in the same lap.**

- **Pack:** the 4th pack, **chosen by measured module compatibility, never by catalogue asset count**
  (law L-D / KRL-4 — L1's count-based ranking inverted the true difficulty order). Run
  `kit_measure.gd` across the candidate packs first, declare the measured wall/floor/pillar
  dimensions and the segment arithmetic against the 17.5 m room, then pick. **The measurement is the
  pick; it needs no ratification.**
- **Why a NEW pack and not R3 ancient-egypt** (amending my own recommendation in
  `2026-07-24-mcp-authoring-surface-audit.md` §5, and the reason matters): ancient-egypt's constants
  are already derived and committed in this repo, so a Pro agent pointed at it could **read the answer
  instead of measuring it.** That is the same contamination the L1 charter §4c guarded against when
  it forced M1 to run before M3 existed. P-B is only testable against a kit whose constants do not yet
  exist on disk.
- **Control:** an M3 (headless GDScript) build of the **same room in the same pack**, from the
  established pipeline. L1 measured this at **1m37s**. Build it *after* the Pro attempt, for the same
  contamination reason.

## §3 — Pre-registered predictions (pinned before results; the lap cannot move its own goalposts)

- **P-A — Pro creates the node graph.** `create_scene` → `add_node` → `add_scene_instance` →
  `update_property` → `save_scene` is a documented, complete assembly loop. *High confidence.*
- **P-B — DECISIVE. Pro cannot measure an un-instantiated FBX.** Pro has no bounds/AABB tool of any
  kind. But it *can* instantiate. **The test:** instantiate the pack's wall mesh into a scratch scene
  and call `get_node_properties`. **If it returns an AABB, Pro has a complete — if roundabout —
  measure→build loop and is an AUTHOR. If it does not, Pro is an EXECUTOR** of constants derived
  elsewhere, and every later Pro lap must be read as "given the right numbers, can it build."
- **P-C — the escape-hatch trap.** If measurement requires `execute_editor_script`, the verdict is
  **"transport, not rival"** — Pro is writing GDScript over a wire, which is M3 with added latency,
  not a rival to M3. **Record whether the hatch was needed; it changes the verdict class.**
- **P-D — ≥32 s of pure wire latency** for the instance placements alone. Log per-call ms and total
  wire time separately from think time.

**Every prediction resolves to a recorded fact. A FAIL is a finding, not a terminal event** (law L-G
— ceiling-finding is a PASS; only an *unattributed* failure fails).

## §4 — The instrument swap, and its restore predicate

**All three wires install to the same path** — `res://addons/godot_mcp/`. The incumbent occupies it;
Pro carries ~70 hardcoded refs to it; Murzak's installer downloads into it. **Only one wire may be
installed at a time.** *(New program law **L-J**; TCP-9.)*

Therefore this lap **swaps**, and the swap is part of the run:

1. **Record the incumbent's file inventory before touching anything** — count `.gd` files, hash the
   directory. Do not trust `plugin.cfg`.
2. Move the incumbent aside (do not delete). Install Pro. Run the lap.
3. **Restore, then VERIFY BY FILE COUNT.** The L1 hazard: `npx …--install-addon` reads `plugin.cfg`,
   sees the expected version, prints *"Addon is already up to date"* and exits **without an integrity
   check** — the installed addon was **3 `.gd` files against an expected 36**. A gutted addon never
   self-heals and reports itself healthy. **The restore predicate is the inventory from step 1
   matching byte-for-byte, not a version string.**
4. If restore fails, **HALT and report** — do not attempt repair-by-reinstall.

Work on a branch or a scratch clone; drax's call.

## §5 — Exit predicate

The lap is done when **all five** hold:

1. **A play-camera frame of the Pro-authored room** and **a play-camera frame of the M3 control**,
   same camera parameters, in a contact sheet (law **L-A** — no cell, table, JSON or prose substitutes
   for a picture; a presentation lap that produces no judgeable frame has not met its exit predicate).
2. **A pixel diff** of the two frames, with the same instrumentation L1 used to catch the transpose
   (whole-frame mean + named patch samples). L1's proof case stands: M2 loaded with **zero errors,
   zero warnings**, passed structural inspection completely, and was **only** caught by measuring
   pixels against a rendered control.
3. **P-A..P-D each resolved** to a recorded fact, with the evidence that resolved them.
4. **A latency ledger** — per-call ms, call count, total wire time, separated from think time.
5. **The restore verified by file inventory** (§4.3).

**Honorable fallback (law L-F — a control or a trace):** if Pro fails at any stage, **the M3 control
is still built and still captured**, and the lap ships the frame plus the attributed failure point.
L1's R1 established this shape: the room shipped a frame even though its method failed. **A lap that
ships no frame has failed even if its finding is interesting.**

## §6 — Conductor interface

- **In-run rulings** (drax may take, logged, veto-open): pack pick from measurement, room dimensions
  if the kit forces a different segment arithmetic, dressing substitutions **declared as substitutions**.
- **HALT to gandalf:** restore failure (§4.4); any need to modify a seam outside `reincarnated-godot/`;
  discovery that Pro's manifest disagrees with `docs/tools-reference.md` (that is an **L-B** event —
  manifest vs behaviour — and it is a finding worth more than the lap).
- **HALT to Matt:** nothing anticipated. If one appears, it is a charter defect; name it as one.

**Report to:** `agentic_orchestration/drax/notes/2026-07-24-tcp-l2-pro-calibration-run-report.md`

---

**Signed:** gandalf, 2026-07-24 (`RUN-CONDUCTOR`). Two charter defects were found in L1 by the
executor and reported rather than worked around — I7's unsatisfiable camera invariant and I4's
conflated clamp/clip numbers. **That is the behaviour I want again.** If something in this charter
cannot be satisfied, say so and ship the frame anyway.
