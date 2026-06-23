# Faction-Descent Model + Reward-Differentiation Principle — Recognition Record

> **STATUS:** CURRENT (recognition record as of 2026-06-22). Architectural commitments
> DEFERRED per recognition → validate → commit discipline. Canonical promotion gated on
> the empirical question in §6 + the consults in §7. NOT load-bearing architecture until
> the gate resolves.

**Date:** 2026-06-22
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-06-22 Pattern-B session (continuation of the seasonal-descent
design dialogue). Captures Matt's settled calls (dungeon-keyed faction model; cluster
the full season population; non-duplicative anti-factions; reward must not break the
WR/KPM bands and must not be played-out cosmetic) + gandalf's proposed sharpenings
(cast/bestiary role-partition; contrast-mode inversion; claimable shadows; coverage-not-
ceiling reward principle) — ALL gated per §6/§7.

**Parents:**
- `canonical/story/2026-06-22-seasonal-descent-architecture-recognition.md` — the descent
  vision. **This record resolves its §7 (per-floor theming) and §8 (mega-boss source).**
- `canonical/story/2026-06-22-seasonal-descent-content-audit.md` — engine×requirement
  audit; §4.A amendment established the BUILT-vs-PARKED map this record builds on.
- `canonical/story/2026-05-29-experiential-cascade-architecture-recognition.md` — Step G
  antagonist generation + P5b monster-contrast (the parked seam) + experiential-archetype
  third coordinate. Gate (iii) is the un-park decision this record gives a consumer to.
- `canonical/story/engine-as-general-serial-content-product-2026-05-22.md` §2.2 (P5b),
  §3.4 (`monster_contrast_vocabulary`, `monster_contrast_per_spirit`).

---

## 0. TL;DR

Two linked recognitions emerged:

1. **The faction-descent is dungeon-keyed, not player-keyed.** The descent strings
   together many distinct faction-dungeons, each with its own identity *independent of the
   player's active spirit*. Per-spirit contrast (`monster_contrast_per_spirit`) is REJECTED
   for the descent — it would collapse a journey-of-many-worlds into a hall-of-mirrors.
   The world is the Diablo-2 world-faction model: you traverse the Zakarum and the Council
   regardless of your build.

2. **The collection reward is "coverage, not ceiling."** The 401st claimed form can't be
   *stronger* (that breaks dm=5.0 + the WR/KPM bands) and shouldn't be a played-out
   cosmetic sticker. It is desirable because it **reaches the band in a context the
   player's other forms fall *below* it** — matchup/niche coverage, per-context viability.
   Bounded-viability is not the obstacle to a good reward; it is the *source* of one.

The single load-bearing **question** these rest on (§6): **is per-context viability
measured and player-surfaced today, or only global?** Without it, the coverage reward is
invisible and the loop fails.

---

## 1. What this resolves (architecture-record open questions)

| Architecture record | Open question | This record's resolution |
|---|---|---|
| §7 per-floor theming | How is each floor themed (NOT element)? | Each floor = a **faction** (or its anti-faction); theming is faction-identity, dungeon-keyed. §2. |
| §8 mega-boss source (A/B/C OPEN) | Where does the mega-boss come from? | The **anti-faction lead** = a contrast-mode inversion of the floor-faction's representative; claimable on defeat (Solo-Leveling shadow). Unifies B (held-out sinister faction) + C/D (claim) — but as a *per-dungeon* lead, not a single season apex. §2.3–2.4. |
| audit §4 P1 fork | Which judge / which population? | Single clustering pass over the full season population; within-cluster viability split partitions claimable cast vs bestiary. §2.2. |

---

## 2. The faction-descent model (dungeon-keyed)

### 2.1 Per-spirit REJECTED; dungeon-keyed ADOPTED

A single player-kit advances through many dungeons, each with its own lieutenants + a
descent-specific mega-boss. If every dungeon's enemies were the contrast of the player's
*active* spirit-faction (`monster_contrast_per_spirit=true`), every floor would be a
variation on the same shadow — the world stops being a *place* and becomes a *mirror*,
and the near-infinite faction-dungeon variety collapses.

**Resolution:** the dungeon's faction is **independent of the player's active form**, drawn
from a season-generated faction library. `monster_contrast_per_spirit` is **FALSE** for the
descent profile. This is the **Diablo-2 world-faction model** — the world has its own
factions and the player traverses them regardless of build. (Per-spirit contrast remains
the correct model for a *different* mode — a nemesis boss-rush keyed to the active form —
not the infinite descent.)

### 2.2 The cast and the bestiary — one clustering pass, role-partitioned by viability

Matt's call: **generate the maximal number of coherent player factions across the full
season kit population (~400), then generate non-duplicative anti-factions.** Sharpened by
the **form-ontology** (Matt 2026-06-22: monsters and kits are one object, role-partitioned
— kit = treatment/under-test, monster = control/static-yardstick):

- **One clustering pass over the full ~400** → coherent faction identities (richer than
  clustering the ~34 survivors; supply solved without over-splitting).
- **Within each faction, viability splits the role:**
  - **Viable survivors → the CLAIMABLE cast** (the faction's leader/representative is a
    viable form the player can become and claim).
  - **Non-viable evicted members → the faction's depth-powered BESTIARY** (mobs). They
    failed *as treatment* (non-viable player kits) but are valid *as control* (monsters),
    because a monster's power comes from the depth-curve, not its own converged stats.
    **The kits the pipeline throws away are the monsters the descent needs.**
- **Emergent partition:** a cluster with viable members = a faction with both a claimable
  hero-form and a fightable horde. A cluster with *zero* viable members = a **pure-enemy
  faction** (bestiary + an inverted anti-lead only; you fight it, you cannot become it).
  The viability distribution across clusters *naturally* partitions claimable vs pure-enemy
  factions — no separate authoring needed.

This honors Matt's "cluster the 400" AND the discipline that a claimable form must be in-band.

### 2.3 Anti-faction = a contrast-*mode* inversion (identity, not mechanics)

"Invert the representative kit identity into an anti-faction lead" (Matt) is made precise
by the engine's existing `monster_contrast_vocabulary = {shadow-self, incomprehensible-
ancient, playful-mocker, primitive-tribal, existential-threat}` (serial-content §3.4):

- The anti-faction lead is the faction medoid **run through a contrast-mode** — shadow-self
  → the fallen mirror of the same knights; existential-threat → the cosmic fire that
  consumes heroes. Not arbitrary opposition.
- **Invert the IDENTITY; let the depth-curve set the POWER** (power/identity orthogonality).
  Mechanical inversion is a trap — power comes from the yardstick, not from negating the
  faction's stats.
- **Supply bonus:** F factions × ~5 contrast-modes = up to **5F** anti-faction flavors
  (the shadow-Pirates *and* the cosmic-Pirates are different dungeons). Count without
  over-splitting the cast.

### 2.4 Claimable shadows (the Solo-Leveling extraction loop)

Anti-faction leads are **also claimable.** Defeat the inverted lead → claim its shadow-form
into the library. This is **Solo Leveling's shadow-extraction** — Sung Jinwoo's army is
desirable not because the shadows are strong but because *each is someone he beat, and they
have names* (Igris, Beru, Tank). It **doubles the collection target** (collect the form
*and* its shadow — a duality, not a duplicate) and gives anti-faction dungeons a
reward-identity equal to faction dungeons.

### 2.5 Non-duplication instrument

"Non-duplicative anti-factions" has a built instrument: run the existing `diversity_flag`
(cosine > 0.85, on `ExportFactionCluster`) collision check across the **combined
faction ∪ anti-faction** identity-embedding set; collisions perturb and regenerate.

---

## 3. BUILT vs PARKED (corrected map — audit §4.A)

**BUILT** (cycle-14 close, 2026-06-01; all `provisional_pending_playtest_validation=True`):
- Wave A faction labels (4 clusters, all `faction_label_canonical` non-null,
  `phase7_gate_status="canonical"`, k=4 held), Wave B per-kit identities (34 — Wave B is
  **no longer a phantom**), F-C inter-faction relationships (6; `relationship_type` enum
  {antagonist, rival, allied, neutral, mysterious, parallel}), theming metadata
  (`faction_thematic_tags`, `faction_identity_narrative`, modal lineage/tech/tone).

**PARKED** (Cycle 15+; `monster_contrast_enabled=False`):
- Step G antagonist generation + P5b monster-contrast. Cascade gate (iii) priced the pair
  at ~3–5 wk rocket/star-lord — **but that estimate was for the full per-faction
  contrastive monster-ROSTER pipeline.** This record's design is a **narrow de-scope**:
  per-faction identity-mode inversion (F cheap LLM calls — Step G shrunk to one call per
  faction) + depth-powering of *retained evicted forms* (existing depth-curve) + the built
  collision check. **Plausibly half the estimate or less, contingent on the §7 consults.**

**The descent is the consumer that justifies un-parking** (it answers gate (iii)'s standing
"why build antagonist generation for invisible-faction Reincarnated").

---

## 4. The reward-differentiation principle — coverage, not ceiling

**The problem (Matt):** why want a 401st form when you have 400 — without breaking the
WR/KPM bands, and without a played-out cosmetic?

**The reframe:** in a power-creep game (D3 Paragon, ancient→primal rolls) the only reward
is "bigger number," so collection *dies* at max — the treadmill death the architecture
record §9 already named. Rejecting power-creep (dm=5.0 + bands) is exactly what **frees the
collection to be horizontal**, and horizontal collection *coupled to play* (not cosmetic
stickers) is the kind that survives endgame. Cosmetic feels played-out because it is
**decoupled from play.** The fix is re-coupling differentiation to what you *do*, where you
*go*, or how it *feels* — never to magnitude.

Three axes, all orthogonal to the bands, priority-ordered by hook strength:

| # | Axis | Why desirable | Why band-safe | Genre precedent |
|---|---|---|---|---|
| 1 | **Matchup / niche coverage** (the spine) | The form is the right tool for a dungeon-profile your roster falls below-band against | Per doc 50 viability is *per-context*; a matched form *reaches* the band where others *fall below* — it closes a gap, never lifts the ceiling. Infinite descent → infinite contexts → bottomless | Pokémon type-coverage; D2 "right resist + merc for the area" |
| 2 | **Access / key** (descent-fit) | The form is a passport — attuned to a faction/element/depth-branch, it opens dungeons others can't enter; once inside, in-band | Gates entry, not power. Use sparingly (hard gate); matchup is the default (soft smoothing) — the knob that keeps coverage a *desire*, not a *tax* | Metroidvania lock-and-key; mapped onto the faction-gates |
| 3 | **Play-feel / experiential archetype** (support) | Same numbers, different *activity* — channels-not-bursts, kites-not-anchors | The cascade record's third coordinate is orthogonal to power by construction | Maxroll archetypes; saturates ~5–8, so supporting |

**The binding frame — the form is a *life you lived, reclaimed.*** The memoir layer is not
a fourth mechanic; it is the framing that turns coverage/access/feel from spreadsheet rows
into reincarnation beats. You don't collect "a frost-matched control kit"; you reclaim "the
Frostwidow of the Ninth Seam — the life that learned to fight the cold things." This is the
Earth-Self meta-layer doing exactly the job it was built for.

---

## 5. Generation is free; indexing + surfacing is the work

The ~400 kits already span the BC-axis space — the descent does **not generate "matched"
forms.** It **indexes** existing forms by which contrast-mode-profiles they hold the band
against (a per-form × per-contrast-mode viability matrix), then **surfaces** the player's
worst-covered profile as the gap the next claim closes. That is telemetry + a coverage
readout (elrond/star-lord), **not new generation.** The reward the design is missing is not
a thing to generate — it is *a measurement to expose.*

---

## 6. THE QUESTION (the gate)

> **Is viability measured per-encounter-type / per-contrast-mode today — and surfaced to
> the player — or is it only calibrated globally?**

The matchup-coverage reward (Axis 1, the spine of the whole loop) works **only if** the
engine resolves WR/KPM per-context *and* the descent shows the player "you are below-band in
incomprehensible-ancient dungeons." An invisible coverage-gap creates no desire.

- If per-context viability **is** measured + surfaceable → the reward loop is enabled; the
  remaining work is the index + readout (cheap) and the parked-seam de-scope (§3).
- If it is **only global** → building per-context measurement + player-facing surfacing is
  **the real prerequisite — ahead of any descent content, ahead of cosmetics, ahead of the
  parked enemy-generation seam.** doc 50 is the *design* of per-context viability; this
  record needs to know whether the *telemetry* resolves it.

**This is the decision gate.** Everything in §2–§5 composes cleanly; this one fact
determines whether the next investment is descent content or the measurement substrate
beneath it.

---

## 7. Consults (empirical, team-answerable)

| # | Consult | Owner | Why it gates |
|---|---|---|---|
| C1 | Is per-context (per-encounter-type / per-contrast-mode) viability measured + surfaceable today? | star-lord / elrond / gamora | THE question §6 — reward-loop prerequisite |
| C2 | Are Phase-4-evicted kits **retained** (MAP-Elites archive?) with identities, or discarded at eviction? | rocket / elrond | Retained → free bestiary (§2.2); discarded → small retention build |
| C3 | Re-price the un-park: identity-mode inversion (F LLM calls) + depth-powering retained evicted forms + collision check | rocket / star-lord | Confirms the §3 de-scope vs the ~3–5 wk gate-(iii) estimate |
| C4 | Per-faction viable-member count across clusters at the 400→cluster scale | elrond / gamora | Confirms enough viable members per cluster for a claimable leader (§2.2) — and identifies the natural pure-enemy factions |

---

## 8. Discipline composition

| Discipline | Honored how |
|---|---|
| Recognition → validate → commit | Synthesis captured NOW; architectural commitment DEFERRED to §6 question + §7 consults |
| Form-ontology (Matt 2026-06-22) | Cast/bestiary partition IS the role-partition (treatment/control); claim = moving a form across the partition |
| Power/identity orthogonality | Anti-faction inverts identity; depth-curve sets power; reward is coverage (identity/context), never magnitude |
| Empirical-inspection-over-assumption (#11/#6) | The faction→monster "backwards" finding was corrected by reading the parked design (audit §4.A); per-spirit assumption corrected by Matt |
| No power-creep (D3 anti-pattern) | The reward principle is explicitly the rejection of the Paragon/number-inflation treadmill |
| #13 implicit-pillar drift | Reincarnated's invisible-player-factions stay invisible as a *player-identity* surface; the descent makes factions visible only as a *world/enemy* surface (no collapse) |

---

## 9. What this record does NOT do

- Does NOT commit the un-park of Step G / P5b (gate (iii) decision; §6 question precedes it)
- Does NOT lock the reward axes as final (recognition; doc-promotion gated on §6)
- Does NOT build descent content ahead of the §6 measurement answer
- Does NOT lock the contrast-mode taxonomy beyond the existing `monster_contrast_vocabulary`
- Does NOT reverse the BUILT post-hoc kit-clustering — it builds the enemy side *forward*
  on top of it

---

**Signed:** gandalf (story-and-design steward)
**Authority:** Matt 2026-06-22 Pattern-B session — settled calls + invited sharpenings, all gated
**For:** capture of the dungeon-keyed faction-descent model + the coverage-not-ceiling
reward principle at recognition-record level, with the per-context-viability-measurement
question (§6) as the decision gate before descent-content investment.
**Next checkpoint:** §6 question answered (C1) → reward-loop enablement disposition → Matt
Pattern-B at re-engage.
