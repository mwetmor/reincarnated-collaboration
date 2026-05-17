# Dispatch — 2026-05-17 — legolas — Track A REVERSE: 2D VFX → pool expansion-opportunity audit (Drift-14 follow-on, parallel to gandalf Track B)

**From:** knight-rider (authored per Matt directive 2026-05-17: "let's go with #1" — fire reverse-direction audit in parallel to gandalf Track B; Matt-flagged: Track A original direction is POOL→VFX only; the reverse direction surfaces pool-EXPANSION candidates that the cull-focused Track A cannot)
**To:** legolas
**Approved by:** Matt at 2026-05-17
**Status:** READY-TO-FIRE — runs parallel to gandalf Track B (different seam; no overlap)
**Mode:** A (analytical research; file inspection across catalogue + pool)
**Estimated effort:** 3-5 hours (per Track A precedent; hard cap 5h)
**Budget:** $0 LLM

**Gate-1 bypass rationale:** Matt-directed (reverse-audit explicitly authorized 2026-05-17 to fill Track A directionality gap); single-seam (legolas-only); read-only research; bounded scope (catalogue × pool cross-reference, inverted direction; no derivation); time-cap discipline; parallel-safe to gandalf Track B (different inputs/outputs).

**Acceptance summary:** Single research doc filed at `agentic_orchestration/research/knowledge/vfx-to-pool-expansion-opportunities-2026-05-17.md`. For each distinct concept-name / asset-name appearing across the 2D VFX catalogue corpus (Pimen + Pixogen + CraftPix + Elthen + CreativeKind + chierit + GandalfHardcore + Fellor + any other crawled vendor), cross-reference against the canonical pool (~156 entries) to surface: **(a) NOT-IN-POOL concept-names** that have catalogue coverage and represent plausible pool additions; **(b) pre-screened candidates** with substrate hypothesis (which canonical-four slot would this most plausibly fit?), genre-precedent signal (does the name appear in ARPG / fantasy genre vocabulary?), and canonical-pair-leak risk (would adding this name re-introduce the structural-bias problem Drift-14 surfaced?); **(c) priority-ranked shortlist** ready for gandalf disposition. Hand-off section for gandalf disposition dispatch (separate, post-Track-B).

---

## Why this dispatch exists — closing Track A directionality gap

Matt's 2026-05-17 question surfaced a real gap in Track A original scope:

> "Did Legolas only audit the fit of the current non-canonical elements across 2D pack elements/vfx? Or did Legolas also audit the 2D pack elements/vfx for named elements which are not currently available in the existing pool of non-canonical elements of the engine today? The goal with the latter would be to add elements to the engine if they fit the 2D packs."

Track A as commissioned was POOL → VFX (cull-focused). This dispatch is REVERSE direction: **VFX → POOL** (expansion-focused).

The two audits compose into the full Drift-14 closure picture:
- Track A original: which pool entries lack catalogue coverage and should be culled?
- Track A reverse (this dispatch): which catalogue concept-names lack pool entries and could be added?

Both inputs feed gandalf disposition decisions. Track B (in-flight) uses Track A original; a follow-on cascade item (post-Track-B) will use Track A reverse for pool-expansion decisions.

## Cross-seam contract change?

**Round-trip: not applicable** — research output is a doc; no schema or contract change; no production state modified. Per R11(b) Principle 6.

## Coordination with in-flight work

- **Gandalf Track B (in-flight):** different seam (design synthesis vs research data-gathering); different output (canonical-doc + dispatch authoring vs research doc); no shared files; no conflict. Track B works from Track A original empirical data; this dispatch produces NET-NEW data that feeds a follow-on cascade. Safe to run in parallel.
- **Drax Case A continuation (in-flight):** unrelated seam (demo render) and unrelated scope (sprite-scale not pool/element); no conflict.
- **Gamora Gate 3b (in-flight):** unrelated seam (simulation MS consumption); no conflict.

Per-seam discipline: this is the only legolas dispatch in-flight. Holds the discipline.

## What this dispatch produces

Single research doc at: `agentic_orchestration/research/knowledge/vfx-to-pool-expansion-opportunities-2026-05-17.md`

### Section 1 — Catalogue corpus inventory

Enumerate ALL distinct concept-names / asset-names appearing across catalogued vendors:
- Pimen (per `research/catalogue/pimen/full-2026-05-16.jsonl` + variants)
- Pixogen (per `research/catalogue/pixogen/findings-summary-2026-05-16.md`)
- CraftPix (per Step B Tier-1 crawl)
- Elthen (per Step B Tier-1 crawl)
- CreativeKind (per drax v0.20 + earlier crawl)
- chierit (per drax ingest)
- GandalfHardcore (per Samurai pack ingest)
- Fellor (per crawl)
- Any other crawled VFX vendor in `research/catalogue/`

Extract concept-names by parsing:
- Pack names (e.g., "Frostwindz Deathbringer" → "frostwindz", "deathbringer")
- Asset filenames (e.g., "Light Spell 04" → "light")
- Vendor descriptions / tags / metadata where present

De-duplicate; produce single canonical concept-name list with per-name source-attribution (which vendor(s) surface it).

### Section 2 — Pool cross-reference (inverse of Track A original)

For each Section-1 concept-name:
- **In-pool?** (exact match against ~156 pool entries; case-insensitive; common-stem matching e.g., "lightning" ↔ "lightning")
- **In-pool-but-quarantine?** (entry exists but operationally-suppressed; not the same as "not in pool" but worth surfacing — may indicate pool churn opportunity)
- **NOT-IN-POOL** (catalogue surfaces this concept but engine doesn't currently have it)

The NOT-IN-POOL set is the candidate pool for the expansion audit.

### Section 3 — Per-candidate pre-screening

For each NOT-IN-POOL candidate, capture:

- **Substrate hypothesis:** which canonical-four slot (fire / water / earth / wind / dark / light / neutral) would this most plausibly fit? Flag if ambiguous-multi-slot. Source: vendor description if available, asset visual register, common-vocabulary register.
- **Genre-precedent signal:** does this name appear in ARPG / fantasy / Isekai genre vocabulary? (Cross-reference your prior research notes on genre-vocabulary; flag if obscure / niche / single-vendor-only).
- **Vendor-coverage strength:** single-vendor surface vs multi-vendor convergent (multi-vendor convergent = stronger signal — both Pimen and Elthen ship "tornado" effects suggests "tornado" is a genre-recognized concept).
- **Canonical-pair-leak risk:** does this name structurally imply canonical-four pair binding? (Same heuristic as Track A original Section 2c). Flag HIGH-RISK candidates as expansion-skip even if they have strong VFX coverage.
- **Existing-pool-overlap risk:** does this name overlap semantically with an existing pool entry (e.g., "tornado" overlaps with the cull-candidate "hurricane")? Flag — adding overlapping entries doesn't help D1 diversity.
- **D1-rubric-amenable estimate:** rough hand-estimate of what d1_total score this name would likely earn under existing D1 rubric (genre-precedent + visualizable + fantasy-heroic + vocab-commonness). Not load-bearing; just calibrates whether the candidate is "obviously high-quality" vs "marginal."

### Section 4 — Priority-ranked shortlist

Synthesize Section 3 into priority tiers:

- **TIER 1 — STRONG CANDIDATES** (multi-vendor coverage + clean substrate + low leak-risk + low overlap-with-existing + estimated d1_total ≥ 8): ready for gandalf disposition, likely allow-list candidates
- **TIER 2 — VIABLE CANDIDATES** (good coverage but one weak dimension): ready for gandalf disposition, likely eligible-tier candidates
- **TIER 3 — INVESTIGATE** (interesting but ambiguous; needs gandalf judgment on whether worth pursuing): surface for gandalf but flag low-priority
- **REJECT** (high leak-risk OR strong-overlap-with-existing OR single-niche-vendor-only): document why rejected, do not surface to gandalf disposition

Per-candidate row: name + substrate + vendors-with-coverage + tier + brief rationale.

### Section 5 — Aggregate statistics + hand-off

- Total Section-1 catalogue concept-names enumerated
- NOT-IN-POOL candidates surfaced (raw count + breakdown by tier)
- TIER 1 / TIER 2 / TIER 3 / REJECT counts
- Per-substrate breakdown (which canonical-four slots have the most expansion opportunity?)
- Cross-reference to Track A original: are any TIER 1 candidates substrate-matched to slots that Track A cull would leave under-represented? (e.g., if Track A culls 5 wind entries and this audit surfaces 8 strong wind candidates, that's a coherent rebalancing opportunity)

**Hand-off for gandalf disposition** (separate dispatch, post-Track-B):
- TIER 1 + TIER 2 candidates as gandalf disposition input
- Per-candidate empirical-data summary (substrate + vendors + leak-risk + overlap-risk)
- Do NOT make adoption recommendations beyond tier classification — gandalf's disposition is the design-side call

## Out of scope (explicit)

- **NO design recommendations** beyond tier classification + empirical hand-off
- **NO new vendor catalogue crawling** (Mode A; use existing catalogue data; if a vendor has thin coverage, note as gap — do not crawl)
- **NO pool-addition execution** (rocket's seam if gandalf disposition approves)
- **NO D1 rubric scoring of candidates** (rocket's seam; your "D1-amenable estimate" is hand-estimate calibration only, not load-bearing)
- **NO disposition recommendations beyond tier classification** — gandalf's call which candidates land
- **NO touching gandalf Track B in-flight work** — they're producing pool-cull decisions from Track A original data; you're producing pool-expansion candidates from net-new data; outputs compose, do not collide
- **NO time-cap overrun** — 5h hard cap; if scope exceeds, surface to knight-rider before continuing
- **NO LLM-API touchpoints** — Mode A; $0 budget
- **NO V2 calibration / regen / cipher-migration follow-on work**

## Required reading

- **Your own Track A original return** (delivered inline 2026-05-17 in prior session) — same methodology, inverted direction. Reuse Section 2 substrate-alignment + canonical-pair-leak heuristics from Track A original.
- **Gandalf commit 8a89d1b:** `canonical/story/drift-audit.md` § Drift-14 re-amendment (VS2a-gating finding; canonical-bias root cause)
- **Canonical pool source-of-truth** (rocket-owned; you located it during Track A original — same path)
- **All catalogue research docs** in `agentic_orchestration/research/catalogue/`
- **Your prior D1-related research** (if any; for genre-vocabulary cross-reference)
- **Form-bias cipher-migration paths-audit:** `agentic_orchestration/research/cipher-migration-paths-audit-2026-05-16.md` (canonical-pair-leak risk cross-reference)

## Acceptance criteria

- [ ] Doc filed at `agentic_orchestration/research/knowledge/vfx-to-pool-expansion-opportunities-2026-05-17.md`
- [ ] Section 1 catalogue corpus inventory complete (all crawled vendors enumerated; concept-names de-duplicated)
- [ ] Section 2 pool cross-reference complete (NOT-IN-POOL set surfaced)
- [ ] Section 3 per-candidate pre-screening (substrate + genre-precedent + vendor-coverage + leak-risk + overlap-risk + D1-amenable estimate)
- [ ] Section 4 priority-ranked shortlist (TIER 1 / 2 / 3 / REJECT with rationale)
- [ ] Section 5 aggregate stats + hand-off
- [ ] Per-data-point source attribution
- [ ] Cross-reference to Track A original noted where rebalancing opportunities surface
- [ ] Time-cap honored (≤ 5h hard cap; surface to knight-rider if approaching)
- [ ] Knight-rider notified with: doc path, NOT-IN-POOL count, TIER 1 / TIER 2 counts, per-substrate breakdown, top-5 TIER 1 candidates with substrate + vendor-coverage summary, any cross-reference-to-Track-A-original rebalancing opportunities surfaced

## Tag policy

- **No git tag** (research persona; file timestamp suffices)

---

## Completion record

**Completed:** 2026-05-17
**Doc path:** `agentic_orchestration/research/knowledge/vfx-to-pool-expansion-opportunities-2026-05-17.md`
**Catalogue concept-names enumerated:** 28 (element-vocabulary register; 436 raw tokens extracted, filtered to concept-name candidates)
**NOT-IN-POOL candidates:** 28
**Tier breakdown:** TIER 1: 5 / TIER 2: 8 / TIER 3: 3 / REJECT: 12
**Per-substrate breakdown:** fire: 0 T1 (1 T3 fireworks) / water: 0 / earth: 1 T1 (poison) + 1 T2 (acid) / wind: 0 T1 (1 T2 lightning post-cull candidate + 1 T1 electric as wind-flex) / dark+light+beyond-C4: 4 T1 (holy/void/shadow/electric) + 5 T2 (divine/cosmic/death/portal/stellar) / neutral-temporal: 1 T2 (time)
**Top-5 TIER 1 candidates:**
1. holy — light/holy (beyond C4) — Pimen + CreativeKind + Pixogen + Frostwindz (4 vendors) — D1-est 10
2. electric — wind/water-flex — Pimen + Fellor + Pixogen + Ansimuz (4 vendors) — D1-est 9
3. poison — earth/dark-flex — CreativeKind + Fellor (2 vendors) — D1-est 9
4. void — dark/neutral (beyond C4) — Pixogen + Frostwindz (2 vendors) — D1-est 9
5. shadow — dark (beyond C4) — Pimen + CreativeKind + Frostwindz (3 vendors) — MEDIUM leak-risk flagged — D1-est 9
**Rebalancing opportunities vs Track A original:**
- Track A original culled 8 wind-storm cluster entries (hurricane/gale/cyclone/tempest/gust/howl/typhoon/squall). This audit surfaces electric (TIER 1, wind/water-flex) + lightning (TIER 2, wind/water-flex post-cull upgrade) as partial wind-rebalancing candidates. Net: 2 wind-adjacent additions vs 8 potential culls — wind-slot becomes smaller but less concentrated. No full numerical rebalancing available from catalogue; this is the coherent call (cull-then-add, not add-to-balance).
- Earth-slot: Track A may have flagged animal-anatomy entries (chitin/scale/horn/tooth/claw/bone/marrow). This audit surfaces poison and acid as earth-flex additions that diversify earth beyond the mineral/anatomy family. Rebalancing opportunity: replace animal-anatomy culls with biological/chemical earth-adjacents.
**Time spent:** ~3.5h
**Notes for knight-rider:** The dominant structural finding is that catalogue expansion opportunity concentrates in BEYOND-CANONICAL-FOUR substrates (dark/light/holy/void/cosmic). The current 156-entry pool covers only fire/wind/water/earth. If the pool stays canonical-four-only, viable additions narrow to electric (wind-flex) + poison/acid (earth-flex). If pool expands to 6-8 elements, Tier 1 becomes fully actionable. Gandalf disposition needs to resolve this structural question before expansion candidates can land. Flagging as primary hand-off item for the cascade dispatch.
