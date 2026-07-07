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
| B-build | wire the `resource_economy` loadout field (Route B) — cross-seam | rocket (emit) + gamora (consume) | ✅ **DONE** — emit `rocket/…-emit-1` (`9eca04c`) + consume `gamora/…-consume-1` (`7e1a5d1`); C3 round-trip GREEN, C4 default-corner 0.0-KPM CONFIRMED |
| B-gate | Gate-2 on the cross-seam field | jack-ryan | ✅ **PASS-WITH-FOLLOWUPS** (`77e634b`) — re-ran all suites, no BLOCK |
| B-sign-off | **ADR-002 cross-seam-schema sign-off on `resource_economy`** | **Matt** | ✅ **SIGNED 2026-07-06** |
| B-fire | economy pilot: 2 cells × 25 LHS-within-strata; pre-registered GO/HALT; PRODUCTION path | star-lord (fire) · gamora (read) | 🛑 **HALT** — 0/50 clear; verdict gamora (`6c5303b`) → escalated to Matt |
| C | full fresh 18-roster emission, all axes live, detached ~12–15h | star-lord (gamora shells) | ⛔ **HELD — does NOT auto-continue on HALT.** Awaiting Matt structural direction |
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

## Gate-2 disposition (2026-07-06) — PASS-WITH-FOLLOWUPS (`77e634b`)

jack-ryan re-ran all suites (Disc #11, didn't trust GREEN): consume 7/7, emit 4/4, pathb-1a 35/35, generation 266 (superset of claimed 122), no Leg-1 regression. C4 confirmed a genuine hard assertion (exit≠0 on failure; re-ran → 0.0 KPM both shells + byte-identical to no-key path). Production-path instrument fact sound + documented. No contract drift; `_validate` rejects extra/missing keys. **Escalates to Matt for ADR-002 cross-seam-schema sign-off — engineering is PASS, this is a tiered-approval gate, not a defect.**

**Followups:**
- **FU-1 (jack-ryan):** decisions-log continuity entry for the Disc-#12 semantic shift (KPM now varies with per-kit economy identity) — jack-ryan authors.
- **FU-2 (star-lord pilot dispatch):** carry `assert WIRE_RESOURCE_ECONOMY is True` onto the PILOT run path (currently asserted in build smoke only) — **folded into the B-fire dispatch.**
- **FU-3 (rocket/gamora, cosmetic):** stale MIGRATION `file:line`s (read `:2694`→`:2780`; flips `:1506/:1519`→`:1536/:1550`) — code correct, citations drifted; batch on next touch.
- **FU-4 (optional):** add no-key==default byte-identity check to the smoke.

## B-fire VERDICT (2026-07-06) — 🛑 HALT (pre-registered, spec §3 — designed outcome, not a failure)

**gamora read `6c5303b`** (`simulation/notes/legB-economy-pilot-read-2026-07-06.md`). Run `617409b8…`, seed base `62_000_000`, 101.3s detached.

- **Formal call:** 0/25 plain-caster configs clear EITHER shell solo → 0/25 clear both → GO condition (i) fails. Sweep confirmed genuinely LIVE via all three anchors: C4 default-corner 0.0/0.0, production path (`from_player_class`→bounded pool, not un-starvable projection), FU-2 `WIRE_RESOURCE_ECONOMY` guard passed.
- **Landscape headline:** best open_arena config 1.0 vs 9.90 (**10.1% of floor, ~10× short**); best chokepoint 2.1 vs 11.65 (**18% of floor, ~5.5× short**). Gradient is **STEEP-but-SHORT** — economy levers HAVE grip (reorder configs), but the axis's ENTIRE dynamic range is worth ~1–2 KPM against a ~10–12 KPM requirement. **Economy tuning cannot close a 10× gap.**
- **Structural-honesty prediction CONFIRMED + sharpened:** the block is below the economy layer — not a bad-region-sampled miss. It's the whole economy layer that's insufficient (Leg-4 "band re-tune may be insufficient" confirmed).
- **Diagnostic seam (localizer):** caster is FINE on packs (3–4 KPM, economy-independent) and broken ONLY on single targets (1–2 KPM, economy-limited) → deficit localizes to **single-target damage-per-cast × cadence vs the 300k/500k HP wall** — a layer the economy cannot govern.
- **Economy-identity read (Axis-5, pilot-confidence):** warm-up/ramping got closest; builder-spender/on_kill dead-floor (chicken-and-egg: can't land the first kill to bootstrap the refund); cheap-sustained mid. Economy identity determines which caster feels LEAST-broken, not which is viable.
- **Summoner cell:** per-cohort measurement INTACT (Balanced/Hybrid scored separately across 25 econ_keys; the empty-`caster_proxy` miss did NOT recur). Certification machinery instrument-ready for when the structural block clears.

**Consequence:** Leg C is HELD (does not auto-continue on HALT). C1 vocab fix also parked — Leg C is not the next move regardless. **Escalated to Matt for structural direction** (analysis only; no fire recommended).

## Leg-C-entry gate (auto-continue is no longer blind)

Spec §8 D1 default = auto-continue Leg C on B-GO. Gate-1 added two Leg-C-gating findings that resolve **during the Leg-B window** (independent of the pilot fire):
1. **C1 — 18-cell vocab fix** (gandalf spec edit) — OPEN, gandalf before Leg C.
2. **gandalf G1 — Axis-5 structural-bin hole ruling** — ✅ **RULED by Matt 2026-07-06** (see below).

Leg C auto-continues on B-GO **AND** these two closed. HALT on B always escalates to Matt regardless.

### Axis-5 ruling (Matt 2026-07-06) — 3 structural bins INTENTIONALLY-EMPTY-FOR-NOW

The 3 structural-cost bins (**HP-economy / damage-taken-converts / charge-stack**) are ruled **intentionally-empty-for-now** in the batch-2 / faction derivation — the mana-default caster population by construction. NOT a gap; a scoped decision. Ships with **gandalf's three guards** (all binding):

- **Guard 1 — reserved, empty-by-ruling.** The 3 bins are recorded RESERVED / empty-by-ruling in the Axis-5 schema, and the **elrond #18 consult is told the coverage explicitly** (so the clustering does not silently form factions around economy-*absence*). → routing: gandalf annotates the axis schema; knight-rider briefs elrond at the derivation-step-3 consult.
- **Guard 2 — F5 re-derivation pre-registered as the arrival path.** When a structural-cost population ships, it enters as its **own build, own pilot, NEW-BRANCH entry**, and triggers **affected-cut re-ratification only** (not a full library re-derivation). → routing: pre-registered in decisions-log / spec (jack-ryan + gandalf).
- **Guard 3 — naming/flavor may not claim identity the population lacks.** The naming/flavor pass (derivation step 6) may NOT assign structural-cost identity (HP-cost, damage-converts, charge-stack flavor) to a population that is mana-default. → routing: constraint on the step-6 naming/flavor dispatch (gandalf).

## B-build result (2026-07-06) — Route B wired, binding CONFIRMED

- **Emit (rocket):** `resource_economy` on both loadout boundaries (`season_generation_pipeline.py:533`, `bc_target_player_class.py:428`), key always present, sibling of `proxies`. Sampler `generation/resource_economy.py` (LHS-within-6-strata, salt `1_800_000`). Emit smoke GREEN; regression clean.
- **Consume (gamora):** entity-init read `spatial_engine.py:2694` (`_econ = class_dict.get("resource_economy") or DEFAULT_RESOURCE_ECONOMY` — sim default IS the emit contract, no drift). Cost `:2745`, cadence `:2126`, regen `:2820`/ramp `:2440`. on_kill hook `_on_kill_energy_burst` at both flip sites (`:1536`/`:1549`).
- **C3 round-trip GREEN:** favorable corner moves a REAL season-001 caster off 0.0 KPM on both shells (open_arena 0.0→1.0/2.67 ramping; chokepoint 0.0→1.0).
- **C4 CONFIRMED (load-bearing):** default corner reproduces 0.0 KPM on BOTH shells + byte-identical to no-economy-key path → the binding is real.
- **Instrument fact (matters for the pilot fire):** economy bites ONLY on the PRODUCTION (bounded-pool) path — the projection/harness path pins `mana=1e9` and cannot starve (`spatial_resolver_adapter.py:192`). **The Leg-B pilot MUST fire through the production path.**
- **WIRE_RESOURCE_ECONOMY** precondition asserted on the run path.

## B-fire result (2026-07-06/07) — pilot FIRED, gamora reads GO/HALT

**Run ID:** `617409b8-3508-4a4f-a307-107c6f564246`
**Engine commits:** `bfb6097` (driver) + `3a09a4d` (artifacts)
**Wall time:** 101.3s — DETACHED nohup (PID 31410, exit 0)
**Seed base:** `62_000_000`

**Cells fired:**
- plain_caster: `endgame_bc_ranged_medium_variable_int_none` (proxy=none), 25 configs, calibrated mobs (300k/500k HP, dmod=0.3)
- summoner: `endgame_bc_ranged_medium_variable_int_none` (proxy=light), 25 configs, same calibration
- Third cell (D2): EXCLUDED — marginal cost not ~zero at config time; documented in run config

**Assertions confirmed on run path:**
- `WIRE_RESOURCE_ECONOMY is True` — PASS (FU-2 carried from Gate-2)
- Production path: `from_player_class` → bounded pool — CONFIRMED
- C4 default-corner: open_arena=0.0 KPM, chokepoint=0.0 KPM — PASS (HARD CHECKED ASSERTION)

**Measured landscape (gamora reads GO/HALT):**
- plain_caster open_arena: max KPM = 1.0 (bar lo 9.90); 0/25 configs clear
- plain_caster chokepoint: max KPM = 2.1 (bar lo 11.65); 0/25 configs clear
- n_configs_clearing_both: 0

**Measurement report:** `output/economy_pilot/economy_pilot_measurement_report.json` (schema `economy-pilot-v1`)
**Checkpoint:** `output/economy_pilot/economy_pilot_checkpoint.json`

Per-cohort bucket keys LIVE: `_econ_key()` encodes all 7 fields as stable string hash — no cohort collapse.

**GO/HALT verdict:** gamora reads and reports per spec §3 pre-registered criteria.

## QA / note trail
- jack-ryan Gate-1: `qa/pending/2026-07-06-legA-economy-axes-gate1-jackryan.md` (`bf2f571`)
- gandalf Gate-1: `gandalf/notes/2026-07-06-legA-economy-axes-gate1-gandalf.md` (`fdd9082`)
- gamora consult: `simulation/notes/2026-07-06-legA-economy-binding-consult.md` (`be6c7c6`)
- rocket axis math: `generation/notes/legA-economy-axes-math-2026-07-06.md` (`ed6c349`)
- star-lord B-fire driver: `export/economy_pilot_driver.py` (`bfb6097`)
- star-lord B-fire artifacts: `output/economy_pilot/` (`3a09a4d`)
