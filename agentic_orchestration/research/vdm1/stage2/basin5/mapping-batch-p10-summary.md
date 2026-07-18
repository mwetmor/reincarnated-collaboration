# mapping-batch-p10 summary — hot-a (9 kits)

## Grade histogram

| Grade | Count | Kits |
|---|---|---|
| EXACT | 3 | hot-dragons-breath · hot-exterminator-burn · hot-meteor-strike |
| CLOSE | 4 | hot-archer · hot-astronomer-orbs · hot-cleric-radiant · hot-kugelblitz |
| APPROX | 1 | hot-landsknecht-grenades |
| GAPPED | 1 | hot-blood-catcher |

## Per-kit one-liners

| kit_id | grade | one-liner |
|---|---|---|
| hot-archer | CLOSE | multi_projectile cone, pierce, no element — physical arrows, element-neutral; variants (lightning/bleed) dropped per variant-scope ruling |
| hot-astronomer-orbs | CLOSE | orbit (3 shells), no element, Summon-typed; movement-speed orbit coupling not expressible in geometry params |
| hot-blood-catcher | GAPPED | negative=1 patched exploit; skill_geometry abstained; no post-patch loop; trigger grammar captures pre-patch shape for record |
| hot-cleric-radiant | CLOSE | aura, element-NEUTRAL (generic "magic" only — "radiant damage" not typed); §B5-ROGUELITE explicit ruling honored |
| hot-dragons-breath | EXACT | cone, fire+burn; fire attested "fire-based attack / 3,000,000 fire damage"; burn attested "Burn Chance / burning" |
| hot-exterminator-burn | EXACT | cone, fire+burn; fire attested "Flame Caster / fire damage"; burn attested "Flames have 10% Burn Chance"; single-axis burn identity |
| hot-kugelblitz | CLOSE | totem (wandering proxy), lightning+stun; "Electrify" is HoT-native, not engine `shock` — dropped to delivery_notes |
| hot-landsknecht-grenades | APPROX | line (Arquebus) + ground_targeted_circle (grenades); derived-scaling ratio has no engine lane; post-cutoff conf capped |
| hot-meteor-strike | EXACT | ground_targeted_circle, fire, no burn (burn is Exterminator class trait, not Meteor Strike attribute per §0-UNIVERSAL) |

## T4-door frequency

| T4 token | Count |
|---|---|
| PERSISTENCE_ENGINE_saturation | 2 (dragons-breath, exterminator-burn) |
| ELEMENT_CONVERSION_MONO | 3 (dragons-breath, exterminator-burn, meteor-strike) |
| PROXY_ASCENSION | 2 (astronomer-orbs, kugelblitz) |
| GEOMETRY_PROPAGATION_overkill | 3 (archer, landsknecht-grenades, meteor-strike) |
| TEMPORAL_CHARGE | 3 (archer, kugelblitz, landsknecht-grenades) |
| PERSISTENCE_ENGINE_uptime | 2 (astronomer-orbs, cleric-radiant) |
| ZONE_CONTROL | 1 (cleric-radiant) |

## Candidate files

None — no mint or docket candidates require side-files.

**Placed-proxy-count accrual** (steward action): hot-astronomer-orbs 3-shell orbital structure is a counted-proxy shape — accrual to placed-proxy-count family (file WITHOUT numbers per basin rule).

## §0 near-misses (wanted to emit but could not attest)

1. **hot-kugelblitz — `shock` ailment:** Wanted to emit `shock` for "Electrify" status. BLOCKED: engine `shock` = paralysis-on-arc hard CC; HoT "Electrify" is a different stacking voltage status not in the 16-ailment registry. Cannot cross-map per §0-UNIVERSAL.
2. **hot-cleric-radiant — `holy` element:** Wanted to emit holy for "Radiant Aura / Cleric." BLOCKED: §B5-ROGUELITE explicit ruling: "radiant→holy only if store types 'radiant damage'; crawl attested generic 'magic' only → neutral."
3. **hot-meteor-strike — `burn` ailment:** Wanted to emit burn given fire element. BLOCKED: burn is Exterminator's class stat (trait), not a typed attribute of Meteor Strike's own damage in the fetched dossier. §0-UNIVERSAL requires status NAMED in THIS kit's dossier text.
4. **hot-archer — `pierce` as ailment:** Pierce is a geometry modifier (lane-through), not a 16-enum ailment. Correctly placed in geometry lane.
5. **hot-landsknecht-grenades — fire element for grenades:** No "fire damage" or "explosive fire" descriptor in fetched text — grenades described as "area damage" only. Cannot attest.

## 3 hardest kits

1. **hot-kugelblitz** — "Electrify" status is the build's secondary identity marker but has no 16-ailment mapping; engine `shock` is categorically different; required full §0-UNIVERSAL discipline to not bleed the HoT-native status through.
2. **hot-landsknecht-grenades** — derived-scaling architecture (grenade damage = f(projectile damage)) has no engine lane; post-cutoff confidence cap adds uncertainty; two-skill decomposition required.
3. **hot-blood-catcher** — confirmed negative with abstained skill_geometry; mapping must record the mechanism shape (trigger grammar) while correctly GAPPING and routing to MAPPED_DOCKET per R-M7.

## Brief ambiguities / flags

- No ambiguities requiring steward escalation this wave. All element rulings resolved cleanly under §B5-ROGUELITE and §B5-ELEMENT.
- Placed-proxy-count accrual for hot-astronomer-orbs flagged for steward action above.
