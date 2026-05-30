# Wave-S — Season-itself Naming Design Spec

> **STATUS:** CURRENT (load-bearing as of 2026-05-29) — Cascade-resumption-4 follow-on per Matt 2026-05-29 verbatim. Resolves the season-name gap empirically surfaced when knight-rider audited Phase 5 LLM coverage and discovered ZERO `season_name` / `name_season` references in engine src — Wave A produces faction names, Wave B produces per-kit names, but the season-itself was never named. Authors a new Phase 5 LLM call surface (Wave-S) that composes from already-emerged Wave A faction substrate + season-level aggregates per the designer-writes-substrate / player-names-experience architectural principle (Matt 2026-05-29 evening verbatim).

**Date:** 2026-05-29
**Author:** gandalf (story-and-design steward)
**Authority:**
- Matt 2026-05-29 verbatim: *"knight-rider, did I see that these seasons did not produce LLM names for our characters and for the season itself? Can we implement retroactive LLM naming across these gaps? Afterwards, let's plug the gaps for future generation."*
- Hive-mind decision-routing directive (Matt 2026-05-23): seam-owner decides in-scope work; this spec is gandalf's design authority per scope-map
- Auto-commit per CLAUDE.md addendum 2026-05-25 (cascade-r4 follow-on cycle authorization carries spec authorship + commit)

**Companion docs:**
- `canonical/story/2026-05-29-designer-writes-substrate-player-names-experience-principle.md` — foundational principle; Wave-S sits at the player-names-experience layer consuming designer-writes substrate
- `canonical/story/phase-5-llm-prompts-cohesion-judge-2026-05-27.md` — Wave A + Wave B + F-C prompt-template canon; Wave-S extends this set as a fourth surface
- `canonical/story/style-register.md` — locked HD-2D pixel-art register, isekai-genre-coded; season names READ as isekai-genre-native
- `canonical/38-downstream-delivery-strategy-2026-05-23.md` § D7 — AI-tell line; Wave-S is templated-narrow-blanks (not raw LLM)
- `canonical/historical/19-llm-call-map.md` — historical call-map (extension target for Wave-S registration; canonical move to current docs handled by knight-rider routing)
- `agentic_orchestration/cycle-14-hive-mind-state.md` cascade-r4 § Amendment 1 (Wanderer architecture) + § Amendment 2 (galadriel-drax hero pair)
- `agentic_orchestration/cycle-14-wave-5-season-001/phase5_faction_clusters.json` (+ 002/003) — substrate ground-truth this spec consumes

**Scope:** design spec only. NO implementation (star-lord owns Wave-S LLM call wiring; rocket owns orchestrator integration + retroactive execution). NO cache investigation. NO drax data-contract authoring (drax follow-on consumes season_name canonical surface). This spec is the canonical reference both downstream seams build against.

---

## § 0 TL;DR

Matt surfaced two empirical naming gaps in production Phase 5 output (season_001/002/003). Wave B kit-naming gap = persistence-only bug (rocket fix). **Season-itself naming gap = NEVER IMPLEMENTED** — no design exists.

**Wave-S spec:** a NEW fourth Phase 5 LLM call surface, ONE call per season, fires AFTER Wave A (consumes faction-name + thematic-tag substrate aggregate as primary input), in parallel with F-C (no inter-dependency), BEFORE Wave B (so per-kit Wave B prompts can reference `{season_name}` as composition context). Templated SYSTEM + USER per D7 AI-tell discipline; substrate-grounded acceptance gates (length 3-7 words, ≥2 substrate signals referenced, no AI-tell phrases, lexical distinctness across seasons, isekai-canon register). Pattern: `Season of the [substrate-derived noun phrase]` OR `The [substrate-derived noun phrase]` (isekai-genre-native). Wanderer composition: Wanderer-COUNT modulates an OPTIONAL season-sub-narrative phrase (NOT the primary name); per-season name stays faction-substrate-grounded. Retroactive backfill across 3 seasons = ~$0.045 total at $0.015/call. Composes cleanly with Amendment 1 + 2 + designer-writes-substrate + locked style register. Unblocks drax loadout summary-tab full-surface header + § 12 hero-card season-context line. **3 worked examples below confirm the spec produces good names from existing substrate.**

---

## § 1 Election rationale — 9 design questions resolved

### Q1 — Substrate inputs (RESOLVED)

**Election:** PRIMARY input = Wave A faction-name set + per-faction thematic_tags aggregate. SECONDARY = season-level element distribution aggregate + modal cultural lineage aggregate + Wanderer count. TERTIARY = season_id for cache-key + RNG-seed echo provenance only (NOT as name fodder).

**Reasoning:** Wave A faction names ARE the season's substrate-honest narrative voice — they were produced by the cohesion-judge from the same substrate that defines the season. A season name composed from those four (or three) faction names is automatically substrate-grounded by transitivity. Going DIRECTLY to raw element distributions risks duplicating Wave A's work or producing names that disagree with Wave A's faction labels (e.g., faction-tier says "Stormveil" + season-tier independently picks "Tidal" — incoherent). Faction-name aggregate as primary input enforces inter-tier coherence by composition, not by re-derivation. Wanderer count is composition-aware (Q3) but does NOT drive primary name choice — per Amendment 1, Wanderers are SINGLETON faction-members, not a separate substrate-layer; their presence is sub-narrative flavor.

### Q2 — Player-facing pattern (RESOLVED)

**Election:** Pattern A (PRIMARY) `Season of the [substrate-derived noun phrase]` OR Pattern B (ALTERNATE, when faction-name aggregate yields a strong single noun phrase) `The [substrate-derived noun phrase]`. LLM chooses A vs B based on substrate fit (acceptance gate W-S2 verifies one of the two patterns).

**Reasoning:** "Season of the X" is isekai-canon-coded — direct lineage from Solo Leveling's "Season of Awakening"-style framings, Re:Zero arc titles, Mushoku Tensei volume titles ("Adolescence Period of the X Family"). "The X" is shorter / harder-hitting / matches PoE league-naming convention (Affliction, Necropolis, Settlers). Single-noun-phrase pattern is genre-ambiguous (could be MMO, could be JRPG, could be ARPG) which fits Reincarnated's isekai-mobile-ARPG positioning per pitch. Year-prefix patterns ("Year of X") were rejected as too WoW-coded — doesn't match isekai voice. Pair-of-words isekai patterns (e.g., "Stormveil Cycle") were folded into Pattern B as the LLM's option-space. The LLM chooses which of the two patterns the substrate composition wants; the acceptance gate enforces one of the two MUST hold.

### Q3 — Wanderer composition (RESOLVED)

**Election:** Wanderers DO NOT modify the primary season name. They surface as an OPTIONAL `season_sub_narrative` field on the Wave-S output (1-sentence; references Wanderer count by name-pattern: 0 → field is null; 1 → "...marked by a single Lone Wanderer..."; 2+ → "...marked by [N] Wanderers..."). The primary season name stays faction-substrate-grounded.

**Reasoning:** Wanderer count is RNG-driven and season-variant per Amendment 1; making it drive primary name would couple the season name's stability to substrate noise. Player-experience-honest framing per the designer-writes-substrate principle: the season name names the SEASON (the substrate envelope); the sub-narrative names the noteworthy substrate-emergent event (Wanderer presence). Composes cleanly with Amendment 2 § 12.1: when the galadriel-drax hero pair elects a Wanderer-as-hero ALTERNATIVE, the sub_narrative field becomes the hero-card narrative context ("Lone Wanderer of the [Season Name]" — the season-name PATTERN per Q2 + the wanderer-as-hero PATTERN per Amendment 2 § 12.1 compose lexically).

### Q4 — D7 AI-tell compliance (RESOLVED)

**Election:** Templated SYSTEM prompt + structured USER prompt with named substrate blanks per the Wave A / Wave B pattern (canonical/story/phase-5-llm-prompts-cohesion-judge-2026-05-27.md § 4 + § 5). NOT raw LLM dialogue. Same AI-tell ban-list as Wave A § 4.2 SYSTEM constraint 4, PLUS season-specific AI-tells (additions below at § 5).

**Reasoning:** D7 is non-negotiable per canonical 38 § D7. Season-name surfaces VERY HIGH player-trust real-estate (loadout app header; summary-tab caption; spirit-guide narration onboarding text). A bad season name reads as "obvious AI" louder than a bad kit name does — the player sees the season name FIRST and most frequently. Templating with substrate-filled narrow blanks is the SAME pattern Wave A + Wave B already operate under; Wave-S inherits the discipline without inventing new compliance mechanism.

### Q5 — Acceptance gates (RESOLVED)

**Election:** 5 acceptance gates per § 5 below: length (3-7 words), substrate-grounding (≥2 substrate signals referenced — at least one faction-name epithet + at least one thematic tag OR element OR cultural lineage), D7 AI-tell mechanical grep (no banned phrases), distinctness (season name lexically distinct from prior season names by Jaccard <0.5), register (matches isekai-canon-coded register; D7 SYSTEM-constraint compliance score ≥0.7 self-assessed by LLM, same threshold as Wave A § 4.4 W-A6).

**Reasoning:** 5 gates compose the substrate-grounding discipline (gates 2 + 3 + 5) with the player-facing quality discipline (gates 1 + 4). Length range tuned to player-readability AND headline-fit on mobile loadout app (~3-7 words = ~25-50 chars including spaces; fits a mobile header at locked register without truncation). Distinctness gate prevents "Season of the Storm" / "Season of the Stormbreak" / "Season of the Stormcaller" — the actually-observed substrate-similarity across seasons 001/002/003 (all storm-lightning-dominant) would otherwise produce variant naming collisions. Jaccard <0.5 on word-set is the operational test; falls back to regeneration with diversity-penalty preamble (same scaffold as Wave A regeneration).

### Q6 — LLM call sequencing (RESOLVED)

**Election:** Wave-S fires **POST-Wave-A + PARALLEL-OK with F-C + PRE-Wave-B**. Concrete sequence: Wave A → {Wave-S, F-C} parallel → Wave B (consumes Wave-S `{season_name}` as composition context in per-kit USER prompts).

**Reasoning:** POST-Wave-A is forced by Q1 input dependency (Wave A faction names ARE the primary substrate). PARALLEL-OK with F-C is enabled by no inter-dependency — F-C reads faction pairs; Wave-S reads faction aggregate; neither blocks the other. PRE-Wave-B is the design judgment call: kit names in Wave B are EXPERIENTIALLY downstream of season name (player reads season-name in loadout header, then kit-names on per-character tiles); composing `{season_name}` into the Wave B USER prompt enables Wave B to produce kit names that read as season-coherent rather than season-orthogonal. This adds ONE more substrate field to Wave B's prompt (no token-cost concern; Wave-S output is ~10 tokens). The alternative — Wave-S fires AFTER Wave B, decoupled — was rejected because it would force a regeneration loop if Wave-S surfaces season-name elements that contradict Wave B kit names already produced.

### Q7 — Composition with cascade-r4 architecture (RESOLVED)

**Election:** Wave-S sits at the player-names-experience layer (per designer-writes-substrate principle § 2.2 + § 4.4) consuming designer-writes substrate (Wave A faction outputs + element distribution + cultural lineage + Wanderer count) AS substrate-input. Composes with Amendment 1 via Q3 resolution (Wanderer count drives sub_narrative, not primary name). Composes with Amendment 2 via Q3 lexical hook (Wanderer-as-hero ALTERNATIVE pattern composes with season-name PATTERN). Composes with style register via Q2 isekai-canon-coded pattern lock + § 5 register acceptance gate. Composes with substrate-input purity precondition (Wave A § 2.5) — Wave-S USER prompt substrate-grounds in already-purified Wave A output; no fresh class-vocabulary leak surface.

**Reasoning:** Wave-S is structurally analogous to Wave A — it produces a thematic identity from substrate. The architectural difference is the COMPOSITION layer: Wave A composes from raw cluster substrate; Wave-S composes from Wave A faction outputs + season-aggregate substrate. The compositional pattern (substrate-input → cohesion-judge LLM → substrate-grounded player-facing name) is identical and inherits Wave A's discipline structures by construction.

### Q8 — Retroactive backfill (RESOLVED)

**Election:** Cache-key by `season_id`; retroactive execution = 3 calls for season_001/002/003; cost projection = ~$0.045 total (3 × ~$0.015/call, same per-call envelope as Wave A faction calls at 3-5K tokens). Rocket's retroactive-backfill execution authority; this spec defines the cache-key + cost envelope.

**Reasoning:** Season-name is season-stable (it does NOT change post-generation; a season's name is its name forever once landed). Cache-key by `season_id` enables idempotent re-fire safety + retroactive backfill without per-timestamp drift. Cost is trivially in-envelope.

### Q9 — Cycle 14 v1 close composition (RESOLVED)

**Election:** Wave-S unblocks drax loadout summary-tab full-surface (per-season tile header line + per-season caption). Composes with § 12 hero card by providing the season-name context line ("Stormveil Lightning Knight, marquee of the [Season Name]" — hero-card pattern per Amendment 2 § 12.1 + season-name pattern per Q2).

**Reasoning:** drax loadout summary tab is currently held on `season_name` placeholder; Wave-S retroactive backfill unblocks the surface for the existing 3 production seasons. § 12 hero card pattern depends on Wave A faction-name + Wave-S season-name + galadriel-drax hero election; Wave-S retroactive landing provides one of the three composition inputs. No new dependencies surfaced.

---

## § 2 Substrate inputs — canonical field list

| Substrate field | Source | Wave-S use | Provenance |
|---|---|---|---|
| `faction_name_set` | Wave A output × N factions per season | PRIMARY substrate; LLM extracts shared epithet / motif patterns | `phase5_faction_clusters.json` → `clusters[].faction_name` |
| `faction_thematic_tags_aggregate` | Wave A output flattened per season | PRIMARY substrate; thematic tag bag for compositional name fodder | `clusters[].faction_thematic_tags` flattened |
| `season_element_distribution` | Aggregated across all clusters' element_distribution, weighted by member_count | SECONDARY substrate; dominant element informs natural-vocabulary hooks (storm / ember / tide / shade) | Computed from `clusters[].element_distribution` weighted by `clusters[].member_count` |
| `season_modal_cultural_lineage` | Modal across cluster modal_cultural_lineage values, weighted by member_count | SECONDARY substrate; informs register / period flavor | Computed from `clusters[].modal_cultural_lineage` |
| `wanderer_count` | Count of SINGLETON `cluster_id` kits per Amendment 1 | TERTIARY substrate; modulates sub_narrative field only (not primary name per Q3) | Phase 5 PM-1 SINGLETON marker per Amendment 1 contract |
| `season_id` | Engine-internal identifier (e.g., `cycle-14-wave-5-season-001`) | Cache-key + provenance only; NOT name fodder | `metadata.season_id` |
| `pm1_algorithm` | PM-1 clustering algorithm tag | Provenance only | `metadata.pm1_algorithm` (if present; else null) |

**Substrate-purity precondition** (inherits Wave A § 2.5): all substituted substrate strings MUST be class-vocabulary-free per Discipline #45. Wave A output is post-cascade-resumption-3-S1 purified; Wave-S inherits this purity by construction.

**Element-vocabulary hook table** (Wave-S prompt-construction reference; supplements the THEMATIC_REGISTRY consumed at Wave A — not a NEW registry, but a vocabulary subset extracted from the registry for season-scale naming):

| Dominant element | Natural-vocabulary hooks (season-scale) |
|---|---|
| lightning | Storm / Stormveil / Stormbreak / Thunderkeep / Skybreak / Galelight |
| fire | Ember / Ashfield / Pyrefall / Ember-Forge / Cinderveil |
| earth | Stonebound / Earthen / Bastion / Mountainwake / Boulderfall |
| water | Tide / Tidewreath / Deepveil / Currentbound / Brinekeep |
| wind | Gale / Galebound / Skytide / Aetherwake / Windveil |
| holy | Dawnlight / Lightbound / Sunken-Choir / Vesperveil |
| shadow | Umbra / Tidal-Umbra / Shadehold / Nightveil / Pall-Reach |

The LLM is NOT constrained to this table; it's a vocabulary anchor showing the genre-register the registry's per-cell entries occupy at the season scale. Compositional flexibility preserved.

---

## § 3 Player-facing pattern — the form a season name takes

**Pattern A (PRIMARY):** `Season of the [substrate-derived noun phrase]`
- Example shape: `Season of the Stormveil Convergence`
- Word count: 5 (within 3-7 gate)
- Isekai-canon-coded: ✅ (Solo Leveling / Re:Zero / Mushoku Tensei volume-title precedent)
- Composes with sub_narrative: "Season of the Stormveil Convergence — marked by a single Lone Wanderer who walks the storm alone."

**Pattern B (ALTERNATE):** `The [substrate-derived noun phrase]`
- Example shape: `The Stormveil Reckoning`
- Word count: 3 (within gate)
- Genre-coded: PoE league-naming convention + ARPG-mainstream-coded
- Composes with sub_narrative: "The Stormveil Reckoning — marked by two Wanderers who refused faction binding."

**Pattern selection:** LLM chooses A vs B per substrate composition fit. Acceptance gate W-S2 enforces output matches one of the two patterns (regex `^(Season of the |The )[A-Z][a-z]+( [A-Z][a-z]+){1,4}$` permissive; LLM-self-assessed register score backstops the regex).

**What gets ruled out:**
- Year-prefix patterns (`Year of the X`) → too WoW-coded; rejected by SYSTEM constraint
- Possessive patterns (`X's Reign`) → too proper-noun-centric; rejected
- Numbered season labels (`Season 1: X`) → too MMO-coded; engine-internal `season_id` already covers numbering; player-facing name doesn't repeat it
- Free LLM dialogue (`This is the season where...`) → D7 violation; rejected by SYSTEM constraint

**Per-embodiment / per-form awareness:** the season name is form-agnostic at the linguistic layer; it names the seasonal envelope (substrate), not the player's specific embodiment. The Wanderer sub_narrative may reference Wanderer-form-substrate when the galadriel-drax pair elects Wanderer-as-hero (Amendment 2 § 12.1 ALTERNATIVE pattern); the primary season name remains substrate-aggregate-grounded.

---

## § 4 Prompt template — Wave-S system + user

### § 4.1 SYSTEM prompt (~110 words)

```
You are a thematic season-namer for an isekai-genre ARPG.

Your task: produce a single SEASON NAME for an entire seasonal arc, composed
from substrate evidence aggregated across the season's emergent factions.

CRITICAL CONSTRAINTS

(1) The season name MUST derive from the supplied substrate — faction names,
    thematic tags, dominant element, cultural lineage. Do NOT invent new
    thematic vocabulary.

(2) Output MUST match one of two patterns exactly:
       PATTERN A:  "Season of the {NounPhrase}"   (3-7 words total)
       PATTERN B:  "The {NounPhrase}"             (3-5 words total)
    Choose whichever pattern the substrate composition fits more naturally.

(3) The {NounPhrase} MUST reference at least TWO substrate signals — at
    minimum one faction-name epithet AND one thematic-tag OR element hook.

(4) Cross-cultural neutrality: lineage signals register tone via supplied
    substrate, never via stereotype.

(5) AVOID AI-tell phrases: "Era of", "Age of", "Chronicles of", "Saga of",
    "Mystical X", "Sacred X", "Ancient X", "Forgotten X", "Eternal X",
    "Reign of", "Behold the". Substrate-grounded phrases instead.

(6) Self-assess ai_tell_compliance_score (0.0-1.0); ≥0.7 to pass.

(7) Respond with valid JSON only. No markdown fences. No preamble.
```

### § 4.2 USER prompt (~140 words template; substrate-filled per season)

```
SEASON_SUBSTRATE_AGGREGATE (weighted HIGHEST):
  season_id: {season_id}
  faction_count: {faction_count}
  faction_names: {faction_name_set}
  faction_thematic_tags: {faction_thematic_tags_aggregate}

SEASON_ELEMENT_PROFILE:
  dominant_element: {dominant_element}
  element_distribution: {season_element_distribution_compact}

SEASON_LINEAGE_PROFILE:
  modal_cultural_lineage: {season_modal_cultural_lineage}

WANDERER_PROFILE:
  wanderer_count: {wanderer_count}

PRIOR_SEASON_NAMES (distinctness check):
  {prior_season_names_list_or_none}

OUTPUT SCHEMA (respond with this JSON shape only):
{
  "season_name": "<3-7 words; PATTERN A or PATTERN B per SYSTEM constraint 2; ≥2 substrate signals per constraint 3>",
  "pattern_used": "<'A' or 'B'>",
  "substrate_signals_referenced": ["<faction-epithet or tag or element or lineage>", "<second signal>", "..."],
  "season_sub_narrative": "<null if wanderer_count==0 else 1 sentence referencing Wanderer count; substrate-grounded; uses season_name + Wanderer phrase>",
  "ai_tell_compliance_score": <0.0-1.0>
}
```

**Combined SYSTEM + USER token estimate:** ~250 words / ~340 tokens / well within ≤250-word combined-prompt target after substrate substitution; LLM output ~50 tokens; total per-call ~400 tokens. At Anthropic Sonnet pricing ~$0.015/call within Wave A envelope.

---

## § 5 Acceptance gates

| # | Gate | Verification |
|---|---|---|
| W-S1 | `season_name` is 3-7 words (Pattern A) OR 3-5 words (Pattern B) | string split; word count per pattern_used |
| W-S2 | `season_name` matches one of two patterns | regex `^(Season of the [A-Z][a-z]+( [A-Z][a-z]+){1,4}\|The [A-Z][a-z]+( [A-Z][a-z]+){1,3})$` |
| W-S3 | ≥2 substrate signals referenced | `substrate_signals_referenced` list length ≥2; each entry substring-matches input substrate fields |
| W-S4 | No AI-tell phrase substring match | grep against SYSTEM constraint 5 ban-list (case-insensitive) |
| W-S5 | No prohibited Discipline #45 vocabulary | grep `\b(class\|warrior\|mage\|rogue\|hunter\|paladin)\b` (case-insensitive) |
| W-S6 | `ai_tell_compliance_score` ≥ 0.7 | numeric ≥0.7; <0.7 triggers regeneration per Wave A scaffold pattern; max 1 regeneration |
| W-S7 | Distinctness from prior season names | Jaccard distance on lowercased word-sets ≥0.5 vs each prior season name in `PRIOR_SEASON_NAMES` |
| W-S8 | Substrate-input purity precondition | all substituted variables grep-clean for class-vocabulary substrings (Wave A § 2.5 pattern inherited) |
| W-S9 | `season_sub_narrative` discipline | null when wanderer_count==0; ≤1 sentence + references wanderer count when wanderer_count≥1 |
| W-S10 | Register coherence (isekai-canon-coded) | LLM-self-assessed via score W-S6 above; manual spot-check at first 3 retroactive outputs (Matt-surface if any fails) |

**Regeneration discipline:** matches Wave A § 4.6 — max 1 regeneration per call on W-S6 fail; on second fail, surface to knight-rider for Matt-surface (not a silent fallback; season-name is high-trust real-estate).

**Distinctness gate edge case:** if W-S7 fails on regeneration, the orchestrator passes a `diversity_penalty_preamble` to the regenerated SYSTEM prompt (matches Wave A diversity-penalty pattern), with prior season names enumerated for the LLM's avoid-list.

---

## § 6 LLM call sequencing — Wave-S in Phase 5

**Existing sequence (per phase-5-llm-prompts-cohesion-judge-2026-05-27.md § 1):**

```
PM-1 cluster output ──→ Wave A ──→ F-C ──→ Wave B
```

**Wave-S extension:**

```
PM-1 cluster output ──→ Wave A ──→ {Wave-S, F-C} (parallel) ──→ Wave B
                                       ↓
                                       ↓ {season_name} consumed by Wave B
                                       ↓   as composition context field
                                       ↓
                                       Wave B per-kit prompts include
                                       {season_name} in USER prompt
                                       SEASON_CONTEXT block (NEW field)
```

**Volume per season:** ONE Wave-S call (k-invariant; one season → one name). Cost contribution: ~$0.015/season. Total Phase 5 per-season cost: was ~$0.55-$1.55 (Wave A + F-C + Wave B); now ~$0.57-$1.57 (Wave A + Wave-S + F-C + Wave B). Cost delta trivial.

**Wall-clock impact:** Wave-S parallel-OK with F-C means NO wall-clock-cost added — Wave-S fires concurrently with F-C; both wait on Wave A completion. Wave B gates on Wave-S completion (was already gating on Wave A; gates on `max(Wave-S, F-C)` now instead — Wave-S typically completes faster than F-C since k=1 call vs k×(k-1)/2 calls).

**Orchestrator hook:** star-lord Seam 2 extends `phase5_orchestrator.py` to add Wave-S as a new method post-Wave-A, parallel-fired-with-F-C via existing asyncio Semaphore(10) infrastructure. Implementation detail (NOT in scope of this spec) — rocket + star-lord coordination per § 9.

---

## § 7 Composition — Amendment 1 + 2 + designer-writes-substrate + style register

### § 7.1 Composition with Amendment 1 (Wanderer architecture)

Per Q3 + Q5 W-S9 + § 4.2 USER prompt: Wanderer count is composed into the `season_sub_narrative` field ONLY, NOT the primary `season_name`. SINGLETON `cluster_id` per Amendment 1 means Wanderers are substrate-elected non-faction kits; they remain visible in the season's narrative surface via sub_narrative without coupling primary name to RNG-variable Wanderer count.

**Example compositions:**
- `wanderer_count == 0` → `"season_sub_narrative": null`
- `wanderer_count == 1` → `"season_sub_narrative": "Season of the Stormveil Convergence — marked by a single Lone Wanderer who walks the storm unbound."`
- `wanderer_count == 2` → `"season_sub_narrative": "Season of the Stormveil Convergence — marked by two Wanderers who refused all faction binding."`

The sub_narrative composes lexically with the season name; the season name is stable across Wanderer-count variants.

### § 7.2 Composition with Amendment 2 (§ 12.1 galadriel-drax hero pair)

Per Q3 + Q9 + § 4.2: when the galadriel-drax pair elects a Wanderer-as-hero ALTERNATIVE (Amendment 2 § 12.1 pattern), the hero-card narrative composes:

`{Wanderer-substrate-identity} of the {season_name}`

Example: `"Lone Wanderer of the Stormveil Convergence"` — composes Amendment 2's hero-card pattern with Q2's season-name pattern (PATTERN A in this example). The hero-card pattern is NOT in this spec's scope (drax + galadriel author); Wave-S provides the substrate-honest season-name surface that hero-card composition consumes.

When the pair elects the DEFAULT faction-hero pattern (not Wanderer-as-hero), composition is `{Faction-Hero-Name}, marquee of the {season_name}` — same season-name surface, different hero composition. Wave-S is hero-election-agnostic; both compositions consume the same season_name field.

### § 7.3 Composition with designer-writes-substrate principle

Per the principle § 2.1 (designer-writes-substrate layer) + § 2.2 (player-names-experience layer) + § 4.4 (Wave A/B Cycle 15+ extension to compose both layers): Wave-S sits at the player-experience layer post-emergence. The substrate the engine has WRITTEN (BC tuples + cultural lineage + element + Phase 2-5 cascade) is what Wave A consumed; Wave-S consumes Wave A's output as already-substrate-coherent input. The season name IS player-naming-the-experience (in this case, the cohesion-judge LLM is the proxy for the eventual community player vocabulary; v1 ships with LLM-mediated player-facing naming; Cycle 15+ may layer community-validated player-experience vocabulary atop or replace).

Wave-S is therefore a **Cycle 14 v1 commitment to LLM-mediated player-naming at the season-scale** — substrate-honest (composed from Wave A faction outputs that were themselves substrate-honest by transitivity), with the player-experience-archetype extension target deferred to Cycle 15+ per the principle's § 4.4 extension framing.

### § 7.4 Composition with style register lock

Per Q2 + Q5 W-S10 + style-register.md isekai-coded register lock: Wave-S output language ("Season of the X" / "The X") is isekai-canon-coded by selection — Solo Leveling / Re:Zero / Mushoku Tensei / PoE-mainstream-coded patterns explicitly. The HD-2D pixel-art register at the visual layer is paired with isekai-canon-coded naming at the linguistic layer; the two reinforce each other in player-trust. Star-lord's visual_prompt downstream consumption (per style-register.md § "What this locks operationally" → Star-lord) can compose the season_name into LLM image-generation prompts as additional thematic context for season-specific Court / Trial cinematic frames.

### § 7.5 Composition with substrate-input purity precondition (Wave A § 2.5)

Wave-S USER prompt substrate-substitutes the following fields:
- `{faction_name_set}` (Wave A output; post-S1-purified)
- `{faction_thematic_tags_aggregate}` (Wave A output; post-S1-purified)
- `{dominant_element}` (substrate-curated; clean)
- `{season_modal_cultural_lineage}` (substrate-curated; clean)
- `{wanderer_count}` (integer; clean)
- `{season_id}` (engine internal; clean)
- `{prior_season_names_list_or_none}` (Wave-S prior output; recursive purity by induction; base case clean)

All substituted values inherit Wave A's post-S1 substrate-input purity. No fresh class-vocabulary leak surface introduced. W-S8 runtime grep is the defensive layer matching Wave A W-A10 pattern.

---

## § 8 Retroactive backfill plan

**Scope:** 3 seasons (cycle-14-wave-5-season-001/002/003) currently have NO season_name. Wave-S retroactive backfill provides season_name for all three.

**Cost projection:** 3 calls × ~$0.015/call = ~$0.045 total. Well within Phase 5 envelope (existing per-season cost ~$0.55-$1.55; adding $0.015/season is <3% delta).

**Cache-key:** `season_id` (e.g., `cycle-14-wave-5-season-001`). Idempotent re-fire safety; same season_id → same cache key → same Wave-S call (or cache-hit on second invocation).

**Execution authority:** rocket (orchestrator integration) + star-lord (LLM call wiring); execution happens AFTER this spec lands + AFTER star-lord implements Wave-S in `phase5_orchestrator.py`. Spec authorship + execution are decoupled per CLAUDE.md addendum + per cascade-r4 routing.

**Backfill ordering:** season_001 first (no prior_season_names → empty list); season_002 second (prior_season_names = [season_001 name]); season_003 third (prior_season_names = [season_001, season_002 names]). This ordering enables the W-S7 distinctness gate to operate retroactively in chronological substrate order, producing a forward-coherent name set.

**Output target:** rocket writes Wave-S output into the existing `phase5_faction_clusters.json` metadata block (extends `metadata` with `season_name`, `pattern_used`, `substrate_signals_referenced`, `season_sub_narrative`, `wave_s_fired`, `wave_s_cost_usd`) OR into a sibling file `phase5_season_name.json` per rocket's existing-schema preference (rocket's decision; both are valid; spec is schema-agnostic).

**Drax data-contract update:** drax loadout app data layer consumes `season_name` from whichever target rocket writes; drax follow-on dispatch carries the data-contract authoring (NOT this spec's scope per cascade-r4 routing).

---

## § 9 Forward-fix integration — rocket + star-lord coordination

**Star-lord scope** (LLM-call seam):
1. Extend `phase5_orchestrator.py` with new `_wave_s_call()` method per § 4 prompt template
2. Fire Wave-S parallel-with-F-C post-Wave-A per § 6 sequencing
3. Implement W-S1..W-S10 acceptance gates per § 5 (mirrors Wave A W-A1..W-A10 patterns)
4. Implement runtime substrate-purity grep at call-construction per W-S8 (same pattern as Wave A W-A10)
5. Cost monitoring + telemetry sidecar emission per existing Wave A pattern

**Rocket scope** (orchestration + schema):
1. Extend `ExportFactionCluster` schema OR new `ExportSeasonName` schema with Wave-S output fields (rocket's call; both valid)
2. Wire `{season_name}` substitution into Wave B USER prompt SEASON_CONTEXT block per § 6 (NEW Wave B field)
3. Execute retroactive backfill for season_001/002/003 per § 8 plan
4. MIGRATION.md entry per ADR-004 if schema change touches downstream consumers

**Cross-seam handoff sequencing:** star-lord implements Wave-S call surface FIRST (no schema dependency); rocket integrates schema + Wave B SEASON_CONTEXT field SECOND (consumes star-lord's surface); rocket executes retroactive backfill THIRD (uses both seams complete). Per CLAUDE.md addendum, all three steps are within-cycle authorized; no fresh Matt re-asking required between steps.

**Gate-2 surface (jack-ryan):**
- Substrate-input purity grep at call-construction (W-S8) NOT bypassed by star-lord implementation
- D-Sharpened invariance preserved — no `substrate_anchored_personage` field exposed to Wave-S prompt
- Discipline #45 vocabulary check on Wave-S output (W-S5)
- Pattern A / Pattern B regex match (W-S2) actually fires on output
- Retroactive backfill produces 3 distinct names (W-S7) on first execution

---

## § 10 Cycle 14 v1 close composition

**Drax loadout summary tab full-surface unblock:** prior state was per-season tile showing faction tiles + Wanderer placeholder slot + "Season Name TBD" header placeholder (cascade-r4 § 11 drax Track B reported this surface as PARTIALLY-shipped pending season-name landing). Wave-S retroactive backfill provides season_name; drax data-contract update consumes; summary-tab header line lands as e.g.:

```
┌─────────────────────────────────────────────────────────┐
│  Season of the Stormveil Convergence                     │
│  4 factions · 1 Wanderer · 34 kits                       │
│                                                          │
│  [faction tile 1] [faction tile 2] [faction tile 3]      │
│  [faction tile 4]                                        │
│                                                          │
│  Lone Wanderer of the Stormveil Convergence:             │
│  [Wanderer kit tile]                                     │
└─────────────────────────────────────────────────────────┘
```

**§ 12 hero-card composition:** per Amendment 2 § 12.1 galadriel-drax hero election (DEFAULT faction-hero pattern OR ALTERNATIVE Wanderer-as-hero pattern), hero-card narrative line composes:

- DEFAULT: `[Hero Faction Name] · [Hero Kit Name] · marquee of the [season_name]`
- ALTERNATIVE: `Lone Wanderer · [Wanderer Kit Name] · of the [season_name]`

Both compositions consume Wave-S `season_name` as the trailing substrate-honest seasonal-context anchor. Hero card visual layer (galadriel-drax authorship) composes the season_name into the card design.

**§ 12 Matt Meshy handoff composition:** when drax surfaces the hero card + image-generation prompt to Matt for Meshy invocation, the prompt template includes `season_name` as thematic context: `"isekai-genre ARPG hero portrait of [Hero], marquee character of the [season_name], hand-drawn pixel-art HD-2D style..."` — composes Wave-S output with style-register.md § "What this locks operationally" → Star-lord visual prompt pattern.

---

## § 11 Worked examples — 3 season names from existing substrate

Sanity-check: do the spec's gates + pattern + substrate inputs actually produce GOOD names for the 3 existing production seasons? Substrate per `phase5_faction_clusters.json` inspection:

### Example 1 — season_001 (4 clusters; lightning-storm dominant; european + fantasy_generic mix)

**Substrate aggregate:**
- `faction_names`: ["Stormground Chain Wardens", "Stormbreak Vanguard", "Stormveil Thunderkeep", "Ashfield Ember Wardens"]
- `faction_thematic_tags_aggregate`: ["earth-lightning convergence", "chain-strike ranged", "medieval pragmatism", "multi-element convergence", "close-range AOE", "medieval combatant", "lightning-dominant", "medieval-european", "close-range-AOE", "fire-spread", "ranged-immolation", "medieval-pyrotactics"]
- `dominant_element`: lightning (~30% weighted) with secondary fire + earth
- `season_modal_cultural_lineage`: fantasy_generic (3 of 4 clusters)
- `wanderer_count`: 0

**Spec-produced season name (Pattern A; LLM-simulated output per § 4 prompt + § 5 gates):**

```json
{
  "season_name": "Season of the Stormveil Convergence",
  "pattern_used": "A",
  "substrate_signals_referenced": ["Stormveil (faction epithet)", "multi-element convergence (thematic tag)", "lightning (dominant element)"],
  "season_sub_narrative": null,
  "ai_tell_compliance_score": 0.85
}
```

**Gate verification:** W-S1 ✅ 5 words within 3-7. W-S2 ✅ Pattern A. W-S3 ✅ 3 signals (Stormveil + Convergence + lightning). W-S4 ✅ no AI-tell. W-S5 ✅ no Discipline #45 vocab. W-S6 ✅ 0.85≥0.7. W-S7 ✅ first season, no prior. W-S8 ✅ substrate clean. W-S9 ✅ null sub_narrative (wanderer_count==0). W-S10 ✅ isekai-canon-coded.

### Example 2 — season_002 (4 clusters; lightning + shadow + earth tri-storm; european dominant)

**Substrate aggregate:**
- `faction_names`: ["Tricast Siege Wardens", "Stormbreak Earthen Vanguard", "Gale and Tide Wardens", "Stormveil Chain Wardens"]
- `faction_thematic_tags_aggregate`: ["tri-element bombardment", "medieval ranged warfare", "large-area denial", "lightning-earth duality", "close-range AOE pressure", "medieval European martial", "multi-element convergence", "wide-arc combat", "elemental generalism", "chain-discharge", "lightning-shadow-duality", "ranged-cascade"]
- `dominant_element`: lightning (~38% weighted) with strong shadow + earth secondaries
- `season_modal_cultural_lineage`: european (split with fantasy_generic; european plurality)
- `wanderer_count`: 0

**Spec-produced season name (Pattern A or B; LLM elects A here for substrate weight):**

```json
{
  "season_name": "Season of the Tricast Siege",
  "pattern_used": "A",
  "substrate_signals_referenced": ["Tricast (faction epithet)", "tri-element bombardment (thematic tag)", "lightning-earth duality (thematic tag)"],
  "season_sub_narrative": null,
  "ai_tell_compliance_score": 0.82
}
```

**Gate verification:** W-S1 ✅ 5 words. W-S2 ✅ Pattern A. W-S3 ✅ 3 signals. W-S4 ✅ no AI-tell. W-S5 ✅ clean. W-S6 ✅ 0.82≥0.7. **W-S7 ✅ Jaccard vs season_001 ("Season of the Stormveil Convergence"): shared {"Season", "of", "the"} = 3 words; total unique = {Season, of, the, Stormveil, Convergence, Tricast, Siege} = 7 words; Jaccard = 3/7 ≈ 0.43; distance = 0.57 ≥ 0.5 ✅ PASS.** W-S8 ✅ clean. W-S9 ✅ null. W-S10 ✅ isekai-coded.

### Example 3 — season_003 (3 clusters; storm-shadow blend; fantasy_generic + european)

**Substrate aggregate:**
- `faction_names`: ["Stormcaller Vanguard", "Chain-Strike Stormcallers", "Tidal Umbra Wardens"]
- `faction_thematic_tags_aggregate`: ["storm-convergence", "broad-front-assault", "sky-and-earth-duality", "chain-propagation", "storm-ranged", "multi-element", "shadow-water convergence", "area suppression", "medieval ranged doctrine"]
- `dominant_element`: lightning + shadow + water roughly balanced
- `season_modal_cultural_lineage`: fantasy_generic (2 of 3 clusters)
- `wanderer_count`: 0

**Spec-produced season name (Pattern B for variety + substrate fit; LLM elects B because faction names already have "Storm" prefix — Pattern A "Season of the Storm-X" would risk W-S7 distinctness fail vs season_001's "Stormveil Convergence"):**

```json
{
  "season_name": "The Tidal Umbra Reckoning",
  "pattern_used": "B",
  "substrate_signals_referenced": ["Tidal Umbra (faction epithet)", "shadow-water convergence (thematic tag)", "area suppression (thematic tag)"],
  "season_sub_narrative": null,
  "ai_tell_compliance_score": 0.88
}
```

**Gate verification:** W-S1 ✅ 4 words within 3-5 (Pattern B). W-S2 ✅ Pattern B. W-S3 ✅ 3 signals. W-S4 ✅ no AI-tell. W-S5 ✅ clean. W-S6 ✅ 0.88≥0.7. **W-S7 distinctness checks:**
- vs season_001 "Season of the Stormveil Convergence": shared {The} only (case-folded); Jaccard ~1/8 ≈ 0.13; distance 0.87 ✅
- vs season_002 "Season of the Tricast Siege": shared {The} only; Jaccard ~1/8 ≈ 0.13; distance 0.87 ✅
W-S8 ✅ clean. W-S9 ✅ null. W-S10 ✅ isekai-coded.

### Examples sanity-check observation

The three names READ as isekai-genre-native AND substrate-honest AND mutually distinct. The substrate-grounding is recoverable from the names: "Stormveil Convergence" traces back to season_001's storm-lightning + multi-element clusters; "Tricast Siege" traces back to season_002's tri-element bombardment Tricast faction; "Tidal Umbra Reckoning" traces back to season_003's shadow + water Tidal Umbra Wardens faction. A player who sees the name in the loadout header can intuit something true about the season's substrate identity WITHOUT explanation. This is the success criterion.

**Failure modes the spec prevents** (counterfactual sanity-check):
- Generic name "Season of Storms" — would FAIL W-S3 (only 1 substrate signal: storms; faction epithet not referenced) and W-S7 vs season_002 + 003 on distinctness
- AI-tell name "Era of the Forgotten Lightning" — would FAIL W-S4 (banned phrases "Era of" + "Forgotten")
- Class-vocab leak "Season of the Storm Warrior" — would FAIL W-S5 (warrior banned per Discipline #45)
- Same-as-faction name "Season of the Stormveil Thunderkeep" — would technically PASS W-S1/2/3 but the sub_narrative+hero-card composition would collide lexically with faction-tile + hero-card; substrate-aware spec discourages via SYSTEM constraint 1 ("aggregated across the season's emergent factions") which steers the LLM toward season-scale aggregation rather than faction-echo

---

## § 12 Open items + Cycle 15+ deferred

**In-scope (this spec resolves):** all 9 design questions per § 1.

**Deferred to Cycle 15+ (per designer-writes-substrate § 4.4 extension framing):**
- Wave-S Cycle 15+ extension to consume community-validated player-experience-archetype vocabulary (Bossing / Speedfarming / Endgame Generalist) as composition input — pending ARPG community research sprint findings per the principle's § 4.5
- Wave-S register-pivot resilience — if Matt ever pivots style register from HD-2D-pixel-art to a different register, Wave-S vocabulary hooks (§ 2 element-vocabulary table) may need register-coherent re-curation (catalogue is score-don't-filter per style-register.md § "Pivot insurance"; same applies here)

**Out of scope (delegated per cascade-r4 routing):**
- Wave-S implementation (star-lord); orchestrator integration (rocket); retroactive execution (rocket); cache infrastructure (star-lord); drax data-contract authoring (drax follow-on)

---

## § 13 Sign-off

**Authored:** gandalf (story-and-design steward) per Matt 2026-05-29 verbatim cascade-r4 follow-on authorization under hive-mind decision-routing.

**For:** the durable canonical capture of the season-itself naming design (Wave-S as the fourth Phase 5 LLM call surface) — composing Wave A faction outputs + season-aggregate substrate + Wanderer count into substrate-honest player-facing season names per the designer-writes-substrate / player-names-experience principle and the locked HD-2D pixel-art / isekai-canon-coded style register.

**Empirical substrate verification:** 3 worked examples per § 11 confirm the spec produces good names from existing season_001/002/003 substrate; all 10 acceptance gates verifiable on the worked examples.

**Composition target:** Wave-S implementation by star-lord; orchestrator integration + retroactive backfill by rocket; drax data-contract update + summary-tab + § 12 hero-card composition by drax. Engine first. Game second. Phase third.

**Tag target:** `gandalf/v1.0-wave-s-season-naming-spec-1`
