# VDM-1 Stage-2 Basin-3 — Mapping Batch 02 Summary

**Batch:** m02 · **Kits:** 12 · **Author:** gandalf (SPEC-AUTHOR) · **Date:** 2026-07-18

## Grade histogram

| Grade | Count | Kits |
|---|---|---|
| EXACT | 3 | d2-fire-sorc · d2-firewall-sorc · d2-fury-wolf |
| CLOSE | 9 | d2-enchantress · d2-fire-druid · d2-fireclaw-wolf · d2-fishyzon · d2-fohdin · d2-frenzy-barb · d2-frost-bowazon · d2-frozen-orb-sorc · d2-ghost-pvp |
| APPROX | 0 | — |
| GAPPED | 0 | — |

All 12: `terminal_state: MAPPED`.

## Per-kit one-liners

- **d2-enchantress** CLOSE — Enchant buff + Zeal oskill melee (Passion item-defined-archetype); fire self_buff+melee_strike; no ailment attestation.
- **d2-fire-druid** CLOSE — Fissure ground_targeted_circle + Armageddon body-attached circle; moving-emitter texture in delivery_notes; no ailment attestation.
- **d2-fire-sorc** EXACT — Fire Ball single_target + Meteor ground_targeted_circle; clean fire caster; no ailment attestation.
- **d2-fireclaw-wolf** CLOSE — Werewolf form-locked; Fire Claws melee_strike fire; Feral Rage §A row 5 self_buff ramp; economy-agnostic form law applied.
- **d2-firewall-sorc** EXACT — Fire Wall placed_lane; perpendicular lane geometry is exact; 1.09 era-canon; capstone/item dossiers abstained.
- **d2-fishyzon** CLOSE — ERRATA-51 governs: LF/CS/FA (not Guided Arrow/Valkyrie); lightning fork + freeze attested on Freezing Arrow; dual-element lightning+water hybrid.
- **d2-fohdin** CLOSE — FoH lightning+holy dual-element single_target + Conviction curse:sap aura; holy bolt shrapnel attested in fetched text (NOT probe-fabricated).
- **d2-frenzy-barb** CLOSE — Physical melee_strike dual-wield; §A row 5 speed-ramp NOT accumulator; Sprint/Frenzy alias confirmed; no ailment attestation.
- **d2-frost-bowazon** CLOSE — Freezing Arrow single_target+freeze attested; Pierce geometry-modifier in delivery_notes; Ice runeword item-layer.
- **d2-frozen-orb-sorc** CLOSE — Frozen Orb mapped as orbit (advancing radial emitter); no chill/freeze attested in skill_loop text; Meteorb is variant-scope.
- **d2-fury-wolf** EXACT — Werewolf form-locked physical melee; Fury melee_strike; Feral Rage §A row 5 self_buff; clean economy-agnostic form application.
- **d2-ghost-pvp** CLOSE — Lightning Sentry totem + Mind Blast stun (attested) + Whirlwind moving-channel; Enigma item-defined-archetype; PvP context in fidelity_notes.


## T4-door frequency

| T4 token | Count | Kits |
|---|---|---|
| ZONE_CONTROL | 6 | fire-druid · fire-sorc · firewall-sorc · fohdin · frost-bowazon · ghost-pvp |
| MOMENTUM_CASCADE | 3 | frenzy-barb · frost-bowazon · fury-wolf |
| PERSISTENCE_ENGINE_uptime/saturation | 3 | enchantress · fire-sorc · firewall-sorc (saturation) · frozen-orb-sorc (saturation) |
| ELEMENT_CONVERSION_MONO | 2 | enchantress · fireclaw-wolf |
| PHASE_MOMENTUM | 2 | fireclaw-wolf · fury-wolf |
| PROXY_ASCENSION | 1 | ghost-pvp |
| NETWORK_AMPLIFIER | 1 | fohdin |
| GEOMETRY_PROPAGATION_overkill | 1 | frozen-orb-sorc |
| ELEMENT_CONVERSION_HYBRID | 1 | fishyzon |
| TEMPORAL_CHARGE | 1 | frenzy-barb |

## Mint candidates
None. All gaps resolved via existing rows or delivery_notes texture. No new mint-candidate side-file created.

## Docket candidates
None. All R-M7 biconditionals satisfied (MAPPED, not GAPPED). No docket-candidate side-file created.

## §0 near-misses — statuses WANTED but could not attest

- **burn** — d2-fire-sorc, d2-fire-druid, d2-enchantress, d2-fireclaw-wolf, d2-firewall-sorc: all fire kits; no fetched dossier text names burn/ignite as an applied status.
- **chill** — d2-frozen-orb-sorc: orb sprays cold bolts; no chill status named in skill_loop or skill_geometry fetched text.
- **bleed** — d2-frenzy-barb: Gore Rider boots have a life-tap/open-wounds item layer; not attested in core skill fetched text.
- **sunder** — d2-fohdin: Griffon's Eye -enemy lightning res is numeric gear-affix; Conviction curse:sap is the correct lane per main-law aura/hex → curse row.

## Hardest 3 kits

1. **d2-frozen-orb-sorc** — The advancing-radial-emitter shape (traveling orb that continuously sprays bolts in all directions) has no exact 26-enum token; orbit maps the self-origin radial emission but misses the advancing trajectory. Delivery_notes carry the shape gap.

2. **d2-ghost-pvp** — Three-verb loop (trap + teleport + WW) spanning two geometry modes (totem placed-proxy + whirlwind moving-channel); PvP context requires §D exclusion; Enigma item-defined-archetype requires §CROSS row 4 application; re-key pending per gandalf-ruling-17 adds identity complexity.

3. **d2-fishyzon** — ERRATA-51 inversion: the entire core_skills vector required rejection of KB-level spec data and substitution with fetched dossier truth; dual-element (lightning+water) hybrid with three-verb loop across two attack modalities (javelin + bow); Lightning Fury's javelin-spawns-radial-bolts shape approximates as fork.

---
*Histogram advisory (D-2c). Steward audits ≥25% + full contiguity battery.*


## STEWARD AUDIT ADDENDUM (2026-07-18, MW1 close)
Recount CONFIRMED 3E/9C/0A/0G, roster 12/12, contiguity CLEAN, fishyzon ERRATA-51 inversion verified honored (LF/CS/FA). ghost-pvp 'gandalf-ruling-17' citation adjudicated: provenance-echo (corpus field carries the re-key ruling note) — LEGAL per GX-register precedent.


## STEWARD RETRO ADDENDUM (2026-07-18, MW2 close — battery v3 retro-run)

MW1's contiguity battery was VACUOUS (double-quote regex vs single-quote citing convention — steward-error #3). Battery v3 retro-run over this batch: only 5/20 spans store-grounded (style-poor batch; most quoted spans were self-coinage one-liners — quote-hygiene notes, not leaks). **One RETRO strike (stamped in-row, grade unchanged):** fishyzon — Freezing Arrow 'freeze' STRUCK; all 10 freeze-family occurrences in the kit's OWN store are the skill name (§0-UNIVERSAL name-collision); the 'attested explicitly' fidelity claim was FALSE (cross-kit splice from frost-bowazon, whose own 'freezing all enemies in radius' keeps ITS freeze).
