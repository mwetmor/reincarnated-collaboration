# VDM-1 basin-4 batch-01 summary — Lost Ark (b01)

**Batch:** b01 | **Kits:** 11 | **Date:** 2026-07-18 | **Mode:** B (systematic crawl)

---

## CANARY WAVE — Live-Source / Domain Report (CRITICAL)

**maxroll.gg/lost-ark: LIVE and PRIMARY.**

- Initial slug guesses (`/arthetinean-skill-machinist-guide`, `/asuras-path-breaker-guide`) → 404.
- Correct slug pattern discovered from `/lost-ark/build-guides` index: kebab-case with trailing `-raid-guide` or `-raid-build-guide` or `-build-guide` suffix.
- All 11 kit guide pages fetched successfully with correct slugs.
- Community tier list pages (`/tierlists/community-class-tier-list-february-2025`) live and returning structured data.
- URL `/tierlists/community-tier-list-february` (2024 list, no year suffix) also live.
- `reddit.com/r/lostarkgame`: **BLOCKED** — WebFetch cannot reach reddit directly. Search results reference reddit content but direct fetch fails. b02–b05 should not attempt direct reddit fetches; use WebSearch for reddit content.
- `papunika.com`: not tested (maxroll coverage was sufficient for all 11 kits).
- Icy-Veins: appears in search results for LA content — NOT tested for fetchability. Brief says likely 404; confirmed live in search results but not relied upon.
- Junk-tail domains (aoeah/mmoexp/igvault/g2g/eldorado): blocked in all searches per law.

**b02–b05 domain-order adjustment:** Use slug index at `maxroll.gg/lost-ark/build-guides` to resolve correct slugs before fetching individual kit pages. Direct slug guessing will 404.

---

## Per-Kit One-Liners

| kit_id | verdict summary | notes |
|---|---|---|
| la-arthetinean-skill-machinist | identity CONFIRMED, mechanics CONFIRMED, era CONFIRMED, negative_canon CONTRADICTED | DB mech_note "C-tier" and negative=1 contradicted by Feb 2025 tier list: B-Tier. See red flags. |
| la-asuras-path-breaker | identity CONFIRMED, mechanics CONFIRMED, era CONFIRMED | DB mech_note "back-attack" contradicted by fetched text: front-attack spec. Red flag filed. |
| la-barrage-enhancement-artillerist | identity CONFIRMED, mechanics CONFIRMED, era CONFIRMED | Exhaustion removal confirmed. Flamethrower+Air Raid confirmed. No element attestation. |
| la-berserkers-technique | identity CONFIRMED, mechanics CONFIRMED, era CONFIRMED | All stat bonuses confirmed verbatim. Bloody Rush/Dark Rush confirmed. |
| la-blessed-aura-paladin | identity CONFIRMED, mechanics CONFIRMED, era CONFIRMED | Holy Aura party buff numbers confirmed verbatim. Sword of Justice brand confirmed. |
| la-brawl-king-storm-breaker | identity CONFIRMED, mechanics CONFIRMED, era CONFIRMED | Non-positional confirmed. Stamina/Shock gauge loop confirmed. |
| la-communication-overflow-summoner | identity CONFIRMED, mechanics UNSUPPORTED, era CONFIRMED | Akir-as-buff mechanics not explicitly confirmed in fetched text; Ancient Orbs/Akir Burst confirmed. "Pets don't panic/miss" language absent from guide. D-Tier confirmed Feb 2025. |
| la-control-glaivier | identity CONFIRMED, mechanics CONFIRMED, era CONFIRMED | 40% Flurry bonus confirmed (DB said 36% — minor discrepancy, fetched text governs). |
| la-death-strike-sharpshooter | identity CONFIRMED, mechanics CONFIRMED, era CONFIRMED | Debuff values confirmed: 27% boss damage, 12% hawk-absent. |
| la-deathblow-striker | identity CONFIRMED, mechanics CONFIRMED, era CONFIRMED | 3-orb system confirmed. Blast Formation/Supernova NOT in main build (Kurzan Front only). |
| la-demonic-impulse-shadowhunter | identity CONFIRMED, mechanics CONFIRMED, era CONFIRMED | All transformation stats confirmed. Eternal Blood perma-form confirmed. |

---

## Verdict Histogram (advisory — steward recounts from files)

| verdict | count |
|---|---|
| CONFIRMED | 31 |
| UNSUPPORTED | 1 |
| CONTRADICTED | 1 |
| SOURCE_NOT_FOUND | 0 |

**Total claim rows:** 33

---

## Contradictions (one line each)

1. **la-arthetinean-skill-machinist / negative_canon:** DB mech_note claims "C-tier" and negative=1 justified by underperformance; fetched Feb 2025 tier list ranks AS Machinist as **B-Tier** (same tier as EL Machinist). Feb 2024 tier list ranked it A-Tier. No source found placing it C-tier in the la-t4-ark-passive era. The negative=1 flag may reflect an earlier meta period or an incorrect internal assessment. Steward (Elrond/Gandalf) should review whether the negative classification holds.

---

## Internal Inconsistencies (not contradiction verdicts — DB-vs-DB, flagged per law)

1. **la-asuras-path-breaker / mech_note:** DB says "positional back-attack discipline." Fetched maxroll guide says Front Attack affix applies (+20% Damage on front-side hits). Asura's Path is a **front-attack** spec. DB field is internally inconsistent with fetched truth. Recommend Elrond correction.
2. **la-control-glaivier / damage bonus:** DB mech_note implies 36% (matching Berserker's Technique Burst Mode). Fetched maxroll guide says "+40% Damage Increase to Flurry skills." Fetched text governs; 40% is the correct figure.
3. **la-deathblow-striker / core_skills:** DB lists "Blast Formation" and "Supernova" as core skills. Fetched guide shows these appear only in the Kurzan Front variant section, not the standard/LTS Reset main build rotation. Core build skills are Lightning Tiger Strike, Tiger Emerges, Charging Kick.
4. **la-communication-overflow-summoner / mech_note:** DB describes Akir as "turns Akir summon from a damaging skill into a powerful buff for normal summons." Fetched guide describes Akir Burst (identity activation) as a separate skill unlocked at Ancient Orbs — the framing is slightly different. The "buff for normal summons" characterization is UNSUPPORTED by fetched text.

---

## SOURCE_NOT_FOUND Kits

None. All 11 kits had live guides on maxroll.gg.

---

## Dossier Coverage

| family | rows present | abstained (payload null) |
|---|---|---|
| skill_loop | 11 | 0 |
| skill_geometry | 11 | 0 |
| item_alterations | 11 | 0 |
| capstone_alterations | 11 | 0 |
| author_credit | 11 | 0 |
| variants | 11 | 0 |

**Coverage: 66/66 rows (100%). Zero null-payload abstentions.**

Note: Several `item_alterations` and `skill_geometry` rows have reduced confidence (0.5–0.6) where fetched summaries did not capture full gem/accessory tables. Full gem tables would require deeper per-page parsing; core mechanics are captured. Steward may want to re-fetch with gem-table-specific prompts for any kits requiring full item_alterations detail.

---

## Author Credits (maxroll.gg contributors)

| author | kits covered |
|---|---|
| Sekwah | la-arthetinean-skill-machinist, la-blessed-aura-paladin, la-brawl-king-storm-breaker, la-communication-overflow-summoner, la-deathblow-striker, la-demonic-impulse-shadowhunter |
| Civo | la-barrage-enhancement-artillerist, la-berserkers-technique, la-control-glaivier, la-death-strike-sharpshooter |
| Raeinor | la-asuras-path-breaker |
| Perciculum | reviewer on Sekwah/Civo guides |

---

## Element-Attestation Notes (ELEMENT LAW applied)

**Zero element attestations across all 11 kits.** All 11 are element-silent per THE D4 NAME-ONLY LAW and the LA element-light baseline.

Specific cases reviewed and ruled element-silent:

- **la-arthetinean-skill-machinist:** "Flame Buster" is a tripod modifier name on Energy Buster skill — skill/tripod name only, not a damage-type descriptor. No fire damage attestation.
- **la-barrage-enhancement-artillerist:** "Sea of Fire" is an Ark Passive node name; "Napalm Shot" is a skill name. Neither is an enemy-directed damage-type descriptor. No fire element attestation.
- **la-brawl-king-storm-breaker / la-asuras-path-breaker:** "Shock gauge" and "Shock skills" are resource/class-mechanic names, not lightning element damage types.
- **la-deathblow-striker:** "Lightning Tiger Strike" and "Lightning Whisper" are skill names. Fetched maxroll guide does NOT describe these skills as dealing "lightning damage" as a damage-type; lightning appears exclusively in skill names. Search result summary mentioned "lightning energy strike" in passing — not verbatim guide text, insufficient for attestation. **Element-silent per D4 NAME-ONLY LAW.**
- **la-blessed-aura-paladin:** "holy energy" mentioned in passing, not as a damage-type classification. Element-silent.
- **la-demonic-impulse-shadowhunter:** All damage references generic; no elemental typing.

Downstream mapping note: Deathblow Striker has the highest probability of lightning element connection given skill names, but no fetched guide text applied lightning as a damage-type descriptor to enemy effects. If Elrond or Gandalf needs a definitive ruling, a targeted re-fetch asking specifically "does the game UI label these skills' damage as lightning-type?" would resolve it.

---

## Red Flags for Steward

1. **NEGATIVE_CANON CONTRADICTED (la-arthetinean-skill-machinist):** Current meta evidence (Feb 2025: B-Tier; Feb 2024: A-Tier) does not support the negative=1 classification for this kit in the la-t4-ark-passive era. If the negative classification was based on an earlier meta period, the era stamp should reflect that; if it was a misclassification, Elrond should correct. **This kit may belong in positive canon.**
2. **POSITIONING ERROR (la-asuras-path-breaker):** DB mech_note states "back-attack discipline." Fetched source is unambiguous: Front Attack spec. Elrond correction needed on mech_note field.
3. **CORE_SKILLS MISMATCH (la-deathblow-striker):** DB lists Blast Formation and Supernova as core skills. These are Kurzan Front variant only, not standard rotation. Elrond correction recommended.
4. **CONTROL GLAIVIER DAMAGE BONUS:** DB implies 36%; fetched text says 40%. Minor but should be corrected for downstream accuracy.
