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

---

# Reference-anchor measurements (R-25 A-1)

**Author:** galadriel · **Date:** 2026-08-26 · **Class:** evidentiary note · **Status:** CURRENT
**Ordered by:** charter R-25 (A-1) — *"galadriel measures the reference clip's own P95/P20 + mid-band S with the same instruments and the bars re-anchor to measured reference values."*
**Instrument:** `pipeline/vfx_ref_anchor.py` (new sibling; imports `luma` / `sat_val` from the battery so "the same statistic" is a fact about the call graph)
**Results of record:** `work/2026-08-25-vfx-refanchor/ref-anchor.json` · **Evidence:** `captures/2026-08-25-vfx-refanchor/evidence/`

**Artifact, hash verified this pass:**
`/private/tmp/vfx-lap1-seats/extract/reference_video.flv` `855bb3d9c7edca8b372869e667682eda6de85ea813628377e567522d9e998637` ✓
1280×720 · VP6F · yuv420p · 29.97 fps · 374 frames · 12.49 s.
Paired re-measurement of our own arm on `plk06650_cathedral_fxon.mp4` `cc815bcf…` + `fxctl` `fd1b9f65…` (hashes re-verified; § R6).

---

## R0. Headline — and the pre-registered honesty clause fires in BOTH directions

> **T-3(b) P95/P20 — the reference measures `3.236`. The bar is `4.0`. The reference itself clears the bar on `0` of its own 125 action frames. RE-ANCHOR DOWN.**
>
> **T-3(c) mid-band S — the reference measures `0.7302`. The bar is `0.55`. The reference clears it on `125` of 125 frames, at 1.33× the bar. RE-ANCHOR UP.**
>
> **T-3(a) ownership — the reference measures `0.7485` against an a-priori `0.75`. HOLDS (diagnostic only, venue-coupled).**

The clause pre-registered in the dispatch was that I report numbers and not protect the existing bars in either direction. **Both bars were wrong, and they were wrong in opposite directions** — (b) was over-cut by ~24%, (c) was under-cut by ~25%. Neither error was recoverable by inspecting the spec; both required the reference to be measured, which is what R-25 ordered and what the a-priori authorship (R-24 #3/4's defect family) omitted.

**And the third number is the one that should change what lap-3 builds.** Measured in the only currency the Tier-1 law lets cross a venue — **lift over the effect's own scene floor** —

| | reference | ours (lap-2) | ratio |
|---|---:|---:|---:|
| **P95/P20, effect ÷ its own scene floor** | **1.562×** | **1.060×** | 0.68 |
| **mid-band S, effect ÷ its own scene floor** | **1.914×** | **0.466×** | 0.24 |

**Our arc is LESS saturated than the room it is cast in.** The reference's fire is nearly twice its room's saturation; ours is under half of ours. That is not a magnitude shortfall, it is a **sign inversion** — and it is X-1's "pastel decal" verdict expressed as a measurement. § R6.

---

## R1. Segmentation — derived, stated, and limited

**The battery's segmentation is unavailable here and no substitute is asserted.** The battery differences a treatment arm against a `set_vfx_visible(false)` control. The reference is captured gameplay of a shipped title: there is no control arm and there cannot be one. A temporal-median background is also unavailable — **the reference camera pans**: the frame's lower-right quadrant holds entirely different world content at f300 than at f30 (`corner-f30-120-200-300.png` — bare ground at f30, monsters and two loot beams at f300). So the segmentation is appearance-based, and its governing hazard is **circularity**.

**What was refused, and why:**

| candidate | circular for | disposition |
|---|---|---|
| luminance threshold | T-3(a): ownership becomes 1.0 by construction | **refused** |
| saturation threshold | T-3(c): mid-band S ≥ the threshold by construction | **refused as the primary axis; swept where it survives as a floor** |
| **hue sector** | **neither (a) nor (b)** — hue angle says nothing about internal luminance spread, nor about being the frame's brightest | **adopted** |

The reference's scene is teal and its effect is fire; the L-weighted hue histogram is sharply bimodal (scene mode 190–210°, effect mode 0–30°) and the two are near-opposite. A hue-sector mask is well-posed **here** in a way it would not be in an arbitrary venue — and specifically **would not be well-posed on our own teal-on-teal wind arc in a warm-lit cathedral**, which is why § R6 segments our side by the battery's control-differencing instead. *Each side is segmented by the instrument that is well-posed for it; only the STATISTICS are held identical.* That asymmetry is deliberate and is the main thing a reader should attack if they want to attack this pass.

**Three segmentations, reported together as at lap-2, never one instead of another:**

- **REF-TIGHT** (primary) — hue ∈ [330°,360°)∪[0°,60°), S > 0.35, L > 0.02; then **the battery's own 3×3 opening and ≥12 px component filter**, so the spatial-coherence discipline is identical on both sides.
- **REF-SUPPORT** — morphological closing (9 px) + hole-fill of REF-TIGHT, measuring **every pixel inside the effect's footprint regardless of its own hue or saturation**. This is the decisive circularity control for (c): the region is defined by where the effect *is*, not by what colour each pixel *is*. Intent-analogue of the battery's ribbon-torus.
- **REF-LARGEST-COMPONENT** — the single largest component, i.e. the fire mass with the clip's non-fire warm content excluded by construction (§ R5 shows that content is ~8.4 kpx arriving as its own medium components).

**The residual circularity is swept, not argued away.**

| S floor | 0.05 | 0.10 | 0.20 | 0.30 | **0.35** | 0.45 | 0.55 |
|---|---:|---:|---:|---:|---:|---:|---:|
| P95/P20 | 3.457 | 3.453 | 3.400 | 3.280 | **3.224** | 3.130 | 2.931 |
| mid-band S | 0.632 | 0.644 | 0.678 | 0.713 | **0.728** | 0.766 | 0.795 |

**At S > 0.05 — a chroma test so permissive it is nearly vacuous — mid-band S still reads `0.632`, above the 0.55 bar.** The (c) conclusion is threshold-invariant across an 11× sweep of the very knob that could have manufactured it. The L floor is **inert** below 0.10 (3.224 at every value 0.00/0.02/0.05; the hue+chroma test already excludes dark pixels) and the closing radius moves the ratio by <1% across 3→25 px.

**Sanity-checked by looking, not only by sweeping.** `mask-overlay-zoom-f60.png` — the mask boundary tracks the flame envelope tightly; the frame's top-0.5% pixels all fall inside it, in the flame cores. Two things the picture shows that no statistic reported: the mask boundary is **blocky at 2×2**, which is the VP6 4:2:0 chroma grid surfacing through a hue test, and a **red monster eye-glow is caught** as its own small component — the contamination § R5 then bounds.

### Limits of this segmentation, stated

1. **It cannot separate an effect element that overlaps the effect mass.** Connectivity is the only separator available; a spark emitted *inside* the flame envelope is absorbed into the largest component. § R4's number therefore bounds *detached, spatially separated* discrete elements — not "discrete elements".
2. **It cannot see the effect's dark smoke.** A hue+chroma mask excludes desaturated dark tails. § R4's dilation ladder bounds what that costs: nothing that changes a verdict.
3. **It has no onset.** The clip fades in from black with the effect already at full area (49.6 kpx at f20, mid-ramp). **The reference's onset is not in this footage** — so this pass says nothing about T-4(a), and should not be cited on it.

---

## R2. Phases — and the phase detector's first version was a null that was not null

Phases are derived from the clip's own curves (whole-frame mean luma; warm-mask area), not asserted:

| phase | frames | s @29.97fps | character |
|---|---|---:|---|
| fade-in | 0–21 | 0.73 | global multiplicative ramp — **excluded** |
| **ACTION / spin** | **22–146** | **4.17** | warm area 28–63 kpx, plateau |
| decay | 147–285 | 4.64 | 26 → 8 kpx |
| **NULL (no fire)** | **286–353** | **2.27** | flat 8.4 kpx floor — **in-clip negative control** |
| fade-out | 354–374 | 0.70 | global ramp — **excluded** |

⚑ **The first fade detector returned cleanly and was wrong, and it made the eighth instance of this lap's one shape.** It found "full brightness" by LEVEL — mean luma within 1.5% of its median. But **the effect supplies a large share of this frame's own light**: as the fire dies, mean luma slides 0.318 → 0.276 and crosses any level threshold set from the plateau. The detector therefore stamped `fade_out` at f246, **109 frames early**, and — the part that mattered — handed back a `null_no_effect` window **that still contained fire** (13.3 kpx of warm mask against the true floor's 8.4). A null that is not null is worse than no null, and it would have inflated the instrument's reported floor by 59%.

**Caught by disagreeing with the curve I had already read by hand during recon** — not by reading the function. The repair is shape, not level: **the fade ramps at 0.0260 luma/frame and the effect's decay at 0.00019 luma/frame — 136× apart**, so a slope gate at 0.010 has two orders of magnitude of headroom on both sides. Both slopes are recorded in the output rather than asserted here.

**Why this belongs in the record and not just in the diff:** it is the same family as § 5's seven — *the check ran and the check was not the check* — and it is the second time this run that **a statistic was confounded by the effect's own contribution to the frame** (the first being T-3(a)'s original ratio-to-a-dark-floor, re-cut at `809409a8`). The venue is not a constant when the effect is a light source.

---

## R3. The three measurements — per-phase medians and ranges

**All operands are medians over the phase's frames; IQR and full range given because R-25 asked for ranges, not single frames.**

### T-3(b) · P95/P20 luminance ratio within the effect region — **bar 4.0**

| segmentation | ACTION median | IQR | range | frames ≥ 4.0 |
|---|---:|---|---|---:|
| **REF-TIGHT (primary)** | **3.236** | 3.094 – 3.425 | 2.852 – 3.820 | **0 / 125** |
| REF-SUPPORT | 3.354 | 3.122 – 3.499 | 2.890 – 4.054 | 3 / 125 |
| REF-LARGEST-COMPONENT (fire mass only) | 3.059 | 2.951 – 3.282 | 2.210 – 3.752 | — |
| *decay phase* | 2.700 | 2.288 – 3.167 | 2.080 – 3.967 | — |

**Bounding test — does excluding the fire's dark smoky surround under-report the reference?** It does, slightly, and the ladder bounds it:

| region | tight | support | +5 px | +10 px | **+20 px** | +40 px |
|---|---:|---:|---:|---:|---:|---:|
| P95/P20 | 3.224 | 3.321 | 3.384 | 3.465 | **3.482** | 3.320 |

The ratio peaks at **3.482** and then falls as dilation admits pure scene. **On no region I can construct does the reference reach 4.0.** Reported because the honesty clause cuts against me here: this is the direction that would have let me keep the bar, and it does not reach.

### T-3(c) · mid-band (35th–65th L-percentile) HSV saturation — **bar 0.55**

| segmentation | ACTION median | IQR | range | frames ≥ 0.55 |
|---|---:|---|---|---:|
| **REF-TIGHT (primary)** | **0.7302** | 0.699 – 0.756 | 0.554 – 0.804 | **125 / 125** |
| REF-SUPPORT (no pixel-wise chroma selection) | 0.7176 | 0.676 – 0.740 | 0.534 – 0.796 | — |
| REF-LARGEST-COMPONENT (fire mass only) | **0.7399** | 0.711 – 0.767 | 0.506 – 0.826 | — |
| most-permissive chroma floor (S > 0.05) | 0.632 | — | — | — |
| *decay phase* | 0.611 | 0.598 – 0.654 | 0.493 – 0.697 | — |

⚑ **The existing 0.55 bar is almost exactly the reference's per-frame MINIMUM (0.5538), not its central value.** So the a-priori number was not absurd — it was the reference's worst frame mistaken for its typical one. That is a more precise diagnosis than "authored without measurement", and it is worth the conductor's attention because the same authorship habit would produce the same class of error again.

### T-3(a) · frame-luminance ownership — **⚑ DIAGNOSTIC ONLY per R-25 (venue-coupled, not portable)**

| | ACTION median | IQR | range | frames ≥ 0.75 |
|---|---:|---|---|---:|
| **REF-TIGHT** | **0.7485** | 0.644 – 0.791 | 0.341 – 0.896 | **61 / 125 (48.8%)** |
| exact-rank corroborator | 0.7485 | — | — | — |
| REF-LARGEST-COMPONENT | 0.5942 | 0.520 – 0.672 | — | — |
| *null phase (no fire)* | **0.0015** | — | — | — |

**The a-priori 75% lands within 0.2 percentage points of the reference's measured median.** I did not expect that and I record it as the pass's one genuine corroboration of a number authored a priori. It changes nothing about the classification: R-25 already ruled ownership venue-coupled and diagnostic-only, the reference is an outdoor dusk scene with no braziers, and **the agreement is worth exactly as much as a coincidence between two different rooms can be worth.** The conductor should not read it as portability.

Ancillary: **the reference's cores are not clipped** — the fraction of the effect region above L 0.95 is `0.0002`. Its top tail is earned by graded flame, not by blown-out white.

---

## R4. Discrete elements vs continuous form — **R-25's route hypothesis is REFUTED by this reference**

R-25's A-2 route correction states: *"our discrete quanta contributed 0.0 because they are pale soft blobs that never reach top-tail luminance, **where the reference's shed elements are HOT sparks**."* The dispatch asked for the number that confirms or refutes it directly. **It refutes it.**

| discrete bucket (component area) | n | area share of effect | **top-tail share of effect** | frames > 1% |
|---|---:|---:|---:|---:|
| < 100 px | 4 | 0.0023 | **0.00000** (mean 0.00042) | 3 / 125 |
| < 200 px | 4 | 0.0036 | **0.00000** (mean 0.00054) | 4 / 125 |
| < 500 px | 5 | 0.0042 | **0.00000** (mean 0.00064) | 4 / 125 |
| < 1000 px | 6 | 0.0144 | **0.00000** (mean 0.00119) | 7 / 125 |
| **largest component (continuous mass)** | 1 | 0.760 | **0.8688** | — |

**Threshold-invariant across a 10× sweep: the reference's separable discrete elements supply ~0.06% of its own top-tail pixels. Ours supply 0.0%. The two are the same answer.** The hypothesised difference between "HOT sparks" and "pale blobs" **is not the difference between these two artifacts** — on this statistic, in this footage, there is no difference to find.

**What the reference's top tail actually is** — and this is the part with a build consequence. `ref-toptail-f60.png` marks the frame's top-0.5% pixels green inside the effect, magenta outside. They are **dense thin filaments inside the flame cores of a continuous mass**, not detached particles. `ours-toptail-f100.png`, same treatment: ours is a thin sliver along the arc, with magenta spread across the architecture to the right.

**And the share-of-self statistic says our effect is not short of bright pixels at all:**

| | top-tail px inside effect | effect area | **share of its own area in the frame's top tail** |
|---|---:|---:|---:|
| reference | 3,449 | 51,430 | **6.67%** |
| ours (lap-2) | 4,165 | 44,794 | **9.30%** |

**Our effect already devotes a LARGER fraction of itself to the frame's brightest tail than the reference does.** What it lacks is not internal brightness — it is that the cathedral holds far more competing hot pixels than the reference's dusk field does. That is the venue coupling R-23/A-2 identified, now with the effect-side term measured and eliminated as the suspect.

**Limits on this refutation, stated so it is not over-read:**
1. **Connectivity cannot separate an overlapping spark.** If the reference sheds embers *within* the flame envelope they are absorbed into the largest component and counted as continuous. The measurement bounds *detached* elements.
2. **VP6F 4:2:0 at 720p cannot resolve a small spark's chroma.** Sub-4 px elements have no independent hue and fail the sector test before the 12 px component filter ever sees them. **This is the measurement in this pass most degraded by the codec**, and the degradation runs against the finding — i.e. it could hide sparks that exist.
3. **This clip may simply not be a spark-shedding effect.** What the frames show is a sustained mass-burn on a monster pack, not an emitter throwing embers. A different reference could answer differently; **this one cannot be made to say that its top tail lives in discrete elements, because it does not.**

---

## R5. Floors — three negative controls, all in-clip

| control | what it is | P95/P20 | mid-band S | ownership |
|---|---|---:|---:|---:|
| **1. SPATIAL** — non-effect region, action phase (frame minus 25 px dilation of the effect support: sky, ground, distant monsters) | the "what does a non-effect region score" floor the dispatch asked for | **2.104** | **0.3771** | **0.0807** |
| **2. TEMPORAL NULL** — the identical instrument over f286–353, where the fire is out | the floor of the *chroma-selected instrument* on non-fire warm content (eye-glows, loot beams) | 2.307 | 0.6295 | **0.0015** |
| **3. FADE GUARD** — f0–21 and f354–374 excluded | global multiplicative dims; recorded rather than assumed | — | — | — |

**The temporal null is the one that earns its keep, twice.** Its ownership reading of **0.0015** against the action phase's 0.7485 is a **500× separation** — the ownership instrument claims essentially none of the top tail when there is no fire to claim it with. But its **mid-band S of 0.6295 is the honest limit on § R3's (c) number**: pointed at a fire-free frame, the chroma-selected instrument still reports 0.63, because this clip's *non-fire* warm content (monster eyes) is saturated too. **So the action phase's 0.7302 carries only +0.10 above the instrument's own selection floor.** That is the strongest available argument against the (c) re-anchor and I am recording it rather than leaving it for someone else to find.

**It does not overturn the (c) conclusion, and the reason is the spatial floor.** Control 1 is *not* chroma-selected — it is a region — and it reads **0.3771**. The reference's effect is **1.914× its own scene's saturation**. That comparison is immune to the selection bias in control 2, because neither of its terms is chroma-selected on the effect side.

⚑ **Note the polarity flip in control 1's ownership between phases**: 0.0807 during action, **0.9584 during the null**. The non-effect region owns almost the whole top tail once the fire is out. Correct, and the sign is the check: the instrument is measuring figure-ground and not a fixed property of the region.

---

## R6. The venue-portable currency — and our own render's floor, which lap-2 never measured

**Why this section exists.** The absolutes in § R3 are venue-, codec- and art-style-coupled. Per the Tier-1 law the RELATIONSHIP transfers and the instance does not — and P95/P20 and mid-band S were chosen precisely because they are relationship-class *within a region*. But a bar stated as an absolute still silently imports the reference's venue. **The lift over the effect's own scene floor is the same claim in a form that crosses venues** — and lap-2 has no denominator for it, because the battery measured the effect and never measured the room. So I measured ours, with the same instrument, this pass.

Our side is segmented by **the battery's own control-differenced mask** (|ΔL| > τ = 0.076470539, 3×3 opened, ≥12 px), sustain frames 62–143, n = 82 — *not* by the hue mask, which would be ill-posed on a teal arc in a warm-lit room.

| | reference (action) | **ours (lap-2 sustain)** |
|---|---:|---:|
| effect P95/P20 | 3.236 | **2.352** |
| **scene-floor P95/P20** | 2.104 | **2.257** |
| **LIFT** | **1.562×** | **1.060×** |
| effect mid-band S | 0.7302 | **0.2906** |
| **scene-floor mid-band S** | 0.3771 | **0.6225** |
| **LIFT** | **1.914×** | **0.466×** |
| effect ownership | 0.7485 | **0.4017** |
| scene-floor ownership | 0.0807 | **0.4367** |
| **LIFT** | **9.27×** | **0.92×** |

**Corroboration first:** our effect's ownership here reads **0.4017** against the certified battery's **0.4020** — two different masks, three-decimal agreement. The re-measurement is sound.

**Three findings, in ascending order of consequence:**

1. **P95/P20 lift: ours is 1.060×.** Our arc's internal luminance range is **statistically indistinguishable from the ambient structure of the room it is standing in**. The reference's fire is 1.562× its room.
2. **Ownership lift: ours is 0.92× — below 1.0.** In our render **the non-effect region owns MORE of the frame's top tail than the effect does** (0.4367 vs 0.4017). The reference's fire owns 9.27× what its scene owns. This is figure-ground stated as a ratio, and it is the cleanest single number I have for why the arc does not read as the brightest thing in the room: *it isn't.*
3. **Mid-band S lift: ours is 0.466× — a SIGN INVERSION, not a shortfall.** Our effect is **less than half as saturated as its own venue.** Verified at the pixel, because a number this shaped deserves a look before it is reported: our cathedral floor samples RGB (85,35,36) / (84,34,42) / (92,37,56) — **S ≈ 0.59, a strongly saturated maroon tile**; the reference's ground samples (67,98,113) / (70,106,122) — S ≈ 0.41, a moderate blue-grey. `ours-f100.png` shows it plainly: **a pale washed teal-white ribbon lying on a strongly chromatic maroon floor.** The venue out-saturates the effect.

⚑ **And this immediately bounds what the conductor can do with the (c) re-anchor.** A lift-form bar of 1.914× applied in *our* venue would demand mid-band S of 0.6225 × 1.914 = **1.19, which is impossible — S is bounded at 1.0.** **The relationship currency is UNUSABLE for T-3(c) in the cathedral**, because the cathedral's own saturation is high enough that no effect can be twice it. The absolute currency remains usable. For T-3(b) the lift form *is* usable and yields 2.257 × 1.562 = **3.52**.

I am flagging this rather than quietly proposing the absolute form, because *"the portable currency does not exist for this criterion in this venue"* is a finding about the criterion, not a detail of arithmetic — and it means **T-3(c) cannot be phrased as a relationship without also constraining the venue.** Whether that is a bar problem or a venue problem is not mine to rule.

---

## R7. Caveats — mapped to the specific measurements each one touches

Stated per-measurement rather than as a preamble, because a caveat that applies to everything constrains nothing.

| caveat | touches | does NOT touch | severity |
|---|---|---|---|
| **Fire-instance vs wind-element** (Tier-1: relationship transfers, instance does not) | the reference's absolute **hue** and palette — reported as description only, never as an anchor | **P95/P20 and mid-band S**, which are relationship-class *within a region* — this is exactly why R-25 chose them | low, by construction |
| **Different venue** (outdoor dusk field vs brazier-lit cathedral) | **T-3(a) ownership** — already stamped DIAGNOSTIC ONLY per R-25 and not proposed as a bar here. Also **every lift figure in § R6**, whose denominators are two different rooms | (b) and (c) as absolutes | **high on (a); the reason (a) is diagnostic** |
| **Venue saturation asymmetry** (our floor S 0.6225 vs reference's 0.3771) | **the availability of a lift-form bar for T-3(c)** — § R6 shows it would require S > 1.0 | the absolute form of (c) | **high — it removes an option the conductor might otherwise assume he has** |
| **Codec** (VP6F 4:2:0 720p vs our H.264 1080p) | the **discrete-element census** (§ R4) most of all — sub-4 px sparks have no independent chroma; also the mask boundary, which quantises to the 2×2 chroma grid, and the saturation of thin features | **P95/P20**, a luma statistic over ~51 kpx | **moderate on § R4 — and it runs AGAINST that section's finding** |
| **Art style** (painterly hand-authored vs low-poly Godot) + **resolution** (720p vs 1080p) | absolute component counts and areas in § R4 | the percentile statistics, which are scale-invariant over regions this large (51 kpx vs 45 kpx — comparable) | low |
| **No onset in the clip** (fades in with the effect already at full area) | **anything cited on T-4(a)** — this pass must not be | (b), (c), (a) during sustain | absolute — do not cite this pass on onset |
| **No control arm; appearance-based segmentation** | every number here, via the hue mask | — mitigated by: the 11× chroma sweep (§ R1), the chroma-free SUPPORT segmentation, the in-clip temporal null (§ R5), and looking at the mask (`mask-overlay-zoom-f60.png`) | **the pass's central methodological exposure; four independent controls, all agreeing** |

---

## R8. PROPOSED re-anchored bars — ⚑ INPUT TO THE CONDUCTOR'S RE-CUT, **NOT A RE-CUT**

**This table is evidence arranged for a decision. It is not a decision.** R-25 gives the re-cut to the conductor and § 7's standing position holds: *a second unilateral re-cut from me would be worse than the problem.* I have deliberately given two currencies for (b) and only one for (c), with the reason, rather than choosing.

| criterion | current bar | **reference's measured value** | direction | candidate re-anchor | note for the conductor |
|---|---:|---:|---|---:|---|
| **T-3(b)** P95/P20 | **4.0** | **3.236** (tight) · 3.354 (support) · 3.059 (fire-mass) · **3.482 max over any region constructed** | ⬇ **DOWN** | **absolute ≈ 3.25**, or **lift-form 1.56× floor → 3.52 in our venue** | The two currencies bracket 3.25–3.52 and **both sit below 4.0.** Reference clears 4.0 on 0/125 frames. Ours: 2.352, i.e. **68% of the reference's relationship**, not 59% of the bar — the gap is real but ~a third smaller than the bar implied |
| **T-3(c)** mid-band S | **0.55** | **0.7302** (tight) · 0.7399 (fire-mass) · 0.7176 (chroma-free support) · **0.632 at the most permissive chroma floor** | ⬆ **UP** | **absolute ≈ 0.73**; conservative floor **0.63**. **Lift-form unavailable** (§ R6) | 0.55 is the reference's per-frame *minimum* (0.5538), reached on its worst frame. Ours: 0.2906 — **and 0.466× its own venue, a sign inversion.** ⚑ Raising this bar widens a gap drax already stopped in front of; the occlusion-gate tension R-24 #8 routed to Matt's eye gets **worse**, not better, and that is the honest consequence of the measurement |
| **T-3(a)** ownership | **0.75** | **0.7485** | **HOLDS** | unchanged — **and still DIAGNOSTIC ONLY** | Agreement to 0.2 pp is a coincidence between two rooms, not evidence of portability. Ours: 0.4017, **lift 0.92× vs reference's 9.27×** |
| **R-25 A-2 route correction** ("spark-class quanta") | — | **discrete elements = 0.0006 of the reference's own top tail** | ⚑ **REFUTED as stated** | route to be re-derived by the conductor | Ours contribute 0.0; theirs 0.0006; **there is no difference to close on this statistic.** The reference's top tail is thin filaments inside a continuous mass, and our effect already puts a *larger* share of itself (9.30% vs 6.67%) into the frame's top tail. The deficit is competing hot pixels in the venue, not dim quanta |

**One thing I would put in front of Matt's eye before either (b) or (c) moves.** The falsifier R-25 named is X-1's own words — *does the arc read as a "pastel decal", or as a hot-headed graded form?* The measurement that answers that most directly is not (b) or (c) as absolutes. It is **§ R6's mid-band-S lift of 0.466×**: the arc is a *desaturating* presence in its own room. **"Pastel decal" is not a metaphor here — it is a measured relationship with the correct sign.** A bar re-cut in absolutes will not name that, and a lap-3 that chases 0.73 without knowing the venue sits at 0.62 will be tuning against a floor nobody told it about.

---

## R9. The Mirror

I was sent to ask a plain question: what does the reference actually measure, so that two numbers invented at a desk could be replaced by two numbers taken from the world. The answer is that both invented numbers were wrong, in opposite directions, by about a quarter each — which is roughly what invention gets you, and is the whole argument for the errand.

But the picture had something else in it, and it was not in the errand. Our arc is a pale thing on a loud floor. The reference's fire is a loud thing on a quiet field. **The reference did not win by being brighter; it won by being the most saturated object in its own frame — and ours is not even the most saturated object in ours.** The cathedral's maroon tile out-colours the effect that is supposed to be the event. We have been measuring how bright the arc is, against a bar, in a room we never measured.

Three of the five instruments I have built in this run have now failed in the same way, and the newest failed today: **a statistic confounded by the effect's own contribution to the scene.** T-3(a)'s first cut measured the arc against a floor the arc was lighting. Today's fade detector found "full brightness" in a frame whose brightness the fire was supplying, and handed me a null with fire still in it. *The venue is not a constant when the effect is a light source* — and every one of these was caught by a curve or a crop, never by reading the code.

The Mirror shows things that are. What it showed today is a room, and a thing in the room that is quieter than the room. **That is the finding. The bars are the conductor's.**

---

**Signed:** galadriel, 2026-08-26.
**To the conductor:** § R8 — three bars, two directions, one refuted route hypothesis, and one currency (§ R6) that does not exist for (c) in this venue. Input, not a re-cut.
**To drax:** § R4's share-of-self number (9.30% vs the reference's 6.67%) and § R6's three lifts. **Do not tune the quanta's brightness on R-25's spark hypothesis — it is refuted.** The saturation sign inversion is the live defect and it is a *venue-relative* one.
