# KC2-PLAY · T-A PREREGISTRATION **v1.8** — the goalposts for the graded run on the **v3.6** substrate (the 338 armed; the C-11a-corrected oracle)

> ⚑ **STATUS: IMMUTABLE ON COMMIT. v1.8, authored 2026-09-30. SUPERSEDES v1.7 FORWARD.**
> *(The filename carries the series' `2026-09-20` prefix. The document is dated 2026-09-30.)*
>
> ⚑ **v1.8 IS A FORWARD RE-DERIVATION FOR A FULLER BOARD. IT IS NOT A ONE-CHANGE VERSION.** Matt ruled
> Q91 (*"Lift their damage first"*, KP-115). The 338 `w45` pool records now carry damage magnitudes. The
> oracle constructs their profiles through its own loader (`load_profiles(pool_lift=…)`). star-lord cut
> pack **v3.5** (KP-122), then **v3.5.1** (KP-123: the fallback run-speed law and its population on the
> wire), then **v3.5.2** (KP-126: the oracle's monster march base on the wire). Matt then ruled that
> the C-11a oracle corrections fold **before** v1.8 (KP-127). They were folded (C1, C2, C4; C3 not folded,
> KP-131), and star-lord cut **v3.6**. **Every row was re-derived against v3.6 and the folded oracle.**
> § 0 gives the per-row diff, and each row there is labelled **carried**, **re-derived** or
> **corrected**, with the reason.
>
> ⚑ **ATTEMPTS: RESET TO `0` OF `2` UNDER v1.8** (Matt, KP-115: *"Reset to 2"*; consistent with Q85: a
> new reference is a new instrument). **Graded attempt 1 stays on the record as SPENT AGAINST v1.7**
> (`STRUCTURAL @ 89/89`, collab `15d6f5ce8`, verdict `9be2d56b…`). It is not a prior for anything here
> (§ C.7).
>
> ⚑ **THE DECLARED SET IS CLOSED AT EXACTLY `["TA-X-06"]`** (Matt, Q83(b), KP-110). v1.8 states the
> closure in words. v1.7 closed it only by enumeration (jack-ryan's v1.7 pre-read, WARN-1).
>
> ⚑ **THE PORT≠ORACLE HOLES ARE NOT NEW EXACT ROWS.** There were six when v1.8 was fired, and the
> conductor named a seventh at KP-126 (the march base). Nobody ruled a goalpost expansion. They are
> **seal-blocking through jack-ryan's hole-closure finding** (R-3…R-6, R-9, R-13…R-16; hole 7's
> criterion is his to fix, § G.2). **A v1.8 `PASS`
> may not be quoted unless that finding is green** (§ G.2).
>
> ⚑ **THIS FILE IS IMMUTABLE ONCE COMMITTED. ANY CHANGE AFTER A GRADED RUN EXISTS AGAINST IT IS A HALT
> TO MATT (`WARN-16`).** Not an erratum and not a clarification: a HALT.
>
> ⚑ **D4 HELD. This file is committed ALONE, with zero code, before any graded run against v3.6
> exists.** Every derivation in it comes from the pack of record, the oracle at engine HEAD
> `96b4529a`, or a pinned artifact. Nothing was transcribed from a ledger row. Where a ledger
> row disagrees with the derivation, the ledger row is corrected forward (§ A.6).
>
> **Authority:**
> * ⚑ **Q91 (Matt, KP-115): *"Lift their damage first"*** → pack v3.5 → prereg v1.8, re-derived FORWARD.
>   **Attempts: *"Reset to 2"*.**
> * ⚑ **KP-122** — pack v3.5 cut (`ba50f8b0…` / `4d23fe84…`). v1.8 was fired with `TA-X-25(c)` to be
>   re-derived from `u5` at the fight grain, z4 re-walked under P-5, and the six holes made
>   seal-blocking through the hole-closure finding.
> * ⚑ **KP-123** — pack **v3.5.1** (the oracle's `FALLBACK_RUN_SPEED` law and population on the wire).
>   Lineage; carried into v3.6.
> * ⚑ **KP-126** — pack **v3.5.2** (the oracle's monster/pet speed base `MARCH_BASE_M_PER_S[px-LO]` =
>   3.209466 m/s on the wire; the port ran 4.0). Lineage; carried into v3.6.
> * ⚑ **KP-127 (Matt): the C-11a corrections fold BEFORE v1.8 and attempt 2.** This is a REFERENCE
>   change, authorized. Fold: engine `b0b041d0` (math note ALONE) → `afc8b702` (C1) · `ce8177ff` (C4) ·
>   `6edb6c96` / `4a6dcdda` (C2) · `e9ae3850` (v3.6 rowsets) · `866db7fb` · `28735961` (pricing).
>   ⚑ **KP-131 (conductor): C3 is HALTED and NOT folded**; Z5 is restated unchanged (rowset `c5`).
> * ⚑ **v3.6 (star-lord, KP-127/KP-131)** — the C-11a rowsets on the wire. **v1.8 pins v3.6: not v3.5,
>   v3.5.1 or v3.5.2.**
> * **Q83(b) (Matt, KP-110):** `TA-X-06` is UNGRADEABLE-declared. **Q85 / Q87 (KP-83):** carried. For
>   Q87, *"all EXACT rows green"* means **28** rows (§ 0.1).
> * **F5 (KP-49):** the EXACT half is the instrument. The tolerance half is a DIAGNOSTIC and **gates
>   nothing**.
> * **jack-ryan, Gate-2 on attempt 1** (`qa/findings/…-ta-grade-v1p7-attempt1-gate2.md`, `d2aa93db…`):
>   R-1…R-12 are fixed before any repair result. The conductor added **R-13…R-16** for holes 3–6
>   (KP-116, KP-118, KP-120).
>
> **Author:** gamora (simulation + spirit-guide seam), Run KC2-PLAY SEAL LAP. **Decision rules only.
> NO BAND WIDTH IS MINTED HERE, AND EVERY WIDTH IN `P-a` STAYS VOID (v1.6 § A.4, carried).**
> **v1.7 (`552d9fae…`), v1.6, v1.5, v1.4, v1.3, v1.2, v1.1 and v1.0 are NOT edited.** v1.4's grade of
> record (`STRUCTURAL @ coverage 89/89`) and v1.7 attempt 1's `STRUCTURAL` both stand. Nothing here
> regrades them.
>
> **Occasioned by:** charter ledger **KP-113 … KP-131**, and Matt's sealing ruling on C-11b (*"Seal v1 with the
> gap declared"*). v1.7's occasion list is carried as lineage in
> the pinned v1.7.

---

## § 0 · ⚑ PER-ROW DIFF v1.7 → v1.8, WITH THE REASON FOR EACH ROW

**Legend.** **CARRIED** means the assertion and its expected value are unchanged. Where the value is a
substrate property, it was re-computed and reproduced. **RE-DERIVED** means the assertion keeps its
shape, but its population, pin or expected value was computed again from the moved substrate.
**CORRECTED** means v1.7's value was wrong for the configuration it names.

### 0.1 · Preconditions

| id | v1.8 | reason |
|---|---|---|
| `P-1` coverage 89/89 | **CARRIED** | a census property, not a pack property. Read the four-way counts off the run |
| `P-2` stream disjointness | **CARRIED**, and the **epoch law is extended to v3.6** (§ C.7) | the pool lift arms 334 more swinging records. More bodies reach `choose_slot` and the chance draws, so the stream moves. `P-2` stays a within-epoch probe |
| `P-3` roll population / law | **CARRIED**. POOL-466 re-derived: **466**, set digest pinned | `waves.json` is byte-identical v3.4.2 → v3.5 → v3.5.1 → v3.5.2 → v3.6 (re-verified at fill) |
| `P-4` pack identity | ⚑ **RE-DERIVED: REPOINTED to v3.6** (model + reference + cross-pin) | KP-122 / KP-123 / KP-126 / KP-127 |
| `P-5` oracle fold settings | ⚑ **RE-DERIVED: EXTENDED from 4 folds to 11 settings.** ⚑ **Setting 11 is the C-11a fold (C1 + C2 + C4 ON; C3 NOT folded, KP-131).** New: **`pool_lift` ARMED** · the loader argument set · the **PCL limb** (`u7`) · the **non-health route** (`u6`) · the **monster run-speed population** (KP-123) · ⚑ **the march base the oracle composes speed against (3.209466 m/s; on the wire since v3.5.2, KP-126)** | a default-OFF fold the graded oracle must arm is the P-5 hazard, and `pool_lift` is default-OFF. The fallback speed law was the oracle's and was not on the wire |

### 0.2 · EXACT rows (28) + the declared row

| id | v1.8 | reason |
|---|---|---|
| `TA-X-01` | **CARRIED** | run-internal |
| `TA-X-02` | **CARRIED** | census |
| `TA-X-03 / 04 / 05` | **CARRIED IN FORM. Every digest moves** (§ C.7 cl. 1) | port-to-port at one substrate |
| `TA-X-06` | **CARRIED as UNGRADEABLE-declared.** ⚑ **The closure `declared_ungradeable == ["TA-X-06"]` is now stated in words** | v1.7 pre-read WARN-1: the class was closed only by enumeration |
| `TA-X-07` | **CARRIED VERBATIM.** ⚑ **R-11's measurement is recorded, and the law is stated for both outcomes** (§ F.2d) | R-11 measured **1,226** terms on one v3.4.2 cell, against a budget of 4,500. Must be re-measured on the v3.6 runtime |
| `TA-X-08` | **CARRIED** | an identity |
| `TA-X-09` | ⚑ **RE-DERIVED: the pin moves, the nine vectors do not.** Scope stays **9**. `C-h` carried | `math_rules.json` gains only `⚑ v3p5_*` and `⚑ v3p6_*` blocks. The 15 rules and 29 vectors are content-identical |
| `TA-X-10` | **RE-DERIVED, UNCHANGED** (43.758085029822276) | `arena.json` is byte-identical |
| `TA-X-11 / 12 / 13 / 14 / 15` | **CARRIED** | no substrate dependency moved |
| `TA-X-16` | **RE-DERIVED, UNCHANGED** (54 with p06, 47 without) | `waves.json` is byte-identical |
| `TA-X-17 / 18` | **RE-DERIVED, UNCHANGED** (8.0 m; (−4.0, 0)) | `arena.json` is byte-identical |
| `TA-X-19 / 20 / 22 / 24` | **CARRIED** | — |
| `TA-X-21` | **CARRIED. Re-verify the live site list at emission** | the oracle code moved again (Q91, C-11a). The site list is a property of the code |
| `TA-X-25` | ⚑ **RE-DERIVED AT THE FIGHT GRAIN** (and re-checked under the C-11a fold: unchanged). (a) carried. (b) carried, and **its counter `n_measured_offense_spawn` is stated by name as a presence condition.** (c) is **re-derived from `u5` and the oracle's own profile predicate** as a per-record partition identity over **SWING-456 / NONSWING-10**. (d) re-derived over NONSWING-10 | § A.3. **Pinning (c) at zero would red a correct port** (Q91 ADDENDUM 1, "For v1.8"), and the non-swinging set is **10 records, not 6** |
| `TA-X-26` | (a)–(d) **CARRIED.** (e) **CARRIED, and labelled as the STATE grain** (the fight grain is SWING-456) | jack-ryan Gate-2 § F INFO. The value reproduces: `0.2468965517` / 17 immune |
| `TA-X-27` | (a)(b)(c) **CARRIED.** (d) **RE-DERIVED, UNCHANGED** (139 / 97) | byte-identical `waves.json` |
| `TA-X-28` | **CARRIED** | a law, not a pack value |
| `TA-X-29` | (a) **RE-DERIVED, UNCHANGED** (193/154 · 527/104; the predicate block is byte-identical). (b)(c) **CARRIED.** (d) **CARRIED at 29**; the new identity-path population is **declared as ceiling `C-k`, not folded in.** ⚑ (e) **CORRECTED and RE-DERIVED**: `3.406 → 3.207764` at w159, `5.418 → 4.980316` at w160. (b) is **carried because v3.6 restates Z5 unchanged** (rowset `c5`; C3 not folded, KP-131) | § A.4. v1.7's `3.406` was walked with the winner surface **OFF** while its P-5 said ARMED. v1.8 walks under **all** P-5 settings, and pool_lift and the C-11a aura removal are now among them |
| `TA-X-30` | **CARRIED.** `d_engage_m` re-derived: **2.4** | `arena.json` is byte-identical |

### 0.3 · Diagnostics, report face, taxonomy

| site | v1.8 | reason |
|---|---|---|
| `TA-B-01` terminal wave | ⚑ **RE-DERIVED reference: `[156, 152, 155, 152, 152]`**, read from the C-11a pricing's v1.8 cell (the FOLDED oracle with pool_lift and the winner surface ARMED; P-n.3). The same cell's unfolded sibling reproduces `[156, 152, 151, 151, 156]`. **The 338 moved no terminal (Q91 pricing). The C-11a fold moved three of five** (§ A.5) | MUST-CARRY 3 |
| `TA-B-15` | ⚑ **RE-POINTED.** It now prints the NO-DATA-labelled count (reference `0` under the oracle's profile predicate) and the **NONSWING-10** body count and fraction. Member-grain reference **10/466 = 0.021459**. The body grain is **owed, not minted** | § A.3 |
| `C-e / C-f / C-i` | ⚑ **RE-DERIVED ON THE LANDED GRAIN.** The folded oracle lands **5,090.3 HP/s over w151–159 = ×3.170** the referent's landed 1,605.6, which is **2,134.1 HP/s per body at N 2.385** (P-n.3). v1.7's `×1.9` and Q91's `×2.031` were **intake-grain** figures against a different referent quantity (2,452). **The two grains are not compared** (§ C.6) | C-11a pricing |
| ceilings | ⚑ **NEW: `C-k`** (identity-path population, 264) · **`C-l`** (mixed edition) · **`C-m`** (the `w43` run-speed MODEL GAP, KP-123) · **`C-m′`** (the `w44` default-attack bodies, inert in the oracle) · **`C-n`** (what the C-11a fold declares and does not fold) | § E.2 |
| § F.5 report face | cl. 7 re-derived · cl. 8 **extended** (a fourth oracle hole, and the C-11a block) · ⚑ **cl. 11 NEW** (the seven holes) · ⚑ **cl. 12 NEW** (mixed edition) | gates nothing |
| § G | the PASS label reads `v1.8 / v3.6`; ⚑ **declared-set closure stated**; ⚑ **§ G.2: the PASS-quoting rule and the seal block (R-9)** | MUST-CARRY 4 |
| verdict file | `prereg_version: "v1.8"`, new `P5_folds` keys, `nodata` extended with `spawn_by_record`, `hole_closure_finding` reference | § G.3 |
| § G.1 counter | ⚑ **`0` of `2` under v1.8** | Matt, KP-115 |

### 0.4 · The counts

| | preconditions | **EXACT** | UNGRADEABLE-declared | DIAGNOSTIC ids | emitted-not-graded |
|---|---:|---:|---:|---:|---:|
| v1.7 | 5 | 28 | 1 (`TA-X-06`) | 19 (0 gating) | 2 |
| ⚑ **v1.8** | 5 | **28** | **1 (`TA-X-06`), closed** | 19 (0 gating) | ⚑ **3** (+ the ten-wave z4 walk, § F.2h) |

⚑ **Q87's *"all EXACT rows green"* at v1.8 means these 28:** `TA-X-01 · 02 · 03 · 04 · 05 · 07 · 08 ·
09 · 10 · 11 · 12 · 13 · 14 · 15 · 16 · 17 · 18 · 19 · 20 · 21 · 22 · 24 · 25 · 26 · 27 · 28 · 29 · 30`.
**The count history, so it never moves silently:** Q87 was ruled over 26 → v1.6 had 29 → v1.7 had 28 →
**v1.8 has 28. No row was added, and no row was removed.** The id namespace does not move: `TA-X-23`
stays struck and retired, and `TA-X-06` stays on record under its own id.

### 0.5 · What was deliberately NOT folded in

1. **The seven holes as EXACT rows** (six at firing, hole 7 at KP-126). No goalpost expansion was ruled. They go through R-series closure
   (§ G.2).
2. **`GM-OQ-1` / `OQ-9`: widening `TA-X-09` to all 29 vectors.** Carried as `C-h`. v1.7 § I said it
   *"should be the FIRST row the next version adds"*, and this is that next version. ⚑ **I am still not
   adding it: v1.8 exists because a substrate moved, and a version that also grows its own instrument
   mixes two kinds of change in one diff.** It stays the first candidate for a version that exists for
   it (§ I, OQ-9).
3. **`TA-X-29(d)` widened to the 264 identity-path records.** Declared as `C-k` instead (§ E.2).
4. **The JOIN-1 golden master.** It is not a v1.8 instrument. It counts as hole evidence only if its PRE
   fixture comes from the Gate-2-passed runtime (jack-ryan, KP-114).
5. **C-11 (the oracle's over-lethality).** C-11a **was** a reference change, and Matt ruled it in before
   this file sealed (KP-127). It is folded into the oracle v1.8 grades against (P-5 setting 11), and
   it is not a row. ⚑ **C-11b (legolas, collab `c2c05bfd3`) landed while this file was held.** It traces
   the monster dex/int lineage to source and finds **two sourced departures, both pointing UP**: (A) the
   record's own `charLevel` equation is dropped, and (B) the +10 % Ultimate/solo attribute modifier on
   the `monsterAttributePak` row is never read. Priced on C-11's decomposition: ×3.162 → ×3.589 for
   A+B. ⚑ **Matt ruled before this file sealed: *"Seal v1 with the gap declared."*** So C-11b is
   **NOT folded**. It is a **declared model gap in the direction of MORE lethality**, and v1.8 carries
   nothing from it (`C-n`). C-11b's sourced A+B folds, and the player-side investigation C-11c
   (devotion procs, Crucible blessings, structures, mutators, tributes), belong to a **REFERENT-v2
   track after the seal**, which v1.8 does not describe.

---

## ⚑ PINS: EVERY PIN RE-DERIVED THIS SESSION BY `shasum -a 256`, NONE RETYPED

> **The standing rule (KP-20, KP-43): a new version re-derives every pin it carries, including the ones it
> believes are unchanged, and prints them in one table.** At v1.8 all **14** carried pins reproduce v1.7
> exactly. **Both pack digests are RE-COMPUTED from their member files** by the manifest's
> `pack_digest_law_exact`, and are not read off the manifest.

| # | artifact | **sha256 (derived 2026-09-30)** | v1.7 → v1.8 |
|---|---|---|---|
| P-a | `gamora/notes/2026-09-20-kc2-play-ta-band-widths.md` (76,464 B). Constructions only; every width VOID | `1c80f08075a1ed0e30e30b348752d2505b39994f7e2c55c348413f6e591248f9` | unchanged |
| P-b | `galadriel/notes/2026-09-20-kc2-play-w1-tb-expected-values-and-u-rider.md` | `d48512aa6e3c9ea70de6675750880a6c8914f0984c3cfe65c6ccb9a24403438f` | unchanged |
| P-c | `…/2026-09-20-kc2-play-w1-tb-expected-values.json` | `a8b85331764ba3fe90f45cf7cd6f1a25f6dc0dae4a7e7fa555c487f0b153ea0b` | unchanged |
| P-d | `…/2026-09-20-kc2-play-w1-tb-release-labels.json` | `15dace604c8d5bb4888223a8b25a07a038bae44431ebd194d682545c0f29c58a` | unchanged |
| P-e | `simulation/math/kc2-play-v3p4-roster-basis-rebase-2026-09-21.md`. **Lineage for `TA-X-25` at v1.8** (governance moved to P-l.q91 + `u5`) | `4b7b78c834c7fbabd61700dda3e730a95ab89990bfa01470e8fb293f41ac7a73` | unchanged; ⚑ **demoted to lineage** |
| P-e′ | `…/math/kc2-play-v3p3-monster-offense-prereg-2026-09-20.md` (lineage) | `27fc59378aee8c9d412f486a63864a3b2ceb5c5473520b60ad80128d47d99cdc` | unchanged |
| P-h | ⚑ **THE MODEL PACK: `kc2-model-pack-v3-E-s09-cp150-mech-v3p6-20260930_045353`** | ⚑ **`4fd353300b96aea2130b88493eb79b902fa846beb6e7866bd4b497013bd94952`**, re-derived from **17** members, 17/17 members verified (digest and bytes) | ⚑ **REPOINTED v3.4.2 → v3.6** |
| P-h2 | ⚑ **THE REFERENCE PACK: `kc2-reference-pack-v3-E-s09-cp150-mech-v3p6-20260930_045353`** | ⚑ **`4e23ffc63902985c99c4dd79403eb3277ab8ca4f8c74d245b4dbc6e4cf90bf60`**, re-derived from **7** members, 7/7 verified. `cross_pin.model_pack_digest` = `4fd353300b96aea2130b88493eb79b902fa846beb6e7866bd4b497013bd94952` ⚑ **verified equal to the derived model digest** | ⚑ **REPOINTED** |
| P-i | `data/kc2/pm4p_leech_resistance.csv` (3,312,159 B) | `cb6a008bde1e102573181968ab7f60958cd28fee07ff8736078fa092a80dd62e` | unchanged |
| P-j | `data/kc2/pm4l_mitigation_by_body.csv` (5,444,380 B). Lineage | `a8c1ffd97dc703419f8447f3d7bbba3903e0f14d2c2e6746a938ceefae9ecec6` | unchanged |
| P-k | `data/kc2/pm2_tg2_monster_timing.csv` (234,541 B). `ANCHOR-169`'s carrier | `58205679e36f0e0361ccd41c844d6bc254ada034447dd1f80e2a46a2b47c7aca` | unchanged. ⚑ **Pinned outright at v1.8** (v1.7: "derived at use") |
| P-l | the seal-lap math notes: `c2` · `c7` · `nine-winner-surface` · `upn4` · `upn5` · `upn5-ADDENDUM` | six digests, printed in full below the table | unchanged |
| ⚑ P-l.q91 | ⚑ **NEW: `simulation/math/kc2-play-q91-338-pool-damage-lift-2026-09-29.md`** (committed ALONE, `2e6f9be5`). **Governs `TA-X-25` and P-5's `pool_lift` at v1.8** | `d68561d59723c3295da3f0456f2fbeaefe8f5f0a30b41d29b5ff0e366966a385` | ⚑ **NEW** |
| ⚑ P-l.q91a | ⚑ **NEW: `…/kc2-play-q91-338-pool-damage-lift-ADDENDUM-2026-09-29.md`** (the pricing, § 2) | `b9ada804e17c01b376e64e82b7e45f66a344d1fc2fc75a0fdd1fd76c56e2cddc` | ⚑ **NEW** |
| ⚑ P-n.1 | ⚑ **NEW: `simulation/output/kc2-play-q91-pool-lift-pricing-20260930_023137.json`** (87,903 B). **`TA-B-01`'s v3.5 re-read** | `f33ce0c0cbeb00bbed7b47a6f7660f20d4aa2be1694f9f4e2486e37d27b553e2` | ⚑ **NEW** |
| ⚑ P-n.2 | ⚑ **NEW: `simulation/output/kc2-lifted-rows-KC2PLAY-SEALLAP-W1-c2-energy-fold-20260928_232836.json`** (90,546 B). **The `x8` artifact that `WinnerSurfaceFold.from_x8` reads for P-5** | `cc361a3fea3e24e55fdf0c8c8eaf52bcc0c729c7de0563d3c84dd0dc21202960` | ⚑ **NEW.** v1.7 wrote `from_x8(…)` without naming its input |
| ⚑ P-l.c11a | ⚑ **NEW: `simulation/math/kc2-play-c11a-oracle-corrections-fold-2026-09-30.md`** (committed ALONE, `b0b041d0`). **Governs P-5 setting 11** | `4af38999ff0544cc9607b34da4fde29fe2c55324e9829894c516cd9837689445` | ⚑ **NEW** |
| ⚑ P-l.c11aA | ⚑ **NEW: `…/kc2-play-c11a-oracle-corrections-fold-ADDENDUM-2026-09-30.md`** (the pricing, `28735961`) | `17a068fe980869e6e344fdf3a652dc275f5cc3a3d65818f2976fe94084d48666` | ⚑ **NEW** |
| ⚑ P-n.3 | ⚑ **NEW: `simulation/output/kc2-play-c11a-fold-pricing-NOT-A-GRADED-RUN-20260930_043045-SUMMARY.json`**. **`TA-B-01`'s v1.8 reference and `C-f`/`C-i`/cl. 7** (`v1p8_seat_cell_pool_lift_winner_surface`) | `b6c9e7953f5b5632ec2dc51c2c8602461aef15d4721f69432444e6f777e1141e` | ⚑ **NEW** |
| ⚑ P-n.4 | ⚑ **NEW: `simulation/output/kc2-play-c11a-landed-by-source-NOT-A-GRADED-RUN-20260930_033242.json`** (engine `d7408a9a`). The per-source census that priced legolas's P1/P2 | `ad018b78a7f85491020a237166af797845bb5de2e562816673fbf925bb41ff1e` | ⚑ **NEW** |
| ⚑ P-o | ⚑ **NEW: `data/kc2/c11a_aura_buff_grants.csv`**. The C2 grant table the fold pins (48 (buff, rank) pairs, 215 rows) | `749d58f45eb312e7a284734a1844f2aabcfd69b7219dd1dafc55e4bb6d64792f` | ⚑ **NEW** |

**P-l in full (re-derived, all unchanged):** `kc2-c2-per-cast-energy-cost-fold-2026-09-28.md`
`b42684e55325bd4caf705b1e7d43462acb5c5818cd5abe3d79eb0d3b9ba6f8c7` ·
`kc2-c7-insufficient-energy-refuse-fold-2026-09-29.md`
`072f9ab787ec840a9bc62ae76a0576fa5db7be0da0b63457851557ea164a7e1f` ·
`kc2-play-nine-winner-surface-reconstruction-2026-09-29.md`
`2c7c3679af67569fff88bb56837ea1ba37499fe9fcbeca85ab63a473b0d7a6dd` ·
`kc2-play-upn4-occupancy-by-pilot-2026-09-29.md`
`787d1a99d9adfedbb34bda69a3c530a653a8df3fc117969e3920c5625791a3cf` ·
`kc2-play-upn5-global-magnitude-fold-lift-2026-09-29.md`
`bfa44b4722ec8b7326987042101f32310c986e3fae489a4372fcc4e0dd5553c7` · `…-ADDENDUM-…`
`5323c1fa9f156e80ced5b1324e4297150cfc759c4e54426f440c33a6c9745fc6`.

⚑ **The Q91 rowset (`kc2-lifted-rows-KC2PLAY-Q91-pool338-damage-lift-20260930_022026.json`, FILE
`82e58985…`) is deliberately NOT pinned.** Its rows sit inside `P-h`'s members (`u1…u8`). Pinning a
lift's intermediate file next to the pack it was cut into pins the same fact twice (the v1.6 `P-f`
rule).

### ⚑ SET DIGESTS: the populations v1.8 grades over, pinned so that nobody re-derives them by phrase

**Law:** `sha256("\n".join(sorted(record_paths)).encode("utf-8"))`, with no trailing newline. Paths are
`records/…/*.dbr` exactly as the pack writes them.

| set | definition (evaluable) | n | sha256 |
|---|---|---:|---|
| **POOL-466** | ∪ `pools.pool_member.member_record` over every `pool_record` that `pools.wave_spawn` references at `global_wave ∈ [151,160]` (109 pools) | 466 | `33c886a11f91db1143c791ffcf9d95f7e7614e423373235231733c994c5c157b` |
| ⚑ **SWING-456** | the POOL-466 records whose oracle profile satisfies `can_swing` (`threat.py:600-604`: `swing_period_s is not None and slots != ()`) under **P-5's loader call** (§ B.6) | 456 | `706a61d55dc6621814fc923d7428c5b263a95ebb00e9786d12f35dd385a7a4c0` |
| ⚑ **NONSWING-10** | POOL-466 − SWING-456 | 10 | `00b4cb0e24b43e591a2e30200979725801aad1e7c1f9b7764ebef67461816e10` |
| ⚑ **FALLBACK-158** | the POOL-466 records whose run-speed multiplier is `FALLBACK_RUN_SPEED` under the sealed stack, meaning **not** in Lap R (`player_locomotion.monster_speeds`) **and not** in band A (`locomotion.locomotion_inputs`) | 158 | `e8114efaa8fa678db6a26bb6e4ffb926fc2c1a15a978e3d589cf918ff17ae6cb` |

### Documents of record (derived here so the next reader does not have to)

| document | sha256 |
|---|---|
| ⚑ prereg **v1.7** (superseded, **not edited**). v1.8's only predecessor | `552d9faecd83d955c77f2be35991ec51e3908d9f586ab70b5a78b6c156b92896` |
| prereg v1.6 (not edited) | `db2c0ca3c6cdba022b83d0229439a3ad9e0709cd25732304ffc979a200be7b0e` |
| ⚑ jack-ryan's **v1.7 pre-read** (`qa/findings/2026-09-29-run-KC2-PLAY-prereg-v1.7-preread.md`) | `ff1df4a18e9e60c1a5543edb391eded667b11711b340cd4763f3cdd204cab1ff` |
| ⚑ **attempt-1 grade note** (`gamora/notes/2026-09-29-kc2-play-ta-grade-v1p7-attempt1.md`) | `9778b4de4aa05acb2396439d2ff9de264ec590475ebf56aec93f3912ba12505e` |
| ⚑ **attempt-1 verdict file** (`…-ta-verdict-v1p7-attempt1.json`) | `9be2d56bfdc49c51c611402ec953b5f59dbfc0c866cdaf5201e0e57d74df08b2` |
| ⚑ **jack-ryan's Gate-2 on attempt 1** (`qa/findings/2026-09-29-run-KC2-PLAY-ta-grade-v1p7-attempt1-gate2.md`). **R-1…R-12** | `d2aa93db92122e033927f63ff61c9e6a2c13e1c7cba09a4fff20cb2382de6c37` |
| jack-ryan's v1.6 pre-read | `5a5f45d76098746ce1dbd31d0091b9a7d62f16978fb52a21ff27990181e0b6c0` |
| the grade of record (`gamora/notes/2026-09-21-kc2-play-ta-grade.md`) | `600f68a7378329c298cd69863903804a6ab7d1ee8a27f666688717f741b9c1c3` |
| the discrimination audit | `852d0bd7d637280cbc42e2ba8494ea7e163b4f6c91741f24eb0ef3da105e674a` |
| divergence register v0.3 (file form) | `5028b555313df2f4690cd96881c700c7d66a4733612894c150c2448915510444` |

### SEALED CELLS: hash-verified this session. K-7 held: never opened for execution, never re-run

| cell | path (`reincarnated-engine/src/reincarnated/simulation/output/`) | sha256 **derived** | bytes |
|---|---|---|---:|
| `[M-POL2]` | `kc2-checkpoint-E-s09-cp150-mpol2-20260825_114420.json` | `ad61ad2a8c799d6ef11a68436756c253f0a34fbb1052e575cdf9f9cd3a44dc5c` | 123,564 |
| `[MECH]` | `kc2-checkpoint-E-s09-cp150-mech-20260816_124031.json` | `20b05cb4ef3bd888b998cbc46c68b41a8051111c12fbcf2066d101b0a4b15f4b` | 2,125,271 |
| `[W1W]` | `kc2-checkpoint-E-s09-cp150-w1walls-20260825_220058.json` | `7a992c81ca6e56e54a53534b438a9ddf87ed42f1bf1a3d0ecc2d2f3c3db7881b` | 403,084 |

**Counts at v1.8:** 5 preconditions · **28 EXACT** · 1 UNGRADEABLE-declared (`TA-X-06`, closed) · 19
DIAGNOSTIC ids (0 gating) · 3 emitted-not-graded.
**Standing law:** Law 3 · K-7 · D4 · GL-6 / GL-7 / GL-12 · the Commission Rule · Disciplines **#1 · #11 ·
#12 · #72 · #75 · #78 · #79 · #84 · #85** · `WARN-16` · digests **derived at use, never retyped**.

---

## § A · WHAT MOVED, DERIVED

### A.1 · The pack, member by member (v3.4.2 → v3.5 → v3.5.1 → v3.5.2 → v3.6)

**v3.4.2 → v3.5 (derived from the member files):** **11 of 17 members are byte-identical.** These are
`ai_states` · `arena` · `config_of_record` · `controllers` · `monster_defense` · `monsters` · `projectiles` ·
`rng_contract` · `summons` · `target_selection` · `waves`. **Six moved:** `math_rules` · `meta` ·
`monster_kinematics` · `monster_offense` · `player_kit` · `provenance`. **All six moves are ADDITIVE
at the top-level-key grain.** A sorted-key comparison of every v3.4.2 top-level key finds each one
content-identical in v3.5. The only exceptions are `meta.json`'s emission-identity fields
(`emitted_at_utc` · `emitted_by` · `headline` · `lap_manifest` · `pack_revision`) and `provenance.json`'s
`absence_registry` (one entry: `ABS-MONSTER-OFFENSE-NO-DATA-POOL466`, carrying KP-122's re-disposition
pointer) and `provenance_registry` (30 → 31 entries: the Q91 lift). The new keys are all `⚑ v3p5_*`: `u1…u3` (offense) · `u4` (kinematics) · `u5` (provenance) ·
`u6` / `u8` (math_rules) · `u7` (player_kit) · the arming block · the edition caveat.

**v3.5 → v3.5.1 (KP-123; `…-v3p5p1-20260930_031425`, the committed cut, engine `fee9c0a4`):** **14 of 17 model members byte-identical to v3.5; 3 moved:** `meta.json` (f3f5c915… → 8bca152d…; changed top-level keys: `emitted_at_utc`, `emitted_by`, `headline`, `lap_manifest`, `pack_revision`; new keys: `⚑ v3p5p1_march_base_ROUTED`, `⚑ v3p5p1_run_speed`, `⚑ v3p5p1_supersession`) · `monster_kinematics.json` (7e61530c… → f7eff09d…; changed top-level keys: none; new keys: `⚑ v3p5p1_grain_law`, `⚑ v3p5p1_rows`) · `provenance.json` (ad768a42… → fc172a98…; changed top-level keys: `provenance_registry`; new keys: `⚑ v3p5p1_precedence_vocabulary`). **Derived from the member files, not from the cut's receipt.**

**v3.5.1 → v3.5.2 (KP-126; `…-v3p5p2-20260930_032822`, engine `e081f3de`):** **13 of 17 model members byte-identical to v3.5.1; 4 moved:** `meta.json` (8bca152d… → ad56177d…; changed top-level keys: `emitted_at_utc`, `emitted_by`, `headline`, `lap_manifest`, `pack_revision`; new keys: `⚑ v3p5p2_march_base`, `⚑ v3p5p2_supersession`) · `monster_kinematics.json` (f7eff09d… → 8ecf4e41…; changed top-level keys: none; new keys: `⚑ v3p5p2_grain_law`, `⚑ v3p5p2_points_to`, `⚑ v3p5p2_rows`) · `player_kit.json` (6db97d07… → aa9d237e…; changed top-level keys: none; new keys: `⚑ v3p5p2_points_to`) · `provenance.json` (fc172a98… → dce46abb…; changed top-level keys: none; new keys: `⚑ v3p5p2_precedence_vocabulary`). **Derived from the member files, not from the cut's receipt.**

**v3.5.2 → v3.6 (KP-127 / KP-131):** **13 of 17 model members byte-identical to v3.5.2; 4 moved:** `math_rules.json` (68378bdd… → 331fd552…; changed top-level keys: none; new keys: `⚑ v3p6_grain_law`, `⚑ v3p6_points_to`, `⚑ v3p6_rows`) · `meta.json` (ad56177d… → 9282f1c1…; changed top-level keys: `emitted_at_utc`, `emitted_by`, `headline`, `lap_manifest`, `pack_revision`; new keys: `⚑ v3p6_c11a_fold`, `⚑ v3p6_supersession`) · `monster_offense.json` (3394db3d… → a7b4e0b7…; changed top-level keys: none; new keys: `⚑ v3p6_grain_law`, `⚑ v3p6_points_to`, `⚑ v3p6_rows`) · `provenance.json` (dce46abb… → e2a531a4…; changed top-level keys: none; new keys: `⚑ v3p6_precedence_vocabulary`). **Derived from the member files, not from the cut's receipt.**

> ⚑ **WHAT THIS BUYS.** `TA-X-10 / 16 / 17 / 18 / 27(d) / 30` are functions of `arena.json` and
> `waves.json` alone, and both are byte-identical across all four cuts (v3.5, v3.5.1, v3.5.2, v3.6). **Each was re-derived anyway:**
> 43.758085029822276 · 54/47 · 8.0 · (−4.0, 0) vs (−5.656854249492381, 0) · 139/97 · 2.4.
> A byte identity proves the input did not move. It does not prove the reading of it was right.

### A.2 · `math_rules.json` moved and the nine vectors did not

The v3.5 digest is `68378bdd…` (v3.4.2: `cc4a9fdb…`). **Every v3.4.2 top-level key is content-identical.
The file gains only `⚑ v3p5_grain_law` and `⚑ v3p5_rows` (`u6_non_health_family_route` ×4,
`u8_pool_lift_law` ×1).** There are still **15 rules** and **29 test vectors**. `TA-X-09` grades the same
9 and `C-h` (the 20 mitigation-order vectors) is carried. **At v3.6 `math_rules.json` is `331fd552dbff6533e1158fe5c2b8716d9ce4ee82eddd924b86914beae1ba42cc`; every v3.5 top-level key content-identical: YES.**

### A.3 · ⚑ THE BODY-STATE TABLE AT THE FIGHT GRAIN: why `TA-X-25(c)` is re-derived, and why its non-swinging set is TEN

**Two grains, and v1.6/v1.7 graded the wrong one.** v1.6 § A.3 counted POOL-466 at the pack's **STATE**
grain (`w45.body_state = MEASURED-OFFENSE`): 464 / 2 / 0. jack-ryan's Gate-2 § B showed that for 338
of those 464 the state grain was a **presence flag with no damage row**. The oracle did not arm them,
so a faithful port had to red `(c)` (F.1a in the opposite direction). **Q91 lifted their damage, and v1.8
re-derives at the grain the fight consumes: the oracle's own profile predicate.**

**Derivation** (oracle at engine HEAD; `threat.load_profiles` called exactly as P-5 names, § B.6):

| population over POOL-466 | predicate (oracle code) | **v3.4.2 oracle** (no pool_lift) | ⚑ **v1.8: P-5 oracle** (pool_lift ARMED) |
|---|---|---:|---:|
| **NO-DATA** | `prof_of[aid] is None` (`run.py:1800`: `engine.roster.get(...)`) | **338** | ⚑ **0** (466/466 profiled) |
| **MEASURED-INERT** | profile present, `not prof.can_swing` (`run.py:3601` skips it) | **6** | ⚑ **10** |
| **MEASURED-OFFENSE** | profile present, `prof.can_swing` | **122** | ⚑ **456** |
| | | 466 ✓ | 466 ✓ |

⚑ **The 334 the pool lift arms are EXACTLY the pack's `u5.outcome == CONSTRUCTED` set** (set equality
verified against the oracle's `can_swing`). `LoadReport.pool_lift_profiles_built = 338`,
`pool_lift_profiles_can_swing = 334`. The pack's arming rule and the oracle agree record by record.

**NONSWING-10, every member named, with the mechanism:**

| record | source | why it cannot swing (oracle) | waves (151–160) |
|---|---|---|---|
| `aetherialimp_a01` | `u5` **CONSTRUCTED-DYING-ONLY** | `slots == ()`. It carries **1 dying slot**, which fires **once on death** if the player is in reach (`run.py` ~2967-2995). ⚑ *Not swinging does not mean dealing no damage* (hole 5's territory) | 155 |
| `bounties/ku_bounty_07` | `u5` **HONEST-FAIL** | WeaponPool + an Edition-II unresolved ref. No slot built | 153 |
| `skeleton_b02_knight` | `u5` **HONEST-FAIL** | rank clamped to table. No slot built | 157 |
| `yetidire_b01` | `u5` **HONEST-FAIL** | damage-less WeaponPool. No slot built | 157 |
| `basilisk_a01` | outside `v20 ∪ w45` (the rebase's class-B construction drop) | `slots == ()`, 2 weapon rows | 152 |
| `yetidire_a01` | outside `v20 ∪ w45` (same) | `slots == ()`, 2 weapon rows | 157 |
| ⚑ `ghost_a01` | ⚑ **`w44` DEFAULT-ATTACK** | ⚑ `slots == ()`, 3 weapon rows, swing period 0.5961 s. **The oracle rides natural-weapon damage ON a slot** (`rows += list(prof.weapon_rows)` inside `if slot.is_weapon_swing`), so a slotless profile never swings | 151 |
| ⚑ `ghost_a02` | ⚑ **`w44`** | same | 151 |
| ⚑ `groblefrost_a01` | ⚑ **`w44`** | same | 153 |
| ⚑ `wendigocannibal_a01` | ⚑ **`w44`** | same | 153, 154 |

> ⚑ **THE FOUR `w44` RECORDS ARE THE FINDING, AND THEY CUT AGAINST AN INSTRUCTION ON THE RECORD.**
> jack-ryan's Gate-2 action for drax read *"Arm the 4 `w44` records from their `v21` rows (rebase G-6)"*,
> and KP-122 counted the fight-grain residue as *"the 4 non-swinging + the 2 residual NO-DATA"*, which is 6.
> **The oracle at HEAD arms none of the four**, with or without the pool lift. `w44` states that they
> are MEASURED-OFFENSE at the upstream grain, and that is true of the game. **It is not true of the
> oracle, and T-A's subject is port ≡ oracle.** A port that arms them reds nothing that v1.7 would have
> seen. At v1.8 it reds `TA-X-25(c)`, **correctly**. The port's own roster code already classes all six
> slotless profiles MEASURED-INERT, *"inert BY THE ORACLE'S ARCHITECTURE"* (`kc2rt_roster.gd` ~926-937).
> The conductor was told before this file was committed, and ruled: do not arm them, or revert.
> ⚑ **Whether the ORACLE should swing a default-attack body is a MODEL question (C-11's, and Matt's). It
> is not a T-A question, and v1.8 does not settle it.** It is declared at `C-m′` (§ E.2).

⚑ **RE-CHECKED UNDER THE C-11a FOLD (setting 11), at engine HEAD:** `load_profiles(…, c11a=C11aLoader(scope=CLASS))` removes 131 aura-buff slots and flips **0 roster `can_swing`** over POOL-466. The only flip is a pet, `chthonianminion_b01_summon`, and pets are not in POOL-466. **SWING-456 and NONSWING-10 reproduce, and so do their set digests.**

⚑ **So `TA-X-25(c)`, re-derived, is a partition identity at the RECORD grain** (§ F.2f): every spawned
body of a SWING-456 record is `measured_offense`, and every spawned body of a NONSWING-10 record is
inert. **The split of the inert bodies between the `nodata` and `measured_inert` LABELS is emitted and
not graded.** The oracle's profile predicate reads 0 / 10. KP-122's disposition reads the four
non-CONSTRUCTED `u5` records under the continuing absence (*"ORACLE spawns inert and counts"*). **Both
readings agree on behaviour, which is the only thing a port can be graded on.** Grading the label would
be the F.1a shape a third time: *a row pinned to a vocabulary choice rather than to the system*.

⚑ **AND THE MEMBERSHIP BIT COMES BACK.** v1.6 recorded that the re-base had *spent* `TA-X-25(c)`'s
one-bit membership test (§ E.1 trap 6: *"wider"*). A per-record partition over SWING-456 ∪ NONSWING-10
= POOL-466 **requires every spawned record to be a POOL-466 member**. Trap 6's **membership** half is
graded again. Its **composition** half is still not graded (§ E.1).

### A.4 · ⚑ `TA-X-29(e)`: z4 RE-WALKED UNDER THE P-5 SETTINGS, AND v1.7's VALUE CORRECTED

**Instrument:** the U-P-N-5 walk **verbatim**
(`simulation/scripts/gamora_kc2_upn5_global_magnitude_lift_2026_09_29.py`: `candidate_records_by_wave`,
`resolver`, `price_record_at_wave`, the `threat.py:1826-1966` arithmetic as the script recorded it at emission; at HEAD the same arithmetic sits at `threat.py:1906-2018`, pre-mitigation). Only the
loader call changes. Its ratio is `Σ(mag × a_mult × (M_inst + own_add) × t_mult) ÷ Σ(mag × M_inst)` over
every `direct` and `leech` row of every **priceable candidate**. Leech is in the denominator and dropped
from the numerator (G3). DoT, PCL and non-health rows are excluded. A **candidate** is every roster,
champion and proxy record of `we.pools_for(w, bonus_spawns_enabled=True)` (the walk's own definition,
**p06 included**). A candidate is **priced** iff it has an oracle profile and a non-zero off-sum.

**Five configurations, one session, one engine HEAD. The attribution is by construction:**

| config | loader call | w159 | w160 |
|---|---|---:|---:|
| A: z4 **as cut** (v3.4.2) | `load_profiles(dot_corrections=True)` | **3.406039** (6 of 21 priced) | **5.418200** (9 of 28) |
| B: + winner surface | `…, winner_surface=from_x8(P-n.2)` | ⚑ **3.423409** (6 of 21) | 5.418200 (9 of 28) |
| C: + pool_lift | `…, pool_lift=pool_lift.load()` | 3.208125 (16 of 21) | 4.968706 (23 of 28) |
| D: + winner surface + pool_lift | `…, winner_surface=…, pool_lift=…` | 3.207764 (16 of 21) | 4.968706 (23 of 28) |
| ⚑ **E = v1.8 P-5** (+ the C-11a loader, CLASS scope) | `…, winner_surface=…, pool_lift=…, c11a=C11aLoader()` | ⚑ **3.207764** (16 of 21) | ⚑ **4.980316** (23 of 28) |

⚑ **THE CORRECTION.** v1.7 printed `3.406` beside a P-5 that said the winner surface was ARMED. **That
value is config A.** With the winner surface armed (B), w159 is **3.423409**. The whole difference is
one record: `korvaakmessenger_02b`, whose campaign rows include the withdrawn `messenger_02_impale`
(z4's off-sum 40,297.515 against the Crucible's 29,575.545). w160 does not move. Seven of the nine
governed records spawn there, and all seven carry slot surfaces that are identical under both modes.
**drax's port walk (godot `6b43cf4`) reads 3.42341, which agrees with B to 5 places.** ⚑ **KP-118
recorded drax's figure as "3.442". That is a transcription slip, and the brief to this author carried
it.** drax's commit and emission probe both read **3.42341**. It is corrected forward here and was told
to the conductor before commit. **Neither 3.442 nor 3.42341 was adopted: the figure is derived.**

⚑ **AND B IS NOT v1.8's TARGET EITHER.** v1.8's P-5 arms the pool lift, which puts **10 more priced
records at w159 and 14 at w160**. All of them are lifted records, and all of them fold (`folds_attr`
and `folds_own` on every priced record at both waves; **none of the 264 identity-path records spawns at
w159/w160**). So the supply-weighted ratio falls to **3.207764 / 4.968706** (config D).

⚑ **AND D IS NOT THE TARGET EITHER, BECAUSE THE ORACLE WAS CORRECTED BEFORE THIS FILE SEALED (KP-127).**
With the C-11a loader armed (E), every `SkillBuff_Passive` row leaves its slot. That removes those rows
from the static supply, including the leech rows the walk counts in the denominator. **w159 does not
move: no aura-buff row is priced there. w160 moves to 4.980316.** Four records change:
`wendigocannibal_h02` / `_h04` / `_h05` (a vampiric-aura leech row leaves the off-sum) and
`nemesis_aetherial_01`. **Config E's `3.207764 / 4.980316` are v1.8's `TA-X-29(e)` targets.** The
per-record table is at § F.2h so the port can localise a miss.

⚑ **WHAT THE STATIC WALK CANNOT SEE, DECLARED.** C2's **grants** (§ B.6 setting 11) are applied at run
time to bodies inside a carrier's radius. They are positional, so no static supply walk can price
them. `TA-X-29(e)` grades the **static** supply of the loader-built profiles, exactly as z4 is defined.
**The grant law is graded by no EXACT row** (§ E.1 trap 11).

### A.5 · ⚑ THE TERMINAL-WAVE EXPECTATION (`TA-B-01`), RE-READ FROM THE SUBSTRATE UNDER v3.5 AND AGAIN UNDER THE C-11a FOLD

**Route 1, the sealed cell (carried, K-7-safe read):** `[M-POL2]` `arms.M-POL-2.terminals` =
**`[156, 152, 151, 151, 156]`**, `player_death` 5/5.

**Route 2, the Q91 pricing (P-n.1), the 338 ARMED, no C-11a fold:** harness `upn4.run`, cell
`SEALED-KMILL | SEP-ON`, salts 0–4. **CONTROL** reproduces W2e: Leg-A deaths `156@5.96 · 152@5.06 ·
151@8.73 · 151@15.18 · 156@6.53`. **LIFT gives the same waves at the same seconds, identical to the
hundredth, on 5 of 5 salts.** The 338 are worth 172 of 992 actor-waves (17.3 %), 364 attacks and
233,620 HP (**2.8 %** of intake), and **zero waves** (P-l.q91a § 2).

**Route 3, ⚑ the v1.8 cell, measured (P-n.3, `v1p8_seat_cell_pool_lift_winner_surface`):** C-11's
harness, cell `SEALED-KMILL | SEP-ON`, Leg B, salts 0–4, **`pool_lift` AND the winner surface ARMED**:

| arm | Leg-A deaths (wave @ s into wave) | landed HP/s, w151–159 | × referent's landed 1,605.6 | per body (N) |
|---|---|---:|---:|---:|
| `PW-BASE` (no C-11a fold) | `156@5.959 · 152@5.061 · 151@8.735 · 151@15.184 · 156@6.531` | 6,012.2 | ×3.745 | 2,617.7 (2.297) |
| ⚑ **`PW-FOLDED`** (C1 + C2 + C4; **the v1.8 oracle**) | ⚑ **`156@7.184 · 152@4.408 · 155@7.020 · 152@7.184 · 152@6.122`** | ⚑ **5,090.3** | ⚑ **×3.170** | ⚑ **2,134.1 (2.385)** |

⚑ **What this settles.** (1) `PW-BASE` arms the winner surface and the pool lift together and reproduces
the sealed terminals exactly. That **measures** what v1.8's first draft argued by construction: neither
the winner surface nor the 338 moves a terminal. (2) **The C-11a fold does move terminals**, on salts 2
and 3 (151 → 155, 151 → 152) and on salt 4 (156 → 152). Removing the aura pulses lowers landed intake by
15.3 %. The grants re-enter as flat damage on covered bodies, and that moves the stream. (3) **No salt
reaches w160 in any arm.** The folded oracle is still over-lethal (×3.17 on the landed grain), so
`C-i` holds.

⚑ **`TA-B-01`'s v1.8 oracle-side reference is `[156, 152, 155, 152, 152]`, `player_death` 5/5.** The
march base (setting 10) is the oracle's own composition in every route above. KP-126 puts it on the
wire and changes no oracle behaviour. **C-11b landed while this file was held (collab `c2c05bfd3`). It reports two sourced departures, both UP (×3.162 → ×3.589 priced). Neither is folded, by Matt's ruling (*"Seal v1 with the gap declared"*; § 0.5 item 5). They belong to REFERENT-v2.**

**`TA-B-01` at v1.8** stays **DIAGNOSTIC, CLASS V, report-only, non-discriminating.** Its printed
reference point becomes the mandatory sentence at § F.3.

### A.6 · Supersession sweep: run against the documents and the substrate

| stale figure hunted | where live | disposition |
|---|---|---|
| **`3.406` as the ARMED-surface z4 at w159** | v1.7 `TA-X-29(e)`, verdict schema `gmag_conformance`, drax's probe expected value | ⚑ **CORRECTED → config A; v1.8 target 3.207764** (§ A.4) |
| **`3.442`** (KP-118) | charter KP-118, and the v1.8 brief | ⚑ **TRANSCRIPTION SLIP.** drax measured **3.42341** (`6b43cf4`). Reported to the conductor |
| **`5.418` at w160** | v1.7 | correct for A and B. ⚑ **v1.8 target 4.980316** (pool lift + the C-11a aura removal; config D's 4.968706 is superseded before commit) |
| **"the 4 non-swinging + the 2 residual NO-DATA" = 6** | KP-122, and the v1.8 brief | ⚑ **INCOMPLETE → NONSWING-10** (§ A.3). The four `w44` records are inert in the oracle |
| **"Arm the 4 `w44` records"** | jack-ryan Gate-2 Action, drax line | ⚑ **CONTRADICTS THE ORACLE** (§ A.3). Routed to the conductor: do not arm them / revert |
| **`NO-DATA 338 → 0` (state grain)** | v1.6 § A.3, v1.7 carried | ⚑ **grain-labelled.** It is true at the STATE grain, where it is a presence flag. At the fight grain the v3.4.2 oracle read 338 NO-DATA, and at v1.8's P-5 it reads 0 NO-DATA + 10 INERT |
| **"~29 % of bodies spawned inert explains the easy port"** | KP-113, attempt-1 grade § 4 | **WITHDRAWN at KP-114 and priced at KP-119: worth 0 waves to the oracle.** Not carried |
| **the oracle's per-body intake `4,822.7` / `×1.967`** | v1.7 `C-f`, § F.5 cl. 7 (*"~1.9× HIGH"*) | ⚑ **SUPERSEDED, AND ON A DIFFERENT GRAIN.** Q91 moved it to `4,979.9` / `×2.031` (intake grain, referent 2,452). The v1.8 oracle is quoted on the **landed** grain: **5,090.3 HP/s = ×3.170**, 2,134.1 per body (P-n.3). **The grains are not compared** |
| **legolas's `P1+P2 at maxima ×1.29`** (C-11a § 5) | relayed to Matt (KP-127 lead-in) | ⚑ **MEASURED at ×2.36–×2.84** by the per-source census (engine `d7408a9a`, `ad018b78…`: retaliation is 8.9 % of landed, aura_buff 26.0 %). The ×1.29 assumed all trash intake was retaliation. **The fold itself priced at ×3.17** (P-n.3) |
| **the port's "~15× LOW on intake per body"** | v1.7 § F.5 cl. 7 | ⚑ **NOT RE-DERIVABLE HERE.** The figure is pre-repair, and seven holes have been repaired since (six in the survival direction, hole 7 in the lethal one). The run prints the port's figure. This file does not assert one |
| **"the 334 armed bodies"** as the fallback-speed population | the KP-123 relay | ⚑ **158, not 334** (§ B.6). 178 of the 334 ride band-A speeds. Reported to the conductor. **star-lord's v3.5.1 cut independently agrees (K1 180 / K2 158)** |
| **monster speed = multiplier × `v_ref` 4.0** | the port (`v_ref_param`), `V3-SPEED-1`'s phrasing | ⚑ **the oracle composes against `march_base` = 3.209466 m/s** (§ B.6 setting 10). Routed by star-lord to the conductor. **Recorded here, not ruled** |

---

## § B · CONFIGURATION AND PRECONDITIONS: five

### B.1 · `ORACLE`: `V0`, five arms, five salts *(carried from v1.7 § B.1 in full)*

`V0` carries five `V0-ARM-*` rows: `M0`, `M-POL-2`, `M-POL-2-NULL`, `W1`, `W1-NULL`. Each is a **DELTA
against the base row set, with exactly one fold moved**. **5 × 5 = 25 headless runs.** `W1-NULL` returns
to `M-POL-2` (`TA-X-04`). Limbs of record: `spawn_fold: POLAR_UNIFORM_RHO` · `sustain: COUPLED` ·
`intake: ARMOUR_THEN_RESIST + global_flat` · `summons: PRESENT_INERT + offense MEASURED_BASIC` ·
`arena_fold: None` (armed only in `W1`) · `interrupts_fold: None` · `WarCryLimb.COOLDOWN` (7.5 s) ·
`PotionLimb.TRACE_CONSISTENT` (θ 0.22972972972972974) · `CritLimb: LO` · **`p06: OFF`** ·
`PhaseModel: ENGAGE`. The runtime prints its **resolved** limb set (`v0_limb_set`), diffs it line by
line against `V0` before any row is read, and **refuses to boot on an unset limb.** **Pilot:**
`DRIVE_TO_PACK` + the M-POL-2 channel policy; `v_ref = 4.0` → 5.4 m/s; no facing model; motion law
`V0-04`. The body halt is graded at `TA-X-30`. **Declared fight scope: waves 151–160.**

### B.2 · `P-1` · COVERAGE 89/89 *(carried)*

All **89** census ids are mapped mechanically to exactly one of `IMPLEMENTED` · `DIVERGENCE(DIV-nn)` ·
`RUNTIME-CHOICE(absent_ref)` · `OUT-OF-SCOPE`, with zero unmapped (graded as `TA-X-02`). **Clauses carried
unchanged from v1.7 § B.2:** (1) `P-1` gates COMPLETENESS, not TRUTH (`M4`, `M10`, `D16`); (2) the refusal
count is emitted; (3) cl. 1a: every `IMPLEMENTED` mapping graded by an EXACT row names that row;
(4) **read the four-way COUNTS off the run, never off this document.** ⚑ **At v1.8 the seven hole repairs
may move census mappings, for example the slot-choice and slot-gate rows. The count is the run's
fact.** (5) `CHARTER_DENOMINATOR` rename still owed (`OQ-7`).

### B.3 · `P-2` · STREAM DISJOINTNESS *(carried)*

Probe: `M-POL-2` salt 0 run twice, once with a zero-draw no-op fold inserted. The digests must be
identical. **Covers** fold-granularity isolation. **Does not cover** site order, board-roll composition,
or lifted-vs-chosen assignment. ⚑ **A within-epoch probe (§ C.7).** **`P-2` red → `TA-X-03…05`
UNGRADEABLE → `INDETERMINATE`.** `TA-X-06` is declared and enters no antecedent.

### B.4 · `P-3` · ROLL POPULATION AND ROLL LAW *(carried; cardinalities re-derived)*

| id | n | re-derived from |
|---|---:|---|
| ROSTER-790 | 790 | `P-i`'s `record` column (+1 declared-absence key `krieg_aethertrap` ⇒ 791 keys; GL-12) |
| **POOL-466** | **466** | `P-h`'s `waves.json`, 109 pools over waves 151–160. **Set digest pinned** |
| ANCHOR-169 | 169 | `P-k` |
| BOTH-128 | 128 | `ANCHOR-169 ∩ POOL-466` |

**Roll law:** **WEIGHTED** by `pool_weight` at the pool-alternative stage (`wave_engine.py:974`);
**UNIFORM** at the name stage (`:849`, `:869`). The port implements the ORACLE's law. **`P-3` red →
`INDETERMINATE`.** ⚑ At v1.8, `TA-X-25(c)`'s per-record partition **behaviourally checks membership
again** (§ A.3). It still does not check composition.

### B.5 · ⚑ `P-4` · PACK IDENTITY: both v3.6 packs and the cross-pin

```
model_pack_dir       : "kc2-model-pack-v3-E-s09-cp150-mech-v3p6-20260930_045353"
model_pack_digest    : 4fd353300b96aea2130b88493eb79b902fa846beb6e7866bd4b497013bd94952   (17 members)
reference_pack_dir   : "kc2-reference-pack-v3-E-s09-cp150-mech-v3p6-20260930_045353"
reference_pack_digest: 4e23ffc63902985c99c4dd79403eb3277ab8ca4f8c74d245b4dbc6e4cf90bf60   (7 members)
cross_pin_verified   : reference.manifest.cross_pin.model_pack_digest == model_pack_digest
```

| # | `model/` member | sha256 (derived) | bytes | v3.5.2 → v3.6 |
|---|---|---|---:|---|
| 1 | `ai_states.json` | `928ded88e74e636422cbc107bdb02ff4cf27521dc74636e5e7e0e1680bd6060e` | 2,497 | identical |
| 2 | `arena.json` | `e65b7da05e87028136e616ad5f7391ca88cb1ae4db3956fc679c1cf0008f3ba6` | 12,932 | identical |
| 3 | `config_of_record.json` | `d34ce0d8d5546ac7de5ab6ea6b30bc5dfae6460c078643d90c54a9209b78ebc4` | 26,909 | identical |
| 4 | `controllers.json` | `b4217daac06f2f55acb3ec68571dd7766d31ac156ee01ee903b721f26042e478` | 5,384,891 | identical |
| 5 | `math_rules.json` | `331fd552dbff6533e1158fe5c2b8716d9ce4ee82eddd924b86914beae1ba42cc` | 178,484 | ⚑ **MOVED** |
| 6 | `meta.json` | `9282f1c1903858c403f760498f1261266ea6587137b292534c644c3b5182c14b` | 73,716 | ⚑ **MOVED** |
| 7 | `monster_defense.json` | `00ffab1576577164cc132b498817d5480822df3234f3f3bcf286c0a407193aac` | 8,816,113 | identical |
| 8 | `monster_kinematics.json` | `8ecf4e418b0896ae49d358bcdaec548fb88d01fd518109b048ad77b1c3b00aee` | 947,176 | identical |
| 9 | `monster_offense.json` | `a7b4e0b784ad182f3803d0641b8804c9434a78e9772ea0fcd07e5cb72f54c800` | 17,326,748 | ⚑ **MOVED** |
| 10 | `monsters.json` | `3839322955b7d4af0a6c8c8b169656136a0271a7ab9bb68893a272df703701a0` | 15,211,150 | identical |
| 11 | `player_kit.json` | `aa9d237ef63d15b2ebd15257688b841dd5e15e3feb3433ff8bca4a8f48da97ab` | 102,797 | identical |
| 12 | `projectiles.json` | `ed32ff8a648d2b3c24918cd20150f27856b371e2a45a0e699cc1c8b6c949a0e5` | 74,198 | identical |
| 13 | `provenance.json` | `e2a531a49c7ecf3fd6ea6d462f208fe8f9cd64ebfb1cf850d575afd866112343` | 646,197 | ⚑ **MOVED** |
| 14 | `rng_contract.json` | `ff6f77b0d54037f61847ab7785b58db324a7a0294d666c952b85fc955127a308` | 31,824 | identical |
| 15 | `summons.json` | `6a7cc5af2bd7291b46c1beafedf2e13b70990a3f9a1a194f2092c1a64e586a93` | 111,259 | identical |
| 16 | `target_selection.json` | `e1df3cf69d2f3f91cce5ab5f9a71de4b7be4fb2372d18de2cc99517d399d68ce` | 31,936 | identical |
| 17 | `waves.json` | `38c43a9c3b35560a3dce88ac16c189cb03b120b1ba2085ae2458040113621072` | 1,087,499 | identical |

**Reference pack (7):** `acceptance.json` `f5ce2c174cccf9a253603ac8bfc3f20b872b2e2a92c8d24e461601e64f1f9853` (4,716 B) · `actors.json` `ef03536f97fe7122e14b34ae69a26bc7616fe58fcbe5989ab3aa09e7420ea04b` (1,956,876 B) · `meta.json` `874ba27250ff29937d4c859175d26b22ae9c3feee0008bcaad34157b811d5fa2` (54,740 B) · `rng_tape.json` `607bf3bffd6a5a330d2ede97eebcd7139f3c218292954aa56fbf38c34e833ea0` (406 B) · `skill_interrupt_reference.json` `45522df26b1703ac2489d08e7e7fa6986255ca80e64f057279ca6b492fdf3707` (3,113 B) · `tracks.json` `bb3495218fcdeaab11d4d5e9a5d25a2e14f2fd21384bcebc7dd1f93b0b7d9bfd` (44,733 B) · `u7_heading_conditioning.json` `5ad6ab0f089d3409506f29293433849f6abcbd1bee2a2242344fe12367287c05` (3,601 B)

⚑ **Every digest above was derived this session. The two PACK digests were re-computed from the member
list by the manifest's `pack_digest_law_exact`.** A mismatch on any of them is **`C1`** and the cap
trips. ⚑ **v3.5 (`ba50f8b0…` / `4d23fe84…`), v3.5.1 (`95d9a614…` / `ba527a07…`) and v3.5.2 (`58e6b687…` / `a75b0a3c…`) are NOT the pack of record.** A run on any of them is `P-4` red.
⚑ **What the grader checks first: the `.app` / runtime header's `pack_digest`, read by RUNNING the
binary.** The attempt-1 runtime reported v3.4.2 (`5cab7433…`). Until drax's v3.6 pass lands, `P-4`
is red, and that is scheduled work, not criticism.

### B.6 · ⚑ `P-5` · THE ORACLE FOLD SETTINGS: ELEVEN, EACH WITH ITS SOURCE

**The graded run declares every one in its header, and the loader refuses to boot on an unset one.**
⚑ **Line numbers are at engine HEAD `96b4529a`** (the C-11a commits moved `run.py` and `threat.py`). Rows 4–6 carry v1.7's citations, which were made at engine `29a66055`.
⚑ **The oracle at engine HEAD `96b4529a`, configured exactly as below, is the reference v1.8
grades against.** The sealed cells ran with `winner_surface` and `pool_lift` OFF. v1.8's reference is a
**sibling, re-derived forward, and not a re-grade** (x9 `SIBLING_NOT_REGRADE`; K-7).

| # | setting | site | default | ⚑ **T-A RUNS UNDER** | source |
|---|---|---|---|---|---|
| 1 | ⚑ **the loader call** | `threat.load_profiles(…)` | — | ⚑ **`load_profiles(dot_corrections=True, pet_special_gates=None, winner_surface=WinnerSurfaceFold.from_x8(P-n.2), pool_lift=pool_lift.load(), c11a=C11aLoader(scope=AuraScope.CLASS))`**. `dot_corrections=True` is the sealed runner's own argument (`make_runner`, `gamora_kc2_w1w2_lift_build_2026_08_25.py:125`). ⚑ **v3.6's `d1_dot_corrections_partition` (21 rows) puts the ON side of that argument on the wire** for the 5 roster records whose `v20`/`v21` rows were lifted OFF, restating each replaced row by name (`⚑ v3p6_points_to.d1_restates`). **A port reading only `v20`/`v21` would run those 5 records on the OFF side, which is not the oracle's side.** | v1.7 wrote the fold settings and **not the call**. The call is the thing a builder reproduces |
| 2 | **the winner surface (the nine)** | `winner_surface.py` | `None` = OFF, byte-inert | ⚑ **ARMED** (carried) | `winner_surface` MIGRATION § 2; KP-97. ⚑ *The input is now named: `from_x8` reads P-n.2 (`cc361a3f…`), rowset `x8_nine_campaign_attack_relift`, cardinality 9* |
| 3 | ⚑ **the Q91 pool lift** | `pool_lift.py` → `load_profiles(pool_lift=…)` | ⚑ **`None` = OFF, byte-inert** (a field-by-field inertness test) | ⚑ **ARMED: `pool_lift.load()`, digest-verified supplement, 338 records.** Result: **466/466 POOL-466 profiled · SWING-456 · NONSWING-10** (§ A.3) | ⚑ **Matt Q91 (KP-115); P-l.q91; pack `⚑ v3p5_pool_arming` (`ARM iff u5.outcome == CONSTRUCTED`), which the oracle matches record for record** |
| 4 | **C-2 · per-cast energy cost** | `per_cast_energy.py` · `CostColumn` | no default (a TYPE) | **`PARENT_PLUS_MODIFIER`: `43.20 / 27.90 / 106.20 / 59.40`** (carried) | KP-84 (L1) · KP-89 · KP-98 |
| 5 | **C-7 · insufficient energy** | `per_cast_energy.refuses_activation` | `REFUSE` (flipped; #12) | **REFUSE, `regen_ungated = true`** (carried) | KP-90 · KP-95 |
| 6 | **the global-magnitude fold** | `run.py:1661 / :1690-1691`; `threat.py:1826-1836` | armed unconditionally | **ON, unconditional; `monster_measured_board` attached ⇒ attribute limb 344/344** (carried) | KP-100 · KP-101 |
| 7 | ⚑ **the PCL limb** | `intake.py:151 PCL_DEFENCE_PCT = 26.0`; `PclLimb.MULTIPLICATIVE` | inherited **by omission** | ⚑ **`MULTIPLICATIVE`, 26.0, read by the port from the pack's `u7_pcl_defence` row (fail closed).** 26.0 is graded **MEASURED** (Lap X, Rebuke r11). The limb is graded **DECLARED-MODEL-LIMB**, a default by omission, labelled as such | KP-115 ruling; KP-119; pack `u7` (`U7-0`) |
| 8 | ⚑ **the non-health route** | `threat.py:209` (`SlowManaLeach`) + `:231` `DECODED_NON_HEALTH_TYPES = {ManaBurnDrain, Disruption, PierceRatio}`, `:1911-1919` | **unconditional** at HEAD | ⚑ **ON.** The row leaves the health path **after** its chance draw (stream untouched) and is **counted** in `non_health_by_type`. **Any other unmapped family still RAISES** (GL-12, `threat.py:312`) | P-l.q91 (semantic shift, named); pack `u6` (4 rows) |
| 9 | ⚑ **monster run speed: the population** (KP-123) | `run.py` ~1510-1532; `locomotion.locomotion_for` (`FALLBACK_RUN_SPEED = 1.000`, `locomotion.py:67`); `player_locomotion.PlayerLocomotionFold(monster_speed_fold=True)` | the sealed stack arms Lap R (`gamora_kc2_pm4_i26_…py:459`) | ⚑ **As the oracle derives it over POOL-466: `LAP-R-MEASURED` 128 · `BAND-A-DB-CITED` 180 · `FALLBACK_RUN_SPEED (1.000)` 158.** ⚑ **All 158 fallback records are in the 338 (156 CONSTRUCTED + 2 HONEST-FAIL). The 180 band-A records are also all in the 338 (178 CONSTRUCTED + 1 DYING-ONLY + 1 HONEST-FAIL). The incumbent 128 are all Lap R.** Set digest: FALLBACK-158 (§ PINS). ⚑ **On the wire (v3.5.1 rows, carried in v3.6):** `monster_kinematics.json :: ⚑ v3p5p1_rows :: k1_banda_run_speed` (180 rows) · `monster_kinematics.json :: ⚑ v3p5p1_rows :: k2_fallback_run_speed` (158 rows) · `monster_kinematics.json :: ⚑ v3p5p1_rows :: k3_run_speed_law` (4 rows). **The port reads the law and the population from these rows; the oracle's derivation above is the check.** | ⚑ **KP-123.** The law and the population come from the oracle, not from "the 334" |
| 11 | ⚑ **THE C-11a CORRECTIONS** (KP-127) | `kc2/c11a_corrections.py`; loader `load_profiles(c11a=…)` (`threat.py:1011-1032`); runtime `simulate_wave(c11a_corrections=…)` (`run.py:1093-1095`, `:1694-1706`); `ThreatEngine.c11a` (`threat.py:1515-1520`) | ⚑ **`None` = OFF, byte-inert** (a fold-OFF digest test) | ⚑ **C1 `retaliation_gate=True`** (keyed on `template_group`; population **measured 0**, byte-identical) · ⚑ **C2 `aura=C11aLoader(scope=CLASS)`**: every row whose own `skill_class == SkillBuff_Passive` leaves its slot (131 carrier slots, 157 rows) and its grants apply to covered bodies (radius `skillTargetRadius` of the buff record, centre-to-centre, carrier covers itself). **D-C11a-1, DECLARED: active while the carrier is alive and on the board. D-C11a-2, DECLARED STACKING RULE: one instance per buff record per covered body; different buff records add** (`stack_same_buff=False`; `S-AURA-STACK` is a sensitivity, not of record). The grant table is `data/kc2/c11a_aura_buff_grants.csv` (P-o) · ⚑ **C4 `duration_divisors=True`** (dex/215, int/200; population on the oracle's arithmetic **measured 0**, byte-identical) · ⚑ **C3 (own-% composition) NOT FOLDED: HALTED, conductor ruling KP-131.** Z5 is restated unchanged (v3.6 rowset `c5`) and routed as C-11a-R3 · the DoT attribute scope is **routed** (C-11a-R4), not folded · `S-AURA-SUFFIX` is a sensitivity, not the scope | ⚑ **Matt KP-127; P-l.c11a; P-n.3; v3.6 rowsets `c1…c6`** |

> ⚑ **Settings 1 and 3 are the reason P-5 exists.** Each is default-OFF and byte-inert when off, so
> forgetting one produces no error, no counter and no digest change. **With `pool_lift` OFF the oracle
> reads 338 NO-DATA and 122 swinging, and a port faithfully arming the 334 reds on every arm.** With
> the winner surface OFF, w159 reads 3.406 instead of v1.8's 3.207764. **With the C-11a loader OFF, w160
> reads 4.968706 instead of 4.980316, and the aura pulses fire as damage.**
>
> ⚑ **Setting 9 is on this table because the port would otherwise have left the lifted bodies
> STATIONARY** (drax, KP-123). A body with no speed stands in place. The law existed only inside the
> oracle. **v3.5.1 put it on the wire (carried into v3.6), and v1.8 names its population, so that a port reading the
> wire and the oracle's own derivation are checkably the same set.** ⚑ **Independent agreement:
> star-lord's `K3-2` partition row carries recordset digests derived by his own emitter, and they equal
> this file's: POOL-466 `33c886a1…` and FALLBACK-158 `e8114efa…`.**
>
> ⚑ **Setting 10: THE BASE THE MULTIPLIER COMPOSES AGAINST, AS THE ORACLE RUNS IT.** The oracle's
> monster speed is `multiplier × march_base`. `run.py:1237-1238` sets `march_base = v_ref if patrol_fold
> is None else patrol_fold.march_base_m_per_s(v_ref)`. The driver of record arms
> `PatrolFold(px_arm=LO, cyclic=True, march_base_fold=True)` (`gamora_kc2_pm4_i26_…py`, beside setting
> 9's fold), so **`march_base = patrol.MARCH_BASE_M_PER_S[LO] = 3.209466 m/s`** (`patrol.py:99-100`),
> **not** `v_ref = 4.0`. A body at 1.000 walks at **3.209466 m/s** in the oracle. ⚑ **This number is on
> no v3.5.1 member** (star-lord MIGRATION § 4, `meta.json :: ⚑ v3p5p1_march_base_ROUTED`), and the
> attempt-1 port binds 4.0 (`kc2rt_fight.gd :: v_ref_param`): **×0.8024 on every monster and monster
> pet.** ⚑ **KP-126 (conductor): v3.5.2 carries it on the wire (carried into v3.6).** ⚑ **On the wire (v3.5.2 rows, carried in v3.6):** `monster_kinematics.json :: ⚑ v3p5p2_rows :: k4_march_base_law` (3 rows). **T-A runs the port
> against the oracle's base, 3.209466 m/s, read from that row and failing closed. The player's speed is
> untouched** (`march_base_m_per_s` is never consulted for the player; `patrol.py:214-224`).
> ⚑ **No EXACT row grades monster speed** (`TA-X-30` grades the halt distance, not the approach rate).
> **A port running 4.0 reds nothing in this instrument.** It is a port≠oracle item of the same class as
> the six holes, and **the conductor named it HOLE 7 at KP-126**; drax repaired it with a fail-first
> probe (godot `000608c`, KP-130). **It is seal-relevant through the hole-closure finding (§ G.2), never
> through a row this file mints.** It is printed on the face
> (`P5_folds.monster_march_base.port_m_per_s`, § G.3) so that it cannot be silent.
>
> **The honest limit on the pilot axis (carried from v1.7 § B.6):** T-A compares port and oracle under
> the same scripted pilot, so the occupancy question does not reach T-A. It reaches T-C.

---

## § C · THE LAWS

**C.1–C.6: carried BY REFERENCE and unchanged** from v1.7 § C (pinned `552d9fae…`): the denominator law
`D_constructed = CHANNELLING + CHANNELLING_AND_MOVING + MOVING + IDLE` (2783 on `[M-POL2]`) · the two
`TA-X-08` identities · mean-of-salts, never pooled · the compared object and its (void) construction ·
T-B's own denominators · the BODY denominator class · **THE GRAIN LAW**. A grader applies them exactly
as v1.7 prints them.

### ⚑ C.7 · THE EPOCH LAW, EXTENDED

> ⚑ **A `v3.3` board, a `v3.4.2` board and a `v3.6` board are pairwise NOT draw-comparable at a
> fixed salt. No row, no diagnostic and no report line may compare across them.**

**The v3.6 mechanism, stated before anyone measures it.** 334 more records swing, the aura-buff slots are gone (C2), and covered swings draw their granted rows' chance. Each swing reaches
`choose_slot` and the per-row **chance draws** (`threat.py:1906`: `self.rng.uniform(0.0, 100.0)`).
Hole 6's repair makes the port draw them too. **The stream therefore moves at the first opportunity a
lifted body gets.** A fixed salt fixes the seed and not the board. **`substrate_epoch = "v3.6 / model
4fd35330… / reference 4e23ffc6…"`** for everything graded under this document. Attempt 1's
cells (v3.4.2) are **not priors** and are not compared.

### C.8 · THE HONEST-`n` LAW *(carried verbatim from v1.7 § C.8)*

The 25 cells are 5 salts × 5 single-fold arms. On any dimension the moved fold does not touch, the
effective `n` is **5**. Every aggregate prints its effective `n`. `ddof = 1`, `df = 4`. The draws are
also clustered (median 3 bodies per pick, max 9).

---

## § D · ROW-ID CONCORDANCE

**Carried BY REFERENCE from v1.7 § D, with three governing-document changes:**

| canonical | statistic | ⚑ **construction governed by, at v1.8** |
|---|---|---|
| `TA-B-01` | terminal wave | `[M-POL2]` `terminals` **+ P-n.1 (the LIFT arm)** · REPORT-ONLY |
| `TA-B-15` | inert spawn count / fraction | ⚑ **P-l.q91 + § A.3 (RE-POINTED)** |
| `TA-X-25` | the spawn partition | ⚑ **P-l.q91 + pack `u5` + the oracle's profile predicate (§ A.3, § F.2f)**; `P-e` demoted to lineage |
| `TA-X-29` | the global-magnitude fold | pack `PRED-GMAG-WHOLE` + `Z5-LAW` + ⚑ **§ A.4's config-D walk (for (e))** |

---

## § E · OUTSIDE T-A'S REACH

### E.1 · The traps *(v1.7 § E.1 carried; three move)*

| # | trap | caught by | ⚑ **at v1.8** |
|---|---|---|---|
| 1–5, 7, 8 | *(carried: arrival telemetry · the dead scatter at the same stream position · point vs disc · the non-neutral cadence law · flag AND coin · the attack PHASE · a declared join with no implementation)* | `TA-X-19 / 17+18 / 20 / 21 / 22 / 24 / 26` | as v1.7 |
| **6** | **THE BOARD ROLL** | `P-3` + `TA-X-27` + ⚑ **`TA-X-25(c)`** | ⚑ **NARROWER AGAIN: MEMBERSHIP IS GRADED** (the per-record partition, § A.3). **Composition is still OPEN.** 12 of 29 live draw sites are the board roll |
| 9 | a declared fold with a PARTIAL implementation | `TA-X-29` | carried |
| 10 | a fold left at its default | `P-5` | ⚑ **WIDER SURFACE: 2 default-OFF folds** (winner surface, **pool lift**) and the loader call |
| ⚑ **11** | ⚑ **NEW: PORT ≠ ORACLE ON THE ATTACK-SELECTION PATH.** Six holes (PCL dropped · death after heal · 28 % of damage rows unreachable · `tree_attack` slots never chosen · dying slots mishandled · slot chance/cooldown/delay never read). **All six are invisible to every EXACT row.** Nothing in the graded set EXECUTES attack selection against the oracle (KP-120). ⚑ **Hole 7 arrived with the substrate: the monster/pet march base (3.209466 vs the port's 4.0), named a hole by the conductor at KP-126 (§ B.6 setting 10). And one more item of the same class has no hole number: the C-11a GRANT LAW (coverage, stacking, the weapon-swing rider, the resistance grants; KP-127; setting 11). drax routed that the port has no aura phase (KP-130).** Whether the grant law joins the hole-closure set is the conductor's decision. This file does not add it | ⚑ **no EXACT row, by ruling.** The R-series closure (§ G.2) | ⚑ **SEAL-BLOCKING, NOT VERDICT-BLOCKING.** The JOIN-1 J-S8 fixture is the instrument that closes the class. It counts only if frozen from the Gate-2-passed runtime |

### E.2 · DECLARED CEILINGS

**`C-a`, `C-b`, `C-c` (struck), `C-d`, `C-g`, `C-h`, `C-j`, S5: carried from v1.7 § E.2 as written.**
`C-b` still holds: no cell was minted over 156–160 (K-7). Re-derived and new:

| # | ceiling | status at v1.8 |
|---|---|---|
| **C-e** | `TA-B-12` (intake / leech) has no oracle side in the seals | **HOLDS.** Answered off-seal: the folded oracle kills the player at **152–156** on salts 0–4, with no salt reaching w160 (§ A.5) |
| **C-f** | the leech/intake surplus | ⚑ **RE-DERIVED ON THE LANDED GRAIN.** The folded oracle lands **5,090.3 HP/s = ×3.170** the referent (w151–159), **2,134.1 per body**. The port side is **not re-derived** (seven holes repaired, no graded emission) |
| **C-i** | the oracle is over-lethal against the referent, and T-A cannot see it | ⚑ **HOLDS, reduced by the fold: ×3.745 → ×3.170** landed (C-11a C2; P-n.3). C-11 decomposed it. C-11a was **folded by Matt's ruling (KP-127)**. C-11b (landed; two sourced departures, both UP, ×3.589 priced) is **not folded, by Matt's ruling (*"Seal v1 with the gap declared"*), and is deferred to REFERENT-v2**. **Any further reference change is Matt's HALT** |
| ⚑ **C-k** | ⚑ **NEW: 264 POOL-466 records (all in the 338) take the global-magnitude IDENTITY path.** No Lap M / Lap O term covers them: no attribute multiplier, no own term, no clamp. 55 % of the 338's lookups (643/1,174) | ⚑ **GRADED BY NO EXACT ROW.** `TA-X-29(d)` is carried at the declared 29. `TA-X-29(e)`'s waves (159/160) contain **none** of the 264. ⚑ **A port that INVENTS supply for them reds nothing.** The port **prints** its ten-wave walk (emitted-not-graded, § F.2h), with the oracle's config-D values beside it. **Widening `(d)` is a separate change for a separate version (§ I, OQ-11)** |
| ⚑ **C-l** | ⚑ **NEW: MIXED EDITION.** The 338 were lifted from the **Edition-II** depot and the incumbent at Edition-III. On the covered set the skill surface runs higher on 41/566 skills (median ×1.235 on the differing rows, range ×0.7107–×1.9983) | ⚑ **HARMLESS TO T-A BY SYMMETRY:** port and oracle read the same `u2` rows. **A T-C exposure** (the board over-reads HARDER on ~7 % of skills). Declared on both packs' faces. § F.5 cl. 12 |
| ⚑ **C-m** | ⚑ **NEW (KP-123), a MODEL-GAP CARRY: the 338 carry MEASURED upstream `characterRunSpeed` in v3.4 `w43_monster_timing_upstream` (monster_kinematics), which the oracle does NOT consume.** Over FALLBACK-158, `w43` reads median 1.0, range **0.66–1.55**, and only **80/158** are exactly 1.0. The oracle runs all 158 at 1.000. (Over the 180 band-A records, `w43` agrees with band A **180/180**) | ⚑ **HARMLESS TO T-A BY SYMMETRY** (both sides run the oracle's law). **It is C-11's territory, not a v1.8 goalpost.** Declared so the next reader does not mistake the fallback for a measurement |
| ⚑ **C-m′** | ⚑ **NEW: the four `w44` default-attack records are MEASURED-OFFENSE upstream and INERT in the oracle** (slotless profile; § A.3) | ⚑ **A MODEL question (C-11 / Matt), not a T-A one.** T-A grades port ≡ oracle, and v1.8 grades them inert |
| ⚑ **C-n** | ⚑ **NEW (KP-127): WHAT THE C-11a FOLD DECLARES AND DOES NOT FOLD.** Monster retaliation is **absent** from the oracle (C-11a-R1; direction UP). Grant families are **DECLARED ABSENT**: `defensiveElementalResistance` expansion, per-type `offensive<T>Modifier`, `offensiveCritDamageModifier`, speed/OA/DA, `damageAbsorptionPercent`, life. **C3 is HALTED** (R3), and **the DoT attribute scope is routed** (R4). The mechanisms are **Edition-IV (post-referent)** and the values are Edition-II | ⚑ **HARMLESS TO T-A BY SYMMETRY** (both sides run the folded oracle's law). **A T-C / C-11 exposure.** § F.5 cl. 8 prints them |

---

## § F · THE GRADED ROWS

### F.1 · Decisiveness classes *(carried verbatim from v1.7 § F.1, including `F.1a`)*

**EXACT:** an identity, invariant, count or declared-precision reproduction. A red says **the port is
wrong**. It may carry a **numerical** tolerance and **never a statistical** one. **The EXACT set is the
entire instrument.** **DIAGNOSTIC:** gates nothing, trips no cap, and counts in no PASS label (F5).
**STRUCTURAL-ZERO / NON-ZERO:** name the mechanism that makes the other value impossible. **`F.1a`:** name
whether that mechanism belongs to the SYSTEM or to OUR DECODE'S COMPLETENESS. If it belongs to the
decode, the row carries an **expiry**.

### F.2 · EXACT rows: 28, plus `TA-X-06` UNGRADEABLE-declared (on record, closed)

*Every assertion is restated here, so a grader holds one file for the rows.*

| id | statistic | basis | tolerance | v1.8 | expiry |
|---|---|---|---|---|---|
| `TA-X-01` | port self-determinism: any arm/salt run twice gives an identical digest. **The arm+salt is NAMED and MUST DIFFER from `P-2`'s** (`M-POL-2`, salt 0) | run-internal | byte-exact | CARRIED | none |
| `TA-X-02` | **coverage 89/89**, zero unmapped | census | integer | CARRIED | a census amendment |
| `TA-X-03` | inertness A: `port(M-POL-2-NULL, s) ≡ port(M0, s)`, all 5 | `[M-POL2]` | byte-exact | CARRIED IN FORM | digests move (§ C.7) |
| `TA-X-04` | inertness B: `port(W1-NULL, s) ≡ port(M-POL-2, s)`, all 5 (**not `M0`**) | `[W1W]` | byte-exact | CARRIED IN FORM | as above |
| `TA-X-05` | distinctness C: `port(M-POL-2, s) ≢ port(M0, s)`, ≥ 1 salt | `[M-POL2]` | exact, one-sided | CARRIED IN FORM | as above |
| `TA-X-06` | distinctness D: `port(W1, s) ≢ port(M-POL-2, s)` | `[W1W]` | **EMITTED AND PRINTED, NOT GRADED** | ⚑ **UNGRADEABLE-declared (Q83(b), KP-110). The declared set is CLOSED at exactly `["TA-X-06"]`** | — |
| `TA-X-07` | conservation over **SEVEN** quantities: `offered = applied + dropped + voided + pool_truncated + pcl_reclaim + counterplay_absorbed` | run-internal | **relative `\|res\|/max(1,\|offered\|) ≤ 1e-12`**; absolute reported; **depth budget ~4,500 terms** | CARRIED VERBATIM; ⚑ **R-11 disposition § F.2d** | none |
| `TA-X-08` | denominator identity, both sub-identities | `[M-POL2]` 5/5 | exact | CARRIED | none |
| `TA-X-09` | all **9** `math_rules.test_vectors` of the five normative channel/release/interrupt/damage rules | `P-h`'s `math_rules.json` (331fd552…) | per-vector | ⚑ RE-DERIVED (pin moves, nine unchanged) | `C-h` carried |
| `TA-X-10` | `max_body_radius_m ≤ 43.758085029822276` (W1) | `[W1W]` · `arena.json` | exact, ≤ | RE-DERIVED, UNCHANGED | an arena/spawn-law change |
| `TA-X-11` | `n_wall_clamps_{player,body} == 0`, every W1 arm | `[W1W]` | integer | CARRIED | a spawn-law or arena change. *A port with no wall also scores zero* (§ F.5 cl. 6) |
| `TA-X-12` | pool inertness under ORACLE: total pool damage `== 0.0` | `[W1W]` · `DIV-19` | exact | CARRIED | satisfied by ABSENCE |
| `TA-X-13` | no player crit | `V0 · CritLimb LO` | integer | CARRIED | config identity |
| `TA-X-14` | the two DO-NOTs (`cause == "energy"` → 0; no release on every cast); a REFUSED cast is not a release | `math_rules` prohibitions | integer | CARRIED | — |
| `TA-X-15` | release schedule: (a) p01–p04 at `t = 0.0`, **p05 one burst at `t = 4.000 s`** (tick 49); (b) **no intra-point stagger**, printed `GREEN-BY-CONSTRUCTION` | census `M4` / `V11` | exact | CARRIED | (b) unrepresentable |
| `TA-X-16` | **p06 OFF:** `n_pool_picks == 47`, `n_spawn_point_6_keys_rolled == 0`, **and a counter for the filtered keys** | `waves.json` | integer | RE-DERIVED, UNCHANGED (54 / 47) | — |
| `TA-X-17` | `‖spawn_xy − anchor_xy‖ ≤ 8.0` m, every body, arm and salt | `placement_extents_m = 8.0` | exact, ≤ | RE-DERIVED, UNCHANGED | — |
| `TA-X-18` | the scatter discriminator: `u₁ = u₂ = 0.5` → **`(−4.0, 0.0)`** (not `(−5.656854249492381, 0)`, not `(0, 0)`) | `arena.json` | exact | RE-DERIVED, UNCHANGED | — |
| `TA-X-19` | arrival unconditionality; no damage predicate reads an arrival's `px, py` | `deferred_arrival.py:13-17` | integer | CARRIED | **GREEN-VACUOUSLY** (no arrival limb) |
| `TA-X-20` | player hit test: 2.99 m hit / 3.01 m miss; no angular gate; no target cap | census `D7` | exact | CARRIED | — |
| `TA-X-21` | quantisation rule per site + **zero bare `round(`** on the port's threat path | four modules | exact | CARRIED. ⚑ **Re-verify the live site list at emission** | the code moved (Q91) |
| `TA-X-22` | `cause == "interrupts_channel_flag"` is **0** under ORACLE | `V0`; V18+V19 | integer | CARRIED | config identity |
| ~~`TA-X-23`~~ | ~~board-roll composition~~ | struck at v1.2, retired | — | — | — |
| `TA-X-24` | **attack phase is `ENGAGE`**; `sha256(actor_id) mod n` is never evaluated | `V0` | exact | CARRIED | — |
| ⚑ `TA-X-25` | ⚑ **THE SPAWN PARTITION: four clauses, at the fight grain** | ⚑ **§ F.2f** | integer identity | ⚑ **RE-DERIVED** | ⚑ § F.2f |
| `TA-X-26` | **declared-join conformance: five clauses** | `P-i` · § F.2a | integer / exact / declared-precision | (a)–(d) CARRIED; (e) CARRIED + **grain-labelled** | — |
| `TA-X-27` | **degenerate-draw consumption: four clauses** | `P-h` · § F.2b | integer / byte-exact | (a)–(c) CARRIED; (d) RE-DERIVED, UNCHANGED | — |
| `TA-X-28` | **leech target law: three clauses** | § F.2g | integer / structural | CARRIED | — |
| ⚑ `TA-X-29` | **global-magnitude fold conformance: five clauses** | § F.2h | integer / declared-precision | ⚑ (e) **CORRECTED + RE-DERIVED** | — |
| `TA-X-30` | **the pursuit halt: two clauses** | § F.2i | exact / integer | CARRIED (`d_engage_m = 2.4` re-derived) | — |

#### F.2a · `TA-X-26`: DECLARED-JOIN CONFORMANCE *(carried)*

| clause | assertion | class |
|---|---|---|
| (a) | every declared JOIN in `V0`/`V1` is CONSUMED with a named call site emitted, or DECLARED-UNCONSUMED BY NAME against an absence row. `join_consumption_audit` asserts `n_declared == n_consumed + n_declared_unconsumed` with zero joins in neither state | EXACT · integer identity |
| (b) | `pm4p_leech_resistance.csv` is **LOADED**, its sha is verified against **`P-i` = `cb6a008b…`**, and ≥ 1 call site on the sustain path is named | EXACT · structural non-zero |
| (c) | RFC-4180 parse: **7,900** rows · **790** records · **8** distinct `total_leech_resist_pct` `{65,75,83,88,105,115,565,588}` · **5** distinct `adcth_mult_COUPLED` `{0.0,0.12,0.17,0.25,0.35}` · **790/790** wave-invariant | EXACT · integer counts |
| (d) | the law is READ from the column and never recomputed; any `max(0, 1 − res/100)` helper has **exactly one** call site (a cross-check) | EXACT · structural |
| (e) | over **`ARMED-464 := POOL-466 ∩ (v20 ∪ w40 ∪ w41 ∪ w44 ∪ w45)`**: mean `adcth_mult_COUPLED` **`0.2468965517`**, median `0.25`, max `0.35`, min `0.0`, **17** leech-immune | EXACT · `± 5e-7` |

⚑ **(e) at v1.8, re-derived: all five values reproduce.** ⚑ **GRAIN LABEL, which is mandatory on the
face:** `ARMED-464` is a **STATE-grain** set expression over pack rowsets. It is **not** the
fight-grain armed set (SWING-456), and the port must **not** substitute its own armed set (jack-ryan
Gate-2 § F INFO). The port may print its fight-armed set's mean **beside** it, under its own name.

#### F.2b · `TA-X-27`: DEGENERATE-DRAW CONSUMPTION *(carried)*

(a) a source scan finds **zero** `lo == hi` / `n_min == n_max` early returns on any registered draw
site, and refuses any site it cannot classify · (b) CPython's `_randbelow_with_getrandbits` rejection
loop is replayed per seed and asserted per seed, never as a mean · (c) the port consumes exactly what
the oracle consumes, none where the oracle takes none (p05, `wave_engine.py:683-695`); **29** live
sites · (d) over `waves.json::pools.wave_spawn_count`, waves 151–160: **139** min/max pairs, **97**
degenerate (69.8 %). ⚑ **At v1.8 hole 6's repair adds the chance draw to the port's per-slot path.
Clause (c)'s identity covers it (the port consumes what the oracle consumes), and G-3 must be re-run
against the ORACLE's draw sites (KP-120).**

#### F.2c · Closing conditions for `TA-X-01 / 15 / 16` *(carried)*

`TA-X-01`: a repeat probe, emission naming arm+salt ≠ `P-2`'s. `TA-X-15`: (a) the realised schedule is
emitted; (b) `GREEN-BY-CONSTRUCTION` with its mechanism. `TA-X-16`: the three counters are emitted.
**All three are emitted by drax's item-2 pass (godot `6b43cf4`); they are checked at the run.**

#### ⚑ F.2d · `TA-X-07`: THE TOLERANCE, CARRIED VERBATIM, AND R-11 GIVEN ITS LAW FOR BOTH OUTCOMES

| clause | assertion |
|---|---|
| (a) GRADED, RELATIVE | `\|residual\| / max(1.0, \|offered\|) ≤ 1e-12` |
| (b) REPORTED, NOT GRADED, ABSOLUTE | `\|residual\|` printed with `offered` beside it, every cell |
| (c) THE ACCUMULATION BUDGET | `1e-12 ≈ 4.5e3 × float64 eps (2.220446e-16)`, a depth budget of **~4,500 terms**. The runtime **EMITS** `conservation.n_terms_accumulated`. **If the realised depth exceeds 4,500 in any cell, the row is `UNGRADEABLE`, not green** |

⚑ **R-11, MEASURED (drax, relayed by the conductor, 2026-09-30):** `n_terms_accumulated = 1,226` against
a budget of 4,500, with `residual_relative ≈ 1e-14`. Cell **M-POL-2 / salt 0 / waves 151–160**, ORACLE
config, **one non-graded run** through the T-A emitter (`kc2rt_ta_emit.collect`). The runtime was the
last committed godot runtime with holes 1–6 + item 2 + labels, **on pack v3.4.2**, from a `git archive
HEAD` copy, tree digest `5876c028…` (make_manifest law). **Depth ≈ 0.68 terms/tick, so a full ~4,000-tick
clear is ≈ 2,700 terms, under budget.** ⚑ **CAVEAT, stated because it is real:** that runtime did not arm
the 334. On v3.6 about 456 records swing instead of 122, and every lifted hit adds a term. **R-11 is
re-measured on the v3.6 runtime before any v1.8 attempt fires (§ H, H-6).** This document does not
predict the re-measured figure.

⚑ **WHAT v1.8 DOES IN EACH CASE, FROM ITS OWN LAW AND NEVER BY WIDENING:**
1. **Re-measured depth ≤ 4,500 on every cell:** the row grades on (a) as written.
2. **Re-measured depth > 4,500 on the ungraded smoke:** by clause (c) the row would be `UNGRADEABLE` on
   that cell, and § G makes the verdict `INDETERMINATE`, which consumes no attempt, buys nothing, and
   seals nothing. ⚑ **So a v1.8 graded attempt MUST NOT FIRE on a runtime whose R-11 smoke reads above
   4,500.** It would be `INDETERMINATE` by construction. **The question goes to Matt (R-11's own
   route).** Any re-sizing of clause (c) is a **new dated prereg version committed ALONE**, never an
   edit to this file, and never a tolerance widened toward an observed residual.
3. **Realised depth > 4,500 on a graded cell** (the smoke read ≤ 4,500 but a graded cell ran deeper):
   `UNGRADEABLE` → `INDETERMINATE`, exactly as (c) says. No attempt is consumed, the attempt counter does
   not move, and the next step is Matt's.

⚑ **The residual is not the criterion, so it cannot rescue the row.** Attempt 1's max relative residual
was 1.563e-14, **64× inside** 1e-12. That shows the tolerance is not binding in practice. **It changes
nothing:** clause (c) keys on DEPTH, and v1.8 does not re-key it. ⚑ **The assert-wall gap is carried:
the row names SEVEN quantities and the attempt-1 wall checked SIX. The wall is not the row.**

#### F.2e · `TA-X-06`: UNGRADEABLE-declared, closed *(carried from v1.7 § F.2e)*

On record under its own id. It is **EMITTED AND PRINTED, NOT GRADED**: the per-salt `W1` / `M-POL-2`
digest pair with `TA-B-14`'s counters beside it, labelled **`UNGRADEABLE-declared (Q83(b), KP-110)`**,
with no colour. **It enters no verdict antecedent, counts in no PASS label, and is not a Q87 seal
condition.** Nothing is rescued. ⚑ **v1.8: THE DECLARED CLASS IS CLOSED.** A verdict file conforms only
if `declared_ungradeable` is **exactly `[{"id":"TA-X-06","authority":"Q83(b) / KP-110",…}]`**. Any other
id there makes the file **non-conforming (C1)**. A new member requires Matt's word **and** a new dated
prereg version. *(v1.7 pre-read WARN-1, folded.)* The six-point reasoning Matt ruled on is carried
verbatim in v1.7 § F.2e (pinned).

#### ⚑ F.2f · `TA-X-25`: THE SPAWN PARTITION, RE-DERIVED AT THE FIGHT GRAIN

> ⚑ **THE PRINCIPLE (`F.1a`, now at its third application to this row).** v1.5 asserted SIGNS over a
> decode-completeness fact. v1.6/v1.7 asserted a ZERO at the pack's STATE grain, which read a presence
> flag as armed offense. **v1.8 asserts IDENTITIES over populations the ORACLE'S OWN PREDICATE
> defines**, pinned as set digests. That grain does not depend on how our decode labels a record.

| clause | assertion | class | a RED means | ⚑ **expiry** |
|---|---|---|---|---|
| **(a)** | under `ORACLE`, `n_nodata_refused == 0`, every arm and every salt | EXACT · integer identity | a config leak: the port runs the `PLAY` refusal rule under `ORACLE` | none. **Print whether it is satisfied over an empty set** (§ F.5 cl. 6) |
| ⚑ **(b)** | **THE SPAWN ACCOUNTING IDENTITY.** Per arm per salt the three counters **`n_nodata_spawn_inert`, `n_measured_inert_spawn` and `n_measured_offense_spawn` are PRESENT BY THESE NAMES and EMITTED**, and **`n_nodata_spawn_inert + n_measured_inert_spawn + n_measured_offense_spawn == n_bodies_spawned`**. ⚑ **A missing `n_measured_offense_spawn` is a RED on the presence clause, not an UNGRADEABLE** (jack-ryan Gate-2 § C: *"Read as written, (b) is RED"*) | EXACT · integer identity + presence | the port re-created the oracle's own silence, or it classifies into an undeclared fourth bucket | **none.** An identity over a partition survives any change to the partition's contents |
| ⚑ **(c)** | ⚑ **THE FIGHT-GRAIN PARTITION, PER RECORD.** Per arm per salt the port emits **`spawn_by_record: {record_path: {n_bodies, class}}`**, with `class ∈ {nodata_inert, measured_inert, measured_offense}`, summing to (b)'s counters. **Assert: (1) every key ∈ POOL-466 (set digest pinned); (2) every record in SWING-456 has class `measured_offense`; (3) every record in NONSWING-10 has class `nodata_inert` or `measured_inert`; (4) per class, `Σ n_bodies` equals (b)'s counter.** | EXACT · integer identity, record grain | (1) the port rolled a non-member (trap 6, **membership**); (2) the port left an oracle-swinging record inert, e.g. a lifted `u5 CONSTRUCTED` record it failed to arm; (3) ⚑ **the port armed a record the oracle cannot swing**, e.g. **the four `w44` records** or the three `u5` HONEST-FAILs (the pack's rule: *"HONEST-FAIL MUST NOT BE ARMED"*); (4) the emission is internally inconsistent | ⚑ **EXPIRES WHEN THE ORACLE'S SWING SET MOVES:** a change to `load_profiles`' construction, to P-5 setting 1 or 3, or to the supplement. **Mechanism:** SWING-456 / NONSWING-10 are the oracle's `can_swing` over POOL-466 under P-5 (§ A.3), which is **a property of the oracle's code and the pinned supply, not of a label** |
| ⚑ **(d)** | the **label split** of NONSWING-10's bodies between `nodata_inert` and `measured_inert` is **EMITTED AND REPORTED, NOT GRADED**. So is **`Σ` bodies of NONSWING-10 per arm** | EMITTED, NOT GRADED | — | ⚑ **§ F.1 forbids grading either one.** The split is a vocabulary choice. The oracle's profile predicate reads 0 / 10, and KP-122's absence disposition reads 4 non-CONSTRUCTED under the continuing absence. **Both agree on behaviour.** The inert body count is a draw outcome: 10 records of 466 make a non-zero likely, never certain |

> ⚑ **WHAT `TA-X-25` PROVES AT v1.8, AND WHAT IT STILL DOES NOT.** **PROVES:** the port spawns only
> POOL-466 members; it arms **exactly** the records the oracle can swing, **no more and no fewer**; its
> counters are complete, named and consistent. **DOES NOT PROVE:** the **composition** of the roll (which
> members, in what proportion), and **what an armed body does after it is armed** (slot choice, gates,
> grouping, dying slots, PCL, death order, march base: the seven holes, § G.2).
>
> ⚑ **Emission requirement:** `spawn_by_record` did not exist at attempt 1. **Its absence makes (c)
> UNGRADEABLE → `INDETERMINATE`** (no attempt consumed). It is listed at § H so that it exists before a
> run.

#### F.2g · `TA-X-28`: THE LEECH TARGET LAW *(carried verbatim)*

(a) **NO CAP, EITHER SIDE:** `n_leech_target_caps_applied == 0` and `n_leech_tick_caps_applied == 0`,
every arm and salt, oracle and port (legolas C-8 `DB-EXHAUSTIVE-ABSENCE`) · (b) **FULL PER-TARGET, FULL
DISC:** leech accrues once per hit body inside the hit loop, with no primary-target privilege and no
arc gate; the applied portion is `0.57 × D_weapon` (`OFFICIAL-GUIDE-VERBATIM`) · (c) **the oracle has the
same shape, asserted.** A green says the replicas implement one leech law, **not** that the law
reproduces Matt's fight (§ F.5 cl. 10).

#### ⚑ F.2h · `TA-X-29`: GLOBAL-MAGNITUDE FOLD CONFORMANCE

| clause | assertion | class | v1.8 |
|---|---|---|---|
| (a) | **`PRED-GMAG-WHOLE` evaluates TRUE:** attribute limb **193** records (**154** cite `pm4o_trash_terms.csv`) **AND** own limb **527** (**104**). A loader short of either **MUST REPORT ITSELF INCOMPLETE** | EXACT · integer counts | RE-DERIVED, UNCHANGED (`⚑ v3p4p2_fold_completeness` is byte-identical in v3.5). **Grain label mandatory:** `attr_limb_records: 193` beside `attr_limb_actors: 344` (INFO-2) |
| (b) | **`Z5-LAW` verbatim:** `om` = `M_inst` (direct/leech) · `M_dot[family]` (dot) · **1.0** (PCL); own % joins **additively into the pool** (`om += own_pct/100`), never as a second multiply; the attribute limb per family; **leech rows DROPPED** by G3; the chain folds whole | EXACT · declared-precision | CARRIED. ⚑ **Governed at v3.6 by `math_rules :: ⚑ v3p6_rows.c5_global_fold_composition` row `C5-Z5-LAW`, a RESTATEMENT of `Z5-LAW` with the content unchanged** (`⚑ v3p6_points_to.Z5-LAW`). C3 is HALTED and not folded (KP-131). **Pack and folded oracle agree** |
| (c) | **`z3` is a CHECK asserted before `own_add`:** the port's `M_inst` per wave equals the pack's `z3_wave_damage_modifier_check` | EXACT · declared-precision | CARRIED |
| (d) | **the 29 inert records take the IDENTITY path** (`attr 1.0`, `type 1.0`, `own 0.0`) and are **never** estimated from a sibling, donor or class median | EXACT · structural identity | CARRIED at **29, of which 0 fall in waves 151–160**. Print *"unexercised: 0 of 29"* (v1.6 pre-read WARN-4). ⚑ **The 264 lifted identity-path records are `C-k`, NOT this clause** |
| ⚑ **(e)** | ⚑ **THE TERMINAL MAGNITUDE, REPRODUCED UNDER P-5:** the supply-weighted pre-mitigation fold ratio (§ A.4's definition, **config E**: the static supply of the profiles `load_profiles` builds under P-5 setting 1, **C-11a loader included; runtime grants excluded, being positional**) is **`3.207764` at w159** and **`4.980316` at w160**, and **each priced record's ratio matches the table below** | EXACT · declared-precision **`\|Δ\| ≤ 5e-4`** on each wave ratio and each record ratio (the third decimal, as v1.7 printed) | ⚑ **CORRECTED** (v1.7's 3.406 was config A) **and RE-DERIVED** (the pool lift adds 10 / 14 priced records; the C-11a aura removal moves w160) |

**`TA-X-29(e)`'s per-record table (config E, the folded oracle at HEAD).** Columns: `ratio` · `sum_fold_on` ·
`sum_fold_off`, rounded as the walk rounds. **L** = supplied by the pool lift; **I** = incumbent.

| w159 (`M_inst` 1.83) | | ratio | on | off |
|---|---|---:|---:|---:|
| L | `aetherial_fleshhulk_mine` | 3.542988 | 107,680.764 | 30,392.64 |
| L | `beetle_maggot01` | 3.366517 | 79,633.54 | 23,654.58 |
| L | `chthonianrylok_ekketzul` | 3.59875 | 100,550.672 | 27,940.44 |
| I | `chthonianservitor_lunalvalgoth` | 2.546547 | 48,845.693 | 19,181.145 |
| I | `humanwendigo_darkwood_01` | 3.784114 | 47,782.013 | 12,627.0 |
| L | `korvaakmessenger_02` | 3.033476 | 86,335.987 | 28,461.075 |
| I | ⚑ `korvaakmessenger_02b` (**Crucible surface**) | 3.034357 | 89,742.771 | 29,575.545 |
| L | `manticore_jaggedwaste_01` | 2.956584 | 45,188.897 | 15,284.16 |
| L | `rokwind_01` | 3.362895 | 39,355.455 | 11,702.85 |
| I | `skeletalgolem_stepsoftorment_01` | 3.120862 | 31,822.677 | 10,196.76 |
| L | `statue_templeguardian_02` | 1.960798 | 25,216.503 | 12,860.325 |
| L | `statue_templeguardian_03` | 1.960798 | 25,216.503 | 12,860.325 |
| L | `stonegryphon_templeguardian_01` | 2.762796 | 56,697.046 | 20,521.62 |
| I | `wendigo_ancient_namadea` | 4.077782 | 97,779.057 | 23,978.49 |
| I | `witchgod_finalboss` | 3.978465 | 80,028.246 | 20,115.36 |
| L | `yeti_rimehorn_01` | 3.080011 | 39,159.032 | 12,713.925 |
| | *unpriced (no profile): `proxy_w09_p01a…p05a` (5)* | | | |
| | **w159 supply-weighted** | ⚑ **3.207764** | | |

| w160 (`M_inst` 1.83) | | ratio | on | off |
|---|---|---:|---:|---:|
| L | `aetherialcolossus_galakros` | 3.80807 | 86,437.112 | 22,698.405 |
| I | `statue_korvaaktombguardian` | 4.102804 | 111,664.686 | 27,216.675 |
| L | `wendigocannibal_h01` | 5.951244 | 42,038.4 | 7,063.8 |
| L | ⚑ `wendigocannibal_h02` (C-11a: an aura leech row leaves) | 5.946459 | 47,652.363 | 8,013.57 |
| L | `wendigocannibal_h03` | 5.476449 | 18,881.261 | 3,447.72 |
| L | ⚑ `wendigocannibal_h04` (C-11a) | 5.429514 | 16,533.522 | 3,045.12 |
| L | ⚑ `wendigocannibal_h05` (C-11a) | 5.429514 | 16,533.522 | 3,045.12 |
| I | ⚑ `nemesis_aetherial_01` (C-11a) | 8.165613 | 235,450.515 | 28,834.395 |
| I | `nemesis_aetherialvanguard_01` | 6.466635 | 155,338.25 | 24,021.495 |
| I | `nemesis_beast_01_p1` | 3.829365 | 48,791.371 | 12,741.375 |
| L | `nemesis_beast_02` | 2.689026 | 34,626.031 | 12,876.795 |
| L | `nemesis_chthonian_02` | 5.55761 | 73,832.204 | 13,284.885 |
| I | `nemesis_chthonianvoidborn_01` | 4.653725 | 128,277.025 | 27,564.375 |
| I | `nemesis_kymon_01` | 3.474869 | 167,919.204 | 48,323.895 |
| L | `nemesis_kymon_02` | 1.075958 | 13,506.377 | 12,552.885 |
| I | `nemesis_orderdeathsvigil_01` | 6.944508 | 181,508.437 | 26,136.975 |
| L | `nemesis_orderdeathsvigil_02` | 3.658935 | 22,012.61 | 6,016.125 |
| I | `nemesis_outlaw_01` | 6.146017 | 98,036.321 | 15,951.195 |
| L | `nemesis_outlaw_02` | 5.388859 | 107,368.292 | 19,924.125 |
| L | `nemesis_undead_01` | 3.822594 | 75,665.167 | 19,794.195 |
| L | `nemesis_undead_02b` | 5.470426 | 124,770.592 | 22,808.205 |
| I | `nemesis_wendigo_01` | 6.06632 | 135,475.515 | 22,332.405 |
| L | `nemesis_wendigo_02` | 4.391011 | 85,550.484 | 19,483.095 |
| | *unpriced (no profile): `proxy_w10_p01a…p04a, p06a` (5)* | | | |
| | **w160 supply-weighted** | ⚑ **4.980316** | | |

⚑ **EMITTED, NOT GRADED: the ten-wave walk.** The port prints its per-wave ratio for **w151–w160**.
The oracle's config-E values are **3.353866 · 1.768566 · 1.899330 · 2.994929 · 1.927777 · 2.846875 ·
1.979824 · 1.592632 · 3.207764 · 4.980316** (w151…w160), with identity-path priced records per wave
**8 · 94 · 73 · 4 · 53 · 5 · 69 · 95 · 0 · 0**. **It gates nothing.** It is the only place a port's
treatment of the 264 identity-path records (`C-k`) shows at all.

#### F.2i · `TA-X-30`: THE PURSUIT HALT *(carried)*

(a) **the halt reads the wire:** every body halts at `arena.json :: d_engage_m` (**2.4**, re-derived),
with `travel = min(v·dt, max(0, dist − d_engage_m))`, centre-to-centre, inclusive `<=`, per-tick order
unchanged, and **NaN tested explicitly** · (b) **`n_bodies_halted_beyond_d_engage == 0`**, every arm and
salt. ⚑ **At v1.8, hole 5's repair removed the port's `MELEE_REACH_M` floor from `_max_reach`, and it
must not have touched the pursuit halt. The halt reads `d_engage_m`, not `_max_reach` (KP-87, KP-118).
(a) is the row that would catch it.**

### F.3 · DIAGNOSTIC rows: 19 ids, 0 gating, every width VOID

**Carried from v1.7 § F.3 in full, BY REFERENCE:** the six mandatory fields (value · coverage k/89 ·
grain pair · calibration range · dilution · effective `n`), `[width VOID @ re-base]`, CLASS I
(`TA-B-16…19`, scale-free by construction, `16a/16b` split owed), CLASS II (the per-tick seven with
both verbatim sentences), CLASS III (`TA-B-06`, `window_coverage` mandatory), and CLASS VI (`TA-B-10 / 11
/ 12`). **Two change:**

⚑ **CLASS IV · `TA-B-15`, RE-POINTED.** It measures the substrate and is **never** promoted. It prints,
per arm per salt: **(i)** the count of bodies **labelled** `nodata_inert` (reference point **`0`** under
the oracle's profile predicate at P-5); **(ii)** the count and body fraction of bodies of **NONSWING-10**
records, with pool-pick count beside it; **(iii)** the **member-grain** reference **10/466 =
0.021459**, labelled as a MEMBER fraction. ⚑ **No body-grain reference is minted.** It needs the roll
law's weights and is owed, like `P-e′` Add. § 3's fractions (`OQ-5`). **A salt reporting zero NONSWING
bodies is plausible and is not an anomaly.**

⚑ **CLASS V · `TA-B-01`, NEW REFERENCE SENTENCE (mandatory, verbatim):** ***"`BAND / NON-DECISIVE /
REPORT-ONLY`. A terminal wave inside or outside this band is not evidence of fidelity either way. The
oracle's sealed `M-POL-2` arm terminates at `[156, 152, 151, 151, 156]`, `player_death` on every salt.
The v1.8 oracle (the 338 armed, the winner surface armed, the C-11a corrections folded) terminates at
`[156, 152, 155, 152, 152]`, `player_death` on every salt, and no salt reaches wave 160. A port that
clears to wave 160 has not survived a hard board; it has failed to be in one."***
`TA-B-13`'s and `TA-B-14`'s sentences are carried verbatim, including *"This is the counter that carries
`TA-X-06`'s ENTIRE MECHANISM, and it is the one the prereg declined to band."*

### F.4 · Emitted, not graded: **three**

Per-registered-site draw counters (29 live sites) · the tick-resolution HP trace · ⚑ **the ten-wave z4
walk (§ F.2h)**.

### F.5 · ⚑ REPORT-FACE RULES: twelve

**Cl. 1–6 and 9–10 are carried verbatim from v1.7 § F.5.** Cl. 6's instance list is **derived
mechanically at emission**. It includes `TA-X-25(a)` (possibly an empty set), `TA-X-28(a)`
(absence-satisfied), `TA-X-29(d)` ("unexercised: 0 of 29"), `TA-X-11`, `TA-X-12`, `TA-X-15(b)`,
`TA-X-17` and `TA-X-19` (v1.6 pre-read WARN-4). Changed and new:

7. ⚑ **THE SUSTAIN SENTENCE, RE-DERIVED (mandatory):** ***"`leech` and `intake` still have no oracle
   side in the seals (`C-e`). Off-seal, the v1.8 oracle (the C-11a corrections folded) KILLS THE
   PLAYER AT WAVES 152–156 on salts 0–4, and lands ×3.17 the referent's intake over waves 151–159 on
   the landed grain. The port's own figure is printed from this run and not
   asserted here. A GREEN T-A IS COMPATIBLE WITH ANY RELATION BETWEEN EITHER REPLICA AND THE
   REFERENT."***
8. ⚑ **THE ORACLE'S OWN HOLES, EXTENDED TO FOUR (mandatory, verbatim):** ***"Four declared absences
   are the ORACLE's holes and not the port's defects. No row grades them, and a port that does not
   implement them is CORRECT: `ABS-NINE-WINNER-SURFACE-HONEST-FAILS` (13 slots) ·
   `ABS-GLOBAL-MAGNITUDE-FOLD-INERT-RECORDS` (29 records, 0 in waves 151–160) ·
   `ABS-C-I14-2-SOURCED-UNFOLDED` (≤ 2.2 % pooled, ×1.000 at w159/160, unfolded on BOTH sides) · the
   Q91 pool lift's unconstructed supply (3 HONEST-FAIL records, 1 dying-only, 249 of 1,618 winner slots
   unbuilt, each listed with its reason in `u5` / `u8`)."*** And one that is **not** an absence but is
   printed beside them: *"264 lifted records take the global-magnitude identity path (`C-k`); no EXACT
   row grades a port that invents supply for them."* ⚑ **And the C-11a block, verbatim:** *"The C-11a
   fold declares: no monster retaliation (C-11a-R1); grant families not applied (elemental-resistance
   expansion, per-type modifiers, crit damage, speed/OA/DA, absorption, life); C3 HALTED and not folded
   (R3); the DoT attribute scope routed (R4). Mechanisms are Edition-IV (post-referent). No row grades
   any of these, and a port that does not implement them is CORRECT."*
11. ⚑ **NEW: THE SEVEN HOLES (mandatory on any report, including a passing one):** ***"Seven port≠oracle
    holes (PCL dropped · death after heal · 28 % of damage rows unreachable · `tree_attack` slots never
    chosen · dying slots mishandled · slot chance/cooldown/delay never read · monsters on the wrong march
    base) are invisible to every
    EXACT row in this instrument. A v1.8 PASS is not quotable without jack-ryan's hole-closure finding
    at the same runtime digest, and the seal is blocked on any non-zero R-6 invariant."*** followed by
    the three R-6 invariants **printed with their values** (§ G.2).
12. ⚑ **NEW: MIXED EDITION (mandatory):** ***"The 338 pool records were lifted from the Edition-II
    depot and the incumbent at Edition-III. The skill surface differs on 41 of 566 skills (median
    ×1.235 on the differing rows, depot higher on 99 of 107). Port and oracle read the same rows, so T-A
    cannot see this. The board over-reads harder than the referent's edition on roughly 7 % of
    skills. The C-11a mechanisms were decoded from Edition-IV, a build that post-dates the referent."***

---

## § G · FAIL TAXONOMY, THE HOLE-CLOSURE RULE, AND THE GRADED-RUN CAP

| verdict | antecedent | consequence |
|---|---|---|
| **`STRUCTURAL`** | **≥ 1 of the 28 EXACT rows RED** | the port is wrong; no W4 until repaired; **consumes one of v1.8's two attempts**; **L2 applies (§ G.1)** |
| **`INDETERMINATE`** | 0 EXACT red, **≥ 1 of the 28 UNGRADEABLE** (incl. `P-1`…`P-5` red, and `TA-X-07(c)` above its depth budget) | **does NOT consume an attempt**; nothing seals |
| ~~`STATISTICAL`~~ | retired at v1.5 under F5 | — |
| **`PASS`** | all 28 EXACT green, none UNGRADEABLE | ⚑ **`PASS @ coverage k/89, 28/28 EXACT rows green, TA-X-06 UNGRADEABLE-declared (Q83(b)), dilution ⟨d⟩×, substrate_epoch v3.6/4fd35330…, prereg v1.8`**. Never unqualified, and **never quotable alone (§ G.2)** |

**Order:** `STRUCTURAL → INDETERMINATE → PASS`; stop at the first hit. **No diagnostic appears in any
antecedent.** A **graded run** is one execution of the 5 × 5 matrix producing a conforming verdict file.
A repair between attempts does not create a third. **No post-hoc widening, by anyone.**

⚑ **A DECLARED ROW IS NOT AN UNGRADEABLE EXACT ROW, AND THE DECLARED CLASS IS CLOSED.** `TA-X-06` appears
in no antecedent. `declared_ungradeable` must be **exactly** `["TA-X-06"]`. Anything else is **C1**
(non-conforming). A grader who reads the declaration into `INDETERMINATE` has re-imposed the gate Matt
removed. A grader who declares a second row has removed a gate Matt did not.

### ⚑ G.2 · THE HOLE-CLOSURE RULE: SEAL-BLOCKING, NOT VERDICT-BLOCKING

**The seven port≠oracle holes are not EXACT rows. They cannot produce, raise or lower a verdict.** They
are closed or not closed by **jack-ryan's repair Gate-2 (the hole-closure finding)**, whose criteria
were **fixed before any repair result existed** (Gate-2 on attempt 1, `d2aa93db…`; R-13…R-16 added by
the conductor for holes 3–6):

| hole | ledger | closure criterion |
|---|---|---|
| 1 · **PCL dropped** | KP-113 | **R-3** (PCL composition exact: `om = 1.0`, × `pcl_fraction` (0.74, MULTIPLICATIVE, from `u7`), once per volley, unmitigated, subject to the R-PM2-5 can't-kill-alone floor, agreeing with the oracle function on one fixture) + **R-6(iii)** |
| 2 · **death after heal** | KP-113 | **R-5** (a lethal hit + a larger same-tick heal ⇒ death **at that tick**; headless loop **and** `play_step`; DoT- and aura-lethal variants at the oracle's break sites) + **R-6(i)(ii)** |
| 3 · **28 % of damage rows unreachable** | KP-116 | **R-13** (reachable rows per record = the oracle's slot-only grouping; `group: weapon` rows on every `is_weapon_swing` slot) |
| 4 · **`tree_attack` slots never chosen** | KP-118 | **R-14** (`choose_slot` iterates the oracle's built slot order) |
| 5 · **dying slots mishandled** | KP-118 | **R-15** (fire once on death if in reach; excluded from `_max_reach`; no `MELEE_REACH_M` floor) |
| 6 · **slot chance / cooldown / delay never read** | KP-120 | **R-16** (read from `⚑ or_zero_fields`; the oracle's draw site and order; cooldowns keyed by (actor, slot name); G-3 re-run against the oracle's sites) |
| 7 · **monsters and pets on V16-4's 4.0, not the oracle's march base 3.209466** | KP-126 (repaired, KP-130) | ⚑ **no R-number from this file.** jack-ryan assigns the criterion at his pre-read, before he reads any repair result (conductor). The natural form is the K4-0 base bound bitwise for monsters and pets, never the player, failing on `c9c973fa…`. **This file names the hole. It does not write his criterion** |
| *(unnumbered)* · ⚑ **the C-11a GRANT LAW**: coverage by radius, D-C11a-1 activation, D-C11a-2 one-instance stacking, the weapon-swing rider, the resistance grants (§ B.6 setting 11). The port had no aura phase at KP-130 | KP-127 / KP-130 | ⚑ **no R-number from this file, and no hole number.** The conductor keeps it NAMED in the closure set. **jack-ryan assigns its criterion at his pre-read**, before he reads any repair result |
| *(all)* | — | **R-1** expected values from **oracle code** (gamora) · **R-2** every probe **FAILS** on `c9c973fa…` · **R-4** a per-dtype counter on the unmapped-type branch · **R-7** one runtime digest · **R-8** probes inside the MANIFEST |

**R-6, the three invariants, printed on the attempt's report face and never in an antecedent:**
(i) cells with `killer_id` set and `terminal_reason == cleared` = **0** · (ii) in-tick resurrections =
**0** · (iii) `PercentCurrentLife` intake **> 0** wherever a PCL row fired.

⚑ **THE RULE (R-9, carried as law of this instrument):**
1. **A v1.8 `PASS` IS NOT QUOTABLE** (in a report, a ledger row, a seal claim, a message to Matt, or a
   T-C re-confirm request) **unless it is quoted TOGETHER WITH jack-ryan's hole-closure finding GREEN
   at the SAME runtime digest (R-7).** A PASS without it is a verdict about 28 rows that cannot see the
   attack-selection path. It is true, and it is not evidence of fidelity.
2. **ANY NON-ZERO R-6 INVARIANT BLOCKS THE SEAL.** It does not block the verdict. The verdict is
   whatever § G's table says.
3. **Q87's seal therefore reads, at v1.8:** `PASS` (28/28) **AND** coverage 89/89 mapped **AND** T-B
   reported DIAGNOSTIC **AND** ⚑ **jack-ryan's hole-closure finding GREEN at the graded digest, with all
   R-6 invariants at their stated values** **AND** Matt's T-C yes **on that same digest** (KP-114: the
   KP-110 yes is bound to `c9c973fa…` and does not carry over). ⚑ *The fifth condition is not a new
   goalpost. It is R-9, fixed before any repair result existed and ruled by the conductor at KP-113(ii)
   and KP-122. This file writes down where it sits.*

### G.3 · Verdict file `kc2play.ta_verdict.v1` (v1.8)

```
prereg_version                    : "v1.8"
prereg_sha256                     : <this file, derived at emission>
substrate_epoch                   : "v3.6 / model 4fd35330… / reference 4e23ffc6…"
band_widths_sha256                : 1c80f080…          (P-a — CONSTRUCTIONS ONLY; every width VOID)
galadriel_note_sha256             : d48512aa…          (P-b)
galadriel_expected_values_sha256  : a8b85331…          (P-c)
galadriel_release_labels_sha256   : 15dace60…          (P-d)
q91_lift_note_sha256              : d68561d5…          (P-l.q91 — governs TA-X-25 / P-5 #3)
roster_rebase_note_sha256         : 4b7b78c8…          (P-e — lineage)
model_pack                        : {dir: "kc2-model-pack-v3-E-s09-cp150-mech-v3p6-20260930_045353", digest: 4fd35330…, files_verified: 17}
reference_pack                    : {dir: "kc2-reference-pack-v3-E-s09-cp150-mech-v3p6-20260930_045353", digest: 4e23ffc6…, files_verified: 7}
cross_pin_verified                : true
leech_resistance_csv_sha256       : cb6a008b…          (P-i)
anchor_timing_csv_sha256          : 58205679…          (P-k)
x8_artifact_sha256                : cc361a3f…          (P-n.2)
set_digests                       : {"POOL-466": 33c886a1…, "SWING-456": 706a61d5…,
                                     "NONSWING-10": 00b4cb0e…, "FALLBACK-158": e8114efa…}
register_sha256                   : <v0.3's MACHINE form, emitter-derived>
preconditions.P1_coverage         : {"mapped":89,"total":89,"unmapped":0,"refusals":<n>}
preconditions.P3_roll             : {"population":"POOL-466","cardinality":466,
                                     "law":{"alternative":"WEIGHTED:pool_weight","name":"UNIFORM:randrange"}}
preconditions.P4_pack             : {"model":<dir>,"reference":<dir>,"files_verified":24,"mismatches":0,"cross_pin":true}
preconditions.P5_folds            : {"loader_call":"load_profiles(dot_corrections=True, pet_special_gates=None, winner_surface=from_x8, pool_lift=load, c11a=C11aLoader(CLASS))",
                                     "winner_surface":"ARMED","pool_lift":"ARMED",
                                     "per_cast_energy_column":"PARENT_PLUS_MODIFIER",
                                     "insufficient_energy_policy":"REFUSE","regen_ungated":true,
                                     "global_magnitude":"ARMED_UNCONDITIONAL","measured_board_attached":true,
                                     "pcl":{"limb":"MULTIPLICATIVE","pct":26.0,"source":"u7"},
                                     "non_health_route":["ManaBurnDrain","Disruption","PierceRatio","SlowManaLeach"],
                                     "monster_run_speed":{"LAP_R":128,"BAND_A":180,"FALLBACK_1.000":158},
                                     "c11a":{"C1_retaliation_gate":true,"C2_aura_scope":"CLASS","C2_stack_same_buff":false,
                                             "C4_duration_divisors":true,"C3":"NOT_FOLDED (KP-131)",
                                             "grants_csv_sha256":"749d58f4…"},
                                     "monster_march_base":{"oracle_m_per_s":3.209466,"source":"patrol.MARCH_BASE_M_PER_S[LO]",
                                                           "port_m_per_s":<n>,"source_on_wire":"v3.5.2 (KP-126), carried in v3.6"}}
declared_ungradeable              : [{"id":"TA-X-06","authority":"Q83(b) / KP-110","graded":false,
                                      "relation_per_salt":<W1 vs M-POL-2 digest pair>}]   ⚑ EXACTLY this one
v0_limb_set                       : <diffed line-by-line against V0>
join_consumption_audit            : [{join_id, consumed, call_site | declared_unconsumed_ref}, …]
gmag_conformance                  : {"pred_gmag_whole": true, "attr_limb_records": 193, "attr_limb_actors": 344,
                                     "attr_lap_o": 154, "own_limb": 527, "own_lap_o": 104, "inert_records": 29,
                                     "terminal_multiplier": {"w159": 3.207764, "w160": 4.980316},
                                     "per_record": <§ F.2h tables>, "ten_wave_walk": <emitted, not graded>}
leech_law                         : {"n_leech_target_caps_applied": 0, "n_leech_tick_caps_applied": 0,
                                     "scope": "ALL_BODIES_IN_DISC", "weapon_portion": 0.57}
pursuit                           : {"d_engage_m": 2.4, "source": "arena.json", "n_halted_beyond": 0}
draw_site_census                  : {registered:29, short_circuits_found:0, degenerate_pairs:"97/139"}
conservation                      : {residual_abs, residual_rel, offered, n_terms_accumulated} per cell
nodata                            : {"refused":0, "nodata_spawn_inert":<n>, "measured_inert_spawn":<n>,
                                     "measured_offense_spawn":<n>, "bodies_spawned":<n>,
                                     "spawn_by_record":{<record>:{"n_bodies":<n>,"class":<c>}}}   per arm per salt
diagnostics                       : [{id, value, coverage, grain_pair, calibration_range, dilution,
                                     effective_n, width: "VOID@rebase"}, …]
hole_closure                      : {"finding": <jack-ryan repair Gate-2 path + sha>, "runtime_digest": <R-7>,
                                     "R6": {"killer_set_but_cleared": <n>, "in_tick_resurrections": <n>,
                                            "pcl_intake_where_pcl_fired": <bool>}}   ⚑ REPORT FACE — never an antecedent
oracle_holes_printed              : true    (§ F.5 cl. 8, four)
starved_channel_printed           : true    (cl. 9)
t_a_limits_printed                : true    (cl. 10)
seven_holes_printed               : true    (cl. 11)
mixed_edition_printed             : true    (cl. 12)
```

**T-B quoting cap: three refusal conditions, UNCHANGED.** **C1:** verdict file absent, unparseable, **any
pinned sha mismatched**, or **`declared_ungradeable ≠ ["TA-X-06"]`**. **C2:** `verdict ∈ {STRUCTURAL,
INDETERMINATE}`. **C3:** coverage not 89/89-mapped. *"A fidelity figure"* keeps v1.7's mechanical
definition. `TA-B-15` is expressly **not** one. Degraded behaviour: raw twin-side statistics, a banner
first, and a non-zero exit.

### ⚑ G.1 · THE GRADED-RUN CAP: **`0` OF `2` UNDER v1.8**

⚑ **Matt, KP-115: *"Reset to 2"*.** The allowance attaches to **v1.8**. **Q85's four guards hold again:**
(1) the reset was ruled **from outside the run** (Matt); (2) this prereg is **committed ALONE, with every
pin re-derived, before anything is graded against v3.6** (D4); (3) **v1.7's attempt 1 STAYS ON THE
RECORD** as spent against v1.7, `STRUCTURAL @ 89/89` (red `TA-X-25(c)` and `(b)`), and v1.4/v1.5's
attempts stay as attempts against v3.3. A reset that erases its predecessors is amnesia; (4)
`substrate_epoch` is declared on every artifact (§ C.7).

**Naming, so the two counters never blur:** the next graded run is **v1.8 attempt 1** (the run's
**second** graded execution under a v1.7-or-later prereg). Ledger prose that calls it "attempt 2"
must say "v1.8 attempt 1 (overall attempt 2)".

⚑ **L2, AS IT APPLIES TO v1.8:**
- **v1.8 attempt 1 fires only after jack-ryan's repair Gate-2 (R-1…R-16) PASSes the repaired runtime,
  on the digest it names (R-7), AND this file's pre-read has been filed, AND R-11 has been re-measured
  on that runtime at ≤ 4,500 (§ F.2d).**
- **v1.8 attempt 2 fires only after a v1.8-attempt-1 `STRUCTURAL` red is repaired and jack-ryan Gate-2
  PASSes that repair.**
- An `INDETERMINATE` consumes nothing and buys nothing.

---

## § H · OWED BEFORE v1.8 ATTEMPT 1 (blocking), AND AFTER

| # | owed | owner | why it blocks |
|---|---|---|---|
| **H-1** | **the port onto v3.6**: arm the **334** (`u5 CONSTRUCTED`, from `u1` slots / `u2` rows / `u3` OA / `u4` swing period); ⚑ **do NOT arm the 4 `w44` records or the 3 HONEST-FAILs**; ride dying-only `aetherialimp_a01`'s dying slot per hole 5; PCL from `u7` (fail closed); non-health families routed per `u6`; **monster run speed per v3.5.1's `K1`/`K2` rows (populations BAND-A-180 / FALLBACK-158, 466/466 coverage asserted at bind)**, composed against **v3.5.2's march-base row (3.209466 m/s, not 4.0; fail closed)** (§ B.6 setting 10); ⚑ **the C-11a fold: the 131 `SkillBuff_Passive` slots removed as damage, and their grants applied to covered bodies per v3.6 `c1`/`c2`/`c6` (coverage, D-C11a-1 activation, D-C11a-2 one-instance stacking, the weapon-swing rider)** (setting 11); the `.app` rebuilt and its header `pack_digest` read by **running** the binary | **drax** | `P-4` is red until the header reads `4fd35330…`. Without the 334 armed, `TA-X-25(c)` reds; without the speed row, the lifted bodies stand still |
| **H-2** | ⚑ **`spawn_by_record`** per arm per salt, class-labelled, summing to (b)'s counters | drax | `TA-X-25(c)` is UNGRADEABLE without it |
| **H-3** | ⚑ **`TA-X-29(e)`'s probe expected values moved from v1.7's `3.406 / 5.418` to v1.8's `3.207764 / 4.980316` + the per-record table (config E).** The probe currently keeps v1.7's value and is RED on w159 (`6b43cf4`) | drax (R-1: values from this file, derived from oracle code) | the probe must fail on `c9c973fa…` and pass on the repair against **v1.8's** numbers |
| **H-4** | ⚑ **R-10: every stale harness field removed or restated to v1.8.** The seven surfaces named at attempt 1: the `ta_x_25` class text (v1.4's sign) · the `ta_b_15` reference points (v1.5's `0.3828`) · the `TA-X-07` conditions (`tolerance: 1e-06`, `terms_expected: 6`) · `relation_rows_RAW_not_graded.TA-X-06` (`holds_raw` + *"DIFFERENT on ≥ 1 salt"*) · the `P3_roll` note *"TA-X-25(c) is the behavioural check"* (at v1.8, restate it as *"membership only, via (c)'s partition"*) · `prereg_version` in every file (**"v1.8"**) · `substrate_epoch` (**v3.6**). drax's `5e5e9e1` moved them to v1.7 **read from the prereg**, so re-pointing the file should carry them. **The grader verifies it on the emission, not on the commit message** | drax | read literally, attempt 1's harness text would have turned its red GREEN (KP-113) |
| **H-5** | **the hole-closure finding** at the graded digest (§ G.2) | **jack-ryan** | `PASS` is not quotable without it, and the seal is blocked on R-6 |
| **H-6** | ⚑ **R-11 re-measured on the v3.6 runtime** (one ungraded cell, the T-A emitter) | drax | § F.2d: above 4,500 the attempt must not fire |
| **H-7** | **this file's pre-read** | jack-ryan | D4 / the series' practice |
| **H-8** | **Matt's T-C re-confirm on the repaired, graded digest** | Matt | a seal condition (KP-114); not an attempt precondition |

**Not blocking, named so they are not lost:** `TA-B-16…19` widths and the `16a/16b` split ·
`TA-B-06`'s corrected port-side emission · body-grain coverage fractions (`OQ-5`) · `CHARTER_DENOMINATOR`
and the charter's live `72 / 229 / 297 / 302` (`OQ-7`) · `wendigo_frenzyswipes` · `pet_limit`
`DECLARED-UNRESOLVED` · the 338's pets are unlifted (Q91 carry) · the `chainInitial`/`chainNext`
enumeration gap in `x8` · the 15 provenance-less DBR-path files · E/W shield-handedness (`R-C8-7`,
deferred by Matt) · ⚑ `C-k`, `C-l`, `C-m`, `C-m′` (§ E.2) · C-11's decomposition.

---

## § I · OPEN QUESTIONS: one lean each

**OQ-1 … OQ-8 carry v1.7's dispositions.** `OQ-1` was ruled (Q83(b)); `OQ-2` was ratified and is now
superseded forward by § F.2f; `OQ-3`'s three rows were kept; `OQ-4 / 5 / 6 / 7 / 8` stand as written in
v1.7 § I.

**OQ-9 · `TA-X-09` still grades 9 of 29, and the 20 it skips govern the mitigation order.**
→ **LEAN, unchanged: widen it in a version that exists for that purpose.** v1.8 exists because the board
moved. Folding an instrument expansion into a substrate re-derivation makes the pre-read's diff
unreadable, and that is how a goalpost moves unnoticed. It is still the first candidate.

**OQ-10 · ⚑ `TA-X-25(c)`'s class labels.** I grade the SWING/NONSWING **behaviour** and leave the
`nodata` / `measured_inert` **label** of the ten emitted but ungraded.
→ **LEAN: ratify.** The alternative is pinning a label, which reds a correct port on vocabulary (the
F.1a shape, third time on this row). **jack-ryan's pre-read should test the one place this could hide a
defect:** a port that labels an oracle-swinging record inert **reds (c)(2)**, so the label freedom does
not reach the swing decision. *I believe that closes it. It is the claim to attack.*

**OQ-11 · ⚑ `C-k`: 264 identity-path records graded by nothing.**
→ **LEAN: widen `TA-X-29(d)` in a later version**, from *"the 29 declared-inert records"* to *"every
record the resolver returns no attribute and no own term for"*, which at v3.6 is 29 + 264. Same law,
wider population, a mechanical set expression. **Not here, for OQ-9's reason.**

**OQ-12 · ⚑ The oracle does not swing default-attack bodies (`C-m′`).**
→ **LEAN: C-11, then Matt.** The game swings them (`w44`: 24 attack-animation weights, a real swing
period). The oracle's architecture needs a slot to carry weapon rows. **This is a MODEL gap in the
reference, and the right place for it is where the reference's other lethality questions already are.**
Until it is ruled, T-A grades the oracle as it is.

---

## § J · DISCIPLINES THIS VERSION EXERCISED

> ⚑ **THE GRAIN LAW, APPLIED TO A POPULATION RATHER THAN A RATE.** *"NO-DATA = 0"* was true at the
> STATE grain and false at the FIGHT grain, and the row was written at the grain nobody fights at. **At
> v1.8 every population in a graded row is defined by the predicate the fight executes, and pinned as a
> set digest.**

> ⚑ **A RELAYED FIGURE IS NOT A DERIVED ONE, AND THIS BRIEF CARRIED THREE.** `3.442` (a transcription
> slip; drax measured 3.42341) · *"the 4 non-swinging + 2"* (it is 10) · *"the 334"* as the fallback
> population (it is 158). **Each was caught by computing it and not by reading it**, and each was sent
> back to the conductor before this file was committed. The same shape as instance #7 of v1.7 § J: a
> relayed diagnosis treated as the system's behaviour.

> **Carried:** the expiry clause (`F.1a`) · the honest-`n` law · Law 3 / `#79` (no fitted constants:
> the 3.406 → 3.207764 and 5.418 → 4.980316 moves were derived, and no figure was nudged toward the port's) · `#75` cl. 1(a):
> *a pin proves what a reviewer checked, never what a builder used.* ⚑ **P-5 row 1 extends it once
> more: the fold pins name WHICH SETTINGS, and the loader call names HOW THE SETTINGS ARE PASSED.**

---

*Filed 2026-09-30 by **gamora** (simulation + spirit-guide seam), Run KC2-PLAY SEAL LAP.
⚑ **v1.8 is a FORWARD RE-DERIVATION of v1.7 for the v3.6 board: the 338 pool records armed through the
oracle's own loader (Matt Q91, KP-115; KP-122; KP-123; KP-126), with the C-11a corrections folded into the oracle
before it (Matt KP-127; C3 not folded, KP-131).** **Attempts reset to `0` of `2` under v1.8.
v1.7's attempt 1 stays on the record as spent. The declared set is closed at exactly `["TA-X-06"]`. The
seven port≠oracle holes (six at firing, hole 7 at KP-126) are seal-blocking through jack-ryan's
hole-closure finding (R-3…R-6, R-9, R-13…R-16, and hole 7's criterion), not new EXACT rows.** Every pin, both pack digests (re-computed from 17 + 7 members), four
set digests, the documents of record and all three sealed cells were re-derived this session. **NO
BAND WIDTH MINTED.** **K-7 held:** the sealed cells were hash-verified only. This file's own derivations
exercised the oracle only through `load_profiles` and the U-P-N-5 static walk. Every simulated figure
it quotes comes from a pinned, committed, non-graded artifact (P-n.1, P-n.3, P-n.4). v1.7, v1.6, v1.5, v1.4, v1.3,
v1.2, v1.1 and v1.0 are **NOT edited**.
⚑ **THIS FILE IS IMMUTABLE. Any change after a graded run exists against it is a HALT (`WARN-16`).**
**No production code. No dispatch. No push. D4 held: committed ALONE.***
