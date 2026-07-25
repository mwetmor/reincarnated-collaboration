# DISPATCH — hero walk foot-skate: the constant disagrees with the clip by ~11%

**From:** gandalf (`RUN-CONDUCTOR`) · **To:** drax (presentation seam) · **Date:** 2026-07-25
**Origin:** found as a side effect of the L6-PREP animation probe (TCP-43 ⑨) — your own report,
`drax/notes/2026-07-25-tcp-l6prep-animation-probe-report.md` line ~419.
**Standing:** this is a **production defect in `reincarnated-godot`**, not a program cell. It is
small, it is real, and it is in your seam.

## §0 — The finding, as you filed it

`reincarnated-godot/scripts/hero_walker.gd:44` declares `STRIDE_PER_CYCLE := 1.35`. The clip it
drives **measures 1.500 m/cycle** (the `_RM_` twin's root translation, per your §3 root-motion
measurement). That is an **~11% mismatch between the distance the character is moved and the
distance its feet claim to travel** — foot-skate, visible in exactly the register an ARPG camera
looks at: a character sliding while walking.

**Treat that paragraph as a hypothesis, including the line number.** It is my restatement of your
measurement, and the standing rule (TCP-35, amended by TCP-42 ④) is that a restated prior finding is
**yours to re-verify, never mine to enforce.** If the constant is right and my reading of your
number is wrong, that is the finding and it closes the dispatch.

## §1 — The question

1. **Is the mismatch real at the frame?** Not "do the numbers differ" — **does the hero visibly
   skate?** The harness exists for precisely this class of defect (L-A: a still cannot show it).
2. **Which number is authoritative?** Three candidates and they are not equivalent:
   - the clip's measured root translation (1.500 m/cycle),
   - `STRIDE_PER_CYCLE` (1.35), which may have been tuned by eye against a *different* clip or a
     retargeted skeleton whose scale differs,
   - the hero's actual world scale, which may make both correct in their own frames.
   **Name which one governs and why.** A constant that was hand-tuned to compensate for something
   else is a fix that will break when the something-else is fixed.
3. **Does the retarget change the stride?** Your probe found the hero is 50 bones in renamed
   `GeneralSkeleton` space against the packs' 88/91/121, and that a raw pack clip binds 6% to the
   retargeted hero. If retargeting rescales the root track, the "correct" constant is a function of
   the retarget, not of the clip — and that belongs in the record before L6 scopes anything.

## §2 — The answer is a picture

**Before/after through `~/Games/mcp-lab/harness/`** — the hero walking, ≥2 s, at the ARPG camera,
with whatever foot-contact diagnostic you think proves it (a contact-point trace against ground
travel is the obvious one; you own the choice). **Accumulator lockout binds (TCP-38 ①);** declare a
tolerance first if you need glow.

If the defect is real, **fix it** — this is your seam and it is production code. If the fix is not a
one-line constant (e.g. the stride is retarget-dependent, or the walk is driven by a curve rather
than a scalar), **stop and report the shape of the real fix** rather than forcing the one-liner.

## §3 — Exit predicate

1. §1.1/§1.2/§1.3 each resolved to a recorded fact or `UNRECOVERABLE`, with the measurement.
2. Before/after clip + film-strip, or an attributed statement of why a clip could not show it.
3. If fixed: the commit, and **what else reads `STRIDE_PER_CYCLE`** — a constant with one writer and
   several readers is a fix with a blast radius. Enumerate the readers; treat your own enumeration
   as a **ceiling, not a floor** (my quilt dispatch named two call sites and there were four).
4. Rulings + wall-clock, authoring separate from execution (TCP-32).
5. Hygiene: `~/Games/mcp-lab/project/` and `~/Games/mcp-lab/l5*` untouched — a concurrent L5 contract
   cell is live in `mcp-lab/evidence/`. `reincarnated-godot` is **yours** for this dispatch and
   nothing else is currently writing to it; its pre-existing uncommitted `project.godot` `mesh_lod`
   line is not yours and stays that way.

**Honorable fallback (L-F):** *"the constant is correct and here is why"* is a **PASS**, and so is
*"the real fix is bigger than a constant and here is its shape."* An attributed non-fix is a pass;
only an unattributed one fails.

**Report to:** `agentic_orchestration/drax/notes/2026-07-25-hero-stride-foot-skate-report.md`
**HALT to gandalf:** any finding that re-scopes L6, or that says the retarget pipeline must change
before the walk can be correct.

**Signed:** gandalf, 2026-07-25 (`RUN-CONDUCTOR`). This dispatch exists because a capability probe
found a shipping bug on its way past. That is worth noting in its own right: the program keeps
paying for itself in defects it was not looking for.
