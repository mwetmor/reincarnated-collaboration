# Substrate Identity Declaration — Specification

**Authority:** gandalf (story-and-design steward).
**Status:** **Canonical Layer-1 specification** for the five-layer diversity architecture's foundation. Defines the data shape and authorship discipline for substrate identity declarations.
**Companion docs:** `substrate-expansion-decision-2026-05-17.md` (the substrate set this spec instantiates against); `earth-self-diversity-tension-2026-05-17.md` (Court-as-grace resolution; introduces `court_resonance` field); `archetype-coupling-archaeology-2026-05-17.md` (the convergence vectors this spec defends against); `grouping-layer-vocabulary.md` (L2 grouping vocabulary; this spec extends it).
**Reading order:** § 0 TL;DR → § 1 Architectural position → § 2 The data shape → § 3 Field semantics → § 4 Authorship discipline → § 5 Engine consumption → § 6 Worked example → § 7 Cross-references.

---

## § 0 — TL;DR

**The substrate identity declaration is the Layer-1 commitment manifest** for each substrate in the canonical-7 expansion. It is the single authoritative source for what each substrate *commits to be* mechanically, geometrically, vocabulary-wise, and cosmologically.

The declaration is **designer-authored** (gandalf seam), **small** (~30-40 lines per substrate), and **load-bearing** for the entire diversity architecture downstream:

- Layer 2 (identity-pruned composition) reads declarations to constrain archetype generation
- Layer 3 (diversity gate) reads declarations to inform similarity-metric weighting
- Layer 4 (LLM flavor diversifier) reads declarations as prompt-template input
- Layer 5 (telemetry feedback) reads declarations to identify convergence pressure targets

**The declaration is the *substrate's promise*.** Everything downstream honors it.

### § 0.1 — Three architectural commitments this spec makes

1. **Substrates declare what they ARE; engine generation cannot violate the declaration.** Forbidden mechanics are enforced; geometry affinities are weighted; ailment signatures are bound.
2. **Substrates declare what they DECLINE TO BE; declines are stronger than affinities.** A substrate cannot be talked into producing what it has declared forbidden — the engine fails-loud rather than fall-back-silent.
3. **The declaration is the LLM's mechanical-constraint scaffold.** Layer 4 cannot generate vocabulary that violates the declaration. The LLM creates within the substrate's commitments, not against them.

---

## § 1 — Architectural position

### § 1.1 — Where the declaration sits

The substrate identity declaration is **Layer 1** of the five-layer diversity architecture. It is the foundation. Every other layer reads from it.

```
Layer 1 — Substrate Identity Declarations (gandalf-authored YAML; this spec)
                 ↓ pruning constraints + affinities + forbiddens
Layer 2 — Identity-Pruned Composition (rocket/gamora; reads Layer 1)
                 ↓ kit shape candidates
Layer 3 — Mirror-Match Diversity Gate (gamora; uses Layer 1 weights)
                 ↓ validated archetype set
Layer 4 — LLM Flavor Diversifier (star-lord; reads Layer 1 as prompt-template scaffold)
                 ↓ per-season vocabulary
Layer 5 — Telemetry Feedback (elrond + gamora; pressures Layer 1 weights over time)
```

The declaration is **not** the Layer-2 archetype template (which is composed, not authored). It is **not** the Layer-4 per-season vocabulary (which the LLM generates against the declaration). It **is** the substrate's *identity claim* — the cosmological-and-mechanical commitments that all downstream generation honors.

### § 1.2 — What the declaration is NOT

- **Not the archetype.** Archetypes (lightning_controller, holy_caster, shadow_mage) compose at Layer 2 from substrate identity × role shape. The declaration is upstream of archetype.
- **Not the per-season vocabulary.** L3 vocabulary (per-season cipher; "Stormcaller" / "Threshold-Spark" / "Pressure-Release") is per-season-LLM-generated. The declaration provides scaffold, not content.
- **Not the resistance matrix or balance numbers.** Resistance values, damage modifiers, gear-affix rates are Phase-1 P1 deliverables that *consume* the declaration but live in their own specs.
- **Not the cosmology.** The cosmology (`cosmology-reincarnated.md`) frames *all* substrates; the declaration is per-substrate commitment within the cosmological frame.

### § 1.3 — Why declaration-first, not template-first

The archetype-coupling archaeology surfaced the failure mode of template-first architecture: 14 hardcoded templates → substrate expansion requires authoring 9+ new templates manually, and the resulting archetypes converge to the mean of their authored parameters.

The declaration-first approach inverts this: **substrate identity is the small authored unit (~30-40 lines × 7 substrates = ~210-280 lines total).** Archetypes compose from substrates × roles at runtime. Substrate expansion = author one declaration. Archetype proliferation = automatic.

This is the architectural commitment Path (a) in the substrate-expansion-decision § 5.7 amendment makes explicit.

---

## § 2 — The data shape

The declaration is **YAML** (or YAML-isomorphic JSON) at `reincarnated-engine/config/substrate_identities/<substrate_name>.yaml`. One file per substrate. Designer-authored.

### § 2.1 — Canonical shape (canonical-7 target)

```yaml
substrate: <name>            # canonical substrate name (e.g., fire, water, lightning, holy, shadow)

identity:
  # === MECHANICAL DECLARATIONS ===
  mechanical_signature: [<verb>, <verb>, <verb>, <verb>]
    # 3-5 mechanical primitive verbs the substrate IS bound to express
    # Examples: [chain, propagate, arc, discharge] for lightning
    # Examples: [radiate, consecrate, cleanse, amplify_allied] for holy

  forbidden_mechanics: [<verb>, <verb>, ...]
    # Mechanical primitives the substrate REFUSES to express
    # The engine fails-loud if generation produces a forbidden mechanic
    # Examples: [root, sustained_aura, ground_persist] for lightning
    # Examples: [drain, stealth, corrupt] for holy

  combat_pillar: <pillar_enum>
    # ONE of: HIGH_BURST_LOW_PERSIST / SUSTAINED_PRESENCE_ZONE_DENIAL /
    #         ANCHOR_AND_DISRUPT / KINETIC_REDIRECTION /
    #         REVELATION_AND_AMPLIFICATION / CONCEALMENT_AND_DRAIN /
    #         DIRECT_STRIKE
    # The substrate's combat-feel commitment in one tag

  ailment_signature:
    name: <ailment_name>      # e.g., shock for lightning, consecrate for holy
    category: <hard_control|soft_control|dot|amplification|debuff>
    description: <one_line_description>

  scaling_attribute: <stat>   # intelligence | wisdom | strength
    # Which stat the substrate's damage scales with by default

  # === GEOMETRY DECLARATIONS ===
  geometry_affinities:        # geometry-keyed weights: PREFER / NEUTRAL / AVOID
    <geometry_name>: PREFER
    <geometry_name>: PREFER
    <geometry_name>: AVOID
    # ... etc.
    # Unspecified geometries default to NEUTRAL
    # PREFER = composition-bias multiplier 2.0×; AVOID = 0.1×; NEUTRAL = 1.0×

  # === ROLE AFFINITIES ===
  role_affinities:            # role-keyed affinity scores (0.0 - 1.0)
    damage: 0.7
    support: 0.3
    control: 0.6
    hybrid: 0.5
    # Higher = substrate naturally produces this role; lower = substrate produces less of this role
    # Used by Layer-2 composition to weight (substrate × role) generation frequency

  # === VOCABULARY DECLARATIONS ===
  iconic_verbs: [<verb>, <verb>, ...]
    # 4-8 verbs that LLM (Layer 4) draws from when naming skills / generating prose
    # Examples: ["arcs", "chains", "discharges", "leaps to", "stuns"] for lightning
    # Examples: ["consecrates", "sanctifies", "burns away", "judges"] for holy

  iconic_register: <register_tag>
    # ONE of: martial | mystic | clerical | shadow | scientific | mythic | other
    # Genre vocabulary register the LLM should lean into

  # === COSMOLOGICAL DECLARATIONS ===
  cosmological_commitment: |
    <multi-line poetic commitment statement>
    # 1-3 sentences naming what the substrate IS in the cosmology's terms
    # Read by LLM as prompt scaffold; visible in Spirit Guide voice; player-perceivable
    # Example (lightning):
    #   "The substrate of sudden traversal — what crosses gaps without crossing
    #    the space between. The strike that arrives before the warning."

  court_resonance: |
    <multi-line Court-of-Forms resonance statement>
    # 1-2 sentences naming how the Court remembers forms of this substrate
    # Read by LLM at Court-aware moments (cross-season references in Spirit Guide voice)
    # Example (shadow):
    #   "The Court remembers shadows as the forms that walked alongside what
    #    they did not name."

  # === PAIR-STRUCTURE METADATA (optional; for paired substrates) ===
  paired_with: <substrate_name|null>
    # Name of the opposed substrate, if this substrate is paired (e.g., holy ↔ shadow)
    # null for unpaired substrates (lightning, physical)

  pair_axis: <axis_name|null>
    # Name of the pair axis if paired (e.g., "luminance")
    # Layer 4 LLM uses this to generate axis-coherent vocabulary

# === GROUPING-LAYER LABEL ===
grouping_label: <label>       # the L2 grouping label the substrate maps to
  # ignition | suffusion | bulwark | displacement | impact |
  # [new labels for lightning/holy/shadow per grouping-vocab extension]
```

### § 2.2 — Field requirements

All fields are **required** except:
- `paired_with` — null/omitted for unpaired substrates
- `pair_axis` — null/omitted for unpaired substrates

Unspecified `geometry_affinities` entries default to NEUTRAL.

`role_affinities` must include all four canonical roles (damage/support/control/hybrid). Values may be 0.0 (substrate produces ~none of this role).

---

## § 3 — Field semantics

### § 3.1 — Mechanical declarations

**`mechanical_signature`** — the 3-5 verbs the substrate IS. The composition layer (Layer 2) requires generated kits to include ≥1 ability that expresses ≥1 signature verb. Substrates without signature expression in their kits fail composition validation.

**`forbidden_mechanics`** — the verbs the substrate REFUSES. Layer 2 composition rejects any candidate kit that includes a forbidden mechanic. Fails-loud, not fall-through. This is the principal mechanism preventing inter-substrate convergence.

**`combat_pillar`** — the one-line commitment. Used by Layer 3 (diversity gate) as a similarity-metric coarse axis: archetypes from substrates with the same combat_pillar pass the gate at a higher similarity threshold than archetypes from substrates with different combat_pillars. (Lightning and fire both being HIGH_BURST_LOW_PERSIST is intentional; the gate works harder to push them apart.)

**`ailment_signature`** — the substrate's native ailment. Substrate identity declaration is the *only* authoritative source for new ailments in the engine; the ailment registry (`config/ailments.yaml` per wide-net-coupling-archaeology § 2.2 fix-shape) reads from substrate declarations.

**`scaling_attribute`** — the stat this substrate scales with. Drives Layer-2 stat allocation composition (replaces hardcoded `ELEMENT_SCALING_ATTRIBUTE` per archetype-coupling Coupling #5 fix-shape).

### § 3.2 — Geometry declarations

**`geometry_affinities`** — the substrate's geometry-bias dict. Replaces hardcoded per-archetype `geometry_bias` in `b6_archetype_templates.py` per archetype-coupling Coupling #6 fix-shape. Layer 2 composes `geometry_bias = substrate_affinities ⊙ role_affinities` to derive archetype-level geometry weights.

### § 3.3 — Role affinities

**`role_affinities`** — substrate × role affinity scores. Used by Layer-2 composition to weight which (substrate × role) archetypes get generated more frequently in a season's class rotation. Substrate that has 0.0 affinity for `support` will rarely produce support archetypes; substrate with 0.8 affinity for `support` will produce many.

This is *not* a prohibition — even 0.0 affinity allows the archetype to compose if explicitly requested. It's a *natural-frequency bias*.

### § 3.4 — Vocabulary declarations

**`iconic_verbs`** — vocabulary the LLM draws from. Layer 4 prompts include the substrate's iconic_verbs as anchor vocabulary the LLM extends from. Critical for combatting LLM training-distribution bias (per Legolas literature pass Finding A): explicit iconic vocabulary anchors prevent the LLM from falling back to fire-mage tropes when generating shadow-substrate prose.

**`iconic_register`** — the tonal register. Layer 4 uses this to set prose tone (martial / mystic / clerical / shadow / etc.).

### § 3.5 — Cosmological declarations

**`cosmological_commitment`** — the substrate's claim within the cosmology. Player-perceivable (surfaces in Spirit Guide voice, in Court entries, in loadout substrate descriptions). Designer-authored with care; this is the *poetic anchor* of the substrate.

**`court_resonance`** — how the Court remembers this substrate. Activated by Layer 4 in Court-aware moments (per Earth-Self diversity tension resolution § 6.2). Cross-season Spirit Guide references draw from court_resonance.

### § 3.6 — Pair-structure metadata

**`paired_with`** — the opposed substrate name. For holy ↔ shadow: holy's `paired_with: shadow`; shadow's `paired_with: holy`. For unpaired (lightning, physical): null/omitted.

**`pair_axis`** — the pair's axis name (e.g., "luminance"). Drives resistance-matrix valence (per substrate-expansion-decision § 5.1) and Layer-4 axis-coherent vocabulary generation.

### § 3.7 — Grouping-layer label

**`grouping_label`** — the L2 grouping vocabulary the substrate maps to. Drives Stage-3-cipher LLM prompt construction (Layer 4). Must match a registered label in `grouping-layer-vocabulary.md`. New substrates (lightning/holy/shadow) require either reassignment to existing labels OR new labels authored per the grouping-vocab extension (Task #4 pending).

---

## § 4 — Authorship discipline

### § 4.1 — Who authors

**Gandalf seam.** Substrate identity is design-direction territory; declarations are gandalf-authored (Pattern A or Pattern B per gandalf operating manual). Matt approval required for canonical-status changes.

### § 4.2 — How to author

1. **Read the cosmology** (`cosmology-reincarnated.md`) and the substrate's place in it
2. **Read sibling substrate declarations** to establish register and pattern
3. **Author mechanical commitments first** (signature + forbidden + pillar) — these are the load-bearing fields
4. **Author cosmological commitment with care** — this is the poetic anchor the LLM and player both consume
5. **Author iconic verbs with substrate-specificity** — avoid generic verbs that any substrate could claim; pick verbs the substrate *uniquely* claims
6. **Validate against archetype-coupling-archaeology convergence vectors** — does this declaration's mechanical_signature ∩ forbidden_mechanics meaningfully partition the substrate from siblings?

### § 4.3 — When to revise

Substrate identity declarations are **not lightly revisable.** They are load-bearing; changes propagate to:

- Layer-2 composition outputs (all archetypes for this substrate)
- Layer-3 diversity-gate similarity-metric weights
- Layer-4 LLM prompt scaffold (vocabulary regeneration may be needed)
- Layer-5 telemetry feedback pressure targets
- Player-perceived substrate identity (cosmological_commitment surfaces are player-facing)

Revision protocol:
1. Gandalf authors the change
2. Knight-rider sequences decisions-log entry
3. Jack-ryan Gate 1 review
4. Matt approval (substrate identity is cosmology-load-bearing per § 1.1)
5. Regenerate downstream LLM-vocabulary outputs if revision changes mechanical_signature, forbidden_mechanics, or grouping_label
6. Cross-doc updates (Spirit Guide voice; Court browser surface text)

### § 4.4 — When NOT to revise

- LLM-generated per-season vocabulary that disappoints — that's Layer-4 work, not Layer-1
- Player-frequency dissatisfaction — that's Layer-5 telemetry pressure, not declaration revision
- Specific archetype balance issues — that's Layer-2 composition tuning or numerical balance work

---

## § 5 — Engine consumption

### § 5.1 — Loader

`reincarnated-engine/src/reincarnated/foundation/substrate_identity_loader.py` (new module; rocket implementation):

```python
def load_substrate_identities() -> dict[str, SubstrateIdentity]:
    """Load all substrate identity declarations from config/substrate_identities/*.yaml"""
    # Returns dict keyed by substrate name; each value is a typed SubstrateIdentity dataclass
```

### § 5.2 — Foundation registry integration

Substrate identity loader is consumed by `foundation.get_rotating_elements()` to produce substrate-aware Element objects:

```python
class Element:
    name: str
    identity: SubstrateIdentity  # NEW; loaded from declaration
    # ... existing fields
```

All consumer sites that iterate `foundation.get_rotating_elements()` (per substrate-coupling-archaeology Coupling #10 + #11 GOOD PATTERNS) automatically inherit substrate identity access.

### § 5.3 — Validation

The loader validates declarations at load-time:

- All required fields present
- `mechanical_signature` ∩ `forbidden_mechanics` is empty (no internal contradiction)
- `grouping_label` exists in registered grouping vocabulary
- If `paired_with` is set, the paired substrate exists and is reciprocally paired
- `role_affinities` includes all 4 canonical roles
- `scaling_attribute` is a registered attribute name
- `ailment_signature.name` is unique across all substrates (no two substrates share an ailment)

Validation failures crash boot — fail-loud per Discipline #1 + Discipline-candidate #X.

### § 5.4 — Hot reloading

Substrate declarations are loaded at engine boot. Hot reloading is **not supported** for Phase-0 (declarations are stable). Future Phase-1+ work may add hot reload for live design iteration.

---

## § 6 — Worked example: lightning

A complete substrate identity declaration for `lightning`:

```yaml
substrate: lightning

identity:
  mechanical_signature: [chain, propagate, arc, discharge]
  forbidden_mechanics: [root, sustained_aura, ground_persist, slow_channel]
  combat_pillar: HIGH_BURST_LOW_PERSIST

  ailment_signature:
    name: shock
    category: hard_control
    description: |
      Paralysis-on-arc; brief immobilization triggered by chain-arc damage.
      Chain hops apply shock to each subsequent target.

  scaling_attribute: intelligence

  geometry_affinities:
    branching: PREFER
    arc: PREFER
    bolt_line: PREFER
    chain_lightning: PREFER
    projectile: PREFER
    ground_targeted_circle: NEUTRAL
    cone: NEUTRAL
    area_sustain: AVOID
    vortex_pull: AVOID
    melee_arc: AVOID

  role_affinities:
    damage: 0.7
    support: 0.3
    control: 0.6
    hybrid: 0.5

  iconic_verbs:
    - "arcs"
    - "chains"
    - "discharges"
    - "leaps to"
    - "stuns"
    - "flashes"
    - "strikes"

  iconic_register: scientific

  cosmological_commitment: |
    The substrate of sudden traversal — what crosses gaps without crossing
    the space between. The strike that arrives before the warning.
    Lightning is the substrate of *interruption* — it ends what was about
    to happen by being faster than it could happen.

  court_resonance: |
    The Court remembers Stormcallers as the forms that walked between
    moments, never quite where they had been seen.

  paired_with: null
  pair_axis: null

grouping_label: resonance   # new label per grouping-vocab extension (Task #4 pending)
```

### § 6.1 — What this declaration buys us

- **Layer-2 composition** generates lightning archetypes whose kits prefer branching/arc/bolt geometries, contain ≥1 chain or arc or discharge ability, never include root or sustained_aura mechanics, and scale with intelligence.
- **Layer-3 diversity gate** measures lightning archetypes against fire archetypes (also HIGH_BURST_LOW_PERSIST) with a tighter similarity threshold to enforce push-apart.
- **Layer-4 LLM flavor** prompts with iconic_verbs as anchor vocabulary; LLM generates per-season lightning vocabulary that draws from "arcs / chains / leaps to" register, not fire-mage tropes.
- **Layer-5 telemetry** monitors lightning archetype play distribution; if lightning_controller and wind_controller converge in player data, identity-weight pressure pushes them apart on the high-affinity geometry/role axes.
- **Player perception** of lightning is anchored by cosmological_commitment in Spirit Guide voice + court_resonance in cross-season references; the substrate has a *voice*, not just numbers.

---

## § 7 — Cross-references

- `canonical/story/substrate-expansion-decision-2026-05-17.md` — the substrate set this spec instantiates against (canonical-7)
- `canonical/story/earth-self-diversity-tension-2026-05-17.md` — introduces `court_resonance` field
- `canonical/story/archetype-coupling-archaeology-2026-05-17.md` — the convergence vectors this spec defends against (geometry-bias silent neutralization; stat-allocator fallback; constraint-checker silent skip)
- `canonical/story/substrate-coupling-archaeology-2026-05-17.md` — the substrate-coupling sites whose fix-shapes consume this spec
- `canonical/story/wide-net-coupling-archaeology-2026-05-17.md` — the broader coupling concerns (roles/ailments/grouping-vocab); this spec is the foundation those concerns build on
- `canonical/story/grouping-layer-vocabulary.md` — L2 grouping labels; `grouping_label` field references this
- `canonical/story/cosmology-reincarnated.md` — cosmological frame within which `cosmological_commitment` is authored
- `canonical/story/spirit-guide-voice.md` — voice register that consumes `cosmological_commitment` + `court_resonance` for player-facing prose
- `agentic_orchestration/research/knowledge/diversity-architecture-literature-pass-2026-05-17.md` — Legolas Mode A findings inform `forbidden_mechanics` discipline + `iconic_verbs` anti-bias rationale
- `reincarnated-engine/config/elements.yaml` — current canonical-four registry; substrate identity declarations extend / replace this

**Pending downstream deliverables (after this spec lands):**

- gandalf authors the 7 substrate identity declarations (Task #6; one file per substrate at `config/substrate_identities/<name>.yaml`)
- rocket implements `substrate_identity_loader.py` (Phase-1 P1a)
- rocket integrates substrate identity into `foundation.get_rotating_elements()` (Phase-1 P1a)
- gandalf authors grouping-vocab extension with new labels for lightning/holy/shadow (Task #4 pending)
- gamora consumes substrate identity for Layer-2 composition (Phase-1 P1 generation work)
- star-lord consumes substrate identity for Layer-4 LLM prompt scaffold (Phase-2 LLM-flavor work)
- elrond consumes substrate identity declarations as Layer-5 telemetry-feedback pressure targets (Phase-3 telemetry work)

---

## § 8 — Maintenance protocol

This spec is the authoritative source for substrate identity declaration shape. Changes require:

1. Gandalf authorship of the change
2. Knight-rider sequencing into decisions-log entry
3. Jack-ryan Gate 1 review (architecture-load-bearing)
4. Matt approval
5. Cross-doc updates: rocket loader code, all 7 substrate identity declaration files, decisions-log

The shape is **stable.** Field additions are accepted (new optional fields); field removals or required-field changes require regeneration of all substrate declarations + downstream LLM vocabulary outputs.

Future shape extensions (Phase-1 P2+) candidates:
- `gear_affix_pool_size` — per-substrate affix pool size hint
- `monster_archetype_affinities` — per-substrate × monster-type affinity (parallel to role_affinities for monster generation)
- `trial_boss_kit_seeds` — per-substrate trial-boss anchor patterns
- `cross_substrate_interactions` — explicit interaction rules with other substrates (e.g., lightning conducts through water if elemental-physics is ever adopted)

These are P2+ candidates; not in scope for Phase-1 P1.

---

*Authored 2026-05-17 by gandalf. Specification for substrate identity declarations — Layer 1 foundation of the five-layer diversity architecture. Companion to substrate-expansion-decision, archetype-coupling-archaeology, and earth-self-diversity-tension. The substrate's promise is what it commits to be; the engine honors the promise.*
