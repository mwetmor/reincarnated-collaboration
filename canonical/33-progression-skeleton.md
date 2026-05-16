# 33 — Progression Skeleton (immutable + decided only)

**Captured:** 2026-05-11
**Status:** Empty skeleton tracking the **structural shape** of Reincarnated's progression system. Contains ONLY (a) immutable substrate from `foundation.md` and (b) decisions already locked. Everything still under discussion lives in **`32-progression-design.md`** — when a decision lands there, it migrates here as a filled section.

**Read order:** start with file 32 for context and discussion; this file is the deliverable.

## Cross-references

- `32-progression-design.md` — companion discussion doc; open questions live there
- `28-engine-arpg-rebalance-design.md` § B9 — endgame math (skill points, traits, reset)
- `17-gear-and-spirit-guide-design.md` — gear progression endgame baseline
- Engine `docs/foundation.md` — immutable 50-tier substrate

---

## Immutable substrate

These are foundation-level commitments — built into the engine and not subject to revision.

### Power scale
- **50-tier power scale aligned with character levels** — a level-50 character uses tier-50 abilities and gear (`foundation.md` line 156).

### Attributes
- Six attributes: **STR, DEX, INT, WIS, VIT (CON), AGI** (AGI currently dead/reserved per decisions-log 2026-05-09).
- Per-attribute scaling targets the math model recognizes (`foundation.md` line 421).

### Resource energy types
- Five: **mana / rage / combo / focus / stamina-as-resource** (Phase 1 of dimensional refactor; decisions-log 2026-05-08).

### Canonical elements
- Six: **physical / fire / wind / water / earth / hybrid** (decisions-log 2026-05-08; no expansion planned).

---

## Decided — progression philosophy (Section 1 RESOLVED 2026-05-11)

### Progression model
- **XP-primary hybrid.** 100 skill points from XP-driven leveling (2 per level × 50 levels) + 20 skill points from quest/boss/Trial-body-swap milestones.

### XP sources (four)
1. **Monster kills** (genre-universal)
2. **Quest completion XP** (D2-style flat XP on top of any skill-point reward)
3. **Discovery / exploration XP** (D4 Renown-adjacent — visiting waypoints, finding altars, etc.)
4. **Trial body-swap completion XP** (Reincarnated-distinctive — defeating Trial boss + electing swap grants meaningful XP)

### Trial body-swap reward bundle (per act)
Each Trial body-swap is a "mini ascension" granting permanent character rewards:
- **XP** (act-scaled)
- **Global resistances** (permanent buff; +X% to all six element resistances per body-swap)
- **Skill point(s)** — 1 per Trial body-swap in early acts; more than one in later acts (specific scaling deferred to Section 11)

### Death penalty model (body-swap-offered with seasonal-death consequences) ⭐ Reincarnated-distinctive
Death pauses → player offered body-swap to a previously-defeated boss form.

| Choice | Consequence |
|---|---|
| **Refuse swap** | Normal respawn + small XP loss (5-10% to next level — specific value TBD at engine impl); **no gear durability damage; no gold/currency drop** |
| **Accept swap** | Dead class is **permanently lost for the current season** (cannot be played again this season) AND **cannot be ascended to Earth realm at season end** (cannot enter form library for future seasons) |

The trade-off is real: keep playing this character (refuse, accept XP loss) vs commit to a new form (accept, lose this class forever for the season).

**Distinct from Trial body-swap.** Trial swaps are mini-ascensions with positive rewards. Death body-swap is the harsh-consequence alternate path. **No mainstream ARPG uses death-as-meta-progression-choice in this form** — this is a Reincarnated design pillar.

### Trial encounter mechanics — two paths chosen upfront (LOCKED 2026-05-11)
Each Trial encounter presents two paths the player chooses BEFORE fighting:

| Path | Fight | Outcome on win | Reward |
|---|---|---|---|
| **Body-swap path** | LLM-generated Trial boss (a fresh class) | Transform into that class identity | Full XP + full SP + full resistances (+10%) |
| **Doppelganger path** | Mirror of current class (self-fight; "your doppelganger/shadow") | Stay as current class identity | 1/4 XP + half SP + half resistances (+5%); remaining claimable via end-game quest |

**Net total rewards equal across both paths over a full season** (doppelganger path uses end-game quest to catch up). Pacing differs: body-swap path is faster; doppelganger path preserves chosen class identity.

**Reincarnated-distinctive design pattern.** Engine cost is minimal — doppelganger fights reuse the class-as-Trial-boss machinery already in the engine (the doppelganger is the player's current class deployed as a Trial-boss-tuned opponent).

### Body-swap pool dynamics (LOCKED + CORRECTED 2026-05-11)

**Within-season body-swap target pool:**
- Engine generates ~8-9 classes per season (per file 29: 5-6 playable + 3 act-boss)
- Pool starts at (N − 1) = ~7-8 at season start (all generated classes minus the starter)
- **BOTH Trial body-swap AND Death body-swap shrink the pool by 1** (abandoned class "left behind"; cannot return)
- **Doppelganger path (Trial refuse) does NOT shrink the pool** (player stays as same class)
- First-time players have death-body-swap available from session 1 — pool is within-season-generated

**Trial body-swap framing:** the bonuses (XP/SP/resistances) are "to progress your new class faster than you could have the old one" — a forward-looking transformation, not a punishment.

### Form library acquisition (LOCKED 2026-05-11; CORRECTED — library is CROSS-SEASON, separate from body-swap pool)
- **Only ONE form ascends to Earth realm per season** — the form alive at season end (the one the player has been actively playing)
- Trial-body-swapped-from classes are **lost for the season** — not ascended (you've moved on)
- Death-body-swapped-from classes are **lost AND cannot ascend** (dying spirit forbidden from library)
- Doppelganger-path Trials don't add forms to library either (you didn't body-swap into the Trial boss)
- **Library is slow-accumulating:** ≤1 form per season; over N seasons, library size ≤ N
- **Library purpose:** Earth Self meta-layer — see below
- **Strategic tension:** "play one class to mastery and ascend that" vs "body-swap for power gains but ascend a less-mastered form"

### Earth Self meta-layer (decided concept; far-future implementation)

**Reincarnated Phase 0 = the SEASONAL JOURNEY portion of a larger eventual game.**

- **Earth Self** = player's persistent identity living on Earth (the meta-layer hub; not in current development)
- **Seasonal journey = descent.** Earth Self body-swaps into a seasonal spirit form for a time-bound journey
- **Ascension = return.** Goal of seasonal journey: ascend the most meaningful life back to Earth as a Spirit form
- **Form library = accumulated ascended spirits** on Earth Self — gacha-style accumulation of LLM-generated unique spirits
- **Earth-layer events (eventual; not Phase 0):** PVP / PVE guild events, usually in the rift (liminal space), defending against third-faction monsters
- **Earth gameplay loop TBD:** MOBA / Pokemon Battles / Arena Style / other combinations
- **Multiplayer scope refinement:** out of scope for SEASONAL play indefinitely; envisioned for Earth meta-layer events post-Phase 0
- **Full vision: `../collaboration-handoff/34-earth-meta-layer.md`** (to be drafted)

### Act structure (locked 2026-05-11)
- **3 acts per game** (supersedes file 29's prior "4, 5, or 6" open decision)
- **Per-act level bands:** A1: 1-17, A2: 18-33, A3: 34-50 (~17 levels per act)
- **1 Trial body-swap opportunity per act = 3 per season**
- **Per-act SP scaling: 4 / 7 / 9 = 20 SP** from milestones (LOCKED)
- **Trial body-swap is the SOLE milestone-SP source.** Non-Trial quests grant XP-only.

### Global resistance system (LOCKED 2026-05-11 — Option C, within-season cap)
- **Within-season cap: +75% all-element resistances** (standard ARPG endgame resist cap)
- **From Trial body-swap path:** +10% per Trial × 3 = +30% max from milestones in a season
- **From doppelganger path:** +5% per Trial × 3 = +15% immediate; remaining +15% claimable via end-game quest
- **From gear: ~+45% required** to reach the +75% cap (resistance affixes on equipment loadout)
- **No cross-season resistance accumulation** — each season starts at +0% baseline; form library carries class identity only, not stat state
- **🔗 New gear-generation constraint:** gear schema must support resistance affixes summing to ~+45% all-element across a full equipment loadout. Matches PoE per-piece resistance rolling pattern. Affects file 17 + B5 + B12 scope.

### Anti-patterns to actively reject
- ❌ Paragon-style infinite grind (D3/D4 paragon doesn't fit one-week seasons)
- ❌ Mandatory respec gold (PoE Orbs of Regret; conflicts with B9c)
- ❌ Level-locked content gates (D3 GR-tier prerequisite friction)
- ❌ Skyrim-style full player-level monster scaling (anti-pattern per genre consensus)
- ❌ Hardcore mode as launch requirement (defer post-launch)
- ❌ Mid-game balance debt acceptance — explicitly REJECT via multi-band sim (Section 8 → Option β commitment)

## Decided — character level + XP curve (Section 2 RESOLVED 2026-05-11)

### XP curve
- **Smooth polynomial** (D2 lineage scaled to 50 levels)
- Polynomial exponent ~2.0-2.5; specific per-level values tuned during engine impl
- Hits "Act-1-quick / Act-3-substantial" naturally

### Level cap
- **Hard cap at L50** (no Paragon-equivalent; anti-pattern locked Section 1)
- **Free pre-cap leveling** (no per-act soft caps); overleveling earlier acts is fine
- Multi-band sim (B14) provides confidence at L17/L33/L50 specifically

### Body-swap and level
- **Player level inherits across body-swap** (Trial or Death). Body-swap = class change, NOT character reset
- Trial body-swap bonuses (XP + SP + resistances) apply ON TOP of inherited level state
- **SP allocation resets at body-swap** (per B9c reset trigger): player re-allocates total earned SP across new class's tree
- Spirit Guide recommends starting distribution on new tree for current band

## Decided — stat progression (Section 3 RESOLVED 2026-05-11)

### Allocation model
- **Auto-allocate per class identity** (D3-style)
- Class generator determines stat growth per archetype (fire mage → INT-heavy; warrior → STR-heavy; etc.)
- **No player stat allocation**
- Reasoning: player-agency thesis is about SKILLS/BUILDS not stats; shaped-balance philosophy locates variance at skill/gear/trait level

### Reset rules
- N/A — auto-allocation; no player reset applicable

### Stat points per level
- N/A — engine determines per-class growth rates

### Diminishing returns
- Existing soft caps preserved: `DODGE_CHANCE_CAP = 0.60`, `CRIT_CHANCE_CAP = 0.75`
- Additional caps documented during engine impl as patterns surface

## Decided — ability progression (Section 4 RESOLVED 2026-05-11)

### Trait acquisition
- **Auto-unlock all traits at floor** (L1, L12, L25, L38) — no player choice within pool
- **Auto-rank with character level** — traits scale per B9a calibration; reach max rank=4 at L50
- Player does NOT invest skill points in traits — traits are passive class-identity

### Skill availability over time
- **All skills in class kit visible from L1** — player can see the full tree from start
- **Investment gated by tier-unlock structure** (see Hierarchical Skill Tree below)

### Trait stacking
- **Additive across all sources** — same trait name from gear + progression + aspects stacks additively
- Genre-standard pattern

### Hierarchical Skill Tree with Dimensional Threading ⭐ Reincarnated-distinctive

Each class kit organized as a TREE structure with:

**4 TIERS (vertical / power axis):**
- Tier 1 — Primaries (3-5 skills, spammable, L1 available)
- Tier 2 — Mids (3-5 skills, medium cost)
- Tier 3 — Advanced (2-4 skills, build-defining)
- Tier 4 — Keystones (1-3 skills, ultimates)

**2-4 CHAINS (horizontal / thematic axis):**
- Each chain runs vertically through some/all tiers
- Each chain has LLM-named thematic continuity + color palette coherence
- **Chain count varies per class** (specialists 2 chains × 4 tiers; generalists 4 chains × 3 tiers; asymmetric depths allowed) — supports archetype emergence

**Hierarchical unlock gates:**
- Tier 1: L1 always
- Tier 2: ≥3 ranks invested in any Tier 1 parent
- Tier 3: ≥5 ranks invested in any Tier 2 parent
- Tier 4: ≥8 ranks invested in any Tier 3 parent

**Cross-chain unlock asymmetry (encodes archetype identity):**
- **Multi-element classes:** ANY Tier N parent skill unlocks Tier N+1 (cross-chain investment counts)
- **Single-element classes:** Only SAME-CHAIN Tier N parent unlocks SAME-CHAIN Tier N+1 (strict chain investment)

**Smooth rank cap (preserved):**
- `rank_cap_per_skill = min(15, floor(level/3.33))`
- L17 → cap 5; L33 → cap 10; L50 → cap 15
- Combined with tier gates: Tier 4 unlocks naturally around L27

**Tier-specific scaling coefficients:**
- Tier 1: 1.05-1.08 per rank (modest)
- Tier 2: 1.08-1.12 (moderate)
- Tier 3: 1.12-1.18 (strong)
- Tier 4: 1.18-1.25 (very strong — keystone payoff)

**Build patterns that emerge:** Pure-chain specialist / Two-chain balanced / Cross-tier hybrid / Keystone-rusher — multiple viable paths from 120 SP × tree × smooth cap × tier coefficients.

## Decided — character progression

### Endgame character level
- **Level 50** = endgame baseline (B9 series).
- Engine balance loop converges classes against level-50 state with full progression applied.

### Skill point budget
- **120 total at endgame** (B9b).
- **Sources:** 100 from levels (2 per level × 50) + 20 from quests/act-bosses.
- **Per-skill cap:** 15 points (hard cap or diminishing returns above).

### Kit size
- **10-15 skills per class** (variable per archetype):
  - Approachable archetypes (warrior, brute, simple casters): 10-11
  - Standard archetypes (single-element mages, hunters, controllers): 12-13
  - Complex archetypes (hybrid_mage, multi-element specialists): 14-15
- **Math implication:** 120 ÷ 15 = ~8 fully-maxable skills regardless of kit size — every kit forces meaningful endgame allocation.

### Trait pool
- **5-10 traits per class**, archetype-appropriate (B9a).
- **Acquisition floors:** 1, 12, 25, 38 (distributed across pool).
- **Max trait rank:** 4 (typically; per-trait `max_trait_level` may vary).
- **Calibration intent:** all eligible traits reach similar power at character level 50, regardless of acquisition floor.
- **Higher-floor traits start more powerful AND ramp faster** (less character-level runway → steeper per-rank gain).
- **Endgame baseline:** balance loop assumes all eligible traits at max rank.

### Per-skill scaling coefficients
- Engine-determined per skill (B9b).
- Typical ranges by role:
  - Primary attack (spammable): 1.05-1.10 per point
  - Burst spender: 1.10-1.15 per point
  - AOE: 1.10-1.15 per point
  - Ultimate / heavy CD: 1.15-1.20 per point
  - Sustain / defensive: 1.05-1.10 per point

### Optimal skill distribution
- Engine computes optimal 120-point distribution per class as the **"meta build"** during balance loop (B9b).
- Player can use meta or experiment.
- Recorded in export packet for Spirit Guide use during play.

### Build reset mechanism (B9c)
- **Strict during play.** Free reset only on specific triggers:
  - Spirit Guide intervention when player is "struggling"
  - Body swap (taking defeated Trial boss's identity; full reset implicit)
  - End-game completion
  - Refusing body swap when offered (incentive: refuse swap = free guided reset)
- **Paid endgame.** Post-completion: pay commodities (currency / crafting materials / unique resources TBD) to reset and replay.

### Spirit Guide as build coach
- Extends from gear marginal-value math (Phase 5.5f) to skill point and trait recommendations.
- Surfaces recommended skill point allocations on the tree at reset moments.
- Displays "current vs recommended" delta using the existing **Strong / Solid / Marginal / Sidegrade / Downgrade** signal language (matches gear UI).

---

## Decided — gear progression

### Tier rarity
- **Five tiers:** common / uncommon / rare / epic / legendary (`17-gear-and-spirit-guide-design.md` § "Tier gradient").
- **LLM naming gradient:**
  - Common / uncommon: template-named (no LLM call)
  - Rare: LLM-named (first tier where uniqueness matters)
  - Epic / legendary: full LLM treatment (name + flavor + visual prompt)

### Equip gating
- **Stat-threshold gating** via calibrated `stat_requirements` (decisions-log 2026-05-09 — Option C).
- `class_fit_profile` retained for affix coherence + Spirit Guide marginal-value ranking (not hard eligibility gates).

### Loot economy
- **Endgame baseline:** `END_GAME_DROPS_PER_SLOT = 50` (file 17 line 80).
- **70/30 smart-loot / pure-RNG hybrid** (file 17 § "Loot economy model" 2026-05-10).
- **One-week seasons** (file 17 loot economy model).

### Legendary mechanical novelty (B5)
- Legendaries carry mechanical effects, not just larger stats:
  - `granted_ability` on weapons (7th hotbar slot)
  - `aura` on armor/shield/accessories (passive tick)
  - `on_hit` on weapons (chance proc)
  - `cast_on_attack` on weapons (deterministic Nth-attack trigger)
- All legendaries grant abilities (variable richness — some procs, some full skills).
- **7th hotbar slot pattern** (not replace-existing).

### Gear slots (LOCKED 2026-05-11 — 10 slots final)
1. Main hand weapon (1H or 2H per handedness)
2. Off-hand (shield/orb/focus/off-hand-weapon/grimoire — 1H weapons only)
3. Head (helmet for heavy; hood for caster — archetype-gated)
4. Chest (chest for heavy; robe for caster — archetype-gated)
5. **Hands (gloves)** — NEW per B12
6. **Feet (boots)** — NEW per B12; primary movement speed source
7. **Belt** — NEW per B12
8. Ring 1 (2 ring slots — matches D3/D4/PoE)
9. Ring 2
10. Amulet

### Tier-availability + drop curves (Section 5 RESOLVED 2026-05-11; implementation locked to B16 in Stage A2 — 2026-05-12)

**Monster-level-tied drop rates per band:**

| Band | common | uncommon | rare | epic | legendary |
|---|---|---|---|---|---|
| A1 (L1-17) | 70% | 25% | 4% | 0.9% | 0.1% |
| A2 (L18-33) | 50% | 30% | 15% | 4% | 1% |
| A3 (L34-50) | 30% | 30% | 25% | 12% | 3% |

Per-monster-tier multipliers: elite ~1.5× rare; boss ~3×; act-boss ~10× legendary.

**Power-score curve:** polynomial matching XP curve (level^2.0-2.5 shape).

**ilvl as separate axis (LOCKED):** gear stamps with ilvl at drop time; affix-tier gating on ilvl; equip = stat_thresholds + character_level ≥ ilvl - 3. Cross-season smuggled gear retains ilvl.

**`*_DROPS_PER_SLOT` per band:**
- L17: 10 drops/slot
- L33: 25 drops/slot
- L50: 50 drops/slot (existing B9b lock)

**Smart-loot:** constant 70/30 across all bands (no phase shifts).

**Implementation: B16 (Stage A2)** ships the drop event mechanism + per-band rarity tables + per-tier multipliers + smart-loot 70/30 + ilvl tracking + drop pool integration + telemetry hooks. Demo: drops render in world + auto-pickup with rarity filter. See `28-engine-arpg-rebalance-design.md` § B16 for full scope. Cross-season smuggling integration + loot economy validation simulation defer to Stage A7 (Earth meta-layer + post-Phase-0 work).

### Cross-season smuggling (basic principles LOCKED 2026-05-11)
- Smuggling exists (body-swap pillar)
- Smuggled gear retains ilvl
- Capacity limited (preserves rarity)
- Specific capacity number deferred to Earth meta-layer doc (`../collaboration-handoff/34-earth-meta-layer.md`)

### Seasonal Sets ⭐ Reincarnated-distinctive (NEW 2026-05-11)

- **One unique set per playable class, generated per season** (5-6 sets per season)
- Sets are class-specific (only fit one class's archetype + stat requirements)
- Set pieces drop ONLY at L50 endgame
- Set pieces are individually rare (legendary-tier or above)
- Set bonuses at multi-piece thresholds: 2-piece / 4-piece / full-set
- Real seasonal goal: gather your favorite class's weekly seasonal set
- Form library trophy value: set-wearing ascended spirits = visible accomplishment + Earth meta-layer event power
- LLM cost: ~+$1-2/season for set naming + flavor + visuals
- **See file 28 B15** (Seasonal Sets) queue item

### Auto-pickup with rarity filter (LOCKED 2026-05-11; ships Stage A3 demo follow-on)

- **Common / uncommon:** auto-pickup → auto-convert to gold/currency (no inventory friction)
- **Rare / epic / legendary:** auto-pickup → inventory; Spirit Guide marginal-value review at room/encounter end
- Player-adjustable rarity threshold in settings
- Engine cost: zero (uses existing rarity data + Spirit Guide math)
- Demo cost: ~3-5 days (UX + rarity filter + summary screen)

### Pet system (DESIGN INTENT LOCKED; specific scope deferred — 2026-05-11)

Captured per Matt's directive:
- Pet picks up gear; brings to Spirit Guide for review (replaces/enhances auto-pickup eventually)
- Pet takes one inventory slot
- Pets drop with seasonal rarities (gacha extension on top of class/spirit accumulation)
- Pet persists across body-swap (loyal companion regardless of class transformation)

**Status:** parked for focused later sprint (~4-6 weeks scope when shipped). Likely Track B / demo2 territory. Memory: `project_pet_system.md`.

---

## Decided — leftover edge-case closures (RESOLVED 2026-05-11)

### Death during Trial-boss encounter (Section 9 #3)
- Trial encounter resets on death; boss HP refreshes; player re-attempts
- Death body-swap offered as normal (refuse-respawn or accept-swap)
- Trial path choice can be re-made on retry (body-swap vs doppelganger)
- Trial body-swap opportunity persists until Trial is completed

### Pool depletion edge cases (Section 9 #6)
- **Pool ≥ 2:** standard multi-choice body-swap
- **Pool = 1:** single-choice body-swap (player picks accept or refuse-respawn)
- **Pool = 0:** death body-swap UI unavailable; only refuse-respawn remains
- **Trial body-swap NOT affected** by pool depletion (Trial boss is specific encounter)

### Trial body-swap XP grant framing (Section 11 #4)
- **Framing: % of XP-to-next-level at the band** (auto-scales with polynomial XP curve)
- A1: +50% (full path) / +12.5% (doppelganger immediate)
- A2: +75% / +18.75%
- A3: +100% / +25%
- Total ≈ 2.25 levels' worth of XP across season (spread across 3 acts)
- Specific multipliers are tuning starting values; framing is the architectural lock

## Decided — Section 6 + 7 closures (RESOLVED 2026-05-11)

### Scaling philosophy (Q6.1)
- **D2/PoE-style FIXED-PER-BAND** (implicit via per-band monster pools)
- Monsters in A1 band have A1 stats and don't rescale when player overlevels
- Preserves zone identity (no D3-style full player-scaling)

### Trial boss level binding (Q6.2)
- **Level-bound at season-generation; no rescaling at encounter**
- A1 Trial boss = L17-band ilvl; A2 = L33; A3 = L50
- Trial bosses are class-converged opponents; rescaling distorts convergence

### Doppelganger level binding (Q6.3)
- **`doppelganger_level = max(player_level, trial_boss_band_level)`** + handicap (+20% HP / +10% damage)
- Minimum-gated at Trial bound level — prevents underlevel-rush exploit
- Overleveled players face appropriate mirror match scaled up

### Class identity preservation (Q7.1)
- **Identity is a trajectory.** Class shape (element distribution, kit composition, trait pool) preserved across bands
- Early-game version IS the class — expressing its early-game shape
- L17 fire mage = "fire mage with early kit"; L50 fire mage = "fire mage with full keystones"

### Doppelganger as alignment-validation tool (Q7.2)
- **+3 doppelganger validation runs added to B14** (one per band × class-vs-self mirror)
- B14 total convergence runs per class: 6 (kit+variance) + 3 (doppelganger) = **9 runs**
- Validation doppelganger at band level (L17/L33/L50) — different from runtime player-level mirror
- Catches class-internal balance holes that gauntlet-convergence alone misses

### Spirit Guide cross-phase coaching UX (Q7.3)
- **Act-transition proactive surfacing** ("Welcome to Act 2 — Spirit Guide has refined recommendation")
- **Reset-moment surfacing** (B9c reset triggers)
- **🆕 Auto-reset recommendation:** if band-meta build differs significantly from player's current build, Spirit Guide proactively offers a free skill reset to accelerate alignment
  - **NEW B9c free-reset trigger:** "Spirit Guide proactive recommendation at act transition"
  - Divergence heuristic: >30% of SP would need to relocate for new meta (engine-impl detail)
  - Player can decline — recommendation, not mandate

## Decided — enemy / monster progression

### Tier structure (B10)
- **Seven tiers:** swarm / magic / trash / elite / mini-boss / boss / act-boss.
- **HP / damage multipliers** (relative to baseline):

| Tier | HP scale | Damage scale | Count per room |
|---|---|---|---|
| swarm | 0.10× | 0.20× | 5-12 per pack |
| magic | 0.25× | 0.40× | 1-3 per pack |
| trash | 0.5× | 0.6× | 1-2 per room |
| elite/rare | 1.5× | 1.2× | 1 per elite room |
| mini-boss | 4.0× | 2.0× | 1 per mini-boss room |
| boss | 8.0× | 3.0× | 1 per boss room |
| act-boss | 10×+ | 3.5× | 1v1 final encounter |

### Boss combat
- **Boss fights stay 1v1** (B10 — genre convention preserved across D2/3/4 + PoE).

### Gauntlet shape (B10)
- **10-12 room generated act** per "act" (replaces the 7-wave linear gauntlet).
- **Composition target:** ~70% trash + ~20% magic/mid + ~10% elite+.
- **Mob density target:** ~80-100 mobs per minute of clear.
- **Trash room clear-time:** 5-15s; elite room: 30-60s; boss: 30-60s; act-boss: 60-120s.

---

## Decided — movement and mobility (2026-05-11)

### Base movement speed (B12)
- **Movement speed is NOT stat-driven.** STR/DEX/INT/WIS/VIT/AGI do not affect base movement speed. AGI must NOT be revived for movement speed despite being currently dead/reserved.
- **All classes can speed run at endgame.** Base movement speed is class-agnostic.
- **Boots is THE primary gear slot for movement speed affix.** Boots have a decent chance to roll a movement speed primary modifier when generated.
- **Engine emits `movement_speed` per class and per monster tier** (queue: B12). Eliminates the current demo-side `speedForProfile` workaround that synthesizes speed from `range_profile` (which is stat-by-proxy).

### Active evasion + mobility abilities (B13)
- **Last Epoch model adopted — per-class movement abilities,** NOT D4 universal Evade. Mobility emerges from the generator pool, archetype-appropriate.
- **No guaranteed mobility per class.** Generator picks freely; some classes have mobility, some don't. Preserves emergence-driven design.
- **Two motion categories in the geometry palette:**
  - **Offensive motion** (B11): whirlwind, dash_attack, leap_strike — damage while moving
  - **Defensive mobility** (B13): roll, defensive_dash, strafe_mode, blink, dodge_stance — mobility without damage
- **Statistical evasion (`DODGE_CHANCE_CAP = 0.60`) preserved as-is.** Active evasion layers on top, not replaces.

### Engine sim metadata for active evasion (B13)
- Engine emits `cast_time` per skill (windup before damage applies)
- Engine emits `damage_resolution_time` per skill (when hitbox resolves)
- Engine emits `i_frame_window` per evasion skill (start_offset + duration)
- Demo respects these for telegraphs + i-frame resolution

### Archetype-emergence observability (B13)
- Engine surfaces per-class kit-mobility tag in output: `none` / `offensive_only` / `defensive_only` / `mixed`
- Cross-class clustering surfaced per season ("this season produced N dodge-tank-shaped classes")
- Spirit Guide includes archetype-cluster context in build coaching
- This is the Reincarnated-distinctive observability — no mainstream ARPG generates classes procedurally and reports emergent archetype clusters.

### Telegraphs (B13)
- Enemy AOE shows ground indicator during `cast_time` window
- Asymmetric indicator scaling: player AOE indicator = `0.92× hitbox` (generous edges); enemy AOE indicator = `1.08× hitbox` (narrow dodges feel earned)
- Indicator throttling may be needed at high mob density (B10 swarm tier 5-12 mobs/pack) — implementation question deferred to B13 ship

## Decided — meta-progression

### Body-swap spine (file 29)
Body-swap, gear smuggling, and accumulated knowledge are **one mechanism viewed from three angles**:

- **Body-swap:** the moment of transformation — defeat Trial boss → option to inhabit → retain world state, transform class identity.
- **Gear smuggling:** what items survive transformation (in-game) AND across games (cross-season).
- **Knowledge:** what the player learns about content shapes, build patterns, anchor archetypes, season conventions.

### Body-swap mid-act behavior
- World state: preserved ✓
- Quest progress: preserved ✓
- Inventory: preserved ✓ (gear may not fit new class)
- Player identity: transforms ✗

### Philosophy framing
- **"Death is progress"** (Hades influence per file 29) — body-swap softens death-state.
- Per-game arc has a defined end (final act boss).
- Seasons rotate; one-week seasons (per loot economy model).

---

## Decided — multi-band sim architecture (Section 8 RESOLVED 2026-05-11)

### Convergence model: Option β — 3-band act-aligned discrete convergence

- Engine converges classes at **3 band-end levels**: L17 / L33 / L50 (matches 3-act structure)
- Per-class convergence runs:
  - **L17** × {75th percentile gear} = 1 run
  - **L33** × {75th percentile gear} = 1 run
  - **L50** × {50th / 75th / 95th / 99th percentile gear} = 4 runs (B7 variance check at endgame)
  - **Total: 9 convergence runs per class** (was 1; 6 kit+variance + 3 doppelganger validation per Section 7 Q7.2)

### Per-band optimal distribution

- The engine's "meta build" output becomes **PER-BAND** — not just endgame
- Class export packet contains optimal_distribution at each band sample point
- Spirit Guide build coach recommends different distributions at different progression phases

### Failure handling: recompose-first

- If a class fails to converge at a given band, engine tries different per-band skill point distributions BEFORE falling back to damage_modifier
- If recomposition fails across all bands: regenerate class
- Aligns with "shaped balance over numeric scaling" philosophy

### Per-band gauntlet (per-band-generated, not same-gauntlet-scaled-stats)

- Engine generates a DIFFERENT gauntlet for each band
- A1 band gauntlet: pack size 2-4, 90/8/2 trash/magic/elite ratio, ~5% multi-pack overlap
- A2 band gauntlet: pack size 3-6, 80/15/5 ratio, ~15-25% multi-pack overlap
- A3 band gauntlet: pack size 5-12, 70/20/10 ratio, ~40-60% multi-pack overlap
- **Per-band monster pools** (LOCKED 2026-05-11): engine generates SEPARATE monster pool per band (A1/A2/A3 flavored). Matches genre's "5-15 new archetypes per act" pattern. ~3× monster LLM cost (~+$1-2/season).

### Cost impact

- Convergence: ~3-5 min/season → ~30-45 min/season (9× increase including doppelganger validation)
- **No LLM call increase from sim work** (convergence is mechanical-only)
- Per-band monster pool decision (pending) determines whether monster LLM cost grows ~3×

### Telemetry export packet additions

```
class.convergence_report = {
    'endgame_L50':     {winrate, iterations, dimensions_explored, optimal_distribution},
    'mid_band_L33':    {winrate, iterations, optimal_distribution},
    'early_band_L17':  {winrate, iterations, optimal_distribution},
    'variance_check_L50': {p50, p75, p95, p99}
}
```

## Decided — geometry/AOE that interacts with progression

Per B11 (2026-05-11 expansion; file 09 § "Revision 2026-05-11" + file 28 § B11):

- **25 active geometry types** post-B11.
- **Active-discrete-AOE: 16** (was 7).
- **Parameter expansions** on existing geometries (collision_mode, angle_distribution, sweep_shape, damage_falloff).

These shape the *content* the progression system delivers but are not progression mechanics themselves.

---

## Empty slots — to be filled from file 32 discussion

These are the structural placeholders. Each will fill in as file 32's open questions resolve.

```
PROGRESSION VECTOR @ character level N
═══════════════════════════════════════

[ ] Section 1 — Philosophy
    [ ] XP-driven / milestone-driven / hybrid?
    [ ] What grants XP if applicable?
    [ ] Death penalty model?

[ ] Section 2 — Character level curve
    [ ] XP curve shape (linear / quadratic / tier-based)?
    [ ] Per-act level bands?
    [ ] Body-swap level preservation rule?

[ ] Section 3 — Stat point progression
    [ ] Allocation model (auto / player-allocated / hybrid)?
    [ ] Stat points per level (if player-allocated)?
    [ ] Reset rules?
    [ ] Diminishing returns curves?

[ ] Section 4 — Ability acquisition UX
    [ ] Trait acquisition moment (auto-grant / pool-choice / quest-rewarded / random)?
    [ ] Skill availability over levels (all-from-start vs unlocked)?
    [ ] Quest skill-point distribution structure?

[ ] Section 5 — Gear progression curve
    [ ] Tier-availability per level (legendary level-gate)?
    [ ] Power-score growth curve?
    [ ] *_DROPS_PER_SLOT values per phase?
    [ ] Smart-loot weight at different phases?

[ ] Section 6 — Enemy/monster scaling
    [ ] Scaling philosophy (fixed-per-zone / scales-with-player / per-act / difficulty-tier)?
    [ ] Monster level vs character level mapping?
    [ ] Trial boss level binding?

[ ] Section 7 — Alignment validation
    [ ] What validation pass guarantees per-level alignment?
    [ ] Failure handling (reject for regen / accept with caveat / scale-back fallback)?

[ ] Section 8 — Sim architecture
    [ ] Option α (endgame-only + scale-back) / β (3-tier) / γ (continuous)?
    [ ] If β: which bands?
    [ ] Per-band gauntlet shape?
    [ ] Cost budget acceptance?

[ ] Section 9 — Death penalty
    [ ] Death model on regular-combat death?
    [ ] Trial-boss-death vs combat-death differentiation?
    [ ] Body-swap forced vs opt-in?

[ ] Section 10 — Per-act content
    [ ] Per-act level band?
    [ ] Per-act mechanical layering (new ailments / geometries / archetypes unlock)?
    [ ] Replayability per act?

[ ] Section 11 — Quest as progression source
    [ ] Quest count and reward structure?
    [ ] Quest types (main / side / hidden)?
    [ ] Repeatable quests?

THE UNIFIED VECTOR @ level N (filled when above sections complete):
═══════════════════════════════════════════════════════════════════
  - Stat points: ___ allocated per ___ rules
  - Skill points: ___ allocated (out of N×2 + quest contribution to date)
  - Traits: ___ unlocked at appropriate ranks
  - Gear: ___ drops per slot per smart-loot/RNG split
  - Faces: monsters at level-band ___ with composition ___
  - Convergence-validated: pass rate ___ at level N matches design target ___
  - Death-state: ___
```

---

## How to maintain this doc

- When file 32 resolves an open question → migrate the decision here as a filled section
- Strikethrough is fine; preserve history
- Keep the cross-references at the top current
- Don't add anything that hasn't been formally decided
