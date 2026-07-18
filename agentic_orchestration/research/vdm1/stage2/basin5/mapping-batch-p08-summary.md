# VDM-1 basin-5 mapping batch-p08 summary — vs-a (12 kits)

**Wave:** p08 · **Cluster:** vs-a · **Kits:** 12 · **Mapper:** gandalf · **Date:** 2026-07-18

## Grade histogram

| Grade | Count | Kits |
|---|---|---|
| EXACT | 0 | — |
| CLOSE | 7 | vs-bloody-tear, vs-death-spiral, vs-fuwalafuwaloo, vs-heaven-sword, vs-hellfire, vs-holy-wand, vs-la-borra |
| APPROX | 2 | vs-gorgeous-moon, vs-je-ne-viv |
| GAPPED | 3 | vs-big-trouser, vs-gatti-amari, vs-infinite-corridor-crimson-shroud |

**GAPPED → MAPPED_DOCKET:** vs-big-trouser, vs-gatti-amari, vs-infinite-corridor-crimson-shroud

## Per-kit one-liners

| kit_id | Grade | One-liner |
|---|---|---|
| vs-big-trouser | GAPPED | No fixed weapon identity (Candybox flex); Greed-economy archetype; skills[] empty-projection |
| vs-bloody-tear | CLOSE | melee_arc + HP-on-crit trigger chain; no element/ailment (VS-silent) |
| vs-death-spiral | CLOSE | orbit geometry; pool-limit saturation identity; no element/ailment |
| vs-fuwalafuwaloo | CLOSE | Dual geometry (melee_arc + orbit); movement-ramp bonus; HP-on-crit sustain |
| vs-gatti-amari | GAPPED | Wandering-cat summon (totem-proxy); anti-harvest pickup-consumption economy has no engine lane; negative=1 |
| vs-gorgeous-moon | APPROX | Global screen-clear + gem-vacuum fusion; max-HP damage scalar; cooldown-floor economy; ring approximation misses global scale |
| vs-heaven-sword | CLOSE | placed_lane out-and-return boomerang; knockback attested; no element (name-only holy silenced) |
| vs-hellfire | CLOSE | placed_lane slow large-meteor delivery; VS element-silent blocks fire+burn despite theme |
| vs-holy-wand | CLOSE | single_target rapid-fire non-pierce volleys; VS element-silent blocks holy despite name |
| vs-infinite-corridor-crimson-shroud | GAPPED | Dual-weapon (beam_channel + aura); freeze attested (enemy status); HP-halving + 10-damage-cap both ungapped |
| vs-je-ne-viv | APPROX | Utility-stat-as-damage (Greed→damage, Magnet→range); aura + wandering entity; stat-conversion has no engine lane |
| vs-la-borra | CLOSE | ground_targeted_circle mobile growing puddles; VS element-silent blocks holy despite 'holy water' name |

## Candidate files

**Docket candidates (MAPPED_DOCKET kits):** vs-big-trouser (Candybox flex weapon identity), vs-gatti-amari (anti-harvest pickup-consumption economy + wandering-proxy delivery), vs-infinite-corridor-crimson-shroud (HP-halving screen effect + 10-damage-cap mechanic)

No mint-candidates-batch-p08.jsonl (no quantitative or qualitative mint calls generated — all mechanism gaps are docketed or approximated without mint need).

## T4-door frequency

| T4 token | Kits |
|---|---|
| PERSISTENCE_ENGINE_uptime | vs-bloody-tear, vs-fuwalafuwaloo, vs-holy-wand |
| PERSISTENCE_ENGINE_saturation | vs-death-spiral, vs-holy-wand |
| ZONE_CONTROL | vs-death-spiral, vs-hellfire, vs-la-borra |
| MOMENTUM_CASCADE | vs-fuwalafuwaloo |
| GEOMETRY_PROPAGATION_cascade | vs-gorgeous-moon |
| GEOMETRY_INVERSION | vs-heaven-sword |
| NETWORK_AMPLIFIER | vs-je-ne-viv |
| RESOURCE_CONVERSION | vs-je-ne-viv |
| DEFENSIVE_TRADEOFF | vs-infinite-corridor-crimson-shroud |
| RETRIBUTION_ENGINE | vs-infinite-corridor-crimson-shroud |


## §0 near-misses — elements/statuses WANTED but could not attest

| Kit | Wanted | Blocked by | Law |
|---|---|---|---|
| vs-hellfire | fire element + burn ailment | Dossier skill_loop explicitly notes "element-law: UNSUPPORTED" — wiki gives no fire damage-type statement | §B5-ROGUELITE element-silent + §0-UNIVERSAL (status not named) |
| vs-holy-wand | holy element | Dossier skill_loop explicitly notes "element-law: UNSUPPORTED" — "blue magic bolts" ≠ holy damage type | §B5-ROGUELITE + D4 name-only law |
| vs-la-borra | holy element | Dossier skill_loop explicitly notes "element-law: UNSUPPORTED" — "holy water" is name/description, not damage-type | §B5-ROGUELITE + D4 name-only law |
| vs-heaven-sword | holy element | "Cross" and "Heaven" in lineage/name → name-only; dossier confirms UNSUPPORTED | D4 name-only law |
| vs-je-ne-viv | shadow element (Shadow Servant, dark aura) | VS element-silent — no damage-type system; "shadow" is visual flavor, not a damage type | §B5-ROGUELITE element-silent |

## Family accrual candidates (file to steward)

- **out-and-return accrual:** vs-heaven-sword (boomerang double-pierce) → accrual to the out-and-return family
- **stat-as-damage-substrate accrual:** vs-je-ne-viv (Greed stat → Insatiable damage; Magnet stat → Insatiable range) → accrual to the stat-as-damage-substrate family

## Three hardest kits — one-line why

1. **vs-infinite-corridor-crimson-shroud** — Two-weapon system with HP-halving, 10-damage-cap, and freeze emission requiring exception adjudication under §B5-ROGUELITE element rule; dual-weapon dossier decomposition required
2. **vs-big-trouser** — Candybox flex identity means no mappable skill loop exists; empty-projection precedent must be applied deliberately, not apologetically
3. **vs-gatti-amari** — Anti-harvest pickup-consumption economy and wandering friendly-fire cats have no engine lanes; negative=1 corpus flag requires map-attested-identity discipline while negative story rides review book

## Brief ambiguities encountered

None filed to steward. All element calls resolved under §B5-ROGUELITE (VS element-silent) + §0.2 (name-only law). The freeze exception for vs-infinite-corridor-crimson-shroud resolved cleanly under §B5-ROGUELITE explicit: "Freezing enemies generates explosions → freeze; out-of-bounds-freeze" — dossier attests "enemies hit by beam are frozen" = enemy-directed status verb → freeze emitted correctly.

