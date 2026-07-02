# Six-Profile Set Architecture — 2026-06-16

> **STATUS:** CURRENT (load-bearing as of 2026-06-16) — see `canonical/00-ground-state.md` § 1. The shipped Set-Gear architecture for Reincarnated v1.1-current: six play-pattern **profiles** (substrate regions, not re-imposed classes), one flagship set per profile per season, 2pc-accelerate + 4pc-global-capstone, element-flavored at the StyleProfile layer. Resolves the measurement-contract § 6 park (6a-vs-6b) by separating the shipped form (this doc) from the measurement instrument (6b).

**Date:** 2026-06-16
**Author:** gandalf (story-and-design steward)
**Status:** v1 — design architecture. Authored from the Pattern-B equipment session with Matt 2026-06-16. Matt rulings folded in verbatim: **§ 6 = 6b-reference-at-T4-scope-magnitude** (measurement instrument); **all six profiles ship — proxy is NOT skipped** ("we need all 6 profiles. I will not skip proxy"); **v1 skipped, v1.1 = current.**
**Authority:** Matt 2026-06-16 Pattern-B equipment session — rulings above are direct. The 4pc-as-second-T4-capstone instinct (Matt) is validated by doc 46 Layer 3 (character/chain-wide scope reserved for T4). The six-profile count is Matt-locked; this doc makes the six substrate-honest.
**Companion docs:**
- `canonical/46-concentration-architecture-2026-05-27.md` — Layer 3 (§ 4; capabilities LOCAL, character/chain-wide reserved for T4), Layer 5.4 (§ 6.4; 4pc set REPLACES individual capability), **Layer 8 (§ 9; set keying to T4-strategy × element clusters — this doc AMENDS the ~12-20-set figure to six flagships)**, Discipline #36 (substrate-as-keying-source). D66 (one chain-T4 at a time).
- `canonical/story/representative-loadout-measurement-contract-2026-06-16.md` § 6 — the 6a-vs-6b park; RESOLVED here (6b = measurement instrument; this doc = shipped 6a-flavored form).
- `canonical/48-cycle-14-class-roster-2026-05-27.md` — VESTIGIAL (class concept architecturally RETIRED); the 10 archetype-shapes are substrate-cluster expressions, consumed here as profile *membership evidence*, not as classes.
- `canonical/story/weapon-as-identity-surface-recognition-2026-06-14.md` § 4 — three-layer identity model (weapon→physical/caster; skill-composition→summon runtime-label; coordinate→behavioral descriptor); the Proxy-Commander profile inherits the skill-composition-derived summon label.
- `canonical/story/telegraph-dodge-temporal-decoupling-2026-06-15.md` — the Berserker profile IS the glass-close-ST FLEX coordinate; viability lives in the dodge layer, not the autobattle.
- `matt_notes_handoff_docs/armor-weapon-pipeline-recommendation.md` — the asset pipeline; § 4.3 emission/glow masks carry the set-complete aura; § 5 StyleProfile schema carries the element-flavor.
- `~/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/` — the 2D spatial sim, the SOLE battle simulation (post 1D-deletion 2026-06-16); sets are validated here.

---

## 0. TL;DR

Reincarnated ships **six Set-Gear profiles**, not ~12–20 combinatorial sets and not per-class sets. Each profile is a **player-legible name for a region of the substrate space** (BC engagement profile × T4 Category-A valence) — emergent, not hand-imposed. One **iconic flagship set per profile per season** is the belovedness play: D3 sets are loved *because* there are few and each is a complete build identity; ~12–20 combinatorial sets optimize coverage, not belovedness.

Each set = **2pc minor bonus** (accelerates the kit's own chosen chain-T4) + **4pc global capstone** (a T4-SCOPE, profile-defining effect that COEXISTS with — does not compete with — the chain-T4). The 4-piece commitment is what earns the T4-scope, exactly as doc 46 Layer 3 reserves character/chain-wide scope for T4. The set-complete state lights the **glowing-aura apex** (emission-mask apex, element-tinted, human-authored per D7).

Sets are **mechanically profile-keyed (element-agnostic) and visually element-flavored** via the StyleProfile (asset pipeline § 5). A fire-Juggernaut and a water-Juggernaut wear the same *mechanical* set with different *visual* skins — D3's Tal-Rasha's-works-for-any-elemental-wizard pattern, generalized from class-lock to profile-lock.

**The six (v1.1-current, all shipping):**

| # | Profile | Substrate signature | Genre touchstone | Fantasy |
|---|---|---|---|---|
| 1 | **Juggernaut** | DEFENSIVE_CONVERSION · close · sustained · high-mitigation | D3 Immortal King / Akkhan | "I tank and grind them down" |
| 2 | **Berserker** | TRADE_OFF · close · burst · fragile-by-choice | PoE Berserker / D2 Frenzy | "All-in; mastery shows" (FLEX coordinate) |
| 3 | **Stormcaller** | RESOURCE_CONVERSION · ranged · area · element-conversion | **D3 Tal Rasha's** | "The elemental engine" |
| 4 | **Reaper** | RESOURCE_CONVERSION · mid · sustained · DoT/ailment | PoE ailment/DoT | "Attrition; they rot as they come" |
| 5 | **Controller** | DEFENSIVE_TRADEOFF · mid/kiting · CC/zone-denial | D3 Inna's / PoE trapper | "I own the battlefield" |
| 6 | **Proxy-Commander** | caster subset, proxy-DOMINANT output (hypothesis-test-flagged — § 2.6 / § 3.2) · proxy-T4 · skill-composition summon | D2 Necro army / D3 gargantuans | "My constructs are extensions of me" |

---

## 1. The principle — flagship profiles, not combinatorial coverage (amends doc 46 Layer 8)

### 1.1 The load-bearing recognition

Doc 46 Layer 8 (§ 9) keys sets to (Category A × Category B/C × primary element) — ~256 theoretical, ~12–20 practical sets per season. **That figure optimizes coverage. It does not optimize belovedness.** Nobody strives for "the RESOURCE_CONVERSION × ELEMENT_CONVERSION × wind set." Players strive for *Tal Rasha's*. The genre evidence is unambiguous:

- **Diablo 3:** ~4–6 sets per class, each a complete build identity (Tal Rasha's, Inna's, Immortal King, Marauder's). Few, named, complete, defining. The most-played, most-remembered endgame content.
- **Path of Exile:** thousands of uniques, but the *beloved* ones are a tiny iconic subset — Headhunter, Mjölner, Shavronne's. Volume ≠ belovedness.
- **Diablo 2:** the runewords and set items players still name a generation later are few (Enigma, Infinity, Tal Rasha's again).

**This doc amends doc 46 Layer 8: ship SIX flagship sets (one per profile) per season, each cross-class + cross-element shareable, in place of the ~12–20 combinatorial figure.** The substrate keying (Layer 8) is preserved as the *mechanism* by which a kit is matched to its profile-set; the *count* collapses to six iconic flagships. Layer 8's cross-class shareability discipline (§ 9.4) is inherited and strengthened: a set works for any kit whose substrate tuple falls in the profile region.

### 1.2 Why this does not re-impose the retired class layer

Doc 48 is explicit: the class concept is **VESTIGIAL — architecturally retired 2026-05-27.** Substrate tuples vote; kits emerge per-kit. Discipline #36 (substrate-as-keying-source) forbids keying design surfaces to hand-imposed identifiers. **A naïve "six core profiles" hand-authored as fixed buckets would quietly rebuild classes under a new name — the precise drift doc 48 exists to prevent.**

The fix is the discriminator between a class and a profile:

> **A class is who you ARE (an assigned identity). A profile is how you ENGAGE (an emergent region of substrate space). Profiles are play-PATTERNS, and play-patterns map to the BC engagement axes the substrate already votes on — range / tempo / geometry / defensive — crossed with the T4 Category-A valence. A kit *belongs to* a profile because its substrate tuple falls in that region, not because a designer assigned it.**

Doc 48 already certifies "8 of 8 BC engagement profile bins covered." The BC engagement profile IS the substrate-native profile layer. The six profiles below are player-legible *names* for six regions of that space — emergent, substrate-led, no class layer between substrate and kit. (§ 3 makes the emergence procedure explicit.)

---

## 2. The six profiles — substrate predicate, genre touchstone, membership evidence

Each profile is defined by its **dominant substrate signature** (the axis that most defines it) plus secondary signatures. The "membership evidence" column cites which of doc 48's 10 substrate-cluster archetype-shapes fall in the region — evidence that the profile is substrate-real, not invented.

### 2.1 Profile 1 — Juggernaut

- **Substrate signature:** DEFENSIVE_CONVERSION (Cat A — converts mitigation into sustained offense) · close range · sustained tempo · high-mitigation defensive profile.
- **Genre touchstone:** D3 Immortal King (barbarian), D3 Aegis of Valor / Akkhan (crusader). The "the more I tank, the harder I hit back" build.
- **Membership evidence (doc 48):** Skirmisher ("cleanest DEFENSIVE_CONVERSION substrate fit per doc 40 § 8.4"), Crusader (consecrated/mitigator), Hoplite (defensive-T4 variant).
- **Player consequence:** "I stand in it. The longer the fight, the stronger I get."

### 2.2 Profile 2 — Berserker (glass-cannon)

- **Substrate signature:** TRADE_OFF (Cat A — sacrifices defense for offense) · close range · burst tempo · fragile-by-choice (low defensive layer).
- **Genre touchstone:** PoE Berserker ascendancy, D2 Frenzy-barb. **This is the glass-close-ST FLEX coordinate** (telegraph-dodge doc): the fragile-high-damage build chosen *because mastery shows*; viability lives in the piloted **dodge layer**, not the autobattle (the 2D sim correctly walls it and flags it dodge-gated).
- **Membership evidence (doc 48):** Barbarian (Berserker-Rage), Duelist (aggressive Riposte), Assassin (Shadow-Strike burst).
- **Player consequence:** "I die in two hits and I don't care, because I delete the boss before it lands the second."
- **Composition note:** the Berserker set must NOT smuggle a survivability global into the 4pc (that re-creates the genre-wrong "buff the fragile coordinate" auto-amp the telegraph-dodge doc deleted). Its 4pc is an *offense* global; survivability is the player's dodge skill (§ 5.2).

### 2.3 Profile 3 — Stormcaller (elemental engine)

- **Substrate signature:** RESOURCE_CONVERSION (Cat A — spend resource → power) · ranged · area geometry (radius/cone) · Category C ELEMENT_CONVERSION / DUAL_ELEMENT_ADDITION.
- **Genre touchstone:** **D3 Tal Rasha's** (the canonical elemental-rotation reference), D3 Vyr's, PoE Elementalist. Spend-to-power, cycle-elements-for-stacking-payoff.
- **Membership evidence (doc 48):** Siege-Master (STR-AoE artillery — the physical area-engine), Crusader (Channel-Aura), Magus (channeling — single-target in v1 per doc 48's honored INT-AoE gap).
- **v1.1 substrate note:** the pure **INT-blaster** Stormcaller variant (canonical fireball/chain-lightning mage) rides the INT-AoE substrate enrichment doc 48 § 0 deferred (Q-S2-12). The profile SHIPS now via the STR-AoE (Siege-Master) and faith-aura (Crusader) area shapes; the INT-blaster variant fills in when its substrate lands. The profile is not gated on the gap — only one of its expressions is.
- **Player consequence:** "I spend everything to make the storm bigger; rotating my elements is the engine."

### 2.4 Profile 4 — Reaper (DoT / attrition)

- **Substrate signature:** RESOURCE_CONVERSION (Cat A) · mid/ranged · sustained/attrition tempo · Category B multiplicative on sustained-damage · DoT/ailment mechanic emphasis.
- **Genre touchstone:** PoE ailment/DoT archetype (ignite/bleed/poison stacking), Grim Dawn's strong DoT culture. The "they're already dead, they just don't know it" build.
- **Membership evidence (doc 48):** Assassin (Venom-Craft — DoT), Gunslinger (sustained fire), Wildhunter (Feral multi-hit → bleed stacking).
- **Thematic anchor:** the Reaper profile is where the per-element **secondary ailment signatures** concentrate (wind cut+bleed / earth thorny-root / water cold-burn / fire burn-DoT, per the ailment-damage-thematic design proposal). The set amplifies the rot.
- **Player consequence:** "I don't burst them. I poison the room and walk away."

### 2.5 Profile 5 — Controller (zone / CC)

- **Substrate signature:** DEFENSIVE_TRADEOFF (Cat A) or control-keyed · mid/ranged · kiting · CC / area-denial mechanic emphasis (slows/stuns/zones).
- **Genre touchstone:** D3 Inna's mystic-ally control monk, PoE trapper / curse builds. The "I shape where the fight happens" build.
- **Membership evidence (doc 48):** Crusader (Banner-Rally — zone buff/control), Hoplite (Phalanx-Reach zone-control), Magus (control utility).
- **Player consequence:** "Nothing reaches me on my terms; the battlefield is mine to shape."

### 2.6 Profile 6 — Proxy-Commander (multi-spawn) — FULL MEMBER, NOT DEFERRED

- **Membership signature (the load-bearing correction — Matt 2026-06-16):** unlike profiles 1–5, the Proxy-Commander is **NOT** read off a generation-time substrate predicate. It is a **subset of CASTER kits, flagged by the `proxy_primary` hypothesis test** — those whose proxies do ≥ ~0.5 of the work (`proxy_contribution_pct` measured in the 2D spatial sim). Summon skills compose into the caster rotation (`summon` is a recognized effect_category; `multi-spawn` is a substrate-voted *geometry*, **now LIVE**: proxy battle is wired into the 2D spatial sim and proxy is in the T4 capstones); the sim then measures which casters are proxy-DOMINANT. *Having a summon skill ≠ being a Proxy-Commander.* The summon identity itself is the **skill-composition-derived runtime label** (weapon-as-identity § 4 three-layer model, D2/D4/Last-Epoch genre-true). See § 3.2 for why this profile is sim-flagged, not predicate-determined. (proxy-keyed T4 carries forward unchanged.)
- **Genre touchstone:** D2 Necromancer skeleton army, D3 Helltooth gargantuans + Inna's mystic allies, PoE summoner/totem, Last Epoch minion builds.
- **Membership evidence (doc 48 + proxy-add spec):** there is no pre-built proxy-primary archetype-shape to point at — membership is established **empirically** by the proxy-add work (proxy skills + gear) plus the hypothesis test. The canonical illustration of `has-a-summon-skill ≠ is-proxy-dominant` is **Beast Taming** (Matt 2026-06-16): ONE summon skill that populates *physical-ranged hunter* kits — the hunter captures an enemy beast-type combatant and uses it as a proxy — but it *supplements* the bow rather than replacing it, so the sim is *expected* to flag it **sub-threshold**. It carries a proxy skill and is NOT a Proxy-Commander. The proxy-add spec § 4.5 authors Beast Taming; the caster-side profile is completed by the proxy-add work Matt directed 2026-06-16.
- **Matt ruling (verbatim intent):** "we just wired proxy battle into the 2D spatial sim and we just added proxy to T4 capstones … I will not skip proxy." Doc 48's "multi-spawn DEFERRED to v1.1" is a v1-framing artifact, **superseded** under v1.1-current. Proxy is first-class.
- **Scarcity discipline (composition with `reap-die-rise-story/story-expansion.md` §12 companion-vs-proxies separation; was the 2026-06-13 companion doc corollary 1, folded 2026-07-01):** the Proxy-Commander's army is **generic constructs**, NEVER past selves or grimoire-listing pages. Proxies may be *flavored* as form-echoes but must never be literal listing entries — the singular companion's reverence must not be diluted by disposable swarms. The Proxy-Commander set amplifies the constructs; it does not summon past selves.
- **Player consequence:** "I don't fight directly. My constructs do — and the better I command, the more they become extensions of me."

---

## 3. Profile emergence — substrate-led, not hand-imposed (the procedure)

The six profiles are **not assigned by a designer to kits.** They are computed:

1. **A kit's substrate tuple** (BC engagement profile + T4 Category-A strategy + Category-B/C + geometry bin) is already produced by generation.
2. **Each profile is a substrate PREDICATE** over that tuple (§ 2's "substrate signature" rows are the predicates). The predicates partition the relevant region of substrate space; a kit's tuple falls in exactly one dominant profile (with a secondary lean where tuples straddle — see § 3.1). **(Exception: the Proxy-Commander, profile 6, is NOT predicate-determined — it is sim-flagged on measured proxy-contribution; see § 3.2.)**
3. **The match is the keying.** Layer 8's set-keying mechanism (preserved) reads the kit's tuple and matches it to the profile-set whose predicate it satisfies. No class layer, no smart-loot filter, no hand-assignment.

This is the substrate-honest version of "six core profiles": the profiles are player-legible *labels* for substrate-defined regions, and the substrate votes which region a kit lands in. Discipline #36 holds (sets key to substrate dimensions). The no-class recommitment holds (no identity layer between substrate and kit). **Note the asymmetry:** five of the six emerge from a generation-time predicate; the Proxy-Commander (§ 3.2) is **sim-flagged** on measured contribution rather than predicate-matched — because proxy-dominance is emergent and cannot be read off the static tuple.

### 3.1 Straddle handling — dominant + lean, never forced

A kit whose tuple straddles two regions (e.g., DEFENSIVE_CONVERSION + burst tempo straddles Juggernaut/Berserker) takes the profile its **dominant** axis selects, and may *benefit partially* from the adjacent profile's set (2pc only — the entry bonus) without completing it. This mirrors D3's "you can run a 2pc of one set + a 6pc of another" flexibility and PoE's hybrid builds. **We do not force a kit into a profile its substrate doesn't support** — that would be the categorical pre-imposition the substrate-led discipline retired. The semantic-layer rep-audit discipline (OP § 4.4) applies: audit the profile assignment at the rep level, not just the geometry-purity score.

### 3.2 Proxy-Commander is sim-FLAGGED, not generation-predicate-determined (corrected per Matt 2026-06-16)

Profiles 1–5 emerge from a generation-time substrate predicate over the kit tuple (§ 3, step 2). The Proxy-Commander does not — and the earlier framing that treated "multi-spawn geometry" as its tuple-predicate was a drift Matt corrected. The honest mechanism:

1. **Add proxy/summon skills to the caster rotation** (generation; ships now — the "I will not skip proxy" deliverable). One summon skill, **Beast Taming**, also populates the physical-ranged hunter rotation (proxy-add spec § 4.5).
2. **The `proxy_primary` hypothesis test** — run in the 2D spatial sim on a proxy CONTRIBUTION measure — **flags which caster kits are proxy-DOMINANT** (proxies do ≥ ~0.5 of the work).
3. **The flagged kits ARE the Proxy-Commander members** — they get the #6 set + the proxy-primary T4 capstone skills.

**Proxy-primary kits are a subset of CASTER kits, not a separated tuple.** You cannot read proxy-dominance off the static tuple — *having a summon skill ≠ being proxy-dominant* (a caster with one minor summon among many is not; a Beast-Taming hunter supplementing its bow is not). Only the sim, measuring where the kit's output actually comes from, can flag it. **The test is the assignment engine, not an obstacle the profile "ships around."**

**Why this asymmetry is correct, not a special-case hack.** Proxy-dominance is *emergent* — it lives in measured behavior, not in the generation-time coordinate. This is exactly the regime the golden-oracle architecture covers (the spatial sim is the behavioral-identity authority) and the weapon-as-identity § 4 model already locks (summon = a skill-composition-derived RUNTIME label, not a generation-time class). Reading the profile off a tuple-predicate would have re-imposed the very generation-time class the canon retired — so sim-flagging *is* the substrate-led move here, with the *behavioral* substrate (the sim) casting the vote instead of the *generative* substrate (the tuple). Whether `proxy_primary` is implemented as a 4th `Architecture` enum value or as a runtime flag layered on the kit's caster architecture is rocket's call (proxy-add spec § 8); membership resolves either way.

---

## 4. Set structure — 2pc accelerate + 4pc global capstone

Doc 46 Layer 5.4 (§ 6.4) already locks: the 4 set slots carry **no individual capability/triggered_passive** — those are REPLACED by the 2pc + 4pc set bonuses (the D3 "set replaces individual legendary powers" lineage). This doc fills in the *content shape* doc 40 D38 deferred.

### 4.1 The 2pc minor bonus — own-T4-accelerate

- **Effect class:** amplifies the **kit's own chosen chain-T4** (a clean, always-on accelerator). Of Matt's three sub-options, *own-T4-accelerate* lands here as the entry bonus — it deepens the build the player already chose.
- **Why here, not as the capstone:** alone, "do your one thing harder" is the D3 set criticism (the "10000% more damage to your one skill" pattern). Correct as the *entry* nudge; wrong as the *capstone*.
- **Scope:** chain-local (it touches the chosen chain-T4). Bounded by Layer 1 stat-range caps where it touches bounded stats.

### 4.2 The 4pc global capstone — profile-defining, T4-scope, coexists with the chain-T4

- **Effect class:** a fixed, **profile-defining global** tied to the *set's* play-pattern — the Tal-Rasha's model ("for everyone who wears it"). Of Matt's three sub-options, *global-per-profile* is the capstone. **Reject parallel-branch-augment** as the 4pc: a second *active* T4-scope effect parallel to the chain-T4 is the capability-soup risk Layer 3 closed and it muddies D66 (one chain-T4 at a time).
- **The distinction that protects the architecture:**

> **The 4pc is a T4-SCOPE *gear capstone* that COEXISTS with — does not compete with — the kit's chain-T4.** Matt's "second T4 capstone" instinct is right in *spirit* (a second T4-magnitude payoff) but it is a different *kind*: gear-profile-scope, not a second chain-T4. D66 governs chain-T4s (one active, switching = respec); the set capstone is a *separate scope* the way a D3 set bonus coexists with the active skill. The 4-piece commitment is what *earns* the T4-scope — exactly as doc 46 Layer 3 reserves character/chain-wide scope for the T4 tier of *earning*.

- **Scope:** character-wide or chain-wide (T4-scope, per Layer 3's reservation). This is the ONLY gear surface licensed to carry T4-scope, and only at the 4-piece commitment.
- **Magnitude:** a **T4-scope magnitude** — calibrated by gamora at the same anchor the measurement contract's 6b reference set uses (§ 9). The shapes in § 5 are design intent; the numbers are gamora's calibration at the T4-scope anchor.

---

## 5. The 4pc capstone content per profile (the shape; magnitude = gamora calibration)

Each 4pc is a global, profile-defining, T4-scope effect. These are SHAPES (design intent), not magnitudes.

| Profile | 4pc global capstone (shape) | 2pc accelerate (shape) |
|---|---|---|
| **1 Juggernaut** | A share of damage *mitigated* converts into bonus weapon damage on subsequent strikes — the more you tank, the harder you hit back (DEFENSIVE_CONVERSION made global). | Amplify the chosen DEFENSIVE_CONVERSION chain-T4. |
| **2 Berserker** | While below a defensive threshold (no shield / low effective mitigation), a large global *offense* multiplier (the glass-cannon payoff). **Offense only — no survivability global** (§ 2.2). | Amplify the chosen TRADE_OFF chain-T4. |
| **3 Stormcaller** | Cycling/spending resource across distinct element applications grants a *stacking global elemental multiplier* (the Tal-Rasha's rotation engine). | Amplify the chosen RESOURCE_CONVERSION / element chain-T4. |
| **4 Reaper** | Your damage-over-time / ailment effects gain magnitude **and** a spreading/proliferation global (attrition becomes contagious). | Amplify the chosen DoT/ailment chain-T4. |
| **5 Controller** | Your CC effects gain duration/area **and** a global "enemies inside your control zone take amplified damage" (zone-denial becomes a damage surface). | Amplify the chosen control / DEFENSIVE_TRADEOFF chain-T4. |
| **6 Proxy-Commander** | Your proxies gain count/power/duration **and** a global "your proxies inherit a share of your offensive profile" (constructs become extensions of you). Constructs are generic, NOT Hall forms (§ 2.6). | Amplify the chosen proxy chain-T4. |

**Authoring note (D7 AI-tell line):** these capstones are *human-authored design shapes*. Phase-5 LLM cohesion-judge narration (doc 46 Layer 6) may *name* and *flavor* a set ("Phoenix-Cycle Set") but does NOT generate the mechanical capstone. The set's mechanical content is curated; the LLM fills the narrow naming/flavor blank only.

---

## 6. Element-flavoring — mechanically profile-keyed, visually element-flavored

**Mechanically, the six sets are element-AGNOSTIC** (the Juggernaut 4pc is the same global for a fire-Juggernaut and a water-Juggernaut). This is what makes six sets enough for 400 kits + balance-tractable + cross-element shareable.

**Visually, each set is element-FLAVORED via the StyleProfile** (asset pipeline § 5): palette/finish/emission/overlay/theme_seed tint to the wearer's primary element. A fire-Juggernaut's set reads ember-and-iron; a water-Juggernaut's reads deep-blue-and-frost. Same mechanical set, different visual skin.

- **Genre precedent:** D3's Tal Rasha's works for any elemental wizard; the meteor visual adapts to your element. We generalize the pattern from *class-lock* to *profile-lock*, with element living in the visual layer.
- **Asset-pipeline tie (Q3):** the element-flavor is exactly the `palette` / `finish_per_region` / `theme_seed` fields of the StyleProfile (§ 5 of the pipeline doc). The set's six *mechanical* identities × the element *visual* flavor compose at the StyleProfile layer — no mechanical combinatorial explosion, full visual variety.
- **Variety for 400 kits:** a kit knows its profile (§ 3), so it knows its flagship set; per-kit visual differentiation (the 400 distinct looks per the asset pipeline) + per-element set tint supplies the variety. Six mechanical sets is the belovedness ceiling, not the variety floor.

---

## 7. The glowing-aura apex — set-complete visual reward

- **What:** the **set-complete state** (4-piece active) lights a glowing aura — the genre-canonical "you made it" signal (D3 set-completion glow; PoE Headhunter-as-social-signal).
- **Where it lives:** the asset pipeline's **emission/glow masks** (§ 4.3) — author the set-complete aura as the **`emission_mask` / `emission_intensity` apex** in the StyleProfile schema (§ 5), reserved exclusively for the 4-piece-complete state. Sub-complete (2pc) carries no apex aura.
- **Element-tinted:** the aura's `emission_color` flavors to the wearer's primary element (§ 6) — a fire-Juggernaut glows ember; a water-Juggernaut glows deep-blue.
- **D7 held:** the aura is a human-authored, curated visual reward, not a generated one. It is the *visual* capstone that pairs with the *mechanical* 4pc capstone — completion you can see.
- **Player consequence:** "When the aura lights, everyone in the Hall knows what I built and what it cost."

---

## 8. Cross-class + cross-element shareability (Layer 8 inheritance, strengthened)

Per Layer 8 § 9.4: a set works for ANY kit whose substrate tuple falls in the profile region — strengthened here by element-agnosticism (§ 6). So:

- A wind-Berserker and a fire-Berserker share the *Berserker set* mechanically (different visual tints).
- A Skirmisher-shaped kit and a Crusader-shaped kit that both land in the Juggernaut region share the *Juggernaut set*.
- The set's content amplifies the *profile play-pattern*, not the archetype-shape — so it is maximally shareable across the 400 kits that land in its region.

This retires (per Layer 8 § 9.7) any per-kit bespoke set pattern. Drops are class-agnostic (Layer 9); a kit collects toward the flagship set of its profile, or trades/alts the off-profile pieces.

---

## 9. Composition with measurement-contract § 6 — the park is RESOLVED

The measurement contract § 6 parked one question: is the measured set 6a (generated per-kit) or 6b (fixed reference)? **Matt ruled 6b-reference-at-T4-scope-magnitude.** This doc completes the composition by separating the two cleanly:

- **Measurement instrument (6b — the gauntlet's set):** a fixed reference-set magnitude profile, its 4pc calibrated to a **T4-scope magnitude** (§ 4.2). It unblocks the keystone *now* without waiting for the six-profile set system to be built. gamora consumes it at the measured-loadout construction point. It is a measurement instrument, not a shipped item.
- **Shipped form (this doc — 6a-flavored):** the six profile-keyed flagship sets are the shipped sets. They are "6a-flavored" because they are kit-aligned *via profile-keying* (a kit's profile selects its set), and they swap in for the 6b reference set when the `set_generator` six-profile pass lands.
- **The magnitudes coincide by construction:** because the 6b reference 4pc is calibrated to the *same* T4-scope anchor the shipped 4pc capstones target (§ 5), the measurement instrument *predicts* the shipped power. The band the gauntlet judges against does not move when the real sets swap in.

This honors recognition→validate→commit: commit the measurement-unblocking instrument (6b) now; commit the shipped six-profile sets when `set_generator` lands; the T4-scope magnitude anchor is the invariant that keeps them coherent.

---

## 10. Composition with the 1D→2D battle-sim deletion (2026-06-16)

The 1D battle sim + b6 archetype processes are **deleted** (Matt-ruled 2026-06-16; the 2D spatial sim is the sole battle simulation). Consequence for sets:

- **Sets are validated in the 2D spatial sim**, not the deleted 1D sim. The 4pc global capstones (especially Stormcaller's area-rotation, Controller's zone-amplification, and Proxy-Commander's construct-inheritance) only mean anything in a *spatial* sim — the 1D duel could not have measured them. The deletion is therefore *enabling* for this architecture, not merely a cleanup.
- **The Proxy-Commander set is only honestly measurable in the spatial sim** (proxy population, spatial coverage, construct positioning — the D4 Axis-2A proxy-population work). This is further evidence the spatial sim is the correct sole authority and the 1D sim was the wrong instrument for the kits this architecture ships.
- **The measurement-contract keystone redirects** (§ 9): real loadouts (node-investment + real gear + the 6b reference set) now feed the 2D spatial sim. The set system is validated there.

---

## 11. Acceptance hooks per seam

### 11.1 rocket (generation seam)
- Author `set_generator.py` as a **six-profile pass** (amending doc 46 Layer 8's ~12–20 figure): emit six flagship sets per season, each keyed to a profile predicate (§ 2 / § 3), each with the 2pc-accelerate + 4pc-global-capstone content shapes (§ 5), element-flavored at the StyleProfile layer (§ 6).
- Proxy gear modifiers + proxy skills (the paired proxy-add spec) supply the Proxy-Commander profile's kit-side surface.
- The 4pc capstone is the ONLY gear surface that carries T4-scope (Layer 3); enforce that no individual legendary capability claims character/chain-wide scope.

### 11.2 gamora (simulation seam)
- Calibrate the 4pc capstone **magnitude** at the T4-scope anchor (§ 4.2 / § 9); the 6b reference set is the measurement instrument carrying this magnitude.
- Validate the six sets in the **2D spatial sim** (§ 10); the Stormcaller / Controller / Proxy-Commander capstones require spatial measurement.
- Methodology consultation per Discipline #18 if the capstone magnitude calibration is a named math hotspot.

### 11.3 drax (player-surface seam)
- Render the **glowing-aura apex** (§ 7) at set-complete state via the StyleProfile `emission_mask` / `emission_intensity` / `emission_color` (element-tinted).
- Surface profile identity + set progress (2pc / 4pc) in the loadout app; the set IS the profile identity.

### 11.4 star-lord (telemetry + LLM seam)
- Phase-5 cohesion-judge LLM *names/flavors* the six sets (D7: narrow blank only; mechanical capstone is human-authored, § 5).
- StyleProfile emission fields carry the set-complete aura state through the asset pipeline.

### 11.5 elrond (substrate seam)
- The profile predicates (§ 2 / § 3) are substrate-curatable; elrond supplies the region definitions over the BC-engagement × T4-Category-A space.

---

## 12. Predictions registered (for empirical validation)

Per recognition→validate→commit, predictions the spatial-sim validation will confirm or falsify:

1. **The six profile predicates partition the 400-kit substrate space with low straddle** — most kits land in exactly one dominant profile; straddle (§ 3.1) is the minority and resolves to dominant-axis + 2pc-lean cleanly. (Empirical gate: run the predicate over a generated season's kit corpus and read the assignment distribution.)
2. **The 4pc global capstones measure as T4-magnitude payoffs in the 2D spatial sim** at the calibrated anchor — i.e., the set capstone shifts the kit's spatial KPM by a margin comparable to a chain-T4. (Empirical gate: gamora's spatial-sim measurement at the calibrated 4pc magnitude.)
3. **Six flagship sets supply sufficient endgame strive-targets** — playtest engagement data shows players orienting toward "their" profile set as a goal. (Empirical gate: playtest, post-pipeline-completion.)
4. **The 6b measurement instrument predicts the shipped six-profile set power** — when the real sets swap for the reference set, the bounded-viability band does not move beyond the calibration tolerance. (Empirical gate: re-measure at swap-in.)

**Empirical gate (NOT time-passage):** predictions 1–2 resolve when the `set_generator` six-profile pass + gamora spatial calibration run; prediction 3 at playtest; prediction 4 at real-set swap-in.

---

## 13. Cross-references

- `canonical/46-concentration-architecture-2026-05-27.md` — Layer 3 / Layer 5.4 / **Layer 8 (§ 9; AMENDED here: ~12–20 → six flagships)** / Discipline #36 / D66.
- `canonical/story/representative-loadout-measurement-contract-2026-06-16.md` § 6 — RESOLVED here (6b instrument / six-profile shipped form).
- `canonical/48-cycle-14-class-roster-2026-05-27.md` — membership evidence (the 10 archetype-shapes map onto the six profiles); class concept retired.
- `canonical/story/weapon-as-identity-surface-recognition-2026-06-14.md` § 4 — Proxy-Commander inherits the skill-composition summon label.
- `canonical/story/telegraph-dodge-temporal-decoupling-2026-06-15.md` — Berserker = glass-close-ST FLEX coordinate; dodge-layer viability.
- `canonical/reap-die-rise-story/story-expansion.md` §12 — proxies are generic constructs, NEVER past selves (was the 2026-06-13 companion doc corollary 1; folded 2026-07-01).
- `matt_notes_handoff_docs/armor-weapon-pipeline-recommendation.md` § 4.3 / § 5 — emission aura + element-flavor StyleProfile.
- `canonical/00-ground-state.md` § 1 — this doc registers as a new CURRENT entry.

**Decisions-log:** the architectural commitments here (six-profile set keying; 4pc-as-gear-capstone-T4-scope; § 6 = 6b ruling) warrant a decisions-log entry — routed to jack-ryan (gandalf recommends; Matt approves; knight-rider drafts; jack-ryan reviews).

---

## 14. Sign-off

**Author:** gandalf (story-and-design steward)
**Status:** CURRENT — the shipped Set-Gear architecture for v1.1-current. Six play-pattern profiles as substrate regions (not re-imposed classes); one flagship set per profile per season; 2pc-accelerate + 4pc-global-capstone (T4-scope, coexists with chain-T4); element-flavored at the StyleProfile layer; glowing-aura apex at set-complete; Proxy-Commander as full member #6. Amends doc 46 Layer 8 (~12–20 → six flagships). Resolves measurement-contract § 6 (6b instrument / six-profile shipped form). Validated in the 2D spatial sim (the sole battle simulation post 1D-deletion).
**Composition:** with doc 46 (concentration architecture — Layer 3 / 5.4 / 8 / Discipline #36 / D66), the measurement contract (§ 6 resolved), doc 48 (no-class; membership evidence), the weapon-as-identity recognition (summon label), the telegraph-dodge doc (Berserker FLEX coordinate), the companion commitment (proxy scarcity discipline), and the asset pipeline (emission aura + element-flavor).
**For:** the canonical definition of Reincarnated's Set Gear — six iconic, beloved, strived-for flagship sets, each a complete play-pattern identity, substrate-keyed and cross-class + cross-element shareable, capped by a T4-scope gear capstone and a glowing-aura apex. The proxy profile ships first-class per Matt's ruling; its kit-side surface is the paired proxy-add design spec.

**Signed:** gandalf (story-and-design steward), 2026-06-16.
