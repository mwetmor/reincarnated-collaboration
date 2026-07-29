# WR1-ENV — Room-sizing envelope spec from the banked WR1-BATTERY-2 traces

**Run:** WR1-2026-07-28 · **Cell:** WR1-ENV (gamora) · **Conductor:** gandalf · **Authority:** R-WR1-17 (Matt-signed), charter §8.20
**Date:** 2026-07-29 · **Consumer:** drax (Godot multi-room level sizing)
**Class:** evidentiary note. READ-ONLY extraction — zero engine-repo writes (WR1-BATTERY-3 was concurrently active in that tree).

---

## ⚑ HALT — read this before reading the table

The brief's framing states: *"the sim is open-field, traces have no walls; a tighter room depicts collisions the sim never resolved."*

**Measured: false.** The traces carry a hard **36.0 × 36.0 m arena** (`header.frame.arena_width_m / arena_height_m`) and entity positions are **clamped to `[radius, arena − radius]`**. The clamp is not incidental — **it binds, hard, and it decides fights**:

| tier | fights where the player touches a wall | share of player-alive ticks spent pinned to a wall | walls hit |
|---|---|---|---|
| trash | 90 / 90 (100%) | 51.99% | S |
| champion | 1 / 90 (1%) | 0.06% | S |
| mixed_pack | 90 / 90 (100%) | 75.33% | S + E |
| boss | 180 / 180 (100%) | 75.03% | S + W (**SW corner**) |

In **179 of 180 boss fights** the player spends a median **70.8%** of its ticks standing on the exact point `(0.5, 0.5)` — the southwest corner, both axes clamped simultaneously. Median first wall-touch is **t = 11.8 s** of a **54.2 s** fight; the player is then cornered for a median **42.2 s**, i.e. **78%** of the fight.

**The mechanism** (trace `boss__B__seed74000802`, verified as the shared shape): the player closes to melee on the boss's bearing (t=0 → 1.5 s), then executes a back-off/re-approach melee cadence whose net is a **monotone straight-line drift** along the reverse of the approach bearing at ~1.5–2.0 m/s, with the boss glued at 1.6–2.0 m separation. The drift does not orbit and does not reverse. It terminates only when the player hits the arena corner and can go no further. The fight is then resolved in the corner.

**Consequence for R-WR1-17.** The rule says *rooms CONTAIN the fight envelope, never constrain it.* It presumes the envelope is a free-field quantity. It is not: **the banked envelope IS a constraint artifact.** The observed 29.58 × 27.23 m boss envelope is a *lower bound* on an unbounded envelope, not a measurement of one. Under a linear-drift extrapolation (drift measured on the free phase, continued through the pinned interval) the *unbounded* boss floor diagonal would be a median **≈109 m** (p95 130 m, max 135 m) and mixed_pack **≈72 m** (p95 78 m). Those numbers are **estimates, not measurements**, and they are **not build targets** — they describe a movement-policy artifact, not a design intent.

**So R-WR1-17 cannot be satisfied and violated at the same time, and the resolution is:**

> **The sim's own arena, 36 × 36 m, is the container.** It is the only floor size that both (a) contains everything the traces show and (b) reproduces the fight the traces actually resolved. A room *smaller* than the containment floor cuts the kite earlier than the sim did — forbidden by R-WR1-17. A room *larger* than 36 × 36 lets the drift run past where the sim stopped it — which does not violate R-WR1-17, but **does mean the banked win rates, durations and damage distributions no longer describe that room.**

This is routed to the conductor as an **unmodeled condition**, not silently resolved. Two candidate readings are live and I do not own the choice:

- **Reading A (fidelity):** build 36 × 36 m clear floor for boss/mixed_pack. The banked numbers transfer exactly. The corner-pin is depicted, because the corner-pin is what happened.
- **Reading B (containment-purist):** build the per-tier containment floor below, and accept that the boss fight in-room will differ from the banked fight the moment the player reaches a wall earlier than t=11.8 s. Requires a re-run to re-bank durations/outcomes.

The table below gives **both**. My recommendation is **Reading A for boss and mixed_pack** (the wall is load-bearing there) and **the containment floor is sufficient for champion** (the wall is touched in 1 fight of 90, for 0.3 s — genuinely incidental). Trash sits between: 100% of fights touch the S wall, but for a 2.9 s tail of a 5.9 s fight, and the mob spawn ring dominates the box regardless.

---

## 1. Instruments

All instruments banked (meta-repo, not the engine tree) at
`agentic_orchestration/gamora/notes/2026-07-29-wr1-envelope-spec-support/`:

| instrument | what it produced |
|---|---|
| `wr1_envelope_extract.py` | pass 1: per-fight bounding boxes, separations, telegraph radii |
| `wr1_envelope_extract2.py` | pass 2: absolute bbox coords, radius-inflated boxes, spawn-vs-movement split, per-leg/per-arm blocks → `wr1_envelope_pass2_output.json` (banked alongside) |
| `wr1_clamp_probe.py` | arena-boundary occupancy census (**the HALT finding**) |
| `wr1_boss_probe.py` | player↔boss separation distribution, corner-pin fraction, nova telegraph origins |
| `wr1_boss_traj.py`, `wr1_path.py` | trajectory reconstruction — established drift-not-orbit |
| `wr1_unbounded.py` | linear-drift extrapolation of the unbounded envelope (**ESTIMATE, not a build target**) |
| `wr1_radii.py` | per-tier entity radii + skill geometry/range census |

**Substrate:** `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/output/kitcal_g5/wr1_battery_2/` — 450 traces at `g5-replay-trace/v1`, engine `7f77ea0`, all 450 parsed, none skipped.
**Percentile estimator:** nearest-rank, 1-based, `k = ceil(q·m)` — matched to the battery's own convention (`wr1_battery2_statistics.json` §G_A) so figures compose with the banked record.

**Occupancy definition (stated because it is a choice):** a fight's occupied point set = every entity's spawn point (all entities occupy their spawn before frame-0 resolution, including entities killed at t=0) ∪ every `(entity, tick)` position where `alive = true`. Dead entities' frozen carcass positions after death are excluded. **"Inflated"** boxes add each entity's own `entity_radius_m` — that is the swept *surface* extent, i.e. the floor bodies actually cover. All recommendations below use inflated boxes.

---

## 2. What does NOT vary

- **Spawn geometry is deterministic per tier.** All 30 seeds share identical spawn coordinates: a mob ring of radius 8.4 m about `(15, 15)` with the player at `(15, 3.0)` for trash/champion; ring radius 10.08 m about `(18, 18)` with the player at `(18, 3.6)` for mixed_pack/boss. Seed varies combat RNG only. **The envelope therefore has almost no seed spread** — median and max coincide on most metrics. Treat these as fixed formation constants, not as a sampled distribution.
- **The three legs are spatially identical.** `pre` (R2_proxy) / `pre_endpoint` (R2_proxy_resists_low) / `post` (R3) produce byte-identical envelopes at every tier; the M-1/M-2/M-3 deltas are damage-side only. **Durations and outcomes DO differ by leg** — reported in §5. No per-leg envelope reporting is needed.
- **Boss arms A and B are spatially identical** (29.58 × 27.23 m both). Arm B lives longer (median 57.2 s vs 38.7 s) and therefore spends longer cornered; it does not go anywhere new.

---

## 3. Movement bounding boxes (radius-inflated, metres)

| tier | player-only W × D (med) | mobs-only W × D (med) | **combined envelope W × D (med)** | **combined W × D (max)** | envelope diagonal (max) |
|---|---|---|---|---|---|
| trash | 8.82 × 5.02 | 16.80 × 22.90 | **18.22 × 23.90** | **20.73 × 23.90** | 31.64 |
| champion | 13.83 × 6.91 | 17.50 × 22.51 | **19.81 × 23.51** | **22.15 × 23.90** | 32.30 |
| mixed_pack | 19.20 × 5.52 | 27.27 × 26.23 | **28.58 × 27.23** | **28.58 × 27.23** | 39.48 |
| boss | 22.29 × 10.43 | 26.45 × 25.21 | **29.58 × 27.23** | **29.58 × 27.23** | 40.20 |

(player/mob sub-boxes are centre-based; combined is inflated. Combined ≠ union of the two sub-boxes because of the radius inflation.)

**Decomposition — how much is formation, how much is combat.** Spawn-footprint box vs. combined envelope:

| tier | spawn footprint W × D | combined envelope W × D (max) | movement adds |
|---|---|---|---|
| trash | 16.80 × 20.40 | 20.73 × 23.90 | +3.93 × +3.50 |
| champion | 16.80 × 20.40 | 22.15 × 23.90 | +5.35 × +3.50 |
| mixed_pack | 20.16 × 23.13 | 28.58 × 27.23 | +8.42 × +4.10 |
| boss | 15.12 × 23.13 | 29.58 × 27.23 | +14.46 × +4.10 |

**The spawn ring is the dominant term at every tier.** Combat movement adds 17–24% in width and 15–18% in depth. Boss is the exception in width (+96%) — and that increment is precisely the SW drift to the corner. *If drax changes the spawn formation radius, the envelope moves one-for-one; these numbers are not portable across a different formation.*

---

## 4. Player ↔ opponent separation

**Pooled across all opponents**, per-fight statistic then summarised across fights:

| tier | median sep (med across fights) | p95 sep (med / max across fights) | max sep (all fights) |
|---|---|---|---|
| trash | 4.45 | 13.71 / 13.71 | 17.88 |
| champion | 1.32 | 11.89 / 11.89 | 13.71 |
| mixed_pack | 1.72 | 16.32 / 16.62 | 22.93 |
| boss | 1.60 | 9.83 / 16.08 | 22.77 |

### 4a. ⚑ The ~5.62 m standoff orbit is NOT in the traces

The brief expects a **~5.62 m** standoff orbit (`wr1_battery2_statistics.json → standoff_context.sim_native_standoff_r_star_m = 5.617`, itself already flagged there as *"FALSIFIED as a fixture descriptor"* by WR1-GAL-3's 1.26 m measurement).

**Measured player↔BOSS separation, pooled over 83,937 entity-ticks across all 180 boss fights:**

```
p5  1.600   p25 1.600   p50 1.600   p75 1.652   p95 1.986   p99 13.141
min 1.555   max 17.051  mean 1.933
per-fight median: 1.600 (max across fights 1.706)
per-fight max:    17.051 (identical in all 180 — it is the t=0 spawn separation)
```

The realised engagement separation is **1.600 m centre-to-centre**, flat, in every fight. The p99 = 13.14 tail is the opening approach run, not an orbit. **There is no orbit.** With boss radius 1.5 + player radius 0.5 = 2.0 m of combined body, a 1.600 m centre separation means the capsules **interpenetrate by 0.40 m** for the majority of every boss fight — the sim resolves no body collision between combatants.

**Load-bearing for drax:** a Godot boss room where the boss and player have real collision bodies **cannot reproduce 1.600 m centre separation**. The floor is 2.0 m. Either the capsules must be allowed to overlap, or the melee-contact geometry differs from the banked fight. This is a third unmodeled item and I am flagging it rather than assuming a resolution. It is also the reason the 5.617 figure should be retired from consumer-facing use entirely: three different numbers (5.617 declared, 1.26 measured by GAL-3 at death 2, 1.600 measured here as the modal engagement) are in circulation for one quantity.

---

## 5. Boss-tier specifics

**Nova footprint — CONFIRMED at 12 m, with a caveat.**
- 132 radius-bearing telegraph events across the battery, **all** at `shape: "circle", radius_m: 12.0`. Single-valued; no spread. **Footprint diameter = 24.0 m.**
- All 132 are boss-tier. 132 of 180 boss fights carry exactly one nova; **48 boss fights carry zero** — consistent with the battery's own banked "8 of 30 seeds produce ZERO nova crossings" (8/30 × 180 = 48). ✓
- **All 132 fire from the identical origin `(25.917, 15.094)` at t = 1.55 s.** The nova is a fixed early event at a fixed point, not a repeating positional threat. Room design should not assume the nova follows the boss.
- ⚑ **Declared-range / telegraph-radius mismatch:** the boss's skill record reads `primordian_frigidring_r4, geometry: circle, range_m: 10.0`, but its telegraph emits `radius_m: 12.0`. Two numbers for one skill's reach in the same trace. **Use 12.0** — the telegraph is the resolved footprint. The 10.0 is flagged for the conductor as a fourth unmodeled item.
- **The nova footprint overflows the arena.** Origin `(25.917, 15.094)` ± 12 m spans `x ∈ [13.92, 37.92]`, `y ∈ [3.09, 27.09]`. The east edge, **37.92 m, exceeds the 36 m arena by 1.92 m** — the banked nova was clipped. A room ≥ 24 m in each dimension holds one nova; a room that places the boss spawn within 12 m of a wall clips it as the sim did.

**Standoff orbit — NOT confirmed.** See §4a. Measured 1.600 m flat, not ~5.62 m, and it is a contact-line, not an orbit.

**Total floor a boss fight sweeps.** 29.58 × 27.23 m inflated (40.20 m diagonal), invariant across all 180 fights, all 3 legs, both arms. Absolute extent `x ∈ [0.5, 28.08]`, `y ∈ [0.5, 26.73]` — the low edges being exactly the player radius confirms the clamp. Path length of a single median boss fight is ~36 m of player travel for ~17.5 m of net displacement.

**Longest resolved reach in the battery** (a hard floor on any room's minor dimension, independent of the envelope): `slitha_shaman_c01_attack`, `point`, **18.0 m**. The player's own `rip_and_tear_r16` is `line`, **14.0 m**. A room narrower than 18 m silently truncates an opponent skill that the sim resolved at full reach.

---

## 6. Fight durations (restated from the artifact, per §8.20's self-containment requirement)

| tier | min | median | p95 | max | outcome (450 traces) |
|---|---|---|---|---|---|
| trash | 5.0 | 5.9 | 6.8 | 6.8 | player 90/90 |
| champion | 5.9 | 6.8 | 7.7 | 7.7 | player 90/90 |
| mixed_pack | 21.3 | 24.8 | 26.6 | 26.6 | player 90/90 |
| boss | 16.0 | 54.2 | 64.3 | 67.1 | **monster 104 / player 76** |

Boss durations by leg — the one place legs diverge materially:

| leg | median | max | outcome |
|---|---|---|---|
| `pre` (R2_proxy) | 47.8 | 67.1 | monster 46 / player 14 |
| `pre_endpoint` (R2_proxy_resists_low) | 38.6 | 63.5 | monster 58 / player 2 |
| `post` (R3) | 58.1 | 59.0 | **player 60 / 60** |

Arm A median 38.7 s, arm B median 57.2 s. **Room dwell-time budget for a boss encounter: 16–67 s, plan for ~60 s.**

---

## 7. Containment margin rule

**Rule:** `clear_floor(dim) = envelope_inflated_max(dim) + 4 × R_max(tier)`, rounded UP to the next 0.5 m.
That is **2 × R_max of margin per side**, where `R_max` is the largest `entity_radius_m` present in the tier (0.50 m for trash/champion/mixed_pack; **1.50 m** for boss — the Primordian).

**Why 2R per side, in two terms:**
1. **One R — body clearance.** The traces record entity *centres*, but the inflated envelope already adds each entity's own radius, so term 1 is not double-counting the envelope: it is the allowance for a body arriving *at* the envelope edge in a room with real collision, which needs its own radius of standoff to sit fully clear of the wall rather than be pushed through it.
2. **One further R — passability.** A gap of `2R` is exactly one body width: the minimum through which a chaser can path *between* the envelope edge and the wall. Anything less re-creates, in Godot's collision solver, the jam that the sim resolved by silently clamping — which is precisely the "depicts collisions the sim never resolved" failure R-WR1-17 forbids.

The rule is deliberately **not** a percentage. The envelope is dominated by a fixed spawn ring (§3), so a percentage margin would scale with formation size rather than with body size, and body size is what the containment failure is about.

---

## 8. ▶ SUMMARY TABLE — read this cold

| tier | median envelope (W × D m) | max envelope (W × D m) | margin/side | **containment floor** (min clear, m) | **recommended build** (m) | duration band |
|---|---|---|---|---|---|---|
| **trash** | 18.22 × 23.90 | 20.73 × 23.90 | 1.0 | **23.0 × 26.0** | 23.0 × 26.0 | 5.0 – 6.8 s (med 5.9) |
| **champion** | 19.81 × 23.51 | 22.15 × 23.90 | 1.0 | **24.5 × 26.0** | 24.5 × 26.0 | 5.9 – 7.7 s (med 6.8) |
| **mixed_pack** | 28.58 × 27.23 | 28.58 × 27.23 | 1.0 | **31.0 × 29.5** | **36.0 × 36.0** ⚑ | 21.3 – 26.6 s (med 24.8) |
| **boss** | 29.58 × 27.23 | 29.58 × 27.23 | 3.0 | **36.0 × 33.5** | **36.0 × 36.0** ⚑ | 16.0 – 67.1 s (med 54.2) |

⚑ = **the wall is load-bearing in this tier** (75% of player-alive ticks pinned; the boss fight is decided in the SW corner). Build the sim's own 36 × 36 m arena so the banked outcomes transfer. The containment floor column is the R-WR1-17-literal minimum; for these two tiers it is *smaller than the arena the sim used*, and building to it re-cuts the fight.

**Additional hard floors applying to every room regardless of tier:**
- **≥ 18.0 m** in the minor dimension — longest resolved opponent reach (`slitha_shaman_c01_attack`). All four rows satisfy this.
- **≥ 24.0 m** in each dimension for any room hosting the boss — one nova footprint (12.0 m radius). Boss row satisfies this.
- **Boss spawn should sit ≥ 12.0 m from every wall** if the nova is to land unclipped. In the banked arena it does not (origin `x = 25.917` is 10.08 m from the east wall) — the banked nova is clipped by 1.92 m. Reproduce or fix, but do it deliberately.

**Portability caveat:** every number here is conditioned on the battery's fixed spawn formation (§2). Change the formation radius and the envelope moves one-for-one.

---

## 9. Items routed to the conductor as UNMODELED

1. **The sim is not open-field.** A 36 × 36 m clamped arena exists and binds in 100% of trash / mixed_pack / boss fights. R-WR1-17's premise does not hold; the rule cannot be applied literally to boss/mixed_pack without changing the fight. Readings A and B offered in the HALT section; I do not own the choice.
2. **No standoff orbit.** Measured player↔boss separation is 1.600 m flat (n = 83,937 ticks), not ~5.62 m. The 5.617 figure should be retired from consumer-facing use; three numbers (5.617 / 1.26 / 1.600) are in circulation for one quantity.
3. **Combatant capsules interpenetrate** by 0.40 m for most of every boss fight. A Godot boss with real collision cannot reproduce the banked melee geometry.
4. **`primordian_frigidring_r4` declares `range_m: 10.0` but telegraphs `radius_m: 12.0`** in the same trace. Spec uses 12.0.
5. **The nova footprint is clipped by the arena** (east overflow 1.92 m) in all 132 firings.

---

*Produced read-only. No engine-repo writes. WR1-BATTERY-3 was concurrently active in that tree and was not touched.*
