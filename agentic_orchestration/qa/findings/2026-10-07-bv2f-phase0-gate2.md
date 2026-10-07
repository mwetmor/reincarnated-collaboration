# Finding — 2026-10-07 — BV2F Phase 0 Gate-2 (0.1 positive control, 0.2 frame fix, 0.3 two-tier freeze, 0.4 parity harness)

**Reviewer:** jack-ryan (DEV-MODE, Gate-2, BLOCK authority)
**Severity:** BLOCK-narrow ×2 (P6a and P11 as binding pass instruments only) · 4 WARN · 5 INFO
**Verdict:** **PASS-WITH-FOLDS.**
- **Phase 0 is accepted:** 0.1, 0.2, 0.3 and 0.4 are DONE.
- **The quality/constraint split freezes at this gate**, as the charter's § 12 W-1 says.
- **Phase 1 may start.** It involves no painting and no P6a or P11 verdicts.
- **G2-B1 and G2-B2 are scoped narrowly.** Until each folds, **no chunk or window may be counted PASS on P6a or P11**. In practice they must fold before the first Phase 2 W-A chunk is judged. Nothing else is held.

**Target:** collab `7fe86a1b6` (R-C9-172). Lane commits reviewed:
- PT: `648c83813`, `ff173e4ed`, `bf188cb9f`, `35ebeadf2`, `c339bc56d`
- LV: `3e18d1e07`
- PH: `6c3b2d4d0`, `e662a3821`, `618735aa7`, `2eda65ce7`, `04deb9d21`, `f0d63e33b`

**Developers:** drax (LV, PT), galadriel (PH), gandalf (conductor).
**Principles applied:** REVIEW_PROCESS 1, 2, 4, 5; Disciplines #10, #11, #73, #75 (cl. 6), #79, #80, #82, #83, #87; ADR-006.

**When each fold is due:**
- Before the first W-A chunk is judged: G2-B1, G2-B2, W-3.
- Before the first Tier-B or paint run in Phase 1/2: W-1, W-2.
- Before the next control re-run (the next phase Gate-2): W-4.
- INFO items are at the conductor's discretion.

---

## What I found

### Gate-1 fold ledger (check 1)

| Gate-1 item | Status | Evidence (inspected, not taken on assertion) |
|---|---|---|
| B-1 two-tier freeze | **Discharged, with residue** (W-1, W-2) | `bash verify.sh` exits 0 at review time: 17 files, Tier A byte-identical @ `0f8f73697`. v1 shas are re-read with `git show <pin>:<path>` at verify time, never from the copies. RED ×3 is logged (`pc/run/verify_red_tests.txt`). Patched tools reproduce v1 byte-for-byte: `freeze_proof.txt` (take_from_paint 6 outputs, paint_world_prep 31/31 painted files, capture_ids ids.png/json). I checked by `git diff` that the t10bf_drive.sh as-run versions (`816fd84b8`, `32d068af9`) differ from the pin only in the disk-guard constant, as PROVENANCE claims. |
| W-1 per-row negatives, constraint RED, rule text | **Discharged, except P11** (G2-B2) | calibration.md § 1. Every row has a named negative. P7–P10 each show a constructed RED. "Re-instrumented or discarded; never threshold-tuned" is the stated rule. P11 has no v1 cell. |
| W-2 recorded targets | **Discharged; my W-2 was partly wrong** (I-3) | `targets.json` was committed at `648c83813` **before** the first measurement at `ff173e4ed`. Each target is written as {record, field, tool+args, config}. |
| W-3 DEV-10..15 | **Registered; measurements owed in Phase 2** | Charter § 12 table. The DEV-15 dry run fires (`pc/run/dev15_dryrun.txt`: exit 7 on a limit, exit 0 when clean). |
| W-4 pilot | **Discharged** (option iv) | Charter § 12. |
| W-5 write scope / control | **Discharged** (I-5) | I recomputed all 32 control files now; they match `before`. `git status --porcelain -- barrow_full/` is identical to `pc/bf_status_before.txt`. |
| W-6 push | **Discharged** | R-C9-164; CLAUDE.md:144 (`f106af6bd`). |
| W-7 instruments | **Discharged for Phase 0** | P2: lineage chain (159 = 0.18). P3: per class, labelled. P4 new classes mapped (R-C9-167(3)). P6-vs-layout polygons is a Phase 1 item. |
| I-1 P11 power / leak-proofing | **Partly** (G2-B2) | n = 40. The power table is printed in `calibration.json`. Metadata is stripped. Null pairs were replaced by repeat-consistency. No v1-vs-v1 run exists. |
| I-2 mechanical 0.2 | **Re-instrumented, accepted** (I-2) | R-C9-165. |
| I-3, I-4 | **Folded in text**; one record gap (I-4 below) | Charter §§ 4, 6. |

### G2-B1 · BLOCK-narrow · P6a fallback (a) puts in a reader who failed the same calibration item as the judge it replaces
- **The judge was rejected for missing one item.** R-C9-172 rejects the blind judge because it missed **item_17**: it read the brazier_sw disc as a declared door.
- **The conductor's eye failed on the same item.** R-C9-170 records the conductor reviewing the same items by eye and reading item_17 as **"a DECLARED opening"** from the same disc. R-C9-172 then issues a corrigendum.
- **So the fallback did not pass the acceptance the judge was held to.** The replacement mechanism (a) has a recorded miss on the one positive that decided the rejection.
- **It cannot be re-calibrated on this set.** The conductor has now seen the key.
- **Nothing defines a record yet.** "Crops + verdict logged per chunk in `fid/ph/results`" has no schema, no decision rule and no independent check. The harness only carries a string (`p6_judge.py:127`).
- **Why this matters.** In-structure candidates are where R-C9-155's invented door actually lived. Under (a), the gate on Matt's named defect reduces to an un-audited eye that is known to fail there.

### G2-B2 · BLOCK-narrow · P11 v2 has never been shown GREEN, and the generator that will run in production has never been judged
- **No positive control.** `calibration.json` P11 has no `v1` cell. No v1-vs-v1 ABX run exists. Without one, nothing shows that a build v1 cannot be told apart from is actually scored ≤ 26/40. This matters because, by location, still source or capture epoch, the v1 pool is itself heterogeneous: v1ref `V1_*` are record-time stills, while PT's `v1_stills/` were captured at HEAD with the lit path drifted (T2 lit 36.2 vs 40.7).
- **One gate in two directions.** #80 holds both ways: a row that has never gone GREEN on its positive is no more a gate than one that has never gone RED. If P11 cannot pass v1, it will fail every candidate. The run will then face a mid-flight re-instrumentation under spend pressure, which is the threshold-tuning-in-disguise path.
- **The calibrated instrument is not the production instrument.** The three REDs (40/40, 37/40, 36/40) were earned on the **pre-fix** generator. R-C9-171/172 changed three things: different-X repeats, X_OVERLAP 0.25, and content control. No judge has run on the fixed generator. #75 cl. 6 says a remedy does not inherit its predecessor's instrument.
- **The 158 RED is itself compromised.** Its judge reported content cues: foliage and water on opposite sides. R-C9-172 says "calibration stands" based on what the 159 and half-density judges **said** they used. That is self-report, not measurement.
- **The < 40 rule (R-C9-172) is sound, and I endorse it.** A set below 40 trials cannot pass.

### W-1 · WARN · The Tier-B allowlist restricts what a patch removes, not what it adds; the allowlist and verifier are not themselves bound
- `verify.sh` step 5's awk inspects only `^-` lines. A patch that **adds** a line overriding a frozen behaviour passes, provided it removes no unlisted v1 line. An example is a second `PAINT_SHA_PREFIX = ""` after the allowlisted one.
- `ALLOWLIST.md` says every added line must "carry `BV2F` or sit in the appended loader / marked block". **Nothing checks this.**
- I read this from the code. I tried to demonstrate it on a scratch copy, but the attempt was permission-denied, and I did not work around the denial.
- The current patches' added lines are what PROVENANCE describes: frame-grid loaders and driver rewiring.
- `ALLOWLIST.md`, `verify.sh` and `patches/` are not in `SHA256SUMS`. Patches are bound indirectly, through `patch(v1) == shipped`. The allowlist and the verifier are bound only by git history.

### W-2 · WARN · Three executed inputs fall outside the freeze's binding
- **(a) The cfg.** The Tier-B `t10bf_drive.sh` now takes the cfg as `argv[1]`. The executed `rules`, `geo` and `refs` (`guided_paint.py:42-55`) therefore come from whatever cfg is passed, not from the frozen `tierA/cfg_t10bf.json`.
  - B-1 named this as the most replication-critical input. Freezing the v1 file does not bind the run.
  - DEV-11 and DEV-12 owe a measurement ("diff of rules = substitution table only") but have no mechanical check.
- **(b) `lane/run_burst.py`.** Tier-A `wave.sh:9` calls `lane/run_burst.py`, the image-generation transport. It is not frozen, sha-recorded or declared out of scope.
- **(c) The other execution paths.** verify § 6's path check scans only the driver. Godot `--script` invocations of Tier-B `.gd` copies, and any Tier-A python not run through `v1run.py`, have no sha check at execution. `v1run.py` does check.

### W-3 · WARN · P8 compares a whole-window value with a single-chunk extreme, and the bar has only moved down
- **The mismatch.** P8 measures **whole-window** precision (`p7_p8_floor_heather.py:195`) against **v1's minimum chunk**, 0.4476 (`:269`). Those are different populations (#82).
  - v1's whole-window value is seeded and has zero spread (0.5221).
  - The bar sits 0.075 below it, a 14% relative drop that v1's whole window has never shown.
- **The bar's history.** The bar went 0.9 × share (provisional), then 0.4567, then 0.4476. Each step loosened it.
- **This is not tuning to a candidate.** No v2 data exists, so these moves are not threshold-tuning in disguise.
- **The bar is untested where it matters.** The only constructed RED is coarse: a 4 m shift reads 0.1061. Sensitivity near the bar has never been shown (#80).

### W-4 · WARN · The positive control is now "v1 at HEAD" for lit and T4; the re-run comparator is not pinned
- R-C9-166 and R-C9-169 re-base lit (36.2) and T4 (11.08/11.22 ms, windowed) at HEAD.
- The § 6 control-drift HALT ("step 0.1 re-run at every phase Gate-2") does not say which values it compares against. They could be the record or the Phase 0 measurements. It also does not say at which `barrow_full` commit; `targets.json` names `f1aa715ac`.
- `barrow_full` keeps receiving commits from other workstreams. An unpinned comparator either HALTs falsely or absorbs real drift.

### INFO
- **I-1 · Re-basings and discards (check 2): none is threshold-tuning in disguise.**
  - **Lit 36.2 and T4 feed no binding threshold.** `36.2` appears nowhere in `ph/harness/`. P3 binds on unlit 15.5, which reproduced exactly. P10 binds on 16.7 ms p99. Lit was never in charter row 0.1. PT registered it as gating in addition, and demoting it restores the charter's scope.
  - **Under the charter's own band, T4 passes.** 11.08/11.22 lies inside 10.9–12.4. It missed only the tighter record-spread tolerance that my W-2 asked for.
  - **T4's pre-registration named the wrong configuration.** It named fullscreen 1920×1080; the app opened windowed at 1726×971. The miss is disclosed (`results.json` T4).
  - **The P6a re-instrumentation kept T fixed at 32.** It rejected the conductor's priors because any separating prior "would be fitted to this one negative" (calibration.md § 7). That is exemplary #80/#82 conduct.
  - **The P4(3) and P9b discards are legitimate.** P4(3) was blind to its constructed patchwork. P9b could not separate 159 from 158.
  - **Consequence of the P4(3) discard.** Matt's named defect C4 (cellular bakes) now has no binding pixel instrument. It is guarded by cause (P2 lineage), by P4 Lab/spectrum, and by eye.
- **I-2 · The LV frame re-instrumentation (R-C9-165) is sound (check 7). My Gate-1 I-2 proxy conflated two questions.**
  - T3 shows that the v1 camera on R_y(+47)·sim equals the layout's yaw-0 law to 1.8e-12 px over 6 anchors and 243 grid points.
  - Both negatives are rejected: yaw −47 is off by 12,480 px; yaw 0 by 6,335 px.
  - The yaw sweep is the decisive evidence: **no** frame yaw passes ±15° on all six anchors. The best result is 34.3° at a yaw of 26.5°. So the bearing table measures layout-vs-sketch, not the frame.
  - p03 is sealed-pack data, and R-C9-145 places it at SSE.
  - The hall being ~90° off is correctly routed to M1.
- **I-3 · I accept the W-2 corrigendum (R-C9-166). My Gate-1 W-2 was wrong on two counts.**
  - **"52%" is recorded.** It is `overlay_check.json:1781` whole-window `precision_drawn_on_painted` 0.5221; I inspected it. I had cited chunk values.
  - **10.93/10.97/12.40 ms is recorded** at `painted_captures.json:234-236`.
  - The lane reproduced 0.5221 and all 16 chunk values exactly. The error was mine, and the conductor was right to reverse "withdrawn".
- **I-4 · Records.**
  - **(a)** BV2F HALTs H-C9-BV2F-PT-1, PT-2 and the PH P6a HALT appear only in ruling text. The ledger `halts[]` has 4 entries, none from BV2F. Charter § 4 says the conductor writes halts to the ledger (#73).
  - **(b)** Stale text in `calibration.md`:
    - the header still says "Open: P6a's scoped judge … and P11 await";
    - § 2's P11 row says "≤ 19/30" with the old power line;
    - § 2's P10 row says "the 10.9–12.4 ms target is withdrawn", which R-C9-166 reversed.
  - **(c)** "UNDERPOWERED cannot pass" does not say whether an underpowered set counts as a FAIL (which triggers a repaint and spends images) or as VOID (supply stills and re-run). It should be VOID.
- **I-5 · Positive-control integrity (check 4) is verified independently.**
  - All 32 `control_shas` files (painting `eecb4266…` plus `godot/data/painted/`) recompute equal to `before` at review time.
  - `git status --porcelain -- barrow_full/` equals `bf_status_before.txt`.
  - The only commit touching `barrow_full/` in this window is `b5b61994f` (R-C9-159). It predates Phase 0.
  - PT ran everything from an APFS clone.

## Rationale
- **G2-B1.** #80: a gate is evidence only once it has gone red on its target. The fallback's reader has a recorded miss on the target. #75: the instrument must bind what ships. Principle 4: R-C9-155 is the defect this row exists for.
- **G2-B2.** #80, in both directions. #75 cl. 6: the remedy shipped a new instrument without re-calibrating it. Principle 2: no smoke test of the production generator.
- **W-1, W-2.** #75 (the check must bind the executed artifact); #83; B-1's own text ("verify checks the files actually executed").
- **W-3.** #82 (a figure carries its population); #80.
- **W-4.** #73 (the record follows the state); ADR-006 (the control is read-only and must be comparable).
- **I-1 through I-5.** #10, #11, #79.

## Action
- [ ] **PH and conductor, G2-B1, before any W-A chunk is passed on P6a.** Replace "triage by eye" with a written protocol whose record can be audited.
  1. **Change the reference.** Each in-structure candidate is shown with the **layout-projected declared-opening overlay**, computed from layout geometry as in calibration.md § 9, with the distance in metres to the nearest declared opening. The guide crop is not the reference; it is what misled both readers.
  2. **Set the decision rule.** Any framed opening, doorway or aperture farther than the match radius from a declared opening is INVENTED. Ambiguous cases FAIL the chunk.
  3. **Record every candidate.** Each row holds: chunk, candidate px, crop sha, overlay sha, nearest declared id and distance, verdict {MATERIAL, INVENTED, DECLARED}, one line of evidence, and the reader.
  4. **Give Matt the passes.** Every MATERIAL verdict in a window goes on one sheet in the M2 packet.
  5. **Recommended.** Re-run a *fresh* blind judge on the § 9 truth set with the overlay in place of the zone map. If it meets acceptance, it becomes the primary reader and the conductor becomes the second.
- [ ] **PH and conductor, G2-B2, before P11 counts in W-A or W-B.** Run fresh blind judges on the **fixed** generator:
  1. **v1 vs v1 must PASS (≤ 26/40).** Use two disjoint v1 pools. Recommended: v1ref record-time stills vs PT's HEAD stills. That also tests whether HEAD's lit drift is visible. If it is, the P11 reference pool must be single-source.
  2. **v1 vs half-density must FAIL** on the content-controlled generator (40 trials exist).
  3. **Record both in `calibration.json` P11**, including the `v1` cell.

  A v1-vs-v1 FAIL is a HALT to the conductor, never a threshold move.
- [ ] **PT, W-1, before Tier-B is used in Phase 1/2.** In `verify.sh`, fail any `^+` line that neither carries `BV2F` nor sits inside the marked block. Add a RED test for an added override. Record the shas of `verify.sh`, `ALLOWLIST.md` and `patches/*` in `PROVENANCE.md` and in the Phase 0 ledger milestone.
- [ ] **PT and conductor, W-2, before the first BV2F paint burst.**
  - **Bind the cfg.** Add a check that the executed cfg's `rules` equals v1's `rules` with the DEV-12 substitution table applied, and that its `refs` equal v1's plus the DEV-11 entries. The driver calls this check before staging.
  - **Handle `run_burst.py`.** Record its sha at the pin in PROVENANCE, or declare it out of scope with a reason.
  - **Close the remaining paths.** Route Godot `.gd` copies through a sha-checking runner, or make lane scripts assert the `--script` path is under `fid/v1tools/`.
- [ ] **PH, W-3, before the first W-A chunk is judged.**
  - **Re-instrument P8 to like-for-like populations.** Either test per chunk against v1's per-chunk distribution, or test whole-window against whole-window with a tolerance justified from v1. Record it as a re-instrumentation; no candidate data exists, so this is permitted.
  - **Add a graded constructed RED near the bar**, for example a 1 m shift.
- [ ] **Conductor, W-4.** In `targets.json` and charter § 6, state the control-drift comparator: the Phase 0 measured values at `f1aa715ac`, with tolerances. Say how a later `barrow_full` HEAD is handled: re-measure at the pin, or re-base by ruling.
- [ ] **Conductor, I-4.**
  - append the three BV2F HALTs to `halts[]`;
  - PH clears the stale `calibration.md` lines;
  - define UNDERPOWERED as VOID.
- [ ] **Matt:** no decision is required by this finding. The bake close-ups (I-1, C4) and the P6a MATERIAL sheet (G2-B1) reach him at M2 through the conductor.

## References
- Charter: `agentic_orchestration/gandalf/notes/2026-10-06-barrow-v2-fidelity-run-charter.md` v0.2, §§ 5, 6, 12.
- Gate-1: `agentic_orchestration/qa/findings/2026-10-06-bv2f-charter-gate1.md`.
- Ledger: `astra_test_01/burst/runs/C-9/ledger.json` R-C9-161..172, `halts[]`.
- Under `astra_test_01/burst/runs/C-9/barrow_v2/fid/`:
  - `pc/{targets.json, results.json, control_shas.json, bf_status_before.txt, run/*}`
  - `v1tools/{SHA256SUMS, verify.sh, ALLOWLIST.md, PROVENANCE.md, v1run.py, frame_grid.v1.json, patches/*, tierA/conductor_scripts/{guided_paint.py, wave.sh}}`
  - `lv/{frame.py, test_frame.py, frame_report.md, frame_proof/test_frame_output.txt}`
  - `ph/{calibration.md, calibration.json, harness/p7_p8_floor_heather.py, harness/p6_judge.py, results/}`
  - `RESUME_PT.md`, `RESUME_PH.md`
- `barrow_full/take/build/{overlay_check.json:1781, painted_captures.json:234-236}`.
- `CLAUDE.md`:144.
