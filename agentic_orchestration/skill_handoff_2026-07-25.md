# Session hand-off — 2026-07-25 — GD instrumentation, and the three-goal reframe

**Conductor:** gandalf (`SPEC-AUTHOR` → `DRIFT-CRITIC`)
**Co-investigator:** Matt, at the PC, live in Grim Dawn
**Sub-agents:** legolas ×4 (binary inspection, Mode A)
**Commits:** `ae070dfa` · `5d3cd00d` · `73c8f4fb` · `ce2755ee` · `5bbedeef` · `d4de9285` · `63d64d45` · `65ce56bf` · `6ea9318f` — none pushed

---

## 0. Read this part if you read nothing else

Two things happened. One is a pile of findings. The other is a **correction to what the
program is for**, issued by Matt, and it reorganizes the pile.

**Matt's framing — the three goals:**

> 1. Ensure all of GD's combat mechanisms exist in our battle sim.
> 2. Develop a conversion key for their player and monster characters to exist in our battle sim.
> 3. Measure the comparative correctness of the key and tune it towards acceptable accuracy.

gandalf had been running as though goal 1 were the whole program, because goal 1 produced the
session's most vivid finding (the telegraph, § 4.2) and vividness was allowed to stand in for
importance. **That is the same partial-view-stated-as-the-whole error that bit this program
four times this week — this time at the level of program intent rather than data.** Matt caught
it; gandalf did not. Recorded plainly because the drift-catch is precisely the seam's job.

**And the reframe surfaces a dependency nobody had stated:**

> **You cannot measure translation fidelity through a mechanism gap.**

Goal 3 compares a fight in GD against the same fight in our sim. But a fight in GD runs GD's
AI. If our sim lacks telegraph, repositioning, wait-to-attack, flee-triggers and pack
leadership — and § 4.1 establishes that it lacks all of them — then the two fights diverge for
**AI reasons**, not **key reasons**, and the divergence is *unattributable*. The measurement
returns a number that means nothing.

**Goal 1 therefore gates goal 3 — unless the test is constrained until the gap stops biting.**
That constraint ladder is § 2, and it is the single most useful thing this session produced.

---

## 1. Goal status at hand-off

| Goal | Substrate | Status | Blocked on |
|---|---|---|---|
| **1 — mechanism completeness** | **COMPLETE.** The 40-entry `ControllerMonster` state table is the *exhaustive* vocabulary of what a GD monster can do. Nothing further to discover. | Discovery **done**; comparison against our sim **not written** | gamora: a state-by-state audit. No Matt action. |
| **2 — conversion key** | The `.arz` via the TRUE-SOURCES pipe; **proven at width one** (FoI, 22/22 byte-match, GD-SLICE run) | Width-one proven; **unit reconciliation unresolved** | One calibration experiment (§ 5, item 2) |
| **3 — comparative correctness** | Not started. The differential rig now exists *in principle* (§ 2.3) | Rig unverified; tolerance undefined | **Q47** ruling + `game.Spawn` test (§ 5, item 1) |

**The single line that most changes the picture:** TSF6-TRACK-A scored our sim **+0.15%
parameter-faithful** on pursuit distance. That score was measuring the parameters we model.
The 40-state table reveals we model **roughly a quarter of GD's monster behaviour vocabulary**.
A near-perfect score on a quarter of the surface is not a near-perfect sim; it is a
well-calibrated quarter.

---

## 2. THE STRUCTURAL FINDING — the constraint ladder

### 2.1 The problem

Goal 3 asks: *is the conversion key numerically correct?* The natural test is a differential —
same character, same monster, same conditions, both engines, compare.

The confound is that "same conditions" is impossible while the engines' AI differs. Every
missing mechanism injects divergence that is indistinguishable from key error.

### 2.2 The way out — constrain until the gap doesn't bite, then widen

Do not close goal 1 first (it just got much bigger — § 4.1). Instead, **start goal 3 at the
most constrained fight that still exercises the key**, and let the test widen as goal 1 closes.

The elegant part: **the constraint set IS the gap register.** Each mechanism implemented
retires one constraint and unlocks one rung. **The test's reachable scope becomes the running
measure of goal 1's progress** — one ledger instead of two.

### 2.3 The ladder

| Rung | Fight setup | What it tests | Gated on (goal-1 mechanism) |
|---|---|---|---|
| **L0** | **one melee monster, pre-aggroed, fight to death, no pack, no flee** | HP · armour · damage · attack speed · skill numbers — **the conversion key, nearly isolated** | **nothing — runnable now** |
| **L1** | + a ranged monster | projectile speed, range bands, kiting geometry | ranged-attack modelling |
| **L2** | + engagement from idle (not pre-aggroed) | aggro onset radius, telegraph duration | KPI 1 · KPI 2 / telegraph |
| **L3** | + a pack of three | distress propagation, pack leadership, attack-token spacing | KPI 5 · pack hierarchy · `WaitToAttack` |
| **L4** | + a flee-capable monster | disengage, leash, return | KPI 3 · fear states |
| **L5** | full room, played normally | everything, and *play feel* | all of the above |

**L0 is runnable now and is the correct next move on goal 3.** It is cheap, it isolates the
key from the mechanism gap almost completely, and it produces the first real fidelity number
this program has ever had.

**L0's readout is coarse and robust** — time-to-kill, damage dealt, damage taken, HP curve.
No sub-second AI-state timing. **This is a materially easier instrument than the one gandalf
had been speccing**, which was aimed at *parameter* measurement (what is GD's aggro radius)
rather than *outcome* measurement (do the two engines resolve the same fight).

**And the console work serves L0 better than it served its original target.**
`game.killMonsters` + `game.Spawn <the exact DBR we imported>` + a known character **is** a
reproducible fight setup. It fell out of work aimed elsewhere.

---

## 3. Where the original commission stands

The commission (`research/commissions/2026-07-24-gandalf-gd-playtest-capture-instrument-scoping.md`)
asked legolas to scope an **AI-agent bake-off** — vision models watching Matt play.

**That premise has largely dissolved, and should be recorded as dissolved rather than quietly
abandoned.** Three reasons, in order of weight:

1. **The overlays render answers as text and lines.** `character.ShowAngerLevels` draws a
   relationship edge; `character.LogData` prints state names. The instrument needs line
   detection, OCR and frame timestamps — **deterministic CV at ~$0/hr**, against the
   $0.23–31/hr vision-model range originally scoped. No semantic judgment required.
2. **The console converts observation into experiment.** Matt is not "playing while something
   watches." He runs trials.
3. **The session's highest-value findings came from Matt reporting in prose** — the empty mod,
   the two-label overlay, the infighting anger line, the zombie's alert beat. Not one is a
   *quantity*; every one is a *recognition*, and no instrument at any price would have produced
   them.

**But point 3 does NOT generalize to "we don't need measurement"** — that was gandalf's
erroneous pushback, and Matt's three-goal framing destroyed it. Recognition suffices for goal 1.
**Goal 3 is fidelity-to-a-reference, and fidelity is exactly what cannot be eyeballed.** If our
sim kills a Chthonian in 4.2 s and GD takes 7.1 s, no amount of feel-tuning ever finds it.

**Disposition:** commission not withdrawn — its Q1 (non-vision channels) remains live and
under-answered. **Grim Internals specifically was never resolved** and is the most likely
source of goal-3's damage/DPS readout (§ 5, item 6).

---

## 4. Findings

### 4.1 The complete monster AI vocabulary — 40 states

`Game.dll` 5418372–5418812. Count verified at exactly 40. Full record:
`research/knowledge/gd/2026-07-25-gd-ai-state-tables-complete.md`.

```
 1 Idle                11 Dying             21 Confused     31 QuestWalk
 2 Startup             12 Return            22 Paralyze     32 QuestMove
 3 Attack              13 FollowLeader      23 Trapped      33 QuestUseSkill
 4 Pursue              14 Dead              24 Immobile     34 QuestPlayAnimation
 5 RepositionForAttack 15 NavigateObstacle  25 KnockedDown  35 TakeHit
 6 JumpAttack          16 DefendLeader      26 Stunned      36 GettingUp
 7 Roam                17 Charge            27 Scared       37 UseSkillOnPoint
 8 Flee                18 Move              28 Sleeping     38 UseSkillOnAlly
 9 WanderPause         19 Panic             29 WaitToAttack 39 Emote
10 Wander              20 DodgeAttack       30 Patrol       40 AlertBeforePursue
```

**Provisional triage — NOT YET VERIFIED against our sim. This audit is owed to gamora and no
number in it should be quoted until she has run it.**

- **Plausibly modelled / status-equivalent (~12):** `Idle` `Startup` `Attack` `Dying` `Dead`
  `Move` `Stunned` `Immobile` `KnockedDown` `Paralyze` `Trapped` `TakeHit`
- **Non-combat / quest / cosmetic (~7):** `QuestWalk` `QuestMove` `QuestUseSkill`
  `QuestPlayAnimation` `Emote` `Sleeping` `Patrol`
- **Combat behaviour we appear NOT to model (~18):** `Pursue`(partial) `RepositionForAttack`
  `JumpAttack` `Roam` `Flee`(partial) `WanderPause` `Wander` `Return` `FollowLeader`
  `NavigateObstacle` `DefendLeader` `Charge` `Panic` `DodgeAttack` `Confused` `Scared`
  `WaitToAttack` `GettingUp` `UseSkillOnPoint` `UseSkillOnAlly` `AlertBeforePursue`

Clustering into **seven mechanism families**, of which the original TSF6 register named five:

| # | Family | States | In TSF6 register? |
|---|---|---|---|
| 1 | aggro onset | `Pursue`, `AlertBeforePursue` | KPI 1 ✓ |
| 2 | **telegraph / pre-commitment beat** | `AlertBeforePursue` | **NEW — reframes KPI 2** |
| 3 | leash + return | `Return` | KPI 3 ✓ |
| 4 | idle loop | `Roam`, `Wander`, `WanderPause` | KPI 4 ✓ *(but three states where we assumed one)* |
| 5 | distress + pack | `FollowLeader`, `DefendLeader` | KPI 5 partial — **pack hierarchy is NEW** |
| 6 | **combat spacing** | `RepositionForAttack`, `WaitToAttack`, `DodgeAttack`, `JumpAttack`, `Charge` | **NEW** |
| 7 | **fear granularity** | `Flee`, `Panic`, `Scared` | partial — three states vs our one `fleeDistance` |

Plus two loose items: `NavigateObstacle` (pathing recovery as a first-class state) and
`UseSkillOnPoint` / `UseSkillOnAlly` (**ground-targeted and ally-targeted monster skills** —
monster *support* behaviour, which we almost certainly have no concept of).

### 4.2 ★ THE TELEGRAPH — the session's best design finding, and it came from an aside

**Matt:** *"I have seen monsters slow down their state transition to allow for graphics such as
a zombie yelling and waving his hands angrily during a long beat of what seems like alert."*

He offered this as an explanation for why he hadn't seen a state word. It is the most
consequential thing in the session.

He described **an animated, observable pre-commitment beat** — which is what
`AlertBeforePursue` looks like from outside the code. Three independent lines converge without
being derived from each other: behaviour observed live; the state confirmed in the binary with
a full RTTI class; an `Alert` entry present in the *animation* table.

**The reframe:** `SightAngerRate` 3.0 and `InnerSightAngerRate` 12.0 had been treated as AI
tuning constants. If that window is occupied by an animated beat, those numbers are **the
duration of a player-facing telegraph**, and the 4× inner/outer ratio is an authored
**fairness curve**:

| Situation | Telegraph | What the player experiences |
|---|---|---|
| spotted at range (outer) | **long** | *"it's seen me — I have time to decide"* |
| walked into its face (inner) | **short** | *"that's on me, I was careless"* |

**The monster performs noticing you, and the length of the performance is inversely
proportional to how much the situation is your own fault.**

That is why GD encounters read as reactive and fair rather than arbitrary, and it is authored,
not emergent. Genre lineage: D2's Fallen shaman wind-up; D3's formalisation of telegraphing
into wind-up frames and ground decals as a readability discipline; D4's elevation of telegraph
legibility to a stated pillar. GD's version lives in the state machine rather than a VFX layer,
which is why a parameter audit never saw it.

**Our sim has no telegraph concept. Not a missing parameter — a missing category.**

**NOT BANKED (D-b):** the join between the observed beat and the named state is *not
established*. Confirming it costs one glance at the top-left word during the beat.

### 4.3 The two-label overlay — CONFIRMED by surviving a falsification test

`character.LogData` draws **two** green words per monster:

| Position | Table | Layer | Entries |
|---|---|---|---|
| **top-left** | Table 3 — ControllerMonster AI State | the **decision** | 40 |
| **bottom-right** | Table 1 — AI Action State (`"Action State: "` prefix) | the **body** | 19 |

The tables are **disjoint state machines**, not one falling back to the other — Table 3 carries
its own `Idle`, `Attack`, `Dying`, `Move`. Seeing `Idle` in both positions means both FSMs are
in `Idle` simultaneously.

**Method note worth keeping.** The model was not confirmed by accumulating agreeable
observations. Matt's initial notes listed `Walk` in *both* positions and Table 3 has no `Walk` —
so the model had a **named falsifier**, and it was checked rather than explained away as
misrecollection. It held (`Walk` renders bottom-right only). The confirmation is worth more
than the original agreement was. **Do not resolve observer-vs-model conflicts by assuming the
observer misremembered; that is the cheap resolution and it is the one that silently corrupts
protocols.**

**Pipeline consequence (galadriel):** all KPIs read off the **top-left label alone**. One OCR
region per monster, not two — a simplification arriving before a line of pipeline code existed.

### 4.4 The anger overlay is a relational primitive

`character.ShowAngerLevels true` draws a **solid red line from a monster to its anger target**,
appearing at the instant of commitment. It correctly points at **other monsters** during
infighting.

**This is a directed graph edge, not a scalar** — richer than the "number / bar / on-off"
option space gandalf had framed. KPIs 1, 3 and 5 all fall out of edge appearance/disappearance
geometry and timing.

**Closed:** the line is **always solid.** Apparent dashes were terrain occluding a
depth-tested 3D line — Matt's correction, and gandalf should not have raised dash-as-state-encoding
as a candidate on three stills.

### 4.5 Anger resets instantly → the trial loop is repeatable

**Matt:** *"Anger resets instantly. Red lines disappear and attacking monsters walk away."*

Monsters *disengage*; they don't merely lose the line. So one pack supports an unbounded loop:

```
invisible → reposition → visible → MEASURE → invisible → reset → repeat
```

**N trials standing still.** Decisive for KPI 5, where `ChanceToRespondToDistressCall` is **75**
— a rate needing dozens of trials. Hunting a fresh pack per trial was never realistic. KPI 5
was quietly the least tractable of the five; it is now arguably the most.

**Residual check (one observation, folded into any trial):** on going visible, is re-aggro
*instant* (accumulator paused) or *normal-delay* (accumulator zeroed)? Matt's description
strongly implies zeroed. The distinction is what makes the loop valid, so it gets confirmed.

### 4.6 ✗ No coordinate readout exists — and the recovery is better than what was lost

Matt tested the console hover-inspector correctly (console open, cursor over objects) and
**nothing printed.** Corroborated statically: the 51-command table contains **no
object-inspection command** in any namespace. The `Origin = %f %f %f` block at exe 2687760 is
unreachable from the shipped console. **Accepted as a real finding.**

**Recovery — `character.WarpCursor`** (exe 2684992): *"Makes it so player always warps to
destination."* Click-to-move becomes click-to-teleport.

**This makes the coordinate problem irrelevant rather than survivable, and the reason is worth
stating precisely because the first framing was wrong.** We wanted coordinates to know
separation *numerically*. But the binding constraint was never the numbers — it is that **the
approach contaminates the trial**: walking toward a monster accumulates anger the whole way, so
the measurement starts dirty. Warping arrives with the clock at zero.

### 4.7 The container — Matt's empty mod

**An EMPTY folder inside `mods/`, opened as a Custom Game.** Console works. Syntax is `true`,
**not `1`** (both gandalf and legolas asserted `1`, neither had verified it).

**Why it is the *ideal* container, not merely an acceptable one:** an empty mod has no
`database.arz`, so there is nothing to override vanilla with. **Contamination is impossible by
construction, not mitigated.** That is categorically stronger than verification-by-diff, and it
obtains for free the property gandalf's vanilla-passthrough proposal would have bought with
280 MB of file copies.

**Ruled out and worth not re-litigating:** all third-party overhaul mods (each ships its own
`database.arz` — the very file carrying the calibration parameters; contamination is silent and
still produces plausible numbers), **and the Crucible** (not in the Custom Game list, *and*
`ViewDistance` 80 vs vanilla 15–16, `MaxPursuitDistance` 125 vs 60–75, `distressCallRange` 50
vs 15–20 across 984/1083 creature records; 175 controller records overridden).

---

## 5. MATT'S REMAINING PC TO-DO — re-prioritized under the three-goal frame

**The order changed.** Previously it was ranked by AI-state curiosity. It is now ranked by
which goal each item unblocks. **Items 1–3 are worth more than everything below them.**

**PC-side sheet (OPERATIVE copy — in-repo):**
`agentic_orchestration/gandalf/pc-handoff/2026-07-25-gd-teleport-probe-directions.md`
**Screenshot drop:** share → `visual-artifacts/2026-07-25-gd-teleport-probe/`

> ⚠ **The share mirror is STALE.** `/Volumes/reincarnated` was unmounted from the Mac side when
> this re-prioritization was written, so `agent-prompts/…-teleport-probe-directions.md` still
> carries the *old* order (teleport-first). **Re-mirror it before Matt next sits at the PC** —
> one `cp` once the share is mounted. Nothing is lost; the repo copy is version-controlled,
> which is precisely why it was made the operative one after the share vanished mid-session.

| # | Action | Serves | Why it's ranked here |
|---|---|---|---|
| **1** | **`game.Spawn <dbr path>` — DOES IT WORK?** Try `game.killMonsters`, then `game.Spawn` with a creature record path. **This has never been asked and it is now the single highest-value untested command.** | **Goal 3** | **The entire L0 rig depends on it.** If Spawn accepts a DBR path we hold in the `.arz`, the parameter↔creature join becomes an *identity* rather than an inference, and a reproducible fight setup exists. If it doesn't, goal 3 falls back to world monsters and gets much harder to control. |
| **2** | **`character.WarpCursor true`** — click the ground. Works? Instant or animated? Max range? Respects pathing? **Does warping past a monster aggro it?** | **Goals 2 + 3** | Positioning without contamination. Enables the unit-calibration experiment (goal 2) and clean L0 setup (goal 3). |
| **3** | **`game.PlayStats`** — run it, screenshot whatever appears. Does it show **damage dealt / DPS / HP**? | **Goal 3** | This is L0's *readout*. If PlayStats carries combat numbers, goal 3's instrument is already installed. If it's cosmetic stats only, see item 6. |
| **4** | **The telegraph word.** Next zombie doing the yelling-and-waving beat: **read the top-left word during it.** And does the beat run longer when spotted from far vs up close? *(prediction: ~4× longer at range)* | **Goal 1** | Confirms the D-b join. Cheap, and it is the last live question on the biggest design finding. |
| **5** | **`FollowLeader` / `DefendLeader` on a normal world pack** — do they ever appear top-left? Then compare against a pack you spawned. | **Goals 1 + 3** | Two jobs. Confirms pack hierarchy (goal 1) **and** tests whether console-spawned monsters are *impoverished* — if world packs show these and spawned ones never do, L0 must use world monsters. |
| **6** | **Grim Internals** — install decision. Combat text, monster HP, DPS readouts. | **Goal 3** | The commission's Q1 was never resolved. **Only pursue if item 3 comes back cosmetic.** Caveat: it is a third-party DLL — establish it does not alter game behaviour before any measurement is banked. |
| ~~7~~ | ~~`game.Teleport` / `character.MoveTo` / `MoveToEntity`~~ | — | **DEPRIORITIZED.** With no coordinate readout and `WarpCursor` available, these are curiosities. Run only if item 2 fails. |
| **8** | **Re-aggro timing** (§ 4.5 residual) — on going visible, instant or delayed? | Goal 1 | One observation, folded into any trial. |

**PC specs still unknown to the team** (legolas § 7 open question) — GPU/VRAM. Matters only if
a local model is ever needed; on current direction, it may never be.

---

## 6. OPEN RULING — Q47

**Surfaced to `canonical/matt_decision_needed/` this session.**

Matt's goal 3 says *"tune it towards **acceptable accuracy**."* **That term is undefined, and
it is the term that sizes the entire measurement program.**

| If "acceptable" means… | Instrument | Trials | Matt's hours |
|---|---|---|---|
| ±5% on time-to-kill, **per fight** | precise, frame-accurate | many | high |
| ±15% **in aggregate** across many fights | coarse | moderate | medium |
| **rank-ordering preserved** (build A beats build B in both engines) | very coarse | moderate | **low** |
| "no result that reads as obviously wrong" | eyeball | few | minimal |

**Two questions, not one:**
1. What is the tolerance?
2. **Is it per-fight or in-aggregate?** These are very different bars. **gandalf's lean: in
   aggregate, and rank-ordering-preserved is probably the honest bar** — it is what actually
   protects against the failure we care about (a key that mis-orders builds), it is far cheaper
   to hit, and it does not pretend to a precision the underlying variance can't support.

**gandalf has been fumbling this question by proxy for a session.** Every instrument decision
made before it is ruled is a guess.

---

## 7. Where everything landed — doc cross-reference

**Nothing from this session lives only in conversation.** Full paths:

| Artifact | Path |
|---|---|
| **This hand-off** | `agentic_orchestration/skill_handoff_2026-07-25.md` |
| Live AI-state observations + full synthesis (§§ 7–8 carry the binary cross-check) | `agentic_orchestration/gandalf/notes/2026-07-25-gd-observed-ai-states.md` |
| **Complete 40-state table + 51-command table** (legolas, binary) | `research/knowledge/gd/2026-07-25-gd-ai-state-tables-complete.md` |
| Console command table + `Origin` adjudication | `research/knowledge/gd/2026-07-25-gd-console-command-table.md` |
| Custom-Game unlock + Crucible contamination diff | `research/knowledge/gd/2026-07-25-gd-custom-game-console-unlock.md` |
| Instrument scoping (Q1 non-vision channels — **partially superseded, Grim Internals still live**) | `research/knowledge/gd/2026-07-24-playtest-capture-instrument-scoping.md` |
| Original commission (**premise dissolved — see § 3**) | `research/commissions/2026-07-24-gandalf-gd-playtest-capture-instrument-scoping.md` |
| **PC-side probe sheet** (operative; version-controlled copy) | `agentic_orchestration/gandalf/pc-handoff/2026-07-25-gd-teleport-probe-directions.md` |
| Probe #1 record (T8, ✓ done) | `canonical/matt_to_do/2026-07-24-gd-console-overlay-probe.md` |
| **Overlay screenshots — galadriel's CV/OCR reference input** | `agentic_orchestration/gandalf/fixtures/2026-07-25-gd-anger-overlay/` (4 files) |
| Matt action queue (T9) | `canonical/matt_to_do/README.md` |
| **Matt decision queue (Q47)** | `canonical/matt_decision_needed/README.md` |
| Gap register (five original KPIs) | `agentic_orchestration/gamora/notes/2026-07-24-tsf6-track-a-run.md` § 3 |
| Corpus editions + manifest-pin validation | `agentic_orchestration/gandalf/notes/2026-07-24-gd-edition-II-cut-record.md` |
| TRUE-SOURCES canon change (D-a / D-b / TSR-4 coverage tier) | `agentic_orchestration/gandalf/notes/2026-07-24-true-sources-founding-evidence-canon-change-proposal.md` |
| Ratification request (**owed — jack-ryan**) | `agentic_orchestration/qa/pending/2026-07-24-gandalf-true-sources-reframe-ratification.md` |

### Owed to other seams

| Seam | Owed |
|---|---|
| **gamora** | **The 40-state audit against our sim's model** (§ 4.1). Every "we don't model this" claim in this doc is *provisional* until she runs it. Then: expand the TSF6 gap register from 5 KPIs to the seven families. |
| **elrond** | `source_version` backfill on Edition-I rows before any gdx3 row lands. Conversion-key coverage beyond width one. |
| **jack-ryan** | Ratify D-a, D-b, and the TSR-4 coverage tier. |
| **galadriel** | Capture pipeline — **but hold until Q47 rules.** Scope is now line-detection + OCR of *one* label region + frame timestamps. Deterministic CV. Fixtures are banked and waiting. |
| **legolas** | BROADEN: re-audit PoE1/PoE2, D2, LE lanes for undeclared coverage boundaries (own charter, queued). |

---

## 8. Method observations — the part most likely to be lost, and most worth keeping

### 8.1 Two option-space failures, same shape, one session

| Episode | How the question was framed | The move that was available |
|---|---|---|
| **The mod container** | *"which mod changes the least?"* — diffing Crucible controllers, checking whether `ModdingTutorial` defines any, costing 280 MB of byte-identical copies | ***"make the delta not exist"*** — an empty `mkdir`. **Matt found it.** |
| **The coordinates** | *"how do we read the coordinates?"* — hover inspector, PlayStats, teleport probes | ***"stop needing them"*** — `character.WarpCursor`, sitting in a table we had already extracted, transcribed and committed |

**Both answers were already inside the material we held.** The failure is not in the gathering.
**It is in the shape of the question asked of what was gathered.** The null case and the
dissolve-the-requirement case were outside the generated option space both times.

A third instance, smaller: framing the anger overlay as *"number / bar / on-off"* when it is a
**directed graph edge** — a relational primitive richer than every branch of the option space
offered.

### 8.2 Partial view stated as fact — four instances, and the differentiator

| # | Inference | Outcome |
|---|---|---|
| 1 | *"numbers differ → the secondary source is wrong"* | **Banked as canon. Wrong. Stood a full program cycle.** |
| 2 | *"the tutorial world is a 48-byte stub"* (gandalf; read `assets/` only) | **Banked to Matt. Wrong** — the buildable source was in `source/`. |
| 3 | *"FoI is an Inquisitor skill → Inquisitor is Forgotten Gods → gdx2"* (gandalf) | **Banked in a provenance record. Wrong** — the archive was named in the localization tag, in our own notes. |
| 4 | *"I found a terminator, therefore I found the end"* (legolas, two enums) | **Falsified by the running game** when Matt observed `Roam`. |
| — | *"the 60s are UI padding"* (gandalf) | **Routed to verification. Wrong, caught in ~20 min.** |
| — | *"a byte-identical passthrough mod"* (gandalf) | **Routed as confirm-or-destroy. Half destroyed before shipping.** |

**The differentiator is not intelligence, model tier, or care. It is whether the inference was
banked or routed.** The proposal that names this finding now has its author as three of its
data points.

**And this session added a fifth level: intent.** § 0 — gandalf ran the program as though goal
1 were the whole thing. Same shape, applied to *what we are doing* rather than *what is true*.

### 8.3 Falsifier-first beats agreement-accumulation

§ 4.3. The two-layer model was confirmed because it carried a **named falsifier** (`Walk`
top-left) that was checked. Cheap now; a protocol built on a wrong label-mapping produces
numbers that look fine and mean nothing.

### 8.4 A near-miss worth recording

gandalf's pushback in § 3 (*"we'd tune to our own feel anyway, so numbers don't matter"*) was
**correct for goal 1 and completely wrong for goal 3**, and was argued confidently while
reasoning about only one of three goals. Had Matt not restated the charter, the program would
have de-scoped the measurement work that goal 3 makes unavoidable.

**The corrective is not "push back less."** It is: **before arguing scope, restate the goal set
and check the argument against each one separately.**

---

## 9. Carried forward — not touched this session

- **Story session (ELICITOR)** — five story gaps; **Q37** successor title; persistence R2–R8.
- **Q44** — deferred to the story session by Matt (*"we need to flesh the story out further"*).
- **Q46** — Murzak compiled-in cloud default; **T4** Murzak MCP column stand-up.
- **gdx3 lap open rulings** — playerclass10 kit-count / GD-SLICE denominator (elrond);
  whether TSF6/VDM must model the **Black Lodge Chaser** outlier (`MaxPursuitDistance` 2000,
  `PursuitTime` 6,000,000 ms — likely sentinels for *"never disengage,"* implying a
  nullable/infinite-leash primitive); adapter coverage for 18 new record types; Ascension scope.
- **T1** Remote Control · **T2** min-spec hardware · **T3** W3 flavor run · **T6** Vercel auth.
- **`reincarnated-legolas-operating-procedure`** still describes a single two-mode legolas.
- **The door-arg RFC (R3).**

---

## 10. If you read this cold, start here

1. **§ 0** — the three goals and the dependency.
2. **§ 2.3** — the constraint ladder. **L0 is runnable now.**
3. **§ 5 items 1–3** — what Matt does next, and why the order changed.
4. **§ 6** — **Q47 is blocking.** Instrument decisions made before it rules are guesses.

**Signed:** gandalf, 2026-07-25. The corpus is frozen, the vocabulary is complete, the container
is uncontaminated, and the rig exists in principle. What is missing is a tolerance and a
`game.Spawn` that works.
