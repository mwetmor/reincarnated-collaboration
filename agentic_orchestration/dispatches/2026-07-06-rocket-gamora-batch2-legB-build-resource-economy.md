# Dispatch — 2026-07-06 — rocket + gamora — batch-2 Leg B BUILD: wire the `resource_economy` field (Route B)

**From:** knight-rider
**To:** rocket (emit lead) + gamora (sim-consume) — coordinated cross-seam build
**Approved by:** Matt 2026-07-06 (batch-2 authorization, "→ Leg B economy pilot"). Route B locked at Gate-1 (rocket+jack-ryan+gamora concur).
**Estimated effort:** ~3–5h across both seams
**Acceptance:** the `resource_economy` loadout dict emits from generation, binds in the SPATIAL fight loop (cost/regen/cadence + on_kill hook), MIGRATION.md authored, round-trip smoke green, `WIRE_RESOURCE_ECONOMY` asserted, default-corner 0.0-KPM regression is a HARD ASSERTION. Then → Gate-2 (jack-ryan).

## Context

Leg A math note (`generation/notes/legA-economy-axes-math-2026-07-06.md`) is Gate-1 RATIFIED-WITH-CONDITIONS. Economy is BC Axis 5; Matt ruled Q1(a) — the population votes on economy identity. This dispatch wires the three axes (E1 cost, E2 regen, E3 cadence) so the Leg-B pilot can actually sweep them. **Route B is locked** by the Gate-1 critique pair + gamora sim consult. This is a genuine cross-seam contract change (ADR-004 / Principle 6).

**This is BUILD only — NO pilot fire, NO gauntlet.** The fire is a separate downstream dispatch (star-lord) after Gate-2.

## Frozen Route-B contract (do NOT drift — both seams build against exactly this)

```
resource_economy = {
    "cost_scale":       float,   # E1a — uniform multiplier on _ENERGY_COST table
    "cost_slope":       str,     # E1b — {"flat","escalating"} (BETA=0.25 fixed for escalating)
    "regen_shape":      str,     # E2  — {"flat","on_kill","ramping"}
    "regen_magnitude":  float,   # E2  — g_flat (flat) | passive floor (on_kill) | RAMP/s (ramping)
    "on_kill_frac":     float,   # E2  — burst = on_kill_frac · max_mana per kill (0 unless on_kill)
    "ramp_per_s":       float,   # E2  — regen ramp per second (0 unless ramping)
    "cadence_scale":    float,   # E3  — uniform multiplier on _COOLDOWN table
}
```
Additive-only; sibling of `t4_cost_resource`. Default corner `{1.0,"flat","flat",1.0,0.0,0.0,1.0}` MUST byte-reproduce the current chassis.

## Required reading before starting
- `generation/notes/legA-economy-axes-math-2026-07-06.md` — the axis definitions, ranges, composition rules (§1, §5, §7).
- `simulation/notes/2026-07-06-legA-economy-binding-consult.md` — gamora's Route-B rationale + the SPATIAL-engine binding sites + on_kill hook location.
- `agentic_orchestration/qa/pending/2026-07-06-legA-economy-axes-gate1-jackryan.md` — Gate-1 conditions C1–C4.
- `canonical/reap-die-rise-engine/batch2-build-spec-2026-07-06.md` §3 (the pilot this build enables) + §5 (provenance).
- `MIGRATION.md` (engine) — the format for the cross-seam contract note.

## Scope — ROCKET (emit side)
- [ ] Emit `resource_economy` on the caster-kit loadout (Route B additive dict), the exact frozen contract above.
- [ ] Implement the Leg-B **LHS-within-6-strata sampler** (`s`×`r` strata; LHS over `{cost_scale, cadence_scale, regen_magnitude}` per stratum; ~4/stratum → ~24/cell) per axis-note §6, deterministic + salted (fresh offset band `+1_800_000+idx`, disjoint from Leg-1 salts) per §7.
- [ ] Default-corner emit MUST reproduce the byte-verified baseline tables exactly (§1.4).
- [ ] Cite the emit site file:line in MIGRATION.md.

## Scope — GAMORA (sim-consume side)
- [ ] Consume `resource_economy` at the entity-init boundary (`spatial_engine.py` entity-from-class path per your consult, ~`:2770-2806`) — scale cost, cadence, and regen from the one dict.
- [ ] Wire the `on_kill` mana-add hook at the kill flip (`spatial_engine.py:1506-1508` resolver / `:1519-1521` flat) — burst = `on_kill_frac · max_mana` to the killer.
- [ ] `ramping` regen: regen scales with `ramp_per_s · t_in_fight`.
- [ ] **ASSERT `WIRE_RESOURCE_ECONOMY=True`** is set for the pilot run path — inert sweep if OFF (`spatial_engine.py:1221`). Make it a checked precondition, not an assumption.
- [ ] Per-cohort measurement stays first-class (economy identity must NOT collapse into shared bucket keys — the Leg-4 miss). Bucket keys carry economy cohort.

## Scope — JOINT
- [ ] **MIGRATION.md** (ADR-004): generation declares the field, sim declares consumption, both file:line. Discipline #12 semantic-shift note (KPM now varies with per-kit economy identity — extends Phase-1).
- [ ] **Round-trip smoke (C3):** a kit emits `resource_economy` → sim reads it → economy demonstrably modulates a fight (a non-default corner changes KPM vs the default corner). Field-presence check on the joined key.
- [ ] **Default-corner regression is a HARD CHECKED ASSERTION (C4):** the default corner MUST reproduce the 0.0-KPM timeout on both single-target shells — assert it, don't describe it. This is the built-in refutation that the binding is correct.
- [ ] Both AGENT_STATE.md updated.
- [ ] Tags: `rocket/v-batch2-legB-economy-emit-1`, `gamora/v-batch2-legB-economy-consume-1` (or a joint tag at Gate-2 — your call, documented).

## Cross-seam contract change? (Principle 6 gate)
**YES — this dispatch IS the cross-seam contract change** (new `resource_economy` loadout field, generation→sim). Acceptance REQUIRES the round-trip smoke above (C3). Gate-2 (jack-ryan) verifies before any pilot fire.

## Out of scope (explicit non-goals)
- **NO pilot fire, NO gauntlet, NO population emit-at-scale.** Build + smoke only. The fire is star-lord's downstream dispatch after Gate-2.
- **NO structural-bin economies** (HP-economy / damage-taken-converts / charge-stack) — those are the 3 unreachable Axis-5 bins (gandalf G1); OUT of scope by construction (mana-default caster population). Do not attempt to reach them.
- **NO band re-tune / re-emit of pilot or pre-axes kits** (provenance law §5).
- **NO 18-cell / roster-enumeration work** — that's the C1 vocab fix (gandalf, spec-side), not this build.

## Open questions for the agents to resolve (document your answers)
- Coordination order: rocket emits the frozen dict first, gamora wires against it? Or parallel against the frozen contract with gamora owning the reconciling round-trip smoke? (Contract is frozen above, so parallel is viable — pick and document.)
- Sampler home: which module owns the LHS-within-strata draw (rocket), and how the pilot driver requests it (star-lord's downstream fire consumes it).

## References
- Leg A axis math `ed6c349`; gamora consult `be6c7c6`; jack-ryan Gate-1 `bf2f571`; gandalf Gate-1 `fdd9082`
- Spec `batch2-build-spec-2026-07-06.md` §3/§5/§8; ADR-004 (MIGRATION); Principle 6 (round-trip); Discipline #12 (semantic-shift), #24 (sweep-isolation)
- `t4_cost_resource` precedent: `combatant.py:711,951` (kernel) — the sibling contract

---

## Completion record

### rocket (EMIT side) — COMPLETE 2026-07-06 — tag `rocket/v-batch2-legB-economy-emit-1` (engine `9eca04c`), NO push

- **Frozen `resource_economy` dict emitted** (exact contract, no drift): both boundaries carry it, KEY ALWAYS PRESENT.
  - **EMIT SITE (pilot production boundary):** `season_generation_pipeline.py:533` (`KitCandidate.to_character_dict`; dataclass field `:424`), sibling of `proxies`.
  - **EMIT SITE (contract parity):** `bc_target_player_class.py:428` (`PlayerClassV2.to_dict`; field `:332`), mirrors the `proxies` two-path contract.
- **Sampler module (rocket-owned):** `generation/resource_economy.py` — `sample_resource_economy(base_seed, samples_per_stratum=4)` (`:124`) = LHS-within-6-strata (6 strata = cost_slope×regen_shape; 3-col LHS, 4-col in on_kill; ~24/cell). Deterministic + salted `ECONOMY_SALT_BASE=1_800_000` (`:64`, disjoint from Leg-1). Also owns `DEFAULT_RESOURCE_ECONOMY` (`:50`, the C4 anchor) + `COST_SLOPE_BETA=0.25`.
  - **Pilot driver requests it (star-lord, downstream, after Gate-2):** `sample_resource_economy(base_seed, samples_per_stratum)` → ~24 frozen dicts per cell; attach each to a kit loadout pre-fight. `DEFAULT_RESOURCE_ECONOMY` is the named regression anchor. Pure function — no fights, no sim touch.
- **C4 default-corner byte-reproduction: VERIFIED (emit side).** `{1.0,"flat","flat",1.0,0.0,0.0,1.0}` == `DEFAULT_RESOURCE_ECONOMY` on emit (smoke E2 GREEN); it is the IDENTITY element of every sim scaling op → sim scaling is a no-op → chassis reproduced. Sim-side 0.0-KPM HARD ASSERTION is gamora's against this emit.
- **Smoke (Disc #2, EMIT half of C3):** `generation/notes/legB_economy_emit_smoke_2026_07_06.py` ALL GREEN (E1/E2/E3/E4). Regression: Leg-1 smoke GREEN; subspace 27 PASS; emitter/proxy/bundle/season-production 122 PASS.
- **Math note (Disc #1, before code):** `generation/notes/legB-economy-emit-math-2026-07-06.md`.
- **MIGRATION.md:** generation-declares half authored (`generation/MIGRATION.md` [2026-07-06] batch-2 Leg B entry); gamora appends the sim-consume half.
- **Out of scope honored:** NO pilot fire, NO gauntlet, NO population emit-at-scale, NO sim-consume (spatial_engine untouched), NO 3 unreachable Axis-5 structural bins.
- **Coordination-order answer (open question):** rocket emitted the frozen dict FIRST (parallel viable since contract frozen); gamora wires the reconciling sim-consume + owns the joint round-trip smoke against this landed emit. Sampler home = `generation/resource_economy.py` (rocket); pilot driver requests via `sample_resource_economy()`.

### gamora (sim-consume side) — pending
<!-- gamora appends on completion of the sim-consume half -->

