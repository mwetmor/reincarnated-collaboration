# VDM-1 basin-3 mapping batch-10 summary

**Batch:** m10 · **Kits:** 12 (1 d3 + 11 d4) · **Date:** 2026-07-18 · **Author:** gandalf-seam

---

## Grade histogram

| Grade | Count | Kit IDs |
|---|---|---|
| EXACT | 2 | d4-bash · d4-blood-surge |
| CLOSE | 6 | d4-andariel-flurry · d4-auradin-paladin · d4-blazing-abyss-warlock · d4-blood-lance · d4-blood-wave · d4-bone-spear |
| APPROX | 2 | d4-ball-lightning · d4-bouldercane |
| GAPPED | 2 | d3-zuni-carnevil · d4-blade-shift |

MAPPED_DOCKET kits: 2 (zuni-carnevil · blade-shift)

---

## Per-kit one-liners

| Kit | Grade | One-liner |
|---|---|---|
| d3-zuni-carnevil | GAPPED | Pet-core fetish army duplicating player darts; no engine lane for autonomous pet combatants (§CROSS summoner-GAP) |
| d4-andariel-flurry | CLOSE | Melee-blur + Andariel's Visage poison-nova proc; item-defined-archetype poison form; Cold Imbuement current-meta variant noted |
| d4-auradin-paladin | CLOSE | Walk-forward fire-aura loop via Dawnfire conversion; fetched-only Paladin, resource do-not-populate; Consecration rider |
| d4-ball-lightning | APPROX | Clean orbit geometry + Mana economy; element null (MW3: 'Ball Lightning' name ≠ damage attestation) |
| d4-bash | EXACT | One-button Fury generate+spend loop; Hooves AoE extension; inverted-resource do-not-merge |
| d4-blade-shift | GAPPED | Mobility-only with no damage identity; Unhindered = self-movement-state, no ailment lane; negative kit |
| d4-blazing-abyss-warlock | CLOSE | Blazing Scream fire zone + Profane Sentinel secondary; cooldown-only Warlock economy; skill-name erratum noted |
| d4-blood-lance | CLOSE | Lingering lances + echo network between Lanced targets; §C.2 echo-mark rider binding |
| d4-blood-surge | EXACT | Self-origin nova; §C.3 Overpower burst_window binding; one-button AoE |
| d4-blood-wave | CLOSE | Ultimate-converted-to-Core via Hematolagnia; dual-wave via Kessime's Legacy; element null (blood/physical) |
| d4-bone-spear | CLOSE | Piercing line + Bone Storm orbit reset loop; shadow via crosswalk deterministic row (bone→shadow) |
| d4-bouldercane | CLOSE | 5-Boulder orbit ring + Hurricane concentric shell; Spirit resource; element null (physical boulders, no damage-type language) |

---

## T4-door frequency

| T4 token | Kits |
|---|---|
| ZONE_CONTROL | d4-auradin-paladin · d4-bash · d4-blazing-abyss-warlock · d4-blood-lance · d4-blood-surge · d4-blood-wave · d4-bone-spear · d4-bouldercane |
| PERSISTENCE_ENGINE_uptime | d4-andariel-flurry · d4-auradin-paladin · d4-blazing-abyss-warlock · d4-bone-spear · d4-bouldercane |
| MOMENTUM_CASCADE | d4-blood-lance · d4-blood-wave |
| TEMPORAL_CHARGE | d4-bash · d4-blood-surge |
| NETWORK_AMPLIFIER | d4-auradin-paladin |
| null (GAPPED/doorless) | d3-zuni-carnevil · d4-blade-shift |

---

## Candidate files

- **docket-candidates-batch-10.jsonl**: 2 entries (zuni-carnevil summoner-GAP · blade-shift mobility-gap)
- **mint-candidates-batch-10.jsonl**: 0 entries (no new mint-eligible mechanisms — all handled by existing lanes or prior docket classes)

---

## §0 near-misses — statuses wanted but not attested

| Kit | Wanted | Reason blocked |
|---|---|---|
| d4-ball-lightning | lightning element | 'Ball Lightning' = skill name only (MW3); no 'lightning damage' language in fetched rows |
| d4-blood-lance | shadow element | blood/physical; no explicit 'shadow damage' language; THE PHYSICAL RULE = element null |
| d4-blood-surge | shadow element | same as blood-lance |
| d4-blood-wave | shadow element | same; blood/physical domain |
| d4-bouldercane | chill (Hurricane) | no 'slow', 'chill', or 'cripple movement' language in Hurricane fetched rows |
| d4-bouldercane | earth element | physical boulders; no 'earth damage' language; THE PHYSICAL RULE = element null |
| d4-bone-spear | shadow via explicit text | shadow applied via crosswalk deterministic table row (bone→shadow); no fetched 'shadow damage' phrase present |
| d4-blade-shift | any damage ailment | no enemy CC language attested; Unhindered = self-movement-state only |


---

## Forced / notable decisions

- **d4-bone-spear shadow element**: applied via main-law crosswalk deterministic row (bone/necrotic → shadow for D4 necro) rather than explicit fetched damage-type language. Per §7.1 deterministic row applies. Recorded in fidelity_notes.
- **d4-blazing-abyss-warlock skill name**: store attests 'Blazing Scream' (not 'Blazing Abyss'); ERRATA-51 in mech_note; kit_id retained for continuity; source_skill uses correct name.
- **d4-auradin-paladin resource_economy empty**: §C.5 do-not-populate erratum on Paladin contested resource (Faith/Resolve).
- **d3-zuni-carnevil GAPPED**: pet-core identity overwhelms item-defined-archetype consideration; §CROSS summoner-GAP terminal law.
- **d4-andariel-flurry item-defined-archetype**: current Cold Imbuement meta variant noted but Andariel poison form mapped as kit identity per item_id declaration and item_alterations anchor.
- **Overpower not an ailment**: §C.3 binding applied to blood-surge (burst_window) and blood-lance (fidelity note); never emitted as 16-enum entry.
- **d4 Vulnerable**: zero attestations confirmed batch-10 — residual OPEN stands.



## STEWARD AUDIT ADDENDUM — MW4-close 2026-07-18 (gandalf run steward)
D-2c re-audit from COMMITTED jsonl (advisory never trusted). Recount m10: 12 kits, grades {GAPPED:2, CLOSE:8, EXACT:2}, terminal {MAPPED_DOCKET:2, MAPPED:10}; biconditional CLEAN.
**8 element/ailment corrections across 5 kits** (store-verified via full-store context dump):
- **d3-zuni-carnevil** — Poison Dart + Fetish Army: earth->null, poison REMOVED (both). "poison" x5 = ALL skill-name "Poison Dart"; venom/toxic/nature 0 hits. The most poison-thematic build in the corpus fetched ZERO poison-damage behavior = pure name-only. Corpus-quality signal (D3 kit exhibiting d4-class name-heavy pattern). Stays GAPPED/DOCKET.
- **d4-andariel-flurry** — Flurry: earth->null. Element-bleed: Flurry own-store = "encircling blades / rapidly stabs" (physical); poison-nova element belongs to the separate "Andariel's Visage poison nova" row (KEPT earth/poison — "poison nova" descriptor attested). [judgment call — element-bleed, lower-confidence than name-only strikes]
- **d4-ball-lightning** — Ball Lightning: null->lightning RESTORE + APPROX->CLOSE. Mapper OVER-blocked; store attests "balls zap all nearby enemies" / "zapping enemies in proximity" = enemy-directed lightning verb. First over-block correction of the run.
- **d4-bone-spear** — Bone Spear + Bone Storm + Skeleton Mage: shadow->null (x3). "bone" x12 ALL names; "shadow" 0 hits; no necrotic/shadow-damage. bone->shadow routing (crosswalk L24) presupposes an attested register — never triggered on name-only.
- **d4-bouldercane** — Hurricane: chill ailment REMOVED. chill/cold/freeze 0 hits in store (thematically cold, textually silent).
