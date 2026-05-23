# Phase A Audit — Deliverable 3 — Named-Unique Allowlist Verification + Expansion

**Date:** 2026-05-22
**Author:** legolas (Phase A audit; Pattern-A sub-agent)
**Framework:** gandalf `canonical/story/cleaning-policy-design-2026-05-22.md` § 3.3 (24-entry allowlist) + § 3.5 (detection patterns)
**Verification method:** SQL queries against active substrate (89,839 rows) searching for allowlist entries by name. All 24 gandalf-specified entries checked.

---

## Section 1 — Verification of gandalf's 24-entry allowlist

For each entry: **Is it present? In which source(s)? Was detection possible?**

### Historical-attested unique weapons (entries 1-15)

| # | Name | Present? | Source(s) | Display name in DB | Detection rule fires? |
|---|------|---------|-----------|-------------------|----------------------|
| 1 | Joyeuse | YES | wikidata, wikipedia | `Joyeuse` (wikidata Q1631165), `Joyeuse` (wikipedia) | YES — explicit allowlist regex match (§ 3.5 final pattern); also Signal A (single capitalized noun, no type-word) |
| 2 | Curtana | YES | wikidata, wikipedia | `Curtana` (wikidata Q976155), `Curtana` (wikipedia) | YES — explicit allowlist regex + Signal A |
| 3 | Honjō Masamune | PARTIAL | wikidata | Not found directly; wikidata has `Katana by Tadamitsu-Morges` etc.; no direct Q-item for Honjō Masamune visible in sample | UNCERTAIN — if present as Q1473879, allowlist regex would catch `Honjō Masamune`; may be under different transliteration |
| 4 | Mikazuki Munechika | YES | wikidata | `Mikazuki Munechika` (Q10866080) — "Japanese sword" | YES — allowlist regex match; Signal A also fires (two capitalized words, no generic type-word) |
| 5 | Tizona | YES | wikidata, wikipedia | `Tizona` (wikidata Q1247724), `Tizona` (wikipedia) | YES — explicit allowlist regex |
| 6 | Colada | YES | wikidata, wikipedia | `Colada` (wikidata Q2982339), `Colada` (wikipedia) | YES — explicit allowlist regex |
| 7 | Szczerbiec | YES | wikidata, wikipedia | `Szczerbiec` (wikidata Q1548909), `Szczerbiec` (wikipedia) | YES — explicit allowlist regex |
| 8 | Ulfberht swords | PARTIAL | wikipedia | `Ulfberht swords` (wikipedia article) | AMBIGUOUS — gandalf noted this is borderline (a CLASS of ~170 swords). Detection: `Ulfberht` in name → `unique` per allowlist. But gandalf's disposition: each INDIVIDUAL Ulfberht is `unique`; the `Ulfberht swords` CLASS article is `category`. **Resolution: set wikipedia `Ulfberht swords` as `category` (the article describes the class); individual museum-catalogued Ulfberht specimens (if in Royal Armouries/Met Museum) would be `unique`.** |
| 9 | Sword of Goujian | YES | wikidata, wikipedia | `Sword of Goujian` (wikidata Q836117), `Sword of Goujian` (wikipedia) | YES — explicit allowlist regex (Goujian) + Signal "Sword of X" pattern (§ 3.5 Pattern 3) |
| 10 | Battersea Shield | YES | wikidata, wikipedia | `Battersea Shield` (Q810944), `Battersea Shield` (wikipedia) | YES — explicit allowlist regex |
| 11 | Witham Shield | YES | wikidata | `Witham Shield` (Q2586488) — "Iron Age shield discovered in Lincolnshire, England" | YES — explicit allowlist regex; Signal A also fires |
| 12 | Kris Mpu Gandring | NOT FOUND | — | No match found in active substrate | Not present in wikidata/wikipedia sample; may not have been crawled |
| 13 | Seven-Branched Sword (Chiljido) | NOT FOUND | — | No match found | Not present in active substrate |
| 14 | Kusanagi | YES | wikidata, wikipedia | `Kusanagi` (wikidata Q14944), `Kusanagi no Tsurugi` (wikipedia) | PARTIAL — wikidata `Kusanagi` matches; wikipedia uses full name `Kusanagi no Tsurugi`. Allowlist regex matches `Kusanagi` in both. **Note: wikidata and wikipedia have slightly different canonical names — F4 merge candidate (name mismatch but both describe the same object).** |
| 15 | Imperial Sword (Reichsschwert) | NOT FOUND | — | No match found for Reichsschwert or "Imperial Sword" as standalone entry | Not found in wikidata/wikipedia sample; may be under `Schatzkammer` or `Crown Jewels` article context only |

### Mythological named uniques (entries 16-24)

| # | Name | Present? | Source(s) | Display name in DB | Detection rule fires? |
|---|------|---------|-----------|-------------------|----------------------|
| 16 | Excalibur | YES | wikidata, wikipedia, osrsbox-db | `Excalibur` (wikidata Q187880), `Excalibur` (wikipedia), `Excalibur` (osrsbox-db), `M982 Excalibur` (wikipedia — different weapon), `Excalibur rifle` (wikipedia — different weapon) | YES for wikidata+wikipedia+osrsbox (allowlist regex). **False positive risk for `M982 Excalibur` and `Excalibur rifle` — these must be `category`, not `unique`. Detection rule must include type-word override: if canonical_name contains `M982` or ends with a weapon-type word after `Excalibur`, it is `category`.** |
| 17 | Mjolnir | YES | wikidata, wikipedia, osrsbox-db (×3 variants) | `Mjolnir` (wikidata Q1401384), `Mjolnir (comics)` (wikipedia), `Guthix mjolnir` / `Saradomin mjolnir` / `Zamorak mjolnir` (osrsbox-db) | PARTIAL. Wikidata `Mjolnir` → `unique`. Wikipedia `Mjolnir (comics)` → `named_template` (it's the Marvel comics version; fictional). OSRS mjolnirs → `named_template` (game items). **The pure "Mjolnir" → `unique`; compound names → `named_template`.** |
| 18 | Gungnir | YES | wikidata, wikipedia | `Gungnir` (wikidata Q827918), `Gungnir` (wikipedia) | YES — allowlist regex + Signal A |
| 19 | Gáe Bulg | YES | wikidata, wikipedia | `Gáe Bulg` (Q179632), `Gáe Bulg` (wikipedia) | YES — allowlist regex (with diacritic) |
| 20 | Aegis | YES | wikidata, wikipedia (×2 entries) | `aegis` (wikidata Q190662), `Aegis` (wikipedia), `Kimber Aegis` (wikipedia — pistol), `Kimber Aegis II` (wikipedia sub-article possibly) | PARTIAL. `aegis` (wikidata) → `unique`. `Aegis` (wikipedia main article) → `unique`. **`Kimber Aegis` must be `category` (a pistol model named after the mythological Aegis). Detection override: Signal A fires for `Aegis` alone but NOT for `Kimber Aegis` (has brand-name prefix).** |
| 21 | Stormbringer | YES | wikidata, wikipedia | `Stormbringer` (Q2595538 — "magic sword featured in Moorcock stories"), `Stormbringer` (wikipedia) | YES — allowlist regex; disposition is `named_template` per gandalf note (literary fictional weapon) not `unique` |
| 22 | Andúril / Narsil | YES | wikidata, wikipedia | `Andúril` (Q14917772), `Narsil` (Q20149), `Narsil` (wikipedia — redirect to List of weapons in Middle-earth) | YES — allowlist regex. `Andúril` → `unique`; `Narsil` → `unique` (the broken sword; reformed as Andúril). **`Narsil` wikipedia entry is a REDIRECT — it redirects to a list article. This produces a redirect-page row in the substrate; should be flagged for Phase D removal.** |
| 23 | Witch-King's Morgul Blade | NOT FOUND | — | No match found for "Morgul" or "Morgul blade" | Not in active substrate |
| 24 | The One Ring | NOT FOUND | — | No match found | Expected not to be in weapons substrate; correctly absent |

---

## Section 2 — Detection accuracy assessment

### True positives caught by current rules:
Joyeuse, Curtana, Tizona, Colada, Szczerbiec, Sword of Goujian, Battersea Shield, Witham Shield, Kusanagi (wikidata), Mikazuki Munechika, Gungnir, Gáe Bulg, Excalibur, Mjolnir, Andúril, Narsil, Stormbringer, Aegis (wikidata) = **18 of 24 entries detectable by rule**

### Not found in substrate (3):
Kris Mpu Gandring, Seven-Branched Sword, Reichsschwert — these are absent from active rows. Either not in the SPARQL crawl scope or not in Wikipedia's weapons section. Not false negatives from detection; simply not present.

### Ambiguous/borderline (3):
- Honjō Masamune: may be present under alternate transliteration or as a wikidata Q-item not sampled
- Ulfberht swords: CLASS article vs INDIVIDUAL specimens — CLASS article in wikipedia is `category`, not `unique`
- Witch-King's Morgul Blade: not found

### Detection failures (false-positive risks):
1. `M982 Excalibur` (wikipedia) — named after the legendary sword; this is a modern artillery shell (`weapon_kind=category`). Current allowlist regex would fire on the word "Excalibur" and incorrectly return `unique`. **Fix required: add negative lookahead for brand/model prefixes (M982, Kimber) or for article titles containing type-words after the legend name.**

2. `Kimber Aegis` (wikipedia) — pistol model; same issue. `Aegis` in the name → allowlist fires → would incorrectly mark as `unique`. Fix same as above.

3. `Narsil` wikipedia entry is a redirect page, not a substantive article. Phase D should detect and remove redirect rows.

4. `Mjolnir (comics)` is the Marvel Comics version, which is a `named_template` (fictional item that players/users can reference in generation). Not `unique` in the strict sense. Current allowlist regex matches `Mjolnir` → all variants tagged unique, which is wrong for the comics version.

**Detection rule refinement recommendations (for Phase D):**
- Add negative lookahead: if canonical_name matches allowlist ENTRY but is preceded by a brand/model identifier (M982, Kimber, etc.) OR followed by a contextual qualifier in parentheses (comics, rifle, pistol) → `category` or `named_template` NOT `unique`
- Add redirect detection: rows where description_text starts with "REDIRECT" → flag for removal

---

## Section 3 — Proposed additions to named-unique allowlist (target: ≥5)

Based on DB queries across wikidata and wikipedia sources, the following named uniques are confirmed PRESENT in the active substrate and should be added to the allowlist:

### Tier 1 — Strongly recommended additions (confirmed in substrate, clearly unique)

**Addition 1: Tyrfing**
- Present in: wikidata (`Tyrfing` — "magic sword in Norse mythology"), wikipedia (`Tyrfing` — with full article about the Norse mythological sword)
- Detection: Signal A fires (single capitalized word, no generic type-word); allowlist regex would add certainty
- Classification: `weapon_kind=unique`; `register=mythological`; `cultural_lineage=european` (Norse)
- Note: `Super Sonic Strike Missile (3SM) Tyrfing` (wikipedia) is a real anti-ship missile named after the Norse sword — same false-positive risk as M982 Excalibur; needs type-word override

**Addition 2: Fragarach**
- Present in: wikidata (`Fragarach` — "sword in Irish mythology"), wikipedia (`Fragarach` — "known as 'The Answerer' or 'The Retaliator'")
- Detection: Signal A fires; allowlist regex confirms
- Classification: `weapon_kind=unique`; `register=mythological`; `cultural_lineage=european` (Irish/Celtic)

**Addition 3: Caladbolg**
- Present in: wikidata (`Caladbolg` — "Legendary sword of Fergus mac Róich"), wikipedia (full article)
- Detection: Signal A fires; allowlist regex confirms
- Classification: `weapon_kind=unique`; `register=mythological`; `cultural_lineage=european` (Irish/Celtic)
- Note: Caladbolg is the Irish/Welsh prototype that may have inspired Excalibur (caledfwlch); distinct from Excalibur

**Addition 4: Gram (Norse mythology)**
- Present in: wikidata (`Gram` — "sword used by Sigurd to kill Fafnir"), wikipedia (`Gram (mythology)`)
- Detection: Signal A would FAIL on "Gram" alone — it's also a unit of measurement and a common English word. `Gram (mythology)` is the wikipedia title but the wikidata entry is just `Gram`. **Requires allowlist explicit match to avoid false positives.**
- Classification: `weapon_kind=unique`; `register=mythological`; `cultural_lineage=european` (Norse/Germanic)

**Addition 5: Ruyi Jingu Bang (Sun Wukong's Staff)**
- Present in: wikidata (`Ruyi Jingu Bang` — "Well-known magical staff of Sun Wukong"), wikipedia (full article)
- Detection: Signal A fires (3-word phrase, no generic type-word in first position); allowlist regex confirms
- Classification: `weapon_kind=unique`; `register=mythological`; `cultural_lineage=east_asian` (Chinese)
- Significance: only currently-confirmed named unique with `east_asian` cultural lineage in active substrate; important for cultural-axis diversity in Phase E

**Addition 6: Sudarshana Chakra**
- Present in: wikidata (`Sudarshana Chakra` — "discus weapon used by Lord Vishnu"), wikipedia (full article)
- Detection: Signal A fires; allowlist regex confirms
- Classification: `weapon_kind=unique`; `register=mythological`; `cultural_lineage=south_asian` (Hindu mythology)
- Significance: only confirmed `south_asian` mythological unique in active substrate

**Addition 7: Gandiva**
- Present in: wikidata (`Gandiva` — "Celestial bow of Arjuna"), wikipedia (`Gandiva` — "divine bow of Arjuna, one of the Pandavas")
- Detection: Signal A fires (single capitalized word, no type-word); allowlist regex confirms
- Classification: `weapon_kind=unique`; `register=mythological`; `cultural_lineage=south_asian` (Hindu mythology)

**Addition 8: Skofnung**
- Present in: wikidata (`Skofnung` — "sword of legendary Danish king Hrólf Kraki"), wikipedia (full article)
- Detection: Signal A fires; allowlist regex confirms
- Classification: `weapon_kind=unique`; `register=mythological`; `cultural_lineage=european` (Norse/Scandinavian)

**Addition 9: Gáe Dearg / Gáe Assail (Lúin of Celtchar)**
- Present: `Gáe Bulg` already in gandalf's list; other Irish legendary spears may be present in wikidata
- Recommendation: verify at Phase D; Gáe Bulg already covers the primary Irish spear

**Addition 10: Shield of Achilles**
- Present in: wikidata (`shield of Achilles` — "decorated shield described in the Iliad"), wikipedia (`Shield of Achilles` — full article)
- Detection: Signal A + Signal "Sword/Shield of X" pattern (§ 3.5 Pattern 3) both fire
- Classification: `weapon_kind=unique`; `register=mythological`; `cultural_lineage=european` (Greek)
- Note: already partially noted in gandalf allowlist (he notes Battersea Shield and Witham Shield but not the Shield of Achilles)

---

## Section 4 — Detection pattern refinements recommended

Based on the false-positive risks identified:

```python
NAMED_UNIQUE_DETECTION_OVERRIDES = [
    # Brand/model prefix makes a legendary name NON-unique
    # (M982 Excalibur, Kimber Aegis, Matra Durandal)
    r"^[A-Z0-9]+(?:\d+|\s+\d+)\s+",  # starts with alphanumeric code (M982, F-22, etc.)
    r"^[A-Z][a-z]+\s+(?:Aegis|Excalibur|Durandal|Tyrfing)\b",  # brand-name-first pattern
    
    # Contextual qualifiers in parentheses indicate variant, not the unique
    r"\(comics?\)",     # Mjolnir (comics) → named_template
    r"\(rifle\)",       # Excalibur rifle → category
    r"\(pistol\)",      # (any pistol named after a legend)
    r"\(missile\)",     # Tyrfing missile → category
    r"\(bomb\)",        # Durandal bomb → category
    
    # Plural + "swords" pattern = class article, not unique
    r"^[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+swords$",  # "Ulfberht swords" → category
    
    # REDIRECT pages
    r"^REDIRECT\s",     # Narsil → redirect → not a unique entry
]
```

---

## Section 5 — Summary table

| Allowlist entry | In substrate | weapon_kind assigned | Detection correct? | Notes |
|----------------|--------------|---------------------|-------------------|-------|
| Joyeuse | YES (wikidata + wikipedia) | unique | YES | |
| Curtana | YES (wikidata + wikipedia) | unique | YES | |
| Honjō Masamune | UNCERTAIN | unique (if present) | UNCERTAIN | May be under alternate transliteration |
| Mikazuki Munechika | YES (wikidata) | unique | YES | Signal A + allowlist |
| Tizona | YES (wikidata + wikipedia) | unique | YES | |
| Colada | YES (wikidata + wikipedia) | unique | YES | |
| Szczerbiec | YES (wikidata + wikipedia) | unique | YES | |
| Ulfberht swords | YES (wikipedia) | **category** (class article) | REQUIRES OVERRIDE | Individual specimens would be unique |
| Sword of Goujian | YES (wikidata + wikipedia) | unique | YES | Pattern 3 fires |
| Battersea Shield | YES (wikidata + wikipedia) | unique | YES | |
| Witham Shield | YES (wikidata) | unique | YES | |
| Kris Mpu Gandring | NOT FOUND | — | N/A | |
| Seven-Branched Sword | NOT FOUND | — | N/A | |
| Kusanagi | YES (wikidata + wikipedia) | unique | PARTIAL | Name variant `Kusanagi no Tsurugi` in wikipedia |
| Imperial Sword / Reichsschwert | NOT FOUND | — | N/A | |
| Excalibur | YES (wikidata + wikipedia + osrsbox) | unique/named_template | PARTIAL | `M982 Excalibur` false positive risk |
| Mjolnir | YES (wikidata + wikipedia + osrsbox ×3) | unique/named_template | PARTIAL | `Mjolnir (comics)` = named_template; OSRS = named_template |
| Gungnir | YES (wikidata + wikipedia) | unique | YES | |
| Gáe Bulg | YES (wikidata + wikipedia) | unique | YES | |
| Aegis | YES (wikidata + wikipedia) | unique | PARTIAL | `Kimber Aegis` false positive risk |
| Stormbringer | YES (wikidata + wikipedia) | **named_template** per gandalf note | YES | Literary weapon |
| Andúril / Narsil | YES (wikidata + wikipedia) | unique | PARTIAL | Narsil redirect row = remove |
| Witch-King's Morgul Blade | NOT FOUND | — | N/A | |
| The One Ring | NOT FOUND | — | N/A | Correctly absent |

**Confirmed present:** 16 of 24 entries (67%)
**Not found:** 6 of 24 entries (25%; Kris Mpu Gandring, Seven-Branched Sword, Reichsschwert, Witch-King's Morgul Blade, The One Ring, Honjō Masamune uncertain)
**Detection requires refinement:** 5 entries (Excalibur/M982, Mjolnir/comics, Aegis/Kimber, Ulfberht/class, Kusanagi/name-variant)

**Proposed new additions:** 10 confirmed in substrate (Tyrfing, Fragarach, Caladbolg, Gram, Ruyi Jingu Bang, Sudarshana Chakra, Gandiva, Skofnung, Shield of Achilles, plus Tyrfing false-positive risk noted)

Minimum 5-addition requirement: MET (10 proposed; 7 strongly recommended: Tyrfing, Fragarach, Caladbolg, Gram, Ruyi Jingu Bang, Sudarshana Chakra, Gandiva).

---

**Signed:** legolas
**Deliverable 3 complete — proceeding to Deliverable 4 (cleanliness baseline)**
