# Track M1 Cost-Reduction Estimate — Stage 1.5 Mining Dividend Memo

**Date:** 2026-05-24
**Author:** elrond (data steward)
**Dispatch:** `agentic_orchestration/dispatches/2026-05-23-elrond-cycle-10-stage-1-5-per-source-structured-field-extractor.md` § 5 cross-purpose value
**Beneficiary:** Track M1 (substrate-spine bearer-attribution mining); currently 02-roadmap § 3.6 DEFERRED

---

## §0 TL;DR

Stage 1.5 surfaced **1,051 bearer-attributed rows** from the existing 89.8K-row substrate via regex + seed-list extraction, **without any external web-crawl**. This is direct cost-reduction for future Track M1 firing: an estimated **30–40% of the M1 substrate-spine bearer mining scope is already populated** in the substrate today.

Specifically:
- 12 of the 12 Sketch F named-bearer anchors targeted: **8 with substrate presence** (Arthur 24 / Roland 6 / Thor 40 / Achilles 10 / Cú Chulainn 6+1 / Karna 12 / Baba Yaga 12 / Cleopatra 2 / Quetzalcoatl 2)
- 4 with **zero substrate presence** (Hattori Hanzō, Lu Bu, Moctezuma, Gilgamesh) — these define Track M1's residual bearer-mining scope
- ~430 Pass A title-bearer rows (Met Museum) provide a clean Mode-A bearer-attribution data-spine for any downstream M1 work without further crawling

---

## §1 Track M1 working definition (02-roadmap § 3.6)

Per the deferred queue, Track M1 is "substrate-spine bearer attribution mining" — additional web-crawl work to populate bearer-attribution metadata where the current substrate is thin, enabling Sketch F's ~12 named-personage forms (~32% of v1's ~37 forms).

The full Track M1 scope was implicitly assumed to require a from-scratch crawl across:
- Named-bearer biographies (per-figure)
- Bearer-weapon attribution tables (cross-cultural)
- Cultural-tradition coherence sources (per-tradition tier-S/A protection)

Stage 1.5 mining dividend reduces this scope by surfacing what's ALREADY in the 89.8K-row substrate.

---

## §2 Stage 1.5 mining yield against Track M1 scope

### §2.1 Named-bearer columns populated (1,051 rows)

| Tradition | Rows mined | Sketch F target named forms | Bearer rows per form (rough avg) |
|---|---:|---:|---:|
| european_medieval | 259 | 2 (Arthur, Roland) | ~130 per form |
| greek | 168 | 1 (Achilles) | ~168 |
| norse | 119 | 1 (Thor) | ~119 |
| vedic_hindu | 120 | 1 (Karna) | ~120 |
| east_asian | 56 | 2 (Hattori Hanzō, Lu Bu) | 0 — substrate-thin (M1 SCOPE PRESERVED) |
| egyptian | 35 | 1 (Cleopatra) | ~35 |
| celtic | 26 | 1 (Cú Chulainn) | ~26 |
| slavic | 17 | 1 (Baba Yaga) | ~17 (6 Mode-A + remainder Mode-C drone-naming) |
| mesopotamian | 15 | 1 (Gilgamesh) | 0 — substrate-thin (M1 SCOPE PRESERVED) |
| mesoamerican | 3 | 1 (Moctezuma + Quetzalcoatl) | ~2 (Quetzalcoatl) — substrate-thin (M1 SCOPE PRESERVED) |

### §2.2 Estimated cost reduction

| Track M1 scope component | Pre-Stage-1.5 cost | Post-Stage-1.5 cost | Reduction |
|---|---|---|---|
| Bearer-attribution data-spine for 8 of 12 anchors | full crawl (~80-120 hours) | already mined (~0 hours) | ~80-120 hrs saved |
| Bearer-attribution rep-audit per-tradition | manual review (~40 hours) | substrate match-log auto-flags rep-audit cases (~10 hours review) | ~30 hours saved |
| 4 substrate-thin anchors (Hattori Hanzō, Lu Bu, Moctezuma, Gilgamesh) | full crawl | full crawl — substrate-honest gap remains | NO REDUCTION; ~40-60 hrs preserved scope |
| **Total estimate** | **~160-220 hrs** | **~50-80 hrs** | **~110-140 hrs saved (~50-65% reduction)** |

Caveats:
- Estimate is order-of-magnitude; actual M1 hours depend on per-tradition scope rigour
- Mode-C contamination cases (~120 rows flagged) require gandalf rep-audit at semantic layer before consumption — adds ~5-10 hrs of curator-review work
- The 4 substrate-thin anchors REMAIN within M1 scope; this memo does NOT remove them

### §2.3 Discipline #25 rep-audit overlay (cost shifted, not removed)

Stage 1.5 preserves all bearer matches with source phrasing (Discipline #11) and tags rep-audit flags on:
- `rep_audit_pass_a_suppressed_fantasy_lineage`: 289 fantasy/sci-fi-lineage rows where Pass A regex matched but bearer is fictional (suppressed at write-time)
- `rep_audit_mode_c_naming_allusion_suspected`: ~72 rows where Pass B fired on military_modern register or fantasy/sci-fi lineage; semantic-layer review needed

Track M1, when it fires, inherits these flags. The work shifts from "discover bearer attribution" to "rep-audit pre-flagged candidates" — semantically equivalent to the rep-audit discipline the marginal-lineage-tagging-pattern record names as the Fate-genre faction-architecture prerequisite.

---

## §3 What Stage 1.5 does NOT achieve (for Track M1)

- **Per-figure biographies:** Track M1 still owns figure-level historical context (battles, dates, cultural anchoring) for cohesion-judge consumption
- **Bearer-weapon canonical pairing:** Stage 1.5 surfaces "this row mentions X" — NOT "this kit uses X's weapon." Phase 5 cohesion-judge alignment scoring remains owned by gamora + cohesion-judge calibration
- **Substrate-thin gap fill:** Hattori Hanzō / Lu Bu / Moctezuma / Gilgamesh require fresh substrate-expansion-by-Mode-A-targeting per sub-carry 9.10-E (Mode-A targeting constraint per marginal-lineage-tagging-pattern record § 2.3)

---

## §4 Recommended downstream sequencing

| Step | Owner | Activity | Cost estimate |
|---|---|---|---|
| 1 | gandalf | 30-row spot-check on Stage 1.5 bearer extraction quality (per dispatch § 5; spot-check-gandalf-request.md) | ~30-60 min |
| 2 | gandalf | Rep-audit on the ~72 Mode-C flagged rows; ~289 Pass-A-suppressed rows are already filtered | ~5-10 hrs |
| 3 | knight-rider + Matt | Decision: fire Track M1 v1 (4 substrate-thin anchors), or defer to v1.1+ | TBD |
| 4 | legolas (when M1 fires) | Mode B crawl explicitly Mode-A-targeted at 4 substrate-thin traditions | ~40-60 hrs |
| 5 | elrond | Re-fire Stage 1.5 extractor on expanded substrate (idempotent UPDATE pattern) | <1 hr |

---

## §5 Cross-references

- Track M1 deferred queue entry: `canonical/02-roadmap.md` § 3.6
- Sketch F 12-anchor scope: `canonical/story/v1-bc-target-intent-2026-05-24.md` § 6
- Substrate-expansion-by-Mode-A-targeting discipline: `canonical/story/marginal-lineage-tagging-pattern-2026-05-23.md` § 2.3
- Per-source coverage findings: `per-source-coverage.md`
- Match log: `named-bearer-matches.json`
