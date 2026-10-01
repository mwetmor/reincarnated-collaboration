# Finding — 2026-10-01 — Run KC2-PLAY · REPAIR GATE-2 on drax's attempt-1 repairs (KP-179)

**Reviewer:** jack-ryan (DEV-MODE, gatekeeper for Run KC2-PLAY; conductor gandalf)
**Severity:** **The repairs PASS-WITH-WARN: 0 BLOCK · 1 WARN · 7 INFO. ⛔ NEW HALT TO MATT under KP-178 law (a).** Every repair item passes. The law (a) audit, run once against v1.12, finds a **second EXACT row the oracle cannot pass on its own graded arms. `TA-X-08` identity 2 (`n_channelling + n_released = D`) fails on the oracle's own reference realisation on 19 of 25 cells.** On every one of the 19, the shortfall equals the number of ticks on which the native control fold (KP-147, v3.7) suppressed a channel the channel fold had left on. This is a prereg defect, not a defect in drax's work. WARN-1 carries it. Per the brief, it goes to Matt.
**Target:** runtime FILE `e584477b3d3c8bd6aa69bc43be32a137ab7b875a6c745aae40ccb20bb0e0591a` (84 members), godot `b4c1ff3`. Repair commits: `0e37db9` (TA-X-08) · `3482aef` (PRE_FIGHT) · `4b019e6` (P-2) · `a8512c4` (emission + verdict file) · `f18e92c` · `8b8efe8` · `c84d5d4` (G3 + L2). G3 evidence `evidence/kc2-play/2026-10-01-g3-25cell-kp177/`, MANIFEST `78bbcc8dbf39eb30fc8e89b35a7a80b8375394a4ddbe64d39a65b4984d351fcb`.
**Developer:** drax (repairs) · gandalf (conductor)
**Principles applied:** REVIEW_PROCESS #1 (math before code), #4 (the committed record and the oracle source are the truth), #5 (severity matters). Disciplines #11 (empirical inspection over assumption) and #12 (semantic restatement needs explicit framing). ADR-002. Charter KP-176 to KP-179; **KP-178's gate-brief law (a)/(b) binds this gate.**
**Read-only attestation:**
- I read godot only through `git archive b4c1ff3`, into my scratchpad.
- `make_manifest.py` on that copy reproduces `e584477b…` (84 members). Its output is byte-identical to the committed `MANIFEST.json`. The seven graded and instrument FILE pins in the G3 MANIFEST match.
- The engine is at `22cd2288` (the oracle pin). The files I cite have no tracked modification.
- The sealed `[M-POL2]` cell (`ad61ad2a…`) was hash-checked and read by key only (K-7).
- All Godot and oracle runs used the heavy lock, in scratch.
- Two instruments were scratch-only and never touched the graded copy:
  - a copy of the G3 port tool with one added `print`;
  - a wrapper that `exec`s the unchanged G3 oracle tool with a read-only hook on `ChannelPolicyFold.observe`. The traces it produced are byte-identical to the filed traces, so the hook perturbed nothing.
- **Disclosure, bearing on law (c), which I did not do:** to learn whether WARN-1 would surface at attempt 2, I read `TA-X-08`'s identity-2 operands and the control-fold counters on 15 port-generator cells in scratch (M-POL-2, M0, W1 × salts 0–4). I read no other row off a candidate cell.
- This file is the only thing I wrote to any repo.

---

## Per-item verdicts

| # | item | verdict |
|---|---|---|
| 1 | `TA-X-08` (`0e37db9`): lethal tick censused ALIVE | **PASS.** Not a hollow green: D equals the oracle's own `_player_rows` count on all 25 dying cells, re-derived independently. *(The row's own identity 2 has a separate defect: WARN-1)* |
| 2 | PRE_FIGHT (`3482aef`) | **PASS.** One per wave played. Census equal on G3, 25/25 |
| 3 | P-2 (`4b019e6`) | **PASS** (INFO-2, INFO-3). A real stream-disjointness test now |
| 4 | Emission + harness-written verdict file (`a8512c4`); `TA-X-21` re-citation | **PASS** (INFO-4, INFO-5). The old citations were stale, and the new ones are right |
| 5 | G3 25/25 at `e584477b`, census = oracle's | **PASS. I re-ran all 25 cells (not only a sample): traces and summaries are byte-identical, 25/25** |
| 6 | Fight unmoved; (L2) of record stands | **PASS.** (L2) operands byte-identical to KP-173; deaths unchanged 25/25. G2 rests on drax's run (INFO-A carried) |
| 7 | KP-178 law (a) | **`TA-X-16` FAILS, as known (PENDING-Q96). ⛔ `TA-X-08` identity 2 ALSO FAILS (19/25): a NEW prereg defect, HALT** |
| 8 | KP-178 law (b) | Every row reading the census, D, PRE_FIGHT or the death tick was re-opened. **No further defect** beyond WARN-1 (INFO-6 notes one thin margin) |

---

## What I found

### Item 1 · `TA-X-08`: the lethal tick is censused ALIVE. PASS, and not hollow

**The mechanism matches the oracle.**
- `_census` now classifies the tick with `player_hp <= 0` by its own channel and motion verdicts.
- `DEAD` is reachable only for a tick censused after the lethal one, and the loop breaks before any exists (`kc2rt_fight.gd`, `_lethal_tick_censused`).
- That is the convention at `run.py:4937-4938` (`player_dead_tick = ledger_player[-1][0]`) together with `actor_state.py:252` (`alive = … rt <= player_dead_tick`). It is exactly the repair WARN-1 of my grade Gate-2 asked for. The "drop the tick" rival is refused.

**D against the oracle's own count, on dying cells.** All 25 G3 cells die. I checked D three independent ways:
1. **The G3 oracle tool** calls the oracle's own `actor_state._player_rows`. It passes `ring_ledger` (whose `"player_rows"` is `ledger_player`, `run.py:4803`) and `player_dead_tick` derived exactly as `run.py:4937` derives it. It is not a re-implementation.
2. **My own re-classification** from the raw per-tick path and channel tracks in each filed trace: first tick of each wave → PRE_FIGHT; otherwise channel × moved.
3. **The port's census.**

**All three agree state by state on 25/25.** The lethal tick has `hp = 0.0` on every cell and is classified alive. On five cells the lethal tick is non-channelling (e.g. M-POL-2 s3, W1 s0), so both branches of identity 2 are exercised on the lethal tick.

**The controls fail for the right reasons** (re-run by me: T8 GREEN, its three negative controls RED):

| control | why it is refused |
|---|---|
| (1) DEAD convention | fails the identities |
| (2) drop-the-tick | fails the oracle's one-row-per-tick predicate (`observed == len(hp_trace)`, and `hp_trace` is appended every tick after `_census`), not the identities, which it would close |
| (3) PRE_FIGHT = 0 | fails PRE_FIGHT == waves played |

The controls mutate the emitted census rather than run rival code. The commit records a fail-first run on the real parent tree (RED 3/6), which covers that gap.

### Item 2 · PRE_FIGHT: PASS

- Each wave's first censused tick is PRE_FIGHT, outside D, and outside `n_channelling` and `n_released`. This matches `actor_state.py:252-262` with `:158-159`, where each wave's first row is `spawned=False`.
- On G3, PF equals the waves played on 25/25 (e.g. 6 for a w156 death, 1 for w151), and the census is equal to the oracle's on 25/25.
- The `n_released` back-out (`n_released = _n_released_at_tick`) **never fires** on any of the 25 reference realisations or the 15 port-generator cells I ran: every wave-first tick is channelling (checked on all 25 oracle traces). Its population question goes into WARN-1.

### Item 3 · P-2: PASS. A real stream-disjointness test now

All of gamora's four requirements and INFO-5 are met, and I re-ran the probe (GREEN):
- **The fold is real.** `p2_noop` is forked by `fork_stream` (V9-LAW-1) first in `_open_run_streams`, ahead of the alert, control, summons and channel forks. It is invoked every tick ahead of the channel fold's tick: 209 invocations = 209 ticks.
- **The zero is measured.** `own_draws` on the stream object reads 0; it is not a literal.
- **One digest function.** `cell_digest` drops zero-draw sites globally on both legs, so a registered site with no draws and an absent site hash the same. The digest's subject (terminal, `state_counts`, board counters, draw counts) is unchanged from attempt 1's `_digest_of`; only the zero rule moved.
- **The controls RED by their own clauses:**
  - (a) NOT RUN (own draws 1), and the digest differs;
  - (a0) RED on the digest alone, with own draws 0;
  - (b) RED on the draw-count term;
  - (c) the attempt-1 law reproduces the false RED.
- **A fresh pack per leg.** Graded cells carry no fold key and no `V9-NOOP-P2` site.
- **Inertness is structural.** Only `ctx.p2_noop` sets `p2_noop_inserted`.

**It is not hollow.** This is the object v1.8 § B.3 names: a zero-draw fold inserted into the fight's fold chain. See INFO-2 and INFO-3 for its limits.

### Item 4 · Emission completeness and the harness-written verdict file: PASS

- **In the emission.** The harness computes `ta_x_09`, `ta_x_20`, `ta_x_21`, `ta_x_27_b` and `ta_x_29_b_c_d` in-run and writes them into `ta_manifest.json` (`kc2rt_ta.gd:529-533`), alongside `runtime_digest_boot` and `runtime_header`. Nothing points into `tmp/`.
- **The verdict file.** `_write_verdict_file` writes `ta_verdict.json` with every § G.3 field: `verdict: null`, `runtime_digest` at boot and end with `unchanged_through_the_run`, `runtime_header`, `cross_pin_verified`, `set_digests`, `declared_ungradeable` = exactly `TA-X-06`, H-9/H-10, `port_holes_*`, `hole_closure: "PENDING (H-5)"`, and `ta_manifest_sha256`.
- **My probe re-run (E): 25/26 GREEN.** The one RED is `runtime_header`, because my scratch copy has no exported `.app`. That is the environment, not the code (INFO-5).
- **`TA-X-21` re-citation, verified at engine `22cd2288`** (`threat.py` last changed `4a6dcdda`):
  - The four `round(` sites in the file are exactly 1561 (swing cadence), 1681 (first-cast `delay_s`), 1714 (slot cooldown) and 2052 (DoT expiry). Each label matches its line.
  - The old lines carry no `round(`: 1451 is a comment, 1571 and 1604 are docstring prose, 1916 is an `if`.
  - **The old citations were stale; the new ones are right.** No prereg version pins these line numbers (grep), so the change is citation-only.
  - The probe's stale-citation control REDs.

### Item 5 · G3 25/25 at `e584477b`: PASS, re-run in full

I ran all 25 cells under the heavy lock (≈25 s each; the oracle tool runs, then the port tool), on a `git archive` copy whose tree digest is `e584477b`:
- every oracle trace's sha256 equals the MANIFEST's `uncompressed_sha256`;
- every port summary is **byte-identical** to the filed one;
- census EQUAL on 25/25, 0 decision divergences, 0 draw mismatches, deaths equal.

Re-derived from the evidence itself:
- MANIFEST `78bbcc8d…`;
- the filed traces minus `census_player` are identical to KP-173's, 25/25;
- death (wave, k) equals KP-173's, 25/25.

### Item 6 · The fight is unmoved: PASS

- `l2_operands_25cell.jsonl` is **byte-identical** between KP-173 and KP-177 (sha256 `b5bcdb7b…`). **My (L2) evaluation of record (collab `c210b1979`) stands for `e584477b`.**
- Death waves and ticks are unchanged.
- My 15 port-generator cells reproduce attempt 1's terminal waves. Their state counts differ from attempt 1's only by the repairs' reclassification: the DEAD tick goes to a live state, and wave-first ticks go to PRE_FIGHT. Observed totals are unchanged, and `n_released` is unchanged.
- **G2 705/705** still rests on drax's run. INFO-A from my delta Gate-2 is carried: the oracle packet log is not in the repo.

---

## Item 7 · KP-178 law (a): does the ORACLE pass every EXACT row on its graded arms and window?

**Method.** The reference is the oracle's own five arms × five salts, leg A: the 25 G3 oracle traces (filed, and re-produced by me byte-identically), plus the oracle source at `22cd2288`.
- Where a row's statistic is an outcome, I measured it on the traces.
- Where a row's statistic is a mechanism the oracle lacks under `ORACLE`, or a value derived from the oracle, I cite the source.
- No port outcome enters this audit, so there is no forking-paths concern.

| row | oracle on its graded arms/window | basis |
|---|---|---|
| `TA-X-01` | **PASS** | The oracle is deterministic: 25/25 traces re-produced byte-identically |
| `TA-X-02` | **PASS** (structural) | A property of the port's census mapping of the 89 oracle census ids; no outcome |
| `TA-X-03` | **PASS 5/5** | `M-POL-2-NULL` ≡ `M0`, full traces equal (streams included) |
| `TA-X-04` | **PASS 5/5** | `W1-NULL` ≡ `M-POL-2`, full traces equal |
| `TA-X-05` | **PASS** (5/5 distinct) | Terminal waves differ on every salt |
| `TA-X-07` | **PASS** (structural) | A per-packet booking closure: the census proves every site terminates in one of the seven buckets on any realisation. (c)/(L2): the reference cells run ≤ 1,168 ticks, inside the port's own longest passing cell (2,013 ticks; worst margin ×27.85) |
| **`TA-X-08`** | **⛔ identity 1 PASS 25/25; identity 2 FAILS 19/25** | **WARN-1 below** |
| `TA-X-09` | **PASS** (no run) | The nine vectors are the oracle's `math_rules`; ROWSET reproduces |
| `TA-X-10` | **PASS** | W1: max body radius 43.405 m and max spawn radius 43.588 m, both ≤ 43.758 m; H-9 |
| `TA-X-11` | **PASS** | H-9 (oracle containment, the five documents FILE-hash to the prereg pins) |
| `TA-X-12` | **PASS** (by absence) | There are no pools under `ORACLE` (DIV-19 is PLAY-only), and no pool damage tag appears in any oracle event |
| `TA-X-13` | **PASS** (structural) | `CritLimb` LO in V0 (`player_offense.py:140`) |
| `TA-X-14` | **PASS** (structural) | The oracle's release causes are Type A and Type B only; energy ends the run (V15-11) |
| `TA-X-15` | **PASS** | (a) on every wave played, p01–p04 at 0.0 s and p05 a single time at 4.0 s (tick 49), 25/25; (b) green by construction |
| **`TA-X-16`** | **FAILS 25/25 (known; PENDING-Q96)** | Distinct (wave, point) pairs over the waves played are 5 / 10 / 23 / 28, never 47. Per wave they match `V11-P06-1`'s prefix `[5,5,5,4,4,5]`, with no p06 |
| `TA-X-17` | **PASS** | Max ‖spawn − anchor‖ is 7.9565 m. By law ρ = 8·u₂ < 8 (`spawn_structure.py:330-331`; the incumbent box is not the arm) |
| `TA-X-18` | **PASS** | The expected value is the oracle's `SpawnStructureFold.offset` (v1.10 § A.5) |
| `TA-X-19` | **PASS-vacuous** | No arrival limb |
| `TA-X-20` | **PASS** (structural) | The oracle's hit predicate (census D7) |
| `TA-X-21` | **PASS** | The oracle's four `round(` are Python 3 half-to-even; the bare-`round(` clause is port-side |
| `TA-X-22` | **PASS** (structural) | There is no `interrupts_channel_flag` cause under `ORACLE` (V0; V18+V19) |
| `TA-X-24` | **PASS** (structural) | V0 attack phase is `ENGAGE` |
| `TA-X-25` | **PASS** (structural) | (a) the refusal rule is PLAY-only; (b) an identity; (c) POOL-466, SWING-456 and NONSWING-10 are defined by the oracle's own roll population and `can_swing`; the set digests reproduce |
| `TA-X-26` | **PASS** (no run) | Derived from `P-i` by script |
| `TA-X-27` | **PASS** | (b) the oracle is CPython; (c) 0 draw mismatches 25/25; (a), (d) scan and pack |
| `TA-X-28` | **PASS** (structural) | The oracle has no leech cap (DB-exhaustive absence) |
| `TA-X-29` | **PASS** | (e) the expected values are the oracle's own walk (643/643 bitwise, KP-175) |
| `TA-X-30` | **PASS** (structural) | The halt is the oracle's law at `d_engage_m` = 2.4 |

**Result:** two rows fail on the oracle. `TA-X-16` is known and is carried as PENDING-Q96. **`TA-X-08` identity 2 is NEW.** Every other EXACT row passes.

### ⚠ WARN-1 · ⛔ HALT: `TA-X-08` identity 2 is not satisfiable by the oracle on its graded arms

**The row.** v1.1 § C.1 (carried unchanged to v1.12) states `n_channelling + n_released = D`, "∴ uptime + n_released/D = 1". There, `n_channelling` is the census's CHANNELLING + CHANNELLING_AND_MOVING on D (the seal's uptime × D: 0.904059 × 1,084 = 980). `n_released` is the channel fold's `n_ticks_released` (sealed 104, which the same section asks the runtime to emit). Verified on the seal: 980 + 104 = 1,084.

**What changed underneath it.** The seal had no native control fold. Its own two-instrument identity carries a separate term, `n_control_suppressed`, which read 0 on all five sealed salts. Since v3.7 (KP-147) the oracle runs `ControlApplicationFold` natively:
- `run.py:2811-2815`: `circle_channel_active = not _cc["channel"] and not _channel_broken`, so a control-suppressed tick is **non-channelling in the census**;
- `channel_policy.py:386-388`: `observe(already_suppressed=True)` returns without touching the fold's verdict, so the tick is **not a fold release**.

The tick therefore lands in D but in neither `n_channelling` nor `n_released`.

**Measured on the oracle itself**, using the read-only `observe` hook; the traces it produced are byte-identical to the filed ones:

| cell | census CH | fold released | CH + rel | D | short by | control-suppressed ticks with the fold still channelling |
|---|---:|---:|---:|---:|---:|---:|
| M-POL-2 s0 | 954 | 104 | 1,058 | 1,062 | **4** | 4 |
| M-POL-2 s1 | 239 | 32 | 271 | 273 | **2** | 2 |
| W1 s4 | 830 | 94 | 924 | 926 | **2** | 2 |
| M-POL-2-NULL s0 | 928 | 0 | 928 | 931 | **3** | 3 |
| W1 s0 | 1,006 | 107 | 1,113 | 1,113 | 0 | 0 |

**All 25 cells.** The port is decision-identical to the oracle on the oracle's draws, and its `n_released` equals the oracle fold's count on all five cells above. So I read identity 2 off the port's G3 runs too:

| arm | salt 0 | 1 | 2 | 3 | 4 |
|---|---:|---:|---:|---:|---:|
| M0 | −3 | 0 | −5 | −1 | −5 |
| M-POL-2-NULL | −3 | 0 | −5 | −1 | −5 |
| M-POL-2 | −4 | −2 | −2 | 0 | −1 |
| W1-NULL | −4 | −2 | −2 | 0 | −1 |
| W1 | 0 | −2 | −2 | 0 | −2 |

- **19 of 25 cells fail.** On every cell the shortfall equals the trace's count of control `channel` entries on leg A.
- Identity 1 (`observed = D + PRE_FIGHT`) holds 25/25.
- **A fully faithful implementation fails identity 2 on 19/25 reference realisations.**

**Why attempt 2 would not show it.** On the port's own generator, the control fold applies 0–4 times per cell, but every application is resisted to zero:
- M-POL-2 s1: 3, M0 s0: 4, W1 s1: 2 applications;
- 0 insertions in 15 cells. On G3, 38 of 63 applications insert.

So attempt 2's cells have no control-suppressed tick, identity 2 closes 25/25, and **`TA-X-08` would grade GREEN on a realisation that never exercises the case the row mis-states.** The defect does not make attempt 2 STRUCTURAL. It makes a PASS rest on a row the oracle fails. That is the TA-X-16 shape seen from the other side: there the row rewards infidelity; here it is blind to a path the candidate never reached.

**A second, latent population question in the same identity.** The oracle's `n_ticks_released` counts every observe tick, PRE_FIGHT included (`duty_on_observed` in `gamora_kc2_mpol2_channel_policy_2026_08_25.py:703-704`). The port's back-out puts `n_released` on D. They differ only if a wave's first tick is released, which happens on 0 of 25 reference cells and on 0 of 15 port cells. v1.13 should state which population `n_released` counts.

**This is a prereg defect, not a repair defect.**
- drax's repair is correct and is the oracle's convention.
- The row's text predates the control fold. The regime change (KP-147 made control-suppressed channel ticks reachable) is exactly law (b)'s trigger.
- No gate re-opened `TA-X-08` at KP-147, including mine.
- Restating an EXACT row after a graded run is Matt's (KP-137; v1.8 § F.2d).
- Attempt 1 is unaffected: it is `STRUCTURAL` on the DEAD-tick defect regardless.

**For Matt, as a question (the conductor numbers it):** restate `TA-X-08` identity 2 for the control fold in v1.13. Options:
- **(i) My lean.** Use the seal's own two-instrument form: `n_channelling + n_released + n_control_suppressed_channelling = D`. The port must emit the new counter, which is a port change and so needs a G3 re-run and a delta gate. The expected per-cell values are the table above, which lets the reference-satisfiability audit be checked before commit.
- **(ii)** Define `n_released` as every non-channelling tick on D. That closes the row by tautology and tests nothing. Not recommended.

Either way, v1.13 must state `n_released`'s population (observe ticks or D).

---

## Item 8 · KP-178 law (b): rows reading a state these repairs made reachable or changed

| row | reads | re-opened against the oracle | result |
|---|---|---|---|
| `TA-X-08` | census, D, PRE_FIGHT, death tick | `actor_state._player_rows`; 25 traces; seal | repair **PASS**; identity 2 → **WARN-1** |
| `TA-X-01`, `03`, `04`, `05` · P-2 | digest = terminal + `state_counts` (census) + board + draw counts; the zero rule changed | oracle relations on traces | **PASS.** The census convention applies to both legs alike. Zero = absent can only add equalities, and the raw relations already held, so 03/04 cannot newly fail. 05 is distinct on 5/5 on both realisations (INFO-3) |
| `TA-X-07` | the death tick (post-death packets `dropped`, KP-169) | unchanged; (L2) operands identical | **PASS** |
| `TA-X-15(a)` | could death truncate p05? | reads the board's release schedule, not realised spawns; reference deaths at k ≥ 54 > 49 | **PASS** (INFO-6) |
| `TA-X-16` | terminal wave | — | **PENDING-Q96** |
| `TA-X-25(b)(c)` | bodies spawned before death | identity and membership are robust to truncation | **PASS** |
| `TA-X-14`, `22` | release causes (not `n_released`) | — | **unaffected** |
| `TA-B-02…09` (diagnostic) | D | now on the oracle's convention (my INFO-4, discharged) | not graded |

---

## INFO

- **INFO-1 · `TA-X-16` emission items from my grade Gate-2 remain open.**
  - The per-cell `n_spawn_point_6_keys_rolled` and the per-cell, per-wave filtered-key counter (INFO-2 there) are not emitted. That is correct to wait for v1.13.
  - The stale prose (INFO-3 there) is **still present** at `kc2rt_roster.gd:1942` ("the port read the default and spawned p06 on seven waves"). Remove it in the v1.13 emission pass.
- **INFO-2 · P-2's controls all change a draw count.** None shows the digest's outcome terms (terminal, `state_counts`, board counters) detecting a perturbation of stream *state* at equal counts. In practice such a perturbation moves the census; but a control (d) that reseeds a live stream without changing its count would prove it. This is optional and does not gate.
- **INFO-3 · INFO-5's ordering cannot fail here, by construction.** `fork_stream` seeds from its `seed_in` alone (`kc2rt_rng.gd:314-326`), so no fork-index dependence exists to expose. "Forked first" is satisfied and inert. **v1.13 must print the digest law (zero-draw = absent) for `TA-X-01` and `TA-X-03…05` as well as P-2**, because one function now serves all of them. Under Discipline #12 that is an operational reading, not a criterion change.
- **INFO-4 · The verdict file must be hash-pinned at filing.** `ta_verdict.json` carries `ta_manifest_sha256`, but nothing pins the verdict file itself until drax's evidence MANIFEST does. Attempt-2 filing must list both `ta_manifest.json` and `ta_verdict.json` in the evidence MANIFEST.
- **INFO-5 · `runtime_header` depends on an untracked local binary.** It runs `desktop/KC2Play/build/…/KC2Play` (git-ignored, built 07:26). Its identity rests on the in-run self-checks `equals_P4` and `vendored_runtime_equals_runtime_digest`. Both must read `true` in attempt 2's verdict file.
- **INFO-6 · `TA-X-15(a)` has a thin margin on the reference.** The earliest reference death is k = 54, against the p05 tick of 49. The row reads the schedule, so it is safe; the margin is noted in case a future row reads realised spawns.
- **INFO-7 · My earlier commitment is superseded.** My grade Gate-2 said I would run a full 28-row dry read regardless of brief. KP-178 routed law (c) to Matt (Q96 part 3), and this brief forbids it. I complied; the disclosure above lists exactly what I read off port-generator cells, which is one row. WARN-1 is the case for (c): the defect is invisible on the candidate's realisation and visible only on the reference.

---

## Verdict

**The repairs: PASS-WITH-WARN** (0 BLOCK · 1 WARN · 7 INFO). drax's four repairs are correct, faithful to the oracle, not hollow, and the fight is unmoved. **⛔ HALT TO MATT** on WARN-1, in addition to Q96.

## Conditions for attempt 2 (all must hold)

1. **Matt rules Q96** (`TA-X-16` per-wave restatement; the budget; law (c)).
2. **Matt rules WARN-1** (`TA-X-08` identity 2 under the native control fold, and `n_released`'s population).
3. **v1.13 lands and folds in:**
   - the `TA-X-16` restatement;
   - the `TA-X-08` restatement;
   - the P-2 operational reading and the digest law for `TA-X-01`/`03…05` (INFO-3);
   - the census convention (lethal tick alive, PRE_FIGHT per wave).

   **Before v1.13 is committed, both restated rows are checked against the 25 reference traces** (law (a)), and v1.13's own once-per-version law (a) audit is run.
4. **If the restatement adds a counter, the port change gets a delta gate:**
   - the emitted `n_control_suppressed_channelling` (option (i)) and the `TA-X-16` per-cell counters (INFO-1);
   - a new MANIFEST, re-pins, a G3 re-run, and gamora or me confirming the (L2) operands are unchanged;
   - a delta Gate-2.
5. **At filing:** the evidence MANIFEST pins `ta_manifest.json` and `ta_verdict.json` (INFO-4). `runtime_header` reads `equals_P4` and `vendored_runtime_equals_runtime_digest` both `true` (INFO-5). The stale note is removed (INFO-1).
6. H-5 (hole closure) remains seal-blocking, and H-8 (Matt's T-C) remains a seal condition. Both are unchanged.

## Rationale

- KP-178 law (a)/(b), which binds this gate: "any other row the oracle cannot pass is a new prereg defect and a HALT to Matt."
- v1.1 § C.1 (the identities); the seal's `two_instrument_identity`.
- `run.py:2811-2815`, `channel_policy.py:361-392`, `actor_state.py:149-173`, `:234-262`.
- REVIEW_PROCESS #4 (oracle source over ledger summary). Discipline #11: the seal's arithmetic held, and only running the oracle with control native exposed the gap. Discipline #12: the restatement is semantic. ADR-002: row restatement after a graded run escalates to Matt.

## Action

- [ ] **gandalf:** route WARN-1 to Matt as a new HALT question, or fold it into Q96 at the conductor's discretion. Record "the repairs pass" against KP-179.
- [ ] **Matt:** rule WARN-1 (lean: option (i)) alongside Q96.
- [ ] **gamora (v1.13, on Matt's word):** restate `TA-X-08` identity 2 and `TA-X-16`. Verify both on the 25 G3 traces before commit (the expected control counts are in WARN-1's table). Print the digest law and the census convention.
- [ ] **drax (after v1.13):** emit the counter v1.13 names; remove `kc2rt_roster.gd:1942`'s stale note; have the filing MANIFEST pin both harness files. Then a delta Gate-2.

## References

- Godot `b4c1ff3` (archive): `kc2_runtime/sim/kc2rt_fight.gd` (`_census`, `_open_run_streams`, `_p2_noop_tick`, `_channel_verdict`, `:1715-1731`); `sim/kc2rt_rng.gd:314-326`; `sim/kc2rt_control.gd:296-449`; `sim/kc2rt_quant.gd`; `sim/kc2rt_roster.gd:1938-1942`; `tests/kc2rt_ta_emit.gd` (`run_cell`, `cell_digest`, `p2_probe`); `tests/kc2rt_ta.gd:500-700`; `tests/kc2rt_attempt2_probes.gd`; `tools/kc2rt_g3_oracle_trace.py`, `kc2rt_g3_loop_trace.gd`
- Evidence: `evidence/kc2-play/2026-10-01-g3-25cell-kp177/` (MANIFEST `78bbcc8d…`), `…-kp173/`, `2026-10-01-ta-attempt1-v1.12-cells/`
- Oracle (engine `22cd2288`): `simulation/kc2/run.py:2325-2336`, `:2795-2815`, `:4803`, `:4925-4939`; `channel_policy.py:361-392`; `actor_state.py:149-173`, `:234-262`; `threat.py:1561`, `:1681`, `:1714`, `:2052`; `spawn_structure.py:309-334`; `player_offense.py:140`; `scripts/gamora_kc2_mpol2_channel_policy_2026_08_25.py:250-269`, `:695-704`
- Sealed: `kc2-checkpoint-E-s09-cp150-mpol2-20260825_114420.json` (`ad61ad2a…`; `⚑ two_instrument_identity`, read by key)
- Prereg: v1.12 (§ B.1a, § F.2, § G); v1.8 § B.3, § F.2–F.2i; v1.1 § C.1
- Charter KP-176 to KP-179; my prior findings `2026-10-01-kc2-play-attempt1-v1.12-grade-gate2.md`, `2026-10-01-kc2-play-repair-gate2.md`; gamora's grade collab `d2fe958ec`
