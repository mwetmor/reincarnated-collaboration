# Demo Audio Content R&D — Sound Effects + Music Generation/Curation

**Captured:** 2026-05-10
**Library:** Pixi.js for visual; **@pixi/sound** or **Howler.js** for audio (per Pixi.js ecosystem conventions)
**Scope:** companion document to file 24 (the demo1 implementation prompt) and parallel to file 25 (visual content R&D). Describes the iterative approach for generating or curating audio content for the Pixi.js demo.

## Why this is its own document

Audio is its own pipeline with its own cost/complexity tiers, similar to but distinct from visual content. A demo without audio feels like a tech demo; with even basic SFX it feels like a game. Audio R&D runs as an iterative ongoing concern across all phases, not as a single phase.

The structure here parallels file 25 (visual content R&D). Same tiered approach, same iterative workflow, same family-collaborator role.

## Audio categories in scope for demo1

Five distinct audio tracks, each with different generation/curation pathways:

| Category | Purpose | Volume |
|---|---|---|
| **Ability SFX** | Match the LLM-named ability's flavor; align timing/duration to the geometry's animation | ~30-50 sounds (one per geometry × element combination, with reuse) |
| **Hit/damage SFX** | Combatant takes damage; archetype-flavored where possible | ~10-15 sounds |
| **Death SFX** | Combatant defeated; tier-graded (trash death vs boss death) | ~5-8 sounds |
| **Drop SFX** | Rare+ gear drops on boss defeat; tiered by gear tier | 3 sounds (rare/epic/legendary chimes) |
| **Potion use SFX** | "Glug" sound on health/mana potion consumption | 1-2 sounds (could differentiate health glug vs mana glug, or single shared sound) |
| **Music** | Single general game soundtrack (1 track) | 1 ambient track for the whole demo (not per-season) |

For demo1, that's ~15-20 unique audio assets minimum (SFX library + 1 music track). Curation is the bottleneck, not playback. Per-season themed music was considered and **deprioritized 2026-05-10** — single general track keeps audio scope contained; per-season music can land in demo2 or as polish later. Reasoning: music scope can balloon (per-season tracks would add 5-10 unique tracks); demo1's value is primarily SFX feedback during combat, not musical season-identity.

## Available metadata to drive audio selection

The engine's JSON exports provide structured metadata that audio mapping consumes:

### Ability
- **`name`**: LLM-generated, evocative ("Chalk Dust Gale", "Inferno Brand")
- **`geometry`**: ranged_physical / fire_blast / frost_nova / melee_strike / etc. (drives the *type* of sound — projectile vs explosion vs swing vs beam)
- **`element`**: fire / water / wind / earth / physical (drives the *tonal character* — fire = crackle/whoosh, water = splash, wind = airy, earth = thud/rumble, physical = impact)
- **`cooldown_seconds`**, **`damage_magnitude`**: indirectly informs intensity (high-damage burst = more impactful sound)

### Combatant (player + monster)
- **`archetype_label`**: warrior / mage / hunter / etc. (drives hit-grunt voice flavor — heavier vs lighter; could differentiate male/female/monster vocals if pack supports it)
- **`damage_type`**: same options as ability element (drives damage-taken sound flavor)
- **`tier`** (monsters only): trash / standard / elite / boss (drives death sound dramatic weight — trash dies with simple thud, boss dies with reverb-heavy roar)

### Gear (drops)
- **`tier`**: rare / epic / legendary (drives chime flavor — subtle ting → bright bell → dramatic stinger)
- **`color_signature`** (legendary): could inform color-themed audio synthesis if Tier 3 AI generation is used

### Season
- **`anchor`**: the season's environmental theme ("The Schoolhouse Standing Alone", "Trench-Caller Abyss") — drives ambient music tonal direction
- **`dominant_element`** or theme: fire-themed seasons get warmer instrumentation, water-themed cooler, etc.
- **`elements`**: the 4 seasonal element flavors (e.g., char/draft/dew/chalk) — could inform secondary instrumentation

## Tiered approach — start cheap, iterate upward

Same shape as file 25's visual tiers.

### Tier 1 — Procedural synthesis (placeholder + ability VFX)

**Approach:** generate audio entirely in Web Audio API code from metadata. No external assets.

**For ability SFX:**
- Geometry drives waveform: projectile = oscillator sweep (rising pitch), AOE = noise burst with low-frequency thud, melee swing = brief noise + impact, beam = sustained drone
- Element drives timbre filter: fire = mid-range distortion, water = low-pass watery filter, wind = high-pass with breath noise, earth = low rumble, physical = clean attack
- Duration matches the ability's animation duration
- Volume scales with `damage_magnitude`

**For hit/death SFX:**
- Hit = brief noise burst with element filter
- Death = longer impact + decay; boss death gets reverb + sub-bass

**For drop SFX:**
- Rare = simple sine ping (300-500Hz, 200ms)
- Epic = chord (multiple sine waves, 500ms)
- Legendary = arpeggiated chord + reverb (1-2sec)

**Pros:** zero external dependencies; deterministic; fully under our control; ships with demo1 with no asset wrangling
**Cons:** sounds synthetic / lo-fi; might feel like 80s arcade rather than modern ARPG
**Best for:** placeholder; first-iteration audio; ability VFX where stylized synth matches "magic spell" feel anyway; rare+ drop chimes (chimes naturally suit synthesis)

**Tractability for Claude CLI:** HIGH. Web Audio API code is well-documented; deterministic outputs; iteration is fast. The agent writes the synthesis code; the user listens and adjusts.

### Tier 2 — Curated free/open-source SFX libraries

**Approach:** use existing free/CC0/permissively-licensed SFX from established libraries; map by metadata.

**Source libraries to evaluate:**
- **Freesound.org** — community-uploaded SFX; mixed licenses (filter to CC0); enormous variety; requires curation
- **OpenGameArt.org (audio)** — game-focused SFX packs; many CC0; includes RPG/fantasy effects
- **Kenney.nl audio packs** — high-quality CC0 game-asset audio (UI sounds, impact sounds, minimal ambient)
- **itch.io free audio packs** — varied; many ARPG-themed packs at low/no cost
- **Pixabay (audio)** — royalty-free; broad coverage

**For ability SFX:** download a pack with fantasy/magic SFX (lots of options for fireballs, lightning, ice, melee swings). Map by geometry × element to specific files. ~30-50 files for full coverage.

**For hit/damage SFX:** generic impact/grunt packs. ~10-15 files.

**For death SFX:** combine impact + groan/roar. ~5-8 files.

**For drop SFX:** chime/bell/crystal packs. 3 files for tiers.

**Pros:** much higher quality than Tier 1; cohesive game audio aesthetic; battle-tested SFX
**Cons:** licensing/credit considerations (CC0 ideal; some packs require attribution); style consistency requires curation; large up-front download volume
**Best for:** all SFX categories in demo1 — likely the right baseline

**Tractability for Claude CLI:** MEDIUM. Claude downloads sample packs, inventories them, writes a JSON mapping `(geometry, element) → filename`. Iteration spot-checks whether mappings produce sensible sounds.

### Tier 3 — AI-generated audio (signature moments + music)

**Approach:** call AI audio generation APIs with structured prompts.

**Service options:**
- **Stable Audio (Stability AI)** — text-to-audio for SFX and short music; reasonable cost
- **ElevenLabs SFX** — high-quality SFX from text prompts; slightly more expensive
- **Suno / Udio** — text-to-music (full tracks); $0-10 per generation depending on tier
- **AudioCraft (Meta, open-source)** — self-hosted music/sfx generation; free if you have GPU access

**For music (high value):**
- Per-season prompt: "ambient ARPG fantasy music, [season anchor], [dominant element]-themed, looping, 2-3 minutes" — Suno/Udio generates a track in ~30 sec; cache as MP3
- Cost: ~$0.10-1.00 per track depending on service tier; ~$1-10 for 10 seasons total
- Result: each season has a unique themed music identity

**For signature SFX (moderate value):**
- Legendary drop chime: "magical legendary item drop chime, ARPG, bright + reverb + [color_signature]-flavored"
- Boss-specific death sounds: prompts derived from boss class name + element

**For ability SFX (lower value):**
- Probably skip Tier 3 for abilities — Tier 2 curated is good enough; the volume is too high to AI-generate cost-effectively

**Pros:** highest uniqueness; per-season music identity; signature drops feel distinct
**Cons:** API cost (~$1-10 setup); quality variance; generation latency (background process)
**Best for:** music (clearly worth it for season identity); legendary drop chime (single signature moment)

**Tractability for Claude CLI:** MEDIUM. Claude writes the API integration + caching pipeline. Quality evaluation needs human-in-the-loop (you/your son spot-check generated tracks; reject obvious failures and re-generate).

### Tier 4 — Composed / commissioned (post-MVP)

**Approach:** human composer or sound designer creates final audio.

**Scope:** post-demo1 enhancement. Could include:
- Family member who plays an instrument creating a few signature themes
- Commissioned freelance composer on Fiverr/etc. for season themes
- Audio designer pass on SFX for cohesion

**Best for:** the eventual game ship; demo1 doesn't need this.

## Iterative workflow for the demo CLI agent

The demo CLI agent should approach audio as **continuous R&D** alongside the six phases of file 24, structured so audio is always **progressive enhancement, never blocking playability**.

**Core principle:** the audio system is initialized in Phase 1/2 with non-blocking fallbacks. If an SFX isn't loaded, the gameplay event still resolves correctly (silently). If music isn't ready, the game still runs. Audio is metadata-driven; assets can be added/swapped without code changes. **The browser must always be runnable, regardless of audio asset state.**

1. **Phase 1 (setup):** No audio assets needed. Stub audio system in place (Pixi.sound or Howler.js loaded; play() calls succeed silently if no asset is attached). Architectural foundation only.
2. **Phase 2 (one ability end-to-end):** Tier 1 procedural SFX for the one chosen ability — even just a Web Audio synthesized beep proves the pipeline. Hit/death SFX can be silent at this milestone. The browser playable state doesn't depend on audio; if SFX file is missing, gameplay event still fires.
3. **Phase 3 (all abilities + statuses):** Begin Tier 2 evaluation — download a curated SFX pack (e.g., Kenney's audio + a Freesound CC0 ability pack) and write a `(geometry, element) → file` mapping function. Replace Tier 1 procedural ability sounds with Tier 2 curated. **If Tier 2 work is delayed, Tier 1 procedural is sufficient for Phase 3 milestone; no blocking.**
4. **Phase 4 (gauntlet):** Add hit/damage/death SFX from Tier 2. Different tier for different combatant types (trash death = simple, boss death = bigger). **Phase 4 milestone is the first family-playtest-worthy state — audio enhances but doesn't gate it.**
5. **Phase 5 (gear drops + inventory):** Add drop SFX (3 tiered chimes — rare/epic/legendary). Tier 1 procedural is fine; Tier 3 AI-gen for legendary chime is optional polish. **Phase 5 milestone = full demo1 loop functional, with or without these SFX.**
6. **Phase 6 (polish):** Single general soundtrack — the **last** item to land. AI-generate via Suno/Udio (one track for the whole demo, not per-season). **Music is explicitly non-blocking — if the track isn't ready when demo1 ships, demo1 ships without it.** The Phase 6 polish pass also evaluates audio mix and family playtest feedback.

**Non-blocking architecture requirements:**

- Sound playback is wrapped in try/catch — failed SFX loads or missing assets log a warning but don't crash the game loop
- Music is a single track loaded asynchronously at game start — if it fails to load, the game runs silently
- Audio asset paths are read from a manifest (e.g., `audio_manifest.json`); the manifest can be partial (incomplete coverage), and the game uses what's available
- During development, the demo agent can add SFX entries one-at-a-time without breaking earlier milestones

## Family collaborator role in audio

Like visuals, audio evaluation is human-in-the-loop. Your son's role specifically:

- **Phase 4:** does the boss death sound impactful? Does the wave-1-trash death feel cheap (good) vs. underwhelming (bad)?
- **Phase 5:** does the legendary drop chime feel like "I got a legendary!"? Or does it blend with the rare/epic chimes?
- **Phase 6:** does each season's music feel distinct? Does the audio overall enhance or distract from the encounter?

Engage him as the audio judge. The CLI agent integrates the audio; family validates whether it lands emotionally.

## Acceptance criteria for audio at demo1 ship

By end of demo1, the audio layer should:

1. **Every ability has audible feedback** synced to its visual animation. Player can close their eyes briefly and tell what type of ability fired (projectile vs AOE vs melee).
2. **Hits and deaths produce satisfying audio.** Damage feels weighty (not "click"); boss death feels like an event.
3. **Rare+ drops produce a distinct chime.** Player hears the chime and knows something good dropped before looking.
4. **Each season has its own music identity.** Loading a different season produces a different sonic palette.
5. **The volume mix isn't overwhelming.** SFX don't drown out music; music doesn't drown out SFX. Player can keep audio on without fatigue.

These don't all require Tier 3. Tier 1 + Tier 2 mix can satisfy 1-3; Tier 3 is what makes 4 land cleanly. Item 5 is universal mixing discipline.

## Architecture notes for the demo agent

**Audio library choice:** **@pixi/sound** is the natural fit (built for Pixi.js ecosystem; handles common needs). **Howler.js** is the alternative (more mature, more features; works fine alongside Pixi.js). Both fine; pick based on agent preference.

**Asset organization:**
```
assets/
  audio/
    sfx/
      abilities/         # ability SFX organized by geometry, sub-organized by element
        ranged_physical/
          fire.mp3
          water.mp3
          ...
        fire_blast/
          ...
      hit/               # hit/damage SFX organized by archetype/damage type
      death/             # death SFX organized by tier
      drop/
        rare.mp3
        epic.mp3
        legendary.mp3
    music/
      season_001001_ambient.mp3
      season_001001_encounter.mp3
      ...
```

**Loading strategy:** preload SFX library at season-load time; lazy-load music tracks (only load the season the player chose). Audio assets are typically <500KB each at game-quality MP3; total demo1 audio asset size ~10-30MB across all 10 seasons.

**Performance:** @pixi/sound and Howler both pool audio contexts; concurrent ability playback is fine. Demo1's combat is sparse enough that audio performance is not a concern.

## What's NOT in scope for audio R&D

- **Spatial audio / 3D positioning** (overkill for stationary 2D top-down demo)
- **Voice acting** (no character dialogue in demo1)
- **Adaptive music systems** (music intensity based on combat state — post-demo polish)
- **Custom audio synthesis libraries beyond Web Audio API** (no DSP development)
- **Audio engine of our own design** (use @pixi/sound or Howler.js — don't roll our own)

## Cross-references

- File 22: companion-track scope for the demo + data export
- File 24: demo1 implementation prompt (this doc + file 25 are its companion docs)
- File 25: visual content R&D scope (parallel structure to this doc)
- File 17 § "Color integration": the engine's color system that audio doesn't directly use, but visual + audio should feel cohesive (warm-tinted scene = warm-tinted music)

## Status checkpoints

Update as audio R&D progresses:

- [ ] Tier 1 procedural pipeline established (ability SFX synthesis)
- [ ] Tier 2 evaluation completed — decision on which curated SFX pack(s) to integrate
- [ ] Tier 3 evaluation completed — decision on AI-generated music + signature drop chime
- [ ] Family playtest #1 (audio feedback after Phase 4)
- [ ] Family playtest #2 (audio feedback after Phase 5)
- [ ] Final audio pass + mix balance check (Phase 6)
- [ ] Demo1 ships with [TIER MIX TBD] as audio approach
