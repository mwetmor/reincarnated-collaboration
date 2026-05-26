# Dispatch — 2026-05-25 — rocket — v2_narrow loadout deployment-shape fix

**From:** knight-rider (orchestrator)
**To:** rocket (generation seam — owns export pipeline output shape)
**Approved by:** Matt 2026-05-25 — root cause identified: loadout discovery hook + structure mismatch
**Estimated effort:** ~15-30 min
**Acceptance:** v2_narrow's 35 forms discoverable by loadout's Vite glob + visible at Vercel preview after auto-deploy

---

## Context (root cause)

Matt identified deployment-shape root cause for "old engine data displays but no v2_narrow":

1. **Discovery mechanism mismatch:** rocket deployed `v2_narrow/classes.json` + `metadata.json` to `~/Games/reincarnated-loadout/public/seasons/v2_narrow/`, but loadout's `src/hooks/useSeasonData.ts` discovers seasons via Vite `import.meta.glob` from `<repo-root>/data/*/` only (NOT from `public/seasons/`):
   - Manifest glob: `../../data/*/manifest.json` (eager: true)
   - Class glob: `../../data/*/classes/*.json` (eager: true)
2. **File-structure mismatch:**
   - `metadata.json` → must be **`manifest.json`** matching `SeasonManifest` type at `src/data/types.ts`
   - Single `classes.json` (array of 35) → must be **`classes/class_0001.json` through `class_0035.json`** (one file per class object)

**Reference existing pattern (KR empirically verified):**
- `/Users/admin/Games/reincarnated-loadout/data/season_002328/` — 10-class season with same shape v2_narrow needs at 35-class scale
- Structure: `manifest.json` + `classes/class_NNNN.json` files + optional `gear_pool.json` (NOT required; not glob'd by useSeasonData)

---

## Required reading

- `/Users/admin/Games/reincarnated-loadout/src/hooks/useSeasonData.ts` (the discovery hook — load-bearing glob patterns)
- `/Users/admin/Games/reincarnated-loadout/src/data/types.ts` — `SeasonManifest` interface (lines around the imports above; full type structure)
- `/Users/admin/Games/reincarnated-loadout/data/season_002328/manifest.json` — reference manifest shape (manifest_version "1.3" + season_id + generated_at + generation_seed + season_theme_element + anchor + elements + etc.)
- `/Users/admin/Games/reincarnated-loadout/data/season_002328/classes/class_0001.json` — reference individual class file shape
- `/Users/admin/Games/reincarnated-engine/exports/v2_narrow/metadata.json` — current rocket-emitted metadata (renames + content adjustments needed)
- `/Users/admin/Games/reincarnated-engine/exports/v2_narrow/classes.json` — current rocket-emitted 35-form array (needs splitting)

---

## Scope

- [ ] **Read SeasonManifest interface** at `src/data/types.ts` — determine exact shape required
- [ ] **Restructure metadata.json content** to match SeasonManifest:
  - Rename to `manifest.json`
  - Adjust fields as needed (`manifest_version`, `season_id` = "v2_narrow", `generated_at`, `generation_seed` = 20250525, `season_theme_element`, anchor structure, etc. — fill from existing run metadata where possible; populate placeholders for absent fields where SeasonManifest requires them; rocket judgment on field defaults that preserve semantic accuracy)
- [ ] **Split classes.json into individual class files**:
  - One `class_NNNN.json` per class object (4-digit padded numbering preserved from existing forms OR re-numbered 0001-0035 per existing season convention)
  - Match shape of `data/season_002328/classes/class_0001.json` reference (one ClassData object per file)
- [ ] **Deploy to correct path:** `/Users/admin/Games/reincarnated-loadout/data/v2_narrow/manifest.json` + `/Users/admin/Games/reincarnated-loadout/data/v2_narrow/classes/class_*.json`
- [ ] **Handle stale `public/seasons/v2_narrow/`:** rocket judgment — DELETE (cleanest) OR LEAVE inert (not glob'd; harmless). Recommend DELETE to avoid confusion in future sessions.
- [ ] **Smoke-test on loadout side:** run `npm run build` in loadout repo; verify build succeeds + Vite picks up v2_narrow season (build output should show v2_narrow modules processed)
- [ ] **Commit + push to loadout repo** per skip-confirmation re-auth — Vercel auto-deploys on push → new preview URL with v2_narrow visible
- [ ] **Optionally re-export from engine** to `~/Games/reincarnated-engine/exports/v2_narrow/` in the new manifest+classes/ shape (so engine export source matches loadout consumption shape) — rocket judgment on whether to update the engine-side export or treat loadout-side files as the canonical deployed form

## Acceptance criteria

- [ ] `/Users/admin/Games/reincarnated-loadout/data/v2_narrow/manifest.json` exists + matches SeasonManifest type
- [ ] `/Users/admin/Games/reincarnated-loadout/data/v2_narrow/classes/class_NNNN.json` × 35 files exist + match ClassData shape per existing season convention
- [ ] Loadout `npm run build` succeeds with v2_narrow included
- [ ] Loadout commit pushed → Vercel auto-deploy fires
- [ ] v2_narrow forms render at new Vercel preview URL (rocket captures URL in completion record)
- [ ] No regression on existing 11 real seasons OR sample-season

## Out of scope (explicit non-goals)

- **NO new engine code changes** — this is deployment-shape fix only
- **NO new schema changes** — consume existing ClassData / SeasonManifest types as-is
- **NO Vercel production promote** — preview-only per Q5 RATIFIED
- **NO drax UI work** — this is rocket export-shape fix; drax UI consumes the corrected shape automatically via existing useSeasonData hook
- **NO restructure of other 11 real seasons** — only v2_narrow needs the fix

## Open questions for rocket to resolve

- **manifest.json field-by-field population:** rocket judgment on what to populate for fields like `season_theme_element` (no single dominant element in v2_narrow per gandalf design-fit pass — all physical; rocket may choose `"physical"` OR a meta-flag like `"narrow_milestone"`), `anchor` (v2_narrow doesn't have a single seasonal anchor; rocket may populate with first-form anchor OR a meta-anchor entry), etc. Preserve semantic accuracy where possible; placeholder where not.
- **Class numbering:** preserve v2-form-NNN convention OR renumber 0001-0035 per existing season convention. Recommend matching existing season convention (class_0001.json style) for consistency.
- **`public/seasons/v2_narrow/` cleanup:** delete OR leave. Recommend delete.

## Cross-seam coordination

- **Loadout repo writes required** (this dispatch crosses into drax's seam territory). Rocket is the OWNER of the export-shape decision; drax's seam owns the consumption hook (already implemented). Coordination flows through existing types contract — no fresh drax dispatch needed.
- **No engine MIGRATION.md amendment** — engine export shape may or may not change per rocket judgment (see optional scope item)

## Handoff trigger (post-completion)

- v2_narrow forms visible at new Vercel preview URL → Matt + gandalf T4 post-mortem session 1 can review forms via loadout UI (design-mode toggle now load-bearing for engine-layer field visibility per drax dispatch `9acff0d`)

## References

- `agentic_orchestration/dispatches/2026-05-25-rocket-engine-generation-run-v1-narrow.md` (original v1 narrow milestone dispatch — completion record at end)
- `agentic_orchestration/gandalf/notes/2026-05-25-engine-generation-special-case-summary.md` (gandalf design-fit verdict for v2_narrow)
- Matt 2026-05-25 root-cause identification (verbatim brief in user message)

---

## Sign-off

**Author:** knight-rider (orchestrator)
**Authority:** Matt 2026-05-25 — deployment-shape fix per identified root cause; scope-doc autonomy + skip-confirmation re-auth
**Status:** FIRE — small deployment-shape fix; Vercel auto-deploys on push; T4 post-mortem session 1 readiness amplified once forms render

---
