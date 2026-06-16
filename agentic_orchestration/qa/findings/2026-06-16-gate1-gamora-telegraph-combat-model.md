# Finding — 2026-06-16 — gate1-gamora-telegraph-combat-model

**Reviewer:** jack-ryan (DESIGN-MODE, Gate-1)
**Severity:** INFO (verdict: CLEAR-WITH-AMENDMENTS)
**Target:** commit `da80750` — `src/reincarnated/simulation/math/telegraph-combat-model-2026-06-16.md`
**Developer:** gamora
**Dispatch:** `agentic_orchestration/dispatches/2026-06-15-gamora-telegraph-combat-model.md` (telegraph dispatch 3, Phase 1)
**Principles applied:** Review #1 (math-before-code), #2 (smoke-gate — projected for Phase 2), #3 (cross-seam impact), #6 (cross-seam round-trip). Disciplines #1, #6/#11, #12. ADR-004.

## Verdict
**CLEAR-WITH-AMENDMENTS.** gamora proceeds to Phase 2 (implement). The orthogonality code-citation HOLDS on independent inspection; the TelegraphSpec is complete and faithful to the kernels. Amendments below are Phase-2 carries, none blocking.

## What I found — the orthogonality claim (gate condition 2), INDEPENDENTLY VERIFIED
I did not trust the citations; I read the code. The K4>=K2/M1 orthogonality claim holds:

1. **The four shape kernels read ONLY position + heading + per-shape constants.** `_compute_circle_hits` (`:519-521`) reads `attacker.distance_to(t)` + `radius`. `_compute_cone_hits` (`:530-544`) reads `attacker.x/y`, `attacker.heading_rad`, `CONE_RANGE_M`, `CONE_HALF_ANGLE_RAD`. `_compute_line_hits` (`:566-573`) reads `attacker.x/y`, `attacker.heading_rad`, `LINE_RANGE_M`, `LINE_WIDTH_M`. NONE references `player_gather_primitive`, `M1_GATHER_RADIUS_M`, KPM, or any clear-rate/credit term. Confirmed.
2. **The gather lever changes only the navigation TARGET POINT, never the shape function.** At `:1287-1299`, the gather flag (when True) reassigns `tgt_x, tgt_y` to the pack centroid; it then sets `player.heading_rad` and player position. When False (default), `tgt_x, tgt_y = nearest.x, nearest.y` — the constructor docstring `:1088-1095` and the navigation branch confirm the production path is BYTE-IDENTICAL with the flag off. The lever moves WHERE the player stands; it does not alter the function mapping (position, heading) -> footprint.
3. **The dispositive logic is sound.** Toggling the gather flag cannot change the danger-zone SHAPE produced at any given (position, heading) — it can only change which (position, heading) the player arrives at, which under temporal-decoupling is Godot's dodge surface, not the sim's exported geometry. The finding is an outcome-CREDIT/KPM-margin metric, orthogonal to shape production.

**Consequence:** the M1 gap does NOT touch the telegraph shape surface. The gate-phase fire-moment (W-C RESOLVE-clear, gandalf ruling `e906d63`) stands. No Tier-3 park to Matt is owed — orthogonality is confirmed, not contested.

## What I found — TelegraphSpec completeness + correctness, VERIFIED
Checked §2.3 against the dispatch "must capture" list and against the actual kernels:
- **Per-attack timing:** `fire_time_s` (seconds, canonical) + `fire_tick` + `wind_up_s`. `fire_time_s` = elapsed at resolution tick (`:1421` predicate) — matches the real resolution site. Complete.
- **Shape + extents for all four:** circle (`radius_m`), cone (`range_m`, `half_angle_rad`), line (`range_m`=length, `width_m`), point (degenerate marker). Each extent is minted FROM the kernel's own footprint constants — verified against `AOE_RADIUS_DEFAULTS`/`DEFAULT_AOE_RADIUS=3.5` (`:69-77`), `CONE_RANGE_M=5.0`/`CONE_HALF_ANGLE_RAD=π/4` (`:85-86`), `LINE_RANGE_M=20.0`/`LINE_WIDTH_M=1.5` (`:88-89`). NO re-computation, no drift source. Cone framing ("π/4 half = 90° full") is correct.
- **Fire-instant DYNAMIC heading:** `orientation_rad` = `attacker.heading_rad` at fire-instant, not the spawn default. Verified the kernels test the dynamic heading (cone `:538`, line `:566`) and heading is re-faced each step (`:1303`). The note correctly rejects the spawn heading.
- **Sim-invariant frame:** meters / radians (atan2) / seconds / bottom-left origin, declared IN the contract object (`spatial_unit`/`time_unit`/`angle_unit`/`frame_origin`) per A3-1. Identical to the kernel mint unit. The tile-vs-meter reconciliation note correctly pins meters as the SOURCE.
- **`damage_amount` + `attack_id` round-trip key:** `attack_id = f"{attacker.entity_id}:{skill_idx}"` — both fields exist at the resolution site (`entity_id` used `:1445`, `skill_idx` `:1422`); the key is constructible from real state.
- **§7.2 no-sim-dodge-term invariant:** RESPECTED. The resolution site (`:1421-1455`) resolves damage instantaneously with no avoidance branch; the TelegraphSpec is additive buffer-append metadata. The §3 wiring design adds no conditional on telegraph in the damage path.

## A3-1 / CL-3 amendments (dispatch-named) — ADDRESSED
- **A3-1 (pin the one unit-drift vector at source):** addressed — §2.0 declares meters as the single source unit, carried in the contract object, with the tile reconciliation note. Confirmed.
- **CL-3 (assert against the post-flag-and-defer dodge-gated baseline):** addressed in §3 — the §7.2 regression smoke asserts the `dodge-gated` flag from dispatch 1 is PRESERVED. This is a Phase-2 smoke obligation; design intent is correct.

## Amendments for Phase 2 (carries, non-blocking)
1. **`wind_up_s` default table is deferred to Phase 2 (§2.2).** The per-geometry default constant table is named but not pinned. Acceptable for a math-note (it is a calibration constant, not geometry). Phase 2 MUST pin it as a named constant table with a one-line rationale per shape, not inline magic numbers — Discipline #1 math-before-code applies to the constants too.
2. **The duplicate `v1.31` MIGRATION.md label (§4 housekeeping):** gamora flagged it and will disambiguate when authoring the telegraph MIGRATION section in Phase 2. Confirmed as Phase-2 scope; hold gamora to it so star-lord (dispatch 4) reads an unambiguous file.
3. **§7.2 regression smoke is the Phase-2 Gate-2 anchor.** The proof is asserted in design (buffer-append downstream of HP/damage/cooldown, byte-identical arithmetic). Phase-2 Gate-2 will require the actual smoke output (telegraphs on vs off → identical HP trajectory + win/loss + `dodge-gated` flag on the glass-close-ST exemplar) plus the code-cited ABSENCE of any avoidance term in the diff. Flagging now so it is not a surprise at Gate-2.

## Action
- [x] jack-ryan: Gate-1 CLEAR-WITH-AMENDMENTS — gamora proceeds to Phase 2 implementation.
- [ ] gamora (Phase 2): pin `wind_up_s` default constant table with per-shape rationale; disambiguate duplicate `v1.31` MIGRATION.md label; produce the §7.2 regression-smoke output + code-cited avoidance-absence for Gate-2.
- [ ] Matt: none — orthogonality confirmed, no Tier-3 park owed; fire-moment ruling (`e906d63`) stands.

## References
- `reincarnated-engine/src/reincarnated/simulation/math/telegraph-combat-model-2026-06-16.md` (the math-note reviewed)
- `reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py:514-602` (kernels + `_compute_aoe_hits`), `:60-93` (shape constants), `:1079-1095` + `:1280-1303` (gather lever), `:1421-1455` (resolution site), `:221-279` (geometry resolver)
- `agentic_orchestration/dispatches/2026-06-15-gamora-telegraph-combat-model.md`
- gandalf gate-phase ruling commit `e906d63`
