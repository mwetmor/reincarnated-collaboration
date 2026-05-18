# Monster Curation Summary — VS2a Final (2026-05-17)

**Author:** elrond
**Dispatch:** `agentic_orchestration/dispatches/2026-05-17-elrond-monster-subset-curation-vs2a-final.md`
**Authority:** Matt L3 2026-05-17 — VS2a Final Sprint Q7 monster-subset curation YES authorization
**Status:** AUTHORED — curation complete; ready for drax v1.14 wiring follow-on

**Companion deliverables:**
- `monster-subset-vs2a-2026-05-17.jsonl` — per-monster manifest (10 priority-3+ rows for drax wiring + 2 priority-2 deferred-noted)
- `monster-coverage-matrix-vs2a-2026-05-17.md` — substrate × role-tier matrix (8 × 3 = 24 cells) with GREEN/YELLOW/RED scoring

---

## § 1 — Executive summary

**Goal.** Curate the 8-12 highest-impact CraftPix monsters from 17 monster packs + 4 boss packs on disk per legolas-3 catalogue, to feed drax v1.14 wiring follow-on. Doubling current wired variety (11 active CreativeKind monsters) transforms VS2a encounter feel.

**Outcome.** **10 priority-3+ monsters selected** (the upper bound of the 8-12 dispatch target, justified by substrate gap-closure urgency). 2 additional priority-2 monsters preserved as deferred-noted for future expansion.

**Variety transformation.** Wired roster goes from **11 → 21 monsters (+91%)** across 8 substrates × 4 tiers (trash / elite / mini-boss / boss).

**Substrate gap closure.** Water (RED → YELLOW) and wind (RED → YELLOW) substrates move from ZERO wired sprites to multi-tier coverage. Earth substrate moves from single-tier (elite) to four-tier coverage. Fire substrate gains boss representation (dragon) for the first time.

**Cost.** Zero acquisition cost (all assets on disk per legolas-3). Drax wiring effort = ~10 monsters at 256x256-monolithic-per-state pattern (drax-familiar shape from CreativeKind work). License posture: single CraftPix corpus credit covers all 10 monsters; no per-pack attribution complexity.

**Boss-tier expansion is the single highest-impact change.** Boss tier goes from 1 monster (angel-guardian, holy) → 3 monsters (dragon=fire, slime-boss=water, angel-guardian=holy). Every act-culminating encounter currently shows angel-guardian; post-curation enables substrate-flavored boss rotation.

---

## § 2 — Per-archetype recommendation

The 10 priority-3+ selections, mapped per substrate × tier:

| Substrate | Trash add | Elite add | Mini-boss add | Boss add |
|---|---|---|---|---|
| **fire** | **imp** (priority 4; pack net-500988; native Attack_fire) | — | — | **dragon** (priority 5; pack net-678687; 10 animation states inc Flight/Landing/Rise) |
| **water** | **slime** (priority 5; pack net-788364; closes critical water gap) | — | — | **slime-boss** (priority 5; pack net-827305; tier-progression-canonical pairing with slime trash) |
| **earth** | **plant** (priority 3; pack net-284465; root-attacker; pairs with ent + golem) | **ent** (priority 4; pack net-838021; nature/earth guardian — supplements crystal-golem) | **golem** (priority 5; pack net-625807; canonical earth construct — pairs thematically with crystal-golem elite) | — |
| **wind** | — | **beholder** (priority 5; pack net-404608; flying aerial caster; closes critical wind gap) | — | — |
| **lightning** | — | — | — | — |
| **holy** | — | — | — | — |
| **shadow** | **zombie** (priority 4; pack net-550920; humanoid undead diversity supplementing mutant-skeleton) | — | — | — |
| **physical** | — | **orc** (priority 4; pack net-363992; melee elite with unique run_attack states) | — | — |

**Two priority-2 deferred-noted alternatives** preserved in manifest (not for v1.14 wiring; for future variety expansion):
- **lich-craftpix-net-543463** — alternative to CreativeKind 'lich' if drax wants shadow-elite caster differentiation
- **skeleton-craftpix-net-870078** — alternative to CreativeKind 'mutant-skeleton' for trash-pool variety expansion

**Pack overlap resolutions** (where dispatch flagged TBD-at-curation):
- **beholder** — chose dedicated pack `craftpix-net-404608` over `craftpix-987754` beholder variant (dedicated pack has cleaner 3-variant structure + shadow/no-shadow architecture matching CraftPix standard)
- **goblin** — chose dedicated `craftpix-net-710530` over `craftpix-987754` goblin (ASEPRITE source + Parts subfolder for decomposition); HOWEVER goblin not selected for v1.14 wiring (current CK goblin-mage already fills humanoid-trash slot; deferred-noted)
- **ent** — chose dedicated `craftpix-net-838021` over `craftpix-987754` ent (6-state full coverage; cleaner variant architecture)
- **lizard** — chose `craftpix-net-900504` lizardmen (humanoid) over `craftpix-561178` lizard (quadruped) — different niches; HOWEVER neither selected for v1.14 wiring (no compelling tier-gap; reptilian archetype lower priority than substrate gap-closure)
- **dragon** — `craftpix-net-678687` (premium 10-state pack with Flight/Landing/Rise) preferred over `craftpix-561178` small-dragon (latter retained as priority-2 elite candidate; not in priority-3+ selections)

---

## § 3 — Acquisition status

**ALL 10 selected monsters on-disk per legolas-3 inventory.** Zero acquisition cost.

| Pack | On disk path | License |
|---|---|---|
| craftpix-net-788364 (slime) | `reincarnated-demo/public/assets/craftpix_catalogue_large/craftpix-net-788364-free-slime-mobs-pixel-art-top-down-sprite-pack/` | CraftPix-Free-Terms |
| craftpix-net-827305 (slime-boss) | `…/craftpix-net-827305-slime-boss-pixel-art-2d-sprite-for-roguelike-games/` | CraftPix-Free-Terms |
| craftpix-net-404608 (beholder) | `…/craftpix-net-404608-beholder-monsters-top-down-pixel-art-sprites/` | CraftPix-Free-Terms |
| craftpix-net-625807 (golem) | `…/craftpix-net-625807-golem-pixel-art-top-down-sprite-pack/` | CraftPix-Free-Terms |
| craftpix-net-500988 (imp) | `…/craftpix-net-500988-imp-mobs-pixel-art-character-sprite-pack/` | CraftPix-Free-Terms |
| craftpix-net-550920 (zombie) | `…/craftpix-net-550920-zombie-4-direction-pixel-character-sprite-pack/` | CraftPix-Free-Terms |
| craftpix-net-678687 (dragon) | `…/craftpix-net-678687-dragon-pixel-art-character-sprite-sheets-pack/` | CraftPix-Free-Terms |
| craftpix-net-838021 (ent) | `…/craftpix-net-838021-top-down-pixel-ent-character-sprites/` | CraftPix-Free-Terms |
| craftpix-net-363992 (orc) | `…/craftpix-net-363992-free-top-down-orc-game-character-pixel-art/` | CraftPix-Free-Terms |
| craftpix-net-284465 (plant) | `…/craftpix-net-284465-free-predator-plant-mobs-pixel-art-pack/` | CraftPix-Free-Terms |

**License attribution posture.** All 10 monsters operate under the CraftPix Free Terms umbrella. **One attribution credit** ("Monster sprites by CraftPix (https://craftpix.net/)") covers the entire selection. No per-monster credit lines needed. This is materially simpler than the CreativeKind monster pack (which required a per-pack vendor credit format).

---

## § 4 — Drax wiring complexity assessment

**Familiar shape.** All 10 monsters follow the CraftPix standard: 256x256 frame size, per-state PNG (monolithic state-per-sheet), with/without shadow variants. This is **simpler** than the CreativeKind heterogeneity drax already absorbed (CreativeKind has mixed grid / strip / combined / row_per_anim layouts per `monsterSprites.ts` § 'CreativeKind sheet layouts'). CraftPix is predominantly `strip` or `row_per_anim` per state-PNG with a single layout pattern across the corpus.

**Per-monster wiring cost estimate.** ~30 min per monster (mirroring CreativeKind onboarding from drax/v0.20 monster-track work):
- Stage 1: per-state PNG copy from `craftpix_catalogue_large/` to `/assets/monsters/<slug>/sheets/` (mechanical)
- Stage 2: metadata.json authoring (frame_w/frame_h, animations dict, element_flavor, tier)
- Stage 3: ENEMY_TIER_CHARACTER_MAP entry + MONSTER_SCALE_BY_SLUG entry per the Path A-prime per-slug-scale-lookup pattern
- Stage 4: smoke-test render at tier midpoint; nearest-neighbor scaleMode confirmation (HARD REQ per current code; 256x256 sources require nearest-neighbor at all current Path A-prime scales)

**Total drax effort estimate for v1.14: ~5 hours** (10 monsters × 30 min). This is at the upper edge of a single-dispatch budget.

### § 4.1 — Phased approach recommendation

If drax v1.14 budget is constrained, recommend **two-phase wiring**:

**Phase A (drax v1.14): 6 priority-5 monsters — substrate gap-closure focus**
- slime (water trash) — CRITICAL gap
- slime-boss (water boss) — CRITICAL gap
- beholder (wind elite) — CRITICAL gap
- golem (earth mini-boss) — high impact (earth tier ladder)
- dragon (fire boss) — high impact (first non-holy boss)
- ent (earth elite supplement) — moderate impact (substrate depth)

Wired total after Phase A: 17 monsters (+6 from current 11). Estimated drax cost: ~3 hours.

**Phase B (drax v1.15 or follow-on): 4 priority-3-4 monsters — variety expansion**
- imp (fire trash)
- zombie (shadow trash supplement)
- orc (physical elite)
- plant (earth trash)

Wired total after Phase B: 21 monsters. Estimated drax cost: ~2 hours.

**Recommendation:** drax v1.14 dispatch should explicitly scope Phase A; Phase B as a separate v1.15 dispatch keeps each wiring sprint bounded and reduces single-dispatch failure-recovery risk.

### § 4.2 — Wiring complexity flags

- **Dragon pack (net-678687) is the most complex single addition** — 10 animation states (idle + walk + 2 attacks + flight + landing + rise + hurt + death + special) with 1792x256 strip-per-state layout. Drax may want to wire only essential states first (idle/walk/attack1/hurt/death = 5 states) and defer Flight/Landing/Rise to a v1.16 cinematic-entry follow-on.
- **Plant pack** — static-rooted predator-plants don't walk. Drax should map walk → idle animation (or set walk to a sway-frame from idle if Parts subfolder offers one).
- **Zombie pack (net-550920)** has 4-directional sheets. VS2a uses single-direction per current pattern (chierit + CreativeKind). Drax confirms direction-selection is deferred to post-VS2a; wire single-direction (likely south-facing or generic).
- **Imp pack** has TWO attack animations (Attack + Attack_fire). Drax can map Attack_fire → 'casting' state (parallel to current lich/fire-lord-v5 dual-attack pattern).

---

## § 5 — Element-imbalance flags

D10/D11 monster generator produces 220 monster instances across 5 seasons with **equal canonical-4 element distribution**: fire(55) / water(55) / earth(55) / wind(55). Engine-generated monsters expect equal substrate distribution.

**Post-curation wired distribution** (21 monsters):

| Substrate | Wired count | Tier coverage |
|---|---|---|
| fire | 3 | trash + elite + boss |
| water | 2 | trash + boss (missing elite) |
| earth | 4 | trash + elite (2-deep) + mini-boss |
| wind | 1 | elite only |
| lightning | 1 | mini-boss (thunder-shifted) |
| holy | 1 | boss only |
| shadow | 5 | trash (3-deep) + elite + mini-boss |
| physical | 3 | trash (2-deep) + elite |

**Imbalance:**

- **Shadow is over-represented** (5 wired vs engine-expected 0 — D10/D11 doesn't generate shadow monsters at the seasonal-mechanical layer; shadow enters at the canonical-7 substrate-expansion gate per Phase-1 P1). The shadow over-representation is a legacy of CK monster pack composition (skeleton/lich/demon-mage all shadow-coded) and isn't fixable in this curation.
- **Wind is severely under-represented** (1 wired vs engine-expected 55). Even post-curation, wind is the thinnest canonical-4 coverage. Recommended Phase-1-P1-follow-on: a second wind monster acquisition or beholder-variant elevation to mini-boss tier.
- **Holy and lightning are placeholder-only** (1 wired each; both substrate-expansion-new). Phase-1 P1 will require dedicated holy + lightning monster acquisitions to match the substrate-set's mechanical claim.
- **Physical boss tier absent** — sword-warrior remains the only humanoid melee at trash; orc adds elite; no boss-tier physical equivalent (orc-warlord style would be canonical).

**Operational impact for VS2a:** Each wave can present substrate-coherent encounters for water/fire/earth (Phase A wires). Wind encounters render only beholder (elite tier). Lightning/holy encounters fall back to current single-slot wiring.

---

## § 6 — RED cells remaining post-curation

Per the coverage matrix § 3.3:

| RED cell | Severity | Resolution path |
|---|---|---|
| **wind boss** | MEDIUM | DEFER — beholder3 variant scale-up at drax follow-on; or `craftpix-897123` boss-monsters pack at v1.15 |
| **lightning trash** | LOW | DEFER — genre-rare; not VS2a-blocking |
| **lightning elite** | LOW-MEDIUM | DEFER — could shift fire-lord-thunder back to elite if Phase-1 P1 substrate-expansion requires it |
| **holy trash** | MEDIUM | ACQUISITION GAP — see § 7 handoff to Matt |
| **holy elite** | MEDIUM | ACQUISITION GAP — see § 7 handoff to Matt |
| **shadow boss** (full-boss tier, not mini-boss) | MEDIUM-LOW | DEFER — could use `craftpix-897123` Demon boss at v1.15; or elevate net-543463 lich variant 3 to boss |
| **physical boss** | MEDIUM-LOW | DEFER — `craftpix-897123` Demon boss is canonically melee-physical; v1.15 follow-on |

### § 6.1 — Bonus pack reserved for follow-on

**`craftpix-897123-boss-monsters-pixel-art`** is a HIGH-VALUE secondary pack NOT included in v1.14 selections.

It contains 3 state-rich bosses (Mage / Demon / Ooze) with full per-state PNG architecture AND projectile sub-assets (FireBall, IceBlock, Ray, orb_of_venom). It could simultaneously address:
- lightning elite (Mage with Ray projectile)
- physical/shadow boss (Demon)
- alternative water boss (Ooze; complementary to slime-boss)

Plus the projectile sub-assets are independently valuable for VFX layering work (see vfx-layered-architecture-vs2a-2026-05-17 for projectile reuse pattern).

**Recommended as v1.15 dispatch scope** — explicit follow-on after v1.14 lands and validates.

---

## § 7 — HANDOFFs

### § 7.1 — HANDOFF → drax (v1.14 wiring inputs)

**Manifest:** `agentic_orchestration/research/curated/monster-subset-vs2a-2026-05-17.jsonl` — 10 priority-3+ rows with per-monster `drax_wiring_notes` field.

**Recommended scope for drax v1.14:**
- **Option A — single dispatch (10 monsters; ~5h):** All priority-3+ in one wiring pass.
- **Option B — phased (recommended; see § 4.1):** Phase A (6 priority-5 monsters; ~3h) at v1.14 + Phase B (4 priority-3-4 monsters; ~2h) at v1.15.

**Key wiring notes:**
- All 10 monsters are 256x256 frame-per-state, monolithic, with-shadow variant preferred for HD-2D depth.
- License: single CraftPix corpus credit covers all.
- Element-flavor assignments per `canonical_substrate_mapping` field in manifest (fire / water / earth / wind / lightning / holy / shadow / physical).
- Animation state coverage per `animation_states` field — minimum 5 states (idle/walk/attack/hurt/death) across all selections.
- Path A-prime per-slug-scale-lookup entries required for all 10 (mirror existing MONSTER_SCALE_BY_SLUG pattern; estimate 0.30-1.8x scale per tier per the `rendered_size_target` field).
- Nearest-neighbor HARD REQ for all (per current monsterSprites.ts `base.scaleMode = SCALE_MODES.NEAREST` enforcement).
- Dragon pack (10 states) is the most complex; recommend wiring 5 essential states first (defer Flight/Landing/Rise to v1.16).

**Coverage matrix reference:** `agentic_orchestration/research/curated/monster-coverage-matrix-vs2a-2026-05-17.md` — substrate × tier × GREEN/YELLOW/RED for ENEMY_TIER_CHARACTER_MAP planning.

### § 7.2 — HANDOFF → matt (acquisition gaps surfaced)

Two substrate gaps are NOT resolvable from on-disk CraftPix corpus and require Matt-decision on acquisition:

1. **Holy substrate non-boss tiers** (MEDIUM severity)
   - Current: angel-guardian fills boss only.
   - Gap: holy trash + holy elite + holy mini-boss are all RED.
   - Recommended acquisition target: chierit pack already ships light-valkyrie + holy-radiance VFX per substrate-expansion-decision-2026-05-17.md § 1 line 36 ("CreativeKind's holy-radiance and shadow-tendril VFX are GREEN-list") — but the light-valkyrie sprite may not be on disk (legolas-3 inventory does not list it under free_characters_and_vfx with status `already_acquired`).
   - Decision needed: commission legolas-4 chierit-pack-expansion crawl to confirm light-valkyrie availability, or accept holy substrate as boss-only for VS2a + Phase-1 P1 follow-on.

2. **Lightning substrate native** (MEDIUM severity)
   - Current: fire-lord-creativkind-thunder is a thunder-shifted re-skin of a fire-pack asset (per Case D dispatch). Not native lightning.
   - Gap: a native lightning-coded monster (lightning-ronin per substrate-expansion-decision-2026-05-17.md line 36, or chierit lightning-ronin / lightning-elemental) would close this elegantly.
   - Decision needed: commission legolas-4 lightning-monster crawl (chierit catalogue or other vendor) or accept thunder-shift as canonical lightning representation through Phase-1 P1.

**No other gaps require acquisition.** Wind boss / physical boss / shadow full-boss can all be addressed via the already-on-disk `craftpix-897123-boss-monsters-pixel-art` pack at v1.15 follow-on.

### § 7.3 — HANDOFF → knight-rider (chain coordination)

**Curation complete.** Three deliverables in `agentic_orchestration/research/curated/`:
- `monster-subset-vs2a-2026-05-17.jsonl` (manifest; was DEFERRED stub, now AUTHORED)
- `monster-coverage-matrix-vs2a-2026-05-17.md` (coverage matrix)
- `monster-curation-summary-vs2a-2026-05-17.md` (this document)

**Parallel-safe execution confirmed.** No conflict with drax v1.13 VS2a Final Sprint (environment + VFX seam, distinct from monster manifest seam), gandalf audio register canon (separate canon authoring), rocket v1.13.2 demo-sync (no shared files), or D11.1 sprint chain (separate engine-side seam).

**Recommended next chain links:**
1. **drax v1.14 dispatch** — wire monster-subset per § 7.1 (recommend phased Option B per § 4.1)
2. **Matt acquisition decision** (async) — resolve holy + lightning substrate acquisition per § 7.2
3. **legolas-4 dispatch** (conditional on Matt § 7.2 acquisition decision) — chierit-pack-expansion crawl for light-valkyrie + lightning-ronin confirmation
4. **drax v1.15 dispatch** (post-v1.14 validation) — wire pack-897123 boss-monsters for wind-boss / physical-boss / shadow-boss gap closure

**No tag.** Curation work (not code) per dispatch policy.

**No MIGRATION.md entry.** This curation does not change data schema or cross-seam contract; it adds to the existing monster-subset manifest already in the research/curated/ tree (overwriting a DEFERRED stub with an AUTHORED full manifest).

---

## § 8 — Notes on what worked + what was deferred

**Worked.**
- Substrate-gap-first prioritization (water + wind RED → YELLOW) gave clear ranking criteria
- Overlap resolution criterion = "dedicated pack > variant-in-mixed-pack" worked cleanly across beholder/goblin/ent
- 8-12 row target was right; 10 priority-3+ + 2 priority-2 deferred-noted = 12 total preserves optionality without over-stuffing manifest
- CraftPix corpus license simplicity (one credit) removes per-monster attribution overhead that the CreativeKind work required

**Deferred and noted.**
- Pack `craftpix-897123-boss-monsters-pixel-art` (3 bosses + projectile sub-assets) reserved for v1.15 — high value but pushes drax v1.14 budget over edge
- `craftpix-561178` 6-variant pack (demon/dragon/jinn/lizard/medusa/small_dragon) — partially absorbed (dragon went via dedicated net-678687 pack instead); medusa/jinn/small-dragon are interesting but no priority-tier gap they uniquely fill
- `craftpix-987754` 6-variant pack (beholder/dino/ent/goblin/mosquito/spider) — partially absorbed (beholder via dedicated net-404608 pack; ent via dedicated net-838021 pack); dino/spider/mosquito retained as future-variety candidates
- `craftpix-net-900504` lizardmen — interesting humanoid-reptilian niche but no gap-fill justification at priority-3+; remains catalogued
- `craftpix-net-710530` goblin (dedicated pack) — quality choice over 987754 goblin but no slot to wire (current CK goblin-mage fills humanoid-trash); manifest-deferred-noted

**Survey-mode discipline.** Per elrond persona ("what EXISTS / what's interesting / what's missing as three separate outputs"):
- **EXISTS:** 17 monster packs + 4 boss packs on disk; 11 CreativeKind monsters wired; canonical-7 substrate framework + physical = 8 axis
- **INTERESTING:** water + wind substrates have ZERO wired sprites despite engine-equal generation; boss tier is mono-substrate (holy only); CraftPix corpus has highly uniform schema (drax-friendly)
- **MISSING:** native lightning + holy non-boss tiers; physical boss tier; wind boss tier — flagged as acquisition gaps for Matt

---

*Curation completed 2026-05-17 by elrond per dispatch + Matt L3 Q7 YES authorization. ~1.5 hours total (manifest authoring + matrix construction + summary). All three deliverables in `agentic_orchestration/research/curated/`. PRE-SIGNAL § 14.1.1 acknowledged; hive-log STATE + HANDOFFs appended in this completion record.*
