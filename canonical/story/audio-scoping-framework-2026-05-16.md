# Audio Scoping Framework — Sub-Axis Decomposition + Phase-1 Decision Surface

**Status:** **Canonical-story design framework.** Authored 2026-05-16 (Day 4 evening) by gandalf on Pattern-A commission from knight-rider (Matt-authorized 2026-05-16). Companions and supersedes (in framing scope) the same-day `audio-strategy-phase0.md`: that doc closed the immediate P6.b deferral question (music + SFX → Phase-1+); this doc decomposes WHAT audio is — at the sub-axis level — so Phase-1 scoping does not inherit a re-occurrence of P6 (audio-as-atomic-deferral) one milestone later.

**Why both docs exist:**
- `audio-strategy-phase0.md` answered: *"is audio in scope for any pre-Phase-1 ship?"* (No, except a near-zero-cost Step-B audit amendment.) That doc is the Phase-0 lock.
- **This doc** answers the deeper question my own P6 forward audit raised but `audio-strategy-phase0.md` deliberately did not extend into: *"when Phase 1 starts and audio promotes to active scope, what AXES of audio need framing, decision, vendor-class taxonomy, and dependency mapping?"*

Without this doc, the same Pattern-P6 risk recurs: "audio is Phase-1+" treats audio as atomic, and Phase-1 ship-pressure will discover that audio is six-to-eight independent sub-axes, each with its own vendor class, license discipline, register decision, and cross-seam coupling. This doc decomposes the atomic deferral.

**Companion docs:**
- `canonical/story/audio-strategy-phase0.md` — the same-day Phase-0 lock (music deferred indefinitely via Matt's AI-music workflow; SFX deferred to Phase-1+ with Step-B audit amendment); this doc extends into the Phase-1 framing
- `canonical/story/p6-forward-audit-2026-05-16.md` § VS2b Full Pimen catalogue integration — the CRITICAL finding this doc + the Phase-0 doc together close
- `canonical/story/drift-audit.md` Pattern P6 — the meta-pattern this doc prevents from recurring at the Phase-1 boundary
- `canonical/story/style-register.md` — the visual register lock; pattern-precedent for how a multi-axis design space gets decomposed for catalogue work
- `canonical/story/spirit-guide-voice.md` § Q1, Q3 — voice-actor / TTS questions explicitly deferred to audio work; this doc receives that hand-off
- `canonical/story/form-bias-cadence-strategy.md` § 6 cipher architecture — informs audio's coupling to per-season vocabulary
- `canonical/story/embodiment-narrative-layer.md` — informs per-embodiment audio variance question (sub-axis 1)

**Pending:**
- knight-rider receives completion report (this doc + key Matt-decision surfaces)
- Matt-decision surfaces in § 4 await routing — most are Phase-1 promotion-time decisions, not Day-4 decisions; this doc's purpose is to make sure they're framed for promotion-time
- Drift-audit Pattern-P6.b status update — already "RESOLVED 2026-05-16" via Phase-0 doc; this doc adds the framing depth (P6 prevention forward-into-Phase-1) and does NOT change the Phase-0 status
- No decisions-log entry needed; this is a Phase-1 framing doc, not a Phase-0 lock

**This doc explicitly does NOT:**
- Specify per-axis design (that's Phase-1 commission territory per Matt direction)
- Identify or recommend vendors (no Legolas Mode-A audio crawl has been commissioned)
- Author the Stage-3+ Spirit-Guide voice-synthesis implementation (separate Stage-3+ work)
- Curate music tracks (Matt's AI-music workflow IS the music strategy per Phase-0 doc)
- Investigate VFX-vendor companion audio (Step-B Tier-1 amendment in `audio-strategy-phase0.md` handles that)
- Make purchase recommendations

---

## 0. TL;DR

Audio is **not one axis** — it is **seven independent sub-axes**, three vendor classes, and at least six cross-seam dependencies. Today's Phase-0 deferral (per `audio-strategy-phase0.md`) is correct AND insufficient — it solves the immediate P6.b surface but leaves the Phase-1 promotion vulnerable to recurrence of P6 in finer-grained form.

**The seven sub-axes:**
1. **SFX-combat (skill-effect audio)** — coupled to VFX catalogue per geometry × element
2. **SFX-impact (hit/damage/death audio)** — coupled to combat-feedback layer
3. **SFX-ambient (per-season environmental audio)** — coupled to per-season cosmology
4. **SFX-UI (interaction/menu/affordance audio)** — coupled to UI surface decisions
5. **SFX-ritual (Trial/Passage/Ascension moment audio)** — coupled to ritual trilogy + Spirit-Guide voice
6. **Spirit-Guide voice (synthesized or VA-performed)** — coupled to Stage-3+ cipher migration + Spirit-Guide register lock
7. **Music score (per-season + per-moment)** — currently Matt-personal AI-music workflow (Phase-0 lock); commissionable-track future

**Three vendor classes:** sound-effect pack vendors; voice-synthesis / TTS services; royalty-free music libraries + AI-music generators. Plus a fourth-edge: VFX vendors with companion audio (handled by Step-B amendment).

**Six+ cross-seam dependencies:** Spirit-Guide voice depends on Stage-3+ cipher migration; UI audio depends on demo UI lock; ritual audio depends on ritual-trilogy specifics; ambient audio depends on per-season cosmology + style-register; combat SFX depends on VFX catalogue coverage; music depends on personal-workflow durability (and pitch-positioning trigger).

**Five+ Matt-decision surfaces:** spread across Phase-1, Phase-1.5, and Phase-2; framed now so promotion-time work has the option-space ready.

**Severity-tier per sub-axis:** see § 8 summary table. CRITICAL: none currently (all Phase-1+; closed by Phase-0 doc for Phase-0 ship). WATCH (Phase-1 promotion gate): SFX-combat, SFX-impact, Spirit-Guide-voice. OK-deferrable: SFX-ambient, SFX-UI, SFX-ritual, music score.

---

## 1. Dimensional framework — the seven sub-axes

Audio in a real-time isometric ARPG is not a single asset class. The standard genre-canon decomposition (per Diablo II/III/IV + PoE + Last Epoch + Grim Dawn dev talks + GDC audio-design tracks) breaks audio into independently-sourced, independently-licensed, independently-mixed sub-systems. Reincarnated inherits this decomposition.

### Sub-axis 1 — SFX-combat (skill-effect audio)

**What it is:** the audio companion to skill-effect VFX. Every cast, every projectile, every AoE, every channel, every damage-tick has a sound signature. Diablo II's "Fireball whoosh + explosion impact" is the canonical example; PoE's "spell-effect-per-gem" pattern is the modern continuation.

**Reincarnated-specific framing:** per the project's geometry × element × tier architecture (per doc 37 § 6 cipher + `form-bias-cadence-strategy.md` § 6), combat SFX coverage decomposes into:
- Per-geometry archetype (16-type active palette per Phase-2 lock; expanding to ~20 with B11 + B13 additions) × per-element (canonical-four + per-season vocabulary variants) × per-tier (basic/empowered/legendary)
- Theoretical coverage matrix: ~20 geometries × ~6-12 elements × 3 tiers = 360-720 distinct audio events
- Practical coverage: vendor packs typically ship element-set + spell-archetype combinations; full matrix achievable through composition (per the VFX-catalogue-coupling pattern in `audio-strategy-phase0.md` Step-B amendment)

**Genre-precedent specificity:**
- **D2**: ~6-8 audio events per skill (cast / projectile-fly / impact / kill-hit / channel-loop / aftermath); sourced from in-house audio team + Hollywood SFX library samples
- **PoE**: per-gem audio identity; community has long noted "you can identify what skill a build uses just from sound"; this is *load-bearing* for combat-clarity in mob-density scenarios
- **Diablo IV**: per-class audio identity layered on per-skill audio — Sorceress chain-lightning sounds different from Druid chain-lightning even when the visual is similar; loadout-readability through audio
- **Last Epoch**: minimal per-skill audio differentiation — community feedback consistently flags this as one of LE's weakest game-feel dimensions despite strong build-craft systems

**Player-experience consequence:** **load-bearing for game-feel.** Silent combat reads as floaty even when VFX is rich. Combat-SFX is the difference between "the spell exists in the screen" and "the spell exists in the world." This is the dimension most likely to surface as playtest-signal post-Phase-0 if deferred too long.

**Severity for Phase-1 ship:** WATCH (likely CRITICAL by Phase-1 mid-cycle if a public-facing demo or pitch moment surfaces in Phase 1).

### Sub-axis 2 — SFX-impact (hit/damage/death/loot audio)

**What it is:** the audio companion to combat-feedback events. Distinct from skill-effect audio because impact is the FEEDBACK on the player's action, not the action itself. Hit-confirms ("did I hit?"), damage-feedback ("how hard?"), death audio ("did it die?"), loot-drop audio ("did something drop?"), loot-pickup audio ("did I get it?").

**Reincarnated-specific framing:**
- Per damage-type (canonical-four resistance categories + physical) × per impact-strength (light/medium/heavy/kill) × per target-class (humanoid/swarm/elemental/golem/cosmic — per embodiment taxonomy) = ~60-100 distinct impact events
- Loot-event audio (drop chime + pickup confirm + rarity-tier accent per Common/Magic/Rare/Legendary/Set) per `canonical/story/p6-forward-audit-2026-05-16.md` B16 loot-pillar finding
- Death-event audio per monster archetype + per player-death (canonical-significant moment; per `passage-moment-ritual.md`)

**Genre-precedent specificity:**
- **D2's "ka-ching" loot sound** is the most iconic single audio cue in ARPG history; rarity-coded chimes are genre-standard
- **D3 introduced per-rarity loot beams + per-rarity loot audio** — high-rarity loot has a distinct sound that players can hear-across-the-screen, allowing audio-driven loot triage without visual scan
- **PoE legendary drop tone** is universally recognized in PoE community; community trades on the audio recognition
- **Hit-confirm audio** is so load-bearing that ARPG playtests routinely flag "feels floaty" when impact audio is absent — even when impact VFX is present

**Player-experience consequence:** **load-bearing for game-feel AND for loot-clarity.** Loot audio is the AUDIO PILLAR of the loot-treadmill UX. Without it, mob-density loot scenarios devolve into visual scanning that doesn't scale.

**Severity for Phase-1 ship:** WATCH; promotes to CRITICAL when B16 loot-drop architecture ships (per P6 forward audit B16 Drift-12 candidate). Loot architecture without loot audio is structurally incomplete; the two should land together or in close sequence.

### Sub-axis 3 — SFX-ambient (per-season environmental audio)

**What it is:** the audio bed of the world. Wind, water, distant rumbles, ambient hum, creatures-off-screen, environmental atmospherics. The thing the player hears when no combat is happening. Distinct from music (which is composed); ambient is sourced/recorded environmental audio that LOOPS across an area without being foregrounded as a "song."

**Reincarnated-specific framing:**
- Per-season-cosmology ambient (the Deep Trench season's ambient is water-pressure-coded; the Yomi season's ambient is funeral-bell + cave-echo-coded; the Throne-Room season's ambient is hushed-grand-hall-coded)
- Per-anchor variance within season (different rooms within a season may carry slightly different ambient registers)
- Coupling to per-season cosmology generation: ambient audio could be sourced once per season (one ambient bed = one season) OR per anchor (more variance, more cost)

**Genre-precedent specificity:**
- **D2 Act I (Rogue Encampment) ambient** is one of the most-praised ambient beds in ARPG history — rain, hushed conversation, distant howls; creates the "tense outpost" feel without any music foregrounded
- **D3's Westmarch ambient** carries the city's anxiety; **D3 Act V Pandemonium Fortress** carries cosmic-horror-coded ambient
- **Hades's per-chamber audio** isn't ambient in the traditional sense (Supergiant uses music + audio-design integration) but the pattern of per-area audio-identity is informative
- **PoE's per-zone ambient** is one of the genre's most underrated achievements — each zone has a distinct audio identity that scales with the player's hundreds of hours of exposure

**Player-experience consequence:** load-bearing for **cosmological-coherence**. The Earth-Self journeying THROUGH SEASONS depends on each season FEELING different; visual style does some of that work; ambient audio does much of the rest. Without ambient audio, all seasons sound the same — which undermines the cosmology's central claim (seasonal-variety as the engine's load-bearing differentiator).

**Severity for Phase-1 ship:** OK-deferrable through Phase-1 early; promotes to WATCH at Phase-1.5 when seasonal-cosmology generation is shipping at full per-season variance. SFX-ambient is the audio dimension MOST coupled to the cipher-architecture and per-season-vocabulary work; should be framed to land WITH the per-season-content pipeline, not retrofitted after.

### Sub-axis 4 — SFX-UI (interaction/menu/affordance audio)

**What it is:** the audio companion to UI affordance events. Button-click, menu-open, item-equip, item-drop, tooltip-hover, error-state, confirmation-state, level-up chime, XP-gain feedback.

**Reincarnated-specific framing:**
- Per loadout-app event (equip, unequip, tooltip surface)
- Per skill-tree event (per `p6-forward-audit-2026-05-16.md` B6 finding — unlock-feedback affordance for tier unlocks)
- Per stat-allocation event (auto-allocate, level-up)
- Per Spirit-Guide UI surface (per `spirit-guide-voice.md` — gear-review surface; act-transition surface)
- Per ritual UI moment (Trial choice screen; Passage threshold; Ascension Court-introduction)

**Genre-precedent specificity:**
- **D2 inventory-Tetris audio** — the satisfying "thunk" of fitting an item in inventory is genre-canonical; D3 sacrificed this for grid-removal and community noticed
- **D4 paragon-board snap audio** — modern Blizzard's UI audio is mixed slightly hotter than gameplay because UI happens in quieter moments
- **PoE atlas-tree audio** is intentionally LOW-mix (PoE's UI is dense; loud UI audio would fatigue across hundreds of hours)
- **Mobile-genre UI audio** (Diablo Immortal, Raid: Shadow Legends) is mixed HOTTER than PC because mobile players play with audio in louder ambient environments

**Player-experience consequence:** medium-load-bearing. Silent UI is acceptable for a Phase-1 ship; UI without audio reads as "spreadsheet UI" but doesn't actively undermine the cosmology. The Spirit-Guide voice surfaces are a partial exception — if voice is implemented, the UI surface that carries voice must have at least an affordance audio.

**Severity for Phase-1 ship:** OK-deferrable. Promote to WATCH if mobile-platform consideration enters Phase-1+ scope (mobile UI audio is more load-bearing than PC).

### Sub-axis 5 — SFX-ritual (Trial/Passage/Ascension moment audio)

**What it is:** the audio companion to the ritual trilogy's canonical moments. These are NOT combat audio (per `trial-moment-ritual.md` etc. — combat is Phase 5 of each ritual; SFX-ritual is the Phase-1/2/3/4/6 audio that frames the combat). The ritual-frame audio is dramaturgically distinct.

**Reincarnated-specific framing:**
- Trial Phase 1 (Approach) — the "softening into significance" audio cue (per `trial-moment-ritual.md` Phase 1 — Spirit Guide softens into presence, wordless signal)
- Trial Phase 2 (Threshold) — Spirit Guide voice line; needs voice-or-silence decision (sub-axis 6)
- Trial Phase 3 (Choice) — the "what register is the choice rendered in?" audio decision
- Trial Phase 6 (Resolution) — closure audio
- Passage Phases 2-4 (canonical-silence per `passage-moment-ritual.md`) — the canonical-silence IS load-bearing; audio MUST honor it (anti-design constraint, not a positive sourcing question)
- Ascension Phases 2 + 3 + 5 (voice climax + Court reception + state-acknowledgment) — three voice lines per Ascension; voice surface decision lands here
- Court entry audio (per `court-of-forms.md`) — the "you are received" register

**Genre-precedent specificity:**
- **Dark Souls bonfire audio** is the canonical "moment-frame" audio in the soulslike genre; silence + crackling fire + brief musical motif; the audio MAKES the moment
- **Hades' chamber-entry audio** + Charon-encounter audio — Supergiant treats moment-frame audio as character-frame audio
- **D2's act-transition cinematic audio** — the cutscene-frame audio is distinct from gameplay audio; this is the closest D-series precedent
- **JRPG ritual audio** — Octopath Traveler's chapter-transition audio; Triangle Strategy's strategic-pause audio; HD-2D-genre handles ritual audio through restraint, not bombast

**Player-experience consequence:** **load-bearing for cosmological-weight**. The ritual moments ARE the cosmology made experiential; if they don't sound like rituals, they don't feel like rituals. The canonical-silence at Passage Phases 2-4 is the most load-bearing single audio decision in the project (silence is a positive design commitment; it requires structural enforcement just as much as positive audio events do).

**Severity for Phase-1 ship:** OK-deferrable at Phase-1 entry. Promotes to WATCH at first ritual ship (Trial first, per ritual-trilogy doc order). Tightly coupled to sub-axis 6 (Spirit-Guide voice) — should be scoped together.

### Sub-axis 6 — Spirit-Guide voice (synthesized or VA-performed)

**What it is:** the audio surface for the Spirit Guide's spoken lines. Currently (Phase 0) text-only per `spirit-guide-voice.md` Q1. The voice register is locked at the text layer; the audio implementation is deferred to this commission's framing.

**Reincarnated-specific framing:**
- **Decision-axis:** text-only (Phase-0 baseline) / TTS-synthesized (mid-cost; consistency challenges) / voice-actor-performed (high-cost; high-quality)
- Per-season-line volume: per `spirit-guide-voice.md` ritual surfaces (2 Trial lines × 3 Trials + 1 Passage line × N Passages + 3 Ascension lines × 1 Ascension + functional-surface lines) = ~10-30 voice lines per season
- Per-act register variance (Reserved / Warmed / Companion arcs) — voice rendering must respect this arc
- Earth-Self-name pronunciation handling (per `spirit-guide-voice.md` Q3 — player-named Earth Self, potentially in non-English-alphabet)
- LLM-generated content (voice lines are LLM-generated per `spirit-guide-voice.md`'s LLM prompt construction guidance) — every-season-different content means every line must be voiced in-season (rules out a pre-recorded line library at the obvious level)

**Genre-precedent specificity:**
- **Beatrice (Re:Zero) — Satomi Arai performance** is the canonical reference per `spirit-guide-voice.md` (Japanese VA); English-dub Beatrice is performed by Caitlin Glass (the localization comparison is the relevant reference)
- **Galadriel (Cate Blanchett, LotR films)** — adjacent mythic-mentor performance; sparse precise speech; voice-actor performance carries the mythic weight
- **TTS in 2026** is dramatically better than 2020 (ElevenLabs, OpenAI Voice, Microsoft Custom Voice all ship consistent-character-voice with sub-cent per-line cost) — but consistency-across-generations remains the binding constraint for character work
- **Hades' fully-voiced cast** is the gold-standard of in-roguelike voice; 80+ characters, hundreds of lines each, Supergiant team of voice actors over years
- **Mobile-ARPG voice patterns** (Diablo Immortal, RAID: Shadow Legends) use TTS-augmented hybrid voice; mobile-genre tolerates TTS register if character consistency holds
- **Disco Elysium's fully-voiced narrator** (2021 voice update) — extreme example; demonstrates LLM-era-feasible-just-barely

**Player-experience consequence:** **transformatively load-bearing**. The Spirit Guide is the player's primary in-fiction relationship (per `spirit-guide-voice.md` § "Why the Spirit Guide voice is load-bearing"). Text-only is acceptable; voiced is genre-elevation; voiced-poorly is worse than text-only.

**Severity for Phase-1 ship:** WATCH — defaults to text-only continuation (Phase-0 inheritance); promote to active decision at Phase-1 mid-cycle when LLM voice-synthesis ecosystem decision can include 6-9 months more landscape maturation. Tightly coupled to Stage-3+ cipher migration: cipher-migration changes the LLM-visible-surface; voice-synthesis pipelines consume that surface; voice decision should land AFTER cipher migration locks (not before — otherwise voice prompts may carry pre-cipher leaks).

### Sub-axis 7 — Music score (per-season + per-moment)

**What it is:** composed music. Per-season main themes, per-moment musical motifs (Trial-fight crescendo; Passage-transition motif; Ascension-Court fanfare), combat music, hub music, world-traversal music.

**Reincarnated-specific framing per `audio-strategy-phase0.md` Phase-0 lock:**
- **Music is currently Matt-personal-workflow** — AI-music-generator (Suno / Udio / equivalent) fed with seasonal flavor text
- Per-season main theme generated personally by Matt at near-zero project cost
- Phase-0 lock holds indefinitely per the Phase-0 doc; no commission needed
- Phase-1+ promotion-trigger: if pitch-positioning requires production-track music; if playtest signal flags music absence/quality; if AI-music landscape regresses

**Genre-precedent specificity:**
- **D2's per-act music** (Matt Uelmen) is genre-defining; sets the bar for memorable ARPG music
- **D3's per-area music** is broader, less iconic
- **PoE's music** is competent-but-forgettable — and PoE community largely doesn't complain (build-craft community over-weights mechanics over music)
- **Hades's music** (Darren Korb) is fully-composed character-music; competitive-with-D2 for genre-best modern ARPG-adjacent score
- **AI-music in 2026** (Suno v4+, Udio, Stable Audio): production-quality output for short-form (under 4 minutes); per-track licensing-still-ambiguous in commercial-distribution contexts; sufficient-for-personal-and-playtest use; INSUFFICIENT-for-commercial-ship without license clarity

**Player-experience consequence:** medium-load-bearing for Phase 1; HIGH-load-bearing for any commercial ship. Phase-0 player-experience (family playtest; no commercial distribution) is well-served by Matt's workflow. Commercial-ship requires either licensed-commercial-AI-music tools, royalty-free music library curation, OR commissioned-composer work.

**Severity for Phase-1 ship:** OK-deferrable per `audio-strategy-phase0.md` Phase-0 lock. Re-assessment trigger: pitch-positioning / commercial-distribution / playtest-signal-flip.

---

## 2. Independent vs coupled axes

Not all seven sub-axes are independent. Knowing the coupling map prevents the false economy of "let's scope SFX-combat in isolation" when SFX-combat is coupled to SFX-impact and both are coupled to VFX catalogue.

### Coupling map

```
Sub-axis              | Coupled to (must scope together OR in close sequence)
----------------------|------------------------------------------------------------
1. SFX-combat         | VFX catalogue (per geometry × element); sub-axis 2 (impact)
2. SFX-impact         | Sub-axis 1 (combat); B16 loot architecture; combat damage-resolver
3. SFX-ambient        | Per-season cosmology; style-register; cipher architecture
4. SFX-UI             | UI surface decisions (loadout, demo, skill tree); ritual UI
5. SFX-ritual         | Sub-axis 6 (voice); ritual-trilogy docs; sub-axis 7 (music at climaxes)
6. Spirit-Guide voice | Stage-3+ cipher migration; spirit-guide-voice.md; sub-axis 5 (ritual)
7. Music score        | Matt-personal-workflow (currently); pitch-positioning (future trigger)
```

### Independent clusters (scope-as-unit candidates)

**Cluster I — Combat-feel cluster:** sub-axes 1 + 2 + (partial 5 — combat phase of rituals). Should be scoped as one Phase-1 commission. Vendor sourcing overlaps heavily (sound-effect packs typically ship combat + impact together). Coupling to VFX catalogue is tight; this cluster's Phase-1 commission should pair with VFX catalogue Phase-1 maturation.

**Cluster II — World-feel cluster:** sub-axis 3 (ambient) + (partial 7 — music when integrated with ambient). Per-season; coupling to cosmology. This cluster's Phase-1 commission should pair with per-season-content-pipeline shipping (likely later than Cluster I).

**Cluster III — Voice-and-ritual cluster:** sub-axes 5 + 6 + (partial 7 — ritual-climax musical motifs). Tightly coupled. Voice decision (TTS / VA / continue-text-only) drives ritual audio scope. This cluster's Phase-1 commission should pair with Stage-3+ cipher migration completion (per dependency map § 4).

**Cluster IV — UI-feel cluster:** sub-axis 4. Independent; smallest scope; most deferrable. Phase-1.5 or Phase-2 timing.

**Cluster V — Music score:** sub-axis 7 standalone. Currently Phase-0 locked per `audio-strategy-phase0.md`. Promotion-triggered.

The cluster-as-unit framing is operationally important: a Phase-1 commission for "audio" without clustering would inherit the same atomic-deferral failure mode P6 names. Clustering allows Phase-1 commissions to land in dependency-correct sequence.

---

## 3. Vendor-class taxonomy

Analogous to the visual-style-register catalogue work (`style-register.md` + Legolas Mode-B crawls), audio sourcing decomposes into vendor classes with distinct license patterns and integration profiles.

### Class A — Sound-effect pack vendors (royalty-free libraries)

**What they ship:** packaged collections of sound effects — typically organized by category (combat / UI / impact / ambient / environmental). Sold per-pack with one-time license fee; some subscription models exist.

**Example vendor tiers** (not endorsements — illustrative of the market):
- **High-end:** Soundly, Boom Library, A Sound Effect (curated marketplace)
- **Mid-tier:** Sonniss GameAudioGDC archives (annual free release; mid-quality production); Pro Sound Effects
- **itch.io-tier:** Kenney Game Assets (CC0 / free), individual indie audio creators
- **VFX-vendor companions:** Pimen, CodeManu (per `audio-strategy-phase0.md` Step-B amendment audit)

**License patterns:**
- **One-time purchase + perpetual royalty-free use** (most common; e.g., Boom Library) — pay once, use forever, in any number of products, no per-stream / per-broadcast tracking
- **Subscription + use-while-active** (Soundly model) — access during subscription; outputs retainable but new sourcing requires active sub
- **Per-project commercial license** (some Pro Sound Effects packs) — license per game-product; sequel requires re-license
- **CC0 / Public Domain** (Kenney; some itch.io) — no license requirements; provenance-tracking still recommended
- **CC-BY** (some Sonniss; some itch.io) — attribution required; usable commercially

**Reincarnated-fit:** Class A is the dominant sourcing path for sub-axes 1 (combat), 2 (impact), 3 (ambient), 4 (UI). Mature market; competitive pricing; license patterns are well-understood (analogous to VFX catalogue vendors).

### Class B — Voice-synthesis / TTS services

**What they ship:** API access to text-to-speech synthesis with character-voice consistency. Per-character pricing typical.

**Example vendor tiers:**
- **High-end:** ElevenLabs (consistent character voices; cloning capability; per-character + per-minute pricing); OpenAI Voice (high-quality but per-API-call); Microsoft Custom Voice (enterprise-tier)
- **Mid-tier:** Murf, Replica Studios, Resemble AI
- **Open-source / self-hosted:** Coqui TTS (deprecated but archived); various Hugging Face TTS models; Bark

**License patterns:**
- **Per-character / per-minute synthesis** with commercial-use rights typical (ElevenLabs) — pricing scales with content volume
- **Voice-cloning licenses** — if cloning a specific voice actor's voice with permission, separate licensing required (varies by service + by voice-source)
- **Output-ownership** — most services grant output ownership; some retain training-rights on inputs (sensitive question for unique character voices)
- **Synthesis-consistency drift** — services have varying levels of "same voice across many generations" reliability; this is a quality-axis, not a license axis, but affects total-cost-of-ownership

**Reincarnated-fit:** Class B is the candidate sourcing path for sub-axis 6 (Spirit-Guide voice). Per-season line volume (~10-30 lines) × per-line synthesis cost (~$0.01-0.05) = ~$0.30-$1.50 per season at scale. CHEAP at the per-season level; the binding constraint is consistency-of-character-voice-across-seasons (a one-Beatrice-voice player should hear the same Beatrice in season 50 as in season 1).

### Class C — Royalty-free music libraries + AI-music generators

**What they ship:** music tracks (libraries) or music-generation API access (AI generators).

**Example vendor tiers:**
- **Royalty-free libraries:** Epidemic Sound, Artlist, Soundstripe, Musicbed, ASCAP-cleared libraries
- **AI-music generators (current Matt-workflow):** Suno (v4+ as of 2026), Udio, Stable Audio
- **Composer commission:** direct hire (Hades-pattern; Darren Korb model)
- **Public domain + Creative Commons:** YouTube Audio Library, ccMixter, Free Music Archive

**License patterns** (genuinely distinct from sound-effect patterns):
- **Sync rights** — music for video/game requires sync license; royalty-free libraries pre-clear sync; AI-generators are ambiguous-by-jurisdiction
- **Per-stream / per-broadcast** — broadcast contexts (Twitch, YouTube) sometimes trigger per-stream royalty; royalty-free libraries clear this; AI-music output is ambiguous (Suno's commercial-tier clears it; consumer-tier does not)
- **Mechanical reproduction rights** — relevant if music ships ON DISC (less relevant for digital distribution)
- **Performance rights organizations** (PRO — ASCAP, BMI, SESAC) — registered compositions trigger PRO collection on broadcast/streaming; royalty-free libraries handle this; AI-music landscape is in flux on this point
- **Music-stem licensing** — some libraries allow stem-level access (separate drums, melody, etc.) for adaptive-music systems; specialized; price premium

**Reincarnated-fit:** Class C is the sourcing path for sub-axis 7. Current Phase-0 lock holds (Matt's AI-music workflow IS the strategy). Phase-1 promotion would re-engage this class with the license-clearance discipline above.

### Class D — VFX-vendor companion audio (edge class)

**What they ship:** VFX packs that include companion audio (cast SFX, impact SFX) bundled in.

**Status:** handled by `audio-strategy-phase0.md` Step-B amendment. Class D is a near-zero-cost partial-coverage layer; not a primary sourcing strategy but a "free option" if VFX vendors happen to ship audio.

**License pattern:** typically inherits the VFX pack's license (one license covers VFX + audio companion). This is operationally simple; no separate audio license discipline required.

**Reincarnated-fit:** Class D is the audit's "starting inventory" for sub-axes 1 + 2. Step-B Tier-1 audit (per `audio-strategy-phase0.md`) populates Phase-1 with this data; Phase-1 commission then knows which sub-axis coverage is partially-pre-existing vs needs-Class-A-sourcing.

### Vendor-class summary table

| Class | Sub-axes served | License patterns | Maturity in 2026 | Phase-1 sourcing path |
|---|---|---|---|---|
| A — SFX pack vendors | 1, 2, 3, 4 | Royalty-free perpetual / subscription / per-project | High; mature market | PRIMARY for combat / impact / ambient / UI |
| B — Voice-synthesis | 6 | Per-character / per-minute; output-ownership grants | Mid; rapid maturation | PRIMARY for Spirit-Guide voice (if voiced) |
| C — Music libraries + AI | 7 | Sync / per-stream / PRO / royalty-free | Royalty-free: high; AI: rapidly maturing but license-ambiguous | DEFERRED per Phase-0 lock; trigger-promoted |
| D — VFX-vendor companion | Partial 1, 2 | Inherits VFX license | Variable per vendor | OPPORTUNISTIC via Step-B amendment |

---

## 4. Per-axis VS2a/VS2b/Phase-1 scoping question — Matt-decision surfaces

For each sub-axis, the Phase-1-promotion question is framed as a Matt-decision surface. Most decisions are NOT Day-4 decisions; they are PROMOTION-TIME decisions. The framing here ensures the decision is ready when promotion arrives.

### Decision surface 1 — SFX-combat (sub-axis 1)

**Question:** when SFX-combat promotes to active scope, what coverage strategy ships first?

**Options:**
- **1A — Step-B-audit-driven** (lowest-cost): use audit-discovered VFX-vendor companion audio as the first SFX-combat coverage; cover gaps with targeted Class-A sourcing
- **1B — Class-A-primary** (mid-cost; cleanest register): treat SFX-combat as an independent sourcing axis; commission a Legolas Mode-A SFX-vendor crawl analogous to the visual VFX crawl; lock an SFX register; source from Class-A vendors aligned to register
- **1C — Hybrid-staged** (recommended for Phase-1): Step-B audit data inventories partial coverage; Class-A primary sourcing fills gaps with register-locked Class-A vendors; coverage matrix tracked per geometry × element
- **1D — Full-commissioned audio design** (highest-cost; deferred indefinitely for Phase-0/Phase-1 context): contract an audio designer to compose per-skill audio bespoke; D2-Matt-Uelmen pattern

**Recommended:** 1C for Phase-1 promotion; reassess at Phase-2 if commercial-distribution context surfaces.

**Promotion trigger:** Phase-1 start OR playtest signal flagging combat-feel issues OR pitch / showcase context.

### Decision surface 2 — SFX-impact (sub-axis 2)

**Question:** when does SFX-impact land — independently, with SFX-combat, or with B16 loot architecture?

**Options:**
- **2A — Bundle with SFX-combat** (Cluster I per § 2): scope together; same vendor crawl; same register lock
- **2B — Bundle with B16 loot architecture**: scope alongside loot drop work; loot audio as the entry point; combat impact audio retrofits
- **2C — Split**: impact audio for combat goes with Cluster I; impact audio for loot goes with B16; same audit / vendor sourcing supports both

**Recommended:** 2C — split, with shared sourcing. Loot-impact audio and combat-impact audio share Class-A vendor sources but ship at different milestones (Cluster I for combat; B16-shipped for loot).

**Promotion trigger:** Phase-1 + B16 work activation.

### Decision surface 3 — SFX-ambient (sub-axis 3)

**Question:** when does ambient audio promote, and at what per-season granularity?

**Options:**
- **3A — One ambient bed per season** (low-cost; low-variance): one looping ambient track per season-cosmology; suffices for player-experience differentiation; sourced from Class-A or AI-generated
- **3B — Per-anchor ambient within season** (mid-cost; mid-variance): each anchor (town hub, dungeon, boss chamber) has its own ambient layer; more sourcing work; richer feel
- **3C — Procedural-ambient layering** (high-complexity): ambient elements (wind, distant, environmental detail) layer compositionally per encounter context; like adaptive music but for ambient; closest to Hades / AAA-industry pattern; out-of-scope for Phase-1

**Recommended:** 3A for Phase-1 entry; 3B as Phase-1.5 deepening if per-season-cosmology pipeline is mature enough to consume per-anchor metadata.

**Promotion trigger:** per-season-cosmology generation shipping at full per-season variance (likely Phase-1.5).

### Decision surface 4 — SFX-UI (sub-axis 4)

**Question:** is UI audio in Phase-1 scope, or deferred to Phase-2?

**Options:**
- **4A — Phase-1 light coverage**: minimal UI audio (button-clicks, equip-chimes, level-up); ~10-20 events; low-cost; quick win for player-feel
- **4B — Phase-2 full coverage**: defer entirely to Phase-2; ship Phase-1 with silent UI; the cost is "feels like a spreadsheet"
- **4C — Trigger-conditional**: ship Phase-1 silent; promote on trigger (mobile-platform consideration; pitch-positioning; playtest signal)

**Recommended:** 4C — trigger-conditional. UI audio is the LEAST load-bearing sub-axis; structural deferral is fine.

**Promotion trigger:** mobile-platform decision OR pitch-positioning OR playtest signal.

### Decision surface 5 — SFX-ritual + Spirit-Guide voice (sub-axes 5 + 6, paired)

**Question:** does Spirit-Guide voice ship voiced or stay text-only in Phase-1? This drives SFX-ritual scope.

**Options:**
- **5A — Text-only continuation** (Phase-0 inheritance): Spirit-Guide voice stays text; ritual audio is minimal-frame (a few SFX cues; no voice rendering); cheapest; preserves Phase-0 register
- **5B — TTS-synthesized voice** (mid-cost; high-consistency-risk): per `spirit-guide-voice.md` Q1 — implement TTS for Spirit-Guide lines; choose Class-B vendor with consistent character-voice; ritual audio scope expands to include voice + supporting SFX-ritual
- **5C — Voice-actor-performed for canonical-locked utterances only**: per `spirit-guide-voice.md` § Specific locked utterances — record the ~5 canonical phrases with a VA (Beatrice-register, English-localization); other lines remain text OR are TTS-augmented in the VA's character voice
- **5D — Fully VA-performed**: every Spirit-Guide line voice-acted; Hades-pattern; HIGH cost; demands per-season content pipeline coordination with VA scheduling

**Recommended:** 5C for Phase-1 mid-cycle (hybrid VA + TTS; canonical-locked utterances anchor the voice register; LLM-generated variants TTS-augmented in the same voice). This honors `spirit-guide-voice.md`'s named locked utterances + register-anchor framing. Defer to Phase-2 if Phase-1 timing pressure binds; default to 5A through Phase-1 entry.

**Promotion trigger:** Phase-1 mid-cycle OR pitch-positioning showcasing Spirit-Guide voice OR voice-synthesis ecosystem reaches a maturity threshold that makes 5B reliable enough for character-work.

**Critical dependency:** Stage-3+ cipher migration MUST complete before voice rendering ships; voice synthesis consumes the LLM-visible-surface and pre-cipher leaks would corrupt the voice character (e.g., the synthesized voice reading the canonical-four labels would be canonically-broken).

### Decision surface 6 — Music score (sub-axis 7)

**Question:** does music promote out of Matt-personal-workflow scope?

**Options:**
- **6A — Indefinite Phase-0 lock continuation** (current state per `audio-strategy-phase0.md`): no change; Matt continues; project absorbs no music sourcing work
- **6B — Promote to royalty-free library curation**: Class-C library sourcing for per-season music; license-clear for commercial; bypasses AI-music license ambiguity
- **6C — Commission composer for signature themes only**: hire composer for ~3-5 signature pieces (Spirit-Guide theme; Court theme; Ascension theme); per-season music remains Matt-workflow
- **6D — Full composed soundtrack**: Hades-pattern; deferred indefinitely

**Recommended:** 6A continues through Phase-1; promotion-trigger:pitch-positioning OR commercial-distribution-context OR playtest-flip.

**Promotion trigger:** pitch / commercial / playtest-signal.

### Decision surface 7 — Audio register lock (cross-cutting)

**Question:** does audio need its own register lock analogous to `style-register.md`?

This is a meta-decision-surface — not per-axis, but cross-axis. Visual style register is HD-2D-pixel; audio register might be lo-fi-pixel-game-audio (chip-style; Pico-8-shaped) OR mid-fi-pixel-game-audio (Octopath-Traveler-shaped; "modern pixel-game audio") OR cinematic (Diablo-IV-shaped; full-orchestral + Hollywood-SFX-library register) OR something else.

**Options:**
- **7A — Lock audio register at Phase-1-promotion time** (paired with first audio commission): the register decision lives WITH the first audio sourcing commission; gandalf authors equivalent of `style-register.md` but for audio
- **7B — Defer register decision; let first commission set de-facto register**: cheaper short-term; risks Discipline-13 drift (the de-facto register accumulates without canonical lock)
- **7C — Lock register NOW** (Phase-0 forward-positioning): author canonical audio register before Phase-1 commissions begin; analogous to how `style-register.md` was authored before Legolas Mode-B crawls

**Recommended:** 7A — lock at Phase-1-promotion time, paired with first commission (Cluster I — combat + impact). Earlier (7C) is unnecessary because Phase-0 has no audio sourcing; later (7B) risks the Discipline-13 drift pattern that the style-register doc was authored to prevent on the visual side.

**Promotion trigger:** Phase-1 first audio commission authoring.

---

## 5. Cross-seam dependency map

Audio sub-axes depend on other project systems. The dependencies are NOT symmetric — audio depends on these systems; these systems do not depend on audio (with one exception, noted).

### Dependency graph

```
SUB-AXIS                    | DEPENDS ON                                    | DEPENDENCY KIND
----------------------------|-----------------------------------------------|-----------------
SFX-combat (1)              | VFX catalogue (geometry × element coverage)   | Asset-coupling
                            | Step-B Tier-1 audit (Class-D pre-coverage)    | Inventory-coupling
                            | Audio register lock (cross-cutting #7)        | Register-coupling
SFX-impact (2)              | B16 loot drop architecture                    | Event-source-coupling
                            | Combat damage-resolver                        | Event-source-coupling
                            | Spirit-Guide gear-review surface              | Surface-coupling
SFX-ambient (3)             | Per-season cosmology generation pipeline      | Content-source-coupling
                            | Style register (HD-2D-pixel)                  | Register-coupling
                            | Cipher architecture (per-season vocabulary)   | Content-source-coupling
SFX-UI (4)                  | Loadout app UI surface                        | Surface-coupling
                            | Demo skill-tree UI (B6)                       | Surface-coupling
                            | Spirit-Guide UI surfaces                      | Surface-coupling
                            | Ritual UI surfaces                            | Surface-coupling
SFX-ritual (5)              | Ritual trilogy canonical docs                 | Specification-coupling
                            | Sub-axis 6 (Spirit-Guide voice decision)      | Sibling-coupling
                            | Passage Phases 2-4 canonical-silence lock     | NEGATIVE-coupling
Spirit-Guide voice (6)      | Stage-3+ cipher migration (S3)                | BLOCKING dependency
                            | spirit-guide-voice.md canonical register      | Specification-coupling
                            | Earth-Self-name handling (Q3)                 | Per-player-data-coupling
                            | LLM-generated content pipeline                | Production-pipeline-coupling
Music score (7)             | Matt-personal-workflow (current)              | Operational-coupling
                            | Pitch-positioning state                       | Trigger-coupling
                            | AI-music landscape maturation                  | External-coupling
```

### Notable dependencies and their implications

**Dependency D1 — SFX-combat × VFX catalogue.** SFX-combat MUST be sourced AFTER (or co-extensively with) the VFX catalogue work. Audio without visual is not actionable; visual without audio is structurally-incomplete but operationally-shippable. Phase-1 SFX-combat commission should reference the Phase-1 VFX-catalogue-maturity state.

**Dependency D2 — Spirit-Guide voice × Stage-3+ cipher migration.** This is the LOAD-BEARING dependency. Voice synthesis consumes the LLM-visible surface. If the canonical-four cipher hasn't fully migrated (S3 per `p6-forward-audit-2026-05-16.md` § VS2b S3), voice prompts will leak canonical-four labels into synthesized voice. The Spirit-Guide reading "fire" or "water" canonically breaks the seasonal-vocabulary discipline (per `spirit-guide-voice.md` § What the Guide does NOT speak about).

**Mitigation:** Spirit-Guide voice ships AFTER S3 completes AND after the S3 paths-audit (per p6 forward audit § VS2b S3) has confirmed no canonical-four leaks through any LLM-consumed surface. This is a hard ordering constraint; voice MUST NOT ship before this.

**Dependency D3 — SFX-ritual × Passage canonical-silence.** The Passage moment's Phases 2-4 are canonical-silent per `passage-moment-ritual.md`. Audio MUST honor this silence. This is the project's most-load-bearing audio decision and it is a NEGATIVE decision (the absence of audio is positively specified). Any audio commission must structurally enforce this silence — not as an oversight ("we forgot to add audio there") but as a positive design specification ("audio is canonically absent at this moment").

**Recommended structural enforcement:** add to audio commission template a "canonical-silence lock check" — does the audio commission specify which moments are canonically silent? If not, reject.

**Dependency D4 — SFX-ambient × cipher architecture / per-season vocabulary.** Per-season ambient audio is coupled to per-season cosmology. The cipher architecture (per `form-bias-cadence-strategy.md` § 6) is the source-of-truth for per-season vocabulary. Ambient audio sourcing MUST consume per-season vocabulary metadata; otherwise ambient drifts away from cosmology.

**Mitigation:** ambient audio scope sequence: per-season-cosmology pipeline ships → per-season-vocabulary metadata stable → ambient sourcing commissions per-season ambient against that metadata. This is the same pattern as visual per-season VFX-selection — the metadata IS the catalogue's consumption key.

**Dependency D5 — SFX-UI × UI surface decisions.** UI audio depends on UI surface decisions being LOCKED. Sourcing UI audio for a "tooltip surface" that doesn't exist yet wastes the commission. UI audio should ship AFTER UI surfaces are stable (post-B6 skill-tree UI; post-Spirit-Guide-UI surface design; post-ritual UI surfaces).

**Reverse-dependency (one exception):** **UI audio decision MAY surface UI surface decisions earlier.** If audio commissioning surfaces "we don't know what UI surfaces will exist," that's an upstream-signal that UI surface scoping is implicit-bundled (per P6 forward audit sub-pattern P6.a). Audio scoping can surface implicit-UI-scope as a forcing function.

---

## 6. License-discipline considerations

Audio licensing is GENUINELY DIFFERENT from VFX licensing. This section surfaces the discipline gaps that a future Legolas Mode-A audio crawl + an Elrond audio catalogue rubric would need.

### What's different vs VFX licensing

**VFX license patterns (per the visual-catalogue work):**
- One-time purchase + perpetual royalty-free use is dominant
- Per-project licensing rare
- CC licensing common at the indie tier
- Attribution requirements moderate

**Audio license patterns differ in:**
- **Sync rights** — music specifically requires sync rights for use in video/game; SFX usually does not (or sync is implicit in the SFX pack license)
- **Per-stream / per-broadcast** — music broadcast (Twitch streaming; YouTube uploads of gameplay) sometimes triggers per-stream royalty; SFX rarely does; this matters for community-content (streamers playing the game)
- **Performance rights organizations (PRO)** — registered music compositions trigger PRO collection on broadcast/streaming; royalty-free libraries pre-clear this; AI-music landscape is ambiguous (Suno's commercial-tier vs consumer-tier have different PRO clearances)
- **Voice-cloning / voice-actor consent** — if a Class-B voice synthesis service is used with a cloned voice, the voice-source's consent + licensing terms govern downstream use; this is a HIGH-stakes legal area
- **Music-stem licensing** — adaptive music systems (where layers swap in/out) require stem-level access; specialized; expensive

### Discipline candidates for audio commissions

These are NEW disciplines that audio-specific commissions should enforce, analogous to Discipline #13 (implicit-pillar drift) and the cipher anti-bias scaffolding Discipline #14 candidate.

**Audio-Discipline candidate AD-1 — License-pattern explicit naming:**
Every audio sourcing commission must explicitly name the license pattern for each asset:
- Royalty-free perpetual? Subscription-bound? Per-project? Per-stream?
- Sync rights covered or separate?
- PRO clearance status (for music)?
- Voice-cloning provenance (for voice-synthesis-cloned voices)?

Without this naming, audio commissions can drift into license-ambiguous territory that surfaces only at commercial-distribution time (catastrophic timing).

**Audio-Discipline candidate AD-2 — Broadcast / streaming compatibility check:**
Reincarnated's commercial future includes potential streaming-community presence (Twitch streamers playing the game). Audio assets that don't clear streaming-broadcast use will trigger DMCA strikes against streamers, which catastrophically harms community. Every audio asset commissioned must pass a streaming-clearance check.

**Audio-Discipline candidate AD-3 — Voice-synthesis consent + provenance discipline:**
If Class-B voice synthesis is used with cloned voices, the source voice's consent + licensing terms must be tracked at the catalogue level. AI-voice-cloning legal landscape is in active flux (2026); this discipline future-proofs against legal-exposure shifts.

**Audio-Discipline candidate AD-4 — Canonical-silence structural lock:**
Per dependency D3 above. Audio commissions must explicitly enumerate canonical-silence moments (Passage Phases 2-4; Trial Phase 3 choice; combat-witness-only Spirit-Guide silence per `spirit-guide-voice.md`). The absence of audio at these moments is a positive design specification; the discipline enforces this structurally.

**Audio-Discipline candidate AD-5 — Per-season vocabulary consumption (for ambient):**
SFX-ambient commissions must consume per-season vocabulary metadata, not source against canonical-four labels. Same anti-bias scaffolding discipline as the Discipline #14 candidate for visual; applied to audio.

These five candidates should land in `engineering-disciplines.md` (jack-ryan territory) at audio-commission promotion time. Not now; not yet. But framed now so promotion-time discipline-codification has the candidates ready.

---

## 7. First-order recommendations

### Severity tier per sub-axis (for Phase-1 ship)

| Sub-axis | Severity | Justification |
|---|---|---|
| 1 — SFX-combat | WATCH → CRITICAL on showcase trigger | Game-feel load-bearing; silent combat reads as floaty even with VFX |
| 2 — SFX-impact | WATCH → CRITICAL on B16 ship | Loot architecture without loot audio is structurally incomplete |
| 3 — SFX-ambient | OK → WATCH on per-season-cosmology pipeline shipping | Cosmological-coherence load-bearing but defers cleanly |
| 4 — SFX-UI | OK → WATCH on mobile-platform consideration | Least load-bearing; structural deferral fine |
| 5 — SFX-ritual | OK → WATCH on first-ritual-ship | Tightly coupled to sub-axis 6; co-decision |
| 6 — Spirit-Guide voice | WATCH; default text-only continuation | Transformatively load-bearing IF voiced; safe to defer; HARD dependency on Stage-3+ cipher |
| 7 — Music score | OK (locked Phase-0 via Matt-workflow) | Re-trigger on pitch/commercial/playtest |

### Recommended Phase-1 sequence

**Phase-1 entry (immediate Phase-1 work):**
- Sub-axis 7 (music) — no change; continue Phase-0 workflow
- Sub-axis 6 (voice) — defaults to text-only continuation; no commission
- Audio register decision surface (#7 above) — author analogous to `style-register.md` at first commission authoring

**Phase-1 mid-cycle (first audio commission):**
- Cluster I commission: SFX-combat + SFX-impact (combat slice); Class-A vendor crawl via Legolas Mode-A; pair with VFX catalogue maturity
- Audio register lock: paired with this commission
- Disciplines AD-1, AD-2, AD-4 codified at this stage

**Phase-1 late (after Cluster I + Stage-3+ cipher S3 complete):**
- Cluster III commission: SFX-ritual + Spirit-Guide voice decision; voice-decision-surface (#5) activated; Discipline AD-3 codified if Class-B voice is selected
- Cluster II commission: SFX-ambient, sequenced behind per-season-cosmology pipeline maturity; Discipline AD-5 codified

**Phase-2:**
- Cluster IV commission: SFX-UI; cheapest; lowest-priority
- Re-evaluation of music sub-axis based on pitch / commercial trajectory

### Recommended next actions

For Matt (Day-4 / immediate decisions):
- **No immediate decisions required.** This doc's purpose is Phase-1 framing readiness; the Phase-0 lock per `audio-strategy-phase0.md` holds.
- Note for Matt: the seven sub-axes + cluster framing here will surface at Phase-1 commission-authoring time; this doc IS the reference for that future moment.

For knight-rider (commission queue):
- **No immediate commissions to author.** Cluster I commission (combat + impact) becomes the first audio commission at Phase-1 entry; this doc + `audio-strategy-phase0.md` + the Step-B audit data are the precursors that ready it.
- Add to Phase-1 dispatch-queue tracking: "first audio commission = Cluster I; precursors ready."

For gandalf (self):
- Re-read this doc at Phase-1 audio-commission authoring time; refresh against landscape changes (voice-synthesis maturation; AI-music license-clarity shifts; per-season-pipeline state).
- Watch for promotion-triggers (playtest signal flagging combat-feel issues; pitch / showcase context; mobile-platform consideration) and surface accordingly.
- At Phase-1 entry, draft audio register lock doc (analogous to `style-register.md`) paired with first commission authoring.

For jack-ryan (engineering-disciplines):
- The five audio-discipline candidates (AD-1 through AD-5) are queued for Phase-1 commission-authoring-time codification. Not now; tracked here.

---

## 8. Severity / decision-surface summary

### Severity table (consolidated)

| Sub-axis | Severity (current) | Severity (Phase-1 mid) | Severity (Phase-1 late) | Decision-surface ID |
|---|---|---|---|---|
| 1 — SFX-combat | OK (Phase-0 deferred) | WATCH | CRITICAL | DS-1 |
| 2 — SFX-impact | OK (Phase-0 deferred) | WATCH | WATCH | DS-2 |
| 3 — SFX-ambient | OK | OK | WATCH | DS-3 |
| 4 — SFX-UI | OK | OK | OK | DS-4 |
| 5 — SFX-ritual | OK | OK | WATCH | DS-5 (paired with DS-6) |
| 6 — Spirit-Guide voice | OK (text-only) | WATCH | WATCH | DS-5 |
| 7 — Music score | OK (Matt-workflow) | OK | OK | DS-6 |
| Cross-cutting — audio register | OK | DECISION (at first commission) | LOCKED | DS-7 |

### Matt-decision surfaces (consolidated, framed for Phase-1 promotion)

| ID | Decision question | Recommended option | Promotion trigger |
|---|---|---|---|
| DS-1 | SFX-combat coverage strategy | 1C — hybrid-staged (Step-B audit + Class-A primary) | Phase-1 start / showcase / playtest |
| DS-2 | SFX-impact bundling | 2C — split; shared sourcing; bundled with combat + B16 separately | Phase-1 + B16 |
| DS-3 | SFX-ambient granularity | 3A → 3B as per-season pipeline matures | Per-season-cosmology pipeline shipping |
| DS-4 | SFX-UI Phase-1 inclusion | 4C — trigger-conditional | Mobile / pitch / playtest |
| DS-5 | Spirit-Guide voice surface | 5C — hybrid VA + TTS for canonical-locked utterances | Phase-1 mid-cycle + Stage-3+ cipher complete |
| DS-6 | Music score promotion | 6A — continue Phase-0 workflow indefinitely | Pitch / commercial / playtest |
| DS-7 | Audio register lock | 7A — lock paired with first commission | First audio commission authoring |

---

## 9. What this doc DOESN'T do (acknowledged out-of-scope)

- **Does not commission Legolas Mode-A audio vendor crawl.** That's a separate later commission per the request scope.
- **Does not specify per-sub-axis design specs.** Framing pass only; per-axis design specs land when Phase-1 commissions activate per direction.
- **Does not identify specific vendors or make purchase recommendations.** Vendor-class taxonomy only; specific vendor identification awaits Mode-A crawl.
- **Does not modify engine code, schema, or any implementation surface.** Design-doc only.
- **Does not implement Spirit-Guide voice synthesis.** Stage-3+ work; this doc frames the decision surface.
- **Does not curate music tracks.** Matt's workflow IS the strategy per Phase-0 doc.
- **Does not extend into Pimen / CreativeKind / character-track audio investigation.** Those are VFX/sprite vendor categories; companion-audio audit is handled by `audio-strategy-phase0.md` Step-B amendment.
- **Does not author the audio register lock doc.** That happens at Phase-1 first-commission authoring per DS-7 recommendation.
- **Does not codify the five audio-discipline candidates (AD-1 through AD-5) into `engineering-disciplines.md`.** That's jack-ryan territory at Phase-1 commission-authoring time.

---

## 10. Maintenance protocol

When Phase-1 audio scope activates (any sub-axis):
1. Re-read this doc.
2. Use the decision-surface table (§ 8) to identify which decision needs to land for the activating sub-axis.
3. Author the audio register lock doc (if first commission) per DS-7 recommendation.
4. Surface the relevant audio-discipline candidates (AD-1 through AD-5) to jack-ryan for engineering-disciplines codification.
5. Reference the dependency map (§ 5) to ensure ordering constraints (notably D2 — voice depends on Stage-3+ cipher complete; D3 — canonical-silence enforcement; D4 — ambient depends on per-season-vocabulary metadata) are honored.

When voice-synthesis landscape materially shifts (new vendors; license-pattern changes; quality-threshold crossings):
1. Re-read sub-axis 6 + Class-B taxonomy + DS-5.
2. Update recommended option for DS-5 if landscape shift changes the calculus.

When pitch / commercial / playtest triggers fire on any deferred axis:
1. Re-read the relevant decision surface in § 8.
2. Promote to active scope; commission per the recommended option.

When future P6 forward-audit re-runs occur:
1. Confirm this doc still names the audio sub-axes correctly (no NEW axes emerged?).
2. Confirm the Phase-1 scoping plan still holds (no new ship-pressures recurring P6 at the audio boundary?).
3. If a new audio sub-axis emerges, append to this doc; do not silently rewrite the seven-axis frame.

When `audio-strategy-phase0.md` Phase-0 lock changes (music promotes; SFX promotes pre-Phase-1):
1. This doc inherits the change; update DS-1, DS-6, and severity tables.
2. Preserve Phase-0 lock history; don't retroactively rewrite.

— gandalf, 2026-05-16 (Day 4 evening)
