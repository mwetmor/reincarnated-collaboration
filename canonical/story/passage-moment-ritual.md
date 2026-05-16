# The Passage Moment — Ritual and Presentation

**Status:** **Canonical.** Authored 2026-05-15 by gandalf as the companion ritual doc to `trial-moment-ritual.md`. Captures the presentational design intent for the Passage — the offered crossing at death — the harsh-moment counterpart to the Trial's dramatic-core.

**Why it exists:** `trial-moment-ritual.md` canonicalized the joyful/dramatic ritualization. The Passage requires equal canonical treatment for the opposite-register moment. Without parallel design intent at both ritual surfaces, the Passage drifts toward "generic ARPG death-penalty" rather than landing as "the Wheel's harshest mechanic." Discipline #13 application at the Passage layer.

**Companion docs:**
- `trial-moment-ritual.md` — the joyful-ritual sibling; this doc deliberately mirrors its six-phase structure with tonal inversion
- `cosmology-reincarnated.md` § "The Passage" — the cosmological frame; particularly the lock that *"the Spirit Guide is visibly absent at the Passage"*
- `naming-triad.md` — Trial / Mirror / **Passage** with per-season vocabulary variation
- `enemy-visual-legibility.md` § S4 (cinematic frame) — the cinematic-tier visual treatment register
- `embodiment-narrative-layer.md` § "Injury / death vocabulary" — per-form death-collapse language consumed at Phase 4
- `style-register.md` — HD-2D-pixel locked register; narrative-moment-tier fidelity for the cinematic frame
- `gandalf-design-lineage.md` Layer 2 (Diablo death patterns) + Layer 4 (Hades "you died" return + Souls bonfire pattern)

**Pending:**
- knight-rider to draft a decisions-log entry capturing the Passage-moment-ritual canonical lock (per ADR-002; cross-seam — drax demo work + star-lord LLM voice-line generation + possibly rocket engine emits for Passage trigger flags + pool-state surface)

---

## What this doc is

This doc captures **presentational design intent** for the Passage — the moment offered when the Earth Self's seasonal form reaches HP=0 (per file 32 § Section 9; file 33 § "Death penalty model"). Mechanical substrate is locked elsewhere; this doc operates one layer up to specify how the moment is *delivered*.

**It is not** a mechanical spec. Mechanics live in file 32/33: refuse → respawn + 5-10% XP loss; accept → transform into a different form from the body-swap pool, current form permanently lost for the season + cannot ascend to the Court. Pool dynamics: pool ≥ 2 multi-choice; pool = 1 single-choice; pool = 0 only refuse-respawn available.

**It is not** an implementation spec. Drax's eventual demo work produces the implementation; this doc is the design-intent target.

---

## The Passage vs the Trial — paired but distinct rituals

| Axis | The Trial | The Passage |
|---|---|---|
| **Frequency** | Planned (3 per season; predictable at act-end) | Unplanned (any time HP→0; potentially never; potentially multiple) |
| **Tone** | Ritualized dramatic core | The Wheel's harshest mechanic |
| **Player agency** | High — chose path proactively at Phase 3 | Forced-choice — cannot avoid the moment; can only refuse the Accept option |
| **Spirit Guide** | Speaks ONE line at threshold; ONE at resolution; bears witness during fight | **Visibly absent at threshold and choice.** Returns AFTER the choice is committed. Speaks ONE line at Phase 5 |
| **Choice weight** | Future-trajectory choice (which class identity I become) | Cost-of-failure choice (which form I abandon) |
| **Reward shape** | Net positive (XP, resistances, SP, transformation) | Either small penalty (refuse) OR real permanent cost (accept) |
| **Visual register** | Cinematic encounter ritual; trial-boss approach; bright cinematic-tier aura | Death scene; pause; offered crossing; harsher register; Wheel's signature aura |
| **Music register** | Trial-specific track; deliberate, building | Passage-specific track; suspended, grieving |
| **Genre precedent** | Hades boon offer; Souls fog-gate | Souls bonfire (refuse) / Hades "you died" return (accept-as-progress) |
| **Cosmological actor foregrounded** | The trial-boss / the Mirror (mechanism-of-the-Wheel) | The Wheel itself (foregrounded by the Spirit Guide's deliberate absence) |

The two rituals are **paired** — both are pause-the-game moments with binary choice + commitment; both use cinematic-tier visual treatment; both consume per-season vocabulary variation. They are **distinct** — Trial is reverence; Passage is consequence.

---

## Why the Passage is load-bearing

The Passage is **the moment of the Wheel.** Throughout the rest of the game, the Wheel is offstage — felt in structure, never named in dialogue. The Passage is when the Wheel surfaces; not by speaking (the Wheel never speaks); by *acting*. The Spirit Guide's absence at the Passage is the design's strongest narrative claim about cosmological agency: the Guide *cannot follow you here.* This is between you and the Wheel.

Players will encounter the Passage at varying frequencies:

- Skilled players may finish a season with zero Passages encountered. The ritual matters for them as design-known-but-experientially-rare — the kind of latent moment that *could* happen and shapes how the player feels about risk.
- Mid-skill players may encounter 1-3 Passages per season. The ritual is encountered multiple times; the second and third Passages must not degrade into routine.
- Less-skilled players may encounter many Passages, eventually reaching pool=0 state. The ritual must support repeat-encounter weight AND must handle the pool=0 edge case with comparable care.

Across all skill levels, the Passage is **the design's claim about what failure costs.** Without ritual, failure is a respawn. With ritual, failure is the Wheel acknowledging the player's mortality.

Genre precedents:

- **Souls family bonfire pattern** (per gandalf-design-lineage.md Layer 4) — the moment of death and the bonfire return are deliberately weighted; the souls-lost mechanic creates ongoing tension; the death is a structural moment, not a respawn-with-cost. The Passage's refuse-path inherits this register.
- **Hades "you died" return** (per gandalf-design-lineage.md Layer 4) — Zagreus's death is the mechanism for meta-progression; the death scene is treated with deliberate care (the Charon's-Crossing-back-to-the-House sequence). The Passage's accept-path borrows weight from this — death-as-transformation rather than death-as-failure.
- **Mushoku Tensei's continuation-of-soul** (per gandalf-design-lineage.md Layer 5) — the seriousness with which the genre treats reincarnation as soul-transit. The Passage is Reincarnated's most explicit invocation of this register; *the form is abandoned but the soul continues.*

---

## The Passage moment — six-phase sequence

Structurally parallel to the Trial's six-phase sequence. Tonally inverted. Drax's implementation should treat these as locked phases; the player progresses through them linearly.

### Phase 1 — Death-approach

The player's HP drops critically. What changes:

- **HP-low visual alarm** (genre-standard; not a Passage-specific addition; UI surfaces existing health-warning patterns)
- **Subtle ambient shift in the last few seconds** — color desaturation begins at the screen edges; ambient audio dampens; the world *notices* the impending death. This is the Wheel beginning to lean in.
- **Music shift** — the combat music's intensity attenuates; a lower-register Passage-specific underlay begins. Not immediately; over the last 2-3 seconds before HP=0. The transition is felt rather than announced.
- **The Spirit Guide does NOT come closer.** Throughout the rest of combat, the Guide is partial-presence at perch-distance. At the death-approach, the Guide's position holds — *the Guide does not lean in to help; the Guide remains at distance.* This is the first visual signal of what's coming.

The death-approach phase is shorter than the Trial's approach phase — 2-3 seconds rather than a deliberate walked corridor. The player has not chosen to approach this moment; the moment is approaching them.

### Phase 2 — Threshold

HP reaches 0. The death moment.

- **Combat pauses.** All NPCs freeze. The world stills.
- **The dying form is shown at center-frame.** Not a death animation playing through — the form *in the moment of falling*, held at the threshold. Embodiment-specific per `embodiment-narrative-layer.md` § "Injury / death vocabulary" (a slime *losing cohesion*; a beast *fallen*; a construct *cracked*; a spirit *fading*). The form is on the threshold but not past it.
- **A cinematic frame at narrative-moment-tier fidelity** surfaces, hand-drawn pixel, depicting the dying form. The frame is *quieter* than the Trial's cinematic frame — less aura-saturated, more contemplative. The Wheel's signature aura tints the screen edges.
- **Per-season seasonal Passage variant surfaces** in cinematic-banner — *The Sinking* / *The Pomegranate-Eaten* / *The Crossing-of-Stone* / etc.
- **The Spirit Guide is conspicuously absent.** Not partial-presence; not at perch-distance; NOT THERE. The visual space where the Guide normally appears is empty. This is the load-bearing distinction from the Trial.
- **No voice line at threshold.** The Wheel speaks in event-not-word. The silence is the speech.

### Phase 3 — The choice

Time remains paused. The choice surfaces.

**Layout (per naming-triad.md § "Where BOTH surface together"):**

```
[Seasonal variant Passage name - cinematic banner]
(The Passage)

THE WHEEL TURNS.

→ [Refuse - seasonal variant phrasing]
  (Refuse the Passage — respawn, [X]% XP loss to next level)
  [Optional: pool state surface — "Your form remains."]

→ [Accept - seasonal variant phrasing]
  (Accept the Passage — transform into [chosen form])
  This form is lost to this season. Cannot ascend.
  [Form-selection sub-UI if pool ≥ 2]
```

**Worked example for Yomi season (with pool ≥ 2):**

```
THE POMEGRANATE OFFERED
(The Passage)

THE WHEEL TURNS.

→ Refuse the Pomegranate
  (Refuse the Passage — respawn, 8% XP loss to next level)

→ Eat the Pomegranate
  (Accept the Passage — transform into [select from pool])
  This form is lost forever to this season. Cannot ascend.
```

For pool = 1: the Accept option auto-fills the one remaining form. For pool = 0: **the Accept option is not shown.** Only Refuse is available. The seasonal banner still surfaces (the moment is still ritualized), but the choice is one-option — the Wheel acknowledges; the player cannot transform; the form continues.

**Choice mechanics:**

- **Time remains paused.** No clock; no real-time pressure.
- **The Spirit Guide is still silent.** Phase 2's absence continues through Phase 3. **The Guide does not advise on the Passage. Ever.** This is the canonical lock.
- **The choice is irrevocable on commit.** No back-out; no reconsider affordance. The Trial admits reconsider because the player chose to approach the Trial; the Passage offers no such grace because the player did not choose to die. The choice IS the only agency available; it must be committed.
- **For Accept with pool ≥ 2:** a sub-selection of which form to transform into. The Court is NOT involved; this is the within-season body-swap pool, not the cross-season Court. The player chooses from the seasonal-generated forms not yet abandoned.

### Phase 4 — Transition

The choice is committed. What surfaces.

**For Refuse:**

- Brief presentational beat — 1-2 seconds.
- The dying form *recovers from the threshold* — embodiment-specific reverse-collapse animation (a slime *recoheres*; a beast *rises*; a construct *seals*; a spirit *anchors*). The form returns to the world.
- The Wheel acknowledges with a subtle environmental signal — the screen-edge tint pulses once, then fades. The Wheel has been refused.
- Respawn position resolves — last checkpoint OR Trial encounter reset (per file 33 § "Death during Trial-boss encounter"; the Trial encounter resets on death; otherwise, the player respawns at last safe state).
- XP loss surfaces — the player's XP bar visibly decrements. This is presented honestly; not euphemized.

**For Accept:**

- A more pronounced presentational beat — 3-5 seconds.
- The dying form *passes through the threshold* — embodiment-specific final-collapse animation per `embodiment-narrative-layer.md` § "Injury / death vocabulary." A slime *fully dissipates and scatters*. A beast *falls and is still*. A construct *cracks and shatters*. A spirit *fades and is unbound*. The form is gone.
- A brief ritualized darkness covers the screen — not a long cutscene; a beat. The Wheel's signature aura pulses more strongly.
- The new form arrives — the chosen body-swap target. Embodiment-specific arrival animation (a slime *coalesces*; a beast *steps forward*; a construct *assembles*; a spirit *anchors*). The new form's first ability flashes; the HUD updates; the kit/stats refresh.
- The world re-anchors — the camera adjusts; the lighting settles; the chamber resumes.
- The body-swap pool decrement is reflected in the in-game pool-status surface (a small UI element shows the pool's current state; updated visibly).

**For pool = 0 forced refuse:**

- The Refuse-only choice is committed.
- Brief presentational beat — 2-3 seconds.
- The dying form *recovers* as in standard Refuse.
- BUT: an additional Wheel-acknowledgment beat — the screen-edge aura pulses more strongly than standard Refuse. The Wheel has noted the depleted pool.
- Respawn position resolves as standard.
- XP loss surfaces.

### Phase 5 — The Spirit Guide returns

After the choice is committed and the transition completes, the Spirit Guide returns. **This is the Guide's only voice line of the Passage moment.** One line; Beatrice register; consumes the seasonal variant where natural.

**For Refuse:**
- The Guide acknowledges continuance. *"You hold."* / *"You walk this further."* / *"The form remains."* — Beatrice register; brief; warm but not relieved.
- The voice line is generated at season-build time as part of the per-season cosmological-vocabulary call OR drawn from a small template-set with seasonal variants substituted. ~3-5 variants per season to prevent repetition over multiple Passages.

**For Accept:**
- The Guide acknowledges transformation. *"A different walk now."* / *"You took the Crossing."* / *"This shape, then."* — Beatrice register; brief; recognition of the cost without judgment.
- The voice line can be generated per-form-pair (acknowledging the specific transformation) OR template-substituted with seasonal vocabulary. ~3-5 variants per season minimum.

**For pool = 0 forced refuse:**
- The Guide acknowledges the harsher state. *"The pool has thinned."* / *"Walk carefully now."* / *"The Wheel has fewer offerings."* — Beatrice register; brief; the gravity is in what's NOT said. The player understands without explanation that future deaths will not offer Accept.
- Generated at season-build as a single line OR small variant-set; this state typically occurs once per season per skill-trajectory and the line bears its weight without needing high variant count.

### Phase 6 — Aftermath

Combat resumes (if death was mid-encounter) or the next encounter begins (if death was at encounter-end).

- The seasonal arc continues.
- For Accept: the abandoned form is *gone for the season* — cannot be played again + cannot ascend to Court (per file 33). This is a permanent state change. The form is not just unavailable; it is *forfeit*. The form will never appear in the player's Court even if the player wanted to return to it; the cosmology has spoken.
- The pool-status UI surface continues to reflect the current state for the rest of the season.
- The Spirit Guide returns to standard partial-presence at perch-distance for the rest of the act/encounter. Standard combat-witnessing posture.
- No further Passage-specific UI until the next death moment.

---

## The Spirit Guide's absence — load-bearing canonical detail

This deserves its own section because it is the Passage's most distinctive narrative-design beat and the design's strongest claim about cosmological agency.

**Canonical lock (from cosmology-reincarnated.md § "The Passage"):**

> *"The Spirit Guide is absent at the Passage. This is the moment between the Earth Self and the Wheel; the Spirit Guide does not advise."*

**What this means presentationally:**

- Phase 1 (death-approach): the Guide does not move closer to help. The Guide's position holds at standard perch-distance throughout the HP-critical window. Visual signal of impending divergence.
- Phase 2 (threshold): the Guide is **not visible.** The space where the Guide normally appears is empty. This is the most distinctive visual moment in the game.
- Phase 3 (choice): the Guide is **not visible.** The choice screen does not depict the Guide. The Guide does not speak. The player is alone with the Wheel.
- Phase 4 (transition): the Guide remains absent. The transformation (or refuse-recovery) happens *without the Guide's accompaniment.*
- Phase 5 (Spirit Guide returns): the Guide reappears. One line. Continuance.

**Why this is load-bearing:**

The cosmology's three named actors are: Earth Self (yours), Spirit Guide (yours, knowing-temporally-other), Wheel (impersonal). The Spirit Guide is the player's companion through *most* of the journey. The Passage is the *one* moment the cosmology insists the player faces alone. This is the design's claim that:

- The Wheel is real, not metaphorical. It acts. The Guide cannot intercede.
- The player's agency is *theirs alone* at this moment. Even the Guide's foresight is silent here.
- The cost is real. The Guide cannot soften it; cannot advise around it; cannot witness it from inside the choice. The Guide can only acknowledge the player on the other side.

**What this protects against:**

Without this lock, every iteration of Spirit Guide voice work would naturally reach to include the Passage. *"Surely the Guide would say something at the moment of death."* No. The Guide is silent here. The silence is the design. Future LLM prompt work that generates Spirit Guide voice content **must explicitly exclude the Passage moment** from its scope. The Phase 5 return-line is the only Passage voice line the Guide speaks.

The canonical lock is enforced via the Trigger Gate-1 question (per Discipline #14 candidate from doc 37 § 9.2b):

> *"Does this Spirit Guide content speak during the Passage moment Phases 2-4? If yes, reject — the Spirit Guide is canonically silent at the Passage threshold and choice."*

---

## Pool-state sub-cases

The Passage's structure varies by body-swap pool state. Three primary states:

### Pool ≥ 2 — standard multi-choice Passage

- Refuse option always available.
- Accept option available; sub-selection of which form to transform into.
- Most common state in a typical season.

### Pool = 1 — single-choice Passage

- Refuse option always available.
- Accept option available; the single remaining form auto-fills.
- The choice text reflects this — *"Accept the Pomegranate, take the form of [the only remaining form-name]."*
- Player understands implicitly that this is their last Accept option for the season.

### Pool = 0 — forced refuse

- Per file 33: *"Pool = 0: death body-swap UI unavailable; only refuse-respawn remains."*
- The Accept option is NOT shown.
- The Refuse option IS shown — and the ritual is preserved. The cinematic frame surfaces; the seasonal Passage variant banner surfaces; the choice screen surfaces with one option.
- The Wheel's acknowledgment at Phase 4 is more pronounced (per § Phase 4 above) — the cosmology notes the depleted pool.
- The Spirit Guide's Phase 5 line acknowledges the harsher state.

### Death during Trial encounter — special sub-case

Per file 33 § "Death during Trial-boss encounter":

- Trial encounter resets on death.
- The Passage is offered as normal during the death moment.
- The Trial path choice can be re-made on retry (player can switch from body-swap-path to Mirror-path or vice versa).
- The Trial body-swap opportunity persists until the Trial is completed.

**For the Passage at Trial-death specifically:**

The Trial-death Passage has a unique cosmological resonance worth flagging. The player chose a Trial path (Body-swap or Mirror); was killed in that choice's fight; is now offered the Passage's transformation. There is something almost ironic about this — the player chose-not-to-transform at the Trial (Mirror-path) or chose-which-to-transform-to (Body-swap-path), and now the Wheel offers transformation entirely outside that choice.

The presentational treatment should honor this without overstating it. The Phase 5 Spirit Guide voice line for a Trial-death Accept can reference the recursion gently: *"You stood at one choice. The Wheel offers another."* Optional; not load-bearing; design intent for if it lands well in family playtest.

---

## Per-form embodiment-specific death language

Phase 2 (threshold display of dying form) and Phase 4 (final-collapse animation for Accept) consume `embodiment-narrative-layer.md` § "Injury / death vocabulary" canonically.

Examples (illustrative; canonical lookups in embodiment-narrative-layer.md):

| Embodiment | Phase 2 threshold posture | Phase 4 final-collapse |
|---|---|---|
| **Humanoid** | bleeding, falling, knee-bent | falls, body still, blood pools |
| **Slime** | viscosity destabilizing, surface losing tension | dissipates, scatters into droplets, unmakes |
| **Beast** | bleeding, fallen, breathing labored | falls, body still |
| **Dragonling** | wings drooping, scales cracking, bleeding | scales-crack-and-fall, body uncoils |
| **Swarm** | clusters disorganizing, lead-individual struck | scatters into individuals, queen-presence fades, the swarm depletes |
| **Construct** | panels cracked, joints misaligned | cracks open, shatters, falls-apart |
| **Spirit** | partial-presence destabilizing, edges fraying | fades, unbinds, dissipates, returns to mist |
| **Plant** | wilting, leaves browning, structure sagging | withers, breaks, dries, decomposes |

The embodiment-specific death language **gives the Passage its emotional weight per form.** A slime's *dissipation and scattering* reads differently than a humanoid's *falling and stillness*. Both are right. Both honor what the form was. The Passage's narrative power depends on this honoring.

When LLM-generated content references a Passage moment, it consumes the embodiment-specific death-language from `embodiment-narrative-layer.md` rather than reaching for humanoid-default death verbs.

---

## Per-season Passage variants

Per `naming-triad.md` § "Per-season vocabulary variation," the Passage gets a seasonal variant generated alongside the season's elemental vocabulary. The variant surfaces:

- Phase 2 cinematic banner (the seasonal Passage name as primary; universal frame in helper-text)
- Phase 3 choice screen primary labels (Refuse / Accept use seasonal phrasing)
- Phase 5 Spirit Guide voice line consumes seasonal vocabulary naturally

**Worked examples for production seasons (from naming-triad.md):**

| Season | Passage variant |
|---|---|
| Deep Trench | *The Sinking* / *The Drift-Below* |
| Crypt of the First Saint | *The Crossing-of-Stone* |
| Cathedral of Bone | *The Final-Breath* / *The Ossuary-Crossing* |
| Throne Room of the Mad King | *The Mercury-Drink* / *The King's-Mercy* |
| Ghost Town of the Gold Strike | *The Strike's-End* / *The Dust-Take* |
| Yomi | *The Pomegranate-Eaten* / 黄泉の道 |

**The Yomi Passage specifically** — per naming-triad.md, this is where the cosmological resonance is most striking. Izanami's myth: eating the food of the underworld binds the soul. The Passage = eating the pomegranate. The mechanic IS the myth. When the Yomi Passage's choice screen surfaces, the player reads *"Eat the Pomegranate. This form is lost forever to this season."* — and the cosmological resonance lands in a way no humanoid-default-"accept death body-swap"-translation could achieve.

This is the level of design the cipher architecture (doc 37 § 6) makes possible. The Passage moment is one of the surfaces where it pays off most.

---

## What this requires — cross-seam summary

### Engine (rocket / star-lord) emits

For Passage triggering:
- HP=0 trigger (existing mechanical surface)
- Pool-state surface (current pool count; per-form remaining-in-pool list for the Accept sub-selection)
- Seasonal Passage variant text (generated in the per-season cosmological-vocabulary call per naming-triad.md § "Generation integration")
- Spirit Guide Phase 5 voice lines:
  - Refuse-acknowledgment variants (~3-5 per season; consumed templatically per Passage instance)
  - Accept-acknowledgment variants (~3-5 per season; possibly per-form-pair if richer generation is opted into)
  - Pool=0-acknowledgment line (1 per season; specifically named state)
- Embodiment-specific death-language for current form + chosen-transformation form

LLM cost impact: ~5-10 additional voice lines per season; modest. Bundled into the per-season cosmological-vocabulary call.

### Demo (drax) implements

- Phase 1 death-approach signaling (HP-low alarm exists; add ambient shift / desaturation / music attenuation; Spirit Guide position holds at perch-distance)
- Phase 2 threshold routine (cinematic frame at narrative-moment-tier; dying form display with embodiment-specific posture; Spirit Guide absence; seasonal Passage variant banner; Wheel signature aura at screen-edge)
- Phase 3 choice screen UI (paused time; layout per worked example; commit-irrevocable mechanic; pool-state-aware option surfacing — pool ≥ 2 multi-choice with form sub-selection, pool = 1 auto-fill, pool = 0 Refuse-only)
- Phase 4 transition routines (Refuse: recovery + Wheel-acknowledgment pulse + XP loss surface; Accept: final-collapse with embodiment-specific death language + ritualized darkness beat + new-form arrival animation + HUD/kit update + pool decrement; Pool=0: enhanced Wheel-acknowledgment)
- Phase 5 Spirit Guide return + voice line surface (consumes engine-emitted line OR template-substitutes seasonal variant)
- Phase 6 standard combat resumption + pool-status UI persistence
- The Spirit Guide canonical-absence enforcement (no Guide rendering at Phases 2-4)

Estimated drax work: 2-3 weeks for the full Passage moment ritual implementation. Smaller than Trial moment (~2-4 weeks) because the Passage doesn't have an approach-zone architecture; it's triggered by HP=0 and unfolds in-place.

### Spirit Guide voice doc (forthcoming, work queue #3)

When `spirit-guide-voice.md` lands:
- The Passage's Phase 5 voice line specifications integrate into the voice doc's coverage.
- The voice doc must explicitly exclude Passage Phases 2-4 from the Spirit Guide's speech surface (per the canonical lock above).
- The Passage's Phase 5 line falls within the broader Beatrice arc (reserved → warmed → companion across season acts).

---

## What this protects against

- **The Passage as generic respawn.** Without ritual, HP=0 reads as standard ARPG death-with-penalty. With ritual, the moment lands as the Wheel's harshest mechanic.
- **The Accept option as free-retry-with-style.** Without ritual weight (form-lost-forever + cannot-ascend), Accept feels like a stylized respawn. With ritual weight, Accept reads as the real-cost choice it mechanically is.
- **The Spirit Guide as crutch.** Without the explicit absence at Phases 2-4, the Guide drifts into advisory-NPC register at every moment. The absence locks the design's claim about cosmological agency.
- **Pool=0 as gameplay-failure-state.** Without ritual treatment, pool=0 reads as "you broke the body-swap system." With ritual treatment, pool=0 is a meaningful cosmological state the Wheel acknowledges with extra weight.
- **Embodiment-default death animations.** Without explicit embodiment-specific death-language consumption, a slime's death and a humanoid's death would use the same fall-and-still animation. The form-specific honoring at the Passage protects the form-bias work (doc 37) at the most emotionally weighted moment.
- **Future LLM Spirit Guide voice content drifting into Passage Phases 2-4.** Trigger Gate-1 question + Discipline #14 candidate enforcement protect against silent drift.

---

## Open questions

These do not block the canonical lock. They surface during implementation.

### Q1 — XP loss specific percentage

File 33 says 5-10% XP loss to next level on Refuse. The specific value is tuning territory. Open: 5% / 8% / 10%; possibly variable per act (later acts have higher stakes). Engine-tuning question; not Gandalf-territory. Surfaces when family playtest of Passage-frequency lands.

### Q2 — Pool depletion before season-end strategic dynamic

If a player burns through their pool via multiple Accept choices, they reach pool=0 with seasonal-form-remaining and pool=0 status. From that point: any death is forced-refuse with XP loss. This creates a meaningful strategic dynamic — the player has effectively "spent" their body-swap currency and is now committed to surviving as their current form. Is this dynamic encouraged via UI surface, or left to emerge? My instinct: pool-status surface (per Phase 6) communicates the state implicitly without leaning into it as an explicit currency. Players discover the depletion's weight through play. Drax implementation choice.

### Q3 — Trial-death Passage recursion line

The optional "you stood at one choice; the Wheel offers another" Spirit Guide line for the Trial-death-Accept case (per § "Death during Trial encounter") is design-intent gesture. Worth experimenting in family playtest; can be cut if it overplays. Generation cost: one additional voice line per season for Trial-death-Accept scenarios; very modest. Recommendation: include but mark as removable.

### Q4 — Body-swap pool sub-selection UI for Accept with pool ≥ 2

When pool ≥ 2 and the player chooses Accept, they must select which form to transform into. The sub-selection UI design — does it show forms with their LLM-generated names + brief flavor + class identifier? Just names? Names + portraits? My instinct: **names + class identifier + brief flavor.** Enough information to choose meaningfully; not so much that the choice becomes a research moment. The player has been seeing these forms throughout the season (they're the season's NPCs in some sense); they should recognize them by name. Drax implementation territory.

### Q5 — Pool=0 acknowledgment in subsequent acts

Once a player reaches pool=0, the rest of the season's Passages are forced-refuse. The Phase 5 Spirit Guide line specifically acknowledging this state (*"The pool has thinned"*) is canonical for the moment pool=0 is reached. Open: should subsequent forced-refuse Passages in the same season also surface this line, or revert to standard Refuse lines? My instinct: **first pool=0 Passage gets the named line; subsequent pool=0 Passages get standard Refuse lines with a subtle reference where appropriate.** The first acknowledgment carries the weight; later occurrences don't need to re-narrate the state.

---

## What this DOESN'T do

- **It does not specify the Refuse XP-loss specific value.** Tuning territory; not Gandalf-canonical.
- **It does not specify form-pool generation specifics.** The within-season body-swap pool's contents and ordering are mechanical-engine territory.
- **It does not specify the Court entry treatment for Passage-accepted forms.** Per cosmology + court-of-forms.md: Passage-accepted forms do NOT enter the Court (cannot ascend). No Court UI treatment needed for these forms; they simply do not exist at the Earth Self's hub. This is a non-action in the Court UI, not an action requiring design intent.
- **It does not specify the ascension moment's ritual.** Ascension is the season's climax; happens once per season; deserves its own ritual doc (`ascension-moment-ritual.md`) when Court / Earth-Self hub implementation nears. Suggested addition to work queue.

---

## Cross-references

- `trial-moment-ritual.md` — the paired ritual sibling
- `cosmology-reincarnated.md` § "The Passage" — the cosmological frame; specifically the Spirit-Guide-absent lock
- `naming-triad.md` — universal frame + per-season Passage variants
- `enemy-visual-legibility.md` § S4 (narrative-moment-tier cinematic frame)
- `embodiment-narrative-layer.md` § "Injury / death vocabulary" — Phase 2 threshold posture + Phase 4 final-collapse language
- `style-register.md` — HD-2D-pixel register; narrative-moment-tier for cinematic frame
- `court-of-forms.md` — Court does NOT receive Passage-accepted forms (canonical exclusion)
- `gandalf-design-lineage.md` Layer 2 (Diablo death patterns) + Layer 4 (Hades / Souls death precedents) + Layer 5 (Mushoku Tensei continuation-of-soul register)
- File 32 § Section 9 — death penalty mechanical substrate
- File 33 § "Body-swap pool dynamics" + § "Death during Trial-boss encounter" + § "Pool depletion edge cases" + § "Death penalty model"

**Forthcoming (not yet authored):**
- `spirit-guide-voice.md` (Phase 2 work-queue #3) — the Passage Phase 5 voice line specifications + canonical exclusion of Passage Phases 2-4 from Spirit Guide speech surface
- `ascension-moment-ritual.md` (suggested addition) — the season-climax ritual; companion to trial-moment-ritual.md and this doc

---

## Maintenance protocol

When drax dispatches Passage-moment implementation work:

1. Re-read this doc with drax.
2. Convert the six phases into demo-side routines: death-approach signaling, threshold cinematic frame, choice screen UI (with pool-state branching), transition routines (per Refuse / Accept / pool=0 variants), Spirit Guide return, aftermath state persistence.
3. **Verify the Spirit Guide absence lock at Phases 2-4** in code review — no Guide rendering, no Guide voice, no Guide interaction during these phases.
4. Resolve open questions (Q1-Q5) with Matt before locking implementation details.

When spirit-guide-voice.md lands:

1. The Passage's Phase 5 voice line specifications cross-reference to that doc.
2. The canonical-absence enforcement at Phases 2-4 is reinforced in that doc's "what the Spirit Guide does NOT do" section.

When future canonical docs touch death-mechanics or cosmological-moment rituals:

1. Reference this doc.
2. The Spirit Guide canonical-absence at the Passage threshold and choice is non-negotiable.

When new embodiments are added (per embodiment-narrative-layer.md expansion protocol):

1. The new embodiment's death-language entries flow naturally into this doc's Phase 2 + Phase 4 consumption.
2. No update to this doc required; the embodiment-narrative-layer.md amendment handles it.

— gandalf, with Matt's standing approval on the canonical patterns this doc consumes (2026-05-15)
