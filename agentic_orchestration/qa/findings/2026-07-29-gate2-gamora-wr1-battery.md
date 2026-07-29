# Finding — 2026-07-29 — WR1-G2-BATTERY (the battery landing, eight commits, two laps)

**Reviewer:** jack-ryan (DEV-MODE, read-only)
**Severity:** **BLOCK** (overall) — per-commit verdicts in §0
**Target:** engine `2594bbb` → `d38e00d` → `5f830d3` → `cf99b5d` → `d4cc2dc` → `7f77ea0` → `05a294f` → `98d3891`
**Developer:** gamora
**Run / cell:** WR1-2026-07-28 · WR1-BATTERY + WR1-BATTERY-2 · conductor gandalf (`RUN-CONDUCTOR`), charter §8.16–§8.18
**Principles applied:** 1 (math-before-code), 2 (smoke-gate / full regression), 3 (cross-seam impact),
4 (decisions-log as truth), 5 (severity), 6 (cross-seam round-trip) · **Disciplines:** #1, #2, #3, #9, #10, #11, #12 · **ADR-004**
**Method:** every headline claim RE-MEASURED on my own instruments, in clean worktrees at
`d38e00d` / `5f830d3` / `98d3891`. Full regression independently re-run to completion, foreground,
against my own `a42d052` baseline from the previous gate. No engine mutation; worktrees removed at
close; engine tree verified clean (`git status --porcelain -- src/ tests/` empty, before and after).

---

## §0 — VERDICT PER COMMIT

| commit | what it is | verdict |
|---|---|---|
| `2594bbb` | Step-0a — WARN-A fix | **PASS** |
| `d38e00d` | Step-0b — WARN-B `hp_provenance` MIGRATION entry | **PASS** |
| `5f830d3` | Step-1a — CLI plumbing + P-5 record | **PASS-with-notes** (WARN-3) |
| `cf99b5d` | Step-1b — HALT on H-B-2 + probe statistics | **BLOCK** (BLOCK-1) |
| `d4cc2dc` | AGENT_STATE | **PASS** |
| `7f77ea0` | Step-1 — R-WR1-16 applied | **PASS** |
| `05a294f` | Step-2/3/4/5 — battery banked, H-B2-6 fires | **PASS-with-notes** (WARN-1, WARN-2) |
| `98d3891` | AGENT_STATE | **PASS** |

**OVERALL: BLOCK.** One pre-registered acceptance criterion is not met and one guard protecting a
Matt-ratified containment boundary is red on the tip.

**What the BLOCK is NOT.** It is not a numbers finding. **Every statistic in the banked artifact
reproduced on my own instruments, to the digit.** The four named special checks (a)–(d) all come
back clean or better-than-claimed. The banked battery is, arithmetically, sound. The BLOCK is a
containment-guard breach with a ~6-line prescribed remedy that moves no number and requires no
re-run of the 450 fights.

---

## §1 — 🛑 BLOCK-1: THE FAILURE-NAME DIFF IS NOT EMPTY. A BQ-3 CONTAINMENT GUARD IS RED.

**Method: I RE-RAN THE FULL REGRESSION.** Fourth consecutive lap on which I have re-run rather than
audited, for the unchanged reason — the pre-registered criterion is an empty failure-NAME diff
against a baseline I produced myself, and an audit of someone else's log cannot confirm the log came
from the tree under review.

```
JR_REG3_START  2026-07-29T13:00:40Z   HEAD = 98d3891138c4a6791f23845ee6d002807b2fc28c
JR_REG3_END    2026-07-29T13:24:29Z   (23 m 47 s)
  61 failed, 6040 passed, 3 warnings, 21 errors
  failure_name_count = 82
  names ONLY in 98d3891 (new failures):
      tests/test_bq3_calibration_override_door.py::TestStaticContainment::
          test_T8_no_production_callsite_enables_overrides
  names ONLY in a42d052 (fixed/vanished) : (none)
```

| term | a42d052 (my baseline) | 98d3891 (measured) |
|---|---|---|
| failed | 60 | **61** |
| passed | 6004 | **6040** |
| errors | 21 | 21 |
| failure names | 81 | **82** |
| **name diff, new-failure direction** | — | **NOT EMPTY (1)** |

**The arithmetic closes exactly and identifies the mover.** New suites: `test_wr1_battery_arms.py`
22 + `test_wr1_battery2_a_dmg1_grain.py` 14 + T-M6-11 1 = **37**, each collected independently.
`6004 + 37 − 1 = 6040` ✓. **All 37 new tests pass; exactly one pre-existing test regressed.**

### 1.1 The breach

```
BQ-3 CONTAINMENT BREACH (math note §2 L5): a shipped module opens the calibration-override door.
Matt's ratification amendment (2026-07-28) is that these values are NEVER used in the sim/pipeline.
If this is a genuine calibration harness, add it to _DOOR_ALLOW_LIST deliberately.
Offending sites: [('src/reincarnated/simulation/wr1_battery_probes_2026_07_29.py', 153),
                 ('src/reincarnated/simulation/wr1_battery_probes_2026_07_29.py', 205)]
```

- **Introduced at `cf99b5d`** (the file's add-commit). The guard **PASSES at `d38e00d`** — I ran it
  in the worktree — and fails at `98d3891`. Deterministic (a static AST sweep), not flaky.
- `_DOOR_ALLOW_LIST` holds exactly one entry, `kitcal_g5_harness.py`, added deliberately at the G-5
  assembly with a written justification. The probes driver was not added.
- `wr1_battery2_2026_07_29.py` does **not** open the door itself; it imports the probes module
  (`as P`, line 48) for `verify_instrument_fidelity()` and the G-B probe legs, so the offending
  module **is** on the banked-statistics path.

### 1.2 Why it is BLOCK, and why it is nonetheless cheap

**BLOCK grounds:**
1. The pre-registered Gate-2 acceptance criterion for this run is an **empty failure-NAME diff in
   both directions**. It is not empty. That criterion is charter-level and I have applied it on the
   three prior laps of this run.
2. The guard protects a boundary carrying a **Matt ratification amendment (2026-07-28)** —
   *"these values are NEVER used in the sim/pipeline."* A red guard over a locked, Matt-ratified
   decision is BLOCK by my own rubric, not WARN (Principle 4, Principle 5).
3. It shipped in `cf99b5d` and survived **two further commits and a conductor ruling** unnoticed.
   Cell note §1.6 and §6.6 both report "adjacent suites re-run whole" (192, then 240 passed);
   `test_bq3_calibration_override_door.py` is not in the adjacent set, and **neither note declares
   that the full regression was not run.** This is precisely the Discipline #2 case my `m4to9`
   finding §10 recorded as the pattern to repeat — the full regression earns its status by catching
   what targeted suites structurally cannot.

**Why it is cheap, stated so the path forward is unambiguous:**
- **No banked number moves.** All 450 banked fights carry
  `calibration_override_fields = armor,block_chance,block_value,crit_chance,elemental_resistances,lifesteal_percent,max_hp,mitigation_law`
  — produced through `kitcal_g5_harness.py`, which **is** allow-listed. The KIT-CAL fixture *is* a
  calibration construct; the door is load-bearing for it.
- **The flag is CORRECT on the probes driver.** It must match the harness or the two paths are not
  comparable — and `instrument_fidelity` reads **6/6 identical** precisely because they do match.
  Closing the door would break the fidelity check, not fix anything.
- **The remedy is the guard's own prescribed act:** add `wr1_battery_probes_2026_07_29.py` to
  `_DOOR_ALLOW_LIST` with the same class of written justification the harness entry carries
  (measurement driver; no season, no convergence loop, no endgame-BC batch; artifacts to
  `simulation/output/`). ~6 lines. **No re-run of the 450 fights.**

**This is a declaration-of-intent gap, not a containment failure.** The distinction matters and I
want it on the record: nothing improper reached production. What is missing is the deliberate,
written act the guard exists to force.

---

## §2 — THE FOUR NAMED SPECIAL CHECKS (charter §8.18)

### (a) R-WR1-16 RECLASSIFICATION — **SOUND. I concur, and the evidence is stronger than cited.**

**Is the anchor-grain argument sound?** Yes. I read all three cited sources at origin.

1. **`greatestDamageReceived = 260.4977`** — legolas `2026-07-28-kitcal1-sustain-decomposition.md`
   §14.10: *"no single damage event exceeded 260.50 HP post-mitigation"* across Act 1, levels 1–13,
   7 champion + 3 hero kills **and the boss**, against pools 366–759. Post-mitigation, MEDIUM-HIGH.
2. **The "≥3 hits" record** — same note, verbatim: *"The death-2 window's `drop_max` is 541 HP over
   a 3 s window — ≥3 hits — against a 747 pool."*
3. **GAL-3's r = 1.26 m** — charter §8.12, verbatim: *"at 1.26 m the rays sit 0.49 m apart,
   **multi-hit is FORCED**."* Band [0.96, 1.61] @95 %; P(r ≥ 5.0) = 0.000.

**A fourth leg the ruling did not cite, and it is the strongest one.** The same legolas note records
galadriel's 15 fps globe series carrying a **single-frame (67 ms) drop of 304 HP** — *above* 260.50 —
which legolas resolved at the time as *"two hits inside one frame pair."* **The fixture's own record
had already forced the per-hit reading before the sim ever produced a 414.80.**

**And the decisive form of the argument, which I want stated because it is a falsification rather
than an interpretation:** if the GD client bucketed a whole nova crossing as one damage event, then
death-2 — measured at a radius where multi-hit is geometrically forced, delivering 541 HP — would
have set `greatestDamageReceived ≥ 541`. It reads 260.4977. **Therefore GD emits per-projectile.**
The grain is not inferred from panel semantics; it is entailed by the anchor's own value.

**Is the amended falsifier genuinely LIVE?** Yes — I drove `assert_a_dmg1` myself:

| planted grain block | result |
|---|---|
| real point leg (414.80 over n=2 ⇒ 207.40/proj) | **PASS** ✓ |
| real endpoint (470.80 over n=2 ⇒ 235.40/proj) | **PASS** ✓ |
| +25.5 % payload (260.29/proj) | PASS |
| +25.6 % payload (260.49/proj) — the stated edge | PASS |
| **+26.0 % payload (261.32/proj)** | **REFUSED** ✓ |
| endpoint +10.7 % (260.59/proj) | **REFUSED** ✓ |
| **NON-NOVA 300 HP, zero crossings** | **REFUSED** ✓ |
| **NON-NOVA 261 HP, zero crossings** | **REFUSED** ✓ |
| NON-NOVA 260.0 HP | PASS (boundary exact) |

The falsifier fires at ~26 % payload inflation exactly as the ruling claims, and **non-nova coverage
did not retreat one HP** — Disposition 2's rejection is real in code, not only in prose. The
predicate is `max` over ALL events of `per_projectile`, where non-nova events carry
`per_projectile = delivered`.

**Is anything hidden?** No. `a_dmg_1_grain` carries `worst_received_event_hp_SIM_GRAIN = 470.80`
(endpoint) / `414.80` (point) beside `worst_per_projectile_hp`, on **every** tier including
nova-free ones, so a measured zero stays distinguishable from an unproduced field. The erratum
banner is in **both** the source comment (`kitcal_g5_harness.py:1444-1449`) and the emitted manifest.
The 414.80 is declared, not suppressed. ✓

**Verdict on the reclassification: APPROVED.** It is a read-side restatement at the anchor's own
grain over a ledger the engine already keeps; no kernel line changed; the falsifier is live with
measured headroom; the rejected dispositions stayed rejected in code.

### (b) THE 1.667× VERIFICATION CLAUSE — **NO CONTAMINATED CLAIM. Verified by measurement.**

I scanned all three prior findings (`m12`, `m3-m12b`, `m4to9`) for magnitudes or outcomes traceable
to the M-3/M-12 direct test paths. **Two candidates; both clear.**

**`m4to9` §4.1** (28.80 s player win → 32.00 s MONSTER win; presses/s 2.431 → 1.031): the instrument
is named in the finding as `--smoke --gd-cadence`. That is the harness path —
`kitcal_g5_harness.py:757` → `run_spatial_fight` → `spatial_engine.py:7075`
`spatial_dm = damage_modifier * SPATIAL_DAMAGE_SCALE`. **On the battery's own regime. CLEAN.**

**`m3-m12b` §1** (crossing t = 1.951 s, r\* = 5.6170 m, delivered 207.40 at n = 1): I settled this by
running both constructions side by side rather than by arguing about it:

| seed | test path (`dm` omitted ⇒ 1.0) | runner-equivalent (`dm = 0.6`) |
|---|---|---|
| 74000900 | `t=1.9512, delivered=207.4, n=1, r*=5.617` | **identical** |
| 74000802 | `t=1.9512, delivered=414.8, n=2, r*=5.617` | **identical** |
| 74000800 | no crossing | no crossing |

**The crossing figures are invariant to the player's damage scale** — the crossing lands at 1.95 s,
before the scale can move the trajectory, and the payload is the *boss's* operator against the
player, which player damage does not enter. The quoted figures also reproduce on the fully
independent banked battery (`t_s = 1.951214` on all three legs). **CLEAN, by measurement.**

**Nothing to retract.** The §4 finding itself is accurate and correctly scoped: I confirmed
`_run_boss_fight` omits the third positional (`tests/test_wr1_m12_gd_mitigation_nova.py:710-711`).

### (c) H-B2-6 DECOMPOSITION — **RE-DERIVED INDEPENDENTLY. The 2.0000 IS the count step.**

I recomputed G-A from the banked traces with my own nearest-rank p99, implemented from the math
note's *words* (§2.3), touching no builder code.

| tier | m pt/post/end | ratio point | ratio endpoint | ratio_max end |
|---|---|---|---|---|
| trash | 264/263/264 | 1.0000 | 1.0000 | 1.0000 |
| champion | 180/179/180 | 1.0000 | 1.0000 | 1.0000 |
| mixed_pack | 519/480/519 | 1.0000 | **1.0696** | 1.0682 |
| **boss** | **1828/2206/1334** | 1.0000 | **2.2700** | **1.1350** |

Every figure reproduces. **The 2.0000 is proven to be the realized-count step, not something else** —
the direct evidence is the payload-quantum histogram, which I computed rather than inferred:

```
delivered / unit-payload, boss-tier nova crossings, all 44 per leg:
  point    (unit 207.40)  ->  {1.0: 30, 2.0: 14}
  post     (unit 207.40)  ->  {1.0: 30, 2.0: 14}
  endpoint (unit 235.40)  ->  {1.0: 30, 2.0: 14}
```

**Every crossing delivers exactly 1× or 2× the unit payload.** So 470.80 = 2 × 235.40 is a
2-projectile crossing and 207.40 is a 1-projectile crossing — the factor is the integer count, and
nothing else. The rank arithmetic:

| leg | m | k = ⌈0.99m⌉ | events at rank ≥ k | histogram at rank ≥ k |
|---|---|---|---|---|
| point | 1828 | 1810 | 19 | `{207.4: 5, 414.8: 14}` |
| post | 2206 | 2184 | 23 | `{207.4: 9, 414.8: 14}` |
| **endpoint** | **1334** | **1321** | **14** | `{470.8: 14}` — razor-thin, exactly 14 |

**Stronger than claimed:** the note says "14 on both legs." It is **14 on all three legs**, and the
total crossing count is **44 on all three** — invariant to the resist vector, which is direct
evidence for the "geometry and its own RNG sub-stream, not the player's HP" claim.

Identity: `235.40/207.40 = 1.135005`; `470.80/414.80 = 1.135005`; `1.135005 × 2 = 2.270010` =
measured `2.270010`. **Exact.** §14.2's mixed_pack mechanism also verified at source —
`slitha_melee_b01_attack` carries `canonical_element: "physical"` with **two** damage effects,
39.8 physical + 9.6 cold; closed form 1.066548 vs measured 1.0696. The schema mis-attribution hazard
is real and correctly routed.

### (d) THE CONDUCTOR'S G-A GRADING STANCE — **HONEST, AND IF ANYTHING UNDER-STATED.**

The conductor pre-stated (before this review) that G-A grades on the gear-step component 1.1350,
with 2.2700 reported and decomposed alongside, because the owner's question is the gear step's
effect. **I concur, independently, and I found a third corroboration the conductor did not have.**

Three independent lines all put the gear step at 1.1350:
1. **The max-based ratio** `470.80/414.80 = 1.135005` — the estimator that does not move with pool size.
2. **The closed form pre-registered in math note §10.2** before the endpoint leg existed as an object.
3. **NEW — the per-arm split (see WARN-2).** Endpoint **arm B reads `ratio_p99 = 1.1350`** because
   its pool (794) is large enough that the 1 % cut does not reach the 2-projectile crossings.
   Arm A (pool 540) reads 2.2700. **The same leg, same gear step, reads the pure gear step under a
   slightly larger pool.** That is direct evidence that 2.2700 is a rank artifact.

**Is the conductor under-crediting a formal pass?** No — and the direction of the error matters:
the endpoint's larger payload is what shortens the fight and shrinks the pool, so grading 2.2700 at
face value would **partially double-count the payload increase through the estimator**. It is not a
neutral estimator quirk; it inflates in the gate's favour.

**One precision note, offered as refinement rather than objection.** The stance as worded grades a
bracket `[1.0000, 1.1350-gear-component]`, whose low end is a raw p99 estimator output and whose
high end is a decomposed component. Those are two different objects in one bracket. The cleaner
construction, which reaches the same verdict without mixing them:

> Report the pre-registered p99 bracket **`[1.0000, 2.2700]`** as the estimator's literal output —
> no goalpost moves — and grade the predicate's **intent** on **1.1350**, naming the rubric and the
> three corroborations above.

**And a warning attached to it:** do **not** reach for the max-based estimator to obtain 1.1350
cleanly (`[1.0000, 1.1350]` on max both ends). §2.3 fixed p99 before any measurement and named max
as a *diagnostic*; switching estimators after seeing numbers is exactly what the builder refused to
do at the moment it would have helped. The decomposition route is the honest one.

---

## §3 — THE STANDARD PER-LANDING REVIEW: WHAT I RE-MEASURED

### 3.1 Step-0 fixes — both CLOSED

**WARN-A (`2594bbb`) — closed, and the wider reach is genuinely covered.** The stale entry is gone
from the **report and the trace header** (I read an emitted `g5_header`: 5 entries, the crit-absence
claim replaced). The replacement claim is verified at source, not accepted:
`spatial_resolver_adapter.py:342` inside `combatant_projection_from_monster_dict` hard-codes
`crit_chance=0.0`, and the signature is `(monster_dict, hp_multiplier)` — **no override door**, as
claimed. `named_absent(with_nova=…)` correctly swaps the nova claim; the armed
`_NOVA_PRESENT_ENTRY` reaches every banked trace header. ✓

**WARN-B (`d38e00d`) — closed, and parseable cold.** I read the entry as drax would. Value set
`{M, D, D-HELD, null}` with meaning *and* producer per tag; `null` framed as a producer statement
with its three cases separated; producer chain named end to end; the do-not-fold-`D-HELD` ask
stated. **Its factual claims verified against the emitted artifact**, not asserted: player
`max_hp 759.0 / hp_provenance null`; boss `14812.0 / "M"`; both slitha `"D"`. ✓

### 3.2 Default-off darkness — REPRODUCED, on a TIGHTER normalization than the builder's

Three worktrees, three `--smoke` runs, my own normalizer:

| tree | trace digest (stripping **only** `engine_git_hash`) |
|---|---|
| `d38e00d` (Step-0) | `9d7890f06db4` |
| `5f830d3` (plumbed) | **`9d7890f06db4`** |
| `98d3891` (tip) | **`9d7890f06db4`** |

**Identical across the whole span.** Report key-diff, volatiles stripped and nothing else:

- `d38e00d` → `5f830d3`: exactly **3** new keys — `wave_regime`, `mitigation_model`, `p5_freeze_shatter`.
- `d38e00d` → `98d3891`: those 3 plus `a_dmg_1_grain` and per-fight `a_dmg1` ×5. **Nothing else.**
- **No value changes anywhere.** Fight digest identical `d38e00d` ≡ `5f830d3`.

This is stronger than the builder's claim, which covered only the plumbed tree: **default-off is
dark all the way to the tip**, and the additive set is provably exactly those five keys.

### 3.3 P-5 manifest + `_gd_nova` walk — REPRODUCED; T-BAT-8b verified BOTH directions, myself

My own `freeze_shatter_manifest()` call reproduces the counts exactly:
`kit_variants 8 · kit_skills 16 · kit_effects 28 · scenario_builds 2 · tiers 8 · mob_rows 42 ·
mob_skills 43 · mob_effects 48 · gd_nova_blocks 1 · effects_total 76` — identical on all three
banked legs.

**The blind spot the cell reported is real:** `_walk_freeze(nova_skill["effects"])` returns **0** —
the nova ships `effects: []` and its payload (including `freeze_min_s=1.3 / freeze_max_s=1.8`) lives
under `_gd_nova`. I drove `_walk_gd_nova_block` myself:

| direction | result |
|---|---|
| the legitimate lock (`freeze_min_s`/`freeze_max_s`) | **PASSES** ✓ — a substring guard would have refused M-2's own mechanic |
| planted `shatter_threshold_fraction` in `params` dict | **REFUSED** ✓ |
| planted `shatter_damage_percent` in `params` dict | **REFUSED** ✓ |
| planted `shatter_threshold_fraction` at block top level | **REFUSED** ✓ |
| planted `shatter_damage_percent` at block top level | **REFUSED** ✓ |
| **planted as an ATTRIBUTE on a `NovaParams` object** — the real shape | **REFUSED** ✓ |

The last row is the one I added beyond the suite: `params` is a dataclass instance, not a dict, so
the object-attribute path is the live one. It holds. **The strengthening of R-WR1-15's discharge is
genuine.**

### 3.4 Banked artifact stamps + SS-1 — VERIFIED

- **P-4:** `wave_regime` per arm (incl. `piloted_competence_m3: null` with its M-3-dark note);
  `mitigation_model` carrying armour, reading, resists and **both grades** (`armour_grade` +
  `resist_grade`) on all three legs.
- **`non_poolable_with`:** names the G-5 before-baseline **by hash** — `bef1f55` and `f54c547` —
  and each arm separately with its own regime id. ✓
- **All three legs:** 12/12 static pins, `effect_name_policy = strict`, INS-1 identical under the
  door, 150 traces, telegraph events present (584 lines/leg).
- **SS-1 INTACT, measured not assumed:** `git diff --name-status 2594bbb^..98d3891 -- output/`
  yields **455 files, all status `A`**. Zero `M`, zero `D`, zero `R`. Nothing banked was overwritten.
- **The C-5 guard is live, not merely disciplined** — it FIRED on me when I attempted a re-run:
  *"already holds a report from engine '7f77ea0'; this run is '98d3891' … another commit's evidence."*
- **A-DMG-1 pre-flight reproduced to the digit** from my own clean-tree run: 207.40 / 207.40 / 235.40
  per projectile, 414.80 / 470.80 sim-grain, 22 crossings and `max_n=2` in every cell, headroom
  25.60 % / 10.66 %, clean and non-vacuous. All six cells.
- H-B2-5 450/450 clean; instrument fidelity 6/6; H-B-4 divergence at arm A's lethal index only.

### 3.5 ADR-004 on the R-WR1-16 landing — EXEMPLARY

The `a_dmg1` / `a_dmg_1_grain` entry is filed **at the same commit as the code** (`7f77ea0`), names
both consumers and that neither owes anything, states the one thing a consumer must not do
(read `worst_received_event_hp` as a per-hit number), and **routes drax the exact field location**
(`gd_nova_crossings`, 7-tuple, 0-based field 6). This is the discipline the two entries above it
exist to establish, applied without being asked twice.

---

## §4 — WARN / INFO (routed, not absorbed)

### WARN-1 — the dual-hash claim is FALSE; the statistics stamp is a C-4-class false record

Cell note §8 and **charter §8.18** both state: *"legs `7f77ea0`, statistics `05a294f` — two
production events, two hashes, deliberately."*

**The artifact reads `statistics_engine_git_hash = "7f77ea0"`.** There is one hash, not two.

- `wr1_battery2_2026_07_29.py` was **added at `05a294f`** — it did not exist at `7f77ea0`. So the
  stamp names a tree that **does not contain the code that produced the artifact**. That is exactly
  the defect `_git_hash`'s own docstring exists to prevent: *"a truthful record of HEAD and a FALSE
  record of the code that ran."*
- **Root cause:** `_git_hash` uses `git status --porcelain --untracked-files=no`. A brand-new,
  never-committed driver is *untracked*, so the `-dirty` suffix never fired.
- **The legs' stamp is honest** — I verified `git diff 7f77ea0..05a294f -- spatial_gauntlet/` is
  **empty**, so the harness that produced the fights genuinely is `7f77ea0`.
- **Second leg of the same imprecision:** the artifact carries `battery_runs: {}` and
  `wall_seconds: 7.0`, i.e. it was written by a `--recompute-only` invocation — not the
  *"full driver 15.2 s, foreground to completion, exit 0"* run the note describes. (Using
  `--recompute-only` is *correct*; C-5 would refuse the full path. Only the note's provenance
  sentence is imprecise.)

**No number is contaminated** and provenance is recoverable (`git log --diff-filter=A` on the
artifact path). **Severity WARN, must close before baton emission** — the charter states the dual
stamp as banked fact and it will travel to consumers. Two routes: re-run `--recompute-only` from the
committed tree (7 s, stamp becomes correct), or correct the note + charter and record the stamp's
known limitation. Reviewer has no preference; one must be chosen. Discipline #9.

### WARN-2 — "arms A and B give the same ratio on every tier, so pooling moves nothing" is FALSE

Cell note §9.1 (line 619) and math note §2.4's erratum both carry that sentence. **The artifact's own
`by_arm` block contradicts it**, and I reproduced both figures independently:

| endpoint leg, boss tier | `ratio_p99` | `n_pre` |
|---|---|---|
| **arm A** | **2.2700** | 540 |
| **arm B** | **1.1350** | 794 |

**The number is not wrong** — 2.2700 is the correct pooled p99 under the pre-registered §2.4 pooling
rule. The defect is that §2.4 offered per-arm reporting as *the auditability guarantee for pooling
across arms*, and the guarantee's stated result no longer holds. The sentence was true when written
(the first cell had no endpoint leg) and was **carried forward unrevised** into a cell where the
endpoint leg exists.

**This finding is materially useful, not merely corrective** — it is the third corroboration of the
conductor's grading stance (§2(d)). Route: correct the sentence, and promote arm B's 1.1350 into the
G-A grading record as supporting evidence.

### WARN-3 — `5f830d3` added three additive report keys with no MIGRATION entry (ADR-004)

`wave_regime`, `mitigation_model`, `p5_freeze_shatter` all first appear at `5f830d3`. MIGRATION.md
mentions: **0**, **1** (incidental, inside the `R2_proxy_resists_low` section — not documented as a
new key), **0**.

By the cell's **own** standard — stated verbatim in the `a_dmg1` entry it filed two commits later:
*"This key lives on the HARNESS REPORT … which star-lord's exporters read"* — these are the same
ADR-004 class. **Third occurrence of WARN-B's defect, inside the very commit sequence whose Step-0b
exists to repair the second.**

Mitigating and real: they are provenance/manifest blocks rather than rendered payload; additive and
default-safe; and `non_poolable_with` / `cadence_generation` carry the same standing gap from M-4,
so this is a harness-report contract gap rather than a new inversion. **WARN, close before the
baton**, alongside WARN-1.

### INFO-1 — the P-5 walk's new half has no runtime non-vacuity guard

`effects_total = kit_effects + mob_effects`; **`gd_nova_blocks` is excluded**. H-B-5's hard refusal
therefore does not cover the nova half — the half added *precisely because* the walk had a blind spot
there. If `GD_NOVA_SKILL_KEY` were renamed, the manifest would record `gd_nova_blocks: 0` beside
`clean: true` and `effects_total: 76`, which is the vacuous-pass shape §1.2's own argument forbids.
Pinned in tests (`test_wr1_battery_arms.py:199` asserts `== 1`) but **not at runtime — and the
manifest is what travels.**

### INFO-2 — T-M6-11's predicate is a literal-string match

It catches the exact stale entry and misses rewordings — I tried *"trace has no crit label"* and
*"crit is not surfaced in the trace"*: both **MISSED**. Same guard-softness class as `m4to9`'s
WARN-C. The rule is honoured and the artifact is correct; the guard is narrow. It also reads only
the *report*'s `named_absent` — the trace header is covered derivatively via T-BAT-13
(`rep["named_absent"] == named_absent(with_nova=True)`) and a shared list object, which is adequate
but indirect.

### INFO-3 — the statistics driver has no `argparse` and no documented `--recompute-only`

`main(argv=None)` parses flags by `in argv` membership. `--recompute-only` is the only route to a
second statistics pass once C-5 protects the legs, and it appears in no help text and in neither
note. It is load-bearing for WARN-1's fix path.

---

## §5 — WHAT THIS LANDING DID WELL (on the record, because it is the pattern to repeat)

1. **The HALT held falsifiably.** H-B-2 was written into the math note §7 *before* any cell code,
   pre-flighted deliberately so a 300-fight run would not discover it at fight 200, and when it
   fired the cell banked **nothing**, self-cleared **nothing**, and did **not** reach for
   `--arm-freeze-shatter`. The cell-boundary discipline was tested and survived.
2. **Two errata banked in place with lineage rather than silently rewritten** (§2.4's over-strong
   multiset pin; §10.2's two wrong predictions) — including one where the author's own note was the
   thing falsified.
3. **The join was wrong first, and the author's own test caught it.** The lethal-clamp fallback let
   a 40.0 mob hit steal a 414.80 crossing; rebuilt two-pass, with both residual failure modes
   RAISING rather than guessing.
4. **The estimator was not re-chosen at the one moment it would have paid.** Re-picking p99 at
   §14.1 would have lowered a number that currently clears its predicate. It was left alone and the
   decomposition was published instead, loudly, with a warning addressed to the grader.
5. **The vacuous-seed trap was found and named:** 8 of 30 seeds produce zero nova crossings
   (74000800 among them) — I measured 16 of 60 boss fights at zero, confirming it. A nova test
   pinned to a nova-free seed passes vacuously forever.

---

## Action

- [ ] **🛑 gamora — BLOCKING, before the conductor grades:** add
      `src/reincarnated/simulation/wr1_battery_probes_2026_07_29.py` to `_DOOR_ALLOW_LIST`
      (`tests/test_bq3_calibration_override_door.py:503`) with a written justification in the class
      of the existing `kitcal_g5_harness.py` entry — measurement driver; no season, no convergence
      loop, no endgame-BC batch; artifacts to `simulation/output/`. Then re-run the guard and confirm
      the failure-NAME diff is empty. **No battery re-run required; no banked number moves.**
- [ ] **gamora — before baton emission:** resolve the statistics stamp (WARN-1) — either re-run
      `--recompute-only` from the committed tree so the artifact stamps its true producer, or correct
      cell note §8 + charter §8.18 and record the `-dirty` detector's untracked-file limitation.
- [ ] **gamora — before baton emission:** MIGRATION.md entry for `wave_regime`,
      `mitigation_model`, `p5_freeze_shatter` on the harness report (WARN-3, ADR-004).
- [ ] **gamora — may ride:** correct the "same ratio on every tier / pooling moves nothing" sentence
      (WARN-2); fold `gd_nova_blocks` into H-B-5's runtime non-vacuity refusal (INFO-1).
- [ ] **gandalf (conductor) — at G-A:** the grading stance is **endorsed**; consider the §2(d)
      bracket-construction refinement, and take endpoint **arm B's 1.1350** into the record as the
      third independent corroboration that the gear step is 1.1350. Do **not** switch to the
      max estimator to reach it.
- [ ] **gandalf (conductor) — verification clause DISCHARGED:** no graded claim in `m12`,
      `m3-m12b` or `m4to9` quoted a magnitude or outcome from the 1.667× paths (§2(b)). Nothing to
      retract.
- [ ] **Matt:** no decision required *unless* the conductor disputes BLOCK-1. Nothing here exceeds
      seam authority; no ADR is implicated; no locked decisions-log entry is in conflict. BLOCK-1's
      remedy is the guard's own prescribed act and is gamora's to perform. The BQ-3 containment
      boundary Matt ratified 2026-07-28 is **not** breached in substance — only its
      declaration-of-intent record is missing.

---

## References

**Commits reviewed** (`~/Games/reincarnated-engine`): `2594bbb` · `d38e00d` · `5f830d3` · `cf99b5d` ·
`d4cc2dc` · `7f77ea0` · `05a294f` · `98d3891`

**Engine files read:**
- `src/reincarnated/simulation/spatial_gauntlet/kitcal_g5_harness.py`
- `src/reincarnated/simulation/spatial_gauntlet/kitcal_g5_scenarios.py`
- `src/reincarnated/simulation/spatial_gauntlet/spatial_resolver_adapter.py`
- `src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py`
- `src/reincarnated/simulation/wr1_battery_probes_2026_07_29.py`
- `src/reincarnated/simulation/wr1_battery2_2026_07_29.py`
- `src/reincarnated/simulation/MIGRATION.md`
- `src/reincarnated/simulation/math/wr1-battery-ga-gb-m8a-2026-07-29.md` (§1–§14, whole)
- `tests/test_bq3_calibration_override_door.py` · `tests/test_wr1_battery_arms.py` ·
  `tests/test_wr1_battery2_a_dmg1_grain.py` · `tests/test_wr1_m6_crit_labelling.py` ·
  `tests/test_wr1_m12_gd_mitigation_nova.py`

**Banked artifact reviewed:**
`src/reincarnated/simulation/output/kitcal_g5/wr1_battery_2/` — three leg reports, 450 traces,
`wr1_battery2_statistics.json`

**Collaboration-repo inputs:**
- `agentic_orchestration/gandalf/notes/2026-07-28-wr1-wave-relay-run-charter.md` §8.12, §8.16–§8.18
- `agentic_orchestration/gamora/notes/2026-07-29-wr1-battery.md` (§0–§10)
- `agentic_orchestration/legolas/notes/2026-07-28-kitcal1-sustain-decomposition.md` §14.10
- `agentic_orchestration/qa/findings/2026-07-29-gate2-gamora-wr1-m4to9.md` (baseline)

**Reviewer artifacts** (ephemeral, `/tmp`): `jr_wr1_g2c_regression.sh` · `jr_wr1c_reg_meta_jr.txt` ·
`jr_wr1c_after_names_jr.txt` · `jr_wr1_after_98d3891.txt` · `jr_bat_cmp.py` · `jr_p5_probe.py` ·
`jr_ga_recompute.py` · `jr_167_probe.py` · smoke out-dirs `jr_d_step0` / `jr_d_plumb` / `jr_d_tip`.
Worktrees `/tmp/jr_bat_step0`, `/tmp/jr_bat_plumb`, `/tmp/jr_bat_tip` removed at close.

---
---

# ADDENDUM — INDEPENDENT SECOND PASS (jack-ryan, 2026-07-29, same date, later session)

**Why this exists.** The WR1-G2-BATTERY cell was re-dispatched on the belief that it had been
declared launched in charter §8.18 but never spawned. It had spawned; the finding above is its
output, committed at `d9628884`. The second pass ran to completion before that was discovered, on
instruments written independently of both the builder's and the first pass's. **Nothing above is
retracted or amended.** This addendum records (i) that the four named checks now carry a second
independent re-derivation, and (ii) four items the second pass surfaced that the first did not.

**Verdict unchanged: BLOCK, on BLOCK-1.** The second pass did **not** re-run the full regression and
therefore did **not** independently find the BQ-3 guard breach. BLOCK-1 stands on the first pass's
evidence, and its remedy is unchanged. This is itself a data point for Discipline #2: the check that
found the only blocking defect in this range is the one a targeted-suite pass structurally cannot
reach.

## A.1 — What reproduced on a second independent instrument

Re-derived from the 450 banked `replica-frame/v1` traces with a nearest-rank p99 written from the
math note's words, touching neither builder nor first-pass code:

- **G-A, every cell.** boss `207.4000` post (n=2206) / `207.4000` point (n=1828) / `470.8000`
  endpoint (n=1334); ratios `1.0000` / `2.2700`; `ratio_max 1.1350`; mixed_pack `1.0696`;
  trash and champion `1.0000`. `k = ⌈0.99m⌉` = 2184 / 1810 / 1321. All to the digit.
- **The H-B2-6 decomposition.** `235.40/207.40 = 1.1350048` × `470.80/235.40 = 2.000000`
  = `2.270010`. Exact.
- **The geometry claim, in a stronger form than either the note or §2(c) states it.** The
  **per-fight** `(n_1-projectile, n_2-projectile)` crossing profile is **identical across all three
  legs on all 60 boss fights** — not merely equal in total. 14 two-projectile crossings on the same
  seven seeds (`…802, 805, 807, 809, 810, 818, 825`) × both arms, on `pre`, `post` and `endpoint`
  alike. The mitigation regime moves the payload per projectile and nothing about multiplicity.
- **A-DMG-1 liveness.** 25.6027 % / 10.6627 % reproduce; `pytest` on the three touched suites,
  55 passed.
- **M-8a from trace footers.** pre A 0/30 → B 14/30; endpoint A 0/30 → B **2/30**; post 30/30 both.
  Boss win (pre) 14/60 = 0.2333. Worst hit 414.80.
- **§2(b) re-confirmed by a different route.** The battery's own crossing time is `t* = 1.9512 s` on
  every boss crossing in every fight, and the measured crossing radius sits in the `(2.50, 7.90]`
  band that yields 207.40/projectile — so the `r* = 5.617 m` figure quoted from the 1.667× path is
  **corroborated by the battery**, not contaminated by it.

## A.2 — 🔶 WARN-4 (NEW) — the grader-facing "55 %" does not reproduce, and it sits in the G-A path

`H_B2_6_FINDING.boss_decomposition.warning_to_the_grader` reads:

> *"2.2700 clears R-WR1-7's ≥ 1.50 on its face and **55 %** of it is NOT the gear step."*

The same figure appears in math note §723 and gamora note §652 — three sites. It does not derive
under any natural reading:

| reading | value |
|---|---|
| multiplicative share of the gear step (`1.1350 / 2.2700`) | **50.000 %** exactly |
| log share of the rank step (`log 2.0 / log 2.27`) | 84.6 % |
| share of the excess over 1 (`(1.27 − 0.135)/1.27`) | 89.4 % |

Nothing yields 55 %. This is the string the conductor is directed to read at the exact moment of
grading G-A, and the correct statement under the obvious reading is *"half of it is not the gear
step"* — which is if anything a cleaner sentence. **WARN: correct to 50.00 % or define the
denominator in place, at all three sites.** Discipline #1 — a number in the artifact of record
either derives or does not appear. Close with WARN-1 and WARN-3, before baton emission.

## A.3 — INFO-4 (NEW) — `headroom_pct` carries one word and two denominators across artifacts

`A_DMG_1_preflight.headroom_pct` and `a_dmg_1_grain.pin_headroom_pct` carry the
**inflation-tolerance** value (10.6627 % at the endpoint). Math note §9.2's table labels the same
quantity's complement *"margin below 260.50"* = 9.64 %, and the new `gd_mitigation.py` comment uses
the margin convention (*"9.64 % of headroom instead of 20.38 %"*). The math-note table names both
columns and is unambiguous; **the artifact key is not**, and the artifact is what drax reads cold.
Rename or annotate. Cheap; ride it with WARN-4.

## A.4 — INFO-5 (NEW) — "razor-thin, exactly 14" quantified: the flip point is a 4.95 % larger pool

§2(c) correctly calls the endpoint rank razor-thin. The threshold is computable and belongs in the
grading record beside it. With `rank_from_top(m) = m − ⌈0.99m⌉ + 1`:

| m | rank from top | endpoint p99 |
|---|---|---|
| 1200 – 1299 | 13 | 470.80 |
| **1300 – 1399** (banked: **1334**) | **14** | **470.80** |
| **1400** | **15** | **235.40** |

> **A boss received-event pool ~4.95 % larger (1334 → 1400) collapses the endpoint p99 from 470.80
> to 235.40 and the headline ratio from 2.2700 to 1.1350.** One-sided: a smaller pool leaves it
> at 470.80.

This is weaker evidence than §2(d)'s arm-B corroboration (which is an *actual measured instance* of
the same leg reading 1.1350 under a larger pool, and is the better artifact) but it is independent
of it and states the margin as a number. Bank both with the grade.

## A.5 — INFO-6 (NEW) — the anchor's DoT grain is UNRESOLVED at source and should ride with the pin

legolas `2026-07-28-kitcal1-sustain-decomposition.md` carries an explicit open item on the very
field A-DMG-1 is anchored to:

> *"it is not established whether `greatestDamageReceived` is updated by damage-over-time ticks.
> If DoTs register per tick the bound is still per-event; if excluded it covers direct hits only.
> Not resolvable from the corpus; resolvable by one L0 trial against a bleeding enemy."*

The sim-side pin excludes DoT structurally (own event type, §2.2's exclusions), so the handling is
consistent and no defect follows. But the reclassification tightened the pin's grain, and the one
remaining grain question on the anchor is open with a one-trial resolution path. It should travel
with the pin rather than dropping out of the record. Wave-tail candidate, not a baton blocker.

## A.6 — INFO-7 (NEW) — a liveness qualification on the 25.60 % / 10.66 % headroom

All 44 nova crossings per leg occur at **one** geometric configuration: measured from the telegraph
origin, every boss crossing in every fight resolves at `t* = 1.9512 s` at the same radius. The
falsifier's 132 pre-flight crossings are therefore one configuration sampled 132 times, not a sample
over geometry. It is fully live against the thing it is aimed at — payload-model inflation, which is
what the pin exists to catch — and this is **not** a defect. It is a scope statement: the headroom is
a single-configuration measurement and should not be read as a distributional bound. Worth one line
in `a_dmg_1_grain` so a later reader does not over-claim it.

## A.7 — Concurrence on the four named checks

| check | first pass | second pass |
|---|---|---|
| (a) R-WR1-16 reclassification | SOUND / APPROVED | **concur — upheld** |
| (b) §8.17 verification clause | no contaminated claim | **concur — and re-confirmed via the battery's own crossing geometry** |
| (c) H-B2-6 decomposition | re-derived, 2.0000 is the count step | **concur — and the per-fight profile is leg-invariant, stronger than "14 on both legs"** |
| (d) G-A grading stance | honest, if anything under-stated | **concur — rubric-honest in substance** |

On (d) the two passes converged independently on the same refinement: report the pre-registered p99
bracket as the estimator's literal output (`[1.0000, 2.2700]`), and grade the predicate's **intent**
on `1.1350` with the rubric named — rather than stating the grade over a bracket whose two ends are
different objects. The second pass's added reason for that form: a future reader who re-runs the
predicate will compute 2.2700 against `≥ 1.50` and must find a record saying the arithmetic condition
was met and *why it does not answer the owner's question*. Letting the intent grade silently replace
the arithmetic result is the WARN-A failure shape inverted — a record omitting a channel it carries.
The first pass's warning against reaching for the max estimator to obtain 1.1350 cleanly is endorsed
without reservation.

## A.8 — Addendum action (additive to the Action block above; nothing there is superseded)

- [ ] **gamora — with WARN-1 / WARN-3, before baton emission:** correct the "55 %" at all three
      sites to 50.00 % or define its denominator (**WARN-4**, §A.2); disambiguate the
      `headroom_pct` denominator (INFO-4, §A.3).
- [ ] **gamora — may ride:** one line in `a_dmg_1_grain` scoping the headroom as a
      single-configuration measurement (INFO-7, §A.6).
- [ ] **gandalf (conductor) — at G-A:** bank §A.4's flip-point (pool +4.95 % ⇒ 2.2700 → 1.1350)
      alongside arm B's 1.1350 as the fourth corroboration that the gear step is 1.1350.
- [ ] **wave tail:** the anchor's DoT-aggregation grain, one L0 trial (INFO-6, §A.5).
- [ ] **Matt — aware only, unchanged:** no decision owed. BLOCK-1 remains the only gating item and
      its remedy remains gamora's to perform.

**Addendum method:** read-only on the engine. G-A recomputed from the banked traces; nova crossing
multiplicity, radius and timing measured from the traces; `pytest` on
`test_wr1_battery2_a_dmg1_grain.py` (14), `test_wr1_battery_arms.py` (20),
`test_wr1_m6_crit_labelling.py` (21) — 55 passed. No full-regression re-run in this pass. Anchor
provenance read at origin in `legolas/notes/2026-07-28-kitcal1-sustain-decomposition.md` §6.
