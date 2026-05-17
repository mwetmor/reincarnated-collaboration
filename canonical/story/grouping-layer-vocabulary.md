# Grouping-Layer Vocabulary — Abstract Pair-Structure Labels

**Authority:** gandalf (story-and-design steward).
**Status:** initial vocabulary spec, 2026-05-16. Pending Matt approval at decisions-log derivation.
**Locks:** the per-substrate abstract label vocabulary that LAYER 2 (grouping layer) carries on every generated class; the labels that become LLM-VISIBLE at Stage 3 cipher migration; the design grammar that admits per-season vocabulary at Layer 3 against these slots.
**Replaces:** the PROVISIONAL illustrative scaffolding in `reincarnated-engine/src/reincarnated/generation/class_generator.py` (`_GROUPING_PAIR_STRUCTURE_LABELS`, currently `kinetic_aggression / fluid_adaptation / structural_resilience / evasive_velocity / raw_force`) and the corresponding example line in `MIGRATION.md` § "Vocabulary-spec-gap".

---

## What this doc is

The cipher-width Outcome 2 resolution (`agentic_orchestration/qa/archive/2026-05-16-decisions-log-cipher-width-resolution.md`, commit `1dff66d`) locked the **structure** of the grouping layer — single classical-element-anchored grouping; Foundation L2-decoupled; per-season vocabulary coupling β. It did not lock the **vocabulary** the grouping layer carries.

This doc locks that vocabulary.

The grouping-layer vocabulary is the set of abstract labels that sit ABOVE the canonical-four substrate (engine-internal; never LLM-visible) and BELOW per-season cosmological vocabulary (LLM-generated per season; player-facing). At Stage 2 (rocket Stage 2, shipped on `rocket/v1.3-form-bias-stage-2-grouping-layer @ 03fb8cb`), the engine emits both layers and the LLM may receive either. At Stage 3 (cipher migration; star-lord future dispatch), the canonical-four substrate hides from LLM prompts entirely and the grouping-layer labels become the LLM-visible primary vocabulary that per-season generation works against.

The vocabulary must:

1. **Preserve substrate-mechanical identity.** The Western-ARPG-genre-canonical mechanical signatures of fire / water / earth / wind / physical are 50-year-load-bearing in the genre (Diablo's fire-burn → Path of Exile's ignite; Diablo's chill → PoE's hinder; Diablo's stun → PoE's stun; Diablo's knockback → PoE's knockback; physical → bleed across all). The substrate carries these signatures *mechanically* through the engine's resistance system, archetype templates, geometry palette, and ailment grammar. The grouping label must encode the *mode of action* the substrate's mechanical signature represents so combat-feel survives when canonical-four labels hide.

2. **Sit one register higher than rename.** "Inferno" is still fire; "Tempest" is still wind. Such labels would not achieve the cipher's bias-removal job per Matt's stated intent ("blocked from view of all LLM calls so that more forms can converge/coalesce" — doc 37 § 6). The vocabulary must abstract to *kind of force*, not *element of force*. Per-season "Pressure" or "Crescendo" should fill the `ignition` slot as readily as "Combustion" does — none of those should *be* fire when the LLM reads the grouping context.

3. **Admit per-season vocabulary variation at Layer 3.** Each slot must be wide enough that the per-season vocabulary (star-lord Stage 2 dispatch territory; β coupling per cipher-width Outcome 2) can fill it for any cosmological setting the project ships — deep-sea, music-spirit, cosmic, necrotic, ghost-town, cathedral-of-bone, Yomi. The slot is the *function*; the per-season vocabulary names the *substance*.

4. **Read as ARPG-genre-legible.** Western ARPG audience reading the labels at Stage 3 should recognize *combat archetypes they know*. Per cipher-width Outcome 2's strategic-axis validation (form-bias-cadence-strategy § 5.1 sub-lock (a)): the substrate-mechanical layer stays ARPG-canon-primary. The grouping-layer labels are how the LLM-visible surface honors that sub-lock.

5. **Carry Reincarnated cosmological resonance.** The Wheel turns; descent and return; the seasonal journey; the Earth Self walks forms. The vocabulary uses verbs and modes-of-action that align with what the player is *living through* in the form, not noun-substances that fight the form-bias work.

---

## The vocabulary

| Substrate (engine-internal L1; HIDDEN from LLM at Stage 3) | Abstract grouping label (LLM-VISIBLE at Stage 3) | Mode of action |
|---|---|---|
| `fire` | `ignition` | Escalating-burst mode. Rapid energy release; area-permeating; ailment-on-contact (burn family). The mode where small inputs cascade into larger outputs over time. |
| `water` | `suffusion` | Pervading-sustain mode. State-changing presence; slows and binds without striking; ailment-by-immersion (chill family). The mode that *fills* a space rather than hitting it. |
| `earth` | `bulwark` | Anchoring-resistance mode. Positional immovability; locks targets in place; ailment-by-binding (root family). The mode of *what does not yield*. |
| `wind` | `displacement` | Directional-impulse mode. Removes targets from position; redirects momentum; ailment-by-impulse (knockback family). The mode of *what carries things elsewhere*. |
| `physical` | `impact` | Direct-strike mode. Martial momentum; dodgeable; ailment-by-wounding (bleed family). The mode of *strike-and-flow*. |

The mapping is **fixed**. Within a season, all classes share the same mapping (per the rocket Stage 2 per-season-id consistency contract). Across seasons, the mapping is also fixed (single-grouping architecture per Outcome 2). What varies across seasons is **only the per-season vocabulary at Layer 3** that fills each slot.

### Example per-season fills (illustrative, not authored — star-lord Stage 2 dispatch generates these per cosmology)

| Slot | Deep-sea season | Music-spirit season | Yomi season | Cosmic / void season | Necrotic season |
|---|---|---|---|---|---|
| `ignition` | Pressure-Release | Crescendo | Threshold-Spark | Stellar-Flare | Quickening-Rot |
| `suffusion` | Trench-Permeation | Sustained-Note | Pomegranate-Bind | Radiation-Saturation | Decay-Permeation |
| `bulwark` | Trench-Pillar | Drone-Anchor | Grave-Stillness | Gravity-Well | Petrified-Mass |
| `displacement` | Riptide | Acoustic-Wave | Threshold-Cross | Solar-Wind-Carry | Carrion-Drift |
| `impact` | Crushing-Burst | Percussion-Strike | Iron-Cudgel | Asteroid-Strike | Bone-Strike |

These are sketches showing the *register* per-season vocabulary should achieve, not authored copy. Per `naming-triad.md` § "Generation integration with the cipher architecture", the per-season vocabulary call generates the cosmology's slot-fills *plus* the Trial / Mirror / Passage variants in one coherent LLM pass against the abstract grouping vocabulary as scaffold.

---

## Pair-structure framing

Per doc 37 § 6 Position (ii) and form-bias-cadence-strategy § 6.1, the grouping layer exposes the substrate as **Primary Opposition + Secondary Opposition pairs**. The pairing of the abstract grouping labels into oppositional pairs is the load-bearing structural scaffold the LLM works against.

The pairings:

- **Primary Opposition:** `ignition` ↔ `suffusion`. The escalating-versus-pervading axis; the strike-and-burn axis versus the fill-and-bind axis. Genre-canonical fire/water opposition mapped to action-mode register.
- **Secondary Opposition:** `bulwark` ↔ `displacement`. The anchoring-versus-removing axis; the stand-firm axis versus the carry-away axis. Genre-canonical earth/wind opposition mapped to action-mode register.
- **Non-opposition (foundation):** `impact`. The direct-strike mode that does not stand in opposition to a counterpart; physical substrate is the Foundation's 1-non-rotating-element per `foundation/foundation.py:39-43`; it does not enter a pair-structure axis. It is *always available* in the season's mechanical surface as the universal martial register the Earth Self can call upon regardless of which cosmology's vocabulary is active.

Why these pairings (not arbitrary):

- The substrate's ailment grammar already encodes the oppositions. Fire's `burn` is heat-application; water's `chill` is heat-removal — opposing actions on the same physical axis (thermal). Earth's `root` is positional fixation; wind's `knockback` is positional displacement — opposing actions on the same physical axis (position). The L1 ailments are *mechanically opposed* in the engine's effect grammar.
- The doppelganger gate (gamora's mirror-validation) tests per-pair viability: a `bulwark`-coded class facing a `displacement`-coded mirror should produce a meaningfully different convergence shape than a `bulwark`-vs-`bulwark` mirror. The pair-structure is what makes the mirror-match work; misaligned pairings would break the gate's diagnostic resolution.
- The Wheel-cosmology resonance: the seasonal journey alternates between *embracing* and *resisting* what the form embodies. The Primary axis (ignition ↔ suffusion) carries the season's *active offensive* register; the Secondary axis (bulwark ↔ displacement) carries the season's *positional* register. Both axes are present in every season; per-season vocabulary names *how* the season's cosmology speaks them.

The LLM at Stage 3 receives the pair-structure framing along with the abstract labels, so per-season vocabulary generation can build coherent opposing pairs (e.g., deep-sea cosmology *naturally* opposes Pressure-Release against Trench-Permeation; both are pressure-state phenomena; the opposition is cosmologically native, not bolted on).

---

## What was considered and rejected

### Approach A — Pure verbs (`igniting / suffusing / anchoring / displacing / striking`)

Strong on action-grammar; the *-ing forms encode mode-of-action cleanly. Rejected because:

- Verb-forms read awkwardly as schema-emit field values (`grouping_pair_structure: {"fire": "igniting"}` reads stilted in code and LLM prompt context)
- Per-season vocabulary fills work better as nouns (Combustion, Pressure-Release, Crescendo are noun phrases); the abstract slot should be a noun the season's vocabulary lives inside
- Verb-forms invite the LLM to over-narrate the action where the slot wants a *category*

### Approach B — Mythic-elemental abstractions (`kindling / suffusion / foundation / motion / striking`)

Tried because the mythic register matches Reincarnated's cosmology (Wheel, Court, Passage, Mirror, Trial). Rejected because:

- `kindling` reads as still-fire (kindling = early fire; not abstraction above fire)
- `foundation` collides with the Foundation L1 system name (`reincarnated-engine/src/reincarnated/foundation/foundation.py`); cross-vocabulary confusion guaranteed
- `motion` is too broad; loses the *knockback/displacement* mechanical specificity
- `striking` is acceptable but `impact` reads cleaner in ARPG genre vocabulary

### Approach C — Force-grammar compounds (`kinetic_aggression / fluid_adaptation / structural_resilience / evasive_velocity / raw_force`)

The PROVISIONAL scaffolding rocket used at Stage 2. Rejected as the locked vocabulary because:

- Two-word compounds are heavy in code, LLM prompts, and decisions-log entries
- The `_aggression / _adaptation / _resilience / _velocity` suffixes import *character-trait* register that pulls toward archetype-coded humanoid framing (the very form-bias the cipher migration is removing per doc 37 § 1 + Cluster B framing in form-bias-cadence-strategy § 2.1)
- `raw_force` for physical is genuinely weak — physical is not "raw" anything; it is the *specifically-martial* register the genre canonically names *physical / impact*
- The compounds blur the substrate-mechanical-identity preservation (criterion 1 above) because *aggression* applies to any offensive mode, not specifically to the escalating-burst signature fire carries

The provisional scaffolding was correct as a *placeholder* — clearly flagged in code as scaffolding-only, structurally complete enough that rocket's Stage 2 infrastructure work could ship. The replacement vocabulary in this spec is what Stage 3 cipher migration will use.

### Approach D — Genre-direct synonyms (`burst / drown / root / push / strike`)

Plain-English what-the-substrate-does. Rejected because:

- Reads as Last-Epoch-style mechanical-label register; loses the cosmological abstraction Reincarnated's cipher architecture requires
- `drown` carries water-substance bleed through; not an abstraction
- `push` is the wrong granularity for wind's full mechanical surface (wind is knockback + projectile-deflection + speed-confer + evasive-positioning; "push" captures only one)
- Per-season vocabulary cannot meaningfully *fill* slots this concrete; the slots ARE the substance already

### Approach E — Symbolic / archaic register (`pyre / lave / megalith / zephyr / hewing`)

Considered for mythic weight. Rejected because:

- `pyre` and `zephyr` are transparent renames; do not achieve cipher-bias removal
- `lave` is archaic to the point of obscurity; doesn't read as legible ARPG vocabulary
- `megalith` is a *thing*, not a mode; collides with the action-mode framing
- The register doesn't survive translation into per-season cosmologies (Yomi's *bulwark* fills naturally to Grave-Stillness; Yomi's *megalith* fills awkwardly to Grave-Megalith)

---

## Genre / design implications

The vocabulary becomes genre-facing at Stage 3. The implications:

**ARPG positioning.** The labels read as combat-mode taxonomy: ignition / suffusion / bulwark / displacement / impact. A Path-of-Exile player encountering "the Primary Opposition between ignition and suffusion" reads the burst-DoT-versus-control-chill axis they already know. A Diablo IV player reads the same. The vocabulary does not break ARPG legibility; it abstracts above the genre's specific element-vocabulary by one register, which is the cipher architecture's whole job.

**Isekai positioning.** The labels read as cosmological-grammar abstractions: the *kind of force* a world's cosmology embodies. A Mushoku-Tensei-reader audience encountering the labels alongside per-season cosmologies (deep-sea's Pressure-Release; Yomi's Threshold-Spark) reads the system-narrative the genre canonically expects — the world has its own mechanical grammar; the system *describes* it; the player learns *the world's terms* as they descend into the form. The labels do the cipher's work of giving the LLM-generated per-season vocabulary a mechanical-coherent scaffold without leaking Earth-realm fire/water/earth/wind register.

**Reincarnated cosmological positioning.** The Wheel turns; the Earth Self descends into a form; the form has *its mode of action* in the season's world. The labels name that mode at the abstraction layer the Wheel itself works at — modes, not substances. The Spirit Guide (Beatrice register; foresight without memory) speaks the per-season vocabulary in dialogue; the engine and the design docs speak the grouping-layer labels structurally; the player learns *both* across seasons as the Court accumulates and the form-library grows.

**Doppelganger-gate implications (gamora cascade).** Position (ii)'s mechanical-signature variety across per-season vocabulary becomes diagnosable against fixed grouping-layer slots. A pure-control-coded `bulwark` per-season vocabulary that breaks the doppelganger gate empirically (per form-bias-cadence-strategy § 6.3's WARN-1 amendment) surfaces as a *grouping-layer-coupled* finding (bulwark slot under-damaging), not a substrate-coupled finding. This sharpens gamora's gate-diagnostic resolution.

**Discipline #14 implications.** The grouping-layer vocabulary IS the answer to Discipline #14 candidate enforcement at Stage 3. Every LLM prompt-construction site that today exposes canonical-four labels (`naming.py:32-35`, `selector.py:43-47`, `library_generator.py:85` per form-bias-cadence-strategy § 1.1 Cluster E) replaces those labels with the grouping-layer abstract labels + per-season vocabulary fills. The discipline becomes mechanically enforceable: any prompt-construction code path that emits `"fire"` / `"water"` / `"earth"` / `"wind"` to an LLM is a discipline violation by inspection.

**Star-lord Stage 2 dispatch implications.** Star-lord's per-season cosmological-vocabulary generation prompt receives the grouping-layer vocabulary as the scaffold. The prompt asks the LLM to generate per-season vocabulary at each grouping-layer slot, in coherent opposing pairs per the Primary / Secondary opposition framing above, against the season's anchor + cosmology + Spirit-Guide voice. The cipher-width Outcome 2 β coupling (in-prompt constraint) lands as: *the prompt names the five slots and the two pair axes; the LLM generates per-season vocabulary that fills each slot with cosmological coherence; engine consumes the structured output downstream*.

**Stage 3 cipher migration implications.** The migration replaces every prompt-construction site's canonical-four exposure with grouping-layer-plus-per-season-vocabulary exposure. After Stage 3, the LLM never sees `fire`/`water`/`earth`/`wind`; it sees `ignition`/`suffusion`/`bulwark`/`displacement`/`impact` as the abstract scaffold and the season's vocabulary as the concrete fills. Experiment 1 (no-seed cosmology generation test; `agentic_orchestration/gandalf/requests/2026-05-16-no-seed-cosmology-generation-test.md`) runs at the Stage 3 gate to confirm residual-bias removal; the grouping-layer vocabulary is the test's positive-control scaffold.

---

## Per-element rationale (the long-form *why* each label was chosen)

### `fire` → `ignition`

The fire substrate carries the ARPG-genre-canonical *escalating-burst* mechanical signature: rapid energy release, area-permeating, ailment-on-contact (burn DoT). Across Diablo II's Fireball / Fire Wall / Hydra, Diablo IV's Sorcerer Pyromancy tree, Path of Exile's Fire damage + Ignite ailment, Last Epoch's Fire spells, the through-line is *small spark → large consequence over time*. The burn DoT is mechanically distinctive precisely because it is *the thing that grows after you've delivered it*.

`ignition` names that mode without naming fire. Per-season fills:
- Deep-sea: Pressure-Release (built-up pressure releases catastrophically; mechanical analog = ignition-burst)
- Music-spirit: Crescendo (built-up volume releases catastrophically)
- Yomi: Threshold-Spark (the moment of crossing the threshold catalyzes transformation)
- Cosmic: Stellar-Flare (solar surface ignition)
- Necrotic: Quickening-Rot (decay accelerates exponentially once seeded)

The label preserves the substrate's mechanical identity (burst-DoT-cascade) while admitting any cosmology's substance to fill it.

### `water` → `suffusion`

The water substrate carries the *pervading-sustain* mechanical signature: state-changing presence, slows and binds without striking, ailment-by-immersion (chill). Diablo II's Frozen Orb / Ice Blast, Diablo IV's Sorcerer Cryomancy tree, Path of Exile's Cold damage + Chill ailment, Last Epoch's Cold spells — the through-line is *the thing that fills space and changes what's in it*. Chill mechanically slows; cold-snap mechanically freezes; both share the *presence-not-strike* register.

`suffusion` names that mode without naming water. To suffuse is to spread through and permeate. Per-season fills:
- Deep-sea: Trench-Permeation (water suffuses everything)
- Music-spirit: Sustained-Note (a held note fills the space)
- Yomi: Pomegranate-Bind (the food of Yomi suffuses the eater; Izanami myth)
- Cosmic: Radiation-Saturation (cosmic radiation permeates without striking)
- Necrotic: Decay-Permeation (rot suffuses tissue)

The label preserves the substrate's mechanical identity (slow-and-bind-by-presence) while admitting any cosmology's substance.

### `earth` → `bulwark`

The earth substrate carries the *anchoring-resistance* mechanical signature: positional immovability, locks targets in place, ailment-by-binding (root). Diablo II's Earthquake / Volcano, Diablo IV's Druid Earth tree, Path of Exile's Earth-themed skills + their stun-and-stand-firm register, Last Epoch's Primalist Earth tree — the through-line is *what does not yield*. Root binds the target's position; the player's earth-coded class is the one that holds ground.

`bulwark` names that mode. A bulwark is a defensive earthwork; the etymology carries the *standing-firm* register the substrate embodies. Per-season fills:
- Deep-sea: Trench-Pillar (the deep-sea floor's columns of compressed sediment)
- Music-spirit: Drone-Anchor (the sustained-low-note that holds the harmonic structure together)
- Yomi: Grave-Stillness (the dead do not move; Yomi's mechanic IS stillness)
- Cosmic: Gravity-Well (mass that holds everything around it in orbit)
- Necrotic: Petrified-Mass (rot stabilized into stone)

The label preserves the substrate's mechanical identity (positional-fixation; immovability) while admitting any cosmology's substance. The slight noun-concreteness of `bulwark` (versus pure verb-form) is intentional — earth is the most *thing-like* substrate; its label honors that without slipping into Earth-realm rock register.

The avoided alternative `anchoring` was rejected because the term "anchor" is heavily overloaded in the project (seasonal anchors per cosmology-reincarnated.md; kit-anchor per rocket dispatches; Pimen anchor types). Cross-vocabulary confusion would be guaranteed.

### `wind` → `displacement`

The wind substrate carries the *directional-impulse* mechanical signature: removes targets from position, redirects momentum, ailment-by-impulse (knockback). Diablo II's Tornado / Cyclone Armor, Diablo IV's Druid Storm tree, Path of Exile's Lightning + Shock ailment (the genre's closest ranged-displacement analog where wind itself is sparse), Last Epoch's wind/storm tree — the through-line is *what moves things from where they were to somewhere else*.

`displacement` names that mode directly. Per-season fills:
- Deep-sea: Riptide (the current that pulls swimmers from their position)
- Music-spirit: Acoustic-Wave (the pressure wave that physically shifts what it strikes)
- Yomi: Threshold-Cross (the act of crossing the underworld threshold)
- Cosmic: Solar-Wind-Carry (the cosmic-scale wind that carries objects across distance)
- Necrotic: Carrion-Drift (the wind that carries decay between bodies)

The label preserves the substrate's mechanical identity (knockback/redirection/positional-removal) while admitting any cosmology's substance.

The avoided alternative `vector` was rejected for technical-math-register bleed; physics-classroom register reads colder than the cipher-architecture's mythic-cosmological context calls for.

### `physical` → `impact`

The physical substrate carries the *direct-strike* mechanical signature: martial momentum, dodgeable, ailment-by-wounding (bleed). Across all ARPGs the physical damage type is the *baseline* the elements are differentiated against. Bleed is mechanically distinctive as the ailment of direct-injury; armor (not percentage resistance) is its mitigation mode (per `foundation/foundation.py` and `config/elements.yaml`).

`impact` names that mode in ARPG-genre-canonical register. The genre routinely calls physical damage "impact damage" already; the label does not require the LLM or the player to learn anything new for the physical slot. Per-season fills:
- Deep-sea: Crushing-Burst (deep-sea-pressure-direct-impact)
- Music-spirit: Percussion-Strike (the drumbeat that physically strikes)
- Yomi: Iron-Cudgel (the underworld's martial register)
- Cosmic: Asteroid-Strike (mass colliding with mass)
- Necrotic: Bone-Strike (the necrotic-warrior's martial register)

The label preserves the substrate's mechanical identity (direct-strike; armor-mitigated; bleed-ailment) while admitting any cosmology's substance.

Per the pair-structure framing above, `impact` does NOT enter the Primary or Secondary opposition. Physical is the Foundation's 1-non-rotating element; it is universally available in every season as the martial register. The pair-structure is the *rotating* opposition the season's vocabulary works around; impact is the *constant* the season's vocabulary works with.

---

## Implementation handoff

### For rocket (small follow-on dispatch, knight-rider will route)

Update `reincarnated-engine/src/reincarnated/generation/class_generator.py`:

```python
_GROUPING_PAIR_STRUCTURE_LABELS: dict[str, str] = {
    "fire":     "ignition",
    "water":    "suffusion",
    "earth":    "bulwark",
    "wind":     "displacement",
    "physical": "impact",
}

GROUPING_LAYER_VERSION = "v1.1"
```

Update the docblock above `_GROUPING_PAIR_STRUCTURE_LABELS` to remove the `*** PROVISIONAL — PENDING GANDALF VOCABULARY SPECIFICATION ***` warning; replace with `# Locked per canonical/story/grouping-layer-vocabulary.md (gandalf, 2026-05-16)`. Cross-reference this doc + decisions-log entry (once derived). Add MIGRATION.md § "Vocabulary update v1.0 → v1.1" entry. Notify star-lord and drax via knight-rider dispatch.

The Stage 2 schema/infrastructure work is unchanged. Only the label string values change.

### For star-lord (Stage 2 dispatch, queued)

Per-season cosmological-vocabulary generation prompts consume the grouping-layer vocabulary as the scaffold per cipher-width Outcome 2 β coupling. The prompt structure:

- Anchor + anchor description (per naming-triad.md § "Generation integration with the cipher architecture")
- The five abstract slots (ignition / suffusion / bulwark / displacement / impact) with brief mode-of-action descriptions (per the table above)
- The Primary / Secondary opposition framing (ignition ↔ suffusion as Primary; bulwark ↔ displacement as Secondary; impact as non-pair foundation)
- The cosmology's narrative seed
- Explicit guidance: *"Generate per-season vocabulary that fills each slot with the season's cosmology. The Primary pair should oppose coherently within the cosmology's terms; the Secondary pair the same. The Foundation slot (impact) should name the season's martial register. The vocabulary should evoke the cosmology; it should not translate the abstract labels literally."*
- Anti-bias scaffolding (Discipline #14 candidate; do NOT expose canonical-four labels in the prompt)

The prompt is one coherent cosmological-vocabulary call per season per naming-triad.md § "Generation integration with the cipher architecture" — it generates the slot-fills *plus* the Trial / Mirror / Passage variants in one pass.

### For Stage 3 cipher migration (separate future dispatch)

The grouping-layer vocabulary REPLACES canonical-four labels in every LLM prompt-construction site identified in form-bias-cadence-strategy § 1.1 Cluster E:

- `naming.py:26-36`, `naming.py:87`, `naming.py:89`
- `selector.py:43-47`, `selector.py:394-446`
- `library_generator.py:85`

Each site emits the grouping-layer abstract labels + the season's per-season vocabulary fills, NOT the canonical-four labels. Experiment 1 runs at this stage's gate to confirm residual-bias removal.

### For gamora (Stage 2-3 doppelganger validation)

The doppelganger gate's per-pair viability check (per form-bias-cadence-strategy § 9.3 gamora cascade) operates against the grouping-layer pair-structure: Primary axis (ignition ↔ suffusion) mirror-matches; Secondary axis (bulwark ↔ displacement) mirror-matches; impact mirror-matches as the non-pair direct-strike register. The gate's diagnostic resolution can now attribute pair-coupled findings (e.g., bulwark slot under-damaging across multiple seasons) to the grouping-layer, not the substrate.

### For drax (Stage 4 display work)

The player-facing surface (per form-bias-cadence-strategy § 9.4 drax cascade) renders the per-season vocabulary at Layer 3, with the grouping-layer abstract labels available as *operational helper-text* in the same dual-surface pattern naming-triad.md § "Where BOTH surface together" specifies. Example:

```
THE SOUNDING                                  ← per-season vocabulary (Layer 3)
(the season's ignition)                       ← grouping-layer label (Layer 2) as helper

You channel the deep-sea pressure-release.    ← per-season vocabulary in flavor text
```

The pattern matches the Trial / Mirror / Passage surfacing pattern from naming-triad.md; the helper-text gives operational clarity without breaking cosmological immersion.

---

## Open questions (not blocking; queued)

### Q1 — Pair-structure label exposure shape

Doc 37 § 6.5 flags as needing prototyping: *"Does the LLM see both pairs simultaneously (and generate four axes at once), or one pair at a time (independently)?"* This spec defaults to **simultaneous exposure** — the LLM sees both Primary and Secondary opposition framings in the same prompt and generates coherent per-season vocabulary across both pairs in one pass per the naming-triad.md § 75 one-call-per-season pattern. Star-lord's Stage 2 prompt design should validate this default; if cross-pair interactions surface in early Stage-2 generation findings, the simultaneous-exposure default may need to be revisited.

### Q2 — Vocabulary stability across the season

Per naming-triad.md Open Question Q2 (variant stability): the per-season vocabulary is generated *once* per season and remains stable for that season's duration. The grouping-layer vocabulary in THIS spec is locked across all seasons; only the per-season Layer-3 fills vary. No stability question at the grouping layer.

### Q3 — Player-naming of grouping-layer labels

Per naming-triad.md Open Question Q3 (player-naming of variants): the grouping-layer labels are engine-spoken vocabulary, NOT player-facing in the way per-season Layer-3 vocabulary is. Players see the per-season vocabulary; they see the grouping-layer labels only in operational helper-text (per drax handoff above). No player-naming question at the grouping layer.

### Q4 — Future cipher-width expansion (Outcome 1 re-opening)

Per cipher-width Outcome 2's re-opening trigger framework: if a future Tier-2 catalogue crawl raises per-novel-substrate n above 3 and Matt elects to invest in substrate expansion, the grouping-layer vocabulary may need to extend to additional slots. The current 5-label vocabulary fits the Foundation 4-rotating-plus-1-physical structure exactly; an Outcome-1-re-opening would require additional labels at the same abstraction register. Reserved labels for future consideration (NOT locked; surfaced for record): `dissolution` (for blood/necrotic/dissolution-of-form mode), `transmutation` (for midas/alchemy/state-change mode), `severance` (for shadow/void/removal-of-being mode), `convergence` (for crystal/cosmic/aggregation mode). These are sketches showing the register the label space admits; concrete adoption awaits the cipher-width re-opening trigger conditions.

### Q5 — Demo2 / Earth-meta-layer implications

Demo2 (post-Phase-0) and the Earth-meta-layer's Court / Spirit Guide / Earth-Self hub surfaces may render the grouping-layer vocabulary in cross-season aggregation surfaces (e.g., a Court entry might be tagged *"the Tidecaller — `suffusion`-coded"* as a cross-season form-archetype reference). This is post-Phase-0 territory; surfaced for future reference, not Phase-0 scope.

---

## Cross-references

- **Cipher-width Outcome 2 resolution:** `agentic_orchestration/qa/archive/2026-05-16-decisions-log-cipher-width-resolution.md` (commit `1dff66d`)
- **Strategy doc — grouping layer framing:** `canonical/story/form-bias-cadence-strategy.md` § 6.1 (three-layer model); § 6.2 (cipher-width framework); § 6.3 (cipher architecture stays operative); § 7.1 Stage 2 (abstract pair-structure added alongside canonical-four)
- **Original cipher architecture:** `canonical/37-form-bias-diagnosis-and-recovery.md` § 6 (canonical-four element cipher; Position (ii) lock)
- **Naming triad integration:** `canonical/story/naming-triad.md` § "Per-season vocabulary variation" (the one-call-per-season pattern that consumes this vocabulary)
- **Engine-generic meta-structure:** `canonical/story/engine-generic-meta-structure.md` § "What's at the L1 engine substrate layer" + § "Architectural patterns" (cipher architecture as licensable pattern)
- **Cosmology framing:** `canonical/story/cosmology-reincarnated.md` (the Wheel, the Earth Self, the Spirit Guide, the seasonal journey — the cosmological frame this vocabulary serves)
- **Rocket Stage 2 dispatch (the originating context):** `agentic_orchestration/dispatches/2026-05-16-rocket-form-bias-stage-2-grouping-layer.md` (the dispatch that surfaced the vocabulary-spec-gap)
- **Rocket Stage 2 implementation:** `reincarnated-engine/src/reincarnated/generation/class_generator.py:153-182`; `reincarnated-engine/src/reincarnated/generation/MIGRATION.md` § "Vocabulary-spec-gap" (the placeholder this spec replaces)
- **Star-lord Stage 2 sister dispatch (queued):** per-season cosmological-vocabulary generation consuming this vocabulary
- **Foundation L1 substrate definitions:** `reincarnated-engine/config/elements.yaml`; `reincarnated-engine/src/reincarnated/foundation/foundation.py` (the canonical-four-plus-physical that this vocabulary's keys correspond to)
- **Genre-canon grounding:** `canonical/story/gandalf-design-lineage.md` + Legolas Pass 4 ARPG-community-discourse findings (the ARPG-canon legibility constraints that shaped vocabulary criterion 4)

---

## Maintenance protocol

This doc is the authoritative source for the grouping-layer vocabulary. Changes require:

1. Gandalf authorship of the change (Pattern A or Pattern B per gandalf operating manual)
2. Knight-rider sequencing into decisions-log entry
3. Jack-ryan Gate 1 review
4. Matt approval
5. Rocket bump of `GROUPING_LAYER_VERSION` per Discipline #12 (schema-semantic shift coordination)
6. MIGRATION.md entry per ADR-004
7. Star-lord prompt-template update (Stage 2+)

The vocabulary is **not** lightly revisable. The substrate-mechanical-identity preservation criterion (criterion 1 above) means changing a slot's label changes the LLM's interpretive frame for every per-season vocabulary generated against it; downstream regeneration of per-season content may be needed. Future changes should be scoped against that re-generation cost.

The re-opening trigger framework from cipher-width Outcome 2 is the *expected* future maintenance event: if Tier-2 catalogue crawl + Matt's substrate-expansion call lands, additional slots are added at the same abstraction register per Q4 above. This is the scoped, anticipated extension; other changes are unscoped.
