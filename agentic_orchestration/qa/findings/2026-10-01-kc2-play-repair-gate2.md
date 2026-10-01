# Finding — 2026-10-01 — Run KC2-PLAY · REPAIR GATE-2 (R-1…R-22, holes 1–17 + 5b, the chance gate, C-11a, the `TA-X-07` leak fix, BLOCK-1 Path B, the census, G3 ×25, G2, H-4, H-6)

**Reviewer:** jack-ryan (DEV-MODE, gatekeeper for Run KC2-PLAY; conductor gandalf)
**Severity:** **BLOCK (2, both scoped to attempt 1) · 0 ESCALATE · 2 WARN · 7 INFO.** The REPAIR itself passes: every item the brief listed (1–8) is PASS or PASS-WITH-WARN. **Both BLOCKs are § H attempt preconditions that the runtime under gate does not meet: H-2 (`spawn_by_record`) does not exist anywhere in the runtime, and H-3 (`TA-X-29(e)` on the `WALK` configuration) is undischarged, with the port's own emitter returning w160 = 4.930528 against the prereg's 4.980316.** The second one predicts a `STRUCTURAL` red, which would spend attempt 1 of 2.
**Attempt 1 may NOT fire.**
**Target:** godot runtime tree FILE `fda00e2876405cec4ff73d8ab836679539ca96b1e77b22a47750cbd598c09a86` (82 members), at godot `ada8048` / `e40a4fc`, and the evidence commit `3956a4f`. Pack v3.7.1: model `48a4c94c…`, reference `1887257f…`. Oracle: engine `22cd2288`. Prereg of record: v1.12 FILE `a0454776…`.
**Developer:** drax (port) · gamora (H-6 note, collab `267dfac03`) · gandalf (conductor)
**Principles applied:** REVIEW_PROCESS #1 (math before code) · #2 (smoke gate) · #4 (the committed record is the truth) · #5 (severity matters). Disciplines #11 (empirical inspection over assumption) and #12 (semantic-shifting fixes need explicit framing). ADR-002. Charter KP-133, KP-136…KP-172.
**Read-before-result attestation:** no graded run exists under v1.12, and I ran none. I read godot only through git objects (`git show`, `git diff`, `git grep`, `git log -S`) and through a `git archive` of `3956a4f` extracted into my scratchpad, where I ran the suite, the emission probe and G3. Nothing in drax's working tree was checked out, run or written. The engine was read and executed read-only at `22cd2288` (HEAD; no tracked modification; `PYTHONDONTWRITEBYTECODE=1`). Every Godot and oracle run was taken under the heavy lock.

---

## What I found

### Pins re-derived (Discipline #11)

| claim | how I checked | result |
|---|---|---|
| runtime tree `fda00e28…`, 82 members | MANIFEST law recomputed over the 82 member blobs at `3956a4f` | ✓, 0 member mismatches; only `MANIFEST.json` itself sits outside the member set |
| `3956a4f` touches only `evidence/` | `git show --stat` | ✓ (51 files under `evidence/kc2-play/2026-10-01-g3-25cell/`) |
| `kc2rt_fight.gd` `5dfb865c…`, `kc2rt_laws.gd` `c234376e…`, G3 tools `50908a22…` / `90a03620…`, census `ecdea42e…` | sha256 of the extracted files | ✓ all five |
| pack v3.7.1 model `48a4c94c…` (19 members), reference `1887257f…` (7 members) | each pack's own digest law, every member re-hashed | ✓ both, 0 member mismatches |
| prereg v1.12 `a0454776…` | sha256 | ✓ |
| engine at `22cd2288`, oracle unmodified | `git rev-parse HEAD`; `git status` over tracked paths | ✓ HEAD = `22cd2288…`; no tracked modification; `simulation/kc2` clean |

### Item 1 · R-1…R-22, holes 1–17 + 5b, the chance gate, the C-11a grant law: **PASS**

**The suite, re-run by me** on the `3956a4f` extraction, under the heavy lock: **SUITE GREEN, exit 0, 0 `FAIL` lines.**

| battery | checks | negative controls RED as required |
|---|---|---|
| loader smoke | 135 / 0 failures | — |
| rules smoke | 58 / 0 | — |
| hole probes: holes 1–7, R-4, R-5 (DoT, aura and granted-row kill variants) | 56 / 0 | 13 / 13 |
| v3.6 probes: R-18 grant law (removal 131/157, coverage, stacking, rider, resist), R-19 label ≡ gate, C3/C4 inert, d1 | 37 / 0 | 9 / 9 |
| completion probes: holes 8–17, 5b, the chance gate, R8, R-17(b)(d) | 48 / 0 | 18 / 18 |
| loop probes: board, energy, channel, drive, wave advance, deferred arrival, counterplay, raw, tps, float64 | 25 / 0 | 12 / 12 |
| v3.7 probes | 71 / 0 | 16 / 16 |
| v3.7.1 probes: arms from `a8`, run state, the control gate, `PX-LO`, r9, Neumaier, the leak (K), (L2) operands, the census | 53 / 0 | 13 / 13 |
| H-4 probe | 20 / 0 | 5 / 5 |
| T-0, purity, 30 `--check-only` legs | green | — |

Each hole probe carries a negative control that re-creates the pre-repair behaviour and must go RED. **That is the fail-first evidence**, and all 86 controls went RED.

**Spot reads in source at `5dfb865c…`:**
- the chance gate is `if u > chance` (`:3169`);
- mitigation is `ARMOUR_THEN_RESIST` per V0-08 (`:5518`, `:5635`);
- the resist cap reads `PLAYER_DEFENSE_CAP_PCT` (`:5608`);
- `fsum` is a correct `math.fsum` replica (`kc2rt_laws.gd:115`).

**R-22** was disposed at KP-144, and its instrument is G3 (item 5). **R-21's** `.app` header is drax-reported; I did not rebuild or run the `.app` (INFO-1).

### Item 2 · The `TA-X-07` leak fix (KP-167/169): **PASS**

I read the whole `933b438 → ada8048` diff of `kc2rt_fight.gd` (+141 lines).
- **The two bookings.** Packets still queued at wave close are booked `dropped` in `_defer_close_wave` (V5-LIMB-3 and the oracle's `drain_at_wave_end`). Packets popped after the player's death (the `break` at `run.py:3484–3485`) are booked `dropped` in `_defer_arrivals`, per KP-169 Ruling 2, with the amount `direct + pcl` at cast.
- **The fight is unmoved, by construction.** Every added line is emission only: counters, `split` flags, an extra slot in the burn tuple that only the flag reads, and the `_land(…, carried)` parameter. The `_defer_arrivals` rewrite keeps the same `break` at the same index. No added line writes `player_hp`, draws from any stream, or touches a decision input.
- **Residual.** From drax's 25 lossless operand lines, max `ρ̂` = **2.2138341115505915e-16** (≤ 2.21e-16 as briefed). **21 cells are exactly 0.0**, not 19; gamora's correction (KP-172) is right.
- **Empirically,** my G3 re-runs reproduce drax's oracle traces and summaries bit for bit (item 5).

### Item 3 · BLOCK-1 cleared by Path B: **PASS-WITH-WARN (WARN-1)**

- **What is in place.** The packet path's carried roundings are counted (`_pkt_roundings` = rows − 1, plus 1 for `direct + pcl` when both are non-zero, plus `_cp_last_roundings`) and flagged on the booking that receives them: `applied` at `:5576`, and `dropped` at `:4136`, `:4172` and `:4734`. The census classes all eight of those rows F(f). `q_applied` and `q_dropped` are > 0 on all 25 cells. **That closes the indicator gap BLOCK-1 named for `applied`.**
- **What is not.** `counterplay_absorbed` is still classed T, with `q = 0` on all 25 cells. My Path-B text named flags there. **WARN-1** below rules on it, together with the conductor's question (a).

### Item 4 · The census against my WARN-1 criteria: **PASS (WARN-2, INFO-2)**

- **(a) Per site × caller path.** 47 rows over 35 sites (T 28 · S 11 · F 8). Every caller of a multi-caller helper has its own row. I enumerated the callers myself: `_land` 6/6, `_cp_absorb` 3/3, `_ss_hit` 2/2.
- **(b) S is not defined by assertion.** `verify()` requires every S row to carry `, true)` and every F row to carry a flag.
- **(c) Checkable by machine.** I re-implemented `kc2rt_census_grep.py`'s match over `git grep` at `3956a4f`: **35 sites = 35 census sites, row for row, code verbatim, 0 differences.** A broader grep for `_cons_add(` and `_offer(` anywhere on a line finds 37 = the 35 sites plus the two function definitions, so no inline call site escapes the anchored pattern. The per-row accumulator matches each call's literal key.
- **(d) Every terminal path enumerated.** 29 paths, counted. The unbound-PCL branch (`:5433`) is counted and emitted: `n_unbound_pcl_rows` = 0 on 25/25. **INFO-2:** the caster-death `VOID` path is not named. It is unarmed: the record is `CasterDeathLimb.PERSIST` (`deferred_arrival.py:266`), and the port has no void path. The census should name it as unarmed rather than leave it silent.
- **WARN-2:** the conductor's question (b), ruled below.

### Item 5 · G3, five arms × five salts: **PASS**

**The filed evidence (`3956a4f`):**
- **Hashes.** MANIFEST: 50/50 files hash-verified. Every summary's `trace_sha256` equals its trace's uncompressed sha256.
- **The counts, 25/25.** `injected: []`; decision divergences 0, with all eight classes 0 per cell; draw mismatches 0; `port_only_streams: []`; oracle-only streams exactly `spawn_structure.py:344|0` and `player_kit_residual.py:286|<seed>`; `death.equal` true. The summary's arm equals the trace's arm on every cell.
- **The POST figures.** Each oracle trace's `(wave, seconds)` equals § B.1a's instrument-free figures for its arm on every salt (M0 / M-POL-2-NULL `[155,151,156,155,155]` · `[7.347,13.143,7.347,6.449,5.143]`; M-POL-2 / W1-NULL `[156,152,155,152,152]` · `[7.184,4.408,7.02,7.184,6.122]`; W1 `[156,152,155,152,155]` · `[6.286,4.408,7.02,7.184,6.939]`). The seconds are `k × 0.0816326530612245`.
- **Arm composition.** The oracle tool's five arms match § B.1a's distinguishing rows: M0 = `seat=False`; M-POL-2-NULL = `ChannelPolicyFold(armed=False)`; W1 = `ArenaFold(armed=True, avoidance=True)`; W1-NULL = `ArenaFold(armed=False)`. They apply only to the graded `run_cell` call. Every hook forwards to the oracle's own function.

**My independent re-run**, oracle at `22cd2288`, under the heavy lock, as many cells as the shared lock allowed. See the table at the end of this item.
- Re-run cells reproduce the filed oracle trace **bit for bit** (same `trace_sha256`).
- The port summary is identical field for field.

**5 of 25 cells re-run, one per arm at salt 0.** The shared heavy lock was held by Run C-9's Blender queue (the first cell waited about 17 minutes). An uncontended cell takes about 160–300 s. I stopped after the salt-0 row rather than hold the lock queue for hours.

| cell | summary identical to filed | oracle trace sha identical | decision div. | draw mm. | death (wave/k) port = oracle | POST |
|---|---|---|---|---|---|---|
| M0 · 0 | ✓ | ✓ `59885e9d…` | 0 | 0 | 155/90 | 155 / 7.347 ✓ |
| M-POL-2 · 0 | ✓ | ✓ | 0 | 0 | 156/88 | 156 / 7.184 ✓ |
| M-POL-2-NULL · 0 | ✓ | ✓ | 0 | 0 | 155/90 | 155 / 7.347 ✓ |
| W1 · 0 | ✓ | ✓ | 0 | 0 | 156/77 | 156 / 6.286 ✓ |
| W1-NULL · 0 | ✓ | ✓ | 0 | 0 | 156/88 | 156 / 7.184 ✓ |

**Assessment.** All five arms, including the three new ones, reproduce bit for bit from a clean extraction. The oracle is deterministic, so a byte-identical trace on each arm, together with the hash-verified filed evidence for the other 20, is sufficient. **G3: PASS on 25/25.**

### Item 6 · G2 705/705 and H-4: **PASS (INFO-3)**

**H-4** printed GREEN on my run of the H-4 probe (20/0, 5/5 controls):
- the label is read from the pinned prereg (`kc2rt_prereg_of_record.gd` → v1.12 `a0454776…`, refuses on mismatch);
- `substrate_epoch` equals the prereg;
- all seven `a8` job ROWSETs equal § B.1a;
- every arm reports `configured_from_a8 true`;
- the **`setup` partition is 8 / 19**, with C `207ab21f…`, T `ab319772…`, and T applied to no arm;
- **`TA-X-18`:** bits `c00fffffffffffde` / `be9777a5cf72cec6`, lossless, round-trip probe true, equal;
- **the OQ-15 tripwire:** `path_used` is the engine CSV, `sha_measured` = `cb6a008b…` = P-i = the `IC7-F-44` image;
- `r11_bound` evaluates **β in exact rationals** (`beta_exact`, decision on the exact value);
- `g3_block` checks § C.9.7 and the POST figures;
- the retired `r11_budget` / 4,500 face is gone.

**G2 705/705 is drax-reported.** I did not run the G2 fixture (INFO-3). The diff makes it moot for this gate: no line of the damage-resolution path changed after the pass-3 G2 record.

### Item 7 · H-6: **PASS**, on gamora's note (collab `267dfac03`, FILE `63915bca…`)

**Independent check.** I re-evaluated (L2) in exact rationals (`fractions.Fraction`) from drax's 25 lossless operand lines, with the law as written:
- **β matches gamora and drax on 25/25**;
- worst **M0·0 = M-POL-2-NULL·0, β = 3.582525e-14, margin ×27.91** (Λ 322.69);
- `f_max` 160 / 120 / 100 as she reports;
- all four antecedents hold.

**Her coarse sensitivity bound** (2φ on all seven accumulators) also reproduces: worst **1.4254e-13, ×7.02**, 25/25.

**WARN-2 and INFO-2/INFO-3 are discharged** by her §§ 1, 8 and 9:
- the relaxation direction is named;
- the β method is stated;
- the exposure is stated.

### Item 8 · Anything that changes ORACLE behaviour: **NONE. No HALT.**

- Engine HEAD is `22cd2288`, with no tracked modification.
- The oracle-trace tool only wraps and forwards; no oracle expression is replaced.
- My re-run traces are bit-identical to drax's.

### ⛔ § H, not in the brief's list, and checked because the verdict must say whether attempt 1 may fire

**⛔ BLOCK-1 · H-3: the port's `TA-X-29(e)` is not the v1.10+ row, and its w160 value is wrong.**

I ran the emission probe (the same `kc2rt_ta_emit.gd` emitter the T-A harness uses; one cell, not graded) on the `3956a4f` extraction. It prints:

`TA-X-29(e) PENDING v1.8 — port: {"w159": 3.20776401984497, "w160": 4.93052801428496}`

| wave | port | prereg v1.12 (config E, § F.2h / v1.8 § A.4) | |
|---|---|---|---|
| w159 | 3.20776401984497 (16 priced) | **3.207764** (16 of 21 priced) | ✓ |
| w160 | **4.93052801428496** (18 candidates, 18 priced) | **4.980316** (23 of 28 priced) | **✗, off by 0.0498 (1.0 %)** |

Three further gaps:
- **It matches no configuration in v1.8's attribution table.** w160 is 5.418200 under A/B, 4.968706 under C/D and 4.980316 under E. The port prices 18 records at w160; E prices 23 of 28 candidates.
- **The emitter is still the v1.7-era form.** It compares records to the v3.4.2 `z4` rows (one disagreement at w160, `nemesis_aetherial_01`, one of the four records C-11a moves), not to the prereg's per-record table. It is **not configured from the `WALK` `a8` rows** (`pools_for(w, bonus_spawns_enabled=True)`, `fold_at(w, to_hit=True, attack_speed=True)`, the `gmg` resolver, the P-5 `load_profiles` `IC7-A-0411`).
- **The graded per-record ratios are absent.** H-3 requires the **39 per-record ratios** (w159's 16 priced + w160's 23 priced, the § F.2h table v1.10/v1.11 reproduce). The port has only 34 priced records (16 + 18), and it emits no per-record ratios against that table. The ten-wave walk is emitted-not-graded, so it is not part of this BLOCK.

The emission probe asserts only *"EMITTED"* on a non-v3.4.2 pack, so it is green over a wrong number: an instrument returning cleanly after it stopped answering the question.

**Consequence:** `TA-X-29` is one of the 28 EXACT rows. Graded on this runtime, (e) is RED at w160, or UNGRADEABLE for the missing per-record values. **A RED makes the verdict `STRUCTURAL` and spends attempt 1 of 2** (§ G: STRUCTURAL is evaluated first).

**Not ruled here:** whether the w160 gap is a port defect in the static profile build for records that never spawn on the traced boards (G3 cannot see those, because it compares only bodies that spawn), or a walk-definition difference. R-22's rule applies: trace it to its first differing record and give it a cause.

**⛔ BLOCK-2 · H-2: `spawn_by_record` does not exist in the runtime.**

`git log -S"spawn_by_record" --all -- kc2_runtime` returns **nothing**: the field has never been written. `grep` over the 82 members finds no per-record spawn-class emission. `board.ta_x_25_inputs()` emits only clauses (a)/(b)/(d), and its prose is still the v1.7 text (*"the port still classifies POOL-466 on the v3.3 basis (338 NO-DATA)"*). v1.8 § F.2f's emission requirement states it in so many words: *"Its absence makes (c) UNGRADEABLE → `INDETERMINATE`."* So, even with BLOCK-1 fixed, a graded run on this runtime is `INDETERMINATE` by construction. **That is the v1.12 § G.1 rule for (L2), applied to a different row: firing would consume nothing and buy nothing.**

---

## The conductor's two census questions (gamora's H-6 § 7), ruled

**WARN-1 · (a) `counterplay_absorbed` (`:3968` `cut`, `:3990` `taken`), classed T with `q = 0`: misclassified for the record.**
- **Where the census is right and where it is not.** It is right that each remainder subtraction's rounding lands on the downstream `applied` booking. It is wrong about the **magnitude basis**. The packet sum's error (R − 1 roundings, `|e| ≤ γ_{R−1}·Σ appliedᵢ`) and the burn aggregation's error scale with the whole packet entering `_cp_absorb`, not with the landed share.
- **When the packet is absorbed whole** (`d2 ≤ 0`, `:4106`, `:4151`), no flagged term carries any of that mass.
- **By the prereg's own T definition** (*"telescopes exactly against its offered counterpart on the floats as formed"*), `cut` and `taken` do not qualify, because the packet float they split is itself `fl(Σ appliedᵢ)`.
- **This is the omission my Path-B text named.**
- **Size.** Charging `φ·A_cp` (cp flagged) moves β by at most **1.5e-16** on any cell. The worst cell becomes **3.590829e-14, ×27.85**, and all 25 still hold. I computed this exactly.

**WARN-2 · (b) DOT_INC (`:4638`, `per_tick·n − inc_total`): the F(f) premise is false under cancellation, and the defect is in v1.12's wording before it is in the census.**
- **The premise.** § F.2k.3/F.2k.4 bound an F(f) term by `γ_f·|x|`. That holds for one-signed chains, not for a difference of carried values. The DOT_INC error scales with `Σ inc ≈ mit_total`, while `|x|` (the MAX-merge loss) can be near zero. **My v1.12 pre-read did not catch this. Recorded against my own pre-read.**
- **The correct statement.** A chain's error is bounded by `γ_f × the absolute mass of its TERMINAL bookings`.
- **Why the as-written law then holds.** Under that statement, (L1)'s `φ·Σ_{q_k>0} A_k` remains a valid bound **provided every terminal accumulator is flagged**, because `φ = γ_{2·f_max}` leaves factor-2 slack for the one mass that two chains share (DOT_INC then BURN). With `counterplay_absorbed` flagged, every terminal accumulator is flagged. Without it, the only unflagged terminal is `counterplay_absorbed`, which is exactly WARN-1.

**Ruling: neither point can change any cell's gradeability, so neither alone would block.**
- **The numbers.** gamora's 2φ-on-everything bound is sound under the corrected chain-mass derivation (it dominates DOT_INC + BURN + S on a shared term), and it holds on 25/25 at ×7.02. The as-written β with cp charged holds at ×27.85.
- **The record must still be corrected**, and it costs nothing extra, because BLOCK-1 and BLOCK-2 force a new runtime digest anyway. **So the corrections ride in that revision and are conditions of my delta gate, not forward-carried WARNs:**
  1. **drax:** flag the two `_cp_absorb` bookings (`split = true`, `n_round` ≥ 1; emission only) so that `q_counterplay_absorbed > 0` wherever the layer fires.
  2. **drax:** reclass `:3968` and `:3990` (three callers each) as F, with the carried chain named.
  3. **drax:** restate the census CHAINS block on the **terminal-mass basis**, including the domination of the shared DoT mass by `φ = γ_{2 f_max}` (`2·f_max ≥ 2N + 2K + 4`, from emitted counters, per cell).
  4. **gamora,** in the next prereg version whenever one is cut (**not required for attempt 1**): amend § F.2k.3's F(f) premise to the terminal-mass statement, as a Discipline #12 corrigendum. It enlarges no bound, so it needs no Matt route.

---

## INFO

- **INFO-1.** R-21's `.app` header (`48a4c94c…`, read by running it) is drax-reported. I did not rebuild or run the `.app`.
- **INFO-2.** The census does not name the caster-death `VOID` path. It is unarmed (`PERSIST` record). Name it as such.
- **INFO-3.** G2 705/705 is drax-reported, not re-run here. No damage-resolution line changed since the pass-3 G2 record.
- **INFO-4.** `kc2rt_v3p7p1_probes.gd` (K) carries a stale comment: *"the after-death skip: NOT booked (halted, no named sink)"*. The assertion beneath it checks the KP-169 booking (`dropped` 500). Fix the comment.
- **INFO-5.** The ledger's "19 cells exactly 0" (KP-170) is **21**. gamora's KP-172 correction is right.
- **INFO-6.** The H-4 print shows `W1-NULL … avoidance true` beside `walls false`, so the avoidance limb is inert without an armed arena. G3 on W1-NULL = M-POL-2 confirms the behaviour. T-0's `TA-X-18 scatter polar [-4.0, 0.0]` is a `%f` print, and the bits are graded by H-4 (§ F.2l), which is correct.
- **INFO-7.** `ta_x_25_inputs()` prose is v1.7-era (the 338 NO-DATA basis). Rewrite it with the H-2 work so the emission does not describe a port that no longer exists.

---

## Rationale

- **Items 1, 2, 5, 6, 7, 8: PASS.** Principle #2: I re-ran the smoke gate myself. Discipline #11: the pins, the census match, β and G3 were re-derived independently, not read off claims.
- **Item 3: PASS-WITH-WARN, and item 4: PASS.** WARN-1 and WARN-2 are Discipline #11 / Principle #1 completeness points in the (L1) derivation. Principle #5: neither can move a cell, as shown by a sound bound at ×7.02.
- **BLOCK-1 (H-3) and BLOCK-2 (H-2).** Principle #4: § H says *"OWED BEFORE v1.12 ATTEMPT 1 (blocking)"*, and the committed runtime does not carry either item. BLOCK-1 is a **predicted STRUCTURAL red on an EXACT row that would spend one of two attempts**. That is the most expensive kind of progress the run can make in the wrong direction, and it is cheapest to stop now. BLOCK-2 makes any attempt `INDETERMINATE` by construction. Both are pre-registered emission obligations carried unchanged since v1.8/v1.10. No KP row records either as discharged, and none of the four documents that fed this gate (KP-170, gamora's note, the brief, my pre-read) named them. I name that so the next gate checks the § H list itself rather than the brief's.

**Overall verdict: BLOCK (2, attempt-scoped).** The repair is PASS-WITH-WARN, and the runtime's fight is G3-exact on five arms × five salts. **Attempt 1 does not fire.**

## Action

- [ ] **drax, BLOCK-1 (H-3).**
  - Re-point the `TA-X-29(e)` emitter to the `WALK` `a8` configuration (`IC7-A-0379`…`0432`: `pools_for(w, bonus_spawns_enabled=True)`, `fold_at(w, to_hit=True, attack_speed=True)`, the `gmg` resolver, the P-5 `load_profiles` of `IC7-A-0411`).
  - Emit w159/w160 and the 39 per-record ratios (16 + 23 priced) against the § F.2h table. Print the ten-wave walk as emitted-not-graded.
  - Reproduce `3.207764` / `4.980316` and the 39 values, at the row's declared precision.
  - Trace any residual (w160 now) to its first differing record and give it a cause, per R-22: a port defect repaired with a fail-first probe; an oracle issue routed; nothing tuned.
  - Make the emission probe **compare** against the prereg's values instead of asserting "EMITTED".
- [ ] **drax, BLOCK-2 (H-2).**
  - Emit `spawn_by_record: {record_path: {n_bodies, class}}` per arm per salt, over roster bodies only, summing to (b)'s counters, per v1.8 § F.2f(c).
  - Add a probe with a negative control. Replace the v1.7 prose (INFO-7).
- [ ] **drax, in the same revision.** WARN-1 items 1–3 (cp flags, cp reclass, census CHAINS on the terminal-mass basis), INFO-2, INFO-4.
- [ ] **drax.**
  - Regenerate the MANIFEST and re-pin.
  - **G3 at the new digest.** A carry-forward of this G3 record is acceptable **only if** every file on G3's path (`sim/`, `loader/`, `kc2rt_pack*.gd`, both G3 tools) is byte-identical to `3956a4f`. A counter added to `kc2rt_board.gd` or `kc2rt_fight.gd` means a re-run on all 25 cells.
  - Re-run the suite and the (L2) operands.
- [ ] **gamora.** Re-evaluate (L2) at the new digest. With cp flagged I predict a worst β of 3.590829e-14, ×27.85. Note WARN-2 for the next prereg version (item 4).
- [ ] **jack-ryan.** Delta Gate-2 on the new digest: the diff, H-2/H-3 evidence, the WARN-1 corrections, the G3 record. It is not a full re-gate. Items 1–8 above stand for every file the delta does not touch.
- [ ] **gandalf.** Ledger row. Record that the § H list (H-2, H-3) was outside this gate's brief and is now in it. Fold KP-172's 21-cell correction.
- [ ] **Matt.** Nothing to decide. No ESCALATE: neither BLOCK touches a locked decision or a tolerance, and no graded attempt has been spent.

## References

- Runtime under gate: godot `ada8048` / `e40a4fc` / `3956a4f`. Extraction at `<scratch>/gd/` (git archive of `3956a4f`: `project.godot` replaced by a minimal one with the autoload and plugins stripped; nothing else changed).
- `kc2_runtime/sim/kc2rt_fight.gd` (`5dfb865c…`): `:3955–3995` `_cp_absorb` · `:4075–4175` the packet and deferral paths · `:4600–4640` `_dot_open` · `:4698–4745` `_burn_dots` · `:5568–5580` `_land` · `:6540–6558` `_cons_add` · `:6640–6672` `l2_operands`.
- `kc2_runtime/tests/kc2rt_booking_census.gd` (`ecdea42e…`) · `tools/kc2rt_census_grep.py` · `tests/kc2rt_h4.gd` · `tests/kc2rt_ta_emit.gd:454–548` (`gmag_conformance`) · `sim/kc2rt_board.gd:870–927` (`ta_x_25_inputs`, `report`) · `tests/kc2rt_emission_probe.gd:217–236`.
- `evidence/kc2-play/2026-10-01-g3-25cell/` (MANIFEST `379b6dbb…`).
- Prereg v1.12 §§ B.1a, C.9, F.2k, G, G.1, H. v1.8 §§ A.4, F.2f. v1.10 § A (the `TA-X-29(e)` ten-wave values).
- gamora's H-6 note `agentic_orchestration/gandalf/notes/2026-10-01-kc2-play-h6-discharge-v1.12.md` (collab `267dfac03`).
- My v1.12 pre-read `agentic_orchestration/qa/findings/2026-10-01-kc2-play-prereg-v1.12-pre-read.md` (collab `1e8bcd1e3`).
- Charter KP-133…KP-172.

---

# ADDENDUM — DELTA GATE-2 on runtime `a9b756cd…` (condition 6), with condition 5 (L2) done here

**Date:** 2026-10-01 · **Reviewer:** jack-ryan · **Severity:** **PASS (0 BLOCK · 0 WARN · 3 INFO).** BLOCK-1 and BLOCK-2 are discharged, and WARN-1 and WARN-2 are folded.
**⇒ ATTEMPT 1 (1 of 2 under v1.12) MAY FIRE, on runtime tree FILE `a9b756cddc4a046ca7a755e51d798158bb4cf84928ec1c12bfdb82c5e12165bb`, with the G3 record `evidence/kc2-play/2026-10-01-g3-25cell-kp173/` (MANIFEST `90195c7c…`).** This addendum is the § G.1 / R-7 repair-Gate-2 PASS for that digest.
**Target:** godot `027de54` … `5302c44` (ledger KP-174). I read it through git objects and a `git archive` of `5302c44` in scratch, and ran the suite, the emission probe, the oracle walk and (L2) myself. The engine was read-only at `22cd2288`, and its tracked tree is still unmodified after my runs.

## What changed, and what that means for G3

- **Tree `a9b756cd…`:** recomputed over 82/82 member blobs, 0 mismatches.
- **Exactly seven members differ from `fda00e28`:** `sim/kc2rt_board.gd`, `sim/kc2rt_fight.gd`, and five files under `tests/` (`booking_census`, `emission_probe`, `ta_emit`, `ta`, `v3p7p1_probes`).
- **Two of those are on G3's path, so G3 had to be re-run, and it was.**

## Results

| check | result |
|---|---|
| **H-3 · `TA-X-29(e)`** | **PASS.** See details below. |
| **H-2 · `spawn_by_record`** | **PASS.** See details below. |
| **WARN-1 census reclass** | **PASS.** See details below. |
| **G3 25/25** | **PASS.** See details below. |
| **(L2), condition 5** | **PASS.** See details below. |
| **Fight unmoved** | **PASS.** See details below. |
| **Suite** (my run, `5302c44` extraction, heavy lock) | **SUITE GREEN, exit 0.** Hole 13/13 · v3.6 9/9 · completion 18/18 · loop 12/12 · v3.7 16/16 · **v3.7.1 57 checks, 15/15 controls** · H-4 20/0, 5/5. |
| **Oracle behaviour** | **No change.** |

**H-3 · `TA-X-29(e)`**
- **The walk.** The emitter is now the config-E walk, read from the `WALK` a8 rows. It refuses on a missing or ambiguous row. Its `load_profiles` row `IC7-A-0411` is checked equal, argument for argument, to the setup row `0453`.
- **The values (my emission-probe run).** w159 **3.207764** / w160 **4.980316**. Priced sets are 16 / 23 and unpriced 5 / 5. **All 39 per-record ratios match**, with their printed on and off values exact.
- **Against the oracle (my independent run).** I ran `kc2_v3p7_closure.run_walk(151…160)` at `22cd2288`. **643/643 priced records are bitwise equal** in ratio, on and off, and identical in `folds_attr` and `folds_own`. All ten wave ratios are bitwise equal. Identity counts are 8·94·73·4·53·5·69·95·0·0.
- **The w160 root cause holds.** The v1.7-era candidate set came from `roster.alternatives`, which omits p06 on the fight arm of record. The `WALK` row passes `bonus_spawns_enabled=True`, which brings back `wendigocannibal_h01…h05`. That takes w160 from 18 priced to 23. The oracle's own sum over the 18 is 4.930528014449965, which equals the old port figure.
- **The three ten-wave fixes touch the walk only, not the fight roster.** The fixes are: every row kind except dot and PCL priced; dying slots and toggled auras excluded; HONEST-FAIL `u2` weapon rows priced as supply. They sit in `tests/kc2rt_ta_emit.gd`. They build walk-local row arrays and only read `pack.roster`. The G3 byte-identity confirms the fight saw no change.
- **The probe tolerance is correct.** The probe's `5e-4` equals the row's own grade (v1.9 § F.2h: `EXACT · |Δ| ≤ 5e-4` per wave ratio and per record ratio). A green probe therefore implies a green grade. The probe also asserts the 39 printed values exactly, which is stricter, and its control (one ratio moved by 1e-3) must go RED. A tighter probe tolerance would grade something the row does not.

**H-2 · `spawn_by_record`**
- **The emission.** It is emitted at `_make_body`, the same site as (b)'s counters, with `class` taken from `roster.body_state` (the label is the gate). It covers roster bodies only. The v1.7 prose is retired (INFO-7).
- **The set digests.** The probe checks all four clauses and reproduces the prereg's set digests from the port's own classes: POOL-466 `33c886a1…`, SWING-456 `706a61d5…`, NONSWING-10 `00b4cb0e…`.
- **On the cell (my run).** 15 records; sums 0 / 1 / 26 = (b)'s counters; 27 bodies.
- **The controls.** Four negative controls go RED as required: a non-member key; a class against the swing set; a count off by one; a flipped swing set. The emission probe is GREEN at 30 checks, 9/9 controls.

**WARN-1 census reclass**
- **The match.** My independent `git grep` match at `5302c44` gives 35 sites = 35, row for row, with code verbatim. The broad grep finds 37 = the 35 sites plus the 2 function definitions.
- **The classes.** 47 rows: **T 22 · S 11 · F 14**. The two `_cp_absorb` sites (3 callers each) are now F (R+4 / 2K+3) and flagged `split = true, n_round ≥ 1` (emission only).
- **The CHAINS block** is restated on the terminal-mass basis.
- **The domination check.** `chain_domination` asserts `2·f_max ≥ 2N + 2K + 4` per cell. That covers the shared DoT mass (2N + 2K + 3 roundings) plus the S split on `pool_truncated`. The probe's control (factor 1) goes RED.
- **The VOID path.** Caster-death `VOID` is named **UNARMED** (`PERSIST`, `deferred_arrival.py:266`). There are 30 paths now.
- **INFO-4** (the stale comment in probe K) is fixed.

**G3 25/25**
- **The KP-173 record.** MANIFEST FILE `90195c7ca96e…`; 51 files hash-verified; produced at engine `22cd2288` on tree `a9b756cd`.
- **Byte-identity.** **All 25 summaries and all 25 gzip oracle traces are byte-identical to the `3956a4f` record**; I diffed the sha256 of all 50 files.
- **The counts.** My earlier five re-run cells (one per arm) and § C.9.7 therefore hold at this digest: 0 decision divergences, 0 draw mismatches, the two declared oracle-only streams, death wave and tick equal.

**(L2), condition 5**
I re-evaluated in exact rationals (`fractions.Fraction`; law as written; `φ = γ_{2·f_max}`) from `l2_operands_25cell.jsonl`.
- **All 25 hold.**
- **Worst: M0·0 = M-POL-2-NULL·0, β = 3.590829330577844e-14, margin ×27.85.** That is drax's figure, and my addendum prediction.
- **Every operand is identical to the `fda00e28` emission except `q_counterplay_absorbed`**, which went from 0 to 970–7,016 per cell. So the only change in β is `φ·A_cp`, which is at most 1.5e-16.
- Antecedents: `n·u < 1`; final-sum and sink counts both 6; the census is filed and green.

**Fight unmoved**
- **G3** is byte-identical, so death wave and tick are unchanged on 25/25.
- **`TA-X-07`** still closes on all 25 cells: max `ρ̂` 2.2138341115505915e-16, **21 cells at 0.0**. The `n_k`, `Â_k`, `Ô` and residuals are bit-identical to the `fda00e28` emission.
- **The source diff.** The `kc2rt_fight.gd` diff is `_cp_absorb(raw, carried_in)` plus two flagged bookings. The `kc2rt_board.gd` diff is a counter. Neither changes a state or a draw.
- **G2 705/705** is drax-reported (AGENT_STATE `0802ab1`). I did not re-run it, because it needs the oracle packet log, which is not in the repo. No damage-resolution line changed (INFO-A).

## INFO

- **INFO-A.** G2 705/705 is drax-reported at this digest. The two independent instruments above (G3 bytes and (L2) operand bits) show the fight did not move.
- **INFO-B.** `walk_config` reads `to_hit` and `attack_speed` off the a8 rows (both true) but does not use them: `walk_config_e` takes `M_inst` from `pack.offense_fold.m_inst_by_wave`. The result is bitwise the oracle's `fold_at(w, True, True)` on all ten waves. It should still assert that those two flags are true, or select by them, so a future arm with false flags cannot silently price at the wrong `M_inst`. This does not block.
- **INFO-C.** gamora's H-6 note (`267dfac03`) evaluated `fda00e28`. **For `a9b756cd`, this addendum is the (L2) evaluation of record**, at gandalf's request (condition 5). For the next prereg version, the WARN-2 premise amendment (§ F.2k.3, terminal-mass basis) stays owed, as stated above. It is not an attempt precondition.

## Verdict and what remains

**PASS. Attempt 1 may fire** on tree `a9b756cd…`, prereg v1.12, pack `48a4c94c…` / `1887257f…`. The H-4 `g3=` input must be `evidence/kc2-play/2026-10-01-g3-25cell-kp173/summaries/`.
- **Still owed, none of it an attempt precondition:**
  - **H-5:** my hole-closure finding at the graded digest. It gates the quotability of a PASS, not the firing.
  - **H-8:** Matt's T-C on the graded digest. It is a seal condition.
  - The next-version WARN-2 corrigendum.
  - **INFO-B.**
- **§ G.1 checklist at `a9b756cd`:** KP-167 repair ✓ · G3 five arms × five salts ✓ · this repair Gate-2 PASS ✓ · H-7 filed (`1e8bcd1e3`) ✓ · H-6 (L2) on all 25 ✓ (here) · H-9 / H-10 discharged ✓ · H-2 ✓ · H-3 ✓ · H-4 ✓.
