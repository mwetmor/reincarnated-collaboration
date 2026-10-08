# Finding — 2026-10-08 — JOIN-1 J3a close-out (closure tally, PACK_PIN v3, controls + RT, G-D3 re-emission), Gate-2

**Reviewer:** jack-ryan
**Severity:** INFO (verdict **GO**: the G-D3 v3 row may go to Matt as the J3a baseline of record and as G-D4)
**Target:** engine `8b7471ea`, `15611d0a`, `64799df9` (§ 6), `736420c2`, `12adaff3`, `06b9bdb3`, `e2537d58`; collab `304706c0a`, `4b60aa968`, `746d9fd3b`, `4c30b0d64`
**Developer:** gamora · conductor gandalf (KP-384/385)
**Principles applied:** 1, 2, 3, 5 · Disciplines #10, #12

## (1) Certification: HOLDS

| Rulebook | P-J2-9 | GM | § 4.7 v4 | Evidence |
|---|---|---|---|---|
| `15611d0a` closure tally (fail-first `8b7471ea`, RED with `KeyError 'lookups'`) | 30/30 | 7/7 FILE-equal; `n_outside` 0 over 829,625 lookups | BYTE-IDENTICAL; HEAD `e0cd5f74` start = end (star-lord's export-only cut); kc2 tree `7496a28a` | `304706c0a` |
| `06b9bdb3` PACK_PIN v3 (tests `736420c2` → instruments `12adaff3` → rulebook) | 30/30 | 7/7 FILE-equal; `n_outside` 0 in 26/26 | BYTE-IDENTICAL; HEAD `06b9bdb3` start = end | `4b60aa968` |

`git diff ea28195a e2537d58 -- src/reincarnated/simulation/kc2` is **empty**. RT is 7/7 FILE-equal after the controls (`746d9fd3b`).

## (2) § 6 preceded the re-emission: YES

§ 6 was committed at 10:34:35 (`64799df9`), before PACK_PIN v3 (10:38:04). The re-emission's courtesy-gate acquire is logged at 10:57:31, with `JOIN-PROVENANCE` rulebook and engine HEAD both `06b9bdb3`. § 6's predictions are fresh: D-1, CLOSURE with the named counter, the PERIOD HALT, and D-2/3/4 unchanged.

## (3) PERIOD, CLOSURE and coverage: AS SPECIFIED; one labelling note (INFO-1)

**Recomputed from `gd3_report.json`:**
- PERIOD: `n_compared` 250, `n_unequal` 0, HALT false.
- CLOSURE: `n_outside_total` 0; 25/25 cells have the counter; no refused or raised cells.
- Lookups: damage 158,047; Soulfire 206,501; bleed 282,078.

**Coverage is sane, but "196 distinct, all in the 248" is a coincidence of size, not identity.**
- I took the union of the `crit_counters.decoded` keys over the 26 bulk records and compared it with pack v2/v3 `offense_da`. Decoded = (J-S8's 196 − `witchgodguardian_sentinel_crystal|159`) + `ghost_a01_summon|153`.
- Say so in the README. A reader will otherwise take it as "the J-S8 path".
- Also, § 6 asked for the distinct pairs *looked up* (all three sites), but the report gives *decoded* pairs (rows 32/34 only). Add the looked-up figure.

## (4) D-4 and L06-4(e) FALSE: REPORTED HONESTLY

- Both read 15/25 against ≥ 20. Both are reported, not re-scored, and the gate reads `gate_pass: false` on that limb alone while validity is true.
- The Σ statistic **did** move in the predicted direction (−3.9 % ticks). The per-cell "≥ 20/25" threshold was miscalibrated against per-cell trajectory variance (INFO-2).
- *Lesson for J3b preregs:* predict direction on the paired Σ, or on a sign test with a stated α, not on a per-cell majority count.

## (5) Baseline summary: FAIR. I reproduced every figure (INFO-3 is a correction for the record)

**Reproduced from per-cell rows:**
- Survival is 20/25 for the referent and 17/25 under JOIN, with 4 survived → died and 1 died → survived. The exact sign test gives **p = 0.375**.
- Ticks 117,695 → 113,051 (**−3.95 %**). Intake **−5.17 %**. "Fewer ticks" holds in 15/25 cells.
- Per-hit multipliers are ×1.178 and ×1.152, against expected values of 1.176 and 1.151.
- The 21 never-refused cells are **identical** to the first emission. The 4 formerly refused cells all survive, under JOIN and in the referent.
- The labels are present: LOWER-SIDE (board-fed PTH), JUDGED (crit damage 69/57), DECODED (the roll), and referent CD = 12, never firing.

**INFO-3, a correction for the record.** The **first** emission's 21-cell figure "5 survived → died vs 1, p = 0.219" was **arithmetically wrong**: 16 − 5 + 1 = 12 ≠ 13.
- The per-cell rows give **4 vs 1, p = 0.375**. The 21 cells have the same discordant pairs as the 25.
- I repeated the wrong figure in `13cc43bd8`, and `af7535540` restated it. Both are superseded by this row.
- So the earlier reading was **not** more adverse than this one. The superseding text should say "**mis-stated**", not "biased", for the p-value. "Non-random exclusion" remains true of the conditioning.

**INFO-4.** The hit and draw counts include the pre-pass (period calibration, waves 151–156), which draws on the JOIN streams (§ 6 (a)). The multipliers are unaffected because they are structural. Survival, ticks and intake are window-only. One clause in the README would cover it.

## G-D4 = this row closes J3a: SOUND

With no joined kit, X = 196. This is the post-sourcing 25/25 emission at the rulebook of record `06b9bdb3`, which meets both conditions of `13cc43bd8` INFO-1.

It must be re-emitted when:
- a rulebook change touches the `gd-decoded` path, or
- J3b names a kit faster than 196.

Present it to Matt as **"valid measurement; one predicted direction limb (per-cell D-4) failed; the Σ direction held."**

## Action
- [ ] gamora: README clauses for INFO-1 (coverage composition, plus the looked-up count), INFO-3 ("mis-stated", 4 vs 1) and INFO-4 (pre-pass in the counts). All are append-only and non-blocking.
- [ ] conductor: present to Matt with the framing above. Carry the INFO-2 lesson into the J3b prereg.
- [ ] Matt: J3→J4 checkpoint (conductor's KP-385).

## References
- collab `agentic_orchestration/gamora/analyses/2026-10-08-join1-{closure,pinv3,j3a-controls,gd3-v3,gd3}/`; bulk `/Users/admin/Games/join3a-bulk-evidence/gd3-v3-emission-06b9bdb3/records/*.json` (read-only)
- engine `src/reincarnated/output/kc2-rulebook-pack-v{2,3}-*/rulebook/offense_da.json`; prereg `join1-j3a-gd3-instrument-prereg-2026-10-08.md` § 5–6
