# C-13 PART 3: GD wave 151–160 enemy quantities, provenance note

**Author:** legolas (fork, PART 3 only) · **Date:** 2026-10-14
**Files:**
- `scripts/gd_enemy_quantities.py` (sha256 `03e0a049…`).
- `gd_enemy_quantities.json` (sha256 `bf4d7cc3…`). It holds per-cell rows, summaries and the footage cross-check.

**Run:**
```
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/Users/admin/Games/reincarnated-engine/src python3 scripts/gd_enemy_quantities.py gd_enemy_quantities.json
```
The engine HEAD at run time was `20ff8684`.

**Read-only.** The script imports the frozen KC2 oracle and calls only its loaders and pure functions. `threat.load_profiles` runs `verify_substrate()`, and the pool-lift and band-B loaders are digest-guarded. Nothing under `reincarnated-engine` was written. The first run did use the default bytecode setting, so it may have refreshed `__pycache__` files, which git ignores.

## Populations: two of them, each weighted two ways

| Name | What | Cells | Records | Bodies |
|---|---|---|---|---|
| **REF** | Pinned bodies of `referent_lineup.REFERENT_LINEUP`. Weight = pin `count`. A class-only pin splits its weight uniformly over its candidates; several alternatives at one point split weight equally (DECLARED). | 79 (record, wave) | 77 | 133 |
| **BOARD** | `data/kc2/pm4o_oa_da.csv`, `row_kind = monster` (the measured board). Weight = `n_actors_this_wave`. | 95 | 91 | 188 |

Bodies by role:
- REF: trash 97, champion-hero 17, boss 15, nemesis 4.
- BOARD: trash 123, champion-hero 33, boss 28, nemesis 4.

**Not in REF:** the bodies the line-up rolls from each pool's roster beyond the pins. They are rolled by the oracle's count law at run time and are not enumerable statically.

**Summaries.** Each summary is given **equal per cell** (`equal_per_cell`) and **body-weighted** (`body_weighted`), with weighted p25/p50/p75 plus min and max.

## Fields: source and grade

| Field | Source (file, column or function) | Grade |
|---|---|---|
| `hp_lo` / `hp_hi` | `monster_stats.ehp_lookup_band_b(wave, LevelLimb.LO/HI)` → `pm4_band_b_ehp_by_wave.csv`. The life equation at the band-B level × wave life term G (306–324 %) and the Ultimate pak. ("eHP" is the table's legacy name; the value is **max HP**, with no armour or resist weighting.) The oracle runs on the LO limb. | DATAMINED |
| footage HP | `kc2_referent_lineup_v3p11.csv` `max_hp_fingerprints` | FOOTAGE. **46 of 46** single-record rows fall inside band-B lo..hi (`footage_hp_crosscheck`), so it is a positive control |
| damage per hit | `threat.load_profiles(dot_corrections=True, pool_lift=pool_lift.load())`. Per slot: `direct` rows, `DamageRow.magnitude()` = (lo+hi)/2, or lo if hi = 0. Weapon rows are added to weapon-swing slots, as the oracle does. **raw** = record value at its rank. **folded** = raw × `a_mult` × `t_mult` × (`offense.fold_at(w).instant_mult` + `own_add`), where `a_mult`, `t_mult` and `own_add` come from `GlobalMagnitudeFold(wave=w, board=MeasuredBoardFold(wave=w), c11b=C11bAttributeFold())`. That is the oracle's own expression (`threat.py` ≈2037–2090). | raw: DATAMINED. folded: MODEL-VERIFIED composition; **which folds the arm of record switches on was not verified against `config_of_record`** (INFERRED) |
| excluded from per-hit | `dot`, `leech`, `percent_current_life` rows, and the non-health families (`threat.NON_HEALTH_DAMAGE_TYPES`, `DECODED_NON_HEALTH_TYPES`). They are listed per slot in `rows_not_flat_per_hit` | — |
| OA / DA | `OA_best` / `DA_best`, with `OA_DA_source` on every cell. Order of preference: (1) pm4o `OA`/`DA` at this (record, wave), **BOARD-EXACT**, all 95 BOARD cells and 26 REF cells. (2) The same record at another wave (2 REF cells). (3) Reconstruction, 51 REF cells: OA = the oracle profile's `oa_for(fold_at(w, to_hit=True))`, which has **no dexterity term** (a declared oracle gap, so it is a lower bound); DA = the stored `defensiveAbilityEquation` over pm4l `DA_bio` + wave flat/pct + Ultimate pak (75 / −8 %) + 12·level_lo, + 0.5·str where strength is known (10 cells) and absent otherwise (41 cells, a lower bound). Reconstruction checked against board-exact cells: **−6.2 % to +3.8 %**. | (1) DATAMINED. (3) INFERRED |
| ⚠ `DA_pm4l_partial_NOT_EQUATION_DA` | The pm4l / pack `monster_defense.json` v23b "DA" (≈ 400–900) is `(DA_bio + wave flat)·(1 + wave %)`. **It omits the level term, the attribute term, the Ultimate pak and the +53 tail. Do not use it as DA.** It is carried only so nobody mistakes it for DA later | DATAMINED (partial) |
| armour, absorption | `pm4l_mitigation_by_body.csv` `armor`, `absorption_pct` at (record, wave) | DATAMINED |
| resists (10 families) | `pm4l_mitigation_by_body.csv` `res_*`: physical, pierce, fire, cold, lightning, poison (acid), life (vitality), aether, chaos, bleeding | DATAMINED |
| `swing_period_s` | `ThreatProfile.swing_period_s`. The `…_with_wave_attack_speed` variant divides by `fold_at(w, attack_speed=True).attack_speed_mult` (×1.11). The oracle's default arm does **not** fold attack speed (`offense.declared_not_folded_for`) | DATAMINED / arm-dependent |
| special reuse | `AttackSlot.effective_cooldown_s` (`skillCooldownTime` if > 0, else slot `delay_s`) | DATAMINED |
| role | pm4o `threat_tier` where the record is on the board. Otherwise inferred from the path and `pm4i_band_c_roster.csv` `monster_class` | DATAMINED / INFERRED |

## Headline values (body-weighted)

| Quantity | REF median [p25–p75] | BOARD median [p25–p75] |
|---|---|---|
| HP (lo) | 275k [202k–448k] | 409k [173k–570k] |
| Damage, basic hit, folded | 4.4k [1.6k–8.1k] | 8.1k [5.8k–10.0k] |
| Damage, max slot, folded | 9.8k [3.9k–16.8k] | 19.3k [12.1k–25.5k] |
| Damage, basic hit, raw | 814 [664–903] | 815 [736–990] |
| OA (best) | 2176 [2045–2352] | 2480 [2357–2647] |
| DA (best) | 2151 [2049–2272] | 2337 [2186–2514] |
| Armour | 915 [612–1246] | 933 [612–1308] |
| Absorption | 70 % on every cell | 70 % on every cell |
| Swing period | 1.05 s [0.82–1.15] | 0.93 s [0.60–1.10] |
| Special reuse | 5 s [3–6] | 4 s [3–7] |

**Fire resist:** median 0, p75 25, range −20 to 80. **Zero cells ≥ 100**, so there are no fire immunes in either population.

The equal-per-cell versions are in the JSON. For example, BOARD equal-per-cell HP median is 444k and DA median is 2473.

## Gaps
1. **REF's unpinned remainder bodies** are not in the population.
2. **OA for 51 REF cells has no dexterity term** (oracle gap), so it is a lower bound. Board-exact OA runs about 15 % higher than the profile OA on the same records.
3. **DA for 41 REF cells has no strength term**, so it is a lower bound (about 0.5·str, roughly 350, or about 15 %).
4. **The folded damage arm was not reconciled with `config_of_record.json`.** The raw values are unaffected.
   - The physical clamp (`t_mult = 0`) zeroes the basic hit on 10 cells, all bosses with physical-only swings.
   - The attribute multiplier (dex/245+1, int/215+1) is ≈ 4.3–4.8 where it is measured. It dominates the raw-to-folded ratio.
5. **No armour pierce in the per-hit totals.** `armor_pierce_ratio` rows (2) are excluded.
6. **`percent_current_life` rows** (229 across all profiles) are not flat magnitudes and are excluded.
7. **Attack rate covers the basic swing and special reuse only.** It does not cover AI selection frequency (`choose_slot` chance weights).
8. **Profile `level` differs from band-B `level_lo`** on some records (e.g. `wraith_a01`: 109 against 103). HP uses band-B, as the oracle does.
