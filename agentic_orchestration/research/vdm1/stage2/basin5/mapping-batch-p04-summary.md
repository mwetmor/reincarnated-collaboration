# VDM-1 Basin-5 mapping batch-p04 summary — chr-b (8 kits)

## Grade histogram

| Grade | Count | Kits |
|---|---|---|
| EXACT | 3 | chr-high-ranger-warden · chr-mechanist-rocketeer · chr-mechanist-saw-master |
| CLOSE | 2 | chr-fulmination-templar · chr-plague-curse-warlock |
| APPROX | 1 | chr-thorns-templar |
| GAPPED | 2 | chr-mechanist-turret-drone · chr-pet-warden |

## Per-kit one-liners

- **chr-fulmination-templar** CLOSE — lightning attested via 'lightning proc events' (indirect descriptor); holy via item bonus anchor; mechanics verify UNSUPPORTED reduces confidence
- **chr-high-ranger-warden** EXACT — 'bleed ethereal damage' direct; physical = no-family; line+pierce geometry; clean
- **chr-mechanist-rocketeer** EXACT — 'fire attribute damage' directly attested; rocket AoE burst; drone variant = placed totem
- **chr-mechanist-saw-master** EXACT — physical ricochet; bleed via Puncture; Loose Blade on-kill cascade = GEOMETRY_PROPAGATION_cascade
- **chr-mechanist-turret-drone** GAPPED — machine-core proxy; 'Holy Lance Turrets' = name-only (hot-fact honored); no player damage loop; summoner-deferral
- **chr-pet-warden** GAPPED — companion-core (7 pet types); per-pet behavior unrepresentable; bleed attested via Wolftooth but pet IS the identity
- **chr-plague-curse-warlock** CLOSE — shadow via 'shadow damage' anchor; 'desecrators set' = name-only (hot-fact honored); Desecration Weakness stack depth unrepresented
- **chr-thorns-templar** APPROX — physical thorns = no-family; stat-as-damage-substrate formula (50% dmg + 30% HP → thorns) not in engine; lightning variant major but secondary

## T4-door frequency

- PERSISTENCE_ENGINE_saturation: 2 (chr-high-ranger-warden, chr-plague-curse-warlock)
- GEOMETRY_PROPAGATION_cascade: 2 (chr-mechanist-saw-master, chr-mechanist-rocketeer)
- PROXY_ASCENSION: 2 (chr-mechanist-turret-drone, chr-pet-warden)
- RETRIBUTION_ENGINE: 1 (chr-thorns-templar)
- ELEMENT_CONVERSION_PHYSICAL: 1 (chr-thorns-templar — conversion variant door)
- TEMPORAL_CHARGE: 2 (chr-fulmination-templar, chr-mechanist-rocketeer)
- RESONANCE_LOOP: 1 (chr-fulmination-templar)
- NETWORK_AMPLIFIER: 1 (chr-plague-curse-warlock)
- COMPANION_CONTRACT: 1 (chr-pet-warden)
- DUAL_PROXY: 1 (chr-mechanist-turret-drone)


## Candidates

### Docket candidates: 3
- **chr-mechanist-turret-drone**: summoner-deferral (placed-proxy-count + per-machine behavior)
- **chr-pet-warden**: summoner-deferral (companion-count + per-pet behavior)
- **chr-thorns-templar**: stat-as-damage-substrate (multi-stat formula → thorns output)

### Mint candidates: 0

## §0 near-misses — elements/statuses WANTED but could not attest

- **chr-mechanist-turret-drone holy**: 'Holy Lance Turrets' = skill-name; 'the holy Mechpriest skill trees' = tree name; no fetched 'deals holy damage' descriptor → SILENCED per §0.2 + hot-fact ruling
- **chr-pet-warden elements**: wolf/wisp physical base only; Wolfcaster Ice Shard → cold possible in Wolfcaster variant but pet-core GAPPED makes variant secondary
- **chr-plague-curse-warlock poison ailment atop curse:amplify**: Desecration Weakness is curse-amplify shaped but also stacks (9-10x) — wanted to attest stacking-curse depth but no engine analog; approximated as curse:amplify
- **chr-fulmination-templar ailments**: wanted shock/sunder from lightning proc identity but no explicit 'enemies shocked' or 'deals increased damage taken' language in dossier — suppressed
- **chr-thorns-templar taunt**: taunt is central to loop (enemies must strike Templar) but taunt has no solo ailment lane per §2 note — recorded in fidelity_note only
- **chr-thorns-templar chain lightning ailments**: chain lightning via Avenger = lightning family confirmed but attested as variant not primary — not promoted to element_primary on primary skill

## Anything forced

- chr-thorns-templar: APPROX forced by stat-as-damage-substrate formula gap AND major lightning-variant identity not representable in primary mapping; player who runs Lightning Thorns Avenger would recognize the primary-APPROX but not as their build
- chr-mechanist-turret-drone element-silent: name-only law applied strictly per hot-fact; element silence may feel surprising given 'holy Mechpriest' tree branding but law is clear

## Placed-proxy-count accrual flag

File accrual to the placed-proxy-count family: chr-mechanist-turret-drone (Stinger turret + Laser/Rocketeer/Poison/Holy Lance drones — multiple simultaneous placed machines). Steward to number.

