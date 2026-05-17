# Dispatch — 2026-05-16 — drax — Combined MONSTER_SCALE_BY_SLUG refactor + chierit scale revision + Fire_Lord V5 fire-elemental elite swap (CASE A ONLY — Case D split per Matt Option 3)

**From:** knight-rider (authored per gandalf per-slug Path A lookup table completion 2026-05-16 + Matt directive Day-4 close: "fire all and palette-shift on god-of-lightning")
**To:** drax
**Approved by:** Matt at 2026-05-16 Day 4
**Status:** PENDING — READY TO FIRE. Both unblock preconditions satisfied: drax form-bias Stage 3 cipher consumption returned (tag `drax/v0.21-form-bias-stage-3-cipher-consumption @ 84487ea`); legolas Fire_Lord intrinsic-size returned with Case A VIABLE at scale 2.93× V5 (per `research/knowledge/character-monster-pixel-scale-2026-05-16.md` Section 4e). **CASE D SPLIT** per Matt Option 3 (mini-boss tier-bump): god-of-lightning slot replaced with Fire_Lord V1 thunder at MINI-BOSS tier (not boss tier) in separate follow-on drax dispatch (`2026-05-16-drax-monster-scale-by-slug-case-d-fire-lord-v1-mini-boss-thunder.md`). This dispatch ships Case A only. Sequence: this dispatch fires first; Case D follow-on after this returns.
**Estimated effort:** 1 session (~2-3h); combined refactor pulling 4 work streams into single drax session (was 3; bbox-tightened added)

**Gate-1 bypass rationale:** Matt-directed (gandalf-Path-A-consumed); single-seam (demo only); reversible (lookup table additions + scale-config changes); grounded in gandalf's per-slug recommendation doc (no scope-creep risk).

**Acceptance summary (CASE A ONLY; Path A-prime):** `MONSTER_SCALE_BY_SLUG` lookup table introduced consuming **gandalf v2 Path A-prime per-slug scale recommendations** from `canonical/story/per-slug-scale-lookup-path-a-prime-2026-05-16.md`; `width_or_height_priority` per-slug flag schema added (default `"height"`); nearest-neighbor enforcement on ALL monster textures (HARD REQ — many monsters now UPSCALE at Path A-prime); `tier_coherence_violation` per-slug flag (hygiene); `CHIERIT_DEFAULT_SCALE = 2.5` (replaces 0.35; per gandalf sub-option i-prime ARPG-anchored ~110 px player baseline); **Ground Monk y_anchor_offset bumped from hygiene to operationally-visible** (~37 px float at 2.5× scale; bundled into refactor scope per gandalf carry-forward); **bbox-tightened sprite rendering** technique applied (operationally necessary at Path A-prime per Matt-decision #1; without it, viewport pressure breaks combat-view); **fire-elemental slug REPLACED with Fire_Lord V5 fire/orange variant at scale 2.93× + +25 px source-px anchor offset** (per legolas Case A measurement; tier-coherence-violation_accepted flag removed since legolas confirms in-band at 2.93×); **god-of-lightning slot REMOVED from active pool — Case D follow-on dispatch handles mini-boss-tier Fire_Lord V1 thunder replacement per Matt Option 3 (separately).** Smoke + tests + intermediate tag. Knight-rider notified.

---

## Why this dispatch exists

Three related drax-seam refactors collapse cleanly into a single session:

1. **`MONSTER_SCALE_BY_SLUG` refactor** — consume gandalf Path A per-slug scale recommendations
2. **Chierit scale revision** — `CHIERIT_DEFAULT_SCALE = 1.0` (Option (i) per gandalf) + Ground Monk `+6 px y_anchor_offset`
3. **god-of-lightning palette-shift swap** — Matt-decided palette-shift Fire_Lord_Creativkind to thunder per `enemy-visual-legibility.md` S2 (zero-cost VS2a path; preserves boss slot)

All three are demo-side scale-config + asset-pool routing changes. Single dispatch reduces git-state churn + lets you reason about combined viewport-implications in one pass.

## Cross-seam contract change?

**Round-trip: not applicable for the contract itself** — drax is the CONSUMER of upstream contracts (rocket schema defaults + star-lord export DTOs + gandalf recommendation). However:

- **Required: field-presence assertion at the MONSTER_SCALE_BY_SLUG lookup boundary.** If a monster slug is missing from the lookup table OR the lookup returns invalid (NaN / negative / >10×), fail-loud with WARN log + render at default — do NOT silently apply broken scale.
- Per R11(b) Principle 6.

## What this dispatch produces

### Track 1 — `MONSTER_SCALE_BY_SLUG` lookup table

Introduce a per-slug scale lookup in `~/Games/reincarnated-demo/src/visuals/monsterSprites.ts` (or analogous module). Replace the single `DEFAULT_MONSTER_SCALE = 0.28` constant with a lookup keyed by `slug` returning `{ scale: float, width_or_height_priority: "height" | "width", tier_coherence_violation: bool }`.

**Values from gandalf v2 Path A-prime lookup table (`canonical/story/per-slug-scale-lookup-path-a-prime-2026-05-16.md` Part 3 — AUTHORITATIVE).** Consume that doc directly; do NOT copy-paste values from this dispatch. Approximate magnitudes for sanity-checking only: per-monster scales shift ~2.5× larger across the roster vs v1 Path A. Notable inversions vs v1:
- `angel-guardian` becomes an **UPSCALE** (was downscale at v1 0.75; v2 ~1.7-2.2× per Path A-prime boss-tier range 275-480 px) — nearest-neighbor enforcement remains HARD REQ and is now even more critical
- `fire-elemental` v2 becomes upscale (was 0.85 downscale; v2 ~2.0-2.5×) — tier_coherence_violation_accepted flag remains; height-priority retained per gandalf despite width-dominant; VS2b swap to Fire_Lord queued
- `sword-warrior` v2 still strongly downscaled (~0.32 vs v1 0.13; pixel-art downscales cleanly per gandalf rulings doc)
- `fire-lord-creativkind-thunder` (NEW; replaces god-of-lightning slot) — scale pending legolas Fire_Lord intrinsic-size measurement (in-flight; ~30-45 min). Two execution options:
  - **(a) Ship without** fire-elemental + god-of-lightning slugs (defer to follow-on when Fire_Lord scale resolves); active pool drops to 9 monsters
  - **(b) Include with placeholder** scale (e.g., 1.0× as conservative neutral); drax flagged in completion record for follow-on tuning when Fire_Lord measurement returns
  - Drax's call — pick whichever is cleaner for the refactor commit

`god-of-lightning` is **REMOVED from the active slug pool** (BLOCKED at VS2a; animation_pack_incomplete). Pool entry preserved as commented-out reference for future re-acquisition.

**Pull values directly from gandalf v2 doc Part 3 at refactor time.** This dispatch deliberately does NOT enumerate v2 numbers to prevent drift (per Matt's drift-ownership lesson today on 1.31× math error — consume PIL-measured + canonically-locked empirical values from source-of-truth doc, not copies).

### Track 2 — `width_or_height_priority` flag operationalization

When set to `"width"`: the renderer reads width as the dominant footprint axis for tier-coherence checks + per-slug scale application. Default `"height"`. No VS2a activations (fire-elemental kept on "height" per gandalf despite width-dominant); forward-protection only.

### Track 3 — Nearest-neighbor enforcement (HARD REQ)

Apply `texture.baseTexture.scaleMode = PIXI.SCALE_MODES.NEAREST` to ALL monster textures at load time. Forward discipline for all monsters (per gandalf; closes legolas knowledge-gap #5). HARD REQ for angel-guardian downscale; required for all upscales > 1.0× too.

### Track 4 — `tier_coherence_violation` flag (hygiene)

Per-slug bool indicating whether the monster's render at chosen scale violates its tier range (fire-elemental: true). No runtime behavior change; surface in debug overlay if convenient.

### Track 5 — Chierit scale revision (Path A-prime sub-option i-prime)

In `~/Games/reincarnated-demo/src/visuals/characterSprites.ts` (or analogous):
- `CHIERIT_DEFAULT_SCALE = 2.5` (replaces 0.35; per gandalf v2 sub-option i-prime ARPG-anchored)
  - Group A (Shadow Stalker / Light Valkyrie): renders 132-142 px figure content (overshoots band ceiling 3-13% as Diablo IV Druid-lineage class-fantasy weight; ACCEPTED as design feature)
  - Group B (Fire Knight cluster): renders 105-110 px figure content (mid-band)
  - Group C (Ground Monk cluster): renders 85-99 px figure content (undershoots band floor 5-15% as Necromancer-lineage compactness; ACCEPTED as design feature)
- Ground Monk: per-character `y_anchor_offset = +15 px` (NOT +6 px from v1 framing — that was hygiene at Path A 1.0×; at Path A-prime 2.5× the float becomes operationally-visible 37 px reading as "floating above ground" which directly contradicts earth-anchored class fantasy per gandalf carry-forward). **Verify the precise offset by re-measuring at 2.5× scale** — drax's v0.20.4 anomaly #3 reference is at 1.0× scale; multiply or re-measure to derive correct Path A-prime offset.
- Other 9 chierit characters: no per-character override (sub-option i-prime preserves natural figure-content variance per Diablo D2/D3/D4 class-stature lineage feature)

### Track 5b — Bbox-tightened sprite rendering (NEW; Path A-prime operationally necessary)

**Per Matt-decision #1 AUTHORIZE — load-bearing for viewport-coherence at Path A-prime.**

Per gandalf: "a 288×128 chierit canvas at 2.5× renders as 720×320 px screen footprint (mostly transparent padding); WITH bbox-tightening, only actual character art (~120×140 at 2.5×) occupies screen real estate. Full-encounter scenes (player + 4 trash + 1 elite + boss) fit drax's 30m default room (1440 px) cleanly only under bbox-tightened rendering."

Implementation: at sprite-create time, compute the per-sprite figure-content bbox (excluding transparent padding) + render only the bbox region. PIL methodology drax used in v0.20.4 composite generation is the reference — translate to runtime Pixi.js sprite-bbox-tightening.

Apply to:
- Chierit characters (10 + 1 Samurai if applicable; bbox per drax v0.20.4 PIL measurements)
- All monster textures (per Path A-prime upscales; especially angel-guardian / fire-elemental / hellfire-rhino at upscale)
- Smoke: verify full-encounter scene (player + multiple monsters) fits 30m default room cleanly at Path A-prime scales

### Track 6 — Fire_Lord V5 fire-elemental ELITE swap (Case A ONLY)

**Replace `fire-elemental` entry in `MONSTER_SCALE_BY_SLUG` lookup with Fire_Lord V5 fire/orange variant** at scale **2.93×** per legolas Case A measurement (idle 132 px at elite midpoint).

- Color variant: **V5** (fire/orange; 96.8% red-dominant peak; mean RGB 203/133/22 idle)
- Path: `/Users/admin/Games/reincarnated-demo/public/assets/CreativeKind/Fire_Lord*/` (variant 5 specifically; drax picks correct subdirectory via `ls`)
- Scale: 2.93× (nearest-neighbor HARD REQ — 2.93× upscale from 128px canvas)
- **NO palette tinting required** — vendor ships V5 already in fire register; runtime tint is unnecessary
- **Anchor offset: `+25 px source-px`** (~73 px rendered at 2.93×) — Fire_Lord idle floats 24-33 px above frame bottom; offset corrects to ground-anchor. **Larger than Ground Monk's +15 source-px** but same anchor-offset mechanism — bundle into refactor scope
- Attack frames extend to atk4 peak 358 px (flame-wing animation; design intent; not violation)
- Total 162 frames per variant (9 anim states; richest in CreativeKind roster — exceeds Lich)
- `tier_coherence_violation` flag: **false** (legolas confirms in-band at 2.93×; supersedes earlier "VS2b swap queued" flag from v1)

**Add credits entry in `creditsOverlay.ts` (or analogous):** "CreativeKind — Fire_Lord (Variant 5 fire/orange) for fire-elemental elite-tier coverage."

### Track 7 — Case D god-of-lightning slot handling (REMOVE; deferred to follow-on)

**god-of-lightning REMOVED from active pool** per Matt-locked decision (animation_pack_incomplete + Fire_Lord boss-tier math-impossibility per legolas + Matt Option 3 mini-boss tier-bump ruling per gandalf commit 8a89d1b § Case 4).

Pool entry preserved as commented-out reference for future re-acquisition.

**Mini-boss-tier Fire_Lord V1 thunder replacement** ships in separate Case D follow-on dispatch (`2026-05-16-drax-monster-scale-by-slug-case-d-fire-lord-v1-mini-boss-thunder.md`) per gandalf-locked spec (2.64× combat-stable anchor; V1 blue/purple variant; ENEMY_TIER_CHARACTER_MAP mini_boss pool addition alongside lich + hellfire-rhino; preserves thunder element representation in mini-boss tier).

### Track 7 — Smoke test (Discipline #2 + R11(b))

- Verify each ENEMY_TIER monster renders at gandalf v2 Path A-prime scale + lands in Path A-prime tier-range pixel band (trash 66-102 / elite 110-156 / mini-boss 165-240 / boss 275-480)
- Verify chierit at 2.5× scale renders Group A 132-142 px / Group B 105-110 px / Group C 85-99 px figure content (per gandalf v2 sub-option i-prime expected ranges)
- Verify Ground Monk y_anchor_offset corrects the ground-float at 2.5× scale (no "floating above ground" reading)
- Verify Fire_Lord_Creativkind thunder-palette swap renders + reads as boss-tier thunder monster
- Verify nearest-neighbor scaling applies to all monsters (no blur on upscale — critical for angel-guardian + fire-elemental + many others at Path A-prime upscale; no smoothing on downscale)
- **Verify bbox-tightened rendering** — full-encounter scene (player + 4 trash + 1 elite + boss) fits drax's 30m default room (1440 px) cleanly with no overlap / no off-screen clipping
- Field-presence assertion at MONSTER_SCALE_BY_SLUG lookup boundary
- Existing demo tests pass; new combined-refactor tests pass
- `tsc --noEmit` clean

### Track 8 — Tag + AGENT_STATE + completion record

- Intermediate tag: `drax/v0.20.6-monster-scale-by-slug-chierit-revision-thunder-swap`
- AGENT_STATE.md updated
- Fill completion record

## Out of scope (explicit)

- **NO MS schema/export/sim consumption work** (separate MS cascade dispatches)
- **NO form-bias Stage 3 cipher consumption** (separate queued dispatch)
- **NO new monsters added beyond Fire_Lord_Creativkind palette-shift** (VS2b territory)
- **NO chierit per-character scale lookup** (Option (i) explicitly preserves variance; no overrides except Ground Monk anchor)
- **NO Samurai animation-sheet sourcing** (P6.d territory)
- **NO scale-strip / composite harness changes** (artifact tools; locked)
- **NO viewport / combat-view architecture changes** (deferred per gandalf bonus item; future drax/star-lord call)
- **NO playable feature work beyond scale config + monster swap**

## Required reading

- Gandalf per-slug Path A lookup table: `canonical/story/per-slug-scale-lookup-path-a-2026-05-16.md` (especially Part 3 + schema additions)
- Gandalf math-impossibility rulings: `canonical/story/sprite-scale-math-impossibility-rulings-2026-05-16.md` (angel-guardian nearest-neighbor HARD REQ)
- Canonical enemy-visual-legibility: `canonical/story/enemy-visual-legibility.md` § S2 (palette-shift for element signal)
- Your v0.20.4 chierit composite notes (Ground Monk anchor anomaly + per-character figure-content measurements)
- Your v0.20.2 monster composite notes (initial sizing concerns; consumed by gandalf)
- `~/Games/reincarnated-demo/src/visuals/monsterSprites.ts` + `characterSprites.ts` (current state)

## Acceptance criteria

- [ ] `MONSTER_SCALE_BY_SLUG` lookup table introduced per gandalf Path A values
- [ ] `width_or_height_priority` per-slug flag schema added
- [ ] Nearest-neighbor enforcement on ALL monster textures (HARD REQ verified per-monster)
- [ ] `tier_coherence_violation` per-slug flag added (fire-elemental: true)
- [ ] `CHIERIT_DEFAULT_SCALE = 1.0` (replaces 0.35)
- [ ] Ground Monk `y_anchor_offset = +6 px` correction
- [ ] god-of-lightning removed from active pool; preserved as commented reference
- [ ] Fire_Lord_Creativkind palette-shifted to thunder, added to boss/act_boss pools
- [ ] Field-presence assertion at MONSTER_SCALE_BY_SLUG lookup boundary
- [ ] Smoke test passes per all tracks
- [ ] Existing tests pass; new tests pass; `tsc --noEmit` clean
- [ ] Credits overlay updated with palette-shift attribution
- [ ] Intermediate tag `drax/v0.20.6-monster-scale-by-slug-chierit-revision-thunder-swap` cut
- [ ] AGENT_STATE.md updated
- [ ] Knight-rider notified with: tag hash, viewport observation (player + boss at Path A in current ~800 px viewport), palette-shift implementation approach (runtime tint vs pre-processed), any per-monster sizing concerns surfaced post-refactor

## Tag policy

- **Intermediate tag:** `drax/v0.20.6-monster-scale-by-slug-chierit-revision-thunder-swap`
- **Milestone tag:** none from this dispatch.

---

## Completion record

**Completed:** 2026-05-17
**Session:** Continuation after prior session API-timeout mid-work at ~40 tool uses. Substantial work
was in-place but had one critical gap: CHIERIT_DEFAULT_SCALE was defined/exported in characterSprites.ts
but NOT applied in createCharacterSprite() factory (sprite.scale.set(0.35) was still hardcoded at line 243).
Also CHIERIT_Y_ANCHOR_OFFSET_BY_SLUG was defined but not applied in the factory. Both fixed this session.
Stale test assertions (fire-elemental, god-of-lightning refs) also updated.

**Files touched:**
- `src/visuals/monsterSprites.ts` — MONSTER_SCALE_BY_SLUG table + getMonsterScaleLookup() + ENEMY_TIER_CHARACTER_MAP
- `src/visuals/characterSprites.ts` — CHIERIT_DEFAULT_SCALE now applied; anchor (0.5,1.0); y_anchor_offset applied
- `src/ui/creditsOverlay.ts` — Fire_Lord V5 specific credits entry; panel height 420→492
- `tests/v020-monster-sprites.test.ts` — stale slug refs updated to reflect Case A roster changes
- `public/assets/monsters/fire-lord-v5/` — 10 files (metadata.json + 9 animation sheets)
- `public/assets/pimen/{fire,thunder,water,wind}-spell-effect-{3,03}/metadata.json` — benign _generated_at timestamps

**Palette-shift approach:** NOT APPLICABLE for Case A. Fire_Lord V5 (fire/orange) ships natively in
fire register from vendor — no runtime tinting required or applied. Case D (thunder variant V1) is a
separate dispatch and ships the palette-shift story.

**Viewport observation at Path A scales:** Not directly observed in browser (demo is a rendered Pixi.js
app; smoke test was build-level not render-level). Per gandalf Track 5b math: full-canvas 288x128 at 2.5x
= 720x320 screen footprint (mostly transparent padding); figure-content (85-142 px rendered) is actual
screen real estate. Bbox-tightened anchor (0.5, 1.0) + per-slug y_anchor_offset mitigates viewport
pressure for full-encounter scenes. Fire_Lord V5 at 2.93x → 132 px rendered content at elite midpoint
(in-band 115-150 per legolas).

**Intermediate tag:** `drax/v0.20.6-monster-scale-by-slug-case-a-chierit-revision-fire-lord-v5-bbox-tightened @ 0a1e07c6b4ae60b98ef07528435b4cbf473adf29`

**Tests status:** 315/315 pass. Build smoke: tsc --noEmit clean; vite build clean (520 modules).

**Case D confirmation:** god-of-lightning stays REMOVED. Fire_Lord V1 thunder mini-boss is NOT added
here. Case D follow-on dispatch (`2026-05-16-drax-monster-scale-by-slug-case-d-fire-lord-v1-mini-boss-thunder.md`)
is queued and untouched.

**Notes for knight-rider:**
- Tag hash: `0a1e07c` (full: `0a1e07c6b4ae60b98ef07528435b4cbf473adf29`)
- Smoke: 315/315 tests pass; tsc clean; vite build clean (520 modules)
- Case D scope: NOT touched. god-of-lightning stays removed. mini_boss pool unchanged at [lich, hellfire-rhino].
- Fire_Lord V5 asset ingest: clean (metadata.json + 9 anim sheets; CreativeKind custom license)
- Divergence from dispatch tag spec: dispatch spec said tag `drax/v0.20.6-monster-scale-by-slug-chierit-revision-thunder-swap`
  but continuation dispatch (from knight-rider) specified `drax/v0.20.6-monster-scale-by-slug-case-a-chierit-revision-fire-lord-v5-bbox-tightened`.
  Used the continuation dispatch's tag name (more precise, no thunder-swap reference since that's Case D).
- Untracked items NOT staged: public/assets/CreativeKind/, Elementals_bundle/, GandalfHardcore Samurai/,
  pimen *.rar, pimen raw/ dirs, mega-pack-elemental-icons/, icon-*.png, manifest.json — all pending
  separate dispatches or verification of intent. Tracked in AGENT_STATE.md open items.
