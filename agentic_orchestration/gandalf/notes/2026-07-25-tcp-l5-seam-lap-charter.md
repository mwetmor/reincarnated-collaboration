# TCP-L5 — THE SEAM LAP (charter)

**Conductor:** gandalf (`RUN-CONDUCTOR`) · **Executor seam:** drax · **Date:** 2026-07-25
**Program:** `2026-07-24-tool-capability-program-charter.md` (this folder) — ruling ledger TCP-1..TCP-37
**Authorized:** Matt, TCP-37 ① (*"L5 as shaped — go"*) + ② (roster + mid-run cull authority)
**Pattern:** `agentic_orchestration/operating-procedures/desirable-run-pattern.md` — §6 observations bind
(owner-eye checkpoints §6.2; rubric law §6.3)

---

## §0 — Intent, in Matt's words, and the rubric-law diff (say what falls out)

> *"…we need to extend until we understand the true extent of the capabilities which matter to us in
> completing our **serial modular asset compilation and development pipeline**. Should it be another
> modular room which can be added to this one with doors connecting?"* — Matt, 2026-07-25. Ruled: yes.

**The lap in one sentence:** connect a second room to the frozen crypt through a door, so that a
player reads them as **one place** — and then prove the connection is a **recipe** by emitting room
#3 from it cheaply.

**Five firsts, none of which L1–L4 measured:** ① **subtractive editing** (a door is a hole; every
prior cell only added), ② a **connection contract** (two rooms sharing a portal, floor plane,
register), ③ a **walkability gate** (geometry a capsule can traverse — the first gate about play,
not pictures), ④ the program's **first mode (ii) datum** (design arrival, method-unconstrained),
⑤ **recipe extraction + serial emission** (room #3 from the recipe; authoring-minutes room-2 vs
room-3 is the serial-pipeline metric — the number Matt's intent sentence actually asks for).

**Rubric-law diff (§6.3), declared now:** the contract's predicates measure the SEAM. They do NOT
measure *"reads as one place"* — that is Matt's eye at the declared checkpoints, and no green
predicate substitutes for it (TCP-28/TCP-35: the six clauses passed scenes the owner's eye
convicted in seconds). And per L4's §0 caveat inverted: this lap's mode (ii) cell DOES measure
design arrival — but for ONE executor (drax) on ONE task; it ranks methods only through the (i)
cells that follow.

## §1 — Structure: five stages

| Stage | What | Who | Gate at exit |
|---|---|---|---|
| **0** | Substrate pin — pristine `~/Games/mcp-lab/project/scene_before.tscn`, sha `d45db0f507f6b835e14447c9ceb7e7e6bd645e070bc1fe1241dd6e8522de1966`, mode 0444. **The dais scenes are L4 residue, not substrate.** | conductor | done at charter |
| **1** | **L5-D, mode (ii) design arrival** — the loose brief (§2), method-unconstrained. **Phase A:** arrive at a siting plan, bank it, **STOP**. **Phase B (after owner-eye):** build, evidence, report | drax | **OWNER-EYE ① — Matt sees the siting plan before the wall is cut** (desirable-run §6.2: the eye gates *before* downstream state builds on it). **OWNER-EYE ② — Matt sees the built seam** before the contract freezes |
| **2** | **Contract freeze** — conductor extracts the connection contract from the built arrival, **in the executor's measured numbers only** (TCP-35 standing rule; the conductor's recollection of a scene is not a description of it) | conductor (`⚠ SWITCH: RUN-CONDUCTOR → SPEC-AUTHOR`) | contract diffed against §0 intent out loud (rubric law); Matt red-flag window |
| **3** | **Three (i) cells vs the frozen contract** — roster per TCP-37 ②: **L5a W-MUR → L5b H → L5c W-PRO**, one at a time (L-J), blind (§5), redacted charters (TCP-34) | drax, fresh spawn per cell | **ROSTER GATE at each cell close:** running comparison surfaces to Matt; **he may cull any remaining cell** (*"I will retain the ability to rule one out if it seems they are redundant"*). The cull is his, on composited evidence — never the conductor's forecast (TCP-22, twice now) |
| **4** | **Composite + recipe + room #3** — contact sheet (conductor-assigned per TCP-34 ③); recipe extracted from the winning route; **room #3 emitted from the recipe**; authoring-minutes compared | drax executes, conductor composites | terminal Matt verdict on the lap |

## §2 — The mode (ii) brief, verbatim and complete

> **"Connect a small side-chamber to the crypt so a player reads them as one place. Kit, wall,
> siting, method — all yours."**

That is the entire spec. Everything else the cell decides and LOGS as veto-open rulings: which wall,
portal dimensions, chamber size/shape, kit, register, method (H / installed W-MUR / W-PRO via L-J
swap, swap-time counted as authoring cost), mesh-vs-module, props or none. **Trace-complete exit:**
FIRST_INTENT banked before work; every design decision logged with reasoning; read-list declared.
Mode (ii) is NOT blind — production ancestry (`kit_replica_level.gd`, KIT_CONSTANTS, catalogue) is
its legitimate inheritance, exactly as a real author would use it.

## §3 — What inverts, extends, or is decided-once relative to L4

1. **P-2 INVERTS.** Subtraction means the differ MUST fire at the seam — a zero diff is now a FAIL
   (nothing was cut). The (i) contract pre-registers a **change-region mask**; legitimacy = change
   inside mask + outside-mask floor in the L4-measured 30–60 LSB-px band (TCP-27 ②), cross-cell
   confound declared per TCP-35 ⑤. For mode (ii): diff is descriptive evidence, no bar.
2. **CENSUS EXTENDS.** The mandatory reload-census (engine reload, not text parse) now also proves
   **removals**: removed wall modules absent, **no orphaned collision shapes / occluders** surviving
   at the cut, plus the L4 trio (expected-vs-actual counts, duplicates, untextured).
3. **G4 WALKABILITY lands** — the lap's own gate: a **0.4 m-radius × 1.7 m capsule sweep** travels
   room-A center → room-B center through the portal without penetration. Implementation is the
   executor's ruling; the claim is decidable and the sweep artifact ships.
4. **TCP-31 flatten rule binds every cell** — instancing FBX sub-scenes into a saved `.tscn`
   duplicates via `PackedScene.pack()`; the flatten idiom (compose the FBX-internal transform on the
   right) is the known-good route. Declared per cell.
5. **TCP-36 ② DECIDED ONCE, here:** the **computed caliper is the standing room-coherence
   mechanism** — known world-width projected through declared camera params to screen px, drawn as
   overlay at composite time. Cells report world-space module scale / material density / naming;
   the caliper is applied by the compositor, not improvised per cell. TCP-36 ① naming law binds:
   diagnostic frames are named for the variable they hold constant.
6. **THROUGH-THE-DOOR MONEY FRAME** — the lap's L-A anchor: camera in the crypt, portal in frame,
   second room legible through it. Plus `__box`-class establishment frames of both rooms.

## §4 — Pre-registered predictions (pinned before Stage 1 fires)

- **P-L5-1 — subtraction surfaces a hazard class absent from the entire TCP ledger** (orphaned
  collision, cut-edge atlas bleed, shadow/occlusion seam). Decidable: a logged hazard no TCP-1..37
  ruling covers.
- **P-L5-2 — mode (ii) authoring wall-clock exceeds every L4 cell's total.** Design arrival is the
  cost (TCP-32: authoring ≈ 99%). A cheap arrival would itself be a finding about the brief.
- **P-L5-3 — the census catches something no frame shows, third consecutive lap.**
- **P-L5-4 — portal siting lands on module-grid boundaries with zero mesh surgery.** The cell
  derives the grid pitch from the substrate. If module surgery IS needed, that is a capability
  finding bigger than the prediction.
- **P-L5-5 — W-MUR needs an escape hatch for removal TARGETING.** Identifying *which* wall modules
  occupy the portal rectangle requires reading transforms; L4a's recorded ceilings suggest the wire's
  node-level API can't see them. How L5a targets removals is the cell's most transferable output.
- **P-L5-6 — room #3 from the recipe costs < 25% of room #2's authoring minutes.** This is the
  serial-pipeline thesis as a number. If it fails, the "recipe" was a diary, not a recipe.

**Every prediction resolves to a recorded fact; a FAIL is a finding (L-G/L-F).**

## §5 — Blind protocol for Stage 3 (TCP-34 discipline)

The ruling ledger is now an answer key; from this lap on, (i) cells receive **redacted dispatch
charters**: the frozen contract + binding laws + the §3 mechanics, and **nothing of** — mode (ii)'s
scene/report, other cells' scenes/reports, the L4/L5 residues, the ledger itself. Forbidden-list
enumerated per cell at dispatch time, including the executor's own prior-note trap (the L4c lesson:
"read your own recent notes" is the leak). Declared read-lists mandatory. **A contaminated control
declared is worth more than a clean one asserted** — accidental reads HALT-and-declare.

## §6 — Matt interface (declared pre-launch)

- **Owner-eye ① (siting plan)** and **② (built seam)** in Stage 1; **roster gate** at every Stage-3
  cell close with the running comparison table — cull authority per TCP-37 ②; **terminal verdict**
  on the lap + recipe + room #3. Red-flag pings any time; all conductor rulings veto-open.
- **HALT to Matt:** anything touching `reincarnated-godot` conversion, credentials, story-register
  territory (Q44 stays parked), or a finding that would re-scope L6–L8.

## §7 — Concurrency + blast radius (this lap does not run alone)

Two authorized parallel dispatches are in flight per TCP-37 ③/④: the **motion harness** (pinned to
`~/Games/mcp-lab/harness/`, its own Godot project — **never** `mcp-lab/project/`) and the
**pillar-quilt fix** (writes `~/Games/reincarnated-godot/scripts/kit_replica_level.gd`, commits in
that repo). Therefore: **one agent at a time in `mcp-lab/project/`** (L5 cells own that floor);
L5 cells verify `reincarnated-godot` blast radius by **git attribution, not byte-fingerprint** —
new *committed* changes attributed to the quilt dispatch are not the cell's; any **uncommitted**
modification at cell end is a HALT. `scene_before.tscn` sha + 0444 verified per cell, unchanged.
The frozen substrate **keeps its quilt** (TCP-27 ③ lineage): the lab is a historical record; the
product repo is where the fix lives.

## §8 — Exit predicate (the lap, not a cell)

1. Mode (ii) built + trace-complete + both owner-eyes fired; 2. contract frozen in executor-measured
numbers, intent-diff spoken; 3. **≥2 (i) cells closed** (roster gate may cull to two — cull is a
recorded Matt ruling, not a missing cell); 4. composite sheet + caliper; 5. G4 capsule-sweep artifact
per built seam; 6. P-L5-1..6 resolved or `UNRECOVERABLE`; 7. **recipe doc + room #3 emitted from it
+ the authoring-minutes pair**; 8. ledger rulings recorded; 9. vacate per TCP-27 ① + TCP-34 ④
(`user://` included) — residues to `prep/l5*_residue/`; substrate sha intact.

**Honorable fallback (L-F):** any stage that cannot complete ships its attributed blocking artifact
and the lap closes at the last decidable stage. An attributed failure is a PASS of the program.

---

**Fit test (desirable-run §3):** F1 bounded (one frozen scene + one kit catalogue + one contract) ·
F2 decidable (predicates, sweep, census, counts, minutes) · F3 pre-drained (TCP-37 rulings + this
charter; residual forks are *reasoning*-boundaries deliberately delegated to mode (ii) as the
measured variable) · F4 authority-resident (conductor rules reasoning; Matt holds both eyes, the
roster, and the verdict). **All four YES.**

**Signed:** gandalf, 2026-07-25 (`RUN-CONDUCTOR`). L4's charter defects were found by executors
three cells running; this one's most likely defect is §3 ① — the change-region mask may be
under-specified for a cut whose shadow spill I cannot predict. If the mask convicts an honest cell,
the mask is the defect (TCP-27 ② lineage), and saying so in the report is the PASS.
