# KC2-MC micro-lap MD-B4app-9 — Does the pursue MoveTo route through CheckAction?

**Author:** legolas (returned 2026-08-25; prose verdict conductor-captured verbatim-in-substance from the lap return — the harness blocked the lap's own report write, third occurrence, 3/3 standing practice; evidence in this directory was committed by the lap itself at `fcf07687`: 16 files, scripts `s1`–`s8` beside them).
**Commission:** gandalf RUN-CONDUCTOR, R-L75-2. Fold of record: run charter L-76.
**Question (verbatim):** *"Does the MoveTo issued inside `Pursue::OnBegin` route through `CheckAction` (0xea260) at all — or does it bypass the permission matrix and install directly?"*

---

## § 0 — VERDICT

> **BOOLEAN: `ROUTED`.** All three `Pursue::OnBegin` `MoveTo` sites reach `?CheckAction@ControllerBaseCharacter@` (`0xea260`). There is no direct-install path: `CharacterActionHandler::Execute` has **six** direct callers image-wide, and the only controller-initiated pair sits **downstream of the permission call**.
>
> ⚑ **AND THE MATRIX IS STILL NEVER READ.** `CheckAction`'s first act is an RTTI downcast of the *controlled entity* to **`Player`**. For a monster that returns `NULL` and the `je` at `0xea28c` is taken. **59 of the function's 130 instructions — the entire `gGameEngine+0x2802c` matrix read at `0xea306`–`0xea310` among them — are unreachable when the controlled entity is not a `Player`** (CFG dominance proof, evidence `13`). The monster limb is a small hand-coded `lifeState × actionType` rule returning **constant `0 = REPLACE`** for every non-`Die` action a non-terminal body requests.
>
> **The commission's two branches therefore split.** The boolean answers `ROUTED`; **the consequence is the one the commission assigned to `BYPASS`.** The pursue move installs unconditionally, every fired closure is REPLACE-outcome, **`MD-B4app-8`'s PENDING limb prices to ZERO**, and **`C-B4app-10`'s attribution question dissolves.** I report the split rather than picking the label that makes the consequence tidy.

## § 1 — Substrate pins

`Game.dll` `4876d6bd…78ab02`, `Engine.dll` `7141b51a…64c87c`, image base `0x10000000` — **verified before any RVA below was cited**, identical to RESID-D1-2's. Read-only throughout. Harness carried unmodified from the prior lap; new scripts `s1`–`s8`.

## § 2 — The call path, per MoveTo site

All three sites are **direct calls to the same terminal function** — none uses the `ControllerAIStateT<>::MoveTo` thunk at `0x60d40`, which has **zero** call sites image-wide (evidence `02`).

| # | site | in | target |
|---|---|---|---|
| 1 | `0x000ff1ee` | `?OnBegin@ControllerMonsterStatePursue@` `+0x3ae` | `0x000e6cd0` |
| 2 | `0x000ff264` | `…+0x424` | `0x000e6cd0` |
| 3 | `0x000ff2ca` | `…+0x48a` | `0x000e6cd0` |

All three load `ecx` from `[state+4]` (the owning controller) — the same idiom the `ControllerAIStateT<>` thunk uses at `0x60d49`, which is what identifies `[state+4]` as the controller.

Then, identically for all three (evidence `25`/`52`/`53` prior lap, `16` this lap):

```
0x000e6cd0  ?MoveTo@ControllerAI@                    builds the action
0x000e6dbb    mov dword ptr [ebx + 8], 4             <- MoveToAction type literal
0x000e6dcd    call 0x100ea480                        <- SOLE exit; no direct install, no [ctrl+0x84] write
0x000ea480  ?HandleAction@ControllerBaseCharacter@
0x000ea4c2 / 0x000ea4d2  call 0x100ea4e0             <- BOTH branches converge on LocalHandleAction
0x000ea4e0  ?LocalHandleAction@ControllerBaseCharacter@
0x000ea537    call dword ptr [eax + 0x68]            <- eax = [esi] = the CONTROLLER's vtable
0x000ea53a    cmp eax, 4 … 0xea54b test eax,eax …    <- the permission switch
0x000ea5d9 / 0x000ea5f2  call 0x100724f0             <- CharacterActionHandler::Execute
```

**`0x000ea537` dominates both `Execute` call sites.** No edge in `LocalHandleAction` reaches an install without first evaluating the permission. Permission `1` parks the action at `[controller+0x88]` and returns *without* `Execute`; permission `2` destroys it.

## § 3 — The vtable slot, enumerated not spot-checked

Image-wide `.rdata` sweep for `0xea260` (evidence `16`): **26 slots, 14 at displacement `+0x68`** of a controller primary vtable — `ControllerBaseCharacter` · `ControllerCharacter` · `ControllerCombat` · `ControllerStooge` · **`ControllerAI`** · **`ControllerMonster`** · `ControllerMonsterSynergy` · `ControllerPet` · `ControllerAlly` · `ControllerNpc2` · `ControllerOrmenos` · `ControllerHades` · `ControllerGraeae` · `ControllerCerberus`.

**`?CheckAction@` has exactly one override image-wide** — `?CheckAction@ControllerPlayer@` (`0x11b430`), at `+0x68` of `??_7ControllerPlayer@` and **nothing else** (evidence `01`, `16`). Nothing on the AI/monster branch overrides it. `0xea260` has **zero direct-call xrefs** (evidence `02`): it is reached *only* by virtual dispatch, which is why the slot enumeration is the whole story.

> **Methodological, published:** the sweep's remaining 12 hits sit at `+0x74`/`+0x198`/`+0x254`/`+0x2ac`/`+0x3f8`/`+0x688`/`+0x984`/`+0xb1c` of the *nearest preceding exported* `??_7` symbol. These are **over-collection** — unexported vtables following an exported one — and are **left in the artifact unfiltered** so the over-collection is visible, per the prior lap's standing practice on evidence `86`.

## § 4 — ⚑ THE FINDING UNDER THE FINDING: the matrix limb is Player-only

`CheckAction` opens:

```
0x000ea273  call [newAction_vtbl + 0x2c]   ; edi := newAction->GetType()   ([action+8])
0x000ea276  push [esi + 0x24]              ; the CONTROLLED entity's id
0x000ea27b  call [0x104e504c]              ; -> the entity registry
0x000ea283  call 0x1000b260                ; registry->Get<Player>(id)
0x000ea288  mov esi, eax
0x000ea28c  je  0x100ea347                 ; NULL  =>  the non-Player limb
```

**`0x1000b260` is `Get<Player>`, `0x1000b150` is `Get<Character>`** — the same template body instantiated with different `RTTI_ClassInfo*` (evidence `06`, `07`): `0xb260` compares against `0x107ff5a0` = `?classInfo@Player@GAME@@1VRTTI_ClassInfo@2@B`; `0xb150` against `0x107ff618` = `?classInfo@Character@GAME@@1VRTTI_ClassInfo@2@B`.

**Independent identity witness (evidence `12`):** `?GetLocalPlayer@AreaTrigger@GAME@@IBEPAVPlayer@2@XZ` — *whose mangled return type is `Player*`* — is a 0x2e-byte function whose entire body is `registry = [0x104e504c](); return Get<Player>(localPlayerId)`. The identification does not rest on the RTTI constant alone.

**Base chains from the shipped class graph (evidence `12`):** `Monster → Character` and `Player → Character`. **`Player` and `Monster` are siblings.** Therefore `Get<Player>(monsterEntityId)` is `NULL`, and `0xea28c` is *always* taken for a monster.

### § 4.1 — CFG dominance proof (evidence `13`, script `s6`)

Built the intra-procedural CFG from decoded branch edges, cut the fallthrough of `0xea28c`, recomputed reachability:

| | instructions reachable | matrix `0xea310` reachable |
|---|---:|---|
| no assumption | 130 / 130 | **True** |
| controlled entity is not a `Player` | **71 / 130** | **False** |

The 59 excluded instructions are exactly `0xea292`–`0xea344`: the current-action-active test, the `type==8` escape, the `[esi+0x760]` predicate, **the matrix load, and the `DEFER` handler**. The script HALTs on any indirect branch it cannot model — it did so once (`0xea2da`, a comment-annotated operand) and was fixed rather than loosened.

### § 4.2 — What the monster limb actually returns (evidence `10`, `14`, `15`; script `s7`)

The limb re-resolves the entity as `Character` and switches on virtual `+0x21c` = `?GetLifeState@Character@` (`0x46e70`, `mov eax,[ecx+0x1b98]; ret`; **not overridden by `Monster`**). `Character_LifeState` decoded **by shipped name** from `GetLifeStateAsText`'s 6-entry jump table, read byte-exactly rather than assumed sequential: `0 Unknown · 1 Initializing · 2 Alive · 3 Dying · 4 Dead · 5 Respawning` (default `"Life: Illegal"`).

| lifeState | new action | permission | producing RVA |
|---|---|---|---|
| Unknown / Initializing / **Alive** / Respawning | **anything except `15 Die`** | **`0 REPLACE`** | `0xea378` |
| Unknown / Initializing / Alive / Respawning | `15 Die` | `0 REPLACE`, or `2 REJECT` over an existing `Die` | `0xea397` |
| `3 Dying` | `15 Die` only | `0 REPLACE` | `0xea397` |
| `3 Dying` | anything else | `2 REJECT` | `0xea3b5` |
| `4 Dead` | `20 Respawn` only | `0 REPLACE` | `0xea378` |
| `4 Dead` | anything else | `2 REJECT` | `0xea373` |

**The two cells this lap was commissioned on, across every non-terminal lifeState:**
- pursue `MoveTo(4)` over `SpawnAction(19)` → **`0 REPLACE`**
- alert `PlayAnimationAction(18)` over `MoveTo(4)` → **`0 REPLACE`**

**Invariant over all four non-terminal lifeStates**, so the verdict does not depend on resolving whether a Crucible body is `Initializing` or `Alive` at `run_tick 1`. `Dying`/`Dead` are excluded **by the measurement itself**: both `REJECT` the pursue `MoveTo`, and the closures fired and the bodies pursued.

## § 5 — Consequence for the run (reported-not-graded, R-L56-2)

1. **`MD-B4app-8` closes: the PENDING limb is ZERO.** `permission[4][19] = 1 PENDING` is a real shipped cell — and it is **never read for a monster**. The two-hop composition is `REPLACE ∘ REPLACE`.
2. **`C-B4app-10` dissolves.** With no non-REPLACE outcome available there is no attribution split to make.
3. **The `PAIR` is no longer the honest answer; the single limb is.** Both branches of the fork land on the same number by different routes.
4. **RESID-D1-2 § 0 is UNAFFECTED and strengthened.** That verdict rested on mechanism 1 — the ActionState gate plus `MoveToAction::Finish` → `NavManager::StopObject` — which lives on the REPLACE path. REPLACE is now the *only* monster outcome, so the halt is unconditional rather than cell-contingent.
5. **D-1 § 3.3 is RESTORED for monsters.** The prior lap narrowed "alert `.anm` length = hold duration" to the REPLACE row. For monsters there is no other row. The narrowing was correct on the bytes it had; it is now superseded by a stronger result.
6. **Nothing touches alert incidence.** D-1 § 2.5's populations and B-5's 260 `L2_chance_roll` closures are untouched.

## § 6 — Corrections to RESID-D1-2 (my own prior lap)

- **§ 4.2 / § 5 CORRECTED.** The 26×26 matrix reconstruction (evidence `71`/`72`) is *byte-correct and stands* — but the claim that it governs the monster's alert displacement does not. It governs the **`ControllerPlayer`** path (`0x11b430`, which reads the same `gGameEngine+0x2802c` with the same `imul …,0x1a` stride) and the base class's Player limb. The prior lap read the matrix index correctly and did not decode the `0xea28c` type gate eleven instructions above it.
- **§ 5's three-regime table is PLAYER-ONLY.** `1 PENDING` over `9 Stun … 14 Trap` and `2 REJECT` over `19 Spawn` describe player behaviour. No monster reaches them.
- **§ 9 DO-NOT #2 SUPERSEDED**, replaced by § 8(2).
- All other prior DO-NOTs stand. **Nothing was cited to `?CanMove@ControllerAI@`** (§ 9 #4 honoured); the ICF-fold hazard bit again in this lap's vtable dump, where `CharacterActionBase` slots `+0x18`/`+0x28`/`+0x2c` resolve to folded one-line getters bearing unrelated names — cited **by body** (`mov eax,[ecx+8]; ret` = the type field, corroborated against the `[action+8] := 4` store) and never by folded name.

## § 7 — Residuals (named, with break points)

- **`RESID-B4app-9a`** — *why* the base carries a Player limb when `ControllerPlayer` overrides the slot. Most likely a non-`ControllerPlayer` controller that can drive a `Player`; **`ControllerStooge` sits at `+0x68 → 0xea260`**, which fits. **INFERENCE, not decoded.** Not load-bearing: it is the limb monsters do not take.
- **`RESID-B4app-9b`** — the Player-limb predicate `[controller+0x760]` → `[+0x2d4]` (`0xea2de`–`0xea304`), which can return `0 REPLACE` *before* the matrix. Undecoded, player-only.
- **`RESID-B4app-9c`** — `[controller+0x88]`, the PENDING slot, is written only at `0xea615` (the `permission==1` branch), unreachable for monsters; its pump is `?CharacterHandlerUpdate@ControllerBaseCharacter@+0x175` (`0xea245`). **Other writers of `+0x88` were not censused** — "a monster's pending slot is never populated" is asserted for *this route only*.
- **`RESID-B4app-9d`** — `ControllerStationaryMonster` has no exported controller vtable, so it is absent from the `+0x68` enumeration. Not load-bearing (KC2 bodies pursue), named so the enumeration's edge is visible rather than implied.
- **`RESID-B4app-9e`** — the three `Pursue::OnBegin` `MoveTo` sites are three *arms of a branch*, not three sequential issues; which arm runs (distinguished by the `[state+0x1c]` flag written `0`/`1` after arms 1 and 2) was **not** decoded. Immaterial — all three converge on the same terminal function and therefore the same permission.

## § 8 — ⚑ DO-NOT block (binding on B-4app, B-5, B-6 and the baton)

1. **DO NOT** model any monster's action admission with the 26×26 matrix. It is **unreachable** for a non-`Player`-controlled body. Use the `lifeState × actionType` table in § 4.2.
2. **SUPERSEDES RESID-D1-2 § 9 #2.** The "ten of twenty-six types give `1` or `2`" caveat is **player-only**. For monsters there is exactly one non-REPLACE outcome outside the terminal rows: a `DieAction` over an existing `DieAction`.
3. **DO NOT** treat `CheckAction` as "the matrix function". It is a **two-limb** function and the limb is chosen by an RTTI downcast at `0xea283`, eleven instructions before the branch that looks like the decision.
4. **DO NOT** read `0x1000b150` and `0x1000b260` as the same helper. Same template, different `RTTI_ClassInfo*`; confusing them inverts this entire verdict.
5. **DO NOT** cite `?CanMove@ControllerAI@` (carried), and **do not cite any `CharacterActionBase` vtable slot by its resolved export name** — `+0x18`/`+0x28`/`+0x2c` are ICF-folded getters wearing unrelated names.
6. All other prior DO-NOT blocks carried unchanged (D-1 § 6, RESID-D1-2 § 9 #1/#3/#5/#6, AA § 6, AB § 5.4, V/V-2/W/X/Y/Z/D-11/D-12).

## § 9 — Evidence index

`01` CheckAction/HandleAction symbol census + controller `+0x68` sweep · `02` install-path xrefs (the six `Execute` callers) · `03` `CharacterActionBase` vtable slots · `04` `ControllerPlayer::CheckAction` · `05`/`07` the two downcast helpers · `06` `RTTI_ClassInfo` identification · `08`/`09`/`10` `Character_LifeState` by shipped name · `11` `Get<Player>` caller census · `12` RTTI base chains + identity witness · **`13` the CFG dominance proof** · `14`/`15` the derived monster permission table · `16` exhaustive `.rdata` slot sweep + assembled call path.

Load-bearing: **`13`** (matrix unreachable) · **`12`** (`Player`/`Monster` are siblings) · **`16`** (slot `+0x68`, never overridden on the AI branch) · **`02`** (no direct-install path) · `15` (the constant `REPLACE`).

---

**Two notes for the conductor.** First, the commission's framing — "either answer is a clean close" — held, but not in the shape it anticipated: the boolean and the consequence came apart, and I have kept them apart rather than collapsing them into whichever label reads more cleanly. Second, this lap **corrects my own prior lap**, and the correction is the more consequential half of the return: the matrix I reconstructed byte-exactly at RESID-D1-2 is real, is shipped, and is read — by players. It was never the monsters' gate.

---

*legolas (UNKNOWN-RESEARCHER), 2026-08-25. Read-only on all substrate. Commit `fcf07687`. No pushes.*
