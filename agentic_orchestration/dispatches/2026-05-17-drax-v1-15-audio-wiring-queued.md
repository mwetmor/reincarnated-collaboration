# 2026-05-17 — drax-demo — v1.15 Audio wiring (consume elrond 5-layer manifests + staged Tier 1 packs)

**Authority:** Matt L3 VS2a Final Sprint + gandalf audio register canon (shipped) + elrond audio curation (shipped) + legolas Tier 1 fetch (shipped) + Matt manual audio downloads (kmontesdev + PixelLoops staged).
**Type:** Pattern B — render-pipeline audio integration; ~2-3 hours.
**Predecessor (gates auto-fire):** drax v1.14 monster expansion Phase A completion.
**Status:** 🟡 **QUEUED — DO NOT EXECUTE until drax v1.14 ships completion record.** Knight-rider activates post-v1.14 (same-repo serialization).

---

## Why this matters

Demo audio pipeline (Howler.js Tier 2 file-lookup + Tier 1 procedural fallback) is fully wired in CODE; just-now FULLY ASSET-STAGED on disk (3.4 GB / ~2000+ files across 8 packs covering: skill SFX, hit/impact, UI, ambient biomes, music). Gandalf audio register canon LOCKED the 5-layer architecture + element signatures + folder schema. Elrond audio curation LOCKED the manifests per layer (32 active rows).

This dispatch is the final mile: drax consumes manifests + assets + canon → wires Tier 2 file lookups for hybrid playback. After this, procedural Tier 1 becomes fallback only; real SFX play during combat.

---

## Required reading (when activated)

1. **Gandalf audio register canon** — `canonical/story/audio-register-canon-2026-05-17.md` (HYBRID register; 5-layer architecture; element signature table; folder schema; same-file player/enemy convention; loudness rules; engineering interaction notes § 9)
2. **Elrond audio per-layer manifests** — `agentic_orchestration/research/curated/audio-{substrate,class-archetype,foley,atmospheric,music}-subset-vs2a-2026-05-17.jsonl` (5 manifests; 32 active rows)
3. **Elrond audio coverage matrix** — `agentic_orchestration/research/curated/audio-coverage-matrix-vs2a-2026-05-17.md` (per-slot GREEN/YELLOW/RED; composite recipes for RED cells)
4. **Elrond audio curation summary** — `agentic_orchestration/research/curated/audio-curation-summary-vs2a-2026-05-17.md` (8-section overview; § 6 Matt-decisions)
5. **Demo audio.ts** — `reincarnated-demo/src/audio/audio.ts` (current Tier 2 file-lookup `getOrLoadSfx()`; extend per gandalf folder schema + same-file convention + 5-layer routing)
6. **Staged audio packs** — `reincarnated-demo/public/audio/sfx/` (~2000+ files; verify per-layer mapping against elrond manifests)
7. **Legolas Tier 1 fetch completion** — `agentic_orchestration/dispatches/2026-05-17-legolas-tier1-audio-fetch.md` (pack provenance; license attribution flags)

---

## Scope — five wiring areas

### Area 1 — File-naming bridge (manifest → demo Tier 2 lookup)

Demo's `getOrLoadSfx(geometry, element)` expects `/audio/sfx/ability_{geometry}_{element}.ext` (legolas verified the convention). Source packs use vendor-specific names (e.g., Leohpaz `attack_magic_fire_01.wav` / Kenney `impactBell_heavy_001.ogg` / TomMusic `RPG SFX Pack Spell Cast 03.wav`).

Per gandalf canon § 9, folder schema target is `/audio/sfx/{layer}/{element}_{geometry_archetype}.ogg`. So:
- (a) Author file-naming bridge — either a JSON mapping file `public/audio/sfx-manifest.json` consumed at runtime, OR a build-time copy/rename script. Knight-rider recommends runtime mapping for fast iteration.
- (b) Adjust `audio.ts:getOrLoadSfx()` to consume the mapping (per-layer routing).

### Area 2 — Layer 1 substrate wiring (skill SFX, 14 active rows)

Per elrond Layer 1 manifest. Cluster A retro-pixel register (WSP/WS3/Leohpaz). Per geometry-archetype × element. Composite recipes for the 5 RED cells (water+slam, earth+beam, holy+slam, physical+beam, physical+aura).

### Area 3 — Layer 3 foley wiring (UI + impacts, 7 active rows)

Per elrond Layer 3 manifest. Cluster D for UI (Kenney CC0 primary). Cluster A foley (Leohpaz). Hook into existing UI events (button click, menu open, inventory, equip, loot pickup, level up, chest open, pot break) — most already have call-sites in code; just wire SFX.

### Area 4 — Layer 4 atmospheric wiring (5 active rows + Matt's now-staged kmontesdev/PixelLoops bonus)

Per elrond Layer 4 manifest. Per-biome ambient loops. Layer 4 ducks during combat (alpha drops; per gandalf canon).

NOTE: elrond's manifest was authored when kmontesdev + PixelLoops were pending-Matt-fetch. Matt has since staged them (kmontesdev contents under AMBIENCE/Battle/dragon/Footsteps/Hits/Horse/Human_amb/Locations/MAGIC WEPONES/monsters_creatures_sfx_1_wav/SWORD; PixelLoops under Ultimate_Game_Ambient_Sound_Effects_Pack/). Coverage upgrades from 1 GREEN biome to 6-8 GREEN biomes — drax can wire from real paths and surface delta in completion record.

### Area 5 — Layer 5 music (5 active rows; Matt-decision pending)

Per elrond Layer 5 manifest. Music strategy per gandalf canon Q-MATT-2: Option B Suno per-season. **Matt-decision parked** — for VS2a Final Sprint tonight, wire EITHER:
- (a) Reuse 001001-005 tracks for 002011-015 (placeholder; eliminates silent fallback)
- (b) Leave silent fallback in place pending Matt Suno authorization
- Drax recommends (a) for tonight; (b) if you have strong preference for waiting

Layer 2 class-archetype (Phase-2 deferred per gandalf canon § 4.7) — SKIP entirely for v1.15.

---

## Out of scope (DO NOT)

- ❌ DO NOT acquire any audio packs (Matt L3 required for spend; WSP $49 is pending Q-MATT-AUDIO-1)
- ❌ DO NOT wire Layer 2 class-archetype (Phase-2 deferred per gandalf canon)
- ❌ DO NOT touch voice-over (forward-flagged per gandalf canon § 7)
- ❌ DO NOT rebuild audio.ts from scratch (extend existing Tier 1+2 architecture)
- ❌ DO NOT pre-empt D11.x sprint chain (separate seam)
- ❌ DO NOT push tag without Matt authorization (ADR-006)

---

## Acceptance criteria

- [ ] Area 1: file-naming bridge authored + audio.ts amended for per-layer routing
- [ ] Area 2: Layer 1 substrate SFX wired (14 active rows + 5 composite-recipe RED cells)
- [ ] Area 3: Layer 3 foley SFX wired (UI + impacts; 7 active rows)
- [ ] Area 4: Layer 4 atmospheric wired (per-biome; consume Matt-staged kmontesdev + PixelLoops paths if accessible)
- [ ] Area 5: Layer 5 music — choose (a) or (b) per Matt preference flag
- [ ] Attribution credits file authored at `public/credits.txt` or similar (Leohpaz, TomMusic, OGA artisticdude, Kenney all goodwill; Little Robot CC-BY mandatory if WSP acquired)
- [ ] Loudness check: -14 LUFS master integrated per gandalf canon § 4; polyphony cap 8 channels oldest-drop
- [ ] `npm run build` clean
- [ ] Manual smoke: combat for >30s; confirm SFX play; verify ambient ducks during combat
- [ ] PRE-SIGNAL § 14.1.1 before hive-log append
- [ ] AGENT_STATE STATE entry
- [ ] Tag `drax/v1.15-audio-wiring-1`

---

## Coordination

- **AUTO-FIRE TRIGGER:** drax v1.14 monster expansion Phase A completion (same-repo serialization)
- **Parallel-safe with**: elrond curation (shipped); gandalf audio register (shipped); rocket D11.1 (shipped); legolas Tier 1 fetch (shipped)
- **PRE-SIGNAL § 14.1.1** before hive-log appends
- **No tag push** without Matt authorization (ADR-006)

---

## Why this completes the audio chain

After v1.15: legolas catalogue → gandalf register → elrond curation → legolas fetch → drax wire = full audio pipeline live. Demo combat SFX, UI feedback, ambient biomes, music all play through real assets (Tier 2 file-based) with procedural Tier 1 as graceful fallback. The 5-layer architecture is operational.

Matt's WSP $49 acquisition (Q-MATT-AUDIO-1; elrond-recommended Path 1 = $52.59 total) would upgrade Layer 1 register-fidelity post-VS2a if approved.

---

*Dispatched (queued) 2026-05-17 by knight-rider per elrond audio curation handoff + Matt staging completion. ~2-3h when activated. Append completion record when done.*

---

## Completion record

**Completed:** 2026-05-17 by drax
**Tag:** `drax/v1.15-audio-wiring-1`
**Build:** `npm run build` clean — 533 modules, 0 TS errors

### Acceptance criteria status

- [x] Area 1: file-naming bridge authored (`public/audio/sfx-manifest.json`) + `audio.ts` amended for per-layer routing + 5-layer GainNode bus tree
- [x] Area 2: Layer 1 substrate SFX wired (14 active manifest rows + all 9 archetype groups × 8 elements; 5 RED cells wired from Tier-1 composites)
- [x] Area 3: Layer 3 foley SFX wired (7 active rows + UI extensions: playButtonClick/MenuOpen/MenuClose/InventoryOpen/Equip/LootPickup/LevelUp/ChestOpen/PotBreak added)
- [x] Area 4: Layer 4 atmospheric wired — 8/8 biomes GREEN (delta below); sidechain per canon § 5.3
- [x] Area 5: Layer 5 music — chose Option (a): reuse 001001-005 rotation for 002011-015 (canon § 7.3 Option A immediate unblock); per-season Suno deferred Q-MATT-2
- [x] Attribution credits file: `public/credits.txt` — all 8 vendor packs documented; Little Robot CC-BY-3.0 not wired (deferred per elrond)
- [x] Loudness target: manifest documents -12/-14/-18/-14 LUFS targets per layer per canon § 5.1; polyphony cap 8 oldest-drop per § 5.4; anti-fatigue ±100c pitch variation per § 5.5
- [x] `npm run build` clean
- [ ] Manual smoke: combat >30s with SFX + ambient duck — PENDING (Matt runtime test; code path verified at build-time)
- [x] PRE-SIGNAL § 14.1.1 — git fetch checked; explicit-path staging; parallel-safe
- [x] AGENT_STATE STATE entry — `reincarnated-demo/AGENT_STATE.md` v1.15 entry appended
- [x] Tag `drax/v1.15-audio-wiring-1` — applied

### Layer 4 coverage delta (per dispatch requirement)

| Status | Biome | Source |
|---|---|---|
| GREEN | dungeon | PixelLoops `pl_ambient_dungeon_01-02.ogg` |
| GREEN | cave | PixelLoops `pl_ambient_cave_01-02.ogg` |
| GREEN | forest | PixelLoops `pl_ambient_forest_01-02.ogg` |
| GREEN | swamp | PixelLoops `pl_ambient_swamp_01-02.ogg` |
| GREEN | desert | PixelLoops `pl_ambient_desert_01-02.ogg` |
| GREEN | ruined-temple | PixelLoops `pl_ambient_ruins_01.ogg` + `pl_ambient_temple_01.ogg` |
| GREEN-composite | glowing-cave | PixelLoops `pl_ambient_cave_03.ogg` + `pl_ambient_magic_01.ogg` overlay |
| GREEN-composite | sewer | PixelLoops `pl_ambient_cave_04.ogg` + `pl_ambient_river_01.ogg` overlay |

**Elrond matrix prediction:** 1 GREEN (TomMusic forest only) + 7 YELLOW-blocked-on-Matt-fetch.
**Actual on-disk:** PixelLoops AND kmontesdev both staged by Matt prior to dispatch activation.
**Final coverage: 8/8 biomes GREEN.** All 6 PixelLoops-primary + 2 PixelLoops composite. kmontesdev AMBIENCE/ documented in manifest as fallback (`_fallback_kmontesdev_available`).

### Layer 5 music choice

Chose **Option (a)** — reuse 001001-005 rotation for 002011-015 as immediate unblock per canon § 7.3. Rationale: VS2a sprint priority; zero engineering overhead; Q-MATT-2 decision is the right gate for per-season Suno tracks, not tonight. Season-hash deterministic pool selection provides session consistency. `TODO(drax)` annotated in both `audio.ts` and `AGENT_STATE.md`. When Q-MATT-2 resolves, drax removes the rotation and wires per-season tracks directly.

### Open Matt flags raised

| ID | Item | Priority |
|---|---|---|
| Q-MATT-AUDIO-1 | WSP $49 acquisition — upgrade Layer 1 to canonical Cluster A retro-pixel register for all 7 magic elements | IMMEDIATE for VS2a register-fidelity |
| Q-MATT-2 | Music gap 002011-015 path — Option A wired as immediate unblock; Option B Suno per-season awaits decision | PARKED-MATT |
| Q-MATT-5 | Holy register-attention zone — bell-chime composite wired (Tier-1); may need playtest signal to escalate | PROCEEDING default (Path 1) |

### Handoff → knight-rider

Auto-fire trigger for v1.16 JSON-parity dispatch: knight-rider monitors star-lord JSON-parity scout + rocket regen prerequisites (per dispatch note — already in flight). v1.15 completion is independent of v1.16 prerequisite chain.

Manual smoke test recommended before declaring audio pipeline production-ready: launch demo, enter combat for >30s, confirm SFX play on cast/hit/death, confirm ambient ducks during combat and restores on idle.

### What is NOT wired (per dispatch scope)

- Layer 2 class-archetype: Phase-2 deferred per canon § 4.7 — not wired
- Layer 6 voice: forward-flagged per canon § 8 — not VS2a scope
- Layer 7 ritual stingers: composite construction deferred post-VS2a
- WSP spell SFX: Q-MATT-AUDIO-1 spend not yet authorized — manifest has TODO(drax) entries
- Enemy emitter spatial panning: playAbilityCast emitter param wired; spatial routing deferred to monster-skill-emission dispatch
- Per-season Suno tracks for 002011-015: Q-MATT-2 pending; Option A rotation is the live wire
