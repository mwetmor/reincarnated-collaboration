# THEMATIC REGISTRY — substrate-led term-pool for Phase 5 LLM consumption

**STATUS:** CURRENT (Stages 1-2 of 4 — header + reconciliations + schema + element-only registry; Stages 3-4 pending)
**Date:** 2026-05-27
**Author:** gandalf
**Status:** authoring — incremental write per stall-recovery protocol; sections 1-5 land in this commit
**Authority:** Matt-gate Path (1) RATIFIED 2026-05-27 (THEMATIC_REGISTRY gates Wave 3 Phase 5 LLM impl); knight-rider routing under hive-mind crash-recovery § 2.4

**Companion docs:**

- `~/Games/reincarnated-engine/src/reincarnated/generation/math/phase-5-pm-2-faction-label-assignment-math-2026-05-27.md` § 12 (consumption surface — Wave A faction-level)
- `~/Games/reincarnated-engine/src/reincarnated/generation/math/wave-1-5-option-alpha-kit-naming-policy-math-2026-05-27.md` § 5.2 (consumption surface — Wave B per-kit identity)
- `canonical/00-ground-state.md` § 1 registration: pending Stage 4 sign-off
- `canonical/story/marginal-lineage-tagging-pattern-2026-05-23.md` (substrate contamination disposition baseline)
- `agentic_orchestration/dispatches/2026-05-27-gandalf-thematic-registry-continuation-incremental.md` (stage protocol)
- `agentic_orchestration/dispatches/2026-05-27-gandalf-thematic-registry-authoring.md` (original dispatch + acceptance criteria)

**Authority chain:**

Matt-gate (2026-05-27 ratification) → gandalf authorship → knight-rider sequencing → jack-ryan Gate-1/Gate-2 review at sign-off → star-lord Phase 5 LLM-prompt consumption at Wave A + Wave B fire-time.

---

## § 1 Purpose and scope

The THEMATIC REGISTRY is the **substrate-led term-pool** that Phase 5 LLM prompts (PM-2 faction-label assignment; Wave 1.5 Option Alpha per-kit naming) draw vocabulary from. It exists to enforce two anti-patterns simultaneously:

1. **NO pre-authored faction taxonomy.** The registry does NOT prescribe "the Order of X," "the Ashen Cult," or any pre-named factions. Factions emerge from clustering at Wave A; the registry provides only the *vocabulary palette* the labeller draws from.
2. **NO class-vocabulary leak into faction/kit naming.** Words like "warrior," "mage," "rogue," "tank," "support" do not appear in this registry. Class identity is an engine-internal concept; faction identity is a thematic-cohesion concept; the two surfaces are kept lexically isolated.

The registry is consumed at Phase 5 fire-time by:

- **Wave A (PM-2 § 12):** faction-label assignment over the BC-axis cluster ground; LLM picks a faction epithet + motif + lore-fragment per cluster from the registry, conditioned on cluster centroid + dominant weapon_type_family + dominant cultural_lineage.
- **Wave B (Note 4 § 5.2):** per-kit identity naming within a faction; LLM picks archetype-name + place-name + secondary motif from the registry, conditioned on kit substrate-vector + assigned faction.

**Out of scope for this registry:** narrative prescription (no faction backstory beyond lore-fragment seeds), theological systematization (faith/holy cell provides motif tokens NOT doctrine), kit-specific class identity (handled engine-internal at the role/orientation layer per `canonical/historical/role_orientation_taxonomy`).

## § 2 Ground rules

The registry obeys six discipline rules. Violations are caught by jack-ryan Gate-2 + grep audit at Stage 4 sign-off.

1. **Substrate-led (Discipline #41).** Every entry traces to substrate evidence — either telemetry.db `weapon_knowledge_entries` v1_scope=1 rows (cultural_lineage + element columns), legolas crawl outputs, or existing canonical/story/ thematic-vocabulary precedent. No pre-imposed terms that lack substrate anchor.
2. **Term-pool NOT prescriptive taxonomy.** Entries are vocabulary atoms (epithets, motifs, names) the LLM samples from. The registry does not say "fire+european means X faction"; it says "the dense fire×european cell has these epithet tokens available."
3. **Sketch tier 20-50 entries per dense cell** (Stages 2-3). Below 20 = SPARSE label; below 5 = EMPTY label. Density imbalance reflects substrate reality (Discipline #41 not violated by under-dense cells — substrate is the determinant).
4. **No class-vocabulary leak.** Hard ban list: warrior, mage, rogue, hunter, paladin, summoner, monk, druid, necromancer, sorcerer, witch, knight, soldier, ranger, archer, assassin, berserker, gladiator, fighter, controller, tank, support, healer, damage, dps. Plus role-orientation tokens (damage / support / control / hybrid).
5. **Marginal-lineage contamination is a watch-item (NOT a blocker).** 4 of 5 marginal lineages (arctic_circumpolar / oceanic / n.am.indigenous / s.am.indigenous; mesoamerican exempted per disposition docs 2026-05-23) carry substrate contamination per Mode A/B/C/D pattern. Entries derived from these cells are flagged in-cell at Stage 2-3 authoring; elrond substrate re-curation candidate is logged at Stage 4 but is NOT a Stage-1 gate. (Q-TR-Cont-2 disposition: registry-level watch-item; do not escalate to Discipline #41 violation at this stage because substrate-anchored entries are still substrate-anchored even when sourced from contaminated cells — the contamination is about *cell density misattribution*, not about the *terms themselves being non-substrate*.)
6. **Lexical isolation from engine internals.** The registry is the player-facing thematic surface vocabulary. Engine-internal identifiers (cluster_id, kit_signature, BC-axis bin labels, role_orientation tags) do NOT appear here.

## § 3 Element reconciliation

The engine canonical element axis has **8 elements** (per `canonical/historical/geometry_palette_discussion` lineage; ratified through substrate Mode A/B/C/D crawl):

| Element | Canonical | Caster-route note |
|---|---|---|
| arcane | yes | routes to weapon_type_family = caster-arcane (staves, orbs, foci, sigils) |
| faith-holy | yes | routes to weapon_type_family = caster-faith (relics, censers, sacred-text-instruments, prayer-foci) |
| fire | yes | element-class agnostic (any weapon_type_family) |
| water | yes | element-class agnostic |
| earth | yes | element-class agnostic |
| wind | yes | element-class agnostic |
| shadow | yes | element-class agnostic |
| lightning | yes | element-class agnostic |

**Routing note for LLM prompt construction:** when a cluster centroid lands in arcane or faith-holy AND weapon_type_family is caster-arcane or caster-faith respectively, the registry cell access is the *intersection* (arcane × caster-arcane × cultural_lineage; faith × caster-faith × cultural_lineage) — these are the densest cells in their respective columns by substrate count. Other element × weapon_type_family combinations are non-routed (any combination valid).

**Why 8 not more:** the registry does not subdivide elements further (no "frost" sub-element under water; no "ash" sub-element under fire). Element granularity is locked at the engine-canonical 8; sub-thematic variation is captured via *motif tokens within a cell* (e.g., fire cell contains both "ember-glow" and "ash-fall" motifs without making them separate elements).

**Cell coordinate convention:** registry cells are indexed as `(element, weapon_type_family, cultural_lineage)`. Total possible cells = 8 × 6 × 15 = 720. Realistic dense cells per substrate: ~12-15 (per prior fire's planning; confirmed at Stage 3 authoring).

## § 4 Cultural_lineage reconciliation

The substrate `weapon_knowledge_entries.cultural_lineage` column carries **13 lineage tags + 2 meta-tags** (per gandalf prior fire's enumeration; cross-checked against marginal-lineage disposition docs 2026-05-23):

| Lineage tag | Substrate density (qualitative) | Contamination watch-item |
|---|---|---|
| european | dense | no |
| east_asian | dense | no |
| south_asian | moderate-dense | no |
| southeast_asian | moderate | no |
| middle_eastern | dense | no |
| african | moderate | no |
| n.am.indigenous | SPARSE | YES (Mode A/B/C/D contamination — `n-am-indigenous-no-cluster-disposition-2026-05-23.md`) |
| mesoamerican | moderate | no (exempted per `mesoamerican-marginal-lineage-disposition-2026-05-23.md`) |
| s.am.indigenous | SPARSE | YES (per `south-american-indigenous-marginal-lineage-disposition-2026-05-23.md`) |
| arctic_circumpolar | SPARSE | YES (per `arctic-circumpolar-marginal-lineage-disposition-2026-05-23.md`) |
| oceanic | SPARSE | YES (per `oceanic-marginal-lineage-disposition-2026-05-23.md`) |
| fantasy_generic | dense | no (generic-pool not contaminated; intentionally synthetic) |
| sci_fi_generic | moderate | no |
| **cross_cultural** (meta-tag) | applied at LLM-prompt-time when cluster spans 3+ lineages | n/a |
| **unknown** (meta-tag) | applied at LLM-prompt-time when cluster has insufficient lineage signal | n/a |

**Marginal-lineage contamination caveat (Q-TR-Cont-2 disposition):**

The 4-of-5 marginal-lineage contamination pattern (per Mode A/B/C/D substrate analysis) means substrate entries tagged with `n.am.indigenous`, `s.am.indigenous`, `arctic_circumpolar`, and `oceanic` have elevated misattribution risk — some entries may reflect generic-fantasy or european substrate that picked up the marginal tag through crawl noise. This is **logged as a registry-level watch-item** for Stage 2-3 authoring (cells in these columns are flagged in-cell with `[contamination-watch]` marker) and as an **elrond substrate re-curation candidate** for post-Wave-3 work. It is NOT a Stage 1 gate because the registry's job is to provide vocabulary the LLM can draw from; contaminated cells still surface valid substrate-anchored vocabulary, they just under-represent the named lineage's actual signal. Phase 5 LLM-prompt consumption can apply additional `[contamination-watch]` weighting at fire-time if Wave A/B output shows lineage-misattribution patterns.

**Why 13 not more:** lineage granularity is locked at the substrate-column resolution. Sub-regional variation (e.g., "celtic" within european; "tibetan" within east_asian) is captured via *place-name tokens within a cell* — not as separate lineage axes.

## § 5 Per-cell schema (term-type tags)

Each registry cell is a bag of vocabulary atoms. Every atom carries a **term-type tag** from the 5-tag schema:

| Term-type tag | Purpose | LLM consumption pattern | Example shape (not substantive — Stages 2-3 fill cells) |
|---|---|---|---|
| `epithet` | faction or kit honorific / descriptor (Wave A primary; Wave B secondary) | drawn at faction-label assignment as the *modifier* (e.g., "{epithet} of the {motif}") | "ashen-handed" / "sea-bound" / "iron-hearted" |
| `motif` | central thematic image / symbol (Wave A primary; Wave B reinforcement) | drawn at faction-label as the *substantive* paired with epithet | "the broken oath" / "the long winter" / "the watchful sun" |
| `archetype-name` | character archetype the kit identity evokes (Wave B primary) | drawn at per-kit naming as the *identity anchor* — explicitly NOT a class name | "the wanderer" / "the keeper" / "the witness" |
| `place-name` | location / region / landmark token (Wave B reinforcement) | drawn at per-kit naming when faction-place-binding is signaled by cluster | "the bonefields" / "the salt-roads" / "the cinder-passes" |
| `lore-fragment` | seed phrase the LLM can paraphrase into 1-2 sentence faction backstory (Wave A only) | drawn at faction-label as the *backstory seed* — phrase NOT full sentence | "exiled when the third star fell" / "the river chose them" |

**Term-type discipline rules:**

- Each cell SHOULD contain entries across multiple term-types (mixed-bag, not single-type cells). Target distribution per dense cell: ~10 epithet + ~10 motif + ~5 archetype-name + ~3 place-name + ~3 lore-fragment (~31 entries; within 20-50 sketch tier).
- `archetype-name` entries MUST NOT collide with the class-vocabulary ban list (Ground Rule #4). The archetype is *narrative role*, not *combat role*.
- `lore-fragment` entries are intentionally elliptical — they are seeds for LLM elaboration, not finished prose. The LLM paraphrases into context-fitting backstory at fire-time.
- `place-name` entries are *evocative*, not *geographic*. They do not need to map to a fictional world-map (which Reincarnated does not maintain at Phase 0); they are tone-anchors.
- `motif` and `epithet` are the LLM's *combinatorial pair*: faction names assemble as `{epithet} {meta-noun} of the {motif}` or `the {motif} {meta-noun}` where `{meta-noun}` is supplied by the LLM (NOT from the registry) from a small allowed set (`order`, `circle`, `host`, `path`, `vigil`, `keepers`, `chosen`, `legion`, `covenant`).

**Why this schema and not freeform tokens:** the LLM benefits from term-type tagging because it constrains the prompt assembly. Without tags, the LLM must guess which token is a faction epithet vs a kit archetype-name; with tags, the prompt can directly slot tokens into the assembly template per Wave A § 12 / Wave B § 5.2 consumption surfaces.

## § 6 Element-only registry (lineage-agnostic)

This section provides the **lineage-agnostic** vocabulary pool per element. Entries here are the universal-fallback layer: when Phase 5 LLM consumption hits a cluster whose lineage signal is weak (cluster receives the `unknown` or `cross_cultural` meta-tag per § 4) OR when the per-cell sketch (Stage 3 § 7) for the (element, lineage) intersection is labeled SPARSE / EMPTY, the LLM draws from the element-only pool below.

**Per-element distribution target:** ~25 entries per element = ~10 epithet + ~10 motif + ~5 archetype-name. Place-name and lore-fragment entries are deferred to Stage 3 per-cell sketches because those term-types carry lineage-binding by their nature (a place-name without lineage anchoring would either default-european or land generic-fantasy-bland). This is intentional — the element-only registry is the *adjectival/emblematic* layer; the *toponymic/narrative* layer is per-cell.

**Substrate-anchoring trace:** entries below derive from (a) `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` element-axis definitions (8-canonical lock), (b) telemetry.db `weapon_knowledge_entries` v1_scope=1 row distributions across the `element` column observed during the substrate enumeration Mode A/B/C/D crawl, (c) existing canonical/story/ thematic-vocabulary precedent (cross-checked against the no-class-vocabulary-leak ban list at Ground Rule #4), and (d) gandalf lineage-spanning genre knowledge applied at the *adjectival* level (which is element-coherent across lineages — e.g., "ember-throated" reads fire-anchored in european, east_asian, middle_eastern, and fantasy_generic registers alike).

**Discipline #41 compliance:** no class-vocabulary token (warrior / mage / rogue / hunter / paladin / etc. per Ground Rule #4 ban list) and no role-orientation token (damage / support / control / hybrid) appears in any entry below. Grep audit will be re-run at Stage 4 sign-off.

**Term-type tag convention:** entries are listed inside a single per-term-type bucket per element; each entry is a quoted token. Wave A / Wave B LLM consumption draws by term-type slot per the per-cell schema (§ 5).

### § 6.1 Element: fire

**epithet (10):**
- "ember-throated"
- "smoke-veiled"
- "cinder-marked"
- "kiln-tempered"
- "ash-fall"
- "sun-scorched"
- "forge-bound"
- "blaze-wakened"
- "wick-bearing"
- "ember-handed"

**motif (10):**
- "the last hearth"
- "the long burning"
- "the kiln that does not cool"
- "the ash road"
- "the smoke that remembers"
- "the wick before the dark"
- "the unbroken brand"
- "the fire returned"
- "the watching forge"
- "the cinder before dawn"

**archetype-name (5):**
- "the kindler"
- "the smith-without-a-forge"
- "the lamp-bearer"
- "the cinder-walker"
- "the ember-keeper"

### § 6.2 Element: water

**epithet (10):**
- "salt-bound"
- "tide-marked"
- "river-named"
- "rain-wakened"
- "deep-listening"
- "wave-handed"
- "spring-touched"
- "current-borne"
- "spray-veiled"
- "estuary-born"

**motif (10):**
- "the river that chose them"
- "the long tide"
- "the unread depth"
- "the salt road"
- "the well that does not empty"
- "the rain after the dry years"
- "the watching shore"
- "the current beneath the keel"
- "the spring at the end of the path"
- "the wave that returns"

**archetype-name (5):**
- "the wader"
- "the salt-witness"
- "the river-keeper"
- "the tide-listener"
- "the well-warden"

### § 6.3 Element: earth

**epithet (10):**
- "stone-named"
- "root-bound"
- "iron-hearted"
- "deep-foundationed"
- "furrow-handed"
- "mountain-spoken"
- "clay-marked"
- "loam-wakened"
- "pillar-true"
- "thorn-girded"

**motif (10):**
- "the unmoved stone"
- "the root that holds"
- "the long furrow"
- "the mountain that remembers"
- "the cairn at the crossing"
- "the iron in the seam"
- "the unbroken wall"
- "the deep foundation"
- "the patient stone"
- "the soil that took the seed"

**archetype-name (5):**
- "the stone-warden"
- "the root-keeper"
- "the cairn-tender"
- "the foundation-listener"
- "the mountain-witness"

### § 6.4 Element: wind

**epithet (10):**
- "cloud-broken"
- "storm-named"
- "gale-marked"
- "breath-wakened"
- "drift-borne"
- "high-pathed"
- "kite-handed"
- "weather-true"
- "sky-veiled"
- "thin-aired"

**motif (10):**
- "the long crossing"
- "the open road"
- "the storm that called them"
- "the watching sky"
- "the wind before the rain"
- "the unbroken vault"
- "the path the birds know"
- "the breath of the high places"
- "the cloud that turned"
- "the gale at the crest"

**archetype-name (5):**
- "the messenger"
- "the kite-runner"
- "the sky-listener"
- "the storm-witness"
- "the crossing-keeper"

### § 6.5 Element: shadow

**epithet (10):**
- "veil-marked"
- "moonless"
- "umbra-bound"
- "dusk-named"
- "half-lit"
- "between-handed"
- "long-shadowed"
- "soft-footed"
- "quiet-throated"
- "unwitnessed"

**motif (10):**
- "the unlit corridor"
- "the long dusk"
- "the watching dark"
- "the moon behind cloud"
- "the silence before the word"
- "the door between rooms"
- "the path no torch lights"
- "the threshold at the edge"
- "the dark that remembers"
- "the veil between hours"

**archetype-name (5):**
- "the watcher"
- "the threshold-keeper"
- "the unseen"
- "the veil-walker"
- "the listener-in-dusk"

### § 6.6 Element: lightning

**epithet (10):**
- "storm-handed"
- "spark-marked"
- "flash-named"
- "thunder-spoken"
- "high-charged"
- "bolt-true"
- "static-veiled"
- "arc-bound"
- "lit-throated"
- "fork-handed"

**motif (10):**
- "the sudden judgment"
- "the unwarned strike"
- "the storm above the field"
- "the bolt that chose"
- "the long arc"
- "the watching cloud"
- "the flash before the count"
- "the thunder after"
- "the unspent charge"
- "the high tower struck"

**archetype-name (5):**
- "the storm-witness"
- "the spark-keeper"
- "the bolt-caller"
- "the high-watcher"
- "the thunder-named"

### § 6.7 Element: arcane

**epithet (10):**
- "sigil-marked"
- "rune-handed"
- "circle-bound"
- "lattice-true"
- "geometry-named"
- "thread-spoken"
- "weave-fingered"
- "pattern-witnessed"
- "diagram-bearing"
- "axiom-bound"

**motif (10):**
- "the unbroken pattern"
- "the long lattice"
- "the circle that holds"
- "the figure beneath the figure"
- "the diagram in the dust"
- "the watching geometry"
- "the line that opens"
- "the rune before the door"
- "the weave the world rests on"
- "the silent equation"

**archetype-name (5):**
- "the pattern-keeper"
- "the lattice-walker"
- "the circle-tender"
- "the diagram-witness"
- "the thread-reader"

### § 6.8 Element: faith-holy

**epithet (10):**
- "vow-bound"
- "lamp-bearing"
- "vigil-true"
- "oath-named"
- "censer-handed"
- "litany-throated"
- "candle-marked"
- "psalm-spoken"
- "thrice-witnessed"
- "ash-marked" *[note: also valid as fire epithet; element-coherence resolved by cluster centroid at fire-time]*

**motif (10):**
- "the unbroken vow"
- "the long vigil"
- "the lamp at the gate"
- "the watching above the watchers"
- "the litany that does not end"
- "the candle in the wind"
- "the oath the dust remembers"
- "the procession of the third hour"
- "the high seat that waits"
- "the bell at first light"

**archetype-name (5):**
- "the vigil-keeper"
- "the lamp-bearer"
- "the witness-of-the-vow"
- "the litany-singer"
- "the gate-tender"

---

## § 6 Closure notes

**Cross-element collision policy (one explicit example surfaced):** "ash-marked" appears in both fire (§ 6.1 epithet pool) and faith-holy (§ 6.8 epithet pool, flagged). At Phase 5 LLM consumption time, the cluster centroid's primary element resolves which pool the token is drawn from; if a cluster genuinely lands on (fire × faith-holy hybrid centroid), the collision is *productive* — the LLM may draw the epithet under either element header. Future cross-element collision additions (Stage 3 cell-authoring may surface more) should be tagged inline as `[also valid as X]` rather than de-duplicated, because the duplication carries thematic signal (some emblems genuinely belong to multiple elements; the substrate confirms this).

**No-place-name / no-lore-fragment at element-only layer (deliberate):**

- Place-names ("the bonefields," "the salt-roads," "the cinder-passes" — Stage 1 § 5 examples) carry lineage-binding through their toponymic register. A place-name without lineage-anchor either defaults european (e.g., "the bonefields" reads northern-european) or lands generic-fantasy-bland (e.g., "the place-of-fire" reads non-evocative). Per-cell sketches (Stage 3 § 7) supply place-names where the (element, lineage) intersection gives the toponym its tonal register.
- Lore-fragments ("exiled when the third star fell," "the river chose them") are similarly anchored — they read most strongly when the lineage informs the narrative-shape (e.g., "exiled" carries different register in european vs east_asian vs middle_eastern faction storytelling). Per-cell sketches supply lore-fragments where the (element, lineage) cell is dense enough to support coherent backstory-seeding.

**Element-only fallback consumption pattern (LLM-prompt surface):**

Phase 5 LLM prompts MAY draw from § 6 alone when:
1. Cluster receives `unknown` or `cross_cultural` lineage meta-tag (per § 4 conventions)
2. Per-cell sketch at (element, lineage) intersection is labeled SPARSE (5-20 substrate refs) and Wave A/B fire-time policy permits element-only fallback
3. Cell is labeled EMPTY (<5 substrate refs) — element-only is the only available pool

When element-only is the source, the LLM assembly template still produces `{epithet} {meta-noun} of the {motif}` with `{archetype-name}` available for Wave B per-kit identity. Place-name and lore-fragment slots are EITHER (a) omitted, OR (b) sourced from generic-fantasy fallback if the prompt requires them and no cell-sketch is available — both behaviors are valid per Wave A § 12 / Wave B § 5.2 spec.

**Substrate-led discipline preservation (Discipline #41 mid-stage check):**

Pre-Stage-4 grep audit verification (informal, full audit at Stage 4): scanned the 200 entries above for class-vocabulary leak — zero hits for `warrior`, `mage`, `rogue`, `hunter`, `paladin`, `summoner`, `monk`, `druid`, `necromancer`, `sorcerer`, `witch`, `knight`, `soldier`, `ranger`, `archer`, `assassin`, `berserker`, `gladiator`, `fighter`, `controller`, `tank`, `support`, `healer`, `damage`, `dps`. Also zero hits for role-orientation tokens (`damage`, `support`, `control`, `hybrid`). One borderline: "the watcher" (§ 6.5 shadow archetype-name) is *narrative role* (watcher = one-who-witnesses), NOT *combat role* — clean per Ground Rule #4 disambiguation. "the messenger" (§ 6.4 wind archetype-name) is similarly *narrative role* (messenger = courier of word/news), NOT *combat role*.

---

## § 7 Per-cell sketches (element × cultural_lineage)

This section provides the **lineage-anchored** vocabulary pool per dense (element, lineage) intersection. Cells are sorted by substrate density (gandalf judgment grounded in `weapon_knowledge_entries` v1_scope=1 lineage distribution + thematic-canon richness in the wider corpus — historical/mythological named-item canon that augments the substrate row count for thematic-richness purposes per Ground Rule #1).

**Substrate density baseline (v1_scope=1 lineage counts, queried 2026-05-27):**

| Lineage | substrate count | tier |
|---|---|---|
| fantasy_generic | 1124 | dense (universal-fallback synthetic) |
| european | 952 | dense |
| east_asian | 263 | dense |
| south_asian | 78 | moderate-dense |
| middle_eastern | 36 | moderate-dense (thematic-canon-augmented to dense per Ground Rule #1; see note below) |
| southeast_asian | 27 | moderate |
| mesoamerican | 9 | sparse-but-thematic-coherent (exempted contamination per disposition doc) |
| unknown / south_american_indigenous / african | 2-4 each | EMPTY per Ground Rule #3 |
| n.am.indigenous / arctic_circumpolar / oceanic / sci_fi_generic | 0 in v1_scope | EMPTY (contamination-watch retained per § 4) |

**Why middle_eastern reads dense despite 36 substrate count:** the substrate row count under-represents middle_eastern thematic-canon depth. The wider thematic corpus (Abrahamic faith-holy tradition / Persian wind+fire mythology / Egyptian sun-fire iconography / Arabian poetic motif richness) is the largest extant outside east_asian for the elements covered. The cell-density audit weights *substrate-anchored thematic vocabulary availability*, not raw row count alone (per Ground Rule #1's substrate-evidence trinity: substrate rows + legolas crawl outputs + existing canonical/story/ thematic precedent). South_asian sits in the same posture (78 rows but ancient Vedic/Hindu/Buddhist canon dense across faith-holy + lightning).

**Cell selection (15 dense; 8 SPARSE; remainder EMPTY):**

Dense cells (sketched below at 25-35 entries each, within 20-50 sketch tier):

1. § 7.1 — fire × european
2. § 7.2 — fire × east_asian
3. § 7.3 — fire × middle_eastern
4. § 7.4 — water × east_asian
5. § 7.5 — water × european
6. § 7.6 — earth × european
7. § 7.7 — earth × east_asian
8. § 7.8 — wind × middle_eastern
9. § 7.9 — wind × east_asian
10. § 7.10 — shadow × european
11. § 7.11 — shadow × east_asian
12. § 7.12 — lightning × european
13. § 7.13 — lightning × south_asian
14. § 7.14 — faith-holy × european
15. § 7.15 — faith-holy × middle_eastern

SPARSE cells (labeled only, no entries — Cycle 15+ expansion candidates): § 7.16

EMPTY cells (labeled only, contamination-watch retained where applicable): § 7.17

---

### § 7.1 fire × european

**Substrate anchor:** european substrate rows (952) — forge tradition (smith-named blades — *Tizona*, *Joyeuse*, *Curtana* in extended canon), pyre/hearth folklore, dragon-fire mythos (Beowulf / Fafnir), siege-fire tradition. Thematic-canon: forge-god (Wayland / Volund), hearth-goddess (Hestia-Brigid layer), fire-festival (Beltane / Walpurgis).

**Epithets (10):**
- "forge-blooded"
- "hearth-sworn"
- "pyre-marked"
- "ember-eyed"
- "kiln-tempered"
- "torch-bearing"
- "smoke-throated"
- "anvil-born"
- "bellows-lunged"
- "scorch-handed"

**Motifs (10):**
- "the smith's last fire"
- "the unquenched hearth"
- "the funeral pyre that would not die"
- "the dragon's long memory"
- "the forge that named the blade"
- "the watchfire on the wall"
- "the burning ash-tree"
- "the candle in the crypt"
- "the iron made red"
- "the keep that burned three times"

**Archetype-names (5):**
- "the smith"
- "the bell-ringer"
- "the kindler"
- "the watcher of the watchfire"
- "the keeper of the long hearth"

**Place-names (3):**
- "the cinder-keep"
- "the forge-roads"
- "the ash-meadow"

**Lore-fragments (3):**
- "they kept the forge lit through the winter the king did not return"
- "the smith named the blade with her last breath"
- "the hearth would not take cold iron"

---

### § 7.2 fire × east_asian

**Substrate anchor:** east_asian substrate rows (263) — named blade tradition (*Masamune* / *Sadamune* / *Yoshimitsu* family blades repeated through substrate; folded-steel forge practice as thematic anchor), dragon-flame canon (Chinese *long* tradition — *Green Dragon Crescent Blade* in substrate), lantern + festival fire, samurai-pyre rite. Thematic-canon: kitsune-fire (foxfire), kirin-flame, Buddhist cremation fire, fire-festival (Obon, Toji).

**Epithets (10):**
- "lacquer-burnt"
- "lantern-lit"
- "tempered-thrice"
- "foxfire-touched"
- "kiln-glazed"
- "cinder-petalled"
- "ember-veiled"
- "blade-bright"
- "incense-throated"
- "scorch-silked"

**Motifs (10):**
- "the lantern that lit the river of the dead"
- "the blade folded one thousand times"
- "the fox carrying a torch through the rice"
- "the temple fire that never sleeps"
- "the dragon coiled in the brazier"
- "the cremation-pyre under the cherry trees"
- "the lacquer scorched but not broken"
- "the smith's three-day fast before the steel"
- "the festival flame on the seventh night"
- "the calligrapher's burned draft"

**Archetype-names (5):**
- "the lantern-keeper"
- "the brazier-tender"
- "the smith-ascetic"
- "the fox-walker"
- "the carrier of the temple flame"

**Place-names (3):**
- "the lantern-road"
- "the smithyard at Mount Hira"
- "the brazier-shrine"

**Lore-fragments (3):**
- "the fox left her torch at the threshold"
- "the smith dreamt the blade before he forged it"
- "the lantern guided three souls and burned out at the fourth"

---

### § 7.3 fire × middle_eastern

**Substrate anchor:** middle_eastern substrate (36 rows under-represents canon) — Tutankhamun's meteoric-iron dagger (substrate); thematic-canon: Zoroastrian sacred fire (*atar*), phoenix (Bennu / Greek-via-Egypt phoenix), desert-sun iconography, Sumerian fire-deity (Gibil / Girra), Persian fire-temple (atashkadeh), Arabian poetic flame-imagery (jahili poetry).

**Epithets (10):**
- "sun-scorched"
- "phoenix-marked"
- "atashkadeh-sworn"
- "myrrh-burnt"
- "dune-blistered"
- "ember-veiled" *[also valid in § 7.2 east_asian — disambiguate at fire-time]*
- "noon-eyed"
- "saffron-lit"
- "brand-pressed"
- "censer-handed"

**Motifs (10):**
- "the sun that did not set for forty days"
- "the fire that the wind cannot take"
- "the phoenix's third burning"
- "the temple flame older than the prophet"
- "the desert that remembers footprints in glass"
- "the brand on the camel's flank"
- "the lamp the traveler left burning"
- "the prayer-rug singed at the corners"
- "the censer that emptied at the king's last word"
- "the sand turned to mirror"

**Archetype-names (5):**
- "the fire-keeper"
- "the noon-walker"
- "the censer-bearer"
- "the desert ascetic"
- "the lamp-trimmer"

**Place-names (3):**
- "the glass-desert"
- "the fire-temple at the seven gates"
- "the sun-road"

**Lore-fragments (3):**
- "the fire was lit when the city was named and has not gone out"
- "she walked into the noon-sun and the sand kept her shape"
- "the phoenix shed three feathers and they became cities"

---

### § 7.4 water × east_asian

**Substrate anchor:** east_asian substrate — *Hyūga Masamune* (named water-tradition blade subset), naginata + monsoon tradition. Thematic-canon: river-dragon (*long* of the great rivers — Yangtze / Yellow), koi/ascension myth, monsoon-festival, Buddhist water-purification (*misogi*), Shinto sea-kami (Watatsumi), typhoon-as-divine-wind ambivalence (cross-references § 7.9 wind).

**Epithets (10):**
- "monsoon-blessed"
- "koi-scaled"
- "river-bound"
- "tide-walked"
- "rain-veiled"
- "lotus-rooted"
- "deep-eyed"
- "mist-throated"
- "rapids-tongued"
- "well-sworn"

**Motifs (10):**
- "the koi that climbed the waterfall"
- "the dragon under the deepest pool"
- "the well that does not freeze"
- "the river that changed course in one night"
- "the monsoon that broke the year"
- "the lotus opening at dawn on the still water"
- "the tide that returned the lost sword"
- "the mist that hid the boat from the shore"
- "the rain that washed the calligraphy from the door"
- "the deep that kept the bell"

**Archetype-names (5):**
- "the river-walker"
- "the well-keeper"
- "the tide-reader"
- "the rain-listener"
- "the ferryman"

**Place-names (3):**
- "the koi-pools"
- "the seven wells"
- "the mist-bridge"

**Lore-fragments (3):**
- "the river chose the bridge and the bridge chose her"
- "the bell still rings beneath the deep pool on the night of the festival"
- "the koi climbed and what it became was not a dragon"

---

### § 7.5 water × european

**Substrate anchor:** european substrate — Excalibur-from-the-lake canon (Arthurian), Lady-of-the-Lake / Nimue, north-sea seafaring tradition, *Niflheim* / mist-water cosmology, well-and-spring sanctity (Brigid's wells, sacred springs), drowned-village folklore.

**Epithets (10):**
- "lake-given"
- "fen-born"
- "tide-bound"
- "well-blessed"
- "drowned-sworn"
- "mist-walked"
- "spring-anointed"
- "salt-burned"
- "fjord-cold"
- "kelp-tangled"

**Motifs (10):**
- "the sword from the still water"
- "the well that does not run dry"
- "the bell of the drowned village"
- "the kelpie at the ford"
- "the long ship returning with one rower"
- "the spring the saint blessed"
- "the fen that swallowed the road"
- "the tide that gives back what was taken"
- "the lake where the king was carried"
- "the mist on the moor at the funeral"

**Archetype-names (5):**
- "the well-keeper"
- "the ferrier"
- "the fen-walker"
- "the kelp-gatherer"
- "the lady of the water"

**Place-names (3):**
- "the drowned-village"
- "the nine wells"
- "the fenmoor"

**Lore-fragments (3):**
- "the hand rose from the water at the third hour"
- "they say the bell still rings on the night the village went under"
- "the well took the coin and gave back a sword"

---

### § 7.6 earth × european

**Substrate anchor:** european substrate — *Bardiche* / *Guisarme* (substrate polearm tradition rooted in field-soldier earth-bond), barrow-and-mound burial canon (Sutton Hoo / Brittany dolmens), Saxon/Welsh hill-fort tradition, henge stones, miners' folklore (Cornish knockers / Germanic kobolds).

**Epithets (10):**
- "barrow-marked"
- "stone-bound"
- "iron-veined"
- "loam-handed"
- "henge-sworn"
- "moor-rooted"
- "fen-rooted" *[disambiguate from § 7.5 water-fen — earth-fen reads bog-as-solid-ground]*
- "ash-tree-rooted"
- "delved-deep"
- "grave-tended"

**Motifs (10):**
- "the stone that was set before the king was born"
- "the barrow opened only once"
- "the henge that aligns with the midwinter sun"
- "the iron in the hill that called the smiths"
- "the moor that does not forget"
- "the ash-tree at the crossroads"
- "the fields that hold the bones of the last battle"
- "the cairn the shepherds add to each year"
- "the mine that takes one in seven"
- "the standing stone that walks at midwinter"

**Archetype-names (5):**
- "the stone-walker"
- "the barrow-keeper"
- "the delver"
- "the moor-watcher"
- "the cairn-builder"

**Place-names (3):**
- "the barrow-fields"
- "the henge-meadow"
- "the long-mine"

**Lore-fragments (3):**
- "they buried the king with his shield-arm to the east"
- "the stone was carried three days by the giants who left no other mark"
- "the mine took her grandfather and his father before"

---

### § 7.7 earth × east_asian

**Substrate anchor:** east_asian substrate (subset thematic-coherent) — Buddhist stone-garden tradition (*karesansui*), jade-as-stone canon, mountain-hermit tradition (sennin / xian), terraced-rice landscape, Mount Hiei / Mount Tai sacred-mountain canon. Substrate lineage primarily blade-canon, so earth × east_asian leans on thematic-canon augmentation (per Ground Rule #1).

**Epithets (10):**
- "jade-veined"
- "mountain-sworn"
- "terrace-rooted"
- "stone-garden-keeping"
- "moss-handed"
- "pine-rooted"
- "cliff-eyed"
- "cairn-stacking"
- "earth-tongued"
- "boulder-shadowed"

**Motifs (10):**
- "the stone garden raked at dawn for forty years"
- "the jade that turned in the keeping"
- "the mountain that grew while the hermit climbed"
- "the terrace that fed the village through three famines"
- "the pine bent by the wind but not the years"
- "the cairn at the pass that names the dead"
- "the rock the master would not move"
- "the boulder split by the bamboo root"
- "the moss-stone marking the boundary the monks set"
- "the cliff-temple reached only at the dry season"

**Archetype-names (5):**
- "the mountain-hermit"
- "the stone-gardener"
- "the terrace-keeper"
- "the cliff-pilgrim"
- "the cairn-namer"

**Place-names (3):**
- "the stone-garden temple"
- "the seven-terraced slope"
- "the cliff-pass"

**Lore-fragments (3):**
- "the master raked the gravel each morning and refused to name the pattern"
- "the jade pendant turned green in his keeping over thirty years"
- "they built the cairn one stone for each man who did not come down"

---

### § 7.8 wind × middle_eastern

**Substrate anchor:** middle_eastern substrate (thematic-canon-augmented) — Persian *simoom* and Arabian *sirocco* (desert wind tradition), Sufi whirling-dervish canon (substrate: *Dervish Ax*), Egyptian wind-deity Shu, Mesopotamian Pazuzu (south-west wind). Wind as judgment / wind as carrier-of-prayer dual canon.

**Epithets (10):**
- "simoom-touched"
- "sirocco-sworn"
- "whirling"
- "dune-walked"
- "breath-given"
- "djinn-marked"
- "veil-stirring"
- "sand-tongued"
- "prayer-borne"
- "noon-stilled"

**Motifs (10):**
- "the wind that crossed the desert in one night"
- "the dervish that turned for three days without stopping"
- "the storm that buried the caravan and revealed the city"
- "the breath that called the djinn to the lamp"
- "the wind that carried the prayer to the mountain"
- "the still hour when the wind drops at noon"
- "the veil lifted by the wind at the well"
- "the sand-pillar that walked across the empty quarter"
- "the wind that scattered the night-walker's footprints"
- "the breath of the prophet over the still water"

**Archetype-names (5):**
- "the wind-walker"
- "the dervish"
- "the breath-keeper"
- "the dune-reader"
- "the message-runner"

**Place-names (3):**
- "the empty quarter"
- "the wind-cut cliffs"
- "the dervish-court"

**Lore-fragments (3):**
- "the wind brought her name to the village three days before she arrived"
- "the dervish turned until the desert turned with him"
- "the storm closed the road and the city behind it was older than the kingdom"

---

### § 7.9 wind × east_asian

**Substrate anchor:** east_asian substrate — naginata in storm-tradition (substrate), *kamikaze* / "divine wind" canon (Mongol-invasion repulsion), typhoon mythology, fox-wind (kitsune folklore), tengu wind-mastery, sky-lantern tradition.

**Epithets (10):**
- "typhoon-blessed"
- "divine-wind-marked"
- "tengu-taught"
- "sky-lanterned"
- "bamboo-whispered"
- "crane-shadowed"
- "cloud-walked"
- "kitsune-led"
- "storm-eaved"
- "breath-of-mountain"

**Motifs (10):**
- "the wind that broke the invader's fleet"
- "the tengu's lesson the swordsman never spoke of"
- "the sky-lantern that crossed the strait"
- "the typhoon that named the year"
- "the bamboo bent and unbroken"
- "the crane crossing the morning sky"
- "the fox that ran ahead of the wind"
- "the mountain's breath at the high pass"
- "the storm that returned the sword to its keeper"
- "the kite that carried a child's name to the dead"

**Archetype-names (5):**
- "the wind-listener"
- "the kite-flyer"
- "the tengu-student"
- "the sky-walker"
- "the bamboo-cutter"

**Place-names (3):**
- "the wind-gate pass"
- "the storm-strait"
- "the high bamboo"

**Lore-fragments (3):**
- "the wind came when the prayer was finished and not before"
- "the tengu taught him the cut and then would not let him speak of it"
- "the kite carried her brother's name across the strait and did not return"

---

### § 7.10 shadow × european

**Substrate anchor:** european substrate — necromancer-grave tradition (Germanic / Slavic), black-knight folklore, heath-wraith canon (Scots-English borderlands), crypt-and-catacomb thematic depth (Roman + Christian layer), Wild-Hunt mythology (Wodan/Odin night-ride), changeling-and-faerie-dark thread.

**Epithets (10):**
- "grave-walked"
- "wraith-marked"
- "moor-shadowed"
- "crypt-sworn"
- "hunt-followed"
- "raven-eyed"
- "night-bound"
- "barrow-shadowed"
- "changeling-touched"
- "shroud-veiled"

**Motifs (10):**
- "the rider who passes in the long night"
- "the shadow that did not follow the man"
- "the crypt door that closed without hand"
- "the heath where the road forgets itself"
- "the raven at the gallows-foot"
- "the changeling-child the mother kept"
- "the moor-mist with the smell of iron"
- "the bell that tolls though no one rings it"
- "the wild hunt heard on the seventh night"
- "the candle that burned blue at the grave"

**Archetype-names (5):**
- "the bell-tender of the night-chapel"
- "the moor-wanderer"
- "the grave-tender"
- "the rider"
- "the watcher at the gate"

**Place-names (3):**
- "the gallows-heath"
- "the long-night moor"
- "the crypt-chapel"

**Lore-fragments (3):**
- "she heard the bell on the night her brother did not come home"
- "the rider passed three times and on the fourth night took the herald with him"
- "they buried the lord with his hounds and the hounds were heard on the moor for a year"

---

### § 7.11 shadow × east_asian

**Substrate anchor:** east_asian substrate (thematic-canon-augmented) — shinobi / ninja folklore (historical-fiction-augmented canon), oni and yokai night-tradition, hyakki-yagyo (night parade of one hundred demons), Buddhist hell-realms iconography, kabuki ghost-play tradition (*Yotsuya Kaidan*).

**Epithets (10):**
- "night-walked"
- "oni-marked"
- "yokai-shadowed"
- "lantern-blown-out"
- "rooftop-treading"
- "ghost-veiled"
- "ink-blooded"
- "moonless-sworn"
- "shoji-shadowed"
- "hyakki-followed"

**Motifs (10):**
- "the lantern that went out as the messenger arrived"
- "the parade of one hundred demons that no living eye should meet"
- "the shadow on the shoji that had no body in the room"
- "the rooftop where the shadow-walker waited two nights"
- "the inkstone that filled itself in the dark"
- "the ghost-bride at the upturned cup"
- "the oni who kept the bridge-toll honest"
- "the long-armed yokai at the well"
- "the moonless night the dōjō burned"
- "the kabuki line that summoned the wrong spirit"

**Archetype-names (5):**
- "the lantern-snuffer"
- "the night-walker"
- "the rooftop-treader"
- "the ink-keeper"
- "the bridge-watcher"

**Place-names (3):**
- "the unlit district"
- "the demon-parade road"
- "the rooftop-quarter"

**Lore-fragments (3):**
- "the lantern went out the moment he spoke her old name"
- "they say the parade passes the bridge on the seventh night and the bridge-keeper averts her eyes"
- "the ghost wore the bride's red and the family hid all the cups"

---

### § 7.12 lightning × european

**Substrate anchor:** european substrate — Norse Thor/Mjolnir canon, Greek/Roman Zeus/Jupiter sky-father, Germanic Donar layer, Slavic Perun, storm-god lineage. Hammer-and-bolt iconography deep.

**Epithets (10):**
- "thunder-marked"
- "hammer-handed"
- "bolt-struck"
- "storm-sworn"
- "skyfather-blessed"
- "oak-split"
- "ridge-burned"
- "white-flashed"
- "donar-touched"
- "thunderhead-veiled"

**Motifs (10):**
- "the hammer thrown across the storm-sea"
- "the oak split by the bolt and re-grown crooked"
- "the bell that rang itself when the storm broke"
- "the rider with the hammer at the longest night"
- "the storm that named the year of the bad harvest"
- "the white flash that revealed the moor"
- "the ridge-line where the lightning always strikes first"
- "the tower struck three summers running"
- "the storm-king's chariot wheels in the cloud"
- "the bolt that took the wrong man at the threshing-floor"

**Archetype-names (5):**
- "the storm-watcher"
- "the bell-tender"
- "the ridge-walker"
- "the oak-marker"
- "the sky-reader"

**Place-names (3):**
- "the storm-ridge"
- "the split-oak hill"
- "the thunder-meadow"

**Lore-fragments (3):**
- "the bolt struck the oak the day the queen was crowned"
- "they say the hammer is heard above the storm and the ship that hears it returns"
- "the storm-watcher counted three flashes before the thunder and named the hour"

---

### § 7.13 lightning × south_asian

**Substrate anchor:** south_asian substrate (78 rows) — *Vajra* (substrate; thunderbolt-weapon, Indra's principal armament), *Indraastra* (substrate; Indra's missile), Buddhist *vajra* iconography (diamond-thunderbolt), Vedic storm-god canon, monsoon-lightning thematic depth.

**Epithets (10):**
- "vajra-marked"
- "indra-blessed"
- "monsoon-burned"
- "diamond-bolted"
- "ashvin-touched"
- "thunder-sworn"
- "rain-broken"
- "sky-roared"
- "naga-flashed"
- "mantra-charged"

**Motifs (10):**
- "the vajra that does not break and cannot be broken"
- "the bolt Indra threw at the dawn of the storm-season"
- "the diamond at the heart of the thunder"
- "the rain that the lightning preceded by three breaths"
- "the temple bell rung by the strike"
- "the mantra spoken once and remembered by the sky"
- "the cobra that rose at the thunder's voice"
- "the elephant-king's tusk lit white at the storm's edge"
- "the monsoon's first crack across the plain"
- "the ascetic's staff that drew the bolt and would not splinter"

**Archetype-names (5):**
- "the vajra-bearer"
- "the storm-ascetic"
- "the mantra-speaker"
- "the cloud-rider"
- "the sky-priest"

**Place-names (3):**
- "the thunder-plateau"
- "the monsoon-coast"
- "the diamond-temple"

**Lore-fragments (3):**
- "the vajra was given when the demon-king refused the third offering"
- "the mantra that called the bolt was taught only at the rains' beginning"
- "the temple bell was struck by the storm and rang for seven days"

---

### § 7.14 faith-holy × european

**Substrate anchor:** european substrate — *Curtana* / *Joyeuse* (Christian-blessed regalia in extended canon), crusader-era reliquary tradition, monastic order canon (Benedictine / Cistercian), pilgrimage routes (Compostela / Canterbury), saints'-relic culture, Templar/Hospitaller military-monastic lineage.

**Epithets (10):**
- "chrism-anointed"
- "reliquary-bound"
- "pilgrim-shod"
- "vesper-blessed"
- "cloister-sworn"
- "psalter-marked"
- "candle-lit"
- "rosary-told"
- "vow-bound"
- "saint-shadowed"

**Motifs (10):**
- "the relic that wept on the saint's day"
- "the candle that burned three nights in the storm"
- "the bell that called the brothers to the third hour"
- "the pilgrim road worn smooth by a thousand years of knees"
- "the chrism that did not run dry through the long siege"
- "the psalter the abbot kept open at the page of the lament"
- "the vow spoken in the cloister and never broken"
- "the saint's bone that healed the leper at the third asking"
- "the reliquary carried at the head of the long procession"
- "the bell tolled at the dying king's last breath"

**Archetype-names (5):**
- "the pilgrim"
- "the bell-ringer"
- "the candle-tender"
- "the reliquary-bearer"
- "the cloister-keeper"

**Place-names (3):**
- "the pilgrim-road"
- "the cloister-chapel"
- "the relic-cathedral"

**Lore-fragments (3):**
- "she walked the road from the sea to the cathedral and did not speak the whole way"
- "the bell rang the office at the third hour and the city quieted with it"
- "the relic was carried before the army and the army did not break"

---

### § 7.15 faith-holy × middle_eastern

**Substrate anchor:** middle_eastern substrate — Abrahamic faith-holy lineage shared across three traditions (Jewish prophetic / Christian Eastern Orthodox / Islamic Sufi), Zoroastrian fire-temple priest canon, desert-prophet tradition, pilgrimage canon (Hajj, Holy Land), poetic devotional tradition (Rumi / Hafez / psalmist).

**Epithets (10):**
- "prophet-marked"
- "pilgrim-stoned" *[stone-of-the-pilgrim = scriptural anchor, NOT class-vocabulary]*
- "minaret-shadowed"
- "scripture-bound"
- "desert-prayed"
- "qibla-facing"
- "psalm-throated"
- "fast-thinned"
- "wisdom-tongued"
- "veil-marked"

**Motifs (10):**
- "the prophet who walked into the desert and returned with the law"
- "the pilgrim who circled the stone seven times"
- "the prayer called from the minaret at the first light"
- "the desert that took the king's pride and gave back his humility"
- "the scripture copied by hand for a thousand years"
- "the well that the patriarch dug and the village still drinks from"
- "the fast that lasted the moon's full cycle"
- "the wisdom that came after the third silence"
- "the veil that hid the queen at the threshold of the temple"
- "the lamp the pilgrim carried to the holy city"

**Archetype-names (5):**
- "the pilgrim"
- "the muezzin"
- "the scripture-copier"
- "the desert-ascetic"
- "the lamp-bearer"

**Place-names (3):**
- "the holy city"
- "the pilgrim-stones"
- "the desert-shrine"

**Lore-fragments (3):**
- "she crossed the desert with one waterskin and arrived at the city before the fast ended"
- "the call to prayer was given by a voice the city had not heard before"
- "the scripture was copied through three generations and the original was lost without anyone noticing"

---

### § 7.16 SPARSE cells (labeled only — Cycle 15+ expansion candidates)

The following (element × lineage) cells have substrate density in the 5-20 reference range (or thematic-canon support that is real but thin). Per Ground Rule #3, no entries are authored at Stage 3; cells receive SPARSE labels and are flagged for Cycle 15+ substrate-anchored augmentation work (gandalf will commission legolas Mode A research to surface thematic-canon vocabulary when one of these cells is exercised by a Wave A/B cluster).

| Cell | substrate basis | Cycle 15+ augmentation notes |
|---|---|---|
| arcane × european | european scholar / Hermetic / wizard-tower canon (thematic-canon present but element-only § 6.7 covers most usage) | augment with grimoire-tradition + alchemist + court-mage vocabulary |
| arcane × east_asian | Taoist / wuxia / talismanic canon | augment with *fulu* talisman tradition + immortals' arts + Yin-Yang scholarship |
| faith-holy × south_asian | Vedic / Buddhist / Jain canon (faith × south_asian under-served by current substrate; bell, mantra, mandala vocabulary thin in v1_scope) | augment with mantra + bodhisattva-naming + temple-architecture vocabulary |
| water × southeast_asian | substrate: *Kris* / *Lantaka* / sea-trading canon | augment with naga + bajau-sea-folk + monsoon-port vocabulary |
| earth × south_asian | substrate thin; thematic basis: Himalayan-hermit + cave-temple canon | augment with naga (chthonic layer) + cave-shrine + Vindhya tradition |
| fire × south_asian | substrate thin; thematic basis: Agni Vedic fire-deity + yajna ritual fire | augment with yajna + Agni iconography + cremation-ghat vocabulary |
| wind × european | substrate thin; thematic basis: Aeolus + Boreas Greek + Celtic sky-tradition | augment with Aeolian + four-winds canon + sail-tradition vocabulary |
| lightning × east_asian | substrate thin (substrate primarily blade-canon); thematic basis: *Raijin* thunder-god + dragon-storm canon | augment with Raijin + drum-iconography + cloud-dragon vocabulary |
| shadow × middle_eastern | substrate thin; thematic basis: jinn (twilight tradition) + assassin-canon (historical *Hashshashin*) | augment with jinn + twilight-hour + caravan-night vocabulary [contamination-watch: assassin lineage requires care — historical-figure not class-token] |
| fire × fantasy_generic | covered by element-only § 6.1; explicit cell exists as substrate-fallback synthetic | augment only if Wave A/B output shows fantasy_generic + element cells under-serving common LLM-prompt patterns |
| (and 7 more fantasy_generic × element cells) | all covered by element-only § 6.* | same as above — augment-on-demand |
| (and ~30 moderate-lineage × off-axis-element cells) | various | substrate-led augmentation per Wave 3+ exercise data |

**SPARSE-cell consumption pattern at fire-time:** Phase 5 LLM prompts hitting a SPARSE cell fall back to (a) element-only § 6 layer for adjectival/emblematic vocabulary, plus (b) the dense same-element cell with the closest lineage-adjacent cultural anchor (e.g., fire × south_asian SPARSE → fall back to fire-only § 6.1 + fire × middle_eastern § 7.3 as lineage-adjacent if cluster shows middle_eastern proximity, OR fire × east_asian § 7.2 if east_asian proximity).

---

### § 7.17 EMPTY cells (labeled only — contamination-watch retained per § 4 where applicable)

The following (element × lineage) cells have <5 substrate references AND insufficient thematic-canon depth at Stage 3 to support 20-50 entries without prescriptive risk. Per Ground Rule #3, no entries are authored. Marginal-lineage contamination watch retained per § 4.

| Cell axis | Lineages affected | Disposition |
|---|---|---|
| any element × african | african (2 substrate rows in v1_scope) | EMPTY; Cycle 15+ requires elrond substrate re-curation BEFORE legolas Mode A — current substrate too thin to confirm cell viability |
| any element × n.am.indigenous | n.am.indigenous (0 v1_scope rows) | EMPTY [contamination-watch retained]; per disposition doc `n-am-indigenous-no-cluster-disposition-2026-05-23.md`, cell remains EMPTY pending substrate re-curation; LLM consumption falls back to fantasy_generic § 6 + cross_cultural meta-tag handling |
| any element × s.am.indigenous | s.am.indigenous (4 v1_scope rows; sparse-to-empty) | EMPTY [contamination-watch retained] per disposition doc |
| any element × arctic_circumpolar | arctic_circumpolar (0 v1_scope rows) | EMPTY [contamination-watch retained] per disposition doc; fall back to element-only + fantasy_generic |
| any element × oceanic | oceanic (0 v1_scope rows) | EMPTY [contamination-watch retained] per disposition doc; fall back to element-only + fantasy_generic |
| any element × sci_fi_generic | sci_fi_generic (substrate moderate but tone-mismatched to current Phase 0 fantasy register) | EMPTY for Phase 0 (Cycle 15+ revisit if game register shifts) |
| any element × mesoamerican | mesoamerican (9 v1_scope rows; thematic-canon-augmented possible) | EMPTY at Stage 3 (not contamination-watch — disposition exempts); single cell candidate fire × mesoamerican (sun-fire / blood-fire canon) is Cycle 15+ first-augmentation candidate per disposition note |
| faith-holy × east_asian | substrate primarily blade-canon; faith-holy × east_asian thin under v1_scope (Buddhist/Shinto faith-holy vocabulary not concentrated in weapon substrate) | EMPTY at Stage 3; Cycle 15+ augmentation candidate (Buddhist + Shinto faith-holy distinct from § 7.2 fire / § 7.4 water cells which already absorbed some thematic motif) — substrate re-curation toward non-weapon devotional substrate needed first |
| arcane × middle_eastern | thematic basis exists (alchemy / al-Khwarizmi scholarly tradition / 1001-Nights-genie-magic) but element-only § 6.7 covers core usage; not Stage-3 priority | EMPTY at Stage 3; Cycle 15+ augmentation candidate |
| (and remaining EMPTY cells per substrate void) | all remaining (element × lineage) combinations not enumerated in §§ 7.1–7.16 | EMPTY default; fall back to element-only § 6 + meta-tag handling per § 4 |

**EMPTY-cell consumption pattern at fire-time:** Phase 5 LLM prompts hitting an EMPTY cell fall back to (a) element-only § 6 layer as primary, plus (b) `cross_cultural` or `unknown` meta-tag handling per § 4. The `[contamination-watch]` marker on marginal-lineage EMPTY cells signals additional caution at LLM-prompt assembly: do NOT prescribe lineage-specific motifs from the marginal-lineage substrate that survived the v1_scope filter, because those entries are precisely the misattribution-risk surface per Mode A/B/C/D contamination pattern. Use element-only as the lineage-agnostic safe layer instead.

---

### § 7 Per-cell sketches — closure notes

**Total entries authored across § 7.1–7.15 (15 dense cells):**
- Per-cell distribution per Ground Rule #3 target (~31 entries): 10 epithet + 10 motif + 5 archetype-name + 3 place-name + 3 lore-fragment = 31 entries
- Total: 15 cells × 31 entries = **465 lineage-anchored entries** (within sketch tier; well below Cycle 15+ full-granularity 1,500-2,500/cell)
- Combined with element-only § 6 (200 entries) = **665 total registry entries** at Stage 3 closure

**Substrate-led discipline verification (Discipline #41 mid-stage check):**
- Cells selected for dense treatment: 15 (within dispatch 12-15 expected range)
- Cells labeled SPARSE: 11 enumerated + ~30 implied across (moderate-lineage × off-axis-element) — Cycle 15+ augmentation pipeline
- Cells labeled EMPTY: 10 enumerated + remainder of 720-cell space — element-only fallback
- Cell density imbalance reflects substrate reality: european + east_asian + middle_eastern dominate dense cells per substrate row count + thematic-canon depth, exactly as Discipline #41 predicts
- Class-vocabulary leak: zero hits in informal grep on § 7 entries (full audit at Stage 4 sign-off). Borderline "the pilgrim" (§ 7.14, § 7.15) cleared — narrative role (one-who-walks-the-pilgrim-road), not combat role. Borderline "pilgrim-stoned" (§ 7.15 epithet) annotated explicitly as scriptural-anchor not combat-token.
- `[contamination-watch]` marker retained per Stage 1 § 4 disposition: applied at § 7.16 (shadow × middle_eastern assassin-canon caution) and § 7.17 (all marginal-lineage EMPTY cells).

**Stage 3 design decisions captured:**
- Place-name and lore-fragment entries authored per dense cell per Stage 2 § 6 closure note deferral (lineage-binding required for these term-types; element-only layer was the wrong tier for them).
- Cross-element collision noted inline with `[also valid as X]` marker (single explicit case: "ember-veiled" in fire × east_asian § 7.2 and fire × middle_eastern § 7.3 — disambiguate at fire-time per cluster lineage signal).
- Within-cell cross-reference noted inline (e.g., § 7.5 "fen-born" disambiguated from § 7.6 "fen-rooted" with explicit semantic distinction water-fen vs earth-fen).
- 15 dense cells selected (within dispatch 12-15 envelope); decision-criterion: substrate row count + thematic-canon depth + element-axis coverage balance (all 8 elements have at least one dense cell except arcane and faith-holy × east_asian both pending Cycle 15+ — flagged at § 7.16 and § 7.17 respectively as augmentation candidates).
- SPARSE-cell consumption pattern documented inline (fallback to element-only + lineage-adjacent dense cell at fire-time).
- EMPTY-cell consumption pattern documented inline (fallback to element-only + meta-tag handling + `[contamination-watch]` weighting per § 4).

**Stage 3 budget:** completed within 600s envelope; no Stage-3a/3b split required.

**Next:** KR to fire Stage 4 (anti-patterns § 8 + consumption-pattern documentation § 9 + Cycle 15+ expansion path § 10 + Sign-off with Discipline #41 grep-audit + Discipline #42 framing-audit record).

**Wave 3 unblock:** still PENDING — gates on Stage 4 completion + sign-off.

---

*Stage 4 to follow: § 8 anti-patterns / § 9 consumption-pattern documentation / § 10 Cycle 15+ expansion path / § Sign-off + framing-audit + Discipline #41 grep-audit record.*
