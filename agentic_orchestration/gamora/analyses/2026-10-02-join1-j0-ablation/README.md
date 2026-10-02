# JOIN-1 · J0: the ablation map, oracle side (v3.11, scripted pilot P-MOVE)

**NOT-A-GRADED-RUN. Print-only, and never a T-A artifact. Nothing tuned. No oracle behaviour change.**
gamora, 2026-10-02, Run JOIN-1 (charter v0.6 § 4.1 / § 5 J0; KC2 KP-229). Gate: jack-ryan Gate-2 on the classification and on the E-2 candidate. Neither may be quoted until that gate passes.

- Pre-registration (committed alone, before the harness existed): engine `0a3e0a0e`, `simulation/math/kc2-join1-j0-ablation-j1-selfjoin-prereg-2026-10-02.md` §§ 1–4
- Harness: engine `6227374a` + table amendment `1e4e00be` (see § Corrections), `simulation/scripts/gamora_join1_j0_ablation_map_2026_10_02.py`. It imports `gamora_kc2_play_v3p11_oracle_2026_10_02` unmodified.
- Per-family runs: `runs/<family>.json` (51 files, incl. CONTROL). Table: `ablation_table.json` (re-emitted under the OBS-1 guard; stdout `table_stdout.txt`). Launcher log: `run.log`.
- **J0-B1 discharge (2026-10-02, after jack-ryan's Gate-2, collab `29124a46e`; Matt "Correct and continue", KP-237):** the completeness guard `simulation/scripts/gamora_join1_obs1_guard_2026_10_02.py`, the salt-4 forensics `diag/A-SECOND_salt4.json`, and the fold-report witnesses `witness/{CONTROL,A-COMP-DOT}.json`. See § OBS-1 and § Corrections.

## Control reproduces pass 4 (prereg § 1 gate: PASSED)
`CONTROL` (`V311-FULL`, arm M-POL-2, salts 0–19) gives **×1.0713**, with leg-A terminals at salts 2/10/15/18 (w160). This is pass 4's `pw_A` figure exactly.

Two cross-checks against pass-4 configurations computed by a different route also hold. `A-MUT` (the mutator keyword removed at the boundary) = **×0.9351** = pass-4 `LU`. `A-LINEUP` = **×2.1233** = pass-4 `MUT`. So the boundary-removal instrument and the oracle's own configuration switches agree to the fourth decimal.

## ⚑ Read this before the table: what "removed" means
A keyword removal restores `simulate_wave`'s **signature default**. For the v3.8–v3.11 folds, the default is **absent**. **For several base folds, the default selects the LEGACY pre-fold branch, not "no mechanism".** Examples:
- `A-SUSTAIN`: healing still lands, and more of it (heal 12.67 M vs 12.00 M).
- `A-DEF`: `defenses_enabled=False` takes the pre-defence path.

Those rows measure **"this fold vs its legacy branch"**, not "this mechanism vs nothing". The direction of a base-fold row is therefore not a sign of the mechanism's own effect. The rows affected are A-GMAG, A-MBOARD, A-DEFER, A-VOLLEY, A-SUSTAIN, A-SECOND, A-KITRES, A-DOTTL, A-CC, A-PETS-PLAYER, A-ALERT, A-PATROL, A-COUNTER, A-DEF and A-SEP.
- `A-SEP` restores `block` / `resolve_then_separate` / `jacobi4`: **a different contact model, i.e. a SUBSTITUTION** (like A-LINEUP), not an absence.
- `A-MBOARD` restores I-13's certainty override (hit = 1.0) **and** drops M1/M1b/M2's attribute and own terms on the 321 previously halted actors: its −0.363 is **the net of two opposite limbs**, not one mechanism's sign. The pre-registered rule (§ 2) defined removal this way. The interpretation is named here, after the fact, so it is not buried (#12).

## ⚑ The metric set is narrower than charter § 2.5 (J0-W2, stated, not patched)
The rule classifies on **four** metrics: ratio, leg-A deaths, mean wave duration, heal:intake (disc occupancy and the pilot's moving fraction are reported, never classifying). **HP occupancy and energy excursion / ceiling duty were not measured** in these runs, and no threshold was pre-registered for them; adding them would mean re-running every cell, so the narrowing is stated instead. **Every INCIDENTAL below reads "incidental on the four classifying metrics"**, and energy is exactly the axis on which the kit-internal families (kit residual, initial self-cast, resource economy) would show.

## Completeness (OBS-1 guard, applied to every row)
A cell is COMPLETE only if every salt banked 10 rows (w151–160), w160 did not end at the tick cap, the cell holds 9·N rows on w151–159 and the summed time matches. Otherwise it is **TRUNCATED** and classes NOT-ABLATABLE-ALONE, whatever `raised` says. On the 51 committed runs (read-only summary form of the guard): **49 complete; A-SECOND truncated (salt 4); A-MECH 0 rows.** Every other cell banks 180 rows on w151–159.

## The table (20 salts, paired; Δ against the control)

Columns: ratio = landed hp/s w151–159 / 1605.6 · dead = leg-A deaths of 20 (all in w160 unless marked) · legB = leg-B deaths per salt · wave_s = mean wave duration w151–159 · heal:in = Σheal/Σintake w151–159 · disc = bodies per tick in the disc · mov = the pilot's moving fraction.

| family | class | ratio | Δratio | dead | Δdead | legB | wave_s | heal:in | disc | mov |
|---|---|---|---|---|---|---|---|---|---|---|
| **CONTROL** | | **1.0713** | | **4** | | 0.20 | 39.38 | 0.9845 | 1.114 | 0.826 |
| A-LINEUP ⚑substitution | LOAD-BEARING | 2.1233 | +1.0520 | 20 (151–160) | +16 | 2.60 | 41.70 | 0.9277 | 1.674 | 0.843 |
| A-MUT | LOAD-BEARING | 0.9351 | −0.1362 | 2 | −2 | 0.10 | 38.74 | 0.9868 | 1.023 | 0.825 |
| A-MUT-BC | LOAD-BEARING | 0.9327 | −0.1386 | 2 | −2 | 0.10 | 39.13 | 0.9871 | 1.116 | 0.826 |
| A-MUT-LEECH | INCIDENTAL | 1.0841 | +0.0128 | 4 | 0 | 0.20 | 39.00 | 0.9826 | 1.091 | 0.822 |
| A-MUT-CRUEL | INCIDENTAL | 1.0265 | −0.0448 | 3 | −1 | 0.15 | 38.83 | 0.9807 | 1.041 | 0.827 |
| A-MUT-RA | LOAD-BEARING | 1.1730 | +0.1017 | 4 | 0 | 0.20 | 39.48 | 0.9810 | 1.122 | 0.824 |
| A-ENG | LOAD-BEARING | 1.2406 | +0.1693 | 11 | +7 | 0.55 | **23.14** | 0.9849 | 1.493 | 0.836 |
| A-ENG-REPOS | LOAD-BEARING | 1.1649 | +0.0936 | 3 | −1 | 0.15 | 40.28 | 0.9611 | 1.012 | 0.826 |
| A-ENG-PERSIST | INCIDENTAL | 1.1134 | +0.0421 | 5 | +1 | 0.25 | 39.77 | 0.9831 | 1.151 | 0.824 |
| A-ENG-RFA | LOAD-BEARING (c: wave +11.8 %) | 1.0676 | −0.0037 | 5 | +1 | 0.25 | 44.01 | 0.9775 | 1.011 | 0.824 |
| A-ENG-PETS | LOAD-BEARING | 1.1630 | +0.0917 | 6 | +2 | 0.30 | 39.41 | 0.9876 | 1.141 | 0.822 |
| A-ENG-SLOTS | LOAD-BEARING | 1.1882 | +0.1169 | 2 | −2 | 0.10 | 36.36 | 0.9756 | 1.101 | 0.823 |
| A-ENG-CROWD | INCIDENTAL | 1.0333 | −0.0380 | 5 | +1 | 0.25 | 37.17 | 0.9818 | 1.106 | 0.822 |
| A-PILOT ⚑pilot sensitivity | LOAD-BEARING | 0.9683 | −0.1030 | 7 | +3 | 0.35 | 45.43 | 0.9872 | 0.937 | **0.737** |
| A-SP (swing pause) | LOAD-BEARING (b: deaths +7) | 1.1070 | +0.0357 | 11 | +7 | 0.55 | 39.62 | 0.9817 | 1.093 | 0.824 |
| A-C11B | LOAD-BEARING | 1.0156 | −0.0557 | 2 | −2 | 0.10 | 39.34 | 0.9862 | 1.111 | 0.823 |
| A-INIT | INCIDENTAL | 1.0255 | −0.0458 | 5 | +1 | 0.25 | 39.87 | 0.9794 | 1.123 | 0.825 |
| A-EM-LAT | INCIDENTAL | 1.0812 | +0.0099 | 5 | +1 | 0.25 | 39.38 | 0.9849 | 1.126 | 0.826 |
| A-COMP-DOT | **INERT** (witnessed: 0 opportunities, see § Corrections) | 1.0713 | 0 | 4 | 0 | 0.20 | 39.38 | 0.9845 | 1.114 | 0.826 |
| A-FR (fire range) | LOAD-BEARING | 1.0180 | −0.0533 | 3 | −1 | 0.15 | 33.01 | 0.9591 | 1.248 | 0.824 |
| A-FR-BANDAURA | NOT-ABLATABLE-ALONE | — | | | | | | | | |
| A-EM (emergence) | INCIDENTAL | 1.1284 | +0.0571 | 4 | 0 | 0.20 | 37.71 | 0.9866 | 1.124 | 0.823 |
| A-STAT | INCIDENTAL | 1.1292 | +0.0579 | 7 | +3 | 0.35 | 36.27 | 0.9786 | 1.231 | 0.824 |
| **A-COMP (composition)** | LOAD-BEARING | **1.5651** | **+0.4938** | 12 | +8 | 0.65 | 37.45 | 0.9497 | 1.153 | 0.825 |
| A-C11A (all C-11a) | INCIDENTAL | 1.0610 | −0.0103 | 3 | −1 | 0.15 | 39.41 | 0.9843 | 1.118 | 0.827 |
| A-C1 (retaliation gate) | **INERT** | 1.0713 | 0 | 4 | 0 | | | | | |
| A-C2 (auras/grants) | INCIDENTAL | 1.0610 | −0.0103 | 3 | −1 | 0.15 | 39.41 | 0.9843 | 1.118 | 0.827 |
| A-C4 (duration divisors) | **INERT** | 1.0713 | 0 | 4 | 0 | | | | | |
| A-POOL (pool lift) | LOAD-BEARING | 0.9071 | −0.1642 | 3 | −1 | 0.15 | 31.56 | 0.9961 | 1.443 | 0.841 |
| A-WINNER (winner surface) | **INERT** | 1.0713 | 0 | 4 | 0 | | | | | |
| **A-GMAG** (global magnitude) | LOAD-BEARING | **0.5381** | **−0.5332** | 0 | −4 | 0.00 | 38.69 | 0.9825 | 1.081 | 0.825 |
| A-MBOARD (measured board) ⚑net of two limbs | LOAD-BEARING | 0.7080 | −0.3633 | 3 | −1 | 0.15 | 38.84 | 0.9720 | 1.128 | 0.826 |
| A-DEFER | INCIDENTAL | 1.0497 | −0.0216 | 5 | +1 | 0.25 | 39.80 | 0.9855 | 1.110 | 0.825 |
| A-VOLLEY | **INERT** | 1.0713 | 0 | 4 | 0 | | | | | |
| A-SUSTAIN ⚑legacy branch | LOAD-BEARING (b: deaths −4) | 1.1125 | +0.0412 | 0 | −4 | 0.00 | 39.74 | 0.9912 | 1.111 | 0.826 |
| A-SECOND | **NOT-ABLATABLE-ALONE** (TRUNCATED: salt 4 stopped at w152, outcome=timeout at the tick cap; cause PILOT-CAPTURE, § OBS-1) | — | | | | | | | | |
| A-KITRES | INCIDENTAL | 1.0834 | +0.0121 | 3 | −1 | 0.15 | 39.50 | 0.9799 | 1.105 | 0.825 |
| A-DOTTL | INCIDENTAL | 1.1185 | +0.0472 | 1 | −3 | 0.05 | 39.09 | 0.9791 | 1.125 | 0.824 |
| A-CC | INCIDENTAL | 1.0579 | −0.0134 | 4 | 0 | 0.20 | 40.29 | 0.9845 | 1.103 | 0.827 |
| A-PETS-PLAYER (SummonFold presence/diversion; no summon damage exists in this model) | INCIDENTAL | 1.0655 | −0.0058 | 4 | 0 | 0.20 | 39.22 | 0.9830 | 1.097 | 0.825 |
| A-ALERT | INCIDENTAL | 1.1004 | +0.0291 | 4 | 0 | 0.20 | 39.75 | 0.9812 | 1.092 | 0.827 |
| A-MECH | NOT-ABLATABLE-ALONE | — | | | | | | | | |
| A-PATROL | LOAD-BEARING | 1.1566 | +0.0853 | 1 | −3 | 0.05 | 35.59 | 0.9843 | 1.197 | 0.828 |
| A-COUNTER (counterplay) | LOAD-BEARING | 1.2558 | +0.1845 | 8 | +4 | 0.40 | 40.08 | 0.9401 | 1.105 | 0.823 |
| A-DEF ⚑legacy branch | INCIDENTAL | 1.1137 | +0.0424 | 2 | −2 | 0.10 | 40.49 | 0.9826 | 1.129 | 0.828 |
| **A-SEP** (body separation) ⚑substitution | LOAD-BEARING | **1.5163** | **+0.4450** | 11 | +7 | 0.55 | **56.88** | 0.9951 | 1.253 | 0.821 |
| A-CHAN (M-POL-2-NULL) | INCIDENTAL | 1.0768 | +0.0055 | 3 | −1 | 0.15 | 39.41 | 0.9833 | 1.061 | 0.839 |
| A-SEAT (M0) | INCIDENTAL | 1.0768 | +0.0055 | 3 | −1 | (identical to A-CHAN) | | | | |
| ARENA-W1 (an addition) | INCIDENTAL | 1.0528 | −0.0185 | 3 | −1 | 0.15 | 40.14 | 0.9841 | 1.075 | 0.820 |
| ARENA-W1-NULL | **INERT** | 1.0713 | 0 | 4 | 0 | | | | | |

The per-row reasons (which of the rule's clauses a–e fired, and SE_paired) are in `ablation_table.json` → `rows[].why`.

**INERT** = per-salt ratios and leg-A terminals identical **at 4 dp** to the control (the comparison is on the 4-dp-rounded summary), not byte-identical runs (J0-I2).

**Counts (50 rows plus the control), corrected per J0-B1:** **21 LOAD-BEARING** (one is the pilot) · **24 INCIDENTAL, of which 5 are INERT** · **3 NOT-ABLATABLE-ALONE** (A-FR-BANDAURA refused; A-MECH 0 rows; A-SECOND truncated) · plus **2 arena arms** (W1 INCIDENTAL; W1-NULL INERT) reported for completeness. *(Was 21 / 25 / 2: A-SECOND moved from INCIDENTAL to NOT-ABLATABLE-ALONE. It is NOT re-classed LOAD-BEARING: the prereg has no clause for a non-clearing wave, and § 4's thresholds are not revised after a result.)*

**Near-threshold INCIDENTALs (J0-I3), so INCIDENTAL is never read as "absent from GD feel":** A-STAT (+0.058, +3 deaths, disc +10.5 %), A-EM (+0.057), A-INIT (−0.046), A-DOTTL (−3 deaths), A-ENG-PERSIST (+0.042).

## What it says for the kit↔world boundary (descriptive)
- **The world's magnitude chain dominates.** The order of effect is global magnitude (−0.53), composition (+0.49), separation (+0.45), measured board (−0.36), engagement (+0.17), counterplay (+0.18), pool lift (−0.16) and mutators (−0.14). Each moves the ratio more than every kit-side fold combined.
- **Kit-side rows, descriptively.** Kit residual (+0.012), DoT timeline, CC on the player and alert are INCIDENTAL on the four classifying metrics. Most are legacy-branch rows, so each says "GD's form ≈ the legacy form on four metrics", not "the mechanism does nothing" (A-DEF, for example, compares DefenceField against the sheet-average mitigation path, not defences against none). `A-PETS-PLAYER` (−0.006) measures the SummonFold's presence/diversion model, which by construction cannot deal damage, die or spend mana; **the player's pets as bodies in engagement slots are A-ENG-PETS, which is LOAD-BEARING (+0.092).** Secondary streams could not be measured alone (truncated, § OBS-1). **These magnitudes say nothing about INTERNAL vs BOUNDARY**, which is a classification by kind (charter § 2.1, Q86), not by load.
- **Swing pause moves deaths, not the mean.** Δratio is only +0.036, but leg-A deaths go 4 → 11: a w160 burst effect.
- **The C-11a layer reduces to C2 alone** (auras/grants, −0.010). C1 and C4 are inert (4 dp) on v3.11, and so are the winner surface, the volley fold, the composition DoT divisor and the disarmed arena fold. They are carried, but they do nothing on this path (#86). C1/C4 are triangulated (A-C11A ≡ A-C2); the DoT divisor is witnessed (§ Corrections).
- **The line-up row is a substitution.** Removing the referent's line-up returns the seed-9 board (×2.12, 20/20 dead from w151). It measures the line-up's choice, not an absence.

## E-2 checklist: CANDIDATE, amended per jack-ryan's Gate-2 § 2.2–2.3 (quotable once the conductor verifies J0-B1's discharge)

> **Scope (mandatory on the quoted face):** *Measured on one board (waves 151–160, the referent line-up, the P-MOVE scripted pilot, 20 paired salts) on four classifying metrics, oracle v3.11 frozen (Q102). LOAD-BEARING base-fold rows compare GD's fold against the pre-fold path; they are not absence tests. INCIDENTAL ≠ not part of GD's feel.*

The GD-native mechanisms classed LOAD-BEARING on this board:
1. **the global-magnitude fold, with its C-11b attribute limb.** Provenance: C-11b B (`monsterAttributePak`, Ultimate / 1 player, +10 % dex and int) is **DB-SOURCED-EXACT**; C-11b A is applied at its **DECLARED mean** (×1.010). The C-11b limb is a KC2 correction fold.
2. **the measured-board fold** (A-MBOARD): removes, together, M1/M1b/M2 (attribute and own terms on the previously halted actors), M3 (measured PTH) and M4 (retirement of the certainty override). **Its −0.363 is the net of opposed limbs**, not a "PTH / crit reading" effect.
3. GD composition (the additive own-term law);
4. **body separation (contact response): SUBSTITUTION** (GD's contact model vs the legacy block / jacobi4 model);
5. **GD engagement:** the family row (A-ENG), the reposition core (**A-ENG-REPOS, LB**), slots, pets in slots, and RFA (by wave duration). **Persist and crowd are INCIDENTAL limbs**; the item is not the whole family;
6. **fire range (reach), LB by wave duration (−16 %)** — clause (a) did not fire;
7. swing pause (by deaths);
8. counterplay;
9. patrol;
10. **pool lift: CONTENT, not mechanism** (like the line-up): `pool_lift.py` supplies 338 records' decoded **rows**, never profiles;
11. the Crucible mutators (Brutal/Corrupted, Resilient/Ascended);
12. the line-up (as content, not mechanism);
13. **player sustain, re-admitted, labelled:** GD's leech basis vs the incumbent applied-damage basis; LB by deaths at the threshold edge (−4/20). It is a legacy-branch row exactly like GMAG, MBOARD, PATROL and SEP. (The earlier exclusion as "not GD-native" was wrong: GD's coupled leech basis is GD-native.)

Excluded: the pilot (A-PILOT), which is the measuring instrument, not a GD mechanism.

## OBS-1 · TRUNCATED cells, and the A-SECOND cause: PILOT-CAPTURE
The composition stops a salt's ladder **by design** on any wave that ends neither cleared nor in a death (`upn4._overrides`, "a genuine model signal"). The summary layer reports such a salt with `raised=None` and no terminal, **i.e. as SURVIVED**. A-SECOND salt 4 is that case. `diag/A-SECOND_salt4.json` (the harness's print-only `diag` mode, one salt, oracle unmodified; it reproduces the committed per-salt ratio 0.1098) shows:
- **w151** cleared (40.0 s). **w152 ended `timeout` at the tick cap** (4000 ticks = 326.53 s). The ladder stopped; 2 rows banked.
- **The one surviving body that gates the clear** is champion `aetherialcorruption_h02` (443,554 HP, **res_physical 0** — killable, *not* immune). It is ring-halted at (−11.9, −3.2), **never contacted, 0 player hits**.
- **Two physically-immune hazard pets survive:** `trap_lightningspike_hero_a01` (res_physical 500, **res_bleeding 0**, no TTL). With the bleed rider removed nothing can kill them. They do not gate the clear, but **P-MOVE steers to the nearest LIVE body, pets included**: the pilot sat on pet0020 at (−20.0, −1.9) for the whole wave, **3,340 player hits, 0 applied**, with the champion ~8.2 m away, outside the 3.0 m disc.
- **Control (bleed on), same salt and wave:** the spikes die to the rider, the champion is contacted at 42.6 s and dies at 43.3 s (9 disc hits, 8 bleed ticks, 3 EoR2 hits, 1 pet hit); w152 clears in 44 s.

**So:** removing the bleed does leave physically-immune records unkillable, as jack-ryan's probable mechanism said, but they block through the **pilot's nearest-body bearing**, not through the clear gate. **PILOT-CAPTURE** is a failure mode in its own right (the P-MOVE live set includes immune hazard pets) and is recorded as such; it is not fixed here (oracle frozen, Q102).

## Corrections, observations and findings
- **OBS-1 (instrument silence in the base harness).** `A-MECH` refused at wave 151 with `ActorStateUnclassifiable` ("the mech block is absent…", A-3), which the oracle raises loudly as designed. Yet `c11.run_arm`'s `raised` field read **None**, with 0 rows. The J0 table caught it only because the ratio came back None. The harness amendment classifies a no-row cell as NOT-ABLATABLE-ALONE. The base harness's silence is a **finding against `gamora_kc2_c11_lethality_decomposition_2026_09_29.run_arm`** (my seam; recorded, not fixed in this wave, because that script is part of the oracle-of-record composition).
- **OBS-2.** `A-FR-BANDAURA` is refused by `InitialSelfCastFold` (it needs the aura rows of fire range). The band/aura limb cannot be removed while the initial self-cast is on: a dependency, recorded.
- **OBS-3.** `A-CHAN` and `A-SEAT` are byte-identical on v3.11, so the seat's only effect on this path is the channel policy.
- **Correction (harness).** After the runs, `classify()`/`table()` gained the no-row branch above (OBS-1). No run was repeated, and no threshold or rule changed.
- **Correction J0-B1 (harness, 2026-10-02).** The no-row branch caught only the 0-row face of OBS-1. It is generalised to the four-clause completeness guard (§ Completeness); the table was re-emitted over the 51 committed runs; **A-SECOND → NOT-ABLATABLE-ALONE with its cause printed**; no other cell changes class, and no threshold or rule changed. New runs persist the guard's per-salt result (`completeness`) on the run JSON. (A-SECOND's former `mean_wave_s` was also biased: it divided by 180 rows where 173 existed; moot now that the cell does not grade.)
- **Correction J0-W3 (witness).** `run_one_mod` now persists `fold_reports` (as `V11.run_one` does) and `fold_telemetry`. `witness/CONTROL.json` (re-run; reproduces ×1.0713, per-salt ratios and terminals identical) and `witness/A-COMP-DOT.json`: the hook took effect (A-COMP-DOT's composition report reads *"1.0 (divisor UNDECODED; DECLARED)"*, the control's *"int/200 + 1 (decoded)"*), and **in both, zero DoT rows reached the SlowChaos/SlowAether divisor branch** (no `n_dot_rows_chaos_aether_decoded` / `n_dot_rows_a_dur_undecoded` count; composition telemetry identical). **A-COMP-DOT is structurally INERT: zero opportunities on this board** (#86).
- **J0-I4.** `run.log` carries an `xargs: command line cannot be assembled` error; A-ENG and A-ENG-REPOS ran twice with **identical** results (a free determinism witness). The interleaved A-ENG-PERSIST / A-ENG-PETS stderr lines do not affect their run JSONs, which are complete.

## Halt check
No ORACLE behaviour change: no file under `simulation/kc2/` and no oracle-of-record script was edited, and every removal is a harness-level keyword or constructor change, restored in `finally`. Nothing tuned. Disk was 26 GiB free (`df -h`) at the run, above the 20 GiB line. **Nothing halts to Matt from J0 itself.** (The OBS-1 retro-audit found truncated salts in other artifacts; Matt ruled "Correct and continue", KP-237.)
