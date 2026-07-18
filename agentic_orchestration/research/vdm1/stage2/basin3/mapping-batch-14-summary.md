# Mapping batch-14 summary — VDM-1 basin-3 MW5 (FINAL WAVE)

**Kits:** 12 · **Date:** 2026-07-18 · **Author:** gandalf (SPEC-AUTHOR)

## Grade histogram

| Grade | Count | Kits |
|---|---|---|
| EXACT | 0 | — |
| CLOSE | 4 | cyclone-strike-monk-base · draw-quarter-crusader · frenzy-barb · hota-wotb-barb |
| APPROX | 4 | bone-wall-necro-pvp · crusader-banner-support · cyclone-monk-pvp · druid-bear |
| GAPPED → MAPPED_DOCKET | 4 | bombardment-wizard-pvp · corpse-explosion-necro · essence-transfer · inferno-ladder |

## Per-kit one-liners

| Kit | Grade | Key note |
|---|---|---|
| di-bombardment-wizard-pvp | GAPPED | Kit-level-flag; all dossier families abstained; d3→di misapplication candidate; zero store |
| di-bone-wall-necro-pvp | APPROX | PvP barrier-placement CC; Bone Wall blocking function has no engine lane; no ailments attested despite CC identity |
| di-corpse-explosion-necro | GAPPED | Corpse-core identity; spatial-consumable-resource-node docket; CE delivery maps but kill→corpse→detonate loop is unrepresentable |
| di-crusader-banner-support | APPROX | Party-buff identity (Holy Banner crit buff + Conjuration of Light damage immunity) loses core value in solo-PvE scope |
| di-cyclone-monk-pvp | APPROX | PvP pull-cluster-CC-lock identity; no ailments attested; element null (wind noun, no damage verb) |
| di-cyclone-strike-monk-base | CLOSE | BACKFILL INSERT; single-skill base-cell; vortex_pull + root-while-charging; Spirit resource UNSUPPORTED |
| di-draw-quarter-crusader | CLOSE | Movement-identity horse charge; root attested via 'bind'; sustained-drag texture partial gap |
| di-druid-bear | APPROX | Werebear form maps; stun attested; summon companions (wolf/grizzly/oak sage) = summoner-GAP; Primal Power resource CONTRADICTED |
| di-essence-transfer | GAPPED | SYSTEM kit §D.3; item-crafting economy; empty-projection; review-book system-register |
| di-frenzy-barb | CLOSE | Stack-ramp attack speed; ERRATA-52 Sprint excluded; ramp_per_s economy; TEMPORAL_CHARGE door |
| di-hota-wotb-barb | CLOSE | Ground slam + WotB burst window + Ground Stomp stun; stun attested in skill_loop payload; cooldown economy |
| di-inferno-ladder | GAPPED | SYSTEM kit; numeric progression spine; empty-projection; review-book system-register |

## T4-door frequency (non-null, non-GAPPED kits)

| Door | Count | Kits |
|---|---|---|
| NETWORK_AMPLIFIER | 1 | crusader-banner-support |
| TEMPORAL_CHARGE | 2 | frenzy-barb · hota-wotb-barb |
| MOMENTUM_CASCADE | 1 | hota-wotb-barb |


## §0 near-misses — statuses WANTED but could not attest

| Kit | Status wanted | Why blocked |
|---|---|---|
| di-bone-wall-necro-pvp | stun | 'stun chains' in mech_note only (ILLEGAL probe field); no stun word in dossier store |
| di-cyclone-monk-pvp | stun/root | Imprisoned Fist labeled 'precise CC' in store but no status named; mech_note 'knockback→pull' re-key is ILLEGAL |
| di-draw-quarter-crusader | holy element | 'holy chains' = mechanism noun; no 'deals holy damage' verb phrase attested; element null per MW4 |
| di-hota-wotb-barb | earth element | 'shakes the earth' = physical flavor; no 'earth damage' verb |
| di-frenzy-barb | resource economy (Fury) | verify_ledger UNSUPPORTED; DI probe fields UNRELIABLE; Fury name-only |
| di-crusader-banner-support | resource economy (Wrath) | verify_ledger UNSUPPORTED; DI probe fields UNRELIABLE |

## Blocked tokens (absent from emitted rows per law)

- `stun` blocked from di-bone-wall-necro-pvp (mech_note-only; ILLEGAL ground)
- `knockback` blocked from di-cyclone-monk-pvp (corpus re-key note in mech_note = ILLEGAL; replaced by store-attested pull)
- `holy` element blocked from di-draw-quarter-crusader (name-noun only, no damage verb)
- `earth` element blocked from di-hota-wotb-barb ('shakes the earth' = flavor, no damage verb)
- `burn`/`poison` blocked from di-corpse-explosion-necro (Rotspur 'DoT component' names no status)

## Docket candidates

3 entries in `docket-candidates-batch-14.jsonl`:
1. **spatial-consumable-resource-node** — standing family accrual (di-corpse-explosion-necro, third corpse-core attestation)
2. **summoner-deferral** — standing family accrual (di-druid-bear, wolf/grizzly/oak sage autonomous combatants)
3. **placement-barrier-blocking** — new gap candidate (di-bone-wall-necro-pvp, Bone Wall pathing-blocker has no engine lane)

## Three hardest kits

1. **di-bombardment-wizard-pvp** — Zero store (all abstained); identity UNSUPPORTED; kit-level-flag d3→di misapplication. Honest GAPPED with zero evidence to map.
2. **di-druid-bear** — 2025 post-cutoff class; Primal Power resource CONTRADICTED against Spirit in verify_ledger; summon companion layer is summoner-GAP; form-law application required. Resource probe ban applied throughout.
3. **di-bone-wall-necro-pvp** — PvP identity with no combat ailments in store despite CC-centric description; barrier-blocking function has no engine lane; mech_note stun-chain language all ILLEGAL.

## Forced calls

- **di-cyclone-strike-monk-base geometry:** vortex_pull is the closest 26-enum approximation; no exact pull-vortex enum exists.
- **di-corpse-explosion-necro Bone Spikes element:** shadow from main-law bone/necrotic register (secondary skill only; no shadow damage verb in store — noted in fidelity).
- **SYSTEM kits (essence-transfer, inferno-ladder):** t4_doors=[] per §D convention.
- **di-bombardment-wizard-pvp t4_doors:** null (not []) — kit-level-flag with zero store differs from SYSTEM kit convention; SYSTEM convention requires a populated system shape; this kit has none.
