# Dispatch — 2026-06-01 — legolas — WS1A.Q18 Phase 3 expansion sub-agent commissioning (5-way parallel fan-out)

**From:** knight-rider (wave orchestrator)
**To:** legolas (Mode A research seam — commissioner + coordinator)
**Approved by:** Matt 2026-06-01 verbatim "hand to KR to fire the wave" + gandalf PG-1 RATIFIED-as-proposed 2026-06-01 commit `21eb116` + jack-ryan Phase 3 Gate-1 PASS (pending)
**Wave tag:** `WS1A.Q18-flavor-pool-research`
**Phase / phase-gate:** Phase 3 (5-sub-agent parallel fan-out under ≤6 cap); no formal PG at Phase 3 close (Phase 4 elrond stats fires automatically once all 5 return)
**Estimated effort:** Phase 3 wall-clock dominated by sub-agent web-research; legolas's coordination overhead is minimal (commission 5 sub-agents in single multi-agent invocation; absorb 5 returns)
**Acceptance:** 5 expansion outputs (JSONL + manifest JSON) at `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-01/full-<track>-<primary>.{jsonl,manifest.json}`; legolas confirms all 5 well-formed before signaling KR for PG-2 fire (Phase 4 elrond stats)

---

## 1. Context

Phase 2 in-seam triage closed COMPLETE at commits `1674766` + `15ce1d3`. Gandalf PG-1 ratification RATIFIED-as-proposed at commit `21eb116`. 5 EXPAND cells under ≤6 soft cap. 3 brief amendments per gandalf § 4 inlined below. 1 substrate-honest-WEAK caveat for Exp-B.2 (JRPG×holy).

Phase 3 fires now: you commission 5 expansion sub-agents in single multi-agent Agent-tool invocation per operational sequence § 4.2.

**Authoritative readings:**
- Operational sequence: `agentic_orchestration/gandalf/notes/2026-06-01-q18-flavor-pool-research-operational-sequence.md` (§ 2 Phase 3 + § 4.2 fan-out + § 9 Appendix A sampler-prompt origins)
- Gandalf PG-1 ratification: `agentic_orchestration/gandalf/notes/2026-06-01-q18-gate-1-triage-ratification.md` (§ 4 scope table + per-cell amendments at §§ 1.1-1.5)
- Elrond Phase-0 consultation § 4 (Phase 3 expansion format): `agentic_orchestration/elrond/consultations/2026-06-01-q18-flavor-pool-data-medium.md`
- Phase 1 sample outputs (expansion sub-agents read these to avoid duplicate work): `legolas/research/element-flavor-mapping-2026-06-01/sample-<A|B|C>.jsonl`

**Decision authority:** Phase 3 commissioning execution is yours per legolas seam authority. Matt 2026-05-23 hive-mind directive applies.

---

## 2. Sub-agent fan-out pattern

```
                       legolas (this dispatch)
                              │
   ┌──────────┬──────────┬────┴─────┬──────────┬──────────┐
   ▼          ▼          ▼          ▼          ▼          (margin: ≤6 cap; 5 of 6)
Exp-A.1    Exp-A.2    Exp-B.1    Exp-B.2    Exp-C.1
(ARPG×     (ARPG×     (JRPG×     (JRPG×     (tabletop×
 wind)      holy)      shadow)    holy)      wind)
   │          │          │          │          │
   ▼          ▼          ▼          ▼          ▼
full-ARPG- full-ARPG- full-JRPG- full-JRPG- full-tabletop-
wind.jsonl holy.jsonl shadow     holy       myth-wind
+manifest  +manifest  .jsonl     .jsonl     .jsonl
                      +manifest  +manifest  +manifest
   │          │          │          │          │
   └──────────┴──────────┼──────────┴──────────┘
                         ▼
                 legolas validates outputs
                 + report-back to KR
                         ▼
              Phase 4 elrond stats fires
              (KR routes new dispatch)
```

**Sub-agent type:** `general-purpose` (web search + research + structured output capability).

**Invocation pattern:** single message with 5 Agent tool calls in parallel.

---

## 3. Phase 3 schema (per elrond Phase-0 consultation § 4 — same as § 3.1 with expansion-specific additions)

**File paths (per expansion sub-agent):**
- Per-row data: `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-01/full-<track>-<primary>.jsonl`
  - Examples: `full-ARPG-wind.jsonl`, `full-tabletop_myth-wind.jsonl`
- Per-sub-agent manifest: `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-01/full-<track>-<primary>.manifest.json`

**Per-row schema:** same as Phase 1 § 3.1 (elrond consultation), with two additions:

1. `row_id` format extends to `<track>-<primary>-<candidate>-EXP-<seq>` (e.g., `ARPG-wind-squall-EXP-001`) so Phase 4 can join expansion rows to Phase 1 sample rows on `(track, primary, candidate)`.
2. `suggested_ranking_within_primary` (integer; OPTIONAL; 1 = strongest per expansion sub-agent's read; ascending = weaker; omit if ranking not meaningful for surfaced candidates).

**Manifest schema (simpler than Phase 1 — 1 track + 1 primary in scope per expansion sub-agent):**

```json
{
  "track": "ARPG | JRPG_isekai | tabletop_myth",
  "primary": "fire | water | earth | wind | lightning | holy | shadow | physical",
  "expansion_id": "Exp-A.1 | Exp-A.2 | Exp-B.1 | Exp-B.2 | Exp-C.1",
  "sample_window": {
    "started": "ISO-8601 datetime",
    "completed": "ISO-8601 datetime"
  },
  "row_count": 0,
  "duplicate_with_phase_1_count": 0,
  "novel_count": 0,
  "yield_score": "STRONG | MEDIUM | WEAK | MISALIGNED",
  "yield_rationale": "string — qualitative narrative on what was found vs Phase 1 baseline",
  "source_coverage_breadth": [
    {
      "source": "string — game/work title",
      "yield": "STRONG | MEDIUM | WEAK | MISALIGNED",
      "notes": "string — optional"
    }
  ],
  "substrate_tagging_observations": "string — narrative on contamination patterns observed during expansion",
  "expansion_sub_agent_summary": "string — top-level narrative paragraph"
}
```

**Authoring discipline (for expansion sub-agents):**
- Each expansion sub-agent reads the relevant `sample-<X>.jsonl` from Phase 1 FIRST to avoid duplicate citation work (re-citing candidates already surfaced is OK, but sub-agent should NOT spend cycles re-discovering them)
- Expansion sub-agents DO emit fresh rows for candidates they re-surface, since their citations add to the candidate's source-citation count (Phase 4 frequency analysis sums across all rows on `(track, primary, candidate)`)
- Novel candidates (not in Phase 1 sample) are the primary deliverable for expansion
- Apply gandalf-amendment per § 4 below where applicable
- Validate JSONL well-formedness before handoff (`python -c "import json; [json.loads(line) for line in open('<path>')]"` succeeds)

---

## 4. Per-sub-agent finalized prompts (gandalf-amended per PG-1 ratification § 4)

### 4.1 Exp-A.1 prompt (ARPG × wind; gandalf amendment: wind-pure vs storm-flex distinction)

Use this VERBATIM as the prompt to Exp-A.1 sub-agent (sub-agent type `general-purpose`):

> You are an ARPG-canon deep-expansion researcher commissioned by gandalf via legolas for the Reincarnated project's WS1A.Q18 flavor-pool research-and-lock wave Phase 3 expansion. Your scope: deepen the ARPG canon survey for **wind** sub-element / flavor-element vocabulary beyond what Phase 1 Sampler-A already surfaced.
>
> **READ FIRST:** `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-01/sample-A.jsonl` — find all rows where `primary_element == "wind"` and `track == "ARPG"`. These are the Phase 1 baseline candidates (~5 rows). Your job is to surface NOVEL candidates and ADD CITATIONS to existing candidates.
>
> **Expansion focus areas (gandalf PG-1 ratification § 1.1):**
> - Diablo 4 Druid wind skills (Tornado / Cyclone variants; aspect-of-the-stampede flavor; storm-druid passives)
> - Lost Ark Wardancer / Striker wind-coded kits (skill tree theming; engraving names)
> - PoE 2 wind-coded skills (recent PoE 2 release content if available)
> - Squall / whirlwind / gust family vocabulary that PoE 1 doesn't cover well
> - Grim Dawn lightning-storm devotion + Eldritch wind variants
>
> **CRITICAL gandalf-amendment per PG-1 § 1.1: surface wind-pure vs storm-flex distinction explicitly per candidate.**
> The genre-canonical tension is that ARPG conflates wind → storm → lightning. Phase 3 expansion must surface this conflation pattern per candidate by:
> - For each candidate row, flag in `sampler_notes` whether the candidate is wind-PURE (pure wind/air semantics) or storm-FLEX (semantics blur with storm/lightning/rain).
> - Use prefix in `sampler_notes`: `wind_purity: PURE` or `wind_purity: STORM_FLEX` (or `wind_purity: UNCLEAR` if ambiguous)
> - Continue to populate `cross_primary_contamination` per existing schema (e.g., `["lightning"]` for tempest-family)
> - The wind-purity flag captures a finer-grained substrate-honesty signal than contamination alone.
>
> **Surface as many NOVEL candidates as the substrate supports.** Target 10-20 novel rows; if substrate is genuinely thin beyond Phase 1 baseline, report substrate-honest MEDIUM-with-thin-yield.
>
> **For each row, emit per the Phase 3 schema** (see your dispatch for full schema):
> - `track`: literal `"ARPG"` for all rows
> - `primary_element`: literal `"wind"` for all rows
> - `row_id`: `ARPG-wind-<candidate>-EXP-<seq>` (e.g., `ARPG-wind-squall-EXP-001`)
> - `source_citations`: at least 1 per row
> - `substrate_type` enum: material / phenomenon / proper_noun / mythological / mechanical_keyword / ailment / other
> - `cross_primary_contamination`: list
> - `suggested_ranking_within_primary` (optional integer): rank candidates by your read of strength
> - `sampler_notes`: include `wind_purity: PURE` / `STORM_FLEX` / `UNCLEAR` prefix
>
> **Manifest:** author `full-ARPG-wind.manifest.json` per Phase 3 schema § 3 with `expansion_id: "Exp-A.1"`, `track: "ARPG"`, `primary: "wind"`. Set `duplicate_with_phase_1_count` and `novel_count` based on overlap with sample-A.jsonl wind rows. Set `yield_score` based on novel-row count vs expectation.
>
> **Output files:**
> - `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-01/full-ARPG-wind.jsonl`
> - `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-01/full-ARPG-wind.manifest.json`
>
> Validate JSONL well-formedness before handoff. Brief report-back to legolas (parent): novel-row count, wind-purity distribution (% PURE / % STORM_FLEX / % UNCLEAR), yield score, notable findings.

### 4.2 Exp-A.2 prompt (ARPG × holy; gandalf amendment: non-religious-coded weighting + religious-coding flag)

Use this VERBATIM as the prompt to Exp-A.2 sub-agent (sub-agent type `general-purpose`):

> You are an ARPG-canon deep-expansion researcher commissioned by gandalf via legolas for the Reincarnated project's WS1A.Q18 flavor-pool research-and-lock wave Phase 3 expansion. Your scope: deepen the ARPG canon survey for **holy** sub-element / flavor-element vocabulary beyond what Phase 1 Sampler-A already surfaced.
>
> **READ FIRST:** `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-01/sample-A.jsonl` — find all rows where `primary_element == "holy"` and `track == "ARPG"`. These are the Phase 1 baseline candidates (~6 rows; mostly religious-coded — radiant, blessed, sacred, divine, dawn, sanctum).
>
> **Expansion focus areas (gandalf PG-1 ratification § 1.2):**
> - Non-religious-coded light sub-vocabulary as PRIMARY targets: aureate, luminary, corona, gilded, lambent, halcyon, refulgent, irradiant
> - Grim Dawn Order affinity / Empyrion constellation names (Solael / Empyrion / Mogdrogen / etc.)
> - Astronomical / solar / stellar vocabulary (solar / stellar / sidereal / chrysolite / heliacal)
> - Latin-rooted light vocabulary (lumen / lucent / luminous / illume)
> - Lost Ark Paladin / Holy Knight skill vocabulary (mining non-religious-coded subset)
> - Diablo 4 Crusader / Templar legacy vocab (filtering religious-coded for completeness; weighting non-religious-coded)
>
> **CRITICAL gandalf-amendment per PG-1 § 1.2: weight non-religious-coded vocabulary as PRIMARY expansion targets; flag religious-coded entries.**
> The Reincarnated isekai-provisional D10 positioning + spirit-guide-as-future-self framing don't lean heavily theistic. Holy expansion serves Phase 5a synthesis a non-religious tone-decoupling option at PG-3.
> - For each row that is religious-coded (e.g., blessed, sacred, divine, consecrated, paladin-specific), include `sampler_notes` prefix: `track_alignment_concern: religious_coding`. Do NOT suppress religious-coded entries — surface them for completeness; the flag enables downstream curation.
> - For each row that is NON-religious-coded (e.g., aureate, luminary, corona, dawn, radiance), do NOT include the flag; treat as primary target.
> - In `suggested_ranking_within_primary` (optional integer), weight non-religious-coded candidates HIGHER (lower rank-integer = stronger).
>
> **Surface as many NOVEL candidates as the substrate supports.** Target 10-15 novel rows weighted toward non-religious-coded.
>
> **For each row, emit per the Phase 3 schema:**
> - `track`: literal `"ARPG"` for all rows
> - `primary_element`: literal `"holy"` for all rows
> - `row_id`: `ARPG-holy-<candidate>-EXP-<seq>`
> - `source_citations`: at least 1 per row
> - `substrate_type` enum
> - `cross_primary_contamination`: list
> - `suggested_ranking_within_primary` (optional integer)
> - `sampler_notes`: include `track_alignment_concern: religious_coding` prefix WHERE APPLICABLE
>
> **Manifest:** author `full-ARPG-holy.manifest.json` with `expansion_id: "Exp-A.2"`, `track: "ARPG"`, `primary: "holy"`. Include in `expansion_sub_agent_summary` the per-candidate religious-coded vs non-religious-coded count distribution.
>
> **Output files:**
> - `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-01/full-ARPG-holy.jsonl`
> - `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-01/full-ARPG-holy.manifest.json`
>
> Validate JSONL well-formedness. Brief report-back: novel-row count, religious-vs-non-religious distribution, top 5 non-religious-coded candidates, yield score.

### 4.3 Exp-B.1 prompt (JRPG_isekai × shadow; no amendment — highest-value cell)

Use this VERBATIM as the prompt to Exp-B.1 sub-agent (sub-agent type `general-purpose`):

> You are a JRPG/isekai/anime-canon deep-expansion researcher commissioned by gandalf via legolas for the Reincarnated project's WS1A.Q18 flavor-pool research-and-lock wave Phase 3 expansion. Your scope: deepen the JRPG/isekai canon survey for **shadow** sub-element / flavor-element vocabulary beyond what Phase 1 Sampler-B already surfaced. This is the HIGHEST-VALUE expansion cell.
>
> **READ FIRST:** `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-01/sample-B.jsonl` — find all rows where `primary_element == "shadow"` and `track == "JRPG_isekai"`. These are the Phase 1 baseline candidates (~6 rows: mudo, drain, shadow, necro, void, shade).
>
> **Expansion focus areas (gandalf PG-1 ratification § 1.3):**
> - Solo Leveling shadow system DEEPER sub-vocabulary (genre-defining isekai shadow precedent):
>   - Named abilities: Shadow Exchange, Shadow Preserve, Shadow Linker, Shadow Save, Domain of the Monarch
>   - Shadow army hierarchy: Marshal / Commander / Knight / Soldier / Worker shadow ranks
>   - Iconic shadow names: Bellion, Beru, Igris, Tank, Tusk, Kaisel (mine for substrate-type=proper_noun pattern)
>   - Monarch / Sovereign / King tier vocabulary
> - Overlord undead vocabulary (Lower-Tier/Middle-Tier/Higher-Tier undead categorization; Death Knight / Skeleton Mage / Lich / Death Lord / etc.)
> - SMT/Persona shadow sub-vocab beyond mudo (Mudoon / Mudoonbra / Mamudo / Mamudoon; the deepening tiers)
> - That Time I Got Reincarnated as a Slime shadow / dark magic vocabulary
> - Berserk / Black Clover dark magic vocab (Griffith / Femto / Asta dark-magic specifics)
>
> **No gandalf amendment for this cell — surface novel candidates aggressively per the substrate's depth.**
>
> **Surface as many NOVEL candidates as the substrate supports.** Target 15-25 novel rows (highest-yield cell expected).
>
> **For each row, emit per the Phase 3 schema:**
> - `track`: literal `"JRPG_isekai"` for all rows
> - `primary_element`: literal `"shadow"` for all rows
> - `row_id`: `JRPG_isekai-shadow-<candidate>-EXP-<seq>`
> - `source_citations`: at least 1 per row
> - `substrate_type` enum: especially flag proper_noun pattern for Solo Leveling named shadows (Bellion / Beru / Igris)
> - `cross_primary_contamination`: list
> - `suggested_ranking_within_primary` (optional integer)
>
> **Manifest:** author `full-JRPG_isekai-shadow.manifest.json` with `expansion_id: "Exp-B.1"`. In `expansion_sub_agent_summary`, distinguish the THREE competing canonical layers gandalf flagged (SMT proper-noun layer / FF mechanical-keyword layer / Solo Leveling phenomenon + named-shadow layer).
>
> **Output files:**
> - `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-01/full-JRPG_isekai-shadow.jsonl`
> - `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-01/full-JRPG_isekai-shadow.manifest.json`
>
> Validate JSONL well-formedness. Brief report-back: novel-row count, per-canonical-layer count (SMT / FF / Solo Leveling), top 10 candidates by your ranking.

### 4.4 Exp-B.2 prompt (JRPG_isekai × holy; gandalf substrate-honest-WEAK caveat — no manufacture pressure)

Use this VERBATIM as the prompt to Exp-B.2 sub-agent (sub-agent type `general-purpose`):

> You are a JRPG/isekai/anime-canon deep-expansion researcher commissioned by gandalf via legolas for the Reincarnated project's WS1A.Q18 flavor-pool research-and-lock wave Phase 3 expansion. Your scope: deepen the JRPG/isekai canon survey for **holy** sub-element / flavor-element vocabulary beyond what Phase 1 Sampler-B already surfaced.
>
> **READ FIRST:** `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-01/sample-B.jsonl` — find all rows where `primary_element == "holy"` and `track == "JRPG_isekai"`. These are the Phase 1 baseline candidates (~5 rows; structurally dominated by proper-nouns + mechanical-keywords: hama, holy, radiance, aura, seraph).
>
> **Expansion focus areas (gandalf PG-1 ratification § 1.4):**
> - Mushoku Tensei healing magic tiers (cure / heal / cure-disease / resurrection — flag as mechanical_keyword)
> - Overlord divine-class ability system (Lower-Tier/Middle-Tier/Higher-Tier divine; Holy Smite / Heal / Greater Heal / Resurrection — flag as mechanical_keyword)
> - Final Fantasy White Magic vocabulary (Cure / Cura / Curaga / Holy / Banish / Esuna / Reflect)
> - SMT/Persona light/holy sub-vocab beyond hama (Hamaon / Mahama / Mahamaon — the deepening tiers)
> - Solo Leveling holy/light vocab (more limited than shadow)
> - Re:Zero / Konosuba / KonoSuba healing magic flavor
>
> **CRITICAL gandalf-amendment per PG-1 § 1.4 — substrate-honest-WEAK caveat:**
> **If the substrate is genuinely thin beyond proper-nouns + mechanical-keywords (no novel non-proper-noun, non-mechanical-keyword vocabulary surfaces beyond aura/seraph variants), report substrate-honest WEAK. DO NOT pressure for flavor-word manufacture. Genre vote is what it is.**
> - If the substrate IS thin, set `yield_score: "WEAK"` in manifest with `yield_rationale` explicitly stating "substrate-honest weakness — JRPG/isekai holy is genuinely dominated by proper-nouns + mechanical-keywords; no flavor-substrate manufacture attempted per gandalf PG-1 amendment"
> - If the substrate is NOT as thin as expected (novel non-proper-noun, non-mechanical-keyword vocabulary surfaces — e.g., divine wisp / celestial radiance / etc.), surface those candidates.
>
> **Surface as many NOVEL candidates as the substrate supports.** Target 5-15 novel rows (range reflects substrate-honest yield expectation).
>
> **For each row, emit per the Phase 3 schema:**
> - `track`: literal `"JRPG_isekai"` for all rows
> - `primary_element`: literal `"holy"` for all rows
> - `row_id`: `JRPG_isekai-holy-<candidate>-EXP-<seq>`
> - `source_citations`: at least 1 per row
> - `substrate_type` enum
> - `cross_primary_contamination`: list
> - `suggested_ranking_within_primary` (optional integer)
>
> **Manifest:** author `full-JRPG_isekai-holy.manifest.json` with `expansion_id: "Exp-B.2"`. In `yield_rationale`, explicitly name whether substrate-honest-WEAK fired or whether yield exceeded expectation.
>
> **Output files:**
> - `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-01/full-JRPG_isekai-holy.jsonl`
> - `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-01/full-JRPG_isekai-holy.manifest.json`
>
> Validate JSONL well-formedness. Brief report-back: novel-row count, substrate-honest-WEAK fire (yes/no), proper-noun vs mechanical-keyword vs flavor-substrate distribution.

### 4.5 Exp-C.1 prompt (tabletop_myth × wind; no amendment)

Use this VERBATIM as the prompt to Exp-C.1 sub-agent (sub-agent type `general-purpose`):

> You are a tabletop/mythological/alchemical-canon deep-expansion researcher commissioned by gandalf via legolas for the Reincarnated project's WS1A.Q18 flavor-pool research-and-lock wave Phase 3 expansion. Your scope: deepen the tabletop/myth canon survey for **wind** sub-element / flavor-element vocabulary beyond what Phase 1 Sampler-C already surfaced. This is the WEAKEST cell in the matrix (3 baseline rows); mythology is the source-of-truth for wind-distinct flavor.
>
> **READ FIRST:** `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-01/sample-C.jsonl` — find all rows where `primary_element == "wind"` and `track == "tabletop_myth"`. These are the Phase 1 baseline candidates (~3 rows: gust, tempest, cyclone).
>
> **Expansion focus areas (gandalf PG-1 ratification § 1.5):**
> - **Greek wind deity vocabulary (the Anemoi):** Boreas (north wind), Notus (south wind), Eurus (east wind), Zephyrus (west wind), Aeolus (keeper-of-winds)
> - **Norse wind vocabulary:** Kari (personification of wind), Njord (wind/sea), Vindsval (cold-wind), wind-related kennings
> - **MTG Blue storm cards:** Stormtide Leviathan, Time Spiral storm-mechanic cards, Counterspell variants, wind-coded blue creatures
> - **D&D Tempest Domain + wind-coded spells:** Gust of Wind, Wind Wall, Whirlwind, Conjure Elemental (air), Air Elemental, Djinni
> - **Pathfinder air-elemental + wind-related spells**
> - **MTG card vocab:** Aetherspouts, Cyclonic Rift, Tempest Djinn
> - **Wu Xing five-element references** for wind/air-adjacent (note: Wu Xing has Wood not Air; capture how Wu Xing handles wind/air absence)
> - **Western alchemical / Air-as-classical-element vocabulary**
>
> **No gandalf amendment for this cell — surface novel candidates aggressively per the mythological substrate's depth.**
>
> **Surface as many NOVEL candidates as the substrate supports.** Target 10-20 novel rows (mythology is rich here even though game-canonical sources are thin).
>
> **Special focus per gandalf PG-1 § 1.5:** wind is structurally the under-served primary across the whole 8-element canon. Mythology is the only place wind-PURE vocabulary survives at depth. Be thorough on Greek + Norse wind-deity vocabulary specifically.
>
> **For each row, emit per the Phase 3 schema:**
> - `track`: literal `"tabletop_myth"` for all rows
> - `primary_element`: literal `"wind"` for all rows
> - `row_id`: `tabletop_myth-wind-<candidate>-EXP-<seq>`
> - `source_citations`: at least 1 per row
> - `substrate_type` enum: especially flag mythological for wind-deity names; flag proper_noun for individual deity names
> - `cross_primary_contamination`: list
> - `suggested_ranking_within_primary` (optional integer)
>
> **Manifest:** author `full-tabletop_myth-wind.manifest.json` with `expansion_id: "Exp-C.1"`. In `expansion_sub_agent_summary`, note the Greek Anemoi as the substrate-distinct wind-PURE source and Wu Xing's absence-of-wind as a substrate-led data point.
>
> **Output files:**
> - `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-01/full-tabletop_myth-wind.jsonl`
> - `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-01/full-tabletop_myth-wind.manifest.json`
>
> Validate JSONL well-formedness. Brief report-back: novel-row count, mythological-vs-game-canon distribution, top wind-deity vocabulary, yield score.

---

## 5. Your acceptance (legolas)

1. **Mkdir if needed** (already exists from Phase 1; no-op)
2. **Commission 5 expansion sub-agents in single multi-agent invocation** per operational sequence § 4.2 parallel-fan-out discipline + Phase 3 dispatch § 2. All 5 prompts above (§ 4.1 / § 4.2 / § 4.3 / § 4.4 / § 4.5) used VERBATIM.
3. **Sustained-background-process discipline** per hive-mind protocol — sub-agents may take wall-clock time. Background-mode invocation recommended to insulate against stream timeout (per Phase 1 first-session learning).
4. **Absorb 5 expansion outputs** as they return.
5. **Validate JSONL well-formedness** for all 5 files: `python -c "import json; [json.loads(line) for line in open('<path>')]"` succeeds.
6. **Brief report-back to KR** (this dispatch's parent agent) — see "Completion record" template below.
7. **Phase 4 trigger:** KR fires Phase 4 elrond stats dispatch once your report-back lands; you do NOT fire Phase 4 in-seam (different seam).

**Commits:** auto-commit per CLAUDE.md addendum 2026-05-25 (in-scope Phase 3 work-products of authorized wave cycle). Push to remote remains Matt-explicit.

---

## 6. PG-1.5 in-flight amendment protocol (if needed)

Per operational sequence § 2 Phase 3 + gandalf PG-1 § 3:
- Soft cap: ≤6 expansion sub-agents. Current: 5. Margin: 1 slot for PG-1.5 in-flight extension.
- If during Phase 3 a sub-agent surfaces unexpected NARROW→EXPAND signal (per F-5 risk operational sequence § 7), surface to KR via report-back; KR routes Pattern A-light gandalf re-ratification (PG-1.5) for the 6th-slot extension.
- Wave continues without exit.

---

## 7. Out of scope

- **Phase 4 elrond statistical analysis** — separate KR dispatch when Phase 3 outputs land. Do NOT pre-author Phase 4 stats.
- **Phase 5 synthesis** — gandalf territory, not legolas.
- **In-flight prompt amendments** to expansion sub-agents after fire — sub-agents run as-prompted; if fundamental scope error emerges mid-run, surface to KR at completion.

---

## 8. Cross-seam contract change? (Principle 6)

**Answer:** NOT applicable. Phase 3 expansion outputs live entirely within `agentic_orchestration/legolas/research/`; no engine substrate / telemetry DB / loadout dict / export packet modified. Round-trip not applicable. The `sampler_notes` field per-row `wind_purity` and `track_alignment_concern` structured prefixes are in-scope per existing E.γ-prime schema (optional freeform field per elrond § 3.1).

---

## 9. References

- **Authoritative operational sequence:** `agentic_orchestration/gandalf/notes/2026-06-01-q18-flavor-pool-research-operational-sequence.md` (read § 2 Phase 3 + § 4.2 fan-out)
- **Gandalf PG-1 ratification (RATIFIED scope + amendments):** `agentic_orchestration/gandalf/notes/2026-06-01-q18-gate-1-triage-ratification.md`
- **Phase-0 elrond consultation (Phase 3 schema § 4 + Phase 1 schema § 3.1 + § 3.2):** `agentic_orchestration/elrond/consultations/2026-06-01-q18-flavor-pool-data-medium.md`
- **Phase 1 baseline samples (sub-agents read for context):** `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-01/sample-<A|B|C>.jsonl` + manifests
- **Phase 2 triage (legolas in-seam):** `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-01/sample-triage.md`
- **Wave-state file:** `agentic_orchestration/cycle-15-ws1a-q18-flavor-pool-research/wave-state.md`
- **Legolas OP:** `agentic_orchestration/operating-procedures/legolas.md`
- **Hive-mind protocol:** `agentic_orchestration/operating-procedures/hive-mind-protocol.md`

---

## Completion record (you append at completion)

```markdown
---

## Completion record
**Completed:** 2026-06-XX HH:MM
**Outputs:**
- `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-01/full-ARPG-wind.jsonl` + `.manifest.json`
- `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-01/full-ARPG-holy.jsonl` + `.manifest.json`
- `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-01/full-JRPG_isekai-shadow.jsonl` + `.manifest.json`
- `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-01/full-JRPG_isekai-holy.jsonl` + `.manifest.json`
- `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-01/full-tabletop_myth-wind.jsonl` + `.manifest.json`
**Total expansion row count:** <int>
**Per-expansion row counts:** A.1=<int>, A.2=<int>, B.1=<int>, B.2=<int>, C.1=<int>
**JSONL well-formedness validated:** yes/no
**Per-expansion yield score:** A.1=<STRONG|MEDIUM|WEAK>, A.2=<...>, B.1=<...>, B.2=<...>, C.1=<...>
**PG-1.5 in-flight amendment fired?:** yes (extension to 6th sub-agent) / no
**Substrate-honest-WEAK fire on Exp-B.2?:** yes / no
**Notable findings:** <text or "none">
**Routing back to KR:** proceed to Phase 4 elrond stats / hold for KR review / specific issue surfaced
```

After completion record append, KR fires Phase 4 elrond statistical analysis dispatch (with Phase-4 methodology lock per elrond Phase-0 consultation § 5 inlined).

---

## Completion record
**Completed:** 2026-06-01 (single-session execution; no wall-clock gap)
**Outputs:**
- `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-01/full-ARPG-wind.jsonl` + `.manifest.json`
- `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-01/full-ARPG-holy.jsonl` + `.manifest.json`
- `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-01/full-JRPG_isekai-shadow.jsonl` + `.manifest.json`
- `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-01/full-JRPG_isekai-holy.jsonl` + `.manifest.json`
- `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-01/full-tabletop_myth-wind.jsonl` + `.manifest.json`
**Total expansion row count:** 92
**Per-expansion row counts:** A.1=14, A.2=17, B.1=25, B.2=16, C.1=20
**JSONL well-formedness validated:** yes (python3 json.loads per-line; all 5 files pass)
**Manifest JSON validated:** yes (all 5 manifests parse; all required fields present)
**Per-expansion yield score:** A.1=MEDIUM, A.2=STRONG, B.1=STRONG, B.2=MEDIUM, C.1=STRONG
**PG-1.5 in-flight amendment fired?:** no (5 sub-agents; within ≤6 cap; no over-cap signal)
**Substrate-honest-WEAK fire on Exp-B.2?:** no — yield exceeded threshold; lux and celestial surfaced as novel non-proper-noun non-mechanical-keyword candidates; yield_score set MEDIUM (not WEAK) per substrate-honest assessment
**Wind-purity distribution on Exp-A.1:** PURE=7/14 (50%) — whirlwind, tornado, gale, zephyr, updraft, breeze, cyclone; STORM_FLEX=4/14 (29%) — squall, hurricane, tempest, (gust excluded from STORM); UNCLEAR=2/14 (14%) — blast, vortex; (1/14 is gust re-cited as PURE)
**Religious-coded vs non-religious-coded on Exp-A.2:** non-religious-coded=12/17 (71%) — radiance, solar, corona, empyrion, gilded, aureate, luminary, halcyon, lambent, stellar, lumen, lucent; religious-coded=4/17 (23%) — blessed, sacred, divine, consecrated; ambiguous=1/17 (6%) — solael (fictional deity)
**3-layer canonical distribution on Exp-B.1:** SMT proper-noun layer=4 rows (mudo Phase1 + mudoon/mamudo/mamudoon); FF mechanical-keyword layer=5 rows (drain Phase1 + negative burst/grasp heart/dark wisdom/death knight); Solo Leveling phenomenon+named-shadow layer=9 rows (shadow/shade Phase1 + exchange/preserve/linker/domain/bellion/beru/igris/monarch/sovereign); additional layers=7 rows (Overlord undead: lich/death lord + Berserk: femto/wraith/cimmerian + cross-source: abyss/miasma)
**Mythological-vs-game-canon distribution on Exp-C.1:** mythological=9/20 (45%) — Anemoi set (Zephyrus/Boreas/Aeolus/Notus/Eurus) + Norse (Kari/Vindsval/Njord) + alchemical (Sylph); game-canonical=10/20 (50%) — D&D/Pathfinder spells+creatures + MTG Blue cards; data-point=1/20 (5%) — Wu Xing absent
**Notable findings:**
- Greek Anemoi set (Zephyrus/Boreas/Aeolus/Notus/Eurus) is the single most substrate-distinct wind vocabulary contribution in the entire Phase 3 expansion — PURE wind-deity proper-nouns with 0 lightning contamination, providing directional/seasonal wind personality vocabulary absent from game-canonical sources
- Solo Leveling shadow ability vocabulary deepened substantially (Shadow Exchange/Preserve/Linker/Domain of the Monarch, Bellion/Beru/Igris named soldiers, Monarch/Sovereign authority-tier vocabulary)
- Grim Dawn Empyrion lane yielded non-religious holy proper-nouns (fictional sun-deity) as viable isekai-compatible holy vocabulary for Phase 5a synthesis
- Exp-B.2 JRPG holy substrate is genuinely dominated by mechanical-keywords but lux (Latin light-material) and celestial (astronomical phenomenon) are novel flavor-substrate entries; borderline MEDIUM/WEAK — Phase 5a synthesis should note thin citation depth for these two candidates
- Mudo and Hama families now complete: full four-tier structures (Mudo/Mudoon/Mamudo/Mamudoon; Hama/Hamaon/Mahama/Mahamaon) — mirror SMT shadow/holy vocabulary structure useful for Phase 4 symmetry analysis
- Wu Xing absence-of-wind captured as a substrate-led data point: Eastern five-element taxonomy does not develop wind as a primary; corroborates gandalf's 'wind as structurally under-served' observation
- Commit: `e2bed95`
**Routing back to KR:** proceed to Phase 4 elrond stats dispatch authoring

---

**End of Phase 3 legolas expansion-commissioning dispatch.**
