# Phase 5 LLM Prompt Templates — Cohesion-Judge (Wave A + Wave B + F-C Inter-Faction Relationships)

> **STATUS:** CURRENT (load-bearing as of 2026-05-27; S4 audit amendment 2026-05-29) — Wave 3 Seam 1 deliverable per dispatch `agentic_orchestration/dispatches/2026-05-27-wave-3-phase-5-cohesion-judge-llm-with-f-c.md`. RE-FIRE after API stream timeout at 658s on prior fire; INFO-1 PM-2 § 13.3 `lexicographic_tiebreak` preamble already landed at engine `0cf4f3a` and is NOT in scope here. **S4 audit (cascade-resumption-3) 2026-05-29 confirmed prompt templates class-free at template-text layer; substrate-input purity precondition documented at § 2.5.**

**Date:** 2026-05-27 (initial); 2026-05-29 (S4 audit amendment)
**Author:** gandalf (story-and-design steward)

## § 0.1 Amendment-pass-record

| # | Date | Author | Amendment scope | Empirical trigger |
|---|---|---|---|---|
| Initial | 2026-05-27 | gandalf | Initial authoring per Wave 3 Seam 1 dispatch (engine commits + dispatch ref in header) | (initial authoring) |
| Amendment 1 (S4) | 2026-05-29 | gandalf | **Cascade-resumption-3 S4 audit pass** per `agentic_orchestration/gandalf/notes/2026-05-29-cascade-resumption-3-class-eradication-authorization.md` Stream S4. Audit verified: § 4 Wave A USER prompt + § 5 Wave B USER prompt + § 6 F-C USER prompt are **class-free at template-text layer**. All three consume substrate-grounded fields only (cluster centroids + cultural lineage + tech level + tone + element distribution + BC axis signature + weapon_type_family + faction-level outputs). § 3 vocabulary discipline already enforces Discipline #45 (no `warrior\|mage\|rogue\|hunter\|paladin\|class taxonomy` etc.) at internal prompt text. **Substrate-input purity precondition** (NEW § 2.5) added — prompts assume substituted variables `{kit_id}` / `{kit_name_placeholder}` / `{rep_kit_X_placeholder}` / `{faction_label_placeholder}` carry class-vocabulary-free substrate per S1 class eradication (substrate-input layer refactor). **Runtime substrate-purity grep acceptance criteria** added at § 4.4 (W-A10) + § 5.4 (W-B8) + § 6.5 (F-C13) — call-construction-time grep against substituted variables prevents class-vocabulary survival via input substrate even if S1 incomplete or future regression. **No prompt template text refactor required**; correctness depends on S1 substrate-input layer eradication landing. Composes with no-classes architectural recommitment (Matt 2026-05-27 verbatim) at substrate-input layer; closes Phase 5 LLM consumption seam in cascade-resumption-3 work program. | Cascade-resumption-3 Stream S4 audit (commit this batch) |

**Authority chain:**
**Authority chain:**
- Matt-gate Path (1) RATIFIED (PM-1 + PM-2 + D-Sharpened LOCKED)
- Matt pre-ratification #2 LOCKED — F-C tonal direction (substrate-evidence-driven 6-enum `relationship_type`; cross-cultural neutrality; D7 AI-tell templated; cosine <0.7 diversity)
- Path III F-C scope addition ratified — Matt verbatim "Let's go with option (III)"
- Cycle 14 quality-orientation: "Engine first. Game second. Phase third." (Move 1)

**Companion docs:**
- `canonical/story/thematic-registry-2026-05-27.md` (registry meta `da56926`; § 5 term-type schema; § 6 element-only fallback; § 7 per-cell sketches; § 9 consumption-pattern spec)
- `~/Games/reincarnated-engine/src/reincarnated/generation/math/phase-5-pm-2-faction-label-assignment-math-2026-05-27.md` § 3.5 (Wave A field spec); § 3.7 D-Sharpened invariance; § 13 G-B primary-pair selection (post-INFO-1 `0cf4f3a`)
- `~/Games/reincarnated-engine/src/reincarnated/export/schemas.py` `ExportFactionCluster` (existing Phase 5 export schema; star-lord `94f8c88` extended with `primary_pair_flag` + `gb_selection_rationale` + `pairwise_distance_distribution`)
- `~/Games/reincarnated-engine/src/reincarnated/llm/phase5_orchestrator.py` (Wave A orchestration scaffold; star-lord Seam 2 will extend with F-C per-pair calls + Wave B per-kit calls)
- `agentic_orchestration/gandalf/notes/2026-05-27-path-iii-faction-assembly-extension.md` § 3 (F-C full spec; LLM prompt sketch § 3.4)
- `agentic_orchestration/research/2026-05-27-cycle-14-sc-3-cohesion-judge-llm-architecture.md` § Recommendation 1 (SC-3 Pattern B PRIMARY)

**Scope of this doc:** the human-readable prompt template specifications for the three Phase 5 LLM call surfaces (Wave A faction-level + Wave B per-kit identity + F-C per-pair inter-faction relationship). Each template specifies SYSTEM prompt + USER prompt assembly + structured output schema + acceptance criteria + composition rules. Star-lord Seam 2 implements the asyncio + AsyncAnthropic + Semaphore wiring per these templates (existing Wave A scaffold at `phase5_orchestrator.py` extends to Wave B + F-C).

**Out of scope:**
- Star-lord Seam 2 implementation work (per-pair LLM call orchestration; cost monitoring; diversity smoke; MIGRATION.md ExportFactionRelationship schema)
- PM-2 amendments (already landed at `0cf4f3a` — `lexicographic_tiebreak` preamble)
- THEMATIC_REGISTRY content (already landed at `da56926` — gandalf cross-cutting closed)
- Phase 7 2-layer joint-gate (separate Phase 7 dispatch)
- Wave 5 production-season fire

---

## § 1 Architecture overview — three LLM call surfaces

Phase 5 cohesion-judge LLM operates across three call surfaces per season. The orchestrator fires Wave A first, then F-C consumes Wave A output for per-pair narrative, then Wave B consumes Wave A + F-C output for per-kit identity within faction context.

```
PM-1 cluster output ──→ Wave A (faction-level)        ──→ ExportFactionCluster.faction_label_canonical
                                ↓                             + faction_identity_narrative
                                ↓                             + faction_thematic_tags
                                ↓
                                + G-B primary_pair_flag (PM-2 § 13)
                                ↓
                          F-C (per-pair) ────────────────→ ExportFactionRelationship.relationship_type
                                ↓                             + tension_narrative
                                ↓                             + shared_history_hook (optional)
                                ↓                             + primary_pair_intensifier (when primary_pair_flag=true)
                                ↓                             + ai_tell_compliance_score
                                ↓
                          Wave B (per-kit identity) ────→ ExportKit.kit_name_canonical (existing)
                                                              + kit_identity_narrative
```

**Volume per season (k ∈ {3, 4} from PM-1 GMM-BIC):**

| Surface | k=3 | k=4 | Token cost per call | Cost contribution |
|---|---|---|---|---|
| Wave A faction-level | 3 calls | 4 calls | ~3-5K tokens | ~$0.10-$0.25 |
| F-C per-pair | 3 pairs | 6 pairs | ~3-5K tokens | ~$0.15-$0.30 |
| Wave B per-kit | ~20-40 kits | ~20-40 kits | ~2-3K tokens | ~$0.30-$1.00 |
| **Per-season total** | ~26-46 calls | ~30-50 calls | — | ~$0.55-$1.55 |

Within SC-3 envelope ($0.50-$5 per season). Cost monitoring is star-lord Seam 2 responsibility (per dispatch acceptance criteria).

---

## § 2 D-Sharpened invariance — load-bearing across all three surfaces

Per PM-2 § 3.7 (engine `7233e0f`), the registry consultation + prompt assembly + LLM call path operates **identically** regardless of whether the kit is substrate-anchored (Sketch F ~32% named-personage allocation) or synthesized (B14.5 V1 primary-loop generated kit).

**Architectural invariant (mandatory for all three prompt templates below):**

- Wave A SYSTEM prompt: **no `substrate_anchored_personage` field exposed** to the LLM. Cluster-level inputs only.
- F-C SYSTEM prompt: **no per-kit anchor metadata** exposed. Faction-level + season-level context only.
- Wave B SYSTEM prompt: kit-level inputs include `weapon_type_family` + `cultural_lineage` + assigned faction context. **NO `substrate_anchored_personage` flag** passed to the LLM. Anchor metadata gating happens at drax loadout summary + star-lord telemetry **downstream of LLM output**, never as an LLM input.

**Player-experience property protected:** the player cannot tell at the name + lore + relationship surface whether a kit (or its cluster, or its inter-faction relationship) came from substrate-anchored vs synthesized lineage. The substrate-anchor signal exists in metadata (drax loadout summary; star-lord telemetry sidecar) but NOT in the LLM-produced narrative surface.

**Gate-2 BLOCK trigger (per PM-2 § 3.7):** any LLM prompt assembly that reads `substrate_anchored_personage` from kit data and routes prompt differently per its presence is a D-Sharpened violation. jack-ryan grep audit pattern at Gate-2: `substrate_anchored_personage` references in `phase5_orchestrator.py` (or any Wave A/B/F-C prompt-assembly call site). Reads at PM-2 layer → invalid; writes at Sketch F allocation layer → valid; reads at drax loadout summary + star-lord telemetry → valid.

---

## § 3 Vocabulary discipline (Discipline #45 LOAD-BEARING)

All three prompt templates below operate under Discipline #45 (generative-architecture vocabulary lock; engineering-disciplines.md § 1700-1745). Prohibited vocabulary in **internal LLM prompt templates AND prompt construction code paths**:

- `class` (as a generative-unit term — Python language keyword `class MyClass:` is exempt; field names like `proxy_geometry_class` are exempt per substrate-infrastructure carve-out)
- `class taxonomy` / `class faction membership` / `class-intrinsic`
- `archetype` as generative-input-label (the THEMATIC_REGISTRY term-type tag `archetype-name` is the **narrative-role label exempt carve-out** per registry § 5; this is the *only* permitted use of "archetype" in the prompt-construction layer)
- `role` (as pre-authored generative taxonomy)
- `warrior` / `mage` / `rogue` / `hunter` / `paladin` / etc. (the class-vocabulary ban list from `canonical/story/thematic-registry-2026-05-27.md` Ground Rule #4)

**Exempt narrative term-type tag usage:** when assembling the THEMATIC_REGISTRY filter for the LLM, the registry's `archetype-name` term-type tag (registry § 5) is allowed AS A TERM-TYPE LABEL — the registry maps narrative roles (e.g., "the wanderer", "the keeper") into the prompt slot. The tag name is metadata about WHERE the vocabulary slots in the assembled name; it is NOT an architectural taxonomy claim. Wave B § 5.2 of this doc and registry § 9.2 document the intended consumption.

**Player-facing output exemption:** the LLM's *emitted* narrative (`faction_identity_narrative`, `tension_narrative`, `shared_history_hook`, `kit_identity_narrative`) is **player-facing output** and may use narrative vocabulary that would be prohibited in internal architecture docs (per `canonical/story/` exemption at engineering-disciplines.md line 1716). Critically: the **prompt that asks the LLM to produce that output** must not itself use prohibited vocabulary as an architectural-layer instruction.

---

## § 2.5 Substrate-input purity precondition (NEW per S4 audit 2026-05-29)

The prompt templates at § 4 (Wave A) + § 5 (Wave B) + § 6 (F-C) are **class-vocabulary-free at template-text layer** per § 3 Discipline #45 enforcement. The templates' correctness depends on a substrate-input purity precondition:

**Precondition:** all substituted variables in the USER prompt assembly carry class-vocabulary-free substrate per Discipline #45. Specifically:

| Substituted variable | Source | Substrate-purity requirement |
|---|---|---|
| `{kit_id}` (Wave B § 5.3) | kit_archive.kit_id | NO class-vocabulary substrings (barbarian / wizard / cleric / monk / knight / fighter / assassin / archer / sniper / fencer / spellsword / mage / caller / etc.) |
| `{kit_name_placeholder}` (Wave B § 5.3) | Phase 2 BC discovery procedural name OR pre-Wave-B placeholder | Same requirement |
| `{rep_kit_X_placeholder}` (Wave A § 4.3) | kit_archive representative kit IDs OR rep summaries | Same requirement |
| `{faction_label_placeholder}` (Wave A § 4.3) | Phase 3 PM-1 fallback label (e.g., "unknown-medieval-unknown-mixed-element") | Same requirement |
| `{weapon_type_family}` (Wave B § 5.3) | Substrate-curated weapon family | Substrate-curated; clean |
| `{cultural_lineage}` / `{modal_cultural_lineage}` | Substrate-curated cultural tradition | Substrate-curated; clean |
| `{element}` / `{dominant_element}` / `{element_distribution}` | Substrate-curated element | Substrate-curated; clean |
| `{bc_axis_signature_compact}` / `{modal_bc_axis_signature_compact}` | BC tuple per qd-engine-bc-axes-lock | Substrate-curated; clean |

**Pre-cascade-resumption-3 violation:** the precondition was empirically violated via ENDGAME_ENCOUNTER_CATALOG class taxonomy (Cycle 13 SC-6 hand-crafted artifact embedding class names in `encounter_id` + `archetype_name` + `intent` + `cohort_notes` per `agentic_orchestration/gandalf/notes/2026-05-29-cascade-resumption-3-class-eradication-authorization.md` § 1). Phase 2 BC discovery inherited class-name embedded `encounter_id` → Phase 4 archive `kit_id` carried class taxonomy → Wave A `rep_kit_X` + Wave B `kit_id` substitutions would have leaked class vocabulary into LLM USER prompts.

**Post-cascade-resumption-3 S1 commitment:** S1 (class eradication at substrate-input layer) refactors the catalog + downstream `kit_id` derivation pipeline + class-name field surfaces. Substrate-purity precondition holds post-S1.

**Runtime enforcement:** § 4.4 / § 5.4 / § 6.5 acceptance criteria add `W-A10` / `W-B8` / `F-C13` runtime substrate-purity grep at call-construction time (star-lord Seam 2 implementation hook). This is the defensive layer — even if S1 incomplete or future regression introduces class vocabulary, runtime grep at prompt-construction catches the violation before the LLM call fires.

**Disc #42a Instance 6 connection:** the substrate-input precondition violation was Instance 6 ROOT-CAUSE finding per `agentic_orchestration/gandalf/pushback/2026-05-28-framing-audit-three-instance-case.md`. § 2.5 makes the precondition explicit so future authors cannot propagate class vocabulary through substrate-input layer without acceptance-criteria refutation.

---

## § 4 Wave A faction-level cohesion-judge LLM prompt template

**Caller:** Phase5Orchestrator Wave A (existing scaffold at `phase5_orchestrator.py` — extends from current Wave A implementation; this section is the canonical spec the implementation references).

**One LLM call per emergent cluster** (D-Separate per PM-2 § 3.3). At k=3 → 3 calls; at k=4 → 4 calls. Calls fire in parallel via Semaphore(10) per existing async infrastructure.

### § 4.1 Registry consumption (per registry § 9.1)

Apply the (element × cultural_lineage) cell filter to the THEMATIC_REGISTRY:

```
dominant_element = argmax(cluster.element_distribution)
dominant_lineage = cluster.modal_cultural_lineage

if cell_present(dominant_element, dominant_lineage):
    # § 7.1-7.15 dense cells; ~20-50 entries across {epithet, motif, archetype-name, place-name, lore-fragment}
    registry_filter = registry["per_cell"][dominant_element][dominant_lineage]

elif cell_sparse(dominant_element, dominant_lineage):
    # § 7.16 SPARSE cells
    registry_filter = (
        registry["element_only"][dominant_element]
        + lineage_adjacent_dense_cell(dominant_lineage)
        + [contamination_watch_flag]  # where annotated per § 4 of registry
    )

elif cell_empty(dominant_element, dominant_lineage):
    # § 7.17 EMPTY cells
    registry_filter = (
        registry["element_only"][dominant_element]
        + meta_tag_substitution(dominant_lineage)  # cross_cultural / unknown / marginal-lineage
    )

else:
    # Fallback safety; defensive
    registry_filter = registry["element_only"][dominant_element]
```

The `registry_filter` is a **bag of vocabulary atoms tagged by term-type** (per registry § 5). Wave A consumes primarily `epithet` + `motif` + `lore-fragment` slots; `archetype-name` + `place-name` reserved for Wave B (per registry § 5 + § 9.2).

### § 4.2 SYSTEM prompt (Wave A)

```
You are a thematic identity synthesizer for an isekai-genre ARPG.

Your task: produce a faction identity for a NATURAL GROUPING discovered by
clustering kits (character forms) that share substrate evidence — cultural
lineage, technology level, tone, and elemental affinity.

CRITICAL CONSTRAINTS

(1) The faction is an EMERGENT cluster — NOT a pre-authored taxonomy. The label
    MUST derive from the cluster's substrate evidence given below.

(2) Draw vocabulary ONLY from the THEMATIC_REGISTRY tokens supplied. Do NOT
    invent new thematic terms. Composition is generative — combine registry
    tokens. Tokens themselves are fixed.

(3) Assemble faction names in the pattern:
       {epithet} {meta-noun} of the {motif}
       OR  the {motif} {meta-noun}
       OR  the {epithet} {meta-noun}
    where {meta-noun} is one of the allowed set:
       order, circle, host, path, vigil, keepers, chosen, legion, covenant.
    Do NOT use {meta-noun} values outside this set. Do NOT invent new ones.

(4) AVOID AI-tell phrases — these mark output as generic LLM cant:
       "Order of [X]" (without substrate grounding)
       "House of [Y]"
       "The Brotherhood"
       "and behold"
       "ancient power"
       "chosen ones"
       "this faction embodies"
       "mystical essence"
       "sacred power"
       "long forgotten"
       "shrouded in mystery"
    The registry provides substrate-grounded alternatives. Use them.

(5) Cross-cultural neutrality: no cultural lineage is intrinsically heroic,
    sinister, or "primitive." Lineage signals tone via the registry's per-cell
    sketches, not via stereotype.

(6) Faction-name length: 2-5 words. Narrative length: 1-2 sentences.
    Thematic tags: 3-5 keywords.

(7) Self-assess the ai_tell_compliance_score (0.0-1.0):
       1.0 = no AI-tell phrases, registry tokens used as primary vocabulary,
             substrate grounding visible in the name and narrative
       0.7 = acceptance threshold per D7 discipline
       <0.7 = call will be regenerated with a diversity-penalty system prompt

(8) Respond with valid JSON only. No markdown fences. No preamble. No
    explanation outside the JSON.
```

### § 4.3 USER prompt (Wave A)

```
CLUSTER_LAYER (substrate evidence — weighted HIGHEST):
  cluster_id: {cluster_id}
  member_count: {member_count}
  modal_cultural_lineage: {modal_cultural_lineage}
  modal_tech_level: {modal_tech_level}
  modal_tone: {modal_tone}
  element_distribution: {element_distribution_compact}
  modal_bc_axis_signature: {modal_bc_axis_signature_compact}

KIT_REPS_LAYER (representative kit substrate — moderate weight):
  rep_kit_1: {rep_kit_1_placeholder}
  rep_kit_2: {rep_kit_2_placeholder}
  rep_kit_3: {rep_kit_3_placeholder}

SUBSTRATE_CONTEXT:
  faction_label_placeholder: {faction_label_placeholder}
  pm1_algorithm: {pm1_algorithm}
  cluster_compactness: {cluster_compactness}
  season_id: {season_id}

THEMATIC_REGISTRY (filtered to element × lineage cell):
  cell_status: {cell_status}   # one of: dense | sparse | empty
  cell_path: {cell_path}        # e.g., "§ 7.1 fire × european" OR "§ 6.1 element-only fire (lineage-fallback)"

  epithet: {epithet_list}
  motif: {motif_list}
  lore-fragment: {lore_fragment_list}

  # archetype-name and place-name slots reserved for Wave B per registry § 9.2

OUTPUT SCHEMA (respond with this JSON shape only):
{
  "faction_name": "<2-5 words; assembled from registry tokens per SYSTEM constraint 3>",
  "faction_identity_narrative": "<1-2 sentences; substrate-grounded; uses registry epithet + motif + paraphrased lore-fragment>",
  "faction_thematic_tags": ["<3-5 keywords; substrate-grounded; registry-vocabulary aligned>"],
  "ai_tell_compliance_score": <0.0-1.0; self-assessment per D7 discipline>
}
```

### § 4.4 Acceptance criteria (per call)

| # | Criterion | Verification |
|---|---|---|
| W-A1 | `faction_name` is 2-5 words | string split; word count in [2, 5] (tolerate [1, 8] with WARN per existing scaffold) |
| W-A2 | `faction_name` uses at least one registry epithet OR motif token | substring match against `registry_filter` epithet + motif lists |
| W-A3 | `faction_name` `{meta-noun}` (if pattern matches) is from allowed set | regex against `(order\|circle\|host\|path\|vigil\|keepers\|chosen\|legion\|covenant)` |
| W-A4 | `faction_identity_narrative` is 1-2 sentences | sentence count in [1, 2] (tolerate 3 with WARN) |
| W-A5 | `faction_thematic_tags` is 3-5 keywords | list length in [3, 5] |
| W-A6 | `ai_tell_compliance_score` ≥ 0.7 | numeric ≥ 0.7; <0.7 triggers regeneration per existing scaffold; max 1 regeneration per existing `MAX_REGENERATION_ATTEMPTS=1` |
| W-A7 | No AI-tell phrase substring match | grep against the AI-tell phrase list in SYSTEM constraint 4; substring match WARN; replicate as cross-cluster check at diversity audit |
| W-A8 | No prohibited Discipline #45 vocabulary in output | grep `\b(class\|warrior\|mage\|rogue\|hunter\|paladin)\b` against output (case-insensitive) |
| W-A9 | D-Sharpened invariance preserved | `substrate_anchored_personage` NOT in SYSTEM or USER prompt (audit at call-construction; Gate-2 grep) |
| **W-A10** (NEW S4 audit 2026-05-29) | **Substrate-input purity precondition runtime grep** — at USER prompt assembly time, grep all substituted variable values (`{rep_kit_1_placeholder}` / `{rep_kit_2_placeholder}` / `{rep_kit_3_placeholder}` / `{faction_label_placeholder}` / `{modal_cultural_lineage}` / etc.) for class-vocabulary substrings | `re.search(r'\b(barbarian\|wizard\|cleric\|monk\|knight\|fighter\|assassin\|archer\|sniper\|fencer\|spellsword\|mage\|caller\|warrior\|rogue\|hunter\|paladin)\b', combined_substituted_text, re.IGNORECASE)` — match triggers Gate-2 BLOCK + halt cascade + surface to Matt queue (substrate-input layer regression beyond cascade-resumption-3 S1 eradication) |

### § 4.5 Composition with G-B primary-pair (Path III)

Wave A produces faction identity FIRST. G-B primary-pair selection (PM-2 § 13) operates on PM-1 cluster centroids; G-B selection runs in parallel with Wave A (no dependency). G-B output (`primary_pair_flag` per cluster) is then consumed by F-C (§ 6 below), not Wave A directly. Wave A is **primary-pair-unaware** — it produces faction identity that stands on its own; primary-pair narrative intensification is F-C territory.

---

## § 5 Wave B per-kit identity LLM prompt template

**Caller:** Phase5Orchestrator Wave B (star-lord Seam 2 implementation; existing Wave A scaffold extended).

**One LLM call per kit** (typically 20-40 kits per season after Phase 4 eviction). Calls fire in parallel via Semaphore(10), gated on Wave A completion (kit calls receive parent faction context).

### § 5.1 Registry consumption (per registry § 9.2)

Apply the **refined** (element × cultural_lineage) cell filter — same cell as Wave A, but Wave B explicitly samples slots Wave A did NOT consume:

```
# Wave B uses kit-level lineage + element when available; falls back to cluster modal
kit_element = kit.element  # primary element
kit_lineage = kit.cultural_lineage  # may differ from cluster modal at the kit margin

if cell_present(kit_element, kit_lineage):
    registry_filter = registry["per_cell"][kit_element][kit_lineage]
else:
    # Wave B falls back to parent cluster's cell (Wave A's filter)
    registry_filter = cluster.wave_a_registry_filter

# Wave B primary slots
archetype_names = registry_filter["archetype-name"]
place_names = registry_filter["place-name"]
secondary_motifs = [m for m in registry_filter["motif"] if m not in cluster.wave_a_consumed_motifs]
```

Wave B primarily consumes `archetype-name` + `place-name` slots; pulls **unused secondary motifs** to avoid token re-use within a single faction (registry § 9.2 token-recycling pattern guard).

### § 5.2 SYSTEM prompt (Wave B)

```
You are naming a single kit (character form) within an already-named faction.

The faction was named in Wave A using cluster-level substrate evidence. You
now name ONE kit within that faction, using:
  - the faction's anchor (faction_name + faction_identity_narrative)
  - the kit's specific substrate vector (BC coords, weapon_type_family, lineage)
  - the THEMATIC_REGISTRY filter (refined to kit element × lineage)

CRITICAL CONSTRAINTS

(1) Use the faction anchor as the THEMATIC FRAME. The kit identity must read
    as a member of the faction — not a separate identity. Faction-coherence
    is load-bearing.

(2) Draw archetype-name and place-name ONLY from the provided registry
    tokens. Compose kit identity from token assembly; do NOT invent new
    thematic terms.

(3) Kit-name assembly pattern:
       {archetype-name} of {place-name}
       OR  the {archetype-name} who {kit-narrative-fragment}
       OR  {archetype-name}, {place-name}
    where the archetype-name and place-name come from the registry filter.

(4) Avoid token re-use within the faction — if Wave A already used a motif,
    Wave B should reach for a different one. The registry filter has already
    been pruned of Wave A's consumed tokens; use what remains.

(5) AVOID AI-tell phrases (same list as Wave A SYSTEM constraint 4).

(6) Cross-cultural neutrality: registry tokens carry lineage-binding via
    per-cell sketch authoring; trust the registry. Do NOT bring training-data
    cultural priors that would conflict with the cell sketch.

(7) Kit-name length: 3-7 words. Narrative length: 1-2 sentences.

(8) Self-assess ai_tell_compliance_score (0.0-1.0); ≥ 0.7 threshold per D7.

(9) Respond with valid JSON only. No markdown fences. No preamble.
```

### § 5.3 USER prompt (Wave B)

```
FACTION_ANCHOR (from Wave A; thematic frame — load-bearing):
  faction_name: {faction_name}
  faction_identity_narrative: {faction_identity_narrative}
  faction_thematic_tags: {faction_thematic_tags}

KIT_LAYER (this specific kit — substrate evidence):
  kit_id: {kit_id}
  weapon_type_family: {weapon_type_family}
  cultural_lineage: {cultural_lineage}
  element: {element}
  bc_axis_signature: {bc_axis_signature_compact}
  kit_name_placeholder: {kit_name_placeholder}

SUBSTRATE_CONTEXT:
  parent_cluster_id: {parent_cluster_id}
  season_id: {season_id}

THEMATIC_REGISTRY (refined cell filter; archetype-name + place-name + secondary motif):
  cell_status: {cell_status}
  cell_path: {cell_path}

  archetype-name: {archetype_name_list}
  place-name: {place_name_list}
  secondary_motif: {secondary_motif_list}   # motifs Wave A did NOT consume for parent faction

OUTPUT SCHEMA (respond with this JSON shape only):
{
  "kit_name_canonical": "<3-7 words; assembled from registry tokens per SYSTEM constraint 3>",
  "kit_identity_narrative": "<1-2 sentences; faction-coherent; substrate-grounded>",
  "ai_tell_compliance_score": <0.0-1.0; self-assessment>
}
```

### § 5.4 Acceptance criteria (per call)

| # | Criterion | Verification |
|---|---|---|
| W-B1 | `kit_name_canonical` is 3-7 words | string split; word count in [3, 7] (tolerate [2, 9] WARN) |
| W-B2 | Uses at least one archetype-name OR place-name token from filter | substring match against filter lists |
| W-B3 | `kit_identity_narrative` is 1-2 sentences (1, 2 tolerate 3 WARN) | sentence count |
| W-B4 | `ai_tell_compliance_score` ≥ 0.7 | numeric threshold |
| W-B5 | No prohibited Discipline #45 vocabulary in output | grep audit |
| W-B6 | D-Sharpened invariance preserved | `substrate_anchored_personage` NOT in SYSTEM or USER prompt; same audit pattern as W-A9 |
| W-B7 | Faction-coherence verified | `faction_name` substring OR ≥1 faction_thematic_tag appears in `kit_identity_narrative` (lightweight cohesion proxy) |
| **W-B8** (NEW S4 audit 2026-05-29) | **Substrate-input purity precondition runtime grep** — at USER prompt assembly time, grep all substituted variable values (`{kit_id}` / `{kit_name_placeholder}` / `{weapon_type_family}` / `{cultural_lineage}` / `{element}` / `{faction_name}` from Wave A / etc.) for class-vocabulary substrings | `re.search(r'\b(barbarian\|wizard\|cleric\|monk\|knight\|fighter\|assassin\|archer\|sniper\|fencer\|spellsword\|mage\|caller\|warrior\|rogue\|hunter\|paladin)\b', combined_substituted_text, re.IGNORECASE)` — match triggers Gate-2 BLOCK + halt cascade + surface to Matt queue (substrate-input layer regression). This is the load-bearing runtime defense at Wave B per-kit layer; kit_id substitution is the highest-risk surface in pre-S1 substrate state |

### § 5.5 Composition with D-Sharpened (CRITICAL)

The Wave B prompt template **does NOT distinguish** between substrate-anchored kits (Sketch F ~32% named-personage allocation) and synthesized kits (B14.5 V1 primary-loop generated). The registry filter is consulted identically. The kit_name_canonical produced is uniform across both populations.

Substrate-anchored kits' personage_name (e.g., a historical figure or canonical literary figure surfaced from the Sketch F allocation) **does NOT enter the Wave B prompt**. It is captured at the Sketch F allocation layer (engine-internal), surfaced as metadata in drax loadout summary + star-lord telemetry sidecar, and never as a Wave B LLM input. Player sees uniform LLM-generated kit names; analytics can attribute the substrate anchor without contaminating the naming surface.

---

## § 6 F-C per-pair inter-faction relationship LLM prompt template (Path III addition)

**Caller:** Phase5Orchestrator (new F-C wave; star-lord Seam 2 implementation per dispatch). Fires AFTER Wave A completes; consumes Wave A outputs + G-B `primary_pair_flag` per pair.

**One LLM call per unordered faction pair** (k choose 2). At k=3 → 3 calls; at k=4 → 6 calls. Calls fire in parallel via Semaphore(10).

### § 6.1 The relationship_type 6-enum specification (gandalf judgment)

Per Matt pre-ratification #2 ("substrate-evidence-driven; no defaulting to 'all enemies'; substrate-distance + lineage-difference vote"), and per gandalf design judgment on the 6-enum exact values:

**Final 6-enum (gandalf judgment, per dispatch Q-W3-G-1):**

| Value | Substrate-evidence trigger | Narrative shape |
|---|---|---|
| `antagonist` | high pairwise Mahalanobis distance + lineage divergence + element-orthogonal | open opposition; one's existence threatens the other's; clean narrative tension |
| `rival` | high pairwise distance + same/adjacent lineage + element-adjacent | shared origin (same cultural soil) + divergent path; "siblings who took different roads" |
| `allied` | low-to-moderate pairwise distance + lineage-compatible + element-complementary | mutual interest binds; cooperation under sustained pressure; not friendship-pure (uneasy allies live here too) |
| `neutral` | moderate distance + no strong lineage or element pull | indifference; awareness without engagement; coexistence without contact |
| `mysterious` | high distance + at least one faction has marginal-lineage or `[contamination-watch]` tag + low named-template anchor density | unresolved relationship; insufficient substrate signal to commit narrative; players left to wonder |
| `parallel` | high distance + cross-cultural fallback + element-divergent + no overlap in named-template anchors | exist in parallel without contact; the kind of factions that would never meet absent the season's framing |

**Why this 6-enum (gandalf judgment, anchored in Diablo IV / PoE / KonoSuba / Mushoku Tensei observation):**

- **`antagonist` separate from `rival`:** PoE's "Wraeclast factions" + Diablo 3's Reaper/Crusader split show that the antagonist (existence threat) vs rival (sibling divergence) distinction lands very differently with players. Conflating them flattens narrative texture. Substrate-distance gates which fires.
- **`mysterious` retained:** isekai convention (Mushoku Tensei's Migurd; Re:Zero's Witch of Envy) shows that *unresolved* faction relationships carry narrative weight specifically by withholding commitment. When substrate signal is thin (marginal-lineage; low named-template anchors), `mysterious` is the substrate-honest output — better than forcing `antagonist` or `neutral` from insufficient evidence. Honors Matt pre-ratification #2 "no defaulting to all enemies."
- **`parallel` separate from `neutral`:** `neutral` implies coexistence within the same narrative frame (indifference under same world-pressure); `parallel` is the recognition that *these factions would never meet in a world without the season's framing*. Earth Self meta-layer (per `canonical/story/earth-meta-layer-2026-05-11.md`) makes `parallel` thematically load-bearing — the seasonal frame is what brings disparate forms together; absent the frame, they exist in parallel.
- **`allied` accepts uneasy-allies + true-allies:** carving uneasy_allies as a 7th enum would inflate decision-space without payoff. Substrate evidence cannot distinguish "uneasy alliance" from "true alliance" reliably; LLM narrative can carry the tonal nuance via tension_narrative wording. 6 enums is the substrate-signal-distinguishable maximum.
- **NOT included — `nemesis` / `progenitor` / `descendant`:** these encode pre-authored mythological taxonomy (Discipline #41 violation). Substrate cannot vote on "progenitor vs descendant" without lineage-time data the engine does not produce. Reject.

**Cross-cultural neutrality binding (per Matt pre-ratification #2):**

The enum has NO "good faction vs evil faction" axis. No cultural lineage is intrinsically antagonist. The LLM must NOT bring training-data priors that map (e.g.) European-medieval-Christian as "default heroic" and Middle-Eastern as "default antagonist" — this is a hard refusal trigger in the SYSTEM prompt below.

### § 6.2 Substrate-distance + lineage-difference vote (input to LLM)

The LLM does not select `relationship_type` from raw cluster centroids — it consumes a pre-computed *substrate vote* (computed star-lord-side before the LLM call):

```
# Computed BEFORE the LLM call; passed as input
substrate_vote = {
    "pairwise_distance": <float; from G-B PM-2 § 13 Mahalanobis output>,
    "pairwise_distance_percentile": <float; this pair's percentile among all season pairs>,
    "lineage_similarity": "same" | "adjacent" | "distant" | "cross_cultural",
    "element_relationship": "shared" | "complementary" | "orthogonal" | "divergent",
    "named_anchor_overlap": "high" | "moderate" | "none",
    "marginal_lineage_flag": <bool; either faction carries marginal-lineage or [contamination-watch] tag>,
    "primary_pair_flag": <bool; True iff this pair is G-B-selected primary_faction_pair>,
}
```

The LLM consumes the `substrate_vote` as input; the LLM selects the `relationship_type` enum value by reasoning over the vote (NOT by raw centroid analysis). This is the **substrate-led discipline at the relationship layer** — LLM is *guided* by computed substrate evidence, not asked to invent evidence.

### § 6.3 SYSTEM prompt (F-C)

```
You are the cohesion-judge for Reincarnated's Phase 5 LLM. Your task: produce
a structured inter-faction relationship narrative for ONE unordered pair of
factions in a season.

CRITICAL CONSTRAINTS

(1) The relationship_type MUST be one of these 6 values; NO other values are
    accepted:
       antagonist, rival, allied, neutral, mysterious, parallel

(2) Select the relationship_type from the SUBSTRATE_VOTE inputs given below.
    Do NOT bring cultural priors from training data. Do NOT default to
    "antagonist" when the vote is ambiguous — when substrate signal is thin
    (low named_anchor_overlap + marginal_lineage_flag set), "mysterious" is
    the substrate-honest answer.

(3) Cross-cultural neutrality (LOAD-BEARING):
    NO cultural lineage is intrinsically antagonist, sinister, or
    "primitive." A European-medieval-Christian faction is NOT default
    heroic; a Middle-Eastern faction is NOT default antagonist;
    East-Asian factions are NOT default mystical; African / Indigenous /
    Pacific factions are NOT default "spiritual." These mappings would
    constitute training-data prior leakage; the SUBSTRATE_VOTE supersedes.

(4) Relationship_type enum semantics:
    - antagonist: open opposition; one's existence threatens the other's.
                  Fires when: high pairwise_distance + lineage divergent +
                  element orthogonal/divergent. NOT a default.
    - rival:      shared origin + divergent path. Fires when: high distance
                  + same/adjacent lineage + element adjacent. "Siblings who
                  took different roads."
    - allied:     mutual interest binds. Fires when: low/moderate distance +
                  lineage compatible + element complementary. Includes
                  uneasy alliances (tension_narrative carries tonal nuance).
    - neutral:    indifference; awareness without engagement. Fires when:
                  moderate distance + no strong lineage or element pull.
    - mysterious: unresolved relationship — insufficient substrate signal.
                  Fires when: high distance + marginal_lineage_flag set +
                  low named_anchor_overlap. The substrate-honest output
                  when the season's evidence does not commit.
    - parallel:   factions exist in parallel; would not meet absent the
                  season's framing. Fires when: high distance + cross_cultural
                  lineage + element divergent + no named-anchor overlap.

(5) tension_narrative is 1-2 sentences. Substrate-grounded. Uses faction
    anchor vocabulary (faction_name + faction_thematic_tags from Wave A).
    Does NOT invent backstory beyond what substrate supports.

(6) shared_history_hook is OPTIONAL (1 sentence; null permitted). Provide
    ONLY if substrate evidence supports it — same lineage + element adjacency
    + named_anchor_overlap high OR moderate. When set, references a SHARED
    substrate origin (e.g., "both drew their first lessons from the long
    burning"). Do NOT invent shared history when substrate is thin.

(7) primary_pair_intensifier is set ONLY when primary_pair_flag=true (1-2
    additional sentences elaborating the central season tension). Otherwise
    return null. The intensifier deepens the tension_narrative; it does NOT
    contradict it.

(8) AVOID AI-tell phrases:
       "bound by ancient grudge"
       "destined to clash"
       "their fates intertwined"
       "shrouded in mystery" (use "mysterious" enum value + concrete
                             tension_narrative instead)
       "for time immemorial"
       "long forgotten"
       "the eternal struggle"
       "primal forces"
       "cosmic balance"
    The faction anchors and registry vocabulary provide substrate-grounded
    alternatives.

(9) Self-assess ai_tell_compliance_score (0.0-1.0); threshold ≥ 0.7 per D7.

(10) Respond with valid JSON only. No markdown fences. No preamble.
```

### § 6.4 USER prompt (F-C)

```
FACTION_A (from Wave A):
  cluster_id: {faction_a_cluster_id}
  faction_name: {faction_a_name}
  faction_identity_narrative: {faction_a_narrative}
  faction_thematic_tags: {faction_a_tags}
  modal_cultural_lineage: {faction_a_lineage}
  dominant_element: {faction_a_element}

FACTION_B (from Wave A):
  cluster_id: {faction_b_cluster_id}
  faction_name: {faction_b_name}
  faction_identity_narrative: {faction_b_narrative}
  faction_thematic_tags: {faction_b_tags}
  modal_cultural_lineage: {faction_b_lineage}
  dominant_element: {faction_b_element}

SUBSTRATE_VOTE (computed pre-call; load-bearing for relationship_type):
  pairwise_distance: {pairwise_distance}
  pairwise_distance_percentile: {pairwise_distance_percentile}
  lineage_similarity: {lineage_similarity}     # same | adjacent | distant | cross_cultural
  element_relationship: {element_relationship} # shared | complementary | orthogonal | divergent
  named_anchor_overlap: {named_anchor_overlap} # high | moderate | none
  marginal_lineage_flag: {marginal_lineage_flag}
  primary_pair_flag: {primary_pair_flag}

SEASON_CONTEXT:
  season_id: {season_id}
  k_clusters: {k_clusters}
  pm1_algorithm: {pm1_algorithm}

OUTPUT SCHEMA (respond with this JSON shape only):
{
  "relationship_type": "<one of: antagonist, rival, allied, neutral, mysterious, parallel>",
  "tension_narrative": "<1-2 sentences; substrate-grounded; uses faction anchor vocabulary>",
  "shared_history_hook": "<optional 1 sentence; null if substrate does not support>" | null,
  "primary_pair_intensifier": "<1-2 sentences IF primary_pair_flag=true; null otherwise>" | null,
  "ai_tell_compliance_score": <0.0-1.0>
}
```

### § 6.5 Acceptance criteria (per call)

| # | Criterion | Verification |
|---|---|---|
| F-C1 | `relationship_type` ∈ {antagonist, rival, allied, neutral, mysterious, parallel} | strict enum match; any other value → regenerate |
| F-C2 | `tension_narrative` is 1-2 sentences | sentence count in [1, 2] (tolerate 3 WARN) |
| F-C3 | `tension_narrative` references at least one faction_name OR faction_thematic_tag | substring match against either faction's anchor |
| F-C4 | `shared_history_hook` null OR 1 sentence | conditional structural check |
| F-C5 | `shared_history_hook` non-null implies lineage_similarity ∈ {same, adjacent} OR element_relationship ∈ {shared, complementary} OR named_anchor_overlap ∈ {moderate, high} | substrate-evidence justification check (WARN if violated; LLM regenerate) |
| F-C6 | `primary_pair_intensifier` null iff primary_pair_flag=false | conditional bijection |
| F-C7 | `primary_pair_intensifier` non-null is 1-2 sentences | sentence count |
| F-C8 | `ai_tell_compliance_score` ≥ 0.7 | numeric threshold; regenerate <0.7 |
| F-C9 | No AI-tell phrase substring match | grep against the F-C SYSTEM constraint 8 list |
| F-C10 | No prohibited Discipline #45 vocabulary in output | grep audit |
| F-C11 | D-Sharpened invariance preserved | no `substrate_anchored_personage` references in F-C prompts; grep audit |
| F-C12 | Cross-cultural neutrality preserved | spot-check at design-quality audit; gandalf reviews relationship_type distribution per lineage-pair across first 3 seasons; if {European, anyOther} pair correlates with antagonist > 50% of fires, neutrality is leaking → prompt amendment |
| **F-C13** (NEW S4 audit 2026-05-29) | **Substrate-input purity precondition runtime grep** — at USER prompt assembly time, grep all substituted variable values (`{faction_a_name}` / `{faction_a_narrative}` / `{faction_a_tags}` / `{faction_a_lineage}` / `{faction_a_element}` + B-side equivalents from Wave A outputs) for class-vocabulary substrings | `re.search(r'\b(barbarian\|wizard\|cleric\|monk\|knight\|fighter\|assassin\|archer\|sniper\|fencer\|spellsword\|mage\|caller\|warrior\|rogue\|hunter\|paladin)\b', combined_substituted_text, re.IGNORECASE)` — match triggers Gate-2 BLOCK. Lower-risk surface than Wave B (F-C consumes Wave A outputs which already passed W-A10); defensive layer against Wave A output regression OR Wave A output not yet S4-audited |

### § 6.6 Distribution acceptance (cross-call; per season)

The dispatch acceptance criteria (per Matt pre-ratification #2) requires distribution health, not just per-call validation:

| # | Cross-call criterion | Threshold | Owner of verification |
|---|---|---|---|
| F-D1 | `relationship_type` distribution NOT "all antagonist" | antagonist ≤ 50% of pairs per season; if >50% across 3+ consecutive seasons, prompt amendment | gandalf design-quality audit at wave-close |
| F-D2 | `tension_narrative` cosine distance average < 0.7 | computed by star-lord via TF-IDF n-gram (2, 4) cosine; per Matt pre-ratification #2 | star-lord Seam 2 diversity smoke |
| F-D3 | `ai_tell_compliance_score` distribution NOT saturated | not all PASS at first impl with no variation; if all calls return ≥0.95 with no <0.7 fires across 3 seasons, the self-assessment is uncalibrated | gandalf + star-lord joint review |
| F-D4 | Cross-cultural-neutrality check | no lineage-pair correlates with single `relationship_type` > 50% | gandalf design-quality audit |

### § 6.7 Composition with primary-pair (G-B)

G-B (PM-2 § 13) selects `primary_faction_pair` via Mahalanobis cluster-centroid distance + tie-breaks (per `lexicographic_tiebreak` preamble at engine `0cf4f3a`). F-C consumes `primary_pair_flag` as input — when set, the LLM produces `primary_pair_intensifier` in addition to the base relationship narrative.

The intensifier is **load-bearing for the season's central narrative tension** (per dispatch `engine-as-general-serial-content-product-2026-05-22.md` § 2.2 faction-pair-season scope). It deepens the relationship_type's tonal weight; player sees the primary pair as the season's dramatic anchor; background pairs carry secondary relationships at less narrative intensity.

`background_faction_pairs` produced by G-B receive F-C calls without intensifier (primary_pair_flag=false; intensifier=null in output). They are rendered at lighter weight in drax loadout summary + faction-detail pages.

### § 6.8 D-Sharpened invariance at F-C (CRITICAL)

The F-C prompt assembly **MUST NOT** read `substrate_anchored_personage` from either faction's cluster data. F-C operates entirely at the faction-anchor + substrate-vote layer. Personage-anchor metadata is downstream-of-LLM (drax + star-lord); never an F-C input.

**Gate-2 BLOCK trigger:** grep `substrate_anchored_personage` in F-C prompt construction code → violation.

---

## § 7 Cross-Character Diversity Audit DETECTION integration

Per Matt pre-ratification #2: "TF-IDF n-gram (2,4) cosine distance per Star-lord Seam 3 current backend; cosine distance average <0.7 across tension_narratives per season; sentence-transformers upgrade path dormant ✅."

### § 7.1 What gets diversity-audited

Per-season, star-lord Seam 2 computes pairwise cosine distance across:

| Surface | Diversity check | Threshold |
|---|---|---|
| Wave A | `faction_identity_narrative` across clusters | average cosine distance ≥ 0.5 (i.e., similarity ≤ 0.5; existing scaffold threshold 0.85 — calibration-pending per registry § 9.3 § Calibration Trigger) |
| F-C | `tension_narrative` across pairs | **average cosine distance < 0.7** (Matt pre-ratification #2 acceptance band; per-season aggregate) |
| Wave B | `kit_identity_narrative` across kits within same faction | average cosine distance ≥ 0.6 (existing scaffold; token-recycling pattern guard per registry § 9.2 § Wave B token-recycling) |

### § 7.2 What happens on diversity failure

| Surface | Failure response |
|---|---|
| Wave A | Re-fire the cluster's Wave A call with diversity-penalty system prompt amendment ("the following faction names are already in use this season — produce a distinguishable identity: {prior_names}"); max 1 regeneration (existing `MAX_REGENERATION_ATTEMPTS=1`) |
| F-C | If season-aggregate cosine distance ≥ 0.7, identify the highest-similarity pair; re-fire that pair's F-C call with diversity-penalty system prompt amendment ("the following tension_narratives are in this season — produce a distinguishable narrative: {prior_narratives}"); max 1 regeneration per pair |
| Wave B | Re-fire the kit's Wave B call with diversity-penalty system prompt amendment naming the conflicting kit_name + the parent faction's other consumed motifs; max 1 regeneration per kit |

### § 7.3 What gets logged for sidecar attribution

Per call, star-lord Seam 2 telemetry records:

- `diversity_check_fired: bool`
- `diversity_check_max_similarity: float`
- `diversity_check_max_similarity_pair: tuple[str, str]` (the two records with highest similarity)
- `regeneration_fired: bool`
- `cell_filter_overlap: list[str]` (the registry cells consulted; cross-faction high similarity is INFORMATIONAL when cell-filter overlap is high — both factions pulled from the same cell, expected)

This composes with existing `ExportFactionCluster.cosine_similarity_max` + `diversity_flag` fields (`schemas.py` lines 638-644) — star-lord Seam 2 extends to F-C and Wave B parallel telemetry.

---

## § 8 D7 AI-tell compliance verification logic

Per dispatch § Seam 1 scope item 5 + jack-ryan Phase 7 canonical lock for `ai_tell_compliance_score` forward-compat with Wave 3 F-C field.

### § 8.1 Threshold spec

- **≥ 0.7:** PASS. Call result is accepted.
- **0.5 ≤ score < 0.7:** WARN. Logged for sidecar review. Call result is accepted at first fire; gandalf design-quality audit at wave-close reviews the WARN distribution.
- **< 0.5:** FAIL. Triggers regeneration with diversity-penalty + AI-tell-elimination system prompt amendment ("the prior call produced a low compliance score; reduce AI-tell phrases from the list and ground vocabulary in substrate"). Max 1 regeneration per existing `MAX_REGENERATION_ATTEMPTS`.

### § 8.2 What gets checked alongside the LLM self-assessment

LLM self-assessment alone is insufficient — the LLM can over-rate its own output (F-D3 cross-call criterion guards against saturation). Star-lord Seam 2 additionally runs **mechanical grep validation** as a sidecar check:

```python
AI_TELL_PHRASES_WAVE_A = [
    "order of", "house of", "the brotherhood", "and behold",
    "ancient power", "chosen ones", "this faction embodies",
    "mystical essence", "sacred power", "long forgotten",
    "shrouded in mystery",
]

AI_TELL_PHRASES_FC = [
    "bound by ancient grudge", "destined to clash", "their fates intertwined",
    "shrouded in mystery", "for time immemorial", "long forgotten",
    "the eternal struggle", "primal forces", "cosmic balance",
]

# Lowercase substring match; case-insensitive; punctuation-tolerant
def ai_tell_grep_check(output_text: str, phrases: list[str]) -> dict:
    lowered = output_text.lower()
    hits = [p for p in phrases if p in lowered]
    return {
        "grep_compliance_pass": len(hits) == 0,
        "ai_tell_phrase_hits": hits,
    }
```

If `grep_compliance_pass=False`, the call result is FAIL regardless of LLM self-assessment score. Mechanical grep takes precedence over self-assessment (jack-ryan Phase 7 canonical lock).

### § 8.3 Combined logic

```
final_compliance = LLM_self_assessment AND grep_compliance_pass

if final_compliance is True AND ai_tell_compliance_score >= 0.7:
    ACCEPT
elif ai_tell_compliance_score >= 0.5 AND grep_compliance_pass:
    ACCEPT + WARN logged for design-quality audit
elif ai_tell_compliance_score < 0.5 OR not grep_compliance_pass:
    REGENERATE (max 1 per existing scaffold)
    if still fails after regeneration:
        FAIL_RECORD logged to telemetry; faction_label_canonical falls back to faction_label_placeholder
        gandalf design-quality audit reviews FAIL_RECORD at wave-close
```

### § 8.4 Sidecar telemetry fields

Per call, the following land in `llm_calls` telemetry (existing infrastructure per `tracked_client.py`):

- `ai_tell_compliance_score`: LLM self-assessment (float 0.0-1.0)
- `grep_compliance_pass`: mechanical check (bool)
- `ai_tell_phrase_hits`: list of phrases found (list[str])
- `final_compliance_status`: ACCEPT | ACCEPT_WARN | REGENERATE | FAIL_RECORD
- `regeneration_count`: 0 | 1
- `regeneration_reason`: low_self_assessment | ai_tell_grep_fail | diversity_collision

---

## § 9 Composition with PM-2 + star-lord Seam 2

### § 9.1 Phase5Orchestrator integration sequence

```
orchestrate_phase5(season_state):
    # Step 1: Wave A fires (D-Hybrid + D-Separate; existing scaffold extended)
    wave_a_results = await fire_wave_a_parallel(
        clusters=season_state.pm1_clusters,
        registry=THEMATIC_REGISTRY,
        semaphore=Semaphore(10),
    )
    # Wave A populates ExportFactionCluster.faction_label_canonical + narrative + tags

    # Step 2: G-B primary-pair selection (PM-2 § 13; rocket impl)
    gb_result = compute_gb_primary_pair(season_state.pm1_clusters)
    # gb_result populates ExportFactionCluster.primary_pair_flag + gb_selection_rationale

    # Step 3: Compute substrate_vote per pair (star-lord Seam 2)
    substrate_votes = compute_substrate_votes(
        clusters=season_state.pm1_clusters,
        gb_result=gb_result,
    )

    # Step 4: F-C fires per pair (new wave; parallel)
    fc_results = await fire_fc_per_pair_parallel(
        pairs=substrate_votes.keys(),
        wave_a_results=wave_a_results,
        substrate_votes=substrate_votes,
        registry=THEMATIC_REGISTRY,
        semaphore=Semaphore(10),
    )
    # F-C populates ExportFactionRelationship records (new schema; star-lord Seam 2)

    # Step 5: Wave B fires per kit (existing scaffold extended)
    wave_b_results = await fire_wave_b_per_kit_parallel(
        kits=season_state.kits,
        wave_a_results=wave_a_results,
        registry=THEMATIC_REGISTRY,
        semaphore=Semaphore(10),
    )
    # Wave B populates ExportKit.kit_name_canonical + narrative

    # Step 6: Diversity audit across all three surfaces
    diversity_report = run_diversity_audit(wave_a_results, fc_results, wave_b_results)
    # Triggers regeneration if thresholds exceeded; see § 7

    return Phase5Result(wave_a_results, fc_results, wave_b_results, gb_result, diversity_report)
```

### § 9.2 Token cost projection per season (composing with § 1 table)

| Phase | k=3 calls | k=4 calls | $ cost (k=3) | $ cost (k=4) |
|---|---|---|---|---|
| Wave A | 3 | 4 | ~$0.15 | ~$0.20 |
| F-C | 3 | 6 | ~$0.15 | ~$0.30 |
| Wave B | ~20-40 | ~20-40 | ~$0.30 | ~$0.60 |
| Diversity regen (1 per surface max) | ≤3 | ≤4 | ~$0.05 | ~$0.10 |
| **Per-season total** | — | — | **~$0.65** | **~$1.20** |

Within SC-3 envelope ($0.50-$5). F-C contribution is ~$0.15-$0.30 per season (dispatch acceptance criterion).

### § 9.3 ExportFactionRelationship schema (star-lord Seam 2 deliverable)

For reference (gandalf does not author schema; star-lord Seam 2 implements per ADR-004 MIGRATION.md), the F-C output composes into:

```python
class ExportFactionRelationship(BaseModel):
    """Per-pair inter-faction relationship; Path III addition."""
    season_id: str
    faction_a_cluster_id: int
    faction_b_cluster_id: int

    # F-C LLM-produced fields
    relationship_type: str  # one of: antagonist, rival, allied, neutral, mysterious, parallel
    tension_narrative: str
    shared_history_hook: str | None
    primary_pair_intensifier: str | None
    ai_tell_compliance_score: float

    # G-B + diversity provenance
    primary_pair_flag: bool
    gb_selection_rationale: str | None
    pairwise_distance: float

    # Diversity audit telemetry
    cosine_distance_to_other_pairs: list[float] | None
    diversity_check_max_similarity: float | None
    regeneration_fired: bool | None
    final_compliance_status: str  # ACCEPT | ACCEPT_WARN | FAIL_RECORD
    llm_call_id: int | None
```

Star-lord Seam 2 authors the canonical schema + MIGRATION.md per Dispatch 3B Seam 3 precedent (`bf7f659`).

---

## § 10 Discipline composition + Gate-2 grep audit patterns

### § 10.1 Disciplines composed in this doc

| Discipline | Application |
|---|---|
| #1 (math-before-code) | This doc IS the spec; star-lord Seam 2 implementation follows |
| #11 (empirical inspection) | Diversity audit + cross-cultural neutrality audit are empirical gates at first 3 seasons |
| #18 (math-hotspot routing) | Phase 5 cohesion-judge is a named math hotspot; legolas Mode A methodology consultation already returned (per SC-3) |
| #19 (no polling) | All three wave prompts fire async via existing `asyncio.sleep()` backoff infrastructure |
| #41 (pre-authored taxonomy interrogation) | `relationship_type` 6-enum is substrate-evidence-driven; NOT pre-authored faction taxonomy. Enum values are emergent labels for substrate-vote patterns, not pre-imposed categories |
| #42 (framing-audit at consumption) | gandalf framing-audited this dispatch before authoring (Q1: registry consumption pattern impl-ready; Q2: D7 threshold + cosine-distance empirically gated; Q3: substrate-vote vote-precedes-LLM is the substrate-led pattern) |
| #44 (framing-refusal authority) | If first 3 seasons surface antagonist > 50% OR cross-cultural neutrality leaks, gandalf authors prompt amendment via framing-refusal pattern |
| #45 (generative-architecture vocabulary lock) | LOAD-BEARING throughout; § 3 above documents discipline + carve-outs |
| #46 (DB anti-materialization) | F-C k(k-1)/2 at k∈{3,4} = max 6 calls per season; trivial; bounded |
| D7 (AI-tell line) | § 8 documents the verification logic; combined LLM self-assessment + mechanical grep |

### § 10.2 Gate-2 mechanical grep patterns (jack-ryan)

Run after star-lord Seam 2 implementation lands:

```bash
# Discipline #45 vocabulary check on prompt construction code
cd ~/Games/reincarnated-engine
grep -rn '\bclass\b' src/reincarnated/llm/phase5_orchestrator.py | grep -v "^.*class [A-Z]" | grep -v "^.*# " | grep -v '"class_'
# Expected: zero matches outside Python language keyword usage

# D-Sharpened invariance check (gandalf design obligation)
grep -rn 'substrate_anchored_personage' src/reincarnated/llm/phase5_orchestrator.py
# Expected: zero matches (no reads at prompt-assembly layer)

# AI-tell phrase list present (sanity check on grep validation)
grep -n 'AI_TELL_PHRASES' src/reincarnated/llm/phase5_orchestrator.py
# Expected: AI_TELL_PHRASES_WAVE_A + AI_TELL_PHRASES_FC defined per § 8.2

# relationship_type enum constraint present
grep -n 'antagonist\|rival\|allied\|neutral\|mysterious\|parallel' src/reincarnated/llm/phase5_orchestrator.py
# Expected: 6-enum present in F-C call construction OR validation

# substrate_vote computation present
grep -n 'substrate_vote\|compute_substrate_vote' src/reincarnated/llm/phase5_orchestrator.py
# Expected: substrate_vote computed before F-C LLM call
```

---

## § 11 Acceptance criteria roll-up (per dispatch)

For the dispatch acceptance criteria checklist:

- [X] **Wave A faction-level cohesion-judge LLM prompt template** — § 4 above (SYSTEM § 4.2; USER § 4.3; acceptance § 4.4)
- [X] **Wave B per-kit identity LLM prompt template** — § 5 above (SYSTEM § 5.2; USER § 5.3; acceptance § 5.4)
- [X] **F-C per-pair LLM prompt template** — § 6 above (SYSTEM § 6.3; USER § 6.4; acceptance § 6.5; distribution § 6.6)
- [X] **relationship_type 6-enum specification** — § 6.1 above; gandalf judgment {antagonist, rival, allied, neutral, mysterious, parallel}; substrate-evidence-driven; cross-cultural neutrality binding
- [X] **D7 AI-tell compliance verification logic** — § 8 above (threshold ≥ 0.7; mechanical grep validation alongside LLM self-assessment; max 1 regeneration)
- [X] **Cross-Character Diversity Audit DETECTION integration** — § 7 above (composes with star-lord local sentence-transformers + TF-IDF n-gram (2,4) cosine <0.7 per season acceptance)
- [X] **D-Sharpened invariance verified at all prompts** — § 2 + § 5.5 + § 6.8 above (`substrate_anchored_personage` NOT in any Wave A / Wave B / F-C prompt; Gate-2 grep audit pattern in § 10.2)

Star-lord Seam 2 (separate signal post this landing) consumes this doc as the canonical prompt spec; implements per § 9.1 orchestration sequence.

---

## § 12 Open questions resolved + queued

### § 12.1 Resolved in this doc

**Q-W3-G-1 (gandalf):** relationship_type 6-enum exact values — your judgment per substrate vote + cross-cultural neutrality.

**Resolution (§ 6.1):** `{antagonist, rival, allied, neutral, mysterious, parallel}`. Rationale anchored on Diablo IV / PoE / Mushoku Tensei / Earth Self meta-layer observation; substrate-evidence-driven; cross-cultural neutrality binding; rejects `nemesis` / `progenitor` / `descendant` (pre-authored mythological taxonomy violations of Discipline #41).

### § 12.2 Queued for star-lord Seam 2 + downstream

- **Q-W3-S-1 (star-lord):** F-C call sequencing relative to G-B `primary_pair_flag` — gate F-C on G-B completion OR fire in parallel?
  - **gandalf design recommendation (non-binding; star-lord judgment per dispatch Q-W3-S-1):** GATE F-C on G-B completion. F-C consumes `primary_pair_flag` per pair; parallel firing would require either (a) all F-C calls including intensifier slot tentatively + regenerate non-primary pairs, or (b) two-pass F-C structure. Both add complexity. Gating F-C on G-B completion is clean; G-B is O(k²) at k∈{3,4} (trivial compute; not latency-meaningful); F-C still fires in parallel across pairs.
- **Diversity threshold calibration (post first 3 seasons):** F-D2 acceptance band (cosine < 0.7) may calibrate down based on observed false-positive rate; gandalf + star-lord joint review at wave-close.
- **Cross-cultural neutrality validation (post first 3 seasons):** F-C12 audit confirms no lineage-pair correlates with single relationship_type > 50%; if neutrality leaks, gandalf authors SYSTEM prompt amendment.
- **`ai_tell_compliance_score` calibration (post first 3 seasons):** F-D3 confirms self-assessment not saturated; if all calls return ≥0.95 with no <0.7 fires, mechanical grep takes precedence per § 8.3.

---

## § 13 Sign-off + framing-audit record

### § 13.1 Discipline #42 framing-audit

| Q | Question | Verdict |
|---|---|---|
| Q1 | Load-bearing framing assumptions of this work | (a) registry § 9.1 consumption pattern impl-ready (verified); (b) D7 threshold ≥0.7 empirically achievable (gated at first 3 seasons; F-D3 audit); (c) cosine <0.7 acceptance empirically achievable (gated at F-D2); (d) 6-enum captures substrate-vote space (gandalf judgment + Diablo/PoE/isekai precedent) |
| Q2 | Refutation evidence currently in hand or surfaceable | (a) Wave A scaffold exists at `phase5_orchestrator.py`; consumption pattern matches; (b) cohesion-judge calibration spec at `canonical/story/phase-5-cohesion-judge-calibration-spec-2026-05-25.md` provides the threshold framework; (c) star-lord Seam 3 `bf7f659` provides ExportFactionCluster + cosine-similarity_max field — diversity check infrastructure ready; (d) THEMATIC_REGISTRY § 9 documents consumption pattern post-Wave-3-unblock — registry term-type tags map cleanly to prompt slots in Wave A / Wave B; F-C consumes faction anchors + substrate_vote (no registry-slot mismatch) |
| Q3 | If refutation plausible, refine framing rather than execute | Q3 = NO — framing holds. Refutation evidence supports the framing rather than refuting it. Empirical gates at first 3 seasons (F-D1-F-D4 + F-C12) will catch any framing-failure mode at the cheapest empirical point. Proceed. |

### § 13.2 Discipline #41 substrate-led grep audit

The `relationship_type` 6-enum is substrate-evidence-driven (per § 6.1 + § 6.2 SUBSTRATE_VOTE structure). Each enum value is *triggered* by substrate-vote pattern; LLM does not freely select. This honors Discipline #41 — no pre-authored relationship taxonomy; emergent labels for substrate-distinguishable vote patterns.

Grep audit at Gate-2 (jack-ryan):

```bash
# Confirm relationship_type values are validated against the 6-enum
grep -n 'RELATIONSHIP_TYPE_ENUM\|relationship_type.*in.*\\\[' src/reincarnated/llm/phase5_orchestrator.py
# Expected: enum constraint present in F-C output validation

# Confirm substrate_vote computed before LLM call
grep -n 'compute_substrate_vote\|substrate_vote =' src/reincarnated/llm/phase5_orchestrator.py
# Expected: substrate_vote computation present; F-C LLM input includes substrate_vote
```

### § 13.3 Cycle 14 quality-orientation contribution

Per Cycle 14 quality-orientation ("Engine first. Game second. Phase third." Move 1):

- **Engine first:** prompt templates produce structured JSON output integrated with existing ExportFactionCluster + new ExportFactionRelationship schemas; PM-2 D-Sharpened invariance preserved; substrate-led discipline at the relationship layer
- **Game second:** the `relationship_type` 6-enum + tension_narrative + shared_history_hook + primary_pair_intensifier compose into player-facing faction-relationship surface in drax loadout summary; players see central narrative tension (primary pair) + background relationships at lighter weight; faction identity reads as substrate-grounded, not pre-authored
- **Phase third:** Phase 5 LLM architecture deepens with Wave 3; Phase 7 joint-gate (separate dispatch) consumes Wave 3 outputs for cohesion evaluation

### § 13.4 Authority chain (final)

- Matt-gate Path (1) RATIFIED (PM-1 + PM-2 + D-Sharpened LOCKED)
- Matt pre-ratification #2 LOCKED — F-C tonal direction
- Path III F-C scope addition ratified — Matt verbatim "Let's go with option (III)"
- Cycle 14 quality-orientation Move 1 ("Engine first. Game second. Phase third.")
- gandalf judgment on `relationship_type` 6-enum exact values (Q-W3-G-1 resolved at § 6.1; substrate-evidence-driven; cross-cultural neutrality binding; Discipline #41 honored)

**Signed:** gandalf (story-and-design steward)
**For:** the Wave 3 Seam 1 LLM prompt authoring deliverable per dispatch `2026-05-27-wave-3-phase-5-cohesion-judge-llm-with-f-c.md` § Seam 1. Three LLM call surfaces (Wave A faction-level + Wave B per-kit identity + F-C per-pair inter-faction relationship) specified with SYSTEM prompt + USER prompt + structured output schema + acceptance criteria + composition rules. THEMATIC_REGISTRY consumption per § 9.1 + § 9.2; D-Sharpened invariance preserved; relationship_type 6-enum substrate-evidence-driven; D7 AI-tell verification combined LLM self-assessment + mechanical grep; diversity audit composes with star-lord Seam 3 cosine-distance infrastructure; cross-cultural neutrality binding. Hand-back to KR: routes star-lord Wave 3 Seam 2 (per-pair LLM infra + ExportFactionRelationship schema + diversity smoke) + rocket 1-line `_apply_gb_tiebreak` lexicographic_tiebreak fix after this landing.
