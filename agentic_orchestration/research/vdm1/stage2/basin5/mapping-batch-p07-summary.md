# VDM-1 basin-5 mapping batch-p07 summary (tli ×9 + tl1 ×2, 11 kits)

## Grade histogram

| Grade | Count | Kits |
|---|---|---|
| EXACT | 0 | — |
| CLOSE | 6 | tl1-ricochet-vanquisher · tli-rehan-berserker · tli-gemma-frost-caster · tli-carino2-lethal-flash · tli-erika3-vendetta · tli-sage-elixir |
| APPROX | 2 | tli-iris2-thunder-magus · tli-rosa-unsullied |
| GAPPED | 3 | tl1-alchemist-summoner · tli-youga-spirit-magus · tli-moto-bots |

MAPPED: 8 · MAPPED_DOCKET: 3

## Per-kit one-liners

| kit_id | Grade | Element(s) | T4 doors | Notes |
|---|---|---|---|---|
| tl1-alchemist-summoner | GAPPED | null / lightning-secondary | PROXY_ASCENSION | Pet-core minion army (summoner-deferral); lightning secondary attested (Ember Lightning electric damage) |
| tl1-ricochet-vanquisher | CLOSE | null (physical) | GEOMETRY_PROPAGATION_cascade | Wall-bounce ricochet; physical no-family; Explosive Shot AoE secondary |
| tli-rehan-berserker | CLOSE | null (physical) | TEMPORAL_CHARGE · ELEMENT_CONVERSION_MONO | Rage accumulator → Berserk; fire-convert variant = T4 door |
| tli-gemma-frost-caster | CLOSE | water | PERSISTENCE_ENGINE_saturation | Cold mage; Ice Lance + Frost Pool + Frozen Lotus on-kill; Frostbite→freeze |
| tli-iris2-thunder-magus | APPROX | lightning | PROXY_ASCENSION · PHASE_MOMENTUM | Hero-merges-into-Spirit-Magus form swap; mode-swap-identity docket |
| tli-youga-spirit-magus | GAPPED | lightning (Thunder Magus variant) | PROXY_SOVEREIGNTY | Pet-core summoner; Spirit Magi do all DPS; hero aura/curse support only |
| tli-carino2-lethal-flash | CLOSE | null (physical) | GEOMETRY_PROPAGATION_overkill | Shotgun out-and-return double pass; ammo cycle economy |
| tli-erika3-vendetta | CLOSE | water | PERSISTENCE_ENGINE_saturation · PHASE_MOMENTUM | Cold melee; Vendetta teleport + auto-attack; Frostbite 100-stack→freeze |
| tli-moto-bots | GAPPED | null (physical; Erosion unresolved) | PROXY_SOVEREIGNTY | Placed Spider Tank army ×6; Erosion filed to steward; summoner-deferral |
| tli-rosa-unsullied | APPROX | water (cold-dominant) | RESOURCE_CONVERSION · PERSISTENCE_ENGINE_uptime | Mana-stacking + highest-element-tracking Mercury Baptism; combination-determines-output docket |
| tli-sage-elixir | CLOSE | fire / water | ELEMENT_CONVERSION_HYBRID | Tri-element Chromatic Shot (Cold/Fire/Lightning); lightning dropped per §1 triple-drop rule |

## T4-door frequency (this batch)

PROXY_ASCENSION ×2 · PROXY_SOVEREIGNTY ×2 · PERSISTENCE_ENGINE_saturation ×2 · ELEMENT_CONVERSION_MONO ×1 · ELEMENT_CONVERSION_HYBRID ×1 · TEMPORAL_CHARGE ×1 · GEOMETRY_PROPAGATION_cascade ×1 · GEOMETRY_PROPAGATION_overkill ×1 · PHASE_MOMENTUM ×2 · RESOURCE_CONVERSION ×1 · PERSISTENCE_ENGINE_uptime ×1

## Candidate counts

| File | Rows |
|---|---|
| docket-candidates-batch-p07.jsonl | 9 (3 summoner-deferral · 2 family-accruals · 1 combination-determines · 1 mode-swap · 1 stat-as-damage-substrate · 1 FILE-TO-STEWARD element) |
| mint-candidates-batch-p07.jsonl | 0 |

## §0 near-misses — elements/statuses WANTED but could not attest

- **tli-moto-bots Erosion element**: Decayed Mind ring converts minion physical → Erosion Damage. Wanted to emit an earth/shadow family but Erosion is TLI-specific with no §1 row. Filed to steward.
- **tli-rehan-berserker fire (base identity)**: Wanted to emit fire for base loop — dossier only attests fire for the Whirlwind VARIANT (physical-to-fire convert). Base physical loop stays null.
- **tl1-alchemist-summoner burn on Ember Lance**: Ember Lance = "blast of ember energy" — wanted burn. No "inflicting burn / burning enemies" descriptor in attested text. Stayed null.
- **tli-iris2-thunder-magus shock ailment**: Thunder skills — wanted shock. No "applies shock / paralyzed / shocked enemies" descriptor in fetched text. Stayed null.
- **tli-youga-spirit-magus poison (Erosion Magus variant)**: Erosion Magus = alternate variant; dominant identity is Thunder Magus. Erosion unresolved per steward filing.

## Forced decisions / anything notable

- **tli-rosa-unsullied corpus elem_raw = "holy"**: overridden by dossier evidence (cold-dominant Skills attested; Extreme Coldness talent; capstone explicitly attests cold Infiltration). holy was a corpus probe artifact, not a fetched-text attestation — name-only logic applied.
- **tli-iris2-thunder-magus APPROX not GAPPED**: player actively fights in the merged Vigilant state using Magus skills — there IS a player-active skill loop (vs full pet-core). The merge is a mode-swap identity docket, not a summoner-deferral.
- **tli-sage-elixir tri-element drop**: §1 requires top-2; lightning dropped; fire/water chosen. The kit's actual identity is all-three-equal — noted as loss in fidelity.
- **era-U wall (all tli kits)**: all 9 TLI kits have UNSUPPORTED era verdicts. Mapped shape, not era. No season-specific mechanics asserted.
