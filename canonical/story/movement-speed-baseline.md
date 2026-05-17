# Movement-Speed Baseline — Tier-1 ARPG Anchor for VS2a

**Status:** **Canonical — Matt-approved 2026-05-16; revised 2026-05-16 (Day 4 close).** Authored 2026-05-16 by gandalf on Matt's direct directive: *"I don't want to ship demo VS2a without this. The actual per-tile movement speed for the player should be exactly set on the Tier 1 ARPG AVG dimension. We may use different tile sizes, or not use tiles at all."* **Revised same day** per Matt verdict reversal: VS2a default rebased from mid-game (7.5 m/s) to end-game (8.0 m/s); sim consumption moved from "post-VS2a tight follow" to "VS2a-gating." See § "Verdict reversal 2026-05-16 (Day 4 close)" below — that section's operational values supersede the locked-values table for VS2a.

---

## 🔴 VERDICT REVERSAL 2026-05-16 (Day 4 close) — Option A superseded by Option B (end-game-anchored)

**Authority:** Matt directly, 2026-05-16 Day 4 evening session. Direct quote:
> *"We need to wire the actual end game player value, end game monster value and end game player:monster movement speed ratio all into the sim and the final JSON packet. No point playing a game which is not ran through the sim."*

**What changed.** Earlier this same day, Matt locked **Option A**: VS2a player at 7.5 m/s (mid-game Tier-1 average; pre-implementation of eventual mid-game feel). Later same day, Matt reversed: lock VS2a player at **8.0 m/s** (end-game value; locked late-game per row 4 of the original locked-values table; gear-only since palette has no MS-skill-buffs). Sim consumption (gamora Gate 3b) moves from "post-VS2a tight follow" to **VS2a-gating**.

**Why.** Option A papered over the schema-emit-without-consumer drift (sim doesn't model MS; demo plays hardcoded MS the sim never saw). Option B closes the drift by forcing sim consumption and using actual end-game values. Playtest signal from VS2a now reflects sim-validated end-game balance, not unmodeled mid-game approximation.

### Rationale — why 8.0 (not 9.5), why 7.5 fast-monster, why 0.719

**9.5 m/s as the "true end-game" value was correctly rejected.** The original AI_SPEED_MULTIPLIER 0.605 anchor (5.75 trash ÷ 9.5 player) assumed D2-style **active MS skill buffs** stacking on top of gear — Vigor aura, Burst of Speed, Frenzy. Phase 0 ships **no MS-affecting geometries** in the palette (B11 16→25 expansion does not include MS-buff actives; B13 active mobility is post-VS2a). Anchoring VS2a to a 9.5 m/s value the engine has no mechanism to produce would replay the exact mid-game-target dishonesty Option B was meant to close — just at a different magnitude. **End-game-gear-only is 8.0 m/s** (locked late-game value per the original Tier-1 table, PoE-1-excluded, +39% over trash). That's the value the engine actually produces at end-of-progression once B12 gear slots ship. VS2a pre-implements the eventual gear-only end-game; nothing further.

**Operational AI_SPEED_MULTIPLIER = 0.719** (5.75 trash ÷ 8.0 player end-game). Replaces the 0.767 mid-game derivation and the 0.605 fictional-buffed derivation. One number, derived from the values the engine can actually produce, consumed by both sim (gamora Gate 3b kiting math) and demo (drax AI-tick code).

**Fast-archetype 7.5 m/s — chase margin 0.5 m/s = 24 px/s — is the genre-correct end-game kiting feel.** D2 Fetishes, D3 Vortex elites, D4 Corrupted Rogues, PoE Fast-affixed rares all sit at ~115–130% of monster baseline, producing a small-but-real chase margin against the player at end-game gear-only. The 24 px/s chase margin at 48 px/m means a fast monster closes 1 tile (~48 px) per ~2 seconds of player straight-line flight — enough to make positional play matter, not enough to make kiting impossible. At the prior 6.6 mid-game-range value, the chase margin was effectively negative against an 8.0 m/s end-game player (player outran fast-monsters trivially), inverting the genre signal. 7.5 m/s preserves "fast monsters are practically threatening" as end-game feel; pack-positional-spread + skill geometry still drive the actual kiting math, but the speed differential is no longer absurd.

### Sim-consumption gating clause — "no point playing a game which is not ran through the sim"

Matt's framing (Day 4 evening): *"We need to wire the actual end game player value, end game monster value and end game player:monster movement speed ratio all into the sim and the final JSON packet. No point playing a game which is not ran through the sim."*

This is operationalized as a hard gating clause on VS2a: **sim and demo MUST consume the same MS values via the same engine-emitted JSON packet.** No demo-side hardcoding that the sim never saw; no sim-side modeling against a baseline the demo doesn't ship. Three concrete consequences:

1. **Balance-loop kiting math depends on it.** Gamora Gate 3b extends `fight_engine.py` with per-tick movement-speed-driven distance updates (3-band distance state: melee / near / mid). The win-rate convergence numbers the engine targets (file 28 § B14.5 V1 primary loop) need the MS the demo will actually ship; otherwise the convergence is balancing the wrong fight. Per gandalf review 2026-05-12 (project_b14_5_sidecar_analyses): convergence iterations are highest for controllers/mages — exactly the archetypes most sensitive to kiting math. A sim that doesn't model kiting under-models the very archetypes that depend on it most.

2. **Pack-encounter convergence depends on it.** Genre-anchored gauntlet target (~80–100 mobs/min per file 29) was authored against a sim that doesn't model movement-speed-aware kiting; single-target archetypes are under-modeled vs packs per `engine-balance-stewardship.md` Gate 1 reading. Sim consumption of end-game-anchored MS values (player 8.0; fast 7.5; trash 5.75; multiplier 0.719) corrects that under-modeling. KPM target may shift once 3b lands; that shift is the *signal* the convergence framework needed.

3. **Boss-arena traversal depends on it.** B10 V2 sequential-room semantics with HP carryover (arena room/hallway 15-45m + 6-10m hallways per `canonical/story/arena-room-hallway-system.md`) assumes specific traversal times derived from player MS. End-game-anchored 8.0 m/s makes a 30m default room cross in 3.75s; a 45m large set-piece room cross in 5.6s. These traversal times feed boss-fight pacing (telegraph windows, mechanic cycles). If demo ships 8.0 m/s but sim assumes 5.75 m/s, every boss telegraph window the sim derived will land at the wrong moment in the demo.

The Option-B commitment is: **rocket schema defaults emit the values → star-lord export DTO consolidates them through `ExportClass` + `ExportMonster` (precondition fix per `2026-05-16-export-dto-stage-b-silent-drop.md`) → gamora sim consumes them via Gate 3b → drax demo consumes them via the same JSON, removing hardcoded values from `world/movement.ts`.** All four seams read from one source. Single source of truth in the JSON packet; no parallel realities.

**New locked values (operational; supersede the corresponding rows in the original locked-values table below):**

| Parameter | Old (Option A — superseded) | **New (Option B — operational)** |
|---|---|---|
| Player VS2a default | 7.5 m/s | **8.0 m/s** (end-game gear-only; matches original late-game lock) |
| Monster trash MS | 5.75 m/s | **5.75 m/s** (unchanged — monsters don't get gear MS scaling) |
| Monster fast-archetype VS2a default | 6.6 m/s (used in current rocket smoke) | **7.5 m/s** (top of locked range; end-game fast monsters at parity with old mid-game player; closes-the-gap kiting threat) |
| AI_SPEED_MULTIPLIER (trash:player) | 0.767 (5.75/7.5) | **0.719** (5.75/8.0) |
| Fast-archetype:player ratio | 0.880 (6.6/7.5) | **0.938** (7.5/8.0; chase margin 0.5 m/s = 24 px/s) |
| Sim consumption (gamora Gate 3b) | "post-VS2a tight follow; not gating" | **VS2a-gating** |
| Demo MS source-of-truth | Hardcoded values in `world/movement.ts` matching spec | **Engine-emitted via JSON; demo reads, doesn't hardcode** |

**Implied demo px/s at PIXELS_PER_METER=48 (Option B):**

| Stage | m/s | px/s |
|---|---|---|
| Base (L1 unbuffed) | 5.75 | 276 |
| Player VS2a default | **8.0** | **384** |
| Monster trash | 5.75 | 276 |
| Monster fast-archetype | **7.5** | **360** |

**VS2a framing change.** No longer "playtest mid-game feel." Now: **end-game playtest. VS2a deliberately ships end-game balance state. The gauntlet shows the player what end-of-progression feels like; sim and demo agree on the same values; what the player feels IS what the engine balanced for.**

**Trade-off acknowledged.** VS2a no longer tests early-game progression pacing. Early-game-feel becomes a Playtest Cycle 1 question (post-Stage-A2 closeout), not a VS2a question. **Don't claim VS2a covers early-game pacing in playtest reports.**

**Cascade (operationalization):**
- **Rocket schema defaults updated:** `PlayerClass.movement_speed = 8.0` (was 5.75 in shipped default); `Monster.movement_speed` per-archetype end-game tuning (trash 5.75; fast 7.5)
- **Gamora Gate 3b sim consumption dispatch authored as VS2a-gating** — kiting modeling + 3-band distance state + AI_SPEED_MULTIPLIER 0.719 consumption
- **Star-lord Stage B export-DTO fix** (separate finding `2026-05-16-export-dto-stage-b-silent-drop.md`) becomes precondition — demo cannot consume engine-emitted MS until `ExportClass` + `ExportMonster` ship the field through consolidated JSON
- **Drax demo:** remove hardcoded values from `world/movement.ts`; consume engine-emitted MS via JSON post-Stage-B-fix; re-derive PIXELS_PER_METER conversions per consumed value (5.75 m/s × 48 = 276; 8.0 × 48 = 384; 7.5 × 48 = 360)
- **Decisions-log supersession entry:** knight-rider drafts; supersedes the prior Option-A entry; locks end-game-anchored values + VS2a-gating framing

**Sections of this doc now stale (preserved as historical record):**
- § "Player-state assumption (resolved Matt 2026-05-16; Option A locked)" — Option A SUPERSEDED
- § "Rationale for Option A" — applies to historical lock; Option B rationale lives above
- § "Drift watch" — drift is now CLOSED by Option B's sim-consumption commitment
- AI_SPEED_MULTIPLIER 0.767 references in § "Reconciliation with the AI speed multiplier" — superseded by 0.719

Read those sections for historical context only. **Operational values are this § "VERDICT REVERSAL" section's table.**

---

## Original locked values (Option A — historical; superseded by Option B above)

| Parameter | Locked value | Notes |
|---|---|---|
| Player base MS | **5.75 m/s** | Tier-1 ARPG mean of D2 run + D3 + D4 + PoE 1 (precise 5.7275; rounded for config cleanliness) |
| Early-game effective | **6.0 m/s** | +4% over base; near-parity with trash (genre convention) |
| Mid-game effective | **7.5 m/s** | +30% over trash baseline |
| **Late-game effective** | **8.0 m/s** | **PoE 1 outlier excluded per Matt; +39% over trash baseline; D4-ish late-game band** (now the VS2a default per Option B) |
| Monster trash MS | **5.75 m/s** | Parity with player base (genre convention) |
| Monster fast-archetype range | 6.6–7.5 m/s | Option B locks VS2a fast-archetype default at top of range (7.5 m/s); ~10–15% of monster mix |
| Range-profile MS variance | **dropped** | All classes same base MS; mobility identity expressed through ability design (B11 geometry palette) |
| Measurement unit | **continuous m/s** | Engine + sim use m/s natively; demo derives px/s |
| `PIXELS_PER_METER` (demo) | **48** | Standard ARPG isometric convention |
| ~~AI_SPEED_MULTIPLIER (demo, VS2a)~~ | ~~**0.767**~~ | ~~Derived: trash 5.75 ÷ player mid 7.5; chase margin 1.75 m/s = 84 px/s~~ — **SUPERSEDED by Option B: 0.719 (= 5.75 / 8.0)** |
| Decisions-log entry timing | **before drax begins implementation** | Per ADR-001 Matt-decision sequencing (Option A entry committed; Option B supersession entry pending) |

**Implied demo px/s at 48 px/m:**

| Stage | m/s | px/s |
|---|---|---|
| Base | 5.75 | 276 |
| Early | 6.0 | 288 |
| Mid | 7.5 | 360 |
| Late | 8.0 | 384 |

Compare current demo: 220 (close) / 180 (medium) / 150 (long) px/s with AI at 0.55× multiplier. **The new mid-game player value of 360 px/s is significantly higher than current 180 px/s medium.** Whether this represents a near-2× speed-up *in feel* depends on what the current implicit pixels-per-meter scale was — drax should back-derive against arena dimensions and report what magnitude of perceived feel-change the rebase produces.

**Gating:** **VS2a SHIP gate.** Demo VS2a does not ship until the values in this doc are implemented in the demo and named in the engine-emitted schema. Per Matt 2026-05-16.

**Reverses:** roadmap entry at `canonical/16-project-roadmap.md` § VS2a "Out of scope" — *"B12 (movement speed / boots / gear slot audit) — defers; not visually load-bearing for VS2a."* **A scoped subset of B12 — the movement-speed-baseline portion specifically — is now in VS2a scope.** Boots, gear-slot audit, and the +% MS affix economy remain B12-Stage-A2 work; the *baseline anchor* lands now.

**Supersedes the deferral on:** `canonical/story/engine-balance-stewardship.md` § Gate 3 Recommendation 3b ("schedule-or-defer per Matt"). Matt has chosen: schedule, now.

**Companion docs:**
- `canonical/story/engine-balance-stewardship.md` § Gate 3 — the original framing this doc operationalizes
- `agentic_orchestration/research/knowledge/arpg-movement-speed-reference-2026-05-16.md` — the Legolas research this doc consumes (Tier-1 numeric data)
- `canonical/story/season-feel-rubric.md` — what kind of seasons we're tuning for (movement is one axis of feel)
- `canonical/story/drift-audit.md` Drift-9 — *"Q2 movement empirically unknown"*; this doc closes that drift

**Engine + demo references:**
- `reincarnated-demo/src/world/movement.ts` — current hand-tuned px/s values (must be replaced)
- `reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md` § "Stage A2 movement-speed sim extension (engine-balance-stewardship lock 3b)" — gamora's queued consumer
- `canonical/16-project-roadmap.md` § B12 — gear-slot work remains Stage A2

---

## Why this doc exists (and why now, not later)

Movement speed is the single most load-bearing player-feel decision in an ARPG that does not get its own decisions-log entry by default. Every other player-feel knob — damage numbers, cooldowns, animation timing — gets exposed during normal development. Movement speed gets *baked into the engine as a constant* at the first prototype, never re-examined, and then defines the player's entire kinesthetic relationship with the game from that point forward. This is the pattern by which D3 launch shipped without FRW (a years-long regret); D4 launch shipped with a 125% cap and then quietly raised it to 200% post-beta; PoE 1 shipped with a base of 3.7 m/s that GGG then spent a decade fighting upward through flask/skill economies; PoE 2 EA explicitly walked the PoE 1 inheritance back as a generation-defining design correction.

Reincarnated's current state: the demo has invented its own px/s values because the engine doesn't emit `movement_speed`. The engine doesn't emit it because the simulation doesn't model movement-speed-aware combat. The simulation doesn't model it because no decision exists about *what movement speed even means* in this game. **Three layers of "we'll figure it out later" sitting in a stack.** The longer this stack stays unresolved, the more downstream tuning compensates for an unnamed constant. The current demo values (220/180/150 px/s by range profile, AI at 0.55×, +99 px/s chase margin tuned via four playtests) are a direct symptom: hand-fitted to *feel right against an unspecified design baseline.*

Matt's call to gate VS2a on this is correct. The cost of locking the baseline now is one design-doc + a demo edit + a small engine schema addition. The cost of *not* locking it now is that VS2a ships with values that may have to be retuned post-playtest, invalidating the playtest data those values informed.

---

## The Tier-1 ARPG average — math fully exposed

### Source data (Legolas research 2026-05-16, citations in source doc)

| Game | Base player MS (m/s) | Derivation |
|---|---|---|
| Diablo II / D2R (run) | **8.23 m/s** | 9 yards/s × 0.9144 m/yard |
| Diablo III | **5.49 m/s** | ~6 yards/s × 0.9144 |
| Diablo IV | **5.49 m/s** | ~6 yards/s × 0.9144 |
| Path of Exile 1 | **3.70 m/s** | direct (PoE wiki) |

**Unweighted Tier-1 mean: (8.23 + 5.49 + 5.49 + 3.70) / 4 = 5.7275 m/s**

Per-stage % progression (unweighted mean across same four games; from Legolas research):

| Stage | D2 | D3 | D4 | PoE1 | Tier-1 mean |
|---|---|---|---|---|---|
| Early | 102.5% | 100% | 100% | 112.5% | **103.75%** |
| Mid | 132.5% | 112.5% | 120% | 162.5%* | **131.88%** |
| Late (typical) | 157.5% | 125% (cap) | 144% | 225% | **162.88%** |

*PoE mid uses Quicksilver-active value; non-flask is 125–130%.

### The recommended values

| Stage | Tier-1 multiplier | Player MS (m/s, precise) | Locked value (rounded) |
|---|---|---|---|
| **Base** | 100% | 5.7275 m/s | **5.75 m/s** ✅ LOCKED |
| Early game | 103.75% | 5.94 m/s | **6.0 m/s** ✅ LOCKED |
| Mid game | 131.88% | 7.56 m/s | **7.5 m/s** ✅ LOCKED |
| Late game (Tier-1 mean *excluding PoE 1*) | 142.17% | 8.15 m/s | **8.0 m/s** ✅ LOCKED (Matt 2026-05-16) |
| ~~Late game (Tier-1 mean including PoE 1)~~ | ~~162.88%~~ | ~~9.33 m/s~~ | Rejected — PoE 1 zoom-zoom identity not the Reincarnated direction |

### The late-game PoE question — RESOLVED

Matt resolved (2026-05-16): **exclude PoE 1 outlier** from the late-game average. The locked late-game value is **8.0 m/s** (precise 8.15 m/s; rounded for config cleanliness). This places Reincarnated in the D4-ish late-game band (~+39% over trash baseline) rather than the D2/PoE wide-delta world.

**Design consequence:** keeping the late-game delta conservative preserves positional gameplay relevance throughout the player's progression curve. This is the D3/D4/Last-Epoch design family rather than the PoE-1-style player-supremacy approach. Fast monster archetypes remain meaningful at late game (a +39% player advantage is closeable by fast monsters at 115–130% of base); a +67% advantage would have made fast archetypes much harder to tune as threats.

---

## Monster baseline + delta progression

Per the Legolas research, the single most robust pattern in the genre is: **standard trash monsters are tuned at ~100% of player base speed across every Tier-1 game.** This is design-convergent across four developers' independent choices over twenty years.

**Recommendation: monster trash MS = player base MS = 5.73 m/s** (or 5.75 rounded). Both move at the same speed at base.

| Stage | Player MS | Trash monster MS | Delta |
|---|---|---|---|
| Early | 6.0 m/s | 5.75 m/s | **+4%** (near parity — by design) |
| Mid | 7.5 m/s | 5.75 m/s | **+30%** |
| Late | 8.0 m/s | 5.75 m/s | **+39%** (PoE 1 outlier excluded per Matt 2026-05-16) |

This places Reincarnated cleanly in the **D3/D4/Last-Epoch design family** — tighter delta than D2's late-game gear-only band, much tighter than PoE 1's 100–150%, modestly wider than D3's hard 25% cap. The late-game delta is *conservative-by-choice*: keeps positional gameplay relevant throughout progression; makes fast monster archetypes practically threatening (a +39% player advantage is closeable by 115–130%-base fast monsters); reads as deliberate rather than as a balance miss.

**Fast monster archetypes** — every Tier-1 game spices in monster types that exceed 100% of player base to keep positional awareness relevant: D2 Fetishes, D3 Vortex elites, D4 Corrupted Rogues, PoE Fast-affixed rares. **Reincarnated should follow this pattern.** Specific values are gamora monster-tier territory; the design constraint from this doc is:

- Standard trash: 100% of player base (5.75 m/s)
- Fast archetypes: 115–130% of player base (6.6–7.5 m/s) — selected enemy types only, ~10–15% of monster mix
- Boss/elite chase mechanics: skill-driven (dash, leap, charge), not base-MS-driven — matches genre

The fast-archetype tuning is what keeps positional gameplay meaningful even at +65% late-game player delta. Without it, late-game becomes walk-past-everything (PoE 1's failure mode that GGG is correcting in PoE 2).

---

## Continuous vs tile-based — the measurement framework

**Recommendation: continuous m/s, not tile-based.** Every Tier-1 ARPG uses continuous-space movement. Only roguelikes and turn-based tactical games use tile-based movement. Reincarnated's design pillars (real-time combat, position-as-mitigation, the cipher-substrate VFX layer) do not benefit from tile discretization and would *fight* tile-based movement at every layer.

**Reference units:**
- Engine + simulation: **meters per second (m/s)** — the natural unit; matches PoE, Torchlight II, and the converted Diablo values
- Demo (Pixi.js): **pixels per second**, derived from m/s × `pixels_per_meter` constant
- Engine schema (`movement_speed` field on combatant + monster): **m/s, float, 2-decimal precision** — single source of truth across all consumers

**`PIXELS_PER_METER` is LOCKED at 48** (Matt 2026-05-16). This is the standard ARPG isometric convention — sits between PoE 1's effective sprite scale and the D-franchise normalized scale. Drax adopts 48 as the canonical demo art-scale constant.

For reference (comparison only — 48 px/m is the lock):

| Art scale convention | pixels_per_meter | Implied px/s at 5.75 m/s base |
|---|---|---|
| Small-character ARPG (Hyper Light Drifter scale) | 32 | 184 px/s |
| **Standard ARPG isometric (LOCKED for Reincarnated)** | **48** | **276 px/s** |
| Large-character (Hades / Bastion scale) | 64 | 368 px/s |
| Demo's current implicit scale (back-derived; unverified) | ~24 | 138 px/s |

The current demo's implicit ~24 px/m scale (back-derived from current 180 px/s medium ÷ assumed 7.5 m/s mid-game) was never an explicit design choice. Drax should verify the back-derivation against arena dimensions in `arena.ts` and confirm the magnitude of the perceived feel-change the rebase to 48 px/m produces. Two outcomes are possible: (a) current arena is already designed for ~48 px/m and current 180 px/s medium represents ~3.75 m/s (PoE-1-base feel) — rebase is a +100% perceived speed-up; (b) current arena is designed for ~24 px/m and current 180 px/s medium represents ~7.5 m/s — rebase is a no-op in feel, just a unit clarification.

**Implementation formula (LOCKED):**
```
PIXELS_PER_METER = 48
px_per_sec = mps × PIXELS_PER_METER
```

**Locked demo px/s values** at 48 px/m:

| Stage | m/s | px/s |
|---|---|---|
| Base | 5.75 | **276** |
| Early | 6.0 | **288** |
| Mid (VS2a default) | 7.5 | **360** |
| Late | 8.0 | **384** |

---

## The range-profile variance question (this is a real design call)

Current demo has **per-range-profile player MS variance:**

| Range profile | Current px/s | Implied m/s (at 24 px/m) | % of demo mean |
|---|---|---|---|
| close | 220 | 9.17 | +22% |
| medium | 180 | 7.50 | (baseline) |
| long | 150 | 6.25 | −17% |

Spread: close is +47% over long. This is **a hand-tuned compensation for combat ranges** — close-range classes had to be faster to feel viable against ranged classes that could kite. It is not in the design canon; it's a playtest-derived workaround.

**The genre does not do this.** D2/D3/D4 have uniform base MS across all classes; PoE has uniform base MS regardless of build. Class-mobility-identity in those games is expressed through *abilities* (D4 Druid bear-form mobility; PoE Pathfinder flask economy; D2 Barbarian Charge), not through *base MS variance.*

**LOCKED: drop range-profile MS variance** (Matt 2026-05-16). All classes move at the same base MS (5.75 m/s; effective at stage per progression curve). Close-range vs long-range viability is balanced through:

1. **Effective range of abilities** — close-range classes have higher DPS once in range; long-range classes have higher safety
2. **Mobility skills as identity** — close-range classes get dash/charge geometries; long-range classes get teleport/blink. The geometry palette (B11, 16→25 expansion in VS2a scope) is the right home for this
3. **AI tuning** — ranged AI kites at retreat-speed; melee AI closes at chase-speed; both at the same base MS multiplied by the AI multiplier

This is the **major reconciliation work** for the demo. The current per-range `MOVE_SPEED` lookup (220/180/150 px/s) collapses to a single base value × `PIXELS_PER_METER`. It will require:

- Replacing `MOVE_SPEED: Record<string, number>` with `MOVE_SPEED_BASE` constant in `world/movement.ts`
- Replacing `speedForProfile(profile)` with `playerMoveSpeed(combatant)` reading from engine-emitted `movement_speed` field (or hardcoded constant pending schema)
- Replaying playtests #3 and #4 conclusions against the new baseline
- Re-deriving AI_SPEED_MULTIPLIER from named design intent (locked at **0.767** for VS2a mid-game-equivalent — see § "Reconciliation with the AI speed multiplier" below)
- Re-tuning AI engagement distances if the new base MS changes how packs close (likely small adjustments to `PREFERRED_RANGE` and `KITE_TRIGGER`)

**Class-mobility identity** — under the locked decision, mobility-as-identity belongs to ability design (B11 geometry palette + B13 active mobility), not base-MS variance. The geometry expansion in VS2a (16→25) is the natural home for close-range classes to get dash/charge geometries that *functionally* make them mobile without inflating their base MS stat. This is genre-aligned (D2 Charge, D4 Druid forms, PoE Pathfinder flask economy all express class mobility through abilities, not base stats).

---

## Reconciliation with the AI speed multiplier

Current demo: `AI_SPEED_MULTIPLIER = 0.55`, producing ~99 px/s chase margin (player 220 close − AI 165 = 55 effective with current ranges).

**The 0.55 multiplier is genre-honest.** It encodes "monster trash = 100% of player base when player is at base, but player has gear/skills above base." For early-game gameplay where player IS at base, the multiplier should be higher (closer to 1.0 — parity). For late-game gameplay where player is at +65% over base, the multiplier should compress (closer to 0.6 — preserving the delta).

**Recommendation: keep AI_SPEED_MULTIPLIER as the single-chokepoint mechanism**, but anchor its value to a design intent rather than playtest fitting:

- **Per genre convention: AI_SPEED_MULTIPLIER = 1.0 at early game (parity)** — player + trash both move at 5.75 m/s
- **For VS2a (gauntlet is mid-game-ish per file 28 § B12 framing): AI_SPEED_MULTIPLIER = 0.767** — player at 7.5 m/s mid; trash at 5.75 m/s base; ratio 5.75/7.5 = 0.767
- **At late-game tuning: AI_SPEED_MULTIPLIER = 0.605** — player at 9.5 m/s; trash at 5.75; ratio 5.75/9.5 = 0.605

The current 0.55 is **lower than even the late-game value** — i.e., the demo is currently telling the player they are faster than a late-game ARPG character. That's a tell that the range-profile MS variance was over-tuned upward and the multiplier had to compensate downward.

**If we drop the range-profile variance AND rebase to 7.5 m/s mid-game-equivalent at VS2a**, the recommended multiplier is **0.767**. Chase margin becomes 7.5 − (7.5 × 0.767) = 1.75 m/s, which at 48 px/m = 84 px/s — comparable to the current ~99 px/s margin but derived from named design intent.

---

## Engine + simulation implications

### Engine schema additions (rocket scope; possibly very small)

Add `movement_speed` field to:
- Class-template JSON exports (single base value per class — 5.75 m/s default; can vary if range-profile variance is kept)
- Monster-tier JSON exports (per-tier base — trash at 5.75; fast archetypes at 6.6–7.5; named bosses at gamora design-call)

**Estimated lift:** trivial schema addition. Maybe 1-2 hours rocket, mostly testing.

### Simulation consumer (gamora scope; consumes Gate 3b)

Per `engine-balance-stewardship.md` § Gate 3 Recommendation 3b: extend `fight_engine.py` with per-tick movement-speed-driven distance updates, replace binary at_melee_range with 3-band distance state (melee / near / mid), enable basic kiting modeling for single-target archetypes.

**Estimated lift per Gate 3b:** ~1.5–2 weeks gamora. VS2a may not need *full* 3b consumption — the MS values can land in schema + demo without full sim consumption — but the schema-emit-without-consumer pattern is exactly the P5 drift the team has been flagging.

**Recommendation:** ship the schema + demo consumption for VS2a; schedule full sim consumption (Gate 3b in full) as a tightly-following ticket. Gamora's existing `AGENT_STATE.md` flag for Stage A2 movement-speed sim extension picks this up.

### Demo consumer (drax scope; the visible VS2a change)

Replace `reincarnated-demo/src/world/movement.ts`:

1. Remove `MOVE_SPEED: { close, medium, long }` lookup table; replace with single `MOVE_SPEED_BASE` constant (or read from engine-emitted `movement_speed` per class)
2. Add `PIXELS_PER_METER` constant; pick value based on art scale (recommend explicitly choosing and documenting)
3. Replace `speedForProfile(profile)` with `playerMoveSpeed(combatant)` reading from engine data
4. Re-derive `AI_SPEED_MULTIPLIER` per the design intent above (0.767 for VS2a mid-game-equivalent gauntlet)
5. Re-test ranges + chase margin against new baseline
6. Update phase-6.x calibration comments to reference this doc

**Estimated lift:** ~1-2 days drax, mostly re-tuning + playtest validation, not implementation.

### Telemetry (star-lord scope; minor)

Recommendation: emit observed player MS per fight in telemetry to enable post-hoc validation of the design baseline against actual gameplay. ~1 hour star-lord lift; not VS2a-gating.

---

## Per-seam action items (handoff summary)

| Seam | Action | Gates VS2a? | Estimated lift |
|---|---|---|---|
| **knight-rider** | Author dispatches per § "Memo to knight-rider" below; draft decisions-log entry; sequence drax + gamora work | Yes (sequencing gate) | ~2 hours |
| **rocket** | Add `movement_speed` field to class-template + monster-tier JSON exports | Yes (schema gate) | ~1-2 hours |
| **drax** | Replace `world/movement.ts` per § "Demo consumer" above; pick `PIXELS_PER_METER`; re-tune AI multiplier; re-validate via playtest | Yes (demo gate) | ~1-2 days |
| **gamora** | Schedule full Gate 3b sim consumption as tightly-following ticket; VS2a does not require sim-side completion but schema-emit-without-consumer drift will trigger jack-ryan if left unactioned | No (VS2a); Yes (post-VS2a tight follow) | ~1.5-2 weeks |
| **star-lord** | Add per-fight observed-MS telemetry emission | No | ~1 hour |
| **jack-ryan** | Gate-2 review of decisions-log entry; verify schema-emit-with-consumer pairing closes by VS2a+1 | No (review only) | ~1 hour |
| **elrond** | None — no catalogue or curation impact | No | 0 |
| **legolas** | None — research already filed and consumed | No | 0 |

---

## Open questions — RESOLVED 2026-05-16

All five resolved by Matt:

1. **Late-game value: exclude PoE 1 outlier.** Locked at 8.0 m/s late game.
2. **Range-profile MS variance: drop.** All classes same base MS per genre convention. Mobility identity via ability design (B11 / B13).
3. **Precise vs rounded base: rounded.** 5.75 m/s (precise 5.7275; deviation < 0.5%).
4. **PIXELS_PER_METER: 48** (standard ARPG isometric convention).
5. **Decisions-log entry: before drax begins implementation.** Per ADR-001.

---

## Player-state assumption (resolved Matt 2026-05-16; Option A locked — ⚠️ SUPERSEDED by Option B; see § "VERDICT REVERSAL" above)

**The Tier-1 ARPG numbers this doc consumes are NOT character-baseline at all stages.** They represent a progression curve from near-baseline-character (early) to fully-equipped-and-buffed-character (late):

| Stage | What the Tier-1 % includes |
|---|---|
| Early (~104%) | D2/D3/D4: near-baseline, no MS gear. PoE 1: typical starter boots (Runner's/Sprinter's 10–15% MS). |
| Mid (~132%) | D2: 60–100% FRW from gear (moderate, not BiS). D3: ~10–15% MS from one boots roll + few Paragon points. D4: typically one boots affix rolled. PoE 1: includes Quicksilver flask active state. |
| Late (~142%, our locked value w/o PoE) | D2: full gear + skill FRW active (Vigor/Burst of Speed/Frenzy). D3: cap from gear + Paragon + passives. D4: L100 Ancestral BiS, both boots + amulet rolled (skill buffs excluded). |

The **truly unbuffed/ungeared character** is exactly the 100% values — averaging to **5.75 m/s** (the locked base).

### What this means for VS2a (Matt-locked Option A)

The engine currently models **zero gear MS** (full B12 gear-slot audit is Stage A2) and **zero skill MS buffs** (no MS-affecting geometries in the palette). Under strict honesty, the VS2a player has no investment that justifies being above 5.75 m/s baseline.

**Matt has chosen Option A (2026-05-16): lock VS2a player at 7.5 m/s (mid-game Tier-1 average) despite the engine not yet modeling the gear MS that would justify it.** The 7.5 m/s value represents the **eventual feel-target** for a mid-game-stage Reincarnated character with moderate MS gear investment. Until B12 full audit lands in Stage A2, VS2a deliberately pre-implements the eventual mid-game feel.

### Rationale for Option A

1. **VS2a showcases pacing, not character build-state.** It is not trying to simulate a specific build-state at level X with Y gear; it is trying to feel like ARPG combat at the intended gauntlet balance point. The gauntlet per file 28 § B12 is mid-game-ish; mid-game ARPG combat is 7.5 m/s.
2. **Playtest cycle clarity.** If VS2a shipped 5.75 m/s baseline and post-B12 shipped 7.5 m/s mid-game, two consecutive playtest cycles compare against shifting baselines. Locking the eventual feel-target now means playtest #5 (post-VS2a) and playtest #7 (post-B12) compare against the same target.
3. **The AI multiplier depends on it.** AI_SPEED_MULTIPLIER = 0.767 is derived from "trash 5.75 ÷ player mid 7.5." Rebasing player to 5.75 would collapse the multiplier to 1.0 (parity) and trigger a different AI engagement design.
4. **Genre precedent.** D3 Inferno-era launch players were at 100% base with no MS gear; the +25% cap was an *aspirational* feel-target reached over weeks of play. The mid-game feel is always the design north star, even when the early-game character can't yet match it.

### What this implies for B12 full audit (Stage A2)

When B12 lands, gear MS will become an *earned* axis: the player's effective MS is the function of gear investment that the Tier-1 % values describe. At B12 ship time:

- L1–20 character with starter boots → 6.0 m/s early (matches Tier-1 early; +4% over trash; near-parity)
- L40–60 character with moderate MS gear → 7.5 m/s mid (matches Tier-1 mid; the VS2a default becomes the actually-earned value)
- L80+ character with BiS gear + (eventual) skill buffs → 8.0 m/s late (matches Tier-1 late no-PoE; +39% over trash)

The progression curve becomes player-experienced rather than pre-baked. **VS2a's 7.5 m/s is a placeholder for what the B12-shipping player will earn through gear.** When B12 ships, the demo's hardcoded mid-game-equivalent constant becomes the function-of-gear computation.

### Drift watch

This is an **explicit deferred-implementation assumption.** If B12 slips substantially (>6 months from VS2a ship), the VS2a 7.5 m/s value will become harder to defend as "eventual feel-target" and may need rebasing to honest baseline. Knight-rider should flag if B12 slips beyond Stage A2 target window so this drift can be addressed before it festers.

---

## What this does NOT lock

- **+% MS gear affixes** — B12 full gear-slot audit territory; Stage A2; not VS2a
- **Boots gear slot** — same
- **Movement skill VFX** (dash, charge, blink, teleport) — B13 active mobility; not VS2a
- **Mount/overworld movement** — not in current scope
- **Class mobility kits** — B11 geometry expansion (16→25) covers this in VS2a separately
- **Slow / chill / root status effects** — already partially modeled; this doc doesn't touch the slow_percent / chill / stagger / knockback infrastructure
- **PoE 2-style movement-skill economy** — not Phase 0 scope

---

## Memo to knight-rider — what needs to happen

This doc surfaces a **scope insertion against VS2a.** It requires the following from knight-rider per ADR-002 dispatch authority:

1. **Author rocket dispatch** for `movement_speed` schema addition (class-template + monster-tier JSON; m/s field, 2-decimal precision; default value from this doc)
2. **Author drax dispatch** for demo movement-speed-baseline implementation (per § "Demo consumer" above); should reference this doc as required reading
3. **Author gamora dispatch** for Gate 3b sim consumption as tightly-following ticket (does not gate VS2a ship but gates VS2a+1 closure of schema-emit-without-consumer drift)
4. **Draft decisions-log entry** capturing:
   - Player base MS = **5.75 m/s** (rounded per Matt; precise 5.7275)
   - Early/mid/late progression curve = **6.0 / 7.5 / 8.0 m/s** (late excludes PoE 1 per Matt)
   - Monster trash MS = **5.75 m/s** (parity); fast archetypes 6.6–7.5 m/s
   - Measurement = **continuous m/s** at engine/sim; demo derives px/s via `PIXELS_PER_METER = 48`
   - Range-profile MS variance = **dropped** per Matt; mobility identity via ability design
   - This doc as authoritative reference
5. **Update `canonical/16-project-roadmap.md`** § VS2a:
   - Move "B12 (movement speed / boots / gear slot audit)" out of "Out of scope" with the scoped-subset note (full B12 stays Stage A2; baseline subset is VS2a)
   - Add new line item: "Movement-speed baseline implementation (per `canonical/story/movement-speed-baseline.md`)"
   - Update VS2a "Ship trigger" to include movement-speed-baseline implementation
6. **Notify drax + gamora + rocket** that dispatches are inbound; coordinate ordering (rocket schema → drax demo + gamora sim sim-consumer schedule)
7. **Brief Matt** on the five open questions; collect answers; cascade into this doc + decisions-log entry

**Sequencing:** rocket schema can land first (1-2h); drax demo work depends on schema being available (or can hardcode the constant pending schema); gamora sim work is post-VS2a. The critical path is rocket → drax → playtest validation → VS2a ship.

**Decisions-log entry classification:** this is a Matt-decision per ADR-001 (design-direction call). Decisions-log entry should land before drax begins implementation, not after.

---

## Cross-references

- **Required reading consumed:**
  - `agentic_orchestration/research/knowledge/arpg-movement-speed-reference-2026-05-16.md` — primary numeric source
  - `canonical/story/engine-balance-stewardship.md` § Gate 3 — original deferral being reversed
  - `canonical/16-project-roadmap.md` § B12 + § VS2a — scope context
  - `reincarnated-demo/src/world/movement.ts` — current implementation being replaced
  - `reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md` — gamora's queued consumer flag

- **Drift-audit instances addressed:**
  - Drift-9 (Q2 movement empirically unknown) — fully resolved by this doc

- **Supersedes:**
  - `engine-balance-stewardship.md` § Gate 3 Recommendation 3b deferral — Matt has chosen "schedule now"
  - `canonical/16-project-roadmap.md` § VS2a "Out of scope" entry for B12 — scoped subset is now in scope

- **Does not supersede:**
  - B12 full scope (gear slots, +% MS affixes, hard-cap design) — remains Stage A2 work
  - Gate 3 Recommendation 3a (abstraction-naming in design docs) — still relevant; this doc satisfies it implicitly via the m/s + 3-band-distance-state recommendation

---

## Maintenance protocol

When playtests on VS2a return feedback:

1. **"Player feels slow / fast"** — check the m/s baseline against this doc. The Tier-1 average is the lock; if Reincarnated diverges from it, name the divergence as a deliberate Matt decision, not a tuning drift.
2. **"Trash monsters feel sluggish / overwhelming"** — check fast-archetype mix percentage; the design intent is 10–15% fast archetypes spiced into trash mix.
3. **"Kiting doesn't work" / "Single-target classes feel helpless against packs"** — this is the gate that gamora's sim consumption (Gate 3b) was supposed to validate. Real-game kiting effectiveness should match sim predictions once 3b lands.
4. **"Close-range classes feel slow / long-range classes feel exposed"** — if Matt chose to drop range-profile MS variance, this is *expected behavior*; mitigation is mobility-skill ability design (B11 geometry palette expansion), not base MS retuning.

When future B-series engine-balance work surfaces movement-related gates:

1. Reference this doc as the baseline
2. Apply deviations explicitly as named decisions
3. Surface drift instances to `drift-audit.md` if implicit-pillar drift is observed

— gandalf, 2026-05-16 (Day 4)
