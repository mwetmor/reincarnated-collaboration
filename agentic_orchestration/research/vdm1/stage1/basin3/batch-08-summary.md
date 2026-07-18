# VDM-1 basin-3 batch-08 summary — kits 85-96 (d3 L85–L96)

**Batch:** 08 | **Game:** d3 | **Date:** 2026-07-18 | **Legolas instance:** batch-08

---

## Per-kit one-liners

| kit_id | verdict summary |
|---|---|
| d3-natalya-rov | identity/mechanics/set-era/late-sets CONFIRMED; s39 CONTRADICTED — set reworked to Spike Trap in S28, RoV build retired Patch 2.7.5 |
| d3-pestilence-lance | identity/mechanics/late-sets CONFIRMED; s39 UNSUPPORTED (post-cutoff) |
| d3-poj-tempest-rush | identity/mechanics/late-sets CONFIRMED; s39 UNSUPPORTED (post-cutoff) |
| d3-raekor-boulder | identity/mechanics/late-sets CONFIRMED; set-era CONTRADICTED (Boulder Toss build is S26 rework, not pre-S26 set-era); s39 UNSUPPORTED (post-cutoff) |
| d3-raiment-shenlong | identity/mechanics/set-era/late-sets CONFIRMED; s39 UNSUPPORTED (post-cutoff) |
| d3-rathma-aotd | identity/late-sets CONFIRMED; mechanics CONTRADICTED (Skeletal Mage NOT in build — "Skeletal Mages don't work for this set bonus"); s39 UNSUPPORTED (post-cutoff) |
| d3-rolands | identity/mechanics/set-era/late-sets CONFIRMED; s39 UNSUPPORTED (post-cutoff) |
| d3-s6-impale | identity/mechanics/set-era/late-sets CONFIRMED; s39 UNSUPPORTED (post-cutoff) |
| d3-shield-bash (negative) | identity/mechanics CONFIRMED; negative_canon CONTRADICTED — weakness/underpowered aspect confirmed but target framing contains two unsupported elements (see red flags) |
| d3-sotl-hammer | identity/mechanics/set-era/late-sets CONFIRMED; s39 UNSUPPORTED (post-cutoff) |
| d3-spectral-blade (negative) | identity/mechanics CONFIRMED; negative_canon CONTRADICTED — target framing contains two factual errors vs fetched text |
| d3-sunwuko-wol | identity/mechanics/set-era/late-sets CONFIRMED; s39 CONTRADICTED — S39 guide is LoD Wave of Light, not Sunwuko |

---

## Advisory verdict histogram (FILE TRUTH GOVERNS — steward recounts)

| verdict | count (advisory) |
|---|---|
| CONFIRMED | 36 |
| CONTRADICTED | 6 |
| UNSUPPORTED | 10 |
| SOURCE_NOT_FOUND | 0 |
| **Total** | **52** |

**0 SOURCE_NOT_FOUND kits.** All 12 kits had usable sources from maxroll.gg/d3 and/or icy-veins.com.

---

## Contradictions (one line each)

1. **d3-natalya-rov era s39** — "This build is no longer relevant in Patch 2.7.5." Natalya was reworked to Spike Trap in S28; RoV build did not continue to s39.
2. **d3-raekor-boulder era set-era** — Boulder Toss build is a Season 26 rework ("reworked again in Season 26 to be centered around Weapon Throw and Ancient Spear"). The build as stamped does not have set-era identity; era floor should be late-sets.
3. **d3-rathma-aotd mechanics (Skeletal Mage as core skill)** — Fetched text: "Skeletal Mages don't work for this set bonus." Skeletal Mage is NOT part of the build core; Revive + Command Skeletons are the minion sources.
4. **d3-shield-bash negative_canon** — Target framing "later reworked into Roland's set" is not attested: Shield Bash was always part of Roland's Legacy from the start, not introduced via rework. The stun-window geometry dead-coverage claim is also not found in any source.
5. **d3-spectral-blade negative_canon** — Two factual errors: (a) "channeled arc" — Spectral Blade is an instant-cast signature spell costing no resources, not channeled (Blizzard official page). (b) "without set-multiplier path" — DMO 6-piece provides 12,500% damage multiplier for skills inside Slow Time, which includes Spectral Blade; Firebird Flame Blades also uses it as primary.
6. **d3-sunwuko-wol era s39** — S39 Wave of Light is LoD (separate guide "Monk Wave of Light Build with LoD (Patch 2.7.8 / Season 39)"); Sunwuko WoL guide is labeled Season 38. Sunwuko variant superseded by LoD in s39.

---

## SNF kits

None. 0/12 kits SOURCE_NOT_FOUND.

---

## Dossier coverage

- 12 kits × 6 families = 72 dossier rows possible
- Abstained rows: d3-pestilence-lance author_credit (no byline found on maxroll page); d3-poj-tempest-rush author_credit (no byline found on maxroll page); d3-raekor-boulder author_credit (no byline found on maxroll page)
- Non-abstained: 69 / 72 = **95.8%**
- Note: probe_facts resource field for d3-raiment-shenlong listed "ignite stack (meter)" — fetched text confirms Spirit as resource (standard Monk); "ignite stack" is not a resource name, it is a probe fabrication artifact. Flagged for erratum.

---

## Author credits

| site | handle(s) |
|---|---|
| icy-veins.com | Deadset (confirmed on: natalya-rov, raiment-shenlong, rathma-aotd, rolands, s6-impale, shield-bash, sotl-hammer, spectral-blade, sunwuko-wol) |
| maxroll.gg | No bylines found on guide pages (pestilence-lance, poj-tempest-rush, raekor-boulder author_credit abstained) |
| diablo3.blizzard.com | Official (spectral-blade skill page) |

---

## Red flags for steward erratum queue

**HIGH — mechanics erratum candidates:**

1. **d3-rathma-aotd core_skills**: spec records "Skeletal Mage" as a core skill. Fetched text contradicts: "Skeletal Mages don't work for this set bonus." The minion sources are Command Skeletons + Revive. ERRATUM candidate: remove Skeletal Mage from core_skills, add Command Skeletons and Revive.

2. **d3-spectral-blade negative_canon_target framing**: Two errors in the target string — (a) "channeled arc" — Spectral Blade is an instant-cast free signature spell, confirmed by Blizzard official page; (b) "without set-multiplier path" — DMO 6pc provides 12,500% and Firebird Flame Blades uses it as primary. The negative is real (no standalone top-tier GR-pushing Spectral Blade build exists; no guide on maxroll/icy-veins as standalone build), but the two framing details are factually wrong. ERRATUM: correct negative_canon_target to "instant-cast signature spell, not channeled; DMO path exists but under-supported for top-tier GR depth."

3. **d3-shield-bash negative_canon_target framing**: "later reworked into Roland's set" — not attested; Shield Bash was always part of Roland's Legacy. "stun-window geometry created dead coverage" — not found in any source. The weakness aspect (under-supported legendaries, inconsistent damage, far behind Sweep Attack) IS confirmed. ERRATUM: strip unsupported mechanistic claims from negative_canon_target; retain "initial implementation underpowered relative to sweep-attack."

**MEDIUM — era erratum candidates:**

4. **d3-raekor-boulder era set-era**: Boulder Toss / Raekor build is a Season 26 rework build. The set existed and had a Furious Charge spam build in set-era, but that build had a different identity. Per the ik-hota lesson binding, the Boulder Toss build's era floor should be late-sets (post-S26 rework), not set-era. D-2a candidate for INGEST-13.

5. **d3-natalya-rov era s39**: RoV build ended at Patch 2.7.5 / Season 27. The `s39` era token is CONTRADICTED — by S39 the set supports Spike Trap. Remove s39 from eras for the RoV kit.

6. **d3-sunwuko-wol era s39**: Sunwuko WoL was superseded by LoD WoL in Season 39. S39 era token CONTRADICTED. Remove s39 from eras.

**LOW — probe fabrication watch:**

7. **d3-raiment-shenlong probe resource "ignite stack (meter)"**: Fetched text confirms Spirit as Monk resource. "ignite stack" is a probe fabrication artifact — not a real resource name in D3. Standard Monk Spirit resource confirmed.

---

## Batch notes

- **0 contradictions** among identity + mechanics families for the 10 positive-canon kits — all 10 had community-confirmed names and mechanics from live guides. Two era contradictions (natalya s39, sunwuko s39) and one mechanics contradiction (rathma Skeletal Mage) plus one era floor contradiction (raekor set-era).
- Both negatives (shield-bash, spectral-blade) issued CONTRADICTED verdicts against the specific negative_canon_target framing — not because the kits are positive, but because the target strings contain factual errors vs fetched text. The underlying negative character (weak/not-viable/unsupported) is real for both.
- **Necromancer debut confirmed 2017** (Rise of the Necromancer, June 27, 2017 / Season 11) — late-sets floor for pestilence-lance and rathma-aotd is consistent, no intro-check failure.
- **Crusader debut confirmed RoS-2014** — ros-early floor for shield-bash consistent; set-era floors for rolands and sotl-hammer consistent.
- **Maxroll author bylines**: maxroll guide pages for pestilence-lance, poj-tempest-rush, raekor-boulder did not surface author bylines in fetched content. Author_credit abstained on those three; Deadset confirmed as icy-veins author across 9 kits.
- **s39 token discipline**: per post-cutoff law, all s39 era rows issued as UNSUPPORTED (honest-U) for the 10 positive-canon kits — two of these (natalya, sunwuko) upgraded to CONTRADICTED because positive evidence of a DIFFERENT build occupying that slot in s39 was found (Spike Trap Natalya; LoD WoL).
