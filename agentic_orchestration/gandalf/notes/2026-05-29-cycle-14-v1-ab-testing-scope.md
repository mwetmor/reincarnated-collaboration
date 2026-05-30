# Cycle 14 v1 — Player-Facing A/B Testing Scope

> **STATUS:** CURRENT — Cycle 14 v1 deliverable = scope + variant catalog + infrastructure spec. Cycle 15+ deliverable = execution + data collection + analysis.

**Date:** 2026-05-29
**Author:** gandalf (story-and-design steward)
**Authority:** cascade-r4 § Step 6/7 + § 11.3 Track C — Matt 2026-05-29 Step 7 CONFIRM-FIRE; KR dispatch `agentic_orchestration/dispatches/2026-05-29-gandalf-cycle-14-cascade-r4-track-c-ab-testing-scope.md` (commit `6e7f62f`); hive-mind decision-routing per Matt 2026-05-23.
**Pattern:** Pattern A-deep authoring (verdict in-session per dispatch scope authority).

**Companion docs:**
- `canonical/story/ab-comparison-protocol-cycle-14-close-2026-05-27.md` — **DISTINCT** A/B protocol (architectural-validation; Option α substrate-led emergence vs doc 48 designer-curated baseline). The player-facing A/B testing scope authored here is COMPLEMENTARY, not duplicative. See § 1 disambiguation.
- `canonical/story/2026-05-29-designer-writes-substrate-player-names-experience-principle.md` — the principle this scope serves: validate whether substrate-led emergence READS as player-facing-distinct
- `canonical/story/style-register.md` — locked HD-2D-shaped hand-drawn pixel-art register; load-bearing for every visual variant pair test
- `canonical/38-downstream-delivery-strategy-2026-05-23.md` § D10 — isekai-framing checkpoint; player-facing A/B testing supplies empirical evidence at Stage 2 Playable
- `agentic_orchestration/qa/pending/2026-05-29-jack-ryan-cascade-r3-instance-6-5-framing-audit-canonical-record.md` — Amendment 6 Sub-fix 2 framing (Pareto-2 archive as A/B substrate); player-facing A/B testing scope inherits from this jack-ryan framing
- `agentic_orchestration/cycle-14-wave-5-season-001/phase5_faction_clusters.json` + `phase5_faction_relationships.json` + `phase7_season_summary.json` — season_001 substrate this scope operates on
- `agentic_orchestration/dispatches/2026-05-29-drax-cycle-14-cascade-r4-track-b-loadout-refresh-plus-12-1-hero-pair-drax-half.md` — drax Track B dispatch (loadout app A/B presentation surface coordination target)

---

## 0. TL;DR

Six-axis variant pair catalog across three coordinate dimensions (faction × archetype-vs-Wanderer × element), each with specified test instruments (visual presentation pair / mechanical presentation pair / cohesion-emergence comparison). Cycle 14 v1 ships the scope + infrastructure spec + variant catalog; Cycle 15+ ships execution + data collection + analysis. Loadout app A/B presentation surface coordination documented as Cycle 15+ deliverable spec for drax (avoiding mid-track sub-agent fire; drax Track B reads this doc as forward reference; KR-routes formal coordination dispatch at Cycle 15+ entry).

**Critical disambiguation (§ 1):** the EXISTING `canonical/story/ab-comparison-protocol-cycle-14-close-2026-05-27.md` is the **architectural-validation** A/B (substrate-led-emergence vs designer-curated-baseline; 6 measurement dimensions on engine output). THIS doc is the **player-facing presentation** A/B (variant pairs of substrate-led emergent outputs tested against PLAYERS to validate experiential distinctness). They are TWO LAYERS of A/B testing serving different load-bearing questions; both fire at Cycle 14+ close into Cycle 15+ execution.

---

## 1. Two-layer A/B disambiguation (load-bearing)

**Failure mode this section prevents:** confusing architectural-validation A/B (which doc 48 baseline serves) with player-facing-presentation A/B (which substrate-led variant pairs serve). Both are real; both load-bearing; both fire at Cycle 14+ close.

| Layer | Purpose | Substrate-A | Substrate-B | Acceptance question | Data source | Audience |
|---|---|---|---|---|---|---|
| **Layer 1 — Architectural-validation A/B** (existing protocol; gandalf 2026-05-27) | Does substrate-led emergence produce coverage at least as broad as a designer would have produced? | Option α: Wave 5 substrate-led emergent factions + kits | Doc 48: 10 designer-curated archetype-shapes | "Did the engine deliver substrate-led promise?" (B-PASS / A-PASS / INCONCLUSIVE per 6 dims) | `kit_archive` + `phase7_kit_verdict_log` + `ExportFactionCluster` + `ExportFactionRelationship` | gandalf + jack-ryan + Matt (Discipline #43 wave-close audit) |
| **Layer 2 — Player-facing-presentation A/B** (THIS doc; gandalf 2026-05-29) | Do substrate-led emergent variants READ as player-facing-distinct + compelling + isekai-coded? | Variant A: cluster-membered hero / within-cluster pair / element pair-A | Variant B: Wanderer hero / cross-cluster pair / element pair-B | "Did the player perceive the substrate-led distinction?" (per-instrument verdict; aggregated → presentation tier list) | Loadout app survey responses + side-by-side tile preference + Wave B name preference | Matt + players (eventual; Cycle 15+ aggregation) |

**Composition:** Layer 1 validates engine architecture; Layer 2 validates that engine output READS to humans. Both must PASS for v1 release coherence. Layer 1 PASS without Layer 2 = engine works but player can't tell. Layer 2 PASS without Layer 1 = player sees variation but it's designer-fiat not substrate-led (violates Designer-writes-substrate principle).

**Why this scope exists at all:** the Amendment 6 Sub-fix 2 jack-ryan framing (`agentic_orchestration/qa/pending/2026-05-29-jack-ryan-cascade-r3-instance-6-5-framing-audit-canonical-record.md` § Q4-Q6) established that Pareto-2 archive serves Layer 1 A/B comparison. cascade-r4 Path X fixed Phase 5 wire-up so Phase 5 emergence is now player-facing-coherent (Phase 4 archive → Phase 5 PM-1 input chain operational). With Layer 1 substrate now player-facing-coherent, Layer 2 presentation A/B becomes meaningful — substrate variation is empirically present in what players see, so testing player perception of it is non-tautological.

---

## 2. Three coordinate axes of variant pairs

### Axis I — Per-faction variant pairs (cluster-membered × cluster-membered)

Tests whether substrate-emergent faction identity reads as coherent at within-cluster scale + distinct at cross-cluster scale + stable at cross-season scale.

**Substrate available (season_001 from `phase5_faction_clusters.json` + `phase5_faction_relationships.json`):**

| Cluster | Canonical name | Members | Modal BC signature | Element dist (top) | Primary-pair? |
|---|---|---|---|---|---|
| 1 | Grounded Chain Strikers | 13 | ranged + chain | earth 38% / lightning 31% / fire 15% | TRUE (paired with C4) |
| 2 | Stormbreak Vanguard | 11 | close + large-AOE | lightning 27% / fire 27% / wind 27% | FALSE |
| 3 | Stormveil Ironclad Surge | 9 | close + large-AOE | lightning 44% / holy 22% | FALSE |
| 4 | Ashfield Siege Callers | 1 (SINGLETON candidate post-gamora Amendment 1) | ranged + large-AOE | fire 100% | TRUE (paired with C1) |

#### I.1 — Within-cluster pair (cohesion-comparison)

**Variant pair shape:** two SHIPPED-WORTHY kits from the same cluster (one "high cohesion-judge score" + one "low cohesion-judge score" if cohesion-judge wired post-Wave B; OR two adjacent kits + two distant kits within same cluster by pairwise BC distance).

**Player-facing question:** "Do these two kits read as belonging to the same faction?"

**Example pair candidates (season_001 Cluster 1 Grounded Chain Strikers):**
- High-cohesion pair: `S1_endgame_bc_ranged_low_spiky_str_none_s0` + `S1_endgame_bc_ranged_low_spiky_dex_none_s0` (both ranged + low-spiky; share engagement + amplitude axes)
- Low-cohesion pair: `S1_endgame_bc_melee_low_spiky_str_none_s2` + `S1_endgame_bc_ranged_medium_variable_wis_none_s2` (engagement + amplitude axes diverge within same cluster)

**Cohesion verdict:** if high-cohesion pair scores significantly higher on player "feels like same faction?" survey than low-cohesion pair, substrate-led clustering algorithm produces player-perceptible cohesion structure. If pair scores indistinguishable, either clustering is too coarse OR cohesion-judge calibration drift OR player can't perceive sub-cluster cohesion at presented fidelity.

#### I.2 — Cross-cluster pair (faction-distinction comparison)

**Variant pair shape:** one kit from Cluster A + one kit from Cluster B (different factions).

**Player-facing question:** "Do these two kits read as belonging to DIFFERENT factions?"

**Example pair candidates (season_001):**
- High-distinction pair: `S1_endgame_bc_ranged_low_spiky_str_none_s0` (Grounded Chain Strikers; ranged + earth/lightning) + `S1_endgame_bc_melee_high_flat_str_none_s2` (Stormbreak Vanguard; close + lightning/fire/wind) — engagement + element + AOE-shape diverge across cluster
- Low-distinction pair: `S1_endgame_bc_melee_high_flat_str_none_s2` (Cluster 2 Stormbreak Vanguard) + `S1_endgame_bc_melee_high_flat_str_none_s0` (Cluster 3 Stormveil Ironclad Surge) — modal BC signatures overlap (both close + large-AOE); distinction lives in cultural-lineage (fantasy_generic vs european) + element distribution

**Faction-distinctness verdict:** if cross-cluster pair scores significantly higher on "feels like different factions?" than within-cluster pair, substrate-led faction emergence produces player-perceptible distinction. If pair scores indistinguishable, either factions are too similar at presented fidelity OR cluster-emergence algorithm produces clusters that are not faction-shaped (too compact or too overlapping).

**Critical case from season_001:** Clusters 2 vs 3 share modal BC signature (close + large-AOE) and the F-C relationship narrative explicitly names them as RIVALS contesting "the same tactical ground." This is the **hardest faction-distinction case in season_001** — if players cannot distinguish Stormbreak Vanguard from Stormveil Ironclad Surge, substrate-led emergence may be producing nominally-distinct clusters that read as variations of the same faction. Test instrument should prioritize this pair as load-bearing.

#### I.3 — Cross-season same-faction pair (substrate-led-emergence stability)

**Variant pair shape:** one kit from season_001 Cluster X + one kit from season_002 cluster judged by substrate-metadata to be "the same archetype-shape faction."

**Player-facing question:** "Do these two kits feel like the same faction across seasons?"

**Status:** REQUIRES Track A seasons 002 + 003 close (rocket dispatch firing in parallel; blocked on gamora Amendment 1). **Cycle 14 v1 deliverable = variant pair SHAPE specified; cross-season instance instantiation deferred to Cycle 15+** when 3 LLM seasons aggregate is in hand.

**Cross-season stability verdict:** if cross-season same-faction pair scores high on "feels like same faction across seasons?" survey, substrate-led emergence produces stable faction identity across RNG seeds (load-bearing for D10 Stage 2 evidence — does engine produce coherent isekai-coded factions OR does cross-RNG variance drift the identity each season?). If pair scores low, either substrate-led emergence is too RNG-sensitive at the faction-identity layer OR cluster centroid encoding doesn't preserve recognizable faction identity across substrate samples.

### Axis II — Per-kit-archetype variant pairs (cluster-membered × SINGLETON Wanderer)

Tests whether Wanderer-as-hero alternative pattern reads as compelling, and whether Wanderer-mode emerges with substrate-led variance across seasons.

**Substrate available (post gamora Amendment 1):** season_001 Cluster 4 (n=1; `S1_endgame_bc_ranged_medium_variable_int_light_s0`; fire-mono) is the natural SINGLETON-candidate; reclassifies to cluster_id="SINGLETON" under Amendment 1 architectural commitment (substrate-elected unclustered state at this temporal scale).

#### II.1 — Cluster-membered hero vs Wanderer hero (faction-anchored vs lone-wanderer narrative)

**Variant pair shape:** one cluster-membered kit elected as season hero (galadriel + drax Amendment 2 pair) + the SINGLETON-marked kit re-framed as "Lone Wanderer of [Season Identity]."

**Player-facing question (two complementary instruments):**
1. "Which seasonal hero is more compelling?"
2. "Which seasonal hero feels more isekai-coded?"

**Example pair candidate (season_001 post-gamora):**
- Cluster-membered hero: galadriel + drax pair-elected per Amendment 2 (TBD; § 12.1 hero pair selection); likely from Cluster 1 (Grounded Chain Strikers — primary pair side; largest member count) OR Cluster 2 (Stormbreak Vanguard — multi-element battlefield doctrine; narrative weight)
- Wanderer hero: `S1_endgame_bc_ranged_medium_variable_int_light_s0` re-framed as "Lone Wanderer of [Season Identity]" — ranged + fire-mono + variable amplitude

**Wanderer-as-hero verdict:** if Wanderer hero scores within ±15% of cluster-membered hero on "more compelling?" survey, the Wanderer-as-alternative pattern is viable as a real recurring hero-selection option (not just a fallback when no cluster anchors a strong hero). If Wanderer scores significantly higher, the Wanderer pattern may be carrying narrative weight the cluster heroes are not (substrate-emergence signal: clusters are mechanically-coherent but Wanderers carry isekai-archetype gravity). If Wanderer scores significantly lower, the Wanderer-as-hero pattern is fallback-only and should not be marketed as primary alternative.

**Composition with isekai canon:** the "Lone Wanderer" pattern is genre-thematic isekai-canon (Vagabond / Mushoku Tensei-era post-reincarnation isolation arc / Solo Leveling early-game isolation / KonoSuba's failed-hero start). The Wanderer-as-hero alternative is structurally isekai-coherent in a way that faction-anchored heroes are not. This makes Wanderer-as-hero a load-bearing test for D10 isekai-framing — if Wanderer reads as more isekai-coded than faction hero, the engine is producing isekai-flavor at the Wanderer layer specifically.

#### II.2 — Within-Wanderer cross-season pair (substrate-led variance signal)

**Variant pair shape:** Wanderer from season_001 + Wanderer from season_002 (assuming both seasons produce at least one SINGLETON-marked kit per Amendment 1; expected per state file § Amendment 1 expected-results: 0-3 Wanderers per season RNG-dependent).

**Player-facing question:** "Do these two Wanderers feel like separate characters, or variations on the same archetype?"

**Status:** REQUIRES Track A seasons 002 + 003 close + at least one SINGLETON per season. **Cycle 14 v1 deliverable = variant pair SHAPE specified; cross-season Wanderer instance instantiation deferred to Cycle 15+.**

**Wanderer-variance verdict:** if cross-season Wanderer pair reads as DISTINCT characters, substrate-led emergence preserves per-Wanderer identity across RNG seeds (Wanderers are not just "the leftover kit" — they are substrate-elected with characterful variance). If pair reads as same-archetype-variations, Wanderer-as-architecture may need richer per-Wanderer characterization at Cycle 15+ (Wave B kit naming context could extend with explicit "Lone Wanderer of [Season Identity]" framing per Amendment 1).

### Axis III — Per-element-class variant pairs

Tests element-identity legibility AND faction-distinction vs element-distinction precedence in player perception.

#### III.1 — Same-element different-faction pair (element-shared faction-distinct)

**Variant pair shape:** two kits with the SAME primary element from DIFFERENT factions.

**Player-facing question:** "Do these two lightning users feel like they belong to the same OR different factions?" (Or per-element: same-fire, same-earth, etc.)

**Example pair candidate (season_001):**
- Lightning-shared cross-faction pair: a lightning-primary kit from Cluster 1 Grounded Chain Strikers (e.g., the lightning members of `element_distribution: lightning 31%`) + a lightning-primary kit from Cluster 3 Stormveil Ironclad Surge (`lightning 44%`) — element shared, faction context (ranged earth-frontier vs close european-medieval) diverges
- Or fire-shared: a fire kit from Cluster 2 Stormbreak Vanguard (`fire 27%`) + the Cluster 4 Wanderer-candidate `_int_light_s0` (fire 100%) — element shared, mechanical context (close multi-element AOE vs ranged variable single-element) diverges

**Element-faction precedence verdict:** if same-element pair scores high on "same faction?" survey despite cluster_id divergence, players are reading element-class as primary faction-identity signal (element dominates faction in player perception). If pair scores low, faction context (substrate metadata + Wave B name + cluster narrative) successfully overrides element-shared visual signal. The verdict informs presentation-tier hierarchy: which axis (element vs faction) carries player-perceived identity weight, and what UI emphasis honors that.

#### III.2 — Different-element same-archetype pair (geometry-shared element-distinct)

**Variant pair shape:** two kits with the SAME BC archetype-shape (engagement + geometry signature) but DIFFERENT primary elements.

**Player-facing question:** "Do these two chain-strikers feel like the same archetype, just elementally re-skinned?"

**Example pair candidate (season_001 Cluster 1):**
- Earth chain-striker + lightning chain-striker (both within Cluster 1 Grounded Chain Strikers; both ranged + chain; different primary element) — archetype shared, element-skin diverges
- Or cross-cluster: a Cluster 2 close large-AOE multi-element kit + a Cluster 3 close large-AOE lightning-dominant kit — archetype shared, element-fingerprint diverges

**Archetype-element verdict:** if pair scores high on "same archetype, different skin?" survey, player perception is correctly reading BC-archetype as primary identity + element as flavor-layer. If pair scores low (perceived as different archetypes despite shared BC), either element carries more weight than designed OR Wave B kit naming is element-overweighted (kit names lead with element, obscuring BC-archetype identity). The verdict informs Wave B prompt tuning at Cycle 15+ (per Designer-writes-substrate § 4.4 Wave B kit naming Cycle 15+ extension).

---

## 3. Test instruments per variant pair type

Each instrument operationalizes one or more variant pair questions for empirical execution in Cycle 15+. Cycle 14 v1 deliverable = instrument specifications; Cycle 15+ deliverable = instrument implementation + data collection + analysis.

### 3.1 Visual presentation pair tests

Substrate-anchored visual variants rendered in the locked HD-2D-shaped hand-drawn pixel-art register (per `canonical/story/style-register.md` § "Lock Candidate B"). Style-register adherence is REQUIRED for every visual instrument — variant pairs render in the same register so the variant axis tests substrate-emergence-perception, not register-difference-perception.

| Instrument | Variant axis | Surface | Player survey question |
|---|---|---|---|
| **VI-1 — Faction tile side-by-side** | I.1 + I.2 + I.3 | Two faction tiles rendered side-by-side in loadout app summary tab (HD-2D pixel; faction-name + modal lineage + BC signature + element distribution + 2-3 representative kit names) | "Which faction would you rather play this season?" + "Do these factions feel distinct?" |
| **VI-2 — Hero card pair** | II.1 + II.2 | Two seasonal-hero cards side-by-side (HD-2D pixel hero portrait + name + faction-anchor OR Wanderer-frame + BC archetype + element) | "Which seasonal hero is more compelling?" + "Which feels more isekai-coded?" |
| **VI-3 — Element marquee art pair** | III.1 + III.2 | Two element-flavored marquee art pieces side-by-side (HD-2D pixel; per-element palette per `style-register.md` element-palette catalogue; faction or Wanderer context layered) | "Which element identity reads more distinctly?" + "Do these feel like the same archetype?" |

**Style register adherence per instrument** (load-bearing constraint per `canonical/story/style-register.md` Path A-prime second amendment):
- All sprite renders at ARPG-anchored operational target (chierit-scale 2.5× → ~108 px figure-content; nearest-neighbor enforcement CRITICAL)
- All faction tiles + hero cards + element marquees in single register (no within-frame mixing per style-register.md § "The proposal")
- Per-embodiment register awareness honored (Wanderer non-humanoid forms render in HD-2D pixel just as cluster-membered humanoid forms do; per-embodiment variance happens within register, not across registers — per style-register.md § "Per-embodiment register awareness")
- LLM image generation (§ 12.2 drax dispatch + legolas Track B prompts) uses canonical register language per style-register.md § "Maintenance protocol"

### 3.2 Mechanical presentation pair tests

Tests whether mechanical signature carries player-perceptible distinction WITHOUT visual support (text-only OR mechanical-summary rendering).

| Instrument | Variant axis | Surface | Player survey question |
|---|---|---|---|
| **MP-1 — BC-axes signature pair** | I.1 + I.2 + II.1 + III.2 | Two kits presented as BC-axis text summaries (engagement / damage-geometry / damage-tempo / amplitude-variance / etc.; NO faction name; NO Wave B kit name; NO visual art) | "Which build approach matches your play preference?" + "Do these feel like different archetypes?" |
| **MP-2 — Wave B name pair** | I.1 + I.2 + II.1 | Two Wave B-generated kit names side-by-side (text-only; NO BC summary; NO visual art; faction context optional per sub-condition) | "Which name reads more naturally?" + "Which feels more isekai-coded?" |

**Substrate-isolation property:** MP-1 and MP-2 isolate substrate signal at the mechanical layer (MP-1) and the naming layer (MP-2). If a visual presentation pair scores high but the mechanical-isolation pair scores low, visual presentation is carrying the distinction signal (player perceives variation primarily through art); if mechanical-isolation pair scores comparably to visual, substrate signal is reading through at multiple layers (load-bearing positive: Designer-writes-substrate is operational at presentation layer).

### 3.3 Cohesion-emergence comparison tests

Tests whether cohesion-judge calibration (Phase 5 cluster compactness + per-kit cohesion verdict per gamora Amendment 1 Phase 7 split) PRODUCES player-perceptible cohesion structure.

| Instrument | Variant axis | Surface | Player survey question |
|---|---|---|---|
| **CE-1 — Within-cluster high vs low cohesion-judge pair** | I.1 | Two cluster-membered kit pairs: one pair with HIGH within-cluster cohesion-judge score + one pair with LOW within-cluster cohesion-judge score (both pairs from same cluster) | "Which pair feels more coherent (like they belong together)?" |
| **CE-2 — Cross-cluster faction distinctness pair** | I.2 | Two kit pairs: one pair from same cluster (within-cluster) + one pair from different clusters (cross-cluster) | "Which pair feels more like belonging to different factions?" |
| **CE-3 — Substrate-led-emergence stability pair** | I.3 + II.2 | Two kit pairs: one pair from season_001 + one pair from season_002 (both pairs representing "same archetype-shape faction" by substrate-metadata + cohesion-judge alignment) | "Do these faction-pairs feel like the same faction across seasons?" |

**Cohesion-judge calibration loop:** CE-1 and CE-2 produce empirical evidence on whether the cohesion-judge score (Phase 5 + Phase 7 cohesion-judge per gamora Amendment 1) correlates with player-perceived cohesion. If correlation is strong, cohesion-judge calibration is operational; if correlation is weak, cohesion-judge needs Cycle 15+ recalibration (which is why this is Cycle 15+ execution scope, not Cycle 14 v1 — calibration loop requires empirical data first).

### 3.4 Cross-instrument composition

For each variant pair, the FULL instrument battery is:
- VI-1 OR VI-2 OR VI-3 (visual layer)
- MP-1 + MP-2 (mechanical isolation layer)
- CE-1 OR CE-2 OR CE-3 (cohesion-emergence layer)

Player completes ~3 surveys per pair; ~5 pairs per session (~15 surveys); session length ~10-15 min. Cycle 15+ infrastructure scope = loadout-app A/B surface + survey widget + persistent local state + cross-session result aggregation (§ 4).

---

## 4. Loadout app A/B presentation surface — coordination notes

**Coordination state for drax (Track B § 11.2 — drax dispatch in parallel firing):** the loadout app refresh dispatch (drax Track B) does NOT presently scope A/B presentation surface infrastructure. Per KR routing trigger evaluation: A/B surface infrastructure is Cycle 15+ scope (per dispatch § "Cycle 14 v1 deliverable = scope filed (infrastructure spec + variant catalog); Cycle 15+ deliverable: A/B execution + data collection + analysis").

**Decision per dispatch authority:** document A/B surface infrastructure requirements HERE as Cycle 15+ deliverable spec rather than fire drax mid-track. Drax Track B baseline (summary tab + per-faction tiles + Wanderer post-gamora) is the FOUNDATION the A/B surface extends. KR routes formal coordination dispatch at Cycle 15+ entry when Track A + Track B + this scope all close.

### 4.1 Loadout-app A/B presentation infrastructure spec (Cycle 15+ drax deliverable target)

**Surface requirements:**

1. **Side-by-side tile rendering** — render any two variant tiles (faction-tile OR hero-card OR element-marquee) horizontally adjacent at HD-2D pixel resolution per style-register.md (ARPG-anchored 100-130 px figure-content target; nearest-neighbor enforcement CRITICAL; intra-class silhouette variance preserved per style-register.md Path A-prime second amendment)

2. **Survey widget** — embed below each pair: question text + answer options (Likert 5-point OR forced-choice binary depending on instrument; MP-2 "which reads more naturally?" is forced-choice; CE-1 "which feels more coherent?" is Likert)

3. **Persistent local state** — each session writes survey responses to localStorage (browser-local; cross-session aggregation deferred to step 4)

4. **Cross-session aggregation** — Cycle 15+ infrastructure target: backend collection endpoint (or localStorage export → manual aggregation if backend-deferred) aggregating responses across player sessions

5. **Per-pair tracking ID** — each variant pair has stable ID for analysis aggregation (e.g., `season_001_I.1_high_vs_low_cohesion`)

6. **Style-register guarantee** — same register applies to both tiles in a pair (no within-frame mixing; no cross-register comparison); register pivot insurance preserved per style-register.md § "Pivot insurance"

### 4.2 Data contract requirements (extending drax Track B baseline data contract)

Drax Track B baseline data contract (per drax dispatch § 3): `cluster_id: int | "SINGLETON"` type union. A/B surface extends with:

```typescript
type VariantPair = {
  pair_id: string;              // e.g., "season_001_I.1_high_vs_low_cohesion"
  axis: "I.1" | "I.2" | "I.3" | "II.1" | "II.2" | "III.1" | "III.2";
  instrument: "VI-1" | "VI-2" | "VI-3" | "MP-1" | "MP-2" | "CE-1" | "CE-2" | "CE-3";
  variant_a: KitOrCluster;      // the A side
  variant_b: KitOrCluster;      // the B side
  survey_question: string;      // human-readable; per instrument spec § 3
  survey_response_schema: "likert_5" | "binary_forced";
};
type SurveyResponse = {
  pair_id: string;
  session_id: string;
  response: number | "a" | "b";  // 1-5 Likert, OR "a"/"b" forced-choice
  timestamp: string;
};
```

### 4.3 Coordination triggers (KR routes if any fire)

- **Drax requests pre-Cycle 15+ A/B surface spike** to validate technical feasibility before Cycle 15+ formal scope → KR routes for Matt design call (could fold into Track B if Matt elects)
- **Style register ambiguity arises at A/B surface design** (e.g., Wanderer card register treatment vs cluster-membered hero card register treatment) → KR routes for Matt design call (UNLIKELY; locked per style-register.md including per-embodiment register-awareness)
- **A/B surface presents architecturally distinct from Cycle 14 v1 loadout-app baseline** (e.g., separate route / separate component tree) → KR routes for Matt confirmation of v1 vs v1.1 scope split
- **Backend infrastructure decision** (localStorage-only vs Vercel KV vs external survey platform) → KR routes for Matt design call at Cycle 15+ entry

---

## 5. Cycle 14 v1 deliverable summary

**Cycle 14 v1 ships (this doc):**

- [x] A/B variant pair catalog across 3 axes (I.1/I.2/I.3 per-faction; II.1/II.2 per-archetype-vs-Wanderer; III.1/III.2 per-element-class) — § 2
- [x] Test instruments specified per variant pair type (VI-1/2/3 visual + MP-1/2 mechanical + CE-1/2/3 cohesion-emergence) — § 3
- [x] Style register adherence noted per visual variant pair test — § 3.1 + § 4.1
- [x] Loadout app A/B presentation surface coordination notes (documented inline as Cycle 15+ drax deliverable spec; NOT fired mid-track per KR routing trigger) — § 4
- [x] Cycle 14 v1 + Cycle 15+ deliverable split documented — this § + § 6
- [x] Composes-with documentation (Amendment 6 Sub-fix 2 / Amendment 1 / Amendment 2 + Designer-writes-substrate principle + D10 isekai-framing checkpoint + existing architectural-validation A/B protocol disambiguation) — § 7

**Cycle 14 v1 explicit non-deliverables:**

- NO A/B execution (deferred Cycle 15+)
- NO loadout-app A/B presentation infrastructure implementation (deferred Cycle 15+ drax; spec in § 4.1)
- NO data collection / analysis (deferred Cycle 15+)
- NO Wanderer architecture implementation (gamora Amendment 1; this doc composes-with)
- NO hero selection (drax + galadriel Amendment 2 pair; this doc lists hero-pair-pick as A/B instrument input via VI-2 + MP-1 + MP-2)

---

## 6. Cycle 15+ execution plan

### 6.1 Cycle 15+ workstream sequence (proposed; KR canonicalizes at Cycle 15+ entry)

| # | Workstream | Owner | Gates on | Deliverable |
|---|---|---|---|---|
| 1 | Loadout-app A/B presentation infrastructure | drax | Cycle 14 v1 close + Cycle 15+ scope authorization | Side-by-side tile rendering + survey widget + persistent local state + per-pair tracking ID + extended data contract per § 4.1 |
| 2 | Per-instance variant pair instantiation (3 seasons aggregate) | gandalf + galadriel (visual CV scoring) + drax (UX-fit) | Track A seasons 002 + 003 close (rocket); Wanderer instances landed (gamora Amendment 1 cross-season replication) | Concrete variant pair instances per axis I.1/I.2/I.3/II.1/II.2/III.1/III.2 per-season + cross-season; ready for player-facing surface |
| 3 | Player surveys conducted | drax (loadout-app surface) + Matt (initial playtest cohort; Matt's son per CLAUDE.md `user_role.md`) | Workstreams 1 + 2 close | Survey responses aggregated; per-pair n=10-30 responses (single-playtester cohort) OR n=50-200 (extended playtest cohort if Matt elects) |
| 4 | Analysis + presentation-tier verdict | gandalf + jack-ryan | Workstream 3 closes with sufficient sample size | Per-instrument verdict + per-axis verdict + composite verdict; informs (a) cohesion-judge recalibration; (b) Wave B prompt tuning; (c) D10 Stage 2 Playable evidence; (d) presentation-tier hierarchy for v1.1 launch |
| 5 | Loop back to engine architecture if verdict surfaces drift | gamora + rocket + elrond | Workstream 4 close | Architectural amendments per drift signal (cohesion-judge recalibration; Wave B prompt extension per Designer-writes-substrate § 4.4) |

### 6.2 Cycle 15+ open questions for Matt resolution at Cycle 15+ entry

1. **Player cohort scope** — single-playtester (Matt's son per CLAUDE.md) OR extended playtest cohort (community / discord beta)? Single-playtester provides directional verdict at small-n; extended cohort provides statistical verdict at larger-n.
2. **Backend infrastructure** — localStorage-only (Cycle 15+ v1 baseline; manual aggregation acceptable at small-n) OR Vercel KV (Cycle 15+ v1.1 if extended cohort elected) OR external survey platform (e.g., Typeform) OR Vercel Workflow (if survey orchestration scales beyond simple persistence)?
3. **Test session pacing** — single 15-min session per playtester OR per-axis sessions across multiple playthrough sessions OR longitudinal pacing (per-season survey at season-end)?
4. **Marketing-art register branch** — per `style-register.md` § "Q5 Marketing / promotional art register" open question: should A/B testing scope also test marketing-art register variants (HD-2D pixel vs raster anime) at Cycle 15+ for marketing positioning? OUT OF SCOPE for current scope; flagged for Cycle 15+ entry consideration.
5. **Cohort_archetype → player-experience mapping survey** — per Designer-writes-substrate § 4.5 Cycle 15+ candidate: does Cycle 15+ A/B testing also include cohort_archetype perception surveys (DPS-min-maxer / Balanced / Defensive / Hybrid presented as activity-vocabulary-mapped Bossing / Speedfarming / Endgame / Endgame-Generalist)? Composes naturally with this scope as ADDITIONAL axis IV (per-cohort-archetype variant pairs); FLAGGED as Cycle 15+ entry consideration.

---

## 7. Composes-with documentation

### 7.1 Amendment 6 Sub-fix 2 (jack-ryan Pareto-2 A/B substrate framing)

`agentic_orchestration/qa/pending/2026-05-29-jack-ryan-cascade-r3-instance-6-5-framing-audit-canonical-record.md` § 5 + § 7 establishes Pareto-2 archive as load-bearing for A/B comparison protocol (architectural-validation Layer 1). Cascade-r4 Path X closed the Phase 4 → Phase 5 wire-up so Phase 5 emergence now consumes Pareto-2 archive substrate. This player-facing A/B scope (Layer 2) operates on Phase 5 emergent outputs that are now Pareto-2-archive-coherent — meaning when this scope tests player perception of substrate-led emergence, the substrate is genuinely Pareto-2-archive-derived (no decorative-archive concern at Layer 2). jack-ryan's framing-audit work made Layer 2 non-tautological.

### 7.2 Amendment 1 (Wanderer architecture)

`agentic_orchestration/cycle-14-hive-mind-state.md` § "AMENDMENT 1 — Wanderer architecture (gamora dispatch scope)" establishes substrate-elected SINGLETON state + "Wanderer" player-facing canonical term + per-kit cohesion-judge verdict for SINGLETONs. This scope consumes Amendment 1 architecture as the basis for Axis II (cluster-membered hero vs Wanderer hero; within-Wanderer cross-season pair). Amendment 1 architectural commitment is what makes Axis II non-vestigial — without Amendment 1, the "Lone Wanderer" pattern is a designer-imposed alternative; WITH Amendment 1, Wanderer-as-hero is a substrate-elected emergent pattern that can be empirically tested for player-coherence.

### 7.3 Amendment 2 (galadriel-drax hero pair selection)

`agentic_orchestration/cycle-14-hive-mind-state.md` § "AMENDMENT 2 — § 12.1 seasonal hero selection delegated to galadriel + drax pair" + drax Track B dispatch § "§ 12.1 hero pair drax half" establishes pair-consensus selection authority for seasonal hero. This scope lists hero-pair-pick as A/B instrument input via VI-2 (hero card pair) + MP-1 (BC-axes signature pair) + MP-2 (Wave B name pair). The hero pair selection output (`agentic_orchestration/drax/notes/2026-05-29-cycle-14-v1-seasonal-hero-selection.md` per drax dispatch § 4.4) feeds Axis II instruments at Cycle 15+ execution.

### 7.4 Designer-writes-substrate principle (gandalf 2026-05-29 evening)

`canonical/story/2026-05-29-designer-writes-substrate-player-names-experience-principle.md` establishes the two-layer architectural separation: designer-writes-substrate at the generative layer + player-names-experience at the post-emergence consumption layer. This player-facing A/B scope is the EMPIRICAL VALIDATION INSTRUMENT for whether substrate-led emergence READS as player-facing-distinct (the principle's load-bearing implicit claim). Per Designer-writes-substrate § 4.2 "Player-experience emerges and is community-named; engine consumes post-emergence" — this scope's player surveys ARE the empirical-evidence instrument for the player-experience layer. § 4.3 "Class/ascendancy/archetype labels are SECONDARY descriptive anchors, NOT primary categorical axes" composes with Axis III element-vs-archetype precedence verdict (III.1 + III.2).

### 7.5 Canonical 38 D10 isekai-framing checkpoint

`canonical/38-downstream-delivery-strategy-2026-05-23.md` § D10 establishes two-stage isekai-framing checkpoint (Stage 1 Cluster + Stage 2 Playable) with three paths (Path A tighten engine; Path B shift framing copy; Path C embrace what engine wants to be). This player-facing A/B scope is empirical-evidence-instrument-grade input to Stage 2 Playable, specifically:
- Axis II.1 "which feels more isekai-coded?" survey instrument provides direct D10 Stage 2 evidence on whether Wanderer-as-hero pattern (genre-thematic isekai canon) reads as more isekai-coded than faction-anchored hero
- Axis I.2 cross-cluster pair test provides D10 Stage 2 evidence on whether substrate-led emergent factions read as isekai-coherent OR sprawl across genres
- The aggregate of player-survey responses across all instruments contributes empirical evidence to Matt + gandalf + jack-ryan D10 Stage 2 decision (Path A / B / C election)

**Critical sequencing:** Layer 1 architectural-validation A/B (Option α vs doc 48; existing protocol) fires at Wave 5 close per architectural-validation protocol; Layer 2 player-facing presentation A/B (this scope) fires at Cycle 15+ player surveys; BOTH feed D10 Stage 2 evidence. D10 path election cannot fire until both layers produce verdicts.

### 7.6 Style register (locked HD-2D pixel-art HD-2D-shaped)

`canonical/story/style-register.md` (Path A-prime second amendment) is consumed at every visual instrument (VI-1 + VI-2 + VI-3) as the operational rendering target. Style-register adherence is empirically necessary — variant pair tests can only test substrate-emergence-perception if the register variable is held constant. Cross-register comparison is OUT OF SCOPE for this protocol (style register pivot insurance preserves the option per style-register.md § "Pivot insurance" but Cycle 15+ A/B execution operates at locked register).

---

## 8. Predictions registered for Cycle 15+ empirical validation

Per § 3.4 recognition-validate-commit discipline, registering predictions HERE for Cycle 15+ empirical refutation:

| # | Prediction | Falsifies if | Architectural implication if FALSIFIED |
|---|---|---|---|
| **P1** | Within-cluster high-cohesion pair (CE-1) scores ≥1 Likert point higher than within-cluster low-cohesion pair | High vs low cohesion pair scores indistinguishable (Δ < 0.5 Likert) | Cohesion-judge calibration drift; Cycle 15+ recalibration required |
| **P2** | Cross-cluster pair (I.2) scores higher on "different factions" than within-cluster pair | Cross-cluster pair scores comparably to within-cluster pair | Substrate-led cluster emergence produces nominally-distinct but player-indistinct clusters; PM-1 algorithm needs re-review |
| **P3** | Stormbreak Vanguard vs Stormveil Ironclad Surge pair (I.2 hardest case) scores at OR above cross-cluster baseline | This pair scores at OR below within-cluster baseline | Substrate-distinction below player-perception floor for shared-modal-BC clusters; Wave A faction-naming + Wave B kit-naming need element-distribution-weighted prompting OR PM-1 needs higher k |
| **P4** | Wanderer hero (II.1) scores within ±15% of cluster-membered hero on "more compelling?" | Wanderer scores >25% below cluster-membered | Wanderer-as-hero is fallback-only; do NOT market as primary alternative; recommend cluster-anchored hero as season-marquee default |
| **P5** | Wanderer hero (II.1) scores higher than cluster-membered hero on "more isekai-coded?" | Wanderer scores equal or lower on isekai-coding | "Lone Wanderer" pattern is NOT carrying additional isekai-canonical gravity over cluster-anchored hero; D10 Stage 2 evidence shifts toward Path B (shift framing copy) or Path C (embrace cross-genre) rather than Path A (tighten to isekai) |
| **P6** | Same-element cross-faction pair (III.1) scores LOW on "same faction?" survey | Same-element pair scores high on "same faction?" | Element class is dominating faction identity in player perception; faction architecture is decorative at the player-presentation layer; Wave B naming + faction-tile presentation need de-element-weighting |
| **P7** | Cross-season same-faction pair (I.3) scores HIGH on "same faction across seasons?" | Cross-season pair scores low on "same faction across seasons?" | Substrate-led emergence is RNG-sensitive at faction-identity layer; Wave A faction-naming needs cross-season anchoring strategy OR substrate clustering needs stability-loss reduction |
| **P8** | Wanderer cross-season pair (II.2) scores LOW on "same archetype" (i.e., reads as DISTINCT characters) | Cross-season Wanderer pair scores high on "same archetype" | Wanderer architecture is producing structurally-similar leftover-kits rather than substrate-elected characterful variants; Wave B "Lone Wanderer of [Season Identity]" framing needs richer per-Wanderer characterization |

**Empirical-criterion for re-engagement:** Cycle 15+ player survey responses landing per workstream § 6.1 #3. NOT time-passage; empirical evidence gates re-engagement per § 3.4.

---

## 9. Sign-off

**Authored:** gandalf (story-and-design steward) per cascade-r4 Step 7 § 11.3 Track C dispatch (Matt 2026-05-29 Step 6 CONFIRM-FIRE)

**For:** the durable canonical capture of Cycle 14 v1 player-facing A/B testing scope — three coordinate axes of variant pairs (per-faction I.1/I.2/I.3 + per-archetype-vs-Wanderer II.1/II.2 + per-element-class III.1/III.2) × three instrument categories (visual VI-1/2/3 + mechanical MP-1/2 + cohesion-emergence CE-1/2/3) — with explicit two-layer A/B disambiguation against existing architectural-validation protocol, loadout-app A/B surface coordination as Cycle 15+ drax deliverable spec, Cycle 14 v1 + Cycle 15+ split documentation, composes-with documentation across Amendment 6 Sub-fix 2 + Amendment 1 + Amendment 2 + Designer-writes-substrate + D10 + Style Register, and 8 predictions registered for Cycle 15+ empirical refutation per recognition-validate-commit discipline.

**Cycle 14 v1 acceptance criteria** (per dispatch):
- [x] A/B variant pair catalog (per-faction + per-archetype + per-element axes) — § 2
- [x] Test instruments specified per variant pair type — § 3
- [x] Loadout app A/B coordination notes filed — § 4
- [x] Cycle 14 v1 + Cycle 15+ deliverable split documented — § 5 + § 6
- [x] Composes-with documentation — § 7
- [x] Style register adherence noted per visual variant pair test — § 3.1 + § 4.1

**Deferred to Cycle 15+** per empirical-criterion-gated workstream:
- A/B execution (workstream § 6.1 #3)
- Loadout-app A/B presentation infrastructure implementation (workstream § 6.1 #1)
- Data collection + analysis + per-instrument verdict (workstream § 6.1 #3 + #4)
- Architectural amendments per drift signal if verdicts surface drift (workstream § 6.1 #5)

— gandalf
