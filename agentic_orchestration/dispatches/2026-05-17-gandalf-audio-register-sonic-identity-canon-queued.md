# 2026-05-17 — gandalf — Audio register / sonic identity canon (QUEUED — auto-fires after gandalf D11 post-mortem + legolas audio crawl)

**Authority:** Matt L3 2026-05-17 late evening — "It is time to fire a Legolas and/or Gandalf/Elrond audio pack research project." This dispatch authors the design-side canon (the WHY + the aesthetic-register criterion); legolas crawls the catalogue (parallel); elrond curates (auto-fires when both inputs land).
**Type:** Pattern B (short) — design-steward canon authoring; ~0.5-1 day.
**Predecessors (both gate auto-fire):**
- Gandalf D11 post-mortem completion (`agentic_orchestration/dispatches/2026-05-17-gandalf-d11-postmortem-option-b-veto-authority.md`)
- Legolas audio vendor catalogue crawl (`agentic_orchestration/dispatches/2026-05-17-legolas-audio-vendor-catalogue-crawl.md`)
**Status:** 🟡 **QUEUED — DO NOT EXECUTE until BOTH predecessors ship completion records.** Knight-rider activates when both land.

---

## Why this matters

Visual register is canonical (HYBRID a3 per `vs2a-vfx-scene-needs.md`); audio register is not yet. Without a canonical audio register, elrond's curation has no decision criterion for "fits Reincarnated" vs "off-genre"; drax integration risks register drift; future audio commissions lack a yardstick.

Your D11 advisory + DoE doc cascade + Phase-1 P1 substrate work has built a body of canonical design language. This dispatch extends it to audio — what Reincarnated SOUNDS like, in the same register-fence-per-surface discipline that gandalf v1.10 established for visuals.

---

## Required reading (when activated)

1. **Legolas audio crawl** — `agentic_orchestration/research/catalogue/audio-vendors-2026-05-17/summary.md` + `inventory.jsonl` (your empirical anchor for what's actually available)
2. **Your VFX scene-needs spec** — `canonical/story/vs2a-vfx-scene-needs.md` (visual register; audio register should mirror similar logic + complement, not duplicate)
3. **Your DoE feel-target doc** — `canonical/story/mobile-feel-target-doe-2026-05-17.md` (mobile combat pace; UI sparseness; positioning-as-skill-ceiling — informs audio non-fatigue + signal-vs-noise)
4. **Your mobile sizing canon** — `canonical/story/mobile-pc-pixel-sizing-ratios-2026-05-17.md` (the register-fence-per-UI-surface rule; audio has parallel surfaces — combat-tier vs UI-tier vs ambient-tier)
5. **Elrond 4-layer VFX architecture** — `agentic_orchestration/research/curated/vfx-layered-architecture-vs2a-2026-05-17.md` (layered visual model; audio likely needs analogous layered model — substrate / class-archetype / physical / atmospheric)
6. **Demo audio.ts** — `reincarnated-demo/src/audio/audio.ts` (current Tier 1 procedural baseline; what register the procedural tones approximate)
7. **Geometry vocabulary** — `reincarnated-engine/src/reincarnated/generation/geometry_derivation.py` (24-type list; informs SFX naming + slot count)
8. **Element vocabulary** — canonical-7 substrates + physical (8 elemental sonic identities to author)

---

## Scope — eight design questions

### Q1 — Sonic register cluster

Reincarnated's visual register is HYBRID a3 (HD-painterly-pixel). What's the sonic equivalent? Options:
- **Cinematic-HD** — full orchestral / Boom Library production-quality; matches AAA ARPGs (D4, PoE2)
- **Pixel-game-retro** — chiptune / 8-bit / 16-bit register; matches Stardew / Hyper Light Drifter
- **Hybrid retro-HD** — chiptune base layer with HD spell effects on top; matches some indie ARPGs (Children of Morta, Wizard of Legend)
- **Dark-synth / electronic** — Hotline Miami / Soulstice register; doesn't fit ARPG but worth considering
- **Orchestral-fantasy-folk** — strings + woodwinds + ambient drones; matches Diablo Immortal mobile pivot

Recommend one. Cite genre-anchor games + sonic exemplars. Note whether visual register HYBRID a3 forces audio to match-or-contrast.

### Q2 — Element-to-sonic-signature mapping

For each canonical-7 substrate + physical, establish a signature audio mapping. Format suggestion (per element):
- **Base timbre**: e.g., fire = crackling + roar; water = trickle + splash; earth = stone-grind + deep impact; wind = whoosh + howl; lightning = electric-zap + thunderclap; holy = bell-chime + choral; shadow = whispers + low-drone; physical = clang + flesh-thud
- **Pitch range**: e.g., fire low + sharp transient; lightning high + sharp transient; water mid + sustained
- **Reverb / spatial**: e.g., holy/shadow longer reverb; physical/fire dry close
- **Spectral envelope**: bright vs muffled

Output: 8-row table (one per element) with timbre + pitch + reverb + spectral envelope + reference exemplar.

### Q3 — Layered audio architecture (mirror elrond's 4-layer VFX)

Elrond's curation extension proposed 4-layer VFX architecture (substrate / class-archetype / physical / atmospheric). Recommend whether audio mirrors this or uses a different layering:
- Substrate-tier (element-driven base SFX) — likely yes
- Class-archetype tier (e.g., chromatic_mage has distinct sonic signature vs physical) — yes/no/maybe
- UI-tier (event-driven; non-combat) — distinct surface
- Ambient-tier (room-tone loops; biome-driven) — likely yes
- Music-tier (season-driven; longer-form) — yes
- Combat-overlay-tier (hit-on-target overlays, death stingers) — sub-layer of substrate or distinct?

Recommend final layered model. Document interaction rules (e.g., "ambient ducks under combat" / "music ducks under spirit-guide voice").

### Q4 — Loudness + signal-vs-noise discipline

Mobile combat fires many simultaneous SFX (5+ enemies, AOE windups, hits, dodges, kills). Without loudness discipline → fatigue + signal loss. Recommend:
- Per-tier loudness targets (e.g., -6 LUFS combat-critical; -12 LUFS ambient; -3 LUFS music — illustrative)
- Compression / sidechain rules (combat SFX ducks ambient; spirit-guide voice ducks both)
- Frequency-band stratification (low = footsteps + earth; mid = swords + voices; high = lightning + UI)
- Polyphony cap (e.g., max 6 simultaneous SFX channels; oldest dropped under load)

### Q5 — Player-emitter vs enemy-emitter distinction

In current `audio.ts`, `playAbilityCast(geometry, element)` doesn't distinguish player vs enemy emitter. Should:
- Player skills sound distinctly different (e.g., brighter, closer-mixed, higher loudness)?
- Enemy skills sound distinctly different (e.g., spatialized, lower loudness, more reverb)?
- Both use the same SFX but spatial panning + loudness differs?

This affects elrond's curation (single SFX file per slot vs paired player/enemy variants) + drax integration (audio call signature).

### Q6 — Music gap for D10 seasons (immediate decision)

D10-curated 002011-015 have NO music (silent fallback per console log). Pragmatic options:
- (a) Reuse 001001-005 tracks as placeholders (fastest; degrades nothing)
- (b) AI-generate per-season music (Suno / Udio / similar; ~$0-20 per track)
- (c) Commission per-season tracks (slow + expensive)
- (d) Skip music until production (silent playtest is acceptable)
- (e) Procedural ambient via tone-stacks in audio.ts (no files; programmatic)

Recommend. Matt-decision flag if you can't choose unilaterally.

### Q7 — Voice-over / spirit-guide narration (forward-flag)

Voice-over is out-of-scope this dispatch BUT spirit-guide is a major character + voice. Forward-flag:
- Register (genre-canonical narrator vs character voice vs procedural text-to-speech for prototyping)
- Acquisition path (commissioned VO ~$100-500 per session; AI-TTS ~$10-50; placeholder text-only acceptable for now?)
- Integration site (separate audio bus; ducks music + ambient; per-language scaling)

Author 1-2 paragraphs scoping out the question; defer to future dispatch.

### Q8 — Engineering interaction (informational)

How does audio register interact with engine code?
- `audio.ts` currently has Tier 2 file path convention; what's the recommended naming/folder schema given the layered model from Q3? (e.g., `/audio/sfx/{layer}/{element}_{geometry}.ogg` for substrate-tier)
- Star-lord telemetry implication: any audio-event telemetry needed (e.g., "music silent fallback fired" → metric)?
- Drax integration concerns: Pixi's Howler.js integration; mobile audio context constraints (user-gesture required); audio-bus mixing

Author as note for drax / star-lord at integration time; don't pre-empt.

---

## Output — canonical audio register doc

Author at: `canonical/story/audio-register-canon-2026-05-17.md`

Structure (mirror your VFX scene-needs spec where applicable):
1. **Executive summary** (1-2 paragraphs; the sonic identity headline)
2. **Sonic register cluster** (Q1 decision + cited exemplars)
3. **Element signature table** (Q2; 8 elements × timbre/pitch/reverb/envelope/exemplar)
4. **Layered architecture** (Q3; mirror or diverge from elrond's 4-layer VFX)
5. **Loudness + signal discipline** (Q4; per-tier LUFS + sidechain + polyphony rules)
6. **Player vs enemy emitter discipline** (Q5; SFX-file convention + drax integration implication)
7. **Music gap pragmatic recommendation** (Q6; specific path; Matt-flag if needed)
8. **Voice-over forward-flag** (Q7; scoped paragraph for future dispatch)
9. **Engineering interaction notes** (Q8; for drax + star-lord)
10. **Open questions for Matt** (anything you can't decide unilaterally)
11. **Handoffs**: → elrond (curation criterion + 4-layer audio model; auto-fires when this lands + legolas lands); → drax (integration architecture for future wiring dispatch); → matt (decisions)
12. **Cross-references** (VFX scene-needs / DoE feel-target / sizing canon / elrond 4-layer VFX / audio.ts file)

Target: 600-1200 lines (smaller than D11 advisory; tighter than VFX scene-needs; this is canon-authoring, not greenfield design).

---

## Out of scope (DO NOT)

- ❌ DO NOT author engine-side audio code (drax's lane post-curation)
- ❌ DO NOT modify legolas crawl output or pre-empt elrond curation
- ❌ DO NOT extend to voice-over scope (Q7 forward-flag only; future dispatch)
- ❌ DO NOT make acquisition decisions — Matt L3 required for spend
- ❌ DO NOT pre-empt D11.1 outcomes (post-mortem authority is separate from this dispatch)
- ❌ DO NOT skip Sub-Qs even if some feel small (Q5 player/enemy emitter affects drax architecture; can't be deferred)

---

## Acceptance criteria (when activated)

- [ ] Canonical doc authored at `canonical/story/audio-register-canon-2026-05-17.md`
- [ ] All 12 sections per structure
- [ ] Sonic register cluster recommendation (Q1) with genre-anchor exemplars
- [ ] Element signature table (Q2) — 8 rows complete
- [ ] Layered architecture (Q3) — final model documented
- [ ] Loudness + signal discipline (Q4) — concrete LUFS / sidechain / polyphony rules
- [ ] Player vs enemy emitter discipline (Q5)
- [ ] Music gap recommendation (Q6) with Matt-flag if needed
- [ ] Voice-over forward-flag (Q7) — 1-2 paragraphs
- [ ] Engineering interaction notes (Q8) for drax + star-lord
- [ ] HANDOFF → elrond (audio curation auto-fires on this completion)
- [ ] PRE-SIGNAL § 14.1.1 before hive-log append
- [ ] Hive-log STATE entry

---

## Coordination

- **AUTO-FIRE TRIGGER:** BOTH (a) gandalf D11 post-mortem completion AND (b) legolas audio crawl completion. Knight-rider monitors and spawns gandalf agent when both land.
- **Parallel-safe with**: D11.1 sprint chain (separate concern); elrond CraftPix curation (shipped); drax/rocket hotfixes (shipped or in flight)
- **PRE-SIGNAL § 14.1.1** before hive-log appends
- **No tag** (canon authoring; not code)

---

*Dispatched (queued) 2026-05-17 by knight-rider per Matt L3 audio research authorization. ~0.5-1 day when activated. Append completion record when done.*

---

## Completion record — 2026-05-17 late-evening+3 — gandalf

**Status:** ✅ **SHIPPED.** Auto-fire trigger fired: both predecessors landed (gandalf D11 post-mortem completion + legolas-4 audio crawl completion). Executed per dispatch directive.

**Deliverable:** `canonical/story/audio-register-canon-2026-05-17.md` — 716 lines (within 600-1200 target band). All 12 sections per dispatch structure; all 8 sub-questions answered; HYBRID register lock + 5-layer SFX architecture + 8-element signature table + Matt L3 decision surface consolidated.

**Acceptance criteria — all checked:**
- [x] Canonical doc authored at `canonical/story/audio-register-canon-2026-05-17.md`
- [x] All 12 sections per structure
- [x] Sonic register cluster lock (Q1) with genre-anchor exemplars — HYBRID Cluster A skill SFX + Cluster C ambient + Cluster B music + Cluster D UI; endorses + amends legolas-4 split
- [x] Element signature table (Q2) — 8 rows complete; holy flagged as register-attention zone per critical insight directive
- [x] Layered architecture (Q3) — 5-layer SFX model documented (mirrors elrond's 4-layer VFX with music as audio-only addition)
- [x] Loudness + signal discipline (Q4) — per-layer LUFS targets, frequency-band stratification, compression / sidechain rules, polyphony cap 8 channels with oldest-drop, anti-fatigue rules
- [x] Player vs enemy emitter discipline (Q5) — same-file + per-emitter mix-bus locked; per-encounter spatial-panning rules
- [x] Music gap recommendation (Q6) — Option B (Suno per-season against canonical retro-JRPG prompt anchor) primary; Option A immediate-unblock fallback; Option D demo-ship-ready path; Matt L3 surface for path selection + Suno prompt anchor lock + $77.60 spend authorization
- [x] Voice-over forward-flag (Q7) — Cluster B-adjacent intimate close-mic register locked; acquisition triage table; integration site spec'd; future-dispatch scope
- [x] Engineering interaction notes (Q8) — folder schema, mobile constraints, audio-bus mixing GainNode tree, star-lord telemetry metrics (3+1), 8-step drax integration sequence
- [x] HANDOFF → elrond — audio curation auto-fires on this completion (per `2026-05-17-elrond-audio-pack-curation-queued.md`)
- [x] PRE-SIGNAL § 14.1.1 — executed (`git fetch origin`; verified no remote-ahead hive-log commits; no race condition)
- [x] Hive-log STATE entry — appended to `agentic_orchestration/hive-mind/phase-1-p1-log.md` at `[2026-05-17 late-evening+3]`

**Critical insight per dispatch — addressed:** Holy element has NO explicit retro-register pack per legolas-4 § 1. Flagged as register-attention zone in canon § 3.2; composite construction path (WS3 Light + bell-chime foley + pitch-shift) recommended for VS2a + VS2b as Path 1. Path 2 (register-mismatch acceptance) and Path 3 (Phase-1+ commission) documented as fallbacks.

**Critical recommendation per dispatch — addressed:** Music register canonicalized as Cluster B (mid-fi orchestral-synth via Suno against locked prompt) per § 7.3 — analog to style-register.md's LLM image-generation prompt anchor. Anchor preserves per-season register coherence; Matt's workflow continues at zero project-corpus cost.

**Handoff packet:**

- **→ elrond:** AUTO-FIRES NOW per dispatch chain. Audio-pack curation consumes § 2 cluster lock + § 3 element signature table + § 4 5-layer architecture + § 5 LUFS targets + § 6 same-file decision + § 7 music path.
- **→ matt:** 5 Matt L3 decisions consolidated at § 10. Highest-priority: Q-MATT-2 (music gap for currently-silent 002011-015) + Q-MATT-1 (register lock canonicalization) + Q-MATT-4 (Suno prompt anchor).
- **→ drax:** Future-wiring dispatch consumes § 4 + § 5 + § 6 + § 9. NOT this canon's commission; fires when elrond curation + Matt Q1 lock land.
- **→ star-lord:** § 9.4 telemetry instrumentation downstream of drax wiring. Awareness flag only.
- **→ knight-rider:** Decisions-log entry drafting for cluster lock + Suno prompt anchor per ADR-002.

**Tag:** None (canon-authoring per dispatch directive; not code).

**Parallel-safety:** Parallel-safe with all in-flight work — gamora D11.1 math note (shipped) + jack-ryan D11.1 Gate-1 advisory (shipped) + rocket persistence diagnostic (in flight) + rocket D11 demo-sync hotfix (shipped). Orthogonal concerns. No engine / demo / decisions-log writes.

**Total effort:** ~0.5 day (within ~0.5-1 day dispatch target).

— gandalf, 2026-05-17 late-evening+3
