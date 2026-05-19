# R8 — Theme-Coalescence Prompt (Inverted Pipeline)

**Authority:** gandalf (story-and-design steward) under autonomous-operation authority.
**Status:** **Canonical methodology asset** for R8 inverted-pipeline A/B run. Authored before A/B run kicks off, per protocol § 5.4 R8 activation requirements and dispatch § "Gandalf authoring (before A/B run starts)".
**Workstream:** R8 — Season-as-Emergent-Output (the science experiment).
**Companion:** `agentic_orchestration/hive-mind/R8-cohesion-judging-protocol-2026-05-19.md` (the judging side of the methodology).
**Dispatch:** `agentic_orchestration/dispatches/2026-05-19-rocket-plus-star-lord-plus-gandalf-R8-season-as-emergent-output.md`.
**Mission canonical:** `canonical/story/engine-rebuild-2026-05-19-gap-solutions-and-tests.md` § 8.

---

## § 0 — TL;DR

The **inverted pipeline** runs mechanical generation first (no theme-as-input, no anchor-as-input, no cosmological-vocabulary-as-input), converges class + monster + gear + trial content on pure substrate-mechanic combinations, then makes **one** post-convergence LLM call that reads the converged content and coalesces:

1. **`anchor_name`** — the place the season is *of* (e.g., "The Subterranean City of the Dead", "The Border Wall")
2. **`anchor_category`** — high-level archetype from the existing anchor taxonomy (underworlds_and_below / liminal_boundaries / royal_courts / etc.)
3. **`season_theme_element`** — the per-season element name (the LLM-visible vocabulary token, e.g., "char", "pitch", "brand") that the converged content's dominant substrate carries
4. **`slot_fills`** — the 8-slot cosmological-vocabulary fill (ignition / suffusion / bulwark / displacement / impact / radiance / penumbra / resonance)
5. **`pair_rationales`** — the three pair-axis rationales (thermal, position, luminance) that articulate WHY the slot fills cohere as a set

This single call **REPLACES** the ~317 input-driven LLM calls per season under the baseline pipeline. The naming of skills, monsters, gear, classes happens via the coalesced vocabulary distributed back through templates, NOT through per-entity LLM calls. (Star-lord's LLM-orchestration design owns that distribution mechanism — this prompt is the upstream input.)

**Design intent:** the prompt is engineered for **cohesion**, not novelty. The mechanical convergence has already done the variety-producing work; the LLM's job is to *recognize the pattern that's already there* and **name** it with discipline. Low temperature; structured JSON output; one anchor among many candidates; the LLM commits.

**Deterministic-friendly so Test 5 multi-shot stability is fair:** temperature 0.3; deterministic seed if the API supports it; same system prompt across all three Test-5 shots; same input payload.

---

## § 1 — Why this prompt looks the way it does

### § 1.1 — Cohesion is the load-bearing job

The baseline pipeline derives cohesion from a *declared* anchor + cosmological vocabulary that constrains downstream content. Everything names against the same root. Cohesion is enforced at every name-it call.

The inverted pipeline doesn't have that scaffolding. The mechanical convergence produces classes / monsters / gear / trial WITHOUT thematic constraint. The coalescence call is the **only** moment the season's thematic identity gets imposed — and it must do so by *reading* what's already there, not by *imposing* what it would prefer.

Consequences for prompt structure:
- Heavy emphasis on **reading the data** (element distribution, dominant substrate, archetype mix, geometry distribution, role distribution) before naming
- Explicit anti-novelty instruction (do NOT introduce themes not present in the data; do NOT favor exotic anchors when boring ones fit better)
- Structured output that forces the LLM to **commit** to one anchor, one element name, one set of 8 slot fills — no candidate lists, no hedging
- Rationale fields required (`pair_rationales`) — the LLM must articulate *why* the chosen vocabulary coheres, which prevents lazy convergence on memorized templates

### § 1.2 — Substrate identity must be preserved (Test 4 instrument)

Test 4 (substrate-identity invariance) asks: *does the LLM's coalescence preserve substrate identity, or does it discover unexpected groupings?* For Test 4 to produce a clean signal, the prompt must NOT pre-bias the LLM toward "discover new substrate identities." It must ask the LLM to find the dominant substrate honestly from the data.

If invariance holds, Test 4 passes: the data carries substrate identity inherently.
If non-invariance surfaces, Test 4 produces a discovery: the LLM names velocity / impact / time-pressure where we expected fire. **Either result is informative — but only if the prompt doesn't tip the scale.**

Consequence: the prompt instructs the LLM to identify the dominant substrate from the converged content's `dominant_element` distribution + skill geometry/effect-category distribution. It does NOT instruct the LLM to "find a more interesting frame than substrate." If substrate is what the data says, substrate is what comes out.

### § 1.3 — Why one call, not multi-call

The dispatch open-question (§ "Open questions for the agents to resolve") asks: *single-call vs multi-call (e.g., one for element, one for cosmology, one for naming)?*

**Decision: single call.** Rationale:

1. **Cost discipline.** R8 Test 3 success criterion is ≥ 75% LLM-call reduction. One call beats three calls.
2. **Coherence enforcement.** A single LLM context produces an internally-coherent answer (anchor + element + slot fills all visible to each other during generation). Multi-call risks the element-call producing "char" and the anchor-call producing "Music Spirit Forest" — incoherent set.
3. **Multi-shot stability (Test 5).** Multi-call expands the multi-shot stability surface: Jaccard overlap must hold across N calls × 3 shots = 3N outputs. Single call is 3 outputs total — cleaner stability measurement.
4. **Operational simplicity.** Star-lord's LLM-orchestration design at one call is materially simpler than at three. Less retry / partial-failure handling.

Trade-off: the single call is **larger** — both prompt tokens (whole converged-content summary) and response tokens (whole structured output). This trade is acceptable; Sonnet handles context windows of this size without degradation, and the per-call cost is still vastly cheaper than 3 calls or 317 calls.

### § 1.4 — Per-entity naming is NOT in this prompt

The baseline pipeline calls the LLM ~317 times per season because EVERY skill, monster, class, trial, and gear item gets its own naming call. The inverted pipeline's coalescence call produces the **vocabulary** (the `slot_fills` + element name + anchor) but does NOT produce per-entity names directly.

How does per-entity naming work under inverted pipeline? **Template-based distribution from the coalesced vocabulary.** Star-lord's LLM-orchestration changes (under R8) own this mechanism. The rough shape:

- Class names: template-composed from `(class.archetype_tag → mode-of-action label) + (class.dominant_element → seasonal element name) + (anchor.category → role-of-actor noun)`. E.g., "Undercity Cremator" = (fire_controller → ignition-mode) + (char → cremator/ash-tender) + (underworlds_and_below → undercity-dweller).
- Skill names: composed from `(skill.geometry_type → action verb from grouping label) + (skill.canonical_element → seasonal element name)`. E.g., "Pyre Debt Settled" = (ground_targeted_circle → "settled/laid-down" verb) + (char → "pyre debt" noun phrase from coalesced vocab).
- Monster names: similar template against monster archetype + dominant element.
- Trial / gear: similar template; epic/legendary may still warrant a small LLM-pass for flavor enrichment if star-lord's cost budget allows.

**The R8 hypothesis is that the coalesced vocabulary is RICH ENOUGH that template-distribution produces names indistinguishable in cohesion from per-entity LLM calls.** This is the load-bearing claim. If templates produce robotic names ("Pyre-Debt-Skill-1", "Pyre-Debt-Skill-2"), the cohesion test will catch it. If templates produce evocative names that read as authored (as they did in the baseline outputs we've seen), the hypothesis holds.

The coalescence prompt's job is to give star-lord's template distribution enough material to work with. That's why the `slot_fills` field is 8 entries (one per grouping slot) and `pair_rationales` provide narrative connective tissue — the templates can sample these strings to compose names that feel like one author wrote them.

---

## § 2 — The prompt (canonical form)

Below is the prompt text in full. Star-lord's LLM-orchestration implementation will wrap this in the `TrackedLLMClient` call infrastructure with `purpose: "theme_coalescence"` for telemetry purposes.

### § 2.1 — System prompt

```
You are the cosmological-vocabulary coalescer for an ARPG seasonal-generation engine.

Your job: read the converged mechanical content of one season (classes, monsters, gear, trial, geometry distribution, element distribution, role distribution) and produce ONE coherent cosmological vocabulary that names what this season IS.

You are NOT inventing the season. The season has already been generated. Its substrate identity, its mechanical signature, its dominant patterns are already present in the data. Your job is to RECOGNIZE the pattern and NAME it with discipline.

Discipline rules:

1. READ FIRST. Identify the dominant element (most common across classes + monsters + skills). Identify the dominant geometry families (what shapes does this season's combat take). Identify the role distribution (how many controllers vs damage-dealers vs hybrids). Identify the anchor candidates by looking at what kind of PLACE this content suggests — underworld, citadel, wilderness, threshold, sanctum.

2. NAME WHAT IS THERE. Do NOT introduce themes not supported by the data. If the data is fire-heavy with burial/decay/preservation motifs in the skill flavor and necrotic monster archetypes, the anchor is a necropolis or crypt or underworld — not a music-spirit forest. The data has already chosen.

3. COMMIT. You will produce exactly ONE anchor, ONE element name (the seasonal-element token), ONE set of 8 slot fills, and the three pair rationales. No alternatives. No hedging. The season has one identity; surface it.

4. COHERE. Every name you produce must read as having one author. The anchor, the element name, the 8 slot fills, and the three pair rationales must all sound like one voice telling one story. If you find yourself producing "Pyre Debt" for ignition and "Music Wave" for suffusion, you are not cohering — back up and find shared register.

5. PRESERVE SUBSTRATE IDENTITY. The 8 slots correspond to canonical substrates (ignition=fire, suffusion=water, bulwark=earth, displacement=wind, impact=physical, radiance=holy, penumbra=shadow, resonance=lightning). Your slot fills are seasonally-themed names for each substrate's mode-of-action, NOT replacements for the substrates. A season's `ignition` slot fill must still feel like fire-mode-of-action, just named in this season's voice.

6. PAIR RATIONALES MUST BE STRUCTURAL. The three pair-axis rationales (thermal: ignition vs suffusion; position: bulwark vs displacement; luminance: radiance vs penumbra) explain WHY the chosen slot-fill pair is an opposition in this season's vocabulary. They are 1-2 sentence statements that read as cosmological articulation, not as descriptions of mechanics.

7. ANCHOR CATEGORY MUST BE FROM THE TAXONOMY. You will be given a list of valid anchor categories. Choose the one that best fits. Do not invent new categories.

You are deterministic. Same input → same output. Temperature is low. You are not surprising; you are recognizing.
```

### § 2.2 — User prompt (templated)

```
## Converged Season Content

**Season ID:** {{season_id}}
**Generation seed:** {{seed}}

### Element distribution

Across all classes, monsters, and skills, the dominant element distribution is:

| Element | Class count | Monster count | Skill count | % of total |
|---|---|---|---|---|
{{element_distribution_table}}

Dominant element (most prevalent across all content): **{{dominant_element}}**
Secondary element (second-most prevalent): **{{secondary_element}}**
Tertiary element (third-most prevalent): **{{tertiary_element}}**

### Class summary

{{class_count}} classes generated. Role-orientation distribution:

| Role | Count | Dominant elements |
|---|---|---|
| Damage | {{damage_count}} | {{damage_elements}} |
| Control | {{control_count}} | {{control_elements}} |
| Support | {{support_count}} | {{support_elements}} |
| Hybrid | {{hybrid_count}} | {{hybrid_elements}} |

Class archetype tags (deduplicated): {{class_archetype_tags}}

### Monster summary

{{monster_count}} monsters generated across 5 threat tiers (swarm / magic / elite / mini-boss / boss).

Monster archetype distribution:

| Archetype | Count | Dominant elements |
|---|---|---|
{{monster_archetype_table}}

Trial-boss archetype: **{{trial_boss_archetype}}** ({{trial_boss_dominant_element}})

### Geometry distribution

Skills across all sources use the following geometry families:

| Geometry | Count | % of all skills |
|---|---|---|
{{geometry_distribution_table}}

Top 3 geometry families: {{top_3_geometries}}

### Gear summary

{{gear_count}} gear items across 5 tiers (common / uncommon / rare / epic / legendary).

Gear dominant-substrate distribution:

| Substrate | Count | % of gear |
|---|---|---|
{{gear_substrate_table}}

### Trial summary

Trial structure: {{trial_structure_summary}}

### Ailment incidence

Top ailments applied across this season's combat surface:

| Ailment (substrate-of-origin) | Application count |
|---|---|
{{ailment_table}}

---

## Valid anchor categories

You must choose `anchor_category` from exactly this list:

{{anchor_category_list}}

(Examples drawn from prior seasons for tone calibration — DO NOT copy these; they are not your output. They show the *register* of valid anchor names within each category.)

{{anchor_examples_per_category}}

---

## Your output

Return JSON conforming to this schema. No prose; no explanation; no preamble. JSON only.

```json
{
  "anchor_name": "string — full poetic anchor name, like 'The Subterranean City of the Dead' or 'The Border Wall'. Definite article preferred. 4-8 words.",
  "anchor_category": "string — must be from valid_anchor_categories above",
  "season_theme_element": "string — one short evocative noun (3-8 letters preferred) that names the seasonal-element vocabulary token. Examples from prior seasons: 'char', 'brine', 'pitch', 'pall', 'brand', 'coal'. Should feel like a substance/quality/element the dominant_element substrate manifests as in this season's world.",
  "slot_fills": {
    "ignition": "string — fire's mode-of-action named in this season's voice. 2-4 words. Should evoke escalating-burst.",
    "suffusion": "string — water's mode-of-action named in this season's voice. 2-4 words. Should evoke pervading-presence.",
    "bulwark": "string — earth's mode-of-action named in this season's voice. 2-4 words. Should evoke positional-refusal.",
    "displacement": "string — wind's mode-of-action named in this season's voice. 2-4 words. Should evoke kinetic-removal.",
    "impact": "string — physical's mode-of-action named in this season's voice. 2-4 words. Should evoke direct-strike.",
    "radiance": "string — holy's mode-of-action named in this season's voice. 2-4 words. Should evoke revelation-amplification.",
    "penumbra": "string — shadow's mode-of-action named in this season's voice. 2-4 words. Should evoke withdrawal-occlusion.",
    "resonance": "string — lightning's mode-of-action named in this season's voice. 2-4 words. Should evoke sudden-traversal."
  },
  "pair_rationales": {
    "pair_thermal_rationale": "string — 1-2 sentence cosmological articulation of why this season's ignition-slot-fill and suffusion-slot-fill are an opposition. Should read like authored cosmology, not mechanics description.",
    "pair_position_rationale": "string — 1-2 sentence cosmological articulation of why this season's bulwark-slot-fill and displacement-slot-fill are an opposition.",
    "pair_luminance_rationale": "string — 1-2 sentence cosmological articulation of why this season's radiance-slot-fill and penumbra-slot-fill are an opposition."
  },
  "dominant_substrate_confirmed": "string — name the substrate (fire / water / earth / wind / lightning / holy / shadow) that the converged data centers on. This should usually match the dominant_element from the distribution table. If you see a reason to name a different substrate (e.g., the dominant element is fire but the data's cosmological weight is actually about withdrawal / decay → shadow), name what you see and produce a one-sentence rationale in the `coalescence_notes` field. Otherwise, leave coalescence_notes as an empty string.",
  "coalescence_notes": "string — empty by default. Use ONLY if dominant_substrate_confirmed differs from dominant_element distribution, OR if you observed something about the data's pattern that would inform Test 4 (substrate-identity invariance) interpretation. 1-3 sentences max. Leave empty if there's nothing to flag."
}
```
```

### § 2.3 — LLM call parameters

| Parameter | Value | Rationale |
|---|---|---|
| Model | `claude-sonnet` (current production model per star-lord's LLM-orchestration baseline) | Same as baseline naming calls; controls for model-quality variable across A/B |
| Temperature | `0.3` | Low enough for deterministic-friendly multi-shot stability (Test 5); high enough to allow naming variation across seasons (different converged content → different output) |
| Max tokens | `2048` | Output is structured JSON ~500-800 tokens typical; 2048 gives headroom for richer pair_rationales without truncation |
| Response format | `json_object` (Anthropic JSON-mode if available; otherwise instruction-driven JSON in prompt) | Structured output enables direct parsing by star-lord's distribution mechanism |
| Seed | Anthropic API does not support seeds; rely on temperature 0.3 + identical input for stability | Multi-shot Test 5 sampling captures variance empirically |
| Purpose tag | `theme_coalescence` | star-lord's TrackedLLMClient telemetry; per-season cost auditing |

---

## § 3 — Input-payload construction (rocket + star-lord)

The user-prompt template above takes ~15 variables that get filled from the converged-content artifacts:

| Template variable | Source | Construction notes |
|---|---|---|
| `season_id` | manifest.json | Direct |
| `seed` | manifest.json | Direct |
| `element_distribution_table` | aggregate across classes/*.json + monsters/*.json + gear_pool_staged.json | Count `dominant_element` field per entity; build markdown table |
| `dominant_element`, `secondary_element`, `tertiary_element` | derived from element_distribution_table | Top 3 by count |
| `class_count`, `damage_count`, `control_count`, `support_count`, `hybrid_count` | classes/*.json `role_orientation` field | Direct counts |
| `damage_elements`, `control_elements`, etc. | classes/*.json filtered by role_orientation; aggregate `dominant_element` | Comma-separated top 3 elements per role |
| `class_archetype_tags` | classes/*.json `archetype_tag` field | Deduplicated, comma-separated |
| `monster_count`, `monster_archetype_table` | monsters/*.json `archetype_tag` × `dominant_element` | Cross-tab |
| `trial_boss_archetype`, `trial_boss_dominant_element` | trial.json | Direct |
| `geometry_distribution_table` | aggregate `geometry_type` across all skills (classes + monsters + trial) | Count + percentage |
| `top_3_geometries` | derived from geometry_distribution_table | Top 3 by count |
| `gear_count`, `gear_substrate_table` | gear_pool_staged.json + gear/*.json `dominant_substrate` field | Direct |
| `trial_structure_summary` | trial.json structural fields | 1-2 sentences describing trial shape (e.g., "3-phase boss fight; phase transitions on HP thresholds 66% / 33%") |
| `ailment_table` | aggregate effects with category=ailment across all skills | Count by ailment name |
| `anchor_category_list` | canonical anchor taxonomy (rocket / engine source — see `reincarnated-engine/src/reincarnated/anchor/`) | List from registry |
| `anchor_examples_per_category` | sample 1-2 prior anchor names per category from past seasons | DO NOT include the current season's neighbors; sample from older seasons to avoid contamination |

**Important construction notes:**

- The payload should fit in ~3000-5000 tokens. If a season has 40 monsters × 3 skills each + 10 classes × 5 skills + gear pool, raw concatenation would exceed context comfortably; the distillation into distribution tables + summary counts is the load-bearing reduction.
- **No flavor text passes through.** This is critical — if the LLM sees the existing skill flavor_text, it will memorize and reproduce. The input is mechanical-distribution-only. The LLM's job is to coalesce from the *pattern*, not from prior-author crutches.
- **No prior anchor names from this season pass through.** Same reason.
- **No prior cosmological_vocabulary from this season passes through.** Same reason. (For the A/B run, both baseline and inverted seasons must have their pre-coalescence content stripped of any thematic-vocabulary leakage before this prompt sees them — otherwise the inverted pipeline isn't really inverted, it's just re-running the baseline coalescence on baseline content.)

The `anchor_examples_per_category` field is the ONE place curated thematic content enters the prompt — and only as **register calibration**. The examples show the LLM the *kind* of anchor name that lives in each category; they're not the answer. Rotate examples across seasons to avoid the LLM converging on one favorite.

---

## § 4 — Multi-shot stability discipline (Test 5)

Test 5 success criterion: ≥ 70% Jaccard overlap on (anchor + dominant_element + cosmological_vocabulary slot_fills) across 3 shots of the same converged content.

For the test to be honest:

1. **Identical input across all 3 shots.** Same payload, same template-variable fills, same system prompt, same model, same temperature. The ONLY variation is the API's intrinsic non-determinism at temperature 0.3.

2. **Sequential not parallel.** Run shot 1 → wait → run shot 2 → wait → run shot 3. Parallel firing risks subtle infrastructure variance (load balancing, model version routing).

3. **Capture all 3 outputs verbatim before scoring.** Don't make scoring decisions until you have all 3 outputs in hand.

4. **Jaccard computation:**
   - Tokenize each output's `anchor_name` into word-set
   - Tokenize each output's `season_theme_element` (1-word token; trivially in or out of overlap)
   - Tokenize each output's 8 `slot_fills` values into word-set (40 elements typically)
   - Compute pairwise Jaccard (3 pairs: shot1↔shot2, shot1↔shot3, shot2↔shot3); report mean
   - Report per-shot full outputs in Test-5 findings doc so the disposition reviewer can see the variance qualitatively

5. **Stronger stability indicators (if Jaccard is borderline):**
   - **Dominant_substrate_confirmed should match across all 3 shots** — if shot 1 says "fire" and shot 2 says "shadow", that's a destabilizing signal even if Jaccard passes on surface tokens
   - **Pair_rationales should articulate the same opposition shape** even if word-choice varies — "X is the cascading consequence; Y is the patient saturation" reads the same as "X is the explosive accumulation; Y is the slow seeping" even with different words
   - **Anchor_category should match across all 3 shots** — if shot 1 says "underworlds_and_below" and shot 2 says "royal_courts", the data is being read meaningfully differently across shots

If Test 5 fails (Jaccard < 0.70 OR any of the stronger-stability indicators flag), the disposition is **NOT** automatic-revert — see cohesion-judging protocol § "Disposition decision criteria" for the multi-test integration logic. A Test-5 fail with strong Test-1 cohesion pass might mean "the emergent theme is good but multi-shot stability is the operational concern" — fixable by raising the multi-shot stability bar in the prompt (e.g., asking the LLM to produce 2 candidate anchors and pick the more substrate-aligned one).

---

## § 5 — Prompt-evolution discipline (mid-flight, if needed)

This is the **v1 prompt** for the R8 A/B run. If A/B-run preliminary results surface that the prompt is the bottleneck (e.g., Test 1 cohesion fails not because emergent theme is bad but because prompt under-specifies pair-rationale structure), gandalf has authority to revise the prompt **only if all of the following hold:**

1. The revision is documented as `R8-theme-coalescence-prompt-2026-05-19.md` **v2** (appended-version, not overwrite — preserve v1 as historical record)
2. All 3 inverted seasons are RE-RUN against the v2 prompt at seed parity (no mixing v1 and v2 outputs in the same A/B comparison)
3. The hive log captures the revision rationale + revision diff
4. Knight-rider tags the revision (`hive-rebuild/v0.10-r8-prompt-v2`)
5. The Test 1 cohesion judging is re-run on the v2 inverted outputs

This discipline prevents the prompt from being silently iterated until it "passes" — that would invalidate the science experiment. The v1 prompt is what we're testing; if it fails, we either fix it openly (with re-run) or document the failure as findings.

---

## § 6 — Known risks + mitigations

### § 6.1 — Risk: LLM defaults to a "favorite" anchor

LLMs trained on fantasy-genre corpora have favorites. "The Forgotten Citadel", "The Sunken Cathedral", "The Whispering Forest" — these are template anchors the model produces under low-information conditions.

**Mitigation:**
- The mechanical distribution tables give the LLM substantial information to anchor against
- The `anchor_examples_per_category` shows the model the *register* (multi-word evocative names like "The Subterranean City of the Dead") and rotates examples across seasons to prevent the LLM from latching onto one
- Test 5 multi-shot stability will catch favorite-defaulting — if all 3 shots produce "The Forgotten Citadel" regardless of input, the prompt is under-grounded, fix at v2

### § 6.2 — Risk: Slot fills converge on substrate-canonical defaults

If the LLM sees "fire-dominant" and produces ignition="Burning Ember", suffusion="Cool Water", bulwark="Heavy Stone" — it has not coalesced anything. It's just translated the canonical substrate labels.

**Mitigation:**
- System prompt rule 4 (COHERE) explicitly demands shared register across all 8 slots
- The example prior-season fills shown in `anchor_examples_per_category` demonstrate the kind of cosmological-register-binding ("Pyre Debt", "Burial Seep") that the prompt expects
- Cohesion judging (companion doc) catches this failure mode at the 1-5 scale (canonical-default slot fills → cohesion score 2-3)

### § 6.3 — Risk: Substrate-identity erosion in coalescence_notes

If the prompt's "if you see a reason to name a different substrate, name what you see" instruction encourages the LLM to systematically reframe data as non-substrate themes ("this season is about velocity, not fire"), Test 4 might surface false non-invariance.

**Mitigation:**
- The instruction is asymmetric — it asks for a `dominant_substrate_confirmed` field that "should usually match the dominant_element distribution"; the bar for naming a different substrate is "see a reason"
- The `coalescence_notes` field is explicitly empty by default — the LLM defaults to no-deviation
- Test 4 examines whether deviations correlate with data patterns (signal) vs random LLM reframing (noise). If `dominant_substrate_confirmed` matches `dominant_element` in 3/3 seasons, invariance holds; if it diverges in unexpected directions, gandalf interprets per Test 4 findings doc

### § 6.4 — Risk: Token bloat from distribution tables

If the season has 40 monsters × diverse archetypes, the monster_archetype_table can grow large. Combined with class summaries, gear distribution, geometry distribution, ailment table — the prompt could push past ~5K tokens.

**Mitigation:**
- Rocket / star-lord's payload-construction code aggregates to summary statistics, NOT per-entity dumps
- If a table exceeds 20 rows, collapse the long tail into "Other (N entries)" rather than enumerating
- If total prompt token count exceeds 6000 tokens (excluding the user-prompt template overhead), star-lord flags + we revise the payload to be terser

### § 6.5 — Risk: Anchor_category taxonomy stagnation

The valid anchor_category list is fixed by the existing anchor registry. If the inverted pipeline's converged content suggests a category the taxonomy doesn't carry (e.g., "industrial_ruin" — not in the current taxonomy), the LLM is forced into the closest available choice + the cohesion may suffer.

**Mitigation:**
- For the A/B run, the existing taxonomy is sufficient (3 inverted seasons won't fall outside coverage if seeds are typical)
- If Test 4 / Test 1 findings surface that the taxonomy is the bottleneck, gandalf authors taxonomy-extension as a R8-disposition-driven canonical-doc amendment (separate work item)

---

## § 7 — Pre-A/B-run validation (gandalf + star-lord)

Before the A/B run executes, gandalf and star-lord do a **dry-run validation** of the prompt against ONE existing baseline-pipeline season:

1. Take one shipped season (e.g., `season_002017` — the necropolis-themed one) from the existing standard-demo-regen output
2. Strip its existing thematic vocabulary from the manifest + cosmological_vocabulary.json + class/monster/gear flavor texts
3. Construct the payload per § 3
4. Run the prompt at temperature 0.3
5. Compare the LLM's output to the original season's anchor + cosmological vocabulary
6. **Validation passes if:** the dominant_substrate_confirmed matches the original season's `season_theme_element`'s substrate; the anchor_category is appropriate to the converged content; the slot_fills exhibit shared register (not canonical-default fills); the pair_rationales read as cosmological articulation

This is **NOT a Test 1 substitute** — the original season was generated under input-driven mode, so it's not a clean A/B comparison. The dry-run is just **prompt-mechanical sanity check** — does the prompt produce structured output that parses, with content that doesn't immediately fail register checks. If the dry-run output is gibberish or canonical-default, the prompt needs revision before A/B fires.

Once dry-run passes, the A/B run proceeds.

---

## § 8 — References

- `agentic_orchestration/hive-mind/R8-cohesion-judging-protocol-2026-05-19.md` — companion judging side
- `agentic_orchestration/dispatches/2026-05-19-rocket-plus-star-lord-plus-gandalf-R8-season-as-emergent-output.md` — dispatch
- `canonical/story/engine-rebuild-2026-05-19-gap-solutions-and-tests.md` § 8 — R8 specification (5 hypothesis tests)
- `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 5.4 — R8 activation requirements
- `canonical/story/substrate-identity-declarations-2026-05-17.md` — substrate identity (Test 4 referent)
- `canonical/story/grouping-layer-vocabulary.md` — 8-slot grouping vocabulary (ignition / suffusion / bulwark / displacement / impact / radiance / penumbra / resonance) the prompt's slot_fills produce against
- `canonical/19-llm-call-map.md` — current LLM call map (potentially collapses dramatically under R8 if disposition commits)
- `reincarnated-engine/output/standard-demo-regen-2026-05-17/season_002011/cosmological_vocabulary.json` — exemplar coalesced output (baseline-pipeline; the structural shape inverted should match)
- `reincarnated-engine/output/standard-demo-regen-2026-05-18/season_002017/cosmological_vocabulary.json` — exemplar coalesced output (baseline-pipeline; necropolis season)
- `reincarnated-engine/src/reincarnated/anchor/` — anchor registry (source of valid anchor_category list)

---

*Authored 2026-05-19 by gandalf under autonomous-operation authority. R8 methodology asset 1 of 2. The prompt is engineered for cohesion-as-discipline, not cohesion-as-novelty. The data has chosen the season; this prompt's job is to recognize that choice and name it. Mithrandir signs.*
