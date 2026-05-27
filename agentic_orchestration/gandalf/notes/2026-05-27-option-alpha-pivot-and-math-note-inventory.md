# Option α Pivot — Substrate-Clustered Emergent Classes + Math-Note Inventory + Path A Revert

> **STATUS:** CURRENT — load-bearing pivot record. Matt 2026-05-27 verbatim ratification sequence: (1) "option 1. Math before code" — Option α architectural pivot to substrate-clustered emergent classes; (2) "would be great to reference the 10 classes against those that emerge from the engine naturally and compare later on" — doc 48 preserved as A/B reference baseline; (3) "scope creep and content destruction may be trivial in comparison to stagnant vestigial logic that becomes ingrained and baked into the engine across time" — **Path A (revert engine commit `0a5a4f2`) ratified over Path B (migrate later)**. State change discovered post-pivot: rocket Stage 3 already shipped against doc 48 at engine `0a5a4f2`; KR closed Wave 1.5 at collab `440a725`. Path A reverts engine `0a5a4f2`; Stage 3 re-implemented under Option α after math notes ratify. Doc 48 retained as PRESERVED-FOR-COMPARISON reference baseline; this doc is the successor for engine generation purposes.

> **PATH A REVERT MECHANICS (added 2026-05-27 evening):**
> - `git revert 0a5a4f2` on engine repo creates revert commit undoing Stage 3 implementation
> - jack-ryan Gate-2 reviews the revert (~1-2 hrs)
> - KR amends collab Wave 1.5 closure records (`a230b71`, `182511b`, `3db7991`, `688cddc`, `440a725`) with revert-superseded notation; closure records stay as audit trail
> - Wave 2 dispatch authoring waits until math notes ratify + Stage 3 re-implementation lands under Option α (Wave 2 references chain structure; references must point at Option α infrastructure, not doc 48)
> - Substrate enrichment work (INT-AoE + monk + hybrid per Matt 2026-05-27 scope-creep directive) fires in PARALLEL with revert + math-note authoring

**Date:** 2026-05-27
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-05-27 verbatim — (a) "option 1. Math before code" ratifying Option α architectural pivot, (b) "reference the 10 classes against those that emerge from the engine naturally and compare later on" preserving doc 48 as A/B baseline
**Supersedes (for engine generation):** `canonical/48-cycle-14-class-roster-2026-05-27.md` canonical lock — retracted to PRESERVED-FOR-COMPARISON; doc 48 retained as design-history + comparison-reference artifact, NOT canonical for generation
**Companion docs:**
- `agentic_orchestration/gandalf/notes/2026-05-27-scaffold-drift-recognition-and-corrective-package.md` § 3 (Wave 1.5 prior framing — note Option α was NOT named in § 3.5's three options; this is the architectural gap the pivot corrects)
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` § 8.3 + § 6.6.1 (chain count + supporting chain — these MECHANISMS are preserved under Option α; only the pre-authored 10-class TAXONOMY is retired)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` Discipline #1 (math-before-code) + #18 (math hotspot routing) + #40 (scaffold-with-pending-decision)

---

## 0. TL;DR

**Architectural pivot ratified:** halt curated-roster path (doc 48); halt rocket Wave 1.5 Stage 3 against doc 48; re-author Wave 1.5 against Option α (engine generates per-kit emergent class identity from substrate clustering; no pre-authored fixed class taxonomy).

**Math-before-code discipline applies:** FIVE math notes must land + jack-ryan Gate-1 ratify BEFORE any rocket Stage 3 code fires. Math notes specify the clustering algorithm, the emergence rules, the naming policy, the cross-season persistence semantics.

**Doc 48 PRESERVED as A/B reference baseline.** When Option α lands and engine produces emergent-per-season classes, we compare those against the 10 hand-curated archetypes. This comparison is empirical evidence on the substrate-led-discipline vs designer-curation tension.

---

## 1. What changed and why

### 1.1 What we just retired (the week's work)

| Rigid form | What it constrained | Retired in |
|---|---|---|
| `synthetic_mode` gauntlet bypass | Gauntlet PASS criteria | Wave 0.5 Discipline #39 |
| `_SyntheticPlayerClass` synthetic class assignment | Per-kit class identity | Wave 0.5 + Cycle 13 close |
| 12-skill 3-chain 4-tier grid (scaffold drift) | Skill tree architecture | Wave 1.5 (in flight) |
| **doc 48 canonical 10-class roster** (the new rigid form sub-agent gandalf authored) | **Engine generation bounded to 10 pre-authored archetypes** | **2026-05-27 — this pivot record** |

Matt's catch: "We just worked for a solid week (maybe 3-6 months of agent hours) to remove the class as a rigid form. And now we added it back in." — empirically correct. The Option C path I framed in the scaffold-drift consolidated doc § 3.5 pre-committed to class-as-fixed-taxonomy without surfacing the deeper question: do classes need to exist as a fixed taxonomy at all?

### 1.2 What Option α commits to

**Engine generates per-kit class-identity from substrate clustering.** No pre-authored 10-class roster. Each season's substrate sample produces ITS OWN emergent class identities. The Court accumulates Spirits across many seasons' emergent classes (Spirits, not class slots).

Concretely:
- Per-kit `chain_count` (3 or 4) emerges from substrate density at the kit's BC cell + clustering parameters
- Per-kit `supporting_chain` theme emerges from substrate cluster characteristics (cultural lineage anchors, named_template aggregation, weapon_kind diversity)
- Per-kit T4 capstones (count = chain_count − 1) emerge from substrate-richest sub-themes within the cluster
- Per-kit `class_name` is POST-HOC: substrate-derived placeholder at Phase 2; Phase 5 LLM cohesion-judge produces final canonical name
- Cross-season identity persistence is a SEPARATE design call (math note 5 below)

### 1.3 What is PRESERVED under Option α

The structural MECHANISMS from doc 40 + doc 46 + the scaffold-drift consolidated doc § 3.3 are preserved:

- Variable chain count (3 or 4) per kit — preserved (now substrate-emergent, not class-pre-decided)
- T4 count = chain count − 1 — preserved (mechanical rule independent of class taxonomy)
- Supporting chain (T3-cap, class-intrinsic) — preserved (now substrate-emergent theme, not class-pre-decided)
- ONE T4 unlocked at a time (D66 active identity discipline) — preserved (runtime mechanism)
- Depth-≥4 branching (D69 wide-vs-tall) — preserved (substrate-emergent at high-density cells)

Only the pre-authored 10-class TAXONOMY is retired. The structural patterns persist.

### 1.4 What Matt preserved by his "compare later" directive

Doc 48 stays as a **reference baseline**. When Option α lands and engine produces emergent classes:

- A/B comparison: which of the 10 hand-curated archetypes does the engine NATURALLY produce?
- Which emergent classes have NO mapping to the 10? (Engine surfaced something the designer didn't anticipate.)
- Which of the 10 has NO substrate-emergent match? (Designer thought it was important; substrate doesn't vote for it.)

This comparison is itself empirical evidence on the substrate-led-discipline vs designer-curation tension. It informs whether we ever need a pre-authored class taxonomy, or whether emergent classes are sufficient for player-UX-legibility.

---

## 2. Math-note inventory (5 notes required BEFORE code fires)

### 2.1 Math Note 1 — Substrate clustering for chain_count emergence

**Owner:** elrond (statistical methodology) + gandalf (design-intent input)
**Target path:** `~/Games/reincarnated-engine/src/reincarnated/generation/math/wave-1-5-option-alpha-substrate-clustering-math-2026-05-27.md`
**Scope:**
- Given a kit's BC cell + the substrate row pool that matches its attribute/geometry/etc., what is the clustering algorithm that determines `chain_count` (3 or 4)?
- Density rule? Diversity rule? Substrate-cell-level natural vote?
- Threshold values for 4-chain-vote vs 3-chain-vote (e.g., "cell has ≥N substrate rows AND ≥K distinct cultural_lineage anchors → 4-chain")
- Smoke test: cluster the 2,293 v1_scope substrate; what's the emergent chain_count distribution? Compare against doc 48's 8 × 3-chain + 2 × 4-chain split.
- **Discipline #18 hotspot:** clustering methodology is statistical work; jack-ryan Gate-1 reviews per Discipline #18 mathematical layer routing.

### 2.2 Math Note 2 — Supporting-chain theme emergence

**Owner:** gandalf (design-spec-as-math)
**Target path:** `~/Games/reincarnated-engine/src/reincarnated/generation/math/wave-1-5-option-alpha-supporting-chain-emergence-math-2026-05-27.md`
**Scope:**
- Given a cluster of substrate weapon rows + their cultural_lineage + named_template anchors, how does a "supporting chain theme" emerge?
- Algorithm: substrate-shared-attribute clustering? Named-template aggregation? Cultural-lineage modal vote?
- Output vocabulary: is there a curated theme-pool (Iron-Discipline, Pack-Sense, etc.) or is it open-ended substrate-derived?
- Composes with Math Note 4 (naming policy) for final theme label production.

### 2.3 Math Note 3 — T4 capstone emergence from substrate sub-clusters

**Owner:** gandalf (design-spec-as-math) + elrond (sub-cluster methodology)
**Target path:** `~/Games/reincarnated-engine/src/reincarnated/generation/math/wave-1-5-option-alpha-t4-emergence-math-2026-05-27.md`
**Scope:**
- Within a cluster, what sub-themes emerge as T4 capstone candidates?
- 2 capstones for 3-chain clusters; 3 for 4-chain clusters (per D83 preserved)
- Substrate-richest sub-themes → T4 capstones; less-substrate-rich themes → supporting chain (T3-cap)
- How is "substrate-richness" measured? Row count? Named-template anchor density? Cultural-lineage diversity?
- Composes with Math Note 2 (supporting chain is the LEAST-substrate-rich emergent theme; T4s are the MOST-substrate-rich).

### 2.4 Math Note 4 — Class-naming policy (deterministic vs Phase 5 LLM)

**Owner:** gandalf (design-spec) + star-lord (Phase 5 LLM integration)
**Target path:** `~/Games/reincarnated-engine/src/reincarnated/generation/math/wave-1-5-option-alpha-class-naming-policy-math-2026-05-27.md`
**Scope:**
- Each kit gets a `class_name` — where does the name come from?
- **Option D1 (deterministic):** substrate-derived label at Phase 2 (e.g., "STR-Cleave-Heavy-Norse" — descriptive, not romantic)
- **Option D2 (Phase 5 LLM):** placeholder at Phase 2 → Phase 5 cohesion-judge LLM generates final canonical name (romantic + genre-coherent)
- **Option D3 (hybrid):** substrate-derived placeholder + Phase 5 LLM final name per cohort
- Player-UX consideration: deterministic names are testable + reproducible; LLM names are atmospheric but introduce non-determinism
- Composes with Phase 5 cohesion-judge architecture (doc 39 + Wave 3 dispatch territory).

### 2.5 Math Note 5 — Cross-season identity-persistence semantics

**Owner:** gandalf (design call)
**Target path:** `~/Games/reincarnated-engine/src/reincarnated/generation/math/wave-1-5-option-alpha-cross-season-persistence-math-2026-05-27.md`
**Scope:**
- Does "Barbarian-shape" persist across seasons, or is each season's class roster fully independent?
- **Option E1 (season-scoped):** each season's emergent classes are independent. Court accumulates Spirits with season-specific class names. Player meets each season's classes fresh.
- **Option E2 (canonical-shape persistence):** substrate-clustering pattern produces recurring shapes across seasons; same shape → same canonical class name across seasons. Court has structured class-collection.
- **Option E3 (hybrid):** seasons produce emergent classes; LLM/clustering pass normalizes recurring shapes to canonical names; some classes are persistent, others are season-unique
- Composes with Earth-realm + Court of Forms framework (Pattern B thought-experiment from earlier session).

---

## 3. Sequencing under math-before-code discipline

| Step | Owner | Status |
|---|---|---|
| 1. Math-note inventory authored (this doc) | gandalf | ✅ 2026-05-27 |
| 2. Doc 48 STATUS retracted to PRESERVED-FOR-COMPARISON | gandalf | ✅ 2026-05-27 |
| 3. KR halt kicker authored | gandalf | ⏳ next |
| 4. KR halts Stage 3 + commissions math-note authoring dispatches | knight-rider | ⏳ |
| 5. Math Notes 1-5 authored | elrond + gandalf + star-lord (per § 2 routing) | ⏳ |
| 6. jack-ryan Gate-1 review on each math note (Discipline #1 + #18) | jack-ryan | ⏳ |
| 7. Math-note ratification | Matt (per Discipline #18 math-hotspot ratification) | ⏳ |
| 8. Wave 1.5 Stage 3 RE-AUTHORED against ratified math notes | knight-rider | ⏳ |
| 9. rocket Stage 3 implementation (math-ratified scope) | rocket | ⏳ |
| 10. A/B comparison: engine-emergent classes vs doc 48 10-class baseline | gandalf | ⏳ post-Wave-5 |

**Critical:** no rocket Stage 3 code fires until step 7 (math-note ratification). This is Discipline #1 math-before-code in its load-bearing form.

---

## 4. What changes for Wave 1.5 + Wave 5 production

### 4.1 Wave 1.5 — Option α re-scoping

- Stage 1 elrond substrate audit output: **STILL USEFUL.** Becomes input to clustering algorithm (Math Note 1), not pre-authored roster source.
- Stage 2: REPLACED. The "gandalf design call for class roster" stage is retired. Replaced by "5 math notes authored + Gate-1 + Matt ratification."
- Stage 3: **HALTED** against doc 48. Re-authored against ratified math notes.

### 4.2 Wave 5 — production season under Option α

- Wave 5 generates ~28-32 surviving characters (season cardinality doc 41 § 4.6 amendment preserved)
- Characters have emergent class names (per Math Note 4 policy)
- No pre-authored class roster constrains generation
- A/B comparison fires post-generation: which doc 48 archetypes emerged? Which didn't? Which emergent classes weren't anticipated?

### 4.3 Pre-Wave-5 prerequisite assertion update

Per scaffold-drift consolidated doc § 5.3 — the prerequisite list shifts:

- [x] Fix A hygiene filter (rocket) — closed
- [x] Fix B math-note (rocket) — closed
- [x] Discipline #40 canonical-write (jack-ryan) — closed
- [ ] **Wave 1.5 RE-SCOPED under Option α** (replaces "Wave 1.5 skill-tree architecture")
  - Math Notes 1-5 authored + Gate-1 + Matt ratification
  - Stage 3 implementation against ratified math
- [ ] **Season cardinality** (doc 41 § 4.6 amendment) — PRESERVED, no change

---

## 5. The architectural lesson (Discipline #40 + substrate-led composition)

The scaffold-drift consolidated doc § 3.5 framed "which classes exist?" as a question requiring an answer from three options (A/B/C). All three pre-committed to class-as-fixed-taxonomy. The deeper question — "do classes need to exist as a fixed taxonomy at all?" — was not surfaced.

Sub-agent gandalf executed the dispatch faithfully and produced doc 48. The drift was UPSTREAM in my framing, not in the sub-agent's execution.

**Discipline-amendment candidate (proposed; routes to jack-ryan):**

> **Discipline #41 candidate — pre-authored taxonomy interrogation.** Before asking "which N exist?" for any pre-authored taxonomy in a generative system, ASK FIRST: "should this taxonomy be pre-authored at all, or should it emerge from substrate clustering?" The substrate-led discipline composes with Discipline #40 (scaffold-with-pending-decision) — pre-authored taxonomies in substrate-led systems are scaffold by default; ratification as canonical requires explicit justification of why substrate-emergence is insufficient.

This is jack-ryan's territory for canonical-write. Separate dispatch.

---

## 6. Cross-references

- `canonical/48-cycle-14-class-roster-2026-05-27.md` — PRESERVED-FOR-COMPARISON (canonical lock retracted)
- `canonical/00-ground-state.md` — needs amendment (doc 48 entry STATUS update + this doc registered)
- `agentic_orchestration/gandalf/notes/2026-05-27-scaffold-drift-recognition-and-corrective-package.md` § 3 — Wave 1.5 framing that pre-committed to taxonomy (architectural-gap origin)
- `agentic_orchestration/elrond/notes/2026-05-27-cycle-14-wave-1-5-class-roster-substrate-audit.md` — Stage 1 audit output (STILL USEFUL as clustering input)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Discipline #1 + #18 + #40 LOAD-BEARING; #41 candidate proposed

---

## 7. Sign-off

**Author:** gandalf (story-and-design steward)
**Status:** CURRENT — Option α pivot record + math-note inventory; load-bearing for Wave 1.5 Stage 3 re-scoping
**Authority:** Matt 2026-05-27 verbatim "option 1. Math before code" + "reference the 10 classes against those that emerge from the engine naturally and compare later on"
**Composition:** with doc 40 § 8.3 + § 6.6.1 (structural mechanisms PRESERVED; only pre-authored taxonomy retired) + doc 41 § 4.6 (season cardinality unchanged) + doc 48 (PRESERVED-FOR-COMPARISON baseline) + scaffold-drift consolidated doc § 3.5 (architectural-gap origin acknowledged)

**For:** the architectural pivot from curated-roster (doc 48 canonical lock) to substrate-clustered emergent classes (Option α), ratified by Matt 2026-05-27. Honors substrate-led discipline by retiring pre-authored taxonomy; honors Discipline #1 by requiring 5 math notes + jack-ryan Gate-1 + Matt ratification BEFORE any rocket Stage 3 code fires; honors Matt's compare-later directive by preserving doc 48 as A/B reference baseline.

**Signed:** gandalf (story-and-design steward)
