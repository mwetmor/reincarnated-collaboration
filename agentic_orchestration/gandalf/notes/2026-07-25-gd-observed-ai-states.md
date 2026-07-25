# GD live-observed AI state vocabulary — Matt's overlay notes

**Date:** 2026-07-25
**Observer:** Matt, at the PC, empty-mod Custom Game, `character.LogData true`
**Recorded by:** gandalf
**Status:** PRIMARY OBSERVATION — first-hand, not derived.
**Binary cross-check RETURNED 2026-07-25** (legolas):
`agentic_orchestration/research/knowledge/gd/2026-07-25-gd-ai-state-tables-complete.md`.
See § 7 for what it confirmed, corrected, and reframed.

---

## 1. The structural finding: there are TWO green labels, not one

Matt: *"Can be top left or bottom right green word (Action State:)"*

The `character.LogData` overlay draws a green state word at the **top-left** of a monster and,
in some cases, a second green word at the **bottom-right**. This was not previously known —
we had been treating the overlay as emitting a single state string.

## 2. The observations, as reported

| Condition | States observed |
|---|---|
| Visible **in either** position | `Idle`, `Walk`, `Dying`, `Move`, `Attack` |
| Visible **only top-left** | `Reposition for Attack`, `Pursue`, `Roam` |
| Seen while player **INVISIBLE** | `Idle`, `Walk`, `Roam` |
| Seen while player **VISIBLE and nearby** | `Dying`, `Move`, `Attack` (+ the top-left-only set) |

Matt's note: *"There are only a couple of states that enemies enter when invisible, which is
why I toggled it off for further data."*

## 3. The split is clean, and it maps onto the binary tables

Every word Matt saw in **both** positions — `Idle`, `Walk`, `Move`, `Attack`, `Dying` — is a
member of **Table 1 (AI Action State**, `Game.dll` ~5192700–5193180, prefix `"Action State: "`).

Every word Matt saw **only top-left** — `Roam`, `Pursue` — is a member of **Table 3
(ControllerMonster AI State**, `Game.dll` 5418372–5418829). Neither is in Table 1.

**Hypothesis (INFERRED — routed to legolas to confirm or destroy, not banked):** the two label
positions render **two different layers of the AI**. One position draws the *action* layer
(what the body is physically doing) and the other draws the *controller* layer (what the
decision-making is doing). If true, the top-left word is the one that matters for every KPI we
care about, because intent lives there and animation does not.

**`Reposition for Attack` is in NONE of the three tables as previously reported.** That is
either a fourth table or — more likely — evidence that our Table-3 enumeration is still a
partial view. Table 3 was reported as "40 entries" with only **7 named**. We have never seen
33 of them. Sent to legolas for the complete enumeration.

## 4. What this buys us, per KPI

- **KPI 1 (aggro onset radius) and KPI 3 (pursuit/leash) gain a second, independent readout.**
  The aggro event now has a *name*: top-left going `Idle`/`Roam` → **`Pursue`**. That is a text
  transition, OCR-able, and entirely separate from the red anger line. Two channels observing
  the same instant means the instrument can **check itself** — if line-appearance and
  `Pursue`-onset agree frame-for-frame across trials, neither has to be taken on faith. We did
  not have a validation path before; now we do, for free.

- **KPI 4 (idle wander) is effectively SOLVED by `character.SetPlayerInvisible`.** The hard
  part of KPI 4 was never the measurement — it was that observing an un-aggroed monster
  requires being present, and being present aggros it. Invisibility gives a clean un-aggroed
  observation window on demand, and Matt's data confirms the peaceful-state set collapses to
  `Idle` / `Walk` / `Roam`. `Roam` appearing *only* top-left further suggests it is the
  controller-layer decision ("go wander") while `Walk` is its action-layer expression — which,
  if confirmed, means `MaxTimeBeforeRoam` is directly readable as the dwell in `Idle` before
  the top-left word flips to `Roam`.

- **KPI 2 (anger accumulation) — still open, and this is the live question.**
  `AlertBeforePursue` was **not** in Matt's list. That is NOT evidence of absence: he was not
  looking for it, and a brief state is easy to miss. Re-asked explicitly in probe #2 § 4a. If
  a state exists between the peaceful set and `Pursue`, its dwell time IS the anger latency,
  and the pre-registered prediction stands: **dwell at outer range ÷ dwell at inner range
  should be 4.0** (`SightAngerRate` 3.0 vs `InnerSightAngerRate` 12.0). If no intermediate
  state renders, we fall back to the visibility-flip trial.

## 5. `Reposition for Attack` — a possible SIXTH gap

Our sim has no concept of a monster **spacing itself** for an attack. `Reposition for Attack`
is a combat-maneuver state distinct from `Move` and from `Attack`, and it is plausibly a large
part of why GD encounters *read* as tactical rather than as a blob converging on the player.

This is a **play-feel** finding rather than a parameter finding, and it is the kind that does
not show up in a parameter-fidelity audit at all — TSF6-TRACK-A scored our pursuit distance at
+0.15% faithful while the sim has no repositioning concept whatsoever. A perfect score on the
parameters we model says nothing about the parameters we don't.

**Not yet a gap-register entry.** It needs (a) legolas's confirmation that the string is a real
controller state, and (b) a look at what governs it in the `.arz` before it can be specified.
Registered here so it isn't lost.

## 6. Provenance

Matt's message, verbatim:

> Here are some notes I took while invisible and visible. There are only a couple of states
> that enemies enter when invisible which is why i toggled it off for further data.
> Can be top left or bottom right green word (Action State:):
> Can be seen when invisible: Idle, Walk
> Can be seen when visible and nearby: Dying, Move, Attack
> Can only be the top-left green word: Reposition for Attack, Pursue, Roam (both when visible or invisible)

---

## 7. Binary cross-check returned — the complete 40-entry table

Source: `agentic_orchestration/research/knowledge/gd/2026-07-25-gd-ai-state-tables-complete.md`
(legolas, `Game.dll` 5418372–5418812, count verified at exactly 40).

```
 1 Idle              11 Dying             21 Confused          31 QuestWalk
 2 Startup           12 Return            22 Paralyze          32 QuestMove
 3 Attack            13 FollowLeader      23 Trapped           33 QuestUseSkill
 4 Pursue            14 Dead              24 Immobile          34 QuestPlayAnimation
 5 RepositionForAttack 15 NavigateObstacle 25 KnockedDown      35 TakeHit
 6 JumpAttack        16 DefendLeader      26 Stunned           36 GettingUp
 7 Roam              17 Charge            27 Scared            37 UseSkillOnPoint
 8 Flee              18 Move              28 Sleeping          38 UseSkillOnAlly
 9 WanderPause       19 Panic             29 WaitToAttack      39 Emote
10 Wander            20 DodgeAttack       30 Patrol            40 AlertBeforePursue
```

### 7.1 What it CONFIRMED

- **`AlertBeforePursue` is real** — entry #40, offset 5418812, with a full RTTI class
  `ControllerMonsterStateAlertBeforePursue@GAME` carrying `OnBegin` / `OnUpdate` / `OnEnd`.
  It is a live state, not a vestigial string.
- **`RepositionForAttack` is entry #5** — not a fourth table. The spaced form Matt reported
  does not exist in any binary; the states are CamelCase and he read it naturally. **The
  "possible fourth table" worry is CLOSED.**
- **The two tables are genuinely disjoint state machines, not one falling back to the other.**
  Table 3 carries its own `Idle` (#1), `Attack` (#3), `Dying` (#11), `Move` (#18) as
  independent entries. Seeing `Idle` at both overlay positions therefore means **both FSMs are
  simultaneously in `Idle`** — two readings, not one echoed twice.

### 7.2 What it CORRECTED — and it corrects me

I pre-registered `AlertBeforePursue` as the answer to **KPI 2** (anger accumulation), on the
reading that it is the state a monster occupies *while accumulating anger*. Anger accumulation
is rate × time — a **timer**.

Legolas found the class carries **its own `HandleEvent` override, which most states do not.**
That is evidence the state is at least partly **event-driven**, which is not what a pure anger
timer looks like.

This does not destroy the hypothesis — `OnUpdate` can still run an anger timer while
`HandleEvent` handles an interrupt. But it opens a second reading I had not considered:
`AlertBeforePursue` may be the **distress-call response** state (KPI 5) — where a monster sits
after hearing a neighbour's alert, before deciding whether to commit. `ChanceToRespondToDistressCall`
is 75, i.e. a *decision*, and a decision made on receipt of an event is exactly what a
`HandleEvent` override implements.

**Most likely it is both**: entered on sight, running an anger timer, and additionally
short-circuited to `Pursue` by an incoming distress event. If so it is the single most
valuable state in the table, sitting on top of two of our five blocked KPIs.

**Not banked.** Legolas states plainly that transition conditions cannot be determined from
string extraction, and I am not filling that gap by inference. It is cheap to distinguish live
and the live test is now in probe #2 § 4a.

### 7.3 ✓ RESOLVED — the two-layer model SURVIVED its falsification test

Matt's initial notes listed **`Walk`** in *either* position, and **Table 3 contains no `Walk`**
— so if top-left renders Table 3, `Walk` top-left is impossible. That single observation was
the falsifier for the entire model, and it was routed back rather than explained away.

**Matt, 2026-07-25:** *"My mis-communication. Walk only renders on the bottom-right."*

Outcome (2) of the three offered. **The model is confirmed, and the confirmation is worth more
than the original agreement was**, because it was reached by naming what would break the model
and then checking that specific thing — not by accumulating consistent observations.

**The mapping is now LOCKED:**

| Overlay position | Table | What it is | Entries |
|---|---|---|---|
| **top-left** | Table 3 — ControllerMonster AI State | the **decision** layer: what the monster has decided to do | 40 |
| **bottom-right** | Table 1 — AI Action State (prefix `"Action State: "`) | the **action** layer: what the body is physically doing | 19 |

And the resolution supplied a *positive* confirmation instance, not merely the absence of a
contradiction: Matt observed `Roam` top-left while `Walk` rendered bottom-right — decision says
*roam*, body says *walk*. That is exactly the pairing the two-layer model predicts.

**Consequence for the capture pipeline (galadriel):** every one of the five KPIs reads off the
**top-left label alone**. The OCR pipeline needs **one** label region per monster, not two. The
bottom-right label is retained as an optional cross-check, not a requirement. That is a real
simplification arriving before a line of pipeline code was written — which is the point of
resolving the anomaly first rather than after.

### 7.4 A SIXTH gap-register candidate — the combat-spacing cluster

Four entries describe behaviour our simulation has no concept of whatsoever:

| Entry | What it implies |
|---|---|
| **#5 `RepositionForAttack`** | monsters take up position rather than closing to contact |
| **#29 `WaitToAttack`** | monsters *hold* rather than all committing at once |
| **#20 `DodgeAttack`** | reactive evasion |
| **#6 `JumpAttack`** | committed gap-closer as a distinct state |

`WaitToAttack` is the structurally important one. A state whose entire job is *not attacking
yet, while able to* is the signature of an **attack-token / turn-taking system** — the
Arkham-lineage device that stops every engaged enemy swinging simultaneously. It is a large
part of why a GD pack reads as a *group of fighters* rather than a blob converging on the
player, and it is invisible to any parameter audit: TSF6-TRACK-A scored our pursuit distance
at **+0.15% faithful** while the sim has no repositioning, holding, or dodging concept at all.
**A perfect score on the parameters we model says nothing about the ones we don't.**

### 7.5 A SEVENTH candidate — pack hierarchy

**#13 `FollowLeader`** and **#16 `DefendLeader`** establish that GD packs have a **leader**.
Our sim has no leader concept.

This also converts a risk into a test. I registered earlier that console-spawned monsters may
arrive without the pack association world-placed monsters carry — biasing KPI 4 (wander is
anchor-relative) and KPI 5 (if pack membership gates distress response). That risk was
unfalsifiable when raised. It now has a **visible signature**: if world packs show
`FollowLeader`/`DefendLeader` and spawned packs never do, spawned monsters are impoverished and
the experiment rig must be built on world packs. Added to probe #2 as § 4c.

### 7.6 Other entries that map onto existing KPIs

- **#12 `Return`** — the leash disengage has a name. KPI 3's end-event is now readable as text.
- **#9 `WanderPause` / #10 `Wander` / #7 `Roam`** — three distinct idle-locomotion states where
  we assumed one. `MaxTimeBeforeRoam` may be the `Idle`→`Roam` dwell, but `WanderPause` sitting
  beside `Wander` suggests the idle loop has internal structure (move, pause, move) that a
  single `WanderDistance` parameter does not capture.
- **#8 `Flee` / #19 `Panic` / #27 `Scared`** — three distinct fear states against our one
  `fleeDistance`. The flee-on-low-HP gap is probably larger than "add an HP trigger."

### 7.7 Standing coverage boundary (D-a)

Legolas's declared boundary, carried forward: **the transition conditions for
`AlertBeforePursue` cannot be determined from string extraction.** The binary establishes the
class is live and event-responsive; it does not establish when it is entered. Resolving that
requires either disassembly of `OnBegin`/`OnUpdate`/`HandleEvent` or a live measurement
protocol. **Live measurement is the cheaper path and is now specced.**

---

## 8. Matt's second observation round — 2026-07-25

### 8.1 ✓ Anger resets instantly — the trial design is sound, and REPEATABLE

**Matt:** *"Anger resets instantly. Red lines disappear and attacking monsters walk away."*

Confirms the visibility-flip trial: every trial starts from a true zero, no carryover.

**The larger consequence is repeatability.** Because monsters *disengage* rather than merely
losing the line, one pack supports an unbounded trial loop — invisible → reposition → visible
→ measure → invisible → reset → repeat, **without moving**.

That is decisive for **KPI 5 (distress propagation)**, where `ChanceToRespondToDistressCall` is
**75** — a rate, requiring dozens of trials for a usable estimate. Hunting a fresh pack per
trial was never realistic. The KPI was, quietly, the least tractable of the five; it is now
arguably the *most* tractable, because it is the one that benefits most from cheap repetition.

**Residual check (one observation, folded into the next trial):** on going visible again, is
re-aggro *instant* (accumulator merely paused) or *normal-delay* (accumulator zeroed)? Matt's
description strongly implies zeroed — they walked away — but the distinction is what makes the
loop valid, so it gets confirmed rather than assumed.

### 8.2 ★ THE TELEGRAPH — Matt saw `AlertBeforePursue` before we had a name for it

**Matt:** *"I have seen monsters slow down their state transition to allow for graphics such as
a zombie yelling and waving his hands angrily during a long beat of what seems like alert."*

He offered this as an aside about why he hadn't seen the state word. It is the most
consequential thing in the round.

He is describing **an observable, animated, pre-commitment beat** — which is exactly what
`AlertBeforePursue` looks like from outside the code. It corroborates independently: the
animation table (Table 2) carries a state named **`Alert`**. Behaviour observed live, state
confirmed in the binary, animation confirmed in a second table — three lines converging without
being derived from each other.

**Not banked.** The join between the observed beat and the named state is not established (D-b).
Resolving it costs one glance at the top-left word during the beat, and that is now the probe's
narrowest and highest-value ask.

### 8.3 The design finding — KPI 2 is not an AI parameter, it is a TELEGRAPH

This reframes the hardest of the five gaps, and it reframes it *out of* the engine lane and
*into* the design lane.

`SightAngerRate` 3.0 and `InnerSightAngerRate` 12.0 have been treated here as AI tuning
constants. If the anger window is occupied by an animated alert beat, then **those two numbers
are the duration of a player-facing telegraph**, and the 4× inner/outer ratio is a deliberately
authored **fairness curve**:

| Situation | Anger rate | Telegraph length | What the player experiences |
|---|---|---|---|
| spotted at range (outer zone) | 3.0/s | **long** | "it's seen me — I have time to decide" |
| walked into its face (inner zone) | 12.0/s | **short** | "that's on me, I was careless" |

The monster does not silently flip to pursuit. It **performs noticing you**, and the length of
that performance is inversely proportional to how much the situation is your own fault. That is
why GD encounters read as reactive and fair rather than arbitrary — and it is authored, not
emergent.

**Our sim has no telegraph concept at all.** Not a missing parameter — a missing *category*.
This is the clearest instance yet of the pattern § 7.4 named: TSF6-TRACK-A scored pursuit
distance at **+0.15% faithful** while the sim cannot represent the thing that makes GD's
encounters feel the way they do. **A perfect score on the parameters we model says nothing
about the ones we don't** — and the ones we don't are turning out to be the play-feel ones.

**Genre note.** This is not a Grim Dawn idiosyncrasy; it is ARPG craft with a long lineage.
Diablo II's Fallen shamans have a wind-up before they act; D3 formalised telegraphing into
ground decals and explicit wind-up frames as a readability discipline; D4 made telegraph
legibility a stated design pillar. GD's version is subtler — it lives in the AI state machine
rather than in a VFX layer — but it is doing the same job: **giving the player a beat in which
the encounter is comprehensible before it is dangerous.**

### 8.4 ✗ Rung 0 CLOSED NEGATIVE — no coordinate readout exists

**Matt:** *"I have tried hovering while I have pressed tilde… nothing prints or appears, and
no origin at all."*

Tested correctly (console open, cursor over objects). Accepted as a real finding.

Corroborated statically: the 51-command table contains **no object-inspection command** in any
namespace — the closest is `character.ShowPlayerTokens` ("dumps to the console"), which is
trigger tokens, not position. The `Origin = %f %f %f` block at exe 2687760 appears to be
unreachable from the shipped console.

**We have no coordinate readout in Grim Dawn.** `game.Teleport` therefore has no anchor and
drops to a low-priority probe.

### 8.5 ★ RECOVERY — `character.WarpCursor`, and it is better than teleport

Re-reading the command table after the negative surfaced an entry skimmed past on the first
pass:

> **`character.WarpCursor`** (exe 2684992) — *"Makes it so player always warps to destination"*

Click-to-move becomes click-to-**teleport**.

**This makes the coordinate problem irrelevant rather than merely survivable**, and it is worth
being precise about why, because the first framing was wrong. We wanted coordinates in order to
*know the separation numerically*. But the binding constraint was never the numbers — it was
that **the approach contaminates the trial**: walking toward a monster accumulates anger the
entire way, so the measurement starts dirty. Warping arrives with the clock at zero.

**Same option-space error as the empty-mod episode**, and worth recording as such. There, the
question was framed *"which mod changes the least"* when the move was *"make the delta not
exist."* Here it was framed *"how do we read the coordinates"* when the move was *"stop needing
them."* Both times the answer was already inside the material we held — an empty `mkdir`, and a
command sitting in a table we had already extracted, transcribed, and committed. **The failure
is not in the gathering. It is in the shape of the question asked of what was gathered.**

Full rig, assuming `WarpCursor` behaves as described:

```
character.SetPlayerInvisible true     → nothing reacts
character.WarpCursor true             → click to place, instantly, no approach
[position]                            → exact spot, clock at zero
character.SetPlayerInvisible false    → THE START INSTANT
[watch top-left word + red line]      → two independent channels
character.SetPlayerInvisible true     → reset
[repeat]                              → N trials, standing still
```

No coordinates required anywhere in it.

**Unverified — the probe asks:** max warp range, whether it respects pathing, whether it is
instant or animated, and critically **whether warping past a monster trips its aggro.** If
warping through a detection zone is silent, trials are clean; if not, routes need planning.
