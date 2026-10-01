# KC2-PLAY · T-A GRADE OF RECORD, graded attempt 2 of 2 under prereg v1.13 (overall attempt 3; the last under the cap): verdict `PASS`

> **STATUS:** CURRENT. Grade seat, Run KC2-PLAY (charter KP-187 / KP-188). **Author:** gamora (simulation seam; the prereg's author, grading strictly by its text), 2026-10-01. **Conductor:** gandalf.
> **Graded object:** drax's emission at godot `7a97716`, `reincarnated-godot/evidence/kc2-play/2026-10-01-ta-attempt2-v1.13-cells/` (25 `cell.json`, `ta_manifest.json`, `ta_verdict.json`, `harness_stdout.txt`, MANIFEST). Every byte was read through `git show 7a97716:<path>`, and each worktree copy was checked equal to its blob.
> **Graded against:** prereg **v1.13**, FILE `c35cca9ceb189b5f78a09b402f9df81b3bb126db132643a57049eb1cc8a46d68`, with every row it carries from **v1.12** (FILE `a0454776…`, re-derived) and, by reference, v1.8 … v1.11.
> **Instrument (mine, independent of jack-ryan's H-7 grader):** `agentic_orchestration/gamora/analyses/2026-10-01-kc2-play-ta-attempt2-v1.13-grade/grade_attempt2_v1p13.py` (FILE `3fc86d70…`). It writes `results.json` (`edbb9809…`) and the grader-written verdict file `ta_verdict_v1p13_attempt2.json` (`521e3fea…`); its stdout is `run_stdout.txt` (`3e0cb27e…`). Re-running it reproduces all three byte for byte.
> **Authority:** grading only. **No expected value or tolerance was changed. No row was reclassified. The prereg was not edited. Nothing graded was re-run.** The same grader function was run, unchanged, on the § G.1a pre-read emission (godot `4833bcf`) only to print the item-5 face (§ 4).

---

## § 0 · Integrity, derived before any row was read

| object | expected | **derived** | |
|---|---|---|---|
| prereg v1.13 · carried v1.12 | `c35cca9c…` · `a0454776…` | `c35cca9ceb189b5f…8a46d68` · `a0454776ab91d85f…a9797fc7854` | ✓ |
| attempt `MANIFEST.json` | `1e27c5fd…` (KP-188) | `1e27c5fdd83e9927a570ae8bc81bf13babe3c726a7a7692abfd988a865027498` | ✓ |
| attempt members | 28 | 28/28 sha256 and bytes match; blob = worktree; tracked set = members + `MANIFEST.json`; tree (pack law) `d5e8ab95…` = MANIFEST; `⚑ filing_checks.all` true | ✓ |
| `ta_manifest.json` · `ta_verdict.json` | `9e35fb2e…` · `f7e19dc1…` | `9e35fb2e3286b033…` · `f7e19dc1a0ec0b11…`; equal to the MANIFEST's pins; `ta_verdict.ta_manifest_sha256` = the filed manifest | ✓ |
| **runtime tree** `kc2_runtime/` | `d03ca891…` (KP-186) | **`d03ca8913901d61de73db40287e31e498e8b2714521f8221fde414682e328ccd`**, recomputed from blobs at `7a97716`; 85/85 members, 0 failures, every member tracked; `kc2_runtime/` byte-unchanged `0f36826 → 7a97716` and `4833bcf → 7a97716` | ✓ |
| runtime as the harness saw it | — | `runtime_digest.value` = `at_boot.value` = `at_end.value` = `d03ca891…`, `unchanged_through_the_run` true; `pre_attempt_read.expected_runtime_digest` = `runtime_digest_at_boot` = `d03ca891…`, `equal_at_boot` true (the WARN-2 boot check) | ✓ |
| `runtime_header` (the `.app`, run) | P-4 | `read_by_running`, `equals_P4`, model `48a4c94c…` / reference `1887257f…`, cross-pin, vendored runtime `d03ca891…` = the runtime digest | ✓ |
| **`pre_attempt_read.finding_sha256`** = the H-7 read | `69235e13…` | `69235e139a2e3bc4340fd2ace4762b023f8c7290cda7fe709f75bec0e486d742` = the worktree file = its blob at collab `9e1b19872` | ✓ |
| emission identity | — | `prereg_version` v1.13, `prereg_sha256` `c35cca9c…`, carried v1.12 `a0454776…`; `run_kind` `attempt`; `attempt` "v1.13 attempt 2 of 2", overall 3; `verdict` null (the harness computes none) | ✓ |
| G3 input (KP-184) · (L2) operand file | `f861b7a1…` · `b5bcdb7b…` | `f861b7a16111531b…` · `b5bcdb7ba61b8ffd…` | ✓ |
| booking census | `73ebc5db…` (PINS.2) | `73ebc5db15aa1df8…` (T 22 · S 11 · F 14) | ✓ |
| **model pack** (19) · **reference pack** (7) | `48a4c94c…` · `1887257f…` | both recomputed by their manifests' law; on-disk set = manifest set; cross-pin `48a4c94c…`; `math_rules.json` FILE `3b1e2d01…` | ✓ |
| POOL-466 / SWING-456 / NONSWING-10 | PINS | 466 `33c886a1…` (both routes agree) · 456 `706a61d5…` · 10 `00b4cb0e…`, **recomputed through the oracle** (`pool466`; `load_profiles` under P-5's call). FALLBACK-158 not recomputed (no graded row reads it) | ✓ |
| H-9 (5) · H-10 receipt | documents of record | all six FILE digests reproduce | ✓ |
| oracle tree | engine `22cd2288`, clean | HEAD `22cd2288`; `git status --porcelain` empty under `simulation/kc2`, `export`, `simulation/scripts` (the engine's other uncommitted changes, KP-188's declaration, are outside these) | ✓ |
| § F.2m.2 vector | pinned | **re-derived from `waves.json` by its law:** `[5,5,5,4,4,5,5,5,5,4]`, Σ 47 / 54; `P06-KEY [0,1,1,0,1,1,1,1,0,1]`; equal to the pin | ✓ |
| pre-read emission (for § 4 only) | `9ed1b999…` · `347f8bad…` · `8dc0a193…` | all three reproduce; 28/28 members; tree `6ea92a4e…`; unchanged `4833bcf → 7a97716` | ✓ |

---

## § 1 · THE VERDICT

```
PASS @ coverage 89/89, 28/28 EXACT rows green, TA-X-06 UNGRADEABLE-declared (Q83(b)), dilution 1.024×,
substrate_epoch v3.7.1/48a4c94c…, prereg v1.13
```

**§ G walked in order (`STRUCTURAL → INDETERMINATE → PASS`):**
* `STRUCTURAL`: no EXACT row is RED (0/28).
* `INDETERMINATE`: no EXACT row is UNGRADEABLE (0/28); P-1 … P-5 are GREEN; `TA-X-07(c)`'s (L2) holds on all 25 cells; every arm is C1-conforming; `declared_ungradeable` is exactly `["TA-X-06"]`.
* **`PASS`: all 28 EXACT rows green, none UNGRADEABLE.**

**Counts: GREEN 28 (of which `TA-X-15(b)` and `TA-X-17` are GREEN-BY-CONSTRUCTION, and `TA-X-19` and `TA-X-24`'s negative rest on source reading at the pinned tree) · RED 0 · UNGRADEABLE 0.** No non-GREEN row.

**The attempt is spent and the cap is exhausted** (v1.13 § G.1: attempt 2 of 2 was the last). A PASS needs no further attempt. **Per § G.2 (carried) a PASS is not quotable alone**: the seal still needs H-5 and H-8 (§ 9).

---

## § 2 · PRECONDITIONS, C1, (L2), AND `TA-X-18`'s EMITTER

| id | on this emission | state |
|---|---|---|
| **P-1** | 89/89 mapped, 0 unmapped, `closes`. IMPLEMENTED 65 · DIVERGENCE 8 · RUNTIME-CHOICE 13 · OUT-OF-SCOPE 3; refusals 3 | **GREEN** |
| **P-2** | § B.3a: **(1)** the fold is inserted, forked once through `fork_stream` (`p2_noop`, forked first in `_open_run_streams`, `kc2rt_fight.gd:2777`), invoked **467 times = 467 ticks observed**; **(2)** own-stream draws **measured** 0, shared draws 0; **(3)** one `cell_digest` (zero-draw = absent), plain = with-fold = `3f3bf1f2…`; **(4)** controls (a) `NOT RUN` with its digest perturbed, (a0) `RED`, (b) `RED` (each `digest_identical: false`); (c) RED at `d03ca891` (jack-ryan H-3 INFO-C, the committed probe `kc2rt_attempt2_probes.gd`, a runtime member); **(5)** fresh pack per leg, no fold in the plain leg, and **no probe site in any of the 25 graded cells** (my scan of every cell's `per_site`) | **GREEN** |
| **P-3** | POOL-466, 466, `WEIGHTED:pool_weight` + `UNIFORM:randrange` | **GREEN** |
| **P-4** | 26 `P4_pack` blocks (25 cells + manifest) verified, paired, cross-pinned, 0 mismatches, both digests of record; `runtime_header` as § 0 (binary `5a65c5e1…`) | **GREEN** |
| **P-5** | the eleven settings of v1.12 § B.6; identical in all 25 cells and the manifest | **GREEN** |
| **C1** | five arms' `a8` ROWSETs = § B.1a; `setup` C `207ab21f…`, 0 probe rows; **G3 per cell 25/25**: pass, `injected []`, 0 decision divergences, 0 draw mismatches, no port-only stream, deaths equal, **§ C.9.5a census equal 25/25 and control term equal 25/25 (Σ port 52 = Σ oracle 52)**; `declared_ungradeable` exactly `["TA-X-06"]` | **CONFORMING** |

**Two independent readings in this table, stated.**
* **P-2 control (a).** Its state is `NOT RUN`, not `RED`, because the harness implemented (a) as an own-stream draw **plus** a shared draw, and § B.3a (2) then fires first. § B.3a (4) asks the controls to *"go RED by their own clauses"*. I read that as: the probe must not pass the control, and the control's perturbation must be visible to the digest. Both hold: (a) is non-GREEN **and** its digest differs (`f1dd54b5…` ≠ `3f3bf1f2…`). (a0), the shared-draw-only form, is the clean digest-only test and is `RED`. jack-ryan's pinned rule R2 reads the same way. **Verdict-neutral either way**: (a0) alone carries the digest clause.
* **P-2 control (c)** is not built by the T-A harness. It rests on jack-ryan's run of the committed probe at the same runtime FILE (H-3, collab `ff6ea9fe6`). The task directs that his evaluation of record stands if the operands are unchanged. **They are**: the P-2 block of `ta_manifest.json` is byte-equal between the pre-read and the attempt (§ 4), and the runtime FILE is the same.

**(L2) of `TA-X-07(c)`: jack-ryan's evaluation of record (H-2, collab `ff6ea9fe6`) stands.** Its operands are unchanged:
* each graded cell's `conservation.l2_operands` equals its line in `l2_operands_25cell.jsonl` (`b5bcdb7b…`), **25/25**;
* my own exact-rational evaluation from the graded cells: **25/25 hold, worst β = 3.590829330577844e-14 (`M0|0`), margin ×27.85**, identical to his;
* the harness's `r11_bound`: `all_25_hold` and `probe_bitwise` true.

**`TA-X-18`'s lossless emitter:** `cpython-repr`, round-trip probe true, and `repr(float(s)) == s` for both strings (my check).

---

## § 3 · THE 28 EXACT ROWS (and `TA-X-06`), graded with my grader on per-cell values

| id | observed on the attempt (from the emission unless labelled) | verdict |
|---|---|---|
| `TA-X-01` | `M0` s2 run twice: `e6ee41c6…` == `e6ee41c6…` == the `M0\|2` cell digest; arm+salt ≠ P-2's (`M-POL-2`, 0) | **GREEN** |
| `TA-X-02` | 89/89, 0 unmapped | **GREEN** |
| `TA-X-03` | `M-POL-2-NULL ≡ M0` on 5/5 by `cell_digest`; **independently, the digest's subject read off each cell** (terminal, `state_counts`, board counters and per-wave rows, non-zero per-site draws) is identical on 5/5 | **GREEN** |
| `TA-X-04` | `W1-NULL ≡ M-POL-2` 5/5 (digest and subject) | **GREEN** |
| `TA-X-05` | `M-POL-2 ≢ M0` on 5/5 salts (digest and subject) | **GREEN** |
| `TA-X-07` | (a) max ρ̂ **2.2138e-16** ≤ 1e-12 on 25/25, 21 cells exactly 0.0; (b) max \|residual\| 7.45e-9 (reported); (c) (L2) 25/25, § 2 | **GREEN** |
| `TA-X-08` | § F.2n.2 on **25/25** cells, every term from per-cell counters with D and PRE_FIGHT re-derived from `state_counts`: (1) observed = D + PRE_FIGHT; **(2) restated** `n_channelling + n_released + n_control_suppressed_channelling = D`; **(2p)** `n_ticks_released = n_released + n_released_pre_fight`; `n_channelling` = CHANNELLING + C&M; `M0` emits `n_ticks_released` = `n_released` = 0. **§ F.2o on 25/25:** PRE_FIGHT = waves played, no `DEAD` state, the lethal tick (last `hp_trace` row, HP 0, tick = `run_tick` = observed) censused alive. Table § 3.1 | **GREEN** |
| `TA-X-09` | ROWSET **recomputed by me from `math_rules.json`** by the § A.2 law: `0e826ee0…` = pin = emitted; 9/9 vectors replayed, each `got` = `want` = the pack vector's `out`; rules = the five named | **GREEN** |
| `TA-X-10` | `W1` `max_body_radius_m` 43.0603720647777 on 5/5 ≤ 43.758085029822276; wall armed | **GREEN** |
| `TA-X-11` | clamps (player, body) (0, 0) on 10/10 (`W1` armed; vacuous on `W1-NULL`). *A port with no wall also scores zero* (cl. 6) | **GREEN** |
| `TA-X-12` | pool damage 0.0 on 25/25 | **GREEN** |
| `TA-X-13` | `n_player_crits` 0 on 25/25 | **GREEN** |
| `TA-X-14` | `cause == energy` 0 on 25/25; causes ⊆ {`type_a`, `type_b`}; 0–19 release events per cell (0 on `M0`/`M-POL-2-NULL`) | **GREEN** |
| `TA-X-15` | (a) all 583 (wave, point) rows: p01–p04 release tick 0, p05 tick 49; (b) 0 intra-point staggers, **GREEN-BY-CONSTRUCTION** | **GREEN** |
| `TA-X-16` | § F.2m.3 (a)–(d) at key grain on **25/25**, `W = {151…T}`, T from `terminal`; (a) is checked on **two emitted paths** (`ta_x_16_counters.pool_picks_per_wave` and `board.per_wave[].pool_picks`), (c) on three (the counters, `per_wave` p06-rolled, no point 6 in the TA-X-15 schedule), (d) on two. **Five cells play to w160** (`M0\|0`, `M-POL-2\|1`, `M-POL-2-NULL\|0`, `W1\|1`, `W1-NULL\|1`), so the vector's w157–w160 entries are exercised: Σ 47 there. Table § 3.1 | **GREEN** |
| `TA-X-17` | **by source at the graded tree** (no per-body statistic is emitted): `rho := extents_m * u2` (`kc2rt_laws.gd:280`); both placement sites pass `placement_extents_m` (`kc2rt_board.gd:620`, `:806`); the extents are **read from `arena.json`** (= 8.0, my read of the pack) and the board halts if k3 disagrees (`:492`); `u2` = `_rng.randf()` (`kc2rt_rng.gd:360`). Residual case, disclosed in § 5.2 | **GREEN-BY-CONSTRUCTION** |
| `TA-X-18` | emitted `["-3.999999999999985", "-3.49691120014899e-07"]` → my parse `c00fffffffffffde` · `be9777a5cf72cec6` = expected (sign bit included); emitter lossless (§ 2) | **GREEN** |
| `TA-X-19` | **by source at the graded tree:** the deferred packet is built once (`_land_attack_packet`, `kc2rt_fight.gd:4162`) with keys exactly `{seq, b, rec, direct, pcl, fams, cast, n_rows}`: **no arrival position**. The arrival loop (`_defer_arrivals :4182`) and the landing calls it makes (`_cp_absorb`, `_land`) read no position or distance. Distance is read only at cast, for the latency (`_defer_latency_ticks(_dist_to_player(b), v)`) | **GREEN** |
| `TA-X-20` | r = 3.0 (= `player_kit.channel.radius_m`, my read): 2.99 HIT · 3.01 MISS · 3.0 behind HIT (no angular gate) · 3.0 side HIT · 12 → 12 (no target cap); computed in this run at the graded tree | **GREEN** |
| `TA-X-21` | 12/12 quantisation rows (the ten numeric rows: `got` = `expect` = CPython `round()`, half-to-even); **oracle live sites re-verified by me** at engine `22cd2288`: `threat.py` FILE equals the emitted `4ce434f9…`, and its only `round(` lines are 1561 / 1681 / 1714 / 2052, each `int(round(`, equal to the cited four; **no bare `round(` on the port**: harness scan 0 over 77 files, **my own scan 0** over every `.gd` in the tree outside the quantisation home | **GREEN** |
| `TA-X-22` | `interrupts_channel_flag` cause 0 on 25/25 | **GREEN** |
| `TA-X-24` | `PhaseModel.ENGAGE` DRIVER-OF-RECORD (emitted); negative by source: every `sha256` site on `sim/` + `loader/` read, and none hashes an actor id (pack/register/leech-table digests, the P-2 and MC stream seeds, `kmill.seed_for`'s wave material) | **GREEN** |
| `TA-X-25` | (a) refused 0; (b) three counters sum to `n_bodies_spawned`; (c) against POOL-466 / SWING-456 / NONSWING-10 **recomputed through the oracle**: (1)–(4) hold; all on 25/25 | **GREEN** |
| `TA-X-26` | (a) audit green, 0 unaccounted; (b) loaded bytes `cb6a008b…` = P-i, `agrees`; (c) 7,900 · 790 · 8 tiers `{65,75,83,88,105,115,565,588}` on 25/25 · 5 · 790; (d) 1 helper, 0 disagreements; (e) ARMED-464 mean 0.246896551724137, median 0.25, max 0.35, min 0, 17 immune | **GREEN** |
| `TA-X-27` | (a) 77 files, 0 short-circuits, 0 unclassified. **(b) my own CPython replay** (3.12.0, as the harness's): the 139 pairs re-derived from `waves.json`, `random.Random(seed).randint` per pair, words counted per call. **For each of the 16 seeds, my per-call consumption and results equal the port's emitted `port_consumed` / `port_results`** (4,281 words in total). (c) 29 live sites, p05 elided as the oracle, G3 draw rules at this digest. (d) **139 / 97, recomputed by me** | **GREEN** |
| `TA-X-28` | caps 0/0, `ALL_BODIES_IN_DISC`, 0.57 on 25/25. *A green says one leech law, not that it reproduces Matt's fight* (cl. 10) | **GREEN** |
| `TA-X-29` | (a) `PRED-GMAG-WHOLE` true: 193/154 (344 actors), 527/104. **(b)** emitted composition: 40 compositions equal to the law, dot/PCL take nothing, leech dropped, clamp cross-check 527 rows 0 disagreements, and the emitted `composition_order_read` equals Z5-LAW's `composition_order` in the pack **verbatim**; `c5_equals_z5_in_content` read as the **dict** it is (`unchanged` true, `differ` [], `added` [`⚑ C-11a_annotations`]) and **checked by me against the pack**: every Z5-LAW `value` key is in C5-Z5-LAW with equal content, the only addition is `⚑ C-11a_annotations`, `v3p6_points_to.Z5-LAW` = RESTATEMENT. **(c)** port `M_inst` = the pack's `z3_wave_damage_modifier_check` on all 10 waves (1.82 ×5, 1.83 ×5; my read of `monster_offense.json`). **(d)** 29 inert, identity path on all, "unexercised: 0 of 29", 0 in POOL-466. **(e)** 3.207764 / 4.980316; 16 + 23 per-record ratios, max \|Δ\| 0.0 | **GREEN** |
| `TA-X-30` | (a) `d_engage_m` 2.4 from `arena.json`, NaN and zero rejected; (b) 0 halted beyond, 25/25 | **GREEN** |
| `TA-X-06` | `W1 ≢ M-POL-2` on 3/5 salts (1, 3, 4); identical on 0 and 2. **`UNGRADEABLE-declared (Q83(b), KP-110)`**, no colour, no antecedent | declared |

`TA-X-23` is struck and retired.

### 3.1 · `TA-X-08` and `TA-X-16` per cell (the attempt; identical on the pre-read)

| cell | T | waves | picks / Σ expected | p06 keys filtered (= `P06-KEY` prefix) | observed | PF | D | `n_chan` | `n_rel` | `n_csc` | `n_ticks_released` | id (1)(2)(2p) · § F.2o |
|---|---:|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| M0\|0 | 160 | 10 | 47 / 47 | `[0,1,1,0,1,1,1,1,0,1]` | 2013 | 10 | 2003 | 2003 | 0 | 0 | 0 | ✓ |
| M0\|1 | 154 | 4 | 19 / 19 | `[0,1,1,0]` | 677 | 4 | 673 | 673 | 0 | 0 | 0 | ✓ |
| M0\|2 | 154 | 4 | 19 / 19 | `[0,1,1,0]` | 652 | 4 | 648 | 648 | 0 | 0 | 0 | ✓ |
| M0\|3 | 154 | 4 | 19 / 19 | `[0,1,1,0]` | 619 | 4 | 615 | 615 | 0 | 0 | 0 | ✓ |
| M0\|4 | 153 | 3 | 15 / 15 | `[0,1,1]` | 472 | 3 | 469 | 469 | 0 | 0 | 0 | ✓ |
| M-POL-2\|0 | 153 | 3 | 15 / 15 | `[0,1,1]` | 467 | 3 | 464 | 402 | 62 | 0 | 62 | ✓ |
| M-POL-2\|1 | 160 | 10 | 47 / 47 | full | 1962 | 10 | 1952 | 1729 | 223 | 0 | 223 | ✓ |
| M-POL-2\|2 | 154 | 4 | 19 / 19 | `[0,1,1,0]` | 671 | 4 | 667 | 589 | 78 | 0 | 78 | ✓ |
| M-POL-2\|3 | 154 | 4 | 19 / 19 | `[0,1,1,0]` | 621 | 4 | 617 | 553 | 64 | 0 | 64 | ✓ |
| M-POL-2\|4 | 153 | 3 | 15 / 15 | `[0,1,1]` | 472 | 3 | 469 | 407 | 62 | 0 | 62 | ✓ |
| M-POL-2-NULL\|0…4 | = M0\|0…4 | | | | | | | | | | | ✓ |
| W1\|0 | 153 | 3 | 15 / 15 | `[0,1,1]` | 467 | 3 | 464 | 402 | 62 | 0 | 62 | ✓ |
| W1\|1 | 160 | 10 | 47 / 47 | full | 1986 | 10 | 1976 | 1753 | 223 | 0 | 223 | ✓ |
| W1\|2 | 154 | 4 | 19 / 19 | `[0,1,1,0]` | 671 | 4 | 667 | 589 | 78 | 0 | 78 | ✓ |
| W1\|3 | 154 | 4 | 19 / 19 | `[0,1,1,0]` | 621 | 4 | 617 | 553 | 64 | 0 | 64 | ✓ |
| W1\|4 | 153 | 3 | 15 / 15 | `[0,1,1]` | 483 | 3 | 480 | 418 | 62 | 0 | 62 | ✓ |
| W1-NULL\|0…4 | = M-POL-2\|0…4 | | | | | | | | | | | ✓ |

`n_released_pre_fight` = 0 and `n_spawn_point_6_keys_rolled` = 0 (per wave too) on every cell. The harness's own `holds` / `id*_holds` flags agree with my arithmetic on 25/25. **They were not used to grade**: they are emitted arithmetic, and the colour is mine.

**States the oracle reference never reaches, checked first (v1.13 H-6 WARN-1 / KP-185 rule 1):** w157–w160 are played on 5 cells, and every one of them **dies at w160** (`death`, no clear). No cell clears. No PRE_FIGHT tick is released. No tick is doubly suppressed. **No row is graded on a state that makes it ill-posed.**

---

## § 4 · § G.1a ITEM 5: THE GRADED EMISSION AGAINST THE READ'S

The same `grade()` (§ Z) was run on both emissions.

| face | attempt (`7a97716`) vs pre-read (`4833bcf`) |
|---|---|
| `cell.json` FILE bytes | **25/25 byte-identical** |
| per-cell `cell_digest` (the manifest's 25) | **25/25 equal** |
| row verdicts (P-1 … P-5, C1, 28 EXACT, `TA-X-06`) | **35/35 equal** |
| **every row value my grader reads** (the full `values` object per row, compared as canonical JSON) | **35/35 equal** |
| `ta_verdict.ta_x_08`, `ta_x_16`, `r11_bound`, `g3` blocks | equal (all four) |
| **the printed difference** | **EMPTY.** No row value, no cell and no digest differs |

**Why the two `ta_manifest` / `ta_verdict` FILE digests differ anyway (`9e35fb2e` vs `347f8bad`; `f7e19dc1` vs `8dc0a193`).** By leaf-path diff of the parsed JSON:
* **`ta_manifest.json`: exactly two leaves differ**, `runtime_header.header_file` and `runtime_header.header_file_sha256`.
  * The header file is the telemetry the exported `.app` writes when the harness runs it to read its header. It is named by the run's unix time (`kc2play-1790883965-…` vs `kc2play-1790886070-…`).
  * Its content differs because that `.app` session seeds itself from the same clock (`run_id`, `seed`, `written_at_unix`) and logs the spawns that seed drives. I diffed the two files: 19 records each, 52 leaves differ, all of them `run_id` / `seed` / `written_at_unix` and the seed-driven spawn rows (`record_path`, `x_m`, `y_m`, one `spawn_point_id`).
  * **Every header field P-4 reads is equal**: pack digests, cross-pin, vendored runtime digest, `equals_P4`.
* **`ta_verdict.json`: 13 leaves differ, all run identity or that cascade.** They are:
  * `run_kind`;
  * `attempt`, `attempt_overall`, `attempt_previewed`;
  * the `pre_attempt_read` block: the attempt carries `finding`, `finding_sha256`, `rows_green`/`ungradeable` (null) and a note, where the pre-read carried a `state` line;
  * the same two `runtime_header` leaves;
  * `ta_manifest_sha256`, which follows from the manifest's own change.
* `harness_stdout.txt` differs in 3 of 3,089 lines: the `run_kind` banner, the attempt label, and the `ta_manifest` prefix.

**So the expectation holds: run identity and timestamps only.** One refinement: the clock also seeds the `.app`'s own demo spawn log inside the header file. That log is neither a graded value nor a field P-4 reads.

---

## § 5 · RECONCILIATION WITH jack-ryan's H-7 READ, ROW BY ROW

| rows | my grade (attempt) | H-7 read (pre-read, grader r2) | agree |
|---|---|---|---|
| P-1 … P-5 | GREEN ×5 | GREEN ×5 | ✓ 5/5 |
| C1 | CONFORMING | CONFORMING | ✓ |
| `TA-X-01` … `05`, `07` … `16`, `18` … `22`, `24` … `30` (26 rows) | GREEN | GREEN | ✓ 26/26 |
| `TA-X-17` | GREEN-BY-CONSTRUCTION | GREEN-BY-CONSTRUCTION | ✓ |
| `TA-X-29` | GREEN | GREEN (r2; pinned grader: RED on (b)) | ✓ |
| **all** | **28/28 GREEN · P GREEN · C1** | **28/28 GREEN · P GREEN · C1** | **✓ 34/34. No row where my reading differs from his** |

His read was of the pre-read emission. By § 4, that emission's cells and every row value I read are identical to the attempt's, so the read and this grade were taken on equal operands.

### 5.1 · His two grader corrections, scrutinised independently

**`TA-X-29` clause (b): I concur, and on wider grounds than his.**
* The emitted `c5_equals_z5_in_content` is a dict, `{unchanged: true, differ: [], added: ["⚑ C-11a_annotations"]}`. Testing it `is True` is a type error in the grader, not a reading of the row.
* I did not rely on the emitted dict. From `math_rules.json` I checked:
  * every Z5-LAW `value` key appears in C5-Z5-LAW with **equal** content;
  * the only added key is `⚑ C-11a_annotations`;
  * the pack itself declares C5-Z5-LAW a RESTATEMENT (`v3p6_points_to`).
* I also checked one thing his read did not print: the emitted `composition_order_read` equals Z5-LAW's `composition_order` **verbatim**. That is v1.8 § F.2h (b)'s *"Z5-LAW verbatim"* checked as a text equality, not only through the 40 sampled compositions.
* The correction moved no criterion. The criterion is checked against the **pack**, not the port.

**`TA-X-17`: I concur with the GREEN-BY-CONSTRUCTION class and add one precision.**
* His correction is right. The port does not type 8.0. It reads `arena.json placement_extents_m` (= 8.0, which I read from the pack) and halts on a k3 disagreement (`kc2rt_board.gd:492`). A grep for a typed 8.0 tests where the constant lives, not the law.
* **The precision (his H-3 INFO-B, which corrects my attempt-1 wording):** the port's `u2` is Godot's `randf()`, documented as **inclusive** of 1.0, not `[0, 1)` as my attempt-1 grade wrote.
* The construction still bounds ρ **exactly**: `extents_m` = 8.0 is a power of two, so `ρ = 8·u2` is exact, and `u2 ≤ 1` gives `ρ ≤ 8.0`.
* ‖offset‖ = ‖(ρ cos θ, ρ sin θ)‖ can exceed ρ only by a few ulps. The subtraction `spawn − anchor` adds at most an ulp of the anchor's magnitude (~7e-15 m at 40 m). So **the row can fail only if `u2` lies within ~1e-15 of 1.0**. Godot documents `randf()` as inclusive of exactly 1.0, and jack-ryan (H-3 INFO-B) estimates that value at about 3e-8 per draw.
* **That one case is not closed by construction.** On this realisation it is closed by measurement: jack-ryan's instrumented replica (H-7 Item 4) found max ‖offset‖ = 7.95483 m and no `u2 ≥ 1.0` over every scatter draw of the run. It reproduced the pre-read's 25 cells content-equal, and § 4 shows those are byte-identical to the attempt's. So it measured the same draws.
* **I label that measurement supplementary.** It is not in the hash-pinned emission. The class stays GREEN-BY-CONSTRUCTION with this residual disclosed, as INFO-2 of his read already recommends: an emitted per-body maximum would close it on a later runtime. It cannot be added now without moving the digest.

### 5.2 · My own instrument, disclosed

This grader was not pinned before the emission was opened. jack-ryan's was, which is the stronger discipline. So every change to it after its first run is printed here. **None moved an expected value, a tolerance or a criterion.**

1. **Run 1 crashed on `TA-X-21`.** Two of the twelve quantisation rows are site-law assertions (`CEIL`, `TRUNCATE`) with no `in`/`got` fields. I had assumed all twelve were numeric. Fixed to check the ten numeric rows against CPython `round()` and to carry the two assertion rows as emitted. This is a field-handling fix.
2. **Run 2 printed `TA-X-19` UNGRADEABLE.** My source read searched for the packet literal only inside `_defer_arrivals`, but the packet is **built** in `_land_attack_packet` and only **consumed** in `_defer_arrivals`. I widened the read to the build site, the arrival loop and the landing calls.
   * The criterion is unchanged: *no arrival position in the packet, no position read on arrival*.
   * **It is the same class of defect as his `TA-X-17` print**: a grep scoped to the wrong place. A source-read row is only as good as the reader's map of the source. INFO-2 of his read (emit a counter for `TA-X-17`/`19`) is the right long-run fix.
3. I added two checks that can only make a GREEN harder, never easier:
   * `TA-X-29(b)`'s verbatim composition-order equality;
   * the § F.3 dilution figure for the PASS line.

---

## § 6 · REPORT FACE

### 6.1 · § F.5 rule 13: the control-term sentence (mandatory under v1.13)

> *"`TA-X-08` identity 2 carries `n_control_suppressed_channelling`. On this run it was **0** (max **0** on one cell); in G3 it was **52** and equal to the oracle's on every cell. A GREEN `TA-X-08` on a run where the term is 0 everywhere has not tested the control path; G3 has."*

**Disclosure (jack-ryan H-6 INFO-6; v1.13 § F.2n.5), from this emission and the KP-184 G3 summaries:**
* On this run, **every** control-suppression counter is 0 on all 25 cells: `n_control_suppressed` Σ 0, doubly suppressed (`n_control_suppressed_released`) Σ 0, PRE_FIGHT-suppressed Σ 0, released PRE_FIGHT Σ 0.
* In G3, the control-suppressed-channelling branch is exercised (Σ 52, port = oracle on 25/25). **The doubly-suppressed and PRE_FIGHT-suppressed branches are 0 on both sides of G3 too** (port Σ 0 / oracle Σ 0).
* Every `ta_x_08_counters` block equals the oracle's in 25/25 G3 summaries.
* So the restated identity's **new term** is tested (in G3). **Its two booking sub-choices (a doubly-suppressed tick counted as released; `n_released` on D) are tested nowhere.** As v1.13 § F.2n.3 states, they are fixed by the oracle's code, not by an outcome.

### 6.2 · § F.5 cl. 11 (the port≠oracle holes), with the v1.13 label (H-3 INFO-A)

> *"Port≠oracle holes 1–17 (PCL dropped · death after heal · damage rows unreachable · `tree_attack` slots never chosen · dying slots mishandled, and 5b one dying slot per death · slot chance/cooldown/delay never read · the wrong march base · to-hit · mitigation order · DoT timeline · monster crit tier · motion order and the contact fold · Soulfire and the bleed rider · monster pets · the resist cap · attack speed and OA adds · the HI life block), the chance-gate boundary, the C-11a grant law, the loop-layer defects of KP-144, the pack-closure defect of KP-147, and the closure-law defects of KP-150 / KP-152 (run state carried as input · arms defined only in prose · read-absent columns · constants on untaken branches) are invisible to every EXACT row in this instrument. A **v1.13** PASS is not quotable without jack-ryan's hole-closure finding at the same runtime digest, and the seal is blocked on any non-zero R-6 invariant."*

The harness's emitted `port_holes_sentence` still carries the **v1.12** label. The sentence above, with **v1.13**, is the report face of record.

**R-6 (my count from the cells; equal to the harness's):** (i) cells with `killer_id` set and `terminal_reason == cleared`: **0** · (ii) in-tick resurrections: **0** · (iii) cells where a PCL row landed and `PercentCurrentLife` intake is not > 0: **0**. **No R-6 invariant is non-zero.**

### 6.3 · § F.5 cl. 7 (sustain), version label only

> *"`leech` and `intake` still have no oracle side in the seals (`C-e`). Off-seal, the v1.13 oracle (the same object as v1.8's, v1.9's, v1.10's, v1.11's and v1.12's; the C-11a corrections folded) KILLS THE PLAYER AT WAVES 152–156 on salts 0–4, and lands ×3.17 the referent's intake over waves 151–159 on the landed grain. The port's own figure is printed from this run and not asserted here. A GREEN T-A IS COMPATIBLE WITH ANY RELATION BETWEEN EITHER REPLICA AND THE REFERENT."*

---

## § 7 · DIAGNOSTICS (§ F.3): reported, gating nothing (F5). Every width VOID

**CLASS V · `TA-B-01`, verbatim (version label only):** *"`BAND / NON-DECISIVE / REPORT-ONLY`. A terminal wave inside or outside this band is not evidence of fidelity either way. It is read from the port's `M-POL-2` arm. The oracle's sealed `M-POL-2` arm terminates at `[156, 152, 151, 151, 156]`, `player_death` on every salt. The v1.13 oracle's `M-POL-2` arm (the same object as v1.8's, v1.9's, v1.10's, v1.11's and v1.12's: the 338 armed, the winner surface armed, the C-11a corrections folded) terminates at `[156, 152, 155, 152, 152]`, `player_death` on every salt, and no salt reaches wave 160. A port that clears to wave 160 has not survived a hard board; it has failed to be in one."*

Every row below prints `@ coverage 89/89` · width `VOID @ re-base` · n = 5 per arm.

| diagnostic | value |
|---|---|
| `TA-B-01` port `M-POL-2` terminal waves | **`[153, 160, 154, 154, 153]`**, `death` on 5/5. Salt 1 plays into w160 and **dies there** (no clear) |
| beside `TA-X-06` (not `TA-B-01`) | port `W1` `[153, 160, 154, 154, 153]` · oracle `W1` `[156, 152, 155, 152, 155]` |
| all arms | `M0` ≡ `M-POL-2-NULL` `[160, 154, 154, 154, 153]` · `M-POL-2` ≡ `W1-NULL` `[153, 160, 154, 154, 153]` · `W1` same terminals |
| `TA-B-19` ticks/wave (D / waves played), `M-POL-2` | `[154.67, 195.20, 166.75, 154.25, 156.33]`, mean **165.44** against the seal's 161.6 → **dilution 1.024×** (v1.7 attempt 1 read 2.431×: the port now dies on the oracle's scale) |
| `TA-B-02` uptime | `[0.8664, 0.8858, 0.8831, 0.8963, 0.8678]` / mean 0.8799. The dead-tick numerator bias attempt 1 flagged is gone with the § F.2o census |
| `TA-B-07` release duty | mean 0.1201. *"`TA-B-02` and `TA-B-07` are ONE ROW WITH A SIGN FLIP (`released/D ≡ 1 − uptime`, exactly). They are not two pieces of evidence."* |
| `TA-B-03` frac moving · `TA-B-04` / `TA-B-05` P(chan \| moving / stationary) | 0.8442 · 0.9143 / 0.6930 |
| `TA-B-06` plant ratio · `TA-B-09` channel split | 0.1850 · 0.1227 |
| `TA-B-08` ordering | holds 5/5 |
| `TA-B-14` `W1` vetoes / occupancy | `[0, 3, 0, 1, 1]` / `[0, 0, 0, 0, 0]` |
| `TA-B-15` NO-DATA bodies | 0 on every cell |
| sustain leech / intake (printed, not asserted) | `M-POL-2` `[2.03, 5.56, 2.62, 2.88, 2.08]` |

**§ F.3a still applies:** the port's generator and the oracle's draws are different realisations, so the per-salt comparison above carries no fidelity information (`C-p`).

---

## § 8 · THE HONEST `n` (§ C.8)

**The 25 cells carry 13 distinct outcomes:**
* `{M0, M-POL-2-NULL}` are byte-identical per salt (5);
* `{M-POL-2, W1-NULL}` are byte-identical per salt (5);
* `W1` differs from `M-POL-2` on salts 1, 3 and 4 (3 more).

Every "25/25" above is **13/13 distinct outcomes**, and every diagnostic is n = 5 for one arm. **The emission is one realisation.** The pre-read reproduced it byte for byte, and so did jack-ryan's replica. That proves determinism, not independent replication.

---

## § 9 · WHAT THE VERDICT MEANS, AND WHAT IT UNLOCKS

**`PASS` under prereg v1.13, attempt 2 of 2 (overall 3), at runtime FILE `d03ca8913901d61de73db40287e31e498e8b2714521f8221fde414682e328ccd`.**

* **The runtime `d03ca891` is the REFERENT-v1 CANDIDATE.** Under the carried § G.2 / R-9 (Q87's seal), it is **not sealed and not quotable alone**. The seal requires, at this **same** digest:
  1. `PASS` (28/28) — **met**;
  2. coverage 89/89 — **met**;
  3. T-B reported DIAGNOSTIC — **met**, § 7;
  4. R-6 all zero — **met**, § 6.2;
  5. **H-5: jack-ryan's hole-closure finding GREEN at `d03ca891`** — **owed** (seal-blocking, not verdict-blocking);
  6. **H-8: Matt's T-C yes on `d03ca891`** — **owed**.
* **The graded-run cap is exhausted.** No attempt remains under v1.13, and a PASS needs none. **Any change to the runtime moves the digest off the graded object**, and with it what this PASS attests to. A port repair from here, e.g. INFO-2's emitted counters for `TA-X-17`/`19`, is a new referent question for Matt, not a re-grade.
* **What the PASS does not say** (cl. 10, cl. 11, F5): it does not say the port reproduces Matt's fight. It does not close holes 1–17 or the KP-144/147/150/152 defects. It does not test the doubly-suppressed booking (§ 6.1). It does not certify `TA-X-17` beyond construction plus one measured realisation (§ 5.1).
* **Not triggered:** the J-P1 failure branch / HALT to Matt. No row is RED, none is UNGRADEABLE, no row is ill-posed on a port-only state, and no row changed after the read.

**Next (conductor):** record KP-189 (PASS, grade of record); jack-ryan Gate-2 of this grade + **H-5** at `d03ca891`; then **H-8** to Matt.

---

## § Z · Reproduce

```
python3 agentic_orchestration/gamora/analyses/2026-10-01-kc2-play-ta-attempt2-v1.13-grade/grade_attempt2_v1p13.py
# reads godot 7a97716 (attempt) and 4833bcf (pre-read) through git; the engine pack and oracle (22cd2288) read-only.
# writes results.json (edbb9809…) and ta_verdict_v1p13_attempt2.json (521e3fea…); stdout = run_stdout.txt (3e0cb27e…)
```

*Filed 2026-10-01 by **gamora**. **Verdict `PASS`; v1.13 attempt 2 of 2 spent; the cap is exhausted; the runtime `d03ca891` is the REFERENT-v1 candidate, with H-5 and H-8 owed for the seal.***
