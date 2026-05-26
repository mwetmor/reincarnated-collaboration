# Dispatch — 2026-05-25 — rocket — v2_narrow main_weapon category-field correction

**From:** knight-rider (orchestrator)
**To:** rocket (generation seam — owns export transform shape)
**Approved by:** Matt 2026-05-25 — "I really need to see this new season's main and secondary weapons"
**Estimated effort:** ~15-30 min
**Acceptance:** v2_narrow main_weapon.category populated with correct categorical value (`melee`/`polearm`/`ranged`/`firearm`/`shield`/`tome`/`banner`/`focus`/`horn`/`talisman`) per WeaponDescriptor type; WeaponSlot renders human-readable category labels in loadout UI

---

## Context (root cause — KR empirically verified)

Loadout's WeaponSlot component at `reincarnated-loadout/src/components/WeaponSlot/WeaponSlot.tsx` consumes `weapon.category` and looks it up against `CATEGORY_LABELS: Record<string, string>` (allowed values: `melee | polearm | ranged | firearm | shield | tome | banner | focus | horn | talisman`). If lookup misses, raw category string renders.

**KR empirical inspection of v2_narrow data (post-rocket-transform):**

| Form | name | category | Issue |
|---|---|---|---|
| v2-form-000 (class_0001) | shield | `"category"` | ❌ literal "category" string |
| v2-form-007 (class_0008) | Terasawa Sadamune | `"category"` | ❌ literal "category" string |
| v2-form-024 (class_0025) | Banner with Shaft | `"banner"` | ✅ correct |
| v2-form-029 (class_0030) | Rimfire breech-loading pocket pistol | `"category"` | ❌ literal "category" string |

**Source-of-bug confirmed:** the literal string `"category"` is present in `/Users/admin/Games/reincarnated-engine/exports/v2_narrow/classes.json` direct from the engine — NOT introduced by your loadout-deployment-shape-fix transform. The substrate-binding layer emitted `main_weapon.category = "category"` as a literal-string placeholder for 24+ of 35 forms. Only the banner-category cases (correctly emitted as `"banner"`) made it through clean.

**Conjecture on engine bug:** the substrate-binding layer likely had a field-name-as-value typo OR a placeholder default that wasn't replaced for non-banner kit profiles. Discoverable but NOT in scope for this dispatch (Cycle 13 substrate-binding scope surface).

---

## What this dispatch does (TRANSFORM-SIDE CORRECTION)

Re-deploy v2_narrow to loadout with `main_weapon.category` correctly mapped from available substrate fields — WITHOUT touching engine code. The transform-side correction uses `mechanical_substrate_triple.weapon_kind` OR `mechanical_substrate_triple.weapon_mechanical_profile` (both available on every kit per L9) to derive the correct WeaponDescriptor.category value.

**Derivation rules (rocket judgment per substrate signal mapping):**

| Substrate signal | WeaponDescriptor.category |
|---|---|
| weapon_kind = "handheld_weapon" + profile hint shows ranged → `ranged` or `firearm` | drax judgment per substrate hint |
| weapon_kind = "handheld_weapon" + profile melee → `melee` or `polearm` per L9 profile distinction |
| weapon_kind = "armor_shield" | `shield` |
| weapon_kind = "banner" | `banner` (already correct) |
| weapon_kind = "accessory_handheld" + name keyword hint | `focus` / `talisman` / `horn` per archetype |
| weapon_kind = "ammo_or_consumable" or "named_template/ammo_consumable" | `ranged` (closest fit) |
| Other / ambiguous | `melee` as conservative default; flag in run log |

Alternative path (simpler if substrate signals don't cleanly map): use form `archetype_tag` field (e.g., "archer" → ranged; "polearm_soldier" → polearm; "heavy_barbarian" → melee + shield off-hand; etc.) as the category source. Rocket judgment on cleanest derivation path.

---

## Required reading

- `/Users/admin/Games/reincarnated-loadout/src/data/types.ts` lines 261-296 — WeaponDescriptor + MechanicalSubstrateTriple shape; valid category values
- `/Users/admin/Games/reincarnated-loadout/src/components/WeaponSlot/WeaponSlot.tsx` — CATEGORY_LABELS lookup table (target categorical vocabulary)
- `/Users/admin/Games/reincarnated-engine/exports/v2_narrow/classes.json` — current engine emit (has the bug)
- `/Users/admin/Games/reincarnated-loadout/data/v2_narrow/classes/class_NNNN.json` × 35 — current loadout-deployed shape (has the bug)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-05-25-engine-generation-run-provenance-manifest.md` — per-form mechanical_substrate_triple values (useful as derivation reference)

---

## Scope

- [ ] **Author transform-side correction script** (extend `scripts/v1_narrow_generation_run_2026_05_25.py` OR new small script — rocket discretion)
- [ ] **Derive correct category** per form from available substrate signals (mechanical_substrate_triple, archetype_tag, range_profile, role_orientation — rocket judgment on cleanest mapping)
- [ ] **Re-emit** `/Users/admin/Games/reincarnated-loadout/data/v2_narrow/classes/class_*.json` with corrected `main_weapon.category` field
- [ ] **Same for secondary_item.category** if present + suffers same bug
- [ ] **Spot-check 5+ representative forms** in classes.json to verify category values render correctly via WeaponSlot CATEGORY_LABELS
- [ ] **Smoke-test on loadout side:** `cd /Users/admin/Games/reincarnated-loadout && npm run build` — verify clean + Vite picks up updated JSON
- [ ] **Optionally also amend the engine-side export** at `~/Games/reincarnated-engine/exports/v2_narrow/classes.json` for historical fidelity — rocket judgment
- [ ] **Document the engine-side substrate-binding bug** in run log for Cycle 13 scope (NOT inline engine code fix — out of scope per dispatch spirit)
- [ ] **Commit + push** to loadout repo (Vercel auto-deploys to production per established pattern this session)

## Acceptance criteria

- [ ] All 35 v2_narrow class files have `main_weapon.category` ∈ {`melee`,`polearm`,`ranged`,`firearm`,`shield`,`tome`,`banner`,`focus`,`horn`,`talisman`} (zero literal `"category"` strings)
- [ ] WeaponSlot renders human-readable category labels (`Melee`, `Polearm`, `Shield`, etc.) on at least 5 spot-checked forms in built bundle
- [ ] secondary_item.category corrected if applicable
- [ ] Build clean (0 TS errors); v2_narrow modules processed
- [ ] Loadout commit pushed → Vercel auto-deploy fires
- [ ] Engine-side bug logged for Cycle 13 scope (run log entry; no engine code amendment)

## Out of scope (explicit non-goals)

- **NO engine substrate-binding code amendment** — flag for Cycle 13 scope, transform-side fix only here
- **NO Vercel CLI production-promote needed** — main-branch push auto-promotes (established this session)
- **NO new schema changes** — consume existing WeaponDescriptor type as-is
- **NO drax UI work** — WeaponSlot already consumes correctly; only data needs fixing
- **NO restructure of other 11 real seasons** — only v2_narrow needs the fix

## Open questions for rocket to resolve

- **Derivation source choice:** mechanical_substrate_triple vs archetype_tag vs hybrid — rocket judgment per data quality
- **Ambiguous-fit cases:** when substrate signal doesn't cleanly map (e.g., `accessory_handheld` + no keyword hint → `focus` or `talisman`?), rocket picks conservative default + documents
- **Engine-side mirror update:** rocket judgment whether to also update `~/Games/reincarnated-engine/exports/v2_narrow/classes.json` for historical fidelity (recommend: yes, for engine-side consistency)

## Cross-seam coordination

- **No fresh drax dispatch needed** — WeaponSlot/OffHandSlot already consume correctly; only the data needs fixing
- **No engine MIGRATION.md amendment** — transform-side correction; engine code unchanged
- **Production deploy already established** — Vercel auto-promotes main pushes this session

## References

- `agentic_orchestration/dispatches/2026-05-25-rocket-v2-narrow-loadout-deployment-shape-fix.md` (prior deployment-shape-fix dispatch with completion record)
- `agentic_orchestration/gandalf/notes/2026-05-25-engine-generation-run-provenance-manifest.md` (per-form substrate reference)
- Matt 2026-05-25 verbatim: "the weapons and gear are all from the old Yomi season for some reason. Can that be fixed? I really need to see this new season's main and secondary weapons."

---

## Sign-off

**Author:** knight-rider (orchestrator)
**Authority:** Matt 2026-05-25 weapon-visibility need + scope-doc autonomy + skip-confirmation re-auth
**Status:** FIRE — transform-side correction for v2_narrow main_weapon.category; engine-side substrate-binding bug deferred to Cycle 13

---
