# Dispatch — 2026-05-22 — gandalf — Weapon-library cleaning-policy design review

**From:** knight-rider
**To:** gandalf
**Approved by:** Matt 2026-05-22 evening
**Estimated effort:** ~half-day (one session)
**Acceptance:** All 7 review items addressed with concrete recommendations; math-anchored substrate-cleanliness bar derived; commit + tag

---

## Context

Hive-mind weapon-library-import campaign completed Cycle 8 wind-down at **89,839 clean knowledge entries** across 24 source libraries (89.8% of 100K floor; ~6,000× the original 15-entry catalogue). Matt has decided: **accept at 89.8% and pivot to canonical normalization** (not Wave-4). Before the substrate feeds the engine's pattern-recognition / abstraction-analysis pipeline, it must be cleaned.

The cleaning pipeline plan is in **5 phases**:
- **Phase A — Substrate audit** (legolas commission; not yet fired — waiting on your rubric refinements)
- **Phase B — Cleaning policy design** (this dispatch + jack-ryan Gate 1 + elrond schema authoring)
- **Phase C — Quarantine triage** (Matt-decisions after Phase A returns)
- **Phase D — Cleaning pipeline build** (elrond Pattern-B execution)
- **Phase E — Emergent-pattern analysis** (your Pattern-6 axis discovery on cleaned substrate)

You are the design-track steward for Phase B; this dispatch asks you to review the proposed taxonomies + rules + cleanliness bar BEFORE legolas's Phase A audit fires, so the audit rubric incorporates your input.

The 130K `wikipedia-unfiltered` quarantine has been **dump-then-deleted** this session per Discipline #11 audit-preservation pattern (compressed JSONL archive at `legolas/research/.../quarantine-archives/`; DB DELETE+VACUUM executed; DB shrank from 523 MB → 136 MB). DB now holds exactly the 89,839 clean entries + 5,162 weapons + 43,602 reference images.

## Required reading before starting

1. `agentic_orchestration/weapon-library-import-hive-mind-state.md` — final Cycle 8 state; per-source counts; PID disposition
2. `agentic_orchestration/weapon-library-import-wind-down-summary-2026-05-22.md` — Cycles 0-8 narrative (esp. § 4 Discipline observations, § 5 License posture)
3. `agentic_orchestration/weapon-library-import-sample-rows-2026-05-22.md` — Matt's 3-rows-per-source review doc (concrete examples per source)
4. `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/findings-summary.md` — original legolas discovery findings
5. `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/schema.sql` (v1.1.0) — current DB schema
6. `canonical/story/engine-as-general-serial-content-product-2026-05-22.md` — engine architecture frame
7. Decisions-log entries relevant to gear-HEAVY promotion + vast-library pivot (2026-05-22 gandalf canonical locks)

## Math-before-code

This is a **design dispatch**, not an execution dispatch — no code. But Review Item #4 (substrate-cleanliness bar) **requires** math-anchored reasoning. See § Scope for the specific math expected.

## Cross-seam contract change? (Principle 6 gate)

**No.** This dispatch produces design recommendations only. No schema changes are executed here; no telemetry contract is touched; no fight_log / loadout dict modified. Elrond authors the actual schema migration (ALTER TABLE) in Phase D execution dispatch.

**Round-trip: not applicable — no cross-seam contract change in this dispatch.**

## Scope (7 review items)

### Item 1 — Three-bucket `weapon_kind` taxonomy

Proposed enum: `category` | `unique` | `named_template` | `unknown`

- **category:** "longsword", "AK-47", "katana", "halberd" — type definitions; engine generates instances from these.
- **unique:** "Excalibur", "Mjolnir", "Joyeuse", "Honjō Masamune", "Curtana" — specific named historical/mythological individuals. NOT used in category sampling.
- **named_template:** D&D "Hammer of Thunderbolts", "Vorpal Sword", "Holy Avenger" — narratively named but stat-block-template; consumable as engine categories. (Matt's third-bucket decision.)
- **unknown:** Pre-classification default.

**Your review:** Does this match your model of how the engine consumes weapons via category sampling? Are there edge-case patterns I'm missing that need a fourth bucket or a refined definition? Concrete examples from the substrate (sample-rows doc) welcome.

### Item 2 — Wieldability filter rules

Matt's locked rule: *"If a single humanoid can carry and fire/wield in active use, it's wieldable."* Shoulder-support counts (RPG-7 / M249 / SMAW in); handheld projectiles count (grenades, bombs, throwing axes in). Excluded: mortars, tripod-MGs in emplaced role, artillery, naval guns, mounted turret weapons.

Proposed enum: `one_hand` | `two_hand` | `either` | `no` | `mount_required` | `unknown`

Per-source signal inventory:
- Wikidata Q-items: `mass`, `mounting type`, `crew`, subclass inheritance (artillery / vehicle weapon / naval gun)
- Royal Armouries: object metadata sometimes includes scale/weight
- Cataclysm-DDA: explicit volume + weight + handedness in JSON
- odin-army-tradoc: crew count and mount platform fields
- Other sources: rule-based regex on `weapon_subclass` text

**Your review:** Anything missing from the active-wield definition? Edge cases that need explicit handling (e.g., warhammer two-handed flails, oversized polearms, mounted ranged like attached crossbows, throwable two-handed like javelins, etc.)? The wieldability filter is **tag-and-keep** (not drop) — non-wieldable rows preserved for potential non-humanoid expansion future work.

### Item 3 — Museum-as-category-by-default rule + named-unique edge cases

Matt's locked rule: *"All museum weapons are categorical representations unless obviously otherwise (e.g., Charlemagne's Broadsword)."*

So Royal Armouries object IX.1234 ("Sword, 14th century English") → category-representative of "longsword" or similar.
But Royal Armouries object holding "Joyeuse" → unique.

**Your review:** What edge-case patterns count as "obviously named"? Concrete categorization framework (e.g., regex on display_name for proper-noun-without-type-descriptor; presence of known historical name in description text; cultural-lineage signaling royal/imperial ownership). Surface as many concrete edge cases as you can think of from your knowledge of historical/mythological weapons that may appear in the substrate — these become the "named unique" detection allowlist.

### Item 4 — Math-anchored substrate-cleanliness bar

**THE LOAD-BEARING ITEM.** Knight-rider asked, Matt deferred to you. Quote: *"Invoke gandalf to decide based on mathematical knowledge of the pattern recognition planned algorithm."*

The question: given the engine's pattern-recognition algorithm operates on the ~89K cleaned rows (filtered to ~70-80K active substrate after wieldability + unique exclusions), **what's the maximum tolerable rate of:**

(a) **False-positives in active substrate** (non-weapon rows mis-classified as weapons; e.g., "Bose headset" type slips)
(b) **Duplication within canonical-merged set** (multiple un-merged source-records of the same canonical entity)
(c) **Field-coverage gaps** (rows with missing display_name / description / cultural_lineage / structured_properties)
(d) **Mis-classified `weapon_kind`** (uniques mis-tagged as categories, or vice versa)

…before the pattern-recognition algorithm's abstraction outputs measurably degrade?

**Required math:** anchor your bar to concrete reasoning. For example:
- If the algorithm uses clustering, what cluster-purity degradation is acceptable as a function of input FP rate?
- If the algorithm computes axis loadings via aggregate statistics, what's the noise floor where loadings stop being reliable?
- If category sampling uses N=X rows per category, what's the minimum effective sample size after dedup + filter?

Output: 4 numbers (or ranges) with derivation. These become Phase A audit acceptance gates AND Phase D cleaning pipeline acceptance gates.

I expect this to be the meaty section of your dispatch. The numbers anchor everything downstream — too lax and the substrate is dirty; too strict and we never declare ready.

### Item 5 — Cultural-lineage canonical taxonomy

The substrate's 24 sources tag culture differently:
- royal_armouries: period + culture text ("18th century, English", "Edo period, Japan")
- wikidata: Q-items for cultures (Q145 = United Kingdom, Q17 = Japan, etc.)
- wikipedia: Category strings ("Category:Japanese swords", "Category:Medieval European weapons")
- fextralife: none / game-canon framing only
- odin-army-tradoc: country-of-origin codes (USA, RUS, FRA, etc.)
- nick-aschenbach: D&D campaign-setting tags
- cataclysm-dda: post-apocalyptic / improvised tags
- bsdata-warhammer-aos: faction tags
- (etc.)

**Your review:** propose a canonical taxonomy these collapse into. Suggested axes (open to your revision):
- **historical_period** (pre-classical / classical / medieval / early-modern / industrial / modern / post-modern / fictional)
- **cultural_lineage** (european / east-asian / south-asian / middle-eastern / african / north-american-indigenous / pacific / fantasy-generic / sci-fi-generic / etc.)
- **register** (historical / military-modern / fantasy / sci-fi / mythological)

How do the 24 sources' raw tags map to this taxonomy? This is Pattern-6 axis-discovery territory — feel free to lean on your existing work there.

### Item 6 — Variant-of-type collapse policy

When Phase A audit surfaces samples of variants like:
- Pompeii gladius / Mainz gladius / Fulham gladius (sub-variants of gladius)
- Type X / Type XIa / Type XII Oakeshott swords (typological sub-variants)
- AK-47 / AKM / AK-74 (model variants)
- Katana / Tachi / Wakizashi / Tantō (size-class siblings)

…what's the policy?

Options:
- **(A) Keep all as separate canonical entries**, with `related_entries` populating variant relationships
- **(B) Collapse to single canonical parent**, with sub-variant data preserved as `structured_properties` attributes
- **(C) Tiered:** strict variants (Pompeii/Mainz/Fulham gladius) collapse to parent; model variants (AK-47/AKM) stay separate as canonical entries

Matt's direction: *"Let's surface samples of these and decide in flight."* — so the Phase A audit must surface concrete sample examples for review. Your job here: define the **policy framework** so that when Phase A surfaces examples, the in-flight Matt+gandalf decision has a clear option-set to choose from.

### Item 7 — Pattern-6 axis discovery interaction (sequencing)

Does cleaning sequence before or after Pattern-6 axis discovery?

- **Pre-cleaning axis discovery:** Run Pattern-6 on dirty substrate; use discovered axes to inform cleaning policy.
- **Post-cleaning axis discovery:** Clean first; run Pattern-6 on clean substrate; trust the axes more.
- **Iterative:** Both, with feedback loop.

**Your review:** confirm sequencing. My instinct is post-cleaning (cleaner axes), but Pattern-6 may need dirty substrate for some signals. You know.

## Acceptance criteria

- [ ] All 7 review items addressed with concrete recommendations (not "TBD" or "depends")
- [ ] Item 4 produces 4 numeric thresholds (or numeric ranges) with derivation math
- [ ] Item 3 produces a named-unique detection allowlist with ≥10 concrete examples
- [ ] Item 5 produces a canonical cultural-lineage taxonomy with explicit mapping from each of the 24 sources' raw tags
- [ ] Item 6 produces a policy framework (option-set, not a single answer) with clear decision-criteria for Phase A in-flight review
- [ ] Output committed as `canonical/story/cleaning-policy-design-2026-05-22.md` (or similar canonical path of your choosing)
- [ ] Round-trip: not applicable because this dispatch produces design recommendations only; no inter-seam contract changes
- [ ] Tag: `gandalf/cleaning-policy-design-review-2026-05-22`

## Out of scope (explicit non-goals)

- **DO NOT** author or execute schema migrations (elrond's seam in Phase D)
- **DO NOT** author or execute cleaning pipeline code (elrond's seam in Phase D)
- **DO NOT** classify the 89,839 substrate rows yourself (legolas's job in Phase A)
- **DO NOT** decide Pompeii/Mainz/Fulham gladius collapse-or-keep here (Matt + you decide in-flight after Phase A surfaces examples)
- **DO NOT** dispatch downstream agents (knight-rider handles next-step orchestration after your return)

## Open questions for the agent to resolve

These are surface for you to think through and document; some may not have clean answers:

1. What if the pattern-recognition algorithm's tolerance for FP rate varies by classification dimension (e.g., it tolerates 5% FP on wieldability but only 1% on weapon_kind)? Output should disambiguate per-dimension.
2. Are there ANY known dimensions where the substrate as-is is ALREADY at acceptable cleanliness (no Phase D work needed)? E.g., maybe `historical_period` is already well-distributed and clean.
3. Should "named_template" weapons (D&D Hammer of Thunderbolts pattern) be sampled at higher frequency than ordinary categories during axis discovery, since they're intentionally designed-with-purpose? Or treated equivalently?
4. Cultural-lineage taxonomy interaction with the engine's `cultural_lineage` field on `weapons` table — should they share enum values? Already-canonical-elsewhere? Worth a quick schema-alignment check.

## References

- `agentic_orchestration/weapon-library-import-hive-mind-state.md` (live state)
- `agentic_orchestration/weapon-library-import-wind-down-summary-2026-05-22.md`
- `agentic_orchestration/weapon-library-import-sample-rows-2026-05-22.md` (3-rows-per-source reference)
- `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/schema.sql` (v1.1.0)
- 2026-05-22 gandalf canonical locks (engine-as-general-serial-content-product; gear-HEAVY-promotion; vast-library-pivot; hive-mind-protocol; Pattern-6 axis discovery)
- ADR-001 (tag prefix convention); ADR-006 (read-only by default for non-Matt-approved DB writes)
- Discipline #1 (math-before-code); Discipline #11 (audit-preservation; empirical inspection)

---

## Tag at completion

```
gandalf/cleaning-policy-design-review-2026-05-22
```

(Seam-prefix per ADR-001; intermediate design artifact; not Matt-milestone tag.)

## What happens after you return

Knight-rider:
1. Reads your output `canonical/story/cleaning-policy-design-2026-05-22.md` (or your chosen path)
2. Refines Phase A audit rubric per your taxonomies + math-anchored cleanliness bar
3. Authors + dispatches legolas Phase A audit dispatch
4. Coordinates Matt-side review when Phase A surfaces in-flight decisions (uniques edge cases, variant collapse, etc.)
5. Authors elrond Pattern-B dispatch for Phase D after Phase A + Phase C settled

You are not blocked on legolas; your design pass is independent. Take the time you need.

---

**Signed:** knight-rider (dispatch authored 2026-05-22 evening; cleaning-policy planning phase active)
