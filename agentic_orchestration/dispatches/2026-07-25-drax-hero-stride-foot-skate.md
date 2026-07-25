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

---

## Completion record

**drax, 2026-07-25.** Report:
`agentic_orchestration/drax/notes/2026-07-25-hero-stride-foot-skate-report.md`
Fix committed to `reincarnated-godot`. **Not pushed.**

### §0 — the hypothesis, re-verified including the line number

`hero_walker.gd:44` did declare `STRIDE_PER_CYCLE := 1.35` — **correct, line 44 exactly.**
`A_MOD_BL_Walk_F_RM_Masc` does carry a 1.500 m root track — **correct, re-confirmed twice.**

**The ~11 % is wrong, and it is my error, not your reading.** 1.500 is measured in the
**source rig's own space**; the constant operates in the **hero's travel space, after
`hero_walker`'s own 0.877497 `TARGET_HEIGHT` scale**. Two frames. In one frame the gap is
**+4.0 %**. My L6-PREP §8 filed the comparison without the frame, and the dispatch's refusal
to enforce it back at me is the only reason it was caught.

(Also: line 38 names the **in-place** twin, and the `_RM_` twin is not vendored in
`reincarnated-godot` at all. Using it as the stride declaration is still legitimate — the
in-place clip's own feet independently measure 1.49696 against its twin's 1.500.)

### §1 — the three questions, each to a recorded fact

1. **Real at the frame? YES.** Rendered and counted by the render itself: **19 stances,
   0.0366 m mean planted-foot slide per stance** (max 0.0438) at 1.35, **0.0129 m** (max
   0.0220) at 1.30 — **−65 %**. Honest qualifier: real and measurable at the ARPG register,
   but **not conspicuous** on this character — the shipped hero is a floor-length-robed
   wizard whose feet are mostly occluded. The ground contact-trace carries the reading.
2. **Which governs?** The hero's own planted-foot travel in travel-node space,
   **D\* = 1.297 ± 0.003** — 1.294…1.299 for **every** contact threshold from 0.10 to 0.50
   (0.4 % spread). Cross-checked criterion-free against the source clip's foot-locked
   1.49696 × 0.877497 = 1.3136; the two routes agree to 1.2 %. **Shipped 1.30.** The old
   1.35 = 0.90 × 1.50 exactly, but the hero scale is 0.8775, so it was **not** a scale
   correction — it was eyeballed, and nothing was depending on it.
3. **Does the retarget rescale? Split answer.** Pose/foot motion: **NO (×1.00003)**. Root
   translation track: **YES, ×1.13280** = 1/motion_scale — `normalize_position_tracks`.
   And **binding to the hero destroys the source clip's foot lock outright.**

### §2 — the picture

`~/Games/mcp-lab/harness/out/hero_stride_{before,after,detail_before,detail_after}/` +
`hero_stride_AB/{AB_gameplay_f140,AB_marks_f100,AB_detail_f100}.png`. 4.0 s @ 40 fps,
1280×720, ARPG framing (yaw 47°, pitch −50°) and a 2.9 m detail framing. Diagnostic:
per-frame ball-contact dots + a white **landing anchor** and a **live tether whose length
is the slide in metres**, over a 0.5 m ground ruler.

**Accumulator lockout held, no tolerance declared** — `deterministic_env()` unmodified,
re-render **160/160 byte-identical**, matching MP4 sha256.

### §3 — exit predicate

1. ✅ §1.1/1.2/1.3 each to a recorded fact, none `UNRECOVERABLE`.
2. ✅ Before/after clips + film-strips + 6× magnified A/B plates.
3. ✅ **Fixed** (`hero_walker.gd` 1.35 → 1.30, committed) and **readers enumerated in 13
   passes**: **1** reader of the constant, **1** writer of `speed_scale`, **2** live call
   sites (`walkthrough_ravine.gd:102`, `walkthrough_carved.gd:145`). 8 `HeroRig`
   instantiators, 6 unaffected. **0** aliased users, **0** `.tscn` attachments, **0**
   re-implementations of the formula. `AGENT_STATE.md:818`'s claim that the kit replica
   preloads `HeroRig` is **stale** — verified against the tree. Effect: cadence +3.8 %;
   travel path, video length and camera path unchanged. **Smoke 11/11, exit 0.**
4. ✅ Rulings R1–R8 + wall clock, authoring separate from execution.
5. ✅ Hygiene: `mcp-lab/project/` and `evidence/l5/` never entered (their recent mtimes are
   your concurrent L5 cell — `l5a_measure.gd` changed at 18:18:09 *while I ran the check*;
   my last write anywhere was 18:13). `project.godot`'s `mesh_lod` diff untouched and
   unstaged. Harness still has no `.godot/`. `user://` returned to clean.

### HALT — this re-scopes L6

**Both honorable outcomes apply.** The constant was wrong and is fixed; **and the real fix
is bigger than a constant.**

- **Retargeting does not preserve foot locks.** The source clip is *perfectly* locked — ball
  height constant to **0.3 mm**, backward rate to **±0.6 %**, both feet, whole stance. On the
  hero the same clip gives a ball that wanders **2.2 cm** vertically and **1.15…1.39** in
  rate, with the two feet planting **3.5 cm apart** in height — while the hero's rest is
  **mirror-exact** (leg chains L/R ratio 1.000000). **75 % of the residual skate is this**
  and no scalar reaches it. Remedy is foot IK or proportion-matched rigs.
- **A stride constant is now a per-character measurement**, not a per-clip one. N monsters =
  N measurements, or foot IK so it stops mattering. Instrument:
  `reincarnated-godot/scripts/tcp_stride_measure.gd`, headless, ~30 s.
- **`normalize_position_tracks` silently inflates retargeted root tracks by 1/motion_scale**
  (×1.1328 here). Lands on **all 3,386** clips my L6-PREP report proposed to patch. Anyone
  reading a retargeted `_RM_` root track as metres is 13.3 % wrong and nothing flags it.

### Worth recording on its own

Four estimators returned **0.641 / 1.245 / 1.229 / 1.297** on the same rig, and two of them
had **invented a 10 % left-right leg defect that does not exist.** Height cannot detect
contact (a swing foot skims to y = +0.001 while moving forward at +3.17 m/cycle); a
rigid-foot test cannot either (toe-off pivots *on* the ball and closes the window early).
Printing the raw curve settled it in one look.

And the first attempt to hand the harness a `.glb` **with animation** passed every structural
check while putting the feet in the air (skeleton lost `Root`, 122 tracks → 36, D\* off by
13 %). Caught by a **numeric clean-room verify before any frame was judged**, and replaced by
a baked pose table that verifies at **0.000000 m**. Same lesson as L6-PREP's, one turn on:
**98.7 % name-match with a head below the floor** then; **all-green export with the feet in
the air** now.

**Wall clock:** 17:37 → 18:22 EDT, **45 min** — execution **~12 min** (13 headless runs, 6
harness renders, 1 framediff), authoring + analysis **~33 min**. The largest single cost was
disproving my own estimators.

**Signed:** drax, 2026-07-25.
