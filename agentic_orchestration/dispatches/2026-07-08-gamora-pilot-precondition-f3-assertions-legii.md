# Dispatch — 2026-07-08 — gamora — pilot precondition: F3 fix + catalog-count consume + Leg-ii harness

**From:** knight-rider
**To:** gamora
**Approved by:** Matt (two-leg pilot process ratified 2026-07-08); commissioned via gandalf transmission `agentic_orchestration/gandalf/notes/2026-07-08-kr-commissioning-transmission-pilot-preconditions.md`
**Estimated effort:** ~2.5–4 h (three beats; beat (a) is verify-not-derive per Gate-1 — see below)
**Acceptance:** F3 STOP resolution **confirmed to hold** under the extended catalog + re-point (NOT re-derived — it was resolved 2026-07-07); gamora consumes rocket's catalog MIGRATION (count 18→N across all six guard sites + band entries) so `gauntlet_sim` imports clean AND the t4 catalog-load path runs clean over the extended catalog; Leg-ii kit-grain spatial harness prepped drawing from the seed-57000000 population.

> **Gate-1 amendment (jack-ryan, 2026-07-08 — BLOCK cleared):** the F3 `boss_damage_scale` STOP is **ALREADY RESOLVED**, verified against source: `gauntlet_lived_channel_repilot_driver.py:62` → `F3_STOP_FLAG = False  # RESOLVED`; `bds=48.0` LOCKED (`:59-60`, boss dmg = 5.0*0.03*48.0 = 7.2, F3 pop WR 0.7018 in-band); derivation math note `simulation/math/step3-f3-boss-damage-scale-2026-07-07.md` exists (2026-07-07). The commissioning transmission's §8.5 carried the STOP forward as open — a stale carry-forward (the exact class of error §8.1 retracted). **Beat (a) is therefore VERIFY-not-DERIVE.** Do NOT re-derive or re-lock the scale.

## Context

The 1800-candidate emission run was Matt-killed 2026-07-08 as mis-instrumented. Two seams supply the pilot preconditions: rocket adds the missing F4/F1 rooms + dedups the feed (companion dispatch); **you** confirm the (already-resolved, 2026-07-07) F3 STOP still holds, consume rocket's cross-seam catalog contract, and prep the Leg-ii kit-grain harness. The stratified re-fire pilot fires only when all three preconditions land (catalog · dedup · F3 fix). This dispatch fires NO run — it validates instruments and preps a harness.

Governing doc: **§8** of `agentic_orchestration/gandalf/notes/2026-07-08-1800-run-postmortem-misinstrumented-emission-fire.md` (§8 governs where it conflicts with §2/§3/§6).

## Required reading before starting

- **Post-mortem §8** (governs): the same-day correction — §8.2 (season_emit≡0 by construction), §8.5 (revised two-leg pilot; Leg-ii is yours).
- **Commissioning transmission:** Unit 2 (your unit) — `agentic_orchestration/gandalf/notes/2026-07-08-kr-commissioning-transmission-pilot-preconditions.md`.
- **rocket's MIGRATION.md** (lands with the companion dispatch `2026-07-08-rocket-pilot-precondition-catalog-dedup.md`) — declares the new encounter count, the **six** count-guard sites you update (five in `gauntlet_sim.py` + `t4_sim_cycling.py:617-620`), and the band-key needs.
- Your own seam: `gauntlet_sim.py:109/667/1203/1871/1884` (count guards), `:323` (`ENCOUNTER_COHORT_KPM_BAND`), `:611-625` (`SPATIAL_ENCOUNTER_KPM_BAND` + keys=={"balanced"} assert), `:217-234` (escape_lane criterion, registered).
- `simulation/math/w-alpha-6-per-encounter-type-bands-2026-05-28.md` (band-derivation methodology — for the dense_cell band).
- engineering-disciplines.md: **#1** (math-before-code — F3 scale + dense_cell band), **#2/#2-FF**, **#11**, **#18.1** (substrate-voting-is-binding), **#24** (single-parameter sweep isolation).

## Math-before-code

- **Beat (a) F3 `boss_damage_scale` — VERIFY, do not derive:** the rank-deficiency was diagnosed and the corrected scale (`bds=48.0`, boss + mini-boss tiers only) derived and LOCKED 2026-07-07 (math note `step3-f3-boss-damage-scale-2026-07-07.md`; `F3_STOP_FLAG = False`). Your job is to **confirm the resolution still holds** under the extended catalog + any driver re-point, and cite the provenance. Discipline #24 here means the INVERSE risk: **do NOT perturb the locked `boss_damage_scale=48.0`** (`repilot_driver:61`). If the re-point demonstrably invalidates the 2026-07-07 lock, STOP and escalate with the specific reason — do not silently re-derive.
- **Beat (b) dense_cell band:** derive its `ENCOUNTER_COHORT_KPM_BAND` / `SPATIAL_ENCOUNTER_KPM_BAND` entry per the w-alpha-6 methodology. **escape_lane band = wiring only** (already registered + density-verified at `:217-234`; do NOT re-derive).
- **Beat (c) Leg-ii:** no derivation; the discipline is sampling-frame correctness — draw from the seed-57000000 population, NOT fresh rolls (below).

## Cross-seam contract change? (Principle 6 gate — completed by knight-rider at authoring)

**Beat (b): YES — you are the CONSUMER of rocket's cross-seam contract change (ADR-004).** rocket's MIGRATION.md hands you the count/band contract. You update **all six** count-guard sites — five in `gauntlet_sim.py` (`:109`, `:667`, `:1203`, `:1871`, `:1884`) plus `t4_sim_cycling.py:617-620` (the runtime SC-6 guard) — from 18 → N and add band entries for the new shell(s). **Ordering:** rocket lands FIRST. Between rocket's catalog landing and your consume beat, `import gauntlet_sim` raises `AssertionError` (18 ≠ new count) and the t4 catalog-load path raises the SC-6 RuntimeError — this transient is expected and confined to your seam; your consume beat closes it. Do not tag any milestone while the window is open.

**Round-trip smoke (Principle 6 — you complete rocket's beat-(a) round-trip):** after consuming, `import gauntlet_sim` is clean AND a gauntlet smoke over the extended catalog emits per-family verdicts including **F4 (escape_lane)** and **F1 (dense_cell)**. This smoke is the round-trip that closes the rocket→gamora contract. Cite it in your completion record.

**Beats (a) and (c): NO cross-seam contract change.** F3 scale is within-seam simulation; Leg-ii harness prep produces a sampling harness, not an inter-seam dict field. Round-trip: not applicable for (a) and (c).

## Scope

**Beat (a) — F3 `boss_damage_scale`: VERIFY resolution holds (NOT re-derive):**
- [ ] Confirm F3 STOP resolution status against source: `repilot_driver:62` (`F3_STOP_FLAG = False`), `:59-61` (`bds=48.0` LOCKED), math note `step3-f3-boss-damage-scale-2026-07-07.md`.
- [ ] Confirm the resolution holds under the extended catalog + any driver re-point; a boss-fight smoke shows non-degenerate F3 verdicts under the locked `bds=48.0`.
- [ ] Cite the resolution provenance in the completion record. If (and only if) the re-point invalidates the lock, STOP and escalate with the specific failing evidence — do NOT re-derive silently.

**Beat (b) — consume rocket's catalog MIGRATION (cross-seam):**
- [ ] Read rocket's MIGRATION.md; update **all six** count guards from 18 → N: five in `gauntlet_sim.py` (`:109`, `:667`, `:1203`, `:1871`, `:1884`) **plus `t4_sim_cycling.py:617-620`** (the independent runtime SC-6 guard, `if encounter_count != 18: raise RuntimeError`). Missing the t4 guard leaves a second false-clean window — it's the mis-fire's own signature (a guard nobody re-pointed).
- [ ] Add `ENCOUNTER_COHORT_KPM_BAND` + `SPATIAL_ENCOUNTER_KPM_BAND` entries for escape_lane (wiring per registration) and dense_cell (derived per w-alpha-6). Respect the `:625` keys=={"balanced"} assert.
- [ ] `import gauntlet_sim` clean AND the **t4 catalog-load path runs clean** (a bare import does NOT trip `t4_sim_cycling:618` — it's a runtime guard inside a function); gauntlet smoke emits per-family verdicts over the N-encounter catalog (the round-trip).

**Beat (c) — Leg-ii kit-grain spatial harness prep:**
- [ ] Harness: **18 cells × ~6 kits**, **kit-grain family verdicts** on the spatial harness.
- [ ] **Sampling discipline (MANDATORY): draw from the seed-57000000 population, NOT fresh rolls** — GRAIN must measure the actual population emission would stamp (transmission Unit 2(b); §8.5 Leg-ii).
- [ ] Harness produces the GRAIN verdict shape (within-cell verdict heterogeneity: do same-cell kits diverge on family verdicts?). Prep only — no full run fires from this dispatch.

**Common:**
- [ ] Smoke-test passes (each beat)
- [ ] MIGRATION consumed (beat b) — round-trip smoke cited
- [ ] Round-trip smoke (beat b) / not-applicable (a, c) per Principle 6
- [ ] AGENT_STATE.md updated at session end
- [ ] Tag (intermediate, seam-prefixed): e.g. `gamora/v-pilot-precond-f3-consume-legii-1`

## Acceptance criteria

- [ ] F3: resolution confirmed to hold — provenance cited (`F3_STOP_FLAG=False`, `bds=48.0` locked, 2026-07-07 math note); boss-fight smoke shows non-degenerate F3 verdicts; locked `bds=48.0` NOT perturbed
- [ ] All SIX count guards updated 18 → N (five in `gauntlet_sim.py` + `t4_sim_cycling.py:617-620`)
- [ ] `python -c "import reincarnated.simulation.gauntlet_sim"` exits clean (no AssertionError) AND the t4 catalog-load path runs clean (a call exercising `t4_sim_cycling` catalog validation raises no SC-6 RuntimeError)
- [ ] Band entries present for escape_lane (wiring) + dense_cell (derived); `:625` assert still holds
- [ ] Gauntlet smoke over the N-encounter catalog emits per-family verdicts incl. F4/escape_lane + F1/dense_cell (this is the beat-(b) round-trip; must exercise the t4 path, not a bare import)
- [ ] Leg-ii harness runs a smoke slice (e.g. 2 cells × 2 kits) drawing from seed-57000000 population and emits kit-grain family verdicts — full 18×~6 is prep, not fire
- [ ] Round-trip smoke: beat (b) round-trip cited (import-clean + per-family verdicts over extended catalog). Beats (a)/(c): not applicable — within-seam.

## #2-FF pre-fire verification (this dispatch names its instruments)

- **Beat (a) instrument:** F3 resolution provenance + a boss-fight sim smoke. **Pre-fire check:** `grep F3_STOP_FLAG src/reincarnated/simulation/gauntlet_lived_channel_repilot_driver.py` → `= False  # RESOLVED`; a boss-fight smoke under the locked `bds=48.0` shows non-degenerate F3 verdicts. (This is a confirm, not a derive — the STOP is already closed.)
- **Beat (b) instrument:** `import gauntlet_sim` + the t4 catalog-load path + gauntlet per-family verdict emission. **Pre-fire check (must exercise BOTH guard files):** `python -c "import reincarnated.simulation.gauntlet_sim"` exits clean AND a call through `t4_sim_cycling`'s catalog validation raises no SC-6 RuntimeError. A bare import alone is INSUFFICIENT — the t4 guard (`:618`) is runtime, not import-time. First-log-line of gauntlet smoke: `catalog N encounters | families F1..F4 all covered`.
- **Beat (c) instrument:** the Leg-ii harness's kit-grain verdict emitter. **Pre-fire check:** smoke slice log names the seed source (`population seed=57000000`, not `fresh roll`) and emits per-kit family verdicts.
- **Precondition state this dispatch stands on:** four-family gate LIVE (R4 flip 2026-07-07); F3 STOP RESOLVED 2026-07-07 (`bds=48.0` locked — this dispatch confirms, does not re-open); catalog extension arrives via rocket's MIGRATION.

## Out of scope (explicit non-goals)

- **Do NOT touch `generation/endgame_encounter_catalog.py`** or `season_generation_pipeline.py` — rocket's seam. You consume the MIGRATION; you do not add rooms or dedup the feed.
- **Do NOT fire the full Leg-ii run** (18×~6 harvest) — prep + smoke slice only. No emission run of any size until the pilot's verdicts land and Matt's rulings close (post-mortem §6).
- Do NOT re-derive the escape_lane band (registered + density-verified; wiring only).
- Do NOT draw Leg-ii kits from fresh rolls — the sampling-frame is the seed-57000000 population by mandate.
- **Do NOT re-derive or re-lock `boss_damage_scale`** — the 2026-07-07 resolution (`bds=48.0`) stands unless the re-point demonstrably invalidates it (in which case STOP + escalate, do not silently change it). Do NOT co-change other scale parameters (Discipline #24 isolation).

## Open questions for the agent to resolve (document your calls)

- The rank-deficiency root cause for `boss_damage_scale` and the corrected derivation (this is the substantive F3 fix — cite the math).
- The dense_cell band values per w-alpha-6 methodology (math-before-code; falsifier named).
- Whether the seed-57000000 population is materialized on disk or must be regenerated deterministically from the seed for Leg-ii sampling — document the sampling mechanism either way.
- If same-cell kits diverge on family verdicts in the smoke slice: note it (it feeds the GRAIN verdict — the transmission's demo-roster-kits-get-individual-cert path). Full analysis is the pilot's, not this dispatch's.

## References

- Post-mortem §8 (governs): `agentic_orchestration/gandalf/notes/2026-07-08-1800-run-postmortem-misinstrumented-emission-fire.md`
- Commissioning transmission (Unit 2): `agentic_orchestration/gandalf/notes/2026-07-08-kr-commissioning-transmission-pilot-preconditions.md`
- Companion dispatch (rocket, supplies your MIGRATION): `2026-07-08-rocket-pilot-precondition-catalog-dedup.md`
- `gauntlet_sim.py:109/217-234/323/611-625/667/1203/1871/1884` (your seam)
- `simulation/math/w-alpha-6-per-encounter-type-bands-2026-05-28.md`
- Discipline #2-FF proposal (jack-ryan ratification queue): `agentic_orchestration/gandalf/notes/2026-07-08-discipline-2-amendment-full-fire-rider-proposal.md`
