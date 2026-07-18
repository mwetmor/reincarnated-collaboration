# VDM-1 basin-4 mapping batch n05 summary — 10 kits (FINAL wave)

**Date:** 2026-07-18 · **Author:** gandalf (SPEC-AUTHOR) · **Wave:** n05 (final — closes basin-4)

---

## Grade histogram

| Grade | Count | Kits |
|---|---|---|
| EXACT | 1 | la-surge-deathblade |
| CLOSE | 9 | all remaining |
| APPROX | 0 | — |
| GAPPED | 0 | — |

**Terminal states:** 10 MAPPED · 0 MAPPED_DOCKET

---

## Per-kit one-liners

| Kit | Grade | One-liner |
|---|---|---|
| la-recurrence-artist | CLOSE | DPS Artist; negative canon (D-tier); Rising Sun/Waning Moon 60s crit buff loop; element null; no ailments; no named individual skill geometries in store |
| la-reflux-sorceress | CLOSE | Element-STRIKE exemplar: Blaze/Rime Arrow/Inferno/Doomsday all name-only null; Arcane Rupture disabled; Blink becomes Magick Charge self_buff; cooldown-spam identity; two Ark Passive sub-variants collapsed to same shape |
| la-remaining-energy-deathblade | CLOSE | Death Trance (Z) → 30s burst_window (timed); death_orbs gates entry; consistent uptime cycling; Art Master/Levin Slash Ark Passive riders; element null throughout |
| la-robust-spirit-soulfist | CLOSE | Robust Spirit instant Hype 3 burst_window (20s, 100% damage); Conviction/Judgment pairing in fidelity_notes; Lightning Palm name-only null; non-positional confirmed |
| la-shining-knight-valkyrie | CLOSE | Light Meter 15-cast fill → Z Synergy (curse:amplify per DIRECTION LAW) + 3x Holy Blade self-charge; Final Splendor X single-hit; non-positional (tripods); 2025-era class |
| la-shock-training-scrapper | CLOSE | Shock gauge builder/spender; Shock = class category NOT ailment; Tenacity Release Z burst_window; 5/10/20% Shock Energy refund on consumption; element null |
| la-surge-deathblade | EXACT | Death Trance + surge_stacks + death_orbs dual economy; 60-stack Limit Break double-damage burst_window; orb refund → instant repeat; Surprise Attack Synergy → curse:amplify |
| la-taijutsu-scrapper | CLOSE | Tenacity Release Z as self_buff (sustained uptime) vs Shock Training burst_window — key spec distinction; unlimited Shock/Stamina during Z; +20% Stagger = boss-break NOT stun; Synergy → curse:amplify |
| la-time-to-hunt-gunslinger | CLOSE | Two-stance (Handgun CDR + Rifle DPS), no docket (dominant loop exists, contrast Peacemaker n04); Quick Scope 20-stack Rose Blossom threshold; element null |
| la-wind-fury-aeromancer | CLOSE | Element-DISCIPLINE exemplar: zero wind damage-type descriptors despite 6+ wind-named skills/nodes; Sun Shower Z: party speed self_buff + enemy slow chill; Raindrop Meter economy; 8s burst window |

---

## T4-door frequency

| T4 token | Count | Kits |
|---|---|---|
| TEMPORAL_CHARGE | 8 | all except shining-knight, wind-fury |
| MOMENTUM_CASCADE | 6 | recurrence, remaining-energy, surge, taijutsu, time-to-hunt, wind-fury (alt) |
| RESOURCE_CONVERSION | 2 | robust-spirit, shock-training |
| NETWORK_AMPLIFIER | 2 | shining-knight, wind-fury |
| ZONE_CONTROL | 1 | wind-fury |

---

## Candidates

**mint-candidates-batch-n05.jsonl:** none — no novel mechanism requiring mint.

**docket-candidates-batch-n05.jsonl:** none — no irreducible stance rotation or pet-core kits in this batch. (Time to Hunt = 2-stance with dominant loop → no mode-swap-identity docket needed; contrast Peacemaker n04.)

---

## §0 near-misses (elements/statuses WANTED but could not attest)

### Element near-misses (many — LA is name-heavy)

- **la-reflux-sorceress:** Blaze (fire-named), Rime Arrow (cold-named), Inferno (fire-named), Doomsday — all in gems_damage list only. Zero damage-type descriptors in store. All null per D4 NAME-ONLY LAW. This is the **element-STRIKE exemplar** for the basin (per hot-facts).
- **la-wind-fury-aeromancer:** Thunderwind (wind+lightning composite name), Tornado Dance, Piercing Wind, Wind Gimlet, Gale Slash (Ark node), Whirlpool — six wind-register names in store with ZERO damage-type descriptor. Aeromancer is wind-themed class; element-POTENTIAL is not attested damage. All null. This is the **element-DISCIPLINE exemplar** for the basin (per hot-facts).
- **la-recurrence-artist:** Rising Sun / Waning Moon — light/sun-themed names. No element damage-type descriptor. Null.
- **la-shining-knight-valkyrie:** Holy Blade, Sword of Revelation, Judgment Stigmata — holy-themed skill names. No holy damage-type descriptor in store. Null. (Contrast: LA igniter n03 = GENUINE fire keep because "+18% elemental skill damage, fire attribute on skills" is a damage-type descriptor.)
- **la-shock-training-scrapper:** Fist of the Wind God, Death Rattle — name-only. Null.
- **la-taijutsu-scrapper:** Explosive Fist, Iron Cannon Blow — name-only. Null.
- **la-remaining-energy-deathblade:** Deathblade Surge — proper skill name, null.
- **la-surge-deathblade:** Blade Dance, Blitz Rush, Wind Cut, Maelstrom — all name-only. Null.

### Status near-misses

- **la-shock-training-scrapper / la-taijutsu-scrapper:** "Shock" appears 10+ times in store text as the Scrapper class skill-category and gauge name. TRAP: could naively map to shock (paralysis). Do NOT — per hot-facts and §LA row 4 (boss-break vocab). No shock ailment emitted.
- **la-taijutsu-scrapper:** "+20% Stagger" in identity bonuses — boss-break Stagger vocab, NOT stun ailment. Correctly not emitted.
- **la-shining-knight-valkyrie:** "Synergy" debuff — could be misread as a named status on the 16-ailment registry. Correctly mapped to curse:amplify per DIRECTION LAW (enemy-directed damage-received debuff).
- **la-wind-fury-aeromancer:** party +12% Attack/Move Speed from Sun Shower — could be misread as curse on enemy. DIRECTION LAW: ally deals more (not enemy takes more) → self_buff, no ailment. Only the enemy -20% Move Speed maps to chill.

---

## Anything forced / notable

- **surge-deathblade EXACT:** The pre-ruling hot-fact precisely described the dual economy (death_orbs gates Z; surge_stacks inside Z gates burst) and the orb-refund repeat cycle. Cleanest EXACT in this batch.
- **taijutsu vs shock-training distinction:** Both Scrappers use Tenacity Release (Z). The key mapping distinction is consequence_type: Taijutsu Z = self_buff (sustained unlimited-resource identity); Shock Training Z = burst_window (discrete spend period). This distinction was author-judged from the dominant-loop criterion.
- **DIRECTION LAW fires on 3 kits:** Synergy → curse:amplify confirmed on shining-knight (Z identity), surge-deathblade (Surprise Attack), taijutsu-scrapper (Judgment), wind-fury-aeromancer (Tornado). Basin-wide pattern: LA Synergy = standard enemy damage-received debuff → always curse:amplify.
- **wind-fury Sun Shower enemy slow → chill:** The only new ailment attestation in this batch beyond curse:amplify. Enemy movement debuff (-20% Move Speed) maps to chill per §2 crosswalk. Party speed side → self_buff per DIRECTION LAW.
- **time-to-hunt: no mode-swap-identity docket.** Two stances with a clear dominant loop (Rifle for damage; Handgun for CDR) → maps cleanly. Contrast Peacemaker (n04) which has 3 stances with no dominant mode.
- **recurrence-artist negative canon:** neg=1 (D-tier Aug 2025). Correctly mapped as attested DPS identity, not as support (which would be Full Bloom).

---

*Basin-4 closed. n05 = final wave. 10 kits. 1 EXACT, 9 CLOSE, 0 GAPPED, 0 APPROX.*
