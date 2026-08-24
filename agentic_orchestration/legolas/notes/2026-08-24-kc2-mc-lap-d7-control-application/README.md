# KC2-MC · Lap D-7 — control-APPLICATION semantics decode (`MD-B2-1` / `MD-B2-2` / `MD-B2-3`)

**Agent:** legolas (UNKNOWN-RESEARCHER) · **Date:** 2026-08-24 · **Conductor:** gandalf (RUN-CONDUCTOR), ledger `L-32`
**Commission:** the three missing decodes named by gamora's B-2 refusal
(`~/Games/reincarnated-engine/src/reincarnated/simulation/math/kc2-mc-b2-control-states-2026-08-24.md` § 3).
**Substrate:** `/Users/admin/Games/vendor/grim-dawn/Game.dll` — 25,091 decorated exports, read-only.
**Method:** the D-4b/D-4c harness (`d4b_pe.py` + `d4b_dis.py`) — symbol-anchored disassembly, vtable
resolution against exported `??_7` vftables, byte-exact `E8 rel32` xref indexing.
**Display-layer guard honoured:** no tooltip / `tags_ui.txt` join was used or needed. Every rule below is
read off an instruction body.

---

## § 0 · VERDICT TABLE

| ask | verdict | one-line rule |
|---|---|---|
| **`MD-B2-1`** magnitude semantics of `defensive<Control>` | **DECODED** | **duration scalar**: `duration *= (1 − r/100)`, clamped `≥ 0`, then truncated into 100 ms buckets |
| **`MD-B2-1`b** does `playerDefenseCap` apply? | **DECODED — YES** | `min(Character::GetDefenseAttributeCap() + Σ maxResist, value)`, applied **per accumulated entry** inside `ProcessDefense` |
| **`MD-B2-1`c** the EoR `defensiveCrowdControl = 25` confound | **DECODED — ADDITIVE, same pool, exactly four families** | `defensiveCrowdControl` **expands** into four separate defence entries — Stun, Freeze, Petrify, Trap — which then join the per-type `defensive<X>` value by **sum** |
| **`MD-B2-2`** player suppression set per family | **DECODED** | matrix in § 3 + `evidence/md_b2_2_player_suppression.csv`; **Confusion, Fear and Taunt are NO-OPS on the player** |
| **`MD-B2-3`** `offensive<Control>Modifier` composition | **DECODED — ONE ADDITIVE POOL** | gamora's analogy is *correct*, and is now a decode: `GetTotalDurationModifierType` sums every matching entry |

Three clean negatives are also recorded (§ 6). Machine-readable table: **`evidence/d7_control_application_parameters.csv`** (43 rows, every row carrying its RVA).

---

## § 1 · THE CHAIN, END TO END

The whole control path is five named functions. Nothing in it was guessed.

```
1.  DamageAttributeReflex::AddDamageToAccumulator            0x00145d70
      rolls uniform(min,max) with the Park–Miller LCG (16807/127773/2836) and pushes a
      CombatAttributeReflexDamage whose +0x1c holds the ROLLED DURATION.
      Shared verbatim by Stun / Sleep / Trap / Freeze / Petrify / Knockdown (vtable slot 10 of all six).

2.  CombatAttributeAccumulator::ProcessDefense               0x000de740
      for each cap entry x each defence entry:  capEntry->Execute(defenceEntry)   -> attr[+0x28] += cap
      then                                       defenceEntry->Process(...)        -> CLAMP (§ 2.3)

3.  CombatAttributeAccumulator::ExecuteDefense               0x000de7e0
      for each defence entry x each damage entry: defenceEntry->Execute(damageEntry)
        -> CombatAttributeAbsDefense::Execute    0x000d9280
        -> damageAttr->ReduceDamage(type, resistValue)

4.  CombatAttributeAbsDamage::ReduceDamage                   0x000d7620      <-- ⚑ MD-B2-1
        if (attr.type == type) attr.value *= (1 - r * 0.01f);
        attr.value = max(attr.value, 0.0f);

5.  CombatAttributeReflexDamage::Execute(Character& tgt)     0x000d8b80
        if (attr[+0x1c] > 0)
            (tgt + 0x3e4)->AddFixedDamage(type = attr[+4],
                                          magnitude = 1.0f,      // literal 0x3f800000
                                          duration  = attr[+0x1c],
                                          source, 0);
```

**Step 5 is the load-bearing one for interpreting step 4.** The magnitude argument is a *hardcoded
`1.0f`* and the duration argument is the CombatAttribute's `+0x1c` — the exact field `ReduceDamage`
scales. So **the resistance stat scales the duration and nothing else.** The "chance gate" and
"threshold" readings are eliminated: there is no RNG draw and no comparison anywhere on this path.

---

## § 2 · `MD-B2-1` — THE APPLICATION LAW

### 2.1 The rule, implementable as written

```
r_type   = Σ over accumulator defence entries with GetType()==family of  min(cap, entry.value)
           cap = Character::GetDefenseAttributeCap() + Σ matching maxResist entries      # if cap > 0
duration = base_duration_s * (1 - r_type/100)                                            # float32
duration = max(duration, 0)
if duration <= 0:  NOTHING IS INSERTED  (AddFixedDamage returns early, 0x00208db9)
buckets  = (int) (duration * 10.0f)                                                      # TRUNCATION
remaining_ms(t) = buckets * 100
```

`GetTotalDefenseType` (`0x000de500`) sums; its averaging branch is gated on `type == 0x27`
(Absorption) and never fires for a control family — the count register stays `0`, the trailing
`comiss xmm0, 1.0 / jbe` skips the divide.

### 2.2 Worked against the KC2 rows

The pinned `data/kc2/pm2_tg2_attack_damage.csv` carries **143 control rows** (Stun 68, Freeze 35,
Petrify 26, Confusion 8, Convert 4, Disruption 2 — all `MEASURED`). Applying the decoded rule to
gamora's own example, `stun_resist = 79`, `base = 1.25 s`, computed in float32 exactly as the binary
does:

| resist | scaled | buckets | delivered |
|---:|---:|---:|---:|
| 0 | 1.2500 s | 12 | **1.2 s** |
| 25 | 0.9375 s | 9 | **0.9 s** |
| 50 | 0.6250 s | 6 | **0.6 s** |
| **79** | **0.2625 s** | **2** | **0.2 s** |
| 80 | 0.2500 s | 2 | **0.2 s** |
| ≥ 100 | ≤ 0 | — | **never inserted** |

**Consistency check on the 143 rows:** exactly **2** rows (the `1.25 s` ones) lose time to the
bucket truncation; the other 141 durations are already exact multiples of 0.1 s in float32, so the
quantisation is a *narrow* correction, not a broad one. It is nonetheless real and it bites precisely
on the duration gamora used as the worked example.

### 2.3 The cap — and a scoped caveat

`Process@CombatAttributeAbsDefenseRestricted` (`0x000d8ff0`), the body used by
`DefenseAttributeAbs_{Stun,Freeze,Petrify,Trap,Sleep,Knockdown,Confusion,Convert,Fear}`:

```
v  = attr[+0x1c];  v += |v| * attr[+0x24] * 0.01f          // % modifier
if (scale > 0) v = scale * 0.01f * v
attr[+0x20] = |v| * 0.0f ;  attr[+0x1c] = v                // "restricted" => reduction factor is 0
cap = char->GetDefenseAttributeCap() + attr[+0x28]
if (cap > 0) attr[+0x1c] = min(cap, attr[+0x1c])
```

`GetDefenseAttributeCap@Player` (`0x0032b720`) is `fld dword ptr [ecx+0x3690]; ret` — a plain player
field, i.e. **the `gameengine.dbr :: playerDefenseCap` seat**. So the cap family *does* cover the
control stats; `freeze_resist = 80` sitting exactly on the cap is now explained rather than
suggestive.

⚑ **Named caveat, and it is mine not gamora's:** the clamp is applied **per accumulated
`CombatAttribute` entry**, and `GetTotalDefenseType` then sums the already-clamped entries.
`GetAllDefenseAttributes@Character` (`0x00055a70`) collects from at least five sources (active buffs,
`SkillManager::GetDefenseAttributes`, an equipment store at `+0x10e4`, and three further virtual
collectors), so **whether the effective total is capped at `cap` or at `n × cap` depends on how many
entries the `DefenseAttributeStore` family emits per type — which this lap did NOT read.** That is
residual **`R-D7-1`** (§ 7). It does not affect the *shape* of the law, only its ceiling.

### 2.4 The EoR confound — resolved, and narrower than feared

`AddToAccumulator@DefenseAttributeAbs_CrowdControl` (`0x001acc70`) does not add one value to one
pool. It allocates **four** `CombatAttribute` objects carrying the same value and stamps them
`[eax+4] = 0x2a, 0x2d, 0x2e, 0x2c` in that order — **Stun, Freeze, Petrify, Trap, and exactly those
four.** `DefenseAttributeDefenseCap_CrowdControl` (`0x001af030`) does the same for the cap.

Therefore:

* **composition is ADDITIVE and it is the same pool.** `stun_resist_effective = defensiveStun + defensiveCrowdControl`. Not multiplicative, not `max()`.
* EoR's `defensiveCrowdControl = 25` while channelling covers **129 of the 143** roster control rows (Stun 68 + Freeze 35 + Petrify 26). It does **not** cover Confusion (8), Convert (4) or Disruption (2).
* `defensiveCrowdControlMaxResist = 25` raises the cap on the same four families only.
* Screenshot 519's `stun_resist = 79` being mid-channel or not is now a **±25 point** question with a decided arithmetic: if the sheet was mid-channel the un-channelled figure is 54; if not, the channelled figure is 104 (subject to `R-D7-1`). The reading is not resolvable from the binary and stays a measurement question — but it is no longer a *semantic* one.

### 2.5 PvP-only multiplier — a trap that is NOT sprung in PvE

`DurationDamageManager::ModifyDuration` (`0x00209db0`) is the only other duration-touching function
on the path. For types `0x2a…0x31` it multiplies by `max(gGameEngine[+0x22f4], 0)` — verified to be
`GetPvpCrowdControlDurationMultiplier` (`0x0026d5d0` is literally `fld [ecx+0x22f4]; ret`) — **but
only when `FactionManager::GetPvpIds(target, attacker, …) == true`.** In the KC2 PvE fight this is a
pass-through. Recorded so nobody re-discovers it as a phantom scalar.

---

## § 3 · `MD-B2-2` — WHAT A CONTROLLED PLAYER CANNOT DO

### 3.1 Family → player state

`Character::StartInvoluntaryEffect(CombatAttributeType)` (`0x0005acc0`) is a flat switch:

| type | family | routes to |
|---:|---|---|
| `0x2a` 42 | Stun | controller vtable `+0x90` → `BeginStun@ControllerPlayer` (`0x000f6ad0`) |
| `0x2b` 43 | Sleep | controller vtable `+0xa8` → `BeginSleep@ControllerPlayer` |
| `0x2c` 44 | Trap | `Character::BeginTrap` (`0x0005afc0`) |
| `0x2d` 45 | Freeze | `Character::BeginFreeze` (`0x0005b020`) |
| `0x2e` 46 | Petrify | `Character::BeginPetrify` (`0x0005b150`) |
| `0x2f` 47 | **Immobilize** | `Character::BeginImmobilize` (`0x0005b280`) |
| `0x30` 48 | Knockdown | `Character::BeginKnockdown` (`0x0005b2e0`) |
| `0x31` 49 | **TakeHit** | controller vtable `+0xa0` → `BeginTakeHit@ControllerPlayer` |

`ControllerPlayer::Begin<X>` forwards to the **current state's** slot; the state names reached are the
string literals passed to `ControllerAI::SetState` by the `Default*Action` helpers:
`Immobilized` · `Trapped` · `Stunned` · `KnockedDown` · `TakeHit` · `Sleeping`
(`0x0011f480 / 0x0011f520 / 0x0011f5c0 / 0x0011f660 / 0x0011f700 / 0x0011f7a0`).

### 3.2 Exactly one control state at a time — and it is a priority ladder

`DurationDamageManager::UpdateFxAndInfluence` (`0x00209fc0`) tests `GetFixedDamage(t) > 0` in this
literal order and takes the **first** hit:

```
0x2f Immobilize  >  0x2e Petrify  >  0x2d Freeze  >  0x2c Trap
    >  0x2b Sleep  >  0x2a Stun  >  0x30 Knockdown  >  0x31 TakeHit
```

On change it calls `StopInvoluntaryEffect(old)` then `StartInvoluntaryEffect(new)` and caches the
winner at `manager[+0x1c]`. **Only one involuntary effect is ever active**, regardless of how many
control timelines are running.

### 3.3 The suppression matrix

Derived by diffing each `ControllerPlayerState<X>` vtable (83 slots, stride `0x14c`) against
`ControllerPlayerStateIdle`. A slot that keeps Idle's occupant is **PERMITTED**; a slot replaced by
`xor al,al; ret n` is **STUB-false** (the request is refused); a slot replaced by a bare `ret n` is
**STUB-ret** (the request is swallowed).

| request (slot) | Stunned | KnockedDown | Sleeping | Trapped | Immobilized |
|---|---|---|---|---|---|
| `RequestUseItem` (58) | PERMITTED | PERMITTED | PERMITTED | PERMITTED | PERMITTED |
| `RequestReleasePet` (59) | PERMITTED | PERMITTED | PERMITTED | PERMITTED | PERMITTED |
| `RequestUseItemOn` (60) | PERMITTED | PERMITTED | PERMITTED | PERMITTED | PERMITTED |
| `RequestItemAction` (61) | STUB-ret | STUB-ret | STUB-ret | STUB-ret | STUB-ret |
| `RequestInteractableAction` (62) | STUB-ret | STUB-ret | STUB-ret | STUB-ret | STUB-ret |
| `RequestNpcAction` (63) | STUB-ret | STUB-ret | STUB-ret | STUB-ret | STUB-ret |
| `RequestCompleteRelics` (64) | PERMITTED | PERMITTED | PERMITTED | PERMITTED | PERMITTED |
| **`RequestSkillAction` (76)** | **STUB-false** | **STUB-false** | **STUB-false** | **IMPL** | **STUB-false** |
| `RequestInstantSkillAction` (77) | PERMITTED | PERMITTED | PERMITTED | PERMITTED | PERMITTED |
| `RequestEvadeAction` (78) | STUB-false | STUB-false | STUB-false | STUB-false | STUB-false |
| **`RequestMoveAction` (80)** | **STUB-ret** | **STUB-ret** | **STUB-ret** | **STUB-ret** | **STUB-ret** |
| `RequestRotateAction` (81) | STUB-ret | STUB-ret | STUB-ret | PERMITTED | STUB-ret |

Reading it in gamora's three-switch vocabulary — **the disc, the motion, the counterplay actives**:

* **motion — SUPPRESSED by all five.** `RequestMoveAction` is a stub in every control state.
* **the disc (channel) — SUPPRESSED by all five, and by *state replacement*, not by a flag.**
  `ControllerPlayerStateUseSkill` inherits **Idle's** `BeginStun`/`BeginSleep`/`BeginKnockdown`/
  `BeginTrap`/`BeginImmobilize` (all `0x0011ff90…0x0011ffe0`), so a landing control calls
  `SetState("Stunned")` **out of** the channel state. The channel does not resume by itself.
* **counterplay actives — SUPPRESSED except under Trap.** `RequestSkillAction` returns `false` under
  Stun/Knockdown/Sleep/Immobilize. **Trapped is the exception:** it carries a real implementation
  (`0x00123c30`) and a dedicated companion state `ControllerPlayerStateUseSkillWhileTrapped` — a
  trapped player may still *cast*, and may still *rotate*, but may not *move*.
* **item use — PERMITTED under every control state.** `RequestUseItem` / `RequestUseItemOn` /
  `RequestReleasePet` / `RequestInstantSkillAction` are untouched. Potions and instant-cast skills
  work through a stun. This is the single most surprising row and it is decoded, not inferred.

Two further decoded facts about the state itself:

* **no refresh.** Every `Begin<Control>` slot *inside* a control state is `Stop@Fx` (`0x00007f40`,
  a bare `ret`). A second landing of the same family does not restart the state.
* **no self-timer.** `DefaultBeginStunAction` passes a zeroed `ControllerAIStateData`
  (`0x0011f609`–`0x0011f617`), and `OnUpdate@ControllerPlayerStateStunned` (`0x00123490`) only
  self-ends when its counter started `> 0`. The four other control states have `OnUpdate` = `ret 4`.
  **The clock is the `DurationDamageManager` bucket list, and only that.**

### 3.4 ⚑ Confusion, Fear and Taunt are NO-OPS on the player

This is the finding with the sharpest consequence for B-2, because **Confusion is the only family
B-2's own measurement observed landing (2/2).**

`UpdateFxAndInfluence` handles the influence families separately, and **only when no involuntary
effect is active** (`cmp [edi+0x1c], 0 / jne`, `0x0020a11c`). It then calls the target's vtable
`+0x3c8` (Confusion) or `+0x3c4` (Fear) with `GetFixedDamageDuration(type)` in **ms**.

| slot | Player occupant | Monster occupant | verdict |
|---|---|---|---|
| `+0x3c8` Confusion | `0x000084d0` — the shared `ret 4` stub | `CombatExertInfluenceConfusion@Monster` `0x002d9670` | **player: NO-OP** |
| `+0x3c4` Fear | `CombatExertInfluenceFear@Character` `0x00054690` → controller `+0x84` | (same) | ControllerPlayer `+0x84` = `0x0000f100`, a `ret 8` stub → **player: NO-OP** |
| `+0x3cc` Taunt | `CombatExertInfluenceTaunt@Character` `0x000546d0` → controller `+0x8c` | (same) | ControllerPlayer `+0x8c` = `0x0000f100` → **player: NO-OP** |

`Character::CombatExertInfluenceConfusion` is *itself* the stub at `0x000084d0` (the same RVA the
export table also names `AddTimeToLive@Skill` and `SetGlobalChance@CombatAttributeAccumulator` —
MSVC folded every identical `ret 4` body). The Player class does not override it; the Monster class
does. **Confusion applied to a player does nothing at all.**

⚑ **Consequence for B-2:** the two observed `Confusion` landings on salts 0 and 1 have a decoded
player-side effect of **zero**. Limb E's cheapest, most-observed cell is closed by a negative rather
than by a model. `Convert` is likewise absent from `StartInvoluntaryEffect`'s switch and from the
influence pair — it has no player-side consumer on this path at all.

---

## § 4 · `MD-B2-3` — THE OUTGOING MODIFIER POOL

`CombatAttributeAccumulator::GetTotalDurationModifierType(Character*, type)` (`0x000de490`):

```
total = 0
for entry in modifierList[+0x10 .. +0x14]:
    if entry->GetType() == type:
        entry->vtable[0x30](char, &out);  total += out
return total
```

A flat additive walk, structurally identical to `GetTotalDamageModifierType` (`0x000de410`) — the
function whose law gamora verified on 39 bodies. Its sole consumer in the image is
`Player::CollectDamageDurationModifiers` (`0x0031a290`).

⚑ **`MD-B2-3` is therefore DECODED, and it decodes to exactly the value gamora refused to assume.**
`offensiveStunModifier` `+25.0` (Ultimate solo) and `−40.0` (Gladiator survival) join **one additive
pool**: net **−15 %** for Stun, **−30 %** for Freeze / Petrify / Trap. B-2's WARN-2 analogy pin can be
retired and the provenance grade raised from `derived-from-decoded-substrate with the analogy pinned`
to **`decoded`**.

---

## § 5 · TWO STRUCTURAL FACTS WORTH CARRYING

**5.1 Control and DoT share one manager, and the control lane is the "fixed" lane.**
Control families live in `DurationDamageManager`'s *fixed* list (`this+0x38 … +0x3c`, stride `0x24`),
parallel to the DoT list that D-4c decoded (`this+0x2c … +0x30`). Both use the same 100 ms bucket
container. The manager lives at `Character + 0x3e4`.

**5.2 Same-family control does not stack — longest wins.**
Two independent proofs:
* the fixed-entry insert (`0x0020e060`) grows the bucket list only when the incoming length exceeds
  the current one (`cmp [ebx+4], edi; jae skip`, `0x0020e0ae`);
* `GetFixedDamageDuration` (`0x002089b0`) takes the **max** across all matching entries
  (`cmp ebx,eax; cmovg eax,ebx`, `0x002089f2`).

This is the opposite convention from the DoT stacking law D-4c decoded, and it is worth stating
loudly because the two lanes sit in the same class.

---

## § 6 · CLEAN NEGATIVES (searched, not found — with the search recorded)

**N-1 — `Character::CalculateStun` is NOT the control-application path.**
`CalculateStun@Player` (`0x0031ee20`) is a real, fully-readable function —
`if ((a/b)·(1−c/100)·100 > d+15) return (3·a/b + 1000)·(1−c/100) else 0`, with a Monster twin
(`0x002d5170`, factor 1000 and threshold `d+5`) and a `fldz` stub on `Character` (`0x00054110`). It
occupies **vtable slot 286 (`+0x478`)**, between `UnderAttack@Character` and
`CombatCausedHitReaction@Character`. **It has zero call sites.** Searched: (a) capstone linear sweep
of `.text` for `call dword ptr [reg+0x478]` — 0; (b) byte-exact scan of all `FF /2 + disp32` and
`8B /r + disp32` encodings across `.text` — 47 hits, all struct-field loads in unrelated classes
(`Destructible`, `Item`, `EndlessDungeon_Generator`, …), none followed by an indirect call;
(c) function-wise disassembly from all 15,558 exported entry points — 0. The same scan for the
neighbouring slot `+0x468` also returns 0, so the *technique* is the limit, not the conclusion; the
honest statement is **"no call site is reachable from any exported entry point, and none exists as a
direct `[reg+0x478]` encoding anywhere in `.text`."** Recorded and **not used** in any rule above.

**N-2 — there is no `defensiveImmobilize` and no `defensiveTakeHit`.**
The `GetType()` census (278 constant bodies, `evidence/combat_attribute_type_enum.json`) has **no
`DefenseAttribute*` class for enum values 47 or 49**, while `StartInvoluntaryEffect` routes both to
real player states. **Immobilize/slow on a player is not reducible by any per-type resistance stat**,
and is not covered by `defensiveCrowdControl` either (§ 2.4). If the roster ever carries an
immobilise row, it lands at full duration.

**N-3 — control resistance is not applied in `CombatManager::TakeAttack`.**
All seven `GetTotalDefenseType` call sites in `TakeAttack` pass `0x3f` (PercentReflectionResistance),
`0x39` (Reflect), `0x3d` (DamageMultiplier), `0x37` (BlockModifier), `0x38` (BlockAmountModifier) —
never a control type. The control resistance is applied one layer down, in `ExecuteDefense` →
`ReduceDamage`.

---

## § 7 · RESIDUALS

| id | residual | why it does not block B-2's application limb |
|---|---|---|
| **`R-D7-1`** | the per-entry cap of § 2.3 means the effective ceiling is `n × cap` where `n` = number of accumulated defence entries per type; `DefenseAttributeStore`'s merge behaviour was not read | affects the ceiling only, not the law shape. If a build needs the ceiling, model `cap` (one entry) and record the assumption — or commission a follow-up on `AddToStore@DefenseAttribute_Typical` (`0x001a58f0`) and the five `DefenseAttributeStore_*` classes. |
| **`R-D7-2`** | `Disruption` (13) and `Convert` (51) have no consumer on the involuntary or influence path; where they *are* consumed was not chased | 6 of 143 roster rows. Both were already outside `defensiveCrowdControl`'s four-family expansion. |
| **`R-D7-3`** | `TakeHit` (49) reaches `SetState("TakeHit")` but no `ControllerPlayerStateTakeHit` class exists in the export table | not a roster family; recorded because it shares the involuntary ladder and could surface as an unexplained state transition. |

---

## § 8 · WHAT gamora CAN NOW BUILD (and what still must be refused)

**Buildable, decoded, with the rule stated:**
1. `defensive<Control>` as a **duration scalar** with the `(1 − r/100)` law, the `max(·,0)` clamp, the
   `duration > 0` insertion guard, and the `(int)(s·10)·100 ms` quantisation.
2. `defensiveCrowdControl` / `…MaxResist` as an **additive** contribution to exactly
   {Stun, Freeze, Petrify, Trap}, channel-conditional on EoR.
3. The **cap** as `playerDefenseCap + Σ maxResist` (carrying `R-D7-1` as a named assumption).
4. `offensive<Control>Modifier` as **one additive pool** (`MD-B2-3` retired; net −15 % Stun,
   −30 % Freeze/Petrify/Trap).
5. **Suppression:** motion OFF, channel OFF (state replacement), counterplay actives OFF (except under
   Trap), **items and instant-cast ON**, for Stun/Freeze/Petrify/Sleep/Knockdown/Immobilize.
6. **Confusion and Convert on the player: NO EFFECT.** The two observed landings move nothing. This is
   a decoded zero, not a defaulted one.
7. **One control state at a time**, chosen by the § 3.2 ladder; same-family **longest-wins**, never
   additive.

**Still to be refused / carried as assumption:** the `R-D7-1` ceiling; the screenshot-519
mid-channel question (a *measurement* residual now, not a semantic one — the arithmetic is 79 = 54+25
or 79 = 79, and the binary cannot say which).

---

## § 9 · REPRODUCTION

All scripts are read-only against `/Users/admin/Games/vendor/grim-dawn/Game.dll`; all output is under
`evidence/`.

| script | what it establishes |
|---|---|
| `d7_step1_enum.py` | the `CombatAttributeType` enum from 278 constant `GetType()` bodies |
| `d7_step2_vtables.py` | which `AddToAccumulator` / `AddDamageToAccumulator` body each family actually uses |
| `d7_step6_slot.py`, `d7_step7*_*.py`, `d7_step8_fnscan.py` | the `CalculateStun` call-site search (N-1), four independent techniques |
| `d7_step9_xref.py` | byte-exact `E8 rel32` xref index (found `StartInvoluntaryEffect` → `UpdateFxAndInfluence`) |
| `d7_step13_slots.py` | named vtable-slot resolver used throughout |
| `d7_step21_ccexpand.py` | the four-family `defensiveCrowdControl` expansion |
| `d7_step30/31/32` | the `MD-B2-2` suppression matrix + CSV |
| `d7_step50_emit.py` | the 43-row parameter table |

**Outputs consumable by gamora:**
* `evidence/d7_control_application_parameters.csv` — 43 rows: 15 enum, 25 rules, 3 negatives; every row carries `rva` + `fn`.
* `evidence/md_b2_2_player_suppression.csv` — the § 3.3 matrix, one row per `Request*` slot.
* `evidence/combat_attribute_type_enum.json` — the full 62-value enum.
* 25 raw disassembly transcripts under `evidence/step*.txt`.
