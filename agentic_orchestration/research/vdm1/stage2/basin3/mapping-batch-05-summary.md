# VDM-1 basin-3 mapping batch-05 summary

**Batch:** m05 · **Kits:** 12 · **Author:** gandalf (SPEC-AUTHOR) · **Date:** 2026-07-18

## Grade histogram

| Grade | Count | Kits |
|---|---|---|
| EXACT | 2 | d2-wl-fire, d2-ww-barb |
| CLOSE | 7 | d2-throw-barb, d2-wind-druid, d2-wl-abyss, d2-wl-echoing-strike, d2-ww-sin, d2-zealot, (wind-druid) |
| APPROX | 2 | d2-trapsin, d2-wl-blood-boil |
| GAPPED | 2 | d2-wl-tainted-summoner, d2-wl-void-rift |

EXACT=2 · CLOSE=7 · APPROX=2 · GAPPED=2 · Total=12 (MAPPED=10 · MAPPED_DOCKET=2)

## Per-kit one-liners

- **d2-throw-barb** CLOSE — ranged dual-throw physical; Lacerator curse:amplify on-hit rider; element-neutral
- **d2-trapsin** APPROX — trap placer (placed-proxy) + Shadow Master autonomous combatant gap; DE Sentry corpse-node consumer
- **d2-wind-druid** CLOSE — Tornado R-M6 drift (element-neutral magic); Hurricane water/chill aura; dual delivery shapes
- **d2-wl-abyss** CLOSE — vortex-pull pull+detonate magic AoE; Terror Zone context NOT fear (§0.4 clean); element-neutral magic
- **d2-wl-blood-boil** APPROX — demon-detonation PROXY_FISSION fire AoE; Summon Tainted summoner-GAP rider
- **d2-wl-echoing-strike** CLOSE — ERRATA-46 probe geometry corrected to ranged line out-and-return; physical+magic element-neutral
- **d2-wl-fire** EXACT — three distinct fire-AoE shapes (ring/cone/circle) map cleanly; mana-starved economy confirmed
- **d2-wl-tainted-summoner** GAPPED — ERRATA-55 unattested folk-name + autonomous demon army = summoner-deferral; identity UNSUPPORTED
- **d2-wl-void-rift** GAPPED — kit-level flag; all families abstained; probable phantom/spec-error; zero mappable evidence
- **d2-ww-barb** EXACT — moving-channel whirlwind; §CROSS.5 hot-fact applied; Battle Orders free-toggle aura; element-neutral
- **d2-ww-sin** CLOSE — item-defined-archetype (Chaos runeword oskill WW); claw-speed math fidelity delta noted
- **d2-zealot** CLOSE — commitment-locked 5-hit melee; Fanaticism free-toggle aura; econ-recrawl 2 mana/use verified

## T4-door frequency

| Door | Count |
|---|---|
| ELEMENT_CONVERSION_PHYSICAL | 3 (throw-barb, ww-barb, ww-sin) |
| ZONE_CONTROL | 2 (wl-abyss, wl-fire) |
| PROXY_ASCENSION | 2 (trapsin, tainted-summoner) |
| MOMENTUM_CASCADE | 2 (ww-barb, zealot) |
| PERSISTENCE_ENGINE_uptime | 2 (wind-druid, wl-abyss) |
| PROXY_FISSION | 1 (blood-boil) |
| PERSISTENCE_ENGINE_saturation | 1 (wl-fire) |
| TEMPORAL_CHARGE | 1 (zealot) |
| GEOMETRY_COLLAPSE | 1 (wl-abyss) |
| GEOMETRY_PROPAGATION_cascade | 0 |
| null (GAPPED/doorless) | 2 (void-rift: null per MW1-close; tainted-summoner: PROXY_ASCENSION retained) |


## Candidates

**docket-candidates-batch-05.jsonl:** 3 entries
1. `summoner-deferral` — d2-wl-tainted-summoner + d2-wl-blood-boil rider (autonomous Warlock demon combatants; new d2 class attestations of summoner-deferral)
2. `spatial-consumable-resource-node` — d2-trapsin Death Sentry CE (trap-mediated corpse consumption variant)
3. `loot-economy-identity` — d2-throw-barb weapon-choice note (review-book texture; no docket escalation)

**mint-candidates:** none this batch.

## §0 near-misses (statuses wanted but not attested)

- **d2-wl-abyss / Abyss "Sigil: Death":** wanted `execute` on the Abyss skill itself — not attested; Sigil:Death is a separate capstone skill that attests execute-field behavior. Emitted on Sigil:Death only.
- **d2-trapsin / Death Sentry:** wanted `burn` from fire component of Corpse Explosion — not attested as burn status; CE attests "Fire and Physical Damage" (delivery, not ailment). No burn emitted.
- **d2-wind-druid / Tornado:** wanted a physical damage ailment (bleed/stun) to carry the physical magic damage identity — not attested. Physical rule: element-neutral only; no ailment without named status in dossier.
- **d2-wl-blood-boil / Blood Boil:** wanted `burn` DoT on fire component — not attested; dossier attests split fire+physical damage (instant, not DoT). No burn emitted.
- **d2-zealot / Zeal:** wanted `stun` from commitment-locked rapid-hits — not attested. Stun is not named anywhere in fetched Zealot text.

## Hardest three kits

1. **d2-wl-void-rift** — Kit-level flag with zero attested evidence across all dossier families. Nothing to map honestly; all surfaces empty. §E.5 discipline required resisting the temptation to project a void/rift geometry from the name alone.
2. **d2-wl-tainted-summoner** — ERRATA-55 unattested folk-name compounds with summoner-GAP core loop. Two-layer honesty problem: can't confirm the name OR map the autonomous-army identity. Verified mechanics exist via Blood Boil guide overlap, but the kit-as-named has UNSUPPORTED identity.
3. **d2-wl-abyss** — Terror Zone language required active §0.4 discipline to avoid a phantom fear token. Abyss pull-then-detonate is a composite mechanic (pull / DoT / detonate) with no single clean geometry; vortex_pull was the least-wrong choice with fidelity note.

## Batch hot-facts applied

- ww-barb moving-channel: §CROSS.5 applied; delivery_notes state moving explicitly
- wl-void-rift kit-level flag: §E.5 applied; sparse evidence mapped honestly; t4_doors=null (GAPPED/doorless per MW1-close)
- wl-abyss Terror Zone language: §0.4 discipline applied; no fear token
- wl-tainted-summoner ERRATA-55: honest-U governs; identity UNSUPPORTED confirmed via verify_ledger
- d2 magic-damage: MW1-close element-NEUTRAL applied (wl-abyss, wl-echoing-strike, wind-druid Tornado)
- freeze vs chill: no freeze attestation in batch; chill from Hurricane cold-slow correctly distinguished

## Errata and amendments consumed

- ERRATA-46 (wl-echoing-strike probe geometry): probe 'melee' contradicted by fetched 'ranged projectile' — fetched text authoritative; line geometry used
- ERRATA-55 (wl-tainted-summoner folk-name): honest-U register governs
- BACKFILL-3 / INGEST-13: all dossier rows read as post-ingest state
