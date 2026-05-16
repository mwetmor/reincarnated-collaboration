# Dispatch — 2026-05-16 — rocket — B6 pre-work: energy-type-aware skill tier assignment

**From:** knight-rider
**To:** rocket
**Approved by:** Matt at 2026-05-16 Day 4 (after jack-ryan Gate 1 PASS WITH FLAGS — WARN on Step 0 framing + two INFOs addressed; finding at `qa/findings/2026-05-16-jack-ryan-gate1-rocket-b6-and-calibration-epoch.md`)
**Status:** PENDING — ACTIVE (rocket may execute when launched)
**Coordination note:** Star-lord is running a fresh `season_001005` regen in the engine repo in parallel (dispatch `2026-05-16-star-lord-fresh-regen-tier1-coverage.md`). Rocket's Steps 0–2 (math note + code change to `b6_archetype_templates.py`) are safe to run alongside. **Rocket should DEFER Step 3 (smoke generation) until star-lord's regen completes** — both processes would otherwise write to `data/telemetry.db` concurrently. Knight-rider notifies rocket via SendMessage when regen lands; alternatively rocket can check `agentic_orchestration/dispatches/2026-05-16-star-lord-fresh-regen-tier1-coverage.md` for a filled completion record before starting Step 3.
**Estimated effort:** 1 session (~2-4 hours); math-before-code per Discipline #1.
**Acceptance:** Math note quantifying expected tier-bound shift; code change to `b6_archetype_templates.py` adding energy-type-aware tier ranges; intermediate tag `rocket/v1.3-b6-energy-type-tiers`; cross-seam impact recorded in MIGRATION.md if simulation-side consumers see the change.

---

## Context — why this dispatch exists

Gamora's 2026-05-16 modifier-range investigation closed with **Option (e)** as the mitigation: no sim code change; instead, queue **B6 pre-work** in the generation seam to raise tier bounds for rage/physical archetypes so their generated skill magnitudes compensate for sim-mechanical disadvantages.

The empirical finding (gamora math note `simulation/math/modifier-range-root-cause.md` §4.3 + findings file `qa/findings/2026-05-16-gamora-modifier-range-rootcause.md`):

- Modifier range is **0.09–0.52** across 7 recent seasons under B10.4 Option 2 convergence — vs file 29 aspirational target band of 0.85–1.15.
- **Generation is NOT the cause of the gap.** Both hybrid_mage/water (mod=0.095) and physical_warrior (mod=0.525) use tier 25–50 skills with near-identical magnitudes (~77k DPS estimate at mod=1.0). The ~5.5× modifier gap between them is entirely from sim mechanics, not from generation producing different power budgets.
- The **structural disadvantage** for physical rage classes vs elemental mana classes is ~3–5× combined: rage starts at 0 (vs mana starts full) → DPS lag in first third of short fights (~1.5–2.0× factor); physical 15% miss rate (~1.18×); armor ~18.6% vs elemental resistance ~0% (~1.23×); melee positioning delays (~1.1×).
- **The correct fix is in generation, not sim.** Rage/physical archetypes need ~1.5–2× higher skill tier baselines so their generated magnitudes can compensate. Gamora proposed approximate targets: mana elemental tier 25–50 (current); rage/physical tier 38–65 (proposed; ~1.7× higher).
- A targeted sim patch (e.g., 15–20 starting rage) would compress modifiers by ~20% without closing the structural 3–5× gap. Architectural fix is better; that's what this dispatch is.

This is **pre-work for B6** — not the full B6 generation refactor. Scope: energy-type-aware tier-range assignment in `b6_archetype_templates.py` only. The broader B6 work (kit-builder, ability-grammar evolutions) is queued separately.

## What this dispatch does

### Step 0 — Verify gamora's compensation factor before writing code (math-before-code, Discipline #1)

Read gamora's math note §4.3 in full. The math note derives a combined sim-mechanical factor (~2.2–3.0× by the math note's table; the findings file summary states ~2.4–3.3× — read both, surface the discrepancy in your own math note as Discipline #11 attribution, and proceed against whichever range you can independently re-derive).

**The 1.7× working multiplier is a DELIBERATE PARTIAL CORRECTION, not the full combined factor.** Tier magnitude only adjusts damage-per-hit. It cannot close gaps from:

- **Rage startup** (~1.5–2.0× factor; rage starts at 0, mana starts full — this is a time-to-availability problem, not a damage-magnitude problem; tier raises don't help)
- **Physical miss rate** (~1.18× factor; 15% miss vs always-hit — this is a hit-probability problem; tier raises don't help)

Tier-addressable mechanics are armor-shrug (~1.23×) and any composition-of-fights interactions where higher per-hit damage shortens fights enough to mitigate the startup gap. So 1.7× targets the tier-addressable portion of the combined factor; the remainder waits for **B14.5 V2** (energy-type lever in primary recompose loop) to close.

Verify and confirm:
- The combined factor estimate from §4.3 (note whichever range — math note ~2.2–3.0× OR findings ~2.4–3.3×).
- The observed gap of ~5.5× modifier ratio between hybrid_mage and physical_warrior (residual beyond ~3× sim-mechanical is gauntlet fight-distribution interactions).
- Whether you accept 1.7× as the partial-correction working multiplier, or recommend a different factor with reasoning grounded in WHICH mechanics are tier-addressable.

If you propose a different factor: state the tier-addressable-mechanics reasoning in your math note explicitly, and flag for knight-rider before shipping code. Otherwise proceed with 1.7× as the working multiplier, with the partial-correction framing explicit in your Step 1 math note.

### Step 1 — Math note: tier-range shift derivation

File at `reincarnated-engine/src/reincarnated/generation/math/b6-pre-work-energy-tier-shift.md` (or equivalent). Cover:

1. **The empirical disadvantage factor** — adopt gamora's §4.3 number (or your derived number).
2. **Mapping factor → tier multiplier** — tier ranges in the current archetype templates are bounded by `(tier_min, tier_max)`. A 1.7× factor means rage/physical archetypes should have `(tier_min * 1.7, tier_max * 1.7)` approximately. Round to clean tier breakpoints.
3. **Per-archetype proposal** — concrete tier-range table:
   - Mana elemental archetypes: current (tier 25–50 for L1, scaling to higher tiers at L50)
   - Rage physical archetypes: proposed shift (~tier 38–65 baseline, scaling)
   - Hybrid archetypes: which side they sit on (probably partial shift; justify)
   - Hunter (physical ranged): gamora's finding shows avg modifier 0.594 — much closer to physical than elemental. Apply the shift? Or shift partially since hunters don't have rage-startup or melee-positioning factors (only the miss-rate factor)? Recommend.
   - Experimental archetypes: gamora flagged these as outliers (avg mod 0.718). Per `project_trait_architecture.md` note, experimental classes don't roll trait affixes. Recommend: skip the shift; experimental tier is intentional outlier territory.
4. **Tier-cap considerations** — confirm that the proposed upper tier (~65) doesn't crash into other generation constraints (skill power budgets, magnitude tables, etc.).

### Step 2 — Code change scope (after Step 1 lands)

**Target file:** `src/reincarnated/generation/b6_archetype_templates.py` (single file; that's the design intent of "B6 pre-work").

**What changes:**
- Add `energy_type` as a parameter on the archetype-template structure (rage / mana / hybrid).
- Tier ranges are now keyed off `energy_type`: rage-archetypes inherit the shifted range; mana-archetypes inherit the current range; hybrid-archetypes per your recommendation.
- All existing archetype templates get an `energy_type` value derived from their existing definitions.
- The tier-range lookup in the class-generation pipeline (`class_generator.py`?) consumes the new energy-type-aware range.

**What does NOT change:**
- Kit-builder (`b6_kit_builder.py`) — out of scope.
- Skill power budgets or magnitude tables in canonical library — out of scope.
- Trait architecture (`project_trait_architecture.md` is intact) — out of scope.
- Anything in simulation/ — out of scope (this is the WHOLE POINT; we're fixing in generation, not sim).
- Any monster/encounter side — out of scope.

### Step 3 — Smoke test

Per Discipline #2 (smoke-test discipline):
- Generate one season (smoke, not full regen) with the new tier bounds.
- Verify: rage/physical archetype skill magnitudes are ~1.7× higher than prior baseline at equivalent levels.
- Verify: no validation errors at class-generation gate.
- Verify: existing tests in `tests/test_generation.py` (or wherever) still pass.

### Step 4 — Tag + cross-seam discipline

- Intermediate tag: `rocket/v1.3-b6-energy-type-tiers` at the commit closing the change.
- **Milestone tag DOES NOT cut autonomously.** Knight-rider confirms with Matt first.
- **MIGRATION.md:** if generated skill magnitude distributions change in a way simulation-side consumers (balance_loop, fight_engine) read directly via schema, append a v1.X entry per ADR-004. If the change only affects values within existing field semantics (no schema change), MIGRATION.md is not required — but flag in your AGENT_STATE update either way.
- **AGENT_STATE.md:** update with the change summary + smoke status.

## Acceptance criteria

- [ ] Math note filed at `src/reincarnated/generation/math/b6-pre-work-energy-tier-shift.md`
- [ ] Step 0 verification recorded in math note (accept gamora's 1.7× or propose alternative with reasoning)
- [ ] Per-archetype tier-range table proposed with justification per archetype family
- [ ] Code change scoped to `b6_archetype_templates.py` (+ minimal callers if the lookup-pattern requires)
- [ ] Smoke season generated; rage/physical magnitudes ~1.7× of prior baseline confirmed
- [ ] All existing generation tests pass
- [ ] Intermediate tag `rocket/v1.3-b6-energy-type-tiers` cut
- [ ] MIGRATION.md entry if cross-seam-visible (otherwise flag in AGENT_STATE)
- [ ] AGENT_STATE.md updated
- [ ] Knight-rider notified at completion with cross-seam implications and smoke-test results

## Cross-seam considerations

- **Gamora's seam (balance_loop, fight_engine):** READ-ONLY. The whole reason this dispatch lives in your seam is so gamora's seam doesn't need to change. If during smoke you see something that suggests a sim-side bug, file a finding; do not modify.
- **Star-lord's seam (telemetry, export):** if exported skill records consume tier values directly, the values they consume will change. Flag in MIGRATION.md.
- **Drax (loadout, demo):** consumers of the season export (loadout) may see shifted magnitude ranges in the gear and skill displays. This is correct behavior; flag for drax only if the change is significant enough to warrant a comm note.
- **Validation against B10.4 Option 2 modifier band:** the NEXT regen after this lands SHOULD shrink the rage/physical modifier compression (closer to 1.0 from below). That validation belongs to a future gamora task — not this dispatch. Note expected direction in your math note for posterity.

## Required reading

- `agentic_orchestration/qa/findings/2026-05-16-gamora-modifier-range-rootcause.md` (the empirical basis for this dispatch)
- `reincarnated-engine/src/reincarnated/simulation/math/modifier-range-root-cause.md` (gamora's math note — full §4.3)
- `reincarnated-engine/src/reincarnated/generation/b6_archetype_templates.py` (your target file)
- `reincarnated-engine/design/decisions/decisions-log.md` 2026-05-16 entries (View A lock + divergence framework + calibration-epoch entry once it lands)
- `canonical/29-design-overview.md` § "shaped balance over numeric scaling" (philosophy; the tier shift IS shaped-balance, not numeric-scaling-at-the-skill-level)
- `~/.claude/projects/-Users-admin-Games-reincarnated-collaboration/memory/project_trait_architecture.md` (experimental-class trait note — relevant for Step 1 experimental exclusion)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Disciplines #1 (math-before-code), #2 (smoke-test), #11 (attribution), #12 (semantic-shifting — relevant: energy_type becomes a meaningful axis after this change)

## Open questions for rocket to resolve during the math note

1. Hunter archetype (avg modifier 0.594 — closest to target band; only miss-rate factor applies, no rage-startup, no melee-positioning): full 1.7× shift (treat as physical) or partial shift? Recommend with rationale grounded in the tier-addressable-mechanics framing from Step 0.
2. Hybrid archetypes: which side of the boundary? Probably partial shift; justify.
3. Round-numbers for tier breakpoints — propose clean values (e.g., 38–65 vs 40–70). Justify what aligns with existing tier-progression mathematics.
4. The proposed shift assumes rage/physical archetype templates currently exist with tier 25–50 bounds. Verify this empirically before sizing the change.

## Out of scope (explicit)

- Full B6 generation refactor (kit-builder, ability-grammar evolutions) — separate future dispatch.
- Sim-side energy-mechanic changes (e.g., starting rage gift) — explicitly rejected by gamora's investigation as the wrong fix.
- B14.5 V2 energy-type lever in primary recompose loop — gamora's seam, separate work.
- Stat distributions (Stage A1 lock — stats sum to 270) — unchanged.
- Trait architecture — unchanged.

---

## Completion record

**Completed:** 2026-05-16
**Math note:** `reincarnated-engine/src/reincarnated/generation/math/b6-pre-work-energy-tier-shift.md`
**Intermediate tag:** `rocket/v1.3-b6-energy-type-tiers` @ commit `639ac3d`
**Smoke status:** PASS — 5-class smoke season generated without errors; rogue (combo/58) avg_mag=2124 vs elemental mana avg 1200-1688; 104 tests passing (class_generation, b6_wired, ability_grammar, energy_types)
**MIGRATION.md entry:** NOT required — change is within existing field semantics (magnitude values in existing `magnitude` field); no schema-level change visible to sim consumers per ADR-004. Cross-seam flag filed in AGENT_STATE for gamora + star-lord awareness.
**Notes for knight-rider:** All four open questions resolved (see math note §3). Gamora should validate next regen shows physical_warrior modifier shifting from ~0.317 upward; hunter from ~0.594 upward. Expected post-B6 pre-work epoch: mean |mod-1.0| toward ~0.60-0.65 (full ~0.50 requires B14.5 V2). Milestone tag does NOT cut — await knight-rider + Matt confirmation per ADR-003.
