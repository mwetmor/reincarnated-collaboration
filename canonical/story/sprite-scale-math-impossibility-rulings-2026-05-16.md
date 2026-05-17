# Sprite-Scale Math-Impossibility Rulings — VS2a CreativeKind Monster Pool

**Status:** **Canonical rulings.** Authored 2026-05-16 by gandalf per knight-rider dispatch (`agentic_orchestration/dispatches/2026-05-16-gandalf-math-impossibility-rulings.md`), Matt-approved at Day 4 close.

**Purpose:** Resolve the four mathematical-impossibility cases legolas pixel-scale research (`agentic_orchestration/research/knowledge/character-monster-pixel-scale-2026-05-16.md` § 4c) surfaced, where intrinsic source-sheet pixel dimensions make the per-tier render target either impossible without unacceptable quality loss, or impossible without a tier-coherence violation.

**Consumes:**
- Legolas pixel-scale research § 4c (math-impossibility flags)
- Drax v0.20.2 composite-strip companion notes (`agentic_orchestration/gandalf/findings/2026-05-16-monster-scale-inspection-strip-notes.md`)
- Drax MONSTER_TRACK_INTEGRATION_NOTES.md (deferred-pack roster for option-b candidates)
- Direct PIL inspection of on-disk sprite content bounding boxes (this doc, § Empirical correction below)

**Feeds:**
- gandalf's in-flight per-slug scale lookup table (consumes these rulings)
- knight-rider's forthcoming drax `MONSTER_SCALE_BY_SLUG` refactor dispatch (downstream consumer of the lookup table)
- Matt-decision queue for any option-d acquisition asks

**Companion canonical:**
- `style-register.md` — HD-2D-pixel register lock (the consumption-time filter these rulings honor)
- `enemy-visual-legibility.md` — tier-coded silhouette / aura / banner hierarchy (the perceptual architecture these rulings serve)
- `gandalf-design-lineage.md` Layer 2 — Diablo size-hierarchy lineage (the genre reference these rulings inherit from)

---

## TL;DR — Rulings summary

| Case | Tier | Frame H | Required scale | Ruling | One-line rationale |
|---|---|---|---|---|---|
| fire-elemental | elite | 192×68 | 1.50× upscale | **(c) Leave best-achievable + (b)-queue for VS2b swap** | Flat-sideview aesthetic is intrinsically untenable as a humanoid-shaped elite; render at 1.10× ceiling, document tier-coherence violation, queue Fire_Lord_Creativkind as swap candidate at VS2b |
| angel-guardian | boss | 256×192 | 1.52× upscale | **(a) Accept quality loss** | Boss-tier-as-aesthetic-choice — large pixels read as "carved presence" with nearest-neighbor; 1.52× is the threshold not the wall; cinematic-tier aura compensates |
| sword-warrior | trash | 280×280 | 0.23× downscale | **(c) Leave best-achievable with corrected math** | Empirically the content bbox occupies 92% of frame so the "extreme downscale" framing is wrong; trash tier wants ~55 px body → scale 0.21 (not 0.23 from frame, but from body); downscale is large but pixel-art tolerates clean downscale far better than upscale |
| god-of-lightning | boss | 256×256 (1-frame) | n/a (acquisition gap) | **(d) Matt-acquisition authorization requested** | Scale is feasible (1.14× upscale acceptable for boss); blocker is missing animation pack — render as static is unacceptable for the act-boss cinematic moment per `enemy-visual-legibility.md` S4 |

---

## Empirical correction to the legolas tier-target math (load-bearing — read before the rulings)

The legolas synthesis (§ 4a, § 4b) and the drax composite notes both anchor on drax's empirical estimate that **chierit character art occupies ~80-96 px of the 288×128 canvas (midpoint 88 px).** That estimate is wrong by roughly a factor of two.

Direct PIL `Image.getbbox()` inspection of `sheets/idle.png` frame 0 across all 10 chierit characters returns these actual character art heights inside the 128 px canvas:

| Character | Body content-h (px) |
|---|---|
| fire-knight | 44 |
| water-priestess | 37 |
| ground-monk | 34 |
| wind-hashashin | 37 |
| lightning-ronin | 43 |
| crystal-mauler | 39 |
| light-valkyrie | 53 |
| shadow-stalker | 57 |
| metal-bladekeeper | 42 |
| leaf-ranger | 44 |

**Range: 34-57 px. Midpoint: ~44 px. Mean: ~43 px.** Not 80-96 px.

This recalibrates the player-reference number used in every prior scale-comparison artifact:

- At current scale 0.35, the chierit player body renders at **~15 px** on screen (44 × 0.35), not 31 px and not 45 px.
- The "Fire Knight = 45 px tall at scale 0.35" number in the drax composite notes is **canvas height × scale (128 × 0.35 = 45)**, not character body height × scale. Useful as a column-height reference but not a body-to-body comparison.
- To reach a Sea of Stars-class 80 px rendered body, chierit characters need scale ≈ **1.85** (80 / 43), not 1.02. This is *above 1.5×* and itself runs into pixel-art upscale-quality concerns.

**Implication for the tier-size hierarchy:** The 55-75 / 90-115 / 130-180 / 225-360 px tier ranges I authored Day 4 were calibrated to a Sea of Stars-class **player body** of ~80 px. If we hold those tier ranges and accept that chierit caps the player at body-height ~44 px without upscaling, **the entire monster-tier hierarchy is over-scaled relative to the player.** The current `DEFAULT_MONSTER_SCALE=0.28` was producing trash mobs at 18-78 px rendered height vs. a 15 px player body — a *trash mob taller than the player* situation that the genre's tier hierarchy explicitly excludes.

**Two paths forward** (not in scope of *this* dispatch but flagged):
- **Path A — re-anchor the tier hierarchy lower to match chierit's actual body height.** New ranges (proportional shrink): trash 28-38 px, elite 45-58 px, mini-boss 65-90 px, boss 113-180 px. Halves all current monster scale factors. Stays inside source-sheet pixel budgets cleanly; eliminates almost all upscale-quality concerns; sword-warrior downscale becomes more extreme (already addressable per ruling below).
- **Path B — upscale chierit characters to reach the 80 px player reference, then keep monster tier hierarchy as authored.** Requires chierit scale ≈ 1.85×, which is itself a pixel-art quality concern at the threshold. Likely needs nearest-neighbor + careful inspection; the chierit asset's hand-drawn-pixel register tolerates this better than retro-pixel would, but it is non-trivial.

I recommend **Path A** as the cleaner answer (anchor to source-asset pixel budgets, accept that HD-2D's 80 px reference is a guideline not a constraint when the source-asset budget is what it is). But this is a separate decision from the four math-impossibility rulings below. I have authored the rulings below against **the tier ranges as originally specified** — the rulings remain valid under either Path A or Path B, with scale factors adjusted proportionally if Path A is chosen.

Knight-rider: please surface "Path A vs Path B re-anchor decision" as a Matt-decision question alongside this ruling doc. It is a parent decision to the per-slug lookup table.

---

## Case 1 — fire-elemental (elite, 192×68)

**Diagnosis (per legolas + my PIL inspection):**
- Frame canvas: 192×68 px (the *width is 192*, the height is 68 — flat-sideview aesthetic per drax)
- Content bbox max over sampled frames: 151×55 px (78-81% of frame height — there is some empty vertical padding but not much; the asset is genuinely short)
- Required scale for elite tier midpoint (102 px target body): 102 / 55 = **1.85×** upscale
- Required scale for elite tier floor (90 px target body): 90 / 55 = **1.64×** upscale
- Required scale just to match the player reference (~44 px body): 0.80× — *the asset would need to be downscaled* to match the player body, which then means the fire-elemental reads as smaller than the player and the elite tier signal collapses

This is **not** a single-axis scale problem. It is an **archetype problem.** The fire-elemental's intrinsic geometry — wide-flat — does not match the **silhouette signature an elite-tier monster needs** per `enemy-visual-legibility.md` S1 + the perceptual axes table. An elite is supposed to read at a glance as "this is a meaningful step up from trash"; a wide-flat ember-shape, however well-rendered, does not carry that perceptual weight regardless of how it is scaled. Upscaling 1.85× produces a *large blurry ember*; not a *visibly upgraded threat*.

**Diablo lineage check:** D2 fire-flavored elites (Hell Bovine's fire-cousin tier, Ancient Kaa, Diablo's Lesser Imps' elite-pack variants) are uniformly tall-vertical silhouettes with visible aura coding. D3's elites use the same convention — tall, distinct, with affix-coded auras. PoE's rare monsters likewise. The genre's elite-tier convention is **vertically-stacked silhouette + clear pack-presence**. A horizontal ember reads as a *fire VFX*, not as an *elite monster*. This is genre-grammar mismatch, not a scale-tuning question.

**Ruling: (c) Leave best-achievable + (b)-queue for VS2b swap.**

**Operational specifics:**
- For VS2a (now): render at scale **1.10×** (resulting body ~60 px, between the elite floor 90 px and the trash ceiling 75 px — a tier-coherence violation but the *least bad* available position; renders cleanly with nearest-neighbor; no significant upscale artifacts).
- Document the tier-coherence violation explicitly in `monster-track-integration-notes.md` and in the per-slug lookup table's flags column: `tier_coherence_violation: TRUE; planned_swap_target: Fire_Lord_Creativkind (VS2b)`.
- For VS2b: swap to **`Fire_Lord_Creativkind`** (drax MONSTER_TRACK_INTEGRATION_NOTES.md line 75: "humanoid fire boss; strong VS2b boss-tier candidate"). This is in the *boss* tier per drax's tagging, but a quick check on its intrinsic pixel size and silhouette would tell us if it can plausibly serve at *elite* tier with a lower scale. Alternatively, `Elemental_mage` (line 70, "generalist mage; VS2b element coverage expansion") may serve directly as a fire-elemental-archetype elite if its sheet is humanoid-vertical.
- Acquisition cost: zero (both candidates already in-house in the deferred-pack pool).

**Why not (a) accept quality loss:** the quality-loss at 1.85× is severe (pixel art at 1.85× upscale shows visible interpolation even with nearest-neighbor — large pixels read as *low-resolution*, not as *intentional pixel-art*), and the silhouette problem is not fixable by scale.

**Why not (d) acquire alternate vendor pack:** the in-house deferred-pack pool already contains viable candidates. Spending a Matt-acquisition request when in-house options are documented and available is premature.

**Lookup-table implication:** `fire-elemental: scale = 1.10, flag = tier_coherence_violation_accepted, planned_resolution = vs2b_swap`.

---

## Case 2 — angel-guardian (boss, 256×192)

**Diagnosis (per legolas + my PIL inspection):**
- Frame canvas: 256×192 px
- Content bbox: max over sampled frames is 240×173 px (90% of frame height; the asset uses most of its canvas vertical budget)
- Required scale for boss tier midpoint (292 px target body): 292 / 173 = **1.69×** upscale
- Required scale for boss tier floor (225 px target body): 225 / 173 = **1.30×** upscale
- Legolas reports 1.52× to reach 292 px from frame_h=192 (without bbox correction). My PIL correction (173 px body, not 192) makes the upscale slightly harsher.

But: this is **a boss**. Bosses are exactly where the genre's "intentional large-pixel render" tradition is most legible. D2's Mephisto, Diablo, Baal renders at the era's max-pixel; D3 launch's Belial / Azmodan / Diablo cinematic-tier renders were canvas-stretched and *the players loved it*; PoE's Atziri / Shaper / Sirus pixel-budgets are extreme by design. **Large pixels on a boss read as "carved presence," not as "low resolution," provided nearest-neighbor is locked and the cinematic-tier aura + name banner stack carries the perceptual weight per `enemy-visual-legibility.md` S3/S5.**

The 1.30× lower-bound is well within "clean upscale" territory; the 1.69× upper-bound is at the threshold but inside it for boss-tier presence-as-aesthetic-choice. The HD-2D register specifically supports this: Octopath Traveler's boss sprites are visibly larger-pixel than the field-explore characters by deliberate design; the HD-2D pattern *uses* that pixel-size differential as a tier signal.

**Ruling: (a) Accept quality loss.**

**Operational specifics:**
- Render at scale **1.30×** (resulting body 225 px — at the boss tier floor, conservative end of the range; produces cleanest upscale).
- Hard requirement: nearest-neighbor filtering must be confirmed active. Per legolas § 4b "Knowledge gaps not resolved" #5, this is currently unconfirmed in the Pixi.js pipeline. **Add to drax's `MONSTER_SCALE_BY_SLUG` refactor scope: explicit `texture.baseTexture.scaleMode = PIXI.SCALE_MODES.NEAREST` on all monster textures.** If nearest-neighbor is not active, bilinear upscale at 1.30× will produce blurring that breaks the "carved presence" reading.
- Cinematic-tier aura (per `enemy-visual-legibility.md` S3) is the load-bearing visual differentiator at boss tier; the pixel-art-upscale aesthetic at 1.30× supports rather than undermines that.

**Why not (b) swap:** the in-house deferred-pack options for boss-tier holy are `Angel_Mage_Creativekind` (line 79) and `angel_v1` (line 80). Neither is a clear upgrade in intrinsic-pixel-budget without further inspection; the angel-guardian asset is solid; no reason to swap when (a) is viable.

**Why not (c) leave best-achievable:** at boss tier the visual stakes are highest; a tier-coherence violation here (rendering an angel-guardian at "magic-tier body height") would directly undermine the act-boss cinematic moment.

**Why not (d) acquire:** acquisition is unjustified when the in-house asset works at 1.30× with nearest-neighbor.

**Lookup-table implication:** `angel-guardian: scale = 1.30, flag = upscale_at_boss_tier_aesthetic_intent, requires: nearest_neighbor_confirmed`.

---

## Case 3 — sword-warrior (trash, 280×280)

**Diagnosis (per legolas + my PIL inspection):**
- Frame canvas: 280×280 px
- Content bbox: max over sampled frames is **258×280 px (92% of frame height — the asset fills almost the entire canvas)**
- Required scale for trash tier midpoint (65 px body target, **legacy framing**): 65 / 258 = **0.25×** downscale
- Required scale for trash tier midpoint **proportionally re-anchored against chierit's actual ~44 px player body** (Path A above): scale ≈ 0.13×
- Drax's composite shows sword-warrior at scale 0.35 rendering at 98 px — *larger than every other monster except god-of-lightning*. Tier inversion confirmed empirically.

The legolas synthesis labeled this a "math impossibility" on the basis of "extreme downscale → fine pixel detail compressed." **That framing is wrong about pixel art's downscale behavior.** Pixel art downscales cleanly when integer ratios are honored and (especially) when downscaled with appropriate filtering. The genre has a 25-year tradition of high-resolution sprites rendered small for trash-tier mob density — this is *not* a problem. The problem is the *current scale* (0.28) is far too high for this asset's intrinsic size, producing the tier inversion drax flagged.

The actual concern at extreme downscale is **animation-frame information loss**: at 0.13× a 258 px body becomes a ~34 px body, and animation detail (sword swings, posture changes) may not be readable. But this is not a *quality-loss* concern in the upscale sense — it is a *legibility-at-rendered-size* concern, which is the **standard problem solved by ARPG trash-tier silhouette design**: trash mobs are *supposed* to be readable as silhouettes at small render size, not as detailed sprites. PoE's white-rarity mobs read as silhouettes; D2's Fallen and Quill Rats read as silhouettes; the entire trash tier reads as silhouette-first by genre convention. The sword-warrior, downscaled to trash size, will read as *a silhouette holding a sword* — which is exactly the genre-correct trash read.

**Ruling: (c) Leave best-achievable with corrected math + downscale documented as feature not bug.**

**Operational specifics:**
- Render at scale **0.25×** (resulting body ~65 px) if the original tier hierarchy holds.
- Render at scale **0.13-0.17×** if Path A re-anchor is adopted (resulting body 34-44 px, matching chierit player body).
- The "math impossibility" label should be removed from this case. It is a clean downscale; pixel art tolerates this; the sword-warrior asset becomes a *high-fidelity-source rendered at trash-tier silhouette* which is *better*, not worse, than a trash mob authored at native trash-tier pixel budget (because the silhouette stays clean and the animation frames retain enough information to read motion).
- **However:** the 280×280 frame canvas is a Pixi.js memory-efficiency concern at runtime if many sword-warriors spawn simultaneously — each instance carries the full 280×280 texture regardless of render scale. Drax/star-lord should evaluate whether trash-tier instances should pre-downsample the texture at load time (one-time CPU cost, sustained GPU/memory savings) vs. accepting the runtime cost for a small VS2a roster. Out of scope for this dispatch; flagged for follow-on engineering call.

**Why not (b) swap:** drax MONSTER_TRACK_INTEGRATION_NOTES.md line 64 lists `SpearWarrior`, `Warrior`, `Warrior_New_Color`, `Warrior_v2_with_jump` as deferred trash-tier humanoid variants. If their intrinsic frame sizes are smaller (more native to trash tier) they are viable swap candidates. But swap is not *necessary* — (c) works cleanly. The deferred warriors should be evaluated when VS2b roster expansion happens, not as a forced swap now.

**Why not (a):** "accept quality loss" implies upscale-blur. There is no quality loss at downscale for pixel art rendered with appropriate filtering. The label does not apply.

**Why not (d):** no acquisition needed; the asset is fine, the scale was wrong.

**Lookup-table implication:** `sword-warrior: scale = 0.25 (path-B) or 0.13-0.17 (path-A), flag = high_intrinsic_pixel_budget_clean_downscale, optional_optimization = pre_downsample_at_load`.

---

## Case 4 — god-of-lightning (boss, 256×256, 1-frame)

**Diagnosis (per legolas + my PIL inspection):**
- Frame canvas: 256×256 px (square)
- Content bbox: 253×212 px (83% of frame height; the asset uses near-full width and ~83% of height)
- Frame count: **1.** This is not an animation pack — it is a single static sheet.
- Required scale for boss tier (212 px body × 1.30× = 275 px target): 1.30× upscale → entirely viable, exactly the same scale as angel-guardian, same nearest-neighbor requirement.

**The scale is not the problem.** Scale is solved by the same approach as angel-guardian — render at 1.30× with nearest-neighbor; rely on cinematic-tier aura and name-banner stack per `enemy-visual-legibility.md` S3/S5.

**The blocker is the 1-frame animation budget.** `enemy-visual-legibility.md` S4 specifies that Trial-encounter / act-boss combat begins with a cinematic frame ritual *before combat* and then combat plays out. A boss rendering as a *static image* during combat is a player-experience failure that no scale-tuning can fix. Bosses are the act's culmination; they are expected to **act** — to wind up attacks, to react to hits, to die with weight. Diablo's full lineage — Diablo (1996), Baal, Belial, Malthael, Lilith — all carry weighty per-frame animation density specifically because the boss kill is the act's emotional payoff. PoE's act bosses likewise. Octopath Traveler's boss sprites animate even in their HD-2D mid-fidelity register. A static-frame boss is a Diablo-Immortal-corner-cutting decision the project should not make.

**Ruling: (d) Matt-acquisition authorization requested.**

**Specifics of the Matt-decision ask:**

> **Authorize acquisition of a god-of-lightning pack with full animation cycles (idle / attack / hurt / death minimum) from CreativeKind or alternate vendor.**
>
> CreativeKind's deferred-pack roster (drax MONSTER_TRACK_INTEGRATION_NOTES.md line 76) includes `God_of_Lightning_Dark_Version` — drax flagged this as "dark lightning variant of boss." Whether this is the same single-frame static sheet or a full animation pack is **not confirmed**. **First investigation step:** drax inspect `God_of_Lightning_Dark_Version` frame count. If it is animated, swap to it (ruling becomes (b) swap, no acquisition needed). If it is also single-frame, then the (d) acquisition is required.
>
> If (d) acquisition required: alternatives include (i) checking the CreativeKind product page for an updated/extended god-of-lightning pack since the original acquisition; (ii) substituting with `Fire_Lord_Creativkind` re-flavored as thunder (palette-shift to thunder palette per `enemy-visual-legibility.md` S2 — element is communicated via palette, not via base sprite); (iii) sourcing from a different vendor (Elthen, LuizMelo) which would require Mode-B catalogue check first.
>
> **Cost surface:** CreativeKind packs are ~$5-15 each. The Pixogen Full thunder pack mentioned in MONSTER_TRACK_INTEGRATION_NOTES.md line 91 is gated on Matt's PayPal availability. If `Fire_Lord_Creativkind` re-palette is viable, **zero acquisition cost** and the result is an in-register boss-tier thunder enemy.
>
> **Recommendation:** **(b) swap to Fire_Lord_Creativkind with thunder-palette per S2** is the cheapest, fastest, and registers-coherently. Acquisition is the fallback if Fire_Lord's intrinsic frames don't support a thunder reframe.

**Operational specifics for VS2a (now):**
- Mark god-of-lightning as **NOT-CANONICAL for VS2a boss-tier rendering.** Do not render in trial-encounters or act-boss slots.
- If a thunder boss is needed for VS2a element coverage, route to **`Fire_Lord_Creativkind` with thunder palette per S2** as the temporary stand-in pending the swap/acquisition decision.
- Document in the per-slug lookup table: `god-of-lightning: scale = 1.30 (technically viable), flag = ANIMATION_PACK_INCOMPLETE_DO_NOT_USE_IN_COMBAT, planned_resolution = matt_decision_pending`.

**Why not (a) accept:** a static-frame boss in combat is a player-experience failure; "accept" is not viable.

**Why not (c) leave best-achievable:** "best-achievable" is "render as static during combat" — same failure as (a).

**Lookup-table implication:** `god-of-lightning: scale = 1.30 [unused in VS2a], flag = animation_pack_incomplete, blocked_on = matt_decision`.

---

## Cross-case synthesis

### Vendor-side intrinsic-size pattern?

Yes — CreativeKind ships at deliberately varied intrinsic frame sizes that **do not match a unified per-tier pixel budget.** The 11-monster VS2a pool spans 64×64 (evil-eye) through 280×280 (sword-warrior) — a **4.4× spread in frame edge length** across vendor-side asset budgets. CreativeKind's design choice (per their itch.io product pages, inferred from per-pack canvas sizes) is that each monster's frame size is tuned to its individual character art's natural size, not to a horizontal cross-pack standard. This is the asset author's prerogative — but it means a buyer-side curator (Reincarnated) cannot assume the vendor's intrinsic sizes will conform to a consumption-side per-tier pixel hierarchy.

The pattern: **vendor intrinsic frame size correlates loosely (not strongly) with the monster's narrative scale.** Sword-warrior is small-character-large-frame (lots of canvas padding around the swordsman, including for swing arcs); fire-elemental is short-flat-elemental (flat-sideview design genuinely is short); angel-guardian is humanoid-tall-canvas (proportional design); god-of-lightning is square-cinematic-canvas (boss-portrait canvas). The vendor's per-asset design language varies because the assets serve different visual purposes within CreativeKind's general catalogue, not just our specific tier-pool needs.

### Broader VS2a pool curation needed?

**Yes, modest curation. No, not a wholesale re-curation.** Three of the four math-impossibility cases (fire-elemental, sword-warrior, god-of-lightning) admit non-acquisition resolutions: fire-elemental gets a (c)+queue-swap ruling using in-house deferred packs; sword-warrior gets a (c) ruling with corrected math (the "impossibility" framing was incorrect); god-of-lightning has a (b) in-house swap candidate (Fire_Lord_Creativkind with palette-shift) before the (d) acquisition is needed.

**The only case that requires Matt-decision now is god-of-lightning's animation-completeness blocker** — and even that has a likely-zero-cost in-house resolution path (Fire_Lord_Creativkind palette-shift).

What the pool *does* need is **explicit per-slug scale documentation and tier-coherence-violation flagging** — which is exactly the lookup-table this dispatch's rulings feed into. The pool composition itself is viable; the integration discipline around it is what was missing.

A modest VS2b roster-expansion review is warranted (queued as future work, not blocking VS2a):
- Evaluate `Fire_Lord_Creativkind` (boss/elite fire), `Elemental_mage` (flexible elite), `Dark_Soul_Creativekind` (dark trash), `Evil_alien_creature_1` (swarm tier — VS2a's swarm tier coverage is empty per current ENEMY_TIER_CHARACTER_MAP), `Archimage` (elite caster) for intrinsic pixel-size fit and silhouette grammar.
- Confirm `God_of_Lightning_Dark_Version` frame count (1 vs many) as the cheapest first step on the god-of-lightning Matt-decision.

### Forward Discipline / register rule for future vendor acquisitions?

**Yes. Add to the engineering disciplines or to the style-register.md operational appendix:**

> **D14 (proposed) — Vendor intrinsic-size pre-acquisition check.** Before any monster-sprite vendor acquisition is authorized, the prospective pack's intrinsic frame size and content-bbox-within-frame must be measured against the project's per-tier pixel budget (currently: trash 28-75 px body / elite 45-115 px body / mini-boss 65-180 px body / boss 113-360 px body, with the Path A vs Path B re-anchor decision pending). Packs whose intrinsic frame size requires upscale >1.3× or downscale extreme enough to lose animation-frame information for the intended tier should either (a) be declined, (b) be acquired with explicit tier-coherence-violation flagging in the integration notes, or (c) be acquired for a different tier than originally intended (per-slug scale and tier-assignment are independent design knobs). The intrinsic-size check is cheaper than post-acquisition tier-coherence remediation.

> **D15 (proposed) — Per-vendor animation-completeness gate.** Before any monster acquisition for a tier that requires animation (elite / mini-boss / boss; trash may accept idle-only initially), confirm the pack contains a minimum animation set (idle / attack / hurt / death). Static-frame or 1-frame sheets are acceptable only for trash tier where pack-cluster aura compensates for per-unit animation loss (per `enemy-visual-legibility.md` S6), and never for boss tier where the act's emotional payoff requires animated weight (per `enemy-visual-legibility.md` S4). The god-of-lightning case is the worked example of this discipline's necessity.

These two disciplines together would have caught the fire-elemental tier mismatch and the god-of-lightning animation gap **before integration time**, deferring those acquisitions or flagging them for replanning before the per-slug scale-tuning gate was hit. The cost of authoring the disciplines is small; the saved cycle time on each future acquisition is substantial.

**Authorship:** these disciplines belong in `reincarnated-engine/design/working-agreement/engineering-disciplines.md` per jack-ryan's discipline-authoring lane, with cross-reference to this doc and to `style-register.md`. I recommend gandalf-and-jack-ryan-co-author per the design-track-quality-track pairing pattern. Knight-rider to sequence.

---

## Matt-decision queue (surfaced by these rulings)

1. **Path A vs Path B tier-hierarchy re-anchor decision** (load-bearing — see § "Empirical correction" above). Affects every per-slug scale factor in the eventual lookup table. Without this decision, the lookup-table values are provisional.
2. **god-of-lightning resolution path:** (b) swap to `Fire_Lord_Creativkind` with thunder-palette per S2 (recommended; zero cost), or (b) swap to `God_of_Lightning_Dark_Version` if drax inspection confirms it has animation frames (low-cost research, in-house), or (d) acquire alternate vendor pack (recommended only as fallback; per-pack cost ~$5-15).
3. **D14 + D15 discipline authoring authorization** (recommended; small effort; substantial forward-cost-savings).

None of (1)-(3) blocks the per-slug lookup table's *structure* — they affect specific values and forward-process discipline. The lookup table can proceed against the rulings above with explicit "Path A vs Path B pending Matt-decision" annotations.

---

## Cross-references

- `agentic_orchestration/research/knowledge/character-monster-pixel-scale-2026-05-16.md` § 4c — the math-impossibility flags this doc resolves
- `agentic_orchestration/gandalf/findings/2026-05-16-monster-scale-inspection-strip-notes.md` — empirical composite reference
- `agentic_orchestration/dispatches/2026-05-16-gandalf-math-impossibility-rulings.md` — the dispatch this doc fulfills
- `/Users/admin/Games/reincarnated-demo/MONSTER_TRACK_INTEGRATION_NOTES.md` — deferred-pack roster for option-(b) candidates
- `canonical/story/style-register.md` — HD-2D-pixel register lock; the consumption-time filter these rulings honor
- `canonical/story/enemy-visual-legibility.md` § S1-S6 — tier-coded perceptual architecture
- `canonical/story/gandalf-design-lineage.md` Layer 2 — Diablo I/II/III/IV/Immortal lineage informing boss-presence + tier-silhouette grammar
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — destination for proposed D14 + D15

---

## Maintenance protocol

When the per-slug lookup table lands (gandalf in-flight authoring), these rulings are consumed and the per-slug table becomes the canonical reference. This doc remains the **rationale-of-record** for why each ruling was issued.

When VS2b roster expansion happens, the swap-target queue from this doc (Fire_Lord_Creativkind, Elemental_mage for fire-elemental; Fire_Lord/God_of_Lightning_Dark_Version for god-of-lightning) is the starting candidate list.

When Matt resolves the Path A vs Path B re-anchor decision, the scale factors recommended in cases 1-3 here are recalibrated proportionally; the rulings themselves (which category, which rationale) do not change.

**Path A-prime supersession 2026-05-16 Day-4 close — rulings status update:** Matt-confirmed Path A-prime (ARPG-vs-JRPG reframing per `canonical/story/per-slug-scale-lookup-path-a-prime-2026-05-16.md`) anchors chierit at uniform 2.5× (mean rendered figure-content ~108 px; ARPG 100–130 px band). The four rulings here remain valid in rationale; specific scale-factor recalibrations under Path A-prime are operationalized in the v2 lookup table. Notably: Case 1 (fire-elemental) — upscale 2.29× height-priority with rendered-width 346 px (vs v1 Path A's 0.85× downscale at 128 px width); tier-coherence violation persists; planned VS2b swap to Fire_Lord_Creativkind priority-bumped. Case 2 (angel-guardian) — upscale 2.06× returns (vs v1 Path A's clean 0.75× downscale); Case 2's original "boss-tier-aesthetic-intent + nearest-neighbor HARD REQ" rationale resurfaces as load-bearing (was dissolved under v1 Path A). Case 3 (sword-warrior) — downscale severity reduced (0.33× at Path A-prime vs 0.13× at v1 Path A); still trash-tier silhouette-readable. Case 4 (god-of-lightning) — palette-shift `Fire_Lord_Creativkind` to thunder palette confirmed Matt-locked; god-of-lightning removed from active VS2a roster. Decision 1 god-of-lightning resolution = closed.

---

## Case 4 — re-amendment 2026-05-17 (Day 4 evening into Day 5 close) — Option 3 (mini-boss tier-bump) ruling

**Empirical update:** Legolas Fire_Lord intrinsic-size measurement returned 2026-05-17 (~35 min Mode A; doc `agentic_orchestration/research/knowledge/character-monster-pixel-scale-2026-05-16.md` § Section 2a + § Section 4e). Fire_Lord canvas is **128×128 px** (NOT 256×256 as the prior Case 4 closure assumed). Idle content 45 px; combat-stable 76 px; peak-attack 122 px (atk4 frame 13 brief). Fire_Lord is **architecturally elite/mini-boss-sized, NOT boss-tier-sized.**

**Math impossibility:** Path A-prime boss tier needs 287-460 px persistent presence. Fire_Lord cannot achieve within viable upscale limits:
- Idle-anchor to boss-mid: 8.22× scale → canvas 1052 px (viewport infeasible)
- Attack-peak anchor: 3.03× scale → idle 136 px (reads ELITE not boss; persistence mismatch)
- Best-achievable: 2.35× → atk4 peak hits boss floor 287 px; idle 106 px above-elite (tier-coherence violation)

**The prior Case 4 closure (palette-shift Fire_Lord to thunder boss) is mathematically infeasible per the empirical measurement.** Case 4 closure REOPENED.

**Ruling: Option 3 (mini-boss tier-bump) — Matt-confirmed 2026-05-17 ("yes to all four").**

### Rationale

#### (a) Thunder element retains monster representation
Without thunder-tier monsters in the gauntlet, thunder exists only as Lightning Ronin player-class skill. Genre canon (D2 Lightning Demon / Wraiths; D3 lightning-affixed elites; PoE lightning monsters at every tier) expects thunder presence across the monster roster. Option 2 (drop entirely) breaks this; Option 3 preserves it at mini-boss tier.

#### (b) Boss-tier diversity loss is acceptable for VS2a
VS2a is a single gauntlet, not multi-act content. Gauntlet genre canon ships with one-to-two boss-tier encounters per pass (D3 Rifts; PoE pinnacle bosses). Boss tier with angel-guardian-only is structurally fine for VS2a's scope. The Trial encounter (player-class mirror per `cosmology-reincarnated.md`) is structurally distinct from gauntlet boss-tier diversity, so the canonical season-defining moment is unaffected.

#### (c) Fire_Lord asset utility preserved across roster
Fire_Lord serves Case 1 (fire-elemental elite swap; V5 fire/orange variant at 2.93×) AND Case 4 reopened (thunder mini-boss slot; V1 blue/purple variant). One asset, two slots, both clean. Zero acquisition cost.

### Scale + anchor specification (Path A-prime mini-boss tier)

- **Tier target:** mini-boss range 173-230 px persistent presence; midpoint 201 px (per per-slug v2 doc § Part 6.3)
- **Fire_Lord V1 thunder:** intrinsic idle content 45 px; combat-stable 76 px; peak-attack 122 px
- **Anchor selection:** **combat-stable (76 px)** — required scale **2.64×** lands idle at 201 px (mid-tier) when in combat stance, pre-combat reads slightly smaller. Sub-3.0× preserves pixel-art-coherent rendering with nearest-neighbor; reads as "monster grows/lessens through combat cycle" rather than "monster oversized for tier"

**Rejected anchor alternatives:**
- Idle-anchor (45 px) → 4.47× scale: above 3.0× clean-upscale ceiling; nearest-neighbor produces visible chunky-pixel-block scaling
- Peak-attack anchor (122 px) → 1.65× scale: idle reads 74 px (above elite 150 ceiling; below mini-boss 173 floor); excessive read-band variance

**Recommended scale: 2.64× (combat-stable anchor).**

### Anchor-offset bundling

Legolas finding: Fire_Lord idle floats 24-33 px above frame bottom (frame-bottom anchor with above-bottom padding). At 2.64× scale this becomes ~63-87 px rendered float — operationally visible. **Bundle anchor-offset correction (~`+25` source-px → ~66 px rendered offset) into the same drax MONSTER_SCALE_BY_SLUG refactor scope alongside Ground Monk's 15 px float + Case 1 fire-elemental's ~70-97 px float concern.** Three monsters with anchor-offset corrections; one refactor pass.

### Slot-routing implication for `ENEMY_TIER_CHARACTER_MAP`

- `god-of-lightning` slug **removed** from boss-tier slot
- `fire-lord-thunder` (slug naming drax's call) **added** to mini-boss-tier slot
- Mini-boss tier composition: `lich` (necrotic) + `hellfire-rhino` (fire) + `fire-lord-thunder` (thunder) — three mini-boss-tier monsters with healthy element diversity
- Boss-tier composition: `angel-guardian` only for VS2a

### Drift-11 sibling-cluster-sweep prescription honored

Per Drift-11 prescription (codified 2026-05-16 amendment): when a deferred milestone surfaces ONE upstream-of-near-term-ship dependency, sweep the rest of the deferred milestone for sibling dependencies in the same session. This Case 4 amendment is the sibling-cluster surfacing of the existing math-impossibility cluster (Cases 1-3). Filed into rulings doc rather than treated as net-new finding.

### Carry-forward

- Drax MONSTER_SCALE_BY_SLUG split-dispatch endorsed (Matt-confirmed 2026-05-17): Case A (fire-elemental V5 at 2.93× + Ground Monk anchor + chierit 2.5× + bbox-tightened + nearest-neighbor) ships **immediately**; Case D (fire-lord-thunder V1 at 2.64× + slot-routing remap god-of-lightning → boss-tier-empty + Fire_Lord-thunder → mini-boss tier + anchor offset bundling) ships **separately** after this ruling commits
- Decision 1 (god-of-lightning resolution) status: **closed via Option 3 mini-boss tier-bump** (was: closed via palette-shift Fire_Lord to thunder boss; superseded by empirical Legolas measurement)
- Per-slug Path A-prime doc (`canonical/story/per-slug-scale-lookup-path-a-prime-2026-05-16.md`) needs follow-on amendment by gandalf or v2-instance: god-of-lightning row removed from boss-tier section; fire-lord-thunder row added to mini-boss-tier section. Bundled into next gandalf authoring window.

When D14 + D15 disciplines land in engineering-disciplines.md, cross-reference from here.

— gandalf, 2026-05-16 (Path A-prime supersession status update appended Day-4 close)
