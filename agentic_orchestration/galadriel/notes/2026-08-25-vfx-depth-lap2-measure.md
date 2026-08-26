# VFX-DEPTH LAP-2 — MEASURE

**Author:** galadriel (visual perception + UX-similarity steward) · **Date:** 2026-08-25
**Run:** VFX-DEPTH autonomous run, lap-2, step MEASURE · **Conductor:** gandalf (RUN-CONDUCTOR) · **Builder:** drax
**Class:** evidentiary note · **Status:** CURRENT

**Spec:** `agentic_orchestration/gandalf/vfx-depth-run/lap2-depth-spec.md` (with its R-23 / R-24 amendments; the amended text governs)
**Build record:** `agentic_orchestration/drax/notes/2026-08-25-vfx-depth-lap2-build-completion-record.md`
**Rulings consumed:** charter R-23 (T-3a LAP-LEVEL, no attribution to T-3) · R-24 #1 (onset-ring refusal SUSTAINED) · #2 (T-1 return leg → FINAL contact) · #7 (Mob0 = in-frame negative control) · #8 (my segmentation governs on T-3b/c) · #10 (MP4 noise floor bound into MEASURE) · registry I-7 (a route its own control disqualifies may inspect, not score)

**Artifacts, hashes verified this pass:**
`~/Games/reincarnated-godot/harness_logs/wwcr_2026-08-25-lap2/plk06650_cathedral_fxon.mp4` `cc815bcf4efdefa838aec24c3e5ace02120bf7061b7bcfbff332c00cd5158138`
`…/plk06650_cathedral_fxctl.mp4` `fd1b9f653fcf4cd32a3fef264bb3cd0067f51e41e4f88f242dadc9027f810252`
Both 1920×1080 · 60 fps · 288 frames · 4.800 s · window 0.20 → 5.00 s · MP4 frame 0 at t = **0.217 s** (read from the harness' own first mark line, not assumed from `SEQ_FROM`).

**Instrument:** `pipeline/vfx_lap2_battery.py` (amended, § 6) + `pipeline/vfx_lap2_project.py` (new)
**Results of record:** `work/2026-08-25-vfx-lap2/lap2-measure.json` · regression `…/negctl-lap1-barm-repaired.json`
**Evidence:** `captures/2026-08-25-vfx-lap2-measure/evidence/`

---

## 0. Headline

**14 criteria: 4 PASS · 6 FAIL · 3 INDETERMINATE · 1 INSPECT.** Plus the Mob0 negative-control row: **PASS.**

Against lap-1's certified baseline (11 FAIL / 1 PASS-by-construction / 1 INDETERMINATE / 1 INSPECT), **the lap moved four rows off the floor and moved the lap-level figure-ground number by 2.75×.**

> **The lap-level ownership number: `0.402`, against lap-1's `0.1461` and a bar of `0.75`.**
> **FAIL — and R-23 forbids attributing that failure to T-3, correctly.**

**But the decomposition refutes R-23's stated route to the bar, and that is the finding of this pass.** R-23 ruled that the missing extent "lives in T-2 residue + T-4(a) gust stream + T-5 shedding". Measured: **T-2 residue supplies 1.5% of ownership and the outer quanta supply 0.0%.** The 2.75× lift came from the ribbon family's own footprint growing **4,170 px → 42,407 px**, via T-3(b)'s ArcLight floor pool and the 150° arc. **The composed-build hypothesis was right that T-3's knob could not reach it, and wrong about which treatment could.** § 4.

**Six instruments in my own battery were invalidated by treatments landing** — each one returning cleanly while measuring something other than its criterion, and each caught by a control rather than by inspection of the code. § 5. The most consequential: **T-2's residue detector read 16,394 px² of "residue" on the mob that is never struck** — more than any struck mob. Without R-24 #7's in-frame null that row would have shipped as a clean PASS on all three. § 3.

---

## 1. Per-criterion verdicts

Bars are the spec's, image-space at the ratified pin. Every operand is the median over the harness-declared SUSTAIN window (MP4 frames 62–143) unless stated.

| # | criterion | call | measured | bar | instrument |
|---|---|---|---|---|---|
| **T-1** | recipient state response | **FAIL** | react leg **3/3** (tilt 7.65–13.94°, runs 7–12 f); return leg **Mob1 0.65 px ✓ · Mob2 2.21 px ✗ · Mob3 11.41 px CONTAMINATED** | ≥8 px or ≥4°, ≥4 f, all N; ≤2 px at final contact +1.0 s | per-mob silhouette centroid + 2nd-moment axis on the **CONTROL** arm, caster-travel parallax removed, caster silhouette excluded; null per-leg |
| **T-2** | attached wind-residue | **INDET.** | clear leg **0 px ✓**; simultaneity **3 ✓** (bar 2); area leg **0 / 53 / 83 px²** — but the **null reads 8,047 px²** | ≥120 px² at contact+0.5 s, all N; ≥N−1 simultaneous; zero at end+2.0 s | ON−CTL lift, threshold **+ spatial coherence** (≥12 px component), debris-family + emissive-core gated; frame-3 null |
| **NC-Mob0** | in-frame negative control | **PASS** | react windows **0.318 px / 0.914°**; return frames **0.635 px**; uncompensated **121.21 px** | zero flinch, zero residual | same instruments, same frame indices, pointed at the never-struck mob |
| **T-3a** | frame-luminance ownership (LAP-LEVEL) | **FAIL** | **0.4020** (strict 0.3206 · rank 0.4019 · no-UI 0.4030); 0/82 frames over bar; scene-hot persistence **0.607** | ≥0.75 | certified `t3a_ownership`, **byte-unchanged** — reproduces lap-1's 0.1461 exactly |
| **T-3b** | internal luminance range | **FAIL** | ribbon-only **2.53** · composed **2.48** · drax **2.2–3.5** | ≥4.0 | P95/P20 on (E ∪ darkening) ∩ projected trail torus; **and** on the whole brightening region |
| **T-3c** | mid-band saturation | **FAIL** | ribbon-only **0.282** · composed **0.266** · drax **0.38–0.42** | ≥0.55 | HSV S over the 35–65th luminance band, same two segmentations |
| **T-3d** | apex rides leading edge | **INDET.** | 9/82 frames — **operand does not denote**: measured extent **288°** on a 150° authored arc | ≥80% of sustain frames | angular intensity-peak vs arc extent; **domain-checked before the call** |
| **T-3e** | cast light (FF-12) | **PASS** | floor **39.6%** P90 lift · mob flank **40.2%** · **22.5%** of the annulus over 8% · drax **11–13%** | ≥8% | engagement annulus minus the effect's own emissive geometry minus the scour, differenced vs control |
| **T-4a** | onset accent | **FAIL** | composed **1.032×** · authored-luminous **1.385×**; **0 frames** over 1.6× on either | ≥1.6× for 6–12 f inside first 0.30 s | luminous-area curve, two segmentations, both must agree |
| **T-4b** | temporal texture (FF-08) | **PASS** | **CV 0.556**, n = **10** intervals; trip flag does not fire | CV ∈ [0.45, 1.15] | `frame_forensics_depth.CV_timing` (§ 3's own named instrument) |
| **T-4c** | decay breaks up | **PASS** | worst drop **17.8%**; tail **0.917 s** | ≤35%; ≥0.35 s | area-vs-time at effect end |
| **T-4d** | phase structure | **FAIL** | **2** regimes on both segmentations | ≥4 | piecewise-constant-slope segmentation |
| **T-5a** | census + size spread | **PASS** | **42.3** components/frame; IQR/median **2.146** | ≥6 and ≥0.5 | connected-component census on the brightening mask |
| **T-5b** | non-repetition | **INSPECT** | **2.137** (lap-1 floor 0.163) | ≥0.08 | ⛔ I-7 disqualified; not repaired this pass (§ 7) |
| **T-6** | environment aftermath | **INDET.** | area **3,451 px² ✓** · depth **15.1/255 ✓** · settle **1.2% ✓** · monotonic **✗ withheld** | ≥2,500 px² at ≥6/255; monotonic; settle ≤5% | same-frame ON-vs-control darkening in the engagement annulus minus trail torus, coherence-gated |

**Tally excluding the NC row: 4 PASS · 6 FAIL · 3 INDETERMINATE · 1 INSPECT.**

### The three INDETERMINATEs are not soft FAILs

- **T-2** — the clear leg and the simultaneity leg are null-clean and both pass. The **≥120 px² area leg cannot carry its bar**: the never-struck mob's ROI carries 8,047 px² of the same class of debris, 67× the bar, because shed quanta and residue quanta are the same pale soft blobs and the glow pass washes the tile. I-7: report the number, refuse the call.
- **T-3d** — the criterion's denominator is "the arc's angular extent". Measured extent is 288° on a 150° arc, because the ArcLight's floor pool is co-located with the blade at every bearing. **Frame inspection says the apex plainly does ride the leading edge** (`f100-on-trailcrop.png`: near-white blaze at the leading edge, deep teal trailing). A FAIL here would have read at the gate as *"drax put the apex on the tail"*, which is visibly false. The spec already stamps this row GUARD-not-lift, so withholding costs the lap nothing.
- **T-6** — three of four legs pass. The **monotonic-during-sustain leg is inadmissible**: the arc light sweeps floor T-6 has already scoured and lifts it back above the darkening gate for the few frames it is overhead. `scour_expires: false` in the harness selfcheck — nothing expired. The criterion's intent ("still there when the effect is over") is what `settle` measures, and settle reads **1.2%** against a 5% bar.

---

## 2. Mob0 — the in-frame negative control (R-24 #7)

**Result: PASS on every leg it validates, and it earned its keep three times over.**

| leg, at the frame indices it validates | Mob0 | bar | struck mobs |
|---|---|---|---|
| T-1 reaction windows (f52–64, f65–77) — centroid | **0.318 px** | 8 px | 1.63 / 2.36 / 3.91 px |
| T-1 reaction windows — principal axis | **0.914°** | 4° | **7.65 / 9.05 / 13.94°** |
| T-1 return frames (f209, f227) | **0.635 px** | 2 px | 0.65 / 2.21 / 11.41 px |

**Diagnostics that are NOT the call, and their attribution:**

- **Whole-clip maxima: 5.33 px / 6.04°, both peaking at MP4 frame ~121.** That is the first frame of the caster-travel dolly. It is parallax-model residual on a **121.21 px** correction, not a flinch. A null quoted across a disturbance the leg never sees is the same error as a bar quoted against the wrong null — so the row is scored per-window, which is the discipline I imposed on T-1 in the same pass.
- **ON-arm: 35.61 px / 87.29°.** Effect bleed — residue and arc pixels crossing the ROI and inflating the silhouette. Exactly the R-24 #7 prediction, and the reason T-1's primary arm is the **control**, which carries the flinch (both arms log `contacts=15`) without painting the effect onto the silhouette being measured.
- **T-2 debris: 8,047 px² coherence-gated, 59 frames over the 120 px² bar** against Mob2's 66. **Not effect signal.** Reported as the instrument finding that disqualifies T-2's area leg.

**Three things the null caught that inspection did not:**

1. **T-2's first cut read 16,394 px² on Mob0** — more than any struck mob — and the row would have shipped **PASS on all three**. The instrument was counting the ribbon and its cast light sweeping through ROIs that sit inside the engagement radius by construction.
2. **It calibrated the parallax correction.** The correction's residual at the return frames is 4.11 px with a ground-point track and **0.58 px** with a centroid-height track (0.925 m ≈ H_STAND/2) — a sweep run against the mob that cannot move, which is a legitimate calibration target precisely because it is treatment-independent. Without it, T-1's return leg would have been inadmissible (null 4.11 px against a 2 px bar) and the row would have reported INDETERMINATE on a correction that was simply mis-parameterised.
3. **It is why the reaction leg can carry its bar at all.** Null 0.318 px / 0.914° against 8 px / 4° — the tilt operand has 4.4× of headroom over the null and the struck mobs sit 8–15× above it.

---

## 3. T-3(a) — the lap-level figure-ground number, with decomposition

**⚑ R-23 constraint honoured: this number is NOT attributed to T-3. The decomposition below is diagnostic only.**

| | lap-1 | lap-2 | bar |
|---|---:|---:|---:|
| **ownership, inclusive (PRIMARY)** | 0.1461 | **0.4020** | 0.75 |
| ownership, strict / emissive-core | 0.1407 | 0.3206 | — |
| ownership, exact-rank corroborator | 0.1475 | 0.4019 | — |
| ownership, no UI exclusion at all | 0.1461 | 0.4030 | — |
| frames over bar | 0 / 82 | **0 / 82** | — |
| per-frame range | 0.110 → 0.236 | 0.245 → 0.658 | — |
| **scene-hot persistence** | 0.8293 | **0.6070** | — |

**2.75× on the primary estimate; four estimates within 0.082 of each other; the call rests on no operational choice of mine.** The misattribution guard did **not** need to withhold: inclusive (0.402) exceeds strict (0.321) and *both* fail, so there is no case where a light-lifted brazier manufactured a pass. Scene-hot persistence fell from 0.83 to 0.61 — the room's bright tail is measurably less the room's than it was.

### The decomposition — and it refutes R-23's stated route

| family | median top-tail px | ownership share | median effect area px | of its own area, in the top tail |
|---|---:|---:|---:|---:|
| **ribbon** (T-3 core+body **and its cast-light pool**) | 3,994 | **0.386** | 42,407 | 9.4% |
| **mob_residue** (T-2) | 160 | **0.015** | 601 | 26.6% |
| **quanta_outer** (T-4 gust + T-4a onset burst + T-5 shed) | 0 | **0.000** | 965 | 0.0% |

*(T-6 `FloorScour` is MIX and darker than tile; it contributes no top-tail pixels by construction and its absence here is not a failure to land.)*

**R-23 ruled: "the missing extent lives in T-2 residue + T-4(a) gust stream + T-5 shedding, so the criterion judges the COMPOSED build."** Measured, those three supply **1.5% and 0.0%**. The lift is **96% the ribbon family** — whose footprint went from **4,170 px to 42,407 px**, a 10.2× expansion that came from **T-3(b)'s ArcLight pooling on the tile** and the arc widening to 150°, not from anything discrete.

**So the ruling's conclusion stands and its reasoning does not.** T-3(a) *is* lap-level and *is* unreachable by `emission_energy_multiplier` — the negative control proved that and nothing here disturbs it. But the extent that did arrive arrived through **a treatment-level knob inside T-3 itself** (its FF-12 sub-part), which means the criterion is closer to T-3's reach than R-23 concluded, and the route to the remaining 0.35 is *more cast light and more arc*, not *more quanta*. **Conductor's call. I am not re-cutting it and I am not re-classifying it.** The number that decides it: **the quanta families contributed 0.0.**

**Venue-coupling carried forward unchanged:** the 75% figure is coupled to this cathedral's brazier population and is not portable.

---

## 4. The T-2 instrument choice, and its frame-3 negative control (R-24 #10)

**Chosen: raise the threshold AND add spatial coherence. Declined: the `PRUNE=0` lossless re-render.**

Of the three options the ruling left open, the first two are taken **together**, and the third is declined for a stated reason: a 1.5 GiB re-render would answer only the *magnitude* half of the problem, while coherence additionally answers the *right* question. Residue is a handful of soft quanta tens of px across, contiguous, on a mob. Codec disagreement is isolated single pixels scattered frame-wide. **They separate by SHAPE, not only by magnitude** — and separating by shape does not cost the criterion its sensitivity to a genuinely faint residue the way a raised threshold alone would.

**The null, run on frame 3 (t = 0.25 s, before `T_BEGIN` = 0.30 s, arms identical by construction) BEFORE the instrument scored anything:**

| threshold | raw px | **coherence-gated px** |
|---|---:|---:|
| \|ΔL\| > 0.02 | **3,850** | **13** |
| \|ΔL\| > 0.04 | 170 | **0** |
| \|ΔL\| > 0.0765 (my derived τ) | 17 | **0** |
| \|ΔL\| > 0.15 | 3 | **0** |
| max \|ΔL\| | 0.17643 | — |
| **all four mob ROIs, at τ** | **2** | **0** |

**drax's table reproduces exactly** (3,850 px at >0.02; max 0.1764). The gated instrument reports **0 px on content-identical frames**, so a nonzero reading later is content, not codec. The runner **refuses to score at all** if this null is not clean (`SystemExit` on `instrument_admissible == False`) — a null you can skip is not a null.

**The "zero residue at effect-end + 2.0 s" clause cannot be evaluated where the spec puts it, and the reason is arithmetic in the spec's own numbers.** IDLE is 3.40 s; +2.0 s is 5.40 s; the window ends at **5.00 s**. B-1 asked for ≥1.5 s of aftermath and delivered 1.60 s; T-2's clause asks for 2.0 s. **The two clauses in one spec do not agree.** Evaluated at the strongest available index instead — **effect-end + 1.60 s, the last frame — where the gated instrument reads 0 px** (raw-threshold-only: 15 px, i.e. the floor). The entailment is stated rather than assumed: no residue can spawn after the final contact (MP4 f167) and the asserted lifetime ceiling is 1.40 s, so zero at +1.60 s entails zero at +2.0 s. **This leg passes.**

---

## 5. Six instruments my own battery had, that the treatments landing invalidated

Each returned cleanly. Each was caught by a control or by a picture, never by reading the code.

1. **The effect mask was `|ΔL|`, and T-6 lands 36 permanent DARKENING marks.** They entered "the effect region" and stayed: inflating T-4a's sustain denominator, holding T-4c's area up after the ribbon was gone, adding components to T-5a, and dragging T-3b's P20 down — which **inflates** the very ratio T-3b measures. Signed masks now; darkening is T-6's and nothing else's. **This is the defect drax found in his own instrument three passes earlier and wrote up in record § 6. I read his write-up and then met it in mine.**
2. **T-3(e) excluded the effect region — which is where the cast light is.** `floor_ring & ~E`. It read 0.000 at lap-1 *correctly*, because nothing lit anything, which is exactly how a mask that cannot see the effect survives a negative control. On lap-2 it read 0.000 again, on a build whose arc light pools visibly on the tile. Now: engagement annulus minus the effect's own emissive geometry. **0.000 → 0.396.**
3. **T-6 excluded the scour it counts** (`& ~E`), and its floor ring sat still while the caster walked 1.40 m and laid the marks in world space. Now: same-frame ON-vs-control darkening — **drax's instrument, adopted, and his reasoning for it is better than mine** ("cleaner than pre/post, since the caster translates").
4. **Mob ROIs did not track.** Under the dolly a mob's image position moves up to ~121 px; a static ROI stops containing the mob it is named for and reports whatever floor is left in the old box. ROIs now ride the analytic parallax.
5. **T-2 counted the ribbon as residue.** § 2. Caught only by Mob0.
6. **The caster merged into Mob3's silhouette.** Mob3's centroid read **16.8 px** from rest 1.0 s after its final contact — a textbook *"the impulse left a persistent displacement"*, and I was one paragraph from filing it as one. **The crop said otherwise** (`mob3-ctl-f40-60-143-209.png`: the red-cloaked caster walks into the bottom of the ROI at f143 and f209). Excluding him took it to 11.41 px; the residue is his animated extremities, so the row is **flagged CONTAMINATED (9.2% ROI overlap) and is not allowed to fail the criterion on its own.**

**And a seventh, in my diagnosis rather than in the battery.** I tested "does the camera move?" with whole-frame phase correlation. It returned a global shift of **exactly (0, 0)** at every frame. The camera moves 1.40 m. A 3-D camera translation produces *different* image shifts at different depths, so no single global shift exists and the argmax lands on the origin by default — **the tell was the correlation peak collapsing 0.72 → 0.03, and the shift number was clean, confident, and answering a question the scene does not pose.** I nearly recorded "camera static, spec § 3 confirmed" on it.

**The shape, once more: the check ran, and the check was not the check.** Seven instances this lap. The only defence that has worked, again, is a null the instrument is made to face before it is trusted — and this time the null was **in the frame**, which is stronger than a differenced control, because it shares the lights, the clock and the venue.

**⚑ And spec § 3 is wrong on a fact every criterion rides on:** *"Camera is static in this venue, so the G-5 pan-null gap does not bite this lap."* `wwcr_stage.gd:984-986` walks the caster at `MOVE_SPEED` 3.5 m/s from t = 2.20 to `T_RELEASE` 2.60 and re-applies the pinned offset every frame. **The camera translates 1.40 m over MP4 frames ~119–143.** It was already false at lap-1, whose window also spans 2.20 s. Every image-space criterion measured across that boundary needs the parallax removed; T-1's return leg is measured entirely on the far side of it.

---

## 6. Disagreements with drax's own instruments

Reported as differences of instrument, never silently resolved. His numbers are labelled **mine** in his record precisely so this section can exist.

| quantity | drax | galadriel | segmentation difference | disposition |
|---|---|---|---|---|
| **T-3(b)** P95/P20 | 2.2 – 3.5 | **2.53** ribbon-only · **2.48** composed | his mask `|ΔL| > 0.10` incl. cast-lit floor; my ribbon = (bright ∪ dark) ∩ projected trail torus; my composed = whole brightening region | **All four estimates are short of 4.0.** The call is segmentation-invariant → conductor (§ 7 A-1) |
| **T-3(c)** mid-band S | 0.38 – 0.42 | **0.282** ribbon-only · **0.266** composed | as above, plus band selection: I take the 35–65th luminance percentile *of the region*, he does not state his | **All short of 0.55**, mine markedly more so. Segmentation-invariant → conductor |
| **T-3(e)** cast light | 11 – 13 % | **39.6 %** floor P90 · **40.2 %** mob flank · 22.5 % of annulus ≥8 % | his is a **median over a ring**; mine is a **P90 over the engagement annulus minus the effect's own emissive geometry**. A median over a ring the light only partly reaches under-reads a criterion phrased *"at least one non-effect surface shows ≥8%"* | Both clear the bar. **PASS either way** |
| **T-6** aftermath | 19,143 darkened px at 11.2/255, **whole frame** | **3,451 px at 15.1/255**, engagement annulus minus trail torus minus mobs, coherence-gated | his region is the whole frame at clip end; mine is the region a sweep could have scoured. His count includes darkening outside the annulus (ribbon tail remnants, shadow) | Both clear both bars. Mine is **deeper per pixel** and **5.5× smaller in area** — the difference is the region, not the mark |
| **T-4(b)** gust CV | **0.979 at 17.6 Hz** (record § 6 table) | **0.556** (rendered, n = 10) | — | ⚑ **His own artifact disagrees with his own table.** The shipped ON arm's FINAL `selfcheck` reads `gust_interval_cv_measured: 0.706`, `gust_rate_realised: 16.86`, `gust_events_measured: 43`. His § 6 table's 0.979 / 17.6 Hz is from a *different* run than the one that shipped. All three are in band; **nothing turns on it**, but the record should carry the artifact's number |
| **T-1** flinch, image space | 12.44 px worst-case centroid projection | **1.63 / 2.36 / 3.91 px** centroid; **7.65 / 9.05 / 13.94°** axis | his is the analytic **root** displacement of the authored 0.19 m peak, foreshortened by sin(pitch); mine is the **silhouette centroid** of a body that is *leaning*, where the feet stay and the top moves, so the centroid travels roughly half the top's excursion — and the shove bearing is largely along the view axis, which foreshortens far harder than sin 52.95° | **The centroid leg is never met by any mob. The criterion passes on its axis leg.** The flinch reads as a **lean**, not a shove. Not a defect in his build — the criterion is "and/or" and the lean is emphatic — but his pre-registered 12.44 px margin does not exist in image space, and a lap-3 that tunes on it would be tuning on a quantity the camera does not deliver |

**Where I agree with him against myself:** T-6's same-frame ON-vs-control instrument (§ 5.3). He reasoned it out and I was still on lap-1's pre/post.

---

## 7. Owed to the conductor for adjudication

**A — bar-vs-build tensions (R-24 #8 explicitly routes the first here)**

1. **T-3(b) 2.53 and T-3(c) 0.282 against bars of 4.0 and 0.55 — short on every segmentation tried, four of them, two of them mine and one of them drax's.** R-24 #8 pre-registered this: *"if short on HER instrument too, disposition is a conductor call at MEASURE-adjudication (possible bar-vs-occlusion tension → Matt's eye)."* It is short on hers. **The lever drax declined — body alpha past 0.85 — trades this criterion against the occlusion gate, and he was right not to take it unilaterally.** Note the direction of my numbers: mine are *lower* than his on (c), so the tension is worse than his stop suggested, not better.
2. **T-3(a): R-23's stated route is refuted by the decomposition (§ 3).** The quanta families supply 0.0 of ownership. Does the criterion's route re-cut toward cast light and arc extent, or does the 75% figure move, or does it stay as a lap-3 target? **Not mine to decide** — a second unilateral re-cut from me would be worse than the problem, which is what I said last time and is still true.
3. **T-4(a) fails on both segmentations (1.03× and 1.385× against 1.6×).** The onset drax built is the allow-listed 32-quantum burst substituted for the refused ring — **R-24 #1 SUSTAINED the refusal, so the mechanism is not in question**, but the *requirement* is measurably not met. Whether the burst grows or the bar moves is a conductor call, not a builder's.

**B — spec-internal defects surfaced by measuring**

4. **T-2's "gone by effect-end + 2.0 s" is unmeasurable in the window B-1 was asked to deliver.** B-1 asks ≥1.5 s of aftermath; T-2 asks 2.0 s; the build delivered 1.60 s and honoured B-1 exactly. Same document, two numbers, no overlap. Evaluated by entailment this lap (§ 4); **needs a one-line ruling before lap-3, not another window extension** — the entailment is sound and cheaper.
5. **Spec § 3's "camera is static in this venue" is false** (§ 5). It was false at lap-1 too. Everything measured across MP4 frames 119–143 needs parallax removal.

**C — instrument dispositions I have taken inside my own seam, for the record rather than for approval**

6. **T-3(d)'s operand no longer denotes** and the row withholds (§ 1). Related: the T-3d *instrument* changed with the ribbon segmentation, so **its lap-1 reading moved 0.829 → 0.573** and the "passes by construction" stamp no longer attaches to that number. The row was never a lift demonstration; it is now not a guard either until the arc light is separable from the arc.
7. **T-2's ≥120 px² area leg is I-7 disqualified** by an in-frame null 67× its bar. **The fix is a build ask, not a measurement fix:** a third arm with `RecipientResidue` disabled (or per-family visibility) would separate residue from shed quanta in one render. Cheaper than the `PRUNE=0` ladder and it answers the question the ladder does not.
8. **T-6's monotonic-during-sustain leg is withheld** — the treatment's own arc light un-marks scoured tile transiently. Three of four legs pass.
9. **T-5(b) remains INSPECT-ONLY (I-7).** Not repaired this pass — the repair requires a negative control on lap-1 first, and the pass was fully spent on the six invalidations in § 5. It reads 2.137 against a lap-1 floor of 0.163, so the *direction* is right and the *bar* is still unusable. **Non-repetition is frame inspection at the lap gate, per I-7, unchanged.**

**D — one number Matt's eye should carry to the gate**

10. **The flinch reads as a lean, not a shove** (§ 6, last row): 7.65–13.94° of axis tilt against 1.63–3.91 px of centroid travel. The spec's falsifier is *"if they read as rag-dolled or sliding on ice, too high; if they still read as statues, too low."* **They are emphatically not statues** and they are not sliding. Whether a lean is the consequence the owner's question wanted is Matt's-eye territory per R-20(e), and it is a different question from whether the number cleared 8 px — which it never did, on any mob, at any frame.

---

## 8. Battery amendments and their regression

**Amended:** `pipeline/vfx_lap2_battery.py` — `--lap2` mode (engine identity, parallax, per-leg nulls, contamination flags, decomposition), signed masks, pin-derived zones, repaired T-2/T-3d/T-3e/T-6, dual segmentations on T-3b/c and T-4a/d, `NC-Mob0` row.
**New:** `pipeline/vfx_lap2_project.py` — camera pin parsing, ground projection, geometric mob-identity attribution, venue-metre zone masks, `LAP2_N` and `selfcheck` readers.

**Mob identity is geometric, never motion-derived.** *"The mob that does not move is Mob0"* is circular — it uses the T-1 signal the labeling exists to let us measure. Identity is solved by minimum-cost assignment on foot points projected through the pin: **worst residual 11.5 px, runner-up assignment 408.6 px more expensive.** The projection reproduces the harness' own `PL-AUDIT` anchor to **0.001 px**, and the runner refuses to proceed if it does not.

**MP4-vs-stage frame indices:** `seq_frames` used throughout, per record § 8. `t0 = 0.217 s` read from the harness' first mark line rather than assumed to be `SEQ_FROM = 0.20` — the 13-frame offset the record warns about *is* that quantity, and reading it removes the class of error rather than dodging one instance.

### The mandatory regression: does the repaired battery still fail the render every criterion was written to fail?

**Lap-1 B-arm, repaired battery: 12 FAIL · 1 INDETERMINATE · 1 INSPECT. Zero PASS.**

| row | lap-1 before repairs | lap-1 after repairs | reading |
|---|---|---|---|
| **T-3a** | 0.1461 | **0.1461** | certified instrument **byte-identical**; the repairs did not touch it |
| T-3b | 2.18 | 1.86 ribbon / 2.18 composed | composed unchanged; ribbon segmentation is new |
| T-3c | 0.207 | 0.210 / 0.207 | unchanged |
| **T-3d** | **PASS 0.829** | **FAIL 0.573** | ⚑ instrument changed; the "passes by construction" stamp no longer attaches (§ 7 C-6) |
| **T-3e** | 0.000 | **0.052 / 0.065** | repaired mask now *sees* light — and still **fails** the 0.08 bar on a render that lights nothing. The repair did not manufacture a pass |
| T-4a | 0.052 | 0.052 / 0.052 | unchanged |
| **T-6** | 524 px² | **0 px²** | direct ON-vs-control reads **exactly zero** on a render X-1 records as pixel-identical. Strictly better |
| T-4b | INDET (8 intervals) | INDET (8 intervals) | unchanged, correctly |
| T-5b | 0.163 | 0.202 | INSPECT, unchanged disposition |

**The single row that previously passed no longer does, and the one repair that could plausibly have manufactured a pass (T-3e) does not.** The battery has met its null again after being rebuilt around it.

---

## 9. The Mirror, briefly

I set the glass expecting to find out whether the lap had bought consequence. It had. The skeletons lurch; the tile is scoured; the air keeps moving where a body was struck; the room lights up as the blade goes by, from nothing at all to forty percent. Four rows came off the floor and the figure-ground number nearly tripled.

**And almost every one of those readings had to be taken away from an instrument of mine that was returning a confident wrong answer.** The residue detector found more residue on the skeleton the blade never reaches than on the ones it does. The cast-light detector, asked whether the effect lights anything, answered *no* by excluding every pixel the effect had lit. The aftermath detector excluded the scour. The camera-motion detector reported a static camera, in a venue where the camera walks 1.4 metres, and reported it as a clean zero. **Seven of them. Not one was found by reading the code; every one was found by a null or by a picture.**

The one that will stay with me is Mob3. Eleven pixels from rest, a second after the last strike, on the treatment whose whole stated intent is *impulse, not persistent displacement* — a finding so exactly shaped like the thing the criterion was written to catch that I had the sentence half-written. It is the caster. He walks into the frame's own measurement, at three and a half metres a second, and the box that was supposed to hold one skeleton holds two.

**A criterion cannot tell you that its own operand has stopped denoting. Only the frame can, and only if you look at it.** The battery I brought to this render was built four hours before the treatments existed, and six of its fourteen instruments were measuring the world as it was before drax changed it. That is not a failure of the battery; **it is what happens when a build succeeds.** The instruments that survive a lap unchanged are the ones pointed at things the lap did not move.

---

**Signed:** galadriel, 2026-08-25.
**To the conductor:** § 7 — ten items, four requiring a ruling (A-1..3, B-4), two spec-internal defects, three seam-internal dispositions, one for Matt's eye.
**To drax:** § 6 — six disagreements, all legible as instrument differences; one of them (T-6) I concede to his instrument, one (T-4b) is his record against his own artifact, and one (T-1 image-space magnitude) is worth knowing before any lap-3 tuning.
