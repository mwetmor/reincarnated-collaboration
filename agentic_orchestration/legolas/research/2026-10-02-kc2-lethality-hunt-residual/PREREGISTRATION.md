# PRE-REGISTRATION: GD's monster AI rule (stop range, attack stand, swing pause, skill choice) on the v3.8 oracle

**Agent:** legolas (UNKNOWN-RESEARCHER) · **Commissioner:** gandalf, KC2-PLAY residual hunt (after KP-208), with Matt's direction on lead 1 relayed by gandalf
**Written:** 2026-10-02, before any counterfactual of the decoded AI rule was run. **This file is committed ALONE.** Every result file comes in a later commit.
**Labels:** DATAMINED · FOOTAGE · SIM · INFERRED.

## 0. What ran before this file, and what I saw

- **The CONTROL** (the v3.8 oracle of record, `Folds("V38-FULL")`, salts 0–19) was re-run twice on an isolated `git archive` snapshot of engine `a40e609b` (the KP-208 head).
  - Both runs reproduce gamora exactly: ×2.3896, first death in w160 on 20/20 salts, same times into the wave.
  - The second run (`CTRL2.json`) adds two **inert** instruments: landed damage by hit distance, and moving-vs-still body steps by distance band. Its outputs are identical to the first run's.
- **Crash-only smoke tests** ran on salt 0 for arms SP, DEF, AIFULL, DOTDIV, C11B and ROSTER. They printed only "ran" and the mechanism counters (for example, how many swings the pause gated and how many defaults fired). No ratio, death wave or landed figure was printed or read.
- **The analyses below use the control only.** No counterfactual output was read.

## 1. The rule, as decoded (DATAMINED: Edition IV `Game.dll`, 32-bit, sha `e75925d1…`; listings follow in `evidence/`)

| # | element | decoded behaviour | address |
|---|---|---|---|
| R1 | Pursue exit | `Pursue::OnBegin` and **every** `Pursue::OnUpdate` call `CloseEnoughToUseSkill(target, chosenSkill)` (vtable +8). If true, the state becomes **"Attack"**. Monsters have no separate stopping range. | `0x0ff41b`, `0x0ff9e1` |
| R2 | Pursue movement | `MoveTo(GetMoveToPoint(target, skill))`. `GetMoveToPoint`'s attack-slot branch is partly decoded. **Exit is governed by R1 whatever the destination is.** Walk/run switches at `Monster+0x3068` (walkDistance): a speed switch, not a stop. A `PursuitTime` timer leads to "Return". | `0x0ff37d`, `0x0ff4f4` |
| R3 | Attack state | `Attack::OnBegin` calls `ControllerAI::Idle()`, so **the body stands**. There is a 10 s safety timeout (`0x2710`), after which the body goes to "Return". | `0x1007f6` |
| R4 | swing pause | The skill fires only when the swing timer `ControllerMonster+0x2f8` ≤ 0 (`Attack::OnUpdate` → `AttackEnemyOrReturn`). The timer is rerolled at each swing as `IGenerate(minSwingPause×1000, maxSwingPause×1000)` ms (D-3 Rule A). It counts down in `ControllerMonster::Update` **unless the current action is a UseAction (7)**, so it also counts during the attack animation. **The next swing therefore comes at max(animation, pause).** | `0x1009e4`–`0x100a17`; `0x0f6735`–`0x0f675d` |
| R5 | after each skill | `ChooseBestSkill(target, false)` runs. If the body is in range of the new skill, it stays in "Attack". If the new skill is the same one, "RepositionForAttack" is rolled at `randomRepositionChance` %. Otherwise the body goes to **"Pursue"**. | `0x100a35`–`0x100ade` |
| R6 | skill choice | `ChooseBestSkill(target, inRange)` takes the **first special** (8 slots, in order) that passes all of: delay ≤ 0, timeout ≤ 0, `rand()%100 < chance`, enabled, and the `IsSkillInProperRange` band. If none passes, it falls back to **Normal** (`+0x3bc` = record `attackSkillName`), then to **Default** (`+0x3b8` = `LoadDefaultSkills()` = `records/skills/default/defaultweaponattack.dbr`, `weaponDamagePct 100`, no `distanceProfile`, so Melee). Pursue and Attack call it with `inRange = false`, so the chosen skill may be out of range, and the body then walks to it. Pursue re-chooses every 200 ms (timer `0xc8`). | `0x0f83d0`; `InitSkillsInController` `0x2da1e0`; `LoadDefaultSkills` `0x43b470` |
| R7 | acquisition | `FindEnemyUpdate` scans every 200 ms (`+0x290`, adding `0xc8` each time). The timer is 0 at construction, so the first scan runs on the first update. **Acquisition latency is therefore below 200 ms (plus one update) once a body is eligible**, and is no longer UNKNOWN. | `0x0fc146`, ctor `0x0f58f9` |
| R8 | `initial` slots | `UseInitialSkillIfSet` (Startup `End`) runs `AddTemporaryState("UseSkillOnAlly", target = SELF, skill = initial)`. **This is a single self-cast at startup.** It is never an aimed attack, so it has no fire range. | `0x0feb90` |
| R9 | SlowChaos / SlowAether | The vtable slot 10 of `DamageAttributeDur_Chaos` and `_Aether` is `DamageAttributeDurBaseElemental::AddDamageToAccumulator`, the same entry Fire, Cold, Lightning, Poison and Life use. It constructs `CombatAttributeDurDamageElemental`, so these types share SlowFire's equation (`magicalDurationDamageEquation`, int/200). | vtables `0x5ca138` / `0x5ca064`; ctor call `0x14493a` |

**Melee vs caster behaviour comes only from the chosen skill's range** (R1 + R6; ladder from the range audit). Pursue and Attack read no controller "stop range". Controller parameters affect walking speed (R2), cadence (R4) and repositioning (R5), not where the body stops.

### Where the oracle departs

| rule | oracle (v3.8 of record) | GD | direction (INFERRED) |
|---|---|---|---|
| R1/R3 | every body walks to **2.4 m**; casters walk in while firing | the body stops at the chosen skill's range and stands while attacking | casters stay out of the 3 m leech disc → less heal, slower kills: **UP** |
| R4 | swing every `basic_swing_period_s / 1.11`; **the pause is omitted** (the pack's own row `V4-ANTI-1` says the oracle reads no SwingPause) | max(animation, pause) | **DOWN** |
| R6 order | **basic first**: a special fires only outside basic reach | specials first, then Normal, then Default | **UP** at melee range (specials fire when ready) |
| R6 tail | no Default: **112 of the 177 roster bodies** (fixed draw, w151–160) have no Normal; e.g. `ghost_a01` has **no attack at all**, and `ghost_b01` attacks only every 8 s | Default weapon attack (natural weapon damage) | **UP** |
| R8 | non-aura `initial` fires as a repeating slot at packed reach | one self-cast | DOWN; ≤ 0.2 % of the control's landed (top-25 skill grain) |
| R9 | `a_dur = 1.0` | int/200 + 1 | UP. **Population on the v3.8 oracle: 0 rows**, because `n_dot_rows_a_dur_undecoded` never increments in the control |

## 2. The arms (implemented in memory as harness patches; engine untouched; `tools/arms_extra.py` sha `e6357b7e…`)

| arm | content |
|---|---|
| **SP** | R4 only, on the incumbent selection and movement. Next opportunity = swing tick + max(n, ⌈pause·12.25⌉), with pause drawn per swing from **Ed II** `min/maxSwingPause` (124/124 records found; 77/77 agree with the oracle's own pinned CSV). The toggled-aura cadence is unchanged. |
| **DEF** | R6 tail only. A Default slot is synthesised for roster profiles with no `basic` or `chain_initial`. Reach = 1.25 + r·scale + 0.336 + 0.5. Damage = the body's own `weapon_rows`. |
| **AIMOVE** | R1 + R3 + R5 + R6 (with DEF) for roster bodies; **no R4**. Specials are chosen in slot order (special1–5, then `tree_attack` as the oracle does). The chance roll uses a dedicated RNG. Cooldown/delay, timeout and band are the oracle's own gates. Re-choice every 200 ms in Pursue and after each skill. The body walks to the chosen skill's reach and stands while in reach and during the animation (proxy: its swing period). `initial` slots are excluded (R8). Pets keep the oracle's rule. |
| **AIFULL** | AIMOVE + R4 (pets also get R4). **This is GD's AI rule as decoded, in full.** |
| DOTDIV | R9. |
| C11B / C11B-B | C-11b B: +10 % dex and int (DB-sourced exact). C11B additionally applies A as the C-11b mean ×1.010 (declared approximation; no per-record table is committed). |
| ROSTER | Diagnostic. The roster is re-drawn per salt (salt 0 keeps seed 9). The oracle replays **one** roster draw per wave on every salt (`engine_seed(CONDUCTOR_SEED=9, w)`). |
| ALLDEC | AIFULL + DOTDIV + C11B-B. |

**Declared, not modelled:**
- RepositionForAttack (a strafe), the walk/run switch, and `GetMoveToPoint`'s slot geometry;
- the initial swing timer at Load (taken as 0);
- per-skill animation lengths (the swing period is the proxy);
- pets under R1/R3/R6;
- 88 pool profiles lack a radius or weapon rows (Default reach falls back to r = 0.5 there; damage 0 where there are no weapon rows).

## 3. Predictions (from the rule plus the control's attribution; numbers in `prediction_numbers.json`, sha `bbf7544e…`)

**Control, for reference** (SIM, `CTRL2.json` sha `b32f62b0…`):
- ratio ×2.3896; first death in w160 on 20/20 salts, 4.3–9.0 s in (mean 6.92).
- per-wave median first hit 4.4–7.6 s (w160: 2.65).
- landed by hit distance: 42.5 % from beyond 5 m, 27.6 % from beyond 7.5 m.
- still fraction of body steps by band, in metres: 0–2.46 m: 1.00 / 1.00 / 1.00 / 0.60; 2.46–3.28 m: 0.60; 3.28–4.92 m: 0.05; 4.92–7.38 m: 0.10; 7.38–11.48 m: 0.16–0.17.

**Referent** (FOOTAGE, Lap H-2 range profile, plates ≤ 1,400 gpx): still fraction 0.20 / 0.23 / 0.28 / 0.28 / 0.34 / 0.35 / 0.24 / 0.15 over the same bands. **Bodies in the referent stand at 3–7 m about a third of the time.**

| # | quantity | arm | prediction |
|---|---|---|---|
| P1 | ratio | SP | **×1.75–2.05** (first order: ×1.90; per-wave multipliers 0.67–1.00) |
| P2 | first death / time into w160 | SP | first death in w160 on ≥ 15/20 salts; **8–13 s in** (first order: 6.92 / 0.68 = 10.2 s) |
| P3 | ratio | DEF | **UP: ×2.45–3.0**; some salts may first die before w160 |
| P4 | ratio | AIMOVE | **UP vs control: ×2.5–3.2** (specials first + Default + standoff each push up) |
| P5 | ratio | AIFULL | **×2.0–2.6** (≈ AIMOVE × the SP factor) |
| P6 | time into w160 | AIFULL | **8–14 s**; still dies in w160 on ≥ 15/20 salts (the nemeses stand off; the disc stays near empty; the wraiths arrive late) |
| P7 | standoff (hit distance) | AIMOVE, AIFULL | landed share beyond 5 m rises from 0.425 to **0.50–0.65**; the median band moves from 3.5–5 m to **5–7.5 m** |
| P8 | still fraction at 3.28–7.38 m | AIMOVE, AIFULL | rises from 0.05–0.10 to **≥ 0.25** (toward the referent's 0.34–0.35). At 0–2.46 m it stays ≥ 0.8: **no convergence there is expected**, because the referent's 0.20–0.28 reflects contact jostling, which the oracle does not model |
| P9 | per-wave first hit | AIMOVE, AIFULL | **later than or equal to the control**: median shift +0.0 to +1.5 s per wave (the first hit now needs the CHOSEN skill in range, not any slot) |
| P10 | ratio | DOTDIV | **identical to the control** (population 0) |
| P11 | ratio | C11B-B | **UP by +3 to +8 %** (additive form: Δrow ≈ 0.1·a/(a + P); 193/344 actors have no attribute term) |
| P12 | spread of the pooled ratio over roster draws | ROSTER | **±15–30 %**; the per-wave ratios move far more (w158 is two skeleton heroes; w152 is one thornedhorror) |

**Pass/fail rule:**
- Each prediction is graded HIT or MISS against its stated interval.
- **No arm is adopted or rejected on its ratio.** The fold recommendation follows the decode grade alone (§ 1).
- The referent is the TEST of the rule, not a target.
