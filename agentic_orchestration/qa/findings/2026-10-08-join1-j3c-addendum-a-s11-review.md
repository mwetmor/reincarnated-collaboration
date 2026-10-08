# Finding — 2026-10-08 — JOIN-1 KP-395 · DESIGN-MODE review of J3c inventory ADDENDUM A (S-11, P0 complete)

**Reviewer:** jack-ryan (DESIGN-MODE, before the conductor asks Matt about S-11)
**Severity:** PASS-WITH-NOTES (1 WARN, 4 INFO)
**Target:** godot `25dea91`, `kc2_play/join/J3C-SITE-INVENTORY-d5384b4b.md` Addendum A. The runtime was read at X = `1b244fb`, the oracle at sealed `969fbd8d`.
**Developer:** drax
**Follows:** `3a21b1bba` (my WARN-1 is resolved as S-11)
**Principles applied:** 1, 3, 5

## Checks

**S-11's values and the S-9 bits are verified.** I ran the sealed `channel.tick_period_s` and `channel_policy.derived_parameters` in a child process on the sealed tree, which was left clean afterwards.

| AS | period | lag | A dur | B dur | p (Type-B chance per tick) |
|---|---|---|---|---|---|
| 196 | `0.0816326530612245` | 20 | 16 | 7 | `0.0035510204081632656` |
| 200 | `0.08` | 20 | 16 | 7 | `0.00348` |
| 300 | `0.05333333333333333` | **30** | **25** | **11** | **`0.0023199999999999996`** |

- These equal Addendum A's table. At 196 they equal the pack values the port reads.
- **The S-9 law-order correction is right.** `0.16*100/AS` gives `0.08163265306122448` at 196 (and p `…2647`) and `0.05333333333333334` at 300. Only `0.16*(100.0/AS)` reproduces the oracle and the wire.
- `ticks_per_s = AS/16` (`channel.py:85`). `_ticks` is Python `round`, which is half-even, so the mirror's explicit half-even rule is correct.

**The default path is unchanged.**
- Both S-11 blocks are added-only. They are guarded by `clock != null and clock.rulebook != null and world_clock_moved()`, which is false in ORACLE and PLAY (`clock.rulebook` is null there) and false for JOIN at X = 196.
- The mirror's unit test that the derivation at 196 equals the pack values bit for bit keeps the predicate choice from hiding a disagreement.
- **Every field's oracle-path consumers are covered:** `:2452` (the coin), `:2463` (the B window), `:2491–2492` (the A window). `:1544`, `:1669`, `:2412–2430` and the const 7 are non-oracle only: `_channel_verdict` returns `_cpf_tick_apply()` for `is_oracle` before reaching them (`:2373–2375`).

**Rejecting an out-of-tree write is right for the three tick counts.**
- They are bound inside sealed `bind_wire` from digest-pinned pack data.
- A harness write after bind would be a value substitution outside any guard, which is the class D2 C-1 and the observe-only contract reject.
- Editing the `math_rules` dict would tamper with the pack.
- See INFO-2 for `p`.

**The fail-first is sound and specific.**
- The port opens Type-A at k > 20 (k 21) and the oracle at k > 30 (k 31), which matches `_cpf_typea_open_k = typea_lag_ticks`.
- Earlier divergence is possible only through a Type-B coin landing in [0.00232, 0.00355).
- See INFO-3 for the one thing it must report.

**The control-fold clock is correctly NOT a port site.**
- Sealed `control_application.py:743` (`ticks_per_s = 12.25`, never wired; `dt_ms = 1000/12.25` at `:1018`) and the port's recorded module default (IC7-D-0117) are equal, so the two mirrors stay equal at any X. It is a JOIN *modelling* question, and routing it to gamora is right.
- **Condition:** if gamora answers by rebinding that clock through a rulebook row, the port's `kc2rt_control.gd` reads become a site (S-12) at that moment. The routing should carry that flag.
- The 4000-tick cap is the same case: parity, no site, modelling question.

## Findings

**WARN-1 · "P0 COMPLETE" is shown for the lines reached on the 196 graded path, not for the X path.**
- **What the sweep covers.** The oracle-side sweep is a line probe of `V311-FULL` at 196, salts 0–4. My spot checks of the period-taking oracle functions agree:
  - `p05_emergence.ticks_until`, `wave_advance.ticks_per_poll`, `mutators.new_wave(period)` and `channel_policy`: port counterparts derive from `_period_s()` / `ticks_per_s`;
  - `mech_lift.p_release_per_tick`: the `interrupts_fold` seat, unreached.

  The port-side literal sweep finds no other 196-bound reads on the sim path.
- **What it misses.** A world-300 run reaches lines a 196 run need not reach. For example, the 4000-tick cap now binds at 213 s.
- **Cite:** Discipline #82 (a figure carries its population); #87.
- **Recommendation, cheap, before Matt's S-11 ruling:**
  - line-probe gamora's engine L01-P (world 300) and L01-W@200;
  - diff the reached-line set against the 196 probe;
  - sweep only the difference for clock-bound values;
  - commit both probes' line lists as evidence. The 196 probe is described but not yet committed.

**INFO-1 · The probe evidence needs to be committed.** See above. A claim of completeness needs its reached-line list on record (Disciplines #7 and #80).

**INFO-2 · S-11b could be avoided.**
- `typeb_p_per_tick` arrives as a harness argument (`configure_arm(…, p_typeb, …)`). A JOIN harness passing the derived `p` would be an input, not a substitution, and would need no sealed line.
- drax's preference (one guard family on one provider) is defensible. **Matt's choice; either is sound.**
- If S-11b is sealed, the harness's pack `p` argument is overwritten under a moved clock. Declare it.

**INFO-3 · Make the fail-first RED attributable.**
- Per cell, the RED must name the first differing field, and that field must be release state: the Type-A window, or a Type-B coin in the interval.
- A RED from any other cause is **not** "as predicted".
- **Cite:** Disciplines #80 and #87.

**INFO-4 · The report at `:6703` misstates the value at X.** It prints the const 7 for `typeb_duration_ticks` at X ≠ 196. Declared as report-only. Make sure no graded comparison reads that field at X.

## Action
- [ ] drax:
  - WARN-1 + INFO-1 (X-path line probe and diff; commit both line lists) before the S-11 ask;
  - INFO-3 (attribution in the fail-first output) into PREDICTIONS part 2;
  - INFO-4 (declare it).
- [ ] gamora: the control-fold clock and the tick cap as modelling questions. A Python rebinding of either makes a port site.
- [ ] Matt: S-11 (a + b, or a only with `p` passed in by the harness, per INFO-2) once WARN-1's diff is clean.

## References
- godot `25dea91`: Addendum A; `kc2_runtime/sim/kc2rt_fight.gd` (`:1162–1172`, `:1255–1263`, `:1544`, `:1669`, `:2373–2375`, `:2412–2430`, `:2452`, `:2463`, `:2491–2492`, `:6701–6703`)
- Sealed `969fbd8d`: `channel.py:75–85`, `channel_policy.py:100–150`, `:255–335`, `control_application.py:743`, `:1018`, `mutators.py:94`, `run.py:1212–1216`, `:1789`
