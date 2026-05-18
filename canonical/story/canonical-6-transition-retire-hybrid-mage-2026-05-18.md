# Canonical-6 Transition — RETIRE hybrid_mage (2026-05-18)

**Author:** gandalf (story-and-design steward).
**Authority:** Matt L3 verdict 2026-05-18 — RETIRE hybrid_mage from the canonical archetype roster after the D11.0 → D11.1 → D11.2 cycle of failures (6% → 0% → 0% interior convergence; D11.2 Phase B failed 0/17 due to gear-environment fidelity bug in the smoke gate).
**Type:** Pattern A design-canon transition doc — decision context, identity record, redistribution plan, alternative-resurrection notes, cross-canon cleanup list.
**Status:** Authored 2026-05-18; hands off to jack-ryan for cross-canon strip pass + decisions-log capture; to rocket for archetype-list removal + `is_retired` flag pass; to drax + loadout for consume-time filter.
**Predecessors:**
- D11 advisory `canonical/story/d11-hybrid-mage-tuning-advisory-2026-05-17.md`
- D11 post-mortem `canonical/story/d11-hybrid-mage-tuning-postmortem-2026-05-17.md`
- D11 Option-B verdict `canonical/story/d11-postmortem-option-b-verdict-2026-05-17.md`
- D11.2 structural-redesign advisory `canonical/story/d11-2-structural-redesign-advisory-2026-05-17.md` (the § identity-preservation argument is now retracted; the § RETIRE clause is activated)
- Rocket D11.2 Phase B failure record (dispatch `2026-05-17-rocket-d11-2-phase-b-full-salvage-scale-0-75.md` § completion)

---

## § 0 — TL;DR

The hybrid_mage archetype — the lone cross-substrate "integrator" mage in the canonical roster — is **RETIRED** from the canonical archetype list as of 2026-05-18. The roster transitions from 7-archetype (substrate-coherent six + hybrid_mage as the integrator) to **canonical-6** (substrate-coherent only).

The transition is a **design simplification under empirical pressure**, not a thematic verdict that hybrid identity is bad. The cycle of three structural attempts (D11.0 element-coverage tax; D11.1 skill-count ceiling primary; D11.2 kit-aggregate DPS-density scaling) each surfaced a different failure mode; the third attempt's smoke gate produced a 5/5 false positive due to a gear-catalog environment-fidelity bug, and the full Phase B salvage at scale_factor=0.75 returned 0/17 interior convergence. Matt's L3 verdict: rather than D12+ structural redesign of the archetype kit composition (uncertain multi-day payoff), retire it from canonical-7 so the engine ships a converging roster and Matt's stated milestone — "develop a completely new LLM generated season once we feel those issues are resolved and converge many classes from it" — unblocks immediately.

Identity-DNA from hybrid_mage redistributes (§ 5) across the canonical-6 surface: multi-element flex builds become a **Spirit Guide / form-library** experience rather than a per-class generative archetype; "wide and modest" tactical positioning lives on through controllers and casters with secondary-element bias; layered identity reframes as a **player-built composition** at the loadout layer rather than a generator-produced kit shape.

Alternative-resurrection paths (§ 6) are noted but not committed: experimental-tier archetype with separate balance treatment; Spirit-Guide bonus form; Earth-Self meta-layer perk; Phase-2 alchemy/poison/acid substrate expansion where the integrator role may sit more naturally on a substrate landscape that's been designed *for* hybrid composition rather than retrofitted *with* it.

The cross-canon cleanup list (§ 8) hands to jack-ryan for a strip pass across canonical-09, -17, -28, -30, -32, -33, -16a, three story docs, the engineering generation code, and the consume-time surfaces (loadout + demo). Nothing in code or doc should imply hybrid_mage is part of the live canonical roster after this transition; everything that *was* part of the roster (the 17 staged instances) remains historical record with an `is_retired: true` flag.

---

## § 1 — Decision context

### § 1.1 — The D11 cycle in three frames

The decision to retire is the empirical conclusion of a three-attempt structural sprint. Each attempt produced a more informed picture of the failure mechanism than the last; none produced a converging archetype.

**D11.0 — element-coverage damage tax (α=0.07).** Anchored against D2 split-Sorceress design-feel (40-50% effective DPS penalty on split-element kits; back-scaled to 7% for Reincarnated's intended-playable framing). Result: 1/17 interior convergence (6%). The lever moved WR-at-floor by ~3-7% across instances — the magnitude was honest about the projection but the projection itself missed the engine's empirical surface by ~10×. Genre-feel anchor; not measured against engine's WR-elasticity function.

**D11.1 — skill-count ceiling primary (ceiling=10; α=0.08 secondary).** Anchored against a "breadth-via-coverage-redundancy" hypothesis: too many element-tagged slots → combinatorial coverage of monster resistance profiles → floor-pin. Result: 0/17 interior convergence (0%). Rocket's surgical finding: the pruned skills under the ceiling protection rule were utility / sustain / DoT non-damage roles with `dps_score=0.0`; pruning them produced no DPS-density change and therefore no WR-elasticity response. The coverage-redundancy hypothesis was refuted: two n=2 (untaxed; only-2-elements) hybrid_mage instances also floor-pinned, which a coverage mechanism cannot explain.

**D11.2 — kit-aggregate DPS-density uniform scaling (Lever B; scale_factor=0.75 at Phase B).** Anchored against the *measured* WR-elasticity from D11.0 → D11.1 data (~0.5-1.0% WR per 1% DPS reduction at floor modifier). Math note projected 4/5 smoke pass at scale_factor=0.65. Discipline #17 smoke gate (3 sweep points × 5 representative instances) returned **5/5 PASS at scale_factor=0.75** — the *lowest* magnitude in the anchor band — which authorized full Phase B salvage. Phase B returned **0/17 interior convergence**.

The Phase A / Phase B mismatch is the load-bearing finding: **the smoke environment did not include the gear_catalog Monte Carlo sampling that the production balance loop uses.** Without gear, hybrid_mage instances at scale_factor=0.75 dropped their WR from ~0.70 baseline to ~0.45-0.50 — interior convergence. With gear (the production environment), the same instances retained ~0.60-0.85 WR — floor-pinned. Gear buffs hybrid_mage's effective fight performance enough that a 25% kit-DPS reduction is insufficient; deeper reductions would be required, but at scale_factor < 0.5 the archetype's identity becomes shell-of-self (every damage-bearing skill hits for less than half of its single-element counterpart).

### § 1.2 — Matt's L3 verdict

Matt's verdict at 2026-05-18 early morning: **RETIRE hybrid_mage from canonical-7.** The verdict's framing — verbatim from the dispatch chain — is *cleanest path to the new-season milestone*, not *the archetype is bad*. Three considerations are visible in Matt's pattern of decisions across this cycle:

1. **Convergence-first ship discipline.** The engine has 23 other archetypes (composed from 7 substrates × 3 roles + 5 physical), all of which converge or are convergeable with substrate-coherent generation. Holding the entire seven-archetype substrate-coherent roster on the *one* archetype that refuses to converge after three structural attempts is a poor ROI on critical-path time.
2. **Identity preservation has a floor.** At scale_factor < 0.5, the chromatic_mage / LE-Runemaster framing (every skill modestly powered by design) becomes "every skill hits for half of its single-element peer" — which is no longer "wide and modest." It's "wide and weak." The thematic story breaks before the math does.
3. **The integrator role belongs at the meta-layer.** The form library, the Earth-Self gallery, and the seasonal accumulation of forms are *already* the mechanism by which a player "integrates many substrates" across a lifetime of play. A per-class hybrid_mage is a generative-layer commitment to the integrator identity; retiring it does not retire the identity — it relocates the identity to the layer where Reincarnated's design naturally hosts it (§ 5.1, § 6.1).

### § 1.3 — Framing: simplification, not failure

This transition is **not** a verdict that hybrid identity is a bad design idea, that the D11 advisory's genre survey was wrong, or that the form-library framing of hybrid composition was misdirected. It is a verdict that the *current generative substrate* — the b6_archetype_templates / kit composition pipeline — does not produce hybrid_mage kits that the balance loop can converge against the current gear-included environment, after three good-faith structural attempts.

What the D11 cycle *did* produce that lands clean of the retire verdict:

- **Discipline #17** — empirical-calibration smoke gate before full-regen / full-salvage with a new lever. The D11.0/D11.1/D11.2 cycle is the canonical case study for the discipline. (Jack-ryan canonicalizes per ADR-002; the smoke-environment-fidelity amendment lands in the same pass.)
- **Empirical-elasticity anchoring** — the durable methodological learning that lever-magnitude must be measured against the engine's WR-at-floor function, not assigned by genre analogy. Future advisories work *from* the engine's empirical surface, not *toward* it.
- **WR-elasticity-to-damage measurement** — the ~0.5-1.0% WR per 1% DPS reduction anchor remains useful for future balance-lever work targeting any archetype.
- **The form-library / Earth-Self / integrator framing** — the work in the D11 advisory § 5 (substrate-commitment-cost; canonical-7 framing; chromatic vocabulary) is *not* retracted as design vocabulary; it is reframed as a *meta-layer* mechanism rather than a *generative-layer* mechanism (§ 5.1).

The chromatic_mage that walks lightly across many substrates is still a recognizable form in the project's cosmology — it just isn't a class the generator produces. It's a *journey* a player takes by accumulating forms across seasons.

---

## § 2 — What was hybrid_mage

### § 2.1 — The generative shape

In the engine's b6_archetype_templates pipeline, `hybrid_mage` was a single preserved archetype template — not composed from SubstrateIdentity × Role like the substrate-coherent archetypes, but explicitly defined with `special_constraints = ["hybrid_element_distribution", "require_3_ailment_types", "require_5_distinct_geometries"]`. Element-coverage ceiling was 3 (post-D11.0; was 4 pre-D11). Energy type: `mana`. Stat profile: INT/WIS-balanced caster (the fallback profile for unrecognized archetypes, by coincidence — Coupling #3 in the archaeology audit). Skill count typical: 9-12 (highest in the roster). Kit composition: 4-8 damage-bearing skills + 4-7 non-damage skills (utility / sustain / mobility / defensive), across 2-3 distinct elements.

It was the *only* archetype in the canonical roster whose generative identity *required* breadth across substrates. Every other archetype is substrate-coherent (fire_mage commits to fire; water_controller commits to water; rogue commits to physical). Hybrid_mage was the integrator slot.

### § 2.2 — The thematic identity

D11 advisory § 5 (substrate-commitment-cost) framed hybrid_mage as the form that holds *many* substrate commitments simultaneously. In the canonical-7 substrate vocabulary, each substrate has a *commitment* — fire's commitment is the willingness to burn the world to remake it; water's is the willingness to dissolve and reform; earth's is the willingness to hold what's given; wind's is the willingness to refuse to settle. A hybrid_mage was the form that participated in multiple commitments without fully expressing any single one. Genre-lineage citations: PoE Elementalist (Ascendancy "Heart of Destruction" / "Pendulum of Destruction" — high investment in multi-element identity; mid-band leaderboard tier); LE Runemaster (multi-element by design via Runic Invocations; per-element power deliberately modest; thematically beloved); D4 Sorcerer mid-band hybrid builds (Lightning Spear / Chain Lightning splash builds; popular mid-band variety).

The identity-statement that the D11.2 advisory landed at was "wide and modest, not narrow and sharp" — the LE Runemaster lineage cleanest. A chromatic_mage with full elemental coverage but modest per-skill magnitude. Substrate-commitment-cost expressed as kit-uniform magnitude restraint rather than a per-element tax surcharge. The narrative voice: a spirit who walked many substrates lightly rather than one who drank one substrate to its depth.

### § 2.3 — What it was trying to express

Three intertwined design intents were riding on hybrid_mage:

1. **Genre-canonical multi-element-mage identity.** ARPGs have a recognizable archetype for the player who refuses to commit to a single element. PoE Elementalist, LE Runemaster, D4 Sorcerer-splash builds, D2 multi-element Sorceress, GD-Spellbinder. The genre vocabulary expects this slot to exist. Without it, the substrate-coherent roster reads as "every mage is locked into one element" — a tonal narrowness that contradicts the genre's mid-band variety.
2. **Reincarnated's accumulation-cost story.** The form library, the seasonal journey, the Earth-Self who accumulates forms across many lives — this story has an *integrator* in its DNA. The being who can wield many substrates *because* it has lived many lives is the through-line of the entire game. Hybrid_mage was the in-season expression of that meta-layer identity.
3. **Mechanical breadth-cost design exploration.** "How does the engine express the cost of breadth?" was a load-bearing design question. The D11 cycle's three lever attempts (element-coverage tax; skill-count ceiling; kit-aggregate DPS-density scaling) were all attempts to answer it. Each attempt produced a clean *empirical* answer: under the current generative substrate, breadth-cost in damage magnitude cannot bring a multi-element kit into convergence against the current gear-included environment without dropping per-skill magnitude below the identity floor.

The retire verdict is a verdict on (3) — the *mechanical-substrate* expression. Intents (1) and (2) remain live design commitments; they are redirected to layers where they can be expressed without forcing the balance loop to converge against an incoherent kit shape (§ 5, § 6).

### § 2.4 — Empirical reality of the 17 staged instances

The 17 hybrid_mage instances in seasons 002011-015 (the standard-demo-regen-2026-05-17 cohort) span the empirical envelope D11 measured:
- WR-at-floor distribution: 0.567 to 0.867 (mean ~0.71)
- Skill counts: 9-12 (most at 10)
- Element counts: 2-3 (15 at n=3; 2 at n=2)
- Damage-bearing-skill counts: 4-8
- Convergence rate across D11.0 / D11.1 / D11.2: 1/17 / 0/17 / 0/17

These instances become **historical record** with `is_retired: true` provenance flags (rocket dispatch). They are not generated in future seasons. Demo + loadout filter them at consume time so playtest doesn't surface them. They remain in the file system for telemetry / decisions-log / historical reference purposes.

---

## § 3 — Why it didn't survive contact with the balance loop

The D11 cycle produced three layered findings that together explain the retire. Each is empirically grounded; none is hypothesis or analogy.

### § 3.1 — Multi-element kits compound the DPS-density problem

Substrate-coherent archetypes (fire_mage, water_controller, etc.) generate kits with strong DPS density concentrated in the primary substrate. The kit's element-resistance exposure is narrow (one or two elements), but its damage output against unresisted monsters is high. The balance loop converges these archetypes by adjusting the modifier downward — the kit *can* hit hard; the modifier dials it back to a fair gauntlet experience.

Multi-element kits (hybrid_mage) distribute DPS across multiple substrates. Each substrate's per-skill damage is modest. The kit's element-resistance exposure is broad (3 elements means at least one of the three is over-resisted by any given monster), but the *aggregate* DPS — summed across all damage-bearing skills — is high because there are 4-8 damage-bearing skills instead of the 3-5 a substrate-coherent kit typically carries. The balance loop sees high aggregate DPS against the gauntlet; it pins the modifier at the 0.05 floor; the floor is too low to make the kit balanced because **the kit's WR-at-floor is still 0.6-0.85** — it wins more than half its fights even at 5% damage scaling.

This is the structural shape of the problem: the *count* of damage-bearing skills compounds with the *gear* monte-carlo affix sampling to produce an aggregate fight-performance that the balance loop's modifier cannot bring under the 0.50 WR target without going below the modifier floor.

### § 3.2 — Gear Monte Carlo over-buffs hybrid kits

The D11.2 Phase A / Phase B mismatch surfaced the load-bearing detail: **gear sampling buffs hybrid_mage more than it buffs substrate-coherent archetypes.** A substrate-coherent fire_mage rolls fire-affinity affixes (burn-on-hit, fire-damage-percentage, fire-resistance-penetration); the affix pool has known density and the kit's expected gear bonus is well-characterized. A hybrid_mage with 3 elements rolls affixes across *all three* element pools; the kit has more eligible affix surfaces and more chances to hit high-value rolls. Empirically, the same hybrid_mage instance shows WR ~0.45 in a gear-stripped smoke environment and WR ~0.70+ in the gear-included production environment.

The structural implication: hybrid_mage's gear-included fight performance is sensitive to the affix-pool composition in a way that substrate-coherent archetypes aren't. Any balance lever targeting damage_multiplier at kit finalization is fighting against the gear affixes that compound *on top* of the scaled magnitude. Lever B at scale_factor=0.55 (the upper bound of the original D11.2 anchor band) would reduce kit damage by 45% but leave the gear affixes untouched — the kit still buffs via gear into a fight-performance that floor-pins.

The clean lever would target gear-included performance directly (e.g., a gear-affix density cap specific to hybrid kits, or a damage_taken_multiplier penalty that compounds against the gear-buffed damage output). This is a substantially more complex lever surface — D12+ multi-day work — and Matt's verdict is that the payoff doesn't justify the cost relative to retiring the archetype.

### § 3.3 — No clean lever

The D11 advisory's lever taxonomy enumerated five lever shapes (A: prune damage skills; B: kit-aggregate DPS-density scaling; C: gen-time damage-skill quota; D: orthogonal HP/CD penalty; E: engine-sim coverage rework). Each one carries either an identity cost (A: drops damage-bearing skills = drops elementalist identity), a coverage gap (C: salvage path = A; doesn't help existing instances), a wrong-mechanism failure (E: coverage-redundancy hypothesis refuted), or a magnitude problem against the gear environment (B, D).

D11.2 picked B + (optional) D as the cleanest available combination. The empirical result — 0/17 at scale_factor=0.75 in the gear-included environment — establishes that B (and likely B+D) at *any* magnitude that preserves identity (scale_factor ≥ 0.5) cannot bring the archetype into convergence against the production environment.

The remaining options after D11.2 Phase B were:
- **Option 1** (deeper Lever B sweep at scale_factor ∈ {0.55, 0.45, 0.35}): identity-destructive below 0.5; uncertain convergence even at 0.35
- **Option 2** (composite B+D at 0.65 + 5% HP in gear environment): incremental; not addressing the gear-buffing root cause
- **Option 3** (RETIRE): Matt's choice
- **Option 4** (D12+ structural redesign of kit composition pipeline): multi-day cycle with uncertain payoff against the same gear-buffing root cause

Option 3 was selected because it produces a converging roster *immediately* and unblocks the new-season milestone. Options 1 and 2 had ~10-30% chance of producing convergence with material identity damage; Option 4 had ~30-50% chance of producing convergence over 3-5 days with substantial engineering surface. Retire is the highest-EV move in critical-path terms.

---

## § 4 — Canonical-6 archetype list

The roster after retire. Each archetype is substrate-coherent (committed to a single primary substrate); roles are composed from SubstrateIdentity × Role at boot per the D3 composition pipeline. Identity reaffirmations are brief; the full identity-statement work for each archetype lives in canonical-32 (progression) + canonical-30 (engine-explainer) + the substrate-identity-declarations + role-orientation taxonomy work; this list is the *canonical-6 surface* reaffirmed in retire context.

The "6" here refers to the **substrate-coherent mage/caster/controller archetypes from the 7 canonical substrates** — the categories that hybrid_mage was previously the 7th member of. Physical archetypes (warrior/grappler/skirmisher/rogue/hunter) are not part of the "canonical-7 vs canonical-6" framing; they remain unchanged. The terminology in this transition specifically addresses the substrate-mage roster.

**Note on naming:** the substrate roster is 7 substrates wide (fire, water, earth, wind, lightning, holy, shadow); the per-substrate composed archetypes therefore yield more than 6 substrate-coherent archetype tags (mage/caster/controller × 7 substrates, with alias collapse for fire/water burst=area, gives ~18 substrate-coherent tags per the b6_archetype_templates docstring). The "canonical-6" terminology in this transition refers specifically to the **substrate-coherent integrator-role roster** — the previous canonical-7 enumerated 6 substrate-coherent integrator slots + 1 hybrid_mage integrator slot; canonical-6 is the 6 substrate-coherent integrator slots without the hybrid integrator. Jack-ryan: verify this terminology is consistent in your decisions-log capture; if the rocket / engine-side canonical-7 enumeration counted differently, the decisions-log should pin the canonical wording before the strip pass propagates.

### § 4.1 — The canonical-6 substrate-coherent integrator slots

(With identity reaffirmation in canonical-7 substrate vocabulary; per-substrate generative composition produces the actual archetype-tag set the engine ships.)

1. **Fire integrator** — the form that commits to fire's willingness to burn-the-world-to-remake-it. Aggressive direct-damage tilt; burn-DoT signature; high mid-fight damage; survivability through pace, not tankiness. Engine-tag examples: `fire_mage`, `fire_controller`.
2. **Water integrator** — the form that commits to water's willingness to dissolve-and-reform. Defensive-pivoting cast cadence; freeze / soak / cold-burn signature; resilient mid-fight; flow-based positioning. Engine-tag examples: `water_mage`, `water_controller`.
3. **Earth integrator** — the form that commits to earth's willingness to hold-what's-given. Sustained tankiness; thorny / petrification signatures; ground-anchored positioning; slow-but-inevitable damage application. Engine-tag examples: `earth_caster`, `earth_controller`.
4. **Wind integrator** — the form that commits to wind's willingness to refuse-to-settle. Mobile / kiting kit; cut / displacement signatures; chains of small displacements; sustain through unhittability. Engine-tag examples: `wind_caster`, `wind_controller`.
5. **Lightning integrator** — the form that commits to lightning's willingness to *strike-without-preamble*. Burst-focused damage; chain / fork geometry signatures; high variance per fight; rewards positioning precision. Engine-tag examples: `lightning_mage`, `lightning_controller`.
6. **Holy / Shadow integrator pair** — the paired-luminance forms (canonical-7 declared paired-amplification, not forbidden). Holy: radiant / consecrate signatures; party-supportive in multi-actor contexts; mid-fight stabilization. Shadow: penumbral / withering signatures; debuff-stacking; opportunistic damage. The pair is composable (Solo Leveling "duality-of-light-and-shadow" lineage); shadow-mage may run with holy-secondary signature and vice versa. Engine-tag examples: `holy_caster`, `holy_controller`, `shadow_mage`, `shadow_controller`.

Note: lightning is canonical-7 declared *unpaired* — it composes freely with any of fire/water/earth/wind/holy/shadow at the substrate-identity layer. This makes lightning the substrate that *can* carry secondary-element signatures naturally without identity friction (§ 5.2). Lightning is the closest canonical-6 surface to the integrator-role identity that hybrid_mage carried.

### § 4.2 — Physical archetypes (unchanged)

The physical roster (warrior, grappler, skirmisher, hunter, rogue) is unaffected by canonical-6. These archetypes were never part of the canonical-7 substrate-coherent integrator enumeration; they have their own identity surface (physical kit + at most 1 secondary element on area skills per `d10_kit_constraints.py` element ceiling). The retire affects only the substrate-mage roster.

### § 4.3 — Experimental tier (open)

The b6_archetype_templates includes an `experimental` slot for novel archetype experimentation. Hybrid_mage *resurrection* into the experimental tier is a noted alternative path (§ 6.1) but is not committed by this transition.

---

## § 5 — Where the lost identity-DNA lives now

Hybrid_mage carried three distinct identity threads: (a) multi-element flex builds; (b) "wide and modest" tactical positioning; (c) layered identity (multiple substrate signatures expressed simultaneously). The retire doesn't kill these threads — it relocates each to a layer that hosts it more naturally.

### § 5.1 — Multi-element flex builds → Spirit Guide / form library / loadout layer

The cleanest home for the "I want my mage to draw from multiple elements" player desire is *not* a per-class generated archetype; it is the **form library + Spirit Guide + loadout composition** layer. Reincarnated already has the meta-layer architecture for this:

- **Form library** (Earth-Self meta-layer): the player accumulates forms across seasons. A player who has finished a fire season, a water season, and an earth season *has* a fire form, a water form, and an earth form in their library. The integrator-identity expresses as the *player's choice* to maintain multiple forms in active rotation rather than committing to a single deep form.
- **Spirit Guide** (canonical-17): the spirit-guide character is the mechanism for body-swap + form-swap. A player can swap between accumulated forms within a season's frame; this *is* the integrator experience at the moment-to-moment gameplay layer.
- **Loadout layer**: at the per-class equip surface, gear affixes and trait choices already allow a single-substrate class to carry secondary-element flavor (a fire_mage with a water-resistance-penetration affix is mechanically expressing a water-secondary signature). The trait architecture (project_trait_architecture; per-class intrinsic trait pool + gear-affix rolls) supports secondary-element expression at the equipment layer.

**Player consequence:** the player who wanted to "play a mage that uses many elements" still has that experience — but it lives at the *journey* layer (accumulate forms across seasons; swap them via spirit guide) rather than at the *in-season generated class* layer (the engine produces a hybrid_mage class). The shift is from "one class with broad elemental coverage" to "many classes; broad elemental coverage across the player's lifetime." This aligns with the project's core thematic commitment: Reincarnated is a game *about* accumulating forms across a long arc. The integrator identity is the through-line of the entire game; it should not be compressed into a single archetype.

### § 5.2 — "Wide and modest" tactical positioning → lightning archetypes + secondary-element bias on controllers

The "wide and modest, not narrow and sharp" identity reads cleanest on two surfaces in canonical-6:

- **Lightning archetypes (lightning_mage, lightning_controller).** Per canonical-7 substrate-identity, lightning is declared *unpaired* — it composes freely with all other substrates. This makes lightning the natural carrier of the "secondary-element flavor without commitment violation" identity. A lightning_mage with secondary-fire kit signature (lightning chain → fire DoT) is recognizable, balance-loop-coherent (substrate-coherent kit shape; just with element-flexibility at the secondary tier), and thematically the closest surviving expression of "wide and modest." This is the lever the project should reach for first when a player asks "what's the most multi-element-feeling class?"
- **Controllers across all substrates.** Controller-archetype kits have higher non-damage-skill proportion than mage / caster archetypes; their identity is utility + crowd-control + survivability with damage as a supporting cast. A controller kit naturally reads as "wider and modester" than a focused mage kit. Players who want the modest-magnitude-by-design feeling can gravitate toward controllers without the substrate-coherence violation that hybrid_mage required.

**Player consequence:** the LE-Runemaster-style "all my skills are modest by design" feeling is preserved through controller archetypes generally and lightning archetypes specifically. The class is recognizable as elementalist (controller signatures are elementalist-coded); the magnitude restraint is structural (controller kits don't peak as hard as mage / caster kits); secondary-element flexibility is available where it doesn't break substrate-identity (lightning's unpaired status).

### § 5.3 — Layered identity → player-built composition at the loadout layer

The third thread — *layered* identity, where multiple substrate signatures express *simultaneously* in a single kit — has its home at the player-composition layer rather than the generator-output layer. The mechanisms:

- **Gear affixes with cross-element flavor.** An earth_controller equipping a wind-secondary weapon expresses a "earth/wind layered" identity through gear composition. The base class is substrate-coherent; the layered feeling comes from player equip choices.
- **Trait choices (per project_trait_architecture).** Per-class intrinsic trait pools + gear-affix rolls let players express identity layering at the build layer without forcing the generator to produce multi-substrate kits.
- **Spirit Guide swaps (in-season).** Within a season, a player can swap between forms (different substrate-coherent classes from the form library). A run that alternates between a fire form and a water form *is* the layered identity expression at the encounter scale.

**Player consequence:** the player builds the layered identity. The engine ships substrate-coherent classes that the balance loop can converge; the player composes layered identity from those classes plus gear plus traits plus spirit-guide swaps. This is the genre-standard ARPG composition pattern (PoE's identity comes from passive-tree composition; D2's comes from skill-allocation + gear; LE's comes from mastery + skill-tree). Reincarnated's composition surface is the loadout-layer + meta-layer; we let it carry the work.

### § 5.4 — Redistribution actions for the engine (none required immediately)

No engine-side trait-pool or element-coverage changes are *required* to absorb hybrid_mage's identity DNA — the existing canonical-6 surface (lightning archetypes; controllers; gear / trait composition; form library; spirit guide) already supports the redistribution. Two *optional* design considerations are flagged for post-canonical-6 review (not blocking; not committed):

1. **Lightning archetype secondary-element-bias review.** If post-canonical-6 playtest data shows players are reaching for hybrid_mage's identity space and not finding it satisfied through lightning archetypes, consider deliberately biasing lightning's kit composition pipeline to favor secondary-element skill inclusion at higher rates than other substrates. Tunable knob; small generative-pipeline cost.
2. **Spirit Guide / form-library narrative emphasis on integrator-form journey.** The form-library narrative voice (per canonical-17 spirit-guide framing + Earth-Self meta-layer) could explicitly call out the "integrator who walks many forms" archetype as a player journey-identity. This is doc work, not engine work; lives wherever the form-library narrative copy lives (player-facing strings; loadout-app copy; spirit-guide dialogue when that ships).

Both are post-canonical-6 polish items; neither blocks the transition.

---

## § 6 — Alternative resurrection paths (noted, not committed)

The retire verdict closes hybrid_mage's seat at the canonical-6 table. It does *not* close the design question of whether the integrator archetype could return in some form. Three plausible resurrection paths are noted here as flagged candidates for future design consideration, *without* commitment to any of them. The discipline is: if a future design pass wants to bring hybrid identity back, it picks one of these paths and re-litigates from the design surface, not from "let's retry hybrid_mage with a different lever."

### § 6.1 — Experimental-tier archetype with separate balance treatment

The b6_archetype_templates includes an `experimental` archetype slot. A future design could place a `chromatic_mage` (or whatever name) in the experimental tier with explicit acceptance that:
- It does *not* need to pass the standard balance-loop convergence gate
- It receives separate handcrafted kit composition (not generative)
- Players access it through an unlock / quest / Earth-Self meta-progression
- It is *intentionally* a flavor archetype, not a balanced one

This is the cleanest resurrection path. The "experimental" framing is a design-vocabulary commitment that hybrid identity costs structural support; the player who picks it accepts the trade. PoE has historical precedent (the Chieftain-Tukohama, the early Hierophant before MoM rework, the long-deprecated Walking Stick of Faltering Steps — all flagged-as-flavor archetypes that the player community embraces *because* they're flavor). Reincarnated could host hybrid identity in this way without forcing the convergent-roster invariant.

**Cost:** small generative-pipeline work to wire experimental-tier composition; identity-document work to make the experimental framing legible to players. Maybe 1-2 days of engineering + design work in a focused sprint.

### § 6.2 — Spirit-Guide bonus form / Earth-Self meta-layer perk

A more conservative resurrection: hybrid identity lives at the *meta-layer* as a Spirit-Guide-granted bonus or Earth-Self-progression-unlocked perk. The mechanism:
- A player who has accumulated forms from 3+ substrates in their library unlocks a Spirit-Guide ability "weave the forms" — within a single season, the player can temporarily *blend* a current substrate-coherent class with secondary-element kit pieces from forms in the library
- The blend is time-limited / encounter-limited / cooldown-gated
- The blend doesn't go through the balance-loop convergence pipeline — it's a temporary boon, not a standing class

This expresses hybrid identity as a *journey-earned ability* rather than a *standing archetype*. Thematically the cleanest fit (the form-library is *already* an integrator mechanism; the spirit-guide weave is just the expression). Mechanically it sidesteps the convergence problem because it's a temporary state, not a balanced kit.

**Cost:** medium — requires Spirit-Guide engine work, meta-layer progression hooks, UI surface for the weave ability. Possibly Phase 2 territory (after Phase 0 ships).

### § 6.3 — Phase-2 substrate expansion (alchemy / poison / acid era)

The longest-horizon resurrection: Phase 2's substrate expansion (alchemy / poison / acid era per MEMORY) introduces a substrate landscape that has been *designed for* hybrid composition from the start. In that landscape:
- The substrates are explicitly composable (poison + acid = corrosion; alchemy + fire = combustion)
- The generative pipeline composes hybrid kits *natively* rather than retrofitting them onto a substrate-coherent base
- The balance-loop accepts hybrid kits as first-class citizens, not exception cases

A Phase-2-native hybrid integrator archetype might converge cleanly because the substrate landscape carries the hybrid commitment in its DNA. The retrofit problem we hit in D11 doesn't exist if the substrates were designed to compose from the start.

**Cost:** large — Phase-2 substrate work is multi-month. But it's a *natural* part of Phase-2 scope; the resurrection of hybrid identity is a *consequence* of substrate-expansion design, not an additional cost.

### § 6.4 — Pattern across the three paths

The three paths share one shape: **hybrid identity returns when the design surface that hosts it is honest about the structural cost.** Experimental-tier acknowledges the cost via the flavor-not-balanced framing. Spirit-Guide bonus acknowledges the cost via the temporary-not-standing framing. Phase-2 expansion acknowledges the cost via the designed-for-hybrid framing. The retire-from-canonical-6 verdict is honest about the cost in *retroactive* framing: this archetype could not converge under the substrate-coherent-with-retrofit-hybrid pipeline.

None of these paths is committed. They are flagged so a future design pass that wants to bring hybrid identity back doesn't have to rediscover the structural problem; it can pick a path and proceed from a clean design surface.

---

## § 7 — What's lost

Honest accounting. The retire has costs; this section names them so they're visible at the decisions-log layer and don't ambush future design work.

### § 7.1 — Thematic variety in-season

A player who plays through a single season — say season_002016 (the first canonical-6 season) — encounters a roster of substrate-coherent archetypes. Every mage / caster / controller class commits to a single primary substrate. The in-season variety is narrower than it would have been with hybrid_mage in the roster. The genre's "multi-element-flex mage" slot is empty *within* the season.

**Mitigation:** the form library / spirit-guide / meta-layer redistribution (§ 5.1) re-introduces variety across seasons rather than within one. A player at season 4 has 4 substrates in their form library; that's the integrator experience. But for the first-season player, the variety floor is genuinely lower.

**Player consequence:** first-season players have fewer build paths than they would have under canonical-7 with a converging hybrid_mage. The genre-expected "I want to splash elements" build is reachable only through gear-affix flavor (a fire_mage with water-affinity gear), not through class selection.

### § 7.2 — Specific player-fantasy paths

Three player-fantasy paths are not directly served by canonical-6:
- **The "wild mage" / "chaos elementalist" fantasy** (every spell a different element). Was hybrid_mage's signature; not directly served.
- **The "polymath wizard" fantasy** (mastery of all schools). Was hybrid_mage's signature; not directly served.
- **The "trickster who refuses commitment" fantasy** (no school owns me). Was hybrid_mage's signature in narrative voice; partially served by lightning archetypes (unpaired status = no specific allegiance) but not exactly.

**Mitigation:** the form library accumulation across seasons serves a *long-arc* version of these fantasies. A player at season 6+ who has the full canonical-7 substrate library in their form collection *is* the polymath wizard, expressed at the lifetime-of-play layer.

**Player consequence:** the in-season player who wants this identity expressed *now* has to wait. The thematic patience required is genuine.

### § 7.3 — Genre vocabulary slot empty

The ARPG genre has a recognizable slot for the multi-element-mage archetype (PoE Elementalist; LE Runemaster; D4 Sorcerer-splash; D2 multi-element-Sorceress). Canonical-6 leaves this slot empty in the per-class roster. Players coming to Reincarnated from other ARPGs will look for this slot; they will find lightning archetypes + controller archetypes as the closest analogs, plus the meta-layer form-library framing as the long-arc analog.

**Mitigation:** lightning archetype emphasis in design copy + form-library narrative emphasis on integrator-form-as-journey (§ 5.4). These are mitigations, not full replacements.

**Player consequence:** experienced ARPG players will note the absence. Whether they're frustrated or intrigued depends on how the form-library story is told.

### § 7.4 — Future-design constraint on substrate composition

The retire verdict establishes a precedent: substrate-coherent generation is the convergence-supporting pattern; multi-substrate generation hit a structural wall in 2026-05. Future design work that wants to introduce multi-substrate composition (Phase 2 substrate expansion; experimental archetypes; spirit-guide weave) must pick up the cost of solving the gear-buffing + balance-loop-convergence interaction that D11 surfaced. This is a *known* cost; it doesn't go away.

**Player consequence:** none directly; this is a design-team-side cost note. But the canonical-6 transition makes substrate-composition work *slower* in the future because the structural problem is now documented as a known-hard rather than an unknown.

---

## § 8 — Cross-canon cleanup list (for jack-ryan strip pass)

This list enumerates every canonical / design / engine doc that mentions hybrid_mage and the rough nature of the amendment needed. Jack-ryan executes the strip pass as a separate dispatch (knight-rider fires post this doc's ship). The list is comprehensive but the strip-pass agent should verify each location and exercise judgment about retain-vs-strip (historical references should typically *retain* with retire-context annotation; live design statements should *strip* or replace with canonical-6 statement; example/illustration uses should *update* to reference a canonical-6 archetype).

**Cleanup strategy decision (recommend):** retain historical references with `[RETIRED 2026-05-18; see canonical-6-transition-retire-hybrid-mage-2026-05-18.md]` annotation; strip live design statements; update illustrative uses to canonical-6 archetypes. Do *not* delete hybrid_mage from docs entirely — the historical record is load-bearing for context.

### § 8.1 — Canonical/ design docs

1. **`canonical/09-geometry-palette-discussion.md`** — line 159 references hybrid_mage in AOE share context. Strategy: retain reference with retire annotation; the AOE-share-design discussion is historical record. Recommend prefix the paragraph with "[Pre-canonical-6; hybrid_mage retired 2026-05-18]".

2. **`canonical/17-gear-and-spirit-guide-design.md`** — no direct hybrid_mage mentions found in grep, but verify by re-scan; this is the spirit-guide canonical doc and may have hybrid references in the gear-fit / archetype-match sections. If any, annotate.

3. **`canonical/28-engine-arpg-rebalance-design.md`** — lines 349, 497, 868, 881, 1137 reference hybrid_mage in B6/B14.5 design discussion. Strategy: retain with retire annotation; this doc is the B-series rebalance history and the references are load-bearing historical context.

4. **`canonical/30-engine-explainer-current.md`** — line 120 enumerates the archetype list including hybrid_mage. Strategy: **strip** hybrid_mage from the enumeration; add a paragraph noting the canonical-6 transition with pointer to this doc.

5. **`canonical/32-progression-design.md`** — lines 260, 282 reference hybrid_mage in skill-tree multi-element rules. Strategy: **strip** the live design rules referencing hybrid_mage; replace with canonical-6 statement ("multi-element classes are not generatively produced post-canonical-6; cross-chain investment rules apply to gear-secondary-element kits if they emerge"). If the multi-element-skill-tree rule was hybrid_mage's primary use case, the rule itself may be reviewable.

6. **`canonical/33-progression-skeleton.md`** — line 237 references hybrid_mage in skill-count band. Strategy: **strip** hybrid_mage from the skill-count band table; adjust band ranges if needed (the "complex archetypes 14-15 skills" band may no longer have a primary member).

7. **`canonical/16a-roadmap-shipped-log.md`** — line 27 references hybrid_mage in B6 templates documentation. Strategy: retain with retire annotation; shipped-log is historical record.

### § 8.2 — Canonical/story/ docs

8. **`canonical/story/d11-hybrid-mage-tuning-advisory-2026-05-17.md`** — the D11 advisory. Strategy: retain entire doc; annotate at the top "[RETIRED outcome — see canonical-6-transition-retire-hybrid-mage-2026-05-18.md for retire verdict and rationale]". The advisory's identity-preservation argument is retracted material per the D11.2 advisory § 0; this canonical-6 doc supersedes.

9. **`canonical/story/d11-hybrid-mage-tuning-postmortem-2026-05-17.md`** — D11 postmortem. Same strategy: retain + annotate retire outcome at top.

10. **`canonical/story/d11-postmortem-option-b-verdict-2026-05-17.md`** — same strategy.

11. **`canonical/story/d11-2-structural-redesign-advisory-2026-05-17.md`** — the D11.2 advisory. Strategy: retain + annotate "[RETIRE outcome triggered per § 6 of this advisory + Matt L3 verdict 2026-05-18 — see canonical-6-transition-retire-hybrid-mage-2026-05-18.md]". The advisory's RETIRE clause has activated; the doc remains historical record of the lever-shape work that preceded.

12. **`canonical/story/archetype-coupling-archaeology-2026-05-17.md`** — lines 43, 69, 89, 196. The Coupling #3 finding (stat allocation fallback to hybrid_mage stats) becomes *more* relevant after retire — the fallback target archetype no longer exists in the canonical roster. Strategy: **strip** hybrid_mage from the fallback-stats-target list; the coupling-archaeology entry needs a follow-up amendment noting "post-canonical-6, the fallback target is unknown / requires re-decision (recommend: error on unrecognized archetype rather than silent fallback)". This is a real engineering follow-up that may warrant a separate dispatch.

13. **`canonical/story/embodiment-narrative-layer.md`** — lines 147, 150, 193, 202-204, 264. Hybrid_mage referenced as energy-tier example + the "hybrid = element-mixing only" clarification section. Strategy: **strip** hybrid_mage examples and references; the energy-tier framing remains valid for substrate-coherent archetypes; the "hybrid = element-mixing only" clarification section can be retained as a *naming-discipline* note (if a future "hybrid_warrior" is ever proposed, the clarification is useful) but should be annotated "[hybrid_mage retired 2026-05-18; clarification retained as naming discipline for any future hybrid-named archetype]".

14. **`canonical/story/vs2a-vfx-scene-needs.md`** — lines 205, 236, 378. Hybrid_mage referenced in VFX-coverage table + beam_channel mappings. Strategy: **strip** hybrid_mage rows from VFX-coverage tables; verify no orphaned VFX commissioning depends on hybrid_mage VFX coverage; if beam_channel was uniquely hybrid_mage's geometry, re-map to a canonical-6 archetype that uses beam_channel (controller archetypes per b6_archetype_templates).

### § 8.3 — Engine code (rocket's territory; flagged here for completeness)

The rocket archetype-list removal dispatch (`2026-05-18-rocket-canonical-6-archetype-removal-plus-is-retired-flag.md`) handles the engine-code strip. Flagged here for cross-reference:
- `reincarnated-engine/src/reincarnated/generation/b6_archetype_templates.py` (HYBRID_FORBIDDEN_PAIRS, _HYBRID_ARCHETYPE_TEMPLATES, ARCHETYPES_FORBIDDEN_CLOSE_RANGE)
- `reincarnated-engine/src/reincarnated/generation/b6_kit_builder.py` (hybrid_mage element-distribution logic)
- `reincarnated-engine/src/reincarnated/generation/element_biases.py`
- `reincarnated-engine/src/reincarnated/generation/d10_kit_constraints.py` (Lever B code; rocket recommends retain-with-comment per their dispatch)
- `reincarnated-engine/src/reincarnated/generation/stat_allocator.py` (hybrid_mage fallback stats — Coupling #3 follow-up)
- Tests / fixtures referencing hybrid_mage

### § 8.4 — Cross-product (loadout + demo)

- **`reincarnated-loadout/src/data/constants.ts`** — line 59 ARCHETYPE_LABEL hybrid_mage entry. Strategy: retain entry but ensure consume-time filter excludes retired classes (loadout-side dispatch separately fires).
- **`reincarnated-loadout/src/__tests__/cipher-no-leak.test.ts`** — lines 208-209 test using hybrid_mage. Strategy: retain test (verifies the label-resolution logic); the test exercise doesn't depend on hybrid_mage being a live archetype.
- **`reincarnated-demo/src/visuals/archetypeRenderer.ts`** — line 44 hybrid_mage renderer entry. Strategy: retain entry; consume-time filter via `is_retired: true` excludes retired classes from render pool.
- **`reincarnated-demo/src/data/loader.ts`** — line 4 D11 sprint authorization comment. Strategy: update comment to reference canonical-6 transition outcome.

### § 8.5 — Decisions log + engineering disciplines (jack-ryan's territory)

- **`reincarnated-engine/design/decisions/decisions-log.md`** — append new RETIRE entry per jack-ryan's dispatch `2026-05-18-jack-ryan-decisions-log-retire-plus-discipline-17-amendment.md`.
- **`reincarnated-engine/design/working-agreement/engineering-disciplines.md`** — append Discipline #17 with the smoke-environment-fidelity amendment per the same jack-ryan dispatch.

### § 8.6 — Cleanup pattern (recommend)

Recommend jack-ryan's strip pass uses one consistent annotation pattern across all retained references:

> `[hybrid_mage RETIRED 2026-05-18 per canonical-6 transition; this reference is historical record. See canonical/story/canonical-6-transition-retire-hybrid-mage-2026-05-18.md for context.]`

This makes the historical-vs-live distinction unambiguous and forward-pointers consistent. Live design statements get the reference stripped + canonical-6 statement substituted; historical references get the annotation prepended.

---

## § 9 — Decisions-log handoff brief (for jack-ryan)

Per the dispatch coordination, jack-ryan authors the decisions-log entry capturing this retire. Brief follows; this is the structured input for jack-ryan's entry construction.

**Title:** `2026-05-18: RETIRE hybrid_mage from canonical-7 — #160 verdict`

**Decision:** Drop hybrid_mage from the canonical archetype list. Canonical-7 (six substrate-coherent integrator slots + 1 hybrid integrator slot) transitions to canonical-6 (six substrate-coherent integrator slots only). The 17 existing hybrid_mage instances in seasons 002011-015 receive `is_retired: true` provenance flags and are filtered at consume time by demo + loadout. Future seasons generate at canonical-6.

**Date:** 2026-05-18

**Authority:** Matt L3 verdict (early morning 2026-05-18; explicit in dispatch chain `2026-05-18-gandalf-canonical-6-retire-hybrid-mage-design-doc.md` and parallel rocket / jack-ryan dispatches)

**Context:** Three structural attempts to bring hybrid_mage into balance-loop convergence under the canonical-7 substrate roster all failed:
- D11.0 (element-coverage damage tax α=0.07; 6% interior convergence; magnitude-by-genre-analogy MISS)
- D11.1 (skill-count ceiling=10 + α=0.08; 0% interior convergence; pruning protected non-damage skills, surfaced coverage-redundancy hypothesis as refuted)
- D11.2 (kit-aggregate DPS-density uniform scaling Lever B; smoke 5/5 PASS at scale=0.75; Phase B 0/17 FAIL — smoke environment lacked gear_catalog, producing false-positive)

The D11.2 Phase A / Phase B mismatch surfaced the structural root cause: gear Monte Carlo affix sampling buffs hybrid_mage's effective fight performance enough that *any* damage-magnitude lever at identity-preserving scale (≥0.5) cannot bring the archetype below the 0.50 WR-at-floor target in the production environment. The clean lever would target gear-included performance directly (gear-affix density cap; damage_taken_multiplier penalty); this is D12+ multi-day work with uncertain payoff.

**Rationale (per Matt):** Fastest path to "develop a completely new LLM generated season once we feel those issues are resolved and converge many classes from it" is to remove the broken archetype, not iterate further on it. Identity at scale_factor < 0.5 would be shell-of-self. The integrator role can be expressed at the meta-layer (form library + Spirit Guide) rather than the per-class-generation layer.

**Alternatives considered:**
- **Option 1** — Re-run smoke with gear_catalog included; sweep deeper {0.55, 0.45, 0.35}. *Rejected*: identity-preservation risk below 0.5 + uncertain whether any scale converges against gear-buffing root cause.
- **Option 2** — Composite B+D at scale=0.65 + 5% HP penalty in full gear environment. *Rejected*: incremental, not addressing the gear-buffing structural problem.
- **Option 4** — D12+ structural redesign of hybrid_mage kit composition pipeline. *Rejected*: multi-day cycle with uncertain payoff against the same gear-buffing root cause.

**Implications:**
- Engine generation drops to canonical-6 substrate-coherent integrator slots (rocket implementation per dispatch `2026-05-18-rocket-canonical-6-archetype-removal-plus-is-retired-flag.md`)
- 17 existing hybrid_mage classes in 002011-015 receive `is_retired: true` flag; demo + loadout filter at consume time
- Cross-canon strip pass (per § 8 of this doc) removes / annotates hybrid_mage references in canonical-09, -17, -28, -30, -32, -33, -16a, six story docs, and the engine + consume-time code
- Future seasons start at 002016 with canonical-6 generation
- Alternative-resurrection paths (§ 6 of this doc: experimental tier; Spirit-Guide bonus; Phase-2 substrate expansion) parked for future design consideration
- Discipline #17 canonical landing + smoke-environment-fidelity amendment (per jack-ryan dispatch)

**Forward pointers:**
- `canonical/story/canonical-6-transition-retire-hybrid-mage-2026-05-18.md` (this doc; design rationale; identity redistribution; resurrection paths)
- `agentic_orchestration/dispatches/2026-05-18-rocket-canonical-6-archetype-removal-plus-is-retired-flag.md` (engine archetype-list removal + is_retired flag pass)
- `agentic_orchestration/dispatches/2026-05-18-jack-ryan-decisions-log-retire-plus-discipline-17-amendment.md` (this decisions-log entry + Discipline #17 canonical landing)
- D11 cycle history: D11 advisory + D11 postmortem + D11.2 advisory + D11.2 Phase B failure dispatch

**Cross-references** (decisions-log entry should mention):
- Earlier hybrid_mage-related decisions-log entries (D10 element-coverage tax authorization; D11 α-recalibration; D11.1 ceiling lever; D11.2 Lever B authorization)
- L3 #42 (hybrid_mage retire-vs-tune; this entry surfaces L3 #42 in the (ii) RETIRE direction per D11.2 advisory § 7.1 / § 6)
- Discipline #17 (canonical landing in same pass)

---

## § 10 — Closing

The chromatic_mage that walks lightly across many substrates is a recognizable form in the cosmology. It is not a class the generator produces in canonical-6. It is the *journey-shape* of the player who accumulates forms across seasons — the integrator identity expressed at the layer where Reincarnated's design naturally hosts it.

The retire is honest. The D11 cycle was a sequence of structural attempts to make the integrator identity converge against a substrate landscape that wasn't designed for hybrid composition from the start. Three attempts; three increasingly-informed failures; the empirical floor at scale_factor=0.75 with gear is the wall. Retiring is not surrendering the identity; it is relocating the identity to the layer that can carry it.

The cosmology is unchanged. The substrate-commitment-cost framing in the D11 advisory § 5 remains true — *holding many commitments without fully expressing any* is still the chromatic identity. We just stop trying to express that identity in a single generated kit. We express it in a *long arc* of forms collected across many lives; in a *spirit-guide weave* across encounters within a season; in a *gear-and-trait composition* at the loadout layer.

The Court of Forms remembers the hybrid identity. It is one of the forms. It walks among the others, in the library, in the player's accumulated journey. The form does not need to be a class to remain a form. The discipline of canonical-6 is the discipline of letting the layer carry the meaning that fits that layer.

The new-season milestone unblocks. The 17 floor-pinned instances become historical record. The roster ships. The form remembers itself in the journey rather than in the generator. That is enough.

---

## § 11 — Acceptance criteria

- [x] § 1 — Decision context: D11 cycle history, Matt's L3 verdict, framing as simplification not failure
- [x] § 2 — What was hybrid_mage: generative shape, thematic identity, design intents, 17 staged instances
- [x] § 3 — Why it didn't survive contact with the balance loop: multi-element DPS compounding, gear over-buffing, no clean lever
- [x] § 4 — Canonical-6 archetype list with identity reaffirmation
- [x] § 5 — Where the lost identity-DNA lives now (Spirit Guide; lightning/controllers; player composition)
- [x] § 6 — Alternative resurrection paths (experimental tier; Spirit-Guide bonus; Phase-2 expansion) — flagged not committed
- [x] § 7 — What's lost (honest accounting of in-season variety, fantasy paths, genre vocabulary, future design constraint)
- [x] § 8 — Cross-canon cleanup list with file/section refs and per-doc strategy (for jack-ryan strip pass)
- [x] § 9 — Decisions-log handoff brief (for jack-ryan)
- [ ] Hive-log STATE entry on phase-1-p1-log.md (next step; PRE-SIGNAL § 14.1.1 required)
- [ ] Completion record appended to dispatch (next step)

---

*Authored 2026-05-18 by gandalf per Matt L3 RETIRE verdict + dispatch `2026-05-18-gandalf-canonical-6-retire-hybrid-mage-design-doc.md`. Successor to the D11 advisory + D11.2 advisory chain. The form remembers itself in the journey rather than in the generator.*
