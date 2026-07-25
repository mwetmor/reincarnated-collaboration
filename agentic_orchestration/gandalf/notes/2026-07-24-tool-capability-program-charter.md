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
- **L-B — Manifest before behaviour.** Capability is read from the manifest or the source; reliability
  is read from behaviour; **neither is inferred from the other.** Proven twice in one session, both
  times against my own committed claims. *(Second discipline candidate — file to jack-ryan.)*
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
| **L2** | **T1 × (i) — CALIBRATION** | **W-PRO** | none | **LAUNCHABLE NOW** |
| **L3** | standup | **W-MUR** | **Matt** (cloud-vs-self-host **+** `godot-cli login`) | blocked |
| **L4** | **T2 × (i)** | W-PRO · W-MUR · H control | L3 for the three-way | partially ready |
| **L5a/b** | **T4-UI × (i)** then **× (ii)** | W-PRO · W-MUR · H control | L3 | **no new harness needed** |
| **L6a/b** | **T3 × (i)** then **× (ii)** | field | **H1 register ruling** | blocked |
| **L7a/b** | **T4-VFX × (i)** then **× (ii)** | field + `Godot-AI-Particles` | **motion harness** | blocked |

### L2 — PRO CALIBRATION (immediately launchable)

**Not a competition — calibration.** Same logic that made drax calibrate `kit_measure.gd` against the
reference pack before trusting it: **if Pro cannot reproduce a known room, it cannot author a new
one**, and nothing it does in L4–L7 can be trusted. It also exercises the swap procedure, the
control-diff and the frame capture *once, on the cheap instrument*, before we spend the expensive one.

One room. One new pack. Pro authors; the existing H build of the same room is the control; diff the
frames. Pre-registered:

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
2. **H1 register ruling** (Matt) — L6 cannot be judged without knowing what register a new room is
   supposed to arrive at. L1's contact sheet showed all three new rooms reading pale tan against a
   dark reference; that is the open question, and T3 inherits it.
3. **Murzak standup** — §7.
4. **Gutted-addon hazard** (drax, flag) — `npx …--install-addon` reads `plugin.cfg`, sees the right
   version, prints *"Addon is already up to date"* and exits **without an integrity check**. The
   installed W-INC addon was 3 `.gd` files against an expected 36. **A gutted addon never
   self-heals.** Any lap touching W-INC must file-count first.

## §7 — Matt interface

**Reserved to Matt (commitment-boundaries):**
- **Cloud vs self-hosted for W-MUR.** Default connects to the ai-game.dev hosted cloud — our scene
  geometry, script contents and screenshots transit a third party. Self-hosting is supported (Docker
  image published). ADR-006 does not cover this shape. → `matt_decision_needed`.
- **`godot-cli login`** — OAuth 2.1 device login, browser, machine-wide credential. → `matt_to_do`.
- **H1 register**, and the H2–H5 rulings still owed from L1.
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
| standup (L3) | ✓ | ✓ readiness predicate | — | Matt-gated credential | **Matt action, then a drax lap** |

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

---

**Signed:** gandalf, 2026-07-24 (`RUN-CONDUCTOR`, gated by `ARCHITECT`). Every fork Matt was asked to
rule is ruled. What remains gated is credential-level and taste-level, and both are named above.
