# R8 — Cohesion-Judging Protocol + Disposition Decision Criteria

**Authority:** gandalf (story-and-design steward) under autonomous-operation authority.
**Status:** **Canonical methodology asset** for R8 inverted-pipeline A/B run cohesion measurement and disposition decision. Authored before A/B run kicks off per protocol § 5.4 R8 activation requirements and dispatch § "Gandalf authoring".
**Workstream:** R8 — Season-as-Emergent-Output (the science experiment).
**Companion:** `agentic_orchestration/hive-mind/R8-theme-coalescence-prompt-2026-05-19.md` (the generation side of the methodology).
**Dispatch:** `agentic_orchestration/dispatches/2026-05-19-rocket-plus-star-lord-plus-gandalf-R8-season-as-emergent-output.md`.
**Mission canonical:** `canonical/story/engine-rebuild-2026-05-19-gap-solutions-and-tests.md` § 8.

---

## § 0 — TL;DR

R8 produces 6 seasons (3 inverted + 3 baseline at seed parity). This protocol governs how those 6 seasons are scored for **cohesion** — the must-pass test (Test 1) of the R8 hypothesis — and how the resulting scores combine with Tests 2-5 to drive the **disposition decision** (commit-to-emergent-default OR revert-to-input-driven OR partial).

**Three measurement instruments:**

1. **Human cohesion judging** — gandalf (primary) + Matt-deferred (if signal is borderline). Gandalf scores all 6 seasons on the 1-5 scale; Matt may co-sign if disposition is borderline at the per-decision point. Under autonomous-operation, Matt is NOT in the judging loop unless disposition is borderline AND wind-down hasn't been called.
2. **LLM-judge cohesion scoring** — blind (judge cannot see which season is inverted vs baseline); same 1-5 scale; LLM-judge prompt below in § 4
3. **Aggregate disposition logic** — integrates Tests 1-5 results into one of three dispositions per § 5

**The 1-5 cohesion scale anchors to prior shipped seasons** so the scoring is calibrated, not abstract. Specifically:
- Cohesion 5 = `season_002017` (the necropolis season; cosmological vocabulary reads as one author wrote it — bureaucratic-necropolis register saturates every slot)
- Cohesion 4 = `season_002013` (the dwarves' empty halls; coherent industrial-mining register; slot fills mostly tight; one or two slot fills slightly drifting)
- Cohesion 3 = workmanlike baseline — the season has a recognizable identity but slot fills feel templated rather than authored
- Cohesion 2 = the season has an anchor but the cosmological vocabulary doesn't honor it; slot fills feel generic or canonical-substrate-default
- Cohesion 1 = incoherent; the anchor and the slot fills tell different stories; the season has no recognizable thematic identity

**Success thresholds (per dispatch § "Acceptance"):**

| Test | Must-pass threshold | Strong-evidence threshold |
|---|---|---|
| **Test 1 (cohesion)** | Inverted mean within **0.5** of baseline mean (e.g., baseline 4.0 → inverted ≥ 3.5) | Inverted mean within **0.2** of baseline OR **higher** than baseline |
| Test 2 (mechanical variety) | Inverted ≥ baseline on entropy + role variance + gear coherence | Inverted > baseline by ≥ 10% |
| Test 3 (LLM cost) | ≥ 75% reduction in calls AND $ | ≥ 90% reduction |
| Test 4 (substrate-identity invariance) | Discovery test; no pass/fail | Documented finding |
| Test 5 (multi-shot stability) | ≥ 70% Jaccard overlap across 3 shots | ≥ 85% Jaccard |

---

## § 1 — The 1-5 cohesion scale

Cohesion is a measurement of: **does the season's surface (anchor + cosmological vocabulary + slot fills + pair rationales + downstream named content) read as having one author who knew what they were telling?**

It is NOT a measurement of:
- Novelty (an emergent season is allowed to land in the same neighborhood as a baseline season; same-territory ≠ low-cohesion)
- Mechanical depth (R2 will test mechanical depth; cohesion is a thematic-coherence measurement)
- Personal taste (some anchors are not to gandalf's or Matt's preference; cohesion measures internal consistency, not external preference)

### § 1.1 — The scale, anchored to prior seasons

#### **Cohesion = 5 — saturated authored register**

The season's anchor, dominant-element vocabulary, and all 8 slot fills share one register so consistently that the season reads as if a single author with strong design discipline wrote every line. Pair rationales articulate the cosmology in language that extends the anchor. Downstream skill / class / monster names are recognizably *of this place*.

**Anchor example:** `season_002017` ("The Subterranean City of the Dead"). The 8 slot fills (Pyre Debt / Burial Seep / Interment Lock / Exhumation Surge / Ossuary Strike / Census Light / Unregistered Absence / Catacomb Transit) every single one reads as bureaucratic-necropolis register. The pair rationales extend the conceit further ("the necropolis's accounting of energy owed"; "the necropolis's bureaucratic permanence"). The downstream class names ("Undercity Cremator") and skill names ("Pyre Debt Settled") and monster names ("Brine Char Hulk") all live in this same world.

A cohesion-5 season passes the **read-aloud test:** if gandalf reads aloud all 8 slot fills + pair rationales in sequence, they sound like one prose excerpt from a single book of cosmology.

#### **Cohesion = 4 — tight authored register with minor drift**

The season has a clear unified register; most slot fills honor it cleanly; one or two slot fills feel slightly off-register but not jarring; pair rationales mostly articulate the cosmology; downstream named content is mostly *of this place* with occasional generic intrusions.

**Anchor examples:**
- `season_002013` ("The Dwarves' Empty Halls"). Slot fills (Seam Pressure / Damp Creep / Load-Bearing Stillness / Collapse Draft / Pickfall / Forge Remembrance / Withdrawal Soot / Shaft Echo) mostly hold industrial-mining register. Pair rationales solid. Minor: "Withdrawal Soot" reads slightly off-register from "Forge Remembrance" — the luminance pair's articulation is good but the slot-fill noun pairing feels less unified than the necropolis season.
- `season_002015` ("The Throne Room of the Mad King"). Slot fills (Royal Decree / Court Obligation / Sovereign Seal / Exile Writ / Gauntlet Strike / Legitimate Claim / Unspoken Censure / Mad Proclamation) all hold courtly-authority register. "Gauntlet Strike" is the only slight drift — the impact slot reaches for martial vocabulary that's adjacent-but-not-of the courtly register. Pair rationales solid.

#### **Cohesion = 3 — workmanlike but templated**

The season has a recognizable thematic identity. The anchor is named. The slot fills are not generic-canonical-defaults (no "Burning Ember" / "Cool Water" / "Heavy Stone"). But the slot fills feel templated — same author's style detectable, but the slots don't extend the anchor's specific world richly. Pair rationales articulate something but feel like the LLM filled them generically rather than from inside the world.

**Anchor example (hypothetical):** An anchor like "The Mountain Pass" with slot fills like "Avalanche Spark" / "Ice Saturation" / "Cliff Hold" / "Wind Sweep" / "Stone Crush" / "Sunrise Reveal" / "Cavern Shadow" / "Echo Strike". Each slot fill is locally-coherent with the anchor's geography, but the WORLD of the anchor (who lives here, what happens here, why does this place matter) isn't legible from the vocabulary. The reader can name the setting but not the story.

#### **Cohesion = 2 — anchor exists, vocabulary doesn't honor it**

The season has an anchor name. The slot fills do not extend it. Slot fills read as generic-substrate-defaults or as drawn from a different cosmology than the anchor's. Pair rationales feel rote.

**Anchor example (hypothetical):** Anchor "The Subterranean City of the Dead" + slot fills "Burning Ember" / "Cool Water" / "Heavy Stone" / "Strong Wind" / "Sharp Strike" / "Bright Light" / "Dark Shade" / "Quick Spark". The anchor promises a specific authored world; the slot fills deliver canonical-substrate-defaults that any season would receive. The disconnect is the failure.

#### **Cohesion = 1 — incoherent**

The anchor, slot fills, and pair rationales tell different stories. Or the slot fills don't honor their grouping-slot semantics (e.g., "ignition" slot filled with a name that reads as bulwark-mode). Or the cosmological vocabulary is nonsense / gibberish / shows model failure.

**Anchor example (hypothetical):** Anchor "The Underwater Library" + ignition slot "Steel Forge" + suffusion slot "Volcanic Burst" + radiance slot "Necrotic Whisper". The set has no shared world. The reader cannot construct an internally-consistent setting from the vocabulary.

### § 1.2 — Why this anchoring matters

Without prior-season anchoring, "rate cohesion 1-5" produces wildly variable scores across judges + sessions. The anchoring to specific shipped seasons (cohesion-5 = season_002017; cohesion-4 = season_002013 / season_002015) gives every judging act a **comparable referent**. Both human and LLM judging use the same anchoring.

If R8 disposition commits to emergent-default and R8 follow-on work generates new seasons, the cohesion-anchoring should be refreshed as a maintenance pass on this protocol (which seasons now serve as cohesion-5 / cohesion-4 referents post-R8?). This is a future-gandalf concern, not an R8-blocking concern.

---

## § 2 — What facets of cohesion are judged

A single 1-5 cohesion score per season is the protocol's primary instrument. But the judge derives that score from **6 facets**, each weighted equally:

| Facet | What's evaluated | Weight |
|---|---|---|
| **F1 — Anchor coherence** | Does the anchor name read as one identifiable place/concept? Is it from the valid anchor taxonomy? Is it specific enough to author against (not "The Place" but "The Subterranean City of the Dead")? | 1/6 |
| **F2 — Slot-fill register unity** | Do all 8 slot fills share one register (bureaucratic / industrial / courtly / etc.)? Or do they read like 8 LLM defaults concatenated? | 1/6 |
| **F3 — Anchor-to-slot-fill extension** | Do the slot fills *extend* the anchor's world, or just coexist with it? (Necropolis anchor → Pyre Debt slot fill extends; necropolis anchor → Burning Ember slot fill coexists-without-extending.) | 1/6 |
| **F4 — Element-anchor-mechanic fit** | Does the dominant_element ↔ anchor relationship read as fit? (Fire-dominant + necropolis = fit, via cremation/pyre register; fire-dominant + underwater library = strain unless explicitly explained.) Does the seasonal element name (e.g., "char") fit both the element substrate and the anchor's world? | 1/6 |
| **F5 — Pair rationale articulation** | Do the three pair_rationales (thermal/position/luminance) read as cosmological articulation that extends the world, or as mechanics-description copy-pasted into prose? | 1/6 |
| **F6 — Cross-content consistency** | If downstream content (class names, monster names, skill names) is sampled, do those names read as *of this place* and not generic? (Sampling discipline below.) | 1/6 |

**Facet scoring:** each facet receives a 1-5 score; the season's cohesion score is the mean across 6 facets, rounded to one decimal place.

This is more discipline than "give a vibe-1-to-5 rating" while remaining lightweight enough to score a 6-season A/B run in a session.

### § 2.1 — Cross-content consistency sampling discipline

For F6, the judge samples downstream content rather than reading the entire season. Sampling protocol:

- **3 random class names** (out of ~10 per season)
- **5 random monster names** (out of ~40 per season; sample across threat tiers)
- **5 random skill names** (out of ~150-200 per season; sample across classes + monsters + trial)
- **1 trial boss name + its 5 skills**
- **3 legendary gear names** (out of ~10)

The judge reads these ~22 names and asks: **how many feel of this place** (numerator)? F6 score derived from the fraction:

- ≥ 90% feel of-this-place → F6 = 5
- 75-90% → F6 = 4
- 50-75% → F6 = 3
- 25-50% → F6 = 2
- < 25% → F6 = 1

For the LLM-judge prompt (§ 4), the LLM is given the same sample selection — the **same names** for the same season — so human and LLM scores are comparable.

### § 2.2 — Why six facets, not one

A single holistic 1-5 score lets judges (human or LLM) collapse facets that should be distinguished. The disposition decision (§ 5) is sharper if cohesion failure can be attributed to a facet (e.g., "F2 slot-fill register fails but F1 anchor + F3 extension pass" → maybe a prompt-revision can fix that specific failure mode without re-architecting the inverted pipeline).

For Test 1's binary "did inverted mean cohesion land within 0.5 of baseline mean", the per-season **mean across 6 facets** is the input. For interpretive depth on WHY, the per-facet breakdown is the diagnostic.

---

## § 3 — Human-judge process

### § 3.1 — Primary judge: gandalf

Under autonomous-operation authority, gandalf judges all 6 seasons solo as the primary instrument. Process:

1. **Blinding:** seasons are shuffled by knight-rider (or rocket as A/B-run executor) before gandalf judges. Gandalf sees season IDs only after scoring is complete. This prevents gandalf from biasing inverted scores up (advocacy for the hypothesis) or biasing them down (over-correcting for advocacy).

2. **Per-season scoring sheet:** gandalf scores per the 6 facets above. Each facet gets a 1-5 score + a 1-sentence rationale. The 6 facets average to the cohesion score for that season.

3. **Order discipline:** gandalf judges seasons in shuffled order, one at a time, completing all 6 facets before moving to the next season. No re-scoring after seeing later seasons — first-impression scores stand.

4. **Time budget:** ~15-20 minutes per season; ~2 hours total for the 6-season run. Done in one sitting if possible; if split, gandalf re-reads the scale anchors (§ 1.1) before resuming.

5. **Output:** `output/R8-test1-cohesion-gandalf.md` with per-season per-facet scores + mean + rationale notes. Format below in § 3.4.

### § 3.2 — Optional secondary judge: Matt

Under autonomous-operation, Matt is NOT in the judging loop by default. **Matt-deferred secondary judging is invoked ONLY if the disposition is borderline** — specifically:

- Inverted mean cohesion lands within 0.4-0.6 of baseline (right on the Test 1 must-pass boundary)
- AND wind-down has not been called by Matt
- AND gandalf judges the disposition decision is materially improved by a second human judge

If those conditions hold, gandalf authors a `disposition-needs-matt-co-sign` REQUEST entry in the hive log. Matt may pick up at next session-open and score independently (using the same blinded shuffle). If Matt's mean ± gandalf's mean produce same disposition decision, disposition stands. If they diverge, gandalf authors a deliberation note describing both perspectives and proceeds with gandalf's call under autonomous-operation authority.

**Most likely:** Matt-deferred is not invoked. Gandalf scores; LLM-judge scores; aggregate disposition logic per § 5 produces the call.

### § 3.3 — Why gandalf-only is appropriate under autonomous operation

The protocol § 4.0 amendment (autonomous operation) explicitly elevates SME-agent authority. Gandalf is the story-and-design steward — cohesion judging is squarely in seam. The standing precedent: every prior cohesion-adjacent design call (form-bias diagnosis, substrate identity declarations, cosmological vocabulary lock) was authored by gandalf with Matt as approving party. Under autonomous-operation, the approval gate is dropped; gandalf decides. The judging protocol is the disciplined version of that authority.

If gandalf's scores systematically advocate for one pipeline or the other in a way the LLM-judge counter-evidences, that asymmetry is itself a disposition-relevant finding and gets documented.

### § 3.4 — Per-season scoring sheet format

```
Season ID: <hidden during scoring; revealed post-scoring>
Pipeline: <hidden during scoring; revealed post-scoring>

F1 — Anchor coherence: <1-5>
Rationale: <1 sentence>

F2 — Slot-fill register unity: <1-5>
Rationale: <1 sentence>

F3 — Anchor-to-slot-fill extension: <1-5>
Rationale: <1 sentence>

F4 — Element-anchor-mechanic fit: <1-5>
Rationale: <1 sentence>

F5 — Pair rationale articulation: <1-5>
Rationale: <1 sentence>

F6 — Cross-content consistency: <1-5>
Rationale: <1 sentence>

COHESION SCORE: <mean across 6 facets, rounded to 1 decimal place>
Holistic note: <1-2 sentences capturing anything not captured by facets>
```

---

## § 4 — LLM-judge prompt (blind judging)

The LLM-judge scores all 6 seasons blind (same shuffle as gandalf; pipeline identity hidden). Uses the same 6-facet structure for comparability. Same model (Sonnet) as the coalescence prompt to control for model-quality variable across the methodology.

**LLM-judge invocation parameters:**

| Parameter | Value | Rationale |
|---|---|---|
| Model | `claude-sonnet` | Same as coalescence call |
| Temperature | `0.2` | Lower than coalescence; judging should be more deterministic than generation |
| Max tokens | `2048` | Output is structured scoring + rationales; ~1000-1500 tokens typical |
| Response format | `json_object` | Direct parsing |
| Purpose tag | `cohesion_judging` | telemetry / cost-audit |

### § 4.1 — LLM-judge system prompt

```
You are a thematic-cohesion judge for an ARPG seasonal-generation engine.

Your job: score a single season's cosmological vocabulary and a sample of its downstream content for thematic cohesion on a 1-5 scale, across 6 facets, using anchored examples from prior seasons as calibration referents.

The cohesion scale, anchored to prior seasons:

5 = saturated authored register. The anchor, dominant-element vocabulary, all 8 slot fills, pair rationales, and downstream named content share one register so consistently the season reads as if one author with strong design discipline wrote every line. Anchor example: "The Subterranean City of the Dead" with slot fills (Pyre Debt / Burial Seep / Interment Lock / Exhumation Surge / Ossuary Strike / Census Light / Unregistered Absence / Catacomb Transit) — every fill reads as bureaucratic-necropolis register.

4 = tight authored register with minor drift. Anchor clear; most slot fills honor register; one or two slot fills slightly off-register but not jarring; pair rationales mostly articulate cosmology; downstream named content mostly of-this-place. Anchor example: "The Dwarves' Empty Halls" with slot fills (Seam Pressure / Damp Creep / Load-Bearing Stillness / Collapse Draft / Pickfall / Forge Remembrance / Withdrawal Soot / Shaft Echo) — solid industrial-mining register with minor drift on Withdrawal Soot.

3 = workmanlike but templated. Recognizable thematic identity. Slot fills not generic-canonical-defaults, but feel templated — the WORLD of the anchor (who lives here, what happens here) isn't legible from the vocabulary.

2 = anchor exists, vocabulary doesn't honor it. Slot fills read as generic-substrate-defaults or drawn from a different cosmology than the anchor's. Disconnect between anchor and vocabulary is the failure.

1 = incoherent. Anchor, slot fills, and pair rationales tell different stories, or slot fills don't honor grouping-slot semantics.

The 6 facets you score (each 1-5, weighted equally):

F1 — Anchor coherence: Does the anchor name read as one identifiable place/concept, specific enough to author against?

F2 — Slot-fill register unity: Do all 8 slot fills share one register, or read like 8 LLM defaults concatenated?

F3 — Anchor-to-slot-fill extension: Do slot fills extend the anchor's world, or just coexist with it?

F4 — Element-anchor-mechanic fit: Does the dominant_element ↔ anchor relationship read as fit? Does the seasonal element name fit both the substrate and the anchor's world?

F5 — Pair rationale articulation: Do the three pair_rationales read as cosmological articulation, or mechanics-description in prose?

F6 — Cross-content consistency: Of the ~22 sampled downstream names (3 classes / 5 monsters / 5 skills / 1 trial boss + 5 skills / 3 legendary gear), how many feel of-this-place?
  - ≥ 90% → F6 = 5
  - 75-90% → F6 = 4
  - 50-75% → F6 = 3
  - 25-50% → F6 = 2
  - < 25% → F6 = 1

You will be given the season's anchor + cosmological vocabulary + pair rationales + the sampled downstream names. You do NOT see whether this season was generated by the "inverted" or "baseline" pipeline. You score on cohesion alone.

You return JSON with per-facet scores + 1-sentence rationales + the mean cohesion score + a 1-2 sentence holistic note. No prose preamble; JSON only.
```

### § 4.2 — LLM-judge user prompt (templated)

```
## Season vocabulary to judge

**Anchor name:** {{anchor_name}}
**Anchor category:** {{anchor_category}}
**Dominant substrate:** {{dominant_substrate}}
**Season theme element:** {{season_theme_element}}

### Slot fills (8-slot cosmological vocabulary)

| Slot | Mode of action | Fill |
|---|---|---|
| ignition | escalating-burst (fire) | {{slot_ignition}} |
| suffusion | pervading-presence (water) | {{slot_suffusion}} |
| bulwark | positional-refusal (earth) | {{slot_bulwark}} |
| displacement | kinetic-removal (wind) | {{slot_displacement}} |
| impact | direct-strike (physical) | {{slot_impact}} |
| radiance | revelation-amplification (holy) | {{slot_radiance}} |
| penumbra | withdrawal-occlusion (shadow) | {{slot_penumbra}} |
| resonance | sudden-traversal (lightning) | {{slot_resonance}} |

### Pair rationales

**Thermal pair (ignition ↔ suffusion):**
{{pair_thermal_rationale}}

**Position pair (bulwark ↔ displacement):**
{{pair_position_rationale}}

**Luminance pair (radiance ↔ penumbra):**
{{pair_luminance_rationale}}

### Sampled downstream content

**3 class names:**
{{class_name_sample}}

**5 monster names:**
{{monster_name_sample}}

**5 skill names:**
{{skill_name_sample}}

**Trial boss:** {{trial_boss_name}}
**Trial boss skills:**
{{trial_skill_sample}}

**3 legendary gear names:**
{{legendary_gear_sample}}

---

## Your output

Return JSON conforming to this schema. No prose preamble; JSON only.

```json
{
  "F1_anchor_coherence": <1-5 integer or half-integer>,
  "F1_rationale": "<1 sentence>",
  "F2_slot_fill_register_unity": <1-5>,
  "F2_rationale": "<1 sentence>",
  "F3_anchor_to_slot_fill_extension": <1-5>,
  "F3_rationale": "<1 sentence>",
  "F4_element_anchor_mechanic_fit": <1-5>,
  "F4_rationale": "<1 sentence>",
  "F5_pair_rationale_articulation": <1-5>,
  "F5_rationale": "<1 sentence>",
  "F6_cross_content_consistency": <1-5>,
  "F6_rationale": "<1 sentence; include the fraction of sampled names that felt of-this-place>",
  "cohesion_score": <mean across 6 facets, 1 decimal place>,
  "holistic_note": "<1-2 sentences capturing anything not captured by facets>"
}
```
```

### § 4.3 — LLM-judge integrity checks

For LLM-judge results to be trustworthy:

1. **Same name samples across human and LLM.** The 22-name sample for F6 must be deterministically selected by season_id seed; both gandalf and the LLM judge the same names per season. (Knight-rider or rocket scripts the sampling step.)
2. **No re-judging on same prompt.** If LLM-judge result for a season looks anomalous (e.g., gandalf scored 4.2 / LLM-judge scored 1.8), do NOT re-run the LLM-judge prompt hoping for a better score — that's score-shopping. Document the divergence as a finding.
3. **LLM-judge runs blind** — same pipeline-identity-hidden discipline as human. The prompt does not mention "inverted" or "baseline".
4. **Sequential not parallel** — judge season 1 → 2 → 3 → 4 → 5 → 6, one at a time. Parallel batching risks subtle judging drift if the LLM picks up on patterns across the batch.

### § 4.4 — When human and LLM-judge diverge

Per-season divergence > 1.0 cohesion point between gandalf-mean and LLM-judge-mean is a **finding to document**, not a problem to resolve by re-judging. Possible interpretations:

- **LLM-judge over-scores:** the LLM has memorized fantasy-cosmology templates and rewards canonical-defaults that gandalf reads as templated (cohesion 3). Documented as model-bias finding.
- **LLM-judge under-scores:** the LLM doesn't recognize the register the season is committed to (e.g., bureaucratic-necropolis reads as "weird" to a fantasy-trained model). Documented as LLM-judge instrument limitation.
- **Gandalf advocacy bias:** gandalf scored inverted-pipeline seasons higher than warranted because gandalf authored the inversion hypothesis. The blinding mitigates this but doesn't eliminate it — if blind-revealed scoring shows gandalf systematically over-scored inverted seasons, that's a finding.
- **Real signal:** the divergence isolates the disagreement between human-design-sense and model-similarity-sense; useful for the disposition write-up.

For the **aggregate disposition (§ 5)**, the human-judge score is the primary instrument; LLM-judge is corroborating evidence. If they materially diverge, gandalf weights the human-judge score and discusses the divergence in the disposition doc.

---

## § 5 — Disposition decision criteria

After all 5 tests' results are in hand (Test 1 cohesion judged; Test 2 mechanical variety measured; Test 3 LLM cost measured; Test 4 substrate-identity invariance documented; Test 5 multi-shot stability measured), gandalf authors the disposition decision at `canonical/story/R8-disposition-2026-05-19.md` (or equivalent naming).

Disposition is one of three:

### § 5.1 — DISPOSITION A: commit-to-emergent-default

The inverted pipeline becomes the engine's default. Theme-as-input becomes the opt-in flag (`--theme-input`). Manifest.json schema treats `season_theme_element` and cosmological_vocabulary as OUTPUT fields. LLM call map collapses dramatically (`canonical/19-llm-call-map.md` amendment authored by gandalf). Substrate-identity declarations are revisited per Test 4 findings.

**Criteria — ALL of the following must hold:**

| Criterion | Threshold |
|---|---|
| Test 1 cohesion | Inverted mean ≥ baseline mean - 0.5 (must-pass) AND no inverted season scores < 2.5 (no individual catastrophic failure) |
| Test 2 mechanical variety | Inverted ≥ baseline on at least 2 of 3 measures (entropy / role variance / gear coherence); no measure < 90% of baseline |
| Test 3 LLM cost | ≥ 75% reduction in both calls AND $ |
| Test 4 substrate-identity invariance | Findings document does not flag systematic substrate-erosion (i.e., not all 3 inverted seasons coalesce away from substrate-identity into something else) |
| Test 5 multi-shot stability | Mean Jaccard ≥ 0.70 across all inverted seasons' 3-shot runs; no season < 0.60 |

If all five criteria hold, DISPOSITION A is authored.

### § 5.2 — DISPOSITION B: revert-to-input-driven

The inverted pipeline is rolled back. CLI flag surface remains (the opt-out `--no-coalesce` and `--theme-input` modes are retained for future use), but default behavior reverts to current input-driven mode. R8 result is documented as findings; substrate-identity declarations stand as-is. R8 fundings doc captures why the hypothesis didn't survive testing — that's the value, even on revert.

**Criteria — ANY of the following:**

| Criterion | Threshold |
|---|---|
| Test 1 cohesion | Inverted mean < baseline mean - 0.5 (must-pass failed) OR any inverted season scores < 2.0 (catastrophic individual failure) |
| Test 5 multi-shot stability | Mean Jaccard < 0.50 across inverted seasons (unstable coalescence — same input → different seasons) |
| Combined Test 1 + Test 5 borderline | Inverted mean within 0.5 of baseline BUT Test 5 < 0.70 AND Test 2 < baseline AND Test 4 surfaces invariance concerns — composite weak signal |

If any of these holds, DISPOSITION B is authored.

### § 5.3 — DISPOSITION C: partial commit

The inverted pipeline ships as **opt-in** (CLI flag `--coalesce` or similar), default remains input-driven. This is the disposition when SOME criteria hold cleanly but not all. Specifically when:

- Test 1 cohesion is within 0.5 (passes) but not within 0.2 (not strong)
- Test 2 mechanical variety is roughly equivalent (not clearly improved)
- Test 3 cost reduction is achieved (≥ 75%)
- Test 5 multi-shot stability is borderline (0.55-0.70)

Under DISPOSITION C, the engine ships both modes; specific use cases (Path B mod export with `--no-coalesce`; cost-sensitive batch runs with `--coalesce`; canonical Path A content with default input-driven mode) are documented in the disposition doc. R8 has produced operational value (cost reduction available when wanted; cohesion-comparable emergent mode for specific contexts) without re-architecting the default pipeline.

**Criteria — composite holding pattern:**

| Criterion | Threshold |
|---|---|
| Test 1 cohesion | Inverted mean within 0.5 of baseline but NOT within 0.2 |
| Test 2 mechanical variety | Equivalent (within 5% either direction) but not clearly improved |
| Test 3 LLM cost | ≥ 75% reduction (operational value retained) |
| Test 5 multi-shot stability | 0.55-0.70 (functional but not robust) |

If the test results clustered around these midline values rather than clear pass/fail, DISPOSITION C is authored.

### § 5.4 — Decision-tree summary

```
START → judge Test 1 cohesion

├── Inverted mean ≥ baseline mean - 0.5 AND no individual < 2.5
│   ├── Test 2 variety ≥ baseline on 2+ measures AND all ≥ 90% baseline
│   │   ├── Test 3 cost ≥ 75% reduction
│   │   │   ├── Test 4 no systematic substrate-erosion
│   │   │   │   ├── Test 5 ≥ 0.70 Jaccard AND no season < 0.60
│   │   │   │   │   └── DISPOSITION A (commit-to-emergent-default)
│   │   │   │   └── Test 5 fails → DISPOSITION C if borderline; B if catastrophic
│   │   │   └── Test 4 flags substrate-erosion → DISPOSITION C with substrate amendment
│   │   └── Test 3 cost reduction fails → DISPOSITION B (operational value lost)
│   └── Test 2 variety < baseline → DISPOSITION C
└── Inverted mean < baseline - 0.5 OR any individual < 2.0 → DISPOSITION B
```

### § 5.5 — Disposition doc contents (regardless of which disposition)

Gandalf authors `canonical/story/R8-disposition-2026-05-19.md` with the following sections:

1. **TL;DR — which disposition + 1-paragraph rationale**
2. **Test 1 results** — per-season cohesion scores (human + LLM-judge), means, divergence analysis if applicable
3. **Test 2 results** — mechanical variety measures (entropy / role variance / gear coherence) — inverted vs baseline
4. **Test 3 results** — LLM call counts + $ per season per mode
5. **Test 4 findings** — substrate-identity invariance discussion; whether invariance held; what (if anything) the data suggests about substrate identity as input-correlation vs inherent-signal
6. **Test 5 results** — Jaccard scores per inverted season; qualitative stability notes
7. **Disposition rationale** — explicit walk through § 5 criteria; which were met; which weren't; the resulting disposition
8. **Canonical-doc amendments triggered** — if Disposition A: LLM call map collapse amendment; if Test 4 triggered: substrate-identity amendment; if anchor taxonomy needs extension: that amendment
9. **Follow-on work** — what does this disposition unlock or block; what's the next session's R8-related work (if any)
10. **What R8 taught us regardless of disposition** — the hypothesis was honest; the test was honest; the disposition is gandalf's call; document the learning

If Disposition A: gandalf also authors the LLM call map collapse amendment immediately (per dispatch § "Gandalf scope" acceptance criteria). If Disposition B: no canonical-doc changes; R8 results are a findings document and the hypothesis is closed (revisable later if new evidence surfaces). If Disposition C: gandalf documents the dual-mode operating envelope at `canonical/19-llm-call-map.md` (the cost-mode option) without collapsing the call map.

### § 5.6 — Authority for disposition

Per dispatch § "Autonomous-operation authority": **gandalf authors and decides the disposition.** No Matt-wait. The disposition decision lands as a canonical-doc; knight-rider tags it (`hive-rebuild/v0.11-r8-disposition-decided`); the hive proceeds to the next workstream batch.

If the disposition is borderline (per § 3.2 criteria) and Matt-deferred is invoked, that's an optional augmentation — but the disposition is still gandalf's call, with Matt's input documented as a contributing data point if it arrives. Wind-down remains Matt's exclusive trigger.

---

## § 6 — Test 4 instrument (substrate-identity invariance) — gandalf examines

Test 4 is a **discovery test, not a pass/fail test**. Gandalf examines the 3 inverted seasons' coalescence outputs and asks:

1. **Does `dominant_substrate_confirmed` match the `dominant_element` distribution in all 3 seasons?**
   - If yes (3/3) → substrate identity is **preserved**; substrate is a signal the data carries inherently
   - If no (2/3 or 1/3 or 0/3) → invariance is **partially or fully broken**; substrate identity may be input-correlation rather than inherent

2. **For any season where dominant_substrate_confirmed ≠ dominant_element distribution:** what did the LLM substitute? Is the substitution a *cosmologically valid alternate frame* (e.g., dominant fire became "thermal violence" reframe; meaningful) or *LLM defaulting to a different favorite substrate* (e.g., dominant fire became "shadow" because the LLM likes shadow; non-meaningful)?

3. **For all 3 seasons:** examine the `coalescence_notes` field. What did the LLM flag? Does the flagged pattern suggest the data has structure the substrate model isn't capturing?

4. **For all 3 seasons:** examine whether the slot_fills' implicit dominant register matches the substrate they're supposedly named for. (E.g., does the `ignition` slot fill across the 3 inverted seasons feel like fire-mode-of-action, or has it drifted to feel like something else?)

Gandalf authors Test 4 findings at `output/R8-test4-substrate-identity.md`. The findings inform whether DISPOSITION A triggers a substrate-identity canonical amendment (per § 5.5 item 8). If the findings surface that substrate identity is genuinely input-correlation (not inherent), the substrate-identity-declarations doc gets a revision pass.

If the findings surface that substrate identity is robustly inherent (3/3 invariance + slot fills genuinely substrate-keyed), the substrate-identity-declarations doc gets **affirmation** — the declarations stand as canonical with empirical backing.

Either result is valuable. Test 4 doesn't gate disposition by itself; it adds the *what we learned about substrate* layer to whatever disposition the other tests indicate.

---

## § 7 — Pre-A/B-run dry-run validation

Before the A/B run executes, gandalf does a **dry-run validation** of the cohesion judging protocol against ONE shipped season (the necropolis season_002017 is the natural choice since it's the cohesion-5 anchor):

1. Construct the judging payload from season_002017
2. Score it with the LLM-judge prompt
3. Score it manually using the 6-facet sheet
4. **Validation passes if:** human + LLM judge agree the season scores 4.5-5.0 (since it's the cohesion-5 anchor referent, both judges should land high; if either judge scores it < 4.0, the judging instrument is miscalibrated and the protocol needs revision before the A/B fires)

If validation passes, the A/B-run cohesion judging proceeds with confidence. If validation surfaces miscalibration, gandalf revises the protocol (likely the LLM-judge prompt — the human sheet is more robust to small variations) and re-runs the dry-run.

---

## § 8 — A/B run execution sequence (gandalf-side)

The full sequence gandalf executes after rocket + star-lord ship the inverted pipeline:

1. **Wait for "R8 prototype operational" hive-log entry** from rocket + star-lord (tagged `hive-rebuild/v0.9-r8-prototype-operational`)
2. **Coordinate seed parity with rocket** — confirm the 6 seeds (3 inverted + 3 baseline) are agreed and reproducible
3. **Wait for "R8 A/B run complete" hive-log entry** (tagged `hive-rebuild/v0.10-r8-ab-run-complete`) — 6 seasons produced + stored at `reincarnated-engine/output/R8-ab-run-2026-05-19/{inverted,baseline}/season_NNNNNN/`
4. **Run dry-run validation** per § 7
5. **Construct the judging payloads** for all 6 seasons (rocket-or-star-lord scripted; deterministic sampling per § 2.1 + § 4.3)
6. **Score Test 1 cohesion** — gandalf human (per § 3) + LLM-judge (per § 4); store at `output/R8-test1-cohesion.md` with sub-files for `R8-test1-cohesion-gandalf.md` and `R8-test1-cohesion-llm-judge.md`
7. **Read Test 2 mechanical variety measurements** (rocket / star-lord produces; gandalf interprets but doesn't author the measurement itself)
8. **Read Test 3 LLM cost measurements** (star-lord produces; gandalf interprets)
9. **Execute Test 4 substrate-identity invariance examination** per § 6; store at `output/R8-test4-substrate-identity.md`
10. **Read Test 5 multi-shot stability measurements** (rocket/star-lord produces; gandalf interprets stability of the qualitative slot-fill register across the 3 shots)
11. **Author disposition decision** at `canonical/story/R8-disposition-2026-05-19.md` per § 5.5; tag `hive-rebuild/v0.11-r8-disposition-decided`
12. **If Disposition A: author canonical-doc amendments** (LLM call map collapse; substrate-identity if Test 4 triggered)
13. **Hive-log entry DECISION on disposition** with reference to the disposition doc + commit SHA

The full gandalf-side cycle (steps 4-13) is estimated ~1 day of focused work once the A/B run output is in hand.

---

## § 9 — References

- `agentic_orchestration/hive-mind/R8-theme-coalescence-prompt-2026-05-19.md` — companion generation side
- `agentic_orchestration/dispatches/2026-05-19-rocket-plus-star-lord-plus-gandalf-R8-season-as-emergent-output.md` — dispatch
- `canonical/story/engine-rebuild-2026-05-19-gap-solutions-and-tests.md` § 8 — R8 specification (5 hypothesis tests)
- `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 — autonomous-operation amendment
- `canonical/story/substrate-identity-declarations-2026-05-17.md` — substrate identity (Test 4 referent)
- `canonical/story/grouping-layer-vocabulary.md` — 8-slot vocabulary that slot fills produce against
- `canonical/19-llm-call-map.md` — current LLM call map (Disposition A triggers collapse amendment)
- `reincarnated-engine/output/standard-demo-regen-2026-05-18/season_002017/cosmological_vocabulary.json` — cohesion-5 anchor exemplar (the necropolis season)
- `reincarnated-engine/output/standard-demo-regen-2026-05-17/season_002013/cosmological_vocabulary.json` — cohesion-4 anchor exemplar (the dwarves' empty halls)
- `reincarnated-engine/output/standard-demo-regen-2026-05-17/season_002015/cosmological_vocabulary.json` — cohesion-4 anchor exemplar (the throne room of the mad king)

---

*Authored 2026-05-19 by gandalf under autonomous-operation authority. R8 methodology asset 2 of 2. The hypothesis is held; the test is honest; the disposition is gandalf's call. Either result is valuable — the season-as-emergent-output either survives the test or it doesn't, and the engine learns which. Mithrandir signs.*
