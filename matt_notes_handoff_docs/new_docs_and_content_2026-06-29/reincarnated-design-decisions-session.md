# Reap. Die. Rise. — Design Decisions Reference (Session Wrap)

**Project:** Reap. Die. Rise. (ARPG / roguelite, Godot 4, deterministic procedural-generation engine, multi-agent Claude dev team)
**Document:** Consolidated decisions from this design session
**Status:** Decisions reference — companion to:
- `reincarnated-gameplay-loop-design.md` (engine, core loop, ontology, sawtooth, Goldilocks, grimoire, spawn economy, story frame v2)
- `reincarnated-performance-target-specs.md` (renderer, horde architecture, tier targets, density benchmarks)
- `reincarnated-backend-networking-stack.md` (PVE-vs-PVP backend, Godot netcode, hosting/cost)

This doc captures what was newly decided or refined **in this session** and is **not** in the three above. Tags: **[DECISION]** settled · **[OPEN]** unresolved · **[FRAGILE]** works only if a condition holds · **[MEASURE]** an empirical question for the battle sim, not an assumption.

---

## 1. Story frame — finalization

**[DECISION] The patron deity is an original, beyond-gender ("it") sealed death-deity** built on **Ereshkigal** (gated underworld, the descent-myth, the canonical "cannot leave its realm" seal that justifies working through abducted servants) + **the Morrígan / Nergal** (war, fate, claiming-the-slain — the *conquest verb* Ereshkigal lacks). Beyond-gender dodges the Diablo-4-Lilith comparison and the documented Ereshkigal↔Lilith link.

Research notes that shaped this:
- Ereshkigal supplies four hard-to-find gifts: the **seven-gated staged descent**, the **canonical cannot-leave seal** (native justification for "deity acts only through servants"), an **abduction origin** (rhymes with the player's abduction), and **pure soul-sovereignty**. But she is a *passive judge-custodian, not a conqueror* — so the harvest-by-conquest engine comes from the *war-death* side (Nergal is literally her consort; the myth splits the labor).
- **[DECISION] Beelzebub rejected** — no death/soul domain, drags into Christian-Hell demonology (Diablo's exact territory), and "Lord of the Flies" fights the grave-menace tone. Lesson: don't reach toward the demonological-prince category (that's Diablo's home turf); reach *deeper* into under-mined pre-Christian death-sovereigns.
- **[DECISION] Hecate rejected as a source**, but its *mechanism* kept — the real "Hecate Ereschkigal" magical papyrus is a primary-source example of a *layered concealed power-name invoked as incantation*, which grounds the true-name device (below) in authentic myth.

**[DECISION] Layered name.** A **crackable alias** (TVA-style cover name — fine for the community to solve fast; reveals the deity's *nature*) + a **true name that is authored-slow** (withheld from game data until a story-reveal chapter; **not** decipherable-from-clues, or datamining spoils it). Slowness comes from *unreleased*, not *concealed*. **[DECISION] Layer the reveals** so casual players get payoff early (alias, then nature/desire within season one); the true name is the deep capstone. **[DECISION] Entangle the true name with the player's own erased name** — remembering who you were is what lets you name what owns you, which is the leverage for the "deny the god / earn your way out" climax. (True-names-as-power is native to the Mesopotamian/Celtic register.)

**[DECISION] Trickster-jab mechanic.** The player can needle the patron's *stature* ("you're just a minor luck-spirit") to enrage it — works *because* it's sealed/diminished (pokes the real wound). Three jobs: makes the menace legible-as-fragile, sets up the true-name reveal (you mocked it as a fraud → it's revealed ancient/terrible = comedy curdles to dread), and gives the defiance axis a vocabulary.
- **[FRAGILE]** Disciplines: the patron must *occasionally win* the exchange (a flash of the real thing) so jabs stay *risky*; let the jab-temperature *cool* as the true name approaches; use a *lesser deity from the game's own pantheon*, **not** literal "Loki" (current Marvel IP, tonally jarring) — and rub the *smallness* wound, not "trickster" (which could make it sound cooler).

**[DECISION] Descent ≠ underworld (aesthetic).** Making the descent look like the underworld would collapse seasonal variety (every season the same gloom). Resolution by layer:
- **Hub / End-of-Time = Irkalla-resemblant** (the sealed deity's domain — spend the Ereshkigal aesthetic here).
- **Cosmograph = the underworld's "sky"** (Irkalla *elevated* into a starfield of claimed souls).
- **Descent = a *living* world being conquered**, rotating per season (the souls' current home, not yet claimed).
- **[DECISION] Ereshkigal's gift to the descent is *structural, not aesthetic*: the seven gates become the gated floor-structure** — an invariant mythic *shape* (staged descent, threshold by threshold) that makes every season feel like "a descent into a death-god's claiming-ground" while each season *looks* completely different. Gates = constant ritual; world = variable skin.
- **[OPEN/probe]** Inanna's stripping-of-power-at-each-gate as a candidate *escalating-cost-with-depth* mechanic (tune carefully against the sawtooth).

---

## 2. Genre identity & density

**[DECISION] It is an *action roguelite ARPG* — ARPG-led.** ARPG is the genre/shelf/identity/differentiation (loot, builds, kit identity, horde power-fantasy, no-meta); roguelite is the *run-structure* (descent, reset, procedural floors). Lead with ARPG (the differentiation is ARPG-native; the audience searches "ARPG"). It sits in the *proven, hot* Hades / Death-Must-Die / Diablo-roguelite hybrid space.

**[DECISION] The load-bearing balance is the persist/reset ratio** — within-run reset (descent 1→50) + cross-run persistence (permanent grimoire, became-it pages, patron relationship, recovered self). Too much persistence → runs feel pointless; too much reset → build-investment fantasy dies. Keep the *failure boundary* clean: a lost descent costs *run-scoped* things (in-run levels, volatile pages), **never** the permanent collection (the two-register grimoire already enforces this).

**Combat pacing — competitive read (research):** most ARPG-roguelites are *deliberate/soulslike-paced* (Moonlighter, Into the Necrovale, Netherworld Covenant). Only **Hell Clock** ("PoE screen-clearing in quick roguelite runs") and **The Slormancer** (screen-filling ARPG density) deliver *true* ARPG horde-feel in a roguelite shell. **Hell Clock is the closest pacing match and the most important title to study.** **Netherworld Covenant** is the closest *thematic* neighbor (cursed artifact binds you to fallen souls, summonable spectral allies) — differentiate via generative scale, *becoming* (you play the souls, not just summon a fixed few), and the reincarnation engine.

**[DECISION] Density target = the genre *comfortable* band (~50–150 simultaneous hostiles); POE-juiced (~few hundred) is the explicit ANTI-target.** See the performance doc §3 for the full bounded-estimate benchmark table (D2 ~30–80, D3 ~50–150, D4 ~50–150+ with strain, POE1 ~100–300+ with franchise-wide strain, POE2 ~nerfed-bounded, Last Epoch ~50–150). MultiMesh fodder makes the comfortable band *feel* dense. **[MEASURE]** Exact peak number on the min-spec floor.

---

## 3. Kit count

**[DECISION] Launch ~100 fully-distinct kits; architect the engine for 400+; grow via seasonal/experimental — "launch lean, grow endless."**
Don't *target* a number; **derive it as `min(marketing-floor, production-ceiling, distinctiveness-ceiling)`**:
- **Marketing floor:** ~50 minimum, **saturated at ~100** (the hook — "violate the single-digit-class norm so hard it's staggering" — saturates; 100 vs. 400 reads identically as "impossibly many"). Past 100, more kits help *retention*, not *acquisition*.
- **Production ceiling: [MEASURE]** — build 10–20 kits to full quality, measure per-kit hours; depends entirely on whether kits are *library+config* (parametric, high ceiling) or *hand-builds* (brutal ceiling). Probably the *binding* wall for a solo dev.
- **Distinctiveness ceiling:** count only kits with a *recognizably distinct verb* — **300-sharp beats 400-with-80-reskins**, because a samey kit *damages* the hook (it's evidence against "every hero is unique").

The *real* hook is the **generative engine** (the *capacity* for endless distinct kits); the launch count just proves the engine is real. Reframed pitch: "100 fully-realized heroes, growing every season, endlessly."

---

## 4. Matchup / dead-end screening / post-hoc labeling system

This is a major analytical pillar resolved this session.

**The problem:** what's the probability a given in-band kit can't beat *any* of the 3 Goldilocks-presented lieutenants on a boss floor — and should outliers be tuned/withheld?

**[DECISION] No a-priori probability exists — it's a property of the kit space's internal correlation structure, knowable only by querying the battle sim.** Shape: probably *low* (Goldilocks is *designed* to include a winnable option) but *non-zero* for *broadly-weak kits whose vulnerabilities correlate across opponents* (they fail all three together). The case to catch = where Goldilocks *failed* to find a winnable matchup.

**[DECISION] Goldilocks already handles kit-imbalance for *chosen* fights.** Kit-imbalance is *real* and is a *feature* in chosen fights (the "too hot" lieutenant *is* the imbalance, harnessed). It's only a *problem* in *forced* fights (the **Mega Boss** and any no-choice gate), which have no fork. **[OPEN/TODO] The Mega Boss needs *matchup-fair* tuning** ("every kit must be able to beat it") — a *different, harder* target than lieutenant tuning ("imbalance is fine because you chose this"). This is a live single-player to-do independent of PVP.

**[DECISION] Levers are coarse and upstream — screen at the level of the 20–24 QD groupings (= your "classes"), not individual kits.** (The dev can only adjust a group/class of potential kits at the top of the pipeline, or a group/class of skills — never an individual kit.) The matchup matrix is therefore a small, legible **~24×24** (~400–576 cells, inspectable), **not** an unwieldy 400-kit matrix. The QD groupings *are* the taxonomy's rows/columns.

**[DECISION] Run an attribution / feature-importance analysis** (restricted to *controllable* features — skills and classes) to find which *predict* dead-ending:
- **World 1:** a few *trap-draw skills* are the disproportionate cause → pull / strengthen / constrain those skills.
- **World 2:** a whole *class* is systematically weak → adjust or rework the class.
- **[FRAGILE]** Target only *pervasive* culprits (coarse levers cause collateral damage — a skill that's a trap in 80% of its kits, not 10%).

**[DECISION] Use matchup structure as a Goldilocks *generation constraint* (safety envelope), NOT for withholding kits** — strictly better (keeps all kits, fixes at the encounter layer). Guarantee **≥1 winnable matchup** in every spread while **keeping the "too hot" counter** (do NOT over-correct into all-easy boards = would gut difficulty). Recompute per-becoming.
- Type relationships (e.g., AOE > summon/proxy, single-target > AOE; melee/close vs. ranged/kite) are a **[MEASURE] prior derived from sim data, not asserted** — and kits are **multi-type** (model combined-type matchups, not independent RPS axes).
- **[OPEN]** Whether the BC axes *align* with matchup axes (then the matrix falls out cleanly) or are *orthogonal* (then matchup is an added characterization layer). Either way: **"mechanically distinct" (QD) ≠ "matchup-distinct"** — measure the matrix separately.

**[DECISION] Pursuit/characterization labels are a POST-HOC layer, decoupled from engine mechanics.** Derive labels via hypothesis tests *over the finished kits*, at whatever **grain** you choose — *independent* of how the engine *built* them. This:
- dissolves the granularity problem at the source (define labels to *bucket* at the right size, rather than runtime-patching combo-caps);
- decouples *pursuit grain* (how players think about what to hunt) from *mechanical grain* (how kits work) — different characterizations of the same kits for different purposes;
- is cheaply *iterable* (re-run hypothesis tests to re-tune feel, without touching the engine).
- **[FRAGILE] bounds:** labels must be *real* (hypothesis tests *discover* structure at the chosen grain — they can't invent a coherent label where kits don't cluster); *legible* (nameable to players); and *bucketing-not-pinpointing* (several kits per label, preserving last-mile RNG).

**[DECISION / general law] Specification ≠ behavior — measure, don't assume.** The clinching case: proxy kits are built by *mixing proxy components with predetermined proxy-skill saturation to target "25% proxy."* That is an *input*; the *behavioral* proxy-ness is determined downstream (skill synergies, the capstone inversion, sim-play). **The hypothesis test is the only way to know engine truth.** Apply everywhere (did the 20–24 groupings actually cluster that way? do capstones behaviorally invert? is the matchup structure what you assumed?). Sharpen "is it engine truth" to *which* truth — population proportion / per-kit degree / behavioral classification — and design the test to measure *that* for *that* purpose.

---

## 5. Capstone system

**[DECISION] Each kit's skill tree culminates in a capstone modeling Diablo/POE build-definers, in three flavors:** *augment/accelerate* (more of what you are), *parallel identity* (elemental/flavor diversity), and *mechanical conversion / inversion* (~1/3 probability — you become something *else*). Only the **conversion third** disrupts the matchup matrix.

**[DECISION] Matchup type = (grouping + capstone-state), and the matrix is *probabilistic*.** A grouping is "mostly pure, with a small tail" weighted by the inversion's *probability mass*. So Goldilocks safety is a **confidence, not a guarantee** → **the portal escape-valve is the backstop** when a rare inversion moves a kit across the matrix and an "expected-winnable" board turns unwinnable. **[MEASURE]** capture not just *which* inversions exist but their *probability mass* (the matrix-as-distribution needs the weights).

**[DECISION] The capstone is a RETENTION ENGINE via *retroactive desire*.** A kit's full identity is *invisible until capstoned* — so the bestiary becomes a *list of roads not taken* ("that average kit had a proxy-mimic capstone I never saw"). Roads-not-taken motivate *far* more than checklist completion, especially in a roguelite.

**Worked example — the "consume-for-caster" capstone:** a *low-probability* inversion where a proxy/summon kit's proxies lose all persistent-fighter value and become *fuel consumed to boost casts* (means↔ends swap; summoner → caster-who-eats-summons). This is the *sharpest proof* of §4's measure-don't-assume law: the kit is *maximally proxy by input* and *caster by behavior* — input-based labeling would be *anti-correlated with truth*. It also *moves the kit's matchup region* (proxy-profile pre-capstone → caster-profile post-capstone), the textbook case for (grouping + capstone-state) typing.

**[DECISION] The "49-level wrong-identity tax" is a NON-issue — because you don't *select* a kit, you *become* it.** (Earlier framing assumed menu-selection; corrected.) The player didn't *want* a different identity — they *became* a proxy and are *living a proxy's life*; the rare capstone is a *surprise apotheosis* of the life they're already living, not a reward they *grind toward*. Problem dissolves for the intended (discovery) player. The roguelite reset is *the point*, not a "brief payoff problem": the apotheosis is a *moment* at a life's culmination, which is *thematically perfect* (elegiac) for a game about living/ending lives.

---

## 6. Re-summon / discovery system

**[DECISION] No "life-reversion item."** A casual revert-to-any-life would collapse the one-way-door commitment that gives every becoming its stakes. Instead **extend the grimoire: re-summon a kit's *permanent (became-it) page***.
- "Going back" = re-summoning a spirit you *possess* (already conquered) = **forward motion** (re-inhabit, don't rewind).
- **Gated:** only kits you actually *became* (first contact stays a commitment).
- **Motivated by the capstone-you-missed** (re-summon to *finish* the road not taken).
- **[DECISION] The permanent page *remembers that spirit's realized apotheosis*** → first discovery is the *rare roll*; *re-living a known paged spirit* can *deterministically* re-reach the *same* apotheosis. (Randomness in *discovery*, reliability in *re-living* — this resolves the "re-reach the capstone every time" problem.)

**[DECISION] Frame it as ARPG re-spec friction (a deliberate cost, not a chore).** Genre lesson: POE-brutal = commitment-but-exclusion; D3-free = zero-stakes; converged middle = "possible but a deliberate cost." Proposed: ~one free re-summon by endgame (accessibility on-ramp), then a play-earned cost.
- **[FRAGILE]** Materials must accumulate through *normal play* (and thematically through *conquest* — it's a ritual to recall a conquered spirit), **not** dedicated separate farming. "2–3 hours of play during which you also earn it" = fine; "2–3 hours of chore before the fun thing" = resented.
- **[DECISION] Lean *repeatable-with-play-earned-cost*, NOT hard-gated** — the roads-not-taken pursuit is a *major retention engine*; hard-gating throttles it.

**[DECISION] The deterministic backstop is your EXISTING spawn-influence economy, extended.** Re-encountering a paged commander = *pursuing the archetype that contains it* via the keystone/pursue, gear-bias, discover channels.
- **[DECISION] Use the *coarse* (archetype-level) lever deliberately — the granularity gap IS the brutality.** The archetype keystone *narrows* the hunt (agency) but the *last-mile RNG* (which specific kit) *preserves brutality* (you can't pinpoint instantly). Add a *within-archetype pity curve* so "never" can't happen. Do NOT add kit-specific tagging (that's the D3-lenient end). **One new rule needed: paged commanders return to the spawn-eligible pool** (conquered ≠ retired).
- This delivers the desired "90% toward POE-brutal" feel as **brutal *cost/hunt*, not brutal *helplessness*** — the genre's most-resented pattern ("I know exactly what I want, pure chance won't give it, no recourse") is avoided.
- **[DECISION] Extend keystone types/combos with post-hoc engine labels** (a query language over the characterized kit space — free expressiveness from data already computed). **[FRAGILE]** cap query granularity (combo-depth limits or result-set floors so a query always resolves to *several* kits, never one) and expose only *legible* labels (keep illegible internal labels as generation/balance machinery).

**[DECISION] Meta / Maxroll reassessment — the *valuable* anti-meta property survives; the *purist* one doesn't (and was never wanted).** A meta *can* now form (re-summon-leveling-kit → re-summon-endgame-kit → strategy guide). But the *toxic* fear (Fear 1: diversity *collapses* to a few builds) **doesn't apply**, because (a) the game is *serial reincarnation* — even the optimizer *re-lives many kits* (the meta says *which lives to live*, not *one build to lock into* — it doesn't flatten), and (b) content is *generative + seasonal + post-hoc-labeled*, so the meta is *perpetually re-solving* (the engine outruns the netdeckers). **[FRAGILE]** Hold the line: keep deterministic backstops from being *so* generous that a guide routes players *straight to known endpoints, skipping discovery* (discovery → fetching). The **discovery/re-living split** is the guard: guides can optimize *re-living*; they can't schedule *first discovery*.

---

## 7. Gear model

**[DECISION] Two tiers each of legendary and set gear provide the endgame investment depth** that carries the "invested character dominates" fantasy (which, post-PVP-decision, lives in *gear/build* rather than *level*). **[DECISION] Gear is pushed into the battle sim** — so kits are validated *as geared units*, and gear is a *treatment variable* the sim can tune/measure.

**[DECISION] Gear transforms with you (PVE) — it does NOT loot the lieutenant's gear (that's the PVP model).** When you become a new kit, your *own* gear *transmutes* into a kit-relevant version: **essence preserved (tier, gems, power level, legendary/set tier), body re-formed (kit-specific expression).** This is the gear-layer expression of the core metaphysic ("keep the spirit/essence, the body changes") — the gear *reincarnates with you*.
- **[DECISION] Thematic justification: the patron deity bestowed this modular gear on *you specifically*; it is *soul-bound* and resonates with your soul as you descend.** This justifies the transformation (soul-bound gear follows your spirit into each body and re-manifests), deepens the patron-bond (your gear is the deity's gift/leash — gearing-up = deepening entanglement, a *material* dimension to the defiance/escape arc), and motivates the PVE/PVP gear split.
- **[OPEN — the crux] What happens to a legendary's *specific effect* on transformation?** Options: **(A)** effect *transforms into the analogous effect* for the new kit (most seamless, "same legendary re-expressed" — requires an essence→kit-idiom *mapping*, but that's exactly the StyleProfile/parametric philosophy); **(B)** power persists, effect *re-rolls* to kit-appropriate (simpler, identity changes); **(C)** only generic stats persist, effects rebuild per kit (clearest, weakest thematically). **Lean A** (makes gear *truly* reincarnate; consistent with the engine's essence+re-expression philosophy). *(User indicated this is largely mapped already.)*

**[DECISION] A gear-affix scaling/generation function lives in the sim** — `express_gear(power_level, kit) → balanced affixes`, called in two directions that are the *same operation*: looting (target-power = current stage) and possession-transform (target-power = prior-gear-power, kit = new kit). This is the gear-layer instance of the essence+parametric pattern.
- **[FRAGILE / general law restated] "Balanced across all stages" is a claim to VALIDATE, not a formula to assume.** Affixes scale *non-linearly in effect* (CDR, %damage, breakpoints, capstone-synergies). The real work is a **generate → sim → check in-band → adjust** loop (the kit-validation pipeline extended to gear). The possession-transform's "preserve power level" must mean **sim-measured equivalence** ("same in-band position for the new kit"), not "same affix numbers." Scope at the *grouping* level, target *pervasive* mis-scalings.

**[DECISION] Level-range-specific tier-0 legendaries are a *separate* content need** (not covered by scaling — scaling re-expresses *existing* legendaries; the early game needs legendaries that *exist* at low ranges). **[OPEN]** the tier-0/1/2 relationship — *three stages of one growing item* vs. *three separate populations found at different stages* — determines whether this is "design each legendary's entry-tier" or "design an early-game legendary roster." Early build-definers are powerful → must pass the *same sim in-band validation at their stage*. *(User indicated this is mapped.)*

**[DECISION / CRITICAL — sawtooth guard] Gear-affix scaling is by *stage of the game* (itemization), NOT content-difficulty scaling by the player's live power.** The Oblivion treadmill is forbidden. **Test for every scaling instinct: is content *fixed by depth* (player rises to meet it = ✓ sawtooth, backtracking-dominance preserved) or *dynamic by player power* (content rises to meet player = ✗ treadmill)?** Lieutenant gear at depth-X is calibrated to *depth-X's expected tier* (fixed), and the player *brings* appropriate gear *to* that depth — a fully-geared kit *should* dominate shallow floors (that's the *reward*, not a bug to scale away).

---

## 8. PVP design

**[DECISION] PVP is post-launch, team-gated, opt-in, bounded — NOT a launch feature.** Architect the combat/state layer to *permit* future authoritative play (deterministic-friendly, sim/presentation split, serializable state) without building netcode now. See the backend doc for the cost/scope reality (Godot ~40-player/instance ceiling, hand-built netcode, perpetual player-scaling hosting cost, permanent live-ops).

**[DECISION] PVP is *level-50 only* — one bracket.** This dissolves *every* problem at once: no player-scaling needed (everyone has their full kit), no bracket-fragmentation, no twink-vs-leveler asymmetry, full kit fidelity. It is the genre-standard solution, reasoned to from the project's own constraints, and it concentrates the entire PVP population into the *one pool* an indie game can fill.
- **Why brackets are dead:** WoW research + first-hand twink-community knowledge — **bracketed PVP fails at indie scale because it failed at WoW scale.** WoW never *removed* battlegrounds; XP-on/off *segregation* (the "fix" for twink-farming complaints) *fragmented* the twink pool below match-formation density, and region-wide there are no longer enough concurrent players to *pop* a twink bracket. At indie scale, fragmenting an already-small population across brackets × two sides × time zones rounds each pool to ~zero. **Population density, not fairness, is what kills bracketed PVP.**
- **Consequence:** PVP matchups are *cleaner* (everyone fully capstoned — the "final form" arena; the matrix operates on complete kits). The "invested character dominates" fantasy *relocates* from *level-twinking* to *endgame build/gear/kit-mastery* (the two-tier legendary/set depth carries it). The power spectrum *survives* (investment-rewarded), so embraced-imbalance and gang-up-to-possess still apply.

**[DECISION] PVP mode = CTF-on-generals.** You win by *possessing GENERALS* (objectives — keep-what-you-kill aimed at generals, not players) and using that power to *muscle the flag through*. This makes the keep-what-you-kill verb *instrumental to victory* (theme = win condition) and *structurally governs kit-imbalance* (raw kit-power can't win alone — victory routes through *contested* objectives + teamplay). **[FRAGILE / anti-snowball]** generals must be *multiple, retakeable, and vulnerable-while-carrying*.

**[DECISION] In bounded PVP you swap *everything* (kit + gear → standardized/provided loadout).** This is a *fair arena* (no PVE-built advantage carried in), it sidesteps the gear-fit/persistence questions, and it makes PVP reward *kit-mastery-and-play* rather than gear-grind (gear-grind stays a PVE fantasy). Thematically: "the arena's terms" vs. the deity's personal soul-gear.

**[DECISION] Forced kit-swap on the win is *opt-in*, and its positive purpose is DISCOVERY.** "Keep what you kill" turned on other players is the creed made into the highest-stakes swap imaginable. The forced swap converts *observing* an astounding kit into *embodying* it (you taste it from the inside → you crave it → you go back to PVE to hunt it). **PVP is a *discovery engine* that re-opens the discovery the Maxroll meta threatens to exhaust** — powered by the *whole community's* ongoing discovery, which no guide can deplete. The opt-in framing becomes "enter the discovery engine," not merely "accept a wager." (For toxicity safety, forced identity-loss is only acceptable *consensually* — opt-in is that consent; the *default* low-stakes battleground can use copy-not-swap, with forced-swap as the opt-in "total war" variant.)

**[DECISION] PVP cannot converge to a narrow meta — *structurally*, via the one-kit-one-body constraint.** In multi-character games PVE and PVP metas converge independently (you hold both optimized builds). Here a *single body* must serve *both* PVE and PVP, so optimizing one *sacrifices* the other → the rational move is a *hybrid* (good-enough at both), and there are *many* viable hybrid points → the playerbase *spreads* instead of converging. Maxroll *can't* say "respec to the PVP kit" (there's no respec — only *becoming*, which costs your body). This *strengthens* the discovery flywheel (PVP kits are *idiosyncratic personal hybrids*, more surprising than meta kits).
- **[FRAGILE — the condition] The tradeoff must be REAL: PVE-optimal and PVP-optimal must pull in *different* directions.** [MEASURE] whether the divergence is strong enough to force genuine hybrids vs. one kit quietly fine at both.

**[DECISION] PVP is the *home* of enfeeble / control / support builds.** This is how the divergence is *guaranteed* (an archetype-to-mode mapping, not delicate tuning): whole build-families *shine* in one mode and *struggle* in the other. It also *rescues* the support/enfeeble/debuff archetypes that PVE struggles to home (damage-attribution, Possess-gate, indirect-contribution awkwardness) — they get a mode where they're the *stars* — and makes PVP *mechanically distinct* (its own control/denial texture, not "PVE with players").
- **Why it works *automatically*:** PVE is *many disposable targets* (reward *deletion*; CC on fodder is wasted); PVP is *few precious human targets* (reward *control*; CC is decisive). The *same* CC kit is mediocre in PVE and dominant in PVP — the divergence falls out of "hordes vs. humans."
- **[FRAGILE — the lever] target durability.** Tune the flag-bearer and generals *too tough to simply burst down*, so *controlling* them (slow, stop, enfeeble, peel) is *necessary*, not optional. This makes CC *structurally mandatory* in PVP *and* ensures the PVE bruiser's burst kit *doesn't translate* (divergence + discovery firing). **[FRAGILE — tilt, not wall]** PVP *favors* support / PVE *favors* bruisers, but each stays *viable* (not optimal) in the other, so the *hybrid middle* (the diversity/discovery engine) stays populated.

**[DECISION] Possess is a castable ability (the becoming verb), not a game-granted event.** Cast on a weakened champion (Monster-Hunter-capture feel — risk/timing/commitment, better than an auto-prompt). Being a *player ability* (not a *game-granted reward*) is what lets it work across all modes (contention resolves through the cast's rules, not bespoke arbitration).
- **[DECISION] In PVP, gate Possess on enfeeblement as a *mechanic*, not "luck/chance."** A general must be *weakened/enfeebled* to be possessed; CC kits *apply* that enfeeblement → possession is a *skill-legible two-step play* (enfeeble → seize), not a dice roll. CC kits become the *key* to possession (essential) without being the *better solo possessor* (dominant) — they *enable*, the team *executes* → PVP rewards a *diverse composition*, keeping CC *home* without *flattening* the meta. (Gentler variant: CC kits possess *faster/safer*, never *luckier* — legible, not random.)
- **[REJECTED] "Majority damage" gate** for Possess — the documented damage-attribution trap (punishes support/tank/summoner archetypes, incentivizes anti-cooperative damage-racing, invisibly frustrating). (Mostly moot since co-op is cut and lieutenant fights are solo, but the framing stands.)

---

## 9. Co-op decision & the cross-level scaling analysis

**[DECISION] Co-op is CUT (or deferred indefinitely) to preserve the pristine solo vision and protect scope.** Co-op was never the hook; it *taxes* the differentiators (becoming, Goldilocks, kit-fidelity). A focused single-player ARPG is complete and sellable. If any multiplayer is a "fast follow," it is *peer-hosted co-op* (cheap, D2-style listen-server, GodotSteam for NAT/invites) — **PVP is categorically more expensive and is the team-gated capstone, NOT a fast follow** (correcting an earlier mis-ordering).

The analysis that led here (preserved because it informs PVP scaling and the gear model):

**[DECISION / CORRECTION] D4 uses a per-player *scalar split*, NOT a median** (verified by research; my earlier "median" was wrong). In D4 mixed-level co-op, a monster has *no fixed level* — it *deals and takes damage scaled to whichever player it's interacting with*; both contribute and earn level-appropriate loot. Cleanest on *bosses* (clear pairwise target), fuzzier on *hordes* (chaotic attribution). D4 *also* uses *fixed-level floors* for endgame (a two-phase model: per-player scaling while leveling, fixed floors at endgame). The "median" *is* used elsewhere — for *shared abilities* / fixed content — and is forced when a *single shared moveset* must threaten a wide level gap (the scalar split frees you from it *only* to the extent threat lives in the *individualizable* layer).

**[DECISION / KEY DISTINCTION] Scalars individualize; abilities don't.** Damage / health / status-severity / loot are *private pairwise transactions* → per-player, fine. *Abilities* are *shared physical/spatial events* (one position, one moveset, one death) → a singular world can't have contradictory physics. So: **one monster, ONE shared physical behavior, per-player damage/health/severity.** You can give a shared fireball *per-player damage* but not a *per-player moveset*; the monster's *death* is a singular world-fact (resolve via *normalized contribution* — each player's hit = % of their own scale, applied to one shared pool, so both contribute meaningfully).

**[DECISION — the wall that justified cutting co-op] Lieutenant fidelity.** Lieutenants *are* real player kits whose *abilities are their identity* **and a promise of what you'll become** — so they can be *neither flattened nor warped*. The "design level-invariant movesets, let numbers carry scaling" trick works for *fodder* (you control their movesets) but *not* for *kits* (a kit's moveset *grows with level* and *defines* it). In co-op this forced *solo lieutenant duels* (the group clears shared, numbers-scaled fodder; becoming happens in *solo* moments — separating by *presence*, not scaling). Combined with the trilemma — *deep mechanical combat + wide-gap shared co-op + no warping* can't all coexist — this made co-op's cost fall on the exact differentiators, hence the cut.

**[DECISION — clarification] The engine only scales *monsters* (PVE), not players. *Player-vs-player* scaling is unsolved** (and is *why* cross-level PVP is hard) — a player kit *can't* be scaled (abilities = identity + becoming promise = the lieutenant-fidelity wall in PVP form). This is the reason PVP is **level-50-only** (§8): full kits, no level gap, no player-scaling needed.

---

## 10. Social architecture (the actual "play together" answer)

**[DECISION] The desire is *social presence*, not *shared combat* — and those have completely different cost profiles.** The "ghost town" fear is caused by lack of shared *space/systems*, not lack of co-op. Build a social game *without* shared combat (leaving solo combat pristine, backend in the *cheap* managed-services tier — see backend doc):

1. **[DECISION] Shared social hub** — the End-of-Time made multiplayer-present (players coexist, emote, chat, show off kits/grimoire, gather between runs). Cheapest, highest-value; touches combat *zero*; needs only presence sync, not authoritative combat. This is the D2/PoE model (social town, solo/instanced gameplay).
2. **[DECISION] Async competition** — leaderboards / ladders / seasonal races off the grimoire/collection. Intense social engagement, *no* shared instance, none of the co-op problems. (PoE's ladder races are deeply social with zero co-op.)
3. **[DECISION] Guilds** — social structure / belonging / async coordination. Needs a *modest managed-services backend* (moves off Steam-Cloud-only onto a BaaS — predictable cost, not authoritative servers).
4. **[OPTIONAL] Async presence** — Dark-Souls-style traces, fitting the death-cult frame; populates the *solo* descent without co-op.
- **[FLAG] Trading / economy** = a *deliberate heavy decision*, not a default (reshapes loot, invites RMT/dupes, can undermine find-your-own-gear satisfaction). Add only if you want the economy as a pillar.

**[DECISION] Async guild boss fights = achievable; Tier 1 is LOW difficulty.** Tiers, cheapest first:
- **Tier 1 (build this):** shared health pool / contribution threshold; each member *solos their own instance*; backend *sums* contributions. No netcode, no scaling problem, reuses solo combat. Costs: requires the *guild BaaS* (already needed for guilds); **contribution-validation / anti-cheat** (client-reported scores can be faked — the *same* client-trust problem as leaderboards; solve once for all async-competitive systems; *less* severe here because guildmates are cooperative); and aggregate tuning with guild-size fairness.
- **Tier 2 (medium):** relay / persistent shared boss state (better feel, adds persistent-entity state-management + concurrency).
- **Avoid Tier 3** (ghost-replays — fiddly, hollow) and **Tier 4** (synchronous raid — that's the co-op that was cut, smuggled back in).

---

## 11. Cross-cutting principles (the portable lessons)

**[PRINCIPLE] Validate the *generator*, not the *instances*.** Recurred everywhere: dead-end screening (act on classes/skills, not kits), gear-scaling (validate the *logic*, not every affix-combo), stage-validation (validate the *staging mechanism* at checkpoints, not the whole season per level), characterization (measure *behavior*, not *input*). Your levers are coarse and upstream, your problems are systematic → diagnose and fix at the generator level and let the sim tell the truth about what came out. *Most portable thing from this session.*

**[PRINCIPLE] Specification is a hypothesis; measurement is the truth.** (§4, §7.) The gap between what you *meant* and what you *built* is where the real (and dangerous) truths live. The hypothesis-test layer is the engine's truth-telling mechanism.

**[PRINCIPLE] Constraints turned out to be assets.** *One-kit-one-body* (felt like a limit) → PVP anti-convergence *and* the discovery flywheel. *The sawtooth* (a difficulty rule) → the co-op scaling frame *and* the gear-progression frame. *The roguelite reset* (mis-read as a problem) → the elegiac point of the capstone apotheosis. When a constraint keeps *solving* unrelated problems, it's load-bearing and correct.

**[PRINCIPLE] Essence + parametric re-expression** is the engine's signature, applied at every layer: kits (essence + config), gear transformation (essence + per-kit re-expression), gear scaling (essence at a power×kit coordinate), pursuit labels (post-hoc characterization). Consistency across layers is a good sign each is right.

**[PRINCIPLE] Discovery is the soul; protect it from being scheduled.** The discovery/re-living split (randomness in *discovery*, reliability in *re-living*) is the guard that keeps both the re-summon system and the Maxroll meta from hollowing the game into *fetching*.

---

## 12. Validation & engineering scope (resolved this session)

**[DECISION] Endgame (level-50) validation does NOT certify the lower stages — but validate the *staging logic*, not the whole season per stage.** A kit balanced at 50 can be broken at 25 (fewer skills, no capstone, weaker gear — it's a *different thing*). But re-running the *entire* season's in-band filtering at *every* stage is a combinatorial explosion (likely intractable per-season). Instead: validate that the *staging logic* (stat curves, skill-unlock order, gear-scaling function) keeps a *representative grouping-level sample* in-band across **a handful of checkpoint stages** (~4–6 milestones across 1–50); fix the *systematic outliers* at the generator level.
- **[DECISION — the lumpy axis] Skill-unlock progression needs the most careful checkpoint-validation.** Unlike stats and gear (which scale *smoothly*), skills unlock *discretely and in an order* → **non-monotonic in-band-ness** (a kit can be fine at 20, broken at 30 when a strong skill unlocks before its counterbalance, fine at 40). The *partial tree's shape* can be unbalanced even when the *full* tree is balanced. Spend the sim budget here.

---

## 13. Consolidated open questions / live edges

- **[OPEN/TODO]** Mega-Boss matchup-*fairness* tuning ("every kit must beat it" — a forced fight with no Goldilocks fork; a harder target than lieutenant tuning). Live single-player to-do.
- **[MEASURE]** Whether the BC axes *align* with matchup axes (clean matrix) or are *orthogonal* (matchup = added characterization layer).
- **[MEASURE]** Whether the PVE/PVP optima *genuinely diverge* enough to force hybrids (the condition the whole archetype-to-mode + anti-convergence thesis rests on). The CTF-on-generals + target-durability design *points* the right way; confirm strength empirically.
- **[MEASURE]** Production per-kit hours (the binding wall for the launch count); exact density peak on min-spec; capstone-inversion *probability masses* for the matchup distribution.
- **[OPEN]** Legendary *effect* transformation on becoming (A/B/C — lean A); tier-0/1/2 legendary *relationship* (growth-arc vs. separate populations). *(User indicates both largely mapped.)*
- **[OPEN]** Patron-banter tech (LLM vs. templated); emergent-personality cheap-vs-expensive scope; deity's final desire (seal-break vs. holding-back-worse); alias + true-name reveal specifics.
- **[FRAGILE / re-verify]** All backend netcode capabilities and hosting/BaaS pricing (Godot ~40-CCU ceiling, BaaS-for-guilds, perpetual PVP hosting cost) move fast and were planning-grade — re-verify before any spend (see backend doc).
- **[OPEN/probe]** Inanna's stripping-at-each-gate as an escalating-cost-with-depth mechanic (tune against the sawtooth).
- **[OPEN]** Re-summon exact cost/cadence tuning; bestiary internal taxonomy; "don't become it" / re-etch cost definitions.

---

## 14. Cross-references

- Engine, core loop, ontology, **sawtooth**, **Goldilocks**, grimoire, spawn economy, story-frame v2 → `reincarnated-gameplay-loop-design.md`
- Renderer (Forward+), **hybrid horde architecture** (Jolt + MultiMesh), tier targets, **density benchmarks** → `reincarnated-performance-target-specs.md`
- **PVE (clientless) vs PVP (authoritative)** backend, Godot netcode reality, hosting/cost, the architect-but-don't-build directive → `reincarnated-backend-networking-stack.md`

*End of session decisions reference. This doc captures the decisions made in this session; the three cross-referenced docs hold the foundational systems those decisions build on.*
