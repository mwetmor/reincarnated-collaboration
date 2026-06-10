# Engine Architecture Canonical Synthesis — Fable-5 Phase 1

> **STATUS:** CURRENT pending Gate-1 critique-pair review (Matt + jack-ryan) per Discipline #51 (`~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` #51 — synthesis-draft adversarial critique before canonical status firms)
>
> **Date:** 2026-06-10
> **Author:** gandalf (story-and-design steward)
> **Authority:** Matt 2026-06-10 ratification of refined 3-part Fable-5 test, Phase 1 — Engine Architecture Canonical Synthesis mission
> **Discipline anchors:** canonical-source-consultation declaration at `agentic_orchestration/gandalf/notes/2026-06-10-fable-5-canonical-synthesis-source-consultation-checklist.md` (committed + pushed before source reads fired; all 33 checkboxes marked before this doc was authored); per-block read distillations at `agentic_orchestration/gandalf/notes/2026-06-10-fable-5-synthesis-working-notes.md`

---

## 1. Purpose

This document is a **RECOGNITION of the engine's current canonical architecture, not new design.** It synthesizes the architecture distributed across ~33 canonical sources into one reference surface, with the authority chain visible at every claim. It exists so that:

1. Downstream consumers (specialists, Fable-5 Phase 2 rocket track, PC-seam team, future sessions) have a single orientation surface instead of a 33-doc walk.
2. Cross-doc lineage (supersession chains, amendment passes, vocabulary layers) is stated once, explicitly, rather than re-derived per session.
3. Gaps and deferred commitments are enumerated in one register (§ 9) with their empirical re-engagement criteria, per recognition-validate-commit discipline.

**What this doc is NOT:** it is not a supersession of any source. Source docs remain authoritative; where this synthesis and a source diverge, **the source wins** and the divergence is a defect in this synthesis. No claim below is authored from ground-state-oracle one-liners or session memory; every architectural claim cites a source read in full (consultation declaration, checklist § 0 commitment).

**Scope framing (the three-sentence orientation):** the engine is a **substrate-led serial-content production system** (Variant C; `canonical/37-engine-and-game-two-products.md`; `canonical/story/engine-as-general-serial-content-product-2026-05-22.md`) that derives all player-facing content from a registry of atomic primitives (§ 3), runs it through an 8-phase generation-simulation-cohesion pipeline (§ 4) under a bounded-viability damage architecture (§ 5), and surfaces it to the player through the cosmograph creation moment (§ 6). Engine build completion criterion and cycle partitioning are tracked operationally at `canonical/02-roadmap.md` § 6.6 (Cycle 14 = Phase 5; Cycle 15 = Phase 6; Cycle 16 = Phases 7+8 → REINCARNATED-GAME UNLOCK).

---

## 2. Source canonical authority

Full enumeration with read-scope is at the consultation checklist (path in header). The authority spine, by architectural domain:

| Domain | Authoritative source(s) |
|---|---|
| Layer architecture (primitives → derivation) | `canonical/story/2026-06-06-atomic-substrate-registry.md`; `canonical/story/2026-05-31-hypothesis-flow-pattern-library-architecture.md` — "together constitute the cemented future-state architecture" (registry § 0/§ 7) |
| BC axes + archive geometry | `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` |
| Convergence algorithm | `canonical/story/multi-dim-convergence-algorithm-2026-05-21.md` (v1.1) |
| Skill + attribute systems | `canonical/story/skill-system-2026-05-24.md`; `canonical/story/attribute-system-2026-05-24.md` |
| End-to-end workflow (the WHAT) | `canonical/39-qd-engine-end-to-end-workflow-2026-05-24.md` (Architecture B base) |
| Execution status (the HOW-FAR) | `canonical/02-roadmap.md` (relationship per its § 7) |
| Gear + balance architecture | `canonical/40-gear-balance-guide-architecture-2026-05-26.md` (D1–D86); `canonical/42…45` wave-intent docs; `canonical/46-concentration-architecture-2026-05-27.md` |
| Damage + scaling | `canonical/47-damage-scaling-architecture-2026-05-27.md` (v1.2); `canonical/50-bounded-viability-with-specialization-design-directive-2026-05-28.md`; `canonical/51-investment-scaling-6-pattern-architecture-2026-05-28.md` (v1.2) |
| Progression | `canonical/41-progression-framework-2026-05-27.md` |
| Creation moment | `canonical/story/2026-06-05-cosmograph-pivot.md` (+§ 9/§ 10); `canonical/story/2026-06-07-earth-avatar-cosmograph-creation-moment-architecture.md` (+§ 11/§ 12); `canonical/story/2026-06-09-tal-rasha-glyphic-primitive-anchor-architecture-recognition.md` |
| Strategic frame | `canonical/37-engine-and-game-two-products.md`; `canonical/38-downstream-delivery-strategy-2026-05-23.md`; `canonical/story/engine-as-general-serial-content-product-2026-05-22.md` |
| Substrate-led discipline lineage | `canonical/story/legacy-categorical-cleanup-audit-2026-05-22.md`; `canonical/story/2026-05-29-designer-writes-substrate-player-names-experience-principle.md` |
| Content-release architecture | `canonical/story/2026-06-02-season-archive-realm-expansion-pivot.md` |
| Weapon substrate | `canonical/story/2026-05-23-weapon-substrate-conclusion-declaration.md` (v1.0 lock); `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` (D1–D7) |
| Genre baselines | `canonical/story/2026-06-09-arpg-physical-magical-ratio-baseline.md` |
| Disciplines + decisions | `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`; `~/Games/reincarnated-engine/design/decisions/decisions-log.md` |

**Reading rule for this synthesis:** strategic-frame docs (37, Variant-C story doc) are cited for their strategic commitments, NOT their operational-state snapshots — both predate the Architecture-B lock, the season-archival pivot, and the Pattern 4-6 retirements. This is supersession-by-refinement, not contradiction (working-notes Block D flags 1-2).

---

## 3. Layer architecture

### 3.1 Layer 0 — atomic substrate (20 primitive families)

Per `canonical/story/2026-06-06-atomic-substrate-registry.md` § 2: the engine's generative ground truth is **20 atomic primitive families**, including: 8 elements (canonical-7 + physical, with STR/INT/WIS scaling coupling per element; DEX has no native element coupling) (§ 2.1); per-primary flavor pools (§ 2.2 — Architecture A LOCKED: 7 rotating primaries = 100 entries + physical taxonomy-sibling 9 = 109, per decisions-log 2026-06 flavor-pool lock); 4 attributes STR/INT/WIS/DEX with VIT deferred (§ 2.3; `canonical/story/attribute-system-2026-05-24.md` § 0–§ 1); T4 strategies (§ 2.4; counts are layered vocabulary — see § 5.4); 16 skill-geometry palette (§ 2.5); skill-tree-position tuples (§ 2.6); scaling patterns (§ 2.7); chain architecture (§ 2.8); 6 investment-scaling patterns (§ 2.9; `canonical/51…` as source); 5 resource models (§ 2.10); ~200 weapon-form tokens (§ 2.11); the 89,839-row weapon substrate (§ 2.12); off-hand parallel substrate (§ 2.13); race/racial-trait schemas — schema-only, per-season authoring (§ 2.14); plus remaining families through § 2.20.

### 3.2 Layer 0.5 — combinatory operators

5 operators (registry § 3), including the **seasonal-substrate-rotation operator** (§ 3.5): single-axis rotation default with multi-axis escape hatch, ≥1 axis held for continuity across seasons.

### 3.3 Layer 1 — derivation chains

Kits, skills, and gear derive from Layer 0 primitives via documented chains (registry § 4). **Nothing player-facing exists that does not trace to a Layer 0 family.** This is the operational form of the substrate-led discipline (`canonical/story/legacy-categorical-cleanup-audit-2026-05-22.md` — six categorical-pre-imposition retirements; audit principle § 1.3; Discipline #41).

### 3.4 Layer 2 — experiential axes

Per `canonical/story/2026-05-31-hypothesis-flow-pattern-library-architecture.md` § 1.8 (iteration 4): **identity axes** (Target-Pattern; Depth-vs-Breadth) vs **viability axes** (Survivability/Playability; Leveling hypothesis § 1.8.5 pending playtest); Mode axis REMOVED (iter 6, § 4.17 note); cell shapes SPECIALIZED / HYBRID / GENERALIST / ANTI_SPECIALIZATION (§ 4.16). The creation-moment § 12 addendum (`canonical/story/2026-06-07-earth-avatar…` § 12) recognizes the primitive layer as two-layer — Layer 0 atomic + Layer 2 experiential — at the player-input surface.

### 3.5 Naming layer (N1–N4)

LLM-generated naming is **downstream of engine substrate, never in it** (registry § 5). Per-skill bounded flavor judgment (hypothesis-flow § 1.7): single-element 3-option {primary/sub/blend}; hybrid 15-option subset; kit identity is primary-element only, flavor is per-skill naming (`canonical/story/2026-06-02-season-archive-realm-expansion-pivot.md` § 3.2, Matt verbatim). Emergent kit concepts emerge, never declared (hypothesis-flow § 1.7). LLM naming placement: Option A — Phase 5+, AFTER Pareto reduction (~30 kits; hypothesis-flow § 1.7.8 iteration-5 lock).

### 3.6 BC axes + archive geometry

Per `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` § 2: **8 mechanical-BC axes, 68,040 cells** (Engagement 6 × Geometry 5 × Proxy-density 3 × Control-density 3 × Tempo 3 × Amplitude-variance 3 × Defensive 4 × Resource-economy 7). Mechanical BC only (§ 1.3) — cohesion BC (LLM-judge) and visual BC (CV) are separate archives on the same MAP-Elites machinery. Hybrid archetypes are cross-axis cell addresses, not dedicated bins (§ 4). Profile A operational archive = 25,920 cells after the sim-deferral matrix (§ 5, § 10.3). 5× substrate-variety rule per bin (§ 6); all thresholds require Discipline #17 empirical calibration pre-production (§ 9). **Pattern 6 caveat carries:** BC axes survive as measurement axes pending post-axis-discovery revisit (`legacy-categorical-cleanup-audit` § 4.2).

### 3.7 Hypothesis-flow validation loop (the cemented future-state)

Per hypothesis-flow § 2: a **6-stage closed loop** — hypothesis (community-research-led) → engineer generation → manifest in Unreal → playtest at 3+ power planes → graduate → encode. Cell statuses PROVISIONAL → … → LIBRARY-LOCKED (§ 6.6); **only LIBRARY-LOCKED cells enter generation logic.** Discipline #41 binds the validation step, not the engineering step (§ 1.2). Discipline #41.x extends this: designer-asserted validation metrics (KPMs, BVV thresholds, cohort taxonomy) are PROVISIONAL hypotheses until playtest-validated (engineering-disciplines #41.x; decisions-log Wave-5 swift-closure — `provisional_pending_playtest_validation=True` on gauntlet metrics).

### 3.8 Lineage note — Architecture A → Architecture B

`canonical/story/multi-dim-convergence-algorithm-2026-05-21.md` § 6 framed Phase 2 as substrate-AGNOSTIC; `canonical/story/skill-system-2026-05-24.md` § 13 + `canonical/39…` lock **Architecture B: substrate-BOUND at Phase 2** (weapon + secondary pulled at generation; cultural-tradition/period/named-bearer signals available from Phase 2 onward). This is lineage supersession, not contradiction: A4's substrate-as-cohesion principle **survives at the convergence-input layer** — mechanical convergence remains element-blind; binding ≠ convergence input (doc 39 § 2.3 substrate-led discipline preservation). Architecture A is retained as developer-tool/R&D reference only (`canonical/37…` 2026-05-24 amendment header).

---

## 4. Generation pipeline (8-phase workflow + content lifecycle)

### 4.1 The 8 phases (doc 39 § 5.1–§ 5.8; execution status per roadmap § 3)

| Phase | What (doc 39 §) | Execution status (roadmap § 3, 2026-06-10) |
|---|---|---|
| 1 — Archive State Inspection | § 5.1 | ⏳ (progression-node coverage check ❌ NEW) |
| 2 — Generation: substrate-bound + multi-T4 + spec-driven gear | § 5.2 | 2a kit composition: 3-or-4-chain locked; max-8-active ❌. 2b T4 algorithm ⚠️ (6 v1 strategies committed; BC-shift sweep FAILED Cycle 11; Tier-2 ratified ships-as-intent-metadata). 2c substrate binding ⏳ (Options α/β/C ✅). 2d spec-driven gear gen ❌ ALL NEW. 2e coherence+faction ⏳ |
| 3 — Convergence + mechanical measurement + multi-T4 sim + playability gate | § 5.3 | ⏳ (8 BC axes ✅; W1.13 H1-H5 🔒 DEFERRED; playability gate D61 ❌; multi-T4 sim methodology D84 ❌) |
| 4 — Mechanical Archive Insertion | § 5.4 | ⏳ (Pareto/crowding/Mahalanobis/KL ✅; multi-T4 entries ❌) |
| 5 — Cohesion Coalescence | § 5.5 | ❌ [CYCLE 14] (bi-modal assignment ✅; spirit-guide data-oracle D28–D32 ❌; T4-attuned gear cohesion ❌; acquisition curve D21 ❌) |
| 6 — Visual Coalescence | § 5.6 | ⏳ [CYCLE 15] (image-pass-through-to-Meshy ✅; polearm items 🔒 v1.1+) |
| 7 — Joint-Gate Evaluation | § 5.7 | 🔄 [CYCLE 16] |
| 8 — Profile Assembly + Export | § 5.8 | ⏳ [CYCLE 16] (loadout M3/M4/M6 ✅ Cycle 11; M1/M2/M5 ❌ gated) |

The **six-step content lifecycle** (doc 39 § 0.5) is the one-way dependency chain the 8 phases execute inside; no circular dependency (§ 0.5.2). Architecture-switch empirical triggers are registered at doc 39 § 4 — Architecture B holds by default (§ 4.3).

### 4.2 Convergence algorithm (Phase 3 mathematical core)

Per `canonical/story/multi-dim-convergence-algorithm-2026-05-21.md`: scalar-modifier-only optimization is **mathematically underdetermined** for the 5-tier WR contract (1 unknown vs 5 constraints; § 2.2; dual-witness empirical mandate § 1.2). Convergence is therefore **5-6 dimensional** (§ 5): per-node SP (120 budget, cap 15) × T4 keystone discrete selection × trigger-interaction discrete selection × tier-specific coefficients (1.05–1.25, LOAD-BEARING per § 2.3) × scalar modifier × gear-affix vector (provisional). Components (§ 4): WR-skew gradient; multi-tier voting with tier-axis sensitivity matrix; soft-preference penalties (UX shows hard gates, engine optimizes smoothly); random-restart; Tier-1 L1-playability invariant (§ 4.6, Matt 2026-05-21). v1 = 10-15 nodes / 2-4 chains substrate-driven; v2 canonical-parity target 24-30 nodes / 3-5 chains (§ 8.3).

### 4.3 Skill + attribute systems (Phase 2 generative surfaces)

Skill = (element, geometry, tempo, amplitude) × tier_coefficient + [special_effect if T4] + placeholder_name (`skill-system-2026-05-24.md` § 1); 10-15 node small tree (§ 2); passives mechanic-altering only (§ 3); synergy via adjacent-axis-overlap ω-field in tree adjacency (§ 5). **Algorithmic mechanic-alteration is the V1 T4 deliverable and the Variant-C differentiator** (§ 8 + § 8.5): engine derives regime-changes per kit's BC-axis space; 11-type regime-change palette (§ 7); spirit-guide templated explainer converts cognitive load into story win (§ 9; D7-compliant). Faction-generated proxies draw from the bound weapon's cultural-tradition + period (§ 8.6). Attributes: STR/INT/WIS/DEX, VIT deferred (`attribute-system-2026-05-24.md` § 0–§ 1); element-attribute coupling § 2; 4-tuple BC-target subspace 108 cells (§ 4).

### 4.4 Weapon substrate (the generative library Phase 2 binds against)

- **v1.0 CONCLUDED** 2026-05-23 (`canonical/story/2026-05-23-weapon-substrate-conclusion-declaration.md`): 125 clusters at k=3 axis basis, mean lineage purity 0.9444, full 48,430-row clustered coverage; all 125 canonically labeled. Conclusion is explicitly NOT a ship gate, NOT a faction-architecture commitment, NOT a k=3 taxonomy lock; residual contamination is handled at consumption time via Discipline #25 semantic-layer rep-audit.
- **Composition policy v1 D1–D7 LOCKED** 2026-05-24 (`canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md`): genre filter `genre IN ('fantasy','mythological','historical')`; tiered promotion (D1a Tier-S handheld auto-promote 449; estimated v1_scope ~1,700–3,100 — **actual locked at 2,293** per roadmap § 3, within estimate, tag `v1.0-weapon-substrate-cycle-10-shipped`); cell-matching Options α (martial 5-tuple) / β (caster attribute-level) / C (cross-attribute ω-penalty), all implemented per roadmap § 3 Phase 2c; register weights (historical 50-55% / fantasy 30-35% / military_modern 5-8%); **bi-modal form library** ~32% named-personage / ~68% engine-original with UNIFORM player-facing presentation; 12 Sketch-F anchors under **§ 5.4 probabilistic-not-enforced sampling** (Matt 2026-05-25 verbatim: forcing personages "may diminish the uniqueness across seasons"); Tier-3 living-religious/marginalized excluded from v1 LLM-naming.
- Named-bearer 3-tier attribution + nested mythology per `skill-system-2026-05-24.md` § 12.3–§ 12.4.

### 4.5 Gear generation (Phase 2d; Cycle 13 wave-intent chain)

The Wave 1→4 intent chain operationalizes doc 40's gear blocks:

- **Wave 1 partition substrate** (`canonical/42…` ): 9-category × 11-slot affinity matrix with relative tier weights (§ 2.1, § 9.2); per-rarity grid Common 1-2 mods → Legendary T2 highest density (§ 3); tier-restriction as separate per-modifier constraint (§ 4); 6 locked principles (§ 6); SC-4 five methodology gates closed (§ 7).
- **Wave 2 T4 algorithm** (`canonical/43…`): 3-category T4 taxonomy (A class-mechanical character-wide + exactly one of B chain-multiplicative XOR C chain-element-conversion/addition; § 2); DUAL_ELEMENT_ADDITION new (§ 3); two-pass compositional synergy scan, no LLM raw-reasoning per D7 (§ 5); Option F 4-phase retry with ≥1 in-band T4 minimum (§ 6); degenerate Patterns 9+10 (§ 7); T4 count = chain_count − 1 per D83 (§ 9).
- **Wave 3 scope dimension** (`canonical/44…`): `T4Scope` CHARACTER_WIDE / CHAIN_WIDE_OWN / CHAIN_WIDE_PARALLEL (§ 2) — doc 40 § 8.2's named "variance generator / biggest design risk"; Category A fixed character-wide (Disc #31 separability guard); 6-step selection with cohort priors + scope-trap synergy catalogs + `1/sqrt(class_chain_count)` magnitude downscale (§ 4); T4CandidateV2 field-addition, no V3 bifurcation (§ 8.5).
- **Wave 4 spec-driven gear gen** (`canonical/45…`): scored-candidate strategy registry mirroring the T4 algorithm at gear-instance layer (doc 40 § 3 D7); **substrate-bound — samples from Wave-1 partition pool; LLM permitted ONLY for player-facing naming** (§ 2.2, § 5.5); all 10 `PartitionRarity` tiers (§ 3.1); uniques = metadata flag sub-pool of legendary (§ 3.2; doc 40 D49+D53); T4-attunement = content-compositional metadata, never toggles (§ 4; doc 40 D33+D38+D51 amended); triggered-passive added skills per D55 with true-active weapons-only ≤~1.5% T2 additive to flat-8 budget per D57 (§ 5); D56 modifier-surface expansion — pure-numerical-escalation legendary is ANTI-PATTERN (§ 6); capability toolkit legendary-exclusive, 6-category enum incl. MULTIPLICATIVE (§ 7); 4-piece set atomicity, endgame-exclusive per D48 (§ 8).

### 4.6 Progression frame (the level/tier scaffold the pipeline calibrates against)

Per `canonical/41-progression-framework-2026-05-27.md`: **L50 hybrid** — light leveling L1-50 + content-tier endgame; 70-point endgame skill budget; NO paragon infinite leveling; post-cap progression = gear tiers T0→T0.5→T1→T2 (D50) + chain investment + T4 unlock + sets + respec-with-legendary-trigger (D65). 4 progression nodes → level bands (Early L1-15/T0 … Endgame L45-50+/T1+T2) with KPM anchor intents ~20-30 → 75+. Season cardinality default n_kits=40 (cap 50) per § 4.6.

### 4.7 Content-release architecture

Per `canonical/story/2026-06-02-season-archive-realm-expansion-pivot.md`: the **season as content-release unit is ARCHIVED** (Matt 2026-06-02). Kits emit into a continuously-growing kit space with stable kit-ids; **Realm Expansion** (new Maps/Acts/Game Modes) is the release mechanism, telemetry-targetable at underplayed kit groupings; ascension is player-driven strategic choice (no forced resets / no FOMO). The seasonal journey is PRESERVED at the narrative layer, decoupled from release schedule (§ 1.4) — this reconciles the Variant-C profile flag `seasonal_journey_narrative_structure` (`engine-as-general-serial-content-product` § 3) with the archival. Conscious genre departure from PoE-league/D4-season conventions, RATIFIED deliberate (§ 4).

---

## 5. Damage + scaling architecture

### 5.1 Bounded viability with specialization (Path α — the governing directive)

Per `canonical/50-bounded-viability-with-specialization-design-directive-2026-05-28.md` § 4, five operationalized targets:

| Target | Criterion (doc 50 §) |
|---|---|
| 1 | Base DPS variance ≤1.5× across 4 damage-scaling paths (§ 4.1) |
| 2 | Every kit non-zero KPM on every encounter type (§ 4.2) |
| 3 | No kit saturates the KPM ceiling on any encounter type (§ 4.3) |
| 4 | Specialization: each kit ~1.5-2× cohort median on 1-2 encounter types (§ 4.4) |
| 5 | No kit <30% cohort median on any encounter type (§ 4.5) |

Together: every kit performs in [30%, 200%] of cohort median across encounter types, with designed peaks (doc 50 § 4.5 composition note). Path β REJECTED (§ 6; 365× imbalance would ship); β-FULL Option 6 REJECTED + Gate-5 D2 Option 6 RETROACTIVELY RETRACTED (decisions-log Path-α ratification arc; Discipline #40 case (c) fourth iteration). Discipline #47 makes the 5 targets the enforcement criterion — threshold relaxation requires Matt ratification.

**Path α v1 closure state** (`canonical/51…` § 10.8.10 + doc 50 § 4.7 v1.3): close-criterion vocabulary renamed C1-C5; closure at 4/4 = C1 (cross-path DPS equity ≤1.5× at BASE CONTEXT / DDA-off, Matt A1 election) + C2 (zero_count=0) + C3 (saturation_count=0) + C5 (no cell <30% cohort median); **C4 (Secondary-T4 cohort peaks) DROPPED from v1, deferred to Cycle 16+ BC-axis expansion**. Path α v1 closure ≠ Cycle 14 v1 MVP closure (Disc #42 Instance 4).

### 5.2 Three-path damage routing + substrate-carries-magnitude

Per `canonical/47-damage-scaling-architecture-2026-05-27.md` (v1.2): three-path damage routing with v1.2 amendments at § 4.5 + § 4.6. Every skill declares `damage_scaling_type` physical/magical/hybrid (Discipline #38; flat weapon-damage for magical skills FORBIDDEN; weapon-as-conduit for casters). Path A substrate-carries-magnitude: `base_physical_damage_l50 = family_baseline × amplitude_mean` with the Pass-2 LUT (177/99/91/31/31 entries) — substrate supplies magnitude, confirming doc 47 § 4.2 consumption (decisions-log Path-A arc).

### 5.3 Two-layer T4 composition (strip-and-ship)

Per doc 47 § 4.6 + `canonical/51…` § 10.7.8/§ 10.8.9: **Primary T4 universal slot** (DIRECT_DAMAGE_AMPLIFICATION; never stripped; delivers doc 50 Target-4 universal-satisfaction guarantee per doc 47 § 4.6.4 proof) + **Layer 2 strategy slots** (6 strategies cycle; strip-and-ship exercises on Layer 2 only). **Kit ships UNIVERSALLY** (`ship_kit(K)` always fires); Layer-2 zero-in-band is honest empirical signal, does not block ship (doc 51 § 10.8.9, superseding § 10.8.5 escalation). DIRECT_DAMAGE_AMPLIFICATION is a **Discipline #39 Mode B scaffold with EXPLICIT CYCLE 15 RETIREMENT COMMIT** (Matt D5 ratification, recorded at doc 50 § 4.7 v1.2 cross-reference) — natural mechanics replace the placeholder at Cycle 15 (§ 9 entry).

### 5.4 T4 strategy-count vocabulary (the layer-separation table)

The apparent count divergence (6 / 7 / 11 / 21 / 3-category / C1-C5) is **layered vocabulary, not contradiction** — canonically disambiguated at doc 47 § 4.6.9:

| Count | Layer | Source |
|---|---|---|
| 3 categories (A / B-XOR-C) | Player-facing + design-spec | doc 40; doc 43 § 2 |
| 7 active strategies (6 + DUAL_ELEMENT_ADDITION) | Operational algorithm registry | doc 47 § 4.6.2 |
| 11 regime-change palette types | Mechanic-alteration palette (WHAT alterations exist) | skill-system § 7 |
| 21 proposed | Future-expansion register | doc 47 § 11 (registry § 2.4 cites as such) |
| C1-C5 | Path-α measurement layer | doc 51 § 10.8.10 |

### 5.5 Investment scaling + concentration

- **6 investment-scaling patterns** (`canonical/51…`; registered as Layer-0 family at registry § 2.9); investment scaling caps at multiplier=1.0 at max — super-peaks from investment are formally impossible (doc 50 § 4.7 citing doc 51 § 7.2 proof); specialization peaks emerge from `base_at_max` distribution, not investment scaling.
- **9-layer concentration architecture** (`canonical/46…`): through-line = **concentration over distribution** (§ 1; genre-canonical § 1.3; anti-pattern = Cycle 13's ~22-alteration capability-soup per Discipline #34). Layers: 1 stat-range bounds (§ 2 — the prerequisite; bounded-stat cap table enforced generation-time AND runtime per Discipline #33); 2 affix migration (§ 3); 3 capability scope reduction (§ 4); 4 trigger-condition vocabulary expansion (§ 5); 5 concentration probability table by tier (§ 6 — expected endgame 2-6 build-defining items per Discipline #34); 6 cohesion-judge layered architecture (§ 7 — identity weighted T1>T2>T3 chain, gear LOW additive nod, per Discipline #35); 7 compositional synergy scan amendment (§ 8 — thematic seeds encouraged Pass 1, redundancy filtered Pass 2); 8 set keying to T4-strategy × element clusters (§ 9 — cross-kit shareable, ~12-20/season, per Discipline #36; per-character set_id RETIRED); 9 class-agnostic spec-driven per-drop generation (§ 10 — per Discipline #37; smart-loot rejected per D21 Option A).

### 5.6 Genre-baseline calibration

Per `canonical/story/2026-06-09-arpg-physical-magical-ratio-baseline.md`: empirical 8-ARPG baseline — physical-primary central 37-40% (range 32-47%); **Reincarnated target band 38-45% physical (central 40%)**; watch flags >48% / <32% / hybrid >25% or <10%. Current corpus 43% = within spec at upper boundary; monitor, no action. Compatible with Discipline #57's 40-45%/55-60% Option-B4 generation target (distinct provenance; both satisfied at 43%). Classification rule: PRIMARY scaling path classifies; aligns with doc 47 `damage_scaling_type`.

---

## 6. Player-facing creation moment

### 6.1 Current frame (the lineage chain, most-recent-lock last)

The creation-moment architecture evolved through explicit supersession-by-refinement; the **current frame is `canonical/story/2026-06-07-earth-avatar-cosmograph-creation-moment-architecture.md` § 12 (2026-06-10 addendum — the most recent canonical lock in the corpus)**, with this lineage:

1. **Cosmograph pivot** (`canonical/story/2026-06-05-cosmograph-pivot.md`): creation surface = interactive force-directed cosmograph, NOT Veo cinematic (4 Veo iterations exposed training-bias failure modes § 1-§ 2); lasso interaction defeats blank-canvas paralysis (§ 2.3).
2. **§ 9 amendment**: stars = Layer-0 primitives; constellations = kits; brightest stars = BDI-β-driving primitives; ~1000 simulated PROVISIONAL constellations, no LLM names per D7; UMAP/t-SNE projection; lasso composite_score formula (§ 9 DP4).
3. **§ 10 amendment (Tal Rasha Branch A)**: primitive-anchors = archaic GLYPHS at the cross-group anchor layer (in-constellation stars-as-primitives preserved); visual register LOCKED (large atmospheric, light-edge brush-stroke, monochromatic, drawn-by-light); 6-group rune scaffold PROTOTYPE; two-tier selection pattern locked. Source recognition: `canonical/story/2026-06-09-tal-rasha-glyphic-primitive-anchor-architecture-recognition.md` (Branch A fired; Branch B retired).
4. **Earth-avatar scene lock** (creation-moment doc): Earth avatar on hill + ambiguous spirit form + **the cosmograph IS the night sky (literal, in-fiction)**; spherical-shell geometry with LOD 0-2; dual-path LOCKED — Path L (lasso; jump-in) + Path I (drop ingredients; take-time), same substrate + convergence; ambiguous spirit form = continuous feedback canvas; materialization cinematic at confirm. Earth-Self meta-layer ANCHORED at first creation moment (§ 3.4); ambiguous form = spirit-guide-in-becoming (§ 3.5).
5. **§ 11 addendum**: two-layer + buffer-space (Layer 1 glyph atmospheric-symbolic "what is this spirit MADE OF" / Layer 2 constellation figurative "what spirit am I BECOMING"); **"Sign" semantic overloading locked as player-facing vocabulary anchor**; Path-I two-tier precursor pattern; seasonal glyph-system rotation pattern.
6. **§ 12 addendum (CURRENT):** spirit-guide-driven elicitation cascade + cycling-preview UX + iPad-text/sky-runes split. Load-bearing recognitions: INPUT primitives (player selects: race / element / weapon-form / style / loot-focus / progression-stage / T4-direction) vs OUTPUT primitives (engine emerges the rest); player NAMES the precedent ("What is most important for your journey this season?" — Disc #41-coherent, no designer-imposed universal precedent); **runes in sky are the ONLY iconography** (~80 per-primitive icons RETIRED; 29 placeholders REMOVED, not replaced); canonical 7 Tier-1 anchors (§ 12.3: Race/ancestry, Element/flow, Weapon/craft, Power/mastery, Style/way, Harvest/rewards, Horizon/goal); cycling ≠ committing, guide silent during cycling (§ 12.4); 3-5 layer nested cascade → nearest-kit-centroid lookup → "Accept this form, or refine?" (§ 12.5); substrate-truth-wins pre-display filtering (§ 12.7); all guide voices templated per D7 + doc 40 D28-D32 (§ 12.9). Matt ratification verbatim: "yes, ratify all three and author the addendum."

The § 10 6-group scaffold vs § 12 7-anchor structure is not a contradiction: group lock was already DEFERRED to Pattern B at § 10; § 12 extends with Layer-2 experiential anchors. The Elements-anchor categorical-distinction constraint carries forward to any future lock (cosmograph-pivot § 10).

### 6.2 Runtime boundary (load-bearing for § 8)

Per cosmograph-pivot § 4.1: **engine pre-generates offline** (kit_archive.db → JSON packet); the game-side runtime does **LOOKUP** — nearest pre-generated character to the lassoed/cascaded centroid — NOT generation. Honest to Architecture B.

### 6.3 P4 — creation-moment memorability

The creation moment is a measured experiential axis: P4 in the hypothesis-flow mathematical cell schema is remapped Reincarnated-specific to creation-moment memorability (hypothesis-flow § 1.3.1), validated at playtest Layer 3 (§ 6.0).

---

## 7. Cross-cutting disciplines

The authoritative corpus is `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (per-discipline detail there; thematic map here):

- **The architectural spine:** #41 pre-authored taxonomy interrogation ("can this emerge from the substrate?") + #41.x (validation metrics are provisional until playtest) + #45 generative-architecture vocabulary lock (class/archetype-as-generative-input HARD-PROHIBITED; kit / per-season emergent kit collection / substrate cluster). Lineage: `legacy-categorical-cleanup-audit-2026-05-22.md` (six retirements; "categorical pre-imposition survives cleanup at one layer by hiding in the next") + `2026-05-29-designer-writes-substrate-player-names-experience-principle.md` (designer writes substrate; player names the experience; class labels are vestigial secondary anchors).
- **Quality-orientation triplet at boundaries:** #42 framing-audit Q1/Q2/Q3 at every dispatch consumption (+42a measurement-context, +42b line-reference re-verification); #43 gandalf design-quality audit at wave-close; #44 framing-refusal authority (Q3=YES → refusal filed instead of execution).
- **Scaffold lifecycle:** #39 no-synthetic-stub-as-permanent-fallback (+ Mode A drift-catch vs Mode B canonical-resolution maturation); #40 scaffold-values-require-canonical-decision (+ case (c) canonical-lock retraction procedure; "shipped ≠ design — Gate-2 PASS does not ratify a scaffold").
- **Gear/damage mirrors of docs 46/47:** #33 stat-range bounds; #34 concentration (2-6 build-defining items); #35 layered cohesion; #36 substrate-as-keying-source; #37 class-agnostic drops; #38 damage-scaling-path declaration.
- **Enforcement hooks:** #47 bounded-viability (doc 50's 5 targets); #46 DB anti-materialization (kernel-panic-class protection); #48 host-RAM-aware concurrency.
- **Methodology:** #18 methodology-before-execution at math hotspots P2/P3/P5 (+18.1 substrate-voting-is-binding; +18.2 extension consultation fires AFTER baseline); #25 semantic-layer rep-audit (geometry-binding ≠ semantics-binding; the consumption-side contract that let weapon-substrate v1.0 conclude); #30 sim-methodology naming; #31 dual-effect separability; #32 first-do-no-harm synergy scan.
- **Substrate vocabulary:** #49 substrate-silence-is-not-validation; #50 substrate-vocabulary 3-test; **#51 synthesis-draft adversarial critique pre-lock — the discipline governing THIS doc's own path to canonical status**; #57 genre-aligned distribution (composes with the D7-baseline doc per § 5.6); #59 substrate-coverage-as-binding-quality-constraint.
- **Behavioral:** #21 no-sleep-recommendations + #22 timezone-agnosticism (Matt directives); #19 Agent-tool-not-for-waiting; #52/#53 pre-commitment + ADDITIVE-AND-REVERSIBLE heuristic; #54-#56 integration-smoke / Gate-2-invocation / generator-path naming.
- **AI-tell line (D7, `canonical/38…`):** no raw LLM dialogue at major story/onboarding moments; templated structure with LLM filling narrow blanks; recurs at skill-system § 9 (spirit-guide explainer), doc 43 § 5 (synergy scan resolves via pattern library, not LLM raw-reasoning), doc 45 § 5.5 (LLM naming-only at gear), cosmograph § 9 (no LLM names on PROVISIONAL constellations), creation-moment § 12.9 (templated guide voices).

**Reconciliation note carried from Block D:** D3's `seasonal_journey_narrative_structure` profile flag and the season-archival pivot reconcile via D6 § 1.4 (narrative layer preserved; release schedule decoupled). Doc 37 + Variant-C story doc are strategic-frame authorities only (§ 2 reading rule).

---

## 8. Cross-seam contracts

The architecture's seam boundaries, as canonically committed:

1. **Engine → player surface:** engine produces structured data; game consumes it (`canonical/37…` clean-interface claim). Operationalized at the cosmograph runtime boundary: offline pre-generation → JSON packet → runtime lookup, never runtime generation (cosmograph-pivot § 4.1). Drax's /forge surface = FUNCTIONAL; UE = AESTHETIC-IMMERSIVE for the creation moment (creation-moment § 3.8). Cosmograph must not visually normalize physical-anchor cluster size (Disc #59 substrate-honesty note at D7-baseline doc).
2. **Engine-flag vs profile-overlay-flag separation** (`engine-as-general-serial-content-product` § 3 pillar 2): Reincarnated distinctives (Earth Self, spirit-form library, reincarnation framing, seasonal-journey narrative, spirit-swap) live in the profile overlay, not the engine. Decision criterion: mechanical effects drive convergence → substrate; follows from determined identity → overlay (pillar 3).
3. **Substrate → generation:** Phase 2 binds against the v1_scope=2,293 weapon pool under composition policy D1–D7 (§ 4.4); contamination handled at consumption per Disc #25; substrate thinness is elrond-enrichment territory, never stub-workaround (Disc #59 + #39).
4. **Generation → simulation:** gamora consumes T4Candidate/PartitionGearInstance schemas (doc 44 § 8.5; doc 45 § 10.1 substrate-consumption table); sim methodology naming per Disc #30; calibration levers partition on MECHANICAL population, never substrate/element identity (Disc #13a-partition).
5. **Mechanical → cohesion → visual:** three separate BC archives on shared MAP-Elites machinery (BC-axes lock § 1.3); Phase 5 cohesion prompts stay substrate-only at Cycle 14 (designer-writes-substrate doc § 6); Phase 7 joint-gate evaluates all three.
6. **Engine → UE (PC seam):** § 12 contracts WS2 to ~7 rune-region AAA rendering (creation-moment § 12.11); UE 3D port direction at cosmograph-pivot § 10.6; mantis spike OVERALL GREEN unblocked WS1-WS5 (decisions-log cosmograph chain).
7. **LLM boundary:** internal-vs-generative schema separation (Disc #14 — canonical-four hidden from LLM; cipher); LLM naming downstream-only (§ 3.5); D7 AI-tell line at every player-facing surface (§ 7).
8. **Cross-seam contract changes** carry R11(b) round-trip discipline (round-trip smoke or explicit not-applicable rationale).

---

## 9. Gaps surfaced — DEFERRED register

Per recognition-validate-commit discipline, each entry carries its empirical re-engagement criterion. Nothing below is resolved by this synthesis.

**Lineage notes (NOT gaps — recorded for clarity):** Architecture A→B supersession (§ 3.8); T4-count layered vocabulary (§ 5.4); doc 51 § 10.8.9 TRADE_OFF-REVERSED pseudocode superseded by doc 47 § 4.6.5 implementation; doc 43 vs doc 44 "multiplier strategies" clarified at doc 44 § 8.3; C2 recognition-record header says DEFERRED but Branch A commitments subsequently FIRED (C3 § 10 + C1 § 11 are the commitment locus).

| # | Deferred item | Source | Empirical criterion / gate |
|---|---|---|---|
| 1 | C4 Secondary-T4 cohort peaks | doc 51 § 10.8.10 | Cycle 16+ BC-axis expansion |
| 2 | DIRECT_DAMAGE_AMPLIFICATION scaffold retirement (natural mechanics replace placeholder) | doc 50 § 4.7 v1.2; Matt D5 ratification | Cycle 15 P0 architectural commit (EXPLICIT COMMIT, not open question) |
| 3 | Per-level scaling formulas (gates multi-node calibration) | doc 41 § 4 | Multi-node calibration workstream fires |
| 4 | W1.13 H1-H5 hypothesis tests | roadmap § 3 Phase 3 | 🔒 DEFERRED; baseline-first per Disc #18.2 |
| 5 | Playability gate D61 + 8-pattern degenerate-state catalog; multi-T4 sim methodology D84 | roadmap § 3 Phase 3 | Cycle 13/14 Phase-3 work-units fire |
| 6 | Canonical rune-group structure lock + rune curation + cluster naming + cascade vocabulary | cosmograph-pivot § 10.11; creation-moment § 12.11 | Pattern B session (~1 hr scope per § 12.11) + Legolas glyph-corpus crawl (C2 § 4.3 commission PENDING) |
| 7 | Tier-1 input-model lock (Option γ tap + gesture-draw) | cosmograph-pivot § 10 | Playtest |
| 8 | Q1-Q5 creation-moment refinements (palette scope, narrowing model, compose direction, pre-scene, materialization ramp) | creation-moment § 4 | Gandalf leans recorded; son's input requested on Q1/Q4/Q5; vertical-slice playtest |
| 9 | Tal Rasha predictions P3/P4/P6; P5 | C2 § 5 | Vertical-slice playtest; S2 launch respectively |
| 10 | Seasonal glyph-system per-season lock | creation-moment § 11 | Cycle 15+ |
| 11 | Leveling experiential axis (§ 1.8.5) + player-input map architecture (§ 1.8.7) + load-bearing subset of hypothesis-flow's 55 open questions | hypothesis-flow § 8 (full register) | Playtest stages per § 6; Option-B naming gate = natural-faction-loss evidence (Q37) |
| 12 | Economic-veteran problem (5 alternatives A1-A5; gandalf lean A5) | season-archival § 5 | Materials/trading scope decision; per-realm market validation (§ 5.2) |
| 13 | Doc 52 experiential-archetype promotion vocabulary; cohort_archetype → player-experience mapping | designer-writes-substrate § 6, § 4.5 | Community research findings; Cycle 15+ consumption layer |
| 14 | Disc #18.2/#18.3 target-vs-watch-flag amendment candidate | D7-baseline § 6; `agentic_orchestration/gandalf/notes/2026-06-09-discipline-recognition-substrate-vs-genre-baseline.md` | jack-ryan ratification consideration |
| 15 | 18 Disc #40 cascade-vocabulary scaffold flags; canonical primitive-group + rune-per-group locks | decisions-log (cosmograph chain) | Pattern B |
| 16 | Phase 7 DB migration | decisions-log | ADR-006 Matt-authorization pending |
| 17 | WEAPON_FAMILY_L50_BASELINE fallback-vs-substrate reconciliation | decisions-log (Gate-2 Finding 2 WARN) | Pre-Wave-5 follow-on |
| 18 | Weapon-substrate v1.1+ items (9.11-C/D/E curation; 9.10-E faction structure; D10 Path C) | conclusion-declaration | P4 labeling surfaces contamination as blocker; engine consumption surfaces Disc-#25-uncatchable contamination; post-ship feedback |
| 19 | Path B post-generation form clustering; doc 45 proposed-field state (`scope_preference`, `is_unique`) + placeholder unique pools | composition-policy § 5.4; doc 45 § 3.2/§ 4.3 | v1.1+; current code state is rocket-seam verification territory |
| 20 | C1-C5 vocabulary migration engine-side | doc 51 § 10.8.10 | gamora seam authority; Cycle 15 housekeeping |
| 21 | VIT attribute; trait identity-modulators; max-8-active skill constraint | attribute-system § 1; cleanup-audit § 3; roadmap § 3 Phase 2a | v1.1+; v1.1+; Phase 2a work-unit |
| 22 | BC-axis Pattern-6 revisit (axes derived vs assigned) | cleanup-audit § 4.2 | Post-axis-discovery (≥1,000-weapon PCA/factor analysis evidence) |

**Contradiction count: zero.** Every apparent divergence surfaced during the 33-source read resolved as either layered vocabulary (§ 5.4), lineage supersession with explicit amendment record (§ 3.8, § 6.1), or estimate-vs-actual within range (composition-policy ~1,700–3,100 vs locked 2,293). This is itself a finding: the canon's amendment-pass discipline (STATUS stamps, § 0.1 amendment records, supersession-by-refinement) is holding.

---

## 10. Sign-off

**Authored:** gandalf (story-and-design steward), 2026-06-10, as Fable-5 Phase 1 deliverable per Matt 2026-06-10 dispatch.

**Method compliance:** consultation-declaration checklist committed + pushed before source reads (commit `dfe168f`); all 33 sources read in full (checkboxes marked pre-authoring); per-block distillations captured at working notes; targeted §-verification re-reads fired on doc 39/46/50 enumerations before authoring. No claim authored from ground-state-oracle one-liners (`canonical/00-ground-state.md` used for orientation only, per checklist E4 declaration).

**Authority chain:** this doc is REFERENCE, not supersession. Source docs win on divergence. Gaps in § 9 are DEFERRED with empirical criteria, not resolved.

**Path to canonical status:** Discipline #51 — Gate-1 critique-pair review (Matt + jack-ryan) before CURRENT status firms. Phase 2 (rocket Fable-5) fires post Gate-1 PASS.

**End of synthesis.**
