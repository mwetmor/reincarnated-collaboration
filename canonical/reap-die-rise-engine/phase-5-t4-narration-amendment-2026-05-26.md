# Phase 5 Spec Amendment — T4 Keystone Descriptive Narration (Form-Level)

> **STATUS:** RATIFIED 2026-05-26 — Matt authorization to gandalf for Phase 5 spec amendment cycle fixing T4 keystone descriptive narration gap surfaced in empirical review of v2_narrow_phase_5 regen output

**Authored:** 2026-05-26
**Author:** gandalf (story-and-design steward; design-spec-as-math per gandalf OP § 3.2)
**Pattern:** small-scope spec amendment to existing canonical doc — preserves parent Phase 5 spec authority; adds form-level T4 keystone narration LLM pass as ADDITIONAL Phase 5 sub-pass (not a re-spec)
**Parent doc:** `canonical/story/phase-5-cohesion-judge-calibration-spec-2026-05-25.md` (Phase 5 skill-node-level naming + cohesion validation)

**Authority basis:**
- Matt 2026-05-26 — direct authorization for amendment cycle ("Fire gandalf sub-agent for Phase 5 spec amendment") via KR hive-mind § 4.3 always-channel routing
- Empirical engine inspection 2026-05-26 — `~/Games/reincarnated-engine/exports/v2_narrow_phase_5/classes.json` spot-check 5/5 forms confirm T4 descriptive fields NULL/empty (see § 1.2)
- Empirical drax inspection 2026-05-26 — `T4AlterationPanel.tsx` falls through to § 9 template voice fallback when both `spirit_guide_narration_metadata.thematic_rationale` and top-level `thematic_rationale` are empty (current state across all 35 forms)

**Companion docs:**
- `canonical/story/phase-5-cohesion-judge-calibration-spec-2026-05-25.md` § 7 (this amendment re-scopes IN what § 7 marked out-of-scope: "T4 keystone narration distinction from spirit-guide narration_metadata")
- `canonical/story/skill-system-2026-05-24.md` § 9 (spirit-guide explainer pattern — the existing canon this amendment operationalizes for the LLM-narration pass)
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` § 5 (named-bearer discipline — informs cohesion-validation kit-identity dimension)
- `~/Games/reincarnated-engine/src/reincarnated/generation/skill_tree.py:611` (the empty-string assignment site; comment "Phase 5 fills via spirit-guide explainer" — this amendment defines that fill)
- `~/Games/reincarnated-engine/src/reincarnated/generation/t4_wireup.py:683` (`_build_spirit_guide_narration` builds dict shell with `thematic_rationale=primary.thematic_rationale` and `manifestation=None` — both populated by this amendment's LLM pass)
- `~/Games/reincarnated-loadout/src/components/SkillTree/T4AlterationPanel.tsx:87-91` (drax fallback chain — this amendment fills the L6-enrichment path so § 9 template fallback no longer fires)

---

## 0. TL;DR

Phase 5 spec § 7 explicitly scoped OUT T4 keystone descriptive narration ("they compose"). Empirical regen output shows the descriptive PROSE fields are NULL/empty across all 35 forms in v2_narrow_phase_5 — schema-shell is wired (`spirit_guide_narration_metadata` dict present; `has_mechanic_alteration: True`; `alteration_type` enum; `narrative_hooks` populated; `spirit_guide_explainer_template` populated) BUT the prose fields are unpopulated:
- `spirit_guide_narration_metadata["thematic_rationale"]` is empty string
- `spirit_guide_narration_metadata["manifestation"]` is None (the PROSE slot per § 9 explainer pattern; distinct from top-level `t4_alteration_output["manifestation"]` which is the TIER LABEL enum `"T4_active"` / `"rank2_passive"` / `"rank3_passive"` semantic — see § 2.1 disambiguation)
- `t4_alteration_output["thematic_rationale"]` is empty string (top-level prose mirror)

Root cause: `skill_tree.py:611` creates `T4Alteration` with `thematic_rationale=""` and comment "Phase 5 fills via spirit-guide explainer" — but Phase 5 never had a spec'd LLM-narration pass for the form-level T4 keystone. Schema designed for it; pass never built. The `_build_spirit_guide_narration` machinery (t4_wireup.py:683-713) ALSO leaves `spirit_guide_narration_metadata["manifestation"]` as None with the comment "set by caller from AlterationOutput.manifestation" — but no caller exists. This amendment specs the caller.

This amendment defines:

1. **Output schema** for form-level T4 narration (4 fields populated per form; matches existing schema-shell so drax `T4AlterationPanel` consumes without changes)
2. **LLM input context** (kit identity + algorithm strategy output + named-bearer + mechanical substrate + already-named skill-tree nodes from § 2.3 of parent spec)
3. **LLM prompt template** (single call per form; ~35 calls per generation run)
4. **Light cohesion-validation** (2-dimension rubric — kit-identity + thematic-rationale; chain-progression dimension N/A because T4 keystone is form-level not chain-level)
5. **Sequencing** within Phase 5 (T4 narration fires AFTER skill-node naming — establishes rationale per § 2.6)
6. **Cost projection** (~35 additional calls / generation; ~$0.05-$0.20 added cost; within G12 cost guard)
7. **Acceptance criteria** for rocket implementation (small addition to parent spec § 6)
8. **Cross-seam coordination note** (drax requires no work; existing T4AlterationPanel consumes the new populated fields)

Rocket implements per amendment + parent spec. jack-ryan Gate-2 validates per § 7 acceptance criteria additions.

**Estimated rocket effort:** ~30-60 min implementation (LLM call wiring + template + cohesion check) + integration with skill-node naming pass + smoke validation; minor incremental cost relative to parent Phase 5 implementation work.

---

## 1. The gap (empirical finding 2026-05-26)

### 1.1 Schema state — wired but unfilled

The export schema (`export/schemas.py:89-100`) defines:

```python
@dataclass
class ExportAlterationOutput:
    strategy_type: str
    strategy_params: dict[str, Any]
    applied_axis_targets: list[str]
    eta_score: float
    thematic_rationale: str       # human-readable rationale for spirit-guide explainer (§ 9)
    manifestation: str | None = None    # T4 manifestation tier label (e.g. "rank3_passive")
    off_hand_contract: dict[str, Any] | None = None
    spirit_guide_narration_metadata: dict[str, Any] | None = None  # § 9 explainer pattern fields
    gamora_combatant_fields: dict[str, Any] | None = None
```

The `spirit_guide_narration_metadata` dict shape (per `t4_wireup.py:_build_spirit_guide_narration`):

```python
{
    "has_mechanic_alteration": bool,
    "alteration_type": str | None,                  # currently strategy_type enum pass-through ("DEFENSIVE_CONVERSION"); amendment replaces with narrated label
    "thematic_rationale": str | None,               # PROSE narration — currently inherits empty string from skill_tree.py:611
    "manifestation": str | None,                    # PROSE narration — currently None per t4_wireup.py:707 "set by caller from AlterationOutput.manifestation" (caller never built)
    "spirit_guide_explainer_template": str | None,  # template ID (populated)
    "narrative_hooks": list[str],                   # tag list (populated)
    "secondary_alteration_types": list[str],
}
```

**Semantic disambiguation:** the nested `manifestation` field (inside `spirit_guide_narration_metadata`) is the PROSE-narration slot per § 9 explainer pattern. The top-level `t4_alteration_output["manifestation"]` is the TIER LABEL enum (`"T4_active"` / `"rank2_passive"` / `"rank3_passive"`) populated by `mechanic_alteration.py:_manifestation_from_tier`. These are TWO different semantics that happen to share the field name. Amendment fills the nested PROSE slot only; top-level tier-label slot is unchanged.

### 1.2 Empirical state — descriptive fields NULL/empty across all forms

Spot-check 5 forms (0-4) in `~/Games/reincarnated-engine/exports/v2_narrow_phase_5/classes.json`:

| Form | strategy_type | thematic_rationale | manifestation | narrative_hooks | spirit_guide_explainer_template |
|---|---|---|---|---|---|
| Rampart Knight | DEFENSIVE_CONVERSION | `""` | None | `[iron_will, endurance, armor]` | `stat_layer_remap` |
| Blade of Empires | DEFENSIVE_CONVERSION | `""` | None | `[iron_will, endurance, armor]` | `stat_layer_remap` |
| Menuki Bladedancer | TRADE_OFF | `""` | None | `[reliability, consistency, no_crits]` | `hit_crit_regime_change` |
| Khyber Shadow Dancer | TRADE_OFF | `""` | None | `[reliability, consistency, no_crits]` | `hit_crit_regime_change` |
| Dueling Pistoleer | DEFENSIVE_CONVERSION | `""` | None | `[iron_will, endurance, armor]` | `stat_layer_remap` |

Pattern uniformity across all 5 spot-checked: **`thematic_rationale` empty string; `manifestation` None.** Mechanical machinery (strategy_type, gamora_combatant_fields, narrative_hooks, explainer_template) populated; descriptive narration machinery unpopulated.

### 1.3 Root cause — `skill_tree.py:611` empty-string assignment + missing Phase 5 LLM pass

```python
# skill_tree.py line 611 — T4Alteration construction inside T4Slot generation
alteration = T4Alteration(
    strategy_type=strategy_type,
    strategy_params=self._default_params(strategy_type),
    estimated_eta=0.5,          # Layer 6 computes real η
    thematic_rationale="",      # Phase 5 fills via spirit-guide explainer
)
```

The comment explicitly defers `thematic_rationale` to "Phase 5 fills via spirit-guide explainer" — but parent Phase 5 spec § 7 marked this OUT of scope. Schema designed for the LLM pass; pass never spec'd or built.

Note: `mechanic_alteration.py` strategy classes DO produce static `thematic_rationale` strings inside `generate_alteration()` (e.g., `"HP-economy archetype with {element}-element affinity. All skill costs draw from HP pool; mana management replaced by life-wager discipline."`) — but those are called by a different code path (`select_mechanic_alteration`) not by `t4_wireup.apply_t4_alteration_to_combat()` which consumes the empty-string T4Alteration from skill_tree construction.

**Two viable fill paths exist:**
- **Path A (static template):** wire `mechanic_alteration.py` strategy-class `generate_alteration()` output (which DOES produce static `thematic_rationale` strings + tier-label `manifestation`) into the active T4 emission path. Cheap; zero LLM cost; per-strategy uniformity (not per-kit identity).
- **Path B (LLM narration per form):** spec a Phase 5 LLM pass that consumes kit identity + algorithm output + named-bearer + skill-tree context to produce kit-specific rationale and manifestation PROSE. More expensive; richer; per-kit varied.

**This amendment specs Path B** — Path A's per-strategy uniformity would produce 35 forms × ~5 strategy-types = effectively only ~5-15 distinct rationale strings across the entire generation run (sub-grouped further by element / cultural-tradition variants from `mechanic_alteration.py` template string interpolation). For a player experience anchored on "this T4 keystone defines THIS kit's identity," per-kit narration is the design intent. Static templates are an acceptable Path A fallback IF the LLM pass fails or budget rejects, but Path B is the spec.

**Path-A flow currently inactive (empirical observation):** the `emit_cross_seam_fields` function (`t4_wireup.py:992-1056`) has a code path at lines 1037-1048 that WOULD populate `thematic_rationale` + `manifestation` from a non-None `AlterationOutput` (the mechanic_alteration.py output with static templates), but the empirical v2_narrow_phase_5 output shows `alteration_output is None` is the active path (lines 1049-1051 else branch) because `t4_alteration_output["manifestation"]` is None across all forms. **Rocket investigation recommendation:** identify why `alteration_output is None` in the current emission path — this may surface a separate engine wiring gap (existing AlterationOutput-bearing code path is not threading through to emit_cross_seam_fields). If that wiring is fixed AND Path B (this amendment) lands, the emission path becomes:
1. `alteration_output` non-None → top-level `manifestation` = tier label (`"T4_active"` etc.) per `mechanic_alteration.py:_manifestation_from_tier`
2. `_build_spirit_guide_narration` populates dict shell with PROSE narration from LLM call (Path B; THIS AMENDMENT)
3. `emit_cross_seam_fields` line 1047 currently OVERWRITES `narration["manifestation"]` with `alteration_output.manifestation` (tier label) — **this overwrite is a BUG when combined with Path B**; rocket must remove the overwrite to preserve LLM-narrated prose in the nested manifestation slot. Suggested fix: line 1047 becomes either `if narration.get("manifestation") is None: narration["manifestation"] = alteration_output.manifestation` (only fill if no LLM prose lands) OR remove the overwrite entirely and let the prose-slot remain LLM-narrated.

### 1.4 Loadout consequence (player-facing impact)

drax `T4AlterationPanel.tsx:87-91` fallback chain:

```typescript
const spiritGuideNarration: string | null =
    narrationMeta?.thematic_rationale       // L6 enrichment path
    ?? alteration.thematic_rationale        // Cycle 11 fallback
    ?? null;                                // triggers § 9 template voice
```

Both upstream fills empty → null → § 9 template voice fallback fires. The template fallback (panel lines 198-205):

> "Summoner, you may have noticed — your spirit has unlocked something truly unique and meaningful. This {strategyLabel.toLowerCase()} defines how your entire kit operates at its peak. If you would like a walkthrough, I can explain how to help them make the most out of it."

This is the **generic § 9 voice** — a placeholder fallback authored to bridge the gap until engine-side narration lands. It is NOT kit-specific. Matt sees the same template voice across all 35 forms with only `{strategyLabel}` varying. The "Spirit Guide unlocked something truly unique" promise is undermined when the same line appears for every kit. The amendment closes this gap.

---

## 2. Amendment — form-level T4 keystone narration LLM pass

### 2.1 Per-form output schema

Per form (one LLM call per kit; ~35 calls per generation run), Phase 5 produces:

```python
@dataclass
class T4KeystoneNarration:
    has_mechanic_alteration: bool           # True if form has a T4 alteration (always True post-§-8); False for pre-§-8 forms
    alteration_type: str                    # human-readable label (~2-5 words; e.g., "Blood-Pact Conduit", "Resolute Edge", "Phoenix Heart")
    manifestation: str                      # 1-2 sentence narrative prose (~25-50 words); what the alteration LOOKS / FEELS like in play; sensory + kinetic; player-facing
    thematic_rationale: str                 # 1-sentence prose (~15-30 words); why THIS alteration fits THIS kit's identity (cultural-tradition + named-bearer + element resonance)
```

**Field placement in existing schema — semantic disambiguation:**

CRITICAL: the existing engine schema has TWO `manifestation` semantics that must be disambiguated:

| Field path | Current semantic | This amendment's treatment |
|---|---|---|
| `t4_alteration_output["manifestation"]` (top-level) | TIER LABEL enum: `"T4_active"` / `"rank2_passive"` / `"rank3_passive"` (per `mechanic_alteration.py:_manifestation_from_tier`) | UNCHANGED — preserves tier-label semantics; populated by existing `mechanic_alteration.py` strategy classes via `_manifestation_from_tier(tier_coefficient)` |
| `spirit_guide_narration_metadata["manifestation"]` (nested) | PROSE NARRATION (currently None per `t4_wireup.py:707` comment "set by caller from AlterationOutput.manifestation" — that wiring was never landed) | **THIS AMENDMENT FILLS** — LLM-narrated prose (1-2 sentence; ~25-50 words; what the alteration looks/feels like in play) |

This dual-use was the source of Matt's empirical-finding ambiguity. The existing `_build_spirit_guide_narration` (t4_wireup.py:683-713) was designed to put prose narration into `spirit_guide_narration_metadata["manifestation"]` (the comment "set by caller from AlterationOutput.manifestation" at line 707 implies the caller would override with richer prose) — but no caller exists. This amendment specs that caller as a Phase 5 LLM pass.

**Final field placement:**

- `has_mechanic_alteration` → `spirit_guide_narration_metadata["has_mechanic_alteration"]` (already populated; LLM doesn't override; passed in context)
- `alteration_type` (label) → `spirit_guide_narration_metadata["alteration_type"]` (REPLACES current enum-pass-through; drax `STRATEGY_LABELS` dict in T4AlterationPanel becomes fallback when null)
- `manifestation` (PROSE; ~25-50 words) → `spirit_guide_narration_metadata["manifestation"]` ONLY (top-level `t4_alteration_output["manifestation"]` PRESERVED for tier-label semantics; does NOT mirror prose)
- `thematic_rationale` (PROSE; ~15-30 words) → BOTH top-level `t4_alteration_output["thematic_rationale"]` AND `spirit_guide_narration_metadata["thematic_rationale"]` (set to same string — `thematic_rationale` has consistent prose semantics across both schema surfaces; drax fallback chain reads L6 path first per `T4AlterationPanel.tsx:87-91`)

**Critical schema-compat note:** the existing dual-field redundancy in `_build_spirit_guide_narration` (t4_wireup.py:706) sets `spirit_guide_narration_metadata["thematic_rationale"]` from `primary.thematic_rationale` (AlterationRecord field). The L6 path mirrors the top-level `thematic_rationale` field. **Amendment preserves this pattern for `thematic_rationale`** — the LLM pass writes to ONE source (the AlterationRecord's `thematic_rationale` field), and the existing `_build_spirit_guide_narration` machinery propagates to both consumption surfaces. Rocket changes the SOURCE for `thematic_rationale` (LLM-narrated string instead of static empty-string); propagation machinery unchanged.

**For `manifestation` prose, NO existing AlterationRecord field carries the prose** — the AlterationRecord field used at line 925 is `thematic_rationale`, and AlterationOutput's `manifestation` is the tier-label semantic. Rocket adds a new prose-source field (suggested name: `AlterationRecord.manifestation_narrative` OR pass through a new field on the LLM-narration result object) and the `_build_spirit_guide_narration` machinery sets `spirit_guide_narration_metadata["manifestation"]` from this new prose source. **Top-level `t4_alteration_output["manifestation"]` retains tier-label semantics; no naming collision because the prose lives only inside the `spirit_guide_narration_metadata` dict.**

### 2.2 Field naming clarification

**`alteration_type` as label, not enum:**
- `strategy_type` (existing field) holds the enum: `"DEFENSIVE_CONVERSION"`, `"TRADE_OFF"`, `"GEOMETRY_COLLAPSE"`, `"RESOURCE_CONVERSION"`, `"ELEMENT_CONVERSION"`, `"DEFENSIVE_TRADEOFF"`
- `alteration_type` (this amendment) holds the per-kit narrative label: `"Blood-Pact Conduit"`, `"Resolute Edge"`, `"Phoenix Heart"`, etc.

drax T4AlterationPanel currently reads `alteration.strategy_type` and maps through `STRATEGY_LABELS` dict for display. Post-amendment, drax SHOULD prefer `spirit_guide_narration_metadata.alteration_type` (the LLM-narrated label) and fall back to `STRATEGY_LABELS[strategy_type]` if null. **This is a small drax follow-on** to optionally surface the narrated label — but NOT a blocker. If drax does not update, the panel continues to show `STRATEGY_LABELS[strategy_type]` (e.g., "Defensive Conversion") and the manifestation prose still surfaces below it. Cross-seam coordination note § 8.

### 2.3 LLM input context per T4-narration call

```python
T4NarrationInputContext = {
    # Kit identity (from form-level Phase 5 form-naming output + Phase 2/3/6/8)
    "form_name": str,                          # e.g., "Jade Warlord", "Menuki Bladedancer"
    "form_kit_summary": str,                   # 1-2 sentence kit identity (from form-level Phase 5 naming)
    "element": str,                            # primary element
    "energy_type": str,                        # mana / rage / charge / focus
    "primary_stat": str,                       # STR / INT / WIS / DEX
    "range_profile": str,                      # close / mid / long
    "tempo_class": str,                        # low / medium / high
    "amplitude_class": str,                    # flat / spiky / variable
    "mechanical_substrate_triple": tuple,      # per L9 — mechanical-only
    "cultural_tradition": Optional[str],       # semantic overlay; informs narration tone
    "named_bearer": Optional[str],             # semantic overlay; named-bearer attribution
    "lineage": Optional[str],                  # named_mythological / generic_cultural / engine-original

    # T4 algorithm output (the mechanic the narration must anchor to)
    "strategy_type": str,                      # algorithm § 8 selection enum
    "strategy_params": dict,                   # algorithm § 8 parameters
    "applied_axis_targets": list[str],         # BC axes the alteration shifts
    "eta_score": float,                        # algorithm η-score (for context — high η means tight algorithmic fit)
    "narrative_hooks": list[str],              # pre-extracted thematic tags from t4_wireup (e.g., [iron_will, endurance, armor])
    "spirit_guide_explainer_template": str,    # template ID for explainer-pattern reference

    # Cross-tree context (skill-node naming output — see § 2.6 sequencing)
    "named_skill_chain_signature": list[str],  # T4-chain (signature chain) skill names from parent spec § 2.1 output (T1-T3 of signature chain)
    "form_all_named_skills": list[str],        # ALL ~10 named skills in this form's tree (for cross-tree thematic anchoring)

    # Static template (Path A fallback) — provided to LLM as STYLE reference, not literal output
    "static_template_rationale": str,          # the mechanic_alteration.py static text (e.g., "HP-economy archetype with fire-element affinity...") — LLM uses as semantic anchor for what to express
}
```

### 2.4 LLM prompt template

```
SYSTEM:
You are writing the SPIRIT GUIDE narration for a Tier-4 keystone alteration in an ARPG.
This is the kit-defining mechanic — the climax of the player's build identity. The narration
appears in the loadout app's T4 Alteration Panel, voiced as the player's Spirit Guide
(the persistent companion who carries memory across reincarnations and explains the
unique mechanical features of each new form).

Form identity:
- Name: {form_name}
- Kit summary: {form_kit_summary}
- Element: {element}; energy: {energy_type}; primary stat: {primary_stat}
- Range: {range_profile}; tempo: {tempo_class}; amplitude: {amplitude_class}
- Cultural tradition: {cultural_tradition or 'engine-original'}
- Named-bearer reference (if applicable): {named_bearer}
- Lineage: {lineage}

Tier-4 keystone alteration (algorithmically selected):
- Strategy type: {strategy_type}
- Parameters: {strategy_params readable list}
- BC axes affected: {applied_axis_targets}
- Algorithmic fit score (η): {eta_score:.2f}
- Pre-extracted narrative hooks: {narrative_hooks}

Static-template semantic anchor (for what to EXPRESS — not literal output):
{static_template_rationale}

This form's named skills (for thematic anchoring; do NOT reuse names):
- Signature-chain skills (T1-T3 leading to this T4): {named_skill_chain_signature}
- All named skills in this kit: {form_all_named_skills}

Voice requirements:
- The Spirit Guide is the in-fiction narrator — speaks WITH the player, not AT them.
- D7 AI-tell discipline: avoid generic LLM-voice tells. No "Behold!", no "magnificent",
  no second-person hyperbole. Anchor on concrete sensory + kinetic detail.
- Cultural-tradition cues if present: surface tradition through verb choice + imagery,
  not stereotype or appropriative shorthand.
- Named-bearer cues if present: subtle reference, not on-the-nose name-drop.

USER (output JSON):
{
  "alteration_type": "<2-5 word kit-specific label for this keystone; e.g., 'Blood-Pact Conduit', 'Resolute Edge', 'Phoenix Heart'; reads as a name THIS kit's spirit would give the technique>",
  "manifestation": "<1-2 sentence narrative; ~25-50 words; what the alteration LOOKS or FEELS like in play; sensory + kinetic; player-facing; written as if observed at the moment of triggering>",
  "thematic_rationale": "<1 sentence; ~15-30 words; why THIS alteration fits THIS kit's identity; cultural-tradition + element + named-bearer resonance; the Spirit Guide explaining the FIT, not the mechanic>"
}
```

### 2.5 LLM model selection

**Primary recommendation:** Claude 3.5 Sonnet (matches parent spec § 2.4 recommendation; narration quality matters more here than at skill-node level because T4 is the form's centerpiece + climactic narration moment).

**Alternative:** Claude 3.5 Haiku acceptable IF cost guard tight; quality risk is slightly higher than skill-node-level Haiku because T4 narration is the panel's anchoring prose. Recommend Sonnet unless G12 cost-budget rejects.

**Cost projection (this amendment, additive to parent Phase 5 spec):**
- ~1 call per form × 35 forms = ~35 calls per generation run
- ~600-1500 tokens per call (combined prompt + completion; longer than skill-node calls due to richer kit-context input)
- Total: ~21K-52K tokens per generation run
- Cost @ Claude 3.5 Sonnet: ~$0.06-$0.20 per generation run
- Cost @ Claude 3.5 Haiku: ~$0.015-$0.05 per generation run

**Composition with parent Phase 5 spec cost (~$0.50-$2.00/run Sonnet):** amendment adds ~5-10% to parent Phase 5 LLM cost. **Well within G12 cost guard** (G12 measurement: ~0.13% repeat rate; first-run dominant; total per-generation-run cost still <$2.50 worst-case at Sonnet).

### 2.6 Sequencing — T4 narration fires AFTER skill-node naming (within Phase 5)

**Decision:** T4 keystone narration call fires AFTER the form's skill-node naming pass (parent spec § 2) completes.

**Reasoning:**

1. **Climactic narration benefits from chain-progression context.** T4 keystone is the apex of the signature chain (T1 → T2 → T3 → T4 progression). The narration is more powerful when it can reference the T4-chain's predecessor skill names as thematic build-up. Skill-node naming establishes those names; T4 narration anchors to them via the `named_skill_chain_signature` context field (§ 2.3).

2. **Cross-tree thematic coherence requires the tree to exist.** The form's ALL named skills (`form_all_named_skills` context field, ~10 names) establish the kit's narration vocabulary (cultural-tradition language patterns; named-bearer references the LLM used; element imagery). T4 narration should match this vocabulary rather than diverge from it. Firing T4 narration AFTER means the tree's vocabulary is available for T4 to anchor to.

3. **Mechanical decisions are pre-committed.** The T4 strategy_type, strategy_params, applied_axis_targets, eta_score, narrative_hooks, and spirit_guide_explainer_template are ALL determined upstream (algorithm § 8 + skill_tree.py construction + t4_wireup `_build_spirit_guide_narration`). The LLM call only fills the descriptive surface; sequencing relative to skill-node naming is purely a context-quality question, not a mechanical-correctness question.

4. **Cohesion validation can compare against tree.** § 3 cohesion-validation kit-identity dimension benefits from the named-tree existing — judges whether T4 narration coheres with the form's already-established skill-tree voice.

**Operational sequence within Phase 5 (amendment to parent spec § 4 calibration approach):**

```
1. Form-level naming (form_name, form_kit_summary, flavor element flavoring) — parent spec § 1.1
2. Skill-node naming (per-node LLM calls; ~8-10 nodes per form; cohesion-judge) — parent spec § 2
3. T4 keystone narration (THIS AMENDMENT; 1 LLM call per form; cohesion-judge per § 3) ← NEW
4. Spirit-guide narration metadata propagation (existing t4_wireup machinery, now sourcing from #3 output)
5. Cross-form name uniqueness check (parent spec § 6 acceptance criterion)
```

### 2.7 Re-roll policy

Follow parent spec § 4 re-roll pattern with these specifics:
- First-attempt PASS target: ≥75% (slightly higher than skill-node-level target because the call has richer context and stronger thematic anchoring)
- Re-roll attempt cap: 3 (matches parent spec)
- FAIL fallback: populate from `mechanic_alteration.py` static template (Path A from § 1.3) — player still sees per-strategy generic prose rather than § 9 template fallback; logged for design review

---

## 3. Cohesion validation — 2-dimension simplified rubric

T4 keystone narration is FORM-LEVEL (one per kit), not CHAIN-LEVEL. Parent spec § 3 5-dimension rubric does not fully apply:
- **Chain-progression cohesion (§ 3.2)** — N/A; T4 narration is the chain climax, not a chain step
- **Mechanical-narration alignment (§ 3.3)** — applicable but lighter (player learns mechanic via mechanic_alteration enum + gamora_combatant_fields surfaces; narration anchors to mechanic but is not the mechanical explainer)
- **Cross-tree thematic cohesion (§ 3.5)** — applicable but checked at form-aggregate level not per-T4

This amendment defines a **2-dimension cohesion-validation rubric** for T4 narration specifically:

### 3.1 Kit-identity cohesion (weight: 0.60)

Does the `alteration_type` label + `manifestation` prose unambiguously read as belonging to THIS kit (named-bearer + cultural-tradition + element + form identity)?

| Score | Criterion |
|---|---|
| 1.0 (PASS) | Label + manifestation reads as THIS kit's signature; could not plausibly belong to another kit; cultural-tradition + element cues integrated naturally; named-bearer reference subtle but recognizable when present |
| 0.6-0.9 (BORDERLINE) | Acceptable but feels somewhat generic OR could plausibly belong to 2-3 other kits with similar elements/traditions |
| 0.0-0.5 (FAIL) | Reads as different kit's identity OR generic D&D/MMO-style filler OR cultural cues misapplied OR appropriative |

### 3.2 Thematic-rationale fit (weight: 0.40)

Does the `thematic_rationale` 1-sentence prose explain why THIS strategy_type fits THIS kit's identity (not generic to strategy_type alone; not generic to element alone)?

| Score | Criterion |
|---|---|
| 1.0 (PASS) | Rationale references kit-specific features (element + cultural-tradition + named-bearer + tempo/range/amplitude) and explains the FIT clearly in one sentence; reads as in-fiction Spirit Guide voice |
| 0.6-0.9 (BORDERLINE) | Rationale present but generic to strategy_type alone OR generic to element alone OR doesn't strongly anchor to kit features |
| 0.0-0.5 (FAIL) | Rationale absent / vacuous / contradicts kit features / breaks Spirit Guide voice |

### 3.3 Aggregate cohesion score

```python
t4_narration_cohesion_score = (
    0.60 * kit_identity +
    0.40 * thematic_rationale_fit
)
```

**Acceptance thresholds:**
- `t4_narration_cohesion_score >= 0.75` → PASS
- `t4_narration_cohesion_score 0.60-0.74` → BORDERLINE; flag for design review (Matt + gandalf review post-generation)
- `t4_narration_cohesion_score < 0.60` → FAIL; re-roll (max 3 attempts; then static-template fallback per § 2.7)

**Why a simpler rubric than parent spec § 3:** T4 narration is FORM-LEVEL not chain-level; the 5-dimension parent rubric (kit-identity, chain-progression, mechanical-narration, cultural-tradition, cross-tree-thematic) collapses for T4 because chain-progression and cross-tree-thematic are evaluated at parent-spec-level (the skill-node naming pass) and mechanical-narration is light (player learns mechanic from enum + gamora fields, not from manifestation prose). The two surviving dimensions (kit-identity, thematic-rationale-fit) are the load-bearing ones for T4.

---

## 4. Calibration sweeps (additive to parent spec § 4)

Following parent spec Discipline #17 + #1 + #18 pattern, additional parameters needing empirical tuning during T4 narration implementation:

| # | Parameter | Initial value | Sweep range | Trigger for tune |
|---|---|---|---|---|
| T1 | T4 narration LLM temperature | 0.75 | 0.6 - 0.9 | Output too generic OR too florid; calibrate post-smoke |
| T2 | T4 narration max_tokens | 300 | 200 - 400 | Truncation observed OR excess verbosity |
| T3 | T4 cohesion-score acceptance threshold | 0.75 | 0.65 - 0.85 | Empirical PASS rate too low/high; aim for ~75-80% first-attempt PASS |
| T4 | `named_skill_chain_signature` context size | 3 (full T1-T3 signature chain) | 2 - 4 | Reduce if context bloat; expand if narration ignores chain |
| T5 | `form_all_named_skills` context size | 10 (all named tree skills) | 5 - 10 | Reduce if context bloat; full tree is the design intent |
| T6 | Named-bearer attribution prominence in prompt | "subtle reference" | explicit / subtle / absent | Player-facing tone test — too on-the-nose vs too subtle |
| T7 | Static-template semantic-anchor inclusion | included | included / excluded | Test if removing increases LLM creativity or reduces alignment |
| T8 | `alteration_type` label uniqueness within generation run | per-kit | per-kit / per-strategy-fallback | Detect if same labels recur across kits → narration not differentiating |

**Rocket calibration approach (additive to parent spec § 4 sequence):**
1. Implement with initial values per above
2. Fire T4-narration smoke (3-5 forms; ~3-5 T4 calls) → measure cohesion-score distribution + re-roll rate + manifestation quality
3. Sweep T1-T8 if smoke surfaces tuning need
4. Re-smoke
5. Fire full 35-form regen WITH parent Phase 5 skill-node naming integrated

---

## 5. What this amendment does NOT decide

- **Engine implementation pattern** (sync LLM call within Phase 5 / async with cache / batch — rocket judgment per existing star-lord LLM-seam infrastructure)
- **Whether drax T4AlterationPanel should display the new narrated `alteration_type` label** (separate small drax follow-on — see § 8 cross-seam note; the manifestation prose lands regardless)
- **Future T4 narration variants for cross-season cohesion** (single-season scope here; cross-season patterns are v1.1+ design per parent spec § 7)
- **Replacing parent Phase 5 § 7 § 9 template voice fallback in drax** (drax fallback chain stays as-is; it now becomes truly a fallback rather than the dominant code path)
- **Adding a T4-keystone-specific spirit-guide explainer beyond the `manifestation` prose** (the manifestation IS the explainer voice per § 2.4 prompt; further explainer-template variation deferred to post-T4-PM1 iteration if Matt requests)
- **Hand-authored T4 narration overrides** (rocket implementation produces algorithmic narration; gandalf/Matt design-review process for hand-authored override candidates is post-T4-PM1 territory)
- **Re-firing existing Phase 5 cohesion-judge calibration** (preserved as-is; this amendment adds T4 narration as ADDITIONAL pass within Phase 5 sequence per § 2.6)

---

## 6. Out-of-scope (per task brief 2026-05-26)

- Flavor element investigation (deferred to Cycle 13 v1.1+; captured in T4 PM1 prep doc § 6 Category 4)
- WeaponSlot fix (drax in parallel via separate sub-agent; Fix 2 per task brief)
- Engine architectural amendments beyond the new T4 narration fields (the schema fields already exist; this amendment only specs the LLM fill)

---

## 7. Acceptance criteria for jack-ryan Gate-2 (additive to parent spec § 6)

Rocket implementation passes Gate-2 (T4 narration sub-criteria; ADDITIVE to parent Phase 5 acceptance) when:

- [ ] T4 keystone narration LLM pass fires for ALL forms in generation run (35/35 in v2_narrow)
- [ ] Per-form output schema § 2.1 populated: `alteration_type` (label, not enum) + `manifestation` (prose) + `thematic_rationale` (prose) all non-empty strings
- [ ] `spirit_guide_narration_metadata["manifestation"]` non-None and non-empty-string across all 35 forms (PROSE; ~25-50 words)
- [ ] `spirit_guide_narration_metadata["thematic_rationale"]` non-empty-string across all 35 forms (PROSE; ~15-30 words)
- [ ] `spirit_guide_narration_metadata["alteration_type"]` non-empty narrated-label string across all 35 forms (replaces enum pass-through with narrated label per § 2.1)
- [ ] `t4_alteration_output["thematic_rationale"]` non-empty-string across all 35 forms (top-level mirror of prose, per § 2.1 dual-field rationale)
- [ ] `t4_alteration_output["manifestation"]` (top-level) preserves tier-label semantics (`"T4_active"` / `"rank2_passive"` / `"rank3_passive"`) — NOT prose; populated by existing `mechanic_alteration.py:_manifestation_from_tier` path; this amendment does NOT change top-level `manifestation` semantics
- [ ] No § 9 template voice fallback fires in drax T4AlterationPanel across all 35 forms (empirical drax-side check — load loadout app + visually inspect 5-10 forms; spirit-guide panel shows narrated prose, not template voice)
- [ ] T4 narration cohesion-judge fires per form + produces `t4_narration_cohesion_score` per § 3.3
- [ ] First-attempt PASS rate ≥ 70% (initial target; tunable per § 4 T3)
- [ ] Re-roll rate ≤ 15% (initial target)
- [ ] Final FAIL rate (after re-rolls; falls back to static-template) ≤ 5% per generation run
- [ ] `alteration_type` label uniqueness ≥ 90% across the 35 forms (catch labels that recur — narration not differentiating kits)
- [ ] LLM-call telemetry per T4-narration call logged (prompt + response + cohesion_score + attempt number)
- [ ] Cost-per-run delta reported (T4 narration additional cost vs parent Phase 5 only baseline)
- [ ] MIGRATION.md entry authored per ADR-004 (engine-side schema-fill behavior change; no SCHEMA change since fields pre-exist)
- [ ] Smoke + full-regen run produces sample output that gandalf design-review reads as kit-specific (gandalf post-implementation design-fit review; analogous to parent Phase 5 spec sign-off downstream)

---

## 8. Cross-seam coordination notes

### 8.1 drax — NO REQUIRED WORK

Current drax `T4AlterationPanel.tsx` consumes the existing schema fields. Once rocket lands this amendment:
- `spirit_guide_narration_metadata.thematic_rationale` populates with LLM-narrated prose → drax fallback chain L6 path returns the narration → § 9 template voice fallback no longer fires → panel displays kit-specific Spirit Guide narration
- `spirit_guide_narration_metadata.manifestation` populates with prose → currently consumed only via `STRATEGY_LABELS` lookup path (which uses `strategy_type` enum, not narrated label); see § 8.2 OPTIONAL drax follow-on

**No drax blocker.** The manifestation prose lands in the panel via the existing thematic_rationale fallback chain because `_build_spirit_guide_narration` propagates source field → both consumption surfaces.

### 8.2 drax — OPTIONAL small follow-on (post-amendment, separate work)

If drax wants to surface the narrated `alteration_type` label (e.g., "Blood-Pact Conduit") in the panel header alongside or instead of the enum-derived label ("Resource Conversion"):

```typescript
// drax follow-on candidate — T4AlterationPanel.tsx:80-81 area
const strategyLabel =
    alteration.spirit_guide_narration_metadata?.alteration_type   // L6 narrated label (preferred when present)
    ?? getStrategyLabel(alteration.strategy_type);                // STRATEGY_LABELS enum fallback
```

This is a 2-line change. **Not a blocker; not in scope of this rocket amendment.** Surfaced for drax discretion via knight-rider routing if Matt + drax want the narrated labels surfaced post-PM1.

### 8.3 gamora — NO IMPACT

T4 narration is descriptive prose; doesn't affect `gamora_combatant_fields` or sim arithmetic. gamora seam unchanged.

### 8.4 star-lord — LLM-seam coordination

T4 narration adds ~35 calls per generation run to star-lord LLM seam telemetry. Existing parent-spec LLM-call telemetry pattern extends to T4-narration calls (per § 7 acceptance criteria). No new telemetry schema; rocket adds T4-narration calls to existing log path with `call_type="t4_narration"` distinguisher.

### 8.5 jack-ryan — Gate-2 amendment

§ 7 acceptance criteria above ADD to parent spec § 6. jack-ryan validates BOTH parent Phase 5 skill-node naming AND this amendment's T4 narration fields in one Gate-2 pass post-rocket-implementation.

### 8.6 gandalf — post-implementation design-fit review

Once rocket lands AND jack-ryan PASS-or-WARN: gandalf fires design-fit review on the new T4-narration output across the 35 forms. Reviews:
- Per-kit identity differentiation (do the alteration_type labels distinguish kits, or do they cluster around strategy_type?)
- Spirit Guide voice consistency (does the manifestation prose read as the same in-fiction narrator across kits, or do voice drifts surface?)
- Cultural-tradition + named-bearer integration quality (does cultural / named-bearer attribution land subtle and respectful, or stereotype / appropriative?)
- Cross-kit narrative-hook coverage (do narrative_hooks per kit feel under-utilized in the prose? — feedback to rocket prompt-template refinement)

Design-fit findings inform:
- Next regen calibration sweep (per § 4 T1-T8)
- T4 PM1 session content (this work is upstream of post-mortem)
- Cycle 13 scope-doc inputs

---

## 9. Sign-off

**Author:** gandalf 2026-05-26 (Pattern-A-deep canonical authoring as sub-agent during knight-rider hive-mind cycle; design-spec-as-math seam-owner authority per OP § 3.2)

**Status:** RATIFIED — Matt authorization for Phase 5 spec amendment cycle ("Fire gandalf sub-agent for Phase 5 spec amendment"); KR routing per hive-mind § 4.3 always-channel; engine state empirically inspected (T4 descriptive fields NULL/empty across 5/5 sampled forms) + drax T4AlterationPanel empirically falling through to § 9 template per § 1.4

**For:**
- rocket implementation → adds T4 keystone narration LLM pass to Phase 5 sequence per § 2.6
- jack-ryan Gate-2 → validates parent spec § 6 + this amendment § 7 in one pass
- drax → consumes via existing T4AlterationPanel without required work (§ 8.1); optional follow-on for narrated label surfacing (§ 8.2)
- star-lord → LLM-seam telemetry extension (§ 8.4)
- gandalf → post-implementation design-fit review (§ 8.6)
- T4 post-mortem session 1 → Matt sees kit-specific Spirit Guide narration in loadout app rather than § 9 template voice; substantive review of "does the T4 keystone feel anchored to this kit's identity" becomes possible

**Companion verdict (parent spec):** `canonical/story/phase-5-cohesion-judge-calibration-spec-2026-05-25.md` (RATIFIED 2026-05-25; this amendment extends parent spec; both must be read together for full Phase 5 implementation scope)

**Downstream:** rocket implementation sub-agent fires post-this-amendment (per task brief forward routing); drax WeaponSlot fix fires in parallel via separate sub-agent
