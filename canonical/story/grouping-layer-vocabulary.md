# Grouping-Layer Vocabulary — Abstract Pair-Structure Labels

**Authority:** gandalf (story-and-design steward).
**Status:** **canonical-7 vocabulary** as of 2026-05-17 Phase-1 P1 Deliverable 20 extension. Original 5-slot canonical-four vocabulary locked 2026-05-16; canonical-7 extension (resonance / radiance / penumbra; pair-structure shape 2-2-2-1-1) authored 2026-05-17 by gandalf as D20 under hive-mind mode. Pending Matt approval at decisions-log derivation (D23 — substrate-expansion decisions-log entry covers).
**Version:** `v1.2` (canonical-7 extension; was v1.1 canonical-four-only at 2026-05-16 lock).
**Locks:** the per-substrate abstract label vocabulary that LAYER 2 (grouping layer) carries on every generated class; the labels that become LLM-VISIBLE at Stage 3 cipher migration; the design grammar that admits per-season vocabulary at Layer 3 against these slots; the pair-structure shape that the registry-driven LLM prompt structure (per star-lord D6 refactor) consumes.
**Replaces:** the PROVISIONAL illustrative scaffolding in `reincarnated-engine/src/reincarnated/generation/class_generator.py` (`_GROUPING_PAIR_STRUCTURE_LABELS`, originally `kinetic_aggression / fluid_adaptation / structural_resilience / evasive_velocity / raw_force`) and the corresponding example line in `MIGRATION.md` § "Vocabulary-spec-gap". Also replaces the hardcoded 2-2-1 pair-structure constants in `reincarnated-engine/src/reincarnated/llm/cosmological_vocabulary.py:63-75` (`GROUPING_SLOTS` / `_PRIMARY_PAIR` / `_SECONDARY_PAIR` / `_FOUNDATION_SLOT`) per the registry-driven refactor star-lord D6 implements.

---

## What this doc is

The cipher-width Outcome 2 resolution (`agentic_orchestration/qa/archive/2026-05-16-decisions-log-cipher-width-resolution.md`, commit `1dff66d`) locked the **structure** of the grouping layer — single classical-element-anchored grouping; Foundation L2-decoupled; per-season vocabulary coupling β. It did not lock the **vocabulary** the grouping layer carries.

This doc locks that vocabulary.

The grouping-layer vocabulary is the set of abstract labels that sit ABOVE the engine-internal substrate set (canonical-four originally; **canonical-7 as of v1.2 per substrate-expansion-decision-2026-05-17**; never LLM-visible) and BELOW per-season cosmological vocabulary (LLM-generated per season; player-facing). At Stage 2 (rocket Stage 2, shipped on `rocket/v1.3-form-bias-stage-2-grouping-layer @ 03fb8cb`), the engine emits both layers and the LLM may receive either. At Stage 3 (cipher migration; subsumed under Phase-1 P1 Deliverable 6 — star-lord LLM-prompt structure refactor), the substrate hides from LLM prompts entirely and the grouping-layer labels become the LLM-visible primary vocabulary that per-season generation works against.

**v1.2 amendment scope:** the canonical-7 substrate expansion adds three new substrates (lightning / holy / shadow) per substrate-expansion-decision Branch A. This doc's v1.2 extension authors three new L2 grouping labels (`resonance` / `radiance` / `penumbra`) at the same abstraction register as the canonical-four labels, adds a third pair-axis (luminance: radiance ↔ penumbra) to the pair-structure framing, treats lightning as unpaired-rotating, and introduces the machine-extractable structured section that makes pair-structure data-driven (closing the wide-net § 2.3 critical-surprise — pair-structure was previously wired into the LLM prompt template as Python constants).

The vocabulary must:

1. **Preserve substrate-mechanical identity.** The Western-ARPG-genre-canonical mechanical signatures of fire / water / earth / wind / **lightning / holy / shadow** / physical are 50-year-load-bearing in the genre (Diablo's fire-burn → Path of Exile's ignite; Diablo's chill → PoE's hinder; Diablo's stun → PoE's stun; Diablo's knockback → PoE's knockback; Diablo's lightning-chain → PoE's chain-shock; Diablo Paladin holy-aura → D4 Necromancer vs holy-encounters; D2 Necromancer shadow-tree → Solo Leveling Shadow Army; physical → bleed across all). The substrate carries these signatures *mechanically* through the engine's resistance system, archetype templates, geometry palette, and ailment grammar. The grouping label must encode the *mode of action* the substrate's mechanical signature represents so combat-feel survives when substrate labels hide.

2. **Sit one register higher than rename.** "Inferno" is still fire; "Tempest" is still wind; "Stormcaller" is still lightning; "Lightbringer" is still holy; "Nightblade" is still shadow. Such labels would not achieve the cipher's bias-removal job per Matt's stated intent ("blocked from view of all LLM calls so that more forms can converge/coalesce" — doc 37 § 6). The vocabulary must abstract to *kind of force*, not *element of force*. Per-season "Pressure" or "Crescendo" should fill the `ignition` slot as readily as "Combustion" does — none of those should *be* fire when the LLM reads the grouping context. Per-season "Sonar-Cascade" should fill `resonance` without the LLM reading "lightning" or "thunder".

3. **Admit per-season vocabulary variation at Layer 3.** Each slot must be wide enough that the per-season vocabulary (star-lord Stage 2 dispatch territory; β coupling per cipher-width Outcome 2) can fill it for any cosmological setting the project ships — deep-sea, music-spirit, cosmic, necrotic, ghost-town, cathedral-of-bone, Yomi. The slot is the *function*; the per-season vocabulary names the *substance*. The v1.2 luminance pair (radiance ↔ penumbra) must admit per-season opposition framings (deep-sea Bioluminescent-Bloom vs Abyssal-Veil; cosmic Solar-Sanctum vs Eclipse-Shadow) without forcing the LLM to translate "holy" or "shadow" into the cosmology's own terms.

4. **Read as ARPG-genre-legible.** Western ARPG audience reading the labels at Stage 3 should recognize *combat archetypes they know*. Per cipher-width Outcome 2's strategic-axis validation (form-bias-cadence-strategy § 5.1 sub-lock (a)): the substrate-mechanical layer stays ARPG-canon-primary. The grouping-layer labels are how the LLM-visible surface honors that sub-lock. `radiance` reads as paladin-aura-register; `penumbra` reads as shadow-stalker-register; `resonance` reads as lightning-chain-register. All three are within ARPG-genre vocabulary surface; none parse as alien.

5. **Carry Reincarnated cosmological resonance.** The Wheel turns; descent and return; the seasonal journey; the Earth Self walks forms; the Court of Forms accumulates ascended forms. The vocabulary uses verbs and modes-of-action that align with what the player is *living through* in the form, not noun-substances that fight the form-bias work. The v1.2 luminance pair specifically honors the cosmology's already-active light/dark grammar: Ascension is holy-coded; Passage is shadow-coded; the Court remembers both. The grouping vocab v1.2 makes this Layer-2-explicit (was Discipline-#13 implicit-pillar drift per substrate-expansion-decision § 4.1).

---

## The vocabulary

| Substrate (engine-internal L1; HIDDEN from LLM at Stage 3) | Abstract grouping label (LLM-VISIBLE at Stage 3) | Mode of action | Status |
|---|---|---|---|
| `fire` | `ignition` | Escalating-burst mode. Rapid energy release; area-permeating; ailment-on-contact (burn family). The mode where small inputs cascade into larger outputs over time. | locked 2026-05-16 |
| `water` | `suffusion` | Pervading-sustain mode. State-changing presence; slows and binds without striking; ailment-by-immersion (chill family). The mode that *fills* a space rather than hitting it. | locked 2026-05-16 |
| `earth` | `bulwark` | Anchoring-resistance mode. Positional immovability; locks targets in place; ailment-by-binding (root family). The mode of *what does not yield*. | locked 2026-05-16 |
| `wind` | `displacement` | Directional-impulse mode. Removes targets from position; redirects momentum; ailment-by-impulse (knockback family). The mode of *what carries things elsewhere*. | locked 2026-05-16 |
| `lightning` | `resonance` | Sudden-traversal mode. Chains across targets; arcs without crossing the space between; ailment-by-arc-paralysis (shock family). The mode of *what ends what was about to happen by being faster than it could happen*. | **added 2026-05-17 (D20)** |
| `holy` | `radiance` | Revelation-and-amplification mode. Consecrates ground; amplifies allies; valenced-ailment (consecrate family — beneficial to aligned, harmful to opposed). The mode of *what cannot abide concealment and lifts what is aligned with it*. | **added 2026-05-17 (D20)** |
| `shadow` | `penumbra` | Concealment-and-drain mode. Withdraws presence and resource; occludes perception; ailment-by-withdrawal (drain family). The mode of *what is taken without striking and arrives without warning*. | **added 2026-05-17 (D20)** |
| `physical` | `impact` | Direct-strike mode. Martial momentum; dodgeable; ailment-by-wounding (bleed family). The mode of *strike-and-flow*. | locked 2026-05-16 (foundation; non-rotating) |

The mapping is **fixed**. Within a season, all classes share the same mapping (per the rocket Stage 2 per-season-id consistency contract). Across seasons, the mapping is also fixed (single-grouping architecture per Outcome 2). What varies across seasons is **only the per-season vocabulary at Layer 3** that fills each slot.

**Vocabulary cardinality (v1.2):** 8 labels total — 7 substrate-mapped (4 canonical rotating + 1 unpaired-rotating lightning + 2 luminance-paired) + 1 foundation (impact / physical-as-modifier; non-rotating; always available). Note that `physical` is NOT one of the canonical-7 substrates (per `substrate-expansion-decision-2026-05-17.md` § 2.2: physical remains a damage-type-modifier available to all substrates, not a substrate itself). The 7 canonical substrates are `fire / water / earth / wind / lightning / holy / shadow`. Impact stays in the grouping vocabulary as the universal martial register because physical damage is *available* in every season's mechanical surface — it just isn't *a substrate slot* generation samples from.

### Example per-season fills (illustrative, not authored — star-lord Stage 2 dispatch generates these per cosmology)

| Slot | Deep-sea season | Music-spirit season | Yomi season | Cosmic / void season | Necrotic season |
|---|---|---|---|---|---|
| `ignition` | Pressure-Release | Crescendo | Threshold-Spark | Stellar-Flare | Quickening-Rot |
| `suffusion` | Trench-Permeation | Sustained-Note | Pomegranate-Bind | Radiation-Saturation | Decay-Permeation |
| `bulwark` | Trench-Pillar | Drone-Anchor | Grave-Stillness | Gravity-Well | Petrified-Mass |
| `displacement` | Riptide | Acoustic-Wave | Threshold-Cross | Solar-Wind-Carry | Carrion-Drift |
| `resonance` | Sonar-Cascade | Harmonic-Chain | Bell-Toll-Bind | Pulsar-Arc | Death-Knell-Ring |
| `radiance` | Bioluminescent-Bloom | Tonic-Major-Chord | Sun-At-Western-Gate | Solar-Sanctum | Sanctified-Ash |
| `penumbra` | Abyssal-Veil | Sub-Audible-Hum | Kuroyami-Shroud | Eclipse-Shadow | Crypt-Damp |
| `impact` | Crushing-Burst | Percussion-Strike | Iron-Cudgel | Asteroid-Strike | Bone-Strike |

These are sketches showing the *register* per-season vocabulary should achieve, not authored copy. Per `naming-triad.md` § "Generation integration with the cipher architecture", the per-season vocabulary call generates the cosmology's slot-fills *plus* the Trial / Mirror / Passage variants in one coherent LLM pass against the abstract grouping vocabulary as scaffold.

Note that with the canonical-7 extension, the per-season LLM call now generates **8 slot fills** (was 5) plus rationale fields for **3 pair axes** (was 2). Star-lord D6 implementation considerations:
- One LLM call per season is preserved; output schema grows by 3 fields.
- Token estimate per call grows by ~30-40% (~600-700 input / ~300-450 output; still negligible vs full regen).
- The `radiance` ↔ `penumbra` luminance pair should generate with **valenced cosmological framing** (luminance opposition is the most strongly axiomatic of the three pairs — the cosmology's own light/dark grammar should surface in the rationale).

---

## Pair-structure framing

Per doc 37 § 6 Position (ii) and form-bias-cadence-strategy § 6.1, the grouping layer exposes the substrate as **a structured set of Opposition pairs plus Unpaired modes**. The pairing of the abstract grouping labels into oppositional pairs is the load-bearing structural scaffold the LLM works against.

### v1.2 canonical-7 shape: 2-2-2-1-1

The canonical-7 expansion (substrate-expansion-decision-2026-05-17) introduces three new substrates: `lightning` / `holy` / `shadow`. The locked pair-structure shape post-extension is **2-2-2-1-1**:

- **Primary Opposition (canonical-four axis):** `ignition` ↔ `suffusion`. The escalating-versus-pervading axis; the strike-and-burn axis versus the fill-and-bind axis. Genre-canonical fire/water opposition mapped to action-mode register. **Axis: `thermal`** (intent register: heat-application vs heat-removal as opposing actions on the same physical axis).
- **Secondary Opposition (canonical-four axis):** `bulwark` ↔ `displacement`. The anchoring-versus-removing axis; the stand-firm axis versus the carry-away axis. Genre-canonical earth/wind opposition mapped to action-mode register. **Axis: `position`** (intent register: positional fixation vs positional removal as opposing actions on the same physical axis).
- **Tertiary Opposition (luminance axis; NEW v1.2):** `radiance` ↔ `penumbra`. The reveal-and-amplify-versus-withdraw-and-conceal axis; the lift-the-aligned axis versus the take-without-striking axis. Genre-canonical holy/shadow opposition (D2 Paladin vs Necromancer; D4 Necromancer vs angelic-encounters; Solo Leveling Light vs Shadow Army). **Axis: `luminance`** (per substrate-expansion-decision § 3.2 — paired-luminance with valenced resistance per § 5.1: +25% damage on opposed-luminance match; -25% on same-luminance match). The luminance axis is **the cosmology's grammar of choice-at-season-end** (per substrate-expansion-decision § 4.1: holy is the substrate of the *ascension moment*; shadow is the substrate of the *Passage*).
- **Unpaired-rotating (NEW v1.2):** `resonance`. Lightning substrate. Unpaired by genre convention — Diablo, PoE, Last Epoch, Grim Dawn all treat lightning as its own thing rather than opposed to a specific substrate (per substrate-identity-declarations § 5: "Lightning is **unpaired** by genre convention. Treating it as paired would require inventing a substrate; that's not in scope."). Lightning enters the season's class rotation alongside the canonical-four and the luminance pair, but does NOT have a resistance-valence opposite; resistance matrix treats lightning symmetrically (1.0× across the board per substrate-expansion-decision § 5.1). **Axis: none.**
- **Non-rotating foundation:** `impact`. The direct-strike mode that does not stand in opposition to a counterpart; physical is the Foundation's 1-non-rotating-element per `foundation/foundation.py:39-43`; it does not enter a pair-structure axis. It is *always available* in the season's mechanical surface as the universal martial register the Earth Self can call upon regardless of which cosmology's vocabulary is active. **Axis: none.**

**Why this shape, not 2-2-1 + 3 unpaired:**

Three structural reasons preferred 2-2-2-1-1 over the alternative of treating lightning/holy/shadow all as unpaired add-ons to the original 2-2-1:

1. **Holy ↔ shadow are mechanically paired in the substrate identity declarations.** Each has the other listed in `paired_with`; the shared `pair_axis: luminance` is canonical; resistance valence per § 5.1 of the expansion decision is paired-only. The grouping-vocab MUST reflect this pairing or there is Discipline-#13 implicit-pillar drift between Layer 1 (declarations) and Layer 2 (grouping-vocab). The vocab here matches the spec there.
2. **The Ascension/Passage cosmology already speaks luminance as an opposition.** Per substrate-expansion-decision § 4.1: ascension is *holy-coded* (form rises into the Court's light); Passage is *shadow-coded* (form-not-ascended recedes into shadow); the luminance axis IS the cosmological grammar of choice-at-season-end. Encoding this as a third pair in the grouping vocab makes the cosmology's existing rhetoric L2-explicit.
3. **Lightning's unpairedness is genre-canonical.** Pairing lightning with anything (water-conductivity hook; air-current hook; storm-aggregate hook) would invite elemental-physics interactions the project has explicitly NOT committed to (substrate-expansion-decision § 5.1: "introducing them via lightning-water would Discipline-#13-drift the canonical-four's no-physics-interactions implicit pillar"). Keeping lightning unpaired preserves the no-physics-interactions commitment while still giving the substrate first-class status in the rotation.

**Why these pairings (the underlying logic preserved from v1.1):**

- The substrate's ailment grammar already encodes the oppositions. Fire's `burn` is heat-application; water's `chill` is heat-removal — opposing actions on the same physical axis (thermal). Earth's `root` is positional fixation; wind's `knockback` is positional displacement — opposing actions on the same physical axis (position). Holy's `consecrate` is presence-amplification (reveal/amplify); shadow's `drain` is presence-withdrawal (occlude/remove) — opposing actions on the luminance/presence axis. Lightning's `shock` is propagation-paralysis — it is itself; it has no opposing-substrate ailment mirror. The L1 ailments are *mechanically opposed within their pair-axis*, or unpaired where lightning sits.
- The doppelganger gate (gamora's mirror-validation) tests per-pair viability: a `bulwark`-coded class facing a `displacement`-coded mirror should produce a meaningfully different convergence shape than a `bulwark`-vs-`bulwark` mirror. The pair-structure is what makes the mirror-match work; misaligned pairings would break the gate's diagnostic resolution. With v1.2, the luminance pair adds a third diagnostic axis (radiance-vs-penumbra mirror match); lightning's unpairedness means its mirror-match is always same-axis (resonance-vs-resonance) — a known constraint for D14 diversity-gate design.
- The Wheel-cosmology resonance: the seasonal journey alternates between *embracing* and *resisting* what the form embodies. Per-axis interpretation: Primary axis (ignition ↔ suffusion) carries the season's *active offensive* register; Secondary axis (bulwark ↔ displacement) carries the season's *positional* register; Tertiary axis (radiance ↔ penumbra) carries the season's *presence-and-judgment* register. All three axes are present in every season; per-season vocabulary names *how* the season's cosmology speaks them. Lightning (`resonance`) is the season's *interrupter*; impact is the season's *baseline*.

The LLM at Stage 3 receives the pair-structure framing along with the abstract labels, so per-season vocabulary generation can build coherent opposing pairs (e.g., deep-sea cosmology *naturally* opposes Pressure-Release against Trench-Permeation; both are pressure-state phenomena; the opposition is cosmologically native, not bolted on). The luminance pair's per-season fills should foreground the season's own *presence-and-judgment* lexicon (Yomi: Sun-At-Western-Gate vs Kuroyami-Shroud; cosmic: Solar-Sanctum vs Eclipse-Shadow; the opposition is cosmologically native, not bolted on).

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

Per the pair-structure framing above, `impact` does NOT enter the Primary, Secondary, or Tertiary opposition. Physical is the Foundation's 1-non-rotating element; it is universally available in every season as the martial register. The pair-structure is the *rotating* opposition the season's vocabulary works around; impact is the *constant* the season's vocabulary works with.

### `lightning` → `resonance` (NEW v1.2 — D20 authorship)

The lightning substrate carries the ARPG-genre-canonical *sudden-traversal* mechanical signature: chains across targets, arcs without crossing the space between, ailment-by-arc-paralysis (shock). Across D2's Sorceress Lightning skill tree (Chain Lightning; Thunderstorm; Lightning Strike) → D3's Wizard Lightning + D4's Sorcerer Lightning → PoE's Lightning damage type + Shock ailment → Last Epoch's Lightning skills + Grim Dawn's Lightning, the through-line is *the strike that arrives ahead of warning and propagates between targets*. The shock ailment is mechanically distinctive precisely because it is *the thing that travels with the strike to subsequent targets*.

`resonance` names that mode without naming lightning. The word's etymology is *to sound back* (Latin *resonare*) — what carries between, what arrives at one place because something happened at another, what propagates as a function of medium-coupling. Two additional rationales for this choice:

1. **Resonance is the physics-precise abstraction of lightning's chain mechanic.** A struck target *resonates* with the strike's charge; that resonance propagates to electrically-adjacent targets via the same coupling that drove the original strike. The label encodes the chain-propagation primitive at one register above its electrical specifics — any cosmology's *propagating coupling* fills the slot (deep-sea: Sonar-Cascade; music-spirit: Harmonic-Chain; cosmic: Pulsar-Arc).
2. **Resonance reads as *both* scientific and mythic without committing to either.** D2's "Chain Lightning" reads pure-scientific; D4's "Spiritbreaker" lightning subclass reads pure-mythic. `resonance` admits both registers; the per-season vocabulary can lean either way (Sonar-Cascade reads scientific; Bell-Toll-Bind reads mythic). The label does not pre-commit. This matches lightning's `iconic_register: scientific` declaration without trapping per-season vocabulary in lab-coat tone.

Per-season fills (illustrative):
- Deep-sea: Sonar-Cascade (the acoustic ping that propagates between vessels via water-coupling)
- Music-spirit: Harmonic-Chain (the resonance that sounds across multiple instruments in the same tonic)
- Yomi: Bell-Toll-Bind (the temple-bell sound that travels between the worlds; the dead hear and respond)
- Cosmic: Pulsar-Arc (the radiation pulse that arcs between cosmic bodies)
- Necrotic: Death-Knell-Ring (the death-toll that propagates through neighboring lives)

The label preserves the substrate's mechanical identity (chain/arc/propagation; shock-paralysis-on-arc) while admitting any cosmology's substance.

**Avoided alternatives:**
- `arc` — too literal to the geometry; reads as a shape-label not a mode-label; would confuse with the `arc` geometry primitive already in the geometry registry. Geometry-vocabulary collision.
- `surge` — strong on energy-burst feel but loses the *propagation-between-targets* specificity; surge is a single rising event, not a between-things mechanism.
- `discharge` — too clinical; reads as battery-vocabulary; loses the mythic-cosmological register the cipher architecture wants.
- `flash` — captures the speed but not the chain; lightning is *not* just fast, it is *fast-and-propagating*; flash misses half the signature.
- `traversal` — captures the cross-without-crossing-space premise but reads as movement-vocabulary; loses the propagation-as-damage register.
- `current` — physics-class precise but reads as fluid-vocabulary; would cross-talk with water's suffusion register.

`resonance` carries the right register: propagation-between-things; sounds-back-from-strike; couples-medium-to-medium. Genre-legible (PoE players have encountered `resonator` items; D4 Druid has resonance-keyed talents at the Storm tree); not over-claimed by another substrate; admits per-season variation cleanly.

### `holy` → `radiance` (NEW v1.2 — D20 authorship)

The holy substrate carries the *revelation-and-amplification* mechanical signature: consecrates ground, amplifies allies, valenced-ailment (consecrate — beneficial to aligned, harmful to opposed). Across D2's Paladin auras (Conviction, Concentration, Fanaticism; Holy Bolt; Holy Fire) → D3's Crusader Heaven's Fury + Akarat's Champion → D4's class-opposition Necromancer-vs-Holy → PoE's Sentinel Holy skills → Last Epoch's Sentinel Holy tree, the through-line is *what lifts what is aligned with it and burns away what is not*. Holy's mechanical distinctiveness is **valence** — almost alone among substrates, holy damage interrogates *who you are* before it interrogates *what you are made of*.

`radiance` names that mode without naming holy. The word's etymology is *to send out rays* (Latin *radiare*) — what emanates outward from a source, what fills the space around it with itself, what *cannot remain in the place it occupies without being noticed there*. Three additional rationales:

1. **Radiance is the abstraction-above-deity that holy needs.** Per substrate-expansion-decision § 3.1, `holy` was chosen as the substrate name over `divine` to avoid deity-coding in Reincarnated's impersonal Wheel cosmology. At the L2 layer, `radiance` does the same work at one register higher: it captures the outward-emanation-of-self primitive without committing to *who* is doing the emanating. A bioluminescent deep-sea organism radiates; a tonic-major chord radiates harmonically; a solar sanctum radiates; none of these need a god to source the radiation.
2. **Radiance encodes the valenced-ailment register cleanly.** Light reveals; light amplifies; light has nothing to do with the value-judgment but the value-judgment is *visible because of the light*. The consecrate ailment is amplification-for-aligned + DoT-for-opposed; the asymmetry is encoded in the label's *what is revealed by being-near-radiance*. Per-season vocabulary can foreground either side: Bioluminescent-Bloom emphasizes the reveal; Sun-At-Western-Gate emphasizes the judgment.
3. **Radiance pairs cleanly with penumbra on the luminance axis.** Radiance is *light emanating outward*; penumbra is *the shadow at the edge of light*. The pair is etymologically and phenomenologically opposed; the LLM does not have to invent the opposition — physics and language already encode it. This matches the criterion (set in the Pair-structure framing § above) that pair-axes be cosmologically native, not bolted on.

Per-season fills (illustrative):
- Deep-sea: Bioluminescent-Bloom (the abyssal organism whose light is what makes it visible AND what makes prey aware of it)
- Music-spirit: Tonic-Major-Chord (the resolved chord that uplifts what aligns with its key and clashes with what does not)
- Yomi: Sun-At-Western-Gate (the dying sun that judges from the threshold of underworld; per Izanami myth)
- Cosmic: Solar-Sanctum (the solar surface as the sanctified register; what stands in its light is revealed)
- Necrotic: Sanctified-Ash (the ash of consecrated-and-burned corruption; what was rot is now revealed-as-rot)

The label preserves the substrate's mechanical identity (consecration zones; ally-amplification; valenced-against-opposed-luminance) while admitting any cosmology's substance.

**Avoided alternatives:**
- `divine` — substrate-name-rejected per § 3.1; same deity-coding concern would persist at L2.
- `light` — substrate-name-rejected per § 3.1 (parses as illumination physics, not as substrate-class-identity); also collides with shadow's *opposing-via-absence* register at the player-parsing layer.
- `consecration` — too literal to the ailment; reads as ailment-label not as mode-label; would confuse cleanly when star-lord's prompt asks the LLM to *fill* the consecration slot.
- `sanctity` — clerical register but too noun-static; the substrate is *what radiates*, not *what is sanctified*. Sanctity is the *result*, not the *action*.
- `glory` — over-claimed in fantasy genre (Warhammer; Path of Exile's `Glory of the High Templar`); reads as character-trait register more than action-mode.
- `dawn` — too time-bound; dawn is a moment, radiance is a mode-of-being.

`radiance` carries the right register: outward-emanation-of-self; what-reveals-and-amplifies-near-it; what-cannot-be-hidden-from. Genre-legible (PoE has `radiance` as a Sentinel-mode flavor — close enough that players recognize it without conflict; D2 Paladin's holy auras *radiate*; the verb is already in genre-mouth); deity-neutral; pairs cleanly with penumbra.

### `shadow` → `penumbra` (NEW v1.2 — D20 authorship)

The shadow substrate carries the *concealment-and-drain* mechanical signature: withdraws presence and resource, occludes perception, ailment-by-withdrawal (drain). Across D2's Assassin Shadow Discipline (Cloak of Shadows; Mind Blast; Shadow Master) → D3's Demon Hunter Shadow Power + D4's Necromancer Shadow tree → PoE's Shadow class + chaos/dot territory → Solo Leveling's Shadow Army (the load-bearing genre precedent per gandalf-design-lineage Layer 5), the through-line is *what takes without striking; what is present by absence; what arrives without warning and leaves without trace*. Shadow's mechanical distinctiveness is **withdrawal** — alone among substrates, shadow's drain ailment is not *adding* a state to the target but *removing* something from them.

`penumbra` names that mode without naming shadow. The word's etymology is *partial-shadow* (Latin *paene* "almost" + *umbra* "shadow") — the half-light region at the edge of a shadow where the source of light is partially obscured. Four rationales:

1. **Penumbra is the abstraction-above-evil that shadow needs.** Per gandalf seven-reflections VI (the moral-asymmetry observation referenced in substrate-identity-declarations § 7 notes): "Shadow is *occlusion*, not malice — the moral-asymmetry observation is consciously bracketed at the substrate-identity layer." `penumbra` does the same bracketing at the L2 layer. A penumbra is not *the shadow* (full occlusion; full absence); it is *the edge where the light is partial*. The label encodes *withdrawal-of-presence-by-degree* without committing to *what the absence means*. The Solo Leveling Shadow Army is penumbral in this sense — the shadows are not enemy; they are *what walks alongside*.
2. **Penumbra is the physics-precise abstraction of shadow's drain mechanic.** The drain ailment is *partial withdrawal continuing over time* — the target is not snuffed; the target is *gradually unmade*. A penumbra similarly is *gradient withdrawal* — light is present but partially obscured; the degree of obscuration is what makes the region *penumbra* rather than *umbra*. The label encodes the gradient/partial primitive at one register above shadow's specific mechanical surface.
3. **Penumbra pairs cleanly with radiance on the luminance axis.** Radiance is *light emanating outward*; penumbra is *the edge where outward-emanation is partial*. The pair is etymologically and phenomenologically opposed; the LLM does not have to invent the opposition. Crucially, the pair is *not* radiance ↔ umbra (full shadow); it is radiance ↔ penumbra (edge shadow). This asymmetry is intentional — the substrate-identity-declarations declare shadow's mechanical pillar as `CONCEALMENT_AND_DRAIN` (gradient process), not `ANNIHILATION` (binary endpoint). Penumbra encodes the process; umbra would encode an endpoint shadow does not commit to.
4. **Penumbra honors the Solo Leveling precedent without parroting it.** Solo Leveling's Shadow Army is named *Shadow*. Reincarnated's Court of Forms can accept shadow-substrate ascended forms as Court-of-Forms members (per § 4.1 of substrate-expansion-decision: "shadow-substrate ascended forms now occupy a first-class cosmological position rather than being a flavor-tier curiosity"). Naming the *substrate label* `shadow` at L1 and the *mode-of-action* `penumbra` at L2 means the player-facing surface (Spirit Guide voice; Court browser) can speak shadow as substance and penumbra as register, layered. This is the layered-vocabulary discipline the cipher architecture is for.

Per-season fills (illustrative):
- Deep-sea: Abyssal-Veil (the abyssal region where light withdraws by degree as depth increases; presence-by-absence-of-light)
- Music-spirit: Sub-Audible-Hum (the frequency below human hearing that is felt as withdrawal of audible presence; what is felt-but-not-heard)
- Yomi: Kuroyami-Shroud (the underworld dark — Yomi-cosmology-native; the dark that *is* the underworld, not merely *in* it)
- Cosmic: Eclipse-Shadow (the regional shadow cast by celestial body occlusion; gradient withdrawal of solar presence)
- Necrotic: Crypt-Damp (the dampness inside the crypt; presence-by-absence-of-life; what fills the space when life has withdrawn from it)

The label preserves the substrate's mechanical identity (drain over time; concealment / dim_perception; valenced-against-opposed-luminance) while admitting any cosmology's substance.

**Avoided alternatives:**
- `umbra` — too endpoint; full-shadow rather than gradient-shadow; would mis-encode shadow's `CONCEALMENT_AND_DRAIN` pillar as annihilation; also reads as academic-Latin without the per-season vocabulary admitting variation (Yomi's `umbra` would be just `darkness` redundantly).
- `void` — substrate-name-rejected per § 3.1 (PoE Void / Last Epoch Void = different specific mechanic; would generate cross-game confusion); same concern persists at L2.
- `shroud` — captures the conceal-by-covering primitive but reads as object-vocabulary (a shroud is a thing); penumbra reads as region-vocabulary (a penumbra is a place); shadow's mode is more like a *region in space-and-time* than a *thing draped over a target*.
- `eclipse` — too event-bound; eclipse is a moment, penumbra is a region-of-being.
- `obscuration` — academic register; lacks per-season vocabulary admission (deep-sea's `obscuration` reads as a textbook entry rather than a cosmological surface).
- `gloom` — captures the dim-perception flavor but too literal-genre (gothic-horror register); per-season vocabulary would have to fight against the gloom-stereotype rather than build from the mode.
- `dusk` — too time-bound (like dawn for radiance); dusk is a moment, penumbra is a mode.

`penumbra` carries the right register: gradient-withdrawal-of-presence; the-edge-where-light-is-partial; what-is-half-there-by-being-half-not-there. Genre-legible (PoE has `umbral` terminology adjacent; D&D players know `penumbra` from astronomy/illusion-magic vocabulary; Solo Leveling readers recognize the *edge* of shadow as where the Shadow Army emerges); admits the Solo Leveling precedent without parroting it; pairs cleanly with radiance.

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

**v1.2 canonical-7 extension follow-on (Phase-1 P1):** rocket's substrate-identity-loader (D1) integrates substrate-identity declarations whose `grouping_label` field must match a registered entry in the v1.2 vocabulary. The loader's validation per substrate-identity-spec § 5.3 reads the machine-extractable section below to confirm `grouping_label ∈ registered_labels` at boot; fails-loud on mismatch. Path: rocket reads the `## Machine-extractable structured section (v1.2)` YAML block below and validates against it.

### For star-lord (Phase-1 P1 Deliverable 6 — LLM prompt structure refactor)

Per-season cosmological-vocabulary generation prompts consume the grouping-layer vocabulary as the scaffold per cipher-width Outcome 2 β coupling. The v1.2 prompt structure (post-canonical-7 extension):

- Anchor + anchor description (per naming-triad.md § "Generation integration with the cipher architecture")
- The **eight** abstract slots (ignition / suffusion / bulwark / displacement / **resonance / radiance / penumbra** / impact) with brief mode-of-action descriptions (per the v1.2 table above)
- The **three pair-axis framings** plus unpaired-rotating note plus foundation note:
  - Primary (thermal axis): ignition ↔ suffusion
  - Secondary (position axis): bulwark ↔ displacement
  - Tertiary (luminance axis; NEW v1.2): radiance ↔ penumbra
  - Unpaired-rotating (NEW v1.2): resonance (lightning; no opposing-substrate ailment mirror)
  - Foundation (non-rotating): impact (always available; universal martial register)
- The cosmology's narrative seed
- Explicit guidance: *"Generate per-season vocabulary that fills each slot with the season's cosmology. The Primary pair should oppose coherently within the cosmology's terms; the Secondary pair the same; the Tertiary (luminance) pair should foreground the cosmology's own presence-and-judgment grammar. The Unpaired-rotating slot (resonance) should name the season's interrupter / propagating coupling. The Foundation slot (impact) should name the season's martial register. The vocabulary should evoke the cosmology; it should not translate the abstract labels literally."*
- Anti-bias scaffolding (Discipline #14 candidate; do NOT expose canonical-7 labels in the prompt; ESPECIALLY do not expose `holy` / `shadow` / `lightning` strings — substrate-expansion-decision § 7 vocab freeze remains operative through Phase-1 P1 ship)

**Registry-driven implementation requirement (wide-net § 2.3 critical-surprise resolution):**

The current `reincarnated-engine/src/reincarnated/llm/cosmological_vocabulary.py:63-75` hardcodes the v1.1 2-2-1 pair-structure as Python constants (`GROUPING_SLOTS` tuple, `_SLOT_MODE_OF_ACTION` dict, `_PRIMARY_PAIR`, `_SECONDARY_PAIR`, `_FOUNDATION_SLOT`). D6 must refactor this to read pair-structure shape from the machine-extractable structured section below. Recommended refactor shape:

```python
from reincarnated.foundation.grouping_vocabulary_loader import load_grouping_vocabulary

GROUPING_VOCABULARY = load_grouping_vocabulary()  # boot-time load; fail-loud on missing file/schema
# GROUPING_VOCABULARY.labels                  → tuple of all 8 labels (ordered)
# GROUPING_VOCABULARY.modes_of_action         → dict[label, str]
# GROUPING_VOCABULARY.pairs                   → list[Pair(label_a, label_b, axis_name)]
# GROUPING_VOCABULARY.unpaired_rotating       → list[label]   (lightning's resonance for v1.2)
# GROUPING_VOCABULARY.foundation              → list[label]   (impact for v1.2)
# GROUPING_VOCABULARY.substrate_to_label      → dict[substrate, label]   (8 entries: 7 substrates + physical)
# GROUPING_VOCABULARY.version                 → str            ("v1.2")
```

After refactor: substrate-expansion to canonical-N (future P2+) requires authoring substrate identity declarations + extending this doc's machine-extractable section + bumping the version field. No Python source change needed at the LLM prompt-construction layer. **This closes the wide-net § 2.3 critical-surprise: pair-structure becomes data, not code.**

The prompt is one coherent cosmological-vocabulary call per season per naming-triad.md § "Generation integration with the cipher architecture" — it generates the slot-fills *plus* the Trial / Mirror / Passage variants in one pass. The call's output schema grows to 8 slot fills + 3 pair-rationale fields (was 5 + 2); token impact ~30-40% increase; still negligible per cosmological_vocabulary.py LLM cost note.

### For Stage 3 cipher migration (Phase-1 P1; subsumed under D6)

The grouping-layer vocabulary REPLACES canonical-7 labels in every LLM prompt-construction site identified in form-bias-cadence-strategy § 1.1 Cluster E + wide-net § 2.3 + substrate-coupling-archaeology Coupling #8:

- `naming.py:26-36`, `naming.py:87`, `naming.py:89`
- `selector.py:43-47`, `selector.py:394-446`
- `library_generator.py:85`
- `cosmological_vocabulary.py:63-75` (NEW v1.2 — the registry-driven refactor)
- Substrate-coupling Coupling #8 fix-shape: `naming.py` `_CANONICAL_TO_GROUPING` reads from machine-extractable section; assert non-fallback (per substrate-identity-spec § 5.3)

Each site emits the grouping-layer abstract labels + the season's per-season vocabulary fills, NOT the canonical-7 substrate labels. Experiment 1 runs at this stage's gate to confirm residual-bias removal.

### For gamora (Stage 2-3 doppelganger validation; D14 diversity gate consideration)

The doppelganger gate's per-pair viability check (per form-bias-cadence-strategy § 9.3 gamora cascade) operates against the grouping-layer pair-structure. v1.2 expands the diagnostic axes:

- Primary axis (ignition ↔ suffusion) mirror-matches
- Secondary axis (bulwark ↔ displacement) mirror-matches
- **Tertiary axis (radiance ↔ penumbra) mirror-matches — NEW v1.2.** Luminance-valenced (per substrate-expansion-decision § 5.1: opposed-luminance +25% damage; same-luminance -25%) — gamora's mirror-match math must consume the resistance valence to interpret cross-axis mirror results.
- **Resonance mirror-match — NEW v1.2.** Lightning's unpairedness means the only mirror for resonance is `resonance` itself; the mirror-match is always same-axis (lightning-vs-lightning). For D14 gate design, this is a *known constraint* — the gate cannot push lightning archetypes apart by varying their mirror; it must push them apart by other dimensions (geometry, mechanical_signature, role, iconic_register).
- `impact` mirror-matches as the non-pair direct-strike register; unchanged from v1.1.

The gate's diagnostic resolution can now attribute pair-coupled findings (e.g., radiance slot under-damaging across multiple seasons) to the grouping-layer, not the substrate. This sharpens D14's perception-test-grounded similarity metric.

### For drax (Stage 4 display work)

The player-facing surface (per form-bias-cadence-strategy § 9.4 drax cascade) renders the per-season vocabulary at Layer 3, with the grouping-layer abstract labels available as *operational helper-text* in the same dual-surface pattern naming-triad.md § "Where BOTH surface together" specifies. Example:

```
THE SOUNDING                                  ← per-season vocabulary (Layer 3)
(the season's ignition)                       ← grouping-layer label (Layer 2) as helper

You channel the deep-sea pressure-release.    ← per-season vocabulary in flavor text
```

The pattern matches the Trial / Mirror / Passage surfacing pattern from naming-triad.md; the helper-text gives operational clarity without breaking cosmological immersion.

**v1.2 drax-loadout extension (D21 substrate-browser):** when the substrate browser renders the canonical-7, each substrate's L2 grouping label can appear as a coarse-tag in the browser's substrate-tile UI. Example: tile for `lightning` shows "(resonance)" as the L2 register. This is operational helper-text identical in pattern to the demo's per-class flavor-text helper; no new authoring shape.

---

## Machine-extractable structured section (v1.2)

**Authority:** This section is the **single source of truth** for the registry-driven implementation in `reincarnated-engine/src/reincarnated/llm/cosmological_vocabulary.py` (per D6 refactor) and the substrate-identity-loader validation in `reincarnated-engine/src/reincarnated/foundation/substrate_identity_loader.py` (per D1; spec § 5.3 — `grouping_label` field validates against `labels[].name` below).

**Format choice (DECISION 2026-05-17, gandalf, D20):** Inline YAML block within markdown. Rationale:

- YAML is the project's config-file convention (`config/vocabularies.yaml`; `config/elements.yaml`; planned `config/substrate_identities/*.yaml` per D1; `config/roles.yaml` per D4; `config/ailments.yaml` per D5). Loader implementations consume YAML; adding a second format (JSON or TOML) would invite serializer-divergence drift.
- Embedded inside the canonical-story markdown (not extracted to a separate config file) because the **semantic context** (mode-of-action prose; pair-axis rationale; etymological notes) lives alongside the structured data, and authorship discipline keeps them coherent. Extracting the YAML to a separate `config/grouping_vocabulary.yaml` would invite drift between the doc's commitments and the engine's behavior — Discipline #13 implicit-pillar drift risk.
- Star-lord's D6 loader extracts this block at boot via simple regex (`^```yaml\n(.*?)\n```` between the `## Machine-extractable structured section (v1.2)` heading and the next `## ` heading). One-pass extraction; no second-source-of-truth.
- An alternative (separate YAML file referenced from the doc) was considered and rejected because the gandalf-only authorship discipline (per coordination-matrix § 3) is harder to enforce when the canonical content lives in two files. Single-file authorship = single-edit discipline.

**Schema commitment:** the structure below is the v1.2 schema. Field additions are accepted (new optional fields per substrate-identity-spec § 8); field removals or required-field-shape changes require a version bump (v1.3+) and full downstream regeneration.

```yaml
grouping_vocabulary:
  version: v1.2
  authored: 2026-05-17
  authority: gandalf
  source_doc: canonical/story/grouping-layer-vocabulary.md
  decision_record: canonical/story/substrate-expansion-decision-2026-05-17.md

  # All registered L2 grouping labels, ordered by canonical presentation order
  # (canonical-four pairs first; luminance pair; unpaired rotating; foundation last).
  labels:
    - name: ignition
      mode_of_action: "Escalating-burst mode: rapid energy release; area-permeating; ailment-on-contact (burn family). Small inputs cascade into larger outputs over time."
      substrate: fire
      rotating: true
      paired: true
      pair_axis: thermal
      pair_partner: suffusion
      added: 2026-05-16

    - name: suffusion
      mode_of_action: "Pervading-sustain mode: state-changing presence; slows and binds without striking; ailment-by-immersion (chill family). Fills a space rather than hitting it."
      substrate: water
      rotating: true
      paired: true
      pair_axis: thermal
      pair_partner: ignition
      added: 2026-05-16

    - name: bulwark
      mode_of_action: "Anchoring-resistance mode: positional immovability; locks targets in place; ailment-by-binding (root family). What does not yield."
      substrate: earth
      rotating: true
      paired: true
      pair_axis: position
      pair_partner: displacement
      added: 2026-05-16

    - name: displacement
      mode_of_action: "Directional-impulse mode: removes targets from position; redirects momentum; ailment-by-impulse (knockback family). What carries things elsewhere."
      substrate: wind
      rotating: true
      paired: true
      pair_axis: position
      pair_partner: bulwark
      added: 2026-05-16

    - name: radiance
      mode_of_action: "Revelation-and-amplification mode: consecrates ground; amplifies allies; valenced-ailment (consecrate family — beneficial to aligned, harmful to opposed). What cannot abide concealment and lifts what is aligned with it."
      substrate: holy
      rotating: true
      paired: true
      pair_axis: luminance
      pair_partner: penumbra
      added: 2026-05-17

    - name: penumbra
      mode_of_action: "Concealment-and-drain mode: withdraws presence and resource; occludes perception; ailment-by-withdrawal (drain family). What is taken without striking and arrives without warning."
      substrate: shadow
      rotating: true
      paired: true
      pair_axis: luminance
      pair_partner: radiance
      added: 2026-05-17

    - name: resonance
      mode_of_action: "Sudden-traversal mode: chains across targets; arcs without crossing the space between; ailment-by-arc-paralysis (shock family). What ends what was about to happen by being faster than it could happen."
      substrate: lightning
      rotating: true
      paired: false
      pair_axis: null
      pair_partner: null
      added: 2026-05-17

    - name: impact
      mode_of_action: "Direct-strike mode: martial momentum; dodgeable; ailment-by-wounding (bleed family). Strike-and-flow."
      substrate: physical
      rotating: false
      paired: false
      pair_axis: null
      pair_partner: null
      added: 2026-05-16

  # The pair-axis registry. Each axis lists its two paired-labels and the axis-level metadata
  # that LLM-prompt generation + resistance-matrix consumption depend on.
  pair_axes:
    - name: thermal
      labels: [ignition, suffusion]
      cosmological_register: "active-offensive (the season's strike-and-burn versus fill-and-bind register)"
      resistance_valence: symmetric  # canonical-four; no cross-axis damage modifier
      added: 2026-05-16

    - name: position
      labels: [bulwark, displacement]
      cosmological_register: "positional (the season's stand-firm versus carry-away register)"
      resistance_valence: symmetric  # canonical-four; no cross-axis damage modifier
      added: 2026-05-16

    - name: luminance
      labels: [radiance, penumbra]
      cosmological_register: "presence-and-judgment (the season's reveal-and-amplify versus withdraw-and-conceal register; the cosmological grammar of choice-at-season-end)"
      resistance_valence: valenced  # paired-luminance; +25%/-25% per substrate-expansion-decision § 5.1
      damage_modifier_opposed: 1.25  # holy vs shadow target = +25%; shadow vs holy target = +25%
      damage_modifier_same: 0.75     # holy vs holy target = -25%; shadow vs shadow target = -25%
      added: 2026-05-17

  # Labels that rotate into a season's class pool but have no opposing-substrate pair.
  # Diversity-gate consumers (D14): the only mirror-match for these is same-axis;
  # push-apart between same-axis classes must occur on other dimensions.
  unpaired_rotating:
    - resonance

  # Non-rotating foundation labels. Always available in every season's mechanical surface.
  # Not sampled from in class rotation; always present as universal register.
  foundation:
    - impact

  # The pair-structure shape designator, for star-lord D6 + jack-ryan continuous-observation.
  # Format: <canonical-pair-count>-<canonical-pair-count>-<luminance-pair-count>-<unpaired-rotating-count>-<foundation-count>
  # v1.2 shape: 2-2-2-1-1 (two ignition+suffusion + two bulwark+displacement + two radiance+penumbra + one resonance + one impact)
  pair_structure_shape: "2-2-2-1-1"

  # Cardinality assertions (star-lord D6 boot-time validation; rocket D1 loader cross-check)
  expected_cardinality:
    labels_total: 8
    pairs_total: 3
    unpaired_rotating_total: 1
    foundation_total: 1
    substrate_to_label_mappings: 8   # 7 canonical-7 substrates + 1 physical foundation
```

**Field semantics (for loader implementers):**

- `name` — the canonical L2 label string. Used everywhere. Must be unique across all `labels[]`.
- `mode_of_action` — the one-paragraph mode description that goes into LLM prompts. Star-lord D6 prompt template references this directly.
- `substrate` — the canonical-7 substrate (or `physical` for impact) that this label is the L2 grouping for. Substrate-identity-spec § 3.7 `grouping_label` field references back to `name` above.
- `rotating: true` — substrate enters per-season class rotation. `rotating: false` — substrate is foundation (impact / physical only as of v1.2).
- `paired: true` — substrate has an opposing-substrate pair via `pair_axis` + `pair_partner`. `paired: false` — substrate is unpaired (resonance / impact).
- `pair_axis` — the axis name from `pair_axes[]` registry. `null` if unpaired.
- `pair_partner` — the partner label name. `null` if unpaired. **Validator must confirm reciprocal pairing**: if A's `pair_partner: B`, then B's `pair_partner: A`.
- `added` — the doc-revision date when this label entered the vocabulary. For audit-traceability.

**Validation rules (star-lord D6 boot + rocket D1 boot):**

1. Cardinalities match `expected_cardinality` block.
2. Every paired-label's `pair_partner` references a label that reciprocally references it (no half-pairs).
3. Every paired-label's `pair_axis` references an entry in `pair_axes[]`.
4. Every entry in `pair_axes[].labels` references existing `labels[].name` entries.
5. `substrate` field values are unique across `labels[]` (no two labels share a substrate).
6. `pair_structure_shape` string matches the actual counts.
7. Substrate-identity declarations (rocket D1 loader) reference `labels[].name` values that exist here; any unknown `grouping_label` fails-loud (per substrate-identity-spec § 5.3; Pattern P7 prevention).

**Version bump protocol:** if Phase-1 P2 adds a substrate (poison/acid candidate per substrate-expansion-decision § 6 cascade order step 7), this section grows: a new label, possibly a new pair-axis, updated cardinalities, bumped `version: v1.3`. Star-lord's D6 refactor (registry-driven) means no Python source change is needed at the LLM prompt-construction layer for that future expansion; only this doc + substrate-identity declarations.

---

## Open questions (not blocking; queued)

### Q1 — Pair-structure label exposure shape

Doc 37 § 6.5 flags as needing prototyping: *"Does the LLM see both pairs simultaneously (and generate four axes at once), or one pair at a time (independently)?"* This spec defaults to **simultaneous exposure** — the LLM sees both Primary and Secondary opposition framings in the same prompt and generates coherent per-season vocabulary across both pairs in one pass per the naming-triad.md § 75 one-call-per-season pattern. Star-lord's Stage 2 prompt design should validate this default; if cross-pair interactions surface in early Stage-2 generation findings, the simultaneous-exposure default may need to be revisited.

### Q2 — Vocabulary stability across the season

Per naming-triad.md Open Question Q2 (variant stability): the per-season vocabulary is generated *once* per season and remains stable for that season's duration. The grouping-layer vocabulary in THIS spec is locked across all seasons; only the per-season Layer-3 fills vary. No stability question at the grouping layer.

### Q3 — Player-naming of grouping-layer labels

Per naming-triad.md Open Question Q3 (player-naming of variants): the grouping-layer labels are engine-spoken vocabulary, NOT player-facing in the way per-season Layer-3 vocabulary is. Players see the per-season vocabulary; they see the grouping-layer labels only in operational helper-text (per drax handoff above). No player-naming question at the grouping layer.

### Q4 — Future cipher-width expansion (Outcome 1 re-opening)

**v1.2 status (2026-05-17 amendment):** the canonical-7 expansion (substrate-expansion-decision-2026-05-17 Branch A) lands three of the reserved labels in modified form: `severance` was originally reserved for shadow/void/removal-of-being mode and is now realized as `penumbra` (the chosen abstraction better honors the gradient-of-withdrawal premise; severance was too endpoint per the per-element rationale § shadow → penumbra above). `radiance` and `resonance` were not in the original reserved-labels list but are the v1.2 additions for holy and lightning. **Remaining reserved labels (still NOT locked; surfaced for record):** `dissolution` (for blood/necrotic/dissolution-of-form mode), `transmutation` (for midas/alchemy/state-change mode), `convergence` (for crystal/cosmic/aggregation mode). Phase-1 P2 (poison/acid substrate candidate per substrate-expansion-decision § 6 cascade step 7) would likely consume `dissolution` if Matt elects that substrate-set growth post-Phase-1 P1.

**v1.2 closes the architectural extensibility risk per Q4.** Star-lord's D6 refactor makes the LLM prompt structure registry-driven against the machine-extractable section above. Future label additions = doc edit + substrate-identity declaration + version bump; no Python source change at the prompt-construction layer. This means future Q4 re-openings are *cheap* — bounded design work, not engineering refactor.

### Q5 — Demo2 / Earth-meta-layer implications

Demo2 (post-Phase-0) and the Earth-meta-layer's Court / Spirit Guide / Earth-Self hub surfaces may render the grouping-layer vocabulary in cross-season aggregation surfaces (e.g., a Court entry might be tagged *"the Tidecaller — `suffusion`-coded"* as a cross-season form-archetype reference). This is post-Phase-0 territory; surfaced for future reference, not Phase-0 scope.

---

## Cross-references

**v1.1 ancestors (canonical-four era):**
- **Cipher-width Outcome 2 resolution:** `agentic_orchestration/qa/archive/2026-05-16-decisions-log-cipher-width-resolution.md` (commit `1dff66d`)
- **Strategy doc — grouping layer framing:** `canonical/story/form-bias-cadence-strategy.md` § 6.1 (three-layer model); § 6.2 (cipher-width framework); § 6.3 (cipher architecture stays operative); § 7.1 Stage 2 (abstract pair-structure added alongside canonical-four)
- **Original cipher architecture:** `canonical/37-form-bias-diagnosis-and-recovery.md` § 6 (canonical-four element cipher; Position (ii) lock)
- **Naming triad integration:** `canonical/story/naming-triad.md` § "Per-season vocabulary variation" (the one-call-per-season pattern that consumes this vocabulary)
- **Engine-generic meta-structure:** `canonical/story/engine-generic-meta-structure.md` § "What's at the L1 engine substrate layer" + § "Architectural patterns" (cipher architecture as licensable pattern)
- **Cosmology framing:** `canonical/story/cosmology-reincarnated.md` (the Wheel, the Earth Self, the Spirit Guide, the seasonal journey — the cosmological frame this vocabulary serves)
- **Rocket Stage 2 dispatch (the originating context):** `agentic_orchestration/dispatches/2026-05-16-rocket-form-bias-stage-2-grouping-layer.md` (the dispatch that surfaced the vocabulary-spec-gap)
- **Rocket Stage 2 implementation:** `reincarnated-engine/src/reincarnated/generation/class_generator.py:153-182`; `reincarnated-engine/src/reincarnated/generation/MIGRATION.md` § "Vocabulary-spec-gap" (the placeholder this spec replaces)
- **Star-lord Stage 2 sister dispatch:** per-season cosmological-vocabulary generation consuming this vocabulary (SHIPPED Stage 2; see `reincarnated-engine/src/reincarnated/llm/cosmological_vocabulary.py`)
- **Foundation L1 substrate definitions:** `reincarnated-engine/config/elements.yaml`; `reincarnated-engine/src/reincarnated/foundation/foundation.py` (the canonical-four-plus-physical that this vocabulary's keys originally corresponded to)
- **Genre-canon grounding:** `canonical/story/gandalf-design-lineage.md` + Legolas Pass 4 ARPG-community-discourse findings (the ARPG-canon legibility constraints that shaped vocabulary criterion 4)

**v1.2 canonical-7 extension ancestors (2026-05-17):**
- **Substrate-expansion decision:** `canonical/story/substrate-expansion-decision-2026-05-17.md` (Branch A confirmed by Matt 2026-05-17; the substrate set canonical-7 = fire/water/earth/wind/lightning/holy/shadow; paired-luminance treatment per § 3.2; resistance valence per § 5.1)
- **Substrate identity declaration spec:** `canonical/story/substrate-identity-declaration-spec-2026-05-17.md` § 3.7 (`grouping_label` field references back to `labels[].name` in the machine-extractable section above; validation per § 5.3)
- **Substrate identity declarations (the seven):** `canonical/story/substrate-identity-declarations-2026-05-17.md` (each substrate's declared `grouping_label`; lightning/holy/shadow's PROPOSED → CONFIRMED by D20 authorship)
- **Wide-net coupling archaeology (critical-surprise):** `canonical/story/wide-net-coupling-archaeology-2026-05-17.md` § 2.3 (LLM-prompt-structure pair-structure-wired-into-template finding; v1.2 machine-extractable section + star-lord D6 registry-driven refactor closes this)
- **Phase-1 P1 scope-of-work:** `agentic_orchestration/hive-mind/scope-of-work-phase-1-p1.md` § 1.5 Deliverable 20 (this extension); § 1.1 Deliverable 6 (star-lord LLM-prompt structure refactor that consumes v1.2)
- **Phase-1 P1 coordination matrix:** `agentic_orchestration/hive-mind/coordination-matrix.md` § 1 row D20 + § 3 hot-spot entry (gandalf-only authorship; star-lord reads post-D20-land)
- **Hive-mind protocol:** `canonical/story/hive-mind-protocol-2026-05-17.md` (the operating mode under which v1.2 was authored)
- **Earth-Self diversity tension resolution:** `canonical/story/earth-self-diversity-tension-2026-05-17.md` (Court-as-grace; introduces `court_resonance` field on substrate identities — relevant context for luminance-axis cosmological positioning)
- **Substrate-coupling archaeology:** `canonical/story/substrate-coupling-archaeology-2026-05-17.md` Coupling #8 (`naming.py` `_CANONICAL_TO_GROUPING` consumes v1.2 via D6 refactor) + Coupling #13 (`cosmological_vocabulary.py` pair-structure constants replaced by v1.2 registry-driven loader)

---

## Maintenance protocol

This doc is the authoritative source for the grouping-layer vocabulary. Changes require:

1. Gandalf authorship of the change (Pattern A or Pattern B per gandalf operating manual; hive-mode authorship pattern for v1.2 D20 per `hive-mind-protocol-2026-05-17.md` § 14.1)
2. Knight-rider sequencing into decisions-log entry (D23 covers v1.2 alongside the substrate-expansion decision)
3. Jack-ryan Gate 1 review (continuous-observation under hive mode for v1.2; standard Gate 1 review for post-hive changes)
4. Matt approval (substrate-expansion-decision Branch A 2026-05-17 covers v1.2 substantively; subsequent label changes require fresh L3)
5. Engine code version bump tracking (was: rocket bump of `GROUPING_LAYER_VERSION` per Discipline #12). **v1.2 amendment:** the `version` field in the machine-extractable structured section above is the canonical version. Engine code's `grouping_layer_version` constant reads from that section at boot via the loader (star-lord D6 refactor). Schema-semantic shifts require both: bump the YAML `version` field + write a MIGRATION.md note.
6. MIGRATION.md entry per ADR-004
7. Star-lord prompt-template update (post-D6: automatic via registry-driven loader; pre-D6: manual prompt-template edit)
8. **(v1.2 NEW)** Rocket substrate-identity-loader cross-check: if a new label is added, confirm any new substrate identity declaration that references it loads cleanly; if an existing label is removed, audit all substrate identities to confirm none reference the deleted label.

The vocabulary is **not** lightly revisable. The substrate-mechanical-identity preservation criterion (criterion 1 above) means changing a slot's label changes the LLM's interpretive frame for every per-season vocabulary generated against it; downstream regeneration of per-season content may be needed. Future changes should be scoped against that re-generation cost.

**v1.2 lessons for future maintenance:**

- **Pair-axis additions are L2/L3 design decisions, not L1 in-seam.** v1.2's luminance pair-axis was authored by gandalf under hive-mode distributed authority but rests substantively on Matt's Branch A confirmation of the canonical-7 substrate set + paired-luminance treatment (substrate-expansion-decision § 3.2). Future pair-axis additions (e.g., a hypothetical `entropy` axis for dissolution ↔ convergence) similarly require Matt L3 cosmological alignment, not just gandalf authorship.
- **Unpaired-rotating additions are L1 design decisions but L2 architectural confirmations.** v1.2's lightning addition required confirming with substrate-identity-declarations § 5 notes that lightning is canonically unpaired by genre convention; future unpaired-rotating additions should similarly cite genre-canon grounding before landing.
- **The machine-extractable section is the source of truth for the engine.** Future label additions edit it directly; prose sections above should be kept synchronized but the YAML is what star-lord D6 + rocket D1 read at boot. Drift between the YAML and the prose IS a Discipline #13 violation; jack-ryan continuous-observation watches.

The re-opening trigger framework from cipher-width Outcome 2 was the *expected* future maintenance event; v1.2 IS that event (substrate-expansion to canonical-7). Future re-openings (Phase-1 P2 poison/acid substrate; further cosmological expansion) follow the same pattern: substrate-expansion-decision-style L3 design doc → substrate identity declarations → grouping-vocab extension (this doc) → registry-driven engine consumption (automatic post-D6).
