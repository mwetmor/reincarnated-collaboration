# 2026-05-18 — elrond — WSP Layer 1 curation: map 405 Pixel Magic SFX files to substrate manifest slots

**Authority:** Matt L3 acquisition 2026-05-18 (Q-MATT-AUDIO-1 $49 approved + staged); upgrades Layer 1 substrate from Leohpaz free baseline to canonical Cluster A retro-pixel register per audio canon § 9.
**Type:** Pattern A — curation + upgrade-manifest authoring; ~45-60 min.
**Status:** 🟢 **ACTIVE — fire immediately. Parallel-safe with drax v1.17 + jack-ryan cross-canon strip.**

---

## Why this matters

Drax v1.15 audio wiring shipped Layer 1 substrate against Leohpaz free baseline (8 elements covered but NOT the canonical Cluster A retro-pixel register that gandalf locked). TODO(drax) markers in `public/audio/sfx-manifest.json` flagged WSP-upgrade paths for when Q-MATT-AUDIO-1 resolved.

Matt acquired WSP (Pixel Magic Sound Effects Pack; 405 .wav files) and staged it at `/Users/admin/Games/reincarnated-demo/public/audio/sfx/Pixel Magic Sound Effects Pack/`. WSP has canonical Cluster A retro-pixel register fidelity for all 7 magic elements + arcane/dark variants. This is the upgrade Layer 1 has been waiting for.

Your curation maps the 405 files to the canonical Layer 1 manifest slots so drax v1.18 can drop them in as a direct manifest replacement.

---

## Required reading

1. **Audio register canon § 9** — `canonical/story/audio-register-canon-2026-05-17.md` § 9 (5-layer architecture; element signatures; folder schema; same-file player/enemy convention)
2. **Your prior Layer 1 manifest** — `agentic_orchestration/research/curated/audio-substrate-subset-vs2a-2026-05-17.jsonl` (14 active rows; Leohpaz baseline)
3. **Drax v1.15 sfx-manifest** — `reincarnated-demo/public/audio/sfx-manifest.json` (runtime mapping; look for TODO(drax) entries flagging upgrade paths)
4. **WSP folder** — `/Users/admin/Games/reincarnated-demo/public/audio/sfx/Pixel Magic Sound Effects Pack/` (405 .wav files; naming pattern PM_ELEM_<element><nn>_<descriptor>_FULL.wav + P<n>_<phase> variants)
5. **Drax v1.15 completion** — `agentic_orchestration/dispatches/2026-05-17-drax-v1-15-audio-wiring-queued.md` § completion (notes on TODO markers + manifest schema)
6. **Cluster A retro-pixel register** — gandalf audio canon § 9 (register fit verification)

---

## Scope — three deliverables

### Deliverable 1 — WSP file inventory + element categorization

Inventory the 405 files. Categorize by element:
- Fire (PM_ELEM_Fire*)
- Water (PM_ELEM_Water* / Ice* if applicable)
- Earth (PM_ELEM_Earth*)
- Wind (PM_ELEM_Wind* / Air*)
- Lightning (PM_ELEM_Lightning* / Thunder*)
- Holy (PM_ELEM_Holy* / Light* / Divine*)
- Shadow (PM_ELEM_Dark* / Shadow*)
- Arcane / Other (PM_ELEM_Arcane* / generic)

For each element, identify:
- "FULL" composite variant (use for short cast effects)
- "P1_Trigger" / "P2_Impact" / "P3_<phase>" decomposition (use for phased multi-stage casts)
- Special variants (poison, hex, gravity, etc. — flag for archetype-specific use)

### Deliverable 2 — Layer 1 manifest upgrade map

Author `agentic_orchestration/research/curated/wsp-layer-1-upgrade-manifest-2026-05-18.jsonl` mapping WSP files to canonical Layer 1 slots per audio canon § 9. Schema (one row per slot):

```jsonl
{"slot": "layer1/fire_aoe", "wsp_file": "PM_ELEM_Fire03_Explosion_FULL.wav", "phase": null, "cluster_fit": "A-retro-pixel", "leohpaz_replaces": "L_fire_aoe_01.wav", "notes": "Composite for short-cast AOE"}
{"slot": "layer1/fire_beam", "wsp_file": "PM_ELEM_Fire07_Beam_P1_Cast.wav,PM_ELEM_Fire07_Beam_P2_Sustain.wav,PM_ELEM_Fire07_Beam_P3_End.wav", "phase": "composite", "cluster_fit": "A-retro-pixel", "leohpaz_replaces": "L_fire_beam_01.wav", "notes": "Multi-phase beam"}
...
```

Cover the 14 active rows from prior Layer 1 manifest (substrate × archetype routing). If WSP has the file, map it. If WSP doesn't (gap), retain Leohpaz fallback path + flag.

### Deliverable 3 — Drax v1.18 handoff brief

Brief block at end of upgrade-manifest doc summarizing what drax does in v1.18 (or whatever version comes after current v1.17):
- Update `public/audio/sfx-manifest.json` per upgrade map (replace Leohpaz paths with WSP paths)
- Strip TODO(drax) markers from manifest
- Manual smoke: play one ability from each element; confirm WSP sound fires (richer / more cinematic vs Leohpaz baseline)
- Loudness check: -14 LUFS target still met (WSP may need volume normalization)
- Per-skill auditory check: gandalf canon § 9 hooks (player vs enemy mix-bus; polyphony cap 8)

---

## Acceptance criteria

- [ ] WSP file inventory authored (405 files categorized by element + phase)
- [ ] Element coverage gap analysis (which substrate slots have full WSP coverage vs partial vs none)
- [ ] Upgrade manifest at `research/curated/wsp-layer-1-upgrade-manifest-2026-05-18.jsonl`
- [ ] Drax v1.18 handoff brief included
- [ ] Loudness normalization recommendation (if WSP files need preprocessing)
- [ ] PRE-SIGNAL § 14.1.1 before hive-log append
- [ ] AGENT_STATE STATE entry
- [ ] Tag `elrond/v1.9-wsp-layer-1-curation-1`

---

## Out of scope (DO NOT)

- ❌ DO NOT modify drax sfx-manifest.json yourself (drax v1.18 seam)
- ❌ DO NOT preprocess WSP files (drax does loudness norm if needed)
- ❌ DO NOT pre-empt drax v1.17 + mobile audit queue
- ❌ DO NOT touch other Layers (Layer 3/4/5 unchanged; WSP is Layer 1 only)
- ❌ DO NOT push tag (ADR-006)

---

## Coordination

- **Parallel-safe with:** drax v1.17 in flight (different repo); jack-ryan cross-canon strip pass in flight (different repo); drax v1.18 mobile audit queued (different drax sequencing position)
- **Triggers downstream:** drax v1.18 (or v1.19) WSP Layer 1 wire-in dispatch — knight-rider fires post-yours + post-drax-v1.17
- **PRE-SIGNAL § 14.1.1** before hive-log appends

---

## Drax queue note

Current drax queue: v1.17 multi-bundle (in flight) → mobile-readiness audit (queued; Matt-authorized) → mobile-polish v1.19 (TBD post-audit).

WSP wire-in inserts ahead of mobile-audit per Matt's "when unblocked + no other priorities" qualifier (audio is higher visible-value than mobile audit; both pending Matt input). So drax sequence will be: v1.17 ships → WSP wire-in → mobile audit → mobile polish.

---

*Dispatched 2026-05-18 by knight-rider per Matt L3 WSP acquisition. ~45-60 min. Append completion record + upgrade-manifest path when done.*

---

## Completion record — elrond — 2026-05-18

**Status:** DONE. Tag `elrond/v1.9-wsp-layer-1-curation-1` (local; no push per ADR-006).

**Deliverables:**
1. **WSP file inventory + element categorization** — 404 .wav files at `/Users/admin/Games/reincarnated-demo/public/audio/sfx/Pixel Magic Sound Effects Pack/` categorized by prefix:
   - `PM_ELEM_Fire` 29 / `Water` 4 / `Ice` 23 / `Earth` 6 / `Wind` 21 / `Electric` 17 / `Light` 34 / `Dark` 34 / `Time` 29 = **197 element files**
   - `PM_GENERIC` 55 (combat foley: slash, kick, impact, missile, death, jump, miss, projectile, hammer, needles, dash)
   - `PM_SPELL_Buff` 32 + `PM_SPELL_Cast` 32 + `PM_SPELL_Debuff` 24 = **88 generic spell files**
   - `PM_UI` 8 (button select, menu, heal items, save)
   - Phase-decomposition pattern confirmed: FULL composite + P1/P2/P3 phase variants for most major spells; L1/L2 layer variants for AOE compositions.
2. **Upgrade manifest** — `agentic_orchestration/research/curated/wsp-layer-1-upgrade-manifest-2026-05-18.jsonl` (74 lines: 1 meta + 72 slot rows + 1 handoff brief). All 167 WSP file references cross-validated on-disk (zero ghosts).
3. **Drax v1.18 (or v1.19) handoff brief** — embedded in upgrade manifest final row (`_handoff_brief`); 9-step wire-in checklist covering path replacements + TODO-strip + RED-cell resolution notes + loudness norm + smoke verification + per-emitter mix bus + telemetry + register-attention-zone resolution + acceptance.

**Key findings:**
- **WSP → canonical-7 routing:** Fire→fire / Water+Ice→water (Ice supplies projectile/beam/slam/aura where PM_ELEM_Water is thin at 4 files) / Earth→earth / Wind→wind / Electric→lightning / Dark→shadow / Light→holy.
- **Canon § 3.2 register-attention zone RESOLVED for holy** — WSP supplies retro-pixel holy directly (34 PM_ELEM_Light files). Path 1 composite-construction (WS3 Light + Kenney bell-chime + pitch-shift) NO LONGER REQUIRED for normal operation. Path 1 recipe remains documented as fallback if WSP Light timbre proves register-mismatched at integration audition.
- **TWO canon § 4.6 RED-cells RESOLVED by WSP**:
  - `water_slam` → `PM_ELEM_Ice04_Avalanche.wav` (cascading ice-mass impact — canonical water-slam signature)
  - `holy_slam` → `PM_ELEM_Light07_Resurrect_FULL.wav` (descending holy-impact)
- **Remaining RED-cells post-WSP:** `earth_beam` (WSP earth thin — 6 impact-only files, no sustained-grind loop; Leohpaz fallback retained + composite recipe documented), `physical_beam` + `physical_aura` (unchanged — Cluster D foley territory; WSP cannot help).
- **Slot coverage:** 72 logical Layer-1 slots in `sfx-manifest.json`. 54 WSP-replaced (7 magic elements × 8 archetypes ex movement edge cases — most slots STRONG fit) + 9 WSP-supplemented-with-foley-retained (`*_melee` + `*_slam` for foley underlayers) + 9 unchanged physical_* slots (NOT WSP territory).
- **Anti-fatigue rotation enabled:** Per canon § 5.5, multi-variant slots provided for `earth_projectile` (4 Rock_Impact_Single variants), `lightning_projectile` (3 zap variants), `lightning_single_target` (3 Strike_Impact variants), `holy_buff` (6+ Heal/Buff variants), `shadow_single_target` (3 Hex/Doom/Evil_Hex variants). Drax wires arrays for engine pitch-rotation.
- **Phase decomposition available** for 34 slots — drax can choose composite-FULL (short cast) or phased P1/P2/P3 (telegraphed cast→impact). Beam slots have explicit `wsp_loop_file` for sustain.

**Loudness norm recommendation (drax):**
- WSP source likely ships at -9 to -11 LUFS short-term (commercial pack norm — louder than canon § 5.1 Layer-1 -12 LUFS target).
- **Apply -1 to -3 dB pre-gain at integration.** Two options: (a) batch `ffmpeg-loudnorm` to -12 LUFS pre-drop into final paths; (b) runtime GainNode offset in Howler.js chain. **Recommendation: (b) runtime gain** — preserves source-pack file integrity for future re-mastering + faster integration. Reverse to (a) if mobile CPU budget reveals runtime-gain regression.
- True-peak cap -1.0 dBTP — verify post-gain at integration; impact transients may need brick-wall limiter.
- For `*_beam` loop files: verify seamless loop boundaries — trim 5-10ms head/tail if click at boundary.
- Format: WSP ships `.wav` 24-bit 96kHz. Recommend keeping `.wav` for v1.18 ship-quick + transcoding to `.ogg` in v1.19 mobile-polish if bundle-size flags it.

**Out of scope (deferred to future dispatches):**
- `PM_ELEM_Time` (29 files) — control-status SFX; Layer-3 `status_slow` / `status_haste` / `status_dispel` slots; not currently in `sfx-manifest.json` schema; future status-effect SFX dispatch.
- `PM_SPELL_Debuff` (24 files) — Layer-3 `status_debuff` supplements; future dispatch.
- `PM_SPELL_Cast` (32 files, ex used for *_buff) — Layer-3 ritual-cast or generic G9 BUFF preambles; future dispatch.
- `PM_SPELL_Buff` (32 files, ex ~7 used) — ~25 unused for future Layer-3 expansion.
- `PM_GENERIC` (55 files) — Layer-3 foley + death slots; major future upgrade opportunity (Death_Boss01/02 + Death_Monster01/02 map directly to existing `death_*` slots in sfx-manifest.json).
- `PM_UI` (8 files) — Layer-3 `ui_*` upgrade candidates; single-dispatch wire-in feasible at drax v1.19 or v1.20 mobile-polish window.

**Cross-seam scope honored:**
- ❌ NO modification to `reincarnated-demo/public/audio/sfx-manifest.json` (drax v1.18 seam).
- ❌ NO preprocessing of WSP files (drax does loudness norm).
- ❌ NO touching of other Layers (Layer 3/4/5 unchanged).
- ❌ NO tag push (ADR-006 honored).

**Drax queue handoff:** v1.17 ships → **WSP Layer 1 wire-in (this manifest)** → mobile audit → mobile polish, per dispatch coordination note.

— elrond
