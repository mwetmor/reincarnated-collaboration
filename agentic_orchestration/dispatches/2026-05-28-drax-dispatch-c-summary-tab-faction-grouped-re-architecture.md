# Dispatch — 2026-05-28 — drax — Dispatch C: Summary tab faction-grouped re-architecture (Replace /pitch with /summary; ~1-2 weeks)

**From:** knight-rider
**To:** drax (loadout/demo seam owner)
**Approved by:** Matt 2026-05-27 design call #2 ratified ("REPLACE /pitch with /summary. /pitch deprecated; new /summary canonical player-surface; if marketing page needed later, author as separate /marketing route") + Matt 2026-05-28 parallel-firing authorization (fires post Wave 5 Step 1 GENERATION completion; parallel with gandalf Step 2)
**Estimated effort:** ~1-2 weeks drax (Summary tab re-architecture; faction-grouped layout; Path III F-C inter-faction surfacing; doc 49 § 1.X compliance; D-Sharpened invariance)
**Acceptance:** New `/summary` route operational; `/pitch` deprecated; Summary tab consumes ExportFactionCluster + ExportFactionRelationship (post Wave 5 production season output); faction-grouped layout displays K∈{3,4} clusters + F-C inter-faction relationship_type narrative; seasonal_hero spotlight slot ready (compose with Dispatch H Meshy embed when Meshy URL lands); Discipline #45 vocab-lock CLEAN; D-Sharpened invariance verified

## Quality criterion (Move 1)

**Game-quality goal this dispatch serves:** replace the static `/pitch` marketing page with the canonical `/summary` player-surface consuming Cycle 14 Wave 5 production data — substrate-emergent faction-grouped kit identity surfaces as the player's first orientation point per season. Composes "Engine first. Game second. Phase third." — Phase 5 emergent identity flows through PM-1 GMM K∈{3,4} clustering + PM-2 D-Sharpened + F-C inter-faction relationships into player-facing faction surface at /summary.

**Refutation conditions** (drax surfaces if any apply):
- ExportFactionCluster + ExportFactionRelationship schemas don't expose enough fields for faction-grouped UX (schema gap)
- Wave 5 production season output JSON shape isn't consumable by loadout data layer (cross-seam contract mismatch)
- F-C relationship_type 6-enum visual treatment conflicts with existing color/visual language
- D-Sharpened invariance breaks if seasonal_hero spotlight metadata leaks to player-facing layer

## Context

**Authority chain:**
- Matt 2026-05-27 design call #2 ratified: REPLACE /pitch with /summary
- Drax Cycle 14 Pattern-A response `a0a449e` Summary tab gap inventory (Q-Summary-6 framing flaw caught: NOT config swap but substantive new architecture)
- Doc 49 (gandalf `67b22d7`) Summary tab player-surface design canonical
- Doc 49 § 1.1.1 rank-0 amendment (gandalf `35c2800`) — composes with Loadout Phase A foundation
- Gandalf seasonal_hero H-5 hybrid spec (`574624a`) — Summary tab consumes season_hero_id metadata
- Gandalf path-iii faction-assembly-extension (`574624a`) — F-C inter-faction relationship_type narrative
- Wave 3 Seam 1 LLM prompts (gandalf meta `3532d76`) — F-C 6-enum {antagonist/rival/allied/neutral/mysterious/parallel}
- Wave 3 Seam 2 ExportFactionRelationship (star-lord `6f94ce5`) — schema + fields
- PM-1 multimodal clustering at engine `a466eb1` (rocket) — K∈{3,4} BIC-selected
- PM-2 D-Sharpened at engine `7233e0f` + § 13 G-B at engine `768a68d` — primary_faction_pair metadata

**Composition with Dispatch H (Meshy embed; queued):** Dispatch C delivers Summary tab faction-grouped re-architecture WITH a seasonal_hero spotlight SLOT (placeholder OR static portrait from G-2-equivalent sidecar); Dispatch H fills the slot with Meshy embed iframe when Meshy URL lands. Dispatch C does NOT block on Meshy URL availability — graceful fallback to static portrait OR placeholder.

**Composition with G-2-equivalent Sidecar (legolas portraits + galadriel AI-tell + drax wiring):** Portrait sidecar fires in parallel; drax Summary tab consumes portrait artifacts when sidecar lands; fallback to placeholder if sidecar delayed.

## Required reading

- `canonical/49-loadout-sample-player-surface-design-2026-05-27.md` (Summary tab player-surface design canonical)
- `canonical/story/seasonal-hero-h-5-hybrid-spec-2026-05-27.md` (gandalf seasonal_hero § 6 drax Summary tab consumption semantics)
- `canonical/story/phase-5-llm-prompts-cohesion-judge-2026-05-27.md` (gandalf Wave 3 Seam 1 § 6 F-C inter-faction relationship_type spec)
- `agentic_orchestration/gandalf/notes/2026-05-27-path-iii-faction-assembly-extension.md` (Path III full spec)
- `agentic_orchestration/drax/notes/2026-05-27-cycle-14-tab-integration-pattern-a-response.md` § Summary tab (current state + redesign scope)
- `~/Games/reincarnated-engine/src/reincarnated/export/schemas.py` ExportFactionCluster + ExportFactionRelationship + ExportSeasonHero
- `~/Games/reincarnated-loadout/src/components/Pitch.tsx` (current /pitch surface; deprecating)
- `~/Games/reincarnated-loadout/src/App.tsx` (route config; replace /pitch with /summary)
- `.claude/skills/reincarnated-drax-operating-procedure`

## Discipline #46 compliance

- N/A — loadout consumes engine JSON output; no DB queries

## Discipline #42 framing-audit

- **Q1 load-bearing assumptions:** (1) ExportFactionCluster + ExportFactionRelationship + ExportSeasonHero schemas are stable enough for Summary tab consumption; (2) Wave 5 production season output JSON path/shape is consumable by existing loadout data layer; (3) seasonal_hero spotlight slot composes cleanly with Dispatch H Meshy embed (when Meshy URL lands) AND with G-2-equivalent portrait sidecar (fallback); (4) faction-grouped layout for K∈{3,4} clusters fits mobile + desktop + tablet
- **Q2 refutation evidence to seek:** verify schema field availability at impl entry; verify Wave 5 output JSON shape; smoke-test on Wave 5 production data when available
- **Q3 outcome trigger:** if Wave 5 output not yet available at fire time, partial-fire scope (Summary skeleton + placeholder data) OR invoke #44 framing-refusal + defer to post-Wave-5

## Scope

### Part 1 — `/summary` route + `/pitch` deprecation (~1 day)

- [ ] Add `/summary` route in App.tsx with new SummaryTab component
- [ ] Deprecate `/pitch` route (redirect to /summary OR keep as legacy /marketing if Matt later requests)
- [ ] Nav.tsx update — Summary tab links to /summary
- [ ] Composition with mobile-fix from Dispatch G (right-fade gradient overlay preserved)

### Part 2 — Faction-grouped layout (~3-5 days)

- [ ] SummaryTab component renders K∈{3,4} faction clusters from ExportFactionCluster
- [ ] Per-cluster: faction_label_canonical (Phase 5 LLM-generated) + cluster_compactness + diversity_flag + per-kit list
- [ ] Per-cluster header includes primary_pair_flag visual treatment (highlights primary faction-pair from G-B selection)
- [ ] Responsive: mobile stacked / tablet 2-column / desktop 3-4-column per K value

### Part 3 — Path III F-C inter-faction relationship surfacing (~2-3 days)

- [ ] Consume ExportFactionRelationship schema (faction_a_cluster_id + faction_b_cluster_id + relationship_type 6-enum + tension_narrative + shared_history_hook + primary_pair_intensifier)
- [ ] 6-enum {antagonist/rival/allied/neutral/mysterious/parallel} visual treatment (drax UX judgment — color/icon/badge per enum)
- [ ] Display tension_narrative (1-2 sentence per gandalf Wave 3 Seam 1 § 6) inline with faction pair
- [ ] primary_pair_intensifier surfacing for primary_faction_pair (per G-B selection)

### Part 4 — Seasonal hero spotlight slot (~1-2 days)

- [ ] Spotlight slot at top of Summary tab consuming ExportSeasonHero schema (season_hero_id + Phase 5 LLM uniform name + element + cohort)
- [ ] D-Sharpened invariance: substrate_anchored_personage NEVER surfaced (gandalf spec § 6.4 + Wave 3 Seam 1 § 10.2 Gate-2 grep audit)
- [ ] Spotlight CONTAINER ready for Dispatch H Meshy embed OR G-2-equivalent portrait OR placeholder fallback
- [ ] Composition note for Dispatch H integration (interface contract: container expects iframe child OR img child)

### Part 5 — Discipline #45 vocabulary lock + D-Sharpened verification (~0.5 day)

- [ ] Vocabulary lock: Spirit / Kit / Form / Faction throughout (no Class non-exempt)
- [ ] Grep audit post-edit (zero new #45 violations)
- [ ] D-Sharpened grep audit (substrate_anchored_personage NOT in Summary tab code per Wave 3 Seam 1 § 10.2)
- [ ] Cross-reference Dispatch G mobile blank skill tree fix (dynamic chain detection) — Summary tab uses similar dynamic schema-driven rendering

### Part 6 — Responsive + accessibility (~1-2 days)

- [ ] Mobile (<640px): vertical stack; faction cards full-width; spotlight at top
- [ ] Tablet (640-1024px): 2-column faction grid; spotlight prominent
- [ ] Desktop (≥1024px): 3-4-column faction grid + spotlight side-by-side
- [ ] Composition with Dispatch G mobile nav fixes preserved

### Closure

- [ ] Update `~/Games/reincarnated-loadout/AGENT_STATE.md`
- [ ] Build verification (tsc -b + vite build clean)
- [ ] Visual verification across breakpoints (mobile + tablet + desktop)
- [ ] Discipline #45 + D-Sharpened grep audits CLEAN
- [ ] Append completion record to this dispatch
- [ ] Commit (per Matt's per-cycle commit pattern)
- [ ] **Push pending Matt authorization per ADR-006** (loadout production-deploy; coordinate with KR for bundle if other dispatches in flight)

## Acceptance criteria

- [ ] `/summary` route operational; `/pitch` deprecated
- [ ] Faction-grouped layout displays K∈{3,4} clusters
- [ ] F-C inter-faction relationship_type surfacing with tension_narrative
- [ ] Seasonal hero spotlight slot ready (placeholder OR portrait OR Meshy iframe per fallback chain)
- [ ] D-Sharpened invariance verified (substrate_anchored_personage NEVER surfaced)
- [ ] Discipline #45 vocab-lock CLEAN
- [ ] Responsive across mobile + tablet + desktop
- [ ] Build clean
- [ ] Completion record + commit + push-authorization request

## Out of scope

- Do NOT touch Loadout/Sample/Analytics/Encounters/Court tabs (other dispatches)
- Do NOT implement Meshy embed (Dispatch H; gates on Meshy URL)
- Do NOT implement portrait generation (G-2-equivalent sidecar legolas seam)
- Do NOT modify ExportFactionCluster / ExportFactionRelationship / ExportSeasonHero schemas (star-lord seam; LOCKED)
- Do NOT enter Track C doc 47 publication (gandalf seam; not Dispatch C gate per Matt parallel firing authorization)

## Open questions for drax

- **Q-DC-1:** /pitch deprecation strategy — hard redirect to /summary vs maintain /pitch as legacy /marketing? Matt design call #2 said "if marketing page needed later, author as separate /marketing route" — your UX judgment on whether to do that NOW or defer
- **Q-DC-2:** F-C 6-enum visual treatment — color/icon/badge/text? Your UX judgment per existing visual language
- **Q-DC-3:** Spotlight slot fallback chain — placeholder vs G-2 portrait vs deferred Meshy embed? Your UX judgment + coordinate with sidecar landing timing

## References

- Matt 2026-05-27 design call #2 verbatim + 2026-05-28 parallel-firing authorization
- Drax Pattern-A response `a0a449e` + Dispatch G mobile fixes (composition)
- Doc 49 + seasonal_hero spec + path-iii spec
- ExportFactionCluster + ExportFactionRelationship + ExportSeasonHero schemas
- Wave 3 Seam 1 LLM prompts canonical `3532d76`

---

## Completion record

(append on completion)
