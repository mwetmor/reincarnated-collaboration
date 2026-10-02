# Research: GD monster repositioning and contact jostling, decoded and run on the v3.9 oracle (2026-10-02)

**Mode:** A (analytical: `Game.dll` + `Engine.dll` primary-source decode; oracle counterfactual)
**Commissioner:** gandalf (RUN-CONDUCTOR), KC2-PLAY after KP-216 (Matt Q101: recover the line-up from footage; meanwhile decode repositioning).
**Agent:** legolas (UNKNOWN-RESEARCHER). **Read-only everywhere.** No engine, pack or vendor file was edited; runs used a `git archive` snapshot of engine `86218701`.
**Labels:** DATAMINED · FOOTAGE · SIM · INFERRED.
**Pre-registration:** `PREREGISTRATION.md`, committed ALONE at collab `b816e68e4` before any counterfactual outcome existed. Its disclosure section lists everything run beforehand (the control, control measurements, crash-only smokes, one mechanism trace).

**Sources consulted**
- `Game.dll` Ed IV, 32-bit, sha `e75925d1…8126`; `Engine.dll` Ed IV, sha `f18e8658…fe24` (`/Users/admin/Games/vendor/grim-dawn-edition-IV-20260929/`). Listings: `evidence/e01–e09`.
- Ed II database (referent era) through the range audit's `gdlib` reader; Ed IV cross-checked: 0 of 544 records differ on any field used (`results/gd_tables.json`).
- Lap H-2 method (`legolas/notes/2026-08-13-kc2-pm4-lap-h2-video-match/method/d1run.py`: `V_STILL` = 50 gpx/s) and range profile (FOOTAGE).
- The v3.9 oracle (gamora, engine `86218701`), imported unchanged; gamora's pass-2 results (`gamora/analyses/2026-10-02-kc2-v3p9-oracle-pass2/`).
- Prior: the residual hunt (`2026-10-02-kc2-lethality-hunt-residual`, evidence 01–14), the range audit (L1–L6).

---

## Summary

1. **RepositionForAttack is decoded in full (DATAMINED A).** After a skill completes, if the monster re-chooses the *same* skill and is still in reach, it rolls `randomRepositionChance`. On success it runs to **body contact** with the target. It leaves on arrival, or after **2.5 s** if it is in reach. The roll is 0 on 96 of 124 roster/pet records, 20 on ranged casters, 5 on imps and wraiths. WaitToAttack and Pursue path failures also enter it.
2. **The attack-slot geometry is decoded (A).** The player has **6** melee slots on one ring at radius 1.25 + r_m + r_p, at fixed world angles. Requests take the nearest free slot or rob a farther occupant. A melee body with no slot goes to **WaitToAttack**: it roams 2–5 m around a point between itself and the player, polls every 333 ms, and has a 50 % RFA chance. A pursuit walks to a **fixed** point. If that point is reached out of range, the body goes back to WaitToAttack.
3. **Contact jostle is decoded in Engine.dll (A/B).** A **moving** body yields 35 % of the overlap per update. A **standing** body yields only to the standing player. Bosses, Quest monsters and forceCollision bodies never yield. Movers stalled below 1.1 m/s for 0.4 s fail their path; that sends them into RFA or a random 3–5 m re-path. The oracle's step is different: a symmetric, fully converging solver that pushes standers too.
4. **Nothing else moves an attacking monster.** In Attack the body stands, and it fires at timer expiry **without re-testing range** (D8). The v3.9 port re-tests range during the swing pause and walks off early: 691 times in 20 salts against 5,249 at completion.
5. **Run in full on the v3.9 oracle (RJ-FULL), the decoded rules do not close the standing gap.** Standing at 2.46–4.92 m moves **0.575 → 0.570**; the referent shows 0.34.
   - RFA, WaitToAttack and slot churn replace *pursuit* time (P share 0.44 → 0.27, with R 0.15 and W 0.02). The *Attack* share in the band is unchanged (0.55 → 0.54).
   - Ratio **×2.304 → ×2.168** (paired −0.120, t95 [−0.220, −0.021]).
   - First deaths move from w152 ×15 to **w152 ×10, w160 ×7, 3 survive**.
   - w152 lengthens to 53 s and w155 shortens to 21.6 s.
   - Pre-registration: **13 HIT, 11 MISS.**
6. **What is left is not GD monster AI** (INFERRED). In the referent the player is moving 88 % of the fight at about 3.3 m/s (Lap H-2 cadence). That takes bodies out of reach constantly, and each re-entry into Pursue is movement. The oracle's pilot drifts at 0.919 m/s on about 52 % of ticks. The instrument also matters: on the referent's own net-speed rule (< 50 gpx/s), the control reads **0.479**, not 0.575.

---

## 1. The decode (DATAMINED; Game.dll RVAs, "E:" = Engine.dll)

The full rule table with addresses is `PREREGISTRATION.md` § 1 (D1–D8). It is not repeated here. Listings: `evidence/e01` (SlotManager), `e02` (RFA state), `e03` (WaitToAttack), `e04` (GetPointAwayFromGoal, RequestAttackSlot, GetTargetDistance, NeedsAttackSlot, GetExtents, slot construction and `numAttackSlots` load), `e05` (Pursue EndOfPathReached and PathFailed), `e06` (Attack LostSlot and projectile callbacks, RequestMove), `e07` (crowd parameters, Depenetrate, Error, ReachedGoal), `e08` (Engine.dll crowd update: separation steering, goal-occupied stop, depenetration, stuck rule, proximity mask), `e09` (vtables). Per-record data: `results/gd_tables.json`.

**The commission's four questions, answered:**

| question | answer | grade |
|---|---|---|
| RFA: when | Only at skill completion in Attack, with the same skill re-chosen and still CloseEnough. It rolls `randomRepositionChance` (per controller; 20 on ranged casters, 5 imps/wraiths, 100 loghorrean, else 0) and needs CanMove. Also: a projectile hitting a non-target pre-sets the roll with `RepositionChance`. It is **not** driven by crowding, line of sight or a timer; crowding reaches it only through slots (WaitToAttack, 50 % per 333 ms) and through crowd path failure (Pursue → RFA). | A |
| RFA: where | To the point on the body's own straight path to the target at distance r_target + r_self (contact): `GetMoveToPoint(target, skill = 0)` → `GetPointAwayFromGoal`. | A |
| RFA: how far, how often | The full approach to contact, at run speed. It ends on arrival, or at 2.5 s if in reach. If the path fails, the body walks to a random point 3–5 m from itself. Frequency on this board: ~8 attack-RFAs per salt, ~108 RFAs per salt in total once slots are on (`results/results_table.json`). | A (B for the 3–5 m) |
| melee vs caster | No branch on class. Melee-profile skills take slots (and so WaitToAttack); the roll field is set mainly on casters' controllers. A caster that RFAs closes to contact and keeps casting from there. | A |
| move-to point / slot geometry | 6 slots (`numAttackSlots`), one ring (SlotMode 0), radius 1.25 + r_m + r_p, angles 2πj/6. Nearest free slot, else override by (d² − e²)⁺ with e = 0.5/1.0/1.75 by pathingSize. Non-melee skills go to the point r_t + ladder on the line. The point is fixed at Pursue entry. | A |
| jostle | See Summary 3 and D6/D7. Groups: hostiles (2, mask 7) collide with all; the player and friendlies (1, mask 2) collide only with hostiles. | A (E:), B ("moving" = crowd state 2) |
| anything else | D8 (no range re-test inside Attack). LostSlot → Pursue. Path end out of range → WaitToAttack. `RequestMove` is a leader command. Knockback, stun and knockdown are temporary states: **not decoded here**. | A |

**Against the oracle's separation step** (`run.py:1963–2035`, `geometry.separate_overlaps_converging`, the KP-136 (12) contact fold):

| | oracle (R-PM4-12/18) | GD (Engine.dll) |
|---|---|---|
| who moves | both bodies of a pair, half each; the player fixed | only the eligible body by the priority rule; standers yield only to the standing player |
| how much | full projection, iterated to convergence each tick | 0.35 × penetration per update, averaged, single pass |
| standers | pushed apart by every overlap | never pushed by monsters; may overlap each other |
| immovables | none | Boss/Quest/SuperBoss/forceCollision |
| blocked movers | slide along the solver indefinitely | stopped after 0.4 s below 1.1 m/s → PathFailed → RFA / re-path |
| player | fixed | a moving player is displaced (body-blocking) |

Measured on the control: the oracle displaces a standing body 37,714 times but pushes one out of reach only 30 times (m4). The symmetric push is therefore not what keeps bodies moving.

---

## 2. The counterfactual (SIM; v3.9 oracle, V39-FULL, seed-9 line-up, salts 0–19; ⚑ NOT-A-GRADED-RUN)

| arm | ratio | paired Δ (t95) | first deaths | w152 s | w155 s | standing 2.46–4.92 (step) | standing (net, < 0.41 m/s) | inside 2.46 (step) | closing (empty) | disc 151–159 |
|---|---|---|---|---|---|---|---|---|---|---|
| CTRL (= V39-FULL) | ×2.304 | 0 | 152×15, 156×2, 154, 160×2 | 33.9 | 28.5 | 0.575 | 0.479 | 0.993 | 0.795 | 1.661 |
| RJ-RFA | ×2.381 | +0.084 [+0.021, +0.147] | 152×15, 160×4, 154 | 33.9 | 22.8 | 0.573 | 0.472 | 0.985 | 0.714 | 1.692 |
| RJ-SLOT | ×1.994 | −0.302 [−0.370, −0.234] | 152×12, 160×2, 6 survive | 38.9 | 28.0 | 0.547 | 0.461 | 0.947 | 1.022 | 1.711 |
| RJ-CROWD | ×2.171 | −0.128 [−0.216, −0.039] | 152×13, 160×3, 4 survive | 41.2 | 30.5 | 0.622 | 0.660 | 0.994 | 1.574 | 2.240 |
| RJ-PERSIST | ×2.281 | −0.021 [−0.084, +0.042] | 152×15, 156×2, 160, 2 survive | 35.4 | 30.5 | 0.586 | 0.488 | 0.993 | 0.936 | 1.624 |
| RJ-CORE | ×2.127 | −0.166 [−0.253, −0.079] | 152×11, 160×3, 156, 5 survive | 46.6 | 22.7 | 0.556 | 0.581 | 0.937 | 1.089 | 1.740 |
| **RJ-FULL** | **×2.168** | **−0.120 [−0.220, −0.021]** | **152×10, 160×7, 3 survive** | **53.3** | **21.6** | **0.570** | **0.595** | **0.938** | **0.976** | **1.699** |
| referent (FOOTAGE) | ×1.0 | | none | 16.3 | 16.2 | 0.34 | (the referent instrument) | 0.20–0.28 | 0.92 | 1.66 |

The RJ-FULL and RJ-SLOT/CORE results replicate byte for byte on a second run.

**What happened (SIM):**
- **Standing does not fall** because the decoded movement replaces *approach* time, not *attack* time. Band shares in RJ-FULL: Attack 0.54 (control 0.55), Pursue 0.27 (0.44), RFA 0.15, WaitToAttack 0.02. Most RFAs end by the 2.5 s timer once in reach, so the body stands at about the same radius as a Pursue arrival.
- **SLOT** cuts the ratio by 13 %. At wave start the 6 slots go to the first requesters, and the overflow spends its approach in WaitToAttack/RFA, unable to attack (~250 failed requests and ~150 robberies per salt). w151–153 own-wave ratios fall about 20 %; w160 rises (bosses are immovable, ranged and slot-free).
- **CROWD** (GD's priority rule in place of the symmetric solver, without the path-failure rule) makes standers immovable to monsters. Movers jam against them: net-still rises to 0.66, disc occupancy to 2.24, w154 stalls at 91.7 s. With D7 in the same run (RJ-FULL), path failure breaks part of the jam (w154 39.6 s).
- **RFA alone** raises the ratio 3.4 %. Casters close to contact and keep firing; w155 shortens to 22.8 s.
- **PERSIST** is neutral (5.7 melee whiffs per salt).

## 3. Prediction scorecard (pre-registration `b816e68e4`)

| # | prediction | result | grade |
|---|---|---|---|
| Q1 | RJ-FULL standing (step) 0.38–0.52 | 0.570 | MISS (it barely moved) |
| Q1b | RJ-CORE standing 0.36–0.50 | 0.556 | MISS |
| Q2 | RJ-FULL standing (net) 0.50–0.70 | 0.595 | HIT on the interval, **but its basis was wrong**: the control figure in the pre-registration (0.761) came from a defective instrument (corrected value 0.479). Net-still went **up**, not down |
| Q3 | w152 22–34 s | 53.3 s | MISS (longer: slot overflow and jams) |
| Q4 | w155 18–30 s | 21.6 s | HIT |
| Q5 | w152 4–12, w160 4–12, ≥ 1 first death elsewhere | 10 / 7 / 0 (3 survive) | MISS (2 of 3 parts) |
| Q6 | ratio ×1.50–2.25 (FULL; CORE) | ×2.168; ×2.127 | HIT; HIT |
| Q7 | closing 0.70–1.10 | 0.976 | HIT |
| Q8 | disc 1.8–2.8 | 1.699 | MISS |
| Q9 | inside 2.46 m 0.80–0.97 | 0.938 | HIT |
| Q10 | RFA Δstand −0.04…−0.005 / Δratio −6…0 % | −0.002 / +3.4 % | MISS / MISS |
| | SLOT −0.18…−0.05 / −30…−3 % | −0.028 / −13.5 % | MISS / HIT |
| | CROWD ±0.02 / ±4 % | +0.047 / −5.8 % | MISS / MISS |
| | PERSIST 0…+0.03 / ±4 % | +0.011 / −1.0 % | HIT / HIT |
| Q11 | FULL standing above 0.34 by +0.04…+0.18; w152 and w155 longer than the referent | +0.23; yes | MISS; HIT |
| Q12 | attack-RFAs 6–20; WaitToAttack 100–300; LostSlot 60–250 per salt | 7.95; 185.8; 151.5 | HIT ×3 |

**13 HIT, 11 MISS.**
- **The common cause of the standing misses:** I assumed RFA arrivals would stand at contact, outside the band. In fact the 2.5 s timer releases them into Attack wherever they are in reach. And the decoded movement takes time from Pursue, not from Attack.
- **The CROWD misses:** I took "standers rarely pushed out of reach" (m4) to mean the jostle rule was inert. Its real effect falls on movers, which now jam.

## 4. Post-registration fixes (disclosed; `results/postreg_fixes.diff`)

1. **The net-speed instrument differenced post-step positions, so it measured only the solver's displacement.** It now differences pre-step positions. No simulated value changed; the ratio, deaths and step-standing are identical before and after.
   - The control's net-still is 0.479, not the 0.761 stated in the pre-registration's disclosure.
   - `results/control_premeasure.json` keeps the old instrument field (m1–m4 are unaffected).
2. **The per-wave RNG caches were keyed by `id(engine)`**, which CPython can reuse across waves. That made RJ-SLOT/CORE differ run to run. The caches are now cleared per wave, and replicas are identical.

No rule, constant or arm changed after the pre-registration.

## 5. What should go into the oracle / what stays open

**Decoded, and candidates for a fold** (the conductor's ruling; each changes the oracle):
- **D8: Attack persistence.** Stand through the swing pause; no range re-test until completion. The port's early re-test is a deviation from GD. Its fire-time resolution for an out-of-reach melee swing is **not decoded** (my whiff limb is INFERRED).
- **D3–D5 + D7: slots, WaitToAttack, fixed move-to point, path failure.** Price −13 % alone, −6 % in RJ-FULL. It needs pets to take slots as in GD, which the port excludes (they would *increase* WaitToAttack).
- **D1–D2: RFA.** +3 % alone. Port-ready: one field per controller (`results/gd_tables.json`).
- **D6: the crowd priority rule.** Fold it only together with D7. Without the path-failure rule it creates jams (w154 91.7 s) that GD resolves.
- **Reference implementation:** `tools/rj_arms.py` (every constant cites its address).

**Open:**
- **The standing gap (0.57 vs 0.34) is not explained by GD's monster AI.** Two leads remain (INFERRED):
  1. the pilot's movement (88 % vs about 52 % of time, 3.3 vs 0.92 m/s): gamora's seam and Matt's play;
  2. the instrument: the referent's 50 gpx/s threshold on plate tracks versus the oracle's step travel. On the referent's rule the control already reads 0.479.
- **Crowd update rate.** GD's 0.35 relaxation is per crowd update, and the update rate is not decoded; I applied it once per oracle tick (82 ms).
- **Pets in the slot system; RepositionChance** (projectile collision with non-targets); **body-blocking of a moving player; the movers' separation steering (weight 1.1)** — none modelled.
- **Knockback, stun and knockdown recovery** (temporary states) — not decoded.
- **The referent's own line-up** (Q101, footage). Seed 9 remains a declared extreme draw.

## Files

| file | contents |
|---|---|
| `PREREGISTRATION.md` | predictions, rules and arms; committed alone at `b816e68e4` |
| `results/results_table.json` | every arm's metrics, paired Δ, the grading |
| `results/arm_*.json` | per-arm summaries (oracle summarise + RJ instruments + telemetry) |
| `results/gd_tables.json` | DATAMINED per-record: randomRepositionChance, RepositionChance, extents, classification, forceCollision; skill distanceProfile; player numAttackSlots |
| `results/control_premeasure.json` | PRE-RUN control measurements m1–m4 (its net field is the defective v1 instrument) |
| `results/postreg_fixes.diff` | the two disclosed fixes |
| `evidence/e01–e09` | targeted Game.dll/Engine.dll listings |
| `tools/` | `rj_tables.py` · `rj_arms.py` (arms + instruments) · `rj_control_measure.py` · `rj_pack.py` (grading) · `rj_trace_diag.py` (the pre-registration mechanism trace) |

*legolas · KC2-PLAY · KP-216 reposition/jostle decode · 2026-10-02*
