# KC2-PLAY · T-A PREREGISTRATION **v1.11**: v1.10 RE-PINNED to pack **v3.7.1** ("the closure law amended"), and R-11's budget DERIVED

> ⚑ **STATUS: IMMUTABLE ON COMMIT. v1.11, authored 2026-10-01. SUPERSEDES v1.10 FORWARD.**
> *(The filename carries the series' `2026-09-20` prefix. The document is dated 2026-10-01.)*
>
> ⚑ **v1.11 MOVES THE PACK OF RECORD FROM v3.7 TO v3.7.1** (KP-150 → KP-153). The cut adds one member,
> `model/input_closure_v3p7p1.json` (891 rows: `a8` · `r9` · `s10` · `w11` · `k12` · `e13`). **It is not purely
> additive: four `k3` rows are WITHDRAWN as run state** (`IC7-K-0036` = `reincarnated.simulation.kc2.alert._INCIDENCE` · `IC7-K-0037` = `reincarnated.simulation.kc2.alert._ROWS` · `IC7-K-0038` = `reincarnated.simulation.kc2.alert._TABLE` · `IC7-K-0255` = `reincarnated.simulation.kc2.locomotion._FALLBACK_HITS`). Every other v3.7 member except `meta.json` and
> `input_closure.json` is byte-identical. **The oracle did not move**: its code and data at engine HEAD `22cd2288`
> are byte-identical to v1.10's `eee8ce8b`, and all 62 content files it consumes re-hash to their rows (§ A.2).
>
> ⚑ **NO EXPECTED VALUE MOVES.** All 28 EXACT rows and the five preconditions keep v1.10's assertion, value,
> tolerance and class. Every oracle-derived value was recomputed on the v3.7.1 tree and reproduces v1.10 exactly,
> `TA-X-18`'s re-derived value included.
>
> ⚑ **AN ARM IS NOW DEFINED BY THE PACK, AND THIS FILE CITES IT** (KP-150 ruling 2). § B.1a gives, for every arm and
> for the `TA-X-29(e)` walk, the `a8` rows that define it, with the ROWSET digest of each arm's rows.
>
> ⚑ **R-11 (KP-152): THE BOUND DOES NOT HOLD. THE 4,500-TERM BUDGET STANDS, AND v1.10/v1.11 ATTEMPT 1 CANNOT FIRE ON
> THE PASS-3 RUNTIME AS MEASURED** (6,616 terms on `M-POL-2`, 6,539 on `W1`, both salt 1). § F.2k derives the
> worst-case rounding error of the summation the port actually uses (read from drax's code, not assumed). At
> n = 6,616 the offered-side term alone is 7.3441e-13 against the 1e-12 tolerance (margin under ×1.37 before any
> sink is counted), and the six sink accumulators,
> which the runtime neither counts nor emits, can only add to it. **No tolerance, budget or expected value is
> changed.** Remedies are listed for the conductor (§ F.2k.6) and none is adopted. ⚑ **jack-ryan: attack § F.2k
> first.**
>
> ⚑ **ATTEMPTS: `0` OF `2` UNDER v1.11. THIS IS A CARRY, NOT A RESET.** No graded run exists under v1.10 (no v1.10
> verdict file exists; the ledger through KP-153 records none). The allowance (Matt KP-115 *"Reset to 2"*, carried
> unspent through v1.8, v1.9 and v1.10) is carried unspent. v1.7's attempt 1 stays on the record as spent.
>
> ⚑ **THE DECLARED SET IS CLOSED AT EXACTLY `["TA-X-06"]`** (Matt, Q83(b), KP-110). Carried.
>
> ⚑ **`H-9` DISCHARGED: PASS** (KP-146; carried). ⚑ **`H-10` DISCHARGED** (KP-153: strict closure 0 on all 14
> captures, seven jobs × two hash seeds, and the static sweep 0). **OQ-14 and OQ-15 stay OPEN.**
>
> ⚑ **THIS FILE IS IMMUTABLE ONCE COMMITTED. ANY CHANGE AFTER A GRADED RUN EXISTS AGAINST IT IS A HALT TO MATT
> (`WARN-16`).**
>
> ⚑ **D4 HELD. This file is committed ALONE, with zero code, before any graded run against v3.7.1 exists.** Every
> digest in it was computed this session from the files and filled into the document by script. None was typed
> or copied from a ledger row. Each is labelled **FILE** (sha256 of one file's bytes), **ROWSET** (sha256 of a
> stated law applied to rows or a member list) or **PACK** (the manifest's pack law over its member rows), per
> KP-101.
>
> **Authority:**
> * ⚑ **KP-150** (conductor): H-10 does not pass as written; three closure-law defects; cut v3.7.1. **Ruling 2:
>   arm and walk definitions are inputs; *"an arm is defined BY THE PACK and the prereg cites the rows."***
> * ⚑ **KP-151**: the mutation-scan gate; exemption class E7; `IC7-K-0036/37/38` withdrawn.
> * ⚑ **KP-152**: port pass 3 accepted (G3 native, zero injections); the conductor's corrigendum (a per-salt
>   native death-wave match is unattainable by construction; the fidelity instrument is G3 on the oracle's
>   draws); ⚑ **H-6 blocks attempt 1 as written; routed here: *"derive, from the summation method actually used,
>   the error bound at the measured term count."***
> * ⚑ **KP-153**: pack v3.7.1 cut PASS; H-10 discharged; *"gamora prereg v1.11 (re-pin v3.7.1 + the R-11
>   derivation, KP-152)."*
> * **Carried from v1.10 without change:** Q83(b), Q85, Q87, Q91, KP-115, KP-127, KP-131, KP-132, KP-137,
>   KP-144, KP-146, KP-149, F5, jack-ryan's v1.8 pre-read (R-17…R-22), the `C-o` ceiling.
>
> **Author:** gamora (simulation + spirit-guide seam), Run KC2-PLAY. **Decision rules only. NO BAND WIDTH IS MINTED,
> AND EVERY WIDTH IN `P-a` STAYS VOID.** **v1.10 (`b1dd68efe2ce6009c2981d1c25bb182aba8c444945ec81f53a5c3c0c8b79061c`) and every earlier version are NOT edited.**

---

## § 0 · ⚑ THE v1.10 → v1.11 DELTA

**Legend.** **CARRIED** = assertion, expected value and derivation unchanged; substrate properties were recomputed
and reproduce. **RE-PINNED** = only a digest moves. **NOTE** = assertion and value unchanged, but a v3.7.1 row
changes how the row is run, configured or booked. **ARM (a8)** = the row's arm(s) are now cited to the `a8` rows
that define them (§ B.1a); the assertion and value are unchanged.

### 0.1 · Preconditions

| id | v1.11 | Δ value | why |
|---|---|---|---|
| `P-1` coverage 89/89 | **CARRIED** | none | census property |
| `P-2` stream disjointness | **CARRIED. ARM (a8):** `M-POL-2` (`IC7-A-0077`…`0152`), salt 0, port only. Epoch now v3.7.1 (§ C.7) | none | — |
| `P-3` roll population / law | **CARRIED.** POOL-466 recomputed from the v3.7.1 `waves.json` (byte-identical): 466, set digest reproduces | none | — |
| `P-4` pack identity | ⚑ **RE-PINNED v3.7 → v3.7.1** (model 19 members, reference 7, cross-pin) | digests only | KP-153 |
| `P-5` oracle fold settings | **CARRIED: the same eleven settings.** ⚑ **NOTE:** the loader call is now on the wire as `a8` row `IC7-A-0453` (with `IC7-A-0435`, `IC7-A-0454`, `IC7-A-0446`); § B.6 | none | KP-150 ruling 2 |

### 0.2 · EXACT rows (28) and the declared row

| id | v1.11 | Δ expected value | note |
|---|---|---|---|
| `TA-X-01` | **CARRIED; ARM (a8)** | none | the named arm is configured from its `a8` rows |
| `TA-X-02` | **CARRIED** | none | — |
| `TA-X-03 / 04 / 05` | **CARRIED IN FORM; ARM (a8)** | none | ⚑ `M0`, `M-POL-2-NULL`, `W1-NULL` are now inside the closure proof (`H-10` discharged, KP-153) |
| `TA-X-06` | **UNGRADEABLE-declared, CLOSED** | — | — |
| `TA-X-07` | **CARRIED VERBATIM; ARM (a8), all 25 cells** | none | ⚑ **§ F.2k: clause (c)'s 4,500 budget is DERIVED, not restated; it stands. At the measured depth the attempt does not fire** |
| `TA-X-08` | **CARRIED; ARM (a8)** | none | — |
| `TA-X-09` | **CARRIED** (`math_rules.json` byte-identical v3.7 → v3.7.1, FILE `3b1e2d014411cb314d5cbf42ea40773dbcfa3de242f13d3a1d31eb830643b62d`) | none: nine graded vectors ROWSET `0e692765` | — |
| `TA-X-10` | **CARRIED; ARM (a8) `W1`**; recomputed `43.758085029822276` | none | `H-9` PASS carries |
| `TA-X-11` | **CARRIED; ARM (a8) `W1`, `W1-NULL`** | none | — |
| `TA-X-12 / 13 / 14 / 15 / 16` | **CARRIED; ARM (a8), all 25 cells** | none | — |
| `TA-X-17` | **CARRIED; ARM (a8), all 25 cells** | none | — |
| `TA-X-18` | **CARRIED** (v1.10's re-derived value, recomputed on the oracle: `(-3.999999999999985, -3.49691120014899e-07)`) | none | the oracle call reproduces bit for bit |
| `TA-X-19` | **CARRIED; ARM (a8), all 25 cells** | none | — |
| `TA-X-20 / 21` | **CARRIED** (probe / source scan; no arm) | none | `NORMAL_PTH_DIVISOR` is now also a `k12` row (`IC7-Q-0387`), already on the wire as `H1-CONST`; no row reads it (§ A.4) |
| `TA-X-22 / 24` | **CARRIED; ARM (a8), all 25 cells** | none | `TA-X-24`: ⚑ NOTE `r9` (§ A.4) |
| `TA-X-25` | **CARRIED; ARM (a8), per arm per salt** | none | — |
| `TA-X-26` | **CARRIED** (no fight run); (e) recomputed `0.2468965517` / 17 | none | (b) as v1.10 § A.4; OQ-15 open |
| `TA-X-27` | **CARRIED**; (c) **ARM (a8), all 25 cells** | none | ⚑ NOTE (§ A.4): `CONTROL_GATE_RNG_SALT` (`IC7-Q-0073`) is on the wire, and the oracle draws nothing from its stream on any graded arm |
| `TA-X-28` | **CARRIED; ARM (a8), all 25 cells** | none | ⚑ NOTE `r9` (§ A.4) |
| `TA-X-29` | **CARRIED**; (e) recomputed `3.207764` / `4.980316`, 39 / 39 per-record values exact | none | ⚑ **(e)'s walk is now defined by the pack: `a8` job `WALK` (`IC7-A-0379`…`0432`)** |
| `TA-X-30` | **CARRIED; ARM (a8), all 25 cells** | none | — |

**Per-row delta in expected value: NONE, on all 28 EXACT rows and the five preconditions.** Gradeability changed by
declaration: **NONE.** Tolerances changed: **NONE.**

### 0.3 · Diagnostics, report face, verdict file

| site | v1.11 | why |
|---|---|---|
| `TA-B-01` terminal wave | **CARRIED: `[156, 152, 155, 152, 152]`**, `player_death` 5/5, arm `M-POL-2` (§ B.1a, now cited to `a8`) | — |
| ⚑ port-generator note | ⚑ **NEW, DIAGNOSTIC ONLY, NOT GRADED:** salt 1 clears to w160 on the port's own generator; what n = 5 can and cannot say (§ F.3a) | KP-152 flag |
| `TA-B-15` | **CARRIED** (10/466 = 0.021459) | NONSWING-10 reproduces |
| `C-e / C-f / C-i` | **CARRIED** | the oracle is unchanged |
| `C-o` | **CARRIED.** It does not cover `TA-X-18` (v1.10 § A.5) | — |
| § F.3 / § F.5 sentences | version label only | — |
| verdict file | `prereg_version: "v1.11"`; `substrate_epoch`; both pack pins; `arm_of_record` with `a8` citations; `closure_H10` = discharged; ⚑ `r11_budget` | § G.3 |
| § G.1 counter | **`0` of `2` under v1.11** (carried unspent) | — |

### 0.4 · The counts

| | preconditions | **EXACT** | UNGRADEABLE-declared | DIAGNOSTIC ids | emitted-not-graded |
|---|---:|---:|---:|---:|---:|
| v1.10 | 5 | 28 | 1 (`TA-X-06`), closed | 19 (0 gating) | 3 |
| **v1.11** | 5 | **28** | **1 (`TA-X-06`), closed** | 19 (0 gating) | 3 |

⚑ **Q87's *"all EXACT rows green"* at v1.11 means the same 28:** `TA-X-01 · 02 · 03 · 04 · 05 · 07 · 08 · 09 · 10 ·
11 · 12 · 13 · 14 · 15 · 16 · 17 · 18 · 19 · 20 · 21 · 22 · 24 · 25 · 26 · 27 · 28 · 29 · 30`. **No row added or
removed.** `TA-X-23` stays struck and retired. The port-generator note of § F.3a is not a DIAGNOSTIC id; it is a
printed note.

### 0.5 · What v1.11 deliberately does NOT fold in

1. **Any remedy for R-11** (§ F.2k.6). The conductor chooses; a chosen remedy that re-keys clause (c) is a new
   dated prereg version committed ALONE, and by v1.8 § F.2d case 2 its question is Matt's.
2. **The KP-144 (b) loop-layer systems as `P-5` settings** (OQ-14, open).
3. **A widening of `TA-X-26(b)`** (OQ-15, open).
4. **`C-h` / `OQ-9`**, **`C-k` / `OQ-11`**, **C-11b and REFERENT-v2**: not here, for v1.9's reasons.
5. **A ruling on the port-generator salt-1 clear** (§ F.3a). It is a Gate-2 question, printed here as a diagnostic.

---

## ⚑ PINS: EVERY PIN COMPUTED THIS SESSION, FILLED BY SCRIPT, NONE TYPED

> **The standing rule (KP-20, KP-43):** a new version recomputes every pin it carries, including the ones it
> believes are unchanged. **All carried pins reproduce v1.10 exactly.** Both pack digests are recomputed from the
> member files with the manifest's `pack_digest_law_exact`, every member's FILE digest and byte count checked
> against its manifest row, the on-disk member set checked equal to the manifest's (no extra file, none missing),
> and the result compared to the manifest's `pack_digest`. They agree.

| # | artifact | label | **sha256 (computed 2026-10-01)** | v1.10 → v1.11 |
|---|---|---|---|---|
| P-a | `gamora/notes/2026-09-20-kc2-play-ta-band-widths.md`. Constructions only; every width VOID | FILE | `1c80f08075a1ed0e30e30b348752d2505b39994f7e2c55c348413f6e591248f9` | unchanged (reproduces v1.10) |
| P-b | `galadriel/notes/2026-09-20-kc2-play-w1-tb-expected-values-and-u-rider.md` | FILE | `d48512aa6e3c9ea70de6675750880a6c8914f0984c3cfe65c6ccb9a24403438f` | unchanged (reproduces v1.10) |
| P-c | `…/2026-09-20-kc2-play-w1-tb-expected-values.json` | FILE | `a8b85331764ba3fe90f45cf7cd6f1a25f6dc0dae4a7e7fa555c487f0b153ea0b` | unchanged (reproduces v1.10) |
| P-d | `…/2026-09-20-kc2-play-w1-tb-release-labels.json` | FILE | `15dace604c8d5bb4888223a8b25a07a038bae44431ebd194d682545c0f29c58a` | unchanged (reproduces v1.10) |
| P-e | `simulation/math/kc2-play-v3p4-roster-basis-rebase-2026-09-21.md` (lineage) | FILE | `4b7b78c834c7fbabd61700dda3e730a95ab89990bfa01470e8fb293f41ac7a73` | unchanged (reproduces v1.10) |
| P-e′ | `…/math/kc2-play-v3p3-monster-offense-prereg-2026-09-20.md` (lineage) | FILE | `27fc59378aee8c9d412f486a63864a3b2ceb5c5473520b60ad80128d47d99cdc` | unchanged (reproduces v1.10) |
| P-h | ⚑ **THE MODEL PACK** `kc2-model-pack-v3-E-s09-cp150-mech-v3p7p1-20261001_021247` (19 members, 19/19 verified: digest and bytes) | PACK | `48a4c94c165715d3f4f5db89c1278aa8439fbe1507c39dd555f7ce91d4636c96` | ⚑ **RE-PINNED** v3.7 `9bee0357…` → v3.7.1 |
| P-h2 | ⚑ **THE REFERENCE PACK** `kc2-reference-pack-v3-E-s09-cp150-mech-v3p7p1-20261001_021247` (7 members, 7/7 verified); `cross_pin.model_pack_digest` verified equal to the derived model digest | PACK | `1887257f5370443a1729fde2ff446579b1acc501dcd03679244297b541e3e5b1` | ⚑ **RE-PINNED** v3.7 `978bb893…` → v3.7.1 |
| P-i | `data/kc2/pm4p_leech_resistance.csv` (imaged as `IC7-F-44`, a column projection; v1.10 § A.4) | FILE | `cb6a008bde1e102573181968ab7f60958cd28fee07ff8736078fa092a80dd62e` | unchanged (reproduces v1.10) |
| P-j | `data/kc2/pm4l_mitigation_by_body.csv` (lineage) | FILE | `a8c1ffd97dc703419f8447f3d7bbba3903e0f14d2c2e6746a938ceefae9ecec6` | unchanged (reproduces v1.10) |
| P-k | `data/kc2/pm2_tg2_monster_timing.csv` (`ANCHOR-169`'s carrier) | FILE | `58205679e36f0e0361ccd41c844d6bc254ada034447dd1f80e2a46a2b47c7aca` | unchanged (reproduces v1.10) |
| P-l.c2 | `simulation/math/kc2-c2-per-cast-energy-cost-fold-2026-09-28.md` | FILE | `b42684e55325bd4caf705b1e7d43462acb5c5818cd5abe3d79eb0d3b9ba6f8c7` | unchanged (reproduces v1.10) |
| P-l.c7 | `…/kc2-c7-insufficient-energy-refuse-fold-2026-09-29.md` | FILE | `072f9ab787ec840a9bc62ae76a0576fa5db7be0da0b63457851557ea164a7e1f` | unchanged (reproduces v1.10) |
| P-l.nine | `…/kc2-play-nine-winner-surface-reconstruction-2026-09-29.md` | FILE | `2c7c3679af67569fff88bb56837ea1ba37499fe9fcbeca85ab63a473b0d7a6dd` | unchanged (reproduces v1.10) |
| P-l.upn4 | `…/kc2-play-upn4-occupancy-by-pilot-2026-09-29.md` | FILE | `787d1a99d9adfedbb34bda69a3c530a653a8df3fc117969e3920c5625791a3cf` | unchanged (reproduces v1.10) |
| P-l.upn5 | `…/kc2-play-upn5-global-magnitude-fold-lift-2026-09-29.md` | FILE | `bfa44b4722ec8b7326987042101f32310c986e3fae489a4372fcc4e0dd5553c7` | unchanged (reproduces v1.10) |
| P-l.upn5A | `…/kc2-play-upn5-global-magnitude-fold-lift-ADDENDUM-2026-09-29.md` | FILE | `5323c1fa9f156e80ced5b1324e4297150cfc759c4e54426f440c33a6c9745fc6` | unchanged (reproduces v1.10) |
| P-l.q91 | `…/kc2-play-q91-338-pool-damage-lift-2026-09-29.md` (governs `TA-X-25` and `P-5` setting 3) | FILE | `d68561d59723c3295da3f0456f2fbeaefe8f5f0a30b41d29b5ff0e366966a385` | unchanged (reproduces v1.10) |
| P-l.q91a | `…/kc2-play-q91-338-pool-damage-lift-ADDENDUM-2026-09-29.md` | FILE | `b9ada804e17c01b376e64e82b7e45f66a344d1fc2fc75a0fdd1fd76c56e2cddc` | unchanged (reproduces v1.10) |
| P-l.c11a | `…/kc2-play-c11a-oracle-corrections-fold-2026-09-30.md` (governs `P-5` setting 11) | FILE | `4af38999ff0544cc9607b34da4fde29fe2c55324e9829894c516cd9837689445` | unchanged (reproduces v1.10) |
| P-l.c11aA | `…/kc2-play-c11a-oracle-corrections-fold-ADDENDUM-2026-09-30.md` | FILE | `17a068fe980869e6e344fdf3a652dc275f5cc3a3d65818f2976fe94084d48666` | unchanged (reproduces v1.10) |
| P-n.1 | `simulation/output/kc2-play-q91-pool-lift-pricing-20260930_023137.json` (the `M-POL-2` seat) | FILE | `f33ce0c0cbeb00bbed7b47a6f7660f20d4aa2be1694f9f4e2486e37d27b553e2` | unchanged (reproduces v1.10) |
| P-n.2 | `simulation/output/kc2-lifted-rows-KC2PLAY-SEALLAP-W1-c2-energy-fold-20260928_232836.json` (the `x8` input; `a8` `IC7-A-0454` names this path) | FILE | `cc361a3fea3e24e55fdf0c8c8eaf52bcc0c729c7de0563d3c84dd0dc21202960` | unchanged (reproduces v1.10) |
| P-n.3 | `simulation/output/kc2-play-c11a-fold-pricing-NOT-A-GRADED-RUN-20260930_043045-SUMMARY.json` (`TA-B-01`'s reference: the `M-POL-2` seat; `C-f` / `C-i`) | FILE | `b6c9e7953f5b5632ec2dc51c2c8602461aef15d4721f69432444e6f777e1141e` | unchanged (reproduces v1.10) |
| P-n.4 | `simulation/output/kc2-play-c11a-landed-by-source-NOT-A-GRADED-RUN-20260930_033242.json` | FILE | `ad018b78a7f85491020a237166af797845bb5de2e562816673fbf925bb41ff1e` | unchanged (reproduces v1.10) |
| P-o | `data/kc2/c11a_aura_buff_grants.csv` (the C2 grant table; imaged as `IC7-F-04`) | FILE | `749d58f45eb312e7a284734a1844f2aabcfd69b7219dd1dafc55e4bb6d64792f` | unchanged (reproduces v1.10) |

### Set digests: the populations v1.11 grades over

**Law:** `sha256("\n".join(sorted(record_paths)).encode("utf-8"))`, no trailing newline. **ROWSET.** Recomputed this
session on the v3.7.1 tree: POOL-466 by both routes of `kc2_baton_v3p5p1_schema.pool466` (routes agree);
SWING-456 / NONSWING-10 as `ThreatProfile.can_swing` over POOL-466 from the oracle's `load_profiles` under
`P-5`'s exact loader call (the call `a8` `IC7-A-0453` records); FALLBACK-158 from `derive_oracle_speeds` (partition
180 / 158 / 128 = BANDA-DB-CITED / FALLBACK / LAPR-MEASURED, `march_base` 3.209466).

| set | n | label | sha256 | v1.10 → v1.11 |
|---|---:|---|---|---|
| **POOL-466** | 466 | ROWSET | `33c886a11f91db1143c791ffcf9d95f7e7614e423373235231733c994c5c157b` | reproduces v1.10 |
| **SWING-456** | 456 | ROWSET | `706a61d55dc6621814fc923d7428c5b263a95ebb00e9786d12f35dd385a7a4c0` | reproduces v1.10 |
| **NONSWING-10** | 10 | ROWSET | `00b4cb0e24b43e591a2e30200979725801aad1e7c1f9b7764ebef67461816e10` | reproduces v1.10 |
| **FALLBACK-158** | 158 | ROWSET | `e8114efaa8fa678db6a26bb6e4ffb926fc2c1a15a978e3d589cf918ff17ae6cb` | reproduces v1.10 |

### Documents of record

| document | label | sha256 |
|---|---|---|
| ⚑ prereg **v1.10** (superseded, **not edited**; v1.11's only predecessor; collab `690865868`) | FILE | `b1dd68efe2ce6009c2981d1c25bb182aba8c444945ec81f53a5c3c0c8b79061c` |
| prereg v1.9 (not edited; collab `d52193c72`) | FILE | `b787308c8c331e98fee6221c97174bf8f696a5b55d699611c5ab697625de95dd` |
| prereg v1.8 (not edited; collab `948bb8082`; § F.2d: R-11's law for both outcomes) | FILE | `69e1de1890a24fb9d9a4dc37cda6edfc39e6c34e45b877a2999b565b4710c49c` |
| prereg v1.7 (not edited) | FILE | `552d9faecd83d955c77f2be35991ec51e3908d9f586ab70b5a78b6c156b92896` |
| prereg v1.6 (not edited) | FILE | `db2c0ca3c6cdba022b83d0229439a3ad9e0709cd25732304ffc979a200be7b0e` |
| ⚑ prereg **v1.5** (not edited; ⚑ § F.2d clause (c): **where the 4,500 budget was derived**, § F.2k.1) | FILE | `efac4bd51f2d2c1f1130a58c85f37d1c7738e51ac15afd3c70930f7ac3eef143` |
| jack-ryan's v1.8 pre-read (R-17…R-22) | FILE | `5358cb8cc99dcf1dd998e875e911d6ae53e9046dab0d24abe28a5c83193d5dff` |
| jack-ryan's v1.7 pre-read | FILE | `ff1df4a18e9e60c1a5543edb391eded667b11711b340cd4763f3cdd204cab1ff` |
| jack-ryan's Gate-2 on attempt 1 (R-1…R-12) | FILE | `d2aa93db92122e033927f63ff61c9e6a2c13e1c7cba09a4fff20cb2382de6c37` |
| attempt-1 grade note | FILE | `9778b4de4aa05acb2396439d2ff9de264ec590475ebf56aec93f3912ba12505e` |
| attempt-1 verdict file | FILE | `9be2d56bfdc49c51c611402ec953b5f59dbfc0c866cdaf5201e0e57d74df08b2` |
| jack-ryan's v1.6 pre-read | FILE | `5a5f45d76098746ce1dbd31d0091b9a7d62f16978fb52a21ff27990181e0b6c0` |
| the grade of record (`gamora/notes/2026-09-21-kc2-play-ta-grade.md`) | FILE | `600f68a7378329c298cd69863903804a6ab7d1ee8a27f666688717f741b9c1c3` |
| the discrimination audit | FILE | `852d0bd7d637280cbc42e2ba8494ea7e163b4f6c91741f24eb0ef3da105e674a` |
| divergence register v0.3 (file form) | FILE | `5028b555313df2f4690cd96881c700c7d66a4733612894c150c2448915510444` |
| `H-9` evidence: `NOTE.md` (collab `dccc7d8ff`) | FILE | `90717b83926f06b5939a48c01c0cc4973d5f20d7d7eb60007b976d01ebde53e5` |
| `H-9` evidence: `h9_out_W1.json` | FILE | `c68fcd3c133c8b8a55d75e85425876fe73d6d1752dfdd1cd21fa9041e87a24ff` |
| `H-9` evidence: `h9_out_M-POL-2.json` | FILE | `2aedf43f2091d0c575af1d7d07deb0278be87f0b4c917efa5c33d01e77707f61` |
| `H-9` evidence: `h9_out_W1-NULL.json` | FILE | `90b9ea619e8adfd3f8532cc55e16990c15348dd537071c5758000c2edafdf801` |
| `H-9` evidence: `h9_w1_containment.py` | FILE | `eede32e85f362b5d57b136b81344cae1bfd4b804515db2d6f2d66279d1920f55` |
| star-lord's v3.7 cut prereg (engine `fdd7c61f`) | FILE | `ccf17ae6ffd06cb17d72ee88e34657fef8a1a16a70839b8ad091e4fdb1f7db05` |
| the v3.7 cut receipt (engine `54968275`) | FILE | `5de7beb2b4c3ad5ab4325fc372783977c86fd1fcd2750d78ccf94c6514baaf98` |
| v3.7 closure table BEFORE | FILE | `e6eeadb42e6928b9d45d2242b0b6cc81ee720709b95148efe8c17184757253b4` |
| v3.7 closure table AFTER | FILE | `e9a5c05e164172b5514e2fa1c323da243bee6fa7e7dc878ade4f4651eebc3805` |
| ⚑ the H-10 run on v3.7 (`output/kc2-v3p7-h10-summary-20261001_001232.json`, engine `93f875d9`; NOT PASS, KP-150) | FILE | `ff81fc9146e86be6c9fc5ad233ef8841ca22feb1bb50f7e9d5667d9beee85e30` |
| ⚑ the v3.7.1 PRE gate and dry run (`output/kc2-v3p7p1-PRE-gate-and-dry-run-20261001_PRE2.json`) | FILE | `fce6a344860e4f539763b08c6320160260e77c28f007ced00d25af7fa8456cbe` |
| ⚑ star-lord's **v3.7.1 cut prereg** (`export/math/2026-10-01-kc2-pack-v3-7-1-closure-law-prereg.md`, engine `67b18f90`) | FILE | `f96bfade2bb9968a943c42b0639cd5fe7f0aec29ad2cf177983c7896a4d4bf0f` |
| ⚑ the **v3.7.1 cut receipt** (`output/kc2-baton-v3-cut-receipt-v3p7p1-20261001_021247.json`, engine `27659b01`; verdict PASS; **`H-10`'s discharge**) | FILE | `a0ad8246ac49628f8bd729c8cc2fba564b6456c4c06df0ae300e0439bfc447c9` |
| ⚑ the closure instrument `export/kc2_v3p7_closure.py` at engine `22cd2288` (supersedes v1.10's `964bfce7…` pin and KP-150's `4c1221b5…`) | FILE | `e5793c281aa86e18e128983883ee8f26d5e5615e6803a1cf682dc49f13a57284` |
| ⚑ the v3.7.1 law `export/kc2_v3p7p1_law.py` | FILE | `2c24ea92dacd259cd4e989fa09cdc08c9f6c91f5b18f49ac17ad6b9b800b008e` |
| ⚑ oracle terminals, instrument-free, `M0` (`output/kc2-v3p7p1-POST-bare-M0-20261001_021247.json`) | FILE | `9cdbd93ca8ca7d35cf39a95ea66eaf9509a89cd430a9f8d415fac4bc7fb7c2fb` |
| ⚑ … `M-POL-2` | FILE | `691ea754633b5ad582c01beb69b0935ef390c803136a76d7b7d6129277423689` |
| ⚑ … `M-POL-2-NULL` | FILE | `c856f83259ca7ea62a0189031e7bd5a47a9bcba66e441da7fb8e55783a0f1f7f` |
| ⚑ … `W1` | FILE | `a6df79289abe349b7e62e6465b749fea26e35107552348bdd9cfe634258d6b32` |
| ⚑ … `W1-NULL` | FILE | `c08fd789a5787bc5660197d90413e7ff6da7868a30a552ec4203a867b5494b59` |
| ⚑ **the port's conservation code, READ for § F.2k** (`reincarnated-godot` HEAD `ffb454e`, read-only; HEAD blob = working tree): `kc2_runtime/sim/kc2rt_fight.gd` | FILE | `e6903095b6bba83f38359a654380cb5b13516c8e2a437b2a04ae1ff73c72a680` |
| ⚑ … `kc2_runtime/sim/kc2rt_laws.gd` | FILE | `406ffeca427bf90bb6b998eba834138eb7f68b76917f95e70fabf72ba523e1b3` |

### Sealed cells: hash-verified only. K-7 held (never opened for execution, never re-run)

| cell | path (`reincarnated-engine/src/reincarnated/simulation/output/`) | label | sha256 | bytes |
|---|---|---|---|---:|
| `[M-POL2]` | `kc2-checkpoint-E-s09-cp150-mpol2-20260825_114420.json` | FILE | `ad61ad2a8c799d6ef11a68436756c253f0a34fbb1052e575cdf9f9cd3a44dc5c` | 123,564 |
| `[MECH]` | `kc2-checkpoint-E-s09-cp150-mech-20260816_124031.json` | FILE | `20b05cb4ef3bd888b998cbc46c68b41a8051111c12fbcf2066d101b0a4b15f4b` | 2,125,271 |
| `[W1W]` | `kc2-checkpoint-E-s09-cp150-w1walls-20260825_220058.json` | FILE | `7a992c81ca6e56e54a53534b438a9ddf87ed42f1bf1a3d0ecc2d2f3c3db7881b` | 403,084 |

---

## § A · WHAT MOVED, DERIVED

### A.1 · The pack, member by member (v3.7 → v3.7.1)

**Model: 16 of 18 carried members byte-identical; 2 moved; 1 added.** Derived from the member files, not
from the cut's receipt:

| member | v3.7 → v3.7.1 (FILE) | what changed |
|---|---|---|
| `input_closure.json` | 273baca8… → 13be3550… | ⚑ four `k3` rows WITHDRAWN (`IC7-K-0036 · 0037 · 0038 · 0255`); top-level keys that differ: `⚑ v3p7_rows`, `⚑ v3p7p1_withdrawn_rows` |
| `input_closure_v3p7p1.json` | — → d1b75980… | ⚑ **NEW MEMBER** (891 rows, six rowsets, § A.1) |
| `meta.json` | 28a9b889… → 8fe51d80… | keys that differ: `emitted_at_utc`, `emitted_by`, `headline`, `pack_revision`, `⚑ v3p7p1_closure_law`, `⚑ v3p7p1_supersession` |

**Reference: 6 of 7 byte-identical; 1 moved:** `reference/meta.json` (2580495a… → 25c2be7e…; keys that differ:
`emitted_at_utc`, `emitted_by`, `headline`, `pack_revision`, `⚑ v3p7p1_closure_law`, `⚑ v3p7p1_supersession`). `waves.json`, `arena.json`, `monsters.json`, `monster_offense.json`, `monster_defense.json`,
`monster_kinematics.json`, `controllers.json`, `math_rules.json`, `rng_contract.json`, `player_kit.json` and
`config_of_record.json` are **byte-identical**, which is why every value below recomputes to v1.10's.

**The six new rowsets of `model/input_closure_v3p7p1.json :: ⚑ v3p7p1_rows`** (member FILE `d1b759800a5709d09170a956c5dea759d80bf69e51a30781db7d16a78e49aadb`,
2,339,790 bytes), ROWSET digests recomputed by the pack's law (`sha256(json.dumps(rows, sort_keys=True,
separators=(",",":"), default=str))`). Each equals the digest on the wire (`meta.json :: ⚑ v3p7p1_supersession`):

| rowset | rows | label | sha256 |
|---|---:|---|---|
| `a8_composition_calls` | 459 | ROWSET | `7a2e5b3dbe40c2505050dc857bab1612b440c598021be0777f3dbf6492639af4` |
| `e13_static_sweep_exemptions` | 6 | ROWSET | `156c96dc3eea9f5b08cf381bedd19e6c3adc67e905c9f459715ce1e463499eec` |
| `k12_static_sweep_constants` | 406 | ROWSET | `a23c551443c1fc224ea8d02a9adb5137964a66f7d89ffa2ea8d668ebdb7546c9` |
| `r9_read_absent_columns` | 12 | ROWSET | `4f07aab93b321e3e4ced55bb1792673d2372c04ecc8b44dbb1b68799b4d82534` |
| `s10_run_state_e6` | 4 | ROWSET | `85d35a3e8b4b578c4748799f44ff5e4f0ca42b55e8500b4596f1ff637134417a` |
| `w11_withdrawals` | 4 | ROWSET | `429955b3f687400062b28e3fe88e1aa7cdf53e37b165d90d64528fc6278cfefa` |
| **all v3.7.1 rows** (the whole `⚑ v3p7p1_rows` object) | 891 | ROWSET | `cb43d84e29a9533deca2d4b0bdb6996d82e6171693fe5cd68f7a0928f14e3059` |

**The seven v3.7 rowsets inside the MOVED `model/input_closure.json`** (FILE `273baca8…` → `13be3550f65ef9b57f14ddee26c43b94296862fe94d221847bdc02c8e22e1b4f`), same law.
Checked by script: the v3.7.1 `k3` equals v3.7's `k3` with the four withdrawn rows removed, **verbatim and in
order**, and each withdrawn row appears verbatim in `w11`:

| rowset | rows v3.7 → v3.7.1 | label | sha256 (v3.7.1) | vs v3.7 |
|---|---|---|---|---|
| `c5_class_constants` | 4 → 4 | ROWSET | `4e65efdc89ddd0da3f5f00625833f4df1e0c98551965d56a51975f06a596ee7d` | identical to v3.7 |
| `d4_defaults_via_omission` | 711 → 711 | ROWSET | `9ef59a4ac5d9726d0afa74cab9e8600ca0c81f9ce1e1537b0139b5324da36758` | identical to v3.7 |
| `f1_file_images` | 51 → 51 | ROWSET | `1b0eeec7ad68c4ca5987bed70532ae3504ef031a0b284940c5c6928972682776` | identical to v3.7 |
| `k3_code_constants` | 612 → 608 | ROWSET | `ad6dc0a5f98da58c5c95864e69807f82a02841c79ed75c8ab8a26c13ed2e2d9c` | ⚑ MOVED (v3.7 `51714f64…`) |
| `p2_reader_products` | 11 → 11 | ROWSET | `cb6d43ab8573f6609799f93a7f51649ae7c5c1b076009ed32853cc30a2ed05db` | identical to v3.7 |
| `t6_text_corrigenda` | 5 → 5 | ROWSET | `38580e85d38deaa84d990c21bde85c1059c0e08a9cdd561803f8f9a526951761` | identical to v3.7 |
| `x7_derived_crosschecks` | 12 → 12 | ROWSET | `61c0eadfa2292c4efc91c8df7b44c6bccee7a2cc412cf44736db1957769b6fa5` | identical to v3.7 |
| **all v3.7 rows, as carried in v3.7.1** | | ROWSET | `87cfba658f2f2d37f55fc714e41d4a08026831c0c3eb867ed79171b704b0127a` | ⚑ MOVED (v3.7 `130c578e…`, v1.10 § A.1) |

### A.2 · ⚑ The oracle did not move, and neither did anything it reads

* `git diff --quiet eee8ce8b 22cd2288 -- src/reincarnated/simulation src/reincarnated/data data` exits **0**; so does
  the same diff from `266714dd` (v1.9's HEAD). The 137 paths changed since v1.10's HEAD lie under
  src/reincarnated/export, src/reincarnated/output, tests only. **The oracle's `kc2/` tree is git tree object `d974998f805b8bc5d620f27d88dd4e8f14972357` at both `eee8ce8b` and
  `22cd2288`** (a git tree id, an identity only). The working tree is clean on `simulation/kc2` and `data/kc2`, and
  carries no tracked modification under `simulation/`, `src/reincarnated/data/` or `data/`.
* **The closure-read files, re-hashed on disk this session:** every `f1` (51) and `p2` (11) row's source file equals
  the FILE digest the row carries: **62 / 62** (7 in `reincarnated-collaboration`, the rest in the engine). The
  `f1` / `p2` rowsets are identical to v3.7's (table above). The four files that carry the `r9` read-absent
  columns (`pm2_tg2_attack_damage.csv` · `pm2_tg2_attack_slots.csv` · `q91_pool338_attack_damage.csv` · `q91_pool338_attack_slots.csv`) are among them (`IC7-F-19` · `IC7-F-20` · `IC7-F-47` · `IC7-F-48`).
* **Recomputed anyway**, because a byte identity proves the input did not move, not that the reading of it was
  right; each value below was asserted equal to v1.10's by the script that filled this file:
  * POOL-466 / SWING-456 / NONSWING-10 / FALLBACK-158: all four set digests reproduce;
  * `TA-X-29(e)`, config E: **`3.207764` at w159, `4.980316` at w160**; all 39 per-record ratios equal v1.10's
    exactly; the ten-wave walk reproduces (`3.353866 · 1.768566 · 1.899330 · 2.994929 · 1.927777 · 2.846875 · 1.979824 · 1.592632 · 3.207764 · 4.980316`);
  * `TA-X-26(e)`: ARMED-464 mean `0.2468965517`, 17 leech-immune;
  * `TA-X-10`: `43.758085029822276` off the v3.7.1 `arena.json`;
  * `TA-X-18`: the oracle's `SpawnStructureFold().offset` at `u₁ = u₂ = 0.5` returns `(-3.999999999999985, -3.49691120014899e-07)`, v1.10's value, and the
    V9-SITE-14 wire constant equals the oracle's `FACING_SPAN_RAD`;
  * `TA-X-09`: the nine graded vectors' ROWSET `0e692765`.
* **`TA-B-01`'s reference `[156, 152, 155, 152, 152]` stands** (arm `M-POL-2`). star-lord's instrument-free v3.7.1
  POST run reproduces it (§ B.1a).

### A.3 · ⚑ THE FOUR WITHDRAWN ROWS, READ AGAINST EVERY GRADED ROW

Every row of the v1.10 instrument, and every derivation this file carries, was checked for a citation of, or a
dependence on, each withdrawn row. **v1.10 cites no `IC7-K` row by id**, and neither does this file except here.

| withdrawn row | binding | class (KP-150 / KP-151 / KP-153) | graded rows that read it | Δ |
|---|---|---|---|---|
| `IC7-K-0036` · `0037` · `0038` | `alert._INCIDENCE` · `_ROWS` · `_TABLE` | **E7, lazy-load cache**: `None` at import, assigned once inside its own guard from `p2` `IC7-P-05` / `f1` `IC7-F-05` | **none by citation.** Every fight row reads the alert layer only through the fight. The oracle always built these from the same files; the port now builds them as the code does (MIGRATION § 1) instead of loading a copy | none |
| `IC7-K-0255` | `locomotion._FALLBACK_HITS` | **E6, run-state accumulator** (34 records / 421 hits accumulated over the W1 + M-POL-2 run) | **none.** ⚑ **FALLBACK-158 is NOT this quantity.** FALLBACK-158 is the set of POOL-466 records whose speed comes from `locomotion_for`'s declared fallback (the `from_fallback` partition of `derive_oracle_speeds`); `_FALLBACK_HITS` counts fallbacks TAKEN during one run. `derive_oracle_speeds` never reads `fallback_hits()` (checked); the set digest reproduces (§ A.2) | none |

### A.4 · ⚑ THE NEW ROWSETS, READ AGAINST EVERY GRADED ROW

`model/input_closure_v3p7p1.json` carries **inputs and declarations**, not graded quantities. No EXACT row's
expected value is derived from any of its rows. Where a row meets one:

* ⚑ **`a8` (459 composition calls): THE ARMS AND THE WALK.** § B.1a now cites them. This is the KP-150 ruling-2
  change, and the only place v1.11's text changes how a row is RUN: **a row graded on an arm configured otherwise
  than by that arm's `a8` rows is graded on a different arm**, and § G calls that C1. The K_MILL pilot's
  `px_arm_label = "PX-LO"` is on 51 rows (KP-152 item 2), including the ten `KinematicsFold` rows of every arm.
* ⚑ **`r9` (12 read-absent columns):** `skill_radius` (both attack-damage files) and `expansion_time_s`,
  `projectile_explosion_radius`, `skill_target_radius`, `wave_start_width`, `wave_end_width` (both attack-slots files),
  read by `.get` with default `None` at the threat extent law (`threat.py:741-779`). **No row's expected value is
  derived from them.** Rows whose run-internal statistic passes through monster reach (`TA-X-24`, `TA-X-28`, and
  every all-25 row through the fight) are affected only in that **the port must run the oracle's `None`
  default** for those columns, which is how the oracle has always run. A port that substituted a value would
  diverge, and G3 is the instrument that sees it (H-1).
* **`s10` (4 run-state declarations: `IC7-S-0001` `_INCIDENCE` · `IC7-S-0002` `_ROWS` · `IC7-S-0003` `_TABLE` · `IC7-S-0004` `_FALLBACK_HITS`):** *not inputs*; the port must not load them. Read by no row.
* **`w11` (4 withdrawals):** § A.3.
* ⚑ **`k12` (406 static-sweep constants).** Two meet a row:
  * `control_application.CONTROL_GATE_RNG_SALT` = 46373536579806 (`IC7-Q-0073`) seeds the control gate's DEDICATED stream
    (`control_application.py:786`). **It was absent from v3.7's `k3`, and v3.7's dynamic capture read 0 constants
    NOT IN PACK on every one of the seven jobs** (v3.7.1 prereg § 0, BEFORE table). So the line that reads it did
    not execute on any graded arm: **the oracle constructs that stream on no graded arm and draws nothing from
    it.** `TA-X-27(c)` (*the port consumes exactly what the oracle consumes, none where the oracle takes none*) is
    unchanged in form and covers it: **a port that draws from the control-gate stream on a graded arm is red on
    (c).** Named for H-1 because pass 3b puts the seed on the wire (KP-153).
  * `threat.NORMAL_PTH_DIVISOR` = 70.0 (`IC7-Q-0387`), already on the wire as `H1-CONST`. No row reads it.
* **`e13` (6 named exemptions):** the four run-state bindings and two typing constructs (`fixture.T`,
  `geometry.Blocker`). Read by no row.

---

## § B · CONFIGURATION AND PRECONDITIONS: five

### B.1 · `ORACLE` *(carried from v1.10 § B.1)*

`V0`, five arms (`M0`, `M-POL-2`, `M-POL-2-NULL`, `W1`, `W1-NULL`), five salts, **25 headless runs**, the limbs of
record, `v_ref` 4.0 → 5.4 m/s, motion law `V0-04`, declared fight scope waves 151–160, leg A (stop at the player's
first death). **Pilot:** U-P-N-4's `SEALED-KMILL` (`DRIVE_TO_PACK`, `seek_fold=True`, `kinematics=True`). The
runtime prints its resolved limb set (`v0_limb_set`), diffs it against `V0` before any row is read (V0-37 =
`MotionLimb.GATE_FIRST (L-B)`), and refuses to boot on an unset limb. ⚑ **At v1.11 every one of these settings is
also on the wire as `a8` rows** (§ B.1a), and the pilot rows are cited there per arm.

### ⚑ B.1a · THE ARM OF RECORD, PER GRADED ROW, AND THE `a8` ROWS THAT DEFINE EACH ARM

**The arm question is carried from v1.10 § B.1a unchanged in substance** (`TA-B-01` = `M-POL-2`, on v1.10's four
grounds). **What v1.11 adds: the arms are no longer defined by this file's prose. They are defined by the pack.**
Each arm is the `a8` job of the same name, plus the shared `setup` job. This file cites those rows; it does not
restate them. **A harness that configures an arm from anything other than its `a8` rows is not running that arm.**

**ROWSET law for one arm's rows:** the pack's law applied to that job's `a8` rows as a list ordered by `id`:
`sha256(json.dumps([rows of job J, sorted by id], sort_keys=True, separators=(",",":"), default=str))`.

| arm (`a8` job) | `a8` rows | n | ROWSET (job rows) | the rows that DISTINGUISH the arm (read off the pack by script; each assertion was checked) |
|---|---|---:|---|---|
| **`setup`** (shared by every fight arm) | `IC7-A-0433`…`0459` | 27 | `c01d1ddaa4a5b7074203662522276a24a150312d9faeceb6634dc5438e0f71f1` | `P-5`'s loader: `threat.load_profiles` **`IC7-A-0453`** (`dot_corrections=True`, `c11a` scope CLASS, `pool_lift`, `winner_surface`; `pet_special_gates` = None), `C11aLoader(scope=CLASS)` `IC7-A-0435`, `WinnerSurfaceFold.from_x8(P-n.2)` `IC7-A-0454`, `pool_lift.load` `IC7-A-0446`; the tick-period probe `IC7-A-0458` |
| **`M0`** | `IC7-A-0153`…`0222` | 70 | `68549af0608cb9979771fcc4955ae8010f4f3516ad55a97b83922c994f571d12` | **no `ChannelPolicyFold` row and no `ArenaFold` row**; `replay(…)` `IC7-A-0208`…`0212` with `channel_gate_fold` OMITTED (default `None`); `run_cell(seat=False, arena=None)` `IC7-A-0218`…`0222` |
| **`M-POL-2`** | `IC7-A-0077`…`0152` | 76 | `e698d5f555a37fcc12e703343286d4e25c12662d8cd35c9571f9a0ac8ae45dbf` | **`ChannelPolicyFold(armed=True)`** `IC7-A-0089`…`0093` (one per salt) + `wrap` `IC7-A-0094`; no `ArenaFold`; `run_cell(seat=True, arena=None)` `IC7-A-0148`…`0152` |
| **`M-POL-2-NULL`** | `IC7-A-0001`…`0076` | 76 | `4393a14b56a97960ef42e73909a1cdefc49f3dc1a4cc41e7f20267b661a1a7b6` | **`ChannelPolicyFold(armed=False)`, explicit** `IC7-A-0013`…`0017` + `wrap` `IC7-A-0018`; no `ArenaFold`; `run_cell(seat=True, arena=None)` `IC7-A-0072`…`0076` |
| **`W1`** | `IC7-A-0301`…`0378` | 78 | `5188284d198c139422276e8ac92f9a0bee03cea7dbb1cea32c6c7bf1d19a55e8` | **`ArenaFold(armed=True)`** `IC7-A-0307` + `wrap` `IC7-A-0308`; `ChannelPolicyFold(armed=True)` `IC7-A-0315`…`0319` + `IC7-A-0320`; `run_cell(seat=True, arena=<ArenaFold>)` `IC7-A-0374`…`0378` |
| **`W1-NULL`** | `IC7-A-0223`…`0300` | 78 | `b2abff6978105bfc1566d678d5f1dea756ea9ef0eab02f8457821f81125a7fdd` | **`ArenaFold(armed=False)`, explicit** `IC7-A-0229` + `wrap` `IC7-A-0230`; `ChannelPolicyFold(armed=True)` `IC7-A-0237`…`0241` + `IC7-A-0242`; `run_cell(seat=True, arena=<ArenaFold>)` `IC7-A-0296`…`0300` |
| **`WALK`** (`TA-X-29(e)`, not a fight) | `IC7-A-0379`…`0432` | 54 | `63c530edd2e825c05f0f95ce2f629d56dbff98da206ddb45690fc129d7bba0f2` | `pools_for(w, bonus_spawns_enabled=True)` `IC7-A-0412`…`0421` (w151–w160); `fold_at(w, to_hit=True, attack_speed=True)` `IC7-A-0400`…`0409`; the `gmg` resolver `IC7-A-0423`…`0432`; `load_profiles` `IC7-A-0411` |

**The pilot, per arm (the same shape on all five):** `upn4._overrides(policy=DRIVE_TO_PACK, seek_fold=True, …)`
(`M0` `IC7-A-0213`…`0217` · `M-POL-2` `IC7-A-0143`…`0147` · `M-POL-2-NULL` `IC7-A-0067`…`0071` · `W1` `IC7-A-0369`…`0373` · `W1-NULL` `IC7-A-0291`…`0295`) and
`KinematicsFold(shape=K_MILL, px_arm_label="PX-LO", …)` (`M0` `IC7-A-0179`…`0188` · `M-POL-2` `IC7-A-0109`…`0118` · `M-POL-2-NULL` `IC7-A-0033`…`0042` ·
`W1` `IC7-A-0335`…`0344` · `W1-NULL` `IC7-A-0257`…`0266`).

**THE TABLE: which arm(s) each graded row runs** (rule carried from v1.10: a row whose statistic names arms grades on
those arms; a run-internal row that names none grades on every cell the graded run emits, 5 arms × 5 salts).
⚑ **The arms are now all inside the closure proof** (`H-10` discharged, KP-153), so v1.10's third column is
retired.

| row | arm(s) × salts | `a8` jobs |
|---|---|---|
| `P-2` | `M-POL-2` × salt 0 (port-only probe) | `setup` + `M-POL-2` |
| `TA-X-01` | one NAMED arm+salt ≠ (`M-POL-2`, 0), run twice | `setup` + the named arm |
| `TA-X-02` | no run (census) | — |
| `TA-X-03` | `M-POL-2-NULL` and `M0` × 0–4 | `setup` + `M-POL-2-NULL`, `M0` |
| `TA-X-04` | `W1-NULL` and `M-POL-2` × 0–4 | `setup` + `W1-NULL`, `M-POL-2` |
| `TA-X-05` | `M-POL-2` and `M0` × 0–4 | `setup` + `M-POL-2`, `M0` |
| `TA-X-06` | `W1` vs `M-POL-2` × 0–4: printed, not graded | `setup` + `W1`, `M-POL-2` |
| `TA-X-07` · `08` · `12` · `13` · `14` · `15(a)` · `16` · `17` · `19` · `22` · `24` · `28` · `30(b)` | all 25 cells | `setup` + all five arms |
| `TA-X-09` · `15(b)` · `18` · `20` · `21` · `26` · `30(a)` | no run | — |
| `TA-X-10` | `W1` × 0–4 | `setup` + `W1` |
| `TA-X-11` | `W1` and `W1-NULL` × 0–4 | `setup` + `W1`, `W1-NULL` |
| `TA-X-25` | per arm per salt, all 25 cells | `setup` + all five arms |
| `TA-X-27` | (a) scan · (b) per-seed replay · **(c) all 25 cells** · (d) pack census | (c): `setup` + all five arms |
| `TA-X-29` | (a)–(d) loader and pack; **(e) the static config-E walk** | (e): `WALK` |
| **`TA-B-01`** (DIAGNOSTIC) | **`M-POL-2` × 0–4** | `setup` + `M-POL-2` |
| `TA-B-15` (DIAGNOSTIC) | per arm per salt | `setup` + all five arms |
| R-11 (`H-6`, § F.2k) | ⚑ **every cell the graded run emits** (clause (c) binds per cell) | `setup` + all five arms |

⚑ **The oracle reference figures, by arm.** Read by script off star-lord's instrument-free v3.7.1 POST runs
(FILE digests in the documents of record; `P-5`, salts 0–4, leg A, composed from `a8`). They reproduce v1.10's
figures for `M-POL-2`, `W1-NULL` and `W1`, to the second.

| arm | oracle terminal waves (leg A), salts 0–4 | seconds into terminal wave | status in this file |
|---|---|---|---|
| `M-POL-2` | **`[156, 152, 155, 152, 152]`** | `[7.184, 4.408, 7.02, 7.184, 6.122]` | `TA-B-01`'s reference (carried) |
| `W1-NULL` | `[156, 152, 155, 152, 152]` (≡ `M-POL-2`, `TA-X-04`) | `[7.184, 4.408, 7.02, 7.184, 6.122]` | carried |
| `W1` | `[156, 152, 155, 152, 155]` | `[6.286, 4.408, 7.02, 7.184, 6.939]` | printed beside `TA-X-06` (carried) |
| ⚑ `M0` | `[155, 151, 156, 155, 155]` | `[7.347, 13.143, 7.347, 6.449, 5.143]` | ⚑ **newly measured. Information only: no row grades it, and it gates nothing** |
| ⚑ `M-POL-2-NULL` | `[155, 151, 156, 155, 155]` (≡ `M0`, `TA-X-03`'s relation) | `[7.347, 13.143, 7.347, 6.449, 5.143]` | ⚑ **information only** |

### B.2 – B.4 · `P-1`, `P-2`, `P-3` *(carried from v1.10 by reference; P-3: POOL-466 = 466, set digest reproduces)*

### B.5 · ⚑ `P-4` · PACK IDENTITY: both v3.7.1 packs and the cross-pin

```
model_pack_dir       : "kc2-model-pack-v3-E-s09-cp150-mech-v3p7p1-20261001_021247"
model_pack_digest    : 48a4c94c165715d3f4f5db89c1278aa8439fbe1507c39dd555f7ce91d4636c96   (PACK: pack law over 19 member rows)
reference_pack_dir   : "kc2-reference-pack-v3-E-s09-cp150-mech-v3p7p1-20261001_021247"
reference_pack_digest: 1887257f5370443a1729fde2ff446579b1acc501dcd03679244297b541e3e5b1   (PACK: pack law over 7 member rows)
cross_pin_verified   : reference.manifest.cross_pin.model_pack_digest == model_pack_digest
                       (48a4c94c165715d3f4f5db89c1278aa8439fbe1507c39dd555f7ce91d4636c96 — equal: true)
```

| # | `model/` member | label | sha256 (computed) | bytes | v3.7 → v3.7.1 |
|---|---|---|---|---:|---|
| 1 | `ai_states.json` | FILE | `928ded88e74e636422cbc107bdb02ff4cf27521dc74636e5e7e0e1680bd6060e` | 2,497 | identical |
| 2 | `arena.json` | FILE | `15078b583364bd1953d8d9480f95a1194a2b01ba8915d87fa9f83dde6e6d75be` | 426,450 | identical |
| 3 | `config_of_record.json` | FILE | `136f3a2072c0f99c8a03a61b1e2ac804d43af3396f588401f9284a5b47412d11` | 28,112 | identical |
| 4 | `controllers.json` | FILE | `b4217daac06f2f55acb3ec68571dd7766d31ac156ee01ee903b721f26042e478` | 5,384,891 | identical |
| 5 | `input_closure.json` | FILE | `13be3550f65ef9b57f14ddee26c43b94296862fe94d221847bdc02c8e22e1b4f` | 26,963,137 | ⚑ **MOVED** |
| 6 | `input_closure_v3p7p1.json` | FILE | `d1b759800a5709d09170a956c5dea759d80bf69e51a30781db7d16a78e49aadb` | 2,339,790 | ⚑ **ADDED** |
| 7 | `math_rules.json` | FILE | `3b1e2d014411cb314d5cbf42ea40773dbcfa3de242f13d3a1d31eb830643b62d` | 188,662 | identical |
| 8 | `meta.json` | FILE | `8fe51d80bd07328ef8ae98c8389f0808062f2059ea5b3139ad725a3c721c2e1b` | 138,408 | ⚑ **MOVED** |
| 9 | `monster_defense.json` | FILE | `00ffab1576577164cc132b498817d5480822df3234f3f3bcf286c0a407193aac` | 8,816,113 | identical |
| 10 | `monster_kinematics.json` | FILE | `b8b1c7b4e491aeb13981b26478c12190ec7efd892eddeeb6eef572f1766bc549` | 965,515 | identical |
| 11 | `monster_offense.json` | FILE | `fad592f5cb1d10030ca4ddd5788f65d3e01c0fc5781a75b73e50693d5f9ea76b` | 17,763,540 | identical |
| 12 | `monsters.json` | FILE | `3839322955b7d4af0a6c8c8b169656136a0271a7ab9bb68893a272df703701a0` | 15,211,150 | identical |
| 13 | `player_kit.json` | FILE | `2b68af939b6c795c1b4c9f0411aa037fb4d0332f983fa942aa307c85329eeac6` | 143,191 | identical |
| 14 | `projectiles.json` | FILE | `ed32ff8a648d2b3c24918cd20150f27856b371e2a45a0e699cc1c8b6c949a0e5` | 74,198 | identical |
| 15 | `provenance.json` | FILE | `1d06e08a1744c8df7e188725f2c2bc5cdbbdf4d1007e75dba01a33fc9f8a0710` | 651,204 | identical |
| 16 | `rng_contract.json` | FILE | `232ad93c6fc982bd5b564ab8f27f684696cd20326a4e3b9f12cc31db39d65fca` | 32,351 | identical |
| 17 | `summons.json` | FILE | `6a7cc5af2bd7291b46c1beafedf2e13b70990a3f9a1a194f2092c1a64e586a93` | 111,259 | identical |
| 18 | `target_selection.json` | FILE | `e1df3cf69d2f3f91cce5ab5f9a71de4b7be4fb2372d18de2cc99517d399d68ce` | 31,936 | identical |
| 19 | `waves.json` | FILE | `38c43a9c3b35560a3dce88ac16c189cb03b120b1ba2085ae2458040113621072` | 1,087,499 | identical |

**Reference pack (7), FILE each:** `acceptance.json` `f5ce2c174cccf9a253603ac8bfc3f20b872b2e2a92c8d24e461601e64f1f9853` (4,716 B) · `actors.json` `ef03536f97fe7122e14b34ae69a26bc7616fe58fcbe5989ab3aa09e7420ea04b` (1,956,876 B) · `meta.json` `25c2be7ef76fef64f8610401196bc3db724c84d62a726ecc8bb596816d0b7d72` (118,847 B; ⚑ MOVED) · `rng_tape.json` `607bf3bffd6a5a330d2ede97eebcd7139f3c218292954aa56fbf38c34e833ea0` (406 B) · `skill_interrupt_reference.json` `45522df26b1703ac2489d08e7e7fa6986255ca80e64f057279ca6b492fdf3707` (3,113 B) · `tracks.json` `bb3495218fcdeaab11d4d5e9a5d25a2e14f2fd21384bcebc7dd1f93b0b7d9bfd` (44,733 B) · `u7_heading_conditioning.json` `5ad6ab0f089d3409506f29293433849f6abcbd1bee2a2242344fe12367287c05` (3,601 B)

**The manifests themselves (FILE; not the pack digest, and not substitutable for it):** model `manifest.json`
`be5d256609d3caa231abcbe6fa042fedfa381035c3bea5c219ab5f54ca7717b9` · reference `manifest.json` `212b8652523048e1f8ac4697f13132388be22b8c6c4510180712832c5e560346`.

⚑ **`P-4` is red on any other pack.** v3.7 (`9bee0357…` / `978bb893…`) and earlier are **not the pack of record**. ⚑ **The
grader checks the runtime header first,** reading the `.app` / runtime header's `pack_digest` **by running the
binary**.

### B.5a · R-21's HEADER RE-PIN

```
R-21 (a) header model pack_digest     == 48a4c94c165715d3f4f5db89c1278aa8439fbe1507c39dd555f7ce91d4636c96   (P-4; read by RUNNING the binary)
R-21 (a) header reference pack_digest == 1887257f5370443a1729fde2ff446579b1acc501dcd03679244297b541e3e5b1   (P-4; read by RUNNING the binary)
R-21 (b) P-5: the SAME eleven settings as v1.8 … v1.10, unchanged in name, value and site; refuse-to-boot on any unset one
```

⚑ **The harness must also move** (the `H-4` class): the prereg it pins (now this file), `substrate_epoch`, ⚑ **each
arm configured from its `a8` rows, with that job's ROWSET digest (§ B.1a) printed on the emission**, and
`TA-X-26(b)`'s file hash (v1.10 § A.4). **The grader verifies these on the emission, not on a commit message.**

### B.6 · `P-5` · THE ORACLE FOLD SETTINGS: ELEVEN *(carried from v1.10 § B.6, unchanged)*

Same eleven settings, values, sources and line numbers; the oracle tree is byte-identical (§ A.2). Same loader
call: `load_profiles(dot_corrections=True, pet_special_gates=None, winner_surface=WinnerSurfaceFold.from_x8(P-n.2),
pool_lift=pool_lift.load(), c11a=C11aLoader(scope=AuraScope.CLASS))`. ⚑ **That call is now `a8` row
`IC7-A-0453`**, with its constructors `IC7-A-0435`, `IC7-A-0454` and `IC7-A-0446`. Where this file's prose and the row
disagreed, the row would govern; **they agree** (checked by script on `dot_corrections`, the C-11a scope and the
`x8` path).

---

## § C · THE LAWS

**C.1–C.6 and C.8: carried BY REFERENCE from v1.10 § C** (which carries v1.9 / v1.8 § C).

### C.7 · THE EPOCH LAW, EXTENDED TO v3.7.1

> ⚑ **A v3.3, v3.4.2, v3.6, v3.6.1, v3.7 and v3.7.1 PORT board are pairwise NOT draw-comparable at a fixed salt.
> No row, diagnostic or report line may compare across them.**

**Why v3.7 → v3.7.1 is declared non-comparable, although v3.7.1 is nearly additive:** pass 3b re-points the
loader (arms from `a8`, the four withdrawn rows dropped, the control-gate seed on the wire, the `r9` defaults
explicit). Whether any of that moves the port's stream is a property of the runtime, not of the pack, and this
file does not predict it. ⚑ **The ORACLE is the same object at every one of these epochs** (§ A.2).
**`substrate_epoch = "v3.7.1 / model 48a4c94c… / reference 1887257f…"`** for everything graded under this document.

---

## § E · OUTSIDE T-A'S REACH

**E.1 (the traps, 1–12) and E.2 (declared ceilings, `C-o` included, and its boundary at `TA-X-18`): carried from
v1.10 as written.** ⚑ **One addition to trap 12's family, stated so it is not mistaken for a pass:** a conservation
identity whose residual is small has shown that its accumulation error was small *on that run*. It has not shown
that the tolerance was sized for the accumulation. § F.2k is the second statement, and only the second is what
clause (c) exists for.

---

## § F · THE GRADED ROWS

**§ F.1, § F.2a–§ F.2j are carried BY REFERENCE from v1.10 / v1.9 / v1.8** (pinned above), unchanged in assertion,
class, tolerance and expected value. The notes of § 0.2 / § A.3 / § A.4 and the arms of § B.1a apply to them.

### F.2 · EXACT rows: 28, plus `TA-X-06` UNGRADEABLE-declared (closed)

| id | statistic | basis | tolerance | arm(s) (§ B.1a, `a8`) | v1.11 |
|---|---|---|---|---|---|
| `TA-X-01` | port self-determinism; arm+salt NAMED, ≠ `P-2`'s | run-internal | byte-exact | one named | CARRIED |
| `TA-X-02` | coverage 89/89, zero unmapped | census | integer | — | CARRIED |
| `TA-X-03` | `port(M-POL-2-NULL, s) ≡ port(M0, s)`, all 5 | `[M-POL2]` | byte-exact | M-POL-2-NULL, M0 | CARRIED IN FORM |
| `TA-X-04` | `port(W1-NULL, s) ≡ port(M-POL-2, s)`, all 5 | `[W1W]` | byte-exact | W1-NULL, M-POL-2 | CARRIED IN FORM |
| `TA-X-05` | `port(M-POL-2, s) ≢ port(M0, s)`, ≥ 1 salt | `[M-POL2]` | exact, one-sided | M-POL-2, M0 | CARRIED IN FORM |
| `TA-X-06` | `port(W1, s) ≢ port(M-POL-2, s)` | `[W1W]` | **EMITTED AND PRINTED, NOT GRADED** | W1, M-POL-2 | **UNGRADEABLE-declared, closed at exactly `["TA-X-06"]`** |
| `TA-X-07` | `offered = applied + dropped + voided + pool_truncated + pcl_reclaim + counterplay_absorbed` | run-internal | relative ≤ 1e-12; **4,500-term depth budget (clause (c)), DERIVED in § F.2k, STANDS** | all 25 | CARRIED VERBATIM |
| `TA-X-08` | denominator identity, both sub-identities | `[M-POL2]` 5/5 | exact | all 25 | CARRIED |
| `TA-X-09` | all **9** `math_rules.test_vectors` of the five normative rules | `P-4`'s `math_rules.json` (FILE `3b1e2d014411cb314d5cbf42ea40773dbcfa3de242f13d3a1d31eb830643b62d`) | per-vector | — | CARRIED |
| `TA-X-10` | `max_body_radius_m ≤ 43.758085029822276` (W1), roster movers | `[W1W]` · `arena.json` | exact, ≤ | W1 | CARRIED (`H-9` PASS) |
| `TA-X-11` | `n_wall_clamps_{player,body} == 0`, every W1 arm | `[W1W]` | integer | W1, W1-NULL | CARRIED (`H-9` PASS) |
| `TA-X-12` | pool inertness under ORACLE: total pool damage `== 0.0` | `[W1W]` · `DIV-19` | exact | all 25 | CARRIED |
| `TA-X-13` | no player crit | `V0 · CritLimb LO` | integer | all 25 | CARRIED |
| `TA-X-14` | the two DO-NOTs; a REFUSED cast is not a release | `math_rules` prohibitions | integer | all 25 | CARRIED |
| `TA-X-15` | (a) p01–p04 at `t = 0.0`, p05 one burst at `t = 4.000 s` (tick 49); (b) no intra-point stagger | census `M4` / `V11` | exact | all 25 / — | CARRIED |
| `TA-X-16` | p06 OFF: `n_pool_picks == 47`, `n_spawn_point_6_keys_rolled == 0`, a filtered-keys counter | `waves.json` | integer | all 25 | CARRIED |
| `TA-X-17` | `‖spawn_xy − anchor_xy‖ ≤ 8.0` m, every roster placement | `placement_extents_m` | exact, ≤ | all 25 | CARRIED |
| `TA-X-18` | `u₁ = u₂ = 0.5` → **`(-3.999999999999985, -3.49691120014899e-07)`** | the oracle's `SpawnStructureFold.offset` · V9-SITE-14 | exact: float64 equality per component at `repr` precision | — | CARRIED (v1.10 § A.5) |
| `TA-X-19` | arrival unconditionality; no damage predicate reads an arrival's `px, py` | `deferred_arrival.py:13-17` | integer | all 25 | CARRIED |
| `TA-X-20` | 2.99 m hit / 3.01 m miss; no angular gate; no target cap | census `D7` | exact | — | CARRIED |
| `TA-X-21` | quantisation rule per site + zero bare `round(` on the port's threat path | four modules | exact | — | CARRIED; re-verify the live site list at emission |
| `TA-X-22` | `cause == "interrupts_channel_flag"` is 0 under ORACLE | `V0`; V18+V19 | integer | all 25 | CARRIED |
| ~~`TA-X-23`~~ | ~~board-roll composition~~ | struck at v1.2, retired | — | — | — |
| `TA-X-24` | attack phase is `ENGAGE`; `sha256(actor_id) mod n` never evaluated | `V0` | exact | all 25 | CARRIED; NOTE `r9` |
| `TA-X-25` | the spawn partition, four clauses (v1.8 § F.2f) | P-l.q91 + `u5` + the oracle's profile predicate | integer identity | per arm per salt | CARRIED |
| `TA-X-26` | declared-join conformance, five clauses (v1.8 § F.2a) | `P-i` | integer / exact / declared-precision | — | CARRIED; (b): hash the loaded file |
| `TA-X-27` | degenerate-draw consumption, four clauses (v1.8 § F.2b) | `P-4` | integer / byte-exact | (c) all 25 | CARRIED; NOTE `CONTROL_GATE_RNG_SALT` (§ A.4) |
| `TA-X-28` | leech target law, three clauses | § F.2g | integer / structural | all 25 | CARRIED; NOTE `r9` |
| `TA-X-29` | global-magnitude fold conformance, five clauses; (e) `3.207764` / `4.980316` + 39 per-record ratios | § F.2h | integer / declared-precision | (e) `WALK` | CARRIED |
| `TA-X-30` | the pursuit halt, two clauses | § F.2i | exact / integer | all 25 | CARRIED |

### ⚑ F.2k · R-11: THE 4,500-TERM BUDGET, DERIVED AT THE MEASURED DEPTH. **IT STANDS. THE ATTEMPT DOES NOT FIRE.**

> ⚑ **jack-ryan: this section is the one to attack first** (H-7). It concludes against firing. The two ways it
> could be wrong are (i) a mis-read of the port's summation, which § F.2k.2 cites line by line so it can be
> checked, and (ii) an error in the bound, which § F.2k.3 states in its standard form with its source.

#### F.2k.1 · Where the budget came from

The budget was derived **once, in v1.5 § F.2d, clause (c)** (pinned above), and carried verbatim by v1.6 § F.2d,
v1.7 § F.2d, v1.8 § F.2d (which added R-11's law for both outcomes, at KP-125 item 1's request), v1.9 and v1.10.
The derivation, in full:

> *"`1e-12 ≈ 4.5e3 × float64 eps (2.220446e-16)` — an accumulation-depth budget of ~4,500 terms. The runtime EMITS
> the realised number of terms summed into `offered`. If the realised depth EXCEEDS 4,500, the row is
> `UNGRADEABLE`, not green."*

So the budget is `n_max = 1e-12 / eps = 4503.5996` with `eps = 2⁻⁵² = 2.220446049250313e-16`: the linear worst-case growth of
rounding error in a running sum, `n · eps`. v1.5 named no summation method and no accumulator other than
`offered`.

#### F.2k.2 · The summation the port actually uses (read from drax's code, `reincarnated-godot` `ffb454e`)

Read from `kc2_runtime/sim/kc2rt_fight.gd` (FILE `e6903095b6bba83f38359a654380cb5b13516c8e2a437b2a04ae1ff73c72a680`) and `kc2_runtime/sim/kc2rt_laws.gd` (FILE
`406ffeca427bf90bb6b998eba834138eb7f68b76917f95e70fabf72ba523e1b3`); HEAD blob equal to the working tree; nothing was run or modified:

* **(M1) Seven independent running accumulators, plain recursive summation.** Every quantity in the identity is a
  value in the dictionary `conservation`, updated in program order by `conservation[k] = float(conservation.get(k,
  0.0)) + x`. GDScript `float` is IEEE-754 binary64. **There is no compensation (Kahan / Neumaier), no pairwise or
  blocked summation and no sorting.**
* **(M2) `n_terms_accumulated` counts additions into `offered` only.** `_offer(x)` (`kc2rt_fight.gd:6334-6336`) is the
  only writer of `conservation["offered"]` after the reset (`:5636`), and it increments `n_terms_offered`;
  `conservation_report()` (`:6339-6345`) emits that count as `n_terms_accumulated`.
* **(M3) Five `_offer` sites:** player → monster per resolution (`:2707`); the secondary streams, once per tick
  (`:3359`); a routed non-health family (`:5152`); a monster row (`:5268`); the PCL component, once per attack (`:5378`).
* **(M4) Two `_offer` arguments are themselves running sums, uncounted.** The secondary-stream term is a local sum
  over that tick's Soulfire body-hits and bleed ticks (`:3306-3354`, when `streams_on`); the PCL term `pcl_raw_hp` is
  a sum over the attack's PCL rows (`:5249`).
* **(M5) The six sinks are accumulated separately and are not counted.** Every `_offer` call is accompanied by at
  least one addition to `applied`, `voided` or `dropped`: `:2707` adds to `applied`, `voided` and
  `pool_truncated`; each stream sub-hit adds to `applied` (or `dropped`) through `_ss_hit`, and each Soulfire sub-hit
  also to `voided`; `:5152` adds to `dropped`; `:5268` is followed by `dropped` (leech, non-health, resist-absent), by
  `voided` (direct rows), or by `_dot_register`, which books `voided` or `dropped` (`:4400-4416`); `:5378` adds to
  `voided` and `pcl_reclaim`. **Hence `m_applied + m_voided + m_dropped ≥ m_offered`.**
* **(M6) The residual.** `conservation_residual` (`kc2rt_laws.gd:479-518`) sums the six sinks left to right (5
  additions), forms `residual = offered − total`, and grades `|residual| / max(1, |offered|) ≤ 1e-12`.
* **(M7) The accumulators feed no decision.** `conservation` is read only by `conservation_report()` and by two
  emission fields (`:5805`, `:5807`). *Stated because remedy (a) below depends on it; a port change must show it,
  not cite this line.*

#### F.2k.3 · The bound

**Standard result** (Higham, *Accuracy and Stability of Numerical Algorithms*, 2nd ed., SIAM 2002, § 4.2, eqs.
(4.4) and (4.6)): recursive summation of `m` terms in floating point with round-to-nearest gives

  `|Ŝ − S| ≤ γ_{m−1} · Σ|xᵢ|`,  `γ_k = k·u / (1 − k·u)`,  `u = 2⁻⁵³ = 1.1102230246251565e-16` (the unit roundoff; `eps = 2u`).

**Applied to the port.** Let `O` be the exact sum of the offered terms and `Sⱼ` the exact sum of sink `j`'s terms.
Where every term of an accumulator is non-negative, `Σ|xᵢ|` is its sum (`O` or `Sⱼ`). A term that can go negative
(e.g. `voided` at `:2714`, if a banner or vector factor lifts `applied` above the raw offer) only enlarges `Σ|xᵢ|`,
so the bound below is then a LOWER envelope of the true one. Then, with `ΣⱼSⱼ ≈ O` because the identity balances, the computed relative residual obeys

  `|r̂| / O ≤ γ_{m_o−1}` *(offered)*  `+ Σⱼ γ_{mⱼ−1}·Sⱼ/O` *(the six sinks)*  `+ γ₅` *(the final six-way sum)*
  `+ c·u` *(forming each sink piece as a difference)*  `+ W_inner` *(the uncounted sums of (M4))*.

To first order, `|r̂|/O ≲ u · (m_o − 1 + W + 5 + c + …)`, where `W = Σⱼ (mⱼ − 1)·Sⱼ/O`. **The tolerance holds in
the worst case iff that is `≤ 1e-12`, i.e. iff `m_o + W + c + 4 ≤ 1e-12/u = 9007.1993`.**

**v1.5's budget is this condition read with `eps` (= `2u`) in place of `u`:** `n · 2u ≤ 1e-12` is the same as
`m_o + m_s ≤ 9,007` with the sink side as deep as the offered side, `m_s = m_o = n`. **So 4,500 is the derived
value under the reading "the sinks are no deeper than `offered`", with `c` and `W_inner` ignored.** It is not a
looser or tighter number than the method warrants on that reading. It is that number.

#### F.2k.4 · Evaluated at the measured depth

`m_o` is measured (KP-152, the port's own generator, salt 1, the run that reaches w160): **6,616 on `M-POL-2`, 6,539 on
`W1`.** Nothing else in the bound is measured, because the runtime does not emit `mⱼ`, `Sⱼ` per sink, or the inner
counts of (M4).

| quantity | `M-POL-2` (6,616) | `W1` (6,539) | read |
|---|---|---|---|
| v1.5's form, `n · eps` | 1.4690e-12 | 1.4519e-12 | **over 1e-12** (the budget's own arithmetic) |
| offered side alone, `γ_{m_o−1}` | 7.3441e-13 | 7.2586e-13 | — |
| ⚑ **best case**: offered + final sum + one split rounding, **every sink exact** (impossible: (M5)) | 7.3508e-13 (margin ×1.360) | 7.2653e-13 (margin ×1.376) | the floor; no runtime reaches it |
| the sufficient condition on the sinks, `max mⱼ ≤ …` (offered + final sum + split + the deepest sink as if it carried all of `O`) | **`max mⱼ ≤ 2,387`** | **`max mⱼ ≤ 2,464`** | not measured |
| what (M5) forces: `max(m_applied, m_voided, m_dropped) ≥ ⌈m_o/3⌉` | ≥ 2,206 | ≥ 2,180 | from the code |
| the sinks as deep as `offered` (v1.5's implicit reading) | 1.4695e-12 | 1.4524e-12 | **over 1e-12** |

**What this establishes.**
1. **The bound cannot be shown to hold at n = 6,616, and it does not hold with margin under any reading.** Even
   the impossible best case, with every sink summed exactly, leaves a margin of ×1.360. The sink side, which
   (M5) proves is non-empty and which the runtime does not count, can only add to it.
2. **The sufficient condition is a narrow window that nothing measures.** The worst-case bound fits under 1e-12 only
   if the weighted sink depth `W` stays under about 2,386 terms. With the unweighted form, that means
   `max mⱼ ≤ 2,387`, while (M5) already forces the deepest of three sinks to `≥ 2,206`. The weighted form needs
   `Sⱼ` and `mⱼ` per sink, and neither is emitted. ⚑ **(M4) points the wrong way for that window:** with
   `streams_on`, every stream tick that offers one term books one `applied` (or `dropped`) per body hit in that
   tick. *That is an expectation from the code's shape, not a measured count, and nothing here depends on it.*
3. **So, by clause (c) as written and as derived, 4,500 stands.** A cell whose `n_terms_accumulated` exceeds 4,500
   is `UNGRADEABLE` (v1.8 § F.2d), and § G makes the verdict `INDETERMINATE`.

#### F.2k.5 · ⚑ Consequence: v1.11 attempt 1 CANNOT FIRE on the pass-3 runtime as measured

The port is deterministic per (arm, salt) (`TA-X-01`), so the measurement **is** the graded cell's value.
`M-POL-2 × salt 1` and `W1 × salt 1` are graded cells of `TA-X-07` (all 25, § B.1a). On this runtime a graded run
would be `INDETERMINATE` by construction. **By v1.8 § F.2d cases 2 and 3, it must not fire.** That consumes
nothing and buys nothing, and the decision is not the grader's to make after the fact. **H-6 is therefore owed on
the graded pass-3b runtime as `n_terms_accumulated` for all 25 cells, `≤ 4,500` on every one** (clause (c)'s own
antecedent, evaluated before firing because the run is deterministic). `M0`, `M-POL-2-NULL` and `W1-NULL` have not been
measured at all.

> ⚑ **What is NOT a derivation, named so none is mistaken for one:**
> * *the observed residual* (`≈ 1e-14`): v1.8 § F.2d already rules that *"the residual is not the criterion, so it
>   cannot rescue the row"*;
> * *re-reading v1.5 with `u` in place of `eps` for `offered` alone* (`n ≤ 9007.1993`): this ignores six accumulators that
>   (M1) and (M5) show exist. It would pass 6,616 only by leaving out what the code does;
> * *a probabilistic `√n` estimate* (`√6616 · u ≈ 9.03e-15`): a statistical model of typical error, not a worst-case
>   bound. Adopting it after seeing the measurement re-keys the clause toward the data. That is the move Law 3
>   and v1.8 § F.2d forbid.

#### F.2k.6 · Honest remedies, for the conductor. **None is adopted here.**

| # | remedy | what it changes | what it costs / its route |
|---|---|---|---|
| (a) | ⚑ **compensated summation** (Neumaier / Kahan–Babuška) on all seven accumulators and the six-way final sum, in the port | per-accumulator bound `(2u + O(m·u²))·Σ|xᵢ|` (Higham § 4.3, eq. (4.8)): ≈ 2.2204e-16 relative, **independent of `m` to first order**. The tolerance then holds at any realistic depth | a port change (drax), so a new runtime digest, G3 re-run, and (M7) shown, not cited. ⚑ **Clause (c)'s 4,500 is a recursive-summation figure**, so moving to it needs a **new dated prereg** that re-derives (c) for the new method, and by v1.8 § F.2d case 2 **the re-sizing question goes to Matt** |
| (b) | **emit the true depth**: `mⱼ` and `Sⱼ` per sink and the inner counts of (M4), and re-key clause (c) to the derived inequality of § F.2k.3 | makes the bound **computable** per cell | a re-keying of (c): new prereg + Matt. **It may still fail:** the window of § F.2k.4 is narrow |
| (c) | **shorten what is summed**: grade the identity per wave (ten identities, each roughly a tenth of the depth) | each per-wave depth falls far below any budget | **changes the row's statistic**: new prereg + Matt (KP-137, *"no goalpost change"*, must be argued) |
| (d) | **R-11's own route**: the question goes to Matt as it stands (v1.8 § F.2d case 2) | — | — |

⚑ **The routing tension, recorded and not resolved:** KP-152 allows v1.11 to restate the budget, with derivation, if
the bound holds, and has jack-ryan's pre-read rule on it. v1.8 § F.2d case 2 says any re-sizing of clause (c) goes
to Matt. The bound does not hold, so v1.11 restates nothing and the tension is moot here. **It is live for remedies
(a)–(c),** and the conductor should rule which route governs before choosing one.

#### F.2k.7 · ⚑ A gap in clause (c) itself, for the pre-read (OQ-17)

The derivation shows that **clause (c)'s antecedent (`n_terms` into `offered` ≤ 4,500) is not, by itself, sufficient
for the bound it was written to make checkable.** The bound also needs the sinks to be no deeper than `offered`,
which no runtime has ever emitted. This was true at v1.5 as well, and it applies to every depth ever measured
(R-11's 1,226 at v1.8 included). **It moves no verdict:** attempt 1's residual (1.563e-14) was 64× inside 1e-12, and
clause (c) only ever made a row UNGRADEABLE, never green. **Not repaired here.** Repairing it is a re-keying of (c),
and the route is remedy (b)'s. **v1.11 grades clause (c) exactly as written.**

### F.3 · DIAGNOSTIC rows: 19 ids, 0 gating, every width VOID *(carried from v1.10 § F.3)*

⚑ **CLASS V · `TA-B-01`, reference sentence (mandatory, verbatim at v1.11; version label only):** ***"`BAND /
NON-DECISIVE / REPORT-ONLY`. A terminal wave inside or outside this band is not evidence of fidelity either way. It
is read from the port's `M-POL-2` arm. The oracle's sealed `M-POL-2` arm terminates at `[156, 152, 151, 151, 156]`,
`player_death` on every salt. The v1.11 oracle's `M-POL-2` arm (the same object as v1.8's, v1.9's and v1.10's:
the 338 armed, the winner surface armed, the C-11a corrections folded) terminates at `[156, 152, 155, 152, 152]`,
`player_death` on every salt, and no salt reaches wave 160. A port that clears to wave 160 has not survived a hard
board; it has failed to be in one."*** Printed beside `TA-X-06`, never as `TA-B-01`, gating nothing: the port's `W1`
terminals next to the oracle `W1` arm's `[156, 152, 155, 152, 155]`. `TA-B-13`'s, `TA-B-14`'s and `TA-B-15`'s
sentences are carried verbatim.

### ⚑ F.3a · DIAGNOSTIC NOTE, NOT GRADED: salt 1 clears to w160 on the port's own generator

**The observation (KP-152, printed by drax's side-by-side tool):** on the port's OWN generator, `M-POL-2` terminal
waves are `[153, 160, 154, 154, 153]`; the oracle's are `[156, 152, 155, 152, 152]`. Salt 1 clears to w160. § F.3's
sentence calls that outcome *"failed to be in [a hard board]"*.

**Why the per-salt comparison carries no information:** the port's generator and the oracle's draws are different
random realisations of the same board (KP-152 corrigendum). Salt `k` on one side and salt `k` on the other are not
the same fight. **Only the distributions are comparable, and each has five draws.**

**What n = 5 can say:**
* **The board is not trivially soft on the port's generator.** 4 of 5 salts die inside w153–w154, inside the
  oracle's range of w152–w156.
* **G3 on the oracle's draws is exact** (0 decision divergences, death wave and tick equal on all five salts, both
  arms). **So if the clear has a cause other than chance, it lies where G3 does not look: in the port's
  generator** (its streams, its consumption, its board seeding), **not in the fight logic G3 compared.**

**What n = 5 cannot say:**
* **Whether the port's clear rate differs from the oracle's.** Port 1/5 against oracle 0/5: Fisher's exact test,
  two-sided, `p = 1.0`. The oracle's 0/5 leaves its clear rate anywhere up to 45.1 % (one-sided 95 %), or 52.2 %
  (two-sided Clopper–Pearson). The port's 1/5 has a 95 % interval of 0.5 %–71.6 %. **The two are indistinguishable
  at this n.**
* **Whether the terminal waves differ in location.** An exact permutation test on the ten values (Mann–Whitney
  U = 17 of 25) gives `p = 0.41`, two-sided. Means are 154.8 against 153.4, and the w160 value is censored (the scope
  ends there).
* **"Realisation variance" against "a generator defect that raises the clear rate".** n = 5 cannot tell these
  apart in either direction. What could: (i) the generator rows, `P-2` and `TA-X-27(c)` (consumption equals the
  oracle's), which grade the generator's law rather than its outcomes; (ii) a larger-n comparison of the two
  generators' terminal-wave distributions on the same board, which would be ungraded and diagnostic. With these
  rates, n in the tens per side is the scale at which a clear-rate difference of a few tens of percent becomes
  visible.

**Nothing here is graded, and nothing gates.** It is printed so that Gate-2 looks before attempt 1, as KP-152 asks.

### F.4 · Emitted, not graded: **three** *(carried)*

### F.5 · Report-face rules: twelve

**Cl. 1–6, 8, 9, 10 and 12 carried verbatim.** Changed:

7. **THE SUSTAIN SENTENCE (mandatory; version label only):** ***"`leech` and `intake` still have no oracle side in
   the seals (`C-e`). Off-seal, the v1.11 oracle (the same object as v1.8's, v1.9's and v1.10's; the C-11a
   corrections folded) KILLS THE PLAYER AT WAVES 152–156 on salts 0–4, and lands ×3.17 the referent's intake over
   waves 151–159 on the landed grain. The port's own figure is printed from this run and not asserted here. A
   GREEN T-A IS COMPATIBLE WITH ANY RELATION BETWEEN EITHER REPLICA AND THE REFERENT."***
11. **THE PORT≠ORACLE HOLES (mandatory on any report, including a passing one; EXTENDED):** ***"Port≠oracle holes
    1–17 (PCL dropped · death after heal · damage rows unreachable · `tree_attack` slots never chosen · dying slots
    mishandled, and 5b one dying slot per death · slot chance/cooldown/delay never read · the wrong march base ·
    to-hit · mitigation order · DoT timeline · monster crit tier · motion order and the contact fold · Soulfire and
    the bleed rider · monster pets · the resist cap · attack speed and OA adds · the HI life block), the
    chance-gate boundary, the C-11a grant law, the loop-layer defects of KP-144, the pack-closure defect of KP-147,
    and the closure-law defects of KP-150 / KP-152 (run state carried as input · arms defined only in prose ·
    read-absent columns · constants on untaken branches) are invisible to every EXACT row in this instrument. A
    v1.11 PASS is not quotable without jack-ryan's hole-closure finding at the same runtime digest, and the seal is
    blocked on any non-zero R-6 invariant."*** Followed by the three R-6 invariants, printed with their values.

---

## § G · FAIL TAXONOMY, THE HOLE-CLOSURE RULE, AND THE GRADED-RUN CAP

| verdict | antecedent | consequence |
|---|---|---|
| **`STRUCTURAL`** | ≥ 1 of the 28 EXACT rows RED | the port is wrong; **consumes one of v1.11's two attempts**; L2 applies |
| **`INDETERMINATE`** | 0 EXACT red, ≥ 1 of the 28 UNGRADEABLE (incl. `P-1`…`P-5` red, and `TA-X-07(c)` above its depth budget) | does NOT consume an attempt; nothing seals |
| ~~`STATISTICAL`~~ | retired at v1.5 under F5 | — |
| **`PASS`** | all 28 EXACT green, none UNGRADEABLE | ⚑ **`PASS @ coverage k/89, 28/28 EXACT rows green, TA-X-06 UNGRADEABLE-declared (Q83(b)), dilution ⟨d⟩×, substrate_epoch v3.7.1/48a4c94c…, prereg v1.11`**. Never unqualified, and never quotable alone (§ G.2) |

**Order:** `STRUCTURAL → INDETERMINATE → PASS`; stop at the first hit. No diagnostic appears in any antecedent. **No
post-hoc widening, by anyone.** `declared_ungradeable` must be **exactly** `["TA-X-06"]`; anything else is **C1**.
⚑ **A row graded on an arm other than § B.1a's, or on an arm not configured from its `a8` rows, is non-conforming
(C1), not red and not green.**

### G.1 · THE GRADED-RUN CAP: **`0` OF `2` UNDER v1.11**

**The allowance is carried unspent** (Matt KP-115; KP-137; no graded run exists under v1.8, v1.9 or v1.10). **Q85's
four guards hold:** (1) the allowance was ruled from outside the run (Matt); (2) this prereg is committed ALONE,
every pin recomputed, before anything is graded against v3.7.1 (D4); (3) v1.7's attempt 1 stays on the record,
spent; (4) `substrate_epoch` is declared on every artifact. **Naming:** the next graded run is **v1.11 attempt 1
(overall attempt 2)**.

⚑ **L2, AS IT APPLIES TO v1.11.** v1.11 attempt 1 fires only after ALL of the following:
- drax's **pass 3b**: the pass-3 runtime (accepted, KP-152) re-pointed to v3.7.1 (arms from `a8`, the four
  withdrawn rows dropped, the control-gate seed on the wire, the `r9` defaults); ⚑ **its acceptance as the conductor
  restated it in KP-152:** G3 on the ORACLE's draws with ZERO injections, 0 decision divergences on every arm and
  salt, death wave and tick equal to the oracle's. *(v1.10's L2 bullet asked for a native per-salt death-wave match.
  The conductor's KP-152 corrigendum rules that unattainable by construction. **v1.11 carries the corrigendum and
  names it: it changes an attempt precondition, not a graded row** (Discipline #12).)*
- jack-ryan's **repair Gate-2 (R-1…R-22 + G3)** PASSes that runtime, on the digest it names (R-7);
- **this file's pre-read** has been filed (`H-7`);
- ⚑ **R-11 (`H-6`): `n_terms_accumulated ≤ 4,500` on EVERY one of the 25 cells of that runtime** (§ F.2k.5). **On the
  pass-3 runtime as measured this is false, so attempt 1 cannot fire there.** A remedy (§ F.2k.6) that re-keys
  clause (c) needs a new dated prereg, committed ALONE;
- `H-9`: discharged (PASS); `H-10`: discharged (KP-153). Nothing further owed on either.

v1.11 attempt 2 fires only after a v1.11-attempt-1 `STRUCTURAL` red is repaired and jack-ryan's Gate-2 PASSes the
repair. An `INDETERMINATE` consumes nothing and buys nothing.

### G.2 · THE HOLE-CLOSURE RULE: SEAL-BLOCKING, NOT VERDICT-BLOCKING *(the rule carried; the table extended)*

**v1.10 § G.2's table is carried row for row.** Changed and added:

| hole | what | ledger / commit | closure |
|---|---|---|---|
| — | the pack-closure defect of KP-147 | KP-147 / KP-148 / KP-152 | pass 3 **accepted** (KP-152, godot `42bf931` … `ffb454e`); pass 3b re-points to v3.7.1; repair Gate-2 |
| ⚑ — | ⚑ **the closure-law defects**: run state carried as input (`IC7-K-0036/37/38/0255`) · arms and the walk defined only in prose · read-absent columns · constants on untaken branches (`CONTROL_GATE_RNG_SALT`) · the `PX-LO` driver literal · `NORMAL_PTH_DIVISOR` unmapped | KP-150 / KP-151 / KP-152 / KP-153 (engine `67b18f90` · `27659b01` · `22cd2288`) | **fixed in the pack (v3.7.1; strict closure 0 on 14 captures and the static sweep 0).** Port side: pass 3b + G3 + repair Gate-2 |
| *(all)* | — | — | R-1 · R-2 · R-4 · R-7 · R-8 · R-19 · R-20 · **R-21 (re-pinned, § B.5a)** · R-22 (disposed, KP-144) |

**R-6, the three invariants, printed on the report face and never in an antecedent:** (i) cells with `killer_id` set
and `terminal_reason == cleared` = **0** · (ii) in-tick resurrections = **0** · (iii) `PercentCurrentLife` intake
**> 0** wherever a PCL row fired. **R-9, carried as law:** a v1.11 `PASS` is quotable only with jack-ryan's
hole-closure finding GREEN at the SAME runtime digest; any non-zero R-6 invariant blocks the seal; **Q87's seal at
v1.11** = `PASS` (28/28) AND coverage 89/89 AND T-B reported DIAGNOSTIC AND the hole-closure finding GREEN at the
graded digest AND **Matt's T-C yes on that same digest** (KP-114).

### G.3 · Verdict file `kc2play.ta_verdict.v1` (v1.11): **the fields that change from v1.10 § G.3**

```
prereg_version                    : "v1.11"
prereg_sha256                     : <this file, derived at emission>
substrate_epoch                   : "v3.7.1 / model 48a4c94c… / reference 1887257f…"
model_pack                        : {dir: "kc2-model-pack-v3-E-s09-cp150-mech-v3p7p1-20261001_021247", digest: 48a4c94c…, files_verified: 19}
reference_pack                    : {dir: "kc2-reference-pack-v3-E-s09-cp150-mech-v3p7p1-20261001_021247", digest: 1887257f…, files_verified: 7}
cross_pin_verified                : true
runtime_header                    : {"model_pack_digest": <read by RUNNING the binary>, "reference_pack_digest": <same>,
                                     "must_equal": "P-4 (§ B.5)", "read_by_running": true}      R-21 (§ B.5a)
preconditions.P4_pack             : {"model":<dir>,"reference":<dir>,"files_verified":26,"mismatches":0,"cross_pin":true}
arm_of_record                     : {<row id>: [<arms>], …}   § B.1a verbatim; TA-B-01: ["M-POL-2"]
arm_config_a8                     : {<arm>: {"a8_rows": "<first>…<last>", "rowset": <§ B.1a digest>, "configured_from_a8": true}, …}
oracle_containment_H9             : carried from v1.10 § G.3 (outcome 1)
closure_H10                       : {"outcome": "discharged", "authority": "KP-153", "evidence": "a0ad8246ac49628f8bd729c8cc2fba564b6456c4c06df0ae300e0439bfc447c9"}
r11_budget                        : {"budget_terms": 4500, "derivation": "§ F.2k", "outcome": "STANDS",
                                     "n_terms_accumulated_per_cell": {<arm>|<salt>: <n>, … all 25},
                                     "max": <n>, "over_budget_cells": [ … ]}     report face; clause (c) is the antecedent
ta_x_18_expected                  : "(-3.999999999999985, -3.49691120014899e-07)"
port_holes_printed                : true    (§ F.5 cl. 11, extended)
```

**Every other field is v1.10 § G.3 unchanged**, including `set_digests` (the four digests reproduce), `P5_folds`
(eleven), `declared_ungradeable` (**exactly** `TA-X-06`), `gmag_conformance` (`3.207764` / `4.980316`), `nodata` and
`hole_closure`. **T-B quoting cap: C1 / C2 / C3 unchanged.**

---

## § H · OWED BEFORE v1.11 ATTEMPT 1 (blocking)

| # | owed | owner | why it blocks |
|---|---|---|---|
| **H-1** | ⚑ **pass 3b**: the pass-3 runtime re-pointed to v3.7.1, every arm configured from its `a8` rows; G3 on the oracle's draws, ZERO injections, 0 decision divergences on all five arms × five salts, death wave and tick equal. ⚑ The port draws nothing from the control-gate stream on a graded arm (§ A.4), and runs the `r9` columns on `None` | **drax** | the pass-3 acceptance was on v3.7 |
| **H-2** | `spawn_by_record` per arm per salt, over roster bodies only | drax | `TA-X-25(c)` is UNGRADEABLE without it |
| **H-3** | `TA-X-29(e)`'s probe values: `3.207764` / `4.980316` + the 39 per-record values, on the `WALK` configuration (`IC7-A-0379`…`0432`) | drax | R-1 |
| **H-4** | ⚑ **the harness re-pointed to THIS file**: label from the pinned prereg; `substrate_epoch` = v3.7.1; ⚑ every arm configured from its `a8` rows, printing each job's ROWSET digest (§ B.1a); the § B.1a arm table as its per-row configuration; `TA-X-26(b)` by hashing the loaded CSV; the V0 diff reading V0-37 = GATE_FIRST; `TA-X-18`'s expected value; ⚑ `r11_budget` with all 25 per-cell counts | drax | a v1.10-pinned harness mislabels a v1.11 run |
| **H-5** | the hole-closure finding at the graded digest (§ G.2) | **jack-ryan** | `PASS` is not quotable without it |
| ⚑ **H-6** | ⚑ **R-11 on the graded pass-3b runtime: `n_terms_accumulated` on all 25 cells, each `≤ 4,500`** (§ F.2k.5). ⚑ **On the pass-3 runtime as measured (6,616 / 6,539 at salt 1), NOT dischargeable.** Discharge needs either a runtime whose every cell is within budget, or a remedy chosen by the conductor (§ F.2k.6) and a new prereg that re-derives clause (c) | drax (measure) · **conductor** (remedy choice) · Matt (any re-sizing, v1.8 § F.2d case 2) | clause (c): above 4,500 in any cell the row is UNGRADEABLE and the attempt is `INDETERMINATE` by construction |
| **H-7** | **this file's pre-read** | **jack-ryan** | D4 / the series' practice. ⚑ **Attack § F.2k first**, then § B.1a's `a8` citations, then v1.10's § A.5 (`TA-X-18`), which has no pre-read yet |
| **H-8** | Matt's T-C re-confirm on the graded digest | Matt | a seal condition, not an attempt precondition |
| ~~H-9~~ | ~~the oracle's `W1` containment~~ | gamora | **DISCHARGED: PASS** (KP-146) |
| ~~H-10~~ | ~~the closure proof on `M0`, `M-POL-2-NULL`, `W1-NULL` and the walk~~ | star-lord | ⚑ **DISCHARGED** (KP-153: strict closure 0 on all 14 captures + the static sweep 0; receipt FILE `a0ad8246ac49628f8bd729c8cc2fba564b6456c4c06df0ae300e0439bfc447c9`) |

**Not blocking, named so they are not lost:** v1.10 § H's list, carried · `C-o` · OQ-14 · OQ-15 · OQ-16 · OQ-17 · the
F.3a generator question (Gate-2) · the KP-139/KP-143 hole-number swap (the committed record governs: 15 = resist
cap, 16 = attack speed + OA adds).

---

## § I · OPEN QUESTIONS: one lean each

**OQ-1 … OQ-13 carry v1.10's dispositions** (OQ-13 closed by H-9).

**OQ-14 · Loop-layer oracle config and `P-5`** → **OPEN, lean unchanged** (v1.10 § I). v3.7.1 sharpens the
instrument: `a8` records every composition argument with its explicit/omitted flag. A loop switch passed
explicitly at a non-default value in an arm's `a8` rows is the `P-5` hazard OQ-14 names. *Not folded here.*

**OQ-15 · `TA-X-26(b)` under a closed pack** → **OPEN, lean unchanged** (v1.10 § I).

**OQ-16 · `TA-X-18`'s exact reading** → **OPEN pending the pre-read, lean unchanged** (keep `exact` as float64
equality; v1.10 § A.5). No pre-read of v1.10 was filed. H-7 now carries it.

⚑ **OQ-17 · Clause (c)'s antecedent is not sufficient for its own bound** (§ F.2k.7). → **LEAN: when clause (c) is
next re-derived (any remedy of § F.2k.6), key it on the computable inequality `m_o + W + c + 4 ≤ 1e-12/u`, with the
sink depths and totals emitted, rather than on `m_o` alone. Until then grade (c) as written.** *The claim to attack:
that a budget on `offered` alone was ever a sufficient check, given that the identity's residual carries the error
of seven accumulators.*

---

## § J · DISCIPLINES THIS VERSION EXERCISED

> ⚑ **A BUDGET IS DERIVED FROM THE METHOD THAT IS RUN, NOT FROM THE ONE THAT IS IMAGINED.** v1.5 sized clause (c)
> for "an accumulation" and counted one. The port runs seven, plus two uncounted inner sums. Reading the code
> before writing the bound is what found that. **The finding argues against firing**, which is what a derivation
> done to unblock an attempt has to be willing to do.

> ⚑ **A DEFINITION THAT LIVES IN PROSE IS AN INPUT NOBODY HASHED.** The arms were defined in this series' text from
> v1.6 to v1.10. At v1.11 they are pack rows, and this file cites them by id with a digest per arm.

> ⚑ **n = 5 IS A DESCRIPTION, NOT A TEST.** The salt-1 clear is printed with what five draws can and cannot
> distinguish. It is not explained away, and it is not promoted to a finding.

> **Carried:** Law 3 (no fitted constants; no tolerance or expected value moved toward a measurement) · the
> `F.1a` expiry clause · the honest-`n` law · `#75` cl. 1(a) · KP-101 (every digest labelled) · Discipline #12
> (the L2 corrigendum named as a precondition change) · **digests computed and filled by script, never typed.**

---

*Filed 2026-10-01 by **gamora** (simulation + spirit-guide seam), Run KC2-PLAY.
⚑ **v1.11 RE-PINS v1.10 FROM PACK v3.7 TO PACK v3.7.1** (KP-150 → KP-153). **No expected value moves on any of the 28
EXACT rows or the five preconditions.** The oracle and all 62 inputs it consumes are byte-identical to v1.10's,
and every oracle-derived value was recomputed and reproduces. **Every arm and the `TA-X-29(e)` walk are cited to the
`a8` rows that define them (§ B.1a).** ⚑ **R-11: the 4,500-term budget is derived from the port's actual summation
and STANDS. v1.11 attempt 1 cannot fire on the pass-3 runtime as measured** (§ F.2k). Remedies are listed, none
adopted. **Attempts: `0` of `2`, carried unspent.** The declared set is closed at exactly `["TA-X-06"]`. **`H-9` and
`H-10` discharged.** OQ-14, OQ-15 and OQ-16 open; OQ-17 new. **NO BAND WIDTH MINTED.** **K-7 held:** the sealed cells
were hash-verified only. This file's derivations exercised the oracle only through `load_profiles`,
`derive_oracle_speeds`, the U-P-N-5 static walk and `SpawnStructureFold.offset`. They read star-lord's v3.7.1 POST
artifacts and drax's runtime source, and modified neither. v1.10 and every earlier version are **NOT edited**.
⚑ **THIS FILE IS IMMUTABLE. Any change after a graded run exists against it is a HALT (`WARN-16`).**
**No production code. No dispatch. No push. D4 held: committed ALONE.***
