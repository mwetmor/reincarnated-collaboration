# Batch-2 run-state — the fresh 18-roster economy fire (staged, pilot-gated)

> **Governing spec:** `canonical/reap-die-rise-engine/batch2-build-spec-2026-07-06.md` (gandalf, ARCHITECT pass CLEAN).
> **Authorized:** Matt 2026-07-06 ("Fire per its §7"). **Orchestrator:** knight-rider.
> This file tracks leg-by-leg state; the spec is authoritative for intent.

---

## Sequence + live state

| Leg | What | Seam | State |
|---|---|---|---|
| A | economy-axes build (math-first) | rocket (+ gamora adjacency) | ✅ **DONE** — `legA-economy-axes-math-2026-07-06.md` (engine `ed6c349`) |
| A-gate | Gate-1 on the axis math (critique pair + sim consult) | jack-ryan + gandalf + gamora | ✅ **RATIFY-WITH-CONDITIONS** (all three) |
| B-build | wire the `resource_economy` loadout field (Route B) — cross-seam | rocket (emit) + gamora (consume) | ⏳ **NEXT** — dispatch authored |
| B-gate | Gate-2 on the cross-seam field | jack-ryan | pending B-build |
| B-fire | economy pilot: 2–3 cells × ~25 LHS-within-strata; pre-registered GO/HALT | star-lord (fire) · gamora (read) | pending B-gate |
| C | full fresh 18-roster emission, all axes live, detached ~12–15h | star-lord (gamora shells) | gates-on B-GO **+ Leg-C-entry gate below** |
| close | batch-2 run report → elrond #18 consult | star-lord → elrond | pending C |

## Gate-1 disposition (2026-07-06) — RATIFY-WITH-CONDITIONS

- **Math / #1 / #1.2:** CLEAN — jack-ryan byte-checked every load-bearing citation.
- **Sweep-isolation #24:** AUDIT CLEAN — E1a⊥E1b (BETA fixed), `_CAST_TIME` excluded, not overloaded on the T4-keyed `gamora_combatant_fields` channel.
- **Structural-honesty:** PASS — default axis corner byte-reproduces the known 0.0-KPM chassis; ranges span outward from a failing center; HALT stays genuine.
- **Route decision: ROUTE B — LOCKED** (rocket + jack-ryan + gamora all concur). Single additive `resource_economy` loadout dict, init-consumed; sibling of the `t4_cost_resource` precedent.

**Frozen Route-B contract (the field that lands in B-build):**
`resource_economy = {cost_scale, cost_slope, regen_shape, regen_magnitude, on_kill_frac, ramp_per_s, cadence_scale}`

**Binding conditions (carried forward):**
- **C1 (jack-ryan) — 18-cell vocabulary fix → gandalf, BEFORE Leg C.** The engine BC space is **68,040 cells**; the "18" is a Matt-ruled demo-roster tiling target (1 kit/rostered cell), NOT a subset enumeration. Spec phrase "full 18-cell emission — every BC cell populated" conflates enumerable space with roster count. Leg A/B unaffected; must close before Leg C.
- **C2 (jack-ryan) — Route B ratified pending gamora concurrence** → gamora concurred → **firm.**
- **C3 (jack-ryan) — B-build carries MIGRATION.md + round-trip smoke; Gate-2 verifies** (ADR-004).
- **C4 (jack-ryan) — default-corner 0.0-KPM regression must be a HARD CHECKED ASSERTION in the pilot, not prose.**
- **gandalf G1 — Axis-5 coverage boundary (MATT-FACING RULING, before Leg C).** Resource economy is BC **Axis 5, a locked 7-bin substrate axis.** The mana-triple reaches the **4 statistical bins** (overflow/steady/generator-spender/starved) but CANNOT reach the **3 structural bins** (HP-economy / damage-taken-converts / charge-stack — keyed on cost-TYPE, not magnitude). Per spec §5, empty axis-bins make the clustering form factions around economy-*absence*. **Matt should rule the hole as a scoped decision, not inherit it after the faction cut.**
- **gandalf G2 — Leg-B report in Axis-5 identity terms** ("generator-spender cleared"), not lever-coordinates ("clear near c=0.7").
- **gandalf G3 — categorical-shape findings stamped pilot-confidence** (~4 LHS points/stratum is directional; densification is Leg C's job).
- **gamora carry-forwards:** (a) caster population is mana-default-only = the correct C2 instrument (build-spend economies deferred, separate rocket item); (b) **RUN PRECONDITION: `WIRE_RESOURCE_ECONOMY=True` must be asserted** — pilot fires inert if the flag is OFF (`spatial_engine.py:1221`); (c) Discipline #12 semantic-shift extends Phase-1; MIGRATION+round-trip with the B-build code.
- **gamora file-location correction (Discipline #11):** the binding fight loop is `spatial_gauntlet/spatial_engine.py` (regen tick `:2407`, energy gate `:1213/:1244`, cast decrement `:2136/:2319`, kill flip `:1506-1508/:1519-1521`), NOT `combatant.py` kernel. rocket's cites were correct as kernel cites; the wiring lands in spatial_engine.

## Leg-C-entry gate (auto-continue is no longer blind)

Spec §8 D1 default = auto-continue Leg C on B-GO. Gate-1 added two Leg-C-gating findings that resolve **during the Leg-B window** (independent of the pilot fire):
1. **C1 — 18-cell vocab fix** (gandalf spec edit).
2. **gandalf G1 — Axis-5 structural-bin hole ruling** (Matt).

Leg C auto-continues on B-GO **AND** these two closed. HALT on B always escalates to Matt regardless.

## QA / note trail
- jack-ryan Gate-1: `qa/pending/2026-07-06-legA-economy-axes-gate1-jackryan.md` (`bf2f571`)
- gandalf Gate-1: `gandalf/notes/2026-07-06-legA-economy-axes-gate1-gandalf.md` (`fdd9082`)
- gamora consult: `simulation/notes/2026-07-06-legA-economy-binding-consult.md` (`be6c7c6`)
- rocket axis math: `generation/notes/legA-economy-axes-math-2026-07-06.md` (`ed6c349`)
