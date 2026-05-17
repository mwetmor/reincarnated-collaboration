# Canonical-Four Intrinsic Trait Pool Authoring — L3 Decision Briefing

**To:** Matt (senior architect)
**From:** gandalf (story-and-design steward)
**Routing:** knight-rider relay 2026-05-18 — Matt explicitly engaged; full options + recommendation requested
**Status:** L3 decision pending — Matt's call
**Authored:** [2026-05-18 12:44Z]
**Companion:** `phase-1-p1-log.md` AMENDMENT [2026-05-18 04:00Z]; D8 design doc `canonical/story/d8-trait-floor-design-phase-1-p1.md`

---

## § 0 — TL;DR

While authoring D8 (per-class intrinsic trait pools for lightning / holy / shadow), I discovered that **the canonical-four classes — fire_mage, water_controller, earth_caster, wind_controller — do not have authored intrinsic trait pools.** Canonical 32 § 4 commits the architecture for ALL classes (5–10 traits each, floors L1/12/25/38, converge L50); the engine has the trait *infrastructure* (`TraitSchema`, `_STAT_TRAIT_POOL` for gear stat-traits) but no per-class authored pools. **D8 is the first authored instance of any kind.**

Shipping Phase-1 P1 as-spec means **3 substrates have characterization depth via 8-trait intrinsic pools; 4 substrates rely on gear-only.** That is a player-visible asymmetry — and an asymmetry pointed the wrong way (the new substrates feel richer than the familiar ones).

**My recommendation: Option I — expand Phase-1 P1 scope to author the canonical-four intrinsic trait pools.** ~1 week additional total work (gandalf authoring + gamora implementing). The cosmology does not authorize asymmetry in trait-depth across the seven substrates; the substrate-expansion design promise was *additive equality* (more substrates, equal depth), not *new-substrate privilege*. Option II ships sooner but with the asymmetry visible, and the work doesn't get cheaper in P2.

I'm not 100% certain Option I is right. I'll name the parts that make me uneasy in § 6. But on weight of evidence, this is one to do now, not later.

---

## § 1 — What I discovered

D8's scope of work is "trait-floor extension to 3 new classes (lightning, holy, shadow)." I interpreted this as authoring three pools — and that is exactly what scope-of-work § 1.2 D8 says. Per the document on my desk, the work I did is correct and complete.

What I found while doing it: **the architecture description in canonical 32 § 4 + the `project_trait_architecture` memory describe a system that is not yet built.**

Specifically:
- Canonical 32 § 4 (locked 2026-05-11) says: "Each class has a curated trait pool of 5-10 traits with floors at L1/L12/L25/L38." Universal language. No exception for canonical-four.
- `project_trait_architecture` memory (2026-05-12) says: "per-class intrinsic trait pool (B9a, 5-10 traits, floors at L1/12/25/38, converge at L50)." Same universal commitment.
- `reincarnated-engine/src/reincarnated/character/trait_schema.py` exists. `TraitSchema` validates trait shapes. The infrastructure is there.
- `gear_generation.py:738` defines `_STAT_TRAIT_POOL` — but this is the *gear-roll stat trait pool*, the universal gear surface. **Not** per-class intrinsic pools.
- I searched. There are no per-class trait pool files for fire_mage, water_controller, earth_caster, or wind_controller anywhere in the engine or in `canonical/story/`.

So when I sat down to author lightning_class's 8-trait pool, I expected to find fire_mage's existing 8-trait pool open on a nearby file and use it as a reference for parity. I expected to be authoring *parallel-pattern work*. Instead, **D8 is the first per-class intrinsic trait pool authoring in the project**, full stop.

Three pools shipped. Four pools still vacant. The canonical-four classes have functioned through B14.5 + Drift-14 + Phase-1 P1 design without intrinsic trait pools — they are not broken. But they are not at the depth the architecture promises.

---

## § 2 — The asymmetry — what it means concretely

### In-game player experience

Under Option II (ship P1 as-spec), at L1 a player in lightning_class sees:
- "Arc Initiate" — your lightning arcs to +1 target
- "Discharge Threshold" — crit damage amplified on 3+ chain targets

At L1 the same player rolling fire_mage sees: their fire skills, their fire stat block, and whatever gear-affix traits dropped. No intrinsic floor-1 identity-anchor passives that say *this is what fire IS*.

By L38 the gap widens. Lightning has 8 intrinsic traits stacking with gear; fire has gear-only. The player's class-identity surface area, expressed in passive characterization, is **lopsided 8-to-0.**

### Phase-1 P1 ship-state

- 3 substrates with characterization depth: lightning, holy, shadow
- 4 substrates with gear-only trait expression: fire, water, earth, wind
- Phase-1 P1 ships at 3/7 substrate parity for intrinsic-pool depth

### Spirit-swap differentiation impact

The differentiation pillar (project_design_intent: "spirit-swap differentiation confirmed load-bearing") is **not broken** under Option II. The mechanical_signature still distinguishes substrates; substrate-coherent gear-affix rolls still characterize. Differentiation is preserved at the level of "fire mage feels different from lightning class."

But the *depth of characterization* is uneven. The new substrates feel mechanically richer than the familiar ones — and this is the wrong direction. The substrate-expansion-decision design promise was: *Phase-1 P1 adds substrates while preserving every player's existing class experience*. Players returning to fire_mage after the expansion should find fire feeling *more* alive, not less, relative to the new neighbors.

### Player perception risk — what they would feel

This is the load-bearing risk. The player who fires up Phase-1 P1, plays a few seasons, and rolls into lightning_class for the first time will feel: *"This class has more going on than my old familiar fire mage."* That is a perception we authored when we shipped the lightning pool; we cannot un-author it without authoring the fire pool too.

In Diablo II terms: this is what it would feel like if Necromancer had 20 synergy bonuses and Sorceress had 4. The newer / less-played class would feel richer than the foundational one. D2 did not ship that asymmetry, and players would have noticed.

### Cosmological integration — does the cosmology authorize this asymmetry?

Direct answer: **no.**

The cosmology says the substrates are *peers in the wheel* — not seven things of varying ontological weight, but seven names the world wears for the same depth. `cosmology-reincarnated.md` § "The Wheel" frames the substrates as cosmologically equivalent expressions; substrate-expansion-decision § 5.1 explicitly chose to keep lightning's resistance behavior "like the canonical-four" rather than introducing tiering. The substrate-identity-declaration spec uses one schema for all seven entries.

If we ship 3-of-7 with intrinsic depth, the cosmology is *spoken-but-not-instantiated* for the canonical-four. The architecture document promises depth; the engine delivers it for three substrates; the cosmology says the wheel is symmetric. Three voices, one direction.

That said, the cosmology does not *forbid* a sequencing where some substrates get their intrinsic depth before others. It just doesn't authorize the asymmetry as *intentional*. This is a "we got here by accident of authoring order" asymmetry, not a "the cosmology says lightning gets a deeper soul than fire" asymmetry.

---

## § 3 — Option I — Expand Phase-1 P1 scope: author canonical-four trait pools

### What gandalf does

4 additional pools × 8 traits = 32 more traits. Per-class authoring with:
- Substrate identity declarations as the constraint surface (mechanical_signature, iconic_verbs, forbidden_mechanics, combat_pillar)
- Floor cadence 2/2/2/2 across L1/L12/L25/L38 (matching D8 pattern)
- Substrate-coherence audit (no canonical-four trait violates other substrates' forbidden_mechanics)
- Genre lineage citations (D2/D3/D4 fire wizards, PoE elementalist trees, Last Epoch elements, etc.)

**Effort estimate: ~3-4 days authoring.** The pattern is established (D8 took ~1.5 days authoring once I had the architecture in hand). The substrate identities are well-defined and locked. The trait architecture is mature. This is parallel-pattern execution — not new design exploration.

The genre lineage work is actually *easier* for canonical-four than for the new substrates. Fire mage / water controller / earth caster / wind controller have decades of ARPG precedent — D2 Sorceress fire/cold/lightning trees, D3 Wizard elements, D4 Sorcerer, PoE Elementalist, Last Epoch Sorcerer, Grim Dawn Pyromancer. The hardest part of D8 was synthesizing thin genre canon for "holy mage" and "shadow drain caster" away from the D2 Paladin / Necromancer crystallizations. Fire and friends will be smoother.

### What gamora does

Extends the D8 implementation contract to cover all 7 substrates. The D8 implementation pattern is already specified (D8 § 6); generalizing it from 3 substrates to 7 is parallel-pattern code work. **Adds ~1-2 days to gamora's existing D8 implementation contract** (~6.5 days → ~8 days). The infrastructure (TraitSchema, per-class trait_pool loaders) is built once for D8; canonical-four pools plug into the same loader.

### Phase-1 P1 timeline impact

~1 week additional total (gandalf authoring ~3-4 days while gamora is on D8 + D10 code phases; gamora canonical-four impl ~1-2 days appended to D8 contract). The critical path stays at gamora; gandalf authoring happens in parallel with other gamora work. Net P1 slip: ~1 week.

### Ship benefit

- Phase-1 P1 ships *substrate-symmetric*: all 7 substrates have intrinsic trait pools
- Canonical 32 § 4 architecture commitment is *instantiated for all seven*, not described-and-deferred
- Player experience returns to fire_mage feel *richer*, not poorer, after the substrate expansion
- The "additive equality" design promise is honored

### Risks

- **Scope expansion can grow.** Once we start authoring canonical-four pools, gear-affix considerations may want re-balancing (the D9 audit assumed canonical-four gear-affix surface unchanged; if canonical-four intrinsic pools introduce new ability_modifier_keys, gear affixes may want extending too). I judge this risk *low* — canonical-four substrates use well-trodden mechanical primitives (fire DoT, water control, earth root, wind displacement) — no new ability_modifier_keys are likely required. But the risk is non-zero.
- **P2 candidate timing pressure.** If Matt commits poison/acid as P2 substrate, the P1 slip pressure compounds. P2 still has to wait for P1 ship.
- **Perfectionism trap.** "We must author all canonical-four pools before shipping" can spiral into "we must also re-validate the gear-affix audit, also extend the resistance-matrix math, also redo balance smoke runs." I think the work is bounded; jack-ryan can fence it.

---

## § 4 — Option II — Defer canonical-four trait pool authoring to Phase-1 P2

### What ships in Phase-1 P1

- 3 new substrate intrinsic pools (lightning + holy + shadow)
- Canonical-four classes: gear-only trait expression (current state preserved)
- All other P1 deliverables ship as planned

### What goes to Phase-1 P2

- Canonical-four intrinsic pool authoring (4 pools × 8 traits = 32 traits)
- Poison/acid P2 substrate candidate (if Matt commits)
- Layer 5 telemetry feedback loop
- Other P2 scope

### Ship benefit

- Phase-1 P1 ships sooner (~1 week earlier vs Option I)
- Scope FIXED — no protocol § 10.1 discipline violation
- Smaller change surface for jack-ryan continuous-observation review

### Risks

- **Asymmetry is player-visible during the P1 → P2 window.** Whatever that window is (probably 2-6 weeks based on roadmap cadence), players experience the lopsided characterization. Player feedback may surface this as "the new classes feel deeper than the old ones." That feedback then becomes pressure for an unplanned mid-P2 hotfix.
- **Canonical 32 § 4 architecture commitment is delayed.** The architecture has been locked since 2026-05-11 (one week ago). Shipping P1 with the architecture described-but-partially-instantiated extends the delay further.
- **The work doesn't get cheaper in P2.** The pattern is established now. Doing it in P2 means context-switching back into trait authoring after gandalf has moved on to other work. ~3-4 days authoring is the same in both worlds. P2 does not save effort; it only delays cost.
- **D9 informational soft-tension flags carry forward.** D9 left 2 jack-ryan watchpoints for canonical-four affix coherence vs the new pools. If canonical-four intrinsic pools land in P2, those watchpoints stay open through the P1 window.

---

## § 5 — Other paths considered

### Option III — Partial expansion: ~4 traits per canonical-four class

Author half-depth pools (4 traits per class × 4 classes = 16 traits, vs the 32 in full Option I). Each canonical-four class gets L1 + L25 floors only; L12 + L38 deferred to P2.

**Pros:**
- ~1.5-2 days gandalf authoring (vs ~3-4 days full)
- Reduces but does not eliminate the asymmetry
- Honors "every class has *some* intrinsic depth" floor

**Cons:**
- Half-asymmetry is still asymmetry. New substrates have 8 traits; old substrates have 4. The player who counts will still count.
- Authoring the L1 + L25 pair *without* the L12 + L38 pair makes the L12 + L38 future-work harder — the L25 trait was authored assuming what would land at L12 between it. Authoring without the full architecture in view introduces local optima that fight global coherence later.
- The cosmology doesn't authorize 4-vs-8 either. It's a smaller version of the same problem.
- Half-effort, half-result. The work doesn't compound favorably.

**I would not recommend Option III.** It is the path that looks safe but accumulates technical debt. Either ship symmetric or ship asymmetric-with-eyes-open; don't ship half-symmetric.

### Option IV — Defer ALL trait pool authoring to P2 (including D8 already shipped)

Revert D8. Ship Phase-1 P1 with substrate identity declarations + composition + resistance matrix + ailment registry but no intrinsic trait pools anywhere. Trait pool authoring becomes a unified P2 milestone covering all 7 substrates at once.

**Why declined:**
- D8 is committed in canonical/story/. Reverting is wasted work.
- D9 gear-affix design depends on D8 (rank-stack architecture references intrinsic ability_modifier_keys). Reverting D8 propagates.
- Gamora has D8 + D9 already in queue. Reverting destabilizes gamora's sequencing.
- The character-depth improvement from intrinsic pools is one of the more visible Phase-1 P1 promised wins. Shipping P1 without any intrinsic pools weakens the P1 demo materially.

Document for completeness only; not seriously considered.

### Option V (one I want to surface) — Author canonical-four pools as *gandalf-only* work during P1, ship gamora-impl in P2

Gandalf authors all 4 canonical-four pools during the P1 window (~3-4 days), commits them to `canonical/story/`, but the gamora-implementation work is deferred to P2. P1 ships with 3 substrates *implemented* + 4 substrates *design-authored-but-not-implemented*.

**Pros:**
- Authoring is the harder-to-context-switch work; doing it now while the design context is hot is cheaper.
- The implementation work (~1-2 days gamora) is parallel-pattern code that's easy to defer without losing context.
- Ship gate for P1 doesn't slip — gamora's queue is unchanged.
- The asymmetry is *temporary*: the design exists; only the implementation lags.

**Cons:**
- The asymmetry is still player-visible during the P1 → P2 window (only player experience matters; design-only authoring doesn't help the player).
- Splitting authoring from implementation across a milestone boundary creates a fragile handoff. The risk is the canonical-four design sits in `canonical/story/` for a P1 window, then gets touched up during P2 implementation, then drifts from D8 patterns.

**I would consider Option V seriously as a fallback if timeline pressure is high.** It doesn't fix the player-experience asymmetry but it does fix the *design-debt* asymmetry, which is the long-term shape of the problem.

---

## § 6 — My recommendation

**Option I — expand Phase-1 P1 scope to author and implement canonical-four intrinsic trait pools.**

Why:

1. **Project intent.** The substrate-expansion-decision design promise was *additive equality* — Phase-1 P1 adds substrates while preserving canonical-four depth, ideally enhancing it. Shipping with new substrates *deeper* than old substrates inverts the promise. Players returning to fire_mage after the expansion should not feel they lost ground; they should feel the substrate floor lifted.

2. **Phase-1 P1 design promise.** P1's named pillars are "substrate expansion → genre floor" and "spirit-swap differentiation preservation." The first pillar speaks of *floor* — bringing all substrates to a baseline of richness. Shipping with 3/7 substrates at floor and 4/7 below floor undercuts the pillar's own language.

3. **Player-experience risk.** This is the strongest argument. The player who feels the new substrates are more interesting than their familiar one experiences a *negative* substrate-expansion outcome. We added work and made the existing experience feel worse by comparison. That is the worst possible read on a substrate expansion.

4. **Cosmological coherence.** The cosmology speaks the seven substrates as peers in the wheel. Shipping with 3-of-7 instantiated creates a *spoken-but-not-honored* asymmetry that we will eventually have to reconcile. Doing the work now reconciles it cleanly; deferring creates "trail debt" that compounds.

5. **Engineering pragmatism — the work doesn't get cheaper later.** ~3-4 days gandalf authoring + ~1-2 days gamora implementation is the same in P1 or P2. P2 deferral does not save effort; it only delays cost while accruing player-experience risk.

6. **Genre canon depth supports the work.** Canonical-four substrates have *more* genre precedent than the three new substrates, not less. The authoring will be faster, not slower, than D8.

### What makes me uneasy

I need to be honest. Two things give me pause:

**(a) Scope-creep risk on a hive-mode P1 that's already complex.** Phase-1 P1 has 26+ deliverables across 6 seams. Adding a 27th deliverable mid-flight is the kind of move that, in Diablo-development history, has destabilized milestones (D3 release was delayed in part by mid-milestone scope additions). I'm proposing a scope addition while jack-ryan is mid-Discipline-#13 continuous-observation. That's a Discipline #12 (semantic shift) signal even if the work itself is clean.

**(b) The discovery is real, but it was a discovery I made, not one Matt asked me to make.** Phase-1 P1 was scoped before I noticed this gap. The "right" move within the protocol is to honor the scope and surface the discovery for P2. Option I is me arguing my discovery merits scope expansion. That's a strong claim and deserves scrutiny — Matt's prerogative to push back on, fully.

I will be at peace with Option II if Matt judges scope discipline trumps cosmological coherence here. Option II is *fine*; it's not *ideal*. The asymmetry is visible but not breaking. The architecture commitment is delayed but not abandoned. The player-experience risk is real but bounded — the P1 → P2 window is finite, and feedback can be incorporated.

But on weight: Option I is what the cosmology asks for; Option I is what the player deserves; Option I is what the architecture has been promising for a week. If we can absorb ~1 week of additional P1 time to deliver substrate-symmetric depth, we should.

---

## § 7 — Cascading consequences either way

### Under Option I

**Gamora queue:**
- D8 implementation contract extends from 3 → 7 substrate pools (~6.5 days → ~8 days)
- D9 gear-affix audit re-runs against canonical-four pools (low-risk; D9 already audited canonical-four affix surface for incoherence; cross-check with intrinsic pools is mostly verification)
- Critical path may shift: if D8 grows by 1-2 days, downstream deliverables (D10 already in math phase; D14 dependent on D27 perception test) reflow

**Jack-ryan watchpoints:**
- D9 informational soft-tension flags close cleanly (canonical-four affix coherence vs intrinsic pools becomes verifiable)
- New Discipline #13 watchpoint: cross-substrate parity on per-rank curve calibration (does fire_mage_t1_kindling reach equivalent L50 power to lightning_t1_arc_initiate?) — bounded; gamora B14.5-style balance work covers
- Discipline #1 math-before-code applies to new pools (gandalf authors trait identities; gamora computes per-rank coefficients — same pattern as D8)

**Phase-1 P1 ship gate criteria:**
- Add: "all 7 substrates have authored + implemented intrinsic trait pools per canonical 32 § 4"
- Ship gate slips ~1 week (gamora critical path)

**D8 + D9 interaction:**
- D8 design doc gains 4 new sections (§ 2 fire / § 3 water / § 4 earth / § 5 wind) — restructure D8 from "three new pools" to "all seven pools, with three for Phase-1 P1 substrate expansion"
- D9 audit § (canonical-four affix coherence) gains cross-check against canonical-four intrinsic pools — already authored against forbidden_mechanics; this is verification not new design

### Under Option II

**Gamora queue:**
- Unchanged from current D8 contract scope (~6.5 days; 3 substrate pools)
- No reflow of downstream deliverables

**Jack-ryan watchpoints:**
- D9 informational soft-tension flags carry forward (canonical-four affix coherence is verifiable against new pools but not against canonical-four intrinsic pools — those don't exist)
- New Discipline #13 watchpoint: substrate-depth asymmetry as continuous observation (does player feedback in P1 → P2 window surface "new substrates feel deeper than old"?)
- Phase-1 P2 carries unfinished architecture commitment as known debt

**Phase-1 P1 ship gate criteria:**
- Unchanged
- P2 ship gate adds: "canonical-four intrinsic trait pool authoring + implementation"

**D8 + D9 interaction:**
- D8 already-committed; remains "three new pools" scope
- D9 already-committed; remains as-is
- P2 deliverable list grows by 1 new deliverable: "canonical-four intrinsic trait pool authoring + implementation" (~5 days total work)

### Under Option III (partial)

Hybrid of the above. Not recommending — listed for completeness. Adds ~2 days vs Option II; saves ~3 days vs Option I; ships half-asymmetric.

### Under Option V (gandalf-only authoring during P1)

**Gamora queue:** unchanged
**Jack-ryan watchpoints:** asymmetry still visible to player; design-debt closes mid-P1
**P1 ship gate:** unchanged
**P2 deliverable:** "gamora implementation of pre-authored canonical-four trait pools" (~1-2 days)

---

## § 8 — What you need from Matt

**Decide between:**

- **Option I** — Author + implement canonical-four trait pools in P1 (~1 week P1 slip; substrate-symmetric ship). [My recommendation]
- **Option II** — Defer canonical-four authoring to P2 (current scope; asymmetric ship). [Default per protocol]
- **Option III** — Partial canonical-four pool authoring in P1 (half-depth; ~2 days gandalf only). [Not recommended]
- **Option V** — gandalf authors all 4 pools in P1; gamora implementation deferred to P2 (~3-4 days gandalf only; player asymmetry persists; design-debt closes). [Reasonable fallback]
- **Something else** Matt sees that I haven't surfaced.

**Decision-by time request:** ideally within ~24 hours so gamora's D8 implementation contract can be finalized at correct scope. Gamora is currently shipping D8/D9 implementation against the 3-substrate scope (per the [2026-05-18 05:30Z] HANDOFF in the hive log) — if Option I lands within ~24h, gamora's in-flight work can be widened in-place rather than re-scoped after partial completion. If decision lands later, gamora ships at 3-substrate scope and any expansion becomes a separate D8-extension contract.

**One sentence to me back ("Option I" / "Option II" / "Option V" / "Stick with II and revisit at P1 retrospective" / etc.) is sufficient.** I'll handle authoring + knight-rider hive log AMENDMENT routing from there.

— gandalf
