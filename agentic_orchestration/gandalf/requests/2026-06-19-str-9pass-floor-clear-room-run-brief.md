# Run brief — STR 9-pass-floor check (clear-room competence, route-via-floor disposition)

**Type:** gandalf-authored measurement-run brief → knight-rider to sequence (gamora harness + jack-ryan Gate-2). Matt-declared 2026-06-19 ("agreed, route it").
**Author:** gandalf
**Driver:** settle STR's boss-failure disposition. The DPS instrument classified STR's boss failure as a **melee target-allocation failure** (deals ~1,300 DPS / ~300k total — would kill the boss 1.1–1.36× over IF focused — but sinks 73–96% into the adds; NOT degenerate, NOT pure-throughput, NOT out-healed). DEX (same physical→bleed ailment, also inert in spatial) succeeds where STR fails → the differentiator is melee-vs-ranged allocation, confirmed. The disposition now hinges on ONE cheap read: **does STR ship on its clear-room competence WITHOUT the two boss shells?**
**Composes with:** the encounter-measurement doctrine ADOPTED by Matt 2026-06-19 (`gandalf/notes/2026-06-19-encounter-measurement-doctrine-spine.md`); the clean boss run (spine §5); the DPS instrumentation (gamora/v-dps-instrument-1, jack-ryan Gate-2 PASS).

---

## 0. The disposition arithmetic (why this run settles it)

The ship gate is `gauntlet_pass(cohort)` = `eligible_encounters_passed(cohort) >= 9` over the **18-encounter** reference gauntlet per cohort (`gauntlet_sim.py:636`, floor `GAUNTLET_ELIGIBLE_PASS_FLOOR_W_ALPHA_6 = 9`).

The 18 break down (`gauntlet_sim.py:125-133`) as **4 boss + 14 clear**:
- **4 boss encounters:** boss_with_adds ×3 (str_01, int_02, wis_02) + mini_boss ×1 (wis_03).
- **14 clear-room encounters:** open_arena, chokepoint_corridor, magic_pack, elite_pack (the W-α6 newly-eligible types).

Under the ADOPTED doctrine STR **auto-fails the 4 boss encounters** (survive+kill = 0.000, spine §5). The current code *also* rejects them (boss KPM 0.25 < the 2.49 floor), so the boss fails are regime-clean either way. Therefore:

> **STR ships via the floor IFF it passes ≥ 9 of the 14 clear-room encounters.**

This run measures exactly that — STR's per-encounter clear-room result across the 14 clear shells, at faithful power, so the disposition is decided on data, not inference.

## 1. THE TRAP (do not re-walk it — generalized from the boss run)

The production path short-circuits tier_2 whenever tier_1 routes REJECT (`gauntlet_sim.py:1019`). A low-DPS archetype's clear shells could tier_1-reject, leaving `tier_2_kpm` **defaulted to 0.0** — which would fabricate a fake "STR fails all clears" exactly as the boss artifact fabricated `survival=0.0`. **This run MUST drive tier_2 on ALL 18 shells unconditionally — bypassing the tier_1 verdict — so STR's clear-room KPM is actually MEASURED, not defaulted.** Measurement harness only; production ship gate untouched. This extends the existing `clean_boss_numbers_harness_2026_06_19.py` tier_1-bypass from the 2 boss shells to all 18.

## 2. What to run

- **Shells:** ALL 18 reference-gauntlet encounters (the full set — 14 clear + 4 boss). Re-running the 4 boss shells is free (reuses the boss-harness path) and gives the doctrine-lens denominator in one artifact.
- **Instrument:** drive `w4g2_tier_2_full_sim(...)` directly per kit × encounter × cohort (the boss-harness mechanism), tier_1-bypassed, on all 18.
- **Population:** the season-001 faithful-power **STR** kit population (attribute-parsed from `legendary_id`, as §5 did). Include dex/int/wis as CONTROLS (cheap, same run) so STR's clear-room pass-rate is read against the archetypes that already pass — but STR is the subject.
- **Cohorts:** all four (DPS-min-maxer, Balanced, Defensive, Hybrid). `eligible_encounters_passed` is per-cohort.
- **Power:** faithful / max-profile investment (current default post flip-#3). Confirm (V2).
- **n_fights:** the production tier_2 count; match/exceed the boss-harness cell sizes (n≈20/cell; attribute cells str/dex/int n≈144, wis n≈360).
- **Seeds:** deterministic, distinct base from the boss harness (Discipline #3), recorded.

## 3. What to record (per kit × encounter × cohort, then aggregated by attribute + cohort)

| Metric | Source | Why |
|---|---|---|
| **tier_2_kpm** (proxy-inclusive) | `observed_kpm` = mobs_killed/min | The clear-room band signal. The thing the floor counts. |
| **band [lo, hi]** for enc_type × cohort | `ENCOUNTER_COHORT_KPM_BAND` | The pass window. |
| **in-band?** + **failure side** | compare KPM to band | NOT just pass/fail — record **below-floor** vs **in-band** vs **above-ceiling** so STR's failure mode is legible (slow vs over-perf clip). |
| **enc_type tag** + **clear-vs-boss** | `scenario_shell_id` | So the 14-clear / 4-boss split is explicit. |
| **survive+kill + termination split** (boss shells only) | as the boss harness | doctrine-lens boss result (reconfirms the 4 auto-fails). |
| **eligible_encounters_passed** | per cohort, TWO lenses | (a) current-code (KPM-band all 18); (b) doctrine (KPM-band 14 clear + survive+kill 4 boss). |

**The headline output:** STR's **clear-room pass count (of 14)** per cohort, with the per-clear-type breakdown (open_arena / chokepoint_corridor / magic_pack / elite_pack) so I can read WHETHER STR is a broad clear-competent or a swarm-only specialist (does it pass the pure-swarm shells but fail the anchored magic/elite packs — the allocation problem recurring on any priority target?).

## 4. Verify-gates — GATES, math-note-first (Discipline #1). Confirm BEFORE numbers are trusted.

- **V1 (tier_2 actually ran on all 18):** confirm tier_1-bypass drove tier_2 on every shell — NO defaulted-0.0 KPM masquerading as a measured miss. The boss-run trap, generalized. Read it, do not assert.
- **V2 (faithful power):** max-profile investment (current default), not the stripped ablation floor.
- **V3 (proxy-inclusive KPM, Matt #5):** `mobs_killed` counts proxy/summon/DoT kills regardless of final-blow source. (STR is melee/solo → proxy term ≈ 0, but confirm the rule.)
- **V4 (clear-shell win condition):** the 14 clear encounters resolve on `all_mobs_killed` and KPM = mobs_killed/min on the pack-clear — not a boss shell mislabeled.
- **V5 (single regime):** current spatial sim only; no old-scale KPM mixed in (the failure that made phase3 useless).
- **V6 (measurement-only):** production ship gate untouched; jack-ryan confirms no gate regression — this is a read-only diagnostic of the existing tier_2.

## 5. Endorse criteria (gandalf checks before consuming)

1. **Single-regime** (current `run_spatial_fight`, faithful power).
2. **V1–V6 confirmed** in the gamora math note before any number is read as data. V1 especially.
3. **tier_1 bypass is measurement-only** — production gate untouched (jack-ryan confirms).
4. **STR clear-room pass-count answerable** — the ≥9-of-14 question is distinguishable, with the per-clear-type texture intact.
5. **n per cell ≥ boss-harness cell sizes.**

## 6. Hand-back

gamora → all-18 JSON + summary table (STR clear-room pass count of 14, per cohort + per clear-type; boss-shell doctrine result; both-lens eligible_encounters_passed) + math note. jack-ryan Gate-2: harness correctness (V1–V6), no gate regression, single-regime, proxy-inclusive. gandalf consumes → STR disposition ruling (route-via-floor confirmed/failed per the pre-registered table) → spine §5 STR-disposition write.

---

**Signed:** gandalf, 2026-06-19. The cheap read that settles STR: measure its clear-room competence directly, so the disposition — ship STR as a clear-specialist (≥9 of 14) or fix the kit (<9) — is ruled on data the boss-only run could not produce. Measured, single-regime, tier_1-bypassed so nothing defaults to a fake zero.
