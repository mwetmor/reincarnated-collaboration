# KC2-MC · Lap D-8 — Freeze / Petrify on a PLAYER: routing, suppression, exit, and the LATCH (`MD-B2app-1`)

**Agent:** legolas (UNKNOWN-RESEARCHER) · **Date:** 2026-08-24 · **Conductor:** gandalf (RUN-CONDUCTOR), ledger `L-42`
**Commission:** `MD-B2app-1` verbatim, fired by the B-2app DRIFT-CRITIC verdict § F-1
(`agentic_orchestration/gandalf/notes/2026-08-24-kc2-mc-b2app-drift-critic-verdict.md`).
**Substrate (pinned, read-only):**
* `/Users/admin/Games/vendor/grim-dawn/Game.dll` — sha256 `4876d6bdb69cca71cfa987652cbd7a42cf6d5578564d02d09aaf9b55c078ab02`, 25,091 decorated exports
* `/Users/admin/Games/vendor/grim-dawn/database/database.arz` + `gdx2/database/GDX2.arz` — `database.arz` sha256 `8cdeff128422c765278087b7e4f95a41b59be8ee51184370d139c451afb5ae3f` (byte-identical to the `grim-dawn-edition-II-20260724` copy the earlier laps used — verified, not assumed)

**Method:** the D-4b/D-7 harness (`d4b_pe.py` + `d4b_dis.py`, `d7_step13_slots.py`, `d7_step9_xref.py`) plus one
new helper, `d8_lib.bounded()`, which stops a listing at the next exported RVA. *(The D-7 harness has no
function bounds; several of its listings ran into the neighbouring body. That did not affect D-7's
conclusions, but it will bite whoever re-runs `d7_step30`. Recorded as an errata, not a finding.)*
**Display-layer guard honoured:** no tooltip and no `tags_ui.txt` join. The two `.arz` records read here are
FX-handler records and a skill record; every gameplay rule below is read off an instruction body.

---

## § 0 · VERDICT TABLE

| target | verdict | one-line rule |
|---|---|---|
| **1 · where do `BeginFreeze` / `BeginPetrify` route?** | **DECODED — TWO LIMBS** | limb A = a **pure-presentation** `SpecialCharHandler`; limb B = controller vtable `+0xb0` = **`BeginImmobilize@ControllerPlayer`** ⇒ the **`Immobilized`** player state |
| **2 · the suppression columns** | **DECODED — `STUN_PROXY` VINDICATED** | the `Immobilized` and `Stunned` vtables differ in **6 of 83** slots and in **0 of 16** request/select slots. Freeze/Petrify suppress *exactly* what Stun suppresses |
| **2b · anything enforced below the controller?** | **DECODED — YES, and it is the one real asymmetry** | `ExecuteImmobilize@Character` sets the movement-lock byte `Character+0x1cb7`; **`ExecuteStun` does not** |
| **3 · exit semantics** | **DECODED — bucket-list expiry ONLY** | `StopInvoluntaryEffect` routes `0x2d→EndFreeze`, `0x2e→EndPetrify`; each has exactly one call site, and the whole lane has **one** caller: `UpdateFxAndInfluence`. No break-on-damage, no break-on-input, no cleanse. `OnUpdate@Immobilized` is a `ret 4` stub — **not even the self-timer Stun has** |
| **4 · THE LATCH** | **DECODED — THE FIGHT LATCHES** | Petrify on a channelling player → `SetState("Immobilized")` → `ImmobilizeAction::Execute` → `SkillManager::StopCurrentSkill` → `StopSpinning` → the EoR spin flag `Skill+0x4f4` clears → `CollectPassiveDefenseAttributes` **early-returns** → `defensiveCrowdControl +25` **DROPS**. Channel-conditionality is now **decoded, not assumed** |
| **5 · clean negatives** | **6 recorded** | § 6 |

**Machine-readable products**
* `evidence/d8_family_request_matrix.csv` — **112 rows** = 7 families × 16 request/select slots × verdict, each row carrying the family's `CombatAttributeType`, the `Character::Begin*` RVA, the controller slot, the player-state class + vftable RVA, the slot occupant RVA + symbol, and Idle's occupant RVA. **This is the CSV the commission asked for.**
* `evidence/d8_routing_and_lifecycle.csv` — **42 rows**, every decoded routing/lifecycle/negative rule with its RVA and containing function. Every non-`n/a` RVA was re-resolved against the export table before shipping (0 unmapped).

---

## § 1 · TARGET 1 — WHERE THEY ROUTE

`Character::BeginFreeze` (`0x0005b020`) and `Character::BeginPetrify` (`0x0005b150`) are the **same function
with two record names and two cache slots.** Both do exactly two things.

```
Character::BeginFreeze                                     0x0005b020
  ; ---- limb B (gameplay) ----
  ctrl = ObjectManager::Get(this[+0x1120])                 ; RTTI-checked -> ControllerCombat*
  if (ctrl) ctrl->vtable[+0xb0]()                          ; 0x0005b05a
                                                           ;   = BeginImmobilize@ControllerPlayer 0x000f6a10
  ; ---- limb A (presentation) ----
  if (this[+0x2e84] == 0)                                  ; cached handler
      this[+0x2e84] = SpecialCharHandler::CreateHandler(
          this, db["records/fx/damagedefault/dmgspecial_freeze_handler.dbr"])   ; 0x0005b0a0
  this[+0x2e84]->vtable[+8]()                              ; Enable@SpecialCharHandler_IcyCharacter

Character::BeginPetrify                                    0x0005b150   ; identical, except
  ctrl->vtable[+0xb0]()                                    ; 0x0005b18a  -- THE SAME SLOT
  cache slot  this[+0x2e88]
  record      "records/fx/damagedefault/dmgspecial_petrify_handler.dbr"
```

### 1.1 Limb B — the state is `Immobilized`, not a new one

`ControllerPlayer` vtable, resolved slot by slot (`evidence/step4_ctrlplayer_slots.txt`):

| offset | occupant | reached from |
|---|---|---|
| `+0x090` / `+0x094` | `Begin/EndStun@ControllerPlayer` | `Start/StopInvoluntaryEffect(0x2a)` |
| `+0x0a8` / `+0x0ac` | `Begin/EndSleep` | `…(0x2b)` |
| `+0x0b8` / `+0x0bc` | `Begin/EndTrap` | `Character::Begin/EndTrap` (`0x2c`) |
| **`+0x0b0` / `+0x0b4`** | **`Begin/EndImmobilize`** | **`Character::Begin/EndFreeze` (`0x2d`)**, **`Character::Begin/EndPetrify` (`0x2e`)**, and `Character::Begin/EndImmobilize` (`0x2f`) |
| `+0x0c0` / `+0x0c4` | `Begin/EndKnockdown` | `…(0x30)` |

`BeginImmobilize@ControllerPlayer` (`0x000f6a10`) is the standard forwarder — *current state if one is set,
else the default state* — tail-jumping to the state's vtable slot **40 (`+0xa0`)**:

```
0x000f6a10  cmp [ecx+0x214], 0 ; je +0x16          ; is a state active?
0x000f6a19  eax = *(this[+0x210]);  ecx = eax[8]   ;   -> the current ControllerPlayerState
0x000f6a26  ecx = this[+0x1e4]                     ;   -> the default state
0x000f6a2e  jmp [eax+0xa0]                         ; slot 40 = Begin*Immobilize* on that state
```

**⚑ The channel state does not intercept it.** `ControllerPlayerStateUseSkill`'s slot 40 **is byte-identical
to Idle's** (`0x0011ff90`, `BeginImmobilize@ControllerPlayerStateIdle`), which tail-jumps to
`DefaultBeginImmobilizeAction` (`0x0011f480`) → `SetState("Immobilized")` with a **zeroed**
`ControllerAIStateData` (`0x0011f4c9`–`0x0011f4d7`; the literal is at VA `0x1052ff18`, length `0xb`,
verified as `'Immobilized'`). Same for `ChargeToUseSkill`, `MoveAndUseSkill`, `MoveToUseSkill` and `MoveTo`.

`ControllerPlayerStateImmobilized` (`0x005c081c`) exists; **`ControllerPlayerStateFrozen` and
`…Petrified` do not** (§ 6 N-1).

### 1.2 Limb A — the `SpecialCharHandler` is presentation, and Petrify is Freeze with different art

`CreateHandler@SpecialCharHandler` (`0x00462250`) reads the record's `handlerType` field and dispatches on
three string literals — `"FadeAwayFromPlayer"`, `"FadeNearPlayer"`, `"Freeze"` (`0x10586c34`). The two
records both carry `handlerType = 'Freeze'`, so both construct `SpecialCharHandler_IcyCharacter`.

The records, dumped from `database.arz` — **seven fields each, and not one of them is a gameplay field:**

| field | freeze handler | petrify handler |
|---|---|---|
| `handlerType` | `Freeze` | `Freeze` |
| `templateName` | `…/specialcharhandler_freeze.tpl` | *(same)* |
| `iceCubeName` | `…/damagefreeze_icechunk01.dbr` | `…/damagepetrify_stonechunk01.dbr` |
| `icyEffectName` | `fx/textures/damagefreeze_overlay.tex` | `fx/textures/damagepetrify_overlay.tex` |
| `freezeSound` / `shatterSound` / `thawSound` | three `spak_damage_freeze_*` | `…freeze_freeze` / `…petrify_shatter` / `…petrify_unpetrify` |

The class matches the data: its whole surface is `AllowBone(GraphicsMeshInstance, Bone)`,
`StoreOverriddenTexture`, `GetOverriddenTexture`, `OnGMIEffectDestroy`, `PhysicsUpdate`. A call-target audit
of `Start@SpecialCharHandler_IcyCharacter` (`0x00462820`, `evidence/step16_handlertype.txt`) shows **zero**
calls into `Character`, `Controller*`, `CombatAttribute*` or `DurationDamageManager`. `BeginFreeze` invokes
handler vtable `+8` = `Enable@…_IcyCharacter`; `EndFreeze` invokes `+0xc` = `Disable`.

> **Consequence for the baton:** *Petrify differs from Freeze in **art and audio only.** Any Layer-1
> implementation that gives petrify a mechanical difference from freeze is inventing one.*

---

## § 2 · TARGET 2 — THE SUPPRESSION COLUMNS

Re-derived on this lap's own basis (not cited from D-7 — `K-7` dated-claim discipline). Idle-diff over the
83-slot `ControllerPlayerState` vtable, stride `0x14c`, occupant classification `PERMITTED` / `STUB-false`
(`xor al,al; ret n`) / `STUB-ret` (bare `ret n`) / `IMPL`.

| request (slot) | **Freeze** | **Petrify** | Stun | Immobilize | Trap | Sleep | Knockdown |
|---|---|---|---|---|---|---|---|
| `SelectPrimaryAction` (54) | PERMITTED | PERMITTED | PERMITTED | PERMITTED | PERMITTED | PERMITTED | PERMITTED |
| `SelectSecondaryAction` (55) | PERMITTED | PERMITTED | PERMITTED | PERMITTED | PERMITTED | PERMITTED | PERMITTED |
| `SelectJoystickAction` (56) | PERMITTED | PERMITTED | PERMITTED | PERMITTED | PERMITTED | PERMITTED | PERMITTED |
| `ActivateSuperSkill` (57) | PERMITTED | PERMITTED | PERMITTED | PERMITTED | PERMITTED | PERMITTED | PERMITTED |
| `RequestUseItem` (58) | PERMITTED | PERMITTED | PERMITTED | PERMITTED | PERMITTED | PERMITTED | PERMITTED |
| `RequestReleasePet` (59) | PERMITTED | PERMITTED | PERMITTED | PERMITTED | PERMITTED | PERMITTED | PERMITTED |
| `RequestUseItemOn` (60) | PERMITTED | PERMITTED | PERMITTED | PERMITTED | PERMITTED | PERMITTED | PERMITTED |
| `RequestItemAction` (61) | STUB-ret | STUB-ret | STUB-ret | STUB-ret | STUB-ret | STUB-ret | STUB-ret |
| `RequestInteractableAction` (62) | STUB-ret | STUB-ret | STUB-ret | STUB-ret | STUB-ret | STUB-ret | STUB-ret |
| `RequestNpcAction` (63) | STUB-ret | STUB-ret | STUB-ret | STUB-ret | STUB-ret | STUB-ret | STUB-ret |
| `RequestCompleteRelics` (64) | PERMITTED | PERMITTED | PERMITTED | PERMITTED | PERMITTED | PERMITTED | PERMITTED |
| **`RequestSkillAction` (76)** | **STUB-false** | **STUB-false** | STUB-false | STUB-false | **IMPL** | STUB-false | STUB-false |
| `RequestInstantSkillAction` (77) | PERMITTED | PERMITTED | PERMITTED | PERMITTED | PERMITTED | PERMITTED | PERMITTED |
| `RequestEvadeAction` (78) | STUB-false | STUB-false | STUB-false | STUB-false | STUB-false | STUB-false | STUB-false |
| **`RequestMoveAction` (80)** | **STUB-ret** | **STUB-ret** | STUB-ret | STUB-ret | STUB-ret | STUB-ret | STUB-ret |
| `RequestRotateAction` (81) | STUB-ret | STUB-ret | STUB-ret | STUB-ret | **PERMITTED** | STUB-ret | STUB-ret |

### 2.1 ⚑ `MD-B2app-1` — the `STUN_PROXY` grain is VINDICATED, and it was a coin-flip

The full 83-slot diff `Immobilized` ↔ `Stunned` (`evidence/step9_matrix.txt`) is **6 slots**, and **none of
them is a request:**

| slot | what | Stunned | Immobilized |
|---:|---|---|---|
| 0 | destructor | class-specific | class-specific |
| 41 | `EndImmobilize` hook | `Stop@Fx` (`ret`) | `EndImmobilize@…Immobilized` (real) |
| 45 | `EndStun` hook | `EndStun@…Stunned` (real) | `Stop@Fx` (`ret`) |
| 68 | `OnBegin` | own | own |
| 69 | `OnEnd` | own | own |
| **70** | **`OnUpdate`** | **real (`0x00123490`)** | **`ret 4` — none at all** |

`OnBegin@Stunned` (`0x001233b0`) and `OnBegin@Immobilized` (`0x00123160`) are the same body modulo two
constants: both allocate a `0x34`-byte `CharacterActionBase`, set priority `250.0f`, re-tag it
(`TakeStunAction` code `9` / `ImmobilizeAction` code `0xd`) and call
`HandleAction@ControllerBaseCharacter`. The single behavioural delta is that Stunned then caches
`GetCurrentStateData()[0]` into `this+0x10` for its `OnUpdate` self-timer — and `DefaultBeginStunAction`
passes that data **zeroed**, so on the control path even that delta is inert.

> **Verdict:** gamora's declared `STUN_PROXY` arm was **right**, at the request layer, exactly. `D-B2app-G3`
> can be retired from `DECLARED` to `decoded`, the 59/131 roster rows re-graded, and the
> `DECLARED-PROXY (MD-B2app-1)` basis struck from every Freeze/Petrify baton row.
> **This was not a foregone conclusion** — the routing is genuinely different (Character-level, not
> controller-slot; a second FX limb Stun does not have; a *different state class*), and the convergence
> happens only because `ControllerPlayerStateImmobilized` and `…Stunned` were written as siblings.

### 2.2 ⚑ …but there IS one asymmetry, and it lives below the controller

`ImmobilizeAction::Execute` tail-jumps to `Character::ExecuteImmobilize` (`0x00048830`), whose first
instruction is

```
0x00048835  mov byte ptr [esi + 0x1cb7], 1
```

`Character+0x1cb7` is the **movement-lock byte**. A byte-exact scan of `.text` for the `disp32 0x1cb7`
encoding (`evidence/step31_disp.txt`, 14 sites, all decoded) gives its complete life:

* **set by** `ExecuteImmobilize@Character` (Freeze / Petrify / Immobilize) and `ExecuteTrap@Character`
* **cleared by** `ReleaseImmobilize@Character`, `ReleaseTrap@Character`, `StartRespawn@Character`, the ctor
* **read by** `DisallowsMovement@Character` (`0x0005b3d0` — the function *is* the byte),
  `Execute@MoveToAction`, `Execute@WalkAction`, `Execute@JumpAttackAction`, `Execute@EvadeAction`,
  `CanMove@ControllerMonster`
* **`ExecuteStun@Character` (`0x000486a0`) never touches it.** Stun sets only the action-state (`8`).

So motion under Stun is refused at the *request* layer alone; motion under Freeze/Petrify/Trap/Immobilize is
refused at the request layer **and** hard-locked at the Character layer, which additionally kills a
**already-queued** `MoveTo` / `Walk` / `JumpAttack` / **`Evade`** action at its `Execute`. Narrow, real, and
a feel difference a Godot build will otherwise get wrong.

> **Baton row owed:** `movement_lock_is_two_layer` (Layer 1, `decoded`). *An evade that has already left the
> player's hand still resolves through a stun and is swallowed by a freeze or a petrify.*
> **Sim impact: none** — B-2app's suppression columns are request-level and are correct as built.

---

## § 3 · TARGET 3 — EXIT SEMANTICS

`StopInvoluntaryEffect@Character` (`0x0005adb0`) is the mirror of `Start`, a flat switch:

```
0x31 TakeHit     -> controller +0xa4  EndTakeHit
0x2b Sleep       -> controller +0xac  EndSleep
0x2a Stun        -> controller +0x94  EndStun
0x2c Trap        -> Character::EndTrap        0x0005aff0
0x2d Freeze      -> Character::EndFreeze      0x0005b110    ⚑  (0x0005ae4b)
0x2e Petrify     -> Character::EndPetrify     0x0005b240    ⚑  (0x0005ae59)
0x2f Immobilize  -> Character::EndImmobilize  0x0005b2b0
0x30 Knockdown   -> Character::EndKnockdown   0x0005b310
```

`EndFreeze` / `EndPetrify` mirror their Begins exactly: controller `+0xb4` = `EndImmobilize@ControllerPlayer`
→ current state slot 41 → `EndImmobilize@ControllerPlayerStateImmobilized` (`0x001232e0`) →
**`SetState("Idle")`** (literal at VA `0x105300b0`, length 4). Plus handler vtable `+0xc` = `Disable`.
`OnEnd@Immobilized` issues a `ReleaseImmobilizeConfigCmd`, which is what clears `Character+0x1cb7`.

**Nothing restarts the channel.** `SetState("Idle")`, not `SetState("UseSkill")`. `C-B2app-1`'s
`REACQUISITION_TICKS = 0` refusal stands, and the `RC-reacquisition` named fork (`F-5`) is still owed.

### 3.1 ⚑ The clock is the bucket list and ONLY the bucket list — proven twice

Two independent search techniques, the D-7 § 6 standard:

**(a) byte-exact `E8`/`E9 rel32` xref scan of `.text`** (`evidence/step11_xrefs.txt`):

| target | call sites |
|---|---|
| `Character::BeginFreeze` | **1** — `StartInvoluntaryEffect+0xaa` |
| `Character::EndFreeze` | **1** — `StopInvoluntaryEffect+0x9b` |
| `Character::BeginPetrify` | **1** — `StartInvoluntaryEffect+0xba` |
| `Character::EndPetrify` | **1** — `StopInvoluntaryEffect+0xa9` |
| `Character::StartInvoluntaryEffect` | **1** — `UpdateFxAndInfluence+0x14d` |
| `Character::StopInvoluntaryEffect` | **1** — `UpdateFxAndInfluence+0x144` |

**(b) image-wide 4-byte VA constant scan** (`evidence/step12_addrscan.txt`): **0 occurrences** for all six.
None of them is virtual, none is ever taken as a function pointer, none sits in any vtable.

⇒ **The entire lifetime of a frozen or petrified player is decided by
`DurationDamageManager::UpdateFxAndInfluence` re-running its ladder each update.** There is **no
break-on-damage, no break-on-input, no potion cleanse, and no skill-driven removal.** The ladder is
`0x2f > 0x2e > 0x2d > 0x2c > 0x2b > 0x2a > 0x30 > 0x31`, first `GetFixedDamage(t) > 0` wins, and on a change
of winner it calls `StopInvoluntaryEffect(old)` then `StartInvoluntaryEffect(new)` (`0x0020a104`/`0x0020a10d`).

And Freeze/Petrify are *more* purely bucket-clocked than Stun: `OnUpdate@ControllerPlayerStateImmobilized`
is the shared `ret 4` stub, so the state has no self-ending path of any kind.

The only structural clear of a fixed timeline is `ImDead@DurationDamageManager` (`0x00209e50`) — the **death**
path — which drops both lists and tail-calls `UpdateFxAndInfluence`. `RemoveAllDamages` (`0x00208f40`) exists
as `DurationDamageManager` vtable slot 6 with exactly one address occurrence image-wide (its own vtable slot)
and no caller found by either technique — residual `R-D8-1`.

---

## § 4 · TARGET 4 — ⚑ THE LATCH. IT LATCHES.

The DRIFT-CRITIC's binary (§ F-1) resolves to **arm 1: a latch fight.** Every link is an instruction.

```
 1. a Petrify lands while the player channels EoR
 2. UpdateFxAndInfluence elects 0x2e  ->  Character::StartInvoluntaryEffect(0x2e)      0x0020a10d
 3.   -> Character::BeginPetrify                                                       0x0005ad7a
 4.      -> ControllerPlayer::BeginImmobilize   (ctrl vtable +0xb0)                     0x0005b18a
 5.         -> current state is ControllerPlayerStateUseSkill, whose slot 40 IS Idle's
 6.            -> DefaultBeginImmobilizeAction  ->  SetState("Immobilized")             0x0011f4ef
 7.               THE CHANNEL STATE IS REPLACED  (OnEnd@UseSkill is the shared `ret`)
 8. OnBegin@ControllerPlayerStateImmobilized  ->  HandleAction(ImmobilizeAction)        0x0012320e
 9.   -> Execute@ImmobilizeAction   ->  SkillManager::StopCurrentSkill()                0x0006f722
10.      -> StopCurrentSkill: clears current-skill id, then skill vtable +0x24c
           (StopSkill) if IsRunning()                                                   0x0043ea3e
11.         -> StopSkill@Skill_AttackRadiusSpin  ->  vtable +0x394 = StopSpinning       0x003e8e38
12.            -> StopSpinning:  mov byte ptr [Skill + 0x4f4], 0                        0x003eba0e
13. CollectPassiveDefenseAttributes@Skill_AttackRadiusSpin:
        cmp byte ptr [this + 0x4f4], 0 ; je RETURN                                      0x003ebdc6
    ==> NOTHING is added to the CombatAttributeAccumulator.
        EoR's defensiveCrowdControl (+25) and defensiveCrowdControlMaxResist (+25) ARE GONE.
14. the next control landing resolves at r = 79 instead of r = 104.
```

**Step 7 needed care and does not work the way it looks.** `OnEnd@ControllerPlayerStateUseSkill` is the
shared `ret` stub at `0x00007f40` — **leaving the channel state does not by itself stop the skill.** The
skill is stopped by step 9, i.e. by the *action* the Immobilized state issues, not by the state transition.
Worth stating because it is the step a re-implementation will skip.

**Step 16 (the other half) — the flag is genuinely a channel flag, decoded:**

| | RVA | instruction |
|---|---|---|
| set | `0x003eb2ab` | `ActivateNow@Skill_AttackRadiusSpin` : `mov byte [edi+0x4f4], 1` |
| cleared | `0x003eba0e` | `StopSpinning@Skill_AttackRadiusSpin` : `mov byte [edi+0x4f4], 0` |
| initialised | `0x003eac53` | ctor : `mov word [esi+0x4f4], 0` |
| read | `0x003ebc19` | `IsRunning` : `return this[+0x44c] != 0 \|\| this[+0x4f4] != 0` |
| **gate** | `0x003ebdc6` | `CollectPassiveDefenseAttributes` — the early return |

The same gate guards `CollectPassiveCharAttributes`, `CollectPassiveRetaliationAttributes`,
`CollectPassiveRetaliationModifierAttributes` and `CollectPassiveRacialBonusDefense`. **Every EoR "passive"
contribution is spin-conditional, not just the CC resistance.**

### 4.1 The confound that was NOT there

`SkillManager::GetDefenseAttributes` (`0x0043ba20`) walks four skill lists and gates each entry on
vtable `+0xe4` — which resolves to **`GetCurrentLevel@Skill`**, i.e. *rank > 0*, **not** *is-active*. So the
collection layer is rank-gated and would happily contribute EoR's defence at all times. **The
channel-conditionality is entirely inside the skill class's own `+0x21c` override.** A build that models
"skill defence contributions are collected while the skill is learned" — the obvious reading of the manager
walk — gets a permanently CC-immune Warlord. This is the single most mis-implementable fact in the lap.

### 4.2 The value, from the primary source

`records/skills/playerclass09/eyeofreckoning1.dbr` (GDX2.arz), `Class = Skill_AttackRadiusSpin`:

```
defensiveCrowdControl           [10,10,10,11,11,11,12,12,12,13,13,13,14,14,14,15,16,17,18,19,20,21,22,23,24,25]
defensiveCrowdControlMaxResist  [ same 26-rank array ]
```

26 ranks — consistent with the `.arz`-vs-grimtools contradiction recorded on 2026-07-23. `eyeofreckoning2`
(`SkillSecondary_AttackProjectileOrbiting`) carries neither field.

### 4.3 What this means for the fight — stated plainly, for the baton

* **Petrify is the can-opener, and the door it opens is real.** `F-1`'s circularity is broken: the grain
  resolves to the arm under which control *does* exist on this board.
* **The positive-feedback structure B-2app implemented is the correct one**, and it is now decoded rather
  than declared: one Petrify landing at `r = 59` (×0.287) drops the player to `r = 79` for Stun/Freeze/Trap,
  where the big three land at ×0.21 instead of never.
* **The vulnerable window is at minimum the petrify's own delivered duration**, because the channel does not
  self-resume and `REACQUISITION_TICKS` is a client-input quantity the binary cannot see. Every published
  channel cost remains a **lower bound**, exactly as `C-B2app-1` said.
* **`F-6`'s latch probe is now worth building** and the semantics it must assert are the fourteen steps above.
* **Stun, Knockdown and Sleep would latch identically** — `TakeStunAction::Execute` (`0x0006f172`),
  `TakeKnockdownAction::Execute` (`0x0006f2e2`) and `TakeSleepAction::Execute` (`0x0006f5b2`) all call
  `StopCurrentSkill` from the same position. They simply never land at `r = 104/105`. *The immunity is what
  makes Petrify special; the latch mechanism is shared.*

---

## § 5 · WHAT gamora CAN NOW BUILD

1. **Retire `MD-B2app-1`.** Freeze (`0x2d`) and Petrify (`0x2e`) drive `ControllerPlayerStateImmobilized`,
   whose 16 request/select columns are byte-identical to `Stunned`'s. Re-grade the 59/131 rows from
   `DECLARED-PROXY` to `decoded`; the numbers do not move.
2. **Keep the ladder, the longest-wins rule and the concurrency law unchanged** — Freeze/Petrify were already
   in the ladder at the right priorities and nothing here touches them.
3. **`channel_conditional_resistance` is `decoded`, not `derived`.** `defensiveCrowdControl` contributes iff
   `Skill_AttackRadiusSpin+0x4f4` is set, i.e. iff the disc is spinning.
4. **Model the channel break as *caused by the action, not by the state transition*** if the sim ever
   separates the two. Today it does not need to.
5. **Do NOT give Petrify any mechanical difference from Freeze.** The delta is a stone chunk instead of an
   ice chunk and three different sound records.
6. **Add the Layer-1 row `movement_lock_is_two_layer`** (§ 2.2). No sim change.

---

## § 6 · CLEAN NEGATIVES (searched, not found — with the search recorded)

**N-1 — there is no `ControllerPlayerStateFrozen` and no `ControllerPlayerStatePetrified`.**
All 25,091 exports searched for `ControllerPlayerState(Frozen|Freeze|Petrified|Petrify|Stone)`: **zero**.
All 27 `ControllerPlayerState*` vftables are enumerated in `evidence/step3_ctrl_slots.txt`. Freeze and
Petrify share `Immobilized` with plain Immobilize (`0x2f`).

**N-2 — no break-on-damage, no break-on-input, no cleanse.** Two techniques (§ 3.1): E8/E9 rel32 xref scan
over `.text`, and an image-wide 4-byte VA constant scan. Six entry points, one call site each, all six
inside `Start/StopInvoluntaryEffect`, which themselves have one call site each inside
`UpdateFxAndInfluence`. Zero function-pointer takes anywhere in the image.

**N-3 — the freeze/petrify handler records carry no gameplay field.** Both DBRs dumped in full from the
pinned `database.arz`: 7 fields, all art/audio/template. `SpecialCharHandler_IcyCharacter`'s
`Start` body was call-target-audited: no `Character` / `Controller*` / `CombatAttribute*` /
`DurationDamageManager` target.

**N-4 — `IsFrozenOrPetrified@Character` is not on this fight's path.** It exists (`0x0005b3a0`) and reads
the **FX handler's** enabled byte (`handler+0x20`) at `Character+0x2e84` / `+0x2e88`. Byte-exact xref scan:
**exactly one caller — `Update@Skill_Shapeshift` (`0x0041acdc`)**. Not in the KC2 player kit and not in the
roster. Recorded because the name invites a wrong assumption: *the engine's own "am I frozen?" predicate is
a query against the visual effect, not against the control state.*

**N-5 — `Skill_AttackRadiusSpin::Update` does not stop the channel on control.** Its one early stop is
`if (!character->IsAlive()) StopSkill(...)` — `Character` vtable `+0x22c` resolves to `IsAlive`
(`evidence/step25_char22c.txt`), not to any is-controlled predicate. The channel break comes from
`ImmobilizeAction::Execute`, § 4 step 9. Recorded because `Update` is where one would look first.

**N-6 — `RemoveAllDamages@DurationDamageManager` has no reachable caller.** Vtable slot 6 (`+0x018`) of
`??_7DurationDamageManager`; exactly one 4-byte VA occurrence image-wide (that slot); zero E8/E9 xrefs. The
honest statement is *"no direct call site exists and no non-vtable reference exists; an indirect
`call [reg+0x18]` was not exhaustively swept, so the technique is the limit."* Residual `R-D8-1`.

---

## § 7 · RESIDUALS

| id | residual | why it does not block the B-2app fold |
|---|---|---|
| **`R-D8-1`** | `RemoveAllDamages` (`0x00208f40`) is a virtual with no found caller. If something does call it, it is a full CC cleanse followed by an immediate ladder re-election | the death path (`ImDead`) is decoded and sufficient; nothing in the KC2 roster or player kit is a cleanse candidate |
| **`R-D8-2`** | `ControllerPet` and `ControllerMonster` carry the **same** `+0xb0` forwarder body as `ControllerPlayer` (`evidence/step12_addrscan.txt`, 19 vtable placements). Whether a *pet* reaches `ControllerPlayerStateImmobilized` or a monster state was not decoded | B-3's question, not B-2app's. Feeds gandalf's `K-2` directly: **the player-side columns must not be inherited by a pet** |
| **`R-D8-3`** | `Skill+0x44c` (the other half of `IsRunning`: `0`/`1`/`2` = idle / warm-up / running) governs EoR's warm-up. Whether a control landing *during warm-up* also clears `+0x4f4` was not chased | `ActivateNow` sets `+0x4f4`, and `StopCurrentSkill` fires regardless of phase, so the latch holds either way; only the *width* of the earliest window could move |
| **`R-D8-4`** | `ControllerPlayerStateUseSkill` slot 59 `RequestReleasePet` is `PERMITTED`, but this lap did not decode whether *executing* a pet release breaks the channel | gandalf's `K-11` verbatim. Partial answer delivered: the **request** is permitted while channelling; the **consequence** is undecided |

---

## § 8 · ERRATA CARRIED

1. **D-7 § 8 item 5** ("Suppression: … for Stun/Freeze/Petrify/Sleep/Knockdown/Immobilize") over-stated D-7's
   own § 3.3, which covered five states and not Freeze/Petrify. **That over-statement is now true** — but it
   became true by decode on this lap, not by D-7's evidence. The § 8 correction already routed at `L-41`
   should be folded as *"true, established D-8"* rather than struck.
2. **D-7 § 2.4** described `defensiveCrowdControl` as "channel-conditional on EoR" without decoding it.
   Now decoded (§ 4). Same conclusion, real basis.
3. **Harness errata:** `d4b_dis.disasm(..., stop_at_ret=False)` has no function bound and will run into the
   next body. `d8_lib.bounded()` fixes it. D-7's `d7_step30_statediff.py` `body()` previews are affected
   (cosmetic only — the slot diff itself reads vtable words, not code).

---

## § 9 · REPRODUCTION

All scripts read-only against the two pinned files; all output under `evidence/`.

| script | what it establishes |
|---|---|
| `d8_step1_begins.py` | full disassembly of `Begin{Freeze,Petrify,Trap,Immobilize,Knockdown}@Character` |
| `d8_step2_strings.py` | the two DBR record paths + the `Singleton<ObjectManager>::Get` IAT resolution |
| `d8_step8_slotnames.py` | names all 83 `ControllerPlayerState` vtable slots from the BASE occupant |
| `d8_step9_matrix.py` | the request matrix over 13 states + the full `Immobilized ↔ Stunned` diff |
| `d8_lib.py` | `bounded()` — function-bounded disassembly |
| `d8_step12_addrscan.py` | image-wide 4-byte VA scan (search technique b) |
| `d8_step21_flag.py` | the `Skill+0x4f4` spin-flag census |
| `d8_step31_disp.py` | the `disp32 0x1cb7` movement-lock census |
| `d8_step40_emit.py` | both CSVs |
| `d7_step9_xref.py`, `d7_step13_slots.py` | inherited from D-7, unmodified |

**Outputs consumable by gamora**
* `evidence/d8_family_request_matrix.csv` — 112 rows, family × request-slot × verdict × RVA
* `evidence/d8_routing_and_lifecycle.csv` — 42 RVA-pinned rules and negatives
* `evidence/step1..step31*.txt` — 20 raw transcripts
