# KC2 MODEL-COMPLETION RUN · Wave 1 · **D-1 — THE ALERT DECODE**

**Seat:** legolas (`UNKNOWN-RESEARCHER`) · **Date:** 2026-08-24 · **Run:** KC2-MC, Wave 1, piece D-1
**Conductor:** gandalf (`RUN-CONDUCTOR`) — charter `agentic_orchestration/gandalf/notes/2026-08-24-kc2-model-completion-run-charter.md`
**Ruling note:** `…/2026-08-24-kc2-model-pack-reframe-and-gap-rulings.md` — facet **(b) BOTH** (in-sim **and** baton)
**Commission:** two undecoded halves — **(1) entry condition** (`ShouldPlayRallyOrAlert`, prior tag `UNREACHED-U3`) · **(2) duration** (prior tags `U-U-2` / `UNREACHED-AA-3` / `UNREACHED-AB-2`)
**Instrument:** `agentic_orchestration/research/scripts/mcd1_alert_decode_2026_08_24.py` — regenerates every claim below; nothing here is retyped from prose.
**Law 3 honoured:** every number is an operand read out of shipped bytes or a shipped record. No fitted constants. No invented rules.

## 0 · Verdicts (the two lines the conductor needs)

> **HALF 1 — ENTRY CONDITION: `DECODED`.** The gate is a **six-limb conjunction** inside `ControllerMonsterState::DefaultEnemyFoundResponse` (`Game.dll` RVA `0x10a360`). **`ShouldPlayRallyOrAlert` is NOT the state's entry predicate** — it is a once-per-monster-lifetime latch on the alert/rally **sound**. `UNREACHED-U3` closes, and closes *differently from how the run assumed it would*.
>
> **HALF 2 — DURATION: `DECODED`.** The state ends on the **`"End"` animation event**, which the engine **synthesises** when the play-head crosses the last frame of the alert animation. Duration = **the alert `.anm`'s own length**, `(frames − 1) / frameRate` seconds, per monster; the pop lands on the **next controller `Update` tick** after the crossing. `U-U-2` / `UNREACHED-AA-3` / `UNREACHED-AB-2` all close.

## 1 · Substrate + pins

| artifact | sha256 |
|---|---|
| `/Users/admin/Games/vendor/grim-dawn/Game.dll` | `4876d6bdb69cca71cfa987652cbd7a42cf6d5578564d02d09aaf9b55c078ab02` |
| `/Users/admin/Games/vendor/grim-dawn/Engine.dll` | `7141b51ae61b396fd0743da9e51471043329c51b3bb61d0037b2ce934864c87c` |
| Lap AB `pm4ab_alert_anim.csv` (imported **by identity**, § 3.3) | `65706232f07e8366459f20e9c3873527ac4c837f7896b80a3e87eebb56fe3aa5` |

Both modules are PE32 `coff-i386`, image base `0x10000000`, with full MSVC-decorated export tables (Lap J's method, `pm4s_pe_2026_08_14.PE32`, imported unchanged). **All RVAs below; VA = RVA + `0x10000000`.** The instrument HALTs on any digest mismatch. Read-only throughout; the vendor tree was never written.

---

## 2 · HALF 1 — THE ENTRY CONDITION

### 2.1 ⚑ THE HEADLINE: the commission's named predicate is not the predicate

`?ShouldPlayRallyOrAlert@ControllerMonster@GAME@@QAE_NXZ` — RVA `0xf9ce0`, evidence `01-ShouldPlayRallyOrAlert.asm`:

```
100f9ce0: cmp  byte ptr [ecx + 0x28c], 0x0
100f9ce7: je   +0x13                      ; -> return false
100f9ce9: mov  byte ptr [ecx + 0x28c], 0x0
100f9cf0: mov  al, 0x1                    ; -> return true, and CONSUME the flag
100f9cf2: ret
100f9cf3: xor  al, al
100f9cf5: ret
```

It is a **one-shot latch**, nothing more. The instrument enumerates **every** `.text` access to `ControllerMonster+0x28c` (not the first — `D-Z-1` discipline), and there are exactly four semantic sites:

| site | instruction | meaning |
|---|---|---|
| `??0ControllerMonster()` `+0x52` | `mov byte [ebx+0x28c], 1` | armed **once, at controller construction** |
| copy-ctor `+0x54/+0x5b` | `movzx` / `mov` | propagated on copy |
| `ShouldPlayRallyOrAlert +0x9` | `mov byte [ecx+0x28c], 0` | consumed |
| `DefaultEnemyFoundResponse +0x421` | `mov byte [eax+0x28c], 0` | **the only consumer — inlined**; zero out-of-line callers exist (`calls_to` returns `[]`) |

And what that single consumer guards is the **sound**, not the state (evidence `03-…-tail.asm`):

```
1010a75d: mov  esi, [eax + 0x3240]        ; Monster::GetAlertSoundChance
1010a763: call rand
1010a769: cdq ; mov ecx,100 ; idiv ecx
1010a771: cmp  edx, esi
1010a773: jae  +0x443                     ; rand()%100 >= alertSoundChance -> no sound
1010a778: cmp  byte [eax + 0x28c], 0
1010a77f: je   +0x443                     ; latch already spent -> no sound
1010a781: mov  byte [eax + 0x28c], 0      ; <- ShouldPlayRallyOrAlert, inlined
1010a788: ... Character::PlayNetSound(GetAlertSound())
```

**And the alert-state branch `jmp`s straight to `0x1010a788` (`+0x428`)** — *past* both the chance roll and the latch. So a body that enters `AlertBeforePursue` plays its alert sound **unconditionally**, while a body that does *not* enter the state may still play the sound at `alertSoundChance` %, once per lifetime. Two different gates on two different things; the run had them fused.

> **⚑ The prior-lap tag `UNREACHED-U3` named the wrong function.** Closing it required decoding `DefaultEnemyFoundResponse`, not `ShouldPlayRallyOrAlert`. Published as a correction, not smoothed over.

### 2.2 The actual gate — six limbs, in evaluation order (plus the `SetState` that precedes them)

`?DefaultEnemyFoundResponse@?$ControllerMonsterState@VControllerMonster@GAME@@VMonster@2@@GAME@@IAEXI@Z`, RVA `0x10a360`. Evidence `02-DefaultEnemyFoundResponse-gate.asm`. Offsets are `+` from function start.

| # | offset | limb (decoded) | operand + provenance |
|---|---|---|---|
| **0** | `+0x9a` | `SetState("Pursue")` fires **first** — the alert is stacked *on top of* an already-set Pursue | literal `0x1052d5d4` = `"Pursue"` |
| **1** | `+0x24d` | `IsInState("Pursue")` must be **true** | literal `0x1052d5dc` = `"Pursue"`; `je +0x443` (skip everything, sound included) |
| **2** | `+0x28f` | `rand()%100 < Monster[+0x3244]` — **the alert-chance roll** | `Monster+0x3244` bound by `?GetAlertAnimChance@Monster@` (`0x2d4ba0`) and written by `?Load@Monster@ +0x55b` from the `.dbr` field literal `0x10560e70` = **`alertAnimChance`** |
| **3** | `+0x2c6` | the **Alert animation slot must be non-empty** | gate reads `AnimationSet+0x90`; slot index `(0x90−0xc)/4` = **`0x21`** = the Alert slot; calls slot `vtable+0x3c`, the same virtual `AnimationSet::DoesAnimationExist` (`0x15d60`) wraps with `sete` ⇒ `vf3c == IsEmpty()`. `jne` on empty ⇒ **skip** |
| **4** | `+0x2e3` | the acquired enemy must still resolve to a live `Character*` | `je +0x3e4` on null |
| **5** | `+0x35f` | `dist(self, enemy) > GameEngine[+0xc80]` | `alertDistance = 6.0` from `records/game/gameengine.dbr` (Lap AA § 5.2, unchanged; single writer `GameEngine::LoadFromDatabase +0x186`, single reader this gate) |
| **6** | `+0x385` | `AngerManager::GetAngerDiff(enemyId) < 15.0f` | threshold literal `0x105f58ac` = `15.0`; arithmetic decoded in § 2.4 |
| **⇒** | `+0x38b` | `ControllerAI::AddTemporaryState("AlertBeforePursue", stateData)` | literal `0x1052d5fc`; **`D-Z-1` guard run**: the string has **two** standalone `.rdata` copies — `0x1052c33c` (referenced only from `RegisterTemporaryStates +0x130`) and `0x1052d5fc` (referenced only from this site). Exactly one entry point exists. |

### 2.3 Which states can reach the gate (the reachability set, enumerated)

`EnemyFound` is virtual per state. The instrument enumerates all sixteen `ControllerMonsterState*::EnemyFound` overrides:

| target | states |
|---|---|
| **→ `DefaultEnemyFoundResponse`** (can alert) | **Idle · Patrol · Roam · Wander · WaitToAttack · FollowLeader · DefendLeader** (all ICF-folded to `0xfecd0`, a bare `jmp`) · **QuestMove** (`0x1099b0`, tail-`jmp` at `+0x10`) |
| own implementation — re-targets, **never alerts** | Pursue · Attack · RepositionForAttack · Trapped |
| ICF-folded no-op (`0x84d0`) | Move · JumpAttack · DodgeAttack · Return |

**Consequence for KC2:** Crucible bodies are given `PatrolPoint_Attack` at placement (Lap AA § 5.1) ⇒ they sit in **Patrol** at acquisition ⇒ they *are* in the reachable set. But once in Pursue/Attack, **re-acquisition can never re-fire the alert** — the alert is at most once per engagement onset, structurally, independent of any latch.

### 2.4 The anger limb — `NAMED-AA-1` closes

`?GetAngerDiff@AngerManager@GAME@@QBEMI@Z` (`0xf360`, evidence `05`):

```
lookup enemyId in the map at AngerManager+0x4
if (not found)  ->  fldz            ; **returns 0.0f**
else            ->  fld [node+0x14] ; anger
                    fsub [node+0x18] ; baseline
```

The baseline is snapshotted inside `?Update@AngerManager@` at RVA `0xf486` (evidence `06`): `movss [esi+0x18], xmm0` where `xmm0` was just loaded from `[esi+0x14]` — i.e. **per record, per anger-update tick, `baseline := anger`**. So

> **`GetAngerDiff(e)` = the anger accrued against `e` since the last `AngerManager::Update` tick.** The limb `15.0 > diff` means *"this body has not just taken a ≥15-point anger spike this tick."*

Two consequences with known sign, both decoded:
1. **A monster that has no anger record for the player returns `0.0f` ⇒ the limb PASSES.** At first acquisition this is the ordinary case.
2. The anger scale is bounded: `AddAnger` clamps `[node+0x14]` to `100.0` (literal `0x105f58e8`), and `AddAnger`'s increment is pre-multiplied by `Character[+0x1958]` (the anger multiplier). `15.0` is therefore **15 % of the anger ceiling**, not an unbounded quantity.

### 2.5 ⚑ THE OPERAND THAT CHANGES THE PICTURE — `alertAnimChance`

Limb 2 is a **percentage roll on a shipped record field**, and `jae` is unsigned: `rand()%100 ∈ [0,99]`, so **`alertAnimChance = 0` ⇒ the alert state NEVER fires for that record.** Joined against Lap AB's per-record artifact (digest asserted, imported by identity — `alert_incidence.json`):

| `alertAnimChance` | alert-slot status | records | rostered actors |
|---:|---|---:|---:|
| 0 | `ALERT-SLOT-EMPTY` | 23 | 50 |
| 30 | `ALERT-SLOT-EMPTY` | 2 | 2 |
| 0 | `HAS-ALERT` | 43 | 98 |
| 30 | `HAS-ALERT` | 19 | 33 |
| 100 | `HAS-ALERT` | 4 | 5 |

- **Records that can alert at all** (non-zero chance **and** non-empty slot): **23 / 91**
- **Rostered actors that can alert at all: 38 / 188 (20.2 %)**
- **Expected number of actors that actually alert over a full roster: 14.90 / 188 (7.9 %)**

> **⚑ This overturns Lap AA's reading in its § 5.2 box.** Lap AA wrote *"the distance limb is satisfied for essentially every body in the band… every such body is pushed into an animation state before it marches."* The distance limb **is** satisfied for essentially every body — Lap AA was right about that limb. But Lap AA had not yet seen limbs 2 and 3, and those two remove **~92 %** of the roster's bodies from the alert. The alert is a **sparse garnish on ~8 % of arrivals**, not a universal spawn-adjacent delay. `UNREACHED-AB-5` (does `alertAnimChance` gate this?) closes **YES — it gates the STATE, not merely the animation.**

---

## 3 · HALF 2 — THE DURATION

### 3.1 The exit, decoded end to end

**(a) `OnBegin` (`0x109410`, evidence `07`)** — one call:
`ControllerAI::PlayAnimation(AnimationSet_Type = 0x21 /*Alert*/, <Name>, speed = 1.0f, loop = false, 0)`.

**(b) `HandleEvent` (`0x1094f0`, evidence `08`)** — the whole body, after the magic-static init, is:

```
10109568: mov  eax, [ebp+8] ; mov eax, [eax]      ; incoming event's interned Name id
1010956d: cmp  eax, [0x1080b338]                  ; the static Name built from literal 0x1052d3f4
10109573: jne  +0x91
10109575: mov  eax,[esi] ; mov ecx,esi ; push 1
1010957b: call [eax + 0x10c]                      ; vtable+0x10c
```

- literal `0x1052d3f4` = **`"End"`**
- vtable `+0x10c` on `??_7ControllerMonsterStateAlertBeforePursue@GAME@@6B@` (`0x5b4af0`) resolves to `0x5e050`, an ICF group whose 19 names include **`?SetDone@?$ControllerAIStateT@VControllerMonster@GAME@@VMonster@2@@GAME@@MAEX_N@Z`**; the body is `mov byte [ecx+0xc], al` (evidence `09`). `+0x108` is its reader, `IsDone()`.

**So: `AlertBeforePursue` ends iff and when it receives the animation event named `"End"`.** No timer, no distance re-check, no `OnUpdate` exit — `OnUpdate` (`0x109430`) only faces the target (`Character::RotateTowards`), and `OnEnd` (`0x7f40`) is a bare `ret`.

**(c) routing** — `?HandleEvent@ControllerAI@` (`0xe6130`, evidence `10`) forwards to `temporaryStates.top()` if `this[+0x214] != 0`, else to the persistent state at `this[+0x1e4]`, via `state->vtable[+0x34]` — which is exactly the `HandleEvent` slot in the vtable dump.

**(d) the pop** — `?Update@ControllerAI@` (`0xe5b80`, evidence `11`):

```
ControllerCombat::Update(dt)
while (GetExecutingState()->IsDone())        ; vtable+0x108
{   top = *[this+0x210];
    top->OnEnd();                            ; vtable+0x114
    top->SetDone(false);                     ; vtable+0x10c (0)
    <unlink node>;  --[this+0x214];  free(node);
    GetExecutingState()->OnBegin();          ; vtable+0x110  <-- Pursue::OnBegin re-fires here
}
executing = ([this+0x214] ? top : [this+0x1e4]);
executing->OnUpdate(dt);                     ; vtable+0x118
```

**The alert is a temporary state stacked over a live `Pursue`.** On pop, `Pursue::OnBegin()` runs and `Pursue::OnUpdate(dt)` runs **in the same tick** — the transition costs no extra frame.

### 3.2 Who emits `"End"` — it is engine-synthesised, not authored

`D-Z-1` guard run over `Engine.dll`: there is **exactly one** standalone `"End"` literal (`0x102a5834`) and **exactly one** code reference to it — inside the animation-instance update. Evidence `12`:

```
1003113c: movss xmm0,[ebx+8] ; addss xmm0,[ebp-0x14] ; movss [ebx+8],xmm0   ; advance play-head
1003114b: test  al, al                                    ; the end-crossing flag
1003114d: je    skip
          <magic-static Name::Create("End") -> 0x1036891c>
100311af: push  0x1036891c
100311b4: call  [entity_vtable + 0xf8]                    ; Entity::RegisterAnimationCallback(Name)
```

and the flag itself (evidence `13`, `0x30577`–`0x305d4`):

```
eax = GraphicsAnim[+0x8c] ; ecx = eax-1            ; last frame index
if ( loop) edx = (prevTime > newTime)              ; wrapped
if (!loop) eax = (lastFrame > prevTime) && (newTime >= lastFrame)
or dl, al ; mov [ebp-0x20], edx                    ; -> consumed at 0x1003113c
```

So `"End"` is **not** an authored `CallbackPoint` in the `.anm` (those exist separately — `GraphicsAnim::GetNumCallbackPoints`, 32-byte stride at `[+0x94]…[+0x98]`); it is generated by the playback code on the update tick that crosses the animation's last frame. The dispatch chain is then: `Actor::HandleAnimationCallbacks` (`0x26de0`) drains the queue at `Actor+0x3cc/+0x3d0` into `vtable+0x1e0` = `Character::AnimationCallback` (`0x454b0`), whose `"End"` branch (evidence `14`) does `this->vtable[0](); [[this+0x1ba4]+4]->vtable[8](name)` — the controller's `HandleEvent`. `"End"` is item 0 of the animation event vocabulary at `0x104f4eb8`: `End · L Footstep · R Footstep · Pickup · Fall · StopRotation · HideRightHand · HideLeftHand · ShowRightHand · ShowLeftHand · voxSound · deathSound1 · deathSound2`. Every animation-driven controller state in `Game.dll` keys on the same `"End"` (Emote, Flee, Attack, JumpAttack, Startup, GettingUp, WaitToAttack, UseSkillOnPoint, QuestPlayAnimation, …), which is the cross-check that this is the generic completion event and not an alert-specific hook.

### 3.3 The number — and it upgrades Lap AB's `DERIVED` column to a decode

`?LoadANMData@GraphicsAnim@` (`0x87660`, evidence `15`) maps the `.anm` header verbatim:

```
100876c2: mov eax, [edi]     ; mov [esi+0x8c], eax     ; header word 1  -> GraphicsAnim+0x8c
100876d0: mov eax, [edi+4]   ; mov [esi+0x90], eax     ; header word 2  -> GraphicsAnim+0x90
```

with `[esi+0x8c]` read by `?GetLength@GraphicsAnim@` and `[esi+0x90]` by `?GetFrameRate@GraphicsAnim@` (evidence `16`; the latter's symbol is ICF-shared with `GetNumHitBoxes@GraphicsMesh`). And the playback code converts:

```
10030485: xmm1 = channelTime_ms * 0.001f      (0x102e0400 = 0.001)
10030494: xmm1 = xmm1 * (float)[GraphicsAnim+0x90]     -> frame index
```

> **⚑ `UNREACHED-AB-1` closes.** Lap AB found the `.anm` `rate` field constant at **30** across **3,452 / 3,452** files but refused to call it fps, publishing seconds as `DERIVED`. The field is **divided into `seconds` to yield a frame index**: it *is* frames-per-second, decoded. Lap AB's `seconds_at_30fps_DERIVED` column is hereby a **decode**, and its identification of header `field0 = bones`, `field1 = frames` is independently confirmed by the loader.

The crossing predicate fires at `newTime >= numFrames − 1` in frame units, so the play-head reaches it at `(frames − 1) / frameRate` seconds. Therefore, with Lap AB's measured alert-animation lengths:

> **duration_seconds = (frames − 1) / (frameRate × speedMultiplier)**, evaluated per monster, with `frameRate = 30` on 3,452 / 3,452 shipped `.anm`s and `speedMultiplier = 1.0f` at the `OnBegin` call site.
>
> **Restricted to the population that can actually alert** (the 23 records / 36 resolved slots of § 2.5, not the roster-wide 94): `frames` min **41** · p25 **51** · median **61** · p75 **68** · max **74** ⇒ **1.333 s · 2.000 s · 2.433 s** (min/median/max). Plus one controller tick of pop latency (§ 3.1 d).
>
> *(The roster-wide figure Lap AB published — 23 / 49 / 74 frames over all 94 slots — is not the right window for this model: 58 of those 94 slots belong to records whose `alertAnimChance = 0` and which therefore never enter the state.)*
>
> **`UNREACHED-AB-2` closes affirmatively**: state-duration **is** animation length, because the only exit is the event the animation's own completion generates. Lap AB was right to refuse the step on its evidence; this lap supplies the missing link.

### 3.4 ⚑ A prior-lap defect caught in passing

Lap AB § 5.3 states *"Every resolved slot carries `AlertAnimSpeed = 1.0` … so the animation speed does not rescale the length."* **It is 92 / 94, not 94 / 94.** Two resolved slots carry `1.2`, of which **one** falls in the can-alert population: `records/creatures/enemies/devotion/rhino_h02.dbr` (`alertAnimChance = 30`, 49 frames, **1 rostered actor**). The claim is therefore true of 35/36 can-alert slots and false as stated. Consequence is bounded and named in `RESID-D1-1`; published rather than quietly inherited.

---

## 4 · The model the consumer should build (B-5 / baton Layer-1)

```
on EnemyFound(e) in state ∈ {Idle, Patrol, Roam, Wander, WaitToAttack,
                             FollowLeader, DefendLeader, QuestMove}:
    SetState("Pursue")
    ... (skill/buff selection, unchanged) ...
    if  IsInState("Pursue")
    and rand()%100 < monster.alertAnimChance          # 0 for 148/188 rostered actors
    and monster.alert_animation_slot is non-empty     # empty for 52/188
    and enemy is alive
    and distance(self, enemy) > 6.0                   # gameengine.dbr alertDistance
    and angerDiff(self, e) < 15.0                     # 0.0 when e is not yet in the anger map
    then:
        push temporary state AlertBeforePursue over Pursue
        play alert animation (type 0x21), speed 1.0, non-looping
        play alert sound unconditionally
        # body faces the target each tick; issues no locomotion call
        on animation completion -> SetDone(true)
        next controller tick -> pop, Pursue.OnBegin(), Pursue.OnUpdate(dt) same tick
    else:
        if rand()%100 < monster.alertSoundChance and firstTimeEver(self):
            play alert sound (once per monster lifetime)
```

Expected incidence over a full roster: **14.9 of 188 bodies (7.9 %)** alert; each for **1.33–2.43 s**, median **2.00 s** (per-monster, from its own alert `.anm`).

## 5 · Residuals — named, not smoothed

| tag | what is not decoded | why it does not undermine the verdicts |
|---|---|---|
| `RESID-D1-1` | **the last hop of the loop/speed parameters.** `OnBegin` passes `speed = 1.0f, loop = false`; both flow `ControllerAI::PlayAnimation` → `PlayAnimationAction[+0x3c/+0x40]` → `AnimationSet::PlayAnimation` → **an un-named per-slot class' `vtable+0x4`** → `Actor/AnimChannel::PlayAnimation`, where `_N` is unambiguously the loop flag (`AnimChannel+0xc`) and `M` the speed (`AnimChannel+0x14`). The slot class is not exported by name; whether it multiplies the record's `AlertAnimSpeed` into the passed `1.0f`, and how it weights the `{1,2,3}` variants, is **UNDECODED**. | `AlertAnimWeight = 100.0` on all can-alert slots, and `AlertAnimSpeed = 1.0` on **35 of 36** of them (§ 3.4) — so the composition is the identity except on one record with one rostered actor, where the duration would be 1.2× shorter (`1.600 s` → `1.333 s`) if the speed *is* composed. **Bound the exposure, do not guess the hop.** Flag it if the model is generalised beyond tier-16. |
| `RESID-D1-2` | **immobility during the alert.** Carried unchanged from Lap AA DO-NOT 4: `OnUpdate` issues no locomotion call, but whether the controller's outer update moves the body regardless is not decoded (`UNREACHED-U1`'s virtual-dispatch driver). | Independent of both verdicts. Still `DECLARED, not DECODED`. |
| `RESID-D1-3` | **anger dynamics.** `GetAngerDiff`'s *arithmetic* and its zero-on-absent case are decoded; the full accrual law in `ControllerMonster::AngerUpdate` (`0xfba90`: `GetCharactersInSphere` → `AddAnger` → `AngerManager::Update`) is not, so the limb's long-run hit-rate is not quantified. | The limb passes trivially at first acquisition (diff = 0.0 on an absent record), which is the only moment the alert can fire (§ 2.3 — combat states never re-enter it). |
| `RESID-D1-4` | **`AnimationSet_Type` enum, globally.** Carried `UNREACHED-AB-4`. Only `0x21 == Alert` is claimed — now independently corroborated: the gate reads `AnimationSet+0x90`, whose slot index is exactly `0x21`, to test the **alert** slot's emptiness. | Narrow claim, twice-anchored. |

## 6 · ⚑ DO-NOT block (binding on B-5 and on the baton)

1. **DO NOT** model the alert as a universal spawn-adjacent delay. **~92 % of rostered actors never alert** (§ 2.5). Lap AA's § 5.2 box is superseded on this point.
2. **DO NOT** implement `ShouldPlayRallyOrAlert` as the state's entry predicate. It is a **sound** latch (§ 2.1). Modelling it as the state gate would produce an alert that fires once per monster lifetime and ignores `alertAnimChance` — wrong on both counts.
3. **DO NOT** give the alert a fixed duration. It is **per-monster, animation-driven**, spanning **3.2×** across the roster (§ 3.3). A fold that needs a scalar here does not have one — it has a per-record join.
4. **DO NOT** treat `alertDistance = 6.0` as a magnitude. It is limb 5 of six, and it is the *weakest* limb in KC2 (satisfied by essentially every body). Carried from Lap AA DO-NOT 3, unchanged in force.
5. **DO NOT** let the alert delay re-fire on re-acquisition. Pursue/Attack/RepositionForAttack/Trapped have their own `EnemyFound` and never reach the gate (§ 2.3).
6. **DO NOT** cite the decoy literal `0x1052c33c` as an entry point. It is the registration-table copy of `"AlertBeforePursue"`, enumerated in § 2.2 so that it is **visibly excluded**, not so it is available.
7. **All prior DO-NOT blocks are carried unchanged** — Lap AA § 6 (with item 3 restated above and its § 5.2 box narrowed by § 2.5 here), Lap AB § 5.4 (with `AB-1`, `AB-2`, `AB-5` now closed), Laps V / V-2 / W / X / Y / Z.

## 7 · Prior-lap ledger touched by this lap

| tag | disposition |
|---|---|
| `UNREACHED-U3` (entry condition) | **CLOSED** — and re-pointed: the predicate is the six-limb gate, not `ShouldPlayRallyOrAlert` |
| `U-U-2` / `UNREACHED-AA-3` (duration) | **CLOSED** — animation-length-driven, per monster |
| `UNREACHED-AB-1` (`.anm` `rate` = fps?) | **CLOSED — YES**, decoded from the playback conversion |
| `UNREACHED-AB-2` (length ≠ duration) | **CLOSED — they are equal**, via the `"End"` completion event |
| `UNREACHED-AB-5` (`alertAnimChance` gates?) | **CLOSED — YES**, and it gates the **state** |
| `NAMED-AA-1` (anger limb) | **CLOSED as arithmetic** (`anger − baseline`, baseline re-snapshotted each anger tick; `0.0` when absent). Accrual law remains `RESID-D1-3`. |
| `UNREACHED-AB-4` (full anim enum) | carried, unchanged |
| `UNREACHED-U1` (outer update driver) | carried, unchanged — see `RESID-D1-2` |

---

## 8 · Evidence index

All under `evidence/`, all regenerated by `mcd1_alert_decode_2026_08_24.py`; `decode.log` is the full instrument transcript, `manifest.json` the file list, `alert_incidence.json` the § 2.5 join.

`01` ShouldPlayRallyOrAlert · `02` gate · `03` sound tail · `04` DoesAnimationExist · `05` GetAngerDiff · `06` anger baseline snapshot · `07` OnBegin · `08` HandleEvent · `09` SetDone/IsDone · `10` ControllerAI::HandleEvent · `11` ControllerAI::Update pop · `12` engine `"End"` emission · `13` end-crossing predicate · `14` Character::AnimationCallback `"End"` branch · `15` LoadANMData header · `16` GetLength/GetFrameRate · `17` ControllerAI::PlayAnimation · `18` AnimationSet::PlayAnimation · `19` AnimChannel::PlayAnimation · `20` Monster::Load chance fields

---

*legolas (`UNKNOWN-RESEARCHER`), 2026-08-24. Read-only on all substrate. No pushes.*
