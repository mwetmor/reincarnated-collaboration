# KC2-PLAY · T-A PREREGISTRATION **v1.10**: v1.9 RE-PINNED to pack **v3.7** ("input closure")

> ⚑ **STATUS: IMMUTABLE ON COMMIT. v1.10, authored 2026-09-30. SUPERSEDES v1.9 FORWARD.**
> *(The filename carries the series' `2026-09-20` prefix. The document is dated 2026-09-30.)*
>
> ⚑ **v1.10 MOVES THE PACK OF RECORD FROM v3.6.1 TO v3.7.** star-lord cut v3.7 (KP-148) so that the
> oracle reads nothing the pack does not carry. The cut adds one member, `model/input_closure.json`
> (1,406 rows). **It is NOT purely additive: five existing rows had their TEXT edited** (V0-37,
> DPE-arcane_barrier, V13-POTION-1, V12-PATHS-1, V9-SITE-14; prior text in the `t6` rowset).
> **The oracle did not move.** Its code and data at engine HEAD `eee8ce8b` are byte-identical to
> v1.9's `266714dd`, and so are all 62 content files the closure proof says it consumes (§ A.2).
> So every oracle-derived value in v1.9 reproduces.
>
> ⚑ **ONE EXPECTED VALUE IS RE-DERIVED, NAMED SO IT CANNOT PASS AS A RE-PIN: `TA-X-18`.** The V9-SITE-14
> text fix puts on the wire the constant the oracle's scatter has always used, `FACING_SPAN_RAD =
> float32(2π) = 6.2831854820251465`, not `2π`. The oracle's own function, fed `u₁ = u₂ = 0.5`, returns
> **`(-3.999999999999985, -3.49691120014899e-07)`**, not `(−4.0, 0.0)`. v1.1 derived `(−4.0, 0.0)` from the law `θ = π`, and
> no build (the oracle, or a port built on `2π`) ever returned it exactly. **The delta is stated and
> derived from the oracle before any v1.10 result exists** (§ A.5). No other expected value moves.
>
> ⚑ **THE ARM QUESTION (KP-146) IS RESOLVED FROM THE PREREG'S OWN TEXT, AND v1.9 WAS AMBIGUOUS.**
> `TA-B-01`'s reference `[156, 152, 155, 152, 152]` is the **`M-POL-2` arm**. The `W1` arm gives
> `[156, 152, 155, 152, 155]`. v1.9's mandatory sentence said *"the v1.9 oracle terminates at…"* and did
> not name the arm. **v1.10 names it, and states for EVERY graded row which arm(s) the port's ORACLE
> configuration must run** (§ B.1a). No expected value was changed to fit a result.
>
> ⚑ **star-lord's DECLARED LIMIT IS RECORDED AND BINDS:** the closure is proven only for the `W1` and
> `M-POL-2` arms at `P-5`. **Most graded rows also run `M0`, `M-POL-2-NULL` and `W1-NULL`.** A closure
> re-run on those three arms (and on the `TA-X-29(e)` static walk) is **owed before attempt 1**
> (`H-10`, § H).
>
> ⚑ **ATTEMPTS: `0` OF `2` UNDER v1.10. THIS IS A CARRY, NOT A RESET.** No graded run exists under v1.9
> (no v1.9 verdict file exists; the ledger through KP-148 records none). v1.9's allowance, itself
> v1.8's carried from Matt's *"Reset to 2"* (KP-115), is carried **unspent**. v1.7's attempt 1 stays on
> the record as spent (`STRUCTURAL @ 89/89`).
>
> ⚑ **THE DECLARED SET IS CLOSED AT EXACTLY `["TA-X-06"]`** (Matt, Q83(b), KP-110). Carried.
>
> ⚑ **`H-9` IS DISCHARGED: PASS** (KP-146; evidence pinned below). **OQ-14 stays OPEN.**
>
> ⚑ **THIS FILE IS IMMUTABLE ONCE COMMITTED. ANY CHANGE AFTER A GRADED RUN EXISTS AGAINST IT IS A HALT
> TO MATT (`WARN-16`).**
>
> ⚑ **D4 HELD. This file is committed ALONE, with zero code, before any graded run against v3.7
> exists.** Every digest in it was computed this session from the files and filled into the document
> by script. None was typed or copied from a ledger row. Each digest is labelled **FILE** (sha256 of one
> file's bytes) or **ROWSET** (sha256 of a law applied to rows, or to a member list), per KP-101.
>
> **Authority:**
> * ⚑ **KP-147** (conductor): port pass 2 matches the oracle decision for decision only with ten folds'
>   inputs injected; the remedy is pack v3.7, then *"gamora prereg v1.10 (re-pin v3.7; budget 0/2
>   carried)"*.
> * ⚑ **KP-148**: pack v3.7 cut (star-lord; engine `fdd7c61f` prereg ALONE → `54968275` cut →
>   `eee8ce8b` MIGRATION). **Declared limit: closure proven for W1 + M-POL-2 at P-5 only.**
> * ⚑ **KP-146**: `H-9` PASS, and the flag for the pre-read: *"Gate-2 must confirm that the arm
>   `TA-B-01` grades on is the arm the harness runs."* **§ B.1a answers it.**
> * ⚑ **KP-137 (Matt): *"Finish the port first."*** A pack re-pin is a new version, not a HALT; substrate
>   only, no goalpost change. **`TA-X-18`'s re-derivation is the one place this version tests that
>   phrase; § A.5 argues it is substrate, and the pre-read should attack that argument.**
> * **Carried from v1.9 without change:** Q83(b), Q85, Q87, Q91, KP-115, KP-127, KP-131, KP-132, KP-144,
>   F5, jack-ryan's v1.8 pre-read (R-17…R-22), the `C-o` ceiling.
>
> **Author:** gamora (simulation + spirit-guide seam), Run KC2-PLAY. **Decision rules only. NO BAND WIDTH
> IS MINTED, AND EVERY WIDTH IN `P-a` STAYS VOID.** **v1.9 (`b787308c…`) and every earlier version
> are NOT edited.**

---

## § 0 · ⚑ THE v1.9 → v1.10 DELTA

**Legend.** **CARRIED** = assertion, expected value and derivation unchanged; substrate properties were
recomputed and reproduce. **RE-PINNED** = only a digest moves. **NOTE** = assertion and value unchanged,
but a v3.7 row changes how the row is derived, booked or run. ⚑ **RE-DERIVED** = the expected value moves,
derived from the oracle and the pack, with the delta stated. **ARM** = the graded arm(s) are now stated
(§ B.1a); the assertion and value are unchanged.

### 0.1 · Preconditions

| id | v1.10 | Δ value | why |
|---|---|---|---|
| `P-1` coverage 89/89 | **CARRIED** | none | census property; read the four-way counts off the run |
| `P-2` stream disjointness | **CARRIED** (within-epoch probe; epoch now v3.7, § C.7). **ARM:** `M-POL-2`, salt 0, port only | none | — |
| `P-3` roll population / law | **CARRIED.** POOL-466 recomputed from v3.7 `waves.json`: 466, set digest reproduces | none | `waves.json` byte-identical v3.6.1 → v3.7 |
| `P-4` pack identity | ⚑ **RE-PINNED v3.6.1 → v3.7** (model 18 members, reference 7, cross-pin) | digests only | KP-148 |
| `P-5` oracle fold settings | **CARRIED: the same eleven settings, values and line numbers** (the oracle code is byte-identical). ⚑ **NOTE:** the `v0_limb_set` diff (§ B.1) now reads V0-37 as `MotionLimb.GATE_FIRST (L-B)` | none | the text fix names the limb the oracle always ran (§ A.3) |

### 0.2 · EXACT rows (28) and the declared row

| id | v1.10 | Δ expected value | note |
|---|---|---|---|
| `TA-X-01` | **CARRIED; ARM** | none | the named arm, if outside {`W1`, `M-POL-2`}, is covered only after `H-10` |
| `TA-X-02` | **CARRIED** | none | — |
| `TA-X-03 / 04 / 05` | **CARRIED IN FORM; ARM**; the port's digests move (§ C.7) | none | ⚑ run `M0`, `M-POL-2-NULL`, `W1-NULL`: **outside the closure proof → `H-10`** |
| `TA-X-06` | **UNGRADEABLE-declared, CLOSED** | — | — |
| `TA-X-07` | **CARRIED VERBATIM; ARM (all 25 cells)** | none | ⚑ **NOTE (§ A.3):** DPE-arcane_barrier and V12-PATHS-1 change what `counterplay_absorbed` books: the barrier absorbs ANY damage type, deferred arrivals absorb at arrival, and the `dying` slot bypasses absorb. The identity is unchanged |
| `TA-X-08` | **CARRIED; ARM (all 25 cells)** | none | — |
| `TA-X-09` | ⚑ **RE-PINNED** (`math_rules.json` FILE `969f8090…` → `3b1e2d01`) | none: **15 rules, 29 vectors content-identical; the nine graded vectors ROWSET `0e692765` both sides** | the file moved only by V12-PATHS-1's text and a pointer key (§ A.3) |
| `TA-X-10` | **CARRIED; ARM (`W1`)**; recomputed `43.758085029822276` | none | `H-9` PASS: outcome 1, the row grades as written |
| `TA-X-11` | **CARRIED; ARM (`W1`, `W1-NULL`)** | none | `H-9` PASS. `W1-NULL` → `H-10` |
| `TA-X-12 / 13 / 14 / 15 / 16` | **CARRIED; ARM (all 25 cells)**; 54 / 47 recomputed | none | — |
| `TA-X-17` | **CARRIED; ARM (all 25 cells)**; 8.0 recomputed | none | NOTE: `ρ = 8.0·u₂` does not read `θ`, so V9-SITE-14 cannot move it |
| `TA-X-18` | ⚑ **RE-DERIVED** | ⚑ **`(−4.0, 0.0)` → `(-3.999999999999985, -3.49691120014899e-07)`**; Δ = `(1.509903313490213e-14, -3.49691120014899e-07)` | ⚑ § A.5. The tolerance stays **exact**, and v1.10 states what exact means |
| `TA-X-19` | **CARRIED; ARM (all 25 cells)** | none | NOTE: pass 2 ported deferred arrival (KP-147), so the row is no longer vacuous. V12-PATHS-1: the absorb at arrival reads no `px, py` |
| `TA-X-20 / 21` | **CARRIED** (probe / source scan; no arm) | none | — |
| `TA-X-22 / 24` | **CARRIED; ARM (all 25 cells)** | none | — |
| `TA-X-25` | **CARRIED; ARM (per arm per salt, 25)**; SWING-456 / NONSWING-10 recomputed | none | — |
| `TA-X-26` | **CARRIED** (no fight run); (e) recomputed `0.2468965517` / 17 | none | ⚑ **NOTE (§ A.4): clause (b) and the new member.** The pack's image of `pm4p_leech_resistance.csv` is a COLUMN PROJECTION; its bytes do not hash to `P-i`. (b) as written is met only by hashing the file the port loads |
| `TA-X-27` | **CARRIED**; (c) **ARM (all 25 cells)**; (d) recomputed 139 / 97 | none | NOTE: V9-SITE-14 changes no draw count (two draws per offset; registry 45 rows) |
| `TA-X-28` | **CARRIED; ARM (all 25 cells)** | none | — |
| `TA-X-29` | **CARRIED**; (e) recomputed **`3.207764` / `4.980316`, 39 / 39 per-record values exact** | none | ⚑ (e) is a STATIC walk, not a fight run; its call path is not the fight loop's → `H-10` (b) |
| `TA-X-30` | **CARRIED; ARM (all 25 cells)**; `d_engage_m` 2.4 recomputed | none | NOTE: V0-37 (GATE_FIRST) governs WHERE a body walks, not where it halts; `(a)` reads `d_engage_m` either way |

**Per-row delta in expected value: ONE, `TA-X-18`, re-derived from the oracle (§ A.5). NONE on the other
27 EXACT rows and the five preconditions.** Gradeability changed by declaration: **NONE.**

### 0.3 · Diagnostics, report face, verdict file

| site | v1.10 | why |
|---|---|---|
| `TA-B-01` terminal wave | **CARRIED: `[156, 152, 155, 152, 152]`**, `player_death` 5/5. ⚑ **ARM NAMED: `M-POL-2`** | § B.1a. The `W1` arm's `[156, 152, 155, 152, 155]` is printed beside `TA-X-06`, never as `TA-B-01` |
| `TA-B-15` | **CARRIED** (10/466 = 0.021459) | NONSWING-10 reproduces |
| `C-e / C-f / C-i` | **CARRIED** (×3.170 landed) | the oracle is unchanged |
| `C-o` | **CARRIED.** ⚑ **It does not cover `TA-X-18`** (§ A.5) | — |
| § F.3 `TA-B-01` sentence | ⚑ **the arm is written into the mandatory sentence** | § F.3 |
| § F.5 cl. 11 | ⚑ **EXTENDED:** the pack-closure defect of KP-147 | § F.5 |
| § G.2 hole table | ⚑ **EXTENDED:** the pack-closure item; the loop-layer closure moves to pass 3 | § G.2 |
| verdict file | `prereg_version: "v1.10"`; `substrate_epoch`; both pack pins; ⚑ `arm_of_record`; ⚑ `closure_H10`; `oracle_containment_H9` filled (PASS) | § G.3 |
| § G.1 counter | **`0` of `2` under v1.10** (carried unspent) | KP-115 / KP-137 / KP-147 |

### 0.4 · The counts

| | preconditions | **EXACT** | UNGRADEABLE-declared | DIAGNOSTIC ids | emitted-not-graded |
|---|---:|---:|---:|---:|---:|
| v1.9 | 5 | 28 | 1 (`TA-X-06`), closed | 19 (0 gating) | 3 |
| **v1.10** | 5 | **28** | **1 (`TA-X-06`), closed** | 19 (0 gating) | 3 |

⚑ **Q87's *"all EXACT rows green"* at v1.10 means the same 28:** `TA-X-01 · 02 · 03 · 04 · 05 · 07 · 08 ·
09 · 10 · 11 · 12 · 13 · 14 · 15 · 16 · 17 · 18 · 19 · 20 · 21 · 22 · 24 · 25 · 26 · 27 · 28 · 29 · 30`.
**Count history:** 26 (Q87) → 29 (v1.6) → 28 (v1.7 · v1.8 · v1.9) → **28 (v1.10). No row added or
removed.** `TA-X-23` stays struck and retired.

### 0.5 · What v1.10 deliberately does NOT fold in

1. **The KP-144 (b) loop-layer systems as `P-5` settings** (OQ-14, open). Pass 2 ported them and v3.7
   carries their inputs. Whether any is a default-OFF setting the graded oracle must ARM is still the
   runtime question OQ-14 names. **Not folded.**
2. **`C-h` / `OQ-9`**, **`C-k` / `OQ-11`**, **C-11b and REFERENT-v2**: not here, for v1.9's reasons.
3. **The side-by-side acceptance** (drax pass 3: NATIVE death wave = oracle on all five salts, G3 with
   ZERO injections). That is the conductor's acceptance and a seal-path criterion, not a v1.10 row.
   **This file names which oracle arm each figure belongs to** (§ B.1a), and rules nothing about it.
4. **A widening of `TA-X-26(b)` to accept the pack's image in place of the file** (OQ-15). Carried as
   written; the consequence is stated for the harness (§ A.4).
5. **The closure result on `M0`, `M-POL-2-NULL`, `W1-NULL`.** It is OWED (`H-10`), not assumed from the
   union of the two proven arms.

---

## ⚑ PINS: EVERY PIN COMPUTED THIS SESSION, FILLED BY SCRIPT, NONE TYPED

> **The standing rule (KP-20, KP-43):** a new version recomputes every pin it carries, including the ones
> it believes are unchanged. **All carried pins reproduce v1.9 exactly.** Both pack digests are
> **recomputed from the member files** with the manifest's `pack_digest_law_exact`, every member's
> FILE digest and byte count checked against its manifest row, and then compared to the manifest's
> `pack_digest`. They agree.

| # | artifact | label | **sha256 (computed 2026-09-30)** | v1.9 → v1.10 |
|---|---|---|---|---|
| P-a | `gamora/notes/2026-09-20-kc2-play-ta-band-widths.md`. Constructions only; every width VOID | FILE | `1c80f08075a1ed0e30e30b348752d2505b39994f7e2c55c348413f6e591248f9` | unchanged (reproduces v1.9) |
| P-b | `galadriel/notes/2026-09-20-kc2-play-w1-tb-expected-values-and-u-rider.md` | FILE | `d48512aa6e3c9ea70de6675750880a6c8914f0984c3cfe65c6ccb9a24403438f` | unchanged (reproduces v1.9) |
| P-c | `…/2026-09-20-kc2-play-w1-tb-expected-values.json` | FILE | `a8b85331764ba3fe90f45cf7cd6f1a25f6dc0dae4a7e7fa555c487f0b153ea0b` | unchanged (reproduces v1.9) |
| P-d | `…/2026-09-20-kc2-play-w1-tb-release-labels.json` | FILE | `15dace604c8d5bb4888223a8b25a07a038bae44431ebd194d682545c0f29c58a` | unchanged (reproduces v1.9) |
| P-e | `simulation/math/kc2-play-v3p4-roster-basis-rebase-2026-09-21.md` (lineage) | FILE | `4b7b78c834c7fbabd61700dda3e730a95ab89990bfa01470e8fb293f41ac7a73` | unchanged (reproduces v1.9) |
| P-e′ | `…/math/kc2-play-v3p3-monster-offense-prereg-2026-09-20.md` (lineage) | FILE | `27fc59378aee8c9d412f486a63864a3b2ceb5c5473520b60ad80128d47d99cdc` | unchanged (reproduces v1.9) |
| P-h | ⚑ **THE MODEL PACK** `kc2-model-pack-v3-E-s09-cp150-mech-v3p7-20260930_231652` (18 members, 18/18 verified: digest and bytes) | ROWSET (pack law) | `9bee0357f7ed8e15a89a980e3c2dd44e17526ab14d580065e2b7e8dd10d229c0` | ⚑ **RE-PINNED** v3.6.1 `3c50e631…` → v3.7 |
| P-h2 | ⚑ **THE REFERENCE PACK** `kc2-reference-pack-v3-E-s09-cp150-mech-v3p7-20260930_231652` (7 members, 7/7 verified); `cross_pin.model_pack_digest` verified equal to the derived model digest | ROWSET (pack law) | `978bb89340afa39646dcabf11c3beff1c33e9608505841d6dde29b316ce73936` | ⚑ **RE-PINNED** v3.6.1 `cca68a6c…` → v3.7 |
| P-i | `data/kc2/pm4p_leech_resistance.csv` (⚑ imaged in v3.7 as `IC7-F-44`, a column projection, § A.4) | FILE | `cb6a008bde1e102573181968ab7f60958cd28fee07ff8736078fa092a80dd62e` | unchanged (reproduces v1.9) |
| P-j | `data/kc2/pm4l_mitigation_by_body.csv` (lineage) | FILE | `a8c1ffd97dc703419f8447f3d7bbba3903e0f14d2c2e6746a938ceefae9ecec6` | unchanged (reproduces v1.9) |
| P-k | `data/kc2/pm2_tg2_monster_timing.csv` (`ANCHOR-169`'s carrier) | FILE | `58205679e36f0e0361ccd41c844d6bc254ada034447dd1f80e2a46a2b47c7aca` | unchanged (reproduces v1.9) |
| P-l.c2 | `simulation/math/kc2-c2-per-cast-energy-cost-fold-2026-09-28.md` | FILE | `b42684e55325bd4caf705b1e7d43462acb5c5818cd5abe3d79eb0d3b9ba6f8c7` | unchanged (reproduces v1.9) |
| P-l.c7 | `…/kc2-c7-insufficient-energy-refuse-fold-2026-09-29.md` | FILE | `072f9ab787ec840a9bc62ae76a0576fa5db7be0da0b63457851557ea164a7e1f` | unchanged (reproduces v1.9) |
| P-l.nine | `…/kc2-play-nine-winner-surface-reconstruction-2026-09-29.md` | FILE | `2c7c3679af67569fff88bb56837ea1ba37499fe9fcbeca85ab63a473b0d7a6dd` | unchanged (reproduces v1.9) |
| P-l.upn4 | `…/kc2-play-upn4-occupancy-by-pilot-2026-09-29.md` | FILE | `787d1a99d9adfedbb34bda69a3c530a653a8df3fc117969e3920c5625791a3cf` | unchanged (reproduces v1.9) |
| P-l.upn5 | `…/kc2-play-upn5-global-magnitude-fold-lift-2026-09-29.md` | FILE | `bfa44b4722ec8b7326987042101f32310c986e3fae489a4372fcc4e0dd5553c7` | unchanged (reproduces v1.9) |
| P-l.upn5A | `…/kc2-play-upn5-global-magnitude-fold-lift-ADDENDUM-2026-09-29.md` | FILE | `5323c1fa9f156e80ced5b1324e4297150cfc759c4e54426f440c33a6c9745fc6` | unchanged (reproduces v1.9) |
| P-l.q91 | `…/kc2-play-q91-338-pool-damage-lift-2026-09-29.md` (governs `TA-X-25` and `P-5` setting 3) | FILE | `d68561d59723c3295da3f0456f2fbeaefe8f5f0a30b41d29b5ff0e366966a385` | unchanged (reproduces v1.9) |
| P-l.q91a | `…/kc2-play-q91-338-pool-damage-lift-ADDENDUM-2026-09-29.md` | FILE | `b9ada804e17c01b376e64e82b7e45f66a344d1fc2fc75a0fdd1fd76c56e2cddc` | unchanged (reproduces v1.9) |
| P-l.c11a | `…/kc2-play-c11a-oracle-corrections-fold-2026-09-30.md` (governs `P-5` setting 11) | FILE | `4af38999ff0544cc9607b34da4fde29fe2c55324e9829894c516cd9837689445` | unchanged (reproduces v1.9) |
| P-l.c11aA | `…/kc2-play-c11a-oracle-corrections-fold-ADDENDUM-2026-09-30.md` | FILE | `17a068fe980869e6e344fdf3a652dc275f5cc3a3d65818f2976fe94084d48666` | unchanged (reproduces v1.9) |
| P-n.1 | `simulation/output/kc2-play-q91-pool-lift-pricing-20260930_023137.json` (the `M-POL-2` seat, § B.1a) | FILE | `f33ce0c0cbeb00bbed7b47a6f7660f20d4aa2be1694f9f4e2486e37d27b553e2` | unchanged (reproduces v1.9) |
| P-n.2 | `simulation/output/kc2-lifted-rows-KC2PLAY-SEALLAP-W1-c2-energy-fold-20260928_232836.json` (the `x8` input `from_x8` reads) | FILE | `cc361a3fea3e24e55fdf0c8c8eaf52bcc0c729c7de0563d3c84dd0dc21202960` | unchanged (reproduces v1.9) |
| P-n.3 | `simulation/output/kc2-play-c11a-fold-pricing-NOT-A-GRADED-RUN-20260930_043045-SUMMARY.json` (`TA-B-01`'s reference: ⚑ the **`M-POL-2`** seat, § B.1a; `C-f` / `C-i`) | FILE | `b6c9e7953f5b5632ec2dc51c2c8602461aef15d4721f69432444e6f777e1141e` | unchanged (reproduces v1.9) |
| P-n.4 | `simulation/output/kc2-play-c11a-landed-by-source-NOT-A-GRADED-RUN-20260930_033242.json` | FILE | `ad018b78a7f85491020a237166af797845bb5de2e562816673fbf925bb41ff1e` | unchanged (reproduces v1.9) |
| P-o | `data/kc2/c11a_aura_buff_grants.csv` (the C2 grant table; imaged in v3.7 as `IC7-F-04`) | FILE | `749d58f45eb312e7a284734a1844f2aabcfd69b7219dd1dafc55e4bb6d64792f` | unchanged (reproduces v1.9) |

### Set digests: the populations v1.10 grades over

**Law:** `sha256("\n".join(sorted(record_paths)).encode("utf-8"))`, no trailing newline. **ROWSET.**
Recomputed this session: POOL-466 off v3.7 `waves.json` by both routes of `kc2_baton_v3p5p1_schema.pool466`
(routes agree); SWING-456 / NONSWING-10 as `ThreatProfile.can_swing` over POOL-466 from the oracle's
`load_profiles` under `P-5`'s exact loader call; FALLBACK-158 from `build_mover` /
`monster_run_speed` via `derive_oracle_speeds` (partition 128 / 180 / 158, `march_base` 3.209466).

| set | n | label | sha256 | v1.9 → v1.10 |
|---|---:|---|---|---|
| **POOL-466** | 466 | ROWSET | `33c886a11f91db1143c791ffcf9d95f7e7614e423373235231733c994c5c157b` | reproduces v1.9 |
| **SWING-456** | 456 | ROWSET | `706a61d55dc6621814fc923d7428c5b263a95ebb00e9786d12f35dd385a7a4c0` | reproduces v1.9 |
| **NONSWING-10** | 10 | ROWSET | `00b4cb0e24b43e591a2e30200979725801aad1e7c1f9b7764ebef67461816e10` | reproduces v1.9 |
| **FALLBACK-158** | 158 | ROWSET | `e8114efaa8fa678db6a26bb6e4ffb926fc2c1a15a978e3d589cf918ff17ae6cb` | reproduces v1.9 |

### Documents of record

| document | label | sha256 |
|---|---|---|
| ⚑ prereg **v1.9** (superseded, **not edited**; v1.10's only predecessor; collab `d52193c72`) | FILE | `b787308c8c331e98fee6221c97174bf8f696a5b55d699611c5ab697625de95dd` |
| prereg v1.8 (not edited; collab `948bb8082`) | FILE | `69e1de1890a24fb9d9a4dc37cda6edfc39e6c34e45b877a2999b565b4710c49c` |
| prereg v1.7 (not edited) | FILE | `552d9faecd83d955c77f2be35991ec51e3908d9f586ab70b5a78b6c156b92896` |
| prereg v1.6 (not edited; § A.5 / § F.2: `TA-B-01` = `[M-POL2]`'s terminals) | FILE | `db2c0ca3c6cdba022b83d0229439a3ad9e0709cd25732304ffc979a200be7b0e` |
| jack-ryan's v1.8 pre-read (R-17…R-22, incl. R-21) | FILE | `5358cb8cc99dcf1dd998e875e911d6ae53e9046dab0d24abe28a5c83193d5dff` |
| jack-ryan's v1.7 pre-read | FILE | `ff1df4a18e9e60c1a5543edb391eded667b11711b340cd4763f3cdd204cab1ff` |
| jack-ryan's Gate-2 on attempt 1 (R-1…R-12) | FILE | `d2aa93db92122e033927f63ff61c9e6a2c13e1c7cba09a4fff20cb2382de6c37` |
| attempt-1 grade note (§ 3: run-internal rows graded 25/25; `TA-X-18` graded as a three-law discriminator) | FILE | `9778b4de4aa05acb2396439d2ff9de264ec590475ebf56aec93f3912ba12505e` |
| attempt-1 verdict file | FILE | `9be2d56bfdc49c51c611402ec953b5f59dbfc0c866cdaf5201e0e57d74df08b2` |
| jack-ryan's v1.6 pre-read | FILE | `5a5f45d76098746ce1dbd31d0091b9a7d62f16978fb52a21ff27990181e0b6c0` |
| the grade of record (`gamora/notes/2026-09-21-kc2-play-ta-grade.md`) | FILE | `600f68a7378329c298cd69863903804a6ab7d1ee8a27f666688717f741b9c1c3` |
| the discrimination audit | FILE | `852d0bd7d637280cbc42e2ba8494ea7e163b4f6c91741f24eb0ef3da105e674a` |
| divergence register v0.3 (file form) | FILE | `5028b555313df2f4690cd96881c700c7d66a4733612894c150c2448915510444` |
| ⚑ `H-9` evidence: `NOTE.md` (collab `dccc7d8ff`) | FILE | `90717b83926f06b5939a48c01c0cc4973d5f20d7d7eb60007b976d01ebde53e5` |
| ⚑ `H-9` evidence: `h9_out_W1.json` (the `W1` terminals `[156,152,155,152,155]`) | FILE | `c68fcd3c133c8b8a55d75e85425876fe73d6d1752dfdd1cd21fa9041e87a24ff` |
| ⚑ `H-9` evidence: `h9_out_M-POL-2.json` (reproduces P-n.3 `PW-FOLDED`) | FILE | `2aedf43f2091d0c575af1d7d07deb0278be87f0b4c917efa5c33d01e77707f61` |
| ⚑ `H-9` evidence: `h9_out_W1-NULL.json` | FILE | `90b9ea619e8adfd3f8532cc55e16990c15348dd537071c5758000c2edafdf801` |
| ⚑ `H-9` evidence: `h9_w1_containment.py` | FILE | `eede32e85f362b5d57b136b81344cae1bfd4b804515db2d6f2d66279d1920f55` |
| ⚑ star-lord's **v3.7 cut prereg** (`export/math/2026-09-30-kc2-pack-v3-7-input-closure-prereg.md`, engine `fdd7c61f`) | FILE | `ccf17ae6ffd06cb17d72ee88e34657fef8a1a16a70839b8ad091e4fdb1f7db05` |
| ⚑ the **v3.7 cut receipt** (`output/kc2-baton-v3-cut-receipt-v3p7-20260930_231652.json`, engine `54968275`) | FILE | `5de7beb2b4c3ad5ab4325fc372783977c86fd1fcd2750d78ccf94c6514baaf98` |
| ⚑ the closure instrument `export/kc2_v3p7_closure.py` (engine `54968275`; `H-10` extends it) | FILE | `964bfce7de8c36a8dd6ceb44ab72984b8fa6ddd4c3187a278463a5ce0f2cdaf2` |
| ⚑ closure table BEFORE (`output/kc2-v3p7-closure-table-BEFORE-20260930_231652.json`) | FILE | `e6eeadb42e6928b9d45d2242b0b6cc81ee720709b95148efe8c17184757253b4` |
| ⚑ closure table AFTER (`output/kc2-v3p7-closure-table-AFTER-20260930_231652.json`) | FILE | `e9a5c05e164172b5514e2fa1c323da243bee6fa7e7dc878ade4f4651eebc3805` |

### Sealed cells: hash-verified only. K-7 held (never opened for execution, never re-run)

| cell | path (`reincarnated-engine/src/reincarnated/simulation/output/`) | label | sha256 | bytes |
|---|---|---|---|---:|
| `[M-POL2]` | `kc2-checkpoint-E-s09-cp150-mpol2-20260825_114420.json` | FILE | `ad61ad2a8c799d6ef11a68436756c253f0a34fbb1052e575cdf9f9cd3a44dc5c` | 123,564 |
| `[MECH]` | `kc2-checkpoint-E-s09-cp150-mech-20260816_124031.json` | FILE | `20b05cb4ef3bd888b998cbc46c68b41a8051111c12fbcf2066d101b0a4b15f4b` | 2,125,271 |
| `[W1W]` | `kc2-checkpoint-E-s09-cp150-w1walls-20260825_220058.json` | FILE | `7a992c81ca6e56e54a53534b438a9ddf87ed42f1bf1a3d0ecc2d2f3c3db7881b` | 403,084 |

---

## § A · WHAT MOVED, DERIVED

### A.1 · The pack, member by member (v3.6.1 → v3.7)

**Model: 11 of 17 carried members byte-identical; 6 moved; 1 added.** Derived from the member files by a
recursive key-by-key comparison, not from the cut's receipt:

| member | v3.6.1 → v3.7 (FILE) | what changed |
|---|---|---|
| `config_of_record.json` | 56413c9a… → 136f3a20… | ⚑ **TEXT EDIT** `⚑ v3p2_rows.v0_fold_limb_of_record[36]` (**V0-37**): `value`, `precedence`; new key `⚑ v3p7_corrected_rows` |
| `input_closure.json` | — → 273baca8… | ⚑ **NEW MEMBER** (1,406 rows, seven rowsets) |
| `math_rules.json` | 969f8090… → 3b1e2d01… | ⚑ **TEXT EDIT** `⚑ v3p2_rows.v12_counterplay[2]` (**V12-PATHS-1**): `value`, `provenance`; new key `⚑ v3p7_corrected_rows`. `rules` (15), `vector_law`, `vector_weakness`, `lifted_mechanics`, `unlifted` content-identical |
| `meta.json` | 4c58422d… → 28a9b889… | changed `emitted_at_utc`, `emitted_by`, `headline`, `lap_manifest`, `pack_revision`; new keys `⚑ v3p7_input_closure`, `⚑ v3p7_supersession` |
| `player_kit.json` | ca199806… → 2b68af93… | ⚑ **TEXT EDIT** `devotion_procs.envelope_rows[4]` (**DPE-arcane_barrier**): `value`; ⚑ **TEXT EDIT** `⚑ v3p2_rows.v13_potion_and_warcry[0].value` gains `⚑ gate` (**V13-POTION-1**); new key `⚑ v3p7_corrected_rows` |
| `provenance.json` | 7d4cebb6… → 1d06e08a… | new key `⚑ v3p7_precedence_vocabulary` only |
| `rng_contract.json` | ff6f77b0… → 232ad93c… | ⚑ **TEXT EDIT** `⚑ v3p2_rows.v9_draw_site_registry[13].value` gains `⚑ FACING_SPAN_RAD` (**V9-SITE-14**); new key `⚑ v3p7_corrected_rows` |

**Reference: 6 of 7 byte-identical; 1 moved:** `reference/meta.json` (25874cfb… → 2580495a…;
changed keys `emitted_at_utc`, `emitted_by`, `headline`, `pack_revision`; new keys `⚑ v3p7_input_closure`,
`⚑ v3p7_supersession`). ⚑ `waves.json`, `arena.json`, `monsters.json`, `monster_offense.json`,
`monster_defense.json`, `monster_kinematics.json` and `controllers.json` are **byte-identical**, which
is why `TA-X-10 / 16 / 17 / 25 / 27(d) / 30` recompute to v1.9's values.

**The seven new rowsets of `model/input_closure.json :: ⚑ v3p7_rows`, ROWSET digests recomputed here** by
the pack's law (`sha256(json.dumps(rows, sort_keys=True, separators=(",",":"), default=str))`). Each
equals the digest on the wire (`meta.json :: ⚑ v3p7_input_closure`):

| rowset | rows | label | sha256 |
|---|---:|---|---|
| `c5_class_constants` | 4 | ROWSET | `4e65efdc89ddd0da3f5f00625833f4df1e0c98551965d56a51975f06a596ee7d` |
| `d4_defaults_via_omission` | 711 | ROWSET | `9ef59a4ac5d9726d0afa74cab9e8600ca0c81f9ce1e1537b0139b5324da36758` |
| `f1_file_images` | 51 | ROWSET | `1b0eeec7ad68c4ca5987bed70532ae3504ef031a0b284940c5c6928972682776` |
| `k3_code_constants` | 612 | ROWSET | `51714f6476b3ca4fe7b0f673aa50e40d044a9af4102c2b8a44fd78e4a686e5d1` |
| `p2_reader_products` | 11 | ROWSET | `cb6d43ab8573f6609799f93a7f51649ae7c5c1b076009ed32853cc30a2ed05db` |
| `t6_text_corrigenda` | 5 | ROWSET | `38580e85d38deaa84d990c21bde85c1059c0e08a9cdd561803f8f9a526951761` |
| `x7_derived_crosschecks` | 12 | ROWSET | `61c0eadfa2292c4efc91c8df7b44c6bccee7a2cc412cf44736db1957769b6fa5` |
| **all v3.7 rows** (the whole `⚑ v3p7_rows` object) | 1,406 | ROWSET | `130c578ea44d7ce3999f3fff24679f56c1b4585309c0f20b9bf7a9f859b69402` |

### A.2 · ⚑ The oracle did not move, and neither did anything it reads

* `git diff --quiet 266714dd eee8ce8b -- src/reincarnated/simulation src/reincarnated/data data` exits
  **0**; so does the same diff from `96b4529a` (v1.8's HEAD). The commits since v1.9's HEAD touch only
  `export/` (the v3.7 emitter, schema, closure instrument, prereg, MIGRATION, AGENT_STATE), `output/`
  and one test. **The oracle's `kc2/` tree is git tree object `d974998f805b8bc5d620f27d88dd4e8f14972357` at both `266714dd`
  and `eee8ce8b`** (a git tree id, neither FILE nor ROWSET; an identity only). The working tree is
  clean on `simulation/kc2` and `data/kc2`.
* ⚑ **Widened at v1.10: the oracle's INPUTS, not only its tree.** The closure proof enumerates the 62
  content files the oracle consumes (51 CSV images `f1`, 11 reader products `p2`). **Each was re-hashed
  on disk this session and equals the FILE digest its row carries: 62 / 62.** Seven live in
  `reincarnated-collaboration` (legolas Lap R / U / V / X / Z / AA notes); none has a commit since
  2026-08-16 and none is dirty. The other 55 are engine files covered by the tree identity above.
  **So the oracle that H-9, P-n.3 and v1.9 measured is the oracle v1.10 grades against, input for
  input.**
* **Recomputed anyway**, because a byte identity proves the input did not move, not that the reading of
  it was right:
  * POOL-466 / SWING-456 / NONSWING-10 / FALLBACK-158: all four set digests reproduce; 466/466 profiled;
  * `TA-X-29(e)`, config E: **`3.207764` at w159, `4.980316` at w160**; all **39** per-record ratios
    equal v1.9's § F.2h table exactly; the ten-wave walk reproduces
    (`3.353866 · 1.768566 · 1.899330 · 2.994929 · 1.927777 · 2.846875 · 1.979824 · 1.592632 · 3.207764 · 4.980316`);
  * `TA-X-26(e)`: ARMED-464 mean `0.2468965517`, median 0.25, max 0.35, min 0.0, 17 leech-immune;
  * `TA-X-10`: `max‖spawn_xy‖ + placement_extents_m = 43.758085029822276` off v3.7 `arena.json`;
  * `TA-X-16` 54 / 47 · `TA-X-27(d)` 139 / 97 · `TA-X-30` `d_engage_m` 2.4 · `TA-X-17` 8.0;
  * `TA-X-09`: 15 rules and 29 vectors content-identical; the nine graded vectors' ROWSET equal both
    sides (§ A.3);
  * `TA-X-18`: **re-derived, not reproduced** (§ A.5).
* **`TA-B-01`'s reference `[156, 152, 155, 152, 152]` stands**, and it is the `M-POL-2` arm (§ B.1a).
  star-lord's closure run reproduced it on that arm as an inertness check (his prereg § 0).

### A.3 · ⚑ THE FIVE EDITED ROWS, READ AGAINST EVERY GRADED ROW

Every row of the v1.9 instrument was checked for a citation of, or a dependence on, each edited row. **A
row not named below neither cites nor depends on any of the five.**

| edited row (member) | what the fix says (READ off the oracle, `t6` evidence) | graded rows that read it | Δ |
|---|---|---|---|
| **V0-37** (`config_of_record`) | `motion_limb` = **`MotionLimb.GATE_FIRST (L-B)`**, precedence `DRIVER-OF-RECORD`: the i26 driver builds `PursuitFold(march_target_player=True)`, whose `motion_limb()` returns GATE_FIRST (`pursuit.py:359`). `ZONE_FIRST` was the incumbent it replaces | **§ B.1's `v0_limb_set` diff** (a boot condition, no EXACT row). `TA-X-30`: the halt reads `d_engage_m`; the limb chooses the march target, not the halt | **no value.** The V0 diff's expected `motion_limb` line is `GATE_FIRST (L-B)`. A runtime that booted to the old text was booting to a limb the oracle never ran |
| **DPE-arcane_barrier** (`player_kit`) | the 2,900 pool is **UNFILTERED**: `CounterplayLayer.absorb` (`counterplay.py:735-782`) reads no damage type; order raw → ×(1 − War Cry) → Turtle Shell → Arcane Barrier → Ascension | `TA-X-07` (the `counterplay_absorbed` sink) | **no value.** A port that filters by type still balances the identity while being wrong: trap 12's shape (§ E.1) |
| **V13-POTION-1** (`player_kit`) | gate = **COOLDOWN ONLY** (`counterplay.py:707`); `charges` (1) is read and never consulted | **none.** The potion sits in the counterplay layer (hole-closure, § G.2). `TA-B-01` is diagnostic and its oracle side is unchanged | none |
| **V12-PATHS-1** (`math_rules`) | absorb applies on direct hits, auras, DoT ticks **and deferred projectile arrivals at arrival** (`run.py:3507`); **the `dying` slot BYPASSES absorb** (`run.py:2967-3000`) | `TA-X-07` (booking); `TA-X-19` (arrival unconditionality); `TA-X-09` (file pin) | **no value.** `TA-X-07`: deferred-arrival absorbs book to `counterplay_absorbed` at arrival; `dying`-slot damage never does. `TA-X-19`: the absorb reads no `px, py`. `TA-X-09`: rules and vectors content-identical; nine-vector ROWSET `0e692765` on both packs |
| **V9-SITE-14** (`rng_contract`) | `FACING_SPAN_RAD` = **6.2831854820251465 = float32(2π), NOT `math.tau`** (`spawn_structure.py:169`, consumed at `:330`, `theta = FACING_SPAN_RAD · u1`) | ⚑ **`TA-X-18`**; `TA-X-17`; `TA-X-10`; `TA-X-27` | ⚑ **`TA-X-18` RE-DERIVED (§ A.5).** `TA-X-17`: `ρ = 8.0·u₂` does not read θ. `TA-X-10`: the bound is `max‖spawn‖ + ρ_max`, θ-free, and H-9 measured the oracle already running float32 θ. `TA-X-27`: two draws per offset, 45 registry rows, count unchanged |

### A.4 · ⚑ THE NEW MEMBER, READ AGAINST EVERY GRADED ROW

`model/input_closure.json` carries **inputs**, not graded quantities. No EXACT row cites it. Two rows
meet it:

* ⚑ **`TA-X-26(b)`: *"`pm4p_leech_resistance.csv` is LOADED, its sha is verified against `P-i` =
  `cb6a008b…`"*.** The pack now images this file (`IC7-F-44`) with `sha256 = cb6a008b…` as a declared
  field. **But the image is a COLUMN PROJECTION:** it carries the 12 columns the oracle reads, not the
  file's whole rows. Re-serialising it cannot reproduce the file's bytes; I tried with both line
  endings and the digests do not match. **So a port that loads the table ONLY from the pack cannot
  itself compute `P-i`.** The row is carried **as written**. **Harness requirement (H-4):** (b) is met
  only by hashing the bytes of the CSV the port loads. A port that reads only `IC7-F-44` does not meet
  (b). *The declared field is pack-authenticated, because `input_closure.json`'s FILE digest is verified
  under `P-4`. Whether that should satisfy (b) is OQ-15. It is not ruled here, because a clause that
  reads "the sha is verified" cannot be met by a sha that is only quoted.*
* **`TA-X-26(c)`** (7,900 rows · 790 records · 8 distinct `total_leech_resist_pct` · 5 distinct
  `adcth_mult_COUPLED` · 790/790 wave-invariant) **can be computed from the image**, which carries
  `record`, `wave`, `total_leech_resist_pct` and `adcth_mult_COUPLED`. Recomputed from `IC7-F-44`:
  7,900 · 790 · `{65, 75, 83, 88, 105, 115, 565, 588}` · `{0.0, 0.12, 0.17, 0.25, 0.35}`. No change.
* `x7` rows (e.g. the K-MILL speed 4.029485432492994) are **derived cross-checks, not inputs**. No row
  grades them.

### A.5 · ⚑ `TA-X-18` RE-DERIVED: THE ORACLE'S SCATTER NEVER RETURNED `(−4.0, 0.0)`

**What the row asserts (v1.1 → v1.9, unchanged in form):** feed the scatter `u₁ = u₂ = 0.5`; the result
discriminates three laws: polar (`ρ = 8·u₂`), uniform-in-area (`ρ = 8·√u₂`) and the retired box.

**What v1.1 derived:** *"`POLAR_UNIFORM_RHO` → `θ = π, ρ = 4.0` → `(−4.0, 0)`"*. That is the law with
`θ = 2π·u₁` idealised. **The oracle does not compute `2π·u₁`.** `SpawnStructureFold.offset`
(`spawn_structure.py:311-338`, the default `POLAR_UNIFORM_RHO` + `RngRepr.CONTINUOUS`) computes
`theta = FACING_SPAN_RAD * u1`, with `FACING_SPAN_RAD = float(pm4aa_placement_law.json ::
random_facing.value)` = `0x40c90fdb` = **6.2831854820251465**. The pack says so on its face at v3.7
(V9-SITE-14). The file it comes from has not changed since 2026-08-16. **So the oracle has returned the
value below at every epoch this row has existed.**

**Measured on the oracle this session**, calling `SpawnStructureFold().offset` with a stream that
returns 0.5 twice:

| law (oracle constants) | `offset(0.5, 0.5)` |
|---|---|
| ⚑ **`POLAR_UNIFORM_RHO` (of record)** | ⚑ **`(-3.999999999999985, -3.49691120014899e-07)`** |
| uniform-in-area, same θ | `(-5.656854249492359, -4.945379245665078e-07)` |
| `INCUMBENT_BOX` | `(0.0, 0.0)` |
| *(not a law of record: polar built on `math.tau`)* | `(-4.0, 4.898587196589413e-16)` |

**Delta vs the v1.9 expected value:** `(1.509903313490213e-14, -3.49691120014899e-07)`. **The discrimination survives:**
the three laws stay separated by at least 1.656854 m.

⚑ **The tolerance stays `exact`, and v1.10 says what exact means:** both components equal to the
oracle's float64 values, compared at full round-trip precision (`repr`). **This is a semantic shift, and
I am naming it, not burying it (Discipline #12).** The attempt-1 grade of record could not grade
`(−4.0, 0.0)` literally, because nothing produces it. It graded *"polar `(−4.0, 4.9e-16)`"* GREEN as the
nearest of three laws with pairwise separation `> 1e-6` (`2026-09-21-kc2-play-ta-grade.md`, `TA-X-18`
row; the attempt-1 grade note). **Under that reading the row cannot see the V9-SITE-14 defect.** A port
built on `2π` sits `3.5e-7` from the oracle, inside `1e-6`. With the oracle's own value as the expected
value, `exact` is attainable, so it is applied as written.

**Why this is substrate, not a goalpost (the claim to attack).** (1) The oracle's value was not chosen;
it was read by calling the oracle, and no v1.10 port result exists. (2) The value v1.9 carried could not
be met exactly by any build, so carrying it is not a neutral option: it would leave the row's verdict to
a grader's unwritten reading. (3) The fix is to the EXPECTED value only. Assertion, tolerance class and
population are unchanged.

**`C-o` does not cover this row.** The probe is a pure function of two fixed inputs and one wire
constant. The port's positions are float64 (KP-147 (c)). If the port's `cos`/`sin` are the platform
libm, as CPython's are, the bits agree. **A last-ulp disagreement is not pre-declared.** Should one
occur, it is a question for Matt under `F.1a`, never a widening by the grader.

---

## § B · CONFIGURATION AND PRECONDITIONS: five

### B.1 · `ORACLE` *(carried from v1.9 § B.1, which carries v1.8 § B.1)*

`V0`, five arms (`M0`, `M-POL-2`, `M-POL-2-NULL`, `W1`, `W1-NULL`), five salts, **25 headless runs**, the
limbs of record, `v_ref` 4.0 → 5.4 m/s, motion law `V0-04`, declared fight scope waves 151–160, leg A
(stop at the player's first death). **Pilot:** U-P-N-4's `SEALED-KMILL` (`DRIVE_TO_PACK`,
`seek_fold=True`, `kinematics=True`), as v1.9 § B.1 corrected. The runtime prints its resolved limb set
(`v0_limb_set`), diffs it against `V0` before any row is read, and refuses to boot on an unset limb.
⚑ **At v1.10 that diff reads V0-37 as `MotionLimb.GATE_FIRST (L-B)`** (§ A.3), plus v3.6.1's pointers
(`V0-24` → `R8-LAW`, `V0-39` → `G12-LAW-CONTACT`, `V0-40` → `G12-LAW-SOLVE`).

### ⚑ B.1a · THE ARM OF RECORD, PER GRADED ROW (the KP-146 question)

**The question.** `TA-B-01` states `[156, 152, 155, 152, 152]`. The oracle's `M-POL-2` arm gives that. Its
`W1` arm gives `[156, 152, 155, 152, 155]` (H-9, `h9_out_W1.json`: salt 0 also ends 6.286 s into w156
rather than 7.184 s, and salt 4 dies at w155 rather than w152, because the avoidance veto moves the
fight). Which arm does `TA-B-01` read?

**The answer, from the prereg's own text.** `M-POL-2`, on four independent grounds:
1. **v1.6 § A.5 and § F.2** set the row's oracle side as *"`[M-POL2]`'s `terminals` array"*. v1.6–v1.9's
   mandatory sentence opens *"The oracle's sealed `M-POL-2` arm terminates at…"*.
2. **v1.8 § A.5**, where the current reference was derived, reads it from P-n.3's `PW-FOLDED`. That is the
   C-11 harness, `c11.run_arm(runner, …)` → `runner(salt, period_s, seat=True)`
   (`gamora_kc2_c11_lethality_decomposition_2026_09_29.py:310`). **No `arena=` is passed, so
   `arena_fold` is `None`: that is the `M-POL-2` seat** (`make_runner`,
   `gamora_kc2_w1w2_lift_build_2026_08_25.py:134-199`). P-n.1's LIFT / CONTROL arms (v1.8 § D) come from
   the same seat via `upn4.run` (`gamora_kc2_upn4_occupancy_by_pilot_2026_09_29.py:256`, no `arena=`).
   **"LIFT arm" there is a pricing-arm label, not a `V0` arm.**
3. **H-9 reproduces `PW-FOLDED` exactly on `M-POL-2` (arena `None`) and on `W1-NULL`** (`TA-X-04`'s
   relation), terminals and seconds-into-wave both, and **not** on `W1`.
4. **star-lord's closure run** names it: *"The M-POL-2 arm (the arm `TA-B-01` grades)"*
   (`kc2_v3p7_closure.py:9-10`; v3.7 prereg § 0).

⚑ **So v1.9 was ambiguous.** Its sentence said *"The v1.9 oracle (the same object as v1.8's…) terminates at
`[156, 152, 155, 152, 152]`"* and never named the arm. The run emits five arms, and a harness that
compared its `W1` terminals would read a false miss on salt 4. ⚑ **THE FIX, NAMED:** the § F.3 sentence
now says *"the v1.10 oracle's `M-POL-2` arm"*, and the table below is part of `H-4`'s harness
requirement. **The expected value did not change. Only the arm it belongs to is now written down.**

**THE TABLE: which arm(s) the port's `ORACLE` configuration must run for each graded row.** Rule used:
a row whose statistic names arms grades on those arms. A run-internal row that names none grades on
**every cell the graded run emits (5 arms × 5 salts)**, which is how the grade of record evaluated them
at attempt 1 (25/25 throughout its § 3). **The "basis" column of § F.2 names the sealed cell a property
was established on. It is not a population.** "No run" = a probe, scan or pack computation, with no arm.

| row | arm(s) × salts | inside the closure proof (W1, M-POL-2)? |
|---|---|---|
| `P-2` | `M-POL-2` × salt 0 (port-only probe) | yes |
| `TA-X-01` | one NAMED arm+salt ≠ (`M-POL-2`, 0), run twice | only if the named arm is `W1` or `M-POL-2`; else `H-10` |
| `TA-X-02` | no run (census) | — |
| `TA-X-03` | `M-POL-2-NULL` and `M0` × 0–4 | ⚑ **no → `H-10`** |
| `TA-X-04` | `W1-NULL` and `M-POL-2` × 0–4 | ⚑ **`W1-NULL` no → `H-10`** |
| `TA-X-05` | `M-POL-2` and `M0` × 0–4 | ⚑ **`M0` no → `H-10`** |
| `TA-X-06` | `W1` vs `M-POL-2` × 0–4: **printed, not graded** | yes |
| `TA-X-07` | all 25 cells | ⚑ **partly → `H-10`** |
| `TA-X-08` | all 25 cells | ⚑ partly → `H-10` |
| `TA-X-09` | no run (pack vectors) | — |
| `TA-X-10` | `W1` × 0–4 | yes |
| `TA-X-11` | `W1` and `W1-NULL` × 0–4 (*"every W1 arm"*; `W1-NULL` reads 0 on a faithful port) | ⚑ `W1-NULL` → `H-10` |
| `TA-X-12` · `13` · `14` · `15(a)` · `16` · `17` · `19` · `22` · `24` · `28` · `30(b)` | all 25 cells | ⚑ partly → `H-10` |
| `TA-X-15(b)` · `30(a)` | the law, by construction / as declared | — |
| `TA-X-18` · `20` · `21` | no run (probe / scan) | — |
| `TA-X-25` | per arm per salt, all 25 cells | ⚑ partly → `H-10` |
| `TA-X-26` | no fight run ((c) and (e) are pack / CSV computations) | — |
| `TA-X-27` | (a) scan · (b) per-seed replay · **(c) all 25 cells** · (d) pack census | ⚑ (c) partly → `H-10` |
| `TA-X-29` | (a)–(d) loader and pack; **(e) the static config-E walk** (not a fight run) | ⚑ **(e) → `H-10` (b)** |
| **`TA-B-01`** (DIAGNOSTIC) | ⚑ **`M-POL-2` × 0–4** | yes |
| `TA-B-15` (DIAGNOSTIC) | per arm per salt | partly |
| R-11 smoke (`H-6`) | `M-POL-2` × salt 0 (v1.8 § F.2d's cell); `TA-X-07(c)`'s budget binds on every cell | yes |

⚑ **The oracle reference figures, by arm, so no figure travels to the wrong arm:**

| arm | oracle terminal waves (leg A), salts 0–4 | seconds into terminal wave | source |
|---|---|---|---|
| `M-POL-2` | **`[156, 152, 155, 152, 152]`** | `[7.184, 4.408, 7.02, 7.184, 6.122]` | P-n.3 `PW-FOLDED`; reproduced by H-9 |
| `W1-NULL` | `[156, 152, 155, 152, 152]` (≡ `M-POL-2`, `TA-X-04`) | as `M-POL-2` | H-9 `h9_out_W1-NULL.json` |
| `W1` | `[156, 152, 155, 152, 155]` | `[6.286, 4.408, 7.02, 7.184, 6.939]` | H-9 `h9_out_W1.json` (FILE `c68fcd3c`) |

*`M0` and `M-POL-2-NULL` at `P-5` have not been measured on the folded oracle. No figure is minted for
them, and no row needs one.* ⚑ **For the conductor, named and not ruled:** the pass-3 acceptance figure
*"NATIVE death wave = oracle on all five salts"* is the `M-POL-2` arm's. Compared against a port `W1`
arm, it would red salt 4 on a faithful port.

### B.2 – B.4 · `P-1`, `P-2`, `P-3` *(carried from v1.9 by reference; P-3's cardinalities recomputed: POOL-466 = 466, set digest reproduces)*

### B.5 · ⚑ `P-4` · PACK IDENTITY: both v3.7 packs and the cross-pin

```
model_pack_dir       : "kc2-model-pack-v3-E-s09-cp150-mech-v3p7-20260930_231652"
model_pack_digest    : 9bee0357f7ed8e15a89a980e3c2dd44e17526ab14d580065e2b7e8dd10d229c0   (ROWSET: pack law over 18 member rows)
reference_pack_dir   : "kc2-reference-pack-v3-E-s09-cp150-mech-v3p7-20260930_231652"
reference_pack_digest: 978bb89340afa39646dcabf11c3beff1c33e9608505841d6dde29b316ce73936   (ROWSET: pack law over 7 member rows)
cross_pin_verified   : reference.manifest.cross_pin.model_pack_digest == model_pack_digest
                       (9bee0357f7ed8e15a89a980e3c2dd44e17526ab14d580065e2b7e8dd10d229c0 — equal: true)
```

| # | `model/` member | label | sha256 (computed) | bytes | v3.6.1 → v3.7 |
|---|---|---|---|---:|---|
| 1 | `ai_states.json` | FILE | `928ded88e74e636422cbc107bdb02ff4cf27521dc74636e5e7e0e1680bd6060e` | 2,497 | identical |
| 2 | `arena.json` | FILE | `15078b583364bd1953d8d9480f95a1194a2b01ba8915d87fa9f83dde6e6d75be` | 426,450 | identical |
| 3 | `config_of_record.json` | FILE | `136f3a2072c0f99c8a03a61b1e2ac804d43af3396f588401f9284a5b47412d11` | 28,112 | ⚑ **MOVED** |
| 4 | `controllers.json` | FILE | `b4217daac06f2f55acb3ec68571dd7766d31ac156ee01ee903b721f26042e478` | 5,384,891 | identical |
| 5 | `input_closure.json` | FILE | `273baca8de8d2e24ca3139a1bb3e1b76e8f10bd4aca064071a4b4fda77afb5e2` | 27,102,021 | ⚑ **ADDED** |
| 6 | `math_rules.json` | FILE | `3b1e2d014411cb314d5cbf42ea40773dbcfa3de242f13d3a1d31eb830643b62d` | 188,662 | ⚑ **MOVED** |
| 7 | `meta.json` | FILE | `28a9b8894f162b6c3f6349e8aeae0a2d7a760b37d743a75b4ab9609906ff058e` | 126,090 | ⚑ **MOVED** |
| 8 | `monster_defense.json` | FILE | `00ffab1576577164cc132b498817d5480822df3234f3f3bcf286c0a407193aac` | 8,816,113 | identical |
| 9 | `monster_kinematics.json` | FILE | `b8b1c7b4e491aeb13981b26478c12190ec7efd892eddeeb6eef572f1766bc549` | 965,515 | identical |
| 10 | `monster_offense.json` | FILE | `fad592f5cb1d10030ca4ddd5788f65d3e01c0fc5781a75b73e50693d5f9ea76b` | 17,763,540 | identical |
| 11 | `monsters.json` | FILE | `3839322955b7d4af0a6c8c8b169656136a0271a7ab9bb68893a272df703701a0` | 15,211,150 | identical |
| 12 | `player_kit.json` | FILE | `2b68af939b6c795c1b4c9f0411aa037fb4d0332f983fa942aa307c85329eeac6` | 143,191 | ⚑ **MOVED** |
| 13 | `projectiles.json` | FILE | `ed32ff8a648d2b3c24918cd20150f27856b371e2a45a0e699cc1c8b6c949a0e5` | 74,198 | identical |
| 14 | `provenance.json` | FILE | `1d06e08a1744c8df7e188725f2c2bc5cdbbdf4d1007e75dba01a33fc9f8a0710` | 651,204 | ⚑ **MOVED** |
| 15 | `rng_contract.json` | FILE | `232ad93c6fc982bd5b564ab8f27f684696cd20326a4e3b9f12cc31db39d65fca` | 32,351 | ⚑ **MOVED** |
| 16 | `summons.json` | FILE | `6a7cc5af2bd7291b46c1beafedf2e13b70990a3f9a1a194f2092c1a64e586a93` | 111,259 | identical |
| 17 | `target_selection.json` | FILE | `e1df3cf69d2f3f91cce5ab5f9a71de4b7be4fb2372d18de2cc99517d399d68ce` | 31,936 | identical |
| 18 | `waves.json` | FILE | `38c43a9c3b35560a3dce88ac16c189cb03b120b1ba2085ae2458040113621072` | 1,087,499 | identical |

**Reference pack (7), FILE each:** `acceptance.json` `f5ce2c174cccf9a253603ac8bfc3f20b872b2e2a92c8d24e461601e64f1f9853` (4,716 B) · `actors.json` `ef03536f97fe7122e14b34ae69a26bc7616fe58fcbe5989ab3aa09e7420ea04b` (1,956,876 B) · `meta.json` `2580495aa63a293975ebb9b067611bda2fc208d515c475dd7d1a600e4188df83` (106,529 B; ⚑ MOVED) · `rng_tape.json` `607bf3bffd6a5a330d2ede97eebcd7139f3c218292954aa56fbf38c34e833ea0` (406 B) · `skill_interrupt_reference.json` `45522df26b1703ac2489d08e7e7fa6986255ca80e64f057279ca6b492fdf3707` (3,113 B) · `tracks.json` `bb3495218fcdeaab11d4d5e9a5d25a2e14f2fd21384bcebc7dd1f93b0b7d9bfd` (44,733 B) · `u7_heading_conditioning.json` `5ad6ab0f089d3409506f29293433849f6abcbd1bee2a2242344fe12367287c05` (3,601 B)

**The manifests themselves (FILE; not the pack digest, and not substitutable for it):** model
`manifest.json` `129f1a2297bab2698ccdd915bad93a0fa4ab65fbf5b8ca8542c5828808ca2e7b` · reference `manifest.json` `99dbf9494de5f71678d4f9b99a96f6156746ed7d7b16266ba598295225ec6803`.

⚑ **`P-4` is red on any other pack.** v3.6.1 (`3c50e631…` / `cca68a6c…`), v3.6 and earlier are **not
the pack of record**. ⚑ **The grader checks the runtime header first,** reading the `.app` / runtime
header's `pack_digest` **by running the binary**.

### ⚑ B.5a · R-21's HEADER RE-PIN

R-21 (jack-ryan, v1.8 pre-read) is jack-ryan's criterion; this file supplies the pin it reads. At v1.10:

```
R-21 (a) header model pack_digest     == 9bee0357f7ed8e15a89a980e3c2dd44e17526ab14d580065e2b7e8dd10d229c0   (P-4; read by RUNNING the binary)
R-21 (a) header reference pack_digest == 978bb89340afa39646dcabf11c3beff1c33e9608505841d6dde29b316ce73936   (P-4; read by RUNNING the binary)
R-21 (b) P-5: the SAME eleven settings as v1.8/v1.9, unchanged in name, value and site; refuse-to-boot on any unset one
```

⚑ **The harness must also move** (the `H-4` class): the prereg it pins (its label is read from the
pinned prereg, now this file), the `substrate_epoch` string, ⚑ the per-row arm configuration of
§ B.1a, and ⚑ `TA-X-26(b)`'s file hash (§ A.4). **The grader verifies all four on the emission, not on
a commit message.**

### B.6 · `P-5` · THE ORACLE FOLD SETTINGS: ELEVEN *(carried from v1.8 § B.6 via v1.9, unchanged)*

Same eleven settings, values, sources and line numbers (engine HEAD `96b4529a`; the oracle tree is
byte-identical at `266714dd` and `eee8ce8b`). Same loader call:
`load_profiles(dot_corrections=True, pet_special_gates=None, winner_surface=WinnerSurfaceFold.from_x8(P-n.2),
pool_lift=pool_lift.load(), c11a=C11aLoader(scope=AuraScope.CLASS))`. v1.9's note on setting 6 is carried.
⚑ **The closure proof ran at exactly this configuration** (star-lord v3.7 prereg § 0), so `P-5` and the
proven closure are the same object on `W1` and `M-POL-2`.

---

## § C · THE LAWS

**C.1–C.6 and C.8: carried BY REFERENCE from v1.9 § C** (which carries v1.8 / v1.7 § C).

### ⚑ C.7 · THE EPOCH LAW, EXTENDED TO v3.7

> ⚑ **A v3.3, v3.4.2, v3.6, v3.6.1 and v3.7 PORT board are pairwise NOT draw-comparable at a fixed salt.
> No row, diagnostic or report line may compare across them.**

**Mechanism, stated before anyone measures it:** at v3.7 the port runs natively the ten folds it ran as
identity at pass 2 (K-MILL seek constants and speed, MovementPolicy cadence and dash layers, the alert
animation table, player summons, control application, the WaveScaling count-law rows, the TTK-by-body
table, banner anchors and `SHEET_PHYSICAL_MODIFIER_PCT`; KP-147). The board count law alone changes
body counts (w151: 24 → 28). **The port's stream moves.** ⚑ **The ORACLE is the same object at every one
of these epochs** (§ A.2), and its references carry over for that reason.
**`substrate_epoch = "v3.7 / model 9bee0357… / reference 978bb893…"`** for everything graded under this
document.

---

## § E · OUTSIDE T-A'S REACH

### E.1 · The traps *(v1.9 § E.1 carried; trap 12 extended)*

| # | trap | at v1.10 |
|---|---|---|
| 1–11 | *(carried from v1.9 § E.1 as written)* | as v1.9 |
| **12** | **A STREAM BOOKED NOWHERE SATISFIES A CONSERVATION IDENTITY VACUOUSLY.** ⚑ **v3.7 adds two booking facts** that `TA-X-07` cannot see: the Arcane Barrier absorbs every damage type (a type-filtered port under-absorbs yet balances), and the `dying` slot bypasses absorb (a port that absorbs it over-absorbs yet balances) | caught only by the hole-closure finding and G3 (§ G.2) |

### E.2 · Declared ceilings

**All of v1.9 § E.2 carried as written, including `C-o`.** ⚑ **One boundary stated:** `C-o` (representation
limits) does **not** extend to `TA-X-18` (§ A.5).

---

## § F · THE GRADED ROWS

**§ F.1 (decisiveness classes, `F.1a`), § F.2a (`TA-X-26`), § F.2b (`TA-X-27`), § F.2c, § F.2d (`TA-X-07` and
R-11's law for both outcomes), § F.2e (`TA-X-06`), § F.2f (`TA-X-25`), § F.2g (`TA-X-28`), § F.2h
(`TA-X-29`, restated in v1.9 with the 39 per-record values, all reproduced here) and § F.2i (`TA-X-30`)
are carried BY REFERENCE from v1.9 / v1.8** (pinned above), unchanged in assertion, class, tolerance and
expected value. The notes of § 0.2 / § A.3 / § A.4 and the arms of § B.1a apply to them as written there.
⚑ **R-11's law is re-applied:** R-11 is re-measured on the graded pass-3 runtime before attempt 1, and a
smoke above 4,500 terms means the attempt does not fire.

### F.2 · EXACT rows: 28, plus `TA-X-06` UNGRADEABLE-declared (closed)

| id | statistic | basis | tolerance | arm(s) (§ B.1a) | v1.10 |
|---|---|---|---|---|---|
| `TA-X-01` | port self-determinism; the arm+salt is NAMED and MUST DIFFER from `P-2`'s | run-internal | byte-exact | one named | CARRIED |
| `TA-X-02` | coverage 89/89, zero unmapped | census | integer | — | CARRIED |
| `TA-X-03` | `port(M-POL-2-NULL, s) ≡ port(M0, s)`, all 5 | `[M-POL2]` | byte-exact | M-POL-2-NULL, M0 | CARRIED IN FORM |
| `TA-X-04` | `port(W1-NULL, s) ≡ port(M-POL-2, s)`, all 5 | `[W1W]` | byte-exact | W1-NULL, M-POL-2 | CARRIED IN FORM |
| `TA-X-05` | `port(M-POL-2, s) ≢ port(M0, s)`, ≥ 1 salt | `[M-POL2]` | exact, one-sided | M-POL-2, M0 | CARRIED IN FORM |
| `TA-X-06` | `port(W1, s) ≢ port(M-POL-2, s)` | `[W1W]` | **EMITTED AND PRINTED, NOT GRADED** | W1, M-POL-2 | **UNGRADEABLE-declared, closed at exactly `["TA-X-06"]`** |
| `TA-X-07` | `offered = applied + dropped + voided + pool_truncated + pcl_reclaim + counterplay_absorbed` | run-internal | relative ≤ 1e-12; ~4,500-term budget | all 25 | CARRIED VERBATIM; NOTE § A.3 |
| `TA-X-08` | denominator identity, both sub-identities | `[M-POL2]` 5/5 | exact | all 25 | CARRIED |
| `TA-X-09` | all **9** `math_rules.test_vectors` of the five normative channel/release/interrupt/damage rules | `P-4`'s `math_rules.json` (FILE `3b1e2d01…`) | per-vector | — | ⚑ RE-PINNED (nine unchanged) |
| `TA-X-10` | `max_body_radius_m ≤ 43.758085029822276` (W1), roster movers | `[W1W]` · `arena.json` | exact, ≤ | W1 | CARRIED (`H-9` PASS) |
| `TA-X-11` | `n_wall_clamps_{player,body} == 0`, every W1 arm | `[W1W]` | integer | W1, W1-NULL | CARRIED (`H-9` PASS) |
| `TA-X-12` | pool inertness under ORACLE: total pool damage `== 0.0` | `[W1W]` · `DIV-19` | exact | all 25 | CARRIED |
| `TA-X-13` | no player crit | `V0 · CritLimb LO` (`S13-CRIT` = 1.0) | integer | all 25 | CARRIED |
| `TA-X-14` | the two DO-NOTs; a REFUSED cast is not a release | `math_rules` prohibitions | integer | all 25 | CARRIED |
| `TA-X-15` | (a) p01–p04 at `t = 0.0`, p05 one burst at `t = 4.000 s` (tick 49); (b) no intra-point stagger | census `M4` / `V11` | exact | all 25 / — | CARRIED |
| `TA-X-16` | p06 OFF: `n_pool_picks == 47`, `n_spawn_point_6_keys_rolled == 0`, a filtered-keys counter | `waves.json` | integer | all 25 | CARRIED (54 / 47) |
| `TA-X-17` | `‖spawn_xy − anchor_xy‖ ≤ 8.0` m, every roster placement | `placement_extents_m` | exact, ≤ | all 25 | CARRIED |
| `TA-X-18` | `u₁ = u₂ = 0.5` → ⚑ **`(-3.999999999999985, -3.49691120014899e-07)`** (not uniform-in-area `(-5.656854249492359, -4.945379245665078e-07)`, not box `(0.0, 0.0)`) | the oracle's `SpawnStructureFold.offset` · `arena.json` extents · V9-SITE-14 `FACING_SPAN_RAD` | ⚑ **exact: float64 equality per component at `repr` precision** | — | ⚑ **RE-DERIVED (§ A.5)** |
| `TA-X-19` | arrival unconditionality; no damage predicate reads an arrival's `px, py` | `deferred_arrival.py:13-17` | integer | all 25 | CARRIED (no longer vacuous) |
| `TA-X-20` | 2.99 m hit / 3.01 m miss; no angular gate; no target cap | census `D7` | exact | — | CARRIED |
| `TA-X-21` | quantisation rule per site + zero bare `round(` on the port's threat path | four modules | exact | — | CARRIED; re-verify the live site list at emission |
| `TA-X-22` | `cause == "interrupts_channel_flag"` is 0 under ORACLE | `V0`; V18+V19 | integer | all 25 | CARRIED |
| ~~`TA-X-23`~~ | ~~board-roll composition~~ | struck at v1.2, retired | — | — | — |
| `TA-X-24` | attack phase is `ENGAGE`; `sha256(actor_id) mod n` never evaluated; roster and pet attackers | `V0` | exact | all 25 | CARRIED |
| `TA-X-25` | the spawn partition, four clauses (v1.8 § F.2f); pool-rolled roster bodies | P-l.q91 + `u5` + the oracle's profile predicate | integer identity | per arm per salt | CARRIED |
| `TA-X-26` | declared-join conformance, five clauses (v1.8 § F.2a) | `P-i` | integer / exact / declared-precision | — | CARRIED; ⚑ (b): hash the loaded file (§ A.4) |
| `TA-X-27` | degenerate-draw consumption, four clauses (v1.8 § F.2b) | `P-4` | integer / byte-exact | (c) all 25 | CARRIED |
| `TA-X-28` | leech target law, three clauses; every hit body, pets included | § F.2g | integer / structural | all 25 | CARRIED |
| `TA-X-29` | global-magnitude fold conformance, five clauses; (e) `3.207764` / `4.980316` + 39 per-record ratios | § F.2h | integer / declared-precision | (e) static walk | CARRIED |
| `TA-X-30` | the pursuit halt, two clauses; (b) counted on the step's verdict, roster movers | § F.2i | exact / integer | all 25 | CARRIED |

### ⚑ F.2j · `H-9`: DISCHARGED, OUTCOME 1 (PASS). `TA-X-10` / `TA-X-11` GRADE AS WRITTEN

The v1.9 law (outcome 1: rows grade as written; outcome 2: the attempt does not fire and it goes to Matt)
was applied by the evidence at collab `dccc7d8ff`
(`agentic_orchestration/gamora/analyses/2026-09-30-kc2-play-h9-w1-containment/`; `h9_out_W1.json` FILE
`c68fcd3c133c8b8a55d75e85425876fe73d6d1752dfdd1cd21fa9041e87a24ff`). ORACLE `W1` under `P-5`, geometry ON, leg A, salts 0–4:
`max_body_radius_m` = `[43.404802385345796, 41.97652009526441, 43.40481520803243, 41.97652009526441, 43.40478928727287]`; `n_wall_clamps_body` = `[0, 0, 0, 0, 0]`;
`n_wall_clamps_player` = `[0, 0, 0, 0, 0]`. Minimum margin **0.353270 m** (salt 2). **Outcome 1.** The oracle is
byte-identical at v1.10 (§ A.2), so the discharge carries: **no re-run is owed.** OQ-13 is closed by it.

### F.3 · DIAGNOSTIC rows: 19 ids, 0 gating, every width VOID *(carried from v1.9 § F.3)*

⚑ **CLASS V · `TA-B-01`, reference sentence (mandatory, verbatim at v1.10; ⚑ the arm is now written in):**
***"`BAND / NON-DECISIVE / REPORT-ONLY`. A terminal wave inside or outside this band is not evidence of
fidelity either way. It is read from the port's `M-POL-2` arm. The oracle's sealed `M-POL-2` arm
terminates at `[156, 152, 151, 151, 156]`, `player_death` on every salt. The v1.10 oracle's `M-POL-2`
arm (the same object as v1.8's and v1.9's: the 338 armed, the winner surface armed, the C-11a
corrections folded) terminates at `[156, 152, 155, 152, 152]`, `player_death` on every salt, and no salt
reaches wave 160. A port that clears to wave 160 has not survived a hard board; it has failed to be in
one."*** ⚑ **Printed beside `TA-X-06`, never as `TA-B-01`, gating nothing:** the port's `W1` terminals
next to the oracle `W1` arm's `[156, 152, 155, 152, 155]` (H-9). `TA-B-13`'s, `TA-B-14`'s and `TA-B-15`'s
sentences are carried verbatim.

### F.4 · Emitted, not graded: **three** *(carried)*

### F.5 · Report-face rules: twelve

**Cl. 1–6, 8, 9, 10 and 12 carried verbatim from v1.8 § F.5 via v1.9.** Changed:

7. **THE SUSTAIN SENTENCE (mandatory; version label only):** ***"`leech` and `intake` still have no
   oracle side in the seals (`C-e`). Off-seal, the v1.10 oracle (the same object as v1.8's and v1.9's;
   the C-11a corrections folded) KILLS THE PLAYER AT WAVES 152–156 on salts 0–4, and lands ×3.17 the
   referent's intake over waves 151–159 on the landed grain. The port's own figure is printed from this
   run and not asserted here. A GREEN T-A IS COMPATIBLE WITH ANY RELATION BETWEEN EITHER REPLICA AND THE
   REFERENT."***
11. ⚑ **THE PORT≠ORACLE HOLES (mandatory on any report, including a passing one; EXTENDED):**
    ***"Port≠oracle holes 1–17 (PCL dropped · death after heal · damage rows unreachable · `tree_attack`
    slots never chosen · dying slots mishandled, and 5b one dying slot per death · slot
    chance/cooldown/delay never read · the wrong march base · to-hit · mitigation order · DoT timeline ·
    monster crit tier · motion order and the contact fold · Soulfire and the bleed rider · monster pets ·
    the resist cap · attack speed and OA adds · the HI life block), the chance-gate boundary, the C-11a
    grant law, the loop-layer defects of KP-144 (deferred arrival · player summons attacking · the
    counterplay/sustain layer · the K-MILL pilot with patrol/alert · energy income · the board seeding),
    and the pack-closure defect of KP-147 (ten folds run as identity because their inputs lay outside the
    pack) are invisible to every EXACT row in this instrument. A v1.10 PASS is not quotable without
    jack-ryan's hole-closure finding at the same runtime digest, and the seal is blocked on any non-zero
    R-6 invariant."*** Followed by the three R-6 invariants, **printed with their values** (§ G.2).

---

## § G · FAIL TAXONOMY, THE HOLE-CLOSURE RULE, AND THE GRADED-RUN CAP

| verdict | antecedent | consequence |
|---|---|---|
| **`STRUCTURAL`** | ≥ 1 of the 28 EXACT rows RED | the port is wrong; **consumes one of v1.10's two attempts**; L2 applies |
| **`INDETERMINATE`** | 0 EXACT red, ≥ 1 of the 28 UNGRADEABLE (incl. `P-1`…`P-5` red, and `TA-X-07(c)` above its depth budget) | does NOT consume an attempt; nothing seals |
| ~~`STATISTICAL`~~ | retired at v1.5 under F5 | — |
| **`PASS`** | all 28 EXACT green, none UNGRADEABLE | ⚑ **`PASS @ coverage k/89, 28/28 EXACT rows green, TA-X-06 UNGRADEABLE-declared (Q83(b)), dilution ⟨d⟩×, substrate_epoch v3.7/9bee0357…, prereg v1.10`**. Never unqualified, and **never quotable alone (§ G.2)** |

**Order:** `STRUCTURAL → INDETERMINATE → PASS`; stop at the first hit. No diagnostic appears in any
antecedent. **No post-hoc widening, by anyone.** `declared_ungradeable` must be **exactly**
`["TA-X-06"]`; anything else is **C1** (non-conforming). ⚑ **A row graded on an arm other than § B.1a's
is non-conforming (C1), not red and not green.**

### ⚑ G.1 · THE GRADED-RUN CAP: **`0` OF `2` UNDER v1.10**

⚑ **The allowance is carried unspent** (Matt KP-115 *"Reset to 2"*; KP-137; KP-147 *"budget 0/2 carried"*;
no graded run exists under v1.8 or v1.9). **Q85's four guards hold:** (1) the allowance was ruled from
outside the run (Matt); (2) this prereg is committed ALONE, every pin recomputed, before anything is
graded against v3.7 (D4); (3) v1.7's attempt 1 stays on the record, spent; (4) `substrate_epoch` is
declared on every artifact. **Naming:** the next graded run is **v1.10 attempt 1 (overall attempt 2)**.

⚑ **L2, AS IT APPLIES TO v1.10.** v1.10 attempt 1 fires only after ALL of the following:
- drax's **pass 3** (KP-147 / KP-148) has landed with its acceptance shown: NATIVE death wave per salt
  equal to the oracle's on all five salts, and G3 with ZERO injections (the conductor's acceptance).
  ⚑ The oracle figure for that comparison is per arm (§ B.1a);
- jack-ryan's **repair Gate-2 (R-1…R-22 + G3)** PASSes that runtime, on the digest it names (R-7);
- **this file's pre-read** has been filed (`H-7`);
- **R-11** re-measured on that runtime at ≤ 4,500 terms (`H-6`);
- `H-9`: **discharged, outcome 1** (§ F.2j); nothing further owed;
- ⚑ **`H-10`** reads outcome 1 (§ H).

v1.10 attempt 2 fires only after a v1.10-attempt-1 `STRUCTURAL` red is repaired and jack-ryan's Gate-2
PASSes the repair. An `INDETERMINATE` consumes nothing and buys nothing.

### ⚑ G.2 · THE HOLE-CLOSURE RULE: SEAL-BLOCKING, NOT VERDICT-BLOCKING *(the rule carried; the table extended)*

**v1.9 § G.2's table is carried row for row** (holes 1–17, 5b, the chance gate, the C-11a grant law, the
KP-144 loop layer, the board seeding; closures as written there). **Changed and added:**

| hole | what | ledger / commit | closure |
|---|---|---|---|
| — | the loop layer (KP-144 (b)) | KP-143 / KP-144 / KP-147 | pass 2 ported it (KP-147, godot `27839ad` … `774ca16`, **relayed**); ⚑ **its native acceptance moves to pass 3** + repair Gate-2 |
| ⚑ — | ⚑ **the pack-closure defect**: ten folds run as identity because their inputs lay outside the pack (K-MILL seek constants and measured speed · MovementPolicy cadence CSV, dash layers, the 4.9699 baseline · `d1_alert_anim.csv` · player summons · control application · the WaveScaling count-law adj rows · `pm4x_ttk_by_body.csv` · banner anchors + `SHEET_PHYSICAL_MODIFIER_PCT`) | KP-147 / KP-148 (engine `54968275`) | **drax pass 3 + its acceptance** (NATIVE death wave = oracle 5/5, G3 zero injections) + repair Gate-2; ⚑ **`H-10` for the arms the proof did not run** |
| ⚑ — | the five pack-TEXT defects (V0-37 · DPE-arcane_barrier · V13-POTION-1 · V12-PATHS-1 · V9-SITE-14) | KP-147 / KP-148 (`t6`) | fixed in the pack. **`TA-X-18` now grades the V9-SITE-14 constant** (§ A.5). The other four: repair Gate-2 + G3 |
| *(all)* | — | — | R-1 · R-2 · R-4 · R-7 · R-8 · R-19 · R-20 · **R-21 (re-pinned, § B.5a)** · R-22 (disposed, KP-144) |

**R-6, the three invariants, printed on the report face and never in an antecedent:** (i) cells with
`killer_id` set and `terminal_reason == cleared` = **0** · (ii) in-tick resurrections = **0** · (iii)
`PercentCurrentLife` intake **> 0** wherever a PCL row fired. ⚑ **R-9, carried as law of this
instrument:** a v1.10 `PASS` is quotable only with jack-ryan's hole-closure finding GREEN at the SAME
runtime digest; any non-zero R-6 invariant blocks the seal; **Q87's seal at v1.10** = `PASS` (28/28) AND
coverage 89/89 AND T-B reported DIAGNOSTIC AND the hole-closure finding GREEN at the graded digest AND
**Matt's T-C yes on that same digest** (KP-114).

### G.3 · Verdict file `kc2play.ta_verdict.v1` (v1.10): **the fields that change from v1.9 § G.3**

```
prereg_version                    : "v1.10"
prereg_sha256                     : <this file, derived at emission>
substrate_epoch                   : "v3.7 / model 9bee0357… / reference 978bb893…"
model_pack                        : {dir: "kc2-model-pack-v3-E-s09-cp150-mech-v3p7-20260930_231652", digest: 9bee0357…, files_verified: 18}
reference_pack                    : {dir: "kc2-reference-pack-v3-E-s09-cp150-mech-v3p7-20260930_231652", digest: 978bb893…, files_verified: 7}
cross_pin_verified                : true
runtime_header                    : {"model_pack_digest": <read by RUNNING the binary>, "reference_pack_digest": <same>,
                                     "must_equal": "P-4 (§ B.5)", "read_by_running": true}      R-21 (§ B.5a)
preconditions.P4_pack             : {"model":<dir>,"reference":<dir>,"files_verified":25,"mismatches":0,"cross_pin":true}
arm_of_record                     : {<row id>: [<arms>], …}   ⚑ § B.1a verbatim; TA-B-01: ["M-POL-2"]
oracle_containment_H9             : {"max_body_radius_m": [43.404802385345796, 41.97652009526441, 43.40481520803243, 41.97652009526441, 43.40478928727287], "n_wall_clamps_body": [0, 0, 0, 0, 0],
                                     "n_wall_clamps_player": [0, 0, 0, 0, 0], "outcome": 1, "evidence": "c68fcd3c…"}
closure_H10                       : {"arms": ["M0","M-POL-2-NULL","W1-NULL"], "walk_TA_X_29e": <bool>,
                                     "not_in_pack": {"files":<n>,"constants":<n>,"defaults":<n>,"class_constants":<n>},
                                     "outcome": 1|2, "evidence": <FILE sha>}     ⚑ § H; report face, never an antecedent
ta_x_18_expected                  : "(-3.999999999999985, -3.49691120014899e-07)"   ⚑ § A.5
port_holes_printed                : true    (§ F.5 cl. 11, extended)
```

**Every other field is v1.9 § G.3 unchanged**, including `set_digests` (the four digests reproduce),
`P5_folds` (eleven), `declared_ungradeable` (**exactly** `TA-X-06`), `gmag_conformance`
(`3.207764` / `4.980316`), `nodata` and `hole_closure`. **T-B quoting cap: C1 / C2 / C3 unchanged.**

---

## § H · OWED BEFORE v1.10 ATTEMPT 1 (blocking)

| # | owed | owner | why it blocks |
|---|---|---|---|
| **H-1** | the port on v3.7 **with pass 3**: every fold running natively off the pack, the acceptance shown (NATIVE death wave = oracle on 5/5, per arm per § B.1a; G3 with ZERO injections) | **drax** | at pass 2 the port dies at w160 natively (KP-147) |
| **H-2** | `spawn_by_record` per arm per salt, over roster bodies only | drax | `TA-X-25(c)` is UNGRADEABLE without it |
| **H-3** | `TA-X-29(e)`'s probe values: `3.207764` / `4.980316` + the 39 per-record values (unchanged) | drax | R-1 |
| **H-4** | ⚑ **the harness re-pointed to THIS file**: label from the pinned prereg; `substrate_epoch` = v3.7; ⚑ the § B.1a arm table as its per-row configuration; ⚑ `TA-X-26(b)` by hashing the loaded CSV (§ A.4); ⚑ the V0 diff reading V0-37 = GATE_FIRST; `TA-X-18`'s expected value (§ A.5); every stale field restated (R-10) | drax | read literally, a v1.9-pinned harness mislabels a v1.10 run and grades `TA-B-01` on an unnamed arm |
| **H-5** | the hole-closure finding at the graded digest (§ G.2) | **jack-ryan** | `PASS` is not quotable without it |
| **H-6** | R-11 re-measured on the graded pass-3 runtime | drax | above 4,500 terms the attempt must not fire |
| **H-7** | **this file's pre-read** | **jack-ryan** | D4 / the series' practice. ⚑ **Attack § A.5 (`TA-X-18`) and § B.1a first** |
| **H-8** | Matt's T-C re-confirm on the graded digest | Matt | a seal condition, not an attempt precondition |
| ~~H-9~~ | ~~the oracle's `W1` containment under separation~~ | gamora | ⚑ **DISCHARGED: outcome 1, PASS** (KP-146; § F.2j) |
| ⚑ **H-10** | ⚑ **THE CLOSURE PROOF ON THE ARMS AND CONFIGURATIONS IT DID NOT RUN.** (a) `kc2_v3p7_closure.py capture` over **`M0`, `M-POL-2-NULL`, `W1-NULL`** at `P-5`, salts 0–4, leg A, composed as the sealed drivers compose them (`M0` = the seat with no `ChannelPolicyFold`; `M-POL-2-NULL` = the fold constructed and disarmed; `W1-NULL` = `ArenaFold(armed=False)`). The script's arm map knows only `W1` / `M-POL-2` today (`kc2_v3p7_closure.py:339-340`), so it must be extended. (b) the same capture over the **`TA-X-29(e)` config-E static walk** (`load_profiles` under `P-5` + `we.pools_for(w, bonus_spawns_enabled=True)` + `offense.fold_at(w, to_hit=True, attack_speed=True)` + the `gmg` / measured-board resolver). Its call path is not the fight loop's. Non-graded; committed as its own artifact | **star-lord** | **Outcome 1:** zero NOT IN PACK on every class → the rows grade as written. **Outcome 2:** any NOT IN PACK → the pack is not closed for arms the graded rows run; ⚑ **the attempt MUST NOT fire.** The remedy is a v3.7.x cut, and since `P-4` would move, **a new dated prereg version committed ALONE**, never an edit here. **Not run → the attempt does not fire either.** *This version does not predict the result. Every run-internal EXACT row reads `M0`, `M-POL-2-NULL` or `W1-NULL` in at least one cell (§ B.1a). A union over `W1` and `M-POL-2` is evidence about those two arms only* |

**Not blocking, named so they are not lost:** v1.9 § H's list, carried · `C-o` · OQ-14 · OQ-15 · the
KP-139/KP-143 hole-number swap (routed at v1.9; the committed record governs: 15 = resist cap, 16 = attack
speed + OA adds).

---

## § I · OPEN QUESTIONS: one lean each

**OQ-1 … OQ-12 carry v1.9's dispositions.**

**OQ-13 · `TA-X-10` / `TA-X-11` under separation** → ⚑ **CLOSED by `H-9` outcome 1.** Nothing moved.

⚑ **OQ-14 · Loop-layer oracle config and `P-5`** → **OPEN, lean unchanged:** now that pass 2 has ported
them, derive for each (`deferred_arrival`, the K-MILL flags `seek_fold` / `kinematics`, energy income,
`simulate_wave`'s seed) whether it is a default-OFF setting the graded oracle ARMS. Any that is becomes a
`P-5` row in a later version. **v3.7's `d4` rowset (711 defaults observed in effect) is the obvious
instrument for that derivation**: a loop system whose switch appears there at a non-default value is the
`P-5` hazard. *Not folded here: this version pins the pack.*

⚑ **OQ-15 · `TA-X-26(b)` under a closed pack.** → **LEAN: widen (b) in a version that exists for that
purpose, to accept `IC7-F-44`'s declared `sha256 == P-i` as authenticated by `P-4`'s member digest, AND
require the port's parsed columns to equal the image's cells.** That would verify content and not only
provenance. **Until then (b) needs the file's bytes.** *The claim to attack: a digest quoted inside an
authenticated member is as strong as a digest recomputed. It is not, if the loader reads cells from a
different place than the one the digest names.*

⚑ **OQ-16 · `TA-X-18`'s exact reading.** → **LEAN: keep `exact` as float64 equality** (§ A.5). *The claim to
attack: that a row whose v1.1 value no build could meet was "exact" in name only, and that restoring an
attainable value restores the tolerance rather than tightening it.*

---

## § J · DISCIPLINES THIS VERSION EXERCISED

> ⚑ **A TEXT FIX IS A SUBSTRATE CHANGE IF A ROW WAS DERIVED FROM THE TEXT'S SILENCE.** V9-SITE-14's fix
> "only adds a key". But `TA-X-18`'s value was derived from an idealised `2π` because the wire never
> said otherwise. **Reading the five `t6` rows against the 28 found one expected value that the oracle
> had never produced**, and a grade of record that had quietly graded a looser reading than its text.

> ⚑ **"THE ORACLE DID NOT MOVE" IS NOW PROVEN ON ITS INPUTS, NOT ONLY ITS TREE.** v1.9 proved the engine
> tree identical. The oracle also reads seven files in another repository. v3.7's closure proof made that
> set enumerable, and v1.10 re-hashes all 62.

> ⚑ **A FIGURE WITHOUT ITS ARM IS A FIGURE WITHOUT ITS POPULATION.** Another instance of the run's
> standing shape (arithmetic right, population unstated): `[156, 152, 155, 152, 152]` was correct and
> belonged to one arm of five.

> **Carried:** Law 3 (no fitted constants; `TA-X-18` was read off the oracle, not chosen) · the `F.1a`
> expiry clause · the honest-`n` law · `#75` cl. 1(a) · KP-101 (every digest labelled FILE or ROWSET) ·
> **digests computed and filled by script, never typed.**

---

*Filed 2026-09-30 by **gamora** (simulation + spirit-guide seam), Run KC2-PLAY.
⚑ **v1.10 RE-PINS v1.9 FROM PACK v3.6.1 TO PACK v3.7** (KP-147, KP-148). **One expected value re-derived
from the oracle (`TA-X-18`, § A.5); none moved on the other 27 EXACT rows or the five preconditions.**
The oracle and all 62 inputs it consumes are byte-identical to v1.9's, and every oracle-derived value was
recomputed and reproduces. **The arm of every graded row is written down (§ B.1a); `TA-B-01` is
`M-POL-2`.** **Attempts: `0` of `2`, carried unspent.** The declared set is closed at exactly
`["TA-X-06"]`. **`H-9` discharged (PASS). `H-10` is new and owed by star-lord.** OQ-14 open. **NO BAND WIDTH
MINTED.** **K-7 held:** the sealed cells were hash-verified only. This file's derivations exercised the
oracle only through `load_profiles`, `build_mover` / `monster_run_speed`, the U-P-N-5 static walk and
`SpawnStructureFold.offset`. v1.9 and every earlier version are **NOT edited**.
⚑ **THIS FILE IS IMMUTABLE. Any change after a graded run exists against it is a HALT (`WARN-16`).**
**No production code. No dispatch. No push. D4 held: committed ALONE.***
