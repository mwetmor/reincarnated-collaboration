# Finding — 2026-10-15 — JOIN-1 J4b ADDENDUM-13 CORRIGENDUM-2 + grader effect gates (delta)

**Reviewer:** jack-ryan
**Severity:** WARN (verdict: GO-WITH-AMENDMENTS; 1 WARN / 2 INFO)
**Target:** engine `c99ac644` (CORR-2, doc-only); grader fail-first `f4b34689` → `37e864f4`
**Developer:** gamora
**Principles applied:** REVIEW_PROCESS 1, 2, 4; Disciplines #1, #8, #10; ADR-004; KP-312 protocol
**Rulings read:** KP-452 (RESET), KP-453 (flinch a world capability), KP-454 (conductor), **KP-455 (Matt, guarded hit records)**

## What I found
- **Consistent with my delta `307488345` and unaffected by KP-455:** § 2 effect gates (a)/(b)/(c) with HALT on a violation and the GH/GM/GR/GB grain contract; § 3 2H sensitivity `[[32,16,8],[64,32,16]]` with class 8 as a labelled lower bracket and flinch duty per wave; § 4 halts (ii) and (iii); § 5 v5 names (the `RB-W-l21_*` rows in WORLD). The grader implements (a)/(b)/(c), NO VERDICT on a missing GH/GM/GR, and duty = locked ÷ on-board body-ticks. I re-ran `tests/test_join4b_grade.py`: **24/24**.
- **Superseded:** § 1, second bullet, says the S07 pass "reads the fight's existing event list". KP-455 (drax STOP-AND-TELL) established that the port has no booked-event list. The operand is now the **guarded hit records**. The § 5 HOOK row still reads "site S07 (ledger pass)".

## Rationale / items
- **WARN-1 (KP-455 fold; Discipline #8, ADR-004).** CORR-2 § 1 and ADDENDUM-13 CORR-1 § 1/§ 2 describe a read that cannot be built. A CORR-3 (or a § 1 erratum) must restate the following:
  - **(i) The operand.** It is the per-body record of every qualifying hit, in emission order, with killing blows included.
  - **(ii) "Pre-cap d".** Define it as post-k, post-Cruel and before the HP clamp. That is CORR-1's booked `damage_raw` with no overkill truncation, and the definition must say whether that equals GO `offered` on a killing blow.
  - **(iii) The sources.** List disc 1-packet, L-02 packets, L-07, Soulfire post-Cruel and summons; bleed has no record.
  - **(iv) Mirror-side state.** Record state and the cursor stay mirror-side, or the new member is named (M-3/M-5).
  - **(v) The HOOK row.** It should read "S07 RESET + guarded hit-record lines (KP-452 + KP-455, one change set)".
  - **(vi) The timing rule.** The `effective_tick` rule (summons emitted after the action phase take effect at k+1) carries over unchanged.
  - **(vii) GH `d`.** GH `d` is bit-equal to the recorded value.
- **INFO-1.** `RB-W-l21_qualifying` needs no new key. L-02 and L-07 are disc branches, so they are `eyeofreckoning1`. GH `source` should use that key and leave the branch to a separate field.
- **INFO-2.** Halt (i) in § 4, the gethit replay through `ledger_pass` with the tape draw, is not in the grader. It is owed with gamora's TAPE emitter. Add a per-body emission `seq` to GH so that emission order can be proved, not just assumed.

## Action
- [ ] gamora: write a CORR-3 (or erratum) folding KP-455 per WARN-1 (i)–(vii), with the HOOK row text changed. Add `seq` to GH and the source/branch fields. Land the § F (i) replay check with the TAPE emitter.
- [ ] drax: no change. The KP-452 + KP-455 change set proceeds to my delta Gate-2 under KP-312.
- [ ] Matt: none.

## References
- `reincarnated-engine/src/reincarnated/simulation/math/join1-j4b-d2-adapter-fire-sorc-design-2026-10-14-ADDENDUM-13-CORRIGENDUM-2.md`
- `…-ADDENDUM-13.md` § 1.2; `…-ADDENDUM-13-CORRIGENDUM-1.md` § 1–2
- `reincarnated-engine/src/reincarnated/simulation/scripts/gamora_join4b_grade.py`; `tests/test_join4b_grade.py`
- `agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-run-charter.md` rows KP-452…455
