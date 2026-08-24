# Dispatch — 2026-08-24 — gamora — X-1 + X-2 (VFX-run cross-seam routings into the sim seam)

**Status:** PENDING — **routing, NOT a blocker on the Step-2 build wave.** Sequence at your convenience.
**From:** knight-rider (VFX archetype-binding run close, carve-out #2 § routings)
**To:** gamora (simulation seam)
**Approved by:** Matt, 2026-08-24
**Pattern:** B — **two independent parts. Part 1 is cheap and may land and tag ALONE. Do not let Part 2's weight hold Part 1.**

---

## Context

The VFX archetype-binding run **SEALED 2026-08-24**, binding 24 canonical VFX archetypes to **1,134** kit-skills (1,135 was the *assigned* count; 1,134 is the bound count post-hold — corrected by gandalf at L-41). In the course of that work it surfaced two findings that live in **your** seam, not in the presentation seam. The sealed spec names and routes them (§ 6.2, X-1 and X-2); it explicitly **does not write them** — *"Where a change must land in the engine, this document names the seam owner and routes it."*

Both landed in `simulation/` on inspection: `kit_compiler` and `spatial_engine` are yours.

**Neither blocks Step 2.** VFX authoring is unaffected by X-1 — the gap is in the run-time hit gauge, not the identity vocabulary. X-2 gates the *scoring* of one late-tier row, not the wave.

---

## PART 1 — X-1: `orbit` is absent from `kit_compiler._RICH_TO_SPATIAL`

**The finding:** `orbit` has no entry in `_RICH_TO_SPATIAL`, so **18 skills silently fall through to the `point` default** — where the sibling archetype `whirlwind` gauges `circle`.

⚠ **`MIGRATION.md` V9 is NOT corroboration — it is a second, different number.** V9's residual blocked bucket carries `geometry:orbit = 6`; the spec carries **18**. **Six and eighteen are not corroboration; they are two populations.** One is a T-K binding count, the other a generation census, and until someone states what each counts, neither is the count. My earlier framing called V9 "independent corroboration" — **that framing is withdrawn**; it is exactly the X-5 error (reading a field, inheriting it as a claim) applied to a number.

**Why it is not cosmetic.** `orbit` and `whirlwind` were ruled **DISTINCT** at charter L-29: *payload revolves* vs *character rotates* — a **different parent transform**. But an orbiting payload gauged as a `point` is gauged at the caster's position rather than across the ring its payload actually sweeps. That is an 18-skill hit-resolution question, and the silence is the dangerous part: a missing dict key produces a default, not an error.

### ⚠ The code is NOT in the state the finding above implies — Gate-1 verified this, and so did knight-rider

**`orbit → circle` ALREADY EXISTS in two of the three sites.** Confirmed by direct inspection:

| Site | State |
|---|---|
| `generation/geometry_derivation._RICH_TO_SPATIAL:477` — **the authoritative table** | ✅ has `orbit → circle` (Wave-C, `rocket/v2.11-wavec-3`) |
| `simulation/spatial_gauntlet/spatial_engine._RICH_TO_SPATIAL:1203` | ✅ has `orbit → circle` — **mirror-synced 2026-07-23, KF-5 Rider 1** |
| `simulation/kit_compiler/kit_compiler._RICH_TO_SPATIAL:52` | ❌ **missing `orbit`.** Has `placed_lane`. **The only stale site.** |

The spec's § 3.1.17 claim that `orbit` sits *"outside the engine's own `_RICH_TO_SPATIAL` keyspace"* **went stale on 2026-07-23.** Confirm all three yourself before touching anything.

**`orbit → circle` is therefore the CORRECT fix, not a hazard.** My original warning told you not to alias `orbit` onto `circle` — that warning pointed at the right answer, and it is withdrawn.

**Suspected mechanism — falsify it, do not assume it.** `kit_compiler.py:577-586` sets `spatial_geometry_type` **EXPLICITLY** on the skill dict specifically so the engine reads it via Path 1 and never consults its own mirror. If that holds, the compiler does not merely *default* an `orbit` skill to `point` — **it OVERRIDES the engine's already-correct `circle` derivation.** That is a worse defect than a missing key, and it is a hypothesis for you to prove or disprove.

**Fix the false comments WITH the code.** `kit_compiler.py:577-578` claims the map matches generation *"incl. the Wave-C placed_lane/orbit entries"* — it has `placed_lane`, not `orbit`. Line 580 calls the engine mirror *"stale… which lacks placed_lane/orbit"* — untrue since 2026-07-23. **Leaving those comments reproduces X-5's exact shape in code:** the next reader inherits a field as a claim. That is the error class this whole session has been tripping over; do not leave a fresh instance behind.

### ⚠⚠ THE REAL L-11-CLASS HAZARD IS `AOE_GEOMETRIES` — NOT the map

Charter L-11 names the error of **two deliberately-distinct things collapsing into one**. On this fix, that trap is not the spatial map. It is `generation/geometry_constants.AOE_GEOMETRIES`:

- A **16-entry frozenset that excludes `orbit` DELIBERATELY.**
- Two live sim consumers read it — `damage_resolver.py` and `combatant.py` — for the **B10.2 pack-proxy AOE multiplier** and the **GEOMETRY_COLLAPSE ×1.5** path.
- Its own module docstring: *"a SEPARATE, deliberately-different concept; do NOT conflate this set with it. Tightening membership would be a separate balance decision (out of scope here)."*
- `generation/AGENT_STATE.md:82`: *"AOE_GEOMETRIES DELIBERATELY UNCHANGED (balance decision deferred to S5)."*

**DO NOT add `orbit` to `AOE_GEOMETRIES`.** It will look like completing the fix. It is a **balance change against a locked deferral** — Principle 4 — and it is precisely the collapse L-11 names. If you believe `orbit` belongs there, that is a separate proposal to knight-rider, and it is a real one worth making; it is just not this dispatch.

### Scope — Part 1
- [ ] Confirm the gap empirically before changing anything: **grep the map, count the affected skills, verify the 18 against your own instrument.** The number came to you in prose; check it. (Discipline #19.1 — cheapest refuting test.)
- [ ] **Reconcile the 18 (T-K binding) against V9's 6 (generation census) — state what each counts — before treating either as the count.** If they measure the same population and disagree, that is a finding worth more than the fix. If they measure different populations, say which one the hit-gauge question actually turns on.
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

- jack-ryan Gate-1 DESIGN-MODE: **PASS-WITH-FINDINGS → **amendments applied 2026-08-24**** — Gate-1 batch review, 2026-08-24.
  Three-site verification table added (`orbit → circle` already exists in the authoritative table and the engine mirror; `kit_compiler` is the only stale site) — my original anti-aliasing warning was withdrawn; the real L-11 hazard relocated to `AOE_GEOMETRIES`; the false MIGRATION.md-corroboration claim withdrawn (6 ≠ 18; two populations, not corroboration) and a reconcile step added to Scope.
  Amendments approved by jack-ryan directly under **ADR-002** (dispatch documents are documentation-only). **Nothing in this batch escalated to Matt.**

---

## Completion record — gamora, 2026-08-24

**Part 1: COMPLETE, committed + tagged `gamora/v1.4-x1-orbit-spatial-map` (commit `45a0dc15`). Landed ALONE, not held by Part 2.**
**Part 2: SURVEY COMPLETE. Verdict = WIRING (mostly). NOT advanced to a build — returning to knight-rider per scope.**
**Push: NOT pushed (no push pattern set for this wave).**

### The three-site check — the table is CORRECT at all three sites

Re-derived from source, not inherited. `generation/geometry_derivation.py:485` ✅ and
`spatial_engine.py:1210` ✅ both carry `orbit → circle`; `kit_compiler.py:52` ❌ was the only
stale site. The sealed spec's § 3.1.17 "outside the engine's keyspace" claim did go stale on
2026-07-23. **No correction to the table is owed.**

⚑ **What the check DID find is the mechanism.** The dispatch's suspected mechanism is
**PROVEN** (probe, not reading): because `kit_compiler` stamps `spatial_geometry_type`
EXPLICITLY, the engine reads it via Path 1 and never re-derives. The missing key did not
*default* orbit to `point` — it **OVERRODE the engine's already-correct `circle`**. With the
stamp: `('point','explicit')`. Without it: `('circle','rich_type_translation')`. The worse of
the two failure modes.

### The 18-vs-6 reconcile CHANGED THE PICTURE — there are THREE populations, and 18 is not the one

| N | Counts | Tense |
|---|---|---|
| **6** | Wave-C **kits** that WILL be tagged at S5 by the new R8-orbit rule (`generation/MIGRATION.md:229`) | **FUTURE** |
| **18** | Existing corpus orbit skills at **ordinal 0** — the `primary_geometry` surface | present |
| **21** | Existing corpus orbit skills at **all** ordinals — the hit-gauge surface | present |

The 6 is **not a census at all** — it is a forward-looking plan count of kits a generation rule
will tag later. It and 18 never shared a tense, so the withdrawn "corroboration" framing was
withdrawn for an even stronger reason than stated.

**The 18 did not reproduce as the hit-gauge count.** My instrument found **21** orbit skills in
1,224 kit-skills, ordinal split `{0: 18, 1: 3}`. 18 is exactly the ordinal-0 subset, because
`primary_geometry` reads `skills[0]` only. **The hit-gauge question turns on 21** — the stamp is
applied at every ordinal. Three skills (`gd-belgothian-blademaster`, `le-warpath-vk`,
`vs-fuwalafuwaloo`) were mis-gauged *and* invisible to the primary-geometry assert.

### `AOE_GEOMETRIES` — trap avoided, and it is structurally unreachable

`orbit` NOT added. Beyond restraint: `AOE_GEOMETRIES` is keyed on the **rich** value
(`damage_resolver.py:1235,1317`; `combatant.py:988`); this change edits only the rich→**spatial**
map. Different vocabulary, different field — the change *cannot* reach it. B10.2 pack-proxy and
GEOMETRY_COLLAPSE ×1.5 unchanged, and now **asserted in smoke (P5)** rather than merely intended.
*(Minor: the docstring's "two live consumers" is right for sim; there are 2 more in generation —
all read the rich field, none affected.)*

### Smoke + round-trip

- `smoke_x1_orbit.py` (NEW): **18 GREEN / 0 RED.** All 21 orbit kits → `circle`; P4 corpus-wide
  before/after diff proves **exactly one** rich value moved and it is `orbit`; P6 all 26 shared
  keys agree across the three sites.
- **Round-trip clause SATISFIED, not waived** — shape is unchanged but a consumed field's *value*
  moves into the hit-gauge path. `d2-frozen-orb-sorc` → `run_spatial_fight`, field present, value
  `circle`, fight runs.
- `smoke_kf4_compiler`: **36 GREEN / 0 RED / 1 GAP — documented baseline exactly restored.**
- pytest geometry+spatial+compiler sweep: **235 passed.**
- Test skew closed: `acceptance.py` imports the *same symbol*, so pre-fix its EXPECTED was `point`
  from the same broken map — **it would have agreed with the bug.** Verified both now read `circle`.

### Judgement calls made (flagging, not burying)

- **`PILOT_KITS` not widened** — `emit_assert_sql.py` reads it to scope corpus SQL emission;
  widening it widens a **DB-write surface**.
- **An orbit kit was trialled in the kf4 roster and REMOVED.** All 21 orbit kits are
  damage-base-GAP, so it contributed a `primary_has_damage_base` RED unrelated to geometry that
  polluted a documented baseline. Orbit coverage lives in the dedicated smoke instead.
- **`generation/MIGRATION.md` NOT edited** — rocket's seam. Its "6 Wave-C kits" reads as a census
  but is future-tense; **routed, not patched.**

---

## PART 2 — X-2 survey. Verdict: **WIRING, not capability** — with one genuinely new piece

### ⚑ The cheap half paid off: enemy displacement ALREADY EXISTS and is proven in production

`spatial_engine.py:2378-2443` — the **Wave-D fear flee-AI** is a complete per-tick enemy
displacement mechanism:

- reads an `ActiveEffect` marker + params off `entity.combatant_state.active_effects`
- computes a **radial unit vector** relative to `nav_target` (`_dx = entity.x - nav_target.x` — outward)
- **mutates position per tick**: `entity.x += _flee_dx * _step`
- composes with `decrepify`, chill (`_f8_slow_factor`), `move_scale`
- clamps to arena, sets heading, and **short-circuits the behavior tree**

**`vortex_pull` inward displacement is this mechanism with the sign flipped.** The marker
plumbing, per-tick hook, composition chain, arena clamp and behavior-tree override all exist and
are exercised. That drops X-2 out of the "new capability" cost class.

### What genuinely does NOT exist (not overclaiming the above)

1. ⚑ **`on_vortex_pull` IS A PHANTOM.** `damage_resolver.py:1487` states the pull "is logged as
   metadata via the `on_vortex_pull` event fired in resolve_skill." **That event is fired
   nowhere** — repo-wide it occurs twice, both being that same comment (one a stale worktree
   copy). **This is X-5's error class again, in the same file family as X-1's false comments**: a
   reader asking "is the pull represented at all?" finds this and concludes yes-at-least-logged.
   It is not. `damage_resolver.py:1488` returns `1.0` with "no spatial model" — itself now stale,
   since `spatial_gauntlet` *is* a spatial model.
2. **Nothing ever applies a pull marker.** Fear's marker arrives via the ailment path; there is no
   equivalent for `vortex_pull`. The trigger half is missing.
3. **The one real new piece: a WORLD-ANCHORED attractor.** Fear's anchor is `nav_target` — an
   *entity*. A vortex's anchor is its **cast point**, which need not be the player's position.
   The engine has no notion of an attractor at a fixed world coordinate. This is the honest
   capability gap, and it is small.
4. **Impulse vs sustained-velocity semantics.** The declared `knockback` ailment
   (`config/ailments.yaml`, `hard_control`, `distance` 3-8 m, `stagger_seconds`) is a
   **displacement magnitude in metres**; fear's is a **speed multiplier**. Generation *emits*
   both params (`ability_grammar.py:708-711`); **the sim reads neither** (`stagger_seconds` has
   zero sim consumers). Which model a pull uses is a design decision, not an implementation detail.
5. **Centre behavior undefined** — fear flees outward without bound (arena-clamped); a pull
   converges, so the at-centre case must be specified.

### CC interaction — the dispatch's framing inverts

**A pull would not fight an existing CC resolver, because no CC resolver applies anything.**
`kc2/control_states.py` (my own B-2, landed 2026-08-24) builds the **delivery half only** — every
ledger row carries `applied: False` / `effect_model: DECLARED-ABSENT`, and limb E ("the effect")
is a NAMED OPEN (`MD-B2-2`), deliberately refused as "a choice of which switch to throw, with no
conservative direction."

So the hazard is **precedent, not conflict**: displacement would be the first control effect in
the sim to actually apply, setting the effect-application law ahead of the decode B-2 refused to
guess. Two further notes: (a) direction/lane differs — KC2's chain is monster→player, X-2's pull
is player→monster; the player-directed lane is the one governed by the I-24(c) kinematics policy
that "supersedes every non-drive limb", so pulling the **player** is where a real conflict lives.
(b) A pull should extend fear's composition chain, **not** open a second movement-override path —
two overrides is L-11's collapse in reverse.

### RT-6 disposition

Either outcome remains available. On this survey the dependency is **small and wiring-shaped**,
so "the engine dependency has landed" is a realistic option rather than a default to
"scored-with-dependency-named". **Not my call to make** — returning to knight-rider.

### NOT DONE, deliberately

No X-2 code, no math note. Dispatch: *"Do not build the feature in this dispatch without
returning to knight-rider first."* The verdict changes the cost class, which is exactly the input
that decision needs.

### Named opens routed to knight-rider

1. **→ rocket:** `generation/MIGRATION.md:229`'s "6 Wave-C kits" is future-tense and reads as a
   census. V10 clarification recommended. Not patched (his seam).
2. **→ elrond:** corpus `geometry_value` values **`mobility` (1)** and **`knockback` (1)** exist
   in **no** `_RICH_TO_SPATIAL` at any site and are absent from `VALID_GEOMETRY_TYPES`; they
   silently default to `point`. Not patched here — that would paper over an upstream vocabulary
   violation.
3. **Vocabulary finding:** orbit's swept region is an **annulus**; the 6-type vocabulary has no
   annulus primitive and `circle` has no inner-radius param. `circle` is an honest
   **approximation** (over-covers the interior disc), already canon at two sites — recorded so it
   is not later mistaken for exact.
4. **Balance proposal (NOT taken):** whether `orbit` belongs in `AOE_GEOMETRIES` is real and
   separate.
5. ⚑ **Stale/false comments in `damage_resolver.py:1484-1488`** (phantom `on_vortex_pull`, "no
   spatial model"). In my seam; not fixed in this commit because it is X-2 surface and X-2 is
   survey-only. **Flagging rather than silently touching.** Will fix on X-2 go, or as a standalone
   comment-truth commit on request.
