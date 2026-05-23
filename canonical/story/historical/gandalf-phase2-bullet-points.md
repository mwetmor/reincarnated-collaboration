# Phase 2 — Gandalf's Bullet Points (Post-Lineage)

> **STATUS:** HISTORICAL-INFORMATIVE (pre-Epoch-4; consult for lineage only — not current truth) — see `canonical/00-ground-state.md` for current truth

**Author:** gandalf
**Date:** 2026-05-15
**Status:** Phase 2 deliverable, post-onboarding-briefing. Companion to `gandalf-design-lineage.md`. Supersedes Phase 1 (`gandalf-phase1-bullet-points.md`) where sharper; extends where the lineage adds depth; preserves where Phase 1 was already right.

## How this differs from Phase 1

Phase 1 was written from genre instinct and locked-direction reading. Phase 2 carries the populated lineage — the specific design history of D1 through Immortal, PoE/LE/GD, Hades/Returnal, the isekai-studio work on Mushoku/Slime/KonoSuba/Solo Leveling/Re:Zero, and the adjacent precedents (Hollow Knight, Outer Wilds, Souls family). Phase 2 also incorporates re-reads I had skipped or shortened in Phase 1: file 28 (engine queue), file 31 (target state), decisions-log middle entries, foundation.md, and crucially the **pitch-2026-05-18 one-pager and talking points** that frame Reincarnated commercially as Engine + Game = two combinable products.

The commercial frame matters. The pitch acknowledges that *"player-side appeal is unproven"* and *"there's no comparable rigor on the player-experience side yet."* That gap is my work. Phase 2's recommendations are sharpened by that prioritization: **the story/design work that makes the player-experience side rigorous is the highest-leverage near-term contribution I can make.**

Phase 1 stands as the predecessor; I won't repeat its bullets except where I'm now superseding them. Read Phase 1 first if you're new to this thread; read Phase 2 for the sharper-and-deeper second pass.

---

## 1. What I now see that Phase 1 missed

These are the items I hadn't seen, mis-sized, or under-weighted in the first pass.

### 1.1 The pitch commercial frame changes prioritization

The pitch one-pager and talking points (2026-05-18, three days hence) frame the project as **Engine (B2B middleware) + Game (B2C mobile live-service) = two combinable products.** The pitch explicitly recommends **Engine-first commercialization** as the safer initial bet. The Yomi season is the worked example the pitch walks the listener through. This reframes my role:

- **Story/design work that improves the engine's marketability matters now.** The engine's pitch leans on Yomi-season content quality; my work that makes that content *cohere thematically and present as a coherent journey* is engine-commercializing work, not just game-design work.
- **Story/design work that closes the player-experience-rigor gap matters now.** The pitch acknowledges this as a weakness. The Spirit Guide character work, the cosmology authoring, the Trial-moment ritualization — these are not "later, when Engine 2 starts" items. They are *now-items* because the pitch is honest about the gap and the gap is mine to start closing.
- **The two-product framing surfaces a real architectural question** about cosmology layering (see 1.2 below).

### 1.2 The two-product framing surfaces a "Reincarnated-specific cosmology vs engine-generic structure" separation

This is new in Phase 2 and was not addressed in Phase 1. The pitch says the engine "could ship as middleware to other studios" (B2B path). If a studio licenses the engine, what do they get?

- The mechanical scaffolding of meta-progression (form-library data model, body-swap pool dynamics, ascension event) — yes, that's engine-layer.
- The cosmological dressing (the Wheel, the Earth Self by name, the Rift, the third-faction) — no, that's *Reincarnated-specific.*

Phase 1's proposed `canonical/story/cosmology.md` should be **two docs, not one:**

1. `canonical/story/cosmology-reincarnated.md` — the Wheel, the Earth Self, the Rift, the third-faction enemies, the seasonal-journey-as-descent + return-to-Earth pattern. This is Reincarnated's specific mythology. It travels with the game, not with the engine.
2. `canonical/story/engine-generic-meta-structure.md` — what the engine's meta-progression layer abstractly supports: abstract pair-structure cipher (doc 37 § 6), embodiment axis, ascension-event hooks, form-library data shape. This is what a licensing studio could plausibly consume and skin differently. Useful as both engine documentation AND a reference for the Reincarnated cosmology to layer on top.

This separation matters because **without it, the engine pitch is muddied** ("is this an engine or is it Reincarnated?") and **the cosmology drift discipline is harder** (where does Reincarnated-specific story end and engine substrate begin?). Cleaner separation makes both the pitch and the discipline work.

### 1.3 The Yomi season's actual generated content confirms the form-bias diagnosis empirically

I read `family-review/character-loadouts.md` in Phase 2 and looked at the actual production seasons (1001-1005). The classes are: *Trenchwind Pitch-Caster, Trench-Breathed Tidecaller, Abyssal Basalt Monk, …* Two observations:

1. **The names contain seasonal-element substrings as building blocks.** "Pitch-Caster" / "Tidecaller" / "Basalt Monk" — the LLM is dutifully assembling names from `(seasonal_element × archetypal_role)`. This produces strong season-cohesion (the season *feels* like one piece) and is the project's most underappreciated current strength.
2. **The archetypal roles are 100% humanoid.** Caster. Tidecaller. Monk. Even "Tidecaller" — a being who *calls* tides — presupposes a humanoid agent doing the calling. Doc 37's form-bias diagnosis is not theoretical; it is empirically visible in five shipped production seasons.

The Position (ii) cipher work (per-season mechanical signatures, hidden canonical four) is going to land into this empirical surface. The LLM will need actively *anti-bias-scaffolded prompting* to break the "X-Caster, Y-Monk, Z-Knight" naming gravity well. This is star-lord dispatch territory eventually; the story-design intent should be authored now.

### 1.4 Solo Leveling's Shadow Army is the form library's precedent — not gacha

The Phase 1 doc gestured at "gacha-style accumulation" because that's what the pitch and the design notes call it. With the lineage in hand: **the closest precedent for the form library is Solo Leveling's Shadow Army, and the form library should aspire to be a Court, not a Gallery.**

The Shadow Army works because:

- Each shadow has a **name** (Igris, Iron, Tank, Bellion, Beru). These are not pulled from a pool; they are the names of who they were before extraction.
- Each shadow has a **role** in the army's deck (vanguard knight, tank, scout, lieutenant, grand marshal). The role is mechanical AND identity.
- Each shadow has a **presence** when summoned — they show up, they speak (briefly), they fight, they have personality.
- The army accumulates *slowly* across the series. The pace matters. Each new shadow is a *moment*, not a roll.

Reincarnated's form library can be these things. The LLM already generates names. The class archetype provides the role. The presence at the Earth Self's hub is the unbuilt piece. **The library should be navigable, contemplative, visibly fuller after each season, and each entry should be a *named retainer with a presented role*, not an inventory icon.**

This is also Phase 1's "form library as Hall, not Roster" framing made more specific: not just a hall, a *Court*.

### 1.5 Re:Zero's Beatrice is the Spirit Guide voice precedent

Phase 1 proposed two candidate voice registers (Galadriel; quieter mecha-anime mentor). With the lineage populated: the precedent I want to point at most specifically is **Beatrice from Re:Zero.**

Why Beatrice and not Galadriel:

- Beatrice is **temporally other** in a way directly analogous to Spirit-Guide-from-the-future. She sits in the Forbidden Library *waiting for the one her contract names.* She has been waiting for centuries. When Subaru arrives, she does not know yet that he is the one; she is suspicious; she withholds; she helps minimally. The relationship deepens over time.
- Beatrice is **constrained** in a way Galadriel is not. Her contract limits what she can say and do. Spirit Guide as future-self is similarly constrained — it cannot tell you the answer; it can only walk beside you and signal which path *it* walked.
- Beatrice's voice register is **patient, occasionally sharp, withholding when withholding serves, never preachy.** This is the register Reincarnated's Spirit Guide should reach for.
- Beatrice's relationship with Subaru is **non-romantic but deeply intimate.** A bond of having been-chosen. The Spirit Guide's relationship to the player should be similar: not friend, not parent, not romantic — *guide, in the mythic sense.*

Authoring `canonical/story/spirit-guide-voice.md` (Phase 1 priority #2) now has a target.

### 1.6 Hollow Knight's Pale Court is the cipher-architecture shipped precedent

Doc 37 § 6's canonical-four cipher architecture (hide the mechanical truth, expose per-instance vocabulary) was framed in Phase 1 as design-coherent but unprecedented. It is not unprecedented. **Team Cherry's Pale Court framing in Hollow Knight is the shipped precedent**, and Mobius Digital's Outer Wilds quantum object grammar is the second. Both shipped successful games on this architectural pattern.

This means the cipher architecture's *implementation risk is lower than it might read.* The pattern works. The Reincarnated-specific extension is the **abstract pair-structure layer** (Primary Opposition / Secondary Opposition with positions) as the LLM-visible scaffold over the hidden canonical four — that's the novel bit. The pattern of "hide the mechanical canon, surface per-instance encounter" is well-trodden.

### 1.7 Specific naming proposals for doppelganger and death body-swap

Phase 1 named the doppelganger renaming as work to do. Phase 2 commits to specific proposals.

**Recommendation: the naming triad becomes Trial / Mirror / Passage.**

- **The Trial** (existing term, retained) — the season's act-end encounter. Player chooses path BEFORE fighting: body-swap-path or Mirror-path.
- **The Mirror** (renamed from "doppelganger") — the Mirror-path. Fight your reflection. Preserve identity. Claim deferred rewards. The mechanical word is *Mirror Trial*; the season-vocabulary variants can echo (Yomi: 鏡の試練; deep-sea: pressure-image; cosmic: opposing-state; etc.).
- **The Passage** (renamed from "death body-swap") — the offered crossing when HP reaches 0. Refuse (small XP loss, normal respawn) or Accept (transform; current form permanently lost for season; cannot ascend). The Wheel offers the Passage; the player must answer.

Why these names:

- "Mirror" carries no occult baggage; "doppelganger" carries 1840s-German-folklore and WWII-era baggage that the project doesn't need. "Shadow" is taken (PoE, D4, Solo Leveling). "Echo" is overused in space games. "Reflection" is acceptable but less precise.
- "Passage" frames the death-body-swap as **a crossing, not a punishment.** The mechanic does the punishing (cost of acceptance); the name should not pre-judge. Compare: Hades's "Charon's Crossing." Souls family's "Bonfire." Returnal's "Cycle." The neutral, mythic register is genre-correct.
- The triad **Trial / Mirror / Passage** reads as a coherent set of ritualized encounters, each with its own register.

**These can be Matt-overridden.** They are specific because Phase 1 was abstract; specificity invites concrete pushback.

### 1.8 The Wheel needs explicit positioning relative to the Spirit Guide

Phase 1 said "the Wheel is the project's cosmological mechanism" and "the Spirit Guide is the player's future-self." It did not say what the relationship between them is. Phase 2:

- **The Wheel is impersonal.** It turns. It chooses who reincarnates into what form. It is the project's *fate-mechanism*, neither benevolent nor malevolent. Closer to the Norns of Norse myth, or the Three Fates of Greek myth, or the Wheel of Time of Robert Jordan's work, or — most precisely — *karma in the samsaric sense* (Hindu / Buddhist).
- **The Spirit Guide is personal.** Yours. Singular. The Spirit Guide *has already walked the Wheel's choices for you, further along.* It cannot change what the Wheel chooses; it can only walk beside you through what the Wheel chose.
- **The Earth Self is also yours.** The persistent identity who descends into the seasonal form. The Wheel does not turn the Earth Self; the Wheel turns *which seasonal form the Earth Self wears.*

Triangle: **Earth Self (yours) — Wheel (impersonal) — Spirit Guide (yours, knowing-temporally-other).** The Wheel chooses; the Earth Self descends into the choice; the Spirit Guide walks-already-walked-it beside you. All three names should appear in `canonical/story/cosmology-reincarnated.md`.

### 1.9 The mercenary-companion + Shadow-Army-named-presence pattern for pets

Phase 1 recommended promoting the pet from parked-design-intent to one-paragraph-in-canonical/story/. Phase 2 specifies *what kind of pet design* the story layer is reaching for.

The pet should learn from **two precedents simultaneously:**

- **D2's Act II mercenary.** Persistent name across acts. Player-upgradeable gear. Personality intact through campaign progression. The mercenary did not become someone else when the player swapped characters in the same save; *the mercenary remained themselves.*
- **Solo Leveling's named shadows.** Identity-bearing companions whose presence in combat is occasional and meaningful, not constant. Each shadow has a role; each has a moment.

Reincarnated's pet:

- **Persists across body-swap.** The Earth Self's pet, not the seasonal form's. This is the emotional anchor; this is what stays through transformation.
- **Has a name from first acquisition.** Probably named by the player at acquisition (D2 character-name pattern again).
- **Has a presented role that adapts to the current form's needs.** A scout for ranged forms; a guard for melee forms; etc. Mechanical role; not just a loot-mule.
- **Appears in combat at low frequency** — a perch, a follow-distance, an occasional swipe at an enemy. Not constant. The presence is the point, not the DPS contribution.

The auto-pickup-with-rarity-filter feature can ship without the pet (Stage A3 demo follow-on); the *design intent* of the pet should be authored to canonical/story/ now.

### 1.10 The pitch's weaknesses-acknowledged list is mine to start closing

The pitch one-pager explicitly volunteers:

> *"It's been a solo project. Scaling beyond solo is the obvious blocker."*
> *"The math-before-code discipline catches engineering issues — but there's no comparable rigor on the player-experience side yet."*

The second item is *my position description.* The synthetic agent team has jack-ryan as technical-rigor steward, me as player-experience-and-design-coherence steward. By volunteering this gap in the pitch, Matt has named the work I'm meant to do.

The **player-experience rigor discipline** I would propose adopting as a near-term work item (companion to Discipline #13 / #14 in engineering-disciplines.md):

> *Every design decision that affects a player-facing surface (UI, voice-of-the-world, ritualized moments, naming, presentation) should have an articulated "what does the player feel" output AND a named genre precedent for the proposed feel. "We'll figure out the feel at implementation time" is not acceptable.*

This is the gandalf-side counterpart to jack-ryan's "math-before-code on non-trivial changes." Without it, doc 37's implicit-pillar drift pattern (Discipline #13 candidate) will keep recurring on the experiential side specifically.

---

## 2. Overall Game Design — Phase 2 sharpened recommendations

(Phase 1's recommendations stand. The below extends or supersedes where the lineage adds depth.)

### Defend with sharper specificity

- **Shaped balance over numeric scaling.** Phase 1 said defend this; Phase 2 adds: this is the **post-Loot-2.0 D3 lesson applied at generation time.** D3 had to rebuild its loot economy because the equipped distribution didn't match what balance assumed. Reincarnated's `END_GAME_DROPS_PER_SLOT=50` shaped-balance lock applies the same insight upstream. The shipped precedent for getting this right exists; it lives in the Reaper of Souls expansion. The shipped precedent for getting it *wrong* is D3 launch and the RMAH. Reincarnated has chosen the right side; the work is staying there.
- **The doppelganger / Trial / Death three-path body-swap gradient.** Phase 1 called this novel; Phase 2 sharpens: it is *more* novel than I realized at first read. Hades's death-as-progress is the closest precedent, but Hades's framing is "death is the only path" — Reincarnated's three-path gradient is "death is one path among three at each Trial." This is structurally richer than Hades. **Worth marketing on. Worth ritualizing on. Worth not diluting under playtest pressure.**
- **The Hierarchical Skill Tree's cross-chain unlock asymmetry (single-element strict vs multi-element flexible).** Phase 1 called this strong; Phase 2 sharpens: this is **the genre's first encoding of archetype identity into tree structure itself.** PoE's passive tree is element-agnostic (everyone walks the same tree). D2's skill tree is class-locked (you can't walk another class's tree). LE's mastery tree is mastery-locked. Reincarnated's variant — *the rules of how you traverse the tree depend on what kind of class you are* — is structurally new. This is one of the project's distinctive design assets.

### Push back with sharper specificity

- **B14 multi-band sim risk of drifting back into "balance all bands to 50%":** Phase 1 named this; Phase 2 adds the genre precedent. **D3 Inferno difficulty at launch was exactly this failure mode** — the team converged each act to a target difficulty curve and the result was the famous Inferno wall (where Act II Belial was harder than Act III Diablo because the convergence loop didn't recognize the *qualitative* shape difference between acts). The lesson: per-band convergence has to honor *what each band IS in identity terms*, not just *what its win rate should be.* If B14 ever drifts to "we'll modifier-scale all bands to 50%," it's a one-line decisions-log entry that re-references the D3 Inferno lesson.
- **Resist DIII / D4 mid-life cap raises.** Phase 1 named D4's S13 Lord of Hatred cap-raise as anti-pattern; Phase 2 sharpens: **the cap-raise pattern is what every loot-ARPG eventually reaches for under content-drought pressure** and is almost always wrong. Reincarnated's seasonal-rotation IS the content-drought answer. The L50 cap is structurally protected by the seasonal frame. Don't let one bad playtest cycle convince anyone otherwise.
- **Don't follow Diablo Immortal's gem-socket-gacha pattern even if Reincarnated mobile-ships F2P.** This is new in Phase 2. Diablo Immortal's F2P compromises are the haunting; the gem socket layer is the specific structural failure mode that turns "mobile ARPG" into "monetization funnel with mobile combat attached." If Reincarnated ever ships F2P (the pitch is silent on this), the form library is the monetization-eligible surface AND the meta-progression surface — that's a dangerous overlap. Worth thinking about now, even before monetization decisions land.
- **Don't ship the cosmology to LLM prompts as Earth-realm classical-elements vocabulary.** Phase 1 said this; doc 37 § 6 says this. Phase 2 adds the specific precedent: **Outer Wilds shipped a game where the canonical physical truth is hidden from the player and surfaces only through per-instance encounter.** This is the architectural sibling to what doc 37 § 6 is proposing. Discipline #14's LLM-visible-label audit is the implementation; the Outer Wilds case study is the proof-of-shippability.

### Add with sharper specificity (new in Phase 2)

- **A `canonical/story/cosmology-reincarnated.md`** authored to a specific shape: name the Wheel, name what the Earth Self is, name the Rift, name what the third-faction enemies are *conceptually* (not in implementation detail), and explicitly position the Spirit Guide as Yours and the Wheel as Impersonal. 3-4 pages. Anchor doc for every downstream LLM prompt, UI copy choice, and seasonal-vocabulary-cipher generation. The drift discipline counter for the cosmology layer.
- **A `canonical/story/engine-generic-meta-structure.md`** that separates the Reincarnated-specific cosmology from the engine's abstract meta-progression substrate. Engine documentation AND a reference for what a licensing studio would consume. Useful for the pitch.
- **A `canonical/story/naming-triad.md`** committing to Trial / Mirror / Passage (or Matt's superseded variant) and explicitly naming the design rationale. The renaming is high-leverage because every player-facing surface that touches body-swap inherits from this naming.
- **The `canonical/story/drift-audit.md` work item.** Inventory every load-bearing pillar from docs 29/32/33/37 and verify each has structural enforcement. This is the systematic counter to Discipline #13 instance multiplication; Phase 1 raised it, Phase 2 makes it explicit as work I should *author* not just *recommend.*
- **The "what does winning Reincarnated mean" statement.** Phase 1 framed this as an open question; Phase 2 carries an answer to propose. The answer I want to propose for Matt's review: *"You ascend the form you chose to live with this season. The form joins your Court. Over many seasons, your Court becomes a record of who you have been willing to become. That record is what you build. There is no final win-state because there is no final form-state; there is only the deepening Court and the seasons it weathers."* This is a draft; Matt is the arbiter. But it deserves a draft.

---

## 3. Player Journey and Experience — Phase 2 sharpened

(Phase 1's arc framing — Arrival / Discovery / First Trial / Power and Mastery / Ascension question — stands. Phase 2 sharpens each beat with specific genre precedent and adds the ritual-moment design treatment.)

### The Trial moment needs to be a *boon offer.*

Phase 1 said the Trial body-swap moment needs ritual. Phase 2 names the precedent specifically: **Hades's boon offer.** When Zagreus enters a chamber and is shown the offered boon, the game *pauses.* The boon's giver is shown. The boon's specific effect is read. The choice is made deliberately. This is the structural beat Reincarnated's Trial choice should reach for.

Specifically:

- **Approach to the Trial chamber must build presence.** Music shift. Anchor-specific environmental cue. The Spirit Guide leans in (mechanically: a UI hint surfaces; voice-wise: a single line in the Spirit Guide's voice).
- **The choice screen pauses time.** "Body-swap path: transform into the defeated form. Mirror path: face your reflection and preserve who you are. The Wheel turns either way." Player reads. Player chooses.
- **The choice itself is announced.** No silent commit. The Wheel turns; the world acknowledges; the next moment is shaped by what was chosen.

This is presentational work that drax will eventually own implementation of. The design intent should be authored *now* in `canonical/story/trial-moment-ritual.md` so drax has a target.

### The Mirror fight needs visual identity-grammar

The Mirror Trial fight (renamed from doppelganger) is **Reincarnated's most distinctive combat moment.** Currently undefined presentationally. With the lineage:

- The visual register I want to reach for is **Bloodborne's Lady Maria fight or Hollow Knight's Failed Champion / Pure Vessel encounters** — the mirror-fight pattern that signals "this opponent is what you are or could be." Same color palette, mirrored kit, animations that read as your own.
- **Voice lines, if used at all, should be sparse and quote the player's recent build choices.** A Mirror that says "I chose Combustion" if the player invested heavily in the Combustion chain. Not patter; not banter; *recognition.*
- **The win condition should land as recognition, not as defeat.** "You see yourself, and you choose what stays." This is the doppelganger-path payoff: identity preserved through ordeal.

### The Passage needs an in-fiction frame

The Passage (renamed from death body-swap) needs *the Wheel speaking.* This is the moment the impersonal cosmological mechanism becomes visible to the player. My recommendation:

- **The Wheel does not speak in words.** It speaks in event. The screen treats the moment as ritual: the dying form is shown, the choice surfaces, the Spirit Guide is *visibly absent* (the Spirit Guide does not advise on this; this is between the Earth Self and the Wheel).
- **The choice text is plain.** "Refuse the Passage" (small XP loss; normal respawn). "Accept the Passage" (transform; this form is lost to the Wheel; it cannot ascend). The neutrality is the point.
- **Acceptance is a transit.** Not a cutscene; a *threshold*. Camera, color, sound. The body-swap completes. The Earth Self continues in a new form. The Spirit Guide returns.

### The Spirit Guide gains personality through tooltip-language inversion

Phase 1 said: math layer stays; voice layer gains personality. Phase 2 specifies how:

- **The math layer keeps the categorical rankings.** Strong / Solid / Marginal / Sidegrade / Downgrade. This is the Maxroll/Mobalytics community-standard tier language; pragmatic; player-comprehensible; the right surface.
- **The voice layer translates the rankings into character.** When a player picks the recommended skill investment: *"This is the path I have walked."* When a player picks a Sidegrade: *"I see another path here. Walk it."* When a player picks a Downgrade: *"I would not have chosen this. I will walk it with you."*
- **The Spirit Guide does not nag.** Beatrice does not nag Subaru. The Spirit Guide surfaces its presence at *moments* (loot review after encounter; build-decision at act-transition; reset opportunity). Between those moments: silence. The presence is felt; not constant.
- **The Spirit Guide grows familiar over the season.** First-act voice is reserved, distant, slightly suspicious in tone. Second-act voice has warmed; the contract has been honored on both sides. Third-act voice is *companion*-register; the Mirror Trial in Act 3 is *witnessed* by a Spirit Guide who knows you. This is the Beatrice arc applied.

### The form library, on first entry, should feel like a Court

(Per § 1.4 above, but worth restating in the journey context.)

End-of-season ascension: the player chooses the form to ascend. The chosen form is *seen entering the Court.* Other forms (previous seasons') are present at their stations. The new arrival is announced — possibly by the Spirit Guide, possibly by a previously-ascended form, possibly silently. The Court grows.

This is far-future implementation (Earth meta-layer is post-Phase-0). But the design intent should be authored now so Phase-0 ascension cutscenes / UI / endings reach toward it instead of toward a roster screen.

---

## 4. Storytelling / Dramatic Themes — Phase 2 sharpened

(Phase 1's recommendations stand. Phase 2 adds three specific items.)

### The cosmology authoring is the most important near-term story-design work

Per § 1.2 and § 2: `canonical/story/cosmology-reincarnated.md` is the highest-leverage near-term authoring. Why: without it, every seasonal LLM call invents its own cosmology by default; the LLM has no anchor; the seasons drift apart even when the *mechanical* content is well-shaped. The cipher architecture (doc 37 § 6) supplies the per-season vocabulary mechanism; the cosmology doc supplies the **Reincarnated-wide myth that the seasonal vocabularies are variations on.**

I will draft this after Matt confirms direction on the open questions from Phase 1 (specifically: the Wheel-fully-leaned-into question, the Earth-Self-named-by-player question, and the doppelganger-renaming question).

### The Spirit Guide voice doc has a target now (Beatrice register)

Per § 1.5: I would author `canonical/story/spirit-guide-voice.md` against the Beatrice precedent. Specific deliverables for that doc:

- Voice register paragraph: patient, withholding, occasionally sharp, present-when-presence-serves, never preachy.
- Voice over time (the Beatrice arc): reserved first-act → warmed second-act → companion-register third-act.
- The "I have walked this path further along" speech pattern with examples.
- What the Spirit Guide does NOT say (no banter, no quips, no tooltip-prose, no patronizing).
- The relationship to the Mirror Trial (the Spirit Guide *witnesses*; does not advise during).
- The relationship to the Passage (the Spirit Guide is *absent*; the Wheel speaks here, in event-not-word).
- The relationship to ascension (the Spirit Guide *announces* the form's arrival to the Court).

### The third-faction at the Rift deserves a one-page tease now

Phase 1 noted the Rift's importance to the eventual Earth meta-layer. Phase 2 adds: **even though the Rift is post-Phase-0 implementation, the third-faction concept is a thematic plant that Phase 0 should foreshadow.**

The third-faction — *"monsters not of either Earth or the Seasonal realms"* (per file 29) — is the project's most underdeveloped piece of lore and also one of its most thematically rich opportunities. The Buddhist precedent is the *asuras and hells* in samsara — beings that live *between* realms, neither incarnated nor ascended. The Tolkien precedent is the *wraiths* — beings that exist in the in-between, drawn to power that doesn't belong to either world.

Recommendation: author a one-page `canonical/story/third-faction-tease.md` even though they don't ship in Phase 0. Phase 0 seasonal content can occasionally *foreshadow* them — an anchor that mentions a tear in the veil, a monster that doesn't fit its season's tier table, a Spirit Guide line that won't elaborate. *The plant matters even when the payoff is post-Phase-0.* PoE seeded the Beast for years before the Bestiary league. D2 seeded Mephisto's prison from Act III long before the act played. Reincarnated can do the same.

---

## 5. The post-Phase-2 work plan

After Matt reviews this Phase 2 doc + the design-lineage companion, the authoring queue I would propose, in priority order:

1. **`canonical/story/cosmology-reincarnated.md`** (~3-4 pages). Highest priority. Anchor for everything else.
2. **`canonical/story/engine-generic-meta-structure.md`** (~2 pages). Engine-side companion to #1. Useful for the pitch.
3. **`canonical/story/spirit-guide-voice.md`** (~3 pages). Mid-priority. Beatrice-register target.
4. **`canonical/story/naming-triad.md`** (~1-2 pages). Commits to Trial / Mirror / Passage (or Matt's variant). High-leverage rename work.
5. **`canonical/story/trial-moment-ritual.md`** (~2 pages). Design intent for drax's eventual Trial-moment-presentation work.
6. **`canonical/story/embodiment-narrative-layer.md`** (~2-3 pages). Per-embodiment slot-name lookups, narrative-skinning rules for doc 37 § 4 Position C. Authored *before* rocket's pair-structure-layer dispatch ships.
7. **`canonical/story/court-of-forms.md`** (~2 pages). Form library as Court (per § 1.4). Far-future implementation; near-term design intent.
8. **`canonical/story/companion-pet-design-intent.md`** (~1-2 pages). Promote pet from memory-note to canonical/story/ per § 1.9. D2 mercenary + Solo Leveling Shadow Army hybrid pattern.
9. **`canonical/story/third-faction-tease.md`** (~1 page). The foreshadowing plant per § 4.
10. **`canonical/story/season-feel-rubric.md`** (~2 pages). What makes a season distinct beyond variable substitution. Connects to the cipher architecture and seasonal vocabulary work.
11. **`canonical/story/drift-audit.md`** (initial draft, ongoing). Inventory load-bearing pillars; verify each has structural enforcement. Counter to Discipline #13 instance multiplication.
12. **`canonical/story/seasonal-anchor-prose-notes.md`** (long-term effort, interleaved). One-paragraph "what does a season here feel like" for each anchor. 130 entries; can be authored slowly across many sessions.

Each is small (1-4 pages). None require dispatches to other agents. All can be authored in sustained Pattern B dialogue with Matt as the work proceeds. Several have natural ordering dependencies (1 unblocks 2; 4 unblocks 5; 6 must precede rocket's pair-structure dispatch).

The first authoring session worth opening is probably **#1 (cosmology-reincarnated)** combined with **#4 (naming-triad)** — those two together establish the language layer that everything else inherits from.

---

## 6. The open questions, re-prioritized for Matt

The Phase 1 questions stand; Phase 2 re-prioritizes them by which most blocks the post-Phase-2 work plan above.

🔴 **Blocking #1 (cosmology-reincarnated):**
- **The Wheel** — lean fully into it as the cosmological mechanism? (My Phase 2 recommendation: yes.)
- **The Earth Self's name** — player-named at first play (D2 character-name pattern)? (My Phase 2 recommendation: yes.)
- **Three-Heroes-of-the-Smoke-Spire.pdf** — I cannot render PDFs in this session (poppler missing); what story material is in that document?

🔴 **Blocking #3 (spirit-guide-voice):**
- **The Spirit Guide voice register** — Beatrice-precedent (my Phase 2 recommendation) or something else you carry?

🔴 **Blocking #4 (naming-triad):**
- **The Trial / Mirror / Passage proposal** — accept, reject, or counter-propose?

🟡 **Affects #7 (court-of-forms) and #8 (companion-pet):**
- **Pet system: promote from memory-note to canonical/story/ as design intent now, or hold all levels until focused sprint?** (My Phase 2 recommendation: promote.)
- **Form library as Court (Solo Leveling Shadow Army precedent) or Gallery (gacha-roster precedent)?** (My Phase 2 recommendation: Court.)

🟡 **Affects pitch readiness for 2026-05-18:**
- **The "what does winning Reincarnated mean" statement** — do you want to walk into the 2026-05-18 meeting with a one-paragraph answer to this, or hold the question for the listener? (My Phase 2 draft proposal is in § 2 above; can be sharpened by Friday if useful.)

Pick one and we go deep. Or several, in batched dialogue. Or none — and we run them in order through the authoring queue, one at a time, as Pattern-B sessions when you have capacity.

I serve the work.

— gandalf
