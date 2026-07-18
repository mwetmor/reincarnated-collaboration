# mapping-batch-p02 summary — tq-b cluster (10 kits)

**Wave:** p02 · **Cluster:** tq-b · **Date:** 2026-07-18

## Grade histogram

| Grade | Count | Kit IDs |
|---|---|---|
| EXACT | 0 | — |
| CLOSE | 8 | tq-onslaught-assassin · tq-phantom-strike-dreamkiller · tq-ranger-hunting-nature · tq-rune-weapon-thunderer · tq-shield-charge-conqueror · tq-ternion-bone-charmer · tq-thane-storm-warfare · tq-warlock-poison-vitality |
| APPROX | 1 | tq-trap-magician |
| GAPPED | 1 | tq-petmaster-summoner |

## Per-kit one-liners

| kit_id | grade | summary |
|---|---|---|
| tq-onslaught-assassin | CLOSE | Physical dual-wield Onslaught loop; Envenom earth/poison overlay; WPS proc chain mapped as on-hit trigger |
| tq-petmaster-summoner | GAPPED | Pet-core summoner (wolves+Liche King); no player-damage loop; summoner-deferral docket |
| tq-phantom-strike-dreamkiller | CLOSE | Teleport-burst dash_attack; Dream Stealer ring-burst trigger-linked; poison earth overlay |
| tq-ranger-hunting-nature | CLOSE | Pierce Marksmanship line-geometry; Study Prey curse:sap; wolf light-proxy companion |
| tq-rune-weapon-thunderer | CLOSE | Lightning melee converter; Rune Weapon tick-cost toggle; ELEMENT_CONVERSION_MONO capstone identity |
| tq-shield-charge-conqueror | CLOSE | Charge-tank; Shield Charge dash_attack lane + stun; Onslaught sustained DPS secondary |
| tq-ternion-bone-charmer | CLOSE | Shadow (vitality→shadow) triple-projectile; Deathchill Aura chill+sap; review-book negative candidate |
| tq-thane-storm-warfare | CLOSE | Lightning dual-wield warrior; placed Squall zone; mechanics UNSUPPORTED in verify_ledger (identity+era confirmed) |
| tq-trap-magician | APPROX | Pierce-trap placed-proxy; max-trap-count economy approximated; Flame Surge NAME-ONLY → null; no fire emitted |
| tq-warlock-poison-vitality | CLOSE | Dual DoT (earth/shadow): poison Ternion primary + vitality secondary; Life Drain beam+drain; Deathchill chill+sap |

## T4-door frequency

| T4 token | Kits |
|---|---|
| MOMENTUM_CASCADE | tq-onslaught-assassin · tq-phantom-strike-dreamkiller · tq-shield-charge-conqueror · tq-thane-storm-warfare |
| PERSISTENCE_ENGINE_saturation | tq-onslaught-assassin · tq-ranger-hunting-nature · tq-warlock-poison-vitality |
| ELEMENT_CONVERSION_MONO | tq-rune-weapon-thunderer · tq-thane-storm-warfare |
| TEMPORAL_CHARGE | tq-phantom-strike-dreamkiller · tq-rune-weapon-thunderer |
| PROXY_ASCENSION | tq-petmaster-summoner |
| PROXY_SOVEREIGNTY | tq-petmaster-summoner · tq-trap-magician |
| PROXY_CONVERGENCE | tq-ternion-bone-charmer |
| DUAL_PROXY | tq-warlock-poison-vitality |
| ZONE_CONTROL | tq-shield-charge-conqueror · tq-trap-magician |
| GEOMETRY_PROPAGATION_overkill | tq-ranger-hunting-nature |

## Candidate files

- `docket-candidates-batch-p02.jsonl` — 2 entries: summoner-deferral (tq-petmaster-summoner) + placed-proxy-count accrual (tq-trap-magician + tq-petmaster-summoner)
- No mint-candidates this batch

## §0 near-misses — elements/statuses WANTED but could not attest

| Kit | Wanted | Reason STRUCK |
|---|---|---|
| tq-trap-magician | fire (Flame Surge) | NAME-ONLY: "Flame Surge" appears in core_skills only as "(support)" label; no "deals fire damage" in dossier payload_json or anchor_quote; §0.2 applied |
| tq-trap-magician | lightning (Storm/Storm Nimbus) | Storm Nimbus buffs trap pet elemental damage via gear (+pets elemental damage jewels) — this is pet-gear buffing, not player damage-typed; NAME-ONLY "Storm" mastery |
| tq-thane-storm-warfare | stun (Thunderball CC) | Stun plausible for Thunderball but not explicitly named in dossier anchor_quote; lower-confidence delivery_note only; omitted from ailments |
| tq-petmaster-summoner | shadow (Liche King vitality) | Pet-owned damage type; not player skill typed; pet damage in capstone_alterations describes PET gear scaling, not player element output |
| tq-shield-charge-conqueror | fire/element | None attested; purely physical build |
| tq-ranger-hunting-nature | poison (wolves/Briar Ward) | Briar Ward listed in core_skills; no "deals poison damage" in dossier; thematic nature element but no damage-type descriptor |

## Anything forced

- `tq-thane-storm-warfare` mechanics claim = UNSUPPORTED in verify_ledger but identity+era confirmed; mapped from dossier evidence with fidelity_note. Lightning attested in identity anchor "dual wielding elemental warrior" + skill_geometry payload "Lightning chains between nearby enemies."
- `tq-ternion-bone-charmer` review-book negative candidate (per brief §E.4): mapped the ATTESTED identity; negative story rides the review book.
- `tq-trap-magician` APPROX (not GAPPED): player-deployment loop IS present ("trap placement IS the build action"); "that build, worse" test applies; not GAPPED.
- Deathchill Aura chill+sap mapping (tq-ternion-bone-charmer + tq-warlock-poison-vitality): applied §B5-ELEMENT source-mechanism-not-token rule — resistance reduction → curse:sap, speed slow → chill; store need not say "chill"/"sap" explicitly.
