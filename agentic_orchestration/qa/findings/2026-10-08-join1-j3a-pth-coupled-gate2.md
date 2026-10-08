# Finding — 2026-10-08 — JOIN-1 J3a pth-coupled / gd-decoded (Gate-2 delta, DEV-MODE)

**Reviewer:** jack-ryan
**Severity:** INFO (verdict **GO**; nothing blocks pack v2 rows)
**Target:** engine `84cc0633` (AMENDMENT-3) · `f1d8fe38` (fail-first) · `5655123c` (rulebook) · `c850a0e7` (corrigendum 1); collab evidence `68e782300`, `61f73c29b`
**Developer:** gamora (star-lord for the § 4.7 run)
**Principles applied:** 1, 2 (smoke gate), 3, 5 · Disciplines #10, #12 (the semantic shift is framed in `5655123c`'s message)

## What I checked

| Check | Result |
|---|---|
| **Soulfire default rationale** | **SOUND.** The data row `pm4l_eor_per_hit.csv:20` carries the Visor as `offensiveCritDamageModifier +12` on `skillmodifiers/…/head_d028_eyeofreckoning.dbr`, graded "EoR-scoped". So 69 for EoR and 57 for Soulfire (a separate skill record, `eyeofreckoning2.dbr`), with the other value printed beside each, is a cited choice. Whether a modifier on EoR reaches the modifier skill's projectile remains open. The bracket covers it (INFO-1). |
| **The 1.1033 / 1.2405 correction** | **CORRECT, and mine was wrong.** `worked_example.summarize(3259, DA, 0.69)` returns 1.1032876564667364 and 1.2405273953024458, matching G-D1(b) bit for bit. The sensitivity rows (PTH 130/135/140 → 1.2331/1.2604/1.2893 at 57 %, 1.2700/1.3004/1.3321 at 69 %; shares 30.8/33.3/35.7 %) also reproduce. |
| **M2 survives only as a labelled bracket; gd-judged refuses** | **YES.** `bracket_sealed_d100` carries `BRACKET_LABEL` and **has no caller in `src/join2_rulebook/`** (grep). `install(crit="gd-judged")` raises `BindRefused` ("retired, renamed gd-decoded"). `gd_decoded` refuses with `GdDecodedValueAbsent` until all four pack v2 rows exist and the model row equals `pth-coupled`. |
| **`ROLL = max(span, PTH)·u`, one draw** | **YES.** `forms._coupled` refuses `p < span`, makes exactly one `draw_u(stream)` call, and calls `coupled_multiplier`. That function computes `roll = max(span_floor, p)·u` and an ascending strict-`>` overwrite over i ≥ 2, which equals the binary's descending cascade for ascending thresholds. Crit damage is added only when the multiplier is above 1.0. Row 32 draws on `crit:player` with `cd_eor`; Soulfire draws on `crit:soulfire` with `cd_soulfire`. |
| **Fail-first preceded the build** | **YES.** Commit order is `f1d8fe38` (08:57) then `5655123c` (08:59); the pack v1 re-cut lands in between and touches export only. I re-ran the `f1d8fe38` test file against an extract of `src/join2_rulebook` at `47c5c94e`: **5 genuine failures** (bracket, G-D1, one-draw, G-D2, tripwire), plus one harness artefact on my side (a sibling test-module import). Against `5655123c` the genuine failures are 0, and the real checkout runs **15/15 passed**. That matches "5 FAILED" as reported. |
| **ORACLE / PLAY exposure** | **NONE.** `git diff 1200ee19 c850a0e7 -- src/reincarnated/simulation/kc2` is empty, and no `reincarnated-godot` path is touched. `gd-decoded` is not a default. GM-0 is 7/7 FILE-equal with 0 JOIN draws and tripwire 0 (`68e782300`). Star-lord's § 4.7 v4 `run_2` has `head_start` = `head_end` = `5655123c`, verdict **ORACLE BYTE-IDENTICAL** (`61f73c29b`, `recut_gate_evidence.json` G-8). Gamora's NO VERDICT run is correctly not quoted. Later HEAD moves (`06d00fb6`, `c850a0e7`) are docs only. |

## INFO
- **INFO-1:** Soulfire's 57 is a JUDGED default. If evidence ever shows EoR modifiers propagating to `eyeofreckoning2`, swap it to 69 with a pack row change only. No code change is needed.
- **INFO-2:** `coupled_multiplier` relies on ascending `pth_thresholds`. One assert at bind (strictly ascending) would make that dependency explicit. Optional.
- **INFO-3:** On the main checkout, `tests/test_join_pj25_guard.py` still has 4 tests failing by design until the guard lands, and this is disclosed. Until they flip, any "suite green" claim must name that file as excluded.
- **INFO-4:** `offense_p` still reads `p2m_attacker_OA` from the pm4o table until the guard commit replaces it. This is disclosed in C-4. It is not a crit column, and the WARN-3 test scans for crit columns.

## Action
- [ ] star-lord: pack v2 rows (`pth_roll_span_floor`, `crit_damage_pct_eor` = 69.0, `crit_damage_pct_soulfire` = 57.0, `crit_model_player_stream_gd_decoded`) may proceed.
- [ ] gamora: INFO-2 optional, at the next rulebook touch.
- [ ] Matt: none.

## References
- engine `src/join2_rulebook/{crit.py, forms.py, bind_oracle.py, hooks.py}` at `5655123c`; `tests/test_join3a_crit.py` at `f1d8fe38`
- engine AMENDMENT-3 (`84cc0633`, corrigendum `c850a0e7`); `data/kc2/pm4l_eor_per_hit.csv:20`
- collab `68e782300` (`gamora/analyses/2026-10-08-join1-j3a/`), `61f73c29b` (`recut_gate_evidence.json` G-8)
