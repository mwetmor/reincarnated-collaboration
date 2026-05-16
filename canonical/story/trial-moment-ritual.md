# The Trial Moment — Ritual and Presentation

**Status:** **Canonical.** Authored 2026-05-15 by gandalf. Captures the design intent for the Trial encounter moment's ritualization — the approach, the choice, the fight, the resolution. Drax's eventual implementation target.

**Why it exists:** the Trial is **the season's dramatic core** (per `cosmology-reincarnated.md`). Three times per season, the player encounters a Trial. Each is the moment the season's structural rhythm pivots on. The mechanical substrate is well-locked (file 32 § 11 + 33; cosmology-reincarnated.md; naming-triad.md). The *presentational* substrate is undefined. Without this doc, the Trial moment ships as "a fight that the player chose a path before." With this doc, the Trial moment ships as **ritual**, which is what the design intends.

**Companion docs:**
- `cosmology-reincarnated.md` § "The Trial" + § "The Mirror" + § "The Passage" — the cosmological frame
- `naming-triad.md` — Trial / Mirror / Passage with per-season vocabulary variation
- `enemy-visual-legibility.md` § S4 (Trial cinematic frame) + § S7 (Mirror exception)
- `embodiment-narrative-layer.md` — per-embodiment vocabulary for trial-boss / Mirror presentation
- `style-register.md` — HD-2D-pixel register; the visual idiom the Trial moment renders in
- `gandalf-design-lineage.md` Layer 2 (Diablo II quest-acceptance ritual) + Layer 4 (Hades boon-offer ritual; Souls bonfire / fog-gate)

**Pending:**
- knight-rider to draft a decisions-log entry capturing the Trial-moment-ritual canonical lock (per ADR-002; cross-seam — drax demo work, star-lord LLM-prompt context, possibly rocket engine emits for trigger flags)

---

## What this doc is

This doc captures **presentational design intent** for one of the project's three load-bearing player-perception moments (alongside the Passage and ascension). It commits the structural shape of the Trial encounter — what the player sees, what builds presence, what the choice screen looks like, what the Spirit Guide does, how the fight begins, how the fight resolves.

**It is not** a mechanical spec. The mechanical substrate is in file 32 § 11 (Trial body-swap reward bundle; choice-before-fight; doppelganger gate). This doc operates one layer up — what does the *moment* feel like, given the mechanics are already locked.

**It is not** an implementation spec. Drax's eventual demo work will produce the implementation; this doc is the design-intent target the implementation reaches for.

---

## Why the Trial moment is load-bearing

Three times per season. Each one is irrevocable in the path-chosen sense (per file 32 § 11: the path is chosen BEFORE the fight; once committed, the player fights through that path). Each one shapes the season's body-swap pool, the player's class trajectory, the Court's eventual composition.

The Trial moment is **the most important single recurring moment in Reincarnated.** No other moment in the game carries comparable structural weight. The Passage is harsher but less frequent and not always encountered. The ascension is the season's climax but happens once per season. The Trial happens three times per season, at predictable rhythmic intervals, and every Trial reshapes the player's trajectory.

Genre precedents for what this caliber of moment needs:

- **Diablo II quest acceptance** — the player walks to the NPC, dialogue surfaces, the NPC explains the stakes, the player commits. Den of Evil + Anya's Scroll + Lam Esen's Tome — these became iconic moments because they were *delivered as moments,* not surfaced as inventory acceptances.
- **Hades boon offer at chamber transition** — Zagreus enters the chamber, the camera centers on the boon giver, the boon's specific effect surfaces, the player chooses deliberately. The pause is the design.
- **Souls family boss approach via fog gate** — the player walks the architecture leading to the boss; the fog gate is visible; crossing it is a *commitment* the player understands; the boss arena is the encounter's amphitheater.
- **Bloodborne hunter-vs-hunter encounters** — the recognition-coded moments when a beast-form encounter reveals itself as a kindred hunter (Father Gascoigne; Lady Maria). Visual identity grammar signals "this is a peer."

The Trial moment should learn from all of these. It is *both* a choice moment (Hades) and an encounter ritual (Souls).

---

## The Trial moment — six-phase sequence

The Trial moment is structured as **six discrete phases**, each with its own presentational signal. Drax's implementation should treat these as locked phases; the player progresses through them linearly.

### Phase 1 — Approach

The player has been clearing the act's content; the Trial chamber approaches. What changes:

- **Music shift.** The act's exploration / combat music gives way to a Trial-specific track. The new track is *quieter*, more *deliberate* — not a power-up cue. The shift signals "something is about to matter."
- **Environmental cue.** The geometry of the level leading to the Trial chamber visually narrows — corridor architecture, archways, a sense of *approach.* Per the locked HD-2D-pixel register: hand-drawn tile work in the approach zone reads as more deliberate than the act's procedural dungeon spaces.
- **Spirit Guide softens into presence.** Per cosmology-reincarnated.md § "The Spirit Guide": the Spirit Guide is partial-presence at all times. At the Trial approach, the Spirit Guide's opacity / position shifts — the Guide *leans in*. Visual signal that the Guide is about to speak.
- **No combat in the approach zone.** The path from "last combat encounter" to "Trial chamber" is clear of monsters. The player walks toward the moment without distraction.

### Phase 2 — Threshold

The player reaches the Trial chamber. What surfaces:

- **A cinematic frame at narrative-moment-tier fidelity** (per style-register.md § "Narrative-moment tier" + enemy-visual-legibility.md § S4). The frame is hand-drawn pixel-art, higher resolution than combat tier. It depicts the trial-boss (for body-swap path candidates) or the player's own form (for Mirror-path foreshadowing — but the player doesn't know which yet at this phase).
- **The trial-boss's full LLM-generated name displayed at cinematic-banner scale.** Per enemy-visual-legibility.md § S5: `display_name_banner_class = cinematic-banner` for trial encounters.
- **Per-season seasonal-variant Trial vocabulary surfaces** (per naming-triad.md § "Per-season vocabulary variation"). The cinematic banner uses the season's flavored Trial name (*The Sounding* / *The Threshold-Test* / *The Vigil-Trial* / etc.).
- **The Spirit Guide speaks — one line.** Beatrice register; per spirit-guide-voice.md (forthcoming). Contextual reference to the trial-boss's nature or the season's cosmology. Example shape: *"This one I have seen before — a Tidecaller of the Deep Trench. Their patience is real."* Single line. The Guide does not explain the choice; that comes in Phase 3.

### Phase 3 — The choice

Time pauses. The choice screen surfaces.

**Layout (per naming-triad.md § "Where BOTH surface together"):**

```
[Seasonal variant - cinematic banner]
[Universal frame - smaller text below]

→ [Body-swap path - seasonal variant phrasing]
  ([Body-swap path - universal frame helper text])
  [One-line description of what victory grants]

→ [Mirror path - seasonal variant phrasing]
  ([Mirror path - universal frame helper text])
  [One-line description of what victory grants]
```

**Worked example for Yomi season:**

```
THE THRESHOLD-TEST
(The Trial)

→ Take the form of the Threshold-Keeper
  (Body-swap path — transform on victory)
  Full XP, +10% global resistances, skill point. Pool reshapes.

→ Face the Pomegranate-Image
  (Mirror path — preserve identity, claim deferred rewards)
  1/4 XP, half resistances, half skill point. End-game reclaim quest.
```

**Choice mechanics:**

- **Time is paused.** No combat clock; no real-time pressure. The player reads, considers, commits.
- **The Spirit Guide is *silent* during the choice.** Phase 2 had the Guide's one line; Phase 3 has the player alone with the decision. This is critical — the Spirit Guide is *yours but does not choose for you.* (Per Beatrice precedent: the Guide carries foresight but the choice is the Master's.)
- **The choice is irrevocable on commit.** Once the player commits to a path, the fight begins. No mid-fight switch. The mechanical lock per file 32 § 11.
- **A "reconsider" button is admissible but not required.** If the player wants to back out before committing, the design allows it — they can walk back to the approach zone, take another minute, return. Once they commit, the fight begins. This protects against accidental clicks but preserves commitment-weight.

### Phase 4 — Transition into combat

The choice is made. What happens between "commit" and "fight":

- **A brief presentational beat** — 2-3 seconds at most. Not a long cutscene; just enough to register the transition. The screen darkens; the Trial chamber's lighting shifts; the music gathers.
- **The Wheel acknowledges.** A brief environmental signal — the chamber's ambient lighting pulses; a wind moves through (Wheel-mythic-coded; not literal). This is the Wheel turning. Subtle; not narrated.
- **The opponent surfaces.** For body-swap path: the trial-boss enters the chamber with cinematic-tier aura (per enemy-visual-legibility.md § S3 `display_aura_tier = cinematic`). For Mirror path: the player's own form appears across the chamber — *same sprite, same palette, mirrored animations* — per enemy-visual-legibility.md § S7's Mirror exception.
- **Time resumes.** The fight begins.

### Phase 5 — The fight

**Body-swap-path fight presentation:**

Standard combat against an elevated opponent. The trial-boss uses their full kit; the cinematic-tier aura is sustained throughout the fight; the encounter is mechanically tuned per file 32 § 11. Visual presentation is consistent with combat tier (HD-2D pixel; tier-coded aura per enemy-visual-legibility.md). The trial-boss's per-embodiment vocabulary surfaces in skill flavor text per embodiment-narrative-layer.md.

**Mirror-path fight presentation:**

The recognition fight. Per enemy-visual-legibility.md § S7: same sprite as player; same animations; same color palette; *recognition-coded subtle cues* signal "this is you, not a copy." The cues should be minimal — perhaps a slightly desaturated palette, perhaps mirrored animation timing — enough to read as "the mirror" without breaking the *"you are fighting yourself"* design intent.

**Voice lines during Mirror fights (if used):** sparse; quoting the player's recent build choices. *"I chose Combustion"* if the player has invested heavily in the Combustion chain. *"This is the path I walked further along"* — but this last is the Spirit Guide's voice, not the Mirror's. The Mirror is the player's class deployed against them; it speaks (if at all) in the player's mechanical voice, not in the Spirit Guide's mentor voice.

**During both paths:**
- The Spirit Guide is *visible but does not advise during combat.* The Guide watches. The Guide does not call shots. Per spirit-guide-voice.md (forthcoming): the Guide *witnesses* the Trial; does not advise through it.
- The player's HUD, controls, and combat mechanics are as in any combat encounter; the Trial does not introduce new combat verbs. The novelty is presentational, not mechanical.

### Phase 6 — Resolution

The fight resolves (the player wins; the alternative is the Passage moment, which has its own design intent forthcoming as a separate doc but is sketched in cosmology-reincarnated.md § "The Passage"). What surfaces:

- **A pause.** Combat ends; the screen does not immediately surface a reward screen. There is a beat — the trial-boss / Mirror falls (per the embodiment-specific death-language; see embodiment-narrative-layer.md § "Injury / death vocabulary"). The player sees the resolution.
- **The Spirit Guide speaks again.** One line; Beatrice register; contextual. *"You have walked this further."* / *"You preserved who you are."* / etc. Per spirit-guide-voice.md (forthcoming).
- **The reward bundle surfaces** — XP, global resistances, skill point(s) per file 32 § 11. The bundle is presented as *named gifts*, not as inventory pings. Each component gets a moment.
  - Per Diablo II quest-reward-bundle precedent (per gandalf-design-lineage.md Layer 2): each reward is *a named thing* the player remembers, not a number that ticks up. Possibly: each Trial body-swap reward bundle has a *gift name* — *"the Mark of the Threshold-Keeper"* or similar — that the player carries forward as a remembered milestone.
- **For body-swap path:** the transformation. The player's seasonal form is replaced by the trial-boss's class identity. Per file 32 § 11: this is irrevocable for the season. The transformation deserves its own presentational beat — the player's HUD / class identification / kit changes; the new class's first ability flashes; the world re-anchors. This is a *moment*, not a stat-change.
- **For Mirror path:** the preservation. The player remains their class; the reward bundle is partial (per file 33: 1/4 XP, half SP, half resistances); the end-game reclaim quest is *flagged as available* for end-of-season pickup. The reclaim flag itself should be presentationally surfaced — the player sees that there's a deferred component, but not in a way that reads as *consolation*.
- **Transition to next act** — the act ends with the Trial's resolution. The player returns to the act's hub (when Engine 2's hub exists; for Phase 0 demo work, the act-end transition is a fade-and-load to the next act's beginning).

---

## What the Spirit Guide does — and doesn't — at the Trial

The Spirit Guide's role at the Trial moment is **important and bounded.** Three appearances; specific functions:

| Phase | Spirit Guide presence | What the Guide does |
|---|---|---|
| Phase 1 — Approach | Softens into presence; opacity / position shifts | Wordless signal: *something is coming* |
| Phase 2 — Threshold | Speaks ONE line | Contextual reference to the trial-boss or the season's cosmology |
| Phase 3 — Choice | **Silent.** Present visually but does not speak. | Honors the player's autonomy in choice |
| Phase 4 — Transition | Background presence; not foregrounded | Bears witness |
| Phase 5 — Fight | Visible but does not advise during combat | Watches; bears witness |
| Phase 6 — Resolution | Speaks ONE line | Acknowledges what was done |

**Two voice lines per Trial.** That's it. The Spirit Guide's presence is far heavier than the Guide's *speech*. This is Beatrice register working — silence weights the few words.

---

## Per-season variant integration

The per-season variant of Trial / Mirror / Passage names surfaces across the Trial moment (per naming-triad.md § "Where seasonal flavor surfaces"):

- Phase 2 cinematic banner uses the season's Trial variant (*The Sounding* / *The Threshold-Test* / etc.)
- Phase 3 choice screen primary labels use seasonal variants of Body-swap-path and Mirror-path opponents (*"Take the form of the Threshold-Keeper"* / *"Face the Pomegranate-Image"*)
- Phase 3 choice screen helper-text uses universal-frame labels in parentheses
- Phase 5 combat aura per enemy-visual-legibility.md inherits the season's element palette through cipher-architecture L2-L3 modulation
- Phase 6 reward-bundle naming (if implemented as "named gifts") uses seasonal vocabulary (*"the Mark of the Threshold-Keeper"* in Yomi; *"the Brine-Sigil"* in Deep Trench; etc.)

The Spirit Guide's two voice lines (Phase 2 and Phase 6) consume the season's variant naturally — referring to "the Threshold-Test" / "the Sounding" / etc. rather than to "the Trial."

---

## What this requires — cross-seam summary

### Engine (rocket / star-lord) emits

For each generated Trial encounter:
- The trial-boss's full data (already emitted for the bestiary; needs `is_trial_encounter = true` per enemy-visual-legibility.md § S7)
- The seasonal Trial / Mirror / Passage variants (generated in the per-season cosmological-vocabulary call per naming-triad.md § "Generation integration")
- One Spirit Guide voice line for the Phase 2 threshold (seeded by the trial-boss's identity + season cosmology; generated at season-build time, not at runtime)
- One Spirit Guide voice line for the Phase 6 resolution (seeded by path-taken-and-won; generated as a small template variation OR generated per-Trial at season-build time for both body-swap-path-victory and Mirror-path-victory)

LLM cost impact: ~2-6 additional LLM calls per season (one Trial × 3 acts × 1-2 voice lines per Trial). Modest; sits within the per-season cosmological-vocabulary call's existing scope.

### Demo (drax) implements

- Approach zone signaling (Phase 1: music shift, environmental cue, Spirit Guide position shift)
- Cinematic frame routine (Phase 2: hand-drawn pixel narrative-moment-tier frame; trial-boss display; Spirit Guide voice line surface; per-season Trial variant banner)
- Choice screen UI (Phase 3: paused time; layout per worked example above; commit-to-path control; reconsider-affordance optional)
- Transition routine (Phase 4: brief presentational beat; lighting shift; Wheel acknowledgment cue; opponent surfaces — body-swap-trial-boss with cinematic aura OR Mirror with player-sprite-rendering routing)
- Combat with Trial-encounter-tier aura sustained throughout
- Mirror-fight rendering exception per enemy-visual-legibility.md § S7
- Resolution sequence (Phase 6: pause; Spirit Guide voice line; reward bundle as named gifts; body-swap-path transformation moment OR Mirror-path preservation acknowledgment with reclaim-flag surface)
- Per-season variant text consumption from the engine export

Estimated drax work: 2-4 weeks for the full Trial moment ritual implementation. Substantial but bounded; pattern reuses for all three Trials in a season.

### Spirit Guide voice doc (forthcoming)

The two Trial voice lines are specific examples consumed by spirit-guide-voice.md (Phase 2 work-queue item #3). When that doc is authored, the Trial moment's voice-line specifics integrate there.

---

## What this protects against

- **The Trial as anti-climax.** Without ritualization, the Trial reads as just-another-fight-with-a-choice-screen. With ritualization, it reads as the moment it is mechanically designed to be. Discipline #13 application — the design intent ("the season's dramatic core") gets structural enforcement at the presentation layer, not just the mechanics layer.
- **The choice screen as inventory.** Without ritual framing, the choice screen risks reading as menu UI. With pause-the-game framing, cinematic banner, Spirit Guide presence, and committed-not-flip-flop mechanics, the choice screen reads as decision-moment.
- **The Mirror fight as just-another-fight.** Without the explicit recognition grammar (per S7) and the Spirit Guide's witnessing-not-advising posture, the Mirror reads as a balance-validation surface (which it is, mechanically). With this doc's design intent, the Mirror reads as the recognition-encounter it is dramatically.
- **Reward bundles as stat-pings.** Without "named gifts" framing, the reward bundle is XP + resistances + SP popping up as numbers. With the framing, each Trial's reward becomes a remembered milestone.
- **The Spirit Guide as tooltip.** Without Beatrice register and the explicit silence-during-choice pattern, the Spirit Guide drifts into advisory-NPC register. With this doc's locks, the Guide stays mythic-mentor.

---

## Open questions

These do not block the canonical lock. They surface during implementation.

### Q1 — Reward bundles as "named gifts"

The Diablo II quest-reward-bundle precedent suggests each Trial reward should be a *named thing* the player carries forward. Open: does the engine generate names for these (yet another LLM call) or are they templated (e.g., always "the Mark of [trial-boss-class-or-form]")? Templated is cheaper and more consistent; LLM-named is richer but adds cost. My instinct: **templated per-trial, with the seasonal variant slot** — *"the Mark of the [trial-boss-class]"* in default register; *"the [seasonal-flavored-mark] of the [trial-boss-class]"* if per-season modulation is enabled. Cost-bounded; meaningful.

### Q2 — Reconsider affordance

Whether the choice screen admits a "back out" affordance. Pro: protects against accidental clicks. Con: dilutes commitment-weight. My instinct: **admit it, but make the back-out a deliberate gesture** (a "leave the chamber" option requiring affirmative action, not a simple cancel-out). The player CAN reconsider; they cannot ACCIDENTALLY commit.

### Q3 — Time pause technical implementation

The Phase 3 pause is presentational. Does the engine actually pause (combat clock stops; all NPCs frozen), or does the demo just present the choice screen as a modal overlay? For Phase 0 single-player, these are equivalent. Becomes relevant if multiplayer / rift events ever ship (post-Phase-0). Parked.

### Q4 — Music sourcing

Trial-specific music is referenced in Phase 1. The current demo1 uses per-season-themed music; the Trial track would be a new asset. Sourcing: licensable from the catalogue (music vendors at the locked HD-2D-pixel register's aesthetic — chiptune-with-orchestration register vendors); generated via LLM-driven music tools (current state of LLM music generation is variable); commissioned. Out of scope for this doc; drax + Matt decision when audio polish work begins.

### Q5 — Three-Trials-per-season variance

All three Trials in a season use this same six-phase ritual. Open: should the act-3 Trial (the season's culmination) get an *amplified* version of the ritual (extended approach, more elaborate cinematic frame, two Spirit Guide voice lines instead of one, etc.)? My instinct: **the act-3 Trial should feel heavier without breaking the structural pattern.** Amplification via *what the cinematic frame shows* (the act-3 Trial's boss gets the most distinctive cinematic-aura signature) and *the Spirit Guide's voice register* (act-3 Trial's lines carry more weight) — but the phase count and ritual shape stay the same. Per spirit-guide-voice.md's Beatrice arc: the Guide's voice register has warmed by act 3 anyway.

---

## What this DOESN'T do

- **It does not specify the Passage moment's ritual.** The Passage (death-offered transformation) has its own design intent which sits in cosmology-reincarnated.md § "The Passage" but is not yet authored as a separate ritual doc. A `passage-moment-ritual.md` companion doc is queue-worthy but not yet in the work plan. Surfaces if drax dispatches Passage UX work.
- **It does not specify the ascension moment's ritual.** Ascension is the season's climax; happens once per season; deserves its own ritual doc when Court / Earth-Self hub implementation nears. Parked.
- **It does not specify combat mechanics or boss kits.** Those are file 32 § 11 territory and engine-generation territory; this doc presupposes them.
- **It does not specify multi-Trial dynamics.** Whether Trial 2's framing is informed by Trial 1's outcome (e.g., the Spirit Guide referencing the prior Trial's path) is open. My instinct: yes, *yes the Spirit Guide should reference prior Trials within a season* — that's continuity-of-relationship between Guide and player. Implementation territory; not blocking.

---

## Cross-references

- `cosmology-reincarnated.md` § "The Trial" / § "The Mirror" / § "The Passage" — cosmological frame
- `naming-triad.md` — universal frame + per-season variants
- `enemy-visual-legibility.md` § S4 (Trial cinematic frame) + § S7 (Mirror exception) + § S3 (cinematic-tier aura)
- `embodiment-narrative-layer.md` — per-embodiment vocabulary for trial-boss and Mirror presentation; injury/death vocabulary at Trial resolution
- `style-register.md` — HD-2D-pixel register; narrative-moment-tier for the cinematic frame
- `court-of-forms.md` — what the Trial's outcomes accumulate into (post-season ascension into the Court)
- `gandalf-design-lineage.md` Layer 2 (Diablo II quest-reward-bundle precedent) + Layer 4 (Hades boon-offer ritual; Souls fog-gate)
- File 32 § Section 11 — Trial body-swap mechanical substrate
- File 33 — per-act SP scaling (4/7/9); per-Trial resistance bonus (+10% / +5%)

**Forthcoming (not yet authored; consumed by this doc):**
- `spirit-guide-voice.md` (Phase 2 work-queue #3) — Spirit Guide voice register specifics; the Trial-moment voice lines integrate when that doc lands
- `passage-moment-ritual.md` (suggested addition; not yet in work queue) — the Passage's ritual companion to this doc

---

## Maintenance protocol

When drax dispatches Trial-moment implementation work:

1. Re-read this doc with drax.
2. Convert the six phases into demo-side routines: approach signaling, threshold cinematic frame, choice screen UI, transition routine, combat-with-Trial-aura, resolution sequence.
3. Resolve open questions (Q1-Q5) with Matt before locking implementation details.
4. Per-seam coordination: rocket / star-lord emit the data drax consumes (trial encounter flags, seasonal variants, Spirit Guide voice lines).

When the engine adds new Trial-affecting capability (Track A B-series work; eventually Engine 2):

1. Re-check the six phases for new presentational requirements.
2. Amend this doc if new affordances change the ritual shape.

When spirit-guide-voice.md lands:

1. The Trial-moment voice lines (Phase 2 + Phase 6) become cross-referenced to that doc's voice-register specifications.
2. The Beatrice-arc (reserved → warmed → companion register) applies to which Trial the player is encountering (Trial 1 = reserved; Trial 3 = companion).

— gandalf, with Matt's standing approval on the canonical patterns this doc consumes (2026-05-15)
