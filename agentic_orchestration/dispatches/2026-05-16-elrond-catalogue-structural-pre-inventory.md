# Dispatch — 2026-05-16 — elrond — Catalogue structural pre-inventory (Q4-agnostic scaffold)

**From:** knight-rider
**To:** elrond
**Approved by:** Matt at 2026-05-16 Day 4 (per knight-rider proposal — survives Q4 lock direction; useful prep work that unblocks the later catalogue-abstraction-analysis dispatch the moment gandalf's Q4 framework lands)
**Status:** PENDING — ACTIVE
**Estimated effort:** 1 session (~2-3 hours); inventory + scaffold work, not analysis. No code changes; no schema migrations.
**Acceptance:** A structural pre-inventory document at `agentic_orchestration/research/curated/catalogue-structural-pre-inventory-2026-05-16.md` capturing the categorical dimensions of the existing 46-pack curated Pimen catalogue (element, mechanic, register, resolution_band, source format, license, cost-tier). Counts, distributions, and cross-tabulations across the dimensions. This is the scaffolding the later Q4-locked abstraction analysis will operate against — not the analysis itself.

---

## Context — why this dispatch exists

Per the project roadmap (`canonical/16-project-roadmap.md` §VS2b), the catalogue abstraction analysis is a critical-path input for Q4 cipher-width decision in gandalf's form-bias-cadence-strategy doc. The full analysis depends on:
- (a) gandalf's Q4 framework landing (in flight right now)
- (b) star-lord's catalogue-mapping experiment results (queued)

Both upstream feeds are in motion but not yet returned. Meanwhile, there is **prep work that survives whatever Q4 framework lands**: a clean structural inventory of the catalogue we already have.

**This dispatch is that prep.** It produces the scaffolding the abstraction analysis will reference — counts, distributions, dimensional shape — without making the abstraction-shape decision itself.

**Why not wait for Q4?** Because the inventory is Q4-agnostic — the structural dimensions exist regardless of how Q4 lands. Doing the inventory now means: the moment Q4 lands, the abstraction analysis dispatch can be authored with the inventory as a pre-existing input, saving ~1 session of round-trip latency at the critical-path moment.

**Out-of-scope:** abstraction analysis itself, clustering candidates, dimensional reduction recommendations, Q4-driven shape proposals. Those wait for Q4.

## What this dispatch produces

A single document: `agentic_orchestration/research/curated/catalogue-structural-pre-inventory-2026-05-16.md`.

Structure:

### Section 1 — Catalogue snapshot

Top-line numbers from `pimen-catalogue-curated-2026-05-16.jsonl` (46 packs, post-curation):
- Total pack count (46 confirmed)
- Total asset count across all packs (sum from curated records)
- Per-pack asset-count distribution (min / median / mean / max / std)
- Date coverage (first curation date, last; staleness if any)

### Section 2 — Categorical dimension inventory

For each dimension below, produce counts + percentages + value list:

| Dimension | Expected source field(s) | What to report |
|---|---|---|
| **element_primary** | from curated record | full value list with counts (e.g., fire 12, water 8, earth 6, ...) |
| **mechanic_category** | from curated record (spell / impact / aura / projectile / etc.) | full value list with counts |
| **derived_register** (per rubric R1-R8) | from curated record | distribution across registers (hand-drawn-pixel, retro-16bit, vector, etc.) |
| **resolution_band** | from curated record | distribution (tiny / pixel / standard / hd / unknown) |
| **file_format** | from curated record | distribution (PNG-sheet, PNG-frames, GIF, MP4, Aseprite-source, RAR-archived, ZIP-archived, ...) |
| **license** | from curated record | distribution (royalty-free-commercial, CC-BY 4.0, CC0, vendor-specific) |
| **cost_tier** | from curated record (free / tier-01 / tier-02 / tier-03+ / paid-unscored) | distribution |
| **pack_register_consistency** | from curated record (advisory) | counts (consistent / mixed / unknown) |
| **bundle_membership** | from `pimen-bundle-relationships-2026-05-16.json` | how many packs are bundle members; how many bundles; per-bundle pack count |
| **has_aseprite_source** | curated note (13 confirmed) | yes/no count |

### Section 3 — Cross-tabulations (the inventory's load-bearing output)

For the abstraction analysis to be useful, knowing the JOINT distributions matters more than the marginals. Produce cross-tabs for the high-information pairs:

1. **element × mechanic** — which elements ship which mechanics? (e.g., fire mostly spell + impact; earth ships more aura?). Surface gaps (which element-mechanic pairs have ZERO coverage in the current catalogue).
2. **element × register** — does the catalogue have register-parity across elements? (e.g., is fire concentrated in hand-drawn-pixel while water has retro-16bit drift?)
3. **mechanic × license** — which mechanics have license constraints? (CC-BY tracking implication: which mechanic types have CC-BY entries that need attribution?)
4. **cost_tier × derived_register** — is the locked register (hand-drawn-pixel) concentrated in paid tiers, or does the free tier carry weight?
5. **file_format × pack_register_consistency** — is "mixed" register correlated with specific file formats?

For each cross-tab: present as a matrix with counts; flag the 2-3 most surprising cells (high concentration or unexpected gap).

### Section 4 — Coverage gaps surfaced by inventory

WITHOUT proposing abstraction decisions, list what the marginals + cross-tabs reveal as catalogue gaps:
- Element types with zero coverage
- Mechanics with zero coverage
- Element × mechanic pairs with zero coverage
- Registers with thin coverage (<5% of catalogue)
- CC-BY-attribution overhead spots
- Bundle dependencies that constrain selection

**Do NOT propose fixes** (vendor crawls, acquisition decisions). Just enumerate. Knight-rider routes fixes via separate dispatches (legolas crawl decisions, Matt acquisition decisions, etc.) once Q4 lands.

### Section 5 — Open-question parking lot for the abstraction analysis

Things the inventory cannot answer alone — they need Q4 framework + experiment results. Park them with explicit "needs Q4" or "needs experiment" flags so the future abstraction-analysis dispatch can pick them up:
- What's the right abstraction granularity (e.g., elements as primitives vs element-mechanic pairs as primitives)?
- What does "non-overlapping vendor coverage" mean in the abstraction shape?
- Per the embodiment-axis substrate work, which catalogue dimensions feed which generator inputs?

This is parking, not analysis. One-line entries per question, with the dependency flag.

## What this dispatch does NOT do

- **No abstraction analysis.** That's the follow-on dispatch once Q4 lands.
- **No vendor-acquisition recommendations.** Matt-decision territory; awaits VS2b acquisition planning.
- **No clustering analysis.** Same reasoning.
- **No schema changes** to the catalogue or curated records.
- **No regen of curation.** Pure consumption-side inventory.

## Required reading

- `agentic_orchestration/research/curated/pimen-catalogue-curated-2026-05-16.jsonl` (the curated catalogue — your primary input)
- `agentic_orchestration/research/curated/pimen-bundle-relationships-2026-05-16.json` (bundle membership)
- `agentic_orchestration/research/curated/pimen-curation-log-2026-05-16.md` (your curation log — context on what was decided during curation)
- `agentic_orchestration/research/curated/catalogue-rubric-schema.md` (rubric definitions — `derived_register`, `resolution_band`, etc.)
- `agentic_orchestration/research/curated/catalogue-rubric-validation-2026-05-16.md` (rubric validation context)
- `canonical/16-project-roadmap.md` §VS2b (why this prep matters for the abstraction-analysis followup)

## Cross-seam considerations

- **Gandalf:** the inventory feeds gandalf's downstream form-bias-cadence-strategy doc when the abstraction analysis lands. No action needed from gandalf during this dispatch.
- **Star-lord:** the catalogue-mapping-and-grouping experiment is downstream of this inventory; once both this inventory AND the experiment return, the abstraction-analysis dispatch operates with full inputs. No action from star-lord during this dispatch.
- **Legolas:** if the inventory surfaces a clear coverage gap that Matt wants filled before VS2b ships, knight-rider authors a legolas crawl-dispatch for the gap-fill vendor. This dispatch surfaces the gap; doesn't decide the fill.
- **Knight-rider:** notify at completion. Next dispatch in this chain is the abstraction-analysis follow-on, which waits on gandalf's Q4 framework + star-lord's experiment.

## Tag policy

No tag for this dispatch (documentation-only; no code changes). Just file the deliverable and update your AGENT_STATE.

## Acceptance criteria

- [ ] Deliverable at `agentic_orchestration/research/curated/catalogue-structural-pre-inventory-2026-05-16.md`
- [ ] All 5 sections present (snapshot / dimension inventory / cross-tabs / gaps / open-question parking)
- [ ] Cross-tabs include the 5 high-information pairs in Section 3
- [ ] Gaps section enumerates without proposing fixes
- [ ] Open-question parking lot lists explicit Q4 / experiment dependencies
- [ ] AGENT_STATE.md (`research/curated/AGENT_STATE.md` or equivalent) updated
- [ ] Knight-rider notified at completion with: doc path, top-3 surprising cells in cross-tabs, and any flags

## Out of scope (explicit)

- Catalogue abstraction analysis (waits for Q4 + experiment)
- Vendor acquisition recommendations
- Clustering or dimensional-reduction analysis
- Schema changes
- Regen of curation
- Mapping to engine generator inputs (that's part of the eventual abstraction-analysis follow-on)

---

## Completion record

**Completed:** 2026-05-16 (elrond session, ~2h elapsed)

**Deliverable path:** `agentic_orchestration/research/curated/catalogue-structural-pre-inventory-2026-05-16.md`

**Status:** COMPLETE

**Total assets inventoried:** 47 curated rows (post 1-row category-split from 46 raw Pimen rows). Single source (`itch-pimen`), single crawl session, schema v1.0 throughout.

**Top-3 surprising cross-tab cells:**

1. **element × mechanic has 1 joint cell out of 242 possible** (§ 3.1). Of 22 mechanic-tagged assets, only 1 carries any `pimen-element:` tag — the multi-element smoke pack. Pimen's element-keyed spell packs and mechanic-keyed buff/debuff packs are structurally disjoint at the tagging layer. Pressures Q-SHAPE-1 (whether the abstraction's primitives are elements, mechanics, or element-mechanic pairs).
2. **cost_tier × derived_register concentration** (§ 3.5). 26 of 28 hand-drawn-pixel rows (92.9%) are paid; 16 of 19 free rows (84.2%) are `manual-review` pending visual inspection. The locked register's ship-ready coverage is mostly behind a paywall pre-inspection-queue-drain.
3. **mechanic × license CC-BY concentration** (§ 3.4). The catalogue's 2 CC-BY assets together cover 100% of `heal`/`healing` and ~50% of `slash`/`thrust`/`hit-effect` mechanic-tag presence. Drax filter behavior on attribution-required materially shifts mechanic-family coverage.

**Gaps enumerated (count):** 9 sub-sections in § 4 — element / mechanic / element×mechanic / register / six-axis-rubric / CC-BY / bundle / category-embodiment-decomposition / source. Three of six rubric axes (palette_size, shading_technique, linework_style) are 100% `unknown`; full six-axis coverage is 0% across the catalogue.

**Open questions parked (count):** 14 — 4 catalogue-design (Q-PRI-1..4), 5 abstraction-shape (Q-SHAPE-1..5), 3 experiment-dependent (Q-EXP-1..3), 4 elrond-internal sequencing (Q-INT-1..4).

**Notes for knight-rider:**

- **Structural finding flagged for upstream visibility:** the dispatch's reference to `mechanic_category` (Section 2 table) describes a dimension that is **not a primary column** in catalogue.db. It's reconstructed at query-time from free-text style_tags (Legolas-inferred). The catalogue has no controlled mechanic-vocabulary; tags are fragmented (22 distinct values across the 22 mechanic-leaning assets). Whether mechanic_category should be promoted to a primary column (v1.x schema entry) is Q-PRI-1 — pressures the abstraction-shape decision when gandalf's Q4 lands.
- **Single-vendor caveat applies throughout.** Every distribution and cross-tab describes Pimen's shape, not "catalogue-wide" patterns. The abstraction analysis should expect distributions to reshape materially when CraftPix / CreativeKind / Foozle land.
- **No follow-on dispatches needed before Q4.** Inventory is the Q4-agnostic prep work; abstraction analysis is the downstream dispatch. The only elrond-internal lever is Q-INT-1 (visual-inspection queue activation), already on Matt's acquisition-trigger queue per Day-4 close.
- **Cross-tab 5 substitution noted inline.** Section 3 pair 5 (`file_format × pack_register_consistency`) had no data — `pack_register_consistency` is `unknown` across all 3 registered packs. Substituted `file_format × manual_review_queued` as the meaningful proxy; rationale documented in § 3.6.
- **AGENT_STATE.md updated** with this session's deliverable and 14-question parking summary.
