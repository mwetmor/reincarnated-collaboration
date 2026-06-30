# Reap. Die. Rise. — Gameplay Loop & Story Frame Design (Canonical)

**Project:** Reap. Die. Rise. (ARPG)
**Document:** Core gameplay loop, story frame, kit system, encounter design, progression, companion
**Status:** Canonical — ratified across the June 2026 design session
**Audience:** Claude design/implementation team
**Revision:** v2. This redraft **supersedes** v1's isekai framing, the "spirit guide," and the "earth realm." Those are replaced by, respectively: the death-faith frame (§2), the **retired-and-split guidance layer** — demigod tutorial + hub ensemble + death-god (§2c, §14, §15) — and the time-agnostic home realm (§3). The gameplay-loop machinery (engine, ontology, sawtooth, Goldilocks, grimoire, spawn economy, experimental kits) is carried forward intact.

---

## 0. How to read this document

This captures both **decisions** and the **reasoning** behind them. The reasoning is load-bearing: it exists so the team does not re-litigate settled questions, and so that when a decision must change, we change it knowing what it was protecting.

Tag conventions:
- **[OPEN]** — genuinely undecided; needs resolution.
- **[RATIFIED-OPEN]** — the *framing* is locked, but the specific *value* is deliberately left pending (often because it should *emerge* in design/playtest rather than be picked up front). Do not treat as decided; do not treat as formless.
- **[FRAGILE]** — a rule where small mistuning breaks the whole; handle with care.

Two external reference points anchor the design:
- **The 7th Saga (Elnard)** — the project's true nemesis ancestor *and* its cautionary tale (§9).
- **The death-faith frame** (§2) is inspired by several sources (Riddick's Necromongers, Elder Scrolls' Dark Brotherhood, the Faustian bound-servant arc seen in KPop Demon Hunters' Jinu/Gwi-Ma). **We metabolize structure; we never use their IP.** See the IP discipline note in §2.

---

## 1. Core concept & hook

**Concept:** You are a spirit bound to a dark patron. You descend into procedural dungeons, inhabiting a *kit* (a fully-realized character build). You best individuated enemy champions and — by choice — take them: **you keep what you kill**, shedding your current body to wear the conquered one. Over many descents you live many lives, and your collection of conquered spirits *is* the record of who you have become.

**The hook (concept layer):** *Conquer your rivals and keep what you kill* — an ARPG where one spirit lives many lives, conquering and becoming an endless roster of rivals. Mechanically: we take Shadow of Mordor's roster-of-conquerable-named-enemies pillar and do the thing Mordor could not — make that roster **generative and effectively endless**, because Mordor hand-authored its orcs and our engine generates ours.

**The creed:** **"You keep what you kill."** This is the spectacle/war-cry line — the conquer-and-become verb rendered as the law of the death-faith (§2). It is the *barb* under the title, not the full concept explanation. (Sharpen into our own phrasing so it carries the reincarnation meaning — you keep the *life/spirit*, not merely the loot — and clear it for verbatim use before any literal marketing use; the phrase is film-associated. Not legal advice.)

**What carries the hook in marketing:** the conquer-and-become loop *shown in motion* (a montage of besting champion after champion and becoming each — ten radically different playstyles in fifteen seconds), never a bare number, never a character-select grid. See §20.

**Precedents and what we take from each:**

- **Shadow of Mordor / Shadow of War (Nemesis System):** we take the *captain pillar* — named, individuated enemies you confront, conquer, and claim. We **deliberately do not take the memory pillar** (enemies that persistently remember and evolve against you across encounters). Two reasons: (1) it is mechanically antagonistic to our hook — memory rewards *continuity* with specific recurring enemies, while our hook rewards *turnover* and novelty; running both engines makes them cannibalize each other; (2) the memory-plus-hierarchy machinery is the part WB patented (see §1a). Our novelty is *captains-without-memory, at infinite scale.*
- **The 7th Saga (Elnard):** the structural ancestor. Seven apprentices; you pick one and the other six exist in the world as rivals you encounter, ally with, or fight; rivals scaled to your level; enemies shown on the minimap; solo duels. We are, structurally, *The 7th Saga with a generative roster.* It is also our key warning — see §9.
- **The "beat it, become it" lineage (deeper than Nemesis):** Shin Megami Tensei / Persona (defeat-and-recruit, fusion that exceeds your level), inherited from Wizardry IV; plus Suikoden, Ogre Battle, Dragon Quest V, Pokémon. Our *verb* has a 20-year-validated JRPG pedigree; what is unprecedented is fusing it with reincarnation + generative scale in a real-time ARPG. (Pitch consequence: we are not only combining lineages, we are patching the canonical Nemesis system's known flaw — it gets too easy once mastered; our Goldilocks + Souls-weight is the answer. See §9, §20.)

### 1a. Patent note (do not skip before building enemy memory)

WB's Nemesis System patent (filed ~2015–16, granted 2021, in force into the mid-2030s) covers a **specific method**: enemy NPCs in a hierarchy that individually remember past encounters with the player, change rank/appearance/behavior in response, with defeats promoting others and altering the social structure. It does **not** cover a vibe, a genre, or "named enemies you defeat and adopt." Our current design (besting → becoming, scouting, the portal, the grimoire) sits safely on the near side. The **one** place to tread deliberately is if we ever build literal cross-run enemy *memory of the player* with dynamic hierarchy reaction — that specific machinery is what is claimed. We have decided that feature does not fit the game anyway (it fights the turnover hook). If it ever returns to scope, get a real IP opinion first. (Not legal advice.)

---

## 2. The story frame — the death-faith, the patron, the creed

This section is the major addition of v2. It replaces the isekai frame. The frame was chosen because **the theology rhymes with the mechanics natively** — every tenet maps onto a system we had already built for other reasons.

### 2a. The frame

You belong to (or are bound to) a **death-faith / dark order** — a conquest-by-conversion cult whose creed is **"you keep what you kill."** This is *colder and stranger* than Diablo's aesthetic darkness: it is a *philosophical* darkness (conquest as sacrament, the claimed dead as the congregation), and it is *more internally coherent* than POE's lore because the cult's beliefs are literally the game's mechanics.

**Why this frame and not warm isekai (the commercial decision):** we deliberately dropped the isekai-audience bridge. Cross-genre bridging (selling an ARPG to isekai fans) is the single hardest marketing task; selling an ARPG to ARPG-shoppers who already want it is far lower commercial risk. We are trading **blue-ocean upside** (interactive isekai was a large, empty prize) for **red-ocean certainty** (a proven, crowded market we now have a sharp differentiator in). The reincarnation *mechanic* and the seasonal world-rotation **survive** — re-registered from "reborn traveler" to "ascending conqueror." See §17, §19, §20.

**Playability proof (the villain-protagonist worry, addressed):** Elder Scrolls' Dark Brotherhood proves a dark order can be a *beloved, playable* faction when framed as initiation into a secret, powerful, ritualistic order rather than as atrocity. KPop Demon Hunters' Jinu/Gwi-Ma arc proves the *bound-servant-of-a-dark-patron* relationship is emotionally resonant and mass-palatable. (Caveat we accepted: KPDH is kid-palatable because its protagonists *fight* the demons; playing the cult is the inverse posture — this is **teen/adult-dark**, not kid-rated. Take the Faustian structure, never the surface.)

### 2b. The creed and the theology-mechanic rhyme

The death-faith's tenets are the game's systems:

- **"You keep what you kill"** = the becoming mechanic as law: ending a champion in combat entitles you to its spirit, power, and position (§8).
- **The roster is the converted** = the ~400 kits (§4) are not a character-select screen; they are *the conquered, taken into the faith.* Every kit you play was a rival you bested and claimed.
- **The cosmograph is the patron's domain** = the night-sky-of-kits is the faith's afterlife / the patron's claimed souls. This is the organizing mythology the cosmograph needed (and a candidate resolution to the long-open framework question — see §19/§21).
- **The rank hierarchy is the descent** = lieutenants (floor bosses) beneath a Mega Boss (finale) beneath the patron — conquest is ascent through the order (§5, §6, §8).
- **Conquest-as-conversion** is the emotional content of the opening (§14): you learn to *take* a body, not to *be reborn into* one.

### 2c. Guidance and companionship (the spirit guide — retired, split three ways)

> **[RULED 2026-06-30 — Matt]** The spirit guide is **RETIRED as an entity** (not re-labeled). Its functions split three ways, and the daily-banter relationship was never one voice at your shoulder — it is **an ensemble in the hub (the Hades model).** This supersedes the earlier "a single patron-voice replaces the spirit guide" framing throughout §§14–16. The reassignment:
> - **(A) The demigod — the jailer / instructor.** Built the cage, barred from the god; selects and steers you. The **tutorial voice** (§14) and the **punctuated Mercer-mentor** at key story beats (keystone §19.1). **Not** daily banter. *Optional enhancement (a deliberate phase, never the steady state): the demigod may run warmer / chattier early — building the bond that makes the betrayal land — then recede and cool as the reveal nears; the withdrawal of the companion becomes a tragedy-beat.*
> - **(B) The death-god / patron deity (keystone §19.3).** Rare, **unreadable — a Rorschach**; seldom-heard guidance, never the daily voice. Defiance into its silence is more loaded than defiance against a god who argues back.
> - **(C) The hub ensemble — Rita and the cult's human faces.** Carries the **daily relationship and antagonistic-helpful banter** (§15) and the **defiance↔devotion personality axis** (§16), which IS the cult-standing economy (§23.5) given a voice. "Who you are to the voice" becomes "who you are to the faith, witnessed by its people."
>
> *Why split, not one chatty patron: a single quip-companion would (1) dilute the §19.1 Mercer reveal — a background-helpful betrayer detonates; a snarky companion merely turns; (2) collide tonally — warm-seductive Mercer vs. snarky-antagonistic banter cannot be the same mouth; (3) not scale the §19 double-coding — innocent-first-pass / damning-on-replay is a scalpel for a few beats, not hundreds of banter lines; (4) waste the Rorschach — defiance into an unreadable silence is the stronger dread.*

The three structural threads the old "single device" was carrying still resolve — now distributed:

1. **Companion / guidance:** the tutor-and-key-beats voice is the **demigod** (§14, §19.1); the **daily relationship** lives in the **hub ensemble** (§15, §16); rare metaphysical guidance is the **death-god**, seldom heard (§19.3).
2. **Telepathy justified:** the demigod's binding and the death-god's rare voice are native to the bound (only you hear them); the hub's faithful are diegetic people you speak with face to face.
3. **Cosmograph framework:** the cosmograph is *the patron's domain* (2b) — unchanged.

The relationship is still **"you owe it."** You are bound to the death-god by a bargain/debt; it has a stake in your conquests even as it holds you in contempt. But that debt is dramatized **not** through a chatty god at your shoulder — it is made audible through the **hub's judgment of your standing** (devotion buys you in; heresy shuns you — §23.5) and the **demigod's punctuated presence** (§19.1). The contempt-that-helps is the faith's, spoken by its people.

**[RATIFIED-OPEN] Villain-protagonist stance.** The *framing* is locked (you are bound to a dark patron by "you owe it"). The *stance* is deliberately pending and should partly **emerge** via the personality axis (§16): are you the **cult ascending** (a willing dark conqueror) or a **rebel bound to it** (chafing against the leash, closer to Jinu)? Do not freeze this. It is answered, over time, by the player's **accumulated actions** (§23.4–23.5) — hand-in vs. hoard, how you die, how you treat the faithful.

### 2d. Art direction — atmospheric-dark, not Diablo-visceral-grit

A real production constraint and its resolution. Synty's low-poly modular catalogue is clean and stylized — the near-opposite of Diablo's photoreal grime. **Do not fight the asset base for Diablo-grit; aim for the darkness the tools and the frame actually want.**

- **Grit is born in this order: lighting → texture → effects.** Blood/VFX is the garnish (the last 10%), not the meal. Clean models under flat light, plus blood, reads *worse* (incongruous), not grittier.
- **Godot helps most at the lighting/atmosphere layer** — SDFGI, volumetric fog, strong shadows, post/tonemapping, WorldEnvironment. The *same* Synty model under low-key directional lighting, deep shadow, volumetric fog, desaturated grim grading, and a dark palette reads as oppressive and moody. **Invest there first.** Then darker/dirtier *materials* on the Synty meshes (which we control). Then, last, imported-and-rebuilt impact/blood VFX.
- **VFX from Fab/Unity is rebuild work, not import work** (author into Godot's particle/shader systems; confirm CC0/licensing) — consistent with our existing harvest-and-rebuild VFX pipeline.
- **The frame lets us off the hook:** a shadowed, ritualistic cult wants **atmospheric-dark** (candlelit shrines, hooded silhouettes, sacred gloom), not Diablo-visceral-grit — and atmospheric-dark is exactly what Synty-under-Godot-lighting can deliver. The Synty↔Diablo-grit mismatch is large; the Synty↔shadowed-ritualistic-cult mismatch is small.

### 2e. IP discipline (bright line)

Build an **original** death-faith — our own names, iconography, and terms. The *concepts* (a conquest-by-conversion death-cult; a creed of claiming the fallen's power/position; an afterlife of dark stars; a bound servant carrying a patron's voice; a Faustian debt) are ancient and unownable. The specific *executions* are protected and must never be used: **never** "Necromonger," Underverse, Lord Marshal, the conversion-spikes (Riddick/Universal); **never** Gwi-Ma, Honmoon, Saja Boys, HUNTR/X, jeoseung-saja imagery (KPDH/Sony-Netflix — and this property is *this year's* phenomenon, so keep extra distance from its recognizable surface); Dark Brotherhood / Night Mother / Sithis (Bethesda). Metabolize the myth, not the movie/game.

---

## 3. The home realm & persistent identity (replaces "earth")

**Replaces the "earth realm."** The structural function is unchanged; only the fiction is re-registered, because "earth" carried a contemporary-real-world implication that fit isekai and fights the death-faith.

**One character creation, for the home-realm self only.** Spirit forms **inherit the home-realm character's facial/physical characteristics.** Reasons (all carried forward from v1, now re-anchored to a time-agnostic home realm rather than modern Earth):

1. **Thematic:** one persistent soul living many lives, not many separately-created identities (the soul persists; the body changes).
2. **Player time:** creating two forms in quick succession is annoying and dilutes both; one meaningful creation serves better.
3. **AI / cultural-appropriation avoidance (decisive):** sculpting culturally-specific faces/bodies via AI is a minefield (appropriation if done well, slop if done poorly, blandness if abstained). The player bringing their **own** home-realm face sidesteps all three. **Cultural diversity becomes *world* diversity, not *identity* diversity** — the player visits cultural worlds *as themselves* (travel-and-discovery framing, broadly acceptable; not identity-assumption framing).

**Implication:** the home-realm creator is the *only* creation moment, so it warrants real investment and breadth (face shapes, skin tones, body types, hair textures, ages). The spirit-form transformation aesthetic must flatter all face types. Each season's world must feel inhabitable by any player.

**[RATIFIED-OPEN] The home realm's cosmological role.** It now needs a *meaning*, not just a name, and that meaning is entangled with the §2c villain-protagonist stance. Options: the **unconverted last-living-realm** (your origin is the last place not yet claimed); the **fallen origin** (you are a convert from a conquered world — rhymes with "all members are converts"); a **liminal staging-ground** (where spirits stage between conquests). Decide deliberately; it co-determines whether the player is the cult's instrument, its taken, or its rebel.

---

## 4. The engine (substrate → kits)

The engine is a **deterministic procedural-generation pipeline**, not AI. Rough shape:

- A substrate axis space populates ~**68,000** points mechanically, joining into roughly **24 coordinates** (BC cells).
- Additional combinatorial mechanisms iterate toward ~**2,000 candidate kits**.
- A **battle simulation** validates candidates and returns ~**400 in-band kits**.
- "In-band" = win-rate, kills-per-minute, and DPS all within genre-canonical ranges learned from ~20 years of ARPG statistics.

The 400 are simultaneously the **hero roster**, the **enemy champion roster** (§5), and the **marketing hook** (§20).

**One pipeline, two roles (critical framing):**
- **Monsters** (trash, packs, elites, mini-bosses) are the **control variable** of the battle sim — the fixed, standardized adversary every kit is measured against.
- **Kits** are the **treatment variable** — the thing under test.

There is therefore only **one** content pipeline: a fixed monster control, against which kits are validated. Monsters are not a second bestiary; they are the measurement apparatus (and, in play, the horde — §6). Because the control is held fixed, it is the **most reusable, write-once asset** in the system, and **the control battery is exactly where validation coverage must be invested** (§18).

---

## 5. Enemy ontology (the asymmetry that protects the genre)

Two ontologically distinct enemy classes. This split is **load-bearing**, not cosmetic.

- **Monsters** — fodder. They exist to die in numbers. They carry the ARPG power fantasy: kills-per-minute, screen-clears, the loot fountain, moment-to-moment rhythm. They are **not** kits, not peers, not becomable.
- **Named champions** — **Lieutenants** (faction lieutenants = floor bosses) and the **Mega Boss** (descent finale). These **are** kits: rare, individuated, a few levels hot, **becomable.** In-fiction, these are the order's ranks — the conquerable, claimable members of the faith (§2b).

**Why the split matters:** ARPG power fantasy runs on an asymmetry of scale — one of you, hundreds of them, dying in droves. If *every* enemy were a kit (a peer), that fantasy dies. The all-kits idea quietly imported a *fighting-game* ontology (every combatant a full character) into an *ARPG* loop (most combatants are chaff); the two are incompatible at the level of feel.

**Why the split is also strictly better:** scarcity gives the becoming its weight. If everything is becomable, becoming is noise. When only named champions are kits, taking one is an **event** — you cut through a hundred monsters feeling like a god, then hit a *peer* who fights you as an equal, and besting *that* and keeping it means something *because* it stood out from the fodder. The horde is the contrast that makes the champion land. (Faithful to Mordor: anonymous fodder + named captains.)

---

## 6. The core loop (the descent)

A roguelite-shaped loop. This is the shippable MVP skeleton (descend, scale, boss, claim, repeat); the *uniqueness* comes from the engine, the conquer-and-become framing, and the per-floor faction/element rotation — not from the skeleton.

- Begin a descent as a spirit inhabiting a kit (see §14 for how the first kit is set; selection recurs between descents).
- Descend through a procedural dungeon. Level **1 → 50**; acquire gear.
- Each floor changes the **faction** and **element** of its enemies.
- Floors are populated by **monsters** (the horde — power fantasy + sim control) plus, at boss floors, **lieutenants** (named champion kits — §8, §9).
- The descent ends with a **Mega Boss** (a holdout champion — §8).

**Two timescales of power:**
- *Within* a descent: gear + levels 1–50 provide the local ramp (moment-to-moment "I'm getting stronger"; resets each descent).
- *Across* descents: choosing a higher **entry tier** faces a harder, higher-reward descent (the Torment/map-tier equivalent; long-term power fantasy lives here, bounded because we author the tiers).

---

## 7. The power curve (sawtooth discipline)

The hardest-won rule set. Difficulty is keyed to **depth and entry-tier, never to live power.**

- A floor is tuned to *expected* power at that depth/tier — specifically, **roughly your power from ~2 levels prior** (a deliberately **lagging** catch-up). Overgear it and you stomp ahead of the curve; rush it and you struggle. The player controls their *relative* power — that is where the fantasy lives.
- **Old floors never rescale.** Returning to floor 5 at level 30 and deleting it *is* the power fantasy. Make backtracking trivially dominant by design. (Note interaction with the portal and temporal summoning — §10, §13.)
- The curve is a **sawtooth, not a flat line.** Catch-up must always *lag* power gains, never lead them: hit a power spike, feel godlike for a few floors, then floors tighten assuming you have it. The spike is the reward; the tightening just resets the baseline.

**[FRAGILE] The lag is the power fantasy.** The moment floors scale to *current* power instead of trailing it, the surge vanishes and the game becomes the Oblivion failure mode — running to stand still, every fight identical, the becoming feels like nothing because the world matched you instantly. Guard the ~2-level trail like it is the core mechanic, because it is.

---

## 8. The Nemesis mechanic (beat it, become it — "you keep what you kill")

- Besting a lieutenant **offers** reincarnation (a "spirit-throw" into the defeated body — the creed enacted). It is **opt-in, always.** Declining keeps your current kit. (Forcing a swap would gut the kit identity the whole project is built on; the player who loves their bone-spear-necromancer must never be made to abandon it.)
- **The becoming reward is a +3 (≈3-levels-up) version** of the champion. Besting the thing built to beat you and then *becoming it, stronger,* is the payoff. **[FRAGILE]** A +3 reward is a real spike; the sawtooth catch-up (§7) must reabsorb it, or +3-per-champion compounds into a ratchet.
- **Mega Boss = a holdout champion from beyond the base 400.** Defeating it and completing the descent earns it as a **401st+ character.** (Relationship to the Experimental pipeline in §18 is a design area — mega bosses may *be* curated experimental kits. **[OPEN]**)

**Why becoming, not just defeating:** in The 7th Saga you beat a rival and they simply died; you never got to *become* them. Making the obstacle and the prize the *same entity* — conquest as transformation — is our innovation over our own nemesis-inspiration, and it is only possible because of the reincarnation engine. (This is also the creed, §1/§2b: you *keep* what you kill.)

**Sidegrade vs. hierarchy (resolved):** base kits are **lateral sidegrades** (in-band, distinct-not-better). Champions are those same kits pushed a few levels up by the descent's scaling. So becoming a champion feels like progress because it *is* a small, bounded, real level gain — not because the kit is intrinsically superior. The hierarchy is *situational* (this kit, right now, is a few levels hotter than you), never *intrinsic*. This keeps engine balance intact while letting "ascend by conquest" land.

---

## 9. The Goldilocks encounter system (the fix for the Elnard trap)

**The warning, stated precisely.** The 7th Saga is "one of the hardest RPGs ever" — but by *accident*, not design. Its US localization reduced the player's per-level stat gains and did **not** reduce the rivals' stats; rivals kept their stronger scaling. Result: level-matched rivals outclassed you completely, and **the gap widened as you leveled** (leveling made the duels *harder*). The midpoint apprentice duel became a wall an enormous fraction of players — including the design lead, by his own account — never passed. **The thing that made it legendary and the thing that made it abandoned were the same broken number.** The line between unforgettable-hard and abandoned-hard is a *single tuning decision*, and Elnard fell on the wrong side of it with the best intentions.

**The trap we must not rebuild:** a level-matched champion, deliberately built to exploit your weaknesses, with a **hard requirement to win and no alternative** — that is structurally the Elnard duel. Weakness-targeting + level-matching + must-win-or-stop = the wall players never beat.

**The fix: bar-as-fork, not bar-as-dead-end.** We keep the punishing duality the design lead cares about — *the same mechanism both transforms you and bars your way* — but make the bar a **fork**, not a dead end.

**The system:** each boss floor presents **3–4 lieutenants plus a portal.** Each lieutenant is a different **matchup temperature** relative to your *current* kit:

- **"Too hot"** — built against your weakness; the **bar**; can genuinely stop you.
- **"Too cold"** — a favorable matchup; a stomp.
- **"Just right"** — the meaningful, winnable-but-real fight.

You **must best one lieutenant to descend** (the gate is preserved — power injection happens on schedule, sawtooth intact). **Which** one is your choice (the bad-matchup escape — "I can't beat the kit" is solved). **Whether** you reincarnate is optional (§8).

**Key properties:**

- **Temperature is relative to the current kit.** There is no objectively hot or cold lieutenant — the champion that is "too hot" for your glass-cannon caster is "just right" for your armored bruiser. Difficulty is **emergent from matchup**, not assigned. This is richer than a difficulty slider and falls directly out of the asymmetric-kit engine.
- **[FRAGILE] The spread must be generated relative to the current kit and regenerated when the kit changes.** When you reincarnate, your weaknesses change, so the *next* floor's temperatures must be computed against the *new* kit. Static temperatures would make difficulty meaningless under kit-swapping.
- **The encounter is built upstream into the JSON** — including room dimensions and structure — constructed around the lieutenant's strengths and the player's weaknesses. This is how we get handcrafted-feeling, Souls-weighted encounters at generative scale (Souls bosses feel authored partly because the *arena* is part of the fight). **Caveat:** weakness-targeting is safe *only because* the fork lets the player route around any single instance of it. Never remove the fork.
- **Reward scales with temperature.** Besting "just right" / "too hot" yields the better become (the +3); "too soft" yields a weaker claim. This **pulls players toward meaningful fights** rather than toward trivial stomps — Goldilocks wanted the *right* bowl, not the cold one. This is also the guard against trivial-matchup farming (see §12 leak discipline): the fork must let you escape the *too-hard* without guaranteeing the *too-easy*.

**Scouting (makes the choice informed, not a coin-flip):** generic class/threat icons are visible above the fog of war on the minimap (Monster Hunter style). An archer scanning the map sees the glass-cannon-caster glyph and can route toward the favorable matchup *before committing.* **Partial reveal** is the right calibration: glyphs read *archetype/threat* (the thing that determines matchup — glass cannon, bruiser, controller), not full kit specifics, preserving some risk and discovery. Without scouting, the Goldilocks choice degrades to "pick a door and hope."

---

## 10. The portal (relief valve)

For the rare case where the whole offered lieutenant set is a bad matchup:

- The portal takes you to the **prior level.** You must **re-clear it** (re-earning the level and stats), and on passing it the game **procedurally generates a fresh boss floor with 3 new lieutenants.**
- Because rerolling **costs a re-clear** (time) and **yields a level** on the way back up, it folds into the sawtooth instead of being a free reroll. A skipped matchup does not leave you under-curve.
- **[FRAGILE] The regenerated boss floor recalibrates to your *new* level when it generates** — so repeated rerolling changes *which* lieutenants you face but never lets you outscale the gate. (Preferred over a hard reroll cap; consistent with the §7 "floors tune to power-minus-two" rule.) Without this, repeated portal use slowly overlevels the boss floor and drifts back toward grind-past-difficulty.

---

## 11. The Grimoire / Book of Spirits (capture & summon; bestiary pillar)

Replaces the placeholder term "tag" (a *tracking* metaphor — wrong for a *capture-and-release* mechanic). In-fiction, the grimoire is the **book of claimed souls** — the record of the converted (§2b), which is why it doubles as the bestiary pillar below.

**Tag the spirit, not the life.** When you best a champion you **kill the body in its own time** (claim its loot — the body yields *matter*) **and** **etch its spirit** into your grimoire (the essence — for later summoning). This dissolves the false either/or of "kill now for loot vs. mark for later access" — you do both.

**Capture method:** etch the spirit onto a page, literally with a pen — **or** via a unique item that **auto-etches on death**, capturing the spirit of *the thing that killed you* (death becomes capture; your defeat becomes the seed of a future transformation). Capture is anchored to the **moment of defeat** (reinforcing body-dies / spirit-is-taken).

**The page-flow economy (self-regulating; encodes the metaphysics as bookkeeping):**

- **Etch** = capture the spirit (a page enters the book).
- **Post a page to the portal keystone** = release/summon it forward into your next dungeon. The page is **spent**, because the spirit is no longer *in* the book — it is *out* in the dungeon, incarnating fresh **at your level** (a spirit has no fixed body, so it manifests at your power — this is *why* summoned champions are level-matched: fiction, not rubber-banding).
- **Become it** (best the summoned spirit) = gain a **new permanent page** (the spirit is now yours, recorded forever).
- **Don't become it** → **re-etch** onto a fresh page (re-capture, **has a cost**) **or lose it** (forfeit).

**Why this is the cleanest version:** depletion-and-replenishment *is* the engine. Pages move (spent on summoning, regained by becoming, optionally re-captured, or forfeited), and that flow encodes the body/spirit dualism without separate systems. The economy regulates itself: summoning is a **bet** — win the becoming and the page converts to permanent; lose and re-capture (paying again) or forfeit. The **forfeit branch is what gives it weight.**

**Reward split (no double-dip):** body-death yields **loot** (matter, in its time); besting the **summoned spirit** yields the **becoming** (identity, in your time). The two reward types split across the two acts — itself the body/spirit dualism applied to rewards.

**Two registers in one book:**
- **Volatile** captured-but-unclaimed pages (the working set; spent on summoning; at risk).
- **Permanent** became-it pages (the collection pillar — see below).
Make them **visually and functionally distinct** so the player reads "mine forever" vs. "loaded and at risk" at a glance.

### 11a. The bestiary as a core pillar

The grimoire's permanent register *is* the bestiary, and it is a **pillar**, because it does four jobs at once:

1. **Scale made visible** — the "I've inhabited 12 of ~400" ache that converts the hidden roster from invisible to *felt* (the marketing condition, §20).
2. **Collection drive** — the engine for the acquisitive player.
3. **Identity mirror** — the player who keeps becoming summoners *sees* their summoner-ness reflected.
4. **Trailer surface** — a filling book of wildly distinct forms is showable.

**It is a record of conquest, not contact** — "lives I have lived," not "monsters I have met." Every permanent page is *earned through becoming.* This is the bestiary as **autobiography**, and (in the death-faith frame) as the literal roll of the converted — far stronger than a bestiary-of-sightings.

**[OPEN / FRAGILE] Internal structure required.** With ~400 base kits plus an endless experimental frontier, a flat "100%" list is either impossible (demoralizing) or endless (meaningless). Give the book **internal shape** — archetype families, faction sets, element groups, rarity tiers — so completion is **locally meaningful** (every summoner variant; all glass-cannon casters; the season's lieutenants) and **globally open-ended.**

### 11b. Open questions on the grimoire

- **[OPEN] Cost of re-etching.** The forfeit branch ("or you just lose it") only has teeth if re-etching costs something (bounded blank-page supply, a material, time, or risk). Otherwise players always re-capture and forfeit never happens. Pin down what makes "let it go" sometimes the right call.
- **[OPEN] What "don't become it" means.** Declined-after-winning (you beat it but chose not to reincarnate) vs. killed-by-it (it beat you). These set whether summoning is a *mild page-bet* or a *run-threatening gamble* — very different stakes, and they interact with the difficulty curve differently.
- **[OPEN] Summoned spirit = same kit vs. fresh incarnation.** Same kit is predictable (you summoned what you specifically coveted). Fresh incarnation (same essence, re-rolled body) is more on-theme and feeds the variety engine. **Lean: same kit first**, for predictability of a specifically-coveted target; fresh incarnation as a possible later layer.

---

## 12. The spawn-influence economy (so identity is reachable AND discoverable)

The player who keeps choosing summoners *is* a summoner (§17) — but only if summoners reliably **appear** when wanted. Spawning cannot be pure RNG, or the system denies the player their identity. Three channels:

1. **PURSUE (deliberate):** the **keystone rune** — slot a rune to weight the next dungeon toward an archetype. *Weights, does not lock.* (High-agency, this-run, identity-expression.)
2. **BIAS (passive):** a **gear modifier roll** — `% increased chance for X archetype` affix. Competes with damage/defense (a real opportunity cost). *Shifts odds, does not guarantee.* (Folds archetype-hunting into the loot treadmill the acquisitive player already loves.)
3. **DISCOVER (wild residual):** a slice of every spawn stays **random** — the discovery channel that surprises the player into archetypes they would never have chosen. **This must be protected.**

**[FRAGILE] Both pursue tools must be *leaky*.** If the rune + gear roll together can fully guarantee the exact archetype every time, the world stops surprising you, and the player who *would have discovered* they love a bruiser never meets one. The rune weights; the gear roll shifts odds; some residual always stays wild. **The access tools make identity *reachable*; the leak makes identity *discoverable*. Both halves are required.** A bestiary filled only with what you asked for is a checklist; one filled partly with what the world surprised you with is a story about who you turned out to be.

(The keystone is therefore a single **pre-descent configuration ritual**: slot runes to bias archetype, post grimoire pages to summon specific coveted champions, then descend into the dungeon you have composed. Rune = "a *kind* I want"; page = "a *one* I want"; residual = "something I didn't know I wanted." Note: this is also a strong diegetic ritual for the death-faith — tacking claimed souls to the keystone before descent.)

---

## 13. Temporal summoning (the grimoire + keystone, integrated)

Summoning a coveted past champion is handled entirely by §11's page-flow posted to §10's keystone — there is **no separate arena.** The summoned champion appears **in your next dungeon, in your time,** at your level (fresh incarnation), fought under normal dungeon conditions (woven into real play, not a side-mode). Besting it applies the standard become loop.

The **temporal fiction** ("backtracking pulls *you* back to their level; summoning pulls *them* forward into your time") justifies the level-matching as coherent worldbuilding rather than a gamey rule, and it has survived multiple design revisions intact — a sign it is sound.

**[FRAGILE] Hold the page cap tight.** Because "tag the spirit, not the life" removed the natural cost of skipping a kill, and because posting a page is frictionless, the **page economy + cap** is the only brake on stuffing every dungeon with summoned favorites and crowding out the wild-residual discovery channel (§12). Keep the working set small.

---

## 14. The opening / tutorial (revised — demigod-voice, not spirit-guide)

**Supersedes v1's spirit-guide tutorial.** The opening is a **playable tutorial** that teaches the (dense) loop *by doing it*, and that **performs conquest-as-conversion** rather than rebirth-as-wonder. The **demigod** (§2c-A, §19.1) is the voice that teaches you — the jailer-instructor who binds you to the work.

- The demigod's voice introduces the board: you learn to *read the minimap and scout factions/lieutenants*, taught by doing (see → then act; better pedagogy than "fight badly while being lectured").
- You best a first lieutenant under guidance; the demigod teaches the **spirit-throw / the taking** (the core verb — "you keep what you kill") in the one moment where it is safe and guided.
- You perform your first **conversion**: you take the body. The opening's emotional content is *cold conquest* (you learn to seize a life), not warm rebirth. The demigod is established as the voice that will **recur at the binding's key beats** (§19.1) — *not* as a constant companion; the **daily** relationship that replaces the old guide's ever-present voice lives in the hub (§15).

**Why this is strong:** the opening establishes the premise by *performing* it (you take a life in the first ten minutes), gives the guidance layer a *character and a reason to exist* (the demigod, not a menu), and seeds the relationship layer (§15, the hub) and the binding (§19.1) without cluttering combat.

**[FRAGILE] Teach by doing; narrate almost nothing.** The opening carries the whole premise *and* the whole literacy load (minimap, scouting, faction-reading, the taking, the metaphysics, the demigod's character). If all of that is *explained*, the opening becomes a lecture and loses players. Story beats ride on top of actions; keep it quiet.

**[FRAGILE] The demigod-voice must be PULL, not PUSH** — available on request, present on notable moments, silent otherwise. The genre is littered with resented "hey, listen!" guides. (The same anti-repetition discipline governs the hub relationship layer — see §15.)

**Where kit selection went:** **not** upfront. The **first body is fixed** (the tutorial conversion), so the opening is authored and tight. The "choose your next life" **selection ritual recurs between descents** — the old galaxy/selection moment is **relocated and made repeating** rather than deleted. Hidden upfront selection is good for this game: identity becomes *emergent and demonstrated* (§17), and the loop is *more* showable than a menu (§20).

---

## 15. The hub ensemble (antagonistic-helpful banter — the relationship layer)

> **[RULED 2026-06-30 — Matt; see §2c]** The banter / relationship layer belongs to the **hub NPC ensemble** (Rita and the cult's human faces), **not** the patron. The mechanics below are unchanged; only the *owner* moves — from one voice in your head to the faith's people in the hub. This consolidates with the cult-standing economy (§23.5): the hub's warmth or coldness IS your standing made audible.

The hub's faithful — **Rita and the cult's human faces** — carry the relationship layer, and the register is **antagonistic-helpful** (the Hades-hub lineage): they *need* you (you do the holy work their faith depends on) and *resent* you (an outsider, a tool, possibly a heretic), and that tension colors every exchange. Example beat:

> Quartermaster: "I'd prefer you stayed dead the next time, and I don't know why I'm telling you this, but that last helmet is exactly what you need for the barbarian fight you're tracking."
> [Equip] / [Don't] — **either choice** triggers a player "smart retort."

**Why this is load-bearing (not mere comic relief):** the help-laced-with-contempt **is your standing with the faith made audible** (§23.5). They serve you because the work serves the god; they sneer because you are a means; you retort because you are bound but not broken. Every interaction re-expresses the relationship that makes the cold death-faith *livable and likable* without softening the darkness — a tonal *register*, not a tonal *retreat*. *(And the relationship is real enough to wound: it is what makes the loss of a hub face — keystone — land.)*

**Structure — comedy is ambient to the loop, never gates it.** The retort-regardless-of-choice means the banter rides *alongside* the decision; the player is neither rewarded nor punished for engaging with the bit, so it never slows or pressures the loop.

**[FRAGILE] Repetition is the whole risk.** Funny-the-first-time is *unbearable* the fiftieth time, and you pass through the hub thousands of times. The discipline:
- **Throttle frequency hard.** The hub's faithful mostly *stay quiet* and speak on *notable* moments (a great drop, a key fight, a death, a milestone, a shift in standing). Rarity keeps a quip a quip. Over-barking is the #1 failure.
- **Contextual over voluminous.** The helmet line works *because it knows your tracked fight.* Few sharply-contextual lines beat many generic ones. Value is in the *targeting*, not the *count*.
- **Keep every line about your standing.** Lines that re-express your standing with the faith (devotion ↔ heresy, §23.5) never become generic filler, because they are always restating the central relationship.

**[OPEN] Contextual-line tech approach (§435).** Sharp contextuality may imply an LLM-driven or heavily-templated-contextual line system. That is a **real scope/cost/latency/consistency decision**, not a free feature. Decide deliberately; do not assume.

---

## 16. Emergent personality (defiance ↔ devotion)

> **[RULED 2026-06-30 — Matt; see §2c]** The defiance↔devotion axis is driven by **actions** — hand-in vs. hoard (§23.4), how you die, how you treat the faithful — and surfaced through the **hub's reactions + cult-standing** (§23.5), **not** by verbal retorts at the equip screen. §16 and §23.5 are **the same axis**, viewed two ways: as *personality* (here) and as *economy* (§23.5).

The player's **actions** — hand-in vs. hoard (§23.4), how they die, how they treat the faithful — **accumulate on a hidden axis** (defiance ↔ devotion) that shapes the character's personality and relationship with the faith over time. This is the same axis the cult-standing economy already tracks (§23.5). It is **"identity through repeated choice" (§17) applied to personality** — the relationship is *demonstrated* across thousands of micro-choices, not picked at a menu. It is also the mechanism that resolves the §2c villain-protagonist stance *through play* rather than up front.

**Build cheap; architect for expensive; ship neither prematurely.**

- **Cheap version (LAUNCH-VIABLE — build this).** The accumulated axis **gates which lines you hear** and **shifts the hub's register** (defiant players get grudging-help + harder mockery from the faithful; devoted players get confiding + softened contempt). This is mostly a **tagging-and-selection layer on the hub banter system you already need** — the anti-repetition writing (§15) and the personality writing are *the same body of work* viewed two ways (a large, contextual, axis-tagged line pool solves both "don't repeat" and "respond to who I am"). **No additional gameplay effect** beyond the standing economy (§23.5) already in scope. Delivers ~90% of the felt magic.
- **Legibility (cheap, required).** Emergence that is never surfaced is unfelt. The cheapest legibility layer: a **hub face — or the demigod, at a key beat — occasionally remarks on your drift** ("you used to talk back more" / "you've grown agreeable, and the faith is not sure it likes it") — itself an axis-tagged line, more elegant than a meter (and consistent with our meter-avoidance elsewhere). The relationship surfaces *through the relationship itself.*
- **Expensive version (POST-LAUNCH / TEAM-EXPANSION — do not gate launch on it).** Relationship state that changes *mechanics and outcomes*, with authored content per state. The reactivity must be *authored for every combination*, so the content surface explodes combinatorially — a drowning risk for a solo launch. File alongside the experimental-kit curation (§18) under "if the first content set succeeds." **Architect** so the axis exists and is tracked from day one (cheap), so deeper reactivity is an *extension*, not a *retrofit*.

**[RATIFIED-OPEN] The protagonist's voice identity.** Defiant (rebellious bound servant — sympathetic, Jinu-adjacent) / gleeful (willing dark ascendant — true villain-protagonist) / deadpan (weary professional — Murderbot-adjacent). At thousands of repetitions, the player-character's expressed stance — the "smart retort," now *theirs*, witnessed by the hub — *is* the protagonist, more than any backstory. It should be partly **chosen by the player through the axis** (their accumulated actions) rather than frozen up front. Do not pre-decide; let it emerge (this is the §2c stance, in the player-character's own mouth).

---

## 17. Identity through repeated choice

**A player who chooses summoner every time is a summoner.** Identity-through-repeated-choice is *more* authentic than identity-through-upfront-declaration, because it is *revealed* (what you actually reach for) rather than *asserted* (what you clicked once). This is *why* hidden upfront selection (§14) works and is not a loss — and it is the same principle that powers the emergent hub-relationship (§16).

**[FRAGILE] Dependency:** this only holds if the player can **reliably reach** the archetype they keep wanting — which is exactly what §12 (rune + gear bias) and §9 (multi-lieutenant scouting choice) provide. Without that access layer, "a summoner every time" becomes an aspiration the RNG denies, and emergent identity collapses into RNG identity. The access tools are *identity-access* tools, not just matchup tools.

---

## 18. The Experimental kits & the endless frontier

**What they are:** within-band kits, **labeled EXPERIMENTAL**, sourced from **non-canonical regions of the BC-cell space** — cells the canonical selection passes over. Same output band (win-rate/KPM/DPS), **alien interior.** The fantasy is exotic; the output is identical — so they resist power creep *by construction* (a different *verb*, never more *numbers*).

**Selection strategies (in rough order of safety):**
- **Density-gap sampling** — sample sparse/empty regions of the existing 24-D space (still our space, just unexplored).
- **Anti-correlation / inversion** — sample coordinate combinations the canonical 400 keep apart (canon's implicit "these don't go together" rules).
- **Genre-prior-guided sampling** — use a non-ARPG genre as a *prior over where to look* in our own space. (Genres do **not** add cells or import mechanics — the axes are fixed; a genre is a *heuristic* for which underused region to prioritize.)
- **Latent-potential modeling** — train on (coordinates → sim outcomes) across the existing 2,000, predict high-potential *unsampled* cells. A search accelerator, not an oracle (its predictions degrade with distance from canon, like everything else).

**Design rule: one weird thing per kit.** A kit that inverts a constraint *and* imports a foreign feel *and* fuses archetypes is unreadable. The 400 are the readable baseline; an experimental kit reads as exotic precisely because *exactly one* axis departs.

### 18a. The validation gap (the real problem)

Both the **battle sim** and the **experiential-label tests** were calibrated on the *canonical region*. They **interpolate** trustworthily on canonical-adjacent cells and **extrapolate** (silently unreliably) on distant ones. A distant cell can post perfect in-band numbers against an encounter battery that does not probe what breaks it, and earn clean labels from tests that have no category for what it does. It looks validated; it is merely *unfalsified by instruments not designed to falsify it.* **Selecting exotic cells is the easy half; knowing whether the instruments can see them is the hard half, and it comes first.**

**Three fixes (build these before mass-producing experimental kits):**

1. **Distance-grading.** Compute each candidate's distance from the canonical region. Near = trust the existing sim/labels (treat like the 400). Mid = suggestive, flag for review. Far = **not trustworthy by default**, regardless of clean results. Triages thousands without manual inspection.
2. **Adversarial battery extension.** The encounter battery (= the **monster control**, §4) tests *canonical* failure modes. Extend it with encounters designed to **break weird kits** — sustained fights that expose infinite-resource loops, burst checks that expose no-defense glass cannons, mobility gauntlets, anti-synergy encounters. *"Add encounters that attack weird kits" and "make the control battery cover non-canonical failure modes" are the same sentence.* **The monsters are exactly where validation coverage gets invested.**
3. **Behavioral anomaly detection.** Shift the experiential tests from **classifiers** ("which known pattern is this?") to **outlier detectors** ("is this doing something none of the 400 do?"). Compare a candidate's full behavioral *signature* (ability-usage distributions, damage timing, positioning, resource curves), not just top-line stats, against the 400's. **In-band + behaviorally anomalous + survives the adversarial battery = the real experimental prize** (and the real hazard). In-band + behaviorally *normal* = just a 401st normal kit.

**Gate logic:** near-canonical in-band → auto-trust (normal kits). Distant + in-band + behaviorally anomalous + survives adversarial battery → **Experimental** (trustworthy). Distant + clean-on-inherited-tests-but-never-hit-by-adversarial-encounters → **explicitly unvalidated → human review → do NOT ship on the sim's say-so.**

### 18b. Fun, curation, and team expansion

- The pipeline can confirm **balanced** and **novel-in-shape.** It **cannot** measure **fun.** A kit can be perfectly in-band, genuinely anomalous, and feel like homework.
- Therefore the bottleneck is **curation, not generation.** Generation scales infinitely on its own; the **human judgment layer** that decides which validated-and-novel kits are *worth shipping* is a **headcount problem.** This is the concrete content of "team expansion if season one succeeds."
- The experimental frontier is a **retention asset (month six), not a launch feature (day one).** New players already have ~400 kits novel *to them.* **Do not gate launch on the experimental pipeline.**
- **Never ship unvalidated experimental kits** — that is the guinea-pig trap. Players do not resent novelty; they resent *unvetted* novelty. The §18a validation work is precisely what converts guinea-pig content into trustworthy discovery content. (Vetted-by-instruments ≠ vetted-for-fun; the fun filter is the human curator.)
- **Long-term augmentation path:** once the current BC space is exhausted, **add substrate axes / substrates themselves** and validate them through the same machine. Years of expansion, but always gated by §18a coverage and §18b curation.

---

## 19. Seasonal structure (background; not a launch hook)

- **Two-layer rotation.** *Outer layer:* which dimension rotates per season (race / culture / period / mechanical). *Inner layer:* the *content* of each dimension rotates (one season's races vs. another's; one culture vs. another).
- **In the death-faith frame:** a season is a **world the cult conquers** — the reincarnation/world-rotation structure survives from the isekai design, **re-registered as conquest** rather than wonder. Each season, a new world falls; its peoples become the season's factions, lieutenants, and converts.
- **Single-axis rotation per season** for legibility (to the cohesion judge and to players). One season is a unified universe containing its variety.
- **Cultural/racial dimensions are *substrate inputs* to generation**, not cosmetic wrappers — they shape what specific kits emerge.
- **Persistent mechanical archetypes across seasons** (the bone-spear-necromancer is findable across seasons with varying specifics), creating natural meta-shifts *through generation* rather than designer patching.
- **IP/naming caution:** draw *inspiration* from sources without claiming IP ("halflings" not "hobbits," etc.). See §2e for the death-faith IP bright line.
- **Cultural rotation is the seasonal-refresh story, NOT a launch hook.** It is expensive (bespoke art/world/faction per season) and a hand-authoring team could fake it, so it fails the "impossible without the engine" test that the kit-count hook passes. Conquest-across-worlds is the *frame*; the kit count is the *engine-justifying hook* (§1, §20).

**[OPEN] Cosmograph / fundamental-axis framework.** Candidate resolution from §2b: the cosmograph is *the patron's domain* (the afterlife of claimed souls), which gives the night-sky-of-kits a native mythology. Still unresolved beneath that: the **physical-vs-magical asymmetry** (physical kits organize by *delivery method* — melee/ranged; magical kits by *element*), which does **not** fit a symmetric 12-sign zodiac and points toward a **two-realm** (or otherwise asymmetric) framework; and whether the most fundamental player-facing axis is *mechanical element* or *experiential access* (design-lead lean: experiential, which persists best across seasons).

---

## 20. Marketing & positioning

### 20a. Hook stack

- A hook must clear four bars: **graspable in a sentence, world-novel, *showable* (not an unfalsifiable claim), and ideally impossible without the engine.** The kit-count hook is the only candidate that is impossible without the engine.
- **Concept hook:** an ARPG where one spirit lives many lives, conquering and becoming an endless roster of rivals.
- **Creed (the barb under the title):** **"You keep what you kill."** (Our own sharpened phrasing; carries the reincarnation meaning — you keep the *life*, not just the loot. Clear for verbatim use first; §1.)
- **Value proposition (longer pitch):** **"the ARPG with no meta"** — every hero is unique, so no guide can be written and no build can be netdecked (the deepest resonance with the audience's build-guide-fatigue pain).
- **Slop-defusing line (store copy):** "every hero feels hand-built; none of them were."
- **Show, do not state.** The trailer films the *loop* — besting champion after champion and becoming each, ten radically different playstyles in fifteen seconds — not a character-select grid. Hidden selection (§14) makes the loop *more* showable than a menu. A bare number does not hook; the consequence framed against genre expectation does ("seven classes is the genre standard; here are four hundred, all real, and no guide can be written for yours").
- **Scale must be *felt* early** (the bestiary, scouting-revealed unseen archetypes) or the hook is present-but-invisible and therefore worthless.

### 20b. The commercial-frame decision (niche over bridge)

We chose the **specialized ARPG niche** over the **isekai-to-ARPG genre bridge** (§2a). The reason that carries the decision is *not* "darker/more-coherent" (those are post-purchase virtues that don't acquire anyone) — it is that **we now speak the native language of an audience that already exists and is already shopping for exactly this.** Diablo/POE players parse "dark conquest fantasy, kill-and-take-their-power, build depth, hard boss encounters, loot" instantly; the isekai frame *obscured* those same mechanics behind a signal that audience doesn't scan for. The Necroism/Dark-Brotherhood frame **translated our ARPG into ARPG's dialect.** The cost, named honestly: we traded **blue-ocean upside** (interactive isekai, a big empty prize) for **red-ocean certainty** (a proven, crowded market — Diablo, POE, Last Epoch, Grim Dawn — where we now have a sharp differentiator). For a first commercial title where survival matters more than ceiling, differentiated-sure beats uncertain-big.

### 20c. Worth-examining: payoff is strong, legibility is the risk

Whether the combination deserves attention splits into two **independent** bars:

- **Payoff differentiation — strong.** The parts *interlock* rather than co-exist: each best idea *solved a problem another part created* (the grimoire economy solved tag-permanence; Goldilocks solved the difficulty-wall the level-matched-nemesis created; emergent personality solved "who is my character" *and* banter-repetition; roster-as-converted made the kit-count theologically meaningful). That interlock produces a distinct *feel*, so examination is *rewarded* — the differences compound rather than pile up.
- **Legibility — the real risk.** The same richness that makes it unique makes it hard to parse: 8+ distinctive parts is *anti-legible*. Most of the differentiation is also **invisible or unfalsifiable up front** (emergent personality is invisible until hour ten; "every build is unique" is a claim players have been burned by; the grimoire economy doesn't screenshot). So the burden falls on **(1) compression to one or two showable promises** (conquer-and-become / no-meta) with the interlocking depth **discovered in play**, and **(2) the one thing that can actually be shown** — the conquer-and-become loop in motion, ten distinct kits, the creed enacted on screen.
- **Net:** worthy in payoff, fragile in legibility. Compression + demonstration is the *solvable* problem (and the good news — an inert combination is *not* solvable, and ours is not inert). The originality is in the **assembly**, not the parts (all borrowed, all recognizable); research repeatedly failed to find the *combination* even as it easily found every *component*.

### 20d. The load-bearing implementation condition

**The 400 must *play* visibly differently.** This requires **parametric/compositional abilities** — a bounded library of ability primitives parameterized by element/shape/timing/scaling, with kits expressed as configurations — so 400 kits cost the primitive library + configuration, **not** 400 hand-built implementations. Without this, the infinite-kit hook is infinite manual effort. With it, the engine's data-layer infinitude survives into playable Godot content. (Same architectural move as the StyleProfile restyle layer and composable VFX slots, pointed at abilities — abilities must produce distinct *verbs*, not just distinct stats.) **This is the condition the entire hook cashes against.**

---

## 21. Consolidated open questions (the live agenda)

**Story-frame opens (new in v2):**
- **[RATIFIED-OPEN]** Villain-protagonist **stance** — cult ascending vs. rebel bound to it. Framing locked (bound by "you owe it"); stance emerges via §16. (§2c)
- **[RATIFIED-OPEN]** Protagonist-**voice** identity — defiant / gleeful / deadpan; emerges via the action-driven personality axis (§23.5), not picked up front. (§16)
- **[RATIFIED-OPEN]** Home-realm **cosmological role** — unconverted last-realm / fallen origin / liminal staging; co-determines the stance above. (§3)
- **[OPEN]** Hub-banter **tech approach** — LLM-driven vs. heavily-templated-contextual; a real scope/cost/latency decision. (§15)
- **[OPEN]** Emergent-personality **scope** — build the cheap (line-gating, no gameplay effect) version for launch; architect for the expensive (mechanics-changing) version; do not gate launch on the latter. (§16)

**Carried-forward opens:**
- **[OPEN]** Mega Boss **401st-reward** ↔ Experimental pipeline — are mega bosses *curated experimental kits*? (§8, §18)
- **[OPEN]** Grimoire **re-etching cost** — must make "lose it" a live choice. (§11b)
- **[OPEN]** Grimoire **"don't become it"** definition — declined-after-winning vs. killed-by-it. (§11b)
- **[OPEN]** Grimoire **summoned spirit** — same kit vs. fresh incarnation (lean: same kit first). (§11b)
- **[OPEN]** Bestiary **internal taxonomy** (families/sets/tiers). (§11a)
- **[OPEN]** **Fundamental-axis / cosmograph framework** — patron's-domain as candidate; physical/magical asymmetry vs. zodiac vs. two-realm; mechanical-element vs. experiential-access. (§2b, §19)
- **[OPEN]** Tuning the **boss-spacing ↔ +3-reward ↔ catch-up** inequality (levels-per-champion ≤ levels-caught-up-between-champions, or the sawtooth tilts into a climb). Battle sim should stress-test. (§7, §8)
- **[OPEN]** **Scouting reveal-depth** calibration (archetype-only vs. more). (§9)
- **[OPEN]** Marketing **legibility compression** — the one/two showable promises and the showable spectacle beat that carry an anti-legible 8-part combination. (§20c)

---

## 22. Cross-references & superseded design

**Superseded by v2 (do not treat as canonical anymore):**
- **Isekai frame → death-faith frame (§2).** Dropped for the niche-over-bridge commercial reason (§20b). The reincarnation *mechanic* and world-rotation *survive*, re-registered as conquest (§8, §19).
- **Spirit guide → RETIRED, split three ways (§2c).** The guidance/companion role does **not** collapse into one patron-voice; it splits: **demigod** (tutorial + key beats, §14, §19.1) + **hub ensemble** (daily relationship + antagonistic-helpful banter, §15, §16) + **death-god** (rare, unreadable guidance, §19.3). *(Ruled 2026-06-30; supersedes the earlier "spirit guide → patron deity" framing.)*
- **Earth realm → time-agnostic home realm (§3).** Same structural function (one creation, face propagation, cultural-diversity-as-world); contemporary-Earth baggage shed.

**Still standing from prior design:**
- **Character creation:** the diegetic "selection" moment is **relocated** to the recurring between-descent "choose your next life" ritual; the opening is the demigod-voice tutorial (§14). Single home-realm creation (§3) stands.
- **Engine identity:** **deterministic procedural generation, not AI** — Dwarf Fortress / Caves of Qud / No Man's Sky lineage, not the generative-AI lineage. AI touchpoints are dev-workflow (this agent team) and possibly some asset generation, not the engine.
- **Genre positioning:** **ARPG, honestly** — the engine surfaces structure the genre usually hides behind symmetric class menus. Not genre-departing; doing ARPG more thoroughly. Audience may extend toward the broader "ambitious RPG with depth" market.
- **Audience model:** design for the **silent majority's motivations** (power, loot, efficiency, standing, accomplishment, engagement — "a leg up") rather than the articulate-minority signal; validate via research (community-signal analysis, reviews, surveys) with the agent team's help.

---

*End of canonical design (v2). The §21 agenda is live. The story frame (§2), hub ensemble (§15), and emergent personality (§16) are the major v2 additions; the loop machinery (§4–§13, §18) is carried forward intact.*

---

## 23. The Run Model — descent shape, the harvest, and the conduit economy (Canonical)

*Consolidates an extended design session. This is the operative run structure; it extends and sharpens §6 (the core loop) and §10 (the portal). Where this conflicts with earlier sketches of run length/shape, this wins.*

### 23.1 Run length & the three-beat descent
- **A run = the descent through (and escape from) one realm.** Target a **~25-minute victory run** (20 floor / 30 soft ceiling). Rationale: cross-genre consensus puts the roguelite sweet spot at 20–30 min; runs reliably feel like a chore past ~30–45 min. The escape beat (below) pushes a clean run to ~25–27 min — slightly long, but the added time is high-tension flight, not more descent, so it doesn't drag.
- **Spatial shape = three beats with a deliberate register shift between them:**
  1. **Structure 1 (architectural interior):** tight ARPG-canon rooms, dense, fast — the "blow through it" stage. Teaches the loop in confined space. ~7–8 min. Holds the **lesser conduit** (required).
  2. **Biome crossing (open field):** larger rooms, WFC-generated terrain, ranged/environmental threats, breathing room. The contrast beat that fights monotony. ~6–7 min.
  3. **Structure 2 (architectural, climactic — the "treasure room" structure):** tight rooms escalating to the **champion** boss; the realm's defenders converge here. ~7–9 min. Holds the realm's **primary conduit** (the #1 treasure).
  Then **The Escape** (~5–7 min) — see 23.3.
- **Room-size grammar = the pacing signal.** Tight rooms in architectural stages (density, kinetic possession exchanges, cheap prefab-tile procgen); larger rooms in biome stages (tactical space, visual relief). Keep biome rooms **few-but-big**, never many-and-big (that's the slog). The geometry teaches the rhythm: tight-fast → open-tactical → tight-climactic → flight.
- **Procgen mapping (reuses the settled strategy):** graph-grammar lays out the macro beat-sequence (Structure→Biome→Structure→Escape); prefab meta-tiles build the architectural structures; WFC builds the biome field. Sequence fixed (legible, lore-true); content procedural (fresh each run).

### 23.2 The harvest — what the necromancers take
- **The objective of a run is to harvest the realm's souls**, bound into **conduits** — engine-generated, realm-thematic artifacts (the StyleProfile / seasonal-coherence engine already produces exactly this kind of coherent per-realm artifact). Form-language: a **consistent category, variable style** (e.g., always "the realm's soul-vessel," but each realm's is visually/thematically unique) — a recognizable objective with infinite thematic variation. Must read as **authored-quality** ("the sacred heart of *this* place"), never as generic loot.
- **Two conduits per realm, asymmetric:** Structure 1 yields a **lesser conduit** (a lieutenant's vessel); Structure 2 yields the realm's **primary conduit** (its core/heart, the #1 treasure, taken from the champion). Both are required.
- **The treasure room (Structure 2):** the **primary conduit is the guaranteed #1 treasure** (the required harvest — you always get it; winning is never in doubt). **Bonus treasures scale with performance** — faster clear / more efficient escape / **more possessions** → more bonus loot. This makes the escape a *risk/reward optimization* and rewards the core verb (possession). Framing discipline: the conduit is always secured first; bonuses are clearly *upside*, never a "missed obligation" — a player who won must never feel they failed by leaving loot.

### 23.3 The manufactured rebellion & the escape (the §14 spine, performed)
- **Combining the two conduits triggers the realm's eruption.** Taking either conduit alone is stable theft (the cult frames it as *liberating souls into merciful death*). But **combining them destabilizes the bound souls into a volatile mass — and the realm's inhabitants erupt into deadly aggression.** *This eruption IS the manufactured rebellion (§14): the player, every run, performs the manufactured uprising with their own hands.*
- **This resolves the asymmetry problem:** you flee only after the *second* conduit because **the combination** (only possible with both) is what erupts the realm — not "the realm reacts to theft" (which would be symmetric and would expose the harvest immediately).
- **CRITICAL framing discipline (Rorschach / peace-illusion):** every beat must be *misreadable as holy* on the surface and *damning* once the truth is known.
  - **Surface (what the cult sincerely believes):** "The moment we gathered the souls, the realm erupted in violence — proof they were never truly at peace, that they needed our mercy. We carry their souls to the god's merciful rest." The eruption *retroactively justifies* the crusade — the perfect self-deceiving lie. **They do not know they caused it.**
  - **Buried truth (§14):** *combining the conduits is what caused the eruption.* The realm was at peace until the harvest. You didn't find a violent realm — you *made* one, to justify taking what you came for.
  - The god consuming the combined soul-mass is **the harvest feeding**, NOT a defusing/saving act. (Do NOT frame extraction as "preventing a catastrophe" — that would make the crusade mechanically heroic and undercut the reveal. The volatility is the *manufactured rebellion*; the god eating it is the *harvest completing*.)
- **The Escape = the reincarnation showcase + the power-fantasy payoff.** Reaping the Structure-2 champion = **reincarnating into the champion's body**. The realm then erupts; you **flee as the champion**, wielding the power you just claimed — *the champion's strength is why you survive the eruption.* The escape path is full of fodder to **plow through** (you're now a juggernaut relative to the soldier-mass — the contrast of "I was struggling; now I'm unstoppable in a stolen god-body" is the run's crescendo). The escape clock must be **generous-but-urgent**: a competent player escapes with a thrilling margin; only a fumbling one fails. Winning the champion fight should *feel like you've won* — the escape is the exclamation point, never a second boss-wall.
- **The champion body is a per-run finale you don't keep** (the *conduits* are what you bank; the body was the vessel). Every run ends on the high of brief unstoppability, then you start humble again — preserving loop tension. *(Optional future: rare champions bankable as unlockable bodies/classes — deferred.)*
- **The accruing moral weight:** every successful run ends with you *fleeing a world you just killed, pockets full of its souls.* Over many runs this accumulates into the dawning §14 horror and feeds the ending. The escapes ARE the player's repeated, embodied complicity.

### 23.4 The conduit as a moral decision-object — hand in OR keep
- **Each run, the harvested conduit poses a choice that is a micro-version of the macro ending (instrument / betrayer / third path):**
  - **Hand it to the god** → progress the sanctioned path (story, meta-progression, feeding the harvest). Piety. Advancement. You give up the conduit.
  - **Keep it** → an act of **defiance**: withhold a soul from the god.
- **The player rehearses the endgame choice dozens of times before reaching it** — so the ending is the *culmination* of a choice long felt, not a sudden fork. **Keeping accumulates toward the betrayer/third-path ending** (the game tracks defiance); the macro-choice is *earned* by the micro-choices.

### 23.5 LAUNCH SCOPE: the conduit is NARRATIVE-ONLY at launch
- **At solo launch the conduit has NO combat value** — keeping it makes you neither stronger nor weaker in fights. The dilemma is **purely moral**: piety-and-progress vs. defiance-and-cost. (This is *truer to the game's soul* than a power-item — the game is about the moral choice.)
- **The cost of keeping = an escalating cult-standing tax ("an unclean air about you").** The longer you hoard, the worse your standing: **rising prices → items off the shelf → vendors refusing to deal with you.** A **heretic / shadow vendor** opens as the pious shun you — so deep defiance **shifts** your economy (pious shun you; heretical embrace you) rather than **stranding** you. This is self-balancing (the squeeze pushes you back toward a hand-in to wash clean) and foreshadows the factional split of the endgame.
  - **Guardrails:** the penalty must be **painful but recoverable** (hand in a conduit → standing recovers → vendors return) and **clearly telegraphed** (vendors comment on your unclean air; the standing meter is visible; cause-and-effect legible) so it reads as a *choice*, not a bug. Never hard-soft-lock a player who over-hoards.
  - **Moral valence (Rorschach):** early on, keeping reads as **heresy/sin** — failing the holy work, denying a soul its merciful rest; the cult is *right* to shun you. Only after the §14 reveal does it reframe as possibly the *first righteous act*. Keep valence inverted/ambiguous until the reveal.

### 23.6 POST-LAUNCH: PvP / CTF as a reuse layer (Option B activation) — NOT a launch dependency
- **De-risking decision (load-bearing):** the solo game must be **100% complete and satisfying without PvP.** PvP is network-heavy, population-dependent (an 8v8 mode is dead without players), and the kind of system that slips/cuts. **Never let the launch depend on it.** Launching PvE-first *builds the playerbase* that later makes PvP viable (PvP should follow the population, not precede it). PvP reuses systems already built and balanced for solo (possession, the commander-domination loop, the conduit) — so it is *additive*, cheap-by-reuse, and deferrable.
- **The PvP mode = bounded Capture-the-Flag**, ~8v8, faction vs faction (rotating constantly via reincarnation). **NPC "giants" are the victory engine:** heroes gang up on the enemy giant-commander, weaken him, and one player **possesses** him to become the ultimate **flag-runner**.
- **Giants are PvP-ONLY by deliberate design.** They do NOT appear in solo PvE. Rationale: a giant in solo would make players (a) expect to reincarnate into it inside a bounded temple — opening lore/balance questions we don't want — or (b) wonder why they *can't*, an unexplained exception that makes the world feel arbitrary. The giant only exists in CTF, where its special possession-rules are the *explicit, bounded objective* and therefore make sense. *(Note: "commanders" in solo PvE are AI-driven **player kits set antagonistically** — not bespoke giant-bosses.)*
- **Conduit's PvP-era role (the dormant combat dimension activates):** the *same* conduit becomes the **flag-capture specialist weapon** — **PvE-normal but exceptional against giants/commanders.** This profile is a *balance feature*, not just flavor: it grants *objective* power (dominating the NPC giant = the victory engine) WITHOUT granting *player-vs-player* dominance (it's normal against enemy player-combatants — the soul-mass), so it can't be used to grief/snowball straight fights. The profile encodes the two-axis hierarchy: exceptional vs. the reincarnating commander-caste (giants), normal vs. the soldier-mass. CTF role split: conduit-hoarders (heretics) are the **capturers**; the pious (who handed in) are the **enablers** — the solo moral choice shapes the multiplayer role.
- **Deferred PvP-balance questions (decide with real player data when PvP is built):** (a) is the conduit a **permanent hoarded weapon** (permanent escalating tax) or a **per-match consumable** (per-use cost — gentler on competitive players, decouples PvP-power from permanent standing)? (b) can the giant be possessed **without** a conduit (conduit = *edge*, keeps CTF fair for conduit-less teams) or **only with** one (conduit = *gate*)? Lean: consumable-ish, edge-not-gate.

### 23.7 Open questions on the run model
- Exact bonus-treasure scaling curve (how much do speed/possessions yield?) — tune in playtest.
- Whether the conduit gets a *small* solo combat relevance vs. the Structure-2 champions (a light "Option 1" touch reusing existing content) — currently **declined** in favor of narrative-only at launch; revisit only if the moral dilemma proves too thin without a power hook in playtest.
- Does keeping a conduit confer any *non-combat* solo utility (e.g., forbidden knowledge / the conduit "whispers" truths the god withholds — feeding the investigation/inner-core path)? Potentially rich, deferred.
- Per-realm conduit *modifier* variety when fed to the god (different conduits → different meta rewards) — flavor-only vs. systems feature; deferred.
