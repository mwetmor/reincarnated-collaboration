# Dispatch — elrond Tier-1 clustering + element-coverage analysis (2026-05-16, queued)

**Status:** **PENDING-TRIGGER** — does NOT activate immediately. See "Activation trigger" section below.
**Target:** elrond (data steward; abstraction-analysis owner per `~/.claude/agents/elrond.md`)
**Branch:** main (collaboration repo)
**Tag intent:** No code tags — produces analytical reports + queryable summary tables in the catalogue DB.

## Context

Per Matt 2026-05-16, the catalogue work has three tiers of analytical depth:

- **Tier 1 (this dispatch)** — preliminary patterns surface once a small representative cross-vendor corpus accrues. Sanity-checks the rubric in production; produces first-pass groupings; identifies obvious coverage gaps.
- **Tier 2 (queued later)** — substantive clustering and element coverage; needs broader corpus (~1000+ assets, 5+ sources).
- **Tier 3 (much later)** — 2D-3D coherence validation; needs Unity Asset Store crawling AND substantial 2D corpus.

This dispatch covers Tier 1 only.

## Activation trigger

This dispatch is **queued**, not active. Knight-rider activates when both conditions are met:

1. **Catalogue asset volume threshold reached:** at least **~500 curated assets** in `catalogue.db` (or equivalent: clean rows across the rubric — not raw extraction count, but assets that passed Elrond's curation pipeline). The threshold is a heuristic — Elrond can argue for activation at a different count if data shape warrants it.
2. **Source diversity:** at least **3 different vendor sources** represented (Pimen + 2 others minimum). Single-source clustering reveals creator style, not cross-vendor patterns.

When both trigger, knight-rider invokes this dispatch (or surfaces to Matt for launch).

**Knight-rider tracks the trigger:** after each Legolas full-crawl curation completes, knight-rider checks catalogue volume + source count against the threshold. When both fire, this dispatch activates.

## Deliverables — three analytical outputs

### 1. Preliminary entity-type clustering report

`agentic_orchestration/research/curated/analysis/tier1-entity-clustering-<date>.md`

For the curated catalogue corpus, run clustering analyses (your choice of method — k-means on numeric axes, hierarchical clustering, manual taxonomic grouping, or combination) along candidate dimensions:

- Visual style (the six-axis rubric)
- Functional role (character / enemy / vfx / environment / ui — per Legolas Mode B `category` field)
- Element (when applicable — for assets that carry element-coding)
- Decomposition state (monolithic / decomposed / partial)
- Source / vendor patterns

**Output structure:**
- For each clustering attempt: method + dimensions used + emergent groupings discovered + groupings that DIDN'T emerge
- Hypothesis-level only (Tier 1 is preliminary; not for canonical lock)
- Explicit negative results (groupings tried that failed) per your `.md`'s methodology section
- Connect to doc 37 § 10.2 open #4 — note which preliminary groupings, if they stabilize through Tier 2, could resolve unit-of-embodiment-variation question

### 2. Element coverage table

`agentic_orchestration/research/curated/analysis/tier1-element-coverage-<date>.md`

A structured table answering: **for each element the engine could produce (canonical four + their seasonal variants per doc 37 § 6), how many catalogue assets exist to visually deliver it?**

**Computation approach:**

- **For canonical four (fire / water / earth / wind):** straightforward — assets with element-coding directly map.
- **For seasonal variants (vacuum / pressure / bioluminescence / decay / void / radiation / etc.):** join via cipher-mapping (each variant ciphers to one canonical, per doc 37 § 6 architecture). Aggregate variant coverage by walking expected variant-vocabulary against catalogue.
- **For combined / hybrid elements:** flag as second-order — Tier 1 doesn't need to resolve these; surfaces them for Tier 2.

**Output structure:**

| Element / variant | Canonical cipher | Asset count | Sources | Decomposition profile | Gap severity |
|---|---|---|---|---|---|
| (per row per element) | | | | | none / minor / major / severe |

Plus narrative section: which elements have abundant coverage, which are sparse, which are absent. Implications for seasonal generation viability — does the engine have visual budget for every cosmology it could generate? Where are the constraints?

### 3. Identified-gaps report + recommendations

`agentic_orchestration/research/curated/analysis/tier1-gaps-and-recommendations-<date>.md`

From the clustering + element-coverage outputs, surface:

- **Elements with sparse / no catalogue coverage** — candidates for either (a) targeted source-commissioning (Legolas crawls a specific vendor known to cover the gap); (b) seasonal-content fallback strategy (when seasonal vocabulary ciphers to a sparse element, engine degrades gracefully — visual fallback to canonical-element asset with palette modulation); (c) explicit elements removed from seasonal-generation pool because they're not deliverable.
- **Decomposition gaps** — character/enemy archetypes with high monolithic-atlas coverage but low decomposed-spritesheet coverage. Affects animation rigging.
- **Style-register edge cases** — assets the rubric flagged as `manual-review` or `borderline` quality; clustering surfaces whether these cluster meaningfully or are scattered noise.
- **Recommendations** for either Tier-2 deeper analysis OR Legolas additional targeted crawls to close gaps before Tier 2 fires.

## Cross-seam consumers

- **Gandalf** — Tier 1 outputs inform his design-track viability gate on subsequent samples AND inform his seasonal-anchor-prose work (which cosmologies are deliverable inform which anchors get prose authored). Surface findings to him via Pattern A subagent invocation OR direct dialogue (your call).
- **Rocket** — Tier 1 outputs eventually inform engine-side element-generation logic (when an element is generated, the engine can consult catalogue coverage to decide whether to degrade gracefully or generate a different element). NOT consumed in Tier 1; queued for when Tier 2 stabilizes findings.
- **Drax** — Tier 1 outputs eventually inform consumption-time filter behavior. NOT consumed in Tier 1.
- **Knight-rider** — receives Tier-1 outputs; decides whether to trigger Tier-2 dispatch OR queue targeted Legolas commissions to close gaps before Tier 2.

## Constraints

- **Tier 1 is preliminary, not canonical.** Findings are hypotheses to validate at Tier 2. Don't over-claim.
- **Time-bound target:** 4-6 hours of focused Elrond analytical work once trigger activates.
- **Read-only on engine telemetry / canonical / decisions-log** — this is data-side analysis. If findings imply design-decision changes, surface via knight-rider for canonical-doc revision; you don't author canonical changes.
- **Gandalf-direct dialogue is welcome** — if design-implication questions emerge during analysis, invoke gandalf via Pattern A subagent or schedule Pattern B. Same direct-dialogue privilege as the rubric-design dispatch.

## What this dispatch does NOT do

- **Tier 2 substantive clustering** — wait for broader corpus
- **2D-3D coherence validation** — wait for 3D crawl data
- **Engine integration** — that's a future rocket dispatch consuming these findings
- **Canonical lock on groupings** — Tier 1 is hypothesis-level

## Acceptance

- Three analytical reports filed at `research/curated/analysis/` (paths above)
- Catalogue DB has summary tables / views supporting the analyses (if Elrond's professional call says they help)
- Knight-rider notified with: report paths, headline findings, recommendation on Tier-2 timing, recommendation on whether to queue targeted Legolas commissions for gap-closure
- If gandalf-direct dialogue was invoked, summary in the dispatch completion record

## Required reading (at activation time)

- `~/.claude/agents/elrond.md` — your abstraction-analysis methodology section
- This dispatch in full
- `canonical/37-form-bias-diagnosis-and-recovery.md` § 6 (cipher architecture — informs element-variant cipher mapping) + § 10.2 open #4 (unit of embodiment variation — informs entity-clustering output)
- `canonical/story/style-register.md` + `canonical/story/enemy-visual-legibility.md` — design-side context
- `research/curated/catalogue-rubric-schema.md` + `research/curated/catalogue-schema.md` — Elrond's own schema work; the rubric values inform clustering dimensions
- Whatever curated catalogue corpus exists at activation time

## Completion record

Append to this file when complete: report paths, headline findings (3-5 bullet summary), Tier-2 timing recommendation, gap-closure recommendations, gandalf-dialogue summary if applicable.
