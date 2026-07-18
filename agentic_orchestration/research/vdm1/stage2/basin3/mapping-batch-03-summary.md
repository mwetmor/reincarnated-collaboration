# VDM-1 basin-3 mapping batch-03 summary

**Batch:** m03 · **Kits:** 12 · **Author:** gandalf (SPEC-AUTHOR) · **Date:** 2026-07-18

## Grade histogram

| Grade | Count | Kit IDs |
|---|---|---|
| EXACT | 3 | d2-javazon, d2-lightning-sorc, d2-maul-bear |
| CLOSE | 3 | d2-hammerdin, d2-hydra-sorc, d2-kicksin |
| APPROX | 3 | d2-impale-zon, d2-inferno-sorc, d2-leap-attack-barb |
| GAPPED | 3 | d2-golemancer, d2-grim-ward-barb, d2-horker |

All GAPPED kits carry `terminal_state: MAPPED_DOCKET`.

## Per-kit one-liners

| Kit | Grade | One-liner |
|---|---|---|
| d2-golemancer | GAPPED | Single autonomous Iron Golem combatant — summoner-deferral GAP; gear-stat-as-minion-scaling docket accrual |
| d2-grim-ward-barb | GAPPED | Identity UNSUPPORTED; Grim Ward maps (fear attested, corpse-node emitted) but combat loop is area-denial only with zero damage engine |
| d2-hammerdin | CLOSE | Spiral-orbit maps to orbit token; magic damage element-neutral (holy excluded per §A.6); Teleport and Concentration aura in scaffold |
| d2-horker | GAPPED | Find Item loot re-roll identity has no engine lane; combat (WW + Berserk) maps but does not constitute the build per R-M7 |
| d2-hydra-sorc | CLOSE | 6-Hydra placed-turret network maps as totem (not summoner GAP); fire element clean; 6-count density = placed-proxy-count accrual |
| d2-impale-zon | APPROX | Melee single-strike maps; weapon durability drain economy has no engine lane; no attested ailment status |
| d2-inferno-sorc | APPROX | Rooted beam-channel maps; burn NOT attested (DoT-timing law bars emission); fire-immune hard-stop is un-mappable |
| d2-javazon | EXACT | Fork geometry + lightning element clean; Pierce as geometry scaffold modifier; Charged Strike secondary boss-kill attested |
| d2-kicksin | CLOSE | Dragon Talon multi-kick + Open Wounds bleed (item_alterations attested); Cobra Strike charge-cycle; Fade activation-toggle |
| d2-leap-attack-barb | APPROX | leap_strike maps D2R 2.4+ landing AoE; classic/lod era movement-only identity split; no ailment attested |
| d2-lightning-sorc | EXACT | Line + chain geometry clean; Infinity Conviction = curse:sap (§A.2 aura-sap); ELEMENT_CONVERSION_MONO + chain propagation |
| d2-maul-bear | EXACT | Form law economy-agnostic; Maul sustain-ramp (§A.5 not accumulator); Shockwave stun attested; MOMENTUM_CASCADE T4 |


## T4-door frequency

| T4 token | Count | Kits |
|---|---|---|
| PROXY_SOVEREIGNTY | 2 | d2-golemancer, d2-hydra-sorc |
| PERSISTENCE_ENGINE_uptime | 3 | d2-hammerdin, d2-hydra-sorc, d2-inferno-sorc |
| PROXY_ASCENSION | 1 | d2-golemancer |
| ZONE_CONTROL | 1 | d2-hammerdin |
| GEOMETRY_PROPAGATION_cascade | 2 | d2-javazon, d2-lightning-sorc |
| ELEMENT_CONVERSION_PHYSICAL | 1 | d2-javazon |
| ELEMENT_CONVERSION_MONO | 1 | d2-lightning-sorc |
| TEMPORAL_CHARGE | 1 | d2-kicksin |
| MOMENTUM_CASCADE | 2 | d2-kicksin, d2-maul-bear |
| GEOMETRY_COLLAPSE | 1 | d2-leap-attack-barb |
| PHASE_MOMENTUM | 2 | d2-leap-attack-barb, d2-maul-bear |
| (empty — GAPPED kits) | 2 | d2-grim-ward-barb, d2-horker |

## Candidate files

No `mint-candidates-batch-03.jsonl` required (no new mint candidates — all mechanisms map to existing lanes or established docket classes).

`docket-candidates-batch-03.jsonl` — non-empty (see file).

**Docket candidates:**
- `d2-golemancer`: summoner-deferral docket (known GAP); gear-stat-as-minion-scaling family accrual (first d2 attestation per §CROSS row 2)
- `d2-grim-ward-barb`: spatial-consumable-resource-node family accrual (§CROSS row 1); fear-only area-denial combat loop has no engine lane
- `d2-horker`: loot-economy-identity docket (§A row 4); Find Item corpse re-roll loop is meta-game register

## §0 near-misses — statuses WANTED but could not attest

| Kit | Wanted | Why blocked |
|---|---|---|
| d2-inferno-sorc | burn | Inferno delivers fire damage per-frame; dossier has no 'burn' or burn-status language; DoT-timing law bars emission |
| d2-leap-attack-barb | stun | Landing AoE impact; 'physical AoE damage on landing' is flavor, not a named stun status in dossier/verify_ledger |
| d2-impale-zon | stun | 'Powerful slow blow'; no stun named in any fetched language |
| d2-lightning-sorc | shock | Lightning element; 'shock' (paralysis) and 'sunder' (damage-amp) both absent from dossier |

## Anything forced

- **§A.6 hammerdin element trap:** element-neutral enforced. Holy is a probe fabrication (ERRATA queue, per §A row 6 hot-fact). Magic damage = element-neutral per THE PHYSICAL RULE extension. Never imported.
- **§CROSS.1 grim-ward identity honesty:** identity UNSUPPORTED → honest-U maintained; no stretch to approximate a confirmed build.
- **§A.4 horker R-M7:** honest GAPPED enforced. Find Item loop IS the identity; combat mapping alone fails R-M7 player test.
- **§CROSS row 5 inferno rooted-channel:** delivery_notes explicitly states ROOTED per basin-3 addendum mandate.
- **§A.5 maul-bear stack law:** Maul ramp confirmed as sustain-stack (§A.5), NOT two-tier-accumulator. No accrual filing.
- **§CROSS row 2 hydra totem-vs-companion:** Hydra is duration-capped stationary emitter → totem lane. NOT summoner GAP (correct two-lane application).

