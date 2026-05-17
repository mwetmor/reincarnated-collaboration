# Dispatch — 2026-05-16 — gandalf — Per-slug scale lookup table v2 (Path A-prime; ARPG 100-130 px chierit baseline) + style-register reconciliation follow-on amendment

**From:** knight-rider (authored per Matt directive 2026-05-16 Day 4 close: items 1-3 confirmed/authorized; Path A-prime locked per ARPG-vs-JRPG reframing)
**To:** gandalf
**Approved by:** Matt at 2026-05-16 Day 4
**Status:** PENDING
**Mode:** Design-track analytical (canonical-doc / findings-doc authoring)
**Estimated effort:** 1 session (~1.5-2h); v2 lookup table revision + style-register follow-on amendment in single session

**Gate-1 bypass rationale:** Matt-directed (Path A-prime explicitly confirmed); single-seam (gandalf canonical / findings only); reversible (recommendation + canonical-doc updates).

**Acceptance summary:** v2 per-slug scale lookup table filed at `canonical/story/per-slug-scale-lookup-path-a-prime-2026-05-16.md` (or supersession-revision of the existing per-slug Path A doc — your call on whether to revise-in-place or new doc). Path A ratios preserved (Matt-locked); absolute baseline corrected to ARPG ~100-130 px (vs prior Path A's ~44 px). Chierit scale revised + per-monster scales shifted up proportionally. Style-register reconciliation note amended to include ARPG 100-130 px operational target framing (the prior note framed 80-100 px as aesthetic-reference-only; ARPG reframing surfaces that 100-130 px IS the operational target). Knight-rider notified.

---

## Why this dispatch exists — Path A-prime locked

Matt's directive: **Path A-prime CONFIRMED.** Apply Path A ratios (Diablo genre-convention 0.6-0.85× swarm / 1.0-1.3× elite / etc.) to corrected ARPG ~100-130 px chierit baseline (vs Path A's ~44 px baseline).

ARPG-genre framing (your forwarded analysis Matt relayed): Reincarnated single-camera ARPG; not JRPG dual-camera. ARPG band at 1080p = 100-130 px (Diablo IV 110-130; PoE 100-120; Last Epoch 100-110; Grim Dawn 90-110). HD-2D-shaped pixel-art register preserved — Path A-prime is a SCALE adjustment within the register, not a register change.

**Two work products in single session** (per Matt items #2 + #3 authorization):
1. v2 per-slug lookup table (Path A ratios × ARPG ~100-130 px baseline)
2. Style-register reconciliation note follow-on amendment (the prior note authored in canonical-amendments batch reflects pre-ARPG-reframing framing — needs ARPG 100-130 px operational target added)

## Cross-seam contract change?

**Round-trip: not applicable** — recommendation-doc + canonical-doc updates only; no schema or contract change. Downstream drax MONSTER_SCALE_BY_SLUG refactor (now blocked on this v2) carries its own round-trip discipline. Per R11(b) Principle 6.

## What this dispatch produces

### Track 1 — v2 per-slug scale lookup table (Path A-prime)

**Doc path (your call):**
- **Option A:** new doc at `canonical/story/per-slug-scale-lookup-path-a-prime-2026-05-16.md` — supersedes the v1 (`per-slug-scale-lookup-path-a-2026-05-16.md`) with explicit cross-reference
- **Option B:** revise-in-place at the existing v1 doc with "Supersession 2026-05-16 — Path A-prime ARPG-anchored" header

Pick whichever fits the gandalf canonical pattern cleaner. My read: Option A (new doc) preserves audit trail; v1 doc becomes historical record.

**Content updates from v1:**

**Part 1 — Chierit operational scale (revised)**

Re-derive chierit operational scale. Old v1: Option (i) chierit at 1.0× → 34-57 px figure content → ~44 px baseline. Path A-prime requires chierit baseline ~100-130 px.

- Approximate scale-up factor: 100/44 = 2.27× to 130/44 = 2.95×
- Chierit at scale **2.3-2.9×** → figure content ~78-165 px depending on character group (A: Shadow Stalker 57px × 2.3-2.9 = 131-165 px; B: Fire Knight 44px × 2.3-2.9 = 101-128 px; C: Ground Monk 34px × 2.3-2.9 = 78-99 px)

Surface chierit-default decision:
- **Sub-option (i-prime):** uniform chierit default ~2.5× → most characters land in 100-130 px band; Group C (smallest) slightly under-band, Group A (tallest) slightly over-band. Preserves variance as design feature.
- **Sub-option (ii-prime):** per-character lookup normalizing all chierit to 110-120 px midpoint → Group A scale ~1.9-2.1× , Group B ~2.5×, Group C ~3.2-3.5×. Homogenizes Diablo-Druid/Barb/Amazon-style intra-class variance.
- Pick + justify per your design judgment.

**Part 2 — Path A-prime monster tier ranges**

Re-anchor your tier ranges against the chosen chierit baseline. If chierit settles at ~110-120 px midpoint:
- **Trash:** 0.6-0.85× player → 66-102 px
- **Elite:** 1.0-1.3× player → 110-156 px
- **Mini-boss:** 1.5-2.0× player → 165-240 px
- **Boss:** 2.5-4.0× player → 275-480 px
- **Act-boss:** as appropriate to your ratios

Compare to v1's Path A ranges (trash 26-37; elite 44-57; mini-boss 66-88; boss 110-176) — all approximately 2.5× larger at Path A-prime.

**Part 3 — Per-monster scales (revised)**

For each of the 10 active ENEMY_TIER monsters (god-of-lightning removed; Fire_Lord_Creativkind palette-shifted to thunder slot per Matt decision), revise the scale factor for Path A-prime tier-range targeting.

Approximate scale-up factor from Path A → Path A-prime ≈ 2.3-2.9×:
- v1 goblin-mage 0.40 → v2 ≈ 0.92-1.16
- v1 mutant-skeleton 0.32 → v2 ≈ 0.74-0.93
- v1 evil-eye 0.60 → v2 ≈ 1.38-1.74
- v1 sword-warrior 0.13 → v2 ≈ 0.30-0.38
- v1 crystal-golem 0.42 → v2 ≈ 0.97-1.22
- v1 fire-elemental 0.85 → v2 ≈ 1.96-2.47 (becomes upscale; tier_coherence_violation may shift)
- v1 demon-mage 0.48 → v2 ≈ 1.10-1.39
- v1 lich 0.70 → v2 ≈ 1.61-2.03
- v1 hellfire-rhino 0.78 → v2 ≈ 1.79-2.26
- v1 angel-guardian 0.75 → v2 ≈ 1.73-2.18 (becomes UPSCALE — nearest-neighbor HARD REQ becomes even more critical)
- Fire_Lord_Creativkind (thunder palette-shift) → derive per Path A-prime boss tier range

(Numbers above are illustrative; you do the math with chosen chierit baseline.)

Per-slug: scale factor + tier-coherence flag (in-band / above / below) + quality-loss flag (none / acceptable-upscale / acceptable-downscale / nearest-neighbor-required) + per-slug width_or_height_priority flag.

**Part 4 — Schema additions for drax refactor (carry forward unchanged from v1):**
- `width_or_height_priority` per-slug flag
- Nearest-neighbor enforcement on all monster textures (HARD REQ becomes more critical at Path A-prime due to monsters at upscale > 1.0×)
- `tier_coherence_violation` per-slug flag

**Part 5 — Viewport pressure analysis (NEW at Path A-prime)**

Path A-prime brings sprites to ARPG-genre absolute size. Surface viewport implications:
- Player at chierit ~2.5× = ~110-120 px tall (figure content), ~320 px tall (full 288×128 canvas × 2.5 — wait, that's wrong because canvas is 288W × 128H so 128 × 2.5 = 320 px tall full canvas; figure-content is the player-visible-region of that)
- Player + boss at boss-tier 2.5-4.0× player = 275-480 px tall
- Combat scene horizontal footprint at ARPG scale: player + boss + 4 trash = significant viewport budget
- **Drax v0.20.4 viewport finding (which dissolved under Path A) RETURNS at Path A-prime.** Pre-existing arena dimensions (drax shipped Diablo/PoE room/hallway topology at 15-45m × 48 px/m = 720-2160 px) may or may not accommodate ARPG-scale sprites cleanly.

Surface for routing — does Path A-prime require arena re-dimensioning (drax/star-lord viewport call) OR does the room/hallway topology drax shipped today already accommodate? If the latter (which Reincarnated's ARPG-from-day-one design likely intended), no further action needed beyond the v2 lookup table. If the former, surface as Matt-decision for separate viewport dispatch.

### Track 2 — Style-register reconciliation note follow-on amendment

The prior style-register reconciliation note (just landed in canonical-amendments batch) frames:
> "80-100 px is register aesthetic reference, NOT operational pixel-count constraint on project's specific source assets. Path A operationalization: chierit native 1.0× → ~44 px baseline; monsters scaled to Path A tier ranges."

Per ARPG reframing this is incomplete. Amend the note to add:
- **ARPG-genre operational target:** 100-130 px at displayed 1080p resolution (Diablo IV / PoE / Last Epoch / Grim Dawn convention). Reincarnated single-camera ARPG, not JRPG dual-camera (Sea of Stars / Octopath overworld 80-100 px was JRPG-overworld-camera reference; Octopath BATTLE camera 120-130 px is closer match per legolas ground-truth).
- **Path A-prime operationalization:** chierit at scale ~2.3-2.9× → ~100-130 px baseline; monsters scaled to Path A-prime tier ranges per `per-slug-scale-lookup-path-a-prime-2026-05-16.md`.
- **Register preservation:** HD-2D-shaped pixel-art register remains the visual-style commitment. Path A-prime is a SCALE adjustment within the register, not a register change. Nearest-neighbor enforcement on all monster textures preserves pixel-art coherence at upscale.
- **Cross-references:** `canonical/story/embodiment-display-loadout.md` § 1.1 (your ARPG-anchored framing amendment already committed at 85ce42f); `canonical/story/per-slug-scale-lookup-path-a-prime-2026-05-16.md` (v2 lookup table).

Note: do NOT rewrite the existing reconciliation note; AMEND with the ARPG operational target framing.

## Out of scope (explicit)

- **NO drax refactor authoring** — knight-rider authors drax MONSTER_SCALE_BY_SLUG dispatch (currently held; unblock trigger updated to "v2 lookup table return") + drax chierit-scale-revision dispatch after this lands
- **NO vendor acquisition execution** — Fire_Lord_Creativkind palette-shift swap is locked; no other acquisitions in scope
- **NO viewport / arena re-dimensioning execution** — surface for Matt-decision routing only if needed
- **NO HD-2D-register revision** — locked anchor; Path A-prime is scale within register
- **NO MS / B6 / form-bias touchpoints** — separate work streams
- **NO god-of-lightning re-evaluation** — palette-shift Fire_Lord_Creativkind locked
- **NO duplicate work** of gandalf 85ce42f commit (embodiment-display § 1.1 ARPG amendment already landed there)

## Required reading

- Your v1 per-slug Path A lookup table: `canonical/story/per-slug-scale-lookup-path-a-2026-05-16.md`
- Your math-impossibility rulings: `canonical/story/sprite-scale-math-impossibility-rulings-2026-05-16.md`
- Your style-register reconciliation note (just landed in canonical-amendments batch): `canonical/story/style-register.md` § Path A reconciliation
- Your committed 85ce42f amendments (`canonical/story/embodiment-display-loadout.md` § 1.1 ARPG-anchored)
- Drax v0.20.4 chierit composite notes: `agentic_orchestration/gandalf/findings/2026-05-16-chierit-character-scale-inspection-strip-corrected-notes.md`
- Drax v0.20.2 monster composite notes: `agentic_orchestration/gandalf/findings/2026-05-16-monster-scale-inspection-strip-notes.md`
- Legolas pixel-scale research: `agentic_orchestration/research/knowledge/character-monster-pixel-scale-2026-05-16.md` (Section 1+2 intrinsic sizes; Section 3 ARPG-vs-JRPG ground truth)

## Acceptance criteria

- [ ] v2 per-slug lookup table doc filed (Option A new-doc or Option B revise-in-place; pick)
- [ ] v1 → v2 supersession explicit (cross-reference; audit trail preserved)
- [ ] Chierit operational scale recommendation revised (sub-option i-prime or ii-prime with rationale)
- [ ] Path A-prime monster tier ranges established
- [ ] Per-monster scale recommendation for all 10 active monsters (god-of-lightning removed; Fire_Lord_Creativkind thunder added)
- [ ] Schema additions carried forward (width_or_height_priority + nearest-neighbor + tier_coherence_violation)
- [ ] Viewport pressure analysis surfaced (Path A-prime re-introduces; flag Matt-decision OR confirm no action)
- [ ] Style-register reconciliation note amended with ARPG 100-130 px operational target framing
- [ ] Cross-references between v2 lookup + style-register amendment + embodiment-display § 1.1
- [ ] Knight-rider notified with: doc paths, chierit sub-option chosen, viewport-pressure recommendation (arena re-dimensioning needed or not?), any new Matt-decisions framed

## Tag policy

- No git tag (gandalf persona convention)

---

## Completion record

**Completed:** _<date>_
**v2 doc path:** _<path; new-doc or revise-in-place>_
**Chierit sub-option chosen:** _<i-prime / ii-prime + rationale>_
**Viewport-pressure recommendation:** _<arena re-dimensioning needed / no action / Matt-decision needed>_
**Style-register amendment landed:** _<yes/no>_
**Open Matt-decisions surfaced:** _<list>_
**Notes for knight-rider:**
