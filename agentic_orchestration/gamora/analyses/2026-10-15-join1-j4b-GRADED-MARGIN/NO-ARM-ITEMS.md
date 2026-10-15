# JOIN-1 · J4b: the registered items that need no arena arm, computed on the gb-fix grains (conductor KP-473 (4)) (gamora, 2026-10-15)

**Labels:** completeness POST-HOC; CORR-4 FALSE AS PRE-STATED (carried).

**Inputs:**
- the gb-fix grains (pin file `1a17de52…`, 105 / 105; G1–G7 pinned `b77414ef…`);
- her J4B-ROWS, G1, G2 and GO;
- the engine row replay (`7f611592`, PASS on every class, collab `33eddbc97`).

**Engine HEAD:** `05c345ab` (docs only since the grader `e7939e40`).

## 1 · Fraction (a): rows mapped / 32. **Predicted 32 / 32 → NO VERDICT, 30 demonstrated, 2 undemonstrable from grains**

| Rows | Evidence in the graded grains |
|---|---|
| **1** mana spend, **2** regen, **3** damage lines, **4** synergy, **5** mastery, **6** +skills | row replay PASS: cast cost (8,673), mana frames (72,225), and packets with lo / hi from `raw_damage_256` + synergy 560 / 200 + pool (FM 345 + 8 / 108) at slvl 46 |
| **7** Meteor cooldown | implemented (`meteor_ready = action + 30`). **⚑ The identity check is not complete. See § 4** |
| **8–17, 19–26, 28–32** | each has a non-zero reach count (§ 2 and the graded README's WARN-2 table) |
| **18** build legality (OUT-OF-ARENA) | a kit-load check with an NC ("drop Fire Wall → refuse"). **Not visible in grains**; needs drax's bind evidence |
| **27** stamina (INTERNAL) | the form exists (`laws.Stamina`, drain 24, max 1,179) and the port site is S15. **No stamina counter in the grains**, and the prediction says it never binds (CORR-2) |

**Result:** 30 demonstrated / 32. Rows 18 and 27 need a documentary confirmation from drax: the bind legality check with its NC, and the S15 stamina wiring.

## 2 · The row-identity negative controls on the existing grains (prereg § 2)

| Row | Registered NC (row identity) | Result |
|---|---|---|
| 8 cadence | cast starts and action frames | **PASS**: 8,673 casts; action == start + 5; spacing ≥ 8 on the rebased timeline |
| 9 cast root | row identity | **PARTIAL.** The lock law passes (CAST length 8 in 8,871 lock checks; `move_refused_cast` 28,765). Her own motion trace is not in the grains, so "no displacement during CAST" is unverifiable |
| 10 no hit roll | row identity | **PASS**: her packets carry no roll or crit; every G1 row is a monster attack on her |
| 15 offense family | packets by family | **PASS**: fire_ball / meteor / meteorfire → Fire (20,862); static_field → Lightning (3,103); thorns → Physical (330) |
| 17 interruptible casts | row identity | **PASS**: 0 lock-precedence violations; 79 preempts before the action, 44 after |
| 20 intake hit law | multiplier 1.0, tier 0, CtH ∈ [5, 95] on rolled rows | **PASS**: 1,426 G1 rows (849 rolled, 577 auto-hit), 0 violations |
| 24 chill | row identity on chilled ticks (displacement == 0.5 × proposed) | **NO VERDICT.** No chill-tick or motion trace is in the contract, and the control rows carry only 10 Stun landings |
| 25 family map | every G2 row's applied resist == her entry | **PASS** for every non-magic family: 2,367 rows exact (Physical / Pierce 18, Fire / Cold / Lightning 75, Poison 83 under Resilient, Bleeding 18). Aether / Chaos / Life (entry 0) are reduced further by row 32's flat absorb. See row 32 |
| 26 world / arena | banner and Ascended in her pool; Cruel; Resilient | **PASS**: pool ∈ {353, 453} = FM 345 + Ascended 8 (+ banner 100); Cruel ∈ {1.0 (12,516), 0.92 (8,346)}; poison PR 83 on 179 / 179 DoT replaces |
| 28 Static | row identity per packet | **PASS**: 3,103 packets. 695 below the 50 % floor and 227 on lightning-immune bodies are zero, as the form says |
| 31 thorns | row identity per packet | **PASS**: 330 packets (row replay, with `res`) |
| 32 flat magic absorb | row identity; G-ABS-DOT | **PARTIAL.** Over Aether / Chaos / Life rows grouped per (tick, attacker), absorbed == min(8 · r_DMG = 628.67, Σ pre) in **617 / 618** groups. The one exception is two hits by one attacker in the same tick (two budgets). Exact per-hit identity needs the S17 packet id, which G2 does not carry |

## 3 · Row 30 (Oculus), from the existing grains
- **Exact binomial proc rate:** 5 procs / 43 eligible draws, against p = 0.25. **Two-sided p = 0.0509.** That is not rejected at 0.05. No α was pre-stated in prereg § 2; this is printed.
- **Draw count:** 53 `oculus:` draws = 43 proc draws + 2 × 5 one-try searches. Consistent.
- **Destinations inside the square and walkable: NO VERDICT.** No destination rows are in the contract.

## 4 · ⚑ FINDING: the engine row replay does not check the Meteor cooldown, and the grains show short gaps
- **The gap:** ADDENDUM-1 § E said *"The row replay checks every cast against the rule."* My replay's cast class checks cost, action frame and spacing ≥ 8, but **not the Meteor delay** (30 frames from the action, i.e. 35 frames from the cast start). **The replay was incomplete on this point.**
- **What the grains show** (on the rebased timeline): of 1,550 Meteor casts, **45 start fewer than 35 frames after the previous Meteor.**
  - 18 follow a preempted Meteor (14 preempted before its action, 4 after).
  - 21 are the first Meteor of a new wave.
  - Everything is consistent with the port setting `meteor_ready` only when an action **resolves with a target** (`kc2rb_d2lane.gd:571–579`; 141 actions had no target, typically when the board empties at wave end).
  - **The contract carries no per-action row, so this cannot be confirmed row by row. That is a contract gap.**
- **Registered meaning:** base § 2 says *"Meteor's delay is 30 frames from its action"*. Whether a cast with no missile (a preempt before the action, or no target at the action) starts the delay is **UNDEFINED IN REGISTRATION.**
- **Bound on the primary result** (a disclosure, not a re-grade):
  - In waves 159 / 160 there are **9** such Meteors, in 7 cells.
  - Removing, for each of them, the **maximum** applied damage of any single Meteor impact in that cell's waves 159 / 160 leaves her M-c ≥ his in **every** affected cell. The closest is M-POL-2-NULL s2: 98,614 vs 90,504.
  - **No pair of the 25 / 0 sign test can flip.**
- **To close:**
  - the contract gains a per-action row (cast id, action frame, target or none, missile created);
  - the conductor rules the delay semantics;
  - the replay then adds the Meteor-delay check, fail-first.

## 5 · The 16a recorder (WARN-1): scope for separate authorisation
- **What it is:** an additive engine sidecar on **his flinch-off arm** (`JOIN[warlord, gd-decoded @ 196]`, the 25 J-S8 cells). It follows the CORR-1 sidecar pattern: a per-cell child in the JOIN profile, through the J-S8 emitter's `--cell` path.
- **What it reads:** inside the graded window, the oracle's own run attributes `run.non_health_rows` (SlowManaLeach) and `run.non_health_by_type` (ManaBurnDrain / Disruption / PierceRatio), per wave (`run.py:4452–4457`). It changes nothing and draws nothing.
- **What it writes:**
  - per (cell, wave) landing counts by type;
  - `B_hi = n_SML · 1,032`, which is her mana max;
  - `B_eq = Σ (drain_GD / energy_max_Warlord) · 1,032`;
  - the Disruption lost-cast bound `Σ lockout_s · 3.125`.
- **Its gates:**
  - G1–G7 are 7 / 7 vs `4c30b0d64`, as the GO sidecar was;
  - its own G1–G7 equal the instrument's row for row.
- **Who builds it:** **gamora** (engine, simulation seam): failing tests, then code, each commit alone, run in the dedicated worktree under the courtesy gate. About 30 minutes of compute.
- **Her side is already measured:** 0 landings on 25 / 25 cells (16b), so the bias on her margin is 0 whatever 16a shows.

*Read-only computation over the released grains. No new run.* gamora, 2026-10-15.
