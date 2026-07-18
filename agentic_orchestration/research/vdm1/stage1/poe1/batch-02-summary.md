# VDM-1 Stage-1 PoE1 Batch-02 Summary

**Kits processed:** 12 (lines 13-24 of poe1-search-specs.jsonl)
**Date:** 2026-07-18
**Steward:** gandalf | **Executor:** legolas

---

## Per-kit one-liners

| kit_id | verdict summary |
|---|---|
| poe1-bladefall-bladeblast | Identity/mechanics/era all CONFIRMED. BF/BB Occultist active in 3.10-3.13 with forum guides; Tripolarbear (maxroll) is primary guide author. |
| poe1-blood-magic-kit | Identity and mechanics CONFIRMED from poedb/fandom. Era stamps UNSUPPORTED — system-record kit; no build-grain era attestation found; expected per db-only status. |
| poe1-boneshatter | Identity/mechanics/era CONFIRMED. Zizaran (maxroll) primary guide. Slayer vs Juggernaut tension documented. |
| poe1-caustic-arrow | Identity/mechanics/era CONFIRMED. Scottoria (3.12 forum) attested-era snapshot available. Trickster and Occultist variants both documented. |
| poe1-charged-dash | Identity/mechanics CONFIRMED. Era CONFIRMED (guides 3.3 through 3.14+). negative_canon CONFIRMED: pulses cannot overlap (intrinsic single-target weakness) and teleport cannot be canceled — source-quoted. |
| poe1-cleave | Identity/mechanics CONFIRMED. Era CONFIRMED (guides 3.11, 3.23). negative_canon UNSUPPORTED — no fetched text explicitly states the no-lever kill causation; recorded as UNSUPPORTED per no-fabrication law. |
| poe1-coc-ice-nova | Identity/mechanics/era CONFIRMED. Cospri's Malice mandatory item quote secured. 3.7 era attestation via pathofexileclub.wordpress.com. |
| poe1-cold-dot-occ | Identity/mechanics/era CONFIRMED. TbXie (poe-vault) primary guide. Vortex instant-cast note: removed in 3.23 — relevant era boundary documented. |
| poe1-crackling-lance | Identity/mechanics CONFIRMED. Era CONTRADICTED — DB stamps 3.7-3.13 but skill introduced in patch 3.12 (Heist); cannot have been meta 3.7-3.11. Correct era span should be 3.12-3.13 at minimum. |
| poe1-cwdt-loop | Identity/mechanics/era CONFIRMED. FR + Petrified Blood loop confirmed community-coined ~3.14. Heartbound Loop variant documented (3.25). |
| poe1-cyclone | Identity/mechanics/era CONFIRMED. Nurseos (overgear) and multiple forum guides covering 2.x through 3.20+. Ngamahu alias confirmed. |
| poe1-dark-pact | Identity/mechanics/era CONFIRMED. poetech#3681 (3.0 forum) attested-era Wayback snapshot available. GhazzyTV (poe-vault) as current-generation guide author. |

---

## Batch verdict histogram

| verdict | count |
|---|---|
| CONFIRMED | 34 |
| UNSUPPORTED | 17 |
| CONTRADICTED | 1 |
| SOURCE_NOT_FOUND | 0 |

Total claim rows: 52 (4 families x 12 kits + 4 dossier-only abstain rows folded into claim audit).

UNSUPPORTED breakdown: all 12 negative_canon N/A rows (negative=false kits) + Blood Magic era + Cleave negative_canon kill mechanism. All UNSUPPORTED are expected-and-honest: either system-record kit, N/A field, or genuinely source-silent on the specific causal claim.

---

## CONTRADICTIONS — 1 total

**poe1-crackling-lance / era claim:**
DB stamps this kit as era "3.7-3.13." Crackling Lance was introduced in patch 3.12.0 (Heist league, September 2020). It cannot have been meta during 3.7-3.11. The correct attestable era is 3.12-3.13 at minimum, extending through 3.20+.
Source: multiple guide titles explicitly dated 3.12, "Heist league" introduction confirmed by mmogah.com and pathofexile.com/forum announcement. Era stamp coarse-prior flag was set in the search spec (.85) — the contradiction is a prior-risk materializing.
**Elrond action required:** correct era field from "3.7-3.13" to "3.12-3.13" (or wider if 3.20+ is confirmed).

---

## SOURCE_NOT_FOUND kits

None. All 12 kits returned qualifying sources. No stop-and-report threshold triggered.

---

## Dossier coverage per family (of 12 kits)

| family | covered (non-abstained) | abstained |
|---|---|---|
| skill_loop | 12 | 0 |
| skill_geometry | 11 | 1 (blood-magic-kit — keystone has no geometry) |
| item_alterations | 12 | 0 |
| capstone_alterations | 11 | 1 (blood-magic-kit — no ascendancy node alteration per keystone scope) |
| author_credit | 10 | 2 (poe1-charged-dash: no author name extracted; poe1-cwdt-loop: no named author) |
| variants | 12 | 0 |

Overall dossier coverage: **93%** of non-N/A family slots filled from fetched text.

---

## Author credits gathered

| kit_id | author_handle | site |
|---|---|---|
| poe1-bladefall-bladeblast | Tripolarbear (reviewed by Raxxanterax) | maxroll.gg |
| poe1-bladefall-bladeblast | TbXie | poe-vault.com |
| poe1-bladefall-bladeblast | TraviiGrinds | pathofexile.com/forum |
| poe1-boneshatter | Zizaran | maxroll.gg |
| poe1-caustic-arrow | Scottoria (Kevin Rasins) | pathofexile.com/forum |
| poe1-caustic-arrow | Moon | poe-vault.com |
| poe1-cleave | IsneakyI | pathofexile.com/forum |
| poe1-cold-dot-occ | TbXie | poe-vault.com |
| poe1-cyclone | Nurseos | overgear.com |
| poe1-dark-pact | GhazzyTV | poe-vault.com |
| poe1-dark-pact | poetech#3681 | pathofexile.com/forum (3.0 era) |

---

## Red flags

1. **Crackling Lance era contradiction** (see above) — DB field needs correction. Not a rubber-stamp batch.
2. **PoEWiki Anubis block**: poewiki.net returned access-denied for all fetches (Anubis bot protection). All mechanics verified via poedb.tw, poe-vault.com, odealo.com, and pathofexile.com/forum instead. Coverage was not degraded but future batches should budget extra fetches to compensate.
3. **Blood Magic era UNSUPPORTED**: system-record kit with mechanic-grain (not build-grain); era stamps not verifiable at build level with available indexed sources. Expected and flagged.
4. **Cleave negative_canon UNSUPPORTED**: The "extrinsic-no-lever" death class is recorded in DB but no fetched text explicitly attests the kill mechanism — the community simply moved to better skills without a documented hard-nerf event. This is honest: the death class is an inference, not a source-attested event. Elrond should note in curation.

---

**Contradiction count: 1 — NOT zero.** Batch is not a rubber stamp. See Crackling Lance era flag above.
