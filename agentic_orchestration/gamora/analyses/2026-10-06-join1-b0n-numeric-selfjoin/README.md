# JOIN-1 · B0-N: the numeric self-join on J-S4b (`gd-eor-warlord-referent`)

**NOT-A-GRADED-RUN.** Nothing under `simulation/kc2/` or pack v3.11 was edited. The ORACLE ran from the sealed worktree (`969fbd8d`, tag `kc2/referent-v1-sealed-r2-oracle`) through the J-S8 emitter, unmodified and in DRY-RUN. corpus.db was not written.
gamora, 2026-10-06, Run JOIN-1 (charter v0.6.5 § 4.2; conductor KP-304). Gate: jack-ryan Gate-2.

> ⚑ **APPROX-CEILING, on every figure below:** J-S4b's mapping grade is NULL (owed at J4a), so every B0-N figure carries the charter § 4.2 APPROX ceiling. Binding coverage is 38 of 104 record rows. Of those 38, **32 are PROVISIONAL-UNSTAMPED** (source_value under the RDR-unit IDENTITY convention, because no rule covers them). The other 6 are stamped in the scratch lane P (4 by R-T2, 2 by the R-CTX-GEO amendment: `eor_radius_m`, `soulfire_explosion_radius_m`). Lane P is not yet applied to the corpus of record.

- **Pre-registration (committed alone first):** engine `cb063d86`, `simulation/math/join1-b0n-numeric-selfjoin-2026-10-06.md`
- **Prerequisites:**
  - engine `ccd89e38`: KC-1 + KC-3
  - engine `faf59dd2`: stamping generator
  - collab `stamping/`: the package for elrond
- **Harness:**
  - `simulation/scripts/gamora_join1_b0n_selfjoin_2026_10_06.py`: prepare / emit / compare / probes
  - `simulation/scripts/join1_b0n_hook/sitecustomize.py`: the in-process binder
  - `simulation/scripts/gamora_join1_b0n_s47_evidence_2026_10_06.py`: § 4.7 evidence
- **Path:**
  1. scratch corpus lane P: the corpus of record (`0d73475a…`) plus R-T2 stamping (14) plus the R-CTX-GEO amendment (5).
  2. `compile_kit`, with KC-1 and KC-3.
  3. Binder, operand map B-01…B-37, which binds 44 sites.
  4. The J-S8 emitter on the sealed tree: V311-FULL, 5 arms × 5 salts.
  5. G1…G7, diffed row by row against J-S8 (MANIFEST `f82807fb…`).

## The verdict

**B0-N = PASS-BY-DISPOSITION, numeric, self-join (J-S4b). One divergence, with a disposition. After that one site, a 7/7 bit-exact reproduction.**

| run | binding | G1 | G2 | G3 | G4 | G5 | G6 | G7 | OBS-1 | reading |
|---|---|---|---|---|---|---|---|---|---|---|
| BASELINE | none | = | = | = | = | = | = | = | 25/25 | P0 HIT: the instrument reproduces J-S8 |
| **R1** | full map (44 sites) | ≠ | ≠ | ≠ | ≠ | ≠ | = (empty) | ≠ | 25/25 | **P2 HIT: RED, as predicted.** 8/25 cells move on G1/G2/G4/G5/G7 and 20/25 on G3; 0 terminal-wave flips |
| **R2** | R1 minus B-20b only | = | = | = | = | = | = | = | 25/25 | **P3 HIT: 7/7 ROWSETs equal J-S8.** Attributes R1's whole divergence to B-20b (#24, #9) |
| NC-B1 | R2 with `eor_radius_m` 3.0 → 3.1 in the scratch record | ≠ | ≠ | ≠ | ≠ | ≠ | = | ≠ | 25/25 | RED 25/25 cells. The instrument sees the compiled-kit radius |
| NC-B2 | R2 with the leech operand on the r26 row (64 %) | ≠ | ≠ | ≠ | ≠ | ≠ | = | ≠ | 25/25 | RED; G3 moves on 25/25 cells. The instrument sees the leech operand |

**The `EXECUTES-THE-BOUNDARY-RULEBOOK` set (J-P2)** (APPROX ceiling applies):

| row | carried by | R1 | R2 |
|---|---|---|---|
| TA-X-07 conservation | G2 offered → applied chain | RED (D-1) | **reproduces** |
| TA-X-20 hit-test predicate + target multiplicity | G4 occupancy; B-01 radius 3.0 bound via the compiled kit (bit-equal) | RED (D-1) | **reproduces** |
| TA-X-29 global-magnitude fold | G2 `pre_mitigation` | RED (D-1) | **reproduces** |
| TA-X-30 pursuit halt | G4 halt counters | RED (D-1) | **reproduces** |

### The divergence list (the charter § 4.2 pass rule)

| id | site | record | oracle | effect | disposition |
|---|---|---|---|---|---|
| **D-1** | B-20b `secondary_streams.SOULFIRE_PERIOD_S` | `soulfire_period_s` = 0.2 (DB decimal) | `0.20000000298023224` (the float32-widened DBR real; pack row S13-SF-PERIOD) | RED on every grain except G6 (first divergence at tick 173 to 3878 in 8 cells; G3 in 20 cells); 0 terminal-wave flips | **`closes-in-J2`.** The oracle holds one operand at two sites in two representations: `fixture.SOULFIRE_PERIOD_S` = 0.2 is read by `energy`, while the f32 value is read live by the Soulfire credit. J2's FORM/OPERAND split must name **one** slot with **one** representation. The FORM rule "a GD DBR real is float32" belongs to the rulebook, not to the record. **Also routed to elrond:** J-S4b's agreement check marked S13-SF-PERIOD "agree" at 0.2 against the pack's 0.20000000298023224, using an undeclared tolerance. |

There are no other numeric divergences. The bind log shows 43 of 44 site bindings bit-equal to the oracle (P1 HIT). **No undisposed divergence, so B0-N is not a FAIL.**

### C-01, the element check (KC-1)
The compiled `dominant_element` is `physical` (basis `court`), which matches the oracle's player stream (physical path, `FIRE_TO_PHYSICAL_CONVERSION_PCT` = 100). **PASS.** Under the pre-KC-1 rule the compiler emits `fire`, and the check would **FAIL**. No value slot exists for this; it is a binder refusal check.

## Binding coverage: what the positive control actually exercised (#86)

The reach probes ran on one cell (V311-FULL, M-POL-2, salt 0) with the R2 binding in place, perturbing one binding at a time (floats × 1.05, ints + 1, B-12 = 0.64). The unbound cell, bound cell #1 and bound cell #2 have the same digest (`8b81b3ff…`), so the probe is deterministic and the binding is inert when its values are equal. That digest also equals the J-S8 manifest's `inertness_bare_vs_hooked["M-POL-2|0"]`.

| verdict | binding ids |
|---|---|
| **REACHED** (11) | B-01 radius (through the compiler) · B-03 base tick period · B-12 leech (r20 row) · B-22 Soulfire projectiles · B-24 attack speed · B-25 HP max · B-30 DA · B-32 ADCTH · B-33 HP regen · B-34 physical resist · **B-20b (by R1 itself)** |
| **NOT-REACHED: the site is read at import into a derived module constant before the binder can set it** (binder-unreachable without editing the oracle) | B-17 (`BLEED_FLAT` → `BLEED_TOTAL_PER_APPLICATION`), B-18 (`BLEED_BASE_DURATION_S` → `BLEED_DURATION_S`), B-19 (→ `BLEED_MODIFIER_PCT`), B-23 (`SOULFIRE_FLAT_LIGHTNING` → `SOULFIRE_RAW_PER_PROC`), all in `secondary_streams`. **Disposition `closes-in-J2`:** an operand slot must be read at use, not frozen at import. |
| **NOT-REACHED: not on the V311-FULL path, as predicted** | B-08 drain, B-09 total rank (KP-243), B-10/B-11 %WD (dead `weapon_damage_pct`, KP-243 V2-EOR-WD-DEAD), B-28 / B-29 energy ceiling and reservation |
| **NOT-REACHED: not predicted; cause not traced (findings)** | B-02 time-between-attacks (the tick period comes through B-03 × attack speed) · B-04 tail · B-05 rotation · B-06 / B-07 mana cost and factor · B-13 conversion % · **B-14 / B-15 flat physical band** · B-16 flat fire · B-20a · B-21 · B-26 / B-27 energy max and regen · **B-31 armour (`threat.PLAYER_ARMOR`, `intake.SHEET_ARMOR_RATING`)** · B-35 v_ref · B-36 run-speed cap · B-37 run speed |

**P4 scored:**
- 7 of 11 predicted-REACHED were reached.
- 4 MISSED: B-14, B-15, B-17, B-31. B-35 was also predicted reached and was not.
- All 6 predicted-NOT-REACHED held.

⚑ **Two of the misses contradict prose on record and are findings, not dispositions:**
- **(i)** KP-243 calls `run.py:1271-1280`'s flat-physical band the live per-tick damage. On V311-FULL a 5 % move of `FLAT_PHYSICAL_BASE_MIN`/`MAX` does not move the cell. My unchecked hypothesis is that the composition supplies `player_damage_per_tick` through `player_offense`, so the band is the default path only.
- **(ii)** The sheet armour 3557 is not the live armour operand. My unchecked hypothesis is that the per-layer intake armour supersedes the aggregate.

Neither changes this verdict, because both values are bit-equal and unreached. Both are routed to J2's operand-slot list.

**So read the positive control honestly:** R2's 7/7 bit-exact reproduction is **demonstrated through 11 reached operands** (radius, tick clock, leech, Soulfire projectile count, attack speed, HP, DA, ADCTH, regen, physical resist, and the Soulfire period by R1). The other 27 bindings reproduce because they cannot move this configuration, not because the binder carried them.

**The 64 record rows not bound** each carry a class and disposition in `runs/R1/binding_table.json` → `record_rows_unbound`. None is UNDISPOSED. The breakdown:
- devotion levels (AC-9.1): `permanent, recorded`
- Vire's Might / War Cry / Blitz / Ascension / Violent Delights / summons / modifier rows (V2-KIT-SCOPE, or CSV-sourced through `counterplay.Kit` / `per_cast_energy`): `closes-in-J2`
- sheet and item quantities the oracle never reads: `permanent, recorded`
- `eor_weapon_damage_pct_total_r26`: INERT (KP-243), `permanent, recorded`

Two further rows are derived cross-checks:
- `eor_tick_period_s` equals the oracle's `tick_period_s` 0.0816326530612245 bit for bit.
- `eor_ticks_per_s` is 12.25, which is 1/period to 9 decimals.

The oracle operands the record does not carry (12 groups) are listed with dispositions in the same file (`unbound_oracle_operands`): `schema-change-owed` where the record must carry a row, `closes-in-J2` for slots and CSV tables.

## The negative controls in detail (predicted at `cb063d86`)

- **NC-B1** (`eor_radius_m` 3.1, applied record-side, so it flows through stamping, the compiler and the binder): RED 25/25 cells. Prediction: "`n_bodies_in_disc` rises on some ticks and never falls on a tick whose positions are unchanged up to the first divergence." **At each cell's first divergent G4 row: up 22, equal 3, down 0. HELD.** Downstream the trajectories part, and the summed occupancy falls (149,821 → 145,961), because a wider disc clears bodies faster. That is reported beside the prediction, not in place of it. Also: G5 has 0 terminal-wave flips and 6 terminal-reason flips.
- **NC-B2** (leech on the r26 row, 0.64): RED, with G3 moving on 25/25 cells. Prediction: "`heal_hp` up on rows with leech events; 0 terminal-wave flips." **At each cell's first divergent G3 wave, heal is up on 25 of 25: HELD. 0 terminal-wave flips: HELD.** Summed heal over the whole run falls (21.84 M → 21.68 M) after trajectories diverge. 1 terminal-reason flip, inside w160.

## Charter § 4.7 evidence: ORACLE output is byte-identical after the compiler change

1. **Sealed vs post-change HEAD, the same command:** pass-4 `graded V311-FULL` (5 × 5) was run from the sealed worktree `969fbd8d` and from the main checkout at HEAD `faf59dd2` (which contains `ccd89e38`). With `wall_s` excluded the two outputs are **byte-identical**, canonical sha256 `eec33665…` on both sides. Files: `s47/graded_V311-FULL.sealed969fbd8d.json`, `s47/graded_V311-FULL.rerun.json`.
2. **Import closure** (`s47/s47_evidence.json`): 141 `reincarnated` modules load and 352 engine files are loaded or opened. **No `kit_compiler` module loads. No loaded file changed between the seal and HEAD, and none is dirty against HEAD.**
3. **The pass-4 artifact of record** (`graded_V311-FULL.json`, FILE `62aecaa6…`) differs from both reruns in exactly **two provenance keys per arm**. The derivation filenames `pilot_derivation_referent.json` and `pilot_move_derivation_referent.json` became `kc2_hunt_pilot_derivation_v3p9.json` and `kc2_pilot_move_derivation_v3p10.json`, with **identical sha256 values** (`fd3f6585…`, `8c40d895…`). This is the input-path move at star-lord's v3.11 closure, which happened before the seal (charter v0.6). Every fight value is equal. The harness's own verdict line reads "NOT SHOWN" because it compares against that pre-seal artifact; the comparison that answers § 4.7 is sealed vs HEAD (item 1). That line is not edited here.
4. **The J-S8 emitter** reproduces `f82807fb` on 7/7 ROWSETs (BASELINE), and R2 with the binder loaded does too.

## Routed

- **elrond** (via the conductor):
  - the stamping package `stamping/` (guards green: 14 R-T2, 5 R-CTX-GEO; expected post-apply J-S4b ROWSET `c3e0f121…`);
  - the S13-SF-PERIOD tolerance in the J-S4b agreement check;
  - the mapping grade, owed at J4a.
- **jack-ryan** (Gate-2):
  - the B0-N table and dispositions;
  - confirmation of the R-CTX-GEO amendment (KP-304, provisional);
  - a decisions-log entry for the KC-1 meaning shift.
- **J2** (operand-slot list):
  - D-1, the two-site Soulfire period;
  - import-frozen derived constants in `secondary_streams`;
  - findings (i) flat band and (ii) sheet armour not live on V311-FULL;
  - the CSV-sourced kit operands.

`runs/<R>/` holds, per run: `bindings.json`, `binding_table.json`, `compare.json`, `run_manifest.json` and a `bindlog_sample.json`. `runs/R2/probes.json` holds the reach probes. The grain files (about 46 MB per run) stay in the scratchpad and are not committed; each run's manifest pins their FILE and ROWSET digests.
