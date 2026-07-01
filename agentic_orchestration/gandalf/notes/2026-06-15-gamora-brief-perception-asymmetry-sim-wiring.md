# gamora brief — wire perception-asymmetry into the spatial battle sim (complete the design that fell through the spatial-rebuild seam)

> **⚠ SUPERSEDED IN PART — Matt-ruled 2026-06-30 (F2 hinge).** The **battle sim is SYMMETRIC** — player and enemy resolve AOE on the same radius, no edge in the balance math. The perceptual edge is granted at the **control layer** (human-piloted = full edge; AI-piloted = reduced edge) as a **piloted-Godot layer-handoff** (sibling to `dodge_gated_deferred`), **controller-keyed** not role-keyed. This **supersedes §2/§5 (edge-in-sim, role-keyed constants) and re-homes the §6 WR-falsifier to the piloted layer.** What SURVIVES: wiring the `AoeCastEvent` producer in `spatial_engine.py` (§1 gap) — but emitting `apparent = true` (spillover 0 = honest "sim granted no edge"), damage untouched. Constants stay in `foundation/perception_asymmetry.py` as the spec the piloted layer consumes. Full ruling: `canonical/matt_decision_needed/README.md` RESOLVED appendix (Q1). Read this brief as lineage for the two-layer *design*; read the ruling for the *implementation split*.

**Type:** direct gandalf→gamora brief (Matt is the conduit to gamora's session; NOT a KR dispatch).
**Date:** 2026-06-15
**Author:** gandalf (story-and-design steward)
**Authority:** Matt-authorized 2026-06-15 — *"regardless of if it's in the emitter, it should be pushed all the way back into the battle sim regardless."* This brief executes that directive.
**Parent:**
- `canonical/story/asymmetric-perceived-aoe-radius-briefing-2026-05-17.md` — THE DESIGN (gandalf L3 binding v1.5; the two-layer model). This is not new design; it is wiring an existing, locked design.
- `reincarnated-engine/src/reincarnated/foundation/perception_asymmetry.py` — the MODULE to consume (rocket's; already built, fail-loud guarded).
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` #16 — tuning-drift guard; the constants are gandalf-locked.

---

## 0. One line

The player-favoring perception asymmetry is **designed + foundation-built + demo-wired + telemetry-schema-built** — but the R2 spatial-gauntlet rebuild never carried it into `spatial_engine.py`, which resolves all AOE symmetrically. Wire the two-layer model into the spatial sim so the gauntlet's win-rate verdicts inherit the genre-standard player advantage the real game will deliver, and so the **already-built `aoe_cast_events` telemetry table finally gets a producer.** This is completing an existing design, not inventing one.

## 1. The gap (code-cited — the precise state)

| Layer | State |
|---|---|
| Design contract | EXISTS — `asymmetric-perceived-aoe-radius-briefing-2026-05-17.md` + Discipline #16 |
| Foundation module | EXISTS — `foundation/perception_asymmetry.py`: `ENEMY_AOE_APPARENT_RATIO=1.12` (`:56`), `PLAYER_AOE_APPARENT_RATIO=0.90` (`:61`), `enemy_apparent_radius()`/`player_apparent_radius()`/`get_apparent_radius()`, `_validate_constants()` fail-loud |
| Demo | WIRED — `perceptionAsymmetry.ts`; `main.ts:1016` sizes enemy AOE indicators at apparent (1.12×) |
| Telemetry SCHEMA | EXISTS — `aoe_cast_events` table (`migrations.py:700-703`, V2.5 `:1112`), `AOECastEvent` dataclass (`telemetry/aoe_cast_event.py`) with `true_radius_hit_count` + `apparent_radius_hit_count`, recorder write path (`recorder.py:1052-1067`), D14-calibration spillover consumer spec |
| Telemetry PRODUCER | **MISSING** — `AOECastEvent` is **never constructed anywhere in `simulation/`** (grep empty). The table is a schema with no producer; nothing writes a row. The migration even tags the intended emitter "gamora narrow-slice" — tied to the pre-spatial combat path. |
| Spatial sim (`spatial_engine.py`) | **NOT wired at all** — `_compute_circle/_cone/_line_hits` (`:514/:524/:560`) + `_compute_aoe_hits` (`:577`) use raw skill radii symmetrically; the `skill_ready` gate (`:854-861`) is `nearest_dist <= range_m` with no apparent/true split; player-proxy nav uses `preferred_range_m` symmetrically. No `apparent_radius`, no ratio constants, no import of the module. The ONLY importer of `perception_asymmetry` anywhere in `src/` is `foundation/__init__.py` (a re-export). |

**Lineage (why it fell through the seam):** the asymmetry stack was built in the 2026-05-17 narrow-slice-telegraphed-combat era. The R2 spatial-gauntlet rebuild (2026-05-19) replaced that combat path and was built without the asymmetry. The telemetry emitter, tagged "gamora narrow-slice," was never re-authored for the spatial loop. So ~80% of the work is staged and waiting; the missing 20% is the spatial-engine wiring.

## 2. The two-layer model (from the briefing — do not re-derive)

- **`true_radius`** — the geometric distance at which **damage resolves. Never fudged.** The spatial engine already resolves damage at true — **do not change damage resolution.**
- **`apparent_radius`** — the distance at which **AI reacts** (and, in the demo, indicators render). Enemy: `true × 1.12` (danger oversold). Player: `true × 0.90` (offense undersold).

## 3. Where the asymmetry enters the spatial sim (the design INTENT — I own this; you own the wiring POINT)

The headless sim has no renderer, so the asymmetry enters at the **AI-decision layer**:

- **Enemy AOE (the load-bearing half — this is what changes fight outcomes):** the player-proxy's avoidance/positioning treats enemy danger zones at `enemy_apparent_radius` (1.12×, *bigger* than true) → the proxy leaves the oversold margin → it eats fewer enemy AOE hits than the true zone would inflict. Damage still resolves at true (1.0×). This models the genre-standard advantage a human gets dodging an oversold telegraph.
- **Player AOE (the "got-em-too" half):** design intent is player-favoring spillover. In a headless sim the player-apparent UNDERsell (0.90×) is fundamentally a *render* concept (pleasant-surprise for a human watching their indicator). The sim-faithful default is the proxy's targeting uses **true** radius (it fires when true-radius hits → full offensive value). Whether to ALSO model a conservative-commit-at-apparent is a real modeling choice — **surface it in the math-note; do not silently pick.**
- **Division of authority:** I (gandalf) own the DESIGN INTENT — player-favoring on both halves, constants locked. You + jack-ryan own the exact WIRING POINT in the engine. Surface the player-AOE-commit choice as an explicit decision; don't pre-impose.

## 4. The three connected wiring pieces

1. **AI-decision uses apparent** (the load-bearing change) — proxy avoidance reads `enemy_apparent_radius`; targeting per § 3.
2. **Damage stays at true** (no change to damage resolution).
3. **Emit `AOECastEvent`** at the damage tick — compute `true_radius_hit_count` AND `apparent_radius_hit_count`, write the row. This **fills the waiting telemetry table** → D14 calibration finally gets its spillover signal (`true_hit − apparent_hit` for player AOEs = "got 'em too"; `apparent_hit − true_hit` for enemy AOEs = "barely escaped"). You are the named emitter; this completes your own staged schema.

## 5. Constraints (do NOT re-open these)

- **Constants are gandalf-locked** (Discipline #16): enemy `1.12 ∈ [1.08, 1.18]`, player `0.90 ∈ [0.85, 0.93]`. **Consume** them from `foundation/perception_asymmetry.py`; do not redefine or re-tune. The fail-loud guard stays. Any change requires gandalf sign-off — not in scope here.
- **Do not touch the demo** (already wired) or the constants module (rocket's). Engine↔demo constant parity is already established; preserve it.
- **Damage resolution stays at true_radius.** The asymmetry is a decision-layer + telemetry overlay, never a damage change.

## 6. Re-validate (known-direction prediction — recognition → validate → commit)

Wiring this should shift player WR **slightly UP** vs the current symmetric baseline, concentrated on enemy-AOE-heavy scenarios (the proxy avoids the oversold enemy zone). **Register the prediction:** WR delta is positive, small (~few %), concentrated where enemy AOE matters.

- **Falsifier:** if player WR moves DOWN or not at all, the wiring is wrong — the asymmetry MUST favor the player on net. Surface it; don't ship a wiring that fails the direction check.
- **Context:** this stacks with the already-logged sim conservatism (decisions-log:1240 — the movement-speed-blind sim already under-credits player margin; "real gameplay closes the gap further"). Perception-asymmetry is another axis where the symmetric sim is conservative vs real gameplay. Wiring it makes the gauntlet's verdicts more faithful, not just more genre-correct.

## 7. Sequencing relative to the live KR engine run (IMPORTANT — clean attribution)

**This fires AFTER the in-flight b6/rogue role-floor chain closes — not concurrently.** Reason: the asymmetry shifts player WR up ~few %, and the rogue role-floor fix is validated by a WR-based G7 HOLD-SIM re-pass. Wiring the asymmetry mid-rogue-validation would confound the signal — you couldn't tell whether rogue clears the upper tiers because of the role-floor fix or the asymmetry's WR boost. One-variable-at-a-time discipline: land + validate the rogue fix on the **current symmetric baseline** first (closing the b6-deletion gate), THEN wire the AOE asymmetry as its own measured increment with the § 6 prediction. It is **not on the critical path** of the current run and blocks nothing.

## 8. Roles / acceptance

- **gamora:** author the sim math-note (the wiring points: proxy avoidance at enemy_apparent; targeting at true; the player-AOE-commit choice surfaced; the `AOECastEvent` emission) → jack-ryan Gate-1 → implement → measure the WR delta vs symmetric baseline.
- **jack-ryan Gate-1:** sim semantic change (Discipline #12) + Discipline #16 tuning-drift (constants consumed, NOT re-tuned) + the engine↔demo parity obligation.
- **gandalf:** design-review that the wiring matches intent (player-favoring on net; constants untouched; the WR delta direction + magnitude).
- **Acceptance:** spatial sim consumes `perception_asymmetry`; `aoe_cast_events` gets a producer; WR delta is positive-small in the predicted direction; constants unchanged; Gate-1 clear.

---

**Signed:** gandalf, 2026-06-15
**For:** executing Matt's directive to push the perception-asymmetry near-miss mechanic into the battle sim — the design + module + demo + telemetry-schema all exist and predate the R2 spatial rebuild, which never carried the asymmetry forward (`spatial_engine.py` is fully symmetric; `AOECastEvent` is a schema with no producer); wire the two-layer model at the AI-decision layer (proxy avoids enemy AOE at apparent 1.12×, damage resolves at true), emit the waiting telemetry rows for D14, keep the gandalf-locked constants untouched, predict a small player-favoring WR shift, and sequence it AFTER the in-flight b6/rogue chain so it doesn't confound the role-floor G7 validation.
