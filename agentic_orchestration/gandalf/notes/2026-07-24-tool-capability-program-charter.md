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

## §6 — Lap sequence

| Lap | Class × mode | Instrument(s) | Gate | Ready? |
|---|---|---|---|---|
| ~~L1~~ | T1 × (i) | W-INC / T / H | — | **CLOSED** — H won; W-INC has no create primitive; T failed silently |
| ~~**L2**~~ | T1 × (i) — CALIBRATION | W-PRO | none | **CLOSED 2026-07-24 — Pro is an EXECUTOR.** See below |
| **L3** | standup | **W-MUR** | ~~Matt~~ **CLEARED** — Q45 ruled self-hosted, mechanism `stdio` (TCP-11); Custom mode needs no credential | **CHARTERED + DISPATCHED 2026-07-24** — charter `…-tcp-l3-murzak-standup-charter.md`; runs in `~/Games/mcp-lab/`, not in the product repo (TCP-17/18) |
| **L4** | **T2 × (i)** | W-PRO · W-MUR · H control | L3 for the three-way | next |
| **L5a/b** | **T4-UI × (i)** then **× (ii)** | W-PRO · W-MUR · H control | L3 | **no new harness needed** |
| **L6a/b** | **T3 × (i)** then **× (ii)** | field | **the STORY session** (Q44 deferred there 2026-07-24) | **blocked on story, not on tooling** |
| **L7a/b** | **T4-VFX × (i)** then **× (ii)** | field + `Godot-AI-Particles` + Pro's `create_particles` | motion harness — **and L2 found Pro ships `record_frames`/`replay_recording`/`compare_screenshots`**, so TCP-8 needs re-examining: if we borrow it we score capture rigs, but it may be worth one lap to learn what the shape should be | blocked |

**Re-sequencing note (2026-07-24).** Matt deferred Q44 to the story session — *"we need to flesh the
story out further before we decide."* Correct: act-register is a consequence of what the acts ARE,
and settling it from tooling evidence would be the tail wagging the dog. **Only L6 waits.** An
expansion lap inherits the register of the scene it expands; a HUD has no act-register; VFX gates on
a harness. **L3 → L4 → L5 is a clear runway.** Meanwhile the story session now gates Q43's seven
persistence rulings, Q44, and L6 — making it the highest-value unfired item on the board.

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

### L4 — T2 EXPANSION: the first lap the wire can genuinely win

Existing scene, bounded modification, **no measurement needed** (constants already derived), **few
calls**. Every structural disadvantage the wire carried in L1 is absent. If MCP loses here it loses
everywhere; if it wins here that is the shape of its real job.

**Named GridMap prediction (W-MUR):** authoring through `gridmap-set-cell` **cannot produce L1's M2
failure class by construction** — orientation is an enum index on an integer grid, not a
`Transform3D` basis, so the transpose trap is unrepresentable. If true, GridMap is not a convenience;
it is a *correctness* property, and it is the first thing in the program that beats H on something
other than speed.

### L5 — T4-UI first, before VFX

Needs **no new harness** (a HUD is judgeable from a still) and is the **strongest untested case for
the wire**: at N≈12 controls with ~40 iterations, latency reverses — ~150 ms per wire nudge against
15–30 s per script edit→relaunch→screenshot cycle. Pro brings `set_anchor_preset` + the full theme
suite; Murzak brings node CRUD + `screenshot-viewport`.

### Blockers to clear

1. **Motion harness** (drax, small) — frame sequence → mp4/gif strip. **VFX cannot be judged from
   stills**; our stack produces only stills. L-A is unsatisfiable for L7 without it. Pro has
   `capture_frames`; Murzak has none — so the harness must be **ours**, or the instruments are being
   scored on their capture rigs rather than their authoring.
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
| **TCP-16** | **H2 disposition (not a Matt call).** R2's flat cream floor is **accepted as a lap artifact** — an experimental room that will never ship. Program consequence: dressing selection must verify **measured texture presence**, not merely a valid material slot (L-K instance #3, and L2 found it one level deeper: the FBX carry **2 surfaces** while `set_material_3d` is single-surface, and **no tool reports a surface count**) | gandalf, veto-open |

---

**Signed:** gandalf, 2026-07-24 (`RUN-CONDUCTOR`, gated by `ARCHITECT`). Every fork Matt was asked to
rule is ruled. What remains gated is credential-level and taste-level, and both are named above.
