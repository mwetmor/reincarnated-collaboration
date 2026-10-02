# KC2-PLAY · T-A PREREG **v1.15 NOTES COMPANION** (dated 2026-10-02): the H-6 pre-read's owed items, filed as notes · NOT A SUCCESSOR PREREG

> ⚑ **STATUS: IMMUTABLE ON COMMIT. A NOTES COMPANION, NOT A PREREG VERSION.** It changes **no criterion, no expected value and
> no tolerance** of any row. It carries, by FILE sha256:
> * prereg **v1.14** `{{V114}}` (collab `4d64316d`);
> * prereg **v1.15** `{{V115}}` (collab `d84010f2`).
>
> Every row, value, tolerance, pin, precondition and the budget (a fresh 2; the next run is "attempt 1 of 2, overall 4") are
> those two files'. **H-7 reads v1.14 + v1.15 + this companion.**
>
> **Occasioned by:** jack-ryan's H-6 pre-read, PASS-WITH-FINDINGS (collab `fd0851c77`,
> `agentic_orchestration/qa/findings/2026-10-02-kc2-ta-prereg-v1.15-h6-preread.md`, FILE `{{H6}}`), and the conductor's
> KP-248 rulings: WARN-2 is a SCOPE reading, WARN-3 is a CITATION under the row's own clause, and the face-printing
> requirements carry no criterion change. **Nothing here needed a restatement, so there is no HALT.** A restatement would
> have been a HALT to Matt (KP-137).
>
> **Author:** gamora, Run KC2-PLAY; conductor gandalf. **Instruments:** `agentic_orchestration/gamora/analyses/2026-10-02-kc2-play-prereg-v1.15-notes/`,
> committed first and separately (collab `{{INSTR_COMMIT}}`); this file is committed ALONE (D4).

---

## 1 · WARN-2 · `TA-X-13`: corrigendum to v1.14's printed basis, the conductor's scope ruling, and the corrected classifier

**Corrigendum (v1.14 § 0.2, row `TA-X-13`, column "law (a) on the oracle"):** for *"PASS 25/25 (every crit row is
monster-sourced)"* **read** *"PASS 25/25 (0 crit rows sourced by `player`; player-summon `ps_…` crit rows exist and are out
of the row's scope)"*. **The verdict, the criterion and the expected value (0) are unchanged.** The printed basis was false.

**The conductor's scope ruling (KP-248), recorded:** `TA-X-13` counts **the player's own rows** (`source_id == "player"`,
basis `V0 · CritLimb LO`, the player-kit crit limb, as defined at v1.1: *"count of player rows with `is_crit == true` is 0"*).
**Player-summon rows (`ps_…`, `summons.SUMMON_ID_PREFIX`) are OUT OF SCOPE.** Their crit tier is the decoded PTH tier of
`summon_offense.swing` (`th.resolve_hit`, draw site `V9-SITE-17`), a different law, which G3 grades. It is printed, not graded.

**The instrument fix (in the instrument commit):**
* `check_v1p14.py:{{CHK_LINE}}`: the dead clause `player_summon == 0` is removed. It was never live, because the classifier
  never matched `ps_`. It is not repaired into scope, per the ruling. The player-summon count is now printed beside the row.
* `oracle_trace_v3p11.py`: the classifier now keys on `ps_`.
* **Not regenerated:** the traces and `results_v1p14.json` that v1.14 § Z pins were written by the old classifier and keep
  their committed bytes. Their `other` class holds the player-summon and the monster crits together; `player` is
  unaffected. Run on those committed traces, the fixed checker gives `TA-X-13` PASS 25/25. The only difference from the
  committed results is the new printed field.

**The corrected classifier's output** (`census_v1p15n.py`, the oracle of record, 25 cells, leg A):

| source class | crit rows, 25 cells | in `TA-X-13`'s scope? |
|---|---:|---|
| `player` (`source_id == "player"`) | **{{C_PLAYER}}** | **yes: the graded count, expected 0** |
| `player_summon` (`ps_…`) | {{C_PS}} (per cell {{C_PS_RANGE}}) | no (KP-248) |
| monster (roster + pet) | {{C_MON}} | no |
| other | {{C_OTHER}} | — |

{{C_AGREE}}

## 2 · WARN-3 · `TA-X-21`: the measured live `round(` site list under `V311-FULL`, all graded arms

**Filed under the row's own clause** (v1.8–v1.14: *"re-verify the live site list at emission"*), as a CITATION per the
conductor's KP-248 ruling. **No rule, value or tolerance moves.** The rule (every live quantisation site is Python 3
`round`, half-to-even, wrapped `int(round(`; zero bare `round(` on the port's threat path) holds on every live site below.

**Instrument:** `census_v1p15n.py` counts every execution of every source line containing `round(` in every
`simulation/kc2` module. It uses `sys.monitoring` LINE events limited to those lines, and every other location is disabled
at first sight. The run is the oracle of record, five arms × salts 0–4, all waves. The probe returns nothing into the
oracle: each run's capture rows equal v1.14's committed bare runs, {{INERT}}.

**Module scope:** the row's v1.2 basis names four modules: `threat.py`, `deferred_arrival.py`, `dot_timeline.py` and
`control_application.py`. The conductor's KP-248 ruling adds the two GD fold modules that now govern the threat path's
slot timing, `gd_engagement.py` and `gd_reposition.py`. Live sites in other modules are printed for information; they
belong to no `TA-X-21` grade.

{{SITE_TABLE}}

**In scope, live ({{N_LIVE}}):** {{LIVE_LIST}}. Every one is `int(round(`: {{ALL_INT}}.
**In scope, dead under `V311-FULL`:** {{DEAD_LIST}}. Of v1.14's four cited sites, **{{DEAD_CITED}} are dead.**
* `threat.py:1813`, the cooldown write, is superseded by v3.9 GD engagement's `choose_slot` (`gd_engagement.py:187`).
* `threat.py:2182`, the DoT expiry, is bypassed because the active DoT timeline quantises at `dot_timeline.py:380`.

**The ten GD sites:** {{GD_LIST}}.
**Outside the row's modules, live (information):** {{OUT_LIST}}.

**FILE digests of the modules scanned, at engine `969fbd8d`, equal on all five arms ({{FILES_EQ}}):**

{{FILES_TABLE_SITES}}

**For drax (H-4):** re-point the `ta_x_21` emission's oracle site list to the in-scope live list above, with each site's
`file:line` and line text, re-verified at emission against these FILE digests.

## 3 · Face-printing requirements for the verdict file and report (conductor, KP-248; no criterion changes)

1. **`TA-X-30(b′)` vacuity, wherever `n_clamp_stops == 0`.** Print it per cell beside `arena_armed`, as
   *"(b′) vacuous: no clamp stopped a body"*. This replaces v1.15's predicate `r_g4_vacuous == not arena_armed`, which would
   print "tested" on W1. **On the reference the clause is vacuous on 25/25 cells, W1 included: {{W1_CALLS}} clamp calls on
   W1, 0 stops** (jack-ryan WARN-1, relayed to Matt as INFO, veto-open). drax emits `pursuit.n_clamp_calls` and
   `pursuit.n_clamp_stops`. The row stays: it catches a port that spawns outside the wall or overshoots its target.
2. **The 12-trajectory collapse, beside every per-cell count:** *"25 cells / {{N_TRAJ}} distinct trajectories
   ({{N_CLEAR}} clear, {{N_DIE}} die)"*. The classes are `M0 ≡ M-POL-2-NULL` and `M-POL-2 ≡ W1-NULL` on every salt; `W1`
   departs on salts 2 and 3. § F.5 cl. 14's residual (2) reads *"20/25 cells clear w160 ({{N_CLEAR}} distinct clearing
   trajectories)"*.
3. **UNEXERCISED-ON-REFERENT, printed:**
   * the non-waypoint Pursue operand class of `TA-X-30(a′)` (`op = reach(S)·(1 − 1e-9)`): {{PURSUE_STEPS}} steps on 25 cells.
     Every Pursue approach runs through a waypoint;
   * the non-penetration clip: {{CLIP_STEPS}} clipped steps; the solver is never called under `V311-FULL`.
4. **FLAG any port step the clip shortens** (`pursuit.travel_law.n_clipped > 0` or `pursuit.pets.n_moved_clipped_shorter > 0`)
   on the face, as a G3-attention item. The oracle has no live clip, so (a′)'s allowance for a shorter step is satisfied
   only by a port the oracle does not match. G3 must answer for it.
5. **`TA-X-08`'s lethal-tick clause** (§ F.2o, "the lethal tick is censused alive"): print it as exercised on **{{N_DIE}}
   distinct dying trajectories**, not 5 cells. On the 20 clearing cells it is inapplicable (§ F.5 cl. 15).

## 4 · INFO-3 · The SlowChaos / SlowAether divisor clause is UNREACHABLE, not merely unexercised; and two text notes

* **Unreachable.** The graded loader builds {{N_ROSTER}} roster and {{N_PET}} pet profiles. On every arm they carry **0**
  SlowChaos or SlowAether damage rows ({{DIV_PER_ARM}}). The pack's offense data carries none either
  (`monster_offense.json` / `monsters.json` text hits: {{DIV_PACK}}). The `Slow*` DoT types present are {{DOT_TYPES}}.
  `math_rules ⚑ v3p11_rows.dc1 V39-DC1-2` records `population_on_the_v3p8_oracle: 0`.
  * **Print v1.15 § F.2h′'s divisor clause as UNREACHABLE-IN-PACK.**
  * v1.15's sentence *"if the port's realisation composes such a row, the row grades it"* can apply only to a row the port
    fabricated. Any such row is a RED on presence.
  * The bound value is unchanged: `int/200 + 1`, the conductor's KP-244 ruling, upheld at H-6.
* **Note 1: the `a8` sibling.** Each fight job, and `WALK`, constructs the composing fold twice: once with an explicit
  `chaos_aether_dot_divisor=True` ({{A8_TRUE}}), and once as the v3.8 base `Folds`' default-`False` sibling ({{A8_FALSE}}),
  which v3.9 replaces before the fight. **A harness "configured from `a8`" takes the explicit `True` row.** All 105,045
  composing instances on the 25 cells have `divisor=True` (v1.15 § K′).
* **Note 2: the fallback v1.15 omitted.** The clause reads in full: `a_dur = int/200 + 1` **when the body's gmag terms carry
  an intelligence value; `a_dur = 1.0` when `intelligence is None`** (`gd_composition.py:{{FALLBACK_LINE}}`,
  `d = 1.0 if v_int is None else float(v_int) / 200.0 + 1.0`). Otherwise `a_dur = 1.0` wherever `duration_attr_mult` returns
  nothing. Both branches are as unreachable as the clause itself.

## 5 · INFO-4 · § B.0's guard of record

**v1.14 § B.0 and v1.15 § K′ cite the shared OBS-1 guard as guard of record:**
`scripts/gamora_join1_obs1_guard_2026_10_02.py`, engine `9c756081`, FILE `{{GUARD}}`, unchanged at HEAD. Its rules:
* **G1:** 10 rows, w151–w160, with raw outcome `cleared` or `player_death`.
* **G2:** w160 not at the tick cap (cap {{CAP_T}} ticks = {{CAP_S}} s).
* **G3:** 9N rows on w151–w159.
* **G4:** the summed time matches. G4 is not applicable: `run_one` carries no summary layer.

Applied by `census_v1p15n.py` to `run_one`'s own result on every arm, `cell_check` is complete on **{{GUARD_N}}/5 arms
(25/25 salts)** with no truncated salt. The longest wave on any of the 25 cells is **{{LONGEST}} ticks**, well under the
G2 cap. Of the guard's rules, § B.0's own predicate names G1 and G3. **G2 is now named too**, and adding it changes no
verdict: B.0's `termination_reason ∈ {board_empty, player_died}` already excluded a tick-cap stall.

---

## § Z · Instruments

`census_v1p15n.py` (five arms, the oracle of record, read-only) → `check_v1p15n.py` (aggregation; it STOPs on a guard
failure or broken inertness, and none occurred) → `fill_v1p15n.py` (every number and digest in this file). The v1.14
instrument fixes are in the same prior commit.

{{FILES_TABLE}}

*Filed 2026-10-02 by **gamora**, Run KC2-PLAY; conductor gandalf. A notes companion: no criterion, expected value or
tolerance changed; no prereg edited; the oracle not edited; godot not touched; no push. D4 held: committed ALONE.*
