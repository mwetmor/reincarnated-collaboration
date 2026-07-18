# VDM-1 Basin-4 Batch-02 Summary — Lost Ark b02 (11 kits)

**Crawl date:** 2026-07-18  
**Primary source:** maxroll.gg/lost-ark (all 11 kits resolved; 0 SNF)  
**Secondary:** playlostark.com (Wildsoul ship-date), mmorpg.com (Wildsoul launch), maxroll.gg tier lists (Aug 2025 + Feb 2025), gamiunity.com (Bard era corroboration)

---

## Per-kit one-liners

| kit_id | verdict summary |
|---|---|
| la-desperate-salvation-bard | CONFIRMED x3 — identity/mechanics/era all attested; Civo/maxroll; Ark Passive era live |
| la-drizzle-aeromancer | CONFIRMED x3 — Sun Shower 35% Weather Damage (not +30% as corpus; minor delta); Raeinor/maxroll |
| la-energy-overflow-soulfist | CONFIRMED x3 — Energy Overflow "never drops to 0" attested; Hype level breakdown confirmed; capstone_alterations abstained (Ark Passive nodes not extracted) |
| la-enhanced-weapon-deadeye | CONFIRMED x3 — 3-stance swap attested; +9% per swap confirmed; Raeinor/maxroll |
| la-esoteric-flurry-striker | CONFIRMED x3 — single-orb spend pattern confirmed; Sekwah/maxroll |
| la-esoteric-skill-wardancer | CONFIRMED x3 — +6%/orb at cast confirmed; Energy Combustion as generator confirmed; Raeinor/maxroll |
| la-evolutionary-legacy-machinist | CONFIRMED x2 (identity, era) + CONTRADICTED x1 (mechanics: corpus says "drone-evolution" — WRONG; identity is Hypersync robot-suit transformation with Sync/Sync Zero skills, no drone mechanic) + CONFIRMED negative_canon (D-tier Aug 2025 tier list, ~3000 community votes) |
| la-ferality-wildsoul | CONFIRMED x3 — Fox/Bear forms + Ferality stacks confirmed; ship date Feb 26 2025 confirmed from official playlostark.com; Raeinor/maxroll |
| la-first-intention-wardancer | CONFIRMED x3 — buff-and-burst loop attested; Esoteric Origin empowerment window confirmed; Raeinor/maxroll |
| la-full-bloom-artist | CONFIRMED x3 — Sunrise 1-orb cost + 25%/15% heal values confirmed; Civo/maxroll |
| la-full-moon-souleater | CONFIRMED x3 — Deathlord Mode cooldown reset on entry confirmed; Footsteps of the Dead 50% CDR confirmed; Sekwah/maxroll |

---

## Verdict histogram (advisory — file truth is count)

| Verdict | Count |
|---|---|
| CONFIRMED | 36 |
| CONTRADICTED | 1 |
| UNSUPPORTED | 0 |
| SOURCE_NOT_FOUND | 0 |

---

## Contradictions (1 total)

**la-evolutionary-legacy-machinist / mechanics:**  
Corpus mech_note states "drone-evolution identity" and "drone evolution builds." Fetched text (maxroll.gg, Sekwah, June 2026) describes a **Hypersync transformation identity** — robot-suit mode with Sync/Sync Zero skill trees, a Sync Zero Battery (1000 units), and human-form energy generators (Command: Baby Drones / Command: Raid Missile). There is NO "drone evolution" mechanic in the Evolutionary Legacy identity per fetched text. The drone confusion likely arises from Arthetinean Skill Machinist (drone-focused) being conflated with Evolutionary Legacy (transformation-focused) during corpus entry. This is an INTERNAL spec confusion in the corpus, not a ship/existence error. Negative=true verdict (D-tier) and identity claim (kit exists) are both CONFIRMED; only the mechanics descriptor is wrong.

---

## SNF kits

None. All 11 kits resolved from maxroll.gg primary source.

---

## Dossier coverage

- 11 kits × 6 families = 66 family slots
- Abstained: 2 slots (la-energy-overflow-soulfist/capstone_alterations — Ark Passive nodes not in extracted content; la-enhanced-weapon-deadeye/variants — no distinct sub-variant identified from fetched text)
- Coverage: 64/66 = **97%**

---

## Author credits

| Author | Kits |
|---|---|
| Civo (maxroll.gg) | la-desperate-salvation-bard, la-energy-overflow-soulfist, la-full-bloom-artist |
| Raeinor (maxroll.gg) | la-drizzle-aeromancer, la-enhanced-weapon-deadeye, la-esoteric-skill-wardancer, la-ferality-wildsoul, la-first-intention-wardancer |
| Sekwah (maxroll.gg) | la-esoteric-flurry-striker, la-evolutionary-legacy-machinist, la-full-moon-souleater |

---

## Element-attestation summary

**D4 name-only law applied strictly.**

- **la-drizzle-aeromancer:** Zero element-as-damage-descriptor attested. The Sun Shower window grants "+35% Damage to Weather Skills" — "Weather Damage" is a skill-category descriptor (damage multiplier to weather-typed skills), not an element word applied as a damage type to an enemy-directed effect. No "lightning damage," "electric damage," "thunder damage," or "weather damage as elemental attack" language found anywhere in the guide. Element-silent per D4 law.
- **la-ferality-wildsoul (Fox/Bear forms):** Zero element descriptors. Fox Form and Bear Form are identity/form mechanics with no elemental damage language in fetched text. Element-silent per identity-form default.
- **la-full-moon-souleater (Deathlord form):** Zero element descriptors. No "dark damage," "shadow damage," or "death energy" language used as damage-type descriptors in fetched text. Element-silent per identity-form default.
- **All other b02 kits:** No elemental damage descriptor language found in any guide. LA is confirmed element-light for this roster.

**Net attested elements in b02: 0.**

---

## Red flags

1. **EL Machinist mechanics mislabel (CONTRADICTED):** Corpus mech_note conflates Evolutionary Legacy (Hypersync transformation) with Arthetinean Skill (drone-focused). Elrond should correct `mech_note` for `la-evolutionary-legacy-machinist`. The D-tier negative_canon verdict is confirmed; only the identity description is wrong.

2. **Drizzle Aeromancer Weather Damage value delta:** Corpus says "+30% Weather Damage passive"; fetched text says "+35% Damage to Weather Skills" (maxroll, June 2026). Minor numerical delta — likely a patch update between corpus entry and guide refresh. Not a contradiction on mechanics structure, but a field value to note for mech_note correction.

3. **Full Moon Souleater mechanics delta:** Corpus claims "+15% Deathlord skill damage; -70% cooldowns." Fetched text confirms cooldown resets on entry and "50% cooldown reduction on Stygian skills during Deathlord mode" (Footsteps of the Dead node). The +15% and -70% figures are not explicitly verbatim-confirmed in fetched text (may require deeper Ark Passive node extraction). Verdict CONFIRMED on structural mechanics; specific %-values UNSUPPORTED pending deeper extraction.

4. **Ferality Wildsoul slug discrepancy:** maxroll slug is `wild-instincts-wildsoul-build-guide`; guide confirms folk_name "Ferality Wildsoul." "Wild Instincts" appears to be either the Ark Passive path name or an alternate build identity label. Aug 2025 tier list lists this spec as "Wild Instincts: S+ Tier." Downstream: folk_name "Ferality" is correct per guide text; slug divergence is a maxroll naming artifact, not a corpus error.
