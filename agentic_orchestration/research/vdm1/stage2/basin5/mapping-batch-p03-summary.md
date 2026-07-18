# Mapping batch p03 summary — chr-a (Chronicon, 8 kits)

**Date:** 2026-07-18 · **Author:** gandalf (SPEC-AUTHOR) · **Source:** batch-c03-verify.jsonl (8 distinct kit_ids confirmed)

## Grade histogram

| Grade | Count | Kits |
|---|---|---|
| EXACT | 2 | chr-bleed-berserker, chr-frost-berserker |
| CLOSE | 2 | chr-fire-berserker, chr-firestorm-warlock |
| APPROX | 1 | chr-bloodbinder-warlock |
| GAPPED | 3 | chr-arrow-storm-warden, chr-bee-warden, chr-demon-legion-warlock |

MAPPED: 5 · MAPPED_DOCKET: 3

## Per-kit one-liners

| kit_id | Grade | One-liner |
|---|---|---|
| chr-arrow-storm-warden | GAPPED | All 6 dossier rows abstained; identity+mechanics UNSUPPORTED — full honest empty-projection |
| chr-bee-warden | GAPPED | All 6 dossier rows abstained; identity+mechanics UNSUPPORTED — full honest empty-projection |
| chr-bleed-berserker | EXACT | Physical bleed melee + Internal Hemorrhage on-kill burst; Rage resource; Bloodsoaked Garb set; maps cleanly |
| chr-bloodbinder-warlock | APPROX | Errata-corrected mana-stack (not HP-sacrifice); poison-trigger companion swarm; companion double-dip scaling engine-gapped |
| chr-demon-legion-warlock | GAPPED | 39-demon pet-core army; summoner-deferral; no shadow damage-type attested in fetched text (probe elem_raw blocked) |
| chr-fire-berserker | CLOSE | Fire melee + Dragonfire explosion chain maps well; Fire Avatar form-swap (GX-02) is mode-swap docket gap |
| chr-firestorm-warlock | CLOSE | Fire spam + soul-reservoir maps; Sun+Moon bidirectional cross-proc (fire↔frost 3x amp) exceeds trigger_grammar depth |
| chr-frost-berserker | EXACT | Freeze-then-shatter setup-payoff maps cleanly; water/freeze CONFIRMED; Rage resource; chill near-miss (no explicit movement-slow) |

## T4-door frequency (this batch)

| T4 token | Count | Kits |
|---|---|---|
| PERSISTENCE_ENGINE_saturation | 2 | chr-bleed-berserker, chr-fire-berserker |
| GEOMETRY_PROPAGATION_cascade | 2 | chr-bleed-berserker, chr-frost-berserker |
| PROXY_ASCENSION | 2 | chr-bloodbinder-warlock, chr-demon-legion-warlock |
| PERSISTENCE_ENGINE_uptime | 1 | chr-bloodbinder-warlock |
| PROXY_SOVEREIGNTY | 1 | chr-demon-legion-warlock |
| GEOMETRY_PROPAGATION_overkill | 1 | chr-fire-berserker |
| RESONANCE_LOOP | 1 | chr-firestorm-warlock |
| TEMPORAL_CHARGE | 2 | chr-firestorm-warlock, chr-frost-berserker |

## Candidates

**Mint candidates:** none this batch.

**Docket candidates:** 3 kits → MAPPED_DOCKET.

- chr-arrow-storm-warden: thin-source UNSUPPORTED (re-crawl candidate)
- chr-bee-warden: thin-source UNSUPPORTED (re-crawl candidate)
- chr-demon-legion-warlock: summoner-deferral (pet-core demon army, 39 companions; no player-damage floor without companion layer)

## §0 near-misses (elements/statuses wanted but could not attest)

| Kit | Wanted | Why not emitted |
|---|---|---|
| chr-bleed-berserker | burn | 'burning ground' in item_alterations describes a zone DoT, not an on-enemy burn status; §0-UNIVERSAL binds |
| chr-bloodbinder-warlock | earth OR shadow (element_primary) | 'poison skill' is a skill-category label, not a damage-type descriptor applied to a generic effect noun; §0.2 name-only discipline |
| chr-demon-legion-warlock | shadow | corpus elem_raw=shadow is probe-heuristic (ILLEGAL grounds); no 'deals shadow damage' in fetched dossier text |
| chr-fire-berserker | burn | burning ground (Smoldering Stone) is a ground zone DoT, not an on-enemy burn status named in fetched text |
| chr-frost-berserker | chill | frost stacks imply movement slow but no explicit '-X% movement speed' text in fetched dossier; §0-UNIVERSAL binds |

## Accrual filings (steward-owned, WITHOUT numbers)

- **Two-tier-accumulator:** chr-bleed-berserker (bleed stacks → Bloodbath stacks → damage amp) · chr-bloodbinder-warlock (mana pool size = scaling substrate) · chr-firestorm-warlock (soul-count → 480% scaling bonus)
- **Placed-proxy-count:** chr-bloodbinder-warlock companion swarm · chr-demon-legion-warlock demon army (39 companions)

## Key rulings applied / traps avoided

1. **bloodbinder errata honored:** CONTRADICTED verdict → mana-stacking identity (not HP-sacrifice); attested from verify_ledger anchor.
2. **demon-legion element silence:** corpus elem_raw=shadow blocked (probe-heuristics ILLEGAL); genuine 'deals shadow damage' not present in 5 non-abstained dossier rows → element null, GAPPED on pet-core grounds.
3. **turret-drone §0.2 corollary (chr-a):** 'Holy Lance Turrets' skill-name trap did NOT appear in this batch — noted as p04 concern.
4. **arrow-storm + bee-warden empty-projection:** BOTH kits fully abstained (6/6 rows each); honest GAPPED with no invented probe-based claims.
5. **fire-berserker physical trap avoided:** fire melee strikes → fire element_primary (fire IS the typed damage); physical = no-family only when physical is the damage — fire overrides here.
6. **firestorm cross-proc element_secondary:** water attested as genuine typed damage element via Sun+Moon cross-proc ('frost damage 3 times') — correctly emitted despite being secondary to dominant fire.
