# Dispatch — Elrond Cosmograph Substrate-Trace Extraction

**Date:** 2026-06-06
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-06-06 multi-iteration design call ratifying primitive-vocabulary lock + cosmograph Phase A commission
**To:** elrond (catalogue DB + abstraction-analysis seam)
**Cycle:** cosmograph Phase A (creation-moment manifestation milestone)
**Type:** SUBSTRATE EXTRACTION + PRIMITIVE VOCABULARY ENUMERATION + 2D EMBEDDING
**Cost budget:** $0 LLM (pure curation; no LLM calls per D7 + cost-discipline)
**Time budget:** ~2-3 days elrond time (Phase 0 ~1 day; Phase 1-5 ~1-2 days)
**Critical anchors:**
- `canonical/story/2026-06-06-atomic-substrate-registry.md` (Layer 0 + Layer 0.5 + derivation chains + Naming Layer N1-N4)
- `canonical/story/2026-05-31-hypothesis-flow-pattern-library-architecture.md` (CANONICAL — cell schema § 3 + flag enum § 4 + Phase A-E roadmap § 5)
- `canonical/story/2026-06-05-cosmograph-pivot.md` (§ 9 amendment — primitive-as-star + kit-as-constellation architectural lock)
- `agentic_orchestration/gandalf/notes/2026-06-06-cosmograph-star-granularity-verdict.md` (Pattern A-deep verdict)
- `agentic_orchestration/gandalf/notes/2026-06-06-framing-audit-na-substrate-blind-recognition.md` (NA-substrate-blind recognition)

---

## 0. TL;DR

Elrond extracts the substrate data that feeds the cosmograph at `/forge`. Output is a unified parquet/JSON packet consumable by drax: ~350-400 atomic substrate primitive nodes ("stars") + **~1000 simulated PROVISIONAL constellations (Option B AMENDMENT 2026-06-06)** + 2D embedding coordinates + per-constellation primitive-set mapping + per-primitive BDI-β load-bearing weights.

**Option B AMENDMENT 2026-06-06** (per Matt ratification): cycle 14 wave-5 named-bearer kits were NOT generated against the future-engine substrate vocabulary (race + ~65-100 mechanic primitives + skill-tree-position + investment-scaling + per-skill flavor judgment + canonical 47/51/atomic-substrate-registry additions). Force-mapping them to constellations defined over future-engine primitives would claim substrate membership they don't have, violating substrate-led discipline. Therefore: **cosmograph at /forge is FORWARD-LOOKING — renders the future-engine substrate vocabulary as ALL simulated PROVISIONAL.** Cycle 14 named-bearer corpus (Duskweaver + 36 others) STAYS at /loadout as the empirical-current-state showcase. Phase 1 (per-kit primitive-set extraction from real corpus) RETIRED; Phase 2 sim count EXPANDED to ~1000.

**Four-phase execution (post-Option B amendment):**
- **Phase 0** — Primitive vocabulary enumeration + validation (~1 day)
- **Phase 1** — RETIRED per Option B amendment
- **Phase 2** — Move B simulated constellation generation, ~1000 PROVISIONAL kits (~1 day; expanded from ~0.5)
- **Phase 3** — Per-primitive BDI weighting + 2D embedding (~0.5 day)
- **Phase 4** — Output packet assembly + delivery (~0.25 day)

**Total time UNCHANGED** at ~2-3 days elrond (Phase 1 retirement reallocated to Phase 2 expansion).
**Total cost UNCHANGED** at $0 LLM.

**Substrate-led discipline applied throughout:** no pre-imposed taxonomy on substrate output; primitives flat-enumerated (no family grouping per Matt 2026-06-06 substrate-led correction); clustering emerges from 2D embedding; cycle 14 kits NOT force-mapped against substrate they weren't generated under (Option B amendment).

**Framing-audit checklist applied at Phase 0 start** (per OP § 4.1 + 2026-06-06 recognition). Q1-Q3 audit of load-bearing assumptions BEFORE Phase 1+ execution.

---

## 1. Scope

### 1.1 What elrond produces

A delivery packet at `agentic_orchestration/elrond/research/cosmograph-substrate-trace-2026-06-XX/` containing:

| Artifact | Format | Purpose |
|---|---|---|
| `primitive_registry.parquet` | parquet | The ~350-400 atomic substrate primitives (Lock #1) with per-primitive substrate fingerprint + element-coupling + 2D embedding coordinate + brightness-weight |
| `region_labels.json` | JSON | Sky-neighborhood labels (BC bins, tier labels, scaling-pattern labels, emergent mechanic-family labels read from clustering) per Lock #4 |
| `kit_constellations.parquet` | parquet | **~1000 simulated PROVISIONAL constellations per Option B AMENDMENT** (no real-kit rows; cycle 14 named-bearers stay at /loadout); per-kit primitive-set membership; cell_status PROVISIONAL; bc_cell_id placeholder identifiers; no LLM-named identities (D7 line) |
| `flag_enum_attachments.parquet` | parquet | Per-kit attachment of hypothesis-flow § 4 flag families (17 family enums) |
| `faction_overlays.json` | JSON | ~9 faction-grouping polygon definitions per phase5_faction_clusters |
| `cosmograph_README.md` | markdown | Manifest of all artifacts + drax ingestion contract |

### 1.2 What elrond does NOT produce in this commission

- **No LLM-driven content** (per D7 AI-tell line + cost-discipline). Cosmograph constellations are ALL bc_cell_id placeholders per Option B amendment; no LLM-named identities at /forge.
- **No real-kit constellation rows in this packet** (per Option B amendment). Cycle 14 wave-5 named-bearer corpus (~150 kits with cohesion-judge-approved identities like Duskweaver) stays at /loadout as the empirical-current-state showcase. They were NOT generated against the future-engine substrate vocabulary (race + ~65-100 mechanic primitives + skill-tree-position + canonical 47/51 additions); force-mapping them as constellations would claim substrate they don't have.
- **No mechanic-family pre-grouping.** Per Matt 2026-06-06 substrate-led correction: enumerate mechanics FLAT; clustering emerges from 2D embedding, not from pre-imposed family taxonomy.
- **No q-score generation for simulated constellations.** All sim constellations carry `is_simulated: true` + null q-scores + null gauntlet pass rate. Drax never displays q-scores in the cosmograph.
- **No engine kit regeneration.** Once cycle 15+ generates kits against the future-engine substrate, THOSE become real constellations at /forge progressively. Until then, /forge is forward-looking simulation.

---

## 2. Phase 0 — Primitive vocabulary enumeration + validation

**Duration:** ~1 day elrond
**Output:** `primitive_registry.parquet` v0 + validation report
**Discipline anchors:** framing-audit Q1-Q3 BEFORE execution; substrate-led discipline; Discipline #41 substrate-led-encoding-gate

### 2.1 Framing-audit Q1-Q3 (PRE-EXECUTION)

Per OP § 4.1 + 2026-06-06 NA-substrate-blind recognition, audit the commission scope BEFORE execution:

| Q | Audit question |
|---|---|
| Q1 | What load-bearing framing assumptions does this commission depend on? (atomic-substrate-registry § 1 captures the full atomic substrate; hypothesis-flow § 4 captures the full flag enum; cosmograph DP1-DP5 lock per § 9 amendment) |
| Q2 | What evidence currently in hand could refute these assumptions? (cycle-14 wave-5 corpus is in `reincarnated-loadout/data/cycle14-season-00{1,2,3}-wave-b-identities.json`; weapon-form-token lookup is in `elrond/research/cycle-10-stage-1-2026-05-24/weapon_form_token_lookup.json`; canonical 39 + 40 + 47 + 51 are CANONICAL) |
| Q3 | If refutation evidence exists, is the right move to refine the framing rather than execute as-framed? (substantive frame is stable; per-primitive enumeration is the work) |

Surface any refutation in pre-Phase-1 escalation to gandalf via Pattern-A query within ~30 minutes.

### 2.2 Enumerate Layer 0 atomic primitives per atomic-substrate-registry § 1

Produce a flat list of ~350-400 primitives with the following per-primitive schema:

```
primitive_registry schema:
- primitive_id: str (unique; e.g., "element_fire", "mechanic_movement_teleport", "weapon_form_greatsword", "race_tolkien_hobbit", "T4_RESOURCE_CONVERSION", "geometry_cleave")
- primitive_family: enum (element / sub_element_flavor / attribute / T4_strategy / skill_geometry / mechanic / weapon_form / cultural_tradition / period / register / off_hand / race / racial_trait / investment_scaling / resource_model)
- primitive_label: str (player-facing label, e.g., "Fire", "Teleport", "Greatsword")
- substrate_fingerprint: dict (per-primitive substrate signature — geometry-tag / tempo / range / resource-interaction / effect-category / element-coupling / attribute-coupling)
- bdi_weight: float (BDI β contribution; populated in Phase 3)
- element_coupling: list[str] (which elements this primitive natively couples with, if any)
- attribute_coupling: list[str] (which attributes this primitive natively couples with, if any)
- canonical_source: str (which canonical doc / engine file is the authoritative source)
- embedding_x: float (2D coordinate; populated in Phase 3 via UMAP)
- embedding_y: float (2D coordinate; populated in Phase 3 via UMAP)
- visibility_at_default_zoom: bool (per Lock #1)
- is_simulated: bool (False for real engine substrate; reserved field for future use)
```

### 2.3 Per-family enumeration tasks

| Family | Count target | Source |
|---|---|---|
| **Elements** | 8 | `~/Games/reincarnated-engine/config/elements.yaml` + element_biases.py |
| **Sub-element flavors** | per primary's pool | `canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md` (each primary's flavor pool) |
| **Attributes** | 4 | `canonical/story/attribute-system-2026-05-24.md` |
| **T4 strategies** | 6 (current; flag 21-proposed for future expansion) | `canonical/39-qd-engine-end-to-end-workflow-2026-05-24.md` § 0.5.1 + Algorithm § 8 |
| **Skill geometry palette** | 16 | `canonical/historical/09-geometry-palette-discussion.md` § Decision table + B11 expansion |
| **Investment-scaling patterns** | 6 | `canonical/51-investment-scaling-6-pattern-architecture-2026-05-28.md` |
| **Resource models** | 5 | `cycle13_characters.db` schema + foundation/ |
| **Mechanic primitives** | ~65-100 (FLAT — no family grouping) | engine `foundation/` + `skill-system-2026-05-24.md` + canonical 47 damage-scaling + canonical 51 — see § 2.4 mechanic-enumeration discipline |
| **Weapon-form tokens** | ~200 | `weapon_form_token_lookup.json` — see § 2.5 ratio validation |
| **Cultural-tradition** | 14 | `weapon-substrate-conclusion-declaration.md` + weapon library `cultural_lineage_canonical` enum |
| **Historical-period** | 9 | `historical_period_canonical` enum |
| **Register** | 6 | `register_canonical` enum |
| **Off-hand substrate types** | 7 (estimate) | `canonical/story/off-hand-items-2026-05-24.md` |
| **Race primitives (per-season)** | 4-8 default randomized | SCHEMA only per atomic-substrate-registry § 1.17 — for Phase A, generate a default-randomized race-set within plausible primitive bounds |
| **Racial trait primitives (per-season)** | 8-20 per race-set | SCHEMA only per atomic-substrate-registry § 1.18 |

### 2.4 Mechanic-enumeration discipline (NEW per Matt 2026-06-06 substrate-led correction)

**Critical:** enumerate mechanics FLAT — one row per individual mechanic. Do NOT group into families pre-imposition. Per Matt 2026-06-06: "I don't think we can group at all" — the individual mechanic IS the right substrate level.

For each mechanic, populate:
- `substrate_fingerprint.geometry_tag` (does this mechanic alter geometry?)
- `substrate_fingerprint.tempo` (does this mechanic alter tempo?)
- `substrate_fingerprint.range` (does this mechanic alter range?)
- `substrate_fingerprint.resource_interaction` (does this mechanic interact with resource economy?)
- `substrate_fingerprint.effect_category` (control / damage / sustain / debuff / mobility per BDI § 4.1)

The 2D embedding (Phase 3) will produce emergent clustering by family WITHOUT us pre-imposing the family taxonomy. Region labels (Phase 0 output) provide ambient navigation; clustering provides the structure.

**Coverage target (per Matt's recall of ~65-100 mechanics):**
- Movement mechanics: teleport / blink / dash / leap / leap-strike / charge / flicker / vault / slide / step / etc. — ENUMERATE
- Combat-modifier mechanics: pierce / chain / multi-strike / extra-projectile / explosion / DoT-attach / split / etc. — ENUMERATE
- Defensive mechanics: block / parry / dodge / reflect / mitigate / shield / stagger-immune / etc. — ENUMERATE
- Sustain mechanics: lifesteal / leech / heal-on-X / regen / drain-recovery / etc. — ENUMERATE
- Crit mechanics: crit-chance / crit-mult / on-crit-trigger / vulnerability-crit / etc. — ENUMERATE
- Spawn/proxy mechanics: summon / clone / decoy / totem / minion / proxy-strike / etc. — ENUMERATE
- Effect-modifier mechanics: knockback / stagger / stun / freeze / silence / pull / push / etc. — ENUMERATE
- Resource-flow mechanics: regen / generation / burn / drain / steal / overflow / threshold-fire / etc. — ENUMERATE
- Trigger mechanics: on-hit / on-kill / on-X-condition / on-cooldown / on-event / etc. — ENUMERATE

These are GUIDES for coverage, NOT the schema. Each mechanic gets its own row.

### 2.5 Weapon-form token enumeration with magic/physical ratio — AMENDED per 2026-06-06 Pattern-A verdict

**AMENDED 2026-06-06 per Pattern-A verdict at `agentic_orchestration/gandalf/notes/2026-06-06-pattern-a-verdict-cosmograph-weapon-form-ratio.md`:** the prior "50/50 working target" was authored at the WRONG SURFACE. The canonical-locked ~54/46 ratio recalled by Matt lives at the KIT-ROSTER element-axis-coverage layer (40-45% physical / 55-60% caster per Discipline #58 + Matt 2026-06-02 verbatim QDX-5 ratification), NOT at the weapon-form-token layer. See verdict § 2 for the three-surface disambiguation.

**Phase A target at weapon-form-token surface:** render the EMPIRICAL substrate ratio honestly per Discipline #41 + #59. NO ratio target imposed; substrate is the truth.

**Phase 0 deliverable:**
1. Enumerate all weapon-form tokens from `weapon_form_token_lookup.json` (~200)
2. Tag each token as `physical` / `magical` / `hybrid` per `(range, geometry, tempo, attribute)` tuple + `gear-substrate-rule-table-v1-2026-05-22.md` § 2 15-gear catalogue physical-vs-caster lean
3. Compute actual physical/magical ratio from substrate enumeration (empirical Phase-0 measurement returned ~89/11 at token level + ~92/8 at row level — this IS the substrate-honest answer at this surface)
4. Render the actual ratio honestly in Phase A cosmograph
5. Document in `cosmograph_README.md` § `substrate_coverage_honesty`: "Weapon-form-token region renders ~89% physical / ~11% magical at token level. Reflects substrate composition under cycle-10 source mix; magical-implement diversity is the elrond substrate-enrichment workstream target per Discipline #59."
6. Queue substrate-enrichment workstream pointer: magical-implement diversity (wand / orb / focus / staff / tome / censer / grimoire) — target v2 substrate-snapshot ramp toward 70/30 phys/mag at token level

**Operational discipline:**
- Honor what the substrate says (substrate-led discipline; Discipline #41 + #59)
- DO NOT manufacture missing magical tokens to balance — would violate substrate-led discipline by ~8× over-sampling
- Render the asymmetry visibly in cosmograph encoding (color-channel or brightness gradient so phys/mag composition is legible, not hidden)
- Kit-roster element-axis-coverage distribution (the 40-45/55-60 layer) is handled at § 4.1 step 2 (Phase 2 sim-kit generation), NOT at weapon-form-token enumeration

### 2.6 Region labels (Lock #4 — sky-neighborhood structure)

Generate `region_labels.json` with the following label families (NOT first-class stars; ambient navigation overlays):

| Region label family | Count | Source |
|---|---|---|
| BC bin labels | 34 | qd-engine-bc-axes-lock-2026-05-20 § 2 |
| Skill-tree tier labels (T1 rotation / T2 β-pair / T3 build-defining / T4 capstone) | 4 | canonical 47 damage-scaling-architecture |
| Scaling-pattern-per-tier labels | 4 | canonical 47 + atomic-substrate-registry § 1.7 |
| Emergent mechanic-family labels | ~9 | READ FROM CLUSTERING (post-Phase-3 embedding); do NOT pre-impose |
| Chain architecture labels (3-chain / 4-chain) | 2 | canonical 40 D83 |

### 2.7 Phase 0 acceptance criteria

- `primitive_registry.parquet` v0 produced with all 14+ primitive families enumerated
- Total atomic primitive count: ~350-400 (within ±20% acceptable range)
- Per-primitive substrate fingerprint populated for ≥95% of primitives
- Weapon-form token physical/magical ratio computed + validated against canonical lock
- `region_labels.json` v0 produced (excluding emergent mechanic-family labels which await Phase 3 clustering)
- Framing-audit Q1-Q3 captured in commission notes
- Pattern-A query escalation to gandalf if substrate-thin or ratio-mismatch surfaces

---

## 3. Phase 1 — RETIRED per Option B amendment (2026-06-06)

**Status:** RETIRED
**Reason:** cycle 14 wave-5 named-bearer kits were NOT generated against the future-engine substrate vocabulary (race + ~65-100 mechanic primitives + skill-tree-position + canonical 47 scaling-pattern-per-tier + canonical 51 investment-scaling + per-skill flavor judgment + atomic-substrate-registry § 1 additions). Force-mapping them as constellations defined over future-engine primitives would CLAIM substrate membership they don't have, violating substrate-led discipline.
**Disposition:** cycle 14 named-bearer corpus stays at `/loadout` as empirical-current-state showcase (Duskweaver + 36 others remain showcased there per cycle-18 wave-close). Cosmograph at `/forge` is FORWARD-LOOKING — renders the future-engine substrate vocabulary as ALL simulated PROVISIONAL until cycle 15+ regenerates kits against the new substrate. Phase 1 time-budget reallocates to Phase 2 sim-count expansion.

**Phase 1 work IS NOT lost** — once cycle 15+ regenerates kits against the future-engine substrate, those kits become real constellations at /forge progressively. The primitive-set extraction methodology lives in this dispatch and is reusable in that future workstream.

---

## 4. Phase 2 — Move B simulated constellation generation (EXPANDED per Option B amendment)

**Duration:** ~1 day elrond (expanded from ~0.5 day per Option B amendment)
**Output:** `kit_constellations.parquet` with ~1000 simulated PROVISIONAL rows (EXPANDED from ~850 per Option B amendment)
**Discipline anchors:** substrate-led (BDI-weighted plausibility); D7 (no LLM-named identities); explicit demarcation
**Per Option B amendment 2026-06-06:** ALL constellations at /forge are simulated PROVISIONAL. No real-kit reference rows. Cycle 14 corpus stays at /loadout.

### 4.1 Generation algorithm

For each of ~1000 simulated constellations:

1. **Sample random subset of primitives** weighted by BDI ω+τ correlation per `canonical/story/bdi-omega-tau-tables-v1-2026-05-22.md` — primitives that co-occur in genre-canonical kits should co-occur in simulated kits at higher rates (plausibility, not noise)
2. **Apply substrate-led plausibility filters:**
   - **Element distribution constraint (NEW per 2026-06-06 Pattern-A verdict):** kit element selection across the ~1000 sim kits is weighted to honor Discipline #58 genre-aligned distribution: physical-primary kits = 40-45% of total; caster-primary kits = 55-60% of total. Within caster primaries, distribute approximately evenly across 7 canonical elements (~7-9% each). This is the kit-roster element-axis-coverage surface where the canonical-locked ratio lives — see Pattern-A verdict § 2.2.
   - Each kit selects 1-2 elements (per atomic-substrate-registry § 2.1 single vs hybrid)
   - Each kit selects 1 attribute (per element-attribute coupling — element_biases.py:28)
   - Each kit selects 1-3 T4 strategies
   - Each kit's skill geometries are 3-5 across 5-8 skills
   - Each kit's mechanic-primitive count is 8-15 (per typical kit composition complexity)
   - Each kit's weapon-form tokens are 1-3 (per main + optional off-hand)
   - Each kit's cultural-tradition is 1-3 dominant
3. **Generate placeholder identifier:**
   - `kit_id`: `kit_bc_cell_<NNNN>_simulated` (NNNN = sequential index)
   - `kit_name`: SAME as `kit_id` (no LLM-derived human-readable name per D7)
   - `kit_identity_narrative`: literal placeholder string: `"PROVISIONAL — engine has not yet composed this pattern."`
4. **Populate sim-specific fields:**
   - `cell_status`: PROVISIONAL
   - `is_simulated`: True
   - `q_scores`: null
   - `gauntlet_pass_rate`: null
   - `pareto_rank`: null
   - `archive_status`: null

### 4.2 Plausibility QA

After generation, run substrate-coherence check:
- Each kit's element-attribute coupling honors element_biases.py:28
- Each kit's T4-element compatibility honors canonical 47 § 11 + canonical 39
- Each kit's weapon-form tokens are compatible with kit's attribute (per weapon_form_token_lookup attribute-tuple)
- No kit has incoherent primitive combinations (e.g., not all 16 geometries; not all 6 T4 strategies)

If >5% of generated kits fail plausibility QA, regenerate the failing subset with tighter sampling.

### 4.3 Phase 2 acceptance criteria

- ~1000 simulated-kit rows produced (EXPANDED per Option B amendment)
- Plausibility QA pass rate ≥95%
- All sim kits flagged `is_simulated: true` + cell_status PROVISIONAL + null identity fields + bc_cell_id placeholder identifiers
- No LLM cost (pure deterministic generation)
- No real-kit reference rows in `kit_constellations.parquet` per Option B amendment

---

## 5. Phase 3 — Per-primitive BDI weighting + 2D embedding

**Duration:** ~0.5 day elrond
**Output:** `primitive_registry.parquet` (final with embedding_x/y + bdi_weight) + `kit_constellations.parquet` (centroid_x/y populated) + `region_labels.json` (mechanic-family labels populated from clustering)
**Discipline anchors:** Discipline #18 math-hotspot methodology consultation (UMAP is a math hotspot — confirm methodology choice with gandalf BEFORE running if any concern surfaces)

### 5.1 BDI-β weight assignment

For each primitive, compute `bdi_weight ∈ [0, 1]` per BDI ω+τ tables:
- Primitives that participate in high-β pairings (per `bdi-omega-tau-tables-v1-2026-05-22.md` § 1) carry higher weights
- Pareto-frontier-defining primitives (T4 capstones; transformative-scaling mechanics; build-defining-tier mechanics) carry highest weights
- Common-substrate primitives (basic attack modifiers; rotation-tier mechanics) carry lower weights

The brightness gradient in the cosmograph is `star_brightness = bdi_weight × normalized_visual_scale`.

### 5.2 2D embedding via UMAP

Compute the 2D embedding over the unified primitive vector:

```
Input: per-primitive substrate fingerprint vector (geometry-tag / tempo / range / resource-interaction / effect-category / element-coupling / attribute-coupling)
Algorithm: UMAP (recommended; t-SNE fallback if performance concerns)
Output: embedding_x, embedding_y per primitive
```

**Discipline:** UMAP is a math hotspot per Discipline #18. If methodology question arises (e.g., parameter choice, distance metric, scaling), escalate to gandalf via Pattern-A query BEFORE execution. Default parameters: n_neighbors=15, min_dist=0.1, n_components=2.

**Expected emergent clustering:**
- Element-related primitives cluster (8 element neighborhoods)
- Mechanic primitives cluster BY FAMILY (movement mechanics cluster together because their substrate fingerprints correlate; defensive mechanics cluster; etc.) — THIS IS THE EMERGENT FAMILY STRUCTURE per Matt 2026-06-06 substrate-led correction
- Weapon-form tokens cluster by form-class (cleave-weapons cluster; pierce-weapons cluster; bow-class cluster; caster-class cluster)
- T4 strategies cluster as capstone-keystones (extra-bright)

### 5.3 Read emergent mechanic-family labels from clustering

POST-clustering, identify mechanic-family neighborhoods:
1. Run k-means or DBSCAN clustering on mechanic primitives' (embedding_x, embedding_y) coordinates
2. For each cluster, derive a label from the dominant `substrate_fingerprint.effect_category` of the cluster's primitives
3. Add cluster labels to `region_labels.json` mechanic-family-labels section
4. Apply substrate-led labeling: do NOT impose family names from the pre-clustering taxonomy — read what the substrate says and label accordingly

### 5.4 Per-kit centroid computation

For each kit constellation (real + sim):
- Compute centroid_x = mean(embedding_x for primitive in primitive_set)
- Compute centroid_y = mean(embedding_y for primitive in primitive_set)
- Optionally weight by bdi_weight (load-bearing primitives have more centroid pull)

### 5.5 Phase 3 acceptance criteria

- All primitives have embedding_x + embedding_y populated
- All primitives have bdi_weight populated
- All kit constellations have centroid_x + centroid_y populated
- `region_labels.json` has mechanic-family labels read from emergent clustering (5-12 labels expected)
- Methodology consultation captured if Discipline #18 escalation fired

---

## 6. Phase 4 — Output packet assembly + delivery

**Duration:** ~0.25 day elrond
**Output:** Complete delivery packet + drax ingestion contract documentation

### 6.1 Packet contents

| File | Final size estimate |
|---|---|
| `primitive_registry.parquet` | ~50-100 KB |
| `region_labels.json` | ~10-20 KB |
| `kit_constellations.parquet` | ~200-500 KB |
| `flag_enum_attachments.parquet` | ~100-200 KB |
| `faction_overlays.json` | ~10-20 KB |
| `cosmograph_README.md` | ~5-10 KB |

### 6.2 Drax ingestion contract

The README documents:
- Schema of each parquet
- How drax reads primitive_registry to render Layer 0 stars
- How drax reads region_labels to render Lock #4 sky-neighborhoods
- How drax reads kit_constellations to render constellation lines + status visual encoding
- How drax reads flag_enum_attachments to render side-panel flag visualization
- How drax reads faction_overlays to render constellation-grouping halos
- The lasso-resolution algorithm input contract (which fields drax needs from each kit constellation)

### 6.3 Phase 4 acceptance criteria

- All packet files delivered to `agentic_orchestration/elrond/research/cosmograph-substrate-trace-2026-06-XX/`
- README documents the full drax ingestion contract
- Commission marked CLOSED in dispatch tracking
- Phase 0 framing-audit + any Pattern-A queries captured in commission notes

---

## 7. Discipline anchors (per project-wide engineering disciplines)

| Discipline | Application |
|---|---|
| #18 — Math-hotspot methodology consultation | UMAP embedding is a math hotspot; consultation with gandalf if methodology questions arise |
| #41 — Substrate-led | Honor what substrate says; no pre-imposed taxonomy on mechanic-family grouping; clustering emerges from data |
| #42 — Framing-audit | Q1-Q3 applied at Phase 0 start; same-author state-import audit per 2026-06-06 recognition |
| #46 — DB anti-materialization | Per-cell bounding on kit-archive joins; no O(n²) anti-patterns in Phase 1 join work |
| #59 — Substrate coverage honesty | Surface substrate-thin areas + ratio mismatches; do NOT manufacture data to balance |
| D7 (AI-tell line) | No LLM-named identities on simulated kits; placeholder identifiers only |

---

## 8. Pre-commission Pattern-A query opportunity

Elrond is authorized to fire a single Pattern-A query to gandalf BEFORE Phase 1 execution if Phase 0 surfaces:
- Substrate-coverage gap that materially affects primitive enumeration
- Weapon-form magic/physical ratio mismatch against canonical lock
- Mechanic enumeration count outside ~65-100 range
- Any other load-bearing question that materially affects downstream phases

Pattern-A query format: cheapest empirical refutation; ~30-min surface time to gandalf.

---

## 9. Commission close protocol

When Phase 4 acceptance criteria met:
1. Author wave-close record at `agentic_orchestration/elrond/research/cosmograph-substrate-trace-2026-06-XX/wave-close-record.md`
2. Notify gandalf via dispatch-response
3. Drax commission spec authoring fires next (gandalf authors with this packet's contracts as inputs)
4. No push to remote required from elrond commission (gandalf + drax handle push-pattern coordination)

---

## 10. Sign-off

**Authored:** gandalf 2026-06-06 per Matt verbatim ratification of primitive-vocabulary lock + cosmograph Phase A commission
**Authority:** Matt 2026-06-06 multi-iteration design call this session
**Anchor evidence:** atomic-substrate-registry doc + hypothesis-flow CANONICAL doc + cosmograph-pivot § 9 amendment + Pattern A-deep verdict + 2026-06-06 substrate-led correction (no family pre-imposition; individual mechanic IS the star)
**Empirical-evidence trigger for downstream commissions:** elrond Phase 4 delivery operational; drax commission authoring fires

**End of commission spec.**
