# VDM-1 basin-4 mapping batch-n02 — summary

**Batch:** n02 · **Kits:** 11 · **Date:** 2026-07-18 · **Author:** gandalf (SPEC-AUTHOR)

---

## Grade histogram

| Grade | Count | Kits |
|---|---|---|
| EXACT | 0 | — |
| CLOSE | 8 | drizzle-aeromancer, energy-overflow-soulfist, esoteric-flurry-striker, esoteric-skill-wardancer, evolutionary-legacy-machinist, ferality-wildsoul, first-intention-wardancer, full-moon-souleater |
| APPROX | 0 | — |
| GAPPED | 3 | desperate-salvation-bard, enhanced-weapon-deadeye, full-bloom-artist |

All 3 GAPPED → MAPPED_DOCKET (strict biconditional honored). No APPROX+MAPPED_DOCKET hybrids.

---

## Per-kit one-liners

- **desperate-salvation-bard** GAPPED/DOCKET — pure support (heal/shield/party-buff); Brand = curse:amplify; no damage loop; support-lane-gapped docket
- **drizzle-aeromancer** CLOSE — raindrop-meter → Sun Shower burst_window; move-slow + attack-debuff attested but not named 16-ailment; values stale (shape only)
- **energy-overflow-soulfist** CLOSE — inner-energy floor (Energy Overflow) + Hype (Z) burst_window; Lightning Palm/Celestial Palm element null (name-only)
- **enhanced-weapon-deadeye** GAPPED/DOCKET — 3-weapon stance rotation irreducible; mode-swap-identity docket; second confirmed instance (n01 Peacemaker = first)
- **esoteric-flurry-striker** CLOSE — esoteric_orbs generate/1-orb-spend sustained cycle; back-attack positioning delivery_notes only; element null throughout
- **esoteric-skill-wardancer** CLOSE — esoteric_orbs + per-orb +6% scalar at cast; Quintuple Resilience Destiny → capstone; Weakness Exposure = raid-break only
- **evolutionary-legacy-machinist** CLOSE — battery_core → Hypersync transformation; Sync/Sync-Zero two-battery approximated; negative=1 (D-tier) mapped attested identity per discipline
- **ferality-wildsoul** CLOSE — Fox/Bear dual-form phantom_beast_energy + ferality_stacks (max 3) → finisher; NOT mode-swap-identity (dominant loop attested across both forms)
- **first-intention-wardancer** CLOSE — esoteric_orbs → Esoteric Origin empower window (burst_window); layered self-buffs; simpler than ESE per-orb scalar
- **full-bloom-artist** GAPPED/DOCKET — support (heal/shield/attack-buff); two curse:amplify attestations (Moonfall + Brand); support-lane-gapped docket
- **full-moon-souleater** CLOSE — soul_stones → possession_meter → Deathlord Mode (Z) burst_window + curse:amplify (Amplified Damage on nearby enemies); two-resource chain native (not two-tier-accumulator docket)

---

## T4-door frequency

| Token | Kits |
|---|---|
| TEMPORAL_CHARGE | drizzle, energy-overflow, evolutionary-legacy, first-intention, full-moon |
| MOMENTUM_CASCADE | esoteric-flurry, esoteric-skill, ferality, first-intention, full-moon |
| ZONE_CONTROL | drizzle, evolutionary-legacy |
| PHASE_MOMENTUM | ferality |
| NETWORK_AMPLIFIER | desperate-salvation (support), full-bloom (support) |

---

## Docket candidates (filed: `docket-candidates-batch-n02.jsonl`)

2 docket entries:
1. **mode-swap-identity** — `la-enhanced-weapon-deadeye` (3-weapon stance; second instance after n01 Peacemaker)
2. **support-lane-gapped** — `la-desperate-salvation-bard` + `la-full-bloom-artist` (mirrors n01 blessed-aura-paladin; steward consolidates at review-book)

No mint-candidates this batch (no quantitative/qualitative mint triggers surfaced).

---

## §0 near-misses (elements/statuses WANTED but could NOT attest)

**Element near-misses (11 total — LA name-only law dominant):**
- esoteric-flurry-striker: Lightning Tiger Strike, Call of the Wind God, Storm Dragon Kick — wanted lightning/wind; all skill-name-only
- esoteric-skill-wardancer: Azure Dragon Supreme Fist, Rising Fire Dragon, Call of the Wind God, Thunderclap Kick — wanted fire/wind/lightning; all name-only
- ferality-wildsoul: Fox Flame — wanted fire; name-only
- evolutionary-legacy-machinist: Crimson Breaker — wanted fire; name-only
- first-intention-wardancer: Lightning Kick, Flash Heat Fang, Leaping Dragon — wanted lightning; name-only
- full-moon-souleater: entire kit — shadow/dark theme throughout, ZERO damage-type descriptor anywhere in store → null
- drizzle-aeromancer: Scorching Sun, Wiping Wind, Rainstorm — wanted fire/wind/water; all name-only
- energy-overflow-soulfist: Lightning Palm, Celestial Palm — wanted lightning; name-only
- enhanced-weapon-deadeye: Judgment Day, Sign of Apocalypse — wanted fire/shadow; name-only

**Ailment near-misses:**
- drizzle-aeromancer: move-speed slow (-20%) and -10% Attack Power debuffs attested in Sun Shower window — WANTED chill + curse:weaken; neither status is NAMED in store → no emission
- esoteric-skill-wardancer: Weakness Exposure (Roar of Courage) — WANTED sunder; it is raid-break vocab (§LA row 4), NOT a 16-ailment
- ferality-wildsoul: Armor Destruction (Vulpine Velocity) — WANTED sunder; raid-break vocab only
- full-moon-souleater: shadow/necrotic theme throughout — WANTED shadow element + drain ailment; zero damage-type descriptors in store

---

## Anything forced

- **drizzle-aeromancer:** Sun Shower debuffs (-20% Move Speed, -10% Attack Power to enemies) are enemy-directed but not named in the 16-ailment registry — forced to delivery_notes; DIRECTION TEST cannot override the §0-UNIVERSAL attestation requirement
- **full-moon-souleater:** Deathlord Mode "Amplified Damage on nearby enemies 10s" — confirmed curse:amplify via DIRECTION TEST (enemies take more); % values omitted per stale-priors pre-ruling
- **full-bloom-artist + desperate-salvation-bard:** Brand / Moonfall both confirmed curse:amplify via DIRECTION LAW — enemy receives more damage (not party-buff misread); n01 canary lesson applied correctly
- **ferality-wildsoul:** Fox/Bear dual-form deliberately NOT filed as mode-swap-identity docket — dominant economy loop (ferality stacks → finisher) is attested across both forms; contrast Enhanced Weapon Deadeye where stance-swap bonus IS the economy with no form-independent loop

---

*Steward audit: ≥25% + full contiguity battery. Histogram advisory per D-2c.*
