# Dispatch — 2026-05-16 — legolas — Track A: pool × VFX catalogue concept-coverage audit (Drift-14 VS2a-gating)

**From:** knight-rider (authored per gandalf commit 8a89d1b — Drift-14 VS2a-gating reclassification + audit kickoff authorization; Matt directive Day-4 close: "elements map cleanly across 2D VFX + halt LLM API canonical-pair visibility confusion")
**To:** legolas
**Approved by:** Matt at 2026-05-16 Day 4
**Status:** PENDING — VS2a-GATING; sequence ahead of VS2a regen.
**Mode:** A (analytical research; file inspection across pool + catalogue)
**Estimated effort:** 3-5 hours (per gandalf scoping)
**Budget:** $0 LLM

**Gate-1 bypass rationale:** Matt-directed (VS2a-gating per gandalf Drift-14 reclassification); single-seam (legolas-only); read-only research; bounded scope (pool × catalogue cross-reference, no derivation); time-cap discipline.

**Acceptance summary:** Single research doc filed at `agentic_orchestration/research/knowledge/pool-vfx-coverage-audit-2026-05-16.md` (or canonical equivalent). For each entry in the canonical-pool element-name list (~156 entries across allow-list / eligible / quarantine per memory), cross-reference against 2D VFX catalogue (Pimen + Pixogen + CraftPix + Elthen + CreativeKind + chierit + GandalfHardcore + any other crawled vendors) on (a) direct concept-name coverage (does any catalogued VFX asset map to this element name?) (b) substrate alignment (does the catalogued asset's substrate match the element name's intended register?) (c) canonical-pair leak risk (does the element name structurally imply canonical-four mapping that the form-bias cipher migration was supposed to cipher?). Synthesis table actionable for gandalf Track B authoring. Knowledge-gap flags for entries with no coverage.

---

## Why this dispatch exists — Drift-14 canonical-bias finding

Per gandalf commit 8a89d1b § Drift-14 re-amendment:

> **D1 rubric pushes selector toward canonical-four conformity → form-bias instance the Stage 1 work was supposed to close at the player-facing surface.**

The form-bias Stage 1+2+3 cipher migration shipped engine-side closure of canonical-four leakage on LLM-bound + export-packet + manifest paths. But Drift-14 surfaces a structural bias: the D1 rubric (element-name selector quality scorer) ranks names by canonical-four conformity criteria, pushing the selector toward names that PARSE as canonical-four-aligned even when the per-season cosmological-vocabulary aims to abstract them.

**Matt's directive operationalizes:** "We need the elements to map cleanly across 2D VFX and to halt LLM API confusion around canonical pair visibility."

Two specific concerns:
1. **2D VFX mapping cleanness** — when the LLM emits a season's cosmological-vocabulary names (e.g., "pall" / "miasma" / "hurricane" / "billow"), do those names map to actual catalogued VFX assets that visually represent them coherently?
2. **Canonical-pair visibility halting** — LLM-API path may still leak canonical-four pair structure (e.g., names that lexically suggest "fire-water-earth-wind" pair binding) even when the form-bias closeout was supposed to abstract them.

Track A (this dispatch) is the EMPIRICAL DATA gathering. Track B (separate gandalf dispatch, follows this return) is the design-side synthesis + recommendation.

## Cross-seam contract change?

**Round-trip: not applicable** — research output is a doc; no schema or contract change; no production state modified. Per R11(b) Principle 6.

## What this dispatch produces

Single research doc at: `agentic_orchestration/research/knowledge/pool-vfx-coverage-audit-2026-05-16.md`

### Section 1 — Pool element-name inventory

Pull the canonical element-name pool list (~156 entries per knight-rider memory; 81 allow-list / 40 eligible / 35 quarantine). Source-of-truth: rocket-owned config file (likely in `~/Games/reincarnated-engine/src/reincarnated/foundation/` or `element/` or `generation/`).

Per entry: name + d1_status + d1_total + primary canonical-four slot + flex-slot if any.

### Section 2 — 2D VFX catalogue cross-reference

For each pool entry, cross-reference against catalogued VFX assets:
- Pimen (Mode-B crawled 2026-05-16; 46 distinct packs per `research/catalogue/pimen/full-2026-05-16.jsonl`)
- Pixogen (Mode-B crawled 2026-05-16; per `research/catalogue/pixogen/findings-summary-2026-05-16.md`)
- CraftPix (per Step B Tier-1 crawl)
- Elthen (per Step B Tier-1 crawl)
- CreativeKind (per drax v0.20 + earlier crawl)
- Any other crawled VFX vendor in `research/catalogue/`

Per entry × per vendor:
- **(a) Direct concept-name coverage:** does any catalogued asset's name OR description map to the pool entry? (e.g., pool "lantern" → Pimen "Light Spell 04" if visual match)
- **(b) Substrate alignment:** does the catalogued asset's substrate (fire / water / earth / wind / dark / light / etc.) match the pool entry's intended register?
- **(c) Canonical-pair leak risk:** does the pool name structurally imply a canonical-four mapping that the cipher migration should have abstracted? (e.g., "fire-eye" lexically suggests fire-canonical pair binding even when cipher migration aims to present it as a non-canonical grouping-layer label)

Flag knowledge gaps where:
- Pool entry has NO catalogued VFX coverage (Track B may recommend pool-cull OR acquisition)
- Catalogued VFX coverage exists but substrate-misaligned (Track B may recommend pool-cull OR vendor-asset-swap)
- Canonical-pair leak risk high (Track B may recommend selector-side hard-floor amendment)

### Section 3 — Synthesis table

Per-pool-entry status:
- **GREEN** — clean coverage; substrate-aligned; no canonical-pair leak risk
- **YELLOW** — partial coverage OR substrate-misaligned OR leak risk
- **RED** — no coverage AND/OR canonical-pair leak risk AND/OR cull-candidate

Surface aggregate statistics:
- % pool entries GREEN / YELLOW / RED
- % canonical-pair-leak-risk entries (raw count + percentage of pool)
- Per-vendor coverage rate (which vendors cover the most pool entries?)
- Pool-cull candidates (RED entries that Track B may recommend dropping from pool)

### Section 4 — Hand-off for gandalf Track B

Surface the empirical inputs gandalf Track B needs:
- Pool-cull candidate list (with rationale per entry)
- Selector hard-floor amendment input (which D1 rubric criteria push toward canonical-pair leak risk?)
- Vendor-acquisition recommendations (where coverage gaps suggest specific vendor packs to acquire)
- Cipher-migration paths-audit cross-reference (does any pool entry leak through a path not in the existing paths-audit?)

Do NOT make recommendations beyond the empirical hand-off. Track B is gandalf's design-side synthesis.

## Out of scope (explicit)

- **NO design recommendations** beyond empirical-input hand-off for Track B
- **NO new vendor catalogue crawling** (Mode A; use existing catalogue data)
- **NO pool-cull execution** (rocket's seam if Track B recommends)
- **NO selector hard-floor amendment** (rocket's seam if Track B recommends)
- **NO LLM prompt re-authoring** (star-lord's seam if needed)
- **NO B11 / B12 / other engine-feature work**
- **NO MS / scale / drax-side touchpoints**
- **NO time-cap overrun** — 5h hard cap; if scope exceeds, surface to knight-rider before continuing

## Required reading

- Gandalf commit 8a89d1b: `canonical/story/drift-audit.md` § Drift-14 re-amendment (VS2a-gating finding; canonical-bias root cause)
- `canonical/16-project-roadmap.md` § VS2a (pool-VFX-mapping audit row added)
- Element-name pool source-of-truth (rocket-owned; likely `foundation/` or `generation/` or `element/`)
- All catalogue research docs in `agentic_orchestration/research/catalogue/`
- Form-bias cipher-migration paths-audit: `agentic_orchestration/research/cipher-migration-paths-audit-2026-05-16.md` (for canonical-pair leak risk cross-reference)
- Star-lord Stage 3 cipher migration MIGRATION.md (the engine-side closure that this audit verifies didn't fully close at structural level)

## Acceptance criteria

- [ ] Doc filed at `agentic_orchestration/research/knowledge/pool-vfx-coverage-audit-2026-05-16.md`
- [ ] Section 1 inventory complete (~156 pool entries; status + slot info per entry)
- [ ] Section 2 cross-reference complete across all crawled VFX vendors
- [ ] Section 3 synthesis table actionable (per-entry GREEN/YELLOW/RED + aggregate stats)
- [ ] Section 4 hand-off lists empirical inputs for Track B
- [ ] Per-data-point source attribution
- [ ] Knowledge-gap flags surfaced
- [ ] Time-cap honored (≤ 5h hard cap; surface to knight-rider if approaching)
- [ ] Knight-rider notified with: doc path, GREEN/YELLOW/RED aggregate %, pool-cull candidate count, top-3 vendor-acquisition recommendations (if any), top-3 selector-hard-floor recommendations (if any)

## Tag policy

- **No git tag** (research persona; file timestamp suffices)

---

## Completion record

**Completed:** _<date>_
**Doc path:** _<path>_
**Aggregate pool status:** _<%G / %Y / %R>_
**Pool-cull candidate count:** _<n>_
**Top vendor-acquisition recommendations:** _<list>_
**Top selector-hard-floor recommendations:** _<list>_
**Time spent:** _<hours>_
**Notes for knight-rider:**
