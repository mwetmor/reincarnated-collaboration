# mapping-batch-p05 summary — Undecember (ud cluster, 12 kits)

## Grade histogram

| Grade | Count | Kits |
|---|---|---|
| EXACT | 4 | ud-whirlwind-str, ud-flamethrower-channel, ud-ice-crystal-arrow, ud-spread-rapid-dex |
| CLOSE | 5 | ud-cwc-spin-caster, ud-toxic-flame, ud-lightning-vortex, ud-illusion-family, ud-seal-veil-daimonios |
| APPROX | 0 | — |
| GAPPED | 3 | ud-multishot-link, ud-snowstorm-frost, ud-summon-strand |

EXACT 33% · CLOSE 42% · GAPPED 25%

## Per-kit one-liners

- **ud-whirlwind-str** — physical channel spin, no element, whirlwind geometry; clean EXACT
- **ud-flamethrower-channel** — genuine fire beam_channel with burn (Arson DoT on cancel); EXACT
- **ud-cwc-spin-caster** — physical whirlwind + Blizzard cold proc via Spell Activation while Channeling; CLOSE (chill/freeze on Blizzard structural but not verbatim-named in this kit's dossier)
- **ud-ice-crystal-arrow** — cold chain projectile, chill+freeze explicitly attested; EXACT
- **ud-toxic-flame** — POISON ONLY (errata applied); piercing line geometry (not small-AOE); earth family; CLOSE
- **ud-lightning-vortex** — MELEE errata applied; element=null (name-only); shock ailment attested; CLOSE
- **ud-illusion-family** — MECHANICS CONTRADICTED: stack-proc auto-fire, not echo-copies; multi_projectile proc geometry; CLOSE
- **ud-multishot-link** — pure geometry-modifier link rune, no standalone skill loop; GAPPED/MAPPED_DOCKET
- **ud-seal-veil-daimonios** — reservation-economy lattice (Seal stack + Veil toggle); primary damage defers to LV; CLOSE
- **ud-snowstorm-frost** — FULLY UNATTESTED (N2): all verify UNSUPPORTED, all dossier abstained; honest empty; GAPPED/MAPPED_DOCKET
- **ud-spread-rapid-dex** — physical kite-archer cone + multi_projectile; Multishot link modifier; EXACT
- **ud-summon-strand** — pet-core summoner with fusion mechanic; fire element on Rune Knight via 'breathes Fire'; summoner-deferral; GAPPED/MAPPED_DOCKET

## T4-door frequency (across 12 kits)

| T4 token | Count |
|---|---|
| PERSISTENCE_ENGINE_uptime | 4 |
| MOMENTUM_CASCADE | 3 |
| TEMPORAL_CHARGE | 3 |
| ELEMENT_CONVERSION_PHYSICAL | 3 |
| GEOMETRY_PROPAGATION_cascade | 3 |
| PERSISTENCE_ENGINE_saturation | 2 |
| ELEMENTAL_ECHO | 2 |
| ZONE_CONTROL | 1 |
| ELEMENT_CONVERSION_HYBRID | 1 |
| DUAL_PROXY | 1 |
| PROXY_ASCENSION | 1 |
| COMPANION_CONTRACT | 1 |
| NETWORK_AMPLIFIER | 1 |
| RESOURCE_CONVERSION | 1 |
| GEOMETRY_PROPAGATION_overkill | 1 |
| PHASE_MOMENTUM | 1 |

## Candidate files

- `docket-candidates-batch-p05.jsonl` — 3 entries: geometry-modifier-link-rune (multishot-link), summoner-deferral (summon-strand), fully-unattested-empty-projection (snowstorm-frost)
- No mint candidates

## §0 near-misses — elements/statuses WANTED but cannot attest

- **ud-lightning-vortex — lightning element:** pocketgamer build guide uses "Cleave Lightning area DMG" as compound build-description; rune page "Swings weapon to damage multiple enemies and create a vortex" carries no element qualifier. Name-only: element=null. This is the largest near-miss in the batch — the build is thematically lightning but the rune page is element-silent.
- **ud-cwc-spin-caster — chill/freeze on Blizzard proc:** structurally cold-registered but this kit's own dossier does not name the ailments verbatim (cross-evidenced from ud-ice-crystal-arrow UD cold evidence). Emitted with near-miss note.
- **ud-toxic-flame — fire element:** skill name is "Toxic Flame" implying fire; rune page attests poison DoT only; fire is a name-register word not a damage-type descriptor.
- **ud-summon-strand — fusion trigger:** Melody High Tone Abyssling→Abyss Knight fusion mechanic has no engine trigger analog; delivery_notes capture it, not mapped to trigger_grammar.

## Forced / notable calls

- **ud-lightning-vortex geometry:** corpus geo_raw="large-AOE" (probe heuristic, illegal grounds). Rune page attests melee weapon swing → mapped melee_arc (per errata).
- **ud-toxic-flame geometry:** corpus geo_raw="small-AOE"; rune page attests piercing projectile → mapped line.
- **ud-illusion-family:** verify CONTRADICTED on mechanics; dossier corrected to stack-proc auto-fire (not echo-copy). This is a genuine mechanics reversal from the original canon claim.
- **ud-summon-strand fire element:** "breathes Fire" = minion-level behavioral delivery verb — border call. Filed as attested under §B5-ELEMENT "enemy-directed behavior verb" applied to minion-unit delivery; this is a proxy-entity fire delivery, not player fire delivery. Summoner-deferral makes the grade call GAPPED regardless.

## Accrual filings (steward-owned)

- **Placed-proxy-count family:** no new placed-proxy-count instances in this UD batch (Illusion proc is caster-origin, not placed; Rune Knight is following companion not stationary totem). No accrual filed.
