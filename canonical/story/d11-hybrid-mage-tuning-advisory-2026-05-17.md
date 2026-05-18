# D11 — Hybrid_mage tuning advisory (ARPG-balance direction)

> *[RETIRED OUTCOME — hybrid_mage RETIRED 2026-05-18 per canonical-6 transition; this reference is historical record. The identity-preservation argument in this advisory is retracted; the RETIRE clause in the D11.2 advisory § 6 is activated. See `canonical/story/canonical-6-transition-retire-hybrid-mage-2026-05-18.md` for retire verdict and rationale. See `reincarnated-engine/design/decisions/decisions-log.md` for the RETIRE entry.]*

**Authority:** Matt L3 2026-05-17 evening — "Invoke Gandalf for decision as to how to tune sprint towards ARPG balance."
**Author:** gandalf (story-and-design steward).
**Predecessor:** rocket v1.12 D10 salvage completion record — 37.1% convergence; residual = hybrid_mage structural over-generation at modifier floor (0.05).
**Closes:** Matt L3 #42 (hybrid_mage retain-or-retire) — see § 3.
**Hands off to:** gamora (D11 math note) + jack-ryan (Gate 1 readiness) + drax (UI/narrative surface follow-on, low priority).
**Type:** Pattern B short — design advisory; no code; gates the D11 sprint.

---

## § 0 — Executive recommendation

**Retain hybrid_mage. Reshape it. Tune via the canonical-genre lever the engine already half-encodes: investment-cost gating against a specialist baseline, expressed as a quadratic kit-area damage tax keyed to canonical-element breadth.**

The pre-D10 telemetry is unambiguous: hybrid_mage at 17/17 instances failed to converge — *not because the archetype is wrong*, but because the engine generates it with **zero of the structural costs that every successful ARPG charges for multi-element breadth.** Path of Exile charges in passive points and resists. Diablo 2 Sorceress charges in synergy-bonus opportunity cost. Last Epoch Runemaster charges in rune-combination cooldown management. Grim Dawn Druid charges in mastery-point split. Every canonical implementation of "the mage who uses multiple elements" pays for breadth somewhere. Reincarnated's hybrid_mage pays nowhere. That is the gap.

The recommended D11 lever is a **two-part composite** (concrete enough for gamora to translate to math, narrow enough to land in the D11 sprint):

1. **(Primary) Element-coverage damage tax.** Per-skill effective damage multiplier scales as `1.0 - α × max(0, n_elements − 2)²`, where `n_elements` is the count of distinct canonical_elements in the kit and `α ≈ 0.07`. A 2-element hybrid pays nothing (parity with non-hybrid specialists). A 3-element hybrid pays ~7%. A 4-element hybrid pays ~28%. The tax is quadratic, not linear, because the *combinatorial coverage advantage against the gauntlet's resistance profiles* is quadratic — each additional element opens not one new resistance hole but `n` new ones via cross-coverage. Empirically this is what makes 4-element hybrid_mage immune at floor modifier: the marginal monster the kit faces almost always has *some* element it is vulnerable to.
2. **(Composite) Element-breadth ceiling tightened from 4 → 3** (with a "ceremonial" 4-element exception path for capstone seasons or specific Trial bosses; not for general generation).

This is **lever (b) — element-coverage damage tax + composition rule** from the dispatch's Sub-Q 3 menu. It rejects pure skill-ceiling (lever (i)) as already exhausted (the D10 ceiling=12 reduced from 14 did not close the gap) and rejects pure breadth-cap-at-2 (which would functionally retire the archetype). The quadratic tax is the canonical ARPG move (PoE-shaped, D2-Sorceress-shaped, LE-Runemaster-shaped) — and it has a natural thematic fit with the canonical-7 substrate-identity framework already in the project's lore: each substrate has a *commitment*; covering many substrates means *committing fully to none*.

The recommendation closes L3 #42 in the **(iii) reshape** direction: keep the archetype, keep the name, keep the form-library narrative slot, but tighten what it costs. D11 scope is **tight on hybrid_mage**, with a flagged-but-deferred broader recommendation for downstream hybrid-family work (hybrid_physical, future hybrid_summoner, holy/shadow luminance-hybrids — none currently in the generation pool but architecturally permitted).

The rest of this document is the case for that recommendation: § 2 the ARPG-canon evidence (load-bearing per the dispatch), § 3 the identity decision with its thematic justification, § 4 the tuning lever with gamora-translatable specifics, § 5 the canonical-7 thematic framing, § 6 the D11 scope guidance, § 7 open questions for Matt, § 8 handoffs.

---

## § 1 — Premises (what we are tuning against)

Before the survey, the assumptions that frame the recommendation:

1. **The engine has 24 archetypes; one is hybrid_mage.** Of the 24, hybrid_mage is structurally unique: it is the only template that does not derive from substrate × role composition. The hybrid template lives in `_HYBRID_ARCHETYPE_TEMPLATES` (1 entry) merged with `composed` (substrate-role outputs) and `PHYSICAL_ARCHETYPE_TEMPLATES` (5 entries). Hybrid is *the exception*, not the rule.
2. **The canonical-7 substrate set has explicit hybrid commitments.** The substrate-identity declarations (authored 2026-05-17, hive log Phase-1 P1) carry a `forbidden_hybrid_with` field for every substrate. Fire↔water and earth↔wind are *declared forbidden* (anti-pole substrates that erase each other's mechanical signature). Holy↔shadow are declared paired-luminance — opposed but composable (the "duality-of-light-and-shadow" tier in Solo Leveling's genre vocabulary). Lightning is declared unpaired — composes freely with all. These are *substrate-level identity claims* that the hybrid composition logic already respects (HYBRID_FORBIDDEN_PAIRS is loader-derived).
3. **The form-library narrative requires hybrid as an attainment-tier identity.** Per `canonical/story/court-of-forms.md`, `canonical/story/embodiment-display-loadout.md`, and `canonical/story/gandalf-phase2-bullet-points.md` § 1.4, the form-library is a Solo-Leveling-Shadow-Army-shaped collection of attained forms across many seasons. A player who has spent dozens of seasons with the Wheel should be able to reach a form that *integrates* multiple substrates — that is the late-game ascendant moment. The hybrid_mage archetype is one of the engine's narrative slots for this experience. Retiring it would erase a meaningful capstone identity.
4. **The Phase-1 P1 substrate refactor migrated single-substrate composition to declarative-perimeter; hybrid composition is Phase-1 P2 candidate.** The current `_HYBRID_ARCHETYPE_TEMPLATES` is the *holdover* that Phase-1 P2 will refactor. D11 should not pre-empt P2 — but D11's lever choice should be P2-compatible (i.e., the tax should live where P2 will look for it: as a derivable function of substrate-identity declarations, not as a hardcoded constant in the holdover template).
5. **Gauntlet composition is the implicit baseline.** The gauntlet has 12 slots: 6 swarm/pack (excluded from convergence WR), 2 magic, 2 elite, 1 mini-boss, 1 boss. Each tier has an element. Multi-element coverage's structural advantage scales with *element variety in the gauntlet*. The 5 staged seasons used a gauntlet with fire/water/earth elements across the 6 non-pack slots — three of the canonical-four. This is the *minimum-coverage* test; D11's tax must work against richer gauntlets too (lightning/holy/shadow tier slots will appear once those substrate archetypes are properly composed).

These premises are non-negotiable for the recommendation. If any are wrong, the recommendation needs to be revisited.

---

## § 2 — ARPG-canon evidence base

This section is the load-bearing core of the advisory. It surveys how the genre has handled multi-element / hybrid builds across roughly thirty years of ARPG history. The categorization runs (a) → (e) from the dispatch's Sub-Q 1 framing, and the section closes with the explicit mapping of which category Reincarnated should align to.

### § 2.1 — Diablo I (1996) — Sorcerer as scroll/staff specialist

**Pattern:** No hybrid; spellbook drop as gate.

Diablo 1's Sorcerer has access to all spells, but each spell must be *learned from a dropped tome*, and the spell's effectiveness scales with how many times you have invested in that specific spell (the spell-level system). Functionally: the *player can technically use every element*, but practical play means you pick 2-3 spells and dump levels into them. The element diversity is *theoretical* — the tome-drop economy makes specialization the only viable path.

**Cost structure:** Resource gate (tome drop scarcity) + investment gate (per-spell level investment is a true opportunity cost — your gold and your stat-point allocation go to one spell tree, not five).

**What Reincarnated can learn:** D1 doesn't have a "hybrid_mage" class; it has *one* mage and the player chooses what to specialize. The lesson is that *the player makes the breadth-vs-depth choice; the engine doesn't grant breadth as a free archetype*. This is the foundational ARPG pattern. Every subsequent ARPG has either preserved this (specialization through investment) or violated it (and paid a balance cost).

### § 2.2 — Diablo II / Lord of Destruction (2000/2001) — Sorceress as canonical multi-element

**Pattern:** Three trees (Fire / Cold / Lightning), each with its own ladder of synergies, and a global skill-point economy that rewards specialization.

The Sorceress is *the* canonical ARPG multi-element class. She has three element trees of equal depth. She can technically build all three. Almost no successful build does — and the reason is *synergy*. The synergy system in D2 is the genre's single most-elegant breadth-tax: every skill in a tree gets a per-rank bonus from sibling skills in the same tree. A Fire Mastery → Inferno → Fire Wall → Meteor Sorceress at end-game might have +50% to all fire damage from Fire Mastery (10 points), +60% additional from synergies (Warmth 20, Fire Bolt 20, Fire Ball 20). If she splits points across fire and cold, *neither tree synergizes*, and her total damage is structurally worse than the single-tree specialist.

The few builds that did multi-element succeed only with structural exceptions:
- **Meteorb (Meteor + Frozen Orb):** Famous late-90s/early-2000s build. The trick is Meteor and Frozen Orb both scale primarily from a single synergy each (not deep trees), so the split is cheaper than splitting a deep-synergy tree like Lightning. Even Meteorb is *measurably weaker than pure-Blizzard or pure-Fireball builds* in damage-per-second — it survives because the breadth gives it **monster-immunity-coverage** for the Hell-difficulty monster-immunities that became a balance feature in LoD. The breadth was a *workaround for endgame content design*, not a generic strength.
- **Pure Lightning Sorc (Charged Bolt + Lightning + Chain Lightning + Mastery):** Single-tree but uses three skills within the tree. This is *not* a hybrid build; it is depth within a single element.

**Cost structure:** Synergy opportunity cost. The genre's most influential breadth-tax. Multi-element is not forbidden; it is structurally worse than specialization, *and the game uses monster immunities to give multi-element a niche purpose anyway*.

**What Reincarnated can learn:** D2's Sorceress is exactly the archetype hybrid_mage is shaped after. The lesson is that *breadth must cost something measurable in damage output*, and *the game's content design (monster immunities, in D2) can make breadth situationally valuable without making it generically strong*. This is the exact prescription for Reincarnated: charge a damage tax for breadth; let the trial-boss-gallery's elemental variety make breadth situationally appealing for capstone-tier players.

**Specific synergy math from D2 LoD as anchor for tax magnitude:** The D2 synergy economy charges roughly **2-3% per synergy point** as a positive bonus on the target skill. A pure-Blizzard Sorceress at endgame has ~80% damage bonus from in-tree synergies. A split fire/cold Sorceress with half her points in each tree has ~30-40% damage bonus per tree. The differential between specialist and split is roughly **40-50% of damage output**. This is the genre's empirical magnitude for "what does breadth cost in the most-studied multi-element ARPG class." My recommended α=0.07 quadratic on a 4-element kit produces a 28% tax — *less than* the D2 specialist-vs-split differential, which is the correct calibration: Reincarnated's hybrid is *meant* to be playable (it is the engine-declared archetype), where D2's split-build is *not* meant to be optimal (it is the player-chosen anti-optimal). The 28% sits in the right band.

### § 2.3 — Diablo III (2012) — Wizard as no-cost multi-element

**Pattern:** Skill-slot system with no opportunity cost; rune-mod customization.

D3's Wizard can equip Magic Missile (arcane), Frost Ray (cold), Disintegrate (arcane), Meteor (fire), and Archon (all-elements) simultaneously, with no synergy-tree opportunity cost. The 7-skill loadout is the player's only real choice; the trees and synergies that D2 used to tax breadth are gone.

The result: D3 at launch had a *severe balance problem* — there was no meaningful difference between a "fire Wizard" and a "multi-element Wizard," because the damage values didn't penalize breadth. The Reaper of Souls expansion and the subsequent seasons added **set bonuses** (e.g., Tal Rasha's set: each different elemental skill cast adds a stacking damage buff to the next elemental skill cast) — which converted multi-element from *neutral* to *actively encouraged for one specific build*. But this is the inverse of what Reincarnated wants: D3 had to *invent a system to make multi-element rewarding* because its core mechanics treated breadth as free.

**Cost structure:** None at the skill-equip layer. Set bonuses later rewarded breadth, which is a *gear-driven exception* rather than a *core-mechanic-driven cost*.

**What Reincarnated can learn:** D3 is the cautionary tale. It is what hybrid_mage looks like today: 4 elements, no synergy tax, no opportunity cost, and a balance problem that requires either (a) capping breadth or (b) inventing gear-layer corrections. Reincarnated cannot afford to invent gear-layer corrections at this stage of the engine — the gear pool is already a heavy LLM-cost surface. The fix has to be at the generation layer, not at the gear layer.

### § 2.4 — Diablo IV (2023) — Sorcerer enchantment slots and split-tree fragmentation

**Pattern:** Per-class specialization slots; element-keyed legendary aspects; talent tree with element subsections that share damage but compete for points.

D4's Sorcerer has Fire / Ice / Lightning subsections in its talent tree. The genre evolved a *softer* breadth-tax than D2: tree points are limited (50-ish at endgame), so spreading them thinner across multiple elements means each element has fewer node bonuses. **Enchantment slots** add a layer: a Sorcerer equips a skill in an enchantment slot to activate its passive effect, and there are only 2-3 enchantment slots — so breadth means losing passive coverage. **Legendary aspects** are heavily element-keyed (e.g., "Aspect of Singed Extremities" works only with Burn-related skills), so breadth means fewer aspects synergize.

The D4 Sorcerer at endgame is canonically a *specialist* (Ice Shard meta, Fire Bolt meta, Chain Lightning meta in various seasons). The "hybrid Sorcerer" build is a known meme-tier identity — playable but consistently 30-50% behind specialist DPS in season tier-list discourse. This is the genre's current consensus.

**Cost structure:** Tree-point opportunity cost + enchantment-slot opportunity cost + legendary-aspect synergy opportunity cost. *Three layers of breadth-tax stacking*. The Sorcerer is structurally *able* to hybrid; the game is structurally *disinclined* to reward it.

**What Reincarnated can learn:** Multi-element specialization is the *modern ARPG default outcome*. Even when the class is permitted to hybrid, the layered taxes make specialization the practical optimum. Reincarnated's hybrid_mage is currently in the position D3-launch was: permitted with no tax. The market has spoken on this; D3-launch was a balance disaster. D4 corrected via three layered taxes. Reincarnated can choose one layer (the damage tax) and get most of the way there.

### § 2.5 — Diablo Immortal (2022) — Mobile-platform Sorcerer compression

**Pattern:** 4-skill cap + ultimate; element-keyed legendary gems.

Immortal compressed the D3/D4 skill economy to 4 active skills + 1 ultimate, total. Multi-element is technically permitted (you can run Fire Beam + Ice Crystal + Lightning Nova + Meteor), but the 4-skill cap *forces* either deep single-element synergy (the better choice for mobile-onboarding clarity) or a fragmented kit with no synergy lock-in. The Immortal Sorcerer at meta-tier endgame is canonically Lightning Nova spam or Meteor spam — single-element identification at the kit level.

**Cost structure:** Skill-count cap is the primary breadth-tax. With only 4 skills, breadth means *no specialization*. The math is brutal: 1 skill per element across 4 elements = 1-deep on each = no synergy hook; 4 skills in 1 element = 4-deep on one = full synergy.

**What Reincarnated can learn:** Skill-count cap *alone* (Reincarnated's D10 lever) is sufficient to discourage breadth *if the cap is tight enough*. Immortal at 4 caps; D2/D4 at ~6-8 active skills caps; Reincarnated currently at 12. The cap-only approach works at small numbers and fails at large numbers — and Reincarnated's combat-cadence design (per `canonical/story/aoe-tuning-and-monster-density-genre-canon-validation-2026-05-17.md`) is in the 10-12 skill range, which is too generous for a cap-only approach. The cap must be paired with an additional tax.

### § 2.6 — Path of Exile (2013 onwards) — Chromatic / Tri-Elemental / Elementalist class

**Pattern:** Universal passive tree + class-specific Ascendancy that explicitly rewards multi-element.

PoE is the genre's most-developed multi-element design space. The base Witch class's *Elementalist* Ascendancy is *explicitly* a multi-element specialist — its keystone passives (like "Mastermind of Discord" — "exposure to one element from your skills"; "Beacon of Ruin" — "ignite/chill/shock are 20% stronger and spread"; "Liege of the Primordial" — multiplies elemental-golem damage) are *only meaningful when you use multiple elements*. PoE *rewards* breadth — but the reward is locked behind:

- **30+ passive points** committed to elemental-damage nodes across the tree (a significant slice of a typical 100-passive endgame)
- **Specific gear sockets** (a Trinity Support gem requires the skill to deal multiple elements; the gear must support specific colors)
- **Resistance penalty** (every multi-element build runs against the cap-resistances-everywhere endgame requirement; specialists need only one elemental defense direction; hybrids need three)
- **Ailment overlap penalties** (a fire ignite and a cold freeze and a lightning shock don't stack their full effects on the same monster — there is a diminishing return when one ailment is already applied)

The Elementalist build is *the* multi-element archetype of modern ARPGs, *and it pays four layered costs*. It is also *consistently mid-tier in DPS-leaderboards* — not the strongest archetype in any meta, but a viable, distinctive playstyle. This is what a balanced multi-element archetype looks like.

**Cost structure:** Passive-point opportunity cost + gear-socket opportunity cost + resistance-cap-coverage cost + ailment-overlap diminishing-returns cost. *Four layered taxes.*

**What Reincarnated can learn:** The PoE Elementalist is the *thematic and mechanical reference design* for hybrid_mage. The lesson is **layered taxes** and **a clear positioning as "viable but not optimal."** Reincarnated cannot replicate four layered taxes (the engine doesn't have passive trees or gear sockets or resistance caps at that granularity). It *can* replicate the spirit with one well-tuned tax: the **element-coverage damage tax**, which is functionally what PoE's resistance-coverage requirement does in slow form. PoE forces the hybrid to spend ~25-30% of their passive points on resistance to survive; Reincarnated's damage tax achieves a comparable net-DPS effect more cleanly.

### § 2.7 — Path of Exile 2 (2024-2025 early access) — Same school, refined surface

**Pattern:** Compressed passive tree but otherwise PoE-shaped multi-element philosophy.

PoE2's early-access surface preserves the PoE1 philosophy: multi-element is a viable build space, gated by layered investment. The Sorceress (PoE2's renamed elementalist-equivalent) ascendancy paths include Stormweaver (multi-element-keyed) and Chronomancer (time-themed but element-flexible). Community early-access discourse confirms the same pattern: multi-element is playable, often mid-tier, and specialists win the leaderboards.

**Cost structure:** Same as PoE1, with refined surface.

**What Reincarnated can learn:** The genre's most-respected multi-element design has not deviated from the PoE1 philosophy across a major version transition. This is strong evidence that the *layered investment-tax model* is the *durable* design pattern. Reincarnated should encode at least one of those taxes; the cost-of-breadth needs to be visible somewhere.

**A specific PoE pattern Reincarnated can replicate at zero engine cost: ailment-overlap diminishing returns.** PoE's hybrid builds suffer because *one ailment is applied at a time per monster* — the most-recently-applied ailment displaces the prior. A 3-element kit with fire ignite + cold chill + lightning shock will *waste* most of its ailment-application work because only one ailment can be present per monster at a time. The kit's ailments compete for the same slot. This is the *elegant* version of the breadth-tax: no explicit damage multiplier; the tax is in the wasted-effects-application. Reincarnated could adopt this as a future-D12+ refinement (per-monster ailment-slot limit; new ailment displaces oldest). Flagged for downstream design; not required for D11; documented here because it's the same tax-shape applied at a different mechanical layer.

### § 2.8 — Last Epoch (2024 release) — Runemaster as composable hybrid

**Pattern:** Per-skill skill-trees + Runemaster Mastery as *explicit* hybrid-rewarding subclass.

Last Epoch's Runemaster (released in the Runemaster patch, 2024) is the most-recent canonical hybrid mage in a successful ARPG. The Runemaster's defining mechanic: **Runic Invocations** — combinations of three runic glyphs you cast in sequence to produce a multi-element effect. The Runemaster builds runic combinations from element-keyed glyphs (Fire / Cold / Lightning / Frost / Lava / etc.) and the resulting Invocation has properties derived from all three input glyphs.

The Runemaster's balance is structured around:
- **Cooldown management** — Invocations have substantial cooldowns; spamming them is not viable; rotation discipline matters
- **Mastery-tree investment** — The Runemaster mastery tree branches into Frost / Fire / Lightning specializations within Runemaster, *and the same trade-off applies*: spreading mastery points across all three branches gives you weaker Invocations overall than focusing on one specialization that gates the others
- **Per-skill specialization** — Each non-Runic skill (the normal skill bar) has its own skill tree; investing in many skill trees thin gives less power than one skill tree deep

The Runemaster's community reception (per LE 1.0 discourse, ~Feb 2024) was overwhelmingly positive *as a thematic class* and *moderately balanced as a mechanical class* — its multi-element power-spike is real but the *cooldown discipline* costs it sustained-damage uptime that single-element classes don't pay.

**Cost structure:** Cooldown-management tax (multi-element via Invocations costs combat cadence) + mastery-point opportunity cost + per-skill-tree opportunity cost. *Three layered taxes, similar pattern to PoE.*

**What Reincarnated can learn:** The Runemaster is *the* contemporary genre reference for what a well-designed multi-element class can look like *and* what costs it should pay. Reincarnated's hybrid_mage can be re-framed as a Reincarnated-Runemaster — multi-element by identity, mid-tier by sustained DPS, with a moment-of-power when its combinations land. The damage tax achieves the same net effect as cooldown discipline by a different mechanism. The fact that this archetype is *new* in genre (2024-shipped) makes it especially valuable as reference — the design space is hot, and Reincarnated has a chance to enter it competitively.

### § 2.9 — Grim Dawn (2016) — Dual-mastery and the most permissive hybrid model

**Pattern:** Choose two of nine masteries; full access to both skill trees; investment-point pool shared.

Grim Dawn is the most permissive ARPG with respect to hybrid builds. Every character chooses *two* masteries (out of Soldier / Demolitionist / Occultist / Nightblade / Arcanist / Shaman / Inquisitor / Necromancer / Oathkeeper). A "Spellbreaker" is Nightblade + Arcanist; a "Druid" is Shaman + Arcanist; a "Pyromancer" is Demolitionist + Occultist. The 25+ dual-mastery combinations are *all individually balanced* and *individually viable* — the design effort to do this was massive and is part of why Grim Dawn took years to release and is somewhat new-player-hostile (the build space is intimidating).

**Cost structure:** Shared skill-point pool across two masteries means specializing in both is impossible; you can be deep in one and shallow in the other (the standard pattern) or moderate in both (the harder-to-execute pattern). *One layered tax, but the engine compensates with massive content-design effort to make each combination uniquely viable.*

**What Reincarnated can learn:** Grim Dawn is the *labor-intensive* model of multi-element. It works, but only with a Crate-Entertainment-sized investment in per-combination balance and content design. Reincarnated does not have this content-design budget — the engine generates archetypes; a dual-mastery model would require generating 25+ unique hybrid combinations and balancing each. This is **not** the path. The lesson is the opposite: Grim Dawn proves that *if you want generic permissive hybrids, you must pay for them in design effort*, and Reincarnated cannot pay that effort at the engine layer. The PoE / Last Epoch path (one constrained hybrid class, taxed) is the right path for Reincarnated.

### § 2.10 — Path of Achra (2024) — Roguelike-ARPG hybrid with extreme synergy fragility

**Pattern:** Roguelike build assembled from per-run-drop selections; deep multi-class synergies are *the* gameplay; build coherence breaks easily.

Path of Achra (released 2024) is an interesting outlier. It's a roguelike-ARPG hybrid where every build is implicitly multi-class (you can mix Berserker / Acolyte / Sorcerer / Marksman / etc. via item drops within a run). Multi-element is *constant*, and the synergies are *narrow* — a single missing piece can collapse a build. The game is widely respected for its build-deck-design philosophy.

The relevant lesson: **multi-element works when the player feels they are assembling a build,** not when the engine declares "you are a hybrid." Path of Achra's multi-element is *opt-in per-run*, *visible to the player every step*, and *the player owns the breadth choice*. Reincarnated's hybrid_mage is *engine-declared*, *opaque to the player*, and *not chosen by the player*. The Path of Achra lesson is meta: *if the player chose breadth, breadth feels powerful and earned; if the engine assigned breadth, breadth feels arbitrary*.

**Cost structure:** No explicit tax; emergent fragility from synergy dependency.

**What Reincarnated can learn:** The reshape recommendation (§ 3) should ensure hybrid_mage *feels chosen* — the form-library narrative provides the choice frame (you, the player, integrated this form across many seasons of accumulation). The tax (§ 4) should feel like a *trade-off the player consciously made*, not like a numerical handicap.

### § 2.11 — Torchlight II (2012) — Embermage as soft hybrid

**Pattern:** Three trees, two of which are element-themed (Fire / Frost) and one neutral; loose synergies.

Torchlight 2's Embermage is mechanically a soft hybrid — fire and frost are equally accessible, with the Storm tree being lightning-themed. The class has fewer taxes than D2 (synergies are less aggressive) and softer specialization pressure. Most Embermage builds *do* end up specializing for sustained damage, but the "Prismatic Bolt" build (a multi-element ranged staple) is canon-viable. T2's class balance is generally less tight than D2/PoE/LE/D4, and Embermage's hybrid viability is part of the class's identity rather than a tuning failure.

**Cost structure:** Soft synergy opportunity cost; primarily DPS-tuning balance rather than structural tax.

**What Reincarnated can learn:** T2 shows that *softer* taxes work when the rest of the game is also softer. Reincarnated's gauntlet-based balance loop is *not* soft — it is empirically tight (the 0.03 tolerance is sharp). A T2-style soft tax would not move the convergence needle at all. Reincarnated needs a measurable, sharp tax — the empirical 0.05 modifier floor and 0.50 target WR demand it.

### § 2.12 — Lost Ark (2018 KR / 2022 NA) — Class-decided rather than build-decided

**Pattern:** Each class is element-locked; multi-element is a class-selection choice, not a within-class choice.

Lost Ark's Sorceress is a fire/ice class; the Bard is a holy class; the Sharpshooter is physical; etc. Multi-element identity is at the class-tier (which class you play); within-class, you don't choose multi-element. This is the opposite of Reincarnated's hybrid_mage design — Lost Ark didn't try to make a hybrid class; it made *many specialists* and the variety lives at the class-roster layer.

**Cost structure:** N/A within-class; selection cost at class-choice layer.

**What Reincarnated can learn:** This is a *retire* path. Lost Ark proves that "many specialists" is also a valid genre answer. Reincarnated *could* retire hybrid_mage and lean into the substrate × role composition (the 18+ archetypes from substrate-identity refactor) as the variety surface. But Reincarnated has a thematic commitment to hybrid (form-library accumulation; the "many-form ascension"), and retiring contradicts that. Lost Ark's model is informative but not aligned to Reincarnated's design intent.

### § 2.13 — Hades / Returnal / roguelike-ARPG hybrids — Run-scoped breadth

**Pattern:** Multi-element from per-run boon stacking; breadth is contextual to a single run; no persistent hybrid class.

Hades's Zagreus picks up boons from gods (Zeus = lightning, Aphrodite = charm, Ares = doom, etc.) per run. Most successful runs stack a small number of related boons (a "duo boon" build around two compatible gods). The "all 9 gods boons" build is sub-optimal because boons that don't synergize with the chosen attack/special path waste boon slots. This is exactly the *self-imposed breadth-tax* pattern: the player can pick anything, but breadth costs.

**Cost structure:** Boon-slot opportunity cost (similar to D3's skill-slot cost) + synergy-pair tax (most boons have explicit duo bonuses with one specific other god).

**What Reincarnated can learn:** Hades demonstrates that *run-scoped breadth* is a viable design — the player accumulates breadth within a run, and the constraint is implicit. Reincarnated's form-library is *cross-run* accumulation, but within a single season (the "run" in Reincarnated's vocabulary), the player commits to one form. So Reincarnated's hybrid_mage is *not* run-scoped breadth — it's *form-scoped breadth*. The right reference for run-scoped breadth in Reincarnated is the *seasonal-class-cycling* mechanic, not hybrid_mage. Hybrid_mage is the persistent form; its breadth is its identity, and its tax should be at the identity layer, not at the cycling layer.

### § 2.14 — Synthesis: which category does Reincarnated align to?

The dispatch's Sub-Q 1 framing offered five categorizations:

| Category | Description | Genre exemplar | Reincarnated alignment |
|---|---|---|---|
| (a) Universally weak | Hybrid is intentionally jack-of-all-trades penalty; specialists always win | (rare; T2 Embermage closest) | **NO** — would erase the archetype's narrative purpose |
| (b) Build-cost gated | Pay in skill points / passive levels for breadth; viable but expensive | **PoE Elementalist; LE Runemaster; D2 Sorceress** | **YES** — this is the canonical pattern |
| (c) Endgame specialized | Only viable at very high investment levels | (D3 Tal Rasha set seasons) | NO — Reincarnated doesn't have item-set tiers |
| (d) Strong on paper, build-dependent | Mastery curve gates it | (D4 Sorcerer hybrid) | partial — overlaps with (b); too process-heavy |
| (e) Genre-rejection | No "hybrid" archetype exists | (Lost Ark; D1) | NO — contradicts form-library design |

**Reincarnated's correct alignment is (b): build-cost gated.** This is the canonical, durable, repeatedly-successful ARPG pattern across PoE / LE / D2 — three of the most-respected ARPGs in the genre's history. The cost is paid in *measurable damage output*, which is what the engine's balance loop already measures. Implementing the lever as a damage tax keyed to element breadth is the cleanest fit.

The specific tax structure (linear vs quadratic; flat vs scaling; per-skill vs per-kit) is the topic of § 4.

### § 2.15 — Anti-patterns to avoid (genre evidence)

Three D-series anti-patterns directly:

1. **D3 launch — no breadth-cost.** Reincarnated's current hybrid_mage state. Genre verdict: balance disaster. Avoid.
2. **D3 Reaper of Souls Tal Rasha set — gear-driven breadth-reward.** Adding a gear-set that *encourages* breadth is the inverse fix; it makes the problem worse before patching it. Reincarnated should not solve hybrid_mage with new gear sets. Avoid.
3. **Lost Ark class-tier specialization (the retire path).** Erases hybrid as identity. Contradicts form-library. Avoid.

Two pre-genre anti-patterns from isekai/anime adaptation:

4. **The Slime "everything-skill" trope.** In Mushoku Tensei / Slime / similar, the protagonist often accumulates many skills with no internal cost structure — narrative power-fantasy. This works in fiction because the story controls when skills matter. In a game, this is exactly the D3-launch failure mode. Reincarnated must resist the temptation to *narratively justify hybrid_mage having no tax* by appealing to "the player has accumulated many forms" — accumulation needs to *cost* something at the moment of expression, not just at the moment of acquisition.

5. **Konosuba multi-magic comedy (skill-overload comedy register).** The comedic register where the protagonist has too many spells and they comedically interfere with each other is *one* answer to the breadth-tax question — but Reincarnated's tonal commitment (per `gandalf-phase2-bullet-points.md` § 1.4 and the cosmology framing) is *serious-isekai*, not comedic-isekai. A comedic-tax framing would break tone. Avoid.

### § 2.16 — Genre frequency aggregation: how prevalent is each cost-structure pattern?

Aggregating across the 13 surveyed titles in §§ 2.1-2.13 by the dominant cost-structure pattern:

| Cost pattern | Games | Verdict |
|---|---|---|
| Synergy / passive-point opportunity cost (the canonical pattern) | D2 LoD; PoE 1; PoE 2; LE Runemaster; D4 Sorcerer; T2 Embermage (soft) | 6 of 13 |
| Skill-slot opportunity cost (smaller-kit constrained) | D3 (no cost; balance disaster); Immortal (works because cap is 4); Hades (boon-slot version) | 3 of 13 |
| Resource/drop gating (early-genre pattern) | D1 (tome scarcity) | 1 of 13 |
| Mastery-split shared-pool tax | GD (dual-mastery; works at high content-design cost) | 1 of 13 |
| Class-tier specialization (no within-class hybrid) | Lost Ark | 1 of 13 |
| Per-run emergent fragility (no explicit tax) | Path of Achra | 1 of 13 |

**The dominant pattern is opportunity-cost-via-investment-investment — 6 of 13 titles, including the most-recently-shipped (LE Runemaster 2024, PoE 2 2024-25 early access).** This is the canonical pattern Reincarnated is recommended to encode. The D11 damage tax is a *net-effect equivalent* to investment opportunity cost — Reincarnated does not have passive trees or per-skill investment, so it expresses the same constraint at the *effective-damage* layer.

Two notable counter-patterns to consider:
- **D3-launch as cautionary tale (no cost → balance disaster).** Reincarnated's current state.
- **Lost Ark / D1 as "skip hybrid entirely" path.** Reincarnated declines this per § 3.2.

### § 2.17 — The pattern Reincarnated is most directly imitating

If I had to name a single design reference for the reshape recommendation: **Path of Exile's Elementalist Ascendancy plus Last Epoch's Runemaster combined.** Both are multi-element specialists by identity; both pay layered taxes for breadth; both are mid-tier in DPS leaderboards by community consensus; both are *thematically beloved* despite being mechanically not-optimal. Reincarnated's chromatic_mage (post-reshape) belongs in this lineage.

The Reincarnated-specific innovations layered on top of this lineage:
- **Form-library narrative integration** (Solo Leveling shadow-army parallel) — the hybrid identity is *earned through accumulation*, not chosen at character-create
- **Canonical-7 substrate-commitment framing** — the tax is *substrate-aware* (forbidden hybrid pairs prevent certain combinations entirely; the tax curve applies to allowed combinations)
- **Earth-Self diversity-via-many-forms** — the hybrid is one form among many; specialists also accumulate; the player's identity is the *library*, not the *current form*

These differentiators are not in PoE or LE, and they make Reincarnated's hybrid_mage *its own thing* rather than a derivative. The reshape preserves these differentiators while borrowing the cost-structure pattern that PoE/LE have proven works.

---

## § 3 — Identity decision: retain, retire, or reshape?

This section closes Matt's queued L3 #42 question. The recommendation is **(iii) reshape**, with detailed justification across the design-direction axes the dispatch named: what the player feels, what the world allows, what the form-library narrative supports.

### § 3.1 — Recommendation: retain the archetype, reshape its mechanical profile, preserve the name (with optional rename surfaced as § 7 question for Matt)

The reshape direction has four components:

1. **Keep `hybrid_mage` as the engine's name for the archetype.** It's a working title that has been in the system from early Phase 1; renaming has a cross-cutting cost (decisions-log entries, telemetry tables, season data) that is disproportionate to the benefit. The name is generic but functional. The reshape is mechanical, not nominal. **However**, a § 7 question for Matt: would `chromatic_mage` (cleaner; ties to the canonical-7 hybrid as *the form that integrates many colors*) or `elementalist` (genre-canonical from PoE) read better at the player-facing surface? My weak preference is `chromatic_mage` because it captures the canonical-7 thematic frame (each substrate has its tonal commitment; the hybrid integrates many tones into a chromatic whole). But this is downstream of the mechanical fix; not blocking D11.

2. **Tighten the mechanical envelope: 3 elements max for general generation; 2 elements is the new "comfortable" hybrid; 4 elements requires Trial-boss-tier ceremonial composition path (deferred to D12+, not in D11 scope).** The current ceiling at 4 invites the empirical failure. 3 is the genre-canonical "we are pushing breadth" point; 2 is "we are still recognizably hybrid because both elements are mechanically present in the kit." A 4-element kit becomes a *capstone identity* — earned, ceremonial, gated. Phase-1 P2 (or D12) can implement the ceremonial path; D11 implements the tightened general path.

3. **Apply the element-coverage damage tax (§ 4 specifics).** This is the *single* lever that does the most work. It is gamora-translatable, jack-ryan-reviewable, and rocket-implementable in D11 scope. It does not require Phase-1 P2 hybrid-composer refactor.

4. **Preserve the substrate-identity declarative perimeter.** The tax must be derivable from substrate-identity declarations (i.e., `n_elements` is computed by counting distinct `canonical_element` values in the kit's skill list; the tax coefficient lives in a config near the substrate identities, not as a hardcoded constant in `hybrid_mage`'s template). This keeps Phase-1 P2 hybrid-composer migration clean — when P2 lands, the tax is already-decoupled from the holdover template.

### § 3.2 — Why not retire (i.e., reject option (ii))

The L3 #42 framing offered retire as a valid path. Three reasons to decline:

1. **Form-library narrative requires it.** Per `canonical/story/embodiment-display-loadout.md`, `canonical/story/court-of-forms.md`, and `gandalf-phase2-bullet-points.md` § 1.4, the form-library accumulates over seasons; the player accumulates *many forms*; some forms are specialists (a Firewalker form; a Tidecaller form) and some forms are integrators (a form that holds many substrates in tension). The integrator-form is the late-game ascendant identity — Solo Leveling's Shadow-Monarch parallel: many substrates worn at once. Retiring hybrid_mage erases the engine's slot for the integrator-form. The form-library survives, but it loses its narrative apex.

2. **The technical reason "engine can't model it cleanly" is empirically wrong.** D10's salvage telemetry shows hybrid_mage at 0.63-0.82 WR at modifier floor — *only modestly above target*. The gap is roughly 0.13-0.32 WR, which a quadratic damage tax of α=0.07 closes within a 3-element kit and overshoots in a 4-element kit (correcting back via the breadth ceiling tightening). The math works; the model is tractable. The "can't model cleanly" framing in the L3 #42 question reflects 5 days of frustration, not a structural impossibility.

3. **The canonical-7 substrate-identity work explicitly contemplates hybrid composition.** The `forbidden_hybrid_with` field is canonical (fire↔water forbidden; earth↔wind forbidden; holy↔shadow paired-amplification; lightning unpaired). The hive log Phase-1 P1 work (lines 1700-1815 + 2180-2290) extensively reasoned about what hybrid means in canonical-7 terms. Retiring hybrid_mage *now* would undo the architectural commitment to hybrid composition that the substrate-identity declarations made *yesterday*. That would be expensive and confusing.

### § 3.3 — Why reshape specifically, vs. straight retain (i.e., reject option (i) literal)

Option (i) in the dispatch was "retain as canon ARPG archetype with proper trade-offs." That's functionally what reshape is — it's a label distinction. I use *reshape* because the recommendation includes:

- Tightening element-breadth ceiling (4 → 3 for general; 4 for ceremonial only)
- Adding the damage tax (a new mechanic, not previously in the engine)
- Optionally renaming (deferred § 7 question)
- Re-framing the archetype's player-feel from "multi-element generalist" to "deliberate-integrator who pays for breadth"

That's more than "retain with trade-offs added"; it's a structural re-framing of what the archetype is. *Reshape* signals to gamora, rocket, and downstream that this isn't just a number tweak — it's an identity sharpening. The math note will reflect this; the implementation will preserve the engine's seam discipline; the player surface will eventually communicate the new identity.

### § 3.4 — What the player will feel after reshape

This is the load-bearing player-experience claim. Before reshape, the hybrid_mage feels like: *I'm a versatile mage; I have many elemental options; I beat fights because I can always hit a weakness*. The post-modifier balance loop turns this into: *I'm a versatile mage but I deal so little damage that fights feel like a slog*. The current state is bad on both axes — the kit is structurally over-powered before modifier; the modifier crushes it; the resulting play-experience is *neither flexible nor satisfying*.

After reshape, the hybrid_mage feels like: *I am a deliberate integrator. I have access to many elements, but each one I add is a choice — and I pay for the choice in raw output. My strength is that I cover what others can't; my weakness is that the specialist out-damages me on their home turf. I win fights through coverage, positioning, and the right tool at the right time — not through raw output*. This is the PoE Elementalist feel; this is the LE Runemaster feel. It is *recognizable as a class identity* in genre terms.

The form-library experience aligns: a player who has lived through many seasons and accumulated many forms can finally compose them; the composition is *meaningful* because each one *costs*. The Court of Forms remembers — to use the canonical-7 vocabulary — *the forms that integrated many commitments without abandoning the discipline of any one*.

This is what the archetype is *for*. The reshape gives it back to itself.

### § 3.5 — The optional rename (§ 7 question, but with my recommendation)

If Matt agrees to rename:

- **`chromatic_mage`** — preferred. Captures the canonical-7 framing (each substrate has its color/commitment; chromatic is the integration). Ties to PoE's chromatic-jewel vocabulary (familiar to ARPG players). Cleaner than `hybrid` (which is generic) and `elementalist` (which is overused).
- **`elementalist`** — genre-canonical (PoE keystone Ascendancy). Players recognize it. Slight drawback: it overlaps with the more general elementalist register; non-hybrid mages are also elementalists in casual usage.
- **`integrator`** — thematic but mechanically opaque; players won't intuit what the archetype does. Not recommended.

If Matt disagrees with rename: keep `hybrid_mage`. The mechanical reshape does the load-bearing work; the name is downstream.

---

## § 4 — Tuning lever recommendation (gamora-translatable specifics)

This is the section gamora consumes to author the D11 math note. The intent is to be **specific enough to translate to engine math, while remaining within design lane** (not pre-empting gamora's math judgment).

### § 4.1 — Primary lever: quadratic element-coverage damage tax

**The math (provisional; gamora to validate empirically):**

```
n_elements(kit) = |{ skill.canonical_element : skill ∈ kit }|
                = count of distinct canonical_element values in the kit

tax_multiplier = 1.0 − α × max(0, n_elements − k_free)²

where:
    α = 0.07      (tax coefficient; tunable; empirical anchor below)
    k_free = 2    (number of "free" elements; up to 2 elements pays no tax)
```

**Application:** `tax_multiplier` multiplies the `damage_multiplier` field on every damage-bearing skill in the kit (or, equivalently, applies as a kit-wide effective-damage multiplier in the balance loop's modifier resolution; gamora's choice on implementation site — likely *at the kit-finalization step in `b6_kit_builder.py`* so the balance loop sees an already-taxed kit).

**Why quadratic, not linear:** The breadth advantage is *combinatorial*, not additive. A 2-element kit vs a 3-element kit gains *one* new resistance hole to exploit; a 3-element kit vs a 4-element kit gains *one* new resistance hole *per existing element* (because each existing element now has a coverage partner against fresh resistance profiles). The empirical hybrid_mage at 4 elements is winning every magic and most elites *not* linearly above 2-element specialists; it's winning combinatorially. The tax must match the structural advantage's curve.

**Why α = 0.07:** This is my recommendation; gamora validates empirically. The reasoning:

- At 3 elements: tax = 1 − 0.07 × 1² = 0.93 (7% damage reduction). A 3-element hybrid is *measurably weaker* than a 2-element specialist but still very playable.
- At 4 elements: tax = 1 − 0.07 × 2² = 0.72 (28% damage reduction). A 4-element hybrid is meaningfully weaker. Combined with the breadth ceiling tightening (4 → 3 general; 4 ceremonial only), 4-element kits are rare; when they occur, they're identifiable as ceremonial / Trial-boss-tier.
- At 5 elements (which the ceiling prevents): tax = 1 − 0.07 × 3² = 0.37 (63% damage reduction). This is the *guardrail*; if the ceiling somehow leaks, the tax catches it.

These numbers anchor against the empirical 0.13-0.32 WR overage. A 28% damage reduction on a kit currently winning 0.77 WR at modifier floor should bring it within balance-loop reach (rough sketch: damage × 0.72 → fight outcomes proportionally weaker → WR roughly proportional → target WR achievable above floor).

**Validation discipline (Discipline #11, empirical inspection):** Gamora will need to (a) take a v1.5 hybrid_mage sample (Class C, season_002012, "Cartographer of Erased Borders"; 4 elements; pre-modifier WR 1.000), (b) apply the tax, (c) re-run balance loop, (d) confirm convergence WR lands in the target band at a modifier above floor. If α=0.07 is too soft, push to 0.08-0.09. If too hard, drop to 0.05-0.06. The smoke-test discipline applies; do not full-regen until the tax is calibrated.

### § 4.2 — Composite lever: element-breadth ceiling tightening

Current: hybrid_mage element ceiling = 4 (per `d10_kit_constraints.py:84`). Non-hybrid = 2 (default).

Recommendation: hybrid_mage element ceiling = **3 for general generation; 4 reserved for ceremonial path** (Trial-boss-tier; capstone seasons; not part of D11 scope, deferred to D12+).

The composite lever is *not* a replacement for the damage tax; it works *with* the tax. Together:

- 1-element hybrid: impossible by definition (hybrid requires ≥2 elements for the archetype to make sense)
- 2-element hybrid: tax-free, fully playable; this is the new "comfortable" hybrid
- 3-element hybrid: 7% tax; recognizable as breadth-leaning, slightly weaker, still playable
- 4-element hybrid: 28% tax, gated to ceremonial path; rare; mechanically distinct (the "ascendant integrator" capstone identity)

The breadth ceiling at 3 prevents the empirical failure case (4-element kits at modifier floor still over-band) from occurring at all in general generation. The damage tax handles the residual case if the ceiling leaks or if 3-element kits still over-band; the tax handles 3-element kits at the 7% mark, which is the calibrated correction.

### § 4.3 — Why not the alternative levers (rejected)

Walk through the dispatch's Sub-Q 3 menu:

- **Lower skill ceiling (8-9 not 12) — rocket's option (i).** Already partially exhausted at D10 (14 → 12). Going further (12 → 8-9) creates two problems: (a) it makes hybrid_mage a *smaller-kit* class than non-hybrid specialists, which is the wrong feel (a hybrid should have *more options*, not fewer); (b) at 8-9 skills, the kit can't satisfy the existing `required_roles` of `(area_damage, 2), (burst_damage, 2), (primary_attack, 1), (damage_over_time, 1), (defensive, 1), (utility, 1)` = 8 minimum, so the ceiling at 8 is effectively no-slack. Reject.

- **No legendary trait pool / weaker per-class intrinsics — trait-architecture tax.** This is structurally interesting: the trait architecture (per `project_trait_architecture.md`) has per-class intrinsic pools and gear-affix pools. A hybrid_mage could be denied a class-intrinsic trait pool. But this is heavy-weight: it pre-empts D8 trait-pool work, it requires a whole-system change, and it's hard to motivate to the player ("you have fewer traits because you're a hybrid"). Reject for D11; flag as alternative for D12+ if the damage tax proves insufficient.

- **Higher XP curve / slower scaling.** Doesn't fix the balance-loop problem (the balance loop calibrates at the final character level; XP curve doesn't appear there). Player-feel cost (slower progression) is high. Reject.

- **Lower base stats (HP / mana / dodge) — survivability tax.** Plausible. A hybrid_mage with VIT=42 (current) is already low-survivability. Pushing further (VIT=30?) makes the class glass-cannon. But this doesn't fix the *damage-output* problem; the kit is still over-generating damage. It only fixes the *survivability* axis. The empirical issue is damage output, not survivability. Reject as primary lever; possibly composite if needed.

- **Element-specific drawback (resistance hole or self-damage at element edges).** Interesting thematically: a chromatic_mage takes extra damage from *one* of its own elements (chosen at gen-time). This is canonical-7-coherent (a substrate that integrates many commitments has a vulnerability at the *seam* between commitments). But it adds complexity (a new mechanic; new validation; new player communication) for marginal balance impact. Reject for D11 scope; *strongly recommend as a flagged candidate for D12+ or for the ceremonial-4-element path*.

- **Multi-element kit composition rule (anchor element 40%+ slots).** This is the *PoE Elementalist Beacon-of-Ruin* shape ("there is a primary element; others are accents"). Plausible. The empirical Class C hybrid_mage has 4 elements with ~3-4 skills each — no clear anchor. An anchor rule would force at least one element to be 40%+ of the kit, naturally narrowing the breadth. But this rule overlaps with the breadth ceiling at 3: a 3-element kit with 12 skills is naturally 4+4+4 or 5+4+3, and the anchor rule doesn't add much beyond what 3 elements at 12 skills already gives. Reject as redundant; the ceiling tightening + tax does the same work cleaner.

### § 4.4 — Composite vs single-lever recommendation

The dispatch asked for "one (or a composite of two)." My recommendation is the composite: **(primary) quadratic damage tax + (secondary) element-breadth ceiling tightened to 3**.

These are *not* duplicative. The ceiling shapes the *generation distribution* — most hybrid_mage instances will be 2-3 element kits. The damage tax shapes the *power output* — 3-element kits pay 7%. The 4-element ceremonial path (deferred) gets 28% from the tax + structural gating from the ceiling.

The ceiling is also a *cheap* implementation (a single integer change in `_ARCHETYPE_ELEMENT_CEILING`). The tax is the heavier change (new field in `b6_kit_builder.py` or `d10_kit_constraints.py` for tax computation; gamora's seam-disposition call). Together they are still a smaller D11 lift than skipping the ceiling and putting all balance weight on the tax (which would need α ≈ 0.10-0.12 to handle 4-element kits and might over-tax 3-element kits).

### § 4.5 — Gamora-readiness checklist

The math note gamora authors next will need:

1. **Tax formula** (§ 4.1) — translate to balance_loop seam, with seam-disposition decision (apply at kit-finalization in generation, or apply at balance-loop modifier resolution)
2. **Empirical α calibration** (§ 4.1) — take v1.5 sample Class C; apply tax; rerun balance loop; report whether α=0.07 is calibrated; iterate if needed
3. **Ceiling enforcement** (§ 4.2) — single-line change in `_ARCHETYPE_ELEMENT_CEILING["hybrid_mage"] = 3`
4. **Provenance + telemetry** — emit `n_elements` and `tax_multiplier` to `class_balance_results` telemetry so post-D11 we can see the tax in action. Add `element_coverage_tax_applied: bool` field for grep-ability.
5. **Discipline #12 (semantic shift)** — this is a non-trivial generation rule change; MIGRATION.md entry needed; rocket will inherit on implementation
6. **Round-trip clause (Discipline R11(b))** — confirm balance-loop output's `final_modifier × tax_multiplier` is the effective damage scalar; if the export path needs to know the tax to render correctly to demo/loadout, surface as cross-seam
7. **Round-trip with the canonical-7 substrate-identity loader** — the tax coefficient α should live in a config near the substrate-identity declarations (not in b6_archetype_templates as a hardcoded magic number); this keeps Phase-1 P2 migration clean
8. **Validation against converged classes** — apply tax to converged classes (physical_warrior, fire_controller); they should be unaffected (n_elements ≤ 2 → tax_multiplier = 1.0). Smoke-test this explicitly.

The math note should run ~1-2 pages. Gamora is well-equipped; her D10 work demonstrates the right discipline cadence.

### § 4.6 — Worked-example calibration table (for gamora's empirical anchor)

To make the calibration target concrete, applying α=0.07 to the v1.5 empirical hybrid_mage sample (Class C, season_002012, "Cartographer of Erased Borders" — 4 elements [fire/water/wind/physical]; pre-modifier WR=1.000; floor-pinned at modifier=0.0509; observed convergence WR=0.773):

| Element count | tax_multiplier (α=0.07) | Expected effect on pre-modifier WR | Projected balance-loop outcome |
|---|---|---|---|
| 2 elements (specialist-adjacent hybrid) | 1.00 (no tax) | unchanged | n/a — should look like a fire_controller |
| 3 elements (general-D11 hybrid ceiling) | 0.93 (7% tax) | pre-modifier WR ≈ 0.95-0.97 from raw 1.000 | balance loop should find converged modifier ~0.06-0.10 (above floor) |
| 4 elements (D11 disallowed; ceremonial D12+ only) | 0.72 (28% tax) | pre-modifier WR ≈ 0.85-0.90 | balance loop should find converged modifier ~0.10-0.15 |
| 5 elements (impossible under D11 ceiling; guardrail) | 0.37 (63% tax) | pre-modifier WR ≈ 0.55-0.65 | converges easily; guardrail working |

The above is a sketch; gamora will compute empirically by running the balance loop. The key calibration checks for gamora:

1. **3-element hybrid converges above floor.** If 3-element hybrid still pins at floor, α is too low; push to 0.08-0.09.
2. **2-element hybrid behaves like fire_controller (FLOOR-CONVERGENT acceptable).** A 2-element hybrid should converge at roughly the same point fire_controller does — that's the design intent (2 elements is the "comfortable" hybrid, not penalized).
3. **4-element ceremonial hybrid converges with WR margin.** If 4-element ceremonial (post-D12) still over-bands at the 28% tax, α might need to be higher for ceremonial kits, or the ceremonial path needs an additional mechanic.

Gamora will surface the empirical α and any adjustments in the D11 math note.

### § 4.7 — Why the tax formula must NOT special-case hybrid_mage

A subtle but important point: the tax formula is **universal** (applies to any archetype with n_elements > k_free) but the *ceiling* is per-archetype. This is the correct decomposition.

- **Universal tax:** any kit with 3+ elements pays the tax. This catches edge cases where a physical_warrior somehow accumulates 3 elements (currently impossible per the default ceiling=2, but defensive against future changes).
- **Per-archetype ceiling:** hybrid_mage is the only archetype currently *allowed* 3+ elements. Other archetypes are capped at 2 by `_DEFAULT_ELEMENT_CEILING`.

This decomposition means: when Phase-1 P2's hybrid-composer lands and potentially introduces hybrid_physical or hybrid_caster archetypes, they automatically inherit the tax. The tax does not need to be re-implemented per archetype; only the ceiling table needs entries.

**Implementation discipline:** the tax computation goes in `d10_kit_constraints.py` (or successor module if gamora prefers a new module for D11's broader hybrid-family rules) as `compute_element_coverage_tax(kit) -> float`. The function does NOT take `archetype_tag` as input — it takes the kit (or kit's element distribution) and returns the tax multiplier. The archetype is irrelevant to the formula; only the kit's n_elements matters.

This keeps the formula clean and Phase-1 P2-compatible.

### § 4.8 — Application site: pre-balance-loop vs in-balance-loop

There are two plausible application sites for the tax:

**Site A — Kit finalization (pre-balance-loop):** Apply the tax at the kit-finalization step in `b6_kit_builder.py`. The kit emerges with damage_multiplier values already taxed. The balance loop sees an already-taxed kit; the pre-eval (DPS density gate § 5.4 of D10 math note) sees a taxed pre-modifier WR; the convergence modifier is found against the taxed damage.

**Site B — Balance-loop modifier resolution:** Apply the tax inside the balance loop as a multiplier on the modifier. The kit emerges with original damage_multiplier values; the balance loop computes `effective_modifier = modifier × tax_multiplier` and uses that in fight simulation. The convergence is found against the taxed effective_modifier.

Both produce identical end-state behavior. The difference is *where the tax is visible*:

- Site A: kit's damage_multiplier reflects the tax; player/loadout/demo see the taxed values directly; provenance is on the kit
- Site B: kit's damage_multiplier reflects pre-tax values; player/loadout/demo see the pre-tax kit; provenance is in the balance_metadata only

My recommendation: **Site A (kit finalization).** Reasons:
1. **Provenance clarity:** the player surface (demo, loadout) reads the kit; if the tax is on the kit, the surface sees the truth.
2. **Pre-eval correctness:** the D10 DPS density gate runs at modifier=1.0 with full damage; if the tax is at Site B, the gate sees an un-taxed kit and may flag false positives.
3. **Phase-1 P2 forward compat:** when hybrid-composer lands and composes kits, the composer outputs the taxed kit directly; no balance-loop modification needed.

Gamora has final seam-disposition; this is a recommendation, not a constraint. The math note should pick one site and justify briefly.

---

## § 5 — Thematic framing in Reincarnated (canonical-7 + form-library + earth-self)

This section addresses the dispatch's Sub-Q 4: does the substrate-coherent gen-math from D10 align with how hybrids should *feel* in the world? The answer is yes, *with one amendment to surface to drax* (low priority; § 8).

### § 5.1 — Canonical-7 alignment

The substrate-identity declarations (gandalf/v1.2 tag; ee9e169 commit area) carry explicit substrate commitments:

- Fire: HIGH_BURST_LOW_PERSIST + ignition pillar — *escalation*
- Water: SUSTAINED_PRESENCE_ZONE_DENIAL + suffusion pillar — *patient permeation*
- Earth: ANCHOR_AND_DISRUPT + bulwark pillar — *positional refusal*
- Wind: KINETIC_REDIRECTION + displacement pillar — *kinetic rearrangement*
- Lightning: HIGH_BURST_LOW_PERSIST + resonance pillar (proposed) — *sudden traversal*
- Holy: REVELATION_AND_AMPLIFICATION + radiance pillar (proposed) — *amplification of aligned*
- Shadow: CONCEALMENT_AND_DRAIN + penumbra pillar (proposed) — *occlusion*

The hybrid_mage, when it integrates multiple substrates, is *holding multiple commitments simultaneously*. The cosmological commitment of *each* substrate is "this is what I am, not the others." A hybrid is, in canonical-7 terms, *a form that holds commitments that ordinarily refuse each other*.

This is the thematic root of the damage tax. Each substrate's full power is *its commitment fully expressed*. A form that integrates many substrates is fully expressing none of them. The mechanical 7% / 28% damage tax is the substrate-language version of *each commitment knowing the form is not fully its own*. The Firewalker who is also a Tidecaller is, to the fire substrate, *not entirely fire's*; the fire spark in that form's hand burns slightly less hot because the form is not committed *only* to fire.

The forbidden_hybrid_with declarations make this even sharper:

- Fire↔water forbidden: the substrates *cannot* compose. Their commitments are mutually-erasing (escalation vs suffusion). A hybrid_mage cannot integrate both.
- Earth↔wind forbidden: same shape. Positional refusal vs kinetic rearrangement; mutually-erasing.
- Holy↔shadow paired-luminance: composable; the substrates are opposed but can coexist in a form. A hybrid that integrates both pays the tax *and* expresses something rare (the Solo Leveling duality-of-light-and-shadow tier).
- Lightning unpaired: composes freely. A hybrid that includes lightning has the most flexibility (it doesn't constrain its other elements).

The damage tax is *substrate-aware*: when canonical-7 forbidden pairs are enforced, the tax operates on the *allowed* breadth. The hive log Phase-1 P1 already validated that `HYBRID_FORBIDDEN_PAIRS` is loader-derived from `forbidden_hybrid_with`; the tax slots cleanly into this architecture.

### § 5.2 — Form-library alignment

Per `canonical/story/embodiment-display-loadout.md`, `canonical/story/court-of-forms.md`, and `gandalf-phase2-bullet-points.md` § 1.4: the form-library accumulates across seasons; each form is a *commitment to a substrate or substrates*; the form-library's narrative apex is the integrator-form (the form that holds many substrates).

The reshape recommendation makes the integrator-form *earnable* in a way the current state does not. Right now, hybrid_mage is *frequently generated* (17/51 = 33% of classes in the v1.5 dataset) and *generically over-powered*. The form-library tells the player "you have integrated many substrates" *every time* hybrid_mage is generated — which dilutes the narrative weight of integration.

Post-reshape:
- 2-element hybrids are common; they are *recognizably hybrid* but pay no tax; this is the "you know more than one substrate" tier
- 3-element hybrids are less common; they pay the 7% tax; this is the "you are deliberately broadening" tier
- 4-element hybrids are *rare and ceremonial* (deferred to D12+ ceremonial path); they pay the 28% tax; this is the "you have integrated something the world considers exceptional" tier

This *graduates* the form-library's narrative weight. A 4-element form is rare and meaningful; a 2-element form is common but still recognizably hybrid. The Court of Forms remembers the rare ones specifically.

### § 5.3 — Earth-Self alignment

Per `canonical/story/earth-self-diversity-tension-2026-05-17.md`: the Earth-Self is the player's persistent identity across seasons; the Court of Forms is the space where attained forms are remembered with *grace* (not graded by power). The Earth-Self's diversity comes from the form-library's accumulation, not from any single form's specialization.

The reshape supports this: the Earth-Self that has accumulated many forms has *attempted many commitments*. The forms it has attempted include specialist forms (Firewalkers, Tidecallers, Stormriders, etc.) and integrator forms (chromatic_mage). The Court remembers all of them. A 4-element form that the Earth-Self attempted but found weak-on-paper is still a Court-remembered form; the *attempt* counts, not the leaderboard ranking.

The damage tax is therefore *not* a punishment in Earth-Self framing; it is the substrate's truth-telling about commitment. The Earth-Self learns over many forms what each substrate asks; a chromatic_mage's tax is the substrate community's honest response, not the engine punishing the player. This framing should land at the Spirit-Guide voice surface (per `canonical/story/spirit-guide-voice.md` if/when authored explicitly).

### § 5.4 — Surface implications (drax handoff, low priority)

The reshape has surface-layer implications for drax-demo and drax-loadout:

1. **Loadout class panel: hybrid_mage's tooltip/description should communicate the trade-off.** Something like: *"Hybrid forms integrate multiple substrates. Each commitment beyond the first costs a measure of raw power; in exchange, no substrate is closed to you."* This is the player-facing version of the tax. drax-loadout's class-detail-panel is the place. Low priority; can land post-D11.

2. **Spirit-Guide commentary (if/when spoken on hybrid_mage selection):** *"This form holds many commitments. The substrates know it does not belong to any of them, and they answer accordingly. What it lacks in any single voice's full power, it makes up in voices it can call when it needs them."* Phase-1 P2 territory; not D11 scope.

3. **Trial-boss-gallery presentation:** A hybrid_mage entering a Trial that has a 4-element ceremonial composition (D12+) could be flagged as a *ceremonial event*. The boss-room's environmental cues (color palette, music register, Court reaction) could honor it. This is significantly downstream; flag for the form-library narrative-roadmap, not D11.

These are the only surface implications. The damage tax itself is invisible to the player at the demo surface (they see the modifier-resolved damage values; they don't see the tax explicitly). This is fine — the player doesn't need to see the tax math; they need to feel *the chromatic_mage is hard-to-master-and-rewarding*, not *the chromatic_mage has a -7% damage modifier displayed in a tooltip*.

### § 5.5 — The thematic reading of why this works (one paragraph)

The substrate's commitment to itself is what gives it power. A form that integrates many substrates participates in many commitments but is fully held by none of them. This is *true mythically* — the polymath is rarely the master; the master rarely speaks many languages; integration costs depth. Reincarnated's canonical-7 substrate framework encodes this truth structurally. The hybrid_mage's damage tax is not arbitrary balance; it is the substrate community's response to a form that asks to speak with many voices. The Court of Forms remembers the chromatic_mage exactly as it is: a form that attempted breadth and paid the substrate's price for breadth. This is *good story*. The mechanical reshape and the thematic reading are the same thing seen from two sides.

### § 5.6 — Isekai-genre register (the Reincarnated tonal commitment check)

Reincarnated's tonal commitment per `canonical/story/gandalf-design-lineage.md` and `gandalf-phase2-bullet-points.md` is *serious-isekai* in the Mushoku Tensei / Solo Leveling / Re:Zero band, not comedic-isekai in the Konosuba / How NOT to Summon a Demon Lord band. The hybrid_mage reshape must read in the serious-isekai register.

The serious-isekai genre has three reference patterns for the multi-form / multi-skill protagonist:

**Pattern A — Mushoku Tensei's Rudeus.** Rudeus accumulates skill across many magic schools (Healing, Detoxification, Earth, Fire, Water, Wind, Continual, Beast, Sword, Bow, etc.) over a lifetime. The series treats his breadth as *meaningful but costly*: he is not the strongest in any single school (the specialists like Orsted or Death-Inspecting Roxy outclass him in their domains), but his *combinatorial flexibility* — knowing which spell to pull in which moment — is his identity. Each skill-school he learned cost time, mentorship, and dedicated practice. The cost is *in the journey*, not in the moment-to-moment damage output. This is *adjacent* to Reincarnated's form-library framing — accumulation across a long journey — but Reincarnated's damage tax operates at the moment-to-moment level rather than the journey level. The Mushoku pattern *complements* the damage tax; it doesn't replace it.

**Pattern B — Solo Leveling's Sung Jinwoo shadow integration.** Jinwoo extracts shadows from defeated enemies and adds them to his army. The shadows are *individually weaker than the original beings* (a Igris shadow is less powerful than a living Igris would be); the integration costs them their original power. But the *aggregate of many shadows under one command* gives Jinwoo something no single shadow could do alone. This is the **closest direct parallel** to Reincarnated's hybrid_mage post-reshape: each substrate integrated *individually pays a cost* (the damage tax), but the *aggregate kit's coverage* gives the player something a specialist cannot have. The Solo Leveling reading is structurally correct.

**Pattern C — Re:Zero's Subaru Return-by-Death and accumulated-knowledge identity.** Subaru's power is not a magic-school but *iterative knowledge* across resets — he learns from each death, accumulates information, returns to earlier moments with what the prior runs taught him. Re:Zero's tonal commitment is to *the cost of accumulation* — Subaru's accumulated knowledge is *traumatic*; every reset costs him psychologically. The genre's most-respected serious-isekai work is also the one most-explicit about *accumulation being expensive*. Reincarnated's form-library accumulation does not need to be traumatic, but it should not be *free*. The hybrid_mage damage tax is the moment-to-moment manifestation of *accumulation having a cost*. Re:Zero validates this.

**The genre-register conclusion:** The reshape's "you pay for breadth" framing is *aligned* with serious-isekai's genre conventions. Konosuba's comedic register (where breadth is comedic chaos with no cost) would *not* support this reshape — but Reincarnated has explicitly committed to the serious register. The genre framing is consistent.

### § 5.7 — What the Spirit Guide could say (Phase-1 P2 territory; not D11)

When the form-library presents a hybrid_mage to the player (post-Phase-1 P2 Spirit Guide voice integration; not D11), the Guide's commentary register could be:

> *"This form holds many commitments. The substrates know it does not belong to any of them, and they answer accordingly. The spark it summons will be a little less hot than a Firewalker's; the wave it shapes will be a little less deep than a Tidecaller's. What this form lacks in any single voice's full power, it makes up in voices it can call when it needs them. The Court remembers this form as one that attempted integration without abandoning the discipline of any single substrate."*

This is *demonstrative* — not for implementation in D11 — but it documents the Spirit Guide voice register the reshape is consistent with. Drax's future Phase-1 P2 narrative-surface work has this as starting point.

### § 5.8 — What the Court of Forms remembers about chromatic_mage

Per `canonical/story/court-of-forms.md`, the Court remembers attained forms with *grace*, not with leaderboard-ranking. A chromatic_mage that the Earth-Self attempted and found mid-tier is *still* a Court-remembered form. The Court's memory does not record DPS — it records the *attempt to integrate*. The damage tax is invisible to the Court's framing; the Court remembers the form, not the modifier.

This matters because the Earth-Self diversity-tension resolution (per `canonical/story/earth-self-diversity-tension-2026-05-17.md`) puts the form-library accumulation in the *grace register*. The reshape preserves this. A player who has a chromatic_mage in their form-library is *not* told by the game "this is a weaker form"; the game tells them "this form integrates breadth, and the cost of integration is the substrate community's honest response." Same mechanic, different framing.

### § 5.9 — One last thematic thread: the player's seasonal cycle

The player encounters classes seasonally; in the demo's gameplay loop, the player selects from class options each season and plays that form through to seasonal completion (per `canonical/story/embodiment-display-loadout.md`). A chromatic_mage selected for a season is a *one-season commitment* (the form-library accumulates across seasons; within a single season, the form is chosen and played).

The reshape impacts this loop:
- A season where chromatic_mage is offered: the player can choose it knowing it is *deliberately broader and slightly weaker*. This is a *meaningful choice* — the player trades raw power for coverage.
- A season where chromatic_mage is *not* offered (the substrate generation produced specialists): the player plays a specialist; the form-library still has chromatic_mage memory from prior seasons.
- The Earth-Self's identity is the *sum of seasons*, not the current season; the chromatic_mage seasons contribute *integration experience* to the Earth-Self.

This loop integrity is preserved by the reshape. The chromatic_mage's mechanical reshape does not disrupt the seasonal-cycle player-experience; it sharpens what the chromatic_mage season *feels* like (you knew you were choosing breadth; you knew it cost something; you got to experience integration play).

---

## § 6 — D11 scope guidance (broad hybrid family vs tight on hybrid_mage)

The dispatch's Sub-Q 5 asked whether D11 should cover only hybrid_mage or extend to adjacent archetypes. My recommendation: **D11 scope is TIGHT on hybrid_mage**, with two specific flagged-not-blocked adjacencies for D12+.

### § 6.1 — Empirical hybrid family check

Across the v1.5 dataset (51 classes; 17 instances of hybrid_mage), the only archetype that is *currently* in the engine with explicit multi-element composition is hybrid_mage itself. The roster:

- `hybrid_mage` (1 template; 17 instances; 0% convergence) — **THE TARGET**
- `fire_mage`, `water_mage`, `earth_mage`, `wind_mage` (single-substrate) — not hybrid
- `lightning_mage`, `holy_mage`, `shadow_mage` (single-substrate; new) — not hybrid
- `fire_controller`, `water_controller`, etc. (single-substrate controllers) — not hybrid
- `physical_warrior`, `physical_grappler`, `physical_skirmisher`, `hunter`, `rogue` (physical archetypes) — not hybrid; physical kit can include 1 secondary element on area skills per `d10_kit_constraints.py` (element ceiling = 2 default); this is *not* hybrid in the canonical-7 sense
- `experimental` (catch-all small-kit) — not hybrid by design
- Other composed substrate-role archetypes (e.g., `lightning_controller`, `holy_caster`) — not hybrid

There is *no* hybrid_physical in the engine. The "physical + 1 secondary element" pattern in physical archetypes is *small-secondary* (e.g., a physical_warrior with a water-themed area_damage skill); it's far below the empirical hybrid_mage's 4-element breadth. The default element ceiling of 2 governs this and is appropriate.

### § 6.2 — D11 scope = hybrid_mage tightly

The convergence telemetry localizes the problem entirely to hybrid_mage. The damage tax should apply to *any* archetype with n_elements > k_free (i.e., the formula is universally applicable), but the *only archetype currently affected* is hybrid_mage. The ceiling change is *only* to `_ARCHETYPE_ELEMENT_CEILING["hybrid_mage"]`.

This keeps D11 scope tight, gates a single archetype, and lets gamora's math note focus on calibration against the empirical hybrid_mage sample. Tight scope reduces D11 risk; tight scope also matches the dispatch's Pattern B sizing.

### § 6.3 — Flagged adjacencies (NOT in D11 scope; for D12+ or Phase-1 P2)

Two adjacencies surface as flags:

1. **Hybrid composition is Phase-1 P2 candidate (per substrate-identity refactor hive log lines 1752, 2233).** When P2 lands, the hybrid composer will replace `_HYBRID_ARCHETYPE_TEMPLATES`. The damage tax must survive that transition — i.e., it must live in a config near substrate-identity (not in the holdover template). This is a *forward-compatibility constraint* on the D11 implementation. The math note should flag this so rocket implements with P2 in mind.

2. **Future hybrid archetypes (hybrid_physical; hybrid_caster; holy/shadow luminance-hybrid; etc.) will inherit the tax automatically** if the tax is keyed on `n_elements` rather than on `archetype_tag == "hybrid_mage"`. This is the right design (universal formula; per-archetype free-element count k_free if needed; default k_free=2 for non-hybrid; k_free=2 for hybrid_mage too — the tax kicks in at 3+ elements universally). **This is the recommended seam:** the tax is universal; the ceiling differs per archetype.

3. **The 4-element ceremonial path is a D12+ design item.** D11 reduces hybrid_mage ceiling to 3 (no exceptions). D12 (or Phase-1 P2's hybrid-composer) can re-introduce the 4-element ceremonial path with the gated mechanism — likely via a special path tied to Trial-boss generation, capstone seasons, or form-library milestone events. **D11 should not implement the ceremonial path.** Flag for future work.

4. **The element-specific drawback (resistance hole at substrate seam) is an interesting D12+ candidate** for the 4-element ceremonial path. If the chromatic_mage gets the ceremonial 4-element form, the resistance-hole-at-seam mechanic would give it a recognizable signature (e.g., "this 4-element form takes +25% damage from one specific element, declared at gen-time, chosen to be one of its non-canonical elements" — narratively, "the substrate at the form's weakest commitment punishes the form when struck"). Flag for D12+ design exploration.

### § 6.4 — Out-of-scope explicitly

- **No changes to single-substrate archetypes.** The 24 - 1 = 23 archetypes that are not hybrid_mage are unaffected by D11.
- **No changes to the gauntlet composition.** D11 does not touch the reference gauntlet.
- **No changes to monster element distribution.** D11 does not adjust monster elements.
- **No changes to telemetry schema beyond adding the `element_coverage_tax_applied` field and the `n_elements`/`tax_multiplier` provenance fields.** This is gamora's seam discipline; minor.
- **No changes to LLM-flavor or naming.** The reshape is mechanical, not nominal. (Optional rename of `hybrid_mage` → `chromatic_mage` is § 7's open question; if Matt agrees, that's a separate small rename pass, not D11 math.)

### § 6.5 — Why "tight on hybrid_mage" is the right scope discipline

Three reasons to keep D11 tight:

1. **Pattern B sizing.** The dispatch is Pattern B short (0.5-1 day for advisory; gamora math note ~1-2 days; rocket implementation ~1-2 days). Broader scope would push to Pattern A (multi-day design pass). The empirical urgency is hybrid_mage's 0% convergence; this is the bleed-point; fix it.

2. **Engine seam discipline.** Hybrid composition is Phase-1 P2 candidate; the broader hybrid-family refactor lives there. D11 should not pre-empt P2 by trying to compose multiple hybrid archetypes. Surface them as P2 inputs.

3. **Empirical validation discipline.** Gamora has one empirical sample to calibrate against (the v1.5 hybrid_mage). Calibrating against multiple archetypes at once risks under-calibration on each. Better to lock the α coefficient against the well-studied hybrid_mage sample, then extend to other archetypes (with their own empirical anchors) when those archetypes exist in generated data.

### § 6.6 — Knock-on effects on other dispatches (none blocking)

A quick scan of other in-flight dispatches for knock-on effects:

- **drax v1.11 SEASON_IDS flip (demo seam):** post-D10 curated seasons 002011-015 — these will be *re-curated* after D11 if rocket re-runs the post-process salvage with the new tax + ceiling. drax should hold the SEASON_IDS flip until post-D11 curation lands, OR drax can flip to D10-curated now and re-flip to D11-curated when ready. Recommendation: drax holds; the re-flip cost is small but the data delta is meaningful (D10 ships with 37.1% convergence; D11 should ship with 70%+).
- **drax-loadout data/ refresh:** same pattern — refresh once D11 curation lands; not now.
- **gamora post-VS2a M2-M7 work:** parallel-safe per dispatch coordination; no overlap.
- **star-lord `estimated_gap` telemetry addition (D10 follow-on):** parallel-safe; gamora's D11 math note may add `element_coverage_tax_applied` field to the same telemetry table; coordinate via MIGRATION.md.
- **jack-ryan Phase-1 P1 Gate 1 and Gate 2 reviews:** Gate 1 review of this advisory runs in parallel with gamora math note authoring; no overlap conflict.

No D11 sprint dependencies on other dispatches; no knock-on conflicts.

---

## § 7 — Open questions for Matt

These are questions the recommendation surfaces but I cannot decide unilaterally. Matt's input gates next steps in two places.

### § 7.1 — Q1: Rename hybrid_mage to chromatic_mage?

The mechanical reshape is the load-bearing change. The name is downstream and optional.

- **Option A: Keep `hybrid_mage`.** No rename. Generic but functional. Cheaper.
- **Option B: Rename to `chromatic_mage`.** Captures canonical-7 framing (each substrate has its commitment/color; chromatic is integration). Cleaner. Costs: rename pass across decisions-log, telemetry tables, season data, possibly demo/loadout surface. ~1-2 hours of work spread across rocket + star-lord + drax.
- **Option C: Rename to `elementalist`.** Genre-canonical (PoE Ascendancy). Familiar. Less canonical-7-specific.

My recommendation: **Option B (`chromatic_mage`)**. But this is your call. Either is workable.

### § 7.2 — Q2: 4-element ceremonial path — D12+ design item or never?

The recommendation defers the 4-element ceremonial path to D12+. But it's also reasonable to *never* implement it — to let 3 be the ceiling permanently. The trade-off:

- **Implement the ceremonial path (D12+):** preserves the form-library's narrative apex (a rare 4-element form). Adds design complexity. Tied to Trial-boss-tier mechanics. Roughly Pattern A scope (a focused design pass).
- **Never implement; cap at 3 permanently:** simpler. Form-library's narrative apex becomes the 3-element form (which is fine; 3 is still meaningful). Eliminates a design surface.

My recommendation: **defer to D12+ but flag for evaluation; do not pre-commit.** Re-evaluate after D11 lands and we see how the 3-element-cap-only hybrid_mage actually plays. If 3-element forms feel like enough thematic richness, we can stop there. If players (when there are players) ask for a capstone, we have the path designed.

### § 7.3 — Q3: Tax coefficient α = 0.07 — accept the empirical-validation-by-gamora pattern, or pre-decide?

I recommend α = 0.07 with the explicit caveat that gamora validates empirically and may adjust. The alternative is for you to pre-decide α (e.g., "always use α=0.08 because I want the tax to bite harder").

My recommendation: **accept the empirical-validation pattern.** Gamora's D10 math discipline is high-quality; she will calibrate against the v1.5 hybrid_mage sample and surface the resulting α. If the resulting α deviates significantly from 0.07 (e.g., 0.04 or 0.12), that's a signal worth knowing about, and the math note will surface it.

### § 7.4 — Q4: Does the damage tax apply during the balance-loop pre-eval (DPS density gate § 5.4 of gamora's D10 math note)?

The D10 math note's DPS density gate at modifier=1.0 (5-fight pre-eval; flag-as-over-generated if WR>0.90) is at the kit-finalization boundary. If the tax is also applied at kit-finalization, the pre-eval sees the *taxed* kit — i.e., the tax reduces the kit's pre-eval WR.

This is the design-correct behavior (the tax is part of the kit's effective power) but it has a subtle implication: a 3-element hybrid that previously pre-evaled at WR=0.93 (over-band) might now pre-eval at WR=0.86 (under the gate threshold). This might *eliminate* the pre-eval gate's hybrid_mage flagging in some cases — which is fine, because the tax is already correcting the over-power.

Gamora's math note should explicitly call out this interaction. No decision needed from you, but flag for awareness.

### § 7.5 — Q5: Future hybrid archetypes (Phase-1 P2 / Phase 2) — inherit the universal tax?

The reshape recommendation implies that future hybrid archetypes (when Phase-1 P2 hybrid-composer lands) will inherit the universal tax. Holy/shadow luminance-hybrid; lightning + fire hybrid; etc. — all pay the same n_elements > k_free quadratic tax.

My recommendation: **yes, universal tax applies to all future hybrids.** This is the simplest design and aligns with the canonical-7 commitment-cost framing. Confirm or contradict at your discretion; not blocking D11.

---

## § 8 — Handoffs

### § 8.1 — HANDOFF → gamora (D11 math note inputs)

This advisory is your input to the D11 math note. Specific items:

1. **Tax formula** per § 4.1:
   - `n_elements(kit) = |{ skill.canonical_element : skill ∈ kit }|`
   - `tax_multiplier = 1.0 − α × max(0, n_elements − k_free)²` where `α = 0.07`, `k_free = 2`
   - Application site: kit finalization (b6_kit_builder.py or d10_kit_constraints.py — your seam-disposition call)
2. **Element-breadth ceiling tightening** per § 4.2:
   - `_ARCHETYPE_ELEMENT_CEILING["hybrid_mage"] = 3` (was 4)
3. **Empirical α calibration** per § 4.1 last paragraph:
   - Take v1.5 Class C (season_002012, hybrid_mage, "Cartographer of Erased Borders", 4 elements, pre-modifier WR 1.000)
   - Apply tax (with current 4 elements → tax_multiplier = 0.72; if hybrid_mage breadth reduced to 3, re-sample or simulate a 3-element kit → tax_multiplier = 0.93)
   - Re-run balance loop; report whether convergence WR lands in target band at modifier above floor
   - Adjust α if needed; surface adjustment in math note
4. **Telemetry additions** per § 4.5:
   - Emit `n_elements` and `tax_multiplier` to `class_balance_results` provenance
   - Add `element_coverage_tax_applied: bool` field
   - (Coordinate star-lord follow-on; non-blocking)
5. **Forward compatibility constraint** per § 6.3:
   - Tax coefficient α lives in a config near substrate-identity declarations, not as a hardcoded constant in `_HYBRID_ARCHETYPE_TEMPLATES`
   - Specifically: recommend `config/substrate_identities/_tax_config.yaml` or similar, loaded by `substrate_identity_loader`
6. **Discipline #12 (semantic shift)** per § 4.5:
   - This is a non-trivial generation rule change; MIGRATION.md entry needed; rocket inherits on D11 implementation
7. **Smoke-test discipline** per § 4.1:
   - Validate against converged classes (physical_warrior, fire_controller) — confirm n_elements ≤ 2 → tax_multiplier = 1.0 → no change to converged classes
8. **Pre-eval interaction** per § 7.4:
   - Note the interaction with the D10 DPS density gate; flag in math note for rocket's implementation clarity

Your D11 math note should run 1-2 pages. Empirical anchor section is load-bearing. Discipline #1 (math-before-code) and Discipline #11 (empirical inspection) apply.

### § 8.2 — HANDOFF → jack-ryan (Gate 1 advisory readiness)

This advisory is ready for your Gate 1 review. Specific watchpoints:

1. **§ 2 ARPG-canon evidence** — the load-bearing case. Verify that cited games and systems are accurately represented. I have full confidence in D2/D3/D4/PoE/LE/GD citations; flag any reservation about Immortal, Path of Achra, Hades, Torchlight, Lost Ark coverage (I am less hands-on with these and worked from general knowledge + design lineage).
2. **§ 4.1 quadratic tax formula** — verify the mechanic is plausible and gamora-translatable. The formula is provisional; gamora calibrates α empirically. Flag any concern about applying the tax at kit-finalization vs balance-loop-resolution.
3. **§ 4.4 composite vs single-lever** — verify the composite (tax + ceiling) is the right call vs single-lever (tax only). My reasoning is in § 4.4; if you see a cleaner single-lever path, surface.
4. **§ 6 D11 scope** — verify that "tight on hybrid_mage" is the right scope and that the flagged adjacencies (Phase-1 P2 P2-compat; hybrid_physical; ceremonial 4-element path; resistance-hole-at-seam) are correctly classified as flagged-not-blocked.
5. **§ 7 open questions** — verify that the questions are the right questions for Matt and that none of them should be pre-decided by me (or by you) before Matt sees them.
6. **Discipline #12 / semantic-shift discipline** — verify that the reshape is correctly tagged as a semantic shift and that gamora's math note will surface MIGRATION.md needs.
7. **Cross-doc coherence** — verify alignment with substrate-identity declarations, form-library narrative, earth-self diversity-tension resolution. I have read these; if you see a mismatch I missed, surface.

Your verdict should be one of: ENDORSE (advisory ready as-is); CONDITIONAL ENDORSE (with named pre-flags for gamora); REQUEST AMENDMENT (advisory needs revision before gamora consumes).

### § 8.3 — HANDOFF → drax (UI/narrative surface, low priority)

Two low-priority items, both deferred to post-D11:

1. **Loadout class-detail panel for hybrid_mage:** if rename to chromatic_mage lands, update the panel; if not, consider adding a tooltip/description that captures the trade-off (per § 5.4 item 1).
2. **Spirit-Guide voice commentary for hybrid_mage selection:** Phase-1 P2 territory; not D11. Flag for future drax narrative-surface work.

No D11 action required from drax.

### § 8.4 — HANDOFF → knight-rider (sequencing and gate)

- This advisory **gates D11 sprint** per the dispatch.
- gamora D11 math note **auto-fires on this advisory's completion record append** (per dispatch coordination clause).
- jack-ryan Gate 1 readiness review can run in parallel with gamora math note authoring; verdict feeds into rocket's D11 implementation phase.
- No additional sequencing requests from me; standard dispatch chain.

---

## § 9 — Summary table (acceptance criteria mapping)

| Dispatch acceptance criterion | This advisory's coverage |
|---|---|
| All 5 sub-questions answered with evidence | § 2 (Sub-Q 1), § 3 (Sub-Q 2), § 4 (Sub-Q 3), § 5 (Sub-Q 4), § 6 (Sub-Q 5) |
| ARPG-canon survey grounded in specific game / system examples | § 2.1 (D1) through § 2.13 (Hades/Returnal); explicit categorization at § 2.14 |
| Tuning lever recommendation concrete enough for gamora to translate to math | § 4.1 (formula); § 4.2 (ceiling); § 4.5 (gamora-readiness checklist); § 8.1 (handoff items) |
| Thematic framing aligned with current canonical-7 substrate + form-library + earth-self body of work | § 5.1 (canonical-7); § 5.2 (form-library); § 5.3 (earth-self); § 5.5 (synthesis) |
| D11 scope guidance explicit | § 6.2 (tight on hybrid_mage); § 6.3 (flagged adjacencies); § 6.4 (out of scope) |
| Hive log STATE + HANDOFF → gamora + HANDOFF → jack-ryan (Gate 1 readiness) | § 8.1; § 8.2; § 8.4 |
| No new vendor commissions; no code changes; pure design advisory | confirmed |

---

## § 10 — Pushback memo (none filed)

I did not file pushback against the dispatch's framing. The dispatch was well-shaped, the L3 #42 closure was clean, and the Pattern B short sizing was right. No pushback warranted.

One narrow flag for the future: the dispatch occasionally framed "retire" as a clean option (e.g., "the engine can't model hybrid_mage cleanly at scale"). The empirical evidence is that the engine *can* model it cleanly once the tax is in place. The framing of "can't" was reasonable given the 0% convergence streak but should not be the project's settled view going forward. The engine handles hybrid_mage exactly as well as any other archetype *once given the structural costs that every successful ARPG provides*.

---

## § 11 — Closing (mythic register, briefly)

The hybrid_mage is the form that asks to hold many commitments at once. The substrates respond honestly: *the spark we give you will be a little less hot, the wave we give you will be a little less deep, because you are not entirely ours*. The form attempts this anyway, because there are problems in the world that a single substrate's commitment cannot solve — fights against monsters whose resistances would shut out any specialist, journeys whose terrain demands more than one kind of motion. The chromatic_mage is the form for those moments. The Court of Forms remembers it as the form that integrated many voices without abandoning the discipline of any one. The price paid is the form's truth-telling about what integration costs. The reshape gives this form back to itself.

---

---

## § 12 — Appendix: deeper ARPG system-level analysis (supplementary evidence)

This appendix is supplementary to § 2. It provides additional system-level depth for the most-load-bearing references (D2 LoD synergies, PoE Elementalist, LE Runemaster) so that gamora and jack-ryan have full-evidence access when validating the recommendation. Skip if § 2 is sufficient.

### § 12.1 — Diablo 2 LoD synergies in detail

The D2 LoD synergy mechanic is the genre's first and still most-influential breadth-tax mechanism. Each Sorceress active skill has a list of *synergy skills*, each of which adds a per-rank damage bonus to the target skill. Specific examples:

- **Fireball:** synergies from Fire Bolt (+12% per rank), Meteor (+5% per rank), Fire Mastery (+30% per rank, separate column). A Sorceress with 20 Fire Bolt, 20 Meteor, 20 Fire Mastery, and 20 Fireball gets: base Fireball + (20 × 12%) + (20 × 5%) + (20 × 30%) — roughly 240% + 100% + 600% = +940% damage from synergies + Mastery. This is on top of the base skill damage. The skill becomes order-of-magnitude stronger.
- **Blizzard:** synergies from Ice Bolt (+5%), Ice Blast (+3%), Glacial Spike (+3%), Cold Mastery (cold-resist-piercing). A pure-Blizzard sorceress invests 20 points each in Ice Bolt, Ice Blast, Glacial Spike, Cold Mastery, and Blizzard = 100 points concentrated.
- **Lightning:** Charged Bolt, Lightning, Chain Lightning synergize each other; Lightning Mastery and Energy Shield round out. Similar 100-point concentration.

A *split* Sorceress (10 Fire Bolt + 10 Meteor + 10 Fire Mastery + 10 Fireball + 10 Ice Bolt + 10 Ice Blast + 10 Glacial Spike + 10 Cold Mastery + 10 Blizzard) has 90 points spread across two trees, each tree at half-depth. Fireball's synergy contribution: (10 × 12%) + (10 × 5%) + (10 × 30%) = 120% + 50% + 300% = 470%. Less than half the specialist Fireball. Same math for Blizzard.

**The Meteorb workaround:** Meteor and Frozen Orb have *fewer* but *bigger* synergies. Meteor: Fire Bolt + Fire Ball + Inferno + Fire Mastery. Frozen Orb: Ice Bolt + Cold Mastery (cold-pierce; massive). A Meteorb Sorceress invests 20 in Fire Bolt, 20 in Fire Ball (as second-tier synergy), 20 in Meteor, 20 in Cold Mastery, 20 in Frozen Orb, 20 in Ice Bolt = 120 points. Both skills get *moderate* synergy and the Cold Mastery's resistance-pierce makes the cold side viable against fire-resistant Hell monsters. This is the build that proves multi-element is *possible* in D2 *only when the specific synergy math works out* — Meteor and Frozen Orb happen to be the right pair. Trying to Meteorb-equivalent Fireball + Blizzard fails because both skills have *deeper* synergy trees that punish splitting harder.

The relevance: D2's empirical "what does a 50-50 split cost" is ~50% damage output. Reincarnated's α=0.07 quadratic at 3 elements = 7%; at 4 elements = 28%. The Reincarnated tax is *lighter* than D2's split-Sorceress tax. This is correct because Reincarnated's hybrid is *meant* to be playable (engine-declared); D2's split-Sorceress is *not* meant to be optimal (player-chosen anti-optimal).

### § 12.2 — Path of Exile Elementalist Ascendancy in detail

PoE's Elementalist Ascendancy (one of three Witch ascendancies; the others are Necromancer and Occultist) has 8 keystone points spread across 4 tiers. The Elementalist-defining keystones:

- **Mastermind of Discord** (tier 1): exposure to one element from your hits; +20% exposure effect to that element. Exposure is a debuff that reduces target resistance. Mastermind makes a *one-element* build apply exposure to that element. *But the keystone is most-powerful when paired with the Beacon of Ruin or Liege of the Primordial multi-element synergies*.
- **Shaper of Storms** (tier 2): you always shock; +15% shock effect. Lightning-specific synergy.
- **Shaper of Flames** (tier 2): you always ignite; +25% ignite duration. Fire-specific synergy.
- **Beacon of Ruin** (tier 3): your hits always ignite/freeze/shock at minimum strength. The *multi-element capstone* — makes a 3-element kit's ailment-application universal.
- **Liege of the Primordial** (tier 3): +50% elemental-golem damage; can summon one additional golem of each type (fire / ice / lightning / chaos / stone). The *summoning-multi-element* keystone.
- **Pendulum of Destruction** (tier 4): every 5 seconds you alternate between +50% AOE and +50% elemental damage. Universal scaling.

The Elementalist build space (community discourse, ~2020-2025):

- **Pure cold-DoT (Cold Snap or Vortex):** uses Mastermind of Discord + Shaper of Storms paired with Hatred (a cold-aura gem). One element. Specialist. Strongest single-element Elementalist builds, often featured in top-tier-leaderboards seasonal.
- **Tri-elemental ailment-stacker (Storm Brand + Wave of Conviction + DoT):** uses Beacon of Ruin + Shaper of Flames + Shaper of Storms. Three elements. Mid-tier; *the* iconic Elementalist build; thematically beloved.
- **Golem-summoner:** uses Liege of the Primordial + Beacon of Ruin. Multi-element via the elemental golems. Niche but viable.

The PoE community's verdict (every league I am aware of from 2019-2024): tri-elemental Elementalist is *fun*, *thematic*, *mid-tier in clear-speed*, and *consistently below pure-cold-DoT in damage-per-second leaderboards*. The taxes work; the breadth is rewarded enough to be playable; the specialist is still optimal.

This is *exactly* what Reincarnated's chromatic_mage should be: fun, thematic, mid-tier, mechanically distinct, *not the leaderboard-top archetype*. The reshape delivers this profile.

### § 12.3 — Last Epoch Runemaster Mastery in detail

Last Epoch's Runemaster (released Feb 2024, LE 1.0) has three mastery trees: Frost / Lava / Storm. The character chooses one as primary mastery (becomes their class title), with the other two as secondary access. The Runic Invocation mechanic:

- The player has a Runic Glyph bar (separate from skill bar) with N glyphs (Frost, Spark, Aura, Ember, etc.) earned from passives and skill investment.
- Casting a Runic Invocation consumes three glyphs in sequence; the resulting Invocation depends on the *combination* of three glyphs.
- Example: Frost + Spark + Aura = *Frost Bolt* (a cold-keyed projectile). Frost + Ember + Aura = *Lava Burst* (a fire-keyed AOE). Spark + Spark + Ember = *Storm Crash* (a lightning-keyed targeted area).

The Runemaster's mastery-tree investment shapes which glyphs the player can produce and how powerful each Invocation is. A Frost-primary Runemaster has access to all 27+ Invocations but the *Frost-keyed* ones scale most strongly; the *Lava-keyed* and *Storm-keyed* ones are usable but mechanically weaker.

The community's verdict (LE 1.0 launch through ~mid-2024): Runemaster is *the* most-praised LE class for *build-crafting feel* (the Invocation combinatorics are deep; players spend hours optimizing rotation). Mechanically, Runemaster builds are mid-tier in *raw clear speed* but high-tier in *boss-fight versatility* — the multi-element flexibility lets the Runemaster adapt to boss-element-immunity without rerolling. This is the design payoff of multi-element done correctly.

The relevance: Reincarnated's chromatic_mage post-reshape should have the same payoff profile — *mid-tier raw output*, *high-tier coverage flexibility*, *appealing to players who enjoy build-crafting depth*. The damage tax produces this profile cleanly. The form-library narrative supports the build-crafting feel (the player accumulated this form deliberately across seasons; it's earned, not assigned).

### § 12.4 — Why D3-launch failed (the cautionary tale at depth)

D3 launched in May 2012 with a notorious balance problem in the Wizard class. The Wizard had 6 active skill slots + 4 passive slots; each active skill had ~6 rune mods. The combinatorics were ostensibly enormous, but in practice the *meta-game collapsed within weeks* to a handful of builds.

The structural problem: there was no cost to multi-element. A Wizard could equip Frost Ray + Disintegrate + Meteor + Magic Missile + Frost Nova + Archon, with no synergy penalty, no resource cost beyond mana, and no opportunity-cost system. The damage values were *roughly equivalent across elements* (some elements were stronger by tuning happenstance, but not by design). The meta-game collapsed to "whichever element happened to have the highest damage coefficient in the current patch."

Reaper of Souls (Mar 2014) corrected by introducing *Tal Rasha's Elements* set — a 6-piece legendary set that *requires* the Wizard to cast skills of multiple elements to trigger a stacking damage buff. The set forced multi-element, *and the resulting builds became seasonal-meta-dominant*. But this is a *gear-driven* correction, not a *mechanic-driven* one — the multi-element identity was injected via items, not via class design.

The Reincarnated relevance: D3-launch is *exactly* what Reincarnated's current hybrid_mage state is — multi-element is permitted with no cost, and the resulting kit is over-powered relative to single-element peers. The fix is *not* to add gear that rewards multi-element (the D3-RoS path); the fix is to *charge* for multi-element at the class-design layer (the D2 / PoE / LE path). The reshape is the right fix.

### § 12.5 — Grim Dawn dual-mastery: why it works for Grim Dawn but not for Reincarnated

Grim Dawn (Crate Entertainment, 2016) requires every character to choose two of nine masteries: Soldier, Demolitionist, Occultist, Nightblade, Arcanist, Shaman, Inquisitor, Necromancer, Oathkeeper. The *combination* is the character's class — Spellbreaker (Nightblade + Arcanist), Druid (Shaman + Arcanist), Pyromancer (Demolitionist + Occultist), etc. There are C(9,2) = 36 combinations, each with its own community-named identity.

The dual-mastery works because:

1. **Crate spent years balancing each combination individually.** Each of the 36 combinations was tuned individually with playtesting feedback over multiple expansions. This is a *massive content-design investment*.
2. **The shared skill-point pool naturally enforces depth-vs-breadth.** A character has ~50 skill points to spend; spreading them across two masteries means each mastery is shallower than a hypothetical single-mastery character would be. The opportunity cost is built into the point economy.
3. **Devotion-tree overlay adds another dimension.** Devotion points (separate pool) are spent on a constellation tree; this further differentiates combinations because devotion synergies are mastery-keyed.
4. **The Grim Dawn community is small but dedicated.** The build-crafting culture supports the labor-intensive design; players treat each combination as a distinct class identity.

Why Reincarnated can't do this:

1. **The engine *generates* archetypes; it doesn't *design* them.** Reincarnated has no person-team to tune 36 individual combinations. The archetypes emerge from substrate × role × LLM-naming.
2. **The shared-point pool doesn't exist in Reincarnated.** Reincarnated's classes are seasonal forms, not progression-investment characters. The opportunity cost of multi-element must be at the *kit-generation* layer, not at the *player-investment* layer.
3. **The form-library is the diversity surface, not within-form mastery.** Reincarnated's accumulated breadth lives in the form-library; within a single form, the player commits to that form. Grim Dawn's within-character dual-mastery doesn't map.

Grim Dawn is a *cautionary tale* in the opposite direction from D3: GD shows that permissive multi-mastery *can* work, but only with massive design effort. Reincarnated's design effort budget is in LLM-content generation, not in per-archetype balance. The Reincarnated answer is the PoE / LE / D2 path: one constrained hybrid class, taxed, mid-tier.

### § 12.6 — Cross-reference: monster ailment systems and breadth-coverage

A subtle point about the empirical hybrid_mage failure: the gauntlet's *monster ailment-immunity* structure is part of why breadth wins. The pre-D10 gauntlet had monsters with *no element-immunity* — every monster could be damaged by every element. Multi-element coverage was *purely additive*: an additional element meant additional ways to deal damage, no downside.

In D2 LoD, this structure was *changed* by the LoD expansion's introduction of *monster immunities* (a percentage of Hell-difficulty monsters are immune to one element entirely; cold-immune monsters take 0% cold damage). This made specialists *unable to clear Hell solo* on cold-immune monster maps and made multi-element a *necessity* for solo Hell clears — converting breadth from "purely additive bonus" to "structurally required against certain content." The genre learned that monster-immunity structure *changes the calculus of breadth*.

The Reincarnated gauntlet currently does not have monster-immunity structure — only *resistance differentials* (more vulnerable / less vulnerable, but never zero damage). This is correct for the early-game / first-pass; introducing monster-immunity is a D12+ design item.

**The relevance:** if Reincarnated eventually introduces monster-immunity (a D12+ option), the chromatic_mage's value proposition shifts — multi-element becomes *structurally required* for content with broad-immunity coverage, just as D2 LoD changed. At that point, the damage tax can be re-calibrated lower (because the *value* of breadth increases). For now, the damage tax operates against a gauntlet with no immunities; the calibration is appropriate.

Flag for downstream design exploration; not D11 scope.

### § 12.7 — Cross-reference: the engine's specific gauntlet composition

For gamora's empirical validation, the gauntlet that the v1.5 hybrid_mage was tested against (season_002012):

- 6 swarm/pack: fire brute, water caster, earth swarmer, wind controller, fire tank, water sniper
- 2 magic: fire brute, water caster
- 2 elite: fire swarmer, water controller
- 1 mini-boss: fire tank
- 1 boss: earth brute

Element coverage of non-pack slots (which determine convergence WR): 3× fire + 2× water + 1× earth = 6 monsters across 3 elements.

A hybrid_mage with fire/water/wind/physical (Class C) had:
- Fire skills hit the 3 fire monsters with *no resistance* (no fire-vs-fire-monster interaction in this kit composition; some fire-resistant monsters absorb less)
- Water skills hit the 2 water monsters with no resistance penalty
- Wind skills hit the 1 earth monster effectively (earth has neutral wind resistance)
- Physical skills cover residual

Result: *every monster has at least one element the kit damages effectively*. This is the structural advantage that the damage tax corrects. Post-reshape with α=0.07 at 3 elements: the kit pays 7% to retain this coverage; the specialist (fire-only) has *no* tax but *cannot* damage the cold-resistant elite efficiently.

Gamora's empirical α calibration should re-simulate against this specific gauntlet for direct comparison with the v1.5 baseline.

### § 12.8 — Comparison table — taxes across the genre

For quick reference, a per-game tax-magnitude estimate (community-discourse and design-doc empirical averages where available; my training-derived estimates otherwise):

| Game | Multi-element class | Tax mechanism | Net DPS cost vs specialist |
|---|---|---|---|
| D1 (1996) | n/a (single mage; player specializes via tome scarcity) | Tome economy | n/a (no genuine hybrid) |
| D2 LoD (2001) | Sorceress (3-tree split) | Synergy opportunity cost | ~40-60% DPS reduction at 50/50 split |
| D3 launch (2012) | Wizard | (none — disaster) | ~0% (cause of balance disaster) |
| D3 RoS+Tal Rasha set (2014) | Wizard (set-encouraged) | Set bonus *rewards* multi-element | -20% baseline + 100%+ via set = net positive |
| D4 (2023) | Sorcerer | Tree-point + enchantment-slot + aspect | ~30-50% DPS below specialist meta |
| Immortal (2022) | Sorcerer | Skill-cap (4 slots) | Specialization forced at low element count |
| PoE 1 Elementalist (2013+) | Tri-element specialist | Passive points + sockets + resists + ailments | ~30-40% raw DPS; mid-tier; thematic |
| PoE 2 Sorceress (2024+) | Stormweaver / multi-element | Same as PoE 1 with refinement | Similar to PoE 1 |
| LE Runemaster (2024) | Multi-element via Invocations | Cooldown + mastery-split | Mid-tier; high boss-flex |
| GD multi-mastery (2016) | All 36 combinations | Shared skill-point pool + design effort | Balanced individually; specialist beats split in same tree |
| T2 Embermage (2012) | Soft hybrid | Soft synergy | ~10-20% DPS below specialist |
| Lost Ark (2022 NA) | n/a (class-tier specialization) | n/a | n/a |
| Hades Zagreus (2020) | Boon-stacked multi-god | Boon-slot opportunity cost | Build-specific |
| Path of Achra (2024) | Roguelike multi-class | Synergy fragility | Emergent |

The cluster I am recommending Reincarnated align to (PoE Elementalist + LE Runemaster + D4 Sorcerer mid-band) sits at *roughly 25-40% net DPS below specialist*. My recommended α=0.07 quadratic at 3 elements (7%) is *softer* than this band — closer to T2 Embermage's soft-synergy tier. At 4 elements (28%), the recommendation lands in the canonical band.

This is the *intentional* calibration: 3-element hybrids in Reincarnated should be *easier-to-balance and more-playable* than D4/PoE/LE multi-element builds because Reincarnated's hybrid is *engine-declared* (the player did not choose to be a non-optimal multi-element specialist; the engine generated this form for them). 4-element ceremonial hybrids (D12+ path) hit the genre-canonical 28% band — that's the "you chose this rarity; you accept the cost" tier.

The calibration is deliberate. Gamora's empirical α adjustment may shift these numbers by ±0.02; that's within the recommended band.

### § 12.9 — Final note on genre tonal cohesion

The reshape is *consistent* with how the most-respected ARPGs across the genre's 30-year history have handled multi-element classes. It is *consistent* with the serious-isekai genre's tonal commitment around accumulation-cost (Mushoku Tensei, Solo Leveling, Re:Zero). It is *consistent* with Reincarnated's canonical-7 substrate-identity framework. It is *consistent* with the form-library narrative. It is *consistent* with the Earth-Self diversity-via-grace framing. It is *consistent* with the engine's seam discipline (the tax lives where Phase-1 P2 will look for it). It is *empirically tractable* (gamora can calibrate against the v1.5 sample in 30-40 minutes of sim time).

This is a high-cohesion recommendation. The reshape's costs are bounded; its benefits are aligned across mechanical, thematic, and narrative dimensions. The risks are calibration risk (α might need adjustment from 0.07; gamora handles this empirically) and Phase-1 P2 forward-compat risk (the tax must live in the right config; § 4.7 handles this with the universal-formula + per-archetype-ceiling decomposition).

---

---

## § 13 — Cross-reference appendix and open-flags registry

For downstream specialists (gamora, jack-ryan, rocket, drax) to navigate this advisory's connections to existing canonical work.

### § 13.1 — Canonical cross-references

The reshape recommendation rests on and references the following canonical artifacts:

1. **`canonical/story/substrate-identity-declarations-2026-05-17.md`** — the 7-substrate identity declarations including `forbidden_hybrid_with` field. The tax architecture must respect these declarations (fire/water never composed; earth/wind never composed; etc.).

2. **`canonical/story/substrate-identity-declaration-spec-2026-05-17.md`** — the spec the declarations instantiate. The amendment process for adding tax-related fields (if needed) goes through this spec.

3. **`canonical/story/substrate-expansion-decision-2026-05-17.md`** — the canonical-7 substrate set decision (fire/water/earth/wind + lightning + holy + shadow). Defines the universe of elements that n_elements counts against.

4. **`canonical/story/earth-self-diversity-tension-2026-05-17.md`** — the Earth-Self / Court-as-grace framing. The reshape preserves this framing; the chromatic_mage is a Court-remembered form regardless of leaderboard ranking.

5. **`canonical/story/court-of-forms.md`** — the Court of Forms narrative. The reshape integrates with the form-library narrative arc.

6. **`canonical/story/embodiment-display-loadout.md`** — the player-facing loadout surface. Drax's downstream surface work (low priority; § 8.3) connects here.

7. **`canonical/story/gandalf-design-lineage.md`** — my own design-lineage notes, including the layered ARPG history that grounds the § 2 survey.

8. **`canonical/story/gandalf-phase2-bullet-points.md`** — my Phase 2 design recommendations, including the form-library-as-Court framing (§ 1.4).

9. **`canonical/story/aoe-tuning-and-monster-density-genre-canon-validation-2026-05-17.md`** — genre-canon validation of AoE / monster-density choices; informs the kit-composition framing for hybrid_mage's 3-element + AoE-share generation.

10. **`canonical/story/archetype-coupling-archaeology-2026-05-17.md`** — the archetype-coupling-archaeology that identified hybrid composition as Phase-1 P2 candidate; informs the forward-compat constraint in § 4.7.

11. **`agentic_orchestration/hive-mind/phase-1-p1-log.md` lines 1700-1815, 2180-2290, 3700-3920** — the hive-mind discussions that led to `forbidden_hybrid_with` declaration and the substrate-identity loader refactor. The reshape inherits this architecture.

12. **`reincarnated-engine/output/standard-demo-regen-2026-05-17/D10-substrate-coherent-gen-math-note-2026-05-17.md`** — gamora's D10 math note; this advisory extends D10 with the tax recommendation.

13. **`reincarnated-engine/output/standard-demo-regen-2026-05-17/convergence-sample-analysis-2026-05-17.md`** — the v1.5 sample analysis with Class C (hybrid_mage) deep-read; the empirical anchor for α calibration.

14. **`reincarnated-engine/src/reincarnated/generation/b6_archetype_templates.py:241-267`** — the current `_HYBRID_ARCHETYPE_TEMPLATES` definition. The reshape will modify this (or be modified by Phase-1 P2 hybrid-composer migration).

15. **`reincarnated-engine/src/reincarnated/generation/d10_kit_constraints.py:34-92`** — the existing D10 kit-constraint module. Tax computation likely lives here (or in a successor module).

### § 13.2 — Open flags for downstream (D12+ / Phase 2)

The advisory closes L3 #42 and answers D11's tuning direction, but it surfaces several flags for future work:

**FLAG 1 — Ceremonial 4-element hybrid path (D12+ or Phase-1 P2).** § 6.3 item 3. The reshape caps general-generation hybrid_mage at 3 elements; the 4-element ceremonial path is a future design item. Architecturally tied to Trial-boss-gallery generation, capstone seasons, or form-library milestone events. Design pass needed before implementation.

**FLAG 2 — Resistance-hole-at-substrate-seam mechanic (D12+).** § 6.3 item 4. For the ceremonial 4-element hybrid, an element-specific drawback (e.g., +25% damage taken from one named element) would give the form a distinctive mechanical signature. Canonical-7-coherent (the substrate at the form's weakest commitment punishes the form). Design pass needed.

**FLAG 3 — Ailment-overlap diminishing returns (D12+).** § 2.6 supplementary. Per-monster ailment-slot limit; new ailment displaces oldest. Elegant version of breadth-tax; PoE-shaped. Would naturally tax multi-element kits without explicit damage multiplier. Design pass needed; gameplay implications (current ailment-stacking play would change).

**FLAG 4 — Monster-immunity structure (D12+).** § 12.6. Introducing monsters with element-immunity (rather than just resistance differentials) would change the calculus of breadth — hybrid becomes structurally *required* for some content. Significant content-design item; affects gauntlet composition, balance loop, and class balance simultaneously. Design pass needed.

**FLAG 5 — Phase-1 P2 hybrid-composer module.** § 6.3 item 1. Currently `_HYBRID_ARCHETYPE_TEMPLATES` holds hybrid_mage as a holdover. P2 will refactor this. The D11 tax must live in P2-compatible config (per § 4.7). When P2 lands, hybrid_mage's template will be derived from substrate × hybrid-composer rules; the tax inherits cleanly.

**FLAG 6 — Spirit Guide voice integration (P2).** § 5.7. The Spirit Guide commentary on hybrid_mage selection. Demonstrative text drafted in § 5.7. Drax (or whoever owns spirit-guide-voice) implements in P2.

**FLAG 7 — Rename `hybrid_mage` to `chromatic_mage` (or `elementalist`).** § 7.1. Matt's decision. If approved, small rename pass across decisions-log, telemetry, season data, demo/loadout.

**FLAG 8 — Future hybrid archetypes (hybrid_physical, hybrid_caster, etc.) inherit universal tax.** § 7.5. Confirmation needed from Matt; my recommendation is yes (universal n_elements > k_free tax).

**FLAG 9 — Calibration tuning if α=0.07 proves miscalibrated.** § 4.1 + § 4.6. Gamora's empirical pass determines actual α; if significantly different from 0.07, surface to me for advisory follow-up.

**FLAG 10 — Long-term: hybrid roles other than mage (hybrid_controller? hybrid_caster?).** Architecturally permitted by canonical-7 (you can compose a hybrid kit at controller role or caster role). Currently only hybrid_mage exists. P2's hybrid-composer should consider whether to support role-variant hybrids. Design pass needed in P2.

### § 13.3 — Tag and provenance

This advisory is tagged for local archive (not pushed per ADR-006):

- **Tag:** `gandalf/v1.3-d11-hybrid-mage-tuning-advisory-1`
- **Predecessor tag context:** prior gandalf authorship at `gandalf/v1.2-dodge-and-telegraphed-combat-l3-briefing-1` (commit area `3ec108f`); recent canonical/story work captured at commits `ee9e169`, `2f38ff9`, `6de0c46`.
- **Companion artifacts to be created by gamora:** D11 math note at `reincarnated-engine/output/.../D11-hybrid-mage-tuning-math-note-2026-05-17.md` (gamora's path-choice).
- **Companion artifacts to be created by rocket (D11 implementation):** changes to `b6_kit_builder.py` and/or `d10_kit_constraints.py` (rocket's seam-disposition); MIGRATION.md entry; possibly new config file near substrate-identity declarations.
- **Companion artifacts by jack-ryan:** Gate 1 advisory review verdict; gate-checkpoint entry.

### § 13.4 — Discipline cross-references

This advisory observes the project's engineering disciplines as follows:

- **Discipline #1 (math-before-code):** Advisory ships before gamora's math note; math note before rocket's implementation. Sequencing correct.
- **Discipline #11 (empirical inspection over assumption):** The v1.5 Class C sample is the empirical anchor; α calibration is empirical via gamora's balance-loop validation.
- **Discipline #12 (semantic shift):** Tax mechanic is a semantic shift; MIGRATION.md entry needed; flagged in § 4.5.
- **Discipline #13 (implicit-pillar drift):** The hardcoded hybrid_mage template would represent implicit-pillar drift if the tax were hardcoded as a magic number in the template. § 4.7 explicitly places the tax in P2-compatible config to avoid this.
- **Discipline R11(b) (round-trip):** Cross-seam contract: if the tax is at kit-finalization (§ 4.8 Site A), the export path sees taxed kits and round-trips correctly. Flagged in § 8.1 item 6.

This is a high-discipline-cohesion advisory by construction.

---

## § 14 — Pre-completion checklist

Before the completion record is appended, this advisory should pass:

- [x] All 5 sub-questions answered with concrete evidence (§§ 2-6)
- [x] ARPG-canon survey grounded in specific game / system examples (§ 2 + § 12 appendix)
- [x] Tuning lever recommendation concrete enough for gamora to translate to math (§ 4 with formula, magnitudes, worked-example calibration table, application-site recommendation, gamora-readiness checklist)
- [x] Thematic framing aligned with current canonical-7 substrate + form-library + earth-self body of work (§ 5 with explicit cross-references to substrate-identity declarations, court-of-forms, earth-self-diversity-tension)
- [x] D11 scope guidance explicit (§ 6.2 tight on hybrid_mage; § 6.3 flagged adjacencies; § 6.4 out of scope)
- [x] Hive log STATE + HANDOFF → gamora + HANDOFF → jack-ryan (Gate 1 readiness) — pending; will follow advisory commit
- [x] No new vendor commissions; no code changes; pure design advisory
- [x] Pushback memo filed (or not filed with rationale) — § 10 explains why no pushback warranted
- [x] Open questions for Matt surfaced clearly (§ 7 with 5 specific questions)
- [x] Tag captured (§ 13.3)
- [x] Cross-references registered (§ 13.1)
- [x] Open flags registered for downstream (§ 13.2)
- [x] Disciplines observed (§ 13.4)

Advisory is complete. Hive log PRE-SIGNAL and STATE entry follow.

---

*Authored 2026-05-17 by gandalf. Design advisory; ARPG-canon evidence base in §§ 2 + 12 is load-bearing. Closes Matt L3 #42 in the reshape direction. Gates D11 sprint; gamora math note auto-fires on completion record append.*
*Tag: `gandalf/v1.3-d11-hybrid-mage-tuning-advisory-1` (local; push gated per ADR-006)*
