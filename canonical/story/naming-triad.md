# The Naming Triad — Trial / Mirror / Passage

**Status:** **Canonical.** The triad is locked per Matt's approval 2026-05-15 in Pattern B dialogue with gandalf (originally accepted from Phase 2 proposal). This doc finalizes the triad with per-season vocabulary-variation guidance, operational rules for where the universal frame surfaces vs where seasonal flavor surfaces, and LLM prompt-construction integration with the doc 37 § 6 cipher architecture.

**Supersedes** in player-facing surfaces:
- File 32 § Section 11 — "doppelganger" terminology → **Mirror** (the universal frame); per-season vocabulary varies
- File 32 § Section 9 + file 33 — "death body-swap" terminology → **Passage**
- File 33 — "Trial body-swap" remains accurate for the body-swap-path of a Trial; the choice itself is between body-swap-path and Mirror-path at the encounter

**Companion docs:**
- `cosmology-reincarnated.md` § "The Trial" + § "The Mirror" + § "The Passage" — narrative source
- `court-of-forms.md` — what comes after (the Court accumulates from these encounters)
- `enemy-visual-legibility.md` § S4 + § S7 — visual presentation of Trial cinematic frame + Mirror exception
- Doc 37 § 6 — the cipher architecture this doc's per-season variants integrate with
- File 19 — LLM call map (the per-season vocabulary generation call this doc consumes)

**Pending:**
- knight-rider to draft a decisions-log entry capturing the triad locks (per ADR-002; affects player-facing UI copy, LLM prompts, telemetry-field-vs-display naming)

---

## The triad

| Universal frame name | What it names | Player choice | Reward shape |
|---|---|---|---|
| **The Trial** | Act-end encounter; the season's three ritualized confrontations (one per act). | Player chooses BEFORE fighting: body-swap-path OR Mirror-path. | Win → reward per chosen path. |
| **The Mirror** | The Mirror-path's opponent: the player's current class reflected against them. | (No further choice during the fight; the choice was at Trial entry.) | Win → preserve class identity. 1/4 immediate reward + remaining via end-game reclaim quest. |
| **The Passage** | The choice offered at death: refuse → respawn with small XP loss; accept → transform into a different form, current form lost for season + cannot ascend. | Refuse or Accept. The Wheel offers; the player answers. | Refuse: continue current journey, mild penalty. Accept: dramatic continuance, real cost. |

These are the **universal frame names.** They are how Reincarnated talks about these encounter moments at the *project* level — in UI labels, in design docs, in operational dispatches, in any context where the language stays the same across seasons.

The **per-season vocabulary** varies, per the doc 37 § 6 cipher architecture. See § "Per-season vocabulary variation" below.

---

## Why this triad — name by name

### The Trial (retained from existing locked terminology)

Already in the project's vocabulary. The locked file 32 § 11 design uses "Trial" for the act-end encounter; this doc retains it. The word does what it should: it names a ritualized confrontation that is *both* a test of the player's current form *and* the season cosmology's mechanism for offering transformation. The word carries Christian-medieval-trial weight (an ordeal the soul must pass) AND samsaric-test weight (a karma-measurement moment). Both readings work.

The Trial is the **structural frame** of each act. The per-act 1-Trial-per-act lock (file 32 § 10) is the rhythm; the Trial is the moment.

### The Mirror (renamed from "doppelganger")

Phase 2 § 1.7 locked this rename for substrate reasons. "Doppelganger" carries 1840s-German-folklore baggage (the prophetic-twin-warning-of-death of European Romanticism) AND WWII-era occult baggage (Nazi-era doppelganger fascination). Neither is what Reincarnated's mirror-fight is doing.

"Mirror" names the central mechanical truth (you face your reflection) without occult baggage. Genre-shipped precedent: PoE's "your shadow" is occupied; D4's "Shadow Realm" is occupied; Solo Leveling's "Shadow Army" is occupied. "Mirror" is *available* in the genre's vocabulary AND the right word for the mechanic.

The Mirror Trial is **the recognition encounter.** Per cosmology-reincarnated.md § "The Mirror": *"You see yourself, and you choose what stays."* The visual identity-grammar per enemy-visual-legibility.md § S7 is the rendering side; "Mirror" is the naming side. They reinforce each other.

### The Passage (renamed from "death body-swap")

Phase 2 § 1.7 locked this rename for framing reasons. "Death body-swap" is mechanically accurate but pre-judges the moment as failure-state. The mechanic itself is a *real choice with real cost* — both options (refuse or accept) are valid. The name should be neutral about which is "right."

"Passage" names the offered crossing without pre-judgment. Shipped genre precedents for neutral mythic-register death-mechanics: Hades's "Charon's Crossing," Souls family's "Bonfire," Returnal's "Cycle." None of these names embed "you failed" in the language. "Passage" sits in this lineage.

The Passage is **the Wheel's moment.** Per cosmology-reincarnated.md § "The Passage": the Spirit Guide is *visibly absent* at the Passage; the Wheel speaks here, in event-not-word. The Wheel offers; the player answers. The neutrality of the name honors that.

---

## Per-season vocabulary variation

Doc 37 § 6 commits the project to **per-season vocabulary** generation as the LLM-visible surface above the hidden canonical four. The Trial / Mirror / Passage triad is part of that per-season vocabulary work — each season generates flavored variants of the triad that honor the season's cosmology.

### The variation pattern

The **universal frame names (Trial / Mirror / Passage)** remain the operational structure across all seasons. The **per-season variants** flavor the prose, dialogue, and LLM-narrated content of the season. Both surfaces coexist:

- **The universal frame** = stable across all seasons. Used in: UI operational labels (the "Trial" button on the act-progression screen); design docs; telemetry; engine code; cross-season Spirit Guide references that span beyond a single season.
- **The seasonal variant** = generated per season. Used in: in-season Spirit Guide dialogue; the Trial encounter's flavor text and announcement; the Mirror's flavor lines; the Passage's flavor framing; LLM-generated quest text, NPC dialogue, world-flavor content within the season.

**The player learns the universal frame across seasons** (Trial / Mirror / Passage become known operational vocabulary by season 2-3) while **each season's flavor variant gives the encounter its cosmological texture** (Yomi's Trial *feels* different from a deep-sea season's Trial without the *frame* being different).

### Generation integration with the cipher architecture

The per-season Trial / Mirror / Passage variants are generated **in the same LLM call** that generates the season's elemental vocabulary (per doc 37 § 6 pair-structure layer). Not three separate calls. One coherent cosmological-vocabulary-generation pass per season produces:

- The seasonal elemental vocabulary (Primary Opposition pair + Secondary Opposition pair, per doc 37 § 6)
- The Trial variant for this season
- The Mirror variant for this season
- The Passage variant for this season

This keeps the LLM cost bounded (one cosmological-vocabulary call per season, not four) and architecturally coherent (the variants are generated *from the same cosmology* that produces the elemental vocabulary).

The LLM prompt construction for this call should include:
- The anchor + anchor description (e.g., "The Deep Trench — the place in the sea where light has never reached")
- The Primary / Secondary opposition labels (abstract; per doc 37 § 6)
- The cosmology's narrative seed (a paragraph of the season's worldbuilding)
- Explicit guidance: *"Generate the season's variants of three encounter moments — the Trial (the act-end ritualized confrontation), the Mirror (the player's reflection encountered as opponent), and the Passage (the offered crossing at death). The variants should evoke the season's cosmology; they should not translate the universal names literally. Each should be a phrase the season's Spirit Guide would use in this world."*
- The canonical-four cipher's anti-bias scaffolding (per Discipline #14 candidate — do not expose canonical-four labels in the prompt)

### Example variants

Worked examples for the existing production seasons + Yomi. **These are illustrative**, not necessarily what an LLM call would generate; they show the *register* the variants should achieve.

| Season | Anchor + theme | Trial variant | Mirror variant | Passage variant |
|---|---|---|---|---|
| **001001 Deep Trench (wind)** | the lightless depths | *The Sounding* | *The Brine-Image* / *The Stillness-Below* | *The Sinking* / *The Drift-Below* |
| **001002 Crypt of the First Saint (earth)** | the saint's reliquary | *The Vigil-Trial* / *The Saint's-Ordeal* | *The Echo-of-Bone* | *The Crossing-of-Stone* |
| **001003 Cathedral of Bone (water)** | the marrow cathedral | *The Marrow-Test* | *The Bone-Reflection* / *The Counter-Cantor* | *The Final-Breath* / *The Ossuary-Crossing* |
| **001004 Throne Room of the Mad King (earth)** | the king's throne | *The King's-Audience* | *The Pretender* / *The Throne-Shadow* | *The Mercury-Drink* / *The King's-Mercy* |
| **001005 Ghost Town of the Gold Strike (water)** | the abandoned strike | *The Vein-Test* / *The Strike-Trial* | *The Counter-Claim* | *The Strike's-End* / *The Dust-Take* |
| **Yomi (Japanese underworld)** | the threshold of the dead | *The Threshold-Test* / 黄泉の試練 | *The Pomegranate-Image* (Izanami myth) | *The Pomegranate-Eaten* / 黄泉の道 |

**The Yomi example is worth dwelling on.** Yomi in Japanese myth is the underworld; Izanami eats the food of Yomi and is bound there permanently. The Passage analog in Yomi is *literally* the eating-of-food — accept the food, become bound to Yomi (lose the form to the season). This is the level of cosmological-resonance the per-season vocabulary work can achieve. A future LLM call generating Yomi's vocabulary should be guided to find this kind of resonance, not produce generic translations.

This is the kind of resonance the cipher architecture (doc 37 § 6) makes possible: the *internal* mechanism (the Wheel offering the body-swap on death) ciphers to the canonical mechanic; the *external* surface (the pomegranate, eaten, binding the soul) is the season's own myth.

---

## Operational rules

### Where the universal frame surfaces

- **UI operational labels** at structural moments — the "Trial" tab on the act-progression screen, the "Mirror Trial / Body-swap Trial" choice screen labels, the "Refuse / Accept the Passage" choice screen labels.
- **Design docs and decisions-log entries** — Trial / Mirror / Passage as the canonical vocabulary.
- **Telemetry fields and engine code** — `is_trial_encounter`, `is_mirror_encounter` per enemy-visual-legibility.md § S7; technical field names use the universal frame.
- **Cross-season Spirit Guide references** that span beyond the current season — *"You faced your Mirror in your Cathedral season; you remember the shape of that fight."*
- **Court entries and the Earth Self hub** — Court members are referred to by their full LLM-generated name; the *circumstance of their ascension* is referred to via universal-frame vocabulary (*"ascended after the Mirror-path Trial in season N"*).

### Where seasonal flavor surfaces

- **In-season Spirit Guide dialogue** during the active season — *"The Sounding waits at the end of this descent."* (Deep Trench)
- **Trial encounter flavor text** and announcement banners — the cinematic-frame banner (per enemy-visual-legibility.md § S4) uses the seasonal variant.
- **Mirror flavor lines** — the Mirror's voice lines, if used, are in the seasonal variant register.
- **Passage flavor framing** — the choice screen text uses the seasonal variant alongside the universal frame (*"Refuse the Pomegranate. / Accept the Pomegranate."* with universal-frame helper-text below: *"Refuse the Passage / Accept the Passage."*)
- **LLM-generated quest text, NPC dialogue, world-flavor content** — uses seasonal variants throughout.
- **Per-season anchor prose** (forthcoming `seasonal-anchor-prose-notes.md`, work queue #12) — references its seasonal variant.

### Where BOTH surface together

The choice screens at Trial entry and at the Passage moment should surface **both** layers simultaneously:

**Trial choice screen example (Yomi season):**
```
THE THRESHOLD-TEST
(The Trial)

→ Take the form of the Threshold-Keeper
  (Body-swap path — transform on victory)

→ Face the Pomegranate-Image
  (Mirror path — preserve identity, claim deferred rewards)
```

**Passage choice screen example (Yomi season):**
```
THE WHEEL TURNS.

→ Refuse the Pomegranate
  (Refuse the Passage — respawn, small XP loss)

→ Accept the Pomegranate
  (Accept the Passage — transform, this form lost forever to this season)
```

The seasonal variant carries the cosmological weight; the universal frame in parenthetical helper-text gives operational clarity. The player learns the frame across seasons; the flavor stays season-specific.

---

## Engine-side telemetry retention

The engine currently uses "doppelganger" as the technical term in code and telemetry (per file 32 § 7.2; the multi-band sim runs three doppelganger-validation runs per class; the doppelganger gate is the validation surface). **The engine can retain this technical name during transition.** The naming-triad lock is player-facing-language work, not engine-field-rename work.

Specifically:
- Engine fields like `doppelganger_validation_runs`, `doppelganger_gate`, `is_doppelganger_encounter` can remain in code and telemetry.
- The export packet **may** expose these as `is_mirror_encounter` for downstream-consumer clarity (per enemy-visual-legibility.md § S7); whether to rename at the export-boundary or only at the rendering-layer is a rocket/star-lord dispatch detail when implementation work begins.
- Engine-side log messages, internal documentation, and code comments can use either term during transition; new engine code should prefer Mirror for fields touching player-facing surfaces and may retain doppelganger for purely mechanical sim-internal contexts (e.g., the doppelganger gate's mathematical doppelganger-vs-self validation logic).

A future MIGRATION (rocket dispatch territory) could rename the engine-internal fields, but it is **not urgent.** The canonical lock is the player-facing naming; the engine-internal naming is operational housekeeping that can land when convenient.

---

## LLM prompt construction guidance

For star-lord's LLM prompt-template work (file 19 § Phase 02 and beyond):

### When the prompt generates per-season cosmological vocabulary

Include the triad-variants generation in the same call as the elemental vocabulary. Prompt structure (illustrative):

```
[anchor description]
[primary/secondary opposition labels, per doc 37 § 6]
[cosmology narrative seed paragraph]

Generate this season's variants for three encounter moments:

1. The Trial — the season's act-end ritualized confrontation.
   Provide a phrase the season's Spirit Guide would use to refer to this moment.
   Do not translate "Trial" literally; evoke the season's cosmology.

2. The Mirror — the encounter where the player faces their reflection deployed
   as opponent (the Mirror-path of the Trial).
   Provide a phrase that evokes self-encounter within this season's cosmology.

3. The Passage — the offered crossing at the moment of death; the Wheel offers
   transformation in exchange for the abandonment of this form.
   Provide a phrase that evokes the offered crossing within this season's cosmology;
   the phrase should be neutral about whether refusal or acceptance is "right."

Respond in JSON: { "trial_variant": ..., "mirror_variant": ..., "passage_variant": ... }
```

### When the prompt generates in-season flavor content

LLM calls for Spirit Guide dialogue, quest text, NPC dialogue, anchor flavor, etc. should be given the season's variants as prompt context AND instructed to use them naturally:

```
Season cosmological vocabulary:
- Trial variant: "The Sounding"
- Mirror variant: "The Brine-Image"
- Passage variant: "The Drift-Below"

When this content references any of these encounter moments, use the variant
naturally as the in-season term. The Spirit Guide says "The Sounding waits,"
not "The Trial waits." Universal frame names (Trial / Mirror / Passage) appear
only in UI helper-text, not in narrative content.
```

### Anti-bias scaffolding (Discipline #14 candidate)

The triad-variant generation prompt should NOT expose:
- The literal English words "Trial," "Mirror," "Passage" as anything other than design-frame references the LLM is asked to flavor
- Canonical-four element labels (per doc 37 § 6 cipher)
- Class-archetype labels or mechanical-property names
- Attribute axis labels (STR/DEX/INT)

The LLM should be working from the season's cosmology + the abstract pair-structure + the design-intent of each encounter moment, not from internal mechanical labels.

---

## Open questions

These do not block the lock. They surface during implementation work.

### Q1 — Variant length / register

Should per-season variants be **single words** ("The Sounding"), **short phrases** ("The Threshold-Test"), or **longer evocative phrases** ("The Place Where the Brine Stops")? My instinct: **short phrases of 2-5 words** are the sweet spot — long enough to evoke cosmology, short enough to fit in UI banners and dialogue. The LLM prompt should specify this length range.

### Q2 — Variant stability across the season

Within a season, should the variant stay **fixed** (same phrase used throughout) or **evolve** (Spirit Guide refers to it differently across acts; the climactic Trial gets a heightened variant)? My instinct: **fixed within a season** for player-recognizability; possibly **act-amplified** at the final Trial (the third Trial gets a heightened reference: *"the final Sounding"*, *"the deepest Sounding"*). Operational simplicity favors fixed.

### Q3 — Player-naming of variants

Should the player be able to **rename** their seasonal variants? E.g., "I call my Trial-of-the-Deep-Trench 'the Brine-Test' — the system should honor that." My instinct: **no.** The variants are the season's voice, not the player's. The Earth Self is named by the player (per cosmology-reincarnated.md); seasonal variants are not. Maintains the "the season has its own cosmology that you walk into" frame.

### Q4 — Variant exposure in pitch / marketing

Should the pitch and marketing materials use the seasonal variants OR the universal frame? My instinct: **the universal frame for marketing** (Trial / Mirror / Passage are clean genre-recognizable terms; seasonal variants require context to land); **seasonal variants for in-game and in-context marketing** (a Yomi-themed marketing piece can use "Threshold-Test" if the context supports it). Per-asset decision.

### Q5 — Existing-season retrofit

The 5 production seasons (1001-1005) shipped without variant generation. When (and if) seasons are re-generated, the new generation includes variants. Existing seasons can either: (a) stay variant-less, with the universal frame surfacing universally; (b) get retrofit-generated variants in a follow-on LLM call. Per the single-season-per-playtest cost guardrail (file 16 § "Single-season-per-playtest rule"), this is not urgent. Probably (a) is fine — the existing seasons are demo1-baseline artifacts; the new seasons (post-Stage-A2) get variants natively.

---

## Cross-references

- `cosmology-reincarnated.md` § "The Trial" / § "The Mirror" / § "The Passage" — the cosmological frame
- `court-of-forms.md` — where Trial / Mirror outcomes accumulate
- `enemy-visual-legibility.md` § S4 (Trial cinematic frame) + § S7 (Mirror exception)
- Doc 37 § 6 — cipher architecture; integration target for per-season variants
- File 32 § Section 11 — body-swap mechanics (the Trial paths' mechanical substrate)
- File 32 § Section 9 + file 33 — Passage mechanics (the death-body-swap substrate)
- File 19 § Phase 02 — LLM call map; the per-season cosmological-vocabulary call this doc consumes
- Discipline #14 candidate (per doc 37 § 9.2b) — anti-bias scaffolding for LLM-visible labels

---

## Maintenance protocol

When implementation work consumes this doc:

1. **Star-lord LLM prompt work** — integrate per-season triad-variant generation into the existing per-season cosmological-vocabulary call.
2. **Drax UI copy work** — surface seasonal variants in choice screens / Spirit Guide dialogue / Trial banners; surface universal frame in helper-text.
3. **Rocket engine work** — no urgent change; the engine retains internal naming; export-boundary rename is optional housekeeping.
4. **Knight-rider dispatches** — reference this doc; use universal frame in dispatch language; seasonal variants are LLM-call output.

When future per-season cosmological-vocabulary generation runs:

1. The call MUST include triad-variant generation (Trial / Mirror / Passage).
2. The call MUST NOT expose canonical-four element labels or universal frame literals as anything other than design-frame instruction.
3. Generated variants land in the season export packet alongside the seasonal elemental vocabulary.

When future canonical docs touch encounter-moment naming:

1. Reference this doc.
2. The universal frame is canonical; do not introduce parallel framings.

— gandalf, with Matt's standing approval on the locked triad (2026-05-15)
