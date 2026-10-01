# Finding — 2026-10-01 — JOIN-1 J-P2 ADDENDUM-2 re-check (pre-freeze of J-S8)

**Reviewer:** jack-ryan
**Severity:** **WARN** — gamora MAY freeze `join1-gm-fixture-v1` citing this commit, with the named items carried (§ 4). 0 BLOCK · 5 WARN · 9 INFO.
**Target:** engine `ee907e42` (ADDENDUM-2 ALONE, FILE `b482f58086459178138f4055cd59e26125f87e5cefd570b34ad4cc0e4ad57fe4`) · engine `05388b25` (emitter, FILE `5fb71adc85f13a63bfb6cd1710846a6331a568b9f4c9e7d9046cce3bf136eb38`) · tag `kc2/referent-v1-oracle-candidate` → `22cd2288`, kc2 tree OID `d974998f…` (all re-derived this session)
**Developer:** gamora (oracle side) · conductor rulings: gandalf, KC2 ledger KP-191
**Principles applied:** REVIEW_PROCESS #1 (math before code), #2 (smoke gate), #3 (cross-seam impact), #4 (decisions-log/committed truth), #5 (severity). Disciplines #11, #12, #24, #73, #80, #86.

## What I found

All twelve RULED readings match the oracle's code. Where a reading cites a conductor ruling (R-SCOPE, R-G1-PTH, R-G1-POP, R-G4, NC-1′, § 6.4 split), it implements that ruling. The dropped fields are justified. **I reproduced the baseline and all four controls myself**: a full 25-cell dry run of each, in a scratch worktree of the tag that I have since removed. Every result matched KP-192:

| run | my result | gamora's claim |
|---|---|---|
| baseline | 25/25 ran, `sim_errors` 0, 0 foreign reads, 14 pinned external inputs; terminals M-POL-2 `[156,152,155,152,152]`, W1 `[156,152,155,152,155]` (= v1.12 § B.1a); G4 beyond = 0 everywhere | same |
| **G2 stage fidelity (my own check)** | **3,939/3,939** folded physical rows: `fsum(w_r/100 · after_stage_2[r]) == applied` **bit-exact**. Regions are in `REGIONS` order and every region input equals `pre_mitigation`. 2,227 rows have an `overflow` region | 3,939 / 2,227 |
| NC-1′ | RED in exactly the predicted 15 cells; GREEN in the predicted 10 (same ids). The baseline law gives 61 exposed attempts; every first divergence is tier 2→1, ×1.1→×1.0, roll 90 | same |
| NC-2 | 25/25 RED; `after_stage_1` moved on 3,939/3,939; non-physical: 29 SlowBleeding rows (25 at 82→80, 4 at 80→82). **In every cell the first non-physical divergence comes strictly AFTER the first physical one**, which supports the Resilience-window state-coupling explanation | same (the ordering check is mine) |
| NC-3′ | `d_engage_m` 2.5 received at every step; G4 RED 25/25; G5 moved in 22/25; halted body-ticks 8,328→11,144; `min_body_distance_m` at 2.400 m: 103→6, at 2.500 m: 6→134; beyond stays 0 | same |
| NC-4 | 25/25 `raised:KeyError` — **but see WARN-2: the raise fires in the `_period()` probe, so 0 waves played and 0 grain rows** | 25/25 |

My baseline ROWSET digests are in § 5. The emission is deterministic, so the frozen fixture should reproduce them; that check is independent of gamora's session.

**Q3 (alert-held bodies left out of `n_bodies_halted`): CONSISTENT with the port.** The oracle sets `mech_ring_halt_step` *before* it applies the alert hold (`locomotion.py:1133` vs `:1182-1189`). An alert-held body inside `d_engage` would therefore carry the flag. The port's pursuit loop runs `continue` on an alert-held body *before* its `d <= stop_at` ring test (`kc2rt_fight.gd`, the `alert_hold_until` block, before `var stop_at`), so the port never counts one. Leaving them out on the oracle side is the only reading the port can reproduce. The arming tick and the expiry tick also line up: on both sides the hold arms after the step and lapses when `t ≥ hold`. The LATENCY-ALERT exclusion (`mech_hold_active_step`) is inert on the record path and has no port twin, so it is consistent too.

## Per-reading verdicts

| # | reading | verdict | note |
|---|---|---|---|
| 1 | R-SCOPE | **PASS** | Leg A; `waves_played ≠ waves_emitted` in 25/25, as designed. INFO-1, INFO-2 |
| 2 | R-TICK | **PASS** | run tick; G2 is keyed to the cast tick (all three `mitigate` sites are inside `resolve_attack`, `threat.py:2018/2026/2098`) |
| 3 | R-G1-PTH | **PASS, WARN-1** | `pth_raw`/`pth_used`/`pth_effective` as ruled; `pth_effective == max(pth_used, 55)` and `hit == (roll ≤ pth_effective)` hold on 8,380/8,380. The floor and the sub-threshold branch are **unexercised** |
| 4 | R-G1-POP | **PASS** | 4,352 monster + 4,028 summon; the summon path calls `th.probability_to_hit`/`th.resolve_hit` through the module, so the hooks see it (`summon_offense.py:879-880`); `pth_raw` is non-null on 8,380/8,380 |
| 5 | R-G2-GRAIN | **PASS** | `dropped`/`voided` really are application-grain fates (`deferred_arrival.py:399-430`, with their own run-grain counters and TA-X-07's residual); `global_flat` selects `armour_table(global_flat)`, so it is an operand table, not a stage. INFO-3 |
| 6 | R-G2-STAGES | **PASS** | verified bit-exact (above). The third `physical_applied` call is the primary one (`aggregate_applied` calls `armour_branch` directly and is not counted). INFO-4 |
| 7 | R-G3 | **PASS** | `n_caps_applied` is declared and emitted but never incremented: there is no `+=` anywhere in `kc2/` (grep). No target-cap path exists. `leech_per_body` is the quotient of the two kept fields |
| 8 | R-G4 | **PASS** | Q3 above. INFO-5, INFO-6 |
| 9 | R-G5 | **PASS, WARN-2** | the vocabulary and the `raised:` precedence are right; the remedy for the swallow has never been exercised |
| 10 | R-G6 | **PASS** | no monster-status code path; named-and-empty is correct |
| 11 | R-G7 | **PASS** | `tick_period_s` in place of `tick_rate_hz` is a named semantic shift (#12) and removes a guaranteed false red |
| 12 | R-ROWSET-SEP | **PASS** | the law is stated verbatim and implemented as stated |

## Rationale — the WARNs

**WARN-1 · Hit resolution's floor and its sub-threshold branch are NOT observable in J-S8 (#86, #80).** `min pth_used = 71.419` over 8,380 attempts. 148 attempts have `pth_raw < 70`, and the measured board substitutes for every one of them. So no attempt reaches `PTH_MINIMUM = 55` or the `p < 70 → p/70` branch. **Changing the floor to any value ≤ 71.42, or removing it, leaves the fixture byte-identical; so does any change to `NORMAL_PTH_DIVISOR`.** That matters to JOIN-1 for a specific reason: D2's floor (5 %) is lower than GD's 55. **A J2/J3 leak of D2's floor into `ORACLE` would therefore pass the golden master green.** § B2's line *"the floor is now visible where J-P2 § 3.2 wanted it"* overclaims. The field is present, but the population cannot reach it. This is the same species as `G6`, and it gets the same treatment.

**WARN-2 · The remedy for the `replay()` swallow has no control.** NC-4 removes `'Fire'`, so the `KeyError` fires inside `PR._period()`. That probe runs outside the recorded composition: `sim_errors[0] = (threat.mitigate, rec=False)`, then `(run.simulate_wave, rec=False, wave 151)`; `harness_error = IndexError`; 0 waves played; 0 rows in G1–G4/G7, in 25/25 cells. NC-4 does prove that GL-12's refusal is preserved. It does **not** prove the KP-191 remedy: that an exception raised in a recorded wave after 151, which `replay()` turns into `arena_tier_exhausted`, ends up as `raised:<T>` in G5. By code reading, `_sw_raw` records it and the `SIM_ERRORS` precedence classifies it correctly. That path has never run. This does not block the freeze: the baseline has `sim_errors` = 0 on 25/25 and its terminals match § B.1a, so the frozen fixture is not affected by the swallow.

**WARN-3 · Limb C's one closed exception names a field that J-S8 does not emit.** J-P2 § 4 grants its single tolerance (`1e-12`, with depth emitted) to *"G2's global-magnitude composition chain (`om`)"*. ADDENDUM-2 § B9 says Limb C *"stands"*. Neither the G2 schema nor the emitter has an `om` field (nor a depth field). `om` reaches the fixture only *inside* `pre_mitigation` (`threat.py:2018/2026/2098`: `magnitude · a_mult · om · …`), which falls under **Limb B, bit-equality**. In effect, then, the exception list is **empty** for fixture v1. A legitimate J2 reassociation of the `om` sum would show as a Limb-B RED. That is the safe direction, but it would be a HALT. **This must be stated at freeze, because after a diff exists, granting `pre_mitigation` a tolerance would be exactly the post-hoc rescue J-P2 § 4 forbids (the `WARN-16` shape).** The ROWSET digest is exact equality on every float, so any Limb-C tolerance would also need a row-level comparator that does not exist yet.

**WARN-4 · The port side of § 4.5 "runs" and of NC-4 is undefined, and GDScript has no exception to observe.** The port's `res_used()` reads `float(player_resist[dtype])` (`kc2rt_fight.gd:5683`). On a missing key that is a Godot script error, not a raised exception. Whether a headless cell then aborts, continues on a default, or reaches a terminal state is **unverified**. Joined kits run on the port, so the charter's *"a `KeyError` in a joined kit is a 'runs' FAIL"* has no port mechanism yet. § 6.3's unredacted stderr stream catches a new error line *for invariance*. It does not define "runs".

**WARN-5 · U-5 (the unported patrol leg) has no instrument in JOIN-1.** (Q5.) Neither J-S8 nor the invariance check *can* see it. Both run the referent arena only, and there the 43.758 m wall keeps every body inside the 80 m view distance. Both are therefore correct as they stand, and **no fixture schema change is owed**. The hazard lives in the JOIN profile: a JOIN arena or board whose geometry puts a body beyond 80 m from the player switches on a mechanism the port never ported (the port `continue`s a gate-closed body, which the oracle sends on patrol). The charter text never mentions U-5. Both sides already have the observable: the port's `n_gate_closed_body_ticks`, and the oracle ring ledger's per-mover `n_patrol_legs`.

## Rationale — INFO (no action required for the freeze)

- **INFO-1** The manifest's `scope.window` still reads `[151, 160]` under R-SCOPE. `waves_emitted` per cell is correct. The label is stale (#73).
- **INFO-2** An exception in a Leg-B continuation wave, past the Leg-A terminal, would still set `raised:`. That is conservative (out of scope but flagged), and it never fires in the baseline. Worth one line in the manifest.
- **INFO-3** G2 `applied` is the **cast-tick mitigation output**, not the damage that landed: deferred arrival can drop it, void it, or re-clamp its PCL part at arrival. No grain records landed intake per tick. Changes in arrival timing (the tick clock, `ceil` quantisation) show only through G3/G5 integrals and state couplings. A per-tick `player_hp` or landed-intake field would make them attributable. It is optional; adding it before the freeze is cheap, and after the freeze it is a re-freeze.
- **INFO-4** The primary call is identified as `n_pa == 3` and region labels come from `REGIONS[i]`. Both are correct under `RegionLimb.EXPECTATION` (verified by the bit-exact identity). Under `ROLLED` the labels would be wrong. An in-emitter assertion of the fsum identity would make this self-checking.
- **INFO-5** No control drives `n_bodies_halted_beyond_d_engage` off zero on either side since NC-3 was corrected (#80). On the oracle side a miswired hook produces a false RED, not a false GREEN, so the freeze is not at risk. **drax:** the port's existing `n_bodies_halted_beyond_d_engage` is a per-body **latch** (`_halted_beyond`), but the fixture field is **per tick**. The port emitter must emit per tick, and its control set should show the counter firing (e.g. a reduced `r_wall`).
- **INFO-6** `min_body_distance_m` is computed over ring-ledger **movers** (state 1), with pets excluded. `n_bodies_in_disc` includes pets. The port emitter must use the same two populations.
- **INFO-7** The control outputs are uncommitted scratch. "Predictions before runs" is evidenced only by commit order: `ee907e42` (17:54:09) precedes `05388b25` (17:56:03), the first commit that contains the NC-1′/NC-3′ mechanisms. **NC-2's corrected expected-negative half was written after a first NC-2 run.** That is disclosed (KP-191, § B7) and acceptable: the core claim (physical stages move) was predicted at J-P2 time and held, and my ordering check gives the correction a falsifiable footing. **NC-3's partial sub-claim is acceptable**: the band shift plus `n_bodies_halted` plus G5 in 22/25 shows the fixture sees movement↔engagement.
- **INFO-8** The freeze gate accepts any non-empty `JOIN1_ADDENDUM2_RECHECK`. The value is recorded on the manifest, so the J0-F Gate-2 checks it against this commit.
- **INFO-9** The oracle-side invariance check, `git diff … -- simulation/kc2/`, is empty today (verified: 0 files). Its scope is narrower than the oracle's import closure: the four composition modules in `simulation/scripts/`, `data/kc2/`, and the packs under `src/reincarnated/output/`. The binding guarantee is limbs 2+3: the emitter refuses any tree whose HEAD is not the seal commit. The diff is hygiene, and widening it to the closure is cheap. **Disk:** my 3.5 GB scratch worktree took free space to 21 GiB, against a 20 GiB HALT line. It is removed, and free space is back to 24 GiB. The next scratch worktree, of any kind, should check `df -h` first.

## Action

- [ ] **gamora + conductor (AT the freeze, in the freeze record: ledger row + the manifest via the conductor's fold; no emitter change needed):** (a) **WARN-1**: declare `G1 floor limb (PTH_MINIMUM) and sub-threshold branch: UNEXERCISED-IN-REFERENT-V1 — min pth_used 71.419 over 8,380; a floor change ≤ 71.42 or a NORMAL_PTH_DIVISOR change is invisible to J-S8`, beside G6. (b) **WARN-3**: declare `Limb C exception list for join1-gm-fixture-v1: EMPTY (om is not emitted; pre_mitigation carries it under Limb B)`. If gamora would rather put both in the emitter's `unexercised` block, I approve it under ADR-002 provided the diff touches only that dict and the new emitter FILE digest is printed in the freeze row.
- [ ] **gamora (before the J0-F Gate-2 quotes G5's `raised:` class):** **WARN-2**: an NC-4b, a refusal first raised inside a recorded wave after 151. Example: a scratch `RESIST_PCT` copy that drops a family absent from wave 151's baseline packets, or a raise armed on `CTX["wave"] > 151`. Predict it in writing first: G5 `raised:KeyError`, G1–G4 rows present up to the raising wave, `waves_played` stopping there.
- [ ] **drax (port emitter Gate-2):** **WARN-4**: a port NC-4 showing what the port does on an unmapped family, and a port-side operational definition of "runs" (e.g. an explicit refusal counter plus zero `SCRIPT ERROR`/`ERROR:` lines on stderr). Plus INFO-5 (per-tick beyond counter, and a control that fires it), INFO-6 (populations), and § 6.4's own invariance negative control on the port (`intake_order` gives an NC-2 twin).
- [ ] **conductor (charter fold):** **WARN-5**: carry U-5 into § 4.5 / J4: before any JOIN arena or board differs from the referent geometry, every JOIN run emits `n_gate_closed_body_ticks`. A non-zero value is a named finding ("unported mechanism live"), or the patrol leg gets ported first. U-5 also goes on the fidelity-cost table. WARN-1's floor blindness goes on J3's `pth_floor_pct` lever: its negative control must run where `pth < 55` occurs, or it is vacuous for the same reason.
- [ ] **Matt:** nothing. No ORACLE behaviour change, no BLOCK, no cross-seam schema change.

## References

- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/math/kc2-join1-golden-master-instrument-2026-09-29.md` (J-P2, FILE `54b62b56…`) · `…-ADDENDUM-1.md` (FILE `480026f6…`) · `…-ADDENDUM-2.md` (FILE `b482f580…`)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/scripts/gamora_join1_gm_emit_2026_09_29.py` (FILE `5fb71adc…`)
- Sealed oracle at `22cd2288`: `kc2/threat.py` (`mitigate` :267-336, `resolve_hit` :390-406, `mitigate` call sites :2018/2026/2098) · `kc2/intake.py` (`armour_branch` :373, `physical_applied` :385, `order_fork_delta` :419, `aggregate_applied` :455, `physical()` :553) · `kc2/locomotion.py` (`step` :1100-1200) · `kc2/run.py` (step→`clamp_body` :2235-2251; ring ledger :2648-2667) · `kc2/player_sustain.py` (:615, :719) · `kc2/deferred_arrival.py` · `kc2/summon_offense.py` :850-900 · `scripts/gamora_kc2_pm4_i26_spawn_structure_fold_2026_08_16.py` :551 · `scripts/gamora_kc2_play_c11a_fold_pricing_2026_09_30.py` `_period` :192
- `/Users/admin/Games/reincarnated-godot/kc2_runtime/sim/kc2rt_fight.gd` (pursuit / alert / wall-clamp block ≈ :2660-2712; `res_used` :5679; `_mitigate` :5749)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-09-29-join-1-run-charter.md` (§ 1 J-S6/J-S8, § 4.3, § 4.5, § 4.7, § 5 J0-F) · KC2 ledger KP-189…KP-192 in `2026-09-20-kc2-play-run-charter.md`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/qa/findings/2026-10-01-kc2-play-h5-hole-closure-d03ca891.md` (U-5)

## § 5 — Independent baseline digests (my dry run, emitter `5fb71adc…`, scratch worktree of `22cd2288`; substrate v3.7.1 / model `48a4c94c…` / reference `1887257f…`)

| grain | rows | ROWSET sha256 |
|---|---|---|
| G1 | 8,380 | `0219a0a51db97ba437c9e0126c6395bd0b9af1bcafc520f9f350cb153196d3ea` |
| G2 | 15,153 | `80e0051afd4a0dc035b91645211add61b169374b092b0635e52dd93d3ea31412` |
| G3 | 98 | `1ef3c85a52c7eb509dd21d4b24126a0902069e89d6cb2abf4d8a5923a9298ed0` |
| G4 | 17,668 | `6014e0bb1162e9e8fef57564da276203dae3cf5fa4cbf4067b1af368d112ed24` |
| G5 | 25 | `9c5ce13e9087c5959a7b0bd790d133b084f0259bbe6204ef943dab6290fb3efa` |
| G6 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty) |
| G7 | 98 | `9f3e213546fc51be397a0d653fdccd5e75bd83c22c86d4d3f3d191f2037640f5` |

**The freeze should reproduce these ROWSET digests exactly.** A mismatch at freeze is a finding, not something to re-run away.

*Read-only review. No code changed. The scratch worktree was created from the tag, used for dry runs only, and removed. No push.*
