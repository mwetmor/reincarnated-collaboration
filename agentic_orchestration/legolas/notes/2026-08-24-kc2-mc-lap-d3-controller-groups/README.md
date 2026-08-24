# KC2 MODEL-COMPLETION RUN — Wave 1, piece **D-3**
## The remaining `ControllerMonster` field groups — decoded

**Author:** legolas (`UNKNOWN-RESEARCHER`), 2026-08-24
**Run:** KC2 MODEL-COMPLETION (conductor: gandalf `RUN-CONDUCTOR`); charter
`agentic_orchestration/gandalf/notes/2026-08-24-kc2-model-completion-run-charter.md`; rulings
`…/2026-08-24-kc2-model-pack-reframe-and-gap-rulings.md` (facets (a)–(i), § 2–3).
**Gate:** *"per-group parameter table or UNDECODABLE per field."*
**Law:** **Law 3 — no fitted constants, no invented semantics.** Every rule below is either a
disassembled code path with an address, or a record census with a corpus and a count. Where the
substrate does not answer, the verdict says so in those words.
**Read-only** on `/Users/admin/Games/vendor/**`. Writes confined to this directory.

---

## 0 · VERDICT BOARD — read this first

| # | Group | Verdict | One-line consequence for the model pack |
|---|---|---|---|
| 1 | **Fleeing** (9) | **DECODED · PROVABLY INERT for this fight — triple-locked** | `FleeBehavior = NeverFlee` on **169/169**; `maxFleeCount = 0` on 158/169; `FleeChance = 0` on 159/169. `CanFlee()` fails at gate 1 *and* gate 3. Ship the 9 parameters; ship the state as unreachable-with-reason. |
| 2 | **Attacking** (5) | **DECODED — all five, with the RNG named** | Swing pause = `IGenerate(minSwingPause×1000, maxSwingPause×1000)` ms, **re-rolled every swing** inside `StateAttack::OnUpdate`. This is facet (i)'s swing-pause, closed. |
| 3 | **Dodging** (4) | **DECODED · LIVE for 42/169 monsters — but projectile-only** | Dodge is a reaction to `ProjectileNotification`, not to melee. Fires iff `DodgeChance > rand()%100`; refractory `DodgeDelay` ms. |
| 4 | **SkillUsage** (6) | **DECODED · LIVE and load-bearing** | `DebuffEnemyBehavior = WhenEnemyIsSeen` on 169/169; ally-heal thresholds are **70–80 %**, not the template's 20 %. Feeds D-2 directly. |
| 5 | **PetBehaviour** (6) | **DECODED · LIVE — and it is the facet-(f) counterparty** | `ignorePetsChance` re-rolled every `ignorePetsInterval`(7000 ms) as **`rand() % 101 < chance`** (⚑ modulus 101, not 100). `petAngerTransference` 17/12/22. |
| 6 | **Roaming** (8) | **DECODED · reachable but starved** | Idle→Roam delay = `lo + rand()/32767 × (hi−lo)` ms; Crucible set `lo = hi = 2000` and `RoamDistance = 2.0 m`. Roam is a 2 m twitch on a fixed 2 s clock. |
| 7 | **Patrolling** (3) | **DECODED — and mis-named in the editor** | The three fields fire **only from `StatePatrol::PathFailed()`**. `ChanceToIdleOnPatrol = 0` on 153/169 ⇒ inert here. |
| 8 | **Emote** (3) | **DECODED · PROVABLY INERT for 150/169** | `randomEmoteChance = 0` on 150/169 (Crucible drove 57 controllers 100→0). |
| 9 | **Sleep** (1) | **DECODED semantics · CONDITIONALLY LIVE — one named open check** | `ignoreSleepingEnemies = True` on 94/169, read in `FindEnemy`/`GetMostHatedEnemy`. `ControllerPlayerStateSleep` **exists** — so this is *not* provably inert; it is inert iff no wave-150–160 monster applies sleep. Handed to D-2/B-2. |
| 10 | **Loot** (2) | **DECODED · PROVABLY INERT — and mis-scoped by its name** | Both fields `__ABSENT__` on 169/169 and on 358/359 corpus-wide. These are **FX attach-point names**, not the loot system. Loot still drops (`StateDying::DropLoot`). |
| 11 | **Dying** (1) | **DECODED · PROVABLY INERT** | `dyingSkillCallbackPoint` `__ABSENT__` on 169/169 (and 358/359 corpus-wide) ⇒ no animation-callback-gated death skill on any monster in this fight. Death-spawn chains ride a different record limb. |
| 12 | **RandomAnger** (2) | **DECODED (context; already-decoded group completed)** | `rand()%100 < RandomAngerChance` every `RandomAngerEvaluationTime` ms, gated on current-state==0, then `PickRandomEnemyInView()`. |

### Two findings that were not asked for and change something

**⚑ F-D3-1 — the whole controller surface is Crucible-overridden, not just `ViewDistance`.**
All **77/77** controllers bound by this fight's roster are **owned by a SurvivalMode archive**
(SurvivalMode 30 · SurvivalMode1 25 · SurvivalMode2 12 · SurvivalMode3 10). Diffed field-by-field
against the base-game winner, **every one of the 68 fields moves on at least one controller**;
`ViewDistance` moves on 77/77, `MaxPursuitDistance` on 76/77 (**75.0 → 125.0**, and bosses
**210.0 → 125.0** — the Crucible *shortened* boss leash), `ProjectileAnger` on 69/77,
`EmoteBeforePursuingChance` on 73/77, `RoamDistance` on 66/77, `randomEmoteChance` on 57/77,
`ChanceToIdleOnPatrol` on 49/77. The Lap-U `ViewDistance 15→80` precedent is **not a special case;
it is one row of a wholesale re-tune.** Any baton row sourced from base-game controller values is
wrong for this fight. Full diff: `evidence/d3_override_rows.csv` (5,313 rows).

**⚑ F-D3-2 — a hidden field group the `.tpl` does not expose: `Leader`.**
`ControllerMonster::Load` (`Game.dll` `0x0f6da0`) reads three record fields that appear in
**no** template: `LeaderBehavior` (GetString, default `NeverLead`, → `+0x360`; enum
`NeverLead=0 · LeadOnPatrol=1 · LeadWhenEnemyIsSeen=2 · LeadOnDamage=3`), `LeaderDistance`
(GetFloat, default **5.0**, → `+0x364`), `MaxFollowers` (GetInt, default **4**, → `+0x368`).
Consumers: `CallForFollowers@ControllerMonsterState<ControllerMonster>`,
`StatePatrol::OnBegin`, `DefaultEnemyFoundResponse`, `DefaultAttackedResponse`,
`FindEnemyUpdate`. **Census: `__ABSENT__` on 169/169 rolled AND on 359/359 `ControllerMonster`
records corpus-wide** ⇒ every monster falls to `NeverLead`. Consequence for the state machine:
**`FollowLeader` (#13) and `DefendLeader` (#16) of the 43 states are unreachable for monsters**,
with a decoded reason rather than an assumption. Godot can ship them as declared-absent.

**⚑ F-D3-3 (gift to D-1, not a D-3 claim).** `EmoteBeforePursuingChance` is a **DEAD RECORD
FIELD**: the literal string does not exist in `Game.dll`, `Engine.dll`, `Grim Dawn.exe`,
`Editor.exe` or `DBREditor.exe` (0 hits, all five). Crate *authors* it — the player's own pet
controllers carry `30` — but the engine never reads it. Separately, `ShouldPlayRallyOrAlert`
(`0x0f9ce0`) is fully disassembled below: it is a **one-shot consume-on-read latch on
`this+0x28c`**, not a chance roll and not a record field. D-1's entry condition is therefore
"whoever writes `+0x28c`", and the candidate writer surfaced by the displacement scan is
`DefaultEnemyFoundResponse@ControllerMonsterState<ControllerMonster>`. D-1 owns confirming it.

---

## 1 · Method and provenance

**Three independent evidence layers, joined per field.**

1. **TEMPLATE** — `controllerai.tpl` (base, 12 fields) + `controllermonster.tpl` (derived, 56
   fields) = **68-field surface**, from the shipped `database/templates.arc` bundle at
   `agentic_orchestration/legolas/scratch/2026-08-08-kc2-halt-bundle/tpl/`. Gives name, type,
   group, Crate's own `description` string, and the **editor** default.
2. **RECORD** — the 8-archive layered corpus (`pm4t_arz_2026_08_14.Corpus`, override order
   base → GDX1-3 → SurvivalMode ×4) over `/Users/admin/Games/vendor/grim-dawn-edition-III-20260808/`.
   Roster basis is Lap D's `pm4d_band_b_monster_life.csv`: **`in_rolled_20w` = 169 monster
   records → 77 distinct controllers** (join on the monster record's `controller` field; **0
   unresolved**). Wider populations reported alongside: `in_pool` (663 → 145 controllers) and
   **corpus-wide `Class=ControllerMonster` (359 records)**.
3. **BINARY** — `Game.dll` (sha256 `4876d6bd…`). For each field: locate the name literal, find
   every `push <VA>` in `.text`, resolve to the enclosing export, disassemble the
   `LoadTable::Get*` call to recover the **engine** default and the **object slot**
   (`this+disp`), then scan `.text` for every other instruction touching that displacement to
   enumerate the **consumers**. `objdump` via `pm4s_pe_2026_08_14.PE32`.

**Slot recovery:** 56 of 68 fields resolved to a numeric `this+disp` by automated walk;
the 9 picklists resolved by reading their string-compare chains (§ 3.10); the 3 string fields
(`lootDrop*`, `dyingSkillCallbackPoint`) are `std::string` members with no scalar slot.

**Provenance grades used below** — **[bin]** disassembled code path with an RVA ·
**[rec]** record census with corpus + count · **[tpl]** template declaration ·
**[inferred]** my reading, labelled as such and never mixed into a table cell.

**Digests:** `d3_digests.json` (Game.dll, Engine.dll, all 8 `.arz`, both `.tpl`, roster CSV).
**Scripts:** `scripts/` (10 files, all read-only). **Raw evidence:** `evidence/`.
**Data deliverables:** `d3_roster_controller_params.csv` (per-controller × per-field, with
base-game vs Crucible value and owner archive) · `d3_group_rollup.json` (monster-weighted
value histograms) · `d3_swing_pause_ms.csv`.

**Counting convention.** "**x/169**" = monster-record-weighted (a controller shared by 9 monster
records counts 9). "**x/77**" = distinct-controller-weighted. Both are given where they differ
materially, because the sim spawns monster records but parameterises from controllers.

---

## 2 · The slot map (the model pack's field→memory contract)

`ControllerMonster::Load` @ **`0x000f6da0`** (`?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z`).
Call shape: `mov [esp], <engine default>` · `push <field-name VA>` · `call [vtable+N]` ·
optional `fmul <const>` / `cvttss2si` · `fstp|mov [edi + SLOT]`. `edi = this`.

| Group | Field | Slot | Getter | Engine default **[bin]** | Editor default **[tpl]** |
|---|---|---|---|---|---|
| Fleeing | `FleeBehavior` | `+0x304` | GetString→enum | `NeverFlee` | picklist |
| Fleeing | `FleeTarget` | `+0x308` | GetString→enum | `AwayFromEnemy` | picklist |
| Fleeing | `maxFleeCount` | `+0x30c` | GetInt | **2** | 3 ⚑ mismatch |
| Fleeing | `FleeTime` | `+0x310` | GetInt | 3000 | 3000 |
| Fleeing | `FleeDelay` | `+0x314` | GetInt | **2000** | 2000 |
| Fleeing | `fleeDistance` | `+0x318` | GetFloat | 5.0 | 5.0 |
| Fleeing | `ClearAngerWhenFleeing` | `+0x31c` | GetBool | false | 0 |
| Fleeing | `ResetOriginAfterFleeing` | `+0x3a4` | GetBool | false | 0 |
| Fleeing | `FleeChance` | `+0x2d8` | GetInt | 100 | 100 |
| Attacking | `minSwingPause` | `+0x2f0` | GetFloat **×1000 → int ms** | 0.0 | 0 |
| Attacking | `maxSwingPause` | `+0x2f4` | GetFloat **×1000 → int ms** | 0.0 | 0 |
| Attacking | *(rolled swing timer)* | `+0x2f8` | — | — | *not a record field* |
| Attacking | `RepositionChance` | `+0x3b0` | GetInt | 0 | 0 |
| Attacking | `randomRepositionChance` | `+0x2e0` | GetInt | 0 | 0 |
| Attacking | `LeadChance` | *(int array)* | GetIntArray | — | array |
| Dodging | `DodgeChance` | `+0x2dc` | GetInt | 0 | 0 |
| Dodging | `DodgeDistance` | `+0x3a8` | GetFloat | 4.0 | 4.0 |
| Dodging | `MinDodgeDistance` | `+0x3ac` | GetFloat | **0.0** | 2.0 ⚑ mismatch |
| Dodging | `DodgeDelay` | `+0x510` | GetInt | 5 | 5 |
| SkillUsage | `BuffSelfBehavior` | `+0x324` | GetString→enum | `NeverUseSkill` | picklist |
| SkillUsage | `BuffAllyBehavior` | `+0x328` | GetString→enum | `NeverUseSkill` | picklist |
| SkillUsage | `BuffAllyTargeting` | `+0x32c` | GetString→enum | `BuffClosest` | picklist |
| SkillUsage | `DebuffEnemyBehavior` | `+0x330` | GetString→enum | `NeverUseDebuff` ⚑ | picklist |
| SkillUsage | `healLeaderHealthPercentage` | `+0x358` | GetInt | **0** | 20 ⚑ mismatch |
| SkillUsage | `healAllyHealthPercentage` | `+0x35c` | GetInt | **0** | 20 ⚑ mismatch |
| Roaming | `RoamBehavior` | `+0x320` | GetString→enum | `NeverRoam` | picklist |
| Roaming | `MinRoamDistance` | `+0x39c` | GetFloat | 2.0 | 5.0 ⚑ |
| Roaming | `RoamDistance` | `+0x374` | GetFloat | 10.0 | 10.0 |
| Roaming | `MinTimeBeforeRoam` | `+0x394` | GetInt | — | 3000 |
| Roaming | `MaxTimeBeforeRoam` | `+0x398` | GetInt | — | 10000 |
| Roaming | `MinWanderDistance` | `+0x3a0` | GetFloat | 2.0 | 2.0 |
| Roaming | `WanderDistance` | `+0x370` | GetFloat | 5.0 | 7.0 ⚑ |
| Roaming | `TeleportToLeaderDistance` | `+0x378` | GetFloat | 20.0 | 20.0 |
| Patrolling | `ChanceToIdleOnPatrol` | `+0x37c` | GetInt | **20** | 20 |
| Patrolling | `MinPatrolIdleTime` | `+0x380` | GetInt | **2000** | 2000 |
| Patrolling | `MaxPatrolIdleTime` | `+0x384` | GetInt | **5000** | 5000 |
| Emote | `randomEmoteChance` | `+0x514` | GetInt | 100 | 100 |
| Emote | `randomEmoteMinTime` | `+0x518` | GetInt | 5000 | 5000 |
| Emote | `randomEmoteMaxTime` | `+0x51c` | GetInt | 10000 | 10000 |
| PetBehaviour | `ignorePetsChance` | `+0x56c` | GetInt | 0 | 0 |
| PetBehaviour | `ignorePetsInterval` | `+0x570` | GetInt | 5000 | 5000 |
| PetBehaviour | `petAngerTransference` | *(see § 3.5)* | GetInt | 30 | 30 |
| PetBehaviour | `petTargetLevelRange` | `+0x580` | GetInt | 1000 | 1000 |
| PetBehaviour | `petTargetLeastAttacked` | `+0x584` | GetBool | false | 0 |
| PetBehaviour | `petTargetGreatestHealth` | `+0x585` | GetBool | false | 0 |
| Sleep | `ignoreSleepingEnemies` | `+0x4d9` | GetBool | false | *(blank)* |
| RandomAnger | `RandomAngerChance` | `+0x390` | GetInt | 0 | 0 |
| RandomAnger | `RandomAngerEvaluationTime` | `+0x504` | GetInt | 3000 | 3000 |
| Loot | `lootDropAttachPointName` | *(std::string)* | GetString | `""` | `""` |
| Loot | `lootDropCallbackPoint` | *(std::string)* | GetString | `""` | `""` |
| Dying | `dyingSkillCallbackPoint` | *(std::string)* | GetString | `""` | `""` |
| **Leader (HIDDEN)** | `LeaderBehavior` | `+0x360` | GetString→enum | `NeverLead` | **not in .tpl** |
| **Leader (HIDDEN)** | `LeaderDistance` | `+0x364` | GetFloat | **5.0** | **not in .tpl** |
| **Leader (HIDDEN)** | `MaxFollowers` | `+0x368` | GetInt | **4** | **not in .tpl** |

⚑ Eight fields where the **editor default and the engine default disagree**. The engine default
is the one that governs an absent record field. This matters for `MinDodgeDistance`
(tpl 2.0 vs engine 0.0 — 34/169 monsters have no Dodging block at all) and for the two
`heal*HealthPercentage` fields (tpl 20 vs engine 0).

Full machine-readable map: `evidence/d3_slots2.json` + `evidence/d3_picklist.json`.
Full annotated `Load` disassembly: `evidence/d3_ctrlmonster_load.asm` (1,122 instructions).

---

## 3 · The groups

### 3.1 · Fleeing (9 fields) — **DECODED · PROVABLY INERT (triple-locked)**

**Rule (`ControllerMonster::CanFlee` @ `0x0f6d40`) [bin]:**

```
100f6d43: mov eax, [esi + 0x528]      ; fleeCountSoFar
100f6d49: cmp eax, [esi + 0x30c]      ; maxFleeCount
100f6d4f: jae  -> return FALSE                              GATE 1
100f6d51: cmp dword ptr [esi + 0x52c], 0   ; flee refractory timer
100f6d58: jg   -> return FALSE                              GATE 2
100f6d5a: call [0x104e650c]           ; CRT rand()
100f6d66: idiv 0x64                   ; % 100
100f6d68: cmp edx, [esi + 0x2d8]      ; FleeChance
100f6d6e: jae  -> return FALSE                              GATE 3
          return TRUE
```
`[0x104e650c]` resolves through the import table to **`api-ms-win-crt-utility-l1-1-0.dll : rand`**.
Sole caller: `FindEnemyUpdate@ControllerMonster`.

**Values on this fight's roster [rec]:**

| Field | Slot | 169-weighted value distribution | 77-controller | corpus (359) |
|---|---|---|---|---|
| `FleeBehavior` | `+0x304` | **`NeverFlee` 169/169** | 77/77 | 351/359 |
| `maxFleeCount` | `+0x30c` | **`0` ×158**, `2` ×10, `1` ×1 | 0 ×71 | 0 ×297 |
| `FleeChance` | `+0x2d8` | **`0` ×159**, `50` ×5, `75` ×5 | 0 ×72 | 0 ×311 |
| `FleeTime` | `+0x310` | `0` ×128, `3000` ×40, `3` ×1 | | |
| `FleeDelay` | `+0x314` | `0` ×101, `5000` ×47, `3000` ×17, `10000` ×3, `8000` ×1 | | |
| `FleeTarget` | `+0x308` | `__ABSENT__` ×92, `AwayFromEnemy` ×55, `TowardsAllies` ×19, `TowardsHome` ×3 | | |
| `fleeDistance` | `+0x318` | `0.0` ×96, `8.0` ×34, `10.0` ×18, `5.0` ×13, `16.0` ×5 | | |
| `ClearAngerWhenFleeing` | `+0x31c` | **`False` 169/169** | 77/77 | 358/359 |
| `ResetOriginAfterFleeing` | `+0x3a4` | `False` ×137, `True` ×32 | | |

**Crucible intent, decoded [rec]:** 16/77 controllers were **changed by the SurvivalMode layer to
`NeverFlee`** — 10 from `FleeOnLowHealth`, 5 from `FleeOnDamage`. `maxFleeCount` was driven to 0
on 28/77 and `FleeChance` to 0 on 21/77. Fleeing was **switched off on purpose** for the Crucible.

**Consumers [bin]:** `DefaultLowHealthResponse` · `DefaultAttackedResponse` ·
`DefaultClosestEnemyFoundResponse` · `Attacked@StateAttack` · `FindEnemyUpdate` (entry side);
`DoFlee@StateFlee` · `PickFleePoint@StateFlee` · `OnEnd@StateFlee` · `ResetFleeTimer` (run side).

**⚑ Carve-out — `fleeDistance` is NOT flee-only.** It is also read by
`PickRunToPoint@ControllerMonsterStateScared` [bin]. The **`Scared`** state (#27) is fear-CC
driven and is **not** gated by `FleeBehavior`. So `fleeDistance` remains load-bearing for the
model pack even though `Flee` is unreachable. Whether any actor in this fight applies fear is a
roster-skill question, not a controller question — handed to D-2/B-2.

**Model-pack instruction:** ship all 9 as parameters; ship state `Flee` (#8) as
**unreachable-for-this-roster with the CanFlee gate cited**; do **not** ship `Scared` (#27) as
unreachable on this evidence.

---

### 3.2 · Attacking (5 fields) — **DECODED (all five)**

**Rule A — swing pause (this closes facet (i)'s "swing-pause") [bin].**
Record fields are in **seconds**; `Load` multiplies by the constant at `0x105f5918` = **1000.0f**
and truncates (`cvttss2si`) to **integer milliseconds**.

`ControllerMonsterStateAttack::OnUpdate` @ `0x100600`–`0x10063c`:
```
if (state.committed == 0) {
    if ( controller[0x2f8] <= 0 ) {                 ; swing timer expired
        state.committed = 1
        controller[0x2f8] = IGenerate( controller[0x2f0],   ; minSwingPause ms
                                       controller[0x2f4] )  ; maxSwingPause ms
        AttackEnemyOrReturn()                        ; <- the swing fires
    }
}
```
`[0x104e5544]` resolves to **`Engine.dll : ?IGenerate@RandomUniformLocked@GAME@@QAEHHH@Z`** —
a *locked uniform integer* generator on the global stream at `[0x108080a4] + 0xc04`. The identical
roll is inlined at exactly **4 sites**: `ControllerMonster::Load` (initial),
`ControllerMonster::ResetSwingTimer` (`0x0fca50`), `StateAttack::OnUpdate` (the live re-roll),
and `ControllerMonsterStateTrapped::EnemyFound`. Countdown is decremented in
`ControllerMonster::Update(dt)`; `ZeroSwingTimer` / `GetSwingTimer` / `SkillFailed` also touch it.

**⚑ The pause is re-rolled on every swing, not fixed per monster.** A Godot runtime that samples
once per spawn will produce visibly wrong attack cadence.

**Values [rec]** — monster-weighted `(min_ms, max_ms)` windows, top rows
(full table: `d3_swing_pause_ms.csv`, 78 rows):

| `(min_ms, max_ms)` | monsters | example controller |
|---|---:|---|
| (200, 600) | 22 | `controller_wendigo` · `controller_rhino` · `controller_sandlizard` |
| (500, 1000) | 16 | `controller_swampgolem` · `controller_giant` · `controller_meleetank` |
| (500, 1100) | 13 | `controller_aetherialcorruption` (9 monsters — the single largest block) |
| (0, 300) | 13 | `controller_aetherialbloater` · `controller_aetherialcolossus` · `controller_avian` |
| (649, 1200) | 11 | `controller_basilisk_melee` · `controller_ghost_meleebasic` |
| (400, 600) | 11 | `controller_chthonicrylok` · `controller_gargoyle` |
| (300, 699) | 8 | `controller_swampcrab_melee` |
| … | | range floor `(0,300)`; ceiling `(2000, 3299)` on `controller_skeletoncaster01_slow` |
| **(None, None)** | **2** | `controller_viper_melee` — **no swing-pause block ⇒ engine default 0/0** |

**Rule B — `randomRepositionChance` [bin]**, `StateAttack::OnUpdate` @ `0x100685`:
```
esi = controller[0x2e0]                       ; randomRepositionChance
edx = rand() % 100
state.reposition = (edx < esi)
state.reposition &= virtual_call(controller, vtbl+0xfc)   ; an additional permission predicate
```
The second conjunct is a virtual call whose target class I did not resolve —
**SEMANTICS-PARTIAL, declared**: the roll is decoded, the permission predicate is not.

**Rule C — `RepositionChance` [bin]:** sole consumer is
`ProjectileCollisionCallback@ControllerMonsterStateAttack`, which matches Crate's own template
description ("chance to reposition after blocked projectile attack") — **CORROBORATED**, not
merely quoted.

**Rule D — `LeadChance` [tpl+rec, SEMANTICS-PARTIAL]:** an `int array` ("percent chance to lead
target"). Values are 3-element vectors: `50;75;100` (26 monsters), `0;50;100` (25), `30;50;80`
(18), `30;60;100`, and scalar `0` (28); `__ABSENT__` on 56/169. **The array INDEX is not
decoded** — the load site is an array getter and I did not find a reader that reveals what the
index means (difficulty tier and projectile-range band are both plausible; neither is attested).
**Verdict: field-name and values KNOWN, index semantics UNDECODED-FROM-SUBSTRATE.** Searched:
`ControllerMonster::Load` array-getter call site; `.text` displacement scan; export names
containing `Lead`. Recommended next probe: the `Skill_Attack*Projectile*` aim path.

**Values [rec]:**

| Field | 169-weighted |
|---|---|
| `minSwingPause` | `0.5` ×42, `0.2` ×28, `0.0` ×16, `0.65` ×16, `0.4` ×16, … |
| `maxSwingPause` | `0.6` ×36, `1.2` ×27, `1.0` ×20, `0.3` ×16, `1.1` ×13, … |
| `RepositionChance` | `0` ×133, `100` ×17, `45` ×11, `50` ×4, `65` ×3 |
| `randomRepositionChance` | `0` ×145, `20` ×15, `5` ×6, `25` ×2, `30` ×1 |
| `LeadChance` | `__ABSENT__` ×56, `0` ×28, `50;75;100` ×26, `0;50;100` ×25, `30;50;80` ×18 |

**Crucible delta [rec]:** the Attacking group is **essentially untouched** by the SurvivalMode
layer (3/77 changed on each of `RepositionChance`, `randomRepositionChance`, `minSwingPause`,
`maxSwingPause`; 2/77 on `LeadChance`). Combat micro-tuning is base-game; the Crucible re-tuned
perception, aggro, flee and emote instead.

---

### 3.3 · Dodging (4 fields) — **DECODED · projectile-reaction only**

**Rule [bin]** — `ControllerMonsterState<ControllerMonster,Monster>::DefaultProjectileNotificationResponse(uint projId)`
@ `0x10b3b0`:
```
1010b3d1: eax = controller[0x2dc]              ; DodgeChance  (int -> double -> float)
1010b3f4: call rand ; idiv 100                 ; r = rand() % 100
1010b40e: comiss xmm1(chance), xmm0(r)
1010b411: jbe  -> return                       ; dodge iff DodgeChance > r
          ... resolve the projectile's owner ...
1010b457: movss xmm0, [ecx + 0x3ac]            ; MinDodgeDistance
          ... squared-distance test against the projectile source ...
          ... lateral displacement of DodgeDistance ([eax+0x3a8]) ...
```
**Refractory [bin]:** `ControllerMonster::ProjectileNotification` (`0x0fb320`) ends with
`this[0x50c] = this[0x510]` — i.e. the live dodge cooldown is reset to **`DodgeDelay`** ms on
every projectile notification.

**⚑ Dodging is a projectile evade. There is no melee-dodge path.** The only other consumer of
`DodgeDistance` is `UseSkill@ControllerAIStateT<…>` (a max-distance clamp), not an evade.

**Values [rec]:**

| Field | Slot | 169-weighted | live monsters |
|---|---|---|---|
| `DodgeChance` | `+0x2dc` | `0` ×93, `__ABSENT__` ×34, `50` ×16, `75` ×13, `30` ×11, `70` ×1, `65` ×1 | **42/169 monsters across 26/77 controllers** |
| `DodgeDistance` | `+0x3a8` | `0.0` ×82, `2.0` ×37, `__ABSENT__` ×34, `3.0` ×11, `5.0` ×4, `4.0` ×1 | |
| `MinDodgeDistance` | `+0x3ac` | `0.0` ×82, `2.0` ×37, `__ABSENT__` ×34, `4.0` ×12, `6.0` ×2, `5.0` ×2 | |
| `DodgeDelay` | `+0x510` | `0` ×76, `__ABSENT__` ×34, `5000` ×21, `1500` ×16, `6000` ×11, `3000` ×8, … | |

*Note on the 34 `__ABSENT__`:* those controllers carry **no Dodging block at all** ⇒ they take the
engine defaults `DodgeChance = 0` (never dodge). So the live population is exactly the **42
monsters (26 controllers) with an explicit non-zero `DodgeChance`** — 24.9 % of the roster — and
the remaining 127 never dodge. Per-controller rows: `d3_roster_controller_params.csv`.

**Crucible delta [rec]:** 2/77 (`DodgeDistance`, `DodgeChance`), 4/77 (`DodgeDelay`), 1/77
(`MinDodgeDistance`). Base-game values govern.

---

### 3.4 · SkillUsage (6 fields) — **DECODED · LIVE, and it feeds D-2**

**Picklist enums [bin], from the compare-chains in `Load`:**

| Field | Slot | Enum |
|---|---|---|
| `BuffSelfBehavior` | `+0x324` | `NeverUseSkill=0 · WhenIdle=1 · WhenEnemyIsSeen=2 · WheneverPossible=3` |
| `BuffAllyBehavior` | `+0x328` | same 4 |
| `DebuffEnemyBehavior` | `+0x330` | `NeverUseSkill=0 · WhenIdle=1 · WhenEnemyIsSeen=2` (engine default string is **`NeverUseDebuff`** — a token that matches none of the three compares, so an absent field lands on the fall-through) |
| `BuffAllyTargeting` | `+0x32c` | `BuffClosest=0 · BuffStrongest=1 · BuffWeakest=2` |

**Consumers [bin]:** `BuffSelfBehavior` → `ShouldBuffSelf@ControllerMonsterState<ControllerMonster>`,
`Update@ControllerMonster`, `HandleEvent@StateAttack`, `HandleEvent@StateJumpAttack`,
`DefaultEnemyFoundResponse`, `DefaultAttackedResponse`, `DefaultAllyAttackedResponse`,
`DefaultAllyNeedsHelpResponse`. `BuffAllyBehavior` → `Update@ControllerMonster`,
`DefaultEnemyFoundResponse`, `DefaultAllyNeedsHelpResponse`. `BuffAllyTargeting` → **only**
`ChooseBestAllyToBuff@ControllerMonster`. `healLeader/AllyHealthPercentage` →
`TryToHealAlly@ControllerMonster` (called from `Update@ControllerMonster`) and
`HealAllyWhenAttacked@ControllerMonsterState<ControllerMonster>`.
`DebuffEnemyBehavior` → its own getter only; the getter's callers are virtual/inlined and were
not resolved by a direct-call scan — **the value and the enum are DECODED, the exact dispatch
site is UNRESOLVED**, declared.

**Values [rec]:**

| Field | 169-weighted | 77-controller | corpus (359) |
|---|---|---|---|
| `BuffSelfBehavior` | `WhenEnemyIsSeen` ×111, `WheneverPossible` ×58 | 54 / 23 | 220 / 137 / 2 |
| `BuffAllyBehavior` | `WhenEnemyIsSeen` ×111, `WheneverPossible` ×58 | 54 / 23 | 241 / 116 / 2 |
| `DebuffEnemyBehavior` | **`WhenEnemyIsSeen` 169/169** | 77/77 | 357/359 |
| `BuffAllyTargeting` | `BuffStrongest` ×134, `BuffWeakest` ×35 | 64 / 13 | 307 / 47 / 4 |
| `healLeaderHealthPercentage` | `80` ×64, `75` ×45, `70` ×41, `20` ×14, `66` ×3, `60` ×2 | | |
| `healAllyHealthPercentage` | `80` ×67, `75` ×45, `70` ×41, `20` ×14, `60` ×2 | | |

**⚑ Consequence for D-2 (the 45/58 silent special slots).** Three of the four gates that decide
whether a granted skill *ever fires* live in this group, and all three are **wide open** on this
roster: every monster debuffs on sight; every monster buffs itself and its allies on sight or
better; and the ally-heal threshold is **70–80 % health**, not the editor's 20 %. A monster in
this fight begins healing an ally that has taken **20–30 %** damage. If D-2 is looking for why
45 special slots are silent in the sim, **it is not the `SkillUsage` gate** — that gate is open.
(`healLeaderHealthPercentage` is only reachable when a leader exists, and § F-D3-2 shows no
monster has one — so the *ally* threshold is the live one.)

**Crucible delta [rec]:** 2/77 on each picklist; base-game values govern.

---

### 3.5 · PetBehaviour (6 fields) — **DECODED · LIVE · facet-(f) counterparty**

**Rule — the ignore-pets decision [bin]**, `ControllerMonster::Update(dt)` @ `0x0f634d`:
```
this[0x574] -= dt                          ; ignore-pets countdown
if (this[0x574] <= 0) {
    this[0x574] = this[0x570]              ; ignorePetsInterval (ms)
    call rand ; idiv 0x65                  ; ⚑ r = rand() % 101   (MODULUS 101)
    this[0x578] = (r < this[0x56c])        ; setl, signed  ; ignorePetsChance
}
```
**⚑ The modulus is 101, not 100.** `mov ecx, 0x65` at `0x100f636f` — verified against
`0x64` (=100) at the emote roll `0x100f6560`, the flee roll `0x100f6d61`, the reposition roll
`0x1010068e`, the random-anger roll `0x100f66c5` and the patrol-idle roll `0x1010547b`, all of
which are 100. The pet-ignore roll is the odd one out. Effective probability is `chance/101`:
a controller carrying `35` ignores pets **34.65 %** of the time, and a hypothetical `100` would
be 99.0 %, never 100 %. This is a real engine quirk, not a rounding artefact, and a Godot
runtime that writes `randf() < chance/100` will drift.

**Values [rec]:**

| Field | Slot | 169-weighted | Consumers [bin] |
|---|---|---|---|
| `ignorePetsChance` | `+0x56c` | `0` ×96, **`35` ×69**, `18` ×3, `15` ×1 | `Update@ControllerMonster`, `GetIgnorePetChance` |
| `ignorePetsInterval` | `+0x570` | **`7000` ×168**, `5000` ×1 | `Update@ControllerMonster`, `GetIgnorePetInterval` |
| `petAngerTransference` | — | **`17` ×112**, `12` ×48, `22` ×7, `15` ×1, `27` ×1 | (getter present; store shape is not a scalar `mov` — **slot UNRESOLVED**, value DECODED) |
| `petTargetLevelRange` | `+0x580` | **`1000` 169/169** | `FindEnemy@ControllerMonster`, `GetMostHatedEnemy@ControllerMonster` |
| `petTargetLeastAttacked` | `+0x584` | **`False` 169/169** | same two |
| `petTargetGreatestHealth` | `+0x585` | **`False` 169/169** | same two |

**Reading [inferred, labelled]:** `petTargetLevelRange = 1000` is a no-op width (no level filter),
and both target-preference booleans are off on every monster ⇒ **monster target selection in this
fight is pure anger-ranking**, with the only pet-specific modifier being the periodic
`ignorePets` coin-flip and the `petAngerTransference` share.

**Crucible delta [rec]:** `petAngerTransference` changed on 8/77 (`24 → 22/17/15`); the rest
inherited from base game.

**⚑ Bonus for facet (f) — the player's own summons.** The Deathstalker (relic
`summondeathstalker.dbr` → `itempet_deathstalker_a01.dbr`, `Class = PetPlayerScaling`) binds
**three stance controllers**, all `Class = ControllerMonster`, all owned by `database.arz`
(**no Crucible override**): `controller_hellhound_{normal,aggressive,defensive}.dbr`. Decoded
values (`evidence/d3_petctrl.txt`):

| Field | normal | aggressive | defensive |
|---|---|---|---|
| `ViewDistance` | 14.0 | 18.0 | 8.0 |
| `InnerViewDistance` | 5.0 | 6.0 | 4.0 |
| `MaxPursuitDistance` | 18.0 | 20.0 | 16.0 |
| `WanderDistance` / `MinWanderDistance` | 5.0 / 3.0 | 7.0 / 4.0 | 4.0 / 2.0 |
| `TeleportToLeaderDistance` | 23.0 | 23.0 | 18.0 |
| `RoamBehavior` | NeverRoam | Roam | NeverRoam |
| `min/maxSwingPause` | **0.0 / 0.0** | 0.0 / 0.0 | 0.0 / 0.0 |
| `DodgeChance` | 0 | 0 | 0 |
| `FleeBehavior` | NeverFlee | NeverFlee | NeverFlee |
| `BuffSelfBehavior` | WheneverPossible | WheneverPossible | WheneverPossible |
| `heal Leader / Ally %` | 80 / 70 | 75 / 60 | 85 / 75 |
| `ignorePetsChance` / `Interval` | 30 / 5000 | 30 / 5000 | 30 / 5000 |
| `randomEmoteChance` | 100 | 100 | 100 |
| `EmoteBeforePursuingChance` | 30 | 30 | 30 | *(dead field — never read, § F-D3-3)* |

The **Guardian of Empyrion** body record was **not resolved in this lap**: it is not a
`Skill_SpawnPet` under `records/skills/devotion/**` (the only `Skill_SpawnPet` there is
Shadow Clone), and the `*guardianofempyrion*` hits are all item skill-modifiers. **Declared open**
and handed to Wave-2 B-3.

---

### 3.6 · Roaming (8 fields) — **DECODED · reachable but starved**

**Rule — idle→roam delay [bin]**, `ControllerMonsterStateIdle::OnBegin` @ `0x0feaf6`:
```
if ( this[0x4dc] == this[0x4e0] ) {
    lo = (float) controller[0x394]                 ; MinTimeBeforeRoam
    hi = (float) controller[0x398]                 ; MaxTimeBeforeRoam
    r  = (float) rand()
    idleTimer = (int)(  r * (1/32767)  * (hi - lo)  +  lo  )       ; const 0x105f5740 = 3.0518509e-05
}
```
The constant at `0x105f5740` is **3.0518509e-05 = 1/32767** — i.e. `rand()/RAND_MAX`, a
*continuous* uniform, unlike the integer `IGenerate` used for swing pause. **Two different RNG
idioms in the same controller**; a faithful runtime must reproduce both.

`StartedRoaming@ControllerMonsterStateIdle` @ `0x0febc6` tests
`cmp dword ptr [ecx+0x320], 0` → roam iff `RoamBehavior != NeverRoam(0)`.
`StartRoaming@ControllerMonsterStateRoam` reads `MinRoamDistance` (`+0x39c`) and `RoamDistance`
(`+0x374`). `StateWander` reads `WanderDistance`/`MinWanderDistance`;
`OnBegin@ControllerMonsterStateNavigateObstacle` also reads `MinWanderDistance`.
`TeleportToLeaderDistance` is read by `StateFollowLeader::OnUpdate`, `StateDefendLeader::OnUpdate`,
`HandleEvent@StateAttack` and `HandleEvent@StateJumpAttack`.

**Values [rec]:**

| Field | Slot | 169-weighted | Crucible changed |
|---|---|---|---|
| `RoamBehavior` | `+0x320` | **`Roam` ×167**, `NeverRoam` ×2 | 16/77 (**15 × `NeverRoam → Roam`**) |
| `MinRoamDistance` | `+0x39c` | `2.0` ×160, `3.0` ×7, `0.0` ×2 | 27/77 |
| `RoamDistance` | `+0x374` | **`2.0` ×144**, `5.0` ×15, `4.0`/`3.0` ×4, `0.0` ×2 | 66/77 (`5.0→2.0`, `4.0→2.0`) |
| `MinTimeBeforeRoam` | `+0x394` | **`2000` ×144**, `6000` ×24, `0` ×1 | 65/77 (`6000→2000`) |
| `MaxTimeBeforeRoam` | `+0x398` | **`2000` ×144**, `12000` ×21, `16000` ×3, `0` ×1 | 66/77 (`12000→2000`) |
| `MinWanderDistance` | `+0x3a0` | `2.0` ×168, `0.0` ×1 | 2/77 |
| `WanderDistance` | `+0x370` | **`0.0` 169/169** | 18/77 (`5.0→0.0`) |
| `TeleportToLeaderDistance` | `+0x378` | **`40.0` 169/169** | 2/77 |

**⚑ Reading of the Crucible re-tune [inferred from rec].** `MinTimeBeforeRoam == MaxTimeBeforeRoam
== 2000` collapses the continuous roll to a **fixed 2000 ms**, and `RoamDistance = 2.0 m` with
`MinRoamDistance = 2.0 m` collapses the roam to a 2 m step. Crate turned roaming *on* for 15
previously-`NeverRoam` controllers while shrinking it to a twitch — a Crucible-specific "keep the
pack milling, don't let it wander out of the arena" tuning. `WanderDistance = 0.0` on all 169 is
the pet-wander field and is dead for enemies (`StateWander` is a pet/follower state).
**Practically:** with `ViewDistance = 80 m` covering the whole arena (Lap U), `StateIdle` is
essentially never occupied by a Crucible attack pack, so the roam limb is reachable-but-rarely-
entered rather than provably inert. I do not claim inertness here — the Idle-occupancy question
belongs to the sim's own state track (facet (a)), not to the record.

---

### 3.7 · Patrolling (3 fields) — **DECODED · and the editor name is misleading**

**Rule [bin]** — `ControllerMonsterStatePatrol::PathFailed()` @ `0x105460`, in full:
```
esi = controller[0x37c]                     ; ChanceToIdleOnPatrol
r   = rand() % 100
if (r >= esi)  { idleTimer = 0 }                                     ; no idle
else {
    span = controller[0x384] - controller[0x380] + 1                 ; Max - Min + 1
    if (span - 1 <= 0x7ffd) idleTimer = rand() % span + controller[0x380]
    else                    idleTimer = controller[0x380]            ; overflow guard
}
if (idleTimer == 0) -> <resume patrol immediately>
```
**⚑ These three fields are read from exactly ONE place: the path-failure handler.** There is no
"idle randomly while patrolling" path. `ChanceToIdleOnPatrol` is a *pathing-failure* idle
probability. The whole group is unreachable unless a monster is in `StatePatrol` **and** its
path request fails.

**Values [rec]:** `ChanceToIdleOnPatrol` = `0` ×153, `75` ×6, `__ABSENT__` ×6, `20` ×4 ⇒
**inert for 153/169**. `MinPatrolIdleTime` = `1000` ×168, `MaxPatrolIdleTime` = `5000` ×168.
**Crucible delta:** 49/77 driven to 0 on the chance; 47/77 and 46/77 re-timed
(`0 → 1000`, `1500|0 → 5000`).

**Compounding evidence [prior lap]:** Lap U (`pm4u_findings.md` § 2.3) decoded that a Crucible
attack pack **essentially never occupies `StatePatrol`** — `ShouldFindEnemy` is `TRUE` in Patrol
and `ViewDistance = 80 m` covers the arena, so the pack hands off to `Pursue` at spawn.
Combined with `ChanceToIdleOnPatrol = 0` on 153/169, the Patrolling group is **doubly inert**
for this fight. Ship the parameters and the `PathFailed` rule; expect zero occupancy.

---

### 3.8 · Emote (3 fields) — **DECODED · PROVABLY INERT for 150/169**

**Rule [bin]** — `ControllerMonster::Update(dt)` @ `0x0f651c`:
```
this[0x520] -= dt
if (this[0x520] <= 0) {
    this[0x520] = IGenerate( this[0x518], this[0x51c] )     ; randomEmoteMin/MaxTime (ms)
    if ( rand() % 100 < this[0x514] ) {                     ; randomEmoteChance
        ; select from the character's emote list at Character+0x1c50 (2 slots scanned),
        ; falling back to Character+0x1c0c
    }
}
```
**Values [rec]:** `randomEmoteChance` = **`0` ×150**, `100` ×10, `__ABSENT__` ×6, `50` ×3;
`randomEmoteMinTime` = `5000` ×126, `6000` ×21, `0` ×21, `9000` ×1;
`randomEmoteMaxTime` = `10000` ×147, `0` ×21, `12000` ×1.

**Crucible delta [rec]: 57/77 controllers driven `100 → 0`** (plus `30→0` ×8, `50→0` ×6).
Together with `EmoteBeforePursuingChance` driven `20→0` on 66/77 (a field the engine does not
read anyway, § F-D3-3), **the Crucible deliberately silenced monster emotes.**

**Separate emote surface, NOT covered by these fields [bin]:** the states
`ControllerMonsterStateEmote` (#39) and `EmoteOrRoam@ControllerMonsterStateWaitToAttack` exist as
code. `StateWaitToAttack::EmoteOrRoam` is a *different* entry point into emoting and is **not**
gated by `randomEmoteChance` — I did not decode its condition. **Declared:
`EmoteOrRoam` entry condition UNDECODED-FROM-SUBSTRATE** (searched: displacement scan on
`+0x514/0x518/0x51c` — no hit inside `EmoteOrRoam`; export-name scan for `Emote`). So "emotes are
inert" is safe for the *random* emote limb only; the WaitToAttack limb is an open residual.

---

### 3.9 · Sleep (1 field) — **DECODED semantics · CONDITIONALLY LIVE**

`ignoreSleepingEnemies` → `+0x4d9` (bool). Accessor `IgnoreSleepingEnemies@ControllerMonster`
@ `0x06a4b0` is a one-instruction load. **Consumers [bin] — clean and unambiguous, only 6 touch
sites in the whole image, all in `ControllerMonster`:** `FindEnemy`, `GetMostHatedEnemy`,
`AngerUpdate`, `FindEnemyUpdate`. It is a **target-selection filter**: a monster with the flag
set will not select an enemy that is asleep.

**Values [rec]:** `True` ×94 / `__ABSENT__` ×75 (169-weighted); `True` ×50 / absent ×27 (77);
`True` ×222 / absent ×137 (corpus 359). Absent ⇒ engine default **false**.
**Crucible delta:** 8/77 (`__ABSENT__ → True`).

**⚑ NOT provably inert.** `ControllerPlayerStateSleep` **exists** in `Game.dll`'s export table
(alongside `ControllerPlayerStateStunned`, `…Immobilized`, `…KnockedDown`, `…Trapped`), and
`BeginSleep@ControllerAIStateT<ControllerPlayer,Player>` is a live override. **The player can be
slept in Grim Dawn.** So this field is inert **iff** no monster in waves 150–160 applies sleep to
the player. That is a roster-skill question and belongs to **D-2 / B-2**, which already holds the
286 control rows. **Named check handed over:** does any granted skill on the 169-record roster
apply a sleep/`Sleep` modifier? If yes, `ignoreSleepingEnemies` produces a *visible* behaviour —
94/169 monsters will drop the player as a target while asleep, which is a mercy window a Godot
runtime must reproduce or the fight gets harder than the referent.

---

### 3.10 · Loot (2 fields) — **DECODED · PROVABLY INERT · and mis-scoped by its group name**

`lootDropAttachPointName`, `lootDropCallbackPoint` — both `std::string`, both read in
`ControllerMonster::Load` at `0x0f7aff` / `0x0f7ac7`. Accessor
`GetLootDropCallback@ControllerMonster` @ `0x0fcb90`.

**Values [rec]: `__ABSENT__` on 169/169 rolled, 145/145 pool, and 358/359 corpus-wide.** The
single exception carries `FX_Weapon` / `LootDrop`.

**⚑ Scope correction.** This group is **not the loot system**. The loot drop itself runs through
`DropLoot@ControllerMonster` / `DropLoot@ControllerMonsterStateDying`, with
`GetLootDropCoords` / `GetLootDropRadius` / `GetLootDropGroup` / `HasLootDropped` as the live
`ILootContainer` surface (`ControllerMonster` has a second vtable
`??_7ControllerMonster@GAME@@6BILootContainer@1@@`). The two `.tpl` fields are only the
**attach-point / animation-callback names** used to *place and time* the drop FX. Absent ⇒ drop
at the actor's own coords with no animation gate.

**Model-pack instruction:** ship the two fields as declared-empty; **do not** conclude anything
about loot from them. Loot economics are a separate decode that this lap did not touch.

---

### 3.11 · Dying (1 field) — **DECODED · PROVABLY INERT**

`dyingSkillCallbackPoint` — `std::string`, read at `0x0f7b77`; accessor
`GetDyingSkillCallback@ControllerMonster` @ `0x0fcba0`. Companion API:
`GetDyingSkillId` / `SetDyingSkill` / `StartDyingSkill@ControllerMonsterStateDying`.
**Semantics [bin+inferred, labelled]:** the *callback point* is the animation event name at which
`StateDying` fires the dying skill; the *skill id* is set through `SetDyingSkill`, a separate
non-record path.

**Values [rec]: `__ABSENT__` on 169/169, 145/145 pool, 358/359 corpus-wide** (sole exception:
`skillFX`). ⇒ **no monster in this fight has an animation-callback-gated death skill.**

**⚑ Carve-out, so this is not over-read:** this does **not** say monsters have no death effects.
`ControllerMonsterStateDying` exists with a full override set (`BeginStun`, `BeginKnockdown`,
`BeginSleep`, `BeginTrap`, `BeginImmobilize`, `BeginTakeHit`, `RespondsToFear`) and
`StartDyingSkill` can still be driven by `SetDyingSkill`. Death-spawn chains (the Kubacabra
lineage from the Lap-D reader-correction) ride the *monster* record, not this controller field.
What is inert is the **callback-point limb** only.

---

### 3.12 · RandomAnger (2 fields) — **DECODED (context)**

Not on the D-3 target list (the AngerManagement group was already decoded at WR3-W2), but the
`RandomAnger` sub-group had no decoded rule, so it is closed here.

**Rule [bin]** — `ControllerMonster::Update(dt)` @ `0x0f66a1`:
```
if (this[0x508] == 0) {
    this[0x500] -= dt
    if (this[0x500] < 0) {
        this[0x500] = this[0x504]                 ; RandomAngerEvaluationTime
        if ( rand() % 100 < this[0x390] ) {       ; RandomAngerChance
            if ( GetCurrentStateData()[0] == 0 ) {
                Character* c = PickRandomEnemyInView()
                if (c) <retarget / anger>
            }
        }
    }
}
```
**Values [rec]:** `RandomAngerChance` = `0` ×125, `10` ×43, `15` ×1;
`RandomAngerEvaluationTime` = `0` ×111, `3000` ×57, `5000` ×1.
⇒ **43/169 monsters re-roll a random target every 3 s at 10 %**. With the player's two summons
present, this is a live target-shuffle source and is worth carrying into B-3.

---

## 4 · Already-decoded groups — corrections and completions (context only, not re-decoded)

The charter said do not redo Senses / AngerManagement / DistressCalls / Pursuit. Three facts fell
out of the same passes and are banked because they *correct* the standing record.

1. **`DistressResponseBehavior` enum, and the Crucible's one-group collapse.**
   Enum decoded [bin] at `+0x354`: `RespondToSameGroup=0 · RespondToSameRace=1 ·
   RespondToAll/other=2` (the `RespondToSameRace` branch is the `neg/sbb/add 2` idiom at
   `0x0f7630`). Census [rec]: `RespondToSameGroup` on **169/169**, and
   **`DistressResponseGroup = "Aetherial"` on 169/169** — with **63/77 controllers changed by the
   Crucible layer** (`Beast→Aetherial` ×13, `Chthonic→Aetherial` ×11, `Undead→Aetherial` ×11,
   `Eldritch→Aetherial` ×10, …). ⚑ **The WR3-W2 reading that distress calls are faction-keyed is
   correct for the base game and WRONG for the Crucible:** every monster is in the same group, so
   `RespondToSameGroup` is functionally `RespondToAll`. Combined with
   `ChanceToRespondToDistressCall` changed on 30/77 (169-weighted: `75` ×48, `15` ×46, `50` ×40,
   `100` ×18, `20` ×15, `0` ×2), the Crucible traded *selectivity* for a *spread rate* — and the
   net effect is **more** cross-faction responders, not fewer.
   Consumers [bin]: `ShouldCareAboutDistressCall@ControllerMonster`,
   `DefaultAllyAttackedResponse`, `DefaultAllyNeedsHelpResponse`.
2. **`MaxPursuitDistance` 75.0 → 125.0 on 76/77, and 210.0 → 125.0 for bosses.** Consumers [bin]:
   `InPursuitRange@ControllerMonster`, `ShouldCareAboutDistressCall@ControllerMonster`,
   `OnBegin@ControllerMonsterStateReturn`. The boss reduction is the notable one: base-game
   bosses are functionally un-leashable at 210 m; the Crucible pulls them to the same 125 m as
   trash. Against the decoded arena (86.9 × 85.3 m, worst spawn→player ≲ 76 m), **125 m still
   exceeds the arena diagonal ⇒ no monster can ever leave pursuit range.** `StateReturn` is
   therefore unreachable in this fight — a second state to ship as declared-unreachable.
3. **`enemyTooClose` driven to `0.0` on 44/77** (from 3.0/5.0/4.0/2.0). Whatever back-off this
   parameterises, the Crucible switched it off.

---

## 5 · Residuals — declared, not papered over

| # | Residual | What I searched | Where it routes |
|---|---|---|---|
| R-1 | **`LeadChance` array INDEX semantics** | `Load` array-getter call site; `.text` disp scan; export scan for `Lead` | UNDECODED-FROM-SUBSTRATE by this lap's method; next probe = `Skill_Attack*Projectile*` aim path |
| R-2 | **`randomRepositionChance` second conjunct** (`virtual_call(controller, vtbl+0xfc)`) | disassembled `StateAttack::OnUpdate` | vtable-index resolution needed; SEMANTICS-PARTIAL |
| R-3 | **`EmoteOrRoam@ControllerMonsterStateWaitToAttack` entry condition** | disp scan on the three emote slots (no hit inside it); export scan | open; blocks a full "emotes inert" claim |
| R-4 | **`petAngerTransference` slot** | automated slot walk (store shape is not a scalar `mov`) | value + getter DECODED; memory slot unresolved (cosmetic — does not block the model) |
| R-5 | **`DebuffEnemyBehavior` dispatch site** | direct-call (E8) scan on the getter → 0 hits (virtual/inlined) | value + enum DECODED; call site unresolved |
| R-6 | **Guardian of Empyrion pet body record** | `Skill_SpawnPet` scan over `records/skills/devotion/**`; name scan `*empyrion*`/`*guardian*` | open → Wave-2 B-3 (facet (f)) |
| R-7 | **`+0x28c` writer** (the rally/alert latch) | disp scan; candidate `DefaultEnemyFoundResponse@ControllerMonsterState<ControllerMonster>` | **belongs to D-1** — handed over, not claimed |
| R-8 | **Does any wave-150–160 monster apply sleep?** | not attempted (roster-skill question, out of D-3's seam) | **D-2 / B-2** — gates § 3.9's inertness |

---

## 6 · What Wave 2 / the baton should take from this

1. **Re-source every controller row from the SurvivalMode-winning record.** F-D3-1 makes
   base-game controller values wrong for this fight across the board, not just on `ViewDistance`.
2. **Two RNG idioms must both be modelled:** integer `RandomUniformLocked::IGenerate(lo,hi)` on a
   named global stream (swing pause, emote interval), and CRT `rand()` with `% 100`
   (flee, dodge, reposition, emote chance, random anger, patrol idle) — **except pet-ignore,
   which is `% 101`**. The tick+RNG contract in the baton should name which is which per rule.
3. **Ship four states as declared-unreachable, each with a decoded reason, not an assumption:**
   `Flee` (#8, `CanFlee` triple gate), `FollowLeader` (#13) and `DefendLeader` (#16)
   (`LeaderBehavior` absent corpus-wide ⇒ `NeverLead`), `Return` (#12) (`MaxPursuitDistance`
   125 m > arena diagonal). `Patrol` (#30) is reachable-but-empty per Lap U + § 3.7.
4. **Do not treat `SkillUsage` as a reason for silent specials (D-2).** All three behaviour gates
   are open on this roster and the ally-heal threshold is 70–80 %.
5. **Swing pause is per-swing, not per-spawn**, and is stored in ms after a ×1000 conversion from
   the record's seconds. `d3_swing_pause_ms.csv` is the ready-to-ship table.
6. **`ignoreSleepingEnemies` is a live risk, not a curiosity.** If D-2 finds a sleep applier,
   94/169 monsters change targeting behaviour and the fight's difficulty moves.

---

## 7 · Files

```
README.md                              this note
d3_digests.json                        sha256 of Game.dll, Engine.dll, 8 .arz, 2 .tpl, roster CSV
d3_roster_controller_params.csv        per-controller × per-field: crucible value, base-game value,
                                       owner archive, slot, n_monsters   (the model-pack feed)
d3_group_rollup.json                   monster-weighted value histogram per field, per group
d3_swing_pause_ms.csv                  per-controller swing-pause window in ms (facet (i))
evidence/d3_census.json|.txt           3-population record census over all 68 fields
evidence/d3_override.json              per-field Crucible-vs-base-game transition counts
evidence/d3_override_rows.csv          5,313 rows: every (controller, field) base→crucible pair
evidence/d3_slots2.json                field → slot / engine default / unit conversion
evidence/d3_picklist.json              picklist token → enum ordinal, per field
evidence/d3_binary_readers.json        field-name literal → every push site → enclosing export
evidence/d3_consumers_filtered.json    slot → Controller* consumers (the semantics map)
evidence/d3_ctrlmonster_load.asm       full disassembly of ControllerMonster::Load
evidence/d3_funcs.txt                  ResetSwingTimer · ShouldPlayRallyOrAlert · CanFlee ·
                                       IgnoreSleepingEnemies
evidence/d3_patrol_dodge.txt           StatePatrol::PathFailed · ProjectileNotification ·
                                       StateIdle::OnBegin · StartedRoaming
evidence/d3_petctrl.txt                the three player-pet stance controllers
evidence/d3_swingpause.txt             swing-pause console dump
scripts/                               10 read-only scripts (d3_lib, census, override, binary,
                                       slots, slots2, picklist, allfields, consumers, emit)
```

---

*Lap D-3 closed 2026-08-24 by legolas (`UNKNOWN-RESEARCHER`). 12 groups: 11 DECODED, 1 DECODED-
with-a-named-conditional (Sleep). 8 residuals declared. No fitted constants; no invented
semantics; every rule carries an RVA or a census.*
