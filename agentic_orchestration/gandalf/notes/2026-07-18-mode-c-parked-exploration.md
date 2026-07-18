# Mode C — player-selected composition (PARKED exploration record)

> **STATUS: PARKED — zero planning weight.** Matt ruling 2026-07-18 (verbatim): *"Ok, let's just toss mode C for now. I like it but I do not want to plan towards it yet."* This note preserves the full ultra-think verbatim so the exploration is recoverable if Matt re-opens it. Nothing downstream may cite this as direction; no charter, tracker, or spec work builds toward it. (VDM-1 charter §1 records the toss.)

**Date:** 2026-07-18 · **Author:** gandalf (ELICITOR turn, Pattern-B dialogue with Matt) · **Trigger:** Matt's R-5 rider — "What if the meteorb sorc was a samurai orc with fire + shadow…" — player-selected element/race/period/culture over faithful kit anchors.

**Why parked, in one line:** Matt likes it but refuses premature planning; the faithful/generative two-mode emission (R-5) proceeds without it; Mode C would re-enter, if ever, only as a post-run decision against dossier-complete substrate.

---

## The ultra-think, verbatim (session turn, pre-toss)

▶ ROLE: ELICITOR — Mode C ultra-think (journey-shaper + senior-designer lenses both firing; this is the deepest fork you've opened since the death-faith frame).

R-1..R-5 are ruled; the charter draft (G-1) will carry them as its authority block. Now the real work of this turn.

---

# Mode C — The Player-Raised Soul

## 1. The reframe that changes everything downstream — you are not leaving reap-die-rise. You are handing it to the player.

You wrote: *"we would probably alter our core gameplay loop away from reap-die-rise in favor of a more usual character selection mode."* I want to push back on this framing hard, because I think you're undervaluing your own design — and the framing error, if it stands, would make Mode C weaker than it deserves to be.

Look at what Mode C actually *is*, structurally:

> Take a **soul** — a build identity forged in another world (the Meteorb, reaped from D2's corpus) — and **raise it in a new body**: new race, new culture, new period, new element.

That is not a character-select screen. That is **the Rise verb of Reap-Die-Rise, performed by the player's own hands.** The whole pipeline we've been building *is already this ritual*: the crawl **reaps** souls from thirty years of ARPG build-culture; faithful mode **raises them as they were**; generative mode raises engine-authored mutations. Mode C completes the triad — the player becomes the one holding the wand. Solo Leveling's entire power fantasy is one word — *"Arise"* — Sung Jinwoo raising the defeated into his own roster. Mode C is our Arise. The what-if the player has carried for years ("what if the Meteorb sorc was a samurai orc warlock") is a séance they've been waiting to perform since 2003.

And there is a designated empty slot in the architecture waiting for exactly this. The Earth Meta-Layer capture (2026-05-11) locked *"form library = gacha-style accumulation of ascended spirits"* and left *"Earth gameplay loop TBD (MOBA/Pokemon/Arena/combination)."* **Mode C is a candidate answer to that TBD.** Composition doesn't displace the seasonal journey — it lives *between* journeys, at the Earth layer, where the persistent self tinkers with the library of the dead. The seasonal loop proves what the Earth loop composes. "Character selection mode" is the weakest possible skin on this; **the Ossuary — where you raise what you've reaped — is the strongest.** Same mechanics, opposite meaning.

## 2. The decomposition that shrinks the balance problem by two orders of magnitude

Your example sentence contains its own architecture. Read it as a designer: *"what if the **meteorb** sorc [mechanical spine] was a **samurai orc** [presentation] with a hybrid **fire + shadow** combo [mechanical] like a **medieval orc warlock from WoW** [presentation]."* The what-if fantasy decomposes naturally into two axis classes — and they have wildly different balance costs:

| Axis | Class | Balance cost |
|---|---|---|
| Kit anchor (skill loop + chains) | **Mechanical** | bounded by the anchor |
| Element (incl. hybrid pairs) | **Mechanical** | real — must be priced |
| T4 capstone selection (expanded doors) | **Mechanical** | real — must be priced |
| Race | **Presentational** | **zero** |
| Culture | **Presentational** | **zero** |
| Period | **Presentational** | **zero** |

WoW itself is the precedent hiding in your own example: an orc warlock and a human warlock are *mechanically near-identical* and *experientially completely different* — race carries the fantasy, class carries the math. Nobody has ever felt cheated that the orc's Shadow Bolt does human numbers. **Rule race/culture/period as presentation-layer vocabulary** — they drive the LLM generation pass (naming, lore text, flavor, visual descriptors — the llm seam's existing territory) and the modular visual system, and **the simulation never sees the word "samurai."** The fantasy surface stays combinatorially infinite *because it costs nothing to balance.* The mechanical surface collapses to: **anchor × element-combo × capstone-choice × chain-options** — large, but anchored and finite.

One receipt from the substrate: the corpus schema *already* carries `elem_p` / `elem_s` — primary/secondary element structure. Fire+shadow hybrid is representable in data we already hold. The hybrid fantasy isn't a new axis; it's a mostly-NULL column waiting to be lit.

## 3. The balance answer: we don't hand-balance N combinations — we own a convergence loop, and this is what it's *for*

Your stated fear — "difficulty in balancing N-skill combinations and N-capstones" — is the correct fear **for every other studio in the genre.** Blizzard hand-balances; when D3's rune system created ~97,000 nominal combinations, they shipped maybe 30 viable ones and then used sets to dictate the rest top-down. PoE ships maximal freedom and outsources balance to the community's corpse-pile of failed theorycrafts — with the famous paradox that infinite freedom produced *maximal guide-following*, because navigating the space blind is hostile.

We are not them. **The engine's core competency is B14.5's primary loop: recompose-first + hybrid rejection gate + adaptive quick-estimate + convergence-by-simulation.** We already balance generatively — the loop just currently takes *generator*-authored compositions as input. Mode C points the same loop at *player*-authored input:

- **Compile-time convergence.** When the player composes, the engine runs its balance loop *on that specific composition* — quick-estimate first, full convergence behind it. The what-if is balanced-by-simulation the moment it is born. **No ARPG can do this. None has a simulation-convergence layer.** This is the moat, and Mode C is the product surface that makes the moat visible.
- **The rejection gate becomes a pricing gate.** Player input is adversarial input; degenerate combos are certain. But player-facing *rejection* ("invalid combination") is fantasy-hostile — the correct move is **never refuse the séance; price it.** Fire+shadow hybrid carries a visible hybrid tax with a visible ceiling ("-12% base, +crit ceiling" class of tradeoff). KonoSuba understood this: Megumin's explosion-only build is degenerate by every metagame standard and it's *the most beloved build in isekai* — because the fiction acknowledges the cost instead of erroring on it. Degenerate builds are identity gold when priced, poison when silently viable.
- **Determinism discipline carries over.** Two players composing the identical what-if must converge identically — our existing seed discipline (no parallel regens of one seed) generalizes to composition-hash caching. Popular compositions converge once, serve forever; the cache *is* the emerging player-meta, observable in our own telemetry.

The genuinely new engineering (gamora-consult territory, not this turn's scope): compile-latency budget, degenerate detection heuristics ahead of full sim, converged-composition cache. Real work — but *bounded* work, on machinery that exists.

## 4. What we lose and what we actually keep — the naming question

"We would lose the ability to have a faction or a distinctly named kit." Half true, and the half that's true is recoverable:

- **The soul-name survives as lineage.** The composition carries its ancestry line: *"Risen from: Meteorb (Sorceress, D2, 2.x era)"* — which is the *same lineage line* the faithful mode and your devlog citations already run on. The player's samurai orc has a body-name (player-authored or LLM-offered) and a soul-name (the lineage). Identity isn't lost; it's *two-layered* — which is, again, literally the game's reincarnation metaphysics doing product work.
- **Community naming replaces factory naming.** The `folk_name` column in our corpus is the fossil record of players naming what matters — nobody at Blizzard named the Meteorb. If Mode C compositions are shareable (build codes — the **loadout app is the obvious ancestor surface**, already deployed), folk names will grow on our soil. Today's corpus was reaped from other worlds' theorycraft culture; **Mode C is how this game grows its own corpus.** The museum becomes a garden.
- Faction: a composed kit's "faction" is its raiser. "Raised by \<player\>" — the corpus kits have game-of-origin, player kits have player-of-origin. Symmetry holds.

## 5. Is the theorycraft fantasy the larger draw? — yes, *and* the fight is not its rival

The genre evidence backs your instinct: PoE's true endgame is Path of Building — a *third-party theorycraft app* so load-bearing GGG designs around it; D2's 25-year afterlife is build-culture, not content. But the sharp version of the insight is this: **theorycraft without a proving ground is spreadsheet-ware, and proving grounds without authorship are screensavers.** They're not rival draws — they're the two strokes of one engine. And the genre's worst standing sin is the *distance* between them: in PoE, testing a what-if costs a 40-hour level-to-maps slog. Your years-held Meteorb-samurai question has never been answerable in under a week of grinding, in any game, ever.

**Mode C + the battle sim collapses that loop from weeks to minutes.** Compose the what-if → watch it *actually fight* → recompose. "And they fight each other" isn't the competing fantasy — it's the **answer step** of the theorycraft fantasy. The draw isn't the fight; it's the *verdict*.

## 6. Four risks, named honestly (DRIFT-CRITIC duty)

1. **Scope gravity.** Mode C is a third product surface (composition UI + compile-time balance + presentation-variant generation). The One Realm MVP is THE DENOMINATOR and Mode C must not silently enter it. It should be specced as the Earth-layer pillar with its own decision entry — **D-20** — and its MVP relationship explicitly ruled (post-MVP pillar vs. MVP-adjacent prototype gate).
2. **The asset surface.** The fantasy is combinatorially free in *text*; the *visual* is bounded by Synty-modular reality. Phase it the way gacha/isekai media houses do: **text-forward first** (the composition screen describes the samurai orc richly; battle presentation uses tinted/modular approximation), full visual variants as the asset system matures. Do not let the visual ceiling cap the compositional floor.
3. **Degenerate-combo integrity** — covered in §3; the gate must price, never refuse, and *never silently ship broken*. The rubber-stamp detector logic applies here too: a Mode C where every combo converges viable means the pricing gate failed.
4. **The front-door trap.** If Mode C becomes the *entry* experience, the game is a character creator with a battle sim attached and reap-die-rise decays into vestigial fiction. The guard is economic and thematic at once: **raising costs reaped material.** You spend what the seasonal journey harvested to perform the séance. Composition then sits *inside* the loop — reap to afford the rise — instead of replacing it. (This is also, flagged-not-designed: the gacha/form-library economy seam.)

## 7. What this means for the crawl: nothing blocks, one family added — and the fire still burns

You said you want this explored *before* the crawl. Here is the clean sequencing answer: **the crawl's payload is Mode-C-invariant.** Element/race/period/culture are *our-side* authoring axes — no source page holds them. Everything Mode C needs from the sources, faithful mode already needs: the anchor loop, geometry, capstone-alterations (which directly feed the *expanded door* authoring — source ascendancy variants become our multiple T4 doors per kit). One cheap addition earns its place:

- **Payload family 6 — `variants`** (optional, abstain-if-silent): guides routinely list build variants ("budget," "alternate element," "boss-killer"). The corpus's `aliases` field already caught one ("Ngamahu Cyclone (budget variant)"). Variant listings are the source-side map of each kit's *natural option-space* — exactly the raw material for Mode C's "more skill chains with generative options."

So: **explore in parallel, crawl on schedule.** The PoE1 tranche fires before July 24 regardless of where Mode C lands — no Mode C branch is foreclosed by the crawl, and every branch is *fed* by it. Better anchors make better what-ifs; the séance is only as good as the soul's true name.

**Proposed process:** I formalize this ultra-think as the Mode C exploration doc (`reap-die-rise-story/` — it's a story-frame + design-frame artifact), file **D-20** in `matt_decision_needed/` with the forks (mechanical-vs-presentational axis ruling · Earth-layer placement · MVP relationship · raising-cost economy), and pull gamora for the compile-time convergence feasibility read + drax for the loadout-app-as-ancestor read when you're ready to move it from exploration to spec. The empirical gate for ruling D-20: the D-10 pilot cohort emission landing (proves the compile path end-to-end on engine-authored input before we point it at player input) — not time-passage.

---

## 8. Side-note answered: the family dockets are sitting, ratification-ready

The six dockets from the E4 islands run are complete and waiting on your names sitting (they're in the gate roster at `canonical/matt_decision_needed/2026-07-17-atlas-parity-run-gate-roster.md`):

| # | Working label | Seed basis |
|---|---|---|
| 1 | MELEE-STRIKE | engine-key geometry `melee_strike` |
| 2 | IDENTITY-GAUGE | economy model `identity-gauge` |
| 3 | SHAPESHIFT | wereform/shapeshift mech-notes — *ties to the D-05 shapeshift fork* |
| 4 | DOT-AILMENT | poison/hex ctrl + ailment notes |
| 5 | **MULTI-PROJECTILE-VOLLEY** | **the U-1 islet — the largest unseeded coherent island on the plate** |
| 6 | MINION-PET | already Gate-A ratified (7 members) |

Totals: 138 proposed members / 7 ratified seeds / 3 conflict-flags, self-scored precision 0.80–1.00. Your instinct is exact — docket 5 is the standout *structurally*, not just aesthetically: it's the biggest coherent island that no prior family ever seeded, which is precisely what a missing family looks like. The follow-up shape: a **names sitting** (~30–60 min, one session-segment) — you review the six labels + the 3 conflicts + the channel-C melee-axis gap, ratify working labels into canonical family names, and ratified families then *color* on the atlas (the E4 plate's ratified-members-only coloring discipline means families visibly grow as you ratify). If you want, I can fast-track docket 5 solo — pull its member roster now and put VOLLEY up for ratification ahead of the full sitting.

And note the convergence: **ratified families are Mode C's browse vocabulary.** When the player walks the Ossuary choosing a soul to raise, the families are the aisles. The names sitting isn't atlas housekeeping — it's naming the wings of the library the player will one day walk.

---

**Next artifacts queued, in order:** G-1 charter draft (carrying R-1..R-5 + the `variants` family) → Mode C exploration doc + D-20 filing → docket-5 roster if you want the fast-track. Say the word on any or all.