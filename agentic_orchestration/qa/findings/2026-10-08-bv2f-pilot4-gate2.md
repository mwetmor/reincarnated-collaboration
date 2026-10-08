# Finding — 2026-10-08 — BV2F PILOT 4 Gate-2

**Reviewer:** jack-ryan (DEV-MODE, BLOCK authority)
**Severity:** **BLOCK-narrow.** It halts the **Phase 3′ paint release only**, until § 6 [B] items close and Matt rules at M2″. Pilot 4 = **FAIL as a parity proof.** The build artifact is **accepted** as the M2″ look candidate. M2″ is **not** blocked.
**Target:** PT `6861bfc32` (painting `7105731298ef`; PS4 canvases per `fid/pt/pilot/build_manifest_ps4.json`; DEV-23/25/26/27 + DEV-24 on); PH `0be9a9d17` (calibration.md § 47, `fid/ph/results/pilot4/`); ledger R-C9-232..266
**Developer:** drax (PT, LV), galadriel (PH); conductor gandalf
**Principles applied:** REVIEW_PROCESS #1 (math before code), #2 (control before claim), #4 (charter + ledger as truth), #5 (severity matters)
**Governs:** charter `agentic_orchestration/gandalf/notes/2026-10-06-barrow-v2-fidelity-run-charter.md`:
- § 5 / § 6 ("first failing gate stops the phase → forensic → one variable → pilot only");
- § 12 W-1 ("re-instrumented or discarded; never threshold-tuned"), W-3 (DEV-13/14 need Matt pre-authorisation), W-4;
- § 15 / 15.1;
- R-C9-189 (the pilot sits at the wavefront origin and is **KEPT**);
- my P5 pre-ruling `309c4c41b` (M-1..M-4).

**Correction to my own pre-ruling.** `309c4c41b` cited W-4 as "the pilot is a proof, not a keeper". Under § 15 that is wrong. **R-C9-189 made the 3×3 pilot a keeper** (W-4 option i): Phase 3′'s column-3 and row-3 chunks take its raw canvases as paste context. Every pilot residual therefore **persists into the M3′ site** unless it is repainted. This finding is written on that basis.

---

## 1. Verdict, row by row

Probe numbers marked † are mine: read-only, on the archived painting and stitch, not binding. They reproduce PH's flags-ON values exactly (P5(b) 0.724; P4 5 binding fails).

| Row | Pilot 4 | Verdict | Note |
|---|---|---|---|
| P1 | all 1.000 | **PASS** | — |
| P2 | 25/25 | **PASS** | — |
| P3 | worst 11.16; sea 5.81 base-only | **PASS** | R-C9-201 exemption as disclosed |
| P4 ice | ΔE 0.79–8.81 against the PS4 mere | **PASS (Matt-ruled reference, R-C9-262)** | **Condition C-1:** the harness's `PH_ICE_REF=self` **re-derives the reference from the build under test**, so on pilot 4 the palette leg is a within-build uniformity check. Legitimate here, because Matt ruled *this* colour. It must be **frozen numerically** at Lab (64.58, −2.75, −21.49) for every later build. Sketch-A ΔE 10.05–23.37 stays reported. |
| P4 snow | 4/9 chunks FAIL (0_0, 1_0, 0_1, 0_2; spectrum; 1_0 histogram as well) | **FAIL** | † DEV-24-independent: the same 5 binding fails flags-on and on the dry stitch `a25fb3`. All 4 failing chunks have **small, fragmented snow support** (27.7k–174k px, against 125k–801k for the passing chunks). That is noted, not used (§ 4). |
| P4 rock 2_1 | spectrum 0.323 (bar 0.19) | **FAIL** | Persists from pilot 3 (0.303), so it is structural (§ 4) |
| P5 a1 | 19.14 at 2_0/2_1, 13.22 at 1_1\|2_1, 11.27 at 1_0/1_1 | **FAIL, cause diagnosed** | The service redrew the shared mere strip a darker blue (ΔRGB −27/−20/−11). a1 is binding on raw canvases by design (M-1). The stitch corrects the painting: c flags-ON 9.95, under v1's 17.42. |
| P5 b | 0.724 | **PASS** | † DEV-24 OFF: **0.786** at x = 1408. DEV-24 did not create the pass, but the margin is 0.013. |
| P6a | 2 declared, 0 invented | **PASS** | Measured on the DEV-24 painting, which is correct (it is what ships) |
| P6′ | 57/57 | **PASS** | — |
| P8 | min 0.5777 | **PASS** | — |
| P9 sway / flow / trail | 5.33 / 7.52 / 1.000 | **PASS** | — |
| P9c | n-insufficient | **NO READING** | Owed on the first Phase 3′ floe build (R-C9-189 W-5) |
| P10 | start worst p99 25.41 (p50 16.17–16.30); sea 20.64 | **FAIL** | Content cost; deterministic hitches (§ 3) |
| P11 v3 | valid (catch 12/12); 30/40 | **FAIL, valid** | Disposition in § 2 |

**Why this is FAIL and not PASS-with-conditions.** Four binding rows fail on a window that is **kept**. Charter § 5 / § 6 hold the phase on a failing pilot gate. A gate cannot convert four FAILs into a PASS by attaching conditions.

**Why it is not a BLOCK on the build.** Every failure is **measured and disclosed, not masked** (§ 5 probes). The build is pinned, reproducible and verify-green. The Tier-B discipline is intact (`fid/v1tools/verify.sh` exit 0†).

**Why the BLOCK is narrow, on Phase 3′ paint.** The pilot's raw edge canvases become Phase 3′ paste context. Opening Phase 3′ on a not-at-parity kept base is a **commitment Matt makes at M2″**, not the conductor (ESCALATE, ADR-002).

## 2. P11 and a Matt-ruled class departure

**Pre-registered exclusion for future runs: YES, under a rule that cannot become a tuning knob.** Ice was a Matt-ruled departure from v1 **before P11 v3 was built**: R-C9-203 made sketch A's ice a Matt-ruled palette DEV at § 38. Nobody excluded it, **this gate included**. My pilot Gate-2 required catch trials (F-5), not a class rule. The consequence is arithmetic, not judgment:
- 13 of the 40 scored trials were ice, which is discriminable by ruling.
- PASS (≤ 26/40) therefore needed **≤ 13/27 on non-ice**.
- For a build genuinely indistinguishable on non-ice, P(X ≤ 13 | n 27, p ½) = **0.50**, against the designed 0.96 (§ 38 operating table).
- **The instrument as composed could not do its job on this build.**

**Rule (PH pre-registers in calibration.md before any Phase 3′ P11 set is built):**
1. A class is excluded from **scored and repeat** trials iff:
   - (a) v1 has no such class (reed; this is already the practice), or
   - (b) a **Matt ruling of record (verbatim choice in the ledger)** directs that class's *look* away from v1.
   The list is written by ruling ID: **ice ← R-C9-203 / 255 / 262**. The conductor cannot add to it. A class is never added after any judge has read a set built under the old list.
2. Each excluded class names its **substitute guard**:
   - ice → P4 ice against the **frozen** PS4 Lab (C-1), the ice spectrum against sketch A, and Matt's eye at M3′;
   - reed → P4 reed advisory and Matt's eye.
3. The 40 scored trials are drawn from the remaining classes under the same content controls. **If 40 cannot be drawn, the set is VOID (I-4). It is never shrunk.**
4. Catch trials are unchanged. The two G2-B2 sets (v1rec vs v1head must PASS; v1 vs half-density must FAIL) are **rebuilt under the new composition and judged once each** before P11 binds at M3′.

**Pilot 4's 30/40 is dispositioned as: FAIL, valid. NOT re-scored. NOT re-judged.**
- **Ice 13/13: cause diagnosed.** The judge's cue ("flat even blue sheet with sparse thin cracks" against "dark mottled slabs with thick white cracks") is R-C9-255 ("mostly unbroken … few soft veins") plus R-C9-262 (blue) verbatim. That is a pre-registration gap, not a paint defect.
- **Non-ice 17/27: NOT a demonstrated pass.** It is not a pre-registered statistic. It is underpowered against the 40-trial minimum. On the null it reads P(≥ 17) = 0.12. The conductor was right to decline the post-hoc exclusion. More important, it carries a **candidate real cue**. When the judge was confident on non-ice, the evidence was "fine single-pixel speckle on the paper grain" in the pilot's snow and heather, and it was **9/11 correct** (trials 07, 12, 17, 22, 28, 39, 46, 49, 61 right; 21, 41 wrong). The judge's weak calls were 8/16, which is chance. That subset is post-hoc and **not binding**. It agrees in direction with the P4 snow spectrum FAIL. **It is the lead for § 4's forensic, not a verdict.**
- INFO: in trial 21 the judge took a *v1* crop's "stippled, halftone-dotted blue shadow patch" for the pilot. v1 itself carries some shadow stipple. DEV-28 removes the guide's dither, so it may remove a trait v1 partly had. This is one observation, recorded only.

## 3. P10

**Is the bar reachable on this machine?** **Yes, for this class of content**:
- the Phase-2′ pilot passed § 34 (16.54);
- PT reproduced phase2p at p50 13.45 today (R-C9-254);
- v1 carries 3× the heather sprays inside its budget.

**Not with the current dress.** The start view's **p50 is 16.17–16.30 ms**, which is the budget spent before any burst. Run 1 has no hitch above 20 ms and still reads p99 17.25. **No burst rule, however defined, passes this build.**

**The "OS bursts" diagnosis does not fit pilot 4's data.** In `results/pilot4/p10_rule.json`:
- the large start hitches sit at **4.73 s and 4.72 s** in two separate fresh processes (35.4 and 32.8 ms);
- the sea hitches sit at **13.0–13.4 s and 12.2–12.4 s** (up to 50 ms) in two of three runs.

Random OS work (mediaanalysisd) does not align to 10 ms across fresh processes. **These are build stutters at a walk position.** First hypothesis to test, with no images: the R-C9-200 load-time warm-up predates the reed cards (DEV-21; 107 now) and other post-warm-up materials. Check its coverage.

**Instrument discipline. Pre-register in calibration.md before the next P10 measurement. The binding bar is unchanged and no frame is ever excluded from it.**
1. **Quiescence precondition, checked BEFORE launch and logged.** No non-Godot process above 10 % CPU averaged over the 30 s before launch; name the usual offenders (mediaanalysisd, photoanalysisd, mds_stores, backupd). If it is not met, the run **does not start** and you wait. This is never a discard after the fact.
2. **In-run process log at 1 Hz.** A run is **VOID** iff a non-Godot process exceeds 25 % CPU for ≥ 1 s during it. A VOID run means the set of three is re-run, as § 34's crash rule. **Two VOID sets → HALT to the conductor.** Host-level mitigation (e.g. excluding the data volume from Spotlight or media analysis) is a `matt_to_do`.
3. **Session witness (control before claim).** Record v1's `barrow_full` under § 34 once now, quiesced, as the machine reference. Every P10 session runs it first; out of its recorded envelope (± 0.5 ms p50) → the session is VOID.
4. **Binding statistic unchanged:** worst-of-3 p99 ≤ 16.7 ms. **New binding check, stricter and pre-data: DETERMINISTIC HITCH.** Any frame > 25 ms recurring within ± 0.5 s of walk time in ≥ 2 of 3 runs = FAIL, whatever the p99. A 2-frame 35 ms hitch is 0.2 % of 900 frames, invisible to p99, and the player meets it every time (R-C9-200's own reasoning).
5. **Reported, non-binding:** burst-excluded p99; burst count and timestamps per run.

**Content lever, in this order:**
1. **The deterministic hitches**, traced and fixed.
2. **Look-neutral cost cuts**, each proven by R-C9-200's method (12-still diff below same-build noise):
   - the ~1.7 ms unattributed since phase2p (R-C9-256);
   - reed-card and heather instancing / LOD;
   - shadow casting off for distant sprays and cards;
   - sea foam cost.
3. **Heather thinning, last, and bounded.** Never below **v1's sprays per painted m²**. Matt asked for v1's 3D plant life (R-C9-244), and v1 ran 954 sprays inside budget, so thinning is the wrong first lever. If it is used, it is proven look-neutral by a **targeted ABX: thinned vs unthinned, same painting and views, 40 heather trials + 12 catch, P11 v3 machinery, PASS iff ≤ 26/40**. A FAIL makes it a look change, which goes to Matt. P8 is re-run.

**Engineering target before the Phase 3′ BUILD (not a bar):** start p50 ≤ 15.0 ms, because Phase 3′ only adds load. P10 does not gate Phase 3′ *painting*.

## 4. P4 snow grain, P4 rock 2_1, P5 a1: fix before Phase 3′ vs carry as known

**Fix before Phase 3′ paints [B]: the snow-grain forensic (0 images).**
- Locate the speckle cue: take the confident-trial crops (07, 22, 25, 26, 39, 61) at the same plate px in the **painting** and in the **still**. Painting-side means paint grain. Render-side means DEV-18 snow / pen / shader, a build fix with no images.
- Report P4 snow **window counts per chunk** (support). A minimum-support rule may be pre-registered **for Phase 3′ only**, calibrated on v1's own low-support chunks, and **never applied to pilot 4**.
- If the cause is painting-side: **one named direction change**, trialled on the first Phase 3′ chunk, with **P4 snow added to per-chunk auto-QA**.
- Reason this cannot wait: **0_2's bottom strip is chunk 0_3's paste context.** The painter continues the grain it is handed.

**Carry as known, disclosed at M3′, unless Matt orders a repaint at M2″:**
- **P5 a1 at 2_0/2_1, 1_1|2_1, 1_0/1_1.**
  - All three are internal joins: no Phase 3′ chunk pastes from them.
  - The mere ice is **99 % inside the pilot**† (38k ice px outside), so the mechanism (a large, uniform, saturated blue field redrawn at a different tone) has almost no Phase 3′ surface.
  - The painting is stitch-corrected and the 1:1 crops show no line.
  - **Under M-1 this stays a FAIL at M3′ until Matt accepts it or the pilot is repainted.** a1 does not move to the stitched painting.
- **P4 rock 2_1.** Forensic owed before M3′: 2_1 is the stone circle. Are these the clean-cut dressed tops Matt asked for (R-C9-244(b)), or paint? Report which. It is not a bar question.
- **4 pilot snow chunks** (kept), with the forensic result attached.
- **2_1|x2816 faint snow line** (R-C9-264), **P9c**.

## 5. Tier-B stack, DEV-23..28: masking

- **M-1 (raw a1): HELD, and it did its job.** It is the only instrument that saw the mere redraw. Keep it raw.
- **M-2 (DEV-25 matches amplitude, not scale):** stands. The speckle cue may be a grain-scale difference that DEV-25 cannot see. That goes to the § 4 forensic.
- **M-3 (DEV-23 feathers straight content edges):** § 44's masking control holds (PS3b FAILs via a1). Nothing new.
- **M-4 (masked medians): CLOSED** by R-C9-261 (the all-class measure governs the stop).
- **M-5 (NEW, DEV-24): WARN.**
  - DEV-24 repaints **13 % of the pilot painting** (1.36 M px†, mean |Δ| 30) with an image-service call **outside v1's brief and geo**, and pastes it **after** the stitch.
  - It cannot touch a1 (raw).
  - † It neither creates nor hides a pilot-4 verdict: P5(b) 0.786 OFF against 0.724 ON (both PASS); P4 has identical binding fails on and off.
  - **Its seam patches (seam1/seam2) are seam-repair canvases in substance, i.e. DEV-13**, which § 12 W-3 reserves for **Matt's pre-authorisation at M2** and caps in Phase 3 at ≤ 1 per seam and ≤ 15 % of chunks.
  - DEV-23/27 (local low-frequency colour correction) are DEV-14-adjacent.
  - The conductor's Tier-B rulings were procedurally clean. **The Matt-level ratification these entries need has not happened.**
- **Re-verify:**
  - **(a) DEV-24 against the full-site stitch [Bb].** DEV-26 cuts **one DP path per GLOBAL band** (`guided_stitch.py`, Tier-B, l. 205–286). Adding columns 3–4 and rows 3–4 lengthens every pilot band, so the optimal path, and with it DEV-27's composite, **can move pilot pixels**. DEV-24's layer check will then **HALT by design** ("a changed base HALTs").
    - Prove **pilot-region pixel identity** in the full-site stitch outside the new joins' zones (x ≥ 3840, y ≥ 2304),
    - **or** rule a re-base: pin the pilot's recorded band paths, or re-stage DEV-24 on the new base with a crop re-review.
    - † DEV-24 changes **0 px** in the pilot's outgoing paste strips (x ≥ 3840, y ≥ 2304), so the **paste context is unaffected**.
  - **(b) `fid/pt/pilot/stitch_record.json`** says `"_what": "... Tier A ..."` and records only `dev24: true`. INFO: record all five flags. The label is stale.
  - **(c) DEV-28:** guide-only, tested. INFO only (§ 2, trial 21).
  - **(d) DEV-23/25/26/27 flag-off byte identity:** carried, with no new evidence needed. verify.sh is green†. `guided_stitch.py`'s Tier-B sha `5fdcb9e5…` matches SHA256SUMS.

## 6. Phase 3′ entry checklist

[B] = before the first Phase 3′ paint burst · [Bb] = before the Phase 3′ build · [M] = Matt

1. **[M] M2″ ruling.** Matt sees pilot 4 with the FAILs stated plainly: P4 snow 4/9 + rock 2_1; P5 a1 ×3 stitch-corrected, with crops; P10; P11 30/40 valid FAIL with the ice cause and the non-ice speckle lead. He rules one of:
   - **accept the kept pilot** (PS4 + DEV-24) as Phase 3′'s base with these as disclosed residuals;
   - **pilot 5.**
   **No Phase 3′ paint without this ruling.**
2. **[B][M] Consolidated DEV register.** Charter **§ 16 does not exist**. It has been owed since R-C9-202 F-1. It must hold DEV-17..28 + DEV-25c, each with reason, measurement and ruling, plus one Matt ratification line at M2″ naming:
   - DEV-23/27 (DEV-14-adjacent);
   - **DEV-24 (incl. DEV-13-in-substance seam patches; 13 % of pilot px outside v1's brief)**;
   - DEV-28;
   - Phase-3′ DEV-24 use counted against the repair cap.
3. **[B] The LV source fixes are NOT Phase 3′ paint prerequisites as listed.** †In the current guide (ids `9e6b303f…` = the PS4 pin), **`mere_cracks` (id 42), `reed_tufts` (id 47), and `cradle_cracks` (id 6, also class *sea*, the same dark-crack mechanism, not on the conductor's list) are 100 % inside the pilot window.** No Phase 3′ canvas contains them. The conductor rules one of:
   - **(a) pilot kept:** the fixes are blockout-of-record hygiene, and the Phase 3′ guide is re-pinned with the pilot tiles' difference recorded *known and inert* (R-C9-191 precedent);
   - **(b) pilot 5:** under R-C9-189, changing the pilot tiles means a repaint.
   Fix `cradle_cracks` with `mere_cracks` in either case.
4. **[B] Bay: CLOSED.** Record the closure. R-C9-259/260's both-sides fix was painted in PS4: a1 at 0_1/0_2 went from 10.54 to **6.02**, raw MAD from 13.81 to 11.36.
5. **[B] DEV-25c:**
   - registered as a DEV;
   - **A/B on the first Phase 3′ wavefront chunk** (both arms, +2 images inside the Ph3′ retries), with the adoption rule pre-registered: adopt iff a1 is not worse **and** the boundary line is gone at 1:1; the losing arm is discarded;
   - **P5 a1 re-instrumented for the inner-128 paste geometry** (a1 over the pasted inner band; v1's bar re-derived on v1 under the same restriction; C1–C3 analogues), committed **before any Phase 3′ P5 value is read**. v1's 9.569 was set under a full-256 paste and does not transfer.
6. **[B] Snow-grain forensic (§ 4)**, and the result folded into the Phase 3′ direction and the per-chunk auto-QA.
7. **[B] P11 pre-registration (§ 2)**, committed before any Phase 3′ P11 set.
8. **[B] P4 ice reference frozen** at Lab (64.58, −2.75, −21.49); `self` mode retired (C-1).
9. **[B] Phase 3′ per-chunk auto-QA list.** Charter Phase 3 reads "invention check first, then P5–P7". Restate it as: P6a, then raw a1 per join with the "stitch-corrected" crop rule, then P4 snow per chunk. P7 is retired.
10. **[Bb] DEV-24 survives the full-site stitch (§ 5 (a)).**
11. **[Bb] P10 (§ 3):**
    - instrument discipline pre-registered;
    - deterministic hitches traced and fixed;
    - start p50 ≤ 15.0 ms via look-neutral cuts;
    - heather thinning last, bounded, ABX-proven.
12. **Carried as known to M3′:** P5 a1 ×3 (pilot-internal); P4 rock 2_1 (forensic owed); 4 pilot snow chunks; 2_1|x2816 faint line; P9c (first floe build).

**INFO.** Budget: BV2F image calls on record are **138** (Phase 2′ ≈ 122 across PT/PS/PS2/LR/PS3/PS3A/PS4/LR4, against R-C9-189's original 18, every step re-based by ruling). That leaves 112 under the ~250 run guard; Ph3′ (35) plus a possible pilot 5 (≤ 24) fit. Recorded so that M2″'s option (b) is costed honestly.

## Action

- [ ] **Matt (ESCALATE, M2″):** keep pilot 4 as Phase 3′'s base with the named residuals, or pilot 5. Ratify the DEV-23..28 line (§ 6 item 2).
- [ ] **Conductor (gandalf):**
  - record this as a ledger row;
  - write charter § 16;
  - rule item 3 (kept + inert, or pilot 5) and add `cradle_cracks`;
  - put the M2″ packet's FAIL lines as stated in § 1;
  - record the bay closure.
- [ ] **PH (galadriel):**
  - § 2 P11 rule and the G2-B2 rebuild;
  - C-1 frozen ice reference;
  - § 3 P10 pre-registration and the v1 session witness;
  - a1 re-instrumentation for DEV-25c;
  - P4 snow support report.
- [ ] **PT (drax):**
  - snow-speckle forensic (painting vs still);
  - P10 hitch trace at start 4.72 s and sea 12.2–13.4 s (warm-up coverage first), then look-neutral cuts;
  - DEV-24 full-site-stitch identity proof or re-base proposal;
  - `stitch_record.json` flags;
  - DEV-25c A/B harness;
  - rock 2_1 forensic.
- [ ] **LV (drax):** after the conductor's item-3 ruling, `mere_cracks`, `reed_tufts` and `cradle_cracks` at source.

## References

- Ledger `astra_test_01/burst/runs/C-9/ledger.json` R-C9-189, -191, -200, -202, -203, -232..266
- `astra_test_01/burst/runs/C-9/barrow_v2/fid/ph/calibration.md` §§ 34, 38, 39, 44–47; `fid/ph/results/pilot4/{p4,p5v2,p10_rule,p11v3_build,tierB_dev_records}.json`
- `fid/ph/p11/keys/abx3_pilot4_v1_vs_pilot.json`, `fid/ph/p11/answers/abx3_pilot4_judge.json` (scored independently: ice 13/13, snow 6/9, heather 11/18; catch 12/12; repeats 6/10)
- `fid/pt/pilot/{painting.png,stitch_record.json,build_manifest_ps4.json}`; `fid/pt/ps4_dry/painting.png` (a25fb3, DEV-24 unset); `fid/pt/dev24/{dev24_block.json,painting_dev24.png,spec_ps4_*.json}` (pixel-equal to the build painting†)
- `fid/v1tools/{ALLOWLIST.md,SHA256SUMS,verify.sh,dev24.py,dev28.py}`, `fid/v1tools/tierB/conductor_scripts/guided_stitch.py` (DEV-26 global-band DP, l. 205–286)
- `fid/lv/guide_art/{guide_manifest.json,ids_art.png,class_art.png}` (crack/reed id extents)
- `fid/RESUME_PT.md` (R-C9-247..264 sections); `fid/pt/m2pp/M2pp_pilot_sketchA_v1.jpg`
- Prior: `agentic_orchestration/qa/findings/2026-10-08-bv2f-p5-dense-texture-preruling.md` (`309c4c41b`)
