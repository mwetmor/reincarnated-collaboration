# KC2-PLAY · T-A PREREGISTRATION **v1.12**: R-11 RE-DERIVED FOR NEUMAIER SUMMATION (Matt Q92 (a)) AS A LAW OVER (n, Σ|term|); the measured values PENDING drax's `TA-X-07` booking fix (KP-167)

> ⚑ **STATUS: IMMUTABLE ON COMMIT. v1.12, authored 2026-10-01. SUPERSEDES v1.11 FORWARD.**
> *(The filename carries the series' `2026-09-20` prefix. The document is dated 2026-10-01.)*
>
> ⚑ **THE PACK DOES NOT MOVE.** v3.7.1, model PACK `48a4c94c165715d3f4f5db89c1278aa8439fbe1507c39dd555f7ce91d4636c96`, reference PACK `1887257f5370443a1729fde2ff446579b1acc501dcd03679244297b541e3e5b1`. Every pin was recomputed
> this session and reproduces v1.11. **The oracle did not move**: engine HEAD is `22cd2288`, v1.11's HEAD.
>
> ⚑ **R-11 / CLAUSE (c) OF `TA-X-07` IS RE-KEYED, BY MATT'S RULING (KP-155, Q92 (a)).** The port now sums all seven
> `TA-X-07` accumulators, both inner sums and the final six-way sum with Neumaier's compensated method. § F.2k derives
> the worst-case rounding bound of that method (Neumaier 1974; Higham § 4.3; the explicit constants of Ogita, Rump and
> Oishi 2005, Prop. 4.5) over **every** rounding between the booked terms and the graded number:
> * the seven accumulators;
> * the two inner sums;
> * the final six-way sum;
> * the split and formation roundings at the call sites;
> * the residual subtraction and the division.
>
> The bound is stated against each accumulator's **Σ|term|**, so negative `voided` terms are counted. **Clause (c) is
> now that law, evaluated per cell from emitted fields alone. It is no longer a term budget.** The 4,500-term budget,
> v1.11's recursive-summation bound and v1.11's code reading at `ffb454e` are **retired and carry nothing operative**
> (§ F.2k.0). **Clause (a)'s tolerance stays at 1e-12.** No expected value moves.
>
> ⚑ **THE CONDITION, IN ONE LINE (§ F.2k.5).** To first order the bound is ≤ 1e-12 relative iff a cell's weighted
> absolute-mass ratio `Λ ≤ 1e-12/u = 9,007.199`. Depth enters only at second order, below `10⁻⁶·u` for every
> accumulator up to 94,907 terms. On the reference case (all terms non-negative, every sink flagged) `Λ ≤ 5`, a margin of
> ×1,801.4. **That is a reference case, not a measurement.**
>
> ⚑ **NO MEASURED VALUE IS ENTERED, AND NO CONCLUSION HERE DEPENDS ON ONE (KP-167).** On drax's pass-3b runtime
> (godot `933b438`), the `TA-X-07` identity **leaks on 22 of 25 cells**. That is a booking defect, which drax is fixing now,
> and his fix changes the term counts. § F.2k.6 gives the per-cell table as a form, every value **PENDING**. The godot
> re-pin is **PENDING** too (jack-ryan item 9).
>
> ⚑ **ATTEMPTS: `0` OF `2` UNDER v1.12. THIS IS A CARRY, NOT A RESET.** No graded run exists under v1.11 (KP-167: *"No
> graded attempt run"*). The allowance (Matt KP-115, *"Reset to 2"*) has been carried unspent through v1.8 … v1.11. v1.7's
> attempt 1 stays on the record as spent.
>
> ⚑ **THE DECLARED SET IS CLOSED AT EXACTLY `["TA-X-06"]`** (Matt, Q83(b), KP-110). Carried.
>
> ⚑ **jack-ryan's v1.11 pre-read governs this version** (collab `607f3b23f`, FILE `b9fd065496d2def98814db9334038aa7f2b466969696d3517a98a0de6f5c89da`).
> Every "v1.12 must change" item (1–9) and every INFO item is folded in. § 0.6 maps each to its section.
>
> ⚑ **THIS FILE IS IMMUTABLE ONCE COMMITTED. ANY CHANGE AFTER A GRADED RUN EXISTS AGAINST IT IS A HALT TO MATT
> (`WARN-16`).**
>
> ⚑ **D4 HELD. This file is committed ALONE, with zero code, before any graded run against v3.7.1 exists.** Every
> digest in it was recomputed this session from the files. The new ones were filled into the document by script, and
> the same script asserted every carried digest equal to its recomputation. None was typed or copied from a ledger
> row. Each is labelled **FILE** (sha256 of one file's bytes), **ROWSET** (sha256 of a stated law applied to rows or a
> member list) or **PACK** (the manifest's pack law over its member rows), per KP-101. The one exception is labelled
> where it stands (`REPORTED`: drax's runtime-tree digest, which this file does not recompute).
>
> **Authority:**
> * ⚑ **KP-154**: v1.11 landed; the R-11 remedy is a re-sizing, so it was routed to Matt as Q92.
> * ⚑ **KP-155 (Matt, Q92):** *"(a) Compensated sum."* drax adds Neumaier on all seven accumulators and both inner sums,
>   and emits the per-accumulator term counts. gamora writes v1.12, with clause (c) re-derived for the compensated method
>   over ALL accumulators, the tolerance unchanged at 1e-12, and *"the budget restated only as the derivation gives
>   it."*
> * ⚑ **KP-158**: jack-ryan's H-7 pre-read of v1.11, PASS-WITH-WARN, with the v1.12 must-change list.
> * ⚑ **KP-167**: pass 3b landed (Neumaier live, matching `math.fsum` bit for bit; G3 at 0). **The identity leaks; it
>   is a booking defect.** *"gamora writes v1.12, with the Neumaier bound written as a LAW over (n, Σ|term|) per
>   accumulator and the measured values filled in after drax's fix."*
> * **Carried from v1.11 without change:** Q83(b), Q85, Q87, Q91, KP-115, KP-127, KP-131, KP-132, KP-137, KP-144,
>   KP-146, KP-149, KP-150 … KP-153, F5, jack-ryan's v1.8 pre-read (R-17 … R-22), the `C-o` ceiling.
>
> **Author:** gamora (simulation + spirit-guide seam), Run KC2-PLAY. **Decision rules only. NO BAND WIDTH IS MINTED,
> AND EVERY WIDTH IN `P-a` STAYS VOID.** **v1.11 (`312d71aaf3b5a15ca44a8179cbb46c35a50343e5bca23ab5201c73ec9c8278cc`) and every earlier version are NOT edited.**

---

## § 0 · ⚑ THE v1.11 → v1.12 DELTA

**Legend.**
* **CARRIED** means the assertion, expected value, tolerance and derivation are unchanged, and the substrate pins were recomputed and reproduce.
* **RE-KEYED** means a clause's antecedent is re-derived (here only `TA-X-07(c)`, by Matt's ruling).
* **OPERATIONAL** means the assertion and value are unchanged, and how the grader evaluates them is now written out.
* **NOTE** means the assertion and value are unchanged, and a population or wording fact is now stated.

### 0.1 · Preconditions

| id | v1.12 | Δ value | why |
|---|---|---|---|
| `P-1` coverage 89/89 | **CARRIED** | none | — |
| `P-2` stream disjointness | **CARRIED** (`M-POL-2`, salt 0, port only) | none | — |
| `P-3` roll population / law | **CARRIED** (POOL-466 recomputed: 466, set digest reproduces) | none | — |
| `P-4` pack identity | **CARRIED** (both PACKs and the cross-pin recomputed; reproduce v1.11) | none | the pack did not move |
| `P-5` oracle fold settings | **CARRIED: the same eleven.** ⚑ **NOTE (INFO-3):** `pet_special_gates` is **OMITTED** on `setup` row `IC7-A-0453` (default `None`) and **EXPLICIT `None`** on `WALK` row `IC7-A-0411`. The value is equal; § B.6 now states this, and the row governs | none | jack-ryan INFO-3 |

### 0.2 · EXACT rows (28) and the declared row

| id | v1.12 | Δ expected value | Δ tolerance | note |
|---|---|---|---|---|
| `TA-X-01` … `TA-X-06` | **CARRIED** | none | none | `TA-X-06` UNGRADEABLE-declared, closed |
| `TA-X-07` | ⚑ **RE-KEYED, clause (c) only** (§ F.2k). (a) relative ≤ 1e-12: **unchanged.** (b) reported: **unchanged.** (c) was a 4,500-term budget on `offered` alone and is now the Neumaier law (L2) over all seven accumulators, both inner sums, the six-way sum and the call-site roundings, evaluated per cell from emitted fields. ⚑ **Population: all 25 cells, carried from v1.11.** ⚑ **Not listed in v1.11 § 0 (WARN-5), so listed here:** v1.10's R-11 row was *"`M-POL-2` × salt 0 (v1.8 § F.2d's cell)"*, one smoke cell, and v1.11 made it *"every cell the graded run emits"*, 25 cells. That is stricter and correct, since clause (c) binds per cell. v1.12 keeps 25 | none | none ((a)'s 1e-12 unchanged) | **Discipline #12: a semantic shift, named.** Authority Matt Q92 (KP-155). Closes OQ-17 |
| `TA-X-08` | **CARRIED** | none | none | — |
| `TA-X-09` | **CARRIED.** ⚑ v1.11's *"nine graded vectors ROWSET `0e692765`"* is **STRUCK**: it is truncated, its law is unstated, and it is not reproducible (WARN-4). It is replaced by the full ROWSET with its law (§ A.2): `0e826ee093b98767901271c95e918a19e1c6d5b8a8663c99c87d8ced17086e78` | none | none | the five normative rules are named by id (§ A.2) |
| `TA-X-10` | **CARRIED** (`43.758085029822276`, `W1`) | none | none | — |
| `TA-X-11` | **CARRIED.** ⚑ **NOTE (INFO-2), population:** v1.10 and v1.11 grade `W1` **and** `W1-NULL` (10 cells), per the text *"every W1 arm"*. v1.7 attempt 1 graded `W1` only (5 cells). On `W1-NULL` the row is vacuous (`ArenaFold(armed=False)` emits `n_wall_clamps_*` = 0 by construction, `arena_fold.py:209-210, 442-443`) but gradeable, not `NODATA` | none | none | named under Discipline #12; no value moves |
| `TA-X-12` … `TA-X-17` | **CARRIED** | none | none | — |
| `TA-X-18` | **CARRIED VALUE** `(-3.999999999999985, -3.49691120014899e-07)`. ⚑ **OPERATIONAL (WARN-1):** "exact" means the emitted strings parse to float64 whose bit patterns equal `0xc00fffffffffffde`, `0xbe9777a5cf72cec6` (sign bit included, so ±0 are distinguished), from an emitter shown to be lossless. Otherwise the row is `UNGRADEABLE`, not green (§ F.2l) | none | none (it was always "exact") | closes OQ-16 (jack-ryan item 1: PASS, a correction, not a fit) |
| `TA-X-19` … `TA-X-28` | **CARRIED** | none | none | `TA-X-26(b)`: OQ-15's tripwire is now written (§ I) |
| `TA-X-29` | **CARRIED** | none | none | ⚑ The `Z5-LAW` gate that v1.6/v1.8 called "G3" (leech rows dropped) is **renamed `UPN5-G3`** wherever this file refers to it, so "G3" names only the loop-trace instrument (§ C.9; WARN-3) |
| `TA-X-30` | **CARRIED** | none | none | — |

**Per-row delta in expected value: NONE, on all 28 EXACT rows and the five preconditions. Tolerances changed: NONE.**
**Gradeability changed by declaration: NONE.** One antecedent was re-keyed (`TA-X-07(c)`) and one evaluation made operational
(`TA-X-18`). Both can only produce `UNGRADEABLE`, never green.

### 0.3 · Configuration, instruments, diagnostics, report face, verdict file

| site | v1.12 | why |
|---|---|---|
| § B.1a `setup` job | ⚑ **PARTITIONED BY ROW ID** into 8 configuration rows (ROWSET `207ab21f853b18ca026327bf6c9ddc4afa705d29cd3ef0868c1e7818d1672b4c`) and 19 tick-period-probe rows (ROWSET `ab3197727b59cc355f479862a297b33bef89e74e6d40dbff14762c701f2c7be0`). `IC7-A-0443`, `-0457` and `-0458` are probe rows and configure **no** arm. The harness obligation is stated for each | WARN-2 |
| § B.1a / § G | ⚑ **C1 conformance is tied to H-1's G3 evidence** at the graded digest. The `configured_from_a8: true` flag is self-attestation and does not discharge it | INFO-4 |
| § C.9 G3 | ⚑ **NEW: G3 DEFINED IN THIS FILE.** It gives the instrument and its pins, the scope of the oracle's draws, zero injections, the decision taxonomy, the draw and stream rules, and how death-wave and death-tick equality are read | WARN-3 |
| § E.2 | ⚑ **NEW CEILING `C-p`:** the port generator's realisation is graded by law, not by outcome | INFO-5 |
| § F.3a | ⚑ **NOTE added:** to the extent the ORACLE-config board is salt-independent, each side fights one board realisation | INFO-5 |
| `TA-B-01`, `TA-B-15`, `C-e/f/i/o` | **CARRIED** | — |
| § F.3 / § F.5 mandatory sentences | version label only | — |
| verdict file | `prereg_version: "v1.12"`. ⚑ `r11_budget` is **RETIRED** and replaced by `r11_bound` (§ G.3). ⚑ New: `ta_x_18` (bits, emitter), `g3` (per arm per salt) | § G.3 |
| § G.1 counter | **`0` of `2` under v1.12** (carried unspent) | — |

### 0.4 · The counts

| | preconditions | **EXACT** | UNGRADEABLE-declared | DIAGNOSTIC ids | emitted-not-graded |
|---|---:|---:|---:|---:|---:|
| v1.11 | 5 | 28 | 1 (`TA-X-06`), closed | 19 (0 gating) | 3 |
| **v1.12** | 5 | **28** | **1 (`TA-X-06`), closed** | 19 (0 gating) | 3 |

⚑ **Q87's *"all EXACT rows green"* at v1.12 means the same 28:** `TA-X-01 · 02 · 03 · 04 · 05 · 07 · 08 · 09 · 10 ·
11 · 12 · 13 · 14 · 15 · 16 · 17 · 18 · 19 · 20 · 21 · 22 · 24 · 25 · 26 · 27 · 28 · 29 · 30`. **No row added or
removed.** `TA-X-23` stays struck and retired.

### 0.5 · What v1.12 deliberately does NOT fold in

1. ⚑ **Any measured value from the pass-3b runtime** (godot `933b438`). The identity leaks there (KP-167), and the fix changes the
   counts. **No sentence of this file depends on those numbers.** The § F.2k.6 form is filled from the fixed runtime's
   emission, in the H-6 discharge note. This file is never edited (§ F.2k.6).
2. **The KP-144 (b) loop-layer systems as `P-5` settings** (OQ-14, open).
3. **A widening of `TA-X-26(b)`** (OQ-15, open; the tripwire is written in § I).
4. **`C-h` / `OQ-9`**, **`C-k` / `OQ-11`**, **C-11b and REFERENT-v2** (incl. KP-156 and KP-162's side findings): not here.
5. **A ruling on the port-generator salt-1 clear** (§ F.3a). It is a Gate-2 question; the diagnostic is printed only.

### 0.6 · jack-ryan's v1.11 pre-read (`607f3b23f`): where each item lands

| item | what it asked | v1.12 |
|---|---|---|
| must 1 | rewrite § F.2k and its dependants | § F.2k (all new); header; § 0.2; § 0.5 item 1; § F.2 `TA-X-07`; § G.1 R-11 bullet; § H H-6; § G.3 `r11_bound`; § J |
| must 1 / § 7.3 | Neumaier against Σ\|term\|; the six-way sum and the split roundings explicit; an antecedent computable from emitted fields; the fail-first probe | § F.2k.2–.5 (L0–L2); H-6 (d) |
| must 2 | close OQ-17 by the re-keying | § I, OQ-17 **CLOSED** |
| must 3 | `TA-X-18` operational; close OQ-16 | § F.2l; § I, OQ-16 **CLOSED** |
| must 4 | partition `setup` | § B.1a |
| must 5 | define G3; disambiguate the `Z5-LAW` G3 | § C.9; `UPN5-G3` |
| must 6 | the `TA-X-09` ROWSET in full with its law, or drop it | § A.2 (given in full) |
| must 7 | list R-11's population change in § 0 | § 0.2, `TA-X-07` |
| must 8 | re-pin godot at the compensated runtime | ⚑ **PENDING**: the graded runtime is the post-KP-167 fix. The `933b438` reading is pinned as READ, not as graded (PINS; § F.2k.1) |
| INFO-1 | no decisions-log entry owed | accepted |
| INFO-2 | `TA-X-11` population | § 0.2 |
| INFO-3 | `pet_special_gates` explicitness | § 0.1; § B.6 |
| INFO-4 | tie C1 to G3 | § B.1a; § G |
| INFO-5 | generator ceiling; one board realisation | § E.2 `C-p`; § F.3a |
| INFO-6 | OQ-15 tripwire | § I |
| INFO (wording) | § A.1's "Reference:" sentence | § A.1 corrigendum |
| ledger INFO | KP-153 "+881" | the conductor's (corrected at KP-158); not this file's |

---

## ⚑ PINS: EVERY PIN COMPUTED THIS SESSION, FILLED BY SCRIPT, NONE TYPED

> **The standing rule (KP-20, KP-43):** a new version recomputes every pin it carries, including the ones it
> believes are unchanged. **All carried pins reproduce v1.11 exactly.** Both pack digests are recomputed from the
> member files with the manifest's `pack_digest_law_exact`, every member's FILE digest and byte count checked
> against its manifest row, the on-disk member set checked equal to the manifest's (no extra file, none missing),
> and the result compared to the manifest's `pack_digest`. They agree.

| # | artifact | label | **sha256 (computed 2026-10-01)** | v1.11 → v1.12 |
|---|---|---|---|---|
| P-a | `gamora/notes/2026-09-20-kc2-play-ta-band-widths.md`. Constructions only; every width VOID | FILE | `1c80f08075a1ed0e30e30b348752d2505b39994f7e2c55c348413f6e591248f9` | unchanged (reproduces v1.11) |
| P-b | `galadriel/notes/2026-09-20-kc2-play-w1-tb-expected-values-and-u-rider.md` | FILE | `d48512aa6e3c9ea70de6675750880a6c8914f0984c3cfe65c6ccb9a24403438f` | unchanged (reproduces v1.11) |
| P-c | `…/2026-09-20-kc2-play-w1-tb-expected-values.json` | FILE | `a8b85331764ba3fe90f45cf7cd6f1a25f6dc0dae4a7e7fa555c487f0b153ea0b` | unchanged (reproduces v1.11) |
| P-d | `…/2026-09-20-kc2-play-w1-tb-release-labels.json` | FILE | `15dace604c8d5bb4888223a8b25a07a038bae44431ebd194d682545c0f29c58a` | unchanged (reproduces v1.11) |
| P-e | `simulation/math/kc2-play-v3p4-roster-basis-rebase-2026-09-21.md` (lineage) | FILE | `4b7b78c834c7fbabd61700dda3e730a95ab89990bfa01470e8fb293f41ac7a73` | unchanged (reproduces v1.11) |
| P-e′ | `…/math/kc2-play-v3p3-monster-offense-prereg-2026-09-20.md` (lineage) | FILE | `27fc59378aee8c9d412f486a63864a3b2ceb5c5473520b60ad80128d47d99cdc` | unchanged (reproduces v1.11) |
| P-h | ⚑ **THE MODEL PACK** `kc2-model-pack-v3-E-s09-cp150-mech-v3p7p1-20261001_021247` (19 members, 19/19 verified: digest and bytes) | PACK | `48a4c94c165715d3f4f5db89c1278aa8439fbe1507c39dd555f7ce91d4636c96` | unchanged (reproduces v1.11) |
| P-h2 | ⚑ **THE REFERENCE PACK** `kc2-reference-pack-v3-E-s09-cp150-mech-v3p7p1-20261001_021247` (7 members, 7/7 verified); `cross_pin.model_pack_digest` verified equal to the derived model digest | PACK | `1887257f5370443a1729fde2ff446579b1acc501dcd03679244297b541e3e5b1` | unchanged (reproduces v1.11) |
| P-i | `data/kc2/pm4p_leech_resistance.csv` (imaged as `IC7-F-44`, a column projection; v1.10 § A.4) | FILE | `cb6a008bde1e102573181968ab7f60958cd28fee07ff8736078fa092a80dd62e` | unchanged (reproduces v1.11) |
| P-j | `data/kc2/pm4l_mitigation_by_body.csv` (lineage) | FILE | `a8c1ffd97dc703419f8447f3d7bbba3903e0f14d2c2e6746a938ceefae9ecec6` | unchanged (reproduces v1.11) |
| P-k | `data/kc2/pm2_tg2_monster_timing.csv` (`ANCHOR-169`'s carrier) | FILE | `58205679e36f0e0361ccd41c844d6bc254ada034447dd1f80e2a46a2b47c7aca` | unchanged (reproduces v1.11) |
| P-l.c2 | `simulation/math/kc2-c2-per-cast-energy-cost-fold-2026-09-28.md` | FILE | `b42684e55325bd4caf705b1e7d43462acb5c5818cd5abe3d79eb0d3b9ba6f8c7` | unchanged (reproduces v1.11) |
| P-l.c7 | `…/kc2-c7-insufficient-energy-refuse-fold-2026-09-29.md` | FILE | `072f9ab787ec840a9bc62ae76a0576fa5db7be0da0b63457851557ea164a7e1f` | unchanged (reproduces v1.11) |
| P-l.nine | `…/kc2-play-nine-winner-surface-reconstruction-2026-09-29.md` | FILE | `2c7c3679af67569fff88bb56837ea1ba37499fe9fcbeca85ab63a473b0d7a6dd` | unchanged (reproduces v1.11) |
| P-l.upn4 | `…/kc2-play-upn4-occupancy-by-pilot-2026-09-29.md` | FILE | `787d1a99d9adfedbb34bda69a3c530a653a8df3fc117969e3920c5625791a3cf` | unchanged (reproduces v1.11) |
| P-l.upn5 | `…/kc2-play-upn5-global-magnitude-fold-lift-2026-09-29.md` | FILE | `bfa44b4722ec8b7326987042101f32310c986e3fae489a4372fcc4e0dd5553c7` | unchanged (reproduces v1.11) |
| P-l.upn5A | `…/kc2-play-upn5-global-magnitude-fold-lift-ADDENDUM-2026-09-29.md` | FILE | `5323c1fa9f156e80ced5b1324e4297150cfc759c4e54426f440c33a6c9745fc6` | unchanged (reproduces v1.11) |
| P-l.q91 | `…/kc2-play-q91-338-pool-damage-lift-2026-09-29.md` (governs `TA-X-25` and `P-5` setting 3) | FILE | `d68561d59723c3295da3f0456f2fbeaefe8f5f0a30b41d29b5ff0e366966a385` | unchanged (reproduces v1.11) |
| P-l.q91a | `…/kc2-play-q91-338-pool-damage-lift-ADDENDUM-2026-09-29.md` | FILE | `b9ada804e17c01b376e64e82b7e45f66a344d1fc2fc75a0fdd1fd76c56e2cddc` | unchanged (reproduces v1.11) |
| P-l.c11a | `…/kc2-play-c11a-oracle-corrections-fold-2026-09-30.md` (governs `P-5` setting 11) | FILE | `4af38999ff0544cc9607b34da4fde29fe2c55324e9829894c516cd9837689445` | unchanged (reproduces v1.11) |
| P-l.c11aA | `…/kc2-play-c11a-oracle-corrections-fold-ADDENDUM-2026-09-30.md` | FILE | `17a068fe980869e6e344fdf3a652dc275f5cc3a3d65818f2976fe94084d48666` | unchanged (reproduces v1.11) |
| P-n.1 | `simulation/output/kc2-play-q91-pool-lift-pricing-20260930_023137.json` (the `M-POL-2` seat) | FILE | `f33ce0c0cbeb00bbed7b47a6f7660f20d4aa2be1694f9f4e2486e37d27b553e2` | unchanged (reproduces v1.11) |
| P-n.2 | `simulation/output/kc2-lifted-rows-KC2PLAY-SEALLAP-W1-c2-energy-fold-20260928_232836.json` (the `x8` input; `a8` `IC7-A-0454` names this path) | FILE | `cc361a3fea3e24e55fdf0c8c8eaf52bcc0c729c7de0563d3c84dd0dc21202960` | unchanged (reproduces v1.11) |
| P-n.3 | `simulation/output/kc2-play-c11a-fold-pricing-NOT-A-GRADED-RUN-20260930_043045-SUMMARY.json` (`TA-B-01`'s reference: the `M-POL-2` seat; `C-f` / `C-i`) | FILE | `b6c9e7953f5b5632ec2dc51c2c8602461aef15d4721f69432444e6f777e1141e` | unchanged (reproduces v1.11) |
| P-n.4 | `simulation/output/kc2-play-c11a-landed-by-source-NOT-A-GRADED-RUN-20260930_033242.json` | FILE | `ad018b78a7f85491020a237166af797845bb5de2e562816673fbf925bb41ff1e` | unchanged (reproduces v1.11) |
| P-o | `data/kc2/c11a_aura_buff_grants.csv` (the C2 grant table; imaged as `IC7-F-04`) | FILE | `749d58f45eb312e7a284734a1844f2aabcfd69b7219dd1dafc55e4bb6d64792f` | unchanged (reproduces v1.11) |

### Set digests: the populations v1.12 grades over

**Law:** `sha256("\n".join(sorted(record_paths)).encode("utf-8"))`, no trailing newline. **ROWSET.** Recomputed this
session on the v3.7.1 tree: POOL-466 by both routes of `kc2_baton_v3p5p1_schema.pool466` (routes agree);
SWING-456 / NONSWING-10 as `ThreatProfile.can_swing` over POOL-466 from the oracle's `load_profiles` under
`P-5`'s exact loader call (the call `a8` `IC7-A-0453` records); FALLBACK-158 from `derive_oracle_speeds` (partition
180 / 158 / 128 = BANDA-DB-CITED / FALLBACK / LAPR-MEASURED, `march_base` 3.209466).

| set | n | label | sha256 | v1.11 → v1.12 |
|---|---:|---|---|---|
| **POOL-466** | 466 | ROWSET | `33c886a11f91db1143c791ffcf9d95f7e7614e423373235231733c994c5c157b` | reproduces v1.11 |
| **SWING-456** | 456 | ROWSET | `706a61d55dc6621814fc923d7428c5b263a95ebb00e9786d12f35dd385a7a4c0` | reproduces v1.11 |
| **NONSWING-10** | 10 | ROWSET | `00b4cb0e24b43e591a2e30200979725801aad1e7c1f9b7764ebef67461816e10` | reproduces v1.11 |
| **FALLBACK-158** | 158 | ROWSET | `e8114efaa8fa678db6a26bb6e4ffb926fc2c1a15a978e3d589cf918ff17ae6cb` | reproduces v1.11 |

### Documents of record

| document | label | sha256 |
|---|---|---|
| ⚑ prereg **v1.11** (superseded, **not edited**; v1.12's only predecessor; collab `f403c53c6`) | FILE | `312d71aaf3b5a15ca44a8179cbb46c35a50343e5bca23ab5201c73ec9c8278cc` |
| ⚑ jack-ryan's **v1.11 pre-read** (H-7 partial; collab `607f3b23f`; **governs this version**) | FILE | `b9fd065496d2def98814db9334038aa7f2b466969696d3517a98a0de6f5c89da` |
| prereg v1.10 (not edited; collab `690865868`) | FILE | `b1dd68efe2ce6009c2981d1c25bb182aba8c444945ec81f53a5c3c0c8b79061c` |
| prereg v1.9 (not edited; collab `d52193c72`) | FILE | `b787308c8c331e98fee6221c97174bf8f696a5b55d699611c5ab697625de95dd` |
| prereg v1.8 (not edited; collab `948bb8082`; § F.2d: R-11's law for both outcomes) | FILE | `69e1de1890a24fb9d9a4dc37cda6edfc39e6c34e45b877a2999b565b4710c49c` |
| prereg v1.7 (not edited) | FILE | `552d9faecd83d955c77f2be35991ec51e3908d9f586ab70b5a78b6c156b92896` |
| prereg v1.6 (not edited) | FILE | `db2c0ca3c6cdba022b83d0229439a3ad9e0709cd25732304ffc979a200be7b0e` |
| ⚑ prereg **v1.5** (not edited; § F.2d clause (c): where the retired 4,500 budget was derived; lineage only, § F.2k.0) | FILE | `efac4bd51f2d2c1f1130a58c85f37d1c7738e51ac15afd3c70930f7ac3eef143` |
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
| ⚑ **the port's conservation code, READ for § F.2k** at godot `933b438` (pass 3b, compensated; read through git objects only, nothing checked out or run). ⚑ **NOT the graded pin. The re-pin at the KP-167-fixed runtime is PENDING** (jack-ryan item 9). `kc2_runtime/sim/kc2rt_fight.gd` | FILE | `2277cc8940d2c50cde5d819545e4ffe5cfbc2207c8f38cfbfe85e37703190303` |
| ⚑ … `kc2_runtime/sim/kc2rt_laws.gd` (same status) | FILE | `c234376e9cbadc2d6f69549966112ec4fc1da7df46069831c7f1b80e3f581a9c` |
| ⚑ **the G3 instrument, READ for § C.9** at `933b438`: `kc2_runtime/tools/kc2rt_g3_oracle_trace.py` (the oracle side) | FILE | `49a044edf2ef2ccefd5987d00707835e5bf21c7ee6436792de60d65b10b1b7d9` |
| ⚑ … `kc2_runtime/tools/kc2rt_g3_loop_trace.gd` (the port side) | FILE | `574facb33a381939cf1254eacb0a82b202829e1d1cb772a3145b624094401d74` |
| lineage only, superseded: `kc2rt_fight.gd` at `ffb454e` (v1.11's reading) · at `fae29ec` (jack-ryan's pre-read) | FILE | `e6903095b6bba83f38359a654380cb5b13516c8e2a437b2a04ae1ff73c72a680` · `41310e5e5330b3e0e186090dcb4ffb91481da71bebc2b2a3a482e490d9d7c148` |
| lineage only: `kc2rt_laws.gd` at `ffb454e` (v1.11's reading) | FILE | `406ffeca427bf90bb6b998eba834138eb7f68b76917f95e70fabf72ba523e1b3` |
| the pass-3b runtime tree (`make_manifest.py`, 79 members) **as drax reports it** (godot `90a2c3c` `AGENT_STATE.md`; KP-167) | **REPORTED**, not recomputed here | `0a8311d0e96202aa0cdcaafd777c7f4ba02fdbd5786865063099aa930fed0139` |
| ⚑ **the GRADED runtime (post-KP-167 fix):** runtime tree · `kc2rt_fight.gd` · `kc2rt_laws.gd` · the G3 instrument · the booking census (§ F.2k.4) | FILE | ⚑ **PENDING** (H-6 (a)) |

### Sealed cells: hash-verified only. K-7 held (never opened for execution, never re-run)

| cell | path (`reincarnated-engine/src/reincarnated/simulation/output/`) | label | sha256 | bytes |
|---|---|---|---|---:|
| `[M-POL2]` | `kc2-checkpoint-E-s09-cp150-mpol2-20260825_114420.json` | FILE | `ad61ad2a8c799d6ef11a68436756c253f0a34fbb1052e575cdf9f9cd3a44dc5c` | 123,564 |
| `[MECH]` | `kc2-checkpoint-E-s09-cp150-mech-20260816_124031.json` | FILE | `20b05cb4ef3bd888b998cbc46c68b41a8051111c12fbcf2066d101b0a4b15f4b` | 2,125,271 |
| `[W1W]` | `kc2-checkpoint-E-s09-cp150-w1walls-20260825_220058.json` | FILE | `7a992c81ca6e56e54a53534b438a9ddf87ed42f1bf1a3d0ecc2d2f3c3db7881b` | 403,084 |


---

## § A · THE PACK DID NOT MOVE: v1.11 § A IS CARRIED, WITH ONE CORRIGENDUM AND ONE STRUCK PIN

**v1.11 § A.1 – § A.4 are carried BY REFERENCE** (v1.11 pinned above): the v3.7 → v3.7.1 member diff, the six new
rowsets, the four withdrawn rows read against every graded row, and the new rowsets read against every graded row.
jack-ryan's pre-read verified every claim in them (findings, "Pins re-derived"). This session recomputed every
digest they carry, and each reproduces. Nothing in them moves at v1.12.

### A.1 · Corrigendum to v1.11 § A.1's wording (INFO, jack-ryan)

v1.11 § A.1's *"Reference: 6 of 7 byte-identical; 1 moved: `reference/meta.json` …"* went on to list eleven files
(`waves.json`, `arena.json`, …, `config_of_record.json`) as byte-identical, inside the reference sentence. **Those
eleven are MODEL members** (model/ rows 2, 3, 4, 7, 9–13, 16 and 19 of § B.5), not reference members. The reference
pack's seven members are listed in § B.5. No digest or count changes; the sentence was mis-scoped.

### A.2 · ⚑ Recomputed this session (the oracle is unchanged at engine HEAD `22cd2288`, v1.11's HEAD)

* **The four set digests reproduce** (POOL-466, SWING-456, NONSWING-10, FALLBACK-158; same instruments and loader
  call as v1.11; partition 180 / 158 / 128, `march_base` 3.209466).
* ⚑ **`TA-X-18`** on the oracle's own `SpawnStructureFold(scatter=POLAR_UNIFORM_RHO, rng_repr=CONTINUOUS).offset`
  with a stream returning 0.5 twice: **`(-3.999999999999985, -3.49691120014899e-07)`**. Bit patterns: **`0xc00fffffffffffde`** · **`0xbe9777a5cf72cec6`**
  (hex-float `-0x1.fffffffffffdep+1` · `-0x1.777a5cf72cec6p-22`). Identical to v1.10's and v1.11's value.
* ⚑ **`TA-X-09`, THE NINE-VECTOR ROWSET IN FULL, WITH ITS LAW (WARN-4).** v1.11's `0e692765` is **STRUCK**. It was
  truncated, its law was unstated, and jack-ryan found no serialisation among 192 that yields it. The replacement:
  * **Rows:** the `test_vectors` of the **five** rules `RULE-CHANNEL-MOVEMENT` (2) · `RULE-RELEASE-TYPE-A` (2) ·
    `RULE-RELEASE-TYPE-B` (1) · `RULE-CAST-INTERRUPT-BINDING-EXCLUSIVITY` (2) · `RULE-DMG-APPLIED` (2) of
    `model/math_rules.json :: rules` (FILE `3b1e2d014411cb314d5cbf42ea40773dbcfa3de242f13d3a1d31eb830643b62d`), concatenated as one list **in file order** (the rules
    in `rules` order, then each rule's vectors in order): **9 objects**.
  * **Law:** the pack's ROWSET law, `sha256(json.dumps(list, sort_keys=True, separators=(",",":"), default=str))`
    (`ensure_ascii` at its default).
  * **ROWSET `0e826ee093b98767901271c95e918a19e1c6d5b8a8663c99c87d8ced17086e78`.** This equals jack-ryan's independent `0e826ee0…`.
  * ⚑ **Scope, stated (not changed):** `math_rules.json` now carries a **sixth** normative rule,
    `RULE-MONSTER-TO-PLAYER-MITIGATION-ORDER` (20 vectors, minted later). `TA-X-09`'s statistic has always been the
    five rules' nine vectors, and it stays so. The sixth is outside `TA-X-09`. Folding it in would be a row change
    (KP-137), and v1.12 makes none.
* **`TA-X-10`, `TA-X-26(e)`, `TA-X-29(e)` and `TA-B-01`'s reference:** carried from v1.11, which recomputed them on this
  same oracle tree. The tree is the same git object at the same HEAD. No input moved, so they were not re-run.

---

## § B · CONFIGURATION AND PRECONDITIONS: five

### B.1 · `ORACLE` *(carried from v1.10 § B.1)*

`V0`, five arms (`M0`, `M-POL-2`, `M-POL-2-NULL`, `W1`, `W1-NULL`), five salts, **25 headless runs**, the limbs of
record, `v_ref` 4.0 → 5.4 m/s, motion law `V0-04`, declared fight scope waves 151–160, leg A (stop at the player's
first death). **Pilot:** U-P-N-4's `SEALED-KMILL` (`DRIVE_TO_PACK`, `seek_fold=True`, `kinematics=True`). The
runtime prints its resolved limb set (`v0_limb_set`), diffs it against `V0` before any row is read (V0-37 =
`MotionLimb.GATE_FIRST (L-B)`), and refuses to boot on an unset limb. ⚑ **Since v1.11 every one of these settings is
also on the wire as `a8` rows** (§ B.1a), and the pilot rows are cited there per arm.

### ⚑ B.1a · THE ARM OF RECORD, PER GRADED ROW, AND THE `a8` ROWS THAT DEFINE EACH ARM

**The arm question is carried from v1.11 § B.1a (and v1.10) unchanged in substance** (`TA-B-01` = `M-POL-2`, on v1.10's four
grounds). **What v1.11 added, carried: the arms are not defined by this file's prose. They are defined by the pack.**
Each arm is the `a8` job of the same name, plus **the configuration part of** the shared `setup` job (⚑ v1.12: the `setup` partition below). This file cites those rows; it does not
restate them. **A harness that configures an arm from anything other than its `a8` rows is not running that arm**, and the evidence that it does is G3 (§ C.9), not a flag.

**ROWSET law for one arm's rows:** the pack's law applied to that job's `a8` rows as a list ordered by `id`:
`sha256(json.dumps([rows of job J, sorted by id], sort_keys=True, separators=(",",":"), default=str))`.

| arm (`a8` job) | `a8` rows | n | ROWSET (job rows) | the rows that DISTINGUISH the arm (read off the pack by script; each assertion was checked) |
|---|---|---:|---|---|
| **`setup`** (shared by every fight arm) | `IC7-A-0433`…`0459` | 27 | `c01d1ddaa4a5b7074203662522276a24a150312d9faeceb6634dc5438e0f71f1` | `P-5`'s loader: `threat.load_profiles` **`IC7-A-0453`** (`dot_corrections=True`, `c11a` scope CLASS, `pool_lift`, `winner_surface`; `pet_special_gates` = None), `C11aLoader(scope=CLASS)` `IC7-A-0435`, `WinnerSurfaceFold.from_x8(P-n.2)` `IC7-A-0454`, `pool_lift.load` `IC7-A-0446`; ⚑ the tick-period probe (`IC7-A-0457`, `0458` and 17 constructions) configures **no** arm: the partition below |
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

⚑ **THE `setup` JOB, PARTITIONED BY ROW ID (WARN-2).** The job's own scope reads *"make_runner + the tick-period probe
(shared by every fight arm)"*. The pack does not mark rows individually, so a harness that applied "setup + arm rows"
literally would apply the probe's `policy=None` / `kinematics=None` / `seat=False` to every arm. **The partition rule
is read off the pack, not chosen:**
* a `setup` row whose callee has **no** counterpart in the fight arms' own rows is **shared configuration**;
* a `setup` row whose callee **also appears in every one of the five fight jobs** is the probe's own instance. Each
  arm carries its own copy of that construction.

The rule was applied by script over all 27 rows. Both ROWSETs below use the § B.1a law over the listed rows, ordered by `id`:

| part | rows | n | ROWSET | harness obligation |
|---|---|---:|---|---|
| **C · shared configuration** | `IC7-A-0435` (`C11aLoader(scope=CLASS)`) · `0439` (`defenses.load_defences`) · `0446` (`pool_lift.load`) · `0452` (`threat.load_pet_contracts`) · `0453` (`threat.load_profiles`, `P-5`'s loader) · `0454` (`WinnerSurfaceFold.from_x8(P-n.2)`) · `0455` (`load_volley_population`) · `0459` (`make_runner`) | 8 | `207ab21f853b18ca026327bf6c9ddc4afa705d29cd3ef0868c1e7818d1672b4c` | **Apply once, shared by all five fight arms**, with every argument's explicit/omitted flag as recorded. (`WALK` carries its own copies of four of them, `IC7-A-0379` · `0410` · `0411` · `0422`, and is configured from those.) |
| **T · the tick-period probe** | `IC7-A-0433` · `0434` · `0436` · `0437` · `0438` · `0440` · `0441` · `0442` · ⚑ **`0443`** (`KinematicsFold(seed_salt=0, px_arm_label="PX-LO")`) · `0444` · `0445` · `0447` · `0448` · `0449` · `0450` · `0451` · `0456` (`replay`) · ⚑ **`0457`** (`_overrides(policy=None, kinematics=None, seek_fold=True)`) · ⚑ **`0458`** (`run_cell(salt=0, seat=False, arena omitted)`) | 19 | `ab3197727b59cc355f479862a297b33bef89e74e6d40dbff14762c701f2c7be0` | ⚑ **Configure NO arm from these rows.** None of their arguments reaches a graded cell. The harness need not run the probe: every arm's `run_cell` rows pass `period_s` **explicitly** (`0.0816326530612245`, e.g. `IC7-A-0148`), so no arm reads the probe's output. If the harness runs it anyway, the probe run is **not a graded cell** and is not emitted as one. `px_arm_label` is read off the arms' own fifty `KinematicsFold` rows, never off `0443` |

The two parts sum to 27, the ROWSET `c01d1ddaa4a5b7074203662522276a24a150312d9faeceb6634dc5438e0f71f1` of the whole job reproduces § B.1a's, and C ∩ T = ∅ (checked by
script). drax's `023790b` excludes `0457`/`0458` structurally, and the px label is read off the arms' fifty rows. This
file states the rule that governs, and that rule covers all nineteen probe rows, not two.

⚑ **C1 CONFORMANCE IS EVIDENCED BY G3, NOT BY A FLAG (INFO-4).** `arm_config_a8.configured_from_a8: true` and a printed
ROWSET prove the harness **had** the rows, not that it **used** them. **The evidence that an arm is configured from
its `a8` rows is H-1's G3 PASS (§ C.9) on that arm, at the graded runtime digest.** A port arm configured otherwise
diverges from the oracle's arm on the oracle's own draws. An arm without a G3 PASS at the graded digest is
**non-conforming (C1)**, whatever its flag says.

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
| `TA-X-11` | `W1` and `W1-NULL` × 0–4 (10 cells; vacuous on `W1-NULL`, § 0.2 NOTE) | `setup` + `W1`, `W1-NULL` |
| `TA-X-25` | per arm per salt, all 25 cells | `setup` + all five arms |
| `TA-X-27` | (a) scan · (b) per-seed replay · **(c) all 25 cells** · (d) pack census | (c): `setup` + all five arms |
| `TA-X-29` | (a)–(d) loader and pack; **(e) the static config-E walk** | (e): `WALK` |
| **`TA-B-01`** (DIAGNOSTIC) | **`M-POL-2` × 0–4** | `setup` + `M-POL-2` |
| `TA-B-15` (DIAGNOSTIC) | per arm per salt | `setup` + all five arms |
| R-11 = `TA-X-07(c)` (`H-6`, § F.2k (L2)) | ⚑ **every cell the graded run emits, all 25** (clause (c) binds per cell; since v1.11. v1.10 had one smoke cell, § 0.2) | `setup` + all five arms |

⚑ **The oracle reference figures, by arm.** Read by script off star-lord's instrument-free v3.7.1 POST runs
(FILE digests in the documents of record; `P-5`, salts 0–4, leg A, composed from `a8`). They reproduce v1.10's
figures for `M-POL-2`, `W1-NULL` and `W1`, to the second.

| arm | oracle terminal waves (leg A), salts 0–4 | seconds into terminal wave | status in this file |
|---|---|---|---|
| `M-POL-2` | **`[156, 152, 155, 152, 152]`** | `[7.184, 4.408, 7.02, 7.184, 6.122]` | `TA-B-01`'s reference (carried) |
| `W1-NULL` | `[156, 152, 155, 152, 152]` (≡ `M-POL-2`, `TA-X-04`) | `[7.184, 4.408, 7.02, 7.184, 6.122]` | carried |
| `W1` | `[156, 152, 155, 152, 155]` | `[6.286, 4.408, 7.02, 7.184, 6.939]` | printed beside `TA-X-06` (carried) |
| ⚑ `M0` | `[155, 151, 156, 155, 155]` | `[7.347, 13.143, 7.347, 6.449, 5.143]` | ⚑ **measured at v1.11. Information only: no row grades it, and it gates nothing** |
| ⚑ `M-POL-2-NULL` | `[155, 151, 156, 155, 155]` (≡ `M0`, `TA-X-03`'s relation) | `[7.347, 13.143, 7.347, 6.449, 5.143]` | ⚑ **information only** |

### B.2 – B.4 · `P-1`, `P-2`, `P-3` *(carried from v1.11 / v1.10 by reference; P-3: POOL-466 = 466, set digest reproduces)*

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

### B.6 · `P-5` · THE ORACLE FOLD SETTINGS: ELEVEN *(carried from v1.11 § B.6, unchanged; one explicitness fact stated)*

The same eleven settings, values, sources and line numbers; the oracle tree is unchanged (§ A.2). The loader call is
`a8` row **`IC7-A-0453`**, with its constructors `IC7-A-0435`, `IC7-A-0454` and `IC7-A-0446` (all in § B.1a's configuration
part C). ⚑ **Explicitness, stated (INFO-3):** on `IC7-A-0453` the argument `pet_special_gates` is **OMITTED** (it takes its
default, `None`); `dot_corrections`, `c11a`, `pool_lift` and `winner_surface` are explicit. On the `WALK` loader row
`IC7-A-0411`, `pet_special_gates` is **EXPLICIT `None`**. The value is the same on both rows, so nothing behavioural follows.
**The row governs**, and the harness reproduces each row's flag as recorded: omitted on `0453`, explicit on `0411`. v1.11's
prose wrote `pet_special_gates=None` as if explicit, and its "they agree (checked by script)" did not check this argument.
This session's script checked all five arguments' values **and** flags on both rows.

---

## § C · THE LAWS

**C.1–C.6 and C.8: carried BY REFERENCE from v1.11 § C** (which carries v1.10 / v1.9 / v1.8 § C). **C.9 (G3) is new.**

### C.7 · THE EPOCH LAW, EXTENDED TO v3.7.1

> ⚑ **A v3.3, v3.4.2, v3.6, v3.6.1, v3.7 and v3.7.1 PORT board are pairwise NOT draw-comparable at a fixed salt.
> No row, diagnostic or report line may compare across them.**

**Why v3.7 → v3.7.1 is declared non-comparable, although v3.7.1 is nearly additive:** pass 3b re-points the
loader (arms from `a8`, the four withdrawn rows dropped, the control-gate seed on the wire, the `r9` defaults
explicit). Whether any of that moves the port's stream is a property of the runtime, not of the pack, and this
file does not predict it. ⚑ **The ORACLE is the same object at every one of these epochs** (§ A.2).
**`substrate_epoch = "v3.7.1 / model 48a4c94c… / reference 1887257f…"`** for everything graded under this document.

### ⚑ C.9 · G3: THE LOOP-TRACE DIFF ON THE ORACLE'S OWN DRAWS, DEFINED HERE (WARN-3)

**Why it is defined in this file now.** Since the KP-152 corrigendum (§ G.1), G3 is the **only** fidelity
precondition on the port's decisions. Until v1.11 it lived in ledger KP-144 and in drax's tool header. A firing
condition belongs in the committed record (Principle #4).

**Name.** In this file **"G3" means only this instrument.** The `Z5-LAW` gate that v1.6 § F.2h(b) and v1.8 § F.2h(b) /
§ A.4 called "G3" (it sits in `TA-X-29(b)`; jack-ryan's finding cites it as "§ F.2a(b)", and the row is § F.2h's) (*"leech rows DROPPED by G3"*, from the U-P-N-5 math note `P-l.upn5`, its gate table row G3, *"leech
off the health path"*) is **`UPN5-G3`** wherever this file refers to it. Its content is unchanged, and those
earlier versions are not edited.

**C.9.1 · The instrument.** Two programs, read at godot `933b438` (FILE pins in the documents of record; ⚑ **the re-pin at
the graded digest is PENDING, H-6 (a)**):
* **Oracle side, `kc2_runtime/tools/kc2rt_g3_oracle_trace.py`** (read-only on the engine). It runs the oracle's
  PW-FOLDED cell on one salt and records, per stream, **every `random.Random` draw**. A stream is named `<construction
  site>|<seed>` (the seed in the port's signed 64-bit view), and each draw is stamped `(wave, k)` with k the
  wave-local tick (`k = run_tick − tick_start`). Per wave it records the actors (record, spawn xy, point), the
  per-tick player track, energy, channel verdict and HP, the oracle's own `ring_ledger` live body rows, the pet rows
  and the event rows. Every hook forwards to the oracle's own function, and no oracle expression is replaced.
* **Port side, `kc2_runtime/tools/kc2rt_g3_loop_trace.gd`.** It hands each port stream (`Kc2RtRng.fork_stream`, V9-LAW-1)
  a **scripted generator that serves the oracle's recorded draws for the same stream** (matched by construction site
  and seed), in order. It then runs the port's own fight code and compares.

**C.9.2 · What "the oracle's draws" covers.** **Every draw the oracle makes on the cell, on every stream it opens, and
nothing else.** The board is **not** handed over. The port's own board code builds it from the served draws, and the
comparison checks the result. The port's own generator (its PRNG algorithm and seeding) is **not** exercised: that
is `C-p` (§ E.2).

**C.9.3 · Zero injections.** The run reports `injected: []`. None of the instrument's isolation switches (`board`,
`pilot`, `alert`, `kvec`, `control`, `summons`, `wavestart`, `banner`) is set. A run with any injection is a diagnostic,
not G3.

**C.9.4 · The decision taxonomy (exact; each count must be 0).** Per arm, per salt, per wave, per wave-local tick, the
instrument's decision classes are:
`board` (records or presence differ) · `alive_set` (at the motion phase) · `pet_set` · `channel` (the channel verdict)
· `drive_target` (the DrivePolicy anchor) · `dmg_sources` (which sources landed on the player this tick) ·
`wave_end` (the port's last wave-local tick ≠ the oracle's `tick_end − tick_start`) · `wave_length` (the port's wave
ended before an oracle tick).
**Draw rules, also exact:**
* (i) **draw mismatches = 0** on every shared stream: a draw asked in a different kind, with different arguments, or
  past the end of the oracle's stream;
* (ii) **no port stream without an oracle counterpart**;
* (iii) **no oracle stream with draws in the traced waves that the port never opened**, except the two declared
  oracle-only streams accepted at pass 3 (KP-152; godot `AGENT_STATE.md` at `90a2c3c`, the pass-3 section):
  `spawn_structure.py:344|0` (the spawn FACING, V9-SITE-16, which no consumer reads) and `player_kit_residual.py:286|…`
  (the Fighting Spirit / Ulzaad rolls, outcome-inert). Any third oracle-only stream is a divergence.

**NUMBERS** (`player_xy`, `body_xy`, `board_xy`, `drive_xy`, `body_hp`, `player_hp`, `energy`, and the `bits_*` lines)
are printed with their tolerances and are **never a pass or a fail by themselves**.

**C.9.5 · Death wave and death tick.** On each (arm, salt):
* the port's terminal wave equals the oracle's;
* on that wave, `wave_end` is 0, so the port's death tick k equals the oracle's `tick_end − tick_start`, with the
  outcome `death` on both sides;
* the printout gives the port's `(wave, run_tick)` beside the oracle's `(wave, seconds into wave)`. The seconds are
  `k × period_s` (`period_s = 1/12.25`).

**C.9.6 · Population, and the oracle side's arm.** **All five arms × five salts** (H-1). The oracle trace of an arm must
be **that arm as `a8` composes it**. The check is that the trace's terminal `(wave, seconds)` per salt equal star-lord's
instrument-free v3.7.1 POST figures for that arm (§ B.1a oracle table, FILE pins in the documents of record).
⚑ **Stated, because it bounds what has been shown so far:** at `933b438` the oracle-trace tool builds the `M-POL-2` seat and,
with its `W1` flag, the `W1` arm. Pass 3b's G3 record covers those **two** arms. **`M0`, `M-POL-2-NULL` and
`W1-NULL` have no G3 record.** The oracle-level identities (`M-POL-2-NULL` ≡ `M0`, `W1-NULL` ≡ `M-POL-2`, bitwise on all
five salts per jack-ryan's sink digests) are facts about the oracle, not about the port. **H-1 owes all five.**

**C.9.7 · G3 PASSES on (arm, salt) iff** C.9.3 holds, every count in C.9.4 is 0 on every traced wave, and C.9.5 holds. It is
evaluated at the graded runtime digest. **G3 is an attempt precondition (§ G.1) and the C1 evidence (§ B.1a). It is
not a graded row.**

---

## § E · OUTSIDE T-A'S REACH

**E.1 (the traps, 1–12) and E.2 (the declared ceilings, `C-o` included, with its boundary at `TA-X-18`): carried from
v1.11 as written,** including v1.11's addition to trap 12's family: a conservation identity whose residual is small has
shown that its accumulation error was small *on that run*. It has not shown that the tolerance was sized for the
accumulation. At v1.12 § F.2k (L2) makes the second statement, and only the second is what clause (c) exists for.

⚑ **E.2, ONE NEW DECLARED CEILING (INFO-5):**

> **`C-p` · THE PORT GENERATOR'S REALISATION IS GRADED BY LAW, NOT BY OUTCOME.** The graded run executes on the port's
> own generator. G3 (§ C.9) compares the port's **logic** on the **oracle's** draws. After the KP-152 corrigendum,
> nothing before firing compares the outcomes of the port generator to the oracle's. What is graded about the generator
> is its **law**: `P-2` (stream disjointness), `TA-X-27(c)` (consumption equals the oracle's, none where the oracle
> takes none), and the structure rows `TA-X-15` / `16` / `17` / `25`. **`TA-B-01` and § F.3a remain non-evidential.**
> A v1.12 `PASS` does not cover the generator's realisation, and must not be read as covering it.

---

## § F · THE GRADED ROWS

**§ F.1, § F.2a–§ F.2j are carried BY REFERENCE from v1.11 / v1.10 / v1.9 / v1.8** (pinned above). ⚑ Where v1.6 / v1.8 § F.2h(b) say "G3" (leech rows dropped), read **`UPN5-G3`** (§ C.9), unchanged in assertion,
class, tolerance and expected value. The notes of § 0.2, of v1.11 § A.3 / § A.4, and the arms of § B.1a apply to them.

### F.2 · EXACT rows: 28, plus `TA-X-06` UNGRADEABLE-declared (closed)

| id | statistic | basis | tolerance | arm(s) (§ B.1a, `a8`) | v1.12 |
|---|---|---|---|---|---|
| `TA-X-01` | port self-determinism; arm+salt NAMED, ≠ `P-2`'s | run-internal | byte-exact | one named | CARRIED |
| `TA-X-02` | coverage 89/89, zero unmapped | census | integer | — | CARRIED |
| `TA-X-03` | `port(M-POL-2-NULL, s) ≡ port(M0, s)`, all 5 | `[M-POL2]` | byte-exact | M-POL-2-NULL, M0 | CARRIED IN FORM |
| `TA-X-04` | `port(W1-NULL, s) ≡ port(M-POL-2, s)`, all 5 | `[W1W]` | byte-exact | W1-NULL, M-POL-2 | CARRIED IN FORM |
| `TA-X-05` | `port(M-POL-2, s) ≢ port(M0, s)`, ≥ 1 salt | `[M-POL2]` | exact, one-sided | M-POL-2, M0 | CARRIED IN FORM |
| `TA-X-06` | `port(W1, s) ≢ port(M-POL-2, s)` | `[W1W]` | **EMITTED AND PRINTED, NOT GRADED** | W1, M-POL-2 | **UNGRADEABLE-declared, closed at exactly `["TA-X-06"]`** |
| `TA-X-07` | `offered = applied + dropped + voided + pool_truncated + pcl_reclaim + counterplay_absorbed` | run-internal | (a) relative ≤ 1e-12 (**unchanged**); (b) reported; ⚑ **(c) = § F.2k (L2), the Neumaier law over `(n, Σ\|term\|)` of all accumulators, per cell; else UNGRADEABLE** | all 25 | ⚑ **RE-KEYED (c)** (Matt Q92, KP-155); (a)/(b) CARRIED |
| `TA-X-08` | denominator identity, both sub-identities | `[M-POL2]` 5/5 | exact | all 25 | CARRIED |
| `TA-X-09` | all **9** `math_rules.test_vectors` of the five normative rules | `P-4`'s `math_rules.json` (FILE `3b1e2d014411cb314d5cbf42ea40773dbcfa3de242f13d3a1d31eb830643b62d`) | per-vector | — | CARRIED; the nine vectors' ROWSET `0e826ee093b98767901271c95e918a19e1c6d5b8a8663c99c87d8ced17086e78` (§ A.2; v1.11's `0e692765` struck) |
| `TA-X-10` | `max_body_radius_m ≤ 43.758085029822276` (W1), roster movers | `[W1W]` · `arena.json` | exact, ≤ | W1 | CARRIED (`H-9` PASS) |
| `TA-X-11` | `n_wall_clamps_{player,body} == 0`, every W1 arm | `[W1W]` | integer | W1, W1-NULL | CARRIED (`H-9` PASS); NOTE: 10 cells, vacuous on `W1-NULL` |
| `TA-X-12` | pool inertness under ORACLE: total pool damage `== 0.0` | `[W1W]` · `DIV-19` | exact | all 25 | CARRIED |
| `TA-X-13` | no player crit | `V0 · CritLimb LO` | integer | all 25 | CARRIED |
| `TA-X-14` | the two DO-NOTs; a REFUSED cast is not a release | `math_rules` prohibitions | integer | all 25 | CARRIED |
| `TA-X-15` | (a) p01–p04 at `t = 0.0`, p05 one burst at `t = 4.000 s` (tick 49); (b) no intra-point stagger | census `M4` / `V11` | exact | all 25 / — | CARRIED |
| `TA-X-16` | p06 OFF: `n_pool_picks == 47`, `n_spawn_point_6_keys_rolled == 0`, a filtered-keys counter | `waves.json` | integer | all 25 | CARRIED |
| `TA-X-17` | `‖spawn_xy − anchor_xy‖ ≤ 8.0` m, every roster placement | `placement_extents_m` | exact, ≤ | all 25 | CARRIED |
| `TA-X-18` | `u₁ = u₂ = 0.5` → **`(-3.999999999999985, -3.49691120014899e-07)`** | the oracle's `SpawnStructureFold.offset` · V9-SITE-14 | exact: ⚑ **bit equality per component, sign of zero included, from a lossless emitter; else UNGRADEABLE** (§ F.2l) | — | CARRIED value (v1.10 § A.5); ⚑ OPERATIONAL |
| `TA-X-19` | arrival unconditionality; no damage predicate reads an arrival's `px, py` | `deferred_arrival.py:13-17` | integer | all 25 | CARRIED |
| `TA-X-20` | 2.99 m hit / 3.01 m miss; no angular gate; no target cap | census `D7` | exact | — | CARRIED |
| `TA-X-21` | quantisation rule per site + zero bare `round(` on the port's threat path | four modules | exact | — | CARRIED; re-verify the live site list at emission |
| `TA-X-22` | `cause == "interrupts_channel_flag"` is 0 under ORACLE | `V0`; V18+V19 | integer | all 25 | CARRIED |
| ~~`TA-X-23`~~ | ~~board-roll composition~~ | struck at v1.2, retired | — | — | — |
| `TA-X-24` | attack phase is `ENGAGE`; `sha256(actor_id) mod n` never evaluated | `V0` | exact | all 25 | CARRIED; NOTE `r9` |
| `TA-X-25` | the spawn partition, four clauses (v1.8 § F.2f) | P-l.q91 + `u5` + the oracle's profile predicate | integer identity | per arm per salt | CARRIED |
| `TA-X-26` | declared-join conformance, five clauses (v1.8 § F.2a) | `P-i` | integer / exact / declared-precision | — | CARRIED; (b): hash the loaded file |
| `TA-X-27` | degenerate-draw consumption, four clauses (v1.8 § F.2b) | `P-4` | integer / byte-exact | (c) all 25 | CARRIED; NOTE `CONTROL_GATE_RNG_SALT` (v1.11 § A.4) |
| `TA-X-28` | leech target law, three clauses | § F.2g | integer / structural | all 25 | CARRIED; NOTE `r9` |
| `TA-X-29` | global-magnitude fold conformance, five clauses; (e) `3.207764` / `4.980316` + 39 per-record ratios | § F.2h | integer / declared-precision | (e) `WALK` | CARRIED |
| `TA-X-30` | the pursuit halt, two clauses | § F.2i | exact / integer | all 25 | CARRIED |

### ⚑ F.2k · R-11 RE-DERIVED FOR THE COMPENSATED METHOD (KP-155, Matt Q92 (a)). CLAUSE (c) IS A LAW OVER (n, Σ|term|), NOT A TERM BUDGET. THE MEASURED VALUES ARE PENDING (KP-167)

> ⚑ **jack-ryan: attack this section first (H-7).** It claims three things:
> 1. the law (L1) bounds, from emitted fields alone, the gap between the graded number and the real-arithmetic residual of the booked terms;
> 2. (L2) is the condition for that bound to be ≤ 1e-12;
> 3. **nothing about any measured cell.**
>
> It could be wrong in four ways, each checkable:
> * (i) a mis-read of the summation (§ F.2k.1, cited line by line at `933b438`);
> * (ii) a wrong constant (§ F.2k.2 cites its source);
> * (iii) a rounding between the booked terms and the graded number that (L1) leaves out (§ F.2k.3 lists every one);
> * (iv) a booking class the law does not count. § F.2k.4 makes the census an antecedent, so a missed class shows up as `UNGRADEABLE`, never as a silent pass.

#### F.2k.0 · What this section replaces. v1.11 § F.2k carries NOTHING operative

* **Retired:** the 4,500-term budget; v1.11's recursive-summation bound `γ_{m−1}·Σ|xᵢ|`; v1.11's code reading at `ffb454e`
  (the file has since moved twice, `e6903095…` → `41310e5e…` at `fae29ec` → `2277cc89…` at `933b438`); the measured
  depths 6,616 / 6,539 (pass-3 runtime); the conclusions *"STANDS"* and *"cannot fire"*; and the *"routing tension"*
  paragraph. That tension is **resolved**: KP-154 routed the re-sizing to Matt under v1.8 § F.2d case 2 as Q92, and
  KP-155 records Matt's ruling, *"(a) Compensated sum."*
* **Kept as lineage only:** 4,500 = v1.5's `1e-12 / eps` (v1.5 § F.2d (c), pinned), the linear worst case of a single
  plain running sum. v1.11 § F.2k showed it was never a sufficient check (OQ-17: the sinks were never counted). **It is
  retired, not re-sized.** The derivation gives no term budget in its place (§ F.2k.5).
* **Kept as principle:** the "What is NOT a derivation" box (§ F.2k.7) and § E's trap-12 addition.

#### F.2k.1 · The summation the port uses, read at godot `933b438` (pass 3b, compensated)

Read through git objects only: `git show 933b438:<path>`. Nothing was checked out, run or modified.
`kc2_runtime/sim/kc2rt_fight.gd` FILE `2277cc8940d2c50cde5d819545e4ffe5cfbc2207c8f38cfbfe85e37703190303`, `kc2_runtime/sim/kc2rt_laws.gd` FILE `c234376e9cbadc2d6f69549966112ec4fc1da7df46069831c7f1b80e3f581a9c`.
⚑ **These are the code the law was derived against, not the graded pins.** drax's KP-167 booking fix changes this file.
**Each item (N1)–(N8) must be re-verified at the graded digest** (H-6 (a)); a change to any of them is a change to the law's
antecedents.

* **(N1) Seven accumulators, Neumaier.** `_cons_add(k, x, split)` (`kc2rt_fight.gd:6471–6489`) keeps, per key, a running sum `s`,
  a running compensation `c`, a term count `n`, Σ|x| and a split count. The step (`:6474–6478`) is `t = s + x`; `c += (s − t) + x`
  if `|s| ≥ |x|`, else `c += (x − t) + s`; `s = t`. With the operand order fixed by the branch, `(s − t) + x` is the exact
  rounding error of `t` (Dekker's FastTwoSum). **`conservation[k] = t + cv` (`:6489`)** is the rounded value `fl(s + c)`. This
  is Neumaier's algorithm. Because FastTwoSum under the branch and Knuth's TwoSum return the identical exact pair, it
  computes, bit for bit, what Ogita–Rump–Oishi's `Sum2` computes.
* **(N2) `offered`.** `_offer(x)` (`:6448`) is `_cons_add("offered", x)` plus `n_terms_offered`. It never flags `split`.
* **(N3) The two inner sums, Neumaier.** They are local `[s, c]` pairs stepped by `_neu` (`:6519`):
  * the per-tick secondary-stream sum in `_secondary_streams` (terms at `:3425`, `:3459`; offered at `:3469` as
    `offered_acc[0] + offered_acc[1]`, i.e. `fl(s + c)`);
  * the per-attack PCL raw sum (terms at `:5358`; offered at `:5491` as `pcl_raw_acc[0] + pcl_raw_acc[1]`).

  Each has a term count and a sum count, plus Σ|term| (`inner_stream_abs`, `inner_pcl_abs`). *Stated so the fixed runtime
  is checked for it:* the stream counters move only when the tick's sum is `> 0` (`:3466–3468`), while its Σ|term| moves
  per term (`:3426`, `:3460`). A zero-sum tick has only zero-magnitude terms, so the law is unaffected.
* **(N4) Σ|term| per accumulator** is itself Neumaier-summed (`_neu(_cons_abs[k], absf(x))`, `:6485`) and emitted as
  `abs_sum_by_accumulator` (`:6551`). The term counts are `n_terms_by_accumulator` (`:6539`); inner counts and inner
  Σ|term| are emitted beside them.
* **(N5) Split roundings.** A call site that forms its term as a difference passes `split = true`
  (e.g. `:2816–2817`, `:3428`, `:3480`, `:5465`, `:5492–5493`, `:5508`). The count per accumulator is emitted as
  `n_split_roundings_by_accumulator` (`:6552`).
* **(N6) The final six-way sum and the graded number.** `conservation_residual` (`kc2rt_laws.gd:479`) runs Neumaier over the six
  stored sink values in `CONSERVATION_TERMS` order (`:484–495`), `total = ts + tc` (`:496`), `residual = offered − total`
  (`:497`, one rounding), `residual_relative = |residual| / max(1, |offered|)` (`:506`, one rounding), compared `≤ 1e-12`.
  Its count is emitted as `final_sum` (`kc2rt_fight.gd:6553`: 6 terms, 5 additions, 1 subtraction).
* **(N7) Emission only.** The accumulators feed no decision. *Not cited from this line:* it is re-shown at the graded
  digest by G3 at 0 (H-1) and G2 705/705.
* **(N8) Stale labels on the emission.** `conservation_residual` still prints `accumulation_budget_terms_v1p7: 4500`
  (`kc2rt_laws.gd:520`), and `conservation_report` prints an `n_terms_note` naming the ~4,500 budget (`kc2rt_fight.gd:6557`).
  ⚑ **Under v1.12 neither is read by the grader, and H-4 must not grade on them.** They are labels left over from v1.11.

#### F.2k.2 · The standard result (L0)

`u = 2⁻⁵³ = 1.1102230246251565e-16` (unit roundoff, binary64 round-to-nearest); `γ_k = k·u / (1 − k·u)` for `k·u < 1`.

**Source.** Neumaier (1974), *Rundungsfehleranalyse einiger Verfahren zur Summation endlicher Summen*, ZAMM 54:39–51 (the
algorithm); Higham, *Accuracy and Stability of Numerical Algorithms*, 2nd ed., SIAM 2002, § 4.3 (the method and its error
behaviour: of order `u·|S|` plus a term `O(n·u²)·Σ|xᵢ|`); **the explicit constant is that of** Ogita, Rump and Oishi, *Accurate
Sum and Dot Product*, SIAM J. Sci. Comput. 26(6), 2005, **Proposition 4.5**, proved for `Sum2`, which (N1) computes bit for bit:

> **(L0)** For `n` binary64 terms `xᵢ` with exact sum `S` and `A = Σ|xᵢ|`, round-to-nearest and no overflow, the compensated
> result `Ŝ = fl(s + c)` satisfies
>   `|Ŝ − S| ≤ u·|S| + γ²_{n−1}·A ≤ (u + γ²_{n−1})·A`.

**L0's antecedents at the port:**
* IEEE binary64 with round-to-nearest;
* every operation of the compensation step rounded separately, with no fused multiply-add and no extended precision.
  Otherwise `(s − t) + x` is not the exact error.

**The empirical check of both is H-6 (d), the fail-first probe:** GDScript's `_cons_add` / `_neu` must equal a Python Neumaier
reference **bit for bit** on a constructed vector where naive summation gives a different result. That probe ran at pass
3b (`ea14efc`; KP-167 also reports a bit-for-bit match to `math.fsum`). It must be re-shown at the graded digest.

#### F.2k.3 · Every rounding between the booked terms and the graded number (L1)

**The booked identity.** Every unit offered is booked into the six sinks by terms the code forms at its call sites.
Write `D` for the real-arithmetic residual of the booking over the terms **as formed**:
`D = Σ(offered terms) − Σ(sink terms)`.
**If the booking is exact** (every site in class T, S or F(f) of the census, § F.2k.4), the only non-zero contributions
to `D` are roundings, and

* **split / formation:** a term formed as `fl(a − b)` where the booking needs `a − b` has error `≤ u·|a − b| ≤ γ₁·|x̂|`. A
  term formed by `f` roundings has error `≤ γ_f·|x| ≤ γ_{2f}·|x̂|`. Let `φ` be the largest such factor over the census
  (`φ = γ₁` if every flagged term is a single difference). Then
  `E_split ≤ φ · Σ_{k : q_k > 0} A_k`, with `q_k` the flagged-term count of accumulator `k`, and `A_k` its Σ|term|
  (the flagged terms are a subset of it);
* **inner sums:** each offered inner-sum term is `fl(s + c)` of its inner terms (N3), while the sinks are booked against
  the inner terms themselves. By (L0) per inner sum, with each inner sum's term count `≤ N_I`,
  `E_inner ≤ Σ_I (u + γ²_{N_I−1}) · A_I`, over `I ∈ {stream, pcl}`. This is conservative where the sinks book against
  the offered float itself, as the PCL component does: `voided = raw − sum` (S), `pcl_reclaim = sum − pcl` (S),
  then `pcl` booked by `_land` as `applied = take` plus `pool_truncated = pcl − take` (S). These telescope to `raw`
(`:5491–5493`, `:5499`, `:5504–5508`). There the inner error does not enter `D` at all, and
  counting it only enlarges `B`.

So `|D| ≤ E_split + E_inner`.

**The computed side.** For each of the seven accumulators `k ∈ K = {offered, applied, dropped, voided, pool_truncated,
pcl_reclaim, counterplay_absorbed}`, (L0) gives `|Ŝ_k − S_k| ≤ (u + γ²_{n_k−1})·A_k`. The final six-way Neumaier sum over the six
stored sink values gives `≤ (u + γ²₅)·Σ_j |Ŝ_j|`, and `|Ŝ_j| ≤ (1 + u + γ²_{n_j−1})·A_j`. The residual subtraction and the
division each multiply by at most `(1 + u)`.

> **(L1)** If the booking is exact, the graded statistic `ρ̂ = residual_relative` of a cell satisfies
>
>   `ρ̂ ≤ (1 + u)² · B / max(1, |Ô|)`, where
>
>   `B = Σ_{k∈K} (u + γ²_{n_k−1})·A_k  +  (u + γ²₅)·Σ_{j∈sinks} (1 + u + γ²_{n_j−1})·A_j  +  Σ_I (u + γ²_{N_I−1})·A_I  +  φ·Σ_{k: q_k>0} A_k`.
>
> `Ô` is the emitted `offered`. **Negative terms are counted:** every `A` is a sum of absolute values. That covers the
> `voided` case (a term that goes negative when a banner or vector factor lifts `applied` above the raw offer).

**From emitted fields.** The `A`'s are emitted as Neumaier sums `Â` of non-negative terms. By (L0) the true value is bounded
by `A⁺ = Â / (1 − u − γ²_{n−1})`. `B⁺` is `B` with every `A` replaced by `A⁺`.

> **(L2) · CLAUSE (c), RE-KEYED.** In each cell, `TA-X-07` is **GRADEABLE iff all four hold**:
> 1. **every operand of `B⁺` is emitted for that cell, losslessly** (round-trip repr):
>    * `n_k`, `Â_k`, `q_k` for the seven accumulators;
>    * `N_I`, `Â_I` for both inner sums;
>    * `final_sum.n_terms = 6` and `sink_terms_present = 6`;
>    * `Ô`;
> 2. **the booking census (§ F.2k.4) is filed at the graded digest**, with every call site classed, and `φ` taken from it;
> 3. **every `n_k` and `N_I` satisfies `n·u < 1`**, so every `γ` is defined. That holds for any count below 9·10¹⁵.
>    (L2) is exact at any such count. § F.2k.5's first-order reading of `Λ` is accurate to one part in 10⁵ up to
>    94,907 terms, and it is printed, never graded;
> 4. **`β := (1 + u)² · B⁺ / max(1, |Ô|) ≤ 1e-12`.**
>
> Otherwise that cell is **`UNGRADEABLE`** on `TA-X-07`, and § G makes the verdict `INDETERMINATE`, as clause (c) always did.
> **Clause (a) is unchanged:** `ρ̂ ≤ 1e-12`, GREEN or RED. **Clause (b) is unchanged.**

**What (L2) buys.** Where it holds, a correct booking **cannot** produce `ρ̂ > 1e-12` from rounding. So a RED on (a) in such a
cell is a booking defect, not an accumulation artefact. That is the question clause (c) exists to settle. Clause (c)
evaluates its antecedent before firing, because the port is deterministic per (arm, salt) (`TA-X-01`), so the
emitted operands **are** the graded cell's.

#### F.2k.4 · The booking census: an antecedent of (L2), owed at the graded digest

The census is a static table of every `_cons_add` / `_offer` call site at the graded digest. Each row gives the line, the
accumulator, the offered site(s) it books against, and one class:
* **T:** the term telescopes **exactly** in real arithmetic against its offered counterpart, on the floats as formed. It
  is the same float bitwise, or exact by construction (e.g. `applied = dealt`, `voided = raw − applied` (S),
  `pool_truncated = applied − dealt` (S) sum to `raw`).
* **S:** formed as one difference `fl(a − b)` whose exact value the booking needs; flagged `split = true`; `φ = γ₁`.
* **F(f):** formed by `f` roundings independently of its counterpart (e.g. a product recomputed on the sink side);
  `φ = γ_{2f}`.

**The census also certifies closure:** every offered site's units are booked, and only into the six sinks the prereg
names. That is KP-167's ruling (*"no new sink invented; if the prereg names none, halt and report"*). Closure includes
every **deferred** booking. For example, under the loop layer the PCL component's sinks after `pcl_reclaim` are booked at
packet landing (`:5495–5498`), so the census must say where a unit is booked if its packet never lands. *This file
names the obligation. It makes no claim about where KP-167's leak is; that is drax's bisection.*

⚑ **Why it is an antecedent.** At `933b438` the runtime flags S terms, but nothing certifies that every **unflagged** term is
T, and KP-167 shows at least one offered unit is not booked. **The census is the static half of the booking proof; the
residual is the dynamic half.** (L1) needs both. A site that is missing, or classed by assertion rather than by reading,
leaves `φ` undefined, so (L2) item 2 fails and the cell is `UNGRADEABLE`. A missed class can never make the row green.

#### F.2k.5 · The condition, to first order, and its margin

For `n ≤ 94,907`, `γ²_{n−1} ≤ 10⁻⁶·u`. So, to within one part in 10⁵:

  `B ≈ u · [ A_offered + Σ_j (2 + φ̃·[q_j > 0])·A_j + Σ_I A_I ]`,  `φ̃ = φ / u` (`= 1` when every flag is a single difference).

Define the cell's **weighted absolute-mass ratio**

  `Λ := [ A_offered + Σ_j (2 + φ̃·[q_j > 0])·A_j + Σ_I A_I ] / max(1, |Ô|)`.

> **The condition.** (L2) item 4 holds, to first order, **iff `Λ ≤ 1e-12 / u = 9,007.199`**. Its **margin** is
> `M := (1e-12 / u) / Λ`. The grader evaluates `β` exactly (L2); `Λ` and `M` are printed beside it.

**What the derivation says about depth: nothing to budget.** Depth enters only through `γ²`. On the reference case below, the
term count at which depth **alone** would carry `β` past 1e-12 is about **5.2 × 10⁹** per accumulator. *Restated, as KP-155
asks, "only as the derivation gives it": the compensated method gives no term budget at any depth this runtime can
reach. The 4,500 figure belonged to plain running sums, and it is not replaced by another number.*

**What moves `Λ`, stated as law, not measured:**
* **The reference case** (not a measurement): every term non-negative, every sink carrying S-flags and no F-class.
  * `A_offered = |O|`.
  * `Σ_j A_j = |O|`, because the sinks then sum to `O` with no cancellation.
  * `Σ_I A_I ≤ A_offered`, because the inner terms are non-negative and sum to offered terms.
  * Hence **`Λ ≤ 5`, margin `M ≥ 1,801.4`.**
* **Negative sink terms** (e.g. `voided`). Let the negative terms carry total magnitude `N`. Then `Σ_j A_j = |O| + 2N`, so
  `Λ ≤ 5 + 6·N/|O|`. The condition fails only beyond **`N / |O| ≈ 1,500`**.
* **F(f) classes** raise a sink's coefficient from 3 to `2 + 2f`.

**So (L2) is a cancellation-and-formation condition, not a depth condition.** That is the precise sense in which Q92 (a)
makes the 1e-12 tolerance hold "at any realistic depth".

#### F.2k.6 · ⚑ THE MEASURED VALUES: PENDING drax's fixed runtime (KP-167)

**No value from the pass-3b runtime (godot `933b438`) is entered here.** There, the identity leaks on 22 of 25 cells
(KP-167), and drax's fix books units that are not booked now, so it changes the term counts and the `A`'s. **No sentence
of § F.2k depends on those numbers.** The law above was written from the code and the standard result alone.

**This file is immutable, so the values are not written into it later.** They are filled into this form in **the H-6
discharge note** (gamora, evaluating (L2) from drax's emission at the graded digest) and in the verdict file's `r11_bound`
(§ G.3). If seeing them prompted any change to the law, its coefficients or its antecedents, that change would be a new
dated version with its own H-7 pre-read, and a HALT to Matt if a graded run already exists (`WARN-16`).

| arm · salt | `n_k` (7) | `N_I` (2) | `Â_k` (7) | `Â_I` (2) | `q_k` (7) | `φ` | `Λ` | `β` | `M` | (L2) | `ρ̂` (clause (a)) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| each of the 25 cells (`M0`, `M-POL-2`, `M-POL-2-NULL`, `W1`, `W1-NULL` × salts 0–4) | PENDING | PENDING | PENDING | PENDING | PENDING | PENDING (census) | PENDING | PENDING | PENDING | PENDING | PENDING (graded only in the attempt) |

**Owed by drax for this form (H-6):**
* (a) the fixed runtime, with its digest, and the godot re-pin of `kc2rt_fight.gd`, `kc2rt_laws.gd`, the runtime tree and the
  G3 instrument;
* (b) every (L2) operand for all 25 cells, lossless;
* (c) the booking census at that digest;
* (d) the fail-first probe at that digest.

H-1's G3 at that digest is owed separately.

#### F.2k.7 · What is NOT a derivation (carried in principle, re-stated for the compensated method)

> * **The observed residual**, small or large, is not clause (c)'s criterion. It cannot rescue the row, and it does not size
>   the tolerance (v1.8 § F.2d).
> * **Dropping any rounding from `B`:** an accumulator, an inner sum, the six-way sum, the residual subtraction, the division
>   or a census class. (L1) counts everything between the booked terms and `ρ̂`. A bound that leaves one out repeats
>   OQ-17 in a new form.
> * **A probabilistic `√n` estimate:** a model of typical error, not a worst-case bound.
> * **One cell's margin read as all 25:** (L2) is evaluated per cell.
> * **Coefficients chosen after seeing the values:** that is a new dated version (§ F.2k.6), not a reading of this one.

### ⚑ F.2l · `TA-X-18`: "EXACT" MADE OPERATIONAL (WARN-1; closes OQ-16)

**Value (carried, re-derived on the oracle, § A.2):** `(-3.999999999999985, -3.49691120014899e-07)`, i.e. bit patterns
**`0xc00fffffffffffde`** and **`0xbe9777a5cf72cec6`**.

**The grading rule.** For each component `i`:
1. **Parse** the emitted string to binary64 with a correctly rounded parser (CPython `float()`).
2. **Compare bits:** `struct.pack(">d", parsed_i) == struct.pack(">d", expected_i)`. That is `==` on the value **with the
   sign of zero checked**: `+0.0` and `−0.0` differ, and a NaN never matches.
3. **GREEN iff both components match.** A mismatch on a lossless emission is RED.

**Lossless emission is a precondition, not an assumption.** Any decimal string of ≤ 15 significant digits is its own shortest
repr, so losslessness cannot be read off the string. It is a property of the emitter. **The row is `UNGRADEABLE` (not
green, not red) unless both hold:**
* (i) the emission is CPython's shortest round-trip repr (drax `91c8fe1`), or ≥ 17 significant digits, or a C99 hex-float;
* (ii) at the graded digest, the harness's round-trip probe (`91c8fe1`: 22 vectors) shows the emitter reproduces
  `repr(x)` for every vector.

A string-level check runs as well: if the emitted string has fewer than 17 significant digits and is not equal to
`repr(float(s))`, the emitter is not CPython's repr, and the row is `UNGRADEABLE`.

*What this changes:* nothing in the value or the tolerance. "Exact" was v1.1's word. The grade of record and v1.7
attempt 1 applied a looser "nearest of three laws, separation > 1e-6" reading silently, and v1.10 restored "exact" (KP-149;
jack-ryan item 1: a correction, not a fit). v1.12 writes down how "exact" is evaluated, so a `%.17g` print of the same float
cannot read RED and a lossy print cannot read GREEN. `C-o` still does not cover the row. A last-ulp libm disagreement routes
to Matt under `F.1a`, and the grader never widens.


### F.3 · DIAGNOSTIC rows: 19 ids, 0 gating, every width VOID *(carried from v1.11 § F.3)*

⚑ **CLASS V · `TA-B-01`, reference sentence (mandatory, verbatim at v1.12; version label only):** ***"`BAND /
NON-DECISIVE / REPORT-ONLY`. A terminal wave inside or outside this band is not evidence of fidelity either way. It
is read from the port's `M-POL-2` arm. The oracle's sealed `M-POL-2` arm terminates at `[156, 152, 151, 151, 156]`,
`player_death` on every salt. The v1.12 oracle's `M-POL-2` arm (the same object as v1.8's, v1.9's, v1.10's and v1.11's:
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
  arms, `M-POL-2` and `W1`; the other three arms have no G3 record yet, § C.9.6). **So if the clear has a cause other than chance, it lies where G3 does not look: in the port's
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

⚑ **v1.12 NOTE: ONE BOARD REALISATION PER SIDE (INFO-5; diagnostic only, gates nothing).** To the extent the ORACLE-config
board is salt-independent (KP-144 (a): `engine_seed(9, w)`), each side fights **one** board realisation, and the five salts
are replicates of the fight streams **on that board**. So remedy (ii) above, *"n in the tens per side"*, would sample
**stream** variance, not **board** variance. It could not separate a board-realisation effect from a generator defect. Telling
those apart would need several board realisations per side, which the ORACLE configuration does not provide. Read with
`C-p` (§ E.2): the generator's realisation is graded by law, not by outcome.
**Nothing here is graded, and nothing gates.** It is printed so that Gate-2 looks before attempt 1, as KP-152 asks.

### F.4 · Emitted, not graded: **three** *(carried)*

### F.5 · Report-face rules: twelve

**Cl. 1–6, 8, 9, 10 and 12 carried verbatim.** Changed:

7. **THE SUSTAIN SENTENCE (mandatory; version label only):** ***"`leech` and `intake` still have no oracle side in
   the seals (`C-e`). Off-seal, the v1.12 oracle (the same object as v1.8's, v1.9's, v1.10's and v1.11's; the C-11a
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
    v1.12 PASS is not quotable without jack-ryan's hole-closure finding at the same runtime digest, and the seal is
    blocked on any non-zero R-6 invariant."*** Followed by the three R-6 invariants, printed with their values.

---

## § G · FAIL TAXONOMY, THE HOLE-CLOSURE RULE, AND THE GRADED-RUN CAP

| verdict | antecedent | consequence |
|---|---|---|
| **`STRUCTURAL`** | ≥ 1 of the 28 EXACT rows RED | the port is wrong; **consumes one of v1.12's two attempts**; L2 applies |
| **`INDETERMINATE`** | 0 EXACT red, ≥ 1 of the 28 UNGRADEABLE (incl. `P-1`…`P-5` red, and `TA-X-07(c)`: § F.2k (L2) not holding on a cell) | does NOT consume an attempt; nothing seals |
| ~~`STATISTICAL`~~ | retired at v1.5 under F5 | — |
| **`PASS`** | all 28 EXACT green, none UNGRADEABLE | ⚑ **`PASS @ coverage k/89, 28/28 EXACT rows green, TA-X-06 UNGRADEABLE-declared (Q83(b)), dilution ⟨d⟩×, substrate_epoch v3.7.1/48a4c94c…, prereg v1.12`**. Never unqualified, and never quotable alone (§ G.2) |

**Order:** `STRUCTURAL → INDETERMINATE → PASS`; stop at the first hit. No diagnostic appears in any antecedent. **No
post-hoc widening, by anyone.** `declared_ungradeable` must be **exactly** `["TA-X-06"]`; anything else is **C1**.
⚑ **A row graded on an arm other than § B.1a's, or on an arm not configured from its `a8` rows, is non-conforming
(C1), not red and not green.** ⚑ **The evidence of configuration is that arm's G3 PASS at the graded digest (§ C.9, § B.1a); a probe row of `setup` applied to an arm is C1.**

### G.1 · THE GRADED-RUN CAP: **`0` OF `2` UNDER v1.12**

**The allowance is carried unspent** (Matt KP-115; KP-137; no graded run exists under v1.8, v1.9, v1.10 or v1.11). **Q85's
four guards hold:**
1. the allowance was ruled from outside the run (Matt);
2. this prereg is committed ALONE, every pin recomputed, before anything is graded against v3.7.1 (D4);
3. v1.7's attempt 1 stays on the record, spent;
4. `substrate_epoch` is declared on every artifact.

**Naming:** the next graded run is **v1.12 attempt 1 (overall attempt 2)**.

⚑ **L2, AS IT APPLIES TO v1.12.** v1.12 attempt 1 fires only after ALL of the following:
- ⚑ **drax's KP-167 booking repair**: the `TA-X-07` booking defect is localized and fixed. Every offered unit is booked into a
  sink this prereg names, and no new sink is invented. The fight is unmoved: G3 at 0 (§ C.9) and G2 705/705. Its runtime is
  **the graded runtime**, and every godot pin is re-pinned at its digest (H-6 (a)).
- ⚑ **G3 (§ C.9) PASSES on all five arms × five salts at that digest**: zero injections, 0 decision divergences, the draw and
  stream rules, death wave and tick equal (H-1). *(Carried from v1.11: v1.10's L2 bullet asked for a native per-salt death-wave
  match. The conductor's KP-152 corrigendum rules that unattainable by construction, and it changes an attempt precondition,
  not a graded row (Discipline #12). At v1.12 G3 is defined in this file instead of by ledger reference.)*
- jack-ryan's **repair Gate-2** PASSes that runtime on the digest it names (R-7), covering the KP-167 repair and the census.
- **this file's pre-read** has been filed (`H-7`: the § F.2k rewrite and the v1.11 → v1.12 delta. The rest of v1.12 may
  cite jack-ryan's v1.11 pre-read).
- ⚑ **R-11 (`H-6`): (L2) of § F.2k holds on EVERY one of the 25 cells of that runtime**, evaluated from its emission before
  firing (the port is deterministic, `TA-X-01`). **PENDING** (§ F.2k.6). A cell where (L2) fails would make the attempt
  `INDETERMINATE` by construction, so the attempt does not fire on such a runtime (v1.8 § F.2d cases 2–3: firing would consume
  nothing and buy nothing).
- `H-9`: discharged (PASS); `H-10`: discharged (KP-153). Nothing further owed on either.

v1.12 attempt 2 fires only after a v1.12-attempt-1 `STRUCTURAL` red is repaired and jack-ryan's Gate-2 PASSes the
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
**> 0** wherever a PCL row fired. **R-9, carried as law:** a v1.12 `PASS` is quotable only with jack-ryan's
hole-closure finding GREEN at the SAME runtime digest; any non-zero R-6 invariant blocks the seal; **Q87's seal at
v1.12** = `PASS` (28/28) AND coverage 89/89 AND T-B reported DIAGNOSTIC AND the hole-closure finding GREEN at the
graded digest AND **Matt's T-C yes on that same digest** (KP-114).

### G.3 · Verdict file `kc2play.ta_verdict.v1` (v1.12): **the fields that change from v1.11 § G.3**

```
prereg_version                    : "v1.12"
prereg_sha256                     : <this file, derived at emission>
substrate_epoch                   : "v3.7.1 / model 48a4c94c… / reference 1887257f…"          (unchanged)
runtime_digest                    : <the graded, post-KP-167 runtime; PENDING>          (H-6 (a))
arm_config_a8                     : {<arm>: {"a8_rows": "<first>…<last>", "rowset": <§ B.1a digest>,
                                     "setup_config_rowset": "207ab21f…", "setup_probe_rows_applied": 0,
                                     "configured_from_a8": true, "c1_evidence": "g3[<arm>]"}, …}       § B.1a
g3                                : {<arm>|<salt>: {"injected": [], "decision_divergences": 0,
                                     "draw_mismatches": 0, "port_only_streams": [], "oracle_only_streams":
                                     ["spawn_structure.py:344|0", "player_kit_residual.py:286|…"],
                                     "death": {"port": [<wave>, <k>], "oracle": [<wave>, <k>], "equal": true},
                                     "oracle_post_check": true}, … all 25}, "instrument": {<two FILE pins>}   § C.9
r11_bound                         : {"law": "§ F.2k (L2)", "u": 2^-53,
                                     "per_cell": {<arm>|<salt>: {"n": {<7>}, "N_inner": {<2>}, "A_hat": {<7>},
                                       "A_hat_inner": {<2>}, "q": {<7>}, "phi": <from census>, "offered": <Ô>,
                                       "B_plus": <…>, "beta": <…>, "Lambda": <…>, "margin": <…>,
                                       "L2_holds": <bool>}, … all 25},
                                     "census": {"file": <FILE>, "sites": <n>, "classes": {"T":…, "S":…, "F":…}},
                                     "probe_bitwise": <bool>, "all_25_hold": <bool>}        clause (c) is (L2)
ta_x_18                           : {"expected_bits": ["c00fffffffffffde", "be9777a5cf72cec6"],
                                     "emitted": [<s0>, <s1>], "parsed_bits": [<…>, <…>],
                                     "emitter": "cpython-repr", "roundtrip_probe": <bool>,
                                     "lossless": <bool>, "equal": <bool>}                  § F.2l
port_holes_printed                : true    (§ F.5 cl. 11, extended)
```

⚑ **RETIRED:** `r11_budget` (its `budget_terms: 4500` and `outcome: "STANDS"` carry nothing) and `ta_x_18_expected` (subsumed by
`ta_x_18`). The runtime's own `accumulation_budget_terms_v1p7` and `n_terms_note` labels are **not read** (§ F.2k.1 (N8)).
**Every other field is v1.11 § G.3 unchanged** (`model_pack`, `reference_pack`, `cross_pin_verified`, `runtime_header`,
`preconditions.P4_pack`, `arm_of_record`, `oracle_containment_H9`, `closure_H10`), and so are v1.10 § G.3's `set_digests`
(the four reproduce), `P5_folds` (eleven), `declared_ungradeable` (**exactly** `TA-X-06`), `gmag_conformance`, `nodata` and
`hole_closure`. **T-B quoting cap: C1 / C2 / C3 unchanged.**

---

## § H · OWED BEFORE v1.12 ATTEMPT 1 (blocking)

| # | owed | owner | why it blocks |
|---|---|---|---|
| **H-1** | ⚑ **G3 (§ C.9) at the graded (post-KP-167) digest on ALL FIVE ARMS × five salts**: zero injections, 0 decision divergences, 0 draw mismatches, no undeclared stream, death wave and tick equal, and each oracle trace checked against its arm's POST figures. ⚑ **At `933b438` the oracle-trace tool builds two arms (`M-POL-2`, `W1`), and pass 3b's G3 covers those two only. `M0`, `M-POL-2-NULL` and `W1-NULL` are owed.** Carried: every arm configured from its `a8` rows (§ B.1a, with the `setup` partition); the port draws nothing from the control-gate stream on a graded arm (§ A.4 of v1.11) and runs the `r9` columns on `None` | **drax** | G3 is the sole fidelity precondition and the C1 evidence |
| **H-2** | `spawn_by_record` per arm per salt, over roster bodies only | drax | `TA-X-25(c)` is UNGRADEABLE without it |
| **H-3** | `TA-X-29(e)`'s probe values: `3.207764` / `4.980316` + the 39 per-record values, on the `WALK` configuration (`IC7-A-0379`…`0432`) | drax | R-1 |
| **H-4** | ⚑ **the harness re-pointed to THIS file** (drax's `b14b050` pins v1.11; it must move): the label from the pinned prereg; `substrate_epoch`; every arm from its `a8` rows with the ROWSETs of § B.1a **and the `setup` partition (C applied once, T applied to no arm)**; the § B.1a arm table; `TA-X-26(b)` by hashing the loaded CSV (with `path_used` and `sha_measured` printed in full, drax `91c8fe1`); the V0 diff (V0-37 = GATE_FIRST); ⚑ `TA-X-18` per § F.2l (lossless, bits, the round-trip probe); ⚑ `r11_bound` per § G.3 with every (L2) operand for all 25 cells; ⚑ `g3` per § G.3. **The legacy `r11_budget` / 4,500 fields are not graded** | drax | a v1.11-pinned harness mislabels a v1.12 run |
| **H-5** | the hole-closure finding at the graded digest (§ G.2) | **jack-ryan** | `PASS` is not quotable without it |
| ⚑ **H-6** | ⚑ **R-11 under (L2), on the graded runtime. PENDING (KP-167):** (a) the KP-167-fixed runtime and its digest, with godot re-pinned (`kc2rt_fight.gd`, `kc2rt_laws.gd`, the runtime tree, the G3 instrument) and (N1)–(N8) re-verified there · (b) every (L2) operand for all 25 cells, lossless · (c) **the booking census** (§ F.2k.4) at that digest · (d) **the fail-first probe** at that digest: GDScript Neumaier equals a Python Neumaier reference bit for bit on a constructed vector where naive summation differs · then (e) gamora evaluates (L2) per cell and files the § F.2k.6 form as the H-6 discharge note. **Discharged iff (L2) holds on all 25 cells** | drax (a)–(d) · gamora (e) · jack-ryan (Gate-2 on the census) | clause (c): where (L2) fails the row is UNGRADEABLE, and the attempt is `INDETERMINATE` by construction |
| **H-7** | **this file's pre-read**, partial: § F.2k + § F.2l + § C.9 + the § B.1a partition + the v1.11 → v1.12 delta. The rest may cite jack-ryan's v1.11 pre-read | **jack-ryan** | D4 / the series' practice. ⚑ **Attack § F.2k first** |
| **H-8** | Matt's T-C re-confirm on the graded digest | Matt | a seal condition, not an attempt precondition |
| ~~H-9~~ | ~~the oracle's `W1` containment~~ | gamora | **DISCHARGED: PASS** (KP-146) |
| ~~H-10~~ | ~~the closure proof on `M0`, `M-POL-2-NULL`, `W1-NULL` and the walk~~ | star-lord | **DISCHARGED** (KP-153; receipt FILE `a0ad8246ac49628f8bd729c8cc2fba564b6456c4c06df0ae300e0439bfc447c9`) |

**Not blocking, named so they are not lost:** v1.11 § H's list, carried · `C-o` · `C-p` · OQ-14 · OQ-15 (with its tripwire) ·
the F.3a generator question (Gate-2) · the KP-139/KP-143 hole-number swap (the committed record governs: 15 = resist cap,
16 = attack speed + OA adds).

---

## § I · OPEN QUESTIONS: one lean each

**OQ-1 … OQ-13 carry v1.11's dispositions** (OQ-13 closed by H-9).

**OQ-14 · Loop-layer oracle config and `P-5`** → **OPEN, lean unchanged** (v1.11 § I). A loop switch passed explicitly
at a non-default value in an arm's `a8` rows is the `P-5` hazard OQ-14 names. *Not folded here.*

**OQ-15 · `TA-X-26(b)` under a closed pack** → **OPEN, lean unchanged.** ⚑ **THE TRIPWIRE, WRITTEN (INFO-6):**
* At godot `fae29ec` and since, `kc2_runtime/loader/kc2rt_leech_table.gd:69-99` reads the path and `sha256` from the
  wire's `V1-JOIN-1`, opens the engine file `data/kc2/pm4p_leech_resistance.csv`, hashes its bytes, and **aborts the load
  on a mismatch**. So (b) is met by construction, **provided** the emission prints `path_used` and `sha_measured` (drax
  `91c8fe1` does) **and the grader checks `sha_measured == P-i` on the emission**, not on a commit message.
* ⚑ **If the leech table is ever re-pointed to the pack's `IC7-F-44` image alone** (for closure purity), (b) goes **red
  by construction**, and a faithful port takes a `STRUCTURAL`. **That re-point must not happen before OQ-15 is resolved
  in a dated prereg version.**
* Any widening of (b) is a row change, so it goes to Matt (KP-137).

**OQ-16 · `TA-X-18`'s exact reading** → ⚑ **CLOSED.** "Exact" stays float64 equality, and it is now operational (§ F.2l:
bits with the sign of zero, a lossless emitter, else `UNGRADEABLE`). Closed on jack-ryan's v1.11 pre-read, item 1
(PASS: a correction, not a fit; WARN-1 folded).

**OQ-17 · Clause (c)'s antecedent is not sufficient for its own bound** → ⚑ **CLOSED BY THE RE-KEYING** (§ F.2k). Clause (c)
is now (L2):
* it is keyed on the computable inequality over **all** seven accumulators, both inner sums, the six-way sum, the
  call-site roundings, the residual subtraction and the division;
* it uses **Σ|term|** per accumulator, so negative terms are counted;
* every operand is emitted.

It is no longer a budget on `offered` alone. v1.11's *"until then grade (c) as written"* is **not** carried. No past verdict
changes: v1.7 attempt 1 was `STRUCTURAL` on `TA-X-25`, which is evaluated first, and its `TA-X-07` was already `UNGRADEABLE`.

---

## § J · DISCIPLINES THIS VERSION EXERCISED

> ⚑ **A LAW IS WRITTEN BEFORE THE NUMBERS IT WILL JUDGE.** The runtime that motivated this version leaks on 22 of 25 cells.
> Its term counts are wrong as a matter of booking, and the fix will change them. So the bound is stated as a law over
> `(n, Σ|term|)`, with every rounding between the booked terms and the graded number counted. It was derived from the code
> and the standard result alone. Every measured value is left PENDING, because a bound drafted beside its first
> measurement can be bent toward it without anyone noticing.

> ⚑ **A DEFINITION THAT LIVES IN A LEDGER IS A FIRING CONDITION NOBODY PINNED.** G3 became the sole fidelity precondition at
> KP-152 and was never defined in a prereg. § C.9 now defines it. Doing so showed that it covers two of the five arms.

> **Carried from v1.11:** *A definition that lives in prose is an input nobody hashed* (arms cite `a8`; at v1.12 the `setup`
> job is split by row id under a rule read off the pack). *n = 5 is a description, not a test* (§ F.3a, now with the
> one-board-realisation note).

> **Carried:**
> * Law 3: no fitted constants, and no tolerance or expected value moved toward a measurement. **The 1e-12 tolerance stays.**
> * the `F.1a` expiry clause;
> * the honest-`n` law;
> * `#75` cl. 1(a);
> * KP-101: every digest labelled;
> * **Discipline #12:** the re-keying of `TA-X-07(c)`, `TA-X-18`'s operational reading, and `TA-X-11`'s and R-11's
>   populations, each named as a semantic or population fact;
> * **digests computed by script, never typed.**

---

*Filed 2026-10-01 by **gamora** (simulation + spirit-guide seam), Run KC2-PLAY.

⚑ **What v1.12 does:**
* **It re-derives R-11 for Neumaier compensated summation**, per Matt's Q92 (a) (KP-155). Clause (c) of `TA-X-07` is
  now (L2), a law over each accumulator's `(n, Σ|term|)`. It counts:
  * the seven accumulators;
  * the two inner sums;
  * the final six-way sum;
  * the split and formation roundings, under a booking census;
  * the residual subtraction and the division.

  To first order it holds iff `Λ ≤ 1e-12/u ≈ 9007`. The 4,500-term budget is retired, not re-sized. **The 1e-12 tolerance is
  unchanged. No expected value moves on any of the 28 EXACT rows or the five preconditions.**
* ⚑ **The measured values are PENDING drax's KP-167 booking fix**, and so is the godot re-pin. No conclusion here depends on
  the leaking pass-3b numbers.
* **The rest of jack-ryan's v1.11 pre-read is folded in.** G3 is defined in this file (§ C.9), and it covers two of the five
  arms so far. The `setup` job is partitioned by row id. `TA-X-18`'s "exact" is operational. `TA-X-09`'s nine-vector ROWSET
  is given in full. `C-p` is declared. OQ-15's tripwire is written. OQ-16 and OQ-17 are closed.

**Attempts: `0` of `2`, carried unspent.** The declared set is closed at exactly `["TA-X-06"]`. **NO BAND WIDTH MINTED.** **K-7
held:** the sealed cells were hash-verified only.

**What this session touched, and how:**
* **The oracle**, only through `pool466`, `load_profiles`, `derive_oracle_speeds` and `SpawnStructureFold.offset`.
* **drax's runtime source and G3 instrument**, through git objects at godot `933b438`, read-only.
* **star-lord's v3.7.1 pack**, read and modified in nothing.
* **v1.11 and every earlier version are NOT edited.**

⚑ **THIS FILE IS IMMUTABLE. Any change after a graded run exists against it is a HALT (`WARN-16`).**
**No production code. No dispatch. No push. D4 held: committed ALONE.***
