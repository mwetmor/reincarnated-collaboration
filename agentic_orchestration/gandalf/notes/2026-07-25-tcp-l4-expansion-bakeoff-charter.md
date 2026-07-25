# TCP-L4 — T2 EXPANSION, THREE-WAY BAKE-OFF (run charter)

**Program:** `2026-07-24-tool-capability-program-charter.md` — lap **L4**, class **T2 EXPANSION** × mode **(i) held-constant spec**
**Conductor:** gandalf (`RUN-CONDUCTOR`) · **Executors:** drax ×3, sequential · **Status:** CHARTERED 2026-07-25
**Matt gate:** none. Q45/Q46 do not block (Q46 is a standing-exposure question, mitigated in-lap by the env block).

---

## §0 — Intent, in one sentence

**Given the same existing scene and the same frozen expansion spec, which of W-PRO, W-MUR and H
produces the addition — without breaking what was already there — and how many author→look→fix cycles
does each one need?**

**Rubric diff against §0 (law L-I).** What falls out: this lap says nothing about *design* quality
(mode (i) freezes the spec), nothing about new-scene authoring (that is L6), nothing about UI or VFX.
It answers **execution fidelity + non-destruction + iteration count** on an expansion task. Do not let
a win here be read as "best tool overall."

**Why this lap is running at all.** The conductor proposed cancelling it on the grounds that the
outcome was predictable. **Matt overruled, and was right to:** the program's founding discipline is
that predictions are pre-registered and then *measured*, and the conductor's prediction record in this
program is five wrong generalizations. **A confident forecast is not a substitute for a lap.** That is
the charter's first sentence for a reason.

## §1 — Why expansion is a different test from replica

Replica (L1/L2) tests: can you build a thing from constants. **Expansion tests something replica
structurally cannot — can you add to a scene you did not author without damaging it.**

L2 found that **a Pro-authored scene does not round-trip through Pro**: `add_scene_instance` calls
`set_owner_recursive`, so internal nodes save owned *and* re-instance on reload, colliding and
renaming. Expansion **requires** loading a scene the instrument did not write. Whether that failure
generalizes to foreign scenes is **untested and is the sharpest question in this lap.**

## §2 — The substrate: one scene-before, one frozen spec, three outputs

**Everything happens in the lab .NET project** (`~/Games/mcp-lab/project/`). It can host all three:
Murzak is a C# addon, Pro is a GDScript addon, H needs neither. `reincarnated-godot` is **not touched**
(TCP-17/18 stand; blast-radius verification per **TCP-20** — file-count + fingerprint of the ignored
tree, because `git status` is structurally blind there).

**`scene_before.tscn`** — the L2 room (17.5 m, 4th pack), rebuilt by the established H pipeline and
**frozen before any instrument runs.** Hash it. Every instrument starts from a pristine copy at its own
output path and **never writes to the frozen original.**

**THE EXPANSION SPEC — identical for all three, held constant (mode (i)):**

A raised dais against the **far (−Z)** wall of the existing room.

1. **Platform** — 6.0 m (X) × 4.0 m (Z) × 0.6 m high, centred on X=0, back edge flush to the existing
   far wall's inner face.
2. **Flanking stairs** — one at each of the dais's +X and −X ends, 4 steps, each 0.15 m rise × 0.40 m
   run, 1.2 m wide, ascending toward −Z.
3. **Two pillars** from the pack, standing **on** the dais, one at each front (+Z) corner, inset 0.5 m
   from each edge.
4. **Two dressing props** from the pack at the dais front edge, symmetric about X=0. Declare which
   props and verify **measured texture presence**, not merely a valid material slot (TCP-16).
5. **NON-DESTRUCTION** — the existing floor, walls, dressing and lighting are **unmodified**: nothing
   moved, deleted, renamed or re-parented. This is a spec clause, not a courtesy.
6. **Camera** — the `__box` standing framing (TCP-12), identical parameters for every cell.

**Kit constants are HANDED TO ALL THREE, deliberately.** We already know Pro cannot derive them (L2
P-B, decisive). Re-testing that here would burn a lap re-answering a settled question and would
confound the thing we *are* measuring. Publish the measured wall/floor/pillar/prop dimensions in the
brief so every instrument builds from the same numbers. **What is being measured is the expansion act,
not the measurement act.**

## §3 — Pre-registered predictions (pinned before results)

- **P-1 — all three produce the dais geometry.** *High confidence.* A FAIL here is a large finding.
- **P-2 — DECISIVE. Non-destruction.** Pixel diff of the region **outside** the addition against
  `scene_before`'s frame must be ~zero for a passing method. **Prediction: W-PRO FAILS** on the L2
  `set_owner_recursive` mechanism, now applied to a foreign scene. **If Pro passes, that is the single
  most interesting result of the lap** and it reverses a standing program belief.
- **P-3 — W-MUR routes through W→H** (authors a builder script via `script-create`) rather than
  placing nodes one at a time, because that is what its 39 tools are shaped like. **If it instead goes
  node-by-node, record that** — it means the W→H path needs deliberate prompting rather than being the
  natural groove.
- **P-4 — H wins wall-clock, but by a NARROWER margin than L2's** — expansion requires *reading* the
  existing scene, which the wire does natively and a script must be told to do.
- **P-5 — ITERATION COUNT, and no lap has ever measured this.** Count author→look→fix cycles to land
  the spec, per instrument. **This is the real axis of "best at building" and the program has been
  proxying it with wall-clock.** Report the count, and what each cycle was spent fixing.

**Every prediction resolves to a recorded fact. A FAIL is a finding (L-G).** **Report medians with n
and exclusions for any timing claim (TCP-19)** — a mean containing retry timeouts is not a measurement.

## §4 — Sequence, and why it is forced

**W-MUR → W-PRO → H.** Three sequential dispatches, one instrument each.

- **Murzak first** — already installed; saves a full swap cycle.
- **Pro second** — swap in, run, **restore verified by file inventory, never a version string** (L-J /
  TCP-9). L-J's three known residues apply: `[autoload]` rewrite, class-name cache emptying, and
  **opening a project in an editor is itself a write.**
- **H last, with no wire installed** — the L1 §4c contamination guard: if H's builder script is on disk
  first, a wire agent can **read the answer instead of solving the task.**
- **No instrument reads another's output.** Separate output paths, and it is a HALT to peek.

**Three dispatches, not one.** L3b burned **217K tokens / 85 tool calls** on a single instrument; a
three-instrument run risks exhausting context mid-lap, which is its own silent failure. Each report
must stand alone.

## §5 — Exit predicate

1. **A four-cell contact sheet** at the `__box` framing: `scene_before` | W-MUR | W-PRO | H — plus a
   **`|diff| ×4` strip against `scene_before` for each**, so non-destruction is visible to the eye and
   not only in a table (**L-A**). Assembled by the H dispatch, which owns the harness.
2. **P-2 resolved numerically** — masked pixel diff of the non-addition region, per instrument.
3. **P-1, P-3, P-4, P-5 each resolved** to a recorded fact with its evidence.
4. **Spec conformance checklist** — the six spec clauses, per instrument, PASS/FAIL with the measurement.
5. **The Pro swap restored and verified by inventory** (§4), plus the class-name-cache rescan.
6. **Blast radius verified per TCP-20** — fingerprint of `reincarnated-godot`'s ignored tree, before
   and after. `git status` alone does not satisfy this.
7. **No Godot or `gamedev-mcp-server` processes left running** — L3's exit-state discipline, standing.

**Honorable fallback (L-F/L-G):** any instrument that fails ships **the attributed failure point with
the exact blocking artifact**, and **its cell still appears on the contact sheet** — showing the
failure. A named ceiling is a PASS. **An unattributed failure is the only real failure.**

## §6 — Conductor interface

- **In-run rulings (drax, logged, veto-open):** prop selection and declared substitutions; how to read
  the existing scene; dais placement arithmetic if the kit forces it; whether to use W→H or direct
  placement **provided the choice is recorded as P-3 evidence**.
- **HALT to gandalf:** any need to write into `reincarnated-godot`; swap restore failure; an instrument
  requiring the frozen `scene_before` to be modified; Murzak launched without the full self-hosted env
  block (**Q46** — the compiled-in default is Cloud and it transmits before any tool call; the launcher
  hard-fails or it does not launch).
- **HALT to Matt:** nothing anticipated.

**Reports:** `agentic_orchestration/drax/notes/2026-07-25-tcp-l4{a,b,c}-<instrument>-run-report.md`

---

**Signed:** gandalf, 2026-07-25 (`RUN-CONDUCTOR`). **This charter exists because its conductor was
overruled.** I argued the outcome was known well enough to skip the measurement — which is precisely
the reasoning that produced five wrong generalizations in this program's short life. Every prior lap
found a charter defect; assume this one has them too, and report rather than work around.
