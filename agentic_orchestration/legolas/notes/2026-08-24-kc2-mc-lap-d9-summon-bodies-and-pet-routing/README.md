# KC2-MC · Lap D-9 — the two player-summon BODIES, the two call-site xrefs, and pet-side control routing

**Agent:** legolas (UNKNOWN-RESEARCHER) · **Date:** 2026-08-24 · **Conductor:** gandalf (RUN-CONDUCTOR)
**Commission:** ledger row **L-48**, ruling **R-L48-1** — `MD-B3-1` + `MD-B3-2` + `MD-B3-3`, named in
`~/Games/reincarnated-engine/src/reincarnated/simulation/math/kc2-mc-b3-summons-2026-08-24.md` § 8.
**Law 3 governs.** Decode-before-declare. No fitted constants. Where the evidence runs out the row reads
`UNDERIVABLE-WITH-PATH-NAMED` and names the path.

**Substrate (pinned, read-only, digests in `d9_digests.json`):**

| artifact | sha256 |
|---|---|
| `/Users/admin/Games/vendor/grim-dawn/Game.dll` | `4876d6bd…c078ab02` (D-8's pin, unchanged) |
| `…/grim-dawn-edition-III-20260808/database/database.arz` | `2ad6d379…93183bfd` |
| `…/gdx1/database/GDX1.arz` | `431e64e1…73a01e292` |
| `…/gdx2/database/GDX2.arz` | `13fa0b93…0dd81a072` |
| `…/gdx3/database/GDX3.arz` | `e990e126…c97d6a2ae4` |

The record side runs on the **Edition-III overlay stack** — the same basis `pm2_tg2_pet_chain.csv` was
emitted on, because this lap performs that walk pointed at a different `Class`. § 7 publishes a
**cross-edition diff** against the `grim-dawn` pin D-8 used, so the choice is checked rather than assumed.

**One declared input that is not read off a record on this lap:** `player level = 100`, **parsed at run
time** from `data/kc2/pm2_measured_player_sheet.csv` row `level` (three-way agreement: screenshot 495 +
screenshot 508 + gdc header). Never typed into the code.

**Display-layer guard honoured:** no tooltip, no `tags_ui.txt` join. Every gameplay rule below is read off
an instruction body or a DBR field.

---

## § 0 · VERDICT TABLE

| target | verdict | one line |
|---|---|---|
| **`MD-B3-1`** the two summon BODY records | **DECODED — both, including the Guardian** | the Guardian's body was never missing: `summon_celestialguardian1.dbr` carries a **26-entry `spawnObjects` array**, `records/skills/playerclass09/pets/celestialguardian_NN.dbr`, indexed by skill rank. At `rank_eff = 2` the body is `celestialguardian_02.dbr`. **`D-3 R-6` and `C-B3-3` CLOSE.** |
| **⚑ the finding under `MD-B3-1`** | **`C-B3-2` IS FALSE AS A DBR CLAIM, AND `C-B3-1` IS TRUE FOR A REASON NOBODY MODELLED** | the summons have **full attack surfaces** (Deathstalker 5 slots, Guardian 1) with real damage rows — but **both bodies carry `invincible = True`**, and that flag early-returns **five** damage/DoT/**control**/debuff entry points in `Game.dll`. Summons are immortal **in the shipped game**, not just in the sim. |
| **`MD-B3-2` (a)** does `RequestReleasePet`'s occupant call `StopCurrentSkill`? | **DECODED — NO** | the chain ends in `KillMe@ControllerCombat` **on the pet**. `StopCurrentSkill@SkillManager` has exactly **7** call sites image-wide and **0** address-takes; none is in this lane. **`K-11` ANSWERED: releasing a pet does not break the channel.** |
| **`MD-B3-2` (b)** slot 76's `UseSkill` `IMPL` verdict | **DECODED — `PERMITTED-EXCEPT-WARM-UP`** | the occupant refuses **iff the channelled skill's `Skill+0x44c == 1`** — the **warm-up** phase (`D-8 R-D8-3`'s own field). While EoR is actually spinning (`+0x44c == 2`) it **tail-forwards to Idle's body**. ⚑ **The Guardian of Empyrion IS castable mid-channel.** B-3's 2,567 `UNDECIDED` resolve. |
| **`MD-B3-3`** player-pet controller class + Confusion/Fear/Taunt | **DECODED, THREE LAYERS, AND THE ANSWER IS OVER-DETERMINED** | all four pet controller records declare **`Class = ControllerMonster`**; `ControllerPet` (if instantiated instead) is a *bare `jmp`* to `ControllerMonster`'s state registration and is byte-identical at every control slot. `Pet`'s body vtable carries **`CombatExertInfluenceConfusion@Monster`** where `Player` carries the `ret 4` stub ⇒ **the route is live on a pet and dead on a player**. **`R-D8-2` RESOLVED; `K-2`'s refusal was correct and is now decoded, not declared.** |

**Machine-readable products (this directory)**

| file | rows | what |
|---|---:|---|
| `d9_summon_bodies.csv` | **216** | `MD-B3-1`. One row per measured body parameter × summon, each with `grade` + `source_record_or_rva` + `extraction_method`. Groups: `chain / body / bio / attack_slot / passive / resist / swing / UNDERIVABLE`. |
| `d9_call_site_xrefs.csv` | **14** | `MD-B3-2`. The two verdicts as instruction chains — 7 links for (a), 7 for (b) — every link an RVA. |
| `d9_pet_control_routing.csv` | **107** | `MD-B3-3`. Record layer → RTTI layer → body-vtable layer → controller-vtable layer → the invincible gate. |
| `d9_digests.json` | — | product digests + the five substrate digests + the parsed player-level input. |
| `evidence/step*.txt` | 39 files | every raw listing and scan, unedited. |

---

## § 1 · `MD-B3-1` — THE GUARDIAN'S BODY WAS NEVER MISSING

`D-3 R-6` searched `records/skills/devotion/**` for a `Skill_SpawnPet` and found only item skill-modifiers.
`B-3 B3-P17` superseded that by pinning the **class** skill instead. Following *that* record one hop is the
whole decode:

```
records/skills/playerclass09/summon_celestialguardian1.dbr        (gdx2)  Class = Skill_TargetedSpawnPet
  petLimit      [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3]     <- 26 ranks
  petBurstSpawn [2, … same shape … ,3,3,3]
  spawnObjects  [ records/skills/playerclass09/pets/celestialguardian_01.dbr,
                  …_02.dbr, … , …_26.dbr ]                                <- 26 BODIES, one per rank
```

**The index rule is decoded, not guessed.** `SpawnPet@Skill_SpawnPet` (`0x0041c850`) does exactly two
lookups before it spawns anything:

```
0x0041c884   call [eax+0x0e4]   ; Skill vtable +0xe4 = GetCurrentLevel@Skill      -> the RANK
0x0041c893   call GetWeightedSpawnObject@Skill                                     ; weighted variant
0x0041c8ae   call [eax+0x154]   ; Skill vtable +0x154 = GetSpawnObject@Skill(rank)
```

`rank_eff = 2` (`pm4g_defensive_actives.csv`, `rank_basis = "DERIVED: allocated+1"`) ⇒
**`celestialguardian_02.dbr`**. The chain **self-checks**: body `NN` carries `skillLevel1 = skillLevel3 = NN`
for its innate and its blade-arc. A census of all 26 bodies (`evidence/step2_bodies.txt`) shows they differ
in **exactly two fields** — `skillLevel1` and `skillLevel3`, `1…26` — and are **identical in every other
field**, including bio, controller, `invincible` and animation table. *The 26 "bodies" are one body and a
rank ladder.*

The Deathstalker needs no such step: `spawnObjects` is the scalar
`records/skills/itemskillsgdx1/pets/itempet_deathstalker_a01.dbr`.

### 1.1 The measured body table

Both bodies: `Class = PetPlayerScaling`, `templateName = database/templates/petplayerscaling.tpl`,
`monsterClassification = Champion`, `factions = faction_player`, `causesAnger = False`,
`angerMultiplier = 0.0`, `actorHeight = 2.0`, **`invincible = True`**, `charLevel = 'charLevel*1'`.

| | **Guardian of Empyrion** | **Deathstalker** |
|---|---|---|
| body record | `…/playerclass09/pets/celestialguardian_02.dbr` (gdx2\|gdx3) | `…/itemskillsgdx1/pets/itempet_deathstalker_a01.dbr` (gdx1) |
| bio record | `…/playerclass09/pets/bio_celestialguardian_01.dbr` | `…/itemskills/pets/bio_nemesis.dbr` |
| `characterLife` | `((charLevel*12)^1.29)+35` | `((charLevel*28)^1.3)+50` |
| `characterOffensiveAbility` | `(charLevel*9)+90` | `(charLevel*6)+50` |
| `characterDefensiveAbility` | `(charLevel*5)+25` | `(charLevel*5)+25` |
| `characterMana` | `500` | `((charLevel*15)^1.2)+50` |
| `characterLifeRegen` | `0` | `(((charLevel*90+10) + lifeRegen))*elapsedTime` |
| STR / DEX / INT | `0` / `0` / `0` | `(cL*6)+30` / `(cL*8)+50` / `(cL*8)+30` |
| **life @ charLevel 100** | **9,413.725121** | **30,340.430151** |
| **OA @ 100** | **990.0** | **650.0** |
| **DA @ 100** | **525.0** | **525.0** |
| mana @ 100 | 500.0 | 6,526.039826 |
| `characterAttackSpeed` | `0.8999999761581421` | `1.149999976158142` |
| `characterSpellCastSpeed` | `1.0` | `1.149999976158142` |
| `characterRunSpeed` | `1.2000000476837158` | `1.2000000476837158` |
| anim table | `anm_celestialguardian.dbr` | `anm_manticore.dbr` |
| unarmed weighted base | **0.633333 s** (2 anims, 19+19 frames @30fps) | **0.933333 s** (3 anims, 25+26+33) |
| **basic swing period** | **0.703704 s** | **0.811594 s** |
| armour skill | `armorpets04` @ rank 100 ⇒ `defensiveProtection = 1225.0` | `armorpets03` @ rank 100 ⇒ `1021.0` |
| **n attack slots** | **1** | **5** |
| controller | `controller_celestialguardian_aggressive.dbr` (single) | `controller_hellhound_normal` + `_aggressive` + `_defensive` |

Swing period uses the **identical method `pm2b_petchain` uses** for the 128 monster pets — weighted
`unarmedAttackAnim{1,2,3}` frame counts from `anm_index.json` at 30 fps, divided by
`characterAttackSpeed`. Nothing new was invented for the player-pet case.

### 1.2 ⚑ The attack surfaces exist. `C-B3-2`'s premise was a *search* result, not a *record* result.

`C-B3-2` reads *"No attack slots, no damage rows, no OA/DA/swing period."* Every one of those exists on
disk. Read off the pinned archives (`d9_summon_bodies.csv`, group `attack_slot`):

**Deathstalker — five slots, all `skillMaxLevel = 1`, all resolved at rank 1:**

| slot | record | class | damage |
|---|---|---|---|
| `basic` | `petskill_deathstalker_basicattack` | `Skill_AttackWeapon` | phys 130 · poison 130–215 · bleed 70 / 3 s |
| `special1` | `…_maul` | `Skill_AttackWeapon` | same magnitudes, `skillTargetNumber 3`, `skillTargetAngle 90°`, anim `Slam` |
| `special2` | `…_tailstrike` | `Skill_AttackWeapon` | phys 177 · poison 177 · bleed 122 / 3 s |
| `special3` | `…_shadowstrike` | `Skill_AttackWeaponBlink` | phys 250 · poison 250–388 · bleed 100 / 3 s, `distanceProfile Long` |
| `special4` | `…_roar` | `Skill_AttackRadius` | phys 130 · poison 130–215, `skillTargetRadius 6.0 m` |
| `buff_self` | `…_auraofdarkness` | `Skill_BuffRadiusToggled` | `instantCast True` |

**Guardian of Empyrion — one slot, rank-2 cell of a 26-rank array:**

| slot | record | class | damage @ rank 2 |
|---|---|---|---|
| `basic` | `petskill_celestialguardian_bladearc1` | `Skill_AttackWeapon` | phys **33–69** · fire **25** · burn **16 / 3 s**, `skillTargetNumber 5`, `skillTargetAngle 180°`, anim `FireArc` |
| `buff_self` | `petskill_celestialguardian_celestialwrath1` | `Skill_BuffRadiusToggled` | **`skillLevel = 0` on the body** — see § 6 `R-D9-3` |

> **What this changes for B-3.** `C-B3-2`'s **measurement** (the `PRESENT_INERT` stripped digest is
> byte-identical to fold-absent, so *this sim's* summons deal zero) is untouched and remains correct.
> What is now wrong is the **reason given**: it is not that the records are absent. They are present and
> fully specified. A follow-up build **can** make the summons damage sources, and § 1.1 + § 1.2 are the
> whole input set for the Deathstalker. For the Guardian the blade-arc is rank-indexed and its
> pet-modifier chain is a named residual (`R-D9-3`).

### 1.3 ⚑ THE FINDING OF THE LAP — `invincible = True`, and what that byte actually does

Both bodies carry the DBR field `invincible = True`. It is not decorative and it is not a display flag.

**Load:** `Load@Character` reads the literal `"invincible"` (VA `0x104f4b9c`) through
`LoadTable::GetBool(name, default = 0)` and writes the result to **two** bytes:

```
0x00043d0a   mov byte ptr [edi + 0x1845], al     ; IsInvincibleInDbr@Character (0x00059c90)
0x00043d17   mov byte ptr [edi + 0x1844], al     ; IsInvincible@Character     (0x00059c80)
```

**Read:** `IsInvincible@Character` is `Character` vtable **slot 262 (`+0x418`)**, inherited unchanged by
`Monster`, `Pet` and `PetPlayerScaling`. (`Player` overrides it at `0x0031b090` to OR in `IsPlayingVideo`.)

**Consumers — byte-exact `disp32 == 0x418` scan over `.text`, 66 instructions, all decoded
(`evidence/step36_isinvincible_callsites.txt`); five of them are this gate:**

| gate | RVA of the vtable load | effect when the flag is set |
|---|---|---|
| `SubtractLife@Character` | `0x000542b4` | early-return — **no life loss** (bypassed by a `force` bool at `[ebp+0x10]`; a second immunity byte `Character+0x1846` refuses immediately after) |
| `SubtractLife@SkillManager` | `0x004405f1` | early-return — **no life loss** |
| `AddDamage@DurationDamageManager` | `0x00208a53` | early-return — **no DoT is enrolled** |
| **`AddFixedDamage@DurationDamageManager`** | **`0x00208d46`** | early-return — ⚑ **NO CONTROL BUCKET IS ENROLLED.** This is the function that fills the fixed-damage buckets `UpdateFxAndInfluence` elects from (D-8 § 3.1) |
| `DebufTarget@Character` | `0x0005302f` | early-return — **no debuff transfer** |

**And the aggro shape is deliberate.** `IsTargetable@Monster` (`0x002dc780`):

```
0x002dc783  cmp byte ptr [esi + 0x1845], 0   ; invincible-IN-DBR
0x002dc78a  je  +0x10                        ;   no  -> al = IsInvincible()   (vtable +0x418)
0x002dc78c  xor al, al                       ;   YES -> al = 0, SKIP the runtime test
0x002dc79a  cmp byte ptr [esi + 0x182e], 0 ; je RETURN-FALSE
0x002dc7a4  test al, al ;                     jne RETURN-FALSE
0x002dc7a8  mov al, 1 ; ret                   ; TARGETABLE
```

A body that is invincible **by DBR declaration** takes the `xor al,al` limb and therefore **stays
targetable**. Invincible-by-declaration means **draws attacks, takes none.** That is the shipped
aggro-sink shape, written into the engine on purpose.

> **What this does to B-3's ledger:**
> * **`C-B3-1` (pet life) — the refusal is RIGHT, and the price shrinks.** B-3 wrote *"Under `DIVERT_MAX`
>   the pets are immortal, which is why that arm is an upper bound and not an estimate."* Immortality is
>   **not a modelling artefact** — it is `invincible = True` on both bodies, enforced at five gates.
>   The `DIVERT_MAX` arm's immortality is **faithful**; what remains an upper bound is only the
>   *diversion fraction*, not the *survival of the diverter*. A re-grade of the band's upper limb is owed
>   and it belongs to gamora, not to me.
> * **`S-B3-3` (summons as aggro sinks, ↑ survival) is now DECODED rather than assumed.** Targetable +
>   invincible is exactly the modelled shape.
> * **`S-B3-5`'s "↓ damage and ↑ tanking simultaneously — an asymmetry, declared"** is half retired: the
>   ↑-tanking limb is the shipped rule. The ↓-damage limb is this sim's choice, and § 1.2 shows the
>   records to undo it.

### 1.4 ⚑ The difficulty pak: `Class` dispatch decoded, and player summons get **neither** 580 nor `G`

Lap E measured (Q1/Q2) that a **monster-summoned** pet takes both the Ultimate `+580 %` cell and the
Crucible wave term `G`, and attributed it to `Class`-scoped pak dispatch. This lap decodes the mechanism
and finds it is **class dispatch by C++ vtable override**, not by a lookup:

| override | reads | folds `GetChallengeAdjustment` (the Crucible `G`)? |
|---|---|---|
| `ContributeGameBalanceCharAttributes@Monster` `0x002d9ab0` | `gGameEngine + 0x1400` (monster pak) | **YES** — `0x002d9ae1`, gated on `esi+0x30e0` |
| `ContributeGameBalanceCharAttributes@Pet` `0x00315f90` | `gGameEngine + 0x19f0` (**pet** pak) | **NO — one call, nothing else** |
| `ContributeGameBalanceCharAttributes@Player` `0x0032b5b0` | `gGameEngine + 0x16f8` (player pak) | NO |
| `…@PetNonScaling` | — | the whole family is overridden to the `ret`/`ret 8` stubs: **no game-balance contribution at all** |

`PetPlayerScaling` has **no** `ContributeGameBalance*` override — vtable slot 225 (`+0x384`) resolves to
`…@Pet` on both `??_7Pet@GAME@@6BObject@1@@` and `??_7PetPlayerScaling@GAME@@6BObject@1@@`.

⇒ **A player summon runs the `Pet` limb: the pet pak only, and no Crucible wave term.** This *retro-lights*
Lap E rather than contradicting it — Lap E's 128 bodies carry `Class = Monster`, so they run the `Monster`
limb and correctly receive both. The two populations were never the same population.

**What is NOT closed:** the 12-cell index selection for Crucible-Ultimate-solo was not re-derived on this
lap. Lap E publishes cell 8 = `15.0` for the pet pak. Row `difficulty_pak_cell_index` in
`d9_summon_bodies.csv` reads **`UNDERIVABLE-WITH-PATH-NAMED`** with that path named. **Do not fold 15 %
without re-deriving the index.**

### 1.5 The one level input this lap could not measure

`SpawnPet@Skill_SpawnPet` (`0x0041c850`) contains **no `SetLevel` call**. The pet is `Load()`ed from its
record and then `JoinMe@Monster` (Character vtable `+0x30c`, called at `0x0041ca9d`) binds it to the
caster. `GetCharLevelGapFixer@Pet` (`0x00009470`) is `xor eax,eax; ret 4` — **zero gap fix**.

So every `*_at_charLevel_100` figure in § 1.1 is graded **`INFERRED-WITH-EVIDENCE`**, on three legs:
(1) the class is literally `PetPlayerScaling`; (2) the gap fixer is zero; (3) Lap E **measured** owner-level
binding for the `Class = Monster` sibling. **Path to make it MEASURED, named in the CSV:** decode
`JoinMe@Monster` (`0x002d5200`) and the leader-level read it performs, **or** read a live Guardian's level
out of a save/GDC block — *not* a tooltip (display-layer guard).

---

## § 2 · `MD-B3-2` (a) — RELEASING A PET DOES NOT BREAK THE CHANNEL. `K-11` IS ANSWERED.

Seven links, each an instruction (`d9_call_site_xrefs.csv`, `target = MD-B3-2a`):

```
1.  ControllerPlayerStateIdle::RequestReleasePet          0x0011ff60
       push ebp; mov ebp,esp; pop ebp; jmp 0x0011f0d0          <- a pure forwarder
2.  DefaultRequestReleasePetAction@ControllerPlayerState   0x0011f0d0
       push 0x14 ; call operator new
       mov dword ptr [edi], 0x1058e0f4                          <- ??_7ReleasePetConfigCmd
3.    call dword ptr [eax+0x1a4]                                <- queue the config cmd
      mov al, 1 ; ret 8                                         <- ALWAYS returns true
4.  Execute@ReleasePetConfigCmd                            0x000a9580
       ObjectManager::Get<Character>([ebx+0xc])   -> esi         (classInfo@Character  0x107ff618)
       ObjectManager::Get<ControllerCombat>([esi+0x1120]) -> edi (classInfo@ControllerCombat 0x107ff510)
       ; reads [esi+0xa38] (current life, double) vs GetLifeLimit@CharacterBio * [esi+0x1d84]
       ; if the bool arg [ebx+0x10] is set, also sets [esi+0x1dcc] = 1
5.    call dword ptr [eax+0x88]                            0x000a9614
       ; controller vtable +0x88 = KillMe@ControllerCombat  0x000eeab0, IDENTICAL on
       ; ControllerPlayer / ControllerMonster / ControllerPet / ControllerAlly
6.  StopCurrentSkill@SkillManager                          0x0043ea00
       E8/E9 rel32 xref scan over .text  -> 7 call sites
       image-wide 4-byte VA scan          -> 0 address-takes
7.  VERDICT: NO.
```

**The seven callers of `StopCurrentSkill`, in full** (`evidence/step27_stopcurrentskill_xrefs.txt`):

| caller | RVA |
|---|---|
| `Execute@MoveToAction` | `0x0006c6bf` |
| `Execute@JumpAttackAction` | `0x0006de19` |
| `Execute@EvadeAction` | `0x0006e5dd` |
| `Execute@TakeStunAction` | `0x0006f172` |
| `Execute@TakeKnockdownAction` | `0x0006f2e2` |
| `Execute@TakeSleepAction` | `0x0006f5b2` |
| `Execute@ImmobilizeAction` | `0x0006f722` |

`ReleasePetConfigCmd::Execute` is not among them, and a call-target audit of all four bodies in the lane
(`evidence/step27`, bottom) shows no path to it. **`C-B3-4` discharges: the request is PERMITTED
mid-channel (D-8) and the consequence is a `KillMe` on the pet, touching nothing on the player's
`SkillManager`.** The baton row is *"pet release is free during a channel"*.

> ⚑ **Unasked, in-family, and load-bearing for the baton.** That same seven-caller census re-derives D-8's
> latch mechanism *and extends it*: D-8 § 4.3 named only the four control actions. The list also contains
> **`MoveToAction`, `JumpAttackAction` and `EvadeAction`.** **A player who clicks to move, jump-attacks or
> evades breaks their own EoR channel by the identical mechanism** — and by D-8 § 4 that drops
> `defensiveCrowdControl +25`. A Godot build that lets the player walk while spinning gets the CC ladder
> wrong. Layer-1 row owed: `channel_breaks_on_self_locomotion`.

---

## § 3 · `MD-B3-2` (b) — ⚑ SLOT 76 MID-CHANNEL IS **PERMITTED-EXCEPT-WARM-UP**

B-3 § 0.3 carried the Guardian's mid-channel availability as **UNDECIDED**, 0 casts / 2,567 opportunities,
because `IMPL` is neither permission nor refusal (`D-B2app-3`). The occupant is thirteen instructions long
and every one of them resolves.

```
RequestSkillAction@ControllerPlayerStateUseSkill              0x00122f50   (vftable +0x130, slot 76)

 0x00122f56  mov ecx,[esi+4] ; call GetCurrentStateData@ControllerAI
 0x00122f5e  push [eax+8]                       ; the state-data's actor id
 0x00122f61  call ObjectManager::Get(...)
 0x00122f69  call 0x0000d4f0                    ; RTTI cast, target = classInfo@Skill (VA 0x107ff570)
 0x00122f72  je  DEFAULT                        ; no current skill -> fall through
 0x00122f76  mov eax,[eax+0x2b0] ; call eax      ; Skill vtable slot 172
 0x00122f80  je  DEFAULT
 0x00122f82  xor al,al ; ret 0x14               ; <- REFUSE
 DEFAULT:
 0x00122f9a  call DefaultRequestSkillAction@ControllerPlayerState   0x0011e1d0
```

`0x0011e1d0` **is Idle's occupant.** `RequestSkillAction@ControllerPlayerStateIdle` (`0x0011ff30`) is a
three-instruction forwarder to the same address. So the fall-through limb is `PERMITTED` **exactly**, not
approximately.

**The predicate at `Skill` vtable `+0x2b0`.** Census over all 141 `??_7Skill*@GAME@@6B@` vftables
(`evidence/step13_skill2b0.txt`): 118 carry `IsActive@Skill` = `xor al,al; ret` (constant false ⇒ always
permitted). `Skill_AttackRadiusSpin` — **Eye of Reckoning** — carries
`GetWarmUpWasActive@Skill_AttackRadiusGrow`:

```
0x003e96f0   cmp dword ptr [ecx + 0x44c], 1
0x003e96f7   sete al
0x003e96fa   ret
```

`Skill+0x44c` is the field **D-8 named in `R-D8-3`**: *"the other half of `IsRunning`: `0`/`1`/`2` = idle /
warm-up / running."* The predicate is true **only in warm-up**.

> ⚑ **VERDICT — `MD-B3-2` (b): the Guardian of Empyrion IS castable while the player channels EoR.**
> Slot 76 refuses only during the channel's **warm-up** window (`+0x44c == 1`); once the disc is spinning
> (`+0x44c == 2`) the request is handed to Idle's body unchanged.
>
> **Consequence for B-3's ungraded finding (a).** The 2,567 `UNDECIDED` opportunities are not undecided
> any more. They split on the pilot's warm-up phase, which the fold does model (`Skill+0x44c` is exactly
> the quantity `R-D8-3` left open). The Wave-4 baton row under the `J-9` capability/measurement split
> should read **capability present AND available**, with the measurement still 0 because *this sim's pilot
> never issues the cast* — a pilot-model gap, no longer an engine-rule gap.
>
> **`C-B3-7` gets sharper, not weaker.** The `instantCast`-absent ⇒ non-instant reading still decides the
> Guardian's route (76 vs 77). What changes is the *cost of being wrong*: both routes are now permitted
> mid-channel, so the flip only moves the five hard control states (`Stunned / Sleep / Immobilized /
> KnockedDown` refuse at slot 76; slot 77 permits everywhere).

**Full slot-76 column, re-derived on this lap's own basis** (`evidence/step11_slots76_59.txt`, 16 states):

| state | slot 76 occupant | verdict |
|---|---|---|
| Idle · MoveTo | `…Idle` `0x0011ff30` | PERMITTED |
| **UseSkill** | `…UseSkill` `0x00122f50` | **PERMITTED-EXCEPT-WARM-UP** |
| Stunned · Sleep · Immobilized · KnockedDown · Dying · Respawning | `0x0005e070` (`xor al,al`) | REFUSED |
| Trapped | `…Trapped` `0x00123c30` | IMPL (not this lap's question) |
| ChargeToUseSkill · MoveToUseSkill | `…MoveToUseSkill` `0x001216f0` | IMPL |
| MoveAndUseSkill | `…MoveAndUseSkill` `0x001225f0` | IMPL |
| Evade · JumpToUseSkill | `…JumpToUseSkill` `0x00122070` | IMPL |
| UseSkillWhileTrapped | `…UseSkillWhileTrapped` `0x00124220` | IMPL |

Slot 59 (`RequestReleasePet`) is `0x0011ff60` — Idle's body — in **14 of 16**; only `Dying` and
`Respawning` override it (to `0x0002ffe0`). Slot 77 is Idle's body in 13 of 16.

---

## § 4 · `MD-B3-3` — THE PET-SIDE ROUTE IS LIVE. THE PLAYER-SIDE ZEROS MUST NOT TRANSFER.

### 4.1 Which controller class

**Record layer, MEASURED.** All four pet controller records declare `Class = ControllerMonster`:

| record | `Class` | `FleeBehavior` | `ViewDistance` | `MaxPursuitDistance` | `TeleportToLeaderDistance` | `DodgeChance` | `min/maxSwingPause` |
|---|---|---|---:|---:|---:|---:|---|
| `controller_hellhound_normal` | `ControllerMonster` | `NeverFlee` | 14.0 | 18.0 | 23.0 | 0 | 0.0 / 0.0 |
| `controller_hellhound_aggressive` | `ControllerMonster` | `NeverFlee` | 18.0 | 20.0 | 23.0 | 0 | 0.0 / 0.0 |
| `controller_hellhound_defensive` | `ControllerMonster` | `NeverFlee` | 8.0 | 16.0 | 18.0 | 0 | 0.0 / 0.0 |
| `controller_celestialguardian_aggressive` | `ControllerMonster` | `NeverFlee` | **18.0** | **15.0** | **15.0** | 0 | 0.0 / 0.0 |

This **re-derives `C-B3-6`'s three hellhound stances exactly** (14/18/8, 18/20/16, 23/23/18, swing-pause 0,
`NeverFlee`) on an independent read, and **adds the Guardian's** — which B-3 did not have, and which is a
**single** controller (no aggressive/defensive variants: `controllerAggressive`/`controllerDefensive` are
absent on `celestialguardian_02.dbr`). ⚑ **`B3-P6`'s Fleeing-inert verdict is re-lit from the pet side:
`FleeBehavior = NeverFlee` on 4/4 pet controllers, the Guardian's included.**

**And the answer is invariant to which C++ class is instantiated**, which is the honest way to state it:

```
classInfo@ControllerPet + 0x08  ==  classInfo@ControllerMonster      ; ControllerPet : ControllerMonster
RegisterStates@ControllerPet          0x000e8e90 : jmp RegisterStates@ControllerMonster
RegisterTemporaryStates@ControllerPet 0x000e8ef0 : jmp RegisterTemporaryStates@ControllerMonster
```

Both are **bare `jmp`s**. A `ControllerPet` registers **exactly** the `ControllerMonster` state set — 36
names, string-literal exact (`evidence/step26_tempstates.txt`), including **`Confused`, `Scared`,
`Stunned`, `KnockedDown`, `Sleeping`, `Trapped`, `Paralyze`, `Immobile`**. And the control-relevant
controller vtable slots are **byte-identical** across `ControllerPlayer` / `ControllerMonster` /
`ControllerPet` / `ControllerAlly` (`evidence/step24_ctrl_control_slots.txt`): `+0x90/0x94` Begin/EndStun,
`+0xa8/0xac` Sleep, `+0xb0/0xb4` Immobilize (= Freeze `0x2d` / Petrify `0x2e`), `+0xb8/0xbc` Trap — all
`0x0f6ad0 / 0x0f6b00 / 0x0f6bf0 / 0x0f6c20 / 0x0f6a10 / 0x0f6a40 / 0x0f6a70 / 0x0f6aa0` on all four. That
is D-8's `R-D8-2` observation confirmed and *explained*: it is one shared forwarder, and it dispatches to
**the current AI state's slot 40** — which for a pet is a `ControllerMonsterState*`, not a
`ControllerPlayerState*`. **`R-D8-2` is resolved.**

### 4.2 Confusion / Fear / Taunt: player-side stub vs pet-side real

`Pet : Monster` in the RTTI (`classInfo@Pet + 0x08 == classInfo@Monster`), and `PetPlayerScaling`'s own
vftable inherits `Pet`'s at every one of these slots.

| family | Character vtable slot | **Player** | **Pet / PetPlayerScaling** | **Monster** |
|---|---|---|---|---|
| **Confusion** | `+0x3c8` | `0x000084d0` — the shared **`ret 4` stub** | **`0x002d9670 CombatExertInfluenceConfusion@Monster`** | same as Pet |
| Fear | `+0x3c4` | `0x00054690 CombatExertInfluenceFear@Character` | same | same |
| Taunt | `+0x3cc` | `0x000546d0 CombatExertInfluenceTaunt@Character` | same | same |

Fear and Taunt then route through the **controller**, and *that* is where the player/pet split lives:

| controller slot | **ControllerPlayer** | **ControllerMonster / ControllerPet / ControllerAlly** |
|---|---|---|
| `+0x84` (Fear) | `0x0000f100` — **`ret 8` stub** | `0x000f6c50 ScareMe@ControllerMonster` — **real** |
| `+0x8c` (Taunt) | `0x0000f100` — **`ret 8` stub** | `0x000f9c80 TauntMe@ControllerMonster` — **real** |

Both pet-side bodies decoded (`evidence/step24_ctrl_control_slots.txt`):

* **`ScareMe@ControllerMonster`** — asks the current AI state's `+0xd0` whether it accepts; if the incoming
  float exceeds the cached `Controller+0x530`, latches the new value and drives the state change.
* **`TauntMe@ControllerMonster`** — `if (InPursuitRange@ControllerMonster(id) [0x000fb7a0]) AddAnger@AngerManager(id, amount, forced=true)`.
  **Taunt on a pet is anger, not a state.**
* **`CombatExertInfluenceConfusion@Monster`** — resolves `this+0x1120` to the controller and tail-jumps to
  the current AI state's `+0x9c` (= `Confused`), which the pet's state set registers.

> ⚑ **`K-2` / `C-B3-5` VERDICT: the player-side zeros are NOT the pet-side zeros, and now it is decoded.**
> D-7 § 3.4 ruled Confusion/Fear/Taunt **NO-OPS on the player**. On a pet **all three reach a real body**.
> `B3-P14`'s raise-on-route enforcement was the correct call: a silent transfer would have been a
> fabricated immunity. **`S-B3-7`'s fourth disposition `PET_ROUTING_UNDECODED` can now be retired to a
> decoded disposition** — the routing is known; what remains is the *magnitude* model.

### 4.3 ⚑ …and yet the number on **these two summons** is still zero — for **three independent reasons**

This is the part a builder must not collapse. There are three distinguishable zeros stacked here, and
`S-B3-7`/`F-2`'s "the baton needs distinguishable zeros" is exactly the discipline that catches it:

| # | zero | where it bites | evidence |
|---:|---|---|---|
| **1** | **NOT-ENROLLED** | `AddFixedDamage@DurationDamageManager` early-returns on `IsInvincible` (`0x00208d46`). **No control bucket is ever created on an invincible body.** Fear (`+0x3c4`) and Confusion (`+0x3c8`) are driven **solely** by `UpdateFxAndInfluence@DurationDamageManager` (`0x0020a19f` and `0x0020a15b`) — the same function D-8 pinned as the sole driver of the involuntary ladder — so both are foreclosed upstream | `evidence/step37`, `step38` |
| **2** | **RESISTED-TO-ZERO** | both bodies' innate passive (`petskill_deathstalker_passiveproperties` / `petskill_celestialguardian_innate01`) carries `defensiveConfusion 500`, `defensiveFear 500`, `defensiveConvert 500`, `defensiveTotalSpeedResistance 500`, `defensivePercentCurrentLife 500`, `defensiveBleeding 88`, all eight `defensive*Duration 33` | `d9_summon_bodies.csv` group `resist` |
| **3** | **NO EMITTER** | the KC2 roster has **no Taunt emitter** — D-7's 143-row control census is Stun 68 + Freeze 35 + Petrify 26 + Confusion 8 + Convert 4 + Disruption 2. *Labelled `inherited-not-re-derived` from D-7 § 3.4; this lap did not recount it* | D-7 § 3.4 |

⚑ **Note what is absent from row 2:** `defensiveStun`, `defensiveFreeze`, `defensivePetrify`,
`defensiveSleep`, `defensiveTrap`, `defensiveKnockdown` are **not present on either innate passive** —
they read `<ABSENT ⇒ 0>` in the CSV. So the *resistance* layer would let Stun and Freeze through on a pet
at 0 % resist. **It is zero #1 — `invincible` — and only zero #1 — that stops them.** A build that models
pet control resistance from the DBR alone and forgets `invincible` will let the board stun the summons.

**And one route is NOT foreclosed by zero #1.** Taunt (`+0x3cc`) has a **different driver**:
`Execute@CombatAttributeInfluenceDamage_Taunt` (`0x000dcf4c`) — hit-resolution side, **not** the
duration-damage ladder. Whether the `IsInvincible` gate covers that path was **not decoded on this lap**.
Row `Taunt (Character +0x3cc)` in `d9_pet_control_routing.csv` reads **`UNDERIVABLE-WITH-PATH-NAMED`**;
the path is *decode the caller of `Execute@CombatAttributeInfluenceDamage_Taunt` (`0x000dcf30`) and test it
for the `+0x418` gate*. **Zero risk on this board (no emitter), non-zero risk on any other.**

---

## § 5 · WHAT THE NEXT BUILD CAN DO WITH THIS

Stated as claims with their grade, so the fold can pick and the gate can check.

1. **`MD-B3-1` CLOSES.** `C-B3-3` discharges — the Guardian's body is `celestialguardian_02.dbr`, reached
   by a decoded index rule. `D-3 R-6` is superseded, not merely bypassed.
2. **Make the summons damage SOURCES from § 1.2** — every magnitude, target count, target angle, radius
   and swing period is `MEASURED`. The Deathstalker is complete. The Guardian's blade-arc is complete at
   rank 2; its pet-modifier chain is `R-D9-3`.
3. **Do NOT make the summons killable SINKS.** `invincible = True` is the shipped rule, enforced at five
   gates. `C-B3-1`'s refusal was right; its *price* narrows — the `DIVERT_MAX` immortality is faithful, and
   only the diversion **fraction** stays an upper bound. **The re-grade is gamora's, not mine.**
4. **`K-11` closes:** `pet_release_does_not_break_channel` (Layer 1, `decoded`).
5. **New Layer-1 row owed, unasked:** `channel_breaks_on_self_locomotion` — `MoveToAction`,
   `JumpAttackAction` and `EvadeAction` all call `StopCurrentSkill` from the identical position as the four
   control actions (§ 2).
6. **The Guardian's mid-channel cell resolves to `PERMITTED-EXCEPT-WARM-UP`** (§ 3). B-3's ungraded
   finding (a) re-scopes from *engine-rule undecided* to *pilot-model gap*.
7. **`K-2` / `C-B3-5` / `R-D8-2` all close together** (§ 4). `PET_ROUTING_UNDECODED` retires to a decoded
   disposition; the magnitude model is what remains.
8. **Three distinguishable zeros, named** (§ 4.3). Any baton row reporting a pet-side control zero must
   carry **which** zero it is. `NOT-ENROLLED` ≠ `RESISTED-TO-ZERO` ≠ `NO-EMITTER`.
9. **`FleeBehavior = NeverFlee` on 4/4 pet controllers, Guardian included** — `B3-P6`'s Fleeing-inert
   verdict re-lit from the pet side, on records B-3 did not have.
10. **Do NOT fold the pet difficulty pak yet** (§ 1.4). The dispatch is decoded; the cell index is
    `UNDERIVABLE-WITH-PATH-NAMED`.

---

## § 6 · RESIDUALS

| id | residual | why it does not block the fold |
|---|---|---|
| **`R-D9-1`** | **`pet_charLevel_binding`** — `SpawnPet` has no `SetLevel`; the binding is `INFERRED-WITH-EVIDENCE` on three legs (§ 1.5). Path named: `JoinMe@Monster` `0x002d5200`, or a save/GDC read | every life/OA/DA figure is published **with its equation**, so a corrected level re-evaluates without re-deriving anything |
| **`R-D9-2`** | **`difficulty_pak_cell_index`** — dispatch decoded, 12-cell index not re-derived on this lap (§ 1.4) | the base figures are pak-free and labelled so; nothing downstream folds a pak yet |
| **`R-D9-3`** | The Guardian's `buffSelfSkillName` (`petskill_celestialguardian_celestialwrath1`) sits at **`skillLevel = 0` on the body**, while `summon_celestialguardian2_petmodifier.dbr` (`SkillSecondary_PetModifier`, rank 13, B-3 § 0.1) names the *same* pet skill. Whether the modifier raises the pet-side rank was not chased | the buff is not an attack slot; § 1.2's damage rows are unaffected |
| **`R-D9-4`** | ⚑ **`PetPlayerScaling` overrides `ContributeMisc*` BACK to `Character`'s** (`0x00316600` etc. are bare `jmp`s to `ContributeMiscCharAttributes@Character`), **suppressing** the `ContributePetBonus*@GameEngine` fold that plain `Pet` performs at `0x00315d99`. So a player-scaling pet does **not** take the player's generic pet-bonus affixes through that path. Where its player scaling *does* enter was not decoded | out of the three commissioned targets; recorded with its address so it is not re-discovered. **Blocks any future "scale summon damage by the player's sheet" build** |
| **`R-D9-5`** | Taunt's driver (`Execute@CombatAttributeInfluenceDamage_Taunt` `0x000dcf30`) was not tested for the `IsInvincible` gate (§ 4.3) | no Taunt emitter in the KC2 roster (D-7 census, `inherited-not-re-derived`) |
| **`R-D9-6`** | `SubtractLife@Character`'s second immunity byte `Character+0x1846`, and the `[vtable+0x228] == 0x15` guard shared by four of the five invincible gates, were seen but not decoded | both are additional *refusal* conditions; missing them can only make a model too permissive in a direction the summons do not exercise (they already refuse on `+0x1844`) |

---

## § 7 · CROSS-EDITION CHECK (the substrate choice, checked not assumed)

`evidence/step39_edition_diff.txt` — every record this lap reads, merged on the `grim-dawn` pin (D-8's,
byte-identical to Edition-I/II) and on Edition-III, field by field:

| record | fields | diffs |
|---|---:|---|
| `itempet_deathstalker_a01.dbr` | 982 / 982 | **0** |
| `summon_celestialguardian1.dbr` | 299 / 299 | **0** |
| `summondeathstalker.dbr` | 32 / 32 | **0** |
| `bio_nemesis.dbr` | 10 / 10 | **0** |
| `bio_celestialguardian_01.dbr` | 10 / 10 | **0** |
| `controller_hellhound_normal.dbr` | 64 / 64 | **0** |
| `controller_celestialguardian_aggressive.dbr` | 64 / 64 | **0** |
| `celestialguardian_02.dbr` | 993 / 1003 | **28 — all in the `skillName*` / `skillLevel*` ITEM-MODIFIER slot list** |

Edition-III adds five item-modifier slots (26…30) and re-orders the block; every added and moved entry sits
at `skillLevel = 0`. **Not one field this lap reports differs**: `Class`, `characterAttributeEquations`,
`controller`, `invincible`, `attackSkillName`, `charAnimationTableName`, `characterAttackSpeed`,
`skillLevel1`, `skillLevel3` are identical across both pins. **The edition choice does not move a single
published figure.**

---

## § 8 · CLEAN NEGATIVES (searched, and the search recorded)

**N-1 — there is no second Deathstalker body.** `summondeathstalker.dbr`'s `spawnObjects` is a **scalar**,
`petLimit = 1` (scalar, not an array). One body, one rank.

**N-2 — the 26 Guardian bodies are not 26 different creatures.** Full field census over all 26
(`evidence/step2_bodies.txt`): **two** fields vary (`skillLevel1`, `skillLevel3`, both `1…26`); every other
field is `CONST` across the set, including `characterAttributeEquations`, `controller`, `invincible`,
`characterAttackSpeed` and `charAnimationTableName`.

**N-3 — `StopCurrentSkill@SkillManager` is never taken as a function pointer.** Image-wide 4-byte VA scan:
**0** occurrences. It sits in no vtable. The 7-caller list is therefore complete for direct dispatch, and
the technique's limit is stated: an indirect `call [reg+disp]` through some other slot was not swept —
but the symbol is `QAEXXZ` (non-virtual `__thiscall`), so there is no slot to sweep.

**N-4 — `PetNonScaling` is not a live class on this board.** Lap E measured `PetNonScaling` **0** records
corpus-wide. This lap adds the binary side: its whole `ContributeGameBalance*` family is overridden to the
`ret`/`ret 8` stubs (`0x000084d0` / `0x0000f100`), i.e. a `PetNonScaling` body receives **no** difficulty
pak at all. Recorded because the name invites the assumption that it means "no player scaling"; it means
**no game-balance contribution of any kind**.

**N-5 — the pet controller records carry `ignorePetsChance` and `petAngerTransference` of their own**
(30 / 30 on the hellhound stances). These govern how **the pet** treats *its* pets, not how the roster
treats the pet. B-3 § 0.4's roster-side census (`0 ×96 · 35 ×69 · 18 ×3 · 15 ×1`) is the relevant one and
is untouched. Recorded because the field names are identical and a join would silently mix them.

**N-6 — `ControllerPet` has no reachable constructor call site.** `E8/E9` xref scan on
`??0ControllerPet@GAME@@QAE@XZ` and `RTTI_new@ControllerPet`: **0** direct calls each;
`RTTI_new@ControllerPet` has exactly one 4-byte occurrence image-wide — its own `classInfo` slot `+0x14`,
i.e. it is reached only through the RTTI factory keyed on the record's `Class` string. The records say
`ControllerMonster`. Honest statement: *the factory dispatch itself was not decoded; the verdict does not
depend on it,* because § 4.1 shows the two classes are identical at every slot this lap reads.

---

## § 9 · METHOD

* PE32 reader + capstone disassembler: `d4b_pe.py`, `d4b_dis.py`, `d8_lib.bounded()` — copied unchanged
  from the D-8 lap directory, so listings stop at the next exported RVA.
* `.arz` reader: `gd_arz_adapter_2026_07_24.py` via `s2_lib.E3` (8-archive last-wins overlay).
* Two independent search techniques wherever a negative is claimed (the D-7 § 6 standard): byte-exact
  `E8`/`E9 rel32` xref scan over `.text`, **and** image-wide 4-byte VA constant scan.
* Byte-exact `disp32` scans for member offsets (`0x1844`, `0x1845`, `0x418`, `0x3c4`, `0x3c8`, `0x3cc`),
  each hit re-disassembled from a candidate instruction start rather than assumed.
* Every RVA printed here was resolved against the 25,091-entry export table at emission time.
* Every RTTI cast helper was identified by resolving its `RTTI_ClassInfo` static to an **exported symbol
  name**, never by inference from the call site.

**Scripts:** `d9_step1_skillrecs.py` · `d9_step2_bodies.py` · `d9_step40_emit.py` (+ the D-8 harness).
**Raw evidence:** `evidence/step1…step39` (39 files; count machine-derived from the directory).

### ⚑ ERRATA on my own listing — `evidence/step22_ctrl_ctrlpet_diff.txt`

That file prints a 200-slot diff of `ControllerMonster` against `ControllerPet` and reports 126 differing
slots. **Slots ≥ 78 in that listing are garbage** and no conclusion here rests on them. The controller
vftables are short and unequal — next-export bounds give `ControllerPlayer` ≤ 76 slots (`0x130` bytes),
`ControllerPet` and `ControllerAlly` ≤ 78 (`0x138`), `ControllerMonster` ≤ 81 (`0x144`) — so the listing ran
off the end of both tables into neighbouring data. The same file's bottom section, `named slots`, reads
**only** offsets `+0x84 … +0xc4` (slots 33–49), which are inside every one of them; that section is sound and
is what §§ 4.1–4.2 cite, cross-checked independently in `evidence/step24_ctrl_control_slots.txt`. Recorded
as an errata rather than deleted, and it is the same class of bug D-8 recorded against the D-7 harness
(`bounded()` exists for the *code* case; there is no equivalent guard for the *vtable* case, and there
should be — a `bounded_vtable()` helper is owed to whoever runs the next lap).
