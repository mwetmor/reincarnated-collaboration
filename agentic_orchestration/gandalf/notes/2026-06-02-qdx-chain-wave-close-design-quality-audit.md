# QDX chain wave-close design-quality audit (LOCK H; PASS-with-design-concerns)

**STATUS:** CURRENT (LOCK H note-only artifact; design-quality lens at chain close)
**Date:** 2026-06-02
**Author:** gandalf (story-and-design steward)
**Authority:** LOCK H standard design-quality audit at workstream close (note-only; not a gate)
**Companion docs:**
- `agentic_orchestration/cycle-17-qdx-qd-engine-re-fire/wave-state.md` (chain state; all 7 workstreams COMPLETE)
- `agentic_orchestration/cycle-17-qdx-qd-engine-re-fire/qdx-5-generator-path-strategic-decision-2026-06-02.md` (Option B + B4.5 ratification)
- `agentic_orchestration/qa/findings/2026-06-02-qdx-phase-3-qdx-5-gate-2.md` (QDX-6 Gate-2 substantive findings)
- `canonical/story/2026-06-02-season-archive-realm-expansion-pivot.md` (architectural commitment preserved + reinforced)
- `canonical/story/2026-06-02-eaa-chain-wave-close-record.md` (preceding chain — QDX iterates from there)

---

## TL;DR

**Overall verdict: PASS-with-design-concerns.**

The QDX chain delivered Matt's verbalized chain-close goal — Cycle 14 wave-5-equivalent kit-richness composed with WS1A.4-lite per-skill flavor naming, at $1.14 / 10.6 min for 37 kits with the exact Matt-target distribution (43.2% physical / 56.8% caster). The architecture works. Caster identities are genuinely on-genre. The pipeline composition (Phase 1→2→4→5(a/b/c)→Wave A→Wave B→7→8) executes cleanly and the per-skill flavor LLM judgment composes naturally with the Wave A/B identity LLM.

**The design concerns are bounded and structural, not architectural:**

1. **24.3% Wave B prompt failure rate on physical/earth/wind/holy** producing within-primary fallback duplicates ("Earthen Earth Fighter Bearer" 3/3; "Scattered Wind Fighter Bearer" 2/3) — these are player-facing identity collisions and the fallback composition rule produces visible redundancy (the word "Earth" appearing twice in the same identity)
2. **Faction-token semantic clustering** ("Scattered", "Meridian", "Reach" appear 7+ times across non-physical kits) — could be intentional faction-coherence-via-naming or incidental LLM-template-pickup; the design call hasn't been made
3. **Physical BC axis homogeneity** — all 16 physical kits share identical BC configuration; differentiation lives at the naming layer alone; substrate-bound

**Strategic re-engagement ranking (gandalf design-steward lens):**

1. **(A) Elrond substrate-enrichment workstream** — the highest-leverage next-cycle investment per jack-ryan's strategic signal AND per the design-steward lens. The QDX-5 quality ceiling is substrate-bound; every other improvement (prompt iteration, distribution refinement, Wave B richness) hits diminishing returns until the substrate gives the engine more to compose with. This is BOTH a structural fix and an architectural alignment fix (returns canonical 39 substrate-led discipline to its purest form).
2. **(B) MM-P1 chernoff celestial body four-stage flow design session** — now empirically grounded. The 37 kits constitute the Stage A browsable substrate for the first time. The design work is no longer hypothetical; it can be designed against actual identity strings, faction names, and per-skill flavor metadata. Composes natively with kit space architecture.
3. **(C) Wave B prompt improvement workstream** (within future cycle; LOCK L iteration pattern) — addresses the visible fallback-redundancy pattern at a prompt-design layer without waiting for substrate enrichment. Cheaper and more bounded than (A) but addresses surface symptom rather than structural root.

(A) and (B) compose naturally — substrate enrichment fires in parallel with MM-P1 design work; MM-P1 can reference current kit-space empirically while the substrate workstream lands richer downstream kits.

---

## 1. Design coherence assessment

### Does the QDX chain advance the project's design goals?

**YES — substantively on several axes, with one structural caveat.**

#### Realm Expansion architectural commitment (preserved + reinforced)

The QDX-5 fire is exactly the kit-space-expansion event the Season-Archive Realm-Expansion canonical record (2026-06-02) describes: parameter scope expansion produces new kits into the continuous kit space (not per-season buckets), chronicled by `kse_20260602_008`. The kit_space at `data/kit_space/kits/` now holds 75 kits across 8 expansion events. The architecture is operating as canonically committed.

This is the **second empirical expansion event** (first was EAA-5 v2 at 25 kits). The compounding kit space is empirical evidence that the architectural commitment is fielded, not just declared. The Realm Expansion mechanism has its substrate.

#### Substrate-led discipline (refined)

Matt + I ratified the **substrate-led WITHIN element axis** interpretation 2026-06-02 morning. The QDX-5 fire empirically exercises that interpretation:
- Element axis = weighted round-robin (Option B4.5: 16 physical + 3 × 7 casters = 37)
- Substrate determines fill within each axis (BC axes, archetype tags, energy types, attribute mappings)

The interpretation holds operationally. The Discipline #41 refinement is canonically defensible — substrate-led at the dimension where substrate ACTUALLY has coverage (the BC-axis / archetype dimension within element); not at the dimension where substrate has known gaps (the element-axis distribution).

This is a genuine canonical clarification, not a discipline weakening. It says: "substrate-led means substrate constrains the dimensions where substrate has signal; it does NOT mean substrate is allowed to over-concentrate where coverage gaps exist." That's a stronger discipline statement than the original.

#### Canonical-7+1 element catalog (operationally honored)

All 8 canonical elements present in QDX-5 output: physical + fire + water + earth + wind + lightning + holy + shadow. Weighted distribution preserves physical-as-taxonomy-sibling per Architecture A. The catalog is in active use, not deprecating into theory.

#### Q18 vocabulary (consumed at per-skill grain)

Sample-inspection confirms Q18 allow-list words are being selected per-skill: `void`, `shade`, `necrotic`, `soul` (shadow); `scorch`, `blaze`, `inferno`, `flare` (fire); `radiant` (holy); `torrent`, `tidal` (water). Per-skill flavor_decision metadata is populated. The Q18 lock and the WS1A.4-lite consumption path are operationally married.

#### Earth meta-layer (NOT addressed by QDX scope — and that's correct)

QDX scope was engine-side kit-space generation. The Earth meta-layer / ascension architecture / spirit-swap-as-class-differentiation framing is preserved but not touched by this chain. That's the correct scope discipline — Earth-layer work composes at MM-P1 time, not at engine-generation time.

#### Emergent identity (substantively advanced; quality-gradient)

Wave B emergent identities for the rich cases are genuinely on-genre:
- "Penumbra Caster of Dusk Meridian" — Diablo-shadow-mage idiom; "penumbra" is precise vocabulary
- "Tidecaller of the Scattered Reach" — Last-Epoch/PoE caster-archetype-with-location-modifier convention
- "Cannonade Cleric of Scattered Light" — interesting Diablo-3-crusader vibe (artillery-cleric is an under-explored archetype space)
- "Stormcaller of the Scattered Meridian" — clean Diablo-2-sorceress / D3-wizard lightning idiom
- "Crusher Who Holds the Ground" — physical-warrior-with-philosophical-stance vocabulary; reads as Grim Dawn / D2-barbarian flavor
- "Slagfist of the Breach" — industrial-physical idiom; reminiscent of Diablo 3 monk-with-tinker-overlay
- "Crushweight of the Mudline" — unusual; reads as low-fantasy / earth-tradition; effective

These are emergent in the genuine sense — they're not template substitutions; they read as the kind of class-archetype-name a thoughtful designer at GGG or Crate Entertainment would author. The architectural intent (Pareto pool + cohesion clustering + Wave A/B identity LLM produces emergent identity) is operating.

#### Spirit-swap differentiation (composes naturally; not directly stressed)

QDX scope didn't directly test spirit-swap mechanics, but the 37-kit diverse-identity space is the necessary precondition for spirit-swap-as-class-differentiation to land — the player can only meaningfully spirit-swap if there are visibly-different kits to swap into. The QDX-5 output expands the swappable space.

### The caveat

**Physical kit identity quality is a step below caster kit identity quality.** This is structurally driven (BC axis homogeneity → LLM has less differentiation signal → fallback rate higher → fallback composition rule produces redundant names). It's not architectural failure — the pipeline fires correctly. But the design intent (every kit feels distinct) is partially compromised on the physical side until substrate enrichment lands.

---

## 2. Thematic alignment

### Wave B emergent identity coherence with project canon

**On-genre for the rich identities; falls flat for fallback identities.**

The rich emergent identities map cleanly onto recognizable ARPG/JRPG archetype space:

| Identity | Genre touchstone | Coherence |
|---|---|---|
| "Penumbra Caster of Dusk Meridian" | D2 Necromancer / PoE Witch (shadow + dusk + caster) | High; "Penumbra" + "Dusk" creates atmospheric coherence |
| "Tidecaller of the Scattered Reach" | LE Druid (Tidecaller skill family) / FF Summoner | High; clean class-archetype-with-location convention |
| "Cannonade Cleric of Scattered Light" | D3 Crusader (cannon-cleric subspace) | Strong; gentle subversion of standard cleric (artillery overlay) |
| "Stormcaller of the Scattered Meridian" | D3 Wizard / WoW Shaman elemental-lightning | High; standard naming convention done well |
| "Galewright of the Scattered Pale" | Slime-isekai air-mage / KonoSuba wind-vanir | Medium-high; "Galewright" is novel; "Pale" is atmospheric |
| "Radiant Arbiter of the Open Field" | D2 Paladin / D3 Crusader judge variant | High; "Arbiter" is Yu-Gi-Oh / TCG-precise religious-judge vocabulary |
| "Ember Caster of Scorched Meridian" | D2 Sorceress fire-tree / Last Epoch Fire Sorcerer | High; clean fire-caster idiom |
| "Crushweight of the Mudline" | Grim Dawn earth-physical hybrid | Medium; unusual; could be archetype-defining or could read as awkward |
| "Crusher Who Holds the Ground" | D2/D3 Barbarian-with-stance discipline | High; the "Holds the Ground" suffix is character-fantasy precise |
| "Slagfist of the Breach" | D3 Monk-industrial / Torchlight Engineer | High; "Slagfist" is original-feeling; industrial-physical idiom |

These read as the kind of class-names a senior ARPG designer would propose. They have the right grammar (noun-of-place / role-with-disposition) and the right vocabulary register (Diablo / PoE / LE-adjacent without being derivative).

### The fallback identities are not thematically coherent

| Fallback identity | Issue |
|---|---|
| "Earthen Earth Fighter Bearer" (3 kits) | Element word appears twice; "Fighter Bearer" reads as machine-generated; no character-fantasy |
| "Scattered Wind Fighter Bearer" (2 kits) | Same structural issue; "Scattered" is too vague an adjective for a class name |
| "Scattered Holy Fighter Bearer" | Same |
| "Iron Physical Fighter Bearer" (3 kits) | Same structural issue — "physical" is a system-vocabulary word, not a character-fantasy word |

These are not just low-quality — they violate the basic class-name convention (a class name should evoke a character, not describe a system category). The word "physical" appearing in a class name is a tell — no Diablo / PoE / LE class is named for its damage type because damage type is a player-system concept, not a character-fantasy concept.

**Design consequence:** if a player sees "Earthen Earth Fighter Bearer" in the chernoff celestial body Stage A browse view, the immersion break is significant. This is the kind of identity that signals "this game's content is AI-generated and didn't get caught" rather than "this is a richly-imagined class."

### Wave A faction names

Three factions emerged:
- **Iron Ground Crushers** — strong; material + terrain + role convention; reads like a Diablo 2 act-NPC faction or a PoE league mob group
- **Earthen Siege Wardens** — strong; "Siege Wardens" carries job-specificity; "Earthen" is appropriate element-coupling
- **Scattered Meridian Cannons** — weak; "Scattered" as adjective is the same problem as in the fallback identities; "Meridian Cannons" is interesting but the "Scattered" prefix dilutes it

The first two factions read as authentic ARPG faction names. The third surfaces the "Scattered" semantic-token issue — when a single weak token gets used both in faction-naming and gets picked up in kit-naming, it spreads through the visible surface.

### Per-skill WS1A.4-lite flavor decisions

Sample inspection shows the per-skill decisions are operating thoughtfully:
- **kit_fire_000006 Ember chain:** "Smoldering Ember → Ember Ward → Ember Burst → Ember Shot → Ember Flare → Ember Surge → Ember Storm → Ember Blaze → Ember Dash → Ember Aegis → Ember Inferno" — the chain progression is on-genre (D2-sorceress fire tree convention; tier escalation visible through vocabulary intensification: smoldering → ward → burst → storm → blaze → aegis → inferno). This is GOOD design work.
- **kit_holy_000005:** "Sacred Verdict / Divine Sentence (radiant-flavored) / Holy Decree / Celestial Judgment / Sacred Ward / Divine Sanction" — the legal-religious vocabulary register is coherent across the kit; the per-skill flavor word ("radiant" on Divine Sentence) sits naturally
- **kit_shadow_000007:** "Shadow Bolt / Shadow Burst / Shadow Eruption / Shadow Rot / Shadow Veil" — clean canonical-naming; physical opt-out style architectural decision honored
- **kit_water_000005:** "Water Bolt / Tidal Surge / Rippling Torrent / Flowing Tide / Drowning Current / Crashing Wave / Surging Current / Eddying Shield" — the WATER vocabulary register is rich; the WS1A.4-lite is picking up "tidal", "torrent", "current" naturally

The per-skill flavor mechanism is thematically COHERENT. This is genuine design success.

### Engine-first / game-second / phase-third orientation

The QDX chain honored the orientation. Engine architectural integrity (canonical commitments) was preserved through the LOCK Q ADDITIVE-ONLY discipline. Game-side (drax MVP refresh) followed engine completion. Phase-level dispatch sequencing held discipline throughout. No engine-canonical amendment was made unilaterally; the substrate-led-WITHIN-element-axis refinement went through gandalf + Matt Pattern B ratification.

---

## 3. Recognition records

### 3.1 Substrate-led WITHIN element axis (canonical refinement)

This recognition deserves its own canonical-story entry. Matt's 2026-06-02 ratification was:

> "substrate-led WITHIN element axis; element axis follows weighted round-robin for genre-true distribution"

This is a substantive Discipline #41 refinement. The original framing ("substrate determines what gets generated") is preserved at the BC-axis / archetype / cultural-tradition layer. At the element-axis layer, **substrate has known coverage gaps** (98%+ physical), and following substrate distribution there produces under-served content. The refined discipline says: **substrate-led applies where substrate has signal; element-axis distribution follows genre-aligned design rule (Option B4.5 weighted round-robin) where substrate would over-concentrate.**

This is a stronger discipline statement than the original. It refuses to be naively-substrate-deferential when substrate has known structural gaps. It composes naturally with the substrate-enrichment workstream — once substrate enrichment lands, the element-axis can return to substrate-led without distribution distortion.

**Recommended canonicalization:** standalone canonical/story record at `canonical/story/2026-06-02-substrate-led-within-element-axis-discipline-refinement.md`. KR to author or route to gandalf during QDX-8 follow-up.

### 3.2 Genre-aligned-distribution discipline candidate

This composes with Discipline #41 refinement but stands on its own:

> **When the engine fires content into a player-facing surface and substrate coverage produces a distribution that conflicts with genre-canonical expectations (ARPG ~40-45% physical / ~55-60% caster), the engine applies genre-aligned distribution at the dimension where the conflict surfaces. Substrate-led applies at dimensions where substrate has signal; genre-aligned applies at dimensions where substrate would produce visible genre-departure.**

This is a Discipline #56 candidate (per jack-ryan's queued discipline harvest). The QDX-5 fire is its empirical demonstration. Worth jack-ryan ratification at QDX-8 engineering-disciplines.md write.

### 3.3 Wave B prompt failure rate as substrate-thinness signal

The 24.3% Wave B fallback rate concentrates on physical / earth / wind / holy — the elements where substrate coverage is thinnest. Caster elements with richer substrate (fire / water / lightning / shadow) produced 0% fallback in the sampling. The Wave B failure rate is operating as a **substrate-thinness signal** — when the LLM has thin signal to work with, the prompt is more likely to parse-fail.

This is worth recognizing as a diagnostic pattern: **Wave B fallback rate per primary element is a substrate-coverage signal for that primary.** If elrond's substrate-enrichment workstream lands richer earth/wind/holy/physical content, the Wave B fallback rate on those primaries should drop without any prompt changes. The empirical prediction would itself validate the enrichment.

### 3.4 Substrate enrichment as highest-leverage next-cycle investment

Both jack-ryan (process lens) and gandalf (design lens) independently surface this as the next-cycle priority. Convergent strategic signal worth recording.

Specifically, the substrate gaps:
- **Earth substrate:** all 16 physical kits + all 3 earth kits have BC axis configuration `melee/medium/flat/STR/none`. The substrate has no earth-caster representation, no earth-ranged representation, no earth-control-with-roots representation. Earth as an element is collapsed into a single archetype.
- **Wind substrate:** 2/3 wind kits hit Wave B fallback — substrate has insufficient wind-caster signal to differentiate wind kits into recognizable archetypes
- **Holy substrate:** 1/3 holy kits hit fallback — somewhat thinner than fire/water/lightning/shadow
- **Physical substrate:** the BC homogeneity issue is real — all 16 physical kits are mechanically identical at the BC layer; substrate enrichment must target BC axis diversity (range / tempo / amplitude / proxy-density) not just cultural-tradition

The elrond workstream is scope-substantial. It is also the highest-leverage move.

### 3.5 Per-skill flavor-or-canonical decision empirical success

WS1A.4-lite operating across 37 kits with 0 fallbacks, 30.3% flavor rate, Q18 pool validation passing across 5 elements I sampled — this is empirical success of the mechanism that was canonically defined in the Season-Archive pivot doc 3.2. Worth recognizing in `canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md` cross-reference: "Empirically validated at production scale via QDX-5 (event kse_20260602_008); 0 fallbacks across 86 flavor decisions + 110 canonical decisions; Q18 allow-list compliance 100% on inspected samples."

---

## 4. 4 INFO design-quality lens

### INFO 2-A — Substrate-derived fallback name duplicates within-primary

**Design severity: high (player-facing immersion break).**

This is the most player-visible issue surfaced by QDX-5. If a player browses the chernoff celestial body Stage A and sees three identical "Earthen Earth Fighter Bearer" entries, the failure mode is recognizable instantly: "this game has AI-generated content that didn't get caught."

**Two compounding problems:**

1. **The fallback composition rule produces redundant names.** "Earthen Earth Fighter Bearer" — "Earthen" + "Earth" is element-repeated. "Iron Physical Fighter Bearer" — "Physical" is a system-vocabulary word that should never appear in a player-facing class name. The composition rule was authored against an assumption that the element token and the substrate-derived prefix would be disjoint, but for element-anchored substrate (where "iron" / "earthen" carry element-meaning), they collide.

2. **The duplicate detection only checks for systematic template-repeat, not substrate-fallback duplicates.** The `wave_b_template_repeat_detected=False` flag is technically accurate (no LLM template applied) but operationally misleading (within-primary identity collisions occurred via a different mechanism).

**Design recommendation (rank-ordered):**

1. **Short-term fix (LOCK L iteration cycle):** amend the fallback composition rule to detect element-token-redundancy and avoid it. If "earthen" already encodes earth-element, don't append "Earth" again. Replace "Fighter" with archetype-specific role-noun ("Warden" / "Smasher" / "Stoneward"). Avoid the word "Bearer" — it reads as machine-generated.
2. **Medium-term fix (substrate enrichment):** richer substrate produces less Wave B fallback. The pattern will diminish naturally as substrate enrichment lands.
3. **Within-primary deduplication safety net:** if Wave B falls back AND the fallback name would duplicate an existing kit within the same primary element, force a regeneration with a different fallback-composition path.

### INFO 2-B + WARN 2 — Faction-token leakage into caster identity names

**Design severity: medium (intentionality unclear; convergence is the concrete risk).**

"Scattered," "Meridian," and "Reach" appear 7+ times across non-physical kit identities. Sample-confirmed:
- water_000005: "Tidecaller of the Scattered Reach"
- fire_000006: "Ember Caster of the Scattered Reach"
- lightning_000005: "Stormcaller of the Scattered Meridian"
- shadow_000007: "Penumbra Caster of Dusk Meridian"
- holy_000005: "Cannonade Cleric of Scattered Light"

**The design question:** is this faction-coherence-via-naming (intentional; tokens express faction membership in the kit name), or template-pickup (incidental; LLM grabbed faction tokens because they were nearby in context)?

**My reading: it's a design opportunity that surfaced as incidental and warrants a deliberate decision.**

Pro-coherence framing: factions in Diablo 2 / Lost Ark / Last Epoch have visible naming influence on the classes within them. If "Scattered Meridian" is a faction, kits with that faction-affiliation reading "Tidecaller of the Scattered Reach" makes faction membership LEGIBLE in the identity. This is a feature.

Anti-coherence framing: too many kits sharing location-token vocabulary blurs the differentiation that emergent identity is supposed to provide. If "Scattered Reach" appears in 2-3 different element primaries, the location is no longer distinctive — it's just a default suffix.

**Design recommendation:** make the call deliberately. If faction-coherence is the intent, ensure each kit's faction is the ONE faction whose token appears in its identity (not random pickup across factions). If not, constrain Wave B prompt to avoid faction-token vocabulary, and let location/region descriptors emerge from cultural-tradition substrate.

The "Scattered" adjective specifically is weak as a place-descriptor. Diablo / PoE / LE places are named with specificity ("Khurzan", "Wraeclast", "Eterra"). "Scattered" reads as a fallback descriptor when no real place-name is available. This is worth addressing whichever direction the faction-coherence call goes.

### INFO 4-A + WARN 1 — t4_selection null on 4/37 kits

**Design severity: low (89% population is operationally acceptable; correlates with quality issues elsewhere).**

The null T4s correlate with other quality issues (kit_physical_000016 and kit_physical_000018 share name "Groundbreaker of the Flat March" AND both have null T4). The correlation pattern jack-ryan flagged — same BC-axis configuration producing both null T4 AND LLM identity collision — points to a unified root cause: ClassGenerator producing structurally identical seeds.

This is not architecturally concerning per se (the pipeline fires correctly; T4 algorithm has no scoring signal to work with when BC axis contribution is empty/identical). It IS a signal that BC axis diversity is the substrate-enrichment target, not just cultural-tradition / period content.

**Design recommendation:** treat T4 null rate per element as a BC-axis-diversity diagnostic. Track over time; expect it to drop as substrate enrichment introduces BC axis variety. No prompt change or pipeline change required.

### INFO physical BC axis homogeneity (WARN 4)

**Design severity: medium-structural.**

All 16 physical kits share identical BC axis configuration (melee/medium/flat/STR/none). This is the deepest substrate constraint. It manifests as:
- Identity collisions on physical
- T4 null on physical
- Wave B fallback rate elevated on physical (3/16)
- All physical kits feel mechanically similar to each other

**This is not addressable without elrond substrate-enrichment.** The pipeline cannot differentiate kits that have identical BC-axis seeds. The naming layer can paper over this for a few kits but breaks down at 16.

**Design recommendation:** elrond substrate-enrichment workstream must target BC axis diversity for physical specifically (introduce ranged-physical, control-physical-with-grapples, tempo-fast-physical, tempo-slow-physical archetypes). Cultural-tradition enrichment alone does not solve the BC homogeneity issue.

---

## 5. Strategic re-engagement options for Matt

Ranked by gandalf design-steward perspective:

### (A) Elrond substrate-enrichment workstream — highest priority

**Why first:** the QDX-5 quality ceiling is substrate-bound. Every quality concern surfaced in this audit (Wave B fallbacks, identity collisions, T4 null rate, physical BC homogeneity) traces back to substrate thinness on specific dimensions. This is convergent with jack-ryan's process-lens strategic signal — both sides of the critique pair independently surface this as next-priority.

**Scope sketch:**
- Elrond catalogue work: source + curate substrate content targeting earth-caster, wind-caster, holy-variety, and physical BC-axis diversity (not just cultural-tradition content)
- Gandalf canonical writes: substrate composition policy refinements per element; archetype-coverage targets; canonical recognition of substrate-thinness diagnostic patterns
- Rocket consultation: BC-axis-diversity targets for ClassGenerator-side coverage; element-keyword library refinement for `infer_element_from_name()`
- Star-lord telemetry: per-element substrate-coverage metrics; Wave B fallback rate per primary as substrate-thinness indicator

**Empirical re-engagement criterion:** next kit-space-expansion event (QDX-9 or equivalent) shows Wave B fallback rate drop on the enriched primaries AND identity collision rate drop AND T4 null rate drop. The empirical evidence is exactly the diagnostic patterns we already track.

**Estimated horizon:** multi-cycle (substrate enrichment is sustained work; not a one-shot dispatch).

### (B) MM-P1 chernoff celestial body four-stage flow design session

**Why second:** Pattern B substantive design session with Matt. Now grounded by 37 kits empirically rather than hypothetically. The Stage A browse-the-kit-space mechanism has its first real substrate to design against.

**What changed since this was last deferred:**
- 75 kits in kit_space (38 historical EAA-5 v2 + 37 QDX-5) — non-trivial browsable space
- Faction emergence empirical (3 factions named)
- Per-skill flavor metadata available for rendering
- Vercel preview already renders the data (drax MVP shows what's possible without UI redesign)

**Pattern B scope** (per `2026-06-01-session-close-out-IA-chain-resume.md` § 3.6 + the 4 additions from Season-Archive pivot § 7.3):

- Stage A celestial-spirit-browse UX design (now empirical)
- Stage B materialization in tattered period clothing
- Stage C customization layer
- Stage D L50 decked-out reveal
- 13. Kit space chronicle UX (engine page redesign)
- 14. Realm Expansion content design discipline
- 15. Underplayed-kit telemetry mechanism
- 16. Ascension-as-strategic-choice UI/UX surfacing

**Composes with (A):** MM-P1 design can fire in parallel with substrate enrichment. Design can reference current kit-space empirically while better kits land downstream.

### (C) Wave B prompt improvement workstream

**Why third:** addresses the visible immersion-break surface (fallback duplicates with redundant element-tokens) without waiting for substrate enrichment. Cheaper, bounded, surface-symptom rather than structural.

**Scope sketch:**
- Amend fallback composition rule to avoid element-token redundancy ("Earthen Earth Fighter Bearer" → something like "Stoneward of the Earthen Tradition" via substrate-tradition lookup)
- Add within-primary deduplication safety net to Wave B (regenerate if fallback would duplicate within primary)
- Tighten Wave B prompt to avoid generic descriptors ("Scattered" as place-adjective; "Fighter" / "Bearer" as role-nouns)

**LOCK L iteration discipline applies** — 2+ Gate-2 BLOCKs would escalate; otherwise within-seam.

**Composes with (A) but is partially redundant:** substrate enrichment naturally reduces Wave B fallback rate. Doing (C) before (A) catches the surface symptom; doing (A) first reduces (C) scope. My soft-lean: do (C) as a small follow-on after (A) is underway, to catch any residual fallback patterns at richer substrate.

### (D) Economic-veteran problem design session

**Why fourth (deferred per its own gate):** per Season-Archive pivot § 5, this gates on materials/trading scope opening. No empirical evidence has arrived to trigger re-engagement. The deferral is correct.

**Re-engagement criterion (unchanged from pivot doc):** materials/trading/economy implementation scope authorized.

### (E) Other strategic options the QDX outputs reveal

A few that surfaced during this audit that don't fit the (A-D) buckets:

- **Drax engine-side faction grouping data exposure** — drax QDX-7 routing note 1 (faction grouping NOT in per-kit `emergent_kit_concept`) means drax has to fetch faction membership from Phase 5a clustering data. Worth a small rocket/star-lord ADDITIVE workstream to add per-kit `faction_id` to the kit JSON; would let drax do faction-grouped rendering without composing two data sources. Small scope; high UX leverage.
- **Per-skill `is_active=false` semantics review** — kit_lightning_000005 has populated T4 with `is_active=false`. The semantics across the 33 populated kits need rocket clarification. May indicate a deeper T4 selection-vs-activation distinction worth canonical capture.
- **Engine page chronicle visualization for cross-event compounding** — 75 kits across 8 events is now interesting browsing-space. The engine page chronicle is currently event-by-event. A cumulative-growth visualization (kit count over events; element distribution shifting over events; substrate diversity over events) would tell the Realm Expansion story visually.

These are small-scope items; not strategic re-engagement directions on their own. Worth queuing for whatever cycle picks them up.

---

## 6. Composition with canonical commitments

### Season-Archive Realm-Expansion pivot — PRESERVED + REINFORCED

The QDX-5 fire is exactly the kit-space-expansion event the canonical record describes. Architectural commitment is operating as canonically declared. The Realm Expansion model's substrate compounds with each event (75 kits across 8 events now). REINFORCED via empirical compounding.

No amendments to the canonical record required.

### Discipline #41 substrate-led — REFINED (canonical refinement)

Matt-ratified 2026-06-02 interpretation: substrate-led WITHIN element axis; element-axis distribution follows genre-aligned weighted round-robin where substrate coverage gaps would produce visible genre-departure.

The refinement is stronger than the original ("substrate-led applies where substrate has signal; not where substrate has known structural gaps"). Composes naturally with substrate-enrichment workstream as the path to return element-axis distribution to substrate-led naturally.

**Recommended canonicalization:** new canonical/story record `2026-06-02-substrate-led-within-element-axis-discipline-refinement.md` capturing the refined discipline statement. KR or gandalf to author in QDX-8 follow-up.

### Canonical 39 substrate-bound at Phase 2 — REFRAMED (interim posture)

The canonical 39 § 1 Phase 2 substrate-bound architecture is REFRAMED to:

> "Phase 2 (canonical 39 § 1) defines the substrate-bound generator (`BcTargetSubspaceGenerator`) as the steady-state path. INTERIM (pending substrate enrichment): when substrate coverage is empirically insufficient to honor canonical-7+1 element distribution at genre-aligned proportions, ClassGenerator + weighted round-robin element assignment (Option B + B4.5 amendment) is the operative path. The canonical-39-substrate-bound path resumes once substrate enrichment lands sufficient coverage."

This is reframing, not amendment — canonical 39's architectural intent is preserved; the current operative posture is named explicitly as interim with a clear path back to canonical-39-pure.

**Recommended canonicalization:** annotate `canonical/39-qd-engine-end-to-end-workflow-2026-05-24.md` with an INTERIM POSTURE note referencing the substrate-enrichment workstream. KR to route to jack-ryan or gandalf in QDX-8 follow-up.

### Q18 vocabulary lock — PRESERVED + EMPIRICALLY VALIDATED

WS1A.4-lite consumed Q18 vocabulary at per-skill grain across 37 kits with 100% allow-list compliance on inspected samples. The Q18 lock is in active use, not theoretical. PRESERVED with empirical validation note.

**Recommended canonicalization (light):** annotate `canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md` with cross-reference to QDX-5 empirical validation. Light touch.

### Architecture A (canonical-7+1; physical as taxonomy-sibling) — PRESERVED

Physical kits opt out of WS1A.4-lite per Architecture A. Sample confirmed: physical kits carry no `ws1a4_*` fields; physical opt-out counter = 16 in chronicle. Architecture A operating as canonically committed.

### Earth meta-layer + ascension + form-library — PRESERVED (not stressed by QDX scope)

Out of scope for QDX chain. Preserved framing; composes at MM-P1.

### Engineering-disciplines #41 / #42 / #49 / #50 / #51 / #52 / #53 — PRESERVED

All preserved. #41 receives the refinement noted above.

### New discipline candidates surfaced

For jack-ryan ratification at QDX-8 engineering-disciplines write (per wave-state § 6):

1. **#56 candidate — Genre-aligned distribution discipline** (per gandalf transmission queue): when substrate coverage would produce a distribution conflicting with genre-canonical expectations on a player-facing dimension, the engine applies genre-aligned distribution at that dimension; substrate-led applies at dimensions where substrate has signal
2. **QD-engine workflow integration-via-LOCK-J ADDITIVE-ONLY** discipline (composes with #53; per wave-state § 6)
3. **Per-skill flavor LLM judgment composition with Wave A/B identity LLM** (cross-LLM-call composition discipline; per wave-state § 6)
4. **Multi-pipeline (legacy ClassGenerator + QD-engine workflow) fire-script discipline** — explicit pipeline naming per Discipline #54/#55 plus EAA-8-queued generator-path-explicit-naming
5. **Wave B fallback rate per primary as substrate-thinness diagnostic** (gandalf-surfaced this audit): the per-primary Wave B fallback rate operates as a substrate-coverage signal; tracking it diagnostically informs substrate-enrichment prioritization

---

## 7. Sign-off

**Overall verdict:** PASS-with-design-concerns.

The QDX chain delivered the architectural objective. The pipeline composes cleanly. Caster identities are genuinely on-genre. Per-skill flavor mechanism works thoughtfully. The Realm Expansion architectural commitment is reinforced via empirical compounding. Matt's verbalized chain-close goal (Cycle 14 wave-5-equivalent richness with WS1A.4-lite per-skill flavor) is empirically met.

The design concerns are bounded and structural — 24.3% Wave B fallback rate on substrate-thin primaries producing player-visible identity collisions; faction-token semantic clustering needing a deliberate design call; physical BC axis homogeneity collapsing 16 physical kits to one BC archetype. All three concerns are tractable. The first two are addressable at the prompt/composition layer (Wave B prompt improvement workstream). The third requires substrate enrichment.

**Top strategic re-engagement options:**

1. **Elrond substrate-enrichment workstream** — highest leverage; convergent with jack-ryan's process-lens signal; address structural root of all surfaced concerns; canonical posture cleanup (returns canonical-39 substrate-bound to pure form)
2. **MM-P1 chernoff celestial body four-stage flow design session** — now empirically grounded by 37 kits; can fire in parallel with (1)
3. **Wave B prompt improvement** — bounded surface-fix; composes with (1); pick up after (1) is underway

**Recognition records recommended:**

- New canonical/story: `2026-06-02-substrate-led-within-element-axis-discipline-refinement.md` (Discipline #41 refinement; KR or gandalf to author)
- Annotation: canonical/39 INTERIM POSTURE note (KR to route)
- Annotation: `canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md` empirical-validation cross-reference (light touch)
- Discipline #56 candidate (genre-aligned distribution) + Wave-B-fallback-rate-as-diagnostic candidate — queued for jack-ryan engineering-disciplines.md write

**Quality observations for ground-state § 1:**

- Kit space now 75 kits across 8 expansion events; substrate compounding visible
- WS1A.4-lite operating at production scale (37 kits / 0 fallbacks / Q18 100% compliance on samples)
- Substrate-led WITHIN-element-axis interpretation operational (Discipline #41 refinement Matt-ratified)
- Substrate enrichment surfaced as next-priority by both critique-pair sides convergently

**Compositional commitments preserved:** Season-Archive Realm-Expansion + Q18 lock + Architecture A + canonical-7+1 + BC axes + Earth meta-layer (untouched) + canonical 39 (REFRAMED as interim posture with path back to pure).

**No BLOCKs issued.** This is LOCK H note-only audit. PASS-with-design-concerns reflects design-quality lens; not gate authority.

---

**Signed:** gandalf (story-and-design steward) 2026-06-02
**LOCK H authority:** standard design-quality audit at workstream close (note-only)
**Composition:** preserves all load-bearing canon; refines Discipline #41 per Matt-ratified interpretation; reframes canonical 39 as interim-posture-with-path-back-to-pure; surfaces 5 discipline candidates for jack-ryan ratification

**End of audit.**
