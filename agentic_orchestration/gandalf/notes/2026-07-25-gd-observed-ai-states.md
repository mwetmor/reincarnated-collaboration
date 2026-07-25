# GD live-observed AI state vocabulary — Matt's overlay notes

**Date:** 2026-07-25
**Observer:** Matt, at the PC, empty-mod Custom Game, `character.LogData true`
**Recorded by:** gandalf
**Status:** PRIMARY OBSERVATION — first-hand, not derived. Binary cross-check in flight (legolas).

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
