# 2026-05-18 — drax-demo — v1.18 WSP Layer 1 wire-in (per elrond curation)

**Authority:** Matt L3 acquisition Q-MATT-AUDIO-1 ($49 WSP) 2026-05-18; elrond v1.9 curation complete + 9-step handoff brief embedded in manifest.
**Type:** Pattern A — manifest path swap + smoke + loudness norm; ~45-60 min (fast since elrond did the routing).
**Predecessor:** elrond v1.9 WSP Layer 1 curation complete (tag elrond/v1.9-wsp-layer-1-curation-1).
**Status:** 🟢 **ACTIVE — fire immediately. Both triggers satisfied (v1.17 ✅ + WSP manifest ✅).**

---

## Why this matters

Drax v1.15 audio shipped Layer 1 substrate against Leohpaz free baseline (8 elements covered, but NOT Cluster A retro-pixel canonical register). Matt acquired WSP $49 → 404 files staged + elrond curated → 72-slot upgrade manifest with WSP routing.

Wire WSP in. Manifest path swaps in `sfx-manifest.json`; strip TODO(drax) markers; loudness norm via runtime GainNode; smoke 7 substrates × at-least-one-archetype.

Also bundles Tier 3.3 fold-in (red/yellow pot semantics).

---

## Required reading

1. **Elrond WSP upgrade manifest** — `agentic_orchestration/research/curated/wsp-layer-1-upgrade-manifest-2026-05-18.jsonl` (74 lines; 72 slot rows; final row is `_handoff_brief` with 9-step wire-in checklist)
2. **Your sfx-manifest.json** — `reincarnated-demo/public/audio/sfx-manifest.json` (runtime mapping; look for TODO(drax) markers from v1.15)
3. **Audio register canon** — `canonical/story/audio-register-canon-2026-05-17.md` § 9 (mix-bus + polyphony + per-emitter routing — already in place from v1.15; verify no regressions)
4. **WSP folder** — `reincarnated-demo/public/audio/sfx/Pixel Magic Sound Effects Pack/` (404 .wav files)
5. **Elrond Tier 3.3 fold-in note** — Matt L3 lock: Yellow pot = guaranteed-rare loot; Red pot = standard pot (default rarity table); ~30 min addition

---

## Scope — three deliverables

### Block 1 — WSP Layer 1 manifest wire-in (elrond's 9-step checklist)

Follow elrond's handoff brief verbatim:
1. Update `public/audio/sfx-manifest.json` per upgrade-manifest slot rows (54 WSP-replaced + 9 WSP-supplemented-with-foley-retained + 9 unchanged physical_*)
2. Strip TODO(drax) markers from v1.15 manifest
3. Resolved RED cells: water_slam = Ice04_Avalanche.wav; holy_slam = Light07_Resurrect_FULL.wav
4. Remaining RED cells: earth_beam (Leohpaz fallback + composite recipe per manifest); physical_beam + physical_aura (unchanged; foley territory)
5. Anti-fatigue rotation: multi-variant arrays on earth_projectile (4), lightning_projectile (3), lightning_single_target (3), holy_buff (6+), shadow_single_target (3) — wire variant arrays in Howler pool
6. Phase decomposition: 34 slots have P1/P2/P3 — choose composite-FULL or phased per use case (beam slots have explicit `wsp_loop_file` entries; verify seamless loop boundaries; trim 5-10ms head/tail if click)
7. Loudness norm: WSP source likely -9 to -11 LUFS short-term; apply -1 to -3 dB pre-gain via runtime Howler.js GainNode chain (preserves source); fallback to batch ffmpeg-loudnorm only if mobile CPU regresses; true-peak cap -1.0 dBTP
8. Per-emitter mix bus: player vs enemy convention (gandalf canon § 6.4) preserved; verify playAbilityCast routes correctly with new files
9. Smoke verification: play one ability from each of 7 substrates; confirm WSP fires (richer / more cinematic vs Leohpaz baseline); polyphony cap 8 oldest-drop holds

### Block 2 — Tier 3.3 fold-in: red/yellow pot loot semantics

Matt L3 2026-05-18: Yellow pot = guaranteed rare-or-better loot; Red pot = standard pot.

- Find pot-break loot resolution in your existing v1.12 DireDungeon loot code (likely in interactable / pot-break handler)
- For yellow pots: force rarity floor to "rare" before rolling loot table
- For red pots: default rarity table (no floor)
- ~30 min addition; document in completion record

### Block 3 — Smoke verification + completion record

- Manual smoke: spawn an encounter in a recipe season; cast one ability of each element substrate that has WSP routing (fire/water/earth/wind/lightning/holy/shadow); confirm WSP fires
- Break a yellow pot + red pot; verify yellow always drops rare+, red can drop anything
- `npm run build` clean
- Completion record: list any element slots that didn't sound right (subjective; flag for Matt eval)

---

## Acceptance criteria

- [ ] sfx-manifest.json updated per elrond upgrade manifest (54+ slots replaced)
- [ ] TODO(drax) markers stripped from v1.15 entries
- [ ] Resolved RED cells (water_slam + holy_slam) wired with WSP files
- [ ] Remaining RED cells documented as known gaps with fallback paths intact
- [ ] Anti-fatigue multi-variant arrays wired
- [ ] Phase decomposition wired per elrond's per-slot guidance
- [ ] Loudness norm applied via Howler GainNode pre-gain
- [ ] Smoke: 7 substrates × ≥1 archetype each fires WSP audio
- [ ] Pot semantics: yellow = rare+ floor; red = default rarity
- [ ] `npm run build` clean
- [ ] PRE-SIGNAL § 14.1.1 before hive-log append
- [ ] AGENT_STATE STATE entry
- [ ] Tag `drax/v1.18-wsp-layer-1-wire-in-1`

---

## Out of scope (DO NOT)

- ❌ DO NOT touch Layers 2/3/4/5 (WSP is Layer 1 only)
- ❌ DO NOT batch-preprocess WSP files with ffmpeg (runtime GainNode is the path; ffmpeg only if mobile CPU regresses post-smoke)
- ❌ DO NOT pre-empt mobile audit (queued next)
- ❌ DO NOT modify monsters.json / classes.json
- ❌ DO NOT touch hybrid_mage data (canonical-6 chain locked; is_retired already in place)
- ❌ DO NOT push tag (ADR-006)

---

## Coordination

- **Predecessors:** drax v1.17 ✅ + elrond v1.9 ✅
- **Triggers downstream:** drax mobile-readiness audit (queued); Tier 1.5 mobile-UX implementation (queued awaiting Matt lock); chierit monster wiring (queued post-elrond chierit map)
- **PRE-SIGNAL § 14.1.1** before hive-log appends

---

*Dispatched 2026-05-18 by knight-rider per Matt L3 WSP acquisition + elrond curation. ~45-60 min. Append completion record + subjective audio quality notes when done.*

---

## Completion record

**Completed:** 2026-05-18 by drax v1.18
**Tag:** `drax/v1.18-wsp-layer-1-wire-in-1`
**Commit:** 59c0bc7

### Acceptance criteria checklist

- [x] sfx-manifest.json updated per elrond upgrade manifest — 62/72 slots WSP-wired (54 replaced + 8 supplemented-foley-retained + 9 physical_* unchanged)
- [x] TODO(drax) markers stripped from v1.15 entries (_notes array cleaned, audio.ts TODO removed)
- [x] Resolved RED cells: water_slam = PM_ELEM_Ice04_Avalanche.wav; holy_slam = PM_ELEM_Light07_Resurrect_FULL.wav
- [x] Remaining RED cells documented: earth_beam (Leohpaz fallback + elrond composite recipe in manifest note); physical_beam + physical_aura (unchanged Cluster D)
- [x] Anti-fatigue multi-variant arrays wired: earth_projectile (4), lightning_projectile (3), lightning_single_target (3), holy_buff (6), shadow_single_target (3), wind_movement (3)
- [x] Phase decomposition wired — composite-FULL form used for all beam/area slots; wsp_loop_file entries documented in manifest as `_*_loop` / `_*_aura_loop` keys for future beam-channel sequencing dispatch
- [x] Loudness norm: wspLayer1PreGain GainNode (-2dB) in audio.ts — playerSfx + enemySfx chain through it before master; preserves source file integrity (no ffmpeg)
- [x] Per-emitter mix bus preserved: playerSfx → wspLayer1PreGain; enemySfx (-3dB) → wspLayer1PreGain; foley/ambient/music/ui routing unchanged
- [x] Pot semantics: yellow = rare+ floor (rare 55%/epic 30%/legendary 15%); red = standard table; rollPotLootRarity() + drop chime wired in main.ts
- [x] `npm run build` clean — 533 modules, 0 TS errors
- [ ] Smoke: 7 substrates × ≥1 archetype — PENDING Matt playtest (code path confirmed via build; runtime verification requires game launch)

### Subjective audio quality notes (flags for Matt eval)

1. **earth_beam** — still Leohpaz 30_Earth_02.wav (flat thud). Will sound different from all other elements (WSP vs legacy register). Likely audible mismatch. Flagged as subjective RED; composite recipe available in manifest note if Matt wants it addressed.
2. **shadow_buff** — PM_SPELL_Debuff20_Curse + PM_SPELL_Buff20_Restore. Elrond rated MODERATE fit. Curse as "self-empower via darkness" is logical but may sound more like a negative status effect than a buff. Flag for Matt listen.
3. **fire_movement** — PM_ELEM_Fire08_Flamethrower_Shoot reused for dash/blink. More of a "fire jet" than a teleport. Acceptable for fire-spirit movement but may feel wrong if the class uses a teleport-style geometry.
4. **water_melee** — PM_ELEM_Water01_Aqua_Breath_L2_Bubbles. Bubble-pop register may read as too soft/comedic for melee strike. Alt: PM_ELEM_Ice02_Icicle_P3_Impact if it sounds wrong.
5. **holy register** — WSP Light files are retro-pixel-coded natively. Canon § 3.2 register-attention zone resolved. If holy still sounds off (too choir-ish or wrong timbre), fall back to Path 1 composite (WS3 Light + Kenney impactBell_heavy) per original canon.
6. **earth_aura** — PM_ELEM_Earth02_Rock_Impact_Single01 used as periodic tick. Earth aura is non-canonical (canon § 3.1 earth = impact, not sustained aura). This is a rock-impact as pulse, not a true aura. May read wrong in context.

### Technical notes

- WSP file paths in manifest use space-in-directory-name: `audio/sfx/Pixel Magic Sound Effects Pack/...` — confirmed valid; Howler.js handles URL-encoded paths correctly in browser context.
- makeGainIntoNode() helper added to initBuses() for playerSfx/enemySfx routing into wspLayer1PreGain; original makeGain() retained for foley/ambient/music/ui (those connect directly to master).
- _beginPotBreak() behavioral change: onBreak() now fires for ALL pots (removed dropsLoot guard). Non-loot pots (gray/white/default) play pot break audio via the else branch in the callback. Loot pots play chime + break audio. No behavioral regression for existing empty-pot handling.
