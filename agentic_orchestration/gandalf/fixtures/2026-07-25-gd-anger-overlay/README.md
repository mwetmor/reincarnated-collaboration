# GD debug-overlay fixtures — CV/OCR reference input

**Banked:** 2026-07-25 by gandalf, from Matt's PC (T8 console probe)
**For:** **galadriel** — but **HOLD. Do not build the pipeline yet.** See § 3.
**Source of truth for the whole session:** `agentic_orchestration/skill_handoff_2026-07-25.md`

---

## 1. What these four files are

Grim Dawn running in an **empty-mod Custom Game** (a folder in `mods/` containing nothing — no
`database.arz` exists in it, so vanilla records load untouched and instrument contamination is
*impossible by construction*, not merely mitigated). Two debug overlays enabled from the in-game
console (backtick):

| File | Overlay | Command |
|---|---|---|
| `anger-overlay-1..3.png` | aggro relation | `character.ShowAngerLevels true` |
| `logdata-overlay-4.png` | per-entity AI state text | `character.LogData true` |

**Note the argument is `true`, not `1`.** Both gandalf and legolas shipped `1` unverified; Matt
found it. Recorded because the shape repeats.

---

## 2. What the overlays actually render — read this before writing a detector

**The anger overlay is a DIRECTED GRAPH EDGE, not a scalar.** A **solid red line from mob to its
anger target**, appearing at the instant of commitment, and correctly pointing at **other mobs**
during infighting. gandalf's read-out questions had framed it as "number / bar / on-off" — that
option space was wrong, and the relational primitive is richer than any of its three branches.

- **The line is always solid.** Matt corrected an earlier gandalf reading: apparent dashes are
  **terrain occluding a depth-tested 3D line**, not a line style. Do not build a solid-vs-dashed
  classifier; do expect occlusion gaps and design the detector to tolerate them.
- **Edge appearance / disappearance geometry and timing** is where KPIs 1 (aggro onset), 3
  (pursuit/leash) and 5 (distress propagation) all come from.

**The `LogData` text has TWO layers, and they are disjoint state machines.** Confirmed by
falsification (Matt's `Walk` report was routed back as a named falsifier and he corrected it
himself — the model held):

| Screen position | Layer | Vocabulary |
|---|---|---|
| **top-left** | the **decision** — what the monster has decided | 40 `ControllerMonster` states (`Idle`, `Roam`, `Pursue`, `AlertBeforePursue`, `WaitToAttack`, …) |
| **bottom-right** | the **action** — what the body is doing; prefixed `Action State: ` | 19 entries (`Walk`, `Move`, `Attack`, …) |

**Pipeline consequence: read ONE region per monster — the top-left label.** Bottom-right is
confirmation, not signal. Complete tables:
`agentic_orchestration/research/knowledge/gd/2026-07-25-gd-ai-state-tables-complete.md`.

**Two independent readouts of the same instant.** The red edge appearing and the top-left word
going `Pursue` should coincide. If they agree frame-for-frame across many trials, **the instrument
is self-validating** and neither has to be taken on faith. Build the cross-check in from the start;
it is nearly free and it is the only validation available without a second instrument.

---

## 3. ⚠ WHY YOU ARE HOLDING — Q47

**Scope is gated on `canonical/matt_decision_needed/README.md` → Q47** — *what is "acceptable
accuracy," and is the bar per-fight or in-aggregate?* That ruling sets required precision, which
sets whether this is a frame-accurate pipeline or a coarse one. **Every pipeline decision made
before Q47 rules is a guess**, and the cost delta between the bars is large.

**What the scope looks like under gandalf's lean** (in-aggregate, rank-ordering-preserved):
**line detection + OCR of one label region + frame timestamps.** Deterministic CV, ~$0/hr. That is
the collapse of the original commission, which had scoped a **VLM bake-off at $0.23–31/hr** to
*infer* quantities the game will simply print. Disposition:
`research/commissions/2026-07-24-gandalf-gd-playtest-capture-instrument-scoping.md`.

---

## 4. Known capture caveats

- **Zoom is player-adjustable and the camera rotates**, so pixel→world calibration is genuinely
  messy. **Prefer not to need it** — `character.WarpCursor` (untested, T9 item 2) would let the
  player *set* separation rather than have it measured, deleting the calibration problem instead
  of solving it.
- **Legibility at normal zoom is unverified** for the green text. If OCR struggles, that is a
  protocol constraint on how Matt plays, and it should be reported as such rather than worked
  around silently.
- More fixtures will arrive from the T9 probe → share `visual-artifacts/2026-07-25-gd-teleport-probe/`.
