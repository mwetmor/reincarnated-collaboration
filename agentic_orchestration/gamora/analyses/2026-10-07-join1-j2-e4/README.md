# JOIN-1 · J2 · E4: evidence (KP-331)

gamora, 2026-10-07. Engine instrument commits, in order:

| Commit | What it carries |
|---|---|
| `a2cb5486` | WARN-E3-1 instrument |
| `eae6af14` | INFO-E3-1 binder |
| `a3eb0e54` | E4a operands (rulebook worktree pinned here) |
| `0e393d7e` | E4b runner, controls and predictions |
| `8861f248` | E4c form-level script; all runs of record started at this HEAD |
| `47c976f7` | E4d classifier `_norm` fix and offline recheck |
| `99043eed` | E4e per-cell / tick-split reader, plus NC-J2-5c registered before its run |

Every prediction below was committed before the run it predicts. The single exception is NC-J2-5c, which was registered after NC-J2-5b's miss, at `99043eed`, and before its own first run.

Bulk emissions, witness records and parity cell dumps have been moved (`os.rename`, nothing deleted) to `/Users/admin/Games/join2-e4-bulk-evidence/<same relative path>`. Each run dir keeps:
- `bulk_manifest.json`: FILE_sha256 and bytes for every moved file, verified after the move;
- `emission_manifest.json`: the emitter's own manifest, which carries ROWSET digests and sim_errors.

`recheck` falls back to the bulk path. `percell` / `ticksplit` read `<run>/emission`, so point them at the bulk copy.

Disk never went below 29 GiB free (HALT 20).

---

## 1. WARN-E3-1: the witness judges an emitter wrapper by the innermost callable's FULL fingerprint

**What changed.** Witness v2 records `wrapped_fp`, the fingerprint of the innermost wrapped callable. `classify()` compares it two ways:
- **do-not-substitute rows:** against the sealed census;
- **substituted rows:** against the bind log's installed-object fingerprint.

`classify()` no longer reads the closure name. Tests: `tests/test_join2_e3_warn_e3_1.py`, which reproduces the Gate's three rows: sealed, re-homed, and a `wraps` delegate.

**INFO-E3-1.** The binder's R-5 sealed-object check now tests four things, in this order:
1. no `__wrapped__`;
2. `co_filename` lies under the sealed dir;
3. `__globals__` is the home module dict;
4. the code object equals the code compiled from disk.

**Checker defect found and fixed in E4 (`47c976f7`).** At the E4 baselines the new classifier first reported 380 / 250 hits. The cause was the record-level keys `defined_on_class` / `wrapped_fp` sitting inside the compared dict. `_norm` now drops them before equality. `defined_on_class` is still checked separately, and a test covers that. Every run below was rechecked offline from its kept records under the fixed classifier (`recheck.json` in each dir).

**The control.** It was predicted before the run (runner `PREDICTIONS["join-gd--rehome"]`): re-home `intake.armour_branch` in one emitter cell (W1-NULL/3). Results, all as predicted:

| Run | J-S8 | Recheck hits |
|---|---|---|
| `golden-master` (JOIN gd, no perturbation) | 7/7 | 0 |
| `oracle-witness` | 7/7 | 0 |
| `rehome-W1-NULL-3-armour_branch` | 7/7 (the re-homed copy computes identically) | exactly 1: pid 3507 = the W1-NULL/3 cell, key `intake.armour_branch`, classed `('emitter-wrapper', 'foreign')`; every other cell clean; `tree_ok` |

## 2. A-5 parity probe, per site (`parity/parity_report.json`, engine `8861f248`)

`sys.setprofile` counts calls under ORACLE and under JOIN, in two cells (M-POL-2/0 and W1-NULL/3). Both cells PASS. Grains are row-equal on all 7 in both cells, and foreign_reads = 0.

Class key for the table:
- **T** = transcribed. Under JOIN the sealed body is called 0 times and the form takes exactly the ORACLE count.
- **D** = dispatch-then-delegate. The sealed body is still reached, but only through the named rulebook caller.
- **S** = subsumed. Row 9 is reached under ORACLE only from inside `applied_for`. Row 10's adapter replaces that path, so under JOIN it has 0 calls. This was declared as class S before the run of record.

| Row | Site | Class | ORACLE sealed (M-POL-2/0 · W1-NULL/3) | JOIN form | JOIN sealed, by caller |
|---|---|---|---|---|---|
| 2 | threat.resolve_hit | T | 2791 · 3150 | same | 0 |
| 3 | threat.mitigate | T | 4659 · 5839 | same | 0 |
| 4 | intake.physical_applied | T | 6606 · 8376 | same | 0 |
| 5 | player_offense.applied_damage | D | 24062 · 25070 | 22905 · 23937 | 22905 via `applied_damage_` plus 1157 · 1133 via `families.summon_applied`; sums equal ORACLE |
| 7 | player_offense.mitigation_at | T | 85462 · 88443 | same | 0 |
| 8 | summon_offense.defence_of | T | 1157 · 1133 | same | 0 |
| 9 | summon_offense.resist_column_for | S | 2314 · 2266 | 0 | 0 |
| 10 | summon_offense.applied_for | T | 2314 · 2266 | same | 0 |
| 11 | SecondaryStreams.soulfire_applied | T | 10403 · 10868 | same | 0 |
| 12 | SecondaryStreams.bleed_dps_against | T | 14318 · 14918 | same | 0 |
| 14 | MeasuredBoardFold.pth_for | D | 1634 · 2017 | same | all via `pth_for_` |
| 16 | GdRepositionFold._stop_where_close_enough | T | 15463 · 16890 | same | 0 |
| 31 | PlayerOffense.__post_init__ | D | 16 · 16 | same | all via `post_init_` |

**Consumer read-back** (`readback_pass` true in both cells):
- `secondary_streams.SOULFIRE_PERIOD_S` = `3fc99999a0000000` under both configurations.
- `energy.SoulfireCostTerm.interval_s` default = `3fc99999a0000000` under JOIN, against `3fc999999999999a` under ORACLE. This is the D-1 RB-REPR-F32 route at row 24.
- *Weak read-back, recorded:* the probe's list of live `PlayerOffense._acc.hits_per_tick` instances was empty at process end in both configurations. So that read-back witnessed nothing. The tick split's observable is §4 NC-J2-5c instead.

## 3. Form-level controls (`formlevel.json`, `gamora_join2_e4_formlevel_2026_10_07.py`): all as predicted

| Control | Prediction | Result |
|---|---|---|
| NC-J2-1 (grid) | RED 140/440 = 63 + 77, every 55.0 row GREEN | 140 = 63 + 77; 55.0 rows GREEN |
| A13-div | rulebook equals sealed twin row for row; RED 146 | equal; 146 |
| NC-J2-11a | 158000 pairs, 46830 differing, max 2 ulp, 0 above 2 | 158000 / 46830 / 2.0 / 0 |
| NC-J2-11b | 170 physical bit-exact at 'pre'; more than 2 ulp exactly on the 138 overflow-bearing; at most 2 ulp elsewhere | 170 / 0 mismatches; 138 = the overflow set; all-absorb max 1 ulp; non-physical 505 verifiable, 0 unverifiable, max 1 ulp |

## 4. Emission controls (J-S8 grain comparison; `controls/<ID>/report.json`)

**Common to every run:**
- 25/25 cells reported.
- foreign_reads 0.
- `head_fixed` and `instrument_pinned` true.
- For every JOIN run, the offline recheck under `47c976f7` / `99043eed` gave 0 hits and `tree_ok` true (`controls/<ID>/recheck.json`).

**Per-cell readings** come from `percell.json` / `ticksplit.json`, produced by `gamora_join2_e4_percell_2026_10_07.py`.

| ID | Prediction (abridged) | J-S8 grains RED | Result |
|---|---|---|---|
| NC-J2-1 | 7/7 GREEN (the floor is never reached on the referent) | none | as predicted |
| A13-hit / -sealed | RED on at least one grain; pair ROWSET-equal on 7 | G1 G2 G3 G5 | as predicted; pair 7/7 equal |
| **NC-J2-2** / -sealed | G2 RED; **pair ROWSET-equal on all 7** | G1-G5 G7 | **MISS on the pair (see below)**; G2 RED as predicted |
| NC-J2-3 / -sealed | refusal KeyError 25/25, the sealed message; pair equal | G1-G5 G7 | as predicted. 25/25 `raised:KeyError`, msg "damage family 'Fire' has no measured resistance on the Lap-A sheet…" at `threat.mitigate`, wave 151; pair 7/7 equal |
| NC-J2-4 | OFFENSE refusal naming the player-stream lane 25/25 | G1-G5 G7 | as predicted. 25/25 `UnmappedDamageFamily` "…'Lightning'… registry 'gd-v0-without-Lightning' (lane player->monster/player-stream)", wave 151. The emitter does not record the tick, so "at the first Soulfire row" is read only as "in wave 151" |
| NC-J2-4b | refusal naming the SUMMON lane in the cells that land a fire summon packet (count not predicted); player streams never refuse | G1-G5 G7 | consistent: 25/25 cells refuse, every message is "…'Fire'… (lane player->monster/summon)", and 0 messages name a player-stream lane. Because the count was 25/25, "every other cell unchanged" was not exercised |
| NC-J2-5 / -sealed | G7 RED 25/25 (tick period 12.25 -> 12.5); pair equal | G1-G5 G7 | as predicted. G7 differs in 25/25 cells, and the world clock differs on 250/250 G7 rows; pair 7/7 equal |
| **NC-J2-5b** | G7 GREEN; at least one player-hit grain RED | **none (7/7 GREEN)** | **MISS (see below)** |
| NC-J2-5c (added) | world clock bit-equal on every G7 row; leech/world-tick LOWER in 25/25 cells; G3 differs in 25/25 cells | G1-G5 G7 | as predicted. 0/250 G7 rows differ in tick_period_s / phase_offset; leech per world tick lower in 25/25; G3 differs in 25/25 |
| NC-J2-6 / -sealed | G4 RED 25/25; pair equal | G1-G5 G7 | as predicted. G4 differs in 25/25 cells; pair 7/7 equal |
| NC-J2-7 / -sealed | RED on G1-G5 and G7; pair equal | G1-G5 G7 (G6 GREEN) | as predicted; pair 7/7 equal |
| A13-resist / -sealed | G2 RED; pair equal | G1-G5 G7 | as predicted; pair 7/7 equal |
| A13-armour / -sealed | G2 RED; pair equal | G2 G3 G5 | as predicted; pair 7/7 equal |
| A13-pth / -sealed | G1 RED; pair equal | G1-G5 G7 | as predicted; pair 7/7 equal |
| A13-board / -sealed | RED on at least one grain; pair equal (immune_records asymmetry declared) | G1-G5 G7 | as predicted; pair 7/7 equal; the declared asymmetry did not bite |
| A5-row5 | row 5 and the summon lane refuse 25/25 | G1-G5 G7 | as predicted. 25/25 "…'Physical'… (lane player->monster/player-stream)" |
| A5-bleed / -sealed | RED on at least one grain; pair equal | G3 | as predicted; pair 7/7 equal |

**Not run, as declared in `E4_NOT_RUN`:**
- **A13-PCL:** the PCL operand is carried but not read in v0.
- **A13-disc:** this would be the same Cited route as NC-B1 of record.

### NC-J2-2: a MISS on the A-13 pair (`controls/pair_NC-J2-2.json`)

JOIN against the sealed NC-2:
- equal on G1, G3, G4, G5, G6 and G7;
- **G2 differs on 26,406 rows**, with 0 rows found on only one side.

**Where the difference sits.** It is confined to the G2 *instrumentation* fields: `stage_order`, `after_stage_1`, `after_stage_2`, the recomputed stage values, and `attribution`. The `applied` value equals the sealed twin on every row. G5 terminal reasons are equal too (19 survived, 6 deaths in both).

**Mechanism.** The v0 order operand (`intake_order_override`) changes only the arithmetic inside the substituted `physical_applied`. The sealed `IntakeFold.order` is on the do-not-substitute list and is not moved. It still drives two things:
- the attribution text;
- the emitter's per-stage recomputation.

So the damage is the same as the sealed NC-2, but the record of *how* it was staged still names the sealed order.

**Implication for J3.** An intake-order lever has to set `IntakeFold.order` at composition level, not only the form's arithmetic. Otherwise its own telemetry contradicts the damage it produced. Nothing was changed in E4. This is reported as a finding.

### NC-J2-5b: a MISS (prediction "G7 GREEN; at least one player-hit grain RED"; observed 7/7 GREEN)

**Mechanism** (sealed `player_offense.HitAccumulator.tick`, the hot-loop gate `po_hits` in `run.py`):
- The gate yields one boolean per world tick.
- At `hits_per_tick >= 1` it fires on every tick.
- So `kit_as_pct/world_as_pct = 200/196 > 1` cannot be told apart from `1.0`, and any kit speed above world speed is inert. The credit overflow is invisible.

**Post-hoc reading (not a prediction)**, from `controls/NC-J2-5b/ticksplit.json`:
- the world clock is bit-equal on 250/250 rows;
- leech per world tick is EQUAL in 25/25 cells.

**The tick split re-tested below saturation.** NC-J2-5c (kit 98 -> 0.5 hits/tick) was registered with its prediction at `99043eed` and passed (table above). Under JOIN the world clock and the kit cadence separate exactly as E1-b R-6 intends, provided the kit is no faster than the world.

**Implication for J3 (L-01 at GD).** The continuous-as-proportional cadence has a ceiling of one hit per world tick. Kit attack speed above world attack speed needs either a multi-hit gate or a world clock that follows the faster kit. That is a design decision for J3, not an E4 fix.

## 5. E2c README "34": KP-331 item 3

The corrigendum was already present in `ac6d565b6`. It is now stated explicitly, append-only, in collab `326186737` ("34" -> 25).

## 6. Files

**Engine scripts** (`src/reincarnated/simulation/scripts/`):
- `gamora_join2_e3_run_2026_10_07.py`: runner, `E4_CONTROLS`, `recheck`;
- `gamora_join2_e4_parity_2026_10_07.py`;
- `gamora_join2_e4_formlevel_2026_10_07.py`;
- `gamora_join2_e4_percell_2026_10_07.py`;
- `join2_bprime_witness_hook_v2/sitecustomize.py`;
- `join2_rulebook_hook/sitecustomize.py`.

**Rulebook:** `/Users/admin/Games/reincarnated-engine-join2-rb` at `a3eb0e54`.
