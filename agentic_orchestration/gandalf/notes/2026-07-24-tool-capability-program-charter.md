# The Tool-Capability Program — charter

**Status:** CHARTERED 2026-07-24 · **Conductor:** gandalf (`RUN-CONDUCTOR`) · **Gate:** gandalf (`ARCHITECT`), this doc
**Supersedes as governing frame:** the one-off KIT-REPLICA LAP-1 charter (which becomes lap L1 of this program)
**Lineage:** MCP bake-off 2026-07-23 → KIT-REPLICA LAP-1 2026-07-24 → two manifest audits 2026-07-24 → Matt's reframe → this

---

## §0 — Intent, in Matt's words

> *"I want to continue testing production/development skills, iteratively across a wide breadth of
> processes and then deep into increasing difficulties until we find the end of the capability of
> each tool."*

> *"We already know that we can rebuild pre-built scene and kit configurations out of similar assets
> with python/etc but there are MANY BIG unknowns that we need to test such as, which tool/process
> combination is best at building **new** scenes, **expanding** scenes or building out other new
> concepts like new **VFX** or **HUD/UX/UI**. Based on that, we owe Murzak some more testing too."*

**Finding a ceiling is a PASS.** The program's product is a capability map, not a winner.

## §1 — What the two audits changed, before any lap fires

L1 shipped a verdict I have now corrected twice from source in a single session.

1. *"The wire inspects, it does not build"* — true of the incumbent, **false of the category.** Pro
   ships a complete assembly loop (`2026-07-24-mcp-authoring-surface-audit.md`).
2. *"Neither server can measure and create"* and *"GridMap is a structural gap"* — **Murzak closes
   both**, ships ten extension packages including GridMap / CSG / GPUParticles, exposes
   `reflection-method-call` (any C# method, any assembly), and — decisively — **CRUDs GDScript and
   can therefore author our own winning method** (`2026-07-24-murzak-manifest-audit.md`).

**Capability enumeration is finished.** The remaining questions are **latency**, **aim** (can the
agent hit the right call with no control to check itself against), and **blast radius**. Every lap
below measures those three, not "can it."

## §2 — The matrix (task-class × judgment-mode)

**Task classes** — increasing distance from a known answer:

| | Class | Definition | Control exists? |
|---|---|---|---|
| **T1** | **REPLICA** | reproduce a known room in a new kit | ✓ the reference |
| **T2** | **EXPANSION** | modify/extend an existing scene in place | ✓ the scene before |
| **T3** | **NEW SCENE** | author a room that does not exist | ✗ |
| **T4** | **NEW SURFACE** | VFX · HUD/UI/UX — a layer we have never authored | ✗ |
| **T5** | **CHARACTER / ANIMATION** *(added by TCP-37, from Matt's next-test question)* | stand up an animated character/monster holding a weapon and swinging it — skeleton, `BoneAttachment3D`, `AnimationPlayer` | ✗ — but **splits in two**: a STATIC phase (rigged pose, weapon in hand — judgeable from stills under L-A now) and a MOTION phase (the swing — judgeable only through the motion harness, TCP-37 ③) |

**Judgment modes** — Matt's ruling, generalized:

- **Mode (i) HELD-CONSTANT SPEC** — every instrument gets the same precise written target.
  **Measures EXECUTION FIDELITY.** Attribution is clean: one variable moves, the tool.
- **Mode (ii) LOOSE BRIEF** — one sentence of intent; the agent decides everything else.
  **Measures DESIGN ARRIVAL** — iteration throughput and terminal quality.

**Matt's ruling (2026-07-24):** *"I would like to see T4 with both (i) and (ii) as **separate tests
of capability**."* Not one lap with two conditions — two laps.

**Why he is right, stated as the program's central law (L-E below).** For 3D architecture, design
judgment and tool capability are separable — a room has measurable geometry, so a spec can carry the
design and the tool is scored on execution alone. **For UI and VFX they are not separable.** Nobody
specs a HUD or a particle effect in advance; you nudge and look, forty times. So (i) and (ii) are not
the same capability under different noise — they are **different capabilities**, and a tool can be
strong at one and useless at the other.

This maps exactly onto the ruled doctrine in `pipeline-game.md` — *"MCP authors recipes / headless
scripts run production."* **(i) measures the "runs production" half. (ii) measures the "authors
recipes" half.** A tool scoring high on (i) and low on (ii) is an **executor**. High on (ii) makes it
a **design instrument**. That is the actual verdict shape the program is trying to produce.

| | mode (i) held-constant | mode (ii) loose brief |
|---|---|---|
| **T1 REPLICA** | **by definition** — the control *is* the spec (L1 ran this) | meaningless — there is a right answer |
| **T2 EXPANSION** | **primary** — "add a side chapel matching the register" is a spec | available; taste-dominated; defer |
| **T3 NEW SCENE** | **most informative single test in the program** — separates *build what you're told* from *decide what to build* | the honest working mode; run second |
| **T4 NEW SURFACE** | **RULED — separate lap** | **RULED — separate lap** |
| **T5 CHARACTER/ANIMATION** | static phase: "this monster, this weapon, this pose" is a spec | motion phase is (ii)-shaped by nature — nobody specs a swing arc in numbers; you nudge and look. Harness-gated |

## §3 — Standing laws

- **L-A — Frames at the play camera.** A presentation lap does not meet its exit predicate until it
  produces images rendered at the play camera, judgeable by Matt unaided. Instrumentation may
  accompany; never substitute. *(Discipline candidate #63, filed to jack-ryan 2026-07-24; in force
  here regardless of ratification.)* Corollary with teeth: Murzak's `screenshot-isolated` is a model
  viewer — **the viewing condition Diablo III's team moved monster review OFF of.** `screenshot-camera`
  is the legal one.
- **L-B — Manifest before behaviour — and THE MANIFEST IS THE WIRE, NOT THE DOCS.** Capability is read
  from the manifest; reliability is read from behaviour; **neither is inferred from the other.**
  **Amended 2026-07-24 by L2, which caught me one level up:** I read
  `godot-mcp-pro-v1/docs/tools-reference.md` — 77 documented tools — and called it the manifest.
  **The server exposes 175**, confirmed in `package.json` and over the wire, including **`add_gridmap`**
  (I wrote "no gridmap" as a field-wide structural gap), `batch_add_nodes`, a second escape hatch
  `execute_game_script`, the `create_particles` family, and `record_frames` / `start_recording` /
  `replay_recording` / `compare_screenshots` — a **motion-capture surface** that bears directly on
  TCP-8. Three documented schemas disagree with the wire. **A vendor's doc is a claim about the
  manifest, not the manifest. Enumerate the live tool list at every lap.**
- **L-K — In this stack, failure returns SUCCESS.** *(Born 2026-07-24 from five instances across two
  laps and three instruments — the single most important finding of this workstream.)* Every failure we
  have found so far reported `ok`:
  1. **M2's transpose** — loaded with zero errors, zero warnings, passed full structural inspection;
     every rotation mirrored.
  2. **`aura_tint`** — host wrote a `tint` uniform the ruled shader variants do not expose. Silent
     no-op for **every pilot**, indefinitely.
  3. **The void-cap rainbow** — sampled a tiling texture the pack does not ship; returned a palette
     swatch strip instead of stone.
  4. **`custom_aabb`** *(L2, and the most dangerous of the five)* — returns a field **shaped exactly
     like the answer**, identically zero, unrelated to the mesh, with `ok=true`. An agent that trusts
     it derives a **zero-sized wall** and every downstream call still succeeds.
  5. **Pro's own round-trip** *(L2)* — 252 `update_property` calls on paths **Pro itself reported**,
     returned **255/255 ok**, and wrote nothing.

  **The law:** any write across a seam boundary — file format, shader uniform, texture slot, wire call
  — is unverified until a **rendered frame** confirms it. Not a return code. Not a structural
  inspection. Not a property read-back from the same surface that lied. **A rendered frame diffed
  against a control is the only instrument that has ever caught one of these.** *(This is the real
  evidentiary basis for discipline candidate #63 — stronger than the one it was filed with.)*
- **L-L — A rule enforced by prose is not enforced.** *(Born 2026-07-25 from three instances in two
  days.)* ① L4's one-scene-per-process hazard was cured by making `l4_shoot.gd` **refuse** a second
  scene, not by documenting it. ② The motion harness found `--headless` exits 0 with zero frames and
  made the rig **refuse at startup** rather than write it in a README. ③ **The proof:** L5-D's own
  probe rig **reproduced the TCP-23 double-grab while citing TCP-23 in its header comment** — `await`
  in `_process` re-enters before `quit()` lands, so it saved the drifted second frame. The author
  knew the rule, wrote the rule down, and broke it in the same file. **Every standing hazard in this
  program gets a latch, a refusal, or a gating assert. A header comment is a wish.** Direct sibling
  of TCP-33's *"a cross-check that reports and does not gate is decoration."* ④ ★ **AND THE PROSE CAN
  BE WRONG WHILE READING AS A SAFEGUARD.** `SITING_PLAN.md` §3's *"Transpose watch"* — the note L5-D
  wrote specifically to avoid the KIT-REPLICA lap-1 transpose trap — **states the convention
  backwards.** `.tscn` stores the basis as **ROWS**, and the 12-float form has **no GDScript
  constructor at all**, so any script authoring transforms is forced through a hand translation with
  no compiler between it and the scene. **Corollary that is worse than the error: SIX OF EIGHT
  transcribed bases PASSED a transposed reading**, their off-diagonals being O(1e-7) — below
  `is_equal_approx`. Only the two ±X walls, off-diagonals O(1), could fail. **A check that most cases
  pass is not a check; pick the case for its capacity to fail, not its representativeness.** What
  saved the build was structural, not careful — *harvest the basis off the live node, never retype,
  keep the transcription only as a gate.*
- **L-O — A predicate that counts the reference implementation's PARTS measures conformance to the
  IMPLEMENTATION, not to the spec. Gate the invariant; REPORT the count.** *(Born 2026-07-25, the L5
  contract freeze.)* I handed the contract author *"cap-node census exact at 34 caps"* as a supplied
  predicate. **34 is true only for one cap construction** — a cell capping the same wall run with
  three long boxes instead of six short ones scores 31 and **fails a predicate it never violated**,
  while a cell that shatters the ribbon into 34 fragments passes. The count is a fingerprint of *how
  drax built it*, not of *what must be true*. Rewritten as **AABB identity on the surviving crypt
  caps + XZ-projected ribbon continuity with no gap > 1e-3 m** — both construction-independent; 34 is
  now reported, not gated. **This is TCP-28's disease inverted:** there the rubric measured fidelity
  to the spec and was blind to quality; here a predicate measured fidelity to an *artifact* and was
  blind to legal alternatives. **In a mode-(i) comparison this is the more dangerous of the two — it
  convicts the tool that solved the problem differently, which is precisely the signal the lap
  exists to detect.** Standing: every (i) predicate states what must be TRUE, never how many pieces
  the reference used to make it true.
- **L-N — CAPABILITY PROBES ARE ASYMMETRIC: a YES is self-certifying, a NO is not. A NO must clear
  the instrument before it is recorded.** *(Born 2026-07-25, L6-PREP.)* A YES ships an artifact you
  can hold — the `.glb` plays, the frame renders. **A NO can be produced by a broken frame, and a
  broken frame can only ever say NO.** L6-PREP hit **four instrument bugs, each of which had already
  produced a confident wrong answer about the ASSETS**, and **two of them — *"the pose is dead"* and
  *"root motion does not survive glTF"* — were exactly the blocker-confirmed answer**, which would
  have hardened TCP-38 ③ into a permanent false finding and argued for keeping the capability fork
  open. **~1/3 of the cell's authoring time went to fixing the instrument before trusting its
  output.** ★ **And note what did NOT protect against this: my charter was scrupulously neutral —
  *"Either answer is a finding of the first rank; do not favour one."* Neutrality between outcomes is
  worthless when the INSTRUMENT is not neutral.** Standing: a probe reporting a capability ABSENT
  ships its instrument-validation alongside the finding; a probe reporting a capability PRESENT ships
  the artifact. Sibling of L-A — see TCP-43 ④ for the case where every numeric check passed a broken
  result and only the render caught it.
- **L-M — A measured limit that is derivable from the instrument is a measurement OF the instrument.**
  *(Born 2026-07-25, L5-D G4.)* The walkability bisection returned a clearance of **0.8595 m** —
  four decimals of apparent precision, and **exactly the height at which a `height ≥ 2r` capsule's
  own bottom re-enters the floor (0.85949)**. The search had converged on the probe's geometry, not
  the doorway's, and would have been believed. Re-asked with a **width-free box probe: 1.9544 m**,
  agreeing with the independently measured kit proxy (1.9553) to **0.9 mm**. Two clauses: ① **a probe
  whose dimensions are coupled cannot measure a gap on the uncoupled axis** — capsule radius drives
  both width and height, so it cannot report width alone; ② **detection rule — before believing any
  measured limit, try to derive it from the instrument's own constants. If it falls out, the
  instrument measured itself.** Sibling of L-K (failure returns SUCCESS): there the error wore a
  success code, here it wears four decimal places.
- **L-C — Capability verdicts expire.** Murzak's ten-package extension family shipped 2026-07-20; our
  bake-off ruled on it 2026-07-23 without seeing it. **Re-read the manifest at every lap, record the
  version/SHA read, never carry a prior lap's verdict forward as fact.**
- **L-D — Never rank by catalogue count.** Rank by *measured module compatibility*. *(KRL-4, carried
  from L1, where asset count inverted the true difficulty order.)*
- **L-E — Separate execution fidelity from design arrival.** *(Matt 2026-07-24, generalized.)* Where
  both modes are meaningful and cheap, run them as separate laps. Never let one lap's result be read
  as evidence for the other capability.
- **L-F — A control or a trace.** Every lap ships exactly one of: a **control-diff** (mode i) or a
  complete **iteration trace** (mode ii). A lap with neither is unjudgeable and must not launch.
- **L-G — Ceiling-finding is a PASS.** A lap that hits a hard limit and **names it with attribution**
  succeeds. Only an *unattributed* failure fails. *(Matt's standing intent.)*
- **L-H — One tool, one room, one variable.** Attribution collapses the moment two things move. L1
  proved this in the negative: R1's method changed mid-room *and* its kit was the incompatible one.
- **L-I — Rubric law, inherited.** *(desirable-run-pattern §6.3.)* At each lap launch, diff the exit
  predicate against §0's intent sentence and **name out loud what fell out.** Three separate defects
  in this workstream trace to a *proven*-needs rubric quietly narrowing the owner's question.
- **L-J — One wire at a time, restore verified by inventory.** All three instruments install to
  `res://addons/godot_mcp/` — the incumbent occupies it, Pro carries ~70 hardcoded refs to it,
  Murzak's installer downloads into it. **They cannot coexist.** Every lap that swaps records the
  outgoing addon's file inventory first and restores against **that inventory, not a version string**
  — because `--install-addon` reads `plugin.cfg`, sees the right version, prints *"already up to
  date"* and exits without an integrity check. The installed incumbent was **3 `.gd` files against an
  expected 36**. A gutted addon reports itself healthy and never self-heals.

  **Three residues the restore predicate does not cover** — L2 found two, and a third surfaced during
  L3's dispatch: (1) Pro rewrites `project.godot`'s `[autoload]`; (2) addon removal **silently empties
  the global class-name cache**; (3) **merely OPENING the project in an editor rewrites
  `project.godot`.** Evidence for (3), caught 2026-07-25 while checking L3's blast radius:
  `reincarnated-godot/project.godot` carried an uncommitted deletion —

  ```
  -[rendering]
  -mesh_lod/lod_change/threshold_pixels=1.0
  ```

  — mtime `00:08`, **29 minutes before the L3 lab directory existed**, with `.godot/` stamped the same
  minute. Not this lap's. The mechanism is Godot stripping a setting whose value equals the engine
  default on save. Effect here is nil (1.0 *is* the default), but the class is not nil: **a setting
  written explicitly because a human wanted it explicit becomes implicit, and then tracks the default
  silently if the default ever moves.** `mesh_lod` in particular is a capture-fidelity setting.

  **Consequence for the program:** an editor open is a WRITE. Any lap that opens a product project in
  any editor — even to look — owes a `git diff` of `project.godot` before and after. **Byte-perfect
  belief is not byte-perfect verification** (L-K wearing configuration clothes: the editor reported
  nothing, logged nothing, and edited the file).

## §4 — Judgment instruments

**Mode (i) — control-diff.** Deliverable: play-camera frame + the control's frame + a pixel diff +
a spec-conformance checklist. Fully decidable in-run. This is L1's machinery, already built
(`kit_contact_sheet.py`, `shoot_kit_replica.gd`).

**Mode (ii) — iteration trace.** No control exists, so the instrument is the *process*: **every
intermediate frame, in order, timestamped, each paired with the prompt that produced it** — the shape
`_dolly/` already has. Metrics: **looks-to-converge**, **wall-clock per look**, **cost per look**.
Terminal verdict is Matt's eye on the final frame.

**The decidability conversion — say it out loud, because §6.3 exists to catch exactly this.** Mode
(ii) laps are legitimate autonomous runs *only* because the exit predicate is **trace-completeness**,
not quality: *run to agent-declared convergence or N looks, whichever first; ship the complete trace.*

> **The run VERIFIES that the trace is complete. The run does NOT verify that the artifact is good.**
> Quality is Matt's, after, on the artifact. A mode-(ii) lap that reports "40 looks shipped" as if it
> meant "the HUD is good" has committed the KIT-FIDELITY failure verbatim.

## §5 — The field: it is instrument × method, and the winner may be a composition

**Wire instruments (MCP):**

| | Instrument | Create | Measure | Escape hatch | Status |
|---|---|---|---|---|---|
| **W-INC** | `@satelliteoflove/godot-mcp` 4.1.0 | ✗ none | ✓ `scene3d get_bounds` · game-clock | `godot_exec` → running game | installed; **gutted addon hazard** |
| **W-PRO** | Godot MCP Pro 1.15.1 | ✓ full | ✗ none | `execute_editor_script` → editor | on disk, shelved; addon-path collision |
| **W-MUR** | IvanMurzak Godot-MCP | ✓ full + GridMap/CSG/Particles | via reflection or own tool | `reflection-method-call` (any C# method) | **not installed** — Matt-gated |

**Non-wire methods:** **T** = Python emits `.tscn` text (L1's M2 — silent transpose trap) ·
**H** = headless GDScript builder (L1's M3 — the winner, 1m37s/room).

**The composition finding.** W-MUR's `script` family CRUDs `.gd` and attaches it. **W-MUR can author
H.** So the program must score a fourth path — **W→H**: the wire authors the builder, the builder
runs production. That is not a compromise between the two camps; it is the ruled doctrine executing
itself inside one tool, and it is the single most likely winner of the whole program. Score it.

> **QUALIFIED 2026-07-25 by L4a (P-3), and the qualification is task-shaped.** L3 proved W→H works
> when the wire builds **from scratch**. Handed an **expansion** task with no method steer — the
> first prompt was banked verbatim before any wire call and carries no method noun — **W-MUR went
> node-by-node.** The reason is a manifest fact, not a preference: **Murzak's wire cannot read a
> transform.** Across all 39 tools, `scene-get-data` and `node-find` return identity only, there is
> no `node-get-properties`, and the reflection hatch is dead for Nodes — `GodotReflectorFactory`
> registers converters for Vector2/Vector3/Color/Resource/NodePath and **no Node converter**, so
> `targetObject` deserializes null. **The audit's "closes both — measure and create" holds for
> Resources and INVERTS for Nodes.** So the cell split: *read* forced onto a script, *write* left on
> the node family. **W→H is not the natural groove for expansion with this instrument** — it has to
> be asked for. That weakens the program's central bet in exactly the place it mattered most, and it
> was measured rather than assumed because the charter forbade steering.

> **QUALIFIED A SECOND TIME 2026-07-25 by L4c (TCP-32), and this one moves the goalposts rather than
> the odds.** The bet's implicit payoff was always *"the wire's convenience, then the builder's
> speed."* **The builder's speed is 0.60 s — it was never the prize.** H's full run costs 282.5 ms of
> build-and-save inside a cell that took 24 minutes; **authoring is ~99% of the cost, and W→H only
> wins if the WIRE reduces AUTHORING time, which no lap has yet measured.** So W→H is not falsified
> and not confirmed — **it is untested on the only axis that decides it**, and every lap so far
> measured the axis that doesn't. A mode-(ii) lap, where nobody knows the geometry in advance, is the
> first honest test of the bet. **Until then, "the single most likely winner" is a forecast — and
> TCP-22 is the standing ruling on what those are worth here.**

## §6 — Lap sequence

| Lap | Class × mode | Instrument(s) | Gate | Ready? |
|---|---|---|---|---|
| ~~L1~~ | T1 × (i) | W-INC / T / H | — | **CLOSED** — H won; W-INC has no create primitive; T failed silently |
| ~~**L2**~~ | T1 × (i) — CALIBRATION | W-PRO | none | **CLOSED 2026-07-24 — Pro is an EXECUTOR.** See below |
| ~~**L3**~~ | standup | **W-MUR** | — | **CLOSED 2026-07-25 — PASS.** All six exit items. **W→H proven with a picture; Murzak runs fully headless.** See below |
| ~~**L4**~~ | T2 × (i) | W-PRO · W-MUR · H control | — | **CLOSED 2026-07-25 — all three cells PASS.** Chartered over its conductor's objection (TCP-22) and **falsified four of the program's own positions** (TCP-31/32/33/34). See below |
| **L5 SEAM** | **T2 × (ii) FIRST, then × (i)** — door-connected second room; **subtractive editing is the novel primitive** | mode (ii) method-unconstrained; then **W-MUR · H · W-PRO** vs a frozen connection contract (**Matt roster, TCP-37 ②, with mid-run cell-cull authority**) | — | **IN FLIGHT 2026-07-25** — charter `2026-07-25-tcp-l5-seam-lap-charter.md`; exits through **recipe extraction + room #3 emitted from the recipe** (authoring-minutes room-2 vs room-3 = the serial-pipeline metric) |
| **L6 MONSTER** | **T5 static → motion** — monster standup, weapon in hand, then the swing | field — **and the first plausible instrument-capability FORK** (TCP-38 ③: `.fbx` needs the editor's import path; the wires live there, H does not) | static: L5 close · motion: **harness CLEARED** | **the lap's first question is now the asset pipeline, not the pose** |
| **L7 VFX** | **T4-VFX × (i)** then **× (ii)** | field + `Godot-AI-Particles` + Pro's `create_particles` | harness CLEARED — TCP-8 held, nothing borrowed, so instruments are scored on authoring not capture | **must declare a diff TOLERANCE before it renders** if its clips need glow (TCP-38 ①) |
| **L8 UI** | **T4-UI × (i)** then **× (ii)** | W-PRO · W-MUR · H control | L3 | **no new harness needed** — re-sequenced behind SEAM/MONSTER/VFX because the serial-pipeline question outranks the HUD question (TCP-37) |
| *(parked)* | **T3 NEW SCENE × (i)/(ii)** | field | **the STORY session** (Q44 deferred there 2026-07-24) | **blocked on story, not on tooling** — unchanged |

**Re-sequencing note (2026-07-24).** Matt deferred Q44 to the story session — *"we need to flesh the
story out further before we decide."* Correct: act-register is a consequence of what the acts ARE,
and settling it from tooling evidence would be the tail wagging the dog. **Only L6 waits.** An
expansion lap inherits the register of the scene it expands; a HUD has no act-register; VFX gates on
a harness. **L3 → L4 → L5 is a clear runway.** Meanwhile the story session now gates Q43's seven
persistence rulings, Q44, and L6 — making it the highest-value unfired item on the board.

### L3 — RESULT (CLOSED 2026-07-25 **PASS**; drax report `…/2026-07-24-tcp-l3-murzak-standup-run-report.md`)

**The headline: TCP-5's W→H path is CLOSED, with a frame.** The wire wrote a GDScript builder via
`script-create`; the lab Godot ran it headless in **0.30 s**; the output `.tscn` carries the exact
arithmetic progression specified and the frame agrees —
`~/Games/mcp-lab/evidence/frames/BUILT_wire_authored_builder.png`, eight pillars ringed on
`h = 1.0 + 0.35i`, judgeable by eye without a table. **The doctrine executed itself inside one tool:
MCP authors the recipe, headless script runs production.** I called W→H "the single most likely
winner of the whole program" on the strength of a *tool list*. It is now the only path in the field
demonstrated end-to-end by the instrument under test.

**A structural argument the frame hands us for free.** The generated builder used `looking_at()` and
the engine's own node API — it never wrote a basis by hand. **A wire-authored builder is
constitutionally incapable of L1's transpose trap**, which silently killed the T path (Python emits
`.tscn` text: row-major floats, basis vectors are the *columns*, emitting axes as triples writes the
inverse). That is not "W→H happened to be correct here." It is a class of error W→H cannot commit.

**Murzak runs fully headless — 39/39 tools, byte-identical name set.** This does not discipline the
three-orphaned-editor failure class; **it deletes it. L4 needs no editor window at all.**

- **P-B FALSIFIED (for Murzak).** Exactly **39 tools / 11 families**, `gamedev-mcp-server 9.2.0.0` +
  addon `0.19.1`, proto `2025-06-18` — **my audit's documented prior was exactly right.** First
  documented number in this program to survive contact with the wire. Pro's docs said 77; the wire
  served 175. **L-B's "trust the wire" stands; L-B's implied "docs always lie" does not.**
- **P-C CONFIRMED.** The ten `Godot-AI-*` packages are catalogued, **not installed** — 63 tools across
  10 packages, none live. Class split (read from `extensions.catalog.json`): **Class A** — Particles ·
  Tilemap · Navigation · Animation · **CSG** · **GridMap** — wrap built-in Godot, no dependency, all
  six **published on nuget.org at `0.1.0`**. **Class B** — PhantomCamera · Beehave · Dialogic ·
  Terrain3D — wrap third-party addons the installer explicitly **never** vendors. **Every capability
  that reopened this column is Class A**; every Class-B wraps an addon we do not use. **L4's opening
  move installs CSG + GridMap at PINNED versions** — the catalog declares them `version: null`
  (floating), and floating a `0.1.x` reference through a comparative lap makes it unreproducible.
- **P-D / P-E.** Asset import **50 s cold / 10 s warm**, cache reusable, **sibling .NET project
  viable — no Matt-gated conversion of `reincarnated-godot`.** TCP-17's fear did not materialize.
- **Latency corrected, see TCP-19.** Murzak steady-state **8.03 ms** vs Pro **8.33 ms** — same class.
- **Honest residues, self-reported:** an inherited orphan `gamedev-mcp-server` (PID 25887, listening
  since 00:43, outlived the editors I killed) found and reaped; **14 files + 17 dirs escaped to
  `~/.dotnet`** because `DOTNET_CLI_HOME` was not redirected — a partial TCP-18 constraint-1 breach,
  named with removal commands rather than buried. Exit state verified: no Godot, no server, port
  closed.
- **→ Matt (Q46):** the addon's **compiled-in default is Cloud** and it transmits `machine_name` +
  project identity **before any tool call**. A second Q45 violation in a different component from the
  banked `setup-mcp` one — and unlike that one, **this one actually transmits.**

### L2 — RESULT (CLOSED 2026-07-24; drax report `…/2026-07-24-tcp-l2-pro-calibration-run-report.md`)

**VERDICT: Godot MCP Pro 1.15.1 is an EXECUTOR, not an author.** It builds a correct node graph from
constants somebody else derived and cannot derive them. Its only route to a measurement is
`execute_editor_script` — GDScript over a wire — which is **M3 with added latency. Transport, not
rival.** Every later Pro result reads "given the right numbers, can it build."

- **P-A CONFIRMED** — 1307/1307 calls, zero failures, 776-node `.tscn`.
- **P-B CONFIRMED, decisively and dangerously** — see L-K instance #4. Zero `aabb|bounds|extents`
  matches across all **175** live tools.
- **P-C CONFIRMED** — hatch needed, worked first try, six decimals identical to `kit_measure.gd`.
- **P-D FALSIFIED** — 8.33 ms/call, not 114–180. See **TCP-15**.
- **Frames:** `reincarnated-godot/harness_logs/tcp_l2_2026-07-24/CONTACT_SHEET_tcp_l2.png` — PRO | M3 |
  `|diff| ×4`. **Geometry registered** (silhouette bbox agrees to ≤3 px of 1673; wall faces cancel to
  black). **Material failed** (whole-frame PRO 107.07 vs M3 37.24) — and the frame is the only thing
  that said so.

**Two ceilings past the predicate.** (1) *The white floor is P-B one level down* — the FBX carry 2
surfaces, `set_material_3d` is single-surface, and no tool reports a surface count. **Handing an
executor the dimensions is not enough**; the author/executor test should generalize to *dimensions +
surface count + node structure*. (2) **A Pro-authored scene does not round-trip through Pro** —
`add_scene_instance` calls `set_owner_recursive`, so internal nodes save owned *and* re-instance on
reload, colliding and renaming. **L4 must not assume a Pro-authored scene is re-addressable by Pro.**

**L-J amended by two residues the restore predicate did not cover:** Pro rewrites `project.godot`'s
`[autoload]`, and addon removal **silently empties the global class-name cache**. Byte-perfect file
restore is necessary and **not sufficient** — a rescan is required. (Restore itself verified 3×:
74 files / 36 `.gd`, byte-identical, `project.godot` sha256 exact.)

### L2 — PRO CALIBRATION (charter, retained)

**Not a competition — calibration.** Same logic that made drax calibrate `kit_measure.gd` against the
reference pack before trusting it: **if Pro cannot reproduce a known room, it cannot author a new
one**, and nothing it does in L4–L7 can be trusted. It also exercises the swap procedure, the
control-diff and the frame capture *once, on the cheap instrument*, before we spend the expensive one.

**One room, one NEW pack, control built in the same lap.** Full charter:
`2026-07-24-tcp-l2-pro-calibration-charter.md` (CHARTERED + DISPATCHED 2026-07-24).

*Amending my own §5 recommendation in the Pro audit, and the reason matters:* the control must be a
**fresh** M3 build of the same new pack, not an existing one — because a pack whose constants are
already derived and committed lets a Pro agent **read the answer instead of measuring it**, which
voids P-B. Same contamination guard the L1 charter §4c applied when it forced M1 to run before M3
existed. Pack picked by **measured** module compatibility (L-D); the measurement is the pick.
Pre-registered:

- **P-A** — Pro creates the node graph. *High confidence; tools documented.*
- **P-B** — **decisive.** Pro cannot measure an un-instantiated FBX. The
  instantiate→`get_node_properties` path is the test. If it yields an AABB, Pro has a complete if
  roundabout measure→build loop. If not, **Pro is an executor of constants derived elsewhere.**
- **P-C** — if measurement requires `execute_editor_script`, the verdict is **"transport, not rival"**
  — MCP as a slow wire for the method that already won.
- **P-D** — ≥32 s of pure wire latency for the instance placements alone (~280 × 114–180 ms).

### L4 — RESULT (CLOSED 2026-07-25 — **all three cells PASS**; reports `…/drax/notes/2026-07-25-tcp-l4{a-wmur,b-wpro,c-h-control}-run-report.md`)

**The lap Matt overruled me to run (TCP-22) falsified four of the program's own positions.** Had it
been cancelled on my forecast, all four would still be standing.

| | **W-MUR** (wire) | **W-PRO** (wire) | **H** (control) |
|---|---|---|---|
| Six clauses (mode-(i) conformance) | **PASS**, 4–5 dp | **PASS** | **PASS** |
| **Stair placement in Z** (TCP-35) | `z[−4.75, −3.15]` — dais **FRONT** | `z[−4.75, −3.15]` — dais **FRONT** | **`z[−8.75, −7.15]` — dais BACK, 4.000 m away.** All three conformant |
| Added-node topology | +14, flattened | **+18** — 4 semantic wrapper `Node3D`s | +14, flattened |
| P-2 outside-mask changed px | 30 / 1,730,817, max Δ **1** | **59**, max Δ 1 | **32**, max Δ 1, all LSB |
| Build cycles to land the spec | **3** | **3** | **5** |
| Wire calls / plans | 117 / 24 | 90 / 11 | n/a |
| **Cell wall-clock** (identical TCP-20 bracket) | **32m44s** | **22m58s** | **12m59s** — *execution 0.60 s* |
| Save-duplication | own-root-only → node count correct, **materials silently dropped** | own-all → **4 co-located duplicates**, 318 vs 314 | **avoided by FLATTENING** — 310/310, 0 duplicates |
| Detected by | **frame only** (white blobs) | **census only** (zero pixels moved) | both instruments, plus 1,480 structural assertions |
| **ROOM-COHERENCE** (TCP-28) | pillars **36.1% undersized**, 2 auto-generated debris names | pillars **exact to 5 dp**, 9 `uv1_scale` materials | **ADOPTED on all four modules**, 0 auto names of 14 |

**What the lap actually settled, in order of how much it costs the program:**

1. **TCP-32 — the cost model was wrong.** Execution 0.60 s against a 24-minute cell. Two rulings
   (TCP-15, TCP-19) were spent refining a per-call latency figure worth **under a second of a
   half-hour**. **Authoring is the entire cost, and mode (i) held it constant on purpose** — so this
   lap could not have found the winner even in principle, and now says so out loud.
2. **TCP-31 — both wires exonerated on the worst defect the lap produced.** The duplication is
   Godot's `PackedScene.pack()`, reproduced from plain GDScript with nothing on the wire. The
   flatten-and-right-compose route transfers to any tool that saves a `.tscn`.
3. **TCP-33 — "just write the script" needed more cycles than either wire**, because three of five
   attempts were spent discovering the substrate and the engine, not the spec. H's real advantage is
   **in-process assertion**, not speed.
4. **TCP-34 — my own blind-control protocol leaked the answer through the documents it mandated.**
   The ledger is now an answer key; blind cells need a redacted charter from L5 on.
5. **TCP-28 — and the axis that outranks all of it:** six clauses passed a scene with 36%-undersized
   pillars and two debris-named nodes. **Matt saw it in ten seconds from two pictures.** The rubric
   could not.

6. **TCP-35 — and this one is the sharpest thing the lap produced, found only by COMPOSITING.** The
   three cells built the stairs **4.000 m apart** — L4a and L4b at the dais's front edge, L4c at its
   back — and **all three PASSED**, because clause 2 never anchors Z. **Two cells filed a clause-2
   spec defect and filed different ones, because they had built different staircases.**

**And the defects that were MINE.** Clause 2 puts both stair flights **entirely outside the dais
footprint** (`|x| 3.00…4.20` against a platform ending at `|x| 3.00`) — architecturally poor, held
constant rather than fixed mid-lap, built as written by all three. **But TCP-35 is worse than that,
and the divergence is probably not the clause's — it is mine:** my L4b reconstruction dispatch
paraphrased the built geometry as *"arriving at its back corner against the wall"* when drax had
measured the **front** edge, and I propagated that sentence into the L4c dispatch as an emphasized
do-not-fix instruction. **The blind control built what I mis-described.** Third defect, the pillar
quilt, propagated to every cell as substrate per TCP-27 ③: **zero cycles burned on it. The
propagation worked.**

~~**Two open items**~~ **ONE open item.** The **four-cell contact sheet** SHIPPED 2026-07-25
(`evidence/l4/sheet/` — five rows plus full-res strips; note
`…/drax/notes/2026-07-25-tcp-l4-contact-sheet.md`), reassigned to the conductor per TCP-34 ③: one
render, blast radius clean, `user://` vacated. **It produced TCP-35 and TCP-36, neither of which any
individual cell could have found — which is the argument for compositing rather than tabulating.**
Remaining: the **pillar-quilt fix** in `reincarnated-godot`, a product change deliberately kept out
of the bake-off — **GO per TCP-37 ④, dispatched 2026-07-25**
(`dispatches/2026-07-25-drax-pillar-quilt-fix.md`). With that dispatch L4 has **zero** open items.

### L4 — T2 EXPANSION: the first lap the wire can genuinely win *(charter, retained)*

**CHARTERED 2026-07-25** — full charter at `2026-07-25-tcp-l4-expansion-bakeoff-charter.md`.

Existing scene, bounded modification, **no measurement needed** (constants already derived), **few
calls**. Every structural disadvantage the wire carried in L1 is absent. If MCP loses here it loses
everywhere; if it wins here that is the shape of its real job.

**Named GridMap prediction (W-MUR):** authoring through `gridmap-set-cell` **cannot produce L1's M2
failure class by construction** — orientation is an enum index on an integer grid, not a
`Transform3D` basis, so the transpose trap is unrepresentable. If true, GridMap is not a convenience;
it is a *correctness* property, and it is the first thing in the program that beats H on something
other than speed.

**The two axes that earn the lap** — and neither has ever been measured here:

- **P-2, NON-DESTRUCTION.** L2 found a **Pro-authored** scene does not round-trip through Pro:
  `add_scene_instance` calls `set_owner_recursive`, so internal nodes save owned *and* re-instance on
  reload, colliding and renaming. **Whether Pro damages a scene it did NOT author is untested** —
  and expansion structurally requires exactly that. Replica laps cannot ask this question.
- **P-5, ITERATION COUNT.** Every lap so far proxied "best at building" with **wall-clock**. None
  counted **author→look→fix cycles to land a spec**. That is the actual axis, and L4 is the first lap
  that counts it.

### L8 — T4-UI *(was "L5 — T4-UI first, before VFX"; re-lettered by TCP-37's runway — the SEAM lap took L5)*

Needs **no new harness** (a HUD is judgeable from a still) and is the **strongest untested case for
the wire**: at N≈12 controls with ~40 iterations, latency reverses — ~150 ms per wire nudge against
15–30 s per script edit→relaunch→screenshot cycle. Pro brings `set_anchor_preset` + the full theme
suite; Murzak brings node CRUD + `screenshot-viewport`.

### Blockers to clear

1. ~~**Motion harness**~~ — **CLEARED 2026-07-25** (`~/Games/mcp-lab/harness/`; report
   `…/drax/notes/2026-07-25-motion-harness-run-report.md`; ruling **TCP-38**). Ours, borrows
   nothing, ≈5 s per 90-frame 720p clip, deterministic to the byte **under the accumulator
   lockout** and tolerance-bound without it. **L-A is now satisfiable for motion** — L6's motion
   phase and L7 are unblocked on evidence. ~~**New blocker in its place: L6's FBX/`.glb` gap**
   (TCP-38 ③) — the animated corpus has no runtime import path, which is a *capability fork*, not
   a chore.~~ → **DISSOLVED 2026-07-25 by the L6-PREP probe (TCP-43): all three questions YES.**
   `godot --headless --import` runs with no GUI (2.78 s, from a dir with no `.godot/`), and the
   `.glb` round-trip carries channels, lengths **and root translation**. **T5 is not an
   instrument-capability fork.** The corpus packages as **one `.glb` per character carrying its
   whole clip library** (3,386 files → a handful of artifacts). **Two real L6 prerequisites replace
   it, neither a fork:** (a) **a Sidekick→`SkeletonProfileHumanoid` retarget is mandatory on both
   sides** — a raw pack clip binds 6% to the retargeted hero we actually ship; (b) ★ **this corpus
   contains NO MONSTER RIG** (TCP-43 ⑤ — `goblin-locomotion` is goblin-flavoured locomotion on the
   humanoid rig), so **the MONSTER lap must source its subject before it can start.**
2. **H1 register ruling** — **deferred by Matt to the story session** 2026-07-24 (*"we need to flesh
   the story out further before we decide"*). L6 cannot be judged without knowing what register a new
   room is supposed to arrive at. L1's contact sheet showed all three new rooms reading pale tan
   against a dark reference; that is the open question, and T3 inherits it. **Blocks L6 only.**
3. ~~**Murzak standup**~~ — **now lap L3, dispatched.** Two toolchain prerequisites the audit missed
   and recon found: **no `dotnet` SDK on this machine at all**, and **no Godot .NET editor build** —
   only the standard 4.6.3. Both install user-local under TCP-18's blast radius.
4. **Gutted-addon hazard** (drax, flag) — `npx …--install-addon` reads `plugin.cfg`, sees the right
   version, prints *"Addon is already up to date"* and exits **without an integrity check**. The
   installed W-INC addon was 3 `.gd` files against an expected 36. **A gutted addon never
   self-heals.** Any lap touching W-INC must file-count first.

## §7 — Matt interface

**Reserved to Matt (commitment-boundaries):**
- ~~**Cloud vs self-hosted for W-MUR**~~ — **RULED 2026-07-24 (Q45): self-hosted**, mechanism `stdio`
  (TCP-11). Nothing of ours transits a third party.
- ~~**`godot-cli login`**~~ — **DISSOLVED.** Custom connection mode requires no OAuth, no login and no
  token; the queue row was struck. There was never a credential to gate on.
- **Converting `reincarnated-godot` to .NET** — if L4 ever needs it, that is Matt's, not mine
  (TCP-17/18). L3 is charged with finding the route that avoids asking.
- **Any toolchain step requiring `sudo` or a machine-wide install** (TCP-18 constraint 3).
- **H1 register** — **deferred by Matt to the story session** 2026-07-24; L6 waits on it.
  ~~H2–H5~~ ruled by me as seam calls (TCP-12/13/14/16) — they were never his.
- Terminal quality verdicts on every mode-(ii) lap (§4).

**Conductor rules in-run (reasoning-boundaries), veto-open:** pack selection, lap ordering within the
sequence, prediction wording, honorable-fallback design, method attribution.

**Owner-eye checkpoints** *(desirable-run-pattern §6.2)*: mode-(ii) laps schedule Matt's eye at a
**named mid-trace point**, not only at the end. Both KIT-FIDELITY catches were his, mid-stream, when
the declared interface had put his eyes only at the finish.

## §8 — Fit test (desirable-run-pattern §3), per lap-type

| | F1 enumerable | F2 decidable | F3 pre-drainable | F4 authority-resident | → route |
|---|---|---|---|---|---|
| mode (i) laps | ✓ pack/scene/spec finite | ✓ control-diff | ✓ | ✓ | **autonomous run**, gandalf conducts |
| mode (ii) laps | ✓ brief + look-budget | ✓ **trace-completeness only** (§4) | ✓ | ✓ for process; ✗ for quality → Matt | **autonomous run + reserved terminal verdict** |
| standup (L3) | ✓ tool surface is finite + enumerable over the wire | ✓ readiness predicate, **behavioural not return-code** (L-K) | ✓ — Q45 ruled, mechanism ruled (TCP-11), blast radius pinned (TCP-18) | ✓ **now resident** — no credential exists to gate on (Custom mode needs none) | **autonomous run**, gandalf conducts |

## §9 — Ruling ledger (veto-open)

| # | Ruling | By |
|---|---|---|
| **TCP-1** | T4 runs **both** modes as separate laps | **Matt 2026-07-24** |
| **TCP-2** | Mode separation generalizes beyond T4 where meaningful and cheap (L-E) | gandalf, veto-open |
| **TCP-3** | Mode-(ii) exit predicate is trace-completeness, **never quality** (§4) | gandalf, veto-open |
| **TCP-4** | L2 reframed from competition to **calibration** | gandalf, veto-open |
| **TCP-5** | **W→H scored as a first-class path** (the wire authors the builder) | gandalf, veto-open |
| **TCP-6** | T4-UI sequenced before T4-VFX (harness dependency) | gandalf, veto-open |
| **TCP-7** | Capability verdicts expire; re-read manifests per lap (L-C) | gandalf, veto-open |
| **TCP-8** | The motion harness must be **ours**, not an instrument's, or the laps score capture rigs | gandalf, veto-open |
| **TCP-9** | **One wire installed at a time**; swap laps restore against a **file inventory**, never a version string (L-J) | gandalf, veto-open |
| **TCP-10** | L2's control is a **fresh** M3 build of a **new** pack — a pack with derived constants on disk voids P-B | gandalf, veto-open |
| **TCP-11** | Q45 ruled SELF-HOSTED; **mechanism = `stdio`**, not Docker (all three paths equally self-hosted; stdio is least machinery and how Claude Code natively runs MCP) | gandalf, veto-open — **Matt's word overrides** |
| **TCP-12** | **I7 RETIRED** (H3). The bit-identical reference-camera invariant is dead — it was authored against a 7.5 m room and the room is 17.5 m, so it frames floor only, and it has been unsatisfiable **two laps running**. **`__box` is the standing judgment framing** (same pitch/yaw/FOV/aim, dollied to fit, applied identically to every cell). **Boundary:** this rules the *harness reference* camera only. The **product** camera (Camera B′ / E4, Matt-ruled) is a different artifact and is untouched | gandalf, veto-open |
| **TCP-13** | **H4 ruled.** The **rig** owns aura colour, through the shader's **declared** uniforms (`primary_color`/`secondary_color`/`tertiary_color`). Host-side writes to undeclared uniforms are forbidden — they are L-K instance #2. Any host→shader write validates against the declared uniform list or is not made | gandalf, veto-open |
| **TCP-14** | **H5 ruled.** G4 collision is **not** owed by rooms that are only photographed. It becomes a **hard gate on the first lap that produces a room intended to be walked**, and no such room passes without it. L1's and L2's rooms are photographic; the debt is real but not theirs | gandalf, veto-open |
| **TCP-15** | **P-D FALSIFIED — my latency constant was stale by ~14×.** Measured on Pro: **8.33 ms/call** (1307 calls, 10.886 s), not 114–180 ms. **Latency is not the wire's binding constraint**, and my bake-off claim that *"the wire will never carry assembly"* was a one-instrument constant generalized to a category — **the same error class, fourth instance.** Consequences: the T4-UI case gets *stronger*, not weaker; L4's three-way is worth running on capability rather than conceding on speed. M3 still wins outright on this task at **1.09 s** for the same room *plus* void caps and shaders | gandalf, veto-open |
| **TCP-17** | **L3 runs OUTSIDE `reincarnated-godot`. Mandatory, no exceptions.** Verified 2026-07-24: the project is **pure GDScript on Godot 4.6.3, non-.NET** — no `.csproj`, no `.sln`, no `[dotnet]` block, `config/features` lists only `("4.6","Forward Plus")`, and `/Applications/Godot.app` is the standard build. **Murzak is a C# addon and needs the .NET editor build + `Godot.NET.Sdk` + a `.csproj`.** Standing it up in the live project would add `C#` to `config/features` and make the project effectively **.NET-only** (the standard editor then errors on it) — a change to Matt's standing product environment, i.e. an external-state commitment-boundary, not a lap decision. Outside it, the same work is a reasoning-boundary and stays mine. ~~**SCRATCH CLONE**~~ **AMENDED before dispatch — the clone form was falsified by its own recon.** `git clone` yields **2.67 MiB against 18 GB on disk**: the whole Synty tree is gitignored under the license rule, so a clone is scripts with no assets. **And L3 needs no assets** — a standup lap proves a wire, not a room. So L3 runs in a **fresh minimal .NET project** in a lab dir. The asset question moves to **L4**, where it is real, and **L3 is charged with measuring it** (symlink one pack, time the import) so L4 launches informed instead of surprised | gandalf, veto-open |
| **TCP-18** | **Toolchain installs for L3 are a reasoning-boundary, under a pinned blast radius.** Neither `dotnet` nor a Godot .NET editor exists on this machine; Murzak cannot run without both, and Q45 ruled self-hosted *before* that requirement was visible — so this is a genuinely new axis and I am ruling it rather than parking a whole runway (L4 **and** L5 gate on L3). It stays a reasoning-boundary **only** under five constraints, and any one of them failing is a HALT to gandalf, then to Matt: (1) **everything lands in `~/Games/mcp-lab/`** — not in any of the four product repos; (2) **`/Applications/Godot.app` is never touched, replaced or upgraded**; the .NET editor installs side-by-side in the lab dir; (3) the .NET SDK installs **user-local via `dotnet-install.sh --install-dir`** inside the lab dir — **no `sudo`, no system-wide install, no PATH edit outside the lap's own shell**; removal is `rm -rf`; (4) **`reincarnated-godot` ends the lap byte-unmodified**, verified by a clean `git status` *including untracked*; (5) the **uninstall procedure is written down** as part of the deliverable. **If any step demands `sudo` or a machine-wide install, stop — that is Matt's call, not mine** | gandalf, veto-open |
| **TCP-19** | **The latency number is corrected AGAIN — and this time the fix is the STATISTIC, not the number.** L3b withdrew its own banked figure: *"114 ms/call, 14× spread vs Pro"* was a **mean contaminated by 10-second disconnected-wire retries.** Server-side median across 252 calls: **3.67 ms**; true steady state **8.03 ms** against Pro's **8.33 ms** — *the same class.* **TCP-15 is NOT amended** — it records a falsification with its own evidence and date, and overwriting it would hide the error trail this program is partly valuable for. TCP-19 supersedes the number and names the method: **every performance claim in this program states its statistic, its n, and its exclusions. Medians, never bare means. A mean containing timeout retries is not a latency measurement.** Error-class tally, said plainly: this is the **fifth** instance of a number measured in one condition generalized to a class, and the fourth of them was **mine — I relayed drax's 114 ms to Matt as a 14× instrument spread before it was withdrawn.** A median would have caught it at either hop | gandalf, veto-open |
| **TCP-20** | **The blast-radius predicate was STRUCTURALLY BLIND, and it was my charter's defect.** L3b §4.4 made *"clean `git status` including untracked"* the proof that the product repo was unharmed — of a repo whose **entire 18 GB of value is gitignored** under the Synty license rule. The same charter then prescribed P-E's **symlink**, which would have written `.import` rewrites into exactly that blind spot, while making writes to that tree a HALT. **A self-contradicting predicate: it forbade an act it also instructed, and could not have detected it.** drax substituted a copy at the mirrored path (1 s) and verified four ways including a **2494-file fingerprint. That fingerprint becomes STANDING** — answering drax's second escalation: **any lap touching a repo with gitignored payload takes a file-count + fingerprint of the ignored tree before and after; `git status` alone is not a blast-radius predicate there.** Generalized: *a verification predicate must cover the surface that carries the value, not the surface that happens to be tracked*. **AMENDED 2026-07-25 — the amended predicate had a hole of the same class, found by its own author.** `~/Library/Application Support/Godot/editor_settings-4.6.tres` is **shared by both Godot builds** and was rewritten by a plain `--script` run with **no `--editor` flag anywhere** — a machine-global surface outside `~/Games/mcp-lab/`, outside every product repo, and outside the fingerprint. No baseline existed to diff against. **Third recurrence of one error: a predicate that does not cover the surface being written.** The out-of-lab surfaces are now baselined and the fingerprint tool covers them | gandalf, veto-open |
| **TCP-21** | **L-K gains its converse, because the law was one near-miss from becoming a paranoia generator.** L3b almost filed a sixth L-K instance: a mesh assignment looked like textbook silent failure and was **a missing `scene-save` — operator error, not instrument mendacity.** One tracked relaunch exonerated the tool. **Amendment: an L-K instance requires BOTH that the tool reported success AND that the operation was correctly invoked.** Without the second clause a law meant to catch lying instruments starts convicting innocent ones, and a program that mis-attributes its failures is worth less than one that has none — mis-attribution is the *only* failure this program calls real (L-G). drax's own words are the rule: **"the independent read exonerates as well as convicts."** | gandalf, veto-open |
| **TCP-16** | **H2 disposition (not a Matt call).** R2's flat cream floor is **accepted as a lap artifact** — an experimental room that will never ship. Program consequence: dressing selection must verify **measured texture presence**, not merely a valid material slot (L-K instance #3, and L2 found it one level deeper: the FBX carry **2 surfaces** while `set_material_3d` is single-surface, and **no tool reports a surface count**) | gandalf, veto-open |
| **TCP-26** | **L-K instance #6 — and a NEW SHAPE: the tool is correct HALF the time.** W-MUR's `node-modify` on `MaterialOverride`: against a **null** property it resolves the ref and saves a proper `ExtResource` — **correct**; against an **already-set** property it builds a blank default and saves an **empty `sub_resource`**, texture gone. **Same tool, same argument shape, no error either way, `Success` both times.** Every prior L-K instance was a tool that lies *consistently* — those are findable by one careful probe. **An intermittently-correct tool defeats probing**, because the probe that passes proves nothing about the call that follows. **Twelve `Success` returns did not catch it; four white pillars in a rendered frame did** — L-A doing the job the tables structurally cannot. Workaround verified (null-first), and the trap fired **a second time** on the steps, so it is a standing property of the instrument and not a one-off. **Program consequence: an instrument's verdict must state whether its failures are consistent or state-dependent** — the two demand completely different verification budgets | gandalf, veto-open |
| **TCP-27** | **CELL HYGIENE + the two substrate notes that must propagate, or P-5 is corrupted.** ① **The exit predicate's contact sheet is assembled from BANKED FRAMES, not re-rendered scenes** — TCP-23 already forces one scene per process, so cells are never shot together anyway. Therefore **each cell banks its frames + diff and then VACATES the project directory** (outputs to `prep/l4<x>_residue/`, byte-identical re-render verified before the move). Answering drax's escalation: `scene_l4a_wmur.tscn` carries **every solved placement** and `mesh_platform.tres` is literally `size = Vector3(6, 0.6, 4)` — the spec's arithmetic, and P-6's hard-won node structure, sitting in the directory the next two cells work in. ② **P-2's passing floor is NOT prep's zero point.** Prep calibrated self-diff to **0 of 2,073,600**; L4a measured **30 changed pixels, every one at channel delta exactly 1, 29 of 30 within 20 px of the mask hull.** A legitimate addition *moves the shadow at the mask edge* — so the floor is ~30 LSB pixels, not zero. **Publishing prep's 0 as the pass bar would convict every honest cell.** ③ **The pillar banding is IN THE SUBSTRATE.** L4a's added pillars read as rainbow atlas bands; drax nearly filed it as his own defect, measured instead (same mesh, same UVs to five decimals, same texture, same scale) and shipped a side-by-side control proving the added pillar and the room's own are **indistinguishable**. It is invisible at `__box` only because the room's corner pillars are **~89% buried in the walls**. **This must be published to L4b and L4c or each burns a cycle "fixing" a non-defect — and P-5, iteration count, is this lap's headline metric.** Substrate knowledge propagates; method knowledge does not | gandalf, veto-open |
| **TCP-23** | **CAPTURE ISOLATION — one scene per process, standing, every lap.** L4-PREP could not satisfy *"self-diff must be EXACTLY zero"* and refused to call the residue noise. Six renders across three processes: all three **position-1** frames byte-identical, all three **position-2** frames byte-identical — **capture ORDER was leaking into the pixels.** And the drift **grows**: q1↔q2 = 2 px in a 5×2 bbox, q2↔q3 = 7 px in a **507×217** bbox. **So it is not warm-up, and discarding a first frame would not have fixed it.** One capture per process is byte-identical across processes and equals q1 exactly; under that rule the zero point is **0 changed pixels of 2,073,600.** Enforced in code — `l4_shoot.gd` refuses a second scene and exits non-zero (the `editor_up.sh` principle: make the failure impossible rather than trusting the operator). **Consequence for this lap's own exit predicate: the four-cell contact sheet is FOUR PROCESSES, not one**, or three of its four cells are photographed under drifted state and every P-2 number carries an undeclared contaminant. Nothing bounds that contaminant for a scene with more shadow casters. **The strictness is what found it** — had I written "small", 2 px would have been filed as noise | gandalf, veto-open |
| **TCP-24** | **L2's P-2 ATTRIBUTION IS WIDENED — the duplication is GODOT's, not Pro's. Sixth instance of the error class, and this one I ratified.** L2 recorded *"a Pro-authored scene does not round-trip through Pro"* and attributed it to `add_scene_instance` calling `set_owner_recursive`. L4-PREP **reproduced the same duplication from a plain headless GDScript builder with no MCP server running** — 808 nodes in, **1320 out** at room scale. Three routes measured, **none gives both correct node count and surviving materials**: own-all `GEN_EDIT_STATE_DISABLED` 4→**6**; own-all `…_INSTANCE` 4→**6**; own-root-only 4→4 but surface overrides 2→**0**, silently dropping every material. Edit state strips `type=` from the instance *root* line only, not from the child. **The mechanism is `PackedScene.pack()` serializing instanced sub-scenes — a property of Godot's SAVE path.** ① **L2's observation STANDS; its attribution was too narrow, exactly as a one-condition measurement generalized to a category** — the same error that produced the 114 ms latency constant twice, *"the wire will never carry assembly,"* and *"Pro has no gridmap."* ② **Why production never saw it, and this is load-bearing beyond the lap:** `reincarnated-godot` builds scenes **at runtime, in memory, and never saves a `.tscn`** — our production idiom is structurally immune to a hazard every scene-authoring tool must face. ③ **Confound removed at PREP, not papered over:** the substrate is flattened to plain `MeshInstance3D` with the FBX-internal transform composed on the right, round-tripping **296 nodes / 540 surface overrides in → 296 / 540 out**, which is also *fairer to the wire instruments* — every piece is addressable by node path instead of buried behind an instance boundary. ④ **The hazard is NOT removed from the ADDED geometry** — pillars and props are FBX, and it becomes prediction **P-6** | gandalf, veto-open |
| **TCP-25** | **TCP-16 amended: measured texture presence discriminates on the MEAN, never on variance.** L4-PREP's automated "is it textured" test **PASSED an untextured white brazier** — shading alone creates variance, and Synty atlas-mapping reads flat by design, so the two signals overlap. Means separate cleanly: **206 untextured vs 82 textured.** A check that cannot fail on the case it exists to catch is not a check, and it would have shipped an untextured prop into all three cells identically. Caught by *looking at the frame*, not by reading the counter — which is L-A doing the job the tables could not | gandalf, veto-open |
| **TCP-22** | **A CONFIDENT FORECAST IS NOT A SUBSTITUTE FOR A LAP — Matt overruled the conductor, and was right to.** After L3 closed I recommended **cancelling L4's three-way** and promoting L5, on the argument that the outcome was already known: the wire is a feedback loop, H is the builder, and expansion would show it again. Matt: *"Maybe you know how it ends but I want to see the requested bake off."* **My entire case was a prediction — inside a program whose founding discipline is that predictions are PRE-REGISTERED AND THEN MEASURED.** My prediction record here is **five wrong generalizations**, four of them mine: the 114 ms latency constant (twice), *"the wire will never carry assembly,"* *"Pro has no gridmap"* (77 documented vs 175 live), and the scratch-clone premise falsified by its own recon. **The standing rule: the conductor may recommend cancelling a lap, but a lap whose only argument for cancellation is the conductor's forecast of its result is a lap that MUST run.** Cancelling on forecast is the program grading its own homework. L4 is chartered, and its §0 records this as its reason for existing | **Matt, ruling over gandalf's recommendation** |
| **TCP-28** | **THE CONFORMANCE RUBRIC PASSED BOTH CELLS AND WAS BLIND TO EVERY DIFFERENCE THE OWNER SAW IN TEN SECONDS.** Matt, shown L4a and L4b side by side: *"The only differences I can see are stair texture and pillar size. The PRO pillars are wider."* Both true, both measured, and **neither is in the six clauses.** ① **Pillar scale.** W-PRO `Dais_Pillar_L/R` = `(1.56392, 1.01682, 1.56392)`. Derivation: `PILLAR_WORLD_FOOT = 1.082276×0.62 = 0.671011` ÷ `pillar_native_w 0.429056` = **1.56392**; `PILLAR_WORLD_H = WALL_H×1.02 = 3.065858` ÷ `pillar_native_h 3.015154` = **1.01682**. **Exact to five decimals — Pro read the handed kit constants and applied the ROOM's sizing convention.** W-MUR shipped scale `(1,1,1)`, native FBX: a **0.4291 m** footprint against the room's own corner pillars at **0.6710 m** — **36.1% narrower than every other pillar in the scene it joined.** ② **Texture density.** L4b carries **nine** materials at `uv1_scale (0.8,0.8,0.8)`; L4a and `scene_before` carry **none**. Pro made a deliberate art call — and thereby *diverged* from the room's convention where it *matched* on sizing, so this is mixed, not uniformly better. ③ **Node hygiene, which Matt did not need to see for it to be real.** W-PRO: `Dais_Pillar_L`, `Dais_Brazier_R`, `Dais_Step_L1` — semantic throughout. W-MUR: **`_MeshInstance3D_27179`** and **`_MeshInstance3D_27180`** — its −X pillar and −X brazier shipped with auto-generated debris names, the visible consequence of L4a's own recorded ceiling (`Name` unsettable via `node-modify`). **The ruling:** a mode-(i) conformance rubric measures **fidelity to the spec**, not **quality of the scene**, and therefore **cannot rank instruments on output.** Six clauses PASSED a scene with undersized pillars, no texture-density call, and two unnamed nodes. **Third firing of the rubric law (`desirable-run-pattern.md` §6.3) inside one lap** — after the flanking-stairs spec defect and the pillar-quilt mis-attribution. **Standing addition: every T2+ lap scores a ROOM-COHERENCE axis — does the addition adopt the conventions of the scene it joins (module scaling, material density, naming)? — judged at the frame and reported per cell.** It is not a clause; it is the axis the clauses structurally cannot reach. Attributed to **Matt, from two pictures, ahead of the instrument** | **Matt observation**, gandalf ruling, veto-open |
| **TCP-29** | **L-J AMENDED — the inventory compares CONTENT PER PATH, and engine-generated sidecars are a declared benign delta.** L4b's swap grew Pro's addon **44 → 79 files (+80%)** while `plugin.cfg` read `1.15.1` throughout. I relayed that to Matt as *"the version string lied by 35 files."* **drax attributed it, and the attribution changes the finding:** all 35 additions are **`.uid` sidecars, one per `.gd`, exactly one-to-one** (35 `.gd` in → 35 `.uid` out), **0 removed, 0 content-changed, all 44 banked files byte-identical at restore.** The mechanism is **Godot 4.4+ script-UID sidecar generation on project scan** — Pro's files were never touched. **What this does to L-J is make it stronger, not weaker.** L-J's founding evidence was a **gutted** addon reporting healthy (3 `.gd` against 36 expected); this is the **grown** addon reporting healthy. **Both failure directions have now been observed on one procedure — and they defeat different checks.** A *count* check false-alarms here and catches the gutting; a *version* check misses the gutting and stays quiet here; **only a per-path content inventory distinguishes a benign accretion from a real corruption.** Amendment as drax proposed it: the restore predicate compares by content per path, and **new engine-generated sidecars are an expected non-corrupting delta** — without this the next swapping lap HALTs on a benign `.uid` bloom, which is a false conviction and those are the only failures this program calls real (L-G). Murzak's restore verified **361/361 OK, 0 FAILED** | drax attribution, gandalf ruling, veto-open |
| **TCP-30** | **THE CONDUCTOR HAS A CONVICTION BIAS, AND IT IS NOW MEASURED AT THREE-FOR-THREE IN ONE SESSION.** Every defect I have attributed to an instrument this session has, on deeper reading by the executor, belonged to **Godot or to our own code**: ① **TCP-24** — L2's scene duplication, which I ratified against Pro's `set_owner_recursive`, reproduces from a plain headless builder with no MCP server; the mechanism is Godot's `PackedScene.pack()`. ② **The pillar quilt** — I filed it as a live hypothesis pointing at PREP's flattening; it is `kit_replica_level.gd:770/:808` applying `tex_atlas` unconditionally to a module the pack declares `Uses custom shader` (no albedo), in all five kits, with the fix already living in `render_catalogue.gd` since Matt's 2026-06-21 quilt review and never back-ported. ③ **TCP-29** — the addon "growth," which is Godot's sidecar generation. **Three for three, and the direction is always the same: I convict the tool.** This is structurally dangerous *because* the program exists to judge tools — a conductor biased toward conviction produces a field report that reads as evidence and is partly an artifact of its author. **Standing rule: an attribution to an instrument is not final until it has been tested against (a) the engine and (b) our own harness.** The control that settles it is usually cheap and usually already exists — the catalogue thumbnail that exonerated the pillar FBX was rendered a month ago, and TCP-21's converse already said it: **"the independent read exonerates as well as convicts."** I wrote that law and then broke it three times in a day | gandalf, self-filed, veto-open |
| **TCP-31** | **THE DUPLICATION HAZARD IS GODOT'S, UNIVERSALLY — PROVEN WITH NOTHING ON THE WIRE. BOTH INSTRUMENTS ARE EXONERATED, AND THE ROUTE THAT SURVIVES IT IS WRITTEN DOWN.** L4c's route **flattens**, so the hazard structurally could not touch its deliverable — which is an answer to the spec and **not** an answer to P-C3. drax ran the experiment the deliverable had declined: `l4c_dupprobe.gd` instances the same four FBX the dais needs, saves, reloads, counts — **plain GDScript under `--headless`, no MCP server, no addon, no port.** Result: own-all `GEN_EDIT_STATE_DISABLED` **9→13**, own-all `…_INSTANCE` **9→13**, own-root-only **9→9 but textured surfaces 4→0.** **TCP-24's three-route trilemma reproduced exactly, at addition scale, with nothing between the author and the engine.** The `+4` is not a coincidence — four instanced FBX, four duplicates, and **four** is precisely what L4b shipped from those same four pieces. **W-PRO is exonerated for the largest defect the lap produced and W-MUR is exonerated pre-emptively.** ★ **The transferable artifact — instantiate the FBX in memory, lift `MeshInstance3D.mesh` off it, compose the FBX-internal transform ON THE RIGHT, emit one plain `MeshInstance3D`, free the temporary.** `out.transform = Transform3D(Basis().scaled(scale), placement) * internal`. **The right-composition is not optional:** the pillar FBX carries a **+0.004478 m Y** offset on its internal mesh node — instancing applies it for you, naive extraction silently drops it, and composed it reproduces the substrate's own seat exactly (`0.6 + 1.0168164 × 0.004478 = 0.6045533`). No sub-scene boundary reaches the save path, so `pack()` has nothing to double. **Honest limit:** our production idiom builds at runtime and never saves a `.tscn`, so it was never exposed; **every scene-authoring tool is, and flattening is what lets a `.tscn`-saving one survive.** **TCP-30 firing #4 — and the first one caught BEFORE the conviction was filed**, by a control the executor built specifically to test his own conductor's standing attribution | drax experiment, gandalf ruling, veto-open |
| **TCP-32** | ★ **P-C5 FALSIFIED — AUTHORING IS THE ENTIRE COST, AND THE PROGRAM HAS BEEN MEASURING THE ~1% TERM.** Predicted: H lands under **one tenth** of either wire. Measured on the identical TCP-20 blast-radius bracket for all three cells: **W-MUR 32m44s · W-PRO 22m58s · H 12m59s** → **0.40× and 0.57×. Falsified by a factor of four to six.** The number that explains it: **pure execution is 0.60 s per full run, 282.5 ms of it the builder's own build-and-save** — opening a 296-node scene, deriving a wall it was never told about, adding 14 nodes, writing a 310-node `.tscn`. **Execution is free. The cell still took ~24 minutes** (~11 min reading + authoring, ~8 min build/look/fix, the rest instruments). Netting out the four instruments L4c had to build and the others did not puts H nearer 6–7 min — **0.20×–0.30×, still not 0.10×; it falsifies either way.** **What this does to the program is larger than the lap.** Every prior lap proxied *"best at building"* with **wall-clock**, and TCP-15/TCP-19 spent two corrections refining a **per-call latency** figure — 114 ms → 8.33 ms → 3.67 ms median. **All of that was refining a term worth 0.60 s of a 24-minute cell.** Latency was never the binding constraint and neither is execution; **the binding constraint is the human-or-agent authoring loop, which is exactly what a mode-(i) held-constant spec was designed to hold still.** Consequences: ① **speed claims in this program state execution AND authoring separately, or they are not claims**; ② the wire's per-call overhead **cannot** decide the field, which strengthens the L5-UI case (TCP-15 already pointed this way and this closes it); ③ **the ~1000× execution advantage is real and nearly irrelevant** — a bake-off that reports it as the headline is grading the wrong axis. **The one number that matters is how long it takes to know what to build, and this lap held that constant on purpose** | gandalf, veto-open |
| **TCP-33** | **P-C1 FALSIFIED — H NEEDED MORE CYCLES THAN EITHER WIRE (5 vs 3 vs 3), ON A TASK WHOSE ANSWER WAS HANDED OVER IN NUMBERS. AND THE REASON IS THE FINDING.** Predicted with *high confidence*: one cycle, because nothing is left to discover. **Three of H's five attempts were spent discovering things about the SUBSTRATE and the ENGINE that no spec could have contained:** ① `get_global_transform()` **returns IDENTITY out of tree** — inside `SceneTree._initialize()` the subtree is not in the tree, so every world read came back **shaped exactly like the answer**, the floor derivation "succeeded" against LOCAL AABBs and reported a **1.25 m room**; only a second, independent derivation failed loudly. *(Not an L-K instance under TCP-21's two-clause test — Godot printed 13 errors, so the operation was also incorrectly invoked. It is L-K's signature wearing engine clothes, and it is the **second** appearance of this exact defect in one lap: L4b's executor found the same identity-transform trap in his own verifier, where it made clause 5 vacuous. **A world-transform read on an out-of-tree node is now a standing trap in this stack — compose it from the node chain.**)* ② **"flat" is not "floor"** — 28 `WallCap` boxes are also under 0.2 m tall, at y≈3.09 out to |x|,|z|=9.2; merging them reported an **18.4 m room with its floor top at y=3.169743.** ③ Texture density, twice, both caught by looking. ★ **The sub-ruling, and it generalizes past this program: a cross-check that REPORTS and does not GATE is decoration.** Cycle 2's cross-check printed `DISAGREE` **and let the build proceed.** It is now a hard gate. ★ **The transferable asymmetry, and it is H's real structural advantage — not speed: 3 of 5 attempts and 2 of 3 fixes were caught by assertions INSIDE the authoring instrument, before any frame existed, at 0.60–1.10 s per attempt.** The instrument that authors is the instrument that checks, in the same process, for free. **A wire cannot assert against its own build without a round trip, and that is a property of the architecture rather than of any vendor's tool list** | gandalf, veto-open |
| **TCP-34** | ★ **THE BLIND CONTROL WAS CONTAMINATED BY THE DOCUMENTS THAT ORDERED IT BLIND — A RUNNING RULING LEDGER IS A GROWING ANSWER KEY.** I signed the L4c dispatch predicting *"this charter's most likely defect is §1: I may have failed to name a file that leaks the answer."* **drax found it and corrected the shape: the leak is not an unnamed file, it is the named ones.** §1 forbade both solved scenes, both residue dirs and both prior reports — then §1 **mandated** the program charter, whose ledger publishes **TCP-28**: W-PRO's solved pillar triple `(1.56392, 1.01682, 1.56392)` with its full derivation, W-PRO's verbatim naming scheme, its `uv1_scale`, and **the prop identity — which is clause 4's answer**; and **TCP-27 ①**, which quotes `size = Vector3(6, 0.6, 4)` — clause 1's arithmetic — inside the ruling explaining why that arithmetic must be hidden. **A large fraction of the answer was delivered by the two documents that forbid the answer, and it arrived before the blind control had formed an intent.** drax declared it at **banking time, before building** (13:17:56), which is the only reason the contamination is measurable rather than suspected. **Consequence for P-C4:** H landed `PILLAR_WORLD_FOOT` exact to **nine** decimals and adopted the room's conventions on all four modules with **0 auto-generated names out of 14** — but *"it can import the constants rather than infer them"* is not what was tested. **P-C4 measures transcription fidelity, not derivation.** The executor is the one who said so. **Standing fix for L5+: a blind cell gets a REDACTED charter, or per-cell results move out of the ruling ledger into cell-scoped notes the ledger cites by reference.** ★ **Structural generalization: this program's own accumulating record is now an attack surface on its own controls.** Three further charter defects, filed by the same cell: ② **the four conformance close-ups are REQUIRED but UNDEFINED**, and their only prior definition lives behind the forbidden wall — **unsatisfiable as written by a blind control**; resolved under L-F by defining four fresh close-ups with every parameter on the command line, **not claimed to match L4a/L4b's crops.** ③ **the lap charter assigns the H dispatch a deliverable §1 forbids it to build** — §5.1's four-cell contact sheet requires reading `evidence/l4/l4a|l4b/**`. **Correctly escalated rather than resolved by reading; the conductor assembles it, or a non-blind pass does.** ④ **the vacate predicate does not reach `user://`** — `l4a_p6_roundtrip.tscn` sits in Godot's userdata, **outside every forbidden path**, a solved-scene-shaped file a blind cell could have opened without breaking a stated rule. **Not opened. Fourth recurrence of one error class: a predicate that does not cover the surface being written** (TCP-20 twice, TCP-27 ①, now this) | drax findings, gandalf ruling, veto-open |
| **TCP-35** | ★★ **THE THREE CELLS BUILT THE STAIRS 4.000 m APART, ALL THREE PASSED, AND THE DIVERGENCE IS THE CONDUCTOR'S.** Found by **compositing the contact sheet**, off the three saved `.tscn` files — not by any cell, and not by the rubric. **L4a and L4b: `z[−4.75, −3.15]`, arriving at the dais's FRONT edge. L4c: `z[−8.75, −7.15]`, arriving at its BACK edge, hard against the far wall.** X identical (`±3.6`), Y identical, **Z differs by exactly the platform's entire depth.** ① **No number in any report is contradicted — nobody put the three numbers next to each other.** L4c could not (blind); L4b's reconstruction compared only against L4a and found them identical, which they are. ② **Both readings are literally conformant**, because clause 2 fixes rise, run, width, the ±X ends and the climb direction and **never anchors Z.** **Six clauses passed three cells and are blind to a 4 m displacement of an 8-node module** — TCP-28's structural defect, **second instance, 16× larger (4.000 m against 0.242 m)**, and found the same way: by an eye on composed pictures, never by the rubric. ③ **The corroboration was already in the reports, unnoticed: two cells filed a "clause 2 spec defect" and filed TWO DIFFERENT ONES** — L4b *"arrives level with the dais top but standing off the slab in X"*; L4c *"climbs away from the room, arriving at the back corner; whoever uses it walks up into a corner and turns around."* **They were describing two different staircases and neither could see the other's.** ★ ④ **ATTRIBUTION, AND IT IS MINE.** My L4b reconstruction dispatch §3.2 described the built geometry as *"entirely outside the dais footprint, **arriving at its back corner against the wall.** Both cells built it faithfully"* — **which was wrong about both scenes it described**; drax had measured `z = −4.75`, the dais **front** edge, and said so in the report body without flagging my paraphrase as an error. **I then propagated the wrong description verbatim into the L4c dispatch §2 as an emphasized DO-NOT-FIX instruction — the one section whose entire purpose was to stop the control deviating — and the control built exactly what I described.** The clause's Z-ambiguity is real and independent; **the 4 m divergence is far more likely my sentence than two independent readings.** **Standing rule: a dispatch that restates built geometry QUOTES THE EXECUTOR'S MEASURED NUMBERS. A conductor's recollection of a scene is not a description of it, and in a blind cell it is a steer.** ⑤ **CONFOUND, DECLARED RATHER THAN BURIED:** L4c did not build the same object as L4a/L4b, so every cross-cell figure in this lap spans geometrically different scenes. Most axes are unaffected (identical module count, identical arithmetic, identical difficulty — eight boxes at a different Z), but **P-2's outside-mask numbers (30 · 59 · 32) diff against mask hulls in different places with different shadow spill**, and row 2's detail crops photograph different objects. **Neither the verdict nor any cell's PASS changes; the comparison's precision does, and it is now stated** | drax finding, gandalf ruling + self-attribution, veto-open |
| **TCP-36** | **THREE SMALLER FINDINGS FROM THE SAME COMPOSITION, EACH STANDING.** ① ★ **A CONTROL FRAME'S CAPTION CAN OUTRUN ITS CONTROL.** L4a banked `CONTROL_pillar_room_vs_added.png` under *"they are indistinguishable"* to settle the atlas banding. Measured on that frame the two pillars are **exactly the same on-screen width — 88/88 px** — because `l4a_pillar_compare.gd` assigns **`Basis.IDENTITY`** to both clones, **discarding the room pillar's `scale = (1.5639, 1.0168, 1.5639)`.** For the *texture* question that is arguably the right control; **no number in L4a is wrong.** But read as a room-vs-added control it **positively certifies a size match that is 36.1% out** — the exact difference Matt caught by eye, divided out of the frame filed to answer it. **Fix: name a diagnostic frame for the VARIABLE IT HOLDS CONSTANT, not for the objects in it.** ② ★ **THE ROOM-COHERENCE REFERENCE IS NOT PHOTOGRAPHABLE IN THE ROOM IT BELONGS TO.** The substrate's own pillars sit at `(±8.975, ·, ±8.975)` against wall inner faces at `±8.75`: the part ever inside the room is a `0.1105 × 0.1105 m` corner nub — **2.7% of the footprint by area** — and at the detail camera the nearest projects off the top of frame at 25.8 m depth. **There is no frame in any of the four scenes in which the reference the whole TCP-28 axis is defined against can be seen at its true size.** drax shipped a **computed caliper** instead — the `0.671010 m` footprint projected through the declared camera at one declared height, identical pixels in all four tiles, validated against the images (predicted 1095.3 vs measured 1100). **It works: W-PRO and H fill it, W-MUR sits visibly inside it.** Standing: **an axis needs a photographable reference or a computed overlay, decided ONCE — not improvised per lap.** ③ **Clause 4 is under-pinned the same way as clause 2** — symmetry about X=0 and nothing else; braziers landed at `x = ±1.2 / ±1.5 / ±1.0`, **all three PASS**. And **W-PRO's `+18` against W-MUR's and H's `+14` is four semantic wrapper `Node3D`s, a naming choice and not a defect** — three instruments, **three different scene topologies for the same 13 visible meshes**, and clause 5 is structurally silent on all of it because non-destruction only asks what did **not** change | drax findings, gandalf ruling, veto-open |
| **TCP-37** | **MATT'S FOUR RULINGS ON THE POST-L4 RUNWAY, VERBATIM, AND A NEW INTERFACE PATTERN.** Asked to ultra-think the next test toward *"our serial modular asset compilation and development pipeline,"* the conductor recommended the L5 SEAM LAP (door-connected second room; mode (ii) design-arrival first; connection-contract (i) cells; recipe + room #3 exit) with a **two-cell lean** (drop W-PRO as likely redundant with W-MUR on a transform-shaped task). Matt: ① *"L5 as shaped — go."* ② *"Let's start with W-MUR + H + PRO. While the autonomous run is in motion I will retain the ability to rule one out if it seems they are redundant."* ③ *"Motion harness commission to drax now, in parallel — go."* ④ *"The pillar-quilt fix — go."* **Ruling ② is the second time the owner has restored a cell the conductor tried to cut on a forecast** — TCP-22 (*"Maybe you know how it ends but I want to see the requested bake off"*) is the standing ruling on what conductor forecasts are worth, and it now has a rhyme. **And ② creates a NEW Matt-interface pattern the program did not have: the OWNER RETAINS MID-RUN CELL-CULL AUTHORITY.** The roster is not a frozen pre-registration; it is Matt's dial while the run is in motion. Conductor obligation that makes the cull decidable: **at each cell close, surface the running comparison table to Matt before the next cell fires** — the cull decision is his, made on composited evidence, not on the conductor's redundancy forecast. This composes with desirable-run-pattern §6.2 (owner-eye checkpoints as pre-registered mid-run gates): the checkpoint is now also a **roster gate**. Also born from Matt's next-test question: **T5 CHARACTER/ANIMATION enters the §2 matrix** (*"animated characters/monsters holding weapons and swinging them"*) — a task class the matrix lacked, static-pose phase judgeable from stills now, motion phase gated on ruling ③'s harness | **Matt rulings, verbatim**, gandalf recording, veto-open |
| **TCP-38** | ★ **THE MOTION HARNESS LANDED AND IMMEDIATELY CHANGED WHAT TWO FUTURE LAPS CAN ATTEMPT.** Built at `~/Games/mcp-lab/harness/` (12 files, self-contained, borrows nothing — TCP-8 holds), ≈5 s per 90-frame 720p clip. Verified by the conductor: substrate sha + 0444 intact, `mcp-lab/project/` zero writes, demo strip read at the picture (L-A). ① ★★ **THE TEMPORAL-ACCUMULATOR LOCKOUT IS CAUSAL, AND IT BIFURCATES MOTION EVIDENCE.** With glow/SSAO/SSIL/SDFGI/volumetric-fog/auto-exposure disabled and TAA/SSAA/debanding off: **90/90 byte-identical** on re-render, on 30-vs-60 fps sample-rate (frame *k* vs frame *2k*), on settle-count, and on GPU particles — against a motion signal of **150,602–208,321 changed px per adjacent frame** (particles to 824,508), so the scale bar is four orders of magnitude wide. Same clip with accumulators **ON**: **0/90**, and the divergence is **max channel delta 1** — invisible to the eye, fatal to a differ testing `==`. **Standing: a motion lap whose clip needs glow — most VFX will — DECLARES ITS TOLERANCE BEFORE IT RENDERS, not after its differ convicts an honest cell.** This is TCP-27 ②'s law (an unsatisfiable zero-bar convicts honest work) arriving a full lap early, in a new medium, because the harness measured its own floor. `probe_accum_on.gd` ships so L7 re-runs the isolation rather than re-deriving it. **It also reconciles L4c:** L4c's CALIBRATION measured 2–7 px of *growing, spreading* drift across repeat captures **inside one process** and responded by refusing more than one scene per invocation; this rig renders **90 captures in one process** and reproduces all 90 across processes. Both true; the variable is the lockout. Honestly bounded by the executor: scene-swapping remains untested (needs the forbidden floor) and every run had a warm shader cache. ② **`--headless` EXITS 0 HAVING WRITTEN ZERO FRAMES** on this build — `frame_post_draw` never emits under the dummy renderer, `--quit-after` kills it, exit code says success. **L-K's third instance** (failure returns SUCCESS), and the sharpest yet: the executor probed the inherited claim (`l4_shoot.gd`'s "empty images") instead of trusting it and **found something worse than the claim.** The rig now **refuses at startup** — structural, not documented, matching L3's `editor_up.sh` and L4's one-scene-per-process. Standing: **an inherited claim about a tool's failure mode is a hypothesis, not a finding.** ③ ★★ **THE L6 ASSET-PIPELINE GAP, FOUND A LAP EARLY AND BY MEASUREMENT: all 2,178 `.glb` under `reincarnated-godot/Assets` carry ZERO animation channels; the 25,992 animated assets are `.fbx`, which has NO RUNTIME IMPORT PATH in Godot** (it needs the editor's FBX2glTF step), and the hero additionally needs a Sidekick→GeneralSkeleton bone-map living in the editor import cache. **This is the first task in the program where H may be STRUCTURALLY UNABLE and the wires structurally able** — an MCP wire runs *inside the editor*, which owns the FBX import path; a headless GDScript builder does not. Every prior lap scored the wire on convenience against a route H could always take. **Registered as L6's central prediction: T5 is the first plausible instrument-capability fork rather than a cost comparison** — and if it holds, "MCP authors, headless runs production" acquires a hard boundary at rigged content. ④ **The determinism instrument convicted its own rig on first use:** `manifest.json` carried observed engine deltas while its own header claimed no wall-clock — 90/90 frames identical, manifests differing. Quarantined to `timing.json`; manifests now byte-identical, so "manifests differ" is once again a clean signal that *the inputs* differed. **An evidence artifact that carries wall-clock is not evidence** | drax findings + build, gandalf ruling, veto-open |
| **TCP-39** | ★★ **THE QUILT IS CURED IN ALL FIVE KITS — AND MY DISPATCH WOULD HAVE DESTROYED ART IF EXECUTED LITERALLY.** Verified at the picture (`reincarnated-godot/harness_logs/quiltfix_2026-07-25/MONEY_before_after.png`, L-A): rainbow banding gone from dark-fortress (the crypt kit), dwarven-dungeon and ancient-egypt; the two legitimately-atlased kits sit in the same sheet as controls and are **visibly unchanged**. Commits `ce1c1af`/`188fd27`/`398609c`; mcp-lab zero writes, substrate sha + 0444 verified by the conductor. ① ★ **THE PARAPHRASE-STEER FAILURE REPEATED WITHIN A DAY OF THE RULING THAT NAMED IT, IN A NEW DOMAIN, WITH A WORSE BLAST RADIUS.** My §0 said *"modules whose pack material list declares no albedo."* **That is not what `Generic_Concrete (Uses custom shader)` means.** `render_catalogue`'s sentinel fires on the parenthesised descriptor only; resolution then falls through to the material **name**, which resolves to a real PNG — its neutral-grey route is reserved for meshes with **zero** slot lines. **A literal execution of my §1 would have painted three kits' pillars flat grey and discarded the concrete and stucco Synty authored** — curing a quilt by deleting the art. drax implemented the sentinel *as specified* **and** the resolution the sibling script actually performs, and said so. **Aggravating factor, mine: I labelled the paraphrase a quote** — *"as the executor derived it (drax-derived — quoted, not recalled)"* — which is worse than an unlabelled one, because it tells the executor not to check. **TCP-35 generalizes and is restated: a dispatch that restates a MECHANISM quotes the CODE, not the conductor's model of the code. Geometry was only the first instance.** ② **§0 named two call sites; there are four.** The atlas also reaches the column through `_build_occlude_mat(occlude_shader, tex_atlas)` as the shader's `stone_tex`, and `se_corner = [false,true,true,true]` — the unnamed path covers **3 of 4 corners**. Curing only the named sites would have **left 75% of the columns quilted while the money frame photographed as a cure.** Standing: **a fix dispatch names the SYMPTOM and the surface it must be absent from; call-site enumeration is the executor's job, and a conductor's enumeration is a CEILING, not a floor.** ③ ★★ **TWO INDEPENDENT CELLS, SAME DAY, FOUND THE SAME LAW FROM OPPOSITE ENDS: EQUALITY DIFFING REQUIRES A SCENE WITH NO CLOCK IN IT.** This cell's first diff pass was junk — **the occupant's aura moved ~6.8% of the frame between two runs of identical code** — cured by re-shooting room-only (the before side via a scoped stash, restored byte-identically by sha256). TCP-38 ① reached it through temporal accumulators (0/90 at max channel delta 1). Different mechanism, one lesson. **Standing: any before/after diff in this project renders the room WITHOUT animated occupants, or declares a tolerance and a mask up front.** And this cell shows the mask discipline done right: **20 pairs, 396,108 changed px, ZERO outside the rendered pillar/topper silhouette** (proven by a mask pass + containment test, not by eye), every kit's play-camera frame differing by **exactly 0 px**, and the shared resolver proven behaviour-identical over **13,229 meshes / 203,453 slot entries / 0 mismatches**. ④ **"LIBRARY-WIDE" WAS ANSWERED WITH A MEASUREMENT INSTEAD OF A CHANGE, AND I RATIFY THE REFUSAL.** Corpus scan — 43 lists / 26,394 mesh blocks / **231,990 slot lines** — found 974 pure-sentinel slots and 7 zero-slot meshes, **none in the builder's blast radius**, the 974 overwhelmingly *character* surfaces where the atlas is the correct read. Rerouting them would have **regressed hundreds of thumbnails to cure a defect they do not have.** The scope word was the owner's; the honest response to a scope word is a measurement of what it contains. ⑤ **HALT TO ME, RULED — DEFER TO THE FRAME, and the finding under it is bigger than the item.** ancient-egypt `SM_Bld_Pillar_Ornate_01` surface 1 names `Stone_Wall_Mural_02`; **the pack ships no such file**, and the three plausible neighbours are three different intents. Not guessed; left on the atlas, behaviour unchanged — correct. **Ruling: do not guess a texture identity from a filename in a kit no lap currently renders for judgment. When ancient-egypt is next staged, it is decided by eye at the play camera, where the answer is cheap and correct.** ★ **The real finding: a pack material list references a file the pack does not ship — the corpus has NAME DRIFT**, and drax's new parity instruments make a **full unresolvable-slot-name audit across all 231,990 lines** nearly free. **Queued, not fired** (L5 owns the floor). If one name is stale, others are, and each is a silent wrong texture waiting for the kit that uses it. ⑥ **Fifth consecutive cell to find a charter defect and report it rather than work around it** (L4a · L4b · L4c · harness · quilt). **That is now the program's most reliable safety property, and it is the thing that has caught every one of my errors** — which is an argument about how these dispatches should be written, not a compliment to pass around | drax build + findings, gandalf ruling **+ self-attribution**, veto-open |
| **TCP-40** | ★★ **L5-D PHASE A — THE PROGRAM'S FIRST MODE-(ii) DATUM, AND IT MOVED THE LAP UNDER ME.** 27.8 min of authoring (thinking included), **method H, no wire engaged** — a design arrival, stopped clean at the owner-eye with nothing built. Answer: portal in the **north wall, bay `0_3`** (the only bay centred on the room's own axis, x ∈ [−1.25, +1.25]); **no cut at all** — drop in `SM_Bld_Base_Wall_Door_Double_01`, a same-family module that already contains the hole; aperture **2.0042 w × 1.9663 h**, sill 8 mm *below* the floor surface so there is no step; chamber 5.00 × 3.75 on the crypt's own 1.25 grid. **P-L5-4 CONFIRMED and stronger than pinned: not merely zero mesh surgery — the kit ships the hole.** ① ★★ **P-L5-5 RESOLVED, AND THE PREDICTION WAS AIMED AT THE WRONG THING.** I predicted W-MUR would lack a removal-*targeting* escape hatch. **W-MUR can delete** (`node-delete` is in the installed 39-tool surface) — capability was never the issue. **The hazard is that name-based targeting is structurally WRONG here:** the bay is a **3-node group whose members do not share a fate** — `WallCap_0_3` carries the same bay index but sits *above* the portal prism at y ∈ [3.0097, 3.1697], and **every natural expression of the removal** (`Wall*_0_3*`, "delete bay 0_3", a wire `node-find` on the bay) **takes the cap and punches a 2.5 m notch through the unbroken wall-top plane — which is the design's single strongest "one place" cue.** The most natural expression of the removal destroys the thing the removal is for. Correct targeting is a **world-AABB volume query** against all 288 geometry nodes. ★ **CONDUCTOR RULING ON THE CONTRACT FREEZE, MADE BECAUSE OF THIS:** the (i) contract will specify the **portal VOLUME** and a **checkable INVARIANT — the wall-top cap ribbon remains unbroken (cap-node census exact)** — and will **NOT hand the two node names.** Handing them turns the lap's sharpest hazard into transcription (TCP-34's disease) and makes the census decorative; withholding them makes *"how did you target the removal?"* the cell's real output, which is what P-L5-5 was reaching for. A cell that takes the cap now fails a **pre-registered predicate**, not an eye. ② ★★ **THE SUBSTRATE CANNOT BE WALKED — 288 `MeshInstance3D`, ZERO `StaticBody3D`/`CollisionShape3D`, ANYWHERE** — and the removal **opens a 0.45 m hole in the walking surface**, because floor stops at |8.75| while the wall band runs to |9.2| and **no floor has ever existed under a wall.** Invisible in a still, fatal in a walk. **Sixth consecutive cell to find a charter defect of mine:** my G4 capsule-sweep gate assumed something to sweep against. **G4 stands, mechanism now specified** — sweep against generated collision (trimesh from visible geometry) or the kit's own proxies, and **measure against the PROXY, never the render: the kit's collision hole is 4.9 cm narrower than its visible one.** The census's orphaned-collision clause is **satisfied with its reason stated** (empty by construction), never silently passed — L-L. ★ **And the finding is bigger than the lap: this is the first time the program has tested PLAY rather than PICTURE, and the first thing it found is that every room we have built is a picture with no floor to stand on.** For the serial pipeline that is load-bearing — **the recipe must emit collision, or the rooms are set dressing.** ③ **THE DESIGN WAS SHAPED BY THE JUDGING INSTRUMENT, honestly and out loud.** North beat west on the binding constraint — **frame budget, 30 px clipped vs 91** — while west won both angle metrics (42.9° vs 47.0° off-normal; 38.9% vs 39.5% self-occlusion). The `__box` camera is therefore **a design constraint, not merely an evidence rig**, and drax filed the veto condition himself: *if Phase B's judgment framing is not `__box`, the whole comparison is downstream of that camera and needs redoing.* Recorded so it cannot be discovered later as a surprise. ④ **THE ROOM-COHERENCE AXIS AROSE FROM THE DESIGNER RATHER THAN THE RUBRIC.** Seven register cues, each stated as something checkable (one floor surface, no threshold, one wall-top plane, one 0.45 band, one material set, on-axis, same lamp colour/attenuation with its own pool) — and R-4's mechanism is the sharp one: **every chamber wall inherits an EXISTING substrate `ShaderMaterial` chosen by matching wall NORMAL, no new shader authored.** The substrate's materials encode **camera visibility** (which ruled out half the candidate walls before any render), so the chamber's camera-near +X wall inherits the east run's fade — *"not imitation, the substrate's own answer to the identical problem, applied to a wall with the identical normal."* **TCP-28 invented the coherence axis after Matt caught 36% pillars by eye; mode (ii) arrived at a stricter version unprompted.** ⑤ **`L4_KIT_CONSTANTS.md` IS ITSELF AN ANSWER KEY, and it is handed to EVERY cell by design.** The steer-check found the one I named (§2's *"the dais is not in your scene"* — changed nothing) and a sharper unnamed one: **the file is disciplined about withholding scene placements, then pins L4's two-brazier dressing decision in §6 — it steers by ADJACENCY, not content.** TCP-34 extends: scrub the constants file before the (i) cells, and audit *what a shared reference document teaches by proximity*, not only by statement. ⑥ **Door variants carry THREE surfaces, not the two `L4_KIT_CONSTANTS.md` §3 warns about** — the 2-override pattern leaves the architrave an **untextured blob at eye level**. Constants file corrected before it is handed out again. ⑦ **Concurrency held:** substrate sha + 0444 verified at cell start **and** end; project dir clean; `reincarnated-godot` judged by git attribution — the quilt dispatch's three commits attributed correctly, and the one uncommitted file (`project.godot`) verified **byte-identical to a baseline the executor banked at cell start** on his own initiative. **No spurious HALT. Three concurrent agents, three floors, zero collisions** | drax arrival + findings, gandalf rulings, veto-open |
| **TCP-41** | ★ **MATT RULED AT THE OWNER-EYE, AND SUPPLIED THE CONTENT THAT MAY DISSOLVE TCP-38 ③.** ① **R-1 CONFIRMED — north wall bay `0_3`, and the camera stays.** Verbatim: *"Chosen wall works for me. Regarding camera angle, let's continue to use this one for now. It could be that we adopt grim dawn's later but for now let's use this one unless there is a specific reason not to."* **`__box` is now the JUDGING FRAMING for Phase B and for every (i) cell** — which **closes drax's own R-1 veto condition** (TCP-40 ③) rather than leaving the comparison to dissolve downstream: the camera the design was optimized against is the camera it will be judged in. **A Grim-Dawn-register camera is a queued PROGRAM item, not this lap's business** — and it is queued precisely because switching it later invalidates the frame-budget comparison that chose north, so the switch must be made deliberately, with the rooms re-judged, never as a rendering convenience. ② **R-3 — *"an opening is fine."*** No leaf, no hinge, no door furniture. **Continuity over boundary** — the design's thesis is *one place*, and a door is the one prop that argues the opposite. ③ **R-7 — *"agreed."*** Method **H** for Phase B; drax's authoring clock continues from 27.8 min. The lap therefore produces **no mode-(ii) wire datum**, by the owner's choice at the only moment it could be chosen uncontaminated — exactly the fork drax surfaced. ④ ★★ **MATT SUPPLIED SIX SYNTY ANIMATION PACKS: 3,386 binary FBX, and the CONTENT is right on every axis that matters.** `matt_notes_handoff_docs/recent-synty-packs/synty-animations/` — bow-combat 1052 · base-locomotion 721 · idles 670 · goblin-locomotion 417 · emotes-taunts 283 · sword-combat 243. **Both rig generations ship** (`Animations/{Sidekick,Polygon}/{Masculine,Feminine,Neutral}/…`) **and our hero already runs the Sidekick rig** (`hero_walker.gd`'s Sidekick→GeneralSkeleton bone map), so the clips target the skeleton we have rather than one we would have to retarget from scratch. ~~**`goblin-locomotion` is a monster rig — L6's literal subject.**~~ **← FALSE, corrected by TCP-43 ⑤: it is goblin-*flavoured* locomotion on the same humanoid Sidekick rig (98.4% bind), tree `…/Neutral/`, characters `SidekickSyntyCharacter.fbx`. THIS CORPUS SHIPS NO MONSTER RIG. Also corrected there: two of the six packs were already vendored.** `sword-combat/Models/` carries `SM_Wep_Sword_01.fbx` + `ModularSyntyCharacter.fbx` + `KidRig_01`/`BigRig_01`. Four Unity `.controller` files are AnimatorControllers — **unusable by Godot, readable as Synty's intended state machine.** ⑤ ★★ **THE OPEN QUESTION WAS NEVER CONTENT — IT IS THE IMPORT PATH, AND TCP-30 FORBIDS ME ANSWERING IT BY REASONING.** TCP-38 ③ registered the L6 blocker as 2,178 `.glb` with zero animation channels and the animated corpus all `.fbx`; **this delivery does not touch that — every one of the 3,386 is FBX, zero `.glb`.** So the probe (`dispatches/2026-07-25-drax-l6prep-animation-probe.md`) asks three decidable things and **is instructed not to favour an answer**: does ufbx import a Synty animation FBX cleanly on 4.6.3 · **does `godot --headless --import` work without a human at the GUI** (if yes, the capability fork **softens from *H cannot* to *H pays a one-time import pass*,** and that changes what L6 measures) · **★★ does `GLTFDocument.append_from_scene()` + `write_to_filesystem()` emit a `.glb` that RETAINS the animation channels**, verified by playing it in a project that never imported it. **If the round-trip carries motion, the entire animated corpus becomes first-class for the headless route and for every wire that loads from a path.** Probe scope is a HANDFUL in a new `~/Games/mcp-lab/l6prep/` — not the corpus, not `reincarnated-godot`'s cache, not the L5-D cell's floor. **The answer ships as a ≥2 s clip of a Sidekick character swinging a sword with the weapon still in hand across the arc** (L-A; the harness exists because a still cannot show a weapon detaching mid-swing) — and two more facts L6 needs regardless of the outcome: **the bone-map/retarget gap, named but NOT fixed**, and **whether the locomotion clips translate the root or run in place** | Matt R-1/R-3/R-7 + supplied corpus; gandalf census (declared to the executor as hypothesis) + probe design |
| **TCP-42** | ★★ **L5-D IS BUILT — THE PROGRAM'S FIRST COMPLETE MODE-(ii) ROOM, 51.1 AUTHORING MINUTES END TO END** (Phase A 27.8 + Phase B 23.3, thinking included, **method H, no wire**). 330 nodes (296 − 2 + 36); an **opening** per R-3; **zero new materials, zero new shaders, and only TWO new meshes in the entire build** — the opening module and a half-width panel, the only two the substrate doesn't already carry inline. All eight gates met. **G4 walkable = TRUE.** Seven register cues each discharged as a *number*: cap tops over all 34 caps spread **< 1e−5**; floor-top delta crypt-vs-chamber **1 µm**; 1201 physics rays, **max step 0.000000 m**. ① ★ **THE FLOOR-HOLE RECIPE CLAUSE, which is the lap's deliverable to the serial pipeline:** *"a doorway's floor is owned by the room BEHIND it — size the new room's plate to the shared wall's NEAR face so it runs under the full band."* Plate `z [−12.50, −8.75]`, not `[−12.50, −9.20]`; 0.4500 m uncovered before → 0.0000 m after. **Every future door in every future room inherits this, and without it the rooms are pictures with no floor to stand on** (TCP-40 ②). ② ★★ **THE TRANSPOSE NEAR-MISS — see L-L ④.** A mirrored chamber was **two bases away from shipping**, and the note written to prevent exactly that was itself backwards. ③ ★★ **G4 MEASURED THE PROBE, NOT THE DOORWAY — see L-M**, a new standing law. ④ ★ **SEVENTH CONSECUTIVE CELL TO FIND A CHARTER DEFECT OF MINE, AND IT IS A NEW CLASS — TCP-35's FIX HAS A FAILURE MODE OF ITS OWN.** My §2.3 restated **drax's own Phase-A proxy measurement** (*"the kit's collision hole is 4.9 cm narrower than its visible one"*) **as a binding constraint.** TCP-35 says quote the executor's measured numbers — I did — **but quoting a number back at its author LAUNDERS A MEASUREMENT INTO A LAW: had his Phase-A figure been wrong, my dispatch would have instructed him to preserve the error, and the finding becomes unfalsifiable at the exact moment it becomes load-bearing.** It survived because he re-measured on his own initiative, **not because the dispatch permitted it.** **TCP-35 AMENDED, both halves now required: quote the executor's numbers AND mark restated prior-phase findings *"your own — re-verify,"* never as the conductor's to enforce.** ⑤ **GATE-ORDERING DISCIPLINE, also mine to fix:** I listed the gates in *build* order, so G4 — the gate most likely to fail and by far the costliest to re-shoot around — ran **after** the frames. **Order gates by (probability of failure × cost of downstream rework), most dangerous first.** ⑥ ★★ **THE FINDING THAT OUTLIVES THE LAP — THE CONFIRMED JUDGING CAMERA CANNOT SEE INTO WHAT IT JUDGES.** §4.5 corrected Phase A: the near walls are **not** faded, `occlude = 0.0` everywhere, so they render **fully solid** — and R-4's predicted mitigation therefore **does not occur**. Measured consequence: *"the wall is solid, and it does occlude the chamber's near side from `__box`."* **Every room the serial pipeline adds on the camera-near side will hide behind its own wall at the camera Matt just confirmed.** This is a property of the substrate × camera pair, discovered by building the first addition, and it is the first **concrete** instance of Matt's *"unless there is a specific reason not to"* (TCP-41 ①) — near-wall handling (fade/cull, the Grim-Dawn register's own answer) now has a measured reason attached rather than a speculative one. **Queued to Matt as a program item; not this lap's business.** ⑦ **CLOCK HONESTY AGAINST SELF-INTEREST:** drax first wrote 30.6 min for Phase B, noticed it ran past Phase A's boundary into report authoring, and **committed a correction to 23.3** — TCP-32 says authoring time is the number that matters, and he made his own number smaller by being exact about where it stops. ⑧ **Blast radius clean:** substrate sha + 0444 at start and end; `l4_shoot.gd`/`l4_diff.py` unmodified; project-dir inventory byte-identical to cell start; `l6prep/` never entered; `reincarnated-godot` moved only by the quilt dispatch's own commits. **No HALT** | drax build + findings + steer-check; gandalf rulings L-L ④, L-M, TCP-35 amendment, all veto-open |
| **TCP-43** | ★★★ **TCP-38 ③ IS DISSOLVED. ALL THREE PROBE QUESTIONS RESOLVED *YES*, EACH WITH ITS COMMAND LINE — THE WIRES DO NOT OWN RIGGED CONTENT.** ① ufbx imports Synty animation FBX cleanly on 4.6.3, **11/11**. ② ★★ **`godot --headless --import` WORKS WITH NO HUMAN AT THE GUI** — exit 0, **2.78 s**, 7 FBX, **from a directory with no `.godot/` at all.** ③ ★★ **THE `.glb` ROUND-TRIP CARRIES THE MOTION** — channels, clip lengths **and root translation**, verified in a project holding zero assets. **The program's central L6 prediction is answered against itself: T5 is NOT an instrument-capability fork. It softens exactly as chartered — from *H cannot reach rigged content* to *H pays a one-time import pass*** — and "MCP authors, headless runs production" acquires **no** hard boundary at rigged content. ② ★★ **THE PIPELINE SHAPE IS FORCED, AND IT IS FAVOURABLE.** A bare animation FBX **cannot** round-trip — glTF has no skeleton without a skinned mesh — so the artifact is necessarily **one `.glb` per character carrying its whole clip library**. **3,386 files collapse to a handful of artifacts**; `sidekick_library.glb` is **1.5 MB** for one character and five clips. The constraint we might have fought is the packaging we wanted. ③ **THE PICTURE (L-A):** 100 frames @ 40 fps = 2.5 s, 720p, the character reaching the harness **only as an emitted `.glb`** — which is the §1.3 answer arriving as a frame. **Weapon-in-hand measured ACROSS the arc: grip-to-socket drift 0.000000000 m over 101 samples** while the socket travels 1.783 m and the blade tip peaks at **46.7 m/s**. It cannot detach — **the mount is computed inside `set_time`, not delegated to a `BoneAttachment3D`**, which is the deterministic idiom for offline capture (gameplay may still delegate). **The harness needed ZERO modification** — `seek_all_players` was the whole bridge, and its determinism property **extends to rigged content: 100/100 byte-identical across processes.** ④ ★★★ **THE HARDEST VINDICATION OF L-A THIS PROGRAM HAS PRODUCED — EVERY NUMERIC CHECK PASSED A BROKEN RESULT.** Pack clips share **98.7% of bone NAMES** with the pack character and **88/88 skin binds resolve** — both green — **and the render showed a head at y = −0.69 with a perfectly intact skin.** Per-bone rest deltas are **~28° mean / 180° max**: **name-match is not rig-match**, the failure is invisible to every name-based check, and **it cost a render to see.** L-A is not a reporting convention; it is a correctness instrument. ⑤ **TWO OF MY §0 HYPOTHESES WERE FALSE, AND I HAD ALREADY REPEATED ONE OF THEM TO MATT IN PROSE.** *"`goblin-locomotion` is a monster rig — L6's literal subject"* — **FALSE.** Tree is `…/Neutral/`, characters are `SidekickSyntyCharacter.fbx`: goblin-*flavoured* locomotion on the **same humanoid Sidekick rig**, 98.4% bind. **This corpus ships NO monster rig** — a distinct goblin character rig exists elsewhere (`reincarnated-godot` carries `goblin_bone_map.tres`), not here. **L6's subject is therefore NOT supplied**, and L6 scoping must find its monster rig before it starts. Also false: **two of the six packs (`base-locomotion`, `goblin-locomotion`) were ALREADY VENDORED** in `reincarnated-godot/Assets`; the genuinely new material is **bow-combat, idles, emotes-taunts, sword-combat**. §0's `Models/` list was also incomplete. **Eighth consecutive cell to find a defect of mine — and the first that had already left the ledger and reached the owner as an assertion.** The §0-as-hypothesis instruction is what caught it; TCP-41 ④ is struck through in place rather than silently edited. ⑥ **THE RETARGET GAP, NAMED NOT FIXED (L6's scope, per charter).** A `sidekick_bone_map` → `SkeletonProfileHumanoid` retarget with `rest_fixer`/`fix_silhouette` is **mandatory on BOTH sides**: a raw pack clip binds **54%** to our hero raw and **6%** to our hero retargeted — **and `reincarnated-godot` ships the retargeted one.** Our hero is **50 bones** in renamed `GeneralSkeleton` space against the packs' 88/91/121. Open sub-item: the **121-bone** base-locomotion pack still inverts an 88-bone pack character *after* retarget, while the **91-bone** packs are clean. ⑦ **ROOT MOTION — SYNTY SHIPS EVERY CLIP TWICE.** Plain is in-place with **no `root` position track at all**; the `_RM_` twin carries a real one (walk **+1.500 m/cycle** = 1.452 m/s; sword combo **+0.500 m** as a lunge). L6 chooses per use rather than converting. ⑧ **FOUR INSTRUMENT BUGS, ALL THE EXECUTOR'S, ALL RECORDED — AND TWO OF THEM WERE THE BLOCKER-CONFIRMED ANSWER. See L-N**, a new standing law: *a NO must clear the instrument before it is recorded.* ⑨ ★ **A PRODUCTION DEFECT FOUND AS A SIDE EFFECT:** `reincarnated-godot/scripts/hero_walker.gd:44` declares `STRIDE_PER_CYCLE := 1.35`; the clip it drives measures **1.500 m/cycle** — an **~11% foot-skate error in the shipped hero walk.** Routed to drax's presentation seam as a fix item; not this program's business to fix, but this program found it. ⑩ **Hygiene:** `mcp-lab/project/` untouched (mtime-verified), `reincarnated-godot` read-only (four files copied *out*), `user://` clean, **11 FBX imported — not 3,386.** The probe project **stays** as the corpus's front door (`l6prep/README.md`, three commands). **Wall clock 37 min: execution ~7 min, authoring + analysis ~30 — TCP-32 holds again, execution was never the constraint** | drax probe + findings + self-filed instrument bugs; gandalf rulings L-N, TCP-41 ④ correction, all veto-open |
| **TCP-44** | ★★ **THE CONNECTION CONTRACT IS FROZEN — 65 PREDICATES, AND IT CAUGHT A DEFECT IN THE BRIEF THAT COMMISSIONED IT.** `~/Games/mcp-lab/evidence/l5/CONNECTION_CONTRACT.md`, 1131 lines: T×3 transform · P×6 portal · V×8 invariants · C×10 chamber · M×6 materials/light · R×7 register cues · G×6 walkability · N×8 census · D×7 differ · F×4 frames. Every number traced to drax's own measurements with a citation tag; **eight items honestly declared UNSOURCEABLE** in a dedicated section rather than invented (Zone P's ±4.00 m x-extent is a *bound*, not a measurement — he sampled spill only on the room axis; D-4's 90% floor rests on a "generous chamber box" he never defined, so his 96.8% cannot be recomputed; the 24 px dilation is inherited and unvalidated for this geometry). ① ★★ **NINTH CONSECUTIVE CELL TO FIND A DEFECT OF MINE — AND IT IS THE MOST DANGEROUS CLASS YET BECAUSE IT WOULD HAVE CONVICTED AN INNOCENT TOOL. See L-O.** My brief supplied *"cap-node census exact at 34 caps"* as the invariant; 34 is a fingerprint of drax's cap construction, not a property of the design. A legal three-box capping scores 31 and fails; a shattered ribbon of 34 fragments passes. Now gated on **AABB identity + XZ ribbon continuity**, with 34 demoted to *reported*. ② ★★ **THE ANSWER KEY LEAKS THROUGH ARITHMETIC AND THROUGH GREP, NOT ONLY THROUGH PROSE — two withholdings the author added BEYOND my brief.** (a) **No removal count and no absolute census counts**, because "296 before, 330 after, 36 added" hands the removal set by subtraction. (b) ★ **`ShaderMaterial_aobh0` is DESCRIBED, never NAMED** — it is carried by exactly the two removed skins, so printing it in the material table would have handed the removal set **in one grep**. TCP-34 said the ledger is an answer key; this extends it: **a contract leaks its answer through any column a cell can join on.** ③ ★ **SIX ★ MECHANISMS REPLACE WHAT WOULD HAVE BEEN WARNINGS (L-L honored structurally, not cited).** The standout is the **Key-light transpose gate**: the substrate's only non-symmetric basis whose correct reading is **decidable by physics** — read it right and it reproduces `l4_diff.py`'s published shadow vector to **7 dp** — so a transposed reader **HALTs before placing a single node.** L-L ④'s near-miss (six of eight bases passed a transposed reading) is converted from a cautionary note into a gate that cannot be passed by luck. Also: the **band-coverage assert** (0.4500 → 0.0000, both readings recorded), the **cap-notch control** (the differ's non-zero calibration point *is* the hazard), a **projection re-implementation gate** (a cell's own hull must reproduce `l4_diff.py`'s six vertices to 0.1 px), and the **decoupled-probe gate** (L-M, made mandatory). ④ **V-2 IS A CATCH I WOULD NOT HAVE MADE:** an assertion that the portal prism is empty **forbids the floor-hole fix.** drax wrote that assertion, it fired on him, and the contract now **splits the prism at the walking surface** — nothing but the opening above, floor *required* below. A gate that forbids the correct answer is worse than no gate. ⑤ ★ **THE CONTRACT AUTHOR NAMED A STRUCTURAL FLAW IN STAGE 2 ITSELF:** *"being handed the removal set in order to be told not to pass it on is TCP-34's structure one layer up."* True, and it did not change the withholding — **but it is the only reason the `aobh0` grep leak was spotted**, since you cannot detect a leak of an answer you have not seen. **Recorded as a process finding: a cleaner Stage 2 has the contract author derive the removal independently FIRST, then freeze.** ⑥ **§5 SCRUB EXECUTED (TCP-40 ⑤):** `L4_KIT_CONSTANTS.md` §6 — L4's dais-dressing decision — relocated to `evidence/l4/L4_DRESSING_DECISION.md`, which is L4's alone; the shared file now carries kit natives only, plus the one genuinely kit-wide constant rescued from that section (**discriminate texture presence on the MEAN, never on VARIANCE** — variance reports an untextured white mesh as textured, and Synty atlas-mapping reads flat by design). §3's surface-count claim corrected: **door/opening variants carry THREE**, and the list is now explicitly *"not a ceiling — count the surfaces on the mesh you are about to assign"* | gandalf sub-agent (`SPEC-AUTHOR`) draft + self-filed steer-check; conducting gandalf review, scrub, rulings L-O, all veto-open |

---

**Signed:** gandalf, 2026-07-24 (`RUN-CONDUCTOR`, gated by `ARCHITECT`). Every fork Matt was asked to
rule is ruled. What remains gated is credential-level and taste-level, and both are named above.
