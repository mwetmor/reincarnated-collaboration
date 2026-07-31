# WR3-KITE-COMMIT — ANCHOR-REFIT REPORT (gamora, simulation seam)

**Commission:** R-WR3-36 (Matt-signed 2026-07-30) — the band fork ruled **(c) SPLIT THE OBJECTS**.
**Engine commits (NOT pushed):** `56881b52` (the lap) · `dbb2d6a9` (AGENT_STATE checkpoint)
**Math note:** `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/math/wr3-anchor-refit-2026-07-30.md` (413 lines, §0–§10, written BEFORE the code)
**Cell:** `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/wr3_cell_refit_2026_07_30.py`
**Probe:** `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/notes/wr3_melee_split_probe_2026_07_30.py`
**Artifact (FROZEN):** `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/output/kitcal_g5/wr3_anchor_refit/wr3_anchor_refit.json`
**Tests:** `/Users/admin/Games/reincarnated-engine/tests/test_wr3_anchor_refit.py` (31)
**MIGRATION:** `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` — new head entry (star-lord + drax + galadriel)

---

## §0 — REPRESENTATION DECISION FOR THE SPLIT

**One row, using the mechanism the escorts already exercise. No new mechanism, no new field on the
damage path.**

`mob_dict_from_row` has always built a **two-effect** melee packet when `cold_rider > 0`, and
`cold_rider` is **ADDITIVE, not a fraction** — `slitha_melee_b01` is 39.8 physical **plus** 9.6 cold
= 49.4 total. So the referent composition is expressible with **zero mechanism change**:

```
default (unchanged):  element "cold"      dmg_per_hit = T        cold_rider = 0.0
armed:                element "physical"  dmg_per_hit = phys(T)  cold_rider = cold(T)   phys+cold ≡ T
```

The armed boss packet is now **the same shape as an escort packet**, and a test asserts that
side-by-side rather than describing it.

**REJECTED: a dedicated `phys_fraction` field** consumed by a new branch. It would be a *second way
to say what `cold_rider` already says*, on the one row in the file that most needs to read like the
others — the state-object degeneracy class this run has now met four times (R-WR3-31(6)).

**The interpolation is CHANNEL-LINEAR, not fraction-linear.** The referent supplied two measured
**(phys, cold) pairs**, not a fraction; a fraction is derived, and interpolating the derived object
then re-deriving the channels adds a float round-trip for nothing. Channel-linear also preserves the
total **exactly** at every point by construction (`cold ≡ T − phys`, never independently computed) —
verified for nine values of T including the three sweep points, `BOSS_DMG_DEFAULT`, and both
out-of-band regimes.

**Outside `[43.1, 60.8]` the operator CLAMPS the share — an extrapolation refusal, not a formula.**
The referent measured a composition at two points and none elsewhere, and the pre-referent G-5a
all-tier band (33–67) is still reachable from `--boss-dmg`. Linear continuation would put the cold
share at 33.9 % at T = 67 on no evidence and would go **negative below T ≈ 22.6**. A test asserts the
clamp *differs* from the linear continuation, so the refusal cannot decay into a formula.

**FLAG-GATED, `wr3_melee_split_v1`, default False — and the default is an argument, not caution.**
R-WR3-36(3) authorizes a fixture change *to the ANCHOR*. WR1 battery-2, the WR1 probes, WR2 cell BAT,
the kitcal-G5 harness defaults and the nine clean-ablation cells all call `boss_rows` with banked
figures taken on the 100 %-cold row. Shipping the split as a default would re-base every one of them
on a ruling nobody made — verbatim R-WR3-35(7)'s ratified argument for `BOSS_DMG_DEFAULT`, and with
more force here because the split *does* move numbers. **Ruling owed** on promoting it (§7.1).

**SS-AR-3, the field-semantics hazard, handled at the site:** on a split row `dmg_per_hit` stops
meaning "per-hit damage" and becomes the physical channel (77.4 % of the total at the default). The
total gets its own home, `OppositionRow.melee_total_pre_mit` (`None` on every unsplit row), echoed
into `_kc1_meta` **only when non-None**, carrying a `reader_warning`. That is R-WR3-27(5)'s
prescription applied to a magnitude instead of a `char_level`.

---

## §1 — THE RE-SPLIT, AND THE VERIFICATION — **P-A HOLDS, RESIDUAL ≈ 0**

### 1.1 The operator, at every point the run uses

| T (pre-mit total) | phys | cold | phys share | `0.30·phys + 0.86·cold` |
|---|---|---|---|---|
| 43.1 (sweep lo) | 35.600000 | 7.500000 | 82.599 % | **17.130** |
| **50.0 (`BOSS_DMG_DEFAULT`, the anchor's own)** | **38.699153** | **11.300847** | **77.398 %** | **21.328** |
| 52.0 (sweep mid) | 39.597458 | 12.402542 | 76.149 % | 22.545 |
| 60.8 (sweep hi) | 43.550000 | 17.250000 | 71.628 % | **27.900** |

### 1.2 ⚑ THE FINDING THAT MADE THE VERIFICATION SHARPER THAN THE COMMISSION ASKED FOR

The commission set the target as "land in/near 17.13–27.90, report the residual, decompose it if it
exceeds ~15 %." Deriving the engine's actual path first (math note §3.1) showed the target is not an
independent measurement to be approached:

```
E[delivered per swing] = 0.30·phys(T) + 0.86·cold(T)
```

because `scaling_stat = 0` ⇒ `S = 1.0` exactly, the physical channel never leaves
`gd_taken_physical`'s scale-invariant `d ≤ A` branch (worst case 52.26 against armour 342.36),
`dodge_chance = 0.0`, `block_chance = 0.0`, `crit_chance = 0.0`, and the only stochastic term is the
per-effect `rng_dmgvar ~ U(0.80, 1.20)` with `E[v] = 1.0`.

**And `[17.13, 27.90]` is that same expression on the referent's own pairs:**

```
0.30 × 35.60 + 0.86 ×  7.50 = 10.680 +  6.450 = 17.130   ← the band's LOW end, exactly
0.30 × 43.55 + 0.86 × 17.25 = 13.065 + 14.835 = 27.900   ← the band's HIGH end, exactly
```

So the band is **our own two mitigation operators on the same operands**. I therefore pre-registered
**P-A: residual ≈ 0, falsified above ±3 %** — a bound five times tighter than the commission's ~15 %,
because a 15 % residual would have meant a term on the melee path my derivation did not contain.

### 1.3 MEASURED (probe: `source_id` + `skill_idx == 0`, icearmor OFF, 60 seeds)

| T | phys + cold | predicted | **measured** | residual | before (100 % cold) | overshoot |
|---|---|---|---|---|---|---|
| 43.1 | 35.600 + 7.500 | 17.1300 | **16.9693** | **−0.94 %** | 36.5665 | **2.135×** |
| 50.0 | 38.699 + 11.301 | 21.3285 | **21.1317** | **−0.92 %** | 42.4205 | **1.989×** |
| 60.8 | 43.550 + 17.250 | 27.9000 | **27.6468** | **−0.91 %** | 51.5833 | **1.849×** |

Referent band `[17.13, 27.90]` → **measured endpoints `[16.969, 27.647]`**. `G-MELEE: PASS` on both
clauses (±3 % of the point prediction; endpoints on the band).

### 1.4 THE RESIDUAL, DECOMPOSED

The residual is **−0.92 % ± 0.02, uniform across all three magnitudes**, and it decomposes to exactly
one term: **the finite-sample mean of the per-hit variance draw**, measured at **0.9906** against
`E[v] = 1.0`. At n = 51 melee events the 1-σ band on the mean is `(0.20/√3)/√51 = 1.62 %`, so
**−0.92 % is 0.57 σ — statistically indistinguishable from zero.** Uniformity across magnitudes is
not a coincidence: seed-matched legs reuse the same variance draws.

Every other candidate term is **zero, and enumerated in the artifact** rather than waved at:
attribute scaling (`S = 1.0`), armour branch straddle (52.26 ≪ 342.36), dodge, block, crit, the
outgoing stage operator (measured exempt), and icearmor's cold rider (measured not to reach the path).

### 1.5 ⚑ CORRECTION OWED TO THE STAGE-2c REPORT §4

> **"our engine on the same 43.1 gives 32.40 → our mitigation carries 0.87×, the *other* way"** — **WRONG.**

`0.7517 / 0.86 = 0.8741`, and `0.86` is already the *whole* cold-channel operator with `S = 1.0`.
0.874 is **a sample mean of `U(0.80, 1.20)` over a small event count**, not a model term. Measured on
the shipped 100 %-cold row at n = 51: **0.8508 × pre-mit, i.e. 0.9893 of the model's 0.86 — parity.**

**Consequence: the channel split carries the WHOLE 1.64–1.89× overshoot, not 2.16× of it with a
0.87× mitigation term the other way.** There is no mitigation-model discrepancy between our engine
and legolas's model on this channel. §4's ratio being *perfectly uniform* across three magnitudes was
the tell — a fight-sampled mean is noisy; a seed-matched one reuses its draws.

**Two more comment-claims promoted to measurements while I was in there:**

1. **SS-S2B-3's stage exemption is now MEASURED.** "`boss_melee` must not be scaled again" has been a
   comment since stage 2b. S0_NONE and S2_FULL produce the same per-hit distribution
   (`[31.16, 44.33]` vs `[30.80, 44.45]`).
2. **Icearmor's +28 % outgoing cold does NOT reach the melee** (max delivered 44.334 vs 44.355 — the
   same distribution). It rides the scheduled channels' payload objects, not the generic per-skill
   path. This is *why* the referent's rider-OFF band is the right comparison object, and arming
   icearmor for the channel comparison would have priced a phantom +28 % into the residual.

---

## §2 — ITEM (B): THE F-2 DESIGNATION — BYTE-INERT, AND THE INERTNESS IS EVIDENCED

**No numeric change. Documentation + designation only, exactly as R-WR3-36(2) rules.**

1. **`F2_INFLIGHT_MAX_CORRECTIONS_PER_RING` — RETIRED IN PLACE.** Stays in the tree; `wr3_f2_cap_v1`
   keeps its `False` default; the docstring now carries the full three-leg measurement table, the
   delta **`−0.300 = −0.64 × ΔF2`**, and — deliberately — **the mechanism sentence beside the
   number**: *one corrective read is worse than zero, because the in-flight verb's value is in the
   RE-SOLVING; a clamp on a re-solving verb does not attenuate it, it inverts it.* A bare negative
   delta invites a sign-flip re-reading, and the delta is not the finding.
2. **`F2_INFLIGHT_MISS_RATE` — DESIGNATED**, ships **0.0** until a referent-derived number exists
   (R-WR3-23(5)). At 0.0 its sub-stream draws nothing, so the designation is byte-inert in RNG
   consumption as well as in value.

**Byte-inertness evidence (asserted, not inspected):**

| check | result |
|---|---|
| mob-dict digest, bare build, this tree vs `HEAD` | `424d9c11046dbc78` == `424d9c11046dbc78` |
| mob-dict digest, armed-2b build, this tree vs `HEAD` | `4a035afc7872bf72` == `4a035afc7872bf72` |
| clean-ablation **PREDICATE R** (9 arm × leech cells) | **PASS 9/9, to the last digit** |
| the refit cell's own seed-matched *before* leg vs the banked stage-2c battery of record | **17/17 comparable keys identical, digit for digit** |

That last row is the strongest form available: `H1 = 0.9666666666666667`,
`intake = 426.64606612040126`, `duration = 34.75000000000023`, `leech_healed = 10807.324925472774`
— re-derived on the post-refit tree, not quoted from the banked report.

Four tests pin the designation, including a **whitespace-normalised, case-insensitive** source scan
for the magnitude *and* the mechanism sentence, so a re-wrap cannot break it and a deletion still can.

---

## §3 — DECLARED-VS-ACTUAL DIGEST MOVEMENT (BQ-3: declared, not discovered)

Math note **§6 was written before the run**. Reproduced here against what happened.

### 3.1 DECLARED TO MOVE — and the mechanism was declared with it

**SS-AR-2:** the split takes the melee from **one** damage effect to **two**, adding one
`rng_dmgvar` draw, one `did_hit` draw and one crit draw per boss swing. **An RNG-stream shift is
TOTAL, not local** — the fights diverge from tick one.

| quantity | before (seed-matched, same process) | ANCHOR | Δ |
|---|---|---|---|
| H1 | 0.967 | **1.000** | +0.033 |
| mean intake | 426.646 | **384.011** | −42.636 |
| mean duration | 34.750 s | **36.107 s** | +1.357 s |
| per-seed win vector | 29/30 (loss on seed +2) | **30/30** | 1 seed flipped |
| wave casts / hits | 74 / 13 | 77 / 15 | moved |
| blizzard casts / hits / slows | 59 / 26 / 26 | 60 / 25 / 25 | moved |
| icearmor casts / up-ticks / total-ticks | 30 / 3630 / 10395 | 30 / 3630 / **10802** | total-ticks moved |
| leech healed / capacity | 10807.3 / 18744.8 | 10158.2 / 18909.0 | moved |

Everything in the declared set moved; nothing outside it did. **The direction is the one the
fidelity fix predicts**: our melee was ~2× over the referent, so making it referent-faithful makes
the boss *less* dangerous — intake −10 %, and the anchor now wins every seed.

### 3.2 DECLARED NOT TO MOVE — PREDICATE R, and exactly what is claimed

> **Every WR3 cell EXCEPT the anchor's split leg reproduces, because the split is reachable only
> through a keyword argument no other call site passes.**

* **Production combat digests** — unreachable: nothing in production calls `boss_rows`' new
  parameter, and off the flag the mob dict is byte-identical *including* `_kc1_meta` key-for-key
  (the split declaration is **ABSENT**, not `None`).
* **The nine clean-ablation arm × leech cells** — re-run: **PREDICATE R PASS 9/9 to the last digit.**
* **The banked stage-2c battery of record** — re-derived by the cell's own before-leg: **17/17.**
* **WR1 battery-2 / WR1 probes / WR2 cell BAT / kitcal-G5 harness defaults** — all call
  `build_scenarios` without the keyword; pinned by a test that the trash/champion/mixed_pack tiers
  are byte-identical *even under the armed flag*.

> **WHAT CANNOT BE CLAIMED, stated precisely:** no figure taken from a split-armed fight can be
> expected to reproduce, and **there is no partial-reproduction claim available for them**. A cell
> that reproduced *some* split-armed figures would mean the flag was not doing what SS-AR-2 says.

### 3.3 THE OTHER SEMANTIC SHIFTS, DECLARED BEFORE IMPLEMENTATION

* **SS-AR-1 — the melee moves from the UNAVOIDABLE branch to the AVOIDABLE one** for 72–83 % of its
  magnitude. The resolver's physical branch carries a `did_hit` gate and the `incoming_attempts` /
  `evasion_misses` BC counters; the elemental branch carries none. **Numerically inert today**
  (`dodge_chance = 0.0` ⇒ `did_hit(1.0, 0.0)` always lands) and **mechanically live the day a
  player-side dodge value enters the BQ-3 door.** The escorts already behave this way.
* **SS-AR-4 — BC-signal denominators move on armed fights:** `incoming_attempts` gains one per boss
  swing (it gained none before) and `premitigation_damage` accumulates over two effects. A units
  change, with the flag as the discriminator.

---

## §4 — THE RE-BATTERY: ANCHOR MEASUREMENTS + THE GATE TABLE

**Arm, unchanged per R-WR3-35(7) / R-WR3-36(4)(C):** `S2_FULL` × Veteran own-stage (×1.40) · cell of
record cl13/r4 via the cl18/r5 fixture · leech 0.05 `attack_only` · F-2 OFF · icearmor cycling ·
`boss_dmg_per_hit` 50.0 · `R2_proxy` · 30 seeds, `BASE_SEED 74000800+i`.
**The single delta is `wr3_melee_split_v1 = True`.**

### 4.1 ANCHOR MEASUREMENTS — **NO BAND VERDICT** (R-WR3-36(1))

```
H1 boss win rate        1.000       ← MEASUREMENT of the referent world
mean boss duration     36.107 s     ← MEASUREMENT of the referent world
mean intake            384.011 HP = 50.6 % of the 759 pool
per-seed wins          30 of 30
```

The cell **has no `_band()` helper and cannot grow one** — a test asserts the string `"IN BAND"` does
not occur in its source, and that the detached bands are carried as provenance only. *Emitting
`"band": "above"` beside a measurement that has no band is how a detached criterion crawls back in.*

`DETACHED_H1_BAND (0.40, 0.60)` and `DETACHED_DURATION_BAND_S (59, 118)` travel in the artifact under
`detached_criteria`, with `detached_to` naming the RDR design lap and the ruling.

### 4.2 THE GATE TABLE — every column names its computing cell (the §8.38 law)

| gate | band / predicate | measured | verdict | cell |
|---|---|---|---|---|
| **H1** boss win rate | *(detached)* | **1.000** | **— ANCHOR MEASUREMENT** | refit §B |
| **G-T′** mean boss duration | *(detached)* | **36.107 s** | **— ANCHOR MEASUREMENT** | refit §B |
| **G-MELEE** *(NEW)* | ±3 % of `0.30·phys+0.86·cold`; endpoints on `[17.13, 27.90]` | **0.94 % max** | **PASS** | refit §A |
| G-W1 wave hit rate | [0.05, 0.45] | 15/77 = **0.1948** | PASS | refit §B |
| G-B1 blizzard drops/cast | [0.0, 0.9] | 25/60 = **0.4167** | PASS | refit §B |
| G-B2 blizzard slows | > 0 | **25** | PASS | refit §B |
| G-I1 icearmor uptime | [0.30, 0.42] | 3630/10802 = **0.3360** | PASS | refit §B |
| G-F2 steers | > 0 on an F-2-**armed** arm | **331** (0 on the anchor arm, by design) | PASS | refit §C |
| G-F2′ capped | steers ≤ rings launched | **41 ≤ 41** | PASS (equality = the clamp) | refit §C |
| G-N3″ worst received event | ≤ A-DMG-1 260.50 | **91.3688** | PASS | refit §B *(instrumented)* |
| G-LEECH healed/capacity | *(diagnostic)* | **0.5372** | — | refit §B |
| **G-BYTE** flag-OFF reproduction | PREDICATE R | **PASS 9/9** + 17/17 | PASS | clean-ablation + refit §B |

### 4.3 ⚑ A DEFECT FOUND IN THE BATTERY-OF-RECORD CELL — THIRD LIVE `get(k, 0)` INSTANCE

`G-N3″` was about to pass on my table off a **0.0000**. It was not a measured zero:

```python
worst = max(worst, float(getattr(fr, "worst_received_event_hp", 0.0) or 0.0))
#                         ^^^^^^^^ SpatialFightResult has 47 fields and NONE of them is this one
```

`getattr`'s default fires on **every fight**, so **the banked stage-2c artifact carries
`worst_received_event_hp: 0.0` on every leg** and the stage-2c gate table's `G-N3″ PASS` against a
260.50 ceiling was graded **on an absence**. (The report §8's `91.369` came from a *different*
instrument — the by-family table — and is unaffected. The artifact's own key was never a measurement.)

This is the **third live instance** of the hazard class R-WR3-35(9) routed to jack-ryan with two, and
it sits **inside the cell that produced the battery of record** — the same shape as the `get(k, 0)`
found in the battery-report *harness* one lap ago.

**Repaired here properly, not patched:** measured off the hit stream via an observability-only sink,
discriminated by `source_is_player` — never by magnitude, never by shape. It returns **91.3688**,
**cross-validating the report §8 by-family instrument to four decimals**. The sink's byte-neutrality
is **proven, not assumed**: a separate seed-matched instrumented leg is run and its H1 / intake /
duration / per-seed vector asserted identical to the uninstrumented anchor (`True`), because the
sink's presence also un-gates the telegraph/decision emission branch and a bare "it's a pure read"
claim is the kind that has cost this run three batteries. **The anchor's own headline figures come
from the uninstrumented leg either way.** A test pins that the `getattr` read cannot return — by
**AST walk, not string scan**, because my first cut tripped on the docstring that quotes the
defective expression in order to explain it.

### 4.4 THE F-2 LEGS ON THE ANCHOR'S OWN FIXTURE

Re-run so the gate table is one fixture throughout. **Predicates only — this does not re-open ΔF2's
attribution, which R-WR3-36(2) closed.**

| leg | H1 (banked, pre-split) | H1 (refit fixture) | intake (refit) | duration | steers / rings |
|---|---|---|---|---|---|
| F-2 OFF | 0.467 | 0.467 | 598.68 (was 608.5) | 24.55 s | 0 / 50 |
| F-2 ON uncapped | 0.933 | 0.933 | 290.44 (was 301.0) | 35.51 s | 331 / 68 |
| F-2 ON **capped** | 0.167 | **0.233** | 717.57 (was 724.1) | 19.09 s | 41 / 41 |
| **ΔF2 uncapped** | **+0.467** | **+0.4667** | | | reproduces |
| **Δ capped** | **−0.300** | **−0.2333** | | | **still inverted** |

The two outer legs' H1 coincide across fixtures while their intake does not (−1.6 % / −3.5 %) — the
melee is a small share of intake in the clean regime and the win/lose outcome did not flip on those
seeds. The **capped** leg is the one that moved, and it moved *toward* zero.

**The inversion is ROBUST to the fixture change.** The clamp softens from −0.64× to −0.50× of ΔF2 on
the referent-faithful melee and stays deeply negative. R-WR3-36(2)'s retirement is corroborated, not
merely carried.

---

## §5 — THE ANCHOR-FREEZE BLOCK

`anchor_frozen: true`, with a provenance block that makes the freeze **a claim about which numbers
later work may quote** rather than a filename convention:

```
ruling                R-WR3-36 (Matt-signed 2026-07-30) — band fork ruled (c) SPLIT THE OBJECTS
acceptance_criterion  PARITY WITH THE REFERENT. The pins-to-three-decimals cross-validation is the
                      PASS; H1 and duration are MEASUREMENTS of the referent world, not gate results.
arm_of_record         S2_FULL × Veteran own-stage (×1.40) · cl13/r4 via the cl18/r5 fixture
                      (mean ratio 0.955, wave residual 6.84 % — a MEAN/DISPERSION statement, false
                      per-channel, per R-WR3-35(4)(b)) · leech 0.05 attack_only · F-2 OFF ·
                      icearmor cycling · boss_dmg 50.0 · R2_proxy · 30 seeds
melee_channel_split   operands lo [43.1, 35.60, 7.50] · hi [60.8, 43.55, 17.25]
                      channel-linear across BOSS_DMG_SWEEP; share CLAMPED outside the band
                      at 50.0 → physical 38.699153 / cold 11.300847 / share 0.773983
frozen_measurements   H1 1.000 · duration 36.107 s · intake 384.011 (50.6 % of pool) · 30/30 wins
melee_parity          referent [17.13, 27.90] → measured [16.969, 27.647] · max |residual| 0.94 %
flag_state            wr3_melee_split_v1 ARMED here, default False tree-wide ·
                      wr3_f2_cap_v1 False (RETIRED IN PLACE) · F2_INFLIGHT_MISS_RATE 0.0
seeds                 base 74000800, n 30, seed_matched true
math_note             simulation/math/wr3-anchor-refit-2026-07-30.md
what_this_freeze_licenses
      "These figures may be quoted as the referent-parity baseline. They may NOT be quoted against
       R-WR3-17's band, which R-WR3-36(1) detached to the RDR design lap."
```

---

## §6 — FULL-REGRESSION NAME-DIFF SWEEP — **81 EXACT · NAME-DIFF 0 / 0**

> **Provenance.** The original commission's sweep **died with its agent** (log
> `/tmp/wr3_refit_sweep.log`, no pytest process behind it). A completion gamora relaunched it
> **from zero, detached** (`/tmp/wr3_refit_sweep_final.txt`, sentinel `EXIT=`, PID 49004), held
> the watch through the `EXIT=` sentinel, and performed the name-diff below. **No partial result
> was carried forward** — the dead log contributes nothing to these numbers.
>
> **Two corrections to the first-pass provenance line, both matters of fact:**
> **(a)** the dead log's "froze at ~55 %" was **block-buffered stdout to a file, not a hang** —
> the relaunched run sat visibly at the same 55 % for minutes at 100 % CPU before flushing, so
> "died at 55 %" describes where the *buffer* stopped, not where the *run* stopped. The prior
> agent's sweep had progressed further than its log shows, and 55 % is not a suspicious site.
> **(b)** the conductor also watched PID 49004 and diffed independently. **Both parties reached
> the identical result on the same artifact** — that is corroboration, and it is worth more to
> the record than either reading alone.

### 6.1 The invocation and the tree it measured

```
cd /Users/admin/Games/reincarnated-engine && python3 -m pytest tests/ -q
    → /tmp/wr3_refit_sweep_final.txt          (no -x — run to the end, per run law)
```

Tree: **`dbb2d6a9`** = `56881b52` (the lap) + a **doc-only** AGENT_STATE checkpoint (`1 file
changed`, `AGENT_STATE.md` — no importable source). Tracked `src/` and `tests/` were **clean**
throughout, and the three refit modules (`wr3_cell_refit_2026_07_30.py`,
`notes/wr3_melee_split_probe_2026_07_30.py`, `tests/test_wr3_anchor_refit.py`) are all **tracked** —
so the SESSION 96 method note (*a sweep started before the source edits measures the old modules out
of `sys.modules` and silently excludes any new test file*) does not apply, and §6.3(3) **proves**
that rather than asserting it.

### 6.2 COUNTS

```
60 failed, 9927 passed, 3 warnings, 21 errors in 1235.29s (0:20:35)     EXIT=1
```

| | baseline (`/tmp/g2c_sweep3.txt`, stage-2c final at `c3887bd3`) | **this sweep** | Δ |
|---|---|---|---|
| failed | 60 | **60** | **0** |
| errors | 21 | **21** | **0** |
| **names (F + E)** | **81** | **81** | **0** |
| passed | 9 896 | **9 927** | **+31** |
| wall | 1 353.03 s (22:33) | **1 235.29 s (20:35)** | −118 s |
| exit | 1 | 1 | — |

### 6.3 THE NAME DIFF — the verdict

```
comm -13 baseline81 refit_names   →  (empty)     ADDED = 0
comm -23 baseline81 refit_names   →  (empty)     GONE  = 0
```

**VERDICT: 0 new / 0 gone. EXACT MATCH against the 81-name baseline. No delta to diagnose, no
allow-list argument owed, no HALT.**

Three checks beyond the bare set difference, because a 0/0 set diff can hide movement:

1. **The FAILED/ERROR partition is identical, kind-for-kind.** Diffing the `(kind, name)` pairs
   rather than the names alone returns empty — **no name flipped `FAILED` ↔ `ERROR`**, which a
   name-only diff cannot see.
2. **The `+31` is fully accounted, and it is a positive result rather than a residual.**
   `pytest tests/test_wr3_anchor_refit.py --collect-only -q` → **31 collected**, and
   `9 896 + 31 = 9 927` **exactly**. So all 31 new tests passed, **and no pre-existing test moved
   across the pass/fail line in either direction** — any such move would break this identity even
   with the name set unchanged.
3. **That same identity is the evidence the new file was actually COLLECTED.** A silently-excluded
   test file is the failure mode the SESSION 96 method note names, and it is invisible to a name
   diff — it makes the sweep *look* clean. `+31` exactly is what rules it out.

### 6.4 The name this lap had specific reason to expect — and did not get

The expectation was **0/0**; per run law **R-WR3-31(8)** the sweep decides. The concrete reason this
lap could have shipped an 82nd name is on the record: it is the **sixth occurrence of the BQ-3-door
class**, and at `127ba505` that class shipped an 82nd name behind a labelled expectation that was
wrong. The difference here is that the two `_DOOR_ALLOW_LIST` entries
(`wr3_cell_refit_2026_07_30.py`, `notes/wr3_melee_split_probe_2026_07_30.py`) were declared **in the
same landing that created the files**, prospectively, rather than being found by a sweep two commits
later.

`test_bq3_calibration_override_door.py` appears **nowhere** in the failure set, so T8's
`offenders = all_sites − allow_listed_sites` came back `[]`. **The sweep CONFIRMED the declaration; it
did not have to correct it** — which is not the same as the declaration having been sufficient on its
own. R-WR3-31(8) stands, and this sweep is why the confirmation is a measurement instead of a second
labelled expectation.

### 6.5 What this discharges — and what it does not

The flag-gated default-False design (§0, §3.2) predicted exactly this: `wr3_melee_split_v1` is
unreachable without a keyword no other call site passes, and item (B) is byte-inert. **PREDICATE R's
9/9 + 17/17 (§2, §3.2) says the DIGESTS do not move; this sweep says the NAMES do not move either** —
two independent instruments, both clean. The landing is regression-clean at the full-suite grain.

**NOT claimed:** nothing here speaks to the split-armed figures, which §3.2 states have no
partial-reproduction claim available. It measures the tree as shipped — flag OFF everywhere except
the anchor cell, which arms it explicitly.

**Artifacts:** `/tmp/wr3_refit_sweep_final.txt` (full run) · `/tmp/baseline81.txt` (the 81 baseline
names extracted from `/tmp/g2c_sweep3.txt`) · `/tmp/refit_names.txt` (this run's 81).

---

## §7 — RULINGS OWED / FORKS HALTed

1. **PROMOTING THE SPLIT TO THE TREE-WIDE DEFAULT.** Today `wr3_melee_split_v1` defaults False and
   only the anchor arms it, on R-WR3-35(7)'s ratified argument. But the referent composition is the
   *faithful* one, and every consumer that keeps calling `boss_rows` unarmed is running a boss whose
   melee is ~2× the referent's post-mitigation. That is a **known-wrong default deliberately
   retained for comparability**, which is a debt, not a resting state. A ruling is owed on when
   WR1/WR2/G-5 re-base. **Not improvised.**
2. **THE STAGE-2c REPORT §4 CORRECTION (§1.5).** "Our mitigation carries 0.87×, the other way" is a
   variance-sampling artifact; our mitigation is at parity and the split carries the whole overshoot.
   The charter's melee decomposition should carry the correction, because the 0.87× is currently
   doing attribution work it cannot do.
3. **THE BANKED STAGE-2c ARTIFACT'S `worst_received_event_hp` IS NOT A MEASUREMENT (§4.3)** — and
   `G-N3″ PASS` in the stage-2c gate table was graded on it. The *report's* 91.369 stands (different
   instrument); the *artifact's* key must not be quoted. Third live instance of the hazard class
   already routed to jack-ryan; the pattern now has an instance inside a battery-of-record cell.
   **The same `getattr` read is still live in `wr3_cell_s2c_2026_07_30.py`** — I did not edit that
   cell, because editing a banked cell would silently re-base its artifact. **Disposition owed.**
4. **SS-AR-1's FORWARD HAZARD.** The boss melee is now dodgeable in principle for 72–83 % of its
   magnitude, inert only because the fixture player's `dodge_chance` is 0.0. The day a dodge value
   enters the BQ-3 door the boss melee starts being evaded. Named for the RDR design lap's lever list.
5. **H1 = 1.000 IS A CEILING, AND A CEILING CARRIES LESS INFORMATION THAN A RATE.** The anchor now
   wins every seed, so H1 has stopped discriminating: any further player-ward change is invisible to
   it and any boss-ward change is only visible once it crosses back under 1.0. **For the RDR design
   lap this argues the anchor's discriminating statistic should be intake or duration, not H1.**
   Flagged, not acted on — choosing the design lap's statistic is not this lap's authority.
6. **NOT HALTed, and worth saying:** the re-split did **not** force a mechanism change beyond the
   melee row. The commission's HALT condition on that point did not trigger — `cold_rider` already
   carried the semantics and the escorts already exercised the two-effect packet.

### Carried forward unchanged from the stage-2c report §10

The ≤5 % caveat under-states the wave (6.84 % here, 9.1 % in legolas's grid); R-WR3-25(4)'s Δkit sign
correction; the "discriminator lost at the seam" pattern; the unpriced Veteran OA/DA/speed/str terms,
all of which bias our boss *weaker* than the referent's — bias, not conservatism.

---

### Key file paths

- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/kitcal_g5_scenarios.py` — `boss_melee_channel_split`, the referent operands, the row, `_kc1_meta`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py` — the F-2 retirement + designation
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/wr3_cell_refit_2026_07_30.py` — the anchor cell
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/notes/wr3_melee_split_probe_2026_07_30.py` — the post-mitigation melee probe
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/math/wr3-anchor-refit-2026-07-30.md` — the math note
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` — the cross-seam entry
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/output/kitcal_g5/wr3_anchor_refit/wr3_anchor_refit.json` — the FROZEN anchor
