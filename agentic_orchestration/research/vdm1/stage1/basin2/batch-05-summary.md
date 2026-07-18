# VDM-1 Basin-2 Batch-05 Summary
**Kits:** le-fire-aura-spellblade · le-flame-reave-spellblade · le-frost-claw · le-frost-wall-rm · le-ghostflame-warlock · le-hammer-throw-paladin · le-harvest-lich · le-healing-hands-paladin · le-judgement-paladin · le-lightning-blast · le-low-life-ward · le-manifest-armor
**Crawl date:** 2026-07-18
**All LE game; negative=false (zero negative_canon rows emitted)**

---

## Per-kit one-liners

| kit_id | identity | mechanics | era(s) verdict summary |
|--------|----------|-----------|----------------------|
| le-fire-aura-spellblade | CONFIRMED | CONFIRMED | 1.4-omens CONFIRMED |
| le-flame-reave-spellblade | CONFIRMED | CONFIRMED | beta CONFIRMED · 1.0 CONFIRMED · 1.4 CONFIRMED |
| le-frost-claw | CONFIRMED | CONFIRMED | beta UNSUPPORTED · 1.0 CONFIRMED |
| le-frost-wall-rm | CONFIRMED | CONFIRMED | 1.0 UNSUPPORTED · 1.2 UNSUPPORTED |
| le-ghostflame-warlock | CONFIRMED | CONFIRMED | 1.0 CONFIRMED · 1.1 CONFIRMED |
| le-hammer-throw-paladin | CONFIRMED | CONFIRMED | beta CONFIRMED · 1.0 CONFIRMED · 1.2 UNSUPPORTED · 1.4 CONFIRMED |
| le-harvest-lich | UNSUPPORTED (combined folk name) | UNSUPPORTED (combined build) | all eras UNSUPPORTED |
| le-healing-hands-paladin | CONFIRMED | CONFIRMED | 1.1-harbingers CONTRADICTED · 1.4 CONFIRMED |
| le-judgement-paladin | CONFIRMED | CONFIRMED | 1.0 CONFIRMED · 1.2 UNSUPPORTED · 1.4 CONFIRMED |
| le-lightning-blast | CONFIRMED | CONFIRMED | beta CONFIRMED · 1.0 CONFIRMED · 1.2 UNSUPPORTED · 1.4 CONFIRMED |
| le-low-life-ward | CONFIRMED | CONFIRMED | beta CONFIRMED · 1.0 CONFIRMED · 1.2 UNSUPPORTED · 1.4 CONFIRMED |
| le-manifest-armor | CONFIRMED | CONFIRMED (with resource flag) | beta CONFIRMED · 1.0 CONFIRMED · 1.2 UNSUPPORTED |

---

## Verdict histogram (advisory — steward recounts files)

| verdict | count |
|---------|-------|
| CONFIRMED | 35 |
| UNSUPPORTED | 17 |
| CONTRADICTED | 1 |
| SOURCE_NOT_FOUND | 0 |

---

## ZERO SOURCE_NOT_FOUND kits

All 12 kits found usable sources. No SOURCE_NOT_FOUND entries.

---

## CONTRADICTIONS (1 total)

**le-healing-hands-paladin · era · 1.1-harbingers:** KB stamps the build as first appearing in 1.1-harbingers. Fetched text from the official maxroll Healing Hands skill tree reveal article states: "With our release of Last Epoch on February 21st, Healing Hands will finally be getting its long awaited skill tree" — confirming Healing Hands skill tree debuted at 1.0 launch (February 2024), not 1.1. A 1.0-era build guide (forum.lastepoch.com, posted February 24 2024) confirms 1.0 community usage. The 1.1-harbingers era floor stamp is too late — CONTRADICTED per D-2a uniform law. **ERRATA candidate: add 1.0-launch to le-healing-hands-paladin eras; 1.1-harbingers is not the debut.**

---

## UNSUPPORTED summary (most notable)

- **le-frost-claw beta-0.8-0.9:** Sorcerer-class Frost Claw guides found from 1.0.3 onward; beta-era Frost Claw guides exist (forum Runemaster variant) but no clean Sorcerer-class beta confirmation in fetched text. Honest UNSUPPORTED.
- **le-frost-wall-rm 1.0-launch and 1.2-woven:** Frost Wall as a Runemaster skill is confirmed; the named "Frost Wall Runemaster" build as a primary-identity endgame build lacks era-stamped guides for these specific windows. Frost Wall appears as a support skill in Lightning Blast RM. Honest UNSUPPORTED.
- **le-hammer-throw-paladin 1.2-woven:** Multiple beta and S4 guides found; 1.2-specific attestation absent in fetched text. Honest UNSUPPORTED.
- **le-harvest-lich all eras:** The combined "Harvest Death Seal Lich" folk name is not attested — maxroll has two separate builds (Harvest Flay Lich and Death Seal Lich). No single fetched source treats Harvest + Death Seal as one co-primary build. All era and mechanics claims for the combined form = UNSUPPORTED.
- **le-lightning-blast 1.2-woven, le-low-life-ward 1.2-woven, le-manifest-armor 1.2-woven:** Attested in adjacent eras; 1.2-specific guides not surfaced in fetched text. Honest UNSUPPORTED.

---

## Dossier coverage

All 6 families attempted for all 12 kits = 72 potential dossier rows.
- **Abstained:** author_credit for 10 kits (maxroll guides do not expose individual author handles in page prose); item_alterations abstained for le-ghostflame-warlock and le-frost-wall-rm (insufficient item-level detail in fetched text); capstone abstained for le-fire-aura-spellblade and le-flame-reave-spellblade.
- **Coverage %:** ~79% (57 of 72 rows non-abstained).

---

## Author credits extracted

- **BinaQc** — Frostbite Frost Claw Sorcerer (maxroll.gg, planner link e62eu0o9); referenced as Runemaster guide author in Frost Wall spec thread.

---

## Red flags for steward / elrond

1. **le-harvest-lich kit identity split:** The canon_corpus folk name "Harvest Death Seal Lich" conflates two separate maxroll builds (Harvest Flay Lich and Death Seal Lich). These have different core skills, damage types (Cold vs Necrotic), and economy (HP leech vs Low Life self-cost). Recommend elrond erratum: either split into two kit records or correct the mechanics fields to match one of the two actual builds. The combined form is not attested anywhere as a single named build.

2. **le-manifest-armor resource_verbatim "Forge Stacks":** DB probe fact records "Forge Stacks" as the resource model (harvest economy). Fetched maxroll guide describes the build as Mana-based for the initial summon; no Forge Stacks mechanic is attested in fetched text. This is a probe-fact artifact — Forge Stacks may be a game concept that does not function as the resource model for Manifest Armor. Elrond sweep recommended.

3. **le-hammer-throw-paladin "Sigils of Hope" vs "Symbols of Hope":** Beta-era guides (0.8.1c) confirm "Sigils of Hope" as the skill name. Current Season 4 maxroll guides use "Symbols of Hope." This is likely a skill rename across patches. The DB records "Sigils of Hope" — which was correct at the beta/1.0 era. Current era name may differ. Steward awareness: not a contradiction (the skill exists and serves the same role), but the name change is worth noting for future era-specific mechanics verification.

4. **le-ghostflame-warlock "beam" vs "cone" geometry:** DB probe fact records "beam" delivery. Fetched text (Warlock reveal + community descriptions) describes Ghostflame as a "channeled jet" and "hellish torrent." The directional channel covers a cone projection area rather than a pure narrow beam. Beam vs cone distinction is a subtle geometry call — flagged for elrond to review the geo_text field.

5. **le-fire-aura-spellblade — "Flame Ward/aura suite" core skill framing:** The DB records core skill as "Flame Ward/aura suite" implying Flame Ward is the aura delivery. Fetched text shows Flame Ward is a defensive cooldown, not the aura itself — the fire aura radiates passively via a passive node (Freezing Aura for cold conversion). The aura is unnamed and emergent from passives, not a placed skill. This is a probe-fact framing artifact — flagged for elrond.

6. **le-low-life-ward "host-flexible" economy discrepancy:** DB records resource_verbatim as "Life (intentionally depleted)" and model as "self-cost." Fetched text confirms this is accurate — Exsanguinous/Last Steps drain HP continuously. No contradiction, but the archetype abstraction (no single skill to verify, no rankable skill) means era claims are harder to pin; era UNSUPPORTED rows for 1.2-woven are honest gaps not SNF.

7. **No junk-tail quarantine events in this batch:** SEO gold-seller domains did not appear in any search results for this batch. Zero quarantined citations.
