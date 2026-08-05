# BR-2 / TRACE-STAGE-1 — the storm gets a clock, and `duration_s` takes ONE anchor on purpose

**Date:** 2026-08-01 · **Author:** gamora (simulation seam) · **Status:** CURRENT
**Run:** BR-2 (TRUE-SHAPE), cell 1b. **Conductor:** gandalf (`RUN-CONDUCTOR`).
**Charter:** `agentic_orchestration/gandalf/notes/2026-08-01-br2-true-shape-run-charter.md`
ADDENDUM 1 — gates G-1c / G-1d / G-1e.
**Predecessor:** cell 1 TRACE-FILL-1, `agentic_orchestration/gamora/notes/2026-08-01-trace-fill-1.md`
(its §5 raised the gap this cell closes).
**Math note (written BEFORE the code, Discipline #1):**
`~/Games/reincarnated-engine/src/reincarnated/simulation/math/br2-trace-stage-1-2026-08-01.md`
**Engine commit:** `5b8c724b` (pushed; verified on remote — §7).

---

## THE ANSWER, FIRST

**G-1c PASS. G-1d PASS, 18 of 18 gates. G-1e satisfied.** The battery is regenerated and promoted.

**G-1c on the same three limbs cell 1 set, and the control arm is stronger this time — it is the
whole battery, not one seed:**

1. **The control.** At pre-change HEAD, all 200 traces regenerated and compared to the cell-1
   battery: **90,708 records, ZERO simulation field paths differ.** Only `header.engine_git_hash`
   moves (`bce46fd9` → `2a9ebb02`), and `git diff --stat bce46fd9 2a9ebb02` is
   **`AGENT_STATE.md | 54 ++-`, one file, zero code.** So the generator is exactly reproducible and
   the whole post-change delta is attributable to this change alone.
2. **The whole-battery diff.** 200 files, **90,708 records**, record-by-record. **Exactly four
   simulation field paths differ, each n = 1,556** — the census's own telegraph total. **No fifth
   path anywhere.**
3. **The acceptance figures.** Every non-provenance key in the pick artifact is **identical**; the
   scan **re-selects seed 74000909** with byte-identical scalars (`cornering 0.0` ·
   `min_hp_fraction 0.654515444497278` · `intake/pool 0.5740120851987082` ·
   `player_damage_taken 435.6751726658195`). The watch trace's footer is unchanged to the last
   digit: `player / 36.10000000000024 s / 3 of 3 killed`. **200 fights of confirmation that no RNG
   moved.**

**Two things the conductor must rule on before drax's cell opens** — one is a deviation from a
pinned value that I am shipping and arguing for (§1), one is a defect of the same class as the two
this run is already fixing (§6). Both are in this note, neither is buried.

---

## §1 — ⚑ THE DECISION THAT CHANGED WHILE I WAS DERIVING IT, AND ONE PINNED VALUE MOVED

The pin was nova **0.857** · wave **1.4** · blizzard **8.0**, under the definition *"how long the
danger zone is live."* Before writing code I checked whether those three share an anchor.

**They appeared not to.** `active_duration_s 8.0` is anchored at `t_cast`; nova's 0.857 and wave's
1.4 are anchored at `fire_time_s`. I drafted the argument for shipping **6.0** on the blizzard
(first impact to last impact, fire-anchored, uniform) and had the measurement to back it.

**Then I wrote out the engine's own liveness bound and the argument collapsed in the pin's favour.**
All three mechanisms carry an `is_live_over(t0,t1)` predicate gated on `t_expiry` — the test that
decides whether the mechanism can still damage anyone. And:

```
BlizzardEvent.t_expiry   = t_cast + active_duration_s + fall_time_s
telegraph.fire_time_s    = t_cast                     + fall_time_s
t_expiry - fire_time_s   =        active_duration_s              = 8.0   exactly, no residue
```

**The two fall-times cancel. The blizzard's 8.0 IS fire-anchored.** The conductor's pinned value and
a uniform anchor are the same number, which I did not expect.

**DEFINITION SHIPPED:** `duration_s` = `event.t_expiry − fire_time_s`. The danger window is
`[fire_time_s, fire_time_s + duration_s]` **on every family, with no family branch** — the
deliberate opposite of cell 1's `projectile_velocity_ms`, where I had to write *"a consumer MUST
branch on `family`."* One field needing a branch is a documented hazard; two would be a minefield.

### The one deviation: wave ships **1.4874999999999998**, not 1.4

`WaveEvent.t_expiry = t_release + wave_time_s + dwell_s`. The front reaches 16.0 m at
`range_m / v` = **1.4 s exactly**; the **1.0 m-deep** band's trailing edge clears the far end one
`dwell_s` = **0.0875 s** later, and the resolver keeps hitting until then. **1.4875 is the last
instant the wave can deal damage; 1.4 is not.**

Shipped, rather than matching the pin, for three reasons:

1. **1.4 is not lost.** The sweep is `range_m / projectile_velocity_ms` = 1.4, derivable exactly from
   two fields the trace has carried since cell 1. Emitting 1.4 would duplicate an existing
   derivation; **`depth_m` is not in the trace**, so 1.4875 adds information nothing else carries.
2. It preserves the single anchor. Any other choice re-introduces the per-family branch.
3. It is resolver-sourced — the cell-1 discipline, read the expression the resolver reads.

**⚑ AND IT CREATES A TRAP I AM NAMING LOUDLY.** Charter **G-2b grades the SWEEP at 1.4 s ± 0.05**.
`duration_s` is **0.0375 s outside that tolerance**. **A renderer that animates the wave's front from
`duration_s` FAILS G-2b.** The front must come from `projectile_velocity_ms` (which R-BR-24 requires
anyway); `duration_s` answers *when may I stop drawing*. Stated in the source at both the emission
site and the schema, in MIGRATION §3, in two tests, and here.

**One word reverses it to 1.4** — it is a one-line change plus a 7-second regen.

---

## §2 — ⚑ THE BLIZZARD'S 8.0 HAS A 2.0 s DEAD TAIL, PROVEN AND MEASURED

`duration_s = 8.0` is the **liveness** bound and it **over-bounds the last impact by 2.0 s.**

**Proven from the scheduler** (`BlizzardScheduler.cast`): volleys at `t_cast + v*2.0` for
`v ∈ {0,1,2,3}`, impacting `+ fall_time_s`; `resolve_tick` resolves only scheduled drops. So the last
drop lands at `t_cast + 6.8333` = **`fire_t_s + 6.0`**, and no damage can occur after it. `t_expiry`
is a culling bound that guarantees any drop launched inside the active window has landed.

**Measured over the cell-1 battery (R-BR-34 — the probe, not the recollection).** Every `damage`
event whose `attack_id` tail is `:<volley>:<drop>`, offset against its own telegraph's `fire_t_s`,
all 200 traces:

| volley | n | min offset | max offset |
|---|---|---|---|
| 0 | 87 | **0.0000** | **0.0000** |
| 1 | 60 | **2.0000** | **2.0000** |
| 2 | 25 | **4.0000** | **4.0000** |
| 3 | 14 | **6.0000** | **6.0000** |

**186 impacts, zero variance, max exactly 6.0.** Drop-index histogram `{0:34, 1:32, 2:30, 3:32,
4:30, 5:28}` — six drops, indices 0–5.

**RENDERING INSTRUCTION, not a caveat:** drive impacts from `stage_count` / `stage_interval_s`
(impacts at `fire_t_s + k·2.0`, `k = 0..3`); **do not paint lethal area over the final 2.0 s.**

**⚑ The same 186 records kill cell 1's route (a) dead.** Only **156 of 570** blizzard casts produce
any hit at all, and per-volley hit counts fall **87 → 60 → 25 → 14**. Recovering cadence by parsing
`attack_id` would flicker seed-to-seed and vanish entirely on 414 of 570 casts. **Emitting the
cadence was not a convenience; it was the only stable route.**

---

## §3 — WHAT CHANGED AND WHERE

**Seam:** `~/Games/reincarnated-engine/src/reincarnated/simulation/`. Commit `5b8c724b`.

| family | `duration_s` | `stage_count` | `stage_interval_s` | `hit_radius_m` |
|---|---|---|---|---|
| `nova` | **`0.8571428571428571`** | `null` | `null` | `null` |
| `wave` | **`1.4874999999999998`** | `null` | `null` | `null` |
| `blizzard` | **`8.0`** | **`4`** | **`2.0`** | **`1.32`** |

**No literal is written at any emission site.** Every value is `p.<attr>` read off the same params
object the resolver uses. `duration_s` needs one composition on the wave, so rather than put
arithmetic in the emitter I added **one identically-named property to each of the three params
classes** — `live_span_s`, each documented as *"`event.t_expiry − telegraph.fire_time_s` for this
family, by construction"*, each asserted against the **live event object** by a test so the two
cannot drift. Symmetric naming means the next family cannot quietly omit it.

**Emitting the SPAN rather than computing `t_expiry − fire_time_s` per cast is deliberate:** that
subtraction of two large floats would inject per-cast ULP noise into an emitted constant, break a
100 %-at-one-value coverage gate for no benefit, and hand a renderer a jittering number.

**Files touched:**

| file | what |
|---|---|
| `gd_nova.py` | `NovaParams.live_span_s` (new property) |
| `gd_boss_kit.py` | `WaveParams.live_span_s` + `BlizzardParams.live_span_s` (new properties) |
| `spatial_gauntlet/spatial_telemetry.py` | four `Optional` fields on `TelegraphSpec`, both traps declared where a consumer reads them |
| `spatial_gauntlet/spatial_engine.py` | the three cast methods (~6740 nova, ~6930 wave, ~6935 blizzard) |
| `spatial_gauntlet/replica_frame_emitter.py` | **four keys in the enumerated projection** |
| `MIGRATION.md` | new 2026-08-01 TRACE-STAGE-1 entry (8 sections) |
| `math/br2-trace-stage-1-2026-08-01.md` | new |
| `notes/br2_trace_stage_1_gates_2026_08_01.py` | the G-1c/G-1d instruments (new) |
| `tests/test_br2_trace_stage_1.py` | 27 tests (new) |
| `tests/test_br2_trace_fill_1.py` | one test amended, framed (§5.2) |

**⚑ The projection is the trap this seam has already fallen into once.** `replica_frame_emitter`
builds the telegraph record **key by key**, and the comment at :551 in that same file is the record
of `family` being minted upstream, riding the spec correctly, and dying **at that site** — 0 of
13,573 records. Four new spec fields therefore meant four new keys there, and a test asserts each
one. Without it this cell would have shipped a schema nobody could read and every gate would still
have been green at the spec level.

**Not touched, deliberately:** `t_launch_s` and `spoke_offset_rad` stay nova-only; `half_angle_rad`
stays null everywhere; `radius_m` semantics unchanged on all three families (the blizzard's 8.0
scatter stays — `hit_radius_m` is added **beside** it, because the scatter is true and useful and
the defect was never that 8.0 was wrong, only that it was alone); `VALID_FAMILIES` / `VALID_SHAPES`
untouched; `validate()` unchanged.

**Schema version: NO BUMP** (G-1e). Four additive, nullable, `None`-defaulted fields —
`replica-frame/v1` and `g5-replay-trace/v1` both stay v1. Third application of the precedent
`spatial_telemetry.py` states verbatim for `spoke_offset_rad`, `prong_count` and `family`. A test
asserts all four defaults are `None` and that `validate()` still accepts a spec declaring none of
them, so the `melee` and generic emitters remain legal.

---

## §4 — G-1c — THE FULL PATH DIFF

**Instrument:** `simulation/notes/br2_trace_stage_1_gates_2026_08_01.py`, modes `diff` / `battery`.

### 4a. The control arm — pre-change HEAD, WHOLE BATTERY

```
files_compared               200
records_compared             90,708
files_with_unexpected_paths  0
all_differing_paths          header.engine_git_hash  n=200   ('bce46fd9' -> '2a9ebb02')
                             ← that is the COMPLETE list. ZERO simulation paths.
VERDICT                      PASS
```

`git diff --stat bce46fd9 2a9ebb02` → `AGENT_STATE.md | 54 ++-`. **One doc file, zero code.**

### 4b. The watch trace — `boss__FULL__seed74000909.jsonl`

```
n_records                    462  (both sides)
record_order_identical       true
unexpected_simulation_paths  []   ← EMPTY
VERDICT                      PASS
```

| column | path | n | sample (cell-1 → new) |
|---|---|---|---|
| SIMULATION | `event[telegraph].duration_s` | **9** | `<ABSENT> → 8.0` · `<ABSENT> → 0.8571428571428571` · `<ABSENT> → 1.4874999999999998` |
| SIMULATION | `event[telegraph].stage_count` | **9** | `<ABSENT> → 4` · `<ABSENT> → None` |
| SIMULATION | `event[telegraph].stage_interval_s` | **9** | `<ABSENT> → 2.0` · `<ABSENT> → None` |
| SIMULATION | `event[telegraph].hit_radius_m` | **9** | `<ABSENT> → 1.32` · `<ABSENT> → None` |
| PROVENANCE | `header.engine_git_hash` | **1** | `'bce46fd9' → '5b8c724b'` |

`n = 9` on each because the trace carries 9 telegraphs and the **key** is added on all nine — the
three blizzard records carry values, the six others carry `null`. `<ABSENT> → None` is the expected
shape for an ADDED field and is what distinguishes this cell from cell 1 (where the keys already
existed and the samples read `None → 24.0`).

**The provenance column is graded separately and its changing is CORRECT.** Pre-registered in the
math note §5.1 **before** the run, as in cell 1: that field's whole job is to say which code ran, and
reproducing the old hash would be the defect (C-4, jack-ryan Gate-2 2026-07-28).

**Everything else is identical** — all 361 tick blocks, every entity's per-frame
`hp / x_m / y_m / heading_rad / energy / ailments / skill_cooldowns`, all 57 `damage` events, 29
`leech`, 3 `death`, and the footer.

### 4c. The whole battery — all 200 traces

```
files_compared               200
records_compared             90,708
files_with_unexpected_paths  0
unexpected_paths             []
VERDICT                      PASS
```

**Every differing field path over the whole battery, with counts:**

| path | n | reconciliation |
|---|---|---|
| `event[telegraph].duration_s` | **1,556** | = 470 nova + 516 wave + 570 blizzard. Exact. |
| `event[telegraph].stage_count` | **1,556** | key added on every telegraph; 570 valued, 986 null |
| `event[telegraph].stage_interval_s` | **1,556** | same |
| `event[telegraph].hit_radius_m` | **1,556** | same |
| `header.engine_git_hash` | **200** | one header per file. Exact. |

**That is the complete list. No fifth path exists anywhere in 90,708 records.**

### 4d. Outcome + scalar reproduction

| what | cell-1 | cell-1b |
|---|---|---|
| footer | `player / 36.10000000000024 s / 3 of 3 / alive` | **identical** |
| pick artifact (non-provenance keys) | — | **0 differing keys** |
| pick | seed 74000909, cornering 0.0, min-HP 0.654515444497278, intake/pool 0.5740120851987082, damage taken 435.6751726658195 | **identical** |

---

## §5 — G-1d — COVERAGE, AS COUNTS, INCLUDING THE NULL COUNTS

Run against the **promoted** battery. `n_files 200 · n_records 90,708 · n_telegraphs 1,556`.

| field | `nova` (470) | `wave` (516) | `blizzard` (570) |
|---|---|---|---|
| `duration_s` | **470** @ `0.8571428571428571` · 0 null | **516** @ `1.4874999999999998` · 0 null | **570** @ `8.0` · 0 null |
| `stage_count` | 0 non-null · **470 null** | 0 non-null · **516 null** | **570** @ `4` · 0 null |
| `stage_interval_s` | 0 non-null · **470 null** | 0 non-null · **516 null** | **570** @ `2.0` · 0 null |
| `hit_radius_m` | 0 non-null · **470 null** | 0 non-null · **516 null** | **570** @ `1.32` · 0 null |
| `projectile_velocity_ms` *(cell-1 control)* | 470 @ `14.0` | 516 @ `11.428571428571429` | 570 @ `24.0` |
| `prong_count` *(cell-1 control)* | 470 @ `16` | **516 null** | 570 @ `6` |

**`absent_key` is 0 in every cell of that table** — the key reaches the wire on all 1,556 records,
which is the R-WR3-40(2) check. `other_values` is **empty on every gate**: no third value hides in
any family. 470 + 516 + 570 = **1,556**, the census's own total.

**18 of 18 gates PASS** — 6 populated-side, 6 null-side, 6 cell-1 controls.

**The null-side gates are graded with their own evidence**, not inferred from the populated side. A
build that wrote `1` into `stage_count` on the nova would pass every populated-side check in the
file and fail exactly these six.

---

## §6 — ⚑ ONE MORE DEFECT OF THE SAME CLASS, REPORTED AND NOT FIXED

**The wave's rect is drawn 2× too wide at the origin.**

`wave_half_width_m(u)` = `(start_width_m + (end_width_m − start_width_m)·u/distance_m)/2`. The lane
**widens 3.0 → 6.0 m** over its 16.0 m run. The telegraph emits `width_m = end_width_m = 6.0` and the
schema's own comment names it *"the END width"* — but **`start_width_m` 3.0 is not in the trace.** A
renderer drawing a uniform 16.0 × 6.0 rect **overstates the lane at every point before 16.0 m — 2×
at the origin.** Charter **G-2b pins exactly that uniform rect.**

**This is the same defect class as the blizzard's scatter-as-lethal that this cell just fixed** —
drawn area larger than dangerous area — and it is the conductor's own coherence argument for pulling
`hit_radius_m` forward: *"fixing one and shipping the other would be incoherent."*

**I did not act on it.** Four fields were pinned; closing this needs either a fifth field
(`start_width_m`, or a `width_start_m`/`width_end_m` pair) or a `shape` change from `rect` to a
trapezoid, and both are charter-level. A test asserts `start_width_m` has **not** been added, so
nobody quietly acts on a finding that was handed up for a ruling. **Conductor's call: BR-3, or a
cell 1c if the ruling goes the same way twice.**

---

## §7 — WHAT SURPRISED ME, AND MY OWN INSTRUMENT HAZARDS

### 7.1 — I had the wrong answer and the derivation caught it, not a review

I was **two paragraphs into arguing for 6.0** on the blizzard, with a 186-impact probe behind it,
when writing out `BlizzardEvent.t_expiry` showed the fall-times cancel and the pin was right. The
probe was not wasted — it is what proves the 2.0 s dead tail in §2, which is a real rendering
instruction — but **the headline I was going to hand up was wrong, and math-before-code is the only
reason it never left my seam.** Worth recording, because cell 1's finding was right and this one's
first draft was not; the discipline is what distinguishes them, not my confidence in either.

### 7.2 — `<ABSENT>` vs `None` mattered this cell in a way it did not in cell 1

Cell 1 filled existing keys, so its diff samples read `None → 24.0`. This cell **adds** keys, so on
the cell-1 side they are ABSENT. My `_walk` already carried a `_Missing` sentinel; had it not, the
diff would have crashed or — worse — silently treated absent as `None` and reported **zero**
differences on the null-valued families, which would have read as a tidier PASS than the truth.
Documented at the function now.

### 7.3 — My selectors could each have matched zero, and one had a new way to fail

- **The coverage instrument's field selector is new and is the one that would have failed
  silently.** `FIELDS` is a tuple of strings; a typo in any of the four would have reported that
  family as **100 % null / 0 at value** and produced a clean, confident, wrong FAIL — or, on the
  null-side gates, a clean confident **PASS**. Guarded by `n_absent_key`, which is reported
  separately from `n_null` and is 0 in every cell of §5's table: a mistyped field name shows up as
  1,556 absent, not as 1,556 null.
- **The family selector** still raises `NullInstrument` unless `n_files > 0`, `n_telegraphs > 0`
  **and** each of nova / wave / blizzard is non-zero.
- **The test fixture `tg_by_family`** asserts all three families are non-empty before any `for` loop.

**Both instruments were self-tested against a known answer before either was trusted:**
- **Coverage, against the cell-1 battery:** returned **FAIL on all 12 new gates** (1,556 absent) and
  **PASS on all 6 cell-1 controls**, reproducing legolas's denominators exactly — 470 / 516 / 570
  over 1,556.
- **Diff, against a deliberately mutated copy** (one tick's `hp` +1.0; one telegraph's `radius_m` →
  999.0 and `duration_s` → 42.0): returned **FAIL** and named
  `['event[telegraph].radius_m', 'tick.entities[].hp']` as unexpected, with the `duration_s`
  mutation folded into the expected path (correctly — it is an expected path, and the mutation there
  was a check that the sample-capture works, which it did: `<ABSENT> → 42.0`).

**An instrument that cannot produce a negative has not produced a positive.**

### 7.4 — The cell-1 test that said "these fields must NOT exist" — amended, framed, not deleted

`test_br2_trace_fill_1.py` asserted `duration_s` / `stage_count` / `stage_interval_s` were **absent**
from `TelegraphSpec`, with the message *"TRACE-FILL-1 was pinned as a fill."* **That assertion was
correct, and it is the thing that stopped me adding the fields unilaterally in cell 1.** It is
discharged by the conductor's Addendum-1 ruling, so **the boundary moves rather than the test being
deleted**: the four fields are now asserted PRESENT (owned by the new suite), and the still-unruled
names — `n_volleys`, `volley_interval_s`, `active_duration_s`, `start_width_m` — are asserted absent.
Deleting it would have erased the record that the refusal happened, and the refusal is why cell 1b
exists. Called out here and in the commit message per Discipline #12.

### 7.5 — A cross-seam name collision drax should know about

**`duration_s` already exists as a field name in `reincarnated-godot/scripts/bundle_loader.gd:233`**
(`_instantiate_proxy` — a summon-proxy duration). **Different record type, different object,
different meaning.** No conflict in the telegraph record, but a parser keyed on field name alone
across record types would conflate them. Named in MIGRATION §8.

### 7.6 — Smoke, and the red baseline is unchanged

`pytest` over the new suite + cell 1 + 10 telegraph/spatial suites: **402 passed** (2.23 s). Zero
failures in `spatial_gauntlet`. The project-wide red baseline (**60 failed / 21 errors**, all in
generation / kit-space / foundation / season-generation) is cell 1's finding, already banked to BR-3
by the conductor; this cell neither touched nor changed it.

---

## §8 — ARTIFACTS, LOCATIONS, AND PUSH VERIFICATION

### The batteries

| what | where | stamp |
|---|---|---|
| **The battery of record (PROMOTED)** | `~/Games/reincarnated-godot/tmp/wr3acc/traces/` — 200 files, 90,708 records, 1,556 telegraphs | **`5b8c724b`** |
| The same battery, as generated | `~/Games/reincarnated-godot/tmp/wr3acc_br2stage/traces/` | `5b8c724b` |
| **The cell-1 battery, PRESERVED** | `~/Games/reincarnated-godot/tmp/wr3acc/traces_CELL1_bce46fd9/` — the G-1c baseline | `bce46fd9` |
| **The pre-fill battery, PRESERVED UNTOUCHED** (G-1e) | `~/Games/reincarnated-godot/tmp/wr3acc/traces_PREFILL_ddbdebc8/` | `ddbdebc8` |
| Control-arm battery (pre-change HEAD) | `~/Games/reincarnated-godot/tmp/wr3acc_br2stage_control/traces/` | `2a9ebb02` |
| Pick scan output (this cell) | `~/Games/reincarnated-godot/tmp/wr3acc/wr3_acc_pick_BR2STAGE.json` (`wr3_acc_pick.json` and `..._BR2FILL.json` untouched) | — |

**Why promoted.** `reincarnated-godot/scripts/wr2_traceset.gd:85` hard-codes
`ACC_ROOT := ".../tmp/wr3acc"`, so promoting means **cell 2 opens with no godot-side edit and no
coordination hop.** Three generations now sit side by side under explicit names, so any diff is
re-runnable at any time.

**Generator:** `~/Games/reincarnated-godot/scripts/wr3_acc_pick_scan.py --seeds 200 --out <dir>`
(drax's, **unmodified** — it takes `--out`). Discipline #3 respected: all 200 seeds run sequentially
in one process, and the control arm ran to completion before the code change was restored.

**Commit-before-generate held** (§5.2, the standing order from cell 1's near-miss): `5b8c724b` was
committed from a clean tracked tree first, and the shipping battery stamps `5b8c724b` with **no
`-dirty` suffix** — a real, pushed commit.

### Commits + push verification

| repo | commit | state |
|---|---|---|
| `reincarnated-engine` | **`5b8c724b`** | pushed · **verified present on `origin/main`** |
| `reincarnated-collaboration` | this note | pushed · **verified present on `origin/main`** |
| `reincarnated-godot` | *(none)* | this cell wrote no godot code; the traces are untracked by design |

---

## §9 — GATE SUMMARY

| gate | criterion | measured | verdict |
|---|---|---|---|
| **G-1c limb 1 (control)** | pre-change HEAD reproduces the cell-1 battery | 200 files, 90,708 records, **0 simulation paths**; only `engine_git_hash`, and `bce46fd9..2a9ebb02` is doc-only | **PASS** |
| **G-1c limb 2 (watch trace)** | exactly the 4 paths + `engine_git_hash` | 462/462 records, order identical, **4 sim paths** (n=9 each), **0 unexpected** | **PASS** |
| **G-1c limb 2 (whole battery)** | same, all 200 | 90,708 records, **4 sim paths at n=1,556 each** + 200 headers. **No fifth path.** | **PASS** |
| **G-1c limb 3 (reproduction)** | outcome + scalars | footer identical to the last digit; **0 differing keys** in the pick artifact; re-picks 74000909 | **PASS** |
| **G-1d `duration_s`** | 100 % of all three families at value | **470/470 · 516/516 · 570/570**, 0 null, 0 absent | **PASS** |
| **G-1d `stage_count`** | 100 % blizzard @ 4; null elsewhere | **570/570**; **470 + 516 null**, 0 non-null, 0 absent | **PASS** |
| **G-1d `stage_interval_s`** | 100 % blizzard @ 2.0; null elsewhere | **570/570**; **470 + 516 null**, 0 non-null, 0 absent | **PASS** |
| **G-1d `hit_radius_m`** | 100 % blizzard @ 1.32; null elsewhere | **570/570**; **470 + 516 null**, 0 non-null, 0 absent | **PASS** |
| G-1d cell-1 controls | unchanged | 6/6 gates, all 100 % | **PASS** |
| **G-1e** | MIGRATION + version decided + PREFILL preserved + commit-before-generate | entry written; **no bump**, stated with precedent; `traces_PREFILL_ddbdebc8/` untouched; `5b8c724b` clean | **PASS** |
| Smoke (Discipline #2) | new + cell-1 + telegraph/spatial suites | **402 passed** | **PASS** |

**Open for the conductor, in priority order:**
1. **§1 — the wave's `duration_s` is 1.4875, not the pinned 1.4**, and G-2b's 1.4 ± 0.05 is graded on
   the SWEEP (`range_m / v`), which is unchanged. Shipped with the argument; one word reverses it.
2. **§2 — the blizzard's `duration_s` over-bounds its last impact by 2.0 s.** G-2c's *"total active
   window 8.0 s ± 0.1"* needs re-pinning if it is measured cast-to-last-impact (**6.8333 s**) or
   first-to-last-impact (**6.0 s**) rather than as the liveness window.
3. **§6 — the wave's rect is drawn 2× too wide at the origin.** Same defect class as the two this run
   is fixing. Reported, not acted on.

---

## ADDENDUM A — `start_width_m` routing probe (conductor follow-up, 2026-08-01, read-only)

**The question put to me:** finding #3 says the drawn rect overstates the lane 2× at the origin. Under
R-BR-24 (*render what the SIMULATION resolves, not what the SOURCE says*), that is only a defect if
**our simulation** tapers. If the resolver hit-tests a uniform 6.0 m rect, then a uniform 6.0 m rect
IS the danger zone, the trace is honest, and drawing a trapezoid would be the worse lie — it would
invite a dodge into space that kills.

**Verdict: the simulation tapers. `start_width_m` is CONSUMED in the damage path. This is (a), a
presentation gap.**

### A.1 — The real hit-test, quoted

Chain, walked not inferred: `_gd_wave_resolve_tick` (`spatial_engine.py:6770`) never tests geometry
itself — it delegates to `self._gd_wave.resolve_tick(...)` and consumes `(ev, target_id)` pairs.
That scheduler is `gd_boss_kit.py:836`, which calls `wave_hits` (`:860`). `wave_hits` tests the
lateral axis at `gd_boss_kit.py:680`:

```python
if abs(s) > wave_half_width_m(u, p) + float(target_radius_m):
    return False
```

and `wave_half_width_m` (`:645`) is the taper itself:

```python
return (p.start_width_m + (p.end_width_m - p.start_width_m) * uu / p.distance_m) * 0.5
```

Not a uniform rect. Not a laterally-moving band. A **linearly tapering lane, evaluated per-target at
that target's own along-axis `u`**, plus the target's body radius. The band motion
(`front`/`back` over `depth_m`) is the ALONG axis only and is orthogonal to this question.

### A.2 — The probe, with counts (R-BR-34)

Selector counts over `src/` (`*.py`); call-form = the name followed by `(`:

| name | total refs | call-form |
|---|---|---|
| `start_width_m` | 3 | 0 (it is a field, read at `:645`) |
| `wave_half_width_m` | 5 | **3** |
| `wave_hits` | 19 | **2** |
| `_gd_wave_half_width_m` | **1** | **0** |

`start_width_m`'s three references are: the `WaveParams` field decl (`:535`), the fixture value
`3.0` (`:614`), and **the read inside the half-width formula (`:645`)** — which is on the damage path
via `:680`. Consumed.

**Null-instrument tripwire.** One selector did return zero: `_gd_wave_half_width_m`, the alias
`spatial_engine.py:717` imports. That zero is real and *informative*, not instrument failure — proof
the selector class can find call sites is that the identical selector shape on the unaliased
`wave_half_width_m` returned **3** and on `wave_hits` returned **2**. So: `spatial_engine.py` imports
the taper helper and never calls it; the taper reaches the damage path through the scheduler in
`gd_boss_kit.py` instead. The unused import is cosmetic, NOT evidence of a dropped taper — I checked
precisely because a naive read of that import suggests the opposite conclusion.

### A.3 — Effective width as a function of distance

`full_width(u) = 3.0 + 0.1875·u`, clamped to `u ∈ [0, 16.0]` (`uu = min(max(u,0), distance_m)`).
It reaches 6.0 m **only at u = 16.0 m — the terminal point of the 16 m lane.** Measured:

| u (m) | actual full width (m) | drawn 6.0 overstates by |
|---|---|---|
| 0.0 | 3.000 | **2.00×** |
| 1.0 | 3.188 | 1.88× |
| **2.0** | **3.375** | **1.78×** |
| 4.0 | 3.750 | 1.60× |
| 8.0 | 4.500 | 1.33× |
| 12.0 | 5.250 | 1.14× |
| 16.0 | 6.000 | 1.00× |

The conductor's point lands: with a 2.0 m cone as the primary skill, the player fights at `u ≈ 2`,
where the drawn rect is **1.78× too wide** — the error is worst everywhere he actually stands and
zero only at the one point he never occupies. Area-wise the drawn rect is 96.0 m² against a true
72.0 m² trapezoid (1.33× overall), but that overall ratio understates the harm: the error is
front-loaded onto exactly the band the dodge verb operates in.

Body convention, for whoever charters the renderer: the resolver tests
`|s| <= half_width(u) + target_radius_m`, so the *lane* is the trapezoid and the body radius is added
to the target, not baked into the drawn shape — the same convention `wave_hits` uses on the along
axis.

### A.4 — Documented, or dropped?

Q4 is moot (it IS consumed), but for completeness on the trace side: the omission is **documented as
a handed-up finding, not an undocumented drop.** It is stated in three places written at cell 1b —
math note §8, `simulation/MIGRATION.md:119-121`, and finding #3 above — and `spatial_engine.py:6728`
emits `width_m=float(p.end_width_m)` with the schema comment naming it *"the END width"*. A test
(`test_br2_trace_fill_1.py:288`) asserts `start_width_m` has NOT been added, so nobody can act on it
quietly. What is NOT documented anywhere is a decision that the *renderer* may treat the lane as
uniform — no math note, no MIGRATION entry, no decisions-log line makes that claim, because the sim
does not support it.

### A.5 — Routing, one line

**(a) Presentation gap** — the sim tapers 3.0 → 6.0 over the full 16.0 m and hit-tests against it, so
the uniform 16.0 × 6.0 rect is the trace under-describing a taper the simulation already resolves;
BR-2 needs a cell 1d to emit it, and this is NOT a BR-3 source-fidelity question.

Not acted on. No production code changed, no regeneration, no test amended by this probe. Charter
G-2b still pins the uniform rect and the cell-1b guard test still asserts `start_width_m` absent —
both remain correct until a cell 1d charter with pre-registered gates says otherwise.

---

*BR-2 / TRACE-STAGE-1 — gamora, simulation seam, 2026-08-01.*
