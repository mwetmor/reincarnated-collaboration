# Rollup Tables — V1 Plane View

> Discipline: assignments grounded in substrate-coordinates.md §1 Axis 2 definitions;
> judgment calls flagged inline. UNMAPPED = genuinely unmappable; never silently bent.

## Table 1: 24→5 Geometry Rollup (Plane A dispersion-v1 families)

Axis 2 families (substrate-coordinates §1): `single` · `chain` · `small_aoe` · `large_aoe` · `multi_spawn`
Ordering rule: `dispersion-v1` (spec §2.3) — single → chain → small-AOE → large-AOE → multi-spawn.

| geometry_value (24-type rich palette) | → Axis 2 Family | Flag | Reasoning |
|---|---|---|---|
| `dash_attack` | **single** | def | Melee-range single contact; footprint 1, no aoe spread |
| `ground_slam` | **single** | def | Footprint 1 impact point despite short cone — classic single in genre (D2 Smite / PoE Leap Slam pattern) |
| `melee_arc` | **single** | judgment | Narrow arc; footprint effectively 1 target per swing in corpus use — filed single vs small-AOE; judgment: genre precedent favors single for tight-arc melee |
| `melee_strike` | **single** | def | Axis 2 def: one impact, melee geometry; footprint 1 |
| `single_target` | **single** | def | Axis 2 def: one impact point |
| `chain` | **chain** | def | Axis 2 def: chain = sequential hops |
| `fork` | **chain** | judgment | Fork = projectile that splits on hit (2 branches); sequential-hop pattern closer to chain than single; judgment: fork is chain-subtype, not AOE |
| `multi_projectile` | **chain** | judgment | Multiple simultaneous projectiles = canonical chain-pattern precursor (D2 Multi-Shot, PoE Barrage); footprint = multiple traveling points; dispersion per-hop not per-region; judgment: chain over large_aoe because the volley radiates from one cast-point sequentially/simultaneously — not a contiguous region |
| `ricochet_bounce` | **chain** | def | Axis 2 def: chain = one moving point, sequential hops; ricochet is the canonical chain exemplar |
| `beam_channel` | **small_aoe** | judgment | Beam = sustained linear region; footprint long but narrow; judgment: small-aoe vs single — more than one point but not wide; filed small-aoe over single for multi-target line |
| `cone` | **small_aoe** | def | Axis 2 def: compact region; cone is bounded forward sweep |
| `line` | **small_aoe** | def | Line AoE = narrow compact region (lightning bolt, ice lance) |
| `vortex_pull` | **small_aoe** | judgment | Pull vortex draws targets into 1 location; effective footprint compact; judgment: small-aoe vs single — multi-target impact but compact; filed small-aoe |
| `whirlwind` | **small_aoe** | def | Spinning melee aura = compact constant region around caster; small-AOE by extent |
| `aura` | **large_aoe** | judgment | Aura = persistent omnidirectional radius = large constant region; judgment: large-aoe vs multi-spawn — no separate entity spawned; filed large-aoe |
| `circle` | **large_aoe** | def | Axis 2 def: wide region; circle is the canonical large-aoe shape |
| `ground_targeted_circle` | **large_aoe** | def | Axis 2 def: wide region; circle at target = arena-covering in genre usage (Blizzard, Meteor, Desecrate) |
| `ring` | **large_aoe** | judgment | Ring = expanding/fixed large radial region; judgment: large-aoe vs multi-spawn — ring IS the damage region, not spawns; filed large-aoe |
| `self_buff` | **multi_spawn** | judgment | Self-buff kits in corpus are companion/minion-empowering passives; judgment: multi-spawn proxy — UNMAPPED-LEANING but best-fit is multi-spawn given proxy dimension. Flagged: 5 kits; if kit has no damage geometry it should be UNMAPPED |
| `totem` | **multi_spawn** | judgment | Totem = persistent autonomous entity that fires independently; judgment: multi-spawn; identical to 'standing army' archetype in spec §2.1 |
| `NULL` | **UNMAPPED** | judgment | NULL geometry = geometry not keyed; cannot be placed |
| `teleport` | **UNMAPPED** | judgment | Teleport is mobility, not damage geometry; cannot be mapped to Axis 2 dispersion without knowing primary damage skill |

**Note on `multi_projectile` (judgment):** 41 corpus kits carry this type. Filed as `chain` — canonical chain-pattern precursor (D2 Multi-Shot, PoE Barrage). See table row above. Alternative mapping `large_aoe` would apply if the volley fans wide rather than traveling as discrete bolts — a per-kit call, not resolvable at geometry_value grain alone.

---

## Table 2: Plane B Delivery-Family Mapping

Parsed from Matt's mock SVG `reap-die-rise-atlas-chart-mock.svg` — text elements verbatim:

**Column headers (8 columns, left→right):**
> `➤ PROJECTILE` · `◎ ORBITAL` · `✳ NOVA` · `▒ ZONE` · `━ BEAM` · `✕ MELEE` · `☍ SUMMON` · `◯ RING`

**Row headers (3 rows, top→bottom):**
> `SNAP` · `WIND-UP` · `CHANNEL`

**Plane B row → commit enum mapping:**
> `SNAP` = instant · `WIND-UP` = wind-up · `CHANNEL` = channel

| Plane B Column | Maps to geometry_value(s) | Flag | Notes |
|---|---|---|---|
| **PROJECTILE** | `single_target`, `multi_projectile`, `fork`, `ricochet_bounce`, `chain`, `line` | def | Maps to: single_target, multi_projectile, fork, ricochet_bounce, chain (sequential), line — the traveling-entity family |
| **ORBITAL** | `ring`, `vortex_pull`, `whirlwind`, `aura` | judgment | Maps to: ring, vortex_pull, whirlwind, aura — rotating/orbiting persistent region; OVERLAP with RING column |
| **NOVA** | `circle`, `ground_targeted_circle` | judgment | Maps to: circle, ground_targeted_circle — instant burst; OVERLAP with ZONE (both accept circle types) |
| **ZONE** | `ground_targeted_circle`, `circle`, `cone` | judgment | Maps to: ground_targeted_circle, circle, cone — placed ground regions; OVERLAP with NOVA |
| **BEAM** | `beam_channel` | def | Maps to: beam_channel only — narrow sustained linear; clean mapping |
| **MELEE** | `melee_strike`, `melee_arc`, `dash_attack`, `ground_slam` | def | Maps to: melee_strike, melee_arc, dash_attack, ground_slam — contact range |
| **SUMMON** | `totem`, `self_buff` | def | Maps to: totem, self_buff — autonomous spawned entities |
| **RING** | `ring` | judgment | Maps to: ring only; judgment: OVERLAP with ORBITAL (ring appears in both families in mock) |

### Overlap flags

Plane B has intentional column overlaps absent in Plane A:
- **NOVA vs ZONE:** Both claim `circle` and `ground_targeted_circle`. In the render, these kits are assigned to first-listed column (NOVA) to avoid double-counting — true split would require per-kit sub-geometry.
- **ORBITAL vs RING:** Both claim `ring` geometry. In the render, these are assigned to ORBITAL first. RING column receives only kits unambiguously ring-only (none in corpus after ORBITAL takes priority).
