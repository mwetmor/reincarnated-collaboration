# KC2-PLAY · T-A GRADE OF RECORD, graded attempt 1 of 2 under prereg v1.12: verdict `STRUCTURAL`

> **STATUS:** CURRENT. W3 grade seat, Run KC2-PLAY (charter KP-175 / KP-176). **Author:** gamora (simulation seam), 2026-10-01. **Conductor:** gandalf.
> **Graded object:** drax's emission at godot `9b0ad0c`, `reincarnated-godot/evidence/kc2-play/2026-10-01-ta-attempt1-v1.12-cells/`. It holds 25 `cell.json`, `ta_manifest.json`, the raw stdout, the H-4 preflight and the MANIFEST. Every byte was read through `git show 9b0ad0c:<path>`, and each worktree copy was checked equal to its blob.
> **Graded against:** prereg **v1.12**, FILE `a0454776ab91d85f37fadffcb8886a498e1f498f208e0eb33b9d5a9797fc7854`, derived before any row was read. Also the rows it carries by reference from v1.8 … v1.11.
> **(L2) evaluation of record for `a9b756cd`:** jack-ryan's delta Gate-2 addendum (collab `c210b1979`).
> **Instrument:** `agentic_orchestration/gamora/analyses/2026-10-01-kc2-play-ta-attempt1-v1.12-grade/grade_attempt1_v1p12.py`. It writes `results.json` and the verdict file `ta_verdict_v1p12_attempt1.json` beside itself. Its stdout is kept as `run_stdout.txt`.
> **Authority:** grading only. **No expected value or tolerance was changed. No row was reclassified. The prereg was not edited.** Nothing graded was re-run. **K-7 held:** the sealed `[M-POL2]` cell was hash-verified (`ad61ad2a…`) and read by key for its census, and nothing else.

---

## § 0 · Integrity, derived before reading any row

| object | expected | **derived** | |
|---|---|---|---|
| prereg v1.12 | `a0454776…` | `a0454776ab91d85f37fadffcb8886a498e1f498f208e0eb33b9d5a9797fc7854` | ✓ |
| emission `MANIFEST.json` | `25e4e5bd…` (KP-176) | `25e4e5bd20dbd07e39a265d82b907a61cdd106b15713ed3b329d38dcf59f04ae` | ✓ |
| emission members | 28 | 28/28 sha256 and bytes match; blob = worktree; the tracked set is the members plus `MANIFEST.json` and `README.md` | ✓ |
| emission tree (pack law) | `ffaf9aab…` | `ffaf9aab32dd9cf5bc395c4c46b0634ffe03cdb8fa985607d2141688a3cc3a4f` | ✓ |
| `ta_manifest.json` | `d352293d…` | `d352293d90da0f73fecd41767a8def0cb31055aff2ecd00a4bbd8ef47bfbb4f9` | ✓ |
| **runtime tree** `kc2_runtime/` | `a9b756cd…` | `a9b756cddc4a046ca7a755e51d798158bb4cf84928ec1c12bfdb82c5e12165bb`; 82/82 member blobs; tracked set = member set; `kc2_runtime/` byte-unchanged from `0802ab1` (HEAD at the run) to `9b0ad0c` | ✓ |
| booking census (`tests/kc2rt_booking_census.gd`) | `cf49eefe…` (H-4) | `cf49eefec225b3d306d3773fe0e264b1c96739b1a2f1185a7706f71b527c2c24` | ✓ |
| G3 input `MANIFEST.json` | `90195c7c…` (KP-175) | `90195c7ca96e04263cfb289e667a1437fa6e16ad97be392c5fdb085b26f2c8a7` | ✓ |
| **model pack** (19 members, `pack_digest_law_exact`) | `48a4c94c…` | `48a4c94c165715d3f4f5db89c1278aa8439fbe1507c39dd555f7ce91d4636c96`; on-disk set = manifest set | ✓ |
| **reference pack** (7) | `1887257f…` | `1887257f5370443a1729fde2ff446579b1acc501dcd03679244297b541e3e5b1`; `cross_pin.model_pack_digest` = `48a4c94c…` | ✓ |
| POOL-466 / SWING-456 / NONSWING-10 | § PINS | 466 `33c886a1…` (both routes agree) · 456 `706a61d5…` · 10 `00b4cb0e…`, **recomputed here from the oracle** (`pool466`; `load_profiles` under a8 `IC7-A-0453`'s call) | ✓ |
| H-9 docs (5) · H-10 receipt | documents of record | all six FILE digests reproduce | ✓ |

**C1 conformance (§ B.1a, § G).** Each arm's `arm_config_a8.rowset` equals § B.1a's ROWSET. `setup_config_rowset` equals the C-part ROWSET `207ab21f…`. `setup_probe_rows_applied` is 0 on all five arms. **G3 PASSES on 25/25 cells at the graded digest:** `injected: []`, 0 decision divergences, 0 draw mismatches, no port-only stream, only the two declared oracle-only streams, and death wave and tick equal. **No arm is non-conforming**, so every graded row is graded on a conforming arm.

**The runtime's identity rests on two things.** First, drax's MANIFEST attestation: the tree was recomputed before and after the run. Second, my recomputation of the tree at the evidence commit. No cell carries the runtime digest itself (§ 6).

---

## § 1 · THE VERDICT

```
STRUCTURAL @ coverage 89/89: 18/28 EXACT green · 2 RED (TA-X-08, TA-X-16) · 8 UNGRADEABLE
(TA-X-03, 04, 05, 09, 20, 21, 27, 29) · P-2 RED · TA-X-06 UNGRADEABLE-declared (Q83(b), KP-110)
· substrate_epoch v3.7.1 / 48a4c94c… · prereg v1.12
```

**Antecedent (§ G, walked in order `STRUCTURAL → INDETERMINATE → PASS`, stopping at the first hit):** at least one of the 28 EXACT rows is RED.
* **`TA-X-08`** is RED on **25/25** cells. This is a port defect (§ 4.1).
* **`TA-X-16`** is RED on **20/25** cells. This is a prereg-scope defect, graded as the text reads (§ 4.2).

Either red alone makes the verdict `STRUCTURAL`.

### ⚑ THIS ATTEMPT CONSUMES ONE OF v1.12's TWO ATTEMPTS. The counter is now `1` of `2`.

§ G: *"`STRUCTURAL` — ≥ 1 of the 28 EXACT rows RED — the port is wrong; **consumes one of v1.12's two attempts**; L2 applies."*

**The conductor's reading at KP-176 was** *"P-2 red → TA-X-03…06 UNGRADEABLE → INDETERMINATE, which does not consume an attempt."* **That reading does not survive the walk.** P-2 red does make TA-X-03…05 UNGRADEABLE (§ 2.1). But `INDETERMINATE` is reached only if **no** EXACT row is red, and `STRUCTURAL` is tested first. Two EXACT rows are red, and P-2 has no bearing on either of them:
* P-2 gates only TA-X-03…05 (v1.8 § B.3, carried);
* every arm is C1-conforming;
* neither red row depends on a stream comparison.

**Consequences as written:**
* The port is wrong (TA-X-08), and nothing seals.
* **L2 (§ G.1):** *"v1.12 attempt 2 fires only after a v1.12-attempt-1 `STRUCTURAL` red is repaired and jack-ryan's Gate-2 PASSes the repair."*
* **⚑ And, from § 4.2: under v1.12 as written, attempt 2 is `STRUCTURAL` by construction** on any cell that dies before w160. The oracle dies at w152–w156 on every salt. **So the last attempt must not fire under v1.12's `TA-X-16` text.** This is a HALT to Matt (`WARN-16`, KP-137; § 9).

⚑ **The eight UNGRADEABLE rows and the P-2 red would give `INDETERMINATE` by themselves. They are outranked here, not dismissed.** A repair that fixes only the two reds reaches `INDETERMINATE`, not `PASS`. Most of these rows need **emission**, not repair (§ 5, § 9).

---

## § 2 · PRECONDITIONS

| id | emitted | state |
|---|---|---|
| **P-1** | 89/89 mapped, 0 unmapped, `closes: true`. Counts: IMPLEMENTED 65 · DIVERGENCE 8 · RUNTIME-CHOICE 13 · OUT-OF-SCOPE 3. Refusals 3 | **GREEN** (completeness, not truth) |
| **P-2** | `M-POL-2` s0: plain `17013bf679e0c57e…` ≠ with the no-op fold `a4ddd03421210909…`; `identical: false` | ⛔ **RED** |
| **P-3** | POOL-466, cardinality 466; law `WEIGHTED:pool_weight` + `UNIFORM:randrange` | **GREEN** (self-reported; `TA-X-25(c)` is the behavioural check, and it is green against the recomputed sets) |
| **P-4** | Every cell and the manifest carry `P4_pack.verified: true`, `paired: true`, `cross_pin: true`, 0 mismatches, both digests of record. The running harness measured pack `48a4c94c…` | **GREEN**. Both packs and the cross-pin were also recomputed by the grader (§ 0). The `runtime_header` field is absent (§ 6) |
| **P-5** | `P5_folds`: all eleven settings present and correct. Loader call `dot_corrections=True`, `pool_lift`/`winner_surface` ARMED, `C11aLoader(CLASS)` · winner surface ARMED · pool lift ARMED (POOL-466 · SWING-456 · NONSWING-10) · `PARENT_PLUS_MODIFIER` · REFUSE + `regen_ungated` · global magnitude ARMED_UNCONDITIONAL + measured board · PCL MULTIPLICATIVE @ 26.0 % · non-health route {Disruption, ManaBurnDrain, PierceRatio} · run-speed population 128 / 180 / 158 · march base 3.209466 · C-11a C1 + C2 (CLASS) + C4, C3 NOT FOLDED | **GREEN** |

### 2.1 · Ruling (1): a red caused by a defect in the probe still makes TA-X-03…05 UNGRADEABLE

drax's read-only diagnosis (godot `b215b11`) shows the red comes from **the probe's digest, not the port**:
* the "no-op fold" is a registry entry, `declare_extra_site("V9-NOOP-P2")`;
* since `46d7475`, the cell digest hashes every registered site's draw count, so the with-fold leg carries one extra key, `"V9-NOOP-P2": 0`;
* with that key removed, the with-fold digest equals the plain digest. Total draws, terminal, census and board are byte-equal.

I accept the diagnosis as a diagnosis. **It does not change the grade, for three reasons.**

1. **The text keys on the outcome of the probe, not on its cause.** v1.8 § B.3 (carried unchanged to v1.12): *"Probe: `M-POL-2` salt 0 run twice, once with a zero-draw no-op fold inserted. The digests must be identical. … **`P-2` red → `TA-X-03…05` UNGRADEABLE → `INDETERMINATE`.**"* The probe was run and the digests differ. No clause excuses a defective probe, and the grader may not supply one.
2. **Substituting drax's corrected digest would grade a probe that was never run.** "With the zero-draw entry removed" is a new comparison, computed after the fact in a scratch tree. Grading it would be the post-hoc repair § G forbids (*"No post-hoc widening, by anyone"*).
3. **⚑ On the prereg's own words, the probe as run is not P-2 even in substance.** The "fold" is not in the fight's call graph. It forks no stream and nothing invokes it (drax § 3.2). *"A zero-draw no-op fold **inserted**"* means a fold inserted into the fold chain the fight executes. A registry entry nobody calls is not that. So even a GREEN from this probe would not have discharged P-2: it would have been `P-2` **not run**, which gates the same rows the same way.

**Scope correction to the harness's label.** The emitted `consequence_if_red` reads *"TA-X-03…06 UNGRADEABLE"*. The text says **03…05**: *"`TA-X-06` is declared and enters no antecedent"* (v1.8 § B.3). TA-X-06 was already UNGRADEABLE-declared and stays so. The difference is verdict-neutral.

**What the ruling does NOT do:** it does not reach the verdict. `STRUCTURAL` is hit before the `INDETERMINATE` antecedent that P-2 feeds (§ 1).

### 2.2 · Ruling (2): what P-2 must test before attempt 2, and whether the text suffices

**What the law asks.** The criterion is *"digests identical"*. The object is *"a zero-draw no-op fold inserted"*. The claim is *"covers fold-granularity isolation"*. Two failures in the current probe each defeat it independently:

| defect | effect | fixed by Fix A? |
|---|---|---|
| (i) the digest treats "registered with 0 draws" and "not registered" as different stream states | **RED by construction** since `46d7475`; a perfectly disjoint port cannot pass | **yes** |
| (ii) the "fold" is a registry entry that no fight code invokes, and it forks no stream | a GREEN would show that *adding a registry entry* perturbs nothing. That is a re-run of an unchanged fight, not fold-granularity isolation | **no** |
| (iii) `noop_fold_draws: 0` is a literal (`kc2rt_ta.gd:296`) | the zero-draw claim is asserted, not measured | yes (Fix A step 1) |

**Fix A alone would turn P-2 from a false RED into a hollow GREEN.** That is worse, because a hollow green is the one outcome nobody re-examines. To satisfy its own law, P-2 needs all four of the following:
1. **A real inserted fold:** a fold object in the fight's fold chain, invoked by the fight loop at the same granularity as the existing folds. It obtains its stream the way every fold does (`Kc2RtRng.fork_stream`, V9-LAW-1) and draws zero values. Forking is the mechanism by which inserting a fold could perturb its siblings (seed derivation or fork order), so a probe that does not fork does not test it.
2. **A measured zero:** read the inserted fold's own counter; it must be 0. Otherwise P-2 is NOT RUN (not GREEN), exactly as Fix A step 1 says.
3. **One digest function for both legs,** in which a site with zero draws and an absent site are the same stream fact. Either drop zero-draw entries globally or filter the probe's own site on both legs. Every other draw count stays in the digest.
4. **Controls that must go RED:**
   * (a) the inserted fold draws once from a shared stream;
   * (b) one extra root draw at a live registered site;
   * plus the hygiene fix: a fresh pack per leg.

**Does v1.12's text suffice?**
* **For the criterion, yes:** *"digests identical"* is satisfiable under item 3.
* **For the object, it already demands item 1:** *"inserted"* is in the text.
* **It is under-specified on two points:** what "inserted" requires operationally (in the call graph, forking its own stream), and the digest's domain (zero-draw sites). A builder misread both, and neither gate caught it.

**So a v1.13 is not strictly required for P-2.** drax can satisfy v1.12's words with item 1. That touches `kc2rt_fight.gd`, a G3-path file, so it needs a G3 re-run and a delta Gate-2. The TA-X-08 repair needs both anyway (§ 4.1). **I recommend folding the operational definition into the v1.13 that § 4.2 already requires**, named under Discipline #12 as an operational reading and not a change of criterion, so the next builder does not have to infer it.

---

## § 3 · THE 28 EXACT ROWS (and `TA-X-06`)

| id | observed (from the emission unless labelled) | verdict |
|---|---|---|
| `TA-X-01` | `M0` s2 run twice, nothing inserted: `3f94ab0c…` == `3f94ab0c…`, and it equals the `M0/2` cell digest. The arm and salt differ from P-2's | **GREEN** |
| `TA-X-02` | 89/89, 0 unmapped | **GREEN** |
| `TA-X-03` | `M-POL-2-NULL ≡ M0` 5/5 (raw relation holds) | **UNGRADEABLE** (P-2 red) |
| `TA-X-04` | `W1-NULL ≡ M-POL-2` 5/5 (raw relation holds) | **UNGRADEABLE** (P-2 red) |
| `TA-X-05` | `M-POL-2 ≢ M0` on 5/5 (raw relation holds) | **UNGRADEABLE** (P-2 red) |
| `TA-X-07` | (a) max ρ̂ = **2.2138e-16** ≤ 1e-12 on 25/25, with 21 cells at exactly 0.0. (b) max \|residual\| 7.45e-9, printed beside `offered`. (c) **(L2) of record (jack-ryan `c210b1979`): 25/25 hold, worst β 3.590829330577844e-14 (M0·0), margin ×27.85.** My cross-check from the graded cells' own `l2_operands`, in exact rationals: 25/25 hold, worst β identical. Census FILE `cf49eefe…` (T 22 · S 11 · F 14) filed at the graded digest; Neumaier probe bitwise | **GREEN** |
| ⛔ `TA-X-08` | identity 1 `n_player_ticks_observed = D + PRE_FIGHT` **and** identity 2 `n_channelling + n_released = D` **fail on 25/25 cells, each by exactly 1** (e.g. M-POL-2 s0: 467 vs 466 + 0, and 405 + 62 = 467 vs 466). The cells' own `holds` fields read `false` | ⛔ **RED** (§ 4.1) |
| `TA-X-09` | **no value in the emission.** The nine-vector replay is in neither `ta_manifest.json` nor any cell. *Supplementary, not graded:* `tmp/kc2/t0/t0_report.json` (05:32:11) reads 9/9, but it is outside the MANIFEST, carries no runtime digest, and predates the graded tree's last runtime-content commit (`2ce053d`, 05:32:37) | **UNGRADEABLE** |
| `TA-X-10` | `W1` `max_body_radius_m` 43.0603720647777 on 5/5 ≤ 43.758085029822276 (margin 0.698 m); wall armed | **GREEN** |
| `TA-X-11` | clamps (player, body) = (0, 0) on 10/10 (`W1` armed with r = 43.7580850298223; vacuous on `W1-NULL`, § 0.2 NOTE). *A port with no wall also scores zero* (§ F.5 cl. 6) | **GREEN** |
| `TA-X-12` | pool damage 0.0 on 25/25; aprons **absent** under ORACLE, not present at zero | **GREEN** |
| `TA-X-13` | `n_player_crits` 0 on 25/25; `CritLimb.LO` DRIVER-OF-RECORD | **GREEN** |
| `TA-X-14` | `cause == energy` 0 on 25/25. Release causes are only `type_a`/`type_b`. Releases are event-scheduled (0–19 per cell; 0 on the two unarmed-channel arms) | **GREEN** |
| `TA-X-15` | (a) every (wave, point) row on 25/25: p01–p04 release at tick 0, p05 at tick **49** (4.000 s). (b) 0 intra-point staggers; **GREEN-BY-CONSTRUCTION** (one release tick per point) | **GREEN** |
| ⛔ `TA-X-16` | `n_pool_picks` **== 47 on 5/25 cells** (the five that reach w160). It is **15 or 19 on the other 20**. On every wave played, the per-wave picks equal V11-P06-1's vector, and no cell has a point-6 row. At manifest grain, `active_points_per_wave` = V11-P06-1 (sum 47) and `picks_suppressed` = 18 | ⛔ **RED** as the text reads (§ 4.2) |
| `TA-X-17` | `ScatterLaw.POLAR_UNIFORM_RHO` (DRIVER-OF-RECORD): ρ = `PLACEMENT_EXTENTS_M` (8.0) · u₂ with u₂ ∈ [0,1) (`kc2rt_board.gd:600/784`), so > 8.0 m is impossible. No per-body statistic is emitted | **GREEN-BY-CONSTRUCTION** |
| `TA-X-18` | Emitted `["-3.999999999999985", "-3.49691120014899e-07"]`. The grader re-parsed the bits with CPython: `c00fffffffffffde` · `be9777a5cf72cec6`, which equal the expected bits (sign included). Emitter `cpython-repr`; round-trip probe true; `repr(float(s)) == s` for both strings, so lossless per § F.2l (i)–(ii) | **GREEN** |
| `TA-X-19` | Read at the graded tree. ⚑ **The deferred-arrival limb is now ported for projectiles** (`_defer_arrivals`, `kc2rt_fight.gd:4125`), so v1.8's *GREEN-VACUOUSLY* has **expired**. A packet carries `{seq, b, rec, direct, pcl, fams, cast, n_rows}` (`:4105`), with no arrival position. Landing (`_land :5577`, `_cp_absorb :3964`) reads no position. Graded by source at the pinned digest; no counter is emitted | **GREEN** |
| `TA-X-20` | **no value in the emission.** *Supplementary, not graded:* t0_report reads 2.99 hit / 3.01 miss / hit from behind / 12 → 12 | **UNGRADEABLE** |
| `TA-X-21` | **no value in the emission.** *Supplementary, not graded:* t0_report and `kc2rt_purity_scan.json` (05:28:37) read 12 rows and 0 violations. ⚑ Both predate `2ce053d` (05:32:37), which removed a `py_round` from the walk **because of this row's own purity assertion**. So the supplementary scan is demonstrably not of the graded tree | **UNGRADEABLE** |
| `TA-X-22` | `interrupts_channel_flag` cause 0 on 25/25 | **GREEN** |
| `TA-X-24` | `PhaseModel.ENGAGE` DRIVER-OF-RECORD (emitted). The negative was checked by source search at the graded tree: no sha256 of any actor id. The sha256 sites are pack, register and leech-table digests, the V9-STREAM-07 seed, and `kc2rt_kmill.seed_for`'s wave material | **GREEN** |
| `TA-X-25` | (a) refused 0 on 25/25, satisfied over an empty refusal set. (b) the three named counters are present and sum to `n_bodies_spawned` on 25/25. (c) `spawn_by_record` against POOL-466 / SWING-456 / NONSWING-10, **recomputed here from the oracle**, all three digests reproducing: (1) every key ∈ POOL-466, (2) every SWING-456 record `measured_offense`, (3) every NONSWING-10 record inert, (4) the class sums equal (b)'s counters, all on 25/25. (d) printed, not graded | **GREEN** |
| `TA-X-26` | (a) audit green, 0 unaccounted. (b) loaded; sha `cb6a008b…` = P-i; call site `sim/kc2rt_fight.gd:2871`. (c) 7,900 rows · 790 records · 8 tiers `{65, 75, 83, 88, 105, 115, 565, 588}` · 5 multipliers · 790 wave-invariant. (d) one helper call site, 0 disagreements. (e) **ARMED-464** mean 0.246896551724137 (Δ 2.4e-14 ≤ 5e-7), median 0.25, max 0.35, min 0.0, 17 immune. Grain-labelled; the port's fight-armed 456 is printed beside it, not instead | **GREEN** |
| `TA-X-27` | (a) scan of 76 files: 0 short-circuits, 0 unclassified (holds). **(b) NOT EMITTED:** the harness emits only a pointer to `tmp/kc2/kc2rt_rules_smoke.json`, which is outside the MANIFEST (05:28:45; 58 checks, 0 failures, no per-seed values). (c) 29 live sites, the p05 draw elided as the oracle elides it, and G3's draw rules hold at the graded digest (holds). (d) 97 / 139 (holds) | **UNGRADEABLE** (on (b)) |
| `TA-X-28` | (a) port target and tick caps 0/0 on 25/25. No cap site exists, so this is a structural zero (§ F.5 cl. 6). Oracle side, derived from oracle code as the emission directs: `player_sustain.py:19` *"NO CAP IS INVENTED"*, `run.py:805` *"per-body leech with no target cap and no per-tick cap"*. (b) `ALL_BODIES_IN_DISC`, 0.57. (c) same shape. *A green says one leech law, not that it reproduces Matt's fight* (cl. 10) | **GREEN** |
| `TA-X-29` | (a) `PRED-GMAG-WHOLE` true: attr 193 / 154 (actors 344), own 527 / 104; grain label printed (holds). **(b) NOT EMITTED** at this digest: no Z5-LAW composition declaration and no clamp cross-check (v1.7's emission had both). **(c) NOT EMITTED as a check:** `M_inst` per wave is printed (1.82 ×5, 1.83 ×5), but no `z3_wave_damage_modifier_check` comparison is asserted. (d) `inert_records` 29; *"unexercised: 0 of 29"* not printed. (e) **3.207764 / 4.980316**, and all 16 + 23 per-record ratios equal v1.8 § F.2h's table, max \|Δ\| 0.0 (holds) | **UNGRADEABLE** (on (b), (c)) |
| `TA-X-30` | (a) halt at `arena.json` `d_engage_m` 2.4; NaN tested explicitly (NaN and zero rejected). (b) `n_bodies_halted_beyond_d_engage` 0 on 25/25 | **GREEN** |
| `TA-X-06` | `W1 ≢ M-POL-2` on 3/5 salts (1, 3, 4); identical on salts 0 and 2. **`UNGRADEABLE-declared (Q83(b), KP-110)`**, no colour, enters no antecedent. `TA-B-14` on `W1`: vetoes `[0, 3, 0, 1, 1]`, occupancy `[0, 0, 0, 0, 0]` | declared |

`TA-X-23` is struck and retired.
**Counts: GREEN 18 · RED 2 · UNGRADEABLE 8 = 28.** The GREEN count includes two GREEN-BY-CONSTRUCTION rows (`TA-X-15(b)`, `TA-X-17`). Two GREENs rest on source reading at the pinned tree (`TA-X-19`, the `TA-X-24` negative).

**The evidentiary rule I applied, stated once.** A **computed** result must be in the hash-pinned emission. A file in `tmp/` is not, nor is anything that predates the graded tree (v1.12 § B.5a: *"The grader verifies these on the emission"*). A **static structural property of the code** may be read off the runtime tree, because the tree is pinned by digest and is the graded object. This is stricter than my v1.7 grade, which graded `TA-X-09`/`20`/`21` from same-session `tmp/` files. That leniency was conditional on the files being folded into the emission for the next attempt ("drax should fold these into the emission for attempt 2"). They were not, and this time one of them is demonstrably not of the graded tree.

---

## § 4 · THE TWO REDS

### 4.1 · ⛔ `TA-X-08`: the port censuses the lethal tick. PORT DEFECT, repairable

**The law** (v1.1 § C.1, carried verbatim through v1.12):

```
D_constructed = CHANNELLING + CHANNELLING_AND_MOVING + MOVING + IDLE   (PRE_FIGHT and DEAD excluded)
n_player_ticks_observed = D + PRE_FIGHT ;  n_channelling + n_released = D
```

**On the emission:** every cell has `state_counts.DEAD = 1`. That tick is counted in `n_player_ticks_observed` and in `n_channelling` or `n_released`, but by law it is not in `D`. Both identities are therefore off by exactly one on all 25 cells.

| cell | `n_player_ticks_observed` | `D` | `PRE_FIGHT` | `n_chan + n_released` |
|---|---:|---:|---:|---:|
| M-POL-2 s0 | 467 | 466 | 0 | 467 |
| M0 s0 | 2,013 | 2,012 | 0 | 2,013 |
| W1 s4 | 483 | 482 | 0 | 483 |

(The other 22 cells follow the same pattern.)

**Mechanism, read at the graded tree:** `kc2rt_fight.gd :: _census` (`:5731–5746`).
* It increments `n_player_ticks_observed` unconditionally.
* It labels the tick `DEAD` when `player_hp <= 0`.
* It still increments `n_channelling` when channelling.

**Why it appears now.** Hole 2's repair (`⚑ death_order: DEATH-CHECK-AT-FLOOR-BEFORE-HEAL`, `n_lethal_floor_ticks: 1`) means the lethal tick now reaches `_census` with HP ≤ 0. In the v1.7 run the same-tick heal resurrected the player, no cell died, and TA-X-08 was GREEN 25/25. **The repair exposed a census branch that had never been exercised.**

**The oracle convention, checked against the seal.** The sealed `[M-POL2]` cell (hash-verified, read by key) has `player_death` on every salt and **no `DEAD` state in its census**. Per salt, observed = D + PRE_FIGHT: 1,090 = 1,084 + 6 · 307 = 305 + 2 · 107 = 106 + 1 · 186 = 185 + 1 · 1,109 = 1,103 + 6. **The oracle does not census the death tick. The port does.** G3 is unaffected, because death wave and tick are equal; this is an accounting defect, not a fight defect.

**Why this is RED and not a technicality.**
* The row exists for exactly this. The port's own `D_law` string, printed in every cell, says a different denominator is *"the single easiest way to fail T-A for a non-reason"*.
* An EXACT identity that fails is RED; there is no tolerance to read.
* It also biases every per-tick diagnostic that divides by `D` (e.g. `TA-B-02` uptime counts the dead tick in its numerator).

**Repair:** make the lethal tick satisfy the law, matching the oracle's convention. Either do not census it, or exclude a `DEAD` tick from `n_player_ticks_observed` and from `n_channelling`/`n_released`. Add a fail-first probe on a cell that dies. `kc2rt_fight.gd` is on the G3 path, so this needs a G3 re-run and a repair Gate-2.

### 4.2 · ⛔ `TA-X-16`: `n_pool_picks == 47` is written over the full window, and 20 cells do not play it. PREREG-SCOPE DEFECT, graded as the text reads

**The text** (v1.8 § F.2, carried unchanged): *"p06 OFF: `n_pool_picks == 47`, `n_spawn_point_6_keys_rolled == 0`, and a counter for the filtered keys | `waves.json` | integer"*. The § B.1a arm table puts it on **all 25 cells**. The figure 47 is the waves.json count over w151–w160 with p06 off: 5+5+5+4+4+5+5+5+5+4. It was derived *"RE-DERIVED, UNCHANGED (54 / 47)"* when every port cell cleared to w160.

**On the emission:** `n_pool_picks` is 47 on the five cells that reach w160. It is 15 (dies in w153) or 19 (dies in w154) on the other 20. **By the text, that is RED on 20/25 cells.** I do not convert it, in either direction:
* not to GREEN by reading 47 as "the window count", which the manifest-grain roster does emit (`active_points_per_wave` sums to 47);
* not to UNGRADEABLE by calling the per-cell statistic "a different statistic".

**Either move would be a grader re-reading an expected value after seeing the data.** That is the one thing this grade is not allowed to do.

**What the red is, stated so it is not mistaken for a port defect.**
* On every wave each cell plays, its per-wave picks equal V11-P06-1 exactly, and no cell rolls a point-6 key. p06 is off, as the row's purpose requires.
* The shortfall is the waves not played: leg A stops at the first death.
* **The oracle itself dies at w152–w156 on every salt of every arm** (§ B.1a). It would score the same red.
* An EXACT row the reference cannot pass is a defect in the row, and **no port repair can reach it.** A port cannot roll waves after the player is dead.

**Consequence, and why it gates the last attempt.**
* Under v1.12 as written, attempt 2 is `STRUCTURAL` on `TA-X-16` whenever any cell dies before w160. The port's own generator did so on 20/25 here, and the oracle does so on 25/25.
* Firing attempt 2 under this text would spend the last attempt on a red known in advance. That is v1.8 § F.2d's case-2 logic in the other direction: *do not fire an attempt whose outcome is fixed by construction*.
* The remedy is a row restatement, for example *"on every wave the cell plays, picks == V11-P06-1[w]; no point-6 key; the filtered-key counter emitted"*. That is a row change (KP-137) to a document against which a graded run now exists. **It is a HALT to Matt** (`WARN-16`), and it needs a dated v1.13 committed alone (D4).

**Did this red decide the verdict?** No. `TA-X-08` alone makes it `STRUCTURAL`, and the counter moves either way. `TA-X-16` matters for **attempt 2**.

---

## § 5 · THE UNGRADEABLE ROWS: what each needs

| row | kind | what closes it |
|---|---|---|
| `TA-X-03` · `04` · `05` | **probe repair** | P-2 per § 2.2: a real inserted fold, a measured zero, one digest function for both legs, controls. The raw relations hold (5/5 · 5/5 · 0/5) |
| `TA-X-09` | emission | fold the nine-vector replay (with its ROWSET `0e826ee0…`) into the emission at the graded digest |
| `TA-X-20` | emission | fold the hit-test table into the emission |
| `TA-X-21` | emission | fold the quantisation vector table and the no-bare-`round(` scan into the emission, run at the graded digest, with the live oracle site list re-verified |
| `TA-X-27` | emission | (b): the per-seed `_randbelow_with_getrandbits` replay values in the emission, not a pointer to `tmp/` |
| `TA-X-29` | emission | (b): the Z5-LAW composition declaration and the clamp cross-check, as v1.7's emission carried. (c): the z3 check asserted per wave against the pack's `z3_wave_damage_modifier_check`. (d): print *"unexercised: 0 of 29"*. jack-ryan's INFO-B (assert the `to_hit`/`attack_speed` flags) belongs here too |

---

## § 6 · THE NINE § G.3 FIELDS THE HARNESS DID NOT EMIT: rulings

**What the prereg's text decides.** § G's antecedents are built from the 28 EXACT rows, `P-1`…`P-5` and `TA-X-07(c)`. **None of the nine fields appears in any antecedent.** So no absence below makes a row UNGRADEABLE or the verdict INDETERMINATE. § G.3 is the schema of the **verdict file**. The only H-4 harness obligations among § G.3's fields are `r11_bound`, `g3` and `ta_x_18` (§ H, H-4), and all three were emitted. The one conformance consequence § G attaches to a field is to `declared_ungradeable` (*"anything else is C1"*), and that binds the verdict file.

**So the verdict file is assembled by the grader.** It is `ta_verdict_v1p12_attempt1.json`, FILE `af3754c701f8afb22a5501b0b955fb8b2dc36cf361d5033980daa23e4c86f2f0`. It keeps the harness's fields and the grader-filled fields in **separate, labelled blocks**, so no grader-filled value can be read as emitted.

| field | ruling | filled from pinned evidence? |
|---|---|---|
| `runtime_digest` | report-face / verdict-file defect. Not an antecedent. ⚑ It is also the one place the cells are tied to the runtime, and today that tie is the seat's MANIFEST attestation plus my recomputation, not the harness | **yes:** `a9b756cd…`, recomputed from `kc2_runtime/MANIFEST.json` over blobs at `9b0ad0c` |
| `runtime_header` | report-face defect. P-4 is met on the emission: the running harness measured pack `48a4c94c…` and `P4_pack` verified both packs and the cross-pin. Only the named header field is missing | **no** (not reconstructible; the harness emits no header object). Left `null` with that note |
| `cross_pin_verified` | report-face (name) defect. The value **is** emitted as `P4_pack.cross_pin: true` with `cross_pin_model_pack_digest` | **yes:** grader recomputation, `true` |
| `oracle_containment_H9` | report-face. H-9 is discharged (PASS, KP-146) | **yes:** five FILE pins, all reproduce |
| `closure_H10` | report-face. H-10 is discharged (KP-153) | **yes:** receipt `a0ad8246…` reproduces |
| `set_digests` | report-face | **yes, for three:** POOL-466, SWING-456 and NONSWING-10 were recomputed from the oracle and reproduce. FALLBACK-158 was **not** recomputed (no graded row reads it); the v1.12 pin is carried, labelled as not re-derived |
| `declared_ungradeable` | not missing in effect. The emission labels TA-X-06 `UNGRADEABLE-declared (Q83(b), KP-110)`, and the verdict file carries **exactly** `[{"id":"TA-X-06","authority":"Q83(b) / KP-110"}]`. **C1 conformance: MET** | **yes** |
| `hole_closure` | seal-blocking, not verdict-blocking (§ G.2). **H-5 (jack-ryan) is not yet filed.** Moot for this verdict; it gates only the quotability of a PASS | **no:** `PENDING (H-5)` |
| `port_holes_printed` | § F.5 cl. 11 is mandatory *"on any report"*. The harness printed none. **This grade prints it (§ 8)**, so the report of record carries it | **yes:** satisfied by § 8 of this grade |

**For attempt 2:** the harness should emit `runtime_digest` (computed by the runtime from its own MANIFEST at boot) and a `runtime_header`. Then the runtime's identity rests on the emission, not on the seat.

---

## § 7 · DIAGNOSTICS: reported, gating nothing (F5). Every width VOID

**CLASS V · `TA-B-01`, verbatim (§ F.3):** *"`BAND / NON-DECISIVE / REPORT-ONLY`. A terminal wave inside or outside this band is not evidence of fidelity either way. It is read from the port's `M-POL-2` arm. The oracle's sealed `M-POL-2` arm terminates at `[156, 152, 151, 151, 156]`, `player_death` on every salt. The v1.12 oracle's `M-POL-2` arm (the same object as v1.8's, v1.9's, v1.10's and v1.11's: the 338 armed, the winner surface armed, the C-11a corrections folded) terminates at `[156, 152, 155, 152, 152]`, `player_death` on every salt, and no salt reaches wave 160. A port that clears to wave 160 has not survived a hard board; it has failed to be in one."*

| diagnostic | value |
|---|---|
| `TA-B-01` port `M-POL-2` terminal waves | **`[153, 160, 154, 154, 153]`**, `death` on 5/5 (salt 1 dies in w160 and does not clear) |
| beside `TA-X-06` (not `TA-B-01`) | port `W1` `[153, 160, 154, 154, 153]` · oracle `W1` `[156, 152, 155, 152, 155]` |
| all arms | `M0` ≡ `M-POL-2-NULL` `[160, 154, 154, 154, 153]` · `M-POL-2` ≡ `W1-NULL` ≡ `W1` (by terminal) `[153, 160, 154, 154, 153]` |
| `TA-B-02` uptime (M-POL-2, per salt / mean) | `[0.8691, 0.8868, 0.8851, 0.8984, 0.8705]` / 0.8820. ⚑ the numerator includes the dead tick (§ 4.1) |
| `TA-B-03` frac moving | mean 0.8446 |
| `TA-B-04` / `TA-B-05` P(chan \| moving / stationary) | 0.9147 / 0.6938 |
| `TA-B-08` ordering | holds 5/5 |
| `TA-B-14` `W1` vetoes / occupancy | `[0, 3, 0, 1, 1]` / `[0, 0, 0, 0, 0]` |
| `TA-B-15` NO-DATA bodies | 0 on every cell (fraction 0.0) against the reference point 0 |
| sustain (port, printed, not asserted) | leech / intake: M-POL-2 `[2.03, 5.56, 2.62, 2.88, 2.08]` |

**§ F.3a still applies.** The port's generator and the oracle's draws are different realisations, so the per-salt comparison above carries no fidelity information (`C-p`). n = 5 per arm.

---

## § 8 · REPORT-FACE SENTENCES (mandatory on any report)

**§ F.5 cl. 7 (sustain):** *"`leech` and `intake` still have no oracle side in the seals (`C-e`). Off-seal, the v1.12 oracle (the same object as v1.8's, v1.9's, v1.10's and v1.11's; the C-11a corrections folded) KILLS THE PLAYER AT WAVES 152–156 on salts 0–4, and lands ×3.17 the referent's intake over waves 151–159 on the landed grain. The port's own figure is printed from this run and not asserted here. A GREEN T-A IS COMPATIBLE WITH ANY RELATION BETWEEN EITHER REPLICA AND THE REFERENT."*

**§ F.5 cl. 11 (the port≠oracle holes):** *"Port≠oracle holes 1–17 (PCL dropped · death after heal · damage rows unreachable · `tree_attack` slots never chosen · dying slots mishandled, and 5b one dying slot per death · slot chance/cooldown/delay never read · the wrong march base · to-hit · mitigation order · DoT timeline · monster crit tier · motion order and the contact fold · Soulfire and the bleed rider · monster pets · the resist cap · attack speed and OA adds · the HI life block), the chance-gate boundary, the C-11a grant law, the loop-layer defects of KP-144, the pack-closure defect of KP-147, and the closure-law defects of KP-150 / KP-152 (run state carried as input · arms defined only in prose · read-absent columns · constants on untaken branches) are invisible to every EXACT row in this instrument. A v1.12 PASS is not quotable without jack-ryan's hole-closure finding at the same runtime digest, and the seal is blocked on any non-zero R-6 invariant."*

**The three R-6 invariants, with their values:**
* (i) cells with `killer_id` set and `terminal_reason == cleared`: **0**;
* (ii) in-tick resurrections (an HP trace that reaches 0 and then rises): **0**;
* (iii) cells where a PCL row landed and `PercentCurrentLife` intake is not > 0: **0**.

*(⚑ Hole 2's repair shows in (i) and (ii): both were non-zero-shaped at v1.7, 9 of 10 outcomes with a killer and "cleared". The same repair exposed `TA-X-08`'s census branch, § 4.1.)*

---

## § 9 · WHAT MUST CHANGE BEFORE ATTEMPT 2 (the last one under the cap)

| # | item | kind | owner / route |
|---|---|---|---|
| 1 | **`TA-X-08`:** the lethal tick must satisfy the denominator law, following the oracle's convention. Fail-first probe on a dying cell | **PORT REPAIR** (`kc2rt_fight.gd`, G3 path) | drax → G3 re-run → jack-ryan repair Gate-2 (L2) |
| 2 | **`TA-X-16`:** restate the row over the realised window. **HALT to Matt.** A v1.13 committed alone, with its own pre-read. **Attempt 2 must not fire under v1.12's `TA-X-16` text** (§ 4.2) | **PREREG ROW CHANGE** (KP-137, `WARN-16`) | gamora drafts on Matt's word |
| 3 | **P-2:** a real inserted fold (forked stream, invoked by the fight loop, zero draws measured), one digest function for both legs, two positive controls, a fresh pack per leg (§ 2.2). Fix A alone is **not sufficient**. Fold the operational reading into v1.13 under Discipline #12 | probe repair (touches `kc2rt_fight.gd`) + prereg wording | drax; gamora (v1.13 wording) |
| 4 | `TA-X-09` / `20` / `21` / `27(b)` / `29(b)(c)(d)` into the hash-pinned emission, run at the graded digest | **EMISSION** | drax |
| 5 | `runtime_digest` and `runtime_header` emitted by the runtime (§ 6) | emission | drax |
| 6 | **H-5:** the hole-closure finding at the attempt-2 digest | seal | jack-ryan |
| 7 | **H-8:** Matt's T-C on the graded digest | seal | Matt |

Items 1 and 3 both touch `kc2rt_fight.gd`, so they share **one** G3 re-run and **one** repair Gate-2. Item 2 is independent of the port, and it is the one that decides whether the last attempt can be anything but `STRUCTURAL`.

**The harness's 2,106 NUL lines.** They are cosmetic (drax `b215b11` § 4): 26 `\u0000` escapes in provenance strings, decoded three times per load, over 27 loads. No emitted value is affected. **No bearing on any row.**

---

## § 10 · THE HONEST `n` (§ C.8)

**The 25 cells carry 13 distinct outcomes:**
* `{M0, M-POL-2-NULL}` are byte-identical per salt (5);
* `{M-POL-2, W1-NULL}` are byte-identical per salt (5);
* `W1` differs from `M-POL-2` on salts 1, 3 and 4 (3 more).

So:
* `TA-X-08`'s *"25/25"* is **13/13 distinct outcomes**;
* `TA-X-16`'s *"20/25"* is 10/13;
* every diagnostic above is a mean over 5 salts of one arm (n = 5).

---

*Filed 2026-10-01 by **gamora**. The commit message records the verdict file's sha256.
**Verdict `STRUCTURAL`; attempt 1 of 2 under v1.12 is CONSUMED; nothing seals; a HALT to Matt is owed on `TA-X-16` before attempt 2.***
