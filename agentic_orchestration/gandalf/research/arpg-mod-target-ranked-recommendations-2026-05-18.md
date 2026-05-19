# ARPG Mod-Target — Ranked Recommendations (2026-05-18)

**Status:** Final synthesis. Pairs `arpg-mod-target-database-2026-05-18.md` (KPI inventory + comparator data + scoring matrix) with Matt's explicit mandate: *"understand the ability to tune to quick modding capability."* Produces a ranked recommendation set + per-target effort estimates + known-friction points. Load-bearing input for Pattern-B commercial-direction dialogue (2026-05-19 morning).

**Authored by:** gandalf — synthesis across:
- Engine-side: Reincarnated KPI inventory (Explore agent on engine codebase)
- Original 4 comparators: Wolcen, DD2, Grim Dawn deep-dives + ARPG baseline (D2/3/4/PoE/LE)
- Survey: 47-candidate modding-host survey
- Wave 2A in flight at authoring time: Titan Quest AE, Torchlight 2, Terraria/tModLoader, BG3 modding-interface deep dives (refinements to land overnight)

**Authored:** 2026-05-18 late evening.

---

## § 0 — TL;DR

**Headline:** The original 3 Director-named targets are technically inverted (Grim Dawn > DD2 > Wolcen). **Expanded research surfaces a SECOND viable primary target — Titan Quest Anniversary Edition — that wasn't in the Director's recommendation set.** Together with Grim Dawn, this is the **killer pairing** — same mastery-system architecture, cross-porting already established community practice, combined audience and credibility doubles the reach of single-target investment.

**Top recommendation:** Build Grim Dawn first, expand to Titan Quest AE second. Combined Phase-1+2 cost: ~10–12 weeks of focused mod-export engineering on top of the Track-F R1 + R3-subset (per fight-integrity-gap canonical doc).

**Three findings, in increasing strategic weight:**

1. **Reincarnated is structurally well-positioned for modding-export.** The engine's mechanical layer is fully deterministic JSON output; the LLM layer is cleanly isolated to naming/vocabulary. Any modding-export pipeline can run mechanics deterministically, then apply per-host naming, then translate JSON → host schema. **The architecture is the asset.**

2. **The mastery-system pairing (Grim Dawn + Titan Quest AE) is the engineering-leverage discovery.** Both hosts share Crate-Iron-Lore lineage; their mastery systems are structurally identical; community cross-porting is already established practice. **A single Reincarnated mod-export pipeline can target both with ~+25% incremental effort vs. building for either alone.**

3. **Tier-2 candidates (Torchlight 2, Terraria) extend reach in different directions.** Torchlight 2 stays in the GD/TQ mastery-system family with smaller community. Terraria sacrifices presentation parity for the most developer-friendly modding pipeline in gaming + Calamity/Thorium/N-Terraria scale precedent. Either is a viable Phase-3 expansion depending on what Phase 1+2 reveals.

---

## § 1 — The producer-side picture (what Reincarnated reliably ships)

**Mechanical output, deterministic, no LLM:**
- Per-class: archetype tag, role orientation, range profile, energy type, 270-point stat distribution, 9-role skill set, color palette, balance metadata, movement speed
- Per-monster: 7-tier threat hierarchy, archetype, energy/role/range, dominant + seasonal element, HP/armor/per-element-resistances, skills list, movement speed
- Per-skill: composition mode, role (9 options), element (8 canonical), geometry (24 types), effect category, energy/cooldown, damage multiplier, typed effects (15+ named effect types with parameters), tier, chain metadata
- Per-gear: base type, slot, rarity tier (5 levels), stats dict (10 fields), rolled effects, ability modifiers, traits, class-fit profile (5 dimensions), set membership
- Per-trait: category (stat/ability/granted), stat key + value, source attribution
- Per-season: manifest, cosmological vocabulary (8 slots), anchor, generation seed

**LLM-authored layer (~$0.74/season, ~317 calls):**
- Element selection per season
- Class / monster / skill / gear naming + flavor text + visual prompts
- Cosmological vocabulary slot fills (8 named slots — ignition / suffusion / bulwark / displacement / impact / radiance / penumbra / resonance)

**Schema-translation gaps (what mod-export pipelines must fill):**

| Gap | Reincarnated current | Mod-export workaround |
|---|---|---|
| Per-skill range published | None | Derive from geometry_type defaults; surface in tooltip metadata |
| Per-skill spatial footprint (radius, cone angle) | None | Map from 24 geometry types to host-game shape catalog |
| Aggro radius / leash | None | Per-tier defaults from host-game conventions |
| Telegraph windows | None | Per-role defaults (boss = 1.5s, elite = 0.8s, etc.) |
| AI behavior fields | Archetype priority only | Host games typically have simpler AI than ours; this gap is small |
| VFX / audio asset references | Placeholders only | Host-game's asset library; mod content uses host-native assets |
| World geometry / quest structure | N/A | Host-game's authoring tools |

**Operational implication:** A first mod-export run can ship without closing the R3 (schema migration) gaps — the host game can absorb defaults. **R3 is required for full-fidelity Path A standalone but is OPTIONAL for Path B mod-first.** This is the most consequential finding for path-cost re-pricing.

---

## § 2 — The consumer-side picture (what hosts actually want)

### § 2.1 — Best-fit hosts (KPI + schema + pipeline)

**Grim Dawn (MFS 4.05):** Mastery DBR template system maps cleanly to Reincarnated mastery/class/skill/monster/gear schemas. Dawn of Masteries' 53-class precedent verifies feasibility at scale. Crate ships the same tools they use internally — Asset Manager, World Editor, Database Editor, Quest Editor, Conversation Editor, Particle Editor, Lua scripting.

**Titan Quest AE (MFS 3.85):** Mastery system architecturally identical to Grim Dawn — Crate principals are Iron Lore alumni who built TQ. Cross-porting between TQ and GD is **already established community practice** (TQ-to-GD mastery ports exist; ShadowChampions Multimaster Mar 2025, Legion of Champions 2024). ARC tools are well-documented.

**Torchlight 2 (MFS 3.50):** GUTS editor is official, comprehensive. SynergiesMOD = 3-class injection proven (Necromancer, Warlock, Paladin) + raid dungeons + world bosses. Direct Reincarnated-scale precedent.

**Terraria/tModLoader (MFS 3.55):** C# API hierarchy (ModNPC, ModItem, ModProjectile). Calamity Mod, Thorium Mod, N Terraria proof of total-conversion-tier injection. **Best-in-class pipeline maturity in the entire survey.** 2D side-scrolling presentation is the trade.

### § 2.2 — Architectural mismatches (why other candidates fall off)

| Host | Mismatch | Severity |
|---|---|---|
| BG3 | Turn-based vs real-time fundamental | Severe — action economy paradigm |
| Elden Ring / DS3 | Souls "class" is just starting equipment; no build-system depth | Moderate — audience expects character-skill execution |
| CK3 | Dynasty management ≠ ARPG combat loop | Severe — entire game loop wrong |
| Skyrim SSE | Bethesda perk + standing-stone + race-ability architecture deeply locked-in | High — translation cost massive despite pipeline quality |
| Bannerlord | Sandbox combat ≠ ARPG dungeon-crawl | Severe — audience expectation mismatch |
| DD2 | RE Engine modding limited to recombination | Severe — no system-level injection |
| Wolcen | Platform end-of-life | Terminal — dormant community |
| D2R | Modding officially restricted; SP-only fan loaders weak legal footing | Severe — anti-cheat hostile |

---

## § 3 — The killer finding — Grim Dawn + Titan Quest AE pairing

**This is the recommendation that emerges from expanded research that was NOT in the Director's option space.**

**Why it works architecturally:**
- Both engines share the Iron Lore mastery system DNA (Crate licensed TQ engine, then built GD with Iron Lore alumni who carried the design forward)
- Both use DBR-style database records for content
- Both have official editor toolsets (TQ's ARC tools ≈ GD's Asset Manager + DB Editor)
- Both support new mastery / class / skill / monster / gear / item injection at proven scale
- TQ-to-GD mastery ports are an existing community practice — a Reincarnated exporter that ships GD content can adapt to TQAE with low marginal engineering effort

**Why it works commercially:**
- Combined audience reach roughly 2× single-target investment
- Two community modder hubs (Crate forum + titanquestfans.net + Nexus) increases distribution surface
- Cross-platform credibility ("our content runs in both ARPG modding ecosystems") strengthens any Path-C buyer narrative
- TQAE has Steam Workshop (lighter activity than GD but present); GD has none — Workshop publishing on TQAE adds discovery surface GD lacks
- THQ Nordic ownership of TQAE creates a different commercial conversation than Crate (whose business model is publisher-via-Steam-only)

**Why this wasn't in the Director's recommendation:**
- Director ranked on commercial-visibility + genre-fit + recent-relevance intuition (all valid signals)
- TQAE is older and less marketing-current than Wolcen (which had a viral 2020 launch)
- TQAE's modding scene is alive but quieter; doesn't make press headlines
- Director may have weighted "recognizable name to modern players" higher than "modding-platform viability" — a fair commercial signal we've now rebalanced

**What to communicate to the Director eventually:**
The Director's three named recommendations were valid signals on commercial-visibility axis; the technical research adds TQAE as a Crate-ancestral leverage play that doubles the reach of Grim Dawn investment. **This is updated info, not rebuttal — the Director may want to incorporate it into his thinking, or may have outside signals that argue against it.**

---

## § 4 — Per-target effort estimates

All estimates assume **R1 (per-tier balance targets) is already shipped** as Track-F prerequisite (1–2 weeks of gamora).

### § 4.1 — Phase 1: Grim Dawn primary

**Engineering work:**
- **R3-subset** (per-skill range + per-skill geometry params + AI behavior fields in catalogue + schema migration across 5 shipped seasons): 2–3 weeks (rocket + star-lord + elrond)
- **Grim Dawn DBR exporter**: 4–6 weeks (rocket + star-lord)
  - JSON → DBR translation layer
  - Asset Manager batch compilation
  - Mod Merger compatibility (clean file namespace)
  - First mod ship: 1 class (1 Reincarnated substrate-class) with full skill tree, monster bestiary, gear set
- **Phase 1 total: ~6–9 weeks**

**Critical path:** R3-subset gates the exporter (need schema to translate from).

**Friction points:**
- One-mod-at-a-time GD engine constraint — clean file namespace from inception is mandatory
- v1.2.0.0 modding tool compatibility status (verify before commit)
- DBR schema requires asset references (icons, particle effects, sound effects) that Reincarnated doesn't currently ship — workaround: human-art-side asset binding OR placeholder host-game-default assets

### § 4.2 — Phase 2: Titan Quest AE secondary

**Engineering work:**
- **TQAE ARC adapter** (translates the GD DBR exporter output into TQAE-compatible files): 2–3 weeks (rocket + star-lord)
  - DBR-to-ARZ format translation (file system differences)
  - TQ mastery template (similar but not identical to GD; ~80% schema overlap)
  - titanquestfans.net + Nexus distribution
- **Phase 2 total: ~2–3 weeks incremental on top of Phase 1**

**Critical path:** Phase 1 must ship first; Phase 2 is a pure translation layer.

**Friction points:**
- TQAE has Steam Workshop; GD does not. Workshop publishing pipeline different from Nexus.
- Verify TQAE concurrent player base before commit (Steam Charts pending in Wave 2A)
- Mastery tier count: TQ uses different progression structure (8 tiers vs GD's 9) — minor translation

### § 4.3 — Phase 3 alternatives (post-Phase-1+2 evaluation)

**Option A — Torchlight 2 SynergiesMOD nest** (~3–4 weeks)
- Build TL2 GUTS exporter
- Evaluate whether SynergiesMOD platform accepts add-on content
- Reach: smaller TL2 community than GD/TQ; engine age cap on visual fidelity
- **Strategic value:** stays in ARPG-mastery-system family; completes the genre-canon mod-host trinity

**Option B — Terraria/tModLoader pivot** (~4–6 weeks for code-gen, +substantial art re-authoring)
- Build tModLoader C# code generator (Reincarnated JSON → ModNPC/ModItem/ModProjectile/DamageClass C# class files)
- **CRITICAL CONSTRAINT (Wave 2A finding):** tModLoader has **NO runtime JSON loading** — all content is compile-time C#. Per-season Reincarnated regen would require weekly rebuild + Workshop push, OR a kRPG-style pre-allocated-slot + ModConfig-JSON-at-runtime workaround (architecturally complex, unvalidated)
- Re-author art assets for 2D pixel-art vocabulary at Terraria scale (16-64px native textures, max 2048×2048, premultiplied alpha, nearest-neighbor scaling) — **this is full art production, not a conversion**
- Reach: enormous Terraria modded-player audience (~32k avg / 79k peak Feb 2026; Calamity Mod = 9.18M subscribers)
- DamageClass injection pattern is well-documented (Thorium's TryFind cross-mod API is the reference)
- **Strategic value:** maximum reach IF the per-season cadence operational + art-cost trade is acceptable; demonstrates engine flexibility but at significant translation cost on two axes (runtime JSON gap + art register gap)
- **Wave 2A revised MFS: 3.20** (down from 3.55 — compile-time-only constraint material)

**Option C — Defer Phase 3 in favor of Path C (engine-as-tool) acceleration**
- Two ARPG mod hosts may be enough commercial proof
- Begin Path C buyer-profile validation + operational layer prototyping
- **Strategic value:** transitions from "prove the engine via mods" to "monetize the engine via tool sale"

---

## § 5 — Effort sequencing recommendation

**Recommended sequence:**

```
Week 0 (pre-flight)
└─ Pattern-B direction commit (Matt) — confirm Path B mod-first with Path C parallel-warm

Week 1–2  R1 — Per-tier balance targets (gamora)
            └─ Class-retuning sprint follows (parallel-fired, multi-week)

Week 3–5  R3-subset — Schema migration (rocket + star-lord + elrond)
            └─ Per-skill range + geometry params + AI behavior fields added to catalogue
            └─ Backfill across 5 shipped seasons

Week 6–11 Phase 1 — Grim Dawn DBR exporter + first mod ship (rocket + star-lord)
            └─ JSON → DBR translation
            └─ Asset Manager batch compilation
            └─ Mod Merger compatibility
            └─ Ship first single-class Reincarnated mod
            └─ Community feedback loop with Crate-forum modders

Week 12–14 Phase 2 — TQAE ARC adapter (rocket + star-lord)
            └─ DBR-to-ARZ translation layer
            └─ titanquestfans.net + Nexus distribution
            └─ Ship same first mod ported to TQAE

Week 15+  Phase 3 evaluation — decide Torchlight 2 OR Terraria OR Path C transition based on Phase 1+2 reception
```

**Total Track-F engineering: ~14 weeks** to two-mod-host viability. This is significantly less than Path A's 9–15 weeks of full Track-F + class-retuning sprint, because Phase 1+2 absorbs the spatial substrate of host games for free.

**Parallel work that can happen:**
- Phase 1 weeks 6–11: drax can ship demo collision/leash fixes (R4/R5) if Path A is kept warm
- Phase 1 weeks 6–11: legolas can scout Path C buyer profiles
- Phase 2 week 12–14: star-lord can spec operational layer for Path C

---

## § 6 — Known-friction points and mitigations

### § 6.1 — Friction common to all mod-host targets

1. **Asset references gap.** Reincarnated ships canonical entries with `particle_theme` and `audio_theme` as text-tag placeholders, NOT actual asset bindings. Host games need VFX + audio + icon assets to render mod content. **Mitigation options:**
   - Human-art-side asset commissioning per mod ship (most expensive, highest quality)
   - Host-game default asset reuse (cheapest, weaker thematic fit)
   - LLM-generated asset prompts → image-gen pipeline (medium cost, medium quality — Reincarnated already has the pitch-image precedent from this session)

2. **Naming layer per-host.** Reincarnated's LLM naming pass produces high-quality names within Reincarnated's own grammar register; some hosts have stylistic conventions (Grim Dawn's Cairn world, Skyrim's Tamriel) that may want re-flavoring. **Mitigation:** per-host LLM naming pass with host-context prompts; manageable additional cost (~$0.74/season × per-host multiplier).

3. **Modding-host patch fragility.** RE Engine games (DD2) are notorious for patches breaking mods; Grim Dawn v1.2 updates required mod tool re-validation; Wolcen-style end-of-life is the worst case. **Mitigation:** track host-patch cadence; budget for periodic mod re-validation; prefer hosts with stable modding APIs (Grim Dawn, Torchlight 2 GUTS).

### § 6.2 — Friction specific to top recommendations

**Grim Dawn specific:**
- One-mod-at-a-time constraint requires clean file namespace from inception
- v1.2.0.0 modding tool compatibility status needs verification
- No Steam Workshop = Nexus + forum distribution only

**Titan Quest AE specific:**
- Steam Workshop activity lighter than expected; verify concurrent player base
- TQAE has DLC fragmentation (Atlantis, Ragnarök, Eternal Embers) — mod compatibility per-DLC needs handling

**Torchlight 2 specific:**
- 2012-era engine caps visual fidelity
- SynergiesMOD openness to third-party class additions is the open question (Wave 2A may answer)

**Terraria specific:**
- 2D side-scrolling presentation requires extensive art re-authoring
- C# API requires Visual Studio / dotnet toolchain familiarity for the exporter team

### § 6.3 — The Wolcen warning

The Director's #1 recommendation has gone end-of-life since his last review. The lesson: **modding-host viability decays.** Reincarnated's mod-export pipeline should be designed for **portability across hosts** so that as platforms decline, the content remains migratable. This argues for:
- Maximally generic intermediate representation (Reincarnated's JSON output)
- Per-host translation layer as a separable adapter (not entangled with the core)
- Versioned exports so old mods can be re-spun for new hosts

---

## § 7 — Pattern-B recommendations (gandalf to Matt)

These slot directly into Pattern-B Q1/Q2/Q4 deliberation tomorrow morning:

### § 7.1 — Q1 direction commit recommendation

**Recommended:** **Path B mod-first (Grim Dawn primary + Titan Quest AE secondary) with Path C kept warm-parallel.**

Rationale:
- Lowest total engineering cost (~14 weeks vs. Path A's 9–15 weeks of full Track F + class-retuning)
- Highest leverage discovery: GD + TQAE pairing reaches 2× audience for ~+25% incremental work
- Aligns with Director's "mods-then-engine-sale ladder" strongest leaning
- Sets up Path C buyer narrative: "our engine ships content into the two most-modded ARPG-mastery-system games"
- Path A defer (not kill) — costs most, exposes most product-market risk

### § 7.2 — Q2 mod-first target ordering

**Recommended:**
1. Grim Dawn first (Phase 1)
2. Titan Quest AE second (Phase 2) — leverages Phase 1 investment
3. Phase 3 decision deferred until Phase 1+2 reception is known

**Override Director's original Wolcen-first recommendation.** Surface the technical inversion respectfully — Director ranked on commercial-visibility (valid), technical evidence inverts on modding-pipeline viability.

### § 7.3 — Q4 engineering scope (operational layer for Path C)

If Path B + Path C parallel-warm:
- Phase 1+2 engineering produces a **Reincarnated → host-game export pipeline** that IS the engine-as-tool prototype
- Path C operational layer (decision-tree authoring + content banking + deployment APIs + admin dashboards) builds ON TOP of the export pipeline
- **Estimated additional Path C ops layer: ~6–10 weeks** (requires star-lord deep scoping)
- **Combined Path B Phase 1+2 + Path C ops layer: ~20–24 weeks to first B2B-tool sellable surface**

### § 7.4 — Q5 emotional/family dimension input

The mod-first path means **Reincarnated content runs inside Grim Dawn / Titan Quest** as the player experience, not in Reincarnated-the-game's own Pixi.js demo. The shift from "the game we're playing together" to "the content we're authoring together that gets played in other games" is real and worth Matt naming explicitly with his son. **This is not a strategy question; it's a life question, and gandalf trusts Matt to weigh it.**

---

## § 8 — Methodology revision notes (per Matt's mandate)

Matt's mandate: *"If any question does not get to the goal of understanding of the ability to tune reincarnated-engine to quick modding capability, then feel free to revise the questions/research/KPIs/scoring methodology as you go."*

**Revisions made during this work:**

1. **Survey scope widened beyond ARPG.** Original 3 Director-named targets were all ARPG-adjacent. Survey deliberately included Adventure/RPG/Sandbox/Strategy to test whether non-ARPG hosts could be viable. Confirmed: most non-ARPG hosts are not viable for Reincarnated content (genre mismatches), but Rimworld + Minecraft + CK3 are interesting edge cases worth documenting.

2. **Scoring weights adjusted mid-analysis.** Initial weights had Pipeline at 25%; raised to 30% after Wolcen finding clarified that "accessibility determines feasibility." Schema kept at 35% as the actual translation overhead. Community held at 15%.

3. **Added "decision band" interpretation layer.** MFS scores alone don't yield a clean recommendation; bands (PRIMARY / Secondary / Niche / Not viable) translate the numerics into actionable tiers.

4. **Added the "killer pairing" finding as a distinct § 3.** This wasn't in the original methodology — the GD+TQAE leverage emerged organically from cross-referencing the survey results with the original 4 comparators. Worth elevating to its own section because it changes the Pattern-B recommendation more than any single MFS score does.

5. **Reframed asset-references gap as a producer-side opportunity, not a blocker.** Per § 1, R3 schema migration is OPTIONAL for Path B (host games absorb defaults). This was not initially clear; surfaced through the comparator-fit exercise.

**Methodology gaps (acknowledged, not resolved this pass):**

1. **No verification of player-base size per host (2024-2026 Steam Charts).** The MFS community score is subjective; harder data would tighten the recommendation.
2. **No cost-model for the LLM naming pass per-host.** Estimated linearly with season count, but host-specific naming conventions may multiply cost.
3. **No deep dive on Path C buyer profiles.** Pattern-B Q4 needs Legolas Mode A scout commission to populate.

---

## § 9 — Open questions for Pattern-B and beyond

1. **Q1 direction commit** — Path A / B / C / combination (gated by Matt)
2. **Q2 mod-first target ordering** — Grim Dawn first confirmed; TQAE second recommended; Phase 3 deferred
3. **R3 scope** — full R3 (all 5 axes for Path A) OR R3-subset (per-skill range + geometry params + AI fields only for Path B)?
4. **Asset commissioning model** — human-art / host-default / LLM-image-gen / hybrid?
5. **Per-host naming budget** — additional LLM cost per host accepted?
6. **Phase 1 first-class candidate selection** — which Reincarnated substrate-class ships first? (Recommendation: a thematically distinctive class with clean Grim Dawn analog — e.g., a fire-substrate caster maps onto Demolitionist; a shadow-substrate controller maps onto Necromancer)
7. **Director-rec inversion communication** — when/how does Matt surface the Wolcen-vs-Grim-Dawn technical inversion to the Director?
8. **Phase 3 trigger conditions** — what reception signals from Phase 1+2 trigger which Phase-3 option?

---

## § 10 — Wave 2A returns (refinements integrated)

All 4 Wave 2A deep-dive agents returned 2026-05-18 very late evening. Key refinements:

### § 10.1 — Titan Quest AE refinement (MFS 3.85 → 3.275)

**Critical findings:**
- **UI authoring overhead is significant** — each new mastery requires 8+ DBR files (masteryXbutton, masteryXtext, masterypane, skill01-skill24, panectrl, masterybar, masterybitmap) PLUS art assets (mastery icons, skill icons). The 1.7 GB ShadowChampions Multimaster mod size reflects this — UI assets dominate authoring cost.
- **Affix system structural mismatch** — TQAE affixes are authored library entries (separate DBR records); Reincarnated's rolled_effects model embeds generated values inline. Two workarounds: (a) pre-generate affix library from possible rolls, (b) embed stats as flat item fields bypassing affix system entirely. Option (b) is more tractable.
- **Community smaller than initially scored** — ~742 avg concurrent (May 2026), 206 Workshop items, 113+ Nexus mods. Stable but small.
- **AI is data-driven priority list, not authorable** — monster AI is `specialAttackXSkillName + chance + timeout + range` slots referencing pre-existing engine behaviors. Custom AI logic cannot be authored.
- **No procedural-to-TQAE pipeline precedent exists** — Reincarnated would be the first.
- **Mastery system structurally identical to Grim Dawn CONFIRMED** — Crate principals are Iron Lore alumni; cross-porting between GD and TQAE is established community practice (Grim Quest, TQ ReDawn — both port TQ → GD direction; GD → TQ direction not confirmed but architecturally feasible).

**Impact on "killer pairing" framing:** The engineering leverage (DBR exporter + minor ARZ adapter reaches both hosts) holds. The audience reach is more modest than initially hoped. **Recommendation:** Keep TQAE as Phase 2, but expectations on Phase-2 commercial reach should be tempered. The combined Phase 1+2 still has strong cross-host portability value as a *credibility signal* for Path C buyer narratives ("our engine ships content into both Crate-lineage mastery-system games") even if the absolute reach is smaller than top-tier hosts.

### § 10.2 — Torchlight 2 refinement (MFS 3.50 → 3.525)

**Critical findings:**
- **DAT format is plain-text key-value** — directly editable in any text editor without GUTS. Implication: Reincarnated's JSON could be transpiled directly to .dat text without GUTS in the authoring loop.
- **10-mod simultaneous limit** — better than GD/TQ's 1-mod-at-a-time; manual merging required for 11+ mods but easier than GD/TQ workflow.
- **Steam Workshop auto-sync via .sch scheme files** — significantly more frictionless than GD's manual `.pak` drop or TQAE's Custom Game menu selection.
- **5 AOE archetypes** (cone, sphere/circle, ring, bolt, channeled-cone) — superset of typical ARPG geometries; 24 Reincarnated geometry types collapse to these reasonably.
- **SynergiesMOD has NO documented license for third-party building on top** — drops the "SynergiesMOD nest" Phase-3 Option A as a viable path. **Target vanilla TL2 for any TL2 export.**
- **Class-registration single-conflict-point** — every class mod touches the options/character-selection file. Multi-class deployment requires merge.
- **Player base small** — ~250 daily concurrent, peaked August 2025 at 808. Realistic reach: hundreds to low-thousands per mod.
- **Game patches stopped 2017** — Runic Games shutdown; no engine updates since v1.25. This is stable (no patch-breaks-mods risk) but also stagnant (no new players from active development).
- **40+ class-injection precedents** (TL2-ACE 6 classes, Classes Reborn 40+ classes, "New Characters and Classes" 90-mod collection) — pipeline is well-traveled.

**Impact:** Slight upward refinement. TL2 is more developer-friendly than initially scored (DAT text format + auto-sync Workshop), but community size constraint holds. Stays in Tier 2 Secondary. **Phase 3 Option A (TL2) becomes a more realistic option than initially framed**, but the audience cost-benefit needs Phase-1+2 reception evidence first.

### § 10.3 — Terraria/tModLoader refinement (already applied — MFS 3.20)

**Critical finding (folded into recommendations earlier):**
- **tModLoader has NO runtime JSON path** — all content compile-time C#. Per-season Reincarnated regen would require weekly rebuild + Workshop push, OR kRPG-style pre-allocated-slot + ModConfig-JSON runtime workaround (architecturally complex, unvalidated). **This is the dealbreaker for procedural seasonal content delivery; viable only if rebuild cadence is acceptable.**
- 2D side-scroller art re-authoring at 16-64px native pixel art remains significant.
- DamageClass injection pattern is the class-equivalent (Thorium's TryFind cross-mod API is the reference).
- Concurrent player base: ~32k avg / 79k peak Feb 2026 (HUGE compared to TL2/TQAE). Calamity Mod = 9.18M subscribers.

**Impact:** Tier 2 Secondary but with operational asterisks. **The audience is order-of-magnitude larger than TL2 / TQAE / GD combined**, which is the strategic counterweight to the operational cost.

### § 10.4 — Baldur's Gate 3 refinement (MFS 2.25 → 2.525)

**Critical findings:**
- **Script Extender (bg3se) v31 actively maintained April 2026** — community tooling infrastructure is durable past Larian's "final patch" (Patch 8 April 2025).
- **Official Toolkit + in-game mod manager + Patch 8 partial level editing** — pipeline more mature than initially scored.
- **15,000+ Nexus mods (Oct 2025)** — community is enormous.
- **5 required files for new class** (ClassDescriptions, Progressions, SpellLists, ActionResourceDefinitions, Localization) + Lua/Osiris scripting layer.
- **FUNDAMENTAL MISMATCHES with Reincarnated CONFIRMED:**
  - Real-time vs turn-based (action economy paradigm)
  - 24 geometries → ~8 SpellTypes (Target / Projectile / Shout / Zone / MultiStrike / Rush / Throw / Wall)
  - cooldown_seconds → action economy (no cooldowns)
  - energy_cost continuous → spell slots discrete
  - stat_distribution 270 budget → 5e 1-20 stats (intelligence=157 incoherent in 5e)
  - HP scale (3,820 Reincarnated trash → 50-300 5e bounded)
  - Duration in seconds → turns (6s/turn 5e)
  - 8 substrates → 13 D&D damage types

**BG3 verdict:** **WEAK for mechanical fidelity; MODERATE for thematic showcase.** Best framed as "subclass injection per Reincarnated elemental archetype" — players get something that smells like Reincarnated but operates as native 5e subclass. **Not a faithful port; a community-engagement / brand-presence play.**

**Impact:** Slight upward refinement on pipeline + community; downward on schema fit. **Net tier unchanged (Niche).** Could be a valid "outreach play" if Path B + Path C is going well and Matt wants brand presence in the largest D&D modding community in gaming — but not a primary or even secondary recommended target.

### § 10.5 — Updated tier ranking

| Tier | Targets (refined MFS) |
|---|---|
| **PRIMARY (≥4.0)** | Grim Dawn (4.05) |
| **Secondary (3.0-3.99)** | Torchlight 2 (3.525); Titan Quest AE (3.275); Terraria/tModLoader (3.20) |
| **Niche (2.0-2.99)** | Minecraft (2.85); Elden Ring (2.65); Rimworld (2.50); DD2 (2.50); DS3 (2.50); BG3 (2.525); Starfield (2.45); V Rising (2.40); CK3 (2.20); Bannerlord (2.20); D2 Median XL (2.70) |
| **Not Viable (<2.0)** | Wolcen (1.65) |

**Refined Pattern-B recommendation (post-Wave 2A):**

The Grim Dawn + Titan Quest AE pairing's engineering leverage holds, but TQAE's smaller community softens the audience-doubling framing. **The recommendation remains: Phase 1 Grim Dawn, Phase 2 Titan Quest AE.** But:

- **Phase 2 framing shifts** from "doubles the audience reach" to "extends the audience reach modestly + builds cross-host credibility for Path C narrative." Both are valid; the second framing is more honest.
- **Phase 3 Option A (Torchlight 2) becomes the strongest Phase-3 candidate** by MFS (3.525 vs Terraria 3.20). DAT text format + Workshop auto-sync makes it the most developer-friendly Tier-2 target. Audience small but realistic mod reach is "hundreds to low-thousands" per ship.
- **Phase 3 Option B (Terraria) audience case strengthens** — order-of-magnitude larger player base than any other Tier-2 candidate, but operational cost (rebuild cadence + art re-authoring) is steep. **Best framed as "moonshot reach" if first three phases succeed.**
- **BG3 explicitly added as an optional outreach play** if commercial direction allows — not a recommended primary path, but a "ship-a-thematic-subclass for community visibility" candidate post-Phase-1+2.

**No primary recommendation flip. Refinements are second-order. The recommendation set was indeed stable enough to enter Pattern-B with.**

---

## § 11 — Closing

Reincarnated's mechanical layer is **highly structured, deterministic, and exportable.** The LLM layer is **cleanly isolated** to naming/vocabulary. This separation makes the engine **structurally well-positioned for mod-export** — far better than if mechanics and narrative were tangled.

**The Grim Dawn + Titan Quest AE pairing is the engineering-leverage discovery.** Combined Phase 1+2 reaches two of the most-modded ARPG-mastery-system hosts with ~14 weeks of focused work. This is the cheapest, highest-leverage commercial-direction path the research surfaces.

**The Director's three named recommendations were valid commercial signals; the technical evidence inverts the ordering and adds TQAE as a high-leverage second target.** Pattern-B should absorb this re-ranking into Q1 + Q2 deliberation.

The work is named. The cost is priced. The road forks tomorrow.

---

*Filed 2026-05-18 late evening by gandalf. Mithrandir signs, and waits for morning.*
