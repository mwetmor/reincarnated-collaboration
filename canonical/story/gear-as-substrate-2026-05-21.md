# Gear as Substrate — Coalescence-Time Identity Generation

> **STATUS:** HISTORICAL-INFORMATIVE (pre-Epoch-4; consult for lineage only — not current truth) — see `canonical/00-ground-state.md` for current truth

**Date:** 2026-05-21 (evening, post substrate-as-cohesion validation probe)
**Author:** gandalf (story-and-design steward)
**Status:** DRAFT — pending Matt review + decisions-log entry
**Authority:** design-architectural; commits substrate-architecture extension
**Companion to:** `canonical/story/substrate-design-supplement-2026-05-21.md`, `canonical/story/multi-dim-convergence-algorithm-2026-05-21.md` v1.1, `canonical/story/build-defining-resonance-formula-2026-05-21.md`

**⚠️ Timing revision (2026-05-21 evening, post BDI resonance formalism):** Phase G timing in § 11 of this doc originally targeted post-P7 (v1.1/v2 work). Per Matt 2026-05-21 evening decision: **gear-as-substrate moves into V1 pre-gauntlet scope (P1-P2 territory).** Rationale captured in § 0.5 below. Phase table in § 11 superseded by protocol amendment doc `agentic_orchestration/hive-mind-protocol-amendments-2026-05-21-evening.md`.

---

## 0. TL;DR

**Gear becomes the fourth substrate axis** — peer to elemental substrate, range substrate, role substrate. Selection happens **BEFORE the gauntlet fires**, at coalescence time. Once selected, the gear-archetype is **locked as identity-substrate**: the balance loop converges *around* it, the cohesion-judge *reads* it, and the class's identity *includes* it.

**The non-negotiable constraint:** "blunderbuss must be viable in battle simulation." Gear-substrate is mechanically real — it carries geometry, tempo, range, and stat-shape signals the sim simulates. It is NOT flavor decoration applied post-hoc.

**The clean landing pad:** `balance_loop.py:858` already has `_gear_loadout_cycling_hook(...)` as a named no-op stub. Matt named this hook himself, anticipating a future where gear participates in coalescence. That future is now.

**v1 / v2 trajectory:** v1 ships with a starting gear-archetype catalogue (~10-15 archetypes); v2 expansion proceeds in lockstep with elemental substrate growth. Parallel growth axes.

---

## 0.5 Why V1 pre-gauntlet (timing revision, 2026-05-21 evening)

The original phasing in this doc placed gear-as-substrate as post-P7 v1.1/v2 work, on the rationale that adding a 4th substrate to P5 cohesion-judge work would conflate two empirical tests (3-substrate validation vs 4-substrate expansion).

The **build-defining resonance formalism** (`canonical/story/build-defining-resonance-formula-2026-05-21.md`) supersedes that rationale by surfacing a deeper structural argument:

### 0.5.1 The combinatorial-richness argument

Build-defining moments live in **interaction terms** (β-pairs and γ-triples per the BDI formalism). The genre's signature builds (rank-3 in the BDI taxonomy) require three substrate components in resonance.

**Without gear-archetype as substrate:**
- Substrate space = 7 × 4 × 4 = **112 vectors** (element × range × role)
- Pairwise interactions ≈ 72 possible β-pairs
- Triple interactions = 112 (each vector is trivially a single triple of its three components)
- Signature-build rank-3 space is **shallow**: only one triple per vector; identity differentiation depends entirely on pair-level β

**With gear-archetype as substrate:**
- Substrate space = 7 × 4 × 4 × 15 = **1,680 vectors**
- Pairwise interactions ≈ 313 possible β-pairs across substrate dimensions
- Triple interactions = C(4,3) × per-axis-values ≈ exponentially richer
- Signature-build rank-3 space is **deep**: multiple distinct triples per vector; identity differentiation has structural room to operate

**The QD archive cannot search the rank-3 space that the BDI formalism predicts contains the genre's signature builds without gear-substrate as a 4th axis.** The substrate-as-cohesion validation probe (4.35 / 5.0) confirmed cohesion-judge recognizes resonance at 3-substrate; the BDI formalism predicts the deeper signature-build moments live at 4-substrate rank-3 resonance.

### 0.5.2 The Tier 4 keystone authorship argument

Tier 4 keystones are **rank-completers** (BDI § 6) — they take a kit's rank-2 resonance and promote it to rank-3 by adding the third leg.

**If the substrate space is rank-2-shallow** (no gear-substrate), Tier 4 keystones have nowhere to complete TOWARD. They become flavor-altering keystones at best, not identity-anchoring rank-completers. The math note v1.1 SD-1 framing ("Tier 4 keystones are mechanic-altering") only achieves its full architectural promise when the substrate space is rank-3-deep enough to support rank-completion.

**Gear-substrate in V1 is the structural precondition for Tier 4 keystones to be build-defining.**

### 0.5.3 The empirical-test rebalancing

The earlier "two empirical tests conflated" concern was about P5 cohesion-judge integration. That concern remains valid — but the resolution is NOT to defer gear-substrate. The resolution is to **sequence the empirical validation:**

- **3-substrate cohesion-judge** validates first (probe 2026-05-21 returned 4.35; P5 confirms at production scale)
- **4-substrate cohesion-judge** validates as **delta** on top of 3-substrate baseline — within the same P5 phase, but as a measurable scope addition (per P5 prompt-priorities 4 + 5)
- The two tests are now **stacked, not conflated** — clean attribution preserved

### 0.5.4 The architectural-stub argument

`_gear_loadout_cycling_hook` (named by Matt; no-op in V1) was already an architectural stub anticipating this future. Activating it during the V1 rebuild — not deferring to post-P7 — was the original architectural intent. The earlier "post-P7" framing was conservatism, not architecture.

### 0.5.5 Updated phasing summary — SUPERSEDED by 0.5.6 LITE path

Phase table in § 11 of this doc is **superseded** by the LITE-path decision in § 0.5.6 below + the protocol amendments doc.

### 0.5.6 LITE path adopted (2026-05-21 evening, post Matt cross-repo concern)

**Decision:** the full V1 inclusion proposed in § 0.5.1-0.5.5 above is REPLACED by a "**gear-as-substrate LITE**" path that threads a middle road. Authored after Matt surfaced the cross-repo concern that legacy archetype-locking removal (W0.2) leaves demo (Pixi.js) + Unity production + loadout app (React) without canonical class-identity-to-gear coherence between now and P7.

#### The LITE path — what it is

**`signature_gear_archetype` becomes a DERIVED TAG in v1, not a generative substrate.**

A class's signature gear-archetype is computed at class-generation time by a deterministic rule:

$$\text{signature\_gear\_archetype} = f(\text{dominant\_element}, \text{role\_orientation}, \text{range\_profile}, \text{stat\_distribution\_signature})$$

The function f is a rule table mapping substrate-vector → gear-archetype. Stat distribution is **already canonical and deterministic** per `element_biases.py:28` `ELEMENT_SCALING_ATTRIBUTE` (verified 2026-05-21 evening): fire/water/lightning/shadow → INT; earth/wind/holy → WIS; physical → STR. The rule table can therefore produce sensible assignments without empirical calibration.

#### What the LITE path preserves

| Concern | LITE path treatment |
|---|---|
| Engine-internal disciplined sequencing (Matt's original instinct) | ✅ Preserved — gear is NOT a generative substrate in v1; BDI tests run at 3-substrate scale + signature_gear_archetype as derived-tag context |
| Cross-repo coherence (Matt's new concern) | ✅ Solved — demo/Unity/loadout have a canonical class-identity-to-gear contract |
| BDI rank-3 detection in P1 | ✅ Partially recovered — tests can probe signature_gear_archetype as proxy 4th dimension without committing it as generative |
| P5 cohesion-judge scope | ✅ Light prompt extension only — not full 4-substrate |
| v1.1/v2 promotion path | ✅ Clean — field exists; rule-table becomes search-space; no schema retrofit |
| The "blunderbuss must be viable in battle simulation" discipline | ✅ Preserved — sim-viability of each archetype in the rule table's value-set is verified before catalogue locks |

#### What the LITE path defers

- **Substrate-vector composition with gear_archetype as 4th generative input** — defers to v1.1/v2 (post-P7) when the rule-table is promoted to a search-space
- **BC archive's gear-archetype axis as a generative dimension** — defers to v1.1/v2
- **Full P5 cohesion-judge gear-archetype recognition (priorities 4 + 5 in full form)** — light version in P5; full version in v1.1/v2
- **Spirit-swap meta-layer "Spirit's Core Gear" gameplay loop** — defers to post-P5 (unchanged from earlier framing)

#### The two-tier semantic preservation

The two-tier distinction from § 2.3 of this doc is preserved by the LITE path:

| Tier | Scope | v1 LITE behavior |
|---|---|---|
| **Gear-archetype** (substrate identity) | "blunderbuss" / "censer" / "kanabō" | **DERIVED-TAG**: set at class generation; persistent as identity metadata; consumed by demo/Unity/loadout/cohesion-judge |
| **Gear-instance** (per-fight roll) | The +180-DEX, scatter-burst, cold-shot blunderbuss that drops at fight 7 | UNCHANGED from current procedural pipeline |

#### Updated phasing — LITE path

| Phase | Scope | New timing |
|---|---|---|
| G0 (architectural commitment) | This doc + decisions-log entry | DONE (this conversation) |
| **G1-LITE** | Rule-table v1 (15 archetypes; deterministic rule table mapping substrate-vector → gear-archetype) | Pre-P1 (gandalf + Matt design call; tomorrow's session) |
| **G2-LITE** | Generation-pipeline `signature_gear_archetype` computation + telemetry column + per-class persistence | **P1** (~3-5 days; rocket) |
| **G3-LITE** | (DEFERRED) gear-instance generation constrained by archetype | Deferred to v1.1/v2 |
| **G4-LITE** | Cohesion-judge light prompt extension (judge receives signature_gear_archetype as identity hint) | **P5** (~1 day; star-lord) |
| **G5-LITE** | Loadout app + demo + Unity consume signature_gear_archetype for class-identity rendering | **P1+** (drax + Unity team; parallel work) |
| **G6** (UNCHANGED) | Spirit-swap meta-layer integration (Spirit's Core Gear) | Post-P5 (unchanged) |
| **G7-LITE** | (DEFERRED) 4-substrate empirical validation gate | Deferred to v1.1/v2 promotion gate |
| **G-PROMOTE-v1.1** | Promote signature_gear_archetype from derived-tag to generative substrate (rule-table → search-space) | v1.1/v2 (post-P7) |

#### Cost summary — LITE vs full

| Path | P1 scope cost | P5 scope cost | Cross-repo coherence | Post-P7 retrofit |
|---|---|---|---|---|
| Full V1 inclusion | +2-3 weeks | +1-2 weeks | Solved | None |
| Pure deferral (original Matt instinct) | None | None | **Risk** | +3-4 weeks |
| **LITE (adopted)** | **+3-5 days** | **+1 day** | **Solved** | **~1-2 weeks** (rule-table → search-space promotion; clean schema) |

The LITE path produces ~1 week of v1 engine work + drax/Unity unblocked + ~1-2 weeks of clean v1.1/v2 promotion. Net cost across v1+v1.1 is **smaller than either pure deferral OR full V1** by ~1-2 weeks total, AND solves the cross-repo coherence concern immediately.

#### Why this is the right architectural call

1. **Stat distributions are already canonical** (`ELEMENT_SCALING_ATTRIBUTE` verified 2026-05-21 evening) — the rule table operates on stable foundation
2. **Drax + Unity team can ship player-facing surfaces** on a canonical class-identity-to-gear contract without ad-hoc mapping that would conflict with eventual v1.1/v2
3. **BDI tests can still probe rank-3 at 4-dim proxy** by using signature_gear_archetype as a derived 4th substrate axis in measurement (without commitment as generative)
4. **The Tier 4 keystone catalogue (T4-B; P3-P4)** can be authored gear-anchored OR gear-agnostic; the gear-anchored option becomes available because signature_gear_archetype exists, but is not forced
5. **Cohesion-judge sees the identity** as light hint (P5 priority 4 in lightweight form); P5 dispositive empirical test remains at 3-substrate
6. **v1.1/v2 promotion is clean** — schema field already exists; promoting from rule-table to search-space is a generation-pipeline change, not a retrofit across BC archive + cohesion-judge + sim

---

## 1. The architectural reframing

### 1.1 What gear is today

Per fact-check (2026-05-21) of current engine state:

| Layer | Current behavior | Citation |
|---|---|---|
| Gear generation | Procedural per-tier per-slot; rolled at gauntlet time | `gear_generation.py:1188` `generate_season_gear_pool` |
| Class-gear linking | `class_fit_profile` — gear-fit-to-class is a **downstream metric** | `gear_generation.py:831` |
| Balance role | Gear modulates win-rate via `compute_balance_gear_stats(archetype_tag, percentile)` | `balance_loop.py:2465` `_evaluate_gear_variance` |
| Cycling hook | `_gear_loadout_cycling_hook(...)` exists but is **no-op in V1** | `balance_loop.py:858` |
| Cohesion-judge visibility | **No.** Gear is invisible to identity-formation layer | substrate-as-cohesion validation probe (2026-05-21) |

**The arrow runs class_archetype → gear_stats.** Class identity is upstream; gear is downstream. Gear's job is to make sim variance realistic.

### 1.2 What gear becomes

| Layer | New behavior |
|---|---|
| Gear-archetype selection | Coalescence-time substrate input alongside element + range + role |
| Gear-archetype scope | Locked at generation; the kit IS its gear-archetype |
| Per-fight gear stats | Still procedural (downstream from gear-archetype; tier/affixes/quality vary) |
| Balance role | Balance loop converges **with gear-archetype fixed** as substrate constraint |
| Cycling hook | Reframed: substrate-vector-selection-time mechanism, not recompose-time fallback |
| Cohesion-judge visibility | **Yes.** Gear-archetype is a fourth substrate dimension the judge reads |

**The arrow inverts: gear_archetype → class_identity (coalescence) → gear_stats (per-fight rolls).** Identity is generated jointly across all four substrates; downstream stat rolls remain procedural.

### 1.3 Why now

The substrate-as-cohesion architectural recommitment (2026-05-21) and its small-sample empirical validation (4.35 mean coherence; probe returned this evening) made this possible. Three converging conditions:

1. **W0.2 substrate-agnostic mechanical generation** removed the hard-coded archetype templates that previously stopped gear from being a substrate (the templates already prescribed weapon-type implicitly)
2. **Cohesion-judge as identity-namer** means substrate signals don't need to be hard-coded; the judge reads mechanical signature and assigns identity
3. **Probe verdict** confirms cohesion-judge can recognize substrate from raw mechanical signature at small sample — adding a fourth signal (gear-archetype) extends the judge's substrate-recognition surface rather than overloading it

Matt named `_gear_loadout_cycling_hook` weeks ago, recognizing the architectural slot but lacking the surrounding QD-coalescence framework to fill it. The framework now exists.

---

## 2. The two layers — Identity and Mechanical

The non-negotiable constraint ("blunderbuss must be viable in battle simulation") establishes that gear-substrate operates on **both layers simultaneously**:

### 2.1 Identity layer — gear-archetype as substrate-signal

The cohesion-judge receives gear-archetype as a substrate input alongside element, range, role. Gear-archetype carries:
- **Geometry signature** (scatter, line, arc, sweep, point, area, beam)
- **Tempo signature** (slow / measured / fast / burst / channeled)
- **Range signature** (melee / medium / ranged)
- **Cultural/genre stance** (pirate, inquisitor, knight, shaman, witch, monk, mercenary, etc.)
- **Vocabulary signal** (the gear-archetype name and its associated lexicon flow into naming prompts)

The cohesion-judge then names the class identity: "holy + ranged + slow + AOE + glass + blunderbuss → **Holy Pirate Sniper**" is exactly the identity-disambiguation move the substrate-as-cohesion architecture is designed for. Strip the blunderbuss and the same substrate stack could be a Crusader-with-heavy-bolts or an artillery-inquisitor — three distinct identities, gear disambiguates.

### 2.2 Mechanical layer — gear-archetype as sim-input

The gear-substrate is *not* a thematic veneer over arbitrary mechanical content. The blunderbuss carries:
- Real ranged-scatter geometry → simulation hits multiple targets with falloff
- Real slow rate-of-fire → simulation models reload windows
- Real damage-shape (heavy single-projectile or shot-spread) → simulation resolves per-fight DPS
- Real stat-shape preferences (DEX for handling, STR for kick-absorption, INT-low) → class stat distribution coheres with weapon

**If the sim cannot deliver a viable Holy Pirate Sniper with the blunderbuss as substrate, the substrate vector is REJECTED and a different gear-archetype is selected** (see § 4 generation pipeline). The substrate is not allowed to be "we'll figure out how to make it work" — it must convergence-pass with the gear-archetype as a binding constraint.

This is the discipline that keeps gear-as-substrate from drifting into pure flavor. The blunderbuss has to fight.

### 2.3 Gear-archetype vs gear-instance — the two-tier distinction

| Tier | Scope | Lifecycle |
|---|---|---|
| **Gear-archetype** (substrate) | "blunderbuss" / "censer" / "kanabō" / "greatsword" | Fixed at class generation; identity-binding |
| **Gear-instance** (per-fight roll) | The specific +180-DEX scatter-burst blunderbuss with cold-shot affix that drops at fight 7 | Procedural; rolled in gauntlet per current pipeline |

**Existing gear_generation.py code remains LARGELY intact for gear-instance work.** What changes: gear-instance generation now constrained to instances OF the class's locked gear-archetype, rather than free-roll across all base types. The class's `gear_archetype` field becomes a generation-time input to `sample_scenario_loadout`, filtering candidate base types.

---

## 3. Gear-archetype taxonomy v1 (proposed)

This is a **starting catalogue** for Matt review. v2 expansion is gated on substrate-availability growth. The catalogue is the substrate equivalent of the 7-element table in the substrate supplement.

**Each archetype defines:** geometry signal, tempo signal, range signal, archetypal stance, sample identity names.

### 3.1 Hand-weapon archetypes (melee, physical-anchored)

| # | Archetype | Geometry | Tempo | Range | Stance | Identity examples |
|---|---|---|---|---|---|---|
| 1 | **Greatsword** | arc/sweep | slow | melee | knight-overwhelming | Crusader, Warlord, Black Knight |
| 2 | **Twin daggers** | point/multi-hit | fast | melee | rogue-precision | Assassin, Cutpurse, Shadow Strider |
| 3 | **Battle spear / longstaff** | reach/line | medium | melee-medium | disciplined-distance | Lancer, Monk, Spear Sage |
| 4 | **Mace / warhammer** | impact/concussive | slow | melee | paladin-or-warlord | Templar, Smiter, Smithlord |

### 3.2 Ranged-weapon archetypes

| # | Archetype | Geometry | Tempo | Range | Stance | Identity examples |
|---|---|---|---|---|---|---|
| 5 | **Longbow** | line/precision | medium | ranged | hunter-clean | Ranger, Sharpshooter, Sentinel |
| 6 | **Crossbow** | line/heavy | slow | ranged | mercenary-tactical | Bolt-Captain, Inquisitor-Marksman |
| 7 | **Blunderbuss / scattergun** | scatter | slow | ranged-medium | pirate-outlaw | Holy Pirate Sniper, Powder Inquisitor, Rust Skirmisher |
| 8 | **Throwing knives / chakram** | multi-projectile | fast | medium | assassin-harasser | Nightblade, Ring-Dancer |

### 3.3 Caster-weapon archetypes (energy-channeling)

| # | Archetype | Geometry | Tempo | Range | Stance | Identity examples |
|---|---|---|---|---|---|---|
| 9 | **Wand / focus rod** | single-line | fast | medium-ranged | precision-mage | Stormcaller, Frost Lancer, Voidpiercer |
| 10 | **Orb / sphere** | area/burst | medium | medium | elementalist-area | Witch, Stormbringer, Pyromancer |
| 11 | **Caster staff** | high-payoff | slow | ranged | archmage-grandeur | Wizard, Stormking, Pyresage |
| 12 | **Tome / grimoire** | conjuration | medium | indirect | summoner-scholar | Necromancer, Conjurer, Pact-Scholar |

### 3.4 Ritual / holy archetypes

| # | Archetype | Geometry | Tempo | Range | Stance | Identity examples |
|---|---|---|---|---|---|---|
| 13 | **Censer / thurible** | area-aura | slow | medium | cleric-sustain | Aegis-Priest, Smoke-Cleric, Inquisitor |
| 14 | **Holy symbol / icon** | beam/line | medium | medium-ranged | exorcist-smite | Exorcist, Judgment-Bringer |
| 15 | **War-trumpet / horn** | cone-AOE | slow | medium | evangelist-blast | War-Priest, Trumpet-Saint |

**v1 cut: 15 gear-archetypes.** v2 expansion candidates include whip/chain, naginata/kanabō, polearm/halberd, veil/shroud (offhand-substrate), elementalist-shard, ritual-mask. These wait until the cohesion-judge has empirically demonstrated stable archetype recognition on the v1 catalogue.

### 3.5 Taxonomy discipline

**Each gear-archetype must satisfy:**

1. **Mechanically distinct** — the geometry × tempo × range combination is not redundant with another archetype (otherwise the cohesion-judge can't disambiguate)
2. **Culturally legible** — genre-canonical or genre-canonical-adjacent (Diablo / PoE / isekai vocabulary applies)
3. **Sim-viable** — convergence loop can produce balance-converged kits with this archetype as substrate constraint (this is the "blunderbuss must fight" discipline)
4. **Identity-generative** — the archetype changes what the cohesion-judge names; element + range + role + archetype produces an identity that element + range + role alone does not

Archetypes that fail criterion 3 (sim-viability) MUST be removed from the substrate catalogue, not retained as "thematic only." Substrate is substrate.

---

## 4. Generation pipeline integration

### 4.1 Where gear-substrate enters

The current generation pipeline (post-W0.2):
```
season_orchestrator → bc_target_composer.compose_kit()
  inputs: (element, range, role, tier, seed, ...)
  output: mechanical kit (skills + stats + BC coordinates)
```

The extended pipeline:
```
season_orchestrator → gear_archetype_selector → bc_target_composer.compose_kit()
  inputs: (element, range, role, gear_archetype, tier, seed, ...)
  output: mechanical kit (skills + stats + BC coordinates + gear_archetype_id)
```

**Gear-archetype selection happens BEFORE the gauntlet.** This satisfies Matt's directive: "put the gear cycling before the gauntlet."

### 4.2 Substrate vector composition

For each class slot in a season:
1. **Substrate vector composed:** (element, range, role, gear_archetype) — four-axis substrate
2. **Mechanical kit generated** with substrate vector as input; gear-archetype shapes geometry preferences, tempo preferences, stat-shape preferences during skill selection
3. **Gauntlet runs** with gear-archetype FIXED; balance loop converges modifier + multi-dim parameters (per W1.13) around the locked substrate
4. **If non-convergent at locked substrate:** generation REJECTS the substrate vector and recomposes — typically by varying gear_archetype OR element, depending on which substrate is signaling weakest
5. **On convergence:** kit + gear_archetype passed to cohesion-judge for identity naming

### 4.3 `_gear_loadout_cycling_hook` reframed

The current hook fires INSIDE `_recompose_gauntlet`, post-primary-loop-failure, as a no-op extension point. **The reframing moves the active gear logic UPSTREAM** to substrate-vector composition.

The hook itself can be repurposed two ways:
- **(A) Per-fight gear-instance variation** — the hook becomes the place where per-fight gear-instance stat rolls happen, varying the *quality* of equipped gear within the locked archetype, for variance-modeling purposes (closer to current intent)
- **(B) Removed entirely** — substrate composition handles all gear logic; the hook is deleted as no-longer-needed

**Recommendation: Option A.** The hook still does real work (gear-instance variance is a real balance concern; B14.3 gear-percentile variance check depends on it). It just operates on instances within the locked archetype, not on archetype selection.

### 4.4 Multi-dim convergence interaction (W1.13)

Per math note v1.1, multi-dim convergence operates over 5-6 dimensions (per-node SP, T4 keystone selection, trigger interaction, scalar modifier, tier scaling, gear-affix provisional). **Gear-archetype is NOT a convergence dimension.** It is a substrate — fixed before convergence runs.

This is the same architectural status as elemental substrate. The convergence loop's job is to find balance WITHIN a locked substrate; it does not get to swap substrates mid-convergence. Swapping substrates is a generation-time reject-and-recompose action, not a convergence-step move.

This keeps the convergence dimensionality bounded and the substrate semantics clean.

---

## 5. Cohesion-judge implications (P5)

### 5.1 Prompt scope expansion

The substrate-as-cohesion validation probe (2026-05-21) tested cohesion-judge on three substrate dimensions (element, range, role). The probe verdict (4.35 mean coherence, high-confidence validation) establishes the cohesion-judge can perform at three substrates.

Adding gear-archetype as a fourth substrate is a **scope expansion, not a re-architecture**. The judge receives:
- mechanical signature (skills, stats, geometries, effects, BC coordinates) — unchanged
- substrate vector (element, range, role, **gear_archetype**) — adds the fourth dimension
- task: assign cohesive identity name + thematic prose

### 5.2 Gear-archetype as identity-disambiguator

The probe surfaced **three failure modes** the gear-substrate may help mitigate:

1. **Three-element contamination** (class_0016 → 3.5) — gear-archetype provides an *anchoring* substrate signal. If three elements are present but the gear-archetype is "blunderbuss," the dominant identity becomes "scatter-pirate with mixed-element munitions" rather than "fragmented multi-element generalist." Gear is the tie-breaker.

2. **Capstone identity alignment** — gear-archetype constrains which capstone designs cohere. A T4 teleport on a blunderbuss class reads as "powder-blink shot" coherently; on a longbow class it reads as a mobility break. The gear-substrate disambiguates capstone interpretation.

3. **Control × fire awkwardness** — gear-archetype rescues awkward element × role pairings by providing a third anchor. "Fire + controller" alone is awkward; "fire + controller + censer" reads cleanly as "smoke-cleric burning silence-aura inquisitor."

**The gear-substrate is a force-multiplier for cohesion-judge accuracy on edge cases.**

### 5.3 P5 prompt-engineering scope addendum

The P5 prompt-engineering priorities (surfaced by the probe) now extend to include:

4. **Gear-archetype recognition** — judge must read mechanical signature for gear-archetype-consistent signals (scatter geometry + slow tempo + ranged-medium → blunderbuss-class) and validate against the supplied substrate-vector gear_archetype field

5. **Gear-archetype × element cross-coherence** — judge must handle gear-element pairings that carry strong genre-precedent (holy+censer, shadow+veil, lightning+wand) AND surprising-but-evocative pairings (holy+blunderbuss = pirate-inquisitor; shadow+horn = whispering evangelist)

This adds ~2-3 weeks to P5 cohesion-judge work scope. Acceptable; the validation gain is significant.

---

## 6. Spirit-swap / meta-layer integration

This is where the gear-substrate framing connects most deeply to Reincarnated's design DNA.

### 6.1 The "Spirit's Core Gear" framing

Each spirit form in the Earth-Self form library carries:
- **Class identity** (the spirit's substrate vector: element + range + role + gear_archetype)
- **Signature gear-substrate** — the gear-archetype that completes the spirit
- **Gear-instance state** — whether the player has acquired a gear-instance of the signature archetype

A spirit-form loaded WITHOUT its signature gear-substrate is **partial identity**:
- Mechanical effect: degraded effectiveness (recommend 60-75% of full-substrate output, not 0%; the spirit still functions but underperforms)
- Narrative effect: visible "incomplete" framing in UI; the spirit is yearning for its weapon
- Gameplay effect: the player has a clear in-season goal — acquire the substrate-gear

### 6.2 Seasonal journey beat — acquiring the substrate-gear

This creates a clean gameplay loop:

1. Player loads a spirit-form for the season (e.g., Holy Pirate Sniper)
2. The spirit drops in **without its substrate-gear** (or with a degraded placeholder)
3. The season's loot table is weighted so that **at least one blunderbuss drops by mid-season** — guaranteed-by-progression, not RNG-cruelty
4. Acquiring the substrate-gear is the "identity-completion event" — a narrative beat, not just a stat upgrade
5. Higher-tier instances (epic / legendary) of the substrate-gear can drop later as endgame goals

This is **the genre-canonical "find your weapon" arc** — the legendary sword that recognizes its master, the staff that channels its true bearer. It is also **deeply isekai**: Rudeus and Aqua Heartia, Kazuma and Chunchunmaru, Subaru and his whip. The named weapon is identity-completion, and the journey to acquire it is the arc.

### 6.3 Cross-season persistence

The Earth-Self meta-layer accumulates spirits across seasons (gacha-form-library). The substrate-gear state persists per spirit:
- A spirit acquired three seasons ago, used in two seasons, may have its legendary substrate-gear unlocked
- A newly-acquired spirit starts with no gear-instance unlocked
- The substrate-gear unlock is a **per-spirit** persistent attribute, surviving body-swap

This makes the form library deeper. A 30-spirit collection isn't just "30 spirits" — it's "30 spirits at varying levels of substrate-completion." Some are signature-weapon-mastered; some are still pursuing their core gear.

### 6.4 Earth-meta-layer hooks (deferred)

The post-Phase-0 rift events (PVP/PVE) may include "substrate-gear ascension" mechanics — competitive or cooperative paths to upgrading a spirit's substrate-gear tier. **Deferred** as Earth-gameplay-loop work; flagged here as integration point.

---

## 7. Identity-with-class vs identity-with-gear — design call

The genre has two patterns:

| Pattern | Example | Implication |
|---|---|---|
| **Identity-with-gear** | PoE (Mjölner Discharger, Voll's Devotion, Crown of Eyes) | Swap the weapon, become a different build |
| **Identity-with-class** | Diablo II Sorceress (Frost Sorc identity persists even when swapping orbs) | Class is the identity; gear modulates expression |

**For Reincarnated, identity-with-class is the right call.** Reasons:

1. **Matches spirit-swap meta-layer.** Spirits are persistent identities. "Holy Pirate Sniper" IS a spirit, not a build-configuration of generic Mage class.
2. **Matches gacha-form-library.** Each spirit is a distinct collectible identity, not an interchangeable mechanical chassis.
3. **Avoids PoE complexity-explosion.** Pure identity-with-gear creates combinatorial gear-build space that demands wiki-grade theorycrafting infrastructure; Reincarnated targets a more accessible audience.

**Substrate-gear is "this spirit's signature gear" not "swap-it-and-become-someone-else."** The spirit IS the Holy Pirate Sniper; the blunderbuss is the spirit's substrate-completion gear. Equipping a different weapon is *substrate-incomplete play*, not *build-respec*.

This call should land in the decisions-log as a design-architectural commitment.

---

## 8. Genre-precedent calibration

This is canonical genre territory. The position:

| Game | Gear's identity role | Reincarnated position |
|---|---|---|
| D1 | Decorative (weapon-of-warrior is flavor) | Below us |
| **D2** | Anchoring (Frozen Orb Sorc — gear anchors build name) | **Adjacent** — substrate-anchored identity |
| D3 | Dominant (Sunwuko Monk, Inna Monk — class is ~40% identity) | Below us — we don't want gear to overwhelm class |
| D4 | Aspect-driven (gear delivers active class-defining traits) | Adjacent to Reincarnated mechanically; we add archetype-as-substrate layer above |
| PoE | Pure gear-as-identity (Mjölner Discharger) | Above us in identity-with-gear depth |
| LE | Item-faction substrate (gear-as-identity-substrate explicit) | **Closest peer** — explicit substrate framing |
| GD | Mastery × set bonus identity | Adjacent — different substrate axis |

**The closest analog is Last Epoch's item-faction system**, which explicitly designs gear as identity-substrate rather than identity-modifier. Reincarnated's gear-as-substrate framing is more conservative (identity-with-class preserved) and more genre-evolved (named gear-archetype taxonomy + spirit-swap meta-layer integration).

**Isekai resonance:** strong, as discussed. Named-weapon-as-identity is canon. The genre will recognize this pattern.

---

## 9. v1 → v2 trajectory

### 9.1 v1 starting state

- 10-15 gear-archetypes in the v1 catalogue (per § 3)
- Cohesion-judge prompts include gear-archetype as fourth substrate
- Per-spirit substrate-gear-state persistence in form library
- Seasonal "acquire substrate-gear" journey beat
- Identity-with-class commitment (decisions-log)

### 9.2 v2 expansion

Parallel to elemental substrate growth (canonical/32 + math note v1.1 § 13):
- v2 catalogue: 20-30 gear-archetypes
- Cohesion-judge prompt-engineering matures for combinatorial substrate-pair coverage
- Earth-meta-layer rift events introduce substrate-gear ascension paths

**v2 trajectory is substrate-availability-gated**, identical to elemental substrate growth gating. The two growth axes proceed in lockstep — adding gear-archetypes when there are enough elemental substrates to combinatorially fill the substrate-vector × gear-archetype matrix without identity collapse.

### 9.3 Out-of-scope for v1

- Multi-slot substrate (offhand + armor + weapon all contributing substrate signals; v1 keeps it weapon-only)
- Gear-archetype evolution (a spirit's substrate-gear changing across player levels; v1 keeps it fixed)
- Cross-class substrate-gear sharing (one blunderbuss across multiple Holy-pirate-sniper variants; v1 keeps it per-spirit)

These are real design questions; they wait until v1 stability is empirical.

---

## 10. Substrate proliferation cost — bounded

With gear-archetype in, Reincarnated has **four substrate axes**: element (7), range (4), role (4), gear-archetype (~15 v1). The combinatorial space is **7 × 4 × 4 × 15 = 1,680 substrate vectors**, of which only a subset is genre-coherent (a holy + offensive-melee + control + tome is awkward; a holy + ranged + control + censer is canonical).

**Risk:** cohesion-judge degradation at four-substrate scale. The probe showed 3-element contamination → 3.5 coherence; a fourth substrate dimension could compound the contamination failure mode.

**Mitigations:**
1. **Hierarchical substrate priority in cohesion-judge prompt** — element is primary; range and role are modulators; gear-archetype is the *disambiguator-of-last-resort* that resolves ties between near-identity classes
2. **Gear-archetype coherence-check at substrate-composition time** — reject substrate vectors with strong genre-incoherence at the vector level (a fire + ranged + control + censer is awkward; the composer can prefer fire + ranged + control + scattergun)
3. **v1 catalogue conservatism** — start with 10-15 gear-archetypes, all genre-canonical; expand only after cohesion-judge empirically holds at 4-substrate scale
4. **P5 cohesion-judge prompt-engineering scope** explicitly addresses gear-archetype recognition (see § 5.3)

The proliferation cost is **real but bounded**. The probe verdict's 4.35 lower bound + the gear-archetype's identity-disambiguating role (§ 5.2) together suggest the four-substrate architecture *increases* cohesion-judge accuracy rather than degrading it. To be empirically verified.

---

## 11. Implementation phases

| Phase | Scope | Owner | Gate |
|---|---|---|---|
| **G0** | Architectural commitment (this doc + decisions-log entry) | gandalf draft + Matt approve | This conversation |
| **G1** | Gear-archetype taxonomy v1 finalization (10-15 archetypes locked) | gandalf + Matt | Matt design-call |
| **G2** | BC target composer extension (gear_archetype as 4th substrate input) | rocket | jack-ryan Gate-1 |
| **G3** | Gear-archetype-constrained gear-instance generation (`sample_scenario_loadout` filter by archetype) | rocket | jack-ryan Gate-1 |
| **G4** | Cohesion-judge prompt extension (P5 scope addendum) | star-lord (LLM seam) | jack-ryan Gate-2 |
| **G5** | `_gear_loadout_cycling_hook` reframed for per-fight gear-instance variance (Option A in § 4.3) | gamora | jack-ryan Gate-2 |
| **G6** | Spirit-swap meta-layer integration (Spirit's Core Gear persistence) | knight-rider sequences across drax (loadout app) + star-lord (telemetry) | Matt approval |
| **G7** | Cohesion-judge empirical verification at 4-substrate scale | legolas (Mode A probe — parallel to substrate-as-cohesion probe pattern) | gandalf review |

**Phase timing:** G0-G3 are P1-P2 territory (parallel to W1.13 multi-dim convergence work). G4-G5 are P5 territory (alongside cohesion-judge primary integration). G6 is post-P5, alongside spirit-swap UX work. G7 is the empirical-validation gate before v1 ship.

**No phase blocks the existing QD-rebuild critical path.** Gear-as-substrate is additive to the rebuild trajectory, not a precondition.

---

## 12. Open questions for Matt

1. **Gear-archetype taxonomy v1 cut** — § 3 proposes 15 archetypes. Which stay, which go, which need different framing? Particularly: keep all four hand-weapon archetypes, or condense (greatsword + mace → "heavy-melee")?
2. **Substrate-gear acquisition mechanic in-season** — guaranteed-by-mid-season-progression vs RNG-weighted-likely vs boss-drop-guaranteed?
3. **"Partial identity" effectiveness** — 60-75% of full-substrate output when gear-substrate is missing? Or harsher? Or just narrative-flag-only?
4. **Multi-slot substrate vs weapon-only** — v1 keeps it weapon-only. Confirm? (Offhand-as-substrate is a real future design space; e.g., shield-vs-tome dual-classing.)
5. **Cross-spirit gear sharing** — v1 keeps substrate-gear per-spirit. Confirm? (Cross-spirit sharing is simpler UX but weakens identity-completion semantics.)
6. **Gear-archetype-vs-element conflict resolution** — when substrate-composer hits a vector like "fire + ranged + censer" (genre-incoherent), reject and recompose? Or accept and let cohesion-judge invent a recovery framing?
7. **v1 launch with all 15 archetypes, or staged rollout?** — Recommend all-15 with the 4-substrate cohesion-judge prompt baking in from the start; alternative is 5-archetype soft-launch with growth.

---

## 13. Cross-references

- `canonical/story/substrate-design-supplement-2026-05-21.md` — elemental substrate framing this doc extends
- `canonical/story/multi-dim-convergence-algorithm-2026-05-21.md` — v1.1 math note; gear-archetype noted as substrate (NOT convergence dimension)
- `canonical/story/hive-mind-protocol-qd-engine-rebuild-2026-05-21.md` v1.2 — protocol amendment needed to add gear-substrate work to P1/P5 scope
- `agentic_orchestration/legolas/research/substrate-as-cohesion-validation-probe-2026-05-21/` — empirical baseline for cohesion-judge substrate recognition
- `reincarnated-engine/src/reincarnated/generation/gear_generation.py` — gear-instance generation (preserved; constrained by archetype in extended pipeline)
- `reincarnated-engine/src/reincarnated/simulation/balance_loop.py:858` — `_gear_loadout_cycling_hook` reframing target
- `canonical/17-gear-and-spirit-guide-design.md` — predecessor design doc; gear-as-balance-and-affix framing (this doc supersedes the substrate framing while preserving the balance and Spirit Guide framings)
- `canonical/32-progression-design.md` — progression spec; substrate-gear unlock as progression milestone candidate
- Memory: `project_gear_and_spirit_guide.md`, `project_trait_architecture.md` (gear-affix rolls remain valid as gear-instance-tier mechanic)

---

## 14. Why this lands

The substrate-as-cohesion validation probe returned 4.35 mean coherence this evening. The probe specifically called out that cohesion-judge **recognized substrate identity confidently in 9/10 cases** with three substrate dimensions and only mechanical signature to work from.

**Adding gear-archetype as a fourth substrate is the natural next move** — it expands the judge's substrate-recognition surface with one of the genre's strongest identity-signals, gives the cohesion-judge a fourth anchor to disambiguate edge cases, and connects the substrate architecture to Reincarnated's spirit-swap meta-layer in a way that completes the design DNA.

It also activates an architectural stub Matt himself named weeks ago, recognizing the slot before the surrounding framework existed.

The blunderbuss must be viable in battle simulation. That is the discipline. Hold it, and gear-as-substrate becomes the layer that makes a Holy Pirate Sniper real.

---

**Signed:** gandalf (story-and-design steward)
**For:** Matt review and decisions-log commitment; canonical commit follows on Matt approval.
