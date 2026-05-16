# Dispatch — 2026-05-14 — drax — loadout gear effects

**From:** knight-rider
**To:** drax
**Approved by:** Matt, 2026-05-14 (Day 1 kickoff)
**Estimated effort:** 1–2 hours
**Acceptance:** `/loadout` and/or `/sample` routes display rolled effects from `effect_pool` on base items — not just the base item name/icon. A player browsing a weapon should see its affixes.

---

## Context

The loadout app (`https://reincarnated-loadout.vercel.app`) reached `v0.3.3-sample-gear` with synthesized gear items rendered by class affinity and game-icons.net SVGs. The real engine catalog data is present in the repo — but the renderer reads only base item fields and does **not** read `effect_pool`. Matt flagged this 2026-05-13: players see a blank or incomplete picture of what their gear actually does.

This is a pure presentation fix in your seam. No engine changes, no schema changes, no cross-seam coordination required.

---

## Required reading before starting

1. `AGENT_STATE.md` (create one at `reincarnated-loadout/AGENT_STATE.md` — this is your first session)
2. The existing gear card component(s) — find where base item data is rendered and where `effect_pool` is not yet consumed
3. The engine-generated catalog JSON used by the loadout (identify the shape of `effect_pool` entries)
4. `agentic_orchestration/AGENTS.md` §4 Tactic 3 — format for `AGENT_STATE.md`

---

## Scope

- [ ] Locate the component(s) that render gear items in `/loadout` and `/sample`
- [ ] Confirm the shape of `effect_pool` in the catalog JSON (document in AGENT_STATE.md)
- [ ] Render rolled effects beneath / alongside the base item — format is your call (pill tags, bulleted list, etc.), but must be readable on mobile
- [ ] Verify no regressions on existing routes (`/loadout`, `/sample`, `/analytics`)
- [ ] Smoke-test locally before deploying
- [ ] Deploy to Vercel (preview URL is fine; prod promotion is Matt's call)
- [ ] Tag: `v0.4-gear-effects` on `main`
- [ ] Create `reincarnated-loadout/AGENT_STATE.md` at session end

---

## Out of scope (explicit non-goals)

- Tailwind safelist trim — separate work item, don't touch
- CC-BY attribution footer — separate work item
- Tier 3 analytics (remaining 3 charts) — separate work item
- Any engine-side changes
- Adding a git remote (separate item)

---

## Open questions for drax to resolve

- How to display `effect_pool` entries cleanly: are they already human-readable strings, or do they need formatting? Inspect the catalog JSON and decide; note the decision in AGENT_STATE.md.
- Mobile layout: do effects wrap under the base item, or in a collapsible? Pick whatever reads cleanly on a 375px screen.

---

## References

- Handoff note: `agentic_orchestration/skill_handoff_2026-05-13.md` §drax
- Current production tag: `v0.3.3-sample-gear`
- Live URL: `https://reincarnated-loadout.vercel.app`

---

## Completion record

**Completed:** 2026-05-14
**Tag shipped:** `v0.4-gear-effects` on `main`
**Preview URL:** https://reincarnated-loadout-3q2sppuw8-matthew-wetmore-s-projects.vercel.app
**Prod promotion:** Matt's call (pending review of preview)
**AGENT_STATE.md written:** yes — `reincarnated-loadout/AGENT_STATE.md` created

**Files changed:**
- `src/data/types.ts` — `GearEffectPoolEntry`, `RolledEffect` interfaces; `GearCatalog` now includes `effect_pool`; `SynthesizedSlot` now carries `rolledEffects`
- `src/utils/formatEffect.ts` — new formatter: `RolledEffect` → human-readable string (e.g., "Fire Damage on hit (562)")
- `src/utils/synthesizeSampleLoadout.ts` — deterministic hash roller picks 1–2 compatible effects per item from `effect_pool`
- `src/components/GearGrid/GearGrid.tsx` — violet Nfx badge on filled cells; FlavorTip modal now lists rolled effects

**Design decisions made:**
- Effects are machine-readable → formatted via lookup tables, not raw field names
- Mobile layout: badge in grid cell + full list on tap (FlavorTip modal); no layout restructure; works at 375px
- Rolls are deterministic by `hashStr(itemId + displaySlot)` — stable across renders/reloads

**Notes for follow-on (queued, not blocking):**
- Skill gate bug: gates open per total tree points (5+5=all open); should be per-chain — separate dispatch
- "Primary attack" label: source unclear (engine field vs. lowest-cooldown heuristic); drax to clarify in next session
