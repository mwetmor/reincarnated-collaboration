# Atlas Derivation Charter — the statistically derived kit-space map

> **STATUS:** CURRENT (load-bearing as of 2026-07-14) — see `canonical/00-ground-state.md`

**Date:** 2026-07-14 (authoring session)
**Author:** gandalf (SPEC-AUTHOR; elicited through Matt grill-session 2026-07-14)
**Status:** v1 — canonical lock on the *derivation method + governance*; the map itself (Edition I) is PENDING pipeline execution
**Authority:** Matt 2026-07-14 — "adopted. let's proceed." (following Matt's re-charter: "I simply want the best representation of our ~500 kits that we can possibly have" + rejection of the Q19 grid as governing frame: "we have no reason to believe that those rows/columns should in any way govern the periodic table")
**Companion docs:**
- `canonical/reap-die-rise-engine/coordinate-register-2026-07-13.md` — the 13-coordinate identity key this charter takes as raw input (register lock UNTOUCHED by this charter)
- `canonical/current-to-end-state/projection-atlas.md` — TRIPLE LAW + grain discipline; this charter fills its § 4 "named face" with a derived (not hand-picked) basis
- `agentic_orchestration/gandalf/design-inputs/2026-07-14-atlas-derivation-preregistration.md` — the pinned analysis plan (parameters, gates, decision rule); the executable twin of this charter
- `agentic_orchestration/gandalf/notes/2026-07-11-atlas-chart-renderer-spec.md` — renderer laws (`chart = render(atlas.json)`, determinism, two skins); §2 amended this date to consume the derived basis
- `agentic_orchestration/gandalf/design-inputs/2026-07-13-gaps-kpis-direction-analysis.md` — the Charge A–D analysis this charter partially supersedes (B-as-oracle STRUCK; see § 8)

---

## 0. TL;DR

- **The goal re-chartered (Matt 2026-07-14):** not *predict future builds* — **best possible representation of the ~500-kit corpus**, showing explored vs unexplored space, eventually sim-falsifiable at the coordinate/cell level, serving as **the number-one devlog reference**.
- **SPACE ≠ MAP.** The SPACE is the exact combinatorial feasible lattice (13 coords minus feasibility cuts) — it is enumerated, never estimated. The MAP is a **derived, validated, frozen** low-dimensional projection for navigation — it is earned from the data by a pre-registered statistical pipeline, never hand-picked.
- **No axis is chosen by a human.** MCA/CATPCA + Gower-MDS + Leiden + LCA triangulate; four validation gates (group-recovery, negative-geography, franchise-mixing, bootstrap stability) must pass before the basis freezes as **Edition I**. Axes are named *after* the loadings, never before.
- **Explored vs unexplored is figure-ground:** the full feasible lattice projects into the frozen basis as a ghost field; corpus kits light their ghosts. Unlit ghosts ARE the unexplored space. The denominator is always the enumerated lattice, never the sample.
- **Sim's honest role (settled this session):** corpus kits are descriptors — the sim can only falsify our *reconstruction* of them, so sim-derived identity-KPIs on corpus kits are STRUCK. Sim falsification enters in the **engine-native epoch**, on OUR emitted kits, via Mantel/PERMANOVA tests that indict coordinates or the map itself → numbered Edition bumps.
- **Fallback is honorable:** if no geometry passes the gates, the deliverable is the exact lattice at meso-grain plus the published negative finding. A map that failed validation does not ship as decoration.

---

## 1. The re-charter — what this document exists to serve

**Lineage of the goal (one paragraph, so drift is impossible):** The original charter said *use the periodic table to predict future builds.* Matt 2026-07-14: "I may have sent us down the wrong path… I want to revise my goal and say that I simply want the **best representation of our ~500 kits that we can possibly have**." Requirements attached to the revision:

1. **Explored vs unexplored** must be visible — the view shows what the genre has built against what the space permits.
2. **Sim-falsifiable eventually** — coordinates/cells must be the kind of object a simulation can later indict (engine-native epoch, § 7).
3. **Devlog-primary** — "this view will be the number one reference for my future devlog," so it must be a *clear* representation of kits-in-game vs potentially-explorable space.

And one rejection that shapes everything: the Glance plan view (movement × delivery × amp rows/columns) is "a table with rows and columns… we have no reason to believe that those rows/columns should in any way govern the periodic table/KPI space for kit search/mapping. **I reject this proposal.**" The governing frame must be **derived**, not inherited from governance history.

## 2. SPACE ≠ MAP — the two objects, never conflated

| | **SPACE** | **MAP** |
|---|---|---|
| What | The exact feasible lattice: 13-coordinate combinatorics minus feasibility cuts | A low-dimensional projection of the corpus for navigation + devlog |
| How obtained | **Enumerated** (arithmetic on the register cardinalities + cut classes) | **Derived** (pre-registered statistical pipeline, § 5) |
| Truth status | Ground truth by construction | Hypothesis that survived four gates |
| Changes when | Register changes or a feasibility-cut class is ratified | Only at a numbered **Edition** (§ 6) |
| Failure mode if conflated | — | Map drawn from intuition = decoration; sample mistaken for denominator = false "coverage" claims |

**Feasibility cuts** (what shrinks raw combinatorics to the feasible lattice) come in three ratified classes only:
- **Logical cuts** — combinations incoherent by definition (a coordinate value that presupposes another's absence).
- **Red-law cuts** — the three intrinsic laws from the 38-negative graveyard analysis (co-location violation; anti-synergy; movement-damage carve-out).
- **Taste cuts** — Matt-ratified exclusions, each logged with rationale; never silent.

Every cut class is documented in a feasibility-cuts register (elrond executes; gandalf audits; Matt ratifies taste cuts). Until that register lands, the ghost field (§ 4) simply doesn't render — the map does not wait on it.

## 3. The three-truths state model (what a cell can BE)

Three truth channels, one per source of knowledge:

- **GENRE** — the corpus channel: what the ARPG genre has actually built (470 keyed kits → 457 strict cells).
- **ENGINE** — the expressible channel: what our pipeline can currently emit.
- **ROSTER** — the emitted channel: what exists in OUR game.

A cell's composite state is the triple. The devlog vocabulary derives from it:

| State | Meaning |
|---|---|
| **CLAIMED** | genre built it AND we emitted it |
| **OWED** | genre built it; engine can express it; roster hasn't emitted it yet |
| **NOVEL** | roster emitted it; genre never built it |
| **FRONTIER** | feasible; nobody has built it (genre or us); engine could |
| **SEALED** | cut by red-law/logical/taste — rendered as sealed ground, never blank |
| **UNREACHABLE-YET** | feasible, genre-built or frontier, but engine cannot yet express it |

**Overlays** (orthogonal to the triple): **GRAVEYARD** (a negative corpse lies here — one of the 38), **AMBER** (extrinsic-failure ledger entry; survives from Pushback 1), **CONTESTED** (curation dispute open).

## 4. The ghost field — explored vs unexplored as figure-ground

The single most important devlog property: **the unexplored space is drawn, not implied.**

1. Enumerate the feasible lattice (SPACE).
2. Project **all** of it into the frozen basis as **ghost points** (supplementary projection — standard CA transition formulas; ghosts have zero mass, they cannot bend the axes).
3. Corpus kits **light** their ghosts. Lit vs unlit = explored vs unexplored. Figure-ground, readable at a glance.
4. **Sealed ground** renders as hatched (SEALED cells) — the eye distinguishes *forbidden* from *unvisited*.
5. Per-hex **depth badges** — how many distinct lattice concepts collapse into that hex (the projection is lossy; the badge is honest about it).
6. Every ghost is **clickable to its exact tuple(s)** — the map never replaces the lattice; it links back to it.

**Decoupling law:** the ghost layer is additive. Axes derive from the corpus alone (§ 5); ghosts land whenever the feasibility-cuts register lands. Neither waits on the other.

**Denominator law:** any coverage claim ("we've explored X%") uses the enumerated feasible lattice as denominator. The corpus is never its own denominator.

## 5. The derivation pipeline (summary — the pre-registration is the executable truth)

Full pinned parameters live in `agentic_orchestration/gandalf/design-inputs/2026-07-14-atlas-derivation-preregistration.md`. Summary of the stages and the non-negotiables:

- **Stage 0 — hygiene.** Data snapshot post-curation-batch (A.5). Unknown coordinate values = **passive categories** (contribute no inertia). The 38 negatives are **supplementary-only** — corpses may not shape the axes they're supposed to validate.
- **Stage 1 — diagnostics.** Per-coordinate entropy; pairwise association (Cramér's V + mutual information) with FDR correction; rare categories (n < 10) fused per Greenacre before decomposition.
- **Stage 2 — four method families, triangulated.** (a) **MCA/CATPCA** with Greenacre-corrected inertia + MFA block weighting so no high-cardinality coordinate dominates by arithmetic accident; ordinal constraints on tempo + commit only. (b) **Gower distance → classical MDS.** (c) **Leiden community detection** (kNN graph, k = 10; CPM resolution scan 0.5–2.0). (d) **Latent Class Analysis** (BIC selection, k = 2..12). Agreement across families is evidence; disagreement is a finding, not an embarrassment.
- **Stage 3 — the four gates.** The basis freezes ONLY if all pass:
  - **Gate A — group recovery.** The 6 confirmed cross-franchise groups (WHIRLWIND, TOTEM/SENTRY, TRAP/MINE, CHANNELED BEAM, AURA, MINION/PET) re-emerge without being told: ARI ≥ 0.6; silhouette ≥ 0.2 for ≥ 5/6 groups.
  - **Gate B — negative geography.** The red-law corpses (projected supplementary) cluster where the map says danger lives: permutation p < 0.05 (10k perms).
  - **Gate C — franchise mixing.** The map organizes by *behavior*, not by *game of origin*: PERMANOVA franchise R² ≤ 0.15.
  - **Gate D — stability.** 1000× bootstrap (90% subsample): median kit displacement ≤ 10% of plane diameter. Leave-one-franchise-out + inverse-√franchise reweight: Procrustes ≥ 0.85.
- **Stage 4 — freeze + name.** Passing basis freezes as **Edition I**. Axes are named from the loadings, AFTER derivation — **placeholder names are banned**; the chart carries an inertia-% badge so the projection's explanatory power is always visible.

**Refused methods (permanent):** t-SNE/UMAP as *the map* (nondeterministic, hyperparameter-ruled, unstable under kit addition — fine as exploratory side-views, never the frame); force-directed layouts; hand-picked axes. The Q19 movement × delivery × amp grid is **demoted to a census-dashboard view** — useful table, not the periodic table. (The coordinate-register lock on coords 1–3 as *identity-key membership* stands untouched — this demotion is about the *visualization frame* only.)

## 6. Edition law — frozen frame, versioned occupancy

- The frozen basis is the **frame**. New kits enter by **supplementary projection** (CA transition formulas) — the map does not rearrange under addition.
- **Occupancy changes** (new kit lands, cell lights up, state flips OWED→CLAIMED) = **version** bump. Cheap, frequent, no ceremony.
- **Structure changes** (axis re-derivation, cell merge/split, sealing/unsealing ground) = numbered **Edition** with a changelog. Rare, evidence-gated (§ 7), announced in the devlog as an event.

This is the property that makes the map devlog-safe: readers can learn its geography once and trust it across posts.

## 7. Sim falsification — the engine-native epoch

**What this session settled (do not re-litigate):** corpus kits are *descriptors*, not engine builds. Simming a corpus kit measures our reconstruction-of-a-representation-inside-our-abstraction — three degrees from the kit. Therefore **sim-derived identity-KPIs on corpus kits are STRUCK**, and the B-as-oracle milestone from the 2026-07-13 analysis is STRUCK with them.

**Sim's honest domain:** OUR emitted kits, where the representation IS the kit. When the roster is populated:

- **Mantel test** — map-distance vs sim-behavior-distance on the emitted roster. If nearby-on-map ≠ similar-in-behavior, the map is indicted.
- **PERMANOVA per coordinate** — which coordinates explain behavioral variance? A coordinate explaining ~nothing is indicted as identity-irrelevant → demotion candidate. Large *unexplained* variance → axis-genesis candidate (something real the register doesn't key).
- Either indictment, if ratified, fires **Edition II** with a changelog naming exactly what the sim falsified.

This satisfies the re-charter's requirement (b): cells become sim-falsifiable *objects* — in the epoch where the sim measures the real thing.

## 8. Governance deltas (what this charter changes, precisely)

1. **B-as-oracle STRUCK** — the 2026-07-13 analysis § B.5 milestone (shape-differential acceptance test at frozen tuning as KPI oracle for corpus kits) is struck per § 7. Shape-telemetry survives ONLY as balance-loop exhaust on emitted kits. *(Partial supersession of the Charge-B analysis; banner goes on the design-input at next touch — it is a design-input note, not canon, so no in-place fold is owed.)*
2. **Goal re-charter** — prediction → representation, per § 1. All downstream language ("predict future builds") is retired.
3. **Q19 plane demoted** — census-dashboard view, not the governing frame (§ 5). Register lock on coords 1–3 as identity-key membership UNTOUCHED.
4. **K1-freeze-spec PARKED** — the K1–K6 KPI vector work from Charge B parks until the engine-native epoch; K-vector semantics on corpus kits died with B-as-oracle.
5. **Pushback 1 amber gate SURVIVES** — the extrinsic-failure amber ledger and its curation gate are unaffected; AMBER is an overlay in § 3.
6. **Legolas feel-layer commission REGISTERED** — Matt's grill point 3 (build guides carry usage/feel information no sim reaches) becomes a Mode-A commission: harvest feel/usage annotations from build-guide prose onto corpus kits as a *soft layer* (never axis input; candidate overlay + naming input). Queued behind the derivation run.

## 9. Seam map + sequencing

| Seam | Role |
|---|---|
| **gandalf** | Pre-registration author (SPEC-AUTHOR); reads results as DRIFT-CRITIC; names axes from loadings; authors Edition changelogs |
| **elrond** | Executes the pipeline against the corpus DB (Stage 0–3); produces the gate report; **no interpretation** — numbers return, gandalf reads them |
| **jack-ryan** | Gate-1 methodology review of the pre-registration BEFORE execution (pre-registration is only binding if reviewed before results exist) |
| **star-lord / drax / galadriel** | Renderer seams unchanged — `chart = render(atlas.json)`; atlas.json plane block gains derived-basis + edition fields (renderer spec § 2 amendment) |
| **KR** | Sequences the dispatches |
| **Matt** | Ratifies Edition I freeze; ratifies taste cuts; rules on any gate-failure fallback |

**Fire order:** (1) jack-ryan Gate-1 on the pre-registration → (2) elrond curation batch A.5 (the data snapshot) → (3) elrond executes pipeline → (4) gates evaluated → (5) Edition I freeze + axis naming (Matt ratifies) → (6) ghost field lands when feasibility-cuts register lands → (7) renderer consumes.

## 10. Fallback clause (pre-committed, so failure is cheap)

If no geometry passes all four gates: **the deliverable is the exact lattice at meso-grain** (register rollup), rendered as the census dashboard, plus a published negative finding: *"the corpus does not support a stable low-dimensional behavioral map at this sample size — here is what it DOES support."* That is an honest devlog post. What is banned is shipping a failed map as decoration.

---

## 11. Cross-references

- `canonical/reap-die-rise-engine/coordinate-register-2026-07-13.md` — input register (LOCKED skeleton coords 1–3; never-demote core #2/#5/#8/#1/#12/#13)
- `canonical/current-to-end-state/projection-atlas.md` § 4 — named face now derives per this charter (amended this date)
- `agentic_orchestration/gandalf/design-inputs/2026-07-14-atlas-derivation-preregistration.md` — pinned parameters (the executable twin)
- `agentic_orchestration/gandalf/design-inputs/2026-07-13-gaps-kpis-direction-analysis.md` — Charge A–D lineage; § B.5 struck per § 8.1
- `agentic_orchestration/gandalf/notes/2026-07-11-atlas-chart-renderer-spec.md` — renderer laws; § 2 second banner this date
- `canonical/matt_decision_needed/2026-07-13-ip-clearance-devlog-and-hook-surface.md` — the devlog surface this map publishes into (two mandatory IP conditions apply to any player-facing render)
- Decisions-log entry owed: `2026-07-14: Atlas derivation charter adopted (representation re-charter; sim-KPI strike; derived-basis map)` — KR drafts, jack-ryan reviews per standing protocol

Tracker-delta: new spec doc + 4 amendments → current-to-end-state-engine.md SESSION-DELTA 2026-07-14 (B-as-oracle struck; derivation pipeline owed as new gap; Q19 plane demoted; K1 parked; feel-layer commission queued)

---

**Signed:** gandalf (SPEC-AUTHOR)
**For:** locking the method by which the kit-space map is derived, validated, frozen, and falsified — so the number-one devlog reference is earned from the data, never drawn from intuition.
