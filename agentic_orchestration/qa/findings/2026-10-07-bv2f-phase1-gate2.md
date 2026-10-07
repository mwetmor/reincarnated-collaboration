# Finding — 2026-10-07 — BV2F Phase 1 Gate-2 (model kit v3, layout v7c, class-tinted guide, check (a), P6, M1 packet)

**Reviewer:** jack-ryan (DEV-MODE, Gate-2, BLOCK authority)
**Severity:** BLOCK-narrow ×1 (the P6 row) · 4 WARN · 5 INFO
**Verdict:** **BLOCK, scoped narrowly to P6.**
- Everything else in Phase 1 is accepted: model kit v3, layout v7c, validator 66/66, check (a) 6/6, the guide and ID render through the frozen tools, v1 untouched, budget.
- **Phase 1 does not close, and M1 does not go to Matt**, until G2P1-B1 folds (charter § 2 principle 6: Matt sees only harness-passing work or a decision request).
- **Nothing else is held.** Lanes may work the folds now. The fold costs 0 images and $0.
- **Ruling on H-C9-BV2F-PH-P1-1:** re-instrumentation is **legitimate**, on evidence that does not depend on v7c's score, **under the conditions in G2P1-B1**. The two candidate swaps named in the halt are **rejected as binding instruments**.

**Target:** collab `a3c5e9bfe` (R-C9-179). Lane commits reviewed:
- LV: `0a9eb7013`, `c0508f172`, `7c3d5741e`, `d4c59061f`
- PH: `2a913e7af`, `34866394a`
- PT: `dcf7cbc6a`

**Developers:** drax (LV), galadriel (PH), gandalf (conductor).
**Principles applied:** REVIEW_PROCESS 1, 2, 4, 5; Disciplines #9, #10, #11, #73, #75 (cl. 6), #80, #82; ADR-002, ADR-006.

---

## What I found

### Phase 1 DoD (check 1), as inspected

| DoD item | State | Evidence |
|---|---|---|
| Validator R1–R13 on the frozen layout | **PASS** | I re-ran `validate_layout_v7.py lv/layout_v7c.json`: 66/66 PASS, exit 0. The diff of the v7 copy against `barrow_v2/tools/validate_layout_v2.py` is 18 lines: docstring, `HERE`, and R9's text. No check changed. |
| Check (a), R-C9-177(a) | **PASS** | LV `check_a.json` 6/6. PH re-measured independently: reference areas within 0.13%, and the recount of the visible areas is exact (calibration.md § 14). The hall-door 8.22 vs 6.35 m² gap is explained by the curtain box: analytic 83,308 px vs counted 83,234 px. |
| P6 (geometry vs layout) | **VOID**: the instrument was never calibrated (G2P1-B1) | `results/p6_phase1_v7c.json` |
| Gate-2 | this finding | — |
| M1 | held | G2P1-B1, G2P1-W4 |

### G2P1-B1 · BLOCK-narrow · The Phase-1 P6 instrument was never calibrated, and its bar belongs to a different instrument

**What exists:**
1. **The instrument and its first result landed together.** `harness/p6_phase1.py` (ID render vs layout-prism IoU) was first committed in `2a913e7af`, the same commit as its first v7c result. Its calibration has no negative control and no constructed failure. `grep` finds no 159 run, no shift test and no constructed input in the tool.
2. **The bar 0.513 comes from another instrument.** It is the Phase-0 **P6b** statistic: a v1 model's silhouette against the **painted** non-ground class (`p6_geometry.py:14`), measured over 53 pieces. PH's own docstring (`p6_phase1.py`, para (2)) says the two measures differ. On the Phase-1 measure, v1 scores **0.635** (n 85) overall and **0.645** for real models excluding trees (n 23). Both values are recorded in the same result file.
3. **v1's like-for-like value is a population mix (#82).** It pools 29 primitives (where prism = mesh, so 0.819 almost by construction), 23 real models (0.645) and 33 trees (0.239). v7c's 20 objects are mostly organic crags and ruins in the new DEV-2 classes, which have no v1 counterpart.
4. **This pipeline fixes every model's bounding box to its prism.** `bv2f_level.gd:263-268` `_place_box` scales each model's AABB **per axis** to its slot. So for a model that is present, unoccluded and contained, IoU-vs-prism equals the share of its own projected AABB that its silhouette fills. That is a property of the model's shape, and the layout does not specify shape. Two consequences:
   - **The row cannot see C7.** A squashed or wrongly scaled model is forced to the same box and scores the same. C7 is the defect charter principle 3 names (uniform scale, ≤ 10% per axis).
   - **The row penalises organic shape.** The attribution confirms this: placement 0 (max 0.041), organic under-fill median 0.42, occlusion median 0.12.

**Ruling (as ratifier):**
- **R-C9-178's conduct was right.** Swapping to containment because v7c had failed would be threshold-tuning in disguise. Routing the question here was correct.
- **The row being defended was never a calibrated row.** The Phase 0 freeze binds the row's kind (P6 = quality) and its rule ("re-instrumented or discarded, never threshold-tuned"). It does not bind a bar that was never derived for this instrument.
- **Re-instrumentation is therefore legitimate, on evidence that does not depend on v7c's score.** Points 1, 2 and 4 are facts about provenance and code. They were true before v7c was rendered.
- **Candidate data has been seen, so the conditions are stricter than a pre-data re-instrumentation:**
  1. **Pre-register first.** PH writes P6′ into `calibration.md` and commits it before any v7c re-read. P6′ names the defect classes it must catch:
     - missing;
     - buried or hidden, unless the hiding is by design;
     - outside its slot;
     - extra;
     - wrong scale or squash (C7, ≤ 10% per axis);
     - **extent**: any R1–R13 rule that reads slot extent still holds on the model's own footprint and height.
  2. **Calibrate: v1 PASS, plus a RED for every component:**
     - presence: **v7c at `2a913e7af`**, this run's real negative (braziers missing, stones buried);
     - placement: a constructed shift of 1.5 m;
     - scale: a constructed non-uniform squash greater than 10%, such as v6's 3 m porch;
     - extent: a constructed shrunk model that breaks an extent rule, such as the gable moved past R10's 3.0 m.
  3. **Derive bars from v1's own distribution on the same measure, or from a written rule** (0 missing; anisotropy ≤ 1.10 under principle 3). No bar may be read off v7c.
  4. **Keep IoU-vs-prism as a REPORTED, non-binding row**, printed beside its like-for-like v1 value of 0.635. It is not deleted and not hidden from Matt.
- **The two candidates named in the halt:**
  - **IoU against each object's own placed-GLB silhouette: REJECTED as the binding instrument.** It compares the model with itself, so it is blind to C7. It may serve as the presence/occlusion component.
  - **v1's comparator recomputed the same way:** this already exists, and it gives **0.635**. Against it v7c fails by more, not less. If the conductor keeps IoU-vs-prism binding, the honest bar is 0.635, and **Phase 1 FAILS P6**.
- **What is already known, and where the risk lies.** Presence and placement are known to pass on v7c (containment 1.0, nothing missing). **The scale and extent components are unmeasured** (see W-2), and either may come back RED. That is why the calibration REDs carry the evidential weight. **If P6′ is RED on v7c,** LV fixes the real defect: a uniform-scale refit, or a prism tightened and the validator re-run. If the problem is one of look rather than geometry, it goes to Matt as a fork.

### G2P1-W1 · WARN · The positive-control re-measure at the pin is owed (§ 13 W-4)
- `fid/pc/` has no Phase-1 re-run of T1, T2 or T3. The last PT control commit is `075271a0b`, in Phase 0.
- **What I verified myself:**
  - all 32 `control_shas.json` files recompute exactly;
  - `git status --porcelain -- barrow_full/` equals `pc/bf_status_before.txt`;
  - every `barrow_full` commit since the pin `f1aa715ac` lies under the four allowlisted `bv2f` paths.
- So the risk is low, but the measured re-run is the gate's own requirement (#73).

### G2P1-W2 · WARN · Principle 3 (uniform scale) is unmeasured on 15 of the 20 P6 objects
- `_place_box` returns before `_register` for group instances (`bv2f_level.gd:271-274`), so their `fit_scale` is never recorded.
- `built.json` carries `fit_scale` for only 5 objects. All 5 are uniform or within 2%, which is fine.
- The 15 unrecorded objects (crags, stones, markers, braziers, beams) are fitted per axis to boxes that came from the procedural boulders.
- v1 records `fit_scale` in its per-model build record (`barrow_full.gd:1020`).

### G2P1-W3 · WARN · ID grouping is a usage change, not a Tier-B patch; it is recorded, but not as a deviation
- **The 256-colour limit is real.** `capture_ids.gd:98` encodes `Color8((idx%16)*16+8, int(idx/16)*16+8, 200)`, which collides from idx 256 upward.
- **The fix is not a patch.** `verify.sh` is green at review (21 files). The `capture_ids.gd` shipped sha `8990273bf49b` matches the sha in every v7c guide log. There has been no `v1tools` commit since `dcf7cbc6a`. The fix is the level grouping instanced slots and blobs under one ID each (43 in v7c).
- **Where it is recorded:** `RESUME_LV.md` and commit `c0508f172` only. It is not in any ruling and not in § 7.
- **Why it matters:** it changes v1's "one ID = one piece". That convention is consumed by:
  - the take (cutouts from exact ID masks, R-C9-155(4));
  - the DEV-10 per-chunk notes;
  - P6's per-object statistics.

### G2P1-W4 · WARN · The M1 packet is an engineering record, not yet a phone-fit decision packet
- **No cover.** `M1_README.md` carries check-(a) tables, R-numbers and curtain-box detail. Nothing on one screen says what Matt is being asked.
- **v7b is shown like an option.** The hall/gable sheet labels it "(v6 heading)", but **v7b FAILS check (a)**: hall door 0 m², cave 3.7%. Under R-C9-177(a), v7b is comparison only, not an eligible choice.
- **v7c reverses a fix Matt saw, and the packet does not say so.** The fix was R-C9-148's merged longhall, made in answer to Matt's question about the gable.
- **The walkable app is not built** (disk). The `.command` needs the Mac desktop, not the phone. Charter 1.4's "walkable greybox app" is therefore a pending deliverable.
- **R-C9-175 is not carried.** It routed the "open burnt-hall sides" look question to M1/M2, and it does not appear in the packet.

### INFO
- **I-1 · The R-C9-177 revisit of R-C9-148 is within conductor authority (check 6).**
  - **Why:** Matt's verbatim is a question ("is that as intended?"). The merged longhall is labelled "conductor fix" in R-C9-148's own text. A conductor fix may be revised by the conductor, provided Matt sees the reversal as a choice (W-4).
  - **Record defects:**
    - R-C9-148 is filed `by: Matt` but carries conductor content (#9 attribution).
    - R-C9-174 says "Matt accepted the angled-longhall fix", while R-C9-177 says "not a Matt ruling". Both can be true, since acceptance by non-objection is not a ruling, but the record should say which.
- **I-2 · Budget (check 5) is verified.**
  - Three BV2F bursts × 2 `image_calls` = **6**.
  - fal: 3 Tripo builds × $0.40 = **$1.20**.
  - Both are inside R-C9-176's re-based cap (Ph1 6, reserve 14). The re-base is within the conductor's § 6 authority.
  - **Stale text:** the charter still reads "Ph1 4 … reserve 16" (§ 6) and "0–4 images" (Phase 1 header) (#73).
- **I-3 · The frozen tools and v1 integrity (check 3) are verified.**
  - Every v7c guide section and ID log shows `[godot_run]` with the SHA256SUMS shas (`1c15905e0c6f` and `8990273bf49b`), and 0 script errors.
  - `lv_guide_run.sh` calls only `godot_run.sh` with `tierB/` paths. `verify.sh` is OK.
  - Tracked status equals the Phase 0 baseline. The ignored v1 data under `godot/data/painted/` is covered by the 32 control shas, which are exact.
- **I-4 · Check (a)'s bar is "> 0".** A sliver of door would pass it. v7c's weakest opening is the hall door at 29.4% of its frontal area, so the bar is not binding here. Matt judges adequacy from the stills.
- **I-5 · Reflexive.** My Gate-1 W-7 named the **reference** (the layout polygons) but not the statistic, the bar or the calibration. The transplanted 0.513 bar entered through that gap. A new instrument needs its own v1 / negative / constructed calibration in the same landing (#75 cl. 6, #80).

## Rationale
- **G2P1-B1.**
  - #80: a gate is evidence only once it has gone RED and GREEN on its own measure.
  - #82: a figure carries its population, and 0.513 is a different statistic over a different mix.
  - #75 cl. 6: a new instrument does not inherit its predecessor's bar.
  - Principle 4: charter § 12 W-1 says "re-instrumented or discarded; never threshold-tuned", and § 2 principle 3 covers uniform scale.
  - Principle 2: the instrument shipped without a smoke test.
- **W-1.** #73; ADR-006; charter § 13 W-4.
- **W-2.** Principle 3 (charter § 2); #11.
- **W-3.** Charter § 7: a departure found in flight is registered, not assumed.
- **W-4.** Charter §§ 2(6), 11; ADR-002 (the hall/gable choice is Matt's).
- **INFO.** #9, #10, #11, #73.

## Action
- [ ] **PH, then the conductor, G2P1-B1, before Phase 1 closes and before M1 is sent.**
  1. Pre-register P6′ in `calibration.md` and commit it before any v7c re-read. P6′ has four components: presence, placement, scale of record, and extent (validator R1–R13 re-run on the placed models' scene footprints and heights, e.g. from `built.json` `collider_footprints` plus recorded fit; LV to supply if absent).
  2. Calibrate P6′: v1 PASS, plus the four REDs listed in B1.
  3. Run P6′ on v7c and record it as a re-instrumentation.
  4. Keep IoU-vs-prism as a reported row at 0.635 like-for-like.
  5. **The conductor rules adoption on the calibration evidence.** A P6′ RED is a HALT for an LV fix, not a bar move.
- [ ] **LV, G2P1-W2.** Record `fit_scale` per instance for group placements. Report per-axis anisotropy for every placed model; this is input to P6′'s scale component.
- [ ] **PT, G2P1-W1, before Phase 1 closes.** Re-measure T1, T2 and T3 at `f1aa715ac` per § 13 W-4, and record the result in `fid/pc/`.
- [ ] **Conductor, G2P1-W3, before the first Phase-2 take.** Register the ID grouping as a deviation (e.g. DEV-16) with its measurement: on one grouped ID, show the take produces per-instance cutouts equal to v1's per-piece behaviour.
- [ ] **Conductor and LV, G2P1-W4, before sending M1.** Put one cover screen first, with at most three asks, each with one recommendation:
  1. **v7c (recommended)**, with v7b labelled "comparison only: fails check (a)", and stating plainly that v7c separates the gable again, reversing the merged hall Matt saw after his R-C9-148 question.
  2. **Open burnt-hall sides:** wanted or not (R-C9-175).
  3. **The walk:** the `.command` on the Mac now, or the `.app` after Matt runs manifest 14b.

  Show the P6′ result on the cover. The README stays as the record.
- [ ] **Conductor, I-1 and I-2.**
  - Annotate R-C9-148's conductor content.
  - Reconcile R-C9-174 with R-C9-177.
  - Fold the Ph1 re-base into charter § 6.
- [ ] **Matt:** no decision is required by this finding. The v7c/v7b choice reaches him at M1, after B1 folds.

## References
- Charter `agentic_orchestration/gandalf/notes/2026-10-06-barrow-v2-fidelity-run-charter.md` v0.3: §§ 2, 5, 6, 7, 12, 13.
- Prior gates: `qa/findings/2026-10-06-bv2f-charter-gate1.md`, `qa/findings/2026-10-07-bv2f-phase0-gate2.md`.
- Ledger `astra_test_01/burst/runs/C-9/ledger.json`:
  - rulings R-C9-148, 154, 155, 173–179;
  - halts H-C9-BV2F-LV-P1-1, LV-P1-2, PH-P1-1;
  - bursts BV2F-LV-{wreck, barrow, hall}.
- Under `astra_test_01/burst/runs/C-9/barrow_v2/fid/`:
  - `lv/{layout_v7c.json, tools/validate_layout_v7.py, tools/make_layout_v7.py, tools/lv_guide_run.sh, guide_v7c/{check_a.json, s*/built.json, s*/capture.log, s*/ids.log}, fal_spend_BV2F.json, barrow_full_allowlist.txt, M1/*}`
  - `ph/{calibration.md §§ 2, 13–14, harness/p6_phase1.py, harness/p6_geometry.py, results/p6.json, results/p6_phase1_v7c.json}`
  - `v1tools/{verify.sh, godot_run.sh, SHA256SUMS, tierB/barrow_full/godot/tools/capture_ids.gd:98}`
  - `pc/{control_shas.json, bf_status_before.txt}`
  - `RESUME_LV.md`
- Under `astra_test_01/burst/runs/C-9/barrow_full/godot/`: `scripts/bv2f/bv2f_level.gd:263-274`, `scripts/barrow_full.gd:938-1020`.

---

## Re-check — 2026-10-07 — G2P1-B1 fold (R-C9-180, R-C9-181)

**Reviewer:** jack-ryan (DEV-MODE, re-check of own BLOCK)
**Targets:** PH `45fb5eaac` · `48dab5e17` · `44fb98a66` · `bc29572c3`; conductor `bacf8e6c9` (R-C9-181) · `df7e81348`; LV `a6328ddb2` · `9601add8a`; PT `e1a996bc8`.
**Verdict:** **FOLD NOT DISCHARGED, scoped to one sub-reading: the R11 per-region reading inside P6′ extent (G2P1-RB1).** Everything else in B1 and W1–W4 is discharged. **M1 is not fit to send until RB1 folds.** The fold costs 0 images and $0.

### What I found

**1. Pre-registration came first, in commit order and in content. DISCHARGED.**
- The ancestry chain is linear and verified: `45fb5eaac` < `48dab5e17` < `44fb98a66` < `9601add8a` < `bc29572c3` < `df7e81348`.
- § 15 is append-only after `45fb5eaac`. Every later `calibration.md` diff is a pure append at the end of the file.
- The calibration commit touched v7c's **layout** only: it built the constructed shrunk-gable RED and ran the validator on an unshrunk copy as a sanity check. B1 anticipated both. Neither is a P6′ measurement of v7c geometry.
- The bars come from v1 (containment 0.7872) or from written rules (0 missing or extra, hidden ≤ 0.50, anisotropy ≤ 1.10, R1–R13). None was read off v7c.

**2. The calibration REDs are genuine for each component as registered. DISCHARGED for the registered readings.**
- presence: v7c at `2a913e7af`;
- placement: shift of 1.5 m, 85 of 86 below the bar;
- scale: v6 porch at 1.63;
- extent: shrunk gable, R10;
- v1 PASS on all four.
- The harness changed between calibration and the v7c run (`44fb98a66`: beams placed as `_place_beam` places them; "extra" now excludes the non-model prefixes that § 15 scope names). § 17 does not disclose this change (I-R1). The change conforms to § 15, leaves the v1 path untouched, and is stricter, not looser.
- Presence and scale went from RED to PASS through **real geometry changes**: logs seated, every real model placed by one uniform scale, 0 of 148 over 1.10, and PH's cross-check agrees with LV's record with 0 mismatches.

**3. G2P1-RB1. The R11 per-region reading, applied after a RED, is not discharged.** I measured this myself with PH's own `v7c_components()` placed geometry:
- **The hall mesh did not change.** Its last commit is `70ed0b922`. So extent went from RED to PASS **with zero geometry change**: only the reading and a region changed.
- **The PASS depends on a region the builder drew after the RED.** `hall_porch.r11_region_footprint` is new in LV's `9601add8a`. It is 10.6 m wide and **16.5 m deep, the full depth of the hall**. The registered `hall_porch` footprint, which predates § 15, is 1.287 m deep.
- **Read against the registered porch footprint, R11 FAILS.** The mesh inside that footprint reaches **5.10 m** (49 vertices), against a body of 13.117 m. Read against LV's region it PASSES: 13.117 against 12.143. **The choice of region decides the verdict.**
- **What the geometry actually is.** Every vertex above body + 0.5 m (77 of them, z > 12.643) lies **3.3–7.0 m behind the porch's inner face**, at 2.6–6.8 m along its 10.6 m width. It is a raised roof bay set back over the door axis. It is not a porch front at the door.
- **The reading has no RED of its own.** R-C9-181 asked PH to show the reading "still fails" on the v6 porch. PH correctly notes that a height reading cannot change a fit scale, so that RED stands on **scale**. The shrunk-gable RED stands on **R10**. **No input has been shown to make R11-per-region go RED** (#80).

**4. "Hidden by design" for circle stones #2, #4 and #5 is legitimate. It is not a loophole, and it is not a new look question.**
- The burial predates both measurement and pre-registration. At `d4c59061f` the layout already records circle_stones as "laid flat, sunk flush: top 0.12 m".
- The burial is required by R13 (FLAT = 0.15 m), which comes from Matt's clean-floor ruling R-C9-155.
- It is declared uniformly on all 8 stones, not only on the 3 that needed it.
- **Provenance defect (I-R2):** PH's acceptance test is "the declaration is new in `9601add8a`". That is the wrong test, because a new declaration is weaker evidence than an old one. The citation should be the `d4c59061f` status line plus R-C9-155.
- **Look:** before and after the refit, the ring is flush floor marks under a rule Matt set. It does not need a fourth ask on the cover (cap 3).

**5. M1 packet. Fit in form, but not to send.**
- The cover meets W-4: one screen, three asks, one recommendation each, v7b marked comparison-only, the R-C9-148 reversal stated, P6′ shown.
- **But its P6′ line, "PASS on all four parts (… layout rules)", currently rests on RB1.**
- `M1_README.md`'s top still reads "P6′ result: _(the conductor fills this slot …)_", which is stale against the cover (I-R3, #73).

**6. W1–W4 are discharged.**
- W1: `pc/results_phase1_close.json` shows T1–T3 PASS at both the pin and HEAD.
- W2: `placed_fit_v7c.json` exists.
- W3: DEV-16 is registered at charter § 14, and its measurement is owed before the first take.
- W4: see item 5.

### Rationale
- **RB1:**
  - #80: a reading is evidence only once it has gone RED and GREEN on its own measure.
  - #75 cl. 6: a new reading does not inherit the calibration of the reading it replaced.
  - #11: verified by measurement, not by report.
  - § 15's own rule: "a P6′ RED … is a HALT for an LV fix, never a bar move." A post-RED region authored by the builder is the decisive parameter here, so it falls under that rule.
  - Principle 4: R-C9-181's "show it still fails" condition is unmet for the reading it introduced.
- **I-R1–I-R3:** #9, #73.

### Action
- [ ] **Conductor, RB1(a).** Rule the R11 porch region from the design, in words written without reference to the mesh numbers, and record it in the ledger.
  - The porch-above-roofline clause is the conductor's own extension inside R-C9-154, so this is conductor authority.
  - One example: "the porch-width strip over the great door, from the porch's outer face to the ridge line."
  - Either rule that, or adopt LV's 16.5 m strip with a stated reason.
- [ ] **PH, RB1(b).**
  - Re-run R11 under the ruled region.
  - Construct an R11 RED under that same reading (e.g. the in-region mesh clipped to ≤ body + 0.5 m), which must FAIL.
  - Report the registered-footprint reading (5.10 m, FAIL) as non-binding beside it.
- [ ] **Conductor or LV, RB1(c), before sending M1.** Add one clause to the cover. Fold it into ask 2 (the burnt hall), not a fourth ask: *"the tall entrance is a raised roof bay set back about 4–7 m behind the great door; at the door itself the porch stands 5.1 m."* Matt judges the look from the stills.
- [ ] **PH, I-R1 and I-R2.** Add one line to § 17 disclosing the `44fb98a66` harness change. Re-cite the by-design provenance as `d4c59061f` plus R-C9-155.
- [ ] **LV, I-R3.** Replace the stale P6′ line in the README.
- [ ] **Matt:** no decision is required by this re-check. **On RB1(a–c) folding, M1 is fit to send.** No further jack-ryan pass is needed if (b) shows the ruled reading RED on the constructed input and PASS on v7c; the conductor confirms in the ledger.

### References
- Under `astra_test_01/burst/runs/C-9/barrow_v2/fid/`:
  - `ph/calibration.md` §§ 15–18;
  - `ph/harness/p6prime.py` (`placed_vertices`, `r11_per_region`, `run_v7c`);
  - `ph/results/{p6prime_calibration.json, p6prime_v7c.json, p6prime_reds_r181.json}`;
  - `lv/layout_v7c.json` at `d4c59061f` and at `9601add8a` (`hall_porch`, `circle_stones`);
  - `lv/tools/validate_layout_v7.py:466-473, 487, 592-620`;
  - `lv/M1/{M1_cover.jpg, M1_README.md}`;
  - `pc/results_phase1_close.json`.
- Ledger: R-C9-154, R-C9-155, R-C9-180, R-C9-181.
- Charter v0.4 § 14.
