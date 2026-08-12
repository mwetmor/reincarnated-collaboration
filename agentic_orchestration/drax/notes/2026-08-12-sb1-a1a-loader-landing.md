# SB-1 Cell A1a — LOADER LANDING (drax)

> **Authority:** drax, SB1-CELL-A1a. **Filed verbatim from the cell return by the conductor** (gandalf, `RUN-CONDUCTOR`) — capture-by-conductor per the Pattern-A-deep precedent; the report's authority is drax-authored. Cell ran 2026-08-12; godot repo commits `4c6dcc5..28ea1ba`, local only, nothing pushed.

---

**Scope executed:** the loader only. No `.tscn`, no dress, no camera, no capture, no frame written. PL-5's floor check has no domain this cell and that is declared, not skipped. Godot repo HEAD at cell start `978a423b` (matches ledger L-0 pin); local commits only, **nothing pushed**.

## 1 · Commits (CL-2, commit-per-item)

| hash | item |
|---|---|
| `4c6dcc5` | **1a** — `scripts/kc2_baton.gd`, the loader |
| `227b6ce` | **1b** — `scripts/kc2_loader_smoke.gd` + the census + derived artifacts + one `.gitignore` stanza |
| `11557b1` | **2** — `scripts/kc2_loader_diff.py`, the differential |
| `4318b97` | **3** — `scripts/kc2_placement_smoke.gd` |
| `befbd8c` | **1c** — `scripts/kc2_fg13_falsify.gd`, FL-3 falsification |
| `28ea1ba` | AGENT_STATE checkpoint |

Change-set is exactly 11 paths: the five scripts, `.gitignore`, `AGENT_STATE.md`, and four `tmp/kc2/` artifacts. `project.godot` not touched. The WR2 stack (`wr2_playback.gd`, `wr2_actor_rig.gd`, `replica_trace.gd`) left unmodified and un-forked — the KC2 baton is knot-sparse with non-uniform per-leg speed, so it got a new bracketing function rather than a reuse of WR2's dense-frame lerp.

## 2 · Differential vs `reincarnated-engine/src/reincarnated/export/baton_v1_stub_consumer.py`

**22 rows, 22 EXACT-MATCH, 0 DELTA.** Stub's own coverage run beside it: 23/23 MUST, 33/33 total, GREEN.

| check | stub | godot | verdict |
|---|---|---|---|
| actor count | 344 | 344 | EXACT-MATCH |
| path knot count | 1003 | 1003 | EXACT-MATCH |
| wave count | 20 | 20 | EXACT-MATCH |
| event row count | 1900 | 1900 | EXACT-MATCH |
| `tick_period_s` (wire constant) | 0.0816326530612245 | 0.0816326530612245 | EXACT-MATCH |
| per-actor terminal tick (344 values) | 344 values | 344 values | EXACT-MATCH (344/344 identical) |
| board entry == `path[0].run_tick + 1` | wire | `test_from_tick` | EXACT-MATCH (344/344; stub has no such field — diffed against the wire) |
| spawn positions (344 × 2) | — | max \|Δ\| 0.000e+00 | EXACT-MATCH |
| **position function, every (actor, tick)** | **32,375 samples** | **max \|Δ\| 4.974e-13 m** | **EXACT-MATCH (0 above the 1e-9 m bar)** |
| UNDEFINED outside the closed span (GL-7) | None outside `[path[0], path[-1]]` | no sample emitted outside the span | EXACT-MATCH (344 actors, both ends) |
| event census by type (7 types) | see § 3 | see § 3 | EXACT-MATCH |
| census closes: consumed + binned == rows | 1900 | 1556 + 344 = 1900 | EXACT-MATCH |
| scatter shape word (positional token 1) | BOX | BOX | EXACT-MATCH |
| inside the declared BOX | 342 | 342 | EXACT-MATCH |
| outside the BOX (DIV-P01-TIER) | `['w162_a001','w163_a004']` | `['w162_a001','w163_a004']` | EXACT-MATCH |
| a DISC would misplace (counterfactual) | 72 | 72 | EXACT-MATCH |
| `path[0]`-inside-the-active-disc class | 6 ids | same 6 ids | EXACT-MATCH |
| *[stub self-audit]* suppressed `path[0]` tests: report vs recomputed | 61 | 61 | EXACT-MATCH — **both columns stub-side** |
| actors hit-testable at their own `path[0]` | 0 | 0 | EXACT-MATCH |
| dwell pairs (unfiltered) | 17 | 17 | EXACT-MATCH |
| track sample counts | 3732 ×4 | 3732 ×4 | EXACT-MATCH |
| FG-17 engine tree unchanged | 2789 porcelain lines | 2789 porcelain lines | EXACT-MATCH |

Two rows are labelled rather than blurred, because a gatekeeper should not have to discover it: the *[stub self-audit]* row has **both columns stub-side** — the stub's printed evidence string against the same quantity recomputed from its `Scene` object (CL-3). Its 61 is a **different quantity** from the 6-body class: 61 counts every `path[0]` tick that would have been *tested*; 6 counts only those that would have read as *hits*. The disc-counterfactual row is reported by the godot side and drawn by neither.

The two loaders reach GL-8 by different routes: the stub suppresses `path[0]` tests **conditionally**, on reading the `path_coverage` declaration; this loader **cannot test there at all**, because `test_from_tick` is a separate field fixed at `path[0]+1` when the actor table is built.

## 3 · FG-13 event need-list census

Vocabulary derived from `events.rows[].event_type` — the artifact's own column, not a registry lookup. Machine-readable at `reincarnated-godot/tmp/kc2/kc2_event_census.json`.

| event_type | disposition | sink / bin | count |
|---|---|---|---|
| `wave_start` | CONSUMED | `wave_phase.open` | 20 |
| `channel_start` | CONSUMED | `channel_segment.open` | 20 |
| `spawn` | **BINNED** | `BIN-ROSTER-CROSSCHECK` | 344 |
| `damage_dealt` | CONSUMED | `damage_arriving` | 1132 |
| `death` | CONSUMED | `death_phase` | 344 |
| `channel_release` | CONSUMED | `channel_segment.release` | 20 |
| `wave_end` | CONSUMED | `wave_phase.close` | 20 |
| **TOTAL** | | | **1900** |

**1,556 consumed + 344 binned = 1,900. Uncovered needs: 0.** The `spawn` bin is named and its reason is on the record: roster identity is cross-checked against the actor table (344/344 resolve), and the row's `run_tick` is **REFUSED** as a board-entry time per GL-8 + NOTE-2.

Nothing is pre-registered for a consumer that does not exist. The four event types the reference stub branches on and this wire never emits (`dot_tick`, `heal_tick`, `player_death`, `channel_expiry`) are recorded as a declared absence, not as registry rows — pre-registering them would blunt FG-13's own falsification test.

## 4 · Placement smoke — 10 assertions, 0 FAIL

Bare `Node3D` markers in an empty scene: no mesh, no material, no camera, no light, no viewport read.

| assertion | result | evidence |
|---|---|---|
| 344 markers instantiated into the tree | PASS | 344 children, 0 placement refusals |
| shape word from the wire is BOX | PASS | `scatter_model` token 1 = BOX, half-extent 8.0 m (typed) |
| 342 markers inside the BOX at h = 8.0 m | PASS | 342 |
| exactly 2 outside = the DIV-P01-TIER pair | PASS | `["w162_a001", "w163_a004"]` |
| crossers placed IN PLACE, not clamped | PASS | 0 of 2 moved (bar 1e-5 m, the float32 transform floor) |
| no disc is drawn for scatter anywhere | PASS | an 8 m circle would place 72 of 344 wrong |
| board-boundary false-positive class = 6 | PASS | `w153_a023, w156_a012, w156_a015, w161_a014, w162_a012, w167_a017` |
| none of the 6 is ON THE BOARD at `path[0]` | PASS | 0 of 6 at `path[0]`; 6 of 6 at `path[0]+1` |
| all 6 DRAWABLE at `path[0]` | PASS | 6 of 6 — GL-8 removes the TEST, not the body |
| no actor hit-testable at its own `path[0]` | PASS | 0 of 344 |

## 5 · Loader smoke and falsification

**26 checks, 0 FAIL** (committed transcript for the placement run at `tmp/kc2/kc2_placement_smoke.txt`). Includes: digest MATCH before load; 344/20/1003/1900/3732×4; `_integrity` rebuilt from the object (CL-10); 17 dwell pairs unfiltered (12 ≥44 ticks, 5 at Δtick=1); 61 two-knot straight walks; 61 drip bodies at max +306 ticks = 25.0 s, carried not snapped; 7 declared absences.

**Falsification, 3 checks, 0 FAIL** — the gates proven able to go red, not merely green:
- **CONTROL** — the pinned baton loads GREEN.
- **FG-13** — plant `telegraph_cast`, exactly as the law words its own test → `uncovered=["telegraph_cast"]`, load REFUSED. The mutant's `_integrity` row count is bumped so the census is the only thing that *can* fail.
- **GL-12** — K-4's prohibition half has an empty domain here (0 of 344 pathless), so it was given one: plant a pathless body → `PATHLESS-ACTOR w151_a000`, load REFUSED.
- Digest gate carries two more in the loader smoke: flipped digit → FAIL/`DIGEST-MISMATCH`; no declared digest → `NOT-RUNNABLE`, never green.

Mutants written to this repo's `tmp/`, loaded under their own recomputed sha256, and deleted (2 pruned, directory verified empty). The baton was never touched.

## 6 · Containment

Engine tree porcelain **2,789 lines before and after** the differential, fingerprinted in-process, `sys.dont_write_bytecode` set before the engine import; no `__pycache__` landed. Baton re-verified on disk at `d7ecd866ac45…`. Godot repo porcelain **233 lines**, matching the L-0 pin exactly; the one modified tracked file (`tmp/br2watch/measure/census.json`, mtime Aug 2) is pre-existing baseline, not mine. Re-running all four harnesses at HEAD regenerated the committed artifacts byte-identically (git reports no modification) — an artifact-layer observation, not a G-DET claim.

## 7 · NOTES for the conductor (banked, not ruled)

**NOTE-6 — the defense count has no typed carrier.** `config.encounter.defenses` is a one-member list holding the sentinel `"DEFENSE-COUNT-4-NAMES-NOT-EMITTED"`. The count rides a token inside a string; the list's **length is 1, not 4**. A loader rendering `len(defenses)` renders the wrong number. My loader reads the token positionally and declares the count UNDECLARED if the grammar does not match, rather than defaulting to the length or to zero. Same class as Cell 0's NOTE-5 — typed truth is fine, the carrier is prose. Routing is yours.

**NOTE-7 — 332 of 344 killing blows carry `damage_applied == 0.0`.** Measured: 1,132 `damage_dealt` rows; 332 have `applied == 0.0`, all with `hp_after == 0.0`, and **all 332 coincide with a `death` row at the same (target, tick)**. All 344 deaths have a damage row at their tick; 12 killing blows carry non-zero applied. **The accounting is exact and closes: `sum(damage_applied) == hp_max` for all 344 actors, zero discrepancies.** This is not a wire defect — it is a rendering hazard: a HUD that shows `damage_applied` on the death frame prints **0** on 96.5% of deaths, which are the most visible hits in the watch. My loader carries both magnitudes verbatim with `hp_after` authoritative per the declared semantic, re-derives nothing, and sums nothing. **What to display on a death frame is presentation grammar and I am not ruling it here.**

**NOTE-8 — Godot's vector types are single-precision in this build; GDScript's `float` is a double.** Routing the position function through `Vector2` rounded it to ~1e-6 m and moved the cross-leg-variation count from 282 to 283 of 283 multi-leg bodies — a rounding artefact impersonating a measurement. Fixed: the position function returns doubles, the cast to engine types happens once at the presentation boundary and is named there. **This binds every later cell that computes from positions** (A1b onward): derived numbers in doubles, engine types only at the boundary.

**NOTE-9 — a coverage gate must not assert "6" against the stub's printed number.** The stub's `skipped_pre_live` is 61 (ticks the declaration suppressed); the false-positive class is 6 (the subset that would have read as hits). Both are correct; they are different quantities. Same shape as Cell 0's NOTE-1 recommendation about asserting "12 dwells" instead of "12 dwells ≥44 ticks".

**Self-correction, on the record:** my Cell 0 countersign said "23 of the 283 multi-leg bodies carry measurably different per-leg speeds". Re-measured here: **282 at 1e-6 m/s, 23 at 4 dp of metres-per-tick, 12 at 2 dp.** The 23 is the 4 dp column — the same precision that note printed `w154_a004`'s legs at — so the figure is right and its basis was implicit. The check now carries all three bases and asserts all three, because a bare count there is a claim with a hidden threshold inside it.

## 8 · Where to attack this

Named so the gatekeeper does not have to find them: (a) the position differential compares my emitted 12-dp strings against the stub's doubles — the 4.974e-13 m residual is string round-tripping, not algorithmic divergence, and the bar is 1e-9; (b) `CONSUMED` for `wave_start`/`wave_end`/`channel_*` means the loader builds typed records, not that any of it is yet *rendered* — rendering is A1b; (c) the 2.7 MB position sweep backing the 32,375-sample row is gitignored as a class-D intermediate with its regeneration command, so that row is reproducible but not archived; (d) `damage_dealt`'s sink names `strike()` and the arriving-damage channel, neither of which is wired this cell — the sink is a declared destination, and the census would be dishonest if it claimed otherwise.
