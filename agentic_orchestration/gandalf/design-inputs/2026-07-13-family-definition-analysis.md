# What defines a kit-family, independent of member count?

**Author:** gandalf (Pattern-B sustained design analysis) · **Date:** 2026-07-13
**Charge:** the §4 crux of `2026-07-13-family-definition-ultrathink-prompt.md` — a member-count-free
definition of "family" that survives the "family ≠ strict cell" sub-question, a member-count-free
identity/texture partition criterion, and the treatment of zero/one-member families and gaps.
**Grounding:** all family claims reproduced against `corpus.db` (`row_class='combat-kit'`, 470 rows,
`PRAGMA query_only=ON`) via the reranked FCA PoC and a targeted wildcard spot-check
(`/tmp/family_spotcheck.py`). Numbers below are the reproduced run, not the prompt's recollection.

---

## 0. The one-sentence answer, then the derivation

> **A kit is a point. A family is the largest behavioral plateau around it.**
> Formally: a family is a maximal, axis-aligned region of coordinate-space over which *combat
> behavior is invariant* to the coordinates it leaves free. Member count is how densely we have
> *sampled* that region — never what *defines* it.

Everything below derives this, breaks the framings that deserve breaking (the structural grounding
as a *definition*; the partition assumption; corpus-absence as a coherence test), confesses the one
knob the reframe relocates rather than removes (minsup → ε), and turns the definition into a
production pipeline whose most valuable output is the empty cells.

---

## 1. The frame that makes member-count obviously irrelevant: families are *fibers of a map*

Set up the space precisely.

- Let **Ω** ⊆ D₁ × … × D₁₄ be the **compossible domain** — the coordinate-vectors that correspond
  to a *realizable, non-degenerate* kit (the engine can instantiate it and it fights). Most of the
  14-D product space is *not* in Ω (e.g. `range=melee · delivery=projectile` is a contradiction).
- Let **B: Ω → S** be the **behavior map** — a kit's signature in the fight simulation (the gamora
  gauntlet): its damage-over-time profile, time-to-kill distribution, matchup vector, tempo curve.
- A **kit** is a point *x ∈ Ω*. It is *realized* if a real combat kit sits there (in the corpus);
  it is a *gap* if the point is in Ω but no kit has been built there yet.

Now the definition writes itself:

> A **family** is (an axis-aligned approximation to) a **level set / fiber of B** — a region on
> which B is constant to within a behavioral tolerance ε.

**Why this kills member-count in one stroke:** *B is a function on Ω. It is defined at every
compossible point, whether or not a kit happens to sit there.* Its fibers exist independent of how
we sampled the domain. The corpus is a finite, biased *sample* of Ω; member count is **sampling
density**. A cartographer does not decide whether a valley exists by counting how many hikers are
standing in it. The valley is a feature of the terrain (B); the hikers are the corpus.

- A **family of many** = a fiber we have sampled densely (six franchises independently walked into
  the same valley).
- A **family of one** = a fiber sampled once.
- A **family of zero** = a fiber of B with *no sample yet* — a valley no one has hiked. This is not
  a degenerate case; it is the **Mendeleev gap**, and it is arguably the point of the whole exercise
  (§6).

This is exactly the periodic table done correctly. A chemical *group* (family) is defined by
valence-electron configuration — a partial specification that *causes* shared chemical behavior —
**not** by how many elements populate it. Group 18's identity ("full valence shell → inert") was a
coherent family when only argon was known; helium, neon, krypton, xenon, radon filled in later.
Astatine (group 17) was predicted from its *position* before it was ever isolated. The group is a
level set of "chemical behavior as a function of electron structure." Population never entered the
definition — only the *confirmation*.

---

## 2. The identity/texture partition — and why it must be *behavioral*, not structural

A fiber of B, written in axis-aligned form, *is* an identity/texture partition:

- **Identity (pinned) coordinates** = those on which B *depends* in this region. Move one and the
  build plays differently → you have left the fiber.
- **Texture (wildcard) coordinates** = those on which B is *invariant* in this region. Move one and
  the fight is unchanged → you are still in the same fiber. These are flavor: element skin, the
  exact resource book-keeping, cosmetic geometry.

The partition is therefore **per-region / contextual by construction** — it is "which coordinates
does B locally depend on," and B depends on different coordinates in different neighborhoods. This
is precisely the geometry-for-whirlwind paradox the charge insists any criterion must survive, and
the behavioral frame *explains* it rather than merely tolerating it (§2.2).

### 2.1 The three candidate groundings, judged

**(i) Design-semantic** ("does changing this coord alter the class fantasy?"). *Member-count-free,
correct in spirit, but not self-executing.* It is the human articulation of the same thing B
measures — "does it play differently?" I keep it, but as the **cross-check and final authority on
feel**, not as the operational criterion. A rubric an LLM/designer applies per coord is real and
useful (it is how we adjudicate when the sim is silent or suspect), but it cannot be the *ground* —
judgment needs an anchor, and "how it plays" is the anchor.

**(ii) Structural** (near-twin manifold-thickness; NMI / Cramér's V redundancy). **I demote this
from "definition" to "candidate-generator," and the reasons are decisive:**

1. *It is not member-count-free even in letter.* Near-twin counts and mutual information are
   computed over *pairs of realized cells* — they are population statistics. A family of one has no
   near-twin; a family of zero has no manifold. The structural signal is literally undefined exactly
   where the reframe most needs an answer.
2. *It is a global average and therefore blind to context — the fatal flaw.* The finding
   `delivery~geometry NMI = 0.445` and geometry's high near-twin count say geometry is texture
   *on average across the corpus*. But "on average" is a population-weighted mean of B's local
   dependence. Whirlwind is the region where geometry *is* identity; that region is a small fraction
   of kits, so it is drowned in the average. **A global structural metric can never see a local
   identity coordinate.** That is not a tuning problem; it is the wrong instrument.
3. *It cannot evaluate the maximality condition at gaps.* Testing "can I free this coord?" means
   evaluating B at a point that may have zero members. Structural methods need member pairs there;
   they have none. So they can only *approximate* families from observed density — the very thing we
   are trying to stop doing.

**(iii) Simulation-behavioral.** **This is the ground I trust, and it is the only one that is
member-count-free *by construction*:**

1. B(x) is defined for a *single* point. You can perturb one coordinate of a lone kit — or of a
   *hypothetical* kit at an empty cell — and re-simulate. Families of one and zero are handled
   natively.
2. It is *natively contextual*: "does perturbing coord c move B" is asked in the local region, so
   geometry-is-identity-for-whirlwind and geometry-is-texture-for-nukers both fall out correctly.
3. It grounds "family" in *how the build plays* — the thing we actually ship to a player — rather
   than in data density, which is an accident of which franchises we crawled.

**Operational criterion (the definition, stated testably):** a subcube F (pinned set P at values
v_P, everything else wildcard) is a **family** iff

- **(Invariance)** for every wildcard coord c ∉ P: sweeping c over its domain, holding v_P fixed,
  leaves B constant within ε — *no wildcard is behavior-determining anywhere in F*;
- **(Irreducibility)** for every pinned coord c ∈ P: sweeping c *does* move B by > ε for some point
  in F — *every pin earns its place*;
- **(Maximality)** F is not properly contained in another subcube satisfying the above.

All three conditions reference B under perturbation. None references member count.

### 2.2 Why this survives "family ≠ strict cell" (the sub-question you may not dodge)

A **strict cell** is a maximally-pinned subcube (all 14 fixed). It is a family **only if it is
irreducible** — only if you cannot free a single coordinate without B changing by > ε. Empirically,
almost no cell is irreducible. The reproduced whirlwind fiber proves it:

```
[7 kits · lift 2119.6] full-move · self-origin · flat · whirlwind · damage · defense=tank ·
                        proxy=solo · range=melee · tempo=high · commit=channel · dependency=one-shot
        varies (texture): function{hard-stop,hex,knockback,none} · economy{free,reserve,spend} ·
                          activation{active,triggered}
```

Ten whirlwind kits across nine strict cells collapse to **one** fiber once you free the coords B is
invariant to (function/economy/activation and, at coarser grains, amp/defense/proxy/tempo). The
nine cells were never nine families; they were one family, sampled nine times with different flavor.
The *cell* is the finest sampling grid; the *family* is the coarser plateau of B. They coincide only
for a genuinely irreducible kit — an archetype so distinctive that every coordinate matters. Such a
kit is itself an interesting output (a "maximally-specified, singular archetype"), but it is rare.

So the collapse-into-cells is prevented not by fiat but by the **invariance + maximality**
conditions, both of which are member-count-free. The naive subcube framing alone does *not* prevent
collapse (all-pinned subcubes = kits); the *behavioral* conditions on the subcube do.

---

## 3. The structure is a **cover / lattice, not a partition** (Fork B, from first principles)

Because the identity/texture split is contextual, "same family" is **not transitive** and families
**overlap**. Two subcubes with different pinned sets can share members; a coord pinned in one region
is free in another, so you cannot simply intersect them. This is not a defect — it is the correct
ontology, and it is Fork B (nested multi-grain) re-derived from B rather than read off the FCA
artifact:

- A kit belongs to a **nested stack** of families at different grains — exactly as iron sits in
  *both* group 8 *and* period 4. The reproduced whirlwind lattice shows this directly: an 11-pin
  fiber (7 kits, lift 2120) nests inside 8-pin fibers (6 kits, lift 482 / 233) that free
  economy/defense/proxy/tempo. Same archetype, three legible resolutions.
- The consequence for the "periodic table": **there is no single canonical 2-D grid.** Any flat
  table is a *projection* onto two chosen family-systems (like group × period). The earlier finding
  "a legible table only appears as a projection" was not a limitation of our data — it is a theorem
  about a contextual behavior map. The clean grid is a **view**; the lattice is the **ontology**.

This retires Fork A (one destructive grain) on principle: destroying coords to force a partition
would discard the contextual identity of coords like geometry, which are texture globally but
identity locally. You would merge whirlwind into "generic melee" — a design catastrophe (below).

---

## 4. Recovering the known families (grounded, this run)

**Whirlwind — recovered, lift 2119.6, Jaccard 1.0 to the gold label** (§2.2). Identity =
`self-origin · whirlwind · damage · melee · channel · one-shot` (+ full-move/tank/solo/high at the
tight grain); texture = function/economy/activation (+ amp/defense/proxy/tempo at coarser grains).
The *player consequence* of getting this right: Cyclone (PoE1), Whirlwind (D2/D3/D4/Immortal),
Warpath (Last Epoch), EoR (Grim Dawn) *feel like the same fantasy* — move-while-you-spin, sustained
melee AoE — and the table says so, across six franchises, unsupervised.

**Trap/Mine — recovered, and it demonstrates the crux.** The FCA-tight fiber is clean:

```
[6 kits · lift 1426] full-move · at-target · totem · damage · defense=tank · economy=cooldown ·
                     proxy=heavy · range=ranged · commit=instant · dependency=apply→detonate
        e.g. gd-mortar-purifier, poe1-{ea-ballista, fire-trap, glacial-cascade-mines, seismic-trap}
```

But my *naive* hand-pin `{activation=triggered, dependency=apply→detonate}` grabbed **15 mixed
members** — control *and* damage, projectile *and* totem, `poe1-detonate-dead` next to
`poe1-hexblast-mines` next to `d2-summonmancer`. That is the whole lesson in one query: **choosing
the pinned set wrongly under-constrains into mush or over-constrains into a cell.** Which coords are
identity is not read off the tokens' names; it is decided by whether B moves when you free them. The
behavioral test is what separates "deployed-remote-detonator archetype" from "everything that
happens to detonate."

**Channeled-Beam — recovered, and it is the textbook context-dependence case.** Reproduced:

```
[7 kits · lift 232.7] rooted · beam · flat · proxy=solo · tempo=high · commit=channel · active
        varies: geometry{beam_channel,chain,cone,vortex_pull} · treatment{control,damage} · …
        e.g. di-ray-of-frost-wizard, gd-{aar,drain-essence,flames-of-ignaffar}, poe1-incinerate
```

Spot-check of two members:
```
di-ray-of-frost-wizard   rooted|beam|flat|beam_channel|control|hard-stop|glass|reserve|solo|dual|high|channel|active|apply→detonate
ud-flamethrower-channel  rooted|beam|flat|cone|damage|none|glass|reserve|solo|dual|high|channel|active|one-shot
```

They share `rooted · beam · flat · glass · dual · high · channel` and split on
**treatment (control vs damage)**. Now — treatment is a *never-demote-core* coord globally (the
near-twin=0 finding: treatment is never the sole difference between two cells). Yet *inside the beam
region it varies across family members.* Two honest readings, and only B can adjudicate:

- If, for a rooted channelled beam, the delivery+channel so dominate the fight that control-vs-damage
  barely moves B → treatment is *locally texture* and this is one beam family.
- If control-beam (a Ray of Frost that hard-stops) plays materially differently from damage-beam
  (an Incinerate that ramps) → treatment is *locally identity* and the beam family **splits in two**.

This is not a flaw in the method; it is the method *asking the right question*. The near-twin=0
global evidence says "treatment is almost always identity" — so the prior is *split* — but the final
call is B's. (This is also why B's level sets are not perfectly axis-aligned: "damage-beam OR
control-beam, each with its own economy" is an L-shaped region we approximate with one or two
subcubes. Honest limitation, named in §7.)

---

## 5. Method implications — lift is *demoted*, FCA is *elevated*, B becomes the arbiter

The lift approach conflated three things the reframe cleanly separates. **Confirmed, refined:**

| | Question it answers | Metric | Member-count role |
|---|---|---|---|
| **Definition** | *What is this family?* | identity/texture partition (fibers of B) | **none** |
| **Validation** | *Is it real / a natural kind?* | cross-**source** recurrence + bootstrap stability | evidence, **source-weighted** |
| **Prioritization** | *Which to build first?* | population + market salience | legitimate ranking input |

Refinement to the charge's lean: validation is **cross-source**, not cross-member. Six kits from six
franchises (whirlwind: D2/D3/D4/Immortal/PoE/GrimDawn/LastEpoch) is overwhelming evidence a fiber
carves reality at its joints; six kits from one game's skill tree is one designer's habit. The
reproduced run makes this measurable — every high-lift fiber is cross-franchise; the lift-1.1 mush
(`126 kits · treatment=damage · function=none · … · everything varies`) is the null family and is
*correctly* garbage. The empty band between lift ~125 and lift ~1 is the real/accidental boundary,
and it exists because *fun mechanics get copied across studios* — behavioral coherence and
cross-source recurrence are correlated, which is *why* lift worked as a finder at all.

**The production pipeline becomes:**

1. **Candidate generation (cheap, data-only).** FCA closed-concept lattice over realized kits.
   Each formal concept *is* a candidate subcube (intent = pinned coords, extent = members) — FCA was
   the right tool for a deeper reason than we knew: **its lattice is literally the subcube lattice
   the definition needs.** Run it at low minsup; annotate every concept with support, **lift, and
   source-diversity**. *This is the only place lift lives now — a triage annotation that points the
   expensive apparatus at promising regions. It never defines a family and never gates its
   existence.*
2. **Behavioral partition test (expensive, the definition).** For candidates above a triage floor,
   run the gamora gauntlet perturbation: sweep each pinned coord (must move B) and each wildcard
   (must not, within ε). Promote to **family** iff invariance + irreducibility + maximality hold.
   This *adjusts* the split FCA proposed (FCA pinned `economy` for whirlwind because the sample did;
   B frees it). **B is the arbiter of the identity/texture line.**
   *Attention budget:* do not sim-test the never-demote-core coords (delivery/treatment/control/
   proxy/activation/dependency) — the global near-twin=0 evidence already pins them. Spend the sim
   budget on the *demotable-with-evidence* coords (amp/geometry/defense/economy/range/tempo/commit),
   which is exactly where context-dependence lives. The register's core/demotable split thus becomes
   **the simulation's attention budget** — a clean tie-in to ratified canon.
3. **Validation (confidence).** Cross-source recurrence + bootstrap stability of the partition +
   gold-label recall (whirlwind/trap/beam). Member-count re-enters *only here, as evidence*.
4. **Gap enumeration + coherence (the prize — §6).**
5. **Prioritization.** Population + market salience over confirmed families *and* coherent gaps.

Steps 2 and 4 use the **same oracle** B: step 2 asks "which coords are texture" (fibers of B); step 4
asks "is this empty point coherent" (domain of B). One simulation apparatus, two questions.

---

## 6. The prize: gaps as predictions

Once families are fibers of B over identity-space, an **empty coherent cell is a predicted
archetype** — territory no ARPG has claimed. This is where "breadth is the pitch" becomes concrete.

**Coherence = membership in Ω (the domain of B).** A gap is *coherent* iff the engine can
instantiate its signature and it fights non-degenerately. This is the exact inverse of the family
question, and — as the charge suspected — it **shares the answer**: families are the *fibers* of B;
coherent gaps are the *domain* of B. Same object.

**Enumeration.** From each *confirmed* family signature, generate Hamming-1/2 neighbors in
identity-space (flip one or two pinned coords) that currently have zero members. Do **not** enumerate
the whole product space — it is astronomically large and mostly void; the valuable gaps are the
*germanium-next-to-silicon* ones, adjacent to rich families.

**Coherence filter — and a sharp warning.** Rank candidates by:
- *compossibility* — sim can instantiate + non-degenerate (the definitive test);
- *adjacency* — Hamming distance to the nearest rich family (near = easy to reach, easy to sell as
  "the X you know, but Y");
- *design-value* — does it fill a hole in the player's build-fantasy space?

**Do NOT use corpus co-occurrence to define coherence** (§7.5) — "delivery=projectile never appears
with range=melee in 470 kits" cannot *define* incoherence, because a family of zero is supposed to
be valid, and "never observed" is exactly what a valuable gap looks like. Corpus-absence is a *weak
prior* for prioritization at most; **sim-feasibility is the arbiter** of coherence.

**Player/design consequence.** Each coherent gap is a **greenlit archetype brief**: "no shipped ARPG
has built the *rooted control-beam that builds→spends into a detonation* — here is its mechanical
signature; here are its two nearest cousins (Ray of Frost, Incinerate); go design it." That is the
periodic table doing what Mendeleev's did: predicting the element before it is found. It is the
single most defensible piece of the "breadth" pitch, because it is *generative*, not inventory.

---

## 7. Failure-mode critique — where "member count doesn't matter" breaks, and the safeguards

Honest pressure on my own reframe. It is right for *definition*; it has real edges.

1. **The sim is the oracle — garbage in, garbage out.** If the gauntlet mis-models kiting, movement,
   or sustain, B will call the relevant coords "inert" and merge families that a human plays as
   distinct. *Safeguard:* the design-semantic rubric (§2.1-i) is a **mandatory** cross-check, not
   optional. When B says "texture" but a designer says "this changes the class fantasy," the flag
   points at the sim, not at the designer. **Human-feel is the final authority on "does it play
   differently"; B is the scalable proxy that must be audited against it.** (DRIFT-CRITIC guard:
   never let the cheap proxy silently redefine the expensive truth.)

2. **ε is the knob we *relocated*, not removed.** The whole partition hinges on "> ε." Small ε →
   everything is identity → collapse toward 457 cells. Large ε → everything is texture → a handful
   of mega-families. So the reframe trades **minsup** (a member-count threshold) for **ε** (a
   behavioral-sensitivity threshold). I will not hide this. ε is nonetheless the *better* knob:
   (a) grounded in gameplay, not data density; (b) interpretable — "how differently must two builds
   play to be different archetypes" is something a designer can reason about; (c) **calibratable
   against gold labels** — choose ε so whirlwind/trap/beam resolve at the grain designers agree on.
   The reframe's honest cost is one named, defensible, calibratable constant.

3. **Zero-member gaps over-generate, and coherence ≠ fun.** The number of compossible empty cells can
   dwarf the realized ones, and B measures *works* and *balanced*, not *fun*. A gap can be coherent
   yet unfun — which is often *why it is empty*. Member-count/recurrence remains load-bearing for
   **confidence**: a fiber six studios converged on is proven-fun; a gap is a *hypothesis*. Genre
   precedent is blunt here: Grim Dawn's dual-class system yields thousands of "compossible" combos of
   which a minority are build-viable and the rest are coherent-but-trap; Diablo III shipped
   mechanically-valid class sets that sat unused until itemization made them *fun*. *Safeguard:* the
   three-way split itself — a gap is a **prototype brief, never a mass-production greenlight.** It
   must pass validation (playtest, market signal) before it becomes shipped content. The reframe is
   right that member-count does not *define*; it is wrong if it tempts us to skip the confidence gate.

4. **No clean partition → no canonical table.** Contextual identity means overlapping families and
   no single 2-D grid (§3). Players/marketers expect a tidy periodic table. *Safeguard/reframe:* ship
   the lattice as the ontology and *chosen projections* as the views (delivery×treatment = 12 cells;
   identity-spine = 78). "The table" is a UI affordance over a richer truth, and that is fine — the
   real periodic table is also a projection of a higher-dimensional quantum structure.

5. **Corpus-compossibility contaminates coherence with member-count** (already flagged §6). Using
   "never co-occurs" to define "incoherent" re-imports member-count through the back door and would
   erase the very gaps we value — it conflates *absent-because-forbidden* with
   *absent-because-unclaimed*. *Safeguard:* only sim-feasibility defines coherence; corpus-absence
   only prioritizes.

6. **Circularity in the contextual partition.** "The region determines which coords are relevant;
   the relevant coords determine the region" is a fixed-point definition and may have several
   solutions or be seed-order-sensitive. *Safeguard:* define it *constructively* — seed from a
   high-triage candidate, greedily free any coord that tests inert, stop at maximality — and verify
   **bootstrap stability**. Accept multiple stable fixed points as the *overlap structure* (a
   feature), but reject unstable ones as artifacts.

7. **B's level sets are not perfectly axis-aligned.** The beam control/damage split (§4) is the live
   example: the true behavioral region can be L-shaped, and a single subcube either over- or
   under-covers it. *Safeguard:* allow a family to be a small *union* of subcubes when B demands it,
   and treat "this fiber wants to split" as a legible design finding (it means the archetype has two
   sub-fantasies), not a bug.

---

## 8. Bottom line

- **Definition (member-count-free):** a family is a maximal axis-aligned region on which the fight-
  simulation behavior B is invariant to its free coordinates — a fiber of B. A kit is a point; a
  family is the largest behavioral plateau around it. Member count is sampling density of the domain,
  never a property of the map.
- **Family ≠ strict cell** because a cell is a family only if *irreducible* (no coord can be freed
  without moving B), which the invariance+maximality conditions enforce and which almost no cell
  satisfies (whirlwind: 10 kits, 9 cells, 1 fiber).
- **Identity/texture partition:** per-region, decided by whether perturbing a coordinate moves B >
  ε. Trust the **simulation-behavioral** ground; keep **design-semantic** as mandatory cross-check
  and final authority on feel; demote **structural** to a cheap candidate-generator.
- **Sizes 0 and 1 are first-class:** one = a fiber sampled once; zero = a fiber not yet sampled = a
  Mendeleev-gap prediction, the highest-value output.
- **Method:** lift is demoted from definition to a triage annotation in FCA candidate-generation;
  FCA is elevated (its lattice = the subcube lattice); B is the arbiter of the pin/wildcard line;
  member-count/recurrence re-enters only as *validation evidence* (source-weighted) and
  *prioritization*.
- **Gaps:** coherence = membership in the domain of B (sim-feasible + non-degenerate), *not*
  corpus co-occurrence; enumerate as Hamming-1/2 neighbors of confirmed families; ship as archetype
  briefs behind a validation gate.
- **Honest cost:** we relocated the tuning knob (minsup → ε), we depend on a trustworthy sim, and
  coherence ≠ fun — so member-count stays load-bearing for *confidence* even though it is banished
  from *definition*.

The reframe is correct and it is the right one for a periodic table: **define families by the map,
confirm them by recurrence, prioritize them by population — and let the empty cells become the
game's promises.**
