# Audio Register Canon — Sonic Identity Lock for Reincarnated

> **STATUS:** HISTORICAL-INFORMATIVE (pre-Epoch-4; consult for lineage only — not current truth) — see `canonical/00-ground-state.md` for current truth

**Status:** **Canonical-story design lock.** Authored 2026-05-17 by gandalf per dispatch `agentic_orchestration/dispatches/2026-05-17-gandalf-audio-register-sonic-identity-canon-queued.md` (Matt L3 audio research authorization 2026-05-17 late evening). Auto-fired after gandalf D11 post-mortem completion + legolas-4 audio vendor catalogue crawl completion (both shipped 2026-05-17). Canon-authoring scope; no tag.

**Predecessor inputs (binding):**
- `agentic_orchestration/research/catalogue/audio-vendors-2026-05-17/coverage-matrix.md` — legolas-4 empirical anchor (35 packs / 18 vendors / 4 sonic clusters); the asset landscape this canon scores against
- `agentic_orchestration/research/catalogue/audio-vendors-2026-05-17/inventory.jsonl` — per-pack JSONL inventory; consumption-time filter target
- `canonical/story/audio-scoping-framework-2026-05-16.md` — the seven-sub-axis framework + cluster decomposition; this canon resolves Cluster I (combat-feel) + Cluster II (world-feel) at register-level
- `canonical/story/audio-strategy-phase0.md` — the Phase-0 silent-ship lock; this canon supplements (does NOT supersede) it by establishing the register that Phase-1+ commission work fires against
- `canonical/story/style-register.md` — visual register HYBRID a3 (HD-2D pixel-art); informs sonic-register match-or-contrast decision
- `canonical/story/vs2a-vfx-scene-needs.md` — register-fence-per-UI-surface authoring rule + per-encounter VFX presence (Section 1.2); the parallel for SFX-tier per-encounter authoring
- `agentic_orchestration/research/curated/vfx-layered-architecture-vs2a-2026-05-17.md` — elrond's 4-layer VFX architecture (substrate / class-archetype / physical / atmospheric); this canon mirrors with a 5-layer SFX architecture (Section 4)
- `reincarnated-demo/src/audio/audio.ts` — current Tier-1 procedural + Tier-2 file-mapping baseline; the integration surface this canon's engineering notes consume

**Companion docs (cross-reference, non-binding):**
- `canonical/story/mobile-feel-target-doe-2026-05-17.md` — DoE ultra-fast combat pace; informs polyphony cap + non-fatigue discipline
- `canonical/story/mobile-pc-pixel-sizing-ratios-2026-05-17.md` — register-fence-per-surface precedent (visual); SFX-tier-fence-per-surface mirrors at sonic layer
- `canonical/story/spirit-guide-voice.md` — voice-register lock; forward-flag in § 9 builds against this canonical text-layer register
- `canonical/story/passage-moment-ritual.md` + `canonical/story/court-of-forms.md` + future `trial-moment-ritual.md` — ritual canonical-silence constraint anchors

**Downstream consumers:**
- elrond — audio-pack curation (auto-fires on this completion per `2026-05-17-elrond-audio-pack-curation-queued.md`); consumes Section 2 cluster lock + Section 3 element signature table as curation criterion
- drax — engine-side integration (future wiring dispatch); consumes Section 4 layered architecture + Section 9 engineering notes
- star-lord — telemetry instrumentation; consumes Section 9 audio-event metric recommendations
- matt — decisions, especially Q1 register lock (§ 2) + Q6 music strategy (§ 8)

**Pending:**
- knight-rider drafts decisions-log entry on the sonic register cluster lock (Q1) + the music-register cleanup (Q6) at promotion to commission
- elrond auto-fires audio-pack curation against this canon
- drax future-dispatch consumes Section 9 at integration time (no immediate engine work this canon)
- Matt L3 on Q6 specific path (Section 8 ranks options; Matt selects)

**Authoring boundary.** This is a register canon. It is NOT:
- a per-pack acquisition recommendation (elrond's curation; consumes this canon)
- engine-side audio code (drax's lane post-curation)
- a voice-over commission decision (§ 9 forward-flag only; future dispatch)
- a Phase-0 acquisition spend authorization (Matt L3 required at acquisition time)
- an amendment to `audio-scoping-framework-2026-05-16.md` (this canon references; does not edit)

---

## 1. Executive summary

**Reincarnated's sonic identity is HYBRID — pixel-game retro spell SFX over HD-cinematic ambient beds, with a mid-fi orchestral-synth music register and clean foley impact layer underneath everything.** This is the audio analog of the locked HYBRID a3 visual register (`style-register.md`): not pure-retro (which reads indie-coded; doesn't carry mythic weight), not pure-cinematic (which reads register-mismatched against pixel sprites and produces uncanny valley between sight and sound), but the genre-correct hybrid that anchors the isekai-ARPG positioning the project commits to.

The five-layer sonic architecture mirrors elrond's four-layer VFX architecture with one addition (music as its own tier). The eight-element signature table establishes per-element timbre / pitch / reverb / spectral envelope / reference exemplar — including a flagged register-attention zone for **holy** (legolas-4 found NO explicit retro-register holy SFX pack; this canon notes the construction path). The loudness discipline target is **-12 LUFS short-term for combat-critical / -18 LUFS for ambient / -16 LUFS integrated for music**, with hard sidechain ducking on combat-critical → ambient at -6 dB and Spirit-Guide voice → music at -8 dB. Polyphony cap is 8 simultaneous combat SFX channels with oldest-drop-on-overflow. Player vs enemy emitter distinction is **same-file + per-emitter mix-bus** (not paired files), preserving curation simplicity and enabling runtime panning + reverb-tail differentiation.

The music gap for D10 seasons 002011-015 (currently silent fallback) is recommended **Option B (Suno per-season generation against canonical retro-JRPG anchor prompt)** as the operational path, with Option A (reuse 001001-005 as placeholder) as the immediate unblock if Suno license clarity stalls. Voice-over is forward-flagged as a future dispatch; the canon prescribes register language and acquisition triage but does not commit. Engineering notes for drax + star-lord land at Section 9, including a folder-schema recommendation (`/audio/sfx/{layer}/{element}_{geometry_archetype}.ogg`) and three telemetry metrics worth instrumenting at integration time.

The whole canon's load-bearing claim: **Reincarnated's audio identity is the same architectural shape as its visual identity — register-fence-per-surface, hybrid-not-mixed-within-frame, anchored against shipped genre precedent (D2 / D-Immortal / Octopath / Sea of Stars in different mix proportions per layer).** Get the register right, the curation is straightforward; get the register wrong, every SFX call carries cognitive load.

---

## 2. Sonic register cluster lock (Q1)

### 2.1 The decision

**LOCKED:** Reincarnated's canonical sonic register is **HYBRID — Cluster A (retro-pixel) for skill SFX + Cluster C (HD-cinematic) for ambient + Cluster B (mid-fi orchestral-synth) for music + Cluster D (minimal/generic) for UI + foley underlayers as construction primitives only.**

This **endorses legolas-4's pragmatic recommendation** ("Cluster A spell SFX + Cluster C ambient — pixel-game sound in combat; environmental HD in biome") and **amends it** with two specifications legolas did not commit to:

1. **Music goes Cluster B (mid-fi orchestral-synth)**, NOT Cluster C (HD-cinematic). Legolas left music register implicit. This canon makes the call: HD-cinematic music over pixel-game combat reads as register-mismatch (the FFXVI-pretending-to-be-FFVI problem). Mid-fi orchestral-synth (Fire Emblem / FFXVI mobile / modern JRPG-adjacent) lands at the same register-altitude as the visual HD-2D pixel art — pixel-bounded fidelity with hand-drawn / mid-fi production sensibility. This is the music-register equivalent of `style-register.md`'s Candidate B lock.
2. **UI goes Cluster D (minimal/generic) deliberately**, not Cluster A. UI SFX in retro-pixel register foregrounds itself in a way that fatigues across hundreds of hours (PoE GGG postmortem evidence; D3 inventory click was deliberately re-mixed quieter in 2014 patches). Cluster D placeholder-grade SFX is *correct* at the UI tier — clean clicks, low color, no genre weight. This is the audio analog of the visual register's stats-block fence: UI surface is **not** where genre identity lives.

### 2.2 Why HYBRID (the design judgment)

The four clusters legolas-4 surfaced map to known shipped patterns. Each pure-cluster option has a failure mode in Reincarnated's context:

**Pure-Cluster-A (retro-pixel everything).** Shipped by Stardew Valley, Hyper Light Drifter, Crawl, Dead Cells (with caveats). Indie-coded. The combat audio reads as Octopath Traveler's combat audio (which is a fine register for skill SFX) but the ambient beds at this fidelity read as Game Boy ambient — a low-fi pad that doesn't carry the *cosmological weight* the seasonal-journey demands. The Deep Trench season's water-pressure ambient cannot be Cluster A; it MUST be HD-recorded or HD-synthesized to feel like a place rather than a screen.

Diablo I/II shipped this lesson at genre-foundational level — Matt Uelmen's Tristram theme is technically lo-fi by modern standards but the Cathedral ambient (the drip, the distant echo, the *room*) is HD-recorded field audio. The combat SFX is mid-fi; the ambient bed is *somewhere else entirely*. Reincarnated inherits this DNA.

**Pure-Cluster-C (HD-cinematic everything).** Shipped by D3, D4, PoE2, Wolcen, Last Epoch (partial). AAA-grade. Register-mismatch against HD-2D pixel sprites. PoE2's HD audio over PoE1's pixel-resolution sprites in early-access reveal demos was *the* most-complained-about audio-visual mismatch in ARPG community discourse for two months — until GGG explicitly re-pixel-rezzed assets. The lesson: HD audio assumes HD visuals, and the inverse — pixel visuals against AAA audio reads as the player wearing two different pairs of glasses simultaneously.

The exception is **ambient**. Ambient is the layer most distant from the visible action; the player's brain accepts ambient at higher fidelity than the foregrounded combat audio because ambient is the *space*, not the *event*. This is the D2 Tristram pattern restated.

**Pure-Cluster-B (mid-fi orchestral-synth everything).** Shipped by Octopath Traveler (closest), Triangle Strategy, Fire Emblem Three Houses, Sea of Stars. JRPG-adjacent canon. Best fit for music — but mid-fi-synth combat SFX *reads as music*, not as combat. The cast/hit/impact moments lose their punchy transient character when rendered at this register. Combat needs sharp-attack, fast-decay, percussive transients — the Cluster A pixel-game-retro register ships exactly this.

**Pure-Cluster-D (minimal/generic everything).** Placeholder-grade. Acceptable for prototyping; sub-genre-correct for nothing. Not a serious candidate for ship.

**Hybrid (the lock).** Mirrors the visual register's hybrid logic. Each layer gets the cluster that matches its dramaturgical function:

| Sonic layer | Cluster lock | Genre exemplar |
|---|---|---|
| **Skill SFX (combat events)** | Cluster A (retro-pixel; WSP / WS3 / WS1 / Leohpaz) | Octopath Traveler combat / Chrono Trigger spells / SNES-JRPG canon |
| **Impact / hit / death (combat feedback)** | Cluster A primary + Cluster D foley underlayers (Kenney Impact / OGA / TOM physical layer) | D2 hit-confirm / PoE rare-pack-clear / 16-bit JRPG hit register |
| **Ambient (per-biome environmental beds)** | Cluster C (David Dumais / Sonniss / Boom Library / kmontesdev) | D2 Cathedral / Hollow Knight ambient / Dark Souls bonfire-area |
| **Music (per-season score)** | Cluster B (mid-fi orchestral-synth via Suno against locked prompt OR Bit By Bit Sound retro-RPG library) | Octopath Traveler / Fire Emblem TH / Sea of Stars / FFXVI mobile |
| **UI (interaction events)** | Cluster D (Kenney Interface / OGA UI) + thin Cluster A accents at rarity-tier chimes only | PoE atlas-tree (LOW-mix) / D4 paragon-snap / mobile-genre clean UI |
| **Ritual moments (Trial / Passage / Ascension)** | Cluster C ambient + Cluster B musical-motif + Cluster A specific impact accents | Dark Souls bonfire / Hades chamber-entry / D2 act-transition cutscene |
| **Spirit-Guide voice** | Cluster B-adjacent (mid-fi vocal register, intimate close-mic) | Beatrice (Re:Zero) / Galadriel (LotR) / Hades-Charon |

### 2.3 Visual register match-or-contrast resolution

The visual register HYBRID a3 is **hand-drawn pixel-art HD-2D-shaped** (`style-register.md` Candidate B). The question this canon resolves: does the sonic register **match** (same hybrid logic) or **contrast** (deliberate fidelity divergence)?

**Match.** The sonic register adopts the same hybrid-with-fence logic as the visual register. Combat fidelity sits in pixel-game retro; ambient fidelity sits in HD-cinematic; music fidelity sits in mid-fi orchestral-synth (the audio equivalent of the visual HD-2D middle-fidelity register).

The audio analog of `style-register.md`'s "no within-frame mixing" rule: **no within-moment mixing of clusters.** A single combat moment is Cluster A skill SFX + Cluster A/D impact + Cluster C ambient bed underneath + Cluster B music underneath all of it. The clusters are layered in z-order (per Section 4), not mixed within a layer. The player's ear learns the geography after the first encounter; cognitive load stays low.

**Why match, not contrast.** Contrast (e.g., pixel visuals + HD-cinematic audio everywhere) is the PoE2-early-access mismatch failure. The genre's working-pattern is match. The audio-visual register-coherence is load-bearing for "this is one work, not two stapled together."

### 2.4 What this rules out

- **Pure-Cluster-A (everything pixel-game).** Ambient at retro-pixel fidelity reads as Game Boy. Forbidden for ambient layer.
- **Pure-Cluster-C (everything HD-cinematic).** Combat SFX at HD fidelity reads as PoE2-early-access mismatch. Forbidden for skill SFX + UI layers.
- **Dark-synth / Hotline-Miami register.** Wrong genre lineage. Acknowledged in dispatch options; rejected.
- **Pure-orchestral-fantasy-folk (Diablo Immortal mobile pivot register).** Acknowledged as a Cluster C variant for ambient possible; rejected as the music register because Immortal's mobile-pivot soundtrack reads less isekai-coded than Octopath Traveler's mid-fi orchestral-synth.
- **Within-moment cluster mixing.** A spell cast cannot fire a Cluster A whoosh layered with a Cluster C reverb-tail simultaneously *in the same channel*. Cluster differentiation lives at the layer architecture (Section 4), not within a single SFX file.

### 2.5 Pivot insurance

Per the score-don't-filter principle (AGENTS.md): elrond curates Cluster A, B, C, D packs with sonic-register tags. The consumption-time filter for Reincarnated's surface defaults to the cluster-per-layer mapping above. Other-cluster packs stay in the catalogue. If Matt ever pivots register (e.g., the project commits to all-HD-cinematic for a higher-fidelity pitch positioning), the catalogue is ready; the cost is in commissioned content already produced.

---

## 3. Element-to-sonic-signature mapping (Q2)

The eight-element signature table establishes per-element timbre / pitch range / reverb / spectral envelope / reference exemplar. This is the SFX analog of the canonical-7 substrate × element-palette mapping in `style-register.md` + `vs2a-vfx-scene-needs.md`. Each element has a *sonic identity* the player learns at trash-tier and recognizes across all geometry types and tiers within a season.

### 3.1 The signature table

| Element | Base timbre | Pitch range | Reverb / spatial | Spectral envelope | Reference exemplar | Cluster fit at retro-register |
|---|---|---|---|---|---|---|
| **fire** | Crackling + roar; transient pop on cast; sustained sizzle on burn DoT | Mid-low for body / sharp transient at peak | Dry close (combustion is local heat) | Bright + warm; mid-band rich; high-band crackle | Diablo II Fireball cast; FFVI Firaga; Octopath Traveler Sealticge fire | GREEN — multiple strong packs (WS3 / WSP / WS1 / Leohpaz) |
| **water** | Trickle + splash; viscous + flowing; freeze-snap on ice variant | Mid + sustained; ice-variant adds high-band crystal-shatter transient | Wet-mid (water is reverberant by nature) | Mid-band body + high-band droplet shimmer | Hollow Knight water-room ambient; FFXIV ice spells; Chrono Trigger water magic | GREEN — multiple packs (WS3 / FH / WS1); ice-variant well-covered |
| **earth** | Stone-grind + deep impact; rumble for sustained; rock-shatter on hit | Low + heavy; sub-bass body; transient at peak | Dry-low (mass-impact is non-reverberant) | Low-band rich; mid-band gritty; high-band sparse | Diablo II Stone Skin / Earthquake; Octopath Traveler boulder spells; LotR Balrog impact | GREEN — WS3 6-file earth + FH stone/lava; thinner than fire/lightning but workable |
| **wind** | Whoosh + howl; cutting / slicing on damage variant; sustained gust on AoE | High-mid + sustained; sharp transient on directional cuts | Open-air spatial (wind is spatially-extensive) | Mid-band airy + high-band whistle; low-band absent | Hyper Light Drifter dash; Octopath Traveler wind spells; D2 Tornado | GREEN — WS3 / WSP / FH / WS1; wind well-covered across packs |
| **lightning** | Electric-zap + thunderclap; crack on transient; sizzle on sustained | High + sharp transient; mid-band rumble on thunder | Wet-high (electricity ionizes air; thunderclap reverberates) | High-band rich; mid-band crack; low-band thunder | D2 Lightning Sentry / Charged Bolt; FFVI Bolt; PoE Arc | GREEN — WS3 / FH / WS1 / ELV pack 8; lightning has strongest coverage |
| **holy** | Bell-chime + choral; rising tone on cast; sustained shimmer on aura | High + sustained; transient at peak (bell-strike) | Wet-high (cathedral reverb is genre-canonical for holy) | High-band rich (bell harmonics); mid-band choral; low-band sparse | D2 Hammerdin Blessed Hammer; FFXIV White Mage; Octopath Traveler holy spells | **YELLOW at retro-register — FLAG.** WS3 Light + FH Divine exist; no explicit pixel-pack labeled "holy." See § 3.2 attention zone below. |
| **shadow** | Whispers + low-drone; cold-decay transient; sustained void hum | Low-mid + sustained; transient is muffled (shadow eats transient) | Wet-mid with extended decay tail | Low-band rich (subwoofer presence); mid-band whisper texture; high-band absent | D2 Necromancer Bone Spirit; FFXIV Black Mage; Hollow Knight Soul Master | GREEN — WS3 Dark / FH Dark / WSP Dark; shadow well-covered |
| **physical** | Clang + flesh-thud; metallic-strike on weapon variant; bone-crack on heavy impact | Mid + sharp transient; very short decay | Dry close (foley register; minimal reverb) | Mid-band body + high-band metallic transient + low-band thud | D2 Barbarian Whirlwind; Octopath Traveler Cyrus physical hits; Sea of Stars sword | GREEN — Kenney Impact / TOM bow+sword / OGA / Leohpaz Dungeon; foley-rich |

### 3.2 Register-attention zone — holy

**Critical insight from legolas-4 worth flagging here per dispatch directive.** Holy element SFX has **NO explicit retro-register pack**. The available holy SFX live in:

- **WOW Sound RPG Magic Pack 3 Elemental "Light"** — produced at mid-fi orchestral-synth register, not pixel-game retro
- **Fusehive Medieval Fantasy Magic Library "Divine"** — produced at HD-cinematic register
- **WSP (WOW Pixel Magic SFX Pack)** — covers most elements at retro-register; **holy is absent** from the WSP coverage

**The construction path.** Three options for landing holy SFX at the canonical retro-register:

1. **Composite construction** (recommended; same approach as drax's tint-composition for VFX). Layer WS3 Light at low-mix + add a bell-chime transient from Cluster A foley + apply pitch-shift to land at retro-band-fidelity. Net: holy SFX is *constructed*, not single-file-sourced.
2. **Register-mismatch acceptance for holy only.** Accept that holy SFX uses mid-fi register (WS3 Light at natural fidelity). Genre-precedent supports this — holy in JRPGs is often the *one* register-elevated element (FFVI's Holy is mid-fi while Fire/Bolt/Ice are sharp-attack; this is convention). The cost: holy fights register-coherence against its peer elements; the player may notice.
3. **Commission a retro-register holy pack** at Phase-1+ spend. Out of scope for VS2a; flag for Phase-1.

**This canon's recommendation: Path 1 (composite construction) for VS2a + VS2b.** Elrond's curation prepares the WS3 Light + bell-chime foley combination as the holy SFX recipe. Drax's audio integration at future-wiring-dispatch implements the composite at load time (analog to the B&W + COLOR tint composition in elrond's 4-layer VFX architecture § 2.3). The register-coherence is preserved through composition rather than through sourcing; flagged here so future audio commissions know holy is the under-covered element at this register.

### 3.3 Per-element layered audio composition

Each element's SFX is itself a stack (per the layered architecture in Section 4):

- **Cast layer** — attack transient + element-signature timbre (fire crackle / water trickle / etc.)
- **Travel layer** (for projectile / beam geometry) — sustained mid-spectrum body
- **Impact layer** — physical thud + element-signature impact (fire boom / water splash / earth rumble / etc.)
- **Status-apply layer** — element-signature trigger (burn = sizzle; freeze = crystal-snap; shock = electric-zap)
- **Status-ambient layer** — sustained element loop while status is active (burn DoT = sizzle loop; freeze = ice-crackle loop; shock = electric-hum loop)

The signature table above defines the *recognizable* sonic identity that holds across all five layers. The cast-fire transient, the travel-fire body, the impact-fire boom, the burn-status sizzle, and the burn-DoT sustained loop are all *recognizably fire* even though they sit in different layers of the architecture.

This is exactly the visual analog of "fire-element-palette-coherence across geometry types within a season" from `vs2a-vfx-scene-needs.md` Section 1.4 Continuity Rule R1. The sonic version: **element-signature coherence across SFX layers within a season.**

### 3.4 Per-season vocabulary variance — deferred

Per `style-register.md` cipher-architecture-compatibility note + `audio-scoping-framework-2026-05-16.md` § Sub-axis 3 coupling to cipher-architecture: the canonical-7 substrate × per-season vocabulary cipher means a season could plausibly want a per-season variation of an element's sonic signature ("this season's fire is *liquid memory* — the signature has more shimmer; less crackle"). This canon does NOT pre-commit to per-season SFX variance — that's a forward question for Stage-3+ cipher migration timing.

**Forward-flag:** at Stage-3+ cipher migration, evaluate whether per-season SFX variants are within commissioning budget (likely no for Phase-1; possibly yes for Phase-2 if vendor catalogue supports element-tint composition at SFX layer). For VS2a + VS2b: canonical-7 substrate sonic signatures hold across all seasons; per-season variance is in the *music* layer (per § 8) and in the *flavor-text register* (per `vs2a-vfx-scene-needs.md` register-fence rule).

---

## 4. Layered audio architecture (Q3)

### 4.1 The five-layer SFX model

Mirroring elrond's 4-layer VFX architecture with one addition (music as its own tier — visual has no music equivalent):

| Layer | Source cluster | Role | Render-pipeline target | Mirrors VFX layer |
|---|---|---|---|---|
| **Layer 1 — substrate SFX** | Cluster A (retro-pixel: WSP / WS3 / WS1) | Element × geometry × tier wiring; canonical-7 substrate × archetype-group coverage | Combat-SFX bus (Howler.js / Web Audio) | Layer 1 (Pimen) |
| **Layer 2 — class-archetype SFX** | Cluster A class-themed packs (TBD via elrond curation) | Active-spirit sonic register; composited ON TOP OF Layer 1 to produce class-specialized SFX for same substrate | Combat-SFX bus + class-overlay sub-mix | Layer 2 (Frostwindz class packs) |
| **Layer 3 — physical / foley** | Cluster D (Kenney Impact / TOM / OGA) + Cluster A foley | Hit-confirm / impact-feedback / physical-archetype Slot B/C; clean-attack transient under spell SFX | Combat-SFX bus + foley sub-mix | Layer 3 (Frostwindz Slashes + Impacts) |
| **Layer 4 — atmospheric** | Cluster C (David Dumais / kmontesdev / PixelLoops Ambient / Boom Library) | Full-scene biome-atmosphere bed; ambient room-theme loops; per-anchor ambient variance | Ambient-bus (separate mix; sidechain ducks under combat) | Layer 4 (Alenia Studios Atmospheric) |
| **Layer 5 — music** | Cluster B (Suno per-season OR Bit By Bit Sound) | Per-season score; per-moment musical motif; combat music; ritual music | Music-bus (separate mix; sidechain ducks under voice + ritual stinger) | NO VFX EQUIVALENT — music is the audio-medium-only tier |

### 4.2 Composition order (rendering / mix-bus structure)

Bottom to top in mix-bus z-order:

1. **Music (Layer 5)** — at master-music-volume; sidechained by Layer 6 voice + Layer 7 ritual stingers (when those fire)
2. **Atmospheric (Layer 4)** — at master-ambient-volume; sidechained by Layer 1 combat at -6 dB when combat-active
3. **Foley / Physical (Layer 3)** — at master-SFX-volume; fires synchronously with Layer 1 impacts
4. **Substrate SFX (Layer 1)** — at master-SFX-volume; the dominant combat audio
5. **Class-archetype SFX (Layer 2)** — at master-SFX-volume; composited on Layer 1 (same temporal moment; overlay register-tint analog)
6. **Voice (Spirit Guide; future, see § 9)** — at master-voice-volume; sidechains music + ambient; high mix priority
7. **Ritual stingers** (Trial / Passage / Ascension moment SFX) — at master-SFX-volume + brief boost; one-shot; sidechains music + ambient

### 4.3 Why a 5-layer SFX model (not the 6-layer dispatch sketch)

The dispatch Q3 sketched six potential layers (substrate / class-archetype / UI / ambient / music / combat-overlay). This canon collapses to five by:

- **Merging "combat-overlay" into Layer 1 substrate.** Combat-overlay (hit-on-target overlays; death stingers) is the IMPACT phase of the substrate SFX, not a separate layer. Sub-axis 2 of `audio-scoping-framework-2026-05-16.md` (SFX-impact) lives at Layer 1's per-element impact sub-layer + Layer 3 foley. No fifth/sixth bus needed.
- **Promoting UI to a separate bus, NOT a separate layer.** UI sound (button-click / menu-open / equip / etc.) doesn't co-occur with combat in the same composition-stack — UI happens in lull moments. UI gets its own mix-bus (master-UI-volume) at the engine level (Section 9), but architecturally it sits "outside" the five-layer combat stack. This is the audio analog of `vs2a-vfx-scene-needs.md`'s register-fence between stats-block and flavor-text-block: UI is a *different surface*, not a *different layer of the same surface*.

### 4.4 Interaction rules — ducking and sidechain discipline

The mix-bus structure produces several mandatory ducking rules:

| Source bus | Target bus | Ducking amount | Trigger |
|---|---|---|---|
| Layer 1 combat-SFX | Layer 4 ambient | -6 dB | Combat-active (last-cast-or-hit timestamp within 1.5s) |
| Layer 1 combat-SFX | Layer 5 music | -3 dB | Combat-active (last-cast-or-hit timestamp within 1.5s) |
| Voice (Layer 6) | Layer 5 music | -8 dB | Voice-active (currently-playing line) |
| Voice (Layer 6) | Layer 4 ambient | -6 dB | Voice-active |
| Voice (Layer 6) | Layer 1 combat-SFX | -3 dB | Voice-active during combat (rare; ritual moments may have combat + voice simultaneous) |
| Ritual stinger (Layer 7) | Layer 5 music | -10 dB for stinger duration + 1.0s tail | Ritual moment-trigger fires |
| Ritual stinger (Layer 7) | Layer 4 ambient | -8 dB for stinger duration + 1.0s tail | Same |

**Canonical-silence enforcement.** Passage Phases 2-4 (per `passage-moment-ritual.md`) carry canonical-silence — load-bearing positive design commitment. Implementation: a `silence-active` flag at the audio manager mutes Layer 1 + Layer 4 + Layer 5 + Layer 7 simultaneously; only Layer 6 voice + ambient room-tone at -24 dB (sub-audible floor) remain active. This is the structural enforcement `audio-scoping-framework-2026-05-16.md` § Sub-axis 5 named.

### 4.5 Layer 4 atmospheric — biome thematic mapping

Per elrond's 4-layer VFX architecture § 2.4 (Atmospheric layer): biome-thematic mapping enables environmental thematic identity. The sonic analog:

| Biome | Ambient bed (Cluster C) | Element-thematic SFX layer (Cluster A composite) |
|---|---|---|
| dungeon | PixelLoops Ambient / David Dumais dungeon | mid-mix shadow/earth element occasional drift |
| cave | PixelLoops Ambient cave / David Dumais caves | water-drip foley loop + earth-rumble distant |
| swamp | PixelLoops Ambient swamp | water/earth/poison element occasional drift |
| ruined-temple | PixelLoops Ambient ruins + magic | holy element occasional shimmer + wind drift |
| forest | PixelLoops Ambient forest / TomMusic free | wind element sustained + occasional water trickle |
| desert | PixelLoops Ambient desert / David Dumais desert | wind/earth element sustained |
| glowing-cave (gap) | David Dumais lava + cave composite | constructible; flag for elrond curation |
| sewer (gap) | David Dumais tar/mud + cave composite | constructible; flag for elrond curation |

Per coverage-matrix § 4: all biomes are GREEN or YELLOW; YELLOW gaps (glowing-cave / sewer) constructible from layered Cluster C primitives. This is consistent with the visual layer 4 atmospheric model.

### 4.6 Layer 1 substrate — archetype-group coverage

Per coverage-matrix § 1: SFX coverage is shared across geometry+element pairs via archetype groups (G1-G9). A single fire-projectile SFX serves `projectile+fire` / `multi_projectile+fire` / `fork+fire` / `ricochet_bounce+fire` because they share the same sonic signature (projectile-travel + fire-element). This reduces the effective 192-cell matrix to ~40-50 distinct sonic slots.

This canon endorses the archetype-group sharing. Sonic slot enumeration at Layer 1:

- **G1 PROJECTILE × 8 elements** = 8 slots
- **G2 MELEE × 8 elements** = 8 slots
- **G3 SINGLE-TARGET × 8 elements** = 8 slots
- **G4 AREA × 8 elements** = 8 slots
- **G5 BEAM × 8 elements** = 8 slots
- **G6 MOVEMENT × 8 elements** = 8 slots (most reuse cast-tier; partial coverage acceptable)
- **G7 AURA × 8 elements** = 8 slots (sustained loops)
- **G8 SLAM × 8 elements** = 8 slots
- **G9 BUFF × 8 elements** = 8 slots

Total Layer-1 sonic slots: **72 (9 groups × 8 elements)**, of which RED cells (5 per coverage-matrix) require construction via layer-composition. All 5 RED cells (water+slam / earth+beam / holy+slam / physical+beam / physical+aura) are constructible from available YELLOW-or-better vendors per the coverage matrix; no bespoke commission needed at VS2a.

### 4.7 Layer 2 class-archetype — coverage forward-flag

Frostwindz class packs (Blood Mage / Necromancer / Rogue / Starcaller / Vampire) ship VFX-only; SFX class-archetype coverage at Cluster A is uneven. Legolas-4 surfaced no class-archetype-specific audio packs at retro register. Two paths:

1. **Defer class-archetype audio to Phase-2.** VS2a + VS2b ship with Layer-1 substrate SFX only; Layer 2 class-archetype SFX is a Phase-2 commission.
2. **Construct class-archetype SFX via Layer-1 substrate-tinting at runtime.** A "Necromancer Spirit" emits Layer-1 shadow substrate SFX with a class-overlay filter (pitch-shift, reverb-tail extension, register-modulation). This is the audio analog of elrond's class-archetype VFX compositing-on-Layer-1.

**Recommendation:** Path 1 for VS2a + VS2b (substrate-only); Path 2 explored at Phase-2 if class-thematic audio identity surfaces as playtest signal. Layer 2's existence in the architecture is *forward-flag-only* for VS2a.

---

## 5. Loudness + signal-vs-noise discipline (Q4)

### 5.1 Per-layer LUFS targets

Mobile combat fires many simultaneous SFX (DoE ultra-fast pace per `mobile-feel-target-doe-2026-05-17.md`; 5+ enemies; AOE windups; hits; dodges; kills). Without loudness discipline → fatigue + signal loss. Per-layer LUFS targets:

| Layer | Short-term LUFS | Integrated LUFS | True-peak ceiling | Genre-precedent |
|---|---:|---:|---:|---|
| Layer 1 — Substrate SFX (combat-critical) | -12 LUFS | -16 LUFS | -1.0 dBTP | D3/D4 combat-critical SFX bus |
| Layer 2 — Class-archetype | -14 LUFS | -18 LUFS | -1.0 dBTP | (Layer 2 is composited under Layer 1; quieter by 2 dB) |
| Layer 3 — Foley / physical | -14 LUFS | -18 LUFS | -1.0 dBTP | D2 hit-confirm / Octopath hit foley |
| Layer 4 — Atmospheric | -18 LUFS | -22 LUFS | -2.0 dBTP | D2 Cathedral ambient / Hollow Knight room-bed |
| Layer 5 — Music | -14 LUFS short-term / -16 LUFS integrated | -16 LUFS integrated | -1.5 dBTP | Spotify mobile-mastering / streaming-platform integrated norm |
| Layer 6 — Voice (Spirit Guide; future) | -12 LUFS | -16 LUFS | -1.0 dBTP | Genre-standard voice-bus loudness |
| Layer 7 — Ritual stingers | -10 LUFS peak / -14 LUFS short-term | -16 LUFS integrated | -0.5 dBTP | D2 act-transition stingers / Dark Souls bonfire-light |

**Master-bus integrated target:** **-14 LUFS integrated for game-runtime mix**, consistent with mobile-ARPG-genre norms (Diablo Immortal lands ~-15; Raid Shadow Legends lands ~-14; PoE mobile target ~-14). The -14 LUFS target is intentionally *quieter* than streaming-platform-mastered (-9 to -11 LUFS for spotify-loudness-war norm) because **game audio fights itself across hundreds of hours of play**; loudness-fatigue is the binding constraint, not loudness-impact-at-first-listen.

### 5.2 Frequency-band stratification

To prevent spectral collision (e.g., earth-rumble + boss-music + ambient-thunder all sharing 60-120 Hz and producing mud), bands are stratified per layer:

| Frequency band | Layer 1 substrate | Layer 3 foley | Layer 4 ambient | Layer 5 music |
|---|---|---|---|---|
| Sub-bass (20-60 Hz) | sparse (earth-slam transient only) | minimal | rumble bed -22 LUFS | bass-line presence |
| Bass (60-200 Hz) | element-low-bodies (earth / shadow / fire-body) | thud transients | low-rumble bed | bass + low-mid |
| Low-mid (200-500 Hz) | element-mid-bodies (water / wind / fire / shadow) | flesh-thud transients | room-tone | mid-low instrumentation |
| Mid (500-2k Hz) | element-mid (most elements; vocal-presence range) | sword-clang / arrow-swish | mid presence | melody + voice |
| High-mid (2-5 kHz) | element-high (lightning / holy / ice) | metallic-clang transients | high-mid environment | brightness + clarity |
| High (5-12 kHz) | sharp transients (cast-attack + impact-snap) | metallic-shimmer | wind / leaves / shimmer | air + sparkle |
| Ultra-high (12 kHz+) | only at lightning + holy bell-strikes | brief shimmer accents | minimal | air + presence |

**Discipline:** at integration time (drax wiring dispatch), each layer's mix-bus carries a band-limiting EQ pre-set that pre-stratifies the spectrum. Layer 4 ambient bus is band-limited to bass-through-high-mid (no high frequencies — those belong to Layer 1). Layer 5 music bus carries the full spectrum but at -3 to -6 dB at the high-mid range where combat SFX dominates. This is genre-canon mixing discipline (D2 / D4 / PoE all ship this pattern).

### 5.3 Compression / sidechain rules

Per § 4.4 (ducking rules), the compression + sidechain implementation:

- **Layer 1 → Layer 4 sidechain** — Layer 4 ambient bus carries a sidechain-compressor keyed to Layer 1's combat-SFX bus. Threshold: -18 dBFS (Layer 1 SFX peaks); ratio: 4:1; attack: 5ms; release: 250ms. When combat fires, ambient ducks; when combat stops, ambient recovers within 250ms.
- **Layer 1 → Layer 5 sidechain** — Layer 5 music bus sidechain-compressor keyed to Layer 1; threshold: -16 dBFS; ratio: 2:1 (gentler than ambient ducking); attack: 10ms; release: 400ms. Music ducks less than ambient because music is dramaturgical and should remain *present* under combat.
- **Voice → Layer 5 sidechain** — Layer 5 sidechain keyed to voice bus; threshold: -24 dBFS; ratio: 6:1 (aggressive); attack: 20ms; release: 600ms. Voice ALWAYS surfaces over music (genre-canon for narrator-and-music interaction).
- **Voice → Layer 4 sidechain** — similar, threshold -20 dBFS / ratio 4:1 / attack 15ms / release 400ms.

### 5.4 Polyphony cap

**Cap: 8 simultaneous combat SFX channels (Layer 1 + Layer 2 + Layer 3 combined).** Oldest-drop-on-overflow. Layer 4 ambient is independent (single stereo channel, looped). Layer 5 music is independent (single stereo channel, looped). Layer 6 voice is independent (single mono channel, oldest-cancels-newest semantic — voice cuts off if new voice line fires before old completes).

**Rationale:** mobile ARPG combat at DoE ultra-fast pace (per `mobile-feel-target-doe-2026-05-17.md`) easily generates 12-20 simultaneous events in a packed room. Without cap → audio engine overload (Howler.js / Web Audio can manage ~32 simultaneous voices but loses dispatch precision at high counts) AND psychoacoustic mud (the player's ear can only resolve 4-6 simultaneous combat events; beyond that, additional channels add noise, not signal). The 8-channel cap is conservative; allows headroom; oldest-drop preserves the *latest* (most-recent player action) which is the player's cognitive focus.

This is genre-canon (D3 caps at ~16 voices; PoE mobile caps at 8; mobile-ARPG-platform-norm is 8-12).

### 5.5 Anti-fatigue rules

Beyond LUFS targets and band stratification, three anti-fatigue rules:

1. **Same-cast SFX limiter.** A cast SFX cannot fire more frequently than once per 80ms per (geometry × element) pair. Prevents stuttered overlap when the same skill fires many times in rapid succession (e.g., AOE rooms with many fire-projectiles). Beyond 80ms, the previous SFX is allowed to fade naturally; new cast plays at full volume; player perceives "many casts" without ear-fatigue.
2. **Pitched variation.** Same-cast SFX fires with ±100 cents random pitch variation. The variation is small enough to be perceptually identical but large enough to prevent the "phaser-effect mud" that identical waveforms produce when stacked. Genre-canon (D3 ships this on every SFX; PoE does it on melee impacts).
3. **Frequency cap on ritual stinger overlap.** Ritual stinger (Layer 7) can fire only once per 4.0s. Multiple rituals do not stack; if two ritual triggers fire within 4.0s, the SECOND is suppressed (with a debug log entry for star-lord telemetry — see § 9).

---

## 6. Player vs enemy emitter discipline (Q5)

### 6.1 The decision

**LOCKED: same SFX file + per-emitter mix-bus differentiation.** Player emitters and enemy emitters share the same SFX assets (same file paths; same Cluster A pack sourcing) but render through different mix buses with distinct panning, reverb, and EQ profiles.

### 6.2 Why same-file (not paired files)

The dispatch options:
- (a) Paired files — separate `ability_projectile_fire_player.ogg` + `ability_projectile_fire_enemy.ogg`
- (b) Same file + spatial mix differentiation

**Option (b) wins on three grounds:**

1. **Curation simplicity.** Elrond's pack selection at curation-time doesn't need to acquire two SFX per slot. Coverage matrix's 72 sonic slots × 2 emitter variants = 144 slot acquisitions vs 72 slots. Halves curation effort.
2. **Storage / load efficiency.** Howler.js + Web Audio asset load is a real cost on mobile. 72 files vs 144 files is meaningful storage-budget savings.
3. **Player cognition.** The player learns "fire-projectile sounds like THIS" once; the SAME sound coming from an enemy is recognized as fire-projectile-from-elsewhere, not as a new sonic entity. This is genre-canon (D2/D3/D4 use same-file with spatial differentiation; PoE does too).

### 6.3 Per-emitter mix-bus profile

Player emitter:
- Panning: center (0.0)
- Reverb: dry close (small room IR; tail 200ms)
- EQ: presence boost at 2-4 kHz (+2 dB) — brings player's own SFX *forward* in the mix
- Loudness: full mix-bus level (no attenuation)

Enemy emitter:
- Panning: stereo-positional based on enemy world-position relative to player
- Reverb: wet-mid (medium room IR; tail 500ms) — enemies sound "in the world"
- EQ: high-mid attenuation at 2-4 kHz (-1.5 dB) — pushes enemy SFX *back* in the mix
- Loudness: -3 dB attenuation relative to player bus

**Net effect:** player skills sound *closer, brighter, present*; enemy skills sound *further, more reverberant, in-the-world*. The player can identify their own action vs an enemy's action by sonic spatial-presence alone, without needing to look at the screen. This is critical for the DoE ultra-fast combat pace where attentional bandwidth is limited.

### 6.4 Engineering integration (preview of § 9)

Drax engine integration at future-wiring dispatch:

```ts
// Audio bus structure
audio.busses = {
  player_sfx: { reverb: 'dry_close', pan: 0.0, eq: { '2k-4k': +2.0 }, level: 0.0 },
  enemy_sfx: { reverb: 'wet_mid',   pan: 'spatial', eq: { '2k-4k': -1.5 }, level: -3.0 },
  ambient:   { reverb: 'wet_long',  pan: 0.0, eq: 'flat',                  level: -6.0 },
  music:     { reverb: 'flat',      pan: 0.0, eq: 'flat',                  level: -2.0 },
  voice:     { reverb: 'dry_close', pan: 0.0, eq: { '500-2k': +2.0 },      level: +1.0 },
  ui:        { reverb: 'flat',      pan: 0.0, eq: 'flat',                  level: -4.0 },
};

audio.playAbilityCast(geometry, element, emitter: 'player' | 'enemy' = 'player')
  // routes through audio.busses[emitter + '_sfx']
```

The current `audio.ts` lacks emitter parameter; the future-wiring dispatch adds it. The signature change is non-breaking (default `'player'` preserves current behavior); enemy emitters become identified at call site (the existing call sites are all player-initiated; enemy call sites are added at the same time as monster-skill-emission wiring).

### 6.5 Spatial panning per encounter type

Per `vs2a-vfx-scene-needs.md` Section 1.1 encounter-type table, the spatial-panning rules per emitter:

| Encounter type | Spatial panning rule |
|---|---|
| Swarm | Pack-cluster center used as emitter position (NOT per-unit) — prevents stereo-clutter from 5-12 simultaneous emitters |
| Trash | Per-unit emitter position |
| Magic | Per-unit emitter position |
| Pack | Per-unit emitter position; pack-shared aura uses pack-center |
| Elite | Per-unit emitter position; cast-charge audio uses center-bias (-30% pan magnitude) to ensure player-attention focus |
| Mini-boss | Per-unit emitter position; signature attacks use center-pan even at off-center positions |
| Boss / Trial | Always-center pan (the boss IS the encounter; spatial pan would dilute presence) |

This is the audio analog of `vs2a-vfx-scene-needs.md` Section 1.4 Continuity Rule R3 (cast-charge density monotonic with tier) — sonic-presence-density monotonic with tier through panning-magnitude.

---

## 7. Music gap pragmatic recommendation (Q6)

### 7.1 The gap

D10-curated 002011-015 seasons hit silent fallback per `audio.ts` `playMusic` `onloaderror` console log. 5 seasons; no per-season music files exist; the engine plays silent.

### 7.2 The five legolas-4-surfaced options

| Option | Cost | Effort | License clarity | Per-season identity | Demo-ship-ready |
|---|---|---|---|---|---|
| **A** — Reuse 001001-005 tracks | $0 | Zero | Clean (existing on-disk assets) | LOSS (same 5 tracks rotated across 10 seasons) | YES at acceptable degradation |
| **B** — Suno Pro per-season generation | ~$10/mo while generating | Low (Matt-personal-workflow) | AMBIGUOUS (WMG partnership improves but game-embedded clause uncertain) | HIGH (per-season unique) | Internal playtest YES; commercial ship CAUTION |
| **C** — CC0 fantasy music library | $0 | Manual curation per track | Clean (CC0) for OGA human-composed; AMBIGUOUS for Blacis AI-generated CC0 | MEDIUM (library scope-limited) | YES at curation cost |
| **D** — Bit By Bit Sound Ultimate Retro RPG Music | $77.60 one-time | Moderate (per-season assignment) | CLEAR (royalty-free + attribution) | MEDIUM (diverse library) | YES, demo-ship-ready |
| **E** — Procedural ambient via tone-stacks | $0 | Engineering effort | Clean (engine-generated) | LOW (procedural sameness) | NO (combat-feel gap) |

### 7.3 The recommendation

**Primary path: Option B (Suno Pro per-season generation against canonical retro-JRPG anchor prompt).** Matt's existing workflow scales to D10 002011-015 + future seasons. The canonical prompt anchor (per legolas's suggestion worth considering per dispatch directive):

> *"Retro JRPG fantasy game music, mid-fi orchestral-synth register, [per-season thematic flavor text], chiptune-bridged-to-orchestral, 16-bit-era SNES JRPG aesthetic reminiscent of Octopath Traveler / Fire Emblem / Sea of Stars, instrumental, 2-4 minute loopable, evocative not bombastic."*

The anchor preserves Cluster B (mid-fi orchestral-synth) as the canonical music register (§ 2.1 lock). Every Suno-generated season-track is prompted against the same register anchor; per-season flavor text drives thematic variance; the register stays consistent.

**Fallback (immediate unblock): Option A (reuse 001001-005 as placeholder rotation).** If Suno license clarity stalls or Matt is between Suno Pro subscriptions, reuse 001001-005 tracks rotated across 002011-015 as zero-cost unblock. Acceptable for internal playtest; not for demo ship.

**Demo-ship path (if Option B's license clarity remains insufficient): Option D (Bit By Bit Sound + attribution).** $77.60 one-time; royalty-free; attribution required in credits panel. Per-season assignment from the 410+ track library. Best long-term solution for demo-public-ship readiness.

### 7.4 Matt-flag — required L3 decisions

- **L3 decision #1:** Option B vs Option D for 002011-015 immediate fill. **Recommendation: B (Suno Pro)** for fastest iteration; **D (Bit By Bit Sound) at pre-demo-ship gate** when license clarity becomes load-bearing.
- **L3 decision #2:** $77.60 Bit By Bit Sound acquisition spend authorization, contingent on Option D selection.
- **L3 decision #3:** confirm canonical Suno prompt anchor (above) as locked music-register prompt — analogous to `style-register.md`'s LLM image-generation prompt anchor.

### 7.5 Why this (not the others)

- **Option A (reuse) alone** — acceptable as immediate unblock but loses per-season identity, which `audio-scoping-framework-2026-05-16.md` § Sub-axis 3 identifies as load-bearing for cosmological-coherence. Player journeying through seasons that all sound the same undermines the project's load-bearing differentiator.
- **Option C (CC0 library)** — Blacis 100+-track AI-generated CC0 pack is the largest matching catalogue, BUT same license-flux risk as Suno (AI-generated CC0 in 2026 carries unresolved jurisdictional questions). Pure human-composed CC0 (OGA fantasy collection) is license-clean but smaller, requires more curation effort, and is a step backward in production-quality vs Suno-generated.
- **Option E (procedural)** — engineering effort for ambient tone-stacks is meaningful (drax + engine-side); output quality is the lowest tier of all options; abandons the per-season music identity entirely. Rejected for ship; acceptable only as last-resort if all other options fail.

### 7.6 Forward implication — Phase-1+ music register

When Phase 1 starts (per `audio-strategy-phase0.md` Phase-1 revisit trigger), the music sub-axis (sub-axis 7) promotes to active commission consideration. This canon's music register lock (Cluster B mid-fi orchestral-synth via canonical Suno prompt OR Bit By Bit Sound library) is the inheritance. Phase-1 commission work either continues the Matt-personal-workflow OR commissions a composer (Hades / Darren Korb pattern) to compose against the locked register. Either way, the register stays Cluster B.

---

## 8. Voice-over forward-flag (Q7)

**This dispatch does NOT commit to voice-over decisions.** Per the audio-scoping-framework's Sub-axis 6 (Spirit-Guide voice) coupling to Stage-3+ cipher migration, voice work fires at Phase-1 mid-cycle at earliest. This canon scopes the question for a future dispatch.

### 8.1 Register

Voice register: **Cluster B-adjacent (mid-fi vocal, intimate close-mic).** Spirit Guide's voice register is established at the text layer per `spirit-guide-voice.md` (Beatrice-as-canonical-reference; sparse precise speech; per-act register variance through Reserved / Warmed / Companion arcs). The audio implementation maps text-layer register to:

- **Timbre:** clean vocal; intimate close-mic (sub-2-foot mic distance equivalent); minimal room-tone bleed
- **Pitch:** mid-vocal range (~200-400 Hz fundamental); avoid extremes
- **Reverb:** dry close (~50ms room-tone); no cathedral / no telephone-EQ
- **Mix:** -12 LUFS short-term / -16 integrated; sidechain priority HIGH (ducks music + ambient + combat per § 5.3)
- **Cluster-fit:** B-adjacent — the orchestral-synth music register reads against the vocal register coherently; clean mid-fi vocal sits naturally over Cluster B music. NOT Cluster A retro-pixel (8-bit-voice would be parodic) and NOT Cluster C HD-cinematic-voice (would over-fidelity the character).

### 8.2 Acquisition path triage (three options for future-dispatch decision)

| Option | Cost / line | Cost / season (10-30 lines) | Consistency | Time-to-ship |
|---|---|---|---|---|
| **Text-only continuation** | $0 | $0 | N/A | Immediate (Phase-0 inheritance) |
| **TTS-synthesized (ElevenLabs / OpenAI Voice / Microsoft Custom Voice)** | $0.01-0.05 | $0.30-1.50 | Good (2026 baseline) — per-character voice consistency reliable across hundreds of generations; verify per-vendor at commission | 1-2 weeks integration |
| **Voice-actor commissioned** | $50-500 / session | $100-500 (single session covers most lines) | Excellent (single human performer) | 4-12 weeks (casting + recording + iteration) |

### 8.3 Integration site

When voice promotes from text-only to audio:

- **Separate audio bus** — Layer 6 voice (per § 4.1)
- **Sidechain priority** — voice ducks music + ambient + combat per § 5.3
- **Per-language scaling** — text-only Phase-0 inheritance is per-language-already (English baseline); audio voice requires per-language commission OR per-language TTS-synthesis
- **Emit trigger** — engine emits a voice-line event with text + register + arc-position; voice-synth/playback layer (drax + future-voice-dispatch territory) resolves text → audio at runtime

### 8.4 Forward-dispatch scope

A future dispatch (Phase-1 mid-cycle) commissions voice-acquisition decision. This canon's contribution is to lock the **register** (Cluster B-adjacent, intimate close-mic, mid-fi vocal) so that whatever acquisition path is chosen, the output sits coherently within the five-layer architecture.

---

## 9. Engineering interaction notes for drax + star-lord (Q8)

These are informational notes for drax + star-lord at integration time. NOT engine work this canon authorizes; that's drax's lane post-curation per future-wiring dispatch.

### 9.1 File naming convention recommendation

Current `audio.ts` file-mapping convention:
```
/audio/sfx/ability_${geometry}_${element}.mp3
```

**Recommendation: extend to layer-aware path schema:**
```
/audio/sfx/{layer}/{element}_{geometry_archetype}.ogg
```

Examples:
- `/audio/sfx/layer1/fire_projectile.ogg` (Layer 1 substrate; fire element; G1 PROJECTILE archetype)
- `/audio/sfx/layer3/physical_melee.ogg` (Layer 3 foley; physical; G2 MELEE)
- `/audio/sfx/layer4/dungeon_ambient.ogg` (Layer 4 atmospheric; dungeon biome)
- `/audio/sfx/layer7/ritual_trial_stinger.ogg` (Layer 7 ritual stinger; trial moment)
- `/audio/music/{seasonId}.ogg` (Layer 5 music; per-season; unchanged from current)

**Rationale:**
- Layer-aware naming makes asset routing to mix-bus structure self-documenting
- Archetype-group naming (G1-G9) matches coverage-matrix § 1 → effective ~72-slot enumeration vs the 192-cell theoretical matrix; reduces file count
- OGG format default (Howler.js supports; smaller than mp3; license-clean) — current convention uses mp3 but ogg is preferred for game-runtime
- Naming preserves the current `audio.ts` `sfxPath()` function's role; minor refactor to accept layer + archetype-group parameters

### 9.2 Mobile audio context constraints

Per Howler.js + Web Audio API mobile constraints:
- **User-gesture-required activation.** Mobile browsers (iOS Safari especially) require user-gesture before audio context unlocks. Current `audio.ts` `getAudioCtx()` lazy-init handles this; no change needed.
- **Background-tab suspend.** Mobile browsers suspend audio context on background-tab. Howler.js auto-handles resume on focus; verify no regression at integration.
- **Memory pressure.** Layer 4 ambient + Layer 5 music are *streaming* candidates (Web Audio `html5: true` mode) to keep memory footprint low. Layer 1 SFX + Layer 3 foley should be *buffered* (default `html5: false`) for sub-50ms latency. The current `audio.ts` `playMusic` already uses `html5: false` for gapless looping at ~3-8 MB / track; verify mobile RAM headroom (mobile budget ~50 MB total audio cache; 5 seasons × 8 MB music = 40 MB; SFX + ambient must fit in remaining 10 MB).
- **Latency.** First-cast latency on mobile is typically 80-150ms after user-gesture-unlock; subsequent casts ~5-20ms. The polyphony cap (§ 5.4) helps; cold-cache misses can be warmed at room-load.

### 9.3 Audio-bus mixing implementation

Drax future-wiring dispatch implements the 5-layer bus structure (§ 4) as Howler.js sub-mix groups OR as Web Audio API GainNode chain. Howler.js native `Howler.volume()` is master; per-bus volumes require Web Audio routing via `Howler.ctx` + custom GainNode tree. Recommended structure:

```
Howler.ctx (root AudioContext)
  ├─ masterGain (Howler.volume)
  │   ├─ playerSfxGain      (level 1.0, pan 0.0, dryClose reverb)
  │   ├─ enemySfxGain       (level 0.71, spatial pan, wetMid reverb)   [-3 dB]
  │   ├─ foleyGain          (level 0.50, pan 0.0, dry)                  [-6 dB]
  │   ├─ ambientGain        (level 0.50, pan 0.0, wetLong reverb)       [-6 dB] [sidechain-target]
  │   ├─ musicGain          (level 0.79, pan 0.0, flat)                 [-2 dB] [sidechain-target]
  │   ├─ voiceGain          (level 1.12, pan 0.0, dryClose, EQ-presence)[+1 dB] [sidechain-source]
  │   └─ uiGain             (level 0.63, pan 0.0, flat)                 [-4 dB]
```

Sidechain-compressors per § 5.3 wire between source/target gain nodes. Mobile-compatible (Web Audio supported across mobile browsers since 2018).

### 9.4 Star-lord telemetry — three recommended metrics

Star-lord telemetry instrumentation at audio-event boundaries:

1. **`music_silent_fallback_fired`** — counter incremented when `audio.ts` `playMusic` hits `onloaderror` for a season ID. Tracks D10-style music-gap incidents; alerts at threshold (>1% of season-loads silent-fallback over 7-day window).
2. **`audio_polyphony_dropped`** — counter incremented when polyphony cap (§ 5.4) drops oldest channel. Sustained high count signals combat-density beyond mix-budget; informs cap tuning OR DoE pacing review.
3. **`canonical_silence_violated`** — counter incremented when Layer 1/4/5/7 fires while `silence-active` flag is set (Passage Phases 2-4). Should be zero in correct operation; non-zero indicates ritual-canonical-silence enforcement broken.

Optional fourth metric for richer instrumentation:
- **`sidechain_duck_latency_ms`** — histogram of latency between sidechain trigger and target-bus attenuation. Mobile platforms may vary; performance-budget signal.

Telemetry events emit through existing star-lord telemetry pipeline; schema additions are minor.

### 9.5 Drax integration sequence (future-wiring dispatch scope)

When drax's future-wiring dispatch fires, recommended sequence:

1. **Step 1:** Add `audio.ts` 5-layer bus structure (§ 9.3) — no asset acquisition required; existing procedural Tier-1 SFX routes through new buses.
2. **Step 2:** Implement sidechain-compressor wiring (§ 5.3) — five mandatory ducking rules.
3. **Step 3:** Wire ambient-bus to per-room loading (Layer 4 atmospheric); accept zero-asset fallback during transition.
4. **Step 4:** Extend `playAbilityCast` signature to accept emitter parameter (§ 6.4); backward-compatible default `'player'`.
5. **Step 5:** Add file-name convention extension (§ 9.1); transitional migration of existing files.
6. **Step 6:** Wire star-lord telemetry events (§ 9.4).
7. **Step 7:** Implement `silence-active` flag for Passage canonical-silence enforcement (§ 4.4).
8. **Step 8:** Acceptance test: full combat encounter with all five layers active; verify mix balance, sidechain behavior, polyphony cap.

Asset-population (Cluster A skill SFX + Cluster C ambient + Cluster B music) is elrond's curation lane; populated assets are dropped into the new layer-aware folder structure; drax wiring picks them up automatically.

### 9.6 Out of scope for engineering notes

Not addressed here (other dispatches own):
- Specific Howler.js version dependencies / mobile-platform browser-matrix testing — drax future-dispatch
- Acquisition spend decisions for Cluster A/B/C packs — elrond curation + Matt L3
- Voice-synthesis integration — § 8 forward-flag; future voice-dispatch
- Per-season music acquisition workflow — § 7 Matt-decision space
- Audio-asset attribution-pipeline schema — elrond curation territory

---

## 10. Open questions for Matt

Five decisions land at Matt's L3 surface; this canon presents the recommendation but does NOT pre-commit. Routing each to the appropriate decision moment:

### Q-MATT-1 — Sonic register cluster lock (§ 2)

**Recommendation:** HYBRID — Cluster A skill SFX + Cluster C ambient + Cluster B music + Cluster D UI. Endorses + amends legolas-4's pragmatic recommendation.

**Decision moment:** at decisions-log entry drafting (knight-rider drafts; Matt confirms). Pre-canonical-lock here; needs decisions-log canonicalization at next governance pass.

### Q-MATT-2 — Music gap path for D10 002011-015 (§ 7)

**Recommendation:** Option B (Suno Pro per-season against canonical prompt anchor) primary; Option A (reuse 001001-005) immediate-unblock fallback; Option D (Bit By Bit Sound $77.60) at pre-demo-ship gate.

**Decision moment:** immediate (002011-015 are currently silent in playtest). Matt picks; engineering-implementation routes through drax (no new code; existing file-loading handles either path).

### Q-MATT-3 — Bit By Bit Sound $77.60 acquisition spend authorization (§ 7)

**Recommendation:** authorize at pre-demo-ship gate (not now). Contingent on Q-MATT-2 selecting Option D.

**Decision moment:** demo-ship-readiness review (months out; not now).

### Q-MATT-4 — Canonical Suno music prompt anchor (§ 7)

**Recommendation:** lock the prompt language in § 7.3 as the canonical anchor (analogous to `style-register.md`'s LLM image-generation prompt anchor). Every Suno-generated season-track uses this prompt + per-season flavor-text injection.

**Decision moment:** immediate (drives Q-MATT-2 Option B execution).

### Q-MATT-5 — Holy element register-attention zone path (§ 3.2)

**Recommendation:** Path 1 (composite construction — WS3 Light + bell-chime foley + pitch-shift to land at retro-band) for VS2a + VS2b. Path 2 (register-mismatch acceptance) only if Path 1 composite produces playtest-flagged audio-mismatch. Path 3 (commission retro-register holy pack) deferred to Phase-1+.

**Decision moment:** at elrond curation pass (auto-fires on this canon completion). Matt-flag only if Path 1 composite cost is non-trivial; otherwise elrond proceeds against Path 1 by default.

---

## 11. Handoffs

### 11.1 → elrond — audio-pack curation (auto-fires on this completion)

Per dispatch `agentic_orchestration/dispatches/2026-05-17-elrond-audio-pack-curation-queued.md`. Elrond consumes:

- **§ 2 cluster lock** as the curation register-filter criterion. Cluster A packs become recommendation-eligible; Cluster B/C selected per layer; Cluster D as UI/foley underlayer; other clusters excluded by register-fit.
- **§ 3 element signature table** as the per-pack scoring rubric. Each candidate pack scored against fit for canonical-7 substrate × archetype-group sonic identity.
- **§ 4 five-layer architecture** as the sonic-slot enumeration target. Curation produces per-layer pack recommendations (Layer 1 substrate × Layer 4 atmospheric × Layer 5 music × Layer 3 foley underlayers).
- **§ 5 loudness target** as the per-pack normalization target. Acquired packs may need master-bus loudness alignment at integration (drax territory; elrond flags pack mastered-loudness in curation metadata).
- **§ 6 player vs enemy decision** as confirmation that same-file curation suffices (no paired-file acquisition).
- **§ 7 music path** as the curation directive for Layer 5 (Suno workflow vs Bit By Bit Sound; elrond doesn't curate AI-generated, but if Path D, elrond curates the Bit By Bit Sound subset).

Elrond produces a sonic curation manifest analogous to the VFX 4-layer manifest at `agentic_orchestration/research/curated/audio-layered-curation-vs2a-2026-05-17.jsonl` (or comparable naming). Schema extends from VFX schema with sonic-cluster + LUFS-mastered + license-class fields.

### 11.2 → drax — engine-side integration (future-dispatch)

Drax future-wiring dispatch consumes:

- **§ 4 layered architecture** as the audio-bus implementation target
- **§ 5 loudness + sidechain rules** as the bus-routing spec
- **§ 6 player vs enemy emitter** as the `playAbilityCast` signature extension
- **§ 9 engineering interaction notes** as the integration sequence + folder schema + telemetry instrumentation

Drax's future-dispatch is NOT this canon's commission — it fires when elrond curation lands AND Matt-Q1 (audio register canonicalization) confirms.

### 11.3 → matt — decisions (Q1 register + Q6 music + voice future-dispatch)

Matt receives:

- **§ 2 cluster lock recommendation** for canonical confirmation
- **§ 7 music gap path recommendation** for D10 002011-015 immediate decision
- **§ 8 voice-over forward-flag** for awareness (no decision required this canon)
- **§ 10 open questions** as the consolidated Matt-decision surface

### 11.4 → star-lord — telemetry instrumentation (downstream of drax wiring)

Star-lord consumes § 9.4 telemetry recommendations. Wires into existing telemetry pipeline at drax's audio-wiring landing. Not this canon's commission; flagged for downstream awareness.

### 11.5 → knight-rider — decisions-log entry drafting

Knight-rider drafts decisions-log entries for:
- Sonic register cluster lock (§ 2; Q-MATT-1)
- Music register canonical Suno prompt anchor (§ 7.4; Q-MATT-4)

Per ADR-002 cross-seam decisions-log discipline (analog to the visual register-fence rule's decisions-log canonicalization).

---

## 12. Cross-references

### 12.1 Binding companion docs (canon-level references)

- `canonical/story/style-register.md` — visual register HYBRID a3 lock; sonic register matches with the hybrid logic at audio layer
- `canonical/story/audio-scoping-framework-2026-05-16.md` — seven-sub-axis decomposition; this canon resolves Cluster I (sub-axes 1+2 combat-feel) and Cluster II (sub-axis 3 ambient) at register layer
- `canonical/story/audio-strategy-phase0.md` — Phase-0 silent-ship lock; this canon supplements with Phase-1+ register inheritance
- `canonical/story/vs2a-vfx-scene-needs.md` — register-fence-per-UI-surface authoring rule (parallel for SFX-tier-fence); per-encounter VFX presence (Section 1.1 mirror for SFX presence per encounter type)
- `agentic_orchestration/research/curated/vfx-layered-architecture-vs2a-2026-05-17.md` — elrond's 4-layer VFX architecture; this canon's 5-layer SFX architecture mirrors with music as audio-only addition
- `agentic_orchestration/research/catalogue/audio-vendors-2026-05-17/coverage-matrix.md` — legolas-4 empirical anchor; this canon's element signature table consumes coverage-matrix § 1
- `reincarnated-demo/src/audio/audio.ts` — current Tier-1 procedural + Tier-2 file-mapping; § 9 engineering notes consume

### 12.2 Cross-reference companions (non-binding, contextual)

- `canonical/story/mobile-feel-target-doe-2026-05-17.md` — DoE ultra-fast pace informs § 5 polyphony cap + anti-fatigue rules
- `canonical/story/mobile-pc-pixel-sizing-ratios-2026-05-17.md` — register-fence-per-surface precedent (visual analog of § 4.3 UI-bus-not-layer decision)
- `canonical/story/spirit-guide-voice.md` — voice-register text-layer lock; § 8 forward-flag builds against
- `canonical/story/passage-moment-ritual.md` — canonical-silence requirement enforced at § 4.4
- `canonical/story/court-of-forms.md` — Court ritual audio register (Layer 7 ritual stinger application)
- `canonical/29-design-overview.md` — engine-1 outputs + seasonal-journey anchor; sonic identity serves the cosmological frame
- `canonical/story/drift-audit.md` Pattern P6 — audio-as-atomic-deferral pattern; this canon prevents Phase-1 recurrence by resolving register-level ambiguity ahead of commission

### 12.3 Downstream dispatches consuming this canon

- elrond audio-pack curation (auto-fired post-canon)
- drax engine-side audio integration (future-dispatch)
- voice-over commissioning (future-dispatch, Phase-1 mid-cycle)
- per-season music register-coherence (Phase-1+; if Matt selects Option B Suno path, this canon's prompt anchor is the inheritance)

---

## Maintenance protocol

This canon is canonical as of authoring 2026-05-17, pending Matt L3 confirmation on Q-MATT-1 (register cluster lock) and Q-MATT-4 (Suno prompt anchor) per § 10.

When future register-relevant decisions arise (cluster pivot; per-season SFX variance; voice-over commissioning; emitter-discipline amendments):
- Append sections; preserve canonical-lock history; reference the original lock
- If pivot lands, mark prior section superseded but preserve for archaeology
- Per AGENTS.md score-don't-filter principle, catalogue serves pivot without re-crawl

When new canonical design docs touch audio:
- Reference this canon
- Defer to this canon on register matters
- Cross-reference for register-coherence checks at Gate 1

When drax future-wiring-dispatch lands:
- This canon's § 4 + § 5 + § 6 + § 9 become the wiring spec
- Decisions-log entry for cluster lock (§ 2) becomes the formal canonicalization; this canon's status updates to "canonical-via-decisions-log"

— gandalf, 2026-05-17

---

*Audio register canon authored per dispatch `2026-05-17-gandalf-audio-register-sonic-identity-canon-queued.md`. Auto-fired after gandalf D11 post-mortem + legolas-4 audio crawl completion. Five-layer SFX architecture; eight-element signature table; -14 LUFS integrated master target; HYBRID cluster lock matching visual register's HYBRID a3. The work that this canon serves: every cast, every impact, every season, every ritual — landing in the same sonic geography the player learned at first encounter. Register-fence-per-surface, hybrid-not-mixed-within-frame. The same architectural shape as the visual register, executed at the audio layer.*
