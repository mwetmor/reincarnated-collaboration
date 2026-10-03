# Engage-review notes (H-3 delta, jack-ryan fork): f37f467 · 70c758d · 0fc806e · 955859b · cb9618c · 8f74db4 · a07f7f5

Method: read-only. Port = `git archive 96fc0cc` (runtime fd799b63). Oracle = engine `969fbd8d`
(`src/reincarnated/simulation/kc2/*`, `simulation/scripts/gamora_kc2_play_v3p{8,9,10,11}_oracle_2026_10_02.py`).
Side-by-side reading, branch for branch. Python was run only on pack CSVs and on the committed G3 oracle traces
(`evidence/kc2-play/2026-10-02-g3-25cell-kp261-V311FULL-96fc0cc/oracle_traces/*.json.gz`). No Godot runs.

## Per commit: what was compared

| commit | port | oracle | result |
|---|---|---|---|
| f37f467 B1 | gd_engage.gd:328-358 (pause_ticks, sp_is_opportunity, sp_note_swing); loader v3p11.gd:458-460 (`int(float(x)*1000.0)`, max(lo,hi)); fight.gd:3206-3218 (pet path) | swing_pause.py:69-114; threat.py:1696-1716, 1824-1827 | faithful |
| f37f467 B4 | gd_engage.gd:364-481 (_choose, _ge_is_opportunity, choose_slot, halt_for), 487-1259 (reposition: _request, _enter_*, _pathfail, is_opportunity, _rfa_trigger, waypoint, _stop_where_close_enough, suppresses, pet_target), 1264-1361 (separate); fight.gd:2719-2754, 3141-3220, 4077-4121, 7347-7357 | gd_engagement.py:84-213; gd_reposition.py:166-852; threat.py:1667-1743; run.py:1996-2000, 2057/2093, 2370-2387, 3801-3822 | faithful (no term divergence found) |
| f37f467 u5 fix | roster.gd hf_swing/hf_oa/hf_damage_by_slot; fight.gd:7732-7781 (_v3p11_slot_overlay, _weapon_rows_of, _hf_on, _oa_row) | threat.py:893-905 (merge_keyed of the 338 rows for every pool record) + gd_engagement.apply_default | faithful by reading; NO PROBE (G3 only) |
| 70c758d B5 | pilot_move.gd (all); fight.gd:2486-2493, 7871-7907 | pilot_move.py:87-172; run.py:327-347, 2597-2602, 2683-2690 | faithful |
| 0fc806e C1 | lineup.gd (all) | referent_lineup.py:184-285 | faithful (capacity law inherited from the incumbent board port, see INFO) |
| 955859b C2 | mutators.gd (all); fight.gd banner 5459-5500, soulfire/bleed 3808-3855, _apply_slot hit/flat rows/pct_add, _land leech, res_used | mutators.py; player_offense.py:486-509; secondary_streams.py:268-310; threat.py:1923-1943, 2098-2101; run.py:1786-1795, 2940-2953, 3172-3347 | **DIVERGENCE (timing of Cruel's factor), latent** |
| cb9618c B2 | global_magnitude.gd attr_of/scaled_terms, _compose; fight.gd _bind_v3p11_phase_b, _comp_dot | global_magnitude.py:319-346, 415-424 | faithful |
| 8f74db4 B3 | fight.gd emergence scan (te = spawn + ceil(D/g − eps)·g), _emerge_tick_eps (il1 V311-IL-01), initial self-cast overlay | p05_emergence.py:57-60, 129-150; initial_self_cast.py:43-66 | faithful |
| a07f7f5 A5 | composition.gd instant/dot; fight.gd 5851-5865 | gd_composition.py:117-178; c11a_corrections.py:109-147; global_magnitude.py:252-260 | faithful |

## The divergence (955859b): Cruel's factor is re-read after the disc phase; the oracle snapshots it once per tick

- Oracle, tick k: `run.py:2945-2953` sets `_mut_f = mutator_fold.player_factor(k)` once, into
  `player_offense.mutator_factor` and `secondary_streams.mutator_factor`. Then the disc resolves; a body it kills fires its
  `dying` slot through `engine.resolve_attack` (`run.py:3172-3212`) → `threat.py:1925-1926 note_monster_hit(k)`. Soulfire
  (`run.py:3289-3308`, `secondary_streams.py:276-277`) and the bleed (`run.py:3313-3329`, `secondary_streams.py:293`, dps fixed
  at application) then use the SNAPSHOT.
- Port, tick k: the disc loop (`fight.gd:2995-3060`) evaluates `_banner_factor_now()` (cached per run_tick at the first body,
  i.e. before any kill: matches the snapshot), kills, `_fire_dying → _apply_slot → mut_fold.note_monster_hit(k)`
  (diff 955859b, `_apply_slot`). Then `_secondary_streams` (`fight.gd:1966` → `3827`, `3847`) calls
  `mut_fold.player_factor(k)` AFRESH, so it sees the window the dying hit just opened.
- The divergent state: Cruel closed at the tick's start, a `dying` hit lands on the player in the disc phase, and a Soulfire
  proc or a bleed (re)application reaches a SURVIVING body on the same tick. Port ×0.92, oracle ×1.0.
- Measured on the 25 G3 oracle traces at 96fc0cc (instrument: inline Python over `oracle_traces/*.json.gz`):
  378 `dying` hits on the player; classification via the trace's per-tick banner factor (cruel-on values 0.951683673469 /
  0.922346938776, cruel-off 1.03443877551 / 1.002551020408): 113 cruel-on at snapshot, **8 cruel-off at snapshot**
  (W1_s1/W1-NULL_s1/M-POL-2_s1 w151 k344; W1_s3/W1-NULL_s3/M-POL-2_s3 w151 k856; M0_s4/M-POL-2-NULL_s4 w151 k391), 257 not
  classifiable (no banner row). The 8 carry no Soulfire/bleed row on a survivor that tick. Every bleed row's 8 % is
  ≥ 1.94e-6 of the body's HP (10,324 rows, 2 M0 cells) and Soulfire's ≥ 2.4e-4, so any occurrence would have broken G3's
  1e-6 body-HP class: G3 25/25 clean ⇒ the full condition did not occur on the G3 draws. **Latent; not certifiable by G3;
  reachable on the port's own generator (T-A) and in PLAY.**
- Fix (drax): take `_mut_f = mut_fold.player_factor(k)` once per tick at the oracle's position (before the disc), store it,
  and use the stored value in `_banner_factor_now`, Soulfire and the bleed. Add a fixture probe: a dying hit after a ≥ 1 s
  lull on a tick with a surviving bled body; control = the fresh read.

## Fail-first quality

- f37f467: "parent RED, 29 checks / 2 failures" = (B1-1) and (B4-1), the "fold bound" checks, each followed by an early
  return. B1 has one mechanism control (B1-5, summed cadence); B4's fixtures cover the Default reach, `_stop_where_close_enough`,
  `_request` (free slot only), `separate`; controls B4-7 (symmetric solver) and B4-9 (tolerance in the ring). **No probe or
  control reaches** D8 persist/whiff, WaitToAttack (poll/roam/50 % RFA roll), pursue path failure → RFA, RFA exits
  (arrive/timer), the D1 RFA trigger, `_request`'s rob branch / LostSlot, `pet_target`, `suppresses`. G3 is their only
  detector.
- 70c758d / 0fc806e / 955859b: parent RED = 1 failure each (the bound check). C1-6's control ("the fold leaves the incumbent
  roll in place") is nominal.
- The yetidire_b01 u5 HONEST-FAIL arming fix has no probe (grep `hf_` / `HONEST` over tests/: none in the v3.11 probes).
- B2 (B2-4: pre-formed product) and A5 (incumbent form; level-blind) controls are genuine mechanism controls.
- Commit times: 4aba33b, cb9618c, 8f74db4, f37f467, 70c758d, 0fc806e, 955859b were authored 18:43:28 → 18:44:54 (86 s). The
  per-commit "RED on the parent's fight" claims therefore were measured during development, not necessarily on the committed
  parent trees. Not re-run here (no Godot lane).

## Literals / cell keys

- No arm/salt/wave/tick literal in a behaviour conditional in these commits' sim/loader diffs (scan:
  `if|elif|and|or … 15x|160|arm names|salt|wave ==|run_tick ==`). Hits: `lineup.gd:156` (the oracle's seed string, not a
  branch); fight.gd (a07f7f5) `for w in range(151, 161)` = a bind-time refusal that every graded wave has a pm4i row.
- Oracle inline literals carried: `_request` `extents_m` default 0.5; `_profile` fallback 0.05 (counted
  `profile_unknown`); `separate` 0.001 / 0.0001 (commented as guards); EPS_CEIL / HALT_SHRINK / UNIT_EPS 1e-9 declared.
- Outside this set, noted: `kc2rt_composition.gd:268-278 f2h_b_holds` (added b46c0b2) hard-codes `f_unmapped == -0.44`,
  `lapm_wave == 160`, `phys_limb == "LO"`, divisor on — prereg expected values inside sim/ (report-face GREEN rule only).

## Equivalences checked by data (not by reading alone)

- Mutator level: port first non-blank `level_min` per record vs oracle last row (`{r["record"]: r ...}`, blank → 0):
  pm2_tg2_monster_timing.csv 169 rows / q91_pool338_monster_timing.csv 338 rows, 0 duplicate records, 0 blanks, 0 differing;
  pet chain 70 threat-actor records, 0 blank owner_level.
- `pct_add` retaliation: port tests the row's `template_group` prefix, oracle tests `retaliation_keys()` (measured empty,
  c11a_corrections.py:57-70). Equivalent while empty.
