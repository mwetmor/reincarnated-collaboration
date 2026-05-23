# Mathematical Seam Naming — Layer Declaration + Math-Hotspot Annotations + Discipline #1.1

**Date:** 2026-05-23
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-05-23 — confirmed during cleanup session following math-agent question
**Status:** DRAFT for jack-ryan review → Matt approval → knight-rider integration
**Companion docs:**
- `canonical/38-downstream-delivery-strategy-2026-05-23.md` (D1-D10 lock; references the P-phase structure)
- `canonical/00-ground-state.md` (ground-state oracle)
- `canonical/story/hive-mind-protocol-weapon-library-import-2026-05-22.md` (P0-P5 + PD weapon-library protocol)
- `canonical/story/hive-mind-protocol-qd-engine-rebuild-2026-05-21.md` (parent QD-engine-rebuild P-series)

---

## 0. TL;DR

Reincarnated has **bounded math hotspots** at three named phases across active P-series protocols — P2 axis discovery, P3 multimodal clustering, P5 cohesion-judge validation. These are graduate-level stats moments where **methodology selection** (not execution) is the failure surface. Rather than draft a dedicated mathematician agent, this artifact:

1. **Names the Mathematical Layer** as a cross-cutting layer distributed across existing seams (no new agent)
2. **Annotates the three math hotspots** with methodology-consultation requirements
3. **Proposes Discipline #1.1 — Methodology-before-execution** as a discipline addition guarding against the "looks-correct-but-subtly-wrong" failure mode

This is jack-ryan's process-side review then Matt's approval then knight-rider's integration into `AGENTS.md` + `engineering-disciplines.md`.

---

## 1. The Mathematical Layer (proposed addition to `agentic_orchestration/AGENTS.md`)

**Proposed text to insert into AGENTS.md (suggested location: after the agent-by-agent scope-map, before founding ADR references):**

> ## Mathematical Layer (cross-cutting; no dedicated agent)
>
> Math work is **distributed by data-locality**, not owned by a single agent. Each seam handles the math native to its data + tooling:
>
> | Math work-type | Owning seam | Examples |
> |---|---|---|
> | **Design-spec-as-math** — axis meanings, formula intent, architectural defaults, design-intent expressed as algebraic structure | **gandalf** | BDI ω/τ tables, BC axes lock, T4 architecture defaults, gear-substrate rule table, build-defining resonance formula |
> | **Statistical methodology on catalogue data** — dimensionality reduction, factor analysis, clustering, embedding-space operations | **elrond** | P2 axis discovery, P3 multimodal clustering, abstraction-analysis tables |
> | **Simulation-side math** — balance loops, convergence algorithms, fight-resolution math, recompose-first arithmetic | **gamora** | B14.5 V1 primary loop, W0.10 boss-AI math, multi-dim convergence algorithm |
> | **Telemetry statistics** — distributions, aggregates, derived metrics, anomaly detection, judge calibration | **star-lord** | LC-002/009/011 attribution analysis, sidecar findings, distribution audits |
> | **Visual perception math** — image-similarity scoring, embedding-based comparison, perceptual-distance metrics | **galadriel** | Visual benchmarking vs genre-peer references, perception-test scoring |
> | **External-literature methodology research** — when methodology selection requires graduate-level stats grounding beyond the seam's native depth | **legolas Mode A** | Methodology consultations for P2/P3/P5 math hotspots |
>
> **Math hotspots** (methodology-choice moments where external-literature rigor is required before execution) are explicitly named in the P-phase protocols. See § 2 below for the current list.
>
> **Routing rule:** when math work could plausibly land in multiple seams, knight-rider dispatches per data-locality. When in doubt, gandalf advises on routing.

---

## 2. Math-Hotspot Annotations (proposed additions to active P-phase protocols)

Three named hotspots across active P-series. Each requires **legolas Mode A methodology consultation before execution** and a **design-call between the owning seam + gandalf** to lock the methodology choice.

### 2.1 Hotspot — P2 axis discovery (weapon-library-import protocol)

**Phase:** P2 — Statistical axis discovery + BDI ω-seeding
**Owning seam:** elrond (execution); gandalf (design intent + acceptance criterion)
**Methodology surface:** PCA vs factor analysis vs NMF vs UMAP vs t-SNE on sparse multimodal feature matrix (text features + numerical properties + categorical features + image embeddings); variance-explained validation; axis-stability bootstrapping; interpretability scoring
**Failure mode:** picking the wrong technique produces axes that look fine in 2D projections but are subtly wrong — variance-loaded on the wrong feature subsets, unstable under resampling, or non-interpretable in domain terms. Downstream Phase 4 cluster-labeling cannot detect this failure mode because the axes are already locked.
**Required action before execution:**
1. legolas Mode A research commission: "methodology selection for dimension reduction on sparse multimodal feature matrices in [our specific data shape]"
2. Design call: gandalf + elrond + Matt review methodology recommendation; lock choice + variance-threshold + interpretability-acceptance criterion
3. Execute via elrond; report stability metrics + interpretability scores alongside the axes themselves

**Annotation to add to `hive-mind-protocol-weapon-library-import-2026-05-22.md` § P2:**
> **[MATH HOTSPOT — methodology consultation via legolas Mode A before execution; methodology lock requires gandalf + elrond + Matt design call; failure mode is "looks-correct-but-subtly-wrong" — guard via Discipline #1.1.]**

### 2.2 Hotspot — P3 multimodal clustering (weapon-library-import protocol)

**Phase:** P3 — Multi-dimensional clustering analysis
**Owning seam:** elrond (execution); gandalf (design intent + acceptance criterion)
**Methodology surface:** HDBSCAN vs k-means vs GMM vs spectral clustering choice; silhouette + Davies-Bouldin + gap-statistic validation; multimodal-distance-metric design (how do you compute distance between two weapons whose features include a 1024-dim text-embedding + 8 numerical properties + 12 categorical tags?); cluster-count selection
**Failure mode:** clusters that pass cluster-validation metrics but don't carry design-meaningful weight at P4 semantic labeling — i.e., gandalf + Matt cannot name them. Or worse: clusters that look meaningful but are artifacts of the distance-metric design rather than substrate-truth.
**Required action before execution:**
1. legolas Mode A research commission: "clustering methodology selection for sparse multimodal data with mixed feature types"
2. Design call: gandalf + elrond + Matt review; lock algorithm + validation metrics + cluster-count target range
3. Execute via elrond; report cluster validation alongside cluster assignments

**Annotation to add to `hive-mind-protocol-weapon-library-import-2026-05-22.md` § P3:**
> **[MATH HOTSPOT — methodology consultation via legolas Mode A before execution; methodology lock requires gandalf + elrond + Matt design call.]**

### 2.3 Hotspot — P5 cohesion-judge statistical validation (both P-series converge here)

**Phase:** P5 — Cohesion-judge validation (weapon-library P5 + QD-engine-rebuild P5)
**Owning seam:** star-lord (statistics execution); gandalf (design intent + acceptance criterion); gamora (simulation-side integration)
**Methodology surface:** LLM-as-judge calibration with statistical rigor; inter-rater reliability (Cohen's kappa, Fleiss's kappa); significance testing for judge accuracy claims; probability calibration via isotonic regression; calibration-set sample-size determination
**Failure mode:** declaring the cohesion-judge "validated" based on a small sample with overstated significance, or with a calibration that's accurate-on-average but miscalibrated at the tails (where rare-but-important judgments live).
**Required action before execution:**
1. legolas Mode A research commission: "LLM-judge calibration methodology + statistical significance testing for content-validation use cases"
2. Design call: gandalf + star-lord + gamora + Matt review; lock calibration methodology + sample-size + acceptance criterion
3. Execute via star-lord; report calibration curves + tail-behavior alongside accuracy point estimates

**Annotation to add to `hive-mind-protocol-qd-engine-rebuild-2026-05-21.md` P5 section AND `hive-mind-protocol-weapon-library-import-2026-05-22.md` § P5:**
> **[MATH HOTSPOT — methodology consultation via legolas Mode A before execution; methodology lock requires gandalf + star-lord + gamora + Matt design call.]**

### 2.4 Light hotspots (worth flagging but lower severity)

These warrant brief methodology check-ins but not full design-call ceremony:

- **P1.5 feature extraction** (embedding-model choice) — if the embedding model changes downstream PCA behavior, elrond should consult legolas Mode A on model selection
- **P5 substrate-density precomputation** (density estimation technique) — KDE vs GMM vs Voronoi-based; star-lord owns; light consultation only

---

## 3. Discipline #1.1 — Methodology-Before-Execution (proposed amendment to `engineering-disciplines.md`)

**Proposed text to add as Discipline #1.1 (sub-discipline of Discipline #1 math-before-code):**

> ### #1.1 — Methodology-before-execution (math-hotspot discipline)
>
> For statistical-methodology choices at named **math hotspots** (currently P2/P3/P5 across active protocols), the methodology decision is made BEFORE execution — not derived FROM execution. This means:
>
> 1. **Commission legolas Mode A research first** for external-literature methodology grounding
> 2. **Design call locks the methodology** (gandalf + owning-seam + Matt) before any code runs
> 3. **Acceptance criteria defined upfront** — variance thresholds, validation metrics, interpretability scoring — not after looking at the output
> 4. **Stability / sensitivity analysis required** at execution time (bootstrapping, cross-validation, ablation across methodology hyperparameters)
>
> **Why this discipline exists:**
> The failure mode at math hotspots is **"looks-correct-but-subtly-wrong"** — execution produces output that passes basic eyeball checks but is methodologically incorrect (wrong technique for data shape, unstable under resampling, miscalibrated at tails, variance-loaded on wrong subsets). Downstream validation cannot detect this because the methodology error is locked into the output's structure.
>
> Discipline #1 ("math before code") catches the case where math should exist before code exists. Discipline #1.1 ("methodology before execution") catches the case where math exists but the wrong math was chosen.
>
> **Identifying math hotspots:**
> A phase is a math hotspot if **methodology selection is non-trivial** (multiple reasonable techniques exist) AND **execution failure is silent** (output passes basic checks even when methodology is wrong). Current named hotspots are documented in `agentic_orchestration/gandalf/notes/2026-05-23-mathematical-seam-naming.md` § 2.
>
> **Integration with Discipline #19 (right tool for the validation question):**
> Discipline #1.1 is the upstream methodology-choice analog to #19's tool-selection discipline. Together: pick the right methodology (#1.1), then pick the right validation tool for it (#19), then execute.

---

## 4. Why this is better than a dedicated mathematician agent

(Documented for posterity and future re-evaluation triggers.)

### 4.1 Why no new agent now

- **Math is cross-cutting, not seam-shaped.** Each seam already has math native to its data. A dedicated agent would either compete with existing seams for the work properly theirs OR have no clear ownership.
- **Volume is bounded.** Three hotspots per active protocol cycle is consultation-volume, not full-time-agent volume.
- **Methodology selection is the failure surface, not execution.** A dedicated agent would be redundant on execution (existing seams handle that) and would create scope-overlap on methodology (where gandalf + Matt + legolas Mode A already serve).
- **Team-complexity cost.** Adding an agent adds documentation streams, scope-boundary policing, cross-reference graph growth — exactly the load that's been slowing the team down (per 2026-05-23 morning diagnosis).
- **Already-diagnosed slowdown root cause is documentation/epoch-collision, not capability gap.** New agent doesn't address the actual bottleneck.

### 4.2 Triggers that would justify drafting a dedicated math agent

If any of these emerge, re-open this question:

1. **legolas Mode A consistently fails to ground methodology decisions** — the external-literature path isn't enough, owning seams keep making methodology mistakes even with research backing
2. **Math-hotspot volume becomes continuous** — 10+ methodology-decisions per week instead of 3 per phase
3. **Advanced-math domain emerges that no existing seam plausibly owns** — reinforcement learning for live-balance, advanced causal inference for player-experience attribution, Bayesian-inference frameworks across multiple seams
4. **Pattern of "subtly wrong" output making it through to player-facing surfaces** — Discipline #1.1 fails empirically; we need a math-rigor reviewer in the loop

None of these conditions are imminent for P1-P7 work.

---

## 5. Integration plan (proposed sequencing)

| Step | Owner | Action |
|---|---|---|
| 1 | jack-ryan | Process-side review of this doc — check cross-references, discipline-numbering, scope-creep risk |
| 2 | Matt | Final approval after jack-ryan review |
| 3 | knight-rider | Append Mathematical Layer section to `agentic_orchestration/AGENTS.md` |
| 4 | knight-rider | Append Discipline #1.1 to `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` |
| 5 | knight-rider | Add math-hotspot annotations to both hive-mind-protocol docs (weapon-library-import + QD-engine-rebuild) at the P2/P3/P5 phase entries |
| 6 | knight-rider | Add cross-reference in `canonical/00-ground-state.md` Section 1 (CURRENT) for this doc once it lands as canonical artifact |
| 7 | gandalf | Spot-check integration completeness; close out request |

**Single-commit recommendation:** all five integration edits land in one commit titled `docs: mathematical-seam-naming + discipline #1.1 + math-hotspot annotations per gandalf 2026-05-23`. Discipline-edits-as-batch keeps the working-agreement coherent.

---

## 6. Open questions for Matt (do not block draft acceptance; flag for awareness)

1. **Should this doc be promoted to `canonical/story/` rather than living in `agentic_orchestration/gandalf/notes/`?** It's a working-agreement amendment with cross-cutting impact, which arguably warrants canonical placement. Default: leave in gandalf/notes/ as drafting space; if knight-rider integration lands cleanly, the integrated artifacts in `AGENTS.md` + `engineering-disciplines.md` become canonical, and this doc stays as the historical-rationale record.

2. **Should the named hotspot list be versioned in a single living doc?** As new P-phases are added or methodology requirements emerge, the hotspot list will evolve. Default: this doc § 2 IS the living list; updates land here; integration artifacts cross-reference here.

3. **Should we name the legolas-Mode-A-for-methodology pattern more formally?** Right now it's described in prose. Could be named as a pattern (e.g., "MMC — Methodology Mode-A Consultation") with a template form. Default: prose is fine for now; promote to pattern if usage volume warrants.

---

**Signed:** gandalf (story-and-design steward)
**For:** jack-ryan process-side review → Matt approval → knight-rider integration into AGENTS.md + engineering-disciplines.md + hive-mind-protocol docs. No dedicated mathematician agent; Mathematical Layer named as cross-cutting, distributed across existing seams; bounded math hotspots at P2/P3/P5 guarded by Discipline #1.1.
