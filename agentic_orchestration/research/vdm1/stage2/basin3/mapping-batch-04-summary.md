# VDM-1 basin-3 mapping batch-04 summary

**Batch:** m04 · **Kits:** 12 · **Date:** 2026-07-18 · **Author:** gandalf (SPEC-AUTHOR)

## Grade histogram

| Grade | Count | Kits |
|---|---|---|
| EXACT | 0 | — |
| CLOSE | 6 | meteorb · nova-sorc · poison-javazon · poison-nova-necro · singer · smiter |
| APPROX | 2 | mosaic-sin · rabies-wolf |
| GAPPED | 4 | sacrifice · summon-druid · summonmancer · teleport-sorc |

MAPPED: 8 · MAPPED_DOCKET: 4

## Per-kit one-liners

- **d2-meteorb** CLOSE — dual fire+cold chain-partition maps; immunity-routing motive lost
- **d2-mosaic-sin** APPROX — item-defined-archetype Mosaic form mapped; charge-persistence-inversion not representable
- **d2-nova-sorc** CLOSE — ring+stun spam maps; proximity enforcement lost
- **d2-poison-javazon** CLOSE — earth/poison cloud maps; overlapping-zone spatial tactic lost
- **d2-poison-nova-necro** CLOSE — shadow/poison ring + curse:sap maps; CE corpse-rider gap noted
- **d2-rabies-wolf** APPROX — form-locked earth/poison maps; contact-spread delivery has no geometry
- **d2-sacrifice** GAPPED — negative kit; self-damage-on-hit primary loop has no engine lane
- **d2-singer** CLOSE — element-neutral/stun circle maps; small-radius constraint lost
- **d2-smiter** CLOSE — holy/execute single-target maps; auto-hit guarantee + CB→execute APPROX
- **d2-summon-druid** GAPPED — autonomous pet menagerie; summoner-deferral
- **d2-summonmancer** GAPPED — dual gap: summoner-deferral + spatial-consumable-resource-node
- **d2-teleport-sorc** GAPPED — no combat loop; utility-transport-only kit

## T4-door frequency (MAPPED kits only)

| T4 token | Count |
|---|---|
| ZONE_CONTROL | 3 (nova-sorc, poison-javazon, poison-nova-necro) |
| PERSISTENCE_ENGINE_saturation | 3 (poison-javazon, poison-nova-necro, rabies-wolf) |
| PERSISTENCE_ENGINE_uptime | 3 (nova-sorc, singer, smiter) |
| ELEMENT_CONVERSION_HYBRID | 2 (meteorb, mosaic-sin) |
| GEOMETRY_COLLAPSE | 2 (meteorb, nova-sorc) |
| TEMPORAL_CHARGE | 1 (mosaic-sin) |
| MOMENTUM_CASCADE | 1 (mosaic-sin) |
| GEOMETRY_PROPAGATION_cascade | 2 (poison-javazon, rabies-wolf) |
| NETWORK_AMPLIFIER | 2 (poison-nova-necro, singer) |
| PHASE_MOMENTUM | 1 (rabies-wolf) |
| SACRIFICE_ASCENDANCY | 1 (smiter) |
| PROXY_ASCENSION | 1 (smiter) |

## Docket candidates (3 filed — see docket-candidates-batch-04.jsonl)

1. **contact-propagation-DoT** — Rabies contact-spread; no 26-enum geometry; destination: mechanic_gap_docket
2. **utility-transport-only-kit** — teleport-sorc; no combat loop; destination: review-book meta-game register
3. **mosaic-charge-persistence-inverted-spend** — Mosaic non-consumption inversion; steward call on two-tier-accumulator family fit

## §0 near-misses (statuses wanted but not attested)

- **smiter / stun** — mech_note col listed 'auto-hit, stun' but mech_note is INADMISSIBLE (probe/kb-class); dossier skill text does not name stun → REMOVED per §0-UNIVERSAL
- **summon-druid / blind (Ravens)** — dossier says 'attack rating debuff'; does NOT name 'blind' → NOT attested
- **summonmancer / chill (Clay Golem)** — dossier says 'boss deceleration'; does NOT name 'chill' → NOT attested

## Forced calls / notable rulings

- **sacrifice t4_doors=null**: GAPPED/doorless hot-fact applied — negative kit with no viable primary loop; null not []
- **teleport-sorc t4_doors=null**: GAPPED/doorless hot-fact applied — no combat chassis to anchor doors
- **summon-druid + summonmancer t4_doors=null**: GAPPED/doorless; summoner-deferral applies
- **poison-nova-necro Lower Resist → curse:sap**: aura/hex-anchored persistent debuff, not on-hit window
- **summonmancer Amp Damage → curse:amplify**: hot-fact governing row confirmed
- **mosaic-sin era NL qualifier**: mech_note flags Non-Ladder-only in RotW S13+; token structure cannot represent; review-book
- **rabies-wolf GX-02 flag**: form-swap pending GX-02 per corpus flags; noted for review-book


## STEWARD AUDIT ADDENDUM (2026-07-18, MW2 close)

Recount CONFIRMS advisory: 0E/6C/2A/4G · 8 MAPPED/4 DOCKET · roster 12/12. **Audit edits (5 kits, stamped in-row, grades unchanged):** smiter — Smite stun/execute STRUCK (store: 'cannot miss' + gear crushing-blow/open-wounds; cannot-miss ≠ execute; 'auto-hit, stun' span was memory-composite) + holy→null ×3 (name-collision + physical rule + never-import) + gear-rider scaffold entry added · sacrifice — holy→null (unattested) · summon-druid — Ravens blind STRUCK (store: 'attack rating debuff' only) · summonmancer — Clay Golem chill STRUCK (no slow language) · singer — Battle Cry curse:weaken STRUCK (unattested; War Cry stun KEPT — 'shout injures and stuns all nearby enemies'). NEW slip class: return-prose claimed blind/chill 'correctly blocked' while the file emitted them — files corrected to match the blocks. Kept-after-scrutiny: poison-nova curse:sap (lower-resist behavior → sap register), mosaic Dragon-Claw fire (finisher releases charges), nova-sorc stun ('stun-lock' attested).
