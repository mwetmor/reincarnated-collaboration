# WS1A.Q18 PG-2 — Gandalf Phase 4 Stats Ratification

**STATUS:** RATIFIED (dataset sufficient; proceed to Phase 5a synthesis draft authoring)
**Date:** 2026-06-01
**Author:** gandalf (story-and-design steward)
**Phase-gate:** PG-2 (post-Phase-4 stats sufficiency ratification)
**Mode:** Pattern A-light verdict (in-wave sub-agent invocation; ≤2-hour bound)
**Authority:** Matt 2026-06-01 verbatim "hand to KR to fire the wave" + hive-mind decision-routing Matt 2026-05-23 (gandalf design-side seam authority for PG-2 scope; Matt NOT in loop here — Matt's touchpoint is PG-3 at Phase 5b Pattern B)
**Companion docs:**
- `agentic_orchestration/elrond/analysis/element-flavor-mapping-stats-2026-06-01.md` (THE ARTIFACT RATIFIED)
- `agentic_orchestration/elrond/analysis/q18_flavor_stats_results_2026-06-01.json` (raw per-step results — spot-checked)
- `agentic_orchestration/elrond/consultations/2026-06-01-q18-flavor-pool-data-medium.md` § 5 (methodology lock executed)
- `agentic_orchestration/gandalf/notes/2026-06-01-q18-gate-1-triage-ratification.md` (PG-1 forward-note honored)
- `agentic_orchestration/gandalf/notes/2026-06-01-q18-flavor-pool-research-operational-sequence.md` § 2 Phase 4 phase-gate
- `agentic_orchestration/cycle-15-ws1a-q18-flavor-pool-research/wave-state.md`
- `~/Games/reincarnated-engine/data/seasonal_elements/pool.json` (cross-checked: fire=20 / water=11 / earth=22 / wind=7 allow-list — matches stats verdict § 5.1 exactly)

---

## 0. TL;DR + routing

**Verdict: RATIFIED.** Elrond's Phase 4 statistical analysis is methodology-faithful to the PG-0 § 5 lock, substrate-grounded, and produces a sufficient synthesis-curation core (31 high-confidence candidates + per-primary T6 floors + contamination matrix + cluster fingerprints). Dataset proceeds to Phase 5a synthesis draft authoring (gandalf seam).

**No amendment-loop fired.** No Phase 3 expansion gap warrants re-firing. All 9 deliverables are sound.

**Design-side read on 7-vs-8 (WEAK-8):** the empirical signal is correctly bounded — physical passes quantitative axes but is qualitatively a damage-type taxonomy, not a flavor pool. Phase 5b Pattern B should surface this to Matt as a **two-architecture choice**, not a binary 7-vs-8. I have a recommendation lean (§ 3 below) which I will surface in Phase 5b framing — not as pre-commitment, as substrate-honest design read.

**Routing instruction for KR:** RATIFIED — fire Phase 5a synthesis draft authoring (gandalf seam). I will author at `agentic_orchestration/gandalf/notes/2026-06-XX-q18-flavor-pool-research-synthesis.md` per operational sequence § 2 sub-phase 5a.

---

## 1. Per-deliverable assessment (9 elrond deliverables per dispatch § 2)

### 1.1 Per-primary candidate frequency distribution — SOUND

Citation-weighted aggregation (recognizability × citation count) over (primary, candidate) combined rows is methodology-faithful to PG-0 § 5. Per-primary counts {fire:15, water:13, earth:10, wind:35, lightning:12, holy:38, shadow:35, physical:13} are internally consistent with row counts {17, 17, 14, 47, 16, 49, 42, 15}.

**Design-side read:** the spread reflects substrate-honest yield: deep-expansion primaries (wind, holy, shadow) surface 35-38 candidates; baseline-only primaries (fire, water, earth, lightning, physical) cluster at 10-15. This asymmetry is structural (Phase 3 expansion concentration) and downstream synthesis must honor it as designed-in, not noise.

Spot-check on fire ranking: ember (R=3 × 2 cites + R=2 × 3 cites = wait — actually 12 weighted from material substrate, recurring) → confirmed by raw JSON `per_primary_frequency.fire`. Cinder also confirmed.

Wind top 10 are all storm-flex cluster (tempest/cyclone/whirlwind/gale/gust/squall/zephyr/hurricane/tornado/vortex) — this confirms my PG-1 forward concern (§ 8.2 of stats verdict) that wind's HIGH yield is concentrated in storm-flex, not wind-PURE. Phase 5a synthesis must preserve this asymmetry in curation language.

### 1.2 Cross-primary contamination matrix — SOUND

Symmetric construction from `cross_primary_contamination` union with primary_element produces the 8×8 matrix correctly. The water↔wind=7 finding is the largest off-diagonal and validates PG-1 § 2 override surface 1 (wind/storm/water conflation as genre-canonical tension). Three secondary contamination lanes (fire↔shadow=3, earth↔shadow=3) are substrate-honest sub-elements of necromancer-fire and decay-earth genre patterns.

**Design-side concern foregrounded for Phase 5a:** the water↔wind=7 set (hurricane, mist, njord, notus, squall, stormtide, tempest) is the single largest curation-decision point downstream. Phase 5a must explicitly route each candidate to a PRIMARY slot — splitting hurricane/squall/stormtide to wind, mist/njord to water, with explicit synthesis-rationale per candidate. This will surface in synthesis as a designated section, not buried in per-primary lists.

Physical's 1-cell contamination row (only `force` ↔ wind via D&D kinetic semantic) is itself a design-relevant signal — physical actively does not flex. Composes with 7-vs-8 verdict.

### 1.3 Cluster analysis per primary — SOUND with design-side note

Substrate-type concentration table (§ 4.1) is the load-bearing axis for the 7-vs-8 verdict. Physical's 0.85 mechanical_keyword modal share is sharply outlier vs rotating primaries' 0.32-0.70 spread. **This is the right empirical axis for the qualitative verdict.**

HDBSCAN cluster outputs (§ 4.2) are coherent:
- Holy's single dominant cluster (n=22) + 3 sub-clusters: confirms the radiance/divine/sacred semantic anchor + the religious-coded / non-religious split — load-bearing for PG-1 surface 2 (Reincarnated's tone-decoupling room).
- Shadow's 7 clusters: confirms PG-1 surface 3 (SMT proper-noun / FF mechanical / Solo Leveling phenomenon three-canonical-layer competition). Phase 5a synthesis must pick the layer-weighting consciously.
- Wind's fragmented 7 clusters + 11 noise: confirms wind's heterogeneous substrate (storm-flex / Greek-Anemoi / atmospheric phenomenon / ailment-adjacent). Curation must lean on cross-track agreement, not raw yield.
- Physical's single dominant cluster (n=11) + 2-element side cluster: lowest diversity. Composes with substrate-type analysis to corroborate WEAK-8.

**Design-side read:** the cluster fingerprints provide Phase 5a synthesis with structural per-primary shape recommendations:
- Holy → CORE-+ -SATELLITES shape (strong radiance core; pick non-religious satellites for tone)
- Shadow → LAYER-PICK shape (pick weighting across SMT / FF / Solo Leveling)
- Wind → STORM-FLEX-CURATED shape (acknowledge storm conflation explicitly; cross-track-only vocab for wind-PURE; storm subset clearly labeled as flex)
- Physical → MONOLITHIC-TAXONOMY shape (if kept as 8th primary, treat as damage-type pool; if collapsed to 7-primary, the cluster IS the kinetic-physical sibling-vocab cross-element)

### 1.4 Cardinality recommendations per primary — SOUND with substrate-led discipline-composition note

T_principal=6 calibration is substrate-led (against pool.json allow-list reference; cross-checked). T_permissive=4 + T_strict=9 reporting gives Phase 5a synthesis flexibility — strong methodology choice.

T6 floor cardinality {fire:8, water:10, earth:3, wind:21, lightning:11, holy:19, shadow:17, physical:9} is internally consistent and substrate-honest. The asymmetry against existing pool (fire:8 vs pool:20; water:10 vs pool:11; earth:3 vs pool:22; wind:21 vs pool:7) IS the substrate-led finding: pool was authored before genre-vote evidence, leading to fire+earth over-curation and wind under-curation.

**Design-side read for Phase 5a:** the synthesis curation target is NOT to land on T6 floors. The floors are research-derived empirical bounds. The curation target is per-primary "natural cardinality" — the depth where vocabulary substrate stops adding meaningful flavor differentiation. Likely Phase 5a recommendation lands:
- fire: ~12-15 (preserve pool depth; add cross-track high-confidence ember/cinder)
- water: ~12 (close to T6; add high-confidence tide/torrent/glacial/brine; possible aqua/frost/chill)
- earth: ~15-18 (lean on pool depth; T6=3 is research-thin not substrate-thin)
- wind: ~10-12 (3× existing pool but DO NOT push to T6=21; storm-flex curation needs design-decision per candidate)
- lightning: ~10 (T6=11 is the natural depth; arc/static/surge/volt/bolt/lightning/shock/spark/thundara/thunder core)
- holy: ~10-12 (radiance core + non-religious satellites; resist religious-coded bias)
- shadow: ~12 (3-layer pick; void/shade/umbra cross-track core + 1-2 layer-specific representatives)
- physical: depends on PG-3 architectural commitment

I will NOT pre-commit these numbers in synthesis. They are my design-side starting frame for Phase 5a curation; numbers move per audit of actual candidates.

### 1.5 Track-source weighting validation — SOUND; PG-1 § 5 forward-note HONORED

Per-track weighted-score shares (ARPG 36.6% / JRPG_isekai 37.2% / tabletop_myth 26.2%) are near-balanced; ARPG and JRPG_isekai parity is correct given Phase 3 expansion concentration. Tabletop's 26.2% is the substrate-honest narrower-yield but it IS the contamination-matrix rigor anchor as I forward-noted.

Elrond's suggested Phase 5a synthesis multipliers (ARPG=1.0 / JRPG_isekai=1.15 / tabletop_myth=1.10) honor my PG-1 § 5 forward note exactly. **PG-1 forward-weighting note is HONORED.** I will apply these as tie-breaking weights, not as primary-score adjustments.

§ 6.4 per-track substrate-type bias observation (ARPG → phenomenon + mechanical_keyword; JRPG → proper_noun + mythological; tabletop → material + mythological + D&D formal damage types) is genre-canonical and useful for synthesis curation routing.

### 1.6 7-vs-8 empirical answer (WEAK-8) — SOUND, correctly bounded as EMPIRICAL not ARCHITECTURAL

This is the load-bearing verdict for Phase 5b Pattern B. Detailed gandalf-design read in § 3 below.

**Empirical bounding check:** § 7 of stats verdict explicitly carries the WEAK-8 verdict as EMPIRICAL ANSWER + § 7.7 explicitly carries the architectural-commitment forward as NOT-a-recommendation-out-of-scope. Disposition is methodologically clean. Phase 5b Pattern B with Matt owns the architectural-commitment decision.

### 1.7 Per-primary statistical confidence — SOUND; my design-side read matches the named primaries

- **earth=MEDIUM (14 rows just under 15 threshold):** matches my design-side read. Substrate-led discipline backstops via pool depth (22 allow-list).
- **physical=DEGRADED (by-construction; Phase 3 deliberately excluded):** matches my design-side read. This is a methodology-deliberate degradation, not a research failure.
- **wind=HIGH-with-caveat (storm-flex yield, structural thin wind-PURE):** matches my PG-1 § 2 surface 1 exactly. The caveat is substrate-honest.

§ 8.3 carrying physical's DEGRADED status as combined by-construction + WEAK-8 substrate signal is the right framing for Phase 5b Pattern B.

### 1.8 Bootstrap stability — SOUND

200-iteration resample bootstrap; median stabilities 0.63-0.88. Earth's 0.88 reflects 3-candidate cross-track-confirmed core. Other primaries' 0.63-0.66 is the citation-sparse-dataset typical range. 31 high-confidence candidates (score≥T6 AND tracks≥2) as synthesis-curation core is the right operational handoff.

**Design-side read:** the bootstrap stability validates the high-confidence core as a robust starting point for synthesis. Single-track borderline candidates require designer-judgment per § 1.9 — bootstrap is silent on those.

### 1.9 Borderline candidate audit — SOUND with one design-side foregrounding

§ 10.1: lux + celestial both flagged correctly as SINGLE-TRACK BORDERLINE (JRPG_isekai only; score=4; below T6). § 10.3 correctly routes to PG-3 if non-religious holy curation is synthesis priority.

§ 10.2: 92 total single-track borderline across all primaries is itemized in raw JSON. **Design-side concern foregrounded:** Greek Anemoi vocabulary (aeolus / boreas / notus / zephyrus / eurus) likely all single-track tabletop-only. These are exactly the kind of mythological depth the PG-1 § 5 tabletop weight elevation was forward-noted for. Phase 5a synthesis MUST treat the Greek Anemoi as designer-judgment surface, not auto-bucket below T6.

Similarly, Solo Leveling shadow vocabulary (per Exp-B.1 manifest at 9 candidates) is single-track JRPG_isekai but isekai-genre-defining for Reincarnated's D10 positioning.

**Disposition:** single-track-borderline is NOT a drop signal. It's a synthesis curation surface. Stats verdict § 10.3 carries this correctly.

---

## 2. Methodology fidelity check

### 2.1 PG-0 § 5 methodology lock — HONORED

| PG-0 § 5 spec | Phase 4 execution | Status |
|---|---|---|
| Cluster method: HDBSCAN gated count≥8 | All 8 primaries qualified; HDBSCAN ran | ✅ |
| Frequency weighting: sum(recognizability × citation count) per row, combined on (primary, candidate) | § 2 method block confirms | ✅ |
| Contamination matrix: symmetric, primary_A↔primary_B = count of candidates with both A and B in flex set | § 3 construction matches | ✅ |
| Cardinality floor: count of candidates with citation-weighted score ≥ T, T substrate-calibrated against pool.json | § 5.1 + § 5.2 confirm | ✅ |
| Acceptance criteria upfront: variance threshold on bootstrap-stability + 3-track agreement + per-primary confidence-degradation naming + borderline audit | § 9.4 + § 8 + § 10 confirm | ✅ |

**Methodology lock fidelity: PASS 5/5.**

### 2.2 PG-1 § 5 forward weighting note — HONORED

Elrond explicitly cites my PG-1 § 5 forward note (JRPG_isekai elevated 1.15; tabletop_myth elevated 1.10) and applies it as advisory tie-breaking, not primary-score adjustment. This is exactly the right disposition. **PG-1 forward-weighting note: HONORED.**

### 2.3 Phase 3 methodology-deviation observation — SOUND disposition

§ 12 reports 0 schema validation issues across 92 Phase 3 rows; citation density 1.78 vs Phase 1's 1.66 (Phase 3 actually marginally higher); substrate-type enum faithfully applied; contamination lists richer. **Disposition: NO data-quality concerns.**

Design-side concur. The legolas-direct execution path produced data of comparable or higher quality vs the sub-agent fan-out path would have. Surfacing as operational-observation for KR + ops awareness is appropriate (§ 12.3) but does NOT warrant re-routing the wave.

### 2.4 F-6 contingency disposition — CORRECT

§ 11 reports F-6 NOT FIRED. Data shape is firmly quantitative-amenable (0 schema validation issues; structured citations; recognizability spread; substrate-type enum populated; contamination lists structured). All 4 dispatch § 2 deliverables produced from structured fields. **F-6 disposition: CORRECT.**

---

## 3. 7-vs-8 design-side read (Phase 5b Pattern B framing input)

This is the most important section of this verdict. Phase 5b Pattern B with Matt is where the architectural-commitment decision lands. My design-side read informs the Pattern B framing — it is NOT pre-commitment.

### 3.1 The empirical signal in plain terms

Physical surfaces in all three tracks with comparable row counts and citation depth to rotating primaries (15 rows, 13 candidates, weighted score 76). Quantitatively, it qualifies as a primary element.

But the vocabulary it surfaces is **fundamentally different in kind** from rotating primaries:
- 0.85 modal share concentrated in `mechanical_keyword` substrate (vs rotating 0.32-0.70)
- Vocabulary IS the D&D 5e damage-type taxonomy (pierce / piercing / slash / slashing / bludgeoning / sever / strike / force / crush / bleed)
- Near-zero contamination (1 cell only via `force` to wind)
- Single dominant HDBSCAN cluster (n=11) — lowest diversity in the dataset
- The cluster captures the damage-taxonomy en bloc

Rotating primaries flex, contaminate, distribute across substrate types, fragment into multiple clusters. Physical does the opposite: monolithic, taxonomic, semantically isolated, structurally non-flexing.

### 3.2 Genre-design reference points (gandalf cross-house knowledge)

**Diablo lineage:**
- D1: physical was implicit (melee/ranged baseline; no "physical damage type" affix system)
- D2: physical damage as a damage-type alongside elemental (fire/cold/lightning/poison); affix vocabulary leaned mechanical (open wounds, crushing blow, deadly strike) — NOT flavor-pool-shaped
- D3: physical as damage type; legendary affixes carry mechanical vocab (pierce/strike/cleave) but feel different from "ash" or "frost" affixes
- D4: physical/non-physical split for many skill modifiers; physical sub-types not surfaced as flavor
- Immortal: same pattern

**PoE 1+2:**
- Physical damage is a base damage type; physical sub-types (pierce/bleed/impale/maim) are AILMENTS not flavor sub-elements. Ignite/Shock/Chill are elemental ailments; bleed/impale/maim are physical ailments. PoE treats them as a different kind of thing semantically.
- This is the strongest genre-canonical precedent: **physical doesn't get a flavor pool because its sub-vocabulary lives in ailment/mechanical space.**

**Grim Dawn:**
- Physical damage + bleed damage + pierce damage as sibling damage types. The "physical flavor" is the damage-type-sibling architecture, NOT a sub-element pool.

**Last Epoch / Lost Ark / Wolcen:**
- Consistent: physical sub-types are damage-classification, not flavor.

**FF / SMT / Mushoku Tensei:**
- FF: physical attacks have no flavor sub-element; spells get the flavor; attacks get the weapon.
- SMT: phys / fire / ice / elec / wind / light / dark + healing/support. Phys is its own thing — Megaton Press / God's Hand / Heat Wave / Hassou Tobi are MECHANICAL named skills, not flavor sub-elements.
- Mushoku Tensei: "sword magic" + physical combat have weapon-style schools (water-god / sword-god / north-god) — these are TECHNIQUE schools, not flavor sub-elements.

**Genre-canonical convergence: physical does not flavor-pool. It taxonomizes, schools, or weapon-anchors.**

### 3.3 My design-side recommendation lean (for Phase 5b Pattern B framing)

Two architectures are substrate-supported:

**Architecture A: 7-primary rotating + physical-as-taxonomy-sibling (my soft lean)**
- 7 rotating primaries (fire / water / earth / wind / lightning / holy / shadow) each carry a flavor pool of substrate-honest vocabulary
- Physical exists as an 8th DAMAGE TYPE in the engine taxonomy (for damage resists, mitigation, ailment routing) but does NOT carry a "flavor pool" in the same sense
- Physical kits flavor through WEAPON-FORM substrate (sword/spear/bow/axe; Reincarnated already has this surface) + AILMENT vocabulary (bleed / impale / sever as physical-ailments analogous to ignite/shock/chill as elemental-ailments)
- This matches genre-canonical convention (Diablo, PoE, FF, SMT all do this)
- Substrate-honest because physical's empirical vocabulary IS this shape

**Architecture B: 8-primary with physical-as-damage-type-flavor (asymmetric structure)**
- Acknowledge physical's flavor pool is qualitatively different (damage-taxonomy: pierce / slash / bludgeon / sever / force)
- Treat the asymmetry as intentional design — every primary has a flavor pool; physical's is mechanical not phenomenological
- This preserves symmetric primary count (cleaner mental model)
- Risk: player experiences asymmetry as flavor-rough-edges ("why does fire feel different than physical?")

**My lean: Architecture A.** Reasoning:
- The empirical substrate is unambiguously taxonomic for physical. Forcing a flavor pool semantic onto taxonomic substrate is the failure mode of "make all primaries look the same on paper at cost of substrate-honesty"
- Genre-canonical convention is strongly Architecture A; isekai+ARPG players already have this mental model
- Reincarnated's spirit-swap-as-class-differentiation already places kit identity at the (primary × form × sub-element) intersection. Physical-as-taxonomy-sibling preserves that intersection cleanly: physical kits differentiate via weapon-form and physical-ailment vocabulary; elemental kits differentiate via flavor sub-element vocabulary
- WS1A.4 (per-skill LLM flavor judgment) will be cleaner against 7 rotating flavor pools + 1 damage-taxonomy than against 8 asymmetric pools

**HOWEVER — this is a soft lean, NOT pre-commitment.** Phase 5b Pattern B should surface BOTH architectures to Matt with the empirical evidence in this verdict + the genre-canonical convergence + my lean reasoning. Matt's call.

### 3.4 What Phase 5b Pattern B should foreground for Matt

- The empirical WEAK-8 signal (substrate is genuinely asymmetric)
- The two architectures (A: 7+taxonomy / B: 8-with-asymmetric-pool)
- Genre-canonical convergence (Diablo, PoE, FF, SMT all converge on A-shape)
- The Reincarnated-specific lens: spirit-swap kit identity surface + WS1A.3/WS1A.4 downstream consumer cleanliness
- The migration cost of A vs B (config/elements.yaml canonical-7+1 IS already shaped for A semantically; less migration if Architecture A)
- My soft lean for A + explicit reasoning
- Acknowledgment that the data does NOT force the answer; this IS a design call

---

## 4. Confidence-degradation acknowledgment + Phase 5a synthesis preparation

### 4.1 Acknowledgment

I accept the three confidence-degraded primaries as named:
- **earth=MEDIUM** — backstop via pool depth (22 allow-list)
- **physical=DEGRADED** — by-construction (Phase 3 excluded) + WEAK-8 substrate
- **wind=HIGH-with-caveat** — storm-flex high yield; wind-PURE structurally thin

### 4.2 Phase 5a synthesis preparation per primary

Carrying confidence-degradation forward into synthesis:

| Primary | Phase 5a curation approach |
|---|---|
| fire | Cross-track core (ember, cinder) + pool depth preservation; minimal expansion |
| water | High-confidence cross-track core (tide, torrent, glacial, brine) + pool depth + selective JRPG/tabletop additions (aqua, frost, chill); resolve water↔wind=7 contamination per candidate |
| earth | LEAN ON POOL DEPTH (research yield is research-thin, not substrate-thin); cross-track core (stone, quake, tremor) preserved; minimal additions |
| wind | EXPLICIT STORM-FLEX SEPARATION: wind-PURE subset (cross-track-confirmed) + storm-flex subset (labeled as flex); resolve water↔wind=7 by routing hurricane/squall/stormtide to wind, mist/njord to water |
| lightning | T6 core (arc, surge, static, volt, bolt, lightning, shock, spark, thundara, thunder) — natural depth at 10-12 |
| holy | CORE + SATELLITES: radiance/divine/sacred core + non-religious satellites (dawn, aurora, lux/celestial designer-judgment); resist religious-coded bias per PG-1 surface 2 |
| shadow | LAYER-PICK: void/shade/umbra cross-track core (3-of-3 tracks) + 1-2 SMT proper-noun representatives + 1-2 Solo Leveling representatives (isekai-genre alignment for Reincarnated) + 1-2 FF mechanical |
| physical | DEFERRED: pending Phase 5b PG-3 architecture decision; synthesis presents BOTH architecture options with the 9-candidate damage-type-taxonomy as the substrate for either path |

### 4.3 Wave-state-wide curation note

The 31 high-confidence (score≥T6 AND tracks≥2) candidates are the synthesis-curation CORE. Bootstrap stability validates them. Single-track borderline (92 total) is designer-judgment surface — NOT auto-drop.

---

## 5. Borderline candidate audit acknowledgment

- **lux + celestial:** acknowledged as SINGLE-TRACK BORDERLINE. Both Latin-tier vocabulary; JRPG_isekai-only sampling artifact, not substrate scarcity. Phase 5a synthesis surfaces both for designer-judgment per PG-1 § 2 surface 2 (non-religious-coded holy curation priority). My lean: include both in synthesis recommendation as Latin-tier non-religious-coded options; Matt's PG-3 call.

- **Greek Anemoi (aeolus / boreas / notus / zephyrus / eurus):** acknowledged as tabletop-single-track-borderline. These ARE substrate-distinct mythological depth that tabletop weight elevation was forward-noted to capture. Phase 5a synthesis MUST treat as designer-judgment surface. My lean: include 2-3 Anemoi as wind primary entries for mythological-depth.

- **Solo Leveling shadow vocabulary:** acknowledged as JRPG-single-track-borderline. Isekai-genre-defining for Reincarnated's D10 positioning. Phase 5a synthesis MUST treat as designer-judgment surface. My lean: include 2-3 Solo Leveling shadow entries.

- **92 total single-track borderline:** I will not enumerate per-primary here; raw JSON has them. Phase 5a synthesis applies designer-judgment per primary curation.

---

## 6. Forward note for Phase 5a synthesis (design-side considerations to foreground)

When I author Phase 5a synthesis draft at `agentic_orchestration/gandalf/notes/2026-06-XX-q18-flavor-pool-research-synthesis.md`, the following design-side considerations get explicit foregrounding:

1. **water↔wind=7 contamination as designated curation-decision section.** Not buried in per-primary lists. Each contamination candidate gets explicit slot-routing rationale.

2. **7-vs-8 BOTH architecture options presented with empirical evidence + genre-canonical convergence + gandalf lean for Architecture A.** Matt decides at Phase 5b Pattern B.

3. **Per-primary cardinality TARGET (not floor) per § 1.4 ranges above** with explicit rationale per primary. T6 floors are reported as empirical bounds; synthesis curation lands somewhere between T6 and pool-depth based on substrate-honest natural depth.

4. **Existing-pool audit integrated per Q-shape-4 ratification.** Preserve / demote / extend per existing pool entry against research findings. Pool ember/cinder (cited in research) PRESERVED. Pool entries with NO research citation flagged for demote-to-eligible decision at Phase 5b.

5. **Holy curation priority: non-religious-coded core + religious-coded flagged for design-tone decision at PG-3.** Per PG-1 surface 2.

6. **Shadow curation priority: 3-layer pick weighted toward isekai-genre alignment (Solo Leveling representation).** Per PG-1 § 2 surface 3 + Reincarnated D10 positioning.

7. **Wind curation priority: wind-PURE explicit + storm-flex explicit + Greek Anemoi mythological depth.** Per PG-1 surface 1 + § 8.2 of stats verdict caveat.

8. **Lux + celestial + Anemoi + Solo Leveling shadow vocab surfaced as designer-judgment items requiring Matt input at PG-3.** Not auto-bucketed.

9. **Q18.a-e structural decisions consolidated per evidence:**
   - Q18.a (primary scope): canonical-7+1 preserved (subject to PG-3 7-vs-8 lock)
   - Q18.b (source of authority): genre-vote + designer curation (substrate-led with designer encoding gate)
   - Q18.c (flex semantics): cross-primary contamination as per-candidate slot-routing decision (water↔wind=7 set worked through)
   - Q18.d (d1_status filter): preserve pool's allow-list / eligible / quarantine structure; extend to new entries with research-based d1_status
   - Q18.e (cardinality target): natural-depth per primary, NOT floor or ceiling, per § 1.4 ranges

---

## 7. Framing-audit Q1-Q3 (Discipline #42)

**Q1 — Load-bearing assumptions in this PG-2 ratification:**
- (a) Elrond's methodology execution faithfully implements PG-0 § 5 lock
- (b) 7-vs-8 substrate verdict (WEAK-8) is correctly bounded as empirical, not architectural
- (c) Single-track borderline is designer-judgment surface, not auto-drop
- (d) Architecture A (7-primary + physical-taxonomy-sibling) is the substrate-honest design lean
- (e) Phase 5a synthesis can proceed without further Phase 3 expansion
- (f) F-6 NOT-fired disposition is correct

**Q2 — Refutation evidence in current scope:**
- (a) Spot-checked stats verdict § 2 + § 3 + § 5 against raw JSON `q18_flavor_stats_results_2026-06-01.json` + pool.json — methodology fidelity confirmed
- (b) § 7 of stats verdict explicitly carries WEAK-8 as empirical + § 7.7 explicitly out-of-scopes architectural-commitment. Disposition is methodologically clean.
- (c) Borderline audit (§ 10) explicitly carries single-track-borderline as designer-judgment surface, not drop. § 10.3 calls this out.
- (d) Architecture A lean is substrate-honest reading — but Phase 5b Pattern B is the decision point, not Phase 5a synthesis. My lean does NOT bypass Matt's decision authority.
- (e) Possible refutation: if Phase 5a synthesis drafting surfaces a substrate gap I cannot currently anticipate (e.g., a primary where the curation cannot land between T6 and pool-depth coherently), amendment loop fires via PG-2.5 in-flight back-route. This is a known unknown; not refutation now.
- (f) F-6 disposition confirmed via § 11 stats verdict; data shape is firmly quantitative-amenable.

**Q3 — Refinement needed:**
- NO refinement needed at PG-2 scope. The dataset is sufficient for Phase 5a synthesis to proceed.
- One forward note to Phase 5a: synthesis MUST present 7-vs-8 as TWO architecture options for Phase 5b Pattern B, NOT as a single recommended option with my lean buried. My lean is articulated; Matt's call.

**Framing-audit verdict: PG-2 ratification is substrate-coherent; RATIFIED.**

---

## 8. Substrate-led discipline composition note (Discipline #41)

The vocabulary catalogue IS the substrate. Genre votes ground the lock empirically. Designer curation at Phase 5a happens post-research, post-stats — the encoding gate per Disc #41 refinement.

This PG-2 ratification respects substrate-led discipline by:
- ACCEPTING the empirical 7-vs-8 verdict (WEAK-8) as substrate's vote on physical's qualitative distinctness, even though it's not the cleanest "all primaries look the same" outcome
- NOT overriding earth's MEDIUM confidence based on designer preference for higher confidence (substrate's research yield IS what it is)
- NOT overriding the storm-flex concentration on wind — accepting that wind's HIGH yield is concentrated in storm-flex AND wind-PURE is structurally thin, as TWO substrate-honest facts
- ACCEPTING the cross-track-confirmed core (31 high-confidence candidates) as the synthesis-curation starting point — not pre-imposing designer-preferred vocabulary
- ACCEPTING that physical's vocabulary IS taxonomic not phenomenological — the substrate has voted, my Architecture A lean follows the vote
- FORWARDING the architectural-commitment decision to Phase 5b Matt without pre-commitment — substrate informs, designer + Matt curate at the encoding gate

**Discipline #41 composition: PASS.**

Composition with substrate-led + framing-audit at PG-2: the empirical evidence in the stats verdict IS the substrate vote. Framing-audit Q1-Q3 ensures I have not pre-imposed designer-frame assumptions on the empirical reading. Both disciplines compose into a clean ratification posture.

---

## 9. Routing instruction for KR

**Routing: RATIFIED — fire Phase 5a synthesis draft authoring (gandalf seam).**

KR action items:
1. Update wave-state file: PG-2 PASS; Phase 5a fires (gandalf seam); decision-log entry appended
2. Phase 5a authoring is GANDALF SEAM (not dispatch-routed); I will author at `agentic_orchestration/gandalf/notes/2026-06-XX-q18-flavor-pool-research-synthesis.md` per operational sequence § 2 sub-phase 5a
3. KR confirms timing for Phase 5a: I can author in-wave as continuation of this PG-2 verdict OR KR routes a fresh gandalf sub-agent invocation for synthesis draft. Either works; KR decides per orchestration efficiency. (My recommendation: fresh sub-agent invocation for synthesis — synthesis is substantial Pattern A-deep / authoring scope, distinct from PG-2 Pattern A-light verdict.)
4. Post-Phase-5a draft, KR HALTS at Phase 5b for Matt Pattern B (PG-3 architectural-commitment lock). PG-3 is Matt-decision per ADR-002 architectural-commitment scope.
5. Critique-pair coverage: Phase 5c canonical write gets jack-ryan Gate-2 at PG-4 (wave-close criterion).

**No halt for Matt at this gate.** Matt's next touchpoint is PG-3 (Phase 5b Pattern B architectural-commitment lock). The wave proceeds per operational sequence § 2.

---

## 10. Sign-off

**PG-2 verdict: RATIFIED. Dataset sufficient. No amendment-loop fired. Proceed to Phase 5a synthesis draft authoring.**

**Authority chain:**
- Matt 2026-06-01 verbatim "hand to KR to fire the wave"
- Hive-mind decision-routing Matt 2026-05-23: PG-2 scope is gandalf design-side seam authority
- Pattern A-light protocol per operational sequence § 2 Phase 4 phase-gate definition

**Disciplines composed:**
- Discipline #41 substrate-led (§ 8 explicit composition)
- Discipline #42 framing-audit (§ 7 Q1-Q3 application)
- Discipline #18 spirit (methodology lock executed faithfully per PG-0 § 5; § 2.1 verification)

**Forward to Phase 5a:** § 6 carries the 9 design-side considerations to foreground in synthesis draft.

**Forward to Phase 5b Pattern B:** § 3 carries the 7-vs-8 design-side framing for Matt's PG-3 decision.

**End of PG-2 ratification.**
