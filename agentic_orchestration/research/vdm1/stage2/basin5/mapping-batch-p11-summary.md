# VDM-1 basin-5 mapping batch-p11 summary — Halls of Torment hot-b (8 kits)

## Grade histogram

| Grade | Count | Kit IDs |
|---|---|---|
| EXACT | 3 | hot-phantom-needles · hot-sorceress-splinters · hot-swordsman |
| CLOSE | 4 | hot-norseman-frost-avalanche · hot-sage-ring-blades · hot-shieldmaiden-block · hot-warlock |
| APPROX | 0 | — |
| GAPPED → MAPPED_DOCKET | 1 | hot-spirit-warrior |

## Per-kit one-liners

- **hot-norseman-frost-avalanche** CLOSE — water/ring/freeze+chill; two-tier accumulator (250-hit nova + 20-stack-per-enemy explode) maps to TEMPORAL_CHARGE+cascade pair but shape is steward-accrual territory
- **hot-phantom-needles** EXACT — null/line/no-ailment; physical pierce-line, clean
- **hot-sage-ring-blades** CLOSE — null/orbit/no-ailment; low-conf dossier (0.42); "Fragile" debuff has no 16-ailment registry lane
- **hot-shieldmaiden-block** CLOSE — null/ring+melee_arc/burn+chill; stat-as-damage-substrate (Block Strength IS Shield Bash damage) is steward-accrual; burn item-sourced; chill from block-charge interaction
- **hot-sorceress-splinters** EXACT — null/multi_projectile/no-ailment; "arcane" name-only STRIKE; "elemental" upgrade = generic tri-element → null
- **hot-spirit-warrior** GAPPED — null/totem/no-ailment; pet-core summoner-deferral; engine has no persistent-placed-melee-proxy archetype
- **hot-swordsman** EXACT — null/melee_arc/no-ailment; physical frontal arc, clean starter
- **hot-warlock** CLOSE — null/chain/no-ailment; summon-projectile chain approximated as chain geometry + proxy layer; fired-expiring specters ≠ persistent pets

## T4-door frequency

| T4 door | Kits |
|---|---|
| ELEMENT_CONVERSION_PHYSICAL | hot-phantom-needles · hot-swordsman |
| GEOMETRY_PROPAGATION_overkill | hot-phantom-needles |
| TEMPORAL_CHARGE | hot-norseman-frost-avalanche |
| GEOMETRY_PROPAGATION_cascade | hot-norseman-frost-avalanche |
| ZONE_CONTROL | hot-sage-ring-blades |
| GEOMETRY_INVERSION | hot-sage-ring-blades |
| RETRIBUTION_ENGINE | hot-shieldmaiden-block |
| PERSISTENCE_ENGINE_uptime | hot-shieldmaiden-block |
| PROXY_ASCENSION | hot-spirit-warrior · hot-warlock |
| PROXY_SOVEREIGNTY | hot-spirit-warrior |
| MOMENTUM_CASCADE | hot-swordsman |
| NETWORK_AMPLIFIER | hot-warlock |

## Candidate files

- `docket-candidates-batch-p11.jsonl`: 1 entry — hot-spirit-warrior summoner-deferral (persistent-placed-melee-proxy)
- No mint-candidates this batch

## Accruals filed (steward-owned)

- **two-tier-accumulator family**: hot-norseman-frost-avalanche (hit-counter → nova; enemy frost stack → explosion)
- **stat-as-damage-substrate family**: hot-shieldmaiden-block (Block Strength IS shield bash damage)
- **placed-proxy-count family**: hot-spirit-warrior (stack multiple Spirit Warriors simultaneously)

## §0 near-misses — elements/statuses WANTED but could not attest

- **hot-sage-ring-blades**: "Fragile" debuff applied by Piercing Blades upgrade — wanted curse:weaken or curse:sap but the precise mechanism (armor-shred vs attack-reduction vs damage-amp) is unresolvable from fetched text; recorded in delivery_notes only
- **hot-sorceress-splinters**: "Arcane Elements adds elemental damage" — wanted to emit an element but "elemental" with no named dominant = generic tri-element → null forced
- **hot-warlock**: "summon/magic damage" — wanted element but generic magic = element-neutral per §B5-ELEMENT; no damage-type descriptor
- **hot-spirit-warrior**: "Magic Melee attacks" — same as warlock; generic magic → null forced; also wanted freeze/chill from Charge Shock upgrade but that is an upgrade-path item interaction, not base skill identity

## Anything forced

- hot-spirit-warrior era = UNSUPPORTED in verify_ledger; era row carries UNSUPPORTED verdict; mapped against confirmed identity + mechanics (two CONFIRMED); docket records era gap
- hot-sage-ring-blades all dossier rows conf 0.42–0.45 (Sage post-cutoff); low-conf mapped with CLOSE grade; steward should audit Sage-specific content when 1.1-2026 sources become available
