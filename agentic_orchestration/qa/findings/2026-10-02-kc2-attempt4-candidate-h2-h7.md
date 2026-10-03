# Finding — 2026-10-02 — Run KC2-PLAY · H-2 + H-7 at the attempt-4 candidate `fd799b63`

**Reviewer:** jack-ryan (DEV-MODE; H-2 and H-7 seat per v1.14 § H). **The pre-read is a gate document. It is not a verdict of record and it is not the attempt.**
**Severity:** **BLOCK** (H-7). H-2 is **PASS**.
**Target:** runtime tree FILE **`fd799b635734904a2f477795526a20c1bbce93b683cc9b8063e865e413804813`** (MANIFEST at godot `96fc0cc`; main at `ef5c04a`). Native lib `74360ffa…` (`kc2rt_contact_native/3`).
**Developer:** drax (port, harness) · gandalf (conductor) · gamora (grades the attempt)
**Prereg set of record:** v1.14 FILE `5bbe7ae5…`, v1.15 FILE `d1c4a75a…`, v1.15 notes FILE `7797ff17…`. All three re-hashed equal.
**Principles applied:** REVIEW_PROCESS #1, #4, #5. Disciplines #10, #11, #12. ADR-002. v1.14 § G.1a (Matt Q96.3) + KP-185 routing; KP-137.

## Verdicts

| item | verdict | one line |
|---|---|---|
| **H-2** · (L2) of `TA-X-07(c)` | **PASS** | (L2) holds **25/25** (exact rationals). Worst β = **5.3644e-14** at `W1\|4`. Margin ×**18.64** (v1.13: ×27.85). Census unchanged in content, verified independently. |
| **H-7** · the 28-row § G.1a read | **BLOCK** | **27 GREEN · 1 RED (`TA-X-25`) · 0 UNGRADEABLE.** P-1…P-5 GREEN, C1 CONFORMING. The emission would take **`STRUCTURAL`**. |
| **Ruling** | **ATTEMPT 1 of 2 (overall 4) DOES NOT FIRE at `fd799b63`.** | The RED is a **port emission defect** (a stale classification label in the runtime tree), routed to drax. It is **not** a prereg defect, so there is **no HALT to Matt**. The read consumed nothing. |

**Read-only attestation:**
- Godot was read through `git archive ef5c04a` into my scratch, and every Godot run was there, under the heavy lock. Nothing in `reincarnated-godot` was edited, staged or run against.
- **One disclosure (INFO-8):** at 00:00 I ran `kc2_runtime/tools/make_manifest.py --help` in the real repo, believing it would print usage. The script ignores arguments and rewrote `kc2_runtime/MANIFEST.json`. The result was **byte-identical** (sha `dc0e87d8…` before and after = `HEAD`'s blob), and `git status` is clean. It also served as a by-hand recomputation of `fd799b63`.
- The engine was used read-only. `referent_lineup.py`, `threat.py`, `spawn_structure.py` and `player_kit_residual.py` are equal at HEAD `102c28e0` and at `969fbd8d`.

---

## 1 · H-2 · (L2) of `TA-X-07(c)` at the attempt digest

**The clause:** v1.12 § F.2k.3 (L2), carried by v1.13 and v1.14 (§ F "F.2k (L2) carried by reference"). v1.14 § L.4 re-opens the *margin*, not the law: the cells are ≈ 4× longer, so v1.13's basis does not carry.

The four antecedents, each evaluated at `fd799b63` with my own code (`grader_h7-r2.py :: l2_cell`, `census_verify`; exact `Fraction` arithmetic, u = 2⁻⁵³):

| (L2) item | result |
|---|---|
| 1 · every `B⁺` operand emitted losslessly | **25/25.** `n_k` / `Â_k` / `q_k` ×7, `N_I` / `Â_I` ×2, `final_sum_n_terms = 6`, `sink_terms_present = 6`, `Ô`. Every float is a CPython-repr round-trip string. |
| 2 · booking census filed at the graded digest, every site classed, φ from it | **GREEN.** My independent Python re-check of `kc2rt_booking_census.gd` (FILE `0b8705b1…`) against the candidate `kc2rt_fight.gd`: **47 rows, 35 sites, 35 call sites found, 0 uncensused, 0 stale, T 22 / S 11 / F 14**, all flags consistent. The row content is **identical to `d03ca891`'s census** with line numbers stripped (rows and PATHS hashes equal), so it is line-relocated only. φ = γ_{2·f_max}, f_max = max(R+4, 2N, 2K+3) from each cell's `census_counters`. |
| 3 · every `n·u < 1` | **25/25** (largest accumulator count < 10⁵). |
| 4 · β ≤ 1e-12 | **25/25.** |

**The re-evaluated operands** (v1.13's figures in brackets):

| measure | at `fd799b63` | [v1.13, `d03ca891`] |
|---|---|---|
| `n_offered` per cell | 8,654 – 15,238; Σ **309,829** | [953 – 6,777; Σ 58,738] → **×5.3** |
| all-accumulator terms per cell | 51,889 – 96,779 | — |
| f_max | 100 (3 cells) · 160 (9) · **240 (13)**; `dot_buckets_max` up to 120 | [100 – 160] |
| Λ (first-order) max | **483.18** | [323.43] |
| β max (exact decision) | **5.3644e-14** (`W1\|4`) | [3.5908e-14] |
| margin 1e-12/β min | **×18.64** | [×27.85] |
| ρ̂ (clause (a)) max | 2.2115e-16 (two cells; 0.0 on 23) | [2.2138e-16] |

**What moved the margin is φ, not depth.** 13 cells reach `dot_buckets_max` = 120, so f_max = 240 and φ is ×1.5 of v1.13's. Depth enters only through γ² and stays negligible, as § F.2k.5 says it would. The harness's own `r11_bound` agrees with mine on every cell, and `neumaier_probe_bitwise` is `true` at this tree.

**(N1)–(N8) re-verified at the graded digest:**
- `_offer` / `_cons_add` / `_neu` (`kc2rt_fight.gd`) and `conservation_residual` (`kc2rt_laws.gd`) are **byte-identical to `0f36826` (d03ca891)** (function bodies diffed).
- So the Neumaier step, Σ|term|, the split counting and the six-way final sum are those the law was derived against.

**H-2: PASS.** INFO-6 (§ 4) records a scope note on v1.14 § L.4 that changes nothing here.

---

## 2 · H-7 · the 28-row pre-attempt read

### 2.1 · The freeze and the emission

- **Grader pinned before the emission was opened:** `grader_h7.py`, FILE `8efa88e3649909b8f021f5205800d807fea65ca2b6ef27c5e11c2f5ae679ca8a`, committed alone at collab **`15cad3371`**.
  - It was written from v1.14 + v1.15 + notes and the harness **source** at `ef5c04a`.
  - Its decision rules R1–R8 are in its docstring.
- **The emission (§ G.1a item 2):** no drax pre-read emission existed at this digest, so I ran drax's committed H-4 harness (`kc2rt_ta.gd`) myself on a scratch `git archive ef5c04a`:
  - with `run_kind=pre_read expect_runtime=fd799b63… g3=<the KP-261 G3 summaries>`;
  - boot check OK; H-4 green against v1.15 / v1.14 / notes, with every § B.1a ROWSET equal;
  - G3 all 25 pass (native shadow mismatches 0, library `74360ffa…`);
  - the runtime digest is unchanged through the run;
  - the verdict file says `run_kind: pre_read`, `attempt: "PRE-READ — NOT A GRADED RUN (§ G.1a)…"`, `verdict: null`.
  - **The only emission failure is `runtime_header`**: there is no `.app` in scratch (see WARN-2).
  - The emission is filed at `…-h2-h7/PRE-READ-NOT-A-GRADED-RUN-emission/emission.tar.gz`: tree digest `35570acd…`, `ta_manifest.json` `4aa125d0…`, `ta_verdict.json` `34636d6d…`.
- **P-2 control (c):** I ran the committed probe `kc2rt_attempt2_probes.gd` at the same tree. *"ok ⚑ NEGATIVE CONTROL REDS AS REQUIRED — (c) the attempt-1 digest law"*; 16/16 controls RED. Its other 5 failures are the declared reds KP-272 names (three v1.13-era population probes, plus the two `.app` checks).

### 2.2 · The read (grader r2; the r2 change is § 3 WARN-1)

| row | read | operands |
|---|---|---|
| **P-1** | GREEN | 89/89 (IMPL 65 · DIV 8 · RC 13 · OOS 3) |
| **P-2** | GREEN | § B.3a (1)–(5); fold 4,706 invocations = 4,706 ticks; own-stream 0; controls (a)/(a0)/(b) not GREEN; (c) RED at this tree |
| **P-3** | GREEN | POOL-466, 466, WEIGHTED/UNIFORM (the incumbent roll, § L.2) |
| **P-4** | GREEN | 26 P4 blocks; packs re-derived from disk: model `99711727…`, reference `af58ef40…`, cross-pin equal. *`runtime_header` printed separately: WARN-2* |
| **P-5** | GREEN | settings (2)–(11) by value; fold list read off `a8` (H-4 green) |
| **C1** | CONFORMING | 5 arms' ROWSETs = v1.14 § B.1a; G3 25/25 incl. census, control term (Σ 80 = oracle's), death equal, native shadow 0; declared = `["TA-X-06"]` |
| `TA-X-01` | GREEN | M0 s2 twice, identical, = the graded M0\|2 digest |
| `TA-X-02` | GREEN | = P-1 (§ L.1 caveat printed) |
| `TA-X-03` | GREEN | M-POL-2-NULL ≡ M0, 5/5 |
| `TA-X-04` | GREEN | W1-NULL ≡ M-POL-2, 5/5 |
| `TA-X-05` | GREEN | M-POL-2 ≢ M0, 0/5 identical |
| `TA-X-07` | GREEN | (a) max ρ̂ 2.2115e-16; (c) (L2) 25/25 (§ 1) |
| `TA-X-08` | GREEN | id (1), (2) restated, (2p), § F.2o convention: 25/25; M0 `n_ticks_released` 0 |
| `TA-X-09` | GREEN | 9/9; ROWSET `0e826ee0…`; `math_rules` = pack file `af2b0c52…` |
| `TA-X-10` | GREEN | W1 armed; max body 43.0183 / 43.0445 / 43.0445 / 43.0445 / 43.0707 ≤ **43.71638147965161**; max spawn 43.2541 |
| `TA-X-11` | GREEN | (0,0) on 10/10 W1 + W1-NULL ("never needed to clamp", § F.5 cl. 6) |
| `TA-X-12` | GREEN | 0.0 on 25/25 (structural; INFO-3) |
| `TA-X-13` | GREEN | 0 crit rows of `source == player`; player rows 9,035 – 16,458 per cell (non-vacuous); notes § 1 scope. Structural, INFO-3 |
| `TA-X-14` | GREEN | cause==energy 0; causes ⊆ {type_a, type_b} |
| `TA-X-15` | GREEN | p01–p04 tick 0, p05 tick 49 on every (wave, point), 169 p05 rows |
| `TA-X-16` | GREEN | § F.2m′ (a)–(d) at key grain, 25/25. LU-KEYS / P06-KEY re-derived from `waves.json` and `referent_lineup.REFERENT_LINEUP`: equal |
| `TA-X-17` | GREEN | **emitted** max ‖spawn − anchor‖ 7.95483 ≤ 8.0; anchor = v3.8 GD `emitter_xy` (sg1 off sg4) on 25/25 |
| `TA-X-18` | GREEN | lossless; bits `c00fffffffffffde` / `be9777a5cf72cec6` |
| `TA-X-19` | GREEN-BY-CONSTRUCTION | `_defer_arrivals` (`kc2rt_fight.gd:4559`); packet carries no position |
| `TA-X-20` | GREEN | 2.99 HIT · 3.01 MISS · behind HIT · side HIT · 12 → 12 |
| `TA-X-21` | GREEN | 12/12 quantisation; **the notes § 2 list: 14/14 live sites cited**, plus 3 dead; 0 bare `round(` over 90 files |
| `TA-X-22` | GREEN | flag cause 0 |
| `TA-X-24` | GREEN | `PhaseModel.ENGAGE` |
| **`TA-X-25`** | **RED** | **set digests GREEN** (SWING = POOL-466 `33c886a1…`, NONSWING = ∅ `e3b0c442…`, `n_nonswing` 0). **Clause (c)(2) fails on 25/25:** 12–14 bodies per cell of 5 records are emitted `measured_inert` (§ 3 BLOCK-1) |
| `TA-X-26` | GREEN | (c) 5/790/7900/8/790; (e) 0.2468965517 / 0.25 / 0.35 / 0, 17 zero, n 464; P-i `cb6a008b…` |
| `TA-X-27` | GREEN | (a) 0/0; (b) 16 seeds equal; (c) registry **41 = 29 V9 + 12 rg1** (V311-RG-019 not live) and G3 draw rules 25/25; (d) 139/97 |
| `TA-X-28` | GREEN | caps 0/0, ALL_BODIES_IN_DISC, 0.57 |
| `TA-X-29` | GREEN | (a) 193/154, 527/104, 344. **(b′) summed by me over 25 per-cell blocks:** constants exact (`CompositionFold`, LO, −0.44, divisor `true`, lapm 160); families `n = n_equal`: instant_nonphys 66,766 · phys_clamped 2,453 · phys_clamped_unmapped 2,121 · phys_unclamped 21,209 · dot 14,958 · dot_leech_type 162 · **dot_chaos_aether 0**; pcl untouched. (c) z3 10/10; (d) 29 inert; (e) **3.197066 / 4.935649**, 16 + 23 records, max dev 0.0 |
| `TA-X-30` | GREEN | § F.2i′.2 GREEN rule on 25/25: roster steps 814,944, held 55,994 (all zero), clipped 0; pet steps 666,392; 0 halt/position/NaN/reach/op mismatches; (b′) 0 beyond; ring_halt_m 2.4 and NaN test |
| *`TA-X-06`* | *UNGRADEABLE-declared* | *W1 vs M-POL-2 identical 2/5* |

**Counts: 27 GREEN · 1 RED · 0 UNGRADEABLE. § G verdict this emission would take: `STRUCTURAL` (on `TA-X-25`).**

### 2.3 · Face-printing requirements (notes § 3), as they read on this emission

1. **`TA-X-30(b′)` vacuity.** `n_clamp_stops == 0` on **25/25**: *"(b′) vacuous: no clamp stopped a body"*. On W1, clamp calls were 32,425 / 38,259 / 36,545 / 26,860 / 33,079 and stops 0. On the 20 unwalled cells, calls were 0.
2. **Trajectories.** The **port's realisation** has *25 cells / **13** distinct trajectories (4 clear, 9 die)*; the **reference** has *25 / 12 (9 clear, 3 die)*. The classes are `M0 ≡ M-POL-2-NULL` and `M-POL-2 ≡ W1-NULL` on every salt; `W1` coincides with `M-POL-2` on salts 2 and 3 and departs on 0, 1 and 4. **Not draw-comparable** (§ C.7; the graded run is on the port's own generator). The face must label which figure is which (INFO-5).
3. **UNEXERCISED-ON-REFERENT.** The non-waypoint Pursue operand had **0** port steps; the non-penetration clip had **0** port steps.
4. **Clip flag:** none (0 clipped steps on 25/25).
5. **`TA-X-08` lethal tick:** exercised on **9 distinct dying port trajectories** (reference: 3); inapplicable on the clearing cells (§ F.5 cl. 15).
6. **`TA-X-13`:** counted from player rows (`n_player_crit_rows` incremented at `kc2rt_fight.gd:3041-3043` per emitted row). This is no longer the old never-incremented `n_player_crits`. See INFO-3 for what the row's crit field is.
7. **`TA-X-21`:** the 14-site list is cited in full; the dead three are `deferred_arrival.py:329`, `threat.py:1813` and `threat.py:2182`.
8. *(also)* **The `TA-X-29(b′)` divisor clause is UNREACHABLE-IN-PACK.** Port composed rows: 0. The `a8` rows taken are the explicit-`True` ones (0017 / 0179 / 0334 / 0490 / 0647).

**§ F.5 rule 13 as it would read:** *"`TA-X-08` identity 2 carries `n_control_suppressed_channelling`. On this run it was 122 (max 12 on one cell); in G3 it was 80 and equal to the oracle's on every cell."*

---

## 3 · Findings

### BLOCK-1 · `TA-X-25` (c)(2) RED: the port labels GD-armed bodies `measured_inert` — **PORT EMISSION DEFECT → drax**

**What I found.**
- On every cell, 12–14 roster bodies of five records are emitted with class `measured_inert` in `cell.json :: nodata.spawn_by_record`, and in `board.ta_x_25 (c)`. They are counted in `measured_inert_spawn`.
- The five records, with bodies over 25 cells: `wendigocannibal_a01` 125, `yetidire_a01` 100, `basilisk_a01` 75, `yetidire_b01` 30, `bounties/ku_bounty_07` 5.
- v1.14 `TA-X-25` re-derived SWING = POOL-466, NONSWING = ∅. So clause (c)(2) requires every body to be `measured_offense`. The oracle passes 25/25 (v1.14 § K).

**Why it is a label defect, not a behaviour defect** (read from source at `ef5c04a`):
- `kc2rt_board.gd:838` classifies a spawn by `roster.body_state[rec]`.
- That value is set at load time (`kc2rt_roster.gd:1133-1143`) from the u5 outcome and `roster.can_swing`, **before** GD's Default-attack fold. A u5 HONEST-FAIL or DYING-ONLY record has no live slot there, so it is labelled MEASURED-INERT.
- The fight does not read `body_state`. At wave open, `_v3p11_wave_open` (`kc2rt_fight.gd:7705-7715`) **overwrites each body's `can_swing`** from `_swing_period_of(rec) > 0 and live_slots(rec)` over `_v3p11_slot_overlay`, which prepends GD's Default attack (`apply_default`).
- The harness's own verdict-level `ta_x_25`, computed through that same fight gate, says `n_nonswing = 0`.
- G3 against `V311-FULL` is 25/25 with zero divergence. That includes `yetidire_b01`, whose arming was the KP-259 fix.
- The board's emitted self-description, *"(c) label_is_the_gate: … the value `_make_body` reads to decide the body's disposition"*, has been false since v3.9 F4 moved the gate into the fight. The disposition it reads is never consulted downstream.

**Classification (KP-185):** a PORT defect in what the runtime **emits**, not in what it **does**.
- It is **not** an ill-posed row. The row is well-posed: the oracle satisfies it, and v1.14's expiry clause for `TA-X-25` named exactly this move.
- So **no HALT to Matt**.
- It is not a harness defect in the narrow sense: the label is produced in `sim/kc2rt_board.gd` / `kc2rt_roster.gd`, inside the runtime tree, so the repair moves the digest.
- **A grader may not substitute the verdict-level set block for the per-cell class.** That would be reading a different field to make a row pass.

**Fix (drax).**
- Make the spawn class follow the v3.11 arming gate. Classify by the same predicate the fight applies at wave open (`_swing_period_of > 0 ∧ live_slots non-empty` over the folded slots), not by the load-time `body_state`. The repair must not branch on arm, salt, wave or tick (§ G.1a).
- Keep `nodata_inert` for genuinely profile-less records. That set is empty at v3.11.
- Correct the board's `label_is_the_gate` text and the stale SWING-456 / NONSWING-10 strings.
- Fail-first probe: RED on `ef5c04a`, GREEN at the fix. Expect 0 `measured_inert` bodies on 25/25.

**Then:**
- a new MANIFEST digest;
- H-3 delta Gate-2;
- G3 V311-FULL 25/25 + native shadow 0;
- **H-2 and H-7 re-run at the new digest** (a read consumes nothing).

### WARN-1 (on my instrument) · the pinned grader printed `TA-X-07` UNGRADEABLE; r2 corrects a regex, one line

- The pinned grader's independent census parser took the census `f` column as `\d+`. F-class rows carry `f` as an expression (`"R+4"`, `"2K+3"`), so 14 F rows were unparsed, the census read non-green, and (L2) item 2 failed on every cell.
- **r2** (`grader_h7-r2.py`, FILE `fd5a2a0f…`) changes that one regex group to `"([^"]*)"`, plus a docstring note. `diff` shows exactly that.
- No expected value, tolerance or rule moved. Every other output line is byte-identical between the pinned and r2 runs (checked by `diff`).
- After r2: census 47 / 35 / T22 S11 F14 green, (L2) 25/25, `TA-X-07` GREEN. The pin did its job: the deviation is in the open.

### WARN-2 · the real `.app` vendors the superseded runtime → drax, before the attempt

- `desktop/KC2Play/build/desktop/KC2Play.app` was built 2026-10-01 15:28. It predates `fd799b63` and vendors `d03ca891` (drax's own probe at this tree: *"re-vendor and rebuild the .app at this tree"*).
- Run at the attempt, the harness will record `runtime_header.vendored_runtime_equals_runtime_digest = false` as an emission failure (exit 1). § G.3 lifts that boolean to the verdict file's top level, and my v1.13 read graded P-4 on it.
- It is not one of the 28 rows.
- **Fix:** re-vendor and rebuild the `.app` at the attempt digest before the attempt.

### WARN-3 · `ta_manifest.json :: ta_x_29_b_c_d["(b)"]` still carries the Z5 block → drax (with BLOCK-1)

- v1.15 § F.2h′.1 names `ta_manifest.json :: ta_x_29_b_c_d["(b)"]` as the CompositionFold block, *"replacing the Z5 block"*.
- At this tree that key holds the v1.13 Z5 content (`c5_equals_z5_in_content`, 40 compositions). The § F.2h′.1 block appears instead in `ta_verdict.json :: ta_x_29_b` (summed) and in every `cell.json :: ta_x_29_b`.
- The row is gradeable from those, and I graded it there. But a grader reading the named location reads the retired law.
- **Fix:** emit the summed § F.2h′.1 block at the named key, or keep both under explicit names. The file is in the runtime tree, so fold it into the BLOCK-1 repair.

### INFO

- **INFO-1 · § G.1a item 2 (who emits).** The emission above is mine (scratch, boot-checked), not a drax-filed `evidence/kc2-play/…PRE-READ…` folder. After the repair, either drax files one and I read it, or I re-run the same way. Both reproduce byte for byte (`TA-X-01`).
- **INFO-2 · `TA-X-10` printed bound.** The harness emits the port-computed bound through `JSON.stringify` as `43.7163814796516`, which is 15 significant digits, not the repr. So "port bound == v1.14 bound" prints false. Not graded; the margin is 0.65 m. A lossless emitter would remove the false-looking print.
- **INFO-3 · Structural zeros.**
  - `TA-X-13`'s count is now taken from rows, but the player row's `crit` field is the literal `false` (`kc2rt_fight.gd:3037`). The port has no player crit roll, consistent with V0 CritLimb LO.
  - `TA-X-12`'s 0.0 is emitted as a constant under ORACLE.
  - Both rows are GREEN on law and source. Neither is a measurement (§ F.5 cl. 6).
- **INFO-4 · Oracle-only stream keys.** G3 labels the two declared oracle-only streams by their **construction** lines (`spawn_structure.py:344`, `player_kit_residual.py:286`). v1.14 § C.9.1′ re-cites the **draw** lines `:345` / `:353`. I read all four lines at `969fbd8d`: same streams. The identity is consistent.
- **INFO-5 · Port vs reference trajectories.**
  - On its own generator the port clears **4 of 13** distinct trajectories, against the oracle's 9 of 12. 16 of 25 cells die, and `M-POL-2/W1/W1-NULL` s3 die at w157.
  - This is `TA-B-01`-type information and not draw-comparable (§ C.7); G3 on the oracle's draws is the fidelity evidence.
  - **gamora:** print the port's 13/4/9 and the reference's 12/9/3, each labelled, so the notes' reference sentence is never read as the emission's.
- **INFO-6 · v1.14 § L.4 scope note.** Player-summon hits on monsters (`_apply_summon_hits`, `kc2rt_fight.gd:2893-2905`) take HP outside `_offer`. They are **outside** `TA-X-07`'s identity, not booked into it. That is consistent with "gains no sink", but § L.4 lists "summon hits" as an intake path without saying they are out of scope. No effect on (L2).
- **INFO-7 · For the attempt** (after the repair):
  - boot with `expect_runtime=<new digest>` and `pre_read_finding=<the re-read>`;
  - print the graded-vs-read difference per cell (the read predicts empty).
- **INFO-8** is the `make_manifest.py` disclosure above.

## Ruling — how the attempt proceeds

**Attempt 1 of 2 (overall 4) does not fire at `fd799b63`.** Firing would read `TA-X-25` RED and grade `STRUCTURAL`, spending one of two on a knowable label defect (the KP-178 lesson).

Sequence:
1. drax repairs BLOCK-1, folding in WARN-3, and rebuilds the `.app` (WARN-2).
2. New digest.
3. H-3 delta Gate-2.
4. G3 25/25 + shadow 0.
5. H-2 + H-7 re-read at that digest.
6. On 28/28 GREEN, fire at the read's digest.

No prereg changes. Nothing goes to Matt. Budget unspent: **2 of 2.**

## Action

- [ ] **drax:** BLOCK-1 (spawn class from the v3.11 arming gate; fail-first probe); WARN-3; WARN-2 (`.app` at the new digest). New MANIFEST.
- [ ] **jack-ryan:** H-3 delta, H-2 and H-7 re-read at the new digest.
- [ ] **gandalf (conductor):** record H-2 PASS and H-7 BLOCK (no fire); budget 2 of 2 unspent; no HALT.
- [ ] **gamora:** INFO-5 face labelling at the attempt.
- [ ] **Matt:** nothing required.

## References

- Instruments: `agentic_orchestration/qa/findings/2026-10-02-kc2-attempt4-candidate-h2-h7/`, `MANIFEST.json` FILE `aa44de23…`:
  - `grader_h7.py` (pinned, `15cad3371`), `grader_h7-r2.py`;
  - both stdouts, `h7_results_r2.json.gz`;
  - `p2c.json`, the control-(c) probe stdout;
  - `PRE-READ-NOT-A-GRADED-RUN-emission/` (`emission.tar.gz`, harness stdout).
- Prereg: v1.14 § 0.2, § B.0, § B.1a, § B.6, § C.9, § F.2m′, § F.2p, § F.5, § G.1/G.1a/G.3, § H, § K, § L; v1.15 § F.2i′, § F.2h′, § K′, § H; notes §§ 1–5; v1.12 § F.2k (L0–L2, census).
- Source at `ef5c04a`:
  - `kc2rt_board.gd:836-945, 1000-1008`; `kc2rt_roster.gd:1130-1143, 1548-1558`;
  - `kc2rt_fight.gd:2893-2905, 3020-3046, 7695-7740` and `_offer` / `_cons_add` / `_neu`; `kc2rt_laws.gd conservation_residual`;
  - `kc2rt_composition.gd:55-66, 255-278`; `kc2rt_booking_census.gd`;
  - `tests/kc2rt_ta.gd`, `tests/kc2rt_ta_emit.gd`, `tests/kc2rt_h4.gd`.
- G3: `evidence/kc2-play/2026-10-02-g3-25cell-kp261-V311FULL-96fc0cc/` (MANIFEST `7a146d89…`).
- Ledger KP-238 … KP-272. My H-6: `2026-10-02-kc2-ta-prereg-v1.15-h6-preread.md`. My v1.13 read: `2026-10-01-kc2-play-v1.13-pre-attempt-read.md`.
