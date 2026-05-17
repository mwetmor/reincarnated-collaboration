# Dispatch — 2026-05-16 — elrond — Emergent-grouping analysis at full substrate width (cipher-width sub-lock resolution)

**From:** knight-rider (authored per Matt's 2026-05-16 Day 4 directive post-Step-B completion; the natural next-up dispatch in the form-bias cipher-width resolution chain)
**To:** elrond
**Approved by:** Matt at 2026-05-16 Day 4 (per gandalf commission's post-Step-B framing: "Cross-vendor synthesis (post-crawl): Elrond consumes the JSONL files + summary findings to run the emergent-grouping analysis at full substrate width. Cipher-width sub-lock resolves on that analysis's output.")
**Status:** PENDING — ACTIVE
**Estimated effort:** 1-2 sessions (~3-6 hours total); analysis + recommendation. NOT a fast pass — coherence-eval at 200-400-pack scale plus methodology-extension comparison plus the multiple flag-adjudications takes deliberate time.
**Acceptance:** Findings document at `agentic_orchestration/qa/findings/2026-05-16-elrond-emergent-grouping-analysis.md` resolving the cipher-width sub-lock per Entry 2's framework (3-5 robust groupings / 1-2 groupings / no grouping survives); recommendations on Foundation-layer L1/L2 placement + per-season vocabulary coupling policy + D1 reconsideration scope; explicit adjudications on the 4 Step-B-surfaced flags. **Output drives knight-rider's downstream cipher-width decisions-log entry authoring task** (which itself routes through jack-ryan Gate 1 + Matt approval + commit before the resolution is durable).

---

## Context — why this dispatch exists

This is the **culminating analysis dispatch** in the catalogue-track work chain that has run today (2026-05-16 Day 4):

```
Elrond pre-inventory (COMPLETE) ─┐
Elrond Step A methodology validation (GREEN-LIGHT) ─┤
Legolas Step B Tier-1 crawl (COMPLETE: 54 packs, 28 substrate rows, 17 novel tags) ─┤
Gandalf gate-3 review (PASS-WITH-AMENDMENTS; Q-PRI-2 amendment-trigger conditions) ─┘
                                ↓
                    THIS DISPATCH (emergent-grouping analysis at full width)
                                ↓
                    Cipher-width sub-lock resolution → knight-rider drafts decisions-log entry → jack-ryan Gate 1 → Matt approval → commit
```

**Three of the four form-bias catalogue-track sub-locks per Entry 3 of the 5-entry batch (`5d51b5a`) resolve on THIS dispatch's output:**

1. **Cipher-width sub-lock** — Options A / B / C per Entry 2's framework outcomes
2. **Foundation-layer placement (Flag B)** — L1 vs L2 ownership; resolves jointly with cipher-width
3. **Per-season vocabulary coupling policy (α / β / γ)** — α validation-and-regenerate / β in-prompt constraint / γ runtime fallback

The fourth sub-lock (D1 element-name pool reconsideration) requires Flag A rubric-screening test which is a separate small commission. This dispatch SCOPES the D1 reconsideration (per Flag A test outcome dependency) but does not resolve it.

## Strategic-axis context (load-bearing)

Per the form-bias 5-entry batch (committed `5d51b5a`) + the cadence Option II lock:

- **Sub-lock (a) ARPG-canon-primary at substrate-mechanical layer** — the cipher-width resolution must be ARPG-canon-compatible (Western ARPG audience reads the substrate as legible per `2026-05-16-arpg-design-discourse.md` Legolas Pass 4 evidence). Substrate widths >7 active per season violate the working-combat-memory ceiling.
- **Sub-lock (b) Isekai-canon-primary at narrative-skin and convergence layers** — the per-season-vocabulary layer (post-cipher-migration) handles isekai-flexibility independent of substrate width. The grouping layer (per Entry 2's three-layer model) absorbs the bandwidth tension.
- **Three-layer model (Entry 2):** substrate (you analyze) / grouping (per-season selection) / vocabulary (per-season LLM names). Cipher-width determines substrate width; grouping-viability determines per-season grouping count; vocabulary is independent.

**Three outcome possibilities per Entry 2's framework (all compatible with the strategic-axis lock):**

1. **3-5 robust groupings emerge** passing all viability filters → multiple-groupings architecture viable; seasonal rotation gains cross-season grouping variance as a structural pillar
2. **1-2 groupings survive** → refined-Option-A collapses to a single fixed grouping; the cipher becomes a single 4-5-tag opposition structure derived from the substrate; cross-season variety is in vocabulary + anchor, not in grouping
3. **No grouping survives** → the canonical-four cipher remains operative; catalogue-curation translation handles substrate-to-VFX mapping at visualization; doc 37 § 6 cipher is unchanged

The analysis output names which of the three outcomes lands. **You don't pick the outcome; you discover it from the data.**

## What this dispatch produces

A single findings document at `agentic_orchestration/qa/findings/2026-05-16-elrond-emergent-grouping-analysis.md`. Structure:

### Section 1 — Input substrate snapshot

Aggregate the substrate-evidence supply Step B produced:

- 9 per-vendor JSONL files at `research/catalogue/<vendor-slug>/full-2026-05-16.jsonl` (total ~54 packs)
- Pimen baseline at `research/catalogue/pimen/full-2026-05-16.jsonl` (47 packs)
- Cross-vendor substrate inventory at `research/catalogue/cross-vendor-substrate-inventory-2026-05-16.jsonl` (28 substrate rows)
- **Total: ~200-400 pack-rows across ~28 substrate-tag candidates** (the actual count emerges from your aggregation)

Confirm: total pack count; per-substrate-tag pack distribution; per-vendor contribution; novel-vs-baseline substrate-tag split (17 novel per Step B).

### Section 2 — Methodology execution (two passes per gandalf gate-3 amendment-trigger)

**Pass 1 — Step A methodology AS-LOCKED.**

Apply elrond's Step A methodology unchanged (7-mechanic-family collapse + Gower-style composite distance Jaccard 0.6 content + Hamming 0.4 form + hierarchical agglomerative average-linkage). Use the validated script at `agentic_orchestration/research/scripts/step_a_methodology_smoke_test_2026_05_16.py` as the methodology anchor (adapt for full-width input).

Produce:
- Cluster assignments per pack
- Cluster centroids / characterizations
- Coherence metrics (silhouette + per-cluster purity against the four hand-labels: element / mechanic / register / category)
- Stability check (ARI across w_content weighting band; per Step A validation)
- Failure-mode checks (singleton-rate; dominant-cluster-share)

**Pass 2 — Step A methodology EXTENDED per gandalf Q-PRI-2 amendment-trigger conditions.**

Apply the methodology with gandalf's three amendments:
1. **Extend to ~10 families:** add `movement-displacement`, `reactive-defensive`, `cast-prep-sustained` to the mechanic-family vocabulary
2. **Split aura-vs-instant within buff-debuff-status** if Frostwindz class-archetype evidence supports (Frostwindz Buff/Debuff Pack 09 was flagged as a register outlier by elrond's pre-inventory; Step B surfaced Frostwindz class-archetype packs with sustained-aura mechanics — evaluate)
3. **Require vendor-namespaced mechanic-tag preservation** (per Step B amendment C.1) — the `vendor_mechanic_tags` field added per pack survives the family-collapse and contributes substrate-distinct signal

Re-produce all the Pass 1 outputs against the extended methodology.

**Compare Pass 1 vs Pass 2:**
- Do clusters differ meaningfully? If yes — which methodology produces more coherent groupings at the cipher-width-framework gates (viability criteria below)?
- Stability across the two passes — does the same outcome possibility (1/2/3 per framework) land regardless of methodology choice?

### Section 3 — Cipher-width framework gates (per Entry 2 of the form-bias batch)

For each emerging cluster (Pass 1 + Pass 2), evaluate against the four viability criteria from strategy doc § 6.2:

| Criterion | What it checks | Pass / Fail per cluster |
|---|---|---|
| **Mechanical-distinctness** | 4-5 substrate tags whose mechanical signatures distinguish in combat | (your assessment per cluster) |
| **Role-orientation coverage** | The cluster admits damage / control / hybrid orientations against the active tags | (your assessment per cluster) |
| **Thematic coherence** | The cluster's anchor + cosmology admits the grouping as natural; doesn't feel arbitrary | (your assessment per cluster) |
| **Genre-recognition** | Western ARPG audience reads the cluster as legible (per Pass 4 ARPG-community discourse evidence) | (your assessment per cluster) |

A "robust grouping" passes ALL FOUR criteria. Count robust groupings; the count drives the outcome:
- **3-5 robust groupings → Outcome 1** (multi-grouping architecture)
- **1-2 robust groupings → Outcome 2** (refined-Option-A)
- **0 robust groupings → Outcome 3** (canonical-four cipher remains operative)

**Name the outcome explicitly** in this section. The cipher-width sub-lock resolves on this naming.

### Section 4 — Foundation-layer L1/L2 recommendation (Flag B)

Per Entry 2 of the form-bias batch + strategy doc § 6.2 item 5:

> Foundation layer placement (Flag B) resolves jointly with cipher-width. If the substrate is Pimen-derived (9 tags), Foundation either grows to 9 (Foundation-coupled-to-substrate; engine treats substrate as L1) or decouples (substrate becomes L2 Reincarnated-cosmology concept; Foundation stays at 4-rotating-plus-1-physical as L1 generic).

Given the cipher-width outcome from Section 3, recommend:

- **L1 (Foundation-coupled-to-substrate):** Foundation grows to N substrate tags (where N = the outcome's substrate width). Pros: substrate IS the engine; clean. Cons: bigger Foundation 4+1 validator change; substrate-vendor-pivot becomes a Foundation-touching change.
- **L2 (Substrate decoupled to Reincarnated-cosmology):** Foundation stays at 4-rotating-plus-1-physical as L1 generic; substrate is L2 Reincarnated-specific. Pros: substrate-pivot is L2-only; Foundation stays stable. Cons: extra layer of indirection; some over-engineering if substrate is locked anyway.

Recommend with reasoning. Knight-rider's downstream decisions-log entry locks the L1/L2 choice.

### Section 5 — Per-season vocabulary coupling policy recommendation (α / β / γ)

Per Entry 3 of the form-bias batch:

- **(α) validation-and-regenerate** — engine validates LLM-generated per-season vocabulary against substrate; regenerates if mismatch
- **(β) in-prompt constraint** — engine constrains LLM prompts so per-season vocabulary maps cleanly to substrate at generation time
- **(γ) runtime fallback** — engine permits LLM-generated vocabulary as-is; falls back to substrate-mapping at runtime if mismatch

Given the cipher-width outcome (especially the substrate width + grouping count), which policy is operationally sensible? Considerations:
- Substrate width affects how often LLM is likely to produce vocabulary that maps cleanly
- Grouping count affects whether "per-season vocabulary" means per-grouping or per-season-overall
- Operational cost: α has highest cost (regeneration loops); γ has lowest cost (post-hoc resolution) but worst predictability; β is middle (one-time-prompt-engineering cost)

Recommend a policy with reasoning. Knight-rider's downstream decisions-log entry locks the policy.

### Section 6 — D1 reconsideration scope recommendation (Flag A dependency)

The D1 element-name pool reconsideration is the fourth sub-lock per Entry 3. It depends on Flag A test outcome (D1 rubric humanoid-fantasy screening) which is a separate small commission NOT triggered by this dispatch.

In Section 6, **scope the reconsideration conditional on Flag A outcome:**

- **If Flag A confirms (rubric reliably under-scores non-humanoid-cosmology candidates):** D1 reconsideration is structural rebuild — the rubric itself needs re-architecture; pool may not survive as-is.
- **If Flag A negates (rubric scores them as expected):** D1 reconsideration is bounded — entry-by-entry review against the cipher-width-determined substrate.

Knight-rider commissions the Flag A test as a separate small dispatch after your analysis lands (so the test framing benefits from your substrate width + grouping count context).

### Section 7 — Adjudications on Step-B-surfaced flags

Four flags from Step B + Step B amendments need YOUR adjudication during the emergent-grouping analysis:

1. **🔴 Pixogen license unverified** — Pass-2 substrate evidence includes Pixogen's Void + Technology substrates. **Recommendation:** include or exclude from cipher-width determination? Knight-rider's strong-default is EXCLUDE pending Matt-authorization for license verification — but if the cipher-width outcome is sensitive to Pixogen's substrate evidence specifically, surface that sensitivity in your analysis (don't pre-decide; report the dependency).
2. **🟡 Blood split-vs-merge** (CodeManu physical-injury/wound vs Frostwindz sanguine-magic/life-drain) — your clustering analysis should evaluate whether these merge or split naturally in the emergent groupings. Report the cluster behavior; recommend split or merge based on coherence.
3. **🟡 Acid vs Poison adjacency** (Pimen Acid = chemical-corrosive vs vendors' Poison = biological-venom) — same: report cluster behavior; recommend.
4. **🟡 CraftPix vector-format inclusion** (2 packs are vector; not pixel-art register) — Pass-1 + Pass-2 should include OR exclude vendor-vector-packs explicitly; report which choice you made and the impact on the cluster shape.

Each adjudication is a small recommendation with cluster-evidence backing.

### Section 8 — Recommendation summary for knight-rider

A concise (1-page) summary capturing:
- Cipher-width sub-lock outcome (named per framework)
- Foundation-layer recommendation (L1 vs L2)
- Per-season vocabulary coupling recommendation (α / β / γ)
- D1 reconsideration scope (conditional per Flag A)
- 4 flag adjudications
- Any other recommendations surfaced (especially: gandalf amendment-trigger conditions per gate-3 — did the extended methodology produce different results that warrant downstream methodology-extension commitment?)

This summary is what knight-rider drafts the cipher-width decisions-log entry against.

## Cross-seam considerations

- **Legolas:** READ-ONLY consumer of legolas's per-vendor JSONLs + cross-vendor substrate inventory. If you find a cataloguing gap (e.g., a vendor JSONL is missing a substrate signal you'd expect), surface as a finding; do NOT modify legolas's outputs.
- **Gandalf:** primary downstream design-instinct reviewer of the cipher-width outcome. Your output's Section 8 summary is what gandalf reviews before knight-rider's decisions-log entry drafting. Per gate-3 amendment-trigger context, gandalf may surface methodology-extension questions or thematic-coherence judgments that your data-side analysis doesn't capture alone.
- **Knight-rider:** notify at completion. Drafts the cipher-width decisions-log entry to qa/pending; routes through jack-ryan Gate 1; Matt approval + commit.
- **Jack-ryan:** future Gate 1 reviewer of the cipher-width decisions-log entry (separate dispatch; not this one).
- **Star-lord:** out of seam for this dispatch. Star-lord's catalogue-mapping experiment is separately-dispatched and feeds related downstream work but doesn't gate this dispatch.
- **Rocket + drax:** out of seam. Downstream consumers of the cipher-width outcome (rocket: schema-side; drax: display-side) but not at this dispatch's authoring time.

## Tag policy

No tag (analysis-only; no code changes).

## Required reading

Primary inputs (your data):
- `agentic_orchestration/research/catalogue/cross-vendor-substrate-inventory-2026-05-16.jsonl` (28 substrate rows; primary input)
- `agentic_orchestration/research/catalogue/<vendor>/full-2026-05-16.jsonl` for all 9 vendors (per-pack rows; secondary input)
- `agentic_orchestration/research/catalogue/pimen/full-2026-05-16.jsonl` (47 Pimen packs; baseline)
- `agentic_orchestration/research/curated/pimen-catalogue-curated-2026-05-16.jsonl` (47 curated Pimen rows; the curation-pass output that Step A methodology was validated against)

Methodology + framework:
- `agentic_orchestration/research/scripts/step_a_methodology_smoke_test_2026_05_16.py` (your methodology script; adapt for full-width input)
- `agentic_orchestration/qa/findings/2026-05-16-elrond-step-a-methodology-smoke-test.md` (your Step A findings; methodology validation + GREEN-LIGHT verdict)
- `agentic_orchestration/research/curated/catalogue-structural-pre-inventory-2026-05-16.md` (your pre-inventory; the 14 parked questions including Q-PRI-2 + Q-SHAPE-1)
- `agentic_orchestration/qa/findings/2026-05-16-gandalf-step-b-gate3-review.md` (gandalf's amendment-trigger conditions for Q-PRI-2)
- `canonical/story/form-bias-cadence-strategy.md` § 5.3 + § 6.1 + § 6.2 (cipher-width framework + three-layer model + four sub-locks)

Decisions-log context:
- `reincarnated-engine/design/decisions/decisions-log.md` 2026-05-16 form-bias 5-entry batch (committed `5d51b5a`) — Entry 2 cipher-width framework + Entry 3 sub-locks deferred
- 2026-05-16 ailment-deferral entry (committed `680a3f1`) — companion empirical-resolution pattern

ARPG-genre evidence (for genre-recognition criterion):
- `agentic_orchestration/research/knowledge/arpg-community/2026-05-16-arpg-design-discourse.md` (Pass 4 substrate evidence)
- `agentic_orchestration/research/knowledge/arpg-adjacent/2026-05-16-adjacent-arpgs.md`
- `agentic_orchestration/research/knowledge/poe/2026-05-16-poe-design-philosophy.md`
- `agentic_orchestration/research/knowledge/diablo/2026-05-16-diablo-design-retrospectives.md`

## Acceptance criteria

- [ ] All 8 sections complete in findings file
- [ ] Pass 1 (Step A methodology as-locked) executed; metrics reported
- [ ] Pass 2 (extended per gandalf Q-PRI-2 amendments) executed; metrics reported; Pass 1 vs Pass 2 compared
- [ ] Cluster viability assessed against all 4 framework criteria (mechanical-distinctness / role-orientation / thematic-coherence / genre-recognition)
- [ ] Cipher-width sub-lock outcome NAMED (Outcome 1 / 2 / 3 per Entry 2 framework)
- [ ] Foundation-layer L1/L2 recommendation with reasoning
- [ ] Per-season vocabulary coupling policy recommendation (α / β / γ) with reasoning
- [ ] D1 reconsideration scope recommendation conditional on Flag A
- [ ] 4 flag adjudications (Pixogen / blood / acid-poison / CraftPix vector) with cluster-evidence backing
- [ ] Section 8 summary captures all recommendations in 1-page form
- [ ] Findings filed at `agentic_orchestration/qa/findings/2026-05-16-elrond-emergent-grouping-analysis.md`
- [ ] Knight-rider notified at completion with the cipher-width outcome + recommendation summary

## Out of scope (explicit)

- **NO Flag A test execution.** That's a separate small commission knight-rider authors AFTER your analysis lands; the framing benefits from your substrate-width context.
- **NO decisions-log entry authoring.** Knight-rider drafts the cipher-width entry to qa/pending based on your findings; you don't write the entry.
- **NO Pixogen license verification.** Matt-decision per ADR-006 territory. Your adjudication is "include or exclude from analysis"; the license verification itself is separate.
- **NO recommendations beyond the four sub-locks (cipher-width / Foundation / vocabulary coupling / D1 scope) + the four flag adjudications.** Stay scoped.
- **NO catalogue-side curation changes.** Read-only on legolas's outputs.
- **NO methodology-script-formalization commits.** If you extend the script for Pass 2, file the extension as a follow-on artifact but don't commit to engine repo without separate dispatch.

## Open questions for elrond to resolve in the analysis

These are likely to surface; capture explicitly in Section 5/6/7 or Section 8 summary:

1. **Does the 17-novel-tag substrate enrichment from Step B actually produce robust groupings, or does it produce a "long tail" of singleton-clusters that don't survive viability filters?** This is the central empirical question; the outcome possibility (1/2/3) hinges on it.
2. **Does the gandalf-amendment methodology extension (10-family + aura-vs-instant split + vendor-namespaced mechanic-tags) produce meaningfully different cluster shapes vs the as-locked 7-family methodology?** If yes, the extended methodology may need to lock as the post-Step-B operative methodology (knight-rider would draft a separate decisions-log entry codifying the methodology lock).
3. **Pixogen exclude-vs-include sensitivity** — if the cipher-width outcome differs based on Pixogen inclusion, Matt's license-verification decision becomes load-bearing for the cipher-width lock itself.
4. **Frostwindz class-archetype packs (Deathbringer / Blood Knight / Warlock / Rogue / Paladin)** — these are class-archetype-shaped rather than substrate-shaped; do they integrate cleanly with the emergent groupings, or do they cluster as a separate "class-archetype" sub-cluster? May surface a methodology refinement opportunity.

---

## Completion record

(To be filled in by elrond on completion)

**Completed:**
**Findings path:**
**Total packs analyzed:**
**Substrate-tag count post-aggregation:**
**Cipher-width outcome (1/2/3):**
**Foundation-layer recommendation (L1/L2):**
**Per-season vocabulary coupling recommendation (α/β/γ):**
**D1 reconsideration scope recommendation:**
**Pass 1 vs Pass 2 outcome consistency:**
**Flag adjudications summary:**
**Notes for knight-rider:**
