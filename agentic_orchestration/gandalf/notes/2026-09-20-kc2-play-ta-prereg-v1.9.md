# KC2-PLAY · T-A PREREGISTRATION **v1.9** — v1.8 RE-PINNED to pack **v3.6.1** (the port≠oracle holes 8–14 on the wire)

> ⚑ **STATUS: IMMUTABLE ON COMMIT. v1.9, authored 2026-09-30. SUPERSEDES v1.8 FORWARD.**
> *(The filename carries the series' `2026-09-20` prefix. The document is dated 2026-09-30.)*
>
> ⚑ **v1.9 IS A ONE-CHANGE VERSION: THE PACK OF RECORD MOVES FROM v3.6 TO v3.6.1.** star-lord cut
> v3.6.1 (KP-141) to put on the wire the inputs the port was missing for holes 8–14: to-hit, attack speed,
> Resilience, mitigation order, the DoT timeline, geometry/contact, Soulfire + bleed, and monster pets.
> The cut is **additive**: no v3.6 row was edited and no member was added. **The oracle did not move.**
> Its code and data at engine HEAD `266714dd` are byte-identical to v1.8's HEAD `96b4529a`
> (§ A.2). So **every oracle-derived value in v1.8 reproduces**, and **no row's expected value changes**.
> What does change: the pins (`P-4`, `TA-X-09`'s member pin, `substrate_epoch`), R-21's header pin
> (which KP-143 left open), the hole list on the report face, and a handful of **derivation-path
> notes** that the new wire rows force (§ A.3). **Three things are added rather than re-pinned, and are
> named so they cannot pass as a re-pin:** the pilot's description corrected to the oracle's own cell
> (§ B.1), one owed oracle-side check before firing (`H-9`, § F.2j), and one ceiling (`C-o`). § 0 is the
> v1.8 → v1.9 delta, row by row.
>
> ⚑ **ATTEMPTS: `0` OF `2` UNDER v1.9. THIS IS A CARRY, NOT A RESET.** Matt's *"Reset to 2"* (KP-115)
> attached two attempts to v1.8. **No graded run exists under v1.8** (no v1.8 verdict file exists; the
> ledger through KP-144 records none). So v1.8's allowance is carried **unspent** to v1.9. This is the
> route KP-137 names: *"no graded run exists under v1.8, so a new version, not a HALT; substrate only,
> no goalpost change."* v1.7's attempt 1 stays on the record as spent (`STRUCTURAL @ 89/89`).
>
> ⚑ **THE DECLARED SET IS CLOSED AT EXACTLY `["TA-X-06"]`** (Matt, Q83(b), KP-110). Carried from v1.8.
>
> ⚑ **THE PORT≠ORACLE HOLES ARE STILL NOT EXACT ROWS.** At v1.8 there were seven. The ledger now carries
> **holes 1–17, plus 5b, the chance gate and the C-11a grant law, plus the KP-144 loop-layer defects**.
> They are **seal-blocking through jack-ryan's repair Gate-2** (R-1…R-22 + G3, KP-144), never
> verdict-blocking (§ G.2). A v1.9 `PASS` may not be quoted without that finding (R-9, carried).
>
> ⚑ **THIS FILE IS IMMUTABLE ONCE COMMITTED. ANY CHANGE AFTER A GRADED RUN EXISTS AGAINST IT IS A HALT
> TO MATT (`WARN-16`).**
>
> ⚑ **D4 HELD. This file is committed ALONE, with zero code, before any graded run against v3.6.1
> exists.** Every digest in it was computed this session from the files and filled into the document
> by script. None was typed or copied from a ledger row. Each digest is labelled **FILE** (sha256 of one
> file's bytes) or **ROWSET** (sha256 of a law applied to rows, or to a member list), per KP-101.
>
> **Authority:**
> * ⚑ **KP-137 (Matt): *"Finish the port first."*** The conductor names this version: v3.6.1 needs a
>   **prereg v1.9** re-pin, as a new version and not a HALT, substrate only, no goalpost change.
> * ⚑ **KP-141** — pack v3.6.1 cut (star-lord; engine `7664999b` prereg ALONE → `b3a29edd` cut →
>   `266714dd`). The digests were re-read by the conductor, and derived again here from the member files.
> * ⚑ **KP-143** — the port-completion pass on v3.6.1. *"R-list: done except R-21's header re-pin (needs
>   prereg v1.9)"*. **v1.9 supplies that pin (§ B.5a).**
> * ⚑ **KP-144 (d)** — gamora writes v1.9 **in parallel with drax's pass 2**. *"It pins the pack, not the
>   runtime, and D4 commits it alone."* **v1.9 therefore does not extend `P-5` to the loop-layer
>   systems of KP-144 (b).** It names them (§ 0.5).
> * **Carried from v1.8 without change:** Q83(b), Q85, Q87, Q91, KP-115, KP-127, KP-131, KP-132 (C-11b
>   declared, not folded), F5 (the tolerance half gates nothing), jack-ryan's v1.8 pre-read (R-17…R-22).
>
> **Author:** gamora (simulation + spirit-guide seam), Run KC2-PLAY. **Decision rules only. NO BAND WIDTH
> IS MINTED, AND EVERY WIDTH IN `P-a` STAYS VOID.** **v1.8 (`69e1de18…`) and every earlier version are
> NOT edited.**

---

## § 0 · ⚑ THE v1.8 → v1.9 DELTA

**Legend.** **CARRIED** = the assertion, its expected value and its derivation are unchanged. Where the
value is a substrate property it was recomputed and reproduced. **RE-PINNED** = only a digest moves.
**NOTE** = the assertion and the value are unchanged, but a v3.6.1 wire row changes **how the row is
derived or which population it reads**, and the note says so. No row is **RE-DERIVED to a new value**
and no row is **CORRECTED**.

### 0.1 · Preconditions

| id | v1.9 | Δ value | why |
|---|---|---|---|
| `P-1` coverage 89/89 | **CARRIED** | none | a census property. The port-completion pass may move census mappings. **Read the four-way counts off the run** |
| `P-2` stream disjointness | **CARRIED** (within-epoch probe; the epoch is now v3.6.1, § C.7) | none | — |
| `P-3` roll population / law | **CARRIED.** POOL-466 recomputed: 466, set digest reproduces | none | `waves.json` is byte-identical v3.6 → v3.6.1 |
| `P-4` pack identity | ⚑ **RE-PINNED v3.6 → v3.6.1** (model + reference + cross-pin) | digests only | KP-141 |
| `P-5` oracle fold settings | **CARRIED: the same eleven settings, the same values, the same line numbers** (the oracle code is byte-identical). ⚑ **NOTE on setting 6** (§ A.3 item 6) | none | the measured board that setting 6 attaches is now ALSO the oracle's PTH source (H1). It is not a new setting |

### 0.2 · EXACT rows (28) and the declared row

| id | v1.9 | Δ expected value | Δ derivation path / population |
|---|---|---|---|
| `TA-X-01` | **CARRIED** | none | none |
| `TA-X-02` | **CARRIED** | none | none |
| `TA-X-03 / 04 / 05` | **CARRIED IN FORM**; the port's digests move (§ C.7) | none | none |
| `TA-X-06` | **UNGRADEABLE-declared, CLOSED** | — | — |
| `TA-X-07` | **CARRIED VERBATIM** | none | ⚑ **NOTE (§ A.3 item 5):** the v3.6.1 DoT timeline (D10) has three places where offered DoT does not land. Each must be booked. R-11 is re-measured on the graded runtime |
| `TA-X-08` | **CARRIED** | none | none |
| `TA-X-09` | ⚑ **RE-PINNED** (`math_rules.json` FILE `331fd552…` → `969f8090…`) | none: **the 15 rules and 29 vectors are content-identical; the nine graded vectors are unchanged** | ⚑ **NOTE (§ A.3 item 3):** v3.6.1 names V6-RULE-1's order TEXT as contradicted. That rule's vectors are `C-h`'s, not `TA-X-09`'s, and **the vectors themselves encode ARMOUR-then-RESIST (19/19)** |
| `TA-X-10` | **CARRIED**; recomputed `43.758085029822276` | none | ⚑ **NOTE (§ A.3 item 1):** the bound is no longer true BY CONSTRUCTION. G12's separation fold can move a body outward, and nothing clamps that move. Population: roster movers. **Owed before firing: `H-9`** |
| `TA-X-11` | **CARRIED** | none | ⚑ **NOTE (§ A.3 item 1):** exposed to the same mechanism. `H-9` |
| `TA-X-12` | **CARRIED** | none | none |
| `TA-X-13` | **CARRIED** | none | NOTE: v3.6.1 `S13-CRIT` confirms Soulfire multiplies by `CritLimb.LO` = **1.0** in the graded cell. No player crit anywhere |
| `TA-X-14 / 15` | **CARRIED** | none | none |
| `TA-X-16` | **CARRIED**; recomputed 54 / 47 | none | none |
| `TA-X-17` | **CARRIED**; recomputed 8.0 | none | ⚑ **NOTE (§ A.3 item 2), POPULATION STATED:** roster placements from a spawn point only. Monster pets (p14) are placed against their OWNER (G12-LAW-PLACE) and have no anchor |
| `TA-X-18` | **CARRIED**; recomputed `(−4.0, 0)` vs `(−5.656854249492381, 0)` | none | none |
| `TA-X-19` | **CARRIED** (GREEN-VACUOUSLY today) | none | NOTE: KP-144 (b) orders the deferred-arrival limb ported. When it lands, the row stops being vacuous. § F.5 cl. 6 derives that at emission |
| `TA-X-20` | **CARRIED** | none | NOTE: the S13 streams target the disc's hit list with no second distance test (`S13-SF-LAW`), so they inherit this row's hit test |
| `TA-X-21` | **CARRIED** | none | NOTE: the oracle's site list is the same object (code identical). **The port's threat path grew** (holes 8–17), and the no-bare-`round(` scan covers the grown path |
| `TA-X-22` | **CARRIED** | none | none |
| `TA-X-24` | **CARRIED** | none | ⚑ **NOTE (§ A.3 item 2), POPULATION STATED:** monster pets are attackers through the same `engine.is_opportunity` (`run.py:3551-3557`). One phase model covers both |
| `TA-X-25` | **CARRIED**; SWING-456 / NONSWING-10 recomputed, digests reproduce | none | ⚑ **NOTE (§ A.3 item 2), POPULATION STATED:** the spawn partition counts **pool-rolled roster bodies only**. Monster pets are not pool picks and not POOL-466 members. A port that counts them reds (c)(1) by construction |
| `TA-X-26` | **CARRIED**; (e) recomputed `0.2468965517` / 17 | none | none |
| `TA-X-27` | **CARRIED**; (d) recomputed 139 / 97 | none | NOTE: the port now draws the to-hit and crit-tier rolls (holes 8, 11). Clause (c) covers them, and G-3 is re-run against the oracle's sites |
| `TA-X-28` | **CARRIED** | none | ⚑ **NOTE (§ A.3 item 2), POPULATION STATED:** a "hit body" includes a monster pet. The oracle's pet arm leeches (`run.py` ~2855-2895) |
| `TA-X-29` | **CARRIED.** (a) block byte-identical; (e) recomputed **`3.207764` / `4.980316`**, **39 / 39 per-record values exact** | none | none |
| `TA-X-30` | **CARRIED**; `d_engage_m` recomputed 2.4 | none | ⚑ **NOTE (§ A.3 item 1):** (b)'s count is taken on the STEP's verdict. Separation runs after all motion, and a count taken on post-separation positions reds a faithful port. Population: roster movers (pets do not take `_halt_radius_m`) |

**Per-row delta in expected value: NONE, on all 28 EXACT rows and all five preconditions.**
**Gradeability changed by declaration: NONE.** Two rows, `TA-X-10` and `TA-X-11`, acquire an owed
**oracle-side check** (`H-9`) whose adverse outcome is a HALT before firing (§ A.3 item 1, § H).

### 0.3 · Diagnostics, ceilings, report face, verdict file

| site | v1.9 | why |
|---|---|---|
| `TA-B-01` terminal wave | **CARRIED: `[156, 152, 155, 152, 152]`**, `player_death` 5/5 | the oracle is the same object (§ A.2). KP-143's side-by-side re-read the oracle side as 156 / 152 / 155 / 152 / 152 |
| `TA-B-15` | **CARRIED** (member grain 10/466 = 0.021459) | NONSWING-10 reproduces |
| `C-e / C-f / C-i` | **CARRIED** (×3.170 landed, the v1.8 cell) | the oracle is unchanged |
| ceilings | ⚑ **NEW `C-o`**: representation limits (KP-144 (c)) | § E.2 |
| § C.8 honest-`n` | ⚑ **NOTE**: under ORACLE the board is salt-independent (KP-144 (a)), so board-composition statistics have effective `n` = **1** per arm, not 5 | diagnostics only; gates nothing |
| § F.5 cl. 11 | ⚑ **RE-DERIVED: the hole list** (seven → the ledger's current set) | the pack this file pins exists because of holes 8–14 |
| § F.5 cl. 7 / § F.3 `TA-B-01` sentence | the version label moves (*"the v1.9 oracle, the same object as v1.8's"*). The figures do not | — |
| § G.2 hole table | ⚑ **EXTENDED** to the current set, with the closure owner | § G.2 |
| verdict file | `prereg_version: "v1.9"`; `substrate_epoch`; both pack pins; ⚑ `runtime_header` (R-21); `port_holes_printed` replaces `seven_holes_printed` | § G.3 |
| § G.1 counter | **`0` of `2` under v1.9** (carried unspent) | KP-115 / KP-137 |

### 0.4 · The counts

| | preconditions | **EXACT** | UNGRADEABLE-declared | DIAGNOSTIC ids | emitted-not-graded |
|---|---:|---:|---:|---:|---:|
| v1.8 | 5 | 28 | 1 (`TA-X-06`), closed | 19 (0 gating) | 3 |
| **v1.9** | 5 | **28** | **1 (`TA-X-06`), closed** | 19 (0 gating) | 3 |

⚑ **Q87's *"all EXACT rows green"* at v1.9 means the same 28:** `TA-X-01 · 02 · 03 · 04 · 05 · 07 · 08 ·
09 · 10 · 11 · 12 · 13 · 14 · 15 · 16 · 17 · 18 · 19 · 20 · 21 · 22 · 24 · 25 · 26 · 27 · 28 · 29 · 30`.
**Count history:** 26 (Q87) → 29 (v1.6) → 28 (v1.7) → 28 (v1.8) → **28 (v1.9). No row added or removed.**
`TA-X-23` stays struck and retired.

### 0.5 · What v1.9 deliberately does NOT fold in

1. **The KP-144 (b) loop-layer systems as `P-5` settings.** These are deferred projectile arrival,
   player summons attacking, the counterplay/sustain layer (potion, Menhir's Will, heals over time),
   the K-MILL pilot layer with patrol/alert, and energy income `/tps`. Also the **board seeding** of
   KP-144 (a): under ORACLE, `simulate_wave` is seeded with `engine_seed(9, w)` and ignores the salt.
   All of these are **oracle config the port must reproduce**, and the conductor ruled every one a port
   defect. **Whether any of them is a default-OFF setting the graded oracle must ARM** (the `P-5`
   hazard) is a question about the runtime. KP-144 (d) says this version pins the pack. **Named for the
   pre-read (OQ-14). Not folded.**
2. **`C-h` / `OQ-9` (widening `TA-X-09` to all 29 vectors).** Still not here, for v1.8's reason. v1.9 adds
   one derived fact to the question (§ A.3 item 3): **11 of the 20 skipped vectors discriminate the
   mitigation ORDER, and all of them encode the oracle's armour-then-resist.** Had they been graded,
   hole 9 would have red an EXACT row at attempt 1.
3. **`C-k` / `OQ-11`** (widening `TA-X-29(d)` to the 264 identity-path records). Not here.
4. **C-11b and REFERENT-v2.** Not here (Matt, KP-132).
5. **The side-by-side acceptance** (death wave per salt equal on all five salts, plus the G3 loop-trace
   diff; KP-144 (b)). That is the **conductor's pass-2 acceptance and a seal-path criterion**. It is not
   a v1.9 row, and `TA-B-01` stays DIAGNOSTIC (§ G.2).

---

## ⚑ PINS: EVERY PIN COMPUTED THIS SESSION, FILLED BY SCRIPT, NONE TYPED

> **The standing rule (KP-20, KP-43):** a new version recomputes every pin it carries, including the ones
> it believes are unchanged. **All carried pins reproduce v1.8 exactly.** Both pack digests are
> **recomputed from the member files** with the manifest's `pack_digest_law_exact`. They were not read
> off the manifest; they were compared to it afterwards and agree.

| # | artifact | label | **sha256 (computed 2026-09-30)** | v1.8 → v1.9 |
|---|---|---|---|---|
| P-a | `gamora/notes/2026-09-20-kc2-play-ta-band-widths.md`. Constructions only; every width VOID | FILE | `1c80f08075a1ed0e30e30b348752d2505b39994f7e2c55c348413f6e591248f9` | unchanged (reproduces v1.8) |
| P-b | `galadriel/notes/2026-09-20-kc2-play-w1-tb-expected-values-and-u-rider.md` | FILE | `d48512aa6e3c9ea70de6675750880a6c8914f0984c3cfe65c6ccb9a24403438f` | unchanged (reproduces v1.8) |
| P-c | `…/2026-09-20-kc2-play-w1-tb-expected-values.json` | FILE | `a8b85331764ba3fe90f45cf7cd6f1a25f6dc0dae4a7e7fa555c487f0b153ea0b` | unchanged (reproduces v1.8) |
| P-d | `…/2026-09-20-kc2-play-w1-tb-release-labels.json` | FILE | `15dace604c8d5bb4888223a8b25a07a038bae44431ebd194d682545c0f29c58a` | unchanged (reproduces v1.8) |
| P-e | `simulation/math/kc2-play-v3p4-roster-basis-rebase-2026-09-21.md` (lineage) | FILE | `4b7b78c834c7fbabd61700dda3e730a95ab89990bfa01470e8fb293f41ac7a73` | unchanged (reproduces v1.8) |
| P-e′ | `…/math/kc2-play-v3p3-monster-offense-prereg-2026-09-20.md` (lineage) | FILE | `27fc59378aee8c9d412f486a63864a3b2ceb5c5473520b60ad80128d47d99cdc` | unchanged (reproduces v1.8) |
| P-h | ⚑ **THE MODEL PACK** `kc2-model-pack-v3-E-s09-cp150-mech-v3p6p1-20260930_110026` (17 members, 17/17 verified: digest and bytes) | ROWSET (pack law) | `3c50e6313ed15c7b416d90fbe9e8c94b4983b30d1c3f3ceea5396f66198423dd` | ⚑ **RE-PINNED** v3.6 `4fd35330…` → v3.6.1 |
| P-h2 | ⚑ **THE REFERENCE PACK** `kc2-reference-pack-v3-E-s09-cp150-mech-v3p6p1-20260930_110026` (7 members, 7/7 verified); `cross_pin.model_pack_digest` verified equal to the derived model digest | ROWSET (pack law) | `cca68a6c2328027a11942cf76a3e737c13ad5a94e69d7e9e284f9e23178c9bd5` | ⚑ **RE-PINNED** v3.6 `4e23ffc6…` → v3.6.1 |
| P-i | `data/kc2/pm4p_leech_resistance.csv` | FILE | `cb6a008bde1e102573181968ab7f60958cd28fee07ff8736078fa092a80dd62e` | unchanged (reproduces v1.8) |
| P-j | `data/kc2/pm4l_mitigation_by_body.csv` (lineage) | FILE | `a8c1ffd97dc703419f8447f3d7bbba3903e0f14d2c2e6746a938ceefae9ecec6` | unchanged (reproduces v1.8) |
| P-k | `data/kc2/pm2_tg2_monster_timing.csv` (`ANCHOR-169`'s carrier) | FILE | `58205679e36f0e0361ccd41c844d6bc254ada034447dd1f80e2a46a2b47c7aca` | unchanged (reproduces v1.8) |
| P-l.c2 | `simulation/math/kc2-c2-per-cast-energy-cost-fold-2026-09-28.md` | FILE | `b42684e55325bd4caf705b1e7d43462acb5c5818cd5abe3d79eb0d3b9ba6f8c7` | unchanged (reproduces v1.8) |
| P-l.c7 | `…/kc2-c7-insufficient-energy-refuse-fold-2026-09-29.md` | FILE | `072f9ab787ec840a9bc62ae76a0576fa5db7be0da0b63457851557ea164a7e1f` | unchanged (reproduces v1.8) |
| P-l.nine | `…/kc2-play-nine-winner-surface-reconstruction-2026-09-29.md` | FILE | `2c7c3679af67569fff88bb56837ea1ba37499fe9fcbeca85ab63a473b0d7a6dd` | unchanged (reproduces v1.8) |
| P-l.upn4 | `…/kc2-play-upn4-occupancy-by-pilot-2026-09-29.md` | FILE | `787d1a99d9adfedbb34bda69a3c530a653a8df3fc117969e3920c5625791a3cf` | unchanged (reproduces v1.8) |
| P-l.upn5 | `…/kc2-play-upn5-global-magnitude-fold-lift-2026-09-29.md` | FILE | `bfa44b4722ec8b7326987042101f32310c986e3fae489a4372fcc4e0dd5553c7` | unchanged (reproduces v1.8) |
| P-l.upn5A | `…/kc2-play-upn5-global-magnitude-fold-lift-ADDENDUM-2026-09-29.md` | FILE | `5323c1fa9f156e80ced5b1324e4297150cfc759c4e54426f440c33a6c9745fc6` | unchanged (reproduces v1.8) |
| P-l.q91 | `…/kc2-play-q91-338-pool-damage-lift-2026-09-29.md` (governs `TA-X-25` and `P-5` setting 3) | FILE | `d68561d59723c3295da3f0456f2fbeaefe8f5f0a30b41d29b5ff0e366966a385` | unchanged (reproduces v1.8) |
| P-l.q91a | `…/kc2-play-q91-338-pool-damage-lift-ADDENDUM-2026-09-29.md` | FILE | `b9ada804e17c01b376e64e82b7e45f66a344d1fc2fc75a0fdd1fd76c56e2cddc` | unchanged (reproduces v1.8) |
| P-l.c11a | `…/kc2-play-c11a-oracle-corrections-fold-2026-09-30.md` (governs `P-5` setting 11) | FILE | `4af38999ff0544cc9607b34da4fde29fe2c55324e9829894c516cd9837689445` | unchanged (reproduces v1.8) |
| P-l.c11aA | `…/kc2-play-c11a-oracle-corrections-fold-ADDENDUM-2026-09-30.md` | FILE | `17a068fe980869e6e344fdf3a652dc275f5cc3a3d65818f2976fe94084d48666` | unchanged (reproduces v1.8) |
| P-n.1 | `simulation/output/kc2-play-q91-pool-lift-pricing-20260930_023137.json` | FILE | `f33ce0c0cbeb00bbed7b47a6f7660f20d4aa2be1694f9f4e2486e37d27b553e2` | unchanged (reproduces v1.8) |
| P-n.2 | `simulation/output/kc2-lifted-rows-KC2PLAY-SEALLAP-W1-c2-energy-fold-20260928_232836.json` (the `x8` input `from_x8` reads) | FILE | `cc361a3fea3e24e55fdf0c8c8eaf52bcc0c729c7de0563d3c84dd0dc21202960` | unchanged (reproduces v1.8) |
| P-n.3 | `simulation/output/kc2-play-c11a-fold-pricing-NOT-A-GRADED-RUN-20260930_043045-SUMMARY.json` (`TA-B-01`'s reference; `C-f` / `C-i`) | FILE | `b6c9e7953f5b5632ec2dc51c2c8602461aef15d4721f69432444e6f777e1141e` | unchanged (reproduces v1.8) |
| P-n.4 | `simulation/output/kc2-play-c11a-landed-by-source-NOT-A-GRADED-RUN-20260930_033242.json` | FILE | `ad018b78a7f85491020a237166af797845bb5de2e562816673fbf925bb41ff1e` | unchanged (reproduces v1.8) |
| P-o | `data/kc2/c11a_aura_buff_grants.csv` (the C2 grant table) | FILE | `749d58f45eb312e7a284734a1844f2aabcfd69b7219dd1dafc55e4bb6d64792f` | unchanged (reproduces v1.8) |

### Set digests: the populations v1.9 grades over

**Law:** `sha256("\n".join(sorted(record_paths)).encode("utf-8"))`, no trailing newline. **ROWSET.**
Each was recomputed this session: POOL-466 from `waves.json`, SWING-456 / NONSWING-10 from the oracle's
`load_profiles` under `P-5`'s exact loader call (C-11a included), and FALLBACK-158 from the oracle's
`build_mover` / `monster_run_speed`.

| set | n | label | sha256 | v1.8 → v1.9 |
|---|---:|---|---|---|
| **POOL-466** | 466 | ROWSET | `33c886a11f91db1143c791ffcf9d95f7e7614e423373235231733c994c5c157b` | reproduces v1.8 |
| **SWING-456** | 456 | ROWSET | `706a61d55dc6621814fc923d7428c5b263a95ebb00e9786d12f35dd385a7a4c0` | reproduces v1.8 |
| **NONSWING-10** | 10 | ROWSET | `00b4cb0e24b43e591a2e30200979725801aad1e7c1f9b7764ebef67461816e10` | reproduces v1.8 |
| **FALLBACK-158** | 158 | ROWSET | `e8114efaa8fa678db6a26bb6e4ffb926fc2c1a15a978e3d589cf918ff17ae6cb` | reproduces v1.8 |

### Documents of record

| document | label | sha256 |
|---|---|---|
| ⚑ prereg **v1.8** (superseded, **not edited**; v1.9's only predecessor; collab `948bb8082`) | FILE | `69e1de1890a24fb9d9a4dc37cda6edfc39e6c34e45b877a2999b565b4710c49c` |
| prereg v1.7 (not edited) | FILE | `552d9faecd83d955c77f2be35991ec51e3908d9f586ab70b5a78b6c156b92896` |
| prereg v1.6 (not edited) | FILE | `db2c0ca3c6cdba022b83d0229439a3ad9e0709cd25732304ffc979a200be7b0e` |
| ⚑ jack-ryan's **v1.8 pre-read** (`qa/findings/2026-09-30-run-KC2-PLAY-prereg-v1.8-preread.md`; R-17…R-22, incl. **R-21**) | FILE | `5358cb8cc99dcf1dd998e875e911d6ae53e9046dab0d24abe28a5c83193d5dff` |
| jack-ryan's v1.7 pre-read | FILE | `ff1df4a18e9e60c1a5543edb391eded667b11711b340cd4763f3cdd204cab1ff` |
| jack-ryan's Gate-2 on attempt 1 (R-1…R-12) | FILE | `d2aa93db92122e033927f63ff61c9e6a2c13e1c7cba09a4fff20cb2382de6c37` |
| attempt-1 grade note | FILE | `9778b4de4aa05acb2396439d2ff9de264ec590475ebf56aec93f3912ba12505e` |
| attempt-1 verdict file | FILE | `9be2d56bfdc49c51c611402ec953b5f59dbfc0c866cdaf5201e0e57d74df08b2` |
| jack-ryan's v1.6 pre-read | FILE | `5a5f45d76098746ce1dbd31d0091b9a7d62f16978fb52a21ff27990181e0b6c0` |
| the grade of record (`gamora/notes/2026-09-21-kc2-play-ta-grade.md`) | FILE | `600f68a7378329c298cd69863903804a6ab7d1ee8a27f666688717f741b9c1c3` |
| the discrimination audit | FILE | `852d0bd7d637280cbc42e2ba8494ea7e163b4f6c91741f24eb0ef3da105e674a` |
| divergence register v0.3 (file form) | FILE | `5028b555313df2f4690cd96881c700c7d66a4733612894c150c2448915510444` |
| ⚑ star-lord's **v3.6.1 cut prereg** (`export/math/2026-09-30-kc2-baton-v3-6-1-cut-prereg.md`, engine `7664999b`) | FILE | `b49838e5ce918fde8ad39776b5611973d3b5f1a21b69a523a5e4d5a650be0c2c` |
| ⚑ the **v3.6.1 cut receipt** (`output/kc2-baton-v3-cut-receipt-v3p6p1-20260930_110026.json`) | FILE | `fc80bd38535d9d33cd9ee9fbaa28b779664714aec8b793dbae9c2be15c7a2633` |

### Sealed cells: hash-verified only. K-7 held (never opened for execution, never re-run)

| cell | path (`reincarnated-engine/src/reincarnated/simulation/output/`) | label | sha256 | bytes |
|---|---|---|---|---:|
| `[M-POL2]` | `kc2-checkpoint-E-s09-cp150-mpol2-20260825_114420.json` | FILE | `ad61ad2a8c799d6ef11a68436756c253f0a34fbb1052e575cdf9f9cd3a44dc5c` | 123,564 |
| `[MECH]` | `kc2-checkpoint-E-s09-cp150-mech-20260816_124031.json` | FILE | `20b05cb4ef3bd888b998cbc46c68b41a8051111c12fbcf2066d101b0a4b15f4b` | 2,125,271 |
| `[W1W]` | `kc2-checkpoint-E-s09-cp150-w1walls-20260825_220058.json` | FILE | `7a992c81ca6e56e54a53534b438a9ddf87ed42f1bf1a3d0ecc2d2f3c3db7881b` | 403,084 |

---

## § A · WHAT MOVED, DERIVED

### A.1 · The pack, member by member (v3.6 → v3.6.1)

**Model: 9 of 17 members byte-identical to v3.6; 8 moved, every move ADDITIVE at the top-level-key grain** (a sorted-key comparison finds every v3.6 top-level key content-identical in v3.6.1, except `meta.json`'s emission-identity fields; no key removed; no member added): `arena.json` (e65b7da0… → 15078b58…; changed top-level keys: none; new keys: `⚑ v3p6p1_grain_law`, `⚑ v3p6p1_rows`) · `config_of_record.json` (d34ce0d8… → 56413c9a…; changed top-level keys: none; new keys: `⚑ v3p6p1_points_to`) · `math_rules.json` (331fd552… → 969f8090…; changed top-level keys: none; new keys: `⚑ v3p6p1_grain_law`, `⚑ v3p6p1_points_to`, `⚑ v3p6p1_rows`) · `meta.json` (9282f1c1… → 4c58422d…; changed top-level keys: `emitted_at_utc`, `emitted_by`, `headline`, `lap_manifest`, `pack_revision`; new keys: `⚑ v3p6p1_port_holes`, `⚑ v3p6p1_supersession`) · `monster_kinematics.json` (8ecf4e41… → b8b1c7b4…; changed top-level keys: none; new keys: `⚑ v3p6p1_grain_law`, `⚑ v3p6p1_points_to`, `⚑ v3p6p1_rows`) · `monster_offense.json` (a7b4e0b7… → fad592f5…; changed top-level keys: none; new keys: `⚑ v3p6p1_grain_law`, `⚑ v3p6p1_rows`) · `player_kit.json` (aa9d237e… → ca199806…; changed top-level keys: none; new keys: `⚑ v3p6p1_grain_law`, `⚑ v3p6p1_points_to`, `⚑ v3p6p1_rows`) · `provenance.json` (e2a531a4… → 7d4cebb6…; changed top-level keys: none; new keys: `⚑ v3p6p1_precedence_vocabulary`). **Reference: 6 of 7 byte-identical; 1 moved:** `reference/meta.json` (874ba272… → 25874cfb…; changed top-level keys: `emitted_at_utc`, `emitted_by`, `headline`, `pack_revision`; new keys: `⚑ v3p6p1_port_holes`, `⚑ v3p6p1_supersession`). **Derived from the member files, not from the cut's receipt.** ⚑ `waves.json`, `monsters.json`, `monster_defense.json`, `controllers.json` and every reference member the rows read are byte-identical. `arena.json` moved **only** by adding `⚑ v3p6p1_rows.g12_geometry_contact`; its `spawn_points`, `placement_extents_m` and `d_engage_m` are content-identical, which is why `TA-X-10 / 17 / 18 / 30` recompute to v1.8's values.

**The eight new rowsets, with their ROWSET digests recomputed here** by the law the pack states on its
face (`sha256(json.dumps(rows, sort_keys=True, separators=(",",":"), default=str))`, `ensure_ascii`
default). Each equals the digest on the wire:

| rowset | member | hole | rows | label | sha256 |
|---|---|---|---:|---|---|
| `d10_dot_application_law` | `math_rules.json` | 10 | 7 | ROWSET | `13ce3beae4f5410422fdecaea13e12700fd8a6c098b83ec607b141ccf67d8896` |
| `g12_geometry_contact` | `arena.json` | 12 | 545 | ROWSET | `bae8d9bef455add5d73ebd527f6b6c1dff3694347ae3710fa1f3b8a7db592ded` |
| `h1_monster_to_hit` | `monster_offense.json` | 8 + 11 | 191 | ROWSET | `5f78f49c763c77e2fb1da1a2688f84b7162f1b0450a0613384ff179d5056db60` |
| `h2_monster_attack_speed_per_wave` | `monster_kinematics.json` | 8 (attack speed) | 20 | ROWSET | `37afa2404151e3fd9089323c7095aa771f034efd2a1cd6f7448f5e276dc8174b` |
| `m9_mitigation_law` | `player_kit.json` | 9 | 5 | ROWSET | `e7c7392db8a8304686084b4f0b385507944a7c8a7afd8f2b8f8c35f66e834e94` |
| `p14_monster_pets` | `monster_offense.json` | 14 | 224 | ROWSET | `738e6f298a9227940bfacfa0f55fcb397091fe4079ca88ad25272ea51f77d20f` |
| `r8_resilience_window` | `player_kit.json` | 8 (DA) | 9 | ROWSET | `8fb239b866d7cef15e37d246589e9a1378c38941c236f33af8d4378033c04588` |
| `s13_secondary_streams` | `player_kit.json` | 13 | 22 | ROWSET | `960bb9cdab9f58c6fec408831bb5abaa65db2e869551ad9cbd68b4920112eeac` |

### A.2 · ⚑ The oracle did not move, so no oracle-derived value moved

* `git diff --quiet 96b4529a 266714dd -- src/reincarnated/simulation data` exits **0**. The
  engine commits since v1.8's HEAD touch only `export/`, `output/` (the two v3.6.1 pack directories
  and the cut receipt) and one export test. **The oracle's `kc2/` tree is git tree object `d974998f805b8bc5d620f27d88dd4e8f14972357` at both commits** (a git tree id,
  neither FILE nor ROWSET; shown as an identity only). The working tree is clean on `simulation/kc2`
  and `data/kc2`.
* **The oracle does not read the pack.** It reads its own code and `data/`, and the pack is emitted FROM
  it. So a pack cut cannot move an oracle value. **It was recomputed anyway**, because a byte identity
  proves the input did not move, not that the reading of it was right:
  * POOL-466 / SWING-456 / NONSWING-10 / FALLBACK-158: all four set digests reproduce (see the set
    table). 466/466 profiled, and `swing ∩ 338 == u5 CONSTRUCTED`;
  * `TA-X-29(e)`, config E: **`3.207764` at w159, `4.980316` at w160.** All **39** per-record ratios and
    `on` / `off` sums equal v1.8's § F.2h table exactly. The ten-wave walk reproduces too (§ F.2h);
  * `TA-X-26(e)`: ARMED-464 mean `0.2468965517`, median 0.25, max 0.35, min 0.0, 17 leech-immune;
  * `TA-X-10`: `max‖spawn_xy‖ + placement_extents_m = 35.758085029822276 (p01) + 8.0 =
    43.758085029822276`;
  * `TA-X-16` 54 / 47 · `TA-X-18` 4.0 vs 5.656854249492381 · `TA-X-27(d)` 139 / 97 ·
    `TA-X-30` `d_engage_m` 2.4 · `C-k` 264 (all in the 338);
  * `TA-X-29(a)`: `⚑ v3p4p2_fold_completeness` is content-identical (193 / 154 · 527 / 104).
* **`TA-B-01`'s reference `[156, 152, 155, 152, 152]` stands unchanged.** It is a property of the same
  oracle object. KP-143 (drax's side-by-side on v3.6.1) independently reports the oracle side as
  156 / 152 / 155 / 152 / 152. *Relayed from the ledger, and consistent; not the source of the value.*

### A.3 · ⚑ WHAT THE v3.6.1 ROWS DO TO ROW DERIVATIONS (read every new rowset against every row)

**1 · G12 separation vs `TA-X-10` / `TA-X-11` / `TA-X-30`.** `G12-LAW-CONTACT` puts on the wire what
the driver of record has always run. With `contact_response='separate'`, no body is blocked during
motion. The board is then repaired ONCE per tick, after all motion, by a converging separation solve
with the player FIXED. *"Separation displacement is NOT speed-limited"* (`G12-LAW-SOLVE`: no damping, no
speed limit). The oracle runs the steps in this order: `m.step` → `arena_fold.clamp_body(m, pre_xy)`
(`run.py:2229-2251`) → … → the separation solve (`_pet_motion_and_separation`, `run.py` ~2573-2582;
`separate_overlaps_converging` at `:1926`). **The wall clamps the step. It never clamps the
separation displacement.**
* **`TA-X-10`.** The supremum `43.758085029822276` was derived as `max‖spawn_xy‖ + placement_extents_m`.
  That derivation rests on `arena_fold.clamp_body`'s own premise: *"Bodies pursue INWARD and no fold in
  this sim drives a body outward"* (`arena_fold.py:282-283`). **G12 is a fold that drives bodies
  outward.** A body near the rim of p01's box can be pushed past 43.758 m, and `clamp_body` then
  measures `r > R_wall` before any clamp. ⚑ **The bound held in the oracle's sealed `[W1W]` cell
  (max 43.404994665356945, a 0.353 m margin). But it held EMPIRICALLY, at the v3.3 epoch, with 122
  swinging records. It does not hold by construction. It has never been measured on the oracle at
  the v3.6 epoch.** Until hole 12 the port had no separation, so its bodies really did move only
  inward. **The port now runs the mechanism the bound assumes away.**
* **`TA-X-11`** (`n_wall_clamps_body == 0`) sits on the same mechanism. `clamp_body` fires on the step
  after an outward push.
* **The expected values do not change** (they are the wire's arithmetic). **What changes is the
  row's `F.1a` status:** a red could now come from the ORACLE's own mechanism rather than a port
  defect. **So `H-9` is owed before firing:** one non-graded ORACLE run of the `W1` arm under `P-5`,
  salts 0–4, printing `max_body_radius_m` and `n_wall_clamps_body`. The law for both outcomes is in
  § F.2j. **This version does not predict the measurement.**
* **`TA-X-30` (b)** counts a halt on the step's verdict (`travel = min(v·dt, max(0, dist − d_engage_m))`).
  A halted body can be displaced by separation afterwards. **A count taken on post-separation positions
  reds a faithful port.** This is a clarification of where the count is taken. The assertion is unchanged.

**2 · p14 monster pets vs the rows that say "body".** Until hole 14 the port had no monster pets, so
"body" had one meaning. At v3.6.1 it has two. **The oracle's populations, read from its code:**

| row | population in the oracle | site |
|---|---|---|
| `TA-X-10 / 11` | **roster movers** (`clamp_body` runs inside the `on_board` mover loop) | `run.py:2229-2251` |
| `TA-X-17` | **roster placements from a spawn point** (`observe_spawn`; `aid = w{wave}_a{i:03d}`) | `run.py:1443-1454` |
| `TA-X-25` (b)(c)(d), `TA-B-15` | **pool-rolled roster bodies**. Pets are not pool picks and are not in POOL-466 | the roll (`wave_engine.py`); pets live in `pet_state` |
| `TA-X-30` | **roster movers** (only `m.step` takes `_halt_radius_m`) | `run.py:1598-1601`, `:2235` |
| `TA-X-24` | **roster AND pets**: both are `attackers` gated by `engine.is_opportunity` | `run.py:3551-3557`, `:3613`, `:3749` |
| `TA-X-28` | **roster AND pets**: a hit pet is a hit body, and it leeches (*"A pet is a body … it leeches like anything else"*) | `run.py` ~2855-2895 |

⚑ **This names populations the oracle already had. It restricts nothing and widens nothing.** A port
that counted pets into `TA-X-25`'s counters would red `(c)(1)` (a non-member key) for a reason that is
not a defect. A port that left pets out of `TA-X-28`'s hit loop would pass `(b)` while being wrong.
**Both are closed by stating the population.**

**3 · M9 vs `TA-X-09` and `C-h`.** v3.6.1 adds a pointer: *"V6-RULE-1: ⚑ CONTRADICTED: this row's order
text puts RESIST before ARMOUR, while V0-08 == ARMOUR_THEN_RESIST."* V6-RULE-1 is a row of record for
`RULE-MONSTER-TO-PLAYER-MITIGATION-ORDER`. That rule's 20 vectors are **`C-h`**, which is not graded.
`TA-X-09` grades the **nine** vectors of `RULE-CHANNEL-MOVEMENT` (2), `RULE-RELEASE-TYPE-A` (2),
`RULE-RELEASE-TYPE-B` (1), `RULE-CAST-INTERRUPT-BINDING-EXCLUSIVITY` (2) and `RULE-DMG-APPLIED` (2).
**None of them encodes a mitigation order. `TA-X-09` is untouched.** ⚑ **And the contradiction is in
the TEXT only.** Replaying the 20 vectors both ways, **19 of the 19 non-immune vectors reproduce
ARMOUR-then-RESIST**, and resist-then-armour reproduces only the 8 with zero resist or zero armour
(e.g. `V6-VEC-04`: 26,029.38 armour-first vs 25,905.90 resist-first; the vector says 26,029.38). **11 of
the 20 discriminate the order.** This bears on `OQ-9` (§ I). It changes no v1.9 row.

**4 · S13 vs `TA-X-13` / `TA-X-20`.** `S13-CRIT`: Soulfire's applied damage is multiplied by
`crit_mult`, and the graded driver binds `CritLimb.LO.multiplier = 1.0` (bleed takes no crit). So
`TA-X-13`'s *"no player crit"* holds on the new stream. A port binding HI (1.5) there would be wrong
while booking no crit event. **Recorded; the row's `V0 · CritLimb LO` basis already covers it.**
`S13-SF-LAW` targets exactly the disc's hit list with no second distance test, so the streams sit
under `TA-X-20`'s hit test.

**5 · D10 vs `TA-X-07`.** At v1.8 the port landed a DoT once, as its per-second rate (hole 10). At
v3.6.1 it burns per 100 ms bucket on the oracle's timeline. **Offered DoT fails to land at three
places:** `n_buckets = int(duration_s × 10)` truncation (`D10-LAW-3`, R-DOT-2); the burn slot stops at
`hp <= 0` (`D10-LAW-5`); and pending and live buckets are discarded at `close_wave()` (`D10-LAW-6`).
`TA-X-07(a)` balances only if each is booked in one of the six sinks, or if DoT enters `offered`
only at burn. **The row does not choose between the two bookings, and v1.9 does not either.** ⚑ A stream
booked nowhere satisfies the identity VACUOUSLY. That is hole 1's shape (the PCL drop was booked), and
it is named as a trap (§ E.1 trap 12), not a row. **Depth:** the cell has 6,686 burn ticks
(star-lord's cut prereg § 0), so R-11 must be re-measured on the graded runtime. KP-143 reports *"R-11
max 257 terms"* on runtime `d8e38823…` (relayed). **That is relayed, not derived here, and pass 2 changes the
runtime.**

**6 · H1 vs `P-5` setting 6.** On the measured board **the oracle READS its PTH; it does not compute
it** (`MeasuredBoardFold.pth_for`; 1,829 board + 1,143 fallback packets on the cell, KP-141). The board
is `monster_measured_board`, which setting 6 already attaches. **So setting 6's consequence widens**:
a port with the board detached now misses PTH as well as the attribute limb. The setting, its value
and its site do not change. `P-5` stays at **eleven**.

**7 · Two relay defects found while deriving, recorded so nobody builds on them.**
* **Hole numbers 15 and 16 are swapped between two ledger rows.** KP-139 says *"(15) cadence … (16)
  resist cap"*. KP-143 and drax's commits (`15027e5` *"hole 15: the player resistance cap"*, `6e0b094`
  *"hole 16: the Crucible's per-wave attack speed (S1) and OA adds (O1)"*) say the reverse. **v1.9
  follows the committed record: 15 = resist cap, 16 = attack speed + OA adds.** Reported to the
  conductor.
* **The pilot of record.** v1.8 § B.1 names the pilot as *"`DRIVE_TO_PACK` + the M-POL-2 channel
  policy"*. The cell that `TA-B-01`'s reference and R-22's side-by-side run is U-P-N-4's
  **`SEALED-KMILL`**: `DRIVE_TO_PACK` with `seek_fold=True` and `kinematics=True` (*"L2 DrivePolicy then L5
  MillWalk/K-MILL (board-blind). ⚑ THE SEALED T-A PILOT"*, `gamora_kc2_upn4_occupancy_by_pilot_2026_09_29.py:89-93`).
  KP-143 lists the K-MILL layer as not ported. **v1.9 § B.1 names the pilot by its cell (§ B.1)** so the
  port reproduces the whole pilot, not its first layer. This is a description corrected to the
  oracle's own config. It is not a new setting (OQ-14).

---

## § B · CONFIGURATION AND PRECONDITIONS: five

### B.1 · `ORACLE` *(carried from v1.8 § B.1, with one description corrected)*

**Carried BY REFERENCE from v1.8 § B.1** (pinned `69e1de18…`): `V0`, five arms (`M0`, `M-POL-2`,
`M-POL-2-NULL`, `W1`, `W1-NULL`), five salts, 25 headless runs, the limbs of record, the resolved-limb
diff against `V0` (`v0_limb_set`), refuse-to-boot on an unset limb, and the declared fight scope of waves
151–160. ⚑ **The `v0_limb_set` diff now reads v3.6.1's pointers beside the V0 rows it names:** `V0-24` →
`R8-LAW` (the Resilience window), `V0-39` → `G12-LAW-CONTACT`, and `V0-40` → `G12-LAW-SOLVE`
(`config_of_record.json :: ⚑ v3p6p1_points_to`; the target rows are byte-unchanged).
⚑ **Pilot, corrected (§ A.3 item 7):** **U-P-N-4's `SEALED-KMILL`**: `PlayerPolicy.DRIVE_TO_PACK`,
`seek_fold=True`, `kinematics=True` (L2 DrivePolicy then L5 MillWalk/K-MILL). The player's `v_ref` is
4.0 → 5.4 m/s, with no facing model and motion law `V0-04`.

### B.2 – B.4 · `P-1`, `P-2`, `P-3` *(carried from v1.8 § B.2–B.4 by reference; P-3's cardinalities recomputed: POOL-466 = 466, set digest reproduces)*

### B.5 · ⚑ `P-4` · PACK IDENTITY: both v3.6.1 packs and the cross-pin

```
model_pack_dir       : "kc2-model-pack-v3-E-s09-cp150-mech-v3p6p1-20260930_110026"
model_pack_digest    : 3c50e6313ed15c7b416d90fbe9e8c94b4983b30d1c3f3ceea5396f66198423dd   (ROWSET: pack law over 17 member rows)
reference_pack_dir   : "kc2-reference-pack-v3-E-s09-cp150-mech-v3p6p1-20260930_110026"
reference_pack_digest: cca68a6c2328027a11942cf76a3e737c13ad5a94e69d7e9e284f9e23178c9bd5   (ROWSET: pack law over 7 member rows)
cross_pin_verified   : reference.manifest.cross_pin.model_pack_digest == model_pack_digest
                       (3c50e6313ed15c7b416d90fbe9e8c94b4983b30d1c3f3ceea5396f66198423dd — equal: true)
```

| # | `model/` member | label | sha256 (computed) | bytes | v3.6 → v3.6.1 |
|---|---|---|---|---:|---|
| 1 | `ai_states.json` | FILE | `928ded88e74e636422cbc107bdb02ff4cf27521dc74636e5e7e0e1680bd6060e` | 2,497 | identical |
| 2 | `arena.json` | FILE | `15078b583364bd1953d8d9480f95a1194a2b01ba8915d87fa9f83dde6e6d75be` | 426,450 | ⚑ **MOVED** (additive) |
| 3 | `config_of_record.json` | FILE | `56413c9ad0be0dae4a8ad98b482b5fcf70997f14ba9203b82762ee1c8b0788d8` | 27,545 | ⚑ **MOVED** (additive) |
| 4 | `controllers.json` | FILE | `b4217daac06f2f55acb3ec68571dd7766d31ac156ee01ee903b721f26042e478` | 5,384,891 | identical |
| 5 | `math_rules.json` | FILE | `969f8090e46ed0b76bdca24792137b27530edeed8bd8b42059af1b1a7fd47eb5` | 188,172 | ⚑ **MOVED** (additive) |
| 6 | `meta.json` | FILE | `4c58422dabeed433e06177abc05413a4a0fb1d311293162171e58a64b9b5cb5c` | 85,671 | ⚑ **MOVED** (additive) |
| 7 | `monster_defense.json` | FILE | `00ffab1576577164cc132b498817d5480822df3234f3f3bcf286c0a407193aac` | 8,816,113 | identical |
| 8 | `monster_kinematics.json` | FILE | `b8b1c7b4e491aeb13981b26478c12190ec7efd892eddeeb6eef572f1766bc549` | 965,515 | ⚑ **MOVED** (additive) |
| 9 | `monster_offense.json` | FILE | `fad592f5cb1d10030ca4ddd5788f65d3e01c0fc5781a75b73e50693d5f9ea76b` | 17,763,540 | ⚑ **MOVED** (additive) |
| 10 | `monsters.json` | FILE | `3839322955b7d4af0a6c8c8b169656136a0271a7ab9bb68893a272df703701a0` | 15,211,150 | identical |
| 11 | `player_kit.json` | FILE | `ca19980677b911af20081ac8b5029f254db1607cf8ee907cd0062863b49ea587` | 142,235 | ⚑ **MOVED** (additive) |
| 12 | `projectiles.json` | FILE | `ed32ff8a648d2b3c24918cd20150f27856b371e2a45a0e699cc1c8b6c949a0e5` | 74,198 | identical |
| 13 | `provenance.json` | FILE | `7d4cebb68b7d182100e00372b8d926127086129ff25a3ea215db0b72185c0c3b` | 649,012 | ⚑ **MOVED** (additive) |
| 14 | `rng_contract.json` | FILE | `ff6f77b0d54037f61847ab7785b58db324a7a0294d666c952b85fc955127a308` | 31,824 | identical |
| 15 | `summons.json` | FILE | `6a7cc5af2bd7291b46c1beafedf2e13b70990a3f9a1a194f2092c1a64e586a93` | 111,259 | identical |
| 16 | `target_selection.json` | FILE | `e1df3cf69d2f3f91cce5ab5f9a71de4b7be4fb2372d18de2cc99517d399d68ce` | 31,936 | identical |
| 17 | `waves.json` | FILE | `38c43a9c3b35560a3dce88ac16c189cb03b120b1ba2085ae2458040113621072` | 1,087,499 | identical |

**Reference pack (7), FILE each:** `acceptance.json` `f5ce2c174cccf9a253603ac8bfc3f20b872b2e2a92c8d24e461601e64f1f9853` (4,716 B) · `actors.json` `ef03536f97fe7122e14b34ae69a26bc7616fe58fcbe5989ab3aa09e7420ea04b` (1,956,876 B) · `meta.json` `25874cfb2c266ed5d4399baee6f49e6379188e2b8bfc2a2d02956a5b38c39a07` (66,383 B; ⚑ MOVED) · `rng_tape.json` `607bf3bffd6a5a330d2ede97eebcd7139f3c218292954aa56fbf38c34e833ea0` (406 B) · `skill_interrupt_reference.json` `45522df26b1703ac2489d08e7e7fa6986255ca80e64f057279ca6b492fdf3707` (3,113 B) · `tracks.json` `bb3495218fcdeaab11d4d5e9a5d25a2e14f2fd21384bcebc7dd1f93b0b7d9bfd` (44,733 B) · `u7_heading_conditioning.json` `5ad6ab0f089d3409506f29293433849f6abcbd1bee2a2242344fe12367287c05` (3,601 B)

**The manifests themselves (FILE; not the pack digest, and not substitutable for it):** model
`manifest.json` `48b5f08421f9baa5d896e0156979b876ba9b93ea3d31a30deded10fc2d4e5783` · reference `manifest.json` `0bab34801ca35eaa39a22a6bbb2d67a218063dcf7175edb337d2d71e0b91c27f`.

⚑ **`P-4` is red on any other pack.** v3.6 (`4fd35330…` / `4e23ffc6…`), v3.5.2, v3.5.1 and v3.5 are
**not the pack of record**. ⚑ **The grader checks the runtime header first,** reading the `.app` /
runtime header's `pack_digest` **by running the binary**.

### ⚑ B.5a · R-21's HEADER RE-PIN (the item KP-143 left open)

jack-ryan's R-21 (v1.8 pre-read, `5358cb8c…`) reads: *"The header `pack_digest` reads `4fd35330…`
and the reference reads `4e23ffc6…`, both read by running the binary. All eleven P-5 settings are
verified, and the runtime refuses to boot on any unset one."* Those two values are **v1.8's `P-4`**. The
port now runs v3.6.1 (KP-143: *"the `.app` header `3c50e631…`, read by running it"*), so **under v1.8's
pins R-21 could only be red.** R-21 is jack-ryan's criterion and this file does not rewrite it. **It
supplies the pin R-21 reads.** At v1.9:

```
R-21 (a) header model pack_digest     == 3c50e6313ed15c7b416d90fbe9e8c94b4983b30d1c3f3ceea5396f66198423dd   (P-4, above; read by RUNNING the binary)
R-21 (a) header reference pack_digest == cca68a6c2328027a11942cf76a3e737c13ad5a94e69d7e9e284f9e23178c9bd5   (P-4, above; read by RUNNING the binary)
R-21 (b) P-5: the SAME eleven settings as v1.8, unchanged in name, value and site; refuse-to-boot on any unset one
```

⚑ **Two things the harness must also move** (the `H-4` class): the prereg it pins (drax's `1a2936d`
has the harness read its label **from the pinned prereg**, which must now be this file), and the
`substrate_epoch` string. **The grader verifies both on the emission, not on a commit message.**

### B.6 · `P-5` · THE ORACLE FOLD SETTINGS: ELEVEN *(carried from v1.8 § B.6 by reference, unchanged)*

**All eleven settings are carried with the same value, source and line numbers.** The line numbers
cite engine HEAD `96b4529a`, and the oracle tree is byte-identical at `266714dd` (§ A.2). The
loader call is unchanged:
`load_profiles(dot_corrections=True, pet_special_gates=None, winner_surface=WinnerSurfaceFold.from_x8(P-n.2),
pool_lift=pool_lift.load(), c11a=C11aLoader(scope=AuraScope.CLASS))`. The one v1.9 note is on
**setting 6** (§ A.3 item 6).

---

## § C · THE LAWS

**C.1–C.6 and C.8: carried BY REFERENCE from v1.8 § C** (which carries v1.7 § C, pinned
`552d9fae…`).

### ⚑ C.7 · THE EPOCH LAW, EXTENDED TO v3.6.1

> ⚑ **A v3.3, a v3.4.2, a v3.6 and a v3.6.1 PORT board are pairwise NOT draw-comparable at a fixed salt.
> No row, diagnostic or report line may compare across them.**

**Mechanism, stated before anyone measures it:** the port now draws the oracle's to-hit roll, crit tier
and chance gate at the oracle's sites (holes 8, 11 and the chance gate). It also runs separation and
monster pets. So the port's stream moves at the first swing. ⚑ **The ORACLE side is a different
case.** The oracle does not read the pack, and its code is unchanged, so **the oracle at v3.6 and at
v3.6.1 is the SAME object with the same stream.** Its v1.8 references carry over **because they were
never pack properties**, not because the epochs are comparable.
**`substrate_epoch = "v3.6.1 / model 3c50e631… / reference cca68a6c…"`** for everything graded under this
document.

### ⚑ C.8 · THE HONEST-`n` LAW *(carried, with one note)*

As v1.7 § C.8, with one note. ⚑ **Under ORACLE the board is salt-independent:** `simulate_wave` is
seeded `engine_seed(9, w)` (KP-143 (ii); the conductor ruled the port must match, KP-144 (a)). So on
**board-composition** dimensions every salt of an arm fights the same board, and **the effective `n` is
1, not 5.** The per-salt variety lives in the fight streams. **This affects diagnostics only.** No EXACT
row reads a board-composition statistic across salts.

---

## § E · OUTSIDE T-A'S REACH

### E.1 · The traps *(v1.8 § E.1 carried; trap 11 re-stated; trap 12 new)*

| # | trap | caught by | at v1.9 |
|---|---|---|---|
| 1–10 | *(carried from v1.8 § E.1 as written)* | as v1.8 | as v1.8 |
| **11** | **PORT ≠ ORACLE BELOW THE GRADED SURFACE.** v1.8 named seven holes on the attack-selection path. **The port-completion pass found the class at every layer**: combat resolution (to-hit, crit tier, mitigation order, resist cap, DoT timeline, attack speed), the board (separation, pets, the LO life block), the player's streams (Soulfire, bleed) and the loop (KP-144 (b)). **None of it is visible to any EXACT row.** The graded set grades constants, identities and counts. It never executes the port's combat against the oracle's (KP-136) | **no EXACT row, by ruling.** The R-series + G3 closure (§ G.2) | **SEAL-BLOCKING, NOT VERDICT-BLOCKING** |
| ⚑ **12** | ⚑ **A STREAM BOOKED NOWHERE SATISFIES A CONSERVATION IDENTITY VACUOUSLY.** At v3.6.1 the intake streams grow (per-tick DoT, monster pets, the Resilience window's resist terms). Any offered quantity that never enters `offered`, or never leaves through a sink, balances `TA-X-07` while being wrong | `TA-X-07` cannot see it by construction | the hole-closure finding. The G2 fixture (705/705 packets, KP-143) and G3 are the instruments that see intake |

### E.2 · Declared ceilings

**All of v1.8 § E.2 carried as written** (`C-a`, `C-b`, `C-d`, `C-e`, `C-f`, `C-g`, `C-h`, `C-i`, `C-j`,
`C-k`, `C-l`, `C-m`, `C-m′`, `C-n`, S5). The oracle is unchanged, so every oracle-side figure in them
stands (×3.170 landed; 152–156; C-11b declared). **One new:**

| # | ceiling | status at v1.9 |
|---|---|---|
| ⚑ **C-o** | ⚑ **REPRESENTATION LIMITS (KP-144 (c)).** The port holds positions in float32. 2 of 164 JSON floats are 1 ulp off. The oracle's Soulfire damage period is `0.20000000298023224` (a float32 artefact), and `V15-8`'s 0.2 is the ENERGY clock (v3.6.1 pointer) | **Declared, not defects, provided G3 shows no decision flip caused by them.** Any flip promotes them to defects (KP-144 (c)). **No EXACT row grades them.** `TA-X-07` is not reached by the position limb: per KP-143 the float32 representation is the port's positions (Godot `Vector2`), and GDScript scalar `float` is 64-bit. **Should G3 show a float32 value in the damage ledger, `C-o` does not cover it** |

---

## § F · THE GRADED ROWS

**§ F.1 (decisiveness classes, `F.1a`), § F.2a (`TA-X-26`), § F.2b (`TA-X-27`), § F.2c (closing
conditions), § F.2d (`TA-X-07`'s tolerance and R-11's law for both outcomes), § F.2e (`TA-X-06`), § F.2f
(`TA-X-25`), § F.2g (`TA-X-28`) and § F.2i (`TA-X-30`) are carried BY REFERENCE from v1.8** (pinned
`69e1de18…`), unchanged in assertion, class, tolerance and expected value. The population and
derivation notes of § 0.2 / § A.3 apply to them as written there. ⚑ **R-11's law (v1.8 § F.2d) is
re-applied at v1.9:** R-11 is re-measured on the graded v3.6.1 runtime before attempt 1, and a smoke
above 4,500 terms means the attempt does not fire.

### F.2 · EXACT rows: 28, plus `TA-X-06` UNGRADEABLE-declared (closed)

*Every assertion is restated so a grader holds one file for the rows.*

| id | statistic | basis | tolerance | v1.9 |
|---|---|---|---|---|
| `TA-X-01` | port self-determinism; the arm+salt is NAMED and MUST DIFFER from `P-2`'s | run-internal | byte-exact | CARRIED |
| `TA-X-02` | coverage 89/89, zero unmapped | census | integer | CARRIED |
| `TA-X-03` | `port(M-POL-2-NULL, s) ≡ port(M0, s)`, all 5 | `[M-POL2]` | byte-exact | CARRIED IN FORM |
| `TA-X-04` | `port(W1-NULL, s) ≡ port(M-POL-2, s)`, all 5 (not `M0`) | `[W1W]` | byte-exact | CARRIED IN FORM |
| `TA-X-05` | `port(M-POL-2, s) ≢ port(M0, s)`, ≥ 1 salt | `[M-POL2]` | exact, one-sided | CARRIED IN FORM |
| `TA-X-06` | `port(W1, s) ≢ port(M-POL-2, s)` | `[W1W]` | **EMITTED AND PRINTED, NOT GRADED** | **UNGRADEABLE-declared (Q83(b), KP-110); the declared set is CLOSED at exactly `["TA-X-06"]`** |
| `TA-X-07` | conservation over SEVEN quantities: `offered = applied + dropped + voided + pool_truncated + pcl_reclaim + counterplay_absorbed` | run-internal | relative `\|res\|/max(1,\|offered\|) ≤ 1e-12`; depth budget ~4,500 terms (v1.8 § F.2d) | CARRIED VERBATIM; ⚑ NOTE § A.3 item 5 |
| `TA-X-08` | denominator identity, both sub-identities | `[M-POL2]` 5/5 | exact | CARRIED |
| `TA-X-09` | all **9** `math_rules.test_vectors` of the five normative channel/release/interrupt/damage rules | `P-4`'s `math_rules.json` (FILE `969f8090…`) | per-vector | ⚑ RE-PINNED (nine unchanged) |
| `TA-X-10` | `max_body_radius_m ≤ 43.758085029822276` (W1), roster movers | `[W1W]` · `arena.json` | exact, ≤ | CARRIED; ⚑ NOTE § A.3 item 1; **`H-9` owed** |
| `TA-X-11` | `n_wall_clamps_{player,body} == 0`, every W1 arm | `[W1W]` | integer | CARRIED; ⚑ NOTE § A.3 item 1; **`H-9` owed** |
| `TA-X-12` | pool inertness under ORACLE: total pool damage `== 0.0` | `[W1W]` · `DIV-19` | exact | CARRIED |
| `TA-X-13` | no player crit | `V0 · CritLimb LO` (and `S13-CRIT` = 1.0) | integer | CARRIED |
| `TA-X-14` | the two DO-NOTs; a REFUSED cast is not a release | `math_rules` prohibitions | integer | CARRIED |
| `TA-X-15` | (a) p01–p04 at `t = 0.0`, p05 one burst at `t = 4.000 s` (tick 49); (b) no intra-point stagger, `GREEN-BY-CONSTRUCTION` | census `M4` / `V11` | exact | CARRIED |
| `TA-X-16` | p06 OFF: `n_pool_picks == 47`, `n_spawn_point_6_keys_rolled == 0`, and a filtered-keys counter | `waves.json` | integer | CARRIED (54 / 47 recomputed) |
| `TA-X-17` | `‖spawn_xy − anchor_xy‖ ≤ 8.0` m, **every roster placement**, arm and salt | `placement_extents_m` | exact, ≤ | CARRIED; ⚑ population stated |
| `TA-X-18` | `u₁ = u₂ = 0.5` → `(−4.0, 0.0)` | `arena.json` | exact | CARRIED |
| `TA-X-19` | arrival unconditionality; no damage predicate reads an arrival's `px, py` | `deferred_arrival.py:13-17` | integer | CARRIED (GREEN-VACUOUSLY until the arrival limb is ported) |
| `TA-X-20` | 2.99 m hit / 3.01 m miss; no angular gate; no target cap | census `D7` | exact | CARRIED |
| `TA-X-21` | quantisation rule per site + zero bare `round(` on the port's threat path | four modules | exact | CARRIED; re-verify the live site list at emission |
| `TA-X-22` | `cause == "interrupts_channel_flag"` is 0 under ORACLE | `V0`; V18+V19 | integer | CARRIED |
| ~~`TA-X-23`~~ | ~~board-roll composition~~ | struck at v1.2, retired | — | — |
| `TA-X-24` | attack phase is `ENGAGE`; `sha256(actor_id) mod n` is never evaluated — **roster and pet attackers** | `V0` | exact | CARRIED; ⚑ population stated |
| `TA-X-25` | the spawn partition, four clauses at the fight grain (v1.8 § F.2f) — **pool-rolled roster bodies** | P-l.q91 + `u5` + the oracle's profile predicate | integer identity | CARRIED; ⚑ population stated |
| `TA-X-26` | declared-join conformance, five clauses (v1.8 § F.2a) | `P-i` | integer / exact / declared-precision | CARRIED |
| `TA-X-27` | degenerate-draw consumption, four clauses (v1.8 § F.2b) | `P-4` | integer / byte-exact | CARRIED |
| `TA-X-28` | leech target law, three clauses (v1.8 § F.2g) — **every hit body, pets included** | § F.2g | integer / structural | CARRIED; ⚑ population stated |
| `TA-X-29` | global-magnitude fold conformance, five clauses (§ F.2h below) | § F.2h | integer / declared-precision | CARRIED (e) recomputed |
| `TA-X-30` | the pursuit halt, two clauses (v1.8 § F.2i); (b) counted **on the step's verdict**, roster movers | § F.2i | exact / integer | CARRIED; ⚑ NOTE § A.3 item 1 |

### F.2h · `TA-X-29`: GLOBAL-MAGNITUDE FOLD CONFORMANCE *(restated; values recomputed at v1.9)*

| clause | assertion | class | v1.9 |
|---|---|---|---|
| (a) | `PRED-GMAG-WHOLE` evaluates TRUE: attribute limb **193** records (**154** cite `pm4o_trash_terms.csv`) AND own limb **527** (**104**). A loader short of either MUST REPORT ITSELF INCOMPLETE. Grain label: `attr_limb_records: 193` beside `attr_limb_actors: 344` | EXACT · integer counts | CARRIED (block content-identical) |
| (b) | `Z5-LAW` verbatim, governed by `C5-Z5-LAW` (restated unchanged at v3.6); C3 not folded | EXACT · declared-precision | CARRIED |
| (c) | `z3` is a CHECK asserted before `own_add` | EXACT · declared-precision | CARRIED |
| (d) | the 29 inert records take the IDENTITY path, never estimated. *"unexercised: 0 of 29"*. The 264 lifted identity-path records are `C-k`, not this clause | EXACT · structural identity | CARRIED |
| (e) | the supply-weighted pre-mitigation fold ratio, **config E** (the static supply `load_profiles` builds under `P-5` setting 1, C-11a loader included, runtime grants excluded) is **`3.207764` at w159** and **`4.980316` at w160**, and **each priced record's ratio matches the tables below** | EXACT · `\|Δ\| ≤ 5e-4` per wave ratio and per record ratio | CARRIED; recomputed at engine HEAD `266714dd`, 39/39 exact |

**Per-record tables, config E. Generated from this session's walk output, not transcribed.** **L** =
supplied by the pool lift; **I** = incumbent.

| w159 (`M_inst` 1.83) | | ratio | on | off |
|---|---|---:|---:|---:|
| L | `aetherial_fleshhulk_mine` | 3.542988 | 107,680.764 | 30,392.64 |
| L | `beetle_maggot01` | 3.366517 | 79,633.54 | 23,654.58 |
| L | `chthonianrylok_ekketzul` | 3.59875 | 100,550.672 | 27,940.44 |
| I | `chthonianservitor_lunalvalgoth` | 2.546547 | 48,845.693 | 19,181.145 |
| I | `humanwendigo_darkwood_01` | 3.784114 | 47,782.013 | 12,627.0 |
| L | `korvaakmessenger_02` | 3.033476 | 86,335.987 | 28,461.075 |
| I | `korvaakmessenger_02b` (**Crucible surface**) | 3.034357 | 89,742.771 | 29,575.545 |
| L | `manticore_jaggedwaste_01` | 2.956584 | 45,188.897 | 15,284.16 |
| L | `rokwind_01` | 3.362895 | 39,355.455 | 11,702.85 |
| I | `skeletalgolem_stepsoftorment_01` | 3.120862 | 31,822.677 | 10,196.76 |
| L | `statue_templeguardian_02` | 1.960798 | 25,216.503 | 12,860.325 |
| L | `statue_templeguardian_03` | 1.960798 | 25,216.503 | 12,860.325 |
| L | `stonegryphon_templeguardian_01` | 2.762796 | 56,697.046 | 20,521.62 |
| I | `wendigo_ancient_namadea` | 4.077782 | 97,779.057 | 23,978.49 |
| I | `witchgod_finalboss` | 3.978465 | 80,028.246 | 20,115.36 |
| L | `yeti_rimehorn_01` | 3.080011 | 39,159.032 | 12,713.925 |
| | *unpriced (no profile): `proxy_w09_p01a`, `proxy_w09_p02a`, `proxy_w09_p03a`, `proxy_w09_p04a`, `proxy_w09_p05a` (5)* | | | |
| | **w159 supply-weighted** | ⚑ **3.207764** | | |

| w160 (`M_inst` 1.83) | | ratio | on | off |
|---|---|---:|---:|---:|
| L | `aetherialcolossus_galakros` | 3.80807 | 86,437.112 | 22,698.405 |
| I | `nemesis_aetherial_01` (C-11a) | 8.165613 | 235,450.515 | 28,834.395 |
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
| I | `statue_korvaaktombguardian` | 4.102804 | 111,664.686 | 27,216.675 |
| L | `wendigocannibal_h01` | 5.951244 | 42,038.4 | 7,063.8 |
| L | `wendigocannibal_h02` (C-11a: an aura leech row leaves) | 5.946459 | 47,652.363 | 8,013.57 |
| L | `wendigocannibal_h03` | 5.476449 | 18,881.261 | 3,447.72 |
| L | `wendigocannibal_h04` (C-11a) | 5.429514 | 16,533.522 | 3,045.12 |
| L | `wendigocannibal_h05` (C-11a) | 5.429514 | 16,533.522 | 3,045.12 |
| | *unpriced (no profile): `proxy_w10_p01a`, `proxy_w10_p02a`, `proxy_w10_p03a`, `proxy_w10_p04a`, `proxy_w10_p06a` (5)* | | | |
| | **w160 supply-weighted** | ⚑ **4.980316** | | |

⚑ **EMITTED, NOT GRADED: the ten-wave walk.** The oracle's config-E values, recomputed:
**3.353866 · 1.768566 · 1.899330 · 2.994929 · 1.927777 · 2.846875 · 1.979824 · 1.592632 · 3.207764 · 4.980316** (w151…w160). Identity-path priced records per wave: **8 · 94 · 73 · 4 · 53 · 5 · 69 · 95 · 0 · 0**. It gates
nothing (R-20 is jack-ryan's pre-fire criterion on it).

### ⚑ F.2j · `TA-X-10` / `TA-X-11` UNDER SEPARATION: THE LAW FOR BOTH OUTCOMES OF `H-9`

`H-9` is one non-graded ORACLE run: arm `W1` under `P-5` (geometry ON per `V0-39` / `V0-40` /
`G12-LAW-CONTACT`), salts 0–4, printing `max_body_radius_m`, `n_wall_clamps_body` and
`n_wall_clamps_player` per salt. It is a sibling cell, not a re-run of `[W1W]` (K-7).
1. **The oracle reads `max_body_radius_m ≤ 43.758085029822276` and zero clamps on every salt:** the
   rows grade as written. A port red is then a port red.
2. **The oracle itself exceeds the bound, or clamps:** a faithful port reds `TA-X-10` / `TA-X-11` **by
   the oracle's own mechanism**. That is the `F.1a` shape (a row pinned to a premise the system does
   not hold). ⚑ **The attempt MUST NOT fire.** The question goes to Matt. Any re-statement of either
   row is a **new dated prereg version committed ALONE**, never an edit to this file. **The declared
   set does not grow without Matt's word** (§ F.2e, v1.8).
3. **`H-9` is not run before an attempt:** the attempt must not fire either (§ G.1, L2).

⚑ **Why this is not a goalpost.** The rows, values and tolerances do not move. `H-9` asks whether the
premise the value was derived from still holds, and it asks this of the ORACLE, before any port result
exists. It is the same form as R-11's smoke (v1.8 § F.2d).

### F.3 · DIAGNOSTIC rows: 19 ids, 0 gating, every width VOID *(carried from v1.8 § F.3)*

⚑ **CLASS V · `TA-B-01`, reference sentence (mandatory, verbatim at v1.9):** ***"`BAND / NON-DECISIVE /
REPORT-ONLY`. A terminal wave inside or outside this band is not evidence of fidelity either way. The
oracle's sealed `M-POL-2` arm terminates at `[156, 152, 151, 151, 156]`, `player_death` on every salt.
The v1.9 oracle (the same object as v1.8's: the 338 armed, the winner surface armed, the C-11a
corrections folded) terminates at `[156, 152, 155, 152, 152]`, `player_death` on every salt, and no salt
reaches wave 160. A port that clears to wave 160 has not survived a hard board; it has failed to be in
one."*** `TA-B-15` (CLASS IV), `TA-B-13`'s and `TA-B-14`'s sentences are carried verbatim.

### F.4 · Emitted, not graded: **three** *(carried)*

Per-registered-site draw counters (29 live sites) · the tick-resolution HP trace · the ten-wave z4 walk.

### F.5 · Report-face rules: twelve

**Cl. 1–6, 8, 9, 10 and 12 are carried verbatim from v1.8 § F.5.** Changed:

7. **THE SUSTAIN SENTENCE (mandatory; version label only):** ***"`leech` and `intake` still have no
   oracle side in the seals (`C-e`). Off-seal, the v1.9 oracle (the same object as v1.8's; the C-11a
   corrections folded) KILLS THE PLAYER AT WAVES 152–156 on salts 0–4, and lands ×3.17 the referent's
   intake over waves 151–159 on the landed grain. The port's own figure is printed from this run and
   not asserted here. A GREEN T-A IS COMPATIBLE WITH ANY RELATION BETWEEN EITHER REPLICA AND THE
   REFERENT."***
11. ⚑ **THE PORT≠ORACLE HOLES (mandatory on any report, including a passing one; RE-DERIVED):**
    ***"Port≠oracle holes 1–17 (PCL dropped · death after heal · damage rows unreachable · `tree_attack`
    slots never chosen · dying slots mishandled, and 5b one dying slot per death · slot
    chance/cooldown/delay never read · the wrong march base · to-hit · mitigation order · DoT timeline ·
    monster crit tier · motion order and the contact fold · Soulfire and the bleed rider · monster pets ·
    the resist cap · attack speed and OA adds · the HI life block), the chance-gate boundary, the C-11a
    grant law, and the loop-layer defects of KP-144 (deferred arrival · player summons attacking · the
    counterplay/sustain layer · the K-MILL pilot with patrol/alert · energy income · the board seeding)
    are invisible to every EXACT row in this instrument. A v1.9 PASS is not quotable without jack-ryan's
    hole-closure finding at the same runtime digest, and the seal is blocked on any non-zero R-6
    invariant."*** It is followed by the three R-6 invariants, **printed with their values** (§ G.2).

---

## § G · FAIL TAXONOMY, THE HOLE-CLOSURE RULE, AND THE GRADED-RUN CAP

| verdict | antecedent | consequence |
|---|---|---|
| **`STRUCTURAL`** | ≥ 1 of the 28 EXACT rows RED | the port is wrong; **consumes one of v1.9's two attempts**; L2 applies |
| **`INDETERMINATE`** | 0 EXACT red, ≥ 1 of the 28 UNGRADEABLE (incl. `P-1`…`P-5` red, and `TA-X-07(c)` above its depth budget) | does NOT consume an attempt; nothing seals |
| ~~`STATISTICAL`~~ | retired at v1.5 under F5 | — |
| **`PASS`** | all 28 EXACT green, none UNGRADEABLE | ⚑ **`PASS @ coverage k/89, 28/28 EXACT rows green, TA-X-06 UNGRADEABLE-declared (Q83(b)), dilution ⟨d⟩×, substrate_epoch v3.6.1/3c50e631…, prereg v1.9`**. Never unqualified, and **never quotable alone (§ G.2)** |

**Order:** `STRUCTURAL → INDETERMINATE → PASS`; stop at the first hit. No diagnostic appears in any
antecedent. **No post-hoc widening, by anyone.** `declared_ungradeable` must be **exactly**
`["TA-X-06"]`; anything else is **C1** (non-conforming).

### ⚑ G.1 · THE GRADED-RUN CAP: **`0` OF `2` UNDER v1.9**

⚑ **The allowance is v1.8's, carried unspent** (Matt KP-115 *"Reset to 2"*; KP-137: no graded run exists
under v1.8). **Q85's four guards hold:** (1) the allowance was ruled from outside the run (Matt); (2) this
prereg is committed ALONE, every pin recomputed, before anything is graded against v3.6.1 (D4); (3)
v1.7's attempt 1 stays on the record, spent; (4) `substrate_epoch` is declared on every artifact.
**Naming:** the next graded run is **v1.9 attempt 1 (overall attempt 2)**.

⚑ **L2, AS IT APPLIES TO v1.9.** v1.9 attempt 1 fires only after ALL of the following:
- drax's **pass 2** (KP-144 (b)) has landed, with its acceptance shown: the side-by-side's **death wave
  per salt equal to the oracle's on all five salts**, plus the per-wave loop-trace diff (**G3**) on the
  oracle's own draws (the conductor's acceptance, KP-144);
- jack-ryan's **repair Gate-2 (R-1…R-22 + G3)** PASSes that runtime, on the digest it names (R-7);
- **this file's pre-read** has been filed (`H-7`);
- **R-11** has been re-measured on that runtime at ≤ 4,500 terms (v1.8 § F.2d, `H-6`);
- ⚑ **`H-9`** reads outcome 1 (§ F.2j).

v1.9 attempt 2 fires only after a v1.9-attempt-1 `STRUCTURAL` red is repaired and jack-ryan's Gate-2
PASSes the repair. An `INDETERMINATE` consumes nothing and buys nothing.

### ⚑ G.2 · THE HOLE-CLOSURE RULE: SEAL-BLOCKING, NOT VERDICT-BLOCKING *(the rule carried; the table extended)*

The holes are not EXACT rows. They cannot produce, raise or lower a verdict. They are closed, or not,
by **jack-ryan's repair Gate-2**. At KP-144 that means R-1…R-22 plus G3, with the side-by-side
acceptance above. **This file names the holes. It does not write any criterion.**

| hole | what | ledger / commit | closure |
|---|---|---|---|
| 1 | PCL dropped | KP-113 | R-3 + R-6 (iii) |
| 2 | death after heal | KP-113 | R-5 + R-6 (i)(ii) |
| 3 | damage rows unreachable (row grouping) | KP-116 | R-13 |
| 4 | `tree_attack` slots never chosen | KP-118 | R-14 |
| 5 · 5b | dying slots mishandled · one dying slot per death, the first in reach | KP-118 · KP-142 (`d54b214`) | R-15; 5b: jack-ryan's repair Gate-2 |
| 6 | slot chance / cooldown / delay never read | KP-120 | R-16 |
| 7 | march base 4.0 vs 3.209466 | KP-126 | R-17 |
| 8 | to-hit (PTH: board, else the equation) | KP-136 · `15739ff` / `18f1bc6` | repair Gate-2 + the G2 fixture (705/705, KP-143) |
| 9 | mitigation order (armour-then-resist) | KP-136 · `e213b19` | repair Gate-2 + G2 |
| 10 | DoT per 100 ms bucket on the oracle's timeline | KP-136 · `5ac8eab` | repair Gate-2 + G2 |
| 11 | monster crit tier | KP-136 · `8ab6a66` | repair Gate-2 + G2 |
| 12a · 12b | motion order (V0-39) · the contact fold | KP-136 / KP-138 · `42211fb`, `b2b55ff` | repair Gate-2 + G3; **`H-9` for `TA-X-10/11`** |
| 13 | Soulfire and the bleed rider | KP-136 / KP-138 · `987b2c9` | repair Gate-2 + G3 |
| 14 | monster pets | KP-136 / KP-138 · `6a538db` | repair Gate-2 + G3 |
| 15 | player resist cap (Bleeding 85 → 80) | KP-139 (numbers swapped there, § A.3 item 7) · `15027e5` | repair Gate-2 |
| 16 | attack speed (S1) and OA adds (O1) | KP-139 (swapped) · `6e0b094` | repair Gate-2 + G2 |
| 17 | monster life: the LO eHP block, not HI | KP-142 · `e2a6a7d` | repair Gate-2 |
| — | the chance gate: `uniform > chance` skips | KP-142 · `c1cb9a9` | repair Gate-2 |
| — | the C-11a grant law | KP-127 / KP-136 | R-18 |
| — | ⚑ **the loop layer (KP-144 (b))**: deferred arrival · player summons attacking · counterplay/sustain (potion, Menhir's Will, heals over time) · the K-MILL pilot with patrol/alert · energy income `/tps` | KP-143 / KP-144 | **pass 2 + its acceptance** (death wave per salt equal on 5/5 + G3) + repair Gate-2 |
| — | ⚑ **the board seeding under ORACLE** (`engine_seed(9, w)`, salt-independent) | KP-144 (a) | as above |
| *(all)* | — | — | R-1 · R-2 · R-4 · R-7 · R-8 · R-19 · R-20 · **R-21 (re-pinned, § B.5a)** · R-22 (disposed, KP-144) |

**R-6, the three invariants, printed on the report face and never in an antecedent:** (i) cells with
`killer_id` set and `terminal_reason == cleared` = **0** · (ii) in-tick resurrections = **0** · (iii)
`PercentCurrentLife` intake **> 0** wherever a PCL row fired.

⚑ **R-9, carried as law of this instrument:** (1) **a v1.9 `PASS` is not quotable** unless it is quoted
together with jack-ryan's hole-closure finding GREEN at the SAME runtime digest (R-7); (2) **any non-zero
R-6 invariant blocks the seal**, not the verdict; (3) **Q87's seal at v1.9** = `PASS` (28/28) AND
coverage 89/89 AND T-B reported DIAGNOSTIC AND the hole-closure finding GREEN at the graded digest with
R-6 at its stated values AND **Matt's T-C yes on that same digest** (KP-114).

### G.3 · Verdict file `kc2play.ta_verdict.v1` (v1.9): **the fields that change from v1.8 § G.3**

```
prereg_version                    : "v1.9"
prereg_sha256                     : <this file, derived at emission>
substrate_epoch                   : "v3.6.1 / model 3c50e631… / reference cca68a6c…"
model_pack                        : {dir: "kc2-model-pack-v3-E-s09-cp150-mech-v3p6p1-20260930_110026", digest: 3c50e631…, files_verified: 17}
reference_pack                    : {dir: "kc2-reference-pack-v3-E-s09-cp150-mech-v3p6p1-20260930_110026", digest: cca68a6c…, files_verified: 7}
cross_pin_verified                : true
runtime_header                    : {"model_pack_digest": <read by RUNNING the binary>, "reference_pack_digest": <same>,
                                     "must_equal": "P-4 (§ B.5)", "read_by_running": true}      ⚑ R-21 (§ B.5a)
preconditions.P4_pack             : {"model":<dir>,"reference":<dir>,"files_verified":24,"mismatches":0,"cross_pin":true}
oracle_containment_H9             : {"max_body_radius_m": [<5 salts>], "n_wall_clamps_body": [<5>], "n_wall_clamps_player": [<5>],
                                     "outcome": 1|2}     ⚑ § F.2j; ORACLE side; report face, never an antecedent
port_holes_printed                : true    (§ F.5 cl. 11, re-derived; replaces seven_holes_printed)
```

**Every other field is v1.8 § G.3 unchanged**, including `set_digests` (the four digests reproduce),
`P5_folds` (eleven, unchanged), `declared_ungradeable` (**exactly** `TA-X-06`), `gmag_conformance`
(`terminal_multiplier` `3.207764` / `4.980316`), `nodata` (roster bodies, § A.3 item 2) and
`hole_closure`. **T-B quoting cap: C1 / C2 / C3 unchanged.**

---

## § H · OWED BEFORE v1.9 ATTEMPT 1 (blocking)

| # | owed | owner | why it blocks |
|---|---|---|---|
| **H-1** | the port on v3.6.1 **with pass 2** (KP-144 (b)): the loop layer, the ORACLE board seeding, and the side-by-side acceptance (death wave per salt equal on 5/5 + G3). KP-143 landed the combat-resolution layer (runtime `d8e38823…`, 63 members, **relayed** from the ledger; G2 705/705) | **drax** | the port does not yet fight the oracle's board or loop (KP-143: port w151 on 5/5 salts vs oracle 152–156) |
| **H-2** | `spawn_by_record` per arm per salt, **over roster bodies only** (§ A.3 item 2) | drax | `TA-X-25(c)` is UNGRADEABLE without it; a pet in it reds `(c)(1)` |
| **H-3** | `TA-X-29(e)`'s probe values: `3.207764` / `4.980316` + the 39 per-record values (**unchanged from v1.8**) | drax | R-1 |
| **H-4** | ⚑ **the harness re-pointed to THIS file** (its label is read from the pinned prereg, `1a2936d`) and `substrate_epoch` = v3.6.1; every stale field restated (R-10) | drax | read literally, a v1.8-pinned harness mislabels a v1.9 run |
| **H-5** | the hole-closure finding at the graded digest (§ G.2) | **jack-ryan** | `PASS` is not quotable without it; the seal is blocked on R-6 |
| **H-6** | R-11 re-measured on the graded runtime (v1.8 § F.2d) | drax | above 4,500 terms the attempt must not fire |
| **H-7** | **this file's pre-read** | **jack-ryan** | D4 / the series' practice |
| **H-8** | Matt's T-C re-confirm on the graded digest | Matt | a seal condition, not an attempt precondition |
| ⚑ **H-9** | ⚑ **the ORACLE's `W1` containment under separation** (§ F.2j): `max_body_radius_m`, `n_wall_clamps_{body,player}`, salts 0–4, `P-5`, geometry ON; non-graded, committed as its own artifact | **gamora** | outcome 2 would red `TA-X-10/11` on a faithful port; the attempt must not fire into it |

**Not blocking, named so they are not lost:** v1.8 § H's list, carried · `C-o` · OQ-13 · OQ-14 · the
KP-139/KP-143 hole-number swap (routed to the conductor).

---

## § I · OPEN QUESTIONS: one lean each

**OQ-1 … OQ-12 carry v1.8's dispositions.** Two gain a fact, and two are new:

**OQ-9 · `TA-X-09` grades 9 of 29 vectors** → **LEAN, unchanged: widen it in a version that exists for
that purpose.** ⚑ **New fact (§ A.3 item 3):** 11 of the 20 skipped vectors discriminate the mitigation
order, and all 20 encode the oracle's armour-then-resist. **Hole 9 was a port defect that the
instrument had the vectors to catch and chose not to grade.** That makes it the strongest candidate
the series has for its first instrument-only version.

**OQ-11 · `C-k`** → **LEAN, unchanged.**

⚑ **OQ-13 · `TA-X-10` / `TA-X-11` under separation.** → **LEAN: measure the oracle first (`H-9`), and do
not touch the rows before that.** If outcome 1, nothing moves. If outcome 2, the honest restatement is
the **same bound over PRE-SEPARATION positions** (the step's own position, where the wall acts), because
that is the quantity the derivation bounds. **That is a new version, and Matt's to rule.** *This is
the claim to attack: that a bound derived from spawn geometry never covered a displacement the wall
does not see.*

⚑ **OQ-14 · Loop-layer oracle config and `P-5`.** KP-144 (b)'s systems and the board seeding are ORACLE
config. → **LEAN: when pass 2 lands, derive for each whether it is a default-OFF setting the graded
oracle ARMS** (`deferred_arrival`, the K-MILL flags `seek_fold` / `kinematics`, energy income, and
`simulate_wave`'s seed). **Any that is becomes a `P-5` row in a later version**, the way `pool_lift`
did. The pilot is already corrected here as a description (§ B.1), because it was always the oracle's
config and v1.8 named only its first layer. *I do not add settings to `P-5` in a version the conductor
scoped to the pack.*

---

## § J · DISCIPLINES THIS VERSION EXERCISED

> ⚑ **A ONE-CHANGE VERSION STILL READS EVERY NEW ROW AGAINST EVERY OLD ROW.** v3.6.1 was cut to feed the
> port, not to move the instrument, and it moves no expected value. **Reading its 1,023 rows against the
> 28 EXACT rows still found a bound that was true only because the port lacked a mechanism** (§ A.3
> item 1). It also found populations that had one meaning until the port gained pets (item 2), and a
> contradiction that lives in text and not in vectors (item 3). **A substrate that "only adds" can
> still falsify a derivation.** It does so by making a premise observable.

> ⚑ **A PREMISE IN A DOCSTRING IS A DERIVATION INPUT.** `clamp_body`'s *"no fold in this sim drives a
> body outward"* was true of the fold set when it was written. The separation fold was ON in the driver
> of record, and the premise was never re-read against it. **The same shape as C-11c's stale docstring
> (KP-134).**

> **Carried:** Law 3 (no fitted constants: no value in this file moved, and none was nudged) · the
> `F.1a` expiry clause · the honest-`n` law · `#75` cl. 1(a) · KP-101 (every digest labelled FILE or
> ROWSET) · **digests computed and filled by script, never typed.**

---

*Filed 2026-09-30 by **gamora** (simulation + spirit-guide seam), Run KC2-PLAY.
⚑ **v1.9 RE-PINS v1.8 FROM PACK v3.6 TO PACK v3.6.1** (KP-137, KP-141, KP-143, KP-144 (d)).
**No expected value moved on any of the 28 EXACT rows or the five preconditions.** The oracle is
byte-identical to v1.8's, and every oracle-derived value was recomputed and reproduces. **Attempts:
`0` of `2`, carried unspent from v1.8.** The declared set is closed at exactly `["TA-X-06"]`. **R-21's
header pin is supplied** (§ B.5a). **`H-9` is new and owed by this seat.** **NO BAND WIDTH MINTED.**
**K-7 held:** the sealed cells were hash-verified only. This file's own derivations exercised the
oracle only through `load_profiles`, `build_mover` / `monster_run_speed` and the U-P-N-5 static walk.
v1.8 and every earlier version are **NOT edited**.
⚑ **THIS FILE IS IMMUTABLE. Any change after a graded run exists against it is a HALT (`WARN-16`).**
**No production code. No dispatch. No push. D4 held: committed ALONE.***
