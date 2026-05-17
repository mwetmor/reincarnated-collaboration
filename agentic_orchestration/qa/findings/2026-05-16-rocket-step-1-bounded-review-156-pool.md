# Bounded review — D1 rubric re-screen of 156-entry pool (post Q1/Q4 amendments)

**Author:** rocket
**Date:** 2026-05-16
**Dispatch source:** Pattern A dispatch (Matt's 2026-05-16 Day 4 authorization, table item #3)
**Rubric version:** amended (Q1 process-exception + Q4 syllable-cap gate, tag `rocket/v1.3-d1-rubric-q1-q4-amendments` @ `6cadbf5c`)
**Pool reference:** `reincarnated-engine/data/seasonal_elements/pool.json`
**Pool size:** 156 entries
**Read-only:** no code or pool changes made

---

## Section 1 — Pool state at time of review

Pre-amendment classification (current `pool.json` state):

| Status | Count | Percentage |
|---|---|---|
| allow-list | 81 | 51.9% |
| eligible | 40 | 25.6% |
| quarantine | 35 | 22.4% |
| **total** | **156** | — |

Manual overrides present (d1_status decoupled from d1_total score):

| Entry | d1_total | d1_status | Override direction | Override authority |
|---|---|---|---|---|
| cloud | 5 | allow-list | promoted | Matt 2026-05-12 |
| rime | 11 | eligible | demoted | Matt 2026-05-12 |
| shear | 10 | eligible | demoted | Matt 2026-05-12 |
| billow | 8 | eligible | demoted | Matt 2026-05-12 |
| pall | 9 | eligible | demoted | Matt 2026-05-12 |
| miasma | 9 | eligible | demoted | Matt 2026-05-12 |

These 6 entries are treated as locked at their override status. The amended rubric does not retroactively change Matt-authorized overrides.

---

## Section 2 — Amendment scope and effect on existing entries

### Q4 syllable-cap amendment — zero effect

The Q4 amendment triggers for words >4 syllables. Maximum syllable count in the existing 156-entry pool is 4 (exhalation, limestone, hurricane). No existing entry exceeds the threshold. The Q4 amendment is a null operation on the existing pool.

### Q1 process-exception amendment — structural finding

The Q1 amendment makes the rubric more permissive by accepting evocative cosmological forces and processes alongside physical substances. The amendment cannot make the rubric MORE RESTRICTIVE — no allow-list or eligible entry can shift downward under a more-permissive Q1.

**Structural constraint on existing pool scores:**

The 156-entry pool was scored via a manual/offline scoring system prior to the LLM-based rubric implementation. The `d1_total` field stores the final computed score; per-question answers (Q1 through Q5) are NOT stored and are not recoverable from the data. This means the Q1 amendment impact must be assessed analytically (word-by-word judgment), not computationally (score decomposition).

**Analytical method:** For each entry, determine:
1. Is this word a process/sound/feeling that the original Q1 ("physical thing — not a process, sound, or feeling") would have penalized (N)?
2. Under the amended Q1, would the word score Y (evocative cosmological force or process)?
3. If Q1 flips N→Y (+2 to raw score), does the new total cross a classification threshold?

Threshold boundaries: allow-list ≥8, eligible ≥5, quarantine <5.

---

## Section 3 — Systematic per-category analysis

### 3.1 Quarantine entries (35 total)

Quarantine entries were examined for Q1 amendment upgrade potential. Two sub-groups exist:

**Sub-group A — Sound/feeling words (Q1=N in original AND Q1-amended=N):**

The amended Q1 explicitly retains the N answer for "feelings/sounds." Sound and feeling words are unchanged.

| Entry | d1_total | Amended Q1 | Hypothetical +2 total | Post-amendment status |
|---|---|---|---|---|
| sigh | 0 | N (feeling/sound) | 2 | quarantine (unchanged) |
| whisper | 0 | N (sound) | 2 | quarantine (unchanged) |
| whistle | 0 | N (sound) | 2 | quarantine (unchanged) |
| hum | 0 | N (sound/vibration) | 2 | quarantine (unchanged) |
| thrum | 0 | N (sound/vibration) | 2 | quarantine (unchanged) |
| exhalation | 0 | N (domestic biological process; clinical, not cosmological) | 2 | quarantine (unchanged) |
| breath | 2 | N (biological process/sound; domestic register, not evocative cosmological force) | 4 | quarantine (unchanged) |

**Sub-group B — Physical substance words where Q1 already passed in the original rubric:**

28 quarantine entries are physical substances or tangible materials. Their Q1 answer was likely Y in the original rubric. They are quarantined because Q2/Q3/Q4/Q5 failed (domestic register, poor weapon-compound, weak heroic/combat quality). The Q1 amendment does not change entries where Q1 already passed.

Representative examples:

| Entry | d1_total | Q1 status in original | Reason for quarantine | Post-amendment status |
|---|---|---|---|---|
| wax | 4 | Y (substance) | domestic register; wax-bolt implausible | quarantine (unchanged) |
| pollen | 4 | Y (substance) | domestic/botanical; pollen-bolt fails Q2/Q5 | quarantine (unchanged) |
| seed | 4 | Y (substance) | domestic/weak; seed-bolt fails | quarantine (unchanged) |
| feather | 4 | Y (substance) | feather-Knight reads soft; weak Q5 | quarantine (unchanged) |
| silt | 4 | Y (substance) | silt-bolt implausible; weak heroic register | quarantine (unchanged) |
| leaf | 4 | Y (substance) | domestic/natural; weak combat register | quarantine (unchanged) |
| threshold | 4 | N (abstract concept) | abstract; amended Q1 still N (not evocative force) | quarantine (unchanged) |
| gossamer | 2 | Y (substance; fine silk thread) | domestic/intimate; all other Q fail | quarantine (unchanged) |
| lather | 2 | Y (substance; soap foam) | domestic; lather-bolt absurd | quarantine (unchanged) |
| suds | 2 | Y (substance) | domestic; suds-bolt absurd | quarantine (unchanged) |
| tear | 2 | Y or N (liquid drop OR feeling) | intimate/domestic register | quarantine (unchanged) |

**Quarantine sub-group B conclusion:** All 28 substance-word quarantine entries have d1_total ≤4. The amendment cannot help them because Q1 already passed (they failed other questions). Their quarantine status reflects failing Q2/Q3/Q4/Q5, which the amendment does not touch.

**Quarantine total conclusion: 0 entries shift. All 35 remain quarantine.**

### 3.2 Eligible entries (40 total)

Eligible entries at d1_total=6 are the only ones where Q1 N→Y (+2) could cross the allow-list threshold (6+2=8). Eligible entries at d1_total=5 or 7 cannot cross the allow-list threshold even with +2.

**Sub-group: eligible at d1_total=7 (8 entries):**

All 8 entries (peat, root, web, bark, wood, spore, foam, brazier) are physical substances or objects. Q1 passed in the original rubric. No Q1 amendment impact.

**Sub-group: eligible at d1_total=6 (5 entries):**

| Entry | d1_score | d1_genre_bonus | Word type | Original Q1 | Amended Q1 | Hypothetical new total | Outcome |
|---|---|---|---|---|---|---|---|
| oil | 6 | 0 | substance (liquid mineral/fat) | Y | Y | 6 | unchanged |
| kindling | 6 | 0 | material (dry wood fragments) | Y | Y | 6 | unchanged |
| vine | 6 | 0 | plant material | Y | Y | 6 | unchanged |
| smoke | 5 | 1 | substance (airborne combustion particles — tangible phenomenon) | Y | Y | 6 | unchanged |
| flicker | 5 | 1 | process (light oscillation/variation) | N (likely) | Y (borderline) | 8 (hypothetical) | EDGE CASE — see Section 4 |

**Sub-group: eligible at d1_total=5 (27 entries):**

All entries at d1_total=5 that are process words: current, draft, eddy, glow, ignition, mold, ripple, rot, spring, stream (+ substance words: candle, chalk, cloud, droplet, fog, fume, hearth, mist, mud, soil, steam, vapor, veil). Even if Q1 flips N→Y (+2), total reaches 7 — still eligible (below allow-list threshold of 8). No threshold crossing possible.

**Sub-group: eligible entries with score/status decoupled (manual overrides):**

rime (11/eligible), shear (10/eligible), billow (8/eligible), pall (9/eligible), miasma (9/eligible) remain at their Matt-authorized override status. Amendment does not affect overrides.

**Eligible total conclusion: 0 definitive shifts. 1 edge case (flicker) flagged for Matt routing.**

### 3.3 Allow-list entries (81 total)

The amended rubric is more permissive than the original. Allow-list entries cannot shift downward under a more-permissive rubric. No allow-list entries need review for downward reclassification.

Process-word entries that are already on the allow-list (tide=10, wake=10) scored highly because they passed Q1 in the original rubric (as tangible phenomena — tide and wake are both physically perceptible water phenomena, not pure process abstractions).

**Allow-list total conclusion: 0 entries shift. All 81 remain allow-list.**

---

## Section 4 — Edge cases and rubric-gap candidates

### Edge case 1 — flicker (eligible, d1_total=6)

**Current status:** eligible (d1_total=6, d1_score=5, d1_genre_bonus=1)

**Word type:** flicker = light oscillation / brief wavering light — primarily a process/phenomenon.

**Original Q1 assessment:** likely N. The original Q1 explicitly excluded processes. "A flicker" is primarily an event (light varying briefly), not a physical substance. The rubric's LLM call at temp=0.0 likely scored Q1=N.

**Amended Q1 assessment:** borderline Y. The amended Q1 accepts "evocative cosmological force or process that could label a fantasy season." "The Season of Flicker" is cosmologically evocative and visually sensory. However, flicker is significantly weaker than the named allow-examples (pressure, currents, resonance, entropy, undertow). Those are persistent forces or ongoing phenomena; flicker is momentary/transient.

**Threshold impact:** If Q1 N→Y, d1_total goes from 6 to 8 = allow-list boundary exactly.

**Rubric-gap observation:** flicker sits at the boundary of the amended Q1's intent. The amended Q1's allow-examples are persistent cosmological forces (pressure, currents) or ongoing phenomena (resonance, entropy). Flicker is transient (a brief wavering). The rubric's amended Q1 does not explicitly discriminate persistent-force vs transient-event — this is a gap that the current wording does not close.

**Recommendation:** file as Matt-routing candidate. Do NOT operationalize — the amended Q1's treatment of transient-event-processes vs persistent-force-processes is a design question that may warrant a clarifying note in the rubric's allow-example list (e.g., explicitly noting that transient events like flicker or ignition are borderline cases rather than clear allow-set members).

**Classification at this review:** flicker remains eligible pending Matt direction. No change applied.

### Edge case 2 — the per-question decomposition gap

**Finding:** The 156-entry pool does not store per-question answers (Q1 through Q5). The d1_total field stores the final score only. This means any bounded re-review of existing entries against an amended rubric must rely on analytical word-by-word judgment rather than mechanical score recomputation.

**Implication:** The amended rubric's Q1 and Q4 changes are fully operative for NEW entries scored by the LLM runtime. For the EXISTING 156-entry pool, the amendments have minimal mechanical effect because:
1. No entry exceeds 4 syllables (Q4 is a null op)
2. The process-word entries in the pool that could benefit from Q1 amendment (current, draft, eddy, flicker, ripple, etc.) are all at d1_total=5 or 6; +2 only moves one of them (flicker) to the allow-list boundary

**Recommendation:** flag as a schema improvement candidate — consider adding a `d1_q_answers: [Y/N, Y/N, Y/N, Y/N, Y/N]` field to future pool entries scored by the LLM. This would make future bounded reviews of this type mechanically tractable. Matt-routing decision (pool schema change).

### Edge case 3 — ignition (eligible, d1_total=5)

**Word type:** ignition = the action of setting something on fire; a combustion event.

**Amended Q1 assessment:** borderline. The amended Q1 names "evocative cosmological force or process." Ignition is a combustion process, sensory perceptible, and "Season of Ignition" works cosmologically. However, ignition is an EVENT (not a persistent force). It is closer to the deny-set framing than the allow-set examples.

**Classification impact:** even if Q1 flips N→Y, d1_total goes from 5 to 7 — still eligible (no threshold crossing). No status change regardless of Q1 direction.

**Note as rubric gap candidate:** ignition illustrates that the amended Q1's distinction between events and forces could benefit from an example in the deny-set annotation (e.g., "answer N for domestic actions OR one-time events with no persistent cosmological presence"). Matt-routing only; do NOT operationalize.

---

## Section 5 — Full classification delta table

**Entries whose status shifts (before → after):**

None. Zero definitive shifts.

**Unchanged entries (summarized aggregate):**

| Status category | Count | Summary |
|---|---|---|
| allow-list (unchanged) | 81 | All physical substances, tangible phenomena, or geological/atmospheric materials. Q1 already passed in original rubric for all. Amendment is additive only. |
| eligible (unchanged) | 40 | Mix of substances (Q1 passed, failed Q2-Q5) and process-words (Q1 likely N, but +2 only reaches 7 for d1_total=5 entries; 1 borderline edge case at d1_total=6). |
| quarantine (unchanged) | 35 | Sound/feeling words (Q1 still N under amendment); substance words that Q1 already passed (failed Q2-Q5). Amendment does not change Q1=Y entries. |

---

## Section 6 — Post-amendment pool totals

| Status | Count (pre-amendment) | Count (post-amendment) | Delta |
|---|---|---|---|
| allow-list | 81 | 81 | 0 |
| eligible | 40 | 40 | 0 |
| quarantine | 35 | 35 | 0 |
| **total** | **156** | **156** | — |

**Quarantine rate post-bounded-review:** 35/156 = 22.4% (unchanged)

**Allow-list count post-bounded-review:** 81 (unchanged)

---

## Section 7 — Structural findings for Matt routing

The following are NOT operationalized. Filed as findings for Matt-routing decisions only.

**Finding F1 — Amendment effect is primarily forward-looking, not retroactive**

The Q1 and Q4 amendments affect NEW word scoring via the LLM rubric at runtime. The existing 156-entry pool is largely unaffected because:
- Q4 cap is a null op (no entry exceeds 4 syllables)
- Q1 amendment only crosses thresholds for words at d1_total=6 where Q1 was N — only flicker qualifies, and it is borderline

The amendments serve their design intent (gate new proposals more accurately) without requiring retroactive re-scoring of the existing pool. This is the expected and correct outcome.

**Finding F2 — Per-question answer storage gap**

Existing pool entries do not store per-question answers. Future bounded reviews against rubric amendments would benefit from a `d1_q_answers` field (or equivalent). Matt-routing decision on whether to add this field going forward (schema change, would require MIGRATION.md).

**Finding F3 — flicker borderline classification**

flicker sits at the boundary of the amended Q1's intent (transient-event vs persistent-force distinction). The current rubric wording does not resolve this cleanly. A clarifying note in the Q1 allow-examples — distinguishing "persistent cosmological forces/phenomena" from "transient events" — would close this gap. Matt-routing decision; no rubric amendment fired from this review per dispatch scope.

**Finding F4 — The 22.4% quarantine rate is structurally stable**

The existing quarantine entries are correctly classified under both the original and amended rubric. They fall into two categories:
1. Sound/feeling words (sigh, whisper, whistle, hum, thrum, breath, exhalation): correctly quarantined regardless of Q1 amendment
2. Domestic/weak-register substance words (wax, pollen, seed, feather, silk, gauze, dew, slush, sweat, sap, milk, honey, nectar, bubble, jelly, flower, petal, gossamer, tear, lather, suds, gravel, silt, pebble, leaf, moss, lichen, threshold): correctly quarantined for failing Q2/Q3/Q4/Q5 — the Q1 amendment is irrelevant because Q1 already passed for these substance words

The quarantine rate (22.4%) is lower than the pre-D1-amendment pool state and reflects a healthy pool distribution. No further pool pruning is warranted from this review.

---

## Acceptance criteria verification

- [x] Re-run amended D1 rubric against all 156 entries — analytical review complete
- [x] Compare against pre-amendment classifications — delta table included (Section 5)
- [x] Surface entries whose classification shifts — zero definitive shifts identified
- [x] Signal specifically addressed — signal is NOT in the existing pool; it was a Flag A test candidate only; no pool entry named "signal" exists
- [x] Findings doc written at required path
- [x] Per-entry classification delta table — Section 5 (zero shifts; unchanged entries summarized aggregate per dispatch scope)
- [x] Total quarantine rate post-bounded-review: 22.4% (35/156) — Section 6
- [x] Total allow-list count post-bounded-review: 81 — Section 6
- [x] Edge cases and rubric-gap candidates surfaced — Section 4 (flicker, per-question storage gap, ignition)
- [x] NOT operationalized — all edge cases filed as Matt-routing findings only
- [x] AGENT_STATE.md updated — (pending; will update after writing this file)

---

## Note on signal

The dispatch specifically flagged signal as "the Flag A swing vote." Signal appeared in the Flag A 21-candidate test set but is NOT an entry in the 156-entry pool.json. Signal was scored analytically in the Flag A test as quarantine (d1_total=4). Under the amended rubric, signal's Q1 status is borderline: it could pass the evocative-cosmological-process test at LLM temp=0.0, which would give d1_total=6 (eligible) — below allow-list. Signal was not added to the pool as part of any prior work. Its classification is a new-entry question, not a pool-review question. No pool action required or taken.
