# T4-B v1 Catalogue Authoring Scaffolding

> **AMENDMENT 2026-05-24 — REFRAMED AS POST-MORTEM EVALUATION FRAMEWORK.** Per Matt 2026-05-24 design dialogue: original scaffolding framed T4-B as hand-authored pre-spec (~30 entries via ~3-6 design call sessions), but skill-system § 8 (locked 2026-05-24) commits to algorithmic mechanic-alteration as architectural advance. The two were inconsistent. Matt's correction: hand-authoring T4 entries in the abstract is meaningless — T4 build-defining skills are always per-kit / per-substrate-anchor / per-BC-target-cell; without forms, hand-authoring is creating-into-the-void. **Revised approach:**
> - **Algorithm IS the v1 T4 deliverable** (rocket seam post-Cycle-10; per skill-system § 8.5)
> - **T4-B catalogue authoring becomes POST-MORTEM EVALUATION** — after engine generates ~30-40 v1 forms with algorithm-produced T4s, Matt + gandalf review form-output via loadout app; for ~5-10 forms, hand-author T4 alternatives; compare to algorithm; lock whichever is better; algorithm gets validation feedback for v1.1+ improvement
> - **Sessions reduce from ~3-6 pre-spec to ~1-2 post-mortem** (post-engine-generation; post-W1.13/H1-H5-baseline territory; ~3-5 weeks from now wall-clock)
> - **Critical-path dependency surfaced:** loadout app integration (drax + star-lord export) must be ready to consume engine-generated forms + display skill trees for hand-authoring interface
> - Sections § 1-9 below remain INFORMATIVE (entry schema, substrate-anchoring decision framework, acceptance gates) but are consumed at POST-MORTEM time, not pre-spec time


> **STATUS:** CURRENT — scaffolding for upcoming Matt + gandalf design-call sessions to author the ~30-50 entry T4-B v1 catalogue. NOT the catalogue itself; the authoring framework + schema + open questions that the design call(s) resolve into actual entries.

**Author:** gandalf
**Authority:** Matt 2026-05-23 — direct instruction to scaffold T4-B authoring as item 1 of P1 hive-mind preparation
**Status:** Scaffolding document. Architectural commitments live at T4-A (already locked) and Question A verdict (deferred per § 9 empirical-evidence criteria). This doc captures HOW to author T4-B v1 entries; entries themselves authored at design call.
**Companion docs:**
- `canonical/story/tier-4-architecture-defaults-2026-05-22.md` (T4-A architecture — locked)
- `agentic_orchestration/gandalf/notes/2026-05-23-question-A-w1-13-tier-4-hypothesis-verdict.md` (Q-A verdict — design-spec-as-math; G1-G4 acceptance gates per § 6.1)
- `agentic_orchestration/gandalf/notes/2026-05-23-question-B-gear-armor-legendary-verdict.md` (Q-B verdict — gear/armor/legendary; named-mythological substrate layer)
- `agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/phase-E-2-cluster-labels.md` (Phase E-2 cluster labels — current 125-cluster substrate-anchoring source)
- `canonical/story/marginal-lineage-tagging-pattern-2026-05-23.md` (semantic-layer rep-audit discipline — required at substrate-anchoring decisions)
- `agentic_orchestration/operating-procedures/gandalf.md` § 4.1-4.6 (operational protocols this work cycle surfaced)

---

## 0. TL;DR

T4-B v1 catalogue = ~30-50 hand-authored Tier 4 build-defining-node entries per T4-A § 4. Each entry:
- Names a specific build-defining-node
- Anchors to substrate identity (cluster + secondary cluster cells)
- Specifies a regime-change mechanic (the η-coefficient operationalization from Q-A § 2.2)
- Predicts G1-G4 gate-pass behavior per Q-A § 6.1
- Carries a sim-viability flag per T4-A § 3.3 step 5

The catalogue gates Q-A H8/H9/H8.diff hypothesis-test execution at gamora. Without entries, the framework has nothing to test.

**This scaffolding does NOT author entries.** It captures the authoring methodology, entry schema, substrate-anchoring decision framework, and open questions for the Matt + gandalf design call(s) that author the actual entries.

---

## 1. T4-B authoring methodology (per T4-A § 3.3)

For each candidate build-defining-node:

| Step | Action | Owner |
|---|---|---|
| **Step 1** | Identify rank-3 candidate identity from BDI ω/τ table substrate-pairs OR named-mythological corpus OR engine-generated cohesion-judge identity | gandalf (proposes); Matt (approves) |
| **Step 2** | Scope the regime-change mechanic (η-coefficient operationalization per Q-A § 2.2) | gandalf design-spec-as-math |
| **Step 3** | Determine substrate-anchoring (cluster identity + secondary cluster cells where applicable) — apply semantic-layer rep-audit per gandalf OP § 4.4 | gandalf |
| **Step 4** | Predict G1-G4 gate-pass behavior per Q-A § 6.1 (multiplicity / bimodality / mode-separation / differential) | gandalf |
| **Step 5** | Sim-viability flag check — rocket runs sim-viability per entry; jack-ryan Gate-2 ratifies | rocket + jack-ryan |
| **Step 6** | Author entry into catalogue with all fields per § 3 schema below | gandalf |
| **Step 7** | Catalogue review pass at Matt + gandalf design call; lock entry | Matt + gandalf |

Steps 1-4 + 6 are foreground design work at Matt + gandalf design call. Step 5 fires post-authoring; Step 7 locks.

---

## 2. Entry schema

Each T4-B catalogue entry carries the following fields:

| Field | Description | Required at v1 |
|---|---|---|
| `entry_id` | Stable identifier (e.g., `t4b-v1-001` through `t4b-v1-NNN`) | YES |
| `name` | Human-readable name | YES |
| `signature_or_secondary` | T4-A § 2 tier — signature (rank-3 completer) OR secondary capstone (rank-2 modulator) | YES |
| `regime_change_mechanic` | What the T4 node does mechanically; the η-coefficient operationalization in design language | YES |
| `substrate_anchoring` | Which substrate-triple identity this T4 node binds to — cluster identity + secondary cells | YES |
| `narrative_intent` | Short design-intent narrative (1-2 paragraphs); the build-defining "feel" this entry produces | YES |
| `expected_g1_pass` | Predicted H8 multiplicity gate behavior (PASS / FAIL / UNCERTAIN with reasoning) | YES |
| `expected_g2_pass` | Predicted H9 bimodality gate behavior | YES |
| `expected_g3_pass` | Predicted mode-separation behavior (on-mode vs off-mode kit_power) | YES |
| `expected_g4_pass` | Predicted differential-effect behavior (η_matched vs η_non_matched) | YES |
| `sim_viability_flag` | Pass/fail flag set post-rocket sim-viability check per T4-A § 3.3 step 5 | YES at lock; deferred at authoring |
| `companion_secondaries` | 1-3 secondary capstones per T4-A § 2 (for signature entries; null for secondary entries) | OPTIONAL v1 |
| `cohesion_judge_name_pending` | Cohesion-judge LLM naming output (if engine-generated identity layer) | OPTIONAL v1 |
| `notes` | Authoring notes; design-call references; substrate-evidence citations; rep-audit findings | OPTIONAL |

JSON schema variant for engine consumption (rocket integration; T4-C/D/E phasing per T4-A § 5) is downstream territory; v1 catalogue may live as Markdown table at `canonical/story/t4-b-v1-catalogue.md` until rocket consumption pattern locks.

---

## 3. Substrate-anchoring decision framework

Substrate anchoring is the **critical pre-step** before entry authoring. Per Q-A verdict § 2.1 P3 (differential effect), each T4 node binds to a specific substrate identity that the multiplicity + bimodality + differential effects fire against.

### 3.1 Four candidate substrate-anchoring sources

| Source | Description | Status | When to use |
|---|---|---|---|
| **A. Phase E-2 cluster identities (coarse-spine k=3)** | 125 clusters; labels at `phase-E-2-cluster-labels.md`; substrate-descriptive (lineage / period / register / form / wield) | Available; Phase E-1.5 may refine cluster taxonomy | Default for v1; preserves substrate-led discipline |
| **B. Named-mythological corpus** | Real-world cultural-tradition figures from broadly-fictionalized traditions (Arthurian, Greek, Norse, Celtic, Finnish) | Track M1a; not yet authored; gated on P4 cluster labeling for faction-architecture validation | Reserve for legendary-tier v1 entries IF Track M1a fires in time; otherwise defer to v1.1+ |
| **C. Engine-generated cohesion-judge identities** | LLM cohesion-judge produces identities post-Phase E-2 cluster labeling for clusters that don't have named-mythological binding | Operational post-Phase-E-2 acceptance; per Q-A verdict + Earth-Self/Spirit-Form thread (deferred) | Primary fallback when cluster has no real-tradition binding |
| **D. Hybrid (A + B + C per entry)** | Some T4 nodes anchor to named-mythological (M1a tier); most anchor to engine-generated identities (M1b tier) | Multi-source per-entry decision | Likely v1 default — most entries are A or C; few are B |

### 3.2 Apply semantic-layer rep-audit at substrate-anchoring

Per gandalf OP § 4.4 (semantic-layer rep-audit discipline):

> The substrate's vote is binding at the geometry layer (clustering algorithm output) but NOT necessarily binding at the semantic layer (cultural-tradition interpretation of cluster identity). Semantic-layer use of substrate output requires rep-audit at firing.

**Operational check at every substrate-anchoring decision:**
- Pull top-5 hdbscan_native reps for the candidate anchor cluster
- Verify reps match the build-defining intent the T4 node carries
- If reps contradict intent (e.g., Cluster 87 "S. American Indigenous Contemporary Shotgun" reps are Modern Argentine military hardware, NOT Pre-Columbian Andean weapons), do NOT anchor to that cluster for a Pre-Columbian-themed T4 node
- Document the rep-audit finding in entry's `notes` field

### 3.3 Cluster-taxonomy stability gate

Phase E-1.5 sensitivity sweep is in flight at scaffolding-authoring time. If Phase E-1.5 refines cluster taxonomy (Cluster 62 split candidate; form-bundling vs prefix-bundling resolution), specific cluster keys T4-B uses will shift.

**Discipline:** T4-B catalogue authoring should fire **after Phase E-1.5 acceptance lands** to lock substrate taxonomy. Pre-Phase-E-1.5 authoring risks re-keying all 30-50 entries when taxonomy refines. This scaffolding doc captures the authoring framework now (cluster-agnostic at scaffolding layer); cluster-specific entry authoring waits.

---

## 4. Open questions for Matt + gandalf design call

These need decision before entry authoring fires:

| Q | Question | Default lean (gandalf) |
|---|---|---|
| **Q1** | Substrate-anchoring source mix for v1 — A-only, A+C, A+B+C? | A+C hybrid; defer B to v1.1+ unless M1a fires in time |
| **Q2** | Catalogue scoping for v1 — 30 entries (light), 40 (medium), 50 (full per T4-A § 4 upper bound)? | 30 first round to validate framework + acceptance gates; expand to 50 if validation lands clean |
| **Q3** | Sim-viability flag check timing — predict G1-G4 first then sim-verify, OR sim-verify candidates pre-authoring? | Predict first, sim-verify per-entry post-authoring per T4-A § 3.3 step 5 |
| **Q4** | Companion-secondary scoping — every entry gets 1-3 secondaries authored together, OR signatures first / secondaries deferred? | Signatures first for v1; secondaries deferred to v1.1+ unless design call surfaces tightly-coupled cases |
| **Q5** | Cohesion-judge naming integration — does cohesion-judge name each entry post-substrate-anchoring, OR human-curated names at authoring? | Human-curated for v1 (per D7 AI-tell discipline — no raw LLM at major story moments); cohesion-judge as flavor-suggestion layer |
| **Q6** | Named-mythological tier (M1a) integration — gate on Track M1a firing OR independent? | Independent; v1 catalogue can mix engine-generated names with optional M1a integration at design call |
| **Q7** | Phase E-1.5 cluster-taxonomy refinement — wait for Phase E-1.5 acceptance, OR proceed against Phase E-2 coarse-spine and re-key? | **Wait for Phase E-1.5 acceptance.** Substrate-led discipline + framing-audit applied: refinement evidence is imminent; locking taxonomy first is cheaper than re-keying 30-50 entries |
| **Q8** | Cultural-sensitivity stratification (per Q-B § 3.2 + reappropriation thread) — apply at substrate-anchoring? | Yes — broadly-fictionalized traditions OK to name explicitly; marginalized-culture traditions stay engine-generated; living-religious traditions excluded |

---

## 5. Acceptance criteria reference

Per Q-A verdict § 6.1 — per-entry acceptance gates measured by gamora at H8/H9 execution:

| Gate | Criterion | Source |
|---|---|---|
| **G1 multiplicity** | η coefficient p-value < 0.05 AND effect size (Cohen's d > 0.5 OR partial η² > 0.06) in matched-substrate-triple kits | Q-A § 4 H8 |
| **G2 bimodality** | Hartigan's dip test rejects unimodality (p < 0.05) AND GMM 2-component selected over 1-component via BIC | Q-A § 5 H9 |
| **G3 mode separation** | On-mode mean ≥ 1.5× off-mode mean kit_power (or threshold per legolas Mode A consultation) | Q-A § 5.6 |
| **G4 differential** | η_matched significantly larger than η_non_matched (bootstrap CI; permutation test) | Q-A § 4.4 H8.diff |

**Per-entry disposition:**
- **Pass-all-gates**: T4 entry validated; folds into v1 catalogue lock
- **Pass-3-of-4**: T4 entry flagged for design review; possible revision
- **Pass-≤2**: T4 entry not doing build-defining work; demote to Tier 3 OR revise OR remove

---

## 6. Sequencing — when T4-B catalogue authoring fires

Per Q-A verdict § 9 empirical-evidence criteria + recommended sequence:

```
Phase E-1.5 sensitivity sweep acceptance lands (cluster-taxonomy stable)
    ↓
Matt + gandalf design-call session 1 scheduled
    ↓
Q1-Q8 open questions resolved at design call session 1
    ↓
~10 exemplar entries authored at session 1 (validates framework)
    ↓
Session 2-N: expand to ~30-50 entries
    ↓
Per-entry sim-viability flag check (rocket; in parallel)
    ↓
Per-entry G1-G4 expected-pass predictions captured
    ↓
T4-B v1 catalogue lock — ready as input to Q-A H8/H9 execution at gamora
```

**Estimated effort:** 3-6 design-call sessions over multiple sessions. Not single-pass work. Catalogue completion is its own work-unit before P1 hive-mind fires H8/H9 against entries.

---

## 7. Downstream consumers of T4-B v1 catalogue

Once locked, T4-B v1 catalogue feeds:

| Consumer | What it consumes |
|---|---|
| **Q-A H8/H8.diff/H9 hypothesis tests** | Per-entry T4_node values for gamora to test against substrate-triple kits |
| **Cohesion-judge calibration (P5)** | Per-entry narrative_intent + cohesion-judge naming candidates |
| **Engine integration via rocket (T4-C/D/E phasing)** | Per-entry substrate_anchoring + regime_change_mechanic for runtime spawning |
| **Q-B v1.1+ named-mythological binding** | Per-entry substrate_anchoring for M1a/M1b/M1c stratification per Q-B § 3 |
| **Player-facing displays (downstream UI)** | Per-entry name + narrative_intent (after D7 AI-tell discipline curation) |

---

## 8. What this scaffolding does NOT do

- **Not the catalogue.** Entries are authored at Matt + gandalf design call session(s) post-Phase-E-1.5 acceptance.
- **Not committed to specific cluster identities.** Substrate-anchoring decisions happen per-entry at design-call time, against locked Phase E-1.5 taxonomy.
- **Not architectural amendments to T4-A.** T4-A architecture stands. This scaffolding operates within T4-A.
- **Not architectural amendments to Q-A or Q-B verdicts.** Both verdicts stand. This scaffolding executes within their frameworks.
- **Not LLM-generation of entries.** Entries are gandalf-authored or gandalf+Matt-curated per T4-A § 3.3. Cohesion-judge naming is an OPTIONAL flavor-suggestion layer at design call, never auto-commit.
- **Not exemplar entries with substrate-specifics.** Exemplar entries (~3-5 candidates) would commit to specific cluster identities prematurely; deferred to design call session 1 after Phase E-1.5 lock.
- **Not gating P1 hive-mind on every entry being locked.** P1 hive-mind can fire on ~30 entries (Q2 default lean) with the remaining ~20 added in subsequent passes during P1 hive-mind cycles.

---

## 9. Empirical-evidence criteria for re-engagement

Per gandalf OP § 3.4 recognition-validate-commit:

- **Recognition (this scaffolding):** captured.
- **Validate before catalogue authoring fires:**
  - Phase E-1.5 sensitivity sweep acceptance landed
  - Cluster taxonomy locked at refined-or-coarse-spine state
  - Matt + gandalf design call session 1 scheduled
  - Q1-Q8 open questions answered at session 1
- **Commit (catalogue lock):**
  - ~30 v1 entries authored with all schema fields populated
  - Per-entry sim-viability flag check complete (rocket)
  - Per-entry G1-G4 expected-pass predictions captured (gandalf)
  - Catalogue file at `canonical/story/t4-b-v1-catalogue.md` registered in ground-state oracle § 1

---

## 10. Sign-off

**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-05-23 — direct instruction to scaffold T4-B authoring as item 1 of P1 hive-mind preparation
**Status:** **Scaffolding** — captures HOW to author T4-B v1 catalogue. Catalogue authoring fires post-Phase-E-1.5 acceptance + Matt + gandalf design call scheduling.
**Cross-references:** T4-A architecture defaults; Q-A verdict; Q-B verdict; gandalf OP § 4.1-4.6 (framing-audit checklist + semantic-layer rep-audit + first-canonical-example); Phase E-2 cluster labels; marginal-lineage tagging-pattern meta-record.
**Companion artifact at lock:** `canonical/story/t4-b-v1-catalogue.md` (proposed path; finalized at design call session 1).

---

**Signed:** gandalf
**For:** the T4-B v1 catalogue authoring framework + schema + substrate-anchoring decision rubric + open questions for the upcoming Matt + gandalf design call session(s). Catalogue itself authored at session(s) post-Phase-E-1.5 acceptance.
