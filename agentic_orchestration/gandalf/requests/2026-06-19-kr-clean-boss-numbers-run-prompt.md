# Run brief — clean current-regime BOSS numbers (survive+kill at faithful power)

**Type:** gandalf-authored measurement-run brief → knight-rider to sequence (gamora harness + jack-ryan Gate-2). Matt-declared 2026-06-19 ("let's run real boss numbers").
**Author:** gandalf
**Depends on:** Gate-1 findings in `agentic_orchestration/gandalf/notes/2026-06-19-encounter-measurement-doctrine-spine.md` (the GATE-1 ADDENDUM + corrected §5/§6).

---

## 0. Why this run exists (the one-paragraph driver)

The encounter-measurement design session needs to settle one empirical question: **at faithful power, on boss shells, which archetypes actually survive-and-kill the boss within the enrage timer — and is the "STR boss-crater" a real failure or an artifact of the KPM gate rejecting STR before survive+kill is ever measured?** The existing `phase3_gauntlet_results.json` cannot answer this: it is regime-mixed (old-scale KPM rows + current-regime metadata), and — more fundamentally — **boss shells are tier_1-KPM-REJECTED, so tier_2 (the survive+kill simulation) never runs on them.** STR's `survival=0.0` in that artifact is a tier_2-never-ran DEFAULT, not a measured death. This run produces the clean boss table that replaces spine §5.

## 1. THE TRAP (do not re-walk it)

A naïve gauntlet re-run reproduces the exact problem. The production path short-circuits tier_2 whenever tier_1 routes REJECT (`t4_sim_cycling.py:1452`), and boss shells REJECT on low KPM at tier_1. **This run MUST run tier_2 on the boss shells unconditionally — bypassing the tier_1 KPM verdict — or it will hand back the same fake 0.0 defaults.** This is a measurement harness, NOT a gate change: it does not touch the production ship gate, it just drives the existing tier_2 sim directly on boss shells so survive+kill is actually observed.

## 2. What to run

- **Shells:** `boss_with_adds` and `mini_boss` ONLY (the two `*_killed` win-condition shells; `arena.py:523` / `:765`).
- **Instrument:** call `w4g2_tier_2_full_sim(...)` (`t4_sim_cycling.py:1199`) directly per kit × boss-shell × cohort. It is standalone — it does NOT require tier_1 to have passed; only the gauntlet caller gates it behind tier_1≠REJECT. Bypassing that caller-gate is the whole harness.
- **Population:** the season-001 faithful-power kit population (the same kits behind §5; max-profile investment — current default post flip-#3 `apply_max_profile_investment` ON). Confirm faithful power is applied (V3).
- **Cohorts:** all four (DPS-min-maxer, Balanced, Defensive, Hybrid).
- **n_fights:** the production tier_2 count (full, not smoke) so survival rates are stable per cell. Match or exceed the §5 per-attribute cell sizes (str/dex/int n≈144, wis n≈360).
- **Seeds:** deterministic, sequential, distinct base from prior harnesses (Discipline #3), recorded.

## 3. What to record (per kit × shell × cohort, then aggregated by attribute + archetype)

| Metric | Source | Why it matters |
|---|---|---|
| **survive+kill rate** | `survival_rate` = fraction with `fr.winner=="player"` | On these shells winner=="player" ⇒ the boss entity died (win_condition `boss_killed`/`mini_boss_killed`). This IS the doctrine's boss gate signal. |
| **termination breakdown** | `termination_reason` counts: `a_dead` / `b_dead` / `timeout` | **The death-vs-under-damage distinction the old artifact could not make.** `a_dead` = player died (real defensive failure); `timeout` = survived but didn't kill in time (too-slow / enrage); `b_dead` = clean kill. This is the single most valuable new column. |
| **TTK (won fights)** | `fr.elapsed_s` on `winner=="player"` fights | Boss kill-time distribution; informs DPS-measure design + encounter tuning. |
| **KPM** | `observed_kpm` = `mobs_killed`/min (proxy-inclusive) | Sanity rail only — NOT a gate here. Confirms the over-perf tail (boss-melt > 3.78). |

Aggregate by **attribute** (int / wis / dex / str — parse from `legendary_id` as §5 did) and by **archetype**, with n per cell. Output a clean JSON + a gandalf-consumable summary table that drops into a corrected §5.

## 4. Verify-items — GATES, math-note-first (Discipline #1). Confirm BEFORE numbers are trusted.

- **V1 (winner = survive AND kill):** confirm `run_spatial_fight` resolves `fr.winner=="player"` ONLY when (a) the win_condition target (boss/mini-boss entity) is dead AND (b) the player is alive — i.e. a player death before the boss dies yields `winner!="player"`. arena.py confirms the kill half (`boss_killed`/`mini_boss_killed`, `mini_boss_index=0`); confirm the player-alive half in the spatial engine. **If winner can be "player" without the boss dead, or while the player is dead, survival_rate ≠ survive+kill and this whole table is invalid.** This is THE load-bearing semantic (the kind of assumption Gate-1 just burned us on — do not assert it; read it).
- **V2 (enrage cap):** report the ACTUAL hard time-cap `run_spatial_fight` enforces on each boss shell (arena.py per-scenario `max_duration` / hard limit). mini_boss is documented 150s soft + 240s hard (`arena.py:720`); confirm boss_with_adds. Reconcile the stale `120s` label at `t4_sim_cycling.py:252`. The cap IS the doctrine's enrage timer — `timeout` terminations are "didn't kill before enrage."
- **V3 (faithful power):** confirm the run executes at max-profile investment (current default), NOT the stripped ablation floor. "Real boss numbers" means geared/faithful kits.
- **V4 (proxy-inclusive kills, Matt #5):** confirm `fr.mobs_killed` counts a mob as killed regardless of whether the player, a summon/totem, or a DoT landed the final blow. (Expected yes by construction — it's a dead-mob count — but confirm; it is the #5 measurement rule.)

## 5. DPS (Matt's #8) — SCOPED OUT of this run; flagged as the Tier-B follow-on

The spatial result currently **drops per-fight damage** (`player_damage_dealt=0.0`, `t4_sim_cycling.py:1096-1098` — "SpatialFightResult carries no per-fight damage field"). Measuring DPS requires gamora to surface player **+ all proxy** damage from `run_spatial_fight` / `SpatialFightResult`, then DPS = damage/elapsed. **That is engine instrumentation, not a harness — a separate build.** This run delivers survive+kill + termination-breakdown + TTK + KPM now; DPS is identified here so the design session knows the DPS-measure pillar is new instrumentation with a real cost, not free. Do NOT block this run on DPS.

## 6. Endorse criteria (what makes the output trustworthy — gandalf will check)

1. **Single-regime fingerprint:** the run uses only the current mobs/min regime (current `run_spatial_fight`, faithful power). No old-scale KPM mixed in. (The failure mode that made the prior artifact useless.)
2. **V1–V4 all confirmed** in the gamora math note before the table is read as data. V1 especially.
3. **termination_reason recorded** so death (`a_dead`) is distinguishable from enrage-timeout (`timeout`) is distinguishable from kill (`b_dead`).
4. **n per attribute cell ≥ §5 cell sizes** (not underpowered).
5. **tier_1 bypass is measurement-only** — production ship gate untouched (jack-ryan confirms no gate regression; this is a read-only diagnostic of the existing tier_2).

## 7. Hand-back

gamora → clean JSON + summary table. jack-ryan Gate-2 on harness correctness (V1–V4, no gate regression, faithful power, proxy-inclusive). gandalf consumes → corrected §5 table → the design session decides boss-bridge membership (caster vs STR: real crater or KPM-reject artifact) and ratifies the doctrine against real numbers.

---

**Signed:** gandalf, 2026-06-19. The measurement intent: run the boss shells the way the doctrine says to MEASURE them — survive-and-kill within the enrage timer, with the termination breakdown that tells mastery from failure — so the session rules on data the current gate structurally cannot produce.
