# 2026-05-17 — drax-demo — v0.28 Hotbar readability overhaul (substrate colors + tier badges + tooltips + cooldown radial)

**Status:** QUEUED — auto-spawn after `drax/v0.27-hud-additions-potion-inventory-character-1` ships.
**Authority:** Matt L3 disposition 2026-05-17 (focused playtest test 6 son final feedback; late-game-cold cognitive-load HUD).
**Type:** Pattern B (long task) — ~1-2 hours estimated.
**Predecessor:** drax v0.27 HUD additions (in flight).
**Seam:** reincarnated-demo (Pixi.js) — UI overlay layer; no engine, simulation, or loadout work.

---

## Why this matters

Matt's son feedback after focused playtest:
> *"The skill hotbar can't be read. Since I haven't played the class from early game, I don't have the skills memorized and I don't know what they do. It would be really helpful if they had an icon/color to make it intuitive which one is my basic attack and which are class ultimates, what the elements are. These need to jump out at me when I play a class and the text is too small and there are too many skills when I jump right into end game so I need some way for this to be simple and clear to me."*

**Two readability axes embedded in the feedback:**
1. **Tier axis** — basic attack vs ultimate vs utility vs AOE (need visual differentiation)
2. **Substrate axis** — element identification (fire/water/earth/wind/lightning/holy/shadow)

Plus operational: bigger icons; reduce reliance on small text; things should "jump out."

The substrate-identity declarations the hive has been building (canonical-7) carry directly into this UI work — substrate colors derived from D20 grouping vocab give visual identity per substrate. The tier axis can be inferred from existing skill metadata (cooldown + geometry + damage profile).

This dispatch is **demo-side only with inferred categories.** The canonical skill-category taxonomy is a separate gandalf design question (queued; not blocking); drax ships with inferred categories now and the taxonomy refinement layer applies later if gandalf returns a different categorization.

---

## Required reading (in order)

1. `agentic_orchestration/hive-mind/phase-1-p1-log.md` — your v0.25 + v0.26 + v0.27 ship STATE entries (most recent)
2. `reincarnated-demo/src/main.ts` — current hotbar rendering (your v0.25 `_syncUiToScreen()` + Phase 9.3 LMB primary-pick logic + v0.26 dodge handler)
3. `reincarnated-demo/src/visuals/sprites.ts` — your v0.26 bar sizing changes
4. `reincarnated-demo/src/data/loader.ts` — season-data loader (read class/skill structure to understand what metadata fields are available per skill)
5. `reincarnated-loadout/data/vfx-manifest.json` — D20 grouping labels per substrate (`ignition`/`suffusion`/`bulwark`/`displacement`/`resonance`/`radiance`/`penumbra`); each substrate entry has a `grouping_label` field — these are the canonical substrate-identity names you'll use for color derivation
6. `canonical/story/grouping-layer-vocabulary.md` — gandalf D20 grouping-vocab v1.2 spec (substrate → grouping label mapping authoritative source)
7. `canonical/story/substrate-identity-declarations-2026-05-17.md` § iconic_register fields per substrate — register language gives mood guidance for color palette per substrate

---

## Scope (5 items)

### Item 1 (HIGH) — Substrate-colored skill icon frames/borders

**Goal:** Player glances at hotbar → recognizes substrate at-a-glance via color.

**Color palette (suggested per substrate; tune for HD-2D-conformant readability):**

| Substrate | Grouping label | Primary color | Secondary accent |
|---|---|---|---|
| Fire | ignition | red-orange (#E85D24) | bright yellow (#FFC857) |
| Water | suffusion | cyan-blue (#3B8EE0) | pale teal (#A4E2F0) |
| Earth | bulwark | brown-ochre (#8B5A2B) | moss-green (#658B3F) |
| Wind | displacement | pale-cyan (#A3D9E0) | white-grey (#D4DDE0) |
| Lightning | resonance | yellow-violet split (#F2D027 + #7A4FAB) | electric-blue (#5DC9E6) |
| Holy | radiance | gold-white (#F5D061) | bright-cream (#FFF6D6) |
| Shadow | penumbra | deep-violet (#3D2C4E) | smoke-grey (#5C5870) |

**Fix:**
- Per skill in the hotbar, render an outer frame/border in the skill's substrate color (~3-4px border thickness, depending on icon size)
- Use the skill's substrate identity (from class data; you have it via D3 archetype_tag parsing or skill metadata)
- For multi-substrate skills (hybrid_mage or physical skills with no substrate), use a neutral metallic-grey frame
- For physical-only skills (`rogue` archetype etc.), use a slate-grey frame
- Inner icon area renders the existing skill icon (or placeholder shape if no real icon)

**Verify across all 7 substrates** + hybrid + physical.

### Item 2 (HIGH) — Tier/category badge per skill

**Inferred-categorization heuristic** (NO engine changes; drax infers from skill metadata):

| Category | Inference rule |
|---|---|
| **BASIC** | Lowest-cooldown attack skill in the kit (matches v0.25 `_pickLmbSkill()` logic). Mark slot index of the lowest-CD skill. |
| **ULTIMATE** | Highest-cooldown skill in the kit (typically ≥ 12-15s cooldown; tune empirically against actual season data) |
| **AOE** | `geometry_type` ∈ {`burst`, `persistent_zone`, `ground_targeted_circle`, `ring`, `nova`, `radiant_aura`, `area_sustain`, `vortex_pull`}. If a skill is BOTH ultimate AND AOE, prefer ULTIMATE badge (higher tier). |
| **UTILITY** | No `damage_type` field, or `damage_type` ∈ {`buff`, `heal`, `dodge`, `movement`} (if such categories exist; tune to your skill data shape). Includes summoner/pet skills. |
| **STANDARD** | Default — none of the above (most skills will fall here) |

**Fix:**
- Per skill, infer one category badge from the rules above
- Render a small badge (~12-16px) in a corner of the icon (top-left or bottom-right; pick one and use consistently)
- Badge symbology suggestion:
  - **BASIC** — small dot/star (think "your bread and butter")
  - **ULTIMATE** — ornate frame around the entire icon + small "U" or crown glyph (highest visual prominence)
  - **AOE** — small spread/burst glyph (3 outward arrows or similar)
  - **UTILITY** — small wrench/gear/sparkle glyph
  - **STANDARD** — no badge (avoid over-decorating)
- Iconic shapes are placeholders; canonical iconography is a later design pass

**Visual hierarchy guidance:**
- **ULTIMATE icon should be visibly larger** than other slots (1.1-1.2x scale) and/or have a more ornate frame
- **BASIC icon** can have a subtle "preferred" marker (small glow, slightly brighter border) since it's the LMB-default
- Other slots equal size

### Item 3 (HIGH) — Cooldown radial sweep on icon

**Goal:** Player sees at-a-glance which skills are ready.

**Fix:**
- Per skill, overlay a radial sweep (pie-wedge shape) on the icon during cooldown
- Sweep starts at 12 o'clock, sweeps clockwise as cooldown progresses (D3/D4/PoE standard)
- Sweep color: semi-transparent dark grey (40-50% alpha) — desaturates the icon during cooldown without obscuring
- Sweep disappears when skill is ready (full color icon)
- Small numeric overlay (cooldown seconds remaining) optional in center of icon; or use just the radial without numbers if numbers feel cluttered

### Item 4 (MEDIUM) — Tooltip on hover

**Goal:** Reduce reliance on always-visible tiny text by surfacing skill info on demand.

**Fix:**
- On mouse hover over a skill icon, render a tooltip popup near the icon (above or to the side; auto-position to not clip off-screen)
- Tooltip contents:
  - Skill name (LLM-generated per star-lord D15; current text label)
  - Substrate (one-line text with substrate-color accent, e.g., "FIRE / ignition")
  - Tier (BASIC / ULTIMATE / AOE / UTILITY / STANDARD)
  - Geometry type (one-line, e.g., "Cone — 60° spread, 8m range" if you have the data; placeholder text if not)
  - Damage / effect summary (if available; placeholder OK)
  - Cooldown (e.g., "Cooldown: 8.0s")
  - Key binding (e.g., "Key: 3")
- Tooltip text: 12-14pt minimum (readable; not the tiny hotbar font)
- Tooltip dismisses on mouse-out

### Item 5 (MEDIUM) — Larger icons + bigger key-binding labels

**Goal:** Visual prominence; reduce text-dependence.

**Fix:**
- Increase hotbar icon size by ~30-50% over current
- Key-binding label (1-9, Q, etc.) rendered prominently on icon corner OR just below — larger, bolder font than current
- Ensure layout still fits viewport bottom (you may need to reduce inter-icon spacing slightly to accommodate larger icons)
- Verify with `_syncUiToScreen()` pinning still works
- Hotkey font: ~14-16pt minimum

---

## Out of scope (DO NOT)

- ❌ DO NOT implement engine-side skill category/tier metadata (drax infers; engine refinement is a separate later question)
- ❌ DO NOT design canonical skill-category taxonomy (that's a gandalf design surface; queued separately)
- ❌ DO NOT modify season data or engine kit composition
- ❌ DO NOT add new skill icons (use existing icons or placeholder shapes; bespoke skill iconography is a much larger asset effort)
- ❌ DO NOT touch the dodge primitive from v0.26 (canonical dodge supersedes it later per gandalf L3)
- ❌ DO NOT touch the HUD additions from v0.27 (potion/inventory/character icons)
- ❌ DO NOT extend scope to other hotbar polish (drag-to-reorder, customization UI, etc.) — surface as OBSERVATION

---

## Acceptance criteria

- [ ] Per-skill substrate-colored frame visible; all 7 substrates + hybrid + physical render distinct colors
- [ ] Tier badge per skill (BASIC / ULTIMATE / AOE / UTILITY / no badge for STANDARD) inferred from cooldown + geometry + damage metadata
- [ ] ULTIMATE icon visibly more prominent than other slots
- [ ] BASIC slot has a subtle "preferred" marker
- [ ] Cooldown radial sweep visible during cooldown; clean when ready
- [ ] Tooltip on hover shows skill name + substrate + tier + geometry + cooldown + key binding (readable font ≥ 12pt)
- [ ] Hotbar icons larger (~30-50%); key-binding labels prominent (≥ 14pt)
- [ ] `_syncUiToScreen()` viewport pinning still works
- [ ] Build clean (`npm run build`); no console errors
- [ ] Tag `drax/v0.29-hotbar-readability-overhaul-1`
- [ ] Hive-log STATE entry + OBSERVATION (any inference-heuristic edge cases noticed)

(Note: tag uses v0.29 to skip past whatever v0.28 ends up being if drax-demo runs another small intermediate ship; pick the next un-used v0.X-tag. If v0.28 is available, use that.)

---

## Smoke test expectation

1. Load demo → hotbar shows substrate-colored frames per skill
2. Hover over a skill → tooltip appears with readable text
3. Press a skill (or wait for one to cooldown naturally) → cooldown radial sweep visible during CD
4. ULTIMATE skill visibly prominent (larger icon / ornate frame)
5. BASIC skill marked subtly
6. Test across 2-3 different classes from different substrates → frame colors change appropriately
7. Verify `?mode=perception_test` still works (P7 substrate-suppression on subtitle text remains; substrate colors on icons are visual-only, not text-leak; this is a design judgment but probably acceptable since substrate "color" is part of the perception test signal, not an out-of-band identity leak — verify with Pattern P7 framing)
8. Demo build clean

---

## P7 substrate-suppression edge case

**Critical question to think through:** in `?mode=perception_test`, is substrate-colored frame an identity leak?

**Knight-rider judgment:** *colors are not labels.* The perception test asks "can subject identify mechanical/substrate distinctness from gameplay" — substrate-color framing is part of the gameplay signal (substrate identity rendered visually), not a textual label of substrate identity. D27 perception test design assumed visual VFX would render substrate (already per drax v0.26 dodge particles being element-colored). Substrate frame on hotbar is consistent with that.

**If you disagree or want to be conservative:** suppress the colored frame in perception_test mode (render neutral grey frame for all skills). Surface judgment in hive log as OBSERVATION.

---

## Hive log discipline

PRE-SIGNAL before hive-log append (per § 14.1.1). `git fetch origin` first.

---

## Tag intent

`drax/v0.28-hotbar-readability-overhaul-1` (or `v0.29-` if `v0.28` is already used) — single-commit ship preferred.

---

*Queued 2026-05-17 by knight-rider per Matt L3 disposition. Spawn after v0.27 HUD additions ship. Estimated 1-2 hours. Append completion record when done.*

---

## Completion record

**Status:** COMPLETE
**Completed:** 2026-05-17
**Agent:** drax
**Commit:** `1d49897`
**Tag:** `drax/v0.28-hotbar-readability-overhaul-1`
**Build:** tsc + vite clean (521 modules, 0 errors)

### Acceptance criteria checklist

- [x] Per-skill substrate-colored frame visible; all 7 substrates + hybrid + physical render distinct colors
- [x] Tier badge per skill (BASIC / ULTIMATE / AOE / UTILITY / no badge for STANDARD) inferred from cooldown + geometry + role metadata
- [x] ULTIMATE icon visibly more prominent (1.15x slot size, ornate double-ring frame, crown glyph)
- [x] BASIC slot has subtle "preferred" marker (brighter 3px border + top glow bar + dot badge)
- [x] Cooldown radial sweep visible during cooldown (pie-wedge from 12 o'clock CW, 48% alpha); clean when ready
- [x] Tooltip on hover shows skill name + substrate/grouping + tier + geometry + cooldown + key binding; all text >= 12pt
- [x] Hotbar icons larger (~40%: 88→124 x 70→98); key-binding labels prominent (14pt bold)
- [x] `_syncUiToScreen()` viewport pinning unchanged (container parenting identical to v0.27)
- [x] Build clean (tsc + vite, 521 modules, 0 errors)
- [x] Tag `drax/v0.28-hotbar-readability-overhaul-1`
- [x] Hive-log STATE entry + OBSERVATION (tier inference edge cases + P7 substrate judgment)

### P7 substrate judgment

Substrate frame colors are gameplay visual signal, consistent with v0.26 element-colored dodge particles. No suppression applied in `?mode=perception_test`. Per knight-rider dispatch judgment (dispatch § P7 edge case).

### OBSERVATIONs surfaced

Three inference edge cases logged in hive log:
1. `defensive` role → UTILITY (not BASIC) even for low-CD defensive skills (correct behavior; future taxonomy candidate)
2. Tied max-CD skills → `findIndex` returns first occurrence (low-priority TODO; future refinement: sort by damage_multiplier)
3. `control` role + `single_target` geometry → STANDARD badge (no CONTROL badge yet; future canon taxonomy candidate when gandalf authors skill-category taxonomy)
