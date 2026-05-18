# 2026-05-18 — drax-loadout — Loadout analytics suite iteration-1 (Track B.7)

**Authority:** Overnight sprint invocation `agentic_orchestration/gandalf/requests/2026-05-18-knight-rider-mobile-playable-analytics-visual-benchmark-sprint.md` Track B § 2.2 deliverable 7; pre-authorization matrix § 6 row 3 + row 4 (push to main triggers Vercel preview auto-deploy — safe-by-default).
**Type:** Pattern B; ~4-6 hours.
**Predecessors:** Gandalf IA dispatch landed + star-lord engine-side manifest landed + elrond catalogue-side manifest landed. Drax checks for all three before starting.
**Status:** 🟡 **QUEUED — fires after Track B prerequisites land. If Track B prerequisites are still in flight when drax-D11.5 + drax-galadriel-pipeline complete, drax pauses for them.**
**Tag intent:** `drax-loadout/v1.18-analytics-suite-iteration-1` (local; push to main triggers Vercel preview deploy — pre-authorized).

---

## Why this is the value-story deliverable

Per invocation § 0 + § 2.2: the analytics suite is the surface that *shows the value of what's been built*. The engine has shipped substrate identity, archetype diversity, LLM thematic generation, audio/VFX/tileset pipeline, mobile UX foundation. Tonight's goal is making that work *visible* in a Vercel-preview surface Matt can show to anyone.

Iteration-1 ships **something visible by morning**, not perfection. Iteration-2/3 lands later. The morning state-of-hive surfaces this preview URL as a primary value artifact alongside the demo's mobile-render captures and the benchmark report.

---

## Required reading

1. The full invocation (above) — Track B § 2.2 (especially the iteration-1 guidance)
2. **Gandalf IA:** `canonical/story/loadout-analytics-suite-information-architecture-2026-05-18.md` — **THIS IS YOUR SPEC.** Panels, visual register, route structure, Phase-1 vs Phase-2 dispositions all come from here.
3. **Data manifest:** `agentic_orchestration/research/curated/loadout-analytics-data-manifest-2026-05-18.md` (star-lord + elrond co-authored) — your data sources per panel
4. Existing loadout app patterns: `~/Games/reincarnated-loadout/src/` — components, routes, tailwind setup; the suite extends this idiom
5. `canonical/story/mobile-feel-target-doe-2026-05-17.md` § for visual-register hints (gandalf IA references this, but worth fresh re-read)

---

## Deliverable

A new route in the loadout app — likely `/analytics` or `/the-work` (gandalf IA picks the route name) — with iteration-1 components per panel.

### Implementation guidance

**Scope iteration-1 to "visible by morning, honest about what data exists":**

- Implement every Phase-1 panel from gandalf IA where data is shippable-tonight per the data manifest
- Phase-2 panels render as **explicit placeholder cards** with one-line "Phase-2: <data gap>" — DO NOT silently skip them; the absence IS part of the story-of-the-work
- Use existing loadout app's tailwind + component idiom; do NOT introduce a new design system tonight
- Type-safety: TypeScript clean (`tsc --noEmit`); existing loadout app already enforces this
- Build: vite build clean
- Data loading: prefer static-import of JSON / JSONL data files at build time over runtime fetch (iteration-1 doesn't need dynamic data; ship the data as part of the deploy)

**Visual register:** consistent with gandalf IA. Typography choices noted in IA; color palette pointers from IA. If gandalf IA leaves something unspecified, default to the existing loadout app's idiom.

**Mobile-responsive:** iteration-1 must render acceptably at 390×844 viewport at minimum. Desktop is the primary viewing context; mobile is a nice-to-have but not blocking for iteration-1.

**Data path:** the manifest tells you exactly which file lives where. Some data may be in `reincarnated-engine/output/`, some in `agentic_orchestration/research/curated/`, some in this repo (`reincarnated-loadout/data/`). For each panel:
- If data is already in loadout repo: import directly
- If data is in engine repo or research repo: import via build-time copy or symbolic-link pattern that loadout app already uses (consult existing `data/season_NNN/*.json` import pattern as template)
- If data needs derivation: small TypeScript transform at build time or in a `data/computed/` directory

### Completion criteria

- New route renders at desktop + mobile-portrait viewports
- All Phase-1 panels (per gandalf IA) shipped
- Phase-2 panels shipped as explicit placeholders
- TypeScript clean; build clean
- Tests pass (loadout app has `vitest`; existing tests pass; new tests not required for iteration-1)
- Commit pushed to main; Vercel preview URL auto-deploys; URL captured in completion record
- Hive-log STATE entry with preview URL surfaced for galadriel-workaround pipeline screenshot capture (separate downstream step)

### Out of scope

- Animations / motion design beyond Tailwind defaults
- Phase-2 panel data sourcing or derivation
- Anything beyond gandalf's iteration-1 IA scope
- Loadout-app architectural changes (new routing pattern, etc.)
- Engine-side data emission changes (consume what star-lord + elrond's manifest names; don't refactor engine to produce new data tonight)
- Touch the demo or engine
- Run the demo benchmark pipeline (galadriel-workaround does that against the preview URL post-deploy)

### HARD NOs (per invocation § 6)

- No `git push --force` to main
- No vendor acquisitions
- No CLAUDE.md or AGENTS.md modifications
- No Phase-1 P1 scope additions or cuts

## Halt conditions (per invocation § 2.2)

- Loadout app architectural conflict (new route breaks existing nav) → queue for morning; do not push the conflict
- Preview deployment fails (Vercel build error) → roll back; queue for morning with build logs
- Data file expected by manifest doesn't actually exist or has wrong shape → surface to star-lord or elrond as FRICTION in hive log; pause that panel; continue with other panels; mark the friction panel as Phase-2 in this iteration

## Completion handoff

1. Append completion record to this dispatch
2. Hive-log STATE entry (§ 14.1.1 PRE-SIGNAL discipline) with:
   - Vercel preview URL
   - List of Phase-1 panels shipped
   - List of Phase-2 placeholders shipped
   - Any halt-condition triggers + dispositions
3. Knight-rider triggers galadriel-workaround pipeline to screenshot the preview URL at desktop + tablet + mobile viewports
4. Captured screenshots land at `agentic_orchestration/galadriel/captures/2026-05-18/loadout-analytics-preview/`
5. Morning state-of-hive surfaces preview URL as primary value artifact

---

*Dispatched 2026-05-18 evening by knight-rider per overnight sprint invocation Track B § 2.2 deliverable 7. Single-night sprint cadence. Pre-authorization row 4: push to main triggers Vercel preview auto-deploy — preview URL is safe-by-default state; if CI fails, roll back and queue for morning.*
