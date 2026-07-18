# Mapping batch p06 summary — Torchlight 2 (canary, 11 kits)

## Grade histogram

| Grade | Count | Kits |
|---|---|---|
| EXACT | 7 | cannon-engineer, emberquake-engineer, flame-hammer-engineer, hailstorm-embermage, prismatic-embermage, shotgonne-outlander, wolf-shade-berserker |
| CLOSE | 2 | arc-beam, glaive-outlander |
| APPROX | 1 | shadowling-outlander |
| GAPPED | 1 | bot-engineer |

## Per-kit one-liners

- **tl2-arc-beam** (CLOSE, MAPPED): NEGATIVE kit. Element-silent beam; source explicitly excludes it from Embermage's elemental damage. Thin but real mapping.
- **tl2-bot-engineer** (GAPPED, MAPPED_DOCKET): Pet-core summoner; no player-damage loop. Summoner-deferral. Spider Mines placed-proxy-count accrual filed.
- **tl2-cannon-engineer** (EXACT, MAPPED): Piercing line, physical, Charge economy. Clean fit to `line` + TEMPORAL_CHARGE.
- **tl2-emberquake-engineer** (EXACT, MAPPED): Fire ring-burst from self, fire attested via "fire-based magic damage." No burn explicitly attested.
- **tl2-flame-hammer-engineer** (EXACT, MAPPED): Fire melee strike + seeking splinters; fire attested on splinters. Charge-burst trigger fits TEMPORAL_CHARGE.
- **tl2-glaive-outlander** (CLOSE, MAPPED): Ricochet bounce physical glaive (EXACT); Venomous Hail poison attested only via dossier characterization text, not direct game quote.
- **tl2-hailstorm-embermage** (EXACT, MAPPED): Water(ice) zone, stun+freeze+curse:amplify all attested. Curse:amplify from ice/electric vulnerability language per source-mechanism callout.
- **tl2-prismatic-embermage** (EXACT, MAPPED): Tri-element fire+water+lightning attested; top-2 emitted (fire+water), lightning in fidelity_note. Freeze attested via Frozen Fate.
- **tl2-shadowling-outlander** (APPROX, MAPPED): Kill-to-spawn swarm; "shadow magic" fails damage-type-descriptor test; element-silent. Swarm-scaling identity not fully representable.
- **tl2-shotgonne-outlander** (EXACT, MAPPED): Cone physical, knockback+stun+blind all attested directly.
- **tl2-wolf-shade-berserker** (EXACT, MAPPED): Melee Charge→Frenzy cycle; "icy fangs" hot-fact STRIKE honored; element-silent.

## T4-door frequency

| T4 token | Count | Kits |
|---|---|---|
| TEMPORAL_CHARGE | 4 | cannon-engineer, flame-hammer-engineer, prismatic-embermage, wolf-shade-berserker |
| ELEMENT_CONVERSION_MONO | 2 | emberquake-engineer, flame-hammer-engineer |
| PERSISTENCE_ENGINE_saturation | 1 | emberquake-engineer |
| ZONE_CONTROL | 2 | hailstorm-embermage, shotgonne-outlander |
| PERSISTENCE_ENGINE_uptime | 1 | hailstorm-embermage |
| ELEMENT_CONVERSION_HYBRID | 1 | prismatic-embermage |
| MOMENTUM_CASCADE | 2 | prismatic-embermage, wolf-shade-berserker |
| GEOMETRY_PROPAGATION_cascade | 2 | glaive-outlander, shadowling-outlander |
| PROXY_ASCENSION | 2 | bot-engineer, shadowling-outlander |
| arc-beam | 0 | (negative, no T4 doors) |

## Candidates

- **docket-candidates-batch-p06.jsonl**: 2 rows — (1) summoner-deferral for tl2-bot-engineer (pet-core, GAPPED); (2) placed-proxy-count accrual for Spider Mines (up to 10 simultaneous placed proxies from one skill).
- **mint-candidates-batch-p06.jsonl**: not created (no quantitative or qualitative mint gap identified; all approximations fit existing engine constructs).

## §0 near-misses (wanted to emit, could not attest)

1. **burn on emberquake-engineer**: "fire-based magic damage" attests fire but no DoT/burn language in any store. Burn withheld.
2. **burn on flame-hammer-engineer**: "splinters deal fire damage" — fire yes, burn no. Withheld.
3. **shadow element on shadowling-outlander**: "shadow magic" describes the curse mechanism, not the damage type. Failed damage-type-descriptor test.
4. **chill on hailstorm-embermage**: persistent cold zone implies slowing but no movement-speed reduction attested explicitly. Withheld.
5. **lightning element on prismatic-embermage (primary slot)**: tri-element confirmed, lightning attested — dropped to fidelity_note per §1 hybrid top-2 rule.
6. **poison element on glaive-outlander primary**: Glaive Throw itself has no element descriptor; only Venomous Hail carries the poison signal.

## Hardest kits

1. **tl2-shadowling-outlander** — pet-rider/pet-core boundary judgment. "Shadow magic" cursor on element (fails descriptor test). Swarm-scaling identity partially GAPPED but player has a real attack loop → APPROX, not GAPPED. Required the most judgment.
2. **tl2-hailstorm-embermage** — curse:amplify call from "susceptible to Ice and Electric damage" required source-mechanism-not-token-word discipline; could have been missed as a simple debuff note without the §B5-ELEMENT callout.
3. **tl2-glaive-outlander** — Venomous Hail poison attestation ambiguity: dossier payload says "supplemental poison AoE" but no direct game-text quote of the form "deals poison damage." Graded CLOSE; steward may upgrade to EXACT on review if dossier payload_json is accepted as sufficient store.
