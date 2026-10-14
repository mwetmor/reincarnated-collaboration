# C-13 / KP-428 (2): GD per-hit damage under the oracle's configuration of record

legolas · 2026-10-14 · engine HEAD `94ed4e428` (read-only) · script `scripts/gd_damage_reconcile.py` · data `gd_damage_reconcile.json`

This closes gap 4 in `gd_notes.md`. The earlier "folded" arm was never checked against the configuration the sealed oracle actually ran. This note checks it.

## 1. The configuration of record and its damage path

`model/config_of_record.json` (pack v3.11) names arm **M0** as the model of record (`V0-ARM-M0`, "THE CONTROL"). The arm set is M0 / M-POL-2 / M-POL-2-NULL / W1 / W1-NULL (`V0-LAW-1` key `arm_set`). The rows list the folds and limbs; the damage folds themselves are built by the driver chain:
`gamora_kc2_play_v3p11_oracle_2026_10_02.run_one("V311-FULL")` (L153-178)
→ V310-FULL → V39-FULL (`v3p9` L52-61) → V38-FULL (`v3p8` L61-74)
→ `c11a_fold_pricing.run_arm("PW-FOLDED")` (L130-170)
→ `w1w2_lift_build.make_runner` (L124-)
→ `i26.replay` per-wave kwargs (L439-453).

For one landed instant row, before player mitigation, `threat.py resolve_attack` applies these terms in order:

| # | Term | Value in V311-FULL | Cite |
|---|---|---|---|
| 1 | Hit/crit `mult`: measured PTH, d100 `resolve_hit`, crit reading RECORD (identity) | Mean mult on trash hits **0.99993**, so effectively ×1.0 | threat.py:1853-1882 |
| 2 | Rows: slot rows, plus on weapon swings the body's weapon rows, C-11a aura grant rows and Brutal/Corrupted flat rows | — | threat.py:1932-1953; mutators.py:106-126 |
| 3 | Per-row `chance_pct` draw (row skipped on failure) | — | threat.py:2024 |
| 4 | `om` = wave `instant_mult` (D+U offensiveTotalDamageModifier) | 1.82 (w151-155), 1.83 (w156-160) | threat.py:2039; offense.py:616-633, `fold_at(w, to_hit=True, attack_speed=True)` at i26:440 |
| 5 | `om` += C-11a aura `om_add`, on covered bodies only | — | threat.py:2043-2047 |
| 6 | `a, t, own` from `GlobalMagnitudeFold(wave, board=MeasuredBoardFold)` with **C-11b on** (dex/int × 1.10 × 1.010) | — | threat.py:2077-2084; global_magnitude.py:231-261, 312-347, 517-523; board attached at run.py:1776; c11b at v3p9:144-145 |
| 7 | C-11a: retaliation rows get a = 1; five-family duration divisors | — | threat.py:2081-2082; c11a_corrections.py:400-417 |
| 8 | Leech rows dropped from the health path (L6) | — | threat.py:2085-2087 |
| 9 | Brutal/Corrupted: +0.50 into the pool on instant Pierce/Chaos rows | — | threat.py:2100-2101; mutators.py:134-145 |
| 10 | **GD composition** (KP-207): `row = m · max(0, a + (om−1))`. Physical-clamped rows are restored as `max(0, a + P + (f−1))` with the Lap-M factor, and f_unmapped = −0.44 (LO). | — | threat.py:2230-2231; gd_composition.py:130-153 |
| 11 | × n_volley × band_scale (ring volleys) | — | threat.py:2245 |

**Not in the per-hit flat figure** (counted, not summed):
- DoT: 486 of 957 landed hits carry DoT rows.
- %current-life: 298 of 957 hits carry it; it is a fraction of the target's pool.
- Leech: all leech rows are dropped by step 8.

**Declared sensitivities** (off in the record):
- `PhysLimb.HI`
- `S-AURA-STACK`
- `V311-ASCX`
- `CF-C3-LITERAL`
- the arms M-POL-2 and W1

M-POL is retired (`config_of_record` V0-LAW-1 annotation).

## 2. Two instruments, and the check that ties them together

- **ENGINE-NATIVE STATIC.** One salt-0 M0 run of V311-FULL. Afterwards, every slot of every board and line-up record is composed with that wave's own `ThreatEngine` folds, following steps 2-10 line for line (granted = none, mult 1, n_volley 1).
- **DYNAMIC.** The same run, capturing every landed hit's `_im × mult × n_volley × band_scale` for direct rows. It is captured at `CompositionFold.instant`, because `mitigate(…, "Life")` is shared by leech rows and Vitality direct rows and cannot tell them apart. The run is wrapped in-process only and restored afterwards. It produced 957 landed hits across w151-160, one engine per wave.
- **Check.** On non-granted hits the dynamic value equals the engine-native static value on **684 of 688 hits**. The 4 misses are chance-gated rows. Aura-granted hits match 92 of 235, as expected, since grants add rows and `om`. 34 hits have no static cell.

A first reconstruction re-loaded the roster without the run's winner-surface, fire-range and self-cast loaders. It did **not** reproduce the engine's profiles: its trash basic median was 15,981 against the engine's 7,683. It is kept in the JSON for audit and labelled SUPERSEDED.

## 3. Reconciled per-hit damage (E5 = record), body-weighted

**Board population** (pm4o, weighted by `n_actors_this_wave`); figures are median [p25-p75] (min-max):

| Role | Basic slot | Max slot | Mean damaging slot |
|---|---|---|---|
| trash (w = 123) | **7,683** [6,178-14,927] (3,001-24,580) | **9,435** [7,175-14,927] (4,632-24,580) | 7,481 [6,003-9,947] |
| champion-hero (33) | 12,120 [8,907-19,361] | 13,592 [10,756-19,361] | 9,706 [8,069-11,611] |
| boss+nemesis (32) | 13,004 [8,860-20,461] | 21,243 [20,114-23,810] | 13,804 [11,570-15,262] |
| all (188) | 9,925 [6,887-16,449] | 12,887 [7,618-17,358] | 8,832 [6,596-11,188] |

**Referent line-up weights** (`REFERENT_LINEUP`, the population the oracle actually fights):

| Role | Basic slot | Max slot | Mean damaging slot |
|---|---|---|---|
| trash (97) | 6,017 [3,001-7,481] | 6,575 [4,472-9,435] | 5,769 |
| champion-hero (17) | 3,859 | 5,665 | — |
| boss+nemesis (19) | 9,465 | 19,147 | — |

**Use-weighted** (dynamic: each landed hit weighted 1, so slots are weighted by the oracle's own slot choice through `GdEngagementFold.choose_slot`, gd_engagement.py:178; aura grants and volleys included):

| Role | Median [IQR] (min-max) | Hits |
|---|---|---|
| trash | **4,472 [2,851-5,609]** (610-16,449) | 309 |
| champion-hero | 3,549 [1,493-8,839] | 128 |
| boss+nemesis | 11,181 [6,086-17,262] | 249 |
| all | 4,472 [2,536-6,915] | 921 |

This is one salt, and its population is attack-weighted: chthonianservitor_b01 alone lands 100 hits.

## 4. Is the earlier "folded" figure the configuration of record? No.

The earlier folded arm equals ladder rung **E1/E2**: the oracle's multiplicative form `m·a·t·(om+own)` with C-11b. Its trash max-slot median of 16,293 is identical to E1. Its "basic" figure was weapon rows only, without the slot's own skill rows, so it is not comparable slot for slot. The config of record adds two terms the folded arm lacked.

Trash max slot, per-cell ratio, board-weighted median [IQR]:

| Rung | Change | Ratio |
|---|---|---|
| E1/E0 | C-11b | ×1.085 [1.083-1.085] |
| E2/E1 | C-11a | ×1.000 (inert on these rows) |
| E3/E2 | **GD composition** | **×0.555 [0.549-0.562]**: the attribute multiplier is now *added to* the pool, not multiplied with it |
| E5/E3 | Brutal + Corrupted flats and the +50 % pool | ×1.171 [1.042-1.431] |
| **E5/folded, max slot** | net | **×0.656 [0.584-0.733]** |
| E5 basic / folded basic | net | ×0.978 [0.844-2.017] (populations are not comparable; see above) |

Composition cuts boss basic hits less than trash hits, because it restores physical rows that were clamped to zero: boss E0 basic 4,815 → E3 9,630.

## 5. Gaps

- One salt, arm M0 only. The dynamic distribution has no between-salt spread.
- Aura grants are positional, so they appear in the dynamic figure only. The static figure is a lower bound for covered bodies.
- DoT, %current-life and leech are excluded by construction and counted (§ 1).
- The mean crit multiplier below 1 (0.99993) is not traced. It is immaterial.
