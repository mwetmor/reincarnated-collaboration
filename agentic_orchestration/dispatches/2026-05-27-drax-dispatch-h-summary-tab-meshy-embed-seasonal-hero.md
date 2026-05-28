# Dispatch — 2026-05-27 — drax — Dispatch H: Summary tab Meshy embed integration (seasonal hero spotlight; ~half-day)

**From:** knight-rider
**To:** drax (loadout/demo seam owner)
**Approved by:** Matt 2026-05-27 verbatim "Author Dispatch H — drax Summary tab Meshy embed integration (seasonal hero spotlight)"
**Estimated effort:** ~half-day drax sub-agent work
**Acceptance:** Seasonal-hero spotlight section added to Summary tab with Meshy embed iframe integration; responsive across mobile + desktop + tablet; fallback handling for embed failure; Discipline #45 vocab-lock CLEAN (Spirit / Kit / Form vocabulary; NOT "Class"); future-state Three.js R3F architectural readiness preserved (comment + structure; no impl); build clean

**Gate:** Meshy embed URL available (post Wave 5 PASS + Matt manual rigging on seasonal hero). **Composes with Dispatch C (Summary tab faction-grouped re-architecture) OR stands alone if Dispatch C delayed.**

## Quality criterion (Move 1)

**Game-quality goal this dispatch serves:** surface the Cycle 14 seasonal hero as the player-facing thematic anchor at Summary tab — animated 3D embed transforms abstract substrate-emergent identity into a tangible character figure. Composes "Engine first. Game second. Phase third." — Phase 4+5 substrate-emergent identity flows through Wave 5 H-5 hybrid curation (gandalf design-call) into player-facing 3D figure surface.

**Refutation conditions:**
- Meshy embed pattern conflicts with existing Summary tab visual language (would warrant Dispatch C composition adjustment)
- Iframe sandboxing breaks (CDN policy issues; ad blocker triggers; CSP conflicts)
- 3D embed mobile performance is unacceptable (would warrant fallback-only strategy on mobile)
- Three.js R3F architectural-readiness scope creep beyond comment+structure (Cycle 15+ deferral preserved)

## Context

**Authority chain:**
- Matt 2026-05-27 design call #1 ratified H-5 hybrid seasonal hero (substrate top-3 + gandalf curates 1)
- Gandalf seasonal_hero H-5 hybrid spec at meta `574624a` (998 lines; Q-Bundle resolved per § 4.1 Phase 4 emission + § 4.2 Phase 5 PM-2 amendment + § 4.3 Wave 5 close + § 6 drax Summary tab consumption + § 6.4 star-lord telemetry)
- Doc 49 (gandalf `67b22d7`) Summary tab player-surface design
- Wave 5 production season FIRING (gamora Option C Step 1 BLOCKED → rocket fix firing → re-fire imminent)
- Phase 6 visual coalescence remains Cycle 15+ scope for full 3D pipeline expansion (per gandalf path-iii spec); Meshy embed is Cycle 14 v1 minimal-viable visual surface

**D-Sharpened invariance:** seasonal hero is player-facing UNIFORM regardless of substrate_anchored_personage internal metadata. Embed URL + spotlight content drawn from `season_hero_id` (gandalf curation pick) + ExportSeasonHero schema (per gandalf seasonal_hero spec § 4.3). substrate_anchored_personage NOT surfaced in spotlight UI.

**Cycle 14 v1 scope:** Meshy embed for seasonal hero ONLY (1 character per season). Phase 6 visual coalescence (full 3D pipeline expansion) remains Cycle 15+.

## Required reading

- `canonical/49-loadout-sample-player-surface-design-2026-05-27.md` (Summary tab player-surface design)
- `canonical/story/seasonal-hero-h-5-hybrid-spec-2026-05-27.md` § 4.3 + § 6 (gandalf seasonal_hero spec; drax Summary tab consumption semantics)
- `agentic_orchestration/drax/notes/2026-05-27-cycle-14-tab-integration-pattern-a-response.md` § Summary tab (current state: static marketing page; Dispatch C re-architecture queued)
- `~/Games/reincarnated-loadout/src/components/Pitch.tsx` (current Summary surface; replaced by /summary route per design call #2)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § Discipline #45 (vocab lock: Spirit / Kit / Form / Faction permitted; "Class" prohibited at player-facing labels)
- `.claude/skills/reincarnated-drax-operating-procedure`

**Reference (when Meshy URL lands):**
- Meshy embed URL provided by Matt post manual rigging (after Wave 5 PASS + seasonal_hero curation pick)
- Cycle 14 lighter sidecar G-2 portraits (if landed first — fallback static portrait source)

## Discipline #46 compliance

- N/A — UI-side embed integration; no DB queries

## Discipline #42 framing-audit at session-start

- **Q1 load-bearing assumptions:**
  1. Meshy embed URL is available at fire time (gate met)
  2. Iframe-based 3D embed performs acceptably across mobile + desktop + tablet (Meshy provider-side optimization)
  3. Three.js R3F architectural-readiness is comment+structure-only scope (no React-Three-Fiber dependency added)
  4. Spotlight section composes with Dispatch C Summary tab architecture (OR stands alone at current /summary route if Dispatch C delayed)
- **Q2 refutation evidence to seek:** verify Meshy URL provided at fire time; verify iframe sandboxing semantics (CSP / sandbox attribute); verify ExportSeasonHero schema availability at fire time (gandalf curation pick produced post Wave 5 PASS)
- **Q3 outcome trigger:** if Meshy URL not available OR iframe sandboxing breaks OR mobile performance unacceptable, invoke Discipline #44 framing-refusal + surface back to KR (defer Meshy embed to Cycle 15+ alongside Phase 6 full 3D pipeline)

## Scope

### Part 1 — Seasonal-hero spotlight section (~1-2 hours)

- [ ] Author spotlight section component (e.g., `src/components/SeasonalHeroSpotlight.tsx` or per drax judgment on file structure)
- [ ] Consume `season_hero_id` from ExportSeasonHero schema (gandalf seasonal_hero spec § 4.3); access via existing loadout data layer OR fetch pattern
- [ ] Spotlight content: hero name (Phase 5 LLM uniform player-facing name) + element + cohort + relationship_type display (composes with F-C inter-faction relationships)
- [ ] D-Sharpened invariance: substrate_anchored_personage NOT surfaced in spotlight UI (engine-internal metadata only)
- [ ] Composition with Dispatch C Summary tab architecture OR standalone at current /summary route (drax judgment)

### Part 2 — Meshy embed iframe integration (~1-2 hours)

- [ ] Iframe component with Meshy embed URL (provided by Matt post manual rigging)
- [ ] Iframe sandbox attribute (security-appropriate; allow-scripts + allow-same-origin for Meshy CDN)
- [ ] Loading state UX (skeleton OR spinner while embed initializes)
- [ ] Aspect ratio preservation (typical 3D embed 16:9 OR 1:1 square; drax UX judgment)
- [ ] Test embed actually loads in browser DOM

### Part 3 — Responsive across breakpoints (~30-45 min)

- [ ] Mobile (<640px): full-width with reduced height; spotlight content stacks below embed
- [ ] Tablet (640-1024px): embed + spotlight content side-by-side OR stacked per UX judgment
- [ ] Desktop (≥1024px): hero embed prominent with spotlight content adjacent
- [ ] Verify mobile performance acceptable (3D embed CPU/GPU usage on mid-range device; consider conditional disable on slow connections)

### Part 4 — Fallback handling (~30-45 min)

- [ ] Iframe load-failure detection (onerror handler OR timeout)
- [ ] Fallback static portrait image source (Cycle 14 lighter sidecar G-2 portraits if landed first; OR placeholder image; OR text-only fallback)
- [ ] Graceful degradation: spotlight content remains visible + functional even if embed fails
- [ ] Visual messaging: subtle "3D preview unavailable; showing portrait" OR silent fallback per drax UX judgment

### Part 5 — Discipline #45 vocabulary compliance (~15 min)

- [ ] Spotlight labels use "Spirit" / "Kit" / "Form" / "Faction" vocabulary
- [ ] NO "Class" terminology in spotlight section
- [ ] Grep audit post-edit: zero new #45 violations introduced
- [ ] Composition with prior Dispatch A vocab-lock fixes (preserve)

### Part 6 — Three.js R3F future-state architectural readiness (~15 min)

- [ ] Code comment block at top of SeasonalHeroSpotlight.tsx noting Cycle 15+ R3F migration path (NO implementation; comment + structure ONLY)
- [ ] Component structure that allows future swap (iframe → R3F Canvas) without API contract change at consumer-side
- [ ] Reference Phase 6 visual coalescence Cycle 15+ scope per gandalf path-iii spec

### Closure

- [ ] Update `~/Games/reincarnated-loadout/AGENT_STATE.md`
- [ ] Build verification (tsc -b + vite build clean)
- [ ] Visual verification across mobile + tablet + desktop breakpoints (devtools + manual)
- [ ] Test fallback handling (block Meshy URL in devtools → verify fallback displays)
- [ ] Discipline #45 grep audit clean
- [ ] Append completion record to this dispatch
- [ ] Commit (per Matt's per-cycle commit pattern)
- [ ] **Push pending Matt authorization per ADR-006** (loadout production-deploy; coordinate with KR for bundle if other dispatches in flight)

## Acceptance criteria

- [ ] Seasonal-hero spotlight section added to Summary tab
- [ ] Meshy embed iframe loads + displays correctly
- [ ] Responsive across mobile + tablet + desktop
- [ ] Fallback handling functional (iframe failure → fallback displays)
- [ ] Discipline #45 vocab-lock CLEAN (Spirit/Kit/Form/Faction; NO Class)
- [ ] Three.js R3F architectural readiness preserved (comment + structure)
- [ ] Build clean
- [ ] Completion record + commit + push-authorization request

## Out of scope

- Do NOT implement React Three Fiber (Cycle 15+; comment-only architectural readiness)
- Do NOT touch Loadout/Sample/Analytics/Encounters/Court tabs (other dispatches)
- Do NOT touch Dispatch C Summary tab faction-grouped re-architecture (gated; Dispatch H composes with OR stands alone)
- Do NOT add full 3D pipeline (Phase 6 Cycle 15+)
- Do NOT modify ExportSeasonHero schema (gandalf seam; spec authoritative at `574624a`)

## Open questions for drax

- **Q-DH-1:** Spotlight section placement — at top of Summary tab as hero (recommended) vs sidebar vs other? Your UX judgment
- **Q-DH-2:** Fallback strategy — static portrait from sidecar G-2 OR placeholder OR text-only? Your judgment based on sidecar G-2 landing status at fire time
- **Q-DH-3:** Mobile 3D embed performance — load by default OR opt-in (tap-to-load) OR conditional disable on slow connections? Your UX judgment

## References

- Matt 2026-05-27 verbatim Dispatch H ratification + scope
- Gandalf seasonal_hero H-5 hybrid spec `574624a` § 4.3 + § 6
- Doc 49 (gandalf `67b22d7`) Summary tab design
- Discipline #45 vocab-lock canonical at engine `b576727`

---

## Completion record

(append on completion)
