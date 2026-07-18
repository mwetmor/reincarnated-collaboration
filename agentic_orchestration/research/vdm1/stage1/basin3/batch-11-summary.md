# VDM-1 basin-3 batch-11 summary — kits 121–132 (d4 all)

**Date:** 2026-07-18  
**Batch:** b11 (L121–L132)  
**Game:** d4 (all 12 kits)  
**Negative kits:** 0 — no negative_canon rows emitted, per law.

---

## Advisory verdict histogram (STEWARD RECOUNTS FROM FILES — this is advisory)

| Verdict | Count (advisory) |
|---|---|
| CONFIRMED | 34 |
| UNSUPPORTED | 4 |
| CONTRADICTED | 0 |
| SOURCE_NOT_FOUND | 0 |

**0 contradictions.** Per law: stated loudly. This is a pre-cutoff-stable + post-cutoff mix; the era-U walls on `launch-s1-3` and `loot-reborn-s4-5` tokens account for most U rows — guides have rolled forward and specific season timestamps are absent from current-season pages. Not a reliability failure.

---

## Per-kit one-liners

- **d4-cataclysm** — Identity+mechanics CONFIRMED (Cataclysm Druid, Spirit resource). `loot-reborn-s4-5` era U (no S4/S5 timestamp in fetched guides; archived as Legacy at S13). `voh-s6+` era CONFIRMED (Mobalytics attests active S6+ meta).
- **d4-chain-lightning** — Identity+mechanics CONFIRMED (Chain Lightning Sorc, Mana, chain-hop bounce). `launch-s1-3` era U (icy-veins changelog only shows S8–S12; no launch attestation recovered). `s7-s12` era CONFIRMED (icy-veins S12 guide live).
- **d4-dance-of-knives** — Identity+mechanics CONFIRMED (Rogue channel-while-moving, Energy). `s7-s12` era CONFIRMED (Maxroll S14 guide confirms persistence; DoK is a skill introduced pre-S7 and current in S14).
- **d4-death-trap** — Identity+mechanics CONFIRMED (Death Trap + Concealment reset via set bonus, Energy). `voh-s6+` CONFIRMED (icy-veins changelog shows S6 Oct 2024 + S7 Jan 2025). `s7-s12` CONFIRMED.
- **d4-dread-claws-warlock** — Identity+mechanics CONFIRMED (Dread Claws AoE + Shadowform stack mechanic, Wrath resource). `loh-s13-14` era CONFIRMED (class debuted LoH S13; guide live S14). Stale-prior warning applied; all evidence from fetched text only.
- **d4-earthquake-barb** — Identity+mechanics CONFIRMED (Leap + Ground Stomp + Fury; overlapping Earthquake zones). `loot-reborn-s4-5` era U (earliest guide timestamp found is S7; no S4/S5 stamp recovered). `voh-s6+` CONFIRMED (S7 Season of Witchcraft Maxroll guide attests).
- **d4-evade-sb** — Identity+mechanics CONFIRMED (Evade + Rushing Claw + Vigor; Eagle Main Hall Storm Feathers). `voh-s6+` era CONFIRMED (PrimaGames Season 6 Vessel of Hatred article attests launch meta; Spiritborn confirmed VoH debut).
- **d4-flame-shield-immortal** — Identity+mechanics CONFIRMED (permanent immunity via cooldown-collapsed Flame Shield + Teleport, Mana). `launch-s1-3` era CONFIRMED (Mobalytics build listing "T100 Immortal...S4 & Eternal (Permanent Flameshield)" establishes S4 Eternal realm presence; launch community attestation via wiki skill page).
- **d4-frozen-orb** — Identity+mechanics CONFIRMED (Frozen Orb Sorc, Mana, radial bolt shatter). `loot-reborn-s4-5` era U (no S4/S5 stamp recovered from current guides). `voh-s6+` CONFIRMED (Maxroll S14 guide active).
- **d4-hammerdin-paladin** — Identity+mechanics CONFIRMED (Blessed Hammer Paladin aka "Hammerdin", spiraling hammers follow character). `loh-s13-14` era CONFIRMED (Paladin debuted LoH S13; guide live S14). Stale-prior warning applied; all evidence from fetched text only.
- **d4-heartseeker** — Identity+mechanics CONFIRMED (seeking arrow basic skill, Energy). `loot-reborn-s4-5` era CONFIRMED (WowCarry: "Heartseeker Rogue set the individual tier 133 benchmark for Season 4").
- **d4-hota** — Identity+mechanics CONFIRMED (HotA + War Cry, Fury, Overpower/Berserk). All four era tokens CONFIRMED: `launch-s1-3` (Dexerto launch-era bug-fix journalism, July 2023), `loot-reborn-s4-5` (icy-veins S5 Berserk HotA guide), `voh-s6+` (Maxroll S13 Reckoning guide), `loh-s13-14` (same; Fire Ancients generatorless variant).

---

## UNSUPPORTED era rows (U wall explanation)

1. **d4-cataclysm `loot-reborn-s4-5`** — Icy-veins legacy note says archived at S13 (implying active before), but no S4/S5 timestamp attested in fetched pages. Guide-title silence, not contradiction.
2. **d4-chain-lightning `launch-s1-3`** — Icy-veins changelog starts at S8. No launch-era guide archived; Chain Lightning present at launch is plausible but not fetched-text attested.
3. **d4-earthquake-barb `loot-reborn-s4-5`** — Earliest located guide is S7 (Maxroll Season of Witchcraft). S4/S5 records not recovered.
4. **d4-frozen-orb `loot-reborn-s4-5`** — Mobalytics title "T100 Immortal Frozen Orb S4" corroborates build existed S4, but that's the Flame Shield build's citation URL, not a Frozen Orb-dedicated S4 guide. Source insufficient for a clean CONFIRMED; logged U.

---

## SOURCE_NOT_FOUND kits

None. All 12 kits recovered from primary domain order.

---

## Probe-fabrication / red-flags

1. **d4-heartseeker resource probe fabrication CONFIRMED:** `canon_probe_facts` economy row shows `resource_verbatim: "spirit/focus"` — this is the known probe fabrication pattern (same artifact as GoD-DH in CW2). Fetched text unambiguously: Rogues use **Energy**. Erratum queue: heartseeker resource HIGH, economy row needs correction.
2. **d4-dance-of-knives resource probe:** probe shows `resource_verbatim: "charge"`, `model: "meter"`. Fetched text: Rogue uses **Energy**. "Charge" is a mechanic description (Evade charges), not the resource name. Probe misclassification — not a fabrication of the same severity but still incorrect. Flag for erratum.
3. **d4-evade-sb resource probe:** probe shows `resource_verbatim: "evade charges"`. Fetched text (icy-veins spiritborn-skills): Spiritborn primary resource is **Vigor**. Ferocity is a Jaguar-specific secondary mechanic. Probe fabrication confirmed. Erratum queue: evade-sb resource HIGH.
4. **d4-dread-claws-warlock and d4-hammerdin-paladin stale-prior warning applied:** both kits are LoH S13 post-cutoff classes. Probe sources flagged `gl`/`sky` (low-conf scraper-adjacent). All identity/mechanics/era verdicts grounded in fetched Maxroll+icy-veins text only. Warlock resource = **Wrath** (icy-veins gear affixes); Paladin resource = **Faith** (icy-veins skills guide + search snippet). Both confirmed from fetched text.
5. **d4-hammerdin-paladin probe element `holy`:** probe says element `holy`. Fetched text does not use the word "holy" for D4 Paladin damage — Blessed Hammer currently deals physical + sacred type damage per guide language. Potential probe fabrication from D2 Hammerdin lineage importing. Flag for erratum review but verdict against mechanics claim is U (source silent on this specific term).
6. **d4-flame-shield-immortal capstone_alterations abstained:** launch-era specific aspect loadout not recoverable from accessible sources (no archived launch-era Maxroll or icy-veins guide page found). Mobalytics S4/Eternal page returned 403. Abstention recorded per NO-FABRICATION LAW.
7. **d4-cataclysm legacy status:** icy-veins archived this build at S13 (LoH). The `voh-s6+` era claim remains confirmed (active through S12 at minimum); the build's future viability in loh-s13-14 is not claimed in the spec, so no contradiction. Noted for steward awareness.

---

## Dossier coverage

- 12 kits × 6 families = 72 potential rows
- Abstained rows: 2 (`d4-flame-shield-immortal` capstone_alterations + author_credit)
- Non-abstained: 70 rows
- **Coverage: 70/72 = 97.2%**

---

## Author credits recovered

| Kit | Author(s) |
|---|---|
| d4-cataclysm | Danger (maxroll) / TheSteve (icy-veins) |
| d4-chain-lightning | pandaglassjaw (maxroll) / Lexyu (icy-veins) |
| d4-dance-of-knives | Avarilyn (maxroll) |
| d4-death-trap | Avarilyn (maxroll) |
| d4-dread-claws-warlock | wudijo (maxroll) / GhazzyTV (icy-veins) |
| d4-earthquake-barb | snail (maxroll) / Mathris (icy-veins) |
| d4-evade-sb | Ignition (maxroll) |
| d4-flame-shield-immortal | not recovered (launch-era) |
| d4-frozen-orb | pandaglassjaw (maxroll) |
| d4-hammerdin-paladin | AoinoMiku (maxroll) / MrLlamaSC + Mathris (icy-veins) |
| d4-heartseeker | DiEoxidE (maxroll) / Lexyu (icy-veins) |
| d4-hota | Beatdropper (maxroll) / Mathris (icy-veins) |

---

## Contradictions

None. 0 contradictions this batch.

---

## Erratum queue (for INGEST-13)

- **heartseeker economy probe `spirit/focus`** → should be `Energy` (Rogue). HIGH priority.
- **dance-of-knives economy probe `charge/meter`** → should be `Energy` (Rogue). Medium.
- **evade-sb economy probe `evade charges/meter`** → should be `Vigor` (Spiritborn). HIGH priority.
- **hammerdin-paladin probe element `holy`** → D4 does not use "holy" damage type; likely D2 lineage import. Review.
- **cataclysm legacy at S13** → steward note: if `loh-s13-14` era token ever added to this kit's eras, it would be CONTRADICTED; current spec stops at `voh-s6+`, consistent with the legacy archival.

---

## Cross-seam notes

- Spiritborn VoH debut confirmed from Wikipedia (October 7, 2024, Season 6). Era instrument validated.
- Warlock and Paladin debuted Lord of Hatred expansion (Season 13, April 28, 2026 per MSN journalism). Era instrument validated.
- reddit remained blocked throughout; no fetch attempts made.
- diabloimmortal.fandom.com not applicable (d4 batch).
