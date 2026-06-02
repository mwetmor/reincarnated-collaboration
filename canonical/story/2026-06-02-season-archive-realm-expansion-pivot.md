# Season Concept ARCHIVED — Realm Expansion Pivot

**STATUS:** CURRENT (architectural commitment; load-bearing for all engine workflow + player-surface design from this point forward)
**Date:** 2026-06-02
**Author:** gandalf (story-and-design steward) per Pattern B substantive design session with Matt
**Authority:** Matt 2026-06-02 ratification ("season = archived. We have lost the concept of season with the introduction of the 'chernoff celestial body'... Realm Expansion confirmed, path α, draft the canonical record")
**Companion docs:**
- `canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md` (Q18 vocabulary lock; preserved; per-skill flavor consumption per § 5)
- `canonical/00-ground-state.md` § 1 (current truth — update needed post-this-record to reflect season-archival)
- `agentic_orchestration/gandalf/notes/2026-06-01-session-close-out-IA-chain-resume.md` § 3 (MM-P1 vision-clarification; chernoff celestial body framing)
- `agentic_orchestration/gandalf/notes/2026-06-01-q18-deferred-commitments.md` (preserved; per-skill flavor-or-canonical decision composes per Matt 2026-06-02 clarification)
- `canonical/historical/19-llm-call-map.md` (R8 inverted-mode reference — historical; mechanism RETIRED via this pivot)
- `canonical/historical/30-engine-explainer-current.md` (legacy 4-canonical-element-flavor-substitution reference — historical; mechanism RETIRED via this pivot)
- `canonical/39-qd-engine-end-to-end-workflow-2026-05-24.md` (QD-engine workflow Phase 1-8; remains for substrate-exploration cycles; NOT for normal player-facing content)
- Project memory `project_earth_meta_layer.md` (Earth meta-layer + ascension-as-strategic-choice; preserved; reinforced)

---

## 0. TL;DR

The **season concept is ARCHIVED** as Reincarnated's content-release unit. Three architectural shifts compose:

1. **Kit space is continuous** — engine generates kits into a continuously-growing chernoff substrate space; not into per-season buckets
2. **Realm Expansion** replaces seasons as content-release mechanism — new Maps, Acts, Game Modes released as substrate engagement; can be designed to surface value of under-played kit groupings
3. **Ascension-as-strategic-choice** preserved as player-driven mechanism; NOT forced as seasonal reset

**Player-driven discipline** explicit: no dev-imposed churn; no forced seasonal resets; no FOMO mechanics. Player chooses when to ascend, when to try new kits, when to engage new content. Genre departure from PoE league / D4 season / LE cycle conventions is deliberate.

**Existing seasons (season_000001 through season_000200)** preserved as historical artifacts per Path α; not migrated to kit space; remain accessible as design-evolution lineage record.

---

## 1. What is ARCHIVED

### 1.1 The season concept as content-release unit

| Mechanism | Archival disposition |
|---|---|
| Season as temporal content-release unit | ARCHIVED |
| Season-numbered ("season_000042") as production identifier | ARCHIVED for new generation; existing season-numbered artifacts preserved as historical |
| Per-season class roster generation (5 / 11 / 10-12 per season) | ARCHIVED |
| Per-season theme cohesion (theme_element field; forge/brine/etc.) | ARCHIVED |
| R8 inverted-mode theme coalescence pipeline | ARCHIVED — see § 1.2 |
| Cosmological vocabulary slot-fill mechanism (ignition / suffusion / bulwark / etc. themed per-season) | ARCHIVED — see § 1.3 |
| Per-season seasonal_dominant_element overlay on kit primary | ARCHIVED |
| Per-season cosmological_vocabulary.json artifact | ARCHIVED for new generation |
| Seasonal_elements / elements_metadata manifest fields | ARCHIVED |
| The seasonal-journey-as-content-release-schedule reading of project canon | ARCHIVED — see § 1.4 reinterpretation |

### 1.2 R8 inverted-mode theme coalescence

Mechanism per `canonical/historical/19-llm-call-map.md` R8 amendment 2026-05-19:

> "Phase A `element_selection` is replaced by `theme_coalescence` in the new default pipeline (the `inverted` mode committed per R8 Sub-case 3)."

This mechanism is **archived** with the season concept. Theme coalescence operates per-season; with seasons archived, the mechanism no longer has an anchor. Engine workflow simplifies — no theme coalescence at kit generation; each kit emerges from substrate inputs (primary + cultural-tradition + period + chain composition + T4) without season-level theme overlay.

### 1.3 Cosmological vocabulary slot-fill mechanism

Mechanism: 8 effect-category slots (ignition / suffusion / bulwark / displacement / impact / radiance / penumbra / resonance) themed via per-season LLM vocabulary (Pit-Flame Surge / Quench Flood / Slag Wall / Bellows Gust / etc.).

This mechanism is **archived** alongside R8 inverted mode. Skill naming shifts to **per-skill LLM flavor-or-canonical decision** per Matt 2026-06-02 clarification (see § 3.2 below). Q18 vocabulary becomes the per-skill flavor pool; cosmological_vocabulary mechanism retires.

### 1.4 Reinterpretation of seasonal-journey project canon

Project memory `project_earth_meta_layer.md` framed the "seasonal-journey-as-descent + return-to-Earth pattern" as foundational. This framing is **preserved at the narrative-layer** but **decoupled from content-release-schedule**:

- **Narrative layer (preserved):** the protagonist's reincarnation arc IS a journey across lifetimes (descent into trial-realms + ascension back to Earth Self). Each character the player embodies IS a lifetime within that journey.
- **Content-release-schedule layer (archived):** the "season" as a temporal/economic content cycle is NOT load-bearing for the narrative; live-service rhythm decouples from narrative arc.

The seasonal journey persists as **story framing**; not as content-release mechanism.

---

## 2. What is PRESERVED

### 2.1 Engine substrate + kit identity emergence

All Q18-era architectural commitments hold:
- WS1A.Q18 Architecture A LOCK (109 entries; canonical-7+1; physical as taxonomy-sibling)
- Q18 vocabulary pool per primary element
- BC axes (substrate measurement coordinate)
- Substrate composition policy (Option α / β / C semantic locks)
- canonical-7+1 element catalog (`config/elements.yaml`)
- Pool.json v1.1 (post-WS1A.Q18 migration)
- Disciplines #41 / #42 / #49 / #50 / #51 / #52 / #53

### 2.2 Per-kit identity architecture

Each kit emerges from substrate inputs:
- Primary element (1; or 2 if hybrid) from canonical-7+1
- Cultural-tradition + period (from substrate library)
- Chain composition + T4 selection + supporting chain
- Per-skill flavor-or-canonical naming (per § 3.2; Q18 vocabulary consumed at per-skill judgment)
- Emergent kit concept (Wave B identity LLM; e.g., "Necromancer" emerges from shadow + necromantic-folk + decay-flavored skills)

NOT per-season theme overlay. NOT season-specific naming. Each kit stands as itself in the continuous kit space.

### 2.3 Earth meta-layer + ascension architecture

Project memory `project_earth_meta_layer.md` mechanisms preserved + reinforced:
- Earth Self as persistent player identity across lifetimes
- Form library as gacha-style accumulation of LLM-generated ascended spirits
- Ascension as strategic player choice (NOT forced)
- Spirit-swap-as-class-differentiation (player can embody different kits across lifetimes)

Per Matt 2026-06-02 strategic clarification: ascension becomes more appealing as Realm Expansion content surfaces value of currently-Earth-Self-strengthening over currently-active-character-strengthening. Player-driven choice.

### 2.4 MM-P1 chernoff celestial body four-stage flow

Per `agentic_orchestration/gandalf/notes/2026-06-01-session-close-out-IA-chain-resume.md` § 3:
- Stage A — Celestial spirit form (player browses/selects from chernoff substrate; kit space is the space)
- Stage B — Materialization in tattered period clothing
- Stage C — Customization (gender / hair / features / skin / tattoos)
- Stage D — L50 decked-out reveal (Tier 2 Set + Legendary gear; skill + gear auras)

Composes natively with the kit space model: Stage A IS browsing the kit space.

---

## 3. What is NEW

### 3.1 Realm Expansion as content-release rhythm

Replaces "season" as Reincarnated's content-release mechanism.

**Mechanism:**
- Engine continuously expands the kit space via parameter scope expansion (e.g., Q18 lock added new primary coverage; future scope expansions add more kits)
- Realm Expansion releases new playable surfaces: **Maps, Acts, Game Modes**
- New Realm content can be **designed to surface value of under-played kit groupings** (substrate-led at the content-engagement layer)
- Player engagement loop: pick from kit space → engage with Realm content → if a new Realm surfaces value of an underplayed kit, player self-selects to try it

**Player-facing framing:**
- "A new Realm has opened: the Frozen Tundra"
- "The Pyralis Trial cycle is live for water-aligned kits"
- "New Game Mode: Eternal Ascent — favors high-mobility kits"

**NOT player-facing:**
- "Season 5 is live"
- "Old season characters are retired"
- "Roll a new character for the new season"

### 3.2 Per-skill LLM flavor-or-canonical naming (Q18 vocabulary consumed)

Per Matt 2026-06-02 clarification:

> "flavor element = applied only means to use it within the naming of the skill. A character/kit does not need to have a flavor element tag at all... just because it is a necromancer that uses bone spear does not mean that it should be thought of as a bone necromancer"

**Mechanism:**
- Per-skill LLM decision: should this skill be flavored (use Q18 vocabulary word) OR stay canonical?
- If flavor: pick a word from the kit's primary element's Q18 pool
- If canonical: use canonical naming convention (e.g., "Shadow Bolt" rather than "Wraith Touch")
- Kit identity: primary element only (no sub-element commitment); emergent kit concept (e.g., "Necromancer") derives from primary + cultural-tradition + period + chain composition + T4

**Example — Shadow primary necromancer kit (6 skills):**
```
Skill 1: LLM picks YES + "bone"   → "Bone Spear"
Skill 2: LLM picks NO             → "Shadow Bolt"
Skill 3: LLM picks YES + "wraith" → "Wraith Touch"
Skill 4: LLM picks NO             → "Shadow Drain"
Skill 5: LLM picks YES + "shade"  → "Shade Veil"
Skill 6: LLM picks NO             → "Shadow Curse"
```

Kit identity stays **Shadow Necromancer**. "Bone" is a contextual skill-name flavor on Skill 1; not a kit identity tag.

**This RETIRES** the prior WS1A.3 framing (per-kit sub-element selection) and SIMPLIFIES WS1A.4 (per-skill bounded judgment becomes flavor-or-canonical binary + Q18-word-pick, no hybrid 15-option matrix).

### 3.3 Continuous kit space

The kit space is the chernoff substrate — continuously growing, addressable by kit-identity coordinates, accessible to player via Stage A celestial body browsing.

**Kit space properties:**
- Each kit has a stable kit-id (not season-numbered; permanent space identifier)
- Kits added via engine parameter scope expansion events (chronicled per § 3.4)
- Player can browse the full space at Stage A (not restricted to "current season's roster")
- Kits don't expire / get retired by dev-imposed lifecycle (player may choose to ascend characters; that's player-driven)

**Implementation implication for engine:**
- Engine output schema shifts from per-season-manifest to per-kit-entry-into-space
- Kit space chronicle (when kit was added; via which parameter expansion; what substrate inputs)
- Per-kit-detail JSON consumed by drax loadout app

### 3.4 Engine kit-space expansion chronicle

Replaces per-season chronicle on the engine page.

**Chronicle records:**
- Parameter expansion event timestamp + scope (e.g., "2026-06-02: Q18 vocabulary lock added — 109 sub-element flavor entries; kit space expansion run produced 87 new kits")
- Per-expansion-event substrate inputs that changed
- Per-expansion-event kits generated
- Per-kit substrate-trace (what inputs produced this kit)
- Realm Expansion events (when new Maps / Acts / Game Modes released; which kit groupings the design surfaces value of)

**Engine page composition:**
- Kit space browser (filter by primary / cultural-tradition / period / etc.)
- Parameter expansion event timeline
- Realm Expansion event timeline
- Per-kit detail view (substrate inputs → emergent identity)

### 3.5 Realm-Expansion-can-target-underplayed-kits design discipline

Per Matt 2026-06-02 design framing:

> "we can specifically tailor these to fit the under-played character kits (if we desire)"

**Mechanism:**
- Telemetry tracks per-kit engagement (which kits get played; which don't)
- Realm Expansion design phase consults under-played-kit telemetry
- New Realm content can be designed to highlight kit groupings that have lower engagement
- Players who try the new Realm naturally encounter value in underplayed kits; may self-select to switch

**Player-facing payoff:** "The Frozen Tundra Realm has opened — survival-focused kits excel here." Player checks their owned kits → sees their water-frost-aligned kit they hadn't played → tries it for the new Realm.

This is a **substrate-led discipline applied at the content-engagement layer** (Disc #41 composition). The substrate (kit engagement telemetry) shapes content design.

---

## 4. Genre departure — conscious commitment

ARPG genre convention is **seasonal**:

| Game | Seasonal mechanism |
|---|---|
| Path of Exile | League seasons (~3 months); economy reset; standard league preserves |
| Path of Exile 2 | Going seasonal at launch |
| Diablo 3 | Seasons with seasonal characters; non-seasonal preserves |
| Diablo 4 | Seasons; seasonal characters can't trade with eternal |
| Last Epoch | Cycles with similar reset/preservation split |
| Diablo 2 (ladder) | Ladder seasons reset; non-ladder preserves |

Reincarnated **departs from this convention.**

**Reasons for the departure (substantive design rationale):**

1. **Isekai narrative pairs naturally with continuous reincarnation-space** rather than forced-reset seasonal cycles. The protagonist of an isekai chooses their journey across lifetimes; the world doesn't dev-impose "your isekai life is over now, start fresh."
2. **Player-driven discipline** — the project's design instinct favors player-driven choice over dev-driven imposition. Forced seasons are dev-driven.
3. **Earth meta-layer + ascension architecture** provides player-driven equivalent (ascension is voluntary; strengthens Earth Self over time; player decides when).
4. **Continuous kit space** matches the "spirit-swap-as-class-differentiation" framing — kits don't expire when a content cycle ends; player can engage any kit at any time.
5. **Realm Expansion content rhythm** provides "what's new" without requiring character retirement.
6. **Substantially simpler engine architecture** — no per-season theme coalescence overhead; no cosmological vocabulary maintenance; engine focuses on substrate expansion rather than season cycling.

**Genuine risks worth conscious commitment:**

1. **ARPG player expectation friction** — players coming from D4/PoE may expect seasonal mechanics; absence may read as missing-feature rather than design-choice
2. **Live-service engagement loop replacement is unproven** — Realm Expansion as content rhythm depends on substantial periodic content releases; sustaining this cadence is a real production commitment
3. **Economic-veteran problem** — see § 5 deferred design discussion

**Disposition:** the genre departure is RATIFIED per Matt 2026-06-02 as deliberate architectural commitment. Future Matt + future agents understand this is conscious choice, not oversight.

---

## 5. Deferred design discussion — economic-veteran problem

**The question (Matt 2026-06-02 verbatim):**

> "if/when we implement materials/trading/etc we may need a way to force seasonal moves. I am still least certain of this. Is there another way to solve for the incumbent player's market capital being prohibitive towards the acquisition of future/new player base?"

The genre-default solution (forced seasonal reset) is one mechanism for solving "incumbent capital prohibits new-player entry." Reincarnated has archived seasons; the economic-veteran question warrants its own design session before materials/trading scope opens.

### 5.1 Five alternatives surfaced (Pattern B 2026-06-02)

| Alternative | Mechanism | Composes with Reincarnated architecture |
|---|---|---|
| **A1 — Ascension as economic reset** | Player ascends character → capital flows to Earth Self → new character starts fresh economically | Ascension-as-strategic-choice + Earth meta-layer |
| **A2 — Earth-realm vs Trial-realm economic separation** | Earth Self = long-term capital storage; per-character/per-trial = temporary economies (each fresh) | Earth meta-layer + spirit-swap differentiation |
| **A3 — Realm-anchored economy** | Each Realm Expansion has its own market that opens fresh; veteran capital doesn't dominate new-realm-launch | Realm Expansion content rhythm |
| **A4 — Bound-on-acquisition for end-game items** | Rarest items become character-bound when acquired; can't be re-traded indefinitely | Genre-canonical; simplest implementation |
| **A5 — Hybrid: A1 + A2 + A3 (composed)** | Per-character economies + voluntary economic reset via ascension + realm-fresh markets | Composes naturally; design coherence |

**Gandalf soft-lean: A5 hybrid.** Reasoning: no single mechanism is load-bearing alone; system has multiple natural pressure-releases; player-driven discipline preserved.

### 5.2 Empirical-evidence trigger for re-engagement

**Architectural commitment deferred pending:**
- Materials / trading / economy scope opens for design
- Pattern B substantive design session on economic-veteran question
- Decision composes with then-current state of player base + telemetry + market design

**Empirical-evidence signal that would re-engage:**
- Materials / trading / economy implementation scope authorized
- Telemetry surfaces evidence on whether ascension-as-voluntary-mechanism naturally addresses veteran-capital concentration
- Realm Expansion content rhythm reveals whether per-realm markets self-stabilize

### 5.3 What this section establishes

- The economic-veteran problem is RECOGNIZED + EXPLICITLY DEFERRED (not dismissed; not resolved)
- 5 alternatives surfaced + gandalf-lean named (A5 hybrid)
- Materials/trading scope opens → Pattern B substantive design session fires → decision lands
- Does NOT gate Realm Expansion architectural commitment (that lands now; economic question composes when scope opens)

---

## 6. Existing seasons disposition (Path α — historical preservation)

Per Matt 2026-06-02 ratification ("We can leave prior seasonal data as historical content"):

**Existing seasons** at `~/Games/reincarnated-engine/seasons/season_*` (season_000001 through season_000200) are **preserved as historical artifacts.**

**Disposition:**
- Existing season manifests + class JSON + monster JSON + gear / trial / etc. preserved
- Not migrated to kit space
- Not deleted
- Engine page (post-architectural-amendment) may include "historical seasons" view as design-evolution lineage reference
- Future tooling browses them as "early-era seasons from when the concept existed"
- Composes with project's overall design-evolution discipline (don't lose history)

**Operational implication:**
- Engine workflow amendment introduces kit-space-output schema for NEW kit generation
- Existing seasonal artifacts continue to exist as historical context
- Drax loadout app for V1/V2 deployed seasons: keep as-deployed historical reference; future drax development consumes kit space

---

## 7. Architectural commitments triggered by this canonical record

The following workstreams unblock (or are amended) by this commitment:

### 7.1 Engine architectural amendment (substantial; ~10-20 sessions; rocket + star-lord lead)

- Retire R8 inverted-mode theme coalescence pipeline
- Retire cosmological_vocabulary slot-fill mechanism
- Retire per-season class generation cycle
- Implement kit-space-expansion infrastructure (engine fires on parameter scope expansion; emits kits to continuous space)
- Implement per-skill LLM flavor-or-canonical decision (Q18 vocabulary consumed; was WS1A.4-lite)
- Implement kit-space chronicle + parameter expansion event tracking
- Cross-seam contracts amended per ADR-004 MIGRATION discipline

### 7.2 Drax + engine page reframe (post-engine-architectural-amendment)

- Engine page chronicles kit space growth + Realm Expansion events (replaces per-season pages)
- Drax loadout app consumes kit space (replaces per-season manifests)
- Chernoff celestial body Stage A = kit space browse/filter
- Stages B-C-D play through with chosen kit (chosen from kit space)

### 7.3 MM-P1 design session composition

The MM-P1 substantive design session continues with the kit-space-and-Realm-Expansion architecture as backdrop. Twelve-item agenda from `2026-06-01-session-close-out-IA-chain-resume.md` § 3.6 composes naturally + adds:

- 13. Kit space chronicle UX (engine page redesign)
- 14. Realm Expansion content design discipline
- 15. Underplayed-kit telemetry mechanism
- 16. Ascension-as-strategic-choice UI/UX surfacing

### 7.4 Deferred work (NOT gated by this record; flagged for future engagement)

- Economic-veteran problem design session (per § 5; gates on materials/trading scope)
- Live-service engagement loop empirical validation (gates on first Realm Expansion content release)
- Telemetry instrumentation for underplayed-kit detection (gates on first kit-space generation)

---

## 8. Cross-references

### 8.1 Composes with (preserved canon)
- `canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md` (Q18 vocabulary; consumed by per-skill flavor-or-canonical decision per § 3.2)
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` (substrate measurement coordinate; preserved)
- `canonical/39-qd-engine-end-to-end-workflow-2026-05-24.md` (QD-engine workflow Phase 1-8; preserved for substrate-exploration cycles; NOT for normal kit-space-expansion)
- Project memory `project_earth_meta_layer.md` (Earth Self + ascension + form library; preserved + reinforced)
- Disciplines #41 / #42 / #49 / #50 / #51 / #52 / #53 (substrate-led + framing-audit + critique-pair + pre-commitment; all preserved)

### 8.2 RETIRES (formerly load-bearing; now archived)
- `canonical/historical/19-llm-call-map.md` R8 inverted-mode reference (mechanism archived with season concept)
- `canonical/historical/30-engine-explainer-current.md` 4-canonical-element seasonal flavor substitution (mechanism archived)
- Per-season class generation pattern
- Cosmological vocabulary slot-fill mechanism
- Season manifest schema (preserved for historical seasons; not used for new kit-space generation)

### 8.3 Authorizes downstream (when implementation fires)
- Engine architectural amendment dispatch chain
- Engine page reframe dispatch
- Drax loadout app reframe dispatch
- Kit space schema definition (elrond + rocket + star-lord cross-seam)
- Parameter expansion event chronicle schema
- Per-skill flavor-or-canonical LLM judgment implementation (was WS1A.4-lite; now THE per-skill flavor mechanism)

### 8.4 Anticipates (future canonical)
- Economic-veteran problem resolution canonical (gates on materials/trading scope)
- Realm Expansion design discipline canonical (gates on first Realm Expansion content design)
- Ascension-as-strategic-choice player-surface canonical (gates on Earth Self UI/UX design)
- Underplayed-kit telemetry instrumentation canonical (gates on first kit-space-expansion telemetry data)

### 8.5 Does NOT replace or amend
- WS1A.Q18 Architecture A LOCK (preserved; vocabulary still locked)
- canonical-7+1 element catalog (preserved)
- BC axes substrate measurement (preserved)
- Substrate composition policy Option α/β/C (preserved)
- Pool.json v1.1 migration state (preserved)
- Earth meta-layer narrative framing at story-layer (preserved + reinforced as decoupled from content-release-schedule)

---

## 9. Discipline observations + recognitions

### 9.1 Substrate-led discipline at content-engagement layer (Disc #41 composition)

The "Realm Expansion targets underplayed kits" mechanism is Disc #41 substrate-led discipline applied at a NEW layer:
- Engineering generation generates kits (substrate-led at generation)
- Player engagement telemetry IS substrate at the content-engagement layer
- Realm Expansion content design CONSULTS this substrate (under-played-kit telemetry)
- Content design encoding gate composes WITH substrate vote (designer curates which kits to surface; doesn't override what telemetry shows is underplayed)

Worth jack-ryan Disc #N candidate ratification at next critique-pair window:

> **Substrate-led discipline at content-engagement layer:** when designing Realm Expansion content, consult kit engagement telemetry; design content that surfaces value of empirically-underplayed kit groupings; designer curates which underplayed kits to surface per design judgment but does NOT override empirical engagement signal. Composes with #41 substrate-led at generation layer.

### 9.2 Player-driven vs dev-driven design distinction

The Reincarnated commitment to player-driven over dev-driven (no forced seasons; ascension voluntary; player picks content engagement) is a meta-design distinction worth canonical recognition.

Worth jack-ryan Disc #N candidate ratification at next critique-pair window:

> **Player-driven over dev-driven design discipline:** when designing engagement mechanisms, prefer player-choice mechanisms over dev-imposed lifecycle mechanisms. Forced seasonal resets / forced character retirement / FOMO mechanics are dev-driven anti-patterns; player-strategic-choice equivalents (ascension as voluntary mechanism / kit space accessible at any time / content that surfaces value of underplayed options) preserve player agency.

### 9.3 Conscious genre-departure commitment

This canonical record establishes conscious genre-departure (ARPG seasonal convention → Reincarnated continuous-space + Realm Expansion). Future agents + future Matt understand this is deliberate.

---

## 10. Sign-off

**Architectural commitment:** Season concept ARCHIVED; Realm Expansion as content-release mechanism; continuous kit space; per-skill flavor-or-canonical naming; player-driven over dev-driven; ascension-as-strategic-choice; genre-departure deliberate.

**Authored:** gandalf 2026-06-02 per Pattern B substantive design session with Matt + Matt ratification ("Realm Expansion confirmed, path α, draft the canonical record")

**Authority:** Matt 2026-06-02 verbatim ratifications across the session:
- "season = archived. We have lost the concept of season with the introduction of the 'chernoff celestial body'"
- "we may periodically look to add additional kits by expanding the scope of the engine's parameters to generate further feature points within space"
- "future content will be a substrate engagement: New Maps, New Acts, New Game Modes. We can specifically tailor these to fit the under-played character kits"
- "Player driven is better than dev driven here I feel"
- "Realm Expansion confirmed, path α"
- "We can leave prior seasonal data as historical content"
- Economic-veteran question EXPLICITLY DEFERRED ("I would like to think further before deciding")

**Recognition-validate-commit discipline (Disc #41):** Architectural commitment LANDS NOW; downstream implementation (engine amendment + drax reframe + economic-veteran problem) GATES per empirical-evidence triggers in respective sections.

**Composition with prior canon:** preserves Q18 lock + Earth meta-layer + canonical-7+1 + BC axes + substrate composition policy; retires R8 + cosmological_vocabulary + per-season class generation; reframes drax + engine page.

**Next moves:**
1. Update `canonical/00-ground-state.md` § 1 to add this canonical entry + note season-concept archival
2. KR routes engine architectural amendment dispatch chain (substantial; ~10-20 sessions; rocket + star-lord)
3. Engine page + drax reframe queued post-engine-amendment-landing
4. MM-P1 substantive design session composes with kit-space-and-Realm-Expansion architecture as backdrop
5. Economic-veteran problem flagged as deferred-commitment; fires when materials/trading scope opens

**End of canonical record.**
