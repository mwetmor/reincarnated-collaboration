# Dispatch — gamora — Wave-B Reservation/Aura BENEFIT round: sim wiring + S6 cert

**Status:** PENDING (BLOCKED until rocket go-token)
**Seam:** gamora (simulation / balance / cert)
**Conductor:** knight-rider (Wave-B Reservation/Aura build lane; run-state `agentic_orchestration/knight-rider/wave-b-reservation-aura-run-state.md`)
**Date authored:** 2026-07-22
**Pattern:** B (multi-slice sim work + full-path cert; dedicated session)
**Ruling that spawned this:** Matt ruled **R2 = (B) BENEFIT-BEARING** + ratified **FIVE families** (2026-07-22). You are the agent that CORRECTLY surfaced the unwired-benefit HALT at S6 cert (SESSION 68). This is the resolution: wire the benefit, then run the cert that is now runnable.

---

## GATE — do NOT start until rocket's go-token lands
rocket LEAD emits the benefit fields FIRST and pushes. **You start only after rocket appends `BENEFIT-EMISSION-READY: aura_benefit_mod + aura_benefit_kind (5-value incl pulse_damage) emitted + pushed`** to `dispatches/2026-07-22-wave-b-reservation-aura-benefit-rocket-emission-LEAD.md`. Read engine HEAD after his push. **No parallel same-tree writes (Discipline #62 — the Wave-C collision that orphaned a commit).**

## What this resolves — READ FIRST (governance)
Your SESSION-68 finding stands: the reservation TAX was wired; the aura BENEFIT was not. `aura_effective_benefit()` (`spatial_engine.py:2650`) composes `full · radius_gate · ramp` correctly but had **zero fight-loop call sites**, and `full_benefit` defaulted 1.0 (never kit-sourced). Matt ruled (B): wire it. rocket now emits the magnitude source. **You do NOT re-touch the radius gate, the C4 ramp, the C3 carrier-widen, the Σ-activation-block guard, or the banner origin-arg thread — all built + smoke-green + preserved.** REMOTE TRUTH `wave-b-economy-engine-spec.md` (`b850800`) stays untouched.

## Required reading
1. `agentic_orchestration/gandalf/design-inputs/2026-07-22-aura-benefit-model-design-read.md` — **§4 (wiring AC — call-site CLASSES by symbol; AC-9a/b/c operationalized), §2 (bands + THE FALSIFICATION), §1 (family shapes 1 & 2), §5 (seam split), the bottom SCOPE AMENDMENT (pulse-damage = AoE emission path + AC-9d + pulse_interval_s=2.0).** Source of record.
2. Your own SESSION-68 artifacts: `simulation/math/waveb-reservation-aura-sim-2026-07-22.md §8` (the HALT analysis + the §8.2 byte-identical sweep this cert must now break), AGENT_STATE SESSION 67/68.
3. `agentic_orchestration/gandalf/design-inputs/2026-07-21-wave-b-reservation-aura-spec-draft.md` — §10-C1 (benefit = stat-mod on in-radius set), §15-R rulings.
4. `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — #1 (math-before-code — REQUIRED here, the pulse AoE path is new arithmetic), #1.1 (resource-bounds), #2 (smoke-test), #8, #12, #40, #41, #62.
5. Read every call-site by symbol/grep at engine HEAD (post-rocket-push), NOT by the read's line numbers (which drift).

## Slice plan (re-sliced per read §5 "slice sizing re-opens")
**Slice B1 — four stat-mod sink axes** (the shape `aura_effective_benefit()` already computes; a SINK problem, not a new mechanism).
**Slice B2 — pulse-damage emission path** (the materially-larger part: a new AoE damage-tick attributed to the aura — closer to `_apply_skill_damage` than to `get_buff_percent`).
**S6 cert** spans both (AC-9a/b/c on the stat-mod families; AC-9d on pulse-damage).

## Acceptance criteria

### Slice B1 — stat-mod wiring (four axes)
1. **Source `full_benefit` from the kit.** The establishment path (`_establish_aura_carriers` ~:2667, called from `run()`) stamps `full_benefit` onto the ActiveEffect params (~:2639) — it must now read the emitted `aura_benefit_mod` instead of defaulting 1.0. `None` ⇒ 1.0 preserved (inert corner byte-identical).
2. **Read `aura_effective_benefit(aura_effect, beneficiary, elapsed)` per-tick per-beneficiary** and apply to that beneficiary's resolved output on the sink axis named by `aura_benefit_kind`. The radius gate + ramp are ALREADY inside `aura_effective_benefit()` — do NOT re-implement; the sink reads the composed `full · radius_gate · ramp` with `full` now kit-sourced.
   - **`damage`** → fold into `buff_dmg_mult` composition in `damage_resolver.resolve_skill` (the `get_buff_percent("buff_damage")` term) — OR seed a `buff_damage` ActiveEffect whose `percent` is refreshed per-tick from the aura's effective benefit. Pick the arithmetic-preserving route; the existing `("buff_damage",…)` dispatch already consumes it, so the aura becomes a *source*, radius-and-ramp-gated.
   - **`defense`** → the incoming-damage mitigation rail (same rail sunder's `damage_taken_percent` uses, mirror-signed): beneficiary's damage-taken ×(1 − effective_benefit).
   - **`regen`** → `combatant.apply_mana_regen_buff` / `get_buff_percent("buff_mana_regen")` (`combatant.py:477`): the aura sources this percent.
   - **`speed`** → the cast/attack/move-rate scalar the beneficiary already carries.
3. **Σ-guard NON-BYPASS (built, live — FLAG A / AC-7-SIM):** the benefit MUST NOT bypass the guard. Order is fixed by built code: `_toggle_aura_on` (~:2605) evaluates `aura_activation_would_breach` BEFORE appending the ActiveEffect (~:2626-2631). A blocked aura is never appended ⇒ its `full_benefit` never enters any sink. AC: a benefit-bearing aura that WOULD breach Σ<0.90 grants EXACTLY ZERO benefit (assert win-rate contribution of a guard-blocked aura is nil).
4. **Banner benefit inheritance (8a):** `plant_banner` (~:2704) already threads `full_benefit` into `_toggle_aura_on` (~:2726) and reuses `aura_effective_benefit` with a `_PosProbe` origin (~:2660). A banner sources `aura_benefit_mod` the SAME way a carried aura does — gated from the plant-point, not the caster. NO separate benefit wiring. AC: banner beneficiaries in radius-from-plant-point receive the benefit; the roaming caster outside plant radius does not (unless self-in-radius).

### Slice B2 — pulse-damage emission path (the fifth family)
5. **`aura_benefit_kind == pulse_damage` is a DAMAGE EMISSION, not a stat-mod.** It does NOT flow through `full_benefit`→sink-mult. It needs its own per-tick AoE-damage-application path: every `pulse_interval_s` the aura emits a damage tick to ENEMIES in radius (centered on the carrier / plant-point via the same origin-arg), attributed to the aura (aura-attributed damage events in telemetry — NOT a buff on anyone).
6. **`pulse_interval_s = 2.0`** is an ENGINE constant (scaffold, Disc #40 — gamora finalizes), NOT kit-emitted. `aura_benefit_mod` for the pulse kind = per-pulse damage as a FRACTION of the bearer's base skill hit (band [0.15,0.35], mid 0.25 ⇒ @2s ≈ 0.125×base-hit DPS — inside the §2 Σ-budget equilibrium principle).
7. **Radius = the existing `aura_radius_m`** (no new geometry). Ramp: the read frames pulse as an emission — decide at math-note time whether the C4 re-attunement ramp applies to pulse magnitude (parallel to stat-mod) or the pulse simply starts/stops with carrier presence; state the choice + rationale (default lean: ramp applies for flicker-parity, but justify).
8. **Σ-guard non-bypass applies identically:** a guard-blocked pulse aura emits ZERO damage (no ActiveEffect ⇒ no pulse source).

### S6 cert — AC-9 "aura-is-felt", now RUNNABLE (the cert that was un-runnable at HALT)
- **AC-9a (non-identity — THE FALSIFICATION):** a band sweep of `aura_benefit_mod` low→high on a damage-amp aura kit produces **monotonically non-identical** fight outcomes (win-rate or TTK moves with magnitude). This is the EXACT test math note §8.2 ran and got 50.000-identical — it MUST now vary. If still byte-identical, the sink is unwired ⇒ **cert FAILS** (not passes). Apply identically to the pulse path (sweep pulse magnitude → aura-attributed damage varies).
- **AC-9b (equilibrium):** aura-ON vs aura-OFF win-rate delta at **band-midpoint** sits in a healthy window — non-trivial (felt: delta ≥ an evaporate floor) but NOT dominant at a single aura (delta below the D2-dominance ceiling). You set the exact window; design constraint is "midpoint ≈ the reservation price at the margin" (§2).
- **AC-9c (stacking is identity, not free power):** two mid-band auras stacked under Σ<0.90 play recognizably differently from one (more total benefit for more total pool paid) but do NOT breach the D2-dominance band.
- **AC-9d (pulse family):** pulse-family aura present ⇒ nonzero aura-attributed damage events in telemetry; band sweep monotonic in aura-attributed damage; Σ<0.90 stacking preserves per-aura attribution.
- **Band finalization (Disc #40):** finalize each of the five scaffold bands between the D2-dominance band (an aura-stacker trivializes content — containment target) and the evaporate band (auras too weak to feel). The read's midpoints are the equilibrium starting-line, not the answer.

## Discipline requirements
- **#1 math-before-code — REQUIRED (not N/A this round):** the Slice-B2 pulse path is NEW arithmetic (per-tick AoE damage attributed to the aura, fraction-of-base-hit magnitude, cadence). Write the math-note BEFORE code: pulse magnitude formula, cadence, radius/origin, attribution, ramp-applies-or-not decision, and the Σ-guard interaction. Slice-B1 stat-mod sinks are arithmetic-preserving (routing a composed scalar into existing hooks) — state the additive claim per axis. Extend `simulation/math/waveb-reservation-aura-sim-2026-07-22.md` (§9+).
- **#1.1 resource-bounds:** if the cert gauntlet is compute-heavy, project peak memory + verify against host RAM before firing.
- **#2 smoke-test:** name smoke fixtures per axis (damage/defense/regen/speed) + pulse + Σ-guard-non-bypass + banner-benefit as deliverables. S6 cert is a SEPARATE full-path gate — do NOT milestone-tag on smoke alone.
- **#8 / #40 / #41 / #12:** preserve additivity; bands are scaffold you finalize; enum is stat-axis mechanical.
- **#62 parallel-tree hygiene:** own the tree alone; read call-sites by symbol at HEAD post-rocket-push.
- **MIGRATION.md:** if any sink wiring changes a cross-seam observable (e.g. telemetry gains aura-attributed damage events), note it (ADR-004). The rocket→gamora field contract is already in rocket's MIGRATION; add the telemetry-attribution note if pulse emits new event rows.

## Out of scope (explicit)
- Any edit to rocket's `aura_geometry` emission surface or REMOTE TRUTH.
- Re-touching radius gate / C4 ramp / C3 widen / Σ-guard / banner origin-arg (all built + preserved).
- The §7 capstone (Fork 4c efficiency dial) — DEFERRED behind this cert AND Q35.
- `aura_polarity` / `aura_target_cap` / `exclusive_aura_class`.

## Commit / push
Auto-commit in-scope work-products. **PUSH authorized "as you go"** (Matt 2026-07-22 per-cycle push pattern). Tag intermediate slices with seam prefix (`gamora/v<next>-wave-b-reservation-aura-benefit-sim-1`, `-pulse-2`); the S6 cert milestone tag drops the prefix ONLY on Matt approval. Append a completion record: sinks wired (per axis), pulse path (math-note ref + attribution), Σ-guard non-bypass confirm, banner benefit confirm, AC-9a/b/c/d results (with the sweep numbers that BREAK the §8.2 byte-identity), finalized bands, smoke + regression, tags. **If the cert FAILS (sweep still byte-identical, or a single aura reaches D2-dominance), STOP and report — do not milestone-tag a failed cert.**

## After gamora green → Gate-2
knight-rider routes jack-ryan Gate-2 (DEV-MODE, BLOCK authority) after the S6 cert is green + tagged. Do not consider the wave closed until Gate-2 passes.

---

## Completion record

**Status:** DELIVERED — gamora, 2026-07-22 (SESSION 69). **S6 cert GREEN 8/8. The FALSIFICATION is broken.**

### Sinks wired per axis (Slice B1, math note §9.1 — arithmetic-preserving)
`full_benefit` is now SOURCED from `aura_benefit_mod` at the ActiveEffect stamp (`_establish_aura_carriers`) — was the 1.0 default (the SESSION-68 HALT). `None` ⇒ 1.0 preserved (inert byte-identical). Per-tick idempotent-REBUILD of aura-sourced rider ActiveEffects (`aura_source=True`) from the live carriers via `_refresh_aura_statmod_riders` at the tick TOP:
- **damage** → `buff_damage` rider read by `resolve_skill:814` `get_buff_percent("buff_damage")` (+ flat-path parity added in `_apply_skill_damage` else-branch, so a flat-damage kit's aura is not silently unwired).
- **defense** → dedicated `aura_defense` mitigation ×(1−m) at the HP-application site (`_aura_defense_mitigation_factor`), mirror-signed vs the sunder amp rail (which clamps ≥0 and would DROP a reduction — the negative-amp-sunder route rejected, math note §9.2). `DEFENSE_MAX_MITIGATION=0.50` runaway guard.
- **regen** → `buff_mana_regen` rider multiplies the energy regen tick (`_regen *= (1 + get_buff_percent("buff_mana_regen"))`).
- **speed** → `1/(1+s)` cadence factor (`_aura_speed_cadence_factor`) applied at BOTH cast writes (committed-path :3157, instant-path :4013).
Radius+ramp already inside `aura_effective_benefit()` — NOT re-implemented; the rider `percent` IS the composed `full·radius_gate·ramp`. A beneficiary leaving radius reverts the SAME tick.

### The pulse path (Slice B2, math note §9.5 — NEW arithmetic, Disc #1 before code)
`pulse_damage` is a DAMAGE EMISSION, not a stat-mod. Own per-tick AoE path `_emit_aura_pulses`.
- **Math-note ref:** `simulation/math/waveb-reservation-aura-sim-2026-07-22.md §9.5` (formula, cadence, origin, attribution, ramp decision, Σ-guard interaction) — authored BEFORE code.
- **Formula:** `pulse_hit = aura_benefit_mod × (primary_skill.damage_multiplier × 500 × damage_modifier) × ramp(elapsed)`. Cadence `AURA_PULSE_INTERVAL_S = 2.0` (engine constant, Disc #40 scaffold — I finalize). Radius = existing `aura_radius_m` (None ⇒ no emission). Delivery mirrors the built `burst-damage` direct-HP path (absorb_with_shield → hp -= → is_alive flip).
- **Attribution mechanism:** `player.aura_pulse_damage_dealt` — a SpatialEntity internal-to-seam accumulator (mirrors `dot_damage_dealt`, which explicitly states "no SpatialFightResult schema change ⇒ no MIGRATION"). SEPARATE from `total/delivered_damage_dealt` (the skill-cast measure) so the AC-9d observable reads directly and no skill-DPS consumer's value shifts. Per-aura attribution verified: two-aura delta = 2× one-aura at equal magnitude.
- **RAMP DECISION:** the C4 re-attunement ramp **APPLIES** to pulse magnitude (default lean adopted). **Justification:** C4's purpose is to make toggling a commitment (no full value faster than τ); if stat-mods ramp but pulse does not, a pulse aura is a flicker-exploit hole (toggle-on → full-damage pulse → toggle-off, dodging the commitment). Applying the ramp keeps all FIVE families under ONE commitment law. Reservation still paid at toggle-ON (ramp gates only emitted magnitude).

### Σ-guard non-bypass confirm
CONFIRMED (AC test GREEN). The benefit rides the aura ActiveEffect; `_toggle_aura_on` evaluates `aura_activation_would_breach` BEFORE appending ⇒ a guard-blocked aura is never yielded by `_iter_aura_carriers` ⇒ its `full_benefit` never enters any B1 refresh AND its pulse never emits (B2 reads the same carrier list). A benefit-bearing aura AND a pulse aura that would breach Σ<0.90 both grant EXACTLY ZERO (carriers stayed 1→1, no side channel). Preserved verbatim — no new wiring.

### Banner benefit confirm
CONFIRMED (AC test GREEN). Benefit inherits via the built `plant_banner` origin-arg thread (no new wiring). A damage banner's beneficiary AT the plant-point receives 0.20; a beneficiary 20m out (roaming caster outside plant radius) receives 0.0. Gated from the plant-point, not the caster.

### AC-9a/b/c/d results (with the sweep numbers that BREAK the §8.2 byte-identity)
- **AC-9a FALSIFICATION — BROKEN.** Damage `aura_benefit_mod` sweep 0.08 → 0.14 → 0.20 gives TTK **24.300 → 23.200 → 22.100** (monotonic decreasing; all < OFF 26.500). This is the EXACT test math note §8.2 ran and got **byte-identical 50.000/50.000/50.000** — it now VARIES monotonically. The sink is wired.
- **AC-9b equilibrium — PASS.** Midpoint (0.14) ON−OFF delta = **12.5% TTK improvement** — inside the healthy window (≥ evaporate floor, < D2-dominance ceiling).
- **AC-9c stacking-is-identity — PASS.** Two mid-band (0.14) damage auras stacked under Σ=0.60<0.90: 1-aura TTK 23.200 → 2-aura TTK **21.000** (recognizably faster — more benefit for more pool paid — no D2-dominance / instant-trivialize).
- **AC-9d pulse — PASS.** Pulse `aura_benefit_mod` sweep 0.15 → 0.25 → 0.35 gives aura-attributed damage **810 → 1350 → 1890** (monotonic increasing, nonzero, per-aura attribution preserved under stacking).

### Finalized bands (Disc #40)
rocket's scaffold midpoints CONFIRMED inside the healthy window at S6: **damage 0.14 / defense 0.14 / regen 0.20 / speed 0.10 / pulse 0.25**. Equilibrium demonstrated at the damage midpoint (12.5%). `DEFENSE_MAX_MITIGATION=0.50` (parity `SUNDER_MAX_AMP_CAP`), `AURA_PULSE_INTERVAL_S=2.0` finalized.

### Smoke + regression
- **S6 cert** `scripts/gamora_waveb_reservation_aura_benefit_s6cert_2026_07_22.py` — **8/8 PASS** (AC-9a/b/c/d + SINKS + GUARD + BANNER + BYTE).
- **Regression:** Slice-1 **8/8**, banner **4/4** (no regression). pytest spatial/aura **57 passed**. Broader sim/fight/resolver/economy **570 passed** (7 pre-existing `season_generation_pipeline.py` cell-grain ERRORs in rocket's generation seam — unrelated; those `output/` files were already dirty pre-session). peak RSS ~51 MB.

### MIGRATION / schema
NO SpatialFightResult schema change (the pulse accumulator is internal-to-seam, mirroring `dot_damage_dealt`) ⇒ **NO MIGRATION owed**. The rocket→gamora field contract is already in rocket's MIGRATION. NO generation/ edit. NO star-lord telemetry-schema change.

### Tags / push
Tag `gamora/v1.13-wave-b-reservation-aura-benefit-sim-1` (B1+B2 wired together in the intertwined tick-loop change — one seam-prefixed slice tag). **NOT a milestone tag** — the milestone tag drops the seam prefix ONLY on Matt approval (per dispatch). Pushed `138999f..a0cb754` on `main` + tag (Matt 2026-07-22 per-cycle push pattern). AGENT_STATE SESSION 69 + math note §9 committed in the same commit.

### After gamora green → Gate-2
Ready for jack-ryan Gate-2 (DEV-MODE, BLOCK authority) via KR routing. Wave not closed until Gate-2 passes.
