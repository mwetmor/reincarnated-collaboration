# KC2-PLAY · T-A "attempt 1 of 2, overall 4": gamora's independent second read

**Date:** 2026-10-03. **Reader:** gamora (simulation and spirit-guide seam). **For:** the conductor, gandalf.
This is the v1.13-era practice: jack-ryan grades, and gamora reads the same emission independently. It answers jack-ryan's INFO-4.
**Read-only.** I did not run or edit the runtime, the oracle, the preregs or the emission. Nothing graded was re-run.

## Verdict: **PASS**. I agree with jack-ryan on every row.

> `PASS @ coverage 89/89, 28/28 EXACT rows GREEN, TA-X-06 UNGRADEABLE-declared (Q83(b)), substrate_epoch v3.11 / model 99711727… / reference af58ef40…, prereg v1.15 (carrying v1.14 5bbe7ae5…, notes 7797ff17…), runtime 3e2359a6…`

- Counts: **28 GREEN, 0 RED, 0 UNGRADEABLE.** P-1 to P-5 are GREEN and C1 is CONFORMING.
- I disagree with jack-ryan on **no row, no precondition and no value.** I found **seven INFO face items** that he did not list (§ 4). None of them changes a row or the verdict.

## 1 · Instrument and independence

- The instrument is `read_attempt4_v1p15.py`, in this folder. I adapted it from my own v1.13 attempt-2 grader (`../2026-10-01-kc2-play-ta-attempt2-v1.13-grade/grade_attempt2_v1p13.py`) and re-pointed it at v1.14 + v1.15 + the notes.
- I did not import or open jack-ryan's grader (`grader_h7-r3.py`).
- **Order of work:** I produced the row table below (`run_stdout.txt`, `results.json`) first. Only after that did I read his finding (collab `08ff46709`), and I wrote § 3 by hand.
- **Expected values** are quoted from the prereg texts. Where a law is stated, I recomputed the value from the v3.11 pack:
  - LU-KEYS and P06-KEY, from `waves.json`;
  - the TA-X-09 ROWSET, from `math_rules.json`;
  - the TA-X-27(d) pairs;
  - z3;
  - POOL-466, by the export law. That module is byte-identical to its `969fbd8d` blob.
- **Oracle source** is read through `git show 969fbd8d:` (TA-X-21). Engine HEAD has moved on to `102c28e0`.
- **Port source** is read through `git show 9756c31:` (TA-X-17, 19, 21, 24).

Run it with `python3 read_attempt4_v1p15.py`. It exits 0 and prints `PASS | identity ok: True`.

## 2 · Identity and pins (all verified)

| item | value | check |
|---|---|---|
| prereg v1.14 / v1.15 / notes | `5bbe7ae5…` / `d1c4a75a…` / `7797ff17…` | FILE re-hashed; committed clean |
| emission | godot `9756c31`; 28 members, all re-hashed from git objects and equal to the worktree; tree recomputed `51dc9d68…` = MANIFEST | ✓ |
| `ta_verdict.json` / `ta_manifest.json` | `03f20be4…` / `4ec6fdc3…`; both equal to the MANIFEST's pinned files; `filing_checks.all` true | ✓ |
| runtime | `kc2_runtime/MANIFEST.json` recomputed over the blobs at `9756c31`: `3e2359a6…` (107 members); `kc2_runtime/` unchanged from `c64c192` (HEAD at the run) and from `66605a1` (G3) | ✓ |
| native library (§ C.9.8) | `native/bin/libkc2rt_contact.macos.arm64.dylib`, a runtime member, `74360ffa…`. This equals the G3 summaries, the 25 T-A cells (contact=shadow, 0 mismatches) and the verdict's `g3.native_shadow` | ✓ |
| G3 folder | `…/2026-10-03-g3-25cell-kp274-V311FULL-66605a1`: 50 members, tree `425f384d…` recomputed, `oracle_level` V311-FULL | ✓ |
| pre-attempt read | `finding_sha256 76667f56…` = the file = its blob at collab `531cbfc1d` | ✓ |
| packs | model `99711727…` (21 members), reference `af58ef40…` (7), cross-pin; `math_rules` / `arena` / `player_kit` FILEs = v1.14 § A.1 | ✓ |
| verdict identity fields | `prereg_version` v1.15; `run_kind` attempt; `attempt` "attempt 1 of 2, overall 4", overall 4; `verdict` null; `substrate_epoch` and `oracle_of_record` as v1.14 § G.3; runtime digest equal at boot and at end; `godot_head_graded` `c64c192`, clean; `failures` []; conditions raised to the grader [] | ✓ |

## 3 · The row table, reconciled with jack-ryan

| row | gamora | operands (gamora's own computation) | jack-ryan | agree |
|---|---|---|---|---|
| P-1 | GREEN | 89/89, 0 unmapped | GREEN | ✓ |
| P-2 | GREEN | § B.3a (1)–(5); controls a/a0/b are not GREEN; control (c) is carried as H-3/H-7's | GREEN | ✓ |
| P-3 | GREEN | POOL-466, WEIGHTED/UNIFORM (the incumbent roll, § L.2) | GREEN | ✓ |
| P-4 | GREEN | 26 P4 blocks; runtime header read by running, = P-4 | GREEN | ✓ |
| P-5 | GREEN | carried settings by value; five `a8` ROWSETs = § B.1a, configured from `a8`, P-MOVE; `setup` C/T partition, 0 applied | GREEN | ✓ |
| C1 | CONFORMING | G3 25/25: 0 decision/draw divergences across all 8 classes; oracle-only streams ⊆ the two declared streams; deaths, census and control term equal (Σ 80 = 80); `oracle_complete` w151–w160 on 25/25 (§ C.9.9); native shadow 0 (§ C.9.8) | CONFORMING | ✓ |
| TA-X-01 | GREEN | M0 s2 run twice `d5f76d79…` = the graded M0\|2 digest | GREEN | ✓ |
| TA-X-02 | GREEN | 89/89 | GREEN | ✓ |
| TA-X-03 | GREEN | M-POL-2-NULL ≡ M0 on 5/5 salts, by digest **and** by my own subject comparison (terminal, census, board, hp_trace, draws) | GREEN | ✓ |
| TA-X-04 | GREEN | W1-NULL ≡ M-POL-2, 5/5, by both methods | GREEN | ✓ |
| TA-X-05 | GREEN | M-POL-2 ≢ M0, 0/5 identical, by both methods | GREEN | ✓ |
| TA-X-07 | GREEN | (a) max ρ̂ 2.2115e-16; (c) (L2) exact over each cell's own operands, 25/25; worst W1\|4, β 5.3644e-14, margin ×18.64 | same figures | ✓ |
| TA-X-08 | GREEN | identities (1), (2) restated, (2p) and § F.2o on 25/25. On the 8 cleared cells: 10 PRE_FIGHT and no lethal tick. On the 17 dying cells: the lethal tick is censused alive. Control term Σ 122 | same (122) | ✓ |
| TA-X-09 | GREEN | ROWSET `0e826ee0…` (from the pack); 9/9 replayed | GREEN | ✓ |
| TA-X-10 | GREEN | W1 armed; max body 43.0183–43.0707 ≤ 43.71638147965161 | same | ✓ |
| TA-X-11 | GREEN | 0/0 clamps on 10/10 W1 and W1-NULL cells | GREEN | ✓ |
| TA-X-12 | GREEN | 0.0 on 25/25 | GREEN | ✓ |
| TA-X-13 | GREEN | 0 crit rows with `source == player`; player rows 9,035–16,458 per cell; never vacuous | same | ✓ |
| TA-X-14 | GREEN | causes ⊆ {type_a, type_b}; 0 energy causes | GREEN | ✓ |
| TA-X-15 | GREEN | 1,133 (wave, point) rows: p01–p04 at tick 0, p05 at tick 49; 0 staggers | GREEN | ✓ |
| TA-X-16 | GREEN | § F.2m′ (a)–(d) at key grain on 25/25. `W` ends at 157 on the three w157 deaths. The LU sets equal `pools_for(w, False)` re-derived from `waves.json`, and equal `derive_v1p14.json` | GREEN | ✓ |
| TA-X-17 | GREEN | max ‖spawn − anchor‖ 7.95483 ≤ 8.0; anchor is the v3.8 GD emitter on 25/25; the source law and the pack's extents of 8.0 also read | same | ✓ |
| TA-X-18 | GREEN | bits `c00fffffffffffde` / `be9777a5cf72cec6`, lossless | GREEN | ✓ |
| TA-X-19 | GREEN | packet keys {seq, b, rec, direct, pcl, fams, cast, n_rows}; no position read in `_defer_arrivals` / `_cp_absorb` / `_land` | GREEN (by construction) | ✓ |
| TA-X-20 | GREEN | r = 3.0; 5/5 cases | GREEN | ✓ |
| TA-X-21 | GREEN | 12/12 quantisation rows = Python `round`. My own read of every `round(` line in the six in-scope modules at `969fbd8d` found exactly the notes' 17 lines: the 14 live sites all use `int(round(`, and 3 are dead. FILE digests = the notes'. The emitted list is equal line for line. 0 bare `round(` over 90 `.gd` files (my scan) | GREEN | ✓ |
| TA-X-22 | GREEN | flag cause 0 | GREEN | ✓ |
| TA-X-24 | GREEN | `PhaseModel.ENGAGE`; no `sha256(actor_id)` site on sim/loader | GREEN | ✓ |
| TA-X-25 | GREEN | POOL-466 recomputed `33c886a1…`; every body ∈ POOL-466 and `measured_offense`; (c3) over ∅ (`e3b0c442…`) | GREEN | ✓ |
| TA-X-26 | GREEN | (a)–(e); P-i `cb6a008b…`; ARMED-464 statistics | GREEN | ✓ |
| TA-X-27 | GREEN | (a) 0/0; (b) my own CPython 3.12.0 replay, 16/16 seeds equal; (c) 41 = 29 V9 + 12 rg1 (ids = § F.2p; RG-019 registered, not live), p05 elided, C1 conforming; (d) 139 / 97 from `waves.json` | same | ✓ |
| TA-X-28 | GREEN | caps 0/0, ALL_BODIES_IN_DISC, 0.57 | GREEN | ✓ |
| TA-X-29 | GREEN | (a) 193/154, 527/104, 344. (b′): four constants exact; each of the 25 per-cell blocks has n = n_equal for all 7 families and its arm's explicit-True `a8` row. Σ25 = the manifest totals: instant_nonphys 66,766 · phys_clamped 2,453 · unmapped 2,121 · unclamped 21,209 · dot 14,958 · dot_leech 162 · chaos_aether 0. PCL untouched. (c) z3 10/10. (d) 29 inert. (e) 3.197066 / 4.935649; 16 + 23 records; max deviation 0.0 | same figures | ✓ |
| TA-X-30 | GREEN | (a′) on 25/25: 814,944 roster steps (55,994 held, all zero; 0 clipped; unclipped + clipped + held = steps); 666,392 pet steps (exact + clipped + no-travel = steps); 0 halt-flag / position / NaN / reach / operand mismatches; every field present. (b′) 0 on 25/25 and vacuous on 25/25 (W1: 26,860–38,259 clamp calls, 0 stops). The manifest's ring halt of 2.4 comes from `arena.json`; NaN test present | same figures | ✓ |
| TA-X-06 | declared | port W1 vs M-POL-2 identical on salts [2, 3]; the oracle's were [0, 1, 4] (v1.14). Printed only | declared | ✓ |

**Disagreements: none.** Where we both print a number, the figures are equal: TA-X-07's β and margin, TA-X-08's 122, the TA-X-29 family counts, TA-X-30's step totals, TA-X-13's row range and TA-X-10's radii. Two readings in the table are mine and confirm his:
- TA-X-03/04/05 also hold on the digest's subject, not only on the digest.
- C1 accepts G3's oracle-only stream labels `spawn_structure.py:344` and `player_kit_residual.py:286`. At `969fbd8d` those two lines are the `random.Random(...)` constructors of the facing stream and the residual stream. v1.14 § C.9.1′ re-cited the draw lines 345 and 353 of the **same two streams**. So they are not a third stream and not a divergence.

## 4 · What the face should print and does not (INFO; no row or verdict effect)

I agree with jack-ryan's **INFO-1**: rule 11's holes sentence still reads *"A v1.12 PASS"* and should read "v1.15". Seven further items:

1. **The verdict file's `prereg_carried_from` does not match v1.15 § G.3.** The prereg specifies `{"version": "v1.14", "sha256": "5bbe7ae5…"}`. The emission writes `v1.12 / a0454776…`, under its own law ("read off the version that last stated it", via v1.15 → v1.14 → v1.13 → v1.12). The correct pins are elsewhere in the file (`prereg_set_of_record` and `prereg_chain` are both correct), so nothing is lost. But the named field departs from the prereg's text. jack-ryan's identity table checked the set of record, not this field.
2. **TA-X-29(e)'s provenance label is stale.** `gmag_conformance.⚑ definition` and `⚑ walk_config_a8` cite the v3.7.1 WALK rows `IC7-A-0379…0432` and say "carried to v1.12". v1.15 defines (e) on the v3.11 `WALK` job (`IC7-A-V311-0792…0830`). The **values** are the v3.11 walk's: they equal v1.15 to 6 dp and differ from v1.13's. So only the label is wrong.
3. **The TA-X-10 bound is printed lossily.** The cell's `ta_x_10.bound` and `walls.r_wall_m` print `43.7163814796516` (15 significant digits). That is not bit-equal to the prereg's `43.71638147965161`. I graded against the prereg's value. The port's in-memory wall radius cannot be confirmed bit-exact from the emission. It does not matter here, because the largest body radius is 0.65 m inside the bound.
4. **The P-5 block's `pool_lift` label and the verdict's `set_digests` block are stale.** The label still reads "SWING-456 · NONSWING-10". The `set_digests` block reports those v1.12 sets as "reproduces" alongside `ta_x_25`, which carries v1.14's SWING = POOL-466 / NONSWING = ∅. A reader could take the v1.12 sets as the graded ones. **v1.14 § B.6's per-arm fold list** ("the harness prints, per arm, the job ROWSET and its fold list") is also absent: the ROWSETs are printed and graded, the fold lists are not.
5. **TA-X-21's `quantisation.live_sites`** still labels the 12 test rows with the v1.13 `threat.py` list. That list includes the two sites the notes declare dead (1813, 2182). The graded site list (`oracle_live_sites`) is correct.
6. **Each cell's `draw_sites.sites_live: 29`** is the V9 count. TA-X-27(c)'s registry is 41 (`ta_x_27_c`). The emission also still prints `accumulation_budget_terms_v1p7: 4500` and the matching `n_terms_note`; that budget was retired at v1.12 (N8, already known). The depth on this run reaches 15,238 terms.
7. **Notes § 3.2 asks for the reference collapse "beside every per-cell count".** It is printed once, in `face.trajectories`, with the port's own figure labelled separately. My count of the port's trajectories agrees with that figure: 13 distinct, 4 clear and 9 die. For the trajectories to sit beside the per-cell rows, the report should print them there.

**Two observations that are not findings:**
- The port's realisation inverts TA-X-06's pattern: the port's W1 equals M-POL-2 on salts 2 and 3, where the oracle's equalled it on salts 0, 1 and 4. TA-X-06 is declared, and port cells are not draw-comparable with oracle cells (§ C.7), so this is print-only.
- The G3 summaries carry `relabelled_streams` (for example `run.py:1150|seed → run.py:1214|seed`). This is a label map between stream-constructor lines, not an injection. G3's `injected` field is [] on 25/25. It falls under H-3's review of the instrument, not this read.

**Seal conditions are unchanged:** H-5 (hole closure; the file says `PENDING (H-5)`) and H-8 (Matt's T-C replay). This read is not either of them.

## Files

| file | what |
|---|---|
| `read_attempt4_v1p15.py` | the instrument (gamora's own) |
| `run_stdout.txt` | its printed report |
| `results.json` | every row's verdict and operands, identity, and face checks |
