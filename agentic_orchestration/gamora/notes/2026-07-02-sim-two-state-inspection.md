# Simulation two-state inspection — demo (One Realm) vs launch (full Godot game)

**Author:** gamora (simulation seam). **Mode:** READ-ONLY SURVEY — no production code / config touched.
**Commissioned:** Matt 2026-07-02 (full sim inspection against two target states).
**Targets read:** `canonical/reap-die-rise-game/one-realm-mvp-scope.md` (State 1); `canonical/current-to-end-state/current-to-end-state-engine.md` PART II/III/IV (State 2); W3 PARK stamp `agentic_orchestration/gandalf/notes/2026-06-21-encounter-model-firm-up-disposition.md`; decisions-log recent entries; proxy math-note series; `simulation/AGENT_STATE.md` (SESSION 41/42).
**Discipline:** survey-mode — reports what IS with file:line cites; "wrong / missing" kept in explicit verdict columns. No `should` interleaved with descriptive findings.

---

## §0 — TL;DR (the two-state verdict)

1. **State 1 (One Realm demo): the sim can already do the load-bearing thing.** A hand-authored summoner (proxy) kit CAN run end-to-end in the spatial gauntlet TODAY: spawn → position → navigate → deal realized damage → take damage → die → graded fight result. Proxy-combat W1 (allegiance+spawn, `gamora/v-proxy-W1-allegiance-spawn-1` @ `ffea0b4`) + W2 (realized damage+targetability+death, `gamora/v-proxy-W2-realized-damage-1` @ `a84a395`) landed 2026-06-22. Demonstrated: W2 spike, army WR 1.000 vs caster-alone 0.000 on a 60k `boss_with_adds`, 60000.0 realized ally damage, boss_final_hp 0.0 (AGENT_STATE SESSION 41).
2. **The demo-summoner-certification gap is NARROW and is a CALIBRATION + GRADING-CRITERION gap, not a mechanism gap.** The W2 realized-fight magnitudes (`damage_multiplier`/`base_hp`/`proxy_max_active`/`attack_interval_s`) are UNCALIBRATED scaffold (all in rocket's `proxy_vocabulary_bridge.py`, marked "SCAFFOLD — gamora calibrates"). A stable GRADED WR band for a proxy kit was explicitly deferred to W3 (knife-edge under the no-death-risk boss model) and W3 is PARKED (Matt 2026-06-30) behind a Godot combat-loop spike. The proxy_commander Set-#6 CONTRIBUTION-selector constants ARE calibrated (`proxy_commander.py`, S_BASELINE=0.35) — a different magnitude set from the fight constants.
3. **Beyond summoner, the demo's load-bearing sim capabilities are LIVE**: the boss-gate (survive-and-kill) three-gate G1 engine-truth grading + the typed-resistance defensive axis (kit-viability floor) are both in production code.
4. **State 2 (launch): the big poles are unbuilt** — kit-vs-kit matchup matrix (III.1), summoner sim-CERTIFICATION un-gate (III.1b: `_DEFERRED_PROXY_BINS` still gated + `proxies:[]` on all real kits), per-level sawtooth harness (III.2), horde density ≥50 (III.3), T4 sim-extension set (III.10).
5. **One confirmed tracker staleness (over-claim), plus several under-claims** — see §4. Tracker III.1b line "The sim cannot create, position, or resolve a player-summoned proxy that deals spatial damage / takes aggro" is FALSIFIED by W1+W2.

---

## §1 — Module inventory (`src/reincarnated/simulation/`)

Status legend: **PROD-LIVE** = on a production path; **FLAG** = flag-gated (default noted §2); **INSTRUMENT** = calibration/measurement harness driven by dispatches; **HARNESS(dated)** = point-in-time instrument; **HISTORICAL** = superseded-but-resident (git is archive).

| Module | What it is | Verdict (live / instrument / historical) |
|---|---|---|
| `balance_loop.py` (168 KB) | The B14.5 V1 primary balance loop: generation→sim→adjust until WR-in-band; recompose-first (4 levers before modifier search). Trial-gallery path RETIRED (`:2881` `NotImplementedError`, 1D-deletion). | **PROD-LIVE** (convergence critical path). Trial-gallery sub-path historical-loud. |
| `gauntlet_sim.py` (122 KB) | Cycle-13 W5G gauntlet execution; the ship gate `eligible_encounters_passed` (:615); boss-shell survive-and-kill branch (:646, `_BOSS_SHELL_GATE_TYPES` :183); clear-shell KPM band. | **PROD-LIVE** (the production ship gate). |
| `combatant.py` (63 KB) | Mutable per-combatant state; `from_player_class`/`from_monster`; typed-resistance STEP-ZERO bridge (:602); `MITIGATION_SYMMETRY` + `apply_max_profile_investment` flags. | **PROD-LIVE**. |
| `damage_resolver.py` (60 KB) | Skill→effect application; 7×7 typed resolution; DoT refresh (max-tick); physical-DoT scaling. Two deferred TODOs (§2). | **PROD-LIVE**. |
| `ai_strategies.py` (27 KB) | Kernel AI action-selection (`_common`/`_scripted` build-vs-spend); ported into spatial rotation (Phase-2). | **PROD-LIVE** (source of the ported rotation intent). |
| `bc_measurement.py` (22 KB) | Reduces per-fight telemetry → per-kit Axis-4/Axis-3B scalars + bin assignment. | **PROD-LIVE**. |
| `effect_resolver.py` (4 KB) | Ticks active effects (DoT/HoT/buff/expiry). | **PROD-LIVE**. |
| `trigger_handler.py` (1.3 KB) | on_hit/on_kill/on_threshold trigger chains, depth-capped 3. | **PROD-LIVE**. |
| `resistance_matrix.py` (8.5 KB) | 7×7 resistance matrix (Phase-1 P1 D7). | **PROD-LIVE** (matrix source). |
| `t4_sim_cycling.py` (83 KB) | Cycle-13 W4G T4 sim cycling; DPS/TTK record sites (:1135); spatial re-point. | **PROD-LIVE** (T4 KPM sweep). |
| `fight_result.py` / `verdict_types.py` / `validation_report.py` | Result dataclasses; the type-wall (`CommitGradeVerdict`, the 1D-deletion SURVIVOR); human-readable report. `SearchGradeEstimate` = inert tombstone. | **PROD-LIVE** (wall) + tombstone. |
| `phase7_bridge.py` / `phase7_cohort.py` / `phase7_db.py` / `phase7_verdict.py` | Phase-7 pipeline: kit_archive→gauntlet bridge, 5-cohort classifier, DB schema, HELD-verdict state machine. | **PROD-LIVE** (season pipeline stages; consumed by `wave5_season_orchestrator`). |
| `wave5_season_orchestrator.py` (147 KB) | Cycle-14 W5 season-001 full Phase-2→7 orchestrator. | **PROD-LIVE** (season production driver). |
| `bounded_viability_validation.py` (73 KB) | W-α4 bounded-viability harness; DPS ≤1.5× cross-path variance check (:431, MEASURE-not-GATE). | **INSTRUMENT** (validation harness). |
| `sc7_calibration_loop.py` (69 KB) | SC-7 BASE_SPELL_DAMAGE_L50 calibration loop. | **INSTRUMENT** (calibration). |
| `unified_calibration_loop.py` (213 KB) | W-α3 unified calibration pass; one TODO (element_conversion_factor). | **INSTRUMENT** (calibration). |
| `anchor_read2_focusfire_harness_2026_06_21.py` | Mixed-pack focus-fire (A)-vs-(B) read, T1.4 Deliverable 3, post-anchor-rescale. | **HARNESS(dated)**. |
| `anchor_rescale_crosscontam_harness_2026_06_21.py` | Cross-contamination HALT-determinant re-run of banked boss-shell instrument. | **HARNESS(dated)**. |
| `armor_resist_symmetry_phase4_harness_2026_06_20.py` | Phase-4 armor/resist-symmetry measure-isolated (drives Path B). | **HARNESS(dated)**. |
| `boss_gate_verification_2026_06_20.py` | Drives the WIRED boss-gate; confirms survive-and-kill counts + no clear-shell regression. | **HARNESS(dated)**. |
| `clean_boss_numbers_harness_2026_06_19.py` | Clean boss-numbers measurement. | **HARNESS(dated)**. |
| `clear_shell_domain_guard_reband_harness_2026_06_21.py` | Clear-shell domain-guard + re-band, T1.3 Deliverable A. | **HARNESS(dated)**. |
| `dot_activation_phase3_harness_2026_06_20.py` | Phase-3 DoT-activation measure-isolated. | **HARNESS(dated)**. |
| `dot_mitigation_symmetry_armb_harness_2026_06_20.py` / `_armc_...` | DoT/ailment mitigation-symmetry Arm-B / Arm-C. | **HARNESS(dated)**. |
| `g3b_rearm_distinguishability_harness_2026_06_20.py` | G3b cross-economy distinguishability + rage build-spend rhythm. | **HARNESS(dated)**. |
| `miniboss_remeasure_corrected_hp_harness_2026_06_21.py` | mini_boss re-measure at corrected gen HP, T1.3 Deliverable B. | **HARNESS(dated)**. |
| `miniboss_smaller_boss_remeasure_2026_06_20.py` | mini_boss "smaller boss" fix re-measure. | **HARNESS(dated)**. |
| `rotation_selector_phase2_harness_2026_06_20.py` | Phase-2 rotation-selector measure-isolated. | **HARNESS(dated)**. |
| `str_9pass_floor_all18_harness_2026_06_19.py` | STR 9-pass-floor all-18 clear-room measurement. | **HARNESS(dated)**. |

### `spatial_gauntlet/` sub-package

| Module | What it is | Verdict |
|---|---|---|
| `spatial_engine.py` (177 KB) | **THE sole battle sim.** SpatialEntity, SpatialFightEngine, `run_spatial_fight`; navigator (`_navigate_entity` :991, allegiance-total); the W1/W2 proxy-combat path (`_build_positioned_allies` :1791, `_spawn_one_ally` :1730, ally realized-fight phase :2321-2399, mob attack-target generalization :2173-2204); typed-resistance death channel (:2235 `resolve_spatial_hit`); telegraph mint (`_mint_telegraph_spec`). | **PROD-LIVE** (proxy path flag/empty-gated inert in solo). |
| `arena.py` (39 KB) | 6 arena shells (open_arena/chokepoint/boss_with_adds/magic_pack/elite_pack/mini_boss), all cap ≤8 concurrent; M1 gather-primitive constants. | **PROD-LIVE**. |
| `spatial_resolver_adapter.py` (15 KB) | Commit-grade spatial damage via kernel resolver (`resolve_spatial_hit`). | **PROD-LIVE**. |
| `spatial_telemetry.py` (26 KB) | SpatialFightResult schema + writer; `mean_active_proxy_count`, `mean_proxy_contribution_pct`, `player_death_element`, boss MEASURE fields. | **PROD-LIVE** (star-lord consumes; §MIGRATION). |
| `spatial_bc_measurement.py` (25 KB) | Commit-grade 8-axis BC reduction from spatial telemetry (W-D); `measure_axis2a_proxy`. | **PROD-LIVE**. |
| `proxy_population.py` (15 KB) | Proxy population model (`ProxyCombatant`, `entity_from_proxy_dict` :259) — the Axis-2A COUNT instrument (positionless, lifetime-attrition). | **PROD-LIVE** (COUNT instrument; distinct from W1/W2 realized path). |
| `proxy_commander.py` (11 KB) | Set-#6 CONTRIBUTION-selector sim half; the calibrated balance constants (S_BASELINE 0.35, C_2PC 0.15, G_POWER 0.25, G_DUR 0.30, DELTA_COUNT 1). | **PROD-LIVE** (CONTRIBUTION selector; NOT the realized-fight magnitudes). |
| `reduced_spatial_substrate.py` (8 KB) | Reduced-spatial inner-loop SEARCH substrate (M1.3.5). | **INSTRUMENT** (search-loop substrate). |
| `gauntlet_modes.py` (35 KB) / `gauntlet_archive.py` (22 KB) | Convergence-vs-validation usage-mode routing; in-memory QD archive + query. | **PROD-LIVE**. |
| `phase4_*.py` (8 files: cell_context/db/mg1_pareto/mg2_crowding/mg3_mahalanobis/mg4_kl/mg5_eviction/pipeline) | Phase-4 QD multi-gate eviction pipeline (Pareto/crowding/Mahalanobis/KL/eviction). | **PROD-LIVE** (QD archive maintenance) — May-dated, not "dated harness". |
| `golden_master/` | Pinned regression oracle (seed 770_011). | **PROD-LIVE** (regression pin). |

---

## §2 — Flags / gates / scaffolds / deferrals

| Name | Site (file:line) | Default / value | Meaning | Demo-relevant? | Launch-relevant? |
|---|---|---|---|---|---|
| `track_proxy_population` | `spatial_engine.py:1581` (class), `:2964` (runner) | **True** (FLIP #2, 2026-06-18) | Builds proxy COUNT population, emits `mean_active_proxy_count` (Axis-2A). COUNT-only, mobs/min inert. | Indirect (Axis-2A bin) | Yes (III.1b measurement) |
| `apply_max_profile_investment` | `combatant.py:527` | **True** (FLIP #3, 2026-06-18) | "kit power" = FAITHFUL geared, not keystone-stripped ablation floor. | Yes (grading geared kits) | Yes |
| `MITIGATION_SYMMETRY` | `combatant.py` (module flag) | **True** (Phase-4) | Floors production-Monster per-element resist to armor-symmetric `r_sym`; symmetrizes off-element caster mitigation. OFF = byte-identical raw rolls. | Yes | Yes |
| `WIRE_RESOURCE_ECONOMY` | `combatant.py` (module flag) | **True** (Phase-1) | Wires doc-48 resource economies into the spatial rotation. | Yes | Yes |
| `ROTATION_SELECTOR_V2` | `spatial_engine.py` (module flag) | **True** (Phase-2) | energy_type-branched build-vs-spend rotation (breaks T1-collapse). OFF = shortest-cd legacy. | Yes | Yes |
| F1 geometry-honest resolver path | (RATIFIED flip #1, 2026-06-18) | LIVE | Spatial commit-grade damage via kernel resolver = shipped measurement basis. | Yes | Yes |
| `_positioned_allies` realized gate | `spatial_engine.py:2328` | gated on non-empty `_positioned_allies` (W1 `proxy_decls` set) | The W1/W2 realized proxy-fight phase; inert in solo (`proxy_decls=[]`). Decoupled from `track_proxy_population` (G-CONSTRAINT). | **Yes (the summon verb)** | Yes |
| `_is_fighting_decl` | `spatial_engine.py:103` | pure fn | A decl is a fighting ally iff `damage_multiplier > 0`; else backline/support (nav-only, no damage). | Yes | Yes |
| Boss-shell survive-and-kill gate | `gauntlet_sim.py:646`, `_BOSS_SHELL_GATE_TYPES:183` | LIVE | Boss shells pass iff `tier_2_survival_rate >= SURVIVAL_FLOOR_BY_COHORT[cohort]` within 240s enrage; KPM band never consulted. | **Yes (G1 boss grading)** | Yes |
| `player_death_element` (typed death) | `spatial_engine.py:1693`, set :2271 | LIVE | Typed per-element death-cause via `resolve_spatial_hit` on the killing blow (kit's real elemental_resistances mediate). | Yes (kit-viability floor) | Yes |
| Boss `damage_multiplier` anchor | (G-C close, decisions-log 2026-06-21) | **5.0 @ cadence 4.5s LOCKED** | Defensive-axis calibration anchor; NOT pushed to 6.0 (PoE tax). 0.926 unmatched softness = named watch-item. | Yes | Yes |
| Swarm `damage_multiplier` anchor | (G-C close) | **0.20 LOCKED** | Trash<boss guard (re-derived down 0.85→0.20). | Yes | Yes |
| **W2 realized-fight magnitudes** — `damage_multiplier` | `proxy_vocabulary_bridge.py:232` (rocket seam) | **1.0 SCAFFOLD** ("gamora-calibrated" = UNCALIBRATED) | Per-hit basis (flat `× 500 × damage_modifier`). | **Yes — the demo-summoner cert gap** | Yes |
| `PROXY_REFERENCE_HP` | `proxy_vocabulary_bridge.py:68` (rocket) | **20 000.0 SCAFFOLD** | Base for proxy `base_hp = REFERENCE_HP × tier hp_factor`. | **Yes** | Yes |
| `PROXY_TIER_MAX_ACTIVE` | `proxy_vocabulary_bridge.py:77` (rocket) | **fixed-per-tier SCAFFOLD** | The `proxy_max_active` count wall (the boss-grading lever, spec §5/§7.4). Beast-Taming override=1. | **Yes** | Yes |
| `DEFAULT_ATTACK_INTERVAL_S` | `proxy_vocabulary_bridge.py:255` (rocket) | **SCAFFOLD** ("gamora-calibrated") | Ally attack cadence. | **Yes** | Yes |
| `_DEFERRED_PROXY_BINS` | `bc_target_composer.py:97,318` (rocket seam) | `{proxy-light, proxy-heavy}` still gated | Content-emission gate: no proxy kit is emitted into a roster; every real kit `proxies:[]`. | **No (demo = hand-authored decls, §5.2)** | **Yes (III.1b un-gate)** |
| Set-#6 CONTRIBUTION constants | `proxy_commander.py:59-70` | **CALIBRATED** (S_BASELINE 0.35 from slice smoke; C_2PC 0.15; G_POWER 0.25; G_DUR 0.30; DELTA_COUNT 1) | Set-#6 selector/band-parity magnitudes (a DIFFERENT set from the realized-fight scaffold above). | Low (contribution selector) | Yes |
| Trial-gallery balance | `balance_loop.py:2881` | `NotImplementedError` (fail-loud) | 1D trial-gallery diagnostic RETIRED with 1D deletion; spatial port = forward-work. | No | Maybe (trial room) |
| `dual_element_factor` TODO | `damage_resolver.py:877` | `1.0` (TODO: read from T4 DUAL_ELEMENT_ADDITION) | T4 dual-element context not wired. | No | Yes (T4) |
| `element_conversion_factor` TODO | `unified_calibration_loop.py:3065` | `1.0` (TODO) | Element-conversion Variant-C ailment (decisions-log AWAITING). | No | Maybe |
| `REDUCED_TICK_SIZE` | `spatial_engine.py` (exported) | 0.5s (vs TICK_SIZE 0.1s) | Perf mitigation; A3 stability ≤±0.05 WR delta required before production reduced-tick. | No | Yes (throughput III.4) |
| Smoke-tier mode | `spatial_gauntlet/__init__` (SmokeTierConfig) | opt-in | ~5 classes / 30 fights iteration mode (Discipline #2). | Instrument | Instrument |

Note: no `_DEFERRED_*` NAMED constant lives inside `simulation/` — the proxy-bin deferral lives in rocket's `bc_target_composer.py`; the sim consumes its effect (`proxies:[]`). The only sim-side `NotImplementedError` is the retired trial-gallery.

---

## §3 — The five questions

### Q1. Can the spatial gauntlet TODAY run a hand-authored proxy (summoner) kit end-to-end?

**YES — the full spawn → position → navigate → deal realized damage → take damage → die → graded fight result path is live in `spatial_engine.py`.** The exact code path:

- **Spawn + position:** `_build_positioned_allies()` (`:1791`) → `_spawn_one_ally(decl, ...)` (`:1730`) builds each ally from the `proxy_decls` dict on an owner-relative summon ring, `allegiance="ally"` (`:1780`), combat-equipped from the decl (`base_hp`/`damage_multiplier`/`range_m`/`geometry`/`attack_interval_s`). Entered into `all_entities` (`:1873 = [player] + mobs + _positioned_allies`).
- **The decl reader:** `proxy_population.entity_from_proxy_dict(d, ...)` (`proxy_population.py:259`) is the canonical `proxies`-dict consumer (COUNT instrument); the realized path consumes the SAME decl keys via `_spawn_one_ally`.
- **Navigate:** the module-level `_navigate_entity` (`:991`) is allegiance-total (W1 parameter rename `player`→`nav_target`); mobs re-path to allegiance-filtered nearest enemy at the single call site; allies navigate the same function.
- **Realized damage OUT:** ally attack phase (`:2321-2399`) — each alive damage-dealer ally fires on `proxy_attack_interval_s` cadence at its allegiance-filtered nearest enemy (boss-focus parity, `:2350`) through the target-agnostic `_compute_aoe_hits` + `_apply_skill_damage` → `mob.hp` decrements. Re-summon loop maintains up to `proxy_max_active` (`:2367-2399`).
- **Damage IN + death:** the mob attack-target generalized from `[self.player]` to allegiance-filtered nearest enemy (`:2173-2204`); an ally hit routes through the same `_apply_skill_damage` → `ally.hp` decrements → death via the existing `hp<=0 → is_alive=False` flip (no parallel proxy-death branch).
- **Graded fight result:** the army's realized output lands on the SAME boss HP the player's does → the SAME `boss_killed`/`mini_boss_killed` gate resolves the win → the boss-gate survive-and-kill grade (`gauntlet_sim.py:646`) applies with no special-cased proxy gate.

**What demonstrated it:** the W2 spike `scripts/gamora_proxy_w2_realized_damage_SPIKE_THROWAWAY.py` (throwaway, NOT committed to `simulation/output/`; results recorded in AGENT_STATE SESSION 41 + math note `proxy-combat-w2-realized-damage-2026-06-22.md` §6/§9). Result: on a 60k `boss_with_adds`, injected fighting `proxy_decls` — **army WR 1.000 vs caster-alone 0.000**, one-fight `proxy_realized_damage_dealt(delivered)=60000.0`, `boss_final_hp=0.0` (army LOAD-BEARING: boss dies to ally hits where the caster alone times out). Targetable-die proven: ally(base_hp=200) took realized mob damage and died. G-SOLO byte-identical re-proven exact vs pre-W2 HEAD `ffea0b4` across all 6 nav branches + the mob attack path. **Caveat (math note §6.1, §0):** this is a "load-bearing fighting contribution" acceptance on an INJECTED FIXTURE — NOT a stable graded WR band, and NOT via a lifted `_DEFERRED_PROXY_BINS` (no kit emitted). The magnitudes were consumed as scaffold.

### Q2. What EXACTLY remains for demo summoner certification?

To run 2-3 hand-authored summoner kits through the sim and grade them credibly, three concrete items remain — all CALIBRATION / GRADING-CRITERION, none a mechanism build:

**(a) The realized-fight magnitudes are UNCALIBRATED scaffold.** The `proxy_vocabulary_bridge.py` set — `damage_multiplier` (`:232`, None→1.0), `base_hp`/`PROXY_REFERENCE_HP` (`:68`, 20000 × tier hp_factor), `proxy_max_active`/`PROXY_TIER_MAX_ACTIVE` (`:77`), `DEFAULT_ATTACK_INTERVAL_S` (`:255`) — are all tagged "SCAFFOLD — gamora calibrates (do-not-self-adjust)". These are the FIGHT constants (W2 consumed them as-is; math note §0/§9). **Distinct from** the proxy_commander Set-#6 CONTRIBUTION constants (`proxy_commander.py:59-70`), which ARE calibrated (S_BASELINE=0.35 derived from the Wave-A2 slice smoke) — but those calibrate the CLASSIFICATION/band-parity selector, not the realized fight. So: the CONTRIBUTION-selector magnitudes are calibrated; the realized-fight magnitudes are scaffold. `proxy_max_active` is the load-bearing one — spec §5/§7.4 makes it the count wall = the boss-grading lever (max army boss-DPS = `proxy_max_active × per_proxy_realized_dps`).

**(b) The GRADING CRITERION for a proxy kit is not established.** W2 math note §0/§6.1 states W2 "does NOT chase a stable graded WR band — the spike showed that is a knife-edge with the current no-death-risk boss model," and deferred the stable-band shape to W3. The spec (`spatial-proxy-combat-spec-2026-06-21.md` §322-329) names W3 = "calibrate `proxy_hp`/cadence/`proxy_max_active`/`s_baseline` so a proxy kit lands at parity-band efficacy with neither failure mode (D3-evaporate / D2-dominance), against `boss_with_adds` + `mini_boss`" and requires "does the army kill the boss gradedly BEFORE any production Wave 2 is authorized."

**Is the knife-edge caveat still true after the typed-resistance defensive-axis close?** The typed-resistance G-C close (decisions-log 2026-06-21) locked the boss anchor (dm=5.0 @ 4.5s, swarm 0.20) for the PLAYER-vs-boss defensive axis — but it was a build-floor close, and the W3 PARK (Matt 2026-06-30, `2026-06-21-encounter-model-firm-up-disposition.md`) explicitly ruled the boss is **build-primary FLOOR + dodge-skill CEILING**, with the dodge ceiling deferred behind a Godot combat loop. The "no-death-risk boss model" the W2 caveat names is precisely the state the PARK froze: dodge is inert in the sim by design, so the only live defensive answers are build (resist/tank/out-range). The PARK unstuck the proxy §4 encounter-model question DESIGN-ONLY and authorized "no proxy build, no `_DEFERRED_PROXY_BINS` lift." So: the encounter-model SHAPE is now ratified (one model answers both the solo firm-up and the proxy §4 grading), but the graded-band CALIBRATION for a proxy kit is still open and is gated (per the PARK) behind the Godot combat-loop spike (named dispatch 4 + dispatch 5). For a DEMO that hand-tunes by playtest (§5.3), a full graded-band certification is not the demo's bar — but a credible sim GRADE of a hand-authored kit needs at minimum a WR/survive-and-kill read against calibrated (not scaffold) magnitudes on `boss_with_adds`+`mini_boss`.

**(c) What a bounded calibration slice would touch (gamora-work terms, NOT calendar):**
- Files: math-note-first (`simulation/math/<proxy-fight-calibration>.md`, Discipline #1); the calibration would SET rocket's scaffold magnitudes (cross-seam — `proxy_vocabulary_bridge.py` is rocket's file; the un-scaffolding is rocket's edit on gamora's calibrated values, mirroring the proxy_commander pattern where gamora owns the constant and rocket's emit guards it). No new production sim code (the fight mechanism is complete).
- Harness: 1 dated calibration harness (`gamora_proxy_fight_calibration_<date>.py`) sweeping `proxy_max_active` × `damage_multiplier` × `base_hp` × `attack_interval_s` on injected fixtures against `boss_with_adds` + `mini_boss`, seeking the graded band (neither D3-evaporate auto-fail nor D2-dominance faceroll). Smoke-tier first (Discipline #2); the W2 resource-bound projection was <5s wall for the load-bearing proof, so a magnitude sweep is a bounded multiple, well under the 104k-fight budget.
- Runs: smoke iteration (~5 fixtures × grid), then one `--full` validation pass at the chosen magnitudes. NO full season regen (proxy path is byte-identical in solo; no production-population regen needed until `_DEFERRED_PROXY_BINS` is lifted — which is launch-track, §5.2).
- Gating dependency: per the W3 PARK, the graded-band *ceiling* texture (dodge) is deferred behind Godot combat. The demo can proceed on the BUILD-FLOOR grade alone (resist/tank/out-range), which is the live axis.

### Q3. What does the demo need from the sim beyond the summoner question?

The demo hand-tunes Goldilocks/sawtooth/density (§5.3), so those three sim CERTIFICATION instruments (III.1/III.2/III.3) are NOT demo-load-bearing. What IS load-bearing for demo certification, and its state:

- **Three-gate G1 engine-truth floor grading — LIVE.** The demo authors floors via the three-gate method (§6.3); G1 = engine-truth. The boss-shell survive-and-kill gate (`gauntlet_sim.py:646`, `_BOSS_SHELL_GATE_TYPES`) + the clear-shell KPM band (`ENCOUNTER_COHORT_KPM_BAND`, W-α6) are both in production code. A curated lieutenant/champion kit can be run and graded (survive-and-kill within enrage for boss shells; mobs/min-in-band for clear shells).
- **Kit-viability floor (typed-resistance defensive axis) — LIVE.** The typed-resistance resolver route (`spatial_engine.py:2235` `resolve_spatial_hit` on the death channel) + `player_death_element` (:2271) are live; the boss anchor (dm=5.0/swarm 0.20) is the locked calibration target. A hand-curated kit's defensive floor (does the right form survive) is measurable.
- **Faithful-geared kit power — LIVE** (`apply_max_profile_investment=True`), so a curated kit is graded as a geared unit (matches the demo shipping gear as bundle content, §5.1).
- **The 6 arena shells + element rotation — LIVE** (`arena.py`; per-floor element rotation validated). The demo's per-floor element rotation (§4) is engine-supported.

Not load-bearing for the demo (curated, not certified): matchup-matrix temperature (III.1 — demo Goldilocks is hand-picked), per-level sawtooth harness (III.2 — hand-tuned by playtest), `SCENARIO_OVERRUN` density (III.3 — the demo's density need is Godot RENDERING at min-spec).

### Q4. State 2 (launch): per-capability gap table vs tracker PART III

| Capability (tracker item) | What the sim does today (cited) | Verdict: built / partial / unbuilt |
|---|---|---|
| **III.1 kit-vs-kit matchup matrix** (Goldilocks temperature) | Only global kit-vs-control validation. No kit-vs-kit path (`spatial_engine.py:2944` single fight-entry; mirror-duel retired). The ~24×24 QD-grouping matrix is un-measured. | **UNBUILT** (a hypothesis-test over finished kits, not asserted; joint gamora+star-lord scoping). |
| **III.1b summoner sim-CERTIFICATION un-gate** | Realized proxy COMBAT is BUILT (W1+W2, §Q1). `_DEFERRED_PROXY_BINS` still gated (`bc_target_composer.py:318`, rocket); `check_infeasibility` still returns `is_deferred=True`; every real kit `proxies:[]` (`proxy_vocabulary_bridge.py:22-23`); 25% emission NOT triggered; realized-fight magnitudes scaffold (§Q2). | **PARTIAL — mechanism BUILT, certification-emit UNBUILT.** The combat path exists; lifting the bin + calibrating the fight magnitudes + grading emitted proxy kits remains. (This is the confirmed tracker staleness — §4.) |
| **support-role un-gate** (rides III.1b) | Mechanics exist (`_ROLE_DEF_BASE["support"]="mitigator"`, aura geometry valid, econ/level/weight tables). Backline/support allies (`base_hp==0`, no damage) already enter `_positioned_allies` for W1 nav (`_is_fighting_decl` false → non-attacking). `_DEFERRED` support bin still gated (rocket). | **PARTIAL** — the multi-actor ally context now EXISTS (proxies provide ally targets); the bin un-gate is rocket's. |
| **III.2 per-level sawtooth harness** | Validates at single fixed L50 endgame; flat-skill assumption (`balance_loop.py:1935`). L17/L33/L50 are monster-difficulty bands, not kit levels. | **UNBUILT** (checkpoint-validation harness across ~4-6 milestones; Q2-persistence-gated per tracker). |
| **III.3 `SCENARIO_OVERRUN` density** (≥50) | Max 8 concurrent ever (`arena.py` 6 shells; MobSpec max 8; `mean_mobs_killed` 8.0). No horde/gather primitive at density (M1 gather-primitive constants exist for ≤8). Defensive axis calibrated at ≤8. | **UNBUILT** (7th scenario + M1 horde-positioning primitive + band re-fit). |
| **multi-actor / kit-vs-kit foundation** | Single fight-entry (one player class vs mob list). W1/W2 added ally allegiance but NOT a second player-KIT slot. | **PARTIAL** — allegiance-heterogeneous world exists; a second-kit combatant slot does not. |
| **T4 sim-extension set** (ResourceBuffer / MechanicReplacement / ZoneControl / ConditionalModifier / ProxySpawn) | `ProxySpawn` un-defers on the same proxy dependency (`mechanic_alteration.py:46`, rocket). T4 modifier algorithm sim-extension-deferred (`bounded_viability_validation.py:1477`; decisions-log AWAITING). `dual_element_factor` TODO (`damage_resolver.py:877`). | **UNBUILT** (T4 affix/mechanic-alteration; decisions-log "measured-for-record, Cycle 16+"; non-blocking per Matt). |

### Q5. Tracker corrections — see §4.

---

## §4 — Tracker corrections (engine tracker sim claims vs code truth)

| Direction | Tracker line (quoted) | Code truth (cited) |
|---|---|---|
| **OVER-CLAIM (confirmed stale)** | III.1b: "The sim cannot create, position, or resolve a player-summoned proxy that deals spatial damage / takes aggro." (line 315) | FALSIFIED by W1+W2 (2026-06-22). The sim DOES create (`_build_positioned_allies` :1791 / `_spawn_one_ally` :1730), position (owner-ring, `allegiance="ally"` :1780), navigate (allegiance-total `_navigate_entity` :991), deal realized damage (`:2321-2399` → `mob.hp` via `_apply_skill_damage`), take aggro + damage (mob attack-target generalized :2173-2204 → `ally.hp`), and die (existing `hp<=0` flip). Proven: W2 spike, army WR 1.000, 60000.0 realized damage. |
| **OVER-CLAIM (stale)** | III.1b Disposition table: "proxy/summon bins → FLIP — RATIFIED. Un-gate → III.1b (high)." framed as not-yet-started multi-actor build. | The MULTI-ACTOR SIM + PROXY COMBAT (the "same multi-actor root" the tracker shares between III.1 and III.1b) is BUILT for the player-side proxy case. What remains un-gated is the CONTENT-EMIT (`_DEFERRED_PROXY_BINS` lift) + fight-magnitude calibration — a narrower residual than the table implies. |
| **OVER-CLAIM (stale)** | II.1 kits row: "every kit emits `proxies:[]` — summoner archetype **unbuilt**, not 'deferred'." (line 271) | The `proxies:[]` emit is accurate (rocket seam unchanged), but "summoner archetype unbuilt" is stale for the SIM half — the summoner's spatial COMBAT is built (W1+W2). Precise: the summoner CONTENT-GENERATION + sim-CERTIFICATION-emit are unbuilt; the summoner FIGHT MECHANISM is built. |
| **OVER-CLAIM (partial-stale)** | I.1: "Summoner/proxy archetype is GATED OUT today ... the sim is solo-only (legacy Profile-A), so proxy-creating kits cannot be evaluated." (line 233) | The CONTENT gate (`_DEFERRED_PROXY_BINS`) is still up, so no proxy kit is EMITTED — accurate. But "the sim is solo-only ... cannot be evaluated" is stale: the sim is no longer solo-only (allegiance-heterogeneous `all_entities` :1873); an INJECTED proxy kit CAN be evaluated end-to-end (§Q1). The barrier is emit + calibration, not sim capability. |
| **UNDER-CLAIM (tracker doesn't credit)** | I.1: lists "summoner spatial-combat unbuilt" among carried B-series blockers (line 244). | Summoner spatial-combat is BUILT (W1+W2, `gamora/v-proxy-W1/W2`). This carried-blocker line is discharged for the combat mechanism. |
| **UNDER-CLAIM (tracker doesn't credit)** | III.1b: "support is NOT missing ... deferred ONLY by solo Profile-A ... un-gates on the same multi-actor-sim dependency." | The multi-actor-sim dependency is now SATISFIED on the sim side: backline/support allies already enter the positional set (`_is_fighting_decl` :103 → non-attacking backline). The ally-target context support needs now exists; only the rocket bin un-gate remains. |
| **ACCURATE (confirm, not correct)** | III.1: "No kit-vs-kit path (`spatial_engine.py:2944`; mirror-duel retired)." | Confirmed accurate — W1/W2 added ALLY allegiance, not a second player-KIT slot. Kit-vs-kit remains unbuilt. The proxy work does NOT discharge III.1 (tracker correctly separates them). |
| **ACCURATE (confirm)** | III.10 table: `ProxySpawn` un-defers on the proxy dependency (`mechanic_alteration.py:46`); T4 modifier algorithm sim-extension-deferred; `dodge_gated_deferred` KEEP. | Confirmed — the dodge-ceiling deferral is the correct KEEP (W3 PARK re-affirms it behind Godot combat). |
| **ACCURATE (confirm)** | I.1: boss shells survive-and-kill, DPS derived-not-gating; defensive axis CLOSED (dm=5.0/swarm 0.20). | Confirmed live in code (`gauntlet_sim.py:646`; `bounded_viability_validation.py:431`; decisions-log 2026-06-21). |

---

## §5 — Sign-off

The simulation seam, measured against the two target states:

- **State 1 (One Realm demo):** the sim's demo-load-bearing surface is LIVE. The summoner FIGHT works end-to-end (W1+W2). The demo-summoner-certification residual is a bounded calibration slice (un-scaffold the `proxy_vocabulary_bridge.py` fight magnitudes + establish a build-floor grade), NOT a mechanism build — and the graded-band CEILING (dodge) is correctly parked behind Godot combat per the W3 PARK. The other demo-load-bearing capabilities (three-gate floor grading, kit-viability floor, geared-kit power, element rotation) are in production code.
- **State 2 (launch):** the long poles are the ones the tracker names — kit-vs-kit matrix (III.1), the summoner CONTENT-EMIT un-gate + fight-magnitude calibration (III.1b residual), per-level sawtooth harness (III.2), horde density ≥50 (III.3), T4 sim-extension set (III.10). The multi-actor FOUNDATION the tracker treats as a shared unbuilt root is, for the player-side proxy case, BUILT.
- **Confirmed tracker staleness:** III.1b line 315 over-claims (the sim CAN create/position/resolve a fighting proxy); II.1/I.1 "summoner archetype unbuilt/gated-out" is precise only for content-emit, stale for the fight mechanism; III.1 kit-vs-kit under-claim does NOT exist — that line is accurate. The proxy work is under-credited in the tracker in exactly the places W1/W2 landed after the tracker's PART III was authored.

Survey complete. No production code, config, or telemetry touched.

**Signed:** gamora (simulation seam), 2026-07-02.
