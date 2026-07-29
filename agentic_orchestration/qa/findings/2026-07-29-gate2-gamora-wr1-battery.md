# Finding — 2026-07-29 — WR1-G2-BATTERY (the battery landing, eight commits, two laps)

**Reviewer:** jack-ryan (DEV-MODE, read-only)
**Severity:** **BLOCK** (overall) — per-commit verdicts in §0
> **⚠ STATUS AMENDMENT, 2026-07-29 (added on re-check; the BLOCK text below is left standing, not
> rewritten).** The BLOCK was discharged by engine `7c16fec` and is **LIFTED**. See
> **RE-CHECK VERDICT — PART 1 / PART 2** at the end of this file. Open items after the lift:
> **WARN-4** (conductor's grading lap, charter §8.20/§8.23) and **WARN-5** (new, §R8) — neither gates.
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

---
---

# RE-CHECK VERDICT — 2026-07-29 — WR1-G2-RECHECK-2 (narrow, repair-commit only)

**Reviewer:** jack-ryan (DEV-MODE) · **Target:** engine `7c16fec` (+ `18f2c14` AGENT_STATE),
meta `8da0539d` · `613ec895` · **Developer:** gamora · **Run/cell:** WR1-2026-07-28 ·
WR1-BATTERY-3 · conductor gandalf, charter §8.19–§8.20
**Scope:** BLOCK-1 and WARN-1/-2/-3 only. Everything PASSed in the landing review above stays passed.
**Status of this section:** PART 1 — items 1, 3, 4, 5, 6 CLOSED. Item 2 (full regression)
IN FLIGHT, foreground, appended below on completion. Committed early by design; the first
re-check instance died with its evidence uncommitted.

## Method note

This is a **relaunch**. A first re-check instance died on a stream stall after verifying the
repair guard-diff. Its full-regression process (`/tmp/jr_wr1_g2d_regression.sh`, started
14:10:13Z at `18f2c14`) **survived the instance** and is still running; I killed my own duplicate
rather than run two laps of the same suite concurrently (Discipline #3 — no parallel regens of
the same seed). Its script diffs against **my own** banked name lists from the previous two laps
(`/tmp/jr_wr1b_after_names_jr.txt` = a42d052 baseline 81, `/tmp/jr_wr1c_after_names_jr.txt` =
98d3891 82) **and** against the builder's banked list — three-way, which is stronger than the
brief asked for. Those /tmp artifacts survived; the name diff is therefore a true reviewer-side
diff, not a comparison against the builder's own record.

## §R1 — 🛑 BLOCK-1: **DISCHARGED.**

| check | result |
|---|---|
| repair guard-diff on `tests/test_bq3_calibration_override_door.py` | **14 insertions / 0 deletions** ✓ |
| `_DOOR_ALLOW_LIST` predicate sites | **exactly one** (line 561); definition 503, message 566 ✓ |
| door suite, re-run by me | **39 passed in 9.36 s** ✓ |
| T8 `test_T8_no_production_callsite_enables_overrides` | **GREEN** ✓ |
| deletions anywhere in `7c16fec` | **one, and it is not in the guard** (`_git_hash`'s old return) ✓ |

**The guard was not weakened, and I checked that structurally rather than taking the commit
message's word for it.** Fourteen insertions and zero deletions in that file means no predicate,
no AST sweep and no assert could have moved; the entire diff is one allow-list string plus its
comment. The whole commit carries exactly **one** deleted line, `-    return _h + "-dirty" if
_dirty else _h`, in `_git_hash` — the WARN-1 repair, not the guard.

**The allow-list entry is a deliberate declaration, not a silencing.** It carries: the date and
cell, the Gate-2 finding path and section, the conductor's acceptance, the two call sites named
(`_fight` / `_fight_engine_direct`), the *reason the flag must be on* (it must match the
allow-listed harness or `verify_instrument_fidelity()` is not comparing comparable paths), the
class-membership argument against the existing `kitcal_g5_harness.py` entry (no season, no
convergence loop, no endgame-BC batch, artifacts to `simulation/output/`), and — the line I care
most about — **an admission that it shipped at `cf99b5d` without the declaration and ran two
commits before the full regression caught it.** That is the written act the guard exists to
force. Principle 4, Discipline #9. ✓

## §R2 — WARN-1: **DISCHARGED.**

**(a) SS-1 byte-check — nothing under the banked battery moved.**

```
git diff --name-status 05a294f..HEAD -- src/reincarnated/simulation/output/kitcal_g5/wr1_battery_2/
  -> EMPTY
git status --porcelain            -- src/reincarnated/simulation/output/kitcal_g5/wr1_battery_2/
  -> EMPTY          (454 files tracked; working-tree bytes == HEAD bytes)
git show --stat 7c16fec           -- src/reincarnated/simulation/output/
  -> EMPTY
```

Not one banked byte was edited, added or removed. `git status --porcelain --untracked-files=no --
src/ tests/` is **empty** before and after my work. ✓

**(b) The errata are present where the false claims were made.** Math note **§15** carries a
titled erratum (*"THE 'TWO HASHES, ON PURPOSE' CLAIM IS FALSE"*); cell note §8 erratum landed at
meta `8da0539d`, and §3.1 gained a forward erratum pointer so the first cell's then-true sentence
is not read cold. Both name what falsified them and when — R-WR1-8 discipline, amended in place
with lineage rather than silently rewritten. ✓

**(c) The `_untracked_loaded_source()` detector carries its Discipline #12 declaration** in three
places, each aimed at a different reader: the `_git_hash` docstring (`⚠ SEMANTIC SHIFT,
2026-07-29 … declared, not buried`), MIGRATION.md §4 with a before/after table and a
**FOR STAR-LORD** two-point consumer instruction, and the detector's own docstring carrying the
scoping rationale. The value set is stated unchanged and the "a clean tree stamps exactly what it
stamped before, so no banked artifact is re-interpreted" claim is the right one to have made. ✓

**(d) NON-VACUITY PROVEN BY NEUTERING, not by reading.** I edited
`_untracked_loaded_source()` to `return []` at the top of the body and re-ran the detector test:

```
E  AssertionError: the detector did not see an imported, never-committed module: []
   tests/test_kitcal_g5_harness.py:651
   1 failed in 0.11s
```

Restored from a byte-backup; `git status --porcelain --untracked-files=no -- src/ tests/` empty;
`tests/test_kitcal_g5_harness.py` **31 passed**; no stray probe module left behind. **The test is
live.** ✓

I also record *why* it is live, because the builder's construction is the non-obvious part and it
is the right one: the test **monkeypatches the tracked-modification branch to return clean for its
whole duration**, so every `-dirty` it observes can only have come from the new branch. Without
that, the test would have passed vacuously on the very commit that introduces the repair — any
working tree with an edit in it satisfies the old branch. It then pins **four** states on one
planted file (absent → clean stamp; untracked-and-unimported → still clean, which is what proves
the scoping rule carries signal; imported → `-dirty`; removed → clean again). The
untracked-but-unimported leg is the one that stops `-dirty` becoming permanent and therefore
meaningless. This is a better test than my finding asked for.

## §R3 — WARN-2: **DISCHARGED.**

Second erratum banked in place at math note **§2.4** (line 149), R-WR1-8 class, explicitly
"amended in place with its lineage, never silently rewritten". It reproduces the falsifying
`by_arm` table (endpoint boss arm A 2.2700 / n_pre 540, arm B 1.1350 / n_pre 794), states that
the sentence **was true when written** and names why (the `R2_proxy_resists_low` leg did not exist
as an object until `7f77ea0`), and adds two imprecisions I had not itemised: the A/B split is
**boss-tier only** (`by_arm` is `none` elsewhere, so "every tier" was never the right quantifier),
and pooling **does** move the endpoint figure. It then routes arm B's 1.1350 into the G-A record
as the third corroboration.

**Estimator and pooling rule UNCHANGED — verified structurally.** `7c16fec` touches five files;
`wr1_battery2_2026_07_29.py` and `wr1_battery_probes_2026_07_29.py` are **not among them**. The
one thing that could have been quietly re-picked at the moment a falsification supplied the motive
was not touched. On the record, per §5.4 of the landing review. ✓

## §R4 — WARN-3: **DISCHARGED, and it is the best MIGRATION entry this run has produced.**

Present, dated, cold-parseable, and it does the thing I have now asked for three times:

- **The third recurrence is named as a recurrence, in a table**, with all three occurrences
  (`1e5b136` M-6 `MovementIntent.EVADE` · `3183efb` M-5 `hp_provenance` · `5f830d3` these three
  keys) and the observation that occurrence 3 shipped *inside the very commit sequence whose
  Step-0b existed to repair occurrence 2*.
- **It names the distinction that kept failing to transfer**: *the ADR-004 trigger is "a
  consumer's parse surface gained a key", not "a player-visible number moved"*. That sentence is
  the actual fix; the three key descriptions are the deliverable.
- Each key gets its own **THE ONE THING A CONSUMER MUST NOT DO** line — `piloted_competence_m3:
  null` is a *no-such-door* statement not an unset flag; a regime must not be consumed without
  both grades (`PROXY` armour vs `BRACKET` resists at the same rendered confidence is the hazard);
  `clean: true` must not be read without `counts`.
- **INFO-1 is folded in as a named known limitation** rather than closed — `effects_total`
  excludes `gd_nova_blocks`, so a consumer asserting non-vacuity must check `gd_nova_blocks >= 1`
  itself. Naming it in the consumer contract is the correct disposition for a runtime gap that is
  only pinned in tests.
- §5 "What did NOT change" states the door allow-list entry is *a declaration of an already-existing,
  already-correct call site — no call site was opened or closed by this repair*. Correct, and it
  is the sentence a future reader auditing the containment boundary will need. ✓

## §R5 — WARN-4: **not discharged here, and that is correct. Routing confirmed. One caveat for the grading lap.**

All three sites still read the underived figure — banked artifact
`wr1_battery2_statistics.json:1066`, math note line 777, cell note line 750 (my earlier
digit-only grep missed the spaced `55 %` form; all three are live). Charter **§8.20** routes it:
*"If BATTERY-3 lands without WARN-4, the correction executes in the grading lap BEFORE the baton,
never after."*

**Consistent with my addendum.** §A.8 asked for it *"before baton emission"*; the grading lap is
before the baton. Nothing in the addendum must precede this CLEAR — §A.8 states explicitly that
BLOCK-1 was the only gating item, and INFO-4/-6/-7 were filed as riders. **Nothing to flag as
mis-routed.**

**One caveat the grading lap needs, offered so it is not discovered mid-correction (INFO, not a
gate):** one of the three sites is **inside the banked artifact**, which SS-1 forbids editing.
The correction there cannot be in-place; it takes the same disposition WARN-1 took — erratum in
prose at the point the claim was made, plus the corrected figure in the grading record, with the
banked string left standing and flagged known-wrong. Only the math note and cell note can be
amended directly.

## §R6 — Item 2: full regression — IN FLIGHT

Foreground lap running at `18f2c14` (= `7c16fec` + AGENT_STATE only; `git diff --name-only
7c16fec HEAD` = `[src/reincarnated/simulation/AGENT_STATE.md]`, verified). Result and the
three-way name diff append below. **I am reproducing the suite rather than judging the banked
list sufficient**, because my own baseline name lists survived and the pre-registered criterion
is a reviewer-side diff.

---

## §R6 (COMPLETED) — Item 2: FULL REGRESSION RE-RUN BY ME. **THE NAME DIFF IS EMPTY. CRITERION MET.**

**I reproduced the suite. I did not judge the banked list sufficient** — my own baseline name
lists from the two prior laps survived in `/tmp`, so a true reviewer-side diff was available and
the pre-registered criterion is a reviewer-side diff. Fifth consecutive lap re-run rather than
audited.

```
JR_REG4_START  2026-07-29T14:10:13Z   HEAD = 18f2c14 ( = 7c16fec + AGENT_STATE.md only, verified)
JR_REG4_END    2026-07-29T14:34:36Z   (24 m 21 s, foreground, exit 1 = failures present)
  60 failed, 6042 passed, 3 warnings, 21 errors
  failure_name_count = 81
  tracked-dirty src/ tests/ : [] before AND after
```

**Three-way name diff — stronger than the brief asked for:**

| comparison | names only on the LEFT | names only on the RIGHT |
|---|---|---|
| my `98d3891` lap (82) → my `7c16fec` lap (81) | **T8** (fixed) | **(none)** |
| **my `a42d052` BASELINE (81) → my `7c16fec` lap (81)** | **(none)** | **(none)** |
| builder's banked list (81) → my `7c16fec` lap (81) | **(none)** | **(none)** |

**The middle row is the pre-registered acceptance criterion and it is EMPTY IN BOTH DIRECTIONS.**
My post-repair failure set is **name-for-name identical to my own pre-landing baseline** — not
merely equal in count. The whole eight-commit battery landing plus its repair moved the failure
set by exactly zero names, and the one name it had moved is gone.

| term | my `a42d052` baseline | my `98d3891` lap | my `7c16fec` lap |
|---|---|---|---|
| failed | 60 | 61 | **60** |
| passed | 6004 | 6040 | **6042** |
| errors | 21 | 21 | **21** |
| failure names | 81 | 82 | **81** |
| **name diff vs baseline** | — | NOT EMPTY (1) | **EMPTY** ✓ |

**The arithmetic closes on both movers, and the builder named the one it had mispredicted rather
than leaving it for me.** `6040 + 1 (T8 flips green) + 1 (the new WARN-1 detector test) = 6042` ✓;
`61 − 1 = 60` ✓; `82 − 1 = 81` ✓. The repair brief predicted 6041 on the assumption the stamp fix
would ship untested; it shipped tested, and the cell note states that in those words. **Exactly one
test function was added to `test_kitcal_g5_harness.py` at `7c16fec`** (30 → 31), and **zero test
functions were added to or removed from the guard suite** (25 defs → 39 parametrized cases, both
before and after) — so "+1 new detector test" is verified structurally, not inferred from a count.

**The residual 81 are outside the seam under review, and I checked the composition rather than
taking it:** `test_cycle12_layer4_convergence` 33 · `test_cycle13_wave5_season_generation` 21 ·
`test_cycle12_layer6_t4_wireup` 12 · 15 across ten other files. `grep -Ei
"spatial|kitcal|wr1|g5|bq3"` over the banked list returns **0**. They are the standing pre-existing
set, unchanged since `a42d052`.

### Method caveat, stated because it is mine and not the builder's

I neutered `_untracked_loaded_source()` on disk for the WARN-1 non-vacuity proof (§R2d) during a
**~13-second window, 14:24:49Z–14:25:02Z, which falls inside this lap**. That is my own Discipline
#3 slip and I record it rather than let it be discovered. **Assessed as immaterial, on grounds that
are falsifiable rather than reassuring:** pytest binds `kitcal_g5_harness` into `sys.modules` at
collection (14:10:13Z), so a 13-second on-disk edit cannot reach an already-imported module; the
lap was in its 90 % band (convergence / season-generation suites) throughout the window; the
planted probe module carried the same 13-second exposure and left nothing behind (verified 0 stray
files, `__pycache__` clean). **The falsifier:** any simulation-seam name appearing in my list and
not the builder's would expose it. **My list and the builder's are identical in both directions,
and the builder's lap ran foreground on a clean tree with no such window.** Two independent laps
converging name-for-name is what retires the caveat; the caveat itself does not survive the
convergence, but the record of it should.

---

## §R7 — RE-CHECK VERDICT: **✅ CLEAR**

| item | verdict |
|---|---|
| **BLOCK-1** — door declaration + guard green | **DISCHARGED** — 39/39, T8 green, guard structurally unweakened, declaration substantive |
| **Regression criterion** — empty failure-NAME diff | **MET** — reproduced by me; EMPTY both directions vs my own baseline |
| **WARN-1** — stamp / SS-1 / detector | **DISCHARGED** — SS-1 byte-clean, errata in place, Discipline #12 declared, non-vacuity proven by neutering |
| **WARN-2** — pooling sentence | **DISCHARGED** — erratum with lineage; estimator + pooling rule verified untouched |
| **WARN-3** — ADR-004 entry | **DISCHARGED** — recurrence named and tabled; per-key consumer contracts; INFO-1 folded in |
| **WARN-4** — the "55 %" | **CORRECTLY DEFERRED** — charter §8.20 routes to the grading lap, before the baton; consistent with the addendum |

**The BLOCK is lifted.** Nothing in the addendum must precede this CLEAR. **Conductor is unblocked
to grade** (stance §8.18, now triple-corroborated) → baton → **HOLD at Matt (R-WR1-6)**.

**Two items ride forward, neither gating:**
1. **WARN-4 must execute in the grading lap** per §8.20 — with the caveat in §R5: one of its three
   sites is inside the banked artifact and SS-1 forbids editing it, so that site takes WARN-1's
   disposition (erratum in prose + corrected figure in the grading record; banked string left
   standing, flagged known-wrong). Only the math note and cell note can be amended directly.
2. **The §8.19 process lesson is now evidenced twice over and should reach the run-pattern doc:**
   the only blocking defect in this entire eight-commit range was found by the full regression and
   was structurally unreachable by every targeted pass that looked for it — including my own
   second pass. Discipline #2.

**What I want on the record about the repair itself.** It moved no number, re-ran no fight, edited
no banked byte, and weakened no guard — and I verified each of those four structurally rather than
by reading the commit message that claims them. The two places it exceeded the finding are worth
naming: the detector test's forced-clean construction (which is what stops it passing vacuously on
the very commit that introduces it — a trap I did not warn about and it avoided anyway), and the
MIGRATION entry's recurrence table, which names the pattern rather than just filing the third
instance. **Nothing was self-cleared.**

## Re-check references

**Verified:** engine `7c16fec` · `18f2c14` · meta `8da0539d` · `613ec895`
**Reviewer artifacts** (`/tmp`): `jr_wr1_g2d_regression.sh` · `jr_wr1d_reg_meta_jr.txt` ·
`jr_wr1_after_7c16fec.txt` · `jr_wr1d_after_names_jr.txt` · baselines `jr_wr1b_after_names_jr.txt`
(a42d052) / `jr_wr1c_after_names_jr.txt` (98d3891) · `jr_recheck_harness_BACKUP.py` (neuter/restore)
**Banked list diffed:** `agentic_orchestration/gamora/notes/2026-07-29-wr1-battery-3-regression-failure-names.txt`

---

# RE-CHECK VERDICT — PART 2 (jack-ryan, 2026-07-29, relaunch instance)

**This part completes the section above.** Nothing in PART 1 is retracted. It adds: the full
regression result (item 2), three falsifiers run on the repair rather than read off it, one NEW
WARN found in the repair itself, and one disclosure about my own instrument.

**VERDICT ON `7c16fec`: ✅ CLEAR-with-notes. BLOCK-1 is CLOSED. The overall BLOCK on the
WR1-BATTERY landing is LIFTED.** One new **WARN-5** and one **INFO-8** ride to the conductor's
grading lap beside the known-unclosed WARN-4. Neither gates the baton.

## §R6 — Item 2: FULL REGRESSION — **COMPLETE. The name diff is empty against my own baseline.**

```
JR_REG4_START  2026-07-29T14:10:13Z   HEAD = 18f2c14  (= 7c16fec + AGENT_STATE.md only, verified)
JR_REG4_END    2026-07-29T14:34:36Z   (24 m 21 s)  foreground, -p no:randomly
  60 failed, 6042 passed, 3 warnings, 21 errors
  failure_name_count = 81
  tracked-dirty src/ tests/ : EMPTY before AND after
```

**Three-way diff, all of it reviewer-side:**

| comparison | names only in LEFT | names only in RIGHT |
|---|---|---|
| my `a42d052` baseline (81) vs **`7c16fec` (81)** | **(none)** | **(none)** |
| my `98d3891` lap (82) vs **`7c16fec` (81)** | `…::test_T8_no_production_callsite_enables_overrides` | **(none)** |
| gamora's banked list (81) vs **`7c16fec` (81)** | **(none)** | **(none)** |

**The pre-registered criterion is met exactly.** The diff against my own baseline is empty in both
directions; the diff against the BLOCKed tip is exactly `{T8 removed}`; and nothing else moved.

**The arithmetic closes and identifies every mover.** `6040 → 6042` passed = T8 flipping red→green
(+1) plus one newly collected test, `test_G5_W1_untracked_loaded_source_is_invisible_until_it_is_imported`
(+1). `61 → 60` failed = T8 alone. **No test was deleted, skipped or renamed to make the diff
empty** — the count rises by exactly the one test the repair adds.

**And, separately worth banking: gamora's 81-name list is byte-identical to mine.** Zero difference
in either direction, on a list neither of us saw the other produce. Her banked artifact
`agentic_orchestration/gamora/notes/2026-07-29-wr1-battery-3-regression-failure-names.txt` is a
faithful record. That does not retire the reviewer-side re-run — the diff had to come from a tree
I drove — but it is the first time this run that the builder's regression record has been
independently confirmed name-for-name, and it belongs on the record.

## §R7 — THE THREE FALSIFIERS (what I broke, rather than what I read)

PART 1 established the guard-diff is 14-insertions/0-deletions. That proves nothing *moved*; it
does not prove the guard still *bites*. These do.

**(i) The door is still OPEN at 153/205 — the allow-list is doing the work, not a quiet flag
removal.** Driving `_door_opening_sites()` myself at `7c16fec`:

```
('src/reincarnated/simulation/spatial_gauntlet/kitcal_g5_harness.py', 806)
('src/reincarnated/simulation/wr1_battery_probes_2026_07_29.py', 153)
('src/reincarnated/simulation/wr1_battery_probes_2026_07_29.py', 205)
OFFENDERS (not allow-listed): []
```

Both original sites are still detected and still open. T8 passes **because they are declared**, not
because the containment question was made to disappear. This is the check that separates a
declaration from a workaround, and it is the one I most wanted to make.

**(ii) The next undeclared door still BLOCKS. The entry is not a rubber stamp.** I planted
`src/reincarnated/simulation/_jr_probe_undeclared_door.py` with one `allow_calibration_overrides=True`
call site and re-ran T8:

```
FAILED …::test_T8_no_production_callsite_enables_overrides
E  AssertionError: BQ-3 CONTAINMENT BREACH … Offending sites:
   [('src/reincarnated/simulation/_jr_probe_undeclared_door.py', 2)]
```

Removed; T8 green again. **The guard's reach is intact and file-scoped exactly as designed.** ✓

**(iii) The `-dirty` detector fails BOTH ways when neutered, not just one.** PART 1 neutered it to
`return []`. I ran the other direction too, because a detector that always fires is as useless as
one that never does and only one of those failure modes was pinned:

| neuter | result |
|---|---|
| `_git_hash` no longer consults the detector | **FAILED** — `assert '7c16fec' == '7c16fec-dirty'` |
| detector always returns a hit (permanent `-dirty`) | **FAILED** — the clean-stamp leg, `…'7c16fec-dirty'.endswith` |
| unmodified | **31 passed** (door suite **39 passed** alongside) |

**The test is non-vacuous in both directions.** ✓

## §R8 — 🔶 WARN-5 (NEW) — the detector's REACH IS `simulation/` ONLY, and all three places it is declared say `reincarnated/`

`_untracked_loaded_source()` computes its root as:

```python
_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # .../src/reincarnated
```

`__file__` is `…/src/reincarnated/simulation/spatial_gauntlet/kitcal_g5_harness.py`. Two `dirname`
calls from there land on `…/src/reincarnated/**simulation**` — **not** `…/src/reincarnated`. The
inline comment is off by one directory, and so is every prose statement of the scope: the
docstring says *"Files of ALREADY-IMPORTED `reincarnated` modules"*, the commit message says
*"a module the process imported"*, and MIGRATION.md §4 says *"a module already imported by the
producing process has a file git does not track"* — none of them qualified by package subtree.

**Measured, not inferred.** At `7c16fec`, importing two untracked modules and asking the detector:

```
detector hits: ['../_jr_scope_probe_sim.py']
sees src/reincarnated/simulation/_jr_scope_probe_sim.py : True
sees src/reincarnated/generation/_jr_scope_probe.py     : False
```

**Why it is WARN and not BLOCK.** The defect class WARN-1 named is genuinely fixed: both WR1
drivers live under `src/reincarnated/simulation/`, so the exact failure that produced the false
`7f77ea0` stamp is now caught, which is what the three falsifiers above show. No banked number is
affected. No guard is red. The pre-registered criterion is met.

**Why it is nonetheless a WARN and not an INFO.** It is the same shape as the defect it repairs —
**a record that is false about the code it describes** — and it is filed in a **cross-seam
consumer contract**. MIGRATION.md §4's *"FOR STAR-LORD, the two things that follow"* invites
exactly the over-trust the gap permits: a producer under `export/`, `telemetry/` or `llm/` that
imports a never-committed module will stamp a **clean hash**, and star-lord's record says it would
have said `-dirty`. ADR-004 asks that an entry be parseable cold; this one is parseable cold and
wrong at the edge. Discipline #12 (declare the semantic shift) is satisfied in form; Discipline #9
(attribution clarity) is not yet satisfied in substance.

**Remedy, and it is one line.** Either widen the reach to match the declaration —

```python
_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # .../src/reincarnated
```

— or narrow all three declarations to say `reincarnated.simulation`. **I recommend widening**: the
stamp's claim is *"the code that ran"*, and code that ran from `generation/` or `export/` is code
that ran. The scoping argument in the docstring (loaded module set, not a repo-wide sweep) is
correct and unaffected by which subtree the root names — widening keeps every word of that
rationale true. If widened, the existing test cannot detect the change either way: it plants into
`os.path.dirname(H.__file__)`, i.e. inside `spatial_gauntlet/`, which is under both roots. **A
second plant outside `simulation/` is what pins the declared scope**, and that is the test the
repair is missing.

**Routing:** rides with WARN-4 into the conductor's grading lap. Does **not** gate the baton and
does **not** reopen BLOCK-1.

## §R9 — INFO-8 (NEW, and it is about MY instrument, not gamora's commit)

**`pytest` run inside a git worktree of this repo still imports `reincarnated` from the MAIN tree.**
The editable install is a `.pth`
(`site-packages/_editable_impl_reincarnated_engine.pth`) that appends
`/Users/admin/Games/reincarnated-engine/src` to `sys.path`. Measured inside `/tmp/jr_repair`:

```
H.__file__ = /Users/admin/Games/reincarnated-engine/src/reincarnated/…/kitcal_g5_harness.py
```

A worktree run therefore exercises **main-tree source** for anything resolved by import, unless
`PYTHONPATH=<worktree>/src` is forced (which does take precedence — it is a path entry, not an
import hook). Tests that locate their subject by **path arithmetic from the test file** — T8's AST
sweep is one — do read the worktree correctly, so a worktree run can mix the two.

**What this does and does not disturb here.** Every result in this PART 2 was either (a) taken with
`PYTHONPATH` forced to the worktree, or (b) taken where the two trees are byte-identical in `.py`
(`git diff --name-only 7c16fec 18f2c14` = `AGENT_STATE.md`, a markdown file). The full regression
ran in the main tree, as REG1–REG3 did, which is what makes the baseline comparison
apples-to-apples. **No conclusion in this finding, or in the landing review above, changes.**
Recorded because it is a live trap for any future per-tree claim of the form *"I ran it at commit
X in a worktree"*, and because Discipline #10 (empirical inspection over assumption) applies to the
reviewer's own instruments first.

## §R10 — WARN-4: confirmed NOT claimed closed by `7c16fec`

`git show 7c16fec | grep -n "55 *%\|55%\|WARN-4"` → **no matches.** The repair commit does not
mention WARN-4, does not touch any of its three sites, and makes no claim about it in the commit
message, the MIGRATION entry, or either erratum. **Correct behaviour** under charter §8.20: it is
the grading lap's item, and `7c16fec` neither closes it nor pretends to. Charter §8.23 records the
conductor accepting it as his own erratum, which is the right owner. **No action asked of gamora
here.** PART 1 §R5's caveat (one of the three sites is inside the banked artifact and SS-1 forbids
editing it in place) stands unchanged.

## §R11 — RE-CHECK ACTION

- [x] **BLOCK-1 — CLOSED.** Declaration present and deliberate; door still open and still swept;
      new undeclared doors still blocked; T8 green; door suite 39/39; full-regression name diff
      empty against my baseline.
- [x] **WARN-1 / WARN-2 / WARN-3 — DISCHARGED** (PART 1 §R2–§R4, falsifiers added in §R7).
- [ ] **gamora — WARN-5 (§R8), before the baton, may ride with the grading lap:** widen `_root` by
      one `dirname` to match the declaration (recommended), or narrow the docstring, commit-message
      lineage and MIGRATION.md §4 to say `reincarnated.simulation`. **If widened, add a second
      plant outside `simulation/`** — the present test cannot see this either way.
- [ ] **gandalf (conductor) — grading lap:** WARN-4 as already routed (§8.20/§8.23), with PART 1
      §R5's SS-1 caveat on the artifact-resident site.
- [x] **Matt — no decision owed.** Nothing here exceeds seam authority; no ADR is implicated; no
      locked decisions-log entry is in conflict. The BLOCK I raised is discharged by its own
      prescribed remedy and is lifted on the evidence above.

## §R12 — Reviewer method and hygiene (PART 2)

**Re-run, not audited — the fifth consecutive lap.** The full regression was reproduced in the main
tree, foreground, `-p no:randomly`, and diffed three ways against name lists I produced myself on
the two prior laps. **What I accepted from gamora's banked list: nothing.** It was compared, and it
matched — that is corroboration, not input.

**Read-only on the engine.** No tracked file in `src/` or `tests/` was modified: `git status
--porcelain --untracked-files=no -- src/ tests/` is empty before and after. All three falsifiers
(planted door module, both detector neuters, both scope probes) ran in a detached worktree at
`7c16fec` with `PYTHONPATH` forced to it, restored from byte-backup, and **the worktree was removed
at close**. No engine push. No banked artifact read-modify-written.

**Reviewer artifacts** (`/tmp`, ephemeral): `jr_wr1_g2d_regression.sh` · `jr_wr1d_reg_meta_jr.txt` ·
`jr_wr1d_after_names_jr.txt` · `jr_wr1_after_7c16fec.txt` · `jr_harness_orig.py` (byte-backup) ·
worktree `/tmp/jr_repair` (removed).

**Files reviewed at `7c16fec`** (all five in the commit, whole):
- `src/reincarnated/simulation/spatial_gauntlet/kitcal_g5_harness.py` (`_untracked_loaded_source`, `_git_hash`)
- `tests/test_bq3_calibration_override_door.py` (`_DOOR_ALLOW_LIST`, `_door_opening_sites`, T8/T8b)
- `tests/test_kitcal_g5_harness.py` (`test_G5_W1_…`)
- `src/reincarnated/simulation/MIGRATION.md` (the 2026-07-29 WR1-BATTERY-3 entry, §1–§5)
- `src/reincarnated/simulation/math/wr1-battery-ga-gb-m8a-2026-07-29.md` (§2.4 second erratum, §15)

**Claims spot-verified at source rather than accepted:** `git diff 7f77ea0..05a294f --
spatial_gauntlet/` is **empty** ✓ · the statistics driver's add-commit is **`05a294f`** and the
probes driver's is **`cf99b5d`** ✓ · `statistics_engine_git_hash = "7f77ea0"`, `battery_runs = {}`,
`wall_seconds = 7.0` read from the artifact ✓ · the §2.4 erratum's `by_arm` table reproduces to the
digit from the banked artifact (endpoint boss A `2.2700`/`1.1350`/n=540, B `1.1350`/`1.1350`/n=794;
`pre` both `1.0000`, n=711/1117) ✓ · every non-boss tier's `by_arm` key is `none`, so the erratum's
"boss-tier only" qualifier is correct ✓ · `_git_hash()` has **no hot-loop call site** (report-time
only, 5 sites), so the added `git ls-files` costs one subprocess per run ✓.
