# Finding — 2026-10-02 — Run KC2-PLAY · H-3 (delta Gate-2 since `d03ca891`) and H-5 (hole closure + closure proof) on the REFERENT-v1 attempt candidate `fd799b63`

**Reviewer:** jack-ryan (DEV-MODE, Gate-2 with BLOCK authority; conductor gandalf)
**Severity:**
- **H-3: BLOCK.** One narrow item, **BLOCK-1**: the Cruel factor is read at the wrong point in the tick for Soulfire and bleed, which breaks the KP-246 bit-equality ruling. There are also 4 WARN and 8 INFO.
- **H-5: PASS-WITH-FINDINGS** (0 BLOCK · 2 WARN · 6 INFO). The closure proof reproduces in full on my own captures, every hole and repair item is closed at `fd799b63`, and nothing has re-opened.
- **H-5 is bound to the digest.** The BLOCK-1 fix will move the digest, so H-5 must be re-confirmed at the new one; § 7 lists exactly what to re-run.

**Target:** candidate runtime FILE **`fd799b635734904a2f477795526a20c1bbce93b683cc9b8063e865e413804813`** (107 members).
- I re-derived the digest with `make_manifest.py` over `git archive 96fc0cc`; `MANIFEST.json` is byte-equal.
- `kc2_runtime/` is identical at `96fc0cc` and `ef5c04a` (main, pushed).
- Native library `74360ffae1a434ba0de85708009c8129c6b39c4ca03898a3e4be01641e27467f` (`kc2rt_contact_native/3`).
- Delta under review: `ff6b267` (the MANIFEST commit of `d03ca891`) `..96fc0cc -- kc2_runtime`, **40 commits, 64 files, +10,546 / −676**.
- Oracle of record: engine tag `kc2/referent-v1-oracle-candidate-v311` → `969fbd8d`, `scripts/gamora_kc2_play_v3p11_oracle_2026_10_02.py` `run_one("V311-FULL")` + `v3p8.graded_arm`.
- Pack v3.11: model `99711727…`, reference `af58ef40…`, `input_closure_v3p11.json` `073d57cd…`.
- Prereg set of record: v1.14 `5bbe7ae5…`, v1.15 `d1c4a75a…`, notes `7797ff17…`; all three FILE digests re-hashed and equal.

**Developer:** drax (port) · star-lord (closure pack) · gandalf (conductor)
**Principles applied:** REVIEW_PROCESS #1, #4, #5. Disciplines #10 (attribution), #11 (empirical inspection over assumption), #12. ADR-002. Charter KP-227 → KP-272, in particular:
- KP-229: the no-hard-coded-GD rule;
- KP-233 / KP-234: the native shadow rule;
- KP-246: **bit-equality stands; a reducible residual is fixed, never absorbed**;
- KP-261 / KP-272: the candidate.

Prereg v1.14 § C.9 (C.9.1′, C.9.8, C.9.9), § G.1, § H.

**Read-only attestation.**
- I read godot only through git objects (`git show`, `git diff`, `git archive 96fc0cc` / `ef5c04a`), never drax's working tree.
- The engine was used read-only, through two `git archive 969fbd8d` copies in my scratchpad. gamora's `reincarnated-engine-join1-v311` worktree was read but nothing ran in it.
- Every Godot and oracle run held the heavy lock.
- I left a concurrent drax G3 job (`$S/g3_273_V311FULL`, engine `$S/eng311`) untouched.
- I did not open the files of the parallel jack-ryan H-2/H-7 session.
- Free disk stayed at or above 32 GiB.
- I wrote only this file and its instrument folder.

**Instruments:** `2026-10-02-kc2-attempt4-candidate-h3-h5/`
- `runs/`: G3, native, hit grid, suite, fresh per-arm shadow;
- `closure/`: the closure proof re-run and the runtime literal and key scans;
- `review/`: notes on the GD-engagement review and the hole table.

Each subfolder carries a `SHA256SUMS` or a README with the exact commands. Large captures and traces stay in scratch, with their sha256 recorded.

---

## § 1 · H-3 verdict table

| # | item | verdict |
|---|---|---|
| 1 | Is each commit faithful to the oracle of record, term for term? | **39 of 40 commits faithful, or harness / MANIFEST only.** **955859b (C2 mutators) carries BLOCK-1:** a latent term-order divergence that G3 cannot see (§ 2) |
| 2 | Is each commit fail-first evidenced? | **Section-level only for B4 / B5 / C1 / C2; no probe at all for the yetidire u5 fix** (WARN-1). For each fold, parent-RED is the "fold is bound" check. G3 is the only detector of the state-machine branches |
| 3 | Are there hard-coded GD values? | **None undeclared.** 268 pack keys and row ids named by the v3.8–v3.11 fold code all resolve in pack v3.11. 153 literal hits on changed lines, each classified as an oracle guard copied verbatim, a structural or unit constant, or a harness check (`closure/literal_scan_strict_delta.tsv`). INFO-3: prereg expected values sit inside `sim/` |
| 4 | Does bit-equality discipline hold (term for term, no FMA, `fsum` where the oracle uses it)? | Held on the reviewed folds (`review/engage-notes.md`), **except BLOCK-1**. The native build has no contraction: exactly 6 fused instructions in the whole dylib, all inside the fail-first fault branches (fault 2 ×4, fault 4 ×2), and no `__sincos_stret` |
| 5 | f37f467: B1 + B4 declared as one commit | **ACCEPTED as declared.** The swing pause's `swing_ready` lives in B4's per-body A-state, so no oracle-shaped intermediate exists between them. The probe file keeps separate B1 and B4 sections. The cost is attribution granularity, carried in WARN-1 |
| 6 | The yetidire_b01 u5 arming fix | **Faithful by reading.** The oracle's `threat._load` merges u2/u3/u4 for every pool record, and `gd_engagement.apply_default` (`:100-105`) arms any profile that has a swing period. The port keeps the HONEST-FAIL halves aside (`kc2rt_roster.gd:274-282`) and reads them only under `_hf_on()` (`kc2rt_fight.gd:7769-7781, 3985, 5703`), so pre-GD paths keep "MUST NOT BE ARMED". **No probe** (WARN-1); G3 only (4,181 divergences → 0) |
| 7 | 29e9bcb: native `pathfail_goal` and the blocker cache | **CORRECT.** Detail below |
| 8 | 751b92d: `resolve_hit` as a single callable | **FAITHFUL.** It matches `threat.resolve_hit` (`threat.py:390-411`) statement for statement: floor `max(pth, 55)`, `roll > p` misses, sub-threshold `p/70` at tier 0, the highest threshold that both `p` and the roll clear. The fight's counters stay outside the call. The summon path's old inline copy computed `maxf(pth, pth_minimum)` unconditionally, but its `pth_minimum` is always bound from `kv["pmin"]` (`kc2rt_summons.gd:295`), so its behaviour is unchanged |
| 9 | The contact-solver shadow compares 0 ticks under V311-FULL. Is the remaining shadow coverage adequate? | **ADEQUATE for the graded configuration, with INFO-1 and INFO-2.** Detail below |
| 10 | Independent re-runs | **G3 4/4 cells clean** (incl. W1 s2 and M-POL-2 s2 dying). **Native `--check` byte-identical** (`74360ffa`). **Hit-grid ROWSET `eaf31884…` reproduced on both sides**, NC-H1 RED on exactly 140. **Fresh per-arm shadow 5/5 arms, 0 mismatches.** Suite: every battery GREEN except the declared and fixture reds (WARN-4) |
| 11 | Cell-keyed branches | **None.** No behaviour branch in `sim/` keys on arm, salt, wave or tick. The two `range(151, 161)` loops are a bind-time refusal (`fight.gd:7555`) and the C.9.9 completeness guard in a tool |

### Item 7 · 29e9bcb in detail

**Kernel.**
- `pathfail_goal` (`kc2rt_contact_native.cpp:595-621`) follows the GDScript reference `_pathfail_scan_ref` (`kc2rt_gd_engage.gd:816-827`) statement for statement: skip self, the liveness test `last < tick−1`, skip ghosts, then `hypot ≤ r` on the goal and `hypot < radius + r` on the step.
- It returns the first qualifying index.
- It uses the same CPython-exact `hypot_py_impl` as the contact solver.

**What the shadow compares.** It is not native-versus-cache against a reference over the same cache:
- the reference re-reads **fresh** state on every call: `_blockers()` → `fight.ge_blockers(pets)`, and `_alive()` → the live `_last`;
- the native side reads the cache.

**So any staleness in the cache would surface as a shadow mismatch.** This is the property that makes the shadow a check on the cache, not only on the kernel.

**`pb_invalidate` placement.** It is called at the top of `_resolve_threat` (`fight.gd:3141-3143`) and of `_pet_motion` (`:4080-4081`). Those are the only two phases that scan.

The tick order is `_pursue` → `_drive` → `_pet_motion` → `_contact_solve` → … → `_resolve_channel` → `_secondary_streams` → summon hits → `_spawn_pets` → … → `_resolve_threat`. So every pet spawn (`_spawn_pets`) and every non-TTL pet death happens before an invalidation:
- killed by summon, `:2906`;
- killed by player, `:3053, 3895`.

**In-phase updates.** These are complete:
- **pet moves:** `note_pet_xy`, after the only `put_xy` in `_pet_motion` (`:4116-4119`);
- **TTL deaths:** `note_pet_dead`, which sets `PB_EXCLUDED`, so the liveness test fails exactly as an absent entry would;
- **`_last` writes:** the only two writes in the module (`gd_engage.gd:498` `note_pre_step`, `:1179` `pet_target`) each mirror into `_pb_last`.

Roster positions do not change inside either scanning phase.

**One harmless oddity.** `note_pet_xy` and `note_pet_dead` test only `_pb_tick`, not `_pb_valid`. Between an invalidation and the first scan they therefore write into a stale array, but the rebuild re-reads live state.

**Fail-first and evidence.**
- Faults 5 (reversed scan) and 6 (ghost ignored) are RED on 1,083 / 3,000 and 392 / 3,000 fixtures.
- G3 shadow: drax 954,208 scans / 0 mismatches on 25 cells; mine 160,077 scans / 0 on 4 cells.

### Item 9 · Native shadow coverage

**What is measured.**
- Under V311-FULL, `ge_fold.crowd` routes `_separate` to GD's `separate` (GDScript, `fight.gd:7347-7357`), so the native `separate_overlaps_converging` is **not reached on the graded configuration.** `shadow_ticks_compared` is 0 on all 4 of my G3 cells and all 5 of my fresh arms.
- The live native surfaces are placement and the blocker scan. Both are shadowed:
  - **G3** (mine, 4 cells): placements 1,554 / 0, blocker scans 160,077 / 0 (748 goal hits).
  - **Fresh w151–w160 per arm**, salt 0, on the port's own generator, `contact=shadow`:

    | arm | placement calls / mismatches | blocker scans / mismatches |
    |---|---|---|
    | M0 | 506 / 0 | 36,035 / 0 |
    | M-POL-2 | 360 / 0 | 35,857 / 0 |
    | M-POL-2-NULL | 506 / 0 | 36,035 / 0 |
    | W1 | 360 / 0 | 35,857 / 0 |
    | W1-NULL | 360 / 0 | 35,857 / 0 |

    The fresh runs come from `runs/scripts/jr_shadow_fresh.gd`, a scratch copy of the timing tool's `_fight` that prints the full `contact_solver_report()`. drax's timing tool aggregates only the contact and placement fields, and its KP-261 runs were `native`, not `shadow`.
- **So v1.14 § C.9.8's second clause, "a fresh w151–w160 run per arm", is now evidenced for the `74360ffa` build on the two live surfaces.**

**Judgment.** For the graded configuration this is adequate:
- the contact kernel is dead code there;
- the two live kernels are compared on every call, on 25 + 4 G3 cells and 5 fresh arms;
- the reference side reads live state.

The residual exposure is any configuration that re-enables the converging solver. Only V38-* levels do that, and the legacy probes and the contact-native probe battery (31 / 11) cover it.

**One instrument note.** H-4's `g3_block` `shadow_ok` (`kc2rt_h4.gd:590-594`) passes on `shadow_mismatch_ticks == 0`, which **holds vacuously with 0 ticks compared** (INFO-1).

---

## § 2 · ⛔ BLOCK-1 · Cruel's factor is re-read after the disc for Soulfire and bleed; the oracle snapshots it once per tick, before the disc

**What is (description).**

*Oracle* (`run.py:2945-2953` at `969fbd8d`). Once per tick, before the player's disc resolves:
```
_mut_f = mutator_fold.player_factor(k)
player_offense.mutator_factor = _mut_f   (or tick_damage *= _mut_f)
secondary_streams.mutator_factor = _mut_f
```
Soulfire and bleed then multiply by that snapshot:
- `secondary_streams.py:277`: `(raw·proj·max(0,1−res/100)·crit) * self.mutator_factor`
- `:293`: `bleed_dps·max(0,1−res/100) * self.mutator_factor`

Cruel's window opens in `ThreatEngine.resolve_attack` → `mutators.note_monster_hit(tick)` (`threat.py:1924-1926`). **That includes a dying attack fired inside the disc** (`run.py:3176-3188`, `engine.resolve_attack(... slot=s ...)`).

*Port* (`kc2rt_fight.gd` at `96fc0cc`).
- The disc snapshot is taken correctly, once, in `_banner_factor_now()` (`:5482`), called from `_resolve_channel` (`:3010`).
- A dying attack inside the disc (`:3055` `_fire_dying` → `_apply_slot` → `:5729-5730` `note_monster_hit`) can open the window mid-tick.
- **`_secondary_streams` then re-reads `mut_fold.player_factor(...)` fresh:** for Soulfire at `:3827`, for bleed at `:3847`.

**The consequence.** On a tick where Cruel is OFF at the start, a dying attack hits the player, and Soulfire or a bleed reaches a surviving body, the port applies ×0.92 where the oracle applies ×1.0.
- The association of the products is otherwise identical.
- Bleed REFRESHES every disc-hit body each tick, so the second condition reduces to "any surviving disc body on that tick".

**Why G3 is clean anyway.** The engage review checked the 25 committed G3 oracle traces:
- 378 dying hits on the player;
- 113 with Cruel already on at the start of the tick;
- 8 with Cruel off at the start;
- 257 that cannot be classified, because those ticks carry no banner value;
- **none of the 8 had Soulfire or a bleed on a surviving body that tick.**

An occurrence moves a body's HP by at least 1.9e-6 relative (bleed) or 2.4e-4 (Soulfire). Both are above G3's 1e-6 number tolerance, so 25/25 clean means **the state was never reached on the oracle's draws, not that the port is right.** The graded attempt runs on the port's own generator, which can reach it.

**Rationale (citations).**
- **KP-246 (conductor ruling, recorded against my WARN-3):** "port V311 term for term … a residual that survives this with a named, irreducible mechanism goes to MATT; it is never absorbed". This residual is named and *reducible*.
- REVIEW_PROCESS #4 (the committed record is the truth: the seal claims port ≡ oracle).
- Discipline #11.
- It is the same instrument-blindness shape as KP-233's FMA build: a real divergence the graded-equality instrument cannot see on its 25 cells.
- An attempt spends one of two budget slots (v1.14 § G.1). Spending it on a digest with a known, reducible divergence is the wrong kind of progress.

**Path forward (drax; small).**
1. Store the per-tick factor once, at the oracle's site. `_banner_factor_now()` already computes it at `:5482`. Use that stored value at `:3827` and `:3847`, and anywhere else the per-tick mutator factor is consumed after the disc.
2. Add a fail-first probe with:
   - a fixture tick: Cruel off at start, a dying hit in the disc, a surviving bleed / Soulfire body;
   - expected ×1.0, read off the oracle;
   - a must-RED control that does the fresh read.
3. Regenerate the MANIFEST. Re-run G3 V311-FULL 25/25 in shadow and the fresh per-arm shadow (`runs/scripts/jr_shadow_fresh.gd` is available).
4. The digest is moving anyway, so **fold in WARN-1 (probes), WARN-3 (the carried d03ca891 actions) and WARN-4 (the T8 fixture) now.**

**Re-gate.** My delta Gate-2 on the fix commit(s) only. H-2 and H-7 re-run at the new digest (the parallel session). H-5 re-confirmed per § 7.

**If the conductor contests the BLOCK** (for example, to accept it as a declared residual), this is a Matt decision under KP-246's valve, not a gate call.

---

## § 3 · H-3 WARN

- **WARN-1 · Fail-first stops at section level. The GD state machine and the u5 fix are pinned by G3 alone** (Discipline #11; R-2 "a control fails for lacking the mechanism").
  - **What is.** f37f467's "parent RED, 2 failures" is the two "fold is bound" checks (B1-1, B4-1), each of which returns early.
  - B5, C1 and C2 likewise fail one bound check on their parent; C1's control (C1-6) is nominal.
  - **No probe or control exercises these B4 branches:** persist / D8 whiff, WaitToAttack, pursue path-failure → reposition, the reposition exits and trigger, LostSlot / slot-stealing, pets taking slots, pet attack suppression.
  - **The yetidire_b01 HONEST-FAIL arming has no probe.**
  - The roster half of holes 4 and 6 and the chance gate now runs through GD's `_choose` (`kc2rt_gd_engage.gd:364-392, 447-467`), also pinned by G3 only.
  - G3 summaries carry no `ge_fold` telemetry, so G3 cannot show which branches its 25 cells reached.
  - **Fix (drax, with BLOCK-1):**
    - fixture probes with must-RED controls for each named branch;
    - a u5 probe: armed under GD with its own u2/u3/u4 rows, unarmed at V38-FULL;
    - emit `ge_fold.report()` in the G3 summary.

- **WARN-2 · The `.app` and the PLAY vendor copy are stale. As built, the attempt harness files emission failures and exits 1.**
  - `kc2rt_ta.gd:216-232` appends a failure whenever any of these is not true:
    - `runtime_header.read_by_running`;
    - `equals_P4`;
    - `vendored_runtime_equals_runtime_digest`.
  - `:282` then quits with code 1.
  - `kc2_play/vendor/kc2_runtime/` on disk is tree `af2d8bbf…`, still pinned to pack v3.8 `6326d02d…`. It is gitignored and rebuilt by `vendor.py`.
  - drax declared the rebuild PLAY-phase (7eda88d). At this candidate it is a **launch precondition**.
  - **Fix (drax; conductor's launch sheet):** re-vendor at the attempt digest with pack v3.11, rebuild the `.app`, and confirm the two self-checks read `true` before attempt 1 of 2.

- **WARN-3 · Two actions I carried at `d03ca891` "for the next runtime change" were not done. This candidate is that change.**
  - (a) R-6 (ii) in `r6_invariants()` (`kc2rt_ta_emit.gd:2037-2043`) is still structurally blind to an in-tick resurrection (my d03ca891 H-5 WARN-1). It matters more now that 20 of 25 cells clear.
  - (b) The stale labels remain: `player_summon_hits: "NOT MODELLED …"` (`kc2rt_fight.gd:7112`) and the `summon_inject` "HALTED" comment (`:513`).
  - **Fix (drax, with BLOCK-1):** redefine (ii) on `n_lethal_floor_ticks` against `terminal_reason`, and correct both labels.
  - If the fix lands without these, gamora prints the stronger R-6 reading on the attempt face.

- **WARN-4 · The attempt-2 battery is RED at this digest: 5 failures, 3 of them a fixture with no dying population.**
  - T8 (`kc2rt_attempt2_probes.gd:124-175`) needs M-POL-2 s0 w151–153 to die. Under V311-FULL it **clears**: terminal_wave 153, `cleared`, `n_lethal_floor_ticks` 0.
  - The file is unchanged since `d03ca891`, and 7eda88d did not move it to V38-RS. So the TA-X-08 lethal-tick and identity checks have no population here.
  - The other 2 failures are `runtime_header` (WARN-2).
  - ⚑ **For the H-7 session, not graded here.** On that clearing fixture cell the *legacy* `⚑ TA-X-08_identity_2.holds` (`fight.gd:6482-6487`) reads **false**: n_channelling 1,755 + n_released 76 = 1,831 against D = 1,835, a deficit of 4. I did not evaluate v1.13's restated identity, which reads the `ta_x_08_counters` block, on graded cells.
  - G3 still pins the dying-cell census: `census_equal` holds on my W1 s2, M-POL-2 s2 and M0 s3.
  - **Fix (drax):** re-point T8 at a cell that dies under V311-FULL (for example W1 s2 or M0 s3), or run it at V38-RS. **Conductor:** route the deficit-4 reading to the H-7 session.

## § 4 · H-3 INFO

- **INFO-1 · `shadow_ok` passes with zero comparisons.** `kc2rt_h4.gd:590-594` accepts `shadow_mismatch_ticks == 0` with 0 ticks compared. Require at least one placement call and at least one blocker-scan call compared, and print "contact solver: not reached at this level" rather than "0 mismatches". (drax)
- **INFO-2 · No shipped path selects the native library.**
  - `kc2rt_ta.gd` never calls `select_contact_solver`, so **the graded attempt runs the GDScript reference everywhere.** § C.9.8 is conditional ("if the attempt runtime executes any native library"), so for the graded run it reduces to the G3 shadow evidence, which is present.
  - No file outside `kc2_runtime/` selects it either (`git grep` at `ef5c04a`), so **the KP-261 stutter fix is active only in tools today.**
  - The H-8 / P1(e) PLAY build must call `select_contact_solver("native")`, and on that platform must pass its own shadow run.
  - **Owner:** drax at P1(e). The conductor should note it against KP-261's "STUTTER FIXED".
- **INFO-3 · Prereg expected values sit in `sim/`.**
  - `Kc2RtComposition.f2h_b_holds` (`kc2rt_composition.gd:268-278`, b46c0b2) hard-codes `−0.44`, `160`, `"LO"` and `divisor == true`. These are v1.15's report-face GREEN rule.
  - The fight itself takes `f_unmapped` and `LAPM_WAVE` from pack rows, so this is not a GD value in behaviour.
  - Move it to `tests/`. (drax)
- **INFO-4 · G3 stream relabelling (KP-227).** When a construction line moves, G3 resolves a stream label by file + seed, only when the match is unique. The used line is recorded and printed (`relabelled_streams`). Acceptable as implemented.
- **INFO-5 · Oracle traces are not byte-reproducible across checkouts.**
  - `composition.engine_src` embeds the scratch path.
  - My 4 traces equal drax's filed ones only with that field blanked.
  - My summaries differ from his only in `trace_sha256`.
  - Relativise or blank the field. (drax)
- **INFO-6 · The suite's 300 s per-leg deadline kills the hole-probe leg under load.**
  - Run alone (2,400 s alarm), the leg is GREEN 56 / 0, 13 / 13 RED, in 333 s.
  - Raise the deadline or split the leg. (drax)
- **INFO-7 · Latent equivalences in the C1 / C2 ports. They agree on the pinned data and are not defects today** (engage review F-5 to F-8):
  - **mutator level lookup:** the port takes the first non-blank row, the oracle the last row with blank read as 0. They agree on 169 + 338 rows with no duplicates or blanks.
  - **the +50 % retaliation test:** the port checks the `template_group` prefix, the oracle `retaliation_keys()`, a set measured empty.
  - **line-up capacity:** the port keys by pool with default 0, the oracle by (wave, point, pool) with uncovered meaning unbounded.
  - **Leeching:** only on packet landings, so it is off if the loop layer is off.
  - Harden these if the pack grows. (drax)
- **INFO-8 · The parent-RED claims of the six-commit run `4aba33b…955859b` are unverified.** Those commits were authored within 86 s, so the claims were probably measured on working trees. I did not re-run the v3.11 sections at each committed parent. Not blocking: G3 at the tree is the graded evidence.

---

## § 5 · H-5 · the closure proof, re-run (star-lord's own instrument at `969fbd8d`, my own captures)

**Method.**
- `git archive 969fbd8d` into scratch. I relocated three hard-coded checkout constants and added a collab alias; the full diff is in `closure/relocation.diff`.
- I added a one-file git shim so the `MIGRATION.md` lookup resolves; its blob `9480be01` equals `969fbd8d`'s.
- I ran star-lord's own `run_captures` with `KC2_CLOSURE_ORACLE=v3p11-record`: 14 captures (7 jobs × hs0 / hs1), 6 bare runs and 2 static sweeps. All 22 exited 0 in 3,688 s.
- I then ran star-lord's own gates V-152 to V-157 **against the written pack bytes**, plus my independent checks.

| criterion | result |
|---|---|
| pack digests (recomputed from member bytes, without importing the engine) | model `997117278c1e28da…d788` 21/21, reference `af58ef4009029c99…ac1c` 7/7, 0 mismatches; cross-pin names the model. New members `input_closure_v3p11.json` `073d57cd…` and `oracle_inputs_v3p11.json` `8c56d2a0…` equal. The main-checkout copies the runtime pins are the same bytes |
| **strict 0 NOT IN PACK** | **0 on 14/14 captures** (after the declared normalisation below) |
| **static sweep** | **0 violations** on both seeds; `n_modules` **75**, 1,169 defined / 1,048 referenced bindings, all covered (k3 629, k12 413, e13 6). Byte-equal to star-lord's POST sweep |
| **mutation gate** | **E6 ×12** (`locomotion._FALLBACK_HITS`) and **E7 ×36** (`alert._INCIDENCE` / `_ROWS` / `_TABLE`) only, the instrument's own per-binding, per-job verdicts. Classes defined at `kc2_v3p7p1_law.py:33-56`. Exempt census over 14 captures: E1 4,276 · E2 868 constants + 2,516 files · E3 172 files · E5 1,862 defaults · E6 12 · E7 36 · E4 absent |
| inertness · seeds · predecessors · K-7 | instrumented == bare on all jobs; hs0 ≡ hs1 on 7/7; v3.8 predecessors untouched; **K-7 3/3 pre and post**; ROWSET `v3p11_all` re-derives to `8dad7a2d…`; census closure 1,035 / hand 168 |
| **KP-213 every-image corrigendum** | **Implemented at `kc2_v3p11_closure.py:104-144`.** It checks every image of a path and counts the path IN PACK only if some image carries every consumed column with equal cells. It replaces the first-image function (`kc2_v3p7p1_law.py:240`) via `law()` (`:167-177`). Two paths have two images each: `pm2_tg2_monster_timing.csv` (IC7-F-22 with 3 cols, IC7-F-V311-04 with 104) and `pm4i_wave_damage_modifier.csv` (IC7-F-37 with 24, IC7-F-V311-05 with 34). **My negative control** (`closure/kp213_negative_control.py`, M-POL-2 hs0) is in the table below |
| vs star-lord's committed POST tables | 0 value differences on every capture. One extra row on mine: the editable-install `.pth` reading `…/reincarnated-engine/src`, classed E2 and read-only |

The KP-213 negative control:

| case | violations | result for the two double-image paths |
|---|---|---|
| A: every-image rule, untampered | 35 (pre-normalisation baseline) | both IN PACK by their second image |
| B: old first-image rule | 42 | both NOT IN PACK: the KP-213 defect reproduced |
| C: `controller_class` dropped from the second image | 36 | `pm2_tg2` goes NOT IN PACK |
| D: one `pm4i` cell altered in the second image | 36 | goes NOT IN PACK, "cell differs at CSV line 5" |

**Declared normalisation, and why it is not a loosening.**
- **Raw counts before normalisation** were 6–7 NOT IN PACK per capture, 35–41 on four first-compile captures (`closure/verify_off_written_summary.json` `RAW_…`).
- **About seven strict pack rows carry host-path values:**
  - IC7-K-V311-0075 `ENGINE_SRC`;
  - IC7-K-V311-0067 `W1_GLOB`;
  - the `from_x8` composition call.
- So any checkout other than star-lord's own reads them as NOT IN PACK.
- **The audit hook** (`kc2_v3p7_closure.py:76`) misses `*.pyc.<id>` temp files on a cold bytecode cache.
- **What I changed:** I rewrote only the checkout root in constant and composition values, and dropped only those temp-file opens. Both are scripted and counted per capture.
- **No consumed value or column was altered.**

**Runtime side at `fd799b63`.**
- **Pin:** `kc2rt_pack_of_record.gd:43-46` pins model `99711727…` and reference `af58ef40…`.
- **Refusals:**
  - the digest gate (`kc2rt_pack.gd:199-225`);
  - the revision gate, accepting only `v3.11` (`loader/kc2rt_v3p11.gd:35, 646`);
  - the census guards, 1,035 / 168;
  - the reference cross-pin (`kc2rt_pack.gd:1138-1165`);
  - the native library pin and refusal (`kc2rt_contact_bridge.gd:24, 61-63`).
- The suite confirms the pin at run time: `PACK PASS | DIGEST PASS | pack 997117278c1e (MATCH)`.

## § 6 · H-5 · the hole and repair table at `fd799b63`

**Probes.** Every battery that pinned a hole at `d03ca891` keeps its size, and every control still goes RED:

| battery | checks / failures | controls RED | at `d03ca891` |
|---|---|---|---|
| hole | 56 / 0 | 13 / 13 | same |
| v3.6 | 37 / 0 | 9 / 9 | same |
| completion | 48 / 0 | 18 / 18 | same |
| loop | 25 / 0 | 12 / 12 | same |
| v3.7 | 71 / 0 | 16 / 16 | same |
| v3.7.1 | 57 / 0 | 15 / 15 | same |
| H-4 | 34 / 0 | 30 / 30 | was 35 / 26 (re-pointed to v1.14 / v1.15, b46c0b2) |
| v3.8 (new) | 31 / 0 | 15 / 15 | — |
| v3.11 (new) | 61 / 0 | 16 / 16 | — |
| contact-native (new) | 31 / 0 | 11 / 11 | — |
| emission (new) | 30 / 0 | 9 / 9 | — |

**236 / 236 controls RED** across these. Loader 135 / 0, rules 58 / 0, purity 0 violations, and all 32 `--check-only` legs are GREEN.

**Probe edits.** No assertion was weakened or removed in the six legacy files (`review/holes-notes.md`):
- the hole-5 dying-reach count went from 14 to 26, re-derived from the oracle; the old value is kept as `_SUPERSEDED`;
- the revision lists were extended.

**Live versus superseded under V311-FULL.** 7eda88d now runs the legacy batteries at oracle level **V38-RS** (an empty a8 chain). The table below says, per item, whether the graded configuration still runs that code:

| class | items | what pins the graded behaviour |
|---|---|---|
| **LIVE** (the same code is reached at V311-FULL) | holes 1, 2, 3, 5, 5b, 7, 8 (now `resolve_hit`), 9, 10, 11, 12a, 13, 15, 16 (GD swing timing still applies the attack-speed multiplier, `fight.gd:3349`), 17; the C-11a grant law; energy, wave poll, deferred landings, counterplay, tps, float64; the remaining KP-147 folds; KP-150/152 except PX-LO; KP-167 / 177 / 180 | the legacy probes (code shared) + G3. Fold counters are non-zero on 25/25 G3 cells: `count_adj` 79–80 per cell, alert 71–76 evaluations, control insertions sum 20, banner ticks 25/25 |
| **PARTIAL** | holes 4 and 6 and the chance gate (the roster goes through GD `_choose`; pets through the legacy path); hole 14 (pets driven by GD `pet_target` / slots / RFA, `fight.gd:4102`); KP-144 board (line-up fold picks keys, `kc2rt_board.gd:641`); pilot (drive superseded, channel fold live); player raw (mutator factor, `fight.gd:5479`) | legacy probes for the non-GD half; **G3 alone for the GD half** (WARN-1, H-5 WARN-A) |
| **SUPERSEDED** | hole 12b (GD crowd `separate`, `fight.gd:7350`); K_MILL + MovementPolicy (P-MOVE returns first, `:2491-2493`); PX-LO with them | v3.11 B4-6 (crowd separate bit-equal to CPython) with control B4-7; v3.11 B5; G3 bit-exact positions and `drive_target` (C.9.1′) |

**R-6 invariants.** These are the attempt emission's, not computed here. WARN-1 from `d03ca891` carries as H-3 WARN-3(a).

**Re-opened holes: none.**
- G3 is clean on my 4 cells and drax's 25: 0 decision divergences, 0 draw mismatches, bit-exact positions.
- Every control is RED.
- No legacy assertion was weakened.

### H-5 WARN

- **WARN-A · The GD half of holes 4, 6 and 14 and the chance gate has moved off probe pinning onto G3 alone.**
  - This is the same remedy as H-3 WARN-1, recorded here because it is a hole-coverage regression relative to `d03ca891`: then, every hole had a probe at the graded configuration.
  - The chance-gate boundary (U-3) now exists in two implementations, and the GD one has no probe.
  - Owner: drax, with BLOCK-1.
- **WARN-B · The new GD sub-states are closed but un-exercised.**
  - The sub-states: WaitToAttack, RFA, path-failure stuck/goal, roam, the D8 whiff and `pet_target`.
  - No probe exercises them, and no G3 telemetry shows any of them reached.
  - Add them to the U-list on the seal record beside U-1 … U-7.
  - Owner: conductor (record) and drax (telemetry).

### H-5 INFO

- **INFO-A · U-list at V311-FULL.**
  - **U-1 (`play_step`):** no suite probe runs it at V311-FULL; Matt's H-8 replay remains its only exerciser.
  - **U-2:** G3 now has 5 dying cells, not 25.
  - **U-3:** see WARN-A.
  - **U-4, U-6, U-7:** unchanged.
  - **U-5 (patrol):** still 0 gate-closed body-ticks on 25/25. Its rationale changed: M0 and M-POL-2 have no wall in the oracle (KP-252), and under reposition the 80 m test is taken against the step's waypoint. The `_pursue_one` comment ("the 43.8 m wall keeps every body inside") is stale.
- **INFO-B · The closure instrument runs only from star-lord's checkout path.** Owner: star-lord.
  - Hard-coded paths: `kc2_v3p7_inputs.py:31-32`, `kc2_v3p7_closure.py:54, 2125`, `kc2_v3p11_rows.py:43-44`, `spawn_structure.py:61`.
  - The host-path pack rows (IC7-K-V311-0075, -0067, `from_x8`) belong in **E1**, as E1's own definition says.
- **INFO-C · The audit hook's `.pyc` filter misses `*.pyc.<id>` temp files** (`kc2_v3p7_closure.py:76`). Invisible on warm caches. Owner: star-lord.
- **INFO-D · Absent-column keys embed the checkout** (`R|:/Users/...`). Run through a relocated instrument, star-lord's own captures read 12 such NOT IN PACK. Owner: star-lord.
- **INFO-E · Inline oracle literals sit outside the closure law.**
  - 44 inline numeric literals in the v3.8–v3.11 fold modules (`closure/oracle_inline_literals.tsv`). Several reach decisions:
    - `gd_reposition.py:205, 238, 248, 360, 454, 661, 774, 789, 817, 822, 829`;
    - `gd_engagement.py:130, 158, 162, 212`;
    - `swing_pause.py:91`.
  - il1 carries only the two p05 guards.
  - The port mirrors them verbatim, and G3 checks parity. This is consistent with KP-259's disclosure, and none is an undeclared GD value in the port.
  - Extend il1 or name the constants at the next cut. Owner: star-lord / gamora.
- **INFO-F · `test_kc2_pack_v3p11_cut.py` has no control for the every-image rule.** Adopt `closure/kp213_negative_control.py`'s cases B to D. Owner: star-lord.

## § 7 · What the BLOCK-1 fix forces at H-5

**Closure, oracle side: unaffected.** The oracle and pack do not move, so § 5's captures stand.

**At the new digest, re-confirm:**
1. the runtime-side pin, key and literal scan on the delta only (`closure/literal_scan_strict.py`, `runtime_key_check.py`, `delta_filter.py` against the new commits);
2. the full suite, with all controls RED, the new probes counted, and T8 re-pointed;
3. G3 25/25 + shadow, plus the fresh per-arm shadow.

I will do 1 and 2 in the delta Gate-2. drax files 3, and I re-run a sample.

---

## Verdict

**H-3: BLOCK** at `fd799b63`, on BLOCK-1 alone.
- Every other runtime change since `d03ca891` is faithful, or harness-only.
- The native `--check`, G3 sample, hit-grid and fresh shadow re-runs all agree with drax's evidence.
- **29e9bcb and 751b92d are correct.**
- The contact-shadow vacuity is real but harmless on the graded configuration.

**H-5: PASS-WITH-FINDINGS** at `fd799b63`.
- The closure proof reproduces: 0 NOT IN PACK on 14/14, static 0 over 75 modules, mutation gate E6/E7 only, the KP-213 every-image rule shown live by a negative control.
- Every hole and repair item is closed and not re-opened.
- **The finding is bound to the digest. It must be re-confirmed per § 7 at the post-fix digest before it can stand beside a graded PASS.**

## Action

- [ ] **drax:**
  - BLOCK-1 fix + probe → MANIFEST → G3 25/25 shadow → fresh per-arm shadow;
  - in the same pass: WARN-1 (B4 branch probes, the u5 probe, `ge_fold.report()` in G3), WARN-3 (R-6 (ii), the two labels), WARN-4 (re-point T8);
  - INFO-1, 3, 5 and 6 if cheap;
  - before launch: WARN-2 (re-vendor + rebuild the `.app` at the new digest, both self-checks `true`).
- [ ] **gandalf (conductor):**
  - record H-3 BLOCK and H-5 PASS-WITH-FINDINGS against `fd799b63`;
  - hold the attempt until the post-fix delta Gate-2 clears;
  - route the WARN-4 deficit-4 reading to the H-7 session;
  - note INFO-2 against KP-261's "STUTTER FIXED" (no shipped path selects native yet);
  - carry WARN-B and INFO-A (U-list) onto the seal record.
- [ ] **star-lord (non-blocking, next cut):** INFO-B to INFO-F.
- [ ] **Matt:** only if the conductor contests BLOCK-1 as a declared residual (the KP-246 valve).

## References

- **Godot (git objects / `git archive 96fc0cc`, `ef5c04a`):**
  - `kc2_runtime/sim/kc2rt_fight.gd:2491-2493, 3010, 3055, 3141-3143, 3349, 3827, 3847, 4080-4119, 5459-5490, 5694-5730, 7112, 7297-7385, 7555, 7731-7781, 7816-7843`;
  - `sim/kc2rt_gd_engage.gd:1-211, 364-467, 496-500, 571-573, 760-892, 1177-1181`;
  - `sim/kc2rt_laws.gd:35-60`;
  - `sim/kc2rt_summons.gd:280-300, 420-440`;
  - `sim/kc2rt_mutators.gd:212-229`;
  - `sim/kc2rt_composition.gd:268-278`;
  - `sim/kc2rt_roster.gd:268-300, 1045-1105`;
  - `native/src/kc2rt_contact_native.{cpp,h}`;
  - `sim/kc2rt_contact_bridge.gd`;
  - `tests/kc2rt_h4.gd:580-605`;
  - `tests/kc2rt_ta.gd:205-235, 275-285`;
  - `tests/kc2rt_ta_emit.gd:2037-2043`;
  - `tests/kc2rt_attempt2_probes.gd:124-175`;
  - `tools/kc2rt_g3_{oracle_trace.py,loop_trace.gd,run25.sh}`, `tools/kc2rt_hitgrid.gd`, `tools/kc2rt_tick_timing.gd`;
  - evidence `evidence/kc2-play/2026-10-02-{g3-25cell-kp261-V311FULL-96fc0cc,tick-timing-kp261-petpath,…}`.
- **Engine (`969fbd8d`, read-only):**
  - `src/reincarnated/simulation/kc2/{run.py:2945-2953, 3172-3215, threat.py:338-411, 1905-1930, secondary_streams.py:243-293, mutators.py, gd_engagement.py:60-140, pilot_move.py:132-172}`;
  - `src/reincarnated/export/{kc2_v3p11_closure.py, kc2_v3p7_closure.py, kc2_v3p7p1_law.py}`;
  - pack `src/reincarnated/output/kc2-{model,reference}-pack-v3-E-s09-cp150-mech-v3p11-20261002_192143/`;
  - star-lord POST captures `kc2-v3p11-POST-*-20261002_192143.json`.
- **Collab:**
  - the charter ledger (KP-213, KP-227 … KP-272);
  - prereg v1.14 (§ C.9, § G, § H), v1.15, notes;
  - my prior `2026-10-01-kc2-play-h3-delta-gate2-d03ca891.md` and `2026-10-01-kc2-play-h5-hole-closure-d03ca891.md`.
- **Instruments:** `2026-10-02-kc2-attempt4-candidate-h3-h5/{runs,closure,review}/` (each with `SHA256SUMS` or README).

---
---

# ⚑ DELTA · 2026-10-03 · the KP-274 repair candidate `3e2359a6` (conductor dispatch KP-275)

**Severity:**
- **H-3 delta: PASS** (0 BLOCK · 0 WARN · 4 INFO). **BLOCK-1 is discharged.**
- **H-5 re-confirm at `3e2359a6`: PASS-WITH-FINDINGS stands.** WARN-A is discharged. WARN-B is reduced to INFO.
- **Corrigendum to § 6 above:** the control total I printed as "236 / 236" was an addition error. The correct sum of the listed batteries at `fd799b63` was **164**, or **180** with attempt-2's 16. No battery figure was wrong, only the total.

**Target:** runtime FILE **`3e2359a6d46c78029f7994a0f600434894dc8916d580b81732c20278257d3057`** (107 members).
- I re-derived it with `make_manifest.py` over `git archive 66605a1`; `MANIFEST.json` is byte-equal.
- `kc2_runtime/` is identical at `66605a1` and `c64c192` (main).
- Native library unchanged: `74360ffa…`, re-hashed in the archive and in the rebuilt `.app`'s `Frameworks/`.
- Delta `96fc0cc..66605a1 -- kc2_runtime`: **d7b4846**, **b87e233** (MANIFEST), **b1d2c9e**, **66605a1** (MANIFEST). 16 files, +716 / −134.
- Evidence: godot `evidence/kc2-play/2026-10-03-g3-25cell-kp274-V311FULL-66605a1/` (summaries + logs). It reuses the committed KP-261 oracle traces: the filed W1 s2 summary's `trace_sha256` `94496de0…` equals the gunzipped `…-kp261-…/oracle_traces/W1_s2.json.gz`.

**Instruments:** `2026-10-02-kc2-attempt4-candidate-h3-h5/delta-3e2359a6/` (with `SHA256SUMS`).

## D.1 · H-3 delta, per commit

| commit | what | verdict |
|---|---|---|
| **d7b4846** | H-7 BLOCK-1 + WARN-3: TA-X-25 (b)/(c) spawn class from `Kc2RtFight.v3p11_can_swing`; `ta_x_29_b_c_d["(b)"]` = the CompositionFold block | **FAITHFUL, labels only.** `_make_body` (`kc2rt_board.gd:909-918`) changes only `sbr_class` and the two counters. Disposition, draws and positions are untouched; G3 summaries are byte-equal to filed except `trace_sha256`. One predicate, `v3p11_can_swing` = `_swing_period_of(rec) > 0 and live_slots(rec)` non-empty, now feeds both the wave-open re-arm (`fight.gd:7730, 7734`, previously two inline copies of the same expression) and the board label. The gate is bound only when a v3.11 slot fold re-arms (`v3p11_gate_on`) and is cleared at every re-bind (`:7546`). Probe (K) K1–K3, K5 and must-RED control K4 (gate unbound → 10 records differ) re-ran GREEN. The TA-X-25 grading itself is the H-7 session's |
| **b1d2c9e** | BLOCK-1 + WARN-1/3/4 + INFO-1/2/3/5/6 | **BLOCK-1 FIXED, FAITHFUL.** Detail below |
| **5b525ec** | `kc2_play/tools/kc2p_probe.gd` expectations | **OUTSIDE THE DIGEST, verified.** It touches one file, `kc2_play/tools/kc2p_probe.gd`. No `kc2_play/` path is among the 107 MANIFEST members (all are `kc2_runtime/`-relative), so it cannot move `3e2359a6`. INFO-D3 |
| b87e233 · 66605a1 | MANIFEST regenerations | digests re-derived (`a38e2913…` intermediate, `3e2359a6…` final) |

### The BLOCK-1 fix, checked against the oracle

**Oracle** (`run.py:2945-2953`): `_mut_f = mutator_fold.player_factor(k)` once per tick, before the disc. It is handed to `player_offense.mutator_factor` and `secondary_streams.mutator_factor`, and Soulfire and bleed multiply by `self.mutator_factor` (`secondary_streams.py:277, 293`).

**Port at `66605a1`:**
- `_mut_snapshot()` (`fight.gd:7518-7519`) sets `mut_tick_factor = mut_fold.player_factor(run_tick − _wave_start_tick)` (or 1.0).
- It is called once per tick in `_tick` (`:1965`), **before `_disc_hit_list()` and the disc**. It comes after `_pursue` / `_drive` / `_pet_motion` / `_contact_solve`, none of which resolves a monster hit.
- Soulfire (`:3834`), bleed (`:3854`) and the disc's banner factor (`_banner_factor_now`, `:5489`) all read `mut_tick_factor`.
- **No other `player_factor` read remains in `sim/`** (grep).
- The association is unchanged: `(…·(1−res/100)·crit) * f` and `(dps·(1−res/100)) * f`, as in the oracle.

**Probe (M).**
- Fixture: Cruel off at the tick's start → snapshot 1.0; then `note_monster_hit` (the dying hit in the disc) → fresh read 0.92; then `_secondary_streams([b])` on a surviving body.
- M1 asserts snapshot 1.0 and fresh 0.92. M2 asserts the bleed `dps == base × snapshot`. Control M3 (`dps == base × fresh`) must go RED.
- **I ran a mutant in scratch.** I reverted `:3834` / `:3854` to the pre-fix fresh read and ran the v3.11 probes. **M2 FAILS** (got 1091.52, want 1186.43), **and M3 does not RED** (27/28 controls). So the probe discriminates the defect it was written for (`delta-3e2359a6/mutant/`).

**Fail-first of the other new probes, read and re-run.** All are GREEN, with every control RED as required, at `66605a1`:
- **(N)** u5 arming. Control N3, "at V38-FULL it still swings", is a real discriminator: with `_hf_on()` false the period is 0.
- **(O)** O0–O10 with controls O1c, O2c, O3c, O4c, O5c, O7c, O8c, O9c, O10c. Each control removes the mechanism: a free slot, an occupant on its slot, not flagged lost, a dead blocker, timer−1, rfa off, persist off, pets out of the system, the Pursue state.

**The carried items:**

| item | at `66605a1` |
|---|---|
| WARN-3(a) | R-6 (ii) is now `n_lethal_floor_ticks > 0` without a death, or `> 1` (`kc2rt_ta_emit.gd`) |
| WARN-3(b) | `player_summon_hits` reports `{modelled, n_hits, site}` off the bound summons fold (`fight.gd:7121`); the "HALTED" comment and the U-5 rationale are corrected |
| WARN-4 | T8 takes the first dying cell of a declared list (M-POL-2 s3, dies w157) and checks identity 2 **as v1.13 restated it**, with the control term. **This explains my earlier deficit of 4:** the legacy v1.1 text omits `n_control_suppressed_channelling`, and the probe now asserts that the legacy gap equals that term exactly. T8 is GREEN |
| INFO-1 | H-4 `shadow_ok` requires `place_shadow_calls > 0` and `petpath_shadow_calls > 0`, and prints "contact solver: not reached at this level". New must-RED control: a shadow cell with zero comparisons |
| INFO-2 | `run_cell` selects `contact=shadow` (ORACLE refuses without the library), and each cell emits `contact_solver_report`. The verdict face gets `_contact_face()` with `zero_mismatches_with_comparisons`. **So the graded attempt now executes the native library in shadow on every cell, and § C.9.8's per-arm fresh shadow is satisfied by the attempt emission itself, at the attempt digest, on its face.** PLAY's session selects `native` and falls back to the exact reference with a header note. The bridge verifies the pin on the exported bundle's `Frameworks/` copy |
| INFO-3 | `f2h_b_holds` moved to `tests/kc2rt_ta.gd`. The literal count in `sim/loader/native` went from 752 to 750 |
| INFO-5 | partial; see INFO-D4 |
| INFO-6 | per-leg deadline 2,400 s; the hole leg now completes inside the suite |
| WARN-1 | discharged by (N), (O) and `ge_fold.report()` in G3 summaries (present in my summaries) |

**WARN-2, checked read-only on disk; I did not run it.**
- `kc2_play/vendor/kc2_runtime/MANIFEST.json` reads `tree_digest` **`3e2359a6…`** and pins model `99711727…`.
- `desktop/KC2Play/build/desktop/KC2Play.app` was built 2026-10-03 02:06, with `Frameworks/libkc2rt_contact.macos.arm64.dylib` = `74360ffa…`.
- drax's commit reports the attempt-2 `.app` header checks true.
- My archive has no `.app`, so my suite's 2 `runtime_header` reds are the environment, as before.

## D.2 · Independent runs at `66605a1`

**G3, contact=shadow, port side, on my own oracle traces.** The oracle is frozen at `969fbd8d`; I generated these traces from my own archive in the first pass. I also produced **one fresh oracle trace with the new tool** (W1 s2). With `engine_src` blanked, it is byte-equal to my earlier trace.

| cell | decision div. | draw mism. | death oracle / port | census · ctrl · x08 · x16 | placement mism. | blocker scans / mism. / goals | oracle_complete |
|---|---|---|---|---|---|---|---|
| **M0 s3** | 0 | 0 | [160,225] / [160,225] | ✓ ✓ ✓ ✓ | 0 | 44,707 / 0 / 277 | ✓ |
| **W1 s2** | 0 | 0 | [160,161] / [160,161] | ✓ ✓ ✓ ✓ | 0 | 41,332 / 0 / 136 | ✓ |
| M-POL-2 s2 | 0 | 0 | [160,221] / [160,221] | ✓ ✓ ✓ ✓ | 0 | 43,657 / 0 / 204 | ✓ |
| M0 s0 | 0 | 0 | survived / [160,576] cleared | ✓ ✓ ✓ ✓ | 0 | 30,381 / 0 / 131 | ✓ |
| W1 s2 (fresh oracle) | 0 | 0 | [160,161] / [160,161] | ✓ ✓ ✓ ✓ | 0 | 41,332 / 0 / 136 | ✓ |

- All 4 summaries equal drax's filed `…-kp274-…-66605a1/summaries/` **in every key except `trace_sha256`**: different oracle-trace files, same content modulo the path field.
- They are also equal to my `fd799b63` summaries on every comparison count. BLOCK-1's state is not reached on these cells, as predicted.

**Suite** (`run_kc2_runtime_suite.sh`, 2,400 s deadline):

| battery | checks / failures | controls RED |
|---|---|---|
| loader | 135 / 0 | — |
| rules | 58 / 0 | — |
| purity | 0 violations | — |
| hole | 56 / 0 | 13 / 13 |
| v3.6 | 37 / 0 | 9 / 9 |
| completion | 48 / 0 | 18 / 18 |
| loop | 25 / 0 | 12 / 12 |
| v3.7 | 71 / 0 | 16 / 16 |
| v3.7.1 | 57 / 0 | 15 / 15 |
| v3.8 | 31 / 0 | 15 / 15 |
| **v3.11** | **80 / 0** | **28 / 28** |
| contact-native | 31 / 0 | 11 / 11 |
| H-4 | 34 / 0 | 31 / 31 |
| **attempt-2** | **54 / 2** | 16 / 16 |
| emission (run separately) | 30 / 0 | 9 / 9 |

- Attempt-2's two failures are `runtime_header` only (no `.app` in my archive). T8 is GREEN.
- **Controls: 193 / 193 RED** (177 without attempt-2).

## D.3 · H-5 re-confirm at `3e2359a6`, per § 7

1. **Runtime-side pin, keys and literals.**
   - The pin is unchanged: `kc2rt_pack_of_record.gd:46/48`, model `99711727…` and reference `af58ef40…`; the suite prints `PACK PASS | DIGEST PASS`.
   - Pack-key check: **268 found / 39 non-key labels**, identical to `fd799b63`.
   - Literal scan over `sim/`, `loader/` and `native/src`: **0 rows on lines added or changed in `96fc0cc..66605a1`** (`scan/scan_delta.tsv` is empty). Total 750, down 2 with the INFO-3 move.
2. **Suite:** per D.2. Every legacy battery keeps its size; v3.11 gained 19 checks and 12 controls. No assertion was weakened: the T8 change replaces an ill-posed fixture and **adds** a legacy-gap assertion.
3. **G3:** drax's 25/25 at `66605a1`, plus my 5-cell sample, plus the attempt emission's own per-cell shadow (INFO-2).

**Oracle-side closure:** unaffected. The oracle and pack are unchanged, so § 5's 14-capture proof stands.

**The H-5 WARNs:**
- **WARN-A is discharged.** The GD half of holes 4, 6 and 14 and the chance-gate path now have probe pins with must-RED controls: (O) slot choice and stealing, pets taking slots and suppression, plus (N).
- **WARN-B is reduced to INFO.** The sub-states have fixture probes, and G3 summaries carry `ge_fold.report()`. Their *reach on graded cells* is now readable from telemetry; carry it on the seal record.

**Re-opened holes: none.**

## D.4 · INFO (delta)

- **INFO-D1 · (M) pins the bleed path and the consumption, not the tick-order placement.** Soulfire and `_mut_snapshot()`'s position in `_tick` (before the disc) are verified by reading only. A future edit that moves the snapshot after the disc would pass (M). Optional: a tick-level fixture that runs one real `_tick` with a dying slot in reach. (drax)
- **INFO-D2 · (O6), the RFA exit on arrival, has no control.** Every other (O) item does. (drax, optional)
- **INFO-D3 · 5b525ec's new statue expectation is a self-consistency check.** It asserts the maximum of the pack's `gr2` rows equals `_max_reach`, where it used to assert an independent 10 m literal. This is correct under the v3.8 fire-range law and PLAY-gate-only, but weaker as an instrument. (drax, record only)
- **INFO-D4 · INFO-5 is only half fixed.** `engine_src` is now recorded as the last two path components (`engine/src` for me, `eng311/src` for drax), so traces are still not byte-equal across checkouts whose directories are named differently. Record a fixed token, or omit the field. (drax, non-blocking)

## Delta verdict

**H-3 (delta on d7b4846 + b1d2c9e; 5b525ec outside the digest): PASS.**
- BLOCK-1 is fixed term for term against `run.py:2945-2953` / `secondary_streams.py:277, 293`, and its probe is shown to discriminate by mutation.
- WARN-1/3/4 and INFO-1/2/3/6 are discharged; INFO-5 is partial.

**H-5 at `3e2359a6`: PASS-WITH-FINDINGS, re-confirmed per § 7.** The closure proof stands, the runtime-side scans are clean on the delta, every control is RED, and no hole has re-opened.

**From my side, `3e2359a6` is clear for the attempt**, subject to the parallel session's H-2 / H-7 at this digest and to the `.app` header checks reading true at launch.

## Delta action

- [ ] **gandalf:** record H-3 PASS (BLOCK-1 discharged) and H-5 PASS-WITH-FINDINGS re-confirmed at `3e2359a6`, plus the § 6 total corrigendum (164 / 180, not 236).
- [ ] **drax (non-blocking, next change):** INFO-D1, D2, D4.
- [ ] **H-7 session:** the deficit-4 reading is explained (the control-suppressed term); T8 now checks the restated identity.
