# Finding — 2026-10-08 — JOIN-1 KP-394 · DESIGN-MODE review of drax's J3c site inventory

**Reviewer:** jack-ryan (DESIGN-MODE, Gate-1 peer, before Matt rules on the J3c change set; conductor gandalf)
**Severity:** WARN (1 WARN, 5 INFO; no BLOCK, since nothing is built)
**Target:** godot `b8ceb52`, `kc2_play/join/J3C-SITE-INVENTORY-d5384b4b.md`. The runtime was read at X = godot `1b244fb`, the last `kc2_runtime/` commit, with a clean tree. Rulebook `d5384b4b`. The sealed oracle is `969fbd8d`.
**Developer:** drax
**Principles applied:** 1, 3, 5

## Answers

**(1) S-10 is the only new site for the ENERGY step. The null path is unchanged by construction.**
- **The energy step.** In `kc2_runtime/**`, the only energy mutations on the JOIN branch (`is_oracle and play_driver == null`) are `:1785` (income) and `:1790` (`energy -= cost`), with `cost` from `:1786`. The other mutations are:
  - per-wave resets to the ceiling (`:1529`, `:1548`, `:1652`, `:1673`);
  - the PLAY branch (`:1951` / `:1953`, gated `not is_oracle or play_driver != null`);
  - `kc2play_driver.gd:522` (PLAY casts);
  - tests.

  `oracle_energy_cost_per_tick()` (`:4808`) has exactly one caller. The oracle side agrees: sealed `run.py:1260` computes `per_tick_cost` once, and `:2316` / `:2321` read that same local, so a single port local feeding both the dry-out check and the charge is faithful.
- **The null path.** S-10's two lines are a G-A block whose condition (`rulebook != null`; `rulebook` is an untyped member at `:142`) has no side effects. The null path is therefore unchanged by construction, and J-S8 bit-equality plus § 4.7 / G3 prove it empirically. PLAY cannot reach S-10 at all, because S-10 sits inside the oracle-only branch.
- **But "the ONLY new sealed site" overall is not established. See WARN-1.**

**(2) The IN-FORM verdicts are sound, with one control owed.**
- **`_c11a_res(b, "Physical")` (`:3014`):** it is the sole "Physical" caller. It runs unconditionally once per disc-hit body, after `n_hit += 1` and before H-11 (`:3031–3033`), with no `continue` in between. `rulebook.applied_damage` has no other caller. An override that records and returns `super` unchanged fits the observe-only contract.
- **Control owed (INFO-1).** The port keys defence on the **body's** `b["wave"]` (`:3006`), while Python's guard and coupled draw key on `self.wave`, the fight wave (`forms.py` `damage_against_`). The observer should record both and assert `b["wave"] == fight.wave` on every H-11, counting any mismatch.
- **Row 35:** sound.
  - Monster G1 is observed from `_resolve_hit`'s `p`. Summon G1 is item 8.
  - The inventory's list of `pth_minimum` reads misses `:5775`. That read is an `is_nan` test feeding the `n_pth_floor_unwired_consults` counter. It is inert on JOIN, because `:5720` binds the value, and it does not read the value of any L-04 floor (INFO-2).

**(3) P0-4: yes, it hides a further site, and the oracle's own code shows it. → WARN-1.**

**(4) The RNG decision (replay through `--draws`, no MT19937 in the runtime) is sound.**
- It is consistent with SKIRT § 2 and KP-204: bit-equality is defined on the oracle's draws.
- `ReplayStream` refuses kind or argument drift and exhaustion, and reports `unserved`.
- **Owed (INFO-3):**
  - the engine-side recorder must emit the JOIN-only `crit:{player,soulfire,intake,summon}` traces per (arm, salt, stream). Confirm that gamora's recorder covers them;
  - make `n_mismatch == 0` **and** `unserved == 0` per `crit:*` stream a graded gate, not a report.

**(5) The proof plan is complete except for the gaps below.** It covers fail-first L01-P, § 4.7, G3, T-A, the census, J-S8 ORACLE 7/7 plus P4b JOIN 7/7 (both halves), and the windowed `.app` at X and then at the new digest. The gaps are WARN-1's sequencing and INFO-1, INFO-3 and INFO-4.

## Findings

**WARN-1 · P0-4 is a clock-following quantity in the oracle and a 196-bound constant in the port. It is a probable further site, and it confounds S-10's own proof.**
- **The oracle.** Sealed `channel_policy.derived_parameters(period_s)` (`:100–118`) derives the release parameters at call time from seconds and the period:
  - `typeA_lag_ticks = _ticks(REF_TYPEA_LAG_MEDIAN_S, period_s)`;
  - `typeA/B_duration_ticks = _ticks(dur_s, period_s)`;
  - `typeB_p_per_tick = lam_b · period_s`.

  **These follow the clock.**
- **The port.** It reads them as fixed integers and rates from the pack (`kc2rt_fight.gd:1162–1167`; `typeb_p_per_tick` `:303`), as exported at 196.
- **Consequence.** At any world X ≠ 196 the two mirrors run different release schedules. The only fixes are a sealed re-derivation (an S-11 at the read site) or a refusal under `world_clock_moved()`.
- **A refusal would block S-10's own fail-first and proof.** L01-P runs at world 300, and S-9 (ii) runs at `world = kit = X`. Without either fix, L01-P's post-S-10 ROWSET equality against gamora's engine run fails for a reason unrelated to S-10.
- **Cite:** Principle 3; Discipline #76 (derive, don't enumerate); #75 (the instrument must bind what ships).
- **Recommendation:** settle P0-4 against `channel_policy.py` and complete the P0 sweep **before** Matt rules. The change set Matt rules on should then be S-10 **plus** P0-4's resolution: S-11, or a refusal together with a re-planned L01-P. Otherwise the "one consolidated ruling" will need a second ruling.

**INFO-1 · Identity-observer key.** See (2). Record `(b.record, b.wave, fight.wave)` and assert that the waves are equal. The negative control (identity shifted by one body → RED) stands as written.

**INFO-2 · Row-35 enumeration.** Add `:5775` to the list of `pth_minimum` reads, marked inert (an `is_nan` test feeding a counter).

**INFO-3 · Replay prerequisites.** See (4).

**INFO-4 · `charge_bound` cardinality.**
- Python calls `charge_per_tick_` **once per `simulate_wave`** (`run.py:1260`, wave setup). Port S-10 calls the mirror form **every tick**. Values are equal because `h` is run-constant, but any count-based counter comparison will differ by a factor of about the number of ticks.
- **Action:** PREDICTIONS part 2 should either count once per wave on the port or compare value sets only, and state that `h` is asserted run-constant. The mirror can cache `h` at arm and assert it equal on every call.

**INFO-5 · `charge_per_tick` return type.** `cost` is an inferred `float` local. The mirror form must return a `float`, never `null` or an `int`. A trivial assertion in the form suffices.

## Action
- [ ] drax:
  - WARN-1: run the P0 sweep now, P0-4 first, against `channel_policy.py`; propose S-11 or a refusal plus a re-planned L01-P; fold the result into the inventory before the ruling;
  - INFO-1, INFO-2, INFO-4, INFO-5 into the inventory and PREDICTIONS part 2.
- [ ] gamora: INFO-3 (confirm the engine trace recorder covers the `crit:*` streams).
- [ ] Matt: rule on S-10 **together with** P0-4's resolution, not S-10 alone.

## References
- godot:
  - `kc2_play/join/J3C-SITE-INVENTORY-d5384b4b.md`
  - `kc2_runtime/sim/kc2rt_fight.gd` (`:142`, `:1162–1167`, `:1781–1790`, `:1947–1953`, `:3006–3033`, `:4803–4809`, `:5720`, `:5775–5790`)
  - `kc2_runtime/play/kc2play_driver.gd:522`
  - `kc2_runtime/sim/kc2rt_rng.gd`
  - `kc2_play/tools/kc2p_join1_gm_emit.gd` (`ReplayStream` `:183`, unserved `:1137`)
- Sealed engine `969fbd8d`: `simulation/kc2/run.py:1260`, `:2316–2321`; `energy.py:57–68`; `channel_policy.py:100–146`.
- Rulebook `d5384b4b`: `src/join2_rulebook/forms.py` (`kit_hits_per_tick` `:236`, `charge_per_tick_` `:395`, `damage_against_`).
