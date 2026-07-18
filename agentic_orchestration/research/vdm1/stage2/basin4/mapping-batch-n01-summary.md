# VDM-1 basin-4 mapping batch n01 — summary

**Batch:** n01 · **Kits:** 11/11 (roster complete) · **Date:** 2026-07-18 · **Author:** gandalf (mapping-author role)

---

## Grade histogram (advisory — steward audits ≥25%)

| Grade | Count | Kits |
|---|---|---|
| EXACT | 1 | berserkers-technique |
| CLOSE | 8 | arthetinean-skill-machinist, asuras-path-breaker, barrage-enhancement-artillerist, brawl-king-storm-breaker, control-glaivier, death-strike-sharpshooter, deathblow-striker, demonic-impulse-shadowhunter |
| APPROX | 0 | — |
| GAPPED → MAPPED_DOCKET | 2 | blessed-aura-paladin, communication-overflow-summoner |

R-M7 biconditional check: both GAPPEDs are MAPPED_DOCKET; zero APPROX+MAPPED_DOCKET hybrids.

---

## Per-kit one-liners

- **la-arthetinean-skill-machinist** (CLOSE): B-tier DPS, negative-flag CONTRADICTED; Normal+Drone/Joint weave loop, Battery economy, no elemental damage-typing, Hypersync attested but suboptimal — omitting it IS the loop.
- **la-asuras-path-breaker** (CLOSE): Front Attack (DB erratum corrected); Stamina/Shock dual-sub-gauge → Asura Energy → timed Asura Destruction burst_window; Defensive Speculation shield = self_buff; no ailments.
- **la-barrage-enhancement-artillerist** (CLOSE): Generate Barrage Meter → Barrage Mode immobile turret (player-transform-as-turret, totem-approximated) → dump damage → exit no-Exhaustion → repeat; no element.
- **la-berserkers-technique** (EXACT): Fury Meter → timed Burst Mode Z → +30% crit/+20% ATK speed/+36% damage (stale values, shape only) → no Exhaustion on exit; canonical build-spend burst_window; maps cleanly.
- **la-blessed-aura-paladin** (GAPPED → MAPPED_DOCKET): Support-class deferral; Holy Aura party buff/heal has no solo engine loop analog; curse:amplify emitted for Sword of Justice enemy debuff but core party-utility identity is GAPPED.
- **la-brawl-king-storm-breaker** (CLOSE): Non-positional (attested explicit); dual Stamina/Shock perpetual alternation — both gauges always in motion (not standard accumulate-then-release); burst-blows on full Shock consume; novel dual-gauge rhythm.
- **la-communication-overflow-summoner** (GAPPED → MAPPED_DOCKET): Pet-core summoner deferral; Akir-as-buff mechanic UNSUPPORTED per verify_ledger; empty-projection applied; companions-as-damage has no solo engine analog.
- **la-control-glaivier** (CLOSE): Control locks Focus stance out entirely; flat +40% Flurry damage (stale — shape only); Dual Meter used only as buff on three specific skills (not identity release); back-attack positional.
- **la-death-strike-sharpshooter** (CLOSE): Rapid Hawk Meter via Death Strike passive; Silverhawk Assault (Z) deploys hawk debuff (curse:sap for 27% damage-to-boss); 12% damage while hawk absent = second timing state not fully captured.
- **la-deathblow-striker** (CLOSE): Strict 3-orb all-consume gate; Lightning NOT emitted (Lightning Tiger Strike = name only, hot-fact honored); back-attack positional; build-and-detonate identity maps cleanly but multiplicative per-orb scaling lost.
- **la-demonic-impulse-shadowhunter** (CLOSE): Near-permanent demon form (Eternal Blood) = PERMANENT burst per §LA row 2 → self_buff steady-state; Blood/shadow NOT emitted (name-only flavor); Shadowburst Meter accumulate-to-form loop.

---

## T4-door frequency

| T4 token | Count |
|---|---|
| TEMPORAL_CHARGE | 9 |
| MOMENTUM_CASCADE | 4 |
| CLOSE (door) | — |
| ZONE_CONTROL | 1 |
| DEFENSIVE_TRADEOFF | 1 |
| NETWORK_AMPLIFIER | 1 |
| RESONANCE_LOOP | 1 |
| PROXY_ASCENSION | 1 |
| RESOURCE_CONVERSION | 1 |
| PHASE_MOMENTUM | 1 |

TEMPORAL_CHARGE dominant (9/11 kits) — LA gauge-identity kits almost universally accumulate-then-release.

---

## Candidate files

- **mint-candidates-batch-n01.jsonl:** NOT CREATED (zero mint candidates this batch — no novel quantitative/qualitative mint forced; all kits mapped or docketed via existing classes).
- **docket-candidates-batch-n01.jsonl:** 2 entries: `support-class-identity` (blessed-aura-paladin) · `summoner-deferral-pet-core` (communication-overflow-summoner).


---

## §0 near-misses: elements/statuses wanted but not attested

**Elements I wanted to emit but could not (D4 NAME-ONLY LAW blocked all):**
- **lightning** (deathblow-striker): Lightning Tiger Strike is a skill name; hot-fact confirmed — highest-prob lightning at crawl but no in-store damage-typing descriptor. Blocked.
- **shadow / dark** (demonic-impulse-shadowhunter): Blood Demon, Blood Vortex, Shadowhunter class flavor — all name-only. No damage-typing descriptor. Blocked.
- **fire** (barrage-enhancement-artillerist): Flamethrower, Sea of Fire skill/node names — name-only, zero damage-typing. Blocked.
- **fire** (berserkers-technique): no element candidates even surfaced — correctly element-silent.
- **holy** (blessed-aura-paladin): Holy Aura, Heavenly Blessings — all class/skill name flavor. No damage-type descriptor. Blocked.

**Statuses I wanted to emit but could not (attestation law blocked):**
- **stun** (asuras-path-breaker, brawl-king-storm-breaker, deathblow-striker): Stagger/Shock language present throughout — all boss-break vocabulary per §LA row 4, never a 16-ailment emit.
- **sunder** (asuras-path-breaker): "Destruction" in gem names (Destruction Charger, Destruction damage on pet skills) — all name-only, no damage-taken-amplification descriptor on a generic effect noun.
- **freeze / chill** (control-glaivier): no cold language attested at all; null is correct.

---

## Anything forced / notable deviations

- **Barrage Mode as totem**: player-transforms-into-turret is approximated as `totem` — closest geometry but source player would note it is a self-transformation, not a placed proxy. Acceptable delivery texture approximation; CLOSE not APPROX because the burst cycle identity maps.
- **Dual-gauge economy (asuras + brawl-king)**: Stamina/Shock as two named sub-gauges feeding one pool (asuras) or alternating perpetually (brawl-king) is a novel economy shape; resource_economy carries it adequately as named keys but the perpetual-alternation rhythm (brawl-king) differs from accumulate-then-release.
- **Silverhawk "hawk absent" bonus** (death-strike-sharpshooter): the 12% damage while hawk NOT summoned creates a second timing loop the engine doesn't directly express — noted in fidelity_notes, not forced into a separate ailment or trigger.
- **Control Glaivier Dual Meter as buff-on-three-skills**: unlike other gauge kits, the Dual Meter here is a buff applicator on specific skills only, not a release button — expressed in resource_economy but acknowledged as a novel sub-use of the economy lane.
- **Communication Overflow mechanics UNSUPPORTED**: empty-projection applied per §E.2 — skills[], motion_frame, economy all empty/null. Docketed for summoner-deferral review-book.

---

**Signed:** gandalf (mapping-author) · 11/11 roster coverage confirmed · batch committed as `gandalf-seam: VDM-1 basin-4 mapping batch-n01 (11 kits)`

---

## STEWARD AUDIT ADDENDUM (gandalf-as-steward, 2026-07-18) — n01 CANARY, 100% DEPTH

**Verdict: PASS (with 2 in-place corrections).** n01 is the basin-4 canary — audited at **100% depth** (11/11 kits, not the ≥25% floor) because it validates the freshly-authored basin-4 mapping law + MAPPING-BRIEF-TEMPLATE before the n02–n05 scale wave. Recounted from the committed file (advisory NEVER trusted, D-2c).

**Histogram — ZERO DRIFT.** File-truth recount == advisory exactly: EXACT 1 / CLOSE 8 / GAPPED 2; MAPPED 9 / MAPPED_DOCKET 2. R-M7 biconditional HOLDS on all 11 (both GAPPEDs are MAPPED_DOCKET; zero APPROX+MAPPED_DOCKET hybrids). Post-correction re-parse: 11 rows clean, grades unchanged.

**Element discipline — PERFECT (the marquee canary success).** ZERO element emissions across 11 kits; every candidate withheld under the D4 NAME-ONLY LAW. The deathblow-striker Lightning-Tiger-Strike withholding — despite the crawl's "highest-prob lightning" hot-fact staring the mapper in the face — is the textbook proof the law is TEACHABLE on a non-Diablo engine. Economy keys all native (battery / asura_energy / barrage_meter / fury_meter / piety_meter / hawk_meter / esoteric_orbs / shadowburst_meter + dual-gauge stamina/shock). burst_window PERMANENT-vs-TIMED correctly discriminated (berserkers/asuras TIMED → burst_window; demonic-impulse PERMANENT → self_buff steady-state). Boss-break Stagger/Shock/Destruction correctly NOT mapped to stun/sunder (§LA row 4 held).

**TWO corrections — both damage-modification-DIRECTION confusion (the LA-dominant ailment trap), both steward-caught, both corrected in-place, ZERO grade impact:**
- **STRIKE #1 (hard) — death-strike-sharpshooter, Silverhawk Assault:** store "27% Increased Damage to the Boss" (enemy-directed damage-taken amplification) mapped `curse:sap` → **corrected to `curse:amplify`**. Grounds: b01 Despair precedent (crosswalk §2 line 52/53) — damage-taken amp ≠ defense shred. sap is defense/resist/armor SHRED only. JSONL edits A (ailment token) + B (fidelity_notes rationale) applied.
- **STRIKE #2 (soft) — blessed-aura-paladin, Holy Aura:** store "+10% damage dealt to enemies [by party]" (an ally/party BUFF) mis-emitted `curse:amplify` → **corrected to `[]`**. Grounds: solo projection — party = player, so a party-damage buff is a self_buff, NOT an enemy curse. JSONL edit C applied. The same kit's Sword-of-Justice row ("target to receive +10% Damage from party" = enemy-directed) correctly KEPT curse:amplify — one kit carrying BOTH directions is the textbook teaching case.

**Inoculation applied BEFORE scale wave:** the §LA DEBUFF-DIRECTION LAW pre-existed (addendum §LA row 5) but was buried and did not fire salient. Hardened into a dedicated `### §LA DEBUFF-DIRECTION LAW` block (3-way direction test + b01 precedent + n01 evidence) AND named as an explicit hot-fact in the n02–n05 re-fire prompts. **Canary purpose FULFILLED** — one systematic gap surfaced + closed before scale.

**Contiguity battery — CLEAN on load-bearing quotes.** blessed-aura "sword_of_justice_effect" ("…target to receive +10% Damage from party"), death-strike "27% Increased Damage to the Boss", arthetinean "Machinist: B Tier" (CONTRADICTED-negative), communication-overflow UNSUPPORTED-with-no-anchor (correct empty-projection) — all verified contiguous in-store. One minor paraphrase-in-quotes noted (death-strike "maintaining damage debuff on target" — non-fabricated, flavor paraphrase, noted only, no strike).

**Signed:** gandalf (steward) · n01 canary PASS · 100% depth · 2 corrections in-place · addendum hardened · scale wave (n02–n05) authorized + fired.
