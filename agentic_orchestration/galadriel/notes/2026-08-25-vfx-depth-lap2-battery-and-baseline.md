# VFX-DEPTH — the lap-2 measurement battery, its negative-control baseline, and the G-5 floor ruling

**Author:** galadriel (visual perception + UX-similarity steward) · **Date:** 2026-08-25
**Run:** VFX-DEPTH autonomous run, conductor **gandalf** (RUN-CONDUCTOR). Matt away; push-as-you-go Matt-authorized.
**Spec measured against:** `agentic_orchestration/gandalf/vfx-depth-run/lap2-depth-spec.md` § 1 (T-1..T-6) + § 3 (measurement plan)
**Governing rulings consumed:** `agentic_orchestration/gandalf/vfx-feature-registry.md` (I-2, **I-7**) · `agentic_orchestration/qa/findings/2026-08-25-vfx-registry-ratification.md` § 1(b) (FF-08 trip-law amendment) + § Action (the minimum-interval threshold, left to me)

**Instrument:** `agentic_orchestration/galadriel/pipeline/vfx_lap2_battery.py` (new)
**Amended:** `agentic_orchestration/galadriel/pipeline/frame_forensics_depth.py` (FF-08 trip law + minimum-interval rule)
**Result of record:** `agentic_orchestration/galadriel/work/2026-08-25-vfx-lap2/negctl-lap1-barm.json`
**Evidence:** `agentic_orchestration/galadriel/captures/2026-08-25-vfx-lap2-baseline/evidence/`

---

## 0. The headline, before the tables

The battery was built **before** drax's treatments exist, and it was validated on the render the criteria were written to indict. **The pre-registration was: every criterion fails.** It does not.

**Fourteen criteria. Ten correctly FAIL. Four do not, and each of the four is a different kind of problem:**

| | criterion | what it is |
|---|---|---|
| ⚑⚑ | **T-3a** | **DEFECTIVE CRITERION.** Reads **4.07×** against a **2.2×** bar on the render whose own spec line says *"Currently < 1.0."* The premise is false at every percentile. **Building to it buys nothing.** |
| ⚑ | **T-5b** | **DISQUALIFIED ROUTE (I-7).** Reads **0.163** on a render the spec records as *"Currently ≈ 0"* — **2× its own 0.08 bar**, stable across a 3.3× threshold sweep. **INSPECT-ONLY.** |
| ⚑ | **T-3d** | **GUARD, NOT LIFT.** Stable pass (0.829–0.866) already. Legitimate as a no-regression clause; **cannot be evidence that T-3 landed.** |
| ⚑ | **T-4b** | **NOT MEASURABLE IN THIS WINDOW.** 8 intervals against my newly-set 10-interval minimum → **INDETERMINATE**, not FAIL. A build-side consequence for spec **B-1**. |

**And the finding that outranks all four:** my own first pass reported **five** passes. Four of them were an instrument defect of a specific, named shape — **and it is the same shape as the G-5 flag drax handed me in Task 2.** § 7.

---

## 1. Per-criterion instrument status

Ten § 3 rows, fourteen § 1 criteria. All image-space at the ratified pin (1920×1080, `player_lock` k=0.665). No metre enters a bar.

| § 1 criterion | § 3 instrument | status |
|---|---|---|
| **T-1** centroid / principal axis | per-mob ROI silhouette tracking, centroid + 2nd-moment axis fit | ✅ **READY** |
| **T-2** residue | per-mob ROI luminance-threshold differencing vs control + lifetime census | ⚠ **READY (partial)** — the *"zero residue at effect-end + 2.0 s"* clause **awaits B-1's extended window**; reports INDETERMINATE until then |
| **T-3a/b/c** photometry | effect-region percentile luminance + HSV S, annular scene sample as ambient | ✅ **READY** (T-3a's *criterion* is flagged; the *instrument* is sound and tau-stable) |
| **T-3d** apex-vs-leading-edge | angular intensity-peak tracking vs rotation sign and arc span | ✅ **READY** |
| **T-3e** cast light | non-effect-surface differencing, treatment vs control | ✅ **READY** — and this row is why the control render matters: it cannot be passed by an effect merely being bright |
| **T-4a/c/d** lifecycle | luminous-area-vs-time curve + piecewise-slope regime segmentation | ✅ **READY** |
| **T-4b** temporal texture | **delegates to `frame_forensics_depth.CV_timing`** — the trip-flag law's own instrument, per § 3 | ✅ **READY**, ⚠ returns INDETERMINATE on windows this short |
| **T-5a** census | connected-component census + area IQR/median | ✅ **READY** |
| **T-5b** non-repetition | revolution-matched width-profile RMS | ⛔ **INSPECT-ONLY (I-7)** |
| **T-6** aftermath | control-anchored floor-region pre/post differencing + accumulation curve | ⚠ **READY (partial)** — the settle clause has **19 frames (0.317 s)** of aftermath to work in; **B-1 asks for ≥ 1.5 s** |

**Nothing "awaits the control render."** The lap-1 B-arm shipped with a matched `set_vfx_visible(false)` control I had not been told existed — `plk06650_cathedral_fxctl.mp4`, sha256 `f8434eb6…`, identical window, identical camera, **210 frames both arms**, in the same prune receipt. So T-2 and T-3(e) ran for real on the negative control rather than on a synthetic stand-in.

⚑ **And the control arm is GAMEPLAY-IDENTICAL, not merely vfx-dark — `contacts=15` in both arms.** That has a consequence drax needs before he builds T-1: **his flinch lands in `wwcr_stage.gd`, so it will fire in the CONTROL arm too.** A control-*differenced* T-1 would therefore null out by construction and report "no flinch" on a working flinch. The battery measures T-1 **within-arm, against each mob's own pre-contact rest pose**, and uses the control only to seed the ROI. This is not a defect in anyone's work; it is a property of the arms that has to be known before the number is read. *(§ 3's phrasing — "treatment vs vfx-off control" — is what would have led a reader into it.)*

---

## 2. The negative-control baseline

**Artifacts (read-only, untouched):**
`~/Games/reincarnated-godot/harness_logs/wwcr_2026-08-25-w2-bcath/plk06650_cathedral_fxon.mp4` · sha256 `19d5e9c29dbc67cbdaf8100d6362b210568f77487529153e4d49219327bf117b`
`…/plk06650_cathedral_fxctl.mp4` · sha256 `f8434eb643c3e24b5e810e1fdb9a66ebfdc97675977d4e145f5ae6d558c7f44c`
210 frames · 1920×1080 · 60 fps · SEQ 0.20 → 3.70 s · phases read from `render.txt`: RISING f20, SUSTAIN f62–f143, FALLING f144, IDLE f191.
**N = 4** contactable mob silhouettes seeded from the control frame. *(Both blind passes said five; drax verifies N at build time from the `contact` signal per the conductor's amendment, and the battery parameterises on whatever the ROI file holds. Four is what is inside the engagement reach in this frame.)*

| # | criterion | call | measured | bar | expectation held? |
|---|---|---|---|---|---|
| 1 | **T-1** recipient response | **FAIL** | 0 of 4 mobs respond; no centroid or axis excursion clears the bar | ≥8 px / ≥4°, 4 frames, all N | ✅ *statues, exactly as X-2 dim 8 said* |
| 2 | **T-2** attached residue | **FAIL** | 2 of 4 at contact+0.5 s; max 3 simultaneous; clear-at-+2.0 s unmeasurable | ≥120 px², all N, ≥N−1 simultaneous | ✅ |
| 3 | **T-3a** luminance dominance | **PASS** ⚑⚑ | **4.07** (P99) · **2.43** (median pixel) · 61 % of arc pixels already clear 2.2× | ≥2.2 | ❌ **FLAGGED — § 3.1** |
| 4 | **T-3b** internal range | **FAIL** | **2.18** | ≥4.0 | ✅ |
| 5 | **T-3c** saturation | **FAIL** | **0.207** | ≥0.55 | ✅ *and it corroborates the spec's own "≈ 0.24" independently* |
| 6 | **T-3d** apex rides leading edge | **PASS** ⚑ | **0.829** of sustain frames (0.829–0.866 across tau sweep) | ≥0.80 | ❌ **FLAGGED — § 3.3** |
| 7 | **T-3e** cast light | **FAIL** | **0.000** floor lift · **0.000** mob-flank lift | ≥0.08 | ✅ *nothing in this render lights anything* |
| 8 | **T-4a** onset accent | **FAIL** | peak/sustain-mean **0.052**; 0 frames over 1.6× | 1.6× for 6–12 frames | ✅ |
| 9 | **T-4b** temporal texture | **INDET.** ⚑ | **CV 0.144** over **8 intervals** (min 10) · tone 17.1× | CV ∈ [0.45, 1.15] | ⚠ **§ 3.4** — CV corroborates the spec's "≈ 0.10"; the *window* cannot carry the call |
| 10 | **T-4c** decay | **FAIL** | worst drop **100 %** (switches off); tail **0.000 s** | ≤35 %; tail ≥0.35 s | ✅ *literally the "does not break up, it switches off" defect* |
| 11 | **T-4d** phase structure | **FAIL** | **1** regime | ≥4 | ✅ |
| 12 | **T-5a** census | **FAIL** | **5.66** components/frame (IQR/med 5.99 clears its sub-bar; the count does not) | ≥6 and ≥0.5 | ✅ |
| 13 | **T-5b** non-repetition | **INSPECT** ⛔ | **0.163** (sweep 0.163–0.196) | ≥0.08 | ❌ **DISQUALIFIED — § 3.2** |
| 14 | **T-6** aftermath | **FAIL** | **524 px²**, mean \|ΔL\| 0.032; not monotonic (min Δ −502) | ≥2500 px² at ≥6/255 | ✅ |

**Tally: 14 criteria · 10 correctly FAIL · 1 correctly INDETERMINATE · 1 INSPECT-ONLY · 2 flagged PASS.**

---

## 3. The four flags

### 3.1 ⚑⚑ T-3a — the criterion is already passed by the render it was written to indict

**The spec's line is `*Currently < 1.0 — the arc is dimmer than the room.*` The arc is not dimmer than the room. It is four times the room.**

| operand | measured | bar |
|---|---|---|
| P99 of effect region ÷ scene-annulus median | **4.07** | 2.2 |
| **median** effect pixel ÷ scene-annulus median | **2.43** | — |
| fraction of arc pixels already ≥ 2.2× room median | **61 %** | — |
| P99 of effect region ÷ scene-annulus **P99** *(i.e. against the room's bright end, not its median)* | **2.44** | — |

**This is not an extremum artefact and it is not the contact sparks.** I split the mask: the ribbon alone reads 4.11, the non-ribbon components 3.95–4.49 — they agree. It is not a threshold artefact either: **4.106 / 4.114 / 4.131 / 4.139 across a 3.3× tau sweep.** And re-anchoring the denominator to the room's *bright end* still gives 2.44, above the bar.

**The instrument is sound; the premise is false. The re-cut is gandalf's, not mine** — I am flagging, not fixing. What I can supply is where the perceptual reading actually lives, since it is genuinely there: the arc is **thin** (3,272 px, 0.16 % of frame), **flat** (P95/P20 = 2.18 vs bar 4.0) and **pastel** (S = 0.207 vs bar 0.55). **T-3b and T-3c already carry the whole of X-2's "pastel decal" and both fail cleanly.** T-3a as written adds a bar the render clears by 1.85×.

### 3.2 ⛔ T-5b — INSPECT-ONLY under I-7

Spec: *"Currently ≈ 0 — X-2 cites cf_100 vs cf_115 as identical."* Measured on that render: **0.163**, twice the 0.08 bar.

I suspected my own estimator first and replaced it twice. All three fail the same way:

| width estimator | revolution-matched RMS on the negative control |
|---|---|
| radial extent (max − min) | 0.163 |
| robust extent (P95 − P05) | 0.169 |
| mass / arc-length | 0.288 |

and it is not mask-edge quantisation — **tau sweep: 0.192 / 0.163 / 0.172 / 0.196** across 3.3× of threshold. The arc's rendered width genuinely varies ~16 % revolution-over-revolution (the trail's radial extent tracks the channel weight `_w`, which is not constant across sustain).

**I-7 disposition:** *a route disqualified by its own control may inspect but may not carry a bar.* My control returns **2× the bar** on the artifact the bar was written to fail. **The route reports its number and refuses the call.** It is rehabilitable in one of two ways — re-set the bar above the measured floor, or re-cut the operand onto the property X-2's eye actually named — and **both are the spec author's call, not the instrument owner's.** Stamped in the code and in the scorecard output.

### 3.3 ⚑ T-3d — a guard mislabelled as a lift

Stable pass at 0.829–0.866 across the sweep. **Diagnosis:** the current ribbon alpha-fades with age, so the newest sample is the brightest **by construction** — a fading trail satisfies "the apex rides the leading edge" trivially.

**Lower severity than 3.1, and worth stating precisely:** the spec never claimed T-3d currently fails. Re-reading § 1, the *only* criteria annotated with a "currently" are **T-3a, T-3c, T-4b, T-5b, T-6 and T-1's baseline sentence** — and of those, four behave as annotated. **So my pre-registration ("every criterion fails") was itself over-general**, and I am recording that against myself: T-3b, T-3d, T-3e, T-4a, T-4c, T-4d, T-5a carry no such claim. T-3d is a legitimate **no-regression guard** on the two-surface split — *don't put the apex on the tail when you rebuild the ribbon* — and it should be read that way. **It cannot be evidence that T-3 landed**, because it is satisfied before T-3 starts. That distinction matters at the lap gate, where a scorecard of passes will otherwise read as a scorecard of lifts.

### 3.4 ⚑ T-4b — INDETERMINATE, and it is a build-side consequence

The FF-08 route on this clip: **CV = 0.144**, 9 events, **8 intervals**, dominant tone 17.1× median. **The CV independently corroborates the spec's cited "≈ 0.10"** and sits far below the 0.25 trip bar — the metronome is real.

**But 8 intervals is below the 10-interval minimum I set below (§ 8), so the row is INDETERMINATE and is NOT a FAIL.** Discipline #63: unmeasured is not zero, in either direction.

**The consequence is drax's and gandalf's, not mine:** a 1.37 s sustain window at the current ~2.8 events/s cannot supply 10 intervals — it would need ~3.6 s. **The good news is that the treatment fixes its own measurability:** T-4's gust stream is specified at **8–14 events/s**, which yields **11–19 intervals in the existing 1.37 s sustain**. So T-4b becomes scoreable exactly when T-4 lands. **B-1's window extension is still owed for T-4c and T-6 regardless.**

---

## 4. Two instrument defects I found and fixed, and one I found and did not

**Both fixed defects were mine.** Recording them because the first pass reported *five* passes and four of them were not real.

**(a) The effect mask's threshold was floor-governed and the floor was too low.** I derived tau as `median + 8·MAD(|ΔL|)` over the pre-effect window. On a deterministic render pair, **more than half the pixels are byte-identical between arms**, so `median = 0` **and `MAD = 0` exactly** — the derived term vanished and the absolute floor (2/255 = 0.0078) silently became the operative bar. The real inter-arm h.264 noise reaches **P99.9 = 0.041** in the far field. The mask filled with compression speckle: **366 components per frame** (the spec says the render has 1–2), an arc "span" of **358°** on a 126° crescent, and **five criteria passing** on a render written to fail all of them. Replaced with an empirical false-positive control: **1.5 × the worst-frame P99.9 of \|ΔL\| in the far field** — pixels no authored effect reaches. The far field is the null this instrument needed and did not have.

**(b) The mob seeder was admitting cathedral fixtures as mobs.** A centroid-radius gate wide enough to hold a standing skeleton also held two wall braziers at y ≈ 3 px and y ≈ 8 px, driving **N from 4 to 6** — and N parameterises *every* T-1 and T-2 criterion. Re-cut as a **ground-plane test on the foot point** (bbox bottom-centre) against the engagement reach: in a pitched view image-y carries depth, so two actors sharing the ground plane share a foot-point neighbourhood and a wall fixture does not. The two rejects are recorded in the output rather than silently dropped.

**(c) T-6 was marking moving shadow as scouring — fixed, and it is the one worth drax's attention.** A bare `|L_on(t) − L_on(0)|` marked **57,768 px²** of "aftermath" on a render X-1 records as *pixel-identical (c0208 identical to c0001)*. The caster animates and drags a shadow across the tile **in both arms**. Now control-anchored: a mark counts only where the ON arm changed **and the control arm did not change with it**. Same clip, same bar: **524 px².** A 110× difference, entirely attributable to whether the instrument asked the control.

**Not fixed, because it is not mine:** T-3a and T-5b's bars (§ 3.1, § 3.2). **The spec is gandalf's; my channel is the flag.**

---

## 5. TASK 2 — ruling on drax's G-5 flag: the `shake_bar_px` floor

**The flag** (`agentic_orchestration/drax/notes/2026-08-25-vfx-depth-g5-completion-record.md` § 3.2): on all six camnull legs `shake_bar_px` returned **exactly 0.5000** — the derived term `median + 6·MAD` never once exceeded the hardcoded absolute floor, so the detector was **entirely floor-governed**, with `N3-high` at **88 %** of the bar (`hf_max` 0.4419) and zero margin to spare.

**He was right to flag it, he was right not to rule on it, and the flag is bigger than the bar he flagged.**

### 5.1 RULING — the floor STANDS at 0.5 px. Its ROLE is narrowed. Its DOMAIN becomes relief-and-speed-conditional. And the primary discriminant changes.

**Clause 1 — the value does not move.** 0.5 px stands.
- *Downward is refuted:* on every one of drax's six legs the derived term collapsed to **`hf_mad_px` ≈ 0 → the `or 1e-9` fallback**, which is the exact degeneracy the floor was added to close. I have now measured a **seventh** leg — the cathedral B-arm, a genuinely static camera — and it reads `hf_median_px = 0.0`, `hf_mad_px = 1e-09`, `shake_bar_px = 0.5000`, `hf_max = 0.078`. **Seven for seven.** Remove the floor and the bar is 0.000 and every nonzero frame is a quake.
- *Upward is unsupported:* **nothing on the ladder crossed 0.5.** A raise would be fitted to no datum — the same objection that sank `CV == 0.000` at ratification. **A bar moved without a measurement that moves it is taste.**

**Clause 2 — the floor is a DEGENERACY GUARD, and it must say so.** Its own comment says it exists so that a *byte-stable* clip does not produce a zero bar. That is a guard against an estimator collapsing. **Being floor-governed on 7/7 legs means it was silently promoted to the operative PARALLAX-REJECTION bar on clips it was never derived against** — a job no measurement gave it. This is the run's recurring shape once more: *the instrument ran, returned cleanly, and had stopped answering the question.* The role is now named in the output rather than inferred from behaviour.

**Clause 3 — RELIEF-CONDITIONAL, in DOMAIN rather than in VALUE.** This is the part of drax's question that is a real yes.
- The residual is monotonic in relief and rising fast: **0.097 → 0.126 → 0.232 → 0.423** (flat/low/mid/high), roughly doubling per rung above "low", at fixed camera, path and speed.
- `N3-high` at **88 %** of the bar therefore has **about one rung of headroom**, and the speed axis is **entirely unswept** (one `SPEED=`, ~3.8 px/frame).
- **So: the 0.5 px bar is VALIDATED ONLY INSIDE the envelope the ladder actually spans — relief ≤ 10 m and pan ≤ ~4.6 px/frame. Outside it, F7 reports INDETERMINATE, never ABSENT.** Discipline #63, and the same construction I use for FF-08's interval minimum. **An absent-call outside a validated envelope is an unmeasured zero wearing a verdict.**

**Clause 4 — `hf_to_pan_ratio` is PROMOTED to the primary F7 discriminant; `hf_p99` vs `shake_bar_px` is DEMOTED to corroborating.** drax offered this *"from the builder's chair, not as a recommendation."* **I am adopting it, and the reasoning is his own unswept axis.** The absolute residual is a function of the pan rate the clip happens to have; a reference clip has its own camera speed **and its own pose**, so an absolute-px bar cannot travel to it. **The ratio is dimensionless in pan rate and therefore does travel** — it dissolves the speed-axis gap rather than deferring it, which is more than a re-run would have bought.

**The bar, measured rather than chosen:**

| class | `hf_to_pan_ratio` |
|---|---|
| five camnull legs | 0.026 · 0.034 · 0.060 · 0.093 · 0.076 |
| cathedral static-cam (my 7th null) | **0.095** |
| **`P1-shake`, 3.0 px authored** | **1.034** |

Empty band **0.095 → 1.034**, an order of magnitude wide with nothing in it. Geometric centre √(0.095 × 1.034) = 0.313. **Bar set at 0.30** — **3.2× above the loudest null, 3.4× below the positive.** Symmetric in log space, which is the right symmetry for a ratio.

**Carried caveats, binding on consumers:**
1. **The positive side is n = 1.** One amplitude, 3.0 px = **6× the floor**. **Detection sensitivity between 0.5 px and 3.0 px authored is UNMEASURED**, and the bar is provisional above until an amplitude sweep exists. drax's `P1` is the right instrument for it and costs one re-run per rung.
2. **Pose transfer remains conditional**, exactly as drax named it. The envelope is closed for `player_lock` k=0.665 and conditional elsewhere; `--pitch/--fov/--plk` exist to close it per reference pose.
3. `N4-high-spring` (0.076) sits *below* `N3-high` (0.093) — a **lagging spring cam is quieter than a lockstep one**, which is worth knowing before anyone assumes a springy follow-cam is the noisy case.

### 5.2 ⚑ The flag was bigger than the bar — and I proved it against myself in the same session

`hf_mad_px = 0` on 7/7 legs, `div_max_z = 3.4 × 10⁶` from a collapsed divergence MAD on the cathedral clip, **and my own tau tonight: `MAD = 0.0` exactly, floor 2/255 becomes the operative bar, four criteria pass on a render written to fail them.** Three instruments, one defect.

**Standing instrument rule, adopted here and applicable across my seam:**

> **On deterministic render pairs, never derive a bar from `median + k·MAD`.** More than half the sample is *exactly* zero, both robust statistics collapse, and whatever absolute floor sits beside them becomes the operative bar **silently, with no error and no warning**. Derive from a **high percentile of an explicitly-named null region** instead — a far field, a pre-event window, a matched control — and **report the null's own statistics beside the bar** so a floor-governed reading is visible as one.

**`shake_bar_px = 0.5000` on six legs was not a curiosity in drax's table. It was a class defect announcing itself, and it took a second instance in my own hands, hours later, to hear it.** Credit where it is owed: **the builder's flag was the alarm; I was the one who then walked into the same room.**

---

## 6. Registry I-7 compliance — instruments my own controls disqualify

| instrument | disqualified? | disposition |
|---|---|---|
| T-5b revolution-matched width RMS | **YES** — 0.163 vs bar 0.08 on the "≈ 0" render, sweep-stable | ⛔ **INSPECT-ONLY.** Emits `INSPECT`, never PASS/FAIL. Stamped in code and in scorecard output. |
| all thirteen others | no | may carry their bars |

**T-3a is NOT an I-7 case and I want that distinction on the record.** I-7 governs a *route* falsified by its own control. T-3a's route is control-clean and sweep-stable to ±0.02 over 3.3×. **What is falsified is the CRITERION'S PREMISE, which is a different object with a different owner.** Filing a spec defect as an instrument disqualification would have quietly moved the repair from gandalf's desk to mine.

---

## 7. What drax needs before he builds, in one place

1. **The control arm is gameplay-identical** (`contacts=15` in both). **Your T-1 flinch will fire in it.** T-1 is measured within-arm; do not gate the flinch on vfx visibility to "help" the differencing — it would make T-2's residue differencing *worse*, because a mob at different coordinates in the two arms turns its own silhouette edge into a false residue signal. **Keep the arms gameplay-identical. That is what makes T-2 clean.**
2. **B-1's window extension is owed for T-4c, T-6 and T-2's clear-at-+2.0 s clause.** Current aftermath: **19 frames, 0.317 s.**
3. **T-4b needs ≥ 10 event intervals.** Your specified gust rate (8–14/s) supplies 11–19 in the existing sustain window. **Landing T-4 makes T-4b scoreable; not landing it leaves the row INDETERMINATE, which is not a pass.**
4. **Two criteria will not move at the gate no matter what you build** — T-3a is already passed, T-5b's route is disqualified. **Do not read either as a signal about your work.** T-3b and T-3c are the operands that carry T-3's real question, and both fail cleanly with room to move.
5. Run: `python3 vfx_lap2_battery.py --on <fxon>.mp4 --control <fxctl>.mp4 --log render.txt --on-prefix <prefix> --ff08 --out <result>.json`

---

## 8. Housekeeping discharged — the FF-08 action items from ratification

Both landed in `frame_forensics_depth.py`:

- **Trip law amended as ratified.** `CV < 0.25` **trips alone**; spectral tone **demoted to a recorded diagnostic**. The code still carried the old conjunct (`CV < 0.25 AND tone > 1000×`) — **the ruling had been made and the instrument had not been told**, which is precisely the record-vs-state gap this run keeps meeting. Now amended in place with the reasoning inline.
- **Minimum-interval threshold set** — the one jack-ryan deliberately left to me. **Derived, not chosen:** SE(CV)/CV ≈ 1/√(2n); separating the 0.25 bar from the reference corpus floor of 0.449 at 2σ requires relative SE ≤ (0.449 − 0.25)/2/0.449 = 0.222, hence **n ≥ 10 intervals**. Below it the row is **INDETERMINATE and never a PASS**. Recorded consequence: `OURS_ground_slam`'s six events fall below the line, consistent with its having been *inspected* rather than passed.

---

## 9. The Mirror, briefly

The picture that came back tonight was not the one I set the glass for.

I built the battery to indict a render, and the render's arc turned out to be **four times brighter than the room it is in** — while every eye that looked at it, twice, independently, called it a flat pastel decal. **Both are true.** The arc is bright; it is a thin bright thread that touches nothing, lights nothing, and leaves nothing. **Brightness was never the deficit.** Consequence was. The criterion that measured brightness passed, and it passed on the very render whose failure it was written to prove.

And the glass turned on the one holding it. The defect that let four criteria through was the same defect I was in the middle of ruling on for someone else — **a bar collapsing to a floor and the floor governing in silence**, which drax had already found, named, and correctly refused to fix. He handed me an alarm about a camera. It was an alarm about instruments, and mine was ringing while I read his.

**A guard that has quietly become the operative bar is still a guard, and still returns cleanly, and is no longer measuring what its author measured.** That shape has now appeared four times in this run. It will appear again. **The only defence that has ever worked is a null the instrument is made to face before it is trusted** — which is the whole of why this battery met the negative control before it met the treatment.

---

**Signed:** galadriel, 2026-08-25.
**Flagged to gandalf (SPEC-AUTHOR):** T-3a criterion defect (§ 3.1) · T-5b route disqualification (§ 3.2) · T-3d guard-vs-lift labelling (§ 3.3) · T-4b window dependency (§ 3.4).
**Flagged to drax (builder):** § 7, all five.
**Ruled (my seam, Task 2):** § 5 — floor stands, role narrowed, domain conditional, discriminant changed.

---

# T-3(a) re-cut negative control

**Date:** 2026-08-26 · **galadriel** (instrument steward) · **Run:** VFX-DEPTH, conductor gandalf, ledger R-22.
**Criterion under test:** T-3(a) as **re-cut** by the conductor in `agentic_orchestration/gandalf/vfx-depth-run/lap2-depth-spec.md` § 1 T-3, committed `168dbe44`, after the original failed its negative control at `809409a8` (§ 3.1 above).
**Instrument:** `pipeline/vfx_lap2_battery.py` § 3b (`derive_ui_mask`, `t3a_ownership`, `t3a_scene_hot_persistence`, `t3a_row`), new this pass.
**Artifacts:** `work/2026-08-25-vfx-lap2/t3a-recut-negctl-fxon.json` · `…-sanity-fxctl-self.json` · `…-sanity-swapped.json` · full-battery regression `…/negctl-lap1-barm-t3a-recut.json`.

## 10. Disposition

> ## **(a) — lap-1 FAILS. The re-cut is CERTIFIED.**
>
> **Measured ownership on the lap-1 B-arm: `0.1461` — 14.6% against a 75% bar.**
> The pre-registered expectation is **met**. T-3(a) enters the battery and may judge the incoming lap-2 build.

The criterion the conductor re-cut now behaves the way an acceptance criterion is supposed to behave on the render it was written to indict: **it fails, by a wide margin, for the reason the perceptual claim named.** The braziers own the room's bright tail. The arc does not.

## 11. The measurement

Sustain window frames **62–143** (82 frames, harness `state=SUSTAIN`), 1920×1080 @ 60 fps, tau `0.07396` (far-field P99.9 null, carried unchanged from the baseline pass).

| statistic | value | reading |
|---|---:|---|
| **ownership, inclusive (PRIMARY)** | **0.1461** | median over sustain frames of \|top-0.5% ∩ effect\| / \|top-0.5%\| |
| ownership, strict / emissive-core | 0.1407 | misattribution guard; see § 12.3 |
| ownership, exact-rank corroborator | 0.1475 | tie-break-free cross-check |
| ownership, **no UI exclusion at all** | 0.1461 | sensitivity: my UI mask decides nothing |
| frames over the 75% bar | **0 / 82** | not a marginal miss |
| per-frame range | 0.110 → 0.236 | the best frame is a third of the way to the bar |
| **scene-hot persistence** | **0.8293** | 83% of the ON arm's top pixels are *still* top pixels with the effect hidden |

**Four independent estimates land within 0.007 of each other.** The call does not rest on any operational choice I made.

**The scene-hot persistence number is the one to read aloud.** It says the room's bright tail is 83% unchanged by turning the effect on — the arc is not competing with the braziers, it is beside them.

## 12. Operational choices, each one named because each could have gone otherwise

**12.1 Sustain window.** Harness state timeline (`state=SUSTAIN` in `render.txt`), not an inference from the pixels. The spec says *"during the effect's sustain window"*; the harness knows where that is and does not have to be asked. `--sustain LO,HI` overrides for clips without a log.

**12.2 Effect region.** The **same** control-differenced mask the rest of the T-3 family uses — `|L_on − L_ctl| > tau`, 3×3 opened, components ≥ 12 px. *"The effect region"* now means one thing across T-3a/b/c/d. Deliberately **not** a new bespoke mask: a criterion family that means four different things by one phrase is how a scorecard stops being comparable.

**12.3 The inclusive/strict split — the misattribution guard, wired in before it was needed.** The differenced mask contains every pixel the effect **changed**, which includes pixels the effect merely **lit**. The lap-2 spec adds an apex `OmniLight3D` (T-3b). That light can brighten a brazier by a few percent, put the brazier into the differenced mask, and **credit the effect with owning top pixels that are the brazier's** — the exact misattribution the task named as outcome (c). So the pass computes two regions:

- **inclusive** — the full differenced region. **Primary**, because it is the plain reading of *"the effect region."*
- **strict** — pixels where the effect supplies the **majority of the pixel's own luminance**, `(L_on − L_ctl) ≥ 0.5·L_on`. An arc pixel on a dark floor passes trivially; a brazier lifted 7% does not; floor genuinely lifted 0.20 → 0.55 by cast light **does** pass (d/L = 0.64), so the guard discriminates *lit-by* from *near*, not merely *bright* from *dim*.

**If inclusive clears the bar while strict does not, the call is `INDETERMINATE` — not `PASS`.** The guard can only ever **withhold** a pass; it cannot manufacture one. Stated here in advance of any build that could trip it, which is the only time such a rule is worth anything.

**12.4 Top-0.5% selection.** Threshold-based: `T = P99.5(L_on over eligible px)`, set = `{L_on ≥ T}`. **Not exact-rank** — exact-rank breaks ties arbitrarily, and a build that clips its core to white creates enormous tie mass, at which point *an arbitrary tie-break decides the criterion*. The threshold set's true size is reported every frame (**measured 0.5004%** against a 0.500% target; frame max L = 0.835, one pixel at max, **no clipping**) and a `tie_inflation_flag` fires if it exceeds 1.5× target. Exact-rank runs alongside as a corroborator and agrees to 0.001.

**12.5 UI exclusion — derived, over-fired, hardened, and then proved inert.** The discriminant is exact temporal constancy in the **control** arm (a HUD is composited after the 3D pass and does not move; world pixels under a moving camera do). Its validity depends on the camera actually moving, so **camera-motion fraction is reported beside the mask — measured 0.634.**

Raw constancy returned **16,652 px in 3,104 components of median size 1** — coincidentally-static dark world pixels, **not a HUD.** A HUD element is contiguous, so a ≥ 64 px coherence filter was added; that leaves 6,559 px, still world geometry, **all of it dark (median L 0.20, max 0.497) and none of it inside the top-0.5% set.** This venue has no HUD at all — confirmed by eye on frame 120.

**I did not stop at asserting the mask was harmless. The pass computes the whole statistic a second time with no exclusion whatsoever, in the same walk: `0.1461` both ways.** A derived mask that could have been wrong and is *measured* not to be load-bearing is worth more than a mask asserted to be right — and the raw pre-filter count stays in the output so the over-fire is visible rather than quietly absorbed.

**12.6 Degenerate frames are scored, not dropped.** A frame with an empty effect mask reports ownership 0.0 and is flagged, never skipped. Dropping empty frames would let a build that flickers off mid-sustain be scored only on the frames where it was on.

## 13. Instrument sanity — what the estimator does on the FX-off control, and why that is sound

**13.1 `fxctl` against itself** (`--on fxctl --control fxctl`) — the pair with no effect in it.

`ownership = 0.0000` on all four estimates · `degenerate_frames = 82/82`, **flagged** · `scene_hot_persistence = 1.0000` · call **FAIL**.

**This is the sound behaviour and the polarity matters.** A criterion asking *"does the effect own the room's brightest pixels"* must answer **zero** on a clip with no effect. An estimator that crashed there, returned `NaN`, or divided its way to a spurious pass would be the defect. It does none of those: it returns a real number, marks every frame degenerate so a reader can see *why* the number is zero, and the scene-hot persistence reads exactly **1.0** — with the effect hidden, 100% of the frame's top pixels are the room's. **The control tells you who owns the tail when nobody is contesting it: the room does, entirely.**

Note the estimator was made to survive this at all: `seed_geometry` raises on identical arms (*"no effect pixels anywhere"*), so a `--t3a-only` path was added that skips geometry seeding. **A sanity check you cannot run is not a sanity check.**

**13.2 Arms swapped** (`--on fxctl --control fxon`) — a polarity check I added beyond the brief.

`ownership = 0.0001`, strict `0.0000`, call **FAIL**. Here the *mask* is the arc's footprint but the *arm being scored* is the one where the arc is absent, so the region is unlit floor. **The estimator credits a region only for the luminance that region actually has in the arm under test — it cannot be fooled by a well-placed mask.** Effect-region max L drops from 0.820 to 0.502 across the swap, which is the arc's brightness moving with the arc rather than with the mask.

## 14. ⚑ CAVEAT THE CONDUCTOR MUST CARRY INTO THE MEASURE STEP

**The re-cut bar is a joint AREA × BRIGHTNESS bar, and on this venue the AREA term is the binding one. Brightness alone cannot reach it — not even infinite brightness.**

| quantity | value |
|---|---:|
| eligible pixels (UI excluded) | 2,067,041 |
| top-0.5% set size, k | 10,335 |
| pixels the effect must present to own 75% | **7,751** |
| …at a luminance of at least | **L ≥ 0.593** |
| the arc's **entire current footprint**, any luminance | **4,170 px** |
| of which already in the top tail | 1,524 (36.5% of the arc's own pixels) |

**The arc's total pixel count is 4,170. The bar needs 7,751. So if every single pixel of the current arc were driven to pure white, ownership would top out at 4,170 / 10,335 = 40.4% — still barely half the bar.** The shortfall is **5.09×** in top-tail pixels, and the deficit is *extent*, not *intensity*.

Three consequences, and the second is uncomfortable:

1. **T-3's stated implementation guidance does not obviously buy this.** The core/body split, the darkening MIX body, the raised `emission_energy_multiplier` and the apex light are all **value/hue/intensity** instruments. None of them widens the ribbon. The criterion text — *"`emission_energy_multiplier` raised until criterion (a) passes"* — **prescribes a knob that cannot reach the bar it names.**
2. **`TrailRibbonBody` works against T-3(a) by design.** It is specified to **darken** as it ages. Every pixel it darkens below L 0.593 leaves the top tail. **T-3's own body treatment reduces the statistic T-3(a) measures** — the two clauses of a single treatment pull opposite ways, and that is worth the conductor's eye before drax builds, not after.
3. **There is a legitimate route, and it is the rest of the spec.** Shed quanta (T-5), recipient residue (T-2), the onset ring-pop (T-4a) and genuine cast light (T-3e) all add effect-region pixels. If T-3(a) is meant to be reachable, **it is reachable by the lap as a whole and not by T-3 alone** — which makes it a *lap-level* criterion wearing a *treatment-level* label.

**This is a finding about the criterion's reachability, not a defect in it.** The criterion is sound, its instrument is sound, and it fails the lap-1 render for exactly the right reason. **But a bar that its own treatment's guidance cannot reach will read at the gate as "drax did not land T-3", when what actually happened is that T-3 was never the treatment that could move it.** I am not re-cutting it — that is the conductor's desk, and a second unilateral re-cut from me would be worse than the problem. **I am putting the number where it cannot be missed: 4,170 against 7,751.**

Two smaller carries:

- **The 75% figure is venue-coupled.** It is stated against *this* cathedral's brazier population. A darker venue would hand the same arc a much higher ownership for free. If lap-2 renders anywhere but plk06650 cathedral, **the criterion has moved and the number is not comparable.**
- **T-3(a) no longer reads the superseded ratio, but the ratio is still emitted** as `SUPERSEDED_floor_referenced_ratio` in the row's operand (4.11 on lap-1), so a reader comparing laps can see both statistics and see which one was retired.

## 15. Battery regression — the negative control is now clean

Full battery re-run end-to-end with T-3(a) re-wired (`negctl-lap1-barm-t3a-recut.json`):

**11 FAIL · 1 PASS · 1 INDETERMINATE · 1 INSPECT.**

The sole PASS is **T-3d**, which the spec itself now stamps as *"a fading trail passes this by construction — a GUARD, not a lift demonstration."* **T-5b remains INSPECT-ONLY under registry I-7. T-4b remains INDETERMINATE on 8 intervals against its derived minimum of 10.**

**No criterion now passes on the render every criterion was written to fail, except the one documented as passing by construction.** That was not true four hours ago: T-3(a) passed at 4.07× and three other rows passed on a collapsed tau. The battery has met its null and the null no longer clears it.

## 16. The Mirror, briefly

The first cut of this criterion asked whether the arc was brighter than the floor, and the floor was never the competition. The second cut asks whether the arc is brighter than the braziers — and the answer came back with a number I did not expect to be the interesting one.

**The arc is bright. Its hottest pixel reads 0.82 against a room whose hottest reads 0.84. It is very nearly the brightest thing in the cathedral.** And it owns fourteen percent of the light.

**Because it is a thread.** Four thousand pixels of it, in a room of two million, laid down beside braziers that are simply *larger*. Two independent eyes called it *"a flat pastel decal"* and the glass has now said the same thing twice in two different statistics — once as *nothing to compare against*, once as *nothing to compare with*. **The deficit was never luminance. It was never luminance either time.**

And the re-cut inherited that. It measures ownership, ownership is extent, and the treatment it hangs on has no extent knob — **the criterion asks for the one thing its own implementation guidance was not written to give.** That is not the same defect as the first cut; the first cut asked a false question, this one asks a true question of the wrong treatment. **But it is the same shape at one remove: a bar and a mechanism that are not looking at each other.** Fourth time this run.

I have certified it, because it does what a criterion must do — it fails the render it was written to fail, for the stated reason, by five to one. **A criterion can be sound and still be pointed somewhere its builder cannot reach, and saying so now costs one paragraph. Saying it at the gate costs drax a lap.**

---

**Signed:** galadriel, 2026-08-26.
**Disposition:** **(a) CERTIFIED** — T-3(a) re-cut enters the battery; ownership `0.1461` vs bar `0.75`; 0/82 sustain frames over bar.
**Flagged to gandalf (conductor):** § 14 — the area term is binding at 4,170 px against 7,751 needed; `emission_energy_multiplier` cannot reach it; `TrailRibbonBody`'s darkening clause opposes it; the bar is venue-coupled to this cathedral.
