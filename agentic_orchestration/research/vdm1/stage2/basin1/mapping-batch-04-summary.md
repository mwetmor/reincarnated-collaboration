# VDM-1 basin-1 mapping batch-04 — summary (12 kits, spec lines 37-48)

**Author:** gandalf (SPEC-AUTHOR, VDM-1 mapping-seam) · **Date:** 2026-07-18 · **Provenance:** authored-vdm1
**Games:** poe2 ×2 · hades2 ×5 (§D governs) · tq2 ×5 (§E governs) · all dossiers ingested (ingest-8/9).

## Grade histogram
| Grade | Count | Kits |
|---|---|---|
| EXACT | 0 | — |
| CLOSE | 9 | poe2-whirling-assault-ma · poe2-witchhunter-grenades · hades2-glorious-disaster · hades2-hail-storm · hades2-hephaestus-blast · hades2-omega-magick · tq2-elementalist · tq2-forge-turrets · tq2-whirlwind-rogue |
| APPROX | 3 | hades2-medea-skull-cast · tq2-bastion-tank · tq2-stormblade-ice-shards |
| GAPPED | 0 | — |

Terminal: 9 MAPPED · 3 MAPPED_DOCKET (the 3 APPROX; R-M7 1:1 holds). No EXACT — post-cutoff kits carry enough game-relative texture (clone-multiplicity, duo-boon coupling, mobile-channel uniqueness, dual-mastery, armor/reservation couplings) that nothing was a lossless fit; grade honesty over optimism.

## Per-kit one-liners
- **poe2-whirling-assault-ma** [CLOSE] — whirlwind spin cast by Hollow Form CLONES; Power Charge accumulator + Lochtonial charge-refund self-loop; clone-multiplicity softened to linked-cast. GX-11/GX-17.
- **poe2-witchhunter-grenades** [CLOSE] — ground_targeted_circle kill-zone (Explosive+Oil+Flash, chain_count=3); ammo-stock + Heat economy; ignite→burn, shock NOT emitted; fuse-timing native (R-M5 N/A). GX-03.
- **hades2-glorious-disaster** [CLOSE] — Zeus+Apollo DUO capstone; Omega Cast placed lightning zone + Magick channel (focus tick-cost); ELEMENTAL_ECHO/GEOMETRY_COLLAPSE. GX-19.
- **hades2-hail-storm** [CLOSE] — Zeus+Demeter DUO; freeze→lightning NATIVE on-ailment-application trigger (NOT R-M9); water+lightning cross-element; control=core. GX-15.
- **hades2-hephaestus-blast** [CLOSE] — weapon-independent periodic fire blast; ground_slam + cooldown-gated on-hit burst; GEOMETRY_PROPAGATION_overkill; single-god (no duo). GX-03.
- **hades2-medea-skull-cast** [APPROX→DOCKET] — throw-explode shells + lunge-RETRIEVE (2nd action); multi_projectile + out-and-return accrual; Static Shock→sunder; element-neutral. GX-14.
- **hades2-omega-magick** [CLOSE] — Omega Cast self-origin delayed nova (circle+delay); STATIONARY charge (ingest-9 corrected); Magick=focus meter charge-release; grammar record. GX-05.
- **tq2-bastion-tank** [APPROX→DOCKET] — Warfare+Forge; armor-AS-damage (Shield Attack/Armor Eruption own docket, FLAG 11); ground_slam+melee_strike; DEFENSIVE_TRADEOFF/RETRIBUTION_ENGINE.
- **tq2-elementalist** [CLOSE] — VERIFIED Storm+Earth (ERRATA-22); Roiling Magma fire + Call Lightning; Amplify/Overload accumulator; both capstones→t4. 
- **tq2-forge-turrets** [CLOSE] — totem placed autonomous fire proxies; 8-trap count accrual to placed-proxy-count family; PROXY_ASCENSION/SOVEREIGNTY. GX-19.
- **tq2-stormblade-ice-shards** [APPROX→DOCKET] — VERIFIED Rogue+Storm (ERRATA-23); 9-shard homing volley (R-M8 pursuit note); reserved-energy-AS-damage-scaler docketed (FLAG 10). GX-17.
- **tq2-whirlwind-rogue** [CLOSE] — VERIFIED WARFARE (not Rogue, identity ERRATA); whirlwind mobile-channel (poe1-cyclone precedent); Rage accumulator; both capstones→t4.

## T4-door frequency
ELEMENTAL_ECHO ×5 · ZONE_CONTROL ×4 · GEOMETRY_COLLAPSE ×4 · MOMENTUM_CASCADE ×2 · RESOURCE_CONVERSION ×2 · TEMPORAL_CHARGE ×1 · GEOMETRY_PROPAGATION_cascade ×1 · GEOMETRY_PROPAGATION_overkill ×1 · DEFENSIVE_TRADEOFF ×1 · RETRIBUTION_ENGINE ×1 · PROXY_ASCENSION ×1 · PROXY_SOVEREIGNTY ×1.
(All tokens verified against `t4_catalog_v2.py` + `layer2_dimensions.py`; all geometries against `geometry_derivation.py` VALID_GEOMETRY_TYPES.)

## Candidates filed (steward-owned; NO numbers per FLAG 14)
**docket-candidates-batch-04.jsonl (3):**
1. armor-conversion damage (defensive-stat AS damage-source) — tq2-bastion-tank — OWN candidate, NOT merged w/ docket #4 stun-as-damage (FLAG 11 + §E).
2. reserved-resource AS damage-scaler (reservation→damage coupling) — tq2-stormblade-ice-shards — §E watch-item FIRED (FLAG 10).
3. throw-retrieve finite-payload reload (spent-ammo you must collect) — hades2-medea-skull-cast — the retrieval-reload rhythm has no ammo lane.

**mint-candidates-batch-04.jsonl (2):**
1. out-and-return (spectral-throw) w/ retrieve-as-second-action — hades2-medea-skull-cast — accrual to EXISTING out-and-return qualitative mint class (§D throw-retrieve row).
2. placed-proxy COUNT (8-trap concurrent cap) — tq2-forge-turrets — accrual to EXISTING placed-proxy-count quantitative mint class (§E + FLAG 9).

## Flags fired
- **GX flags (corpus-carried, noted in fidelity_notes, not numbered):** GX-11/GX-17 (whirling-assault) · GX-03 (witchhunter, hephaestus) · GX-19 (glorious-disaster, forge-turrets) · GX-15 (hail-storm) · GX-14 (medea) · GX-05 (omega-magick) · GX-17 (stormblade). No GX-02 form-swap in this batch.
- **§E reservation-as-damage watch-item:** FIRED (tq2-stormblade-ice-shards) → docket-candidate.
- **HOT-FLAG confirmations against DB:** (1) hades2 Magick mapped as focus-meter cast-cost, NOT reservation/spirit-guide (glorious-disaster, omega-magick). (3) omega-magick STATIONARY charge — verify_ledger mechanics-sprint CONTRADICTED (anchor 'she must remain stationary'); `_prior_ingest9` sprint claim NOT mapped. (4) hail-storm freeze→lightning = native on-ailment-application, NO R-M9. (5) medea retrieve = 2nd action, out-and-return accrual WITHOUT number. (7) Static Shock armor removal (medea) → sunder. (8) tq2 dual-mastery ERRATA pairs mapped from verified rows (whirlwind→Warfare, elementalist→Storm+Earth, stormblade→Rogue+Storm; bastion→Warfare+Forge CONFIRMED). (12) tq2-whirlwind queried kit_mapping → poe1-cyclone (whirlwind, mobile-channel native) mirrored.
- **§A discipline:** shock emitted ONLY where probe-attested as lightning-status rider (glorious-disaster, hail-storm, elementalist); NOT emitted on witchhunter (no attestation). ignite→burn throughout. `slow` (tq2 riders) → would be chill per §2 but NOT emitted absent positive attestation on mapped builds; noted only (forge-turrets, elementalist, stormblade). taunt (bastion probe) has no ailment slot (fear-exclusive) → noted not emitted.

## What felt forced (honest flags for steward audit)
- **medea-skull element-neutral + throw-retrieve** — the hardest kit: n/a element ('chaos/skull'), a throw-explode-retrieve loop with TWO gaps (out-and-return geometry + go-collect-ammo economy), Static Shock sunder, AND arcana-gated 'two curse types' (Origination) that is NOT engine curse-ailments (Hades arcana mechanic — noted, not mapped as curse:<variant>). Everything about this kit resisted a clean lane; MAPPED_DOCKET is honest.
- **bastion armor-as-damage** — armor OVERWRITING the damage source is a genuinely novel stat-substrate the engine has no lane for; the tank is playable but the whole POINT (stack armor to hit harder) is docketed.
- **stormblade reserved-energy coupling** — reservation_percent set as the nearest surface is a stretch (engine reservation pays for auras, doesn't scale damage); flagged in-row + docketed rather than pretend a lane exists.

---

## STEWARD AUDIT ADDENDUM (gandalf, DRIFT-CRITIC — 2026-07-18)

**Verdict: ACCEPTED w/ corrections (applied in-place).** Recount matched the return exactly (0E/9C/3A/0G). Enum sweeps: geometry all §6-valid; T4 tokens valid incl. Layer-2 variants; no `ignite`; no `"n/a"` literals; R-M5 sanctioned phrasing only.

**Correction class 1 — §0 ailment leak (12 tokens stripped, 2 attested adds).** The batch emitted 14 ailment tokens; per-kit fetched-text sweep found only 5 grounded. Stripped: glorious-disaster shock+stun · hail-storm shock · hephaestus burn · witchhunter burn+blind · bastion stun×2 · elementalist burn+shock · stormblade freeze · whirlwind knockback. Added (attested): witchhunter Oil `sunder` ("fire exposure" → main-law hit-proc exposure row) · bastion Armor Eruption `sunder` ("Vulnerable on Hit" node). Upheld: witchhunter stun · hail-storm freeze · medea sunder ("Static Shock for Armor removal" verbatim). **Leak provenance: dominantly kb-derived — the mapper cited `canon_probe_facts` as attestation** (its own notes say "probe: blind attested", "burn rider (probe)"); probe facts are pre-verification kb data. Remainder: element-flavor priors (incl. one double inference fire→ignite→burn). **Root-cause split recorded honestly: the steward's own m04 briefing scoped the §0 flag "for the poe2 kits" — the mapper followed the brief literally.** Law fix: §0-UNIVERSAL added to the addendum header (run-wide; probe-facts-never-attestation made explicit); §D Daze→curse:weaken row + §E Vulnerable-on-Hit→sunder row added from this batch's attested language.

**Correction class 2 — R-M7 biconditional (3 terminal flips).** medea · bastion · stormblade were APPROX/MAPPED_DOCKET — MAPPED_DOCKET is reserved for GAPPED (1:1). All three are §D/§E-prescribed approximate+note+candidate kits; docket-candidates ride the side-files (m02 grim-feast precedent). Flipped → MAPPED. Post-edit invariant: 0 GAPPED = 0 MAPPED_DOCKET.

**Upheld:** Magick = cast-cost mana-register (no reservation/spirit_guide surface) · omega-magick STATIONARY per ingest-9 correction · hail-storm native on-ailment-apply trigger grammar (R-M9 correctly absent) · tq2 mastery pairs mapped from ERRATA-21/22/23 verified rows, not corpus class columns · whirlwind mirrors poe1-cyclone `whirlwind` token · forge-turrets `totem` + placed-proxy accrual number-free · medea out-and-return accrual number-free · 3 docket-candidates well-formed (bastion armor-as-damage kept DISTINCT from docket #4 as instructed) · witchhunter fuse = skill-native timing, R-M5 sanctioned phrasing. **Note:** `GX-03` corpus-flag echoes appear in 2 kits' fidelity_notes (steward accrues; register vocabulary check at basin close-out).

**Post-correction file truth: 0E / 9C / 3A / 0G · 12 MAPPED · ailments {stun, sunder×3, freeze} all attested.**
