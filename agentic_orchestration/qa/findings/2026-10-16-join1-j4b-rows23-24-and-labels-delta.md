# Finding — 2026-10-16 — JOIN-1 J4b rows 23/24 + the label fixes (closing delta for the design-finding chain)

**Reviewer:** jack-ryan
**Severity:** INFO (verdict: **PASS-WITH-NOTES**; 0 WARN / 4 INFO). **The J4b design-finding chain is closed for QA.**
**Target:**
- label fixes: collab `486a788b9`;
- rows 23/24 grade: collab `194f4211d`, against the pre-run quantity note at engine `6587ffe8`;
- trace arms: godot `10e89c6` / `34ae399` / `b474a9e` (runner and trace `a7044d7`, fail-first `c4c4f5c`);
- legolas D2 citation: collab `1d0504430`.

**Developers:** gamora, drax, legolas
**Principles applied:** REVIEW_PROCESS 1, 2, 4; Disciplines #8, #10, #12

## My `ec3d78cd5` notes: all closed
- **WARN-1:** rows 11, 12 and 14 now read **NO VERDICT as registered (runs FAIL)**. The 24-cell grade is labelled POST-HOC, the 25-cell grade CELL RERUN UNDER KP-500, and neither is "of record". This is in Batch 3, in the summary table, and in the arm JSON.
- **WARN-2:** **fraction (a) FALSE AS PRE-STATED, 31/32** (29/32 pack reading beside) is now in the results table.
- **Row 14:** labelled "NC statistic non-discriminating by construction (as rows 11–13, KP-501); LOW EVIDENTIAL VALUE".
- **INFO-1 (D2 citation): CONFIRMED.** legolas cites D2MOO 1.10f `5596f5cb`:
  - Confuse at SkillNec.cpp L723;
  - Conversion at SkillPal.cpp L1131, with an explicit `UNIT_MONSTER` test;
  - the shared `AIUTIL_CanUnitSwitchAi`, which is false for any non-monster (AiUtil.cpp L1326);
  - Basin as a secondary source.

  The KP-500 nativity claim is now sourced on both sides.

## Q3 — byte-identity and zero sealed lines: CONFIRMED
- **Pins:** 85/85 in each trace arm (my own check). Each committed pin file equals its bulk copy.
- **Pre-existing files:** **105/105 byte-identical** in every arm, each compared with its filed arm (primary vs car2, dot-gd vs t2 dot-gd, chill-off vs t2 chill-off). The only new files are DRIVE ×5, GDDOT ×5 and `verdict.json`.
- **Zero sealed lines:** `a7044d7` touches **0** files under `kc2_runtime/`. The runtime digest at HEAD recomputes to **`fb49080f…`**. The overrides only read state around `super()`, as in `ec3d78cd5` Q5.

## Row 23: TRUE, re-derived with my own script
- **Quantities, as fixed beforehand in `6587ffe8`:**
  - d2 = rate × `len_eff` per `replace` row, or rate × 1 per `ignore_one_frame` row, from the traced primary's `dots`;
  - gd = GDDOT `d_effective`.
- **Stage:** all **469/469** gd rows are `post_resist`.
- **Result:** **25 pairs. d2 > gd in 1 cell, d2 < gd in 24.** Σ of per-cell means **7,259.5 vs 10,939.7**. Applications 462 / 469.
- **The pre/post-table choice is moot:** `d_base == d_effective` on every gd row, so the ordinal diminishing never fired on this data. The trade-off is that gd's stacking rule was **not exercised**. That is not a defect, but the row demonstrates d2's replace / ignore and poison-length rules against gd's insertion, not gd's diminishing (INFO-1).

## Row 24: TRUE, re-derived with my own script
**Q1 — which way the 9/16 runs.**
- **d2 > off in 9 cells; d2 < off in 16; no ties.** The **majority (16) agrees** with the registered direction d2 ≤ off, and so does the paired total (Σ of means **7.758 vs 7.871** m per moving tick).
- So the case you were worried about (16 disagreeing cells) does not occur.
- But the sign test is **p = 0.23**, and the per-cell differences are small and two-signed (−0.027 … +0.018 m). Chill scales only chilled moving ticks, about 1,466 of roughly 35k, so trajectory noise is the same size as the effect.

**Disposition:**
- **TRUE as registered**, labelled **"DIRECTION WEAK (16/25 agree, p = 0.23); LOW EVIDENTIAL VALUE on the direction limb"**.
- **This is not the row-14 case.** Row 24's statistic is not non-discriminating by construction.
- **ACTIVE stands, and rests mainly on two limbs that are not weak:**
  - **the row identity:** on every moving tick, (dx, dy) = scale × proposed, with scale 1 unchilled and in [0.25, 0.5] chilled. **0 violations in both arms** (my check);
  - **reach:** chill on her in **all 25 cells**.

**Reach naming (INFO-2).** gamora's "112 landings" is the number of **chilled episodes**: rising edges of the chilled state in DRIVE, which I reproduce at 112. The lane's own counter `row24_chill_on_her_landed` is **177**, because overlapping landings merge into one episode. Print both under their names.

**Q2 — the off arm's one chill (M0/1, 22 chilled ticks): carried cleanly.**
- The lever is defined at `_chill_trigger` (`kc2rb_d2lane.gd:1340`) as "chill off = REFERENT-v1, no damage-triggered slow on her". It suppresses the Cold / Elemental rider (`t2_chill_suppressed` 123).
- The remaining chill comes from the **row 22 control path**, Freeze → chill (`:1650`), which the lever does not touch.
- That matches the prereg, where row 24's table entry assigns *"the freeze→chill clause … wherever row 22 is"* to row 22.
- The comparison therefore isolates row 24's own rider. The M0/1 Freeze → chill episode is present in both arms, so it pairs out.

## Fraction (b)
**15 ACTIVE + 0 RI / 23, FALSE AS PRE-STATED against 22 + 1.** The print carries row 14 as low-evidential and rows 23/24 as INSTRUMENT ADDED AFTER RUN.
- **Add to the print:** row 24's **direction limb is weak** (INFO-3).
- **Unchanged:** failed NC 11, 12, 13, 19; partial 9, 32; open 29, 30.

## Notes (INFO)
- **INFO-1:** row 23 never exercised gd's diminishing (`d_base == d_effective` everywhere). Say so in the close-out.
- **INFO-2:** name both row 24 reach quantities: 112 episodes and 177 counter landings.
- **INFO-3:** row 24 label "DIRECTION WEAK (p = 0.23); LOW EVIDENTIAL VALUE on the direction limb; ACTIVE on row identity + reach".
- **INFO-4:** for the close-out, every FALSE AS PRE-STATED / FAILED-NC / POST-HOC / INSTRUMENT-ADDED-AFTER-RUN item in this chain is now carried in gamora's TIER2 README. I checked fraction (a), fraction (b), rows 11–14, 19, 21, 22, 23 and 24.

## Action
- [ ] gamora: INFO-2 and INFO-3 wording; carry INFO-1 into the close-out.
- [ ] Matt: none from QA. The close-out goes to Matt from the conductor.

## References
- trace grains `/Users/admin/Games/join3c-bulk/r2324/{primary,dot-gd,chill-off}/`; filed arms `/Users/admin/Games/join3c-bulk/{car2/primary,t2/dot-gd,t2/chill-off}/`
- `reincarnated-engine/src/reincarnated/simulation/math/join1-j4b-grading-prereg-2026-10-15-ROW23-24-TRACE-QUANTITIES.md` (`6587ffe8`)
- `reincarnated-godot/kc2_play/join/rulebook/kc2rb_d2lane.gd:1332–1348, 1650`
- `agentic_orchestration/gamora/analyses/2026-10-15-join1-j4b-TIER2/README.md`; legolas citation at collab `1d0504430`
