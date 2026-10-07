# Finding — 2026-10-07 — BV2F Phase 2′ PILOT Gate-2 (before M2′)

**Reviewer:** jack-ryan (DEV-MODE, BLOCK authority)
**Severity:** WARN (verdict **PASS-WITH-FOLDS**; 0 BLOCK)
**Target:** PT `776e265f0`…`186743b58` (pilot build, HEAD of the pilot level `186743b58`); PH `4bd299a18`…`cb2571f9f` (calibration.md §§ 24–37); conductor rulings R-C9-188..201
**Developer:** drax (lane PT), galadriel (lane PH); conductor gandalf
**Principles applied:** REVIEW_PROCESS #1 (math before code), #2 (smoke gate / control), #4 (charter + ledger as truth), #5 (severity matters)
**Governs:** charter `agentic_orchestration/gandalf/notes/2026-10-06-barrow-v2-fidelity-run-charter.md` §§ 2, 5, 6, 7, 12–15.2

## Verdict

**PASS-WITH-FOLDS. M2′ may go to Matt once the packet folds (P-1…P-5) are in.** They are cover and sheet disclosures. No re-render, no image. **Folds F-1…F-6 are owed before the first Phase-3′ burst.** No conductor ruling R-C9-196..201 is tuning in disguise. Two are under-recorded (F-3, F-4).

## What I found (descriptive)

**Independently checked**

| Check | Evidence | Status |
|---|---|---|
| Final table | calibration.md § 37 (as corrected by § 36). Binding PASS: P1, P2, P3, P5, P6a, P6′, P8, P9 sway / flow / trail, P9c, P10. Binding FAIL: P4. VOID: P11 × 2. Every PASS row carries a RED that fails on the same instrument. | as stated |
| P11 void-rule math | Guesser inconsistency ~ Bin(10, ½)/10. P(≤ 2/10) = 56/1024 = 5.5%. A perceiver's inconsistency is 2p(1−p). I re-derived both. P(> 26/40 \| p = ½) = 1.9%. | confirmed |
| Ph2′ budget | Ledger: 9 `BV2F-PT-*` bursts × 2 image calls = **18 / 18**. Run BV2F total 24 (LV 6 + PT 18). | within cap, **cap exhausted** |
| v1 untouched | `git diff f1aa715ac HEAD -- barrow_full`: only `bv2f/` paths and `scenes/bv2f_*.tscn`. Untracked set == `pc/bf_status_before.txt`. **32 / 32 v1 control payloads** (painting, bakes, lit / painting / snow bins, manifest, heather) re-hashed by me against `pc/control_shas_phase1p_close.json`: identical. `v1tools/verify.sh` exit 0 (22 files; guided_paint.py moved to Tier B at `03d5278d4`, as § 12 DEV-10/11 required). | PASS |
| Positive control T1–T3 | Last measured `00db8970b` (07:47, HEAD 550682c73). `barrow_full` HEAD has since moved by 17 bv2f paths. **No pilot-Gate-2 re-measure is on record.** | owed (F-6) |
| Settle code | `bv2f_pilot.gd` `_ready()` (`186743b58`). Gated only on `painted && !is_web()`, with **no harness or env gate**. It runs about 230 driven frames + 30 presented frames with the knight hidden, at uv (11.5 → ~15.5, 15.5), then resets six private `knight.gd` fields by string `set()`. | build path, ships to players |

## Rulings on the four questions

### (1) P11: VOID ×2. Re-instrument with embedded catch trials. The pilot MAY reach Matt with P11 VOID.

- **The instrument is broken by construction, not by these judges.** The fixed generator (R-C9-171) draws a fresh X on each repeat. That makes repeat-consistency a chance variable under the null. The void gate and the pass bar are anti-correlated: a judge only validates if it can discriminate, and a build only passes if the judge cannot. **P(valid ∧ PASS) ≤ ~5% for every judge** (§ 28). The G2 v1-vs-v1 GREEN (22/40, inconsistency 0.10) is itself a 1.1% event under guessing. **It is therefore not a valid calibration of the current gate**, and § 13 G2-B2 must be re-run.
- **Same-X repeats: rejected.** They are what R-C9-171 removed: the half-density judge answered the repeat from memory. Consistency then measures recall, not attention.
- **Fixed-judge panel: not preferred.** A "judge" is a fresh model session. Calibrating one session does not certify attention in another.
- **Ruled design: embedded catch trials (attention / competence measured in the same session that produces the score).**
  - Interleave **12 catch trials**, format-identical and blind, drawn from a pre-calibrated, clearly discriminable pair. Use v1 vs R-C9-159 or v1 vs half-density, whichever calibrates at **≥ 0.95** per-trial accuracy.
  - **Valid iff ≥ 10/12 catches are correct.** Binomial: a guesser validates 1.9% of the time; a p = 0.95 judge validates 98%. PH confirms these numbers by Monte Carlo on the real key.
  - The 40 scored trials and the ≤ 26/40 bar are unchanged.
  - Repeat-consistency is demoted to a reported, non-binding diagnostic.
  - An always-A answer set must VOID.
- **Calibration before it binds, all pre-registered in calibration.md:**
  - (a) a Monte Carlo operating table: guesser VOID ≥ 95%; always-A VOID; P(valid ∧ PASS \| indistinguishable, attentive judge) ≥ 0.9;
  - (b) the catch pair's per-trial accuracy measured on fresh judges;
  - (c) § 13 G2-B2 re-run under the new design: v1-vs-v1 **valid ∧ PASS**, and v1-vs-half-density **valid ∧ FAIL**.
- **The pilot's answers are NOT re-scored under the new rule.** They had no catches, so re-scoring would be post-hoc. **Pilot P11 stays VOID.** The re-instrumented P11 binds at M3′ over the whole site, kept pilot chunks included.
- **M2′ with P11 VOID: allowed.** Principle 6 lets Matt see a decision request. VOID is neither a pass nor a fail. **But the cover must not let VOID read as "fine"** (P-1).

### (2) P4 FAIL → a Matt look decision at M2′: LEGITIMATE. The pilot does not repaint first.

- **The routing is legitimate.**
  - § 27 shows the guide, tint, light and brief text match v1. The departure is the painter's guide-to-paint transfer: ice −4 L\* where v1 had −18. So the toolchain replication is not wrong; the content differs. Principle 6 permits a decision request.
  - The charter already anticipates this path. DEV-14 (master colour transfer) is "Matt pre-authorization at M2, and only if P4 drifts".
- **Repainting first would be wrong.**
  - Without a method change it is a stochastic re-roll until P4 passes: fishing.
  - With a method change it is a new variable whose direction depends on Matt's answer.
  - Ph2′ is 18/18, so any repaint is a sub-cap HALT and a reserve re-base either way.
- **Conditions on the ask (P-2):**
  - The cover states **"P4 FAIL"**, not "look question" alone.
  - The sketch-A evidence is shown with **both** readings. By median it favours the pilot's pale ice (ΔE 11.0 vs 23.7). By histogram it is a tie (Hellinger 0.691 vs 0.685).
  - The brief's own ice words are *"flat lapis-blue ice"*. The pilot under-delivers "lapis" relative to v1. Say so.
  - **Coastal snow (0_2 / 1_2, b\* −1.5 to −1.9) is a separate line.** Sketch A was not read for snow, and an ice palette ruling does not clear it.
  - The options carry their costs:
    - (a) accept pale ice / cool coastal snow: a new Matt-ruled palette DEV;
    - (b) v1's lapis via DEV-14;
    - (c) repaint with a named method change. Images come from reserve or Ph3′.
- **Whatever Matt picks (F-5):**
  - P4 stays BINDING. Option (a) is a registered DEV that re-bases the reference **for the named classes only**, with the measured values. It is not a bar move and not a row reclassification (§ 13).
  - The Phase-3′ P4 reference for coastal snow is pre-registered before the first Phase-3′ burst, because the same painter will paint the remaining coastal chunks.

### (3) Instrument-touching rulings R-C9-194..201: none is tuning in disguise. Two are under-recorded.

| Ruling | Change | Ruling |
|---|---|---|
| R-C9-194 | P6a: sea / mere routed to conductor triage, not auto-pass | **Legitimate** (v0.1 was calibrated on a site with no sea). PH concurs independently. Post-data, so the § 13 G2-B1(4) MATERIAL sheet must be in the packet (P-3). |
| R-C9-196 | P8: PT fixes the heather-mask input; PH's exclusion is withdrawn | **Legitimate.** An input defect, fixed at the input. RED retained. 0_1 / 0_2 were n/a in both builds. |
| R-C9-196..198 | P9c re-instrumented (§ 30 → § 31 + A1) | **Legitimate.** Pre-registered before the counted measurement. A1 was triggered by a marker that drew nothing, not by drift data. RED 1.766 fails. Thin: **n = 1 floe, 4 pairs** (F-4). |
| R-C9-197 | paint_mix 1.0 → 0.75 | **Build change on a hypothesis**, falsified (1.524 → 1.551) and correctly withdrawn. But 0.75 was **kept**, and it departs from R-C9-194's "base = the painting". Its standing reason (parity with the R-C9-159 water Matt accepted) is not recorded at DEV-5 (F-3). |
| R-C9-198 | Foam field added; P9 flow on the "same water mask" | **Legitimate.** A build fix inside DEV-5's own referent, the bar held, the Matt fallback pre-committed, the mask fixed before measuring. Geometric floe exclusion (4.092) corroborates. The per-run mask leak (1.914) is an instrument defect, owed before Phase 3′, where no pre-foam mask exists (F-4). |
| R-C9-199 | P10 § 34 worst-of-3 | **Legitimate, stricter, pre-registered.** The refusal of PT's discarded warm-up run (R-C9-200) is the correct call. |
| R-C9-200 | Shadow-cast restored to v1's rule; load-time pipeline warm-up | **Legitimate build fixes.** Look-neutral is measured (still diff 0.10 < noise 0.19; time-phase only). |
| R-C9-201 | P3 sea: DEV-5 mover exemption extended from P2 to P3 | **Legitimate scope correction, ruled post-data, and the record mis-states the passing measurement.** The ruling says "held at rest", but **at rest the sea reads 21.62 (FAIL)**. Only the **painted base** (0.75 × painting + 0.25 deep_col) reads 5.73 PASS. So the player-visible still sea departs from the painting by 21.6 > 15.5. That is the DEV-5 look and must be disclosed, not just exempted (F-3, P-4). |
| R-C9-201 / `186743b58` | Hidden pre-control settle | See below. |

**The settle: acceptable as a build fix. It does not hide the remaining player stutter.**
- **It ships, so it is not a harness trick.** It runs in the level's own `_ready` for every desktop player, before `ready_done`, which gates control. The first-use costs it absorbs are the first footsteps, the first stop and the load tail. The player is spared them as well, the same as the warm-up.
- **It does not mask the measured window.** PH's § 37 trace still finds and reports a **7-frame mid-walk cluster (16.9–28.6 ms) at 12.4 s**. That stutter is real and after control, and it is why P10 passes with **0.16 ms headroom**. A cluster of 9 or more frames fails.
- **Conditions (F-2, P-5):**
  - (i) The player sees about 4 s of the start view without the knight, with the 55–95 ms load-tail frames presented. That is a visible load-in. Disclose it, and consider a veil for Phase 3′ (web already has `warm_veil.gd`).
  - (ii) The settle walks at uv 11.5 → ~15.5, v 15.5. That is outside the 3×3 pilot (u ≤ +7.1) but **inside the full 66 × 51 m window** (u to +32.6, row 0). In Phase 3′ the settle would stamp real footprints and puffs into painted, filmed ground for up to 60 s. Re-site it or clear the prints.
  - (iii) The six private `knight.gd` fields written by string `set()` silently no-op on a rename. Assert that they exist.

### (4) DEV register, budget, v1, control

- **Register of record is stale.**
  - Charter § 7 still shows DEV-5 as "P2 exemption only".
  - DEV-17, DEV-18 and DEV-19, plus DEV-5's extensions (P3 base-only exemption, paint_mix 0.75, the foam field, 17 bobbing floes), exist only in ledger prose.
  - The load-time warm-up + settle is a new start-up behaviour that v1 does not have. It is unregistered.
  - **Charter § 6 / § 7 text:** *"A departure found in flight that is not here is a HALT, not an entry"* → **HALT to Matt**. DEV-17/18/19 were conductor-registered instead.
  - Mitigation: all three are measured (DEV-17 is byte-identical on v1's data; DEV-18 is quantified; DEV-19 is a frozen tool's own `--size` argument, with P1 PASS). Matt sees M2′ next. **So the remedy is ratification at M2′, not a BLOCK** (P-4, F-1).
- **DEV-17 omits parts of v1.** v1's anchor/footprint self-checks, the tree search and section (c) are not run (R-C9-192/193). Name them in the entry.
- **DEV-18 residual.** 28.8% of painted tuft px have no 3D heather within 24 px (12.3% on slopes). The snow on slopes keeps the flat-field normal. The R-C9-193 mound-flank look check must be on the M2′ sheet (P-5).
- **DEV-16** is closed as not opened (124 ids). Correct.
- **Budget:** 18/18; reserve 14. Any P4 repaint is a re-base.
- **v1:** untouched (table above).
- **Control:** owed (F-6).
- **INFO:**
  - The final table is a cross-build composite: P9 sway / trail at `0b72461db`, P10 at `186743b58`. Per-row build shas are recorded, and still diffs show the later changes are look-neutral. A single-build sweep at the M2′ build sha is recommended before Phase 3′.
  - R-C9-194's rebuild changed four variables at once (DEV-19, DEV-5, DEV-18, lineage). Water contaminating the P3 / P8 inputs was the direct cost (principle 7).

## Action

**Packet folds: before M2′ goes (conductor / PT; text only):**
- [ ] **P-1.** P11 line: *"VOID ×2: an instrument defect found (a guesser voids ~95%); being re-instrumented; not a pass."* Show both raw scores. **Judge 1's 27/40 would have FAILED.**
- [ ] **P-2.** P4 ask framed as in (2): "P4 FAIL", both sketch-A readings, the "lapis" brief wording, coastal snow as its own line, options (a) / (b) / (c) with image costs.
- [ ] **P-3.** The § 13 G2-B1(4) sheet: the 5 MATERIAL sea crops with their overlays.
- [ ] **P-4.** One ratification line for the departures registered in flight:
  - DEV-17 (with what it omits), DEV-18 (with its residual), DEV-19;
  - DEV-5's extensions (paint_mix 0.75, foam, the P3 base-only exemption with the **at-rest residual 21.6 vs 15.5** stated);
  - the load-time warm-up + settle.
- [ ] **P-5.** The DEV-18 mound-flank snow look check (R-C9-193). The settle's knight-less load-in. The build sha behind the stills and film (they predate `789618d45` / `186743b58`).

**Before the first Phase-3′ burst:**
- [ ] **F-1 (conductor).** Charter § 16 with a consolidated DEV register: DEV-5 (amended), DEV-17, DEV-18, DEV-19, and DEV-20 (warm-up + settle). Each entry carries its reason and measurement, and records Matt's M2′ ratification.
- [ ] **F-2 (PT).**
  - Re-site the settle off the full window, or clear its prints before control.
  - Assert the `knight.gd` fields exist.
  - Localise the 12.4 s mid-walk cluster from the § 37 traces. Phase 3′ starts at 0.16 ms headroom.
- [ ] **F-3 (conductor / PH).** DEV-5 entry:
  - P3 for the sea reads the **painted base only**. "Held at rest" is the wrong label: it reads 21.62.
  - paint_mix 0.75 is kept for R-C9-159 parity, not for flow.
  - Optional: a graded RED (paint_mix 0.5).
- [ ] **F-4 (PH).** Pre-register two instrument fixes:
  - P9 flow exclusions from geometry (marker / ID), not cross-time differences;
  - P9c on a floe-field view with ≥ 3 in-plate floes (§ 30 option (c)).
- [ ] **F-5 (PH / conductor).** The P11 catch-trial design and calibration as in (1), with G2-B2 re-run. Also the P4 references that follow Matt's M2′ answer. **If P11 cannot be calibrated by M3′, it is recorded as dropped from the parity claim, not silently absent.**
- [ ] **F-6 (PT).** Positive control T1–T3 at pin `f1aa715ac` and at `barrow_full` HEAD (§ 13 W-4). Any difference is a HALT.
- [ ] **Matt (at M2′):** the P4 palette choice; ratification of P-4. **Nothing from this Gate-2 is escalated beyond the M2′ packet.**

## References
- `astra_test_01/burst/runs/C-9/ledger.json`: R-C9-188..201, `bursts` (BV2F-*)
- `astra_test_01/burst/runs/C-9/barrow_v2/fid/ph/calibration.md` §§ 24–37; `ph/results/pilot{,2..7}/`; `ph/results/pilot/p11_void_analysis_sim.json`; `ph/results/p6a_triage_pilot{,_conductor}.jsonl`; `ph/p11/answers/abx_pilot_judge{1,2}.json`
- `astra_test_01/burst/runs/C-9/barrow_v2/fid/pt/pilot/pilot_record.json`; `pt/perf/`; `pt/dev17/`; `pt/dev18/`; `pt/m2/M2p_pilot_beside_v1.jpg`
- `astra_test_01/burst/runs/C-9/barrow_full/godot/scripts/bv2f/bv2f_pilot.gd` (`c578db842` warm-up; `186743b58` settle)
- `astra_test_01/burst/runs/C-9/barrow_v2/fid/pc/control_shas_phase1p_close.json`; `fid/v1tools/verify.sh`
