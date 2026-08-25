# KC2-MC mini-lap RESID-D1-2 — The Immobility Decode

**Author:** legolas (returned 2026-08-25; prose verdict conductor-captured verbatim-in-substance from the lap return — the harness blocked the lap's own report write, second occurrence after D-12; evidence in this directory was committed by the lap itself at `d6fd09b4` + `f44982aa`: 66 evidence files, 17 regenerating scripts `r1`–`r14`).
**Commission:** gandalf RUN-CONDUCTOR, R-L70-4 (MD-B5-2 / MD-B6-2). Fold of record: run charter L-71.
**Question (verbatim):** *"does the controller's outer update move a body whose state issues no locomotion call?"* Stakes: *"it decides whether B-5 has any effect at all."*

---

## § 0 — VERDICT

> **`RESID-D1-2` / `UNREACHED-U1`: DECODED. The body DOES stand still.** The controller's outer update does NOT move a body in `AlertBeforePursue`. **`C-B5-1` discharges IN FAVOUR of B-5** — the modelled hold is substrate-enforced, not declared. **`A2 − A1` is B-5's effect, entire.**
>
> ⚑ **But the enforcement is not where the run was looking, and not unconditional.** Immobility is not the state machine's doing (`Pursue::OnEnd` is a bare `ret`; the alert state issues no stop). It is the **action layer**: a shipped **26×26 `CharacterActionPermission` matrix** decides whether the alert animation *displaces* the current action. Ordinary case: cell = `0 = REPLACE`, move is `Finish()`ed, body halts. **Ten of twenty-six current-action types give `1 PENDING` or `2 REJECT`** — the alert animation is deferred/dropped while the state is pushed anyway, decoupling the hold's duration from the alert `.anm` length that D-1 § 3.3 and B-5 model. New named limb (§ 5), reported-not-graded.

## § 1 — Substrate pins

`Game.dll` sha256 `4876d6bd…78ab02` and `Engine.dll` `7141b51a…64c87c` — **both identical to D-1's pins.** All RVAs, image base `0x10000000`. Read-only throughout. Cross-anchor: the `Character` vtable slot numbering that yields these answers is the one that already yielded D-1's `+0x1e0 AnimationCallback` "End" dispatcher.

## § 2 — One locomotion hop, image-wide

`?Update@CharacterMovementManager@` (`0x781a0`) has **exactly one call site**: `Character::UpdateSelf+0x38d` (`0x4ce5d`), gated on `IsAlive()` (evidence `31`/`32`). `ControllerAI::Update` (`0xe5b80`) issues **no** locomotion call. The commission's question reduces without residue to one function.

## § 3 — The movement gate + the state the alert writes

- **`CMM::Update` runs IFF `GetActionState() ∈ {5 Move, 6 Walk, 19 Jump, 20 (unnamed), 21 Evade}`** — five compares at `0x781b0`–`0x781ec` (evidence `33`); otherwise early-return. `GetActionState` = `mov eax,[ecx+0x1b9c]; ret`.
- The `Character_ActionState` enum decoded **by name** from `GetActionStateAsText`'s 22-entry jump table (evidence `84`/`85`). Value **20 has no shipped name**; its sole producer is `MoveAttackAction::Execute+0x112` (census, evidence `86`).
- `AlertBeforePursue::OnBegin` → `ControllerAI::PlayAnimation` (`0xe77f0`) constructs a `PlayAnimationAction` (type **18**, no pre-action — `[this+0x14]=0` at `0xe7854`) whose `Execute` (`0x704b0`) ends in **`SetActionState(2 = Play Animation)`**. `2 ∉ {5,6,19,20,21}` ⇒ **`CMM::Update` early-returns every tick of the alert.**

## § 4 — The displaced move is ACTIVELY STOPPED (two independent mechanisms, both decoded)

1. **The stop:** `CharacterActionHandler::Execute` (`0x724f0`) `Stop()`s the current action before installing the new one; for the displaced pursue move that is `MoveToAction::Finish` (`0x6c850`), whose tail is `CMM::Stop` **inlined verbatim** → IAT-resolved (evidence `88`) `Engine.dll :: NavManager::StopObject` (`0x127aa0` → crowd impl `0x2045c0`, evidence `89`): **the agent's goal position is overwritten with its own current position** (`[+0x70..0x78] := [+0x40..0x48]`). Nothing left to travel toward. `CMM::IsMoving := FALSE`.
2. **The permission:** `CheckAction@ControllerBaseCharacter` (`0xea260`, evidence `66`) indexes `permission[newType*26 + curType]` at `gGameEngine+0x2802c` — a **26×26 matrix** filled by `InitializeActionMatrix` (`0x26d7c0`), reconstructed **byte-exactly** by `r8_matrix.py` (evidence `71`/`72`; reconstructor HALTs on unmodelled store forms, asserts 676 cells written, zero stores outside the window — stride decoded, not assumed). Semantics decoded from `LocalHandleAction` dispatch: `0 REPLACE · 1 PENDING · 2 REJECT · 3 DEFER · 4 interrupt-then-replace`.

> ### ⚑ THE LAP CELL: `permission[18 PlayAnimationAction][4 MoveToAction] = 0 = REPLACE.`
> Row 18 is `0` against **every producer of a gate ActionState** (MoveTo 4, Walk 5, Attack 8 — with `MoveAttackAction`/`JumpAttackAction` **inheriting type 8** via base-ctor call, closing the ActionState-20 hole — and Evade 24).

- Nothing re-issues a move under the alert: `AlertBeforePursue::OnUpdate` only calls `RotateTowards` (evidence `98`); its `RequestMove` slot is the ICF-folded no-op `ret 8` at `0xf100`.
- **Ordering decoded (§ 4.4):** `SetState("Pursue")` runs `Pursue::OnBegin` **inline** (three `MoveTo` sites) → `SetActionState(5)`; then `AddTemporaryState` runs the alert's `OnBegin` **inline** (`Pursue::OnEnd` = bare `ret`, stops nothing). **The entire alert entry including the halt happens inside one call of `DefaultEnemyFoundResponse`, in one tick, at the action layer.** D-1's refusal to conclude immobility from `OnUpdate`'s silence was right — the mechanism was one layer down.

## § 5 — ⚑ FLAG-DON'T-FLIP: the three-regime limb the premise did not contain

Row 18 of the matrix has **three regimes**; only the first is what B-5 models:

| `permission[18][cur]` | current-action types | consequence |
|---:|---|---|
| **0 REPLACE** | 0, 1, 3, **4 MoveTo**, 5 Walk, 6, 7, **8 Attack (+inherited)**, 24 Evade, 25 | animation plays, move `Finish()`ed, body halts — **the modelled case** |
| **1 PENDING** | 9 Stun, 10 Knockdown, 11 TakeHit, 12 Sleep, 13 Immobilize, 14 Trap | alert animation **deferred**; state pushed regardless |
| **2 REJECT** | 2, 15 Die, 16, 17, 18, **19 Spawn**, 20, 21, 22, 23 | alert animation **dropped**; state pushed regardless |

On PENDING/REJECT the `"End"` that pops the state belongs to **some other animation** — **the hold's duration is decoupled from the alert `.anm` length** (D-1 § 3.3 narrowed, not overturned). Concretely reachable: `19 Spawn` is REJECT, and Crucible bodies are spawned. Whether any of B-5's **26 fired closures** sat on a non-REPLACE action is a **sim-side** question — cheap instrumentation: per-closure record of the referent's current-action type at the push. **Reported-not-graded.** The § 0 verdict is not weakened: on the row B-5's population occupies, the answer is unambiguous. Duration caveat, not an immobility caveat.

## § 6 — Residuals (named, with break points)

- **`RESID-D1-2a`** — crowd-solver settle after `StopObject` (Engine.dll `0x204650`, unexported): at most one solver step of drift vs a 1.33–2.43 s hold — cannot change any measured outcome.
- **`RESID-D1-2b`** — `SetMotion({0,0,0})` in `MoveToAction::Finish` is **conditional** (skill-id resolvable); not load-bearing — `StopObject` is unconditional modulo `IsActivated`. Named so nobody inherits "velocity is zeroed" as unconditional.
- **`RESID-D1-2c`** — `AddTemporaryState` asymmetry: pushed onto a **non-empty** temporary stack, the new state's `OnBegin` is **never called** (`0xe6ac8`). Not reachable at engagement onset; **flagged for the state-vocabulary seam** (B-6 sealed — carried to wave-close seating).
- **`RESID-D1-2d`** — ActionStates 11/16/20 unnamed in shipped text; 20's sole writer decoded; 11/16 outside the gate; no claim rests on their names.
- **Methodological, published:** evidence `86` is a byte-pattern census that over-collects foreign vtables' slot `0x224`; foreign rows **left in the artifact unfiltered** so the over-collection is visible.

## § 7 — Sim implications (reported-not-graded, R-L56-2)

1. **`C-B5-1` discharges affirmatively** — B-5's σ-narrowing (2.098→1.673, mean 153.0 exact) never needed the hedge; `A2 − A1` is B-5's effect entire.
2. **`B5-P1b`** (non-vacuity) now has substrate backing — equality there would indicate a fold defect, not an inert mechanism.
3. **`B5-P20`** ("suppresses travel and nothing else") — substrate agrees by a stronger route: ActionState change + nav-goal reset touch nothing in life/targeting/collision/anger.
4. Refinement offered without recommendation: the hold is `permission[18][cur]==0`, not an unconditional gate consequence — carry the § 5 row if the fold generalises past tier-16 KC2.
5. **Nothing touches alert incidence** — D-1 § 2.5's populations and B-5's 260 `L2_chance_roll` closures untouched.

## § 8 — Prior-lap ledger

`RESID-D1-2` **CLOSED** (re-pointed: action-permission matrix, not state machine) · `UNREACHED-U1` **CLOSED** (one call site) · `UNREACHED-AA-4` **CLOSED — now DECODED** · `C-B5-1` **DISCHARGED IN FAVOUR** · `MD-B5-2`/`MD-B6-2` **RETURNED** · D-1 § 3.3 **narrowed** (true on REPLACE row only) · D-1 § 6 DO-NOTs + `RESID-D1-1/-3/-4` carried unchanged.

## § 9 — ⚑ DO-NOT block (binding on B-5, B-6, B-4app and the baton)

1. **DO NOT** model the hold as a property of the alert *state* — it is the **action layer** (displace-and-`Finish` + an ActionState outside the movement gate).
2. **DO NOT** treat `permission[18][cur]==0` as universal — ten of twenty-six types give 1 or 2; there the alert `.anm` length is NOT the hold's duration.
3. **DO NOT** re-derive the movement gate from state *names* — it is `{5,6,19,20,21}` read off `CMM::Update`'s compares, and **20 is unnamed**; a name-built model silently drops `MoveAttackAction`.
4. **DO NOT** cite `?CanMove@ControllerAI@` for anything — ICF-folded onto `xor al,al; ret` with four unrelated predicates. Fold artifact, enumerated so it is visibly excluded.
5. **DO NOT** read "the velocity is zeroed" as unconditional (`RESID-D1-2b`) — the unconditional part resets the *goal*, not the velocity.
6. All prior DO-NOT blocks carried unchanged (D-1 § 6, AA § 6, AB § 5.4, V/V-2/W/X/Y/Z/D-11/D-12).

## § 10 — Evidence index

66 files under `evidence/`, regenerated by `r1`–`r14` scripts beside them. Load-bearing: `31` (CMM::Update sole xref) · `33` (movement gate) · `66` (matrix index) · `71`/`72` (the 26×26 matrix) · `81` (MoveToAction::Finish inlined stop) · `82` (SetActionState 2) · `84`/`85` (ActionState enum by name) · `88`/`89` (IAT + Engine.dll NavManager) · full index in the lap return, captured in the run charter L-71 lineage.

---

*legolas (UNKNOWN-RESEARCHER), 2026-08-25. Read-only on all substrate. Commits `d6fd09b4`, `f44982aa`. No pushes.*
