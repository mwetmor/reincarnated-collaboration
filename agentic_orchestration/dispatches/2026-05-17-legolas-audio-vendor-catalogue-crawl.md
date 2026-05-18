# 2026-05-17 — legolas — Audio vendor catalogue crawl (Mode B / Mode A hybrid)

**Authority:** Matt L3 2026-05-17 late evening — "It is time to fire a Legolas and/or Gandalf/Elrond audio pack research project. I would like to load and wire sound effects." Standard scout → register → curate chain.
**Type:** Pattern B — Mode B catalogue crawl across audio vendors; ~1 day. Read-only across vendors; downstream curation is elrond's; design framing is gandalf's (parallel/queued).
**Predecessors:** Demo audio infrastructure already in place (Howler.js Tier 2 file-lookup + Tier 1 procedural fallback at `src/audio/audio.ts`); empty SFX library on disk; music for historical 001001-005 only; D10-curated 002011-015 hit silent fallback.

---

## Why this matters

The demo's audio pipeline is fully wired in code but starved of assets. `playAbilityCast(geometry, element)` does a Tier 2 file lookup (`/audio/sfx/{geometry}_{element}.{ext}`) and falls back to procedural Tier 1 (basic tones) when no file exists. Procedural tones are placeholders — the actual gameplay feel needs real SFX. Matt has greenlit the audio acquisition workstream.

Concretely needed:
1. **Skill-cast SFX library** — per geometry_type × per canonical-7 element (e.g., fire-projectile, lightning-cast, melee-strike, ground-slam-earth)
2. **Hit/impact SFX** — per element (overlay on skill cast; signals damage applied)
3. **Death SFX** — per tier (trash / elite / boss / player-death distinct)
4. **UI SFX** — button click, menu open/close, inventory open, equip, drop, chest-open, pot-break, loot-pickup, level-up, error
5. **Ambient room-tone loops** — per biome (dungeon, cave, ruined-temple, etc.); supports Layer 4 atmospheric overlay from elrond's 4-layer VFX architecture
6. **Music** — per-season thematic tracks (5 D10 seasons need music; future-proofing for VS2b biome diversity)

This crawl produces the raw catalogue. Gandalf authors sonic-identity register (parallel/queued). Elrond curates the subset (auto-fires when both inputs land).

---

## Required reading (orientation)

1. **`reincarnated-demo/src/audio/audio.ts`** — Tier 2 file-lookup convention (`/audio/sfx/{geometry}_{element}.{ext}` likely; verify by reading `getOrLoadSfx()`); existing ELEMENT_FREQ + GEOMETRY_FREQ_MULT tables for Tier 1 sense-checking
2. **`reincarnated-demo/public/audio/`** — current music directory layout (5 historical season mp3s)
3. **Geometry vocabulary** — `reincarnated-engine/src/reincarnated/generation/geometry_derivation.py` for D10 24-type list (plus monster-skill set once rocket v1.13.1 backfill ships)
4. **Element vocabulary** — canonical-7 substrates (fire / water / earth / wind / lightning / holy / shadow) + physical
5. **Your prior catalogue work** — Pimen subset, icons-and-props crawl, CraftPix mega-catalogue (same JSONL schema pattern; mirror it)
6. **Gandalf VFX scene-needs spec** — `canonical/story/vs2a-vfx-scene-needs.md` for visual-register parallels (audio register will mirror similar logic when gandalf authors)
7. **DoE feel-target doc** — `canonical/story/mobile-feel-target-doe-2026-05-17.md` for combat-pace + UI-sparseness context (mobile audio also needs to be punchy + non-fatiguing)

---

## Scope — three deliverables

### Deliverable 1 — Audio vendor catalogue inventory

Crawl vendors. Categories of vendors to target (non-exhaustive):

**Free / CC0 / CC-BY sources:**
- freesound.org (CC0 + CC-BY; community SFX library)
- OpenGameArt (mixed licenses; game-asset focus)
- Sonniss GDC Game Audio Bundles (annual free packs; commercially-usable)
- Mixkit (free SFX + music; commercial-OK)
- ZapSplat (free with attribution; premium tier exists)
- Pixabay audio (CC0)
- Kenney.nl audio packs (CC0)
- OneShot Studios (free packs)

**Paid / commercial:**
- CraftPix audio packs (commercial-license per craftpix terms; mirror their UI/sprite pack pattern)
- Sonniss premium (~$50-200 per pack)
- Boom Library (high-end SFX; expensive)
- GameSounds.xyz (varied)
- Itch.io game-audio sellers (range of prices)
- Asset Store (Unity / Unreal libraries; check licensing)

**Class-thematic / spell-VFX libraries (highest priority):**
- Fellor / similar pixel-game audio packs (cluster matches our pixel visual register)
- Anything matching "RPG spellcast pack" / "fantasy magic SFX" / "elemental spell library"

Per vendor / per pack:
- **Pack identifier** (vendor + pack name)
- **Pack category** (sfx-spell / sfx-impact / sfx-ui / sfx-ambient / music / mixed)
- **Coverage matrix** (which geometry × element / which UI events / which death tiers / which biomes)
- **File count + format** (wav / mp3 / ogg; mono vs stereo; bit depth)
- **License** (CC0 / CC-BY / CraftPix-Free-Terms / commercial / unclear)
- **Attribution requirements**
- **Cost** (free / $X / subscription)
- **URL / source**
- **Reincarnated-fit score (1-5)** — 5 = direct slot-in (e.g., a pack labeled "Fire Spell SFX" with cast/projectile/impact variants); 4 = strong candidate (covers some elements with extensible naming); 3 = potentially useful; 2 = niche; 1 = off-genre
- **Sonic-register notes** — heavy/cinematic vs lo-fi/retro vs orchestral vs synth; does it match a "HD-painterly-pixel-game" cluster? Gandalf register doc (in parallel/queued) will formalize the criterion; for now, flag obvious clusters
- **Sample audio link** (if vendor provides; otherwise note "preview not available")

Output: `agentic_orchestration/research/catalogue/audio-vendors-2026-05-17/inventory.jsonl`

### Deliverable 2 — Coverage gap matrix

Author `agentic_orchestration/research/catalogue/audio-vendors-2026-05-17/coverage-matrix.md`:

For each SFX slot needed (geometry × element + UI + ambient + music), identify:
- **GREEN** — multiple strong candidates from CC0 / CC-BY / commercial vendors
- **YELLOW** — limited candidates; some quality concerns or vendor risk
- **RED** — no clean candidate; commission or generative path needed

Matrix axes:
- **Skill SFX**: 24 geometry_types × 8 elements (canonical-7 + physical) — 192 cells (most cells likely shareable: e.g., "single_target" + "fire" maps to one SFX whether the skill is "fireball" or "fire bolt"; cell density tunable)
- **UI events**: ~12-15 events (button-click, menu-open, menu-close, inventory-open, equip, drop, chest-open, pot-break, loot-pickup, level-up, error, dash, dodge-iframe-pulse, etc.)
- **Death**: trash / elite / boss / player
- **Ambient**: ~5-8 biomes (dungeon, cave, swamp, forest, desert, ruined-temple, sewer, glowing-cave per elrond CraftPix curation Layer 4)
- **Music**: per-season thematic (5 D10 + future seasons) — note that one good pack with stems may suffice

### Deliverable 3 — Summary doc with shortlist

Author `agentic_orchestration/research/catalogue/audio-vendors-2026-05-17/summary.md`:

Structure (mirror your prior crawl summary docs):
1. Executive summary
2. Vendor count + category distribution
3. License posture summary (CC0 / CC-BY / commercial; cost totals if all RED cells closed)
4. Coverage matrix highlights (RED cells = acquisition priorities)
5. Sonic-register cluster preview (HD-cinematic / lo-fi-retro / orchestral / synth-electronic / pixel-game — clusters observed)
6. **Music gap for 002011-015** — pragmatic options (generate via AI music tools; reuse historical 001001-005 tracks as placeholder; commission per-season; or skip music until production)
7. Acquisition shortlist (prioritized; minimum-cost to close GREEN+YELLOW; preferred-cost to close all)
8. Open questions for Matt — anything that requires his sign-off (e.g., budget ceiling; AI-music-generation acceptable?; per-season vs shared music)
9. Handoffs:
   - → gandalf: vendor sonic-cluster preview informs your audio register / canonical identity authoring (gandalf audio register dispatch is queued; consume your summary when it fires)
   - → elrond: curated-subset manifest authoring (auto-fires when both your crawl + gandalf register land)
   - → matt: acquisition shortlist requires Matt L3 for any commercial spend

---

## Out of scope (DO NOT)

- ❌ DO NOT acquire any packs (Matt L3 required for any purchase)
- ❌ DO NOT modify any audio files on disk (consume + survey only)
- ❌ DO NOT pre-empt elrond curation (your output is RAW catalogue; elrond turns it into manifests + acquisition decisions)
- ❌ DO NOT pre-empt gandalf audio register (you flag sonic clusters as observation; gandalf formalizes register canon)
- ❌ DO NOT touch demo's audio.ts or any code (drax integration follows post-curation)
- ❌ DO NOT extend to voice-over / spirit-guide narration (separate scope; major design+legal layer)
- ❌ DO NOT skim — Matt explicitly named this as a load-bearing research project. Full coverage of the named vendor list; reasonable additional discovery beyond.

---

## Acceptance criteria

- [ ] Audio vendor inventory authored (target 20-40 packs across the named vendor categories)
- [ ] Coverage gap matrix (skill SFX + UI + death + ambient + music; GREEN/YELLOW/RED per cell or aggregated cluster)
- [ ] Summary doc with all 9 sections
- [ ] License posture per vendor (CC0 / CC-BY / commercial / unclear flagged)
- [ ] Sonic-register cluster preview (informal; gandalf formalizes in his register dispatch)
- [ ] Music gap for 002011-015 with pragmatic options outlined
- [ ] Acquisition shortlist with cost + links
- [ ] PRE-SIGNAL § 14.1.1 before hive-log append
- [ ] Hive-log STATE + HANDOFF → gandalf (audio register consumes summary) + HANDOFF → elrond (curation auto-fires when both inputs land) + HANDOFF → matt (acquisition decisions)

---

## Coordination

- **Parallel-safe with**: drax v1.12.0.1 audio hotfix (in flight; defensive null-coalesce; doesn't touch audio system architecture); rocket v1.13.1 monster geometry backfill (in flight); gandalf D11 post-mortem (in flight); D11.1 sprint (pending gandalf verdict)
- **Triggers downstream chain**:
  - → gandalf audio register dispatch (queued; auto-fires after gandalf D11 post-mortem lands AND your crawl lands)
  - → elrond audio curation (queued; auto-fires after gandalf audio register lands)
  - → drax audio wiring (much later; after elrond curation + any Matt-approved acquisitions land)
- **PRE-SIGNAL § 14.1.1** before hive-log appends (many writers today)

---

## Quick orientation — your prior catalogue work pattern

You've shipped 3 catalogue crawls today (legolas-1 icons+props; legolas-2 broader 2D/sprite genre survey; legolas-3 CraftPix mega-catalogue). Mirror the JSONL schema + summary-doc structure. The audio domain is new but the discipline is identical: read-only crawl → structured inventory → gap matrix → shortlist → handoff to elrond.

---

*Dispatched 2026-05-17 by knight-rider per Matt L3 audio research authorization. ~1 day. Append completion record when done.*

---

## Completion record — 2026-05-17

**Status:** COMPLETE
**Completed by:** legolas
**Output files:**
- `agentic_orchestration/research/catalogue/audio-vendors-2026-05-17/inventory.jsonl` — 35 packs catalogued (18 vendors)
- `agentic_orchestration/research/catalogue/audio-vendors-2026-05-17/coverage-matrix.md` — full GREEN/YELLOW/RED matrix across all 5 SFX categories

**Summary returned as agent text output** (per sub-agent rules; not written to file).

**Acceptance criteria status:**
- [x] Audio vendor inventory (35 packs; exceeds 20-40 range minimum)
- [x] Coverage gap matrix (skill SFX + UI + death + ambient + music; GREEN/YELLOW/RED)
- [x] Summary with all 9 sections returned as text
- [x] License posture per vendor (CC0 / CC-BY / commercial / unclear flagged)
- [x] Sonic-register cluster preview (4 clusters: A=retro-pixel, B=mid-fi-orchestral-synth, C=HD-cinematic, D=minimal-generic)
- [x] Music gap for 002011-015 with 5 pragmatic options (A-E ranked)
- [x] Acquisition shortlist with 4 tiers ($3.59 / $182 / $83 / $226 additional)
- [x] Open Matt decisions (6 flagged)
- [x] HANDOFF → gandalf (audio register consumes summary)
- [x] HANDOFF → elrond (curation auto-fires after gandalf register lands)
- [x] HANDOFF → matt (acquisition decisions; Tier 2 ~$182, Tier 3 ~$83 require L3 auth)

**Key finding:** WOW Sound Pixel Magic SFX Pack ($49, retro register) or RPG Magic SFX Pack 3 Elemental ($99, mid-fi register) closes nearly all spell SFX gaps. Register decision is the blocking dependency before acquisition. Zero cells require bespoke commission.
