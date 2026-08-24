# Dispatch — 2026-08-24 — gamora — X-1 + X-2 (VFX-run cross-seam routings into the sim seam)

**Status:** PENDING — **routing, NOT a blocker on the Step-2 build wave.** Sequence at your convenience.
**From:** knight-rider (VFX archetype-binding run close, carve-out #2 § routings)
**To:** gamora (simulation seam)
**Approved by:** Matt, 2026-08-24
**Pattern:** B — **two independent parts. Part 1 is cheap and may land and tag ALONE. Do not let Part 2's weight hold Part 1.**

---

## Context

The VFX archetype-binding run **SEALED 2026-08-24**, binding 24 canonical VFX archetypes to 1,135 kit-skills. In the course of that work it surfaced two findings that live in **your** seam, not in the presentation seam. The sealed spec names and routes them (§ 6.2, X-1 and X-2); it explicitly **does not write them** — *"Where a change must land in the engine, this document names the seam owner and routes it."*

Both landed in `simulation/` on inspection: `kit_compiler` and `spatial_engine` are yours.

**Neither blocks Step 2.** VFX authoring is unaffected by X-1 — the gap is in the run-time hit gauge, not the identity vocabulary. X-2 gates the *scoring* of one late-tier row, not the wave.

---

## PART 1 — X-1: `orbit` is absent from `kit_compiler._RICH_TO_SPATIAL`

**The finding:** `orbit` has no entry in `_RICH_TO_SPATIAL`, so **18 skills silently fall through to the `point` default** — where the sibling archetype `whirlwind` gauges `circle`. Corroborated independently by `MIGRATION.md` V9 (`geometry:orbit` = 6, residual blocked bucket).

**Why it is not cosmetic.** `orbit` and `whirlwind` were ruled **DISTINCT** at charter L-29: *payload revolves* vs *character rotates* — a **different parent transform**. But an orbiting payload gauged as a `point` is gauged at the caster's position rather than across the ring its payload actually sweeps. That is an 18-skill hit-resolution question, and the silence is the dangerous part: a missing dict key produces a default, not an error.

**Watch for the failure class this belongs to.** Charter L-11 caught a structurally similar error in a `_RICH_TO_SPATIAL` merge hop — two distinguishable geometries collapsing into one selection. Verify you are not *creating* that error while fixing this one: `orbit` must not simply be aliased onto `circle` if the swept region differs.

### Scope — Part 1
- [ ] Confirm the gap empirically before changing anything: **grep the map, count the affected skills, verify the 18 against your own instrument.** The number came to you in prose; check it. (Discipline #19.1 — cheapest refuting test.)
- [ ] Math-before-code note: what spatial primitive `orbit` *should* gauge and why, stated as geometry — including whether the swept annulus is representable in the 6-type spatial vocabulary at all, or whether `orbit` is honestly approximated
- [ ] Land the mapping; keep `acceptance.py`'s expectation consistent with `kit_compiler`'s (they import the same symbol — a fix in one place that misses the other is a silent test skew)
- [ ] Smoke-test proving the 18 skills now gauge as intended, and that **nothing else moved**
- [ ] Reconcile `MIGRATION.md` V9's residual blocked bucket
- [ ] Tag `gamora/v<X.Y>-x1-orbit-spatial-map`

---

## PART 2 — X-2: `vortex_pull` readability requires engine-side enemy displacement

**The finding:** `vortex_pull` (15 skills / 15 kits, T3) **cannot be validated on VFX alone.** No effect the presentation seam mints can supply the inward vector — the archetype's readability is carried by **enemies actually moving inward**. The spec is explicit that this is `AUTHOR-not-SELECT`: we own zero attractor and zero particle-collision content, so its reference is a *spec*, not a pack selection.

**This ties to a live pre-registered trigger, RT-6:** when the minted gate reaches this row, it is **not scored against the VFX rubric in isolation.** Either the engine dependency has landed, or **the row is scored with the dependency named as the limiting factor.** Both are acceptable outcomes — which one happens depends on this part.

**Do the cheap half first.** Before designing anything: **does the sim already have a displacement primitive?** Forced movement may exist under another name (knockback, pull, reposition, forced-move). If it does, X-2 may be a *wiring* question rather than a *capability* question, and that changes its cost class entirely. Answer that before proposing a build.

### Scope — Part 2
- [ ] **Survey first:** does an enemy-displacement / forced-movement primitive already exist in the sim? Report the answer either way, with the code evidence.
- [ ] If it exists: state what wiring `vortex_pull` would need, and the cost
- [ ] If it does not: **math-before-code first** — the displacement model (inward vector, magnitude, duration, what happens at the centre, interaction with existing movement/CC resolution). **Do not write code before this note exists.**
- [ ] **Do not build the feature in this dispatch without returning to knight-rider first.** A new sim capability with CC-adjacent interactions is a scope decision, not a routing consequence.
- [ ] Flag any interaction with the KC2 hard-CC work — a pull that fights an existing CC resolver is a design question, not an implementation detail

---

## Cross-seam contract change? (Principle 6 gate)

**Part 1: potentially YES.** `_RICH_TO_SPATIAL` output feeds compiled fighter `primary_geometry`, which crosses into the sim/telemetry path.
- **Required if the compiled output shape or any consumed field changes:** `Round-trip smoke: production-path kit fixture containing at least one `orbit` skill → `kit_compiler` → compiled fighter → the spatial/hit-gauge consumer boundary, with a field-presence and value check on `primary_geometry`.`
- If the change is purely a dict-key addition with no consumer-visible field change, state: `Round-trip: not applicable because <explicit reason>` — **silence on this field is a Gate-1 BLOCK** per REVIEW_PROCESS Principle 6.
- **MIGRATION.md required** per ADR-004 if any consumer-visible surface moves.

**Part 2: TBD** — survey-only as dispatched; if it advances to a build, the round-trip clause is authored then.

## Acceptance criteria

- [ ] X-1: gap confirmed empirically (not inherited from prose), mapping landed, smoke green, `MIGRATION.md` V9 residual reconciled, round-trip clause satisfied or explicitly not-applicable
- [ ] X-1 tagged independently — **it does not wait on Part 2**
- [ ] X-2: survey answered with code evidence; wiring-vs-capability verdict stated; math note if capability
- [ ] X-2 does **not** advance to a build without knight-rider concurrence

## Quality criterion

**Game-quality goal:** that a skill's *hit resolution matches what the player sees*. An orbiting payload that visually sweeps a ring but mechanically resolves at a point is exactly the read-what-you-see contract breaking — and telegraph literacy is worth nothing if the telegraph lies about where the damage lands. X-2 is the same contract from the other side: a vortex that visually pulls but mechanically does not is an effect that *decorates* rather than *causes* — the run's named failure mode, expressed in the sim.

**Refutation conditions** (surface to knight-rider before executing if any apply):
- The 18-skill count does not reproduce against your instrument — the finding needs re-derivation, not implementation
- Mapping `orbit` correctly requires a spatial primitive the 6-type vocabulary does not contain — a vocabulary finding, worth more than a forced approximation
- X-2's displacement conflicts with an existing CC/movement resolver — a design question, escalate
- A fix in `kit_compiler` without the matching change in `acceptance.py` would let the test agree with the bug

## Out of scope

- Any VFX authoring (presentation seam)
- Re-opening T-A or the L-29 `orbit`↔`whirlwind` distinctness ruling — **sealed law; HALT to Matt**
- Building X-2's capability without concurrence
- The F-2 kit re-mapping lap (elrond, future)

## References

- Sealed spec § 6.2 (X-1, X-2) · § 3.1.17 (`orbit`) · § 3.1.19 (`vortex_pull`) · § 6.1 RT-6
- Charter L-11 (the merge-hop error class), L-12 (POST-run routing pattern), L-29 (distinctness), L-30
- `src/reincarnated/simulation/kit_compiler/kit_compiler.py` · `acceptance.py` · `spatial_gauntlet/spatial_engine.py` · `generation/MIGRATION.md` V9

---

## Gate record

- jack-ryan Gate-1 DESIGN-MODE: **pending at authoring time** — Gate-1 batch review, 2026-08-24.
