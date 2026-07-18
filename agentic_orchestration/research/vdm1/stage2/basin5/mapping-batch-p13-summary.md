# VDM-1 basin-5 mapping batch-p13 — summary

**Wave:** p13 (FINAL basin-5 wave) · **Sources:** MCD (5 kits) + LE-riders (2 kits) = **7 kits total**
**Date authored:** 2026-07-18 · **Author:** gandalf (SPEC-AUTHOR)

---

## Grade histogram

| Grade | Count | Kit(s) |
|---|---|---|
| EXACT | 0 | — |
| CLOSE | 5 | mcd-dynamo-torment, mcd-fireworks, mcd-soul, le-bomb-lance-falconer, le-harvest-lich |
| APPROX | 1 | mcd-speed |
| GAPPED → MAPPED_DOCKET | 1 | mcd-summoner |

**MAPPED:** 6 · **MAPPED_DOCKET:** 1

---

## Per-kit one-liners

| kit_id | Grade | One-liner |
|---|---|---|
| mcd-dynamo-torment | CLOSE | Roll-stack(20x)→unload; Torment Quiver line-pierce with knockback; TEMPORAL_CHARGE; no element (MCD silent) |
| mcd-fireworks | CLOSE | Multi-projectile+circle-explosion per arrow; CD-cycling artifact loop; GEOMETRY_PROPAGATION_cascade; no element |
| mcd-soul | CLOSE | beam_channel Corrupted Beacon (20 souls/sec tick-cost) + circle Harvester AoE; PERSISTENCE_ENGINE_uptime; no element |
| mcd-speed | APPROX | Movement-as-offense/defense; no engine first-class speed lane; PHASE_MOMENTUM approximation; Light Feather knockback |
| mcd-summoner | GAPPED | Pet-CORE (3 companion artifacts = entire damage loop); summoner-deferral; no player-rotation; MAPPED_DOCKET |
| le-bomb-lance-falconer | CLOSE | Explosive Trap (free) procs placed Ballista turrets (totem) + Dive Bomb burst + Falcon companion; water primary (cold/physical attested); DUAL_PROXY |
| le-harvest-lich | CLOSE | Two-build: Harvest Flay (water/cold melee_arc, Reaper Form) + Death Seal (shadow/necrotic aura, Low Life tradeoff); DEFENSIVE_TRADEOFF |

---

## T4-door frequency (this batch)

| T4 token | Kits |
|---|---|
| TEMPORAL_CHARGE | mcd-dynamo-torment |
| MOMENTUM_CASCADE | mcd-dynamo-torment, mcd-speed |
| GEOMETRY_PROPAGATION_cascade | mcd-fireworks |
| ZONE_CONTROL | mcd-fireworks |
| PERSISTENCE_ENGINE_uptime | mcd-soul |
| RESOURCE_CONVERSION | mcd-soul |
| PHASE_MOMENTUM | mcd-speed |
| PROXY_SOVEREIGNTY | mcd-summoner |
| COMPANION_CONTRACT | mcd-summoner |
| PROXY_ASCENSION | le-bomb-lance-falconer |
| DUAL_PROXY | le-bomb-lance-falconer |
| DEFENSIVE_TRADEOFF | le-harvest-lich |
| SACRIFICE_ASCENDANCY | le-harvest-lich |


---

## Candidate files

**docket-candidates-batch-p13.jsonl** — 2 entries:
1. `mcd-summoner` → `summoner-deferral` (pet-CORE; companions are entire damage loop; no player rotation)
2. `le-bomb-lance-falconer` → `placed-proxy-count` accrual (dual placed entity: Explosive Trap + Ballista simultaneously in loop)

**mint-candidates-batch-p13.jsonl** — empty (none required; all approximations handled via existing T4 tokens + APPROX grade)

---

## §0 near-misses — elements/statuses WANTED but could not attest

| Kit | Wanted | Reason blocked |
|---|---|---|
| le-bomb-lance-falconer | fire (element_secondary) | Brief hot-fact references "Explosive Trap inflicting fire damage" but this phrase not found in any non-abstained (abstained=0) dossier row; store-not-style law requires abstained=0 text only; fire NOT emitted |
| mcd-soul | shadow (element) | "shadow beam" and "soul" are explicitly noted as flavor/resource in §B5-MCD; no damage-type language → null |
| mcd-fireworks | fire (element) | "explosion" is mechanism/delivery, not fire damage-type per §B5-MCD; null |
| mcd-dynamo-torment | any element | MCD element-silent throughout; Torment Quiver "soul" is resource; null |
| mcd-speed | any ailment (enemy-directed) | Only attested: knockback on Light Feather dash (self-use, not enemy status); no enemy chill/slow language in dossier |

---

## Anything forced / notable

- **MCD capstone: structural abstain correct on all 5.** No mastery tree in MCD; capstone_alterations omitted from all 5 MCD rows — this is inapplicability not gap.
- **le-harvest-lich two-build split:** folk name "Harvest Death Seal Lich" is NOT a verified single build per maxroll (two separate guides). Mapped as two-variant kit with both represented in skills[]; motion_frame notes both variants. Grade held at CLOSE rather than GAPPED because each sub-build maps cleanly.
- **le-bomb identity mismatch wrappers used as prose per brief:** all 6 dossier rows carry `{"note":"IDENTITY_MISMATCH..."}` wrappers; the prose inside IS the mappable content per brief instruction. Mapped accordingly.
- **mcd-speed APPROX:** movement-as-defense/offense identity has no engine first-class lane; PHASE_MOMENTUM approximates but the cycling-speed-buff experience is distinctly thinner in engine translation.
- **verify_ledger UNSUPPORTED on le-harvest-lich:** all 5 ledger rows are UNSUPPORTED (dossier populated in basin-2, not crawled in basin-5 pipeline). Mapping proceeds on dossier content as directed by brief.

---

## Basin-5 FINAL WAVE note

p13 closes the 13-wave basin-5 mapping pass: 125 kits mapped across tq/chr/ud/tl2/tli/tl1/vs/hot/hades1/mcd/le-riders. This wave completes the FINAL basin (basin-5) of VDM-1 Stage-2 mapping.

