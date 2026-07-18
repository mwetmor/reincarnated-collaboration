# VDM-1 basin-3 mapping batch-06 summary

**Batch:** m06 · **Kits:** 12 · **Author:** gandalf (SPEC-AUTHOR) · **Date:** 2026-07-18

## Grade histogram

| Grade | Count | Kit IDs |
|---|---|---|
| EXACT | 0 | — |
| CLOSE | 7 | d3-akkhan-condemn, d3-aov-foth, d3-arachyr-firebats, d3-dashing-strike-monk, d3-dmo-twister, d3-firebird, d3-god-hungering |
| APPROX | 3 | d3-firebomb, d3-frenzy-h90, d3-ik-hota |
| GAPPED | 2 | d3-call-of-the-ancients, d3-helltooth-garg |

## Per-kit one-liners

| Kit | Grade | One-liner |
|---|---|---|
| d3-akkhan-condemn | CLOSE | Self-origin nova crusader; Phalanx trigger-avatar rider; holy element unatttested; no ailment. |
| d3-aov-foth | CLOSE | At-target FotH bolt + Heaven's Fury beam; holy/lightning element unatttested in dossier. |
| d3-arachyr-firebats | CLOSE | Rooted channel cone (§B.5); fire element unatttested (skill-name collision); no ailment attested. |
| d3-call-of-the-ancients | GAPPED | Army GAP (three autonomous warrior NPCs); placed-proxy-count accrual filed. |
| d3-dashing-strike-monk | CLOSE | Dash_attack + Fists of Thunder trigger window; cold element unatttested (extraction artifact only); obsolete post-2.4. |
| d3-dmo-twister | CLOSE | R-M6 drift-tick twisters + Slow Time placed_lane; element null; Ranslor's pixelpull vortex rider. |
| d3-firebird | CLOSE | Beam_channel Disintegrate + mark-execute trigger pair; fire element unatttested; burn ailment near-miss (Ignite = set-specific mark). |
| d3-firebomb | APPROX | Negative confirmed; ERRATA-46 lob-framing governs; fire attested ("as Fire"); map covers skill, not a build. |
| d3-frenzy-h90 | APPROX | Melee_strike ramp-stack; CotA-permanent = pet-rider gap; ERRATA-51 Sprint added. |
| d3-god-hungering | CLOSE | Moving-channel Strafe + seeking-line Hungering Arrow; ERRATA-52 GoD alias fixed; element null. |
| d3-helltooth-garg | GAPPED | Army GAP (three Gargantuans); garg-split placed-proxy-count accrual; gear-stat-as-minion-scaling accrual. |
| d3-ik-hota | APPROX | Ground_slam HotA + CotA permanent pet-rider; Fury-Crit scaling attested; ERA watch D-2a pending. |

## T4-door frequency

| T4 token | Count | Kits |
|---|---|---|
| ZONE_CONTROL | 5 | akkhan-condemn, aov-foth, dmo-twister, firebird, ik-hota |
| TEMPORAL_CHARGE | 4 | akkhan-condemn, dashing-strike-monk, frenzy-h90, ik-hota |
| PERSISTENCE_ENGINE_uptime | 3 | arachyr-firebats, dmo-twister, firebird |
| PHASE_MOMENTUM | 2 | dashing-strike-monk, god-hungering |
| MOMENTUM_CASCADE | 2 | frenzy-h90, god-hungering |
| PROXY_ASCENSION | 0 | (filed in docket; no GAPPED kit gets doors) |


## Candidates

**Mint candidates:** 0 (none — no new engine rows required; all gaps filed to standing dockets)

**Docket candidates:** 3 (in `docket-candidates-batch-06.jsonl`)
1. Army GAP: Call of the Ancients (d3-call-of-the-ancients / d3-ik-hota / d3-frenzy-h90) → summoner-deferral + placed-proxy-count accrual
2. Army GAP: Helltooth Gargantuan ×3 (d3-helltooth-garg) → summoner-deferral + placed-proxy-count accrual (garg-split) + gear-stat-as-minion-scaling accrual
3. Negative-confirmed kit: Firebomb → review-book meta-game register

## §0 near-misses (statuses WANTED but could not attest)

| Status wanted | Kit | Why blocked |
|---|---|---|
| holy (element) | d3-akkhan-condemn, d3-aov-foth | Crusader/FotH thematic; mech_note probe-class only; no dossier anchor_quote names "holy" |
| fire (element) | d3-arachyr-firebats | "Firebats" skill-name collision (§0.3 leak class); no fetched anchor text names "fire damage" |
| burn (ailment) | d3-firebird | Firebird "Ignite" = set-specific mark mechanic, not the burn ailment status; no "burning" enemy status in anchor text |
| cold (element) | d3-dashing-strike-monk | "DS Cold" appears only in variants.payload_json extraction artifact, not anchor_quote verbatim |
| fear (ailment) | d3-arachyr-firebats | Horrify text in mech_note (probe-class); no "fear" in fetched dossier anchor text |
| arcane→shadow (element) | d3-dmo-twister, d3-firebird | Arcane→shadow default requires "arcane" attested in dossier; unatttested in anchor_quotes |
| chill (ailment) | d3-dmo-twister | "Slow Time" = skill-name collision (§0.3 leak class); no "chill" or "slow" status in anchor text |

## Family accruals (steward-owned, no numbers)

- **placed-proxy-count family**: d3-call-of-the-ancients (three named warriors), d3-helltooth-garg (garg-split ×3 via Short Man's Finger), d3-frenzy-h90 (permanent CotA rider), d3-ik-hota (permanent CotA rider)
- **gear-stat-as-minion-scaling family**: d3-helltooth-garg (Mask of Jeram pet damage + Tasker and Theo pet attack speed — both are scaler-on-pet-stat pattern, first d3 Witch Doctor attestation)

## Forced decisions / binding hot-facts applied

- §B.1 set-multiplier = scaler-only: applied to all 10 non-GAPPED kits (15000%, 17500%, 12500%, 20000%, etc.)
- §B.4 akkhan Phalanx = trigger-avatars: d3-akkhan-condemn trigger_grammar rider
- §B.2 CoE = R-M5 token: d3-arachyr-firebats, d3-dmo-twister, d3-firebird, d3-ik-hota
- §B.5 arachyr firebats = rooted channel cone: d3-arachyr-firebats delivery_notes
- §CROSS.2 army GAP + garg-split = placed-proxy-count: d3-call-of-the-ancients (GAPPED), d3-helltooth-garg (GAPPED)
- ERRATA-46 firebomb lob-framing: d3-firebomb geometry = single_target (lob), not ground_targeted
- ERRATA-51 frenzy-h90 core_skills Sprint: added to d3-frenzy-h90 skills[] row
- ERRATA-52 god-hungering GoD alias: Gears of Dreadlands confirmed, Grace of Inarius alias removed per DB state
- ERRATA-54 NULL-era backfill: d3-call-of-the-ancients, d3-dashing-strike-monk (eras field; no mapping impact)
- MW1-close amendment (GAPPED/doorless): d3-call-of-the-ancients and d3-helltooth-garg emit t4_doors null
