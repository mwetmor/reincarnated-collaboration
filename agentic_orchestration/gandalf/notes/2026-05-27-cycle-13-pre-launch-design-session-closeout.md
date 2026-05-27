# Cycle 13 Pre-Launch Design Session — Closeout (2026-05-27)

> **STATUS:** CURRENT — durable record of design decisions from the Matt + gandalf Pattern-B session 2026-05-27 covering T4 PM1 expanded scope (Q7 amendment) + Phase 3 gap-closure (GAPS 1-7). Authoritative for Cycle 13 scope-doc inputs.

**Author:** gandalf (story-and-design steward)
**Session participants:** Matt + gandalf (Pattern-B sustained design dialogue)
**Session pattern:** Pattern-B per `.claude/agents/gandalf.md`
**Authority basis:** Matt 2026-05-27 — full session greenlight; full-pass single-session; gandalf staff-bearer-mode leadership
**Companion docs:**
- `agentic_orchestration/gandalf/notes/2026-05-26-cycle-13-pre-launch-design-session-start.md` — session-start agenda
- `agentic_orchestration/gandalf/notes/2026-05-26-t4-post-mortem-session-1-prep.md` — pre-session T4 PM1 prep doc
- `agentic_orchestration/gandalf/notes/2026-05-26-cycle-13-framing-brief.md` — RATIFIED Cycle 13 framing brief (Q1-Q11)
- `agentic_orchestration/gandalf/notes/2026-05-27-block-c-calibration-scaffolding.md` — Block C math-before-code scaffolding for gamora handoff
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` — Cycle 13 architectural foundation (D1-D86); doc 40 amendments queued Wave 0
- `canonical/41-progression-framework-2026-05-27.md` — NEW canonical doc (queued Wave 0 authoring) capturing L50 hybrid + ~30-day seasonal duration framework

---

## 0. TL;DR

Single-pass ~4-hour Pattern-B design session covering Blocks A / A.5 / B / C / D / E. Every Cycle 13 step now has design inputs needed to fire. ~90 architectural decisions locked or refined; 7 engineering-discipline candidates flagged to jack-ryan; substantial latent canon (L50 hybrid progression framework) made explicit; T4 algorithm taxonomy materially refined; content-compositional attunement supersedes binary/graduated framing; Block C calibration scaffolding produced for gamora handoff per Discipline #18.

Session output → KR consumes for Cycle 13 scope-doc authoring → Cycle 13 launches via Wave 0 (scope-doc + canonical authoring) → Wave 1+ executes.

---

## 1. Block A — T4 + skill tree architecture lock

### 1.1 Skill tree architecture (Q7 item 1 → D69)

**LOCKED**: Chain-based investment + LINEAR default within chain + SHARED skill point pool across chains + T4 unlocked by chain-investment threshold.

- Closest genre analog: Grim Dawn mastery trees with PoE-2-tight node count + algorithmic mechanic-alteration as per-node payload
- 9-16 total nodes per kit matches `skill-system-2026-05-24.md` 10-15 budget
- Per-skill mini-trees (LE-style) rejected; PoE mega-tree rejected

### 1.2 Branching refinement (Matt 2026-05-27)

**LOCKED**: Branching gated by **chain depth ≥4 nodes**, not class chain count.

- Chains ≥4 nodes eligible for 1 branch point: 1 → 2 → {3a OR 3b} → 4 → T4-capstone
- Chains ≤3 nodes linear only
- Substrate-led: chain depth votes on branching eligibility
- Supporting chains stay linear (shallow by construction)

### 1.3 One-T4-unlocked-at-a-time (Matt 2026-05-27)

**LOCKED**: Only ONE T4 capstone unlocked at a given time. Sharpens doc 40 D66 from passive description to active identity discipline. Composes with D65 respec-with-legendary-trigger as swap mechanism + D76 dual-effect architecture (concentrated identity, not diluted).

### 1.4 Class chain architecture (Q7 items 2 + 6 → D70/D83)

**LOCKED**:
- A2a: **Variable 3-or-4 chains per class** (depth-vs-breadth lever)
  - 3-chain class: 2 T4 chains × ~5 nodes (branching-eligible) + 1 supporting chain × ~3 nodes
  - 4-chain class: 3 T4 chains × ~3-4 nodes (linear) + 1 supporting chain × ~3 nodes
- A2b: First-pass class roster **DEFERRED** — substrate-evidence follow-on (Wave 1 BC-target review surfaces substrate vote)

### 1.5 Skill point economy (Q7 item 3 → D71)

**LOCKED (with Matt 2026-05-27 graduated-investment refinement)**:

| Sub-item | Lock |
|---|---|
| Per-node max — Passive | **5 points** |
| Per-node max — Active (T1-T3) | **15 points** |
| Per-node max — T4 capstone | **1/1 binary** (0/1 if another T4 selected) |
| Endgame total budget | **~70 points** (anchor; tunable) |
| T4-unlock threshold | **70% of chain max** (per-chain calc; chain max varies by composition) |
| Earn rate | **Per-level (L1→L50 = 50 points) + per-content-completion bonuses (~20)** |
| Branched-chain T4-unlock | All UNIQUE prerequisites along one path; other branch optional pay-extra |

Insight A from T4 PM1 prep (active/passive mix per kit) **OPERATIONALLY RESOLVED** within this lock — chain composition (active/passive ratio per chain) is generated per kit identity at Phase 2a kit composition; cohesion-judge validates ratio at Phase 5; active-heavy vs passive-heavy emerges naturally from kit identity.

### 1.6 Respec rules (Q7 item 4 → D73)

**LOCKED (with Matt 2026-05-27 spirit-guide-mediated refinements)**:

| Sub-item | Lock |
|---|---|
| Reset scope | **Two-option presentation**: (1) T4-respec IF player has multiple chains above T4-unlock-threshold (swap which T4 is active); (2) Full respec always available. Spirit Guide offers to auto-allocate points during full respec if desired |
| Full respec cost | **DEFERRED** — substrate (gear/currency infrastructure) needed before lock; Cycle 14+ acquisition curve calibration |
| Player-facing trigger | **Spirit Guide initiated OR player asks Spirit Guide.** D75 T4-swap UX resolves to Spirit-Guide-as-surface |

### 1.7 NEW T4-failure-handling decision (Matt 2026-05-26)

**LOCKED**: **Option F (Hybrid)**:
1. Algorithm regenerates failing T4 with alternate strategies from registry (3 attempts; configurable per D62 compute budget)
2. If all regeneration attempts fail, ship character with partial T4 (in-band subset; chain keeps T1-T3 nodes but no functional capstone)
3. Minimum threshold = ≥1 T4 in-band for character to ship at all
4. Track regeneration rate as quality metric

Composes with D1 (balance-as-property — failures are honest), D67 (independent gauntlet sim validation), D65 (respec mechanism), D62 (compute budget).

---

## 2. Block A.5 — Trait architecture absorption + resource model

### 2.1 Trait architecture absorption (GAP 5 reframed)

**LOCKED**: May 12 trait architecture (per `project_trait_architecture.md` memory) is **SUPERSEDED** by current chain + stat-sheet + legendary-passives architecture. ~90% absorbed automatically; the remaining "per-class intrinsic baseline passive" surface lands in:

**Option C — Supporting chain absorbs class identity.** The T3-only supporting chain (every class has one per D83) serves as the "class-intrinsic passives" location. Supporting chain represents class identity; T4 chains represent build specialization.

- No separate "trait modifier" axis on character sheet
- Player chooses investment level in class-identity vs build-specialization (real opportunity cost)
- Composes with depth-vs-breadth lever
- Substrate-led: uses existing architectural surface rather than adding new layer

### 2.2 Resource model per cell type (GAP 6)

**LOCKED**: 8-model resource catalog + hybrid-permitted-per-kit rule.

| # | Resource model | Likely cell types |
|---|---|---|
| 1 | **Mana** | High-burst caster cells; ranged elemental |
| 2 | **Cooldown** | Tactical-pattern cells; rotation-driven |
| 3 | **Stamina** | Melee martial cells; sustained-attack |
| 4 | **Rage / Fury** | Berserker/melee burst cells; tank-DPS hybrids |
| 5 | **Energy** | High-tempo physical cells; combo executor |
| 6 | **Channeled** | Sustained-beam cells; channeled-AoE |
| 7 | **Combo / Charges** | Combo-builder cells; finisher-driven |
| 8 | **Health-as-resource** | Sacrifice-archetype cells; blood-themed kits |

Hybrid models permitted per kit identity. Specific bin-to-model mapping is rocket Phase 2a kit composition work.

### 2.3 v1.1+ resource model extension candidates

Flagged for future substrate-vote-on-promotion:
- **Faith / Souls / Karma** (Soulslike spell-casting; finite-per-encounter)
- **Crafted-resource** (player crafts pre-encounter; consumes in-encounter)
- **Position-as-resource** (some skills cost movement / require positioning state) — **HIGH PRIORITY v1.1+ candidate per Matt 2026-05-27**. Empirical trigger: P2/P3 substrate clustering surfaces artillery/cannoneer/siege-emplacement cluster (~50+ rows) whose mechanical natural fit is none-of-the-above. Opens additional martial archetypes.

### 2.4 T4 node algorithm revisit (Matt 2026-05-27)

**LOCKED — supersedes doc 40 § 3.2 + § 8.4 6-strategy registry as player-facing taxonomy + design-spec.**

**3-category T4 taxonomy** (composes with D76 dual-effect):

| Category | Role | D76 dual-effect part | Algorithm strategies mapping |
|---|---|---|---|
| **A — Class mechanical/energy alteration** | Character-wide effect (always present) | Character-wide effect | RESOURCE_CONVERSION, DEFENSIVE_CONVERSION, DEFENSIVE_TRADEOFF, class-wide TRADE_OFF |
| **B — Chain multiplicative event** | Chain-specific (exactly one of B or C per T4) | Chain-specific effect | Skill-specific TRADE_OFF, GEOMETRY_COLLAPSE, multiplier strategies |
| **C — Chain element conversion / addition** | Chain-specific (exactly one of B or C per T4) | Chain-specific effect | ELEMENT_CONVERSION, **NEW: DUAL_ELEMENT_ADDITION** |

**NEW algorithm strategy: DUAL_ELEMENT_ADDITION** — chain skills retain primary element AND add a secondary element. Genre precedent: PoE's "X% physical as fire"; D4's "all skills deal X% as cold." Substantively expands T4 design space.

**Parallel-chain reach**: chain-specific effect can target the T4's OWN chain OR a PARALLEL chain. Algorithm-fixed at generation time (not player-chosen). Composes with depth-vs-breadth.

**Existing 6-strategy registry retained** as algorithm implementation detail under 3-category umbrella.

### 2.5 Compositional synergy scan (Matt 2026-05-27 theorycraft → algorithm)

**LOCKED as Cycle 13 algorithm extension (NOT v1.1+; required for parallel-chain reach to function as design).**

**Two-pass synergy scan** (Matt 2026-05-27 button-up):

| Pass | Description |
|---|---|
| **Pass 1 (resolve)** | Does candidate resolve existing kit tensions? (e.g., HP-cost-without-regen → life-steal-from-bleed) |
| **Pass 2 (preserve)** | Does candidate CREATE new tensions not resolved elsewhere? (e.g., life-steal-from-bleed against bleed-immune bosses → mechanism has no fuel) |

**Net synergy score = resolve-score − create-score.** Candidates that resolve more than they create get the boost. Cohesion-judge validates BOTH directions.

**Synergy opportunity patterns (v1 catalog):**

| Pattern | Description |
|---|---|
| **Tension-resolution** | Kit has a mechanic creating a problem the T4 could solve |
| **Theme-compound** | Kit has a passive theme the T4 could amplify |
| **Cross-chain composition** | Parallel chains have elements/mechanics that could combine |
| **Element-gap fill** | Kit has element coverage gap a T4 could fill |

**Honor AI-tell line (D7)**: pattern library (gandalf-curated) + statistical co-occurrence priors (elrond) + algorithmic composition. **NOT LLM raw-reasoning** for core synergy detection.

**Engineering-discipline candidate #7 (this session): First-do-no-harm discipline** — T4 synergy detection must include downstream-tension-creation check, not just upstream-tension-resolution.

**Compositional synergy scan serves BOTH** T4 generation AND legendary added-skill generation at consumption time. Same engine; two consumers.

---

## 3. Block B — Gear architecture lock

### 3.1 Character sheet stats — 9-category surface (Q7 item 8)

**LOCKED** (per ultra-think pass against Diablo 1-4 + Immortal + PoE 1-2 + LE + Grim Dawn + Lost Ark; revised from 8 to 9 categories):

| # | Category | Sub-divisions |
|---|---|---|
| 1 | **Damage** | base / by-element / by-mechanic / by-condition / weapon-scaling |
| 2 | **Defense** | armor / DR% / dodge / block / +HP / +HP-regen / element-resists / status-resists |
| 3 | **Resource** (8-model-dependent) | per-model specific stats (mana max/regen/cost-reduction; cooldown reduction; stamina max/regen; rage gen/decay/cap; energy gen/max; channel efficiency/duration; combo retention/cap; HP-cost efficiency) |
| 4 | **Crit** | crit chance / crit multiplier / crit-on-condition / crit-on-element |
| 5 | **Speed** | attack-speed / cast-speed / cooldown-reduction / movement-speed |
| 6 | **Resistance / Penetration** | element penetration / armor penetration / status duration / status resistance |
| 7 | **On-trigger** | on-hit / on-crit / on-kill / on-block / on-dodge / on-element-cast (toolkit-only at legendary tier per D54) |
| 8 | **Build-identity** | T4-attunement annotation / set-bonus rank / class-intrinsic supporting-chain investment |
| 9 | **Utility / Meta-progression** (NEW) | magic find / currency drop rate / experience boost / rare-find chance |

**Specific modifier lists within each category DEFERRED to Wave 1 partition cycle.**

**Discipline lock — gear modifier rule (Matt 2026-05-27 pushback refinement):**
- Gear ADDS skills via capability toolkit (D54-D55) — triggered-passive (high prob on weapons; armor on-being-hit; other slots general passive) + true-active (extremely rare, weapons only)
- Gear does NOT modify existing chain-node skills (no +levels-to-Fireball)
- Upper-tier (1+2) added-skill content is chain-aligned AND T4-attuned (triple cohesion)

### 3.2 Full gear details — 11-slot taxonomy + per-rarity × per-slot grid (Q7 item 7)

**LOCKED — 11 slot taxonomy:**

| Slot family | Slots | T4-attunement eligible (Tier 1+2) |
|---|---|---|
| Weapon | Main-hand (main_weapon) | Yes |
| Off-hand | Secondary-item (shield / tome / banner / focus / horn / talisman / dual-wield-secondary per `off-hand-items-2026-05-24.md`) | Yes |
| Armor | Head / chest / hands / feet / legs (5 slots) | Yes |
| Accessory | Amulet / ring × 2 / belt (4 slots) | Yes |
| **Total** | **11 slots** | All eligible at upper tiers |

**LOCKED — per-rarity × per-slot specification grid** (architectural; specific modifier counts/magnitudes/tier-restriction lists DEFERRED to Wave 1 partition cycle):

| Rarity | Modifier count | Categories rollable | Added-skill content |
|---|---|---|---|
| Common | 1-2 | 1-3 (Damage/Defense/Resource) | No |
| Uncommon | 2-3 | 1-6 | No |
| Rare | 3-4 | 1-6 + 9 | No |
| Epic | 4-5 | 1-9 (full) | No |
| Legendary T0 | 4-5 + Epic-exclusion modifiers (D56) | 1-9 + legendary-exclusive | Yes — chain-aligned |
| Legendary T0.5 | Higher density | Same | Yes — chain-aligned |
| Legendary T1 | Higher density + T4-attunement annotation | Same + T4-attunement | Yes — **chain + T4-attuned** |
| Legendary T2 | Highest density + T4-attunement | Same | Yes — chain + T4-attuned |
| Unique T0-T2 | Per tier (parallels legendary); signature-mod patterns | Same as legendary at tier | Per tier (same as legendary) |
| Set T1-T2 (endgame-only) | Per tier + set bonus rank | Same as legendary at tier | Yes — chain + T4-attuned + set-cohesive |

**Tier-restricted modifier surface: YES** (architectural; ~10-20% of modifier types tier-restricted to Epic+/Legendary+/Tier-1+2; specifics partition-cycle).

### 3.3 Per-gear-slot fill rules (Q7 item 9)

**LOCKED — per-slot affinity matrix architectural framework + 6 principles:**

Affinity matrix: 9 categories × 11 slots, with **primary (~50%) / secondary (~30%) / tertiary (~15%) / off-affinity (~5%)** weighted probability per slot per category (specific weights tune in Wave 1).

Sample affinity:
- Main-hand weapon: Damage primary / On-trigger primary / Crit secondary / Speed secondary / Resource tertiary
- Chest: Defense primary / Resource primary / On-trigger (on-being-hit per D55) secondary / Build-identity secondary
- Feet: Speed (movement) primary / Defense (dodge) primary / Resource (stamina/energy regen) secondary
- (Full matrix in Block B execution; specifics partition-cycle)

**6 locked principles:**

1. **Graduated affinity, not binary** — every slot CAN roll any category but with weighted probability per affinity tier
2. **Tier-restricted modifiers** — locked to qualifying rarity tiers regardless of slot affinity
3. **Resource-model-gated** — resource modifiers map by class resource model; cross-resource rolls DO NOT APPEAR
4. **Gap-filling discipline (D80)** — spirit guide surfaces gap-fill opportunities
5. **No-skill-modifier rule** — gear NEVER modifies existing chain-node skills; capability toolkit ADDS new triggered-passives + rare true-actives only
6. **Cross-cohesion validation** — Wave 1 partition cycle must validate affinity matrix supports build-diversity via spot-check simulation across cohort archetypes (per D61 + D84)

### 3.4 T4-attuned gear specifics (Q7 item 5 → D38)

**LOCKED — content-compositional attunement (Matt 2026-05-27 original-intent surface)** — supersedes binary/graduated framing.

| Sub-item | Lock |
|---|---|
| Attunement model | **Content-compositional with metadata annotation**. Gear's content (passives, weapon specs) IS the attunement. Annotation field exists as metadata recording generation-time alignment intent; drives drop pool restriction (D50), spirit-guide projection (D34), algorithm-side optimization. Annotation does NOT toggle anything ON/OFF at consumption time — gear passives always fire; synergy value varies by build. |
| Magnitude | **No separate multiplier**. Gear content design is sim-calibrated to produce playability-AND-in-band synergy with target chain+T4. Magnitude IS the content quality. |
| Cross-rarity distribution | Per D33 + D51: Tier 1+2 legendary/unique have chain+T4 annotation; all sets have chain+T4 annotation (endgame-only); Tier 0+0.5 have chain-alignment annotation only |
| Set bonus structure | **4-piece sets standard; 2pc minor bonus (always-active) + 4pc full bonus (content composed with chain + T4)** |

**Doc 40 D33+D38+D51 amendment queued Wave 0** — content-compositional attunement reframe.

**Spirit-guide implementation requirement**: synergy-score projection ("playing T4-A: projected KPM 75. Switching to T4-B: projected KPM 62. Net synergy score: T4-A composes 23% better with this gear") — composes with D28 data-oracle voice naturally.

---

## 4. Block C — Calibration scaffolding for gamora handoff

**LOCKED — see companion doc `agentic_orchestration/gandalf/notes/2026-05-27-block-c-calibration-scaffolding.md` for full scaffolding artifact.**

Summary:

- **Scaffold 1 (P_node)** — 5-dimensional power vector (KPM / HP / defensive uptime / resource flow / rotation coherence); architectural definition of "power as vector, not scalar"; per-node numerical calibration deferred to gamora (gates on per-level scaling formulas)
- **Scaffold 2 (C_archetype)** — FULL LOCK; 5-dimensional play-strategy vector + 4 cohort identities (DPS-min-maxer / Balanced / Defensive / Hybrid-as-substrate-led); scaling-independent
- **Scaffold 3 (W function)** — W(cell, node, cohort) → (WR_lower, WR_upper); function signature locked; cell-difficulty-adjustment as gandalf+gamora+legolas+elrond math hotspot; per-node bracket numerical calibration deferred
- **Compose-rules Steps 1-8** — full lock; calibration loop operates against L50 hybrid framework once scaling formulas land

**Cycle 13 v1 mechanical season gen scope:** calibrate against **endgame-reference-encounter** (L45-50+ progression node only); multi-node calibration is post-scaling-formulas work (Cycle 14+).

---

## 5. Block D — Test encounter content + degenerate-state detection

### 5.1 GAP 2 — Test encounter content

**LOCKED architectural intent**:

- Endgame-reference-encounter catalog covering ~22 BC-target cells (per `v1-bc-target-intent-2026-05-24.md`)
- Minimum 8-12 / optimal 15-22 / maximum ~30 reference encounters
- Each encounter exercises full playability criterion (D61)
- **Wave 0 audit dispatch fires** — gamora (sim-side audit) + rocket (encounter content audit) + jack-ryan (Gate-1 critique); enumerate existing + identify gaps + recommend additions

### 5.2 GAP 3 — Degenerate-state detection

**LOCKED — Hybrid approach (Approach C)**:

- Explicit checks for known patterns FIRST + KPM-out-of-band as second-pass proxy
- **8-pattern v1 catalog**:
  1. Infinite stunlock (time-in-CC > 60% encounter duration)
  2. Zero-damage void (player damage dealt < 1% expected OR taken < 1% expected)
  3. Mandatory-skill-lock (only 1 viable rotation)
  4. Permanent-CC (movement-blocked > 70% encounter)
  5. Resource-starvation (resource < skill cost > 50% encounter)
  6. Degenerate-tank (defensive_uptime > 99%; pure DPS check)
  7. Bounce-CC (skill-cancellation rate > 50% attempted casts)
  8. Resource-overflow (resource at max > 80% encounter; paradoxical)
- Substrate-led extension via Cycle 13 telemetry
- **Methodology consultation per Discipline #18** fires: gamora + legolas Mode A + star-lord
- **Doc 40 D61 amendment queued Wave 0** — explicit degenerate-state detection compositional with KPM-band gate

---

## 6. Cross-cutting locks (foundational; cross-block)

### 6.1 L50 hybrid progression framework + ~30-day seasonal duration (Matt 2026-05-27)

**LOCKED — substantial latent canon made explicit:**

- **Hybrid progression** = light leveling + content-tier dominance at endgame
- **Level 50 cap**
- **~30-day seasonal duration** (NOT cadence-term "monthly" — D3 language discipline preserved; we say "seasonal")
- **Each season**: player levels L1→L50 over ~3-4 weeks engagement + endgame phase (L50 cap; power growth via gear acquisition + chain investment + T4 unlock + set completion)
- **Cross-season** (D25): season N telemetry → season N+1 generation inputs
- **NO PARAGON-style infinite leveling** — endgame post-cap growth purely via gear + build

**Composes with everything**: skill point math (A3 50+20=70), seasonal cycling (D2), 85th-percentile cumulative engagement (D18), 4 progression nodes (D27 mapped to level bands L1-15 / L15-30 / L30-45 / L45-50+), gear tier progression (D50 mapped to player level bands), T4-unlock economics, spirit-guide projection bounds.

**Canonical doc 41 queued Wave 0**: `canonical/41-progression-framework-2026-05-27.md`.

### 6.2 Methodological pattern observation — substrate-led-variance at design-architecture layer

Recurring pattern through Block A → Block A.5 → Block B: **the structural substrate votes for variance; don't pre-impose uniformity where the structure itself differentiates.**

Instances:
1. Chain branching gated by chain depth (not class chain count)
2. Variable 3-or-4 class chain count (not uniform)
3. Per-node max 5/15/1 by category (not uniform 10)
4. Trait absorption into supporting chain (not separate trait layer)
5. Content-compositional attunement (not binary/graduated flag)

This is the operational signature of substrate-led discipline at the design-architecture layer. Worth recognizing as a methodology theme; potential Discipline #18 amendment candidate.

---

## 7. Engineering-discipline candidates flagged to jack-ryan (7 total from this session)

The 5 candidates from doc 40 § 12.1 (already flagged):
1. Playability discipline (D61) — playable-AND-in-band as sim validation criterion
2. Dual-effect capstone discipline (D76) — multi-capstone systems should architect capstones to have dual-effect structure
3. Spirit-guide-pacing discipline (D78) — offer-triggering mechanisms must avoid training players to defer commitment indefinitely
4. Commitment-to-consequence discipline (D79) — decision-mechanisms requiring commitment produce more meaningful engagement
5. Sim methodology naming discipline (D84) — combat sim methodology must explicitly name node-population sampling + cohort coverage + edge-case handling

NEW from this session:

6. **Dual-effect separability discipline (D76 amendment)** — Category A (character-wide) and Category B/C (chain-specific) effects must be INDEPENDENTLY COHERENT; removing one should leave the other as a genuine standalone mechanic. Failure mode: T4s where chain effect is just "consequences of character-wide effect spelled out in chain terms." [Founding instance: corrected Blood Magic example 2026-05-27]

7. **First-do-no-harm discipline for algorithmically-generated T4 keystones** — Synergy detection must include downstream-tension-creation check (Pass 2 preserve), not just upstream-tension-resolution (Pass 1 resolve). Net synergy score balances both passes. Failure mode: T4s that solve a stated problem by introducing an equally-bad new problem.

---

## 8. Deferred commitments (with empirical-evidence triggers)

| # | Commitment | Empirical-evidence trigger for re-engagement |
|---|---|---|
| 1 | First-pass class roster (specific class lineup) | Wave 1 BC-target review + substrate evidence on chain composition viability |
| 2 | Full respec cost calibration | Gear/currency infrastructure landed (Cycle 14+) |
| 3 | Per-level scaling formulas (stat scaling / monster scaling / XP curve) | Cycle 13 mechanical season gen telemetry OR scaling-implementation cycle scheduled |
| 4 | Multi-node calibration WORK across all 4 progression nodes | Per-level scaling formulas land (post #3) |
| 5 | Acquisition curve calibration sharpening (D21 Option A specifics) | Post-scaling-formulas + per-cohort empirical engagement data |
| 6 | Position-as-resource (9th resource model) | P2/P3 substrate clustering surfaces artillery/cannoneer/siege cluster (~50+ rows) |
| 7 | Faith/Souls/Karma + Crafted-resource (10th+ resource models) | Substrate vote OR design call for specific archetypal kits requiring them |
| 8 | Per-node bracket numerical calibration | Per-level scaling formulas (#3) |
| 9 | Chain-level respec (between T4-only and full respec) | Substrate-evidence shows binary T4-only / full respec is too rigid |
| 10 | Graduated attunement (alternative to content-compositional) | Substrate-evidence shows content-compositional too rigid |

---

## 9. Wave 0 follow-on items (gandalf authors when Cycle 13 launches)

| # | Item | Owner |
|---|---|---|
| 1 | **New canonical doc 41** — `canonical/41-progression-framework-2026-05-27.md` (L50 hybrid + ~30-day seasonal duration + node-to-level-band mapping + endgame-post-cap-via-gear) | gandalf |
| 2 | **Doc 40 amendments** — T4 algorithm 3-category taxonomy (D81 amendment); DUAL_ELEMENT_ADDITION strategy (§ 3.2 + § 8.4 amendment); parallel-chain reach (§ 6 + § 8); compositional synergy scan (§ 8 + new § for algorithm extension); content-compositional attunement (D33+D38+D51 amendment); 9-category char sheet surface (§ 3.6 amendment); class-intrinsic supporting chain (§ 6 amendment); dual-effect separability + first-do-no-harm (§ 12.1 candidates #6 and #7) | gandalf |
| 3 | **Ground-state 00 § 1 update** — register doc 41 as new CURRENT entry; foundational architecture | gandalf |
| 4 | **Roadmap 02 § 3 visual flow update** — status icon transitions for landed decisions | gandalf (knight-rider may update as cycle advances) |
| 5 | **Block C scaffolding doc** — `2026-05-27-block-c-calibration-scaffolding.md` (companion doc; LANDED in this session) | gandalf (done) |
| 6 | **Cycle 13 scope-doc** — `agentic_orchestration/cycles/cycle-13-mechanical-engine-build-scope.md` consuming this closeout + framing brief + canonical foundation | gandalf OR knight-rider per Q7 ratification |

---

## 10. Sidecar dispatches queued (Cycle 13)

| Sidecar | Owner | Description |
|---|---|---|
| **SC-1: Main_weapon routing cleanup** | elrond + rocket | Substrate curation pollution fix; embedded in Wave 1 |
| **SC-2: Engineering-discipline ratification** | jack-ryan | Ratify 7 candidate disciplines from this session + doc 40 § 12.1 |
| **SC-3: Discipline #23 amendment** | jack-ryan | Discipline #23 amendment write-up |
| **SC-4 (EXPANDED): legolas Mode A research** | legolas | Partition methodology + 9-category surface verification + synergy taxonomy + degenerate-pattern catalog research (post-training-data ARPG state) |
| **SC-5: Pi infrastructure execution** | star-lord (Matt scheduling) | Out-of-cycle |
| **SC-6 (NEW): GAP 2 reference encounter audit** | gamora + rocket + jack-ryan | Enumerate existing + identify gaps + recommend additions |
| **SC-7 (NEW): Gamora methodology consultation** | gamora (Discipline #18 + amendment 18.2) | Per D60 + D84; consumes Block C scaffolding; fires post-Wave-1 |

---

## 11. Sign-off

**Author:** gandalf (story-and-design steward)
**Status:** RATIFIED 2026-05-27 — closeout doc captures Matt + gandalf design call outputs in full; KR + specialists consume this as primary handoff
**Composition:** with `2026-05-27-block-c-calibration-scaffolding.md` (Block C math handoff) + `2026-05-26-cycle-13-framing-brief.md` (Cycle 13 framing — to be updated with concrete-outputs-landed reference) + `2026-05-26-t4-post-mortem-session-1-prep.md` (T4 PM1 prep — to be updated with Pass-1-complete reference) + Wave 0 canonical artifacts (doc 41 + doc 40 amendments)

**For:** the Matt + gandalf Pattern-B sustained design session 2026-05-27 covering T4 PM1 expanded scope (Q7 amendment 9 outputs) + Phase 3 gap-closure (GAPS 1-7) + L50 hybrid progression framework lock + T4 algorithm taxonomy refinement + content-compositional attunement + compositional synergy scan + 7 engineering-discipline candidates. By end of session, every Cycle 13 step has design inputs needed to fire; KR + specialists have substantive handoff for Wave 0 scope-doc authoring → Cycle 13 launches.

**Signed:** gandalf
