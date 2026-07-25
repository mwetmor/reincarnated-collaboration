# DISPATCH — TCP-L5a: build the seam with **W-MUR** (mode (i), blind)

**From:** gandalf (`RUN-CONDUCTOR`) · **To:** drax (presentation seam) · **Date:** 2026-07-25
**Cell:** L5a · **Method: W-MUR — the installed Murzak Godot-MCP wire. This is not negotiable; it
is the variable under test.**

## §0 — What this cell measures

**Execution fidelity, and what the WIRE costs to achieve it.** A contract exists. It is complete,
measured, and pre-registered. Your job is to satisfy it **through the wire** and to report honestly
what that was like — where the tool helped, where it fought you, and where it hit a ceiling.

**Ceiling-finding is a PASS (L-G). An attributed failure is a PASS (L-F). Only an unattributed one
fails.** If the wire cannot do something, the *finding* is the deliverable and the room is not.
Do not route around the wire to make the room look good — that destroys the only datum this cell
produces. If you must fall back to script for a step, **declare it, time it separately, and say
exactly which tool call could not be made.**

## §1 — The contract

**`~/Games/mcp-lab/evidence/l5/CONNECTION_CONTRACT.md`** — 65 predicates, read it whole before you
touch anything. It is your complete specification. Its §0 tells you how to read it.

**Two things about it you should know going in:**

1. **It deliberately does NOT specify the removal set.** It gives you the portal **volume** and the
   **invariants that must survive** (§6). *How you identify what to remove is your own problem and
   is one of this cell's real outputs.* Report your method.
2. **§14 lists what it deliberately leaves open.** Those are yours to decide and to log as rulings.
   Everything else is spec — meet it.

**`~/Games/mcp-lab/evidence/L4_KIT_CONSTANTS.md`** is your kit-native reference. It was scrubbed
2026-07-25: it carries kit natives only, and its §3 surface-count list is **explicitly not a
ceiling — count the surfaces on the mesh you are about to assign.**

## §2 — BLIND PROTOCOL — the forbidden list, enumerated

This cell is one of three building the same contract with different tools. The comparison is void if
you see another cell's answer. **Do not read, open, list, grep, or infer from:**

- `~/Games/mcp-lab/evidence/l5/l5d/**` — **anything** (SITING_PLAN, FIRST_INTENT, probe frames,
  MEASURED_DOOR_MODULES, rigs, frames)
- `~/Games/mcp-lab/prep/l5d_residue/**` — **especially `l5d_scene_after.tscn`**, which is the answer
- `agentic_orchestration/drax/notes/2026-07-25-tcp-l5d-*` — both phase reports
- `agentic_orchestration/dispatches/2026-07-25-drax-l5d-*` — both dispatches and their completion
  records
- `agentic_orchestration/gandalf/notes/2026-07-24-tool-capability-program-charter.md` — **the ruling
  ledger is an answer key** (TCP-34)
- `agentic_orchestration/gandalf/notes/2026-07-25-tcp-l5-seam-lap-charter.md`
- `evidence/l4/L4_DRESSING_DECISION.md`
- ★ **Your own prior notes from this date.** This is the L4c lesson and it is the one people trip
  on: *"read your own recent notes to get oriented"* **is the leak.** A previous drax session solved
  this exact problem. You are not that session. Orient from the contract.

**A contaminated control DECLARED is worth more than a clean one ASSERTED.** If you read something
on this list by accident — a grep that matched, a directory listing that showed you a filename —
**HALT, declare it in your report, and continue.** That is a PASS. Silence is the only failure.

**Declare your read-list** in the report: everything you opened, including things you opened and
found irrelevant.

## §3 — Method: W-MUR, and how to be fair to it

The installed wire is **Murzak Godot-MCP 0.19.1** (C#, 39-tool surface, ~8.32 ms mean call latency —
that figure is a prior cell's measurement, **treat it as a hypothesis and re-measure if it matters
to your account**). **L-J binds: one wire at a time.** W-PRO stays parked in its swap directory —
do not install it, do not look at it.

**Be fair to the instrument in both directions.** This program has convicted tools three times for
defects that belonged to Godot or to our own code (standing rule: an attribution to an instrument is
not final until tested against the engine and our own harness). If the wire produces a bad result,
**ask whether a plain script does the same thing** before you file it against the wire. Equally, do
not launder a real ceiling into a workaround and call the tool capable.

**TCP-31 flatten idiom binds** if you instance FBX sub-scenes into a saved `.tscn`: `PackedScene.pack()`
duplicates them. Declare instance-vs-flatten in your census.

## §4 — Clock (TCP-32 — this is the number that matters)

**Bank your authoring-clock start before any work.** Authoring time **includes thinking**, includes
reading the contract, includes composing tool payloads. Execution time is reported **separately**.
Prior cells have found execution to be a small single-digit fraction of the total; if this cell
inverts that, that is a finding about the wire.

## §5 — Exit predicate

1. **All 65 contract predicates evaluated** — each PASS / FAIL / `UNRECOVERABLE`, with its measured
   value. A FAIL with a number is a finding; a predicate silently skipped is not.
2. **Frames per contract §13**, rendered through the known-good L4 shoot rigs (**one scene per
   process — the rig refuses more**). `__box` is the judging framing (Matt ruling).
3. **The differ per §12, with the P-2 inversion honored: a ZERO diff is a FAIL** (nothing was cut).
4. **Your removal-targeting method, stated** — this is a headline output, not a footnote.
5. **Wire account:** what W-MUR did well, what it could not do, every ceiling with the exact call
   that hit it, and every fallback-to-script with its separate time.
6. Rulings logged veto-open · read-list declared · clock closed (authoring separate from execution).
7. **Hygiene:** substrate `~/Games/mcp-lab/project/scene_before.tscn` sha
   `d45db0f507f6b835e14447c9ceb7e7e6bd645e070bc1fe1241dd6e8522de1966`, mode 0444 — verify at start
   AND end. **Save to your own output path under `evidence/l5/l5a/`, never over the substrate.**
   Leave the project dir as you found it (inventory it at start).
8. **Name anything in this dispatch that steered you.** That sentence has caught a conductor defect
   in **nine consecutive cells** and I would rather it caught a tenth.

**Concurrency:** a drax cell is live in `~/Games/reincarnated-godot/` (hero foot-skate) — **not your
floor.** `~/Games/mcp-lab/harness/` and `~/Games/mcp-lab/l6prep/` are not yours this cell.

**Report to:** `agentic_orchestration/drax/notes/2026-07-25-tcp-l5a-wmur-report.md`
**HALT to gandalf:** any need to modify the substrate, the contract, the shoot rigs or the differ;
any contract predicate you believe is **wrong** rather than merely hard (say so — the contract has
already been corrected once for exactly that, and a predicate that convicts a legal answer is the
defect class this lap most needs to catch).

**Signed:** gandalf, 2026-07-25 (`RUN-CONDUCTOR`). The contract's own author filed a steer-check
against my brief and it was correct. Do the same to me.

---

## Completion record

**Executed:** drax, 2026-07-25. **Report:** `agentic_orchestration/drax/notes/2026-07-25-tcp-l5a-wmur-report.md`
**Build:** `~/Games/mcp-lab/evidence/l5/l5a/l5a_scene_after.tscn` sha256 `25530cc952dec799b22da62904a61cdafa0c4fe7f6b29b4f8e795be9322c9b0c`

**Clock (TCP-32).** Authoring **38 min 49 s** (22:02:53Z → 22:41:42Z, thinking + contract read +
payload composition included). Execution **≈ 1 min of machine time, ~2 % of total — not inverted**:
W-MUR build 2.993 s / 77 calls (ledger-exact), ~1.6 s of probe calls, 8 headless Godot runs at
0.29–0.56 s each (measured), 4 Metal renders, 4 s editor+relay cold start.

**Exit predicate.**
1. **All 65 predicates evaluated: 57 PASS · 8 FAIL · 0 UNRECOVERABLE**, each with a measured value.
   **None of the 8 FAILs is a build defect** — 5 are one contract-figure blind spot (§5.1), 3 are
   the mask/tolerance defects the contract pre-registered as its own most likely failure (§5.2–5.3).
2. **Frames** shot through the frozen rigs (shooter sha verified `d5297505…`): `__box` eye reads
   `(23.123901, 39.502224, 21.687008)` exact; money frame fully derived (`d = 2.81582`,
   pitch −7.0854°); F-4 re-render byte-identical.
3. **Differ, P-2 inversion honoured — the diff is NOT zero.** `changed_pixels = 134294`, which is
   *bit-for-bit the figure the contract attributes to the mode-(ii) cell*: two blind cells moved
   the same pixels. D-3 projection gate reproduced all six L4 hull vertices to **0.000 px**.
4. **Removal targeting (headline).** World-AABB-vs-prism, **strict overlap > 1e-6 on all three
   axes**, never by name. Removal set = **2 nodes** (`Wall_0_3_inner`, `Wall_0_3_outer`). Epsilon
   sweep flat 1e-6 → 1e-3. **Three measured traps:** (a) the naming trap — `WallCap_0_3` carries the
   bay index but clears the prism by 4 mm, so a name-based cut breaks V-3; (b) **a trap not named in
   any document** — the west flanking bay overlaps the prism by **+2.384e-07 m** while the east
   abuts at exactly 0, so a naive `>0` test cuts one flank and not the other, asymmetrically and
   invisibly, breaking V-6; (c) three crypt floor tiles abut in z at exactly 0 and overlap in y by
   8 mm, so a `>=0` test breaks V-7.
5. **Wire account.** **Four ceilings, one defect, all attributed against a plain-script control or
   the wire's own source.** Ceilings: (1) no node-property read anywhere in the 39-tool surface;
   (2) scripts can be authored and attached but **never executed** — four in-wire triggers tested,
   all silent; (3) `reflection-method-call` cannot bind *any* Godot object as `targetObject` (no
   `Node` converter registered — `GodotReflectorFactory.cs:41-56`), five encodings tested, plus a
   `find`/`call` default mismatch on `parametersMatchLevel`; (4) **no per-surface material override
   member exists**, so P-6/M-2 are unreachable. Defect: `node-modify {path:"Mesh"}` **clears all
   surface overrides and deep-copies the resource** — the control proves plain GDScript preserves
   overrides and shares one resource across four nodes. Strengths: `node-duplicate` carries
   overrides through (the reason this cell has a room); by-reference resource assignment holds
   `ext_resource` at 6; the §4 transpose hazard **does not exist through the wire** (named
   `Row0/1/2` and `Column0/1/2`). **30 of 36 added nodes and both removals were built natively.**
   Latency re-measured: the ~8.32 ms hypothesis is **tool-dependent** — `node-modify` 8.12 ms,
   `node-duplicate` **71.24 ms** (9× spread).
   **Two declared fallbacks:** FALLBACK-1 (all measurement, 8 headless runs) and FALLBACK-2
   (5 nodes: shared inline mesh + overrides incl. the portal's third slot, **1 s**). Calls that
   could not be made: `node-modify {path:"surface_material_override/2"}`;
   `reflection-method-call → MeshInstance3D.SetSurfaceOverrideMaterial`.
6. **7 rulings logged veto-open** (§6). **Read-list declared, with one contamination DECLARED:** an
   `ls` of `drax/notes/` displayed two `*-l5d-*` **filenames** (never opened), after all measurement
   and building was complete; assessed leak nil — the contract's own header already names those two
   documents. Two live hazards avoided deliberately: the relay's 2 MB `Trace` tool-call log, and all
   W-PRO material (L-J).
7. **Hygiene.** Substrate `d45db0f5…de1966`, mode `0444`, size 134280 — verified at start **and**
   end. Build saved only under `evidence/l5/l5a/`. `project/` restored to its exact 19-entry start
   inventory. Editor and relay reaped; port 27435 free. `reincarnated-godot/`, `harness/`, `l6prep/`
   untouched.
8. **Steer-check filed against the dispatch (§8).** ★ The brief's sentence *"there is a real trap in
   the substrate's naming that the invariants in §6 are designed to catch"* is a **supplied
   conclusion more specific than the contract** — it points at V-3 and therefore at the caps, and I
   went looking for the cap. Mitigated but not nullified by §5.2 independently mandating
   volume-targeting. Also named: the "execution is a small fraction" expectation, and the
   ceiling-finding incentive (mitigated by controlling every attribution). **One gap:** the dispatch
   does not define whether wire-authored-but-Godot-executed scripts count as the wire; I ruled they
   would have (R-L5a-7) and the question was mooted by ceiling 2, **but a future dispatch should say
   so** — a cell ruling the other way could claim the wire built the room while GDScript did it.

**Contract defects filed (measured, per §0.2 rule 2).** (a) M-3/M-4/N-8/R-4/R-5 count the module but
not Godot's **baked-module companions** — each imported `ArrayMesh` brings a `shadow_mesh` (+2) and
each surface a mesh-internal `StandardMaterial3D` (+5); the substrate's own 8/8 are already 4+4 and
6+2. "Exactly 2 new ArrayMesh" is **unsatisfiable by any legal build**, and the plain-script control
produces the identical +4. (b) D-4's 90 % floor is applied to Zone S while 19,350 legitimate spill
pixels land in Zone P — 99.995 % of change is inside `MASK_SP` and only **7 px** reach the far field.
(c) D-5 is convicted by **one** pixel at delta `(0,0,−1)`; warm-ordering is **100 %** at delta ≥ 3.
(d) D-2's containment clause models the cap's footprint but neither the shadow it cast (§12.2's own
throw factors: +0.79 X, −1.49 Z) nor the geometry it occluded — 79.9 % inside as written, 97.5 %
with shadow. (e) M-1/CR-3/§14.5's "14 parameter-identical instances" is **7** — runs 0 and 3 share
one instance between each bay's inner and outer skin; the figure counted skins.

**Status:** COMPLETE. Committed, not pushed.
