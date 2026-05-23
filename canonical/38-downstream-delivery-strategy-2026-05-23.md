# 38 — Downstream Delivery Strategy

> **STATUS:** CURRENT (load-bearing as of 2026-05-23) — see `canonical/00-ground-state.md`

**Status:** Active, captured 2026-05-23
**Author:** gandalf (story-and-design steward; senior designer)
**Authority:** Matt 2026-05-23 — D1-D10 confirmed in sequence during gandalf design session following Matt's external-counsel strategic-synthesis conversation 2026-05-22 evening
**Audience:** Knight-rider (orchestration), jack-ryan (process gate), specialist agents (rocket / gamora / star-lord / drax / elrond / galadriel / legolas), future Matt, future gandalf, eventual industry partners
**Companion docs:**
- `canonical/historical/29-design-overview.md` — strategic anchor (predecessor)
- `canonical/37-engine-and-game-two-products.md` — Variant C lock; engine-vs-game distinction
- `canonical/story/engine-as-general-serial-content-product-2026-05-22.md` — Variant C strategic lock (story-side)
- `canonical/story/gear-heavy-promotion-2026-05-22.md` — vast-library substrate architecture
- `canonical/story/hive-mind-protocol-weapon-library-import-2026-05-22.md` — substrate-acquisition protocol
- `canonical/story/style-register.md` — visual style register (used in D10 Path A filter)
- `agentic_orchestration/weapon-library-import-wind-down-summary-2026-05-22.md` — 89,839-row substrate state
- MEMORY entries: `project_earth_meta_layer.md`, `project_pet_system.md` — pre-existing continuity canon

---

## 0. TL;DR

Reincarnated commits to a **solo-dev-plus-agent-augmented** delivery model on **Unreal Engine** with **PC/console-first launch and mobile port at +6 months**. The game ships with **variable execution depth by build** (substrate-axis-driven, not pure auto-combat) on a **seasonal cadence** (~30-day seasons with weekly thematic beats). The **Earth Self / form library / spirit guide / persistent pet** continuity architecture (already canon, 2026-05-11) is the legacy mechanism — surfaced explicitly in player-facing copy.

**Genre framing is provisional.** The isekai positioning is held as a flagged decision-point (D10) gated at a two-stage substrate-evidence checkpoint. The engine's 89K-row substrate is already partially voting against pure-isekai framing; the final genre commitment waits on Phase-4 cluster evidence and first-playable-demo validation.

**Timeline floor:** ~200-220 effective dev-days under variable-execution + seasonal-cadence + humanoid-only-playable scoping, ~10-14 calendar months, contingent on **ship discipline + scope lock at MVP**.

---

## 1. Provenance

This doc captures the integration of two prior conversations into a single delivery-strategy canon:

1. **External strategic-counsel conversation (Matt, 2026-05-22 evening through 2026-05-23 morning).** Long-form synthesis covering engine choice (Unreal), pipeline savings math, agent-leverage multipliers, what the sim can/can't tune, weekly reincarnation design, mobile-first framing, auto-combat consideration, cadence design, and continuity question. The synthesis was structurally sound but reasoning from first-principles + commercial sense without knowledge of project canon.

2. **gandalf integration pass (2026-05-23 morning).** Brought the synthesis into contact with existing project canon (Variant C lock, weapon substrate state, Earth Meta-Layer canon, pet-system canon, style-register canon, hive-mind protocol). Several "open questions" from the external conversation resolved against existing commitments; several recommendations sharpened or amended; three new decision-points surfaced (D9 humanoid-only, D10 isekai-framing-checkpoint, asset-pipeline humanoid-skeleton constraint).

This doc is the **load-bearing capture** of that integration. It should be the first read for any agent or external party seeking to understand "what is Reincarnated shipping, on what timeline, with what design commitments."

---

## 2. The ten decisions

### D1 — Engine choice and platform sequencing

**Decision:** **Unreal Engine. PC/console-first launch. Mobile port at +6 months post-launch.**

**Reasoning:**
- **Meshy → Control Rig → Unreal** is a real pipeline integration that saves months of character-rigging work. Meshy 6 emits Control Rig specifically for Unreal compatibility. Unity equivalent requires significantly more glue code.
- **Niagara VFX** consumes JSON skill-data natively; data-driven workflow maps well to engine's ability-data emission.
- **PCG framework** is well-suited to consuming geo-spatial combat simulator data from the engine.
- **Lumen + Nanite** elevate AI-generated 3D content quality significantly, mitigating the "obviously AI generated" perception problem.
- **PC/console-first** matches the target audience (Matt is the audience — ARPG-depth-loving, ambivalent-about-pure-auto, deep-engagement preference). Mobile-first would require concessions in combat design, performance optimization, and engine choice (Unity would be marginally better for mobile-first) that don't serve the design.
- **Mobile port at +6 months** is real product work but achievable on Unreal with modular control architecture and scalable UI designed in from day one (see D8).

**Concerns logged for architectural mitigation:**
- TAA blur during fast combat — mitigated by TSR + motion-vector tuning + per-character motion-aware shader tweaks
- Iteration time / compile cycles — mitigate via Blueprint-heavy game-logic + C++-only-where-necessary architecture boundary
- Royalty structure — 5% of gross over $1M lifetime, budgeted as known cost

**Cross-reference:** Variant C lock (canonical 37) — engine-as-product remains commercially relevant on any deployment target; this decision is specific to Reincarnated-the-game.

---

### D2 — Execution model: variable execution by build

**Decision:** **Execution depth varies by build, driven by substrate axes. Movement (joystick) + potions + ultimate are universal across all builds. Everything above that varies by where the build's substrate-vector sits on range / rhythm / charge axes.**

**Reasoning:**
- Pure auto-combat was considered and rejected. Matt's stated ambivalence ("I'm always on the fence with auto battle") is diagnosis, not indecision — the target audience (Matt) does not want pure auto.
- Path of Exile precedent: summoner / totem / herald-stacker builds are auto-leaning; melee-combo / cast-on-crit / channeling builds are active. Both first-class. Players self-select.
- **Our substrate already produces this natively.** Range axis (close/medium/wide), rhythm axis (slow/medium/fast), and charge axis (continuous/charge-up/burst) implicitly produce builds across the execution-depth spectrum. Execution-variance is a substrate property, not a feature to add.
- Wide-range slow-rhythm builds are naturally set-and-forget. Close-range fast-rhythm charge-up builds are naturally active. Players choose engagement level by choosing form.

**Player-facing framing:** "Some forms fight themselves. Some forms ask everything of you. The choice is yours each season."

**Cross-reference:** substrate-vector axes per `canonical/story/multi-dim-convergence-algorithm-2026-05-21.md` and substrate-supplement docs; BDI ω/τ tables provide the substrate-vector arithmetic that drives execution-depth emergence.

---

### D3 — Cadence: seasonal arcs with weekly thematic beats

**Decision:** **One season ≈ 30 days. One reincarnated form per season. Within each season, weekly thematic beats (factions, dungeon variants, events, balance updates) produce four marketing/engagement moments per season.**

**Beat structure within a season:**
- **Week 1 — Reincarnation Week.** New form drops. Spirit-guide introduces context. Faction and starting-zone reveal.
- **Week 2 — Expansion Week.** New faction expansion or new dungeon variants thematically coherent with the form.
- **Week 3 — Challenge Week.** Mid-season event, special encounters, gear-set introduction, or boss encounter.
- **Week 4 — Conclusion Week.** Endgame challenges, build-pushing content, retrospective community moments, teaser for next season's form.

**Reasoning:**
- A week is too short for the depth our engine produces per form to be discovered by players.
- A month gives time for theory-crafting, build optimization, community-level meta-development, and emotional attachment to the form before reincarnation.
- Weekly sub-content prevents engagement decay through the month, creates four marketing moments per season, and matches industry-standard live-service patterns (Destiny 2, FF14, WoW, LoL).
- The cohesion-judge already operates at season-coherence granularity; weekly sub-content is thematically coherent with the seasonal form by construction.
- "Seasonal" is our existing project vocabulary — do not introduce "monthly" as a new term.

**Commercial implication:** the seasonal-with-weekly-beats pattern is what AAA live-service studios already operationalize. The engine's pitch becomes "slots into your existing operational model," not "requires you to adopt a non-standard content cadence." This is a stronger commercial story.

---

### D4 — Continuity architecture (already canon, restated for prominence)

**Decision:** **Reaffirm pre-existing canon. The Earth Self is the persistent player identity. The form library accumulates across seasons. The spirit guide carries memory across reincarnations. Pets persist across body-swap.**

**Architecture:**
- **Earth Self** — persistent player identity. NOT reincarnated. The soul that wears forms.
- **Form library** — every form ever worn becomes part of the player's accumulated gacha-style collection. Forms are not lost at season's end; they enter the library as mementos. Post-Phase-0 vision: re-enter play via rift events, PVE, PVP.
- **Spirit guide** — the player's future self speaking back across time. Carries memory across reincarnations because that's what the spirit guide is structurally.
- **Pets** — persistent companion across body-swap. The through-line that survives reincarnation.

**Reasoning:**
- This architecture was committed canonically 2026-05-11 (`project_earth_meta_layer.md` memory entry) and reinforced by the pet-system commitment (`project_pet_system.md`).
- The external-counsel conversation offered four options for "what happens at month-end" and gestured at "reincarnation as transformation" as the interesting one. This is what we've already chosen — a richer version of it than the conversation contemplated.
- The game's title — "This Season I Was Reincarnated as a…" — has the right grammar by accident: *I* (Earth Self, persistent) *was reincarnated as a* (form library entry, gacha-accumulated) *…* (this season's specific form).

**Pending action:** the architecture is canon, but **player-facing copy that surfaces this clearly does not yet exist.** Onboarding script, marketing positioning, and spirit-guide dialogue templates need to make the Earth-Self-persistent vs Form-rotates distinction visible to players. This is post-D6 design work.

---

### D5 — Timeline floor

**Decision:** **Approximately 200-220 effective dev-days under the current scope (variable-execution + seasonal-cadence + humanoid-only-playable). Approximately 10-14 calendar months under realistic solo-dev-plus-agent-augmented pace, contingent on ship discipline and scope lock at MVP.**

**Reasoning:**
- External-counsel synthesis arrived at 240 effective days for traditional ARPG scoping with agent augmentation; 196 days under pure-auto-combat scoping; 210-220 days under variable-execution scoping.
- Adjustments downward for humanoid-only constraint (D9) saving custom-rig + custom-animation work on non-humanoid playable forms: ~5-10 days.
- Adjustments upward for asset-pipeline integration work, ongoing engine maintenance during dev, scope-discipline checkpoints: ~10-15 days.
- Net: ~200-220 effective dev-days.

**Calendar conversion:** 1.5-2x ratio (productive-day to calendar-day) for solo-dev with agent augmentation. 200-220 effective days → ~10-14 calendar months.

**Variance:**
- **Faster (closer to 10 months)** requires: tight MVP scope, fast pipeline-integration validation in first 4-6 weeks, no surprise on Meshy / Control Rig / PCG / Niagara integration friction, sustained ship-discipline.
- **Slower (closer to 14 months or beyond)** if: scope creep at month 5-6 (the standard failure mode), pipeline-integration surprises, mobile-port work pulled forward, isekai-framing-checkpoint forces engine retightening (D10 Path A).

**Failure modes to actively guard against:**
- **Scope creep** — every individual feature feels affordable under agent leverage; aggregate scope explodes. Jack-ryan gates every milestone against the MVP lock.
- **The second-50% problem** — polish, integration, and feel-tuning take longer than mechanical implementation. Don't underestimate the back half.
- **Ship-discipline collapse** — the project that doesn't ship is worth less than the shipped imperfect project. Resist the temptation to expand scope for "future commercial use" if it delays the current ship.

---

### D6 — Canonical doc capture

**Decision:** **This doc (`canonical/38-downstream-delivery-strategy-2026-05-23.md`) is the canonical capture. It supersedes ad-hoc Matt-and-counsel conversations as the authoritative source for the delivery strategy.**

This doc is downstream of:
- Variant C lock (canonical 37 and `canonical/story/engine-as-general-serial-content-product-2026-05-22.md`)
- Vast-library substrate pivot (`canonical/story/gear-heavy-promotion-2026-05-22.md`)
- Hive-mind protocol (`canonical/story/hive-mind-protocol-weapon-library-import-2026-05-22.md`)

This doc is upstream of (pending future authorship):
- MVP scope lock document — the specific roster size, season count for launch, feature inclusion list, what-ships-vs-what-defers
- Player-facing copy for the Earth Self / form library / spirit guide / pet continuity (D4)
- Stage 1 cluster-checkpoint evaluation methodology (D10)

This doc is a key input to the forthcoming **`canonical/00-ground-state.md`** (epoch-cleanup oracle to be authored during the documentation-cleanup pass).

---

### D7 — AI-tell line: what we will not ship as raw AI output

**Decision:** **The following classes of content WILL NOT ship as raw AI output. Each requires either human-authored / human-curated / templated structure with narrow LLM blanks.**

| Category | Allowed | Not allowed |
|---|---|---|
| **Spirit-guide dialogue** | Templated structure with LLM filling narrow blanks (form name, faction reference, item descriptor) | Free LLM dialogue generation at runtime for major story or onboarding beats |
| **Voice acting** | Human-cast voice + scripted lines OR templated voice with LLM-filled narrow blanks | Full-LLM-generated voice monologues for named characters |
| **Marketing / store-page art** | Engine-rendered scenes + human polish + human-authored hero art | Raw AI-generated 2D promo art used unedited |
| **Trailer cuts** | Engine-rendered gameplay + human edit + scripted voiceover | Fully AI-generated trailer narration |
| **Audio (music + SFX)** | Human-composed or curated audio packs integrated into pipeline (already canon) | Raw AI-generated music shipped to player without composition pass |
| **Store-page copy** | Human-written marketing voice | Raw LLM-generated marketing copy |
| **Form / faction / lore output** | Engine-generated + cohesion-judge validated + spot-checked by Matt | Engine-generated unspot-checked at high cadence |

**Reasoning:**
- Players in 2026 are increasingly attuned to AI-tells. A single bad LLM response in onboarding can confuse a player into thinking a mechanic works differently than it does, or into thinking the game's writing is bad.
- The substrate-as-cohesion architecture (cohesion judge + substrate-vector validation) is the defense against the disjointed-mishmash "obvious AI" failure mode. **But cohesion alone does not address player trust at content surfaces.**
- This is a player-trust line. Once crossed, it's expensive to recover.

**Operational implication:** all generative-pipeline output passes through human-curation / spot-check / cohesion-judge before reaching player surfaces. Generation volume does not equal ship volume.

---

### D8 — Mobile-friendly design choices from day one

**Decision:** **Design UI, controls, and input architecture with mobile portability in mind from day one. Do NOT optimize for mobile constraints at the expense of PC/console experience.**

**Specific commitments:**
- **Modular control architecture** — input system abstracted so touch-input layer can be added without rewriting gameplay code
- **Scalable UI** — UI elements size correctly at mobile resolutions and tablet resolutions; no hard-coded pixel positions
- **Touch-mappable interactions** — combat actions, ability triggers, item interactions all designed as discrete events (not held / drag / multi-touch) that map cleanly to touch
- **Performance-aware art and VFX** — visual targets are PC/console-quality at launch but every system has a documented mobile-reduction path
- **Session-length flexibility** — content is enjoyable in 3-7 minute mobile sessions AND in 30-60 minute PC sessions; encounter pacing and save-resume behavior accommodate both

**What this does NOT include:**
- Mobile monetization design (deferred to mobile-port scoping)
- Mobile-specific UI elements that compromise PC UI quality (rejected)
- Cross-platform play infrastructure (deferred)

**Cost:** ~5-10 dev-days of architectural overhead distributed across UI and input system work. Significantly cheaper than retrofit-for-mobile-port if not designed in upfront.

---

### D9 — Playable forms are humanoid

**Decision:** **All playable forms (Earth Self's reincarnations) use humanoid skeletons. Non-humanoid presences live as setpiece bosses, pets/familiars, and background fauna. Slime/beast/non-humanoid form-suggestions are ultimate or transformation moments within humanoid base forms, executed via particle FX + IK constraints.**

**Reasoning:**
- **Asset pipeline constraint:** Meshy + Mixamo + Unreal Control Rig are humanoid-skeleton pipelines. Non-humanoid playable forms would require custom rigging, custom animation, and custom gear-attachment logic per non-humanoid topology — potentially 4-8 additional months of dev work.
- **Isekai genre canon supports humanoid-only:** Mushoku Tensei, Solo Leveling, KonoSuba, Re:Zero, Overlord, Tate no Yuusha — all humanoid protagonists and main casts. Even *That Time I Got Reincarnated as a Slime* — the title literally promises slime protagonist — keeps Rimuru in humanoid form 90%+ of screentime, and party members (Benimaru, Souei, Shion, Diablo) are all humanoid.
- **ARPG canon overwhelmingly supports humanoid-only:** Diablo I-IV, Path of Exile, Last Epoch, Grim Dawn, Lost Ark — zero non-humanoid playable rosters exist in commercially successful ARPGs. The constraint is the genre.
- **Gear/weapon substrate is humanoid-wielded:** the 89K weapon-substrate library was built for humanoid wielders. Forcing it onto non-humanoid topology burns substrate value.
- **Identity variance comes from substrate, not topology:** kitsune nine-tailed wind-sorcerer vs fallen-paladin oath-broken-knight feel as different as a slime and a dragon despite sharing a humanoid skeleton. Race / lineage / cultural register / element / mechanic / rhythm / VFX signature all produce identity differentiation within humanoid.

**Asset budget for non-humanoid presences (setpiece bosses, pets, fauna):**
- Setpiece bosses: ~10-20 over launch year, hand-commissioned or polished Sketchfab base, ~5-10 dev-days each
- Pets/familiars: ~30-50 over launch year, simple custom or compact humanoid skeleton, limited animation set, ~2-3 dev-days each
- Background fauna: low-budget, static or single-loop, in volume

**Slime concession (if desired):** humanoid base form + special ability or ultimate that transforms briefly into slime/beast form via particle replacement + IK constraints. Gear becomes embedded particles / glyphs during transformation. ~3-5 dev-days for the genre-fanservice nod.

---

### D10 — Isekai-framing checkpoint (provisional lock with substrate-evidence gate)

**Decision:** **Game-framing is currently isekai, PROVISIONAL. Engine is genre-agnostic per Variant C lock. The framing is held against engine-output evidence at two checkpoints. Three paths exist at the checkpoint; the choice is decided by what the substrate actually produces.**

#### Two-stage checkpoint

| Stage | Trigger | Evidence evaluated | Decision authority |
|---|---|---|---|
| **Stage 1 — Cluster Stage** | After Phase 4 (cluster semantic labeling) per hive-mind-protocol | Do the ~50-150 emergent clusters cohere within isekai aesthetic register, or do they sprawl across genres? Spirit-guide narrative output, form-library narrative output, weapon-substrate distribution by register | Matt + gandalf design call |
| **Stage 2 — Playable Stage** | First vertical-slice demo with engine-generated content | Does the produced content *feel* isekai when played, or does it feel like something else? | Matt + gandalf + jack-ryan |

#### Three paths at the checkpoint

- **Path A — Tighten the engine to isekai.** Add isekai-flavored substrate (anime/manga weapon set, Eastern mythology lineage tags, isekai trope library). Tighten cohesion-judge weighting to favor isekai-aesthetic clusters. Use existing style-register filter (canonical/story/style-register.md) as a consumption-time gate suppressing non-isekai substrate. **Cost: ~30-60 engine-days.** Preserves "isekai" as game's pitch.
- **Path B — Shift the framing copy only.** Engine output stays as-is; game's player-facing copy adjusts to a broader-than-isekai positioning while keeping the title. **Cost: ~10-15 days marketing/copy.** Cheapest. Risks pitch coherence.
- **Path C — Embrace what the engine wants to be.** If engine output is naturally cross-genre, lean into it. Framing examples:
  - **"Soul-traveler"** — each season is reincarnation into a different world (medieval-fantasy / cyber-mage / post-apocalyptic / anime-isekai cycling)
  - **"Multiversal reincarnation"** — explicitly trans-genre, Earth Self traverses universe-boundaries each season
  - **"Cross-genre roguelike-ARPG"** — closer to Hades or Risk of Rain framing

#### What the substrate is already partially voting

The 89,839-row weapon substrate (per `weapon-library-import-wind-down-summary-2026-05-22.md`) distributes as:

| Bucket | % of substrate | Register |
|---|---|---|
| Museums (Royal Armouries + Met Museum) | 50.9% | Western-historical-authentic + global-historical |
| Wikidata / Wikipedia | 23.3% | Cross-register general-fantasy + general-historical |
| TRPG community data (D&D, Pathfinder, OSR) | 9.3% | Western-fantasy |
| MMO/ARPG/Soulslike (D2, PoE, ER, DS) | 7.6% | Western-fantasy + Dark Souls-Eastern blend |
| Modern military | 4.5% | Modern-tactical |
| Tabletop fantasy (Warhammer AoS) | 2.4% | Western-grimdark |
| Modern/post-apoc (Cataclysm DDA) | 1.8% | Modern + post-apoc |
| Anime/manga sources | ~0% | (none catalogued) |

**The substrate skews overwhelmingly Western-historical + Western-fantasy + grimdark + modern.** Pure-isekai framing would require either Path A (tighten engine + add anime/manga substrate) or Path C (embrace cross-genre).

The Stage 1 checkpoint will reveal whether Phase-4 clusters confirm this skew or whether emergent clustering produces unexpected isekai-aesthetic coherence from the cross-register substrate. Hold final judgment until evidence lands.

#### Sequencing implication

**Do NOT author marketing positioning, title-locking copy, or genre-specific design docs (kitsune forms, oni race tags, anime-trope language) until after Stage 1 checkpoint clears.** The reincarnation core, Earth Self architecture, form library, spirit guide — all genre-agnostic, can be written now. Isekai-specific framing waits.

#### Why this discipline matters

This is the test of whether Variant C (engine-as-general-serial-content-product) is real. Variant A (engine-as-this-game-only) would let isekai constrain the engine. Variant C lets the engine reveal what content it naturally produces, and the game-framing adjusts to honor what was built.

Precedent: Hades was pitched as "Greek mythology roguelike." The engine wanted broader dialogue-driven narrative than the Greek frame allowed at the deep design level. Supergiant kept Greek aesthetically but expanded the design surface; Hades 2 broadened the framing explicitly (witchcraft, Slavic mythology). They followed the engine's voice. It worked.

The reverse — forcing a genre commitment onto a substrate that wanted something else — burns dev cycles fighting the engine, or ships a game where the genre feels forced.

---

## 3. What this doc does NOT decide

To avoid drift / scope expansion / future-agent confusion, the following are explicitly **out of scope** for this doc and live in separate canonical authorship:

- **MVP scope lock** — specific roster size, season count for launch, feature inclusion list. Authored as a separate canonical doc following Stage 1 cluster checkpoint.
- **Monetization model** — premium vs F2P vs hybrid, expansion pricing, mobile-port monetization. Deferred until Stage 2 playable validates the game.
- **Trial-boss-gallery roster** — which boss forms exist at launch. Lives in `canonical/story/`-side design work post-cluster-checkpoint.
- **Multiplayer / OOS clause refinement** — the pre-existing canon ("Reincarnated Phase 0 is solo + post-Phase-0 rift events PVP/PVE") stands; refinement is post-launch design.
- **Specific Unreal-side architecture** — Blueprint-vs-C++ boundary, plugin choices, asset-import-automation specifics. Owned by future engine-integration work after architecture-validation spike.
- **Provisional patent application** — IP step independent of dev-strategy decisions, sequenced by Matt's external counsel.

---

## 4. Immediate next actions (post-doc)

This doc serves the following downstream sequencing:

1. **Documentation-cleanup pass** (immediate, this session continuing). The documentation-velocity diagnosis from 2026-05-23 morning identified four-epoch-collision-in-flat-namespace as the root cause of agent slowdown. This doc is a key input to:
   - `canonical/00-ground-state.md` (oracle authored by gandalf during cleanup)
   - Epoch-stamping pass on `canonical/story/` (sub-agent coordination via knight-rider)
   - Onboarding-list shrink in agent definitions (working-agreement edit via jack-ryan)
2. **Skill packaging pass** (post-cleanup, pre-architecture-validation). Author canonical patterns as installable Claude skills using **Skill Creator**:
   - `reincarnated-engineering-disciplines` (19 disciplines)
   - `reincarnated-hive-mind-protocol` (per-cycle pattern)
   - `reincarnated-decision-log-format` (entry authoring protocol)
   - `reincarnated-canonical-doc-format` (epoch stamping + cross-reference)
   - `reincarnated-substrate-vector-cheatsheet` (BC axes, range/rhythm/charge taxonomy)

   Then use **Skill Seekers** to convert Unreal Engine / Niagara / PCG / Meshy / Control Rig documentation into installable skills *before* architecture-validation spike begins. Goal: shrink per-invocation onboarding cost for both internal-protocol knowledge and external-engine knowledge.
3. **Architecture-validation spike** (~1-2 weeks, post-cleanup + post-skill-packaging). Push a small slice of engine output through full pipeline (JSON → Meshy → Control Rig → Unreal import → playable form with one skill). De-risk Meshy / Control Rig / Niagara / PCG integrations before committing months. **Specific acceptance criteria include:**
   - 3.1 — JSON output from engine imports cleanly into Meshy and produces a usable 3D model
   - 3.2 — Meshy Control Rig export imports into Unreal with bones / skeleton intact and animatable
   - 3.3 — **Image-pass-through-to-Meshy validation** (per `canonical/story/asset-pipeline-meshy-swap-2026-05-22.md` § 3.6) — test substrate-image-pass-through path against ChatGPT-gen path on 3-5 weapons from the museum-tier substrate subset. Pass criterion: direct-pass-through produces equal-or-better Meshy output (mesh quality, rigging quality, Unreal-import compatibility). If pass, lock direct-pass-through as production default for ~91.5% of weapon assets (substrate-resident with quality-suitable image); ChatGPT-gen remains fallback for substrate coverage gap (~8.5%).
   - 3.4 — Niagara VFX consumes engine ability-spec JSON and produces visible in-engine effect
   - 3.5 — PCG framework consumes engine geo-spatial output and produces a navigable room layout
   - 3.6 — TAA/TSR fast-combat readability validated with rapid motion (per D1 concern)
4. **Stage 1 cluster checkpoint preparation.** Once hive-mind Phase 4 (cluster semantic labeling) completes, evaluate D10 evidence. Three-paths decision lands here.
5. **MVP scope lock** (post-Stage-1). Lock roster size, season count, feature list. Jack-ryan gates all subsequent work against this lock.

---

## 5. Cross-references

### Active project canon this doc depends on
- `canonical/historical/29-design-overview.md` — strategic anchor (predecessor)
- `canonical/37-engine-and-game-two-products.md` — Variant C lock
- `canonical/story/engine-as-general-serial-content-product-2026-05-22.md` — Variant C (story-side)
- `canonical/story/gear-heavy-promotion-2026-05-22.md` — vast-library architecture
- `canonical/story/hive-mind-protocol-weapon-library-import-2026-05-22.md` — substrate-acquisition
- `canonical/story/style-register.md` — visual style register
- `canonical/story/multi-dim-convergence-algorithm-2026-05-21.md` — substrate-vector axes
- MEMORY entries: `project_earth_meta_layer.md`, `project_pet_system.md`

### Live state references
- `agentic_orchestration/weapon-library-import-wind-down-summary-2026-05-22.md` — 89,839-row substrate
- `agentic_orchestration/weapon-library-import-hive-mind-state.md` — live hive-mind state

### Downstream artifacts this doc anchors
- `canonical/00-ground-state.md` (to be authored during cleanup pass)
- MVP scope lock doc (post-Stage-1)
- Stage 1 cluster-checkpoint evaluation methodology (post-Phase-4)
- Player-facing copy for continuity architecture (D4)

---

## 6. Sign-off

**Author:** gandalf (story-and-design steward; senior designer)
**Authority:** Matt 2026-05-23 — D1-D10 confirmed in sequence
**Status:** Active, load-bearing, top-of-stack for downstream-delivery decisions

**Co-attestation pending:** jack-ryan process-side review (Discipline #11 empirical inspection, Discipline #13b two-way attribution where applicable, cross-reference integrity, goalpost-shift-honesty where this doc supersedes prior framings).

**Next gandalf action:** author `canonical/00-ground-state.md` and coordinate epoch-stamping pass via knight-rider as the documentation-cleanup work continues.

---

**Signed:** gandalf (story-and-design steward; canonical lock for the downstream-delivery strategy of Reincarnated-the-game)
**For:** Matt's confirmation of D1-D10 ratifying the integration of external-counsel strategic synthesis with project canon as authoritative delivery strategy.
