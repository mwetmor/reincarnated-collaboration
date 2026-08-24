# KC2-MC · Lap D-10 — the ARMED ROWS decoded: `Disruption` + `ManaBurnDrain` consumers, and `R-D7-2` player-side

**Agent:** legolas (UNKNOWN-RESEARCHER) · **Date:** 2026-08-24 · **Conductor:** gandalf (`RUN-CONDUCTOR`)
**Commission:** ledger row **`L-55`**, ruling **`R-L55-2`** — `MD-B4-1` (a)(b)(c)(d) + the `R-D7-2` player-side half.
**Charter:** `agentic_orchestration/gandalf/notes/2026-08-24-kc2-model-completion-run-charter.md` (rows `L-50` / `L-54` / `L-55`)
**Consumes:** B-4's math note `reincarnated-engine/src/reincarnated/simulation/math/kc2-mc-b4-specials-2026-08-24.md` §§ 3, 3.1, 4 (`C-B4-4`), 9 (`MD-B4-1`) · D-7 `§ 7 R-D7-2` · D-8 `§ 0` (the LATCH).

**Substrate (pinned, read-only):**

| source | sha256 |
|---|---|
| `/Users/admin/Games/vendor/grim-dawn/Game.dll` | `4876d6bdb69cca71cfa987652cbd7a42cf6d5578564d02d09aaf9b55c078ab02` |
| `/Users/admin/Games/vendor/grim-dawn/gdx1/database/GDX1.arz` | `e28ab2515477ac80bdc3f955b6aa804eee791d4c51fda64c9ea01306522a4539` |
| `data/kc2/pm2_tg2_attack_damage.csv` | `e250089e7db3ef90f8a02dc2459c27b5bcc159a559769630aefb0167577bbf3c` |
| `data/kc2/pe6_crucible_wave_pools_v2.csv` | `bbdc18f12aab8e3788eac229ed1871a88ed7790dc3d1786c509cd26c076e5587` |
| `data/kc2/pm2_measured_player_sheet.csv` | `6852794382b9bf608f13433ea18be7a52d1f2f0942801e5bb7c4e1be8899badd` |
| `data/kc2/pm4g_played_kit.csv` | `2fd5a34792b96125bd55a40891dfd65cdeb43c385c6ef06607486342d53ce0b3` |

Full digest sidecar, including the emitted files: `d10_digests.json`.
**Method:** the D-7/D-8/D-9 harness (`d4b_pe.py`, `d4b_dis.py`, `d8_lib.bounded()`, `d7_step13_slots.py`,
`d7_step9_xref.py`) plus four new instruments: `d10_step3_fieldscan.py` (struct-offset write scan),
`d10_step4_ctorchain.py` (ctor-chain flag resolution), `d10_step5_vslot_callscan.py` (indirect-call scan
through a vtable displacement), `d10_step6_arz.py` (record read via the banked TQIT reader).
**Display-layer guard honoured:** zero tooltip / `tags_ui.txt` joins. Every rule below is read off an
instruction body or a `.dbr` field; the only string literals consumed are the DBR *field-name* tags the
loader itself returns, which are substrate, not display.

---

## § 0 · VERDICT TABLE

| target | verdict | one line |
|---|---|---|
| **MD-B4-1 (a) — is `min` a DURATION or a MAGNITUDE?** | **DECODED, and the two rows answer DIFFERENTLY** | **`Disruption` = DURATION in SECONDS** (`Execute` does `v *= 1000.0; cvttss2si` — the ×1000-and-truncate *is* the units proof). **`ManaBurnDrain` = MAGNITUDE, specifically a PERCENT of the target's mana limit** (`Execute` inlines `Character::GetManaLimit()` byte-for-byte; no ×1000 anywhere). |
| **MD-B4-1 (b) — which engine path consumes each?** | **DECODED end to end, both** | Disruption → `Character::CombatAddCooldownDamage` → `SkillManager::ApplyCooldownDamage` → **every** skill's `ApplyDisruptionCooldownTime` → `ReplaceCooldownTime` = **a kit-wide cooldown lockout, longest-wins**. ManaBurn → an **energy drain** clamped to current energy, plus an **optional** health limb gated on `offensiveManaBurnDamageRatio`. |
| **MD-B4-1 (b′) — does Disruption interrupt the channel? (the D-8 latch)** | **DECODED — NO.** *(the negative the conductor pre-authorised)* | `SkillManager::StopCurrentSkill` — D-8's latch trigger — has **exactly seven call sites, all `<Action>::Execute`**: MoveTo, JumpAttack, Evade, TakeStun, TakeKnockdown, TakeSleep, Immobilize. **No cooldown path, no mana path, and nothing on Disruption's chain is among them.** Disruption does not clear the EoR spin flag and does not drop the `+25/+25`. |
| **MD-B4-1 (c) — who carries them, at what value, on which slots** | **DECODED — ONE BODY in the whole 237-record roster** | `nemesis_chthonianvoidborn_01` (**Grava'Thul, the Voiddrinker**), 5 rows, 2 skills. CSV: `d10_roster_carriers.csv`. |
| **MD-B4-1 (d) — can either produce a SPIKE?** | **Disruption: NO as damage, NO as defence-drop, YES as a 1.4 s COUNTERPLAY LOCKOUT. ManaBurn: NO as damage (ratio field ABSENT ⇒ 0), CONDITIONAL as a 257.6-energy resource spike.** | The real spike on the Disruption row is its **carrier**: a 5-target 180° charge for **1,092 physical + 771 chaos** at rank 28, followed by 1.4 s in which Blitz / Vire's Might / War Cry / Ascension / EoR-restart are all locked — **and the health potion is EXEMPT** (decoded, § 4.3). |
| **`R-D7-2` player-side — `Disruption` (13) and `Convert` (51) consumers** | **BOTH DECODED, and they land on opposite verdicts** | **Disruption is REAL on the player** — `Character::CombatAddCooldownDamage` is a genuine implementation that `Player` does **not** override. **Convert is a decoded PLAYER NO-OP** — its consumer is `Character::JoinMe`, the shared `ret 0x10` stub, un-overridden by `Player` while `Monster` overrides it. `R-D7-2` **CLOSES.** |

**Machine-readable products**

* `d10_armed_row_consumers.csv` — **17 rows**, one per HOP of the two decoded chains + the carrier-skill limb, each carrying the RVA, the demangled symbol, the first six bytes of the body, the method, and the rule.
* `d10_roster_carriers.csv` — **5 rows** = MD-B4-1 (c), every carrier row with its value, decoded unit, decoded DBR field, and its **pool reachability** (which global wave, which spawn point, uniform-draw probability).
* `d10_player_side_consumers.csv` — **7 rows** = the whole armed/influence family with the `Player` **and** `Monster` vtable occupants, the **second hop** where one exists, and the player-side verdict.
* `evidence/step1…step37` — 37 raw listings; every RVA cited below appears in one of them.

---

## § 1 · TARGET (a) — THE UNITS, DECODED FROM THE CONSUMER'S READ

### 1.1 `Disruption` — seconds, and the proof is an instruction

`?Execute@CombatAttributeAbsDamage_Disruption@GAME@@UAEXAAVCharacter@2@@Z` — **`0x000dc9e0`**, ten instructions
(`evidence/step1_disruption_execute_and_applycd.txt`):

```
0x000dc9e3  movss     xmm0, [ecx + 0x1c]          ; the attribute value v
0x000dc9e8  comiss    xmm0, [0x105f5708]          ; f32 = 0
0x000dc9ef  jbe       <return>                    ; v <= 0  -> nothing
0x000dc9f4  mulss     xmm0, [0x105f5918]          ; f32 = 1000
0x000dc9fe  cvttss2si eax, xmm0                   ; -> INTEGER
0x000dca06  jmp       dword ptr [edx + 0x3d0]     ; tailcall target->vtable[+0x3d0](int)
```

**`× 1000.0` then truncate-to-int, and the callee's mangled signature is `…UAEXH@Z` (one `int`).** A magnitude
is not multiplied by a thousand on its way to an `int` parameter; a **seconds→milliseconds** conversion is.
This is the identical shape D-7 § 3.4 found on the influence lane (`GetFixedDamageDuration` in ms) and the
identical shape B-2 § 2 registered for the control lane.

**The field name confirms the join independently.** The loader's own tag accessors return C-strings
(`evidence/step8_load_tags.txt`):

| accessor | returns |
|---|---|
| `GetLoadValueMinTag@DamageAttributeAbs_Disruption` `0x0014d830` | **`"offensiveDisruptionMin"`** |
| `GetLoadValueMaxTag@…` `0x0014d840` | `"offensiveDisruptionMax"` |
| `GetLoadChanceTag@…` `0x0014d7f0` | `"offensiveDisruptionChance"` |
| `GetType@DamageAttributeAbs_Disruption` `0x0001fc80` | `mov eax, 0xd` ⇒ **enum 13** |

`offensive<X>Min` is the same shape `offensiveStunMin` uses, and B-2 decoded *that* as a duration.
⚑ **Answer to `MD-B4-1` (1): `min` on a `Disruption` row is a DURATION IN SECONDS. B-4 § 3's reading was
right, and it is now decoded rather than inferred by analogy to the control lane.**

### 1.2 `ManaBurnDrain` — a percentage magnitude, and the proof is a byte-identical inline

`?Execute@CombatAttributeAbsDamage_ManaBurn@GAME@@UAEXAAVCharacter@2@@Z` — **`0x000dcc90`**
(`evidence/step7_manaburn_lifeleech_percentlife_execute.txt`). Reduced:

```
v   = this->[+0x1c]                       ; if v <= 0 -> return
A   = target->[+0xc6c]  B = target->[+0xa9c]  C = target->[+0xa54]  D = target->[+0xb84]
X   = ((D*0.01) + 1.0) * B * max((A+1.0)*100.0, 0.0) * 0.01        ; B >= 0 branch
burn = min( v * 0.01 * X , max(C,0) )
if (!target->[+0x1847]) { target->[+0x10f8] = 1; target->[+0xa5c] += burn; target->[+0x1320] += burn; }
x = this->[+0x2c] * 0.01 * burn ;  if (x > 0) CombatManager::ApplyDamage(&target[+0x3dc], x, …)
```

⚑ **`X` is not "a derived quantity resembling max energy" — it is `Character::GetManaLimit()`, inlined.**
`?GetManaLimit@Character@GAME@@QBE?BMXZ` at **`0x00056e20`** reads the *same three fields in the same order*
(`+0xc6c`, `+0xa9c`, `+0xb84`), uses the *same three constants* (`1.0`, `100.0`, `0.01`), takes the *same*
`comiss/jb` negative branch with the *same* `andps` absolute-value mask, and clamps with the *same*
`maxss`/`minss` (`evidence/step34_getmanalimit.txt`). And `C = +0xa54` is exactly what
`?GetCurrentMana@Character@…` returns and `?SetCurrentMana@Character@…` writes
(`evidence/step33_char_energy_offsets.txt`). **DECODED by structural identity, not by analogy.**

There is **no `× 1000`, no `cvttss2si`, and no duration parameter anywhere on this path.**

| accessor | returns |
|---|---|
| `GetLoadValueMinTag@DamageAttributeAbs_ManaBurn` `0x00155170` | **`"offensiveManaBurnDrainMin"`** |
| `GetLoadDamageRatioTag@…` `0x00155190` | **`"offensiveManaBurnDamageRatio"`** |
| `GetType@DamageAttributeAbs_ManaBurn` `0x0014fcd0` | `mov eax, 0xc` ⇒ **enum 12** |

⚑ **Answer to `MD-B4-1` (1), second row: `min` on a `ManaBurnDrain` row is a MAGNITUDE — specifically a
PERCENT of the target's mana limit, clamped to the target's current energy.** `min = 10.0` is **10 %**, not
10 points. B-4 correctly refused to guess; the two rows really do disagree, which is why the question was
worth firing.

### 1.3 ⚑ THE FINDING UNDER THE FINDING — neither row is on the health-damage lane at all

B-4 § 3 flagged that a 2 s duration "sits on the health-damage lane where it would be read as two points of
damage." **The engine's own answer is that it sits nowhere near it.** The `CombatAttribute` vtable diff
(`evidence/step11_attr_vtable_diff.txt`) shows:

| slot | base `CombatAttributeAbsDamage` | `_Disruption` | `_ManaBurn` |
|---|---|---|---|
| 9 / 17 `GetTotalDamage` | `0x000d7570` — **adds `[+0x1c]` into the running total** | `0x0003e4c0` = **`ret 0xc`** | `0x0003e4c0` = **`ret 0xc`** |
| 14 `GetMinMaxDamage` | `0x000d7590` | `0x000d7040` = **`ret 0x14`** | `0x000d7040` = **`ret 0x14`** |

**Both rows override the damage-total and min/max accumulators with pure no-op stubs.** They contribute
**zero** to the attack's health damage and zero to its displayed min/max. `ReflexDamage` (the whole control
family) and every influence family do the same. `kind = 'direct'` in
`pm2_tg2_attack_damage.csv` is therefore an **extraction-side label, not an engine-side lane** — the mislabel
is real and worth repairing, but the damage it was feared to cause does not exist in the engine.

### 1.4 ⚑ AND BOTH ROWS *ARE* RESISTIBLE — the "no `RESIST_PCT` entry" is a sim-side gap, not an engine one

* **`Disruption` does NOT override `ReduceDamage` (slot 21)**; it inherits
  `?ReduceDamage@CombatAttributeAbsDamage@…` at **`0x000d7620`** — *the exact function D-7 decoded as the
  control-duration scalar*: `if (this->[+4] == type) v *= (1 − r/100); v = max(v, 0)`
  (`evidence/step12_gettotaldamage_reducedamage.txt`).
* The enum census carries **`DefenseAttributeAbs_Disruption` (13)** *and* **`DefenseAttributeDefenseCap_Disruption`** — the game ships both a resistance and a cap for it.
* **The KC2 pilot has 30 % of it.** `pm2_measured_player_sheet.csv`: `disruption_resist, 30, percent, screenshot 519`.
* **`ManaBurn` DOES override `ReduceDamage`** (`0x000dce40`) with a wider match:
  `type ∈ {self, 0x0c ManaBurn, 0x15 ManaLeach}` reduces the **drain**; `type == 0x3e ManaBurnRatio` reduces
  the **health ratio**; both clamped ≥ 0. The pilot's `energy_leech_resist = 0` (sheet, screenshot 519)
  zeroes the ManaLeach limb.

**Consequence for `C-B4-4`.** B-4 refused to map a resistance because inventing one moves damage *upward*.
That refusal was correct **and** the number it needed was already measured: **`Disruption → 30 %`**, from the
pilot's own sheet, applied by a law the run has already decoded. The `ManaBurn` limb still needs one number
(`defensiveManaBurn`, enum 12) that the sheet does not print — see `R-D10-2`.

---

## § 2 · TARGET (b) — THE CONSUMER CHAINS, HOP BY HOP

Full machine form in `d10_armed_row_consumers.csv`. Prose here; every RVA is in `evidence/`.

### 2.1 `Disruption` — a nine-hop chain that ends in a KIT-WIDE COOLDOWN LOCKOUT

```
offensiveDisruptionMin (seconds)
  → ReduceDamage@CombatAttributeAbsDamage       0x000d7620   v *= (1 − defensiveDisruption/100), clamp ≥0
  → Execute@…_Disruption                        0x000dc9e0   ms = (int)(v × 1000)
  → Character vtable +0x3d0                                  ⚑ REAL on Player (§ 5)
  = Character::CombatAddCooldownDamage          0x00054710   (float)ms → SkillManager at this+0x600
  → SkillManager::ApplyCooldownDamage           0x004454d0   walks FOUR containers, calls +0x144 on EVERY skill
  → Skill::ApplyDisruptionCooldownTime          0x003bf110   if (this->[+0xca]) ReplaceCooldownTime(ms, 0.0)
  → Skill::ReplaceCooldownTime                  0x003bf0b0   THE WRITE
  ⇒ Skill::SetAvailability                      0x003bf880   [+0x150] > 0 ⇒ unavailable, reason = ON_COOLDOWN
```

`SkillManager::ApplyCooldownDamage` (`evidence/step4_…txt`) iterates **four** skill containers
(`+0x154/+0x158`, `+0x8c`, `+0x174/+0x178`, `+0x1f8/+0x1fc`) and calls `skill->vtable[+0x144](ms)` on every
non-null element of each. Slot `+0x144` resolves to `ApplyDisruptionCooldownTime` on **every** Skill-family
vtable checked, including `SkillChanneled` (`evidence/step5_skill_vtable_140_144.txt`) — **no subclass
overrides it**.

`Skill::ReplaceCooldownTime(float newMs, float secondaryMs)`, decoded in full:

```
if (newMs <= 0.0)                    return;
if (newMs <= (float)this->[+0x150])  return;      ⚑ LONGEST-WINS — never additive, never shortens
this->[+0x150] = (int)newMs;                       ; cooldown REMAINING
this->[+0x154] = (secondaryMs > 0) ? (int)secondaryMs : (int)newMs;   ; cooldown TOTAL (the UI sweep)
this->[+0x80]  = 1;                                ; unavailability reason = ON_COOLDOWN
this->[+0x86]  = 1;                                ; the on-cooldown flag
```

Disruption passes `secondaryMs = 0`, so both the remaining **and** the total become the disruption time.
⚑ **`newMs > 0` alone is enough to arm a skill that has no cooldown at all** (`[+0x150]` starts at 0), so a
Disruption puts a cooldown on cooldown-free skills — that is what makes it a *kit lockout* rather than a
per-skill delay. And the longest-wins rule is the **same convention D-7 § 5.2 decoded for same-family
control**, and the **opposite** of D-4c's DoT lane — worth stating because all three live in the same class
family.

`Skill::SetAvailability` (`evidence/step22_…txt`) closes the loop: it computes
`[+0x86] = ([+0x150] > 0)` and returns **false** with `[+0x80] = 1` whenever that is set. Disruption
pre-writes both fields, so the skill is unavailable the instant the row fires, not one tick later.

### 2.2 ⚑ WHICH SKILLS ARE DISRUPTABLE — `Skill+0xca` is a CTOR CONSTANT, not a DBR field

The gate at `0x003bf113` is `cmp byte ptr [ecx + 0xca], 0`. A struct-offset write scan
(`d10_step3_fieldscan.py`, `evidence/step20_skill_0xca_writes.txt`) finds **no loader writes it at all** —
every write is in a **constructor**:

| value | constructors |
|---|---|
| **0 — NOT disruptable** | `Skill` (the base, via `mov dword [esi+0xca], 0x100`), `Skill_BuffSelfImmobilize`, **`Skill_ChargePotion`**, **`Skill_Evade`**, `SkillBuff_Debuf`, `SkillBuff_BuffImmobilize`, `SkillBuff_DispelMagic` |
| **1 — disruptable** | **`SkillActivated`** (and therefore every activated skill), `SkillBuff_Passive`, `SkillSecondary` + all 15 `SkillSecondary_*` |

The ctor-chain walker (`d10_step4_ctorchain.py`, `evidence/step21_ctorchain_playerkit.txt`) resolves the flag
for the pilot's **nine bar-bound skills** (`pm4g_played_kit.csv`, `bound_on_bar == True`) by running the chain
in order and taking the last write:

| binding | skill | class | chain | `+0xca` |
|---|---|---|---|---|
| 0 | Vire's Might | `Skill_AttackPathCharge` | Skill→**SkillActivated**→Skill_AttackWeapon→· | **1** |
| 1 | War Cry | `Skill_AttackRadius` | Skill→**SkillActivated**→· | **1** |
| 2 | Ascension | `Skill_BuffSelfDuration` | Skill→**SkillActivated**→Skill_BuffSelfToggled→· | **1** |
| 3 | Violent Delights | `Skill_AttackPathCharge` | as above | **1** |
| 4 | Blitz | `Skill_AttackWeaponCharge` | Skill→**SkillActivated**→Skill_AttackWeapon→· | **1** |
| 5 | Weapon Attack | `Skill_WeaponPool_Default` | Skill→**SkillActivated**→· | **1** |
| 6\|7 | **Eye of Reckoning** | `Skill_AttackRadiusSpin` | Skill→**SkillActivated**→**SkillChanneled**→· | **1** |
| 8 | Summon Guardian of Empyrion | `Skill_TargetedSpawnPet` | Skill→**SkillActivated**→· | **1** |
| 9 | Summon Deathstalker | `Skill_SpawnPet` | Skill→**SkillActivated**→· | **1** |

**All nine. One Disruption landing arms all nine simultaneously** — including the basic Weapon Attack and both
summons.

⚑ **And the two classes that opt OUT are `Skill_ChargePotion` and `Skill_Evade`.** Potions and evade are
exempt from Disruption by construction. That is the *same design law* D-7 § 3.3 decoded for control states
("items + instant-cast PERMITTED through every control state"), arriving from an unrelated direction:
**GD's involuntary mechanics consistently spare the counterplay of last resort.** A first-class finding for
the game tracker — it is a *rule about what a lockout may never take*, and it is decoded twice now.

### 2.3 `ManaBurnDrain` — an energy drain with an OPTIONAL, HERE-DISABLED health limb

Chain in § 1.2. Two decoded gates matter:

1. **The health limb is `if (ratio * 0.01 * burn > 0)`.** The carrier record has **no
   `offensiveManaBurnDamageRatio` field at all** (`evidence/step31_arz_gdx1_carriers.txt`, checked by explicit
   presence test, not by grep-absence) ⇒ `this->[+0x2c] == 0` ⇒ `CombatManager::ApplyDamage` is **never
   reached**. **This row deals exactly zero health damage. MEASURED.**
2. **The drain is clamped to `CurrentMana`** — it cannot go negative and cannot overdraw.

---

## § 3 · TARGET (b′) — DOES DISRUPTION TRIP THE D-8 LATCH? **NO, AND THIS IS THE LAP'S CLEANEST NEGATIVE**

D-8 § 0 target 4 decoded the latch: *Petrify → `SetState("Immobilized")` → `ImmobilizeAction::Execute` →
`SkillManager::StopCurrentSkill` → `StopSpinning` → the EoR spin flag `Skill+0x4f4` clears →
`CollectPassiveDefenseAttributes` early-returns → `defensiveCrowdControl +25` DROPS.*

**`SkillManager::StopCurrentSkill` (`0x0043ea00`) has exactly SEVEN direct call sites in `.text`**
(`d7_step9_xref.py`, byte-exact `E8`/`E9` scan — `evidence/step36_stopcurrentskill_xrefs.txt`):

```
0x0006c6bf  MoveToAction::Execute            0x0006f172  TakeStunAction::Execute
0x0006de19  JumpAttackAction::Execute        0x0006f2e2  TakeKnockdownAction::Execute
0x0006e5dd  EvadeAction::Execute             0x0006f5b2  TakeSleepAction::Execute
                                             0x0006f722  ImmobilizeAction::Execute
```

**Nothing on Disruption's chain is among them, and neither is any cooldown or mana path.** Three independent
corroborations:

* `SkillChanneled::Update` (`0x00436250`) ends the channel on **one** predicate: `Character::IsAlive`
  (vtable `+0x22c`, resolved on both `Character` and `Player`). It does **not** consult cooldown,
  availability, or mana (`evidence/step22`, `step23`).
* `SkillChanneled::ForceEnd` (`0x004361b0`) has **zero** `E8`/`E9` xrefs **and zero image-wide 4-byte
  occurrences** — no call site and no function-pointer take anywhere in the image
  (`evidence/step30_addrscan.txt`). *(Technique limit named, per D-7 N-1: this is "no direct encoding and no
  pointer take exists," not a proof of unreachability under every possible dispatch.)*
* `Skill::Update` (`0x003b29a0`) only **decrements** `[+0x150]`; it does not gate on it.

⚑ **Ruling-ready statement: Disruption does NOT interrupt an in-flight channel, does NOT clear the EoR spin
flag, and does NOT drop the `+25/+25`.** The spike hypothesis's *defence-drop* limb is **falsified for this
mechanism**. What Disruption denies is **re-initiation and every other bar action** for its duration.

⚑ **Bonus, unlooked-for: this decodes L-52/L-53/L-54's attested channel breaks from the binary side.**
`MoveToAction`, `EvadeAction` and `JumpAttackAction` are three of the seven — so Matt's attested
movement-breaks and dodge-breaks are not behavioural colour, they are **the engine's own channel-stop list**.
The remaining attested break (casting another hotbar active) is *not* on this list, so it must break the
channel by **state replacement** rather than by `StopCurrentSkill` — consistent with D-7 `MD-B2-2`'s "channel
OFF by state replacement," and recorded as such rather than assumed.

---

## § 4 · TARGET (c) — THE CARRIERS, AND THE REACHABILITY FACT THE RUN NEEDS

### 4.1 One body. In the whole roster.

`pm2_tg2_attack_damage.csv` carries 4,724 rows over 237 distinct records (3,849 roster / 875 pet). Exactly
**5** are `Disruption` or `ManaBurnDrain`, and **all five are on the same record**:

| damage_type | surface | slot / tree | skill | class | `min` | decoded unit |
|---|---|---|---|---|---|---|
| `Disruption` | slot | **special4** | `chthonian02_charge.dbr` | `Skill_AttackWeaponCharge` | **2.0** | seconds |
| `Disruption` | tree | index 8 | (same) | (same) | 2.0 | seconds |
| `ManaBurnDrain` | slot | **special3** | `chthonian02_nullification_buff.dbr` | `SkillBuff_DispelMagic` | **10.0** | % of ManaLimit |
| `ManaBurnDrain` | tree | index 10 | (same) | (same) | 10.0 | % of ManaLimit |
| `ManaBurnDrain` | tree | index 11 | (same) | (same) | 10.0 | % of ManaLimit |

Body: `records/creatures/enemies/nemesis/nemesis_chthonianvoidborn_01.dbr` — **Grava'Thul, the Voiddrinker**,
stratum `nemesis`, `level_used = 109`, `rank_used = 28` (`rank_grade = MEASURED`). **Zero pet bodies carry
either row.** This reproduces B-4 `B4-P9`'s set equality from the CSV side, independently.

`.arz` read of both carriers (`d10_step6_arz.py` against `GDX1.arz`) confirms the values at source and adds
what the CSV projection dropped:

```
chthonian02_charge.dbr            Class = Skill_AttackWeaponCharge     skillMaxLevel = 60
    offensiveDisruptionMin        2.0                    (Max / Chance / Global / XOR all ABSENT)
    offensivePhysicalMin[60]      … [28] = 1092 …        offensiveChaosMin[60]  … [28] = 771 …
    skillTargetNumber 5 · skillTargetAngle 180.0 · skillAllowsWarmUp True
    characterRunSpeedModifier 150.0 · characterAttackSpeedModifier 300.0

chthonian02_nullification_buff.dbr   Class = SkillBuff_DispelMagic     skillMaxLevel = 1
    offensiveManaBurnDrainMin     10.0                   (Max / Ratio / Chance / Global / XOR all ABSENT)
    skillActiveDuration           5.0
    dispelFriendly False · dispelDamageOverTime False
```

### 4.2 ⚑ REACHABILITY — and it lands on the run's sharpest coincidence

`pe6_crucible_wave_pools_v2.csv`: Grava'Thul appears in **16** pool rows. **Exactly one is at tier ≤ 16:**

```
global_wave 160 · tier 16 · tier_wave 10 · spawn_point 2 · pool_kind BOSS · weight 100 · spawn 1–1
pool records/proxies/poolsbossgdx1/nemesis_all_noaetherialvanguard.dbr · roster_n = 5
    Kubacabra, the Endless Menace | Grava'Thul, the Voiddrinker | Reaper of the Lost
    | The Underking | Reaper of Rot
```

The sim's own emitter draws the name **uniformly** over the roster
(`wave_engine._emit`, the docstring registers the uniformity as a deliberate incumbent choice), so on the
record configuration:

> **p(Grava'Thul) = 1/5 = 0.20, on global wave 160, spawn point 2 — and NOWHERE EARLIER.**

⚑ **The record cell's terminals are `155 / 156 / 152 / 151 / 151`. The referent's terminal is `160`.**
B-4 § 3.1's "the only thing standing between this configuration and a `KeyError` halt is a roll" is now
**dated and located**: the sim cannot reach the roll, because it dies 4–9 waves short of the only wave that
offers it — while **the referent reached exactly that wave**. This is a *reachability* statement about the
armed rows, not a claim about what killed the referent; the causal question needs the video and is named as
`R-D10-3`.

**Two consequences that do not depend on resolving `R-D10-3`:**

1. **B-4's `C-B4-4` "bounded at zero on this configuration" is confirmed and now has a boundary condition**:
   bounded at zero **for as long as the sim terminates below wave 160**. Any change that buys the sim four
   more waves — a fold, a repair, a policy — arms a **20 % per-run halt**, and it arms it on the *first* wave
   past the current terminal band. That is not a distant latency.
2. **PM5 attribution gains a hard partition**: no residual at waves ≤ 159 can involve these rows at all.

### 4.3 ⚑ TARGET (d) — CAN EITHER PRODUCE A SPIKE?

Computed in f32, exactly as the engine does it:

| quantity | value |
|---|---|
| `offensiveDisruptionMin` | 2.0 s |
| `defensiveDisruption` (pilot sheet, screenshot 519) | 30 % |
| after `ReduceDamage`: `2.0 × (1 − 30×0.01)` | `1.4000000953674316` |
| `× 1000.0`, `cvttss2si` | **1400 ms** *(unmitigated would be 2000 ms)* |
| `offensiveManaBurnDrainMin` | 10.0 % |
| pilot `energy_max` (sheet, screenshots 495/508) | 2576 |
| `burn = min(10 % × 2576, CurrentMana)` | **257.6 energy** — 16.2 % of the screenshotted 1594 current, ≈ 3.42 s of the pilot's 75.37/s regen |
| `offensiveManaBurnDamageRatio` | **ABSENT ⇒ 0 ⇒ zero health damage** |

**`Disruption` — verdict: NO spike as damage. NO spike as defence-drop. YES as a 1.4 s counterplay lockout,
and the condition is named.**
* Damage: structurally zero (§ 1.3) — it is not on the damage lane at all.
* Defence-drop: structurally impossible (§ 3) — it cannot stop the channel.
* **What it *is*:** for 1.4 s the pilot has **no Blitz, no Vire's Might, no War Cry, no Ascension, no
  Weapon Attack, no summons, and cannot restart EoR if it stops for one of the seven reasons.** The health
  potion **remains available** (`Skill_ChargePotion`, `+0xca = 0`). So the decoded shape is
  **"escape and offence denied, healing preserved"**.
* **The spike that actually accompanies it belongs to the CARRIER**, not the attribute: `chthonian02_charge`
  is a 5-target, 180° weapon charge dealing **1,092 physical + 771 chaos** at rank 28, with a 150 % run-speed
  and 300 % attack-speed modifier. **Sub-second, multi-target, and immediately followed by 1.4 s in which the
  pilot cannot Blitz away.** That is a textbook spike-then-lockout geometry, and it is exactly the lane
  `L-50`'s spike-driven death asked to be separated from attrition.
* ⚑ **Registered negative, so it is not later over-read:** the charge record carries **no** knockdown, stun or
  immobilise field. It does not stop the channel by itself.

**`ManaBurnDrain` — verdict: NO spike as damage (measured zero). CONDITIONAL as a resource spike, and the
condition is `L-54`'s attested energy floor.**
* 257.6 energy in one application, against a pool of 2576 and a regen of 75.37/s.
* On the **sim as built** this is nothing: `L-54` establishes the sim is energy-**rich** and emits zero
  `energy_dryout` events. On the **referent**, Matt attests *"I had moments where I nearly ran out even with
  my policy"* — and a near-floor pool minus 257.6 is a floor. **The mechanism and the attestation meet.**
* Whether an energy-starved channel *stops* (and therefore trips the D-8 latch by the mana route) is
  **UNDERIVABLE here** — see `R-D10-4`. What is decoded is that a mana-out is **not** among
  `StopCurrentSkill`'s seven callers, so if it stops the channel it does so by another mechanism.

⚑ **AND THE LARGER SPIKE IS THE CARRIER, AGAIN — this time by class.** The `ManaBurnDrain` row rides
`SkillBuff_DispelMagic`. `?Install@SkillBuff_DispelMagic@…` (`0x003cc730`,
`evidence/step14_dispelmagic_install_load.txt`) branches on faction and, **on the hostile branch, calls
`target->vtable[+0x320]` = `Character::DispelSkillBuffs()` and then runs the attack.** `dispelFriendly` and
`dispelDamageOverTime` (both `False` here, read from the record) govern only the *same-faction* branch.
`Character::DispelSkillBuffs` → `SkillManager::DispelSkillBuffs` (`0x00444ec0`) walks a buff container and
calls `[vptr + 0x340](Character*)` on each element; **within the `SkillBuff_*` family** that slot is
`DispelBuff(Character&)`, the base is the shared `ret 4` stub, and **only five classes override it**:
`SkillBuff_Passive`, `_PassiveCharged`, `_PassiveEndless`, `_PassiveShield`, `_BuffImmobilize`
(`evidence/step19_dispelbuff_census.txt`).

**This is a buff-strip on the player, unresisted, instantaneous — i.e. a genuine defence-drop spike shape.**
Its magnitude for *this pilot* depends on one link this lap did **not** close: `R-D10-1`, § 6.

---

## § 5 · `R-D7-2` PLAYER-SIDE — CLOSED, WITH OPPOSITE ANSWERS ON ITS TWO HALVES

D-7 § 7 stated it verbatim: *"`Disruption` (13) and `Convert` (51) have no consumer on the involuntary or
influence path; where they *are* consumed was not chased — 6 of 143 roster rows."* Both are now chased.
Machine form: `d10_player_side_consumers.csv`.

### 5.1 `Disruption` (13) — **REAL on the player**

`Execute` tailcalls `Character` vtable **`+0x3d0`**. Resolved on all three vftables
(`evidence/step2_char_vtable_3c4_3d8.txt`):

| vftable | `+0x3d0` |
|---|---|
| `Character` | `?CombatAddCooldownDamage@Character@GAME@@UAEXH@Z` `0x00054710` |
| **`Player`** | **the same `0x00054710` — NOT overridden, NOT a stub** |
| `Monster` | the same `0x00054710` |

An image-wide 4-byte address scan (`evidence/step30_addrscan.txt`) finds `0x00054710` in **26** vtables at
`+0x3d0` and **no override anywhere**. Its callee `SkillManager::ApplyCooldownDamage` has **zero** image-wide
occurrences ⇒ its only entry is the direct `E8` from `CombatAddCooldownDamage` ⇒ the chain is single-path and
un-hijackable. **Disruption applies to the player in full.**

### 5.2 `Convert` (51) — **a decoded PLAYER NO-OP, and a stronger negative than D-7 could state**

`?Execute@CombatAttributeInfluenceDamage_Convert@…` `0x000dd010` is a **real** implementation
(`evidence/step9_…txt`):

```
v = this->[+0x1c];  if (v < 1.0) return                       ; ⚑ note: >= 1.0, not > 0
caster = Lookup(this->[+0x2c]);  if (!caster) return
if (caster->vtable[+0x2ac]() + 5 < target->vtable[+0x2ac]())  return     ; ⚑ A LEVEL GATE
ms = (int)(v × 1000.0)                                        ; Convert min is ALSO a duration
target->vtable[+0x30c](this->[+0x2c], ms, 1, 0)
```

`+0x2ac` = `GetCharLevel@Character` on `Character`/`Player`, overridden to `GetConvertLevel@Monster`
`0x002d5470` on `Monster`. `+0x30c`:

| vftable | `+0x30c` |
|---|---|
| `Character` | `?JoinMe@Character@GAME@@UAEXIH_N0@Z` `0x0003e4b0` — **`ret 0x10`, the shared 4-arg stub** |
| **`Player`** | **the same `0x0003e4b0` stub — NOT overridden** |
| `Monster` | `?JoinMe@Monster@GAME@@UAEXIH_N0@Z` `0x002d5200` — a real function |

⚑ D-7 could only say *"Convert is absent from `StartInvoluntaryEffect`'s switch and from the influence
pair."* The stronger, decoded statement is: **Convert has a real, level-gated consumer that reaches
`Character::JoinMe`, and `Character::JoinMe` is an empty stub that `Player` does not override while `Monster`
does. Convert on a player is a decoded ZERO — not a defaulted one, and not an absence.** The four `Convert`
roster rows are player-side inert. `R-D7-2` **CLOSES**.

*(Incidental, banked: `PetPlayerScaling` and `PetNonScaling` carry `Monster::JoinMe` at `+0x30c` — the
player's **pets** are convertible even though the player is not. Named, not chased.)*

### 5.3 The whole family, one table — and a correction I nearly shipped

| family | enum | `Player` occupant of the consulted slot | second hop | verdict |
|---|---|---|---|---|
| **Disruption** | 13 | `CombatAddCooldownDamage` `0x00054710` | (direct call, non-virtual) | **REAL on Player** |
| **ManaBurnDrain** | 12 | (no vtable hop — `Execute` writes Character fields) | — | **REAL on Player** |
| LifeLeech | 20 | `CombatAddLifeLeechDamage` `0x00054730` | — | REAL on Player |
| **Convert** | 51 | `JoinMe@Character` `0x0003e4b0` = `ret 0x10` | — | **PLAYER NO-OP at hop 1** |
| Confusion | 53 | shared `ret 4` stub `0x000084d0` | — | PLAYER NO-OP at hop 1 |
| Fear | 52 | `CombatExertInfluenceFear@Character` `0x00054690` — **a real function** | `ControllerPlayer+0x84` → `0x0000f100` `ret 8` | **PLAYER NO-OP at hop 2** |
| Taunt | 50 | `CombatExertInfluenceTaunt@Character` `0x000546d0` — **a real function** | `ControllerPlayer+0x8c` → `0x0000f100` `ret 8` | **PLAYER NO-OP at hop 2** |

⚑ **Self-disclosure #1.** The first emitter run labelled Fear and Taunt *"REAL on Player"* because their
`Player` slot holds a real `Character::` body. It is real — and it forwards to a controller slot that is a
stub. A one-hop reading of a two-hop dispatch produces a confident, wrong row. The emitter now carries an
explicit `second_hop` column and resolves it; D-7 § 3.4 had this right and I reproduced it only after the
check. **Rule worth carrying: a "REAL implementation" verdict is not a consumer verdict until the body has
been read to a terminal write.**

---

## § 6 · RESIDUALS — named, with the path, per Law 3

| id | residual | why it is UNDERIVABLE here | the named continuation |
|---|---|---|---|
| **`R-D10-1`** | **Does Grava'Thul's nullification strip the KC2 pilot's passive defensive layer?** § 4.3 decodes that `DispelSkillBuffs` removes exactly the `SkillBuff_{Passive,PassiveCharged,PassiveEndless,PassiveShield,BuffImmobilize}` instances. What is **not** established is which of the pilot's **DBR-declared** skills (258 `Skill_Passive`, 2 `Skill_BuffSelfShield`, `Skill_PassiveOnHitBuffSelf`, 2 `Skill_PassiveOnLifeBuffSelf`) instantiate such a buff into `SkillManager+0x88`. | ⚑ **Self-disclosure #2 — I over-read a vtable slot and caught it.** I first treated `+0x340` as "the DispelBuff slot" globally. It is **not**: `Skill_Passive+0x340` = `Load@SkillActivated`, `Skill_AttackRadiusSpin+0x340` = `StartAction` (`evidence/step37_…txt`). The Skill-family vtables are **not slot-aligned** across the hierarchy; the slot is only `DispelBuff` **within** `SkillBuff_*`. Reading it outside that family would have produced a false verdict on the pilot's whole defensive layer. | read `?Install@Skill_PassiveShield@GAME@@…` `0x00418440` and whatever `SkillBuff::Install` `0x10433cf0` pushes into `SkillManager+0x88`; that establishes the `Skill_* → SkillBuff_*` instantiation edge once for all classes. |
| **`R-D10-2`** | The pilot's **`defensiveManaBurn` (enum 12)**. `disruption_resist = 30` and `energy_leech_resist = 0` are on the sheet; a mana-burn resistance line is not. The § 4.3 figure of **257.6** therefore assumes `defensiveManaBurn = 0`, **stated as an assumption, not measured**. | GD's character sheet does not print a separate mana-burn resistance row; `pm2_measured_player_sheet.csv` has no such stat. | the `.gdc` save block (the lane `2026-08-23-eorwarlguts-save-decode` opened), or a `DefenseAttributeStore` read on the pilot record. |
| **`R-D10-3`** | **Was Grava'Thul present at the referent's wave-160 death?** § 4.2 establishes only that wave 160 sp 2 is the first and only tier-≤16 offer, at p = 1/5. | reachability is a substrate fact; presence is a **video** fact, and inferring it from p = 0.20 would be exactly the laundering `L-50` struck. | the wave-160 segment of the referent footage (`pm4k_death_anchor.csv` locates the death anchor); a single nameplate frame settles it. |
| **`R-D10-4`** | **Does a mana-starved channel stop, and does that stop trip the D-8 latch?** Decoded: a mana-out is **not** among `StopCurrentSkill`'s seven callers, and `SkillChanneled::Update` does not check mana. | the availability path is not polled per tick from the controller in this build — the **only** indirect call through vtable `+0x148` (`SetAvailability`) in all of `.text` is inside `Player::PostPetSpawn` `0x0032c8ad` (`evidence/step25_…txt`), which is itself evidence, not a gap. | `SkillActivatedSpell::Update` / `SkillChanneled`'s mana-drain tick, and `Skill::IsManaAvailable` `0x003bf780` call sites. |
| **`R-D10-5`** | Whether the nullification's `skillActiveDuration = 5.0` means the `ManaBurnDrain` **re-applies** over 5 s or fires once at `Install`. § 4.3's 257.6 is **per application**. | `Install` runs the attack limb once; the buff's own tick behaviour was not read. | `SkillBuff::Update` / the `SkillBuff` lifetime path off `0x10433cf0`. |

---

## § 7 · WHAT THIS HANDS FORWARD

**To `MD-B4-1` / `C-B4-4` (B-4, gamora).** Both questions answered. `Disruption` `min` is **seconds**;
`ManaBurnDrain` `min` is a **percent of mana limit**. Neither is on the health-damage lane (`GetTotalDamage`
is a no-op on both), so **no `NON_HEALTH_DAMAGE_TYPES` entry can raise damage and none is needed to prevent
one**. `Disruption`'s player resistance is **measured at 30 %** on the pilot's own sheet, applied by
`ReduceDamage@CombatAttributeAbsDamage` — the exact function D-7 decoded — so a `RESIST_PCT` entry for
`Disruption` would be **measured, not invented**. `ManaBurnDrain` needs `R-D10-2` before it gets one, or it
enters as `NON_HEALTH` with the drain modelled on the energy lane.

**To PM5 (Wave 3) — three prereg-shaped rows.**
1. **A hard partition:** no residual below wave 160 can involve these rows. The armed rows are *unreachable*,
   not merely unrolled, on the current terminal band.
2. **A dated latency, not a distant one:** `C-B4-4`'s zero holds only while the sim terminates below 160. The
   first wave past the current band carries a **0.20 per-run** halt.
3. **The spike lane narrows, and the narrowing is the finding:** Disruption **cannot** be the defence-drop
   spike (§ 3, seven call sites). If a spike-driven death is to be attributed to this body, the candidate is
   the **charge's 1,863 raw multi-target hit plus the 1.4 s escape-denial**, and/or the **nullification's
   buff-strip** (`R-D10-1`) — not the 2 s duration on the damage lane.

**To the game tracker — one design law, decoded twice from unrelated directions.**
> **A GD lockout never takes the counterplay of last resort.** D-7 § 3.3: items and instant-cast pass through
> *every* control state. D-10 § 2.2: `Skill_ChargePotion` and `Skill_Evade` are the only two activated classes
> that reset `+0xca` to 0 and are therefore immune to Disruption. Two mechanisms, two code paths, one rule.
> A lockout in *Reincarnated* that takes the panic button is off-genre by decoded precedent, not by taste.

**To the run close — one harvest candidate, offered not self-adopted.**
> *A vtable slot number is only a name inside the class family where the name was verified.* Both
> self-disclosures in this lap are the same error at two depths: a one-hop read of a two-hop dispatch (§ 5.3)
> and a cross-family read of a non-aligned slot (`R-D10-1`). Both would have shipped a confident, wrong,
> *plausible* row — which is the exact failure class the two-model split exists to prevent. The instrument
> that caught both was **resolving the slot on more than one vtable and comparing**, which costs one command.

---

*legolas · KC2-MC Wave 2 · lap D-10 · 2026-08-24 · read-only throughout; no push.*
