# Finding — 2026-10-02 — JOIN-1 J0-F oracle half (J-S8 `join1-gm-fixture-v1/oracle`, re-frozen at v3.11)

**Reviewer:** jack-ryan (DEV-MODE, Gate-2)
**Severity:** **PASS-WITH-FINDINGS.** No BLOCK. No re-freeze is owed: all four § C2 readings are ACCEPTED. 4 WARN, 4 INFO. The WARN-3 ruling is in § 5.
**Target:** engine `43b033d6`, MANIFEST of record `f82807fb6de68a6cee4eff69bb7028457143b4951fe9abccee94caa735c4d217` (it supersedes `7088cd54…` at `f4a9948e`). Emitter `acba3ac5` (FILE `2382e5b0…`). Oracle tag `kc2/referent-v1-oracle-candidate-v311` → `969fbd8d` (kc2 tree `7496a28a…`). OBS-1 guard `9c756081` (FILE `5f3f4f1e…`). Instruments: J-P2 + ADDENDUM-1/-2/-3 (`2f90c3b5`)/-4 (`c5bea1a2`).
**Developer:** gamora (oracle half). Conductor: gandalf (KP-242, KP-245).
**Principles applied:** REVIEW_PROCESS 1 (math before code), 2 (smoke gate / reproduction), 3 (cross-seam impact: the port half), 4 (committed truth: prereg v1.15 TA-X-30 and Matt Q104), 5 (severity matters).
**Instruments (sibling folder, committed with this file):** `2026-10-02-join1-j0f-oracle-half-gate2/jr_rowset_rederive.py` (an independent ROWSET law implementation that imports nothing from the emitter) and `jr_control_check.py` (a per-cell, per-grain diff of the recorded control outputs against the frozen fixture, independent of gamora's `cmp.py`). Their outputs are saved there as `out_rederive_fixture_vs_reemit.json`, `out_control_check.json` and `out_reemit_summary.log`. Disk stayed at 25–29 GiB free throughout, above the 20 GiB HALT.

---

## 1 · Reproduction: what I re-derived myself, and what I only re-read

| claim | how I checked it | result |
|---|---|---|
| **7 ROWSETs**: G1 `725cbe3d…` · G2 `ec0b1af5…` · G3 `46c18ed8…` · G4 `ee431329…` · G5 `0757ec07…` · G6 empty `e3b0c442…` · G7 `69a7e00e…` | **INDEPENDENTLY RE-DERIVED** from the stored grain files with my own implementation of the manifest's printed `rowset_law`: f64 bit patterns, KEY sort, `,`/`:` separators, no trailing newline. G2 was gunzipped first | **7/7 equal.** FILE digests 7/7 equal. Row counts 56,511 / 105,045 / 250 / 117,695 / 25 / 0 / 250. Key tuples unique in every grain. Every non-empty grain has rows in all 25 cells |
| **The fixture is what the oracle emits** (re-emission) | **INDEPENDENTLY RE-EMITTED.** I made a fresh worktree of the pushed tag (HEAD `969fbd8d`, kc2 OID `7496a28a…`, clean) and ran the committed emitter (`2382e5b0…`) as a DRY run with `--inertness` on all 25 cells. Then I compared it by both my re-deriver and the manifest digests | **REPRODUCED.** 25/25 cells, 0 failed, wall 368.5 s. **All 7 ROWSETs and all 7 FILE digests are byte-equal to `f82807fb`'s** (checked with my re-deriver, not only the emitter's own print). Same row populations. `foreign_reads=0` on 25/25 hooked cells. The worktree was still clean after the run (`git status --porcelain` empty). Evidence: `out_rederive_fixture_vs_reemit.json`, `out_reemit_summary.log` |
| **Inertness**: bare == hooked | the re-emission's own `--inertness` pass (a fresh interpreter per cell, no hooks) | **REPRODUCED: 25/25 equal** |
| **OBS-1 completeness** under the shared guard | the re-emission applies `cell_check` from `9c756081` verbatim | **REPRODUCED: 25/25 complete** |
| G5 terminals equal star-lord's graded V311-FULL (one w160 death per arm) | read from G5: 5 `player_death` / 20 `survived_window` | consistent. I did not re-run star-lord's graded harness |
| Re-freeze changed the manifest only | the re-deriver confirms that the `7088cd54` frozen copy (gamora's scratch `j0f/frozen_7088`), the round-trip `out_RT`, the guarded verification `out_GV` and `f82807fb` carry identical ROWSETs on all 7 grains | confirmed |
| WARN-1 population | recomputed from G1: min `pth_used` 67.72363776155538, min `pth_raw` 66.80545402122416, 129 below 70, **0 below 55**, `pth_effective == pth_used` on 56,511/56,511 | equal to the manifest |
| G4 totals | recomputed: Σ`n_bodies_halted` = 253,753; Σ`n_bodies_halted_beyond_d_engage` = **0**; `max_halt_distance_m` is **null on all 117,695 rows** | equal to ADDENDUM-3; see INFO-2 |
| 12 distinct trajectories | **INDEPENDENTLY RE-DERIVED** as a per-cell digest over every row of every grain with the `arm` column removed | **exactly 12 classes**, with membership as ADDENDUM-3 § C1 states (§ 6) |

**Not independently re-derived:** the NC-2 sub-claims about the first physical row having no overflow region and the Resilience-window coupling (I verified only that G2 and G3 are RED in 25/25), and the § C1 G2 stage identity (my ADDENDUM-2 re-check reproduced it at `22cd2288`; I did not repeat it on V311).

⚑ **A reproduction hazard, found by failing first (INFO-1).** My first re-emission sat in a scratch directory and **all 25 cells refused** with `RingSubstrateError: Lap Z artifact ABSENT: <worktree-parent>/reincarnated-collaboration/…/pm4z_findings.md`. The oracle resolves its 14 pinned collab inputs **relative to the worktree's parent directory**, so a worktree that is not a sibling of `reincarnated-collaboration` cannot run. **The refusal is loud and correct** (14 content-pinned inputs, refuse-on-absent). The rerun used a sibling symlink to the real collab repo, and the emitter's content check (each read's digest must appear in the sealed source) still binds. The log of the failed attempt is kept beside the rerun in my scratch area. It matters for drax and for any third-party reproducer: **the run is location-sensitive, and nothing on the manifest says so.**

---

## 2 · The four NEW § C2 readings, checked against prereg v1.15 `TA-X-30` (Matt Q104, KP-240)

v1.15 § F.2i′ is the controlling text. It restates TA-X-30 on **the step's own operand**, and it defines (b′) R-G4-V311 as *"distinct roster bodies with at least one player-targeted, **non-waypoint, non-hold, non-emerging** step that `ArenaFold.clamp_body` stopped with pre-step distance **> that step's own `op`**."* Its operand table gives Attack `op` = the current centre distance, Pursue-without-waypoint `op` = reach × (1 − 1e-9), waypoint `op` = 0, and no-state `op` = 2.4.

| § C2 reading | v1.15 | verdict |
|---|---|---|
| **(i)** a waypoint-aimed step is not a pursuit step | (b′) says **"non-waypoint"** in so many words. (a′) still governs the waypoint step's travel with `op = 0` and the target set to the waypoint, but (a′) is TA-X-30's travel law, not G4's halt count | **ACCEPTED.** Identical exclusion. ⚑ **Its stated rationale is wrong, and a reader should know it (WARN-A, § 7).** ADDENDUM-3 justifies (i) as *"a body standing at its slot point is not halted by the engagement law."* ADDENDUM-4 § D1 then measured that most waypoint returns are **intercepts placed where the body first comes within reach of the player** (8,884 intercepts against 6,579 fixed points at M-POL-2/0). So (i) excludes the very mechanism that halts a pursuing body near the player. The reading still stands, because v1.15 draws the same line and the operational definition is unambiguous. But what it measures has to be said plainly (next row) |
| **(ii)** the operand is the step's own `d_engage_m`, literally, so a body in GD Attack counts as halted | the table row *"GD state Attack · op = the current centre distance"*, with *"halt ⇔ dist − op ≤ 0 (inclusive, exact)"* | **ACCEPTED.** Verified bit-safe: `halt_for` returns `math.hypot(player_xy[0] − body_xy[0], player_xy[1] − body_xy[1])`, and the emitter's recomputed distance uses the same operand order on the same tuples, so `dist − op` is exactly 0 and never 1 ulp positive. ⚑ **Named consequence, measured (WARN-A):** at M-POL-2/0, Σ`n_bodies_halted` = **9,032** = the cell's count of Attack-stand steps (`n_other` 9,032). Every pursue-branch step is waypoint-aimed (22,573 = 22,573), and 0 halts are counted at 2.4. **On this baseline, G4 `n_bodies_halted` is therefore exactly a per-tick census of roster bodies in GD's Attack state.** The ring-halt law contributes nothing independent to it. That makes it a useful join quantity: the port's GD state machine must agree with the oracle's tick by tick. But the field name says "halted", and the manifest's `R-G4` text (still ADDENDUM-2's) does not say what it now counts |
| **(iii)** stationary bodies count when the ring clip binds | v1.15 defines no `n_bodies_halted`. (a′)'s halt flag is computed on every player-argument step, holds included, so counting the literal flag is consistent. **But (b′) excludes holds**, and the stationary plant is listed among them | **ACCEPTED for `n_bodies_halted`.** ⚑ **INFO-3, a definitional delta that is UNREACHABLE on V311-FULL:** the emitter's beyond-count predicate excludes `alert_hold` and `mech_hold` but **not** `stationary_hold_active_step`. v1.15 (b′) excludes all holds. The delta cannot fire: a stationary body's travel is zeroed, so its post-step position equals its pre-step position, and `clamp_body` returns True only for a centre beyond `r_wall`, where the spawn scatter's support ends by construction. G4 beyond is 0 on every row. The port must still mirror **the emitter's** predicate, not (b′)'s, or the two harnesses define different fields |
| **(iv)** emerging bodies are never counted | (b′) **"non-emerging"** | **ACCEPTED.** The emitter relies on the oracle's verdict: `is_player_tgt` is False while emerging **because** `emerge_acquires = False`. That holds on V311-FULL (`P05EmergenceFold(bound=LONG)`, default `acquire_during_emergence=False`). It would not hold under the v3p8 `"A3"` audit configuration (`acquire_during_emergence=True`). There the emitter would count emerging bodies, because it has no explicit `emerge_hold_active_step` exclusion. Same class as INFO-3: unreachable here, and to be closed in the predicate at the next re-freeze |

**C2 item 5** (beyond-count = definition (i) + operand (ii)) matches (b′) except for INFO-3. Its grain differs: G4 counts per-tick body steps, while (b′) counts distinct bodies. **At zero the two are equivalent**, and zero is the only value either has taken.

**Ruling: § C2 (i)–(iv) ACCEPTED; no re-freeze.** WARN-A and INFO-3 are recorded corrigenda for the next freeze's face. They are not grounds to re-freeze, because neither changes a single emitted value.

---

## 3 · Controls: was each prediction committed before its run?

The commit times are git's. The run windows come from gamora's scratch outputs (`…/scratchpad/j0f/`): each log's mtime minus the run's own printed `wall=`, cross-checked against the output directory's birth time.

| control | prediction committed | run window | emitter of the run | before? | outcome (my `jr_control_check.py` vs the frozen fixture) |
|---|---|---|---|---|---|
| NC-M | ADDENDUM-3 `2f90c3b5` 16:47:46 | 16:55:39 | — | ✅ | `JOIN1-HALT provenance: HEAD is not the seal commit`: refused at limb 2, as predicted |
| NC-1′ | 16:47:46 | 16:55:49 → 16:58:41 | `a12c4af2` (`f4a9948e`) | ✅ | G1 RED **25/25**. First G1 divergence ticks at M-POL-2 /0..4 = **1531 · 519 · 191 · 695 · 658**, exactly as predicted |
| NC-2 | 16:47:46 | → 17:01:44 | `a12c4af2` | ✅ | G2 RED 25/25, G3 RED 25/25 |
| NC-3 | 16:47:46 | → 17:04:25 | `a12c4af2` | ✅ | GREEN 25/25 on all 7 grains (vacuous, as predicted) |
| **NC-3b** | 16:47:46 | 17:04:26 → 17:07:34 | `a12c4af2` | ✅ | **GREEN 25/25 on all 7 grains: the MISS is real** |
| NC-4 | 16:47:46 | → 17:08:22 | `a12c4af2` | ✅ | `raised:KeyError` 25/25; OBS-1 0/25 |
| NC-4b | 16:47:46 | → 17:10:21 | `a12c4af2` | ✅ | `raised:KeyError` 25/25; OBS-1 0/25. First divergence after w152's end (M-POL-2/0: G4 at tick **871**, against a predicted 870-tick w151+w152; M-POL-2/3: **1239** against 1238) |
| **NC-3c** | **ADDENDUM-4 `c5bea1a2` 17:18:15** | **17:18:25 → 17:21:22** (dir birth 17:18:25; wall 176.9 s) | `d26f5750` = `d46eefe4`'s emitter, which itself landed at 17:18:15 | ✅ **by 10 s** | G4 RED **25/25**; beyond **0** on every row; first G4 divergence ≤ first G1 divergence in **25/25**; OBS-1 25/25. Every element of the prediction held |

The only work between the NC-3b miss and the ADDENDUM-4 commit was `diag_halt.py` (17:15), a baseline mechanism count with no perturbation, and two single-cell baseline smokes (`smk3`/`smk4`, M-POL-2/2, `control=None`) for the OBS-1 guard. **No run of the NC-3c perturbation preceded its prediction.**

**Ruling on the NC-3b → NC-3c replacement: SOUND PRACTICE. It STRENGTHENS the control set rather than weakening it.** Reasons:
1. The miss is **recorded as a miss**, with its mechanism measured after the fact and labelled as such. It was not re-parameterised, not re-run and not dropped (ADDENDUM-4 § D1). That is the honest form, and it is what J-P2 § 5's "an instrument that has never failed has not been shown to be able to" requires of the controls themselves.
2. The replacement's prediction was committed **before** its run (verified above). It targets a **different, explicitly named site**, `_stop_where_close_enough`'s R, chosen because the miss proved the old site unreachable. That is a new hypothesis tested fresh, not a re-roll of the same one.
3. The miss carries **information the set did not have before**: under V311-FULL, the pursue reach `halt_for` returns never reaches a `Mover.step`. That fact sharpens § C2 (WARN-A) and agrees independently with Q104's TA-X-30 finding.
4. **What would have weakened it, and did not happen:** replacing NC-3b silently, re-running NC-3b with a larger delta until it turned red, or counting NC-3c as the "same" control so the record shows 7/7 held. The ledger says 6 of 7 predictions held, plus a predicted-and-held replacement. **That count must stay in that form in every downstream citation (INFO-4).**

⚑ **INFO-4, an attribution caveat on NC-3c.** `_stop_where_close_enough` is a single static method with **two consumers**: the roster's `waypoint()` (line 651) **and** the pet melee path `pet_target` (line 763; `pets=True` in V310-FULL). So NC-3c moved roster **and** pet intercepts together. ADDENDUM-4's "nothing else moves" understates this. **G4 sensitivity is witnessed** (that was the control's job), but the witness does not isolate roster pursuit from pet placement. If a later gate needs roster-only sensitivity, the wrapper should branch on the caller. No action is owed for J-S8.

---

## 4 · WARN-1: the 55 floor is never reached

**Ruling: acceptable for J-S8's own claim. Not acceptable as the ONLY guard. A targeted control IS owed, and it is owed earlier than J3.**

- **Why it is acceptable for J-S8.** J-S8 certifies port ≡ oracle **on what the referent executes**. A branch the referent never takes cannot produce a difference on the referent, so the fixture is not wrong. It is silent there, and its face says so (`unexercised`, `warn1_recheck_v311`). The sub-threshold branch is now exercised (129 attempts), which is an improvement over `22cd2288`.
- **Why it is not enough.** The JOIN-1 charter's § 4.7 ORACLE/PLAY invariance is enforced by **this same fixture** (J-P2 § 6; charter BLOCK-B; "any change in `ORACLE` behaviour" is a HALT-to-Matt boundary). The most plausible way for D2 content to leak into `ORACLE` is the `pth_floor_pct` lever (D2 5 % vs GD 55). A floor leak is therefore invisible both to the golden master **and** to the HALT it exists to trigger. The blind spot sits exactly on the boundary the run was chartered to police.
- **The fix owed (WARN-1, carried, now with a target):** a **targeted G1-law probe**. Call `probability_to_hit` → `pth_used` → `max(·, PTH_MINIMUM)` → `resolve_hit` directly on a small declared grid that straddles the floor: `pth_raw ∈ {40, 54.999…, 55.0, 55.000…1, 60, 69.999…, 70.0}`, with a fixed set of rolls on each side of each value. Run it on the oracle at `969fbd8d` and freeze its rows (bit-equality, Limb A/B) beside J-S8 as a supplementary fixture. Its own negative control: `PTH_MINIMUM 55 → 5` must RED, with the predicted row count stated first. The port runs the same grid in `--draws` mode. **This costs seconds and needs no fight.**
- **Owner / when:** gamora authors and freezes the oracle grid (a J-P2 addendum, prediction first, D4). drax mirrors it on the port. **The conductor binds it as a precondition of the first § 4.7 invariance claim and of J2's Gate-2, not J3.** The J3 `pth_floor_pct` lever NC (my ADDENDUM-2 re-check, WARN-5) still stands, and its population must contain `pth < 55` or the NC is vacuous.

---

## 5 · ⚑ WARN-3 RULING: Limb C stays EMPTY. **Keep bit-equality on `pre_mitigation`; the port must match exactly.** No ulp exception is granted, now or after the v3.11 port diff.

**Recommendation: option 1, keep bit-equality,** with a defined remedy path and an escalation valve. It is not option 2 (a named, bounded ulp exception).

**Reasoning:**

1. **The standing native-shadow rule (KP-233) is the decisive precedent, and it points one way.** An FMA-contracted build produced **383 mismatching ticks and 0 G3 divergences**. Decision-level agreement could not see it; only bit-for-bit comparison could. Hence the rule: *every native build ships only after a shadow-mode bit-equality run.* A 1–2 ulp allowance on `pre_mitigation` is **exactly the band an FMA contraction or a re-association lives in.** Granting it would make J-S8 blind, on the damage path, to the defect class the project already learned it cannot otherwise detect. The Q103 compiled-port principle is spreading (contact solver, now pet placement), and the damage chain is a plausible next candidate. Once it is compiled, J-S8's G2 is the only instrument that would catch a contracted build.
2. **Bit-exact is demonstrated, not aspirational.** The compiled contact solver matched 202,572 values with 0 mismatches. The port already reproduces CPython-exact `hypot` and visit order. G1/G4/G5/G6/G7 were already EQUAL in KP-204. The residual is the last bit of one chain. J-P2 § 4's principle covers it exactly: *"a FORM/OPERAND separation is supposed to RELOCATE code, not RE-ASSOCIATE arithmetic."* A last-bit difference in a magnitude chain is a re-association, and re-associations are fixable.
3. **The KP-204 evidence is from a superseded chain.** The 4,783 rows came from the port's **om/Z5** chain against the `22cd2288` candidate. V311's composition law is **`CompositionFold`** (TA-X-29(b′), Matt Q98/Q104: `m · max(0, a + P + (f − 1))`, etc.). The port has to be re-ported to it in any case. **Any exception sized now would be fitted to an observed diff of a chain that no longer exists.** That is the WARN-16 shape twice over: a tolerance sized against a known result, and sized at the wrong mechanism.
4. **A pre_mitigation exception does not stay on pre_mitigation.** KP-204 already shows the knock-on: G3 moved by 1 ulp. A tolerance on `pre_mitigation` would have to cascade to `after_stage_1/2`, `applied`, G3 `intake_hp`/`heal_hp` and G5 `final_hp`. That amounts to a float tolerance over the whole damage path, which is precisely what Limb B exists to forbid. "No decision differs" is a fact about one run. It is not a property: `p ≤ armour` (absorb vs overflow), HP ≤ 0, and the leech caps are all threshold decisions a last bit can flip on some future input.
5. **The machinery does not exist.** The ROWSET is exact equality over every float. A Limb-C tolerance would need a row-level comparator, which does not exist and which would itself need a Gate (my ADDENDUM-2 re-check, WARN-3).
6. **Option 3 (record the summation order, `--draws`-style) was considered and not preferred.** Replaying the oracle's accumulation order into the port would need a new oracle-side emission, which means a re-freeze, and it would hide a genuine operation-order defect rather than fix it. It stays available as a fallback, behind the valve below.

**What this means operationally (the fix owed):**
- **drax (port, v3.11):** implement `CompositionFold` and the global-magnitude `om` chain with **the oracle's operand order and association, term for term**: left-to-right `+`, the same parenthesisation (`a + P + (f − 1)` is not `(a + P + f) − 1`), the same iteration order over any per-family set (CPython's, which is deterministic under `PYTHONHASHSEED=0`), `math.fsum` wherever the oracle uses `fsum`, and no FMA (`-ffp-contract=off` on any compiled piece, per KP-233). Diff in `--draws` mode. **Target: G2 and G3 bit-equal.**
- **Escalation valve (not a tolerance):** if a residual survives a term-for-term port and its mechanism can be **named** (for example, a CPython library function with no bit-exact Godot counterpart), it is a **finding routed to Matt**. It is not absorbed. Any exception then is a Matt ruling with the mechanism, the field, the ulp bound and the measured depth on the face, plus a declared decision-invariance clause (Limb A fields bit-equal). That is the WARN-16 HALT shape J-P2 § 4 already prescribes.
- **gamora / conductor:** no fixture change. The manifest's `limb_c_exception_list: EMPTY` stands as frozen. Record this ruling against KP-204 finding 2 in the ledger, so the port diff is read against it.

---

## 6 · Discriminating power: 25 cells, 12 trajectories

**Independently confirmed (my census, every grain, `arm` removed): exactly 12 classes.** `M0 ≡ M-POL-2-NULL` on all 5 salts. `M-POL-2 ≡ W1-NULL` on all 5 salts. `W1` joins that class on salts 0, 1 and 4 and departs **only on salts 2 and 3**. The equality is byte-identity of every row, not just equal counts. The inertness digests on the manifest show the same pairs.

**Is the manifest honest about it?** **Partly.** The disclosure is in ADDENDUM-3 § C1, which the manifest pins by FILE under `readings_authority`. Nothing on the face claims 25 independent witnesses, and J-P2 § 4 Limb D (per-cell diff, no aggregate gate, effective n = 5) already guards the statistical misuse. **But the manifest face itself says nothing**, and a reader of `manifest.json` alone sees 25 cells (WARN-B).

**Does it matter for J-S8 as the join golden master? Mostly no, in one place yes.**
- **No** for the core claim. The golden master diffs **per cell**. A duplicated trajectory costs a redundant comparison, not a false green. Every grain is still compared on 12 genuinely distinct fights.
- **No** for the arm NULLs, which is actually a strength. `M-POL-2-NULL ≡ M0` and `W1-NULL ≡ M-POL-2` are **predicted identities** (a constructed-but-disarmed fold equals its absence). The fixture witnesses them byte for byte, so a port whose disarmed `ChannelPolicyFold` or `ArenaFold` leaks behaviour will RED.
- ⚑ **Yes for W1's armed wall and for G4's beyond-limb.** W1's armed `ArenaFold` is distinguished from its NULL on **2 of 5 salts**. G4 `n_bodies_halted_beyond_d_engage` is **0 on every row** and `max_halt_distance_m` is **null on every row** (117,695/117,695). **A port that hard-codes beyond = 0 and max_halt = null passes J-S8.** v1.15 prints this vacuity on TA-X-30(b′)'s face by Matt's Q104(1) ruling. J-S8's `unexercised` block names G6 and the G1 floor but **not these two G4 fields (WARN-B).** For the TA-X-30(b′) limb, the J-S8 golden master is therefore no stronger than TA-X-30 itself: tested on W1 only, and vacuous everywhere it is zero.

---

## 7 · Findings register

| id | sev | finding | fix owed · by whom |
|---|---|---|---|
| **WARN-A** | WARN | § C2 (i)'s rationale ("slot point") is contradicted by ADDENDUM-4 § D1 (most waypoints are reach intercepts). Under (i)+(ii), G4 `n_bodies_halted` is **exactly** a per-tick GD-Attack census on this baseline, and the manifest's `R-G4` text (ADDENDUM-2's) does not say so | **gamora:** ADDENDUM-5 (corrigendum, D4) re-stating (i)'s rationale as *"(b′) draws the same line; the intercept halt is observed one tick later as the Attack stand"* and naming the census identity. Carry it into `readings.R-G4-V311` at the next freeze. **No re-freeze for this alone** |
| **WARN-B** | WARN | The manifest face omits (a) the 12-trajectory collapse and (b) G4 `beyond` ≡ 0 and `max_halt_distance_m` ≡ null on every row (UNEXERCISED-IN-REFERENT-V1). A hard-coding port passes those fields | **gamora:** declare both in ADDENDUM-5 now. Put them on `unexercised` (and a `distinct_trajectories: 12` field) at the next freeze. **conductor:** any J2/J5 citation of J-S8 as TA-X-30(b′) evidence prints *"vacuous outside W1; 2/5 W1 salts distinct"* |
| **WARN-1** (carried) | WARN | The 55 floor is unexercised; a D2 floor leak passes J-S8 **and** the § 4.7 invariance HALT that relies on it | **gamora** (oracle grid + NC, prediction first) · **drax** (port grid, `--draws`) · **conductor**: bind it before the first § 4.7 claim and J2 Gate-2 (§ 4) |
| **WARN-3** (ruled) | WARN | Limb C EMPTY; port 1–2 ulp `pre_mitigation` is RED | **RULED § 5: bit-equality stands.** **drax**: term-for-term V311 port, no FMA. Valve: a named irreducible residual goes to Matt, never to a tolerance. **conductor**: record against KP-204 F2 |
| **INFO-1** | INFO | The run is location-sensitive: the oracle resolves 14 pinned collab inputs relative to the worktree's parent | **gamora**: one line in ADDENDUM-5 ("the worktree must be a sibling of `reincarnated-collaboration`"). **drax**: note it in the port sidecar's reproduction recipe |
| **INFO-2** | INFO | G4 beyond = 0 and max_halt null everywhere (the evidence for WARN-B) | — |
| **INFO-3** | INFO | The emitter's beyond predicate omits `stationary_hold` and does not explicitly exclude `emerge_hold`; v1.15 (b′) excludes both. Unreachable on V311-FULL | **gamora**: add both exclusions at the next re-freeze (no grain changes, since beyond ≡ 0). **drax**: mirror the emitter's predicate as frozen |
| **INFO-4** | INFO | NC-3c perturbs roster **and** pet intercepts (one static method, two callers). The tally must stay "6 of 7 held + NC-3c predicted-and-held" | **conductor**: keep the count in that form in downstream citations |

**Matt:** nothing is escalated by this finding. WARN-3 is ruled within my Gate-2 authority (it keeps a frozen default and adds no tolerance). Matt's attention becomes due only if drax's v3.11 port leaves a named, irreducible residual (the valve in § 5).

---

## References

- Fixture: `reincarnated-engine/src/reincarnated/simulation/output/join1-gm-fixture-v1/oracle/` (manifest `f82807fb…`)
- Emitter: `reincarnated-engine/src/reincarnated/simulation/scripts/gamora_join1_gm_emit_2026_09_29.py` (`2382e5b0…`; NC-3c ran under `d26f5750…` = `d46eefe4`)
- OBS-1 guard: `…/scripts/gamora_join1_obs1_guard_2026_10_02.py` (`5f3f4f1e…`)
- Oracle at `969fbd8d`: `kc2/run.py` 2366–2385, `kc2/gd_engagement.py` 199–213, `kc2/gd_reposition.py` 640–672 / 745–764, `kc2/locomotion.py` 1163–1240, `kc2/arena_fold.py` 278–304, `kc2/p05_emergence.py` 67/143
- Instruments: `…/simulation/math/kc2-join1-golden-master-instrument-2026-09-29.md` (§ 4, § 5, § 6) and ADDENDUM-2/-3/-4
- Prereg v1.15 § F.2i′: `reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-ta-prereg-v1.15.md`
- Ledger: `…/gandalf/notes/2026-09-20-kc2-play-run-charter.md` KP-204, KP-233, KP-242, KP-245. JOIN-1 charter § 4.3 / § 4.7 / BLOCK-B
- Prior: my ADDENDUM-2 re-check `2026-10-01-join1-jp2-addendum2-recheck.md` (`28bacbb7`); J0/J1 Gate-2 `2026-10-02-join1-j0-j1-gate2.md` (`29124a46e`)
- Control outputs re-checked: gamora scratch `…/scratchpad/j0f/out_NC-{1,2,3,3b,3c,4,4b}`, `out_RT`, `out_GV`, `frozen_7088`, `ncM.log`
