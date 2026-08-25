# Finding — 2026-08-25 — S2C pre/post recapture: **my second limb is REFUTED, my falsifier was unfalsifiable, and the seal SURVIVES on a floor I derived myself**

**Reviewer:** jack-ryan
**Severity:** WARN (self-directed) + **INFO** on the seal
**Target:** `reincarnated-godot` pre-fix `s2c12` vs post-fix `s2c12v3`; flake twin `s2c12v3b`
**Developer:** drax (measurement); jack-ryan (the trace under test)
**Principles applied:** 1 (math-before-code), 2 (smoke-gate), 4 (decisions-log as truth), 5 (severity)
**Disciplines cited:** #75 cl. 2 / cl. 7 (proposed, unratified), #79 cl. 1, #80, #80.x (proposed, unratified)

---

## 0. Headline — four dispositions, in the order asked

| # | Question | Disposition |
|---|---|---|
| 1 | Second limb (`gaps move « 0.2069`) | ⚑ **REFUTED.** Not by the Commit A confound — **I derived that confound and it is not there.** Refuted by a dimensional error in my own inference. |
| 2 | Does the seal's status change now? | **NO — and it does not wait for per-mob either.** `L-29(6)` / `R-1.3` **HOLDS, now with a measured flake floor.** Reclassified `OFF-PATH` → **`ON-PATH-INVARIANT`**. |
| 3 | Is per-mob still the decisive test? | ⚑ **NO. It never was.** Mob3 is `UNEVALUABLE-BELOW-FLOOR` in **all four cells** — my control could not go red. **The per-mob numbers also already existed** in both artifacts. |
| 4 | Pre-registration for rows 3–8 | **Filed, § 6, five predictions with falsifiers.** |

**KR stated my prediction accurately and stated drax's numbers accurately.** I re-derived every figure in his table from the artifacts; all match. **Two of his interpretive claims do not survive (§ 5).**

---

## 1. The confound KR offered me — DERIVED, and it is NOT THERE

KR wrote: *"Commit A changed render output BY DESIGN... this may conflate the yaw repair with intended rendering changes. If so, the 84% is not evidence about your trace at all — but that argument needs making, not assuming."*

**He is right that it needs making. I made it, and it fails.** I decline the escape hatch.

Five commits sit between the two corpora. Each is either gated off this path or receipted as a no-op:

| Commit | Change | Reaches this corpus? |
|---|---|---|
| `612c1e3` **Commit A** | caster yaw at 3 sites (`s2a_stage:303` mob yaw was **already correct and not changed**) | ✅ **YES — the only one** |
| `1c4f90f` Commit B | `face_toward()` refactor | ❌ byte-identity receipted 471/472 |
| `689116c` Commit C | `--audience=review` → cathedral | ❌ gated; runner passes explicit `--stage=`, which always wins |
| `1475ed9` **camera pitch** | `CAM_PITCH_REVIEW := -41.0` | ❌ **gated on `--audience=review`** |
| `713f487` mesh_lod | override removed | ❌ my own F-10: shipped default **equals** deleted value |

**The camera chain, link by link:**
1. `s2a_stage.gd:904` — `_cam_pitch()` returns `CAM_PITCH_REVIEW` **iff** `_audience == "review"`, else `CAM_PITCH`.
2. `s2a_stage.gd:173` — `var _audience := "measure"`; set **only** by `--audience=` at `:321`.
3. `run_s2c_rows12.sh` — `grep -c -- "--audience"` → **0**. Flags passed: `--aim --clip --clipfrom --clipto --defensive --element --fx --motion --out --prefix --row --stage`.

**⇒ every frame in both corpora was rendered at `CAM_PITCH = -55.0`, byte-untouched.** drax held that const deliberately — *"the C-3 error class through a sixth door"* — and holding it is exactly what makes this comparison clean.

⚑ **So the delta is attributable to Commit A alone. The convenient answer was available and it is false.**

---

## 2. The flake floor — **I established it, and it is ~4×10⁻⁵ against a signal of 0.1738**

The dispatch § 1 ordered the floor FIRST and it did not exist when KR invoked me — the twin pass (`v3b`) finished at **22:29:58Z**, mid-invocation. So I derived it, from frames, without re-firing anything and without running drax's script.

⚑ **Byte-identity is a STRONGER floor receipt than recomputing SC: identical inputs to a deterministic script give identical statistics by construction.**

Full md5 sweep, all co-named frames:

```
PRE-FIX vs POST-FIX (the delta)    co-named=874  identical=  0  differing=874
FLAKE FLOOR (same code, twin)      co-named=874  identical=873  differing=  1
```

**One differing frame — and it is on a scored arm**, so it does not get waved away:

```
clip_da_cathedral_f0050.png
  differing pixels : 6 of 2,073,600  (0.000289%)
  max channel delta: 1               (i.e. ±1/255)
  bbox             : y[545..586] x[1388..1407]
  max |added-luma| : 0.2126 at a pixel
```

`PAIRS` in `s2c_pair1_reproduction.py:42-47` scores exactly `clip_da_*` / `clip_bl_*`, so `f0050` **is** in the measured set — the `on` arm of `dash_attack/cathedral`, the cell that carries the pooled gap.

**Propagation (disc `n ≈ 1,520 px`, from `h_px ≈ 43–46` → `r = h_px/2 ≈ 22`, `πr² ≈ 1,520`):**

- ΔA at f0050 ≤ 6 × 0.2126 / 1520 = **8.4 × 10⁻⁴** added-luma units
- one frame perturbs two diffs ⇒ ΔS ≤ **1.7 × 10⁻³**
- `S ≥ peak_A = 26.63`; `ΔSC ≈ SC · ΔS/S ≤ 0.6756 × 1.7e-3 / 26.63` = **4.3 × 10⁻⁵**

> ### ⚑ FLAKE FLOOR ≤ 4.3 × 10⁻⁵. MEASURED DELTA = +0.1738. **RATIO ≈ 4,000 : 1.**
> **The measurement is EVALUABLE. The delta is real. `#80` UNEVALUABLE does not fire.**

**drax's § 3.1 ruling is vindicated by its own result.** He argued determinism does not transfer across a code change and demanded a post-fix twin. He was right, and the twin was not free — it found a real, if tiny, nondeterminism the old receipt could not have predicted.

---

## 3. Limb 2 — **REFUTED, and the refutation CONFIRMS the mechanism while convicting the inference**

### 3.1 What I claimed, and the exact error

I sized the on-path residual at *"tens of pixels against a ~1,520 px disc"* and concluded the gap would move `« 0.2069`.

**The 1,520 px figure is correct** (re-derived above). **The residual sizing is correct.** The *inference* is where it dies:

> **`step_concentration` is `pos.max() / pos.sum()` — a SCALE-INVARIANT SHAPE statistic** (`s2c_onset.py:128-139`). Multiply the entire series by any constant and SC does not move.
>
> ⚑ **No bound expressed in units of "pixels out of 1,520" can bound a change in a scale-free statistic.** I compared an amplitude to a disc area and read the ratio as if SC responded linearly to it. **SC does not respond to the perturbation's AMPLITUDE. It responds to its TOTAL VARIATION across the series** — because the numerator is ONE frame's rise and the denominator accumulates over ~30 positive rises in a 61-frame series.

**Transfer function ≈ n/2 ≈ 15–30×.** I carried none of it.

### 3.2 The amplification, quantified from the data

`dash_attack / cathedral / Mob1` — the body that supplies `min(dash)`:

| | pre-fix | post-fix |
|---|---|---|
| SC(added-luma) | 0.50266 | 0.67555 |
| peak A | 33.4068 | 26.6338 |

With `S = M/SC`: the fix removed **≈ 25.6% of the pre-fix sum-of-positive-rises** — `ΔS ≈ 8.55` added-luma units spread over ~30 rises = **≈ 0.29 units per frame**.

**Converting back to pixels:** `0.29 × 1520 / 255` ≈ **1.7 fully-saturated pixels per frame** (≈17 px at 10% contrast).

> ### ⚑ ~2 saturated pixels per frame out of 1,520 moved the sealed gap by 84%.
> **That is comfortably INSIDE the "tens of pixels" bound I wrote. My physics was right and conservative. My inference was wrong by a factor of ~n/2.**

### 3.3 The measured signature confirms the mechanism — including in reverse

Per-body Δ SC(added-luma), pre → post (**derived by me from `per_body`**):

| row / stage | Mob0 | Mob1 | Mob2 | Mob3 |
|---|---|---|---|---|
| dash / arena | **+0.0987** | **+0.2228** | **+0.1564** | −0.0103 *(floored)* |
| dash / cathedral | **+0.0840** | **+0.1729** | **+0.1551** | −0.1895 *(floored)* |
| blink / arena | −0.0073 | −0.0043 | +0.0074 | +0.0003 *(floored)* |
| blink / cathedral | −0.0009 | −0.0013 | −0.0048 | +0.0018 *(floored)* |

**All six evaluable dash bodies ROSE (+0.084 … +0.223). All six evaluable blink bodies barely moved (|Δ| ≤ 0.008). Ratio ≈ 75 : 1.**

`class_gap = min(STEP) − max(RAMP)` (`s2c_onset.py:168-179`). Decomposing the cathedral move:

- `min(dash)` : 0.50266 → 0.67555 = **+0.17288**
- `max(blink)`: 0.29580 → 0.29487 = **−0.00093**
- gap Δ = **+0.17381** ✅ **99.5% of the movement is the STEP arm alone.**

**Why the classes split — analytically, before looking:** dash is a STEP (SC ≈ 0.5–0.74 ⇒ `S ≈ 1.6M`); blink is a RAMP (SC ≈ 0.21–0.30 ⇒ `S ≈ 4M`). Same spurious `δ` gives `SC·δ/S` **~10× smaller** on the ramp. **The gap inherits the STEP arm's sensitivity almost entirely.**

⚑ **And the clincher, which runs the wrong way for any amplitude-based story:** the largest per-frame perturbation in the whole corpus is `blink/arena/Mob2 f0030`, at **28.16** added-luma units (`independent_rederivation.worst_abs_delta_per_frame`). That body's SC moved **+0.0074**. Meanwhile dash bodies took smaller per-frame hits and moved **+0.16**.

> **Perturbation amplitude and SC movement are ANTI-correlated in this data. The transfer function governs, not the perturbation size.** That is not a story I fitted; it is the opposite of what an amplitude account predicts.

### 3.4 One hypothesis of mine that died on the read — reported because it would have convicted me harder

`s2c_dash_attack.gd:10` reads *"anchor : MOVER-BOUND — everything attaches to the travelling body."* If the VFX were **parented** to the yawed mover, my links 3 and 4 (*"world-framed end to end"*, *"write-only"*) would both be false, and the yaw would be read by the scene graph rather than by code.

**It is false.** Every `add_child` in that file (`:567, :584, :594, :601, :629`) attaches to `self`, not `_mover`. Placement is by `global_position` assignment from `_mover.global_position` / `_mover_home` (`:283, :342-346, :372`) — **position reads, never basis reads.** "Mover-bound" is positional, not hierarchical.

**Links 3 and 4 SURVIVE.** Second time this session one of my own hypotheses died on the read, and the second time it died before it left the building.

---

## 4. The seal — **HOLDS. Status does NOT change. Reclassified, not revoked**

**Under `#75` cl. 7 as I proposed it, I ruled this `OFF-PATH`. That classification was wrong.** The correct one is **`ON-PATH-INVARIANT`**: the defect *is* on the causal path — via exactly the one residual I refused to paper over — and the verdict is invariant to it.

**Why the verdict is invariant, on measured grounds:**

1. **Sign preserved in every cell**, pre and post — arena, cathedral, pooled. Zero inversions.
2. **The margin WIDENED**: pooled +0.2069 → **+0.3807.** ⚑ The defect was **SUPPRESSING** the separation, not manufacturing it. **The seal UNDER-claimed.** A verdict that strengthens when its contaminant is removed is in the strongest position available.
3. **The floor is 4,000× below the delta** (§ 2), so both figures are real measurements.
4. `class_gap` is `min − max` — a **no-overlap** criterion. Post-fix, `min(dash) = 0.6756 > max(blink) = 0.2949` in cathedral and `0.7442 > 0.2487` in arena.

This is **outcome 2** in drax's own pre-registered taxonomy (`s2c_prepost_compare.py:20-22`): *"gap survives, MARGIN MOVES MATERIALLY → verdict vs figures split."* **His instrument named the disposition that fired, before it fired.**

### ⚑ What is NOT sealed, and must not be quoted

> **The FIGURE `+0.2069` is now known to be a pre-fix-contaminated UNDERSTATEMENT.** The verdict it supports survives; **the number itself must not be re-quoted as a measurement.** Any downstream artifact citing `+0.2069` as the class gap is citing a contaminated figure and should cite **+0.3807** (post-fix, cathedral/pooled) or say "pre-fix, contaminated."

**Action for KR:** the `PENDING-RECAPTURE` scope I widened *"to every row in which a body appears"* was correct for **which rows the FIX changes** — 874/874 differ. It remains correct. **This ruling discharges rows 1–2 of it.**

---

## 5. Two of KR's interpretive claims do not survive — he asked me to say so plainly

**(a) ⚑ "drax reported per-CELL, not per-MOB… no number exists for [Mob3] yet." — FALSE. The per-mob numbers already existed, in both artifacts, before he asked drax for them.**

- post-fix: `harness_logs/s2c_rows12_2026-08-25-v3v3/pair1_reproduction.json` → `per_body`
- pre-fix: `harness_logs/s2c_rows38_2026-08-25/pair1_reproduction.json` → `per_body` (identical to `harness_logs/s2c_rows12_2026-08-25/pair1_repro.json`)

Both carry all four bodies × two rows × two stages. I built § 3.3's table from them in one call. **This is a third instance of the `#79` cl. 1 shape he flagged against himself — a property asserted about an artifact not opened.** He predicted a third would not surprise him; it did not, and I am recording it because he asked, not to score it.

⚑ **Consequence for routing, which is his:** the dispatch's acceptance criterion 4 (*"per-mob breakdown emitted"*) is **already satisfied by existing artifacts.** drax need not produce it, and the re-analysis he is being held to for rows 1–2 is complete. That may save a dispatch.

**(b) "`SC(coverage)` is the pose-fragile one; the ruled instrument is the robust one." — NOT SUPPORTED as stated.**

| instrument | arena Δ | cathedral Δ | pooled Δ |
|---|---|---|---|
| SC(coverage) — **rejected** | +0.0225 | +0.1813 | +0.1397 |
| SC(added-luma) — **ruled** | **+0.2302** | +0.1738 | **+0.1738** |

**The RULED instrument moved MORE in two of three cells and more in the pooled figure.** It is not the pose-robust one.

**What IS true, and it is a better point than the one he made:** `SC(coverage)` pooled is **negative in BOTH corpora** (−0.141 → −0.0013) — i.e. **the classes never separated on it, before or after.** R-1.1 is vindicated on **separating power**, not on figure-stability.

⚑ **He asked whether this is a founding instance of `#75` cl. 7. Ruling: YES, but of the cl. 7 DISTINCTION, not of "instrument choice determines whether a defect reaches a verdict."** It is the cleanest live demonstration I have of **verdict-robustness and figure-robustness being independent properties** — the ruled instrument has the *less* stable figure and the *only* stable verdict. That is precisely what cl. 7 exists to separate, and I am carrying it into the proposed text as its founding instance. **His instinct was right; his mechanism was not.**

---

## 6. ⚑ PRE-REGISTRATION — rows 3–8 (R-5 fold, R-3 corridor, R-7 shuriken)

**Filed 2026-08-25 before these numbers exist.** `rows38_v3` began 22:29:58Z. **Falsifier attached to each; if it fires, I say so.**

**P1 — sensitivity tracks pre-fix SC, not render change.** Across rows 3–8 cells, `|ΔSC|` correlates **positively** with pre-fix SC. *Falsifier:* Spearman ρ ≤ 0, or ramp-like cells (SC < 0.35) moving more than step-like (SC > 0.5).

**P2 — every row's class-gap SIGN is preserved.** *Falsifier:* any inversion. (This is the only limb of my original three that held; I re-stake it.)

**P3 — movement concentrates in the STEP arm.** For each row, `|Δ min(step)| > 5 × |Δ max(ramp)|`. *Falsifier:* ramp arm contributing > 20% of gap movement.

**P4 — the rows 3–8 flake floor is ≥ 0 but ≪ the delta, and is best measured by md5, not by recomputing SC.** Predict **> 99% byte-identical** on the `v3`/`v3b` twin, with any differing frames being ≤ ~10 px at |Δchannel| ≤ 2. *Falsifier:* > 1% of frames differing, or any frame differing by > 100 px → floor becomes non-negligible and rows 3–8 are UNEVALUABLE per `#80`.

**P5 — if any verdict flips, it will be R-5's fold/hold, not R-3's corridor.** A fold test is a ratio-of-extrema operator and inherits the same `n/2` amplification; a corridor test is an amplitude threshold and does not. ⚑ **A fold/hold flip would NOT refute the fix — it would be the amplification acting on a knife-edge operator, and R-5 would need a stated separating margin before its verdict is evidence.** *Falsifier:* R-3's corridor verdict flipping while R-5's holds.

---

## 7. ⚑ Self-conviction — my falsifier was structurally incapable of firing

**Mob3 is `UNEVALUABLE-BELOW-FLOOR` in all four cells, in BOTH corpora.** Peak added luma: **0.0009, 0.0172, 0.1517, 0.2544** — against `MIN_SIGNAL_FLOOR = 1.0`. `floor_audit` confirms `n_floored: 4`, `n_floored_non_mob3: 0`.

**Mob3 receives no payload signal. It is not a control; it is an empty region.** The instrument says so in its own words (`s2c_onset.py:112-115`): *"Empty region => the criterion CANNOT go red here. UNEVALUABLE, never PASS (#80 cl. 1)."*

> ### I filed *"if Mob3 moves materially, my trace is wrong"* against a body that **could not move materially in either direction**, and I did not check its signal level before staking the ruling on it.

The three Mob3 near-zeros are near-zeros **of nothing**. The one large one (dash/cathedral, −0.1895) is noise-on-noise: `SC` computed on a series whose peak is **0.0017**, i.e. 0.17% of floor. **Neither confirms nor refutes anything.**

⚑ **This is `#80` — and worse, it is `#80.x`, the sub-clause I authored *in the immediately preceding finding*** (`2026-08-25-godot-forward-axis-convention.md` § Q3): *"check whether the correct and incorrect implementations coincide at that value. If they do, the arm cannot go red and its green is not evidence."* **I wrote that about drax's `aim=0` default and then filed a control arm with the identical defect, one ruling later, in the same session.**

**The real control was in the data all along and I did not name it: `blink`.** Signal-carrying (peak 72–99, far above floor), same caster, same corpus, and it moved **75× less** than dash. That is a control with power. Mob3 never was.

**#80.x should be ratified, and this is a second founding instance stronger than the first — because the author of the clause violated it.**

---

## 8. `#75` — the container question I flagged, answered

I asked that someone check whether `#75` was becoming a container if a fourth ruling arrived. **A fourth arrived — this one.** Answer: **do NOT put it in `#75`.**

The failure here is neither instrument-drift (cl. 6) nor subject-drift (cl. 7). It is:

> **⚑ CANDIDATE (unratified, escalated) — a bound is only a bound in the units of the statistic it bounds.**
> Bounding a perturbation's **AMPLITUDE** does not bound its effect on a statistic that integrates **VARIATION**. Before asserting "the defect is too small to move the number," state the instrument's **transfer function** from perturbation to statistic, and show it is O(1). For any ratio-of-extrema statistic over an *n*-sample series (`max/sum`, fold/hold, concentration indices), the gain is **~n/2**, not 1.
> *Founding instance: this finding — ~2 saturated px/frame out of 1,520 moved a sealed class gap 84%, with the physical sizing correct and only the transfer function missing.*

**`#75` stays a rule, not a container. This is a separate shape and belongs at its own number or under `#79`/`#11`, at Matt's discretion.**

---

## Action

- [x] **jack-ryan:** limb-2 disposition — **REFUTED**, confound derived false, dimensional error owned.
- [x] **jack-ryan:** flake floor derived (≤ 4.3e-5) — **seal is EVALUABLE and HOLDS.**
- [x] **jack-ryan:** seal reclassified `OFF-PATH` → **`ON-PATH-INVARIANT`**; status **unchanged, not PROVISIONAL**.
- [x] **jack-ryan:** rows 3–8 pre-registration filed (§ 6), five falsifiers.
- [x] **jack-ryan:** forward-pointer stamp on `2026-08-25-godot-forward-axis-convention.md` — **DONE this session.**
- [ ] **knight-rider:** dispatch acceptance criterion 4 (per-mob) is **already satisfied by existing artifacts** — § 5(a). Routing is yours.
- [ ] **knight-rider / any consumer:** stop quoting **+0.2069** as the class gap; it is a contaminated understatement. Use **+0.3807** or label it pre-fix.
- [ ] **Matt:** ratify **`#80.x`** — now with a second founding instance in which its author violated it.
- [ ] **Matt:** rule on the § 8 candidate (transfer-function/units) — **new number, or fold into `#79`/`#11`. NOT `#75`.**
- [ ] **Matt (carried, unchanged):** `#75` cl. 7, `#75` cl. 2 mandate-limb, `#62` cl. (c).

## References

- `/Users/admin/Games/reincarnated-godot/harness_logs/s2c_rows12_2026-08-25-v3v3/pair1_reproduction.json`
- `/Users/admin/Games/reincarnated-godot/harness_logs/s2c_rows38_2026-08-25/pair1_reproduction.json`
- `/Users/admin/Games/reincarnated-godot/harness_logs/s2c_rows12_2026-08-25/pair1_repro.json`
- `/Users/admin/Games/reincarnated-godot/scripts/s2c_onset.py` (`body_disc` :71-76, `added_luma_series` :88-125, `step_concentration` :128-139, `class_gap` :168-179)
- `/Users/admin/Games/reincarnated-godot/scripts/s2c_pair1_reproduction.py` (`PAIRS` :42-47, `--cap` :66-79, gap assembly :155-200)
- `/Users/admin/Games/reincarnated-godot/scripts/s2c_dash_attack.gd` (:10, :283, :342-354, :372, add_child :567/584/594/601/629)
- `/Users/admin/Games/reincarnated-godot/scripts/s2a_stage.gd` (`_audience` :173/:321/:331, `_cam_pitch()` :904, `CAM_PITCH_REVIEW` )
- `/Users/admin/Games/reincarnated-godot/scripts/run_s2c_rows12.sh`
- Corpora: `~/Library/Application Support/Godot/app_userdata/reincarnated-godot-spike/{s2c12, s2c12v3, s2c12v3b}`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/knight-rider/returns/2026-08-25-jack-ryan-four-dispositions-and-a-prediction-filed-against-a-run-still-executing.md` § 0
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/qa/findings/2026-08-25-godot-forward-axis-convention.md`
