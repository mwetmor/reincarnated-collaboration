# The Ascension Moment — Ritual and Presentation

**Status:** **Canonical.** Authored 2026-05-15 by gandalf. Third doc in the ritual trilogy (Trial / Passage / Ascension). Captures the presentational design intent for the once-per-season climax — the moment the form alive at season-end joins the Earth Self's Court.

**Why it exists:** the ritual trilogy is the project's three load-bearing player-perception moments. Without Ascension's ritual canonicalized, the trilogy is incomplete and the season's climactic moment risks shipping as a fade-to-roster-screen rather than landing as the cosmological completion it is mechanically. Discipline #13 application at the season-climax layer.

**Companion docs:**
- `trial-moment-ritual.md` — the joyful-mid-season-ritual sibling
- `passage-moment-ritual.md` — the harsh-anytime-ritual sibling; this doc completes the trilogy
- `cosmology-reincarnated.md` § "Ascension and the Court" — the cosmological frame
- `court-of-forms.md` — the Court the new form joins; C5 (accumulation is paced and commemorated)
- `naming-triad.md` — Trial / Mirror / Passage variants; this doc commits that Ascension uses Earth Self register (NOT seasonal variants)
- `embodiment-narrative-layer.md` — per-embodiment vocabulary for the form's arrival language
- `style-register.md` — HD-2D-pixel; narrative-moment-tier for cinematic ascension frame
- `gandalf-design-lineage.md` Layer 5 (Solo Leveling shadow-extraction-as-Court-arrival precedent) + Layer 4 (Hades House-of-Hades return) + Layer 2 (Diablo II act-completion register)

**Pending:**
- knight-rider to draft a decisions-log entry capturing the Ascension-moment-ritual canonical lock (per ADR-002; cross-seam — drax demo work + star-lord LLM voice-line generation + possibly rocket engine emits for path-taken-during-season metadata that informs Court entry)

---

## What this doc is

This doc captures **presentational design intent** for the Ascension — the moment that closes a Reincarnated season. Mechanical substrate is locked elsewhere (per file 32 § Section 11, file 33 § "Form library acquisition", and `court-of-forms.md` C5): **one form ascends per season — the form alive at season's end.** Forms left behind (via Trial body-swap, Passage Accept, or simply not-being-the-final-form) do not ascend.

**It is not** a mechanical spec. The "one form per season" lock, the Court entry data model, and the per-season-form-state tracking are engine territory.

**It is not** an implementation spec for the post-Phase-0 Earth-Self hub. The hub itself is post-Phase-0 work; the Ascension RITUAL canonicalized here is **the threshold event between seasonal play and the hub**. It can be implemented within the Phase 0 demo (as a season-end cutscene) before the full Earth-Self hub ships; the design intent extends forward as the hub matures.

---

## The ritual trilogy — comparison

The three moments together cover the player's full perception arc through a season:

| Axis | The Trial | The Passage | The Ascension |
|---|---|---|---|
| **Frequency** | 3x per season | 0–many per season | EXACTLY 1 per season |
| **Predictability** | High (act-end) | Triggered (HP=0) | High (season-end) |
| **Tone** | Reverence; dramatic core | Consequence; the Wheel's harshness | Culmination; cosmological completion |
| **Player agency** | High (chose path) | Forced-choice | Largely receptive (with optional contemplative gesture) |
| **Spirit Guide** | Speaks 2 lines (threshold + resolution); witnesses fight | Absent at threshold + choice; returns to speak 1 line | **Speaks 3 lines** (threshold + Court-introduction + settling); voice climax |
| **Wheel** | Acknowledges via event | Foregrounded by Guide absence | **Strongest cosmological event** of the game |
| **Earth Self** | Implicit (the persistent player behind the form) | Implicit | **Active for the first time** — receives the form by name |
| **Court** | Witnesses (offstage) | Witnesses (offstage) | **Foregrounded; grows; first appears to player** |
| **Vocabulary register** | Seasonal variants surface | Seasonal variants surface | **Earth Self register; seasonal vocabulary is LEFT BEHIND** |
| **Duration** | ~30-60s including fight | ~10-20s | **~30-60s** (longer; respects rarity) |
| **Genre precedent** | Hades boon offer; Souls fog-gate | Souls bonfire; Hades "you died" | Solo Leveling shadow-extraction-into-army; Hades House-of-Hades return; D2 act-completion |

The Ascension closes the cosmological cycle. The descent that the season-arrival began ends here; the return-to-Earth is complete; the form joins the Court; the Earth Self holds it.

---

## Why the Ascension is load-bearing

The Ascension is **the player's first encounter with the cosmology made explicit.** Throughout the season, the Wheel is offstage; the Earth Self is structural-placeholder; the Court is a future-state pointer. At Ascension, all three become *visible*:

- **The Wheel turns** — its strongest acknowledgment-event in the game
- **The Earth Self acts** — addressed by name; receives the form
- **The Court grows** — the new retainer is welcomed; existing Court members witness

This is the **only moment** in standard Phase-0 play where the cosmology's three named actors are simultaneously foregrounded. The moment must land. Without ritual, the cosmology's payoff registers as a roster-update; with ritual, the cosmology's claim about reincarnation-and-return is *experientially demonstrated.*

The Ascension is also **the player's first direct interaction with their Earth Self.** The Earth Self was named at first play (per cosmology-reincarnated.md). Throughout the season the name lives in the project's substrate. At Ascension, the player hears the Spirit Guide address them BY THAT NAME — *"Aiden, your Court grows."* This is the meta-layer becoming personal.

For first-time players: the first Ascension is also the **birth of the Court.** Special framing (per § Special cases below) honors this.

For experienced players: each Ascension is **the Court's accumulation made visible.** The new retainer joins; the Court's depth becomes the measurable thing per `court-of-forms.md` C7.

Genre precedents:

- **Solo Leveling shadow-extraction-into-army** — Jin-Woo extracts a defeated foe's shadow; the new shadow joins the army; the army is shown together. The arrival is *named.* The army acknowledges. This is the closest precedent for Ascension's Phase 4 Court reception.
- **Hades House-of-Hades return** — Zagreus returns to the House between runs; the House's residents acknowledge his return; dialogue trickles; meta-progression UI surfaces in a navigable space. This is the closest precedent for Ascension as **threshold-between-realms moment.**
- **Diablo II act-completion** — the act-ending moment in D2 (notably the Mephisto / Diablo / Baal sequence) carries weight via dialogue, music, and the world's acknowledgment. The Ascension borrows this register at season-end.

---

## Canonical commitment — Earth Self register, NOT seasonal vocabulary

The Ascension uses **Earth Self register** throughout. The seasonal vocabulary (per `naming-triad.md` per-season variants for Trial / Mirror / Passage) does NOT extend to the Ascension. **This is the canonical lock.**

**Why:**

The Trial / Mirror / Passage variants live in the seasonal world. They are the season's cosmological vocabulary — its way of naming its own cosmology. They belong IN the season.

The Ascension is the return-to-Earth-Self moment. The player is leaving the seasonal world and crossing into their own persistent identity's hub. The language at this threshold should be **the player's own**, not the season's. The Earth Self has its name; the Court has its name; the Wheel turns in its impersonal universality. The seasonal vocabulary stays in the season.

**What this looks like presentationally:**

- The cinematic-frame banner uses *"The Ascension"* universally, NOT a seasonal variant
- The Spirit Guide's three voice lines use Earth Self register — addressing the player by their chosen name, referencing "the Court," referencing "the Wheel"
- The form being ascended carries its LLM-generated full name (*"Lantern-Keeper of Yomi's Winds"*) into the Court — that name is the bridge from seasonal to Earth Self register
- The Court itself is named *the Court of [Earth Self name]* — the player's hub, populated by what they have lived as

**What this protects against:**

- Seasonal vocabulary creep into the Earth Self register. If Yomi's Ascension was called *"The Yomi-Return"* and Deep Trench's was called *"The Trench-Surfacing,"* the Earth Self hub would feel like a museum of seasonal vocabularies. By contrast, ALL seasons share *the Ascension* — the player learns this single universal moment across seasons; each season's contribution is *what form ascended,* not *what the Ascension was called.*
- The cosmology's three-actor structure (Earth Self / Wheel / Spirit Guide) becoming fragmented across seasonal vocabularies. The three actors are universal across seasons; their universal language must be preserved at the Ascension threshold.

**What this DOES admit:**

- The form's LLM-generated name carries seasonal flavor naturally (*"Lantern-Keeper of Yomi's Winds"* arrives at the Court with its seasonal-origin name intact)
- The Spirit Guide may reference the season's anchor in voice lines (*"the descent through Yomi is complete"*) — the season is acknowledged as the journey just walked, but the Ascension moment itself uses Earth Self register

---

## The Ascension — six-phase sequence

Structurally parallel to Trial and Passage; tonally distinct as cosmological completion.

### Phase 1 — Season-end approach

The final act-3 Trial has resolved. The final encounter / boss has been overcome. The seasonal arc is complete in mechanical terms. What changes:

- **Music shifts to Ascension register.** The seasonal music attenuates; a higher-register cosmological underlay begins. The track is *spacious* — not triumphant; not somber; *open.* The Ascension music is unique to the moment; the same track plays at every season's Ascension (consistent with Earth Self register).
- **Environmental signals — the seasonal world *softens.*** The chamber / vista the player ends in becomes lit in a Wheel-acknowledgment register. Color desaturation shifts toward warmer tones (the season's cosmology gently releasing). Ambient sound clarifies.
- **Spirit Guide partial-presence shifts.** Through the final act, the Spirit Guide's voice has been in companion-register (per Beatrice arc in spirit-guide-voice.md forthcoming). At the Ascension approach, the Guide's *presence* becomes more present-without-being-foregrounded — the Guide stands at perch-distance but slightly closer; opacity slightly more solid. The Guide is here for what comes.
- **The form pauses.** Whatever combat or encounter just resolved, the player's form is left in a contemplative posture — embodiment-specific (a humanoid form standing; a slime form at rest; a dragonling form coiled; a spirit form gathered). The world holds.

### Phase 2 — Threshold

The seasonal world's last vista is shown.

- **Camera holds on the seasonal vista.** The player can look. No combat clock; no time pressure. The season is being given its final witnessing.
- **A cinematic frame at narrative-moment-tier fidelity** surfaces. Hand-drawn pixel; depicts the form at peace in the season's world. This is the form's final moment IN the season — at home, at completion, at the threshold.
- **Per `embodiment-narrative-layer.md`:** the form's posture in the frame is embodiment-specific. A humanoid stands looking outward; a slime rests in a contemplative pose; a dragonling perches; a spirit gathers itself into more solid form.
- **The banner surfaces:** *"The Ascension"* — universally; Earth Self register. The form's full LLM-generated name is shown below: *"Lantern-Keeper of Yomi's Winds"* / *"Trenchwind Pitch-Caster"* / etc.
- **The Spirit Guide speaks the FIRST voice line.** Beatrice register; warmed by the season's arc; companion-tone. Acknowledges the journey just walked. Examples:
  - *"[Earth Self name], the descent through [season anchor] is complete. The form has walked it well."*
  - *"You have lived this season. The Wheel has turned, and you have walked through it. Now we cross."*
  - *"The seasonal world holds — but you cross back. The form comes with us."*
- The voice line MAY reference the season's anchor or the season's particular journey-trajectory (which acts had Trial body-swaps, which had Mirror paths, etc.). This is engine-emitted at season-build time OR template-substituted with season-specific data.

### Phase 3 — The ascension event

The threshold is crossed. The form ascends.

- **The form rises** — visual: the seasonal form rises into the air, dissipates upward in light, OR transforms via embodiment-specific arrival-language (per `embodiment-narrative-layer.md` § "Communication / speech vocabulary" — a slime *coalesces upward*; a humanoid *transfigures into light*; a dragonling *takes wing*; a spirit *gathers and ascends*; a swarm *clusters into rising assembly*).
- **The Wheel acknowledges** — the strongest cosmological-aura event in the game. Screen-edge ambient register intensifies; a deep, slow musical swell underscores. Possibly: a brief environmental gesture (the seasonal world's color palette inverts momentarily; or, the chamber's geometry resolves into a more transcendent register). This is the Wheel's most visible action throughout the project's Phase-0 surface.
- **The seasonal world recedes.** Not abruptly — the camera moves with the ascending form; the seasonal vista fades behind. The form is leaving the season behind.
- **The Court surfaces.** As the form rises, the Earth Self's hub becomes visible above / beyond. This is the player's first view of the Court for this season's Ascension. Existing Court members (if any) are visible at their stations; the new arrival's station is foregrounded (or, for first season, the Court is being born — special framing per § Special cases).
- **The Spirit Guide speaks the SECOND voice line — the introduction.** This is the Court-introduction line. Beatrice register; formal; recognition. Examples:
  - *"Court of [Earth Self name] — receive the [Court class-role] who walked the [season anchor]. They carry the [path designation — body-swap-path-survivor / Mirror-path-keeper / etc.]."*
  - *"The Court grows. The Lantern-Keeper of Yomi's Winds takes their station. They walked [act-completion-detail]."*
  - The line is *formal*, slightly ceremonial — this is the Guide acting in their role as announcer-to-the-Court (per cosmology-reincarnated.md § "The Spirit Guide" Phase 5 functions).

### Phase 4 — Court reception

The form arrives at the Court.

- **The form takes its station.** Visual: the new retainer settles into position within the Court's spatial arrangement. The station may be auto-assigned at this Phase 0 stage; future Earth-Self hub work may admit player-chosen station placement (per § Open questions Q1).
- **Existing Court members acknowledge** — visual: any existing Court members turn toward the new arrival. For voiced retainers (per `court-of-forms.md` C4 — voiced characters emerging over time), a brief chorus-acknowledgment voice line may surface. For first-season players, no existing members to acknowledge; special framing applies.
- **The Court is shown briefly in its current state.** The player sees: how many retainers (N forms now, where N = seasons-completed); the Court's composition; the new arrival in context. This is the "depth of the Court" surfacing per `court-of-forms.md` C7.
- **A contemplative beat.** ~3-5 seconds where the player can look at the Court — the new retainer in their station; the existing members at theirs. No input required; the player is *seeing* the cosmological accumulation.

### Phase 5 — Settling

The Court has received the form. The cosmology has completed its turn.

- **The Spirit Guide speaks the THIRD voice line — the settling line.** Beatrice register; warm; recognition of state. Examples:
  - *"Your Court holds [N] now, [Earth Self name]. Walk well, until the next descent."*
  - *"The Wheel rests. The descent is complete. You return to yourself."*
  - *"This shape — the Lantern-Keeper — walks with you now. Until the Wheel turns again."*
- **Music settles.** The Ascension track softens to outro register; the moment is wrapping. Not abruptly — there is breath.
- **Optional contemplative gesture surface (design space; not Phase 0 required).** Per § Open questions Q2 below — the player MAY have the opportunity to make a small gesture acknowledging the new retainer (a kept-memory designation; a station-adjustment; words of welcome). This is design space parked for Earth-Self hub maturation; Phase 0 ships with the moment as purely receptive.
- **The Court holds.** The Court UI persists; the new arrival is highlighted; the player can navigate briefly OR press to continue.

### Phase 6 — Threshold to next descent

The Ascension has completed. The player's next choice surfaces.

- **The player has the option to begin a new descent (start a new season) OR remain at the Court.**
- **Spirit Guide retreats to standard partial-presence at the Earth Self hub.** The companion-register voice softens back to perch-distance posture. The Guide will return at the next descent.
- **New season generation can be triggered** if the player chooses to begin again. This handles the engine's Phase-0-shippable path: end-of-season → next-season-or-Court-stay choice.
- **For Phase 0 demo specifically:** the demo's end-of-season state may simply be "return to main menu / loading screen for next season." The full Earth-Self hub navigation is post-Phase-0 work. The Phase 0 Ascension ends at Phase 5; the Phase 6 threshold-to-next-descent is gestured at but not fully implemented until the hub ships.

---

## The Spirit Guide at Ascension — the voice climax

The Spirit Guide speaks **three voice lines** at Ascension. This is more than at any other moment in the game.

| Phase | Line | Function |
|---|---|---|
| Phase 2 — Threshold | Journey-acknowledgment | Recognizes the season's walk; names the form's identity |
| Phase 3 — Ascension event | Court-introduction | Formal announcement to the Court; uses Earth Self name + season anchor + form class-role + path-taken designation |
| Phase 5 — Settling | State-acknowledgment | Acknowledges the new Court size; signals continuance |

Three lines justified by:

1. **Once-per-season frequency.** The voice weight matches the moment's rarity.
2. **Cosmology becoming explicit.** This is where the Wheel + Earth Self + Court are all named together; the Spirit Guide's role as the cosmology's announcer requires the voice to do the naming.
3. **The Beatrice arc reaches its season-climax.** Per spirit-guide-voice.md (forthcoming) — the Guide's voice register has progressed from reserved (early season) to warmed (mid season) to companion (late season). At Ascension, the Guide is in companion-register — addressing the player by name, recognizing the journey, formally welcoming the new retainer.

**The Guide's voice at Ascension does NOT:**
- Become exuberant or celebratory in modern-game register (no high-energy congratulations; no "you did it!")
- Use seasonal vocabulary (Earth Self register only)
- Speak more than the three named lines (silence between is part of the weight)
- Address the form being ascended directly (the Guide addresses the Earth Self and the Court; the form is received but not spoken-to)

**The Guide's voice at Ascension DOES:**
- Address the Earth Self by name (Phase 2 + Phase 5 at minimum; Phase 3 formally invokes the Court by Earth Self name)
- Reference the journey concretely (season anchor; path-taken; form identity)
- Sound like a being who has walked this Ascension many times — recognition, not novelty (Beatrice has waited centuries; the Guide has witnessed many Ascensions; each is precious without being startling to the Guide)

---

## The Wheel at Ascension

The Wheel does not speak (per cosmology-reincarnated.md lock — the Wheel never speaks). At Ascension, the Wheel **acts at its strongest visible register.**

- **Phase 3 cosmological-aura event** is the Wheel's most pronounced action throughout Phase 0. Visual: screen-edge intensification; deep slow musical underlay; possibly a brief environmental inversion (seasonal palette giving way to Earth Self register).
- **The Wheel's action is the agent of the cycle's completion.** The descent ends; the return is acknowledged; the form crosses the threshold. The Wheel turns.
- **The player understands the Wheel as cosmologically real** at Ascension. Throughout the season, the Wheel has been gestured at; here it acts. By the second or third season, players will associate the Phase 3 environmental signature with the Wheel and understand it as the cosmology's load-bearing actor.

---

## The Earth Self at Ascension

The Earth Self becomes **active for the first time** at Ascension.

- **Named.** The Spirit Guide addresses the player BY their chosen Earth Self name (locked at first play per cosmology-reincarnated.md). For first-time players, hearing this name spoken in the Guide's voice for the first time is significant — *"Aiden, your Court grows."*
- **Receives the form.** The Court — which is the Earth Self's — receives the new retainer. The Earth Self's persistent identity is the *destination* of the form's ascent.
- **Not voiced.** The Earth Self does not speak in Phase 0. The Spirit Guide speaks; the Wheel acts; the Court receives. The Earth Self is *present as the player* — the player IS the Earth Self at this moment. No artificial Earth Self voice should be introduced; doing so would split the player's identity from the Earth Self in a way the cosmology rejects.
- **Possibly voiced in future:** post-Phase-0 Earth-Self hub work may admit Earth Self interactions that involve dialogue (with the Court, with the Wheel-in-implicit-form, with the Spirit Guide). At Ascension specifically, the Earth Self remains the player's silent agency.

---

## The Court at Ascension

The Court is **foregrounded** at Ascension — likely for the first time in the player's experience this session, possibly for the first time ever for new players.

- **Phase 3 reveal** — as the form ascends, the Court becomes visible. Player's first view of the cosmological hub their seasonal play has been building toward.
- **Phase 4 reception** — the form takes its station; existing members acknowledge.
- **Phase 5 state surfacing** — the Court's size and composition are visible to the player.
- **Special cases for first / large Court:** see § Special cases below.

The Court's presentation at Ascension consumes `court-of-forms.md` canonical:
- C1 — Court framing supersedes Gallery/Roster
- C2 — Navigable spatial presentation
- C3 — Each form's LLM name preserved
- C4 — Voiced retainers (subset; emerging over time)
- C5 — Accumulation is paced and commemorated (this IS that commemoration)
- C6 — Court belongs to the player
- C7 — Depth-of-Court is the meta-measure
- C8 — Dual-label class-roles per embodiment

---

## Special cases

### First-season Ascension — the Court's birth

The player's first Ascension is also the Court's first arrival. There are no existing members; the Court is being founded.

Special framing:

- **Phase 3 Court reveal** is the Court's *first appearance* to the player. The space is shown empty — Earth Self's hub, prepared for retainers, awaiting the first.
- **Phase 4 Court reception** is the Court's birth. The new retainer takes the first station. No existing members to acknowledge (the chorus is silent because the chorus is *being formed* here).
- **Spirit Guide Phase 5 voice line specifically acknowledges the birth state:**
  - *"Your Court begins, [Earth Self name]. The [form class-role] is the first to walk it with you. Many more, if you choose."*
  - This line is generated at first-Ascension specifically; not re-used at subsequent Ascensions.
- **The contemplative beat at Phase 5** has additional weight — the player is seeing the *beginning* of their persistent meta-progression. This is a once-per-account moment.

This first-Ascension framing is **load-bearing for retention.** The pitch's "Earth Self collection grows across seasons" claim depends on the first Ascension landing as *"this is the beginning of something I will accumulate."* If the first Ascension feels equivalent to a "form added to roster (1/N)" notification, the meta-progression hook fails to register. With ritual treatment, the first Ascension lands as foundational.

### Large-Court Ascension — depth becoming visible

After many seasons, the player's Court has substantial size (10+ retainers, possibly more over months/years of play). The Ascension must scale.

- **Phase 4 Court reception** surfaces the new arrival in foreground; the broader Court is glimpsed in background. The player can see the accumulated depth without the new arrival being lost in it. Per Solo Leveling shadow-extraction precedent: the new shadow joins the army; the army is present; the new arrival is the moment.
- **Phase 5 state surfacing** uses the depth as positive signal — *"Your Court holds 17 now, [Earth Self name]."* The number is naming the accumulated identity.
- **Voiced retainers** (if any have emerged — per court-of-forms.md C4 + Q2) may surface a brief chorus-acknowledgment. If a previously-ascended retainer of the same class-role is voiced and present, a recognition-line could surface (*"the Knight of your Throne-Room season acknowledges the new arrival"* — implementation territory; cf. § Open questions Q3).

### Body-swap-path vs Mirror-path Ascension distinction

The form ascending arrived at season-end via a particular trajectory. Per `court-of-forms.md` Q1 (rank dimensions): path-taken is a candidate marker. At Ascension, this distinction can be surfaced:

**Body-swap-path-only-ascension:** the player took at least one Trial body-swap during the season; the final form is one they transformed into via Trial body-swap. The Court entry notes this — possibly the Spirit Guide's Phase 3 line reads *"the [class-role] who arrived by transformation."*

**Mirror-path-only-ascension:** the player took Mirror-paths at all Trials; the final form is their original seasonal class identity. The Spirit Guide's Phase 3 line reads *"the [class-role] who walked the season as themselves; identity preserved."*

**Mixed-path-ascension:** the player took both Body-swap and Mirror paths across the season's three Trials. The Spirit Guide's Phase 3 line acknowledges the journey-shape — possibly *"the [class-role] who walked many shapes to arrive here."*

**No-Trial-ascension:** if the player somehow ended a season without completing all Trials (likely edge case — depends on whether the engine permits this), the Ascension acknowledges the partial-completion register.

This distinction gives Court members **real biographical distinction** — each retainer has a Court-entry story. The Spirit Guide's Phase 3 line consumes this designation; it could also surface as a Court entry metadata field visible in the hub.

---

## What this requires — cross-seam summary

### Engine (rocket / star-lord) emits

For Ascension triggering:
- Season-end state trigger (form alive at season end is the ascension candidate)
- Form's path-trajectory metadata (which Trials were Body-swap-path vs Mirror-path; whether any Passages were Accepted earlier; the final form's origin — original-seasonal-class vs body-swap-acquired)
- Spirit Guide Ascension voice lines:
  - Phase 2 journey-acknowledgment line — generated per-season at season-build; references season anchor + form identity (~1 line per season; possibly variants for path-trajectory variations)
  - Phase 3 Court-introduction line — generated per-Ascension at season-end; references Earth Self name + form class-role + path designation (~1 line per Ascension; templatically substituted with Earth Self name)
  - Phase 5 state-acknowledgment line — generated per-Ascension; references current Court size + form identity (~1 line per Ascension; templatically substituted)
- First-Ascension special line (Phase 5) — engine-emitted once per account; recognizes Court's birth
- Court state surfaces — current N forms; ordering; station assignments

LLM cost impact: ~3-5 additional voice lines per season (most templatically substituted; minimal LLM generation overhead). Bundled into the per-season cosmological-vocabulary call where applicable.

### Demo (drax) implements

- Phase 1 season-end approach signaling (music shift, environmental softening, Spirit Guide presence shift)
- Phase 2 threshold routine (camera hold on seasonal vista; cinematic frame; banner using universal "The Ascension" + form's LLM-generated full name; Spirit Guide first voice line surface)
- Phase 3 ascension event routine (form rises with embodiment-specific arrival animation; Wheel's strongest cosmological-aura event; seasonal world recedes; Court surfaces; Spirit Guide second voice line surface)
- Phase 4 Court reception routine (form takes station; existing-member acknowledgment if any; Court state surfacing; contemplative beat)
- Phase 5 settling routine (Spirit Guide third voice line surface; music settling; optional contemplative gesture affordance — Phase 0 ships without affordance; future hub work admits it)
- Phase 6 threshold-to-next-descent (in Phase 0: "return to main menu / load next season"; in future Earth-Self hub: navigation to Court / next-descent-start / hub-stay)
- Special-case branches: first-season-Ascension framing; large-Court rendering; path-trajectory designation surfacing

Estimated drax work: 2-4 weeks for the full Ascension moment ritual implementation (Phase 0 scope, without full Earth-Self hub). The hub work itself adds substantial scope but is post-Phase-0.

### Spirit Guide voice doc (forthcoming, work queue #3)

When `spirit-guide-voice.md` lands:
- The three Ascension voice lines specifications integrate into the voice doc's coverage.
- The Beatrice arc reaches season-climax at Ascension; the voice doc commits to companion-register at this moment.
- The first-Ascension special line is named as a once-per-account variant.

---

## What this protects against

- **Ascension as roster-update notification.** Without ritual, "form added to library (1/N)" reads as inventory ping. With ritual, the moment lands as cosmological completion.
- **The Earth Self remaining structural-placeholder.** Without explicit naming at Ascension, the Earth Self never becomes *the player* in the cosmology's vocabulary. The Spirit Guide addressing the player by their chosen name at Ascension is the moment the meta-layer becomes personal.
- **The Court remaining offstage.** Without Phase 3-4 foregrounding, players may complete several seasons before realizing the Court is a real navigable space. The first-Ascension Court reveal is the player's introduction to the meta-layer's hub.
- **Seasonal vocabulary creep into Earth Self register.** Without the canonical commitment that Ascension uses Earth Self register, future LLM work may reach for seasonal Ascension variants and dilute the universal-frame distinction. The canonical lock prevents this.
- **Spirit Guide voice climax landing weakly.** Without the three-voice-line specification, future LLM work may default to one Ascension line; the season-climax weight requires more.
- **The Wheel remaining hidden.** Without the Phase 3 strongest-cosmological-aura event, the Wheel stays gestured-at but never visibly active. Phase 3 is the Wheel's most visible action; lock it.
- **First-Ascension generic-Ascension equivalence.** Without the first-season special framing, the meta-progression hook fails to register at the moment most likely to determine retention. Lock the first-season variant explicitly.

---

## Open questions

These do not block the canonical lock. They surface during implementation.

### Q1 — Court station placement at arrival

Phase 4 commits that the new retainer "takes its station." Open: is the station auto-assigned by the system (newest-to-frontmost; or some other rule), or does the player place the new retainer themselves? Phase 0 likely ships with auto-assignment; future Earth-Self hub work may admit player-placement. My recommendation: **Phase 0 auto-assigns; hub work admits player-placement gesture as optional Phase 5 affordance.** The mechanical default works; the player-placement gesture is upside design space.

### Q2 — Optional contemplative gesture at Phase 5

Earlier discussion proposed an optional contemplative gesture the player can make at the new retainer's arrival — a kept-memory designation, words of welcome, station-adjustment. Phase 0 ships without affordance; the moment is purely receptive. Future Earth-Self hub work may admit a gesture-affordance. My recommendation: **defer to hub work; ship Phase 0 receptively; family-playtest may surface whether the moment feels complete without gesture or wants one.**

### Q3 — Voiced-retainer chorus acknowledgment

If existing Court members include voiced retainers (per court-of-forms.md C4), they may briefly acknowledge the new arrival. Open: should this be a *chorus* line (multiple voiced retainers together) or a *single voiced retainer's* line (the seniormost; the most relevant by class-role; etc.)? Implementation cost varies. My recommendation: **start with no chorus at first; if family-playtest finds the Court feels too silent at Ascension, add a single voiced retainer's brief acknowledgment from the most-relevant member.** The Spirit Guide's three voice lines carry the moment without needing chorus support.

### Q4 — Ascension during very-late-game (Court with many same-class-role members)

When a player's Court has multiple Knights or multiple Bulwarks or multiple Casters from different seasons, the new arrival's distinctiveness lives in their **path-trajectory designation + seasonal anchor + LLM-generated full name** — not in their class-role alone. Open: does the Spirit Guide's Phase 3 introduction surface comparative language (*"another Knight joins your Court"*)? Probably yes — comparative awareness gives Court members real biographical distinction. My recommendation: **engine emits awareness of class-role-count-in-Court; Spirit Guide line consumes it when ≥2 of the same class-role exist.**

### Q5 — Pacing tuning

The estimated 30-60 second duration for Phase 0 Ascension is design intent; tuning territory at implementation. Family playtest will inform whether the moment feels appropriately weighty or drags. My instinct: **30s minimum (Phase 2 threshold + Phase 3 event + Phase 4 reception + Phase 5 settling each ~5-10s) with affordance to extend for first-Ascension and large-Court special cases.**

### Q6 — Subsequent-season Ascension within a single play session

If a player completes a season and immediately begins another, ascending two forms in quick succession, the second Ascension's special weight may diminish. Open: does the Spirit Guide adjust register for sequential-Ascensions-in-one-session? Probably yes — slight register acknowledgment of "the next descent comes quickly" without removing the moment's weight. My instinct: **let it emerge from family playtest; no special design intent locked until pattern is observed.**

---

## What this DOESN'T do

- **It does not specify the full Earth-Self hub implementation.** The hub is post-Phase-0; this doc captures the Ascension threshold event that bridges seasonal play TO the hub. Hub navigation, hub-state interactions, hub social features (when applicable) are out of scope.
- **It does not specify the next-descent initiation flow.** Phase 6 gestures at "begin a new descent" but the specific demo/UI flow for starting a new season post-Ascension is drax + Matt decision when hub work begins.
- **It does not specify Court-member voiced-emergence rules.** Per court-of-forms.md Q2 — that's its own design space.
- **It does not specify multi-account Court behavior.** Far-future when (or if) shared-account / family-Court / inheritance patterns surface.
- **It does not address Ascension failure modes.** Mechanically: the form alive at season end ascends; this is locked. There are no Ascension-failure modes to specify. (Edge case: if a player somehow exits a season without any form alive, that's a Passage-pool-depletion-at-season-end scenario that should be impossible per mechanical design; if it surfaces, file 32 § Section 9 + 11 territory, not this doc.)

---

## Cross-references

- `trial-moment-ritual.md` — paired ritual; the act-end ritualization
- `passage-moment-ritual.md` — paired ritual; the harsh-moment ritualization
- `cosmology-reincarnated.md` § "Ascension and the Court" + § "The Spirit Guide" Phase 5 functions + § "The Earth Self" + § "The Wheel"
- `court-of-forms.md` — C1-C8 structural commitments + the meaning-of-the-arc statement
- `naming-triad.md` — universal frame for Trial / Mirror / Passage; the contrast frame Ascension's Earth Self register is committed AGAINST
- `embodiment-narrative-layer.md` — per-form arrival animations and contemplative-posture vocabulary
- `enemy-visual-legibility.md` § S4 (narrative-moment-tier for cinematic ascension frame)
- `style-register.md` — HD-2D-pixel; narrative-moment-tier specification
- `gandalf-design-lineage.md` Layer 2 (D2 act-completion register) + Layer 4 (Hades House return) + Layer 5 (Solo Leveling shadow-extraction-into-army)
- File 32 § Section 11 — "Form library acquisition" + ascension mechanical substrate
- File 33 § "Form library acquisition (LOCKED + CORRECTED)" + § "Earth Self meta-layer"

**Forthcoming (not yet authored):**
- `spirit-guide-voice.md` (Phase 2 work-queue #3) — the three Ascension voice lines specifications + Beatrice-arc season-climax register
- `seasonal-anchor-prose-notes.md` (Phase 2 work-queue #12) — anchor-specific Ascension flavor (e.g., what does *"the descent through The Deep Trench is complete"* register evoke)

---

## Maintenance protocol

When drax dispatches Ascension-moment implementation work:

1. Re-read this doc with drax.
2. Convert the six phases into demo-side routines: approach signaling, threshold cinematic frame, ascension event with Wheel-acknowledgment-event + Court reveal, Court reception, settling with optional gesture affordance deferred, threshold-to-next-descent.
3. Verify Earth Self register lock (no seasonal-vocabulary creep) in implementation.
4. Resolve open questions (Q1-Q6) with Matt before locking implementation details.
5. Special-case branches for first-season Ascension + large-Court rendering + path-trajectory designation.

When spirit-guide-voice.md lands:

1. The three Ascension voice lines specifications cross-reference to that doc.
2. The Beatrice-arc companion-register at Ascension is reinforced.
3. The first-Ascension special line is documented as once-per-account variant.

When Earth-Self hub work begins (post-Phase-0):

1. Phase 6 threshold-to-next-descent receives full implementation.
2. Optional Phase 5 contemplative-gesture affordance is implemented per § Open questions Q1-Q2.
3. Court station-placement gesture is implemented per Q1.
4. Voiced-retainer chorus acknowledgment is implemented per Q3.

When future canonical docs touch cosmological-moment rituals or meta-progression:

1. Reference this doc.
2. The Earth Self register canonical lock at Ascension is non-negotiable.
3. The Spirit Guide's three voice lines at Ascension are the season's voice-climax; reverence for the rarity-of-this-moment is required.

— gandalf, with Matt's standing approval on the canonical patterns this doc consumes; the ritual trilogy is complete (2026-05-15)
