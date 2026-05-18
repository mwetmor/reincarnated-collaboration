# Chierit Monster Wire-In Handoff Brief — Lightning Ronin + Light Valkyrie

**Author:** elrond
**Date:** 2026-05-18
**Dispatch:** `agentic_orchestration/dispatches/2026-05-18-elrond-chierit-substrate-mapping.md`
**Authority:** Matt L3 acquisition 2026-05-18 — Lightning Ronin Full ($7.50) + Light Valkyrie Complete ($12); closes #138 monster acquisition gaps for lightning + holy non-boss substrates.
**Tag:** `elrond/v1.10-chierit-substrate-mapping-1`
**Target consumer:** drax (v1.20 chierit-monster-wiring dispatch, queued post-mobile chain)

**Companion deliverables:**
- `monster-subset-vs2a-2026-05-17.jsonl` (extended this dispatch — 1 addendum-meta row + 2 monster rows appended at lines 14-16)

---

## § 1 — TL;DR for drax

Wire **Lightning Ronin** (lightning, mini-boss tier) and **Light Valkyrie** (holy, mini-boss tier) into `monsterSprites.ts` reusing the existing chierit preprocessed sheets at `/assets/characters/lightning-ronin/sheets/` and `/assets/characters/light-valkyrie/sheets/`. Use distinct monster slugs (`lightning-ronin-monster` + `light-valkyrie-monster`) to avoid namespace collision with the player-character slugs that already consume those assets.

Both monsters add 1 mini-boss-tier substrate slot each:
- **lightning** mini-boss tier: was YELLOW (filled by thunder-shifted Fire_Lord palette only). Now: GREEN with native lightning anchor + optional 2-deep coexistence with the existing thunder-Fire_Lord (drax's call).
- **holy** mini-boss tier: was RED (only angel-guardian at boss tier). Now: GREEN with holy mini-boss → angel-guardian boss tier-progressive ladder.

Substrate coverage matrix § 6 ACQUISITION gaps both addressed; #138 closed.

---

## § 2 — Pack content audit

### § 2.1 — Lightning Ronin (Full tier, $7.50)

**Disk path:** `/Users/admin/Games/reincarnated-demo/public/assets/chierit/lightning_ronin/`

**Already preprocessed for player-character wiring at:** `/Users/admin/Games/reincarnated-demo/public/assets/characters/lightning-ronin/sheets/` (stage1 chierit pipeline output)

**Frame dimensions:** uniformly 288×128 per frame across all animations (PIL-measured 2026-05-18). Figure content ~50 px tall, ~30-50 px wide, right-of-center within the 288×128 canvas (per characterSprites.ts measurement notes lines 31-50).

**Master spritesheet:** `animations/spritesheet/lightning_ronin_full_288x128_SpriteSheet.png` at 12672×4224 (44 cols × 33 rows of 288×128 cells).

**Animation states present (34 total, frame counts PIL-measured):**

| Category | States |
|---|---|
| Human-mode core (10) | idle (10f), run (8f), 1_atk (8f), 2_atk (10f), 3_atk (19f), air_atk (8f), sp_atk (20f), defend (8f), take_hit (6f), death_cen (20f) |
| Human-mode mobility (4) | jump_full (20f), jump_up (3f), jump_down (3f), roll (8f) |
| Human-mode death variant (1) | death_uncen (20f) |
| Lightning-flavor mobility (4) | dash (13f), dash_loop (6f), lightning_dash (13f), lightning_dash_loop (6f) |
| Elemental-mode transform (2) | transform (44f human→elemental), back2human (12f elemental→human) |
| Elemental-mode core (9) | e_idle (9f), e_run (8f), e_1_atk (7f), e_2_atk (14f), e_3_atk (25f), e_sp_atk (20f), e_defend (8f), e_take_hit (6f), e_air_atk (8f) |
| Elemental-mode mobility (4) | e_air_atk_loop (3f), e_jump_full (20f), e_jump_up (6f), e_jump_down (6f) |

**Elemental Mode variants present:** YES (15 e_* states + transform + back2human). Full-tier acquisition delivers as expected.

**Lightning-specific assets:** `lightning_dash` + `lightning_dash_loop` (4-folder cluster — visible lightning crackle during dash).

**Missing/extra vs chierit standard:** Standard chierit Full pack delivers; nothing missing. `death_cen` and `death_uncen` are both present (centered + uncentered death variants — `death_cen` is the typical wire-in target per characterSprites.ts line 144).

**License attribution string:** `chierit (https://chierit.itch.io/) — CC-BY 4.0` (already in `creditsOverlay.ts` CREDITS[0] umbrella entry).

### § 2.2 — Light Valkyrie (Complete tier, $12)

**Disk path:** `/Users/admin/Games/reincarnated-demo/public/assets/chierit/light_valkyrie/`

**Already preprocessed for player-character wiring at:** `/Users/admin/Games/reincarnated-demo/public/assets/characters/light-valkyrie/sheets/` (stage1 chierit pipeline output).

**Frame dimensions:** uniformly 288×128 per frame across all main animations. Figure content ~50 px tall, right-of-center.

**Master spritesheet:** `animations/spritesheets/light_valkyrie_complete_288x128_SpriteSheet.png` at 10080×5760 (35 cols × 45 rows of 288×128 cells).

**Bonus VFX spritesheets (Complete-tier exclusive):**
- `light_projectile_96x64_SpriteSheet.png` — 672×192 = 7 frames at 96×64 (ranged-projectile VFX)
- `light_sp_atk_vfx_160x128_SpriteSheet.png` — 2880×128 = 18 frames at 160×128 (sp_atk overlay VFX)

**Bonus transition frames (1.1 addon):** `couch_to_idle_transition.png` + `idle_to_couch_transition.png` (couch-stance transition smoothing).

**Animation states present (43 total, frame counts PIL-measured):**

| Category | States |
|---|---|
| Human-mode core (10) | idle (12f), run (10f), 1_atk (9f), 2_atk (17f), 3_atk (31f), air_atk (8f), sp_atk (29f), defend (8f), take_hit (7f), death (18f) |
| Human-mode mobility (8) | dash (13f), dash_loop (6f), jump (20f), j_up_loop (3f), j_down_loop (3f), roll (8f), wall_cling (10f), wall_slide (5f) |
| Human-mode ranged/casting (2) | projectile_atk (17f), sp_atk_cast (29f) |
| Couch-stance suite (4) | couch_idle (10f), couch_defend (8f), couch_slide (5f), couch_stab (7f) |
| Climb-locomotion (4) | ladder_climb_back (8f), ladder_climb_side (8f), ledge_climb (9f), ledge_cling (12f), rope_climb (8f) |
| Elemental-mode transform (2) | transform (35f), back2human (18f) |
| Elemental-mode core (10) | e_idle (14f), e_move (8f), e_1_atk (10f), e_2_atk (12f), e_3_atk (17f), e_air_atk (8f), e_sp_atk (21f), e_sp_atk_loop (12f), e_defend (8f), e_take_hit (6f) |
| Elemental-mode flight (2) | e_up_loop (3f), e_down_loop (3f) |

**Elemental Mode variants present:** YES (14 e_* states + transform + back2human). Complete-tier acquisition delivers full elemental + flight + couch + climb suite as expected.

**Holy-specific bonuses:**
- Native ranged projectile + projectile VFX spritesheet (light_projectile_96x64) — drax can wire as holy ranged-attack VFX (resolves the engine's current procedural-fallback for holy multi_projectile geometry).
- sp_atk dedicated VFX overlay (light_sp_atk_vfx_160x128) — drax can layer as holy ultimate VFX.

**Missing/extra vs chierit standard:** Complete tier delivers as expected; nothing missing. Note that `death` is the only death animation (no `death_cen`/`death_uncen` split as in Lightning Ronin).

**License attribution string:** `chierit (https://chierit.itch.io/) — CC-BY 4.0` (same umbrella entry as Lightning Ronin).

---

## § 3 — Manifest extension (where in monsterSprites.ts)

### § 3.1 — Tier-routing additions

Append to `ENEMY_TIER_CHARACTER_MAP` (`monsterSprites.ts` line 403-417):

```typescript
'mini-boss': ['lich', 'hellfire-rhino', 'fire-lord-creativkind-thunder', 'golem',
              'lightning-ronin-monster', 'light-valkyrie-monster'],
mini_boss:   ['lich', 'hellfire-rhino', 'fire-lord-creativkind-thunder', 'golem',
              'lightning-ronin-monster', 'light-valkyrie-monster'],  // underscore alias
```

**Recommendation:** Append to existing arrays (3-deep → 5-deep mini-boss pool). DO NOT retire `fire-lord-creativkind-thunder`; let it coexist with `lightning-ronin-monster` as 2-deep lightning mini-boss pool (palette-shifted Fire_Lord + native chierit Lightning Ronin). Round-robin within tier naturally gives variety.

### § 3.2 — Element-flavor preferences

Append to `ELEMENT_PREFERRED_SLUG` (`monsterSprites.ts` line 427-442):

```typescript
// chierit additions (drax/v1.20 — elrond elrond/v1.10 manifest)
lightning: 'lightning-ronin-monster',  // mini-boss native lightning (overrides thunder→fire-lord-thunder pref;
                                       // both remain in mini-boss pool for variety)
holy:      'light-valkyrie-monster',   // mini-boss native holy (was no holy entry in this table)
```

**Consider:** The current `thunder: 'fire-lord-creativkind-thunder'` entry coexists with the new `lightning: 'lightning-ronin-monster'` entry — engine D19+ uses 'lightning' but the project keeps both keys for back-compat per characterSprites.ts lines 116-120. Add both `lightning` AND `thunder` entries that both resolve to `lightning-ronin-monster` for canonical-7 consistency.

### § 3.3 — MONSTER_SCALE_BY_SLUG entries

Append after the CraftPix Phase A block (`monsterSprites.ts` line ~285):

```typescript
// ── chierit monsters (drax/v1.20-chierit-monster-wiring) ─────────────────────
//
// Source-of-truth: elrond manifest 2026-05-18 (monster-subset-vs2a-2026-05-17.jsonl
// chierit addendum rows). Frame canvas 288×128 (figure content ~50 px tall right-of-center).
// Path A-prime mini-boss band: 173-230 px content; midpoint 201 px.
// Canvas-relative scale 201/128 = ~1.57× from canvas-height OR figure-content scale ~4.0×.
// Chierit player baseline at 2.5× renders ~125 px elite midpoint; mini-boss requires bigger.
// nearest_neighbor HARD REQ — chierit pixel-art register must hold.
//
// Recommendation: start at scale 1.57 (canvas-relative; consistent with how characterSprites.ts
// computes; sprite.anchor.set(0.5, 1.0) per chierit ground-anchor convention).
// y_anchor_offset starts at 0 (chierit figures are canvas-bottom-anchored per characterSprites.ts
// note line 76); visual inspect at runtime and tune per slug.

'lightning-ronin-monster': {
  // mini-boss; 288×128 frame; lightning element; chierit Lightning Ronin Full.
  // Rendered target: ~201 px content (mini-boss midpoint).
  // canvas-relative scale 1.57× → rendered canvas 452×201; figure content 1.57×50 = ~78 px (BELOW band).
  // RECOMMEND increasing scale to ~3.5-4.0× to lift figure content into 173-230 band.
  // First-cut: scale 4.0 → figure 200 px (mini-boss midpoint). Visual inspect required.
  scale: 4.0,
  width_or_height_priority: 'height',
  tier_coherence_violation: false,
  y_anchor_offset: 0,  // TBD visual-inspect; chierit figures canvas-bottom-anchored per characterSprites.ts
},
'light-valkyrie-monster': {
  // mini-boss; 288×128 frame; holy element; chierit Light Valkyrie Complete.
  // Same scale family as Lightning Ronin (288×128 canvas → 4.0× → 200 px figure).
  // Valkyrie has flight states (j_up_loop / j_down_loop) — drax may want positive y_anchor_offset
  // to lift sprite slightly (gives air-presence) OR use ground state during combat.
  scale: 4.0,
  width_or_height_priority: 'height',
  tier_coherence_violation: false,
  y_anchor_offset: 0,  // TBD; may bump to +8 to +12 for hover air-presence
},
```

**Sanity check the math:** the chierit player baseline `CHIERIT_DEFAULT_SCALE = 2.5` (characterSprites.ts line 253) renders figure content at ~125 px (elite midpoint). For mini-boss tier (~200 px midpoint) we need scale ≈ 4.0× (160% of player). At 4.0× the canvas occupies 1152×512 — within viewport per existing precedents (fire-lord-v5 at 2.93× from 128 canvas renders 376×376; chierit at 4.0× from 288×128 renders 1152×512 — wider footprint but viewport-compatible).

Drax must visual-inspect at runtime; recommend 0.75-step adjustments if the figure undershoots/overshoots.

### § 3.4 — Per-monster `metadata.json`

Recommended file: `/assets/monsters/lightning-ronin-monster/metadata.json` (and symmetric for `light-valkyrie-monster`):

```json
{
  "monster_slug": "lightning-ronin-monster",
  "display_name": "Lightning Ronin",
  "vendor": "chierit",
  "vendor_url": "https://chierit.itch.io/",
  "license": "CC-BY-4.0",
  "license_url": "https://creativecommons.org/licenses/by/4.0/",
  "pack": "Elementals_Lightning_Ronin_Full_v1.0",
  "tier": "mini-boss",
  "element_flavor": "lightning",
  "register": "hd-2d-pixel",
  "pattern": "C-chierit",
  "layout": "strip",
  "frame_w": 288,
  "frame_h": 128,
  "_sheet_source_note": "Sheets sourced from /assets/characters/lightning-ronin/sheets/ (chierit stage1 pipeline output — same physical assets as the player Lightning Ronin character). Distinct monster slug for tier-routing namespace separation.",
  "animations": {
    "idle":    {"sheet_path": "../../characters/lightning-ronin/sheets/idle.png",       "sheet_w": 2880, "sheet_h": 128, "frame_count": 10, "frame_w": 288, "frame_h": 128, "layout": "strip"},
    "walk":    {"sheet_path": "../../characters/lightning-ronin/sheets/run.png",        "sheet_w": 2304, "sheet_h": 128, "frame_count": 8,  "frame_w": 288, "frame_h": 128, "layout": "strip"},
    "attack":  {"sheet_path": "../../characters/lightning-ronin/sheets/1_atk.png",      "sheet_w": 2304, "sheet_h": 128, "frame_count": 8,  "frame_w": 288, "frame_h": 128, "layout": "strip"},
    "hurt":    {"sheet_path": "../../characters/lightning-ronin/sheets/take_hit.png",   "sheet_w": 1728, "sheet_h": 128, "frame_count": 6,  "frame_w": 288, "frame_h": 128, "layout": "strip"},
    "death":   {"sheet_path": "../../characters/lightning-ronin/sheets/death.png",      "sheet_w": 5760, "sheet_h": 128, "frame_count": 20, "frame_w": 288, "frame_h": 128, "layout": "strip"},
    "casting": {"sheet_path": "../../characters/lightning-ronin/sheets/sp_atk.png",     "sheet_w": 5760, "sheet_h": 128, "frame_count": 20, "frame_w": 288, "frame_h": 128, "layout": "strip"}
  },
  "_generated_at": "2026-05-18T00:00:00Z",
  "_pipeline_version": "v1.20",
  "_dispatch_ref": "drax/v1.20-chierit-monster-wiring",
  "_elrond_manifest_ref": "agentic_orchestration/research/curated/monster-subset-vs2a-2026-05-17.jsonl (chierit-lightning-ronin-monster row)"
}
```

**Note on `sheet_path` cross-folder reference (`../../characters/...`):** This is the PREFERRED reuse pattern — zero new disk; the player Lightning Ronin sheets ARE the monster Lightning Ronin sheets. The `monsterSprites.ts` loader builds the sheet URL as `${MONSTERS_BASE}/${slug}/${sheet_path}` — relative paths resolve naturally. If drax's loader doesn't tolerate relative `../../` in URL resolution, fallback is symlink: `ln -s /Users/admin/Games/reincarnated-demo/public/assets/characters/lightning-ronin/sheets /Users/admin/Games/reincarnated-demo/public/assets/monsters/lightning-ronin-monster/sheets`.

Light Valkyrie metadata.json is symmetric — substitute slug + animation frame counts from § 2.2.

**Light Valkyrie projectile + sp_atk VFX:** Optionally wire as separate Pixi.js sprite resources in `spriteVfx.ts` or a new chierit-vfx module — these are 96×64 and 160×128 spritesheets not bound to the monster sprite anchor. Drax decides whether to wire in v1.20 (clean) or defer to a separate v1.21 holy-VFX-completion dispatch.

### § 3.5 — Animation state machine mapping

Recommended `idle`/`walk`/`attack`/`hurt`/`death`/`casting` mappings (the existing `MonsterAnimState` machine, `monsterSprites.ts` line 446):

| State | Lightning Ronin | Light Valkyrie |
|---|---|---|
| `idle` | `idle` (10f) | `idle` (12f) |
| `walk` | `run` (8f) | `run` (10f) |
| `attack` | `1_atk` (8f, basic sword) | `1_atk` (9f, basic spear) |
| `hurt` | `take_hit` (6f) | `take_hit` (7f) |
| `death` | `death_cen` (20f, centered) | `death` (18f) |
| `casting` | `sp_atk` (20f, lightning special) | `sp_atk_cast` (29f, holy charge — projectile-VFX-compatible) |

**Alt attack swap candidates (drax may map to alternate-attack pool):**
- Lightning Ronin: `2_atk` (10f, mid-swing), `3_atk` (19f, multi-hit chain) — could drive attack variety per encounter.
- Light Valkyrie: `projectile_atk` (17f, ranged) — natural fit if drax wires the projectile sprite alongside; gives holy substrate a real ranged-attack archetype.

---

## § 4 — Elemental Mode wire-now-vs-Phase-2 recommendation

**Recommendation: SKIP for VS2a wire-in (v1.20). DEFER Elemental Mode to Phase-2 polish (v1.21+).**

**Rationale:**
1. **Combat state machine fit:** the current `MonsterAnimState` (idle/walk/attack/hurt/death/casting) is 6 states. Elemental Mode introduces a transform-trigger + secondary state machine (e_idle/e_run/e_1_atk/e_2_atk/e_sp_atk/e_defend/e_take_hit/e_air_atk + transform + back2human). This is a feature-class addition, not a wire-in delta.
2. **Activation logic absent:** transform should fire on a combat trigger (HP threshold? cast cooldown? enrage timer?). No engine-side activation semantics exist for monster mode-shift. Defining + integrating that is a design conversation (Gandalf-domain), not a wiring task.
3. **Visual polish bandwidth:** transform itself is 35-44f one-shot anim (1.5-1.8 seconds at chierit's 12 fps). Worth the polish but requires animation-coordination engine support that doesn't currently exist for monsters.
4. **VS2a scope discipline:** the chierit-monster-wiring dispatch is a substrate-gap-close. Adding Elemental Mode as a v1.20 scope-creep risks slipping the substrate-gap-close.

**Phase-2 candidate scope (v1.21+):**
- Define monster Elemental Mode activation trigger (HP < 50% recommended starting point).
- Add `e_*` animation states to monster metadata + state machine.
- Wire transform animation as a one-shot interrupt (other states pause, transform plays, then e_idle takes over).
- Consider an elemental-mode VFX aura overlay on the monster sprite.
- Surface for Matt review when v1.20 ships and Phase-2 polish bandwidth opens.

---

## § 5 — Light Valkyrie atk.png GPU upload investigation cross-reference

**Context:** drax v1.16.2 (audio-fix-plus-holy-vfx-black-rect dispatch, completed 2026-05-18 per dispatch line 142-150) closed Bug 2 (Starcaller VFX activation gap) but Bug 1 (black-rect-on-each-holy-cast) root-cause remained UNIDENTIFIED through static analysis. Two hypotheses remain:

1. **Pixi v7 WebGL artifact** from `light-valkyrie atk.png` rendering BEFORE its GPU texture upload completes (one-shot async race condition).
2. **Pixi batching collision** between holy color palette and the default WebGL texture slot.

**During v1.20 chierit-monster wiring, drax should investigate hypothesis (1):**

**Recommended verification steps:**
- **File path verification:** open `/Users/admin/Games/reincarnated-demo/public/assets/characters/light-valkyrie/sheets/1_atk.png` (it's `1_atk`, not `atk` — the existing chierit pipeline strips numeric prefixes only when source folder has no prefix; light-valkyrie source has `05_1_atk` → `1_atk.png` per characterSprites.ts lines 139-141). Verify file is on disk and not corrupt.
- **Texture preload opportunity:** during `light-valkyrie-monster` monster-sprite creation, EAGERLY call `BaseTexture.from(sheetUrl)` for the attack sheet at sprite instantiation rather than lazily on first state transition to 'attack'. The chierit player-character sprite (characterSprites.ts line 222) does lazy texture loading via `BaseTexture.from(sheetUrl)` inside `textureForFrame()`; if the monster wire-in mirrors this pattern, the same race-condition could surface in monster context.
- **Test reproduction:** spawn a `light-valkyrie-monster` mini-boss encounter and observe whether the same black-rect artifact appears on its first `1_atk` cast. If yes → confirmed Pixi v7 WebGL pre-upload artifact, fix is `BaseTexture.from(sheetUrl)` eager call at monster instantiation. If no → suggests the artifact is specific to the player-sprite render path or the Starcaller VFX overlay, not the underlying atk.png itself.
- **Document findings:** drax v1.20 completion record + cross-reference v1.16.2 dispatch findings doc for closure.

**Coordination note:** the Light Valkyrie monster wire-in creates a SECOND consumer of `1_atk.png` (the player Light Valkyrie character is the first). If both consumers can be loaded simultaneously (player + monster in same scene), texture sharing via `BaseTexture.from(sheetUrl)` cache should work correctly (Pixi caches by URL). But the FIRST load triggers GPU upload; both consumers wait for it. This is a benign sharing pattern unless one consumer's anchor / blend-mode / shader differs from the other (unlikely).

---

## § 6 — Attribution credit

**chierit attribution is already in place:** `creditsOverlay.ts` CREDITS[0] entry:
```typescript
{
  label:       'Character sprites — Elementals',
  attribution: 'by chierit',
  license:     'CC-BY 4.0',
  url:         'https://chierit.itch.io/',
}
```

This umbrella entry **legally satisfies CC-BY 4.0 attribution obligation** for both player AND monster wirings of the chierit Elementals pack.

**Recommendation for in-game clarity:** add a SECOND CREDITS entry surfacing the dual-use as monsters:

```typescript
{
  // drax/v1.20-chierit-monster-wiring: Lightning Ronin + Light Valkyrie wired as
  // mini-boss-tier monsters (lightning + holy substrates). Same chierit Elementals pack
  // as the player characters above. Dual-use credit for in-game clarity.
  label:       'Monster sprites — Lightning Ronin + Light Valkyrie',
  attribution: 'by chierit',
  license:     'CC-BY 4.0',
  url:         'https://chierit.itch.io/',
},
```

**`credits.txt` note:** the file at `/Users/admin/Games/reincarnated-demo/public/credits.txt` is currently AUDIO-only. The visual-asset attribution surface is the F1 in-game overlay (`creditsOverlay.ts`). No `credits.txt` modification is required for chierit monsters (the audio-only file scope is unchanged).

---

## § 7 — Test plan

**Smoke verification after drax v1.20 wiring:**

1. **Mini-boss encounter spawn (lightning):** trigger an encounter that should resolve to lightning mini-boss tier (encounter element=lightning, wave-5 mini-boss slot). Expected: `lightning-ronin-monster` resolves via `ELEMENT_PREFERRED_SLUG` lookup; sprite renders at mini-boss scale; idle animation cycles.
2. **Mini-boss encounter spawn (holy):** trigger encounter element=holy, wave-5 mini-boss slot. Expected: `light-valkyrie-monster` resolves; sprite renders; idle cycles.
3. **Combat sequence (both):** observe full attack → take_hit → death state transitions. Verify no animation glitches, no anchor jumps, no black-rect artifacts.
4. **2-deep mini-boss pool variety (lightning):** spawn multiple lightning mini-boss encounters across seeds. Expected: round-robin between `fire-lord-creativkind-thunder` and `lightning-ronin-monster` (visual variety).
5. **Substrate coverage check:** verify the engine's `monsterSprites.ts` resolution path for `(lightning, mini-boss)` and `(holy, mini-boss)` no longer falls through to procedural archetypeRenderer primitives.
6. **Light Valkyrie atk.png black-rect investigation:** observe the FIRST holy combat cast after a fresh load. Compare to v1.16.2 baseline. Capture findings in v1.20 completion record.
7. **No regression on player-character rendering:** spawn a Lightning Ronin player or Light Valkyrie player encounter. Verify player-character rendering unaffected (asset sharing should be clean).

**Acceptance:** if all 7 smoke checks pass and no black-rect on cast (test 6), v1.20 ships clean. If test 6 still surfaces the artifact, log findings + cross-reference v1.16.2 for next investigation cycle.

---

## § 8 — Coverage matrix update preview

For elrond's next pass post-drax-v1.20-completion, the coverage matrix evolves:

| Substrate | Before (post-v1.14) | After (post-v1.20) | Change |
|---|---|---|---|
| **lightning** | YELLOW (mini-boss only via fire-lord-thunder palette-shift) | GREEN (mini-boss native + palette-shifted 2-deep) | +1 (native anchor) |
| **holy** | YELLOW (boss only via angel-guardian) | GREEN (mini-boss + boss tier-progressive) | +1 |

Remaining matrix RED/YELLOW after this:
- holy trash/elite (MEDIUM — future acquisition; chierit lower tiers? or vendor crawl)
- lightning trash/elite (LOW — genre-rare at low tiers)
- wind boss (LOW-MEDIUM)
- physical boss (LOW-MEDIUM)
- shadow full-boss (LOW)

#138 monster acquisition gaps CLOSED for lightning + holy non-boss substrates per Matt L3 2026-05-18.

---

## § 9 — Out of scope for elrond v1.10 (DO NOT)

- No wiring (drax v1.20 seam — separate dispatch).
- No sprite preprocessing (the chierit stage1 pipeline already produced `/assets/characters/<slug>/sheets/` — drax reuses these).
- No drax v1.18 WSP wire-in or mobile audit pre-empt.
- No other monster manifest row modification.
- No tag push (ADR-006).

---

*Brief authored 2026-05-18 by elrond per dispatch + Matt L3 acquisition. Companion to monster-subset-vs2a manifest chierit addendum rows. Drax v1.20 chierit-monster-wiring dispatch may consume this brief directly.*
