# Finding — 2026-06-19 — gamora DPS-measurement instrumentation (boss MEASURE + STR classification)

**Reviewer:** jack-ryan (DEV-MODE, Gate-2)
**Severity:** PASS-WITH-INFO
**Target:** engine `26a6f27` (tag `gamora/v-dps-instrument-1`); collab re-run `a9a68f1`. NOT pushed (Matt-gated, ADR-006).
**Developer:** gamora (simulation seam)
**Principles applied:** Review Principles #2 (smoke-gate), #3 (cross-seam impact), #4 (decisions-log as truth), #6 (empirical-inspection-over-assumption). Engineering disciplines #1, #2, #11, #12.

## Verdict

**PASS-WITH-INFO.** Every load-bearing claim (V1–V5, no-double-count, no-gate-regression, no-star-lord-MIGRATION, the empirical STR numbers) was reproduced FIRST-HAND on disk — none taken on gamora's report (the Gate-1 lesson on this exact workstream). The single INFO is a code-citation imprecision in the math note (wrong subdirectory in the path); it is non-blocking because every line number resolves correctly within the real file. The three new fields are a clean additive schema change, RECORDED-NEVER-GATED. The STR numbers are trustworthy to rule a design disposition on.

## What I found

gamora added three additive `float = 0.0` fields to `SpatialFightResult` (`player_damage_total`, `damage_to_boss`, `boss_max_hp`) backed by two scratch accumulators on `SpatialEntity` (`delivered_damage_dealt`, `delivered_damage_received`), clamping overkill per-hit at the single `_apply_skill_damage` site and attributing boss damage via `_boss_focus_entity`. The build surfaces per-fight DELIVERED damage the spatial sim already computes but previously dropped (`player_damage_dealt=0.0` hardcoded), giving the encounter-doctrine's boss MEASURE (DPS / boss_HP_removed) and the disambiguating signal for STR's boss failure. I read the actual damage path, the boss-focus setup, the self-heal site, the result-assembly, every gate function, the SQLite writer, the harness, and the re-run JSON. The instrumentation is correct, purely additive, and does not enter any gate. The math note is math-before-code (Discipline #1), thorough, and cites code for every claim — the citations are accurate modulo one wrong subdirectory.

## V1–V5 — each reproduced first-hand on disk

- **V1 (proxy-inclusive) — REPRODUCED.** `proxy_population.py:32` verbatim: "proxies in the spatial port deal NO spatial damage and take NO spatial position — the port is a POPULATION/LIFETIME instrument only" (and `:74` "the spatial population port does NOT apply proxy damage"). I confirmed there is exactly ONE call site of `_apply_skill_damage` (`spatial_engine.py:1610`) and it passes `self.player` as the only attacker. `_proxy_damage_unit_seconds` (`:1755`) is a damage-POTENTIAL integral, never `target.hp`. So the player accumulator IS the complete delivered-damage measure today because proxies deliver zero HP damage. The forward-flag (a future proxy-spatial-damage regime would need a `proxy.delivered_damage_dealt` term) is honest and correctly raised.
- **V2 (no double-count) — REPRODUCED.** Per-hit clamp `_delivered_this_hit = dmg if dmg < target.hp else target.hp` at `spatial_engine.py:1137` (resolver path) AND `:1150` (legacy path). Single accumulation at `:1163` (`attacker.delivered_damage_dealt += delivered`). DoT is NOT a separate over-time HP channel — `resolve_skill` returns a single consolidated `total_damage` float with DoT/ailment folded in (`damage_resolver.py:576`, accumulation at `:462`/`:505`). Exhaustive grep of mob-HP-decreasing sites shows ONLY `:1138`/`:1151` (both inside `_apply_skill_damage`). The accumulators are written ONLY at `:1141`/`:1154`/`:1163` — no stray writes.
- **V3 (faithful power) — REPRODUCED.** `apply_max_profile_investment: bool = True` is the chain default at both runner ends (`spatial_engine.py:1947`, `:2167`), post-FLIP #3 (ratified `f32e48a`, decisions-log 2026-06-18). The resolver returns post-mitigation float (`spatial_resolver_adapter.py:281`, `:299-303`). The re-run metadata confirms `smoke:false`, single regime, faithful.
- **V4 (MEASURE-not-GATE — LOAD-BEARING) — REPRODUCED with my own defensive grep + empirical cross-check.** I grepped every read of the three fields across `src/`: they appear ONLY in (a) the write-site `spatial_engine.py:1906-1914`, (b) the dataclass def `spatial_telemetry.py:293-295`, (c) the `FightSummary` pass-through `t4_sim_cycling.py:208-211,1108-1111`, (d) the harness report `clean_boss_numbers_harness_2026_06_19.py`. I then read the gate logic: `StratumFightBatch` properties (`t4_sim_cycling.py:228-267`) read `player_won`/`kills`/`duration_s`/`termination_reason`; `_evaluate_compound_gate` (`:795-840`) reads only `observed_kpm` + `survival_rate` (HARD-BLOCK sg1/sg2) plus sub-gates 3–6 on kills/timeout; even the sub-gate NAMED `_check_zero_damage_floor` (`:714`) reads `f.kills == 0` (zero-KILL, NOT zero-damage). **Empirical cross-check from the re-run itself: 832 cells have `boss_HP_removed > 0.9` yet `sg_overall = BLOCK`** — if any gate read the damage measure, near-full-boss-HP-removed cells could not all BLOCK. Gate verdict is decoupled from the measure in code AND in practice. The #8 anti-homogenization guarantee holds.
- **V5 (boss-entity attribution) — REPRODUCED.** `_boss_focus_entity` set ONCE (`spatial_engine.py:1331`) via `self.mobs[focus_index]`, `focus_index = scenario.boss_index` (boss_killed) or `scenario.mini_boss_index` (else), gated on `win_condition in BOSS_FOCUS_WIN_CONDITIONS` (`:1324`) — the same indices the outcome resolver uses to decide the win. At result-assembly (`:1907-1914`): `damage_to_boss = _boss_focus_entity.delivered_damage_received`, `boss_max_hp = _boss_focus_entity.max_hp`, both 0.0 when no boss focus. Boss shells set both adds `suppress_leash_hp_reset=True` (`arena.py:509/519` for boss_with_adds, `:751/761` for mini_boss), so the §3.1 leash-reset caveat is correctly handled.

## Also confirmed

- **`boss_HP_removed > 1.0` is self-heal, NOT a clamp leak — REPRODUCED.** The only mob-HP-INCREASING site is `spatial_engine.py:1662` `mob.hp = min(mob.max_hp, mob.hp + heal)` (mob's own action phase, geo self/none). The per-hit clamp is vs LIVE HP, so re-removing healed HP is correctly re-counted as new HP removal. gamora's cited 240s mini-boss timeout reaching 8.5× traces to cumulative delivered damage against a regenerating target, not double-counting.
- **No star-lord MIGRATION — REPRODUCED.** The SQLite writer uses an explicit positional `_INSERT_SQL` tuple of named attributes (`telemetry/spatial_recorder.py:148-173`) — no `asdict()`, no reflection — and the three new fields are not in the tuple. `validate()` requires only `["fight_id","class_id","scenario_id","session_id","created_at"]` (`spatial_telemetry.py:92`), not the new fields. So the fields are write-safe and simply unpersisted (identical status to `total_displacement`/`mean_active_proxy_count`). The telemetry writer round-trips unchanged; star-lord seam untouched. MIGRATION v1.77 records this accurately.
- **No gate regression / additive-only — REPRODUCED.** `total_damage_dealt += total` (`spatial_engine.py:1162`) is unchanged in value and semantics; the new `delivered` accumulator is parallel. No existing consumer shifts.
- **Smoke (Discipline #2) — present.** The harness `--smoke` path (`clean_boss_numbers_harness_2026_06_19.py:479-501,581-583`) runs 1 kit × both boss shells × 1 cohort with tiny n_fights to prove tier_2 fires; plus a V1 self-consistency "fail loud" assertion (`:168`). The full re-run reports `v1_all_cells_pass: true`.

## Are the STR numbers trustworthy to rule a design disposition on?

**Yes.** The re-run (`clean-boss-numbers-harness-2026-06-19.json`) metadata: `n_cells:1056`, `n_fights_per_cell:20` (21,120 fights), `smoke:false`, `measurement_only:true`, `production_gate_modified:false`, `v1_all_cells_pass:true`, single seed namespace (`seed_base:619000`, no parallel same-seed runs per Discipline #3), enrage caps confirm `boss_index:0`/`mini_boss_index:0` and `max_duration_s:240`. The claimed STR aggregates reproduce exactly:
- `str|boss_with_adds`: `boss_HP_removed` median **0.3607** (claimed 0.361), DPS median 1309, timeout 1.0.
- `str|mini_boss`: `boss_HP_removed` median **0.0485** (claimed 0.049), DPS median 1099, timeout 1.0.
- `str` overall: DPS median **1303.75** (claimed ~1304/s).

The boss-attribution (V5) is doing real work here: STR delivers ~300k total but its boss_HP_removed is far below its DPS×240/boss_max_hp would imply — most damage sinks into the ADDS (the harness duplicates one representative mob across all 3 spawn slots, so total-damage-only would have masked the boss shortfall). The mini-boss 0.049 is the out-healed signal (DPS cannot offset regen). The numbers are non-circular (unlike the 0.25 KPM, which is circular with timeout=1.000 on a single-boss shell) and are a sound basis for the slow-but-real-vs-degenerate ruling. **The disposition RULING is gandalf's per brief §6 — this finding blesses the numbers, not the verdict.** (For the record, descriptively: the numbers lean toward degenerate/structural rather than clean slow-but-real, since even on boss_with_adds STR removes only ~36% of one health-bar over the full enrage window.)

## Rationale

The build satisfies all five verify-gates (brief §4) and all five endorse criteria (brief §5): single-regime, V1–V5 confirmed-from-code, DPS recorded-not-gated with no gate regression, STR classification answerable, n-per-cell (20) matches the boss-harness cell size. It is a Discipline #12 schema ADDITION (new measure deliberately distinct from `total_damage_dealt`; `boss_HP_removed`>1.0 self-heal framed) — declared in the decisions-log per the brief §6 hand-back. The V4 anti-homogenization constraint (Matt #8) is the load-bearing one and is confirmed both in code (no gate reads the fields) and empirically (832 high-HP-removed cells still BLOCK). Per ADR-002 this is a cross-seam-adjacent schema change to a shared telemetry dataclass, so the semantic-shift declaration is the appropriate gate artifact; no Matt escalation is required because it is purely additive, no existing consumer shifts, and no star-lord DB schema changes.

## INFO (non-blocking)

- **Math-note path imprecision.** The math note cites `simulation/spatial_engine.py`, `simulation/spatial_resolver_adapter.py`, `simulation/proxy_population.py`, etc., but the real paths are under the `spatial_gauntlet/` subdirectory (e.g., `simulation/spatial_gauntlet/spatial_engine.py`). Every cited line number resolves correctly within the subdir file, so this is cosmetic — but a future reader running the citations from the stated path will hit "file not found". Recommend gamora correct the subdir in the math note on next touch (documentation-only; jack-ryan can APPROVE that edit directly per ADR-002). No code impact; does not affect the verdict.

## Action

- [x] jack-ryan: V1–V5 + no-double-count + no-gate-regression + no-star-lord-MIGRATION + STR numbers all reproduced on disk — PASS-WITH-INFO.
- [x] jack-ryan: semantic-shift declaration written to `reincarnated-engine/design/decisions/decisions-log.md` (2026-06-19 entry).
- [ ] gamora (INFO, non-blocking, next-touch): correct the `spatial_gauntlet/` subdir in the math-note line citations.
- [ ] gandalf: consume the re-run → rule the STR slow-but-real-vs-degenerate disposition (brief §6; numbers blessed as trustworthy by this finding).
- [ ] Matt: push is Matt-gated (ADR-006) — engine `26a6f27` (tag `gamora/v-dps-instrument-1`) + collab re-run `a9a68f1` carried in the push gate.

## References

- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py` (damage path `1064-1172`; boss-focus `1318-1331`; self-heal `1662`; result-assembly `1903-1915`; accumulator defs `489-500`)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/spatial_resolver_adapter.py:271-303` (post-mitigation float)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/proxy_population.py:32,74` (proxies deal zero spatial damage)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/spatial_telemetry.py:92,293-295` (validate() + new field defs)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/arena.py:472-524,713-767` (boss shells, suppress_leash_hp_reset, boss_index/mini_boss_index)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/t4_sim_cycling.py:203-267,714-840,1105-1111` (gate properties, compound gate, FightSummary fill)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/damage_resolver.py:282-576` (single consolidated total_damage return — DoT folded)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/telemetry/spatial_recorder.py:127-173` (positional _INSERT_SQL — no reflection)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/clean_boss_numbers_harness_2026_06_19.py:146-163,466-501,581-583` (DPS/boss_HP_removed report + smoke path)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/math/dps-measurement-instrumentation-2026-06-19.md` (gamora math note)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` (v1.77)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/cycle-14-wave-5-season-001/clean-boss-numbers-harness-2026-06-19.json` (re-run; STR aggregates verified)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/requests/2026-06-19-dps-measurement-build-brief.md` (brief §4 verify-gates, §5 endorse, §6 hand-back)
