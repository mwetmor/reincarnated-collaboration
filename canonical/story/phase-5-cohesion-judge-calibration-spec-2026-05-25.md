# Phase 5 Cohesion-Judge Calibration Spec — Skill-Node-Level Naming + Cohesion Validation

> **STATUS:** RATIFIED 2026-05-25 — Matt authorization to gandalf for Phase 5 calibration spec authoring (gates rocket regen post-Cycle-12 to fix Phase 5 placeholder issue per design-fit pass finding)
>
> **Authored:** 2026-05-25
> **Author:** gandalf (story-and-design steward; design-spec-as-math per gandalf OP § 3.2)
> **Pattern:** design-spec-as-math canonical authoring — defines WHAT Phase 5 produces + cohesion-validation rubric; rocket implements per spec; jack-ryan Gate-2 validates output

**Authority basis:**
- Matt 2026-05-25 — "let's start the regens to fix the Skill Tree Null value issue" + authorization to fire gandalf parallel-track authoring with Phase 5 spec as regen-gate
- gandalf design-fit pass 2026-05-25 (`agentic_orchestration/gandalf/notes/2026-05-25-engine-generation-special-case-summary.md` finding #2 — "Phase 5 ran at form-layer only — 289/289 skill nodes are placeholders")
- v2_narrow generation run (35 forms; 2026-05-25) — empirical evidence Phase 5 didn't fire at skill-node level

**Companion docs:**
- `canonical/story/skill-system-2026-05-24.md` § 9 — spirit-guide explainer pattern (Phase 5 context)
- `canonical/story/qd-engine-end-to-end-workflow-2026-05-24.md` Phase 5 Cohesion Coalescence (engine workflow context)
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` § 5 (named-bearer discipline; informs cohesion rubric)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#18 methodology-before-execution; #1 math-before-code)

---

## 0. TL;DR

Phase 5 currently fires at form-layer only (form name + sub-element flavoring). It does NOT fire at skill-node level → 289/289 skill nodes in v2_narrow are placeholders ("Chain A T1 0" etc.). This spec defines:

1. **What skill-node-level Phase 5 produces** — name + flavor text + thematic alignment per node
2. **LLM prompting structure** — input context, output schema, prompt template per node-tier × node-type
3. **Cohesion-validation rubric** — how cohesion-judge evaluates skill-node output for kit-identity coherence
4. **Calibration sweeps** — per Discipline #17, what parameters need empirical tuning during implementation

Rocket implements per spec. jack-ryan Gate-2 validates per acceptance criteria § 6.

**Estimated rocket effort:** ~1-2 days implementation + ~30-60 min calibration sweeps + jack-ryan Gate-2 validation

---

## 1. Phase 5 current state + gap

### 1.1 What Phase 5 currently DOES (per legacy engine + Cycle 12 sample-season output)

- **Form-level naming**: produces form name per kit identity (e.g., "Jade Warlord" from Aztec war-club + Moctezuma anchor + RESOURCE_CONVERSION)
- **Sub-element flavoring**: produces sub-element manifestation per substrate-tradition (per skill-system sub-element architecture)
- **Spirit-guide narration metadata**: per L6 narration_metadata schema (drax Cycle 12 Wave 5 LIVE-supported)

### 1.2 What Phase 5 currently DOES NOT do (the gap)

- **Skill-node-level naming**: 289/289 skill nodes (35 forms × ~8-10 nodes each) are placeholders like "Chain A T1 0", "Chain A T1 1", "Chain B T2 0" etc.
- **Skill-node-level flavor text**: no description text per node
- **Skill-tree thematic alignment validation**: no cohesion check that skill names + flavor align with kit identity at the tree level

### 1.3 Why this matters

Per gandalf design-fit pass finding #2: "Matt cannot fully evaluate 'skill-tree feel' at T4 post-mortem with placeholders."

Plus per all-0.5-win-rate finding (gandalf design-fit pass supplemental): without real skills, kits are mechanically indistinguishable → balance loop trivially converges → no fight-behavior differentiation observable.

**Phase 5 skill-node naming is THE gating piece for both T4 post-mortem evaluation and meaningful fight-behavior signal.**

---

## 2. Skill-node-level naming — what Phase 5 must produce

Per skill-node per kit per generation run:

### 2.1 Per-node output schema

```python
@dataclass
class SkillNodeNaming:
    skill_node_id: str            # existing identifier (e.g., "chain_a_t1_0")
    name: str                     # short name (~2-5 words; e.g., "Bloodletter's Discipline")
    flavor_text: str              # 1-2 sentence flavor (~15-40 words; thematic alignment with kit identity + cultural-tradition + element)
    effect_description: str       # 1 sentence mechanical description (~10-25 words; surfaces node's bc_axis_contribution in player-readable terms)
    thematic_tags: list[str]      # extracted thematic anchors (cultural / element / archetype / etc.) for cross-tree validation
```

### 2.2 Input context per skill-node LLM call

Per node naming call, Phase 5 provides:

```python
PromptInputContext = {
    # Kit identity (already determined by Phase 2/3/6/8)
    "form_name": str,                          # e.g., "Jade Warlord"
    "form_kit_summary": str,                   # 1-2 sentence summary of kit identity from form-level Phase 5
    "element": str,                            # 8 core elements
    "energy_type": str,                        # mana / rage / charge / focus
    "primary_stat": str,                       # STR/INT/WIS/DEX
    "range_profile": str,                      # close / mid / long
    "tempo_class": str,                        # low / medium / high
    "amplitude_class": str,                    # flat / spiky / etc.
    "mechanical_substrate_triple": tuple,      # per L9 — mechanical only (no cultural overlay in math; but provided here for narration cohesion)
    "cultural_tradition": Optional[str],       # semantic overlay; informs narration tone
    "named_bearer": Optional[str],             # semantic overlay; informs narration anchoring
    "lineage": Optional[str],                  # named_mythological / generic_cultural

    # Per-node context
    "skill_node_id": str,
    "chain_id": str,                           # which chain (A, B, C, D)
    "tier": int,                               # 1-4
    "node_type": str,                          # damage / control / defense / mobility / utility
    "bc_axis_contribution": dict[str, float], # which BC axes this node contributes to + weights
    "cost": int,
    "cooldown_seconds": float,
    "playable_at_level_1": bool,
    "is_t4_slot": bool,                        # if T4 keystone slot
    "t4_alteration": Optional[T4Alteration],   # if T4 slot; per § 8 algorithm output

    # Cross-node context (for cohesion)
    "chain_predecessor_names": list[str],      # if T2+; names of T1/T2 nodes in same chain (for thematic continuation)
    "form_previously_named_nodes": list[str],  # nodes already named in this form's tree (for cross-tree cohesion)
}
```

### 2.3 Prompt template structure

Per node, Phase 5 calls LLM with structured prompt:

```
SYSTEM:
You are naming skills for a fantasy class in an ARPG. The class identity is:
{form_kit_summary}

This skill is in chain {chain_id}, tier {tier}. It is a {node_type} skill with the following mechanical properties:
- Cost: {cost} {energy_type}
- Cooldown: {cooldown_seconds}s
- Contributes to: {bc_axis_contribution dictionary as readable list}
{if t4_slot: - Tier 4 keystone alteration: {t4_alteration.strategy} ({t4_alteration.summary})}

Cultural / thematic anchoring (use as narration tone reference, not literal):
- Element: {element}
- Cultural tradition: {cultural_tradition or 'engine-original'}
- Named-bearer reference (if applicable): {named_bearer}
- Previously-named skills in this chain: {chain_predecessor_names}
- Other named skills in this kit: {form_previously_named_nodes}

USER (output JSON):
{
  "name": "<2-5 word skill name; cohesive with chain progression + kit identity>",
  "flavor_text": "<1-2 sentence flavor; cultural tradition + element + named-bearer-resonance where applicable; thematic continuation with predecessor names>",
  "effect_description": "<1 sentence player-readable mechanical effect; surfaces bc_axis_contribution in plain terms>",
  "thematic_tags": ["<3-5 thematic tags; subset of cultural / element / archetype / mood / etc.>"]
}
```

### 2.4 LLM model selection

**Primary recommendation:** Claude 3.5 Sonnet (good balance of quality + cost; matches existing Phase 5 form-level naming).

**Alternative:** Claude 3.5 Haiku (cheaper; possibly sufficient for skill-node-level naming since context is narrower than form-level).

**Cost projection:**
- ~10 LLM calls per form × 35 forms = ~350 calls (35-form generation run)
- ~500-1500 tokens per call combined (prompt + completion)
- Total: ~175K-525K tokens
- Cost @ Claude 3.5 Sonnet: ~$0.50-$2.00 per generation run
- Cost @ Claude 3.5 Haiku: ~$0.10-$0.50 per generation run

Per G12 measurement (~0.13% repeat rate; DiskCache catches repeats at $0). First-run dominant.

---

## 3. Cohesion-validation rubric — how cohesion-judge evaluates output

Per skill-node naming output, cohesion-judge (Phase 5 sub-pass) validates against 5 dimensions:

### 3.1 Kit-identity cohesion (weight: 0.30)

Does the skill name + flavor align with the form's kit identity (element + cultural tradition + named-bearer)?

| Score | Criterion |
|---|---|
| 1.0 (PASS) | Name + flavor unambiguously reads as belonging to this kit (e.g., "Bloodletter's Discipline" for an Aztec RESOURCE_CONVERSION kit) |
| 0.6-0.9 (BORDERLINE) | Name + flavor is acceptable but feels generic OR could fit multiple kits |
| 0.0-0.5 (FAIL) | Name + flavor reads as a different kit's identity OR breaks thematic coherence |

### 3.2 Chain-progression cohesion (weight: 0.20)

Does the skill name fit the progression of its chain (T1 → T4)?

| Score | Criterion |
|---|---|
| 1.0 (PASS) | Name builds thematically from predecessor names; tier-appropriate (T4 should feel climactic vs T1 baseline) |
| 0.6-0.9 (BORDERLINE) | Acceptable progression but doesn't strongly build |
| 0.0-0.5 (FAIL) | Disconnected from chain predecessors OR tier-inappropriate naming |

### 3.3 Mechanical-narration alignment (weight: 0.20)

Does the effect_description accurately convey the node's mechanical contribution (bc_axis_contribution)?

| Score | Criterion |
|---|---|
| 1.0 (PASS) | Player reading effect_description would correctly predict the node's combat behavior |
| 0.6-0.9 (BORDERLINE) | Description accurate but unclear OR uses jargon that's not player-friendly |
| 0.0-0.5 (FAIL) | Description misrepresents the mechanic OR omits load-bearing behavior |

### 3.4 Cultural-tradition cohesion (weight: 0.15)

If cultural_tradition is set, does the skill name + flavor reflect that tradition appropriately?

| Score | Criterion |
|---|---|
| 1.0 (PASS) | Cultural tradition surfaces clearly; not stereotypical OR appropriative |
| 0.6-0.9 (BORDERLINE) | Cultural alignment present but weak OR slightly off-tone |
| 0.0-0.5 (FAIL) | Cultural cues misapplied OR appropriative |

### 3.5 Cross-tree thematic cohesion (weight: 0.15)

Do the named nodes in this kit's tree TOGETHER read as a coherent identity?

| Score | Criterion |
|---|---|
| 1.0 (PASS) | All ~10 named nodes feel like they belong to the same character; no jarring contrasts |
| 0.6-0.9 (BORDERLINE) | Most nodes cohesive; 1-2 outliers |
| 0.0-0.5 (FAIL) | Tree reads as 10 disconnected skills from different characters |

### 3.6 Aggregate cohesion score

```python
cohesion_score = (
    0.30 * kit_identity +
    0.20 * chain_progression +
    0.20 * mechanical_narration +
    0.15 * cultural_tradition +
    0.15 * cross_tree_thematic
)
```

**Acceptance thresholds:**
- `cohesion_score >= 0.75` → PASS per node
- `cohesion_score 0.60-0.74` → BORDERLINE; flag for design review
- `cohesion_score < 0.60` → FAIL; re-roll node naming (max 3 attempts; then placeholder + flag)

---

## 4. Calibration sweeps — per Discipline #17

Per math-before-code + Discipline #17, the following parameters require empirical tuning during Phase 5 implementation:

| # | Parameter | Initial value | Sweep range | Trigger for tune |
|---|---|---|---|---|
| 1 | Per-node LLM temperature | 0.7 | 0.5 - 1.0 | Output variance too low or too high; adjust for creativity balance |
| 2 | Per-node max_tokens | 200 | 150 - 300 | Truncation observed OR excess verbosity |
| 3 | Cohesion-score acceptance threshold | 0.75 | 0.65 - 0.85 | Empirical PASS rate too low/high; aim for ~80% first-attempt PASS |
| 4 | Re-roll attempt cap | 3 | 2 - 5 | Empirical re-roll rate; aim for <10% nodes hitting cap |
| 5 | Chain-predecessor context size | 3 most recent | 2 - 5 | Cohesion improves vs context cost trade-off |
| 6 | Cross-tree thematic context size | 5 most recent | 3 - 10 | Cross-tree cohesion improves vs context cost trade-off |
| 7 | Element + cultural-tradition weight in prompt | balanced | element-dominant / cultural-dominant variants | Output reads too generic-element OR too generic-cultural |
| 8 | T4 slot prompting (separate template?) | shared template | separate T4 template variant | T4 slot naming distinguishable vs blends in |
| 9 | Named-bearer attribution prominence | subtle reference | explicit-name / subtle / absent variants | Player-facing tone test — too on-the-nose vs too subtle |

**Rocket calibration approach:**
1. Implement with initial values per § 4
2. Fire small smoke (3-5 forms; ~30-50 nodes) → measure cohesion-score distribution + re-roll rate + observable quality
3. Sweep parameters per § 4 if smoke surfaces tuning need
4. Re-smoke to validate
5. Fire full regen (35 forms; ~289 nodes)

---

## 5. Sub-element flavoring at skill-node level

Per skill-system sub-element architecture:
- Phase 5 produces sub-element manifestation per substrate-tradition at form level
- Should this extend to skill-node level? (e.g., per-node sub-element flavor variation within form)

**Recommendation (initial):** sub-element flavoring at form level only; skill-node naming inherits form's sub-element. Re-evaluate post-implementation if observed forms feel "over-uniformized."

**Reasoning:** sub-element-per-skill-node would explode LLM call complexity + risk over-fragmenting form identity. Form-level sub-element + skill-level cultural-tradition + element references should suffice for coherent narration.

---

## 6. Acceptance criteria for jack-ryan Gate-2

Rocket implementation passes Gate-2 when:

- [ ] Phase 5 fires at skill-node level for ALL nodes in ALL generated forms
- [ ] Per-node output schema § 2.1 populated (name + flavor_text + effect_description + thematic_tags)
- [ ] No placeholder strings (e.g., "Chain A T1 0") in skill-node names; all named per Phase 5 LLM output
- [ ] Cohesion-judge fires per node + produces cohesion_score per § 3.6 weighted aggregate
- [ ] First-attempt PASS rate ≥ 70% (initial target; may calibrate per § 4 #3)
- [ ] Re-roll rate ≤ 15% (initial target; may calibrate per § 4 #4)
- [ ] Final FAIL rate (after re-rolls) ≤ 5% per generation run
- [ ] Spirit-guide explainer integrates skill-node naming where applicable (per skill-system § 9)
- [ ] LLM-call telemetry per node logged (prompt + response + cohesion_score + attempt number) for downstream evaluation
- [ ] DiskCache hits + misses logged per generation run
- [ ] Cost-per-run metric reported (compares to G12 measurement baseline)
- [ ] Cross-form name uniqueness ≥ 95% (within a generation run, ≤ 5% duplicate skill names across different kits)
- [ ] MIGRATION.md entry authored per ADR-004

---

## 7. What this spec does NOT decide

- **Specific LLM model choice** — Claude 3.5 Sonnet is RECOMMENDED but rocket may select Haiku for cost or another model with star-lord LLM-seam consultation
- **Existing Phase 5 form-level naming behavior** — preserved as-is unless implementation surfaces conflict
- **Visual coalescence (Phase 6) integration** — out of scope per Cycle 12 Option γ; Phase 6 wire-up is v1.1+ candidate
- **Per-form sim re-run after Phase 5 names land** — implementation decision; if names don't affect mechanics, sim is independent
- **Phase 5 calibration for cross-season cohesion** — single-season scope here; cross-season patterns are v1.1+ design
- **T4 keystone narration distinction from spirit-guide narration_metadata (drax Cycle 12 Wave 5)** — spirit-guide narration_metadata covers T4 strategy at form level; skill-node naming per § 2.1 covers per-node skill content; they compose
  - **AMENDMENT 2026-05-26** (`canonical/story/phase-5-t4-narration-amendment-2026-05-26.md`): empirical regen review surfaced that T4 descriptive fields (`manifestation` + `thematic_rationale`) are NULL/empty in v2_narrow_phase_5 output → drax T4AlterationPanel falls through to § 9 template voice. Amendment re-scopes IN: form-level T4 keystone narration LLM pass (1 call per form; ~35 calls/run; ~$0.05-$0.20 added cost; 2-dimension cohesion-validation rubric); fires AFTER parent-spec skill-node naming within Phase 5 sequence. Rocket implements per amendment; jack-ryan Gate-2 validates parent-spec § 6 + amendment § 7 in one pass.

---

## 8. Sign-off

**Author:** gandalf 2026-05-25 (Pattern-B canonical design-spec-as-math)
**Status:** RATIFIED — Matt authorization for Phase 5 calibration spec authoring as regen-gate
**For:** rocket implementation → jack-ryan Gate-2 validation → regen fires → 35-form v2_narrow regenerates with REAL skill names + flavor + effect descriptions (no more placeholders) → meaningful fight-behavior differentiation enabled (skills no longer mechanically equivalent) → T4 post-mortem session 1 reviews substantive skill-tree feel + fight outcomes

**Downstream consumers:**
- rocket (engine generation/skill composition; implements per spec)
- jack-ryan (Gate-2 validation per § 6 acceptance criteria)
- star-lord (LLM-seam coordination; telemetry per § 6)
- gandalf (post-implementation design-fit review; new design-fit pass when regen lands)
- drax (loadout app displays real skill names + flavor + effect descriptions in existing SkillTree components; no drax work required IF rocket emission matches existing schema)
