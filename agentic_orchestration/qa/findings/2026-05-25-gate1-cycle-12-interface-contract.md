# Finding — 2026-05-25 — Gate-1 Cycle 12 Interface Contract

**Reviewer:** jack-ryan
**Severity:** CLEAR-WITH-AMENDMENTS (WARN + INFO findings; no BLOCK)
**Target:** framing brief § 4 interface contract (RATIFIED 2026-05-25)
**Developer:** gandalf (contract author); rocket (downstream consumer)
**Principles applied:** 1, 2, 3, 4, 6

---

## Summary verdict

**CLEAR-WITH-AMENDMENTS.** Rocket L2 + L3 dispatches may fire. No BLOCK-level issue found against canonical authority. Seven WARN and three INFO observations; five of the seven WARNs are directly actionable at dispatch-authoring time by KR before rocket fires. Two WARNs are noted-for-implementation (rocket embeds fix at Layer 2/3 implementation).

---

## Per-principle findings

---

### Principle 1 — Soundness against canonical authority

#### WARN-1 — `off_hand_item` references wrong sidecar

**Observation:** `PlayerClass.off_hand_item` field comment reads "if applicable; per Sidecar B" but the framing brief § 2 SC-3 sidecar is the Cycle 12 off-hand mechanical contract work. Sidecar B is the Cycle 10 substrate-curation work (already closed). The off-hand mechanical contract is SC-3 in Cycle 12 terminology.

**Risk:** rocket reading the contract comment will look for the wrong sidecar for design authority. Sidecar B is a substrate-curation execution doc; SC-3 is the un-authored mechanical contract design. The field label cross-reference is ambiguous about which authority governs mechanical behavior.

**Cite:** Discipline #13a (implementation-vs-intent drift — contract comment must cite correct authority).

**Action:** KR amends `off_hand_item` field comment in rocket L3 dispatch to read "if applicable; mechanical contract per SC-3 (Cycle 12); substrate per off-hand-items-2026-05-24.md" before firing.

---

#### WARN-2 — `mechanical_substrate_triple: tuple[str, str, str]` type underspecified relative to L1 math model

**Observation:** The BDI math model (framing brief L1) defines the triple as `(element, weapon_kind, weapon_mechanical_profile)` — but `weapon_mechanical_profile` is itself a structured 6-tuple per L9: `(range, tempo, amplitude, AoE, primary_stat, hits_per_attack)`. The contract types the triple as `tuple[str, str, str]` — three bare strings. This collapses the third member to a single string label when the canonical definition has sub-structure.

**Consequence for Discipline #1:** A rocket math note citing "mechanical_substrate_triple feeds γ-coefficient" cannot be verified unless the triple's third member is explicitly either (a) the weapon_kind_classified_subtype string OR (b) a structured sub-type. The type annotation leaves this ambiguous. Dispatch notes on open question 5 in the jack-ryan dispatch correctly flag this — the finding here is that it needs resolution at dispatch time, not left for rocket to decide.

**Cite:** Discipline #1 (math-before-code — math hotspot must be math-note-able from field structure); framing brief L1 + L9.

**Action:** KR's rocket L2 dispatch should explicitly specify: `mechanical_substrate_triple` is `tuple[element_str, weapon_kind_subtype_str, weapon_mechanical_profile_label_str]` where the third element is one of a defined vocabulary (matching `weapon_kind_classified_subtype` patterns in the DB) NOT a freeform string. Alternatively, promote to a structured dataclass per dispatch open question 5 — KR judgment call at dispatch authoring.

---

#### INFO-1 — Cultural_tradition / lineage / period placement is sound against L9

**Observation:** These three fields are present on `PlayerClass` but the contract's review note correctly flags them as "NOT in BDI math; for narration + naming." This is aligned with L9 (`framing-brief.md § 1 L9`) and the Q-A verdict. The semantic-overlay-only placement is correct.

**No action required.** Citing for the record: Discipline #25 (semantic-layer rep-audit) is satisfiable from field structure — mechanical vs semantic boundary is visually clear in the dataclass layout.

---

#### INFO-2 — Layer 6 wire-up signature correctly references L9 opportunity-scan refactor

**Observation:** The `apply_t4_alteration_to_combat` docstring explicitly states "Per L7 refactor: opportunity-scan triggers use mechanical_substrate signals (NOT cultural_tradition per L9)." This is the correct canonical constraint. The docstring notation says "L7" but means the L9 refactor — this is a minor internal notation error (L7 is the deferred BDI test framework; L9 is the substrate split). Not blocking; the intent is unambiguous in context.

**No action required.** Notation: rocket should read this as the L9 refactor requirement regardless of the "L7" label in the docstring.

---

### Principle 2 — Completeness for parallel L2 + L3 work

#### WARN-3 — `bc_axis_contribution: list[float]` arity unspecified against 8-axis vs 5-axis discrepancy

**Observation:** The framing brief comment says "5+ floats per node per math note v1.1 § 3.6." Math note v1.1 § 3.6 defines `bc_axis_contribution_tags` as a dict covering 8 BC axes (axis_1_engagement, axis_2_geometry, axis_2A_proxy, axis_2B_control, axis_3A_tempo, axis_3B_variance, axis_4_defensive, axis_5_economy). The contract types this as `list[float]` rather than matching the math note's dict shape.

**Risk for Layer 4 consumption:** `converge_kit` (Layer 4) must walk `bc_axis_contribution` to compute WR-gradient-weighted node adjustments per math note § 4.2-4.3. A list with unspecified ordering is not safely walkable without a shared index → axis mapping. The math note's dict-of-axis-id-to-weight is the correct shape.

**Cite:** Discipline #1 (math-before-code — math hotspot must be math-note-able); Principle 2 (completeness for parallel L2+L3 work — L4 must know how to consume L3 output).

**Action:** KR's rocket L3 dispatch should specify `bc_axis_contribution` as `dict[str, float]` keyed by axis ID per math note v1.1 § 3.6 vocabulary (8 keys), NOT a bare list. This is a non-blocking WARN — list could work if ordering is locked per convention, but the dict form is the canonical-aligned shape and eliminates ambiguity at no cost.

---

#### WARN-4 — `stat_allocation: StatDistribution` and `attribute_coupling: list[str]` are undefined types

**Observation:** Two Layer 4 output fields (`stat_allocation: StatDistribution`, `attribute_coupling: list[str]`) and the `converged_modifier: float` field are listed as "(populated by Layer 4)" on `PlayerClass`. However, `StatDistribution` is a referenced type with no definition in the § 4 contract. Layer 3 dispatches must know the shape to emit a coherent kit even if Layer 4 hasn't run yet; Layer 2 must emit a stub or leave these nullable.

**Consequence:** If `StatDistribution` is undeclared, rocket L2 cannot emit a conformant `PlayerClass` stub (needed to allow L3 to compose against it in parallel). This is a completeness gap for the parallel-build coordination intent.

**Cite:** Principle 2 (completeness — does L3 know how to walk L2 output; do L2/L3 contracts compose).

**Action:** KR's rocket L2 dispatch should explicitly define `StatDistribution` as a named type (or alias `dict[str, float]` with explicit keys per attribute system: STR/INT/WIS/DEX stat allocation floats). Also: `stat_allocation`, `attribute_coupling`, and `converged_modifier` should be marked `Optional[...]` on the `PlayerClass` dataclass (as Layer 4 stubs) — they are nullable pre-Layer-4, non-nullable post-Layer-4. The contract as written does not distinguish nullable vs required state by layer.

---

#### WARN-5 — `t4_candidates: list[T4Candidate]` has no arity bound or per-chain coverage spec

**Observation:** The contract lists `t4_candidates: list[T4Candidate]` without specifying expected arity relative to chain count. Math note v1.1 § 3.4 and skill-system § 2 state there are 2-4 chains per kit and 0-1 T4 keystone per chain. The dispatch open question asks whether this should be capped.

**Canonical answer available:** T4-A § 2 locks 1 signature + 1-3 secondary capstones. Per chain × per-T4-slot the math is: with 2-4 chains, expect 3-5 T4Candidate slots maximum at v1 (signature + up to 3 secondaries across chains). A cap of 5-6 is mathematically derivable from existing canon.

**Risk without spec:** rocket L3 could produce unbounded T4Candidate lists; Layer 4 and Layer 6 would have no enforcement boundary.

**Cite:** Discipline #1 (math-before-code — T4 count bound is math-derivable); T4-A § 2 canonical authority.

**Action:** KR's rocket L3 dispatch should specify `t4_candidates` max arity = (chain_count × 1 signature + up to 3 secondary) ≤ 5-6 entries at v1, with per-chain slot structure captured. This is directly derivable from T4-A § 2 + skill-system § 2.2.

---

#### INFO-3 — `SkillChain.tier_4_slot` is a single slot; SkillTree has no cross-chain T4 election mechanism

**Observation:** Each `SkillChain` has a single `tier_4_slot: T4Slot`. This is correct for per-chain T4 architecture per T4-A § 2. However, the contract has no cross-chain T4 election mechanism (which chain's T4 is the "signature capstone" per T4-A hierarchy vs "secondary capstone"). Layer 6 wire-up needs to know which `T4Alteration` is the build-defining regime-change for the L9 opportunity-scan refactor.

**Not blocking for L2+L3 parallel fire.** This is a Layer 6 design detail. Calling it out so rocket L6 dispatch author is aware the contract needs an election mechanism at `SkillTree` level (e.g., `signature_chain_id: Optional[str]`).

---

### Principle 3 — Cross-seam round-trip readiness

#### WARN-6 — `generation_params: dict` is serialization-hostile without schema discipline

**Observation:** `generation_params: dict` is an untyped dict. In Python's JSON serialization ecosystem, untyped dicts serialize safely as long as values are JSON-primitives. However, the risk is that rocket's implementation places non-serializable values in `generation_params` (e.g., generator function references, numpy dtypes, Enum objects) without schema validation at the export boundary.

**Per Discipline #8 (schema validation at export boundaries):** this field needs a JSON-primitives-only constraint or an explicit schema. The `source_library: str` field is correctly typed.

**Cite:** Discipline #8 (schema validation at export boundaries — validate before writing to disk); Principle 3 (round-trip readiness — PlayerClass must serialize through star-lord JSON).

**Action:** KR's rocket L2 dispatch should specify: `generation_params` values must be JSON-primitive (str / int / float / bool / None / list / dict of same). Enforce via Discipline #8 schema validation at export boundary. Pydantic `model_validator` or explicit `json.dumps` round-trip test in smoke is sufficient.

---

#### INFO-4 (from dispatch open question) — `engine_version: str` field absence

**Observation:** The dispatch's open-questions list asks whether `engine_version: str` should be required. Per Cycle 10 Sidecar A telemetry-gap finding ("`engine_version unknown`" in telemetry), this gap was already surfaced. The new engine's `PlayerClass` is the earliest provenance record — omitting `engine_version` here means gate-2 attribution to a specific new-engine generation is only reconstructable via `source_library`, which doesn't carry schema version.

**Not blocking for L2+L3 fire.** But: adding `engine_version: str` to `PlayerClass` at authoring time costs nothing and prevents a known telemetry-gap pattern from recurring.

**Cite:** Discipline #7 (capture decision telemetry for archaeology — bias toward over-capturing provenance).

**Action (recommended):** KR adds `engine_version: str` as a required field to `PlayerClass` in the rocket L2 dispatch. Value: `"v2.0"` or equivalent semantic version for the new engine path, distinct from the legacy `ClassGenerator`.

---

### Principle 4 — Engineering-disciplines compliance

#### WARN-7 — `generation_seed: int` + `generation_params: dict` nullable status unspecified

**Observation:** The dispatch's open-questions list asks whether these should be required-not-nullable for reproducibility. The answer from Discipline #1 (reproducibility as math-before-code substrate) and Discipline #10 (attribution clarity — same seed across before/after comparisons) is: `generation_seed` SHOULD be required-not-nullable. If a `PlayerClass` can be generated without a seed, deterministic replay is impossible.

**Canonical precedent:** `generate-season --seed N` discipline across all existing engine work treats seed as required. The new engine should match this.

**Cite:** Discipline #1 (math-before-code — deterministic reproducibility is load-bearing for algorithm validation); Discipline #10 (attribution clarity — same seed across before/after comparisons).

**Action:** KR's rocket L2 dispatch should specify `generation_seed: int` as required (not Optional). `generation_params: dict` as required with JSON-primitive constraint per WARN-6.

---

### Cross-cutting findings

#### Q3 AUGMENT compatibility — SOUND

**Assessment:** The contract requires both legacy `ClassGenerator` and new generator to produce the same `PlayerClass` shape (per framing brief § 4 contract note: "Q3 Option B: legacy ClassGenerator preserved alongside; new generator is production path; both produce PlayerClass shape"). This is architecturally correct for AUGMENT compatibility. No finding required. The `source_library: str` field explicitly distinguishes `"generator_v2"` vs `"legacy_classgenerator"` provenance — this is the correct discriminator.

#### L11 strict 4-tuple matching — contract enforcement is implicit, not explicit

**Assessment:** The `bc_target_cell: BcTargetCell` field typed as a `5-tuple (range, tempo, amplitude, attribute, proxy_density)` is structurally correct per L11. The strict matching constraint (L11) is captured in the framing brief but is NOT enforced at contract level — there is no `strict_match_enforced: bool` or matching-strategy field on `PlayerClass`. This is acceptable for v1 because L11 is a generator-behavior constraint, not a per-PlayerClass instance property. No action required.

#### SC-3 off-hand mechanical contract fit — partially sound; pending SC-3 authoring

**Assessment:** `off_hand_item: Optional[WeaponKnowledgeEntry]` correctly types the field as optional (cells without off-hand items produce `None`). The `WeaponKnowledgeEntry` type captures the substrate row correctly. HOWEVER: the mechanical contract for off-hand items (buff/aura/proxy effects for banner/focus/talisman/tome/horn) is NOT captured in the interface contract. The `weapon_sim_props` extension fields (`off_hand_buff_geometry`, `off_hand_aura_tempo`, etc., per off-hand-items doc § 2.3) are the mechanical-contract layer — and SC-3 has not yet been authored. This is not a BLOCK because SC-3 is explicitly Cycle 12 scope (to be authored alongside Layer 3), but rocket L3 dispatch must confirm SC-3 mechanical fields are readable from the `WeaponKnowledgeEntry` shape (or extend it).

**Cite:** Principle 3 (cross-seam readiness); off-hand-items-2026-05-24.md § 2.3.

**No additional action beyond what SC-3 authoring already covers.** Flag for KR when authoring rocket L3 dispatch: verify SC-3 mechanical fields surface on or alongside `WeaponKnowledgeEntry`.

---

## Action summary (all non-blocking)

| # | Severity | Action | Owner | When |
|---|---|---|---|---|
| WARN-1 | WARN | Amend `off_hand_item` comment to cite SC-3 (not Sidecar B) | KR | At rocket L3 dispatch authoring |
| WARN-2 | WARN | Specify `mechanical_substrate_triple` third member vocabulary OR promote to structured dataclass | KR | At rocket L2 dispatch authoring |
| WARN-3 | WARN | Change `bc_axis_contribution` type from `list[float]` to `dict[str, float]` per math note v1.1 § 3.6 axis-id vocabulary | KR | At rocket L3 dispatch authoring |
| WARN-4 | WARN | Define `StatDistribution` type; mark Layer-4-populated fields as `Optional[...]` pre-Layer-4 | KR | At rocket L2 dispatch authoring |
| WARN-5 | WARN | Specify `t4_candidates` max arity ≤ 5-6; derive from T4-A § 2 chain hierarchy | KR | At rocket L3 dispatch authoring |
| WARN-6 | WARN | Constrain `generation_params` values to JSON-primitives; add Discipline #8 export validation | KR / rocket | At rocket L2 dispatch authoring (spec); at L2 implementation (enforce) |
| WARN-7 | WARN | Make `generation_seed` required-not-nullable per Disciplines #1 + #10 | KR | At rocket L2 dispatch authoring |
| INFO-4 | INFO | Add `engine_version: str` required field to `PlayerClass` | KR (recommended) | At rocket L2 dispatch authoring |
| INFO-3 | INFO | Note at rocket L6 dispatch: add cross-chain T4 signature-election mechanism to `SkillTree` | KR | At rocket L6 dispatch authoring (deferred to after L2+L3 land) |

---

## What I did NOT flag

- The `ConvergenceResult.per_dim_adjustments: dict` type: this is intentionally open-schema for the multi-dim convergence implementation to populate; acceptable given legolas MC-3 methodology consult gates L4 implementation.
- The `SkillTree.cross_chain_rule: Optional[str]` field: correctly Optional per math note v1.1 § 3.3 cross-chain-rules structure.
- The `FightEngineContext` / `AlteredFightEngineContext` types in the Layer 6 signature: dispatch open question about narrowing vs using `FightEngineContext` is a KR judgment call at L6 dispatch authoring; not blocking for L2+L3 parallel fire. Current as-drafted signature is acceptable.

---

## Final verdict

**CLEAR-WITH-AMENDMENTS.**

Seven WARN findings; zero BLOCK findings. All WARNs are resolvable at rocket L2 + L3 dispatch authoring time by KR before rocket fires — they do not require gandalf design-fit review or Matt escalation. The contract is structurally sound against:

- L9 substrate split (mechanical vs semantic correctly separated)
- L11 strict 4-tuple matching (enforced at generator level; contract shape is correct)
- T4-A architecture (per-chain T4 slot structure correct)
- Skill-system § 8 Layer 6 wire-up (L9 opportunity-scan refactor explicitly noted)
- Off-hand-items canonical (WeaponKnowledgeEntry shape correct; SC-3 scope acknowledged)
- Multi-dim convergence v1.1 (ConvergenceResult shape matches; WARN-3 corrects bc_axis_contribution type)

**Rocket L2 + L3 dispatches may fire after KR integrates the 7 WARN amendments at dispatch authoring.**

No gandalf design-fit route required. No Matt escalation required.

---

## References

- `agentic_orchestration/gandalf/notes/2026-05-25-cycle-12-new-engine-parallel-build-framing-brief.md` § 4 (primary review target)
- `agentic_orchestration/cycles/cycle-12-hive-mind-scope.md`
- `canonical/story/skill-system-2026-05-24.md` § 2, § 3, § 8, § 12
- `canonical/story/multi-dim-convergence-algorithm-2026-05-21.md` v1.1 § 3.4, § 3.6, § 4.2, § 4.3
- `canonical/story/tier-4-architecture-defaults-2026-05-22.md` § 2
- `canonical/story/off-hand-items-2026-05-24.md` § 2.3
- `canonical/story/attribute-system-2026-05-24.md`
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md`
- `canonical/story/qd-engine-end-to-end-workflow-2026-05-24.md`
- `agentic_orchestration/REVIEW_PROCESS.md` (5 principles + severity rubric)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` (Disciplines #1, #7, #8, #10, #13a, #25)
- `agentic_orchestration/dispatches/2026-05-25-jack-ryan-cycle-12-gate-1-interface-contract.md` (dispatch scope + open questions)
