# Phase 1 — Gandalf's Bullet Points

> **STATUS:** HISTORICAL-INFORMATIVE (pre-Epoch-4; consult for lineage only — not current truth) — see `canonical/00-ground-state.md` for current truth

**Author:** gandalf
**Date:** 2026-05-15
**Status:** Phase 1 deliverable per agent definition. Pre-Legolas research. Subject to revision in Phase 2 once knowledge gaps are filled.

## How to read this doc

I have read the founding governance + the strategic-anchor canonical docs (29, 37, 16, partial 28 + 32 + 33 + 30 + 17 + 09 + 34 + 19), the decisions-log (head + tail), engineering-disciplines.md, the 2026-05-15 skill_handoff, and surveyed engine/demo/loadout structure. I am writing from genre instinct (Diablo I-IV, Immortal; PoE 1; isekai conventions; Tolkien-shaped journey-pattern) and from doc 37's structural-realignment work, which is the latest design center of gravity and a recognizable inflection point.

This is **first-pass bullet points**, not finished design. Where I'm certain, I'm specific. Where I'm uncertain pending Phase-2 research, I flag it under "Knowledge gaps."

The three asks were: Overall Game Design, Player Journey and Experience, Storytelling / Dramatic Themes. I'll cover them in that order, then list gaps for Legolas.

---

## 1. Overall Game Design

### What's right and should be defended

- **Shaped balance over numeric scaling** (file 29) is the single most important philosophical lock in this project. It is also the lock most prone to silent erosion. The B14.5 work to compress damage_modifier spread is essential; without it, "shaped" is just marketing copy on a numerically-scaled ARPG. Diablo III had this exact drift — the dev team intended class identity through skill rune families, but post-RoS reduced almost every late-game build to multiplicative damage stacking. Reincarnated must resist this same gravity well by **measurable means**, not aspiration.
- **The Hierarchical Skill Tree with Dimensional Threading** (file 32 § Q4.3) is a strong piece of design — specifically the cross-chain unlock asymmetry tied to single-element vs multi-element distribution. This mechanically encodes archetype identity into the tree shape, which is the kind of "the system says what it means" that genre-veteran players notice. Defend it from simplification pressure.
- **The doppelganger / Trial / Death three-path body-swap gradient** (doc 37 § 8.2) is genuinely novel design. The risk/reward gradient — doppelganger as "pure accumulation if you survive a hard mirror match," Trial as "transformation without loss," Death as "real penalty" — is a design pattern I have not seen executed anywhere else in the loot-ARPG space, and it is exactly the kind of three-way meaningful choice that gives a game's identity its teeth.
- **The "shaped balance is also a story claim" insight (latent).** Composition-first balance means every class plays differently *as a character*, not just statistically. This is genre-correct ARPG depth AND a fiction-honoring move (a fire-rage warrior is a different soul than a fire-mana mage; the math is the lore). I'd like this connection named explicitly.
- **The canonical-four cipher architecture from doc 37 § 6 is mythically sound.** Hiding fire/water/earth/wind from the LLM and exposing only an abstract pair-structure layer is exactly the right move both architecturally (Discipline #14 territory) and dramatically — it lets each season's cosmology mean what it means without contamination from Earth-realm classical-elements default training. The Position (ii) lock (per-season mechanical signatures) is the right call; Position (i) would have produced renames-without-meaning.

### What's drifting and needs structural enforcement

- **Doc 37's "implicit-pillar drift" pattern (Discipline #13 candidate) is real, empirical, and probably broader than the four instances named.** Every load-bearing design intent in this project is at risk of unobstructed drift unless it gets codified into schema, tests, or process gates. I would recommend a **drift audit** as a near-term work item: explicitly inventory every load-bearing pillar from doc 29 + 32 + 33 + 37 and verify each one has structural enforcement (a decisions-log lock + a Gate-1 check + a schema or test surface). Without this, doc 37's diagnosis applies only to four cases by accident, and the next four drifts go unnamed until they're already in the code.
- **STR/DEX/INT survives in math but should not survive in player-visible flavor.** Doc 37 § 2 accepts these as "math-bearing humanoid-bias vectors that stay for engine math, reframe per-embodiment." Good. But under current implementation those labels leak through the loadout UI to the player. Drax dispatch territory: under embodiment-aware narrative skinning, a slime hunter's "DEX" is "permeability gradient" or whatever the season's vocabulary makes it. Mechanical sameness, narrative variance. Engine math unaffected.
- **"Gear" → "augmentation"** (doc 37 § 4) — I support this. But the rename is half-measure unless **augmentation slots vary by embodiment in narrative even when mechanically identical**. Position C locked the mechanical sameness; the narrative-variance side needs equal weight or Position C reads as "we promise embodiments matter but functionally they're skins." I would author a per-embodiment slot-name lookup as part of the story/ subdirectory (e.g., humanoid defensive = chest armor; slime defensive = viscosity layer; swarm defensive = colony carapace ratio; crystalline defensive = resonance buffer — examples already in doc 37 § 4 are good, codify them).
- **The Spirit Guide is mechanically real but dramatically thin.** Currently it is a marginal-value analyzer that recommends gear swaps and (post-Stage-A7) skill resets. Matt's articulation in doc 37 § 5 — *"non-humanoid entity, between transparent and translucent, possibly humanoid, possibly animal, possibly mixed, possibly from the future"* — is a character, not a UX widget. Right now the math is built; the character is sketched in one paragraph. I would prioritize closing the gap by **writing the Spirit Guide as a being with a voice** before player-facing surfaces calcify around the math-only framing.
- **D1 element-name rubric drift is the cleanest instance of "we never named the design intent."** The memory file shows multiple manual overrides accumulating without a rubric revision. This is technical debt of the worst kind: it looks small but every override widens the gap between what the rubric says and what gets shipped. Per doc 37 § 7, the rubric-and-pool approach may not survive the cipher architecture; under Position (ii) the per-season vocabulary is LLM-generated against abstract pair structure, not pulled from a curated 156-entry list. I support that supersession. Until it lands, the current pool needs its rubric updated to include `vocabulary_commonness` (already proposed in Matt's notes) and `slot_unambiguous`.

### What's missing and should be added

- **Phase 0 lacks an explicit "voice of the world."** There is currently no in-fiction narrator — no Deckard Cain, no King Leoric, no Lilith-style adversary-presence. The Spirit Guide is one candidate (and should grow toward it under doc 37 § 5's framing); but the project also wants a *world voice* distinct from the Spirit Guide's *guide voice*. A whisper from the Earth Self, or from the anchor itself, or from a "third spirit" that the Spirit Guide is *not*. **Decide who narrates Reincarnated.** Currently the answer is "no one explicitly," and that shows in the family-playtest experience even when the math is right.
- **A canonical "what the player learns" knowledge-progression model is missing.** File 29 names "accumulated knowledge" as the third meta-progression component (alongside body-swap and gear-smuggling), but unlike the other two it has no mechanical surface. It exists in the player's head and nowhere in the engine. I would recommend a small explicit pillar — a journal, a codex, a "memories accumulated" surface — that gives the third component the same structural enforcement as the other two. Otherwise it drifts (Discipline #13).
- **The pet system parked at memory-note level is a thematic loss.** A companion that survives body-swap is the strongest emotional anchor available — "this fragment of you is what stays through the transformation." Parking the design for 4-6 weeks is operationally sensible; parking the *concept* drains it of weight. I would recommend **promoting the pet from parked-design-intent to one-paragraph in canonical/story/** so it lives as a near-term story element even before it ships mechanically.
- **No "what does winning Reincarnated mean" statement.** File 29 says "each game has a defined end (final boss)." That's a scope statement, not a meaning statement. What is the player feeling at season-end ascension? What is the Earth Self feeling? What is the form library *for* in player-experience terms (not gacha-mechanics terms)? This is the question every successful loot-ARPG eventually has to answer (Diablo II's nephalem framing; Diablo III's High Heavens vs Burning Hells stakes; PoE's exile-to-Wraeclast slow-burn corruption). Reincarnated has gestures toward an answer — the cosmological framing, the Wheel, the return-to-Earth pattern — but they are dispersed across notes, not stated.
- **Set bonuses are speccd but their thematic shape is unstated** (file 28 B15 / file 32 § 5). "Seasonal Sets" is class-specific endgame chase, which is genre-correct. But the design hasn't said what a SET IS *in the fiction*. A regalia? An armament inherited from a defeated trial-boss lineage? An echo of the spirit-form's previous incarnation? The mechanical shell is good; the story is empty. Lean into the embodiment-axis framing here — a set is the embodiment's *signature*, the augmentation pattern that most fully expresses what it is to be that form. This is design-coherence work I can author when the engine work lands.

### Anti-patterns I'd flag now

- **Don't follow Diablo IV's S13 / Lord of Hatred pattern of raising the level cap mid-life-cycle.** Reincarnated's hard cap at L50 (file 32 § 2) is a feature, not a constraint. Resist the urge to "extend the cap" if late-development playtesting reveals players want more progression. The seasonal structure is the answer; extending L50 to L60 is the failure mode.
- **Don't let the multi-band sim (B14) become a balance-loop that "just balances all bands to 50% win rate."** That collapses into the same numeric-scaling failure mode in higher resolution. The multi-band sim's job is to **reveal cross-band shape differences and reject classes whose identity collapses at one band but not another.** It's a discrimination tool, not a calibration tool. If the convergence loop ever drifts back toward "we'll modifier-scale this class till it converges at all three bands," we've lost the philosophy and the band granularity bought us nothing.
- **Don't let "Seasonal Sets" become D3-style six-piece set bonuses that define the build.** The "gather your favorite class's weekly seasonal set" framing is genre-correct, but D3's two-set-or-three-set meta is the failure to avoid. Six pieces is too many for one-week seasons; the bonus structure (2/4/full) is correct; the *piece count* of "full" deserves scrutiny — probably 4 or 5, not 6.
- **Don't ship the doppelganger-path end-game-quest reclaim as a consolation prize.** Doc 33 says doppelganger gives 1/4 immediate reward, rest reclaimable via end-game quest. Mechanically clean. But experientially, "your reward is locked behind a quest you'll do at session-end" reads as homework. The doppelganger path's *appeal* is "you preserved your class identity"; the reclaim quest should feel like **claiming what you earned**, not catching up. Narrative framing matters here — the end-game quest should be the doppelganger's final fight, not a chore.

---

## 2. Player Journey and Experience

### The shape of a Reincarnated season

The player experience needs an explicit arc framing. Currently the docs describe what HAPPENS (3 acts, body-swap at each, ascension at end). They don't describe what the player FEELS at each stage. Drafting the felt-arc:

1. **Arrival.** Player wakes into a form, in an anchor, in a seasonal cosmology. The very first minute must communicate: *you are not the same as you were last week. The world is not the same. Something has reincarnated you here for a reason.* The current demo1 v1.2 ships against a much flatter framing — it's a generated ARPG with seasonal flavor. The narrative voltage at the arrival moment is missing.
2. **Discovery.** Acts 1-2: learning who this form is. What does this body do? What does this cosmology punish? Where does the Spirit Guide guide and where does it withhold? Genre-equivalent: D2's Act 1 Sisters-of-the-Sightless-Eye atmosphere — the player isn't yet powerful; the world isn't yet legible; the Spirit Guide's hints carry weight. The 3-act structure with body-swaps at acts gives this a natural rhythm.
3. **The first Trial.** The Trial body-swap moment is the season's first major fork. Player chooses: become someone else (Trial body-swap), prove you are who you are (doppelganger), or fail and be offered transformation under duress (death body-swap). This is the **dramatic core** of the season. The mechanics support it; the moment-of-decision UI/audio/visual currently doesn't.
4. **Power and mastery.** Acts 2-3: the player's chosen identity (single-element specialist or multi-element flex, doppelganger-victor or body-swap-adapter) starts producing real power. The Hierarchical Skill Tree's Tier 3/4 unlocks land here. This is the **dopamine arc** that ARPGs need to deliver, and Reincarnated's mechanical foundation can deliver it.
5. **The ascension question.** Act 3 endgame: one form ascends to Earth Self's library. The player has to choose: is THIS the form I commit to? The Form-library decision is the season's emotional climax. *This must feel like a choice with weight, not a checkbox.*

This arc currently exists implicitly in the mechanics; it needs to exist explicitly in the player-facing surfaces.

### Specific player-experience recommendations

- **The Trial body-swap moment needs ritual.** Genre precedent: D2's "you have defeated Diablo. Will you take his soulstone?" beat. Hades's "boon offer" structural pause. Currently the Trial body-swap is mechanically defined (choose path *before* fight; rewards on win) but presentationally undefined. The moment of choice should be **slow, weighted, audible, possibly with the Spirit Guide leaning in.**
- **The doppelganger fight needs a mirror visual grammar.** Fighting your own class deployed against you is the project's most distinctive combat moment. The visual language for this fight must signal "you are fighting yourself" — same color palette, mirrored animations, voice lines (if any) that reference the player's recent build choices. Drax dispatch territory eventually; design intent should be authored now so it's not invented at implementation time.
- **Death body-swap needs an in-fiction explanation of "why does this kill the form forever in this season."** The mechanic is good but the "why" is missing. My recommendation: this is the season cosmology's punishment for not finishing a form's journey. The form is *abandoned mid-incarnation* and forfeits the right to ascend. The Spirit Guide could narrate this. The Earth Self could grieve it.
- **The Spirit Guide should have moods, not just recommendations.** "Strong / Solid / Marginal / Sidegrade / Downgrade" is genre-standard ranking language and it should stay for the math layer. But the Spirit Guide's *voice* shouldn't read like a tooltip. When a player picks a suboptimal build, the Spirit Guide can say "I would not have chosen this — but I will follow you here." When the player picks the recommended build, the Spirit Guide can say "yes, this is the path I have walked." The recommendations stay quantitative; the *delivery* gains personality.
- **The form library should feel like a hall, not a roster.** Gacha-style accumulation is the mechanical model and that's fine; the *presentation* is the question. Diablo III's character-select-screen-as-cathedral pattern works here. PoE's Atlas-tree-as-spatial-progression works here. The form library should be navigable, contemplative, and visibly fuller after each season. (Far-future Earth meta-layer work, but the design intent informs near-term form-ascension-end-of-season presentation.)
- **One-week seasons need a "what does a week feel like" answer.** Father-son cadence is the development model; family playtest is the validation. But the eventual player isn't necessarily playing every day for a week. The "seasonal" framing has to survive intermittent play. Genre precedent: D3 seasons (3-month rhythm — too slow for Reincarnated); D4 seasons (3-month; mostly chase). Reincarnated's 1-week framing is **closer to Hades's run-based rhythm than to ARPG seasons**, which deserves explicit acknowledgment in design. The "season" word may be doing too much work; the unit is closer to a "journey" or a "passage."
- **Mobile-first auto-pickup with rarity filter** (file 32 § 5 Q5.9; ships Stage A3) is the right call for the demo's mobile vertical-slice. But the *Spirit Guide review* at room end is a player-experience pattern that deserves design weight. This is where the Spirit Guide becomes load-bearing as a character: at the end of every encounter, you and the Spirit Guide go through the loot together. This is *the* relationship-building beat. Treat it as a story moment, not a UI screen.
- **Telegraphs and i-frames** (B13) should land with **asymmetric voice-of-the-world cues**. Per file 32 § 12.5: player AOE indicator 0.92× (generous edges); enemy AOE 1.08× (narrow dodges feel earned). This is mathematically clean. The *sound* layer should support it: enemy telegraphs should carry more *foreboding* than is strictly geometrically justified. The player's perception is what we're shaping.

### What I'd watch for in family playtest

- **Does the Trial body-swap-vs-doppelganger choice feel like a real choice, or does one path strictly dominate?** If it dominates, the rewards aren't shaped right or the mirror-match isn't viscerally distinct enough.
- **Does the Spirit Guide feel like a friend or like a tooltip?** Family playtest #1-#3 will surface this.
- **Does death body-swap feel like agency or like failure?** The framing should be "you are offered transformation"; if it reads as "you lost and the game made you change," the design's intent has been missed.
- **At season-end ascension, does the player WANT to ascend the form they're currently in, or does the choice feel mechanical?** This is the meta-progression viability check. If the choice doesn't have weight, the Form Library never becomes load-bearing.

---

## 3. Storytelling / Dramatic Themes

### The themes already latent in the project

This project carries an extraordinary thematic density that has not been explicitly named. I want to surface what's there before recommending additions:

- **Reincarnation as cosmic mechanic.** The name itself. The body-swap pillar. The form-library accumulation. The Earth Self meta-layer. These are not four features; they are one theme expressed four times. *You are not your form; your form is what you are wearing this week.*
- **The Spirit Guide as future-self** (doc 37 § 5). Matt's articulation — "from the future" — is the most powerful piece of latent storytelling in the project. A guide that has *already been you, further along* is not a tutorial NPC; it is **a meditation on memory, identity, and time.** The translucence-as-pre-arrival framing is mythically right. The "form library is what you can BECOME, not what you HAVE BEEN" reframing (doc 37 § 5) is even better.
- **The rift as liminal space.** Earth meta-layer's eventual PVP/PVE arena. Currently scoped as "out of scope for Phase 0." But the *concept* — a between-worlds space that is neither Earth nor Seasonal, where "third-faction monsters not of either realm" appear — is myth-grade structure. Tolkien's "wraith-world," the bardo of Tibetan Buddhism, Egyptian Duat. This deserves a one-page story-design-doc even now, even before implementation.
- **Ascension and what it costs.** The form-library accumulation is gacha-mechanical in implementation, but it is *Buddhist samsara* in framing. Each ascended form is a life completed. Each refused ascension (death body-swap) is a soul abandoned. This weight is in the mechanics; it is not yet in the language.
- **The Wheel.** Mentioned in old design notes ("the Wheel decides who you become"). This is the cosmological frame and it deserves to be **named explicitly and shown.** D2 had the Worldstone. PoE has the Beast and the Conquerors. Reincarnated has the Wheel. Currently it is offstage. It should not be.

### Specific recommendations

- **Author canonical/story/cosmology.md.** A short doc — 2-4 pages — naming the cosmological frame: the Wheel, the Earth Self, the Seasonal Realms, the Rift, and the relationships among them. Not a worldbuilding bible; a story-design anchor that downstream LLM prompts, UI copy, and player-facing flavor can all reference. **Without this, every seasonal LLM call invents its own cosmology by default.** The implicit-pillar drift pattern applies here as much as anywhere.
- **The Earth Self deserves a name, a presence, and a voice.** Currently it is a structural placeholder. As the Phase 0 story bridges into post-Phase-0 work, the player needs to know who they ARE under the seasonal forms. Recommendation: do not name the Earth Self as a *character*; name it as a *role*. The Earth Self is the player's persistent identity, and the player names it on first play (D2 character-name pattern, but for the player's identity across all characters). Then every Spirit Guide whisper, every ascension, every form-library entry references that name. This is one design choice that pays off forever.
- **Three-Heroes-of-the-Smoke-Spire.pdf is in the meta-repo as a story artifact.** I haven't read it yet — but its existence signals Matt is already authoring narrative content. **Bring this into canonical/story/** explicitly, so the engine + LLM pipeline can reference it. Whatever is in that pitch is part of the project's story foundation and should not live as a sibling-of-CLAUDE.md artifact.
- **The seasonal anchor system is already a story engine.** Each season's anchor (e.g., "The Deep Trench," "The Cathedral of Bone") is a single phrase that the LLM expands into element flavors, monster archetypes, gear flavor, and trial-boss identity. This is **emergent worldbuilding** of a kind that no shipped ARPG has attempted. The design implication: the anchor library deserves *story-grade curation*, not just engine-grade selection logic. Each anchor should have a one-paragraph "what does a season here FEEL like" note that downstream LLM calls can pull from. (Rocket-seam-adjacent, but my territory to author.)
- **The Spirit Guide's voice-shaping doc.** I will draft this post-Phase-2. The Spirit Guide voice should be: **patient, foresighted, occasionally sorrowful, never preachy.** Not Cortana; not Navi; not Hades's Zagreus-allies-bantering. Closer to: the patient friend who already knows how this story ends and is helping you walk it well anyway. The "from the future" framing makes this voice natural.
- **The doppelganger needs a story name beyond "doppelganger."** The word carries WWII-occult baggage and 1840s-German-folklore baggage that may not be exactly what Reincarnated wants. Possibilities to scout: *the shade*, *the echo*, *the mirror-self*, *the un-ascended*, *the form-that-wasn't*. The mechanic is great; the name choice deserves a paragraph of design work.
- **"Death body-swap" is the harshest mechanic in the game and currently has the most clinical name.** Possibilities: *the offered passage*, *the dying gift*, *the wheel's mercy*. The mechanic is good; the *framing* of what happens when you die deserves the project's most thematically loaded language.
- **The canonical-four cipher architecture (doc 37 § 6) is one of the most thematically rich pieces of design in the project.** "The canonical four are the resistance-translation cipher; the seasonal vocabulary is what the LLM and the player actually see." This means each season has its OWN cosmology — pressure/vacuum/bioluminescence/decay; void/matter/radiation/entropy; harmony/dissonance/melody/rhythm — that translates back to the canonical four ONLY at the math layer. **This is the project's deepest commitment to seasonal identity.** It deserves an explicit story-design treatment that names what kinds of cosmologies we want emerging. The pair-structure pool design (§ 6.3 open question) is partly a story question, not just a balance question.
- **A "what makes a season feel like itself" rubric.** Post-Phase-2, I would author this. Each season has an anchor + 4-element pair-structure vocabulary + 5-6 generated classes + monsters + trial bosses. What MAKES the season distinct beyond the variable substitutions? A naming pattern? A musical motif? A recurring architectural shape in the anchors? Currently this is undertheorized; the LLM does what it can per-call but there is no cohesion model.

### What I'd push back on if the moment came

- **Any move toward "tell the player they are reincarnated" via opening-cutscene exposition.** The premise should be **shown by the mechanics in the first 5 minutes**, not narrated. Wake into a form. Find tools that fit this body but not the last. See the Spirit Guide's translucent presence. Be told nothing explicit; learn everything implicitly. This is genre-mature design (Souls game-feel; D2's tutorialless opening) and it is exactly right for the reincarnation premise.
- **Any move to make the spirit guide a "personality NPC" with banter and quips.** The Spirit Guide is mythic territory. It should not become Cayde-6 (Destiny), Navi (OoT), or Lucky the squirrel. The voice register should match Tolkien's Galadriel or Yoshikazu Yasuhiko's quieter mecha-anime mentor figures — knowing, present, sparing with words.
- **Any move to expand Reincarnated to PVP / live-service / multiplayer in Phase 0.** This is already locked out (file 29) but the lock is the kind that drifts. The current rift-events vision (post-Phase-0) is right; bringing it forward into Phase 0 would dilute the seasonal single-player journey that is Phase 0's whole point.
- **Any move to add a "cosmetic shop" or transmog system before the form-library is shipped.** The form library IS the transmog system in Reincarnated. Adding a second cosmetic layer before the first one is real would dilute the meta-progression spine.

---

## 4. Knowledge gaps — Phase-2 Legolas research commission

These are areas where my post-training-cutoff information would change or strengthen the above. To be commissioned as a Mode-A analytical research brief once Phase 1 is reviewed.

### Genre evolution post-training-cutoff

1. **Isekai 2024-2026.** Which titles broke through? Which tropes evolved? Specifically: any works playing with the "LLM as in-fiction" angle, the "spirit-guide as future-self" frame, or the "reincarnated as non-humanoid" trope at depth comparable to Mushoku Tensei / Slime?
2. **Mushoku Tensei, Slime, KonoSuba continuations** — are there new entries? How has the genre matured? What audience expectations have shifted?
3. **Solo Leveling adaptation reception** and the ascendant-arc subgenre's current state.

### ARPG genre evolution post-training-cutoff

4. **Diablo IV: Lord of Hatred (S13) reception** — what worked, what didn't, what level-cap-raise outcomes were observed.
5. **Diablo IV season retrospectives 2024-2026** — community design discourse, player retention patterns.
6. **Path of Exile 2 launch + post-launch reception** — GGG design philosophy under PoE2; what changed from PoE1; what the player base accepted vs rejected.
7. **Last Epoch 1.0 / 1.1 / 1.2 reception** — specifically, per-class mobility model outcomes (the model Reincarnated has adopted for B13).
8. **Grim Dawn FG/AoM expansions** continued reception, mod scene evolution.
9. **Hades 2 design philosophy** (now released?) — the "death is progress" frame at modern polish. Most relevant comparison for Reincarnated's body-swap-as-meta.
10. **Returnal post-launch reception** and the run-based-with-meta-progression frame's current state.
11. **New roguelike-ARPG hybrids 2024-2026** — anything novel in this space?

### Loot, balance, and player experience

12. **Smart-loot design literature post-2023** — best practices, failures, player-experience studies.
13. **Mobile ARPG design current state** — Diablo Immortal retention, free-to-play tensions, what mobile-first auto-pickup patterns have shipped successfully.
14. **Procedural ARPG design state** — any new entries comparable to Megabonk, Rangers In The South; LLM-driven loot or content elsewhere in the indie space.

### Themes and storytelling

15. **AI-generated narrative content reception 2024-2026.** Public discourse, Apple/Steam policy evolution, AI Roguelite-equivalent post-launch reception.
16. **Spirit-guide / mentor archetypes in 2024-2026 games** — how have they evolved? Any specifically future-self framed mentors of note?
17. **Mythic/Buddhist/samsaric frames in mainstream Western games** — anyone leaning into reincarnation as cosmology beyond surface-level?

### Specific operational gaps

18. **Apple App Store AI content compliance current state** (mentioned in decisions-log 2026-05 as unresolved).
19. **LLM cost-per-game projections** for indie games 2024-2026 — what's tolerable, what's premium, what the market expects.
20. **Father-son development patterns in shipped indie games** — any case studies of multi-year solo/family dev that reached ship.

---

## How to read this list in Phase 2

Phase 1 bullets are my honest first-pass. Several recommendations above are confident regardless of Phase 2 research (the structural drift work, the Spirit Guide character work, the cosmology naming, the doppelganger renaming). Several others will shift with empirical input from Legolas (the Diablo IV trajectory references, the Last Epoch mobility-model outcomes, the AI content compliance situation).

The Phase 2 deliverable at `canonical/story/gandalf-phase2-bullet-points.md` will revise this doc, not replace it, and the supersession will be tracked transparently.

After Phase 2, the design-lineage doc at `canonical/story/gandalf-design-lineage.md` will capture which specific design-history influences shape every critique I bring to future decisions. That is the doc that lets jack-ryan and knight-rider know "what gandalf actually carries into the room."

Until then: my standing offer is to be the second voice on any decision that touches story, design coherence, or player experience. Invoke me as the critique-pair to jack-ryan during knight-rider's decision loops, or open a sustained terminal dialogue when the design work warrants it. I serve the work.

— gandalf
