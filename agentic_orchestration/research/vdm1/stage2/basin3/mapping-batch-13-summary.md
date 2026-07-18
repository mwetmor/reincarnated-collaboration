# Mapping batch-13 summary — VDM-1 basin-3 (MW5, FINAL wave)

**Batch:** m13 · **Kits:** 12 · **Author:** gandalf (SPEC-AUTHOR) · **Date:** 2026-07-18

## Grade histogram

| Grade | Count | Kits |
|---|---|---|
| EXACT | 0 | — |
| CLOSE | 10 | d4-rabies-lacerate, d4-rapid-fire, d4-shadowblight, d4-thorns-barb, d4-tornado-werewolf, d4-touch-of-death, d4-twisting-blades, d4-wind-shear, d4-wing-strike-arbiter, d4-ww-dust-devils |
| APPROX | 1 | di-blood-knight |
| GAPPED → MAPPED_DOCKET | 1 | d4-spiritborn-vortex |

## Per-kit one-liners

- **d4-rabies-lacerate** (CLOSE): item-defined-archetype (Mad Wolf's Glee), Rabies chain→Lacerate burst; poison attested; earth element; PERSISTENCE+TEMPORAL_CHARGE doors.
- **d4-rapid-fire** (CLOSE): ricochet_bounce barrage; element null (imbuement build-variable); ELEMENT_CONVERSION_HYBRID door; energy economy.
- **d4-shadowblight** (CLOSE): shadow ground-pool + corpse-node economy; Blight→CE→Shadowblight pulse; corpse_nodes key; spatial-consumable-resource-node docket.
- **d4-spiritborn-vortex** (GAPPED→MAPPED_DOCKET): component-not-archetype; skill_loop + skill_geometry + capstone all abstained; empty-projection; review-book keep/relabel/excise.
- **d4-thorns-barb** (CLOSE): reactive reflect-damage aura; stat-as-damage-substrate (Razorplate Thorns); RETRIBUTION_ENGINE door; no ailments in dossier.
- **d4-tornado-werewolf** (CLOSE): R-M6 drift-tick Tornado entities; circle token + Fleshrender return pursuit note; form-law (Werewolf); GEOMETRY_PROPAGATION door.
- **d4-touch-of-death** (CLOSE): hold-channel poison DoT chain + swarm spawn; item-defined-archetype (Rod of Kepeleke); fear only in variant (variant-scope blocked from core).
- **d4-twisting-blades** (CLOSE): melee-strike + delayed-return arc; element null; poison only in variant (blocked); Blade Shift self_buff; TEMPORAL_CHARGE door.
- **d4-wind-shear** (CLOSE): FALSIFIED-NEGATIVE redeemed; Calm Breeze aspected line projectile; poison DoT attested; element null (no element verb despite Storm tag).
- **d4-wing-strike-arbiter** (CLOSE): trigger-entered Arbiter form; auto-seeking circle; element null (holy unattested — 'zaps' verb lacks element name); resource contested per erratum.
- **d4-ww-dust-devils** (CLOSE): moving-channel whirlwind + R-M6 Dust Devil drift entities; knockback attested ('knock enemies off their feet'); GEOMETRY_PROPAGATION door; own-language only.
- **di-blood-knight** (APPROX): essence-transform (Swarm of Bats aura+drain); Anger-meter form-threshold; shadow attested in verify_ledger anchor; drain attested; sparse di dossier.

## T4-door frequency (this batch)

PERSISTENCE_ENGINE_saturation ×4 · GEOMETRY_PROPAGATION_overkill ×2 · PHASE_MOMENTUM ×3 · TEMPORAL_CHARGE ×2 · RETRIBUTION_ENGINE ×1 · ELEMENT_CONVERSION_HYBRID ×1 · MOMENTUM_CASCADE ×1 · SACRIFICE_ASCENDANCY ×1 · NETWORK_AMPLIFIER ×1 · DEFENSIVE_TRADEOFF ×1

## Candidates

- **docket-candidates-batch-13.jsonl** — 3 entries:
  1. `spatial-consumable-resource-node`: d4-shadowblight additional attestation (standing docket class)
  2. `component-not-archetype`: d4-spiritborn-vortex (review-book keep/relabel/excise)
  3. `stat-as-damage-substrate`: d4-thorns-barb (first d4-Thorns attestation; accrual to standing family)
- No mint-candidates this batch.

## §0 near-misses — statuses WANTED but could not attest

| Kit | Wanted token | Why blocked |
|---|---|---|
| d4-shadowblight | `curse:decrepify` | "Abhorrent Decrepify" is an ASPECT NAME only — skill-name collision law (§0.4); no movement-slow language in dossier text |
| d4-shadowblight | `root` | Corpse Tendrils pull attested; "root" word absent from dossier |
| d4-tornado-werewolf | `chill` / `knockback` | Neither named in dossier text; ww-dust-devils sibling's knockback is its OWN language and NOT importable |
| d4-twisting-blades | `poison` | Only in variants payload ("Poisoning Assassin" S14 variant) — variant-scope law blocks core-row emission |
| d4-touch-of-death | `fear` | Only in variants payload ("Scourge on cooldown to fear enemies") — variant-scope law blocks core-row emission |
| d4-wind-shear | `lightning` (element) | elem_raw=lightning in corpus but corpus provenance NEVER attests; no lightning/wind damage verb in dossier legal store |
| d4-wing-strike-arbiter | `holy` (element) | elem_raw=holy in corpus; "zaps" is enemy-directed damage verb (MW4 edge 1) but does NOT name an element; no "holy damage" or "divine damage" text |
| d4-thorns-barb | `bleed` | Not named in dossier; no Lacerate reference (separate kit) |
| di-blood-knight | `bleed` | Not named in dossier |

## Forced calls / standing law applications

- **d4-spiritborn-vortex**: empty-projection convention forced by kit-level flag + all skill families abstained; R-M7 honest GAPPED grading.
- **d4-shadowblight**: Reap added to core-skills per ERRATA-51; not mapped as separate skill row (dossier loop text focuses Blight+CE as damage verbs).
- **d4-wind-shear**: FALSIFIED-NEGATIVE (ERRATA-43) — mapped as positive; item-defined-archetype (Calm Breeze form).
- **d4-wing-strike-arbiter**: resource do-not-populate erratum (Faith/Resolve contested §C); cooldown key only.
- **d4-ww-dust-devils**: own-language-only mapping per hot-fact; no cross-kit import of tornado-werewolf language.
- **di-blood-knight**: di resource probe fields not consulted (basin-wide UNRELIABLE per addendum); verify_ledger anchor_quote used as primary shadow-element attestation.

## 3 hardest kits

1. **d4-wind-shear** — FALSIFIED-NEGATIVE handling required careful separation of corpus elem_raw (illegal) from dossier text; "Storm tag" ≠ lightning element; element null counter-intuitive.
2. **d4-wing-strike-arbiter** — "zaps" verb ruling (MW4 edge 1) does not resolve element; holy remains unattested; resource contested erratum applied; form-trigger grammar required careful §CROSS threading.
3. **di-blood-knight** — sparse di dossier; shadow element required verify_ledger anchor as the legal ground ("entraps them in deadly shadows"); Anger-meter is a native di resource with no prior engine lane; APPROX grade honest.


## STEWARD AUDIT ADDENDUM (MW5-close, gandalf)

Store-context adjudication, batch-13. **4 strikes / 1 kit:**
- **di-blood-knight** — Siphon Blood / Abomination / Sanguinate / Ravage: `shadow` → **null** ×4. All 3 store `shadow` hits trace to ONE shoulder legendary's bats-tornado visual ("bloody shadowy tornado of bats"; "deadly shadows summoned with cursed strength") — flavor-prose/item-visual, NOT a damage-type descriptor and no enemy-directed shadow verb (review-book flavor-prose flag governs). **drain KEPT** on Siphon Blood ("steals health from enemies all around (aoe drain)" — cleanly attested; carries kit identity). Grade APPROX unchanged (blood-resource/monster-form deviation is element-independent). *Medium-confidence flavor-prose call, andariel-class.*
