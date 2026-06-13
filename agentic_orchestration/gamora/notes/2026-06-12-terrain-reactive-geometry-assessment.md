# Terrain-reactive geometry — boundary assessment (Item 5)

**Author:** gamora
**Date:** 2026-06-12
**Dispatch:** `agentic_orchestration/dispatches/2026-06-12-gamora-proxy-kernel-handoff.md` § 5
**Status:** ASSESSMENT (not an implementation item). Informs Session 3 scope decision.
**Premise (code-verified):** terrain-reactivity is **GREENFIELD**. Confirmed by code read — see § 0.

---

## 0. Code-state baseline (what exists)

| Surface | What it does | Damage / element / CC? |
|---|---|---|
| `spatial_gauntlet/arena.py:104` `ChokeZone` | Clamps **x-movement** to `[x_min, x_max]` for entities whose **y** is in `[y_min, y_max]`. Bottleneck modeling without pathfinding. | **None.** Pure positional clamp (`clamp_position`). Zero damage/element/CC interaction. |
| `fight_engine.py:55-57` "zone" | Comment labels for the three distance BANDS (close/mid/far). | N/A — naming only, not a spatial zone. |
| `fight_engine.py:1255` `p.zone_effect` | Proxy `ProxyZoneEffect` (Item 1/2) — player-buff / debuff field applied by a minimal-tier proxy. | Buff/debuff to a combatant, **not** terrain. Caller-attached entity, not arena geometry. |

There is **no `terrain_type`, no `zone_type`, and no terrain/zone concept of any kind in the 1D `simulate_fight` kernel.** The only spatial-zone object in the entire sim (`ChokeZone`) lives in the **2D** spatial gauntlet and is movement-only. The original draft's "already implements terrain-reactive geometry" claim is retracted (confirmed by the normalization pass).

**Load-bearing split:** the 1D kernel has scalar `distance_m` and no position. Terrain is inherently a 2D/positional concept. Any terrain-reactive DAMAGE/CC mechanic that depends on "where you are standing" has no 1D substrate — it can only exist (a) in the 2D spatial gauntlet, or (b) as a position-independent caller-side parameter that a 1D fight inherits as a flat per-fight condition.

---

## Q1. Is `ChokeZone`'s zone-position infrastructure reusable as the substrate for terrain ZONES with damage/CC semantics, or is a separate terrain-zone model cleaner?

**Partially reusable for the geometry; a separate model is cleaner for the semantics.**

`ChokeZone` already solves *position-in-zone testing* (`y_min ≤ y ≤ y_max` → membership). That membership predicate is the reusable kernel — a terrain zone needs the same "is this entity inside this rectangle?" test, generalized from a y-band to a full `(x,y)` AABB.

But `ChokeZone`'s *effect* is hardwired to one action (clamp x). A terrain zone with damage/element/CC semantics carries a fundamentally different payload: an effect descriptor (damage-per-tick, element tag, CC-duration modifier, damage-amp-on-match) applied to entities **inside** the zone each tick. Bolting that onto `ChokeZone` would overload a movement primitive with combat semantics — a semantic-shift smell.

**Recommendation:** factor a small shared membership primitive (`Zone.contains(x, y) -> bool`, AABB), let `ChokeZone` keep its movement payload, and introduce a **separate `TerrainZone`** carrying an effect descriptor. Two zone types, one membership test. This keeps `ChokeZone`'s movement semantics untouched (golden-master-safe) and gives terrain its own clean effect surface. This is a **2D spatial-gauntlet change**, not a 1D-kernel change.

## Q2. Is terrain-reactivity implementable as a **caller-side parameter** (`terrain_type` kwarg per Session 3 § 3.2) with skill-tag checks at damage resolution, or does it require a new fight_engine branching path?

**Two distinct sub-cases — the answer splits by whether the mechanic is positional.**

- **Position-INDEPENDENT terrain-reactivity (flat per-fight condition)** — "this whole fight takes place on `lava` terrain; fire skills get +X% and the enemy's CC-resist is −Y%." This is cleanly **caller-side** in the 1D kernel: a `terrain_type: str | None = None` kwarg on `simulate_fight`, read at damage resolution via a skill-tag/element check (mirrors exactly how `enemy_cc_mult` / `cc_duration_mult` already route through `damage_resolver`). It is the **same shape as the Item 3 companion-modifier pattern** — a caller-supplied multiplier the resolver reads. Minimal, brownfield-safe (`None` ⟹ no-op ⟹ 0/60 golden-master), and it requires **no new branching path** beyond a single guarded multiplier at the existing `buff_dmg_mult` site (cf. the charge-stack §6.3 passive-bonus precedent — one guarded line).

- **Position-DEPENDENT terrain-reactivity (zone you can step into/out of)** — "stand in the fire patch → take damage; cast from high ground → +range." This has **no 1D substrate** (no position). It requires the 2D spatial gauntlet's `TerrainZone` (Q1) plus a per-tick in-zone effect application loop. That is a **spatial-gauntlet change**, and within the spatial gauntlet it is closer to a new dispatch path than a caller kwarg (the per-tick zone-membership × effect application is structural, akin to the proxy dispatch loop).

**Recommendation for Session 3:** prefer the **position-independent caller-side `terrain_type` kwarg** as the v1 terrain-reactivity surface — it covers "terrain flavors the fight" (element affinity, CC modifiers, damage-on-match) with the cheapest, brownfield-safe kernel surface and reuses the Item 3 caller-modifier idiom. Defer position-dependent terrain zones to a spatial-gauntlet `TerrainZone` item only if a design requirement genuinely needs *steppable* terrain (a higher-cost, structural change).

## Q3. Does the current fight_engine have ANY concept of "terrain type" or "zone type" that damage modifiers can reference? What is the minimum kernel surface to add terrain-type as a fight parameter?

**No** — confirmed (§ 0). The 1D kernel has zero terrain/zone concept; the only zone object anywhere (`ChokeZone`) is 2D and movement-only.

**Minimum kernel surface** for position-independent terrain (the recommended v1):
1. `simulate_fight(..., *, terrain_type: str | None = None)` — one keyword-only param, default `None` (brownfield: `None` path bit-identical → 0/60 golden-master).
2. A caller-side / config terrain table mapping `terrain_type` → `{element_affinity_bonus, cc_duration_mult, damage_amp_on_match, ...}` (rocket/design supplies magnitudes; **kernel reads, never chooses** — same contract as charge-stack kit data and companion modifiers).
3. **One guarded multiplier** at the `damage_resolver` `buff_dmg_mult` site (and/or the control-duration site for CC terrain), keyed on a skill element/tag match against the terrain descriptor. Guarded by `terrain_type is not None` ⟹ dead code for every existing fight.

This is **caller-side-preferred and kernel-light** — structurally identical to the two precedents already landed in this dispatch (Item 3 companion vector; Item 4 charge-stack passive bonus). It is **not** a kernel-change-protocol-heavy item in the position-independent form. Position-dependent terrain (steppable zones) is the only variant that escalates to a structural spatial-gauntlet change.

---

## Bottom line for Session 3 scope

- Terrain-reactivity is greenfield; nothing to retrofit.
- **Position-independent terrain** (terrain flavors the whole fight): **caller-side `terrain_type` kwarg + one guarded resolver multiplier.** Preferred. Brownfield-safe. Reuses the Item 3 / Item 4 caller-supplied-magnitude idiom. Recommend as v1.
- **Position-dependent terrain** (steppable zones): a **2D spatial-gauntlet `TerrainZone`** built on a generalized AABB membership primitive (factored out of `ChokeZone`, which stays movement-only). Higher cost; structural. Recommend deferring unless a design requirement needs steppable terrain.
- The Q1 membership-primitive refactor and the Q2 caller-kwarg are **independent** — Session 3 can ship the caller-side `terrain_type` flavor without touching `ChokeZone` at all.
