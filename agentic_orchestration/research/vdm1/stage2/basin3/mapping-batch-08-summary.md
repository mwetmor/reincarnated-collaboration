# VDM-1 basin-3 mapping batch-08 summary

**Batch:** m08 · **Kits:** 12 · **Date:** 2026-07-18

## Grade histogram

| Grade | Count | Kits |
|---|---|---|
| EXACT | 0 | — |
| CLOSE | 10 | natalya-rov, poj-tempest-rush, raekor-boulder, raiment-shenlong, rolands, s6-impale, shield-bash, sotl-hammer, spectral-blade, sunwuko-wol |
| APPROX | 1 | pestilence-lance |
| GAPPED | 1 | rathma-aotd |

Terminal states: 10× MAPPED · 2× MAPPED_DOCKET

## Per-kit one-liners

| Kit | Grade | One-liner |
|---|---|---|
| d3-natalya-rov | CLOSE | RoV at-target zone + Strafe moving-channel CDR-reset loop; Hatred economy; PERSISTENCE_ENGINE_uptime door; CDR-reset-on-hit has no native engine analog |
| d3-pestilence-lance | APPROX | Corpse Lance shadow missile; spatial-consumable-resource-node docket (§CROSS); auto-fire-from-corpse-position unlaneable; LotD burst window; Essence+corpse_nodes economy |
| d3-poj-tempest-rush | CLOSE | Moving-channel whirlwind through packs; Flurry 100-stack→icy explosion = two-tier accumulator accrual; Spirit economy; water elem_s from attested 'icy explosion' |
| d3-raekor-boulder | CLOSE | Furious Charge dash + Boulder Toss Fury-dump; two-tier accumulator confirmed (charge accumulate → Fury-dump release); ERRATA-49 S26 rework governs |
| d3-raiment-shenlong | CLOSE | Lightning generator melee-arc + Shenlong Spirit-dump burst; chill from 'Crippling Wave' movement-slow; two-tier accumulator accrual; inverted-resource shape noted |
| d3-rathma-aotd | GAPPED | Summoner-deferral: Command Skeletons + Revive persistent army is pet-core GAP; AotD large-zone maps; ERRATA-51 removes Skeletal Mage line |
| d3-rolands | CLOSE | Sweep Attack 360° melee_arc; 375% AS cap engine = approximated MOMENTUM_CASCADE; fire elem_s from attested Blazing Sweep rune |
| d3-s6-impale | CLOSE | Single-target knife execution; Hatred economy with Karlei's Point near-infinite refund; Shadow Power self_buff; physical element-neutral |
| d3-shield-bash | CLOSE | Negative=1 kit mapped in redeemed/attested form; directional line charge-projectile; Wrath economy; stun NOT emitted (only in inadmissible kb-class claim_text) |
| d3-sotl-hammer | CLOSE | Orbit spiral per §A row 6 + PERSISTENCE_ENGINE_uptime door (30-orbit hot-fact); holy element attested; Falling Sword blink triggers SotL 4pc marks |
| d3-spectral-blade | CLOSE | ERRATA-43 falsified-negative — redeemed DMO form mapped; melee_arc + Slow Time chill zone; arcane→shadow; zero-cost signature in DMO |
| d3-sunwuko-wol | CLOSE | Bell-drop ground_targeted_circle at-target; holy element; Sunwuko clone-multiplication trigger_grammar rider; Spirit economy with Epiphany sustain |

## T4 door frequency (batch-08)

| Door | Count |
|---|---|
| PERSISTENCE_ENGINE_uptime | 5 (natalya-rov, poj-tempest-rush, s6-impale, sotl-hammer, sunwuko-wol) |
| TEMPORAL_CHARGE | 7 (natalya-rov, poj-tempest-rush, raekor-boulder, raiment-shenlong, rolands, shield-bash, sotl-hammer) |
| MOMENTUM_CASCADE | 4 (natalya-rov, poj-tempest-rush, raekor-boulder, rolands) |
| RESOURCE_CONVERSION | 2 (raekor-boulder, raiment-shenlong) |
| ZONE_CONTROL | 3 (sotl-hammer, spectral-blade, sunwuko-wol) |
| GEOMETRY_COLLAPSE | 2 (s6-impale, shield-bash) |
| PHASE_MOMENTUM | 1 (raiment-shenlong) |
| PROXY_ASCENSION | 1 (pestilence-lance) |
| null | 1 (rathma-aotd — summoner-docked) |

## Candidates

**docket-candidates-batch-08.jsonl** — 3 entries:
1. `spatial-consumable-resource-node` docket — pestilence-lance positional auto-cast-per-corpse variant
2. `summoner-deferral` docket — rathma-aotd minion-hit-resets-ultimate-cooldown variant
3. `two-tier-accumulator` family accrual — raekor-boulder (Fury-dump) + raiment-shenlong (Spirit-dump); family now 8+ instances

No mint-candidates (no quantitative mints; all approximations carried by existing family accruals).

## §0 near-misses (wanted to emit, could not attest)

- **stun (d3-shield-bash):** negative_canon claim mentioned "stun-window geometry" but verdict = UNSUPPORTED; claim_text = inadmissible kb-class; no stun in fetched dossier text. Blocked.
- **burn (d3-natalya-rov, d3-s6-impale):** fire-themed rune names present but no "burn" status named in fetched skill text. Blocked.
- **holy (d3-rolands Sweep Attack / Akarat's):** Crusader class-thematic; no explicit 'holy damage' for Sweep Attack in dossier; blocked on class-thematic-element-import rule. Akarat's Champion self_buff holy carried as class-flavor fidelity note only.
- **freeze (d3-poj-tempest-rush):** 'icy explosion' attests water element but no 'freeze' status named in fetched text. Blocked; water elem_s only.

## Anything forced

- **ERRATA-51 (rathma-aotd):** Skeletal Mages line absent from mapping per erratum (verify_ledger CONTRADICTED verdict governs). Core skills corrected to Command Skeletons + Revive.
- **ERRATA-43 (spectral-blade):** Falsified-negative — mapped redeemed DMO form per batch hot-facts. Negative flag retained; review-book decision.
- **d3-shield-bash negative=1:** Verdicts govern — mapped attested/redeemed Roland's-set form; negative_canon claim UNSUPPORTED by ledger.
- **Rathma t4_doors=null:** Summoner-docked; no clean door assignment without summoner lane resolution.

## 3 hardest kits

1. **d3-rathma-aotd** — ERRATA-51 correction + summoner-GAP for army core + need to distinguish AotD (maps) from the minion reset-engine (does not). Required careful ERRATUM discipline.
2. **d3-pestilence-lance** — §CROSS corpse-node docket class + auto-fire-from-corpse-position = two compounding gaps; had to honor R-M7 biconditional for the APPROX vs GAPPED boundary.
3. **d3-spectral-blade** — ERRATA-43 falsified-negative + DMO-redeemed form mapping + arcane→shadow element routing + chill attestation via Slow Time; required layered law application.
