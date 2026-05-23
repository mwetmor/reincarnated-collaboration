# Dispatch — 2026-05-22 — legolas — Phase A substrate audit (cleaning-pipeline rubric application)

**From:** knight-rider
**To:** legolas (Mode B systematic extraction + Mode A analytical sampling — hybrid)
**Approved by:** Matt 2026-05-22 late-evening (path (a) accept + pivot; F1-F6 locked; cleaning-policy framework from gandalf locked)
**Estimated effort:** ~1 day Pattern-B preferred / Pattern-A acceptable with strict sequencing (see § Execution mode below)

**Execution mode** (jack-ryan Gate-1 amendment #4):
- **Pattern B preferred.** Substantive multi-deliverable work; LLM-judgment for ambiguous rows; cross-source duplicate detection; 30-60 variant clusters with 4-criteria analysis each. Real timeout risk for Pattern A in a single subagent call.
- **Pattern A acceptable** IF strict sequencing: complete Math note A + Deliverable 1 (per-source quality report) BEFORE Deliverable 2 (variant clusters) BEFORE Deliverable 3 (allowlist verification) BEFORE Deliverable 4 (cleanliness baseline). Each deliverable committed independently so partial completion still produces usable artifacts.
**Acceptance:** All 5 per-row classification dimensions populated for ~600-1,250 stratified samples; per-source quality reports authored; variant-cluster examples surfaced; named-unique allowlist verified + expanded; F1-F6 operational implications recorded; commit + tag

---

## Context

**Cycle 9 cleaning-phase status:**
- Hive-mind weapon-library-import at 89,839 clean knowledge entries / 24 sources (Matt: accept-at-89.8% + pivot to canonical normalization)
- 130K `wikipedia-unfiltered` quarantine dump-then-deleted 2026-05-22 evening (audit archive at `quarantine-archives/`)
- Gandalf delivered Phase B cleaning-policy design 2026-05-22 late-evening at `canonical/story/cleaning-policy-design-2026-05-22.md` — full taxonomies, math-anchored cleanliness bars, allowlists, per-source mappings, variant-collapse framework, Pattern-6 sequencing
- Matt locked F1-F6 (see § Matt-locked-decisions table below)

**Phase A audit is THIS dispatch.** Your job is to apply gandalf's classification framework to a stratified sample of the substrate, surface per-source quality reports, and surface variant-cluster examples for in-flight Matt+gandalf review. Phase D (elrond) extrapolates your rubric to the full 89K substrate later. Phase E (Pattern-6 axis discovery) waits for Phase D.

You are NOT classifying the full substrate. You are sampling N=20-50 per source × 24 sources = 600-1,250 rows, applying gandalf's classification rules, computing per-source FP/error rates, and surfacing edge cases.

## Required reading before starting

1. **`canonical/story/cleaning-policy-design-2026-05-22.md`** — gandalf's full framework; **read § 1.5 (weapon_kind detection rules), § 2.5 (wieldability edge cases), § 3.3 (named-unique allowlist), § 3.5 (Phase A audit deliverable for Item 3), § 5.2 (per-source cultural-lineage mapping), § 6.3 (variant-collapse decision criteria), § 6.5 (Phase A audit deliverable for Item 6)**
2. `agentic_orchestration/dispatches/2026-05-22-gandalf-cleaning-policy-design-review.md` — your upstream dispatch (gandalf's brief) — for context
3. `agentic_orchestration/weapon-library-import-hive-mind-state.md` — Cycle 9 live state
4. `agentic_orchestration/weapon-library-import-sample-rows-2026-05-22.md` — Matt's 3-row-per-source review doc; the concrete-examples reference
5. `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/findings-summary.md` — your prior discovery
6. `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/schema.sql` v1.1.0 — current DB schema

## Math-before-code

Yes. Required deliverables before classification starts:

### Math note A — sampling strategy

For each of the 24 source libraries, derive your sample size N_source via:
- N_source = min(50, max(20, ceil(source_row_count / 1000)))
- Override: if source_row_count < 20, sample ALL rows (census)
- Override: if source_row_count > 30,000 (Royal Armouries), stratify the N=50 sample across `weapon_subclass` if available + at least 5 rows from each variant-cluster signal you can detect by name-substring

Output: a math-note at `legolas/research/weapon-library-import-2026-05-22/phase-A-math-note.md` with the per-source N_source table BEFORE you fire classification.

### Math note B — confidence per classification

For each row classification (5 dimensions: `weapon_kind`, `wieldable_humanoid`, `cultural_lineage`, `historical_period`, `register`), record a confidence ∈ {1.0, 0.7, 0.5, 0.3} per the gandalf framework § 5.3:
- 1.0: explicit structured-tag match (e.g., wikidata Q-item P31 chain unambiguous)
- 0.7: description-regex match (e.g., wikipedia category strings)
- 0.5: source-library default (e.g., fextralife defaults to fantasy_generic)
- 0.3: fallback heuristic (LLM judgment with weak signal)

Per-source aggregate stats reported as mean + median confidence per dimension.

### Math note C — variance check (jack-ryan Gate-1 amendment #1)

If **ANY** source returns >0.3 stdev in classification confidence on `weapon_kind` (not just Royal Armouries), surface BEFORE finalizing the per-source report. This catches detection-confidence instability across all gandalf § 4.2-flagged FP-risk sources (pf2ools, gta-v-data, fextralife, souls-api) plus museum-as-category-default candidates (Royal Armouries, met-museum).

## Cross-seam contract change? (Principle 6 gate)

**No.** Phase A audit produces classification estimates + per-source reports + surfaced edge-case examples. No schema changes executed. No telemetry contract touched. Elrond authors actual schema migration in Phase D.

**Round-trip: not applicable — Phase A is an audit deliverable; no inter-seam contract changes.**

## Matt-locked decisions (F1-F6 + prior)

| ID | Decision | Locked value |
|---|---|---|
| Path | Accept at 89.8% + pivot to canonical normalization | LOCKED |
| Wikipedia v1 (130K) | Dump-then-delete | EXECUTED |
| Non-weapons + non-wieldable | Tag-and-keep via filter; never drop | LOCKED |
| `weapon_kind` taxonomy | **5-bucket** per gandalf § 1.3 (added `ammo_or_consumable`) | LOCKED |
| `wieldable_humanoid` enum | **6-bucket** per gandalf § 2.4 (added `shoulder_supported`) | LOCKED |
| Museum-as-category default | Categorical-representation unless named per § 3.2 detection signals | LOCKED |
| **F1: Royal Armouries within-source dedup-policy** | **TIERED collapse** — strict near-duplicates (same maker / period / culture / type / scale ±10%) → COLLAPSE-TO-PARENT; meaningfully-distinct museum holdings → preserved as variants | LOCKED |
| **F2: Cultural-lineage axis bias** | **Weighted (inverse-frequency)** for Phase E axis discovery — not stratified-sampling | LOCKED |
| **F3: pf2ools drift (688 rows mostly non-weapons)** | **Quarantine** — mirror the wikipedia-unfiltered pattern at smaller scale; preserve in archive; exclude from active | LOCKED |
| **F4: Fuzzy cross-source name-match for canonical merge** | **≥ 0.85 cosine + cross-source corroboration required** | LOCKED |
| **F5: Pattern-6 methodology** | **PCA-as-starting-method** (autoencoder/UMAP question deferred to Phase E pilot if needed) | LOCKED |
| **F6: Sample-pool size N for category sampling** | **N=20-50 default** (revisit if Phase E pilots show different needs) | LOCKED |

These all flow into your audit rubric. Apply them.

## Scope (5 classification dimensions per sample row + 4 deliverables)

### Per-row classification dimensions (apply gandalf's § 1.5 + § 2.5 + § 3.2 + § 5.2 + § 6.3 rules)

For each sampled row, classify on 5 dimensions:

#### Dim 1 — `weapon_kind` ∈ {`category` | `unique` | `named_template` | `ammo_or_consumable` | `unknown`}
- Apply gandalf § 1.5 detection rules per source-library
- For named-unique detection, apply gandalf § 3.5 patterns (24-entry allowlist + 6 regex patterns)
- Confidence per Math note B

#### Dim 2 — `wieldable_humanoid` ∈ {`one_hand` | `two_hand` | `shoulder_supported` | `either` | `no` | `mount_required` | `unknown`}
- Apply gandalf § 2.5 edge-case dispositions + § 2.6 per-source signal inventory
- Per Matt's rule: "single humanoid carries + fires/wields in active use"
- For `ammo_or_consumable` rows: set `wieldable_humanoid='unknown'` per § 2.5 footer (ammo isn't wielded; it's loaded)

#### Dim 3 — `cultural_lineage` ∈ {`european` | `east_asian` | `south_asian` | `southeast_asian` | `middle_eastern` | `african` | `north_american_indigenous` | `mesoamerican` | `south_american_indigenous` | `arctic_circumpolar` | `oceanic` | `fantasy_generic` | `sci_fi_generic` | `cross_cultural` | `unknown`}
- Apply gandalf § 5.2 per-source mapping rules
- For multi-lineage signal: assign primary; capture secondary in note

#### Dim 4 — `historical_period` ∈ {`pre_classical` | `classical` | `medieval` | `early_modern` | `industrial` | `modern` | `contemporary` | `fictional` | `unknown`}
- **Apply year bands per gandalf § 5.1 exactly** (jack-ryan Gate-1 amendment #3): `pre_classical`=pre-500-BCE / `classical`=500-BCE-to-500-CE / `medieval`=500-1500-CE / `early_modern`=1500-1800 / `industrial`=1800-1914 / `modern`=1914-1989 / `contemporary`=1989-present / `fictional`=ahistorical (in-genre / fantasy / sci-fi)
- Inference from raw period/date signals; fallback to source-library default
- Do NOT invent alternate cutoff dates — exact match to gandalf's year bands is required so Deliverable 4's cleanliness-bar comparison to gandalf's projections remains valid

#### Dim 5 — `register` ∈ {`historical` | `military_modern` | `fantasy` | `sci_fi` | `mythological` | `unknown`}
- Apply gandalf § 5.1 register definitions
- Default per source-library category (museums + wikidata/wikipedia → `historical` unless modern-military; TRPG/MMO/ARPG → `fantasy`; odin-army/army-recognition → `military_modern`; mythological per named-unique allowlist)

### Deliverable 1 — Per-source quality report (24 markdown files OR one consolidated)

For each source library, report:
- Sample size N_source (per Math note A)
- Per-dimension classification distribution (frequency table per bucket)
- Per-dimension confidence stats (mean, median, stdev)
- **Estimated per-source FP rate** for `weapon_kind=category` (what fraction of the sample is actually NOT a weapon in the wield-and-fight sense?)
- **Estimated per-source duplication rate** within the source (how often do you see what appears to be near-duplicates by name + structured_properties similarity?)
- **Surfaced edge cases** — rows that are unclassifiable (`unknown` after rule application + LLM judgment) — list with notes
- **F1 implication for this source** — if it's Royal Armouries, what fraction of the sample looks like it would collapse under TIERED policy? Estimate.

Output path: `legolas/research/weapon-library-import-2026-05-22/phase-A-audit/per-source-<source>.md` OR one consolidated `phase-A-audit/per-source-quality.md`.

### Deliverable 2 — Variant-cluster examples (for Item 6 in-flight Matt+gandalf decision)

Per gandalf § 6.5: surface 5-10 sample variant clusters per source library where the variant-collapse policy question applies. For each cluster:
- The variants present (list names + brief description)
- Mechanical signature variance per § 6.3 (1) — same range_class / geometry_class / tempo_class / charge_class? Or different?
- Cultural-narrative distinctness per § 6.3 (2) — culturally-named-and-recognized or academic typology?
- Substrate-density consequence per § 6.3 (3) — sparse or dense region?
- Your recommended policy (A / B / C / D) with one-sentence rationale

Output path: `legolas/research/weapon-library-import-2026-05-22/phase-A-audit/variant-clusters.md`

Target: 30-60 variant clusters total across all 24 sources, prioritizing high-yield candidates (Royal Armouries gladius variants; Met Museum katana/tachi/wakizashi/tantō; wikidata AK-47/AKM/AK-74; nick-aschenbach D&D weapon variants).

### Deliverable 3 — Named-unique allowlist verification + expansion

Per gandalf § 3.5: validate the 24 named-unique allowlist entries against the substrate. For each:
- Is it actually present? In which source(s)? At what `display_name` / `canonical_name`?
- If present, was your classification rule able to detect it as `weapon_kind=unique`? If not, why not?
- Are there OTHER named uniques in your sample that should be added to the allowlist? List them with source-attribution.

Target: confirm allowlist coverage + propose ≥5 additions if your sample surfaces them.

Output path: `legolas/research/weapon-library-import-2026-05-22/phase-A-audit/named-unique-verification.md`

### Deliverable 4 — Math-anchored cleanliness bar empirical baseline

Per gandalf § 4: he projected empirical baselines (e.g., "current FP ≈ 0.7%", "raw duplication ~47%"). Your audit refines those projections with actual sample data.

For each of the 4 thresholds in § 4 (FP rate / duplication / coverage / weapon_kind mis-classification):
- Empirical estimate from your sample
- Comparison to gandalf's projection
- Recommendation: does Phase D cleaning need to focus on this dimension, or is it already at/below target?

Output path: `legolas/research/weapon-library-import-2026-05-22/phase-A-audit/cleanliness-baseline.md`

## Acceptance criteria

- [ ] Math note A authored at `phase-A-math-note.md` BEFORE classification fires
- [ ] All 24 sources sampled at N=20-50 per gandalf framework + your math note A
- [ ] All 5 classification dimensions populated per sample row with confidence scores
- [ ] Per-source quality report authored (one consolidated OR 24 per-source files)
- [ ] Variant-cluster examples document authored (30-60 clusters surfaced)
- [ ] Named-unique allowlist verification document authored (24 entries verified + ≥5 additions if any)
- [ ] Math-anchored cleanliness bar empirical baseline document authored (4 thresholds × empirical estimate)
- [ ] **F1-F6 operational implications recorded** (jack-ryan Gate-1 amendment #2):
  - **F1 (Royal Armouries TIERED collapse):** per-source collapse-rate estimate — N rows in sample that would collapse to M canonicals under the TIERED rule; report M/N ratio
  - **F2 (Cultural-lineage axis bias):** confirm or challenge with `cultural_lineage` distribution stats from your sample
  - **F3 (pf2ools quarantine):** percentage of pf2ools sample classified as NOT a weapon (confirming "mostly non-weapons" assessment)
  - **F4 (fuzzy cross-source ≥0.85 + corroboration):** at least one concrete case from your sample (e.g., Wikidata-Aegis vs Wikipedia-aegis) showing the threshold would catch the merge
  - **F5 (PCA methodology):** no sample-data needed; note any signals that suggest non-linear axes (e.g., bimodal distributions) which would imply PCA is insufficient — purely advisory
  - **F6 (N=20-50 sample-pool size):** no sample-data needed; note any classification confidence patterns that suggest larger sample pool would help — purely advisory
- [ ] Round-trip: not applicable — audit deliverable, no contract change
- [ ] Tag: `legolas/phase-A-substrate-audit-2026-05-22`
- [ ] Append completion record to this dispatch file per `dispatches/README.md` convention

## Out of scope (explicit non-goals)

- **DO NOT** classify the full 89,839 substrate — that's Phase D (elrond)
- **DO NOT** modify the DB — Phase A is read-only audit; no INSERT/UPDATE/DELETE except temp tables you may create for your own analysis
- **DO NOT** make Matt-decisions on F1-F6 — those are LOCKED; apply them
- **DO NOT** decide variant-collapse policies per cluster — surface the clusters with recommendations; Matt + gandalf decide in-flight
- **DO NOT** execute Pattern-6 axis discovery (Phase E; later)
- **DO NOT** author schema migrations (elrond's seam)
- **DO NOT** modify gandalf's `canonical/story/cleaning-policy-design-2026-05-22.md` — you implement his framework, not amend it

## Open questions for you to resolve + document

These are decisions YOU make + record in your math note + per-source reports:

1. **Sampling stratification within a source.** For Royal Armouries (38K rows), should the N=50 sample be uniform random across the source, or stratified by `weapon_subclass` (if populated) or by name-prefix to ensure diverse coverage? Decide + document.
2. **LLM-judgment use.** When rules return `unknown`, when do you escalate to LLM-judgment classification? Pre-set a threshold (e.g., "after applying all rules; if still unknown AND row has descriptive text ≥50 chars; then LLM-judge"). Document your threshold.
3. **Cross-source duplicate detection in the sample.** Within your 1,250-row sample, can you detect cross-source duplicates of high-frequency canonicals (AK-47 / Gladius / Katana / Excalibur)? If yes, report — this informs Phase D's canonical-merge work.
4. **Tagging the pf2ools 688 rows for F3 quarantine.** Sample N=20-30 from pf2ools to confirm the "mostly non-weapons" assessment from sample-rows doc. Recommend quarantine slug (e.g., `source_library='pf2ools-quarantined'`).
5. **Wikidata `Aegis` vs Wikipedia `aegis` cross-source dup.** If your sample includes both, confirm gandalf's F4 fuzzy-merge threshold ≥0.85 + corroboration would catch it. If it wouldn't, surface as F4-refinement-needed.

6. **Source library with <5 queryable rows in active substrate** (jack-ryan Gate-1 amendment #5). If a source library has fewer than 5 active rows (notably pf2ools post-F3 quarantine if elrond's Phase D pre-fires that — Phase A may run before or after; clarify in your math note A) confirm: sampling the quarantine-archive (`legolas/research/.../quarantine-archives/`) for AUDIT-PURPOSES-ONLY is permitted (read-only; classifications recorded for archive completeness). Do NOT treat 0-active-row source as census-skipped without explicit acknowledgement in the per-source report.

## References

### Upstream design doc (LOAD-BEARING)
- `canonical/story/cleaning-policy-design-2026-05-22.md` — gandalf's full framework; read in full

### State + context
- `agentic_orchestration/weapon-library-import-hive-mind-state.md`
- `agentic_orchestration/weapon-library-import-wind-down-summary-2026-05-22.md`
- `agentic_orchestration/weapon-library-import-sample-rows-2026-05-22.md`

### Schema + prior research
- `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/schema.sql` v1.1.0
- `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/findings-summary.md`
- `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/quarantine-archives/README.md`

### Disciplines
- #1 math-before-code (math notes A/B/C before classification fires)
- #11 empirical inspection over assumption (sample + verify; don't trust gandalf's projection without empirical check)
- #19 right tool / smoke-test discipline (do you actually need LLM-judgment for every sample, or can rules + a small LLM-fallback do it?)

### Prior tags
- `knight-rider/cleaning-plan-design-locked-2026-05-22` — cycle 9 cleaning-plan + 130K cleanup
- `gandalf/cleaning-policy-design-review-2026-05-22` — gandalf's Phase B design

---

## Tag at completion

```
legolas/phase-A-substrate-audit-2026-05-22
```

(Seam-prefix per ADR-001; intermediate audit artifact; not Matt-milestone.)

## What happens after you return

Knight-rider:
1. Reads your 4 deliverables
2. Surfaces F1-F6 operational implications to Matt
3. Surfaces variant-cluster examples to Matt+gandalf for in-flight decision (Item 6 framework)
4. Coordinates the in-flight Matt+gandalf review pass (likely Pattern-A subagent for gandalf re-engagement)
5. Authors elrond Phase D Pattern-B dispatch with locked policies + Phase A empirical baselines operationalized
6. Optional: fires legolas Mode A dirty-probe (gandalf § 7.2 Step 1) as a sidecar — surfaces axes the cleaning pipeline must preserve

Phase E (Pattern-6 canonical axis discovery) waits for Phase D clean substrate.

---

**Signed:** knight-rider (dispatch authored 2026-05-22 late-evening; cleaning Phase A audit fires next)

---

## Completion record

**Completed:** 2026-05-22
**Executed by:** legolas (Pattern-A sub-agent in knight-rider session)
**Tags shipped:** `legolas/phase-A-substrate-audit-2026-05-22`

**Deliverables authored:**
- `phase-A-math-note.md` — Math note A (sampling strategy; N_source table; OQ1-6 resolutions; field coverage baseline; raw duplication baseline)
- `phase-A-audit/per-source-quality.md` — Deliverable 1 (all 24 sources; FP rates; Math note C alerts for 7 sources)
- `phase-A-audit/variant-clusters.md` — Deliverable 2 (38 variant clusters across 8 cluster groups)
- `phase-A-audit/named-unique-verification.md` — Deliverable 3 (24-entry allowlist: 16/24 confirmed; 10 proposed additions)
- `phase-A-audit/cleanliness-baseline.md` — Deliverable 4 (all 4 gates empirically measured vs gandalf projections)

**Round-trip:** not applicable — audit deliverable; no contract change.

**F1-F6 operational implications recorded:**
- F1 (Royal Armouries TIERED): M/N ratio ≈ 9.2% (38,127 rows → ~3,500 canonicals; 87.9% within-source raw duplication)
- F2 (Cultural-lineage axis bias): European ~43% of classified rows confirmed; weighted inverse-frequency decision validated
- F3 (pf2ools quarantine): 100% non-weapons confirmed (all 688 rows are Pathfinder 2e character backgrounds; "mostly non-weapons" understated)
- F4 (fuzzy cross-source ≥0.85): Aegis/Aegis wikidata+wikipedia = confirmed >0.90 cosine + corroboration; Battersea Shield + Excalibur 3-source cases also confirmed
- F5 (PCA): no evidence PCA is insufficient; discrete cluster structure expected; wieldability dimension flagged as potential non-linear monitor in Phase E
- F6 (N=20-50): confirmed; note that v_category_sample must exclude ammo_or_consumable/non-wieldable before pool draw

**Key findings for knight-rider to surface to Matt:**
1. Substrate FP rate is ~2.83% (above 1.5% target; Phase D cleaning necessary — not optional)
2. `ammo_or_consumable` boundary error is 17.5% (far above 1.0% ceiling); Royal Armouries armour/ammunition categories are the dominant driver (~10,951 rows)
3. `named_template` boundary error is ~11.4% (above 5.0% threshold); TRPG/MMO/ARPG routing is the largest classification task in Phase D
4. pf2ools is 100% character backgrounds — F3 quarantine confirmed and operationally ready
5. souls-api is 96.6% non-weapon game items — recommend separate quarantine or ammo_or_consumable tagging
6. Named-unique allowlist: 10 proposed additions including first east_asian (Ruyi Jingu Bang) and south_asian (Sudarshana Chakra, Gandiva) mythological uniques
7. Phase D priority order: (1) ammo_or_consumable tagging, (2) F1 RA dedup, (3) F3 quarantine, (4) named_template routing, (5) FP removal, (6) unique detection, (7) F4 cross-source merge

**Notes for gandalf/elrond:**
- Detection rule refinement required for false-positive risk: M982 Excalibur, Kimber Aegis, Tyrfing missile (modern weapons sharing names with legendary uniques)
- Ulfberht swords wikipedia article should be `category` (class article), not `unique`; individual museum specimens = `unique`
- Narsil wikipedia entry is a REDIRECT — Phase D should detect and remove
- Top 5 variant clusters for in-flight Matt+gandalf review: AK-47 family (WIKI-4), Met Museum katana/tachi/wakizashi/tantō (MET-1), Royal Armouries generic "Sword" 3,155 rows (RA-2), cross-source Katana (CS-1), soulslike Dagger (SOULS-1)

---

## Downstream — gandalf variant-cluster policy assignment (2026-05-23)

gandalf completed the in-flight Matt+gandalf variant-cluster review on 2026-05-23 (Pattern-A subagent). All 26 cluster IDs (38 discrete variant decisions) assigned policies per § 6.3 criteria.

**Output:** `canonical/story/variant-cluster-policy-assignments-2026-05-23.md`
**Tag:** `gandalf/variant-cluster-policy-2026-05-23` (annotated)

**Policy distribution (per cluster ID):** A=5, B=8, C=8, D=2, plus 3 hybrid "A-at-top + B-within" cases for multi-type clusters (RA-4, MET-1, CS-3). 5 clusters flagged for Matt review (WIKI-3 game-tier merge, SOULS-1 auto-merge cutoff, AOS-2 split decision, RA-2 grouping threshold, WIKI-2 OSRS Excalibur disposition).

**Phase D handoff to elrond:** ammo_or_consumable drain (RA-5 + MET-3 alone = ~3,800 rows leaving active substrate) is priority 1. F1 RA TIERED collapse per RA-1/RA-3/RA-4. F4 confirmed merges for WIKI-1, WIKI-2, SOULS-2, WIKI-3 game-tier. Complex Policy-C routing (RA-2, WIKI-4, CS-1, CS-2) needs the three-lane historical/game-category/named_template router and caliber-bucket logic.
