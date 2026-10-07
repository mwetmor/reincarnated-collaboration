# Finding — 2026-10-06 — BV2F charter v0.1 Gate-1 (barrow_v2 at v1 fidelity)

**Reviewer:** jack-ryan (DESIGN-MODE, Gate-1)
**Severity:** BLOCK-narrow (step 0.3 only) · 7 WARN · 5 INFO
**Verdict:** **GO-WITH-FOLDS.** LV (0.2), PH (0.4) and PT (0.1) continue. **Step 0.3 holds until B-1 folds.** I am scoping my own BLOCK to step 0.3, as at the JOIN-1 Gate-1 (BLOCK-narrow); the charter's header sentence ("a Gate-1 BLOCK halts every lane") should be amended to match.
**Target:** `agentic_orchestration/gandalf/notes/2026-10-06-barrow-v2-fidelity-run-charter.md` @ `8f54cb1a1`. The plan is `…-run-architecture.md` @ `6e6e550ea`.
**Developer:** gandalf (RUN-CONDUCTOR)
**Principles applied:** REVIEW_PROCESS 1, 4, 5; Disciplines #1, #10, #11, #75, #79, #80, #82, #83, #87; ADR-006; CLAUDE.md push section.

**When each fold is due:**
- Text-only, now: W-6.
- Before step 0.3 executes: B-1.
- Before the Phase 0 Gate-2: W-1, W-2, W-5, W-7.
- Before Phase 2 starts: W-3, W-4.
- INFO items are at the conductor's discretion.

---

## What I found

### B-1 · BLOCK-narrow · Step 0.3's DONE row cannot be met as written
Step 0.3 says: "byte-identical to their v1 sources … only frame and grid are parameters, in a separate config." Inspection shows that the frame and grid are written into the tools themselves:
- `capture_blockout.gd:26,34-35,71,111` and `capture_ids.gd:23,47` hard-code `const GUIDE := Vector2i(5376, 3328)`, `GRID_U/V`, the window centred at (−2, −3), and `load("res://scenes/barrow_full.tscn")`. They cannot render barrow_v2 without being edited.
- `paint_world_prep.py:34,43-46` hard-codes `PAINTING`, `PPM` and the frame.
- `heather_instances.py`, `t5_06b_bake.py` and `hero_surface.py` resolve every path relative to the script's own location (`HERE`/`ROOT`). A copy placed in `fid/v1tools/` silently reads and writes `fid/`.
- `t10bf_drive.sh` hard-codes `CFG=…/cfg_t10bf.json` and the `T10BF-` prefix. It also calls `$C/guided_paint.py`, `wave.sh` and `refs_guard.py` at **`conductor_scripts/`, not at the frozen copies**.

This leaves the lane two ways out, and both are bad:
- **Edit the copies.** The sha check then fails and the lane HALTs every run.
- **Regenerate `SHA256SUMS` from the edited copies.** `verify` then returns cleanly while proving nothing. Worse, `verify` can pass on the `fid/` copies while the driver runs the originals. That is #75 at its root: the instrument does not bind the artifact that ships.

The freeze also leaves out the most replication-critical input: **`cfg_t10bf.json` (`rules`, `refs`)**. It also omits `make_layout.py`, `wave.sh`, `refs_guard.py` and `nb_t8/scripts/t5_06a_surface.py`, which `hero_surface.py` and `take_from_paint.py` name as their surface step.

### W-1 · WARN · Calibration logic: C-1 is sound in principle, but as written it is a loophole, and it discards the wrong rows
- **The quality side.** C-2 makes R-C9-159 the negative control for P1–P6, and 0.4 discards any quality row that cannot tell v1 from 159. But 159's ground seams were **2–6/255** (handoff § 3, "what works"), inside v1's 2.7–13.1. So P5 cannot fail 159. P6's invention check also has nothing to catch in 159: its structures were placed models. **Both would be discarded.** P5 and P6 guard the two defects Matt actually named: seams (R-C9-159(2), on the R-C9-158 build) and invented doors (R-C9-155).
- **The constraint side.** C-1 rightly keeps P7–P10, but it requires **no RED case at all** for them. A row that has never been shown to fail is not a gate (#80). That is the loophole.
- **The discard rule.** "Discarded, not tuned" makes no distinction between **re-instrumenting** (changing *what* is measured) and **tuning** (moving a threshold). A row that is mis-built, such as P2 in W-7, gets thrown away rather than fixed.

### W-2 · WARN · Step 0.1's targets are not traced to recorded instruments, and P8 could fail v1 on v1's own record
- **"heather 52% on tufts".** This figure exists only in ledger prose. The persisted records show something else:
  - `take/build/overlay_check.json`: `precision_drawn_on_painted` 0.4653 and 0.4476;
  - `take/build/painted_prep.json`: `tuft_cells_covered_share` 0.4379.

  **P8's "≥ 50%" can therefore fail the positive control.**
- **"Frame time 10.9–12.4 ms".** There is no level record for this band:
  - the 10.9 ms values are VFX budget runs (`meteor_mix4_crater_v4.json`, `fire_ball_budget.json`);
  - "12.4 ms" is a Godot frame-split figure quoted inside an outlier note;
  - v1's own frame costs (`barrow_full_layout.json` `frame_cost_ms`) run from 8.55 to 21.31 ms depending on configuration.
- **Consequence.** As written, step 0.1 will either HALT falsely, or invite the lane to search for the instrument that reads 52. That second path is calibrating to a number (#79, #82).

### W-3 · WARN · Departures from v1 that the deviation register does not record
Under § 7, each of these becomes an in-flight HALT:
- **(a) Per-chunk notes "generated from the ID render".** v1's brief has one global `geo` and `rules`, and `guided_paint.py` has no per-chunk text field.
- **(b) DEV-3 plates, per chunk.** `guided_paint.py` takes only global `cfg['refs']`. The *mechanism* that would attach plates to some chunks and not others is not registered (#83).
- **(c) v1's `rules` names v1's site.** It says "Paint the barbarian OUT", "the ring's centre, the path, the cutting and the tarn", "Frost King's Barrow". "Verbatim" is impossible, so this needs a substitution entry.
- **(d) Seam-repair canvases.** v1 has no such stage.
- **(e) G-2, the master colour transfer.** This is a new stage, and the gate names no authority. § 2.4 requires a Matt gate.
- **(f) Driver exit 7 on a usage limit.** It exists only in the v2 drivers (`v2sw_drive.sh:32-33`, `section_sw_drive.sh`). v1's `t10bf_drive.sh` treats a limit as a failed burst, retries, and exits 2.

### W-4 · WARN · Keeping pilot chunks breaks the v1 wavefront at the pilot edges
The grid arithmetic checks: (11,776 − 256) / 1280 = 9 and (8,704 − 256) / 768 = 11, so the grid is exactly 9 × 11.

The problem is the paste rule. `guided_paint.py:28-35` pastes only the **left, top, top-right and top-left** neighbours. Take a kept 4 × 4 pilot block that is not at the wavefront origin. The chunks painted later above it and to its left never receive the pilot's top or left strips. That gives structural seams on 2 × 4 edges per window, **about 16 for W-A plus W-B**. The seam-repair cap is "≤ 15% of chunks", about 15. **The pilot alone would spend the whole repair budget.**

### W-5 · WARN · C-4 is acceptable only if its write-scope claim holds, and it does not
C-4 says Phase 0 "writes only to `barrow_v2/fid/` and the RESUMEs". Two steps break that:
- **Step 0.1** re-renders v1 with tools whose default outputs are v1's own directories. The painting is gitignored (`astra_test_01/.gitignore:1`), and `godot/data/painted` has 2 tracked files. **An overwrite of the positive control would be invisible to git.**
- **Step 0.2** puts the frame function into `barrow_full/godot`. That is the project the live Barrow page builds from.

There is also **no HALT for positive-control regression.** If a v2 edit touches a shared v1 script (`painted_world.gd`, `barrow_heather.gd`, `snow_field.gd`, `barrow_full.gd`), the control moves without anyone noticing.

### W-6 · WARN · § 10's push scope cites the wrong authority and claims too much
The handoff it carries says "(JOIN-1)", but JOIN-1's J-L5 is scoped to **JOIN-1's duration**. C-9's own authority is:
- **R-C9-71**: push-as-work-lands "for this run";
- **R-C9-84**: collaboration plus the loadout playtest routes. It also says **"reincarnated-godot stays with the JOIN-1/KC2 conductor"**, and it supersedes C-9 charter § 6 ("no push without Matt's word").

What that means for each repo:
- **Collaboration:** authorized; no Matt ask is needed.
- **Engine:** BV2F writes no engine paths, so it should be struck.
- **Godot:** not the BV2F conductor's to release. Phase 4 vendors `kc2_runtime` into the collaboration repo's `barrow_full/godot`, so BV2F should need no `reincarnated-godot` push. Any write there goes out through the Sim Session conductor.

Separately, CLAUDE.md's push section does not record C-9's R-C9-71/84 posture. That gap predates this charter, and the fix is knight-rider's.

### W-7 · WARN · Instrument hazards in P2, P3 and P6 (the #75 cl. 6 family)
Each of these can return cleanly without answering its question:
- **P2 (provenance).** Checked by shader or layer, P2 passes 159: its 4-view-sheet bakes also wore `PaintStack.world_material`. Only a **lineage chain** answers the question: each texture's input sha, through the producing tool's manifest, back to painting sha `eecb4266…` (#87).
- **P3 (lighting).** As a site mean, ground area dominates. 159's ground was an unlit projection, so P3 passes 159. The row is also mislabelled: 15.5 is the **unlit** residual (`build_plan.md:215`: "Unlit: 15.5. Lit: 40.7.").
- **P6 in Phase 1.** "P6 green on the guide" is circular when the class map comes from the same render. It needs an independent reference: the layout_v2 polygons.
- **P4 for DEV-2's new classes.** Sea, shingle and shore ice have no v1 crop to compare against, so P4 is undefined for them.

### INFO
- **I-1 · P11's statistical power.** P11 passes at ≤ 13 of 20 pairs (65%). The probability of a pass for a judge with each true accuracy:

  | Judge's true accuracy | P(pass) |
  |---|---|
  | 50% (chance) | 0.94 |
  | 65% | 0.58 |
  | 75% | 0.21 |
  | 85% | 0.02 |

  So P11 catches only gross gaps. Two fixes: print this table on the row's face, or raise n to 40 or more. Two leak-proofing measures as well:
  - add v1-vs-v1 null pairs, to catch judging by content rather than quality;
  - strip PNG metadata and filenames, and keep crop sizes identical.
- **I-2 · Two judgments with no mechanical criterion.** Step 0.2's "judged by the conductor" and P9's "film check" are both decided by eye. Mechanical proxies are available:
  - step 0.2: the cyclic order of the six anchor bearings matches sketch A, each within ±15°;
  - P9: flow above 0 inside the water mask; floe UV drift of 0 px on a marker; snow-trail coverage as a % of the floor.
- **I-3 · Caps.**
  - The sub-cap labels "P1 4, P2 70, P3 160" collide with harness IDs P1–P11; rename them Ph1/Ph2/Ph3.
  - § 6 has no breach row for the seam-repair cap.
  - `images_used` is the shared C-9 counter: 1,251 used against the 1,500 guard leaves 249, under the run's 250. BV2F needs its own counter.
  - One W-A re-paint costs about 28 images. Started after the first ~56 of the 70 Ph2 cap, it overruns that cap, so the first W-A failure is in practice a sub-cap HALT. State that this is intended.
  - Phase 4's "0 frames > 16.7 ms" needs a window and a warm-up exclusion. v1's records include a 52 ms outlier.
- **I-4 · Ledger writes.** Lanes write HALTs into ledger `halts[]` while the conductor commits the ledger. That is a lost-update race on a single JSON file.
- **I-5 · Decidability.** Once W-2 and I-2 are folded, every pre-Matt DONE row is decidable without Matt. M1–M4 are HITL by design, which is consistent with § 3. I found no conflict with the decisions-log; the run's truth is the C-9 ledger.

## Rationale
- **B-1.** #75 (the instrument must bind what ships, and prove its own sensitivity) and #83 (the surface cannot carry the remedy). Principle 1: the freeze was specified without checking the tools.
- **W-1.** #80: a gate's green is not evidence until that gate has gone red. #10: one variable at a time.
- **W-2.** #79: figures derived at writing time. #82: a figure carries its population. #11.
- **W-3 and W-4.** Charter § 2.4 and § 7. Principle 4: R-C9-159 and R-C9-155 name the defects being guarded. #1: the seam-budget arithmetic.
- **W-5.** ADR-006: v1 is a read-only control. #75.
- **W-6.** CLAUDE.md's push section, including its conflict rule and recording mandate; R-C9-71 and R-C9-84; JOIN-1 J-L5.
- **W-7.** #75 cl. 6 and #87.

## Action
- [ ] **Conductor, before step 0.3 executes (B-1):** fold a **two-tier freeze**.
  - **Tier A, byte-identical:** the frame-free tools, **plus `cfg_t10bf.json`'s `rules` and `refs`, `wave.sh`, `refs_guard.py` and `t5_06a_surface.py`.**
  - **Tier B, minimal patches:** the frame-bearing tools (`capture_blockout.gd`, `capture_ids.gd`, `paint_world_prep.py`, `take_from_paint.py`, `t10bf_drive.sh`). Each patch is committed as a diff against the v1 source, and the diff touches only allowlisted constants and paths. Register it as a DEV entry.
  - **`SHA256SUMS` holds both shas:** the v1 source's (read from git at a pinned commit, **never computed from the copies**) and the patched file's.
  - **`verify` checks the files actually executed.** The driver invokes only `fid/v1tools/` paths, and `verify` fails if any v1 original path appears in the command line.
- [ ] **PH, before the Phase 0 Gate-2 (W-1):**
  - Give every row a **named negative control: the attempt that showed that row's defect.** P1–P4 and P11 → R-C9-159. P5 → the R-C9-158 section. P6's invention check → the R-C9-155 BVP re-test-2 blocks. Use a seeded failure where no real one exists.
  - Constraint rows each show RED once (#80).
  - Freeze the quality/constraint split at the Phase 0 Gate-2. Reclassifying a failing row afterwards is a HALT.
  - Change "discarded, not tuned" to "re-instrumented or discarded; never threshold-tuned".
- [ ] **PT, before the Phase 0 Gate-2 (W-2):** write each 0.1 target as {record file, field, tool and args, configuration}. Take tolerances from the record's own spread. **Re-derive P8's threshold from the reproduced v1 value.**
- [ ] **Conductor, before Phase 2 (W-3):** register entries (a)–(f), each with its A/B measurement owed. (d) and (e) need Matt pre-authorization at M1 or M2 (§ 2.4).
- [ ] **Conductor, before Phase 2 (W-4):** choose one of these and record it:
  - (i) put a pilot window at the wavefront origin;
  - (ii) register a DEV for pasting bottom and right neighbours (this needs a Tier-B patch to `guided_paint.py`);
  - (iii) budget the pilot-edge repairs outside the 15% cap.
- [ ] **PT and LV, before the Phase 0 Gate-2 (W-5):**
  - step 0.1 writes only to `fid/pc/`;
  - record the shas of the painting (`eecb4266…`) and of `godot/data/painted/` before and after the run;
  - v1 scripts are read-only, and barrow_v2 levels **extend** them;
  - re-run step 0.1 at every phase Gate-2, and **HALT if the control drifts**;
  - `git status --porcelain -- …/barrow_full/` shows only allowlisted new paths.
- [ ] **Conductor, now (W-6):** rewrite § 10's push line as: "collab: push-as-work-lands under R-C9-71/84; engine: none (no BV2F paths); reincarnated-godot: none by this conductor, the Sim Session conductor releases (R-C9-84); loadout and demo: fresh-ask." Route the missing CLAUDE.md record of R-C9-71/84 to knight-rider.
- [ ] **PH, before the Phase 0 Gate-2 (W-7):**
  - make P2 a lineage chain;
  - make P3 per class, labelled "rendered-vs-painting";
  - in Phase 1, judge P6 against the layout_v2 polygons;
  - give P4's new classes a named nearest v1 class, or run only the class-agnostic cellularity detector on them.
- [ ] **Matt:** no decision is required by this finding. W-3 (d) and (e) reach him at M1 or M2 through the conductor.

## References
- The charter and plan named above; `2026-10-06-c9-phase2-session2-handoff.md` §§ 3 and 6; `2026-09-26-illuminated-archive-run-C-9-charter.md` § 6; `2026-09-29-join-1-run-charter.md` J-L5.
- The ledger `astra_test_01/burst/runs/C-9/ledger.json`: R-C9-64, R-C9-71, R-C9-84, R-C9-155, R-C9-158..160; `images_used` 1251 against `images_cap` 1500.
- `runs/C-9/conductor_scripts/{guided_paint.py, guided_stitch.py, t10bf_drive.sh, cfg_t10bf.json}`.
- `runs/C-9/barrow_full/godot/tools/{capture_blockout.gd, capture_ids.gd}`.
- `runs/C-9/barrow_full/tools/{paint_world_prep.py, heather_instances.py, take_from_paint.py, hero_surface.py, t5_06b_bake.py}`.
- `runs/C-9/barrow_full/take/{build_plan.md, build/overlay_check.json, build/painted_prep.json}`; `barrow_full_layout.json` `frame_cost_ms`.
- `runs/C-9/barrow_v2/tools/v2sw_drive.sh`.
