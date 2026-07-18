# VDM-1 basin-5 mapping batch-p01 summary — tq-a (11 kits)

**Wave:** p01 · **Cluster:** tq-a (Titan Quest) · **Date:** 2026-07-18

## Grade histogram

| Grade | Count | Kits |
|---|---|---|
| EXACT | 3 | tq-brigand-poison · tq-ice-shard-oracle · tq-marksmanship-haruspex |
| CLOSE | 4 | tq-battlemage-warfare-earth · tq-distortion-templar · tq-druid-squall-caster · tq-elementalist-volcanic-storm |
| APPROX | 3 | tq-calculated-strike · tq-dream-harbinger · tq-flame-surge |
| GAPPED | 1 | tq-liche-king-conjurer |

## Per-kit one-liners

| kit_id | grade | one-liner |
|---|---|---|
| tq-battlemage-warfare-earth | CLOSE | Fire+physical hybrid; burn on melee via Volatility; physical no-family loses half the identity at element level |
| tq-brigand-poison | EXACT | Earth poison DoT ranged; Study Prey → curse:sap; Poison Gas Bomb zone; clean fit |
| tq-calculated-strike | APPROX | Negative=1; every-fourth-hit charge burst maps temporal_charge shape; non-primary nature = diminished |
| tq-distortion-templar | CLOSE | Vitality→shadow correction applied; stun ring AoE; physical+shadow dual but only shadow emits |
| tq-dream-harbinger | APPROX | Thin dossier (mechanics UNSUPPORTED); melee+blink; drain from ADCTH; Dream Trance specifics absent |
| tq-druid-squall-caster | CLOSE | Squall lightning NAME-ONLY struck; blind from accuracy-reduction source-mechanism; lightning via Static Charge |
| tq-elementalist-volcanic-storm | CLOSE | Fire+water dual; burn from Conflagration; lightning Storm Surge not emitted (no damage-type descriptor found) |
| tq-flame-surge | APPROX | Negative=1; short-range fire cone; curse:sap from Defensive Ability reduction; late-game-only viability = diminished |
| tq-ice-shard-oracle | EXACT | Cold→water; chill from slow; Deathchill→curse:weaken; Torrent variant noted; clean fit |
| tq-liche-king-conjurer | GAPPED | Pet-core summoner; Liche King = following companion, not player transform; summoner-deferral filed |
| tq-marksmanship-haruspex | EXACT | Pierce+physical no-family; bleed attested; Study Prey → curse:sap; fork Scatter Shot; clean fit |

## T4-door frequency

| T4 token | Count |
|---|---|
| PERSISTENCE_ENGINE_saturation | 2 |
| PERSISTENCE_ENGINE_uptime | 3 |
| ZONE_CONTROL | 2 |
| TEMPORAL_CHARGE | 2 |
| MOMENTUM_CASCADE | 2 |
| ELEMENT_CONVERSION_PHYSICAL | 3 |
| PROXY_SOVEREIGNTY | 1 |
| PROXY_ASCENSION | 1 |
| ELEMENTAL_ECHO | 1 |
| GEOMETRY_PROPAGATION_cascade | 2 |
| GEOMETRY_COLLAPSE | 2 |
| GEOMETRY_INVERSION | 1 |
| DEFENSIVE_TRADEOFF | 1 |

## Candidates

- **Docket:** 1 (`docket-candidates-batch-p01.jsonl`) — tq-liche-king-conjurer summoner-deferral
- **Mint:** 0

## §0 near-misses — elements/statuses wanted but could not attest

- **tq-distortion-templar:** knockback — mechanics claim CONTRADICTED at verify; the stun replaced it.
- **tq-elementalist-volcanic-storm:** lightning — Storm mastery is thematically central but no damage-type descriptor found in fetched text for lightning on this specific kit; Storm Surge attested as a passive proc name only.
- **tq-druid-squall-caster:** wind — Squall delivers a "wind storm" effect noun but the description "slight damage and applies useful debuffs" never applies "wind" as a damage-type descriptor to a generic effect noun; struck per §0.2.
- **tq-dream-harbinger:** no element wanted; but fear — "one of the more powerful Dual Wielding builds" with Dream Trances — no fear/terrorize mechanic attested in fetched dossier text.
- **tq-marksmanship-haruspex:** poison — secondary mention ("DoT bleeding and poison") in broader Brigand description but Haruspex kit dossier does not specifically attest poison application; bleed is the attested ailment.
- **tq-liche-king-conjurer:** arcane Blast synergy "multi-projectile elemental/vitality stun+slow" mentioned in capstone_alterations — stun and slow (chill) would be real signal if the player's kit rather than the Liche pet triggered them; mapped as pet-output, not player ailment, so held from ailment[] list.

## Three hardest kits

1. **tq-liche-king-conjurer** — player-transform identity CONTRADICTED at verify; summoned-pet determination required totem-vs-companion ruling + §B5-ELEMENT vitality→shadow correction simultaneously; GAPPED threshold judgment on pet-core vs pet-rider.
2. **tq-distortion-templar** — "physical and vitality damage" phrase requires §B5-ELEMENT correction (vitality→shadow) while holding the physical no-family rule; two competing no-family instincts active at once; stun vs knockback contradicted mechanics claim adds adjudication layer.
3. **tq-druid-squall-caster** — Squall lightning strike (name-only per p01 hot-fact) + blind from accuracy-reduction (source-mechanism inference, no token word "blind" in text) + lightning attestation routed through Static Charge capstone rather than Squall's own anchor — three simultaneous §0.2 / source-mechanism adjudications.

## Brief ambiguity

None requiring steward escalation. All elements and mechanisms resolved under main-law + §B5-ELEMENT + p01 hot-facts. No erosion, no radiant ambiguous-bucket triggers.

**Negative-flag note:** tq-calculated-strike and tq-flame-surge are negative=1; attested identities mapped; negative story rides review book per §E-4. tq-ternion-bone-charmer flagged in brief as review-book negative candidate — not in this batch (p02 territory).
