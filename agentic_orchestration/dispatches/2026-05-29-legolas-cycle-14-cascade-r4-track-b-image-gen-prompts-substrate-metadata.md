# Dispatch — 2026-05-29 — legolas — cascade-r4 Track B — substrate-metadata-informed image-gen prompts (per-kit + per-faction)

**From:** knight-rider
**To:** legolas
**Approved by:** Matt 2026-05-29 (cascade-r4 § 11.2 Track B; Step 7 CONFIRM-FIRE)
**Authority document:** `agentic_orchestration/cycle-14-hive-mind-state.md` cascade-r4 § Step 6/7 + § 11.2 (commit `b9cd9e0`)
**Estimated effort:** Mode A analytical research authoring prompt templates ~1-2d
**Acceptance:** Per-kit + per-faction image-gen prompt templates produced; substrate-metadata-informed per Discipline #41 + D7 AI-tell line; style register per `canonical/story/style-register.md` lock; auto-commit per CLAUDE.md addendum
**Hive-state:** ENABLED — parallel fan-out with gamora + drax + galadriel + gandalf

---

## Context

cascade-r4 Step 6 Matt CONFIRM-FIRE. Track B § 11.2 — drax loadout app refresh + summary tab integration consumes ChatGPT API image-gen for hero + 11 gear-piece images per § 12 + per-faction tile art for loadout app summary tab.

Image-gen prompts are templated with narrow substrate-filled blanks per D7 AI-tell line (canonical/38 § D7) — NOT raw LLM dialogue. Substrate-led discipline per Discipline #41 — substrate votes; designer doesn't pre-impose taxonomy. Style register per `canonical/story/style-register.md` lock (hand-drawn pixel-art HD-2D-shaped register; Octopath Traveler / Triangle Strategy / Eastward / CrossCode primary references).

Legolas provides image-gen prompts informed by per-kit + per-faction substrate metadata (cultural lineage + period + register + element + weapon family + faction OR Wanderer identity).

---

## Required reading before starting

1. THIS dispatch
2. cascade-r4 § Step 6/7 + Amendment 1 + 2: `agentic_orchestration/cycle-14-hive-mind-state.md` tail (commit `b9cd9e0`)
3. Path X output: `agentic_orchestration/cycle-14-wave-5-season-001/phase5_faction_clusters.json` (faction metadata + cluster member kit IDs)
4. Style register (locked): `canonical/story/style-register.md`
5. Canonical 38 D7 AI-tell line: `canonical/38-downstream-delivery-strategy-2026-05-23.md` § D7
6. Designer-writes-substrate principle: `canonical/story/2026-05-29-designer-writes-substrate-player-names-experience-principle.md`
7. Engineering disciplines (Disc #41 substrate-led): `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`
8. Drax Track B dispatch (for consumption coordination): `agentic_orchestration/dispatches/2026-05-29-drax-cycle-14-cascade-r4-track-b-loadout-refresh-plus-12-1-hero-pair-drax-half.md`

---

## Scope

### Per-faction prompt templates (4 in season_001; layer per-Wanderer prompts post-gamora)

For each of season_001's 4 faction clusters (Grounded Chain Strikers / Stormbreak Vanguard / Stormveil Ironclad Surge / Ashfield Siege Callers), author a faction-level image-gen prompt template:

1. **Substrate blanks (filled at prompt construction time, NOT at template design time):**
   - `[cluster_id]` — faction identifier (1, 2, 3, ...)
   - `[faction_name]` — Wave A canonical name
   - `[modal_cultural_lineage]` — e.g., fantasy_generic / european / norse / etc.
   - `[modal_tech_level]` — medieval / pre-industrial / etc.
   - `[modal_tone]` — heroic / grim / mythic / etc.
   - `[modal_bc_engagement_profile]` — ranged / close / hybrid
   - `[modal_bc_damage_geometry]` — chain / large-AOE / spike / etc.
   - `[top_elements]` — element distribution top-3 (e.g., "earth-lightning-fire")
   - `[member_count]` — cluster size

2. **Style register adherence:** template includes style register lock — "in hand-drawn pixel-art HD-2D-shaped illustration register; reference Octopath Traveler / Triangle Strategy / Eastward / CrossCode art direction; isekai-genre-readable; NOT retro pixel-art"

3. **D7 AI-tell line compliance:** templates are TEMPLATED with narrow substrate blanks; NOT raw LLM dialogue; no free-form generation requests. Validation: each template ≤ 200 words with clearly-bracketed substrate blanks.

### Per-kit prompt templates (34 in season_001 — all archive kits; layer per-SINGLETON post-gamora)

For per-kit image-gen prompts (used by § 12 hero + 11 gear extraction; also faction-tile candidate art):

1. **Substrate blanks (per-kit):**
   - `[kit_id]` / `[character_id]`
   - `[wave_b_name]` — Wave B kit name (per-kit identity)
   - `[cluster_id]` — int OR "SINGLETON"
   - `[faction_name]` (if cluster-membered) OR `[wanderer_framing]` (if SINGLETON: "Lone Wanderer of [Season Identity]")
   - `[cultural_lineage]` — per-kit cultural lineage from substrate binding
   - `[historical_period]` — per-kit period
   - `[register]` — per-kit register
   - `[weapon_type_family]` — per-kit weapon family
   - `[element_primary]` — primary chain element
   - `[element_secondary]` (if hybrid per Amendment 7) — secondary chain element
   - `[attribute]` — STR / DEX / INT / WIS
   - `[bc_axes]` — BC tuple (engagement profile / damage geometry / ...)
   - `[t4_strategy]` — Layer 2 T4 strategy

2. **Style register adherence + D7 AI-tell line compliance:** same as faction templates above

3. **Gear-piece prompt sub-template** (for § 12 per-gear extraction):
   - `[gear_slot]` — head / chest / hands / legs / etc. (11 slots)
   - `[kit substrate metadata as above]`
   - Style register: "isolated gear piece; no background; no overlap; suitable for Meshy ingestion; hand-drawn pixel-art HD-2D-shaped illustration register"

### Wanderer-specific prompts (post-gamora)

After gamora Amendment 1 closes, layer Wanderer-specific prompt variants:
- Faction-style template inapplicable (no faction); use Wanderer-framing template with "Lone Wanderer of [Season Identity]" pattern
- Per-Wanderer kit prompts emphasize standalone-identity composition (substrate-honest + genre-thematic isekai canon)

### Output deliverable

Author at `agentic_orchestration/legolas/notes/2026-05-29-cycle-14-v1-image-gen-prompt-templates.md`:
- Per-faction prompt template (4 templates filled with season_001 substrate)
- Per-kit prompt template (1 template + 34 substrate-filled instances for season_001)
- Per-gear-piece sub-template (11 gear-slot templates)
- Wanderer-specific variant templates (post-gamora; layered as iteration)
- Style register adherence checklist per template
- D7 AI-tell line compliance verification per template

---

## Acceptance criteria

- [ ] Per-faction prompt template authored (4 templates for season_001; iteratively extend per season)
- [ ] Per-kit prompt template authored (1 template + 34 substrate-filled instances for season_001)
- [ ] Per-gear-piece sub-template authored (11 gear-slot templates)
- [ ] Wanderer-specific variant templates authored (post-gamora close iteration)
- [ ] Style register adherence verified per template (Octopath Traveler / Triangle Strategy / Eastward / CrossCode reference style; hand-drawn pixel-art HD-2D)
- [ ] D7 AI-tell line compliance verified per template (templated with narrow substrate blanks; ≤ 200 words each; NO free-form LLM dialogue)
- [ ] Substrate metadata fields documented (cultural lineage + period + register + element + weapon family per Discipline #41)
- [ ] Iteration plan documented (Wanderer prompts post-gamora; season 002+003 prompts post-Track-A)

---

## Out of scope

- NO image generation execution (drax executes via ChatGPT API; legolas authors prompts only)
- NO CV-pipeline scoring (galadriel)
- NO loadout app UI integration (drax)
- NO substrate-curation work (elrond)
- NO sub-agent invocation (legolas Mode A discipline; defer parallel work to KR)

---

## KR routing triggers

- Substrate metadata gap surfaced (engine substrate-curation issue; missing fields on kit) → surface to KR for elrond routing
- Style register ambiguity surfaced (prompts can't honor lock without designer call) → surface to KR for gandalf design-call routing
- D7 AI-tell line compliance violation requested (raw LLM dialogue needed for narrative quality) → surface to KR for gandalf design-call routing
- Prompt template size exceeds ChatGPT API context (≥ 4000 chars per template) → surface to KR for tool/format change

---

## Execution sequence

1. Read required-reading docs (especially style register + D7 AI-tell line)
2. Inspect `phase5_faction_clusters.json` for season_001 substrate metadata (4 clusters + 34 kits)
3. Author per-faction prompt templates (4 for season_001)
4. Author per-kit prompt template + substrate-filled instances (34 for season_001)
5. Author per-gear-piece sub-template (11 gear slots)
6. Document iteration plan for Wanderer variants (post-gamora) + season 002+003 (post-Track-A)
7. Auto-commit prompt templates + iteration plan
8. Append completion record to this dispatch
9. Tag: `legolas/v1.0-cascade-r4-track-b-image-gen-prompts-1`

---

## Deliverable summary back to KR

1. Per-faction prompt templates (4 for season_001; status of style-register adherence + D7 compliance)
2. Per-kit prompt templates (1 + 34 instances; status of substrate metadata completeness)
3. Per-gear-piece sub-templates (11 gear slots)
4. Wanderer variant templates (post-gamora deferred plan)
5. Iteration plan for season 002+003 (post-Track-A)
6. Tag committed
7. Commits made

---

## References

- cascade-r4 § Step 6/7 + § 11.2: `agentic_orchestration/cycle-14-hive-mind-state.md`
- Path X output: `agentic_orchestration/cycle-14-wave-5-season-001/phase5_faction_clusters.json`
- Style register: `canonical/story/style-register.md`
- D7 AI-tell line: `canonical/38-downstream-delivery-strategy-2026-05-23.md` § D7
- Designer-writes-substrate principle: `canonical/story/2026-05-29-designer-writes-substrate-player-names-experience-principle.md`
- Drax Track B dispatch: `agentic_orchestration/dispatches/2026-05-29-drax-cycle-14-cascade-r4-track-b-loadout-refresh-plus-12-1-hero-pair-drax-half.md`

---

**KR sign-off:** Authored per Matt 2026-05-29 Step 7 CONFIRM-FIRE + cascade-r4 § 11.2 Track B legolas scope; routed to legolas as seam owner of research/image-gen prompt construction per AGENTS.md scope map. Auto-commit per CLAUDE.md addendum.

---

## Completion Record

**Completed by:** legolas
**Completed at:** 2026-05-29
**Tag:** `legolas/v1.0-cascade-r4-track-b-image-gen-prompts-1`
**Deliverable:** `agentic_orchestration/legolas/notes/2026-05-29-cycle-14-v1-image-gen-prompt-templates.md`

### Status per acceptance criterion

- [x] Per-faction prompt templates (4 for season_001) — COMPLETE; style adherence PASS; D7 compliance PASS
- [x] Per-kit prompt template (1 + 34 instances) — COMPLETE; substrate metadata partially complete (3 gaps flagged)
- [x] Per-gear-piece sub-templates (11 gear slots) — COMPLETE; slot-specific visual notes per slot
- [x] Wanderer-specific variant templates — COMPLETE (Section 4; deferred plan + template format; layering condition: gamora Amendment 1 close)
- [x] Style register adherence verified — PASS all templates
- [x] D7 AI-tell line compliance verified — PASS all templates (all <= 200 words; bracketed blanks; no free-form dialogue)
- [x] Substrate metadata fields documented — COMPLETE; per-kit fields from substrate_weapon_binding (loadout telemetry.db); 3 gaps in KR Flags section
- [x] Iteration plan documented — COMPLETE (Section 5; post-gamora; seasons 002+003; Cycle 15+)

### KR flags requiring routing

1. **wave_b_name gap** — Wave B LLM names not in available JSON output files; routing: rocket/elrond for persistence location
2. **element_primary gap** — per-kit element not persisted in phase4/5 archive; proxy applied (cluster modal element); routing: star-lord/rocket to add per-kit element to archive JSON
3. **t4_strategy gap** — null in phase4 archive insertion per-kit; routing: rocket to expose t4_strategy in archive JSON
4. **modal_tone unknown** — all 4 clusters have modal_tone="unknown"; low impact; routing: gandalf if needed

### Substrate metadata extraction method

- Faction metadata: `phase5_faction_clusters.json` (all fields direct)
- Per-kit BC axes: parsed from `bc_cell_id` string (engagement / damage_level / damage_pattern / attribute / element_secondary)
- Per-kit weapon substrate: `substrate_weapon_binding.select_and_bind_substrate_weapon()` with seed from `kit_archive.db` + loadout `telemetry.db` v1_scope weapon entries
- Per-kit element_primary: cluster modal element proxy (gap; see KR Flag 2)
- wave_b_name: kit_id substituted (gap; see KR Flag 1)
