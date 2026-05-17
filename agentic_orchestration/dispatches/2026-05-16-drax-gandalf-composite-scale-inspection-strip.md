# Dispatch — 2026-05-16 — drax — Gandalf composite scale-inspection strip (follow-on to v0.20.1)

**From:** knight-rider (authored per gandalf request file `agentic_orchestration/gandalf/requests/2026-05-16-drax-monster-scale-screenshot-strip.md`; Matt-relayed Day 4 close)
**To:** drax
**Approved by:** Matt at 2026-05-16 Day 4 (relayed gandalf's commission with explicit endorsement framing)
**Status:** PENDING
**Estimated effort:** 1 session (~1h); harness exists from v0.20.1; this dispatch only adds a composite-layout render mode.
**Gate-1 bypass rationale:** Matt-directed (via gandalf), single-seam (demo-only), reversible (artifact generation, no production code), small scope. Per CHANGELOG rubric.

**Acceptance summary:** Single composite PNG at `agentic_orchestration/gandalf/findings/2026-05-16-monster-scale-inspection-strip.png` (≤2MB) showing 11 monster rows × (chierit player-reference column + 3 scale columns) = 44 thumbnails. Rows sorted swarm → boss tier. Each row labeled with monster name + tier; each thumbnail labeled with rendered-pixel-height numeric. Neutral background, idle frame only, no VFX. Companion notes file at `agentic_orchestration/gandalf/findings/2026-05-16-monster-scale-inspection-strip-notes.md`. Knight-rider + gandalf notified.

---

## Why this dispatch exists

Your v0.20.1 dispatch (`drax/v0.20.1-sprite-scale-strip-and-black-screen-fix @ b621af9`) delivered 6 grid PNGs split by category × scale. **Gandalf's commission needs a different artifact format** for ratio-judgment: all 11 monsters in ONE composite image, with the player chierit reference in the LEFT column of each row, so gandalf can scan the full bestiary's tier-hierarchy in one glance.

Your existing `scale-strip.html` harness at `~/Games/reincarnated-demo/src/scale-strip.ts` already wires the render path. This dispatch reuses that infrastructure with a different layout output mode.

## Cross-seam contract change?

**Round-trip: not applicable** — demo-internal artifact generation only; no schema or contract change. Per R11(b) Principle 6.

## What this dispatch produces

### Required artifact 1 — composite PNG

Path: `agentic_orchestration/gandalf/findings/2026-05-16-monster-scale-inspection-strip.png`

Layout (per gandalf's exact spec):

```
                     SCALE 0.20         SCALE 0.28         SCALE 0.35
                  ┌────────────┐    ┌────────────┐    ┌────────────┐
  [PLAYER REF]    │ goblin-    │    │ goblin-    │    │ goblin-    │
  Fire Knight     │ mage       │    │ mage       │    │ mage       │
  (chierit @ 0.35)│ (trash)    │    │ (trash)    │    │ (trash)    │
                  │ XXX px     │    │ XXX px     │    │ XXX px     │
                  └────────────┘    └────────────┘    └────────────┘
                  ... (11 rows total, ordered tier-ascending)
```

**Row order (swarm → boss; per `ENEMY_TIER_CHARACTER_MAP`):**
1. `goblin-mage` (trash)
2. `mutant-skeleton` (trash)
3. `evil-eye` (trash)
4. `sword-warrior` (trash)
5. `crystal-golem` (elite)
6. `fire-elemental` (elite)
7. `demon-mage` (elite)
8. `lich` (mini_boss)
9. `hellfire-rhino` (mini_boss)
10. `angel-guardian` (boss)
11. `god-of-lightning` (boss)

(Note: `act_boss` tier maps to same monsters as `boss`; do not duplicate rows.)

**Per-row required elements:**
- **Player reference at LEFT** — chierit Fire Knight rendered at current default scale (0.35), anchored at ground-level so it sits visually adjacent to the monster on the SAME baseline. Same player-ref repeats every row (consistent reference).
- **Monster name label** above the three scale-thumbnails
- **Tier label** below monster name (`trash` / `elite` / `mini_boss` / `boss`)
- **Per-thumbnail rendered pixel-height numeric** (e.g., `@ 0.20 → 102 px tall`; `@ 0.28 → 142 px tall`; `@ 0.35 → 178 px tall`). Measure from sprite ground-anchor to top of bounding box (full bounding box height acceptable if separating body from protrusions is impractical).

**Constraints (gandalf-locked):**
- Neutral background — single muted color (slate grey or off-white) so eye focuses on scale comparison
- Same camera distance for all three scale columns (only `DEFAULT_MONSTER_SCALE` value varies)
- Idle animation first frame — visual stability; not mid-action
- No combat VFX in frame
- Single PNG; ≤2MB file size

### Required artifact 2 — companion notes file

Path: `agentic_orchestration/gandalf/findings/2026-05-16-monster-scale-inspection-strip-notes.md`

Required content:
- Source-sheet intrinsic pixel size per monster (you know this from v0.20.1 ingest pipeline; if any are missing, flag "see Legolas commission")
- Chierit Fire Knight current scale value used as reference (you noted 0.35 in v0.20.1 completion record — confirm)
- Per-row notes on any rendering anomalies you noticed (e.g., "Crystal_Golem combined-sheet cycles all anims; idle first-frame extracted manually for this composite")
- Confirm GandalfHardcore Samurai is OUT OF SCOPE for this composite (gandalf's commission specifies the 11 ENEMY_TIER monsters, not characters)

## How to reuse the existing harness

Your `scale-strip.html` / `src/scale-strip.ts` already renders monsters at multiple scales. This dispatch needs:
1. Add a layout mode that composites all rows into a single canvas
2. Insert the chierit Fire Knight reference column at left
3. Compute + render pixel-height numerics per cell
4. Save to the gandalf/findings path (not the scale-comparison directory used in v0.20.1)

Either add a `?layout=composite` query param to `scale-strip.html`, OR add a new route like `scale-strip-composite.html`. Pick whichever is faster.

## Out of scope (explicit)

- **NO character composite.** Gandalf's commission specifies monster-only (chierit acts as reference at single current scale). The character-side 3-scale strips you produced in v0.20.1 are already on disk; gandalf may consult them separately. **Do not generate a chierit composite under this dispatch.**
- **NO new scale candidates.** Use the same 0.20 / 0.28 / 0.35 monster scales from v0.20.1. (Gandalf may request a 4th scale column AFTER seeing this composite + legolas intrinsic-size data; that's a separate follow-on dispatch.)
- **NO per-monster MONSTER_SCALE_BY_SLUG refactor.** Still gated on gandalf's recommendation table. Separate follow-on.
- **NO black-screen-related changes.** Already fixed at `f54da43`.

## Required reading

- `agentic_orchestration/gandalf/requests/2026-05-16-drax-monster-scale-screenshot-strip.md` (gandalf's full spec)
- Your own v0.20.1 dispatch + completion record (`drax/v0.20.1-sprite-scale-strip-and-black-screen-fix`)
- `~/Games/reincarnated-demo/src/scale-strip.ts` + `scale-strip.html` (harness you already built)
- `~/Games/reincarnated-demo/src/visuals/monsterSprites.ts` — `ENEMY_TIER_CHARACTER_MAP` at line 73 (sort-order source)

## Acceptance criteria

- [ ] Composite PNG at `agentic_orchestration/gandalf/findings/2026-05-16-monster-scale-inspection-strip.png` (≤2MB)
- [ ] 11 rows × 4 columns (player-ref + 3 scales); rows sorted trash → elite → mini_boss → boss
- [ ] Per-row labels: monster name + tier label
- [ ] Per-thumbnail labels: rendered pixel-height numeric
- [ ] Neutral background; idle first frame only; no VFX
- [ ] Companion notes file at `agentic_orchestration/gandalf/findings/2026-05-16-monster-scale-inspection-strip-notes.md`
- [ ] No new TS errors (`tsc --noEmit` clean)
- [ ] Existing tests pass (`npm run test`)
- [ ] Intermediate tag `drax/v0.20.2-gandalf-composite-scale-strip` cut
- [ ] AGENT_STATE.md updated
- [ ] Knight-rider notified with: composite file path, notes file path, any per-monster sizing concern surfaced during rendering

## Tag policy

- **Intermediate tag:** `drax/v0.20.2-gandalf-composite-scale-strip` at the commit producing the composite + notes file.
- **Milestone tag:** none.

---

## Completion record

**Completed:** 2026-05-16
**Composite PNG path:** `agentic_orchestration/gandalf/findings/2026-05-16-monster-scale-inspection-strip.png`
**Notes file path:** `agentic_orchestration/gandalf/findings/2026-05-16-monster-scale-inspection-strip-notes.md`
**File size:** 116.8 KB (canvas 1010 × 3159 px; well within 2MB limit)
**Intermediate tag:** `drax/v0.20.2-gandalf-composite-scale-strip @ 872891b` (demo repo)
**Tests status:** 294/294 PASS; `tsc --noEmit` clean
**Notes for knight-rider:**

Generation method was Python/PIL direct sheet extraction (not browser screenshot). Same frame-extraction logic as the existing `monsterTexture()` in `scale-strip.ts`. New file `scripts/generate-composite-strip.py` in demo repo.

Sizing concerns surfaced for gandalf review:

1. **Sword Warrior (trash)** — 280×280 frame renders at 98px @ 0.35, larger than all bosses except God of Lightning (90px). Tier-size inversion. Likely needs per-slug scale correction when MONSTER_SCALE_BY_SLUG refactor lands (still gated on gandalf's recommendation table).

2. **Evil Eye (trash)** — 64×64 frame, 22px @ 0.35 (49% of player reference height). Very small; legolas intrinsic-size data needed to determine how much is empty-frame margin vs actual body.

3. **Fire Elemental (elite)** — 192×68 frame (short/wide), 24px @ 0.35. Height metric undersells horizontal visual presence. Assessment may need a width-footprint metric rather than pure height.

4. **Demon Mage (elite)** — `row_per_anim` layout with no `row_index` set on the single "combined" animation; frame 0 extracted from row 0 of sheet. May not be true idle frame. Legolas may need to add per-animation `row_index` metadata if idle isolation is needed.

The 6 grid PNGs from v0.20.1 (`scale-comparison/monsters/`) remain on disk and are not affected. This composite adds gandalf's preferred single-image format alongside them.
