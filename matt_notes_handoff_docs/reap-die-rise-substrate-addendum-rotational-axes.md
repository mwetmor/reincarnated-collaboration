# Reap. Die. Rise. — Substrate Addendum: Rotational Motion-Frame Axes

**Audience:** the build team (Claude agent team on the Mac).
**Status:** addendum to the mechanic coordinate space (~64K decomposition). Extends trajectory vocabulary with the frame-relative rotational family. Integrates with `reap-die-rise-agnostic-loot-system.md` (§1.3 transform operators, §6 coverage search, §7 fairness bands, blacklist) and the battle sim.
**The gap being closed:** the substrate covered linear/targeted/homing motion but had no frame-relative rotation — orbitals, spirals, swirling auras, spin channels, wandering rotators, orbiting emitters. Genre evidence (verified): PoE Blade Vortex (10-blade orbit, per-blade scaling, detonation synergy), D4 Gravitational-Aspect Ball Lightning (orbit conversion with damage trade, 10-ball cap), Last Epoch's five orbital node-transforms (Dark Moon, Hammer Vortex, Burning Dagger, Blade Shield, Orbital Fulmination) + Ring of Shields, D2 Blessed Hammer (spiral-out), survivor-like staples (King Bible, Garlic, orbiting emitter birds), bullet-hell rotating emitters.

---

## 1. The Seven Sub-Axes

| # | Axis | Domain | Notes |
|---|---|---|---|
| 1 | **reference_frame** | `caster_body` \| `cast_point` \| `autonomous` \| `parent_entity` | `cast_point` = Blessed Hammer frame (does not follow the caster). `autonomous` composes with EXISTING trajectory axes for the frame's own motion (wander = LE Tornado, seek = Vaal Blade Vortex) — composition, not new axes. `parent_entity` = nested orbits (orbiters around a projectile/orbiter). |
| 2 | **angular_velocity ω** | signed deg/s | 0 = static satellite ring. v1: constant. Time-varying ω (accelerating spin) → v2. |
| 3 | **radial_velocity dr/dt** | signed units/s | 0 = orbit · positive = spiral-out (Hammerdin) · negative = spiral-in/collapse (optional center event via collision_mode). |
| 4 | **orbiter_count + phase_spacing** | int + distribution (uniform default) | Genre caps ≈10 (PoE, D4). Our cap = min(fairness band, perf band) — see §4. |
| 5 | **persistence_mode** | `duration` \| `while_channeling` \| `stack_refresh` \| `until_consumed` | `stack_refresh` = BV pattern: each cast adds an orbiter with its own timer; count is the resource. |
| 6 | **collision_mode** | `pierce_tick(rate)` \| `detonate_on_contact` \| `block_incoming` | BV ticks at 0.6s. `block_incoming` = defensive orbital (Ring of Shields / interceptor) — cross-system with projectiles; recommend **v2**. |
| 7 | **emission_hook** | `none` \| `radial_spawn(cadence)` \| `tangential_release(trigger)` \| `detach_and_seek(trigger)` | Sub-projectiles are ordinary substrate projectiles; recursion via `parent_entity`. **Recursion depth cap: 2** (perf + legibility). |

## 2. Degenerate Identities (compression wins — do not build these separately)

- **Swirling aura** (Garlic, Sweeping Wind, Maelstrom, Hurricane) = orbiter_count → ∞ ≡ annular zone tick. **Compile rule:** count above threshold ⇒ implement as zone, render as rotation.
- **Spin-to-win** (Whirlwind, Cyclone, Warpath, Eye of Reckoning) = frame `caster_body`, radius ≈ melee reach, the body is the orbiter, `while_channeling` + `pierce_tick`; body translates freely.
- **Nova / expanding ring** = ω 0, dr/dt positive, high count — the existing nova mechanic is a point in THIS family; unify the representation.
- **Stationary satellite turret** (Winter-Orb-shaped) = ω 0 (or low), `radial_spawn`.

One parametric family therefore covers Garlic → Hammerdin → Blade Vortex → Touhou emitters, and absorbs novas and spin channels the substrate already had.

## 3. Loot Integration: the "Orbitize" Transform Operator

New legendary-class transform operator per loot doc §1.3:

> **ORBITIZE** — *"Your [structural slot: primary projectile ability]'s projectiles orbit you instead of traveling. −X% damage."*

- Mechanics: sets frame `caster_body`; ω from default band; radius derived from the ability's existing range axis; damage scalar trade (genre precedent −10..−25% — D4 Gravitational Aspect).
- Precedent proves the pattern: Last Epoch implements orbit as a **node transform on base projectile skills** (Hammer Throw → Hammer Vortex) — i.e., our operator model already shipped in a competitor. Archetype-agnostic by construction (operates only on universal trajectory axes).
- Pipeline: passes §6 coverage search and §7 cross-kit fairness band like any operator. Candidate **fixed-name marquee legendary**. Family extensions (spiral-out conversion, detach-and-seek conversion) noted but **one shipped operator in v1**.

## 4. Sim & Validation Requirements

1. **Orbital-aware hit accounting.** Orbital DPS is geometry-dependent (angular alignment × target rings × radius vs. density). Gauntlet must sample density regimes (sparse / ring / surround). AOE% attribution for orbitals = **swept-annulus coverage per second**, not cast-shape area.
2. **Pre-registered degenerate combos → blacklist candidates before first run:**
   - orbit-stack + detonate-all (the published PoE BV + Blade Blast pattern);
   - emission recursion stacking (orbiters spawning orbiter-spawners — hence the depth cap);
   - spiral-in + detonate on dense packs (free full-pack hit);
   - block_incoming vs. projectile-heavy kits (defensive uptime unfairness) — deferred with v2 anyway.
3. **Caps are dual bands.** orbiter_count cap = min(fairness band, **M2 perf band**) — N orbiters × M entities of collision checks; provisional cap 8–12 pending profiling; orbiter VFX get LODs per the asset pipeline.
4. **Fun-signal calibration.** Orbitals are density-loving and low-APM (always-on spatial control). Expect a different fun-σ signature than skillshots; calibrate so the spatial fun signal doesn't penalize low input cadence — the survivor-like genre proves the fantasy is real.

## 5. Emission Plumbing

- Allocate axis IDs; **emission weight: orbital-flavored kits are a minority flavor** (visual legibility at horde density — too many orbital kits on screen is soup). Provisional weight pending first gauntlet review.
- VFX: orbiters map to the composable slot model — travel slot = the orbital loop; trail/glow LODs mandatory.
- Naming layer (loot doc §5.1 rule — name must signal mechanic): orbit vocabulary (Ring-, Halo-, Vortex-, Waltz-, Grave-…). Function first, flavor second.

## 6. Open Decisions

- v2 axes: time-varying ω; elliptical orbits (eccentricity); orbit-plane tilt (likely render-only at ARPG camera); `graze` collision (bullet-hell near-miss reward).
- `block_incoming` ship decision (cross-system projectile interception) — recommended v2.
- Final orbiter cap + emission weights after first orbital gauntlet batch.

## 7. What Was Missing Before (do not regress)

The trajectory vocabulary had no reference-frame concept — all motion was world-frame. This addendum introduces frame-relative motion as a first-class dimension; novas and spin channels should be **migrated into** this family rather than kept as separate mechanics, or the coordinate space will carry duplicate representations of the same physics.
