# PRE-REGISTRATION: GD repositioning and contact jostling on the v3.9 oracle (legolas, 2026-10-02)

**Committed ALONE, before any counterfactual outcome was computed** (KP-209 law; commission after KP-216).
**Agent:** legolas (UNKNOWN-RESEARCHER). **Read-only everywhere.** **Labels:** DATAMINED · FOOTAGE · SIM · INFERRED.
**Binaries:** `Game.dll` Ed IV sha `e75925d1…8126`, `Engine.dll` Ed IV sha `f18e8658…fe24` (32-bit). Database: Ed II
(referent era), Ed IV cross-checked (0 of 544 records differ on any field used here).
**Oracle of record:** gamora `gamora_kc2_play_v3p9_oracle_2026_10_02.py`, `Folds39("V39-FULL")`, PW-FOLDED, graded arm
M-POL-2, fixed seed-9 line-up, salts 0–19; run from a read-only `git archive` of engine `86218701`.

**Pinned code (sha256):** `tools/rj_arms.py` `5d5d6279…08716` · `tools/rj_tables.py` `519838ad…c6a3` ·
`tools/rj_control_measure.py` `b39c5749…7240` · `results/gd_tables.json` `fa0b78b4…139c`.
Any later change to `rj_arms.py` is a disclosed bug fix, listed in the results with its diff and reason.

---

## 0. What ran before this file, and what I saw (disclosure)

1. **The control, only.** The `CTRL` arm (V39-FULL with the inert RJ instruments) reproduces gamora's published
   V39-FULL exactly: salt 0 ×2.5439 / w152; salts 0–19 ×2.3037, standing fraction 0.575 (KNOWN, gamora `d642ece49`).
2. **PRE-RUN MEASUREMENT on the control** (`results/control_premeasure.json`, behaviour unchanged):
   - m1: roster bodies in Attack with a Melee choice exceed 6 on 53 of 74,917 ticks; bodies with a Melee choice
     within 6 m exceed 6 on 1.3 % of ticks;
   - m2: of 15,506 skill completions, 5,999 re-choose the same skill in reach; 1,259 of those belong to records with
     `randomRepositionChance` 20 (none with 5 or 100 recorded);
   - m3: Attack → Pursue happens 691 times BEFORE the skill completes (the incumbent re-tests reach during the swing
     pause) against 5,249 at completion;
   - m4: the converging solver displaces a STANDING body 37,714 times, but pushes one out of its reach only 30 times;
   - **a second standing instrument on the control:** net world speed per tick (step + solver displacement) below
     the referent's own threshold (Lap H-2 `V_STILL` 50 gpx/s = 0.41 m/s) gives **0.761** at 2.46–4.92 m (the step
     instrument gives 0.575), 0.59–0.70 inside 2.46 m, 0.85–0.93 at 4.9–11.5 m.
3. **Counterfactual arms: crash-only, salt 0, mechanism counters only.** Smokes of RJ-RFA, RJ-SLOT, RJ-CROWD,
   RJ-PERSIST, RJ-CORE and RJ-FULL printed only whether they ran and these counters (salt 0, last build): RFA entries
   from Attack 7–10 (41–50 rolls); with SLOT, about 700 slot requests, 220–300 with no slot, 120–180 overrides,
   170–230 WaitToAttack entries, 70–100 RFA entries in total, 20–55 PathFailed events; with CROWD, 30–60 thousand
   displaced-mover events and ~20–30 displaced-stander events. **A state-transition trace of salt 0 (RJ-SLOT,
   `tools/rj_trace_diag.py`)** printed transition counts and four bodies' state sequences with their distances.
   **No ratio, death, wave duration, standing fraction, closing or disc figure of any counterfactual arm was
   computed, printed or read.**

---

## 1. The decoded rules (DATAMINED unless marked; addresses are Game.dll RVAs unless "E:" = Engine.dll)

| # | rule | grade | where |
|---|---|---|---|
| D1 | **RepositionForAttack trigger.** After a skill completes in Attack, `ChooseBestSkill` again; if still `CloseEnoughToUseSkill`, roll `rand()%100 < randomRepositionChance` (controller field, `+0x2e0`) `&& CanMove()`, once per Attack entry; RFA only if the re-chosen skill is the SAME skill, else re-enter Attack; out of reach → Pursue. A projectile that collides with something other than its target pre-sets the flag with `RepositionChance` (`+0x3b0`); a hit on the target clears it. | A | `0x100a1c–0x100abe`; `0x1013a0`, `0x1013f0`; Load `0x0f7cc1/0x0f7cd5` |
| D2 | **RFA movement.** `GetMoveToPoint(target, skill = 0)` → no-skill branch → `GetPointAwayFromGoal(targetPos, r_target + r_self)`: the point on the monster's own path to the target at body-contact distance. Run speed. Leave on arrival (`EndOfPathReached`: CloseEnough ? Attack : Pursue) or, after **2.5 s**, if CloseEnough → Attack. No skill use inside RFA. Path failure → walk to a random point **3–5 m from itself**. | A (B for the 3–5 m callee convention) | `0x1024b0`, `0x1025c0`, `0x1028b0`, `0x102a10`; `0x049a90` (branch `0x4a43d`); `0x077d20` |
| D3 | **Attack slots.** A skill whose `distanceProfile` is Melee (`NeedsAttackSlot` = `[skill+0x8c]==0`) requests a slot on the target. The player has **6** (`numAttackSlots`, malepc/femalepc), **one ring** (attack `SlotManager` constructed with SlotMode 0; extra rings only in mode 1, max 3). Ring radius = `GetTargetDistance` = 1.25 + r_m + r_p (no tolerance); slot j at the world-fixed angle 2πj/6. A request first frees the requester's own slot and dead occupants, then takes the **nearest free slot**; if none, it **overrides** the nearest slot whose occupant's (d² − e²)⁺ exceeds the requester's (e = `GetExtents`: Small 0.5 / Medium 1.0 / Large 1.75); the robbed body gets `LostSlot`. Slots are held until the holder requests again, dies, or is robbed (a body that switches to a ranged skill keeps its slot). | A | `0x460710`, `0x4602c0`, `0x460400`, `0x4604f0`, `0x460990`, `0x460bf0`, `0x0499b0`, `0x049100`; ctor `0x03f81c/0x03f839`; Load `0x0422d7` |
| D4 | **Move-to point.** `Pursue::OnBegin` calls `GetMoveToPoint` once and moves to that FIXED point (Melee: its slot point; otherwise r_target + ladder from the target on the straight line); no slot → **WaitToAttack** (before the CloseEnough test). Pursue ends as soon as CloseEnough holds. If the path ends out of reach (the player moved): release the slot → WaitToAttack. Path failure → release slot → RFA. `LostSlot` in Attack → Pursue (new request); in Pursue → re-request (none → WaitToAttack). Re-entry into Pursue on every change of the chosen skill (200 ms re-choose). | A | `0x0ff37d–0x0ff3a3`, `0x0ff783–0x0ff8a4`, `0x0ffcf0`, `0x0ffec0`, `0x101be0`, `0x100080` |
| D5 | **WaitToAttack.** Every **333 ms**: re-choose and `GetMoveToPoint` → a point (slot or non-melee) → Pursue; none → **50 %** RFA. Every **1 s** (and on entry): roam (run) to a random point at R from a centre placed R from the target toward the body, R = clamp(d, 4, 10)/2. No skill use. | A (B for the roam radius = R exactly) | `0x104cf0`, `0x104e00`, `0x1053a0`, `0x0fe4e0` |
| D6 | **Contact jostle (Engine.dll crowd).** Per crowd update, an overlapping pair displaces body i away from j by **0.35 × penetration**, averaged over i's eligible overlaps, iff `Depenetrate(i.state, i.prio, j.state, j.prio)`: a MOVING i yields to a standing j and to a moving j of priority ≤ its own; a STANDING i yields only to a standing j of higher priority. Monsters priority 1, player 2. Boss/Quest/SuperBoss and `forceCollision` monsters never yield. Hostile monsters collide with everything (group 2, mask 7); the player and friendlies only with hostiles. Moving monsters also steer apart (separation weight 1.1). | A (E: depenetration, groups); B (who "moving" is = crowd state 2) | E:`0x2080a2–0x208215`, E:`0x208d00` (mask), E:`0x20714a–0x20738a`; `0x052d70`, `0x2d70a0`, `0x2d6f20`, `0x2d6fb0`, `0x32fb30`, `0x0527d0` |
| D7 | **Crowd path failure.** A moving agent whose achieved speed stays below **1.1 m/s** for more than **400 ms**, or whose next step overlaps a body standing on its goal, is stopped; `CrowdAgentError` sets the action idle and calls the state's `PathFailed` (Pursue → RFA; RFA → random 3–5 m; WaitToAttack → idle until the next roam). Goal reached within **0.1 m**. | A | E:`0x208668–0x20873a`, E:`0x207da8–0x207f4a`; `0x052db0`, `0x2d7130`, `0x052cb0` |
| D8 | **Attack persistence.** In Attack the body stands; at swing-timer expiry `AttackEnemyOrReturn` uses the skill **without a range test**; range is re-tested only after the skill completes. | A | `0x1009e4–0x100a17`, `0x101410–0x101bca` |

**Nothing else moves an attacking monster** in the Attack state's code: `RequestMove` is a leader command (pets),
`HandleEvent` handles buffs/leash, stun/knockdown are separate temporary states (not decoded here).

---

## 2. The arms (named before any outcome), all on V39-FULL, salts 0–19, ⚑ NOT-A-GRADED-RUN

| arm | rules installed (in memory) |
|---|---|
| `CTRL` | none (inert instruments only; must equal V39-FULL) |
| `RJ-RFA` | D1 (Attack trigger) + D2, incl. RFA's own path failure (D7) |
| `RJ-SLOT` | D3 + D4 + D5 + D7 (+ the RFA they enter, D2) |
| `RJ-CROWD` | D6 depenetration rule in place of the oracle's symmetric converging solver |
| `RJ-PERSIST` | D8, with an **INFERRED** limb: a MELEE swing fired out of reach is a whiff (animation and pause consumed, no damage); a ranged skill launches |
| `RJ-CORE` | RFA + SLOT + CROWD |
| **`RJ-FULL`** | RFA + SLOT + CROWD + PERSIST (**the primary arm**) |

**Declared stand-ins (not decoded, or outside this lap):** pets keep the incumbent movement (and take no slots;
in GD melee pets would also occupy the player's 6 slots); the `RepositionChance` projectile-collision trigger is not
modelled (the oracle has no projectile collision with non-targets); the player stays fixed in the jostle (the pilot
owns its position; GD displaces a MOVING player); the 0.35 relaxation is applied once per oracle tick (GD's crowd
update rate is not decoded); the moving-monster separation steering (weight 1.1) is not modelled; slot-ring
orientation is arbitrary (θ_j = 2πj/6 in oracle coordinates); point-targeted skills (types 2–5, 7) use the same
line point as other non-melee skills; walk/run switching is not modelled (one mover speed); `CanMove` = not
stationary.

---

## 3. Predictions (from the decoded rules and the control measurements alone)

**Control (KNOWN):** ×2.304; first deaths w152 ×15, w156 ×2, w154 ×1, w160 ×2; w152 33.9 s, w155 28.5 s; standing
(step instrument) 0.575; closing 0.795 m/s; disc 1.661. **Referent (FOOTAGE):** standing 0.34, closing +0.92,
w152 16.3 s, w155 16.2 s.

| # | quantity (RJ-FULL unless named) | prediction | basis |
|---|---|---|---|
| Q1 | standing fraction 2.46–4.92 m, step instrument (oracle of record) | **0.38–0.52** (central 0.45) | bodies that reach Attack through RFA stand at body contact (0.8–1.5 m), outside the band; WaitToAttack bodies roam through it; m4 says the solver rarely un-stands anyone, so CROWD barely moves it; m3 says PERSIST adds ≤ +0.03 |
| Q1b | same, RJ-CORE | **0.36–0.50** (central 0.43) | Q1 without PERSIST |
| Q2 | standing 2.46–4.92 m, net-speed instrument | **0.50–0.70** (central 0.60) | control 0.761: stalled pursuers pushed back by the solver; D7 turns a stall into RFA / a random re-path within 0.4 s |
| Q3 | w152 mean duration | **22–34 s** (central 28) | 13 melee bodies on 6 slots: the overflow RFAs to contact, filling the player's reach and disc |
| Q4 | w155 mean duration | **18–30 s** (central 24) | 15 melee bodies (corruption_c01 ×7, imps ×8); same mechanism |
| Q5 | first-death waves (20 salts) | w152 on **4–12**; w160 on **4–12**; at least one salt outside {152, 160} | less attack time (RFA / WaitToAttack bodies do not attack) and more disc occupancy in w152; w160's four bosses are immovable and ranged (RFA chance 0), so w160 stays lethal |
| Q6 | ratio | **×1.50–2.25** (central ×1.90); RJ-CORE the same interval | attack time lost in RFA and WaitToAttack, partly offset by melee overflow reaching contact |
| Q7 | pilot-realised closing, empty disc | **0.70–1.10 m/s** (central 0.85) | the pilot rule is unchanged; bodies running in add closing, roamers add noise |
| Q8 | disc occupancy, bodies/tick, w151–159 | **1.8–2.8** (central 2.2) | RFA ends inside the 3 m disc |
| Q9 | standing inside 2.46 m, step instrument | **0.80–0.97** | control 1.00; roamers and RFA runners cross it |
| Q10 | decomposition, Δ standing (step, 2.46–4.92) / Δ ratio vs CTRL | RJ-RFA −0.04…−0.005 / −6 %…0 · RJ-SLOT −0.18…−0.05 / −30 %…−3 % · RJ-CROWD −0.02…+0.02 / ±4 % · RJ-PERSIST 0…+0.03 / ±4 % | m2: ~12.6 attack-RFAs per salt; smoke counters for SLOT; m4, m3 |
| Q11 | against the referent | RJ-FULL standing (step) still **above 0.34 by +0.04…+0.18**; w152 and w155 still **longer** than 16.3 / 16.2 s | the decoded rules close part of the gap; the pilot, the board and the instrument carry the rest |
| Q12 | mechanism counts per salt, RJ-FULL | attack-RFAs 6–20; WaitToAttack entries 100–300; LostSlot 60–250 | m2; smoke |

## 4. Grading

- Each row is HIT or MISS against its interval; a central value is not graded.
- **No rule is adopted or rejected on its effect on the ratio.** The referent tests the rules; nothing is tuned.
- Misses are reported with the mechanism that produced them, not re-predicted.
