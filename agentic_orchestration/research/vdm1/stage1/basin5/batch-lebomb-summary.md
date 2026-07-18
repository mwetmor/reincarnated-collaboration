# VDM-1 basin-5 BACKFILL-2 — le-bomb-lance-falconer re-crawl summary
**Date:** 2026-07-18
**Legolas batch:** lebomb (targeted re-crawl, 1 kit)

---

## Kit one-liner

**le-bomb-lance-falconer** — IDENTITY MISMATCH CONFIRMED. "Bomb Lance" does not exist as a Last Epoch skill, passive node, or community build identity in any fetched source. The corpus folk_name is a fabricated or misassigned name. The real "ballista-and-bird engine" kit is **Explosive Ballista Falconer** (community name: Explosive Ballista Falconer / Dive Bomb Explosive Ballista Falconer). All dossier payload extracted under IDENTITY_MISMATCH flag using the real attested build.

---

## Verdict histogram (ADVISORY — file truth is the count)

| Verdict | Count |
|---|---|
| CONFIRMED | 0 |
| CONTRADICTED | 3 |
| UNSUPPORTED | 1 |
| SOURCE_NOT_FOUND | 0 |

---

## Contradictions

1. **identity** — "Bomb Lance Falconer" is CONTRADICTED. No skill, passive node, guide, or forum post named "Bomb Lance" exists in any fetched source. Falconer skill set confirmed as: Falconry, Explosive Trap, Net, Aerial Assault, Dive Bomb. Sources: maxroll.gg (multiple guides), icy-veins.com, loltank.com, maxroll.gg Falconer reveal page.

2. **mechanics** — Core skill "Bomb Lance (thrown explosive)" is CONTRADICTED. The fetched real build loop is: spam Explosive Trap (0-mana) → proc explosive Ballista turrets → Dive Bomb for burst → Falconry (Falcon Strikes passive) → Smoke Bomb defense. No thrown lance. Sources: maxroll.gg Explosive Ballista Falconer (BinaQc), icy-veins.com Explosive Dive Bomb (EMP1241).

3. **era** — "Season 4 (1.4-omens) new Rogue skill" is CONTRADICTED by D-2b intro-check. Falconer debuted at Last Epoch 1.0 (February 2024). Season 4 (patch 1.4 Shattered Omens) launched March 26, 2026 — the Falconer is over 2 years old at that point, not new. Source: icy-veins guide "originally added February 19, 2024"; loltank.com build dated February 27, 2024; maxroll Season 4 update article.

---

## Dossier coverage

All 6 families populated (abstained: 0). Coverage 100%. ALL rows carry IDENTITY_MISMATCH flag — payload extracted from the attested real "ballista-and-bird" build (Explosive Ballista Falconer), not from a kit called "Bomb Lance Falconer".

| Family | Status | Source |
|---|---|---|
| skill_loop | populated, conf=0.72 | maxroll.gg BinaQc |
| skill_geometry | populated, conf=0.65 | maxroll.gg BinaQc |
| item_alterations | populated, conf=0.70 | maxroll.gg BinaQc |
| capstone_alterations | populated, conf=0.75 | icy-veins EMP1241 |
| author_credit | populated, conf=0.90 | multiple |
| variants | populated, conf=0.80 | maxroll.gg rogue page |

---

## Element-attestation notes

**Element law applied.** Fetched sources mention physical damage (Ballista primary, Dive Bomb), cold damage (Explosive Ballista Falconer via Apogee of Frozen Light, Mourningfrost — "Cold (primary)" per maxroll guide), and fire damage (Explosive Trap "inflicting fire damage" per Falconer skill description). Physical is engine-silent per element law. Cold is attestable: maxroll guide explicitly names cold damage items and cold as primary. Fire is attestable from Explosive Trap description. No element word was sourced solely from a skill name; each attestation has a damage-type descriptor from fetched text.

Element attestation summary:
- **Cold** — ATTESTED. Anchor: "Cold (primary)" in Explosive Ballista Falconer guide; Apogee of Frozen Light and Mourningfrost items. Source: maxroll.gg BinaQc.
- **Fire** — ATTESTED. Anchor: "throw traps that explode when triggered" with "inflicting fire damage" from Falconer skill description. Source: icy-veins Falconer overview.
- **Physical** — engine-silent per law (engine has no physical family).

---

## Red flags for Elrond / steward

1. **CRITICAL — kit_id re-assessment required:** `le-bomb-lance-falconer` is built around a skill name that does not exist. Elrond should evaluate whether to: (a) re-key this kit as `le-explosive-ballista-falconer` with updated folk_name, (b) retire the kit and create a new canon_corpus entry for the real build, or (c) leave with CONTRADICTED identity as a mapping GAP. The dossier payload here is for the real "Explosive Ballista Falconer" build and IS mappable.

2. **era_raw correction needed:** corpus era_raw "Season 4 (1.4-omens)" implies Falconer is a Season 4 skill. It is not — Falconer was introduced at 1.0 (February 2024). The era_raw needs correction to "1.0 (launch, Feb 2024); attested through Season 4 (1.4, 2026)".

3. **core_skills correction needed:** corpus core_skills = `["Bomb Lance", "Falconry"]`. Should be `["Explosive Trap", "Ballista", "Falconry", "Dive Bomb"]` for the Explosive Ballista Falconer variant.

4. **Mappability verdict:** The dossier payload (skill_loop + skill_geometry) IS real and mappable — the Explosive Ballista Falconer has a genuine Falcon + turret + explosive AoE identity. Cold element attested. Downstream mapping CAN proceed on the extracted payload IF Elrond corrects the identity fields first.

---

## Author credits

- BinaQc (maxroll.gg) — Explosive Ballista Falconer, Ballista Falconer
- LizardIRL (maxroll.gg) — Dive Bomb Falconer
- EMP1241 (icy-veins.com) — Falconer Explosive Dive Bomb, Falconer Bleed Bomb
- Dwight (loltank.com) — 1.0 launch guide

---

## Banned-domain enforcement

`lastepochtools.com` appeared in search results (planner URL, skill changelog) — not used as a verify or dossier source per basin-2 banned-domain precedent. Confirmed clean.
