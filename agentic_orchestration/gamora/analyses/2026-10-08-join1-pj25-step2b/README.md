# JOIN-1 · P-J2-5 step 2b: DA sourcing over the line-up roster, the pre-pass and their pet closure (KP-379/380)

**gamora, 2026-10-08.**
- **Prereg:** engine `join1-pj25-step2b-roster-population-prereg-2026-10-08.md`, committed alone before the run.
- **Census instrument:** `gamora_join1_pj25_step2b_census_2026_10_08.py`.
- **Run instrument:** `gamora_join1_pj25_step2b_2026_10_08.py`, committed before its run.
- **Edition IV**, build 24825149; the source pre-check passes. The run opened 8 vendor files, none from another edition.

## Verdict: PASS, no HALT. All 47 new sourced pairs are CERTAIN.

| Prediction | Result |
|---|---|
| Population counts: A 173 · B 62 · A∪B 209 · **P 248** · new 52 (5 measured, 47 to source) · depth-2 5 · capped-out 19 | **all equal** (`counts_ok`); the 196 J-S8 pairs ⊆ P |
| S2b-CAL-1: S2-CAL-1 on the same 74 pairs, bit-exact | **74/74, max Δ 0.0** |
| S2b-E_L == 130.36799999999994 | **bit-equal** |
| S2b-REPRO: the 122 sourced path pairs reproduce `s2_apply` of record | **122/122 bit-equal** (DA, p, p at DA+E_L, class, L) |
| S2b-MEAS: the 5 new measured pairs, library vs table | **5/5, Δ 0.0**; table p 109.48 … 110.68 |
| S2b-CLASS on the 47 new sourced pairs | **47 CERTAIN** · 0 UNDECIDED · 0 BELOW · 0 UNSOURCEABLE |

**The 47 new pairs:**
- 38 come from the line-up roster and 9 are pets.
- By body class: 23 bounty, 16 common, 7 summon, 1 hero.
- **Minimum p** = 107.131, at `devotion/chthonianherald_h03|157`. Its level margin is 20.9, i.e. 20.9 levels of level-rule error before the verdict would flip.
- **The G-D3 refusal body, `ghost_a01_summon|153`:** p = 123.24, CERTAIN.
- **The 5 depth-2 pets** (structurally unspawnable, included per KP-380) are all CERTAIN.
- **7 pairs are labelled "CERTAIN under L-RULE-B; class uncalibrated":** the summon class has no measured representative among the 74 (as in step 2).

## The census (prereg § 0)
Bulk is at `/Users/admin/Games/join3a-bulk-evidence/step2b-census-oracle/` (25 cells). The run records each file's sha256 in `s2b_report.json` → `census_shas`. Findings:

- **The instrument is validated:** the census's struck union equals the J2 196-pair path exactly.
- **A line-up-free PRE-PASS, waves 151–156, inside every cell.**
  - Call chain: emitter `run_cell` → `c11a._period()` → `w1w2_lift_build.run_cell` → `i26 replay` → `simulate_wave`.
  - Its spawn set (62 pairs) is identical in 25/25 cells. The player strikes those bodies.
  - **The G-D3 refusal body is a pet of pre-pass ghosts.** So KP-379's wording ("the line-up roster") alone would not have covered it. B is in P for that reason, **flagged here as an extension of the ruling's wording.**
- **No carry-over.** No body is struck in a wave other than its spawn wave:
  - structurally, `PlayerOffense(wave=w)` is built per wave, and actors and `pet_state` are locals of `simulate_wave`;
  - empirically, 0 cases in 25 cells.

## Next (KP-379 sequence)
1. jack-ryan delta.
2. star-lord cuts pack v3 `offense_da` (248 rows, from `s2b_report.json` plus the measured table rows).
3. gamora moves PACK_PIN to v3.
4. Then the deferred controls, the G-D3 re-emit (D-1 as a FRESH prediction, plus the § 3 closure test predicted 0) and RT.

**INFO-V2-3:** the sealed referent's `fixture.CRIT_DAMAGE_PCT` is **12** (the Visor alone), not 57 or 69.
