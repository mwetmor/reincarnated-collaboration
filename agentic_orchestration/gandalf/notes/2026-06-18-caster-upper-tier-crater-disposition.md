# Caster upper-tier-crater — disposition: the crater is REAL + ROBUST (NOT the rogue's swarm-hot shape), the cheap disambiguation is a caster-pointed Lever-C, and the boss-bridge family is ONE evidence-backed problem (keystone-ceiling EXCLUDED)

**Type:** design-disposition note (gandalf → knight-rider). Reads the caster-hot construction run (STILL_INCONCLUSIVE) for the finding that is sitting in its data UNDISPOSITIONED, generalizes the rogue boss-efficacy arc to the caster side, and loads the buildable Run-A caster item.
**Date:** 2026-06-18
**Author:** gandalf (story-and-design steward)
**Authority:** continuation of the Matt-authorized 2026-06-15 (Pattern-B) degeneracy-resolution workstream + the 2026-06-18 "load both runs" authoring pass (Matt "yes please" to faction-shape + caster-crater + endorse-criteria). This note RESOLVES the caster-side generalization that the rogue diagnosis (§3) and the Lever-C verdict (§1 "what remains OPEN") both explicitly left open with a named re-open criterion. It locates + frames + recommends; the FIX decision and the apparatus call remain RESERVED FOR MATT.
**Parents (read order):**
- The rogue diagnosis that registered the caster prediction: `agentic_orchestration/gandalf/notes/2026-06-15-rogue-degeneracy-role-floor-diagnosis-for-kr.md` §3 (branch-4 prediction + branch-2 falsifier).
- The Lever-C verdict that ruled out architecture for the rogue: `agentic_orchestration/gandalf/notes/2026-06-15-lever-c-composition-verdict-disposition.md` (C-2: composition, not the instrument; b6 = SPEC).
- The DoT-as-boss-bridge verdict + Q4 control: `agentic_orchestration/gandalf/notes/2026-06-15-dot-as-boss-bridge-verdict-disposition.md` + `...2026-06-15-dot-verdict-Q4-foldin-and-power-tier-control.md` (the genre-correct boss-bridge mechanism; tick_scale keys on int/wis; matched-pt control).
- The keystone-ceiling park (the item I EXCLUDE from the family): `agentic_orchestration/gandalf/notes/2026-06-18-three-flip-run-close-band-hold-keystone-park.md` §2.
- The spirit-guide combat-bridge (the season-2 sibling of this family): `canonical/story/2026-06-18-companion-difficulty-inversion-and-spirit-guide-combat-bridge.md` §3.
**Evidence (read first-hand 2026-06-18, not taken on report):**
- Caster-hot result: `reincarnated-engine/output/g7-reshape-hot-caster-b6-20260615.json` — VERDICT `STILL_INCONCLUSIVE`; the per-rung ladder data extracted in §1 below.
- Construction note: `reincarnated-engine/src/reincarnated/simulation/math/b6-reshape-hot-caster-cell-construction-2026-06-15.md` (the anti-rig floor + stop rule).
- Gate-1: `agentic_orchestration/qa/findings/2026-06-15-gate1-gamora-b6-reshape-hot-caster-cell-construction.md`.
- Tier eligibility: `reincarnated-engine/src/reincarnated/simulation/gauntlet_sim.py:16-17, 125-138` (gating = `boss_with_adds` + `mini_boss`; bypassed = `swarm` / `magic_pack` / `elite_pack`).

---

## 0. One line

**The caster-hot run honestly returned STILL_INCONCLUSIVE on the narrow swarm-hot question — because the caster's swarm tier could NOT be driven over ceiling even at the anti-rig floor (the caster is genuinely NOT the rogue's shape) — but the data it produced contains a clean, robust, undispositioned finding: across all 4 rungs and all 4 caster cells, `mini_boss` and `boss` sit at EXACTLY 0.0 every single time, while the caster over-clears the BYPASSED `magic_pack` tier (~1.0). Casters crater the same shared boss tier as the rogue, reached by a DIFFERENT over-clear tier (pack-AoE, not single-target-swarm). This is one more member of the boss-bridge family — multiple archetypes lacking a concentrated single-hard-target finisher — and Lever C already ruled the balance INSTRUMENT out for that family on the rogue side. The buildable Run-A caster item is the cheap caster-pointed Lever-C (reuse the existing harness), NOT a speculative fix. The keystone-ceiling is EXCLUDED from this family (it is measurement-saturation, a different problem).**

---

## 1. What the caster-hot run actually showed — read it honestly, then read what is SITTING IN IT

gamora built the caster-hot run to test the rogue diagnosis's pre-registered question: *does a caster, with its role floor intact (casters compose through `archetype_composer.py`, which PRESERVES `required_roles`), exhibit the rogue's swarm-hot → modifier-suppress → boss-crater chain (branch-2 architectural) or not (branch-4 envelope-specific)?* The construction tried to MANUFACTURE a swarm-hot caster by driving swarm HP down a ladder (0.5 → 0.3 → 0.15) and then cutting swarm count (rung 4), bounded by an anti-rig floor with a stop rule.

**The verdict is honest and correct on its own terms: STILL_INCONCLUSIVE.** No rung drove any caster cell's swarm over the ceiling, so the floor-to-suppress trigger never arose, so branch-2-vs-branch-4 stayed untestable *within the anti-rig floor.* gamora reported per the stop rule and did NOT over-claim. That is good discipline and I honor it: the swarm-hot question is genuinely unanswerable for casters because **the precondition is false — casters do not over-clear swarm.** That is itself a clean, useful NEGATIVE: the rogue's degeneracy SHAPE (raw single-target throughput melting low-HP mobs one-by-one) does not exist on the caster side. Prediction-wise, the caster did NOT reproduce the rogue's branch-2 chain — consistent with the role-floor diagnosis, just not provable through the swarm door.

**But here is the finding the INCONCLUSIVE label leaves undispositioned — the per-tier win-rates across the full ladder:**

| rung (swarm HP × / count) | cell | modifier | swarm | magic | elite | **mini_boss** | **boss** |
|---|---|---|---|---|---|---|---|
| r1 (0.5 / 8) | fire_mage | 0.111 | 0.47 | 1.00 | 0.50 | **0.00** | **0.00** |
| r1 | water_mage | 0.111 | 0.46 | 1.00 | 0.50 | **0.00** | **0.00** |
| r1 | earth_caster | **0.366** | 0.52 | 1.00 | 0.52 | **0.00** | **0.00** |
| r1 | wind_caster | 0.095 | 0.44 | 1.00 | 0.50 | **0.00** | **0.00** |
| r2 (0.3 / 8) | all four | 0.06–0.24 | 0.45–0.51 | 0.97–1.00 | 0.50 | **0.00** | **0.00** |
| r3 (0.15 / 8) | all four | 0.03–0.13 | 0.46–0.74 | 0.60–1.00 | 0.50 | **0.00** | **0.00** |
| r4 (0.15 / 4) | all four | 0.018–0.076 | 0.53–0.67 | 0.50–1.00 | 0.50 | **0.00** | **0.00** |

**Three facts jump off this table, none of which the swarm-hot verdict captures:**

1. **`mini_boss` = 0.00 and `boss` = 0.00 — INVARIANT.** Sixteen cell×rung observations; thirty-two upper-tier win-rates; every one is zero. Not "low," not "fragile" — *zero kills.* No caster cell, at any difficulty rung, at any converged modifier from 0.018 to 0.366, lands a single mini_boss or boss kill. This is the most robust crater in any of this workstream's data.
2. **The over-clear tier is `magic_pack` (~1.0), not swarm.** The caster's "hot" tier — the one pinned at ceiling that drags the modifier down — is magic_pack, with elite and swarm sitting moderate (~0.5). The rogue's hot tier was swarm. *Same suppression mechanism, different tier.*
3. **`elite` = 0.50 — eerily constant.** Across every cell and rung, elite is exactly 0.50. The caster half-clears packs-with-an-elite and fully clears magic packs, but the moment the encounter is a SINGLE high-HP target (mini_boss / boss_with_adds), it goes to zero.

**The tier semantics make this unambiguous.** Per `gauntlet_sim.py:16-17 / 125-138`: the GATING (eligible) encounters are `boss_with_adds` (3) + `mini_boss` (1); `swarm` / `magic_pack` / `elite_pack` are BYPASSED (they ceiling-saturate, non-discriminating). magic_pack and elite_pack are GROUPED encounters; mini_boss and boss_with_adds are SINGLE high-HP targets. **The caster clears the grouped tiers and craters the single-target tiers** — and it craters on *exactly the encounters the production gate evaluates.* In the live gate, this caster fails. The thing it is good at (magic_pack) is the thing the gate ignores.

**Net: the caster-hot run is INCONCLUSIVE on the swarm-hot question and simultaneously DISPOSITIVE on a question nobody asked it — casters have a hard, robust upper-tier crater on the single-target gating tiers. That crater has been sitting in this JSON undispositioned since 2026-06-15. This note dispositions it.**

---

## 2. The caster crater is the SAME family as the rogue crater — reached by a different over-clear tier (the genre-faithful mapping)

The two craters are the same problem wearing two archetype costumes, and the difference between them is itself genre-correct design truth:

| | **glass single-target rogue** | **AoE caster** |
|---|---|---|
| over-clear tier (drags modifier down) | swarm (raw ST throughput, mobs one-by-one) | magic_pack (AoE shreds grouped mobs) |
| cratered tier (shared) | boss / mini_boss = 0.0 | boss / mini_boss = 0.0 |
| genre archetype | ST striker: shreds trash, no working boss finisher | pack-mage: shreds packs, no concentrated single-target finisher |
| genre precedent | D3 Demon Hunter pre-itemization (swarm-shredder, boss wall); PoE glass-cannon ST (deletes packs, dies to boss slam) | D2/D3 elemental sorc without a single-target spell (clears trash, stalls on Diablo/Baal); PoE AoE-only caster with no single-target finisher (maps fast, dies to pinnacle bosses) |

**This is the cleanest possible statement of the unified problem, and it is MORE genre-faithful than my prior shorthand ("single hard targets punish certain profiles").** The sharper truth: *each damage archetype over-clears a DIFFERENT trash/pack tier — and that over-clear pins the single global modifier DOWN, which craters the SHARED single-hard-target tier where neither archetype has brought a concentrated finisher.* The over-clear tier is archetype-specific; the cratered tier is universal. The single global modifier cannot simultaneously suppress an archetype's over-clear tier AND lift its boss tier — the exact one-degree-of-freedom limitation, surfacing identically on both sides via different doors.

**And Lever C already ruled the balance INSTRUMENT out for this family.** On the rogue side, Lever C pinned the modifier high (M=1.0, well above the 0.65 killable calibration) and the rogue STILL landed zero boss kills — proving the single global modifier was never the constraint; the constraint is kit-composition (boss EFFICACY). The structural mechanism is identical on the caster side. So the strong prior is: **the caster crater is ALSO a composition/efficacy gap (the caster has no boss-killer that lands), NOT a balance-architecture gap.** That prior is strong — but it has NOT yet had the caster's OWN clean test, and discipline forbids me asserting it without one (§3).

---

## 3. The honest locate — composition STRONGLY SUGGESTED, NOT YET Lever-C-proven for casters → the cheap caster-pointed Lever-C is the Run-A item

The caster crater in §1 is, by itself, CONFOUNDED in exactly the way the rogue's ORIGINAL crater was — and I will not repeat the Q4 mistake of attributing to composition a result that was run at a low/suppressed modifier:

- The caster's converged modifiers are LOW (0.018–0.366), dragged down by the magic_pack over-clear. A zero-boss-kill result at a low modifier could be composition (no boss finisher) OR could still be modifier-suppression (the magic over-clear forcing the knob down below boss-killable). The one near-healthy data point — earth_caster at modifier 0.366, still boss 0.0 — is *suggestive* of composition, but 0.366 is below the rogue's 0.65 killable calibration, so it is not "generous headroom." Not conclusive.

**The disambiguation is the same instrument that settled the rogue: a caster-pointed Lever-C.** Pin the caster's global modifier high — M=1.0 generous + the M=0.30 conservative discriminator jack-ryan pivoted Lever-C to (so generous headroom cannot brute-force a false "architecture" verdict) — hold the magic_pack tier at normal difficulty (do NOT rig it), and ask the single clean question: **does the caster kill mini_boss / boss when its modifier is NOT suppressed?**

- **Zero boss kills at M=1.0** → composition/efficacy, clean and proven, SAME verdict as the rogue (C-2). The caster lacks a boss finisher that lands. → the fix is a caster boss-bridge (§4), gated exactly as the rogue's was.
- **Meaningful boss kills at M=1.0** → it WAS modifier-suppression on the caster side — i.e. the magic_pack over-clear dragging the knob below boss-killable. That would be a genuinely DIFFERENT verdict from the rogue (architecture/loop, not composition) and would re-open the single-global-modifier question on the caster side — on evidence, not silence. (See §5: this branch couples to the bypassed-tier loop question.)

**Implementation economy worth naming up front:** this is not new harness. It is Lever-C's existing rig (`reincarnated-engine/output/lever-c-upper-tier-disambiguation-20260615.json` lineage; the M-pin + tier-isolation machinery) pointed at the four caster cells instead of the rogue cell. Near-zero marginal build cost, decisive output, non-destructive (a diagnostic; shifts no WR; concurrent-safe like Q1–Q4 and Lever C were). **This is the buildable Run-A caster item — the PROBE, not a fix.** The fix is gated on the probe, mirroring the rogue arc's recognition → validate → commit discipline exactly. I will NOT load Run A with a speculative caster boss-bridge fix ahead of its own evidence; that would be the precise discipline failure Q4 caught.

---

## 4. The boss-bridge family — ONE evidence-backed problem; and the keystone-ceiling EXCLUSION (correcting my prior over-reach)

In the prior session I floated a four-way unification ("single hard targets punish certain profiles") spanning swarm-crater, DoT-as-boss-bridge, keystone-ceiling, and spirit-guide-bridge. On the evidence now in hand, that synthesis was PARTLY right and partly over-reach. The disciplined restatement:

**IN the family (one problem — archetypes lacking a concentrated single-hard-target finisher; fix is a boss-bridging TOOL, not a balance-instrument change):**
1. **Rogue boss-crater** — composition deficiency, Lever-C-PROVEN. Fix-direction: a working burst / a DoT that lands. Matt call PARKED ((a) composer efficacy fix vs (b) accept-and-route-via-b6).
2. **Caster boss-crater** — composition STRONGLY SUGGESTED (this note); gated on the caster-Lever-C probe (§3).
3. **DoT-as-boss-bridge** — the genre-correct MECHANISM that IS the boss-bridge for both. PoE-bleed single-strongest-stack model; relocated to the sim's `_add_or_refresh` no-stack wall + the tick_scale lever. **A detail that binds this tightly to the caster side:** the DoT verdict found `tick_scale` keys on **int/wis** (which is why the DEX rogue's bleed never amplifies — a thematic bug for the rogue). For CASTERS, int/wis IS the offensive stat — so a caster's DoT (ignite/fire-DoT, cold) ALREADY scales with tick_scale; it is capped only by the no-stack architecture (5 DoT skills → 1 instance), not by the stat bug. **The caster's boss-bridge may be even closer to working than the rogue's** — the same sim no-stack fix could light it up, IF casters select DoT (a generation question to confirm, parallel to the rogue's 5/10-bleed-selection finding).
4. **Spirit-guide combat-bridge** — the SEASON-2 sibling: an ALLY boss-bridge, encounter-tier-gated to boss/elite, baton-passed at first-form ascension. Same gesture (a boss-bridging tool fills the single-hard-target gap), different layer (ally vs kit-intrinsic), different season. The companion-difficulty-inversion note already routes it to season-2.

**OUT of the family — the keystone-ceiling is a DIFFERENT problem (this is the over-reach I retract):**
- The keystone-ceiling is **measurement-saturation**: open_arena WR saturates at 1.000 with zero loss-variance, so the apparatus cannot RANK top-end builds (you cannot rank what does not vary; `spearman_degenerate=true`). Its re-engagement criterion is a *non-degenerate open_arena reference* (de-saturate the metric).
- That is the OPPOSITE END of the encounter space (open/trash tier, not boss tier), a DIFFERENT mechanism (the metric's discriminating power, not an archetype's throughput), and a DIFFERENT fix (de-saturate the reference, not add a finisher tool). It shares only a superficial "tier extremes" vibe. **Folding it into the boss-bridge family would muddy a clean, evidence-backed unification with an unrelated measurement question.** It stays its own parked ticket. I name the exclusion explicitly so a future reader does not re-ask "why isn't keystone here?" — the answer is: because it is not the same problem, and I checked.

**Net: the boss-bridge family is THREE archetype/season instances (rogue / caster / season-2-ally) of one problem (no concentrated boss finisher), served by one genre-correct mechanism class (DoT-that-accumulates / working-burst / boss-tier-gated-ally), with the balance INSTRUMENT ruled out as the lever (Lever C, rogue side) pending the caster confirmation. Keystone-ceiling is adjacent-not-same and stays excluded.**

---

## 5. The apparatus question this surfaces — FLAG, do not assert (a real gandalf-spotted-it-before-others item)

The caster data raises one genuinely new apparatus question I cannot answer from the JSON alone, and I flag it rather than assert it (survey discipline: what IS vs what I suspect):

**Does the balance LOOP optimize the global modifier against tiers the production GATE BYPASSES?** The caster's modifier (0.018–0.366) is being dragged DOWN, and the only over-ceiling tier is `magic_pack` — which is a BYPASSED, non-gating encounter. If the loop is chasing magic_pack's over-clear (a tier the gate ignores) and that chase craters the gating tiers (mini_boss/boss), then the apparatus is **fighting itself**: optimizing against a tier it has declared non-discriminating, at the cost of the tiers it actually gates on. That would be a real, fixable apparatus issue — and it would mean part of the caster crater is an artifact of the loop's objective, not the kit's composition (the §3 "meaningful kills at M=1.0" branch).

- **Why I flag rather than assert:** the modifiers differ ~3× across cells (earth 0.366 vs wind 0.095) while their tier WRs are near-identical, which suggests the modifier is set by something other than these WRs (a KPM throughput objective, perhaps) — i.e. I do NOT actually know the loop's objective function from this data, and guessing it would violate empirical-inspection-over-assumption. This is gamora's seam to answer.
- **Why it matters to the disposition:** the caster-Lever-C probe (§3) PARTIALLY answers it for free — pinning the modifier high removes the loop's objective from the equation entirely, so a zero-at-M=1.0 result is clean of this confound. But the standalone question ("does the loop optimize against bypassed tiers?") deserves its own look regardless, because if it does, it is a cross-archetype apparatus issue, not a caster issue.

**Routing:** gamora (loop objective), as a question, not a task — coupled to the §3 probe. If the probe returns zero-at-M=1.0, the caster crater is composition (§4 fix path) AND the loop question is a separate, lower-urgency apparatus cleanup. If the probe returns meaningful kills, the loop question becomes load-bearing.

---

## 6. Routing + Matt decision points + what Run A actually gets

**What Run A gets from this disposition (the buildable item):**
- **The caster-pointed Lever-C probe** (gamora seam; reuse the existing Lever-C harness; M=1.0 generous + M=0.30 discriminator; magic_pack at normal difficulty; the four caster cells; non-destructive diagnostic, concurrent-safe). Output: composition (zero-at-M=1.0, same as rogue) vs suppression (meaningful kills → re-opens the caster architecture/loop question on evidence). **This is the caster-crater item — a PROBE that earns its fix, not a speculative fix.**

**What this disposition does NOT do (held / parked / RESERVED):**
- It does NOT author a caster boss-bridge fix. That is GATED on the probe (recognition → validate → commit). If the probe confirms composition, the fix-direction is §4's mechanism class (caster DoT efficacy via the same `_add_or_refresh` sim change the rogue's bleed needs — with the bonus that caster int/wis already scales tick_scale — and/or a single-target finisher floor for AoE-geo caster cells, the caster analog of the rogue's reserved-burst-efficacy layer). Math-note → Gate-1 → G7 re-pass chain, same as the rogue.
- It does NOT touch the rogue Matt-call (parked: composer efficacy fix vs accept-and-route-via-b6). The caster finding INFORMS that call (it is the same family) but does not pre-empt it.

**Matt decision points (RESERVED — surfaced, not decided):**
1. **Authorize the caster-Lever-C probe into Run A?** (My recommend: yes — cheap, decisive, reuses existing harness, closes a genuinely open generalization on evidence.)
2. **The boss-bridge family — one coherent treatment or per-archetype?** The rogue (parked), caster (probe-gated), and season-2-ally (deferred) are one problem. Matt may wish to rule on whether the boss-bridge is treated as ONE design line (a "concentrated-finisher floor" doctrine across archetypes + the spirit-guide ally for season-2) or three separate tickets. (My lean: one doctrine, three instances — it is the same genre truth and the same mechanism class, and treating it once avoids three drifting partial fixes. But this is a Matt-scope call, not mine to make.)
3. **The apparatus question (§5)** — whether to have gamora characterize the loop's objective-vs-bypassed-tiers behavior as its own item. (Lower urgency; the probe de-risks it.)

**Routing:**
- **knight-rider:** the caster generalization is RESOLVED to "real + robust crater, same family as rogue, reached via magic_pack over-clear not swarm; clean disambiguation is a caster-pointed Lever-C." Load the probe into Run A as the caster-crater item. Do NOT sequence a caster fix ahead of the probe. Surface the three §6 Matt decision points.
- **gamora:** the caster-Lever-C probe is yours (reuse the Lever-C harness; the four caster cells; M=1.0 + M=0.30; magic_pack unrigged). And the §5 loop-objective question is yours to characterize (question, not task, coupled to the probe).
- **rocket:** parallel-confirmable generation question (cheap, like the rogue's role-count audit): **do caster cells SELECT DoT?** (ignite/fire-DoT, cold). If they do — as the rogue incidentally did (5/10) — then the §4 caster boss-bridge is largely a sim no-stack fix away (caster int/wis already scales tick_scale). If they do NOT, the caster boss-bridge needs a selection/floor change too. Read-only; concurrent-safe.
- **jack-ryan:** if the probe → fix path opens, the Gate-1 discipline is the same one that held the rogue arc: keep boss EFFICACY a SEPARATE layer from role PRESENCE (do not let an efficacy fix smuggle a conjunctive label back in), and hold the matched-power_tier control discipline (the Q4 lesson) so the caster fix is not attributed on a confounded premise.

---

## 7. Player consequence (the anchor)

A player who builds an elemental caster in this state experiences the single most demoralizing arc in the genre, and it is worse than the rogue's because it is the FANTASY tier of the class. The mage shreds every pack — magic_packs evaporate, the screen clears, the player feels powerful — and then walks into the boss room and *cannot kill the boss at all.* Not "dies on a knife's edge," not "needs to play the mechanics carefully" — chips it forever and times out, zero kills. This is the D2 elemental-sorc-with-no-single-target-spell wall (clears the whole game, stalls on Diablo); the D3-vanilla Inferno cliff; the PoE map-blaster who hits a pinnacle boss and discovers the build has no single-target. **The promise of a caster is "I am a master of devastating power" — and the boss fight, the moment that promise should pay off hardest, is exactly where it pays off least.** That is the performance of power without the substance of it — the hollow journey this seat exists to catch.

The genre-correct version is not "make the caster a single-target build" — it is to give the pack-mage a *concentrated finisher* (the ignite that ramps over a long boss fight; the single-target nuke; in season-2, the ally who helps hold the line) so the player who built for AoE devastation can ALSO, with intent, bring a boss down. One kit, AoE-strong AND boss-capable, no per-tier modifier — the same bridge argued for the rogue, owed equally to the mage.

---

**Signed:** gandalf, 2026-06-18.
**For:** dispositioning the caster upper-tier-crater that has sat undispositioned in the STILL_INCONCLUSIVE caster-hot run since 2026-06-15 — the run honestly could not drive swarm over ceiling (casters are NOT the rogue's shape; clean negative on the swarm-hot chain), but its ladder shows mini_boss + boss at an INVARIANT 0.0 across all 4 cells × 4 rungs while the caster over-clears the BYPASSED magic_pack tier, so casters crater the SAME shared single-hard-target gating tiers as the rogue, reached by a DIFFERENT over-clear tier (pack-AoE not single-target-swarm) — one more member of the boss-bridge family (archetypes lacking a concentrated finisher), for which Lever C already ruled the balance INSTRUMENT out on the rogue side; the crater at the caster's LOW converged modifier is confounded, so the buildable Run-A item is the cheap caster-pointed Lever-C (reuse the existing harness; M=1.0 generous + M=0.30 discriminator; magic_pack unrigged) that PROVES composition-vs-suppression and earns its fix — NOT a speculative fix; the keystone-ceiling is EXCLUDED from the family (measurement-saturation, a different problem, different tier, different mechanism, different fix — the prior four-way unification over-reached and is retracted to a three-instance boss-bridge family plus an excluded adjacent item); a real apparatus question is flagged (does the loop optimize against bypassed tiers?), routed to gamora as a question the probe partly answers for free; and the player consequence is named — a pack-mage that shreds everything and then cannot kill the boss at all is the hollow-journey failure this seat exists to catch, owed the same boss-bridge as the rogue.
