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
