# Finding — 2026-10-07 — JOIN-1 J0-F port half (J-S8) · KP-310 runtime delta · KC-1b delta

**Reviewer:** jack-ryan (DEV-MODE, Gate-2). Three gates in one pass, under the JOIN-1 conductor (gandalf).
**Severity / verdicts:**

| item | verdict | what it means for the run |
|---|---|---|
| **(A) J0-F PORT-HALF Gate-2** (J-S8 port half re-frozen at the KP-310 anchor, `5ca44258`) | **PASS-WITH-FINDINGS** | **J-S8 is frozen on both sides and its digests are recorded. The charter § 5 J0-F bar ("no J2 commit may land before J-S8 is frozen") is MET.** 0 BLOCK, 1 WARN, 6 INFO. The WARN must be fixed before the first § 4.7 check of a J2 join-path commit. It does not have to be fixed before J2 work starts |
| **(B) KP-310 DELTA Gate-2** (runtime `5b5a539e` → `472cffc4`, godot `256b3e4`) | **PASS-WITH-FINDINGS** | The new digest may be depended on. 0 BLOCK, 0 WARN, 5 INFO |
| **(C) KC-1b DELTA** (engine `6f25b139` note, `4f6a8443` code + tests) | **PASS** | The decisions-log KC-1 entry is updated from "KC-1b owed" to **LANDED** (clause 5 + Status). 1 INFO |

**Targets:** godot `1c254a6` (emitter + wrapper + diff tool) · `34e77e3` (runtime tag as an argument) · `d33f7b9` (r2 freeze, now kept as `port-r2-534febc/`) · `115b9aa` (PREDICTIONS, committed first) · `17b1378` (controls + RESULTS) · `256b3e4` (KP-310 runtime; tag `kc2/referent-v1-sealed-r2-runtime-kp310` → `256b3e4`) · `15e4357` (re-freeze, manifest-port FILE `5ca44258…`) · `663aa2c` (KP-310 evidence). Engine `6f25b139`, `4f6a8443`. Oracle half of record: MANIFEST `f82807fb…` (engine `43b033d6`), unchanged.
**Developers:** drax (port half, KP-310), gamora (KC-1b). Conductor: gandalf (KP-309, KP-310, KP-312, KP-313).
**Principles applied:** REVIEW_PROCESS 1 (math before code), 2 (smoke gate / reproduction), 3 (cross-seam impact: oracle ↔ port), 4 (decisions-log as truth: KC-1), 5 (severity matters). Disciplines **#12**, **#75 cl. 6**, **#80**, **#86**. ADR-002, ADR-004. JOIN-1 charter § 4.3, § 4.7, § 5 J0-F, § 6 HALTs. CLAUDE.md "Sealed-artifact change protocol" (KP-312).
**Instruments (sibling folder `2026-10-07-join1-j0f-port-gate2/`, committed with this file):**
- `jr_port_rowsets_and_deltas.py`: an independent ROWSET re-derivation (written from the manifests' printed `rowset_law`; it imports nothing from drax's emitter or `kc2p_join1_gm_diff.py`) plus row-level cross-side diffs, with G2/G3 deltas bucketed by wave, family, field and ulp. Outputs: `out_rowsets_committed.json` (committed port, r2 port, oracle) and `out_rowsets_reemit.json` (my re-emission).
- `jr_kp310_term_check.py`: the port's KP-310 expressions, transcribed from the diff as Python doubles in the same operand order, checked against the **sealed oracle's own functions**, which are imported unmodified from the worktree of `kc2/referent-v1-sealed-r2-oracle`. It covers all 20 waves, 140 (wave, family) cells and 68 pets. Output: `out_kp310_term_check.json`.
- `jr_kc1b_blast_radius.py`: three 591-record compiles (pre-KC-1 / KC-1 / KC-1b) on one corpus, diffed. Output: `out_kc1b_blast_radius.json`.
- Logs of my own runs: `out_reemit_wrapper.log` (re-emission), `out_inv_base_kp310.json` (§ 4.7 round trip at KP-310), `out_ncm_kp310.log` (NC-M at KP-310). The grain files themselves stay in scratch: they are byte-equal to the committed ones (FILE digests 7/7).

Disk was 27–29 GiB free throughout, above the 20 GiB HALT. No command was refused.

---

## (A) J0-F PORT HALF

### A.1 · Is the emitter honest? **YES.** Each claim was checked, most of them reproduced.

| claim | how I checked it | result |
|---|---|---|
| **The 7 port ROWSETs equal the oracle half's** | **INDEPENDENTLY RE-DERIVED** from the committed grain files with my own rowset-law code, then **row-level** diffed against the oracle fixture, keyed by each grain's KEY | **7/7 ROWSETs equal the manifest and equal `f82807fb`'s**: G1 `725cbe3d` · G2 `ec0b1af5` · G3 `46c18ed8` · G4 `ee431329` · G5 `0757ec07` · G6 `e3b0c442` (empty) · G7 `69a7e00e`. Row level: **0 keys only-in-port, 0 only-in-oracle, 0 differing rows in any grain.** FILE digests 7/7 equal the manifest. Every non-empty grain has rows in 25 cells. Keys are unique |
| **Reproducible at the KP-310 anchor** | **INDEPENDENTLY RE-EMITTED.** I ran the committed wrapper (`kc2p_join1_gm_run.sh`, FILE `3e2d925a…`) with `JOIN1_RUNTIME_TAG=kc2/referent-v1-sealed-r2-runtime-kp310` and `JOIN1_PRE=…-join1-kp310`, into my own scratch. Its limbs derived the pins from the tag | **REPRODUCED.** Start-up limbs GREEN (L2 HEAD `256b3e49df` clean · L3 tree `472cffc4` · `N_moved` 0). 25/25 cells, 0 failed, 0 truncated, 0 cross-check failures, `draws_mm=0` and `shadow_mm=0` on every cell, wall 1051.5 s, rc 0. **All 7 ROWSETs equal the committed half, re-derived with my code.** At row level the re-emission differs from **both** the committed port half **and the oracle fixture** on 0 rows in every grain. **Even the 7 grain FILE digests are byte-equal to the committed manifest's**, gzip included. Log: `out_reemit_wrapper.log` |
| **It reads the sealed runtime unmodified** | the manifest's three start-up limbs, plus my own re-derivation of the tree digest | L1: loaded from the vendor root. L2: vendor-source worktree `reincarnated-godot-join1-kp310` at HEAD `256b3e49…` = the tag's commit, clean. L3: the tree digest recomputed from the vendored bytes = `472cffc4…`. **I re-derived `472cffc4…` myself from the worktree's 107 members (0 member mismatches)** under the MANIFEST `tree_digest_law`. `N_moved` = 0: mainline `kc2_runtime/` is byte-identical to the tag (`git diff 256b3e4 HEAD -- kc2_runtime` is empty). The hooks are subclass substitutions (RecFight / RecSummons / RecRng). They are shown inert by **bare == hooked 25/25**, and that digest is computed with **`JSON.stringify(…, full_precision=true)`**, so it is a bit-level inertness check and not a 15-digit one |
| **It uses the J-P2 normaliser** | the pin compared with the oracle manifest's, and the file hashed | `join1_stdout_normalise.sed` FILE `da5d148a…`. Wrapper pin = oracle manifest pin = the file on disk (engine `8eb982b0`, unchanged since) |
| **It replays the oracle's recorded draws** | the per-cell draw-trace FILE pins on the manifest; `draws_mm` per cell | 25 traces are pinned by FILE. `draws_mm=0` on 25/25 baseline cells, so it is a pure replay with no fallback. The traces are also **validated end to end**: the oracle fixture was emitted by gamora's Python emitter **without** these files, and the port that consumed them reproduces it bit for bit on 7 grains. A wrong trace would not survive that |
| **The emitter of record** | manifest `emitter.FILE_sha256` compared with the file at HEAD | `5a9466c2…` = `kc2_play/tools/kc2p_join1_gm_emit.gd` at HEAD; last touched at `34e77e3`; `uncommitted_changes: false` |
| **The r2 half is kept honestly** | the renamed half's manifest re-hashed, its ROWSETs re-derived, and r2 diffed against oracle and against the re-frozen half | `port-r2-534febc/manifest-port.json` = **`8479a2fd…`**, the KP-309 FILE, byte-identical after the move. Its G2 `5a1e1aa7` and G3 `1bbe76bb` differ from the oracle on **exactly 10,256 G2 + 34 G3 rows, all in waves 151–155** (G2 by wave: 2,423 / 1,790 / 3,756 / 1,254 / 1,033). **The r2 → KP-310 delta is that same row set, row for row.** Nothing else moved |

**What J-S8's port half certifies, stated plainly (INFO-A5):** this is a `--draws` replay. It certifies the port's arithmetic and decision logic **given the oracle's random stream**. It does not certify the port's own RNG. That is carried separately by G3 (`draws 0` on 25/25 at KP-310) and by the bare == hooked inertness limb, where the bare run uses the runtime's own classes. The manifest's `draw_mode` field says so. Any citation of J-S8 as "the port equals the oracle" should keep the qualifier.

### A.2 · The controls were sized and run against the r2 half, not the re-frozen half. **ACCEPTABLE.** I discharged the two re-runs it still owed myself

**What changed between the half the controls ran against and the half of record:**
- **Runtime:** 3 files, all in the loader (`kc2rt_offense_fold.gd`, `kc2rt_v3p6p1.gd`, MANIFEST). On J-S8 the change moves **only** `pre_mitigation` and its arithmetic descendants (`after_stage_1/2`, `regions`, `applied`, G3 `intake_hp`/`heal_hp`), by ≤ 2 ulp, on w151–155. Re-derived (§ A.1): **no decision field moves.** That means `family`, `stage_order`, `armour_branch`, `attribution`, `resist_used_frac`, the n-counts, and every row of G1/G4/G5/G6/G7.
- **Emitter/wrapper:** `1c254a6` → `34e77e3` only parameterises the runtime tag. I read the whole diff: **no grain, hook, guard, normaliser or control code changed.** The limb code **did** change: L2 provenance and `N_moved` now read `runtime_tag` instead of a constant.

**Per control: does its verdict transfer?**

| control | mechanism it exercises | transfers to the KP-310 half? |
|---|---|---|
| NC-1′ (pth threshold 90→91) | G1 only | **Yes, exactly.** G1 is byte-identical r2 ↔ KP-310 |
| NC-2 (RESIST_THEN_ARMOUR) | `stage_order` label + positional `after_stage_1` | **Yes.** The RED is a label/positional change that no ulp can mask. The "same pre_mitigation" clause was read against r2's value, which is the right baseline for that run |
| NC-3 / NC-3b / NC-3c0 (vacuous) | movement operands that never bind | **Yes, by mechanism.** Vacuity is a property of the movement code, which KP-310 does not touch, and KP-310 moves no decision |
| NC-3c (SWC R − 0.1) | G4 positional | **Yes for the RED limb.** G4 is identical. The MISS is ruled in § A.3 |
| NC-4 / NC-4b (KeyError) | refusal tick at the first Fire / Chaos packet | **Yes.** No decision or timing moved |
| § 4.7 control (INV-NC-2) RED | stream inequality | **Yes.** The NC-2 RED is independent of ulps |
| **§ 4.7 baseline round trip (INV-BASE)** | reproduction of the **frozen** half on three streams | **No. It is a statement about the specific frozen bytes.** INV-BASE showed r2 reproduces r2. It cannot show KP-310 reproduces KP-310 → **re-run owed** |
| **NC-M (provenance)** | the L2 limb refusing a non-tag vendor source | **Not by inheritance.** The limb's own code changed at `34e77e3`, and a remedy does not inherit its predecessor's instrument (**#75 cl. 6**) → **re-run owed** |

**Both owed re-runs were cheap. I performed them myself at this Gate, so neither is left to drax:**
- **Round trip at KP-310:** `kc2p_join1_invariance.sh` with `JOIN1_RUNTIME_TAG=…-kp310`, `JOIN1_PRE=…-join1-kp310` and `--inertness`, exactly as at the freeze. Result: **INVARIANCE GREEN on all three streams.** Stream 1: 7/7 ROWSETs and row counts equal. Stream 2: normalised stdout `4bb66fcd…` equals the frozen one. Stream 3: raw stderr `95c22c82…` equals the frozen one. rc 0, wall 1888.5 s, INERTNESS bare==hooked 25/25. Output: `out_inv_base_kp310.json`. With my earlier non-inertness re-emission, that makes **two independent reproductions** of the KP-310 half.
- **NC-M at KP-310:** `kc2p_join1_gm_run.sh … --nc-m` under the KP-310 env. Result: **HELD.** `JOIN1-HALT provenance: the vendor source worktree reincarnated-godot is at 663aa2c0…, not the seal commit 256b3e49…`, rc 2, the out dir was not created (only `-streams`), and the vendor seam was restored. As at r2, mainline `kc2_runtime/` is byte-identical to the tag (`N_moved` 0), so limb 3 could not fire and **limb 2 carried the control**. The parameterised limb therefore refuses on the KP-310 tag. Log: `out_ncm_kp310.log`. After both runs, the PRE worktree is clean and `git status` on mainline `kc2_runtime/` is empty.

**Ruling:** the eight perturbation controls stand as run, and they are cited as having run against the r2 half (`8479a2fd`). The round trip and NC-M at the KP-310 anchor are discharged by this Gate's runs. **No re-run is owed by drax.** INFO-A4 below covers the path references in PREDICTIONS/RESULTS that now point at the re-frozen half.

### A.3 · The NC-3c MISS (W1/3 refused with a port `timeout`). **ACCEPTED AS A RECORDED MISS. Not re-run, not a defect finding.**

- **What fired:** `terminal_reason timeout is outside the declared map [death, cleared, oracle_raises_unmapped_damage_type]`. The cell **failed and was not emitted.** ⚑ **Precision for the record (INFO-A2):** the refusal came from the emitter's **terminal-map check**, one step **before** the OBS-1 guard. So W1/3 has **no OBS-1 verdict at all**: `obs1_guard_port_equivalent.per_cell["W1|3"]` is `null`, and `n_truncated` is 0 on the NC-3c manifest. The failed clause is "OBS-1 complete 25/25", which failed because one cell never reached the guard. It did not fail because the guard returned TRUNCATED.
- **Why it is not evidence against the port:** `timeout` arises only from `ORACLE_WAVE_MAX_TICKS` (4000, `run.py:362`) in ORACLE mode, which means one wave of the **perturbed** fight stalled for 4000 ticks. In `--draws` mode, a control that moves the fight moves the draw sequence. drax disclosed this, and I confirmed it from the RESULTS: 1,447–3,000 mismatches per perturbed cell, after which the port falls back to its own generator. W1/3's tail is therefore **neither the oracle's perturbed fight nor the port's**. The oracle's own NC-3c ran 25/25 OBS-1 complete (my 2026-10-02 Gate, § 3), but it was a different fight, so the two are not comparable.
- **What the control was for, and whether it did it:** it was meant to show **G4 can see a pursuit-intercept perturbation.** It did: RED in **24/24** emitted cells, with the first G4 divergence before the first G1 divergence in each one. A refused cell is never GREEN, so the miss cannot hide a false negative.
- **Citation form (binding on downstream quotes):** *"NC-3c: G4 RED 24/24 emitted cells; W1/3 refused (terminal_reason `timeout` in the post-divergence hybrid tail), no verdict; the 'OBS-1 complete 25/25' clause MISSED."* The control tally, counted the way I counted the oracle side (INFO-4, 2026-10-02): **10 perturbation/instrument controls, 9 held in full, NC-3c held on its RED limb and missed one clause; plus the INV-BASE round trip GREEN.** KP-309's "9 of 10 held fully" and RESULTS' "10 predictions held and 1 clause missed" are the same facts counted over 10 and 11 rows. Quote the form above.
- **Predictions really came first.** `115b9aa` was committed at 19:40:09. The shared scratch shows `controls.sh` and `NC-M.log` at 19:40:26 and the first control directory (`NC-1`) born at 19:40:30. The dry runs before the freeze (`dry1` 18:51, `dry2` 19:01) contain no `control=` cell. The sizing file was computed from the frozen baseline grains (`d33f7b9`, 19:39:32), not from any control output.

### A.4 · The port OBS-1 guard. **ACCEPTED: equivalent in strength on everything J-S8 contains, and stricter in one clause.**

The shared module (`gamora_join1_obs1_guard_2026_10_02.py`, FILE `5f3f4f1e…`) checks the oracle composition's **Leg-B banked rows**, which continue past a death. The port plays **Leg A** and stops at the first death, so the module cannot be applied verbatim. I compared the clauses side by side (`_obs1`, emitter lines 1295–1318, against `salt_check`/`cell_check`):

| shared clause | port clause | on J-S8's window (151..terminal_wave) |
|---|---|---|
| G1: 10 rows 151..160 in order; raw outcome ∈ {cleared, player_death} | G1′: waves 151..terminal in order; every pre-terminal wave closed `cleared`; terminal ∈ {death, cleared}; a `cleared` ladder ends at 160 | **Equivalent.** The port's terminal is never rewritten, so it needs no raw-capture caveat |
| G2: **w160** did not end at the tick cap | G2′: **no played wave** reached the cap (4000, read from the sealed `simulate_wave` signature) | **Port stricter** (all waves, not one) |
| G3: 9·N rows on w151..159 | G3′: every wave 151..min(terminal, 159) present | **Equivalent per cell** |
| G4: summed time = summary | n/a (no summary layer) | n/a on both sides |

**Where the port guard is weaker:** it cannot inspect the **post-death** waves that the oracle banks under Leg B. Those waves lie **outside J-S8's window** (`scope.window = 151..terminal_wave`). A defect there cannot produce a J-S8 row, so it cannot produce a false green on J-S8.
**It is witnessed live, not just written down.** NC-4 and NC-4b were TRUNCATED 25/25, matching the oracle side's OBS-1 0/25 on the same controls. NC-3c W1/3 was refused, and as noted above that refusal came one step earlier, from the terminal map. A freeze refuses on either path (`n_failed > 0` and `n_trunc > 0` both halt when `control == ""`).
**The rule is on the manifest** (`obs1_guard_port_equivalent.rule`) and pins the shared module by FILE, and the cap is derived, never typed. **Ruled: accepted as the guard of record for the port half.**

### A.5 · The § 4.7 invariance control: **RED armed, GREEN baseline — HELD, and now re-proved at the KP-310 anchor (§ A.2).** One instrument defect found.

INV-NC-2 was RED on stream 1 (G1, G2, G3, G4, G5, G7) and stream 2 (first difference at cell M0/0, `control=NC-2`), with stderr byte-equal and rc 1, as predicted. INV-BASE was GREEN on all three streams at r2.

⚑ **WARN-A1, the default instrument is now inconsistent with its own frozen PRE (#75 cl. 6).** `kc2p_join1_invariance.sh` hard-codes `PRE = evidence/…/port`, which since `15e4357` holds the **KP-310** half (`5ca44258`). It then calls `kc2p_join1_gm_run.sh`, whose tag **still defaults to the r2 seal** (`TAG=${JOIN1_RUNTIME_TAG:-kc2/referent-v1-sealed-r2-runtime}`, and `34e77e3`'s message says "default is the r2 seal, unchanged"). Anyone who runs the § 4.7 port check **as documented, with no env vars**, re-emits the r2 runtime and compares it with the KP-310 PRE. The result is **INVARIANCE RED on G2/G3: a false HALT to Matt** on a join-path commit that changed nothing. This is the same shape as the second-face hazard in CLAUDE.md: a correct reading of the wrong configuration that presents as a real alarm.
**Fix (drax, before the first § 4.7 check of a J2 join-path commit):** the wrapper and the invariance script must **derive** the runtime tag from the frozen PRE they compare against (`join1-sealed-pins.json` `port.tag`, or `manifest-port.json` `port_tag`), and **refuse** if an env override disagrees with it (KP-101: derived, never typed). Then re-run the INV-NC-2 control once through the fixed script to show it can still go RED. **This WARN does not hold J2 work.** It holds the first gated § 4.7 claim.

---

## (B) KP-310 DELTA Gate-2 — runtime `5b5a539e` → `472cffc4`

### B.1 · Consent and protocol (KP-312, all four items)
1. **Matt ruling as a ledger row:** KP-310 (Q105, recommended option). ✓
2. **Fail-first:** probe RED at `5b5a539e`, GREEN at `472cffc4`. **I re-derived it from committed artifacts, independently of drax's probe:** the r2 half's G2 row `(M-POL-2, 0, 62, w151_a007, 0)` holds `pre_mitigation = 835.38` (`408a1b0a3d70a3d7`), and the KP-310 half and the oracle both hold `835.3799999999999` (`…d6`). ✓
3. **ORACLE byte-identity:** the Python oracle is untouched. The `simulation/kc2` tree OID at engine HEAD = `7496a28a…` = the sealed tag's, and the working tree is clean there. G3 V311-FULL 25/25 `dec 0 · draws 0` (`equal_to_kp274.json`: 0 differing leaves excluding `trace_sha256`). T-A pre_read 25/25 cell digests equal KP-290b's (= attempt 4). § 4.7 PLAY harness GREEN in all four modes. ✓ See INFO-B2 for what these instruments can and cannot see.
4. **jack-ryan delta Gate-2:** this section. ✓

The runtime diff is exactly 3 files (`git diff --stat 534febc 256b3e4 -- kc2_runtime`). The tree digest `472cffc4…` was re-derived (§ A.1).

### B.2 · Term-for-term fidelity. **VERIFIED over the whole pack table, not only the graded referent.**

`jr_kp310_term_check.py` runs the port's expressions as Python doubles in the diff's operand order, against the **sealed oracle's own** `WaveDamageRow.instant_mult` / `.dot_mult(fam)` / `.attack_speed_mult` / `.oa_flat_add` / `.oa_modifier_add` and `threat._pet_oa_folded` / `oa_pre_modifier`. Those are imported from the sealed worktree, reading the oracle's own CSV.

| value | oracle site | port expression (KP-310) | port == oracle | old literal == oracle |
|---|---|---|---|---|
| `M_inst` | `offense.py:398-401` `1.0 + sum_total_pct / 100.0` | `1.0 + float(sum_total_damage_modifier_pct) / 100.0` | **20/20** | 10/20. It differs on **w151–155 and w161–165** (Σ = 82; 1 ulp) |
| `M_dot` | `offense.py:403-428` `1.0 + (d_dot_pct[fam] + u_dot_pct) / 100.0`, raise on m < 0 | `1.0 + (D_pct + U_offensiveSlowAllTypes_pct) / 100.0`, refuse on m < 0 | **140/140** | **0/140**: the literal is **1–4 ulp high** on every cell |
| H2 `attack_speed_mult` | `offense.py:386` | `1.0 + (D + U) / 100.0` | 20/20 | 20/20 |
| H1-OAW `oa_flat_add` / `oa_modifier_add` | `offense.py:364-372` | `D + U`, both limbs | 20/20 | 20/20 |
| H1-OA pet `oa_eff` / `oa_pre_modifier` | `threat.py:355-366`, `1183-1190` | `(base + 0.0 + float(lvl) * lf) * (1.0 + 0.0/100.0) + tail` | **68/68** (level 68/68) | 68/68 |

The pack operands equal the oracle's CSV values (`sum_total` 20/20, `D_pct` + `U` 140/140), and `H1-CONST` `OA_LEVEL_FACTOR` / `OA_FLAT_TAIL` equal the oracle's constants. The pack's DoT family set equals `DOT_FAMILY_COLUMN` on all 20 waves, and neither declared-unmodified family appears in it, so iterating the pack's `per_family` keys builds exactly the oracle's table. The `SlowLifeLeach` / `SlowManaLeach` → 1.0 path is unchanged in `mult_for`.

### B.3 · Does the `M_dot` change move anything graded? **NO, re-derived two ways.**
- **Analytically:** under V311 composition, `M_dot` enters a DoT row only as `(om − 1.0)` (`gd_composition.py:176`). For every (wave, family) I checked whether `(literal − 1.0) == (computed − 1.0)`. The two are **equal on w151–166 for all 7 families and differ on w167–170 for all 7.** The graded window is w151–160, so the old literal was absorbed everywhere it was graded. drax's mechanism is confirmed. ⚑ **Correction (INFO-B1):** the literal is 1–**4** ulp high, not "1–3".
- **Empirically:** the r2 → KP-310 J-S8 delta is **exactly** the r2-vs-oracle row set, confined to **w151–155**. That is 10,256 G2 rows, 17 families, DoT families included through `tdm = M_inst − 1`. **Zero rows moved on w156–160.** G3 is `dec 0` on 25/25, and the T-A digests are unchanged.
- **What it does move:** port output at w167–170 and on the non-composition DoT path (pre-V311 oracle levels), both toward the oracle. **The latent defect drax named is real, and it is now closed.** PLAY sessions that pass w166 will differ from pre-KP-310 PLAY by ulps on DoT rows. That is by design, toward the oracle, and not a § 4.7 matter, because PLAY and ORACLE read the same fold.

### B.4 · The same-class grep. **ACCEPTED: the FIXED and LISTED dispositions hold.** My own pass found nothing reclassifiable, plus three INFO notes

I grepped the runtime loaders and sim for reads of derived-looking pack fields (`*mult*`, `*_eff*`, `*_add*`, `*effective*`, `M_inst`, `M_dot`, `*total*`, `sum_*`, `*speed*`), about 40 sites, and checked each one against drax's list:
- **`z3` `M_inst` (assert only): confirmed.** `check_z3_against` has 4 callers and changes no value. ⚑ Its tolerance is `|Δ| ≤ 1e-9` against the z3 **literal**, so it passed the pre-fix port as well. **It cannot see the class it sits beside.** This is not a defect, because z3 carries no operands and bit-equality against a literal would now go RED. It must never be cited as evidence of `M_inst` fidelity (INFO-B3).
- **V22 roster `oa_eff` / `oa_pre_modifier` (LISTED, "operand absent"): confirmed.** The oracle builds `oa_pre` from `offensive_ability_base` + `level_min` (from `tim`) + `tree_oa_flat_sum` + `creature_own_oa_flat` (`threat.py:941-951`), and the V22 row carries the base but **not the level or the flats**. The pair is internally consistent on **169/169** rows (`oa_eff == oa_pre·(1+mod/100)+53` exactly). G1 `oa_folded` is bit-equal on 56,511 attempts on the referent. **This is a residual class instance bounded by J-S8, not closed by construction.** It goes on **J2's FORM/OPERAND operand list**: level + the two flat sums (INFO-B3).
- **Not on drax's list, and not the class:** `v3p6` `om_add` (already computed from rows, cross-checked against `grant_om_add` at 1e-12); `leech_table` `adcth_mult_*` (READ by rule V1-LIMB-2, "never recomputed", which is the oracle's own column choice); `global_magnitude` `own_total_damage_modifier_pct` (an operand). ⚑ **Test-side only:** `tests/kc2rt_completion_probes.gd:639-648` still reads the **`M_dot` literal** to size an expectation (1e-9 relative). That is harmless, but it is the class living in a probe. Compute it there too, or list it (INFO-B3).
- **Parity nit (INFO-B4):** the port's `attack_speed_mult` drops the oracle's two `raise` guards (m ≤ 0, and m > `MONSTER_ATTACK_SPEED_CAP_MULT` 5.0). They are unreachable on v3.11 (sums are +11/+12). `M_dot` **does** carry its refusal. Add the two refusals in the next runtime touch, so that a future pack cannot drift past what the oracle would raise on.

### B.5 · The protocol slip (`rm -f /dev/null;` in one call). **Recorded. No effect, no finding against the change.**
The command had no effect (`/dev/null` is root-owned), and it was self-disclosed in KP-313. It broke two conventions at once: no `rm`, and one command per call. **The rule set did not block it**, which is the informative part: KP-312's mechanism is allow rules, and nothing **denies** `rm`. I agree with the candidate tightening (`Bash(rm *)` deny in the collab `settings.local.json`). That is **Matt's call** (configuration he controls, KP-312), and it is routed to him in the Action list, not decided here.

---

## (C) KC-1b DELTA — engine `6f25b139` (note) · `4f6a8443` (code + tests). **PASS.**

| claim | how I checked it | result |
|---|---|---|
| Math before code | commit order | note § 7 **alone** at 19:34:18, code at 19:35:31 ✓ |
| The predicate is narrowed to an **evidenced** conversion | read `_has_conversion_row` | `(?:^|_)<re.escape(original)>_to_physical(?:_conversion)?_pct$` on the record's own `kit_numeric` keys. Presence is the evidence; the value is never read, so the dual-column law holds ✓ |
| **Fail-first 10 → 32/32** | **REPRODUCED.** I ran the `4f6a8443` test file against the `ccd89e38` compiler (both exported by `git archive` into scratch, with a sibling link so the live corpus tests run), then against the `4f6a8443` compiler | **10 failed / 22 passed** → **32 passed.** The 10 are the pierce/bleed/`physical?` buckets, fire-court-without-row, the wrong-element row, and the 5 restored live records ✓ |
| **Exactly the referent moves over 591 records** | **REPRODUCED.** I compiled all 591 records three ways on **one** corpus (FILE `37635bad…`, read-only; it has moved on from gamora's `639acb20`, so I compared code versions on a fixed corpus) | KC-1 → KC-1b: **exactly the 5 over-moved records restored** (pierce ×2, bleed ×2, `physical?`). Pre-KC-1 → KC-1b: **exactly** `gd-eor-warlord-referent` (fire → physical) + the KC-3 note on `gd-eor-warlord`. 0 compile errors × 3 ✓ |
| Only the referent carries the evidence | `kit_numeric` query (read-only) | 3 `*to_physical*` rows in the corpus, all on `gd-eor-warlord-referent` (`eor_fire_…_conversion_pct`, `gutsmasher_chaos_…`, `gutsmasher_lightning_…`) ✓ |

**Decisions-log:** the 2026-10-06 KC-1 entry now has **clause 5 (KC-1b LANDED, re-derived)** and a superseding **Status** (the clause-3 gate is discharged; J2's family table may consume `dominant_element`). The original clause 3 is kept as the record of what was owed. Engine commit alongside this finding.
**INFO-C1 (for J2's family table; unreachable today):** the predicate keys on a row's **presence**, not on its **scope** or **magnitude**. A record whose only conversion row is **skill-scoped** (as `gutsmasher_*` is) or **partial** (< 100 %) would still move its **record-level** `dominant_element`. No corpus record is in either case. J2's family-table author should assert it rather than assume it.

---

## Findings register

| id | sev | finding | fix owed · by whom · by when |
|---|---|---|---|
| **WARN-A1** | WARN | `kc2p_join1_invariance.sh` compares against `port/` (now KP-310) while `kc2p_join1_gm_run.sh` defaults to the r2 tag. Run as documented, the § 4.7 port check reports a **false RED, which is a false HALT to Matt** | **drax:** derive the tag from the frozen PRE's pins and refuse on disagreement; re-show the INV-NC-2 RED through the fixed script. **Before the first § 4.7 check of a J2 join-path commit** |
| INFO-A2 | INFO | NC-3c W1/3 was refused by the **terminal map**, before the OBS-1 guard; it has no OBS-1 verdict (`per_cell` null, `n_truncated` 0) | conductor: cite in the § A.3 form |
| INFO-A3 | INFO | Control tally: 10 controls, 9 held in full, NC-3c held RED and missed one clause; round trip GREEN (r2, and now KP-310 per § A.2) | conductor: one form in every citation |
| INFO-A4 | INFO | `PREDICTIONS.md` / `RESULTS.md` name `port/manifest-port.json (FILE 8479a2fd)`, and that path now holds `5ca44258`. The FILE pin disambiguates, but the path is stale | **drax:** an append-only note in both, saying the controls ran against `port-r2-534febc/` (`8479a2fd`) |
| INFO-A5 | INFO | The port half is a `--draws` replay; it does not certify the port RNG (G3 `draws 0` does) | conductor: keep the qualifier when J-S8 is cited |
| INFO-A6 | INFO | **WARN-B (2026-10-02) carried to the port face:** `unexercised` lists only G6. It does not list G4 `beyond` ≡ 0 / `max_halt_distance_m` ≡ null, the 12-trajectory collapse, or the 55 floor (now covered by the hit-chance grid, KP-247/272). ADDENDUM-5 is pinned by FILE, so a reader can find it, but the face is silent | **gamora + drax:** add them to both faces at the next freeze of either half. **No re-freeze for this alone** |
| INFO-B1 | INFO | The `M_dot` literal is 1–**4** ulp high (not 1–3); `(om − 1)` absorbs it on w151–166 and not on w167–170 | conductor: correct KP-313's text in the next ledger row |
| INFO-B2 | INFO | **What the "ORACLE byte-identity proof" instruments can see.** T-A `cell.json` is serialised at **15 significant digits** (e.g. `intake_by_wave."151": 36739.3476266794`), and G3 compares decisions and draws. **Neither can see a ≤ 2-ulp move by construction.** "Unchanged" is a **decision-invariance** witness. For a change that is **meant** to move port values, the fidelity proof is **J-S8 bit-equality against the Python oracle**, and here it holds | **conductor/KR:** at the next touch of the CLAUDE.md protocol, item 3 should read *"ORACLE decision-invariance (G3 + T-A digests) + the Python oracle tree unchanged; and, where the change moves port values, J-S8 bit-equal"* |
| INFO-B3 | INFO | Residual class instances, none graded: the `z3` assert's 1e-9 tolerance is blind to this class; the V22 `oa_pre_modifier` literal has its operands (level, flats) absent from the row (169/169 consistent; G1 bit-equal); a completion probe reads the `M_dot` literal | **gamora/star-lord (J2):** level + flats onto the J2 operand list. **drax:** the probe, at the next runtime touch |
| INFO-B4 | INFO | Port `attack_speed_mult` lacks the oracle's m ≤ 0 / m > 5.0 raises (unreachable) | **drax:** at the next runtime touch |
| INFO-B5 | INFO | The `rm -f /dev/null;` slip is recorded; the allow-rule set has no `rm` deny | **Matt:** the `Bash(rm *)` deny is his to adopt or decline |
| INFO-C1 | INFO | KC-1b keys on presence, not on scope or magnitude (skill-scoped or partial conversion rows); unreachable on the corpus | **J2 family-table author:** assert it |

## Action

- [ ] **drax — WARN-A1:** derive the runtime tag in `kc2p_join1_gm_run.sh` / `kc2p_join1_invariance.sh` from the frozen PRE's `join1-sealed-pins.json`; refuse on an env disagreement; re-run INV-NC-2 through it (must be RED). **Before the first gated § 4.7 claim on a J2 join-path commit.**
- [ ] drax — INFO-A4 (append-only notes), INFO-B3 (probe), INFO-B4 (raises): at the next touch of those files; no runtime change is owed now.
- [ ] gamora + drax — INFO-A6 at the next freeze of either half.
- [ ] conductor — fold INFO-A2/A3/A5/B1 into the ledger's wording; route INFO-B2 to the CLAUDE.md protocol text and INFO-B5 to Matt.
- [ ] **Matt:** nothing is escalated. No BLOCK. No ORACLE behaviour change (the Python oracle tree is unchanged; G3 / T-A / § 4.7 decision-invariant; J-S8 moved toward the oracle by ruling KP-310). The one item for him is optional and configuration-level: INFO-B5's `rm` deny.

## References

- Charter: `agentic_orchestration/gandalf/notes/2026-09-29-join-1-run-charter.md` (v0.6.6; § 4.3, § 4.7, § 5 J0-F, § 6). Ledger: `…/2026-09-20-kc2-play-run-charter.md` KP-242–247, KP-307–313.
- CLAUDE.md § "Sealed-artifact change protocol (Matt, 2026-10-07; KC2 ledger KP-312)".
- J-P2 + ADDENDUM-1..6: `reincarnated-engine/src/reincarnated/simulation/math/kc2-join1-golden-master-instrument-2026-09-29*.md`.
- Prior Gates: `qa/findings/2026-10-02-join1-j0f-oracle-half-gate2.md` (WARN-3 ruling; INFO-4 tally form; WARN-B), `qa/findings/2026-10-06-join1-b0n-gate2.md` (KC-1 WARN-1).
- Port: `reincarnated-godot/kc2_play/tools/kc2p_join1_gm_emit.gd` (FILE `5a9466c2…`; `_obs1` 1295–1318; freeze refusals 760–790), `kc2p_join1_gm_run.sh`, `kc2p_join1_invariance.sh`, `kc2p_join1_gm_diff.py`; `evidence/join1/join1-gm-fixture-v1/{port, port-r2-534febc, port-streams, controls, oracle-draws, join1-sealed-pins*.json, diff-port*-vs-oracle.json}`.
- Runtime: `reincarnated-godot/kc2_runtime/loader/kc2rt_offense_fold.gd` (175–220, 225–330), `loader/kc2rt_v3p6p1.gd` (122–180), `loader/kc2rt_global_magnitude.gd` (282–310), `sim/kc2rt_fight.gd` (276, 1595–1615, 1715–1735, 5706–5720, 7660–7668), `sim/kc2rt_roster.gd` (1719–1721), `tests/kc2rt_completion_probes.gd` (639–648).
- KP-310 evidence: `reincarnated-godot/evidence/kc2-play/2026-10-07-g3-25cell-kp310-V311FULL-256b3e4/`, `…-ta-preread-kp310-472cffc4-cells/`, `…-kp310-s47-build/`.
- Oracle (sealed `969fbd8d`): `kc2/offense.py` 125–150, 340–430, 455–485, 600–710; `kc2/threat.py` 345–366, 925–965, 1183–1190, 2015–2160; `kc2/gd_composition.py` 15–30, 125–180; `simulation/scripts/gamora_join1_obs1_guard_2026_10_02.py`.
- KC-1b: `reincarnated-engine/src/reincarnated/simulation/kit_compiler/kit_compiler.py` (`resolve_element`, `_has_conversion_row`), `tests/test_kit_compiler_join1_kc1_kc3.py`, `simulation/math/join1-b0n-numeric-selfjoin-2026-10-06.md` § 7; decisions-log `design/decisions/decisions-log.md` (2026-10-06 KC-1, clause 5 + Status).
