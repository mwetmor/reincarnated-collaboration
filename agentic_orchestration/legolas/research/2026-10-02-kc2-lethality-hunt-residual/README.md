# Research: KC2 lethality hunt, the residual leg (on the v3.8 oracle of record, ×2.390), 2026-10-02

**Mode:** A (analytical: `Game.dll` primary-source decode, footage-trace measurement, oracle counterfactuals)
**Commissioner:** gandalf (RUN-CONDUCTOR), KC2-PLAY after KP-208. Lead 1 was sharpened by Matt's hypothesis ("no stopping range; AI state, perception and attack ranges drive it"), relayed by gandalf as a structured test.
**Agent:** legolas (UNKNOWN-RESEARCHER). **Read-only everywhere.**
- Every run used an isolated `git archive` snapshot of engine `a40e609b` (the KP-208 head; star-lord moved the engine to `affaaa05` concurrently). No engine, pack or vendor file was touched.
- Every arm is ⚑ **NOT-A-GRADED-RUN**: salts 0–19, the paired Δ against the control, t95.

**Labels:** DATAMINED · FOOTAGE · SIM · INFERRED.

**Pre-registration:** `PREREGISTRATION.md`, committed **alone** at collab `7330e2461` before any counterfactual of the decoded AI rule ran. The arm code it pins (`tools/arms_extra.py`, sha `e6357b7e…`) is unchanged. Arms added after it are marked **POST-REG**.

**Sources consulted**
- `Game.dll` Edition IV, 32-bit, sha `e75925d1…` (`/Users/admin/Games/vendor/grim-dawn-edition-IV-20260929/`). Listings are in `evidence/01–14`.
- Edition II records (`gdlib` reader from the range audit): controllers (`min/maxSwingPause`), `records/skills/default/*.dbr`, `combatformulas.dbr`, `mutator_monster_*.dbr`.
- The referent HP trace (Lap Q `pm4q_hp_trace.csv`) and Lap H-2's wave boundaries, range profile and tracks; Lap S's plate arrival stats; the KP-203 footage plate reads.
- The oracle `kc2/` at `a40e609b` and gamora's `gamora_kc2_play_v3p8_oracle_2026_10_02.py`, imported unchanged.
- Prior findings: the 10-01 lethality hunt, the range audit, D-1, D-3, D-11, C-11a/b/c, KP-201…208.

---

## Summary

1. **Lead 1 (wave-start engagement): the premise is refuted on the v3.8 oracle.**
   - The oracle's per-wave first hit comes **later** than the referent's, not earlier: median 4.4–7.6 s, against the referent's 0.35–10.5 s, median about 4 s.
   - GD's acquisition latency is now decoded: below 200 ms.
   - **Matt's hypothesis is confirmed in the binary.** GD has no monster stopping range. A monster pursues until `CloseEnoughToUseSkill` holds for the skill `ChooseBestSkill` chose, then stands (`Idle()`) while attacking. Melee versus caster behaviour comes only from the chosen skill's range. (DATAMINED A)
2. **A decoded rule the oracle omits: the swing pause.**
   - Every swing rerolls `IGenerate(minSwingPause, maxSwingPause)` ms. The next swing comes at max(animation, pause).
   - The pack even carries a prohibition row against porting it, because the oracle never read it.
   - **×2.390 → ×2.015 (−0.37 [−0.42, −0.33]).** Seven of 20 salts die in w160; 13 survive it. (DATAMINED A + SIM)
3. **The largest single term is not a mechanism.**
   - The oracle replays **one roster draw per wave** (`engine_seed(9, w)`) on every salt, and that draw is extreme. Re-drawing the roster per salt gives **×1.68 ± 0.23** (salts 1–19), and every one of those 19 draws is below seed 9's ×2.38.
   - The w152 (×4.3) and w158 (×7.6) spikes are the seed-9 board (one thornedhorror; two skeleton heroes).
   - The referent's w152 plate names a hero the oracle's w152 does not have. (SIM + FOOTAGE)
4. **GD's AI rule in full** (stop at the chosen skill's range, stand in Attack, specials first, Default fallback, swing pause) **cannot be judged apart from the pilot.**
   - The rule lowers the intake rate: ×1.60 on seed 9; ×0.74 on re-drawn rosters.
   - But the oracle's board-blind K-MILL pilot never closes on the casters it leaves standing, so waves stall (w152 runs 42–223 s against the referent's 16 s). The player then dies of attrition in **w152** (seed 9, 19/20 salts).
   - On standoff, the rule moves the oracle toward the referent: in the referent, bodies stand at 3–7 m about a third of the time. The control shows 5–10 %; the GD rule shows 52–64 %. It overshoots because the pilot never comes.
5. **The residual after the certain corrections** (roster-averaged, swing pause, C-11b B) is **×1.66 ± 0.23**. It concentrates on w151 (×2.7 own-wave), w156 (×2.35), w159 (×2.34) and w152 (×2.0).
   - The four unidentified monster mutators push UP; the pool alone bounds them.
   - **The open quantity that now decides the number is the pilot under GD's AI.** Under the incumbent walk-in it is ×1.66. Under GD's stand-off with today's pilot it is ×0.74. The referent's ×1.0 lies between.

---

## Lead 1: Matt's structured test (wave-start engagement and stopping range)

### 1.1 The decode (DATAMINED, grade A unless marked; addresses are RVAs in `Game.dll` IV 32-bit)

| question | answer | where |
|---|---|---|
| Pursue movement target and exit | It moves to `GetMoveToPoint(target, skill)`. That function's attack-slot branch is partly decoded (B). **Pursuit ends when `CloseEnoughToUseSkill(target, chosenSkill)` holds.** The check runs in `OnBegin` and on **every** `OnUpdate`, and the state then becomes "Attack". There is no separate stop field. | `Pursue::OnBegin` `0x0ff41b`; `OnUpdate` `0x0ff9e1`; listings 01, 02 |
| Movement inside Attack | `Attack::OnBegin` calls `ControllerAI::Idle()`, so **the body stands; it does not strafe, keep closing or kite**. After each skill it re-chooses. If it is in range of the new skill it stays (and, if the new skill is the same one, it rolls `randomRepositionChance` for "RepositionForAttack"). Otherwise it goes back to "Pursue". A 10 s safety timeout leads to "Return". | `0x1007f6`, `0x100a35`–`0x100ade`; listing 03 |
| Cadence | The skill fires when the swing timer `+0x2f8` ≤ 0. The timer is rerolled each swing as `IGenerate(min×1000, max×1000)`. It is decremented in `ControllerMonster::Update` unless the action is a UseAction (7), **so it also runs during the attack animation**. | `0x1009e4`–`0x100a17`; `0x0f6735`–`0x0f675d`; listings 03, 07, 08 |
| Skill choice | `ChooseBestSkill(target, inRange)` takes the first of the 8 specials that passes delay, timeout, chance, enabled and the `IsSkillInProperRange` band. If none passes it falls back to **Normal** (`+0x3bc` = `attackSkillName`), then **Default** (`+0x3b8` = `LoadDefaultSkills()` = `defaultweaponattack.dbr`, `weaponDamagePct 100`, Melee). **Pursue and Attack pass `inRange = false`**, so the chosen skill may be out of range and the body walks to it. Pursue re-chooses every 200 ms. | `0x0f83d0`; `InitSkillsInController` `0x2da1e0`; `LoadDefaultSkills` `0x43b470`; listings 04, 09, 10 |
| Perception, chase, leash | `ViewDistance` (80 m on the roster), `PursuitTime` (leads to "Return"), `MaxPursuitDistance`. These were loaded and decoded by earlier laps (Lap U, D-3); confirmed in `ControllerMonster::Load`. | listing 08 |
| Order and latency | Idle → `FindEnemyUpdate` (every **200 ms**: timer `+0x290` starts at 0 at construction and adds `0xc8` each time) → `DefaultEnemyFoundResponse` (Pursue first; then an AlertBeforePursue overlay at `alertAnimChance`, per D-1) → Pursue → Attack. **The "UNKNOWN acquisition latency" is below 200 ms plus one update.** | `0x0fc146`; ctor `0x0f58f9`; listing 06 |
| Melee vs caster | **Only the chosen skill's `distanceProfile`** sets it (ladder + radii + 0.5; range audit L1–L6). No controller field sets a stopping distance. `walkDistance` (`+0x3068`) only switches between walking and running. | listings 01, 02 |
| Non-aura `initial` slots (lead 6) | `UseInitialSkillIfSet` runs at the end of Startup and executes `UseSkillOnAlly(target = self, initial)`. **It is a single self-cast: no aim and no fire range.** | `0x0feb90`; listing 11 |

### 1.2 The referent measurement (FOOTAGE)

**First hit per wave.** Times are the first decrement of 100 HP or more after Lap H-2's counter increment. Under Lap S A-5 the counter increments inside `SpawnNext`, so the boundary is the spawn.

| wave | 151 | 152 | 153 | 154 | 155 | 156 | 157 | 158 | 159 | 160 |
|---|---|---|---|---|---|---|---|---|---|---|
| referent (s) | 5.67 | **10.47** | 3.72 | 3.22 | 4.95 | 0.53 | 2.02 | 4.22 | 4.07 | 0.35 |
| oracle control, median [range] (s) | 5.88 [4.8, 6.1] | 5.63 [2.9, 7.1] | 5.27 | 6.82 | 7.55 | 6.98 | 4.37 | 6.29 | 4.69 | 2.65 |

- **The oracle engages later than the referent in 8 of 10 waves.** w152 is the only clear exception.
- The matched first-10-s windows show the control's excess is **mostly after 10 s**. For example, w151's ratio over the first 10 s is ×5.6, but w153 ×1.3, w154 ×1.1, w155 ×1.0 and w160 ×0.9 (`results/arm_CTRL2.json`; `tools/analyse_timing.py`).

**Standoff.** Lap H-2's range profile (339 tracks, plates ≤ 1,400 gpx, 122 gpx/m) gives the still fraction by band. The oracle's equivalent is an inert observer on `Mover.step`, counting body steps with travel = 0.

| band (m) | 0–0.8 | 0.8–1.2 | 1.2–1.8 | 1.8–2.5 | 2.5–3.3 | 3.3–4.9 | 4.9–7.4 | 7.4–11.5 |
|---|---|---|---|---|---|---|---|---|
| **referent** (FOOTAGE) | 0.20 | 0.23 | 0.28 | 0.28 | 0.34 | **0.35** | 0.24 | 0.15 |
| control (SIM) | 1.00 | 1.00 | 1.00 | 0.60 | 0.05 | **0.10** | 0.16 | 0.17 |
| AIFULL (SIM) | 1.00 | 1.00 | 1.00 | 0.98 | 0.64 | **0.54** | 0.54 | 0.58 |

- In the referent, bodies stand at 2.5–5 m about a third of the time. The oracle's walk-to-2.4 m rule allows that only through holds (5–10 %).
- Inside 2.5 m the referent's 0.20–0.28 is contact jostling (Lap H-2: tangential flow dominates the ring), which neither oracle variant models.
- **Hit distance:** the control lands 42.5 % of monster direct damage from beyond 5 m; AIFULL lands 62 %.

### 1.3 Predictions against results

Pre-registered (`7330e2461`); the numbers come from `results/`.

| # | prediction | result | grade |
|---|---|---|---|
| P1 | SP ratio ×1.75–2.05 | **×2.015** | HIT |
| P2 | SP: first death in w160 on ≥ 15/20 salts, 8–13 s in | 7/20 die in w160, at 7.6–10.4 s; **13/20 survive w160** | MISS (more survival than predicted) |
| P3 | DEF UP, ×2.45–3.0 | **×2.292** (−0.10 [−0.16, −0.04]) | MISS. INFERRED cause: under the oracle's **basic-first** order, a new Melee Default pre-empts specials inside its reach |
| P4 | AIMOVE UP, ×2.5–3.2 | **×1.790**; first death **w152** | MISS |
| P5 | AIFULL ×2.0–2.6 | **×1.603** | MISS |
| P6 | AIFULL: dies in w160, 8–14 s in | first death in **w152** on 19/20 salts, 32–38 s in | MISS |
| P7 | AI arms: share of landed beyond 5 m 0.50–0.65; median band 5–7.5 m | AIFULL 0.62, band 5–7.5 m; AIMOVE 0.65, band 7.5–11.5 m | HIT (AIFULL); partial (AIMOVE) |
| P8 | AI arms: still fraction at 3.3–7.4 m ≥ 0.25; inside 2.5 m ≥ 0.8 | 0.52–0.64; inside 2.5 m 0.97–1.00 | HIT. Overshoots the referent's 0.24–0.35 |
| P9 | AI arms: first hit later than or equal to the control | AIFULL is earlier in 5 of 10 waves | MISS |
| P10 | DOTDIV identical | byte-identical ×2.3896 | HIT |
| P11 | C11B-B +3 to +8 % | **+7.8 %** (×2.577) | HIT |
| P12 | ROSTER spread ±15–30 % | sd ±14 % about a **mean of ×1.68**, range 1.38–2.07 | HIT on spread; **the −28 % shift in level was not predicted** |

**What the misses have in common: P2, P4, P5, P6 and P9 all come from one effect the pre-registration did not foresee.**
- Under GD's stand-off, the oracle's pilot (K-MILL, board-blind by decode, kinematics § 0) does not close on standing casters.
- Waves stall: AIFULL w152 runs 42 s (223 s on re-drawn rosters), w155 runs 93 s, against the referent's 13–26 s.
- With few bodies in the 3 m disc there is little leech. The player dies of attrition rather than burst.

**POST-REG AIFULL-P** widens the oracle's own JC-G9 collect rule to standing bodies. It gives ×1.885 and still dies in w152, because the rule needs every live body standing and no live pet. **The pilot is not GD code: GD has no player AI, and the referent's pilot is Matt.**

### 1.4 Verdict on lead 1

- **Engagement onset is not a lever. The oracle already engages late.**
- **The stop rule is real and decoded** (A): pursue to `CloseEnoughToUseSkill`, then stand. The referent's standoff signature points the same way.
- **Adopting it is coupled to the pilot.** Folding R1/R3/R6 without a pilot that engages standing bodies produces a w152 death the referent does not show. Rejecting the rule on that basis would be fitting. **The right ruling is to fold it together with a pilot repair** (gamora's seam; the conductor's call).

---

## Lead 2: the per-wave residual on the new oracle, and the roster

Ratios against the referent's own per-wave rate (SIM against FOOTAGE; `results/perwave_residual.json`):

| wave | ref hp/s | ref T (s) | control (seed 9) | ROSTER, salts 1–19 | SP\|R | SP+C11B\|R | top control attackers (seed 9) |
|---|---|---|---|---|---|---|---|
| 151 | 1,220 | 15.6 | ×3.93 | ×2.58 | ×2.49 | ×2.71 | ghost_b04/b03 `ghost_cadence` 51 %, plant `venomousseed` 16 %, swampgolem_h05 14 % |
| 152 | 766 | 16.3 | **×4.31** | ×1.78 | ×1.79 | ×2.01 | **thornedhorrorfrost_b01 47 %** (`iceshardburst` 33 %), ugdenbog crab 21 % |
| 153 | 1,394 | 14.9 | ×1.89 | ×1.20 | ×1.19 | ×1.26 | plant 37 %, giant_b01 18 % |
| 154 | 2,692 | 14.2 | ×2.29 | ×1.32 | ×1.14 | ×1.26 | nemesis_beast 33 %, eldritcharmor_c01 `firebreath` 25 % |
| 155 | 1,018 | 16.2 | ×1.61 | ×1.33 | ×1.24 | ×1.41 | aetherialcorruption_c01 44 % |
| 156 | 1,648 | 20.2 | ×3.96 | ×2.92 | ×2.18 | ×2.35 | janaxia `necroticmissiles` 30 %, chthonickurn shaman `chaosorb` 24 %, heralds 29 % |
| 157 | 2,167 | 19.3 | ×0.87 | ×0.75 | ×0.71 | ×0.75 | bloater `plaguepresence` 28 % |
| 158 | 288 | 13.0 | **×7.56** | ×1.47 | ×1.46 | ×1.57 | **skeleton_h09 + h08 66 %** |
| 159 | 2,318 | 26.3 | ×1.73 | ×2.17 | ×2.17 | ×2.34 | korvaak messenger 40 % |
| 160 | 4,070 | 25.0 | ×1.20 | ×1.73 | ×1.78 | ×1.86 | vanguard `arcanemissilenova` 52 %, Kymon 25 % |

- **The board is identical on all 20 salts.** Every record is present 20/20, because `replay` seeds every wave from `engine_seed(CONDUCTOR_SEED=9, w)`. The salt varies only kinematics, channel policy and the like. The control's per-salt sd (0.117) therefore **omits roster variance**.
- With rosters re-drawn (ROSTER; salt 0 keeps seed 9), salts 1–19 give **×1.680 ± 0.233, range 1.38–2.07**. **Seed 9 (×2.380) lies above all 19.** (SIM)
- **The referent's draw is not seed 9's** (FOOTAGE plate reads, KP-203):
  - w152's p05 hero is *Vanallius the Voracious* (`aetherialcorruption_h02`); the oracle's w152 carries `aetherialcorruption_h01` plus thornedhorrors;
  - w153 shows an Ugdenbog Golem (`swampgolem_a01`); the oracle's w153 shows giants and bounties.
- **Wave durations:** on re-drawn rosters with the incumbent movement (SP\|R) they are 14–23 s, against the referent's 13–26 s. On seed 9 they are 13–25 s.
- **Matched body counts** (INFERRED): the referent shows a mean of 8.6 living plates within the frustum; the control has a mean of about 4.3 bodies within 11.5 m. **At matched geometry, the oracle's intake per nearby body is about 4–5× the referent's.** The excess is per-body cadence and magnitude, not exposure.

---

## Lead 3: w160

On seed 9, salts 0–19 (SIM):
- **The intake rate is not the problem.** The w160 own-wave ratio is **×1.20** (4,892 against the referent's 4,070 hp/s).
- **The heal is.** The oracle heals 14.8 k HP per wave, about 2.1 k hp/s, all from Menhir's Will, the potion, regen and counterplay. There is **zero leech**: the disc averages 0.0–0.34 bodies.
- The referent heals about **103 k over 25 s (≈ 4.1 k hp/s)**, from Lap Q's trace, at N(disc) = 1.66 with 25 peak plates (Lap S).
- **The board:** the four seed-9 bodies (Kymon, Wendigo, Aetherial Vanguard, Korvaak statue) spawn 30 m out. The 30 pets (wraiths, crystals) walk in at pet speed and arrive after the player is dead.
- **The killer:** the Vanguard's `arcanemissilenova` (`Skill_AttackProjectileRing`, boomerang missiles) causes **13/20 kills** and 17.6 k of the last 3 s.
- **The empty disc is a board property, not a leech-law defect.** On re-drawn w160 boards 10/20 die in w160 and 9 survive. With the swing pause on seed 9, 13/20 survive w160.
- **Open:** the multiplicity of the nova's boomerang ring against a single target (the oracle lands one hit per cast). That is geometry, and it is not decoded here.

## Lead 4: the SlowChaos/SlowAether DoT divisor

- **Decoded** (DATAMINED A−):
  - `DamageAttributeDur_Chaos` and `_Aether` take vtable slot 10 = `DamageAttributeDurBaseElemental::AddDamageToAccumulator`, the same entry as Fire, Cold, Lightning, Poison and Life.
  - That function constructs `CombatAttributeDurDamageElemental` (call at `0x14493a`), whose `Process` has one equation path for every elemental DoT type.
  - **So the divisor is int/200, `magicalDurationDamageEquation`.**
  - The "−" in the grade is because the identity of the `+0x550` equation object with magicalDuration is inherited from C-11a and the composition leg, not re-traced here.
  - Listings 12–14.
- **Population on the v3.8 oracle: 0 rows.** `n_dot_rows_a_dur_undecoded` never increments in the control. Counterfactual DOTDIV is byte-identical (×2.3896).

## Lead 5: C-11b A+B and the four monster mutators

- **C-11b B** (+10 % dex and int; `monsterAttributePak` at Ultimate / 1 player; DB-sourced exact; applied through `GlobalMagnitudeFold.terms_for`): **×2.577, +0.185 [+0.143, +0.227]**. First deaths: 16/20 in w160, three at 156, one at 151.
- **A** (the record's own `charLevel` equation): no per-record table is committed, so it is applied as the C-11b mean ×1.010. **C11B (A+B) gives ×2.602.**
- With roster re-draw and swing pause (SP+C11B\|R): ×1.660 ± 0.229.
- **Mutators** (DATAMINED pool, INFERRED effect):
  - The referent ran six mutators, four of them monster mutators, **identities unrecorded** (C-11c). The Ed II pool has 17 monster mutators.
  - The large terms at monster level about 103–107 are flat adds of **≈ 185–190 per hit** (aether, chaos or pierce; physical 140) and DoT adds of about 150. Under the additive composition these scale by (a + P/100) ≈ 6–7 before resistances.
  - Other terms: attack speed +6/+12/+15 %; `offensiveDamageMultModifier` +5; cooldown −15 %; life +6/+12 %; regen; slows.
  - A random four contains about one flat-damage mutator in expectation. **This plausibly pushes intake UP by 10–30 %** (INFERRED; not run, because the identities decide it).
  - **To settle it:** read the six-icon mutator row at t ≈ 684 s in the referent MP4. That needs the Pi share mounted (Matt).

## Lead 6: non-aura `initial` slots

- **GD's rule is settled:** a single self-cast at Startup (§ 1.1, `0x0feb90`). They are never an aimed, repeating attack, so the packed 90 m reach on `nemesis_eldritch_01` has no meaning as a fire range.
- **Size:** `initial` is 0.2 % of the control's landed (top-25 skill grain). The AI arms exclude it.
- If the self-cast is a toggled aura or an orbital buff, its effect is the aura or orbit radius around the caster, which v3.8 already gives auras.

## POST-REG: D-11's special gates (unfolded, decoded)

- **GATES** arms `gate_model.SpecialGateFold` in full: reuse = max(Delay, cooldown) (DOWN), plus a first cast gated by `Timeout`, counted from acquisition and one-shot (UP field half, DOWN anchor half). **Result: ×2.420, +0.03 [−0.02, +0.08]. Neutral.**
- SP+GATES: ×2.045.

---

## Ranked explanation of the residual (×2.390 on the oracle of record)

1. **The single roster draw: ×2.39 → ×1.68 ± 0.23** (SIM; high confidence in the size, and not a mechanism).
   - The w152/w158 spikes belong to the seed-9 board.
   - The referent is also one draw; its own draw uncertainty is about ±14 % (1σ).
2. **The swing pause: −16 %** (DATAMINED A + SIM; ×2.39 → ×2.02; on re-drawn rosters ×1.68 → ×1.53). Decoded and certain.
3. **GD's AI stop, stand and specials-first rule: the rate falls, by an amount the pilot decides** (DATAMINED A; SIM bracket).
   - It brings the oracle's standoff signature toward the referent's.
   - With today's pilot it gives ×1.60 (seed 9) and ×0.74 (re-drawn), with waves stalling.
   - Under the incumbent walk-in it is ×1.53–1.66.
4. **C-11b B: +7.8 % UP** (DB-sourced exact); **A ≈ +1 %**.
5. **Monster mutators: likely +10–30 % UP** (INFERRED from the pool; identities need footage).
6. **Neutral or zero:** D-11 gates (+1 %, noise); the DoT divisor (population 0); the Default fallback alone on the oracle's basic-first order (−4 %, an interaction); engagement onset (the oracle is already late).
7. **What remains on the certain set (1 + 2 + 4): ×1.66 ± 0.23.** It sits mainly on w151 (×2.7), w156 (×2.35), w159 (×2.34) and w152 (×2.0). Mutators push it up; GD's stand-off with a pilot that clears like Matt's pushes it down. **The referent's ×1.0 lies inside that bracket.**

## What should go into the oracle (decoded and certain) / what stays open

**Fold: decoded and certain.** Each item changes the oracle, so the conductor and Matt rule on each.
1. **The swing pause** (R4): next swing at max(animation, U{min..max} ms), rerolled per swing; Edition II values, 124/124 found and 77/77 matching the pinned CSV (`results/swing_pause_table.json`). **The pack's `V4-ANTI-1` "DO-NOT-IMPLEMENT-SWINGPAUSE" must be retired with it, or port parity breaks.**
2. **Evaluate over roster draws** (methodology, not mechanism). Run the oracle on several roster seeds, or recover the referent's own roster from footage plate reads (partial reads exist for w151–153 and w157). A single fixed draw cannot stand as the denominator's comparator.
3. **C-11b B** (+10 % dex and int), sourced and exact.
4. **Declared constants that can now be replaced by decodes:**
   - acquisition latency ∈ [0, 200 ms) (the 0 in use is inside the range);
   - SlowChaos/SlowAether int/200 (no numeric effect today);
   - `initial` = one self-cast at Startup (≤ 0.2 %).
5. **GD's AI rule** (R1 stop at `CloseEnoughToUseSkill` of the chosen skill; R3 stand in Attack; R5/R6 specials-first `ChooseBestSkill` with Normal → Default fallback): **decoded, but fold it only together with a pilot repair.** On its own it creates a w152 death the referent does not show. The arm code in `tools/arms_extra.py` is a working reference implementation, with these declared proxies:
   - the swing period stands in for animation length;
   - no RepositionForAttack;
   - no walk/run switch;
   - pets are unchanged.

**Open**
- **The pilot under GD's AI.** How does the player close on standing casters? This decides the final number (×0.74–1.66). It belongs to gamora's seam.
- **The four monster mutator identities.** They need the referent MP4 at t ≈ 684 s, i.e. the Pi share mounted. **gandalf: please ask Matt.**
- **The referent's roster per wave.** It needs more plate reads from the footage, or a decision to compare on expectations.
- **The 193/344 actors with no attribute term** (`gt.inert`, attribute = 1). In GD every monster has attributes, so this pushes UP; unpriced.
- **The boomerang-ring nova's hit multiplicity** (the w160 killer).
- `GetMoveToPoint`'s slot geometry; per-skill animation lengths; C-11b A per record.

## Files

| file | contents |
|---|---|
| `PREREGISTRATION.md` | the pre-registration, committed alone at `7330e2461` |
| `results/results_table.json` | every arm: ratio, paired Δ, first-death waves and times, roster-redraw statistics |
| `results/arm_*.json` | per arm: summary, per-wave, fold reports, first hit by wave against the referent, standoff instruments |
| `results/perwave_residual.json` | the lead 2 table |
| `results/swing_pause_table.json` | Edition II swing pause for 124 roster and pet records, cross-checked 77/77 |
| `results/prediction_numbers.json` | the inputs of the pre-registration |
| `evidence/01–14` | `Game.dll` listings: Pursue, Attack, ChooseBestSkill, GetMoveToPoint, FindEnemyUpdate, `ControllerMonster::Update`/`Load`, `InitSkillsInController`, `Monster::Load`, `UseInitialSkillIfSet`, the DoT accumulators, vtables and getters |
| `tools/` | `gdx.py` (disassembly) · `swing_pause_table.py` · `predict.py` · `hunt2.py` (harness and instruments) · `arms.py`, `arms_extra.py` (pre-registered arms) · `arms_post.py`, `hunt2_post.py` (POST-REG arms) · `analyse_*.py` · `pack_results.py`. They run against a `git archive a40e609b` snapshot with `PYTHONDONTWRITEBYTECODE=1`; the scratch paths in `H` are provenance. |

*legolas · KC2-PLAY residual hunt · 2026-10-02*
