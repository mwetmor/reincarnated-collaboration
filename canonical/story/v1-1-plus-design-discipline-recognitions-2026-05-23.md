# v1.1+ Design-Discipline Recognitions — 2026-05-23

> **STATUS:** CURRENT — recognition record capturing three forward-looking design-discipline recognitions surfaced at session-end. Architectural commitments deferred per § 4 empirical-evidence criteria. All three move to v1.1+ post-ship substrate-and-design-discipline-refinement queue alongside 9.11-C/D/E + 9.10-E (per 02-roadmap.md § 1.0 v1.1+ deferred queue).

**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-05-23 — direct invocation ("flag for later")
**Status:** Recognition Record — architectural commitments deferred per § 4
**Companion docs:**
- `canonical/00-ground-state.md` § 1 (current-truth oracle)
- `canonical/02-roadmap.md` § 1.0 v1.1+ deferred substrate-refinement queue
- `canonical/37-engine-and-game-two-products.md` (Variant C lock — engine vs game as two products)
- `canonical/38-downstream-delivery-strategy-2026-05-23.md` § 7 (D7 AI-tell discipline)
- `canonical/story/marginal-lineage-tagging-pattern-2026-05-23.md` (4-mode tagging-vocabulary collapse pattern)
- `agentic_orchestration/gandalf/notes/2026-05-23-geography-vs-culture-substrate-analysis.html` (empirical substrate analysis with charts)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (Discipline #25 semantic-layer rep-audit)

---

## 0. TL;DR

Three forward-looking design-discipline recognitions surfaced at session-end 2026-05-23. None gate v1 ship; all affect v1.1+ substrate-refinement + design-discipline work AND downstream consumer surfaces. Captured as recognition record so they're not lost between sessions:

1. **Sampling-proportionality flagging** — per design surface; explicit declaration of sampling policy at design-spec-as-math time
2. **Country-title name cleanup** — substrate-curation; remove geographic-encoding from canonical_name strings
3. **Commercial-vs-solo output differentiation** — per output stream; metadata flag distinguishing player-ship vs Matt-solo-development vs engine-internal-validation purposes

Each recognition is load-bearing for v1.1+ work AND for design discipline going forward. None requires immediate v1 action.

---

## 1. Recognition 1 — Sampling-proportionality flagging per design surface

### 1.1 The recognition

The substrate's row distribution is wildly uneven (european ~27K rows vs north_american_indigenous ~32 rows; 1000:1 ratio). Per the marginal-lineage meta-record + geography-vs-culture substrate analysis, this distribution reflects substrate-acquisition crawl bias + 4-mode tagging-vocabulary collapse. Any downstream design surface that samples the substrate MUST specify its sampling policy explicitly. Currently the policy is IMPLICIT (whatever the consumer happens to do); it should be EXPLICIT (named design parameter per surface).

### 1.2 Surfaces requiring explicit sampling-proportionality flag

| Surface | Sampling decision | Default if implicit |
|---|---|---|
| T4-B v1 catalogue substrate-anchoring | Which clusters anchor T4 entries; per-cluster representative samples | european + east_asian dominate; marginal lineages absent (scaffolding § 4 Q1 already accepts this) |
| Cohesion-judge LLM-naming (P5) | Per-cluster reps fed to judge for naming | Top-N reps by hdbscan-native density; biases to dominant clusters |
| D10 Path C faction architecture | Per-faction emergence weighting | Substrate-dominant lineages produce 3+ factions; marginal lineages produce zero |
| Spirit-form generation (player surface) | Per-summon sampling distribution | Biased to dominant lineages unless specified |
| Player-facing cluster discovery | Which clusters players encounter | Substrate-coverage-weighted by default |

### 1.3 Sampling policies worth naming canonically

- **Uniform-row** — each substrate row equal weight (favors dominant lineages by ~1000x)
- **Lineage-balanced** — equal per-lineage weight (gives marginal lineages equal voice; risks empty cells)
- **Capacity-weighted** — weight reflects substrate coverage quality (per-lineage floor + ceiling)
- **Custom-weighted** — design call sets specific weights per surface
- **Explicit-exclusion** — list which lineages are out of v1 scope (scaffolding § 4 Q1 default lean implicitly does this)

### 1.4 Discipline-candidate framing

Every design surface that samples substrate must declare its sampling-proportionality policy at design-spec-as-math time. Composes with Discipline #25 semantic-layer rep-audit family: "the sampling policy IS a design parameter; declare it; rep-audit applies at the chosen policy."

Candidate for future Discipline #26 OR sub-discipline amendment to #25. Jack-ryan canonical-write territory when v1.1+ design-discipline work fires.

---

## 2. Recognition 2 — Country-title name cleanup at substrate-curation

### 2.1 The recognition

The substrate has captured weapon names that encode country-titles in canonical_name strings. These country-titles are a parallel mode of the 4-mode tagging-vocabulary collapse pattern (per marginal-lineage meta-record § 1.1) — geographic-encoding-in-name, not cultural-encoding-in-name. Examples:

- `2S1 Gvozdika Russian 122mm Amphibious Self-Propelled Howitzer (SPH)`
- `AN-74 (Coaler-B) Ukrainian Transport/Passenger Aircraft`
- `Bv 206 Swedish Articulated All-Terrain Tracked Carrier`
- `Mendoza HM-3` (Mexican; implicit; brand-encodes country)
- `Knight's Armament Company PDW` (US; implicit; brand-encodes country)

**The pattern:** modern-military-equipment names typically encode `[official-designation] [country-adjective] [functional-descriptor]`. The country-adjective in the NAME is geographic-encoding-in-name parallel to Mode B at the tag level.

### 2.2 Operational consequences

- LLM cohesion-judge consuming these names inherits the country-encoding into generated narrative
- Player-facing surfaces displaying these names leak "Russian Self-Propelled Howitzer" framings into spirit-form identity
- T4-B catalogue rep-audit relying on names biases the rep-audit toward modern-military reading
- Re-clustering pass would re-find the same clusters because the name-tokens carry the country signal even if lineage tags are re-tagged

### 2.3 Cleanup options

| Option | Description | Trade-off |
|---|---|---|
| Parse-and-separate | Add `country_of_manufacture` field; strip from canonical_name; original preserved as `source_canonical_name` | Schema change; substantial curation; lossless |
| Flag-only | Add `country_prefix_present` flag without changing names | Lighter; preserves names; downstream filters via flag |
| LLM-curated cleanup | LLM-curated pass to identify + strip country-prefixes | Substrate-curation discipline; elrond + LLM-call territory |

Elrond + jack-ryan v1.1+ work. Composes with 9.11-D/E substrate-tagging cleanup queue.

---

## 3. Recognition 3 — Commercial-vs-solo output differentiation per output stream

### 3.1 The recognition

The engine (Variant C — engine as general serial-content product per canonical/37) produces outputs that serve different purposes:

- **Commercial-ship outputs** — content shipped in Reincarnated (or other commercial products); player-facing; needs full polish, D7 AI-tell discipline, curation
- **Solo-work outputs** — Matt's solo development workflow; engine validation; tooling; one-off content for iteration; less polished; doesn't need full D7
- **Engine-internal-validation outputs** — sim test runs; balance loop outputs; BDI hypothesis test outputs; not player-facing; minimal curation
- **Marketing/pitch outputs** — commercial-positioning materials; demo content; different curation discipline than player-facing
- **Future commercial products** — Profile B B2B SaaS contexts (per gear-heavy promotion); Profile C/D/etc. as Variant C expands

Each output stream has different discipline requirements:

| Stream | D7 AI-tell strictness | Curation overhead | Sampling-proportionality policy | Rep-audit overhead |
|---|---|---|---|---|
| commercial_ship_player_facing | STRICT (no raw LLM) | High | Lineage-balanced or capacity-weighted | Mandatory per #25 |
| solo_work_dev | Loose | Low | Whatever serves iteration | Optional |
| engine_internal_validation | N/A (not human-consumed) | None | Sim-distribution-appropriate | N/A |
| marketing_pitch | STRICT (different curation; performative) | High | Performative; specific |
| Profile B B2B SaaS (future) | TBD per profile | TBD | TBD | TBD per profile |

### 3.2 The discipline gap currently

The engine currently does NOT carry explicit `output_purpose` metadata on its generated outputs. Every output is implicitly "for whatever's calling the engine" — whether that's Matt's dev iteration, sim validation, T4-B catalogue authoring, or future player-facing surfaces.

This is operationally fine while there's only one engine consumer (Matt's dev workflow). It becomes load-bearing when:
- Player-facing surfaces start consuming engine outputs (post-v1-ship)
- Multiple commercial products consume the same engine (Variant C expansion)
- Engine outputs are mixed across streams (e.g., dev-iteration outputs accidentally land in commercial-ship surfaces)

### 3.3 Implication for engine architecture

Future engine work should add `output_purpose` field to generation outputs. Possible field values:

```
output_purpose ∈ {
  commercial_ship_player_facing,      // Reincarnated player surfaces
  solo_work_dev,                       // Matt's dev workflow
  engine_internal_validation,          // sim test / balance loop / BDI tests
  marketing_pitch,                     // commercial-positioning materials
  cohesion_judge_calibration,          // P5 training data
  cluster_rep_audit,                   // substrate-tagging discipline work
  profile_b_saas (future)              // Variant C commercial expansion
  // extensible per future profiles
}
```

Composes with Variant C — engine knows what profile it's serving; outputs carry the purpose tag.

### 3.4 Cross-references to existing canon

- **Variant C** (`canonical/37-engine-and-game-two-products.md` + `canonical/story/engine-as-general-serial-content-product-2026-05-22.md`) — engine as general product serving multiple consumers; output differentiation flag composes with this architecture
- **D7 AI-tell discipline** (`canonical/38-downstream-delivery-strategy-2026-05-23.md` § 7) — strictness varies per output stream; flag determines which strictness applies
- **Gear-heavy promotion Profile B** (`canonical/story/gear-heavy-promotion-2026-05-22.md`) — Profile B B2B SaaS is a future commercial product that consumes engine; output_purpose tag is how engine distinguishes Profile B from Reincarnated

---

## 4. Empirical-evidence criteria for re-engagement (architectural commitment gates)

Per gandalf OP § 3.4 recognition-validate-commit cycle:

### 4.1 Recognition (this doc)

All three recognitions captured at session-end 2026-05-23.

### 4.2 Validate before architectural commitment

| Recognition | Validation criterion |
|---|---|
| 1. Sampling-proportionality flagging | T4-B v1 catalogue design call surfaces first explicit sampling-policy declaration; empirically validates whether the discipline is operational at v1 OR needs explicit canonical capture |
| 2. Country-title name cleanup | Elrond v1.1+ substrate-tagging-discipline work (9.11-D/E) execution surfaces whether name-pattern artifacts compound with tag-level artifacts; empirical scope sizing for cleanup work |
| 3. Commercial-vs-solo output differentiation | First multi-consumer scenario (post-v1-ship; Profile B B2B SaaS scoping OR Reincarnated player-surface integration) surfaces whether implicit output-purpose-passing breaks; empirically validates need for explicit flag |

### 4.3 Commit (architectural lock fires when)

| Recognition | Commit trigger |
|---|---|
| 1. Sampling-proportionality flagging | If T4-B v1 design call requires explicit policy → discipline candidate proposed to jack-ryan for canonical write at engineering-disciplines.md (probable #26 or sub-discipline of #25) |
| 2. Country-title name cleanup | When elrond v1.1+ substrate-tagging work fires; cleanup folds into Phase D-bis-style pass + LLM-curated review |
| 3. Commercial-vs-solo output differentiation | When Variant C engine adds multi-consumer support OR Reincarnated v1.1+ integration scoped; output_purpose field added to engine generation schema |

---

## 5. What this recognition record is NOT

- NOT pre-committing to any of the three architectural commitments (all deferred per § 4)
- NOT a discipline-amendment candidate canonical write — that's jack-ryan's territory if/when recognitions validate
- NOT a substrate-cleanup dispatch — that's elrond's territory in v1.1+ work
- NOT engine-architecture canonical doc — that's rocket + Matt territory when output_purpose field gets scoped
- NOT v1-gating — none of the three blocks v1 ship; all are v1.1+ refinement work
- NOT a roadmap edit (separate small entry will be added to 02-roadmap.md § 1.0 v1.1+ deferred queue cross-referencing this doc)

---

## 6. Cross-references

### Adjacent recognitions
- `canonical/story/marginal-lineage-tagging-pattern-2026-05-23.md` — 4-mode tagging-vocabulary collapse; predecessor pattern that this recognition extends with three forward-looking flags
- `canonical/story/n-am-indigenous-no-cluster-disposition-2026-05-23.md` + 4 sister marginal-lineage records — empirical grounding for sampling-proportionality recognition
- `canonical/story/fate-genre-recognition-and-mobile-alignment-trajectory-2026-05-23.md` — Variant C + Track M1a; downstream of commercial-vs-solo differentiation

### Empirical companion artifact
- `agentic_orchestration/gandalf/notes/2026-05-23-geography-vs-culture-substrate-analysis.html` — Chart.js visualization of 4-mode tagging-vocabulary collapse; empirical grounding for recognition 1 + 2

### v1.1+ deferred-queue residence
- `canonical/02-roadmap.md` § 1.0 v1.1+ deferred substrate-refinement queue — adjacent to 9.11-C/D/E + 9.10-E (subsumes 9.11-B)

---

## 7. Sign-off

**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-05-23 — direct invocation ("flag for later")
**Status:** Recognition Record — architectural commitments deferred per § 4 empirical-evidence criteria.
**Re-engagement gate:** Per § 4.2 validation criteria; recognitions move from "captured" to "validated → commit" when respective empirical triggers fire.

---

**Signed:** gandalf
**For:** capturing three forward-looking design-discipline recognitions (sampling-proportionality flagging; country-title name cleanup; commercial-vs-solo output differentiation) at session-end 2026-05-23 so they're not lost between sessions and v1.1+ work has explicit canonical reference.
