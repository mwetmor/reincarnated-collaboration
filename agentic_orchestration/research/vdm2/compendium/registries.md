# VDM-2 Compendium — Registries (global reference)

> **v2.0** · db md5 `bebc933b0bf9bcab5988bbc16bcc55b4` · generated 2026-07-22T09:46:42Z. Read-only render of the two global registries the per-kit blocks reference. `door_registry` resolves each kit's `mapping_json.t4_doors` tokens; `motion_signature_registry` resolves each skill band's `motion_signature`.

## door_registry (28)

| door_name | status | rfc_ref | description |
|---|---|---|---|
| `COMPANION_CONTRACT` | active | — | Binds a persistent autonomous companion (falcon/wolf/beast) to the player as a contracted delivery proxy; its count/behavior scales off dedicated companion affixes (LE-native beastmaster/falconer family). |
| `DEFENSIVE_TRADEOFF` | active | — | Trades a defensive stat for offensive power (or vice-versa). |
| `DUAL_PROXY` | active | — | Spawns proxy clones that mirror the caster's skills from their own spatial origins. |
| `ELEMENTAL_ECHO` | active | — | Trigger-family door: a host action triggers a payload skill (e.g. Cast-on-Crit). |
| `ELEMENT_CONVERSION_HYBRID` | active | — | Converts a skill's damage into a hybrid of two elements (e.g. fire+physical melee). |
| `ELEMENT_CONVERSION_MONO` | active | — | Converts a skill's damage to a single target element. |
| `ELEMENT_CONVERSION_PHYSICAL` | active | — | Converts a skill's damage to/from physical. |
| `GEOMETRY_COLLAPSE` | active | — | Collapses delivery geometry (e.g. shotgun-density / burst-around-self). |
| `GEOMETRY_PROPAGATION` | active | — | Propagates delivery geometry across the pack (chain/fork/cascade family). |
| `GEOMETRY_PROPAGATION_cascade` | active | — | Cascade variant: geometry propagates in a forward-marching cascade. |
| `GEOMETRY_PROPAGATION_overkill` | active | — | Propagation via overkill spill: excess/lethal damage chains onward (corpse-explosion/detonation cascade). |
| `MOMENTUM_CASCADE` | active | — | Momentum/build-up that cascades into escalating output. |
| `NETWORK_AMPLIFIER` | active | — | Amplifies via a network of linked effects (brands/links). |
| `PERSISTENCE_ENGINE` | active | — | Sustains a persistent effect while a resource/summon is active. |
| `PERSISTENCE_ENGINE_saturation` | active | — | Persistence via saturating overlapping zones/DoTs. |
| `PERSISTENCE_ENGINE_uptime` | active | — | Sustains a defensive/utility effect while a resource/summon is active. |
| `PHASE_MOMENTUM` | active | — | Movement/phase momentum that powers the loop. |
| `PROXY_ASCENSION` | active | — | Places autonomous emitter proxies (totem lane) that act on their own. |
| `PROXY_CONVERGENCE` | active | — | Many proxies converge fire on a point/target. |
| `PROXY_FISSION` | active | — | Splits into many small proxies/minions (fission). |
| `PROXY_INVERSION` | active | — | Inverts the proxy relationship (host becomes proxy or vice-versa). |
| `PROXY_SOVEREIGNTY` | active | — | A dominant proxy governs subordinate proxies. |
| `RESONANCE_LOOP` | active | — | Self-reinforcing resonance loop (trigger feeds itself). |
| `RESOURCE_CONVERSION` | active | — | Converts one resource into another (life-as-mana, etc.). |
| `RETRIBUTION_ENGINE` | active | — | Reactive retribution (damage returned on being hit/blocking). |
| `SACRIFICE_ASCENDANCY` | active | — | Self-sacrifice/self-damage as the power source. |
| `TEMPORAL_CHARGE` | active | — | Accumulate-then-discharge charge economy (build stack, dump stack). |
| `ZONE_CONTROL` | active | — | Controls/denies a zone of the battlefield. |

## motion_signature_registry (18)

| signature_name | engine_impl_ref | description |
|---|---|---|
| `arc_sweep` | — | Melee arc sweeps a sector in front of the attacker (cleave/swing). |
| `blink_translate` | — | Instant point-to-point positional translate (teleport-class movement). |
| `burst_around_self` | — | Nova/ring bursts radially outward from the origin point. |
| `chain_hop` | — | Bolt/effect hops target-to-target across a pack (chain geometry). |
| `fan_spread` | — | A-3: radial fan / sector spray (e.g. GD Stun Jacks 180-degree point-blank spread). |
| `fork_split` | — | Projectile splits into diverging bolts at a fork point. |
| `ground_place` | — | Effect is placed at a targeted ground point (trap/mine/brand/rain). |
| `inward_pull` | — | Radial inward pull that draws enemies toward a focal point. |
| `lane_place` | — | A placed straight damaging lane laid on the ground (firewall/trap-lane). |
| `leap_arc` | — | Travel-then-slam leap: airborne arc terminating in an AoE landing. |
| `mortar_arc` | — | Projectile lobs on a ballistic arc to a target point. |
| `orbit_fixed` | — | Effect orbits a fixed point (player or anchor). |
| `point_strike` | — | Single-point melee/slam impact at the targeted enemy/ground. |
| `ricochet_return` | — | Out-and-back projectile: homes on the target, bounces target-to-target through the pack, then returns to its origin (distinct from chain_hop one-way and fork_split diverging — this one returns). |
| `sine` | — | Projectile follows a sinusoidal path. |
| `spiral_out` | — | Projectile spirals outward from origin. |
| `straight_line` | — | Projectile travels a straight vector from origin. |
| `wall_sweep` | — | Effect sweeps as a wall/line across an area. |

