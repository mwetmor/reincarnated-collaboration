# KC2 MODEL-COMPLETION RUN · mini-lap **D-11** — `Timeout` SCOPE and `Delay` × `skillCooldownTime` COMPOSITION

**Agent:** legolas (UNKNOWN-RESEARCHER) · **Date:** 2026-08-25 · **Conductor:** gandalf (`RUN-CONDUCTOR`)
**Commission:** ruling **`R-L60-2`** — `MD-B4-2` (D-2 CARRIED-QUESTION-1) and `MD-B4-3` (D-2 CARRIED-QUESTION-2)
**Consumes:** `reincarnated-engine/src/reincarnated/simulation/math/kc2-mc-b4-specials-2026-08-24.md` § MD table (lines ~468-469)
**Prior art reused:** D-2 (`…lap-d2-specials-reuse-gates/`) field decode · D-10 (`…lap-d10-…/`) toolchain (`d4b_pe.py`, `d4b_dis.py`, `d8_lib.bounded()`, `d7_step9_xref.py`, `d10_step1_dump.py`, `d10_step5_vslot_callscan.py`)
**Substrate (pinned, read-only):** `/Users/admin/Games/vendor/grim-dawn/Game.dll` sha256 `4876d6bdb69cca71cfa987652cbd7a42cf6d5578564d02d09aaf9b55c078ab02` — **byte-identical to the D-2 and D-10 pins.**
**Discipline:** READ-ONLY. Law 3 absolute. Every claim below is `decoded` unless explicitly tagged otherwise.

---

## § 0 · VERDICT TABLE

| target | verdict | one line |
|---|---|---|
| **`MD-B4-2` — `Timeout` scope** | **DECODED — and it is NEITHER offered reading.** `Timeout` is **PER-SLOT** and it is **not a recovery window at all**: it is a **one-shot post-aggro arming delay.** | Loaded as `Timeout×1000` ms into a **per-slot** counter that starts ticking only once `ControllerMonster::FindEnemy` latches a target, is required `≤ 0` by `ChooseBestSkill`, and is **never re-armed by any code path** on a generic monster. `Delay` — not `Timeout` — is the reuse gate, re-armed per-slot on use. |
| **`MD-B4-3` — `Delay` × `skillCooldownTime`** | **DECODED — two INDEPENDENT gates that must BOTH be satisfied.** | `Delay` gates the AI's slot offer (`ControllerMonster::ChooseBestSkill`); `skillCooldownTime` gates the same slot on the *same* pass through a second, longer chain (`SkillManager::Update → Skill::Update → Skill::SetAvailability → Skill.m_available → Skill::IsSkillEnabled`), which `ChooseBestSkill` calls as its 5th predicate and `SkillManager::StartSkill` calls again. Neither consumes state when it blocks. **Effective reuse interval = `max(Delay, skillCooldownTime)`.** |
| **Does the incumbent "prefer `skillCooldownTime`" survive?** | **NO — FALSIFIED.** | It is not a *selection between* the two fields at all. Replace `effective_cooldown_s = skill_cooldown_s or delay_s` with `max(delay_s, skill_cooldown_s or 0.0)`. On D-2's 14 firing slots this lengthens 7 gates (up to 14× on `dravis_thrall_01 special2`) and changes none of the other 7. |
| **Bonus falsification (unprompted, load-bearing)** | **R-PM2-1's "`delay_s` is ALSO the initial-availability gate" is FALSIFIED.** | The engine initialises the per-slot **delay** timer to **0** (`SetSpecialAttackSkill+0x5a`) and the per-slot **timeout** timer to `Timeout×1000` (`+0x54`). The first-cast gate is `Timeout` (pet range 0.0–6.0 s), not `Delay` (1.5–50.0 s). The sim is currently **over**-gating the opening cast. |

---

## § 1 · THE STRUCTURE — where the four DBR fields actually live at runtime

### 1.1 The loader: `Monster::InitSkillsInController`

The `specialAttack*` DBR field-name strings live in one contiguous `.rdata` block at `0x00561504…0x005618c8`
(`evidence/step1_specialattack_strings.txt`, 54 strings). Every one of them has **exactly one** 4-byte
reference image-wide, and all of them land in the same function
(`evidence/step2_strxref_slot1_slot2.txt`):

```
?InitSkillsInController@Monster@GAME@@AAEXABVLoadTable@2@PAVControllerMonster@2@I@Z   @ 0x002d8850
```

Note the naming: **slot 1 has no index** (`specialAttackSkillName` / `…Timeout` / `…Delay` / `…Chance` /
`…Range`); slots 2..8 are indexed. This matches `monsterskillmanager.tpl` exactly (D-2 § 1).

Slot 1's block, verbatim (`evidence/step3_initskillsincontroller.txt`):

```
0x002d88e7  push     0x10561578                    ; "specialAttackTimeout"
0x002d88ef  call     edx                           ; LoadTable::GetFloat(name, default=0.0f)
0x002d88f1  fmul     dword ptr [0x105f5918]        ; f32 = 1000
0x002d8903  push     0x10561590                    ; "specialAttackDelay"
0x002d890b  fstp     dword ptr [esp + 0x18]
0x002d890f  cvttss2si ebx, dword ptr [esp + 0x18]  ; ebx = Timeout  in MILLISECONDS
0x002d8915  call     eax                           ; GetFloat("specialAttackDelay")
0x002d8923  push     0x105615a4                    ; "specialAttackChance"
0x002d892b  fmul     dword ptr [0x105f5918]        ; f32 = 1000
0x002d8935  cvttss2si edi, dword ptr [esp + 0x18]  ; edi = Delay    in MILLISECONDS
0x002d893b  call     eax                           ; GetFloat("specialAttackChance")   (NOT ×1000)
...
0x002d897e  mov      dword ptr [esp + 0x28], ebx   ; SpecialAttackSkill + 0x04 = timeout_ms
0x002d8982  mov      dword ptr [esp + 0x2c], edi   ; SpecialAttackSkill + 0x08 = delay_ms
0x002d8986  mov      dword ptr [esp + 0x30], 0     ;                    + 0x0c = 0
0x002d898e  mov      dword ptr [esp + 0x34], 0     ;                    + 0x10 = 0
0x002d8996  call     0x104bfcf0                    ; __ftol2 (chance f32 -> int)
0x002d89a0  mov      dword ptr [esp + 0x38], eax   ;                    + 0x14 = chance (int %)
0x002d89ab  mov      dword ptr [esp + 0x44], esi   ;                    + 0x18 = range enum
0x002d89af  call     ?SetSpecialAttackSkill@ControllerMonster@…   (index = 0)
```

⚑ **`Delay` and `Timeout` are both stored as INTEGER MILLISECONDS** (`×1000.0` then `cvttss2si`) — the same
units proof shape D-10 § 1.1 used for `Disruption`. `Chance` is **not** scaled; it is truncated to an int and
compared against `rand() % 100`. **`0x104bfcf0` is the CRT `__ftol2`/`_ftol_sse` helper**, decoded from its
body (`movd eax,xmm0; and 0x7fffffff; cmp 0x7f800000; cvtss2sd; …; fnstcw` — a float→int64 conversion with
IEEE special-case handling), not a game function (`evidence/step6_struct_helpers.txt`).

**Corroboration — the same register assignment recurs in the independently-compiled slot-2 block**
(`0x002d8a01` Timeout→`ebx`, `0x002d8a1d` Delay→`edi`, stored to `+0x28`/`+0x2c`). Two independent code
blocks, same mapping. The interleaving (the *next* field-name string is pushed one call ahead of the
`fstp`/`cvttss2si` that retires the *previous* value) is standard MSVC FPU scheduling and is the only
reading under which both blocks are consistent.

### 1.2 The runtime record: `ControllerMonster` special-attack slot array

`?SetSpecialAttackSkill@ControllerMonster@GAME@@QAEXIABUSpecialAttackSkill@2@@Z` @ `0x000f7cf0`
(`evidence/step4_setspecialattackskill.txt`) computes `ebx = this + index*28` (`lea eax,[edx*8]; sub eax,edx;
lea ebx,[esi+eax*4]` = `index*7*4`) and writes:

| controller offset (slot *i*) | source | meaning | provenance |
|---|---|---|---|
| `0x3ec + 28i` | `src+0x00` | **skillId** (0 ⇒ slot empty) | decoded |
| `0x3f0 + 28i` | `src+0x04` | `timeout_ms` — **const copy, never read again** | decoded |
| `0x3f4 + 28i` | `src+0x08` | `delay_ms` — the const the reuse timer re-arms from | decoded |
| `0x3f8 + 28i` | `0` | **RUNNING DELAY TIMER**, initialised **0** | decoded |
| `0x3fc + 28i` | `src+0x04` | **RUNNING TIMEOUT TIMER**, initialised `timeout_ms` | decoded |
| `0x400 + 28i` | `src+0x14` | `chance` (int, 0..100) | decoded |
| `0x404 + 28i` | `src+0x18` | `range` enum | decoded |

Stride **28 (0x1c)** and **8 slots** are both confirmed independently by `ChooseBestSkill`'s loop
(`add esi, 0x1c` / `cmp eax, 8`) and by `SkillUsed`'s scan (`add ecx, 0x1c` / `cmp eax, 8`).

**Exhaustive access census** (`evidence/step7_dispscan_slotfields.txt`, `step11`, `step12`): across the whole
`.text`, the eight per-slot displacement families are touched by **exactly six** functions —
`ControllerMonster::ControllerMonster` (zero), `SetSpecialAttackSkill` (load), `GetSpecialAttackSkillId` /
`GetSpecialAttackSkillInfo` (getters), `ChooseBestSkill` (the gate), `ControllerMonsterState<…>::SkillUsed`
(re-arm), `ControllerMonster::Update` (tick) — plus two boss-specific derived controllers
(`ControllerGraeae::{InitialUpdate,GetEye,LoseEye}`, `ControllerMonsterSynergy::InitialUpdate`) that rebuild
the array for their own scripted behaviour. **The `timeout_ms` const family (`0x3f0, 0x40c, 0x428, 0x444,
0x460, 0x47c, 0x498, 0x4b4`) has ZERO readers** — it is written at load and never consulted.

*(Two apparent hits were run down and dismissed as offset collisions on unrelated objects:
`ControllerMonsterStateStartup::OnEnd+0x96` `mov eax,[eax+0x418]` is a **vtable** dispatch on a `Character`
(`evidence/step34_startup_onend.txt`), and `Character::AttackTarget+0x12` `mov eax,[eax+0x150]` is likewise a
virtual call, not a cooldown read. The displacement scanner is type-blind by construction; both were
resolved by reading the instruction context.)*

---

## § 2 · `MD-B4-2` — `Timeout` IS PER-SLOT, AND IT IS AN ARMING DELAY, NOT A RECOVERY WINDOW

### 2.1 The gate — `ControllerMonster::ChooseBestSkill` @ `0x000f8020`

`evidence/step8_choosebestskill.txt`. The whole selection loop, decoded:

```
0x000f807b  lea esi, [edi + 0x3fc]          ; cursor = &slot[0].timeoutTimer
0x000f8081  mov [ebp-4], 0                  ; i = 0
loop:
0x000f8090  cmp dword ptr [esi - 0x10], 0   ; slot[i].skillId
0x000f8094  je  next                        ;   empty        -> skip
0x000f809a  cmp dword ptr [esi - 4], 0      ; slot[i].DELAY timer   (+0x3f8)
0x000f809e  jg  next                        ;   still > 0    -> skip
0x000f80a4  cmp dword ptr [esi], 0          ; slot[i].TIMEOUT timer (+0x3fc)
0x000f80a7  jg  next                        ;   still > 0    -> skip
0x000f80ad  call [rand]                     ; ---- chance roll ----
0x000f80b3  cdq ; mov ecx,0x64 ; idiv ecx   ; edx = rand() % 100
0x000f80bb  cmp edx, dword ptr [esi + 4]    ; slot[i].chance   (+0x400)
0x000f80be  jae skip                        ;   roll >= chance -> skip
0x000f80c7  ... resolve skillId -> Skill*
0x000f80d2  mov edx, [edx + 0xf4]           ; Skill vtable +0xf4
0x000f80d8  call edx                        ; = Skill::IsSkillEnabled()      <-- see § 3
0x000f80da  test al,al ; je skip
0x000f80de  push [esi + 8]                  ; slot[i].range enum  (+0x404)
0x000f80e6  call ?IsSkillInProperRange@ControllerMonster@…
...
0x000f8135  add esi, 0x1c                   ; stride 28
0x000f813b  cmp eax, 8 ; jl loop            ; 8 slots
```

⚑ **Two independent per-slot countdowns, both required `≤ 0`.** The loop body **writes nothing** — a slot
that fails any predicate costs no state. That fact is load-bearing for § 3.

### 2.2 Who re-arms which — `SkillUsed` @ `0x000d14d0`

`evidence/step9_skillused_controllermonsterstate.txt` — the entire function:

```
?SkillUsed@?$ControllerMonsterState@…@GAME@@MAEXI@Z(unsigned int skillId)
  scan i = 0..7 over [esi + 0x3ec + 28i]  looking for skillId
  on match:
     0x000d1501  mov eax, dword ptr [esi + ecx*4 + 0x3f4]   ; slot[i].delay_ms      (const)
     0x000d1508  mov dword ptr [esi + ecx*4 + 0x3f8], eax   ; slot[i].DELAY timer  := delay_ms
```

⚑ **The only re-arm in the engine writes `Delay` into the delay timer of the ONE slot that fired.**
Nothing anywhere writes the timeout timer after load. **`Timeout` is therefore per-slot AND one-shot.**

### 2.3 Who ticks which — `ControllerMonster::Update` @ `0x000f6200`

`evidence/step10_controllermonster_update.txt`, fully unrolled, `ebx = [ebp+8]` = the tick delta in ms:

```
; --- DELAY timers: ticked UNCONDITIONALLY, all 8 slots ---
0x000f63b3  mov eax,[edi+0x3f8] ; test; jle; sub eax,ebx; mov [edi+0x3f8],eax
            … then 0x414, 0x430, 0x44c, 0x468, 0x484, 0x4a0, 0x4bc        (stride 28)

; --- TIMEOUT timers: ticked ONLY IF the aggro latch is set ---
0x000f6455  cmp byte ptr [edi + 0x4d8], 0
0x000f645c  je  <skip all eight>
0x000f6462  mov eax,[edi+0x3fc] ; test; jle; sub eax,ebx; mov [edi+0x3fc],eax
            … then 0x418, 0x434, 0x450, 0x46c, 0x488, 0x4a4, 0x4c0        (stride 28)
```

And the latch, decoded (`evidence/step13_findenemy.txt`):

```
?FindEnemy@ControllerMonster@GAME@@MAEXXZ @ 0x000fb670
  0x000fb6d1  call ?GetNewTarget@AngerManager@GAME@@QAEPAVCharacter@2@…
  0x000fb6d6  test eax, eax ; je  <no target>
  0x000fb6da  mov  byte ptr [esi + 0x4d8], 1        <-- the latch
```

`byte[+0x4d8]` is written in exactly two places image-wide: the `ControllerMonster` ctor
(`mov dword [ebx+0x4d8], 0x1000000` ⇒ byte `0x4d8 = 0`) and `FindEnemy` (`= 1`). **It is a one-way latch,
never cleared.**

### 2.4 ⚑ The answer to `MD-B4-2`

> **`Timeout` is a PER-SLOT, ONE-SHOT arming delay measured from the instant the monster first acquires a
> target.** It gates the slot's *first* use and nothing after that. It is **not** kit-wide, and it is **not**
> a post-fire recovery window in either scope. The kit-wide reading that GD's own description string
> (*"Seconds - time out for all skill use"*, present only on slot 1) invites is **falsified by the
> consumer**: the field is stored per slot at stride 28, ticked per slot, and tested per slot, and no code
> path keys any lockout off "whichever slot fired".

**Why this reads sensibly against D-2's measured values.** Pet `Timeout` spans 0.0–6.0 s (mode 3.0) — a
believable "don't open the fight with the special" delay. Pet `Delay` spans 1.5–50.0 s — a believable reuse
interval. Under the incumbent reading the two ranges were awkwardly unexplained; under the decode they are
two different quantities with two different natural scales. *(This paragraph is `inferred-with-evidence`
plausibility commentary, not part of the decode.)*

**Corroboration, second way.** The initialiser asymmetry is itself a proof: `SetSpecialAttackSkill` sets the
delay timer to **0** and the timeout timer to **`timeout_ms`** (`0x000f7d44` / `0x000f7d4a`). Only a startup
gate is initialised non-zero; only a reuse gate is initialised open. The two writes come from the same
struct field (`src+0x04` is written to *both* `+0x3f0` and `+0x3fc`), which is exactly what a
"const + running copy" pair looks like and is unexplainable under any recovery-window reading.

---

## § 3 · `MD-B4-3` — `Delay` AND `skillCooldownTime` ARE INDEPENDENT AND-ed GATES

The composition question turns on one predicate: `ChooseBestSkill`'s 5th test,
`call [SkillVtbl + 0xf4]`.

### 3.1 Slot `+0xf4` is `Skill::IsSkillEnabled`, and it is not overridden for any activated skill

`evidence/step14_skill_vtable_f4.txt`, `evidence/step30_slot_f4_census.txt`:

| vtable slot | occupant | classes |
|---|---|---|
| `+0xf4` | `?IsSkillEnabled@Skill@GAME@@UBE?B_NXZ` @ `0x003be680` | **150** — every `Skill*` / `SkillActivated*` / `Skill_Attack*` class |
| `+0xf4` | `?IsSkillEnabled@Skill_Modifier@…` @ `0x00411d60` | 10 modifier classes (same shape, wider) |
| `+0xf4` | `?GetSkillLevel@Skill@…` | 31 `SkillBuff*` classes — shorter vtables, slot is past the end |

`Skill::IsSkillEnabled` decoded (`evidence/step15_isskillenabled.txt`):

```
enabled =  ( m_available[+0x9c] && !m_locked[+0x9d] && m_level[+0x98] > 0 )
        ||   IsActive()                      (vtable +0x2b0)
        ||   m_projectilesEnabled[+0xcd]
```

*(`+0x98` is confirmed as the level by `?GetSkillLevel@Skill@…` @ `0x003be3f0` = `mov eax,[ecx+0x98]; ret`;
`+0x9d` by `Skill::SetLocked` / `Skill::IsLocked`; `+0xcd` by `Skill::EnableProjectiles`.)*

### 3.2 `m_available` is where `skillCooldownTime` enters — and it is live on monsters

`?Update@Skill@GAME@@UAEXAAVCharacter@2@H@Z` @ `0x003b29a0` (`evidence/step36_skill_update.txt`):

```
0x003b29ab  mov eax,[edi+0x150] ; test; jle; sub eax,esi; mov [edi+0x150],eax   ; tick cooldown remaining
...
0x003b2a81  mov ecx,[edi+0x24]            ; SkillManagerBase* (Skill::SetManager writes this)
0x003b2a96  call dword ptr [eax + 4]      ; = SkillManager::GetSkillServices()  -> [mgr + 0x210]
0x003b2a99  test eax, eax
0x003b2a9b  jne 0x003b2aa1                ;   services present -> run the availability pass
0x003b2a9d  test bl, bl                   ;   else: only if this is the local player's character
0x003b2a9f  je  <skip>
0x003b2ab9  push [ebp+8]                  ; Character&
0x003b2abc  mov eax,[edx + 0x148]         ; vtable +0x148 = Skill::SetAvailability
0x003b2ac2  call eax
0x003b2ac4  cmp al, byte ptr [edi + 0x9c]
0x003b2acf  mov byte ptr [edi + 0x9c], al   <-- writes m_available, read by IsSkillEnabled
```

`?SetAvailability@Skill@GAME@@UAE_NAAVCharacter@2@_N1@Z` @ `0x003bf880`
(`evidence/step23_setavailability.txt`):

```
0x003bf892  cmp dword ptr [esi + 0x150], 0    ; cooldown remaining
0x003bf89f  setg al
0x003bf8a2  mov byte ptr [esi + 0x86], al     ; m_onCooldown
...
0x003bf900  cmp byte ptr [ebp + 0x10], 0      ; arg2 — Skill::Update always passes 0
0x003bf904  jne <bypass>
0x003bf906  cmp byte ptr [esi + 0x86], 0
0x003bf90d  jne 0x003bf913                    ; on cooldown -> FAIL
0x003bf913  mov dword ptr [esi + 0x80], 1     ; reason = 1
0x003bf91d  xor al, al ; ret 0xc              ; return FALSE
```

⚑ **The chain closes: `skillCooldownTime` → `Skill::StartCooldown` → `Skill.m_cooldownRemaining (+0x150)` →
`Skill::SetAvailability` → `Skill.m_available (+0x9c)` → `Skill::IsSkillEnabled()` →
`ControllerMonster::ChooseBestSkill` predicate 5.**

**The one thing that could have broken this chain — and does not.** The pass is gated on
`mgr->GetSkillServices() != NULL` (`SkillManager + 0x210`, default `0` from `??0SkillManager`), set only by
`?SetAsControllingManager@SkillManager@GAME@@QAEXXZ` @ `0x004379c0`. That function has **four** call sites
(`evidence/step40_setascontrollingmanager_xrefs.txt`), and one of them is:

```
?Load@Monster@GAME@@UAEXABVLoadTable@2@@Z + 0xa77
  0x002d3a81  lea ecx, [edi + 0x600]        ; the Monster's own SkillManager — the SAME `this+0x600`
  0x002d3a87  call ?SetAsControllingManager@SkillManager@…       ; that InitSkillsInController uses
```

⚑ **Every monster's SkillManager is a controlling manager, so the availability pass runs for monster skills
exactly as it does for the player's.** `SkillManager::Update` dispatches `Skill::Update` through vtable slot
`+0x68` in five loops (`evidence/step41_skillmanager_update.txt`, sites `0x0043ce37 / 0x0043d032 /
0x0043d0c5 / 0x0043d23e / 0x0043d384`), so the tick is live.

### 3.3 The second enforcement point, and the no-state-consumed property

`SkillManager::StartSkill` @ `0x0043da20` (`evidence/step25_startskill.txt`) checks `IsSkillEnabled` **again**
before dispatching (`0x0043da99 call [eax+0xf4]; test al,al; je <fail>`), and so does
`SkillActivatedSpell::StartAction` @ `0x0042b310` and `Skill_AttackRadius::WarmUpStart` @ `0x003e7bb0`
(which then calls `Skill::StartCooldown`, `evidence/step27`, `step33`).

Crucially — **a cooldown-blocked slot never reaches `SkillUsed`**, because `ChooseBestSkill` rejects it at
predicate 5, before the state machine ever builds the `AttackAction`. And `SkillUsed` is the *only* writer of
the delay timer (§ 2.2). So:

* a `Delay`-blocked slot is skipped, no state written;
* a cooldown-blocked slot is skipped, no state written;
* a chance-roll-lost slot is skipped, no state written;
* `ControllerMonster::SkillFailed` @ `0x000fc510` (`evidence/step43_skillfailed.txt`) clears only the
  attack-cadence timer `[+0x2f8]` and notifies the state — **it does not touch the special-slot array**.

⚑ **No gate consumes the other.** Both simply have to be open at the same evaluation.

*(Disclosed one-hop read: `SkillUsed` is invoked unconditionally at
`?UseSkill@?$ControllerAIStateT@VControllerMonster…@+0x507` (`0x000d1d27`, `call [eax+0x11c]`) immediately
after `HandleAction(new AttackAction(...))`, whose return is `void` and is not checked
(`evidence/step21`, `step22`). So `Delay` arms at **dispatch**, not at confirmed execution. This only matters
if an `AttackAction` can be dropped *after* dispatch for a reason not already screened by `ChooseBestSkill` —
`AttackAction::QueryActionPermission` @ `0x0006d870` (`evidence/step32`) screens on target validity and
`SkillManager::IsRunningSkill`, not on cooldown. I did not trace the full action-queue rejection surface;
the `max()` composition below is stated for the normal path.)*

### 3.4 ⚑ The answer to `MD-B4-3`

> **The engine consults BOTH.** `Delay` gates the AI's re-offer of the slot; `skillCooldownTime` gates the
> same slot through `IsSkillEnabled`. Both are tested inside the same `ChooseBestSkill` iteration, neither is
> consumed when it blocks, and both start at essentially the same instant on a successful cast (`SkillUsed`
> arms `Delay` at dispatch; `WarmUpStart`/`ActivateNow` calls `StartCooldown` at activation). **The effective
> reuse interval of a slot carrying both is `max(Delay, skillCooldownTime)`**, after which the `Chance` roll
> resumes per opportunity.
>
> **"Prefer `skillCooldownTime`" is falsified.** It is not a choice between fields; it is a conjunction.

Applied to D-2 § 3's 14 already-firing slots:

| body | slot | `Delay` s | `skillCooldownTime` s | sim today | **engine (`max`)** | delta |
|---|---|---|---|---|---|---|
| `bonerat_witchgod_a01_summon` | special1 | 15.0 | 15.0 | 15.0 | **15.0** | — |
| `chthoniandevourer_b02_summon` | special1 | 9.0 | 3.0 | 3.0 | **9.0** | **3.0×** |
| `hellhound_witchgod_b01_summon` | special2 | 12.0 | 15.0 | 15.0 | **15.0** | — |
| `korvaakservant_a01_summon` | special2 | 6.0 | 3.0 | 3.0 | **6.0** | **2.0×** |
| `korvaakservant_a02_summon` | special2 | 6.0 | 3.0 | 3.0 | **6.0** | **2.0×** |
| `skeleton_c01_summon` | special2 | 20.0 | 20.0 | 20.0 | **20.0** | — |
| `wormworldrot_a01_summon` | special1 | 1.5 | 1.0 | 1.0 | **1.5** | **1.5×** |
| `wormworldrot_a01_summon` | special2 | 4.0 | 3.0 | 3.0 | **4.0** | **1.33×** |
| `wraith_b01_summon` | special3 | 14.0 | 14.0 | 14.0 | **14.0** | — |
| `wraith_c01_summon` | special3 | 14.0 | 14.0 | 14.0 | **14.0** | — |
| `firedevil_01` (×2 bodies) | special1 | 9.0 | 3.0 | 3.0 | **9.0** | **3.0×** |
| `dravis_thrall_01` | special2 | 14.0 | 1.0 | 1.0 | **14.0** | **14.0×** |
| `dravis_thrall_01b` | special2 | 12.0 | 1.0 | 1.0 | **12.0** | **12.0×** |

**7 slots lengthen (`max` = `Delay`), 7 are unchanged. Nothing shortens — the correction is monotonically
damage-DOWN, which is the safe direction.** *(Table values carried from D-2's decoded CSV; the `max` column
is this lap's rule applied to them.)*

---

## § 4 · THE FULL DECODED FIRING RULE (what the baton and the sim should model)

For monster special slot *i* of a generic `ControllerMonster`, per AI evaluation opportunity:

```
fire(i)  ⟺   skillId[i]  ≠ 0
         ∧   delayTimer[i]   ≤ 0        # armed to Delay ms on each dispatch; ticks always
         ∧   timeoutTimer[i] ≤ 0        # armed to Timeout ms at LOAD; ticks only after aggro; never re-armed
         ∧   rand() % 100 < Chance[i]   # integer chance, per opportunity, no state consumed on loss
         ∧   Skill::IsSkillEnabled()    # ⊃ (cooldownRemaining == 0) ∧ (mana available) ∧ level>0 ∧ !locked
         ∧   IsSkillInProperRange(target, Range[i])
         ∧   <skill-type group allowed>  ∧  CloseEnoughToUseSkill(target, skillId)   [when arg2 set]
```

Sim-facing consequences, in priority order:

1. **`AttackSlot.effective_cooldown_s` (`threat.py:498-500`) is wrong.** Replace "prefer `skill_cooldown_s`"
   with `max(delay_s, skill_cooldown_s or 0.0)`. Damage-DOWN on 7 of 14 slots, no-op on the rest.
2. **The initial-availability gate is `timeout_s`, not `delay_s`.** R-PM2-1's reading is falsified in its
   first half. `delay_s` should gate reuse **only**; `timeout_s` should gate the **first** cast, measured from
   engagement start, and should then be discarded for the rest of the fight. This is damage-**UP** on the
   opening cast (typical `Timeout` 0–3 s vs `Delay` 1.5–50 s) and therefore needs a conductor ruling before it
   lands, not a silent flip.
3. **`timeout_s` is no longer a dead field.** D-2 recorded that the sim writes `timeout_s` at
   `threat.py:862` and never reads it. It now has a decoded job.
4. **`Chance` is an integer percent** compared with `rand() % 100`, so `chance = 100` is a certainty and
   fractional DBR values truncate. Worth checking the loader does not carry a float that rounds up.
5. Unchanged from D-2: the `Range` metre annulus remains an unmodelled second gate, and turning it on is
   still a scoped change with its own sweep obligation.

---

## § 5 · WHAT IS **NOT** DECODED (`UNDERIVABLE-WITH-PATH-NAMED`)

| open item | where the derivation would resume |
|---|---|
| **Whether an `AttackAction` can be rejected *after* `SkillUsed` has already armed `Delay`.** `SkillUsed` fires unconditionally at `0x000d1d27` after `HandleAction`; I screened `AttackAction::QueryActionPermission` (`0x0006d870`) and `AttackAction::Execute` (`0x0006d440`) and found no cooldown/mana rejection there, but I did not walk the whole `ControllerBaseCharacter::HandleAction` queue-arbitration surface. | `?HandleAction@ControllerBaseCharacter@GAME@@QAEXPAVCharacterAction@2@@Z` @ `0x000ea480`, and the `CharacterActionPermission` enum consumers. If a rejection path exists, a *wasted* `Delay` arm becomes possible and the composition would be `max()` **plus** an occasional lost cycle. |
| **The mana limb of `SetAvailability`.** `Skill::Update` passes `arg1 = byte[skill + 0x164]`; when that byte is non-zero the mana clause is bypassed. I did not decode what sets `+0x164`, so I cannot say whether monster specials are mana-gated in practice. The *cooldown* limb is unaffected — `Skill::Update` passes `arg2 = 0` as an immediate, so the cooldown test always runs. | writers of `Skill + 0x164`; `?IsManaAvailable@Skill@GAME@@QBE_NXZ` @ `0x003bf780`. |
| **Six `Skill_WPAttack*` classes override `SetAvailability`** (`0x00428120`, vtable `+0x148` census, `evidence/step39`/`step30`). Weapon-pool attacks are a player-side family; I did not check whether any KC2 monster special resolves to one. | `??_7Skill_WPAttack*@GAME@@6B@` slot `+0x148` → `0x00428120`; cross-check against the D-2 slot table's 65 + 484 skill names. |
| **`ControllerGraeae` and `ControllerMonsterSynergy` rewrite the slot array** (`GetEye` / `LoseEye` / `InitialUpdate` write both timer families). Both decodes above are stated for the **generic `ControllerMonster`**. If any KC2 roster body uses one of those controllers, its `Timeout` is *not* one-shot. | `?InitialUpdate@ControllerGraeae@…` @ `0x000ef460`, `?InitialUpdate@ControllerMonsterSynergy@…` @ `0x0010ca70`; the roster's `Class`/controller assignment. |
| **`Timeout` behaviour across a wave boundary / de-aggro.** The `+0x4d8` latch is never cleared, and nothing re-arms the timeout timer, so within one controller lifetime `Timeout` fires once. Whether a Crucible wave re-instantiates the controller (fresh `Timeout`) or reuses it is a spawn-lifecycle question this lap did not open. | `?RestoreState@Monster@…`, and the wave-spawn path already mapped in lap AA/AC. |

---

## § 6 · METHOD, ARTEFACTS, ATTESTATION

**Method.** Five instruments, three inherited from D-10 and two new:

| script | what |
|---|---|
| `d4b_pe.py` · `d4b_dis.py` · `d8_lib.py` · `d10_step1_dump.py` · `d7_step9_xref.py` · `d10_step5_vslot_callscan.py` | inherited unchanged from D-10 |
| `d11_step1_strings.py` | locate every `specialAttack*` C-string with RVA/VA/section |
| `d11_step2_strxref.py` | image-wide 4-byte references to a string VA (finds the field-name pushes) |
| `d11_step3_dispscan.py` | in-phase linear sweep from every export for **any** access to a struct displacement (read *or* write) — the instrument that produced the exhaustive slot-array census |
| `d11_step4_vtable.py` | read named vtable slots (`??_7X@GAME@@6B@` + displacement) with body preview |
| `d11_step5_vfind.py` | inverse — given a target RVA, find which vtable slot holds it |
| `d11_step6_slotcensus.py` | census one vtable displacement across every matching class — answers "is this slot ever overridden?" |
| `d11_digest.py` | digest manifest |

**Corroboration discipline.** Every load-bearing claim is established two ways:

| claim | way 1 | way 2 |
|---|---|---|
| `Timeout`→`+0x3f0/+0x3fc`, `Delay`→`+0x3f4` | register trace through the slot-1 loader block | independently-compiled slot-2 block, identical assignment |
| stride 28, 8 slots | `ChooseBestSkill` loop (`add esi,0x1c` / `cmp eax,8`) | `SkillUsed` scan (`add ecx,0x1c` / `cmp eax,8`); also `SetSpecialAttackSkill`'s `index*7*4` |
| `Timeout` is per-slot and never re-armed | exhaustive displacement census over all 8 timeout-timer offsets | `Update`'s fully-unrolled 8-way tick + the single `SetSpecialAttackSkill` initialiser |
| `Timeout` ticks only post-aggro | `Update`'s `cmp byte[edi+0x4d8],0 / je` | the latch has exactly two writers image-wide (ctor `0`, `FindEnemy` `1`) |
| cooldown reaches the AI gate | `Skill::Update → SetAvailability → +0x9c` instruction chain | `IsSkillEnabled` reads `+0x9c` as its first term; slot `+0xf4` census shows no activated-skill class overrides it |
| the chain is live on monsters | `Monster::Load+0xa77` calls `SetAsControllingManager` on `this+0x600` | `SkillManager::Update` dispatches `Skill::Update` (vtable `+0x68`) at five sites |

**Evidence.** `evidence/step1…step43` — 43 raw listings; every RVA cited above appears in one of them.
**Digests.** `d11_digests.json` (substrate + all 61 lap artefacts).

**Read-only attestation.** No write outside this directory. No vendor file, engine source, engine data file,
sim checkpoint, baton or math note was modified. The `Game.dll` digest is byte-identical to the D-2 and D-10
pins, so all three laps read the same binary.

---

*legolas · KC2-MC mini-lap D-11 · 2026-08-25*
