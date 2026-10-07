# Finding — 2026-10-07 — BV2F re-scope Gate-1 (charter v1.0 § 15 + RESUME_LV PHASE 1′)

**Reviewer:** jack-ryan (DESIGN-MODE, Gate-1)
**Severity:** WARN (overall) — **Verdict: GO-WITH-FOLDS.** Phase 1′ continues now (0 images). No BLOCK.
**Target:** collab `5bfb4ded9` (charter v1.0 § 15, R-C9-185), `7d73e4eb1` (RESUME_LV PHASE 1′)
**Developer:** gandalf (RUN-CONDUCTOR); lane LV drax
**Principles applied:** Review 1 (math before code), 2 (smoke gate), 3 (cross-seam impact), 4 (decisions log as truth); ADR-002; § 2 principles of the charter

**Ruled and not reopened:** Matt's "None at all" (R-C9-185(1)). Nothing below adds a gameplay constraint. Every fold is bookkeeping, an instrument, or a decidability fix.

## What I found

Most of the operationalisation is correct. Retiring anchors, discs, the v7 validator, lanes, R13/P7, P6′ extent, DEV-4 and the divergences matches R-C9-185 exactly. The frozen toolchain, the positive control at pin `f1aa715ac`, the quality rows and the M-gates carry over, which matches "KEPT" in R-C9-185. Check (a) as INFO is the right demotion. The Tier-B freeze survives intact (Q3 below). The defects are in what § 15 **does not say**. Text sized for the old 9×11 / two-window plan still governs wherever § 15 is silent, and the two-window pilot carried three measurement obligations that now have no venue.

## Q1 — Retired vs kept

- **W-1 · Rows dropped by omission.** § 15 "Kept" lists P1–P5, P11 and P6′. It does not list **P6a/P6b**, the paint-time invention check that guards against invented doors (§ 13 G2-B1). It also does not list the constraint rows **P8 (heather), P9 (life) or P10 (performance)**, yet Phase 3′ builds heather, snow and water. None of these rows served the arena. Only P7 did. **Fold:** list P6a/P6b, P8, P9 and P10 as kept. P6a is now *more* load-bearing, because Matt's later arena puts spawns in the real doorways (R-C9-185(4)). Invented doors would then become spawn sites.
- **W-2 · Principles 5 and 8 dropped.** Principle 5, "compose for the play window", is about camera composition, not the arena. Phase 1′ is judged at the play camera, so dropping it contradicts the brief. Principle 8, "Phase 4 after M3", is the guard that keeps arena work out of the build, which is Matt's own sequencing. **Fold:** restore 5. Restate 8 as "no arena or spawn work before M3′".
- **I-1 · Arena-derived rulings with unstated status.** R-C9-154 (door sizes per monster), the R11 porch-above-roofline rule (R-C9-182), R-C9-155 "one great door" and R-C9-175 (open hall sides) are not named in § 15. The first two are arena-derived and therefore retired. The kit already carries their sizes, so this is moot unless the kit is rescaled. "One great door" is a look and invention guard. Hall sides is a look question Matt never answered (R-C9-184 STOP). **Fold:** one line in § 15 giving each ruling's status. Carry hall sides as an M1′ ask.
- **I-2 · Dead weight that is harmless but should be marked.** These are now inert: § 0 terminal artifact (M4), § 1 KC2-runtime row, § 3 fit-test hand-off row, § 4 lane AR, § 5 Phase 4 text, and § 8 G-3/G-4. Mark them **DEFERRED with Phase 4 (R-C9-185(4))** so a later reader does not resurrect G-3, which treats "the arena geometry as the barrow_v2 floor polygon".

## Q2 — Decidability between M-gates

- **W-3 · Phase 1′ has no "Done when".** The brief has state boxes but no DoD. "Every hero should read in a v1-zoom screen with neighbours visible" has no named reader. **Fold:** DONE = (a) P6′ presence, placement and scale PASS against `layout_bv2art.json`; (b) a hero-coverage table from the ID render of each M1′ still, showing each of the 7 heroes in at least 1 still with at least 1 neighbour hero's ID visible (mechanical); (c) a measured footprint against ~55–65 m, with the measure defined (world-metre extent of the composed area on the u and v axes); (d) the declared-openings list emitted (see W-5); (e) Gate-2 (§ 4 still requires it at every phase close); then M1′. The art read itself belongs to Matt at M1′. That is what the gate is for.
- **W-4 · The Phase 2′ pilot is under-specified, and three ways it can fail to close.**
  1. **Size and keep.** On a ~v1-footprint site, a "v1-size pilot window" (v1 = 4×4 canvases) *is* the whole site. State the sub-block dims and the origin. State whether the pilot sits at the wavefront origin and is kept (§ 12 W-4 option (i)) or is not kept (option (iv), which re-paints it).
  2. **P11 can be VOID.** P11 needs 40 trials with X_OVERLAP ≤ 0.25 (`p11_abx.py:44`). A small home-ground window may not yield about 12 distinct v1-zoom stills. An UNDERPOWERED set is VOID (§ 13), and then the pilot cannot close. **Fold:** before the pilot is chosen, PH computes from the generator the minimum window that reaches 40 trials.
  3. **Take/build moved after all paint.** Phase 2′ is "paint, pilot first" and take/build/life is Phase 3′. In-engine rows (P2 lineage, P3 residual, P8–P10, and P11 on in-engine stills) would then first measure after the whole site is painted. That is where R-C9-159's cellular bakes were found. **Fold:** the pilot includes take, bake and build for its window, as the original Phase 2 did. Alternatively, § 15 names the rows that bind at M2′ and accepts the late-detection risk on the record.
- **W-5 · The single pilot orphans the obligations W-B carried.** W-B ("the coast") was the venue for: DEV-3/DEV-11, the hero-plate A/B; P4 for the new classes (sea, shingle, shore ice), which binds in Phase 3 *against W-B's distribution* (R-C9-167(3)); and P9c, the floe-drift positive control (DEV-5's first build). The home-ground pilot has no coast. **Fold:** either extend the pilot to a coast strip (wreck, shore ice, sea), or re-home the obligations. DEV-3/11 A/B moves to the barrow-door chunk. P4 new classes and P9c move to a mini-gate on the first Phase-3′ coast canvases, judged before the rest of the coast paints. Either way, a DEV must not be relied on before its measurement (§ 7 header). **Also fold:** Phase 1′ must still emit `declared_openings.json` and the char/ash dark-structure class (the § 13 P6a overlay inputs). The PHASE 1′ brief dropped both.

## Q3 — Tier-B patches and DEV bookkeeping

- **I-3 · The Tier-B freeze binds without re-freezing.** The frame-bearing surface is a *config*. `frame_grid.*.json` (guide_px, walk_grid, topdown, scene, painting path/sha) is read via `--frame-grid` / `$BV2F_FRAME_GRID`. cols and rows live in the BV2F paint cfg, and `cfg_check.py` checks only rules and refs. The non-parameterised constants are PLAY 1920×1080, `capture_ids` px/m 100.6 with its pitch formula, and the snow-field px in `paint_world_prep.py`. They are v1's values, and M0(c) keeps v1's zoom, so they remain correct. **Fold:** LV/PT write `frame_grid.bv2art.json`. `verify.sh` and `cfg_check.py` stay unchanged.
- **W-6 · § 15 leaves DEV bookkeeping silent.**
  - **DEV-1 (9×11) and G-1:** restate for the compact grid, expected 4×4–5×5. If the grid equals 4×4, close DEV-1 as *not opened*.
  - **DEV-4:** the retirement is correct. Record it as *retired, never relied on*; the 0.2 proof is historical. LV must not inherit `bv2f_level.gd`'s sim→R_y(47°) Level-node frame for the bv2art layout, or the site will be rotated twice.
  - **DEV-6:** a 55–65 m site exceeds v1's 47.2 m snow field, so DEV-6 is probably still needed. Re-measure against the bv2art floor. If the resize touches `paint_world_prep.py`'s snow-field px, it is outside the Tier-B allowlist. That means a DEV-9 patch amendment and a re-verify, not an in-flight edit (§ 6: a departure not in § 7 is a HALT).
  - **DEV-7 (11,776×8,704):** obsolete. Restate at the compact painting size, or close it.
  - **DEV-16:** still owed before the first take *if grouping is used*. A compact site may fit 256 IDs ungrouped. If so, close it as not opened.
  - **DEV-2, 3, 5, 9–15:** stand. For DEV-3/11/5, see W-5.
- **I-4 · P6′ against a new geometry of record.** Retargeting P6′ is not re-instrumentation. The bars stay frozen, and the scale component is layout-independent. The v1 PASS already exercises the v1-format reader that bv2art mirrors. **Fold (cheap):** before P6′ counts on bv2art, run one constructed RED (a 1.5 m shift) on `layout_bv2art.json`, to prove the reader parses the new file. PH's RESUME still points at "layout_v7 polygons" and the "v7 declared-opening list". Update it (see W-8).

## Q4 — Budget and HALTs

- **W-7 · No binding sub-caps for Ph2′/Ph3′.** The § 6 sub-caps (Ph2 70, Ph3 160) were sized for 99 chunks. The 250 run cap is a 3.5× guard over the expected 40–70, so it is not a HALT that fires on a wrong process. **Fold:** set Ph2′ to (pilot chunks × 2) and Ph3′ to (remaining chunks + ≤ 15% repairs + one retry each). Keep "first pilot failure = sub-cap HALT". DEV-13 (seam repair) and DEV-14 (master colour transfer) still require Matt pre-authorization at M2′. Carry that line forward explicitly.
- **I-5 · The Phase 1′ "missing kit piece" HALT is not mechanical, and fit is a real risk.** Hall 32.4 m + barrow front 25.8 m + wreck 13 m inside a ~60 m site is tight. **Fold:** LV's first step is (a) a kit inventory against sketch A's features, each marked {kit-v3 / R-C9-155 build (cavecliff, staircliff, cliffplain, crag) / v1 piece (stones, groves) / procedural (palisade, stream) / MISSING}, and (b) a top-down 2D footprint fit at the current scales. MISSING items and any non-fit go to the conductor as a HALT. A uniform kit rescale needs no ruling, because no door-size rule binds now. Record the scale per instance, as W2 did.
- **INFO:** Disk gate, heavy lock, usage-limit exit 7, the control-drift HALT, the `barrow_full` write allowlist, fal ($1.20 of $10) and Ph1′ drawing ≤ 2 from reserve 14 all carry correctly. The M1′ walk bound is an art-walk convenience (v1 `bounds` practice), not a gameplay constraint.

## Q5 — Dangling cross-run dependencies (annotate now; they cost one line each)

- **W-8 · Records that still state retired or superseded constraints:**
  - **C-9 ledger R-C9-156(3)** ("then the KC2 sim runs inside the 3D barrow"): add a forward annotation, "sequencing step (3) amended by R-C9-185(4): decided after M3′". The conductor writes it.
  - **KC2 charter KP-252/253/281/283/285:** "barrow_v2 constraint given to C-9" (six anchors, 8 m discs, open lines). KP-281 offers "the barrow_v2 v4 polygon as the [kc2_play] bound". KP-285(3) promises a later joint scoping. KC2 records these as live. Annotate: not binding on the scene; the v4/v5 polygon is no longer barrow_v2's geometry. If kc2_play's walk bound actually uses that polygon, it is now a dependency on a retired layout (the files persist, so nothing breaks). **V2-TERRAIN (KP-255)** will arise unavoidably when Matt fits an arena to a scene that has cliffs, stairs and doorways. Note it there. Route to the KC2/Sim Session conductor; C-9 does not write KC2 records.
  - **JOIN-1 charter line 8:** Matt's playtest order ends "→ barrow-fit arena". Annotate it as unscheduled, after M3′ (R-C9-185(4)).
  - **Lane RESUMEs:** RESUME_PH (next steps cite layout_v7 and P6b against v7 polygons) and RESUME_PT carry no § 15 header. Lane law (§ 4) requires each RESUME to be current. **Fold:** add a § 15 header to both: P6′ against bv2art with extent retired, P7 retired, frame_grid.bv2art, and the DEV status from W-6.

## Rationale

Review Principle 4 (the ledger and decisions are the truth: every superseded record gets a forward annotation, per the CLAUDE.md corollary that "silence is not" a disposition). Principle 2 and charter § 7 (a DEV is measured before it is relied on: W-5, W-6). Principle 3 (KC2/JOIN-1 annotations: W-8). Charter § 3 fit test, "decidable target-state" (W-3, W-4). § 6 "first failing gate stops the phase" (W-4(2): a VOID P11 is a gate that can never fail or pass).

## Action

- [ ] gandalf (conductor), **before Phase 1′ closes:** W-1, W-2 and I-1 as a § 15 amendment. The W-3 DoD in RESUME_LV. W-5's declared-openings and char-class emission added to the LV brief. I-5 inventory and fit step first in LV. W-6 DEV table restated. W-8 annotations: the R-C9-156 ledger line and the RESUME headers now; the KC2 and JOIN-1 lines routed to the Sim Session conductor and KR.
- [ ] gandalf, **before Phase 2′ opens (no image spend until then):** W-4 (pilot dims and keep, PH's 40-trial minimum window, take/build in the pilot or rows named), W-5 (re-home DEV-3/11, P4 new classes, P9c), W-7 (sub-caps).
- [ ] drax (LV): I-5 inventory and fit; `frame_grid.bv2art.json`; no inherited R_y Level frame; emit declared openings + char/ash; placed-fit record.
- [ ] galadriel (PH): I-4 constructed RED on bv2art; W-4(2) minimum window computation.
- [ ] Matt: no decision needed. Hall sides (I-1) rides the M1′ cover as an ask.

## References

- `agentic_orchestration/gandalf/notes/2026-10-06-barrow-v2-fidelity-run-charter.md` §§ 0–15
- `astra_test_01/burst/runs/C-9/barrow_v2/fid/RESUME_LV.md` (PHASE 1′), `RESUME_PH.md`, `RESUME_PT.md`
- `astra_test_01/burst/runs/C-9/ledger.json` R-C9-156, -162, -167, -180, -182..185
- `astra_test_01/burst/runs/C-9/barrow_v2/fid/v1tools/{frame_grid.v1.json, ALLOWLIST.md, cfg_check.py}`
- `astra_test_01/burst/runs/C-9/barrow_v2/fid/ph/harness/p11_abx.py:44`
- `agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-run-charter.md` KP-252/253/255/281/283/285; `2026-09-29-join-1-run-charter.md:8`
- Prior gates: `qa/findings/2026-10-06-bv2f-charter-gate1.md`, `2026-10-07-bv2f-phase0-gate2.md`, `2026-10-07-bv2f-phase1-gate2.md`
