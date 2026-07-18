# VDM-1 Basin-3 Mapping Batch-12 Summary

**Batch:** m12 (stage1 batch-12 roster, all d4)
**Author:** gandalf (SPEC-AUTHOR)
**Date:** 2026-07-18
**Kits:** d4-ice-shards · d4-incinerate · d4-infinimist · d4-kick · d4-lightning-spear · d4-lightning-storm · d4-mighty-throw · d4-minion-necro · d4-payback-sb · d4-pen-shot · d4-pulverize · d4-quill-volley

---

## Grade histogram

| Grade | Count | Kits |
|---|---|---|
| EXACT | 2 | d4-lightning-storm, d4-pulverize |
| CLOSE | 8 | d4-ice-shards, d4-incinerate, d4-kick, d4-lightning-spear, d4-mighty-throw, d4-payback-sb, d4-pen-shot, d4-quill-volley |
| APPROX | 0 | — |
| GAPPED | 2 | d4-infinimist, d4-minion-necro |

---

## Per-kit one-liners

| Kit | Grade | One-liner |
|---|---|---|
| d4-ice-shards | CLOSE | Water/freeze seeking volley; Frost Nova setup + conditional re-seek (§C.1 target-frozen); item-defined pierce form |
| d4-incinerate | CLOSE | Falsified-negative redeemed; rooted fire beam_channel; Overheating burst_window; PERSISTENCE_ENGINE_uptime door |
| d4-infinimist | GAPPED | Blood Mist invulnerability cycle + CE corpse-core loop; spatial-consumable-resource-node docket; cooldown_refresh_on_proc via lucky_hit |
| d4-kick | CLOSE | Falsified-negative redeemed; Fury-pool finisher; rotation builds Chainscourged stacks → Kick burst; TEMPORAL_CHARGE door |
| d4-lightning-spear | CLOSE | Hot-fact: Ice Blades struck (CONTRADICTED); actual bar Lightning Spear + Unstable Currents + Ball Lightning; stun attested; PROXY_ASCENSION door |
| d4-lightning-storm | EXACT | Toggled lightning aura via Hero of the Storm; Storm Shepherd's Set makes Spirit free; continuous zone zap; PERSISTENCE_ENGINE_uptime |
| d4-mighty-throw | CLOSE | Fire element attested via Bane of Ahjad-Den detonation; auto-throw + pulsing zone; WW carrier; ZONE_CONTROL door |
| d4-minion-necro | GAPPED | Autonomous skeleton army + golem = summoner-deferral docket; Decrepify attests curse:decrepify; no T4 doors |
| d4-payback-sb | CLOSE | Spiritborn Vigor inverted-loop (100% restore per cast); Rod of Kepeleke free spam; geometry unknown (single_target default) |
| d4-pen-shot | CLOSE | Line pierce; Eaglehorn ricochet_bounce variant noted; Shadow Clone shadow element; Heartseeker trigger rider via Nilfur's Narrow Eye |
| d4-pulverize | EXACT | Werebear ground_slam; form law; Overpower burst_window; ZONE_CONTROL + PHASE_MOMENTUM doors |
| d4-quill-volley | CLOSE | Fan multi_projectile; partial Vigor inverted-loop (40-50% restore); 4-guardian Berú stack unengined; RESOURCE_CONVERSION door |

---

## T4-door frequency

| Door | Count | Kits |
|---|---|---|
| RESOURCE_CONVERSION | 2 | d4-kick, d4-payback-sb, d4-quill-volley (3 inc.) |
| ZONE_CONTROL | 3 | d4-ice-shards, d4-mighty-throw, d4-pulverize |
| PERSISTENCE_ENGINE_uptime | 2 | d4-incinerate, d4-lightning-storm |
| TEMPORAL_CHARGE | 2 | d4-ice-shards, d4-kick |
| PROXY_ASCENSION | 1 | d4-lightning-spear |
| PHASE_MOMENTUM | 1 | d4-pulverize |
| GEOMETRY_PROPAGATION_overkill | 1 | d4-pen-shot |
| NETWORK_AMPLIFIER | 1 | d4-lightning-storm |
| PERSISTENCE_ENGINE_saturation | 1 | d4-mighty-throw |
| null (GAPPED/doorless) | 2 | d4-infinimist, d4-minion-necro |

*Note: RESOURCE_CONVERSION appears in 3 kits (kick + payback-sb + quill-volley).*

---

## Candidates

**Docket candidates:** 2
- `d4-infinimist` → spatial-consumable-resource-node (corpse-CORE loop; §CROSS row 1)
- `d4-minion-necro` → summoner-deferral (autonomous skeleton army + golem; §CROSS row 2)

**Mint candidates:** 0

---

## §0 near-misses (statuses wanted but could not attest)

| Kit | Wanted | Why blocked |
|---|---|---|
| d4-incinerate | burn | Aspect of Conflagration references 'Burning' as a condition modifier; no enemy burn status named in fetched text; MW3 law: store DAMAGE/STAT language required for ailment, not aspect-name |
| d4-pen-shot | freeze | Variants payload lists 'Cold (Shadow/Freeze)' as variant label only; freeze not attested as enemy status in fetched behavior/damage language; MW3 law: variant-NAME is never ailment ground |
| d4-minion-necro | curse:decrepify on Blood Mist | Decrepify is attested in skill_loop but Blood Mist cycling is the dominant loop verb; Decrepify is economy texture in this kit; emitted only on Decrepify skills[] row |
| d4-lightning-spear | sunder | No 'increased damage taken' or sunder language in store; stun (not sunder) attested via 'through stuns, proccing Shocking Impact' |
| d4-pulverize | stun | Ground slam could imply stun but no stun status named in fetched store text |

---

## Forced / notable calls

- **d4-lightning-spear hot-fact:** Ice Blades battery claim X (CONTRADICTED verify_ledger); actual 6-slot bar is Lightning Spear + Ball Lightning + Unstable Currents + Chain Lightning + Charged Bolts. Ice Blades absent from mapping row entirely.
- **d4-incinerate + d4-kick falsified-negatives:** both negative=1 in corpus, both negative_canon CONTRADICTED by verify_ledger; both mapped as redeemed VoH/S12-era forms per §CROSS row 4.
- **d4-infinimist Blood Mist clarification:** Blood Mist invulnerability is player-side defense, not enemy status — hot-fact §C.4 note honored; no ailment emitted for Blood Mist.
- **d4-mighty-throw fire element:** fire_damage language attested via item_alterations anchor ('causes instant detonation of pulses as fire damage'); MW3 element law satisfied (DAMAGE language, not name).
- **d4-payback-sb + d4-quill-volley Vigor inversion:** basin-2 inverted-resource no-merge ruling applied to both; vigor keyed as 'inverted-loop' separate from regen_shape.
- **d4-minion-necro t4_doors null:** GAPPED/doorless per MW1 standing amendment (GAPPED kits emit t4_doors null, never []).


## STEWARD AUDIT ADDENDUM — MW4-close 2026-07-18 (gandalf run steward)
Recount m12: 12 kits, grades {CLOSE:8, GAPPED:2, EXACT:2}, terminal {MAPPED:10, MAPPED_DOCKET:2}; biconditional CLEAN.
**7 element/ailment corrections across 3 kits** (name-only, store-verified):
- **d4-lightning-spear** — Lightning Spear + Ball Lightning + Unstable Currents: lightning->null (x3); STUN kept on Lightning Spear ("chain stuns via shocking impact"). 9 lightning hits ALL names + "shocking impact" passive; NO zap-verb. MARQUEE SPECIMEN: identical "Ball Lightning" skill = lightning in d4-ball-lightning (has "zap enemies") but NULL here (name-only) — same name, opposite verdict, store evidence governs.
- **d4-minion-necro** — Raise Skeleton + Golem + Decrepify: shadow->null (x3); curse:decrepify KEPT on Decrepify ("cast decrepify to curse enemies"). shadow 0 hits; minions "deal sustained damage" element-unstated. Third necro name-only case.
- **d4-pen-shot** — Shadow Clone: shadow->null. "shadow clone for unstoppable and damage boost" = buff/utility, not shadow damage; Penetrating Shot correctly null (physical pierce).
KEEPS confirmed: infinimist shadow ("shadow dots deal damage while inside mist"), lightning-storm lightning ("aura zaps all nearby enemies"), ice-shards water/freeze, incinerate fire, mighty-throw fire.
