# Season-Feel Rubric — What Makes a Season Distinct

**Status:** **Canonical.** Authored 2026-05-16 by gandalf. Captures the design-intent dimensions that must cohere for a Reincarnated season to feel like *its own thing* rather than as procedural variation on a generic template.

**Why it exists:** the project's commercial frame depends on cross-season distinctiveness (per pitch-2026-05-18 talking-points-distillations § "The Court" — *"how many seasons has the Wheel turned with you still walking"* presupposes that walking each season is *meaningfully different*). Without explicit canonicalization of what makes a season distinct, the seasonal generation pipeline may produce content that is technically varied but experientially homogenous. Discipline #13 application at the season-feel layer.

**Companion docs:**
- `cosmology-reincarnated.md` — the Reincarnated-specific cosmology this rubric operates within
- `engine-generic-meta-structure.md` — the L1/L2/L3 layer separation; this rubric operates at the L3 per-season content layer with L2 cosmology grounding
- `naming-triad.md` — per-season vocabulary variation as one rubric dimension
- `embodiment-narrative-layer.md` — embodiment vocabulary as one rubric dimension
- `style-register.md` — visual register; the canvas this rubric paints on
- `spirit-guide-voice.md` — the Guide's voice acknowledges each season's particular cosmology
- `gandalf-design-lineage.md` Layer 2 (D2 act-thematic-distinctiveness) + Layer 3 (PoE league-atmospheric-coherence)
- Doc 37 § 6 — cipher architecture; the mechanism for per-season vocabulary

**Pending:**
- knight-rider to draft a decisions-log entry capturing the season-feel-rubric canonical lock (per ADR-002; affects star-lord LLM prompt construction + rocket generation + drax UI presentation)
- engine-balance-stewardship.md (forthcoming) will consume this doc as foundation

---

## What this doc is — and isn't

**It is** a design-intent doc articulating the dimensions that must cohere for season-distinctiveness. It admits derived-rubric usage — LLM prompts, family-playtest review, and future-content quality gates can evaluate generated seasons against these dimensions.

**It is not** a scoring rubric with numeric thresholds. The dimensions are categorical-design-criteria, not metrics. *"Does the season's gear flavor cohere with the season's anchor?"* admits a yes/needs-revision answer, not a 0-100 score.

**It is not** an exhaustive enumeration of season content. It names the dimensions that *must* cohere; downstream content (specific names, specific mechanics, specific player decisions) flows from the dimensions but is not pre-enumerated here.

**It is not** Reincarnated-specific in its PATTERN. The dimensions and the coherence-requirement are generic; a licensing studio's engine instance produces their own season-feel rubric grounded in their L2 cosmology. This doc is Reincarnated-specific in its EXAMPLES and the cosmology those examples consume.

---

## Why season-feel matters

The pitch's load-bearing claim is *"how many seasons has the Wheel turned with you still walking"* — the Court's depth as the meta-measure (per court-of-forms.md C7 + cosmology-reincarnated.md meaning-of-the-arc statement). This claim presupposes that **each season is meaningfully different** in the player's experience.

If seasons are procedurally varied but experientially homogenous, the meta-measure collapses. *"Twelve seasons"* becomes a counter, not an accumulation. The Court becomes a roster of differently-named-but-fundamentally-same retainers.

Genre-precedent failure modes:

- **Diablo III post-launch seasonal content** initially shipped with thin thematic differentiation between seasons — different cosmetic rewards, similar content. Player retention suffered until seasons gained more distinct thematic personalities.
- **PoE leagues without strong mechanical identity** (some weaker leagues mid-history) registered as forgettable; players who played through them couldn't recall their distinctive shape later. Strong leagues (Bestiary, Delve, Heist, Affliction) had deep mechanical-AND-thematic coherence.
- **Procedural roguelikes generally** struggle with cross-run distinctiveness when the procedural variety is mechanical-only. Slay the Spire's runs feel similar despite enormous mechanical variation; Hades's runs feel distinct because each Olympian boon-giver carries thematic-AND-mechanical identity.

Reincarnated's seasons must achieve **the Hades-level of per-run thematic-mechanical coherence** rather than the Slay-the-Spire-level of procedural-mechanical-only variation. This rubric articulates how.

Genre-precedent success modes:

- **Diablo II's acts** (per gandalf-design-lineage.md Layer 2): each act is *deeply* thematically coherent — Act 1's gothic Rogue Encampment, Act 2's Arabian-night Lut Gholein, Act 3's jungle ruin Kurast, Act 4's Pandemonium hell, Act 5's Viking Harrogath. Music, architecture, NPCs, monster types, lore, named weapons, questing rhythm all reinforce one another within each act. **This is the level of coherence per-season Reincarnated should reach for.**
- **PoE leagues with strong identity:** Affliction's wilderness-bordering-on-horror; Heist's stealth-and-heist register; Delve's claustrophobic-darkness. The league's mechanical novelty IS its thematic novelty.
- **Hades's biome chambers:** Tartarus / Asphodel / Elysium / Styx each has its own visual register, music, enemy types, environmental hazards, and atmospheric weight.

---

## The rubric — ten dimensions that must cohere

A Reincarnated season's distinctiveness emerges when these ten dimensions all coherently express the season's cosmological register. **Missing or thin coherence on any single dimension may not break the season; missing coherence on multiple dimensions does.**

### D1 — Cosmological register (the anchor's spiritual/emotional weight)

The anchor (e.g., *"The Deep Trench"*, *"Yomi"*, *"The Cathedral of Bone"*) carries a specific cosmological register — a mythology, an atmosphere, an emotional weight. This register is the season's *soul*. Every downstream dimension should pulse through this register.

**Example:** Yomi as Japanese underworld carries: liminality (the threshold between life and death); binding-via-consumption (Izanami's pomegranate myth); the unease of *that-which-should-stay-buried*; ancestor-presence; the specific Shinto-Buddhist mythological register.

**Failure mode:** the anchor name is evocative but the rest of the content treats it as a sticker. *"The Cathedral of Bone"* with classes named "Fire-Mage of the Cathedral" — the anchor is decoration, not soul.

**Where the cosmological register lives:** in the anchor's prose description (the 130-entry library content — partially `seasonal-anchor-prose-notes.md` work queue item #12 territory); in the per-season LLM-call's cosmological-vocabulary generation seed (per doc 37 § 6); in every downstream LLM prompt's context.

### D2 — Elemental palette (the cipher-substituted vocabulary)

The four seasonal element flavors (cipher-substituted per doc 37 § 6: e.g., *pitch / brine / thrum / basalt* for Deep Trench) must:

- **Cohere with the anchor's cosmological register** (Deep Trench's *brine* and *basalt* land because the anchor is a lightless sea; Yomi's vocabulary lands because it's the underworld)
- **Be visualizable** (per file 28 § D1 rubric — *milk* failed because it doesn't visualize in combat)
- **Be combat-compatible** (per file 28 § D1 — soft/intimate/medical/domestic associations fail)
- **Mechanically signature per Position (ii) lock** (doc 37 § 6.2 — pressure has its own mechanical feel, not just renamed-fire)

**Example:** *pitch* (the Deep Trench's fire-flavor): visualizable (black viscous substance); combat-compatible (sticky, burning, adhesive); cosmologically coherent (the abyssal sea has *something* hot in its depths — geothermal vents, oil seeps). The single word carries the anchor's register.

**Failure mode:** elemental palette is technically substituted but semantically thin (*milk* / *thrum*; see decisions-log on D1 rubric work). The substitution looks right in spreadsheet review but lands badly in player experience.

### D3 — Class roster (generated classes that fit the cosmology)

The 5-6 playable + 3 act-boss classes generated for the season should:

- **Read as inhabitants of THIS cosmology** (the Pitch-Caster belongs in the Deep Trench; a generic fire-mage would not)
- **Cohere with each other within the season** (the Deep Trench's roster is unified by *its* register; not a random assortment)
- **Express archetype variety within the cosmology** (Front-Line, Ranged, Control, etc. all rendered through the season's cosmological lens per embodiment-narrative-layer.md C8)
- **Include the embodiment axis variation** (post-doc-37 embodiment work — not all classes humanoid; the season's cosmology admits or rejects specific embodiments)

**Example:** Deep Trench's class roster includes *Trenchwind Pitch-Caster*, *Trench-Breathed Tidecaller*, *Abyssal Basalt Monk* (from family-review/character-loadouts.md). The names contain the seasonal vocabulary substrates; the identities cohere within the abyssal sea cosmology. **What's weak in current production:** these are all humanoid (per doc 37 form-bias diagnosis; this season's roster could include a slime-form, swarm, or other non-humanoid).

**Failure mode:** classes have seasonal element substrings in their names but are otherwise generic. *"Cathedral Fire-Mage"* with a humanoid robe-wearing kit indistinguishable from any other season's fire-mage.

### D4 — Monster register (adversary identity coherent with the anchor)

Generated monsters across all tiers (swarm / magic / trash / elite / mini-boss / boss / act-boss) should:

- **Read as creatures of THIS world** (Deep Trench monsters are abyssal-coded; Yomi monsters are underworld-coded; Cathedral monsters carry ossuary register)
- **Cohere across the tier hierarchy** (the swarm and the boss share an aesthetic-cosmological lineage; the world's predators are recognizably *of* the world)
- **Display embodiment variety appropriate to the cosmology** (Deep Trench may have aquatic / aberrant non-humanoid forms; Cathedral may have skeletal / construct forms)
- **Carry visual-register coherence** (per `enemy-visual-legibility.md` + `style-register.md` — sprite-archetype tags + element palette + aura class all support the cosmological register)

**Example:** Yomi's monsters might include shadowed-form swarms; bound-spirit elites; pomegranate-myth-resonant bosses. The Yomi register pulses through tier-by-tier.

**Failure mode:** monsters are tier-stat-blocks with seasonal-color-tints; the world's predators don't read as *of* the world.

### D5 — Trial-boss identity (each season's three culminations)

The three Trial bosses (one per act) are the season's structural pivots (per `trial-moment-ritual.md`). They should:

- **Each be a distinct character within the season's cosmology** (not three-similar-fights; three-distinct-encounters)
- **Build in cosmological weight across the acts** (Act 1 Trial introduces the season's register; Act 3 Trial culminates it)
- **Be embodiment-diverse where appropriate** (the season's three Trials may include humanoid, non-humanoid, hybrid embodiments — per the season's cosmology's breadth)
- **Carry per-season Trial-variant naming** (per `naming-triad.md` per-season vocabulary — Yomi's *The Threshold-Test*; Deep Trench's *The Sounding*)

**Example:** Yomi's three Trials could be: Act 1 *The Boundary-Walker* (a guardian of the threshold; introduces Yomi's liminality); Act 2 *The Bound-One* (one who has eaten the pomegranate; demonstrates the cosmology's cost); Act 3 *Izanami-Echo* (the cosmological mother-shadow; ultimate culmination).

**Failure mode:** three Trial bosses with the same shape (all humanoid; all using similar kits; differentiated only by stat-tuning). The act-end-encounter rhythm doesn't build cosmological weight.

### D6 — Gear texture (generated gear flavor coherent with the season)

Generated gear (especially epic+ tiers; rare-tier template-named per LLM cost optimization) should:

- **Carry seasonal vocabulary naturally** (Deep Trench's *Thrumming Trench Caller*; Yomi's *Pomegranate-Stained Mantle* register)
- **Read as artifacts OF the cosmology** (not generic items with seasonal-flavor-prefixes; items the world would actually have)
- **Connect to specific cosmological elements** (the Cathedral's gear references its bone-architecture; Yomi's gear references its threshold-mythology)
- **Per the locked style register** (HD-2D pixel hand-drawn; visual-prompt fields per file 19 § Phase 02 produce gear images consistent with the register)

**Example:** Deep Trench gear from family-review: *Thrumming Trench Caller* (weapon), *Pitchthrum Abyssal Orb* (off-hand), *Thrumwarden's Basalt Robe* (armor), *Thrumming Trench Band* (accessory). The seasonal vocabulary (*pitch*, *brine*, *thrum*, *basalt*) appears across the gear naming pipeline.

**Failure mode:** gear names use seasonal-element words but feel like a template (`<adjective> <material> <slot> of <element>`) without the cosmological grounding that makes them feel like *things from this world*.

### D7 — Music register (per-season-themed music)

Per file 28 + demo1's per-season music implementation: each season has its own themed music. The music should:

- **Cohere with the anchor's cosmological register** (Deep Trench's music is *deep*, *resonant*, *under-pressure*; Yomi's music is *ritualistic*, *threshold-coded*, *ancestor-presence*)
- **Build across the season's arc** (Act 1 music can be more reserved; Act 3 climactic Trial music can intensify; Ascension music transitions to Earth Self register universal track per ascension-moment-ritual.md Phase 1)
- **Match the locked visual register** (HD-2D pixel — chiptune-with-orchestration is the genre's matching audio register; not anime-cel orchestral; not synthwave; specific to the locked visual aesthetic)
- **Carry the Wheel's signature event at Ascension Phase 3** (per ascension-moment-ritual.md — the strongest cosmological-aura event has a unique musical signature)

**Example:** Yomi's music register includes shakuhachi-coded sparseness; ritual-percussion at Trial-encounters; threshold-resonance at the cinematic frames; pomegranate-myth-evoking tonal patterns where appropriate.

**Failure mode:** music is generic ARPG-orchestral with seasonal-flavor-instrumentation overlay; the cosmology doesn't infuse the audio register.

### D8 — Visual palette modulation (per-season palette within locked register)

Per `style-register.md`'s HD-2D pixel hand-drawn locked register: per-season visual palette modulates this register WITHIN consistency. Each season's:

- **Primary palette** reflects the cosmological register (Deep Trench's blacks-and-pressure-blues; Yomi's reds-and-shadows; Cathedral's bone-whites-and-decay-greys)
- **Element-coded palettes** (per enemy-visual-legibility.md § S2) modulate consistently per the season's elemental flavors
- **Tier-aura color signatures** (per enemy-visual-legibility.md § S3) carry the season's palette modulation
- **Trial-encounter cinematic-tier aura signatures** carry per-season distinctiveness (per ascension-moment-ritual.md Phase 3 + enemy-visual-legibility.md § S4)
- **Spirit Guide partial-presence rendering** stays consistent across seasons (per spirit-guide-voice.md — the Guide is constant) but the ambient palette around the Guide modulates per season

**Failure mode:** every season looks the same (same palette across all anchors); the visual variety lives only in the specific sprite-asset selection, not in palette-coherence.

### D9 — Spirit Guide season-acknowledgment

Per `spirit-guide-voice.md`: the Spirit Guide is constant across seasons, but the Guide's voice ACKNOWLEDGES each season's particular cosmology. This is a structural way the season's distinctiveness reaches the player.

- **Spirit Guide voice lines within the season** consume the season's seasonal vocabulary naturally (*"The Sounding waits at the end of this descent"* — Deep Trench; *"The Threshold-Test awaits, Aiden. Yomi has been long-watching"* — Yomi)
- **Spirit Guide Court-references in subsequent seasons** acknowledge specific prior-season cosmologies (*"The Lantern-Keeper of Yomi's Winds saw places like this; the threshold-register holds here too"*)
- **Spirit Guide journey-trajectory acknowledgments** reference the season's specific shape (path-taken at Trials; Passages encountered; Court-state)

**Failure mode:** Spirit Guide voice is constant across seasons in EVERY sense — same phrases at same moments; no cosmology-specific acknowledgments; the Guide doesn't notice what season they're walking with the player.

### D10 — Narrative through-line (the season's emotional shape)

Even without explicit quest content (Phase 0 doesn't have Engine 2 quest infrastructure yet), each season should carry a **felt emotional shape**. This is the *"what happened to me this week"* register from a player's after-session reflection.

The shape emerges from:

- **The journey-trajectory** (which Trials were Body-swap-path vs Mirror-path; what Passages were encountered; what form ascended)
- **The cosmological register pulsed through every moment** (D1-D9 cohering)
- **The Spirit Guide's voice arc across the season** (reserved → warmed → companion per spirit-guide-voice.md)
- **The Ascension's specific resolution** (the form-ascended carries the season's mark)
- **The seasonal-vocabulary moments** (the player's first Trial choice in Yomi vocabulary; the Passage's pomegranate-eating moment if encountered; the Ascension's Earth Self register departure from seasonal vocabulary)

**Example shape:** "My Yomi season was the descent where I refused the Pomegranate at the second Passage and took the Body-swap path at the third Trial. The Lantern-Keeper ascended; the cosmology held me to my choices."

**Failure mode:** seasons have all the surface-level distinctiveness (D1-D9 intact) but lack felt-shape — the player can't articulate what *kind of journey* this season was. The season was *content*; not *experience*.

---

## Cross-season distinctiveness vs cross-season recognizability

The rubric balances two competing requirements:

**Cross-season distinctiveness** — each season feels like *its own thing* (the load-bearing claim of the pitch's meta-measure).

**Cross-season recognizability** — the player learns the universal frame across seasons and recognizes Reincarnated as a *coherent project*, not a series of disconnected procedural exercises.

What stays consistent across all seasons (cross-season recognizability):

- **The cosmology's three named actors** (Wheel; Earth Self; Spirit Guide) — these are universal
- **The naming triad universal frame** (Trial / Mirror / Passage; per `naming-triad.md`) — these are universal in operational labels; seasonal variants surface in flavor
- **The visual style register** (HD-2D pixel hand-drawn; per `style-register.md`) — locked across all seasons
- **The Spirit Guide voice register** (Beatrice-shaped; per `spirit-guide-voice.md`) — the Guide is constant
- **The Court's structural shape** (per `court-of-forms.md`) — universal across seasons
- **The Ascension's Earth Self register** (per `ascension-moment-ritual.md`) — the threshold-back-to-Earth uses universal language
- **The meaning-of-the-arc statement** (per cosmology-reincarnated.md + court-of-forms.md) — the answer to "what does winning mean" is consistent

What varies across seasons (cross-season distinctiveness):

- **The cosmological register** (D1)
- **The elemental palette** (D2)
- **The class roster** (D3)
- **The monster register** (D4)
- **The Trial-boss identities** (D5)
- **The gear texture** (D6)
- **The music register** (D7)
- **The visual palette modulation** (D8)
- **The Spirit Guide's season-acknowledgments** (D9; the Guide is constant; what they acknowledge varies)
- **The narrative through-line** (D10)

**The balance produces** an experience where the player recognizes Reincarnated immediately upon return (universal frame anchors them) AND experiences each new season as a genuine descent into different cosmology (the ten dimensions cohere).

This is analogous to **Diablo's structural recognizability** (Tristram-shaped opening + town-act-dungeon-boss rhythm + Deckard-style mentor presence) AND **Diablo's act-distinctiveness** (each act is its own thematic place). Both at once. Both load-bearing.

---

## Worked examples — what coherence looks like

### The Yomi season

Per the pitch one-pager + naming-triad worked examples + family-review patterns:

| Dimension | Yomi-coherent expression |
|---|---|
| D1 Cosmological register | Liminality; binding-via-consumption; underworld-presence; Shinto-Buddhist mythological substrate |
| D2 Elemental palette | (Per anchor-specific generation) — Yomi vocabulary that visualizes underworld register |
| D3 Class roster | Threshold-Keepers, Bound-Ones, Shadow-Walkers (illustrative) — humanoid AND non-humanoid embodiment variety where the cosmology admits |
| D4 Monster register | Shadowed forms; bound spirits; ancestor-echoes; threshold-guardians |
| D5 Trial bosses | Act 1 *The Boundary-Walker*; Act 2 *The Bound-One*; Act 3 *Izanami-Echo* (illustrative) |
| D6 Gear texture | *Pomegranate-Stained Mantle*; *Threshold-Bound Charm*; *Bound-Soul Sigil*; *Underworld-Forged Implement* — names that read as artifacts OF Yomi |
| D7 Music register | Shakuhachi-coded sparseness; ritual-percussion; threshold-resonance |
| D8 Visual palette modulation | Reds-and-shadows; pomegranate-color highlights; threshold-light-and-dark contrasts |
| D9 Spirit Guide acknowledgment | *"The Threshold-Test awaits, [Earth Self name]. Yomi has been long-watching"* (Trial Phase 2); *"You stand near the Pomegranate, [Earth Self name]"* (Passage approach if encountered); *"The descent through Yomi is complete"* (Ascension Phase 2) |
| D10 Narrative through-line | The Yomi season's emotional shape: *"the descent into the place where the dead are bound; the choice at each threshold; the form that returns marked by Yomi's liminality"* |

**Why Yomi works as a worked example:** the cosmology is mythologically dense (Izanami's pomegranate myth is *the* binding-of-souls-via-food story); the Passage analog is verbatim cosmological resonance (eating the pomegranate IS the Passage Accept); the threshold mythology pulses through every dimension naturally.

### The Deep Trench season (existing production season 001001)

Per family-review + decisions-log:

| Dimension | Deep Trench-coherent expression |
|---|---|
| D1 Cosmological register | Lightless depths; pressure; abyssal otherness; the-place-where-light-has-never-reached |
| D2 Elemental palette | *pitch* (fire) / *brine* (water) / *thrum* (wind) / *basalt* (earth) — all visualizable; all anchor-coherent; *thrum* was a known weakness (per decisions-log D1 work) |
| D3 Class roster | *Trenchwind Pitch-Caster*, *Trench-Breathed Tidecaller*, *Abyssal Basalt Monk* — all humanoid (form-bias surfaced by doc 37); the cosmology admits much richer non-humanoid expression |
| D4 Monster register | Abyssal aberrants; pressure-formed predators; lightless-cave swarms |
| D5 Trial bosses | (Generated per season — *Trench-Breathed Tidecaller* was an act-boss in production; others per the specific roster) |
| D6 Gear texture | *Thrumming Trench Caller*, *Pitchthrum Abyssal Orb*, *Thrumwarden's Basalt Robe*, *Thrumming Trench Band* — seasonal vocabulary infuses naming |
| D7 Music register | Deep resonance; under-pressure pulse; abyssal-distance reverb |
| D8 Visual palette | Blacks; pressure-blues; bioluminescent accents (where cosmology admits); contrast between lightlessness and revealed-presence |
| D9 Spirit Guide acknowledgment | *"The Sounding waits at the end of this descent"* (Trial Phase 2); seasonal-vocabulary-natural references throughout |
| D10 Narrative through-line | The descent INTO the lightless; the discovery of what lives there; the choice to bring back or be bound; the Sounding as culmination |

**What's strong:** elemental palette + gear texture + naming integration (the seasonal vocabulary pulses naturally through downstream content). **What's weak:** D3 class roster is humanoid-only; D4 monster register details are unverified; D9 specific Spirit Guide acknowledgment phrasings need pass-through review.

### The Cathedral of Bone season (existing production season 001003)

| Dimension | Cathedral-coherent expression |
|---|---|
| D1 Cosmological register | Death-architecture; ossuary; the cathedral built FROM what was once living; sanctity-of-decay |
| D2 Elemental palette | *torch* (fire) / *milk* (water — known weakness per D1) / *breath* (wind) / *bone* (earth) — *milk* is the documented failure case; *bone* is strong |
| D3 Class roster | Various Cathedral-themed classes — humanoid-only in current production |
| D6 Gear texture | Bone-mantled / ossuary-bound / cathedral-marked items |
| D9 Spirit Guide acknowledgment | *"The Marrow-Test waits; the Cathedral does not forget the living"* (Trial Phase 2 illustrative) |
| D10 Narrative through-line | The descent into the cathedral-of-the-dead; the encounters with what-remains; the return |

**What's a known weakness:** *milk* fails as water-flavor (per decisions-log). This is the canonical example of D2 elemental-palette failure mode used throughout file 28 § D1 design discussions.

---

## How LLM generation honors this rubric

Per file 19 § Phase 02 + the per-season cosmological-vocabulary call architecture (per naming-triad.md § "Generation integration"):

**The per-season cosmological-vocabulary LLM call should include this rubric's dimensions as prompt context.** Specifically:

- The anchor + anchor description (D1 cosmological register seed)
- The Primary / Secondary opposition labels per doc 37 § 6 cipher (D2 elemental palette substrate)
- Instruction to generate naming-triad variants per `naming-triad.md` (D5 Trial-boss + D9 Spirit Guide acknowledgment ground)
- Instruction to generate the per-season cosmological flavor for downstream consumers

**Subsequent LLM calls within the season** (class naming, skill naming, monster naming, trial-boss naming, gear naming, Spirit Guide voice generation) consume the per-season cosmological vocabulary as prompt context. The rubric's coherence emerges from each downstream LLM call faithfully consuming the cosmological seed.

**The Discipline #14 candidate anti-bias scaffolding** applies to ALL these LLM calls:
- No canonical-four element labels in LLM-visible prompts
- No class-archetype labels in LLM-visible prompts  
- No mechanical-property names in LLM-visible prompts
- No attribute axis labels in LLM-visible prompts
- Per-season vocabulary AND embodiment-narrative-layer vocabulary AND the season-feel rubric's cosmological seed are the LLM's working vocabulary

**Quality gates against this rubric:**

When a season has been generated, before it ships (to demo, to family playtest, to production), it can be reviewed against the rubric:

- Does the elemental palette cohere with the anchor? (D1 × D2)
- Does the class roster read as inhabitants of THIS cosmology? (D3)
- Are the Trial bosses distinct characters within the season's cosmology? (D5)
- Does the gear texture read as artifacts OF the cosmology? (D6)
- Do the Spirit Guide voice lines reflect this season's cosmology? (D9)

These are categorical-design-criteria; the answer is yes / needs-revision / no. Family-playtest review consumes this rubric implicitly (the playtester's *"this season feels coherent / this season feels generic"* response is the rubric's primary validation surface).

---

## Reverse-validation — the convergence-pattern applied to D1

The rubric's forward flow is *anchor → cosmological vocabulary → D2-D9 content*. **Reverse-validation** asks the inverse: given a generated season's D2-D9 content, what cosmological register (D1) does an independent LLM-as-observer derive from the sum? The technique is two-variant, and each variant serves a distinct diagnostic purpose.

**Architectural grounding.** This applies the project's existing convergence-pattern (decisions-log 2026-05-07: *"Multiple downstream consumers... each transform the math engine's specifications independently. Quality is measured by their cross-consumer coherence"*) to D1 specifically. The reverse-test adds a new convergence consumer — the **LLM-as-cosmological-observer** — whose independent transformation should converge with intended cosmology if cross-dimensional coherence is real.

### Variant 1 — Seeded reverse-test (ongoing quality gate)

**Setup:** generate a season with anchor-driven cosmological seed (the standard forward flow). Run a separate, context-isolated LLM call that ingests only the generated D2-D9 content (the JSON output, not the generation prompt). Ask the observer LLM to articulate the cosmological register it observes.

**Outcomes:**

- **Reverse-derived D1 closely matches seed-D1.** The pipeline preserves cosmological intent. Healthy.
- **Reverse-derived D1 differs from seed-D1 but is internally coherent.** The pipeline produces coherent content but the cosmological register drifts during generation. Designable signal — drift may be acceptable (emergent better-than-seed identity) or problematic (anchor's intent not honored).
- **Reverse-derived D1 is incoherent.** The pipeline produces technically-varied but cosmologically-flat content. Cross-dimensional-flatness failure detected.

**Operational use:** pre-flight quality gate before a season ships to demo / family playtest / production. Cheap (~$0.10-1.00 per reverse-test); catches failure modes the per-dimension checks miss.

### Variant 2 — No-seed reverse-test (one-time architectural prototype)

**The more rigorous form, per Matt's sharpening 2026-05-16.** Setup: run the generation pipeline **without** anchor-driven cosmological seed. Only the abstract pair-structure cipher (per doc 37 § 6) and maximum anti-bias scaffolding are provided. Generate D2-D9 from this minimal input. Reverse-derive D1 from the result.

**This is not validation; it tests an architectural claim.** Does the engine *generate* a coherent cosmology without one, or does it only *amplify* a seed?

**Outcomes:**

- **Outcome 1 — Coherent cosmology emerges.** The cipher + dimensional generation + per-season LLM call together constitute **an engine for novel cosmological invention.** Not a cosmology-amplifier; a cosmology generator. This is a substantially stronger architectural claim than the current framing admits, with real implications for licensing positioning (per `engine-generic-meta-structure.md`).
- **Outcome 2 — Cosmology-amplifier confirmed.** Without seed, nothing coherent emerges. The current framing is correct; the seed is load-bearing; licensees author their own L2 cosmology.
- **Outcome 3 — Training-default leakage.** The reverse-derived cosmology reads as generic-fantasy / Western-mythological-default. The cipher's anti-bias scaffolding isn't doing its job without the seed reinforcing it. This is the failure mode `canonical/37-form-bias-diagnosis-and-recovery.md` § 6.5 explicitly named as a **high-stakes open question requiring empirical prototyping.**

**This variant IS the empirical resolution to doc 37 § 6.5.** Not approximated; literally the prototype that doc 37 named as needing. One of the few project-wide opens where a single experiment directly answers the question.

### Implementation requirements for both variants

- **Context isolation.** The observer LLM call must not share context with the generator LLM calls. Separate API calls; JSON output only (not the generation prompts); ideally a different LLM model entirely for strongest independence.
- **Anti-bias scaffolding in observer prompt.** The reverse-prompt must apply Discipline #14 candidate anti-bias scaffolding — no canonical-four labels, no archetype labels, no mechanical-property names. The observer must work from per-instance vocabulary and content only.
- **Structured output.** Reverse-derived D1 should include: (a) a short cosmological articulation paragraph; (b) key cosmological-register keywords; (c) comparison to common world-mythology frameworks (samsaric / Egyptian transit / Norse / Aztec / cosmic / etc.) for cross-checking coherence.
- **Categorical-diagnostic, not quantitative.** Per the rubric's general stance, outcome categories (matches-seed / drifts-coherently / drifts-incoherently / training-default-leak) are the right grain. Not a 0-100 score.

### What both reverse-tests unlock

1. **Pre-flight quality gate against the rubric** (Variant 1 ongoing): cheaper than family-playtest; catches cosmological drift early.
2. **Architectural claim validation** (Variant 2 one-time): resolves doc 37 § 6.5; informs engine commercialization framing; clarifies whether the engine is a generator or an amplifier.
3. **Per-season-cosmological-vocabulary call self-validation** (Variant 1 inline): the generation call could include a self-consistency loop — generate, reverse-derive, check against seed, iterate. Chain-of-thought-style consistency.
4. **Seed for `seasonal-anchor-prose-notes.md`** (Variant 1 derivative use): generate a season per anchor, reverse-derive the cosmological register, refine the LLM's articulation into permanent per-anchor notes. Accelerates the 130-anchor long-term effort from months to weeks.
5. **Creative iteration** (Variant 1 emergent use): when the reverse-derived D1 exceeds the seed-D1 in richness or specificity, that's information worth capturing. Update the anchor library; let seasonal generation enrich anchors over time.
6. **Divergence-floor measurement** (cross-test): two seasons whose reverse-derived D1s read as the same cosmology are below the divergence floor (per engine-balance-stewardship Gate 2, forthcoming). The reverse-test becomes part of the cross-season-distinctiveness measurement framework.

### Cross-seam implementation scope

This requires:

- **Rocket dispatch:** configure the generation pipeline to support a no-seed mode (empty / abstract-only cosmological seed input) for Variant 2 runs.
- **Star-lord dispatch:** author the observer LLM call template; integrate context-isolation + anti-bias scaffolding; structured output spec; cost-tracking.
- **Gandalf review:** evaluate reverse-derived output against the outcome categories; flag drift; recommend revision or acceptance.
- **Decisions-log entry on Variant 2 results:** the no-seed experiment's findings resolve doc 37 § 6.5; the resolution becomes a project-wide locked answer.

A commission request for the Variant 2 experiment is filed at `agentic_orchestration/gandalf/requests/2026-05-16-no-seed-cosmology-generation-test.md` (parallel to the Elrond catalogue-rubric commission). The experiment is parked as **not urgent**; captured for the right moment when capacity allows.

---

## Failure modes to protect against

In addition to per-dimension failure modes named above:

### Cross-dimensional flatness

All ten dimensions individually adequate but none deeply coherent. The season passes a per-dimension check but lands as procedurally-correct-but-soulless. Indicator: family-playtest response *"it was fine, I guess"*.

**Protection:** the season-feel review should evaluate *the experience of the season as a whole*, not just per-dimension checkboxes. If the per-dimension reviews all pass but the season-as-experience doesn't land, the seed cosmological register (D1) probably needs revision — the upstream root of coherence is the anchor.

### Genre-default leakage despite cipher

Per doc 37 § 6.5 (high-stakes open): even told *"two opposition pairs for [non-Earth-fantasy] cosmology, do not echo Earth-realm classical elements"*, the LLM may still reach for fantasy analogs. Indicator: a season's generated content reads as *generic-fantasy-with-seasonal-relabeling* rather than as *genuine-different-cosmology*.

**Protection:** anti-bias scaffolding per Discipline #14 candidate; pre-flight LLM call validation; structural enforcement at the prompt-template layer.

### Cross-season homogeneity in roster

Different anchors but procedurally-identical class roster shapes. Every season has roughly 5-6 humanoid classes with element distributions; the procedural skeleton shows through.

**Protection:** the embodiment axis (per `embodiment-narrative-layer.md` + doc 37 § 4) admits non-humanoid forms; the season's cosmology should drive embodiment selection (Deep Trench admits aquatic non-humanoid; Cathedral admits skeletal-construct non-humanoid; Yomi admits shadow-form non-humanoid). The rocket dispatch for embodiment-axis implementation work should consume this rubric's D3 expectation.

### Music + visual + naming three-way mismatch

The season's music is one register; the visual palette is another; the named content is a third. Multiple consumers each go their own way, and the season feels patchwork.

**Protection:** the per-season cosmological-vocabulary LLM call's output is the SHARED seed across all consumers — music sourcing, visual palette modulation, naming pipeline, Spirit Guide voice generation. One source, many consumers. Discipline #13 application at the inter-dimensional coherence layer.

### Player-experience flatness despite all upstream coherence

The hardest failure mode to diagnose. Every dimension passes; the seed cosmology is rich; the consumers all align. Yet the season doesn't feel distinct to the player.

**Protection:** family-playtest is the primary validation. If multiple playtests register *"the season felt generic despite the cosmological coherence"*, the design intent itself may have a gap — possibly the season's emotional shape (D10) didn't crystallize at design time, only at consumption time. Authoring `seasonal-anchor-prose-notes.md` (work queue item #12; long-term effort) for each anchor with explicit *"what does a season here FEEL like"* notes preempts this failure.

---

## Open questions

These do not block the canonical lock. They surface during implementation.

### Q1 — Quantitative rubric for automated quality gate

The rubric as authored is categorical-design-criteria; it does not produce a score. Should there be a quantitative rubric (per-dimension 0-N score; threshold-based ship/no-ship gate)? My instinct: **no, not at canonical-story-doc level.** Quantitative rubrics drift toward Goodhart's law; the categorical-design-criteria preserve human-design-judgment as the primary gate. If quantitative metrics are needed at engine telemetry level (for cross-season analytics; for v0.7-encounter-analytics integration), they live in engine-side telemetry schema, not in this canonical-story doc.

### Q2 — Anchor library expansion and review

The 130-entry anchor library is curated; each anchor's cosmological register is more or less locked at curation time. Open: do anchors get explicit `seasonal-anchor-prose-notes.md` (work queue #12) entries that articulate the cosmological register for downstream LLM consumption? My recommendation: **yes**; the long-term effort is worthwhile because each anchor's notes become reusable prompt context. The 130 entries can be authored incrementally across many sessions.

### Q3 — Cross-season-recognition register thresholds

How much should subsequent seasons in a player's playthrough reference earlier seasons (via Spirit Guide Court-reference register, per spirit-guide-voice.md § "The Court-reference register")? Too little: each season feels disconnected. Too much: the seasons all reference each other constantly and the cross-season recognition drowns out cross-season distinctiveness. My instinct: **sparing references** — once or twice per season, at moments where the reference deepens the moment.

### Q4 — Rubric pre-flight vs post-flight review

Should the rubric be applied pre-flight (during LLM generation, as a quality gate before the season ships) or post-flight (after generation, in family-playtest review)? My instinct: **both, with different rigor.** Pre-flight: structural checks on D2 elemental palette + Discipline #14 anti-bias scaffolding. Post-flight: holistic season-feel review including D10 emotional shape. The pre-flight catches mechanical-coherence failures; the post-flight catches experiential failures.

### Q5 — Worked-example development pace

The doc has worked examples for Yomi + Deep Trench + Cathedral-of-Bone (briefly). The other production seasons (Crypt of First Saint; Throne Room of Mad King; Ghost Town of Gold Strike) don't have worked examples here. Open: does each season need a worked example in this doc, or do worked examples emerge in `seasonal-anchor-prose-notes.md` per-anchor? My instinct: **worked examples in seasonal-anchor-prose-notes.md per anchor.** This doc names the rubric; the per-anchor doc instantiates it for each specific anchor. Reduces doc-bloat here; gives anchor-specific work its own surface.

---

## What this doc DOESN'T do

- **It does not specify per-anchor cosmological-register content.** That's `seasonal-anchor-prose-notes.md` territory (work queue #12).
- **It does not specify the engine's per-season generation pipeline implementation.** That's rocket / star-lord engine territory.
- **It does not specify quantitative-metric quality gates.** Per Q1.
- **It does not specify Engine 2 quest content's contribution to season-feel.** Engine 2 is future work; quest content will add a D11+ dimension when it ships; this doc is Phase-0-shippable scope.
- **It does not specify music sourcing or audio-asset acquisition.** D7 names the register; audio work specifics are out of scope.
- **It does not enforce the rubric via process gates.** The rubric is design-intent; process enforcement (where it lands) is jack-ryan + knight-rider Gate-1 territory.

---

## Cross-references

- `cosmology-reincarnated.md` — the cosmology this rubric operates within
- `naming-triad.md` — D5 + D9 dimension's per-season vocabulary mechanism
- `embodiment-narrative-layer.md` — D3 + D4 dimensions' embodiment variation support
- `style-register.md` — D8 dimension's locked register the palette modulates within
- `spirit-guide-voice.md` — D9 dimension's Guide-acknowledgment register
- `enemy-visual-legibility.md` — D4 + D8 dimensions' implementation surface
- `engine-generic-meta-structure.md` — the L1/L2/L3 layer separation; this doc operates at L3-per-season layer with L2 cosmology grounding
- `court-of-forms.md` — cross-season meta-progression context this rubric serves
- `trial-moment-ritual.md` + `passage-moment-ritual.md` + `ascension-moment-ritual.md` — ritual moments consume the rubric's per-season cosmological grounding
- Doc 37 § 6 — cipher architecture; the mechanism for cross-season distinctiveness
- File 28 § D1 — element-name rubric (subset of D2 dimension)
- File 29 § "Cross-season meta-progression" — the meta-measure the rubric serves
- `pitch-2026-05-18/talking-point-distillations.md` — the pitch's "depth of the Court" claim presupposes this rubric

**Forthcoming (consumed by this rubric):**
- `seasonal-anchor-prose-notes.md` (work queue #12) — per-anchor cosmological-register notes; instantiates this rubric per anchor
- `engine-balance-stewardship.md` (forthcoming) — engine-balance decisions grounded in this rubric's "what kind of seasons are we balancing for?" answer

---

## Maintenance protocol

When new canonical design docs reference season-feel:

1. Reference this doc.
2. Use the ten dimension framework; do not invent parallel-dimensional framings.
3. Per-anchor specifics live in `seasonal-anchor-prose-notes.md`, not in this doc.

When the LLM-generation pipeline ships new per-season cosmological-vocabulary calls:

1. The prompt template consumes this rubric's dimension expectations.
2. Anti-bias scaffolding (Discipline #14 candidate) enforced.
3. Outputs are reviewed against D1-D10 coherence pre-flight.

When family-playtest surfaces season-feel drift:

1. Diagnose against the ten dimensions.
2. If a dimension is structurally insufficient, file an amendment.
3. If the cosmological seed (D1) was thin at generation, refine the per-anchor cosmological-register articulation (`seasonal-anchor-prose-notes.md`).

When new dimensions emerge from playtest / design conversation:

1. Append D11+ entries (don't renumber existing dimensions).
2. Cross-reference the new dimension throughout consuming docs.
3. Update the LLM prompt templates that consume the rubric.

— gandalf, with Matt's standing approval on the rubric framework + the canonical patterns this doc consumes (2026-05-16)
