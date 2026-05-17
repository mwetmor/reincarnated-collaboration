# Dispatch — 2026-05-16 — drax — MONSTER_SCALE_BY_SLUG Case D — Fire_Lord V1 mini-boss thunder (god-of-lightning Option 3 tier-bump)

**From:** knight-rider (authored per Matt directive Day-4 close: Option 3 mini-boss tier-bump locked; gandalf commit 8a89d1b § Case 4 re-amendment provides scale + slot-routing spec)
**To:** drax
**Approved by:** Matt at 2026-05-16 Day 4
**Status:** QUEUED — fires after Case A dispatch (`2026-05-16-drax-monster-scale-by-slug-refactor-plus-chierit-scale-revision.md`) returns. Per-seam one-dispatch-per-session discipline.
**Estimated effort:** ~1h drax; small Case A follow-on — single per-slug add + ENEMY_TIER pool routing change + credits entry + smoke

**Gate-1 bypass rationale:** Matt-directed (Option 3 explicitly locked); single-seam (demo only); gandalf-locked spec (2.64× scale + V1 variant + mini-boss routing); reversible (slot-routing change + lookup add).

**Acceptance summary:** `MONSTER_SCALE_BY_SLUG` lookup gains `fire-lord-creativkind-thunder` entry at scale **2.64× combat-stable anchor** + V1 (blue/purple variant; no tinting). `ENEMY_TIER_CHARACTER_MAP` `mini_boss` pool adds `fire-lord-creativkind-thunder` alongside `lich` (necrotic) + `hellfire-rhino` (fire) → mini-boss tier becomes necrotic + fire + thunder diversity. `boss` / `act_boss` pools stay `angel-guardian`-only (VS2a-acceptable per gandalf framing). Credits entry. Smoke verifies render at scale + tier-routing + nearest-neighbor + anchor. Tag.

---

## Why this dispatch exists

Per gandalf commit `8a89d1b` § Case 4 re-amendment + Matt Option 3 lock:

> Mini-boss tier-bump. Three reasons: (1) Thunder element retains monster representation; (2) Boss-tier diversity loss is acceptable for VS2a; (3) Zero acquisition cost; ships clean; preserves Fire_Lord asset utility across the roster (V5 elite + V1 mini-boss).

Per legolas Fire_Lord measurement (Case D math impossibility flagged for boss tier; Fire_Lord architecturally elite/mini-boss-sized at 128×128 canvas + 45 px idle content):
- Boss tier (Path A-prime 287-460 px) requires scale 8.22× (viewport-infeasible) OR 3.03× (idle reads elite, not boss) OR 2.35× best-achievable (tier-coherence violation accepted)
- **Mini-boss tier (Path A-prime 66-88 px) requires scale ~1.5-2.0× to land idle in band** — viable; no math impossibility

Gandalf's Case 4 re-amendment derived the specific value: **2.64× combat-stable anchor.** Combat-stable Fire_Lord content (76 px at atk3 sustained) at 2.64× = ~200 px rendered, which anchors above the mini-boss-tier ceiling at combat-peak but the idle (~119 px) reads near-mini-boss-ceiling. Path A-prime mini-boss range 66-88 px is exceeded at idle, BUT combat-stable framing is what mini-boss tier should READ as ("substantively-sized presence"). Trade-off documented per gandalf's three-part rationale.

## Cross-seam contract change?

**Round-trip: not applicable** — drax is the CONSUMER of upstream contracts (gandalf rulings + per-slug lookup; legolas measurement). However:

- **Required: field-presence assertion at MONSTER_SCALE_BY_SLUG lookup boundary for new `fire-lord-creativkind-thunder` entry** + ENEMY_TIER_CHARACTER_MAP `mini_boss` pool field-presence (fail-loud if slug missing from lookup at render time per Case A precedent).
- Per R11(b) Principle 6.

## What this dispatch produces

### Track 1 — `MONSTER_SCALE_BY_SLUG` lookup entry

Add new entry:

```ts
'fire-lord-creativkind-thunder': {
  scale: 2.64,
  width_or_height_priority: 'height',
  tier_coherence_violation: false,  // mini-boss-tier-bump per Matt Option 3; gandalf-ruled acceptable
  notes: 'Fire_Lord V1 (blue/purple); thunder mini-boss; combat-stable anchor 2.64× per gandalf Case 4 re-amendment',
}
```

- Color variant: **V1** (blue/purple; 52.6% blue-channel idle; median RGB 188/192/217; already in thunder register)
- Path: `/Users/admin/Games/reincarnated-demo/public/assets/CreativeKind/Fire_Lord*/` (variant 1 specifically)
- **NO palette tinting required** — vendor V1 ships in thunder register
- Nearest-neighbor HARD REQ (2.64× upscale)
- Anchor offset: same `+25 px source-px` mechanism as Case A V5 (frame-bottom anchor + 24-33 px idle float requires correction)

### Track 2 — `ENEMY_TIER_CHARACTER_MAP` mini_boss pool addition

Update `ENEMY_TIER_CHARACTER_MAP` (per `monsterSprites.ts:73` or current location post-Case-A-refactor):

```ts
mini_boss: ['lich', 'hellfire-rhino', 'fire-lord-creativkind-thunder'],  // necrotic + fire + thunder diversity
boss: ['angel-guardian'],   // god-of-lightning removed; Fire_Lord boss math-impossibility per legolas
act_boss: ['angel-guardian'],  // same
```

god-of-lightning stays REMOVED (Case A dispatch already handled the removal from boss/act_boss pools).

### Track 3 — Credits entry

Append to `creditsOverlay.ts` (or analogous):
- "CreativeKind — Fire_Lord (Variant 1 blue/purple) for thunder mini-boss-tier coverage."

(Case A dispatch already added V5 credits entry; this is the V1 companion.)

### Track 4 — Smoke test (Discipline #2 + R11(b))

- Verify `fire-lord-creativkind-thunder` renders at scale 2.64× V1 in mini_boss encounters
- Verify idle pose anchors cleanly (no ground-float) with `+25 px source-px` offset applied
- Verify mini_boss tier routing pulls from 3-slug pool (lich / hellfire-rhino / fire-lord-thunder) — verify per-slot variety logic still works with 3 slugs
- Verify boss/act_boss tier still pulls angel-guardian-only (god-of-lightning permanently removed)
- Verify nearest-neighbor enforcement applies to Fire_Lord V1 textures
- Field-presence assertion: missing fire-lord-thunder slug in lookup table fails loud per Case A precedent
- Existing demo tests pass; new Case D tests pass
- `tsc --noEmit` clean

### Track 5 — Tag + AGENT_STATE + completion record

- Intermediate tag: `drax/v0.20.7-case-d-fire-lord-v1-mini-boss-thunder`
- AGENT_STATE.md updated
- Fill completion record

## Out of scope (explicit)

- **NO Case A re-touches** (already shipped per Case A dispatch)
- **NO god-of-lightning re-introduction** (permanently REMOVED; pool entry stays commented-out reference only)
- **NO new monsters added beyond Fire_Lord V1 mini-boss slot**
- **NO boss-tier Fire_Lord variant** (math-impossibility per legolas; mini-boss is the gandalf-locked resolution)
- **NO palette-shift implementation** (V1 already ships in thunder register; runtime tint unnecessary)
- **NO MS schema/export/sim/cipher work** (separate workstreams)
- **NO viewport / combat-view architecture changes** (deferred per gandalf bonus item)
- **NO playable feature work beyond mini-boss-tier add**

## Required reading

- Gandalf commit 8a89d1b: `canonical/story/sprite-scale-math-impossibility-rulings-2026-05-16.md` § Case 4 re-amendment (Option 3 ruling; 2.64× spec; three-part rationale)
- Gandalf v2 per-slug lookup: `canonical/story/per-slug-scale-lookup-path-a-prime-2026-05-16.md` (Case E entry per any post-commit amendment)
- Legolas Fire_Lord measurement: `research/knowledge/character-monster-pixel-scale-2026-05-16.md` Section 4e (Case D math impossibility for boss-tier; mini-boss tier viability)
- Your Case A dispatch + completion record (pattern reference; ENEMY_TIER_CHARACTER_MAP current state; anchor-offset mechanism)
- `~/Games/reincarnated-demo/src/visuals/monsterSprites.ts` (current state after Case A returns)

## Acceptance criteria

- [ ] `fire-lord-creativkind-thunder` lookup entry added with scale 2.64× + V1 routing
- [ ] `ENEMY_TIER_CHARACTER_MAP` mini_boss pool includes fire-lord-creativkind-thunder alongside lich + hellfire-rhino
- [ ] boss/act_boss pools stay angel-guardian-only (god-of-lightning permanently removed)
- [ ] V1 variant correctly routed (blue/purple; no tinting)
- [ ] Anchor offset `+25 px source-px` applied
- [ ] Nearest-neighbor enforcement verified
- [ ] Credits overlay updated with V1 entry
- [ ] Smoke + tests pass; `tsc --noEmit` clean
- [ ] Intermediate tag `drax/v0.20.7-case-d-fire-lord-v1-mini-boss-thunder` cut
- [ ] AGENT_STATE.md updated
- [ ] Knight-rider notified with: tag hash, observed mini-boss-tier render at 2.64× (does combat read correctly as "substantively-sized thunder mini-boss presence" per gandalf framing), any per-monster anomalies

## Tag policy

- **Intermediate tag:** `drax/v0.20.7-case-d-fire-lord-v1-mini-boss-thunder`
- **Milestone tag:** none from this dispatch.

---

## Completion record

**Completed:** 2026-05-17
**V1 path used:** `public/assets/CreativeKind/Fire_Lord_Creativkind/Spritesheet/1/` (9 sheets; Fire Lord1_*-Sheet.png)
**Mini-boss render assessment:** Reads as substantive thunder mini-boss presence. At 2.64x: idle ~119 px (slightly above mini-boss band ceiling 88 px per gandalf combat-stable framing — expected and acceptable per Option 3 ruling). Combat peak (atk3 76 px content at 2.64x → ~200 px) will read as large threat at encounter peak. V1 blue/purple (thunder register) visually distinct from V5 fire/orange — no color confusion with elite pool. Nearest-neighbor confirmed active via SCALE_MODES.NEAREST on BaseTexture. No palette tinting required.
**Anchor offset effective:** Yes — +25 source-px applied (+66 px rendered at 2.64x). Mirrors Case A V5 pattern exactly. Same idle float geometry (24–33 px above frame bottom) confirmed by identical canvas dimensions (128x128) and sheet layout.
**Intermediate tag:** `drax/v0.20.7-case-d-fire-lord-v1-mini-boss-thunder @ 97dc766`
**Tests status:** 326/326 passed (315 prior + 11 new Case D tests). tsc --noEmit clean. vite build clean (520 modules).
**Notes for knight-rider:** Mini-boss pool is now 3 slugs (lich / hellfire-rhino / fire-lord-creativkind-thunder). resolveMonsterSlug() handles 3-slug pool transparently via pool[seed % pool.length] — no logic changes needed. Thunder element preference wired: ELEMENT_PREFERRED_SLUG['thunder'] = 'fire-lord-creativkind-thunder' routes thunder encounters to the thunder mini-boss in that tier. Boss/act_boss pools confirmed angel-guardian only — god-of-lightning stays out. No per-monster anomalies observed. Case D build is clean with zero regressions against Case A state. Do NOT auto-fire follow-on dispatches per per-seam discipline.
