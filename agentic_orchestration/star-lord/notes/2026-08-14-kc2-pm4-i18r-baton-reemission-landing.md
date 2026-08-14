# KC2-PM4 · I-18R — **THE EXPORT-SIDE REPAIR CELL** — landing note

**star-lord · 2026-08-14 · R-PM4-44 part 4 (second serial cell) + R-PM4-45 part 2 · conductor
gandalf · charter ledger L-35 / L-36**

Engine commits: `72685351` (math note, ZERO code) → `ddd7b119` (the repair) → `63b9bad2` (the
verification harness) → `9672cfff` (a self-caught defect in that harness) → `c8c02e41` (the eight
batons + both verification reports) → `3b4021a7` (MIGRATION + AGENT_STATE).
**NOT PUSHED** — the conductor pushes after CL-10.

---

## 0 — THE HEADLINE, IN ONE PARAGRAPH

**The eight refused batons write. 67/67 each, 536/536 across the eight, and every one of them
REPRODUCES the banked `…145832` record rather than re-modelling it.** ⚑ **But the mechanism is not
the one the commission named, and the difference matters:** the export seam's `MovementPolicy` was
ALREADY ladder-scoped — `_player_fold_state` has been called once, outside the wave loop, since
I-4, exactly as gamora's own caller census found. What was wrong was the **STATE INSIDE** the
ladder-scoped object. I-18 gave the player's rate **two carriers**, and the adapter set one of
them: the seek ran at the MEASURED px-arm rate (4.0295 / 3.8361 m/s) while the cadence, the dash
layers and the kite heading ran at the DERIVED **5.4**. One ladder, two speeds. Wave 151 then ran
**361** ticks against the driver's **370**, re-basing every later wave, and `_spawn_tick`'s
F5-M/F5-E interlock refused eight artifacts rather than emit a body whose spawn tick and whose
recorded knot disagreed. ⚑ **The scope ruling still binds and still lands — construction now goes
through `run.ladder_movement_policy()`, the site gamora's refusal message names — but the honest
account of `D-I18-7`'s export half is a SPEED divergence inside a correctly-scoped object, not a
scope divergence. Reported as measured, not as commissioned.**

---

## 1 — ⚑ THE MECHANISM, MEASURED

`kc2_run_adapter._spawn_tick` under the ruled `F5-M-SPAWN-TICK = LAST-STILL-TICK`:

```
derived  = base + max(0, ceil(spawn_t_s / tick_period) - 1)
recorded = knots[actor_id][0]["run_tick"]
raise if recorded != derived
```

`base` is the adapter's own cumulative ladder clock (`tick_start(w_{n+1}) = tick_end(w_n)`);
`recorded` is the DRIVER's, frozen into the digest-pinned artifact. ⚑ **The interlock is therefore
not a rounding check — it is a whole-ladder clock comparison, and `ceil` cannot absorb a term that
changes a wave's DURATION.** That is why I-17's one-tick-per-wave version stayed silent and I-18's
did not.

| carrier of the player's rate | driver (px-LO) | adapter, pre-repair |
|---|---:|---:|
| sim `player_speed_m_s` (`run.py:891`, from the per-wave `player_locomotion` object) | 4.029485432492994 | 4.029485432492994 |
| `MovementPolicy.speed_m_per_s` (cadence phase / dash layers / kite heading) | **4.029485432492994** | ⚑ **5.4** |

| cell `…cluster-defon-critlo-coupled-px-lo` | w151 `tick_start → tick_end` | w152 base |
|---|---|---:|
| DRIVER (banked `…145832`, min `path[0].run_tick` over `w152_*`) | 0 → **370** | **370** |
| ADAPTER, pre-repair | 0 → **361** | **361** |
| ADAPTER, post-repair | 0 → **370** | **370** |

Δ = 9 ticks = 9 × 0.0816326530612245 s = **0.7346938775510205 s**. This is the refusal message
verbatim: `F5-M/F5-E DISAGREE for 'w152_a000': … recorded 370 … derives 361`.

### 1.1 — THE REPAIR

```python
st["movement_policy"] = ladder_movement_policy(
    speed_m_per_s=(plo.measured_speed(_px_arm_of(spec.locomotion_px_arm)).m_per_s
                   if (spec.locomotion_px_arm and spec.locomotion_speed_fold) else None))
```

⚑ **The LAST-STILL-TICK arithmetic is UNTOUCHED** — it is ruled (R-L80-1(M)); what moves is the
ladder state its `base` term derives from. ⚑ **ZERO CONSTANTS**: `measured_speed()` is the sim's
own Lap-R-sourced object, and `speed_m_per_s=None` resolves inside `ladder_movement_policy()` to
`player_drive.player_speed_m_per_s()` with `sane_bound_m` at `run.PLAYER_SANE_BOUND_M`, which `is`
`player_drive.PLAYER_SANE_BOUND_M`. ⚑ **One `_px_arm_of()` table now serves both the per-wave fold
and the ladder policy — two copies of that dict is how the two speeds diverged.**

---

## 2 — ⚑ THE VERIFICATION WALL, AND THE TRUE CHECK COUNT

The charter's **67/67** is **EXACT for this instrument, per baton**, and I confirmed the
composition rather than the number: `VALIDATOR 33 + G-STATS 1 + G-E 33 = 67`
(`kc2_baton_emit.run_gates`). Across the eight re-emitted columns that is **536/536**.

⚑ **The gate wall alone would not have discharged the commission**, because it does not compare
anything to the BANKED record — so the harness adds three reproduction checks that state the
interlock as a COUNT rather than as an absence of exceptions (a silent skip must not read as a
pass):

| check | what it compares | cluster total |
|---|---|---|
| **GATES 67** | VALIDATOR 33 + G-STATS 1 + G-E 33, per column | **536 / 536** |
| **REPRO-SPAWN** | every emitted `actors[].spawn_tick` vs the banked `path[0].run_tick` | **786 / 786** |
| **REPRO-PATH** | every emitted polyline vs the banked one, vertex for vertex | **786 / 786** |
| **REPRO-BASE** | every wave's replay base vs the banked minimum spawn tick | **40 / 40** |

The banked artifact is **digest-verified on read**, twice: once by `load_actor_path_knots` against
`KC2RunSpec.knots_sha256`, and once independently by the harness against the same pin. **The
batons consume the record; they do not re-derive it.**

---

## 3 — ⚑ THE EIGHT RE-EMITTED BATONS (FULL 64 hex, GL-6)

| column | gates | spawn | path | base | file sha256 |
|---|---|---|---|---|---|
| `pm4-i18-cluster-defoff-critlo-coupled-px-lo` | 67/67 | 46/46 | 46/46 | 2/2 | `b3609811cfa3503497845796b145ca27c96ed224d69d749399eee37218e8c736` |
| `pm4-i18-cluster-defoff-critlo-coupled-px-hi` | 67/67 | 116/116 | 116/116 | 6/6 | `9e5bbdabcc9e3f923c4fde4926e8718ecb470d402b97b5f43de69bbab5048dcd` |
| `pm4-i18-cluster-defoff-critlo-decoupled-px-lo` | 67/67 | 115/115 | 115/115 | 6/6 | `5744c9da9341ae53c5385bc457801bf6b171319801c381bfe84fb132e47791b7` |
| `pm4-i18-cluster-defoff-critlo-decoupled-px-hi` | 67/67 | 116/116 | 116/116 | 6/6 | `7f9c56ba66642aec8f8c0258ee8c49a619cc1e5ee2904beff4a07c063e0fa620` |
| ⚑ `pm4-i18-cluster-defon-critlo-coupled-px-lo` | 67/67 | 46/46 | 46/46 | 2/2 | `d2b73d8ff0759d05f4879d9f740ed483a2fdf5ea8f629ce83f19de471ce7a1f0` |
| ⚑ `pm4-i18-cluster-defon-critlo-coupled-px-hi` | 67/67 | 116/116 | 116/116 | 6/6 | `c8fd6de7b986d52809b1a6f28152bcb2f0101d1ee8dbcdefb9542a68247c391e` |
| ⚑ `pm4-i18-cluster-defon-critlo-decoupled-px-lo` | 67/67 | 115/115 | 115/115 | 6/6 | `2f4131f423769bad9baa3b221ee02697b316660cb6b597ea0fe72e1dafa05be8` |
| ⚑ `pm4-i18-cluster-defon-critlo-decoupled-px-hi` | 67/67 | 116/116 | 116/116 | 6/6 | `1cbf1e60870243f616e464df1c02072fe6036c688dc645173e7b665e12b87d76` |

**Verification reports (both runs, committed):**

| file | sha256 |
|---|---|
| `kc2-pm4-i18r-baton-verification-20260814_155000.json` (run 1, the writing run) | `5a5d4eab42ed9372c045ad4c0abf085fa83c039ad023b5299b66490232c409ea` |
| `kc2-pm4-i18r-baton-verification-run2-20260814_155000.json` (run 2, determinism) | `452d709a086d4fa06b4009f0da4a8b01f4921a0454d8138bbdb6040b4a09f2a5` |

### 3.1 — THE PER-WAVE REPRODUCTION, WHERE IT WAS BROKEN

Emitted wave rows carry `tick_start = run_tick_base + 1` (F5-N), so the base is `tick_start − 1`.
The px-LO cells' whole ladder now sits on the banked clock:

| cell | banked / emitted wave bases | terminal |
|---|---|---|
| `cluster-defon-critlo-coupled-px-lo` | 0, **370** | `player_death` @152 |
| `cluster-defon-critlo-decoupled-px-lo` | 0, **370**, 678, 1075, 1640, 1935 | `player_death` @156 |
| `cluster-defon-critlo-coupled-px-hi` | 0, 291, 550, 907, 1472, 1753 | `player_death` @156 |
| `cluster-defon-critlo-decoupled-px-hi` | 0, 291, 550, 907, 1472, 1753 | `player_death` @156 |

The four `defoff` arms reproduce the same bases as their `defon` siblings, wave for wave. ⚑ The
terminals reproduce **L-35's own scorecard** — COU·PX-LO dies @152, everything else @156 — without
anything on this side having been aimed at that result.

---

## 4 — DETERMINISM ×2 — **ZERO DIFF ON ALL TWELVE COLUMNS**

Two separate OS processes; run 1 wrote the eight batons, run 2 wrote nothing. Masked wire digests
(`mask_volatile()`, the one canonical application — never a hand-rolled `pop`) compared on all
twelve columns: **12/12 IDENTICAL, zero differing columns.**

| column | masked wire sha256 (identical in both runs) |
|---|---|
| `cluster-defoff-coupled-px-lo` | `c625c81d3b2aaf4cdcca60983e66aade61c5725996e03b7e1ba2ce646b8b1940` |
| `cluster-defoff-coupled-px-hi` | `97977e162981c4b09e325eadba7b3ca547e02d1d8a263cc69059c2e7a9214728` |
| `cluster-defoff-decoupled-px-lo` | `30b5eaba0420d79d4d8890015886f3ae43d6cb7cd7936546855f913633ba2d61` |
| `cluster-defoff-decoupled-px-hi` | `cf74a2e6ad890a541d07b3e2eda0d69f1dff1da8b52eec411cd8160b5b4fa518` |
| `cluster-defon-coupled-px-lo` | `afdebdff89d37f5e61f2ed7ad5a18358fd10c1269e77df9e037970f4619948f2` |
| `cluster-defon-coupled-px-hi` | `69f5d5227347fbee566aca334e0fd4e85475a021484e594ae72bf92ae303d129` |
| `cluster-defon-decoupled-px-lo` | `a92971e8c0dd51656be9a10457059c72d0f889c3a66ae053e8e69b5f5b08e3cd` |
| `cluster-defon-decoupled-px-hi` | `5ff66a5b176873aa15cbb0b0fc737f1afbf8aefe7890dde059386aacba7ea102` |
| `camp-defoff-coupled-px-lo` | `b192b4d49ff9353089789692cb7f06ffee6facd077abff61fa89bf067be02e4f` |
| `camp-defoff-coupled-px-hi` | `a957cb3daadc7740037b7a16390f4995bfab172b2d0c7d2ea85cdd34a580e889` |
| `camp-defoff-decoupled-px-lo` | `25c1f4b054a11a58a5deacc83a69d3127f9109957de4f6518de79bceb4f436d1` |
| `camp-defoff-decoupled-px-hi` | `d41090ec37a77b1db599b17ca2ecef57e51c169ba0f6f05e60121e7a2619746d` |

---

## 5 — THE CONTROLS: **NOTHING ELSE MOVED, AND IT IS MEASURED**

**(a) The four CAMP columns vs their banked batons — EXACTLY TWO DIFFERING LEAVES, on all four:**

```
.sim_pin.engine_version_full  ['9672cfff…' != '2052f145…']
.sim_pin.engine_version_sha   ['9672cff'  != '2052f14' ]
```

⚑ Nothing else. Not one actor, not one event row, not one track sample, not one wave key. The
engine pin advances with this cell's own commits **by construction** — and it is deliberately NOT
masked, because `engine_tree_state` / `tree_state_policy` / `engine_version_sha` are claims about
the run rather than colour. **Camp carries `movement_fold=False`, so no policy object exists there
at all; that is the control that proves the repair touched only what it claimed to.**

**(b) Every pre-I-18 movement-fold spec — EXACT.** Old construction vs new, in the SAME process, on
the masked run-record digest and the full wave `tick_start`/`tick_end` series:

| spec | old digest | new digest | verdict |
|---|---|---|---|
| `pm4-i4-cluster-defon` | `7f1125aead48c7f4…` | `7f1125aead48c7f4…` | **EXACT** |
| `pm4-i13-cluster-defon-critlo` | `4374075fcc89ab34…` | `4374075fcc89ab34…` | **EXACT** |
| `pm4-i17-cluster-defon-critlo-coupled` | `e0ee0b9e4617ba6c…` | `e0ee0b9e4617ba6c…` | **EXACT** |

**(c) Test suite:** 427 pass on the `kc2 | baton | adapter` selection. The one failure
(`test_AC_10_10 :: bare 30.0 in secondary_streams.py`) is **PRE-EXISTING and gamora's own reported
one** — same failure, same line, before and after this cell.

**(d) Frozen substrate `E-s09-cp150` UNTOUCHED. `simulation/` READ ONLY — zero writes.** Zero
telemetry-schema change; zero `baton/v1` schema change; `_schema_version` unmoved.

---

## 6 — ⚑ DEFECTS, BOTH SELF-CAUGHT, BOTH MINE (FIT law)

| id | what | disposition |
|---|---|---|
| ⚑ **`D-I18R-SL-1`** | The comment at the `player_locomotion` kwarg said verbatim: *"the movement policy below takes the SAME speed, so the adapter cannot hand the cadence one rate and the seek another."* **It could and it did, on every I-18 cluster replay.** The sentence was a guarantee with no mechanism, nothing tested it, and the F5-M/F5-E gate is what caught it nine ticks later. | **REPAIRED + the comment amended to describe a mechanism instead of an intention.** The mechanism is the shared `_px_arm_of()` table. |
| ⚑ **`D-I18R-SL-2`** | My own REPRO-PATH check compared the baton's **quantised** wire values against the sim's **raw** floats and read **0/N on all twelve columns — including the four CAMP columns whose banked batons shipped GREEN at I-18**. A check that fails on a known-good emission is measuring the wrong quantity. | **REPAIRED in its own commit (`9672cfff`), cause named.** The precision is now READ FROM THE WIRE (`_precision.position_dp`) and applied with the emitter's own `quantise()`. ⚑ **Had the camp control not been carried, this would have read as eight failed batons — the control earned its keep on its first outing.** |

---

## 7 — THE PRE-REGISTERED CLAIMS, GRADED — **7 / 7**

Registered at `72685351`, before any code moved.

| # | claim | verdict |
|---|---|---|
| **C1** | divergence is entirely the policy speed term; post-repair w151 `tick_end` = 370 | ⚑ **HELD** — 370 on every px-LO cell |
| **C2** | eight columns emit, 67/67 each | ⚑ **HELD** — 536/536 |
| **C3** | F5-M/F5-E agrees on every body, zero raises | ⚑ **HELD** — 786/786 spawn, 786/786 path, 40/40 base |
| **C4** | camp payloads identical under `mask_volatile()` except the engine version pin | ⚑ **HELD** — exactly 2 leaves, both the pin, on all four |
| **C5** | pre-I-18 specs unmoved | ⚑ **HELD** — EXACT on i4 / i13 / i17 |
| **C6** | determinism ×2, zero-diff | ⚑ **HELD** — 12/12 |
| **C7** | zero schema change, `simulation/` reads only, frozen substrate untouched | ⚑ **HELD** |

**Nothing was adjusted to make a digest fit. No check failed, so no HALT was owed** — and the one
thing that DID read RED was my own instrument, reported in § 6 rather than tuned away.

---

## 8 — TO THE CONDUCTOR

| id | what | disposition |
|---|---|---|
| ⚑ **`C-I18-2`** | eight batons refused | ⚑ **CLOSED. Eight batons on disk, 536/536 gated, reproducing the banked record on 1,612 independent per-body checks.** |
| ⚑ **`D-I18-7`** | export half | ⚑ **REPAIRED — and RE-CHARACTERISED.** The export seam's policy was already ladder-scoped since I-4; the divergence was its SPEED. The ruling's construction-site consolidation lands anyway and is what prevents the recurrence. **The conductor may want L-37 to say "one ladder, two speeds" rather than "wave-scoped in the adapter", because the second sentence is not true of `export/`.** |
| ⚑ **`D-I18R-SL-1` / `D-I18R-SL-2`** | two self-caught defects | banked, § 6, both repaired in their own commits |
| ⚑ **THE `S-*` SENSITIVITY LIMBS ARE NOT EMITTABLE TODAY** | `S-SPEED-ONLY`, `S-SEEK-ONLY`, `S-INCUMBENT-SEEK`, `S-PX-MID`, `S-NO-KILLABLE-FILTER`, `S-CAMP-UNPINNED` have **no registered `KC2RunSpec`** and therefore no baton path. `_i18_spec` also RAISES on `px="mid"` by design. **NAMED, not taken** — a spec per limb is a designation question, not a plumbing one. | **for the conductor** |
| ⚑ **MIGRATION entries lapse at I-11** | `export/MIGRATION.md`'s newest KC2-PM4 row before this one is **I-11**; I-12 … I-18 added adapter specs with no export-seam entry. This cell's row is written; the gap behind it is **REPORTED, NOT BACKFILLED** — backfilling seven iterations from memory would manufacture a record rather than keep one. | **flagged to knight-rider for a dispatch** |
| carried | knot-leg instrument candidate (R-PM4-45 part 3) is gamora's, not mine — noted only so it is not double-counted | carried |

---

## 9 — COMMITS (ENGINE, `main`, **UNPUSHED**)

| sha | what |
|---|---|
| `72685351` | math note, **ZERO code** — the derivation change + C1–C7 pre-registered |
| `ddd7b119` | the repair: `_player_fold_state` → `ladder_movement_policy()` + measured px-arm speed; `_px_arm_of()`; `D-I18R-SL-1` comment amended |
| `63b9bad2` | the verification harness (committed BEFORE it runs — it is on the code surface the batons grade themselves against) |
| `9672cfff` | `D-I18R-SL-2` — the harness's own quantisation defect, caught by the camp control |
| `c8c02e41` | the eight batons + both verification reports |
| `3b4021a7` | `export/MIGRATION.md` I-18R row + `AGENT_STATE.md` |

**Meta:** this note. **Push withheld for CL-10 per the cell's instruction.**
