# Finding — 2026-10-01 — Run KC2-PLAY · H-5 · THE HOLE-CLOSURE FINDING AT THE GRADED DIGEST `d03ca891`

**Reviewer:** jack-ryan (DEV-MODE, gatekeeper for Run KC2-PLAY; conductor gandalf)
**Severity:** **H-5 DISCHARGED (0 BLOCK · 1 WARN · 7 INFO).** Every hole and repair item is closed at `d03ca891`, by a commit that is an ancestor of the graded commit. Each is pinned by a fail-first probe that is GREEN at the graded digest, with its negative control RED; I re-ran all 125 controls. None re-opened. The R-6 invariants read 0 / 0 / 0. **Seven items are closed but un-exercised by any graded row or G3 class. They are listed in § 5, not hidden.**
**Target:** graded runtime FILE **`d03ca8913901d61de73db40287e31e498e8b2714521f8221fde414682e328ccd`** (85 members) at godot `7a97716`. `kc2_runtime/` is byte-identical at `0f36826` and `7a97716`. Graded emission: `evidence/kc2-play/2026-10-01-ta-attempt2-v1.13-cells/` (MANIFEST 28 members, 0 mismatches; `ta_verdict.json` `f7e19dc1…`; `ta_manifest.json` `9e35fb2e…`). G3: `evidence/kc2-play/2026-10-01-g3-25cell-kp184/` (MANIFEST `f861b7a1…`). Pack v3.7.1: model `48a4c94c…`, reference `1887257f…`. Oracle: engine `22cd2288`. Prereg of record: v1.13 FILE `c35cca9c…`, carried base v1.12 `a0454776…`.
**Developer:** drax (port) · gamora (grade of record, concurrent; not read, not touched) · gandalf (conductor)
**Principles applied:** REVIEW_PROCESS #1 (math before code), #4 (the committed record is the truth), #5 (severity matters). Disciplines #10 (attribution), #11 (empirical inspection over assumption), #12 (semantic shifts named). ADR-002. Charter KP-113 → KP-188. Prereg v1.13 § F.5 cl. 7, 11, 13; § G.1, § G.3, § H (H-5); v1.12 § G.2 (the hole table, carried); KP-178 laws (a) and (b).

**Read-only attestation.**
- I read godot only through git objects (`git show`, `git log`, `git diff`, `git merge-base`) and a `git archive 7a97716` of `kc2_runtime/`, `project.godot`, `icon.svg` and the two evidence folders, extracted into my scratchpad under `h5/`.
- Every Godot run held the heavy lock and wrote only to scratch: the full suite, G3 port side ×25, and the G2 fixture.
- The engine and the v3.7.1 pack were read only. No engine code was executed.
- **gamora's grading files were not opened.** Her attempt-2 scratch (`a2/`, `pr/`) was not read or written.
- This file is the only thing I wrote to a repo.

**What this finding is and is not.**
- It is the seal condition named in v1.12 § G.2 R-9, carried by v1.13 § G.3 and § H. A v1.13 `PASS` is quotable only beside this finding at the same runtime digest.
- **It does not grade attempt 2.** The verdict of record is gamora's. I read no graded row's value against its expected value.
- A hole is *invisible to every EXACT row* by definition (§ F.5 cl. 11). So in column (c), "exercised" means one of two things:
  - the graded run **reaches the mechanism**: a non-zero emitted counter on the port's own generator, which nothing grades; or
  - **G3 / G2 verify it against the oracle** on the oracle's own draws.

  Where neither holds, I say so.

---

## § 1 · Pins and instruments, re-derived (Discipline #11)

| claim | how I checked | result |
|---|---|---|
| graded runtime = `d03ca891…`, 85 members | `make_manifest.py`'s law recomputed over the extracted `kc2_runtime/` at `7a97716` | ✓ 85 lines, digest equal; `MANIFEST.json`'s `tree_digest` equal |
| the runtime did not move between the candidate and the graded commit | `git diff 0f36826 7a97716 -- kc2_runtime` | ✓ empty (`7a97716` adds `evidence/` only, 29 files) |
| the graded evidence is intact | evidence MANIFEST members re-hashed | ✓ 28/28, 0 mismatches. The identity block reads runtime `d03ca891…` (boot input equal), prereg v1.13 `c35cca9c…`, carried v1.12 `a0454776…`, packs `48a4c94c…` / `1887257f…`, `run_kind: attempt`, `verdict: null` |
| the graded cells are the cells my H-7 read | sha256 of each `cell.json` at `7a97716` vs the PRE-READ folder at `4833bcf` | ✓ **25/25 byte-identical.** The states the holes reach in the graded run are exactly those the H-7 read graded. *(The § G.1a item-5 face is gamora's to print. I cite this only as hole-coverage evidence.)* |
| every closing commit below is in the graded tree | `git merge-base --is-ancestor <c> 7a97716` for every godot commit this finding cites (70, excluding the evidence / HEAD commits) | ✓ 70/70 ancestors |

**The instruments I ran at `d03ca891`** (archive of `7a97716`, heavy lock):

1. **The full runtime suite** (`run_kc2_runtime_suite.sh --locked` via the lock wrapper). Output sha256 `f4bb909f…`. Every leg is GREEN, with one exception: the **attempt-2 probes read 54 checks with 2 failures**. Both failures are `runtime_header` checks, because my scratch archive has no exported `.app`. This is the same environment artefact as my H-3 INFO-C. In drax's emission, `equals_P4` and `vendored_runtime_equals_runtime_digest` are both `true`.

   | battery | checks / failures | negative controls RED |
   |---|---|---|
   | loader smoke · rules smoke | 135 / 0 · 58 / 0 | — |
   | hole probes (holes 1–7, R-4, R-5) | 56 / 0 | **13 / 13** |
   | v3.6 probes (C-11a grant law R-18 (a)–(e), R-19, C3/C4 inert, d1 + toggled aura) | 37 / 0 | **9 / 9** |
   | completion probes (holes 8–17, 5b, the chance gate, R8, R-17 (b)(d)) | 48 / 0 | **18 / 18** |
   | loop probes (KP-144 (a)(b)(c)) | 25 / 0 | **12 / 12** |
   | v3.7 probes (KP-147's ten folds, t6 text fixes, zero injections, W1 arena) | 71 / 0 | **16 / 16** |
   | v3.7.1 probes (KP-150/152 closure law, KP-155 Neumaier, KP-167 leak, census) | 57 / 0 | **15 / 15** |
   | H-4 probe | 35 / 0 | **26 / 26** |
   | attempt-2 probes (KP-177 TA-X-08 · PRE_FIGHT · P-2 · emission; KP-180 counters) | 54 / 2 *(env: no `.app`)* | **16 / 16** |
   | T-0 · purity · 30 `--check-only` legs | GREEN · 0 violations · clean | — |

   **125 / 125 negative controls RED as required.** Every battery's check count and control count equals the count at the last gate that read it (KP-143, KP-152, KP-173, my H-3). **No probe and no control has been removed since its hole closed.**

2. **G3, port side, on all 25 filed oracle traces** (`kc2rt_g3_loop_trace.gd`, zero injections), **with stdout kept this time.**
   - Summaries: **25/25 byte-identical to the filed ones.**
   - **98/98 played waves print `NO DIVERGENCE`.** That verdict covers every class the tool compares:
     - the exact DECISION classes: board, alive set, pet set, channel, drive target, damage sources per tick (with multiplicity), wave end, wave length;
     - the NUMBER classes: player and body positions **bit for bit**, player HP and **every live body's HP** at 1e-6 relative, energy at 1e-9.
   - **384 draw streams compared, 0 mismatches.** The only oracle-only streams are the two declared ones (`spawn_structure.py:344`, `player_kit_residual.py:286`).
   - Census EQUAL 25/25; control term EQUAL 25/25.
   - Native-fold counters, summed over the 25 cells (cells non-zero in parentheses):

     | fold | count |
     |---|---|
     | board `count_adj` | 435 (25) |
     | alert evaluations / fired | 1,760 / 164 (25) |
     | `kvec` covered | 4,893 (25) |
     | banner aura ticks | 3,232 (23) |
     | control observations / applications / insertions | 3,765 / 64 (20) / 40 (19) |
     | control `gate_halted` | 0 |
     | summon casts / swings | 73 / 5,067 (25) |
     | K_MILL | true 25/25 |
     | **patrol gate-closed body-ticks** | **0 (0)** |

3. **The G2 fixture** (`kc2rt_g2_fixture.gd`) at `d03ca891`, run on the oracle packet log `oracle_packets3.jsonl` (sha256 `2bafa200…`; 2,972 packets, the KP-152 re-recording).
   - **Result: 705 Leg-A packets, IDENTICAL 705.** Max relative \|port − oracle\| 4.20e-16. Differing: draw count/kind 0 · PTH 0 · hit/miss 0 · tier/mult 0 · DoT registration 0 · applied 0. Total applied 2,450,361.5 on both sides.
   - The 705 contain:

     | packet class | count |
     |---|---|
     | misses | 92 |
     | tier 0 / tier 1 / **tier 2** | 459 / 144 / **10** |
     | `tree_attack` | 15 |
     | `dying` | 43 |
     | `toggled_aura` | 17 |
     | with granted rows | 461 |
     | with DoT registrations | 383 |
     | with PCL | 105 |

   - *Provenance caveat (INFO-5): the log is a scratch file, not committed evidence. KP-175 INFO-A stands.*

4. **Leg-A event census of the 25 oracle traces** (my script; counts restricted to each cell's waves ≤ its Leg-A death wave, i.e. exactly what G3 compares):

   | event class | count | cells |
   |---|---|---|
   | hits on the player | 3,070 | 25 |
   | DoT ticks | 33,228 | 25 |
   | **Bleeding-family DoT ticks** | 3,458 | 23 |
   | `dying` hits | 160 | 25 |
   | `tree_attack` hits | 81 | 15 |
   | monster-pet hits on the player | 49 | 15 |
   | pet spawns | 2,373 | 25 |
   | `toggled_aura` hits | 58 | 20 |
   | **deferred landings** (cast tick ≠ landing tick) | 1,111 | 25 |
   | player summon hits on monsters | 3,075 | 25 |
   | potion heals | 44 | 23 |
   | Menhir's Will heals | 39 | 23 |
   | heal-over-time ticks | 1,563 | 23 |
   | control entries | 52 | 19 |

5. **The graded emission's own counters, 25 cells** (port generator, nothing graded):
   - every cell dies (terminal waves 153–160, five cells reach w160), with `n_lethal_floor_ticks = 1` and `death_order = DEATH-CHECK-AT-FLOOR-BEFORE-HEAL`;
   - PCL landed 19–218 per cell, with PCL intake > 0 on 25/25;
   - `n_dying_attacks` 9–32;
   - to-hit resolutions 121–649, with board-PTH substitutions on 25/25, crit tier ≥ 2 on 5/25, and sub-threshold scaling on the 5 w160 cells;
   - DoT registrations 26–245;
   - Soulfire procs 189–816 and bleed ticks 536–4,735;
   - monster pets spawned 4–275;
   - geometry projections on 25/25;
   - aura-grant rows applied 23–139;
   - toggled-aura applications on 25/25;
   - Resilience activations 2–6;
   - Disruption routed (U6) on 24/25, with unmapped drops `{}` on 25/25;
   - deferred `dropped` bookings after death on 9/25 and at wave end on 22/25;
   - **`n_control_suppressed` = 0 on 25/25** (the port's own generator inserts no control; § F.2n.5).

---

## § 2 · The hole table (v1.12 § G.2 as carried by v1.13): holes 1–17, 5b, the chance gate, the C-11a grant law

Column legend. **(a)** the closing commit (godot unless marked), an ancestor of `7a97716`. **(b)** the probe section at `d03ca891`, written *checks ok / controls RED*. **(c)** what exercises it: **GR** = graded emission (port generator; reached, not graded); **G3** = verified against the oracle on its draws; **G2** = verified per packet.

| hole | what | (a) closed by | (b) pinned at `d03ca891` | (c) exercised by |
|---|---|---|---|---|
| 1 | PCL dropped | `358113d` (built, fail-closed) → `23f6caa` (wired from U7-0, v3.5) | hole probes · HOLE 1 · 8 ok / 1 RED (R-3 composition inside) | **GR** PCL landed on 25/25 with intake > 0 (R-6 (iii)) · **G3** player HP at 1e-6 on 3,070 hits · **G2** 105 PCL packets identical |
| 2 | death after heal | `d3fd37b` | HOLE 2 order 11 / 1 · both loops on the real pack 5 / 1 | **GR** 25/25 die on the floor tick, `n_lethal_floor_ticks` = 1 · **G3** death wave and tick equal 25/25. ⚑ **`play_step()` un-exercised (§ 5 U-1)** |
| 3 | damage rows unreachable (grouping) | `1766c57` | HOLE 3 · 8 / 2 | **G3** damage sources per tick + HP · **G2** 705 packets, per-(record, slot) rows identical (461 carry granted rows) |
| 4 | `tree_attack` slots never chosen | `50a87d5` | HOLE 4 · 4 / 1 | **G3** 81 `tree_attack` hits in 15 cells, 0 draw mismatches · **G2** 15 packets |
| 5 | dying slots mishandled | `e747756` | HOLE 5 · 7 / 1 | **GR** 9–32 dying attacks per cell · **G3** 160 dying hits (25 cells) · **G2** 43 |
| 5b | one dying slot per death, the first in reach | `d54b214` | completion · 5b · 2 / 1 | the death path is exercised as for hole 5. ⚑ **The discriminating state (≥ 2 in-reach dying slots at one death) is not shown reached (§ 5 U-4)** |
| 6 | slot chance / cooldown / delay never read | `469ef09` | HOLE 6 · 7 / 1 | **G3** 384 streams 0 mismatches (every gate draw at its site) · **G2** draw count/kind 0 differ |
| 7 | march base 4.0 vs 3.209466 | `000608c` (+ `86a9e7d` speeds, `b1e441d` R-17 (b)(d)) | HOLE 7 · 4 / 1 · R-17 (b)(d) · 7 / 1 | **G3** every body position **bit-exact**, 98/98 waves |
| 8 | to-hit (board PTH, else the equation) | `15739ff` → `18f1bc6` (wired, h1) | completion · hole 8 · 5 / 1 | **GR** board PTH substituted 25/25 · **G3** threat-stream draws 0 mismatches · **G2** PTH 0 differ / hit-miss 0 differ |
| 9 | mitigation order (armour-then-resist) | `e213b19` | hole 9 · 5 / 1 | **G3** player HP at 1e-6 · **G2** applied 0 differ |
| 10 | DoT per 100 ms bucket | `5ac8eab` → `18f1bc6` | hole 10 · 6 / 2 | **GR** 26–245 registrations · **G3** 33,228 DoT ticks with HP at 1e-6 · **G2** 383 registrations 0 differ |
| 11 | monster crit tier | `8ab6a66` | hole 11 · 4 / 2 | **GR** tier ≥ 2 on 5/25 · **G2** 10 tier-2 + 144 tier-1, tier/mult 0 differ |
| 12a · 12b | motion order · the contact fold | `42211fb` · `b2b55ff` → `18f1bc6` | hole 12a · 4 / 1 · hole 12b · 8 / 1 | **GR** projections on 25/25 · **G3** positions bit-exact 98/98 waves |
| 13 | Soulfire and the bleed rider | `987b2c9` | hole 13 · 3 / 1 | **GR** Soulfire procs 189–816, bleed ticks 536–4,735 · **G3** every live body's HP at 1e-6 every tick, alive set exact |
| 14 | monster pets | `6a538db` | hole 14 · 4 / 1 | **GR** 4–275 pets · **G3** pet set exact; 2,373 pet spawns, 49 pet hits on the player |
| 15 | player resist cap (Bleeding 85 → 80) | `15027e5` | hole 15 · 3 / 1 | **GR** Bleeding-family intake on 25/25 · **G3** 3,458 Bleeding-family DoT ticks (23 cells) with HP at 1e-6 (an 85 % cap would move every one) |
| 16 | attack speed (S1) + OA adds (O1) | `6e0b094` → `18f1bc6` | hole 16 · 7 / 2 | **G3** swing cadence = draw cadence, 0 mismatches · **G2** PTH (OA) 0 differ |
| 17 | monster life: LO, not HI | `e2a6a7d` | hole 17 · 2 / 1 | **G3** every body's HP at 1e-6 (HI is 5–7 % higher) and the alive set exact |
| — | the chance gate: `uniform > chance` skips | `c1cb9a9` | chance-gate boundary · 2 / 1 | the gate is exercised (hole 6 row). ⚑ **The boundary `u == chance` is a probability-zero event and is exercised by nothing (§ 5 U-3)** |
| — | the C-11a grant law (R-18) | `e2525d3` (removal 131 slots, R-19) · `08e4920` (grant phase) · `ebcf4cd` (C3/C4 inert) · `607935f` (d1 + toggled aura) | v3.6 · R-18 (a) 4 / 1 · (b) 6 (boundary checks in-line) · (c) 6 / 1 · (d) 5 / 1 · (e) 4 / 1 · R-19 3 / 1 · piece 4 7 / 2 · piece 5 6 / 1 | **GR** grant rows 23–139, om-grant rows on 5 cells, toggled aura 25/25 · **G3** 58 toggled-aura hits · **G2** 461 granted-row packets. ⚑ **C1/C4 have zero population (§ 5 U-6)** |

**Holes 1–17 + 5b + the chance gate + the C-11a grant law: 20 items. Closed 20/20 · pinned 20/20 · exercised 20/20 at the mechanism level.** Three of them carry a named un-exercised sub-state (5b, the chance-gate boundary, C1/C4). Hole 2's `play_step` path is a fourth (§ 5).

---

## § 3 · The loop layer, the pack closure, the leak, and the KP-177 repairs

### 3.1 · KP-144 loop-layer items (pass 2, godot `27839ad` … `774ca16`)

| item | (a) closed by | (b) loop probes | (c) exercised by |
|---|---|---|---|
| (a) ORACLE board `engine_seed(9, w)`, salt-independent | `27839ad` | (a) board · 8 / 3 | **G3** board class exact, 98/98 waves |
| energy ledger (`/tps`) | `3b46b7b` | energy · 3 / 1 | **G3** energy at 1e-9, every tick |
| pilot: DrivePolicy + ChannelPolicyFold | `8637427` · `505c13f` | channel fold 3 / 1 · drive 2 / 1 | **G3** drive target + channel classes exact (17,668 drive rows) |
| the 1.0 s wave-advance poll | `0215496` | wave advance · 3 / 1 | **G3** wave end / wave length exact |
| deferred projectile arrival | `99f2ac3` | deferred arrival · 4 / 1 | **G3** 1,111 deferred landings, damage sources per tick exact |
| counterplay (War Cry, Turtle/Barrier/Ascension, Menhir's Will, potion, HoTs) | `782018f` | counterplay · 4 / 1 | **GR** `counterplay_absorbed` booked on 25/25 · **G3** 44 potion, 39 Menhir, 1,563 HoT heals with HP at 1e-6 |
| player summons attacking | pass 2 injection → **native at `ca5d306`** (pass 3) | v3.7 (S) · 8 / 1 | **G3** 73 casts / 5,067 swings (port), 3,075 summon hits (oracle), alive set exact |
| player raw = V0-28 EXPECTATION | `45fd97b` | raw · 3 / 1 | **G3** body HP at 1e-6 |
| tps = 12.25 exactly | `dc14111` | tps · 4 / 1 | **G3** tick grid (wave length exact) |
| (c) float64 positions (promoted from declared limit) | `73e2c81` | float64 · 3 / 1 | **G3** positions bit-exact |

### 3.2 · KP-147's halted folds, closed by v3.7 / v3.7.1 (pass 3 `42bf931` … `ec597d7`; pass 3b `d9666a2` … `933b438`)

| fold (input outside the pack at KP-147) | (a) closed by (pack · port) | (b) probe | (c) exercised by |
|---|---|---|---|
| WaveScaling count-law `*Adj` rows | engine `54968275` · `b83ea7f` | v3.7 (B) · 8 / 2 | **G3** `count_adj` 435 (25/25), board exact |
| K_MILL seek constants + speed 4.029485432492994; MovementPolicy cadence, dash layers, 4.9699 baseline | `54968275` · `6f94919` | v3.7 (K) · 14 / 3 | **G3** K_MILL true 25/25, player position bit-exact |
| `d1_alert_anim.csv` (AlertBeforePursue) | `54968275` · `8309d87` | v3.7 (A) · 9 / 1 | **G3** 1,760 evaluations / 164 fired (25/25) |
| player summons (petLimit, cooldowns, ordinals, D-8) | `54968275` · `ca5d306` | v3.7 (S) · 8 / 1 | as § 3.1 |
| control application (D-7, CC resists, EoR bonus, durations, suppression) | `54968275` · `0b18ef6` | v3.7 (C) · 14 / 1 | **G3** 64 applications / 40 insertions (19–20 cells), control term EQUAL 25/25 (Σ 52). **GR: 0 insertions on 25/25** (§ F.2n.5) |
| `pm4x_ttk_by_body.csv` (vector k) | `54968275` · `10f3a3f` | v3.7 (V) · 4 / 1 | **G3** `kvec` covered 4,893 |
| banner anchors + `SHEET_PHYSICAL_MODIFIER_PCT` | `54968275` · `55a2024` | v3.7 (N) · 6 / 1 | **G3** banner aura ticks 3,232 (23/25) |
| W1 arena avoidance | `54968275` · `5e8ace4` | v3.7 (W) · 4 / 1 | **G3** W1 and W1-NULL, 10 cells, 0 divergences |
| zero injections (the native path touches no G3 hook) | `bb86bce` | v3.7 (I) · 4 / 1 | **G3** `injected: []` 25/25 |
| ⚑ the patrol leg (V0-37 GATE_FIRST, gate closed) | **not ported**: `01a1f0a` counts it and leaves it unported | v3.7 (P) · 2 / 1 (counter + 81 m control) | ⚑ **0 gate-closed body-ticks on 25/25 G3 cells; no graded counter. Un-exercised by construction on this arena (§ 5 U-5)** |
| the five t6 pack-text fixes (V0-37 · DPE-arcane_barrier · V13-POTION-1 · V12-PATHS-1 · V9-SITE-14) | `54968275` (t6) · `42bf931` (on the wire, 5/5) | v3.7 (L) · 14 / 3 | V9-SITE-14 is graded by **`TA-X-18`** (EXACT); the barrier, potion and deferred-absorb rows by **G3** HP at 1e-6; V0-37 as the patrol row |

**KP-150 / KP-152 closure-law items (pack v3.7.1, engine `67b18f90` · `27659b01` · `22cd2288`):**

| item | port side | probe | exercised by |
|---|---|---|---|
| run state carried as input (`IC7-K-0036/37/38/0255` withdrawn) | `451c811` | v3.7.1 (R) · 6 / 1; (L) withdrawals · 18 / 2 | **G3** alert stream 0 mismatches |
| arms and walk defined only in prose → `a8` rows | `fae29ec` · `023790b` (setup split) | v3.7.1 (A) · 6 / 2 | **GR** every cell configured from `a8` (verdict `arm_config_a8`) · **G3** five arms. The `TA-X-29(e)` walk is EXACT-graded |
| read-absent columns (`r9`, `.get` defaults) | `5b73941` | v3.7.1 (D) · 4 / 1 | **G3** (the reads sit on the fight path, 0 divergences) |
| constants on untaken branches (`CONTROL_GATE_RNG_SALT`) | `b3facec` | v3.7.1 (G) · 5 / 1 | **G3** `gate_halted` 0; 64 control applications |
| the `PX-LO` driver literal | `ce21334` | v3.7.1 (X) · 3 / 1 | **G3** K_MILL bit-exact |
| `NORMAL_PTH_DIVISOR` unmapped | pack-side mapping to H1-CONST. The port already binds it from `RULE-GD-normalPTHEquation` and **refuses** on any disagreement with H1-CONST (`kc2rt_fight.gd:5200`) | no probe names it (the to-hit probe covers the ladder) | **GR** sub-threshold scaling 12–21 per w160 cell |

### 3.3 · The KP-167 leak and the KP-177 repairs

These are **visible to EXACT rows or preconditions.** They are listed because the brief names them.

| item | (a) | (b) | (c) |
|---|---|---|---|
| KP-167 `TA-X-07` leak: deferred packets booked `dropped` at wave end and after death | `fd7bef4` · `d02462a` (KP-169 Ruling 2; Path B flags) · `a05b501` (WARN-1 reclass) | v3.7.1 (K) · 4 / 1 · census (C) · 12 / 3 | **GR** after-death drops on 9/25 cells, wave-end drops on 22/25; **`TA-X-07` (EXACT) grades the closure** (H-2: (L2) operands byte-identical, worst β 3.590829e-14) |
| KP-177 `TA-X-08`: the lethal tick censused ALIVE | `0e37db9` | attempt-2 (T8) · 10 / 3 | **GR** 25/25 dying cells; `TA-X-08` (EXACT); **G3** census EQUAL 25/25 |
| KP-177 PRE_FIGHT, one per wave played | `3482aef` | (T8) control (3) | **G3** PRE_FIGHT equal 25/25 |
| KP-177 P-2: a real inserted zero-draw fold | `4b019e6` | (P2) · 15 / 4 | P-2 GREEN at the read (H-7), a precondition |
| KP-180 counters (control term, `TA-X-16` per wave) | `2e2f5a0` · `96b1f5a` · `df2bba7` | (CSC) 11 / 3 · (T16) 8 / 2 | `TA-X-08` id. 2 / `TA-X-16` (EXACT); **G3** EQUAL 25/25 |

---

## § 4 · R-1 … R-22 at `d03ca891`

| R | requirement | state at `d03ca891` |
|---|---|---|
| R-1 | expected values from oracle code | held. v1.13 § K / my H-6: the oracle passes all 28 EXACT rows |
| R-2 | fail-first; a control fails for lacking the mechanism (restated KP-133) | **125/125 controls RED** (§ 1) |
| R-3 | PCL composition exact | HOLE 1 probe GREEN · G2 105 PCL packets identical |
| R-4 | per-type counter on unmapped damage types, reading 0 | probe 8 / 1. Unmapped drops `{}` on 25/25 graded cells. U6 routes Disruption (24/25). ⚑ ManaBurnDrain / PierceRatio reached nowhere (§ 5 U-7) |
| R-5 | death order in both loops, incl. DoT / aura / granted-row kills | probes 11/1 + 5/1 + 7/3. ⚑ `play_step` and the DoT / granted-row lethal variants are probe-only (§ 5 U-1, U-2) |
| R-6 | the three invariants | **0 / 0 / 0**, recomputed independently from the 25 cells. ⚑ **WARN-1: (ii) as emitted cannot see an in-tick resurrection**; the stronger reading also gives 0 (below) |
| R-7 | the exact digest | `d03ca891…` re-derived (§ 1); boot check equal at boot and at end |
| R-8 | the probes inside the attempt MANIFEST | the 85-member runtime digest covers `tests/` and `tools/`; the evidence MANIFEST's identity pins that digest |
| R-9 | PASS quotable only beside this finding; any non-zero R-6 blocks the seal | **this finding.** R-6 is 0 |
| R-10 | stale harness fields | closed at H-4 / H-3. One report-face residue (INFO-2) |
| R-11 | term count | **superseded** by Matt's Q92 (a) → (L2) (v1.12 § F.2k); H-2 PASS |
| R-12 | `TA-X-25(c)` waits on Matt | ruled Q91 → v3.5. `TA-X-25(c)` is EXACT-graded via `spawn_by_record` (H-2 of v1.12, `ee96d08`) |
| R-13 … R-16 | holes 3 · 4 · 5 · 6 | § 2 |
| R-17 | hole 7: K4-0 exact, fail-closed; speeds; player unchanged; (b)(d) | § 2. Loader `V3P5P2 … K4-0 3.209466 @ px-LO GREEN` |
| R-18 | the grant law | § 2 (C-11a row) |
| R-19 | label ≡ swing gate | v3.6 R-19 · 3 / 1 |
| R-20 | the ten-wave walk; the 264 take identity | `TA-X-29(e)` (EXACT): 643/643 priced records bitwise (KP-174 / KP-175) |
| R-21 | digests by running the binary; 11 P-5 settings | drax's `runtime_header.equals_P4: true` and `vendored_runtime_equals_runtime_digest: true`. ⚑ Not re-run by me (INFO-6). P-5 folds printed on 25/25 cells |
| R-22 | divergence traced to its first tick | disposed KP-144. Its instrument, G3, reads 98/98 waves NO DIVERGENCE |

**The R-6 invariants, printed with their values** (§ F.5 cl. 11's companion):
- (i) cells with `killer_id` set and `terminal_reason == cleared` = **0**. All 25 cells end `death`.
- (ii) in-tick resurrections = **0**.
- (iii) cells where a PCL row landed and PercentCurrentLife intake is not > 0 = **0**. PCL landed on 25/25, and intake is 13,819–131,662 per cell.

**WARN-1 · R-6 (ii) as emitted is structurally blind to the defect it names.**
- `r6_invariants()` (`tests/kc2rt_ta_emit.gd:1781-1803`) counts a cell only if an `hp_trace` row with hp ≤ 0 is followed by a row with hp > 0.
- `hp_trace` is appended **after** the heal (`kc2rt_fight.gd:1966`, step 7, which follows `_death_check_then_heal` at step 6).
- So the pre-repair order would lift the lethal floor before the row was written. The trace would never record hp ≤ 0, and (ii) would read **0 on the broken port too**.
- **The invariant runs, and it cannot fail.** It is the same failure shape as the instrument defects recorded in CLAUDE.md.
- **The stronger reading is available from the same emission.** An in-tick resurrection is a cell with `terminal.⚑ n_lethal_floor_ticks ≥ 1` whose `terminal_reason ≠ death`, or with `n_lethal_floor_ticks > 1`, since under the oracle order the first lethal floor ends the run. On all 25 cells it reads `n_lethal_floor_ticks = 1` with `death`, so the stronger reading is also **0**.
- **The seal is not blocked.** The defect is in the instrument, not the port, and the HOLE 2 probe pins the port (`lethal_floors: 30, reason: cleared` under the control order).

---

## § 5 · Closed but UN-EXERCISED: named, per the brief

No graded row and no G3 class exercises the following states. Each is closed and probe-pinned at `d03ca891`. **A future runtime change that breaks one of them would be caught only by its probe.**

| # | state | why nothing exercises it | pinned by |
|---|---|---|---|
| **U-1** | hole 2 / R-5 on **`play_step()`** (the PLAY loop) | T-A and G3 run the ORACLE configuration through `run()`. **Matt's H-8 replay is the only run-level exerciser** | HOLE 2 both-loops probe (control: both loops resurrect 30 lethal floors) |
| **U-2** | R-5's **DoT-only-lethal** and **granted-row-lethal** deaths | all 25 G3 Leg-A lethal ticks carry a hit packet (0 DoT-only). Whether a granted row delivered any lethal hit is not determinable from the trace. The graded emission does not classify the lethal tick | R-5 probe · 7 / 3 |
| **U-3** | the chance gate **at its boundary** (`u == chance` lands) | a probability-zero event on a continuous `uniform(0,100)` draw. The gate itself is exercised (hole 6, 0 draw mismatches) | chance-gate probe · 2 / 1 |
| **U-4** | hole 5b's **discriminating state**: two or more in-reach dying slots on one death | not shown reached. G3 (160 dying hits) and G2 (43) see one dying hit per death, all matched, and G3's per-tick source multiplicity would show an extra. The graded emission has no per-death candidate counter, and I could not establish from the pack whether any Leg-A record carries two distinct dying slots | 5b probe (a synthetic two-slot record) · 2 / 1 |
| **U-5** | the **patrol leg** (V0-37 GATE_FIRST, gate closed) | **0 gate-closed body-ticks on 25/25 G3 cells**: the 43.8 m wall keeps every body within the 80 m view. **It was never ported** (`01a1f0a` counts it; the patrol inputs have no consumer). It is closed by measured unreachability, not by port. **If any arm, board or the PLAY config puts a body beyond 80 m, this is a live port gap** | v3.7 (P) · 2 / 1 (counter + an 81 m control) |
| **U-6** | C-11a **C1 (retaliation gate)** and **C4 (duration divisors)** | zero population in the pack and in the oracle (KP-131), so they are inert by construction | v3.6 piece 4 · 7 / 2 |
| **U-7** | the U6 non-health route for **ManaBurnDrain** and **PierceRatio** (R-4's founding rows, `nemesis_chthonianvoidborn_01`) | not reached in any graded cell, G3 trace or G2 packet. **Disruption** is routed on 24/25 graded cells, but **no G3/G2 instance exists**, so even Disruption's route is unverified against the oracle | R-4 probe · 8 / 1 |

**Exercised in G3 only, never in the graded emission:** control insertion. The port's generator inserts 0 on 25/25 graded cells; G3 inserts 40, with the term Σ 52 EQUAL. This is § F.2n.5 / cl. 13's sentence, and it is recorded here because a `TA-X-08` GREEN on the graded run did not test the control path.

---

## § 6 · Did any hole re-open between its closing commit and `d03ca891`?

**No.** The evidence:

1. **All 70 godot commits cited are ancestors** of `7a97716`, and `kc2_runtime/` there equals `0f36826`'s.
2. **The probe batteries kept their size.** The check and control counts at `d03ca891` equal those at the gates that closed each hole (hole 56 / 13 · v3.6 37 / 9 · completion 48 / 18 · loop 25 / 12 · v3.7 71 / 16 · v3.7.1 57 / 15). All 125 controls still go RED. A control can only go RED if the path it re-creates still exists in the runtime and the probe still reaches it, so each hole's pre-repair behaviour is still distinguishable at the graded digest.
3. **I read every post-closure edit to the hole probes:**
   - **`kc2rt_hole_probes.gd`**: R-5's DoT variant changed its *arrangement* at `27839ad` / `782018f`. Its pool is now 1e-3 HP, and its counterplay kit is emptied so that the death-order property is exercised on the DoT phase alone. The assertions did not change (INFO-4).
   - **`fae29ec`**: arms come from `a8`.
   - **`kc2rt_completion_probes.gd`**: its `_rev()` gates were widened from `v3.6.1` to `["v3.6.1", "v3.7", "v3.7.1"]`. That keeps the WIRED branches executing; if they were skipped, the count would have fallen below 48, and it did not.

   No assertion was weakened.
4. **G3 is the re-open detector for every fight-path hole, and it is clean.** All 98 Leg-A waves print NO DIVERGENCE over decisions, positions (bits), every body's HP, player HP and energy, with 0 draw mismatches on 384 streams. A re-opened hole 3/4/5/6/7/8/9/10/11/12/13/14/15/16/17, or a re-opened loop fold, would surface as a draw mismatch, a decision divergence or a number divergence on the states listed in § 1.4. **G2 705/705** covers the packet layer independently.
5. **The only `sim/` change since the last full repair gate** (`a9b756cd`, KP-175) is the four-line in-place INFO-1 counter change (`2a4201b`), which my H-3 read in full. Since `c9a7299e`, everything else is harness, tests, tools, README or MANIFEST.

---

## § 7 · The KP-178 laws as they bear on hole coverage

**Law (a)** says the oracle itself passes every EXACT row on its graded arms and window, once per prereg version.
- Discharged for v1.13 at § K (gamora) and in my H-6 (re-measured, 28/28).
- **Its bearing on holes:** the oracle's own realisations include every state the holes made reachable for the port: death, pets, dying attacks, control insertion, deferred landings and the rest. So no EXACT row is ill-posed against any of them on the 25 reference cells. My H-7 then read 28/28 GREEN off the candidate emission, and § 1 shows the graded cells are byte-identical to that emission.

**Law (b)** says that when a repair makes a state reachable, every row reading that state is re-opened against the oracle source. Here is each state the holes made reachable for the port, and where its readers were re-opened:

| state made reachable (by) | EXACT rows that read it | re-opened at |
|---|---|---|
| player death (hole 2) | `TA-X-08` (census), `TA-X-16` (picks) | **both failed at v1.12 attempt 1** (KP-177). That was the incident that founded law (b). Repaired / restated (KP-179, v1.13 § F.2m/§ F.2n); law (a) at KP-180 |
| control suppression with the fold channelling (KP-147 control fold) | `TA-X-08` identity 2 | **caught by law (a) at KP-180**; restated in v1.13 (Q96.4); G3 § C.9.5a |
| monster pets as "bodies" (hole 14) | `TA-X-10/11` (radii), `TA-X-17`, `TA-X-25`, `TA-X-30` | v1.9 § A.3 item 2 |
| per-tick DoT, pets, Resilience terms in intake (holes 10, 13, 14, R8) | `TA-X-07` | v1.9 item 5. **The KP-167 leak was this class**, found by the row itself and repaired |
| deferred landings (KP-144) | `TA-X-07` | KP-167 / KP-169 (`dropped`) |
| new draw sites (holes 6, 8, 11, the chance gate) | `TA-X-27(c)`, `TA-X-01/03–05` | v1.8 / v1.9 notes; G3 0 draw mismatches; P-2 § B.3a |
| separation pushes (hole 12) | `TA-X-10/11` | H-9 (KP-146) |
| tree_attack / dying / grant rows in pricing (holes 4, 5, C-11a) | `TA-X-29(e)` walk | KP-173 BLOCK-1 → KP-174 (643/643 bitwise) |

**No row reads a hole-reachable state without a re-open on record.** The two that were missed *before* law (b) existed are the two attempt-1 reds. They cost attempt 1, and law (b) was written because of them. **No hole closed after KP-178 made a new state reachable.** The KP-179/180 repairs were checked under law (b) at KP-180 Item 8; INFO-1 (`2a4201b`) moves no census row.

---

## § 8 · § F.5 report face (cl. 7, 11, 13) as it bears on this finding

- **cl. 11** is printed by the harness (`port_holes_printed: true`). Its text enumerates exactly the set in § 2–§ 3.2 of this finding. KP-167 and KP-177 are not in it, correctly: both are visible to EXACT rows. Its version label reads "v1.12" (INFO-2, carried from my H-3 INFO-A). **This finding is the hole-closure finding that cl. 11 names, at the same runtime digest.**
- **cl. 7** (the sustain sentence) is not a hole statement. One precision note goes to gamora's face (INFO-3): its "kills the player at waves 152–156 on salts 0–4" holds on the M-POL-2 arm of record and on W1. On M0 and M-POL-2-NULL the oracle's Leg-A deaths are [155, 151, 156, 155, 155], from the filed traces.
- **cl. 13** (the control-term sentence) is recorded in § 5 above: the term was 0 in the graded run and Σ 52, EQUAL, in G3.

---

## Verdict

**H-5 DISCHARGED at `d03ca8913901d61de73db40287e31e498e8b2714521f8221fde414682e328ccd`.**

| set | items | closed | pinned (GREEN, control RED) | exercised by GR / G3 / G2 |
|---|---|---|---|---|
| holes 1–17 + 5b + chance gate + C-11a grant law | 20 | 20 | 20 | 20 (with sub-states U-3, U-4, U-6) |
| KP-144 loop layer | 10 | 10 | 10 | 10 |
| KP-147 folds + t6 text fixes + zero injections + W1 | 11 | 11 | 11 | **10** (patrol: U-5) |
| KP-150/152 closure-law items | 6 | 6 | 5 named + 1 by bind-time refusal | 6 |
| KP-167 leak · KP-177 TA-X-08 / PRE_FIGHT / P-2 · KP-180 counters | 5 | 5 | 5 | 5 (EXACT rows / precondition) |
| R-1 … R-22 | 22 | all held, superseded (R-11) or disposed (R-22) | — | — |
| **R-6** | 3 | — | — | **0 / 0 / 0** |

- **Re-opened holes: none.**
- **Closed but un-exercised:** U-1 (`play_step`), U-2 (DoT-only and granted-row lethal), U-3 (the chance-gate boundary), U-4 (5b's multi-slot death), U-5 (the patrol leg, unported), U-6 (C1/C4, zero population), U-7 (ManaBurnDrain / PierceRatio, and no oracle-side instance of any U6 route).
- **None of them blocks the seal.** Every one is either probe-pinned against its pre-repair behaviour or unreachable on this arena and pack by measurement.

**A v1.13 `PASS` at `d03ca891`, if gamora's grade of record reaches one, is quotable beside this finding.** The remaining seal condition is H-8 (Matt's T-C replay on the same digest), and that replay is also the only run-level exerciser of U-1.

## Action

- [ ] **gandalf:** record H-5 DISCHARGED at `d03ca891`, with U-1 … U-7 carried onto the seal record and onto the JOIN-1 golden-master hand-off. U-5 (patrol) and U-7 (U6 routes) are the two that a new arena or kit could make live.
- [ ] **gamora (attempt-2 report face):**
  - print R-6 (ii) beside its stronger reading, `n_lethal_floor_ticks` vs `terminal_reason`, which gives 0 on 25/25 (WARN-1);
  - print cl. 11 with the v1.13 label (INFO-2);
  - name the arm in cl. 7 (INFO-3).
- [ ] **drax, at the next runtime change (not now; it would move the digest):**
  - redefine R-6 (ii) in `r6_invariants()` on the floor counter (WARN-1);
  - correct the stale `⚑ player_summon_hits: "NOT MODELLED …"` label (`kc2rt_fight.gd:6695`) and the `summon_inject` comment that calls the summons fold HALTED (`:510-511`) (INFO-1);
  - if a PLAY-config or new-arena run is planned, add a patrol-leg counter to the T-A emission (U-5).
- [ ] **Matt (H-8):** your replay is the only run that exercises the PLAY loop's death order (U-1). Nothing else is asked of you here.

## INFO

- **INFO-1 · Stale emission labels, report-face only.**
  - `c11a_corrections.⚑ player_summon_hits` reads *"NOT MODELLED — the player's summons do not attack in this runtime"* on every graded cell. The summons have attacked natively since `ca5d306`: the code path is `kc2rt_fight.gd:1894-1908`, and G3 matched 3,075 oracle summon hits.
  - The `summon_inject` doc comment (`:510-511`) still calls the fold HALTED.
  - Neither is a verdict input.
- **INFO-2 · cl. 11's version label.** The harness string says "v1.12". This is carried from my H-3 INFO-A.
- **INFO-3 · cl. 7's wave range is arm-specific.** It holds as "152–156" on M-POL-2 and W1; M0 and M-POL-2-NULL die at w151 on salt 1.
- **INFO-4 · R-5's DoT-variant arrangement changed after closure** (`27839ad`, `782018f`): the pool is 1e-3 HP and the counterplay kit is emptied. This is legitimate, and documented in-line. It does mean the probe no longer exercises the death check *with* counterplay in the loop. G3 does: 25/25 deaths are equal with counterplay live.
- **INFO-5 · The G2 log is scratch.** `oracle_packets3.jsonl` (sha256 `2bafa2001020adf9b907de06f5bcba2795eab2a733a897a2e5daf27350ad6aea`, 2,972 packets) is not in any repo. My G2 re-run at `d03ca891` is 705/705 on it, but its provenance is drax's KP-152 recording (KP-175 INFO-A).
- **INFO-6 · R-21 not re-run by me.** My archive has no exported `.app`. drax's emission carries `equals_P4: true` and `vendored_runtime_equals_runtime_digest: true`.
- **INFO-7 · `dot_timeline.⚑ deferred_arrival: "NOT PORTED"` is not a hole.** It is the oracle's own declared-not-folded item (`deferred_arrival.py` `DECLARED_NOT_FOLDED["DoT seeding (C-I15-1)"]`): a DoT registers at cast in the oracle too. The port follows the oracle. It is recorded so that nobody reads it as an open port gap.

## References

- **Godot (git objects / `git archive 7a97716`):**
  - `kc2_runtime/` (85 members);
  - `run_kc2_runtime_suite.sh`;
  - `tests/kc2rt_{hole,v3p6,completion,loop,v3p7,v3p7p1,attempt2}_probes.gd`, `tests/kc2rt_h4_probe.gd`, `tests/kc2rt_ta_emit.gd:1781-1803`;
  - `sim/kc2rt_fight.gd:1925-1966, 2138-2150, 4839, 5143-5205, 5248-5254, 6695`;
  - `tools/kc2rt_g3_loop_trace.gd`, `tools/kc2rt_g2_fixture.gd`;
  - `evidence/kc2-play/2026-10-01-ta-attempt2-v1.13-cells/`, `…-g3-25cell-kp184/`, `…-PRE-READ-NOT-A-GRADED-RUN-v1.13/` (`4833bcf`);
  - closing commits as cited in § 2–§ 3.
- **Engine (read-only, `22cd2288`):** `src/reincarnated/simulation/kc2/deferred_arrival.py` (`DECLARED_NOT_FOLDED`); pack `src/reincarnated/output/kc2-model-pack-v3-E-s09-cp150-mech-v3p7p1-20261001_021247/model/monster_offense.json`.
- **Collab:**
  - `agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-run-charter.md` (KP-113 … KP-188);
  - `…-ta-prereg-v1.13.md` (§ F.5, § G.1, § G.3, § H, § K);
  - `…-ta-prereg-v1.12.md` (§ F.5 cl. 7/11, § G.2);
  - `…-v1.10.md` and `…-v1.9.md` (§ G.2 tables carried).
- **My prior gates today:**
  - `2026-10-01-kc2-play-repair-gate2.md` (`6d360df78`, `c210b1979`);
  - `2026-10-01-kc2-play-attempt1-v1.12-grade-gate2.md` (`347ce2e1e`);
  - `2026-10-01-kc2-play-attempt1-repairs-gate2.md` (`ea0317306`);
  - `2026-10-01-kc2-play-prereg-v1.13-pre-read.md` (`8af096b22`);
  - `2026-10-01-kc2-play-h3-delta-gate2-d03ca891.md` (`ff6ea9fe6`);
  - `2026-10-01-kc2-play-v1.13-pre-attempt-read.md` (`9e1b19872`).
- **Scratch instruments** (session scratchpad `h5/`): `suite.txt` (sha256 `f4bb909f…`), `g3/out/*.txt` (25), `g3_all.log`, `g2.txt` (`058d4e46…`), `parse_suite.py`, `g3_agg.py`, `legA_counts.txt`.
