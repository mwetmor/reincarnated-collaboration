# DISPATCH — TCP-L7-V: mode (ii) VFX ARRIVAL — make the crypt feel inhabited

**From:** gandalf (`RUN-CONDUCTOR`) · **To:** drax (presentation seam) · **Date:** 2026-07-25
**Authorization:** Matt, 2026-07-25 — L7 flipped to **(ii)-first**, running in parallel with L5.
**Lap:** L7 VFX (T4-VFX). This is the lap's **first** cell and it is a **design arrival**, not an
execution of a spec.

## §0 — Why (ii) comes first here

L5 ran design-arrival before spec-execution and **every finding of consequence came out of the
arrival**, not the execution: the floor hole nobody had specified, the substrate's total absence of
collision, the transpose near-miss, the fact that the judging camera cannot see into what it judges.
A spec-execution cell can only find defects in the spec. **An arrival finds defects in the world.**

So: you decide the answer. Your iteration loop, your rulings, and your **authoring clock** are the
measurements.

## §1 — The brief, verbatim and complete

> **"Make the crypt feel inhabited. One ambient VFX pass — what, where, how many, and by what
> method: all yours."**

That is the entire spec. Effect choice, placement, count, budget, tool, whether it is one system or
six — all yours, each logged as a **veto-open ruling with reasoning.**

**Register note, and it is a constraint rather than a hint:** this is *Reap. Die. Rise.* — a
death-faith ARPG, judged at an ARPG camera, not a cinematic one. An effect that reads beautifully in
a close-up and vanishes at play distance has failed. **Whatever you author, you must show it at the
camera the player actually has.**

## §2 — Hard constraints (three, and only three)

1. **Your floor is `~/Games/mcp-lab/l7vfx/` — a NEW project.** Create it. **`~/Games/mcp-lab/project/`
   is FORBIDDEN** — a blind L5a cell is live there and its attribution is destroyed if anything
   moves. `~/Games/mcp-lab/harness/` is yours to *use*, not to modify (a fourth cell may need it).
2. **The stage:** copy `~/Games/mcp-lab/project/scene_before.tscn` **out** (read-only; it is mode
   0444 and stays that way — verify sha `d45db0f507f6b835e14447c9ceb7e7e6bd645e070bc1fe1241dd6e8522de1966`
   at start and end) into your own project and work on the copy. **Derive its geometry yourself** —
   this dispatch deliberately states none, because a conductor's description of a scene is a steer.
3. ★ **DECLARE YOUR DIFF TOLERANCE BEFORE YOU RENDER, IN WRITING (TCP-38 ①).** The accumulator
   lockout is causal and measured: with glow/SSAO/SSIL/SDFGI/volumetric-fog/auto-exposure off, the
   harness is **90/90 byte-identical**; with them **on, 0/90**, diverging by a **max channel delta of
   1** — invisible to the eye, fatal to a differ testing `==`. **Most VFX wants glow.** So decide
   *first* whether this cell buys glow at the price of a tolerance, or refuses glow to keep byte
   equality, **and write the number down before the first frame.** A tolerance declared afterwards is
   a tolerance fitted to the result. `probe_accum_on.gd` ships in the harness — re-run the isolation
   rather than re-deriving it.

Everything else — kit, particle counts, shaders, lights, whether you use `GPUParticles3D` or
`CPUParticles3D` or a shader, method (H / the installed W-MUR wire / a script) — **is yours.**
**L-J binds: W-PRO stays parked**; a concurrent cell owns the wire question this session.

## §3 — What you ship

1. **FIRST_INTENT banked verbatim + authoring-clock start, before any work** (TCP-32 — the clock
   includes thinking, and authoring time is the number that matters).
2. **The tolerance declaration**, timestamped before the first render.
3. **The answer as MOTION (L-A):** a clip at the ARPG camera, ≥2 s, ≥24 fps, through
   `~/Games/mcp-lab/harness/` — plus the film-strip. Ambient VFX that cannot be judged in a still is
   exactly why the harness exists. **Also ship one still at `__box`** (Matt's confirmed judging
   framing) so this cell composites against every other room the program has built.
4. **A COST account** — this is the part a pretty clip cannot substitute for. Particle counts, draw
   calls, and **frame time with the effect and without it**, measured not estimated. An ambient pass
   that doubles frame cost is a finding; so is one that costs nothing.
5. **Rulings, veto-open, with reasoning.** Read-list declared, including an explicit *not-read* list.
6. **Clock closed** — authoring separate from execution.

## §4 — Exit predicate

1. §3.1–§3.6 all present. 2. Substrate sha + 0444 verified at start AND end. 3. `mcp-lab/project/`
demonstrably untouched (inventory or mtime it). 4. Harness unmodified (hash it) — **or**, if you had
to extend it, say exactly how and why, because that is a finding about the harness. 5. `user://`
clean; your project stays.

**Honorable fallback (L-F):** an arrival that stalls and ships **the attributed blocker plus its best
partial answer** is a **PASS**. **Ceiling-finding is a PASS (L-G)** — if the tooling cannot author
the effect you wanted, *that is the lap's whole point*, and the honest ceiling beats a lesser effect
you could get.

**Report to:** `agentic_orchestration/drax/notes/2026-07-25-tcp-l7v-vfx-arrival-report.md`
**HALT to gandalf:** any need to touch `mcp-lab/project/`, the substrate, or another cell's floor;
any finding that re-scopes the lap.

**Signed:** gandalf, 2026-07-25 (`RUN-CONDUCTOR`). **Name anything in this dispatch that steered
you.** That sentence has caught a conductor defect in **nine consecutive cells**, and §1's register
note is my prime suspect this time — if "death-faith ARPG" pushed you toward an effect you would not
otherwise have chosen, say so.
