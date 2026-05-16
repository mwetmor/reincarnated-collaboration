# Dispatch — 2026-05-14 — drax — real gear from season JSON

**From:** knight-rider
**To:** drax
**Approved by:** Matt, 2026-05-14
**Estimated effort:** 2–3 hours (implementation — investigation pre-done by knight-rider)
**Acceptance:** `/loadout` and `/sample` display real Yomi season gear — item names, tiers, rarities (including legendaries and rares), flavor text, and fit-score-based assignment are all authoritative engine output. "Gear - Synthesized" label retired.

**Prerequisite:** Star-lord must deliver `reincarnated-loadout/data/season_002328/gear_pool.json` before drax starts implementation. This dispatch is BLOCKED until that file exists. Check for it before proceeding.

---

## Context

The loadout's gear display (v0.4–v0.4.1) is entirely synthesized — drax invented gear using a deterministic hash roller and a static 19-item flavor text lookup. The engine already produces real gear with the right schema, but the Yomi season's `gear_pool.json` was never exported to the loadout repo. Star-lord is unblocking this by exporting it.

The synthesis layer should be fully retired once real data lands. When this dispatch closes, rarity distribution (40 legendary / 40 epic / 40 rare / 40 uncommon / 40 common per season), real names, real flavor text, and fit-score-based gear assignment will all come from engine output.

---

## What knight-rider already knows about the real schema

**Do not re-investigate this — start from here.**

Real gear lives in `gear_pool.json` — a flat array of 200 items per season. Schema confirmed from demo1 seasons:

```
{
  "gear_id": "gear_098580",
  "slot": "accessory",          // main_hand, off_hand, armor, accessory, etc.
  "handedness": "1h",
  "tier": "legendary",          // legendary | epic | rare | uncommon | common
  "dominant_element": "earth",  // may be null
  "power_score": 0.467,
  "name": "...",                // real item name — use this, not synthesized
  "flavor_text": "...",         // real flavor text — retire the static 19-item lookup
  "visual_prompt": "...",
  "stat_requirements": { ... },
  "fit_energy_type": {          // used for gear→character assignment
    "mana": 1.0, "rage": 0.708, "combo": 0.609, ...
  },
  "fit_range_profile": {
    "close": 0.841, "medium": 1.0, "long": 0.83
  },
  "fit_role_orientation": {
    "damage": 1.0, "control": 0.631, "hybrid": 0.914, "support": 0.442
  },
  "color_value": 363435,
  "color_palette": [ ... ],
  "color_signature": "..."
}
```

**Rarity distribution is exactly 40 of each tier** — engine produces a balanced pool. Legendaries and rares will appear naturally.

**Gear is a pool, not pre-assigned to characters.** Demo1 assigned gear to characters using fit scores. Drax must implement the same logic: for each loadout slot, pick the highest-scoring gear item from `gear_pool.json` where `slot` matches, scoring by fit against the character's energy type + role orientation. Use the same deterministic approach (hash by class+slot) so results are stable across renders.

**The current `effect_pool` / `RolledEffect` types are the wrong schema entirely** — they don't exist in the real gear JSON. Retire them.

---

## What to check first (before any code)

1. Confirm `reincarnated-loadout/data/season_002328/gear_pool.json` exists (star-lord delivers this)
2. Check a class JSON (e.g., `data/season_002328/classes/class_0001.json`) for "primary attack" field on skills — Matt asked whether this is an engine field or a UI heuristic. Note the answer in AGENT_STATE.md.

---

## Implementation targets

- **`src/data/types.ts`** — retire `GearEffectPoolEntry`, `RolledEffect`, `GearCatalog` (effect_pool shape). Replace with `GearPoolEntry` matching the real schema above. Update `SynthesizedSlot` (rename to `LoadoutSlot` or similar) to carry a `GearPoolEntry` instead of synthesized fields.
- **`src/utils/synthesizeSampleLoadout.ts`** — replace hash roller with a real fit-score selector: for each slot, find best-matching gear from `gear_pool.json` by comparing character's energy type + role orientation against item's `fit_energy_type` + `fit_role_orientation`. Keep deterministic (hash seed by class_id + slot).
- **`src/utils/formatEffect.ts`** — `stat_requirements` may replace what this was formatting. Inspect the field and update or retire accordingly.
- **`src/components/GearGrid/GearGrid.tsx`** — update to consume `GearPoolEntry`. Tier badge color now comes from real `tier` field (not derived from rarityMin heuristic). Item name from `name`. Flavor text from `flavor_text` — retire static lookup table.
- **Label** — "Gear - Synthesized" → "Gear — Yomi Season"

---

## Scope

- [x] Confirm `gear_pool.json` delivered by star-lord before starting
- [x] Check class JSON for "primary attack" field — note answer in AGENT_STATE.md
- [x] Retire `GearEffectPoolEntry`, `RolledEffect`, `effect_pool` types
- [x] Implement `GearPoolEntry` type matching real schema
- [x] Implement fit-score gear selector (replaces hash roller)
- [x] Real item names displayed
- [x] Real flavor text displayed (retire static 19-item lookup)
- [x] Real tier/rarity displayed with tier badge colors — legendaries and rares must be visible
- [x] Retire "Gear - Synthesized" label → "Gear — Yomi Season"
- [x] Verify no regressions on `/loadout`, `/sample`, `/analytics`
- [x] Deploy to Vercel preview
- [x] Tag: `v0.5-real-gear` on `main`
- [ ] Push to `origin/main` — SKIPPED: no `origin` remote in loadout repo (flagged in AGENT_STATE.md)
- [x] Update `AGENT_STATE.md` at session end
- [x] Append completion record to this dispatch file

---

## Out of scope (explicit non-goals)

- Connecting to SQLite directly — JSON is the right source for the web app
- Using seasons 001001–001005 gear data — Yomi only
- Any engine-side changes
- Skill gate bug fix — separate dispatch
- Tailwind safelist trim, CC-BY attribution, Tier 3 analytics — still queued
- UI-side skill calculations — out of scope per Matt

---

## Completion record

**Completed by:** drax
**Date:** 2026-05-14
**Commit:** `20bf305` (`v0.5-real-gear` tag on `reincarnated-loadout` main)
**Preview URL:** https://reincarnated-loadout-osl3wm67q-matthew-wetmore-s-projects.vercel.app

**Findings:**
- `role: "primary_attack"` is a real engine field on skills (not a UI heuristic). Confirmed
  from `data/season_002328/classes/class_0001.json`.
- `stat_requirements: null` for all 200 Yomi gear items — `formatEffect.ts` retired cleanly.
- Fit-score formula ported from `reincarnated-demo/src/inventory/spiritGuide.ts`:
  `fit = (energy_type × range_profile × role_orientation)^(1/3); value = power_score × fit`
- Top-fit items for most classes are legendaries (highest power scores + broad fit profiles).
  This is expected — rarer items naturally score higher.
- No `origin` remote exists in loadout repo; push step skipped. Vercel preview is the delivery artifact.

**Acceptance check:** `/loadout` and `/sample` display real Yomi season gear — item names,
tiers (full tier badge palette: legendary/epic/rare/uncommon/common), flavor text, and
fit-score-based assignment all from engine output. "Gear - Synthesized" label retired.

---

## References

- Yomi season: `season_002328`, seed 2328, anchor Yomi (Japanese underworld), theme wind→miasma, 10 classes, 200 gear items (40/tier), validation PASSED
- Real gear schema confirmed from `reincarnated-demo/public/seasons/season_001001/gear_pool.json`
- Demo1 (`reincarnated-demo/`) is the reference implementation for fit-score gear assignment
- Prior tags: `v0.4-gear-effects`, `v0.4.1-gear-display`
- Star-lord dispatch: `2026-05-14-star-lord-export-yomi-gear-pool.md`
