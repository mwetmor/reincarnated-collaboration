# KC2-PLAY · T-A PREREG **v1.15 NOTES COMPANION** (dated 2026-10-02): the H-6 pre-read's owed items, filed as notes · NOT A SUCCESSOR PREREG

> ⚑ **STATUS: IMMUTABLE ON COMMIT. A NOTES COMPANION, NOT A PREREG VERSION.** It changes **no criterion, no expected value and
> no tolerance** of any row. It carries, by FILE sha256:
> * prereg **v1.14** `5bbe7ae5f0c3f73c77ee7cc3e21870ed8523b6d19fa1eae977dff451ef6b2d92` (collab `4d64316d`);
> * prereg **v1.15** `d1c4a75ae2d35b2c27ddd127b18ef0066664eb54926e8466f2fe522a1ca34593` (collab `d84010f2`).
>
> Every row, value, tolerance, pin, precondition and the budget (a fresh 2; the next run is "attempt 1 of 2, overall 4") are
> those two files'. **H-7 reads v1.14 + v1.15 + this companion.**
>
> **Occasioned by:** jack-ryan's H-6 pre-read, PASS-WITH-FINDINGS (collab `fd0851c77`,
> `agentic_orchestration/qa/findings/2026-10-02-kc2-ta-prereg-v1.15-h6-preread.md`, FILE `1a5dfa5b60aa5d8c8084f82559e44563be571d9ca5c432faa17c37309733b171`), and the conductor's
> KP-248 rulings: WARN-2 is a SCOPE reading, WARN-3 is a CITATION under the row's own clause, and the face-printing
> requirements carry no criterion change. **Nothing here needed a restatement, so there is no HALT.** A restatement would
> have been a HALT to Matt (KP-137).
>
> **Author:** gamora, Run KC2-PLAY; conductor gandalf. **Instruments:** `agentic_orchestration/gamora/analyses/2026-10-02-kc2-play-prereg-v1.15-notes/`,
> committed first and separately (collab `8a9ca320`); this file is committed ALONE (D4).

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
* `check_v1p14.py:262`: the dead clause `player_summon == 0` is removed. It was never live, because the classifier
  never matched `ps_`. It is not repaired into scope, per the ruling. The player-summon count is now printed beside the row.
* `oracle_trace_v3p11.py`: the classifier now keys on `ps_`.
* **Not regenerated:** the traces and `results_v1p14.json` that v1.14 § Z pins were written by the old classifier and keep
  their committed bytes. Their `other` class holds the player-summon and the monster crits together; `player` is
  unaffected. Run on those committed traces, the fixed checker gives `TA-X-13` PASS 25/25. The only difference from the
  committed results is the new printed field.

**The corrected classifier's output** (`census_v1p15n.py`, the oracle of record, 25 cells, leg A):

| source class | crit rows, 25 cells | in `TA-X-13`'s scope? |
|---|---:|---|
| `player` (`source_id == "player"`) | **0** | **yes: the graded count, expected 0** |
| `player_summon` (`ps_…`) | 4,281 (per cell 127–206) | no (KP-248) |
| monster (roster + pet) | 132 | no |
| other | 0 | — |

jack-ryan's independent probe (H-6 § 7 WARN-2) read 0 player · 4,281 `ps_` · 132 monster; this census reads 0 · 4,281 · 132: **equal**.

## 2 · WARN-3 · `TA-X-21`: the measured live `round(` site list under `V311-FULL`, all graded arms

**Filed under the row's own clause** (v1.8–v1.14: *"re-verify the live site list at emission"*), as a CITATION per the
conductor's KP-248 ruling. **No rule, value or tolerance moves.** The rule (every live quantisation site is Python 3
`round`, half-to-even, wrapped `int(round(`; zero bare `round(` on the port's threat path) holds on every live site below.

**Instrument:** `census_v1p15n.py` counts every execution of every source line containing `round(` in every
`simulation/kc2` module. It uses `sys.monitoring` LINE events limited to those lines, and every other location is disabled
at first sight. The run is the oracle of record, five arms × salts 0–4, all waves. The probe returns nothing into the
oracle: each run's capture rows equal v1.14's committed bare runs, 25/25.

**Module scope:** the row's v1.2 basis names four modules: `threat.py`, `deferred_arrival.py`, `dot_timeline.py` and
`control_application.py`. The conductor's KP-248 ruling adds the two GD fold modules that now govern the threat path's
slot timing, `gd_engagement.py` and `gd_reposition.py`. Live sites in other modules are printed for information; they
belong to no `TA-X-21` grade.

| site | scope | live hits (25 cells) | `int(round(` | cited in v1.14 | line |
|---|---|---:|---|---|---|
| `alert.py:319` | outside the row's modules | 0 | **no** |  | `return round(f / s)` |
| `alert.py:367` | outside the row's modules | 0 | **no** |  | `return {"n": m, "min": round(s[0], STAT_DP),` |
| `alert.py:368` | outside the row's modules | 0 | **no** |  | `"median": round(` |
| `alert.py:370` | outside the row's modules | 0 | **no** |  | `"max": round(s[-1], STAT_DP)}` |
| `alert.py:390` | outside the row's modules | 0 | **no** |  | `round(expected, INCIDENCE_DP) == round(` |
| `alert.py:394` | outside the row's modules | 0 | **no** |  | `"duration_min_slot_window": slot_window["min"] == round(float(published_secs["min"]), STAT` |
| `alert.py:396` | outside the row's modules | 0 | **no** |  | `slot_window["median"] == round(float(published_secs["median"]), STAT_DP)),` |
| `alert.py:397` | outside the row's modules | 0 | **no** |  | `"duration_max_slot_window": slot_window["max"] == round(float(published_secs["max"]), STAT` |
| `alert.py:403` | outside the row's modules | 0 | **no** |  | `"expected_alerting_actors_full_roster": round(expected, INCIDENCE_DP),` |
| `alert.py:408` | outside the row's modules | 0 | **no** |  | `{round(r.duration_s(speed_composes=False) or 0.0, STAT_DP) for r in can})},` |
| `alert.py:530` | outside the row's modules | 0 | **no** |  | `"t_s": (None if t_s is None else round(float(t_s), EMIT_DP)),` |
| `alert.py:535` | outside the row's modules | 0 | **no** |  | `else round(float(t_s) - float(spawn_t), EMIT_DP)),` |
| `alert.py:536` | outside the row's modules | 0 | **no** |  | `"path_len_before_push_m": round(max(path_len - travel, 0.0), EMIT_DP),` |
| `alert.py:539` | outside the row's modules | 0 | **no** |  | `"travel_this_step_m": round(travel, EMIT_DP),` |
| `alert.py:773` | outside the row's modules | 250 | **no** |  | `"arm_latency_travel_m": round(self.arm_latency_travel_m, EMIT_DP),` |
| `alert.py:781` | outside the row's modules | 250 | **no** |  | `"held_travel_suppressed_m": round(self.held_travel_suppressed_m, EMIT_DP),` |
| `alert.py:783` | outside the row's modules | 250 | **no** |  | `"n": len(q), "mean": (round(sum(q) / len(q), EMIT_DP) if q else None),` |
| `alert.py:784` | outside the row's modules | 250 | **no** |  | `"max": (round(max(q), EMIT_DP) if q else None)},` |
| `alert.py:849` | outside the row's modules | 0 | **no** |  | `"distance_m": round(float(v.distance_m or 0.0), EMIT_DP),` |
| `alert.py:851` | outside the row's modules | 0 | **no** |  | `else round(float(v.duration_s), EMIT_DP)),` |
| `arrival_order.py:293` | outside the row's modules | 0 | **no** |  | `vals = sorted({round(float(b["spawn_t_s"]), 12) for b in bodies})` |
| `calibration.py:503` | outside the row's modules | 0 | yes |  | `override = None if n_scale == 1.0 else max(0, int(round(er * float(n_scale))))` |
| `channel_policy.py:148` | outside the row's modules | 120 | yes |  | `return int(round(seconds / period_s))` |
| `control_application.py:591` | row basis (v1.2 four modules) | 274 | yes |  | `n = max(0, int(exact) if TRUNCATE_BUCKETS else int(round(exact)))` |
| `counterplay.py:212` | outside the row's modules | 25 | yes |  | `return tuple(sorted({int(round(x * BAR_PX)) for x in h}))` |
| `defenses.py:471` | outside the row's modules | 0 | **no** |  | `"r_from_camp_m": round(math.hypot(*d.xy), 3)} for d in defences},` |
| `deferred_arrival.py:329` | row basis (v1.2 four modules) | 0 | yes |  | `return int(round(raw))` |
| `discrete_volley.py:452` | outside the row's modules | 0 | **no** |  | `"dist_m": round(dist_m, 4),` |
| `discrete_volley.py:454` | outside the row's modules | 0 | **no** |  | `"latency_s": round(dist_m / float(ring.velocity), 5),` |
| `dodge.py:193` | outside the row's modules | 0 | yes |  | `refractory_ticks = int(round(DODGE_REFRACTORY_S * ticks_per_s))` |
| `dodge.py:204` | outside the row's modules | 0 | yes |  | `self._react_until_tick = tick + max(0, int(round(latency * ticks_per_s)))` |
| `dot_timeline.py:380` | row basis (v1.2 four modules) | 14,218 | yes |  | `n_ticks = int(exact) if TRUNCATE_NTICKS else int(round(exact))` |
| `gate_model.py:323` | outside the row's modules | 0 | **no** |  | ```max(1, round(delay_s * ticks_per_s)) if delay_s else 0``, memoised at first sight.` |
| `gate_model.py:434` | outside the row's modules | 0 | yes |  | ```max(1, int(round(s.delay_s * self.ticks_per_s))) if s.delay_s else 0`` — the ``max(1, …)` |
| `gate_model.py:438` | outside the row's modules | 0 | yes |  | `return max(1, int(round(seconds * ticks_per_s))) if seconds else 0` |
| `gd_composition.py:189` | outside the row's modules | 0 | **no** |  | `"telemetry": {k: round(v, 1) for k, v in self.tele.items()}}` |
| `gd_engagement.py:121` | GD fold (KP-248) | 9,004 | yes |  | `gate = max(1, int(round(s.delay_s * tps))) if s.delay_s else 0` |
| `gd_engagement.py:187` | GD fold (KP-248) | 11,099 | yes |  | `eng._cooldown_until[key] = tick + max(1, int(round(cd * eng.ticks_per_s)))` |
| `gd_reposition.py:364` | GD fold (KP-248) | 12,484 | yes |  | `X["wpoll"] = tick + max(1, int(round(WTA_POLL_S * tps)))` |
| `gd_reposition.py:365` | GD fold (KP-248) | 12,484 | yes |  | `X["wroam"] = tick + max(1, int(round(WTA_ROAM_S * tps)))` |
| `gd_reposition.py:519` | GD fold (KP-248) | 274,825 | yes |  | `if tick - X["t0"] >= int(round(RFA_TIMER_S * tps)) and d <= S.reach_m:` |
| `gd_reposition.py:530` | GD fold (KP-248) | 6,609 | yes |  | `X["wpoll"] = tick + max(1, int(round(WTA_POLL_S * tps)))` |
| `gd_reposition.py:554` | GD fold (KP-248) | 231 | yes |  | `X["wroam"] = tick + max(1, int(round(WTA_ROAM_S * tps)))` |
| `gd_reposition.py:726` | GD fold (KP-248) | 284,815 | yes |  | `if arrived or (tick - X["t0"] >= int(round(RFA_TIMER_S * tps)) and d <= reach):` |
| `gd_reposition.py:731` | GD fold (KP-248) | 11,184 | yes |  | `X["wpoll"] = tick + max(1, int(round(WTA_POLL_S * tps)))` |
| `gd_reposition.py:739` | GD fold (KP-248) | 378 | yes |  | `X["wroam"] = tick + max(1, int(round(WTA_ROAM_S * tps)))` |
| `global_magnitude.py:880` | outside the row's modules | 0 | **no** |  | `round(mine, 3), rawf, round(budget, 3))` |
| `hunt_pilot.py:131` | outside the row's modules | 0 | **no** |  | `"n_drift_ticks": self.n_drift_ticks, "drift_path_m": round(self.drift_path_m, 3)}` |
| `intake.py:1047` | outside the row's modules | 0 | yes |  | `p90 = srt[min(len(srt) - 1, int(round(0.90 * (len(srt) - 1))))]` |
| `micro_oracles.py:682` | outside the row's modules | 0 | **no** |  | `"margin_pct_on_pinned_target": round(r.margin_pct, 4),` |
| `mutators.py:202` | outside the row's modules | 0 | **no** |  | `t["cruel_active_tick_fraction"] = (round(t["cruel_ticks"] / t["player_ticks"], 4)` |
| `opposition.py:430` | outside the row's modules | 0 | **no** |  | `return round(raw)` |
| `pilot_move.py:184` | outside the row's modules | 0 | **no** |  | `"commanded_moving_fraction": (round(sum(t["n_move_ticks"].values()) / n_on, 4) if n_on els` |
| `pilot_move.py:185` | outside the row's modules | 0 | **no** |  | `"commanded_path_m": round(t["path_m"], 2), "n_jumps": t["n_jumps"], "n_advances": t["n_adv` |
| `player_sustain.py:173` | outside the row's modules | 0 | **no** |  | `total = round(sum(s.value for s in joins), 10)` |
| `player_sustain.py:179` | outside the row's modules | 0 | **no** |  | `"⚑ D_P1_residual_pct": round(ADCTH_PCT - total, 10),` |
| `player_sustain.py:183` | outside the row's modules | 0 | **no** |  | `"⚑ measured_inactive_pct_total": round(sum(s.value for s in inactive), 10),` |
| `player_sustain.py:186` | outside the row's modules | 0 | **no** |  | `"⚑ skill_scoped_NOT_MODELLED_pct_total": round(sum(s.value for s in skill), 10),` |
| `pursuit.py:408` | outside the row's modules | 0 | **no** |  | `vd = sorted({round(float(m.view_distance_m), 4) for m in mv})` |
| `pursuit.py:409` | outside the row's modules | 0 | **no** |  | `mpd = sorted({round(float(m.max_pursuit_distance_m), 4) for m in mv})` |
| `pursuit.py:410` | outside the row's modules | 0 | **no** |  | `ptm = sorted({round(float(m.pursuit_time_ms), 4) for m in mv})` |
| `residence.py:220` | outside the row's modules | 0 | **no** |  | `if len({round(p, 15) for p in periods}) != 1:` |
| `roster.py:398` | outside the row's modules | 0 | **no** |  | `out[k] = {"per_wave": {str(w): round(per[w], 6) for w in sorted(per)},` |
| `roster.py:401` | outside the row's modules | 0 | **no** |  | `"⚑ reproduces_to_3dp": abs(round(tot, 3) - published[k]) < 5e-4}` |
| `run.py:3361` | outside the row's modules | 169,858 | yes |  | `expires=rt + int(round((_exp - t) / period))):` |
| `run.py:3495` | outside the row's modules | 9,339 | yes |  | `led[1] = k + max(1, int(round(c.cadence_s * tps)))` |
| `run.py:3856` | outside the row's modules | 0 | yes |  | `detonation_tick=k + max(1, int(round(slot.detonation_s * tps))))` |
| `spawn_structure.py:161` | outside the row's modules | 0 | yes |  | `RAND_MAX: int = int(round(1.0 / K_RHO))` |
| `summon_offense.py:825` | outside the row's modules | 37,274 | yes |  | `return max(1, int(round(body.swing_period_s * self.ticks_per_s)))` |
| `summons.py:821` | outside the row's modules | 75 | yes |  | `return max(1, int(round(s * self.effective_tps)))` |
| `summons.py:906` | outside the row's modules | 0 | yes |  | `period = max(1, int(round(p[F_IGNORE_INTERVAL] / MS_PER_S * tps)))` |
| `summons.py:1322` | outside the row's modules | 0 | **no** |  | `ts = sorted({round(v["t"], 4) for v in per.values()})` |
| `threat.py:1613` | row basis (v1.2 four modules) | 2,593 | yes | yes | `self._swing_ticks[key] = (max(1, int(round(per / mult * self.ticks_per_s)))` |
| `threat.py:1774` | row basis (v1.2 four modules) | 6,940 | yes | yes | `gate = max(1, int(round(s.delay_s * self.ticks_per_s))) if s.delay_s else 0` |
| `threat.py:1813` | row basis (v1.2 four modules) | 0 | yes | yes | `1, int(round(cd * self.ticks_per_s)))` |
| `threat.py:2182` | row basis (v1.2 four modules) | 0 | yes | yes | `exp = tick + max(1, int(round(r.dot_duration_s * self.ticks_per_s)))` |

**In scope, live (14):** `control_application.py:591`, `dot_timeline.py:380`, `gd_engagement.py:121`, `gd_engagement.py:187`, `gd_reposition.py:364`, `gd_reposition.py:365`, `gd_reposition.py:519`, `gd_reposition.py:530`, `gd_reposition.py:554`, `gd_reposition.py:726`, `gd_reposition.py:731`, `gd_reposition.py:739`, `threat.py:1613`, `threat.py:1774`. Every one is `int(round(`: true.
**In scope, dead under `V311-FULL`:** `deferred_arrival.py:329`, `threat.py:1813`, `threat.py:2182`. Of v1.14's four cited sites, **`threat.py:1813`, `threat.py:2182` are dead.**
* `threat.py:1813`, the cooldown write, is superseded by v3.9 GD engagement's `choose_slot` (`gd_engagement.py:187`).
* `threat.py:2182`, the DoT expiry, is bypassed because the active DoT timeline quantises at `dot_timeline.py:380`.

**The ten GD sites:** `gd_engagement.py:121`, `gd_engagement.py:187`, `gd_reposition.py:364`, `gd_reposition.py:365`, `gd_reposition.py:519`, `gd_reposition.py:530`, `gd_reposition.py:554`, `gd_reposition.py:726`, `gd_reposition.py:731`, `gd_reposition.py:739` (10).
**Outside the row's modules, live (information):** `alert.py:773`, `alert.py:781`, `alert.py:783`, `alert.py:784`, `channel_policy.py:148`, `counterplay.py:212`, `run.py:3361`, `run.py:3495`, `summon_offense.py:825`, `summons.py:821`.

**FILE digests of the modules scanned, at engine `969fbd8d`, equal on all five arms (true):**

| module | FILE sha256 |
|---|---|
| `alert.py` | `adfeda1352ef2e27c352a8d067e1d73bdb6667e340404f95aa242f2eb53e3c07` |
| `arrival_order.py` | `ab0468d6fde72359a556933714ee2027ae0f81791182ec27a0eed46b65f0d148` |
| `calibration.py` | `0cb4b09750076645756b0463133fed8aec9f5b8eb3dcd806045d9c62132c98d9` |
| `channel_policy.py` | `6850878d4fc880eb46fa9106e464426595109eb44dceb0f66424db34cfe2d958` |
| `control_application.py` | `c0b0cc73bea6fb860cf49b2602a507a2a57b6242728cf520bc6a4960b3405643` |
| `counterplay.py` | `f375323d8b2178f40f937fff663687390129298ee29f47988fdd8f12161e4e99` |
| `defenses.py` | `009e590cd770c99b7f9a3e7d8ca36d7d5919aa33a90fdafa74012a7c0b0de5eb` |
| `deferred_arrival.py` | `0a6b579b78aaf748732afadce50558c6f00eb2eb916ea7d9b5def7a69243557a` |
| `discrete_volley.py` | `f20228c9aa3c0b93590826f143816e2d5e5d4ae9f0be0cfae47bd85e9899d80c` |
| `dodge.py` | `7ca3a1395bc31b03c512cbc4dc11cf38bdc9c4ec3c7ce23af25257ec471b11f2` |
| `dot_timeline.py` | `b4a3bb8268c71005b4d2f317cbd9a7b20e505193f09e78924712258ed92cbe37` |
| `gate_model.py` | `85182da16a5566075fb914782ba4d03f880f2ffbd716955924e655006748969f` |
| `gd_composition.py` | `ddb0ceb47e5f08f6c46ace55382cc2b5d6891766443b0d1ef6f02cb906db6b83` |
| `gd_engagement.py` | `776e7048427bbd47bbf9ffb36f9a3d162a990b182fd71e3f207a41c0cafee920` |
| `gd_reposition.py` | `28c2031ddbdd8f30eeaefd10467a81353dfe9004163fd1f18f82f8164fab3c1c` |
| `global_magnitude.py` | `b84816bff76b01c84f93311b427cf7fcf40bcbca3f45a86dbe88998d505b1a94` |
| `hunt_pilot.py` | `7db812d1bfdad71fedb19d60a29ddbad20edc72c9705c2f125d2a6d33f13993e` |
| `intake.py` | `42fd1cc0ac5d96c4d98dd711693663942b824249fb882e2dc72c8ccfd91954d1` |
| `micro_oracles.py` | `3e1d8a6f6c4134324679fc02a8eba74af28997ae5038cca8864a2faf2dc5041e` |
| `mutators.py` | `104debd66443e3ebaa2cf5251f6bf165ef9bcb6966c489ec7ff1c9db07d15bc9` |
| `opposition.py` | `72b699d9e3707bd4ad6aefb6a592a433dd4b674fe05d065562f5ea3a17f74ac2` |
| `pilot_move.py` | `e4e54d78310e1e4c0fccd51a575475ee3789fdb696a32e9d9f9db7c64fb11429` |
| `player_sustain.py` | `851488e10459bca29ecaa19285605fad27169687f58e5831112eb6acbf408672` |
| `pursuit.py` | `2b58fcd8eacf02b7560a71ea3fd652f4934fa69314d7c3f6b5544239b3fdeb34` |
| `residence.py` | `24ff66d0907d9f9c89b26d6c077eea148d3cdab9e982af5f541ebea5ab9a0c94` |
| `roster.py` | `75afebb2e725dd8345f48af99db8a637567b2c146036b41e4964791b48cc140c` |
| `run.py` | `c2224cf3a3430e1d741a2f735f3ff08edbcf91fb442b55d2db1f48aaa9794a47` |
| `spawn_structure.py` | `431539ffd670b7853bd9bff84b8cdb62e6642956372c4267f9f99897bddee715` |
| `summon_offense.py` | `9c150b3a12a690f549e16ea3eaade71c12f73789f7d5373940b6a699f31734ea` |
| `summons.py` | `dad4196c58987eca265790a9126a15b2bcd0c5eaa0e1244e9a11e85afb4eb660` |
| `threat.py` | `18b2500e7c429f67e82e489637212b3f1148762ac7f865d340b2a64f51a2d8a3` |

**For drax (H-4):** re-point the `ta_x_21` emission's oracle site list to the in-scope live list above, with each site's
`file:line` and line text, re-verified at emission against these FILE digests.

## 3 · Face-printing requirements for the verdict file and report (conductor, KP-248; no criterion changes)

1. **`TA-X-30(b′)` vacuity, wherever `n_clamp_stops == 0`.** Print it per cell beside `arena_armed`, as
   *"(b′) vacuous: no clamp stopped a body"*. This replaces v1.15's predicate `r_g4_vacuous == not arena_armed`, which would
   print "tested" on W1. **On the reference the clause is vacuous on 25/25 cells, W1 included: 171,478 clamp calls on
   W1, 0 stops** (jack-ryan WARN-1, relayed to Matt as INFO, veto-open). drax emits `pursuit.n_clamp_calls` and
   `pursuit.n_clamp_stops`. The row stays: it catches a port that spawns outside the wall or overshoots its target.
2. **The 12-trajectory collapse, beside every per-cell count:** *"25 cells / 12 distinct trajectories
   (9 clear, 3 die)"*. The classes are `M0 ≡ M-POL-2-NULL` and `M-POL-2 ≡ W1-NULL` on every salt; `W1`
   departs on salts 2 and 3. § F.5 cl. 14's residual (2) reads *"20/25 cells clear w160 (9 distinct clearing
   trajectories)"*.
3. **UNEXERCISED-ON-REFERENT, printed:**
   * the non-waypoint Pursue operand class of `TA-X-30(a′)` (`op = reach(S)·(1 − 1e-9)`): 0 steps on 25 cells.
     Every Pursue approach runs through a waypoint;
   * the non-penetration clip: 0 clipped steps; the solver is never called under `V311-FULL`.
4. **FLAG any port step the clip shortens** (`pursuit.travel_law.n_clipped > 0` or `pursuit.pets.n_moved_clipped_shorter > 0`)
   on the face, as a G3-attention item. The oracle has no live clip, so (a′)'s allowance for a shorter step is satisfied
   only by a port the oracle does not match. G3 must answer for it.
5. **`TA-X-08`'s lethal-tick clause** (§ F.2o, "the lethal tick is censused alive"): print it as exercised on **3
   distinct dying trajectories**, not 5 cells. On the 20 clearing cells it is inapplicable (§ F.5 cl. 15).

## 4 · INFO-3 · The SlowChaos / SlowAether divisor clause is UNREACHABLE, not merely unexercised; and two text notes

* **Unreachable.** The graded loader builds 507 roster and 68 pet profiles. On every arm they carry **0**
  SlowChaos or SlowAether damage rows (M-POL-2 0, M-POL-2-NULL 0, M0 0, W1 0, W1-NULL 0). The pack's offense data carries none either
  (`monster_offense.json` / `monsters.json` text hits: `monster_offense.json` 0, `monsters.json` 0). The `Slow*` DoT types present are `SlowBleeding`, `SlowCold`, `SlowFire`, `SlowLife`, `SlowLifeLeach`, `SlowLightning`, `SlowManaLeach`, `SlowPhysical`, `SlowPoison`.
  `math_rules ⚑ v3p11_rows.dc1 V39-DC1-2` records `population_on_the_v3p8_oracle: 0`.
  * **Print v1.15 § F.2h′'s divisor clause as UNREACHABLE-IN-PACK.**
  * v1.15's sentence *"if the port's realisation composes such a row, the row grades it"* can apply only to a row the port
    fabricated. Any such row is a RED on presence.
  * The bound value is unchanged: `int/200 + 1`, the conductor's KP-244 ruling, upheld at H-6.
* **Note 1: the `a8` sibling.** Each fight job, and `WALK`, constructs the composing fold twice: once with an explicit
  `chaos_aether_dot_divisor=True` (`IC7-A-V311-0017` (M-POL-2-NULL), `IC7-A-V311-0179` (M-POL-2), `IC7-A-V311-0334` (M0), `IC7-A-V311-0490` (W1-NULL), `IC7-A-V311-0647` (W1), `IC7-A-V311-0792` (WALK)), and once as the v3.8 base `Folds`' default-`False` sibling (`IC7-A-V311-0018` (M-POL-2-NULL), `IC7-A-V311-0180` (M-POL-2), `IC7-A-V311-0333` (M0), `IC7-A-V311-0491` (W1-NULL), `IC7-A-V311-0648` (W1), `IC7-A-V311-0793` (WALK)),
  which v3.9 replaces before the fight. **A harness "configured from `a8`" takes the explicit `True` row.** All 105,045
  composing instances on the 25 cells have `divisor=True` (v1.15 § K′).
* **Note 2: the fallback v1.15 omitted.** The clause reads in full: `a_dur = int/200 + 1` **when the body's gmag terms carry
  an intelligence value; `a_dur = 1.0` when `intelligence is None`** (`gd_composition.py:169`,
  `d = 1.0 if v_int is None else float(v_int) / 200.0 + 1.0`). Otherwise `a_dur = 1.0` wherever `duration_attr_mult` returns
  nothing. Both branches are as unreachable as the clause itself.

## 5 · INFO-4 · § B.0's guard of record

**v1.14 § B.0 and v1.15 § K′ cite the shared OBS-1 guard as guard of record:**
`scripts/gamora_join1_obs1_guard_2026_10_02.py`, engine `9c756081`, FILE `5f3f4f1e29d147e528709ef317b20ae226edc04c60534d9d506e987d5a3b54d2`, unchanged at HEAD. Its rules:
* **G1:** 10 rows, w151–w160, with raw outcome `cleared` or `player_death`.
* **G2:** w160 not at the tick cap (cap 4000 ticks = 326.531 s).
* **G3:** 9N rows on w151–w159.
* **G4:** the summed time matches. G4 is not applicable: `run_one` carries no summary layer.

Applied by `census_v1p15n.py` to `run_one`'s own result on every arm, `cell_check` is complete on **5/5 arms
(25/25 salts)** with no truncated salt. The longest wave on any of the 25 cells is **968 ticks**, well under the
G2 cap. Of the guard's rules, § B.0's own predicate names G1 and G3. **G2 is now named too**, and adding it changes no
verdict: B.0's `termination_reason ∈ {board_empty, player_died}` already excluded a tick-cap stall.

---

## § Z · Instruments

`census_v1p15n.py` (five arms, the oracle of record, read-only) → `check_v1p15n.py` (aggregation; it STOPs on a guard
failure or broken inertness, and none occurred) → `fill_v1p15n.py` (every number and digest in this file). The v1.14
instrument fixes are in the same prior commit.

| file | sha256 |
|---|---|
| `census_v1p15n.py` | `562c92854339a50573210e93f26752fa9aede6b9f2db9ba65c90ba134a431050` |
| `check_v1p15n.py` | `405e0228ec413ac7182b028cf3f45759c41e9c4fa6466445057e12b3fabb88f3` |
| `results_v1p15n.json` | `25e03f1fbcbc1cf0573bee303c06c61ea0943c89e772869a301008ae64062faa` |
| `fill_v1p15n.py` | `1eda4cd1903397e91c63dbb4e229e9bab5a0e0e0bc7cdce45e5237aab4946974` |
| `notes.template.md` | `f99eb42ab304bf9ace786449c1b72372ba6ec6d6e3ae833c6729750238b75160` |
| `census/census_M-POL-2-NULL.json.gz` | `36f0db2054931682d1b28f991a20f9e67a6a1f950b7003f5d45d74ba8ca1154d` |
| `census/census_M-POL-2.json.gz` | `0d105edc349cdd28539754d3b28e0309c3cc8989ab0331a15fec7d91d7ebf445` |
| `census/census_M0.json.gz` | `de90492ff0b5b5cc82dfe404d0ab667b726460ead26537ed86b2d6cdd6713e37` |
| `census/census_W1-NULL.json.gz` | `89ca2c15b22521b6266045d5a29acf908d3e7ba0fb2781107e5dde2835c04da1` |
| `census/census_W1.json.gz` | `98af843bee3559f95c1e7a7d60e4a069b88454c722fe0a205481c25f3a666efd` |
| v1.14 folder `check_v1p14.py` (fixed, KP-248) | `b4313aaeee4ac0becc0515bc4c0806897c7139b8534ccd9f8c232e07b1f37025` |
| v1.14 folder `oracle_trace_v3p11.py` (fixed, KP-248) | `065b09e3326a1c4af79c9196fa03215f093a2e38d2d5493c77b05fbad997a6e4` |

*Filed 2026-10-02 by **gamora**, Run KC2-PLAY; conductor gandalf. A notes companion: no criterion, expected value or
tolerance changed; no prereg edited; the oracle not edited; godot not touched; no push. D4 held: committed ALONE.*
