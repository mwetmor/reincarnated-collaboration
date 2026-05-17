# Gandalf request to knight-rider — per-season Suno AI music prompt pipeline

**From:** gandalf
**To:** knight-rider (for star-lord dispatch authoring + small gandalf design-spec authoring)
**Date:** 2026-05-17 (Day 5 — small commission interleaved with main VS2a work)
**Authorized by:** Matt direct ("I think I have one small commission draft request for you")
**Type:** Two-phase commission — minimum viable text-prompt-per-season; ideal extension to API-integrated music-file-per-season
**Estimated effort:** Phase 1 ~3-5h combined; Phase 2 ~1-2 days depending on Suno API availability

**Source context:** Per `canonical/story/audio-strategy-phase0.md` (authored 2026-05-16 Day 4): *"Music deferred to Phase 1+ (Matt's AI-music-generator workflow IS the Phase-0 strategy)."* This commission operationalizes that workflow — automating the prompt generation per season so Matt doesn't hand-author each season's Suno prompt from scratch.

---

## Why this commission exists

Matt's Phase-0 music workflow is: per generated season → manually craft Suno AI music prompt → paste into Suno UI → download generated music → integrate into demo as that season's ambient track. The manual prompt-authoring step is the friction point. Each generated season has rich per-season identity material (season name, seasonal flavor text, anchor archetype, per-season element vocabulary, Court of Forms framing) that can be templated into a coherent Suno prompt automatically.

Goal: **engine generation produces a per-season Suno prompt as part of the export packet.** Matt opens the season, copies the prompt, pastes into Suno, gets music. Phase 2 extension closes the manual-paste step if Suno API access is viable.

---

## Phase 1 — Minimum viable: per-season Suno prompt text generation

**Goal:** Each generated season produces a Suno-ready prompt as a text file in the season's export directory. Matt manually pastes into Suno UI.

### Track A — Gandalf design spec for Suno prompt template

**Owner:** gandalf
**Estimated effort:** ~1-2h
**Output:** `canonical/story/suno-prompt-template-2026-05-17.md`

**Scope:**

Author a per-season Suno prompt template that consumes the season's identity material and produces a Suno-coherent prompt. Spec must define:

1. **Genre + register anchor** (consistent across all seasons; baseline aesthetic):
   - Diablo-IV-adjacent dark fantasy ARPG + Octopath Traveler / Sea of Stars HD-2D ambient layering
   - Mystical / isekai-coded undertones (per `gandalf-design-lineage.md` Layer 2 + 5)
   - Instrumental-dominant; vocals optional and per-season-discretionary
   - Tempo: slow-to-mid; ambient-leaning rather than combat-driving (combat layer is separate per future audio-strategy doc)

2. **Per-season variable slots** (filled from generation output):
   - **Season name** (e.g., "The Cinderborn Hour")
   - **Seasonal flavor text** (the existing 1-3 paragraph season summary)
   - **Anchor archetype** (Hermit / Full Moon / Capricorn / Death / etc.)
   - **Per-season element vocabulary** (per pool selection: e.g., "ember + frost + tide + bone")
   - **Court of Forms spirit name** (e.g., "Cinderborn") — when L3 vocabulary lands post-Stage-3
   - **Optional: dominant mood descriptor** derivable from anchor + flavor text via LLM mini-call

3. **Suno-coherent prompt structure** (what Suno's prompt parser expects):
   - **Genre tags:** comma-separated short tags (e.g., "dark fantasy, orchestral, ARPG, ambient")
   - **Mood descriptors:** 2-4 evocative adjectives (e.g., "brooding, melancholic, mystical, building")
   - **Instrumentation hints:** specific instruments + their roles (e.g., "low strings melody, distant choir, soft percussion")
   - **Structure hints:** intro/build/climax/outro pacing if relevant (Suno respects this)
   - **Lyrics OR instrumental:** per-season-discretionary; default instrumental; vocals only when flavor text suggests (rare)
   - **Length target:** 3-4 minutes (Suno default; suitable for seasonal-loop ambient)

4. **Exemplar prompts** for 3-5 reference seasons (the existing 1001-1005 production seasons OR hypothetical seasons against the anchor exemplars in `data/seasonal_elements/element-pool.md`):
   - The Hermit season (ember/breath/mist/stone) — solitary, contemplative, slow-build orchestral with low strings + distant choir
   - The Full Moon season (spark/howl/tide/bone) — eerie, lunar, sparse percussion + reverb-heavy ambient
   - The Cinderborn Hour (per Court of Forms framing exemplar) — warm-burn dark fantasy with cinder-tinted brass + slow heartbeat percussion

5. **Genre precedent calibration:**
   - **Reference for tone-and-instrumentation:** D2 / D3 / D4 soundtrack ambient tracks; Diablo IV Sanctuary exploration ambient as the closest band
   - **NOT reference:** PoE combat tracks (too aggressive for seasonal-loop ambient); Bloodborne organ (too gothic-specific); Witcher 3 fantasy folk (too celtic-specific); Skyrim main theme (too triumphant-melodic)
   - **HD-2D adjacency:** Octopath Traveler town themes for the "ambient + storytelling" balance; Sea of Stars overworld for the "warm dark fantasy" tonal anchor

6. **Voice convention** (for any mood-descriptor LLM mini-call):
   - Third-person about the season-as-place ("a season of...")
   - Concrete sensory imagery ("ember-smoke drifting across stone")
   - NOT first-person from player POV; NOT Spirit Guide voice

**Required reading:**
- `canonical/story/audio-strategy-phase0.md` — the policy this commission operationalizes
- `canonical/story/cosmology-reincarnated.md` — Wheel / Earth Self / seasonal descent framing
- `canonical/story/court-of-forms.md` — per-season cohort identity
- `canonical/story/season-feel-rubric.md` — what makes a season feel coherent (informs mood descriptors)
- `data/seasonal_elements/element-pool.md` — anchor examples + flavor templates
- Sample of existing seasons (e.g., `exports/season_001003/metadata.json` or `design_context.md`) for flavor-text structure reference

### Track B — Star-lord per-season prompt generation pipeline

**Owner:** star-lord (LLM call pipeline; `src/reincarnated/llm/`)
**Estimated effort:** ~2-3h
**Output:** New LLM call in season generation pipeline + new export file per season

**Scope:**

1. **Add `suno_music_prompt` generation call** to the per-season LLM call pipeline (per `canonical/19-llm-call-map.md` extension). Inputs: season name + flavor text + anchor + per-season vocabulary + (optional) mood-descriptor mini-call output. Template per Track A spec. Single LLM call per season.

2. **Output: persistent text file** at `exports/<season_id>/suno_music_prompt.txt`:
   - Plain text; copy-paste-ready into Suno UI
   - Includes header comment with season ID + generation date for reference
   - Includes brief usage note ("Paste into Suno AI; recommended duration 3-4 minutes; download .mp3 to `exports/<season_id>/audio/seasonal_ambient.mp3`")

3. **Manifest entry:** add `suno_music_prompt_path` field to season manifest (or `audio_assets` block forward-compat for Phase 2). Drax can read this if downstream demo consumption ever wires the prompt-as-metadata.

4. **MIGRATION.md entry** per ADR-004 (new export file; new manifest field; cross-seam: gandalf design-spec consumed; drax forward-compat consumer; elrond may want to track in catalogue).

5. **Smoke verify:** regen smoke season; confirm `suno_music_prompt.txt` populates with coherent prompt structure per Track A spec; gandalf review of first 1-2 generated prompts for quality.

**Required reading:**
- Track A doc (gandalf design spec)
- `canonical/19-llm-call-map.md` — existing LLM call topology
- Star-lord's existing per-season LLM call patterns (`src/reincarnated/llm/season_*.py` or equivalent)

### Track C — Quality smoke + iteration

**Owner:** gandalf review; Matt validates
**Estimated effort:** ~30 min gandalf + Matt manual Suno test

**Scope:**

1. After star-lord Track B ships, regen 1 season; gandalf reads the generated `suno_music_prompt.txt`; flags any spec violations
2. **Matt manual test:** paste generated prompt into Suno UI; review generated music for genre-coherence + mood-fit
3. If music quality is acceptable: Phase 1 ships; Matt's workflow becomes 1-click-copy + 1-click-paste-and-generate
4. If quality is off: gandalf iterates Track A spec; star-lord re-runs Track B; repeat until acceptable

---

## Phase 2 — Ideal extension: Suno API integration + music file persistence

**Status:** Forward-flag; sequence after Phase 1 ships and Matt confirms workflow is operational

**Goal:** Engine generation calls Suno API directly; music file persisted to `exports/<season_id>/audio/seasonal_ambient.mp3`; Matt's manual paste step removed; demo can wire seasonal ambient track at season-load time.

**Preconditions (none of which gandalf or knight-rider can answer; needs Matt research):**
- Does Suno expose a programmatic API? (Public Suno AI as of 2024-2025 mostly UI-only; API access may exist for paid tiers)
- Cost per generation (Suno credits per song; Matt's existing credits balance)
- Rate limits / generation queueing
- License terms for API-generated music (commercial use; attribution; etc.)

**If preconditions clear:**
- Star-lord extends per-season pipeline: prompt → API call → wait for generation → download .mp3 → persist to season export
- New export file: `exports/<season_id>/audio/seasonal_ambient.mp3`
- Manifest field: `seasonal_ambient_audio_path`
- Drax demo consumer: load seasonal audio at season-start; loop during seasonal play
- New per-season LLM/API budget line item (per `canonical/16-project-roadmap.md` § Single-season-per-playtest rule cost projection)

**If preconditions fail:**
- Phase 2 deferred indefinitely; Phase 1 remains operational with Matt's manual paste workflow

**Out of scope for THIS commission:** Matt researches Suno API availability separately. This commission scopes Phase 1 only; Phase 2 is flagged as forward-extension awaiting Matt's go-decision.

---

## Acceptance criteria (Phase 1)

- [ ] Track A: gandalf design spec doc filed at `canonical/story/suno-prompt-template-2026-05-17.md`; structure + variable slots + exemplars + genre precedent all populated
- [ ] Track B: star-lord pipeline change shipped; `suno_music_prompt.txt` populates per-season at season generation; MIGRATION.md entry filed; smoke test confirms field population
- [ ] Track C: gandalf review of first generation; Matt manual Suno test confirms music quality acceptable
- [ ] Cross-references: Track A doc references audio-strategy-phase0.md + cosmology + court-of-forms + season-feel-rubric; Track B MIGRATION.md entry references Track A spec
- [ ] Phase 2 forward-flag captured: deferred indefinitely awaiting Matt's Suno API research; star-lord's pipeline change leaves forward-compat hook (manifest field for future audio path)

---

## What this commission unblocks + delivers

- **Matt's per-season music workflow shifts from "hand-author Suno prompt every time" to "open season exports, copy prompt, paste into Suno."** Friction reduction is the immediate win.
- **Per-season audio identity becomes a named design dimension** rather than implicit "Matt makes something up." The design-spec Track A produces is a canonical-story artifact that future audio commissions can extend.
- **Phase 2 extension path is named explicitly** — no implicit-pillar-drift on whether the manual paste is the long-term workflow or a placeholder.
- **Aligns with audio-strategy-phase0.md commitment** — operationalizes Matt's AI-music-generator workflow as the Phase-0 audio strategy without inventing new audio-pipeline scope.

---

## Sequencing — flexible

Independent of:
- VS2a critical-path work (MS cascade, B6, character ingest, Drift-14 pool cull, Stage B export-DTO, etc.)
- VS2b parallel work (cipher migration, embodiment display)
- All other in-flight dispatches

Can fire whenever gandalf + star-lord have a small capacity window. **Recommended priority: LOW** — small win that doesn't gate any near-term ship; bundle into a capacity-permitting session.

---

## Open questions for gandalf (Track A authoring)

1. **Per-season-vocabulary substitution in the Suno prompt itself** — should the prompt reference per-season element labels (e.g., "ember + frost") OR canonical-four labels (e.g., "fire + ice")? Suno's prompt parser may not recognize project-specific vocabulary; canonical-four labels translate to broader cultural fantasy vocabulary. Recommend: **canonical-four labels in Suno prompt for clarity**, with per-season labels embedded in the FLAVOR-TEXT portion of the prompt for character. Drax-side seasonal-vocabulary cipher migration doesn't reach Suno.
2. **Combat-track separation** — does this commission scope ONLY seasonal-ambient music, or also combat-track variations? Recommend: **seasonal-ambient only for Phase 1**; combat-track per-encounter is post-VS2a scope.
3. **Voice-line / vocal-track integration** — Suno can generate vocals. Recommend: **instrumental default**; vocals only when flavor text strongly suggests (rare; gandalf judgment call per-season).

---

— gandalf, 2026-05-17 (Day 5 — small commission interleaved with main VS2a work)
