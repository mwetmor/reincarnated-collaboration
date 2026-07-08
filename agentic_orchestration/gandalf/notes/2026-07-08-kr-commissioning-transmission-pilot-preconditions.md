# KR Commissioning Transmission — Two-Leg Pilot Preconditions (Matt-Ratified 2026-07-08)

**From:** gandalf → **To:** knight-rider (session-start pickup)
**Date:** 2026-07-08
**Authority:** Matt ratified the two-leg pilot process same-day ("wholeheartedly agree");
KR's code-hold (post-forensic) releases on this transmission.
**Context anchors (read first):** post-mortem
`agentic_orchestration/gandalf/notes/2026-07-08-1800-run-postmortem-misinstrumented-emission-fire.md`
**§8 governs**; engine tracker SESSION-DELTA 2026-07-08 (corrected block).

---

## Unit 1 — rocket (one Gate-1 unit, two beats)

**(a) Encounter-catalog extension** (`generation/endgame_encounter_catalog.py`):
- ≥1 `escape_lane` encounter **MANDATORY** — F4's sole member shell; the four-family
  conjunction is unsatisfiable without it (season_emit ≡ 0 by construction, §8.2).
- `dense_cell` **RECOMMENDED** — F1 rigor parity with the pilot standard (emission currently
  judges F1 without its hardest member).
- **Seam note (ADR-004):** rooms = rocket's file; but band-table keys
  (`ENCOUNTER_COHORT_KPM_BAND` / `SPATIAL_ENCOUNTER_KPM_BAND`) + the 18-count assertions
  (`gauntlet_sim.py:1205`, `t4_sim_cycling.py:620`, `GAUNTLET_ENCOUNTER_COUNT_EXPECTED`) live in
  gamora's `gauntlet_sim.py` — KR splits or sequences with MIGRATION. escape_lane's F4 criterion
  (exit-window ≥0.80 + KPM [60,150]) is already registered in `_shell_result_passed`; wiring
  check, not re-derivation.
- **gandalf rider:** my design read on the per-family room roster rides the Gate-1 review
  (which rooms per family the emission rotation carries; the F1 rigor question rules there).

**(b) Feed dedup** (`season_generation_pipeline.py:1717-1726`):
- Submit **distinct `legendary_id`s only** (currently `all_configs.append` is unconditional →
  ~100× redundant fights of the same cell-config; 1,800 kits → 2,422 submitted configs).
- This ENFORCES the code's existing cell-grain contract (`:1710-1714`) — not a semantics change.
- **MANDATORY rider — halt-loud byte-identity assert:** same-lid configs must be identical; if
  `_build_legendary_config` leaks sample-derived fields, the contract comment lies — die loud,
  never certify quiet. (We were just burned by a stale docstring; comments are claims, not proof.)

## Unit 2 — gamora (two beats)

**(a) F3 `boss_damage_scale` rank-deficiency fix** — the standing STOP; pilot precondition
(F3 leg validity — boss fights under a rank-deficient damage scale produce garbage F3 data).

**(b) Leg-ii harness prep:** 18 cells × ~6 kits, **kit-grain** family verdicts on the spatial
harness. **Sampling discipline: draw from the seed-57000000 population, NOT fresh rolls** —
GRAIN must measure the actual population emission would stamp.

## Pilot firing condition + shape

Fires when **all three preconditions land** (catalog · dedup · F3 fix):

- **Leg i — emission path, cell-grain, SAME SEED (57000000):** post-dedup the gauntlet fights
  only ~20-70 distinct configs (near-free). Returns **PIPE** (rotation contains escape_lane;
  per-family verdicts emit; conjunction reachable) + **YIELD** (per-cell × per-family map =
  season_emit yield by construction).
- **Leg ii — kit-grain spatial sample:** returns **GRAIN** (within-cell verdict heterogeneity;
  F1 pilot's 25/40 kit-grain split is prima facie it's real). If same-cell kits diverge:
  demo-roster kits get individual kit-grain certification (roster-sized); population cert stays
  cell-grain.
- **SIZING** synthesized from both legs; roster need is the denominator, not 1800.

**#2-FF applies to the pilot dispatches themselves** (eat our own cooking, pre-ratification):
each dispatch names the verdict-rendering instrument + a one-command pre-fire verification
(e.g., `grep -c escape_lane generation/endgame_encounter_catalog.py` ≥1; first-log-lines
expectation "N distinct configs | 19+ encounters") + cites the precondition state it stands on.

## Parallel track (NOT gated by this transmission)

Matt rulings proceed in the gandalf session while the code work runs: **§4 acceptance-layer
reframe** (lean A-firm filed; jack-ryan review leg) → **F2 flag-pass** (rules inside §4's
vocabulary). **F4-martial disposition fork drafts AFTER Leg ii** (Matt-accepted lean —
evidence-shaped options over speculative ones). **No emission fire of any size** until the
pilot's verdicts land and the rulings close.

---

**Sign-off:** gandalf, 2026-07-08. Companion: Discipline #2-FF proposal (jack-ryan ratification
queue) — `2026-07-08-discipline-2-amendment-full-fire-rider-proposal.md`.
